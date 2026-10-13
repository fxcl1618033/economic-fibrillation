"""DTT figures (dtt/fig/), regenerated from this code with the project palette. The report's own figures stay in
dtt/legacy/figures_extracted/. Inter is the project font; where it is not installed matplotlib falls back to DejaVu
Sans.

    python -m ef.dtt_d2 figures
"""
import json
import os
import warnings

import numpy as np

from ef import config, dtt
from ef.dtt import Params

OUT = os.path.join(config.repo_root(), 'dtt')
FIG, RES = os.path.join(OUT, 'fig'), os.path.join(OUT, 'results')
BLUE, ORANGE, AQUA, YELLOW, VIOLET, RED, GREY, LIGHT = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#4a3aa7', '#e34948', '#898781', '#c3c2b7'
KCOL = [GREY, BLUE, AQUA, ORANGE, RED, VIOLET]


def _plt():
    import matplotlib
    matplotlib.use('Agg'); import matplotlib.pyplot as plt
    warnings.filterwarnings('ignore', module='matplotlib')
    plt.rcParams.update({'font.family': ['Inter', 'DejaVu Sans'], 'font.size': 9, 'axes.titlesize': 10, 'axes.titleweight': 'bold',
                         'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e5df',
                         'grid.linewidth': 0.6, 'legend.frameon': False, 'figure.dpi': 150, 'savefig.bbox': 'tight'})
    return plt


def _save(fig, name):
    os.makedirs(FIG, exist_ok=True); fig.savefig(os.path.join(FIG, name)); import matplotlib.pyplot as plt; plt.close(fig)


def _err(r): return np.clip(np.array([[r['p'] - r['lo']], [r['hi'] - r['p']]]) * 100, 0, None)


def _c(a): return np.clip(np.asarray(a, dtype=float), 0, None)       # error bars never below zero (rounding at 0% and 100%)


def reproduced(plt, rep):
    from ef.dtt_runs import REPORT
    B = rep['B']; K = [b['K'] for b in B]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.errorbar(K, [b['mine_mean_R'] for b in B], yerr=[b['mine_sd_R_between'] for b in B], color=BLUE, marker='o', ms=4, capsize=2,
                label='mean R ± between-ensemble s.d. (40 ensembles)')
    ax.set(xlabel='Coupling K', ylabel='Order parameter R', title='B1. Synchronization of 31 noisy oscillators', ylim=(0, 1)); ax.legend(loc='upper left')
    _save(fig, 'B1_synchronization.png')
    fig, ax = plt.subplots(figsize=(6.4, 3.6)); ax2 = ax.twinx()
    ax.plot(K, [31 * b['mine_mean_R2'] for b in B], color=BLUE, marker='o', ms=4, label='amplification N·E[R²]')
    ax.plot(K, [31 * x for x in REPORT['B']['mean_R2']], color=LIGHT, marker='o', ms=3, ls='none', label='report')
    ax2.plot(K, [1 / b['mine_mean_R2'] for b in B], color=ORANGE, marker='s', ms=4, label='N_eff = 1/E[R²]')
    ax2.plot(K, REPORT['B']['n_eff'], color=LIGHT, marker='s', ms=3, ls='none')
    ax.set(xlabel='Coupling K', ylabel='World variance ÷ independent baseline', title='B2. Loss of diversification from vector summation')
    ax2.set_ylabel('Effective number of economies', color=ORANGE); ax2.spines['right'].set_visible(True); ax2.grid(False)
    h = ax.get_legend_handles_labels(); h2 = ax2.get_legend_handles_labels(); ax.legend(h[0] + h2[0], h[1] + h2[1], loc='center right')
    _save(fig, 'B2_amplification_neff.png')
    # C2: averaged-noise escape, both R^2 sources
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for src, col, lab in (('report_R2', ORANGE, "the report's E[R²]"), ('my_R2', BLUE, 'my E[R²] (section B)')):
        rows = [r for r in rep['C'] if r['R2_from'] == src]
        ax.errorbar([r['K'] for r in rows], [100 * r['tipping']['mine'][2] for r in rows],
                    yerr=_c([[100 * (r['tipping']['mine'][2] - r['tipping']['wilson_mine'][0]) for r in rows],
                                   [100 * (r['tipping']['wilson_mine'][1] - r['tipping']['mine'][2]) for r in rows]]),
                    color=col, marker='o', ms=4, capsize=2, label=lab)
    ax.plot([r['K'] for r in rep['C'] if r['R2_from'] == 'report_R2'], [100 * r['tipping']['report'][2] for r in rep['C'] if r['R2_from'] == 'report_R2'],
            color=GREY, marker='x', ls='none', label='report (500 trials)')
    ax.set(xlabel='Coupling K', ylabel='Tipping by t = 40, %', title='C2. Escape with averaged noise σ√E[R²], σ = 0.82'); ax.legend()
    _save(fig, 'C2_averaged_noise.png')


