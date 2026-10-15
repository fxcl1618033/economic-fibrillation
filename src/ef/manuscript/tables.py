"""The manuscript's tables, each built from results files. A template asks for one with {{table:name}}; every table
returns its markdown and the files it read (logged like any other number)."""
import json
import os

import numpy as np

from ef.manuscript.values import ROOT, _load, fmt

LAGS = ['lead2', 'lead1', 'crisis', 'after1', 'after2']
LAGN = {'lead2': 'Lead-2', 'lead1': 'Lead-1', 'crisis': 'Crisis year', 'after1': 'After-1', 'after2': 'After-2'}
NAME = {'CHN': 'China', 'BRA': 'Brazil', 'SAU': 'Saudi Arabia', 'IRN': 'Iran', 'RUS': 'Russia', 'USA': 'United States', 'GBR': 'United Kingdom',
        'DEU': 'Germany', 'FRA': 'France', 'ITA': 'Italy', 'JPN': 'Japan', 'CAN': 'Canada', 'ESP': 'Spain', 'AUS': 'Australia', 'KOR': 'South Korea',
        'IND': 'India', 'MEX': 'Mexico', 'NLD': 'Netherlands', 'SWE': 'Sweden', 'CHE': 'Switzerland', 'BEL': 'Belgium', 'ZAF': 'South Africa',
        'TUR': 'Turkey', 'NOR': 'Norway', 'AUT': 'Austria', 'DNK': 'Denmark', 'FIN': 'Finland', 'GRC': 'Greece', 'PRT': 'Portugal',
        'IDN': 'Indonesia', 'THA': 'Thailand'}


def _r(sample, test):
    rel = f"results/{sample}/P/{test}.json"
    return (_load(rel)['results'], rel) if os.path.exists(os.path.join(ROOT, rel)) else (None, None)


def cp(c, p, d=3): return f"{fmt(c, f'c{d}')} ({fmt(p, 'p')})"


def table_kappa0():
    """Table 1: the G1 kappa = 0 size check (gnn/G1/rejections.csv)."""
    from ef.gnn import g1_report as T
    rows = _load('gnn/G1/rejections.csv'); src = ['gnn/G1/rejections.csv']
    get = lambda m, rule, t: next(r for r in rows if r['model'] == m and r['cell'] == 'null' and r['rule'] == rule and r['test'] == t)
    L = ["| Test | Correct rate | Kuramoto, real dates | Stuart–Landau, real dates | Kuramoto, own dates | Stuart–Landau, own dates |",
         "|---|---|---|---|---|---|"]
    for t in T.ORDER:
        cells = []
        for m, rule in (('kuramoto', 'A'), ('stuart_landau', 'A'), ('kuramoto', 'B'), ('stuart_landau', 'B')):
            r = get(m, rule, t); s = fmt(float(r['rate']), 'pct1'); cells.append(f"**{s}**" if r['verdict'] == 'over' else s)
        ex = get('kuramoto', 'A', t)['exact']; ex = fmt(float(ex), 'pct1') if ex not in ('', 'nan') else '—'
        L.append(f"| {T.LABELS[t]} | {ex} | " + " | ".join(cells) + " |")
    return "\n".join(L), src


def table_conventions():
    """Table 2 (Methods 7.2): the arc and the synchronization-swing link under each phase convention, S31 with S30's lead-1."""
    c31, s31 = _r('S31', 'conventions'); c30, s30 = _r('S30', 'conventions')
    L = ["| Convention | Lead-2 | Lead-1 | Lag $-2$ | $r$–$\\bar A$, detrended | S30 lead-1 |", "|---|---|---|---|---|---|"]
    for conv in ('P', 'W', 'N', 'E', 'C'):
        a = c31[conv]['arc']; amp = c31[conv]['amp_detrended']; b = c30[conv]['arc']['lead1']
        L.append(f"| {conv} | {cp(a['lead2']['corr'], a['lead2']['p'])} | {cp(a['lead1']['corr'], a['lead1']['p'])} | "
                 f"{cp(a['after2']['corr'], a['after2']['p'])} | {cp(amp[0], amp[1])} | {cp(b['corr'], b['p'])} |")
    return "\n".join(L), [s31, s30]


