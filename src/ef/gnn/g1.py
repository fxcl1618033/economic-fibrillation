"""G1 experiment (docs/preregistration_G1.md): calibrate the simulator to S31, run every Paper 1 test on simulated
worlds with known coupling, and write gnn/G1/ and gnn/G1_report.md.

    python -m ef.gnn.g1 calibrate     # -> gnn/G1/calibration.json, gnn/G1/r_curve.csv
    python -m ef.gnn.g1 run           # -> gnn/G1/pvalues.csv.gz (needs the calibration)
    python -m ef.gnn.g1 report        # -> gnn/G1/rejections.csv, gnn/G1_report.md
"""
import argparse
import json
import os
import warnings
from multiprocessing import Pool

import numpy as np
import pandas as pd

from ef import config, paper1
from ef.gnn import simulator as S

DESIGN = {
    'n_worlds': 1000,             # per model and cell
    'n_calib': 200,               # worlds per calibration evaluation (common random numbers)
    'surrogates': 199,            # per surrogate test: p = (1 + k) / 200, so p <= 0.05 exactly when k <= 9
    'alpha': 0.05,
    'seed_calib': 1001, 'seed_cells': 2001, 'seed_tests': 3001, 'seed_curve': 4001,
    'sigma_grid': np.geomspace(0.05, 5.0, 25).round(5).tolist(),
    'mu_grid': [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0],
    'coupling_bracket': [1e-3, 50.0], 'bisection_steps': 16,     # amendment 1: Euler-Maruyama stays stable below 50
    'chunk': 250,
}
CELLS = (('null', 0.0, 0.0), ('forcing', 0.0, 1.0), ('network_half', 0.5, 0.0), ('network', 1.0, 0.0))  # x kappa*, x phi*
RUN_CONFIG = 'configs/runs/phase3_s31.yaml'
OUT = os.path.join(config.repo_root(), 'gnn', 'G1')
# the p-values read from each test's output: (test, label, path into the result, direction tested)
PVALUES = [('arc', f'arc.{l}', ('arc', l, 'p')) for l in ('lead2', 'lead1', 'crisis', 'after1', 'after2')] + \
          [('conventions', f'arc_C.{l}', ('C', 'arc', l, 'p')) for l in ('lead2', 'lead1')] + \
          [('amplitude', 'amplitude.p_shift', ('p_shift',)), ('amplitude', 'amplitude.p_surrogate', ('p_surrogate',)),
           ('diversification', 'diversification.gdp_mean', ('gdp_mean', 'p_surrogate')),
           ('diversification', 'diversification.equal', ('equal', 'p_surrogate')),
           ('structure', 'structure.p_align', ('p_align',)), ('structure', 'structure.p_swing', ('p_swing',)),
           ('mst', 'mst.p_contraction', ('p_contraction',)), ('mst', 'mst.p_contraction_detrended', ('p_contraction_detrended',)),
           ('mst', 'mst.p_fragility', ('p_fragility',)), ('phase_lags', 'phase_lags.p_spread_lower', ('p_spread_lower',)),
           ('csd', 'csd.p_ar1', ('p_ar1',)), ('csd', 'csd.p_var', ('p_var',)), ('bifurcation', 'bifurcation.p_slowing', ('p_slowing_post',))]
DATE_FREE = {'amplitude', 'phase_lags'}        # tests that do not use the recession years


def run_config():
    """The S31 Phase 3 settings, with 199 surrogates per test and only convention C among the alternative conventions
    (the past-only lead check); the bootstrap interval of run_arc is description only and gets 200 draws."""
    cfg = paper1.load_run_config(os.path.join(config.repo_root(), RUN_CONFIG))
    for t in cfg['tests'].values():
        if 'surrogates' in t: t['surrogates'] = DESIGN['surrogates']; t['batch'] = DESIGN['surrogates']
    cfg['tests']['arc']['bootstrap'] = 200; cfg['tests']['conventions']['conventions'] = ['C']
    return cfg


# ------------------------------------------------------------------ calibration

def _calib_stats(model, T, Wy, kappa, phi, sigma, mu, m=1.0, n=None, seed=None):
    n = n or DESIGN['n_calib']; rng = np.random.default_rng(seed or DESIGN['seed_calib'])
    sig = S.simulate(model, Wy, T['omega'], kappa, phi, sigma, rng, n, mu=mu)
    z = S.pipeline_z(sig, T, model, m); st = S.stats(z)
    return {k: float(np.mean(v)) for k, v in st.items()} | {'m': float(np.abs(sig).mean())}, z


