"""G1 tables: rejection rates with Wilson intervals against each test's exact rate (gnn/G1/rejections.csv), and the
pieces of gnn/G1_report.md that are numbers. The report's text is in report_text()."""
import json
import os

import numpy as np
import pandas as pd

from ef import config
from ef.gnn import g1, simulator as S

SHIFT = {'arc.lead2', 'arc.lead1', 'arc.crisis', 'arc.after1', 'arc.after2', 'arc_C.lead2', 'arc_C.lead1', 'amplitude.p_shift'}
EXACT = {'shift': 2 / 53, 'surrogate': 10 / 200}
LABELS = {
    'arc.lead2': 'Arc, lead-2', 'arc.lead1': 'Arc, lead-1', 'arc.crisis': 'Arc, crisis year', 'arc.after1': 'Arc, after-1',
    'arc.after2': 'Arc, after-2', 'arc_C.lead2': 'Arc, lead-2, past-only phases', 'arc_C.lead1': 'Arc, lead-1, past-only phases',
    'amplitude.p_shift': 'r with swing size (shifts)', 'amplitude.p_surrogate': 'r with swing size (surrogates)',
    'diversification.gdp_mean': 'Cross term at recessions, GDP weights', 'diversification.equal': 'Cross term at recessions, equal weights',
    'structure.p_align': 'Identity: alignment at recessions', 'structure.p_swing': 'Identity: swing size at recessions',
    'mst.p_contraction': 'MST contraction before recessions', 'mst.p_contraction_detrended': 'MST contraction, detrended',
    'mst.p_fragility': 'MST fragility before recessions', 'phase_lags.p_spread_lower': 'Phase leads clustered',
    'csd.p_ar1': 'Slowing down: autocorrelation of r', 'csd.p_var': 'Slowing down: variance of r',
    'bifurcation.p_slowing': 'Slower recovery after recessions',
    'family.arc_any': 'Any of the five arc lags', 'family.arc_leads': 'Any of lead-2, lead-1, crisis'}
ORDER = list(LABELS)
MODEL = {'kuramoto': 'Kuramoto', 'stuart_landau': 'Stuart–Landau'}
CELL = {'null': 'null (κ = 0, φ = 0)', 'forcing': 'forcing only (φ*)', 'network_half': 'network, κ*/2', 'network': 'network, κ*'}


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def exact_rate(test):
    if test.startswith('family.'): return np.nan
    return EXACT['shift'] if test in SHIFT else EXACT['surrogate']


def rejections(P, alpha=g1.DESIGN['alpha']):
    """One row per model, setting, rule and test: worlds, rejections, rate, Wilson interval, exact rate and verdict.
    Date-free tests (rule 'any') are listed under both rules. Family rates: any arc lag; any of the three leads."""
    P = pd.concat([P[P.rule != 'any'], P[P.rule == 'any'].assign(rule='A'), P[P.rule == 'any'].assign(rule='B')])
    P = P.assign(reject=P.p <= alpha)
    fam = []
    for name, tests in (('family.arc_any', [f'arc.{l}' for l in ('lead2', 'lead1', 'crisis', 'after1', 'after2')]),
                        ('family.arc_leads', ['arc.lead2', 'arc.lead1', 'arc.crisis'])):
        f = P[P.test.isin(tests)].groupby(['model', 'cell', 'rule', 'world']).reject.any().reset_index().assign(test=name)
        fam.append(f)
    P = pd.concat([P[['model', 'cell', 'rule', 'world', 'test', 'reject']]] + fam)
    R = P.groupby(['model', 'cell', 'rule', 'test']).reject.agg(['size', 'sum']).reset_index().rename(columns={'size': 'worlds', 'sum': 'rejections'})
    R['rate'] = R.rejections / R.worlds
    lo, hi = wilson(R.rejections.to_numpy(float), R.worlds.to_numpy(float)); R['lo'], R['hi'] = lo, hi
    R['exact'] = R.test.map(exact_rate)
    R['verdict'] = np.where(R.exact.isna(), '', np.where(R.lo > R.exact, 'over', np.where(R.hi < R.exact, 'under', 'pass')))
    R['test_order'] = R.test.map(ORDER.index)
    return R.sort_values(['model', 'cell', 'rule', 'test_order']).drop(columns='test_order')


def fmt(row, bold_over=True):
    s = f"{100 * row.rate:.1f}% ({100 * row.lo:.1f}–{100 * row.hi:.1f})"
    return f"**{s}**" if bold_over and row.verdict == 'over' else s


