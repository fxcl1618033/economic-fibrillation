"""Paper 1 figures, redrawn on S31 (convention P) with corrected labels. Each keeps its catalogue ID and goes next to the
earlier file in its category folder under a new name (the earlier file is never overwritten). The series behind each
figure are written to paper1/manuscript/figdata/ first, and every value the figure prints is checked against the
results file it comes from.

Main text (six): F1.3 r(t); F2.5 the tested arc, two-sided and past-only; F4.1 synchronization and swing size; F4.4 loss
of diversification; F5.1 the network's tightening; F6.1 the early-warning tests. Supplementary: F4.5 (both weightings)
and F5.4, the Methods diagnostics figure (open issue 18).
"""
import json
import os
import warnings

import numpy as np

from ef import config, crisis, decomposition, network, nulls, order, paper1, phaselags, tipping
from ef.manuscript.values import lookup
from ef.phases import analytic, window_cycles

ROOT = config.repo_root()
FIGDATA = os.path.join(ROOT, 'paper1', 'manuscript', 'figdata')
BLUE, ORANGE, AQUA, YELLOW, RED, GREY, LIGHT = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e34948', '#898781', '#c3c2b7'
CFG = os.path.join(ROOT, 'configs', 'runs', 'phase3_s31.yaml')
MAIN = {  # ID: (folder, stem, title)
    'F1.3': ('01_method', 'F1-03_order_parameter_s31', 'The Kuramoto order parameter r(t), 31 economies, 1970–2022'),
    'F2.5': ('02_crisis_arc', 'F2-05_arc_tested_s31', 'Synchronization around global recessions: the tested arc'),
    'F4.1': ('04_amplitude_diversification', 'F4-01_amplitude_s31', 'Synchronization and swing size move together'),
    'F4.4': ('04_amplitude_diversification', 'F4-04_diversification_s31', 'Loss of diversification in global recessions (GDP-weighted)'),
    'F5.1': ('05_network_phase', 'F5-01_mst_s31', 'The correlation network has tightened'),
    'F6.1': ('06_tipping_nulls', 'F6-01_early_warning_s31', 'Early-warning tests before global recessions'),
}
SUPP = {
    'F4.5': ('04_amplitude_diversification', 'F4-05_diversification_weightings_s31', 'Loss of diversification under both weightings'),
    'F5.4': ('05_network_phase', 'F5-04_methods_diagnostics_s31', 'Methods diagnostics'),
}


def _plt():
    import matplotlib
    matplotlib.use('Agg'); import matplotlib.pyplot as plt
    warnings.filterwarnings('ignore', module='matplotlib')
    plt.rcParams.update({'font.family': ['Inter', 'DejaVu Sans'], 'font.size': 9, 'axes.titlesize': 10, 'axes.titleweight': 'bold',
                         'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e5df',
                         'grid.linewidth': 0.6, 'legend.frameon': False, 'figure.dpi': 150, 'savefig.bbox': 'tight',
                         'axes.unicode_minus': True})
    return plt


def path(fid, ext='png'):
    folder, stem, _ = {**MAIN, **SUPP}[fid]; return os.path.join(ROOT, 'figures', folder, f"{stem}.{ext}")


def _save(fig, fid):
    import matplotlib.pyplot as plt
    for ext in ('pdf', 'png'):
        f = path(fid, ext); assert os.path.basename(f).endswith(f'_s31.{ext}'), f; fig.savefig(f, dpi=200 if ext == 'png' else None)
    plt.close(fig)


def _foot(fig, text):
    """A wrapped note under the figure, as wide as the figure."""
    import textwrap
    fig.text(0.01, -0.01, textwrap.fill(text, int(fig.get_figwidth() * 17)), fontsize=6.8, color=GREY, va='top')


def _sup(fig, text):
    fig.suptitle(text, x=0.01, y=1.06, ha='left', fontweight='bold', fontsize=10)


def _s(x, d=3): return f"{x:+.{d}f}".replace('-', '−')


def _p(p): return '0.0002' if p < 0.00025 else (f"{p:.4f}" if p < 0.001 else f"{p:.3f}")


