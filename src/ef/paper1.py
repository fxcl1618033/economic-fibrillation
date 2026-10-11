"""Paper 1's tests, one function per family, driven by a run config (configs/runs/*.yaml).

    python -m ef.paper1 --config configs/runs/paper1_S26_asrun.yaml            # all tests -> build/paper1/<name>.json
    python -m ef.paper1 --config ... --golden                                   # and compare with tests/golden_paper1.json

Each test takes its convention, window, seed and surrogate batch from the config, so the as-run config reproduces the
stored results (including the surrogate p-values, whose random draws follow the as-run order) and a Phase 3 config
can run everything under convention P on another sample.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
from dataclasses import dataclass

import numpy as np
import yaml
from scipy.ndimage import gaussian_filter1d
from scipy.signal import hilbert
from scipy.stats import pearsonr

from ef import config, crisis, decomposition, network, nulls, order, phaselags, tipping
from ef.data import maddison
from ef.filters import bandpass, cycles
from ef.phases import analytic, window_cycles

ARC4 = tuple(l for l in crisis.ARC if l[0] != 'after1')     # the four lags robustness.py and structure_tests.py used


@dataclass
class Data:
    sample: str
    isos: list
    years: np.ndarray       # the span, e.g. 1950-2022
    logs: np.ndarray        # log real GDP per capita, economies x years
    levels: np.ndarray      # real GDP (per capita x population), economies x years


def load_data(sample, span=(1950, 2022), drop=(), gmd_growth=None):
    """Maddison panel for a sample (a name in configs/default.yaml or a list of ISO codes), leaving out `drop`.

    gmd_growth = {'economies': [...], 'years': [a, b]} replaces Maddison's year-on-year growth of GDP per capita in
    years a..b with the Global Macro Database's real GDP per capita growth and re-chains the levels (open issue 13,
    pre-registration amendment 1.7); population is unchanged."""
    isos = [i for i in (config.sample(sample) if isinstance(sample, str) else list(sample)) if i not in drop]
    L = maddison.panel(isos, years=tuple(span))
    g, p = maddison.wide(L, 'gdppc'), maddison.wide(L, 'pop')
    G = g.values.astype(float); years = g.index.to_numpy()
    if gmd_growth:
        from ef.data import gmd
        M = gmd.read(config.raw_file('gmd', 'data/final/data_final.dta'), columns=['ISO3', 'year', 'rGDP_pc'])
        M['year'] = M.year.astype(int); a, b = gmd_growth['years']; G = G.copy()
        for iso in [i for i in gmd_growth['economies'] if i in isos]:
            j = isos.index(iso); s = M[M.ISO3 == iso].set_index('year').rGDP_pc; old = G[:, j].copy()
            for k in range(1, len(years)):
                y = int(years[k]); f = s[y] / s[y - 1] if a <= y <= b else old[k] / old[k - 1]
                G[k, j] = G[k - 1, j] * f
    name = sample if isinstance(sample, str) else '+'.join(isos)
    return Data(name, isos, years, np.log(G.T), (G * p.values.astype(float)).T)


def _years(window): return np.arange(window[0], window[1] + 1)


def _g(x, s): return x - gaussian_filter1d(x, s, axis=-1)


def cycle_source(D, span, convention, band):
    """For tests without a Hilbert transform (MST, decomposition): the cycles on the span, the cycles surrogates are drawn
    from, and the map from a surrogate batch to the span. As run (convention None): surrogates of the span's cycles.
    P: surrogates of the 1950-2022 cycles, cut to the span (pre-registration section 3). N: band-pass on the span only."""
    m = (D.years >= span[0]) & (D.years <= span[1])
    if convention == 'N':
        X = bandpass(D.logs[:, m], *band); return X, X, lambda Xs: Xs
    X = window_cycles(D.logs, D.years, span, band)
    if convention in ('P', 'E', 'W'):
        return X, cycles(D.logs, lo_period=band[0], hi_freq=band[1]), lambda Xs: Xs[..., m]
    return X, X, lambda Xs: Xs


def surrogate_source(D, window, convention, band):
    """The cycles surrogates are drawn from, and the map from a batch of surrogate cycles to analytic signals on the
    window, consistent with the convention used for the real data."""
    m = (D.years >= window[0]) & (D.years <= window[1])
    if convention == 'P':
        return cycles(D.logs, lo_period=band[0], hi_freq=band[1]), lambda Xs: hilbert(Xs, axis=-1)[..., m]
    if convention == 'W':
        return window_cycles(D.logs, D.years, window, band), lambda Xs: hilbert(Xs, axis=-1)
    if convention == 'N':
        return bandpass(D.logs[:, m], *band), lambda Xs: hilbert(Xs, axis=-1)
    if convention == 'E':
        p = int(round(band[0]))
        def to_z(Xs):
            z = hilbert(np.pad(Xs, [(0, 0)] * (Xs.ndim - 1) + [(p, p)], mode='reflect'), axis=-1)[..., p:p + Xs.shape[-1]]
            return z[..., m]
        return cycles(D.logs, lo_period=band[0], hi_freq=band[1]), to_z
    raise ValueError(f"no surrogate scheme for convention {convention!r}")


# ------------------------------------------------------------------ the tests

def run_arc(D, cfg, t):
    """kose_terrones_test.py: the crisis arc of r(t), the superposed epoch, bootstrap means and multiplicity."""
    w = cfg['window']; yrs = _years(w); rec = cfg['recessions']
    r = order.r(analytic(D.logs, D.years, w, t['convention'], cfg['band']))
    arc = crisis.arc(r, yrs, rec)
    _, em = crisis.epoch(r, yrs, rec, range(-4, 5))
    g = crisis.indicator(yrs, rec); dn = crisis.indicator(yrs, cfg['downturns']); rng = np.random.default_rng(t['seed'])
    ci = {k: crisis.bootstrap_mean_ci(r[mk], rng, t['bootstrap']) for k, mk in
          (('recession', g == 1), ('downturn', dn == 1), ('normal', (g == 0) & (dn == 0)))}
    p = [arc[l]['p'] for l, _, _ in crisis.ARC]
    return {'arc': arc, 'epoch_mean_t-4..t+4': em.tolist(), 'epoch_peak': float(em[3]), 'epoch_after2': float(em[6]),
            'mean_ci': ci, 'bonferroni': dict(zip([l for l, _, _ in crisis.ARC], crisis.bonferroni(p).tolist())),
            'benjamini_hochberg': dict(zip([l for l, _, _ in crisis.ARC], crisis.benjamini_hochberg(p).tolist())),
            'r_by_year': {int(y): float(v) for y, v in zip(yrs, r)}}


def run_conventions(D, cfg, t):
    """tools/check_runin_conventions.py: the arc and the r-amplitude link under each phase convention."""
    w = cfg['window']; yrs = _years(w); s = t['detrend_sigma']; out = {}
    for conv in t['conventions']:
        z = analytic(D.logs, D.years, w, conv, cfg['band']); r = order.r(z); A = order.mean_amplitude(z)
        out[conv] = {'arc': crisis.arc(r, yrs, cfg['recessions']), 'amp_raw': nulls.shift_corr_test(r, A),
                     'amp_detrended': nulls.shift_corr_test(_g(r, s), _g(A, s)),
                     'r_by_year': {int(y): float(v) for y, v in zip(yrs, r)}}
    return out


def run_amplitude(D, cfg, t):
    """amplitude_test.py: corr(r, mean amplitude) after detrending, against circular shifts and surrogate economies."""
    w = cfg['window']; s = t['detrend_sigma']
    z = analytic(D.logs, D.years, w, t['convention'], cfg['band']); r = order.r(z); A = order.mean_amplitude(z)
    c_det, p_shift = nulls.shift_corr_test(_g(r, s), _g(A, s))
    X, to_z = surrogate_source(D, w, t['convention'], cfg['band']); null = []
    for Xs in nulls.surrogates(X, t['surrogates'], np.random.default_rng(t['seed']), t['batch']):
        zs = to_z(Xs); rc = _g(order.r(zs), s); ac = _g(order.mean_amplitude(zs), s)
        rc = rc - rc.mean(axis=-1, keepdims=True); ac = ac - ac.mean(axis=-1, keepdims=True)
        null.append((rc * ac).mean(axis=-1) / (rc.std(axis=-1) * ac.std(axis=-1)))
    null = np.concatenate(null)
    return {'corr_detrended': c_det, 'p_shift': p_shift, 'p_surrogate': float(nulls.p_upper(c_det, null)),
            'null_mean': float(null.mean()), 'corr_raw': nulls.shift_corr_test(r, A)}


def run_diversification(D, cfg, t):
    """diversification.py and diversification_equal.py, with the Methods' within-window mean GDP weights added.
    t['window'] sets the span the rolling windows may use (default: the statistics window, as run)."""
    w = t.get('window', cfg['window']); yrs = _years(w); m = (D.years >= w[0]) & (D.years <= w[1]); rec = cfg['recessions']
    X, Xsrc, cut = cycle_source(D, w, t.get('convention'), cfg['band']); lev = D.levels[:, m]; out = {}
    for kind in t['weights']:
        W = decomposition.weights(lev, kind, t['win'])
        own, cross, tot, rbar = decomposition.rolling(X, W, t['win'])
        res = decomposition.crisis_excess(own, cross, tot, yrs, rec)
        res['recession_windows'] = [int(y) for y in yrs[np.isin(yrs, rec) & ~np.isnan(tot)]]
        rw = np.abs((W * np.exp(1j * np.angle(hilbert(X, axis=-1)))).sum(axis=0)); ok = ~np.isnan(rbar)
        res['corr_rbar_r'] = float(pearsonr(rbar[ok], rw[ok])[0])
        if t.get('surrogates'):
            sh, do, dc = decomposition.surrogate_excess(Xsrc, W, yrs, rec, t['surrogates'], np.random.default_rng(t['seed']),
                                                        t['win'], t['batch'], cut)
            res['p_surrogate'] = float(nulls.p_upper(res['cross_share_crisis'], sh))
            ratio = dc / (do + dc)
            res['d6'] = {'n_ratio_at_least_observed': int(np.sum(ratio >= res['cross_fraction_of_excess'])),
                         'p_ratio_nominal': float(nulls.p_upper(res['cross_fraction_of_excess'], ratio)),
                         'p_excess_cross': float(nulls.p_upper(res['excess_from_cross'], dc)),
                         'p_excess_own': float(nulls.p_upper(res['excess_from_own'], do))}
        out[kind] = res
    return out


def run_cross_split(D, cfg, t):
    """crossterm_split.py: the cross term's recession rise split into correlation and swing size.
    t['window'] as in run_diversification; t['weights'] defaults to the as-run pair."""
    w = t.get('window', cfg['window']); yrs = _years(w); m = (D.years >= w[0]) & (D.years <= w[1])
    X = cycle_source(D, w, t.get('convention'), cfg['band'])[0]; lev = D.levels[:, m]
    return {k: decomposition.cross_split(X, decomposition.weights(lev, k, t['win']), yrs, cfg['recessions'], t['win'])
            for k in t.get('weights', ('gdp_end', 'equal'))}


def run_structure(D, cfg, t):
    """structure_tests.py: the fibrillation identity |Z| = Abar R_A and the Fiedler blocs."""
    w = cfg['window']; yrs = _years(w); rec = cfg['recessions']; cm = crisis.indicator(yrs, rec) == 1; nm = ~cm
    z = analytic(D.logs, D.years, w, t['convention'], cfg['band'])
    Z = order.world_phasor(z); Abar = order.mean_amplitude(z); RA = order.amplitude_alignment(z); r = order.r(z)
    lZ, lA, lR = np.log(np.abs(Z) ** 2), 2 * np.log(Abar), 2 * np.log(RA)
    dZ, dA, dR = (lZ[cm].mean() - lZ[nm].mean(), lA[cm].mean() - lA[nm].mean(), lR[cm].mean() - lR[nm].mean())
    X, to_z = surrogate_source(D, w, t['convention'], cfg['band']); nR, nA = [], []
    for Xs in nulls.surrogates(X, t['surrogates'], np.random.default_rng(t['seed']), t['batch']):
        zs = to_z(Xs); lr = 2 * np.log(order.amplitude_alignment(zs)); la = 2 * np.log(order.mean_amplitude(zs))
        nR.append(lr[:, cm].mean(1) - lr[:, nm].mean(1)); nA.append(la[:, cm].mean(1) - la[:, nm].mean(1))
    nR, nA = np.concatenate(nR), np.concatenate(nA)
    lam2, in_a = network.fiedler(np.real(z) if t['convention'] in ('W', 'N') else
                                 window_cycles(D.logs, D.years, w, cfg['band']))
    rw, rb = network.bloc_alignment(np.angle(z), in_a)
    return {'identity_err': order.identity_error(z), 'corr_RA_r': float(pearsonr(RA, r)[0]),
            'dZ': float(dZ), 'dA': float(dA), 'dR': float(dR), 'align_share': float(dR / dZ), 'swing_share': float(dA / dZ),
            'p_align': float(nulls.p_upper(dR, nR)), 'p_swing': float(nulls.p_upper(dA, nA)),
            'lambda2': lam2, 'blocA': [i for i, a in zip(D.isos, in_a) if a], 'blocB': [i for i, a in zip(D.isos, in_a) if not a],
            'hier': {name: crisis.arc(x, yrs, rec, ARC4) for name, x in (('r', r), ('r_within', rw), ('r_between', rb))}}


def run_mst(D, cfg, t):
    """mst_network.py: mean MST edge length and largest eigenvalue on 10-year windows, pre-crisis trends vs surrogates."""
    w = t['window']; yrs = _years(w); rec = cfg['recessions']; sig = t.get('detrend_sigma')
    X, Xsrc, cut = cycle_source(D, w, t.get('convention'), cfg['band'])
    C = network.corr_windows(X, t['win']); L, M = network.mst_stats(C[None], t['win']); L, M = L[0], M[0]
    k = dict(pre=t['pre'], strict=t.get('strict', False))

    def detr(x):
        ok = ~np.isnan(x[..., :]).any(axis=tuple(range(x.ndim - 1))) if x.ndim > 1 else ~np.isnan(x)
        d = np.full_like(x, np.nan); d[..., ok] = x[..., ok] - gaussian_filter1d(x[..., ok], sig, axis=-1); return d
    tauL = float(crisis.tau_pre(L, yrs, rec, **k)); tauM = float(crisis.tau_pre(M, yrs, rec, **k))
    tauLd = float(crisis.tau_pre(detr(L), yrs, rec, **k)) if sig else None; nL, nM, nLd = [], [], []
    for Xs in nulls.surrogates(Xsrc, t['surrogates'], np.random.default_rng(t['seed']), t['batch']):
        Ls, Ms = network.mst_stats(network.corr_windows(cut(Xs), t['win']), t['win'])
        nL.append(crisis.tau_pre(Ls, yrs, rec, **k)); nM.append(crisis.tau_pre(Ms, yrs, rec, **k))
        if sig: nLd.append(crisis.tau_pre(detr(Ls), yrs, rec, **k))
    nL, nM = np.concatenate(nL), np.concatenate(nM)
    det = {'tau_L_detrended': tauLd, 'p_contraction_detrended': float(nulls.p_lower(tauLd, np.concatenate(nLd)))} if sig else {}
    yi = {int(y): i for i, y in enumerate(yrs)}
    dec = lambda a, b: float(np.nanmean(L[yi[a]:yi[b] + 1])) if a in yi and b in yi else None
    periods = t.get('decades', [[1979, 1989], [2013, 2022]])
    return det | {'tau_L': tauL, 'p_contraction': float(nulls.p_lower(tauL, nL)), 'tau_lambdamax': tauM,
            'p_fragility': float(nulls.p_upper(tauM, nM)), 'pre_crisis_events': _events_used(L, yrs, rec, t['pre'], k['strict']),
            'L_decade_means': {f'{a}-{b}': dec(a, b) for a, b in periods},
            'centrality': dict(zip(D.isos, network.mst_degree(C, t['win']).tolist())),
            'L_by_year': {int(y): (None if np.isnan(v) else float(v)) for y, v in zip(yrs, L)},
            'lambdamax_by_year': {int(y): (None if np.isnan(v) else float(v)) for y, v in zip(yrs, M)}}


def _events_used(x, yrs, rec, pre, strict):
    """The recessions a pre-crisis trend actually uses, with how many of the pre-window years are defined."""
    yi = {int(y): i for i, y in enumerate(yrs)}; out = {}
    for o in rec:
        idx = [yi[y] for y in range(o - pre, o) if y in yi]
        n = int((~np.isnan(x[idx])).sum()) if len(idx) == pre else 0
        if n and not (strict and n < pre): out[int(o)] = f"{n}/{pre}"
    return out


def run_phase_lags(D, cfg, t):
    """phase_lags.py: leads over the world phase in years, and the spread of leads against surrogates (both tails;
    the as-run script stored the upper tail, open issue 8)."""
    w = cfg['window']; yrs = _years(w)
    TH = np.angle(analytic(D.logs, D.years, w, t['convention'], cfg['band'])); PSI = np.angle(np.exp(1j * TH).mean(axis=0))
    omega = phaselags.mean_frequency(TH); lead = phaselags.leads(TH, omega, PSI); sd = float(lead.std())
    X, to_z = surrogate_source(D, w, t['convention'], cfg['band']); null = []
    for Xs in nulls.surrogates(X, t['surrogates'], np.random.default_rng(t['seed']), t['batch']):
        ths = np.angle(to_z(Xs)); null.append(phaselags.leads(ths, omega).std(axis=-1))
    null = np.concatenate(null); yi = {int(y): i for i, y in enumerate(yrs)}; per = {}
    for onset in (2009, 2020):
        idx = [yi[y] for y in range(onset - 8, onset) if y in yi]
        d = phaselags.wrap(TH[:, idx] - PSI[None, idx]); per[onset] = dict(zip(D.isos, (np.angle(np.exp(1j * d).mean(axis=1)) / omega).tolist()))
    return {'period_years': float(2 * np.pi / omega), 'sd': sd, 'spread': float(lead.max() - lead.min()),
            'p_spread_lower': float(nulls.p_lower(sd, null)), 'p_spread_upper_as_run': float(nulls.p_upper(sd, null)),
            'null_mean': float(null.mean()), 'null_min': float(null.min()), 'lead_years': dict(zip(D.isos, lead.tolist())), 'per_crisis': per}


def run_csd(D, cfg, t):
    """csd_surrogate.py: pre-crisis trends in the lag-1 autocorrelation and variance of r, against surrogates.
    The restoring time is not in the battery: it is a monotone function of the lag-1 autocorrelation, so its trend
    test repeats the autocorrelation's (open issue 22, decision of 11 October 2026)."""
    w = t['window']; yrs = _years(w); rec = cfg['recessions']; k = dict(win=t['win'], sigma=t['sigma'])
    kt = dict(pre=t['pre'], strict=t.get('strict', False))
    r = order.r(analytic(D.logs, D.years, w, t['convention'], cfg['band']))
    ar, va = tipping.rolling_ar1_var(r, **k)
    tau = {n: float(crisis.tau_pre(x, yrs, rec, **kt)) for n, x in (('ar1', ar), ('var', va))}
    X, to_z = surrogate_source(D, w, t['convention'], cfg['band']); nulls_ = {n: [] for n in tau}
    for Xs in nulls.surrogates(X, t['surrogates'], np.random.default_rng(t['seed']), t['batch']):
        a_, v_ = tipping.rolling_ar1_var(order.r(to_z(Xs)), **k)
        for n, x in (('ar1', a_), ('var', v_)):
            nulls_[n].append(crisis.tau_pre(x, yrs, rec, **kt))
    return ({f'tau_{n}': tau[n] for n in tau} | {f'p_{n}': float(nulls.p_upper(tau[n], np.concatenate(nulls_[n]))) for n in tau}
            | {'pre_crisis_events': _events_used(ar, yrs, rec, t['pre'], kt['strict'])})


