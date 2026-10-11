"""The country atlas data: panel, global factors, per-economy statistics and channel synchronization.

Port of atlas/data.py, atlas/stats.py and atlas/sync.py (frozen). The arithmetic and its order are unchanged, so
the outputs are byte-identical to the as-run scripts on the same machine; only the paths come from the config.

build_panel  -> panel.csv, global.csv, meta.json   (data.py; reads the channel anatomy written by ef.data.channels)
build_stats  -> stats.json                         (stats.py)
build_sync   -> sync.json                          (sync.py)

Sources
  Global Macro Database (GMD; Mueller, Xu, Lehbib, Chen 2025) final panel and its cleaned source files:
     IMF World Economic Outlook, IMF Public Finances in Modern History (FPP), IMF Historical Public Debt (HDD)
  Penn World Table 10.01 (four GDP-growth patches; validation of contributions)
  BP Statistical Review via Our World in Data; EIA Brent via datasets/oil-prices (oil)

Data repairs (all logged to meta.json -> 'fixes'):
  1. GDP growth: 4 country-years where GMD disagrees with both PWT and Maddison by >2pp are replaced
     with PWT growth (deflator rescaled so nominal GDP is unchanged).
  2. Expenditure contributions: exports and imports are deflated with the GDP deflator (no component
     deflators exist for all 26), so they are reported only as net exports; years where C+I+NX misses
     GDP growth by >3pp (national-accounts breaks) are blanked.
  3. Budget: GMD revenue has coverage jumps (central vs general government). Spending and balance are
     taken from IMF WEO from its first year; earlier years from IMF FPP, level-matched to WEO at the
     junction and cut at FPP coverage breaks. Revenue = spending + balance.
  4. Debt: WEO from its first year; earlier years IMF HDD, ratio-matched at the junction.
  5. Money: growth in log points; real = nominal log growth - log(1+inflation); definitional breaks dropped.
"""
import json
import os

import numpy as np
import pandas as pd
import pyreadr
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr

from ef import config

ORDER = [('USA', 'United States', 'North America'), ('CAN', 'Canada', 'North America'), ('MEX', 'Mexico', 'North America'),
 ('DEU', 'Germany', 'Western Europe'), ('FRA', 'France', 'Western Europe'), ('GBR', 'United Kingdom', 'Western Europe'), ('ITA', 'Italy', 'Western Europe'),
 ('NLD', 'Netherlands', 'Western Europe'), ('BEL', 'Belgium', 'Western Europe'), ('AUT', 'Austria', 'Western Europe'), ('CHE', 'Switzerland', 'Western Europe'),
 ('SWE', 'Sweden', 'Nordics'), ('NOR', 'Norway', 'Nordics'), ('DNK', 'Denmark', 'Nordics'), ('FIN', 'Finland', 'Nordics'),
 ('ESP', 'Spain', 'Southern Europe & Turkey'), ('PRT', 'Portugal', 'Southern Europe & Turkey'), ('GRC', 'Greece', 'Southern Europe & Turkey'), ('TUR', 'Turkey', 'Southern Europe & Turkey'),
 ('JPN', 'Japan', 'Asia-Pacific'), ('KOR', 'South Korea', 'Asia-Pacific'), ('AUS', 'Australia', 'Asia-Pacific'), ('IND', 'India', 'Asia-Pacific'),
 ('IDN', 'Indonesia', 'Asia-Pacific'), ('THA', 'Thailand', 'Asia-Pacific'), ('ZAF', 'South Africa', 'Africa')]
ISOS = [o[0] for o in ORDER]
# economies added after the first edition: processed identically, but compared with the 26 (never part of their averages)
EXTRA = [('CHN', 'China', 'Added · East Asia'), ('BRA', 'Brazil', 'Added · Latin America'), ('SAU', 'Saudi Arabia', 'Added · Middle East'),
 ('ARE', 'United Arab Emirates', 'Added · Middle East'), ('IRN', 'Iran', 'Added · Middle East')]
XISOS = [o[0] for o in EXTRA]; ALLS = ISOS+XISOS
GDP_FROM = {'SAU': 1970, 'ARE': 1975}      # earlier national-accounts levels are spliced estimates (SAU: +53% "growth" in 1970; ARE: +77% in 1973)
COMP_FROM = {'BRA': 1981, 'ARE': 1975}     # Brazil's expenditure components before 1980 do not add up (C+I+X-M = 128-141% of GDP; imports recorded as 0)
CONTRIB_FROM = {'BRA': 1996}               # annual-average deflation is unreliable through hyperinflation and the 1994 Real Plan
INFL_FROM = {'ARE': 1980}                  # 1970-77 values are a constant 22.0 placeholder; CPI starts in 1980
STRATE_FROM_POLICY = ['SAU']               # money-market rate covers only 2010-17; use the SAMA policy (repo) rate, 1999-2022
GROWTH_PATCH = [('AUT', 1988), ('SWE', 1981), ('PRT', 1988), ('PRT', 1990)]   # GMD splice errors (vs PWT and Maddison)
MONEY_MANUAL = [('ITA', 1999), ('ESP', 1999), ('GRC', 1999), ('CAN', 2007)]   # euro changeover / series redefinitions
UNEMP_BREAK = [('ZAF', 1995)]                                                 # survey change
LTRATE_BAD = [('MEX', 2021), ('MEX', 2022)]                                   # 19.7% placeholder value in GMD (actual 10-y yield ~7-9%)
GL = [1975, 1982, 1991, 2009, 2020]


