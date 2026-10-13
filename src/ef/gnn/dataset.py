"""G0: the yearly heterogeneous graph dataset on S31, 1970-2022 (gnn/README.md; HANDOFF.md section 7).

    python -m ef.gnn.dataset          # -> build/gnn/g0/ and the reports gnn/G0_missing_data.md, gnn/G0/*.csv

Nodes: the 31 economies of S31 plus one world node (WLD). Node features per year: phases built from past data only
(convention C) and the repaired atlas panel with Russia (build/data/atlas_s31). Edges, one type each, no correlation
edges (Sid, 11 October 2026):
  trade  i -> j   goods exports of i to j (IMF IMTS, imf_imts_s31): i's reported exports and j's mirror imports,
                  kept as two separate attributes, neither filled from the other
  bank   l -> b   cross-border claims of banks in l on b, year-end (Q4) stock (BIS LBS, bis_lbs); the fixed 10 lenders
                  reporting since 1977; Russia is a borrower only
  oil    i -> WLD one link per economy to the world node, weighted by net oil exports as a share of GDP (Our World
                  in Data energy, owid_energy; production 2017-22 from the EIA (eia_intl) where the two agree within
                  the tolerance fixed beforehand; five documented non-producers; valued at the pinned crude price)
Edge weights (fixed by Sid on 13 October 2026, before any training): primary = the flow as a share of the receiving
economy's nominal GDP (World Bank current US dollars, the WDI vintage of 8 October 2026 since 14 October); sensitivity = the flow as a share of the exporter's or lender's
total. Raw US dollars are stored (raw_* columns) for checking only and are never model inputs (model_inputs()).
Missing values are masked, never filled. Every gap gets a class (GAP_CLASSES) saying whether it is a true zero or
missing data, and why.
"""
import argparse
import hashlib
import json
import os

import numpy as np
import pandas as pd
import yaml

from ef import config
from ef.data import gmd, maddison
from ef.phases import analytic

YEARS = np.arange(1970, 2023)
WORLD = 'WLD'
LENDERS10 = ['FR', 'BE', 'SE', 'CH', 'DE', 'DK', 'NL', 'US', 'GB', 'JP']      # BIS reporters since 1977-Q4 (Sid)
BIS2 = {'USA': 'US', 'GBR': 'GB', 'DEU': 'DE', 'FRA': 'FR', 'ITA': 'IT', 'JPN': 'JP', 'CAN': 'CA', 'ESP': 'ES', 'AUS': 'AU',
        'KOR': 'KR', 'IND': 'IN', 'MEX': 'MX', 'NLD': 'NL', 'SWE': 'SE', 'CHE': 'CH', 'BEL': 'BE', 'ZAF': 'ZA', 'TUR': 'TR',
        'NOR': 'NO', 'AUT': 'AT', 'DNK': 'DK', 'FIN': 'FI', 'GRC': 'GR', 'PRT': 'PT', 'IDN': 'ID', 'THA': 'TH', 'CHN': 'CN',
        'BRA': 'BR', 'SAU': 'SA', 'IRN': 'IR', 'RUS': 'RU'}
# IMF reporting units before a country's own code starts (decided 11 October 2026, docs/data_edges.md): kept as a
# flagged proxy, not a fill
IMF_PROXY = {'BEL': ('TX126', 1996), 'ZAF': ('TX198', 1997)}       # (code, last year it stands in for the country)
SOURCES_USED = ['maddison', 'gmd', 'pwt', 'oil_bp', 'oil_brent', 'owid_energy', 'eia_intl', 'wb_gdp_current_usd',
                'wb_wdi_gdp_2026_10', 'imf_imts_s31', 'bis_lbs']
