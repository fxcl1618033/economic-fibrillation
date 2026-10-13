"""Pre-registration amendment 4 (docs/preregistration_S30.md): edge-matched nulls for the Paper 1 tests whose
statistic leans on 2019-2022, the last years of the data.

    python -m ef.edge_null validate     # on the G1 worlds -> results/edge_matched/validation.csv.gz
    python -m ef.edge_null run          # S31, S30, S26 -> results/edge_matched/<sample>.json
    python -m ef.edge_null report       # -> results/EDGE_MATCHED.md

The current surrogates randomize the phases of each economy's band-passed cycle over 1950-2022, so they wrap around and
have no ends. Edge-matched surrogates are made one step earlier and go through the whole pipeline: growth rates
(72 values) -> a long series of 8 x 72 values with the same periodogram (each frequency takes the amplitude of the
nearest of the 72-point frequencies, scaled by sqrt(8); random phases; the zero frequency keeps the mean growth) ->
72 consecutive values from a random start, cumulated from the real 1950 level -> the same band-pass, Hilbert transform,
convention and windows as the real data. Independent: phases drawn per economy. Multivariate: one random phase per
frequency added to every economy's real phase, so co-movement (and r's level and persistence) is kept and only the
timing against the calendar is random. Statistics and directions are Paper 1's (ef.paper1); only the null changes.
"""
import argparse
import datetime
import json
import os
import warnings

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.signal import filtfilt, hilbert

from ef import channels, config, crisis, decomposition, network, order, paper1, tipping
from ef.filters import BAND, butter_band
from ef.nulls import p_lower, p_upper
from ef.phases import window_cycles

FINE = 8
SEEDS = {'ind': 6001, 'multi': 6002, 'channel': 6003}
N_SUR, BATCH = 5000, 250
SAMPLES = {'S31': 'configs/runs/phase3_s31.yaml', 'S30': 'configs/runs/phase3.yaml', 'S26': 'configs/runs/phase3.yaml'}
PANELS = {'S31': 'build/data/atlas_s31', 'S30': 'build/data/atlas', 'S26': 'build/data/atlas'}
OUT = os.path.join(config.repo_root(), 'results', 'edge_matched')
ARC_LAGS = (('lead1', 1, 'pos'), ('crisis', 0, 'pos'), ('after1', -1, 'neg'), ('after2', -2, 'neg'))
CHANNEL_LAGS = (('lead1', 1, 'pos'), ('same', 0, 'pos'), ('after2', -2, 'neg'))


# ------------------------------------------------------------------ the surrogates