def _gmd(): return config.raw_file('gmd', 'data/final/data_final.dta')


def _imf(name): return config.raw_file('gmd', f'data/clean/aggregators/IMF/IMF_{name}.dta')


def build_panel(out_dir, panel26_path, verbose=True):
    """data.py: the country-year panel (1950-2022) with every repair logged, and the global factors."""
    G = pd.read_stata(_gmd())
    G = G[G.ISO3.isin(ALLS) & (G.year >= 1950) & (G.year <= 2022)].copy(); G['year'] = G.year.astype(int)
    WEO = pd.read_stata(_imf('WEO')); FPP = pd.read_stata(_imf('FPP')); HDD = pd.read_stata(_imf('HDD'))
    for d_ in (WEO, FPP, HDD): d_['year'] = d_.year.astype(int)
    PWT = pyreadr.read_r(config.raw_file('pwt'))['pwt10.01']; PWT['year'] = PWT.year.astype(int)
    b, a = butter(2, [(1/9)/0.5, 0.49/0.5], btype='band')
    FIX = {iso: {} for iso in ALLS}

    def first_year(df, iso, col):
        s = df[(df.ISO3 == iso) & df[col].notna() & (df.year <= 2022)].year
        return int(s.min()) if len(s) else None

    frames = []
    for iso in ALLS:
        d = G[G.ISO3 == iso].sort_values('year').set_index('year').reindex(range(1950, 2023))
        if iso in GDP_FROM:
            d.loc[:GDP_FROM[iso]-1, ['rGDP', 'nGDP', 'deflator', 'cons', 'inv', 'exports', 'imports', 'rGDP_USD']] = np.nan
            FIX[iso]['gdp_from'] = GDP_FROM[iso]
        if iso in COMP_FROM:
            d.loc[:COMP_FROM[iso]-1, ['cons', 'inv', 'exports', 'imports', 'cons_GDP', 'inv_GDP', 'exports_GDP', 'imports_GDP']] = np.nan; FIX[iso]['components_from'] = COMP_FROM[iso]
        if iso in INFL_FROM:
            d.loc[:INFL_FROM[iso]-1, ['infl', 'CPI']] = np.nan; FIX[iso]['infl_from'] = INFL_FROM[iso]
        if iso in STRATE_FROM_POLICY:
            d['strate'] = d.cbrate; FIX[iso]['strate_is_policy_rate'] = [int(d.cbrate.first_valid_index()), int(d.cbrate.last_valid_index())]
        o = pd.DataFrame(index=d.index); o['iso'] = iso
        rg = d.rGDP.copy(); defl = d.deflator.copy()
        # 1. growth patches
        for (i, y) in GROWTH_PATCH:
            if i != iso: continue
            pw = PWT[PWT.isocode == iso].set_index('year').rgdpna
            g_new = pw[y]/pw[y-1]; old = rg[y]; new = rg[y-1]*g_new; f = new/old
            rg.loc[y:] = rg.loc[y:]*f; defl.loc[y:] = defl.loc[y:]/f
        o['rGDP'] = rg; o['growth'] = 100*rg.pct_change(); o['rGDP_USD'] = d.rGDP_USD; o['deflator'] = defl
        for (i, y) in GROWTH_PATCH:
            if i == iso:   # [year, GMD growth, replacement (PWT) growth]
                FIX[iso].setdefault('growth_patch', []).append([y, round(float(100*(d.rGDP[y]/d.rGDP[y-1]-1)), 1), round(float(o.growth[y]), 1)])
        # 2. contributions (GDP-deflator real); exports/imports only as net exports
        for k in ['cons', 'inv', 'exports', 'imports']:
            o['r_'+k] = d[k]/defl*100
        y0 = o.rGDP.shift(1)
        o['c_C'] = 100*o.r_cons.diff()/y0; o['c_I'] = 100*o.r_inv.diff()/y0
        o['c_X'] = 100*o.r_exports.diff()/y0; o['c_M'] = -100*o.r_imports.diff()/y0
        o['c_NX'] = o.c_X+o.c_M
        o['c_resid'] = o.growth-(o.c_C+o.c_I+o.c_NX)
        blank = (o.c_resid.abs() > 3) | o.index.isin([y for (i, y) in GROWTH_PATCH if i == iso])
        bl = [int(y) for y in o.index[blank & (o.index >= 1971)]]
        # alternative: C and I deflated with CPI (domestic prices), contribution = own real growth x lagged nominal share,
        # net exports = GDP growth - C - I.  Removes terms-of-trade effects that the GDP deflator puts into C and I.
        sh = lambda k: (d[k]/d.nGDP).shift(1)
        o['cC_cpi'] = 100*((d.cons/d.CPI)/(d.cons/d.CPI).shift(1)-1)*sh('cons')
        o['cI_cpi'] = 100*((d.inv/d.CPI)/(d.inv/d.CPI).shift(1)-1)*sh('inv')
        o['cNX_cpi'] = o.growth-o.cC_cpi-o.cI_cpi
        if iso in CONTRIB_FROM:
            blank = blank | (o.index < CONTRIB_FROM[iso]); bl = [y for y in bl if y >= CONTRIB_FROM[iso]]; FIX[iso]['contrib_from'] = CONTRIB_FROM[iso]
        for c in ['c_C', 'c_I', 'c_X', 'c_M', 'c_NX', 'cC_cpi', 'cI_cpi', 'cNX_cpi']: o.loc[blank, c] = np.nan
        if bl: FIX[iso]['contrib_blank'] = bl
        # choose the deflation that best reproduces Penn World Table volume contributions (1971-2019)
        q = PWT[PWT.isocode == iso].set_index('year').sort_index(); q0 = q.rgdpna.shift(1)
        pc = pd.DataFrame({'C': 100*q.rconna.diff()/q0, 'I': 100*(q.rdana-q.rconna).diff()/q0, 'NX': 100*(q.rgdpna-q.rdana).diff()/q0})
        if iso == 'AUS': pc = (pc+pc.shift(1))/2      # PWT Australia runs on July-June years: average to calendar timing
        val = {}
        for lab, cols in [('gdp_deflator', ['c_C', 'c_I', 'c_NX']), ('cpi', ['cC_cpi', 'cI_cpi', 'cNX_cpi'])]:
            j = pd.concat([o[cols].set_axis(['C', 'I', 'NX'], axis=1), pc], axis=1, keys=['o', 'p']).loc[1971:2019].dropna()
            val[lab] = {k: round(float(np.corrcoef(j['o'][k], j['p'][k])[0, 1]), 2) for k in ['C', 'I', 'NX']}
        m = 'cpi' if (np.mean(list(val['cpi'].values())) > np.mean(list(val['gdp_deflator'].values()))+0.005) else 'gdp_deflator'
        if m == 'cpi': o['c_C'], o['c_I'], o['c_NX'] = o.cC_cpi, o.cI_cpi, o.cNX_cpi
        FIX[iso]['contrib_method'] = m; FIX[iso]['contrib_validation'] = val[m]
        for k in ['cons_GDP', 'inv_GDP', 'exports_GDP', 'imports_GDP', 'strate', 'ltrate', 'infl', 'unemp', 'CA_GDP', 'REER', 'USDfx',
                  'BankingCrisis', 'CurrencyCrisis', 'SovDebtCrisis']:
            o[k] = d[k]
        for (i, y) in LTRATE_BAD:
            if i == iso and not np.isnan(o.ltrate.get(y, np.nan)): o.loc[y, 'ltrate'] = np.nan; FIX[iso].setdefault('ltrate_dropped', []).append(y)
        for (i, y) in UNEMP_BREAK:
            if i == iso: o['unemp_break'] = (o.index == y); FIX[iso]['unemp_break'] = y
        if 'unemp_break' not in o: o['unemp_break'] = False
        o['real_strate'] = o.strate-o.infl
        # 3. budget: WEO from its first year, IMF FPP before (level-matched, cut at coverage breaks)
        o['govexp_GDP_gmd'] = d.govexp_GDP; o['govrev_GDP_gmd'] = d.govrev_GDP; o['govdef_GDP_gmd'] = d.govdef_GDP; o['govdebt_GDP_gmd'] = d.govdebt_GDP
        w = WEO[WEO.ISO3 == iso].set_index('year').reindex(o.index); f = FPP[FPP.ISO3 == iso].set_index('year').reindex(o.index)
        s = first_year(WEO, iso, 'IMF_WEO_govexp_GDP')
        exp = pd.Series(np.nan, index=o.index); bal = pd.Series(np.nan, index=o.index); hist = pd.Series(False, index=o.index)
        exp.loc[s:] = w.IMF_WEO_govexp_GDP.loc[s:]; bal.loc[s:] = w.IMF_WEO_govdef_GDP.loc[s:]
        fe, fr, fb = f.IMF_FPP_govexp_GDP, f.IMF_FPP_govrev_GDP, f.IMF_FPP_govdef_GDP
        start = s
        if s > 1950 and not np.isnan(fe.get(s, np.nan)) and abs(exp[s]-fe[s]) <= 3 and abs(bal[s]-fb[s]) <= 1.5:
            ae = exp[s]-fe[s]; ab = bal[s]-fb[s]
            t = s-1
            while t >= 1950 and not np.isnan(fe.get(t, np.nan)):
                de = fe[t+1]-fe[t]; dr = fr[t+1]-fr[t]; db = fb[t+1]-fb[t]
                if max(abs(de), abs(dr)) > 6 and abs(db) < 0.5*max(abs(de), abs(dr)): break   # coverage break between t and t+1
                exp[t] = fe[t]+ae; bal[t] = fb[t]+ab; hist[t] = True; start = t; t -= 1
            FIX[iso]['fiscal'] = {'weo_from': s, 'hist_from': start if start < s else None, 'level_adj_exp': round(float(ae), 1), 'level_adj_bal': round(float(ab), 1)}
        else:
            gap = [round(float(exp[s]-fe[s]), 1), round(float(bal[s]-fb[s]), 1)] if not np.isnan(fe.get(s, np.nan)) else None
            FIX[iso]['fiscal'] = {'weo_from': s, 'hist_from': None, 'hist_gap_too_large': gap}
        # breaks inside the assembled series (spending jumps not matched by the balance)
        brk = []
        for t in range(max(start, 1951), 2023):
            de = exp.get(t, np.nan)-exp.get(t-1, np.nan); db = bal.get(t, np.nan)-bal.get(t-1, np.nan)
            if not np.isnan(de) and abs(de) > 6 and abs(db) < 0.5*abs(de): brk.append(t)
        if brk: FIX[iso]['fiscal']['breaks'] = brk
        o['govexp_GDP'] = exp; o['govdef_GDP'] = bal; o['govrev_GDP'] = exp+bal; o['fiscal_hist'] = hist
        o['fiscal_break'] = o.index.isin(brk)
        # 4. debt: WEO from its first year, HDD before (ratio-matched)
        sd = first_year(WEO, iso, 'IMF_WEO_govdebt_GDP'); h = HDD[HDD.ISO3 == iso].set_index('year').IMF_HDD_govdebt_GDP.reindex(o.index)
        debt = pd.Series(np.nan, index=o.index); dh = pd.Series(False, index=o.index)
        debt.loc[sd:] = w.IMF_WEO_govdebt_GDP.loc[sd:]
        j = [y for y in range(sd, 2016) if not np.isnan(h.get(y, np.nan))]
        ratio = debt[j[0]]/h[j[0]] if j else np.nan
        if j and 0.75 <= ratio <= 1.34:
            hh = h.loc[:sd-1].copy(); gm = d.govdebt_GDP.reindex(hh.index)
            fill = hh.isna() & gm.notna() & (hh.index >= hh.first_valid_index())          # HDD gaps: GMD's own series if it agrees with HDD nearby
            if fill.any() and (gm-hh).abs().dropna().mean() < 3: hh[fill] = gm[fill]; FIX[iso].setdefault('debt_gapfill', [int(y) for y in hh.index[fill]])
            miss = hh.isna(); hh = hh.interpolate(limit=3, limit_area='inside')             # short internal gaps: linear (dotted segment anyway)
            ip = [int(y) for y in hh.index[miss & hh.notna() & (hh.index >= 1970)]]
            if ip: FIX[iso]['debt_interp'] = ip
            pre = hh.dropna(); debt.loc[pre.index] = pre*ratio; dh.loc[pre.index] = True
            FIX[iso]['debt'] = {'weo_from': sd, 'hdd_ratio': round(float(ratio), 3)}
        elif j:
            FIX[iso]['debt'] = {'weo_from': sd, 'hdd_ratio': None, 'hdd_ratio_too_far': round(float(ratio), 3)}
        else:
            FIX[iso]['debt'] = {'weo_from': sd, 'hdd_ratio': None}
        o['govdebt_GDP'] = debt; o['debt_hist'] = dh
        # 5. money: log growth, M2 chain-linked with M3 (then M1) where M2 stops; real = log nominal - log(1+inflation)
        gm = {m: 100*np.log(d[m]).diff() for m in ['M2', 'M3', 'M1']}
        mg = gm['M2'].copy(); src = pd.Series(np.where(mg.notna(), 'M2', None), index=d.index, dtype=object)
        last_m2 = d.M2.last_valid_index()
        for alt in ['M3', 'M1']:
            fill = (mg.isna()) & (gm[alt].notna()) & (d.index > (last_m2 if last_m2 is not None else 0))
            mg[fill] = gm[alt][fill]; src[fill] = alt
        rm = mg-100*np.log1p(o.infl/100)
        m2 = (src == 'M2')
        odd = m2 & gm['M3'].notna() & gm['M1'].notna() & ((mg-gm['M3']).abs() > 15) & ((mg-gm['M1']).abs() > 15)      # M2 disagrees with both M1 and M3
        odd |= m2 & gm['M3'].isna() & gm['M1'].notna() & ((mg-gm['M1']).abs() > 25) & (rm.abs() > 15)                 # no M3: M2 far from M1 and implausible in real terms
        drop = (((rm.abs() > 40) & (o.infl < 100)) | odd | o.index.isin([y for (i, y) in MONEY_MANUAL if i == iso])) & mg.notna()   # in hyperinflation only the M1/M3 check applies
        dl = [int(y) for y in o.index[drop & (o.index >= 1970)]]
        mg[drop] = np.nan; rm[drop] = np.nan
        if dl: FIX[iso]['money_dropped'] = dl
        o['money_growth'] = mg; o['money_src'] = src.where(mg.notna()); o['real_money_growth'] = rm
        # business cycle: 2-9y band-pass of log real GDP (zero-phase), full 1950-2022 run-in
        sl = np.log(o.rGDP).interpolate(limit=2); ok = sl.notna()
        cyc = pd.Series(np.nan, index=o.index); ph = pd.Series(np.nan, index=o.index)
        x = sl[ok].values; c = filtfilt(b, a, x-x.mean()); cyc[ok] = c; ph[ok] = np.angle(hilbert(c))
        o['cycle'] = cyc; o['phase'] = ph
        frames.append(o.reset_index().rename(columns={'index': 'year'}))
    P = pd.concat(frames, ignore_index=True)
    # China: official growth vs the alternative (Harry Wu) estimates that Penn World Table and Maddison use
    _pw = PWT[PWT.isocode == 'CHN'].set_index('year').rgdpna; _pg = 100*_pw.pct_change(); _og = P[P.iso == 'CHN'].set_index('year').growth
    FIX['CHN']['alt_growth'] = {'official_mean_1978_2019': round(float(_og.loc[1978:2019].mean()), 1), 'pwt_mean_1978_2019': round(float(_pg.loc[1978:2019].mean()), 1),
        'official_1998': round(float(_og[1998]), 1), 'pwt_1998': round(float(_pg[1998]), 1), 'official_2008': round(float(_og[2008]), 1), 'pwt_2008': round(float(_pg[2008]), 1)}

    # rest-of-world cycle for each economy: mean of the other 25 standardized cycles; and RoW phase
    W = P.pivot(index='year', columns='iso', values='cycle').loc[1955:2022]
    Z = (W-W.loc[1970:2022].mean())/W.loc[1970:2022].std()
    PH = P.pivot(index='year', columns='iso', values='phase').loc[1955:2022]
    row = {}; rowph = {}
    for iso in ALLS:
        others = [i for i in ISOS if i != iso]      # added economies are compared with all 26
        row[iso] = Z[others].mean(axis=1)
        rowph[iso] = np.angle(np.exp(1j*PH[others]).mean(axis=1))
    P = P.merge(pd.DataFrame(row).stack().rename('row_cycle').reset_index().rename(columns={'level_1': 'iso'}), on=['year', 'iso'], how='left')
    P = P.merge(pd.DataFrame(rowph, index=PH.index).stack().rename('row_phase').reset_index().rename(columns={'level_1': 'iso'}), on=['year', 'iso'], how='left')
    P['cycle_z'] = P.groupby('iso').cycle.transform(lambda s: (s-s[(P.loc[s.index, 'year'] >= 1970)].mean())/s[(P.loc[s.index, 'year'] >= 1970)].std())
    P.to_csv(os.path.join(out_dir, 'panel.csv'), index=False)

    # ---------------- global factors ----------------
    A = P[(P.year >= 1965) & P.iso.isin(ISOS)].copy()      # world aggregates stay the 26
    wts = A.pivot(index='year', columns='iso', values='rGDP_USD'); w = wts.div(wts.sum(axis=1), axis=0)
    gr = A.pivot(index='year', columns='iso', values='growth')
    glob = pd.DataFrame(index=range(1965, 2023))
    glob['world_growth'] = (gr*w).sum(axis=1, min_count=20)
    glob['n_contracting'] = (gr < 0).sum(axis=1)
    imr = A.pivot(index='year', columns='iso', values='imports_GDP')
    glob['world_imports_GDP'] = (imr*w).sum(axis=1, min_count=20)/w.where(imr.notna()).sum(axis=1)
    inf = A.pivot(index='year', columns='iso', values='infl')
    glob['infl_med'] = inf.median(axis=1); glob['infl_q25'] = inf.quantile(.25, axis=1); glob['infl_q75'] = inf.quantile(.75, axis=1)
    sr = A.pivot(index='year', columns='iso', values='strate')
    glob['us_strate'] = sr['USA']; glob['strate_med_ex_us'] = sr.drop(columns='USA').median(axis=1)
    dsr = sr.diff(); glob['share_raising'] = (dsr > 0).sum(axis=1)/dsr.notna().sum(axis=1)
    glob['n_raising'] = (dsr > 0).sum(axis=1); glob['n_rate_obs'] = dsr.notna().sum(axis=1)
    bc = A.pivot(index='year', columns='iso', values='BankingCrisis'); glob['banking_onsets'] = bc.sum(axis=1)
    cc = A.pivot(index='year', columns='iso', values='CurrencyCrisis'); glob['currency_onsets'] = cc.sum(axis=1)
    glob['us_reer'] = A[A.iso == 'USA'].set_index('year').REER
    bp = pd.read_csv(config.raw_file('oil_bp'))
    bp = bp[bp.Entity == 'World'].set_index('Year')['Crude oil price (BP Statistics (2016))']
    br = pd.read_csv(config.raw_file('oil_brent')); br['year'] = br.Date.str[:4].astype(int); br = br.set_index('year').Price
    Gu = pd.read_stata(_gmd()); cpi = Gu[Gu.ISO3 == 'USA'].assign(year=lambda d: d.year.astype(int)).set_index('year').CPI
    br_real = br*cpi.loc[2015]/cpi.reindex(br.index)
    ov = pd.concat([bp, br_real], axis=1, keys=['bp', 'eia']).loc[1988:2015].dropna()
    oil = bp.reindex(range(1965, 2023)).copy(); oil.loc[2016:2022] = br_real.loc[2016:2022]
    glob['oil_real_2015usd'] = oil
    r26 = json.load(open(panel26_path))
    for ch in ['GDP', 'inv', 'imports', 'strate', 'govexp']:
        glob['sync_'+ch] = pd.Series(r26['r_t'][ch], index=r26['years'])
    glob.index.name = 'year'; glob.to_csv(os.path.join(out_dir, 'global.csv'))
    json.dump({'order': ORDER, 'extra': EXTRA, 'fixes': FIX}, open(os.path.join(out_dir, 'meta.json'), 'w'), indent=1, default=int)
    if verbose:
        print("panel", P.shape, "global", glob.shape)
        print("oil splice check 1988-2015: mean |EIA/BP-1| =", f"{(ov.eia/ov.bp-1).abs().mean():.3f}")
        print("blanked country-years:", sum(len(v.get('contrib_blank', [])) for v in FIX.values()))
        vv = pd.DataFrame({i: FIX[i]['contrib_validation'] for i in ISOS}).T
        print("contribution method:", {i: FIX[i]['contrib_method'] for i in ALLS}); print("validation vs PWT, median r:", vv.median().round(2).to_dict())
    return P, glob, FIX


