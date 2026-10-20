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
BLUE, ORANGE, AQUA, YELLOW, RED, GREY, LIGHT = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e34948', '#898781', '#c3c2b7'   # project palette
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


W_FULL = 6.5                                                   # inches: the text width of the PDF (A4, 2.2 cm margins)
INK, MUTED, BAND, PRE = '#1f1f1d', '#6b6a64', '#e8e7e1', '#f6e7bf'


def _plt():
    """Journal style: Inter at 8 pt at the printed size, thin axes and ticks, no in-figure titles (the captions carry
    them), recessive grey for context, colour only for data."""
    import matplotlib
    matplotlib.use('Agg'); import matplotlib.pyplot as plt
    warnings.filterwarnings('ignore', module='matplotlib')
    plt.rcdefaults()
    plt.rcParams.update({
        'font.family': ['Inter', 'DejaVu Sans'], 'font.size': 8, 'axes.labelsize': 8, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
        'legend.fontsize': 7.5, 'axes.linewidth': 0.6, 'axes.edgecolor': INK, 'axes.labelcolor': INK, 'text.color': INK,
        'xtick.color': INK, 'ytick.color': INK, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.major.size': 3,
        'ytick.major.size': 3, 'xtick.direction': 'out', 'ytick.direction': 'out', 'axes.spines.top': False,
        'axes.spines.right': False, 'axes.grid': False, 'legend.frameon': False, 'legend.handlelength': 1.6,
        'lines.linewidth': 1.3, 'lines.solid_capstyle': 'round', 'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.03, 'pdf.fonttype': 42, 'axes.unicode_minus': True, 'mathtext.fontset': 'custom',
        'mathtext.rm': 'Inter', 'mathtext.it': 'Inter:italic', 'mathtext.bf': 'Inter:bold', 'axes.axisbelow': True})
    return plt


def path(fid, ext='png'):
    folder, stem, _ = {**MAIN, **SUPP}[fid]; return os.path.join(ROOT, 'figures', folder, f"{stem}.{ext}")


def _save(fig, fid):
    import matplotlib.pyplot as plt
    for ext in ('pdf', 'png'):
        f = path(fid, ext); assert os.path.basename(f).endswith(f'_s31.{ext}'), f; fig.savefig(f)
    plt.close(fig)


def _panel(ax, letter, x=-0.075, y=1.0):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=9.5, fontweight='bold', va='bottom', ha='left')


def _s(x, d=3): return f"{x:+.{d}f}".replace('-', '−')


def _p(p): return '0.0002' if p < 0.00025 else (f"{p:.4f}" if p < 0.001 else f"{p:.3f}")


def _bands(ax, rec, label=False, y=1.0):
    """Global recessions as light grey bands (optionally named at the top)."""
    for e in rec:
        ax.axvspan(e - 0.5, e + 0.5, color=BAND, lw=0, zorder=0)
        if label: ax.text(e, y, str(e), transform=ax.get_xaxis_transform(), ha='center', va='bottom', fontsize=6.5, color=MUTED)


