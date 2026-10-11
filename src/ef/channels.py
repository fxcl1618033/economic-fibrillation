"""Inside the economies: synchronization of macroeconomic channels on the repaired atlas panel, for any sample.

sync       atlas/sync.py generalized: real GDP, investment and short-rate synchronization against the recessions
           (registry G1-G3), under convention P (the as-run) or C (past data only).
anatomy    the panel26 channel anatomy rerun on the repaired panel (open issue 12; G4, G5).
contracting, coupling   G7 and G8 on the chosen sample.

Series (pre-registration amendment 1.5): an economy enters a channel only if the channel has continuous data from
1965 to 2022 after at most two-year interpolation, as run.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr

from ef import config, crisis, nulls
from ef.data import gmd

YEARS = np.arange(1970, 2023)
ANATOMY = ['GDP', 'cons', 'inv', 'exports', 'imports', 'govexp', 'balance', 'strate', 'M2']


def load_panel(atlas_dir):
    return pd.read_csv(os.path.join(atlas_dir, 'panel.csv')), json.load(open(os.path.join(atlas_dir, 'meta.json')))


def _b(): return butter(2, [(1 / 9) / 0.5, 0.49 / 0.5], btype='band')


def _prepare(s):
    """As sync.py's cycle(): from the first valid year, interpolate gaps of up to two years; None if the series does
    not cover 1965-2022."""
    s = s.loc[1950:2022]
    if s.first_valid_index() is None: return None
    s = s.loc[s.first_valid_index():].interpolate(limit=2)
    if s.index.min() > 1965 or s.loc[1965:2022].isna().any(): return None
    return s.dropna()


def _phases(s, convention):
    """Phase on 1970-2022 of one prepared series: P (band-pass and Hilbert on the whole series) or C (on data up to
    each year only)."""
    b, a = _b()
    if convention == 'P':
        c = filtfilt(b, a, s.values - s.values.mean()); return np.angle(hilbert(c))[np.isin(s.index, YEARS)]
    out = []
    for y in YEARS:            # an economy has no phase until it has 16 years of history (the filter needs more than 15)
        v = s.loc[:y].values; out.append(np.angle(hilbert(filtfilt(b, a, v - v.mean())))[-1] if len(v) > 15 else np.nan)
    return np.array(out)


def _sync_series(P, G, fix, iso, ch):
    d = P[P.iso == iso].set_index('year')
    if ch == 'GDP': s = np.log(d.rGDP)
    elif ch == 'inv':
        g = G[G.ISO3 == iso].set_index('year').reindex(d.index)
        s = np.log(g.inv / (g.CPI if fix[iso]['contrib_method'] == 'cpi' else d.deflator))
    elif ch == 'strate': s = d.strate
    return s.replace([np.inf, -np.inf], np.nan)


def sync(atlas_dir, isos, recessions, convention='P', channels=('GDP', 'inv', 'strate')):
    """Channel synchronization r(t) and its lead-lag tests (sync.py), for the given economies."""
    P, meta = load_panel(atlas_dir); fix = meta['fixes']
    G = gmd.read(config.raw_file('gmd', 'data/final/data_final.dta'), columns=['ISO3', 'year', 'inv', 'CPI']); G['year'] = G.year.astype(int)
    out = {}
    for ch in channels:
        prep = {i: _prepare(_sync_series(P, G, fix, i, ch)) for i in isos}; prep = {k: v for k, v in prep.items() if v is not None}
        PH = np.array([_phases(s, convention) for s in prep.values()])
        r = np.abs(np.nanmean(np.exp(1j * PH), axis=0)); n_t = (~np.isnan(PH)).sum(0)
        arc = crisis.arc(r, YEARS, recessions, (('lead2', 2, 'pos'), ('lead1', 1, 'pos'), ('same', 0, 'pos'), ('after2', -2, 'neg')))
        out[ch] = {'n': len(prep), 'economies': list(prep), 'tests': {k: [v['corr'], v['p']] for k, v in arc.items()},
                   'tests_rounded': {k: [round(v['corr'], 3), round(v['p'], 3)] for k, v in arc.items()},
                   'r_t': r.tolist(), 'n_with_phase_by_year': dict(zip(YEARS.tolist(), n_t.tolist()))}
    return out


def _anatomy_series(d, ch):
    if ch == 'GDP': s = np.log(d.rGDP)
    elif ch in ('cons', 'inv', 'exports', 'imports'): s = np.log(d['r_' + ch])
    elif ch == 'govexp': s = np.log(d.govexp_GDP / 100 * d.rGDP)
    elif ch == 'balance': s = d.govdef_GDP
    elif ch == 'strate': s = d.strate
    elif ch == 'M2':
        g = (d.real_money_growth / 100).interpolate(limit=2, limit_area='inside')
        if g.loc[1965:2022].isna().any(): return pd.Series(np.nan, index=d.index)
        start = g.loc[:1964][g.loc[:1964].isna()].index.max() if g.loc[:1964].isna().any() else g.index.min() - 1
        g = g.loc[start + 1:]; s = pd.Series(np.r_[0.0, np.cumsum(g.values)], index=np.r_[g.index[0] - 1, g.index])
    return s.replace([np.inf, -np.inf], np.nan)


def anatomy(atlas_dir, isos, recessions, seed=2610, n_batches=40, batch=50):
    """The panel26 channel anatomy on the repaired panel: each channel's synchronization against surrogates (one random
    stream across channels, as run), mean pairwise cycle correlation before and after 1990, and the lead-lag tests."""
    P, _ = load_panel(atlas_dir); rng = np.random.default_rng(seed); b, a = _b(); res = {}
    for ch in ANATOMY:
        cyc = {}
        for iso in isos:
            s = _prepare(_anatomy_series(P[P.iso == iso].set_index('year'), ch))
            if s is not None and len(s) >= 40: cyc[iso] = pd.Series(filtfilt(b, a, s.values - s.values.mean()), index=s.index)
        isos_c = list(cyc); M = np.array([cyc[i].reindex(YEARS).values for i in isos_c])
        PH = np.array([np.angle(hilbert(cyc[i].values))[np.isin(cyc[i].index, YEARS)] for i in isos_c])
        r = np.abs(np.exp(1j * PH).mean(0))

        def mpc(lo, hi):
            m = (YEARS >= lo) & (YEARS <= hi); cc = np.corrcoef(M[:, m]); return float(np.nanmean(cc[np.triu_indices(len(isos_c), 1)]))
        XL = [cyc[i].values for i in isos_c]; L = min(len(x) for x in XL); Xs = np.array([x[-L:] for x in XL])
        amp = np.abs(np.fft.rfft(Xs, axis=1)); nf = amp.shape[1]; nr = []
        for _ in range(n_batches):
            rp = rng.uniform(0, 2 * np.pi, (batch, len(isos_c), nf)); rp[..., 0] = 0
            if L % 2 == 0: rp[..., -1] = 0
            S = np.fft.irfft(amp[None] * np.exp(1j * rp), n=L, axis=-1)
            ph = np.angle(hilbert(S, axis=-1))[..., -len(YEARS):]; nr.append(np.abs(np.exp(1j * ph).mean(1)).mean(1))
        nr = np.concatenate(nr)
        arc = crisis.arc(r, YEARS, recessions, (('lead2', 2, 'pos'), ('lead1', 1, 'pos'), ('crisis', 0, 'pos'), ('after2', -2, 'neg')))
        res[ch] = {'n': len(isos_c), 'economies': isos_c, 'mean_r': float(r.mean()), 'null_r': float(nr.mean()),
                   'p_sync': float((1 + np.sum(nr >= r.mean())) / (1 + len(nr))),
                   'paircorr_pre90': mpc(1970, 1989), 'paircorr_post90': mpc(1990, 2022)} | {k: [v['corr'], v['p']] for k, v in arc.items()}
    return res


def contracting(atlas_dir, isos, recessions):
    """G7: how many of the sample's economies had negative growth in each recession year."""
    P, _ = load_panel(atlas_dir); gr = P[P.iso.isin(isos)].pivot(index='year', columns='iso', values='growth')
    return {int(y): int((gr.loc[y] < 0).sum()) for y in recessions}