# Energy Institute conversion factors: 1 tonne of oil equivalent = 11.63 MWh = 7.33 barrels, so 1 TWh = 630,267 barrels
BBL_PER_TWH = 1e6 / 11.63 * 7.33
OIL_PRICE_SWITCH = 1987          # EIA Brent (oil_brent) from this year; the BP series (oil_bp) before it
RUSSIA_OIL_FROM = 1985           # the Energy Institute reports Russia from 1985, the USSR before
# EIA production where Our World in Data's ends in 2016 (Sid, 13 October 2026). Tolerance fixed in docs/decisions.md
# before the comparison was run: d_t = |EIA_t - OWID_t| / max(OWID_t, 10 TWh); agree if the median d_t over 1980-2016
# is at most 0.10 and d_t <= 0.10 in every year 2012-2016. EIA production = crude oil including lease condensate (57)
# + natural gas plant liquids (58), thousand barrels a day, converted with BBL_PER_TWH.
EIA_SERIES = (57, 58)
EIA_TOL, EIA_FLOOR_TWH, EIA_COMPARE, EIA_SPLICE, EIA_EXTEND = 0.10, 10.0, (1980, 2016), (2012, 2016), (2017, 2022)
# Documented non-producers (Sid, 13 October 2026): production is a true zero in every year
TRUE_ZERO_PRODUCERS = ('KOR', 'CHE', 'BEL', 'FIN', 'PRT')

ATLAS_FEATURES = [  # panel column, description
    ('growth', 'real GDP growth, %'), ('c_C', 'consumption contribution to growth, pp'),
    ('c_I', 'investment contribution, pp'), ('c_NX', 'net-export contribution, pp'),
    ('govexp_GDP', 'government spending, % of GDP'), ('govdef_GDP', 'budget balance, % of GDP'),
    ('govdebt_GDP', 'government debt, % of GDP'), ('infl', 'inflation, %'), ('strate', 'short-term interest rate, %'),
    ('ltrate', 'long-term interest rate, %'), ('real_money_growth', 'real money growth, log points x 100'),
    ('exports_GDP', 'exports, % of GDP'), ('imports_GDP', 'imports, % of GDP'), ('CA_GDP', 'current account, % of GDP'),
    ('unemp', 'unemployment rate, %')]
PHASE_FEATURES = [('phase_sin', 'sin of the past-only phase'), ('phase_cos', 'cos of the past-only phase'),
                  ('log_amplitude', 'log of the past-only cycle amplitude (swing size)'),
                  ('row_phase_sin', 'sin of the rest-of-world past-only mean phase'),
                  ('row_phase_cos', 'cos of the rest-of-world past-only mean phase')]
WORLD_FEATURES = [('r_past', 'order parameter r(t) of the 31 past-only phases'),
                  ('world_phase_sin', 'sin of the world mean past-only phase'), ('world_phase_cos', 'cos of it'),
                  ('us_strate', 'US short-term interest rate, %'), ('us_real_strate', 'US real short rate, %'),
                  ('oil_real_2015usd', 'real crude oil price, 2015 US dollars'),
                  ('world_growth', 'world growth, % (GDP-weighted over the 26 of the atlas, not the 31)')]

GAP_CLASSES = {  # code: (true zero or missing, meaning)
    'observed': ('observed', 'value present'),
    'not_yet': ('missing', 'the series starts later (for bank claims on Russia: from 1993-Q4; the BIS reports claims on the '
                'USSR, code SU, before that, not used)'),
    'ended': ('missing', 'the series stops earlier'),
    'internal': ('missing', 'a gap inside the series in the source'),
    'absent': ('missing', 'the source has no value for this economy in any year'),
    'repair': ('missing', 'removed by an atlas repair (meta.json fixes)'),
    'entity': ('missing', 'Russia did not report as Russia yet: the USSR reported instead (trade before 1992, oil before '
               '1985); the USSR figures are not used for Russia'),
    'not_reporting': ('missing', 'neither side reported any trade with any partner that year'),
    'unrecorded': ('zero or unrecorded', 'no flow recorded while both sides report other partners that year; the IMF file '
                   'never records zeros, so this cannot be confirmed as a true zero'),
    'before_bis': ('missing', 'before the lender reported to the BIS (from 1977-Q4)'),
    'series_absent': ('missing', 'the lender reports no series for this borrower'),
    'series_gap': ('missing', 'the lender\'s series for this borrower has no year-end value'),
    'zero': ('true zero', 'a reported value of exactly zero'),
    'no_denominator': ('missing', 'the flow is observed but its denominator is missing (the receiving economy\'s GDP, or '
                       'the sender\'s total)'),
    'other_report_only': ('missing', 'this side\'s report of the flow is missing; the other side\'s report exists and is '
                          'not used to fill it'),
}


# ------------------------------------------------------------------ sources