def _years_axis(ax, lo, hi):
    ax.set_xlim(lo - 0.5, hi + 0.5); ax.set_xticks(range(1970 if lo <= 1970 else (lo // 10 + 1) * 10, hi + 1, 10))


def _halo(t):
    import matplotlib.patheffects as pe
    t.set_path_effects([pe.withStroke(linewidth=2.2, foreground='white')]); return t


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
    iu = np.triu_indices(len(D.isos), 1); pairs = {}
    for lo_, hi_ in ((1979, 1989), (2013, 2022)):        # pairwise correlations averaged over the windows ending in each decade
        sel = (ym >= lo_) & (ym <= hi_); pairs[f'{lo_}-{hi_}'] = np.nanmean(C[sel], axis=0)[iu].round(6).tolist()
    out['mst_pairs'] = pairs
    out['mst'] = {'years': ym.tolist(), 'L': [Lf[str(y)] for y in ym], 'decade_means': lookup('S31/P/mst#L_decade_means')[0],
                  'last_window': [int(wm[1] - tm['win'] + 1), int(wm[1])], 'tree': sorted([sorted([a, b]) + [d['weight']] for a, b, d in T.edges(data=True)])}   # fixed order: the library's edge order varies between runs
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
    # F2.5: the arc under P and C with the circular-shift null at each lag (5th-95th percentile of the 52 shifted values)
    rC = order.r(analytic(D.logs, D.years, w, 'C', band)); rCf = lookup('S31/P/conventions#C/r_by_year')[0]
    assert np.allclose(rC, [rCf[str(y)] for y in yrs], atol=1e-12)
    g = crisis.indicator(yrs, rec); out['arc'] = {}
    for conv, series in (('P', r), ('C', rC)):
        arc = crisis.arc(series, yrs, rec); out['arc'][conv] = {}
        for lab, lag, _ in crisis.ARC:
            stored = lookup(f'S31/P/arc#arc/{lab}')[0] if conv == 'P' else lookup(f'S31/P/conventions#C/arc/{lab}')[0]
            assert abs(arc[lab]['corr'] - stored['corr']) < 1e-12 and abs(arc[lab]['p'] - stored['p']) < 1e-12
            nul = nulls.shift_null(series, g, lag)
            out['arc'][conv][lab] = {'corr': arc[lab]['corr'], 'p': arc[lab]['p'], 'null_lo': float(np.percentile(nul, 5)),
                                     'null_hi': float(np.percentile(nul, 95))}
    out['added'] = [i for i in D.isos if i not in config.sample('S26')]
    json.dump(out, open(os.path.join(FIGDATA, 'figdata_s31.json'), 'w'))
    return out




# ------------------------------------------------------------------ the figures

def f13(plt, d):
    """F1.3: r(t), with the five recessions named and the random-phase mean as reference."""
    yrs, r = np.array(d['r']['years']), np.array(d['r']['r']); N = d['n_economies']; m0 = np.sqrt(np.pi / (4 * N))
    fig, ax = plt.subplots(figsize=(W_FULL, 2.3))
    _bands(ax, d['recessions'], label=True)
    ax.axhline(m0, color=MUTED, lw=0.7, ls=(0, (1.5, 2)))
    ax.text(yrs[-1] + 0.4, m0, 'independent\nphases', fontsize=6.5, color=MUTED, va='center', ha='left', linespacing=1.1)
    ax.plot(yrs, r, color=BLUE, lw=1.4, zorder=3)
    ax.set_ylim(0, 1); ax.set_yticks([0, 0.25, 0.5, 0.75, 1]); ax.set_ylabel('Order parameter $r(t)$')
    _years_axis(ax, yrs[0], yrs[-1])
    _save(fig, 'F1.3')


def f25(plt, d):
    """F2.5: the arc at every lag, two-sided (P) and past-only (C) phases, against the range of 90% of circular shifts.
    Filled markers: p <= 0.05 in the pre-registered direction."""
    from matplotlib.lines import Line2D
    labs = ['lead2', 'lead1', 'crisis', 'after1', 'after2']; names = ['Lead 2', 'Lead 1', 'Recession\nyear', 'After 1', 'After 2']
    fig, ax = plt.subplots(figsize=(W_FULL, 2.6)); x = np.arange(5)
    ax.axhline(0, color=INK, lw=0.6, zorder=1)
    for off, conv, col, mk in ((-0.14, 'P', BLUE, 'o'), (0.14, 'C', ORANGE, 'D')):
        A = d['arc'][conv]
        for k, l in enumerate(labs):
            a = A[l]; ax.plot([x[k] + off] * 2, [a['null_lo'], a['null_hi']], color=BAND, lw=5, solid_capstyle='butt', zorder=1)
            sig = a['p'] <= 0.05 + 1e-12
            ax.plot(x[k] + off, a['corr'], marker=mk, ms=6.5 if mk == 'o' else 5.8, mec=col, mew=1.3, mfc=col if sig else 'white', ls='none', zorder=3)
    for conv, off, col in (('P', -0.14, BLUE), ('C', 0.14, ORANGE)):
        a = d['arc'][conv]['lead1']
        _halo(ax.text(1 + off + (0.06 if conv == 'C' else -0.06), a['corr'] + 0.035, _s(a['corr']), fontsize=7, ha='left' if conv == 'C' else 'right', color=INK))
    ax.set_xticks(x, names); ax.set_xlim(-0.6, 4.6); ax.set_ylabel('Correlation of $r(t)$ with\nthe recession indicator')
    ax.set_ylim(-0.45, 0.6); ax.tick_params(axis='x', length=0)
    h = [Line2D([], [], marker='o', ls='none', mec=BLUE, mfc=BLUE, ms=6, label='Two-sided phases (P)'),
         Line2D([], [], marker='D', ls='none', mec=ORANGE, mfc=ORANGE, ms=5.5, label='Past-only phases (C)'),
         Line2D([], [], marker='o', ls='none', mec=INK, mfc='white', ms=6, label='Open: p > 0.05'),
         Line2D([], [], color=BAND, lw=5, label='90% of circular shifts')]
    ax.legend(handles=h, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=4, columnspacing=1.4, handletextpad=0.4)
    _save(fig, 'F2.5')


def f41(plt, d):
    """F4.1: (a) detrended, standardized r and Abar over time; (b) the same pairs as a scatter, recession years marked."""
    yrs = np.array(d['r']['years']); rd, Ad = np.array(d['r']['r_detrended']), np.array(d['r']['Abar_detrended'])
    z = lambda v: (v - v.mean()) / v.std(); zr, zA = z(rd), z(Ad); rec = np.isin(yrs, d['recessions'])
    fig = plt.figure(figsize=(W_FULL, 2.45)); gs = fig.add_gridspec(1, 2, width_ratios=[2.55, 1], wspace=0.28)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
    _bands(a, d['recessions']); a.axhline(0, color=BAND, lw=0.8, zorder=0)
    a.plot(yrs, zr, color=BLUE, lw=1.3, label='Synchronization $r(t)$', zorder=3)
    a.plot(yrs, zA, color=ORANGE, lw=1.3, label=r'Mean swing size $\bar{A}(t)$', zorder=3)
    a.set_ylabel('Detrended (standard deviations)'); _years_axis(a, yrs[0], yrs[-1]); a.set_ylim(-3, 4.5)
    a.legend(loc='upper left', ncol=2); _panel(a, 'a', x=-0.1)
    b.axhline(0, color=BAND, lw=0.8, zorder=0); b.axvline(0, color=BAND, lw=0.8, zorder=0)
    sl, ic = np.polyfit(zA, zr, 1); xs = np.array([zA.min(), zA.max()]); b.plot(xs, ic + sl * xs, color=INK, lw=0.8, zorder=2)
    b.scatter(zA[~rec], zr[~rec], s=11, color=LIGHT, edgecolor='white', lw=0.4, zorder=3)
    b.scatter(zA[rec], zr[rec], s=22, color=BLUE, edgecolor='white', lw=0.6, zorder=4)
    off = {1975: (0.12, -0.42, 'left'), 1982: (-0.12, 0.14, 'right'), 1991: (0.15, -0.05, 'left'), 2009: (-0.15, 0.12, 'right'), 2020: (0.05, -0.5, 'right')}
    for y_, xa, ya in zip(yrs[rec], zA[rec], zr[rec]):
        dx, dy, ha = off.get(int(y_), (0.15, 0.12, 'left')); _halo(b.text(xa + dx, ya + dy, str(y_), fontsize=6.5, color=INK, ha=ha))
    b.text(0.97, 0.04, f"corr {_s(d['r']['corr_detrended'])}", transform=b.transAxes, ha='right', fontsize=7.5)
    b.set_xlabel(r'Swing size $\bar{A}$ (SD)'); b.set_ylabel('$r$ (SD)'); _panel(b, 'b', x=-0.3)
    _save(fig, 'F4.1')


def f44(plt, d):
    """F4.4: (a) own and cross terms of world cycle variance on 10-year windows (GDP weights); (b) the cross share in
    normal and recession windows under both weightings."""
    yrs = np.array(d['div']['years']); dv = d['div']['gdp_mean']; own = np.array(dv['own'], float) * 1e4; cross = np.array(dv['cross'], float) * 1e4
    ok = ~np.isnan(own); fig = plt.figure(figsize=(W_FULL, 2.45)); gs = fig.add_gridspec(1, 2, width_ratios=[2.2, 1], wspace=0.48)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
    _bands(a, d['recessions'])
    a.fill_between(yrs[ok], 0, own[ok], color=LIGHT, lw=0, zorder=2)
    a.fill_between(yrs[ok], own[ok], own[ok] + cross[ok], color=BLUE, alpha=0.8, lw=0, zorder=2)
    a.plot(yrs[ok], own[ok] + cross[ok], color=BLUE, lw=0.8, zorder=3)
    _halo(a.text(1975.5, 0.12, 'Own term', fontsize=7, color=INK)); _halo(a.text(1975.5, 0.5, 'Cross term\n(co-movement)', fontsize=7, color=INK, linespacing=1.1))
    a.set_ylabel('World cycle variance ($\\times10^{-4}$)'); a.set_ylim(0, None); _years_axis(a, int(yrs[ok][0]), int(yrs[-1])); _panel(a, 'a', x=-0.09)
    rows = [('GDP weights', d['div']['gdp_mean']), ('Equal weights', d['div']['equal'])]
    for k, (nm, v) in enumerate(rows):
        y = 1 - k; lo, hi = v['cross_share_normal'], v['cross_share_crisis']
        b.plot([lo, hi], [y, y], color=LIGHT, lw=2.2, zorder=1, solid_capstyle='butt')
        b.plot(lo, y, 'o', ms=6.5, mfc='white', mec=MUTED, mew=1.1, zorder=3); b.plot(hi, y, 'o', ms=6.5, mfc=BLUE, mec=BLUE, zorder=3)
        b.text(lo, y - 0.2, f"{lo:.3f}", ha='center', va='top', fontsize=6.8, color=MUTED); b.text(hi, y - 0.2, f"{hi:.3f}", ha='center', va='top', fontsize=6.8)
    b.set_yticks([1, 0], [r[0] for r in rows]); b.set_ylim(-0.7, 1.6); b.set_xlim(0.55, 0.85); b.tick_params(axis='y', length=0)
    b.spines['left'].set_visible(False); b.set_xlabel('Cross share of world variance')
    b.plot([], [], 'o', mfc='white', mec=MUTED, label='Normal windows'); b.plot([], [], 'o', mfc=BLUE, mec=BLUE, label='Recession windows')
    b.legend(loc='upper left', ncol=1, handletextpad=0.3, borderaxespad=0); _panel(b, 'b', x=-0.55)
    _save(fig, 'F4.4')


def f45(plt, d):
    """F4.5 (supplementary): the cross share of world variance on 10-year windows, both weightings."""
    yrs = np.array(d['div']['years']); fig, ax = plt.subplots(figsize=(W_FULL, 2.2)); _bands(ax, d['recessions'])
    for kind, col, nm in (('gdp_mean', BLUE, 'GDP weights'), ('equal', ORANGE, 'Equal weights')):
        sh = np.array(d['div'][kind]['share'], float); ok = ~np.isnan(sh); ax.plot(yrs[ok], sh[ok], color=col, lw=1.3, label=nm, zorder=3)
    ax.set_ylim(0, 1); ax.set_ylabel('Cross share of world variance'); _years_axis(ax, 1971, int(yrs[-1])); ax.legend(loc='lower right', ncol=2)
    _save(fig, 'F4.5')


def f51(plt, d):
    """F5.1: (a) mean MST edge length with the two decade means; (b) the 465 pairwise cycle correlations, averaged over
    the windows ending in each decade, as densities."""
    m = d['mst']; yrs = np.array(m['years']); L = np.array([np.nan if v is None else v for v in m['L']]); dm = m['decade_means']
    fig = plt.figure(figsize=(W_FULL, 2.6)); gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.22)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1])
    _bands(a, d['recessions']); ok = ~np.isnan(L)
    a.plot(yrs[ok], L[ok], color=BLUE, lw=1.3, zorder=3)
    for lo, hi in ((1979, 1989), (2013, 2022)):
        v = dm[f'{lo}-{hi}']; a.hlines(v, lo - 0.5, hi + 0.5, color=ORANGE, lw=2, zorder=4)
    r0, r1 = dm['1979-1989'], dm['2013-2022']
    a.annotate('', xy=(1991.5, r1), xytext=(1991.5, r0), arrowprops=dict(arrowstyle='->', color=INK, lw=0.7, shrinkA=0, shrinkB=0))
    _halo(a.text(1990.5, (r0 + r1) / 2, f"Decade means\n{r0:.3f} → {r1:.3f}\n{r0 / r1:.1f}× shorter", fontsize=7, va='center', ha='right', linespacing=1.2))
    a.set_ylabel('Mean MST edge length, √(2(1 − ρ))'); _years_axis(a, int(yrs[ok][0]), int(yrs[-1])); _panel(a, 'a', x=-0.13)
    bins = np.arange(-1.0, 1.0001, 0.05)
    for key, col, nm, alpha in (('1979-1989', MUTED, '1979–89', 0.45), ('2013-2022', BLUE, '2013–22', 0.45)):
        v = np.array(d['mst_pairs'][key]); hh, _, _ = b.hist(v, bins=bins, density=True, histtype='stepfilled', color=LIGHT if col == MUTED else BLUE,
                                                              alpha=0.7 if col == MUTED else alpha, lw=0)
        b.hist(v, bins=bins, density=True, histtype='step', color=col, lw=0.9)
        med = float(np.median(v)); b.axvline(med, color=col, lw=0.8, ls=(0, (3, 2)))
        _halo(b.text(med + (0.03 if col == BLUE else -0.03), hh.max() * (1.02 if col == BLUE else 1.08), f"{nm}\nmedian {med:.2f}",
                     fontsize=6.8, ha='left' if col == BLUE else 'right', va='bottom', color=INK, linespacing=1.1))
    b.set_xlim(-1.0, 1.0); b.set_ylim(0, None); b.set_xlabel('Pairwise cycle correlation'); b.set_ylabel('Density')
    b.set_yticks([]); b.spines['left'].set_visible(False); _panel(b, 'b', x=-0.06)
    _save(fig, 'F5.1')