def coupling(atlas_dir, isos):
    """G8: each economy's correlation with the mean standardized cycle of the rest of the sample, 1970-89 and
    1990-2022, averaged over the sample (atlas data.py and stats.py, with the sample as the rest)."""
    P, _ = load_panel(atlas_dir)
    W = P.pivot(index='year', columns='iso', values='cycle').loc[1955:2022, isos]
    Z = (W - W.loc[1970:2022].mean()) / W.loc[1970:2022].std(); out = {}
    for lo, hi in ((1970, 1989), (1990, 2022)):
        v = []
        for iso in isos:
            x = pd.concat([W[iso], Z[[i for i in isos if i != iso]].mean(axis=1)], axis=1).loc[lo:hi].dropna()
            if len(x) >= 8: v.append(float(np.corrcoef(x.iloc[:, 0], x.iloc[:, 1])[0, 1]))
        out[f'{lo}-{hi}'] = float(np.mean(v))
    return out


def run(atlas_dir, isos, recessions, convention='P'):
    """Every channel test for a sample: sync (G1-G3), anatomy (G4, G5), contracting (G7), coupling (G8)."""
    if convention == 'C': return {'sync': sync(atlas_dir, isos, recessions, 'C')}
    return {'sync': sync(atlas_dir, isos, recessions, 'P'), 'anatomy': anatomy(atlas_dir, isos, recessions),
            'contracting': contracting(atlas_dir, isos, recessions), 'coupling': coupling(atlas_dir, isos)}