def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def verify_sources(ids=SOURCES_USED):
    """Every file of the given sources and downloads against its sha256 in data/sources.yaml. Returns
    [(id, file, date or commit, ok)] and raises if any file is missing or changed."""
    y = yaml.safe_load(open(config.load()['paths']['sources'])); raw = config.load()['paths']['raw']; out = []
    for s in y['sources'] + y.get('downloads', []):
        if s['id'] not in ids: continue
        for f in s['files']:
            p = os.path.join(raw, s['dir'], f['path'])
            ok = os.path.exists(p) and _sha(p) == f['sha256']
            out.append((s['id'], f['path'], str(s.get('commit', s.get('downloaded', '')))[:10], ok))
    bad = [r for r in out if not r[3]]
    if bad: raise SystemExit("sources missing or changed (run make fetch): " + ", ".join(f"{a}:{b}" for a, b, _, _ in bad))
    return out


# ------------------------------------------------------------------ nodes

def _classify_series(v, years, repair_years=()):
    """Gap class per year for one series (NaN = missing)."""
    ok = ~np.isnan(v); cls = np.where(ok, 'observed', '').astype(object)
    if not ok.any(): return np.full(len(v), 'absent', dtype=object)
    first, last = np.flatnonzero(ok)[[0, -1]]
    for k in np.flatnonzero(~ok):
        cls[k] = 'repair' if int(years[k]) in repair_years else ('not_yet' if k < first else 'ended' if k > last else 'internal')
    return cls


def _repair_years(fx, col):
    """Years an atlas repair removed for a panel column (meta.json 'fixes')."""
    ys = set()
    comp = ('c_C', 'c_I', 'c_NX', 'exports_GDP', 'imports_GDP')
    if col in comp and 'components_from' in fx: ys |= set(range(1950, fx['components_from']))
    if col in ('c_C', 'c_I', 'c_NX'):
        if 'contrib_from' in fx: ys |= set(range(1950, fx['contrib_from']))
        ys |= set(fx.get('contrib_blank', []))
    if col in ('growth', 'c_C', 'c_I', 'c_NX') and 'gdp_from' in fx: ys |= set(range(1950, fx['gdp_from'] + 1))
    if col == 'infl' and 'infl_from' in fx: ys |= set(range(1950, fx['infl_from']))
    if col == 'real_money_growth': ys |= set(fx.get('money_dropped', []))
    if col == 'ltrate': ys |= set(fx.get('ltrate_dropped', []))
    return ys


def past_only_phases(isos):
    """Convention C: band-pass and Hilbert transform on Maddison data up to each year (ef.phases.analytic)."""
    L = maddison.panel(isos); logs = np.log(maddison.wide(L, 'gdppc').values.T); yrs = maddison.wide(L).index.to_numpy()
    z = analytic(logs, yrs, (1970, 2022), 'C')
    return z


def nodes(atlas_dir, isos):
    """Node feature arrays X (years x nodes x features), mask (True = observed) and gap classes, economies then WLD."""
    P = pd.read_csv(os.path.join(atlas_dir, 'panel.csv')); meta = json.load(open(os.path.join(atlas_dir, 'meta.json')))
    G = pd.read_csv(os.path.join(atlas_dir, 'global.csv')).set_index('year')
    z = past_only_phases(isos); th = np.angle(z); u = np.exp(1j * th); N = len(isos); T = len(YEARS)
    efeat = [f for f, _ in PHASE_FEATURES] + [f for f, _ in ATLAS_FEATURES]
    X = np.full((T, N + 1, len(efeat) + len(WORLD_FEATURES)), np.nan); C = np.full(X.shape, '', dtype=object)
    for i, iso in enumerate(isos):
        row = (u.sum(0) - u[i]) / (N - 1)
        vals = {'phase_sin': np.sin(th[i]), 'phase_cos': np.cos(th[i]), 'log_amplitude': np.log(np.abs(z[i])),
                'row_phase_sin': np.sin(np.angle(row)), 'row_phase_cos': np.cos(np.angle(row))}
        d = P[P.iso == iso].set_index('year').reindex(YEARS)
        for k, f in enumerate(efeat):
            v = vals[f] if f in vals else d[f].to_numpy(float)
            X[:, i, k] = v; C[:, i, k] = _classify_series(v, YEARS, _repair_years(meta['fixes'].get(iso, {}), f))
    m = u.mean(0); us = P[P.iso == 'USA'].set_index('year').reindex(YEARS)
    w = {'r_past': np.abs(m), 'world_phase_sin': np.sin(np.angle(m)), 'world_phase_cos': np.cos(np.angle(m)),
         'us_strate': us.strate.to_numpy(float), 'us_real_strate': us.real_strate.to_numpy(float),
         'oil_real_2015usd': G.oil_real_2015usd.reindex(YEARS).to_numpy(float), 'world_growth': G.world_growth.reindex(YEARS).to_numpy(float)}
    for k, (f, _) in enumerate(WORLD_FEATURES):
        X[:, N, len(efeat) + k] = w[f]; C[:, N, len(efeat) + k] = _classify_series(w[f], YEARS)
    C[:, :N, len(efeat):] = 'not_a_feature'; C[:, N, :len(efeat)] = 'not_a_feature'
    return X, ~np.isnan(X), C, efeat + [f for f, _ in WORLD_FEATURES]


