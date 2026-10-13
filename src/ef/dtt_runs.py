"""DTT runs: the reproduction of the report's tables from its stated equations (D1), written to
dtt/results/reproduction.json and dtt/D0_reproduction.md.

    python -m ef.dtt_runs reproduce

Agreement rules (fixed before the run): EXACT, the same number to the digits the report prints (deterministic
quantities only); CLOSE, for Monte Carlo quantities, a two-sided 95% test does not tell the two apart (proportions:
pooled two-proportion z test; medians of tipping times: |difference| <= 1.96 sqrt(SE_report^2 + SE_mine^2), the SEs
bootstrapped from my tipping times at the report's and my own number of tippers; mean R^2: |difference| <=
1.96 sqrt(2) SE_mine, two estimates from 40 ensembles each); DIFFERENT otherwise.
"""
import argparse
import datetime
import json
import os

import numpy as np

from ef import config, dtt
from ef.dtt import Params

OUT = os.path.join(config.repo_root(), 'dtt')
KS = (0.0, 0.8, 4 / 3, 5.6 / 3, 3.2)                       # the report's K values for sections C-E

# the report's tables (dtt/legacy/DTT_Unified_Simulation_Report.pdf)
REPORT = {
    'B': {'K': np.linspace(0, 3.2, 13).round(3).tolist(),
          'mean_R2': [0.0318, 0.0398, 0.0536, 0.0733, 0.0976, 0.1711, 0.3029, 0.4403, 0.6182, 0.7532, 0.8168, 0.8625, 0.8911],
          'theory_var': [0.01591, 0.01988, 0.02679, 0.03664, 0.04878, 0.08555, 0.15144, 0.22015, 0.30912, 0.37659, 0.40838, 0.43126, 0.44554],
          'mc_var': [0.01590, 0.01996, 0.02675, 0.03650, 0.04911, 0.08573, 0.15202, 0.22100, 0.30839, 0.37808, 0.40609, 0.43021, 0.44581],
          'amplification': [0.99, 1.23, 1.66, 2.27, 3.02, 5.30, 9.39, 13.65, 19.17, 23.35, 25.32, 26.74, 27.62],
          'n_eff': [31.42, 25.16, 18.67, 13.65, 10.25, 5.84, 3.30, 2.27, 1.62, 1.33, 1.22, 1.16, 1.12]},
    'C': {'mean_R2': [0.0318, 0.0733, 0.1711, 0.4403, 0.8911], 'k': [2, 118, 422, 500, 500], 'n': 500,
          'median': [9.14, 26.54, 12.51, 4.67, 2.29]},
    'D': {'k': [19, 136, 296, 388, 400], 'n': 400, 'median': [27.71, 21.54, 14.64, 7.67, 3.82],
          'control_k': 13, 'control_n': 4000, 'control_median': 24.72},
    'E': {'n': 800, 'instantaneous': ([22, 263, 590, 773, 800], [23.29, 16.19, 14.13, 7.85, 3.82]),
          'rms_trial': ([5, 161, 531, 767, 800], [18.26, 16.86, 12.79, 5.28, 2.24]),
          'rms_ensemble': ([4, 160, 663, 797, 800], [15.12, 19.28, 13.76, 5.29, 2.21])},
    'F': {'scenario': ['asynchronous (K = 0)', 'intermediate (K = 1.5)', 'strong (K = 2.5)'], 'V': [1.0, 10.7, 27.2],
          'innov_sd': [0.0449, 0.1469, 0.2342], 'stationary_sd': [0.103, 0.337, 0.5372], 'k': [0, 561, 600], 'n': 600,
          'median_steps': [None, 202, 34]},
    'I3': {'up_2.5': 0.9879, 'down_2.5': -0.9829, 'down_0': 0.07983, 'max_gap': 1.970796, 'area': 2.273208,
           'up_jump_g': 0.915, 'down_jump_g': 1.25},
}


def _rng(*k): return np.random.default_rng([dtt.SEED, *k])


def _median_se(times, k_other, rng, nb=2000):
    t = times[~np.isnan(times)]
    if len(t) < 2 or not k_other: return np.nan, np.nan
    se = lambda m: np.std([np.median(rng.choice(t, m)) for _ in range(nb)])
    return se(len(t)), se(int(k_other))