def run_bifurcation(D, cfg, t):
    """kuramoto_bifurcation.py: implied coupling K/Kc and the post-crisis change in the recovery rate."""
    w = t['window']; yrs = _years(w); rec = cfg['recessions']; k = dict(win=t['win'], sigma=t['sigma'])
    r = order.r(analytic(D.logs, D.years, w, t['convention'], cfg['band']))
    stat = float(tipping.post_minus_base(tipping.recovery_rate(r, **k), yrs, rec))
    X, to_z = surrogate_source(D, w, t['convention'], cfg['band']); null = []
    for Xs in nulls.surrogates(X, t['surrogates'], np.random.default_rng(t['seed']), t['batch']):
        null.append(tipping.post_minus_base(tipping.recovery_rate(order.r(to_z(Xs)), **k), yrs, rec))
    null = np.concatenate(null); KK = tipping.implied_coupling(r); lam = tipping.recovery_rate(r, **k)
    post_used = [int(o) for o in rec if any((o + j) in set(yrs[~np.isnan(lam)].tolist()) for j in (0, 1, 2))]
    _, ek = crisis.epoch(KK, yrs, rec, range(-3, 4))
    return {'stat_real': stat, 'p_slowing_post': float(nulls.p_lower(stat, null)), 'null_mean': float(null.mean()),
            'post_crisis_events': post_used,
            'epoch_KKc_mean_t-3..t+3': ek.tolist(), 'KKc_by_year': {int(y): float(v) for y, v in zip(yrs, KK)}}


