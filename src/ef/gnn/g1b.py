"""G1b (docs/preregistration_G1b_dtt.md, amendment 1 of 15 October 2026): a synchrony-driven escape layer on the G1
Kuramoto worlds. Does it reproduce Paper 1's past-only lead-1?

The layer is a bistable state driven by noise whose size follows the worlds' true synchrony,

  dx = (mu + x - x^3) dt / tau + g(t) dW / sqrt(tau),  g(t) = sigma r(t),  r(t) = |mean_i exp(i theta_i(t))|,

integrated beside the oscillators (Euler, dt = 0.01 years) from 1950 at the lower equilibrium. Reaching x = 0 is an
escape: the state is reset at once to the lower equilibrium, and the year is a recession year unless one was counted
in the previous `refractory` years (only 1970-2022 count). sigma is calibrated to five recession years in 1970-2022 on
average over worlds that are not the test worlds. The worlds are the G1 worlds themselves (same seeds and chunks); the
tests run on the pipeline phases of their simulated GDP, exactly as for the real data. Only the recession dates
change between layers, so each world's pipeline r(t) (conventions P and C) is computed once.

    python -m ef.gnn.g1b run      # -> gnn/G1b/ (about 15 minutes)
    python -m ef.gnn.g1b report   # -> gnn/G1b_report.md
"""
import argparse
import json
import os
import warnings
from multiprocessing import Pool

import numpy as np
import pandas as pd

from ef import config, crisis, dtt, order, paper1
from ef.gnn import g1, simulator as S
from ef.phases import analytic

OUT = os.path.join(config.repo_root(), 'gnn', 'G1b')
CACHE = os.path.join(config.repo_root(), 'build', 'gnn', 'g1b')
FROM, WINDOW, SPY = 1950, (1970, 2022), int(round(1 / S.DT))
YEARS = np.arange(FROM, WINDOW[1] + 1); WYEARS = np.arange(WINDOW[0], WINDOW[1] + 1); STEPS = len(YEARS) * SPY
DESIGN = {'n_worlds': 1000, 'n_calib': 500, 'chunk': g1.DESIGN['chunk'], 'target': 5.0, 'share': 0.5,
          'sigma_bracket': [0.02, 20.0], 'bisection_steps': 16, 'alpha': 0.05,
          'seed_worlds': g1.DESIGN['seed_cells'], 'seed_calib_worlds': 5001, 'seed_calib_noise': 5002,
          'seed_noise': 6001, 'seed_shuffle': 6101, 'seed_shuffle_calib': 6102}
SETTINGS = {'network': 3, 'null': 0, 'forcing': 1}          # name -> G1 cell index (g1.CELLS)
PRIMARY = {'layer': 'world', 'measure': 'r', 'mu': 0.2, 'refractory': 2, 'tau': 1.0}
VARIANTS = {'primary': {}, 'per_economy': {'layer': 'economy'}, 'weighted': {'measure': 'ZA'}, 'mu0.1': {'mu': 0.1},
            'mu0.3': {'mu': 0.3}, 'refractory0': {'refractory': 0}, 'refractory4': {'refractory': 4},
            'tau0.5': {'tau': 0.5}, 'tau2': {'tau': 2.0}}
KINDS = ('layer', 'constant', 'shuffled')
ARC = [l for l, _, _ in crisis.ARC]
P_REAL = 2 / 53                                            # the real past-only lead-1 p; also the largest p <= 0.05


def _rng(*k): return np.random.default_rng(list(k))


def spec(variant): return {**PRIMARY, **VARIANTS[variant]}


# ------------------------------------------------------------------ the worlds and their true phases

class Recorder:
    """hook for simulator.simulate: the true r(t) and |mean_i A_i exp(i theta_i)| at every step from 1950, and (if
    asked) the phases themselves, wrapped to [0, 2 pi) in float16, steps first (steps, worlds, economies)."""

    def __init__(self, n, A, n_econ, theta=False):
        self.A = A; self.r = np.empty((n, STEPS), np.float32); self.za = np.empty((n, STEPS), np.float32)
        self.th = np.empty((STEPS, n, n_econ), np.float16) if theta else None; self.rows = slice(0, n); self.k = 0

    def start(self, rows): self.rows = rows; self.k = 0

    def __call__(self, y, th):
        if y < FROM: return
        u = np.exp(1j * th); self.r[self.rows, self.k] = np.abs(u.mean(axis=1)); self.za[self.rows, self.k] = np.abs((self.A * u).mean(axis=1))
        if self.th is not None: self.th[self.k, self.rows] = np.mod(th, 2 * np.pi)
        self.k += 1