A1_COLS = [('S26', 'S26'), ('S30', 'S30'), ('S31', 'S31'), ('S31_minus_CHN', 'S31 without China'), ('S31_minus_BRA', 'without Brazil'),
           ('S31_minus_SAU', 'without Saudi Arabia'), ('S31_minus_IRN', 'without Iran'), ('S31_minus_RUS', 'without Russia (= S30)'),
           ('S31_rus_from_1992', 'Russia from 1992'), ('S31_minus_IRN_SAU', 'without Iran and Saudi Arabia')]


def _a1_cell(sample, row):
    src = []
    def R(test):
        r, s = _r(sample, test)
        if s: src.append(s)
        return r
    try:
        if row == 'lead2': a = R('arc'); return cp(a['arc']['lead2']['corr'], a['arc']['lead2']['p']), src
        if row == 'lead1': a = R('arc'); return cp(a['arc']['lead1']['corr'], a['arc']['lead1']['p']), src
        if row == 'past': a = R('conventions'); return cp(a['C']['arc']['lead1']['corr'], a['C']['arc']['lead1']['p']), src
        if row == 'after2': a = R('arc'); return cp(a['arc']['after2']['corr'], a['arc']['after2']['p']), src
        if row == 'amp':
            a = R('amplitude'); s = f"{fmt(a['corr_detrended'], 'c3')} ({fmt(a['p_shift'], 'p')}"
            return s + (f"; surr. {fmt(a['p_surrogate'], 'p')})" if a.get('p_surrogate') is not None else ")"), src
        if row in ('d1', 'd3'): a = R('diversification'); return fmt(a['gdp_mean' if row == 'd1' else 'equal']['cross_fraction_of_excess'], 'pct1'), src
        if row == 'd7':
            a = R('cross_split')['gdp_mean']; return " / ".join(fmt(a[k], 'pct0').rstrip('%') for k in ('from_correlation', 'from_swing_size', 'interaction')) + "%", src
        if row == 'd11': a = R('structure'); return f"{fmt(a['align_share'], 'pct1')} ({fmt(a['p_align'], 'p')})", src
        if row == 'e1':
            m = R('mst')['L_decade_means']; return f"{fmt(m['1979-1989'], 'f3')} vs {fmt(m['2013-2022'], 'f3')} ({fmt(m['1979-1989'] / m['2013-2022'], 'x2')})", src
        if row == 'e7': a = R('phase_lags'); return f"{fmt(a['sd'], 'f3')} yr ({fmt(a['p_spread_lower'], 'p')})", src
        if row == 'f1': a = R('csd'); return cp(a['tau_ar1'], a['p_ar1']), src
        if row == 'f2': a = R('csd'); return cp(a['tau_var'], a['p_var']), src
        if row == 'f4': a = R('bifurcation'); return cp(a['stat_real'], a['p_slowing_post']), src
        if row == 'g1':
            a = R('channels')['sync']['strate']; return f"{cp(a['tests']['lead2'][0], a['tests']['lead2'][1])} [{a['n']}]", src
    except (TypeError, KeyError):
        return '—', src
    raise ValueError(row)


A1_ROWS = [('lead2', 'Arc, lead-2'), ('lead1', 'Arc, lead-1'), ('past', 'Lead-1, past-only phases'), ('after2', 'Arc, after-2 (lower tail)'),
           ('amp', 'r with swing size, detrended'), ('d1', 'Cross share of the recession excess, GDP weights'), ('d3', 'Same, equal weights'),
           ('d7', 'Cross-term rise: correlation / swing size / interaction'), ('d11', 'Alignment share of the swing excess (p)'),
           ('e1', 'MST decade means, 1979–89 vs 2013–22'), ('e7', 'Phase-lead spread (lower-tail p)'), ('f1', 'Autocorrelation trend before recessions'),
           ('f2', 'Variance trend before recessions'), ('f4', 'Recovery-rate change after recessions'), ('g1', 'Short-rate synchronization, lead-2 [economies]')]


def table_A1():
    src = []; L = ["| Quantity | " + " | ".join(n for _, n in A1_COLS) + " |", "|---|" + "---|" * len(A1_COLS)]
    for row, name in A1_ROWS:
        cells = []
        for s, _ in A1_COLS:
            c, sr = _a1_cell(s, row); cells.append(c); src += sr
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(L), sorted(set(src))


ROB = [('band 2-8 yr', 'Band 2–8 years'), ('band 3-10 yr', 'Band 3–10 years'), ('HP filter (lambda=100)', 'HP filter, λ = 100'),
       ('growth rates', 'Growth rates instead of band-pass'), ('1970-1995 (1975,82,91)', '1970–1995 only (1975, 1982, 1991)'),
       ('1996-2022 (2009,2020)', '1996–2022 only (2009, 2020)'), ('without 1975', 'Without 1975'), ('without 1982', 'Without 1982'),
       ('without 1991', 'Without 1991'), ('without 2009', 'Without 2009'), ('without 2020', 'Without 2020'),
       ('without 2009 AND 2020', 'Without 2009 and 2020')]