def build_stats(out_dir, verbose=True):
    """stats.py: per-economy statistics, 1970-2022 (growth contributions 1971-2022), from panel.csv and meta.json."""
    P = pd.read_csv(os.path.join(out_dir, 'panel.csv')); META = json.load(open(os.path.join(out_dir, 'meta.json')))
    ORDER_ = META['order']+META.get('extra', []); FIX = META['fixes']
    OMEGA = 2*np.pi/5.85

    def nz(x): return None if (x is None or (isinstance(x, float) and np.isnan(x))) else x
    S = {}
    for iso, name, region in ORDER_:
        d = P[P.iso == iso].set_index('year'); w = d.loc[1970:2022]; wc = d.loc[1971:2022]
        st = {'iso': iso, 'name': name, 'region': region}
        g = w.growth.dropna()
        st['growth_mean'] = g.mean(); st['growth_sd'] = g.std(); st['worst'] = (g.min(), int(g.idxmin())); st['best'] = (g.max(), int(g.idxmax()))
        st['n_neg'] = int((g < 0).sum()); st['neg_years'] = [int(y) for y in g[g < 0].index]
        st['gr_global'] = {str(y): nz(float(d.growth.get(y, np.nan))) for y in GL}
        st['n_contract_global'] = int(sum(1 for y in GL if d.growth.get(y, np.nan) < 0))
        # swing anatomy
        cc = wc[['growth', 'c_C', 'c_I', 'c_NX']].dropna(); vg = cc.growth.var()
        st['anat'] = {k: float(np.cov(cc['c_'+k], cc.growth)[0, 1]/vg) for k in ['C', 'I', 'NX']}
        st['anat']['resid'] = 1-sum(st['anat'].values()); st['anat_years'] = (int(cc.index.min()), int(cc.index.max()))
        cc19 = cc.loc[:2019]; vg19 = cc19.growth.var()
        st['anat_pre2020'] = {k: float(np.cov(cc19['c_'+k], cc19.growth)[0, 1]/vg19) for k in ['C', 'I', 'NX']}
        st['anat_n'] = int(len(cc))
        # composition
        st['shares_from'] = int(w.cons_GDP.first_valid_index())
        st['shares_1970'] = {k: nz(float(w[k+'_GDP'].dropna().iloc[0])) if w[k+'_GDP'].notna().any() else None for k in ['cons', 'inv', 'exports', 'imports']}
        st['shares_2022'] = {k: nz(float(d[k+'_GDP'].get(2022, np.nan))) for k in ['cons', 'inv', 'exports', 'imports']}

        # coupling to rest of world
        def cr(lo, hi):
            x = d.loc[lo:hi, ['cycle', 'row_cycle']].dropna()
            return float(np.corrcoef(x.cycle, x.row_cycle)[0, 1]) if len(x) >= 8 else None
        st['coup_7089'] = cr(1970, 1989); st['coup_9022'] = cr(1990, 2022); st['coup_all'] = cr(1970, 2022)
        st['coup_dec'] = {lab: cr(lo, hi) for lab, lo, hi in [('1970s', 1970, 1979), ('1980s', 1980, 1989), ('1990s', 1990, 1999), ('2000s', 2000, 2009), ('2010-22', 2010, 2022)]}

        def al(lo, hi):
            x = d.loc[lo:hi, ['phase', 'row_phase']].dropna(); return float(np.mean(np.cos(x.phase-x.row_phase)))
        st['align_7089'] = al(1970, 1989); st['align_9022'] = al(1990, 2022)
        x = d.loc[1970:2022, ['phase', 'row_phase']].dropna()
        st['phase_offset_yrs'] = float(np.angle(np.mean(np.exp(1j*(x.phase-x.row_phase))))/OMEGA)
        # rolling 10-y coupling
        roll = {}
        for y in range(1979, 2023):
            x = d.loc[y-9:y, ['cycle', 'row_cycle']].dropna(); roll[y] = float(np.corrcoef(x.cycle, x.row_cycle)[0, 1]) if len(x) >= 8 else None
        st['coup_roll'] = roll

        # budget
        def dm(col, lo, hi):
            s = d.loc[lo:hi, col].dropna(); return float(s.mean()) if len(s) else None
        st['spend_70s'] = dm('govexp_GDP', 1970, 1979); st['spend_10s'] = dm('govexp_GDP', 2010, 2022)
        st['rev_70s'] = dm('govrev_GDP', 1970, 1979); st['rev_10s'] = dm('govrev_GDP', 2010, 2022)
        bal = w.govdef_GDP.dropna(); st['bal_mean'] = float(bal.mean()); st['bal_worst'] = (float(bal.min()), int(bal.idxmin()))
        st['fiscal_from'] = int(bal.index.min()); st['bal_best'] = (float(bal.max()), int(bal.idxmax()))
        st['spend_first'] = (float(w.govexp_GDP.dropna().iloc[0]), int(w.govexp_GDP.dropna().index[0])); st['spend_2022'] = nz(float(d.govexp_GDP.get(2022, np.nan)))
        st['spend_peak'] = (float(w.govexp_GDP.max()), int(w.govexp_GDP.idxmax()))
        st['bal_surplus_years'] = int((bal > 0).sum())
        xb = w[['cycle', 'govdef_GDP']].dropna(); st['bal_cyc'] = float(np.corrcoef(xb.cycle, xb.govdef_GDP)[0, 1])
        db = w.govdebt_GDP.dropna(); st['debt_start'] = (float(db.iloc[0]), int(db.index[0])); st['debt_2022'] = float(db.loc[2022]) if 2022 in db.index else None
        st['debt_low'] = (float(db.min()), int(db.idxmin()))
        st['debt_peak'] = (float(db.max()), int(db.idxmax()))
        # rates, inflation, money
        inf = w.infl.dropna(); st['infl_mean'] = float(inf.mean()); st['infl_peak'] = (float(inf.max()), int(inf.idxmax()))
        st['infl_median'] = float(inf.median())
        sr = w.strate.dropna(); st['strate_start'] = int(sr.index.min()) if len(sr) else None
        RR_FROM = {'BRA': 1995}       # before the 1994 Real Plan, nominal-minus-inflation is meaningless under hyperinflation
        rr = w.real_strate.loc[RR_FROM.get(iso, 1970):].dropna(); st['rr_mean'] = float(rr.mean()) if len(rr) else None; st['rr_from'] = RR_FROM.get(iso)
        st['rr_neg_years'] = int((rr < 0).sum()) if len(rr) else None
        z = sr[sr <= 0.5]; st['zlb_years'] = int(len(z)); st['zlb_first'] = int(z.index.min()) if len(z) else None
        st['neg_rate_years'] = int((sr < 0).sum())
        st['strate_peak'] = (float(sr.max()), int(sr.idxmax())) if len(sr) else None
        lr = w.ltrate.dropna(); st['ltrate_start'] = int(lr.index.min()) if len(lr) else None
        mg = w.real_money_growth.dropna(); st['rmoney_mean'] = float(mg.mean()) if len(mg) else None
        st['rmoney_sd'] = float(mg.std()) if len(mg) else None
        st['money_end'] = int(mg.index.max()) if len(mg) else None
        src = w.money_src.dropna()
        sw = src[src != 'M2']; st['money_note'] = ('M2' if not len(sw) else f"M2 to {int(sw.index.min())-1}, then {sw.iloc[0]}")
        if st['money_end'] is not None and st['money_end'] < 2022: st['money_note'] += f" (series ends {st['money_end']})"
        xm = w[['cycle', 'real_money_growth']].dropna(); st['money_cyc'] = float(np.corrcoef(xm.cycle, xm.real_money_growth)[0, 1]) if len(xm) > 10 else None
        # external
        op = (w.exports_GDP+w.imports_GDP).dropna(); st['open_1970'] = float(op.iloc[0]); st['open_2022'] = float(op.loc[2022]); st['open_from'] = int(op.index[0])
        ca = w.CA_GDP.dropna(); st['ca_mean'] = float(ca.mean()); st['ca_min'] = (float(ca.min()), int(ca.idxmin())); st['ca_max'] = (float(ca.max()), int(ca.idxmax()))
        st['ca_start'] = int(ca.index.min())
        re = w.REER.dropna(); st['reer_change'] = float(100*(re.loc[2022]/re.iloc[0]-1)) if len(re) else None
        # labour
        u = w.unemp.dropna(); st['unemp_mean'] = float(u.mean()) if len(u) else None; st['unemp_peak'] = (float(u.max()), int(u.idxmax())) if len(u) else None
        st['unemp_start'] = int(u.index.min()) if len(u) else None
        # crises
        st['crisis_covered'] = bool(w.BankingCrisis.notna().any())
        st['cycle_from'] = int(d.cycle.first_valid_index()); st['growth_from'] = int(g.index.min())
        for k, c in [('bank', 'BankingCrisis'), ('curr', 'CurrencyCrisis'), ('sov', 'SovDebtCrisis')]:
            st['crisis_'+k] = [int(y) for y in w.index[w[c] == 1]]
        # extra series stats for text
        inv = w.inv_GDP.dropna(); st['inv_peak'] = (float(inv.max()), int(inv.idxmax())); st['inv_2022'] = float(inv.loc[2022])
        st['fixes'] = FIX[iso]
        S[iso] = st
    json.dump(S, open(os.path.join(out_dir, 'stats.json'), 'w'), indent=1, default=float)
    if verbose:
        for iso in ['USA', 'JPN', 'GRC', 'IND']:
            s = S[iso]; print(iso, f"g {s['growth_mean']:.2f}±{s['growth_sd']:.2f} worst {s['worst']} | anat", {k: round(v, 2) for k, v in s['anat'].items()},
              f"| coup {s['coup_7089']:+.2f}->{s['coup_9022']:+.2f} | bal_cyc {s['bal_cyc']:+.2f} debt {s['debt_start']}->{s['debt_2022']} | zlb {s['zlb_years']} from {s['zlb_first']} | money {s['money_note']} | crises {s['crisis_bank']}")
    return S