def _bisect(f, target, lo, hi, steps):
    """Log-scale bisection for an increasing f with f(lo) < target < f(hi); returns (x, f(x), bracketed)."""
    flo, fhi = f(lo), f(hi)
    if not (flo < target < fhi): return (lo, flo, False) if target <= flo else (hi, fhi, False)
    for _ in range(steps):
        mid = np.sqrt(lo * hi); fm = f(mid)
        lo, hi = (mid, hi) if fm < target else (lo, mid)
    x = np.sqrt(lo * hi); return x, f(x), True


def calibrate():
    """Step 1, at kappa = phi = 0: the noise (and for Stuart-Landau mu) whose pipeline phases match S31's median sd of
    annual phase steps (and median swing-size variation): the grid point nearest the target(s). Step 2: m, the mean
    size of the uncoupled annual signal. Step 3: kappa* (phi = 0) and phi* (kappa = 0) whose mean r over 1970-2022
    matches S31's, by bisection. Nothing here uses the recession years."""
    warnings.filterwarnings('ignore'); T = S.targets(); Wy, _ = S.trade_network(); out = {'targets': {k: float(T[k]) for k in ('sd_phase_step', 'cv_amplitude', 'mean_r')}}
    for model in S.MODELS:
        grid = []
        for mu in (DESIGN['mu_grid'] if model == 'stuart_landau' else [0.0]):
            for s in DESIGN['sigma_grid']:
                st, _ = _calib_stats(model, T, Wy, 0.0, 0.0, s, mu)
                d = (st['sd_phase_step'] / T['sd_phase_step'] - 1) ** 2 + ((st['cv_amplitude'] / T['cv_amplitude'] - 1) ** 2 if model == 'stuart_landau' else 0)
                grid.append(dict(mu=mu, sigma=s, distance=d, **st))
        G = pd.DataFrame(grid); best = G.loc[G.distance.idxmin()]; sigma, mu, m = float(best.sigma), float(best.mu), float(best.m)
        res = {'sigma': sigma, 'mu': mu, 'm': m, 'at_kappa0': {k: float(best[k]) for k in ('sd_phase_step', 'cv_amplitude', 'mean_r')},
               'grid': G.to_dict(orient='records')}
        for name, which in (('kappa_star', 'kappa'), ('phi_star', 'phi')):
            f = lambda x: _calib_stats(model, T, Wy, x if which == 'kappa' else 0.0, x if which == 'phi' else 0.0, sigma, mu, m)[0]['mean_r']
            x, fx, ok = _bisect(f, T['mean_r'], *DESIGN['coupling_bracket'], DESIGN['bisection_steps'])
            st, _ = _calib_stats(model, T, Wy, x if which == 'kappa' else 0.0, x if which == 'phi' else 0.0, sigma, mu, m)
            res[name] = float(x); res[f'{name}_bracketed'] = ok; res[f'at_{name}'] = {k: st[k] for k in ('sd_phase_step', 'cv_amplitude', 'mean_r')}
        out[model] = res; print(model, {k: v for k, v in res.items() if k != 'grid'})
    os.makedirs(OUT, exist_ok=True); json.dump(out, open(os.path.join(OUT, 'calibration.json'), 'w'), indent=1)
    r_curve(out, T, Wy)
    return out


def r_curve(cal, T, Wy):
    """Known coupling against what the pipeline sees: mean r (and by decade) for kappa and phi as multiples of the
    calibrated values, 200 worlds each; the real S31 values for comparison."""
    rows = []; dec = [(1970, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2022)]; yrs = np.arange(1970, 2023)
    for model in S.MODELS:
        c = cal[model]
        for which in ('kappa', 'phi'):
            for mult in (0.0, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0):
                k = mult * c['kappa_star'] if which == 'kappa' else 0.0; p = mult * c['phi_star'] if which == 'phi' else 0.0
                st, z = _calib_stats(model, T, Wy, k, p, c['sigma'], c['mu'], c['m'], seed=DESIGN['seed_curve'])
                r = np.abs(np.exp(1j * np.angle(z)).mean(axis=1))
                rows.append(dict(model=model, coupling=which, multiple=mult, kappa=k, phi=p, mean_r=float(r.mean()),
                                 sd_r_across_worlds=float(r.mean(axis=1).std()),
                                 **{f'r_{a}s' if b - a == 9 else f'r_{a}_{b}': float(r[:, (yrs >= a) & (yrs <= b)].mean()) for a, b in dec}))
    from ef import order
    from ef.phases import analytic
    D = paper1.load_data('S31', S.SPAN); r = order.r(analytic(D.logs, D.years, (1970, 2022), 'P'))
    rows.append(dict(model='real S31', coupling='', multiple=np.nan, kappa=np.nan, phi=np.nan, mean_r=float(r.mean()), sd_r_across_worlds=np.nan,
                     **{f'r_{a}s' if b - a == 9 else f'r_{a}_{b}': float(r[(yrs >= a) & (yrs <= b)].mean()) for a, b in dec}))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'r_curve.csv'), index=False, float_format='%.6g')


