"""DTT D2: robustness runs of the escape model (dtt/D2_plan.md, committed before any run). Simulation only.

    python -m ef.dtt_d2 run        # -> dtt/results/d2_*.json  (about half an hour; conditions run in parallel)
    python -m ef.dtt_d2 figures    # -> dtt/fig/*.png
    python -m ef.dtt_d2 report     # -> dtt/D2_report.md
"""
import argparse
import json
import os
import warnings
from dataclasses import replace
from multiprocessing import Pool

import numpy as np

from ef import config, dtt
from ef.dtt import Params

OUT = os.path.join(config.repo_root(), 'dtt')
RES = os.path.join(OUT, 'results')
KS = (0.0, 0.8, 4 / 3, 5.6 / 3, 3.2)
SWEEP_K = (0.0, 0.8, 4 / 3, 5.6 / 3)
SWEEPS = {'D': [0.005, 0.01, 0.02, 0.04, 0.08], 'omega_sd': [0.5, 0.75, 1.0, 1.5, 2.0], 'N': [11, 21, 31, 61, 121],
          'mu': [0.0, 0.1, 0.2, 0.3], 'sigma': [0.5, 0.65, 0.82, 1.0, 1.2], 'T': [10.0, 20.0, 40.0, 80.0]}
ABL_K = (0.0, 0.8, 4 / 3, 1.6, 5.6 / 3, 3.2)
ABL_KINDS = ('instantaneous', 'rms_trial', 'rms_ensemble', 'permuted', 'block_permuted', 'independent')
RHOS = tuple(np.round(np.linspace(0, 1, 11), 1))


def _rng(*k): return np.random.default_rng([dtt.SEED, *k])


def rate(tip):
    k, n = int(tip.sum()), len(tip); lo, hi = dtt.wilson(k, n); return {'k': k, 'n': n, 'p': k / n, 'lo': lo, 'hi': hi}


def paired(a, b):
    """a - b for two formulations run on the same traces and increments: mean difference of the per-trial outcomes and
    its 95% interval."""
    d = a.astype(float) - b.astype(float); m = d.mean(); se = d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
    return {'diff': float(m), 'lo': float(m - 1.96 * se), 'hi': float(m + 1.96 * se)}


def unpaired(a, b):
    """Difference of two independent rates with a 95% normal interval."""
    pa, pb = a['p'], b['p']; se = np.sqrt(pa * (1 - pa) / a['n'] + pb * (1 - pb) / b['n'])
    return {'diff': pa - pb, 'lo': pa - pb - 1.96 * se, 'hi': pa - pb + 1.96 * se}


def _median(t): t = t[~np.isnan(t)]; return float(np.median(t)) if len(t) else None


# ------------------------------------------------------------------ 1. convergence