def run_robustness(D, cfg, t):
    """robustness.py, saved in full (open issue 9): band, cycle method, dropped economies, split sample and
    leave-one-crisis-out, each with the four-lag arc."""
    span = (int(D.years[0]), int(D.years[-1])); w = cfg['window']; rec = list(cfg['recessions'])
    conv = t['convention']; b = cfg['band']

    def phases(band=b, method='bp'):
        return np.angle(analytic(D.logs, D.years, span, conv, band, method))

    def arc(TH, keep=None, y0=w[0], y1=w[1], events=rec):
        sel = (D.years >= y0) & (D.years <= y1); keep = np.ones(len(D.isos), bool) if keep is None else keep
        if sum(e in range(y0, y1 + 1) for e in events) < 2: return None
        r = np.abs(np.exp(1j * TH[keep][:, sel]).mean(axis=0))
        return {k: (v['corr'], v['p']) for k, v in crisis.arc(r, D.years[sel], events, ARC4).items()}
    base = phases(); out = {'baseline': arc(base)}
    out['band 2-8 yr'] = arc(phases((8.0, 0.49))); out['band 3-10 yr'] = arc(phases((10.0, 1 / 3.)))
    out['HP filter (lambda=100)'] = arc(phases(method='hp')); out['growth rates'] = arc(phases(method='growth'))
    drops = t.get('drop_economies', ['USA', 'DEU', 'JPN']); drops = D.isos if drops == 'all' else drops
    for c in drops:
        out[f'without {c}'] = arc(base, np.array([i != c for i in D.isos]))
    out['1970-1995 (1975,82,91)'] = arc(base, y0=1970, y1=1995, events=[1975, 1982, 1991])
    out['1996-2022 (2009,2020)'] = arc(base, y0=1996, y1=2022, events=[2009, 2020])
    for c in rec: out[f'without {c}'] = arc(base, events=[y for y in rec if y != c])
    out['without 2009 AND 2020'] = arc(base, events=[y for y in rec if y not in (2009, 2020)])
    return out