def build_sync(out_dir, verbose=True):
    """sync.py: channel synchronization r(t) across the 26 on the repaired panel.

    Band-pass 2-9y on each economy's series (1950-2022 run-in, needs coverage from 1965), Hilbert phase,
    Kuramoto r(t) = |mean exp(i*theta)|, 1970-2022. Lead-lag vs the five global recessions with circular-shift
    permutation (floor 1/53). Channels: real GDP (patched), real investment (deflator chosen per economy in
    build_panel), short-term interest rate (level)."""
    P = pd.read_csv(os.path.join(out_dir, 'panel.csv')); META = json.load(open(os.path.join(out_dir, 'meta.json')))
    FIX = META['fixes']; ISOS_ = [o[0] for o in META['order']]
    G = pd.read_stata(_gmd(), columns=['ISO3', 'year', 'inv', 'CPI']); G['year'] = G.year.astype(int)
    b, a = butter(2, [(1/9)/0.5, 0.49/0.5], btype='band'); YEARS = np.arange(1970, 2023); T = len(YEARS)
    Gv = np.isin(YEARS, GL).astype(float)

    def series(iso, ch):
        d = P[P.iso == iso].set_index('year')
        if ch == 'GDP': s = np.log(d.rGDP)
        elif ch == 'inv':
            g = G[G.ISO3 == iso].set_index('year').reindex(d.index)
            s = np.log(g.inv/(g.CPI if FIX[iso]['contrib_method'] == 'cpi' else d.deflator))
        elif ch == 'strate': s = d.strate
        return s.replace([np.inf, -np.inf], np.nan)

    def cycle(s):
        s = s.loc[1950:2022]; s = s.loc[s.first_valid_index():].interpolate(limit=2)
        if s.index.min() > 1965 or s.loc[1965:2022].isna().any(): return None
        s = s.dropna(); return pd.Series(filtfilt(b, a, s.values-s.values.mean()), index=s.index)

    def lagcorr(x, lag, g):
        u, v = (x[:-lag], g[lag:]) if lag > 0 else ((x[-lag:], g[:lag]) if lag < 0 else (x, g)); return pearsonr(u, v)[0]
    out = {'years': YEARS.tolist(), 'r_t': {}, 'tests': {}, 'n': {}}
    for ch in ['GDP', 'inv', 'strate']:
        cyc = {i: cycle(series(i, ch)) for i in ISOS_}; cyc = {k: v for k, v in cyc.items() if v is not None}
        PH = np.array([np.angle(hilbert(c.values))[np.isin(c.index, YEARS)] for c in cyc.values()])
        r = np.abs(np.exp(1j*PH).mean(0)); out['r_t'][ch] = r.tolist(); out['n'][ch] = len(cyc)
        t = {}
        for lab, lag, dn in [('lead2', 2, 1), ('lead1', 1, 1), ('same', 0, 1), ('after2', -2, -1)]:
            o = lagcorr(r, lag, Gv); nl = np.array([lagcorr(r, lag, np.roll(Gv, k)) for k in range(1, T)])
            t[lab] = [round(float(o), 3), round(float((1+np.sum(dn*nl >= dn*o))/T), 3)]
        out['tests'][ch] = t
    json.dump(out, open(os.path.join(out_dir, 'sync.json'), 'w'), indent=1)
    if verbose:
        for ch in out['tests']: print(ch, 'n=', out['n'][ch], out['tests'][ch])
    return out