# ------------------------------------------------------------------ the test runs

_W = {}


def _init():
    warnings.filterwarnings('ignore'); _W['T'] = S.targets(); _W['cfg'] = run_config()


def _get(d, path):
    for k in path: d = d[k]
    return d


def _tests(args):
    """Every Paper 1 test on one world, under the real recession dates (rule A) and the world's own (rule B)."""
    model, cell, w, sig, m = args; T, cfg0 = _W['T'], _W['cfg']
    D = S.to_data(sig, T, model, m); recB, downB = S.world_recessions(D); rows = []
    for rule, rec, down in (('A', list(cfg0['recessions']), list(cfg0['downturns'])), ('B', recB, downB)):
        cfg = dict(cfg0, recessions=rec, downturns=down); res = {}
        for test in dict.fromkeys(t for t, _, _ in PVALUES):
            if rule == 'B' and test in DATE_FREE: continue
            t = dict(cfg['tests'][test])
            if 'seed' in t: t['seed'] = DESIGN['seed_tests'] + 7919 * w + sum(map(ord, test))     # own draws per world and test
            res[test] = paper1.TESTS[test](D, cfg, t)
        for test, label, path in PVALUES:
            if test in res: rows.append((model, cell, w, 'any' if test in DATE_FREE else rule, label, float(_get(res[test], path))))
        if rule == 'B':     # description: r in the world's own recession years and the year before, against all years
            r = res['arc']['r_by_year']; yrs = np.array(sorted(r)); rv = np.array([r[y] for y in yrs])
            st = (model, cell, w, float(rv.mean()), float(np.mean([r[y] for y in recB])), float(np.mean([r[y - 1] for y in recB if y - 1 in r])),
                  float(rv[(yrs >= 1970) & (yrs <= 1995)].mean()), float(rv[yrs >= 2010].mean()))
    return rows, (model, cell, w, recB), st


def run(processes=None):
    cal = json.load(open(os.path.join(OUT, 'calibration.json'))); T = S.targets(); Wy, _ = S.trade_network()
    rows, recs, stats = [], [], []
    with Pool(processes or max(1, (os.cpu_count() or 2) - 1), initializer=_init) as pool:
        for mi, model in enumerate(S.MODELS):
            c = cal[model]
            for ci, (cell, km, pm) in enumerate(CELLS):
                rng = np.random.default_rng([DESIGN['seed_cells'], mi, ci]); sig = []
                for s0 in range(0, DESIGN['n_worlds'], DESIGN['chunk']):
                    nb = min(DESIGN['chunk'], DESIGN['n_worlds'] - s0)
                    sig.append(S.simulate(model, Wy, T['omega'], km * c['kappa_star'], pm * c['phi_star'], c['sigma'], rng, nb, mu=c['mu']))
                sig = np.concatenate(sig)
                for r_, rec, st in pool.imap_unordered(_tests, [(model, cell, w, sig[w], c['m']) for w in range(len(sig))], chunksize=8):
                    rows += r_; recs.append(rec); stats.append(st)
                print(model, cell, 'done', flush=True)
    P = pd.DataFrame(rows, columns=['model', 'cell', 'world', 'rule', 'test', 'p']).sort_values(['model', 'cell', 'world', 'rule', 'test'])
    P.to_csv(os.path.join(OUT, 'pvalues.csv.gz'), index=False, float_format='%.6g', compression={'method': 'gzip', 'mtime': 0})
    R = pd.DataFrame([(m_, c_, w_, ' '.join(map(str, r_))) for m_, c_, w_, r_ in recs], columns=['model', 'cell', 'world', 'rule_B_recessions'])
    R.sort_values(['model', 'cell', 'world']).to_csv(os.path.join(OUT, 'rule_b_recessions.csv.gz'), index=False,
                                                     compression={'method': 'gzip', 'mtime': 0})
    W = pd.DataFrame(stats, columns=['model', 'cell', 'world', 'r_mean', 'r_at_rule_b_recessions', 'r_year_before_rule_b_recessions',
                                     'r_1970_1995', 'r_2010_2022'])
    W.sort_values(['model', 'cell', 'world']).to_csv(os.path.join(OUT, 'world_stats.csv.gz'), index=False, float_format='%.6g',
                                                     compression={'method': 'gzip', 'mtime': 0})


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('step', choices=['calibrate', 'run', 'report']); ap.add_argument('--processes', type=int)
    a = ap.parse_args(argv)
    if a.step == 'calibrate': calibrate()
    elif a.step == 'run': run(a.processes)
    else:
        from ef.gnn import g1_report; g1_report.main()


if __name__ == '__main__':
    main()