def _shade(ax, years, rec, color=RED, alpha=0.12):
    for y in rec: ax.axvspan(y - 0.5, y + 0.5, color=color, alpha=alpha, lw=0)


# ------------------------------------------------------------------ figure data, checked against the results files

def figdata():
    """Recompute the series the figures draw (pinned data, the Paper 1 library, the S31 run settings) and check each
    printed statistic against its results file. Writes paper1/manuscript/figdata/*.json."""
    os.makedirs(FIGDATA, exist_ok=True); cfg = paper1.load_run_config(CFG); band = cfg['band']; rec = cfg['recessions']
    D = paper1.load_data('S31', tuple(cfg['span'])); w = tuple(cfg['window']); yrs = np.arange(w[0], w[1] + 1)
    out = {'recessions': rec, 'downturns': cfg['downturns'], 'window': list(w), 'code_version': paper1.code_version(), 'n_economies': len(D.isos)}
    # F1.3, F2.5, F4.1: r and the mean swing size under P
    z = paper1.signal(D, w, 'P', band); r = order.r(z); A = order.mean_amplitude(z)
    r_file = lookup('S31/P/arc#r_by_year')[0]; assert np.allclose(r, [r_file[str(y)] for y in yrs], atol=1e-12)
    s = cfg['tests']['amplitude']['detrend_sigma']; rd, Ad = paper1._g(r, s), paper1._g(A, s)
    c = float(np.corrcoef(rd, Ad)[0, 1]); assert abs(c - lookup('S31/P/amplitude#corr_detrended')[0]) < 1e-9
    out['r'] = {'years': yrs.tolist(), 'r': r.tolist(), 'Abar': A.tolist(), 'r_detrended': rd.tolist(), 'Abar_detrended': Ad.tolist(),
                'detrend_sigma': s, 'corr_detrended': c}
    # F4.4, F4.5: the rolling decomposition, both weightings
    td = cfg['tests']['diversification']; wd = tuple(td['window']); yd = np.arange(wd[0], wd[1] + 1); m = (D.years >= wd[0]) & (D.years <= wd[1])
    X = window_cycles(D.logs, D.years, wd, band); out['div'] = {'years': yd.tolist()}
    for kind in td['weights']:
        W = decomposition.weights(D.levels[:, m], kind, td['win']); own, cross, tot, _ = decomposition.rolling(X, W, td['win'])
        res = decomposition.crisis_excess(own, cross, tot, yd, rec)
        stored = lookup(f'S31/P/diversification#{kind}')[0]
        for k in ('cross_share_crisis', 'cross_share_normal', 'cross_fraction_of_excess'): assert abs(res[k] - stored[k]) < 1e-12, (kind, k)
        nn = lambda a: [None if np.isnan(v) else float(v) for v in a]
        out['div'][kind] = {'own': nn(own), 'cross': nn(cross), 'share': nn(cross / tot), 'rbar': nn(_),
                            **{k: res[k] for k in ('cross_share_crisis', 'cross_share_normal', 'cross_fraction_of_excess')}}
        if kind == 'equal':        # each economy's share of the own term (equal weights: its cycle variance over the sum)
            v = np.full((len(D.isos), len(yd)), np.nan)
            for t in range(td['win'] - 1, len(yd)): v[:, t] = X[:, t - td['win'] + 1:t + 1].var(axis=1)
            out['div']['own_share_by_economy'] = {iso: nn(v[i] / v.sum(axis=0)) for i, iso in enumerate(D.isos)}
    # F5.1, F5.4a: MST length (stored by year) and the last window's tree
    tm = cfg['tests']['mst']; wm = tuple(tm['window']); ym = np.arange(wm[0], wm[1] + 1)
    Xm = window_cycles(D.logs, D.years, wm, band); C = network.corr_windows(Xm, tm['win'])
    L = network.mst_stats(C[None], tm['win'])[0][0]; Lf = lookup('S31/P/mst#L_by_year')[0]
    assert np.allclose(np.nan_to_num(L), [Lf[str(y)] or 0 for y in ym], atol=1e-12)
    import networkx as nx
    Dm = np.sqrt(np.clip(2 * (1 - C[-1]), 0, None)); G = nx.Graph()
    for i in range(len(D.isos)):
        for j in range(i + 1, len(D.isos)): G.add_edge(D.isos[i], D.isos[j], weight=float(Dm[i, j]))
    T = nx.minimum_spanning_tree(G, algorithm='prim')
    assert abs(np.mean([d['weight'] for *_, d in T.edges(data=True)]) - Lf[str(wm[1])]) < 1e-9
    out['mst'] = {'years': ym.tolist(), 'L': [Lf[str(y)] for y in ym], 'decade_means': lookup('S31/P/mst#L_decade_means')[0],
                  'last_window': [int(wm[1] - tm['win'] + 1), int(wm[1])], 'tree': [[a, b, d['weight']] for a, b, d in T.edges(data=True)]}
    # F6.1: rolling lag-1 autocorrelation and variance of r on 15-year windows from 1962
    tc = cfg['tests']['csd']; wc = tuple(tc['window']); yc = np.arange(wc[0], wc[1] + 1)
    rc = order.r(analytic(D.logs, D.years, wc, 'P', band)); ar, va = tipping.rolling_ar1_var(rc, win=tc['win'], sigma=tc['sigma'])
    kt = dict(pre=tc['pre'], strict=tc.get('strict', False))
    assert abs(float(crisis.tau_pre(va, yc, rec, **kt)) - lookup('S31/P/csd#tau_var')[0]) < 1e-12
    assert abs(float(crisis.tau_pre(ar, yc, rec, **kt)) - lookup('S31/P/csd#tau_ar1')[0]) < 1e-12
    out['csd'] = {'years': yc.tolist(), 'ar1': [None if np.isnan(v) else float(v) for v in ar], 'var': [None if np.isnan(v) else float(v) for v in va],
                  'pre': tc['pre'], 'win': tc['win']}
    # F5.4b: the phase-lead spread against its surrogate null (seed and draws of the run)
    tp = cfg['tests']['phase_lags']; TH = np.angle(z); PSI = np.angle(np.exp(1j * TH).mean(axis=0))
    omega = phaselags.mean_frequency(TH); sd = float(phaselags.leads(TH, omega, PSI).std())
    assert abs(sd - lookup('S31/P/phase_lags#sd')[0]) < 1e-12
    Xs_, to_z = paper1.surrogate_source(D, w, 'P', band); null = []
    for Xs in nulls.surrogates(Xs_, tp['surrogates'], np.random.default_rng(tp['seed']), tp['batch']):
        null.append(phaselags.leads(np.angle(to_z(Xs)), omega).std(axis=-1))
    null = np.concatenate(null); assert abs(null.mean() - lookup('S31/P/phase_lags#null_mean')[0]) < 1e-12
    out['phase'] = {'sd': sd, 'null': null.round(6).tolist()}
    json.dump(out, open(os.path.join(FIGDATA, 'figdata_s31.json'), 'w'))
    return out