def convergence(K, n=1000, dts=(0.02, 0.01, 0.005, 0.0025), base=Params()):
    """All step sizes side by side with common random numbers: oscillator and state increments drawn at the finest
    step and summed for the coarser ones."""
    rng = _rng(10, int(round(K * 1000))); fine = min(dts); T = base.T; Sf = int(round(T / fine)); N = base.N
    r = [int(round(d / fine)) for d in dts]; S = [Sf // q for q in r]
    om = rng.normal(0, base.omega_sd, (n, N)); th0 = rng.uniform(-np.pi, np.pi, (n, N))
    th = [th0.copy() for _ in dts]; acc = [np.zeros((n, N)) for _ in dts]; drift = [None] * len(dts)
    Rl = [np.empty((n, s), dtype=np.float32) for s in S]; sqf = np.sqrt(fine); sq2D = np.sqrt(2 * base.D)
    for k in range(Sf):
        xi = rng.standard_normal((n, N))
        for l, q in enumerate(r):
            if k % q == 0:
                Z = np.exp(1j * th[l]).mean(axis=1); Rl[l][:, k // q] = np.abs(Z)
                drift[l] = om + K * np.imag(Z[:, None] * np.exp(-1j * th[l]))
            acc[l] += xi
            if (k + 1) % q == 0:
                th[l] = th[l] + drift[l] * dts[l] + sq2D * sqf * acc[l]; acc[l][:] = 0
    xif = rng.standard_normal((n, Sf)).astype(np.float32); out = {}
    for l, (dt_, q) in enumerate(zip(dts, r)):
        p = replace(base, K=K, dt=dt_); xi_l = xif.reshape(n, S[l], q).sum(axis=-1) / np.sqrt(q)
        res = {kind: dtt.escape(dtt.noise_scale(Rl[l], p, kind), xi_l, p)[0] for kind in ('instantaneous', 'rms_trial', 'independent')}
        out[dt_] = {'mean_R': float(Rl[l].mean()), **{k_: rate(v) for k_, v in res.items()}, '_tips': res}
    for dt_ in dts[:-1]:                                    # paired gaps to the finest step
        out[dt_]['gap_to_finest'] = {k_: paired(out[dt_]['_tips'][k_], out[dts[-1]]['_tips'][k_]) for k_ in ('instantaneous', 'rms_trial', 'independent')}
    for dt_ in dts: out[dt_].pop('_tips')
    return {'K': K, 'n': n, 'by_dt': {str(d): v for d, v in out.items()}}


# ------------------------------------------------------------------ 2. sweeps

def _condition(args):
    """One sweep condition: R traces and increments, four formulations on them."""
    param, value, K, idx = args; warnings.filterwarnings('ignore')
    p = replace(Params(), K=K, **{param: (int(value) if param == 'N' else value)}); rng = _rng(20, *idx)
    out, R = dtt.dynamic(p, 2000, rng, kinds=('instantaneous', 'rms_trial', 'block_permuted', 'independent'))
    tips = {k: v[0] for k, v in out.items()}
    return {'param': param, 'value': value, 'K': K, 'mean_R': float(R.mean()), 'mean_R2': float((R.astype(float) ** 2).mean()),
            **{k: rate(v) for k, v in tips.items()}, 'median_inst': _median(out['instantaneous'][1]),
            'inst_minus_rms': paired(tips['instantaneous'], tips['rms_trial']),
            'inst_minus_block': paired(tips['instantaneous'], tips['block_permuted']),
            'inst_minus_independent': paired(tips['instantaneous'], tips['independent'])}


def sweeps(processes=None):
    jobs = [(param, v, K, (pi, vi, ki)) for pi, (param, vals) in enumerate(SWEEPS.items()) for vi, v in enumerate(vals)
            for ki, K in enumerate(SWEEP_K)]
    with Pool(processes or max(1, (os.cpu_count() or 2) - 1)) as pool:
        rows = pool.map(_condition, jobs, chunksize=1)
    for r in rows:                                          # the coupling effect within the same model: K against K = 0
        base = next(x for x in rows if x['param'] == r['param'] and x['value'] == r['value'] and x['K'] == 0.0)
        r['coupling_effect'] = unpaired(r['instantaneous'], base['instantaneous'])
    return rows


# ------------------------------------------------------------------ 3-5. ablation, timing, rho

def _timing(R, tip_t, p, lags=np.arange(0, 10.01, 0.5), n_max=500, rng=None):
    """Superposed R(t) before first passage against R at the same clock times in trials not yet tipped; R's
    autocorrelation time after t = 10."""
    dt = p.dt; k_tip = np.round(tip_t / dt).astype(float); tipped = np.flatnonzero(~np.isnan(tip_t))
    if len(tipped) > n_max: tipped = rng.choice(tipped, n_max, replace=False)
    L = np.round(lags / dt).astype(int); before, ctrl = [], []
    alive_until = np.where(np.isnan(k_tip), np.inf, k_tip)
    for i in tipped:
        k = int(k_tip[i]) - 1; ok = L <= k
        if not ok.all(): continue
        before.append(R[i, k - L]); alive = alive_until > k + 1; alive[i] = False
        ctrl.append(R[alive][:, k - L].mean(axis=0) if alive.any() else np.full(len(L), np.nan))
    b = np.array(before); c = np.array(ctrl)
    # autocorrelation time of R(t) fluctuations after the transient (t > 10)
    seg = R[:, int(10 / dt):].astype(float); seg = seg - seg.mean(axis=1, keepdims=True); var = (seg ** 2).mean()
    ac = [float((seg[:, :seg.shape[1] - m] * seg[:, m:]).mean() / var) for m in range(0, int(10 / dt) + 1, int(0.1 / dt))]
    tau = next((0.1 * i for i, a in enumerate(ac) if a < np.exp(-1)), None)
    return {'lags': lags.tolist(), 'n_tippers': int(len(b)), 'R_before': np.nanmean(b, axis=0).tolist(),
            'R_alive_same_time': np.nanmean(c, axis=0).tolist(), 'autocorr_time': tau}


def ablation(K):
    rng = _rng(30, int(round(K * 1000))); p = Params(K=K)
    out, R = dtt.dynamic(p, 4000, rng, kinds=ABL_KINDS); tips = {k: v[0] for k, v in out.items()}
    res = {'K': K, 'mean_R': float(R.mean()), **{k: {**rate(v[0]), 'median': _median(v[1])} for k, v in out.items()},
           'vs_instantaneous': {k: paired(tips['instantaneous'], tips[k]) for k in ABL_KINDS if k != 'instantaneous'}}
    if K in (0.8, 4 / 3): res['timing'] = _timing(R, out['instantaneous'][1], p, rng=rng)
    return res


def rho_sweep(K):
    rng = _rng(40, int(round(K * 1000))); p = Params(K=K)
    R = dtt.kuramoto_R(p, 2000, rng); xi = rng.standard_normal((2000, p.steps)).astype(np.float32); rows = []
    for rho in RHOS:
        q = replace(p, rho=float(rho))
        a = dtt.escape(dtt.noise_scale(R, q), xi, q)[0]; b = dtt.escape(dtt.noise_scale(R, q, 'rms_trial'), xi, q)[0]
        rows.append({'rho': float(rho), 'instantaneous': rate(a), 'rms_trial': rate(b), 'inst_minus_rms': paired(a, b)})
    return {'K': K, 'rows': rows}


def run_rho(processes=None):
    """The rho sweep alone (rerun on 14 October 2026 after the constant-RMS control was fixed for rho < 1)."""
    with Pool(processes or max(1, (os.cpu_count() or 2) - 1)) as pool: rho = pool.map(rho_sweep, SWEEP_K)
    json.dump(rho, open(os.path.join(RES, 'd2_rho.json'), 'w'), indent=1)


def run(processes=None):
    os.makedirs(RES, exist_ok=True); warnings.filterwarnings('ignore')
    with Pool(processes or max(1, (os.cpu_count() or 2) - 1)) as pool:
        conv = pool.map(convergence, KS); abl = pool.map(ablation, ABL_K); rho = pool.map(rho_sweep, SWEEP_K)
    json.dump(conv, open(os.path.join(RES, 'd2_convergence.json'), 'w'), indent=1)
    json.dump(abl, open(os.path.join(RES, 'd2_ablation.json'), 'w'), indent=1)
    json.dump(rho, open(os.path.join(RES, 'd2_rho.json'), 'w'), indent=1)
    print('convergence, ablation, rho done', flush=True)
    sw = sweeps(processes); json.dump(sw, open(os.path.join(RES, 'd2_sweeps.json'), 'w'), indent=1)
    print('sweeps done', flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('step', choices=['run', 'rho', 'figures', 'report']); ap.add_argument('--processes', type=int)
    a = ap.parse_args(argv)
    if a.step == 'run': run(a.processes)
    elif a.step == 'rho': run_rho(a.processes)
    elif a.step == 'figures':
        from ef import dtt_figs; dtt_figs.main()
    else:
        from ef import dtt_text; dtt_text.write_d2()


if __name__ == '__main__':
    main()
