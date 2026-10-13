"""results/EDGE_MATCHED.md: the validation of the edge-matched nulls on the G1 worlds and the real p-values on S31,
S30 and S26 beside the current ones (pre-registration amendment 4). Every number is read from results/edge_matched/
and gnn/G1/."""
import json
import os

import numpy as np
import pandas as pd

from ef import config
from ef.edge_null import G1_PAIRS, OUT, TESTS
from ef.gnn import g1_report

ROOT = config.repo_root()
MODEL = {'kuramoto': 'Kuramoto', 'stuart_landau': 'Stuart–Landau'}
SAMPLES = ('S31', 'S30', 'S26')
ORDER = [*(f'arc.{c}.{l}' for c in 'PWNE' for l in ('lead1', 'crisis', 'after1', 'after2')), 'E11.within.lead1', 'E11.between.lead1',
         'G3.lead1', 'G3.same', 'G3.after2', 'D5.gdp_mean', 'D5.equal', 'D6.ratio.gdp_mean', 'D6.ratio.equal', 'D6.cross.gdp_mean',
         'D6.cross.equal', 'D6.own.gdp_mean', 'D6.own.equal', 'D11.align', 'D11.swing', 'E4.raw', 'E4.detrended', 'E6', 'F1', 'F2', 'F4', 'C1']
REGISTRY = {'arc.P.lead1': 'A2', 'arc.P.crisis': 'A3', 'arc.P.after1': 'A4', 'arc.P.after2': 'A5', 'arc.W': 'A10', 'arc.N': 'A11',
            'arc.E': 'A12', 'E11': 'E11', 'G3': 'G3', 'D5': 'D5', 'D6': 'D6', 'D11': 'D11', 'E4': 'E4', 'E6': 'E6', 'F1': 'F1',
            'F2': 'F2', 'F4': 'F4', 'C1': 'C1'}


def reg(k):
    for pre in (k, '.'.join(k.split('.')[:2]), k.split('.')[0]):
        if pre in REGISTRY: return REGISTRY[pre]
    return ''


def rates(df, col='p', alpha=0.05):
    k = (df[col] <= alpha).sum(); n = len(df); lo, hi = g1_report.wilson(k, n); return k / n, lo, hi, n


def fmt_rate(x, exact=0.05):
    r, lo, hi, n = x; s = f"{100 * r:.1f}% ({100 * lo:.1f}–{100 * hi:.1f})"
    return f"**{s}**" if lo > exact else s


def load():
    V = pd.read_csv(os.path.join(OUT, 'validation.csv.gz'), keep_default_na=False, na_values=[''])
    G = pd.read_csv(os.path.join(ROOT, 'gnn', 'G1', 'pvalues.csv.gz'), keep_default_na=False, na_values=[''])
    R = {s: json.load(open(os.path.join(OUT, f'{s}.json'))) for s in SAMPLES if os.path.exists(os.path.join(OUT, f'{s}.json'))}
    return V, G, R


def validation_table(V, G):
    """Rejection rates at p <= 0.05 on the uncoupled G1 worlds, real calendar: the current null (from gnn/G1) and the
    edge-matched null, both models."""
    Gn = G[(G.cell == 'null') & (G.rule.isin(['A', 'any']))]; Vn = V[(V.cell == 'null') & (V.null == 'edge')]
    L = ["| Test | Registry | Kuramoto, current null | Kuramoto, edge-matched | Stuart–Landau, current null | Stuart–Landau, edge-matched |",
         "|---|---|---|---|---|---|"]
    rows = []
    for k in [k for k in ORDER if k in set(Vn.test)]:
        cells = []
        for m in MODEL:
            g1t = G1_PAIRS.get(k)
            cur = Gn[(Gn.model == m) & (Gn.test == g1t)] if g1t else None
            exact_cur = g1_report.EXACT['shift'] if g1t in g1_report.SHIFT else 0.05
            cells.append(fmt_rate(rates(cur), exact_cur) if cur is not None and len(cur) else '—')
            em = rates(Vn[(Vn.model == m) & (Vn.test == k)]); cells.append(fmt_rate(em)); rows.append((k, m, em))
        L.append(f"| {TESTS[k][0]} | {reg(k)} | " + " | ".join(cells) + " |")
    return L, rows


def coupled_table(V, G):
    Gk = G[(G.cell == 'network') & (G.rule == 'A')]; Vk = V[(V.cell == 'network') & (V.null == 'edge')]
    L = ["| Test | Kuramoto κ\\*, circular shifts | Kuramoto κ\\*, edge-matched (multivariate) | Stuart–Landau κ\\*, circular shifts | Stuart–Landau κ\\*, edge-matched |",
         "|---|---|---|---|---|"]
    for k in [k for k in ORDER if k in set(Vk.test)]:
        cells = []
        for m in MODEL:
            cur = Gk[(Gk.model == m) & (Gk.test == G1_PAIRS[k])] if k in G1_PAIRS else None
            cells.append(fmt_rate(rates(cur), g1_report.EXACT['shift']) if cur is not None and len(cur) else '—')
            cells.append(fmt_rate(rates(Vk[(Vk.model == m) & (Vk.test == k)])))
        L.append(f"| {TESTS[k][0]} | " + " | ".join(cells) + " |")
    return L


def scheme_table(V, G):
    """Cross term and MST under Phase 3's own surrogate scheme, which the G1 run did not use."""
    Gn = G[(G.cell == 'null') & (G.rule == 'A')]; Vp = V[(V.cell == 'null') & (V.null == 'phase3_scheme')]
    L = ["| Test | Kuramoto, as G1 ran it (1962–2022 cycles) | Kuramoto, Phase 3 scheme (1950–2022 cycles, cut) | Stuart–Landau, as G1 ran it | Stuart–Landau, Phase 3 scheme |",
         "|---|---|---|---|---|"]
    for k in ('D5.gdp_mean', 'D5.equal', 'E4.raw', 'E4.detrended', 'E6'):
        cells = []
        for m in MODEL:
            cells.append(fmt_rate(rates(Gn[(Gn.model == m) & (Gn.test == G1_PAIRS[k])])))
            cells.append(fmt_rate(rates(Vp[(Vp.model == m) & (Vp.test == k)])))
        L.append(f"| {TESTS[k][0]} | " + " | ".join(cells) + " |")
    return L


def pfmt(p):
    return '—' if p is None else (f"{p:.4f}" if p < 0.001 else f"{p:.3f}")


def real_table(R):
    L = ["| Test | Registry | " + " | ".join(f"{s}: statistic | {s}: p now | {s}: p edge-matched" for s in SAMPLES if s in R) + " |",
         "|---|---|" + "---|---|---|" * len(R)]
    flags = []
    for k in ORDER:
        cells = []
        for s in SAMPLES:
            if s not in R: continue
            t = R[s]['tests'][k]; pc, pe = t['p_current'], t['p_edge']
            cross = (pc <= 0.05) != (pe <= 0.05)
            if cross: flags.append((s, k, pc, pe))
            cells += [f"{t['stat']:+.3f}" if abs(t['stat']) >= 0.01 or t['stat'] == 0 else f"{t['stat']:+.2e}", pfmt(pc), f"**{pfmt(pe)}**" if cross else pfmt(pe)]
        L.append(f"| {TESTS[k][0]} | {reg(k)} | " + " | ".join(cells) + " |")
    return L, flags


def main():
    from ef import edge_text
    V, G, R = load()
    open(os.path.join(ROOT, 'results', 'EDGE_MATCHED.md'), 'w').write(edge_text.report(V, G, R))
    print("wrote results/EDGE_MATCHED.md")