# ------------------------------------------------------------------ the figures

def f13(plt, d):
    yrs, r = np.array(d['r']['years']), np.array(d['r']['r']); N = d['n_economies']
    fig, ax = plt.subplots(figsize=(6.6, 2.8)); _shade(ax, yrs, d['recessions'])
    ax.plot(yrs, r, color=BLUE, lw=1.6); ax.axhline(np.sqrt(np.pi / (4 * N)), color=GREY, ls=':', lw=1)
    ax.text(2000.5, np.sqrt(np.pi / (4 * N)) - 0.06, f'mean under independent random phases ≈ {np.sqrt(np.pi / (4 * N)):.2f}', color=GREY, fontsize=7.5)
    i, j = int(np.argmin(r)), int(np.argmax(r))
    ax.annotate(f"{r[i]:.2f} ({yrs[i]})", (yrs[i], r[i]), textcoords='offset points', xytext=(6, 2), fontsize=7.5)
    ax.annotate(f"{r[j]:.2f} ({yrs[j]})", (yrs[j], r[j]), textcoords='offset points', xytext=(-48, 3), fontsize=7.5)
    ax.set_ylim(0, 1.02); ax.set_xlim(yrs[0] - 0.5, yrs[-1] + 0.5); ax.set_ylabel('r(t)')
    ax.set_title(MAIN['F1.3'][2], loc='left'); ax.text(0.99, 0.02, 'red bands: global recessions · convention P', transform=ax.transAxes, ha='right', fontsize=7, color=GREY)
    _save(fig, 'F1.3')


