"""Every number the Paper 1 manuscript prints is a placeholder resolved here, so each one traces to a results file.

A placeholder is {{ref}} or {{ref|fmt}}. ref is either
  file#path      a key path inside a results file ('/' separates keys); file is
                   S31/P/arc            results/S31/P/arc.json, path starting under its 'results'
                   results/..., gnn/..., dtt/... with an extension: that file from the repository root (JSON from its root;
                   CSV rows chosen by 'col=value' steps, then the column: gnn/G1/rejections.csv#model=kuramoto/cell=null/rule=A/test=arc.lead1/rate)
  @name:arg,...  a derived value (ranges, ratios, counts) from DERIVED, each listing the files it reads.
fmt (default g3): c3 c2 c1 (signed), f4 f3 f2 f1 f0, p (a p-value: 0.019, 0.0002), pct1 pct0 (a share as %), pp1 (already
in %), x1 (a ratio, 1.6×), int, yr (a year), e2 (scientific).
"""
import csv
import gzip
import json
import os
import re
from functools import lru_cache

import numpy as np

from ef import config

ROOT = config.repo_root()
MINUS = '−'
USED = []           # (placeholder, value, text, sources) in the order resolved


@lru_cache(maxsize=None)
def _load(rel):
    f = os.path.join(ROOT, rel)
    if rel.endswith('.json'): return json.load(open(f))
    if rel.endswith('.csv') or rel.endswith('.csv.gz'):
        op = gzip.open if rel.endswith('.gz') else open
        with op(f, 'rt') as h: return list(csv.DictReader(h))
    raise ValueError(f"unknown file type: {rel}")


def _file(spec):
    """'S31/P/arc' -> ('results/S31/P/arc.json', ['results']); explicit paths are taken as they are."""
    if '.' in os.path.basename(spec): return spec, []
    return f"results/{spec}.json", ['results']


def lookup(ref):
    """(value, [source file]) of file#path."""
    spec, path = ref.split('#', 1); rel, pre = _file(spec); d = _load(rel)
    if isinstance(d, list):                                      # CSV: filter rows, then a column
        steps = path.split('/'); rows = d
        for s in steps[:-1]:
            k, v = s.split('=', 1); rows = [r for r in rows if r[k] == v]
        if len(rows) != 1: raise KeyError(f"{ref}: {len(rows)} rows")
        return float(rows[0][steps[-1]]), [rel]
    for k in pre + path.split('/'):
        if isinstance(d, list): d = d[int(k)]
        elif k in d: d = d[k]
        else: raise KeyError(f"{ref}: no key {k!r}")
    return d, [rel]


def fmt(v, f='g3'):
    if v is None or (isinstance(v, float) and np.isnan(v)): return '—'
    if f == 'raw': return str(v)
    v = float(v)
    if f in ('c3', 'c2', 'c1'): s = f"{v:+.{f[1]}f}"
    elif f in ('f4', 'f3', 'f2', 'f1', 'f0'): s = f"{v:.{f[1]}f}"
    elif f == 'p':
        if v < 0.00025: s = '0.0002'
        elif v < 0.001: s = f"{v:.4f}"
        else: s = f"{v:.3f}"
    elif f == 'p2': s = f"{v:.2f}"
    elif f in ('pct1', 'pct0', 'pct2'): s = f"{100 * v:.{f[3]}f}%"
    elif f in ('pp1', 'pp0'): s = f"{v:.{f[2]}f}%"
    elif f == 'pts1': s = f"{100 * v:.1f} percentage points"
    elif f == 'x1': s = f"{v:.1f}×"
    elif f == 'x2': s = f"{v:.2f}×"
    elif f == 'int': s = f"{int(round(v)):,}"
    elif f == 'yr': s = f"{int(round(v))}"
    elif f == 'e2':
        e = int(np.floor(np.log10(abs(v)))); m = v / 10 ** e
        s = f"{m:.2f} × 10^{e}^" if abs(m - 1) > 1e-9 else f"10^{e}^"
    elif f == 'g3': s = f"{v:.3g}"
    else: raise ValueError(f"unknown format {f!r}")
    return s.replace('-', MINUS)


# ------------------------------------------------------------------ derived values

def _arc(sample, lag, conv='P'):
    if conv == 'P': return lookup(f"{sample}/P/arc#arc/{lag}/corr")[0], lookup(f"{sample}/P/arc#arc/{lag}/p")[0]
    return lookup(f"{sample}/P/conventions#{conv}/arc/{lag}/corr")[0], lookup(f"{sample}/P/conventions#{conv}/arc/{lag}/p")[0]