TESTS = {'arc': run_arc, 'conventions': run_conventions, 'amplitude': run_amplitude, 'diversification': run_diversification,
         'cross_split': run_cross_split, 'structure': run_structure, 'mst': run_mst, 'phase_lags': run_phase_lags,
         'csd': run_csd, 'bifurcation': run_bifurcation, 'robustness': run_robustness}


def load_run_config(path):
    cfg = yaml.safe_load(open(path)); cfg['band'] = tuple(cfg['band']); return cfg


def code_version():
    try:
        root = config.repo_root()
        rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(['git', 'status', '--porcelain'], cwd=root, capture_output=True, text=True).stdout.strip()
        return rev + ('+uncommitted' if dirty else '')
    except OSError:
        return 'unknown'


def run(cfg, only=None):
    D = load_data(cfg['sample'], cfg['span'])
    res = {n: f(D, cfg, cfg['tests'][n]) for n, f in TESTS.items() if n in cfg['tests'] and (only is None or n in only)}
    return {'config': cfg, 'code_version': code_version(), 'run_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'results': res}


# ------------------------------------------------------------------ the golden view

def golden_view(results, sync=None):
    """The results under the keys of tests/golden_paper1.json (tools/make_golden.py). sync: an atlas sync.json."""
    R = results; v = {}
    lab = {'lead2': 'lead2', 'lead1': 'lead1', 'crisis': 'crisis', 'after1': 'after1', 'after2': 'after2'}
    if 'arc' in R:
        for k in lab:
            v[f'arc.P.{k}.corr'] = R['arc']['arc'][k]['corr']; v[f'arc.P.{k}.p_one_sided'] = R['arc']['arc'][k]['p']
        v['epoch.P.peak_t-1'] = R['arc']['epoch_peak']; v['epoch.P.t+2'] = R['arc']['epoch_after2']
        v['r.P.1970'] = R['arc']['r_by_year'][1970]; v['r.P.2020'] = R['arc']['r_by_year'][2020]
    for conv, c in R.get('conventions', {}).items():
        for k in lab:
            v.setdefault(f'arc.{conv}.{k}.corr', c['arc'][k]['corr']); v.setdefault(f'arc.{conv}.{k}.p_one_sided', c['arc'][k]['p'])
        v[f'amplitude.{conv}.detrended'] = c['amp_detrended'][0]; v[f'amplitude.{conv}.raw'] = c['amp_raw'][0]
    if 'amplitude' in R: v['amplitude.W.p_surrogate'] = R['amplitude']['p_surrogate']
    for kind, name in (('gdp_end', 'gdp_end_of_window'), ('equal', 'equal')):
        d = R.get('diversification', {}).get(kind)
        if d:
            for k in ('cross_fraction_of_excess', 'cross_share_crisis', 'cross_share_normal'): v[f'diversification.{name}.{k}'] = d[k]
    if 'structure' in R:
        s = R['structure']; v['identity.alignment_share_of_crisis_excess'] = s['align_share']
        v['identity.p_alignment'] = s['p_align']; v['identity.p_swing'] = s['p_swing']; v['fiedler.lambda2'] = s['lambda2']
    if 'mst' in R:
        s = R['mst']; v['mst.L_1971'] = s['L_by_year'][1971]; v['mst.L_2022'] = s['L_by_year'][2022]
        v['mst.pre_crisis_tau'] = s['tau_L']; v['mst.p_contraction'] = s['p_contraction']
    if 'phase_lags' in R: v['phase.lead_sd_years'] = R['phase_lags']['sd']; v['phase.mean_period_years'] = R['phase_lags']['period_years']
    if 'csd' in R:
        s = R['csd']; v['csd.ar1_tau'] = s['tau_ar1']; v['csd.ar1_p'] = s['p_ar1']; v['csd.var_tau'] = s['tau_var']; v['csd.var_p'] = s['p_var']
    if 'bifurcation' in R: v['bifurcation.delta_lambda'] = R['bifurcation']['stat_real']; v['bifurcation.p_slowing'] = R['bifurcation']['p_slowing_post']
    if 'robustness' in R:
        for k in ('lead2', 'lead1', 'crisis', 'after2'): v[f'robustness.baseline.{k}.corr'] = R['robustness']['baseline'][k][0]
    if sync:
        for ch, tests in sync['tests'].items():
            for k, (c, p) in tests.items(): v[f'atlas_sync.{ch}.{k}.corr'] = c; v[f'atlas_sync.{ch}.{k}.p'] = p
    return v


def golden_table(view, golden_path=None):
    """Rows (key, source, stored, computed, |diff|, tolerance, within, exact) for every golden value."""
    G = json.load(open(golden_path or os.path.join(config.repo_root(), 'tests/golden_paper1.json')))['values']; rows = []
    for g in G:
        got = view.get(g['key']); d = None if got is None else abs(got - g['value'])
        rows.append((g['key'], g['source'], g['value'], got, d, g['tol'], d is not None and d <= g['tol'], d is not None and d <= 1e-12))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--config', default=os.path.join(config.repo_root(), 'configs/runs/paper1_S26_asrun.yaml'))
    ap.add_argument('--out'); ap.add_argument('--only', nargs='*'); ap.add_argument('--golden', action='store_true')
    ap.add_argument('--sync', help='an atlas sync.json for the atlas_sync golden values (default build/data/atlas/sync.json)')
    args = ap.parse_args(argv); cfg = load_run_config(args.config)
    out = run(cfg, args.only)
    path = args.out or os.path.join(config.load()['paths']['build'], 'paper1', f"{cfg['name']}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(out, open(path, 'w'), indent=1, default=float); print(f"wrote {path}")
    if args.golden:
        sp = args.sync or os.path.join(config.load()['paths']['build'], 'data/atlas/sync.json')
        rows = golden_table(golden_view(out['results'], json.load(open(sp)) if os.path.exists(sp) else None))
        bad = [r for r in rows if not r[6]]
        summary = f"{sum(r[6] for r in rows)} of {len(rows)} within tolerance; {sum(r[7] for r in rows)} identical to 1e-12"
        md = ["# Golden check — Paper 1 on S26", "",
              f"`python -m ef.paper1 --golden` with `{os.path.relpath(args.config, config.repo_root())}`, code {out['code_version']}, "
              f"run {out['run_at']}. Stored values from `tests/golden_paper1.json`; atlas_sync from `{os.path.relpath(sp, config.repo_root())}`.", "",
              f"**{summary}.** Tolerance: 1e-9 for deterministic values, the Monte Carlo tolerance for surrogate p-values.", "",
              "| Key | Source | Stored | Computed | Difference | Within tolerance |", "|---|---|---|---|---|---|"]
        md += [f"| {k} | {src} | {st:.12g} | {'—' if got is None else f'{got:.12g}'} | {'—' if d is None else f'{d:.1e}'} | {'yes' if ok else '**no**'} |"
               for k, src, st, got, d, tol, ok, ex in rows]
        rp = os.path.join(os.path.dirname(path), 'GOLDEN.md'); open(rp, 'w').write("\n".join(md) + "\n")
        print(f"golden: {summary} -> {rp}")
        for r in bad: print(f"  NOT MATCHED {r[0]} ({r[1]}): stored {r[2]!r} computed {r[3]!r}")
        sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