def _prop(k_r, n_r, k_m, n_m):
    return {'report': [int(k_r), int(n_r), k_r / n_r], 'mine': [int(k_m), int(n_m), k_m / n_m], 'wilson_mine': list(dtt.wilson(k_m, n_m)),
            'mark': 'CLOSE' if dtt.same_proportion(k_r, n_r, k_m, n_m) else 'DIFFERENT'}


def _median(m_r, k_r, times, rng):
    t = times[~np.isnan(times)]
    if m_r is None or not len(t): return {'report': m_r, 'mine': float(np.median(t)) if len(t) else None, 'mark': '—'}
    se_m, se_r = _median_se(times, k_r, rng); m = float(np.median(t))
    return {'report': m_r, 'mine': m, 'tolerance': float(1.96 * np.hypot(se_m, se_r)),
            'mark': 'CLOSE' if abs(m - m_r) <= 1.96 * np.hypot(se_m, se_r) else 'DIFFERENT'}


def reproduce():
    res = {'seed': dtt.SEED, 'run_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
    # B: stationary mean R^2 (my choices: dt 0.01, run-in 50, then 200 time units, 40 ensembles)
    B = REPORT['B']; rows = []
    for j, K in enumerate(np.linspace(0, 3.2, 13)):
        r2, R = dtt.stationary_R2(Params(K=float(K), D=0.015, dt=0.01), 40, _rng(1, j))
        se = r2.std(ddof=1) / np.sqrt(len(r2)); m = float(r2.mean())
        phi = _rng(11, j).uniform(0, 2 * np.pi, size=R.shape)          # MC over shock directions: qbar / sigma = R cos(psi - phi)
        mc = float((R.astype(float) * np.cos(phi)).var())
        # the report's own arithmetic: its theoretical variance implies mean R^2; check the other columns against it
        r2_impl = 2 * B['theory_var'][j]
        arith = (abs(31 * r2_impl - B['amplification'][j]) <= 0.006 + 31 * 1e-5 and abs(1 / r2_impl - B['n_eff'][j]) <= 0.006 + 1e-5 / r2_impl ** 2
                 and abs(r2_impl - B['mean_R2'][j]) <= 5e-5 + 1e-5)
        rows.append({'K': round(float(K), 3), 'report_mean_R2': B['mean_R2'][j], 'mine_mean_R2': m, 'se_mine': float(se),
                     'mark': 'CLOSE' if abs(m - B['mean_R2'][j]) <= 1.96 * np.sqrt(2) * se else 'DIFFERENT',
                     'mine_theory_var': m / 2, 'mine_mc_var': mc, 'report_mc_over_theory': B['mc_var'][j] / B['theory_var'][j],
                     'report_arithmetic': 'EXACT' if arith else 'DIFFERENT'})
    res['B'] = rows
    # diagnostic, not part of the marks: a second seed, and the oscillator noise halved, where B differs
    res['B_diagnostic'] = []
    for j, K in [(j, K) for j, K in enumerate(np.linspace(0, 3.2, 13)) if rows[j]['mark'] == 'DIFFERENT']:
        for lab, D_ in (('second seed', 0.015), ('second seed, noise sqrt(D) instead of sqrt(2D)', 0.0075)):
            r2, _ = dtt.stationary_R2(Params(K=float(K), D=D_, dt=0.01), 40, _rng(6, j))
            se = r2.std(ddof=1) / np.sqrt(len(r2))
            res['B_diagnostic'].append({'K': round(float(K), 3), 'variant': lab, 'mean_R2': float(r2.mean()), 'se': float(se),
                                        'within_tolerance': bool(abs(r2.mean() - B['mean_R2'][j]) <= 1.96 * np.sqrt(2) * se)})
    # C: averaged-noise escape, sigma 0.82 (not stated in section C; section D's value), T 40, dt 0.01
    C = REPORT['C']; rows = []
    for j, K in enumerate(KS):
        my_r2 = res['B'][[round(b['K'], 3) for b in res['B']].index(round(K, 3))]['mine_mean_R2']
        for src, r2 in (('report_R2', C['mean_R2'][j]), ('my_R2', my_r2)):
            tip, t = dtt.averaged_noise_escape(Params(K=K), r2, 10_000, _rng(2, j, src == 'my_R2'))
            rows.append({'K': K, 'R2_from': src, 'R2': r2, **{'tipping': _prop(C['k'][j], C['n'], tip.sum(), len(tip))},
                         'median': _median(C['median'][j], C['k'][j], t, _rng(12, j))})
    res['C'] = rows
    # D and E: the dynamic shared-shock model and its constant-RMS controls on common traces; the independent control
    D, E = REPORT['D'], REPORT['E']; rows_d, rows_e = [], []
    for j, K in enumerate(KS):
        out, R = dtt.dynamic(Params(K=K), 4000, _rng(3, j), kinds=('instantaneous', 'rms_trial', 'rms_ensemble'))
        tip, t = out['instantaneous']
        rows_d.append({'K': K, 'tipping': _prop(D['k'][j], D['n'], tip.sum(), len(tip)), 'median': _median(D['median'][j], D['k'][j], t, _rng(13, j)),
                       'mean_R': float(R.mean()), 'mean_R2': float((R.astype(float) ** 2).mean())})
        for kind in ('instantaneous', 'rms_trial', 'rms_ensemble'):
            tip, t = out[kind]; kr, mr = E[kind][0][j], E[kind][1][j]
            rows_e.append({'K': K, 'kind': kind, 'tipping': _prop(kr, E['n'], tip.sum(), len(tip)), 'median': _median(mr, kr, t, _rng(14, j))})
    p0 = Params(); xi = _rng(4).standard_normal((40_000, p0.steps)).astype(np.float32)
    tip, t = dtt.escape(np.full((40_000, 1), p0.sigma / np.sqrt(p0.N)), xi, p0)
    res['D'] = rows_d; res['D_control'] = {'tipping': _prop(D['control_k'], D['control_n'], tip.sum(), len(tip)),
                                           'median': _median(D['control_median'], D['control_k'], t, _rng(15))}
    res['E'] = rows_e
    # F: the stress-threshold prototype from the table's V (the oscillator settings behind V are not stated)
    F = REPORT['F']; rows = []
    for j, V in enumerate(F['V']):
        sd = 0.25 * np.sqrt(V / 31); ev, t = dtt.threshold_events(sd, 6000, _rng(5, j))
        rows.append({'scenario': F['scenario'][j], 'V': V, 'innov_sd': sd, 'innov_sd_report': F['innov_sd'][j],
                     'stationary_sd': sd / np.sqrt(1 - 0.81), 'stationary_sd_report': F['stationary_sd'][j],
                     'events': _prop(F['k'][j], F['n'], ev.sum(), len(ev)), 'median': _median(F['median_steps'][j], F['k'][j], t, _rng(16, j))})
    res['F'] = rows
    # I3 (frozen section, checked because of Sid's question): the mean-field Ising model m = tanh(g m + h)
    res['I3'] = ising_check()
    os.makedirs(os.path.join(OUT, 'results'), exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'results', 'reproduction.json'), 'w'), indent=1, default=float)
    from ef import dtt_text
    open(os.path.join(OUT, 'D0_reproduction.md'), 'w').write(dtt_text.d0(res, REPORT))
    print("wrote dtt/results/reproduction.json and dtt/D0_reproduction.md")
    return res