def f25(plt, d):
    labs = ['lead2', 'lead1', 'crisis', 'after1', 'after2']; names = ['lead-2', 'lead-1', 'crisis\nyear', 'after-1', 'after-2']
    P = [lookup(f'S31/P/arc#arc/{l}')[0] for l in labs]; C = [lookup(f'S31/P/conventions#C/arc/{l}')[0] for l in labs]
    fig, ax = plt.subplots(figsize=(6.6, 3.2)); x = np.arange(5); wd = 0.38
    for off, S, col, lab in ((-wd / 2, P, BLUE, 'two-sided phases (P)'), (wd / 2, C, ORANGE, 'past-only phases (C)')):
        b = ax.bar(x + off, [s['corr'] for s in S], wd, color=col, label=lab)
        for k, s in enumerate(S):
            y = s['corr']; ax.text(x[k] + off, y + (0.015 if y >= 0 else -0.015), f"p {_p(s['p'])}", ha='center', va='bottom' if y >= 0 else 'top', fontsize=6.8,
                                   fontweight='bold' if s['p'] <= 0.05 else 'normal')
    ax.axhline(0, color='black', lw=0.6); ax.set_xticks(x, names); ax.set_ylabel('corr(r, recession indicator)')
    ax.set_title(MAIN['F2.5'][2], loc='left'); ax.legend(loc='lower left', fontsize=7.5); ax.set_ylim(min(s['corr'] for s in P + C) - 0.07, max(s['corr'] for s in P + C) + 0.08)
    _foot(fig, 'One-sided p against 53 circular shifts of the recession years (floor 0.019); leads and the crisis year tested upward, '
               'after-lags downward; bold: p ≤ 0.05. Past-only phases use data up to each year only.')
    _save(fig, 'F2.5')


def f41(plt, d):
    yrs = np.array(d['r']['years']); rd, Ad = np.array(d['r']['r_detrended']), np.array(d['r']['Abar_detrended'])
    z = lambda v: (v - v.mean()) / v.std()
    fig, ax = plt.subplots(figsize=(6.6, 2.8)); _shade(ax, yrs, d['recessions'])
    ax.plot(yrs, z(rd), color=BLUE, lw=1.6, label='synchronization r(t)'); ax.plot(yrs, z(Ad), color=ORANGE, lw=1.6, label='mean swing size Ā(t)')
    ax.set_ylabel('detrended, standardized'); ax.set_xlim(yrs[0] - 0.5, yrs[-1] + 0.5); ax.legend(loc='upper left', fontsize=7.5, ncol=2)
    p_s, p_u = lookup('S31/P/amplitude#p_shift')[0], lookup('S31/P/amplitude#p_surrogate')[0]
    ax.set_title(MAIN['F4.1'][2], loc='left')
    _foot(fig, f"corr {_s(d['r']['corr_detrended'])}; p = {_p(p_s)} against 53 circular shifts and {_p(p_u)} against 5,000 surrogates (both floors). "
               f"Each series minus a Gaussian-smoothed copy (σ = {d['r']['detrend_sigma']:g} years), then standardized; convention P; red: global recessions.")
    _save(fig, 'F4.1')


def _div_panel(ax, d, kind, title):
    yrs = np.array(d['div']['years']); dv = d['div'][kind]; own = np.array(dv['own'], float); cross = np.array(dv['cross'], float)
    _shade(ax, yrs, d['recessions']); tot = own + cross
    ax.fill_between(yrs, 0, own * 1e4, color=LIGHT, label='own term (each economy alone)', lw=0)
    ax.fill_between(yrs, own * 1e4, tot * 1e4, color=BLUE, alpha=0.75, label='cross term (co-movement)', lw=0)
    ax.set_xlim(yrs[~np.isnan(tot)][0] - 0.5, yrs[-1] + 0.5); ax.set_ylabel('world cycle variance (×10⁻⁴)'); ax.set_title(title, loc='left')