def table_null(R):
    """The κ = 0 check: every test, both models, both rules."""
    N = R[R.cell == 'null'].set_index(['model', 'rule', 'test'])
    L = ["| Test | Exact rate | Kuramoto, real dates (A) | Kuramoto, own dates (B) | Stuart–Landau, real dates (A) | Stuart–Landau, own dates (B) |",
         "|---|---|---|---|---|---|"]
    for t in ORDER:
        ex = exact_rate(t); cells = []
        for m in S.MODELS:
            for rule in ('A', 'B'):
                cells.append(fmt(N.loc[(m, rule, t)]) if (m, rule, t) in N.index else '—')
        L.append(f"| {LABELS[t]} | {'—' if np.isnan(ex) else f'{100 * ex:.1f}%'} | " + " | ".join(cells) + " |")
    return L


def table_cells(R, rule):
    """Every setting, for one rule: rejection rate per test."""
    D = R[R.rule == rule].set_index(['model', 'cell', 'test'])
    L = ["| Test | Exact | " + " | ".join(f"{MODEL[m][:4]}. {c}" for m in S.MODELS for c in ('null', 'forcing', 'κ*/2', 'κ*')) + " |",
         "|---|---|" + "---|" * 8]
    for t in ORDER:
        ex = exact_rate(t)
        vals = []
        for m in S.MODELS:
            for c in ('null', 'forcing', 'network_half', 'network'):
                x = D.loc[(m, c, t)] if (m, c, t) in D.index else None
                vals.append('—' if x is None else (f"**{100 * x.rate:.1f}**" if x.verdict == 'over' else f"{100 * x.rate:.1f}"))
        L.append(f"| {LABELS[t]} | {'—' if np.isnan(ex) else f'{100 * ex:.1f}'} | " + " | ".join(vals) + " |")
    return L


def load():
    P = pd.read_csv(os.path.join(g1.OUT, 'pvalues.csv.gz'), keep_default_na=False, na_values=[''])     # 'null' is a setting
    cal = json.load(open(os.path.join(g1.OUT, 'calibration.json')))
    curve = pd.read_csv(os.path.join(g1.OUT, 'r_curve.csv'))
    W = pd.read_csv(os.path.join(g1.OUT, 'world_stats.csv.gz'), keep_default_na=False, na_values=[''])
    B = pd.read_csv(os.path.join(g1.OUT, 'rule_b_recessions.csv.gz'), keep_default_na=False, na_values=[''])
    return P, cal, curve, W, B


def main():
    from ef.gnn import g1_text
    P, cal, curve, W, B = load(); R = rejections(P)
    R.to_csv(os.path.join(g1.OUT, 'rejections.csv'), index=False, float_format='%.6g')
    root = os.path.dirname(g1.OUT)
    from ef import order, paper1
    from ef.phases import analytic
    D = paper1.load_data('S31', S.SPAN); r = order.r(analytic(D.logs, D.years, (1970, 2022), 'P')); y = np.arange(1970, 2023)
    real = {'r_1970_1995': float(r[y <= 1995].mean()), 'r_2010_2022': float(r[y >= 2010].mean())}
    # the identity's swing-size statistic on real S31 (as results/S31/P/structure.json, 'dA'), with and without 2020
    la = 2 * np.log(order.mean_amplitude(analytic(D.logs, D.years, (1970, 2022), 'P')))
    st = json.load(open(os.path.join(config.repo_root(), 'results', 'S31', 'P', 'structure.json')))
    real['dA'] = float(st.get('results', st)['dA'])
    for k, rec in (('dA_check', [1975, 1982, 1991, 2009, 2020]), ('dA_without_2020', [1975, 1982, 1991, 2009])):
        cm = np.isin(y, rec); real[k] = float(la[cm].mean() - la[~cm].mean())
    assert abs(real['dA_check'] - real['dA']) < 1e-9, "the recomputed statistic must equal the stored one"
    edge = pd.read_csv(os.path.join(g1.OUT, 'swing_edge_check.csv'))
    for x in pd.read_csv(os.path.join(g1.OUT, 'swing_edge_by_year.csv')).itertuples():
        g1_text._EBY[(x.model, int(x.year))] = x.mean_2logAbar_minus_average
    open(os.path.join(root, 'G1_report.md'), 'w').write(g1_text.report(R, cal, curve, W, B, P, real, edge))
    print(f"wrote {g1.OUT}/rejections.csv and gnn/G1_report.md")