def f61(plt, d):
    """F6.1: variance and lag-1 autocorrelation of r's fluctuations on trailing windows; the eight years before each
    recession, over which the trend is tested, in colour."""
    c = d['csd']; yrs = np.array(c['years']); fig, axes = plt.subplots(2, 1, figsize=(W_FULL, 3.3), sharex=True, gridspec_kw={'hspace': 0.18})
    for ax, key, col, lab, letter in ((axes[0], 'var', ORANGE, 'Variance of $r$', 'a'), (axes[1], 'ar1', BLUE, 'Autocorrelation of $r$', 'b')):
        x = np.array(c[key], float); ok = ~np.isnan(x)
        for e in d['recessions']: ax.axvline(e, color=BAND, lw=4, zorder=0)
        ax.plot(yrs[ok], x[ok], color=LIGHT, lw=1.1, zorder=2)
        for e in d['recessions']:
            m = (yrs >= e - c['pre']) & (yrs <= e - 1) & ok
            if m.sum() >= 2: ax.plot(yrs[m], x[m], color=col, lw=1.8, zorder=3)
        tau, p = lookup(f'S31/P/csd#tau_{key}')[0], lookup(f'S31/P/csd#p_{key}')[0]
        ax.text(0.01, 0.95, f"Pre-recession trend τ = {_s(tau)}, p = {_p(p)}", transform=ax.transAxes, va='top', fontsize=7.5)
        ax.set_ylabel(lab); _panel(ax, letter, x=-0.1, y=1.02)
    _years_axis(axes[1], int(yrs[~np.isnan(np.array(c['var'], float))][0]), int(yrs[-1]))
    _save(fig, 'F6.1')