def f44(plt, d):
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={'width_ratios': [2.3, 1]})
    _div_panel(a, d, 'gdp_mean', 'a  World cycle variance on 10-year windows'); a.legend(loc='upper left', fontsize=7)
    dv = d['div']['gdp_mean']
    b.bar([0, 1], [dv['cross_share_normal'], dv['cross_share_crisis']], color=[LIGHT, BLUE], width=0.6)
    for k, v in enumerate([dv['cross_share_normal'], dv['cross_share_crisis']]): b.text(k, v + 0.015, f"{v:.3f}", ha='center', fontsize=7.5)
    b.set_xticks([0, 1], ['normal\nwindows', 'recession\nwindows']); b.set_ylim(0, 1); b.set_ylabel('cross share of world variance')
    b.set_title('b  Cross share', loc='left')
    _sup(fig, MAIN['F4.4'][2])
    _foot(fig, f"GDP weights (within-window mean real GDP); windows from 1962; red: windows ending in a global recession. The cross term supplies "
             f"{100 * dv['cross_fraction_of_excess']:.1f}% of the extra variance in recession windows (descriptive; no p-value: the share has no proper null).")
    _save(fig, 'F4.4')


def f45(plt, d):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=False)
    for ax, kind, name in zip(axes, ('gdp_mean', 'equal'), ('GDP weights', 'equal weights')):
        dv = d['div'][kind]; v = [dv['cross_share_normal'], dv['cross_share_crisis']]
        ax.bar([0, 1], v, color=[LIGHT, BLUE], width=0.6); ax.set_ylim(0, 1); ax.set_xticks([0, 1], ['normal windows', 'recession windows'])
        for k, x in enumerate(v): ax.text(k, x + 0.015, f"{x:.3f}", ha='center', fontsize=7.5)
        ax.set_title(f"{name}: cross term supplies {100 * dv['cross_fraction_of_excess']:.1f}% of the excess", loc='left', fontsize=8.5)
    axes[0].set_ylabel('cross share of world variance'); _sup(fig, SUPP['F4.5'][2])
    _save(fig, 'F4.5')


def f51(plt, d):
    import networkx as nx
    m = d['mst']; yrs = np.array(m['years']); L = np.array([np.nan if v is None else v for v in m['L']])
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={'width_ratios': [1.6, 1]})
    _shade(a, yrs, d['recessions']); a.plot(yrs, L, color=GREY, lw=1.2, label='L(t), 10-year windows')
    dm = m['decade_means']
    for k, (lo, hi) in enumerate(((1979, 1989), (2013, 2022))):
        v = dm[f'{lo}-{hi}']; a.hlines(v, lo, hi, color=BLUE, lw=2.4, label='decade means' if k == 0 else None); a.text((lo + hi) / 2, v + 0.02, f"{v:.3f}", ha='center', color=BLUE, fontsize=7.5)
    ratio = dm['1979-1989'] / dm['2013-2022']
    a.set_title(f"a  MST mean edge length: {ratio:.1f}× tighter", loc='left'); a.set_ylabel('mean edge length √(2(1−ρ))'); a.legend(loc='lower left', fontsize=7)
    a.set_xlim(yrs[~np.isnan(L)][0] - 0.5, yrs[-1] + 0.5)
    G = nx.Graph(); [G.add_edge(x, y, weight=w) for x, y, w in m['tree']]
    pos = nx.kamada_kawai_layout(G, weight='weight')
    nx.draw_networkx_edges(G, pos, ax=b, edge_color=LIGHT, width=1.2); nx.draw_networkx_nodes(G, pos, ax=b, node_size=22, node_color=BLUE)
    nx.draw_networkx_labels(G, {k: (v[0], v[1] + 0.06) for k, v in pos.items()}, ax=b, font_size=5)
    b.set_title(f"b  The tree, {m['last_window'][0]}–{m['last_window'][1]}", loc='left'); b.axis('off')
    _sup(fig, MAIN['F5.1'][2])
    _foot(fig, "Minimum spanning tree of the 31 business cycles, distance √(2(1−ρ)) on 10-year windows (windows may start in 1962). "
               "Decade means: 1979–89, the first decade whose windows lie inside 1970–2022, and 2013–22. Red: global recessions.")
    _save(fig, 'F5.1')