def table_robust(sample='S31'):
    r, s = _r(sample, 'robustness'); src = [s]; k4 = ['lead2', 'lead1', 'crisis', 'after2']
    L = ["| Check | Lead-2 | Lead-1 | Crisis year | After-2 (lower tail) |", "|---|---|---|---|---|"]
    L.append("| Baseline | " + " | ".join(cp(*r['baseline'][k], d=2) for k in k4) + " |")
    for key, name in ROB: L.append(f"| {name} | " + " | ".join(cp(*r[key][k], d=2) for k in k4) + " |")
    loo = {k: v for k, v in r.items() if k.startswith('without ') and len(k) == 11}
    rng = lambda k: (f"{fmt(min(v[k][0] for v in loo.values()), 'c2')} to {fmt(max(v[k][0] for v in loo.values()), 'c2')} "
                     f"({fmt(min(v[k][1] for v in loo.values()), 'p')}–{fmt(max(v[k][1] for v in loo.values()), 'p')})")
    L.append(f"| Each of the {len(loo)} economies left out (range) | " + " | ".join(rng(k) for k in k4) + " |")
    g, gs = _r(f'{sample}_gmd_growth', 'arc')
    if g: src.append(gs); L.append("| Norway, Switzerland, South Africa with GMD growth 1991–2011 | " + " | ".join(cp(g['arc'][k]['corr'], g['arc'][k]['p'], 2) for k in k4) + " |")
    return "\n".join(L), src


def table_loo(sample='S31'):
    r, s = _r(sample, 'robustness'); loo = {k[8:]: v for k, v in r.items() if k.startswith('without ') and len(k) == 11}
    L = ["| Left out | Lead-2 | Lead-1 | Crisis year | After-2 (lower tail) |", "|---|---|---|---|---|"]
    for iso, v in loo.items(): L.append(f"| {NAME.get(iso, iso)} | " + " | ".join(cp(*v[k], d=3) for k in ('lead2', 'lead1', 'crisis', 'after2')) + " |")
    return "\n".join(L), [s]


def table_edge():
    src = []; reg = []
    for smp in ('S31', 'S30', 'S26'):
        rel = f"results/edge_matched/{smp}.json"; src.append(rel); reg.append(_load(rel)['tests'])
    L = ["| Test | S31 | S30 | S26 |", "|---|---|---|---|"]
    for k, t in reg[0].items():
        cell = lambda d: f"{fmt(d[k]['stat'], 'c3') if abs(d[k]['stat']) >= 1e-3 else fmt(d[k]['stat'], 'e2')} ({fmt(d[k]['p_current'], 'p')} → {fmt(d[k]['p_edge'], 'p')})"
        cross = lambda d: (d[k]['p_current'] <= 0.05) != (d[k]['p_edge'] <= 0.05)
        L.append(f"| {t['label']} | " + " | ".join((f"**{cell(d)}**" if cross(d) else cell(d)) for d in reg) + " |")
    return "\n".join(L), src


def table_multiplicity():
    src = []; L = ["| Lag | " + " | ".join(f"{s} raw p | {s} Bonferroni | {s} BH q" for s in ('S31', 'S30', 'S26')) + " |", "|---|" + "---|" * 9]
    data = {}
    for s in ('S31', 'S30', 'S26'): a, rel = _r(s, 'arc'); data[s] = a; src.append(rel)
    for l in LAGS:
        L.append(f"| {LAGN[l]} | " + " | ".join(f"{fmt(data[s]['arc'][l]['p'], 'p')} | {fmt(data[s]['bonferroni'][l], 'p')} | {fmt(data[s]['benjamini_hochberg'][l], 'p')}"
                                                for s in ('S31', 'S30', 'S26')) + " |")
    return "\n".join(L), src