def _spectrum_map(Tg, fine=FINE):
    """For each frequency of the long series (fine x Tg values), the index of the nearest Tg-point frequency; the
    frequencies below the lowest resolved one take its amplitude."""
    k = np.arange(fine * Tg // 2 + 1); j = np.floor(k / fine + 0.5).astype(int)
    j[1:] = np.maximum(j[1:], 1); return np.minimum(j, Tg // 2)


def long_growth(g, nb, rng, multivariate, fine=FINE):
    """nb long surrogate growth series (nb, N, fine x Tg) with each economy's periodogram (see the module notes)."""
    N, Tg = g.shape; M = fine * Tg; G = np.fft.rfft(g, axis=-1); j = _spectrum_map(Tg, fine)
    amp = np.abs(G)[:, j] * np.sqrt(fine); nf = amp.shape[-1]
    if multivariate:
        ph = np.angle(G)[:, j][None] + rng.uniform(0, 2 * np.pi, size=(nb, 1, nf))
    else:
        ph = rng.uniform(0, 2 * np.pi, size=(nb, N, nf))
    X = amp[None] * np.exp(1j * ph)
    X[..., 0] = fine * G[:, 0].real                      # the mean growth
    X[..., -1] = X[..., -1].real                         # the Nyquist frequency stays real
    return np.fft.irfft(X, n=M, axis=-1)


def surrogate_logs(logs, n, rng, multivariate, batch=BATCH, fine=FINE):
    """Batches (nb, N, T) of edge-matched surrogate log levels: a window of the long growth series from a random start
    (common to all economies), cumulated from the real first level."""
    logs = np.asarray(logs, dtype=float); g = np.diff(logs, axis=-1); N, Tg = g.shape
    for s0 in range(0, n, batch):
        nb = min(batch, n - s0); Lg = long_growth(g, nb, rng, multivariate, fine)
        start = rng.integers(0, Lg.shape[-1] - Tg + 1, size=nb)
        w = np.stack([Lg[b, :, s:s + Tg] for b, s in enumerate(start)])
        yield logs[None, :, :1] + np.concatenate([np.zeros((nb, N, 1)), np.cumsum(w, axis=-1)], axis=-1)


def _bp(x, band=BAND):
    """The band-pass of ef.filters.bandpass on the last axis of any array (each series minus its own mean)."""
    b, a = butter_band(*band); return filtfilt(b, a, x - x.mean(axis=-1, keepdims=True), axis=-1)


def pipeline(L, years, band=BAND, conventions=('P',)):
    """Cycles and analytic signals of a batch of log levels (..., N, T over 1950-2022), as ef.phases does for the real
    data: 'X62' the cycles cut to 1962-2022, 'z62' and 'z70' convention P on 1962-2022 and 1970-2022, and the arc's
    other conventions on 1970-2022."""
    years = np.asarray(years); m62 = (years >= 1962) & (years <= 2022); m70 = (years >= 1970) & (years <= 2022)
    C = _bp(L, band); H = hilbert(C, axis=-1); out = {'X62': C[..., m62], 'z62': H[..., m62], 'z70': H[..., m70]}
    for conv in conventions:
        if conv == 'P': out['P'] = out['z70']
        elif conv == 'W': out['W'] = hilbert(C[..., m70], axis=-1)
        elif conv == 'N': out['N'] = hilbert(_bp(L[..., m70], band), axis=-1)
        elif conv == 'E':
            p = int(round(band[0])); pad = [(0, 0)] * (C.ndim - 1) + [(p, p)]
            out['E'] = hilbert(np.pad(C, pad, mode='reflect'), axis=-1)[..., p:p + C.shape[-1]][..., m70]
    return out


# ------------------------------------------------------------------ the statistics (Paper 1's, vectorized)

def lagcorr(x, g, lag):
    """nulls.lagcorr on the last axis of any array."""
    if lag > 0: u, v = x[..., :-lag], g[lag:]
    elif lag < 0: u, v = x[..., -lag:], g[:lag]
    else: u, v = x, g
    u = u - u.mean(axis=-1, keepdims=True); v = v - v.mean()
    return (u * v).sum(axis=-1) / np.sqrt((u * u).sum(axis=-1) * (v * v).sum())


def _g(x, s): return x - gaussian_filter1d(x, s, axis=-1)


def _detr(x, sig):
    """run_mst's detrending of L(t), on the years every series defines."""
    ok = ~np.isnan(x).any(axis=tuple(range(x.ndim - 1))) if x.ndim > 1 else ~np.isnan(x)
    d = np.full_like(x, np.nan); d[..., ok] = x[..., ok] - gaussian_filter1d(x[..., ok], sig, axis=-1); return d


class Stats:
    """Every listed statistic for real data or a batch of surrogate worlds, with the settings of the Phase 3 run."""

    def __init__(self, cfg, levels, years, in_a):
        self.cfg, self.t = cfg, cfg['tests']; self.years = np.asarray(years)
        self.y70 = np.arange(1970, 2023); self.y62 = np.arange(1962, 2023); rec = cfg['recessions']
        self.g70 = crisis.indicator(self.y70, rec); self.cm = self.g70 == 1; self.rec = rec
        m62 = (self.years >= 1962) & (self.years <= 2022)
        self.W = {k: decomposition.weights(levels[:, m62], k, self.t['diversification']['win']) for k in self.t['diversification']['weights']}
        self.in_a = in_a

    def multi(self, z_by_conv):
        """Arcs (multivariate null): r under each convention at lead-1, crisis, after-1, after-2; the bloc arcs."""
        out = {}
        for conv, z in z_by_conv.items():
            r = order.r(z)
            for lab, lag, _ in ARC_LAGS: out[f'arc.{conv}.{lab}'] = lagcorr(r, self.g70, lag)
            if conv == 'P':
                rw, rb = network.bloc_alignment(np.angle(z), self.in_a)
                out['E11.within.lead1'] = lagcorr(rw, self.g70, 1); out['E11.between.lead1'] = lagcorr(rb, self.g70, 1)
        return out

    def ind(self, d):
        """The independent-null statistics from pipeline() output."""
        t, out = self.t, {}
        z = d['z70']; lr = 2 * np.log(order.amplitude_alignment(z)); la = 2 * np.log(order.mean_amplitude(z))
        out['D11.align'] = lr[..., self.cm].mean(-1) - lr[..., ~self.cm].mean(-1)
        out['D11.swing'] = la[..., self.cm].mean(-1) - la[..., ~self.cm].mean(-1)
        s = t['amplitude']['detrend_sigma']; rc = _g(order.r(z), s); ac = _g(order.mean_amplitude(z), s)
        rc = rc - rc.mean(-1, keepdims=True); ac = ac - ac.mean(-1, keepdims=True)
        out['C1'] = (rc * ac).mean(-1) / (rc.std(-1) * ac.std(-1))
        X = d['X62']; rec = np.isin(self.y62, self.rec)
        for k, W in self.W.items():
            own, cs, to, _ = decomposition.rolling(X, np.broadcast_to(W, X.shape) if X.ndim > 2 else W, t['diversification']['win'])
            share = cs / np.clip(to, 1e-18, None); ok = ~np.isnan(to)
            out[f'D5.{k}'] = np.nanmean(np.where(rec & ok, share, np.nan), axis=-1)
            okv = ok if ok.ndim == 1 else ok[0]; g, m = rec & okv, ~rec & okv
            do = own[..., g].mean(-1) - own[..., m].mean(-1); dc = cs[..., g].mean(-1) - cs[..., m].mean(-1)
            out[f'D6.cross.{k}'] = dc; out[f'D6.own.{k}'] = do; out[f'D6.ratio.{k}'] = dc / (do + dc)
        ms = t['mst']; C = network.corr_windows(X, ms['win'])
        L, M = network.mst_stats(C if C.ndim == 4 else C[None], ms['win'])
        if C.ndim == 3: L, M = L[0], M[0]
        kt = dict(pre=ms['pre'], strict=ms.get('strict', False))
        out['E4.raw'] = crisis.tau_pre(L, self.y62, self.rec, **kt)
        out['E4.detrended'] = crisis.tau_pre(_detr(L, ms['detrend_sigma']), self.y62, self.rec, **kt)
        out['E6'] = crisis.tau_pre(M, self.y62, self.rec, **kt)
        r62 = order.r(d['z62']); cs_ = t['csd']; kc = dict(pre=cs_['pre'], strict=cs_.get('strict', False))
        ar, va = tipping.rolling_ar1_var(r62, win=cs_['win'], sigma=cs_['sigma'])
        out['F1'] = crisis.tau_pre(ar, self.y62, self.rec, **kc); out['F2'] = crisis.tau_pre(va, self.y62, self.rec, **kc)
        bf = t['bifurcation']
        out['F4'] = tipping.post_minus_base(tipping.recovery_rate(r62, win=bf['win'], sigma=bf['sigma']), self.y62, self.rec)
        return out


# test id: (label, null, direction)
TESTS = {**{f'arc.{c}.{l}': (f"Arc, {l.replace('after', 'after-').replace('lead', 'lead-').replace('crisis', 'crisis year')}, convention {c}", 'multi', d)
            for c in 'PWNE' for l, _, d in ARC_LAGS},
         'E11.within.lead1': ('Arc within the Fiedler blocs, lead-1', 'multi', 'pos'),
         'E11.between.lead1': ('Arc between the Fiedler blocs, lead-1', 'multi', 'pos'),
         'G3.lead1': ('Real-GDP channel arc, lead-1', 'channel', 'pos'), 'G3.same': ('Real-GDP channel arc, crisis year', 'channel', 'pos'),
         'G3.after2': ('Real-GDP channel arc, after-2', 'channel', 'neg'),
         'D5.gdp_mean': ('Cross share at recessions, GDP weights', 'ind', 'pos'), 'D5.equal': ('Cross share at recessions, equal weights', 'ind', 'pos'),
         'D6.ratio.gdp_mean': ('Share of the excess from the cross term, GDP weights', 'ind', 'pos'),
         'D6.ratio.equal': ('Share of the excess from the cross term, equal weights', 'ind', 'pos'),
         'D6.cross.gdp_mean': ('Δcross at recessions, GDP weights', 'ind', 'pos'), 'D6.cross.equal': ('Δcross at recessions, equal weights', 'ind', 'pos'),
         'D6.own.gdp_mean': ('Δown at recessions, GDP weights', 'ind', 'pos'), 'D6.own.equal': ('Δown at recessions, equal weights', 'ind', 'pos'),
         'D11.align': ('Identity: alignment at recessions', 'ind', 'pos'), 'D11.swing': ('Identity: swing size at recessions', 'ind', 'pos'),
         'E4.raw': ('MST contraction before recessions', 'ind', 'neg'), 'E4.detrended': ('MST contraction, detrended', 'ind', 'neg'),
         'E6': ('MST fragility before recessions', 'ind', 'pos'), 'F1': ('Slowing down: autocorrelation of r', 'ind', 'pos'),
         'F2': ('Slowing down: variance of r', 'ind', 'pos'), 'F4': ('Slower recovery after recessions', 'ind', 'neg'),
         'C1': ('r with swing size, detrended (outside the rule)', 'ind', 'pos')}


def p_of(obs, null, direction): return float(p_upper(obs, null) if direction == 'pos' else p_lower(obs, null))


# ------------------------------------------------------------------ one data set

def edge_pvalues(D, cfg, n, seeds, conventions=('P', 'W', 'N', 'E'), in_a=None, kinds=('ind', 'multi')):
    """Observed statistics and edge-matched p-values for one data set (a paper1.Data). Returns {test: (obs, p, null
    mean)} for the Maddison tests (not the channel arc)."""
    yrs = D.years
    if in_a is None: in_a = network.fiedler(window_cycles(D.logs, D.years, tuple(cfg['window']), cfg['band']))[1]
    st = Stats(cfg, D.levels, yrs, in_a)
    d = pipeline(D.logs, yrs, cfg['band'], conventions)
    obs = (st.multi({c: d[c] for c in conventions}) if 'multi' in kinds else {}) | (st.ind(d) if 'ind' in kinds else {})
    nul = {k: [] for k in obs}
    for kind, multi in (('ind', False), ('multi', True)):
        if kind not in kinds: continue
        rng = np.random.default_rng(seeds[kind])
        for L in surrogate_logs(D.logs, n, rng, multi):
            ds = pipeline(L, yrs, cfg['band'], conventions if multi else ('P',))
            res = st.multi({c: ds[c] for c in conventions}) if multi else st.ind(ds)
            for k, v in res.items(): nul[k].append(np.asarray(v))
    out = {}
    for k, v in obs.items():
        nl = np.concatenate(nul[k]); out[k] = (float(v), p_of(float(v), nl, TESTS[k][2]), float(np.nanmean(nl)))
    return out


def channel_pvalues(atlas_dir, isos, rec, n, seed):
    """The real-GDP channel arc (G3) against multivariate edge-matched surrogates of the channel series: spectra and
    phases from the common span 1966-2022 growth rates; each economy's surrogate cut to its own length ending in 2022,
    cumulated from its real first value and passed through channels._phases (convention P)."""
    P, meta = channels.load_panel(atlas_dir); fix = meta['fixes']
    prep = {i: channels._prepare(channels._sync_series(P, None, fix, i, 'GDP')) for i in isos}
    prep = {k: v for k, v in prep.items() if v is not None}
    Y = channels.YEARS; g = crisis.indicator(Y, rec)

    def r_of(series):
        PH = np.array([channels._phases(s, 'P') for s in series]); return np.abs(np.nanmean(np.exp(1j * PH), axis=0))
    r = r_of(prep.values()); obs = {f'G3.{l}': lagcorr(r, g, lag) for l, lag, _ in CHANNEL_LAGS}
    common = np.array([s.loc[1965:2022].to_numpy() for s in prep.values()]); gc = np.diff(common, axis=-1)
    lens = [len(s) - 1 for s in prep.values()]; rng = np.random.default_rng(seed); nul = {k: [] for k in obs}
    for s0 in range(0, n, BATCH):
        nb = min(BATCH, n - s0); Lg = long_growth(gc, nb, rng, True)
        end = rng.integers(max(lens), Lg.shape[-1] + 1, size=nb)
        for b in range(nb):
            ser = [pd.Series(s.iloc[0] + np.concatenate([[0.0], np.cumsum(Lg[b, i, end[b] - ln:end[b]])]), index=s.index)
                   for i, (s, ln) in enumerate(zip(prep.values(), lens))]
            rs = r_of(ser)
            for l, lag, _ in CHANNEL_LAGS: nul[f'G3.{l}'].append(lagcorr(rs, g, lag))
    return {k: (float(v), p_of(float(v), np.array(nul[k]), TESTS[k][2]), float(np.mean(nul[k]))) for k, v in obs.items()}, list(prep)


# ------------------------------------------------------------------ the current p-values, for the side-by-side table

def current(sample):
    R = lambda t, c='P': json.load(open(os.path.join(config.repo_root(), 'results', sample, c, f'{t}.json')))['results']
    a, cv, st, dv, ms, cs, bf, am, ch = (R('arc'), R('conventions'), R('structure'), R('diversification'), R('mst'), R('csd'),
                                          R('bifurcation'), R('amplitude'), R('channels'))
    out = {}
    for c in 'PWNE':
        arc = a['arc'] if c == 'P' else cv[c]['arc']
        for l, _, _ in ARC_LAGS: out[f'arc.{c}.{l}'] = (arc[l]['corr'], arc[l]['p'])
    for w in ('within', 'between'): x = st['hier'][f'r_{w}']['lead1']; out[f'E11.{w}.lead1'] = (x['corr'], x['p'])
    for l, _, _ in CHANNEL_LAGS: out[f'G3.{l}'] = tuple(ch['sync']['GDP']['tests'][l])
    for k in ('gdp_mean', 'equal'):
        x = dv[k]; out[f'D5.{k}'] = (x['cross_share_crisis'], x['p_surrogate'])
        out[f'D6.ratio.{k}'] = (x['cross_fraction_of_excess'], x['d6']['p_ratio_nominal'])
        out[f'D6.cross.{k}'] = (x['excess_from_cross'], x['d6']['p_excess_cross']); out[f'D6.own.{k}'] = (x['excess_from_own'], x['d6']['p_excess_own'])
    out['D11.align'] = (st['dR'], st['p_align']); out['D11.swing'] = (st['dA'], st['p_swing'])
    out['E4.raw'] = (ms['tau_L'], ms['p_contraction']); out['E4.detrended'] = (ms['tau_L_detrended'], ms['p_contraction_detrended'])
    out['E6'] = (ms['tau_lambdamax'], ms['p_fragility']); out['F1'] = (cs['tau_ar1'], cs['p_ar1']); out['F2'] = (cs['tau_var'], cs['p_var'])
    out['F4'] = (bf['stat_real'], bf['p_slowing_post']); out['C1'] = (am['corr_detrended'], am['p_surrogate'])
    return out


def run(samples=('S31', 'S30', 'S26')):
    warnings.filterwarnings('ignore'); os.makedirs(OUT, exist_ok=True)
    for s in samples:
        cfg = paper1.load_run_config(os.path.join(config.repo_root(), SAMPLES[s])); D = paper1.load_data(s, tuple(cfg['span']))
        res = edge_pvalues(D, cfg, N_SUR, SEEDS)
        chres, ch_isos = channel_pvalues(os.path.join(config.repo_root(), PANELS[s]), D.isos, cfg['recessions'], N_SUR, SEEDS['channel'])
        res |= chres; cur = current(s); bad = []
        for k, (o, p, m) in res.items():
            if abs(o - cur[k][0]) > 1e-9 * max(1, abs(o)): bad.append((k, o, cur[k][0]))
        if bad: raise SystemExit(f"{s}: recomputed statistics differ from the stored ones: {bad}")
        json.dump({'sample': s, 'economies': D.isos, 'channel_economies': ch_isos, 'surrogates': N_SUR, 'seeds': SEEDS, 'fine': FINE,
                   'code_version': paper1.code_version(), 'run_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                   'tests': {k: {'label': TESTS[k][0], 'null': TESTS[k][1], 'direction': TESTS[k][2], 'stat': o, 'p_edge': p,
                                 'null_mean': m, 'p_current': cur[k][1]} for k, (o, p, m) in res.items()}},
                  open(os.path.join(OUT, f'{s}.json'), 'w'), indent=1)
        print(f"{s}: wrote {OUT}/{s}.json", flush=True)