def dynamic_figs(plt, rep, abl):
    from ef.dtt_runs import REPORT
    Ks = [d['K'] for d in rep['D']]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.errorbar(Ks, [100 * d['tipping']['mine'][2] for d in rep['D']],
                yerr=_c([[100 * (d['tipping']['mine'][2] - d['tipping']['wilson_mine'][0]) for d in rep['D']],
                               [100 * (d['tipping']['wilson_mine'][1] - d['tipping']['mine'][2]) for d in rep['D']]]),
                color=BLUE, marker='o', ms=4, capsize=2, label='shared shock, g = σR(t) (4,000 trials)')
    ax.plot(Ks, [100 * k / REPORT['D']['n'] for k in REPORT['D']['k']], color=GREY, marker='x', ls='none', label='report (400 trials)')
    c = rep['D_control']['tipping']['mine'][2]
    ax.axhline(100 * c, color=ORANGE, lw=1.2, label=f'independent noise σ/√N ({100 * c:.2f}%)')
    ax.set(xlabel='Coupling K', ylabel='Tipping by t = 40, %', title='D1. Dynamic shared-shock model and the independent-noise control'); ax.legend()
    _save(fig, 'D1_dynamic.png')
    # D2: example paths
    p0 = Params(); fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.2), sharex=True)
    for j, K in enumerate((0.0, 0.8, 4 / 3, 5.6 / 3, 3.2)):
        p = Params(K=K); rng = np.random.default_rng([dtt.SEED, 60, j]); R = dtt.kuramoto_R(p, 1, rng)[0].astype(float)
        xi = rng.standard_normal(p.steps); x = np.empty(p.steps + 1); x[0] = p.x0
        for k in range(p.steps): x[k + 1] = x[k] + (p.mu + x[k] - x[k] ** 3) * p.dt + p.sigma * R[k] * np.sqrt(p.dt) * xi[k]
        t = np.arange(p.steps + 1) * p.dt
        a1.plot(t, x, color=KCOL[j], lw=0.7, label=f'K = {K:.3g}'); a2.plot(t[:-1], R, color=KCOL[j], lw=0.8)
    a1.axhline(0, color='black', lw=0.8, ls='--'); a1.axhline(p0.x0, color=GREY, lw=0.8, ls=':')
    a1.set(ylabel='State x(t)', title='D2. Example paths: state (top) and synchrony R(t) (bottom)'); a1.legend(ncol=5, fontsize=7, loc='upper left')
    a2.set(xlabel='Model time', ylabel='R(t)'); _save(fig, 'D2_example_paths.png')
    # E1: instantaneous vs constant RMS (same traces)
    fig, ax = plt.subplots(figsize=(6.4, 3.6)); w = 0.25; x = np.arange(len(Ks))
    for i, (kind, col, lab) in enumerate((('instantaneous', BLUE, 'σR(t)'), ('rms_trial', AQUA, "each trial's RMS"), ('rms_ensemble', ORANGE, 'ensemble RMS'))):
        rows = [r for r in rep['E'] if r['kind'] == kind]
        ax.bar(x + (i - 1) * w, [100 * r['tipping']['mine'][2] for r in rows], w, color=col, label=lab)
        ax.plot(x + (i - 1) * w, [100 * r['tipping']['report'][2] for r in rows], 'x', color='black', ms=4)
    ax.set_xticks(x, [f'{k:.3g}' for k in Ks]); ax.plot([], [], 'x', color='black', label='report (800 trials)')
    ax.set(xlabel='Coupling K', ylabel='Tipping by t = 40, %', title='E1. Instantaneous R(t) against constant-RMS noise'); ax.legend()
    _save(fig, 'E1_time_variation.png')