def table_neff():
    d = _load('dtt/results/d3_neff.json'); src = ['dtt/results/d3_neff.json']
    L = ["| Sample, phases | All years | Recession years | Year before | Normal years | 2009 | 2020 |", "|---|---|---|---|---|---|---|"]
    for s in ('S31', 'S30', 'S26'):
        for conv, nm in (('P', 'two-sided (P)'), ('C', 'past-only (C)')):
            x = d[s][conv]
            L.append(f"| {s}, {nm} | " + " | ".join(fmt(x[g]['neff'], 'f2') for g in ('all years', 'recession years', 'lead-1 years', 'normal years'))
                     + f" | {fmt(x['by_year']['2009']['neff'], 'f2')} | {fmt(x['by_year']['2020']['neff'], 'f2')} |")
    return "\n".join(L), src


def table_neff_recessions():
    d = _load('dtt/results/d3_neff.json')['S31']; src = ['dtt/results/d3_neff.json']
    rec = [1975, 1982, 1991, 2009, 2020]
    L = ["| Phases | " + " | ".join(str(y) for y in rec) + " |", "|---|" + "---|" * len(rec)]
    for conv, nm in (('P', 'two-sided (P)'), ('C', 'past-only (C)')):
        L.append(f"| {nm} | " + " | ".join(fmt(d[conv]['by_year'][str(y)]['neff'], 'f2') for y in rec) + " |")
    return "\n".join(L), src


def table_g1b():
    V = _load('gnn/G1b/verdicts.json'); src = ['gnn/G1b/verdicts.json']
    from ef.gnn.g1b_report import SETTING, SHORT
    L = ["| Worlds | Layer | Past-only lead-1 rejects (95% interval) | Minus constant noise, points (95% interval) | Minus shuffled synchrony, points (95% interval) | Worlds at p ≤ 0.038 | Verdict |",
         "|---|---|---|---|---|---|---|"]
    pt = lambda x: fmt(100 * x, 'c1')
    for v in V:
        dc, ds = v['diff_constant'], v['diff_shuffled']
        L.append(f"| {SETTING[v['setting']]} | {SHORT[v['variant']]} | {fmt(v['rate'], 'pct1')} ({fmt(v['lo'], 'pct1')}–{fmt(v['hi'], 'pct1')}) | "
                 f"{pt(dc[0])} ({pt(dc[1])} to {pt(dc[2])}) | {pt(ds[0])} ({pt(ds[1])} to {pt(ds[2])}) | {fmt(v['share_at_real_p'], 'pct1')} | {v['verdict']} |")
    return "\n".join(L), src


def table_channels():
    src = []; L = ["| Channel | Economies | Lead-2 | Lead-1 | Crisis year | After-2 | Past-only lead-2 | Past-only lead-1 |", "|---|---|---|---|---|---|---|---|"]
    a, s = _r('S31', 'channels'); src.append(s); rel = 'results/S31/C/channels.json'; c = _load(rel)['results']; src.append(rel)
    for k, nm in (('GDP', 'Real GDP (Global Macro Database)'), ('inv', 'Investment'), ('strate', 'Short-term interest rate')):
        t = a['sync'][k]['tests']; tc = c['sync'][k]['tests']
        L.append(f"| {nm} | {a['sync'][k]['n']} | " + " | ".join(cp(*t[x]) for x in ('lead2', 'lead1', 'same', 'after2')) + f" | {cp(*tc['lead2'])} | {cp(*tc['lead1'])} |")
    return "\n".join(L), src


def table_strict():
    src = []; L = ["| Rolling statistic, windows kept inside 1970–2022 | S31 | S30 | S26 |", "|---|---|---|---|"]
    vals = {}
    for s in ('S31', 'S30', 'S26'):
        st = s + '_strict'; d, ds = _r(st, 'diversification'); m, ms = _r(st, 'mst'); c, cs = _r(st, 'csd'); b, bs = _r(st, 'bifurcation')
        src += [ds, ms, cs, bs]; vals[s] = (d, m, c, b)
    rows = [('Cross share of the recession excess, GDP / equal weights', lambda d, m, c, b: f"{fmt(d['gdp_mean']['cross_fraction_of_excess'], 'pct1')} / {fmt(d['equal']['cross_fraction_of_excess'], 'pct1')}"),
            ('MST contraction before recessions, raw; detrended', lambda d, m, c, b: f"{cp(m['tau_L'], m['p_contraction'])}; {cp(m['tau_L_detrended'], m['p_contraction_detrended'])}"),
            ('Autocorrelation trend', lambda d, m, c, b: cp(c['tau_ar1'], c['p_ar1'])), ('Variance trend', lambda d, m, c, b: cp(c['tau_var'], c['p_var'])),
            ('Recovery-rate change', lambda d, m, c, b: cp(b['stat_real'], b['p_slowing_post']))]
    for nm, f in rows: L.append(f"| {nm} | " + " | ".join(f(*vals[s]) for s in ('S31', 'S30', 'S26')) + " |")
    return "\n".join(L), src