# ------------------------------------------------------------------ validation on the G1 worlds (amendment 4.3)

G1_PAIRS = {'arc.P.lead1': 'arc.lead1', 'arc.P.crisis': 'arc.crisis', 'arc.P.after1': 'arc.after1', 'arc.P.after2': 'arc.after2',
            'D11.align': 'structure.p_align', 'D11.swing': 'structure.p_swing', 'D5.gdp_mean': 'diversification.gdp_mean',
            'D5.equal': 'diversification.equal', 'E4.raw': 'mst.p_contraction', 'E4.detrended': 'mst.p_contraction_detrended',
            'E6': 'mst.p_fragility', 'F1': 'csd.p_ar1', 'F2': 'csd.p_var', 'F4': 'bifurcation.p_slowing', 'C1': 'amplitude.p_surrogate'}
_V = {}


def _vinit():
    from ef.gnn import g1, simulator as S
    warnings.filterwarnings('ignore'); _V['T'] = S.targets()
    cfg = g1.run_config(); _V['cfg'] = cfg
    _V['cfg_p3'] = dict(cfg, tests={k: dict(v, convention='P') if k in ('diversification', 'mst') else v for k, v in cfg['tests'].items()})


def _validate(args):
    """One G1 world on the real calendar: edge-matched p for every listed Maddison test (uncoupled worlds) or for the
    arc's multivariate null only (coupled worlds), 199 surrogates; for uncoupled worlds also the cross-term and MST tests
    under Phase 3's own surrogate scheme (convention P), which the G1 run did not use."""
    from ef.gnn import simulator as S
    model, mi, cell, ci, w, sig, m = args; cfg = _V['cfg']; D = S.to_data(sig, _V['T'], model, m)
    seeds = {'ind': [SEEDS['ind'], mi, ci, w], 'multi': [SEEDS['multi'], mi, ci, w]}
    kinds = ('ind', 'multi') if cell == 'null' else ('multi',)
    res = edge_pvalues(D, cfg, 199, seeds, conventions=('P',), kinds=kinds)
    rows = [(model, cell, w, k, 'edge', v[1]) for k, v in res.items()]
    if cell == 'null':
        c3 = _V['cfg_p3']; t = dict(c3['tests']['diversification'], seed=SEEDS['ind'] + w)
        dv = paper1.run_diversification(D, c3, t)
        rows += [(model, cell, w, f'D5.{k}', 'phase3_scheme', dv[k]['p_surrogate']) for k in dv]
        ms = paper1.run_mst(D, c3, dict(c3['tests']['mst'], seed=SEEDS['multi'] + w))
        rows += [(model, cell, w, k, 'phase3_scheme', ms[f]) for k, f in (('E4.raw', 'p_contraction'), ('E4.detrended', 'p_contraction_detrended'), ('E6', 'p_fragility'))]
    return rows