def f61(plt, d):
    c = d['csd']; yrs = np.array(c['years']); ar = np.array(c['ar1'], float); va = np.array(c['var'], float)
    fig, (a, b) = plt.subplots(2, 1, figsize=(6.6, 4.0), sharex=True)
    for ax, x, col, name, key in ((a, va, ORANGE, 'variance of r(t) fluctuations', 'var'), (b, ar, BLUE, 'lag-1 autocorrelation of r(t) fluctuations', 'ar1')):
        for e in d['recessions']: ax.axvspan(e - c['pre'] - 0.5, e - 0.5, color=YELLOW, alpha=0.15, lw=0)
        _shade(ax, yrs, d['recessions']); ax.plot(yrs, x, color=col, lw=1.5)
        tau, p = lookup(f'S31/P/csd#tau_{key}')[0], lookup(f'S31/P/csd#p_{key}')[0]
        ax.set_title(f"{'a' if key == 'var' else 'b'}  {name}: pre-recession trend τ = {_s(tau)}, p = {_p(p)}", loc='left', fontsize=8.5)
    b.set_xlim(yrs[~np.isnan(ar)][0] - 0.5, yrs[-1] + 0.5)
    _sup(fig, MAIN['F6.1'][2])
    _foot(fig, f"Trailing {c['win']}-year windows of r(t) minus a Gaussian-smoothed trend; yellow: the {c['pre']} years before each recession (red). "
             "Kendall-type trend, one-sided upward, against 5,000 surrogates. Critical slowing down would raise both together.")
    _save(fig, 'F6.1')


def f54(plt, d):
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(10.0, 3.0)); fig.subplots_adjust(wspace=0.35)
    m = d['mst']; yrs = np.array(m['years']); L = np.array([np.nan if v is None else v for v in m['L']]); dm = m['decade_means']
    a.plot(yrs, L, color=GREY, lw=1)
    for lo, hi in ((1979, 1989), (2013, 2022)): a.hlines(dm[f'{lo}-{hi}'], lo, hi, color=BLUE, lw=2.2)
    a.set_title(f"a  MST mean edge length\ndecade means {dm['1979-1989']:.3f} vs {dm['2013-2022']:.3f} ({dm['1979-1989'] / dm['2013-2022']:.1f}×)", loc='left', fontsize=7.5)
    null = np.array(d['phase']['null']); b.hist(null, bins=50, color=LIGHT); b.axvline(d['phase']['sd'], color=RED, lw=1.5)
    b.set_title(f"b  Phase-lead spread {d['phase']['sd']:.3f} yr (red)\nvs {len(null):,} surrogates: p = {_p(lookup('S31/P/phase_lags#p_spread_lower')[0])} (floor)", loc='left', fontsize=7.5)
    b.set_xlabel('s.d. of phase leads (years)')
    labs = ['lead2', 'lead1', 'crisis', 'after1', 'after2']; raw = [lookup(f'S31/P/arc#arc/{l}/p')[0] for l in labs]; bon = [lookup(f'S31/P/arc#bonferroni/{l}')[0] for l in labs]
    x = np.arange(5); c.bar(x - 0.2, raw, 0.4, color=BLUE, label='raw'); c.bar(x + 0.2, bon, 0.4, color=ORANGE, label='Bonferroni')
    c.axhline(1 / 53, color='black', ls=':', lw=0.8); c.axhline(0.05, color='black', ls='--', lw=0.8); c.set_yscale('log')
    c.set_xticks(x, ['lead-2', 'lead-1', 'crisis', 'after-1', 'after-2'], fontsize=7); c.legend(fontsize=6.5, loc='upper left'); c.set_ylim(0.01, 1.5)
    c.set_title('c  Arc p-values, raw and Bonferroni\nfloor 1/53 (dotted), 0.05 (dashed)', loc='left', fontsize=7.5)
    _sup(fig, SUPP['F5.4'][2] + ' (S31, convention P)')
    _save(fig, 'F5.4')


def main():
    d = figdata(); plt = _plt()
    for f in (f13, f25, f41, f44, f45, f51, f61, f54): f(plt, d)


if __name__ == '__main__':
    main()