def table_csd_by_event():
    rel = 'results/followup/S31/P/csd_by_event.json'; d = _load(rel)['results']['sets']
    L = ["| Recessions used | Variance trend τ (p) | Autocorrelation trend τ (p) |", "|---|---|---|"]
    for k, v in d.items():
        L.append(f"| {', '.join(map(str, v['events']))} | {cp(v['tau_var'], v['p_var'])} | {cp(v['tau_ar1'], v['p_ar1'])} |")
    return "\n".join(L), [rel]


def table_meanr():
    """Mean r by period type with 95% bootstrap intervals, and the superposed epoch, three samples."""
    src = []; L = ["| Sample | Recession years | Downturn years (1998, 2001, 2012) | Other years | Epoch mean r, t−4 … t+4 |", "|---|---|---|---|---|"]
    for smp in ('S31', 'S30', 'S26'):
        a, rel = _r(smp, 'arc'); src.append(rel); m = a['mean_ci']
        ci = lambda k: f"{fmt(m[k][0], 'f2')} [{fmt(m[k][1], 'f2')}, {fmt(m[k][2], 'f2')}]"
        L.append(f"| {smp} | {ci('recession')} | {ci('downturn')} | {ci('normal')} | " + ", ".join(fmt(x, 'f2') for x in a['epoch_mean_t-4..t+4']) + " |")
    return "\n".join(L), src


def table_conv_full():
    """The arc at every lag under each phase convention, three samples."""
    src = []; L = ["| Sample | Convention | " + " | ".join(LAGN[l] for l in LAGS) + " | r–Ā detrended |", "|---|---|" + "---|" * (len(LAGS) + 1)]
    for smp in ('S31', 'S30', 'S26'):
        c, rel = _r(smp, 'conventions'); src.append(rel)
        for conv in ('P', 'W', 'N', 'E', 'C'):
            a = c[conv]['arc']; amp = c[conv]['amp_detrended']
            L.append(f"| {smp} | {conv} | " + " | ".join(cp(a[l]['corr'], a[l]['p']) for l in LAGS) + f" | {cp(amp[0], amp[1])} |")
    return "\n".join(L), src


def table_g1_full():
    """Every G1 test in every setting, real recession dates (rule A) and own dates (rule B): the share of 1,000 worlds
    rejecting at p <= 0.05."""
    from ef.gnn import g1_report as T
    rows = _load('gnn/G1/rejections.csv'); cells = [(m, c) for m in ('kuramoto', 'stuart_landau') for c in ('null', 'forcing', 'network_half', 'network')]
    name = {'null': 'none', 'forcing': 'forcing', 'network_half': 'κ*/2', 'network': 'κ*'}
    out = []
    for rule, title in (('A', 'real recession dates'), ('B', 'each world\'s own recession dates')):
        L = [f"*{title.capitalize()}.*", "", "| Test | " + " | ".join(f"{'K' if m == 'kuramoto' else 'SL'} {name[c]}" for m, c in cells) + " |", "|---|" + "---|" * len(cells)]
        for t in T.ORDER:
            vals = []
            for m, c in cells:
                r = next((x for x in rows if x['model'] == m and x['cell'] == c and x['rule'] == rule and x['test'] == t), None)
                vals.append('—' if r is None else (f"**{fmt(float(r['rate']), 'pct1')}**" if r['verdict'] == 'over' else fmt(float(r['rate']), 'pct1')))
            L.append(f"| {T.LABELS[t]} | " + " | ".join(vals) + " |")
        out.append("\n".join(L))
    return "\n\n".join(out), ['gnn/G1/rejections.csv']


TABLES = {'kappa0': table_kappa0, 'conventions': table_conventions, 'A1': table_A1, 'robust_S31': lambda: table_robust('S31'),
          'robust_S30': lambda: table_robust('S30'), 'robust_S26': lambda: table_robust('S26'), 'loo_S31': lambda: table_loo('S31'),
          'edge': table_edge, 'multiplicity': table_multiplicity, 'neff': table_neff, 'neff_recessions': table_neff_recessions,
          'g1b': table_g1b, 'channels': table_channels, 'strict': table_strict, 'csd_by_event': table_csd_by_event,
          'meanr': table_meanr, 'conv_full': table_conv_full, 'g1_full': table_g1_full}