def worlds(setting, n, seed, theta=False):
    """The Kuramoto worlds of a G1 cell, simulated in G1's chunks from one generator (so seed [2001, 0, cell] gives the
    G1 worlds), with their true phases recorded. Returns (annual signals, Recorder)."""
    cal = json.load(open(os.path.join(g1.OUT, 'calibration.json')))['kuramoto']; T = S.targets(); Wy, _ = g1.network()
    _, km, pm = g1.CELLS[SETTINGS[setting]]; rng = np.random.default_rng(seed)
    rec = Recorder(n, T['A'], len(T['omega']), theta); sig = []
    for s0 in range(0, n, DESIGN['chunk']):
        nb = min(DESIGN['chunk'], n - s0); rec.start(slice(s0, s0 + nb))
        sig.append(S.simulate('kuramoto', Wy, T['omega'], km * cal['kappa_star'], pm * cal['phi_star'], cal['sigma'], rng, nb, mu=cal['mu'], hook=rec))
        assert rec.k == STEPS
    return np.concatenate(sig), rec


def pipeline_r(sig_w, T=None, band=None):
    """A world's pipeline r(t), 1970-2022, under convention P (as the two-sided arc) and C (as the past-only arc)."""
    T = T or S.targets(); band = band or g1.run_config()['band']; D = S.to_data(sig_w, T, 'kuramoto')
    return order.r(paper1.signal(D, WINDOW, 'P', band)), order.r(analytic(D.logs, D.years, WINDOW, 'C', band))


# ------------------------------------------------------------------ the escape layer

def block_permutation(n, rng):
    """One permutation of the years 1950-2022 per world."""
    return np.argsort(rng.random((n, len(YEARS))), axis=1)


def shuffle_steps(x, perm):
    """x (worlds, steps[, ...]) with each world's one-year blocks reordered by its permutation."""
    s = x.reshape(x.shape[0], len(YEARS), SPY, *x.shape[2:])
    return np.take_along_axis(s, perm.reshape(perm.shape + (1,) * (s.ndim - 2)), axis=1).reshape(x.shape)