def validate(n_worlds=1000, processes=None):
    from multiprocessing import Pool
    from ef.gnn import g1, simulator as S
    cal = json.load(open(os.path.join(g1.OUT, 'calibration.json'))); T = S.targets(); Wy, _ = g1.network(); rows = []
    with Pool(processes or max(1, (os.cpu_count() or 2) - 1), initializer=_vinit) as pool:
        for mi, model in enumerate(S.MODELS):
            c = cal[model]
            for ci, (cell, km, pm) in enumerate(g1.CELLS):
                if cell not in ('null', 'network'): continue
                rng = np.random.default_rng([g1.DESIGN['seed_cells'], mi, ci]); sig = []          # the G1 worlds, regenerated
                for s0 in range(0, n_worlds, g1.DESIGN['chunk']):
                    nb = min(g1.DESIGN['chunk'], n_worlds - s0)
                    sig.append(S.simulate(model, Wy, T['omega'], km * c['kappa_star'], pm * c['phi_star'], c['sigma'], rng, nb, mu=c['mu']))
                sig = np.concatenate(sig)
                for r_ in pool.imap_unordered(_validate, [(model, mi, cell, ci, w, sig[w], c['m']) for w in range(len(sig))], chunksize=4):
                    rows += r_
                print(model, cell, 'validated', flush=True)
    os.makedirs(OUT, exist_ok=True)
    V = pd.DataFrame(rows, columns=['model', 'cell', 'world', 'test', 'null', 'p']).sort_values(['model', 'cell', 'world', 'test', 'null'])
    V.to_csv(os.path.join(OUT, 'validation.csv.gz'), index=False, float_format='%.6g', compression={'method': 'gzip', 'mtime': 0})


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('step', choices=['validate', 'run', 'report']); ap.add_argument('--processes', type=int)
    a = ap.parse_args(argv)
    if a.step == 'validate': validate(processes=a.processes)
    elif a.step == 'run': run()
    else:
        from ef import edge_report; edge_report.main()


if __name__ == '__main__':
    main()