def f54(plt, d):
    """F5.4 (supplementary, Methods diagnostics): (a) MST decade means; (b) phase-lead spread against its null;
    (c) raw and Bonferroni p of the arc against the permutation floor."""
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(W_FULL, 2.1), gridspec_kw={'wspace': 0.42})
    m = d['mst']; yrs = np.array(m['years']); L = np.array([np.nan if v is None else v for v in m['L']]); dm = m['decade_means']; ok = ~np.isnan(L)
    a.plot(yrs[ok], L[ok], color=BLUE, lw=1)
    for lo, hi in ((1979, 1989), (2013, 2022)): a.hlines(dm[f'{lo}-{hi}'], lo - 0.5, hi + 0.5, color=ORANGE, lw=1.8)
    a.set_ylabel('Mean MST edge length'); a.set_xticks([1980, 2000, 2020]); _panel(a, 'a', x=-0.32)
    null = np.array(d['phase']['null']); b.hist(null, bins=40, color=LIGHT, lw=0)
    b.axvline(d['phase']['sd'], color=BLUE, lw=1.3); b.set_xlabel('S.d. of phase leads (years)'); b.set_ylabel('Surrogates')
    _halo(b.text(d['phase']['sd'] + 0.02, b.get_ylim()[1] * 0.9, 'observed', fontsize=6.8, color=INK)); _panel(b, 'b', x=-0.32)
    labs = ['lead2', 'lead1', 'crisis', 'after1', 'after2']; raw = [lookup(f'S31/P/arc#arc/{l}/p')[0] for l in labs]
    bon = [lookup(f'S31/P/arc#bonferroni/{l}')[0] for l in labs]; x = np.arange(5)
    c.axhline(1 / 53, color=MUTED, lw=0.7, ls=(0, (1.5, 2))); c.axhline(0.05, color=MUTED, lw=0.7, ls=(0, (4, 2)))
    c.plot(x, raw, 'o', ms=5, color=BLUE, label='Raw'); c.plot(x, bon, 'D', ms=4.5, mfc='white', mec=ORANGE, mew=1.1, label='Bonferroni')
    c.set_yscale('log'); c.set_ylim(0.012, 1.4); c.set_xticks(x, ['L2', 'L1', 'R', 'A1', 'A2']); c.set_ylabel('p'); c.set_xlim(-0.5, 4.5)
    c.set_yticks([0.02, 0.05, 0.1, 0.2, 0.5, 1], ['0.02', '0.05', '0.1', '0.2', '0.5', '1']); c.minorticks_off()
    c.text(-0.45, 1 / 53 * 0.84, 'floor 1/53', fontsize=6.3, color=MUTED, va='top', ha='left')
    c.legend(loc='upper left', handletextpad=0.2, borderaxespad=0); _panel(c, 'c', x=-0.32)
    _save(fig, 'F5.4')


def main():
    d = figdata(); plt = _plt()
    for f in (f13, f25, f41, f44, f45, f51, f61, f54): f(plt, d)


if __name__ == '__main__':
    main()