# ------------------------------------------------------------------ denominators and prices

GDP_SOURCE = ('wb_wdi_gdp_2026_10', 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv')   # Sid, 14 October 2026 (option b)


def gdp_usd(isos):
    """Nominal GDP in current US dollars (World Bank NY.GDP.MKTP.CD), years x economies; NaN = missing. The
    denominator of the primary edge weights and of the oil share. Since 14 October 2026 (Sid, option b) every
    denominator comes from the fresh WDI vintage (wb_wdi_gdp_2026_10, WDI of 8 October 2026); the earlier pinned file
    (wb_gdp_current_usd) is kept for the vintage comparison only."""
    N = pd.read_csv(config.raw_file(*GDP_SOURCE), skiprows=4, float_precision='round_trip')
    N = N[N['Country Code'].isin(isos)].set_index('Country Code')[[str(y) for y in YEARS]].T
    N.index = YEARS
    return N.reindex(columns=isos).astype(float)


def oil_price_nominal():
    """Crude oil price in US dollars of each year, per barrel, and its source. EIA Brent (oil_brent) from 1987, the first
    year it covers. Before 1987 no Brent series is pinned: the BP series (oil_bp: Arabian Light posted at Ras Tanura to
    1983, Brent dated 1984-86, in 2015 dollars) is converted back to dollars of the day with the US consumer price index
    (Global Macro Database). Returns (price, source, check), check = mean |BP converted / EIA - 1| over 1987-2015."""
    br = pd.read_csv(config.raw_file('oil_brent')); br.index = br.Date.str[:4].astype(int); br = br.Price
    bp = pd.read_csv(config.raw_file('oil_bp')); bp = bp[bp.Entity == 'World'].set_index('Year')['Crude oil price (BP Statistics (2016))']
    G = gmd.read(config.raw_file('gmd', 'data/final/data_final.dta'), columns=['ISO3', 'year', 'CPI'])
    cpi = G[G.ISO3 == 'USA'].assign(year=lambda d: d.year.astype(int)).set_index('year').CPI
    bp_nominal = bp * cpi.reindex(bp.index) / cpi[2015]
    price = pd.Series([br[y] if y >= OIL_PRICE_SWITCH else bp_nominal[y] for y in YEARS], index=YEARS)
    source = pd.Series(['eia_brent' if y >= OIL_PRICE_SWITCH else 'bp_deflated' for y in YEARS], index=YEARS)
    o = range(OIL_PRICE_SWITCH, 2016)
    return price, source, float(np.mean([abs(bp_nominal[y] / br[y] - 1) for y in o]))


def _wgap(value, pair_gap, denom):
    """Gap class of one normalised weight: the flow's own class, or why the weight is missing although the pair is not."""
    if not np.isnan(value): return 'observed' if not np.isnan(denom) else 'no_denominator'
    return 'other_report_only' if pair_gap == 'observed' else pair_gap


# ------------------------------------------------------------------ edges

def trade_edges(isos, gdp):
    """Directed i -> j goods trade for every ordered pair of S31 economies and year: i's reported exports to j (FOB) and
    j's reported imports from i (CIF, mirror), each with its own mask and gap class, neither filled from the other.
    Weights: primary, the flow as a share of the importer's (the receiving economy's) GDP; sensitivity, as a share of
    the exporter's total goods exports to the world (as the exporter reports it)."""
    t = pd.read_csv(config.raw_file('imf_imts_s31', 'IMTS_S31_annual.csv'), low_memory=False)
    t = t[t.TIME_PERIOD.between(1970, 2022)]

    def code(iso, y):
        p = IMF_PROXY.get(iso); return p[0] if p and y <= p[1] else iso
    xs = t[t.INDICATOR == 'XG_FOB_USD'].set_index(['COUNTRY', 'COUNTERPART_COUNTRY', 'TIME_PERIOD'])
    ms = t[t.INDICATOR == 'MG_CIF_USD'].set_index(['COUNTRY', 'COUNTERPART_COUNTRY', 'TIME_PERIOD'])
    xv, xe = xs.OBS_VALUE.to_dict(), (xs.STATUS == 'e').to_dict()
    mv, me = ms.OBS_VALUE.to_dict(), (ms.STATUS == 'e').to_dict()
    wx = t[(t.INDICATOR == 'XG_FOB_USD') & (t.COUNTERPART_COUNTRY == 'G001')].set_index(['COUNTRY', 'TIME_PERIOD']).OBS_VALUE.to_dict()
    rep_x = t[t.INDICATOR == 'XG_FOB_USD'].groupby('TIME_PERIOD').COUNTRY.apply(set).to_dict()     # reporters with any exports
    rep_m = t[t.INDICATOR == 'MG_CIF_USD'].groupby('TIME_PERIOD').COUNTRY.apply(set).to_dict()
    rows = []
    for y in YEARS:
        y = int(y)
        for i in isos:
            for j in isos:
                if i == j: continue
                ci, cj = code(i, y), code(j, y)
                ex = xv.get((ci, cj, y), np.nan); im = mv.get((cj, ci, y), np.nan)       # OBS_VALUE is in US dollars
                tot = wx.get((ci, y), np.nan); g_j = gdp.at[y, j]
                if not (np.isnan(ex) and np.isnan(im)): cls = 'observed'
                elif (i == 'RUS' or j == 'RUS') and y < 1992: cls = 'entity'
                elif ci in rep_x.get(y, set()) and cj in rep_m.get(y, set()): cls = 'unrecorded'
                else: cls = 'not_reporting'
                rows.append((y, i, j, ex, im, ex / g_j, im / g_j, ex / tot, im / tot,
                             _wgap(ex, cls, g_j), _wgap(im, cls, g_j), _wgap(ex, cls, tot), _wgap(im, cls, tot),
                             bool(xe.get((ci, cj, y), False)), bool(me.get((cj, ci, y), False)), ci != i or cj != j, cls))
    return pd.DataFrame(rows, columns=['year', 'src', 'dst', 'raw_exports_fob_usd', 'raw_mirror_imports_cif_usd',
                                       'w_exports_share_dst_gdp', 'w_mirror_share_dst_gdp',
                                       's_exports_share_src_total', 's_mirror_share_src_total',
                                       'gap_w_exports', 'gap_w_mirror', 'gap_s_exports', 'gap_s_mirror',
                                       'exports_imf_estimate', 'mirror_imf_estimate', 'proxy_reporting_unit', 'gap'])


def bank_edges(isos, gdp):
    """Directed lender -> borrower year-end (Q4) cross-border claims on all sectors, for the fixed 10 lenders and every
    other S31 economy (sources.yaml read_with filters; values in millions of US dollars). Russia is never a lender.
    Bilateral claims are published for all sectors and for non-banks only, so a banks-only attribute would have to be
    derived as a difference; it is not built. Weights: primary, the claims as a share of the borrower's (the receiving
    economy's) GDP; sensitivity, as a share of the lender's cross-border claims on all countries."""
    lend = [i for i in isos if BIS2.get(i) in LENDERS10]
    want = {BIS2[i] for i in isos} | {'5J'}                                                       # 5J: all countries
    d = pd.read_csv(config.raw_file('bis_lbs', 'WS_LBS_D_PUB_csv_col.csv'), dtype=str, low_memory=False)
    base = ((d.FREQ == 'Q') & (d.L_MEASURE == 'S') & (d.L_POSITION == 'C') & (d.L_INSTR == 'A') & (d.L_DENOM == 'TO1') &
            (d.L_CURR_TYPE == 'A') & (d.L_PARENT_CTY == '5J') & (d.L_REP_BANK_TYPE == 'A') & (d.L_POS_TYPE == 'N') &
            d.L_REP_CTY.isin(LENDERS10) & d.L_CP_COUNTRY.isin(want))
    q4 = [f'{y}-Q4' for y in YEARS]; cols = [c for c in q4 if c in d.columns]
    ser = {'A': d[base & (d.L_CP_SECTOR == 'A')].set_index(['L_REP_CTY', 'L_CP_COUNTRY'])[cols].apply(pd.to_numeric, errors='coerce')}
    first = {k: int(r.first_valid_index()[:4]) for k, r in ser['A'].iterrows() if r.first_valid_index() is not None}

    def val(sector, key, col):
        s = ser[sector]; return s.loc[key, col] * 1e6 if key in s.index and col in s.columns else np.nan
    rows = []
    for y in YEARS:
        y = int(y); col = f'{y}-Q4'
        for l in lend:
            for b in isos:
                if b == l: continue
                key = (BIS2[l], BIS2[b]); a = val('A', key, col); ta = val('A', (BIS2[l], '5J'), col); g_b = gdp.at[y, b]
                if y < 1977: cls = 'before_bis'
                elif key not in ser['A'].index: cls = 'series_absent'
                elif np.isnan(a): cls = 'not_yet' if key in first and y < first[key] else 'series_gap'
                elif a == 0: cls = 'zero'
                else: cls = 'observed'
                pair = 'observed' if cls == 'zero' else cls
                rows.append((y, l, b, a, ta, a / g_b, a / ta, _wgap(a, pair, g_b), _wgap(a, pair, ta), cls))
    return pd.DataFrame(rows, columns=['year', 'src', 'dst', 'raw_claims_usd', 'raw_lender_claims_all_countries_usd',
                                       'w_claims_share_dst_gdp', 's_claims_share_src_total',
                                       'gap_w_claims', 'gap_s_claims', 'gap'])


def eia_production_twh(isos):
    """EIA crude oil including lease condensate + natural gas plant liquids, in TWh (thousand barrels a day x 1,000 x
    days in the year / BBL_PER_TWH), years 1970-2022 x economies. NaN where either series is missing ('--' or not
    listed), so a year with crude but no NGL figure is missing, not crude only."""
    import calendar
    want = {f'INTL.{c}-1-{i}-TBPD.A': (c, i) for c in EIA_SERIES for i in isos}; S = {}
    for line in open(config.raw_file('eia_intl', 'INTL.txt')):
        if not line.startswith('{"series_id"'): continue
        d = json.loads(line)
        if d['series_id'] in want: S[want[d['series_id']]] = {int(y): v for y, v in d['data']}
    out = pd.DataFrame(np.nan, index=YEARS, columns=isos)
    for i in isos:
        for y in YEARS:
            v = [S.get((c, i), {}).get(int(y)) for c in EIA_SERIES]
            if all(isinstance(x, (int, float)) for x in v):
                out.at[y, i] = sum(v) * 1000 * (366 if calendar.isleap(int(y)) else 365) / BBL_PER_TWH
    return out


def owid_oil(isos):
    """Our World in Data oil production and consumption (TWh), years x economies each."""
    O = pd.read_csv(config.raw_file('owid_energy', 'owid-energy-data.csv'), usecols=['year', 'iso_code', 'oil_production', 'oil_consumption'])
    O = O[O.iso_code.isin(isos)]
    return tuple(O.pivot(index='year', columns='iso_code', values=c).reindex(index=YEARS, columns=isos).astype(float)
                 for c in ('oil_production', 'oil_consumption'))


def eia_comparison(isos):
    """EIA against OWID production for every economy whose OWID production ends before 2022, by the tolerance fixed
    beforehand (EIA_TOL). Returns (summary per economy, d_t per economy and year)."""
    prod, _ = owid_oil(isos); eia = eia_production_twh(isos); rows, long = [], []
    for i in isos:
        p = prod[i]
        if p.notna().any() and p.last_valid_index() >= EIA_EXTEND[1]: continue
        both = p.notna() & eia[i].notna() & (YEARS >= EIA_COMPARE[0]) & (YEARS <= EIA_COMPARE[1])
        d = (eia[i] - p).abs() / np.maximum(p, EIA_FLOOR_TWH)
        ys = YEARS[both.to_numpy()]; dd = d[both]
        spl = [y for y in range(EIA_SPLICE[0], EIA_SPLICE[1] + 1)]
        spl_ok = all(bool(both.get(y, False)) and d[y] <= EIA_TOL for y in spl)
        med = float(dd.median()) if len(dd) else np.nan
        ratio = float((eia[i][both] / p[both]).median()) if (p[both] > 0).all() and len(dd) else np.nan
        ext = [y for y in range(EIA_EXTEND[0], EIA_EXTEND[1] + 1) if not np.isnan(eia.at[y, i])]
        rows.append(dict(iso=i, owid_last=int(p.last_valid_index()) if p.notna().any() else None, years_compared=len(ys),
                         first=int(ys.min()) if len(ys) else None, median_d=med,
                         max_d_splice=float(d[spl].max()) if all(bool(both.get(y, False)) for y in spl) else np.nan,
                         splice_ok=spl_ok, agree=bool(len(dd) and med <= EIA_TOL and spl_ok),
                         median_ratio_eia_owid=ratio, eia_years_2017_2022=len(ext), true_zero=i in TRUE_ZERO_PRODUCERS,
                         eia_max_twh=float(eia[i].max()) if eia[i].notna().any() else np.nan,
                         eia_listed=f"{int(eia[i].first_valid_index())}-{int(eia[i].last_valid_index())}" if eia[i].notna().any() else ''))
        long += [(i, int(y), float(p[y]), float(eia.at[y, i]), float(d[y])) for y in ys]
    return pd.DataFrame(rows), pd.DataFrame(long, columns=['iso', 'year', 'owid_twh', 'eia_twh', 'd'])


def oil_production(isos):
    """Production used for the oil weights (TWh, years x economies) and its source per cell: 'owid'; 'eia' (2017-2022,
    economies where EIA and OWID agree); 'true_zero' (the documented non-producers, in the years OWID does not list);
    '' where masked."""
    prod, _ = owid_oil(isos); eia = eia_production_twh(isos); summ, _ = eia_comparison(isos)
    agree = set(summ[summ.agree & ~summ.true_zero].iso)
    P = prod.copy(); src = pd.DataFrame(np.where(prod.notna(), 'owid', ''), index=YEARS, columns=isos)
    for i in isos:
        for y in YEARS:
            if not np.isnan(P.at[y, i]): continue
            if i in TRUE_ZERO_PRODUCERS: P.at[y, i] = 0.0; src.at[y, i] = 'true_zero'
            elif i in agree and EIA_EXTEND[0] <= y <= EIA_EXTEND[1] and not np.isnan(eia.at[y, i]):
                P.at[y, i] = eia.at[y, i]; src.at[y, i] = 'eia'
    return P, src


def wb_vintage_comparison(isos):
    """The fresh World Bank download (wb_wdi_gdp_2026_10) against the pinned denominator file, economy-years 1970-2022:
    old value, new value and the relative difference (NaN where either is missing)."""
    f = config.raw_file('wb_wdi_gdp_2026_10', 'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_512.csv')
    N = pd.read_csv(f, skiprows=4, float_precision='round_trip'); N = N[N['Country Code'].isin(isos)].set_index('Country Code')
    N = N[[str(y) for y in YEARS]].T; N.index = YEARS; N = N.reindex(columns=isos).astype(float)
    W = pd.read_csv(config.raw_file('wb_gdp_current_usd', 'data/gdp.csv'), float_precision='round_trip')
    W = W[W['Country Code'].isin(isos)].pivot(index='Year', columns='Country Code', values='Value').reindex(index=YEARS, columns=isos).astype(float)
    L = W.rename_axis('year').reset_index().melt(id_vars='year', var_name='iso', value_name='old')
    L['new'] = N.rename_axis('year').reset_index().melt(id_vars='year', var_name='iso', value_name='new')['new'].to_numpy()
    L['rel'] = L.new / L.old - 1
    return L


def oil_edges(isos, gdp):
    """One i -> WLD link per economy and year, weighted by net oil exports as a share of the economy's nominal GDP:
    (oil production - primary energy consumption from oil, TWh; owid_energy) x 630,267 barrels per TWh (Energy Institute
    factors) x the crude price in dollars of the year (oil_price_nominal) / GDP in current US dollars (World Bank).
    Positive for net exporters, negative for net importers."""
    P, psrc_prod = oil_production(isos); _, Cn = owid_oil(isos)
    price, psrc, _ = oil_price_nominal(); rows = []
    for i in isos:
        prod, cons = P[i].to_numpy(float), Cn[i].to_numpy(float)
        cp, cc = _classify_series(prod, YEARS), _classify_series(cons, YEARS)
        for k, y in enumerate(YEARS):
            y = int(y); g_i = gdp.at[y, i]; ps = psrc_prod.at[y, i]
            net = prod[k] - cons[k]; value = net * BBL_PER_TWH * price[y]
            if np.isnan(net):
                if i == 'RUS' and y < RUSSIA_OIL_FROM: cls = 'entity'
                else: cls = cp[k] if np.isnan(prod[k]) else cc[k]
            else: cls = 'observed' if not np.isnan(g_i) else 'no_denominator'
            rows.append((y, i, WORLD, prod[k], cons[k], net, value, price[y], psrc[y], ps, value / g_i,
                         ps == 'eia', ps == 'true_zero', psrc[y] == 'bp_deflated', cls))
    return pd.DataFrame(rows, columns=['year', 'src', 'dst', 'raw_oil_production_twh', 'raw_oil_consumption_twh',
                                       'raw_net_oil_twh', 'raw_net_oil_value_usd', 'oil_price_usd_per_bbl', 'oil_price_source',
                                       'oil_production_source', 'w_net_oil_exports_share_gdp',
                                       'production_from_eia', 'production_true_zero', 'price_from_bp_series', 'gap'])


# The edge attributes a model may read (Sid, 13 October 2026): normalised weights only, never raw US dollars
MODEL_INPUTS = {
    'trade': {'primary': ['w_exports_share_dst_gdp', 'w_mirror_share_dst_gdp'],
              'sensitivity': ['s_exports_share_src_total', 's_mirror_share_src_total'],
              'flags': ['exports_imf_estimate', 'mirror_imf_estimate', 'proxy_reporting_unit']},
    'bank': {'primary': ['w_claims_share_dst_gdp'], 'sensitivity': ['s_claims_share_src_total'], 'flags': []},
    'oil': {'primary': ['w_net_oil_exports_share_gdp'], 'sensitivity': ['w_net_oil_exports_share_gdp'],
            'flags': ['production_from_eia', 'production_true_zero', 'price_from_bp_series']},
}


def model_inputs(E, variant='primary'):
    """Edge tables cut to what a model may read: year, endpoints, the weights of the chosen variant ('primary' or
    'sensitivity') with a mask column each (True = observed), and the flags. Raw US dollars (raw_*) never appear."""
    out = {}
    for k, e in E.items():
        cols = MODEL_INPUTS[k][variant]; d = e[['year', 'src', 'dst'] + cols + MODEL_INPUTS[k]['flags']].copy()
        for c in cols: d[f'mask_{c}'] = d[c].notna()
        out[k] = d
    return out


# ------------------------------------------------------------------ build and report

def build(out_dir, atlas_dir, isos=None):
    isos = isos or config.sample('S31'); os.makedirs(out_dir, exist_ok=True)
    src = verify_sources()
    X, M, C, feats = nodes(atlas_dir, isos)
    np.savez_compressed(os.path.join(out_dir, 'nodes.npz'), X=X, mask=M, gap=C.astype(str), years=YEARS,
                        nodes=np.array(isos + [WORLD]), features=np.array(feats))
    gdp = gdp_usd(isos); gdp.to_csv(os.path.join(out_dir, 'gdp_current_usd.csv'))
    E = {'trade': trade_edges(isos, gdp), 'bank': bank_edges(isos, gdp), 'oil': oil_edges(isos, gdp)}
    for k, e in E.items(): e.to_csv(os.path.join(out_dir, f'edges_{k}.csv'), index=False)
    return dict(isos=isos, X=X, M=M, C=C, feats=feats, E=E, sources=src, gdp=gdp)


def load(out_dir):
    """The built dataset: node arrays, the three edge tables (masks are the non-NaN cells; raw_* columns are for
    checking only) and the GDP denominators."""
    n = np.load(os.path.join(out_dir, 'nodes.npz'), allow_pickle=False)
    E = {k: pd.read_csv(os.path.join(out_dir, f'edges_{k}.csv')) for k in ('trade', 'bank', 'oil')}
    return dict(n), E
