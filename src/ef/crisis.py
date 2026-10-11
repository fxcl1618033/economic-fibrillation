"""Tests against the global recessions: the lead-lag arc, the superposed epoch, bootstrap intervals, pre-crisis
trends and multiplicity corrections.

Directions are fixed in advance (CLAUDE.md rule 2): synchronization is predicted to rise before a recession
(leads and the crisis year, upper tail) and to fall after it (lags, lower tail).
"""
import numpy as np

from ef.nulls import lagcorr, p_lower, p_two, p_upper, shift_null

RECESSIONS = (1975, 1982, 1991, 2009, 2020)      # Kose, Sugawara and Terrones (2020)
DOWNTURNS = (1998, 2001, 2012)                     # description only
ARC = (('lead2', 2, 'pos'), ('lead1', 1, 'pos'), ('crisis', 0, 'pos'), ('after1', -1, 'neg'), ('after2', -2, 'neg'))


def indicator(years, events=RECESSIONS):
    return np.isin(np.asarray(years), events).astype(float)


def arc(x, years, events=RECESSIONS, lags=ARC):
    """Lagged correlation of x with the recession indicator, one-sided circular-shift p in the stated direction
    and a two-sided p. Returns {label: {lag, corr, p, p_two, dir}}."""
    g = indicator(years, events); out = {}
    for lab, lag, d in lags:
        obs = lagcorr(np.asarray(x), g, lag); null = shift_null(np.asarray(x), g, lag)
        out[lab] = {'lag': lag, 'corr': float(obs), 'p': float(p_upper(obs, null) if d == 'pos' else p_lower(obs, null)),
                    'p_two': float(p_two(obs, null)), 'dir': d}
    return out


def epoch(x, years, events=RECESSIONS, lags=range(-4, 5)):
    """Superposed epoch: x around each event (events x lags, NaN outside the sample) and its mean across events."""
    yi = {int(y): i for i, y in enumerate(years)}; lags = list(lags)
    M = np.array([[x[yi[e + k]] if (e + k) in yi else np.nan for k in lags] for e in events])
    return M, np.nanmean(M, axis=0)


def bootstrap_mean_ci(v, rng, nb=10000):
    """Mean of v and the 2.5 and 97.5 percentiles of nb bootstrap means (draws as in kose_terrones_test.py)."""
    v = np.asarray(v); bs = [rng.choice(v, len(v), replace=True).mean() for _ in range(nb)]
    return float(np.mean(v)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def tau_pre(ind, years, events=RECESSIONS, pre=8):
    """Mean over events of a Kendall-type trend of `ind` over the `pre` years before each event:
    (pairs rising - pairs falling) / all pairs, on the last axis. Events without a full pre-window are skipped."""
    yi = {int(y): i for i, y in enumerate(years)}; iu = np.triu_indices(pre, 1); taus = []
    for o in events:
        idx = [yi[y] for y in range(o - pre, o) if y in yi]
        if len(idx) < pre: continue
        seg = ind[..., idx]
        if np.isnan(seg).all(axis=-1).any(): continue
        d = seg[..., iu[1]] - seg[..., iu[0]]
        taus.append(np.nansum(np.sign(d), axis=-1) / (0.5 * pre * (pre - 1)))
    return np.nanmean(np.stack(taus, axis=-1), axis=-1)


def bonferroni(p):
    p = np.asarray(p, dtype=float); return np.minimum(1.0, p * len(p))


def benjamini_hochberg(p):
    """Adjusted p-values (q) for false-discovery-rate control, step-up."""
    p = np.asarray(p, dtype=float); m = len(p); o = np.argsort(p)
    q = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
    out = np.empty(m); out[o] = np.minimum(q, 1.0); return out