def world_layer(g, mu, tau, seed):
    """Escapes of the world-level state. g: (worlds, steps) noise size. Returns (worlds, years 1950-2022) booleans."""
    n = g.shape[0]; rng = np.random.default_rng(seed); x_lo = dtt.equilibria(mu)[0]; a = S.DT / tau; b = np.sqrt(S.DT / tau)
    x = np.full(n, x_lo); esc = np.zeros((n, len(YEARS)), bool)
    for k in range(STEPS):
        x = x + (mu + x - x ** 3) * a + g[:, k] * b * rng.standard_normal(n)
        hit = x >= 0
        if hit.any(): esc[hit, k // SPY] = True; x[hit] = x_lo
    return esc


def economy_layer(theta, sigma, mu, tau, seed, share=DESIGN['share'], perm=None, c=None):
    """Escapes of one state per economy: dx_i = (mu + x_i - x_i^3) dt/tau + sigma v_i . dW / sqrt(tau), v_i = (cos, sin)
    of the true phase, W one common two-dimensional Brownian motion; theta is (steps, worlds, economies). A year is
    flagged when at least `share` of the economies escape in it. perm: shuffled control (whole phase vectors moved by
    one-year blocks). c (per world): constant control, noise sigma (sqrt(c) dW_0 + sqrt(1 - c) dW_i). The same
    increments drive all three."""
    _, n, N = theta.shape; rng = np.random.default_rng(seed); x_lo = dtt.equilibria(mu)[0]; a = S.DT / tau; b = sigma * np.sqrt(S.DT / tau)
    x = np.full((n, N), x_lo); hit_year = np.zeros((n, N), bool); out = np.zeros((n, len(YEARS)), bool); w = np.arange(n)
    for k in range(STEPS):
        xi = rng.standard_normal((n, N + 2))
        if c is not None:
            noise = np.sqrt(c)[:, None] * xi[:, :1] + np.sqrt(1 - c)[:, None] * xi[:, 2:]
        else:
            th = theta[k] if perm is None else theta[perm[:, k // SPY] * SPY + k % SPY, w]
            th = th.astype(np.float64); noise = np.cos(th) * xi[:, :1] + np.sin(th) * xi[:, 1:2]
        x = x + (mu + x - x ** 3) * a + b * noise
        hit = x >= 0; hit_year |= hit; x[hit] = x_lo
        if (k + 1) % SPY == 0: out[:, k // SPY] = hit_year.mean(axis=1) >= share; hit_year[:] = False
    return out


def recessions(esc, refractory):
    """Recession years in 1970-2022 from yearly escape flags: a flagged year counts unless a counted year lies in the
    previous `refractory` years; flags before 1970 neither count nor block. Returns (worlds, 53) booleans."""
    e = esc[:, YEARS >= WINDOW[0]]; out = np.zeros_like(e); last = np.full(e.shape[0], -10 ** 6)
    for j in range(e.shape[1]):
        c = e[:, j] & (j - last > refractory); out[c, j] = True; last[c] = j
    return out


def alignment_share(r, N):
    """c for the per-economy constant control: the world's mean pairwise alignment (N r^2 - 1)/(N - 1), at least 0."""
    return np.clip(((N * r.astype(np.float64) ** 2 - 1) / (N - 1)).mean(axis=1), 0.0, 1.0)


def layer_recessions(sp, kind, sigma, data, seed):
    """Recession years (worlds, 53) of one layer and kind at noise size sigma on a set of worlds (data: dict with r, za,
    theta, perm)."""
    if sp['layer'] == 'world':
        base = data['za'] if sp['measure'] == 'ZA' else data['r']
        g = np.ones_like(base) if kind == 'constant' else shuffle_steps(base, data['perm']) if kind == 'shuffled' else base
        esc = world_layer(sigma * g, sp['mu'], sp['tau'], seed)
    else:
        N = len(S.targets()['omega']); th = data['theta']() if kind != 'constant' else np.empty((STEPS, len(data['r']), N), np.float16)
        esc = economy_layer(th, sigma, sp['mu'], sp['tau'], seed, perm=data['perm'] if kind == 'shuffled' else None,
                            c=alignment_share(data['r'], N) if kind == 'constant' else None)
    return recessions(esc, sp['refractory'])


def calibrate(sp, kind, data, seed):
    """sigma whose mean number of recession years in 1970-2022 is the target, by log-scale bisection with common random
    numbers (g1._bisect). Uses only how many recession years there are, never which."""
    f = lambda s: float(layer_recessions(sp, kind, s, data, seed).sum(axis=1).mean())
    s, fs, ok = g1._bisect(f, DESIGN['target'], *DESIGN['sigma_bracket'], DESIGN['bisection_steps'])
    return {'sigma': float(s), 'mean_recessions': fs, 'bracketed': bool(ok)}


# ------------------------------------------------------------------ the run

def _load(setting, which):
    z = np.load(os.path.join(CACHE, f'{setting}_{which}.npz')); d = {k: z[k] for k in ('r', 'za', 'perm')}
    f = os.path.join(CACHE, f'{setting}_{which}_theta.npy')
    d['theta'] = (lambda: np.load(f)) if os.path.exists(f) else None          # loaded only when a layer needs it
    return d


_W = {}          # per-process state for the worker pools


def _simulate(args):
    """Worker: simulate one set of worlds (the G1 test worlds or the calibration worlds) and cache their true r(t),
    Abar R_A(t), block permutations and (for the trade-coupled setting) phases."""
    setting, which = args; warnings.filterwarnings('ignore'); ci = SETTINGS[setting]; theta = setting == 'network'
    if which == 'test':
        n, seed, sseed = DESIGN['n_worlds'], [DESIGN['seed_worlds'], 0, ci], [DESIGN['seed_shuffle'], ci]
    else:
        n, seed, sseed = DESIGN['n_calib'], [DESIGN['seed_calib_worlds'], ci], [DESIGN['seed_shuffle_calib'], ci]
    sig, rec = worlds(setting, n, seed, theta)
    np.savez(os.path.join(CACHE, f'{setting}_{which}.npz'), r=rec.r, za=rec.za, perm=block_permutation(n, _rng(*sseed)), sig=sig)
    if theta: np.save(os.path.join(CACHE, f'{setting}_{which}_theta.npy'), rec.th)
    return setting, which


def g1_identity():
    """Check that the G1b test worlds are the G1 worlds: each world's own recession dates (G1 rule B, from its simulated
    world GDP) must equal those G1 stored for the same world. Writes gnn/G1b/g1_identity.json."""
    T = S.targets(); B = pd.read_csv(os.path.join(g1.OUT, 'rule_b_recessions.csv.gz')); out = {}
    for s, ci in SETTINGS.items():
        sig = np.load(os.path.join(CACHE, f'{s}_test.npz'))['sig']; cell = g1.CELLS[ci][0]
        ref = B[(B.model == 'kuramoto') & (B.cell == cell)].set_index('world').rule_B_recessions
        same = sum(' '.join(map(str, S.world_recessions(S.to_data(sig[w], T, 'kuramoto'))[0])) == ref[w] for w in range(len(sig)))
        out[s] = {'g1_cell': cell, 'worlds': len(sig), 'rule_b_dates_identical': int(same)}
    json.dump(out, open(os.path.join(OUT, 'g1_identity.json'), 'w'), indent=1); print(out, flush=True)


def _pipeline(args):
    warnings.filterwarnings('ignore'); setting, w, sig_w = args
    if 'T' not in _W: _W['T'] = S.targets(); _W['band'] = g1.run_config()['band']
    rP, rC = pipeline_r(sig_w, _W['T'], _W['band']); return setting, w, rP, rC


def _job(args):
    """Worker: calibrate one (setting, variant, kind) on the calibration worlds, then date the test worlds' recessions."""
    setting, variant, kind = args; warnings.filterwarnings('ignore'); sp = spec(variant); li = 0 if sp['layer'] == 'world' else 1
    ci = SETTINGS[setting]; cal = calibrate(sp, kind, _load(setting, 'calib'), [DESIGN['seed_calib_noise'], ci, li])
    rec = layer_recessions(sp, kind, cal['sigma'], _load(setting, 'test'), [DESIGN['seed_noise'], ci, li])
    return setting, variant, kind, cal, rec


def jobs():
    return [(s, v, k) for s in SETTINGS for v in (VARIANTS if s == 'network' else ['primary']) for k in KINDS]


def _arcs(args):
    """Worker: both arcs of a batch of worlds under their recession years. A world whose statistic is undefined (no
    recession year among the years the lag uses) cannot reject: p = 1, flagged."""
    setting, variant, kind, ws, recs, rP, rC = args; warnings.filterwarnings('ignore'); rows = []
    for w, rec, a, b in zip(ws, recs, rP, rC):
        ev = WYEARS[rec].tolist()
        for conv, r in (('P', a), ('C', b)):
            arc = crisis.arc(r, WYEARS, ev) if ev else {}
            for lab in ARC:
                c = arc.get(lab, {}).get('corr', np.nan); undefined = not np.isfinite(c)
                rows.append((setting, variant, kind, int(w), conv, lab, len(ev), np.nan if undefined else c,
                             1.0 if undefined else arc[lab]['p'], undefined))
    return rows


def run(processes=None):
    os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True); warnings.filterwarnings('ignore')
    procs = processes or max(1, (os.cpu_count() or 2) - 1)
    with Pool(min(procs, 6)) as pool:                                     # 1. worlds
        pool.map(_simulate, [(s, w) for s in SETTINGS for w in ('test', 'calib')], chunksize=1)
    print('worlds simulated', flush=True)
    g1_identity()
    sig = {s: np.load(os.path.join(CACHE, f'{s}_test.npz'))['sig'] for s in SETTINGS}   # 2. pipeline r once per world
    rP = {s: np.empty((DESIGN['n_worlds'], len(WYEARS))) for s in SETTINGS}; rC = {s: np.empty_like(rP[s]) for s in SETTINGS}
    with Pool(procs) as pool:
        for s, w, a, b in pool.imap_unordered(_pipeline, [(s, w, sig[s][w]) for s in SETTINGS for w in range(DESIGN['n_worlds'])], chunksize=16):
            rP[s][w] = a; rC[s][w] = b
    np.savez_compressed(os.path.join(OUT, 'pipeline_r.npz'), years=WYEARS, **{f'{s}_{c}': (rP if c == 'P' else rC)[s] for s in SETTINGS for c in 'PC'})
    true_r = {s: np.load(os.path.join(CACHE, f'{s}_test.npz'))['r'].reshape(DESIGN['n_worlds'], len(YEARS), SPY).mean(axis=2)[:, YEARS >= WINDOW[0]] for s in SETTINGS}
    np.savez_compressed(os.path.join(OUT, 'true_r_annual.npz'), years=WYEARS, **true_r)
    print('pipeline phases done', flush=True)
    with Pool(procs) as pool:                                             # 3. layers: calibrate, date recessions
        res = pool.map(_job, jobs(), chunksize=1)
    cal = [dict(setting=s, variant=v, kind=k, **c) for s, v, k, c, _ in res]
    pd.DataFrame(cal).to_csv(os.path.join(OUT, 'calibration.csv'), index=False, float_format='%.6g')
    R = pd.DataFrame([(s, v, k, w, ' '.join(map(str, WYEARS[rec[w]]))) for s, v, k, _, rec in res for w in range(len(rec))],
                     columns=['setting', 'variant', 'kind', 'world', 'recessions'])
    R.to_csv(os.path.join(OUT, 'recessions.csv.gz'), index=False, compression={'method': 'gzip', 'mtime': 0})
    print('layers done', flush=True)
    args = [(s, v, k, np.arange(i, min(i + 100, len(rec))), rec[i:i + 100], rP[s][i:i + 100], rC[s][i:i + 100])
            for s, v, k, _, rec in res for i in range(0, len(rec), 100)]
    with Pool(procs) as pool:                                             # 4. the arcs
        rows = [r for part in pool.imap(_arcs, args, chunksize=2) for r in part]
    P = pd.DataFrame(rows, columns=['setting', 'variant', 'kind', 'world', 'convention', 'lag', 'n_recessions', 'corr', 'p', 'undefined'])
    P.to_csv(os.path.join(OUT, 'pvalues.csv.gz'), index=False, float_format='%.6g', compression={'method': 'gzip', 'mtime': 0})
    json.dump({'design': DESIGN, 'primary': PRIMARY, 'variants': VARIANTS, 'settings': SETTINGS, 'code_version': paper1.code_version()},
              open(os.path.join(OUT, 'design.json'), 'w'), indent=1, default=str)
    summarize()


# ------------------------------------------------------------------ summaries

def _paired(a, b):
    d = a.astype(float) - b.astype(float); m = d.mean(); se = d.std(ddof=1) / np.sqrt(len(d))
    return float(m), float(m - 1.96 * se), float(m + 1.96 * se)


def real_values():
    """The real S31 values the worlds are compared with: past-only and two-sided arcs (results/S31/P/)."""
    c = json.load(open(os.path.join(config.repo_root(), 'results', 'S31', 'P', 'conventions.json')))['results']['C']['arc']
    a = json.load(open(os.path.join(config.repo_root(), 'results', 'S31', 'P', 'arc.json')))['results']['arc']
    return {'C': {l: {'corr': c[l]['corr'], 'p': c[l]['p']} for l in ARC}, 'P': {l: {'corr': a[l]['corr'], 'p': a[l]['p']} for l in ARC}}


def summarize():
    """gnn/G1b/rejections.csv (every setting, variant, kind, convention and lag), verdicts.json (the pre-registered
    verdict for every setting and variant), p_distribution.csv, counts.csv and describe.csv."""
    P = pd.read_csv(os.path.join(OUT, 'pvalues.csv.gz')); real = real_values(); eps = 1e-9
    P['reject'] = P.p <= DESIGN['alpha'] + eps; P['at_real_p'] = P.p <= P_REAL + eps
    rows = []
    for (s, v, k, c, l), g in P.groupby(['setting', 'variant', 'kind', 'convention', 'lag'], sort=False):
        n = len(g); kk = int(g.reject.sum()); lo, hi = dtt.wilson(kk, n); mid = g[g.n_recessions.between(4, 6)]
        rows.append(dict(setting=s, variant=v, kind=k, convention=c, lag=l, worlds=n, rejections=kk, rate=kk / n, lo=lo, hi=hi,
                         at_real_p=float(g.at_real_p.mean()), corr_at_least_real=float((g['corr'] >= real[c][l]['corr'] - eps).mean()),
                         undefined=int(g.undefined.sum()), worlds_4_6=len(mid), rate_4_6=float(mid.reject.mean()) if len(mid) else np.nan,
                         mean_corr=float(g['corr'].mean())))
    Rj = pd.DataFrame(rows); Rj.to_csv(os.path.join(OUT, 'rejections.csv'), index=False, float_format='%.6g')
    verdicts = []
    for (s, v), g in P[(P.convention == 'C') & (P.lag == 'lead1')].groupby(['setting', 'variant'], sort=False):
        x = {k: g[g.kind == k].sort_values('world').reject.to_numpy() for k in KINDS}
        kk = int(x['layer'].sum()); n = len(x['layer']); lo, hi = dtt.wilson(kk, n)
        dc, dc_lo, dc_hi = _paired(x['layer'], x['constant']); ds, ds_lo, ds_hi = _paired(x['layer'], x['shuffled'])
        share = float(g[g.kind == 'layer'].at_real_p.mean())
        a, b, c = lo > P_REAL, dc_lo > 0 and ds_lo > 0, share >= 0.20
        verdicts.append(dict(setting=s, variant=v, rate=kk / n, lo=lo, hi=hi, a=bool(a), diff_constant=[dc, dc_lo, dc_hi],
                             diff_shuffled=[ds, ds_lo, ds_hi], b=bool(b), share_at_real_p=share, c=bool(c),
                             verdict='reproduced' if a and b and c else 'partly' if a and b else 'not reproduced'))
    json.dump(verdicts, open(os.path.join(OUT, 'verdicts.json'), 'w'), indent=1)
    d = P[(P.convention == 'C') & (P.lag == 'lead1')]                          # the full p distribution, past-only lead-1
    D = d.assign(k=np.round(d.p * 53).astype(int)).groupby(['setting', 'variant', 'kind', 'k']).size().rename('worlds').reset_index()
    D['p'] = D.k / 53; D.to_csv(os.path.join(OUT, 'p_distribution.csv'), index=False, float_format='%.6g')
    rec = pd.read_csv(os.path.join(OUT, 'recessions.csv.gz'), keep_default_na=False)
    rec['n'] = rec.recessions.map(lambda x: len(x.split()) if x else 0)
    rec.groupby(['setting', 'variant', 'kind', 'n']).size().rename('worlds').reset_index().to_csv(os.path.join(OUT, 'counts.csv'), index=False)
    pr = np.load(os.path.join(OUT, 'pipeline_r.npz')); tr = np.load(os.path.join(OUT, 'true_r_annual.npz')); rows = []
    for (s, v, k), g in rec.groupby(['setting', 'variant', 'kind'], sort=False):
        M = np.zeros((len(g), len(WYEARS)), bool)
        for i, x in enumerate(g.sort_values('world').recessions):
            if x: M[i, np.searchsorted(WYEARS, list(map(int, x.split())))] = True
        B = np.zeros_like(M); B[:, :-1] = M[:, 1:]; O = ~M & ~B
        for name, X in (('true r', tr[s]), ('pipeline r (P)', pr[f'{s}_P']), ('pipeline r (C)', pr[f'{s}_C'])):
            rows.append(dict(setting=s, variant=v, kind=k, measure=name, recession=float(X[M].mean()), year_before=float(X[B].mean()), other=float(X[O].mean())))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'describe.csv'), index=False, float_format='%.6g')


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('step', choices=['run', 'summarize', 'report']); ap.add_argument('--processes', type=int)
    a = ap.parse_args(argv)
    if a.step == 'run': run(a.processes)
    elif a.step == 'summarize': summarize()
    else:
        from ef.gnn import g1b_report; g1b_report.main()


if __name__ == '__main__':
    main()