def c3_and_f1(plt, rep):
    """C3 (sensitivity to sigma, averaged noise with my section-B E[R^2]) and F1 (section F model, time axis in steps):
    computed here, seeded, and saved to dtt/results/figdata_C3_F1.json."""
    B = {round(b['K'], 3): b['mine_mean_R2'] for b in rep['B']}; Ks = (0.0, 0.8, 4 / 3, 5.6 / 3, 3.2); out = {'C3': {}, 'F1': {}}
    for i, s in enumerate((0.45, 0.6, 0.75, 0.9)):
        out['C3'][s] = [float(dtt.averaged_noise_escape(Params(K=K, sigma=s), B[round(K, 3)], 4000, np.random.default_rng([dtt.SEED, 70, i, j]))[0].mean())
                        for j, K in enumerate(Ks)]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for i, (s, v) in enumerate(out['C3'].items()): ax.plot(Ks, np.array(v) * 100, color=[BLUE, AQUA, ORANGE, RED][i], marker='o', ms=4, label=f'σ = {s}')
    ax.set(xlabel='Coupling K', ylabel='Tipping by t = 40, %', title='C3. Sensitivity to the disturbance scale (averaged noise)'); ax.legend()
    _save(fig, 'C3_sigma_sensitivity.png')
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for j, (V, lab, col) in enumerate(((10.7, 'intermediate (V = 10.7)', BLUE), (27.2, 'strong (V = 27.2)', ORANGE))):
        ev, t = dtt.threshold_events(0.25 * np.sqrt(V / 31), 6000, np.random.default_rng([dtt.SEED, 71, j]))
        steps = np.arange(0, 801); cdf = [(t <= s).mean() for s in steps]; out['F1'][lab] = {'median_steps': float(np.nanmedian(t)), 'share_by_800': float(ev.mean())}
        ax.plot(steps, np.array(cdf) * 100, color=col, label=f'{lab}: {100 * ev.mean():.1f}% by step 800, median {np.nanmedian(t):.0f} steps')
    ax.set(xlabel='Step', ylabel='Events so far, %', title='F1. Stress-threshold events (section F model), time in steps'); ax.legend(loc='lower right')
    _save(fig, 'F1_threshold_events_steps.png')
    json.dump(out, open(os.path.join(RES, 'figdata_C3_F1.json'), 'w'), indent=1)