def _rob(sample='S31'):
    return lookup(f"{sample}/P/robustness#baseline")[0] and _load(f"results/{sample}/P/robustness.json")['results']


def loo_range(sample, lag, which, end):
    """Leave-one-economy-out range of a lag: which = 'corr' or 'p', end = 'min' or 'max'."""
    R = _rob(sample); vals = [v[lag][0 if which == 'corr' else 1] for k, v in R.items() if k.startswith('without ') and len(k) == 11]
    return (min(vals) if end == 'min' else max(vals)), [f"results/{sample}/P/robustness.json"]


def loo_count_below(sample, lag, alpha=0.05):
    R = _rob(sample); vals = [v[lag][1] for k, v in R.items() if k.startswith('without ') and len(k) == 11]
    return sum(p <= alpha + 1e-12 for p in vals), [f"results/{sample}/P/robustness.json"]


def n_economies(sample):
    return len(_load(f"results/{sample}/P/arc.json")['economies']), [f"results/{sample}/P/arc.json"]


def mst_ratio(sample):
    m = lookup(f"{sample}/P/mst#L_decade_means")[0]; return m['1979-1989'] / m['2013-2022'], [f"results/{sample}/P/mst.json"]


def neff_year(sample, conv, year):
    return _load('dtt/results/d3_neff.json')[sample][conv]['by_year'][str(year)]['neff'], ['dtt/results/d3_neff.json']


def min_r(sample='S31', end='min'):
    r = lookup(f"{sample}/P/arc#r_by_year")[0]; y = (min if end == 'min' else max)(r, key=r.get); return r[y], [f"results/{sample}/P/arc.json"]


def argmin_r(sample='S31', end='min'):
    r = lookup(f"{sample}/P/arc#r_by_year")[0]; y = (min if end == 'min' else max)(r, key=r.get); return int(y), [f"results/{sample}/P/arc.json"]


def g1_rate(model, cell, rule, test):
    return float([r for r in _load('gnn/G1/rejections.csv') if r['model'] == model and r['cell'] == cell and r['rule'] == rule
                  and r['test'] == test][0]['rate']), ['gnn/G1/rejections.csv']


def g1_range(cell, rule, test):
    v = [g1_rate(m, cell, rule, test)[0] for m in ('kuramoto', 'stuart_landau')]; return v, ['gnn/G1/rejections.csv']


def g1_lo(cell, rule, test):
    v, s = g1_range(cell, rule, test); return min(v), s


def g1_hi(cell, rule, test):
    v, s = g1_range(cell, rule, test); return max(v), s


def g1_size_ok(model):
    rows = [r for r in _load('gnn/G1/rejections.csv') if r['model'] == model and r['cell'] == 'null' and r['rule'] == 'A'
            and not r['test'].startswith('family.')]
    return sum(r['verdict'] != 'over' for r in rows), ['gnn/G1/rejections.csv']


def g1_n_tests():
    rows = {r['test'] for r in _load('gnn/G1/rejections.csv') if r['model'] == 'kuramoto' and r['cell'] == 'null' and r['rule'] == 'A'
            and not r['test'].startswith('family.')}
    return len(rows), ['gnn/G1/rejections.csv']


def g1b_verdict(setting, variant, key):
    v = next(x for x in _load('gnn/G1b/verdicts.json') if x['setting'] == setting and x['variant'] == variant)
    k = key.split('.'); x = v[k[0]]
    if len(k) > 1: x = x[int(k[1])]
    return x, ['gnn/G1b/verdicts.json']


def g1b_rate(setting, variant, kind, conv, lag, col='rate'):
    r = [x for x in _load('gnn/G1b/rejections.csv') if x['setting'] == setting and x['variant'] == variant and x['kind'] == kind
         and x['convention'] == conv and x['lag'] == lag][0]
    return float(r[col]), ['gnn/G1b/rejections.csv']


def g1b_count(verdict):
    return sum(1 for x in _load('gnn/G1b/verdicts.json') if x['setting'] == 'network' and x['variant'] != 'primary'
               and x['verdict'] == verdict), ['gnn/G1b/verdicts.json']


def g1b_names(verdict):
    """The sensitivities (trade-coupled worlds) with this verdict, by their short names."""
    from ef.gnn.g1b_report import SHORT
    v = [SHORT[x['variant']] for x in _load('gnn/G1b/verdicts.json') if x['setting'] == 'network' and x['variant'] != 'primary' and x['verdict'] == verdict]
    return '; '.join(v), ['gnn/G1b/verdicts.json']


def ratio(a, b):
    va, sa = resolve_value(a); vb, sb = resolve_value(b); return va / vb, sa + sb