def ising_check(h=0.08, n=2501):
    """Up-sweep from g = 0 on the low-g branch, down-sweep from the negative branch at g = 2.5; the fold of the
    negative branch solved exactly (m = tanh(g m + h) with g (1 - m^2) = 1)."""
    from scipy.optimize import brentq
    g = np.linspace(0, 2.5, n)

    def follow(gs, m):
        out = []
        for gg in gs:
            for _ in range(100000):
                mn = np.tanh(gg * m + h)
                if abs(mn - m) < 1e-14: break
                m = mn
            out.append(m)
        return np.array(out)
    up = follow(g, 0.0); dn = follow(g[::-1], -1.0)[::-1]
    f = lambda m: np.tanh(m / (1 - m * m) + h) - m              # on the fold g = 1 / (1 - m^2)
    mf = brentq(f, -0.99, -0.05); slope = np.gradient(up, g)
    return {'h': h, 'grid': n, 'up_2.5': float(up[-1]), 'down_2.5': float(dn[-1]), 'down_0': float(dn[0]),
            'max_gap': float((up - dn).max()), 'area': float(np.trapezoid(np.abs(up - dn), g)),
            'steepest_up_g': float(g[slope.argmax()]), 'largest_up_step': float(np.abs(np.diff(up)).max()),
            'largest_down_step_g': float(g[np.abs(np.diff(dn)).argmax()]), 'fold_g': float(1 / (1 - mf * mf)), 'fold_m': float(mf)}


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('step', choices=['reproduce']); a = ap.parse_args(argv)
    if a.step == 'reproduce': reproduce()


if __name__ == '__main__':
    main()