def d2_figs(plt, conv, abl, rho, sw):
    # convergence
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2), sharey=True)
    for ax, kind, t in zip(axes, ('instantaneous', 'rms_trial'), ('σR(t)', "each trial's RMS")):
        for j, c in enumerate(conv):
            dts = [float(d) for d in c['by_dt']]; ax.plot(dts, [100 * c['by_dt'][str(d)][kind]['p'] for d in c['by_dt']], color=KCOL[j + 1 if j else 0], marker='o', ms=3, label=f"K = {c['K']:.3g}")
        ax.set(xscale='log', xlabel='Step dt', title=t); ax.invert_xaxis()
    axes[0].set_ylabel('Tipping, %'); axes[1].legend(fontsize=7); fig.suptitle('Convergence: four step sizes, common random numbers', fontweight='bold')
    _save(fig, 'D2a_convergence.png')
    # ablation
    kinds = (('instantaneous', BLUE, 'σR(t)'), ('rms_trial', AQUA, "trial RMS"), ('rms_ensemble', YELLOW, 'ensemble RMS'),
             ('permuted', VIOLET, 'step-permuted'), ('block_permuted', ORANGE, 'block-permuted'), ('independent', GREY, 'independent'))
    fig, ax = plt.subplots(figsize=(7.6, 3.6)); w = 0.13; x = np.arange(len(abl))
    for i, (k, col, lab) in enumerate(kinds):
        ax.bar(x + (i - 2.5) * w, [100 * a[k]['p'] for a in abl], w, color=col, label=lab,
               yerr=np.hstack([_err(a[k]) for a in abl]), error_kw={'lw': 0.6, 'capsize': 1})
    ax.set_xticks(x, [f"{a['K']:.3g}" for a in abl]); ax.set(xlabel='Coupling K', ylabel='Tipping by t = 40, %', title='Mechanism ablation on the same R(t) traces')
    ax.legend(ncol=3, fontsize=7); _save(fig, 'D2b_ablation.png')
    # rho
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for j, r in enumerate(rho):
        rr = [x['rho'] for x in r['rows']]
        ax.plot(rr, [100 * x['instantaneous']['p'] for x in r['rows']], color=KCOL[j + 1 if j else 0], marker='o', ms=3, label=f"K = {r['K']:.3g}, σ√(ρR² + (1−ρ)/N)")
        ax.plot(rr, [100 * x['rms_trial']['p'] for x in r['rows']], color=KCOL[j + 1 if j else 0], ls='--', lw=0.9)
    ax.set(xlabel='Shared fraction ρ', ylabel='Tipping by t = 40, %', title='Shared fraction from 0 (independent) to 1 (fully shared); dashed: constant RMS')
    ax.legend(fontsize=7); _save(fig, 'D2c_rho.png')
    # timing
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for j, a in enumerate([a for a in abl if 'timing' in a]):
        t = a['timing']; lag = -np.array(t['lags'])
        ax.plot(lag, t['R_before'], color=[BLUE, ORANGE][j], marker='o', ms=3, label=f"K = {a['K']:.3g}: before first passage ({t['n_tippers']} paths)")
        ax.plot(lag, t['R_alive_same_time'], color=[BLUE, ORANGE][j], ls='--', lw=0.9, label='paths not yet tipped, same clock times')
    ax.set(xlabel='Model time relative to first passage', ylabel='Mean R', title='Synchrony before escape'); ax.legend(fontsize=7)
    _save(fig, 'D2d_timing.png')
    # sweeps: tipping and the time-variation effect
    params = list(dict.fromkeys(r['param'] for r in sw)); lab = {'D': 'oscillator diffusion D', 'omega_sd': 'frequency dispersion', 'N': 'N',
                                                                  'mu': 'μ', 'sigma': 'σ', 'T': 'horizon T'}
    for what, fname, ylab in (('instantaneous', 'D2e_sweeps_tipping.png', 'Tipping with σR(t), %'), ('inst_minus_rms', 'D2f_sweeps_time_variation.png', 'σR(t) minus constant RMS, points')):
        fig, axes = plt.subplots(2, 3, figsize=(8.6, 5.0))
        for ax, prm in zip(axes.flat, params):
            for j, K in enumerate(sorted({r['K'] for r in sw})):
                rows = sorted([r for r in sw if r['param'] == prm and r['K'] == K], key=lambda r: r['value']); v = [r['value'] for r in rows]
                if what == 'instantaneous': ax.plot(v, [100 * r[what]['p'] for r in rows], color=KCOL[j + 1 if j else 0], marker='o', ms=3, label=f'K = {K:.3g}')
                else:
                    ax.errorbar(v, [100 * r[what]['diff'] for r in rows], yerr=_c([[100 * (r[what]['diff'] - r[what]['lo']) for r in rows],
                                [100 * (r[what]['hi'] - r[what]['diff']) for r in rows]]), color=KCOL[j + 1 if j else 0], marker='o', ms=3, capsize=1.5, label=f'K = {K:.3g}')
                    ax.axhline(0, color='black', lw=0.6)
            ax.set_title(lab[prm], fontsize=9)
            if prm in ('D', 'N'):
                from matplotlib.ticker import FixedLocator, NullLocator
                ax.set_xscale('log'); vals = sorted({r['value'] for r in sw if r['param'] == prm})
                ax.xaxis.set_major_locator(FixedLocator(vals)); ax.xaxis.set_minor_locator(NullLocator())
                ax.set_xticklabels([f'{v:g}' for v in vals], fontsize=7)
        axes[0, 0].set_ylabel(ylab); axes[1, 0].set_ylabel(ylab); axes[0, 2].legend(fontsize=7)
        fig.suptitle('One-at-a-time sweeps around the base', fontweight='bold'); fig.tight_layout(); _save(fig, fname)


def main():
    plt = _plt(); L = lambda f: json.load(open(os.path.join(RES, f)))
    rep = L('reproduction.json'); conv, abl, rho, sw = L('d2_convergence.json'), L('d2_ablation.json'), L('d2_rho.json'), L('d2_sweeps.json')
    reproduced(plt, rep); dynamic_figs(plt, rep, abl); c3_and_f1(plt, rep); d2_figs(plt, conv, abl, rho, sw)
    print('wrote', len(os.listdir(FIG)), 'figures to dtt/fig/')