def diff(a, b):
    va, sa = resolve_value(a); vb, sb = resolve_value(b); return va - vb, sa + sb


def sub1(a):
    v, s = resolve_value(a); return 1 - v, s


FIGDATA = 'paper1/manuscript/figdata/figdata_s31.json'


def fd(series, agg, y0=0, y1=9999):
    """A statistic of a figure-data series (S31, equal weights unless the name says otherwise) over windows ending in
    y0..y1: series 'rbar', 'share', or 'own_IRN' (Iran's share of the own term); agg min, max, or below40 (count < 0.40),
    n (windows)."""
    d = _load(FIGDATA)['div']; yrs = d['years']
    x = d['own_share_by_economy'][series[4:]] if series.startswith('own_') else d['equal'][series]
    v = [a for y, a in zip(yrs, x) if a is not None and y0 <= y <= y1]
    r = {'min': min(v), 'max': max(v), 'below40': sum(a < 0.40 for a in v), 'n': len(v)}[agg]
    return r, [FIGDATA]


def eq_share(agg):
    """(N - 1) rho / (1 + (N - 1) rho), the equal-variance cross share, at the smallest or largest window rho."""
    rho, s = fd('rbar', agg); N = len(_load('results/S31/P/arc.json')['economies'])
    return (N - 1) * rho / (1 + (N - 1) * rho), s + ['results/S31/P/arc.json']


def rms_random(sample):
    N = len(_load(f'results/{sample}/P/arc.json')['economies']); return N ** -0.5, [f'results/{sample}/P/arc.json']


def mean_random(sample):
    N = len(_load(f'results/{sample}/P/arc.json')['economies']); return (np.pi / (4 * N)) ** 0.5, [f'results/{sample}/P/arc.json']


def edge_rate(model, cell, test):
    """Share of simulated G1 worlds in which the edge-matched null rejects at p <= 0.05 (results/edge_matched/validation.csv.gz)."""
    rows = [r for r in _load('results/edge_matched/validation.csv.gz') if r['model'] == model and r['cell'] == cell and r['test'] == test and r['null'] == 'edge']
    return sum(float(r['p']) <= 0.05 + 1e-12 for r in rows) / len(rows), ['results/edge_matched/validation.csv.gz']


def edge_crossings():
    """How many (sample, test) p-values fall on opposite sides of 0.05 under the circular and the edge-matched null."""
    n = 0; src = []
    for smp in ('S31', 'S30', 'S26'):
        rel = f'results/edge_matched/{smp}.json'; src.append(rel)
        n += sum((t['p_current'] <= 0.05) != (t['p_edge'] <= 0.05) for t in _load(rel)['tests'].values())
    return n, src


def nexceed(ref, n=5000):
    """Number of the n null draws at least as extreme as the observed value, from its p = (1 + k) / (n + 1)."""
    p, s = resolve_value(ref); return round(p * (n + 1) - 1), s


DERIVED = {f.__name__: f for f in (loo_range, loo_count_below, n_economies, mst_ratio, neff_year, min_r, argmin_r, g1_rate, g1_lo, g1_hi,
                                   g1_size_ok, g1_n_tests, g1b_verdict, g1b_rate, g1b_count, ratio, diff, sub1, fd, eq_share, rms_random, mean_random, edge_rate, edge_crossings, nexceed, g1b_names)}


def _args(s):
    out = []
    for a in s.split(','):
        a = a.strip()
        if re.fullmatch(r'-?\d+', a): out.append(int(a))
        else: out.append(a)
    return out


def resolve_value(ref):
    ref = ref.strip()
    if ref.startswith('@'):
        name, _, args = ref[1:].partition(':')
        if name in ('ratio', 'diff'):
            a, b = args.split(';'); return DERIVED[name](a, b)
        if name in ('sub1', 'nexceed'): return DERIVED[name](args)
        return DERIVED[name](*_args(args)) if args else DERIVED[name]()
    return lookup(ref)


def render(text, where=''):
    """Replace every {{ref|fmt}} in text; log each in USED."""
    def rep(m):
        if m.group(1).startswith('lit:'):                 # a literal number from outside the results files, with its source
            lit, _, why = m.group(1)[4:].partition('|'); USED.append((where, m.group(1), lit, lit, why)); return lit
        ref, _, f = m.group(1).partition('|'); v, src = resolve_value(ref); s = fmt(v, f or 'g3')
        USED.append((where, m.group(1), v if not isinstance(v, (list, dict)) else str(v), s, ';'.join(dict.fromkeys(src))))
        return s
    return re.sub(r'\{\{([^{}]+)\}\}', rep, text)
