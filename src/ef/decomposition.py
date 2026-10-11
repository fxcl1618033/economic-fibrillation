"""Loss-of-diversification decomposition (Methods 6.1).

World cycle c(t) = sum_i w_i x_i(t). On each trailing window (10 years, population variances):
  Var(c) = OWN + CROSS,  OWN = sum_i w_i^2 var_i,  CROSS = sum_{i != j} w_i w_j cov_ij.
CROSS rises when economies move together (correlation) or swing harder (size); cross_split separates the two.

Weights: 'equal'; 'gdp_mean', each economy's mean real GDP over the window as a share (what the Methods state);
'gdp_end', the share in the window's last year (what diversification.py did; open issue 4).
"""
import numpy as np

from ef.nulls import p_upper, surrogates


def weights(levels, kind='gdp_mean', win=10):
    """Weights (economies x years); column t is used for the window ending in year t."""
    levels = np.asarray(levels, dtype=float); N, T = levels.shape
    if kind == 'equal': return np.ones((N, T)) / N
    if kind == 'gdp_end': return levels / levels.sum(axis=0, keepdims=True)
    if kind == 'gdp_mean':
        W = np.full((N, T), np.nan)
        for t in range(win - 1, T):
            m = levels[:, t - win + 1:t + 1].mean(axis=1); W[:, t] = m / m.sum()
        return W
    raise ValueError(kind)


def rolling(X, W, win=10):
    """Own term, cross term, total world variance and the weighted mean pairwise correlation, per window end.
    X (..., economies, T); W (economies, T) or matching X. As diversification.py."""
    T = X.shape[-1]; N = X.shape[-2]; lead = X.shape[:-2]
    own = np.full(lead + (T,), np.nan); cross = np.full(lead + (T,), np.nan)
    tot = np.full(lead + (T,), np.nan); rbar = np.full(lead + (T,), np.nan)
    eye = np.eye(N, dtype=bool)
    for t in range(win - 1, T):
        xs = X[..., :, t - win + 1:t + 1]
        w = W[..., :, t] if W.ndim == X.ndim else W[:, t]
        xm = xs - xs.mean(axis=-1, keepdims=True)
        cov = np.einsum('...iw,...jw->...ij', xm, xm) / xs.shape[-1]
        ww = np.einsum('...i,...j->...ij', w, w)
        diag = np.einsum('...ii->...i', cov)
        own_t = np.einsum('...i,...i->...', w * w, diag)
        tot_t = np.einsum('...ij,...ij->...', ww, cov)
        own[..., t] = own_t; cross[..., t] = tot_t - own_t; tot[..., t] = tot_t
        sd = np.sqrt(np.clip(diag, 1e-18, None))
        corr = cov / np.einsum('...i,...j->...ij', sd, sd)
        offw = ww.copy(); offw[..., eye] = 0
        rbar[..., t] = np.einsum('...ij,...ij->...', offw, np.where(eye, 0, corr)) / np.clip(offw.sum(axis=(-1, -2)), 1e-18, None)
    return own, cross, tot, rbar


def crisis_excess(own, cross, tot, years, events):
    """Cross-term share of world variance in recession and normal windows, and the share of the recession excess in
    world variance that comes from the cross term."""
    share = cross / np.clip(tot, 1e-18, None)
    g = np.isin(years, events) & ~np.isnan(share); n = ~np.isin(years, events) & ~np.isnan(share)
    d_own = np.nanmean(own[g]) - np.nanmean(own[n]); d_cross = np.nanmean(cross[g]) - np.nanmean(cross[n])
    return {'cross_share_crisis': float(np.nanmean(share[g])), 'cross_share_normal': float(np.nanmean(share[n])),
            'excess_from_own': float(d_own), 'excess_from_cross': float(d_cross),
            'cross_fraction_of_excess': float(d_cross / (d_own + d_cross))}


def cross_share_null(X, W, years, events, n, rng, win=10, batch=200):
    """Surrogate p for the recession cross share, as diversification.py. It only tests whether economies are
    correlated at all, not the share claim (open issue 6); kept for the record."""
    own, cross, tot, _ = rolling(X, W, win)
    obs = np.nanmean((cross / np.clip(tot, 1e-18, None))[np.isin(years, events) & ~np.isnan(tot)])
    rec = np.isin(years, events)[None, :]; null = []
    for Xs in surrogates(X, n, rng, batch):
        _, cs, to, _ = rolling(Xs, np.broadcast_to(W, Xs.shape), win)
        null.append(np.nanmean(np.where(rec, cs / np.clip(to, 1e-18, None), np.nan), axis=1))
    null = np.concatenate(null)
    return float(obs), float(p_upper(obs, null))


def cross_split(X, W, years, events, win=10):
    """Split the recession rise of the cross term into correlation, swing size and their interaction, from mean
    correlation matrices, cycle s.d. and weights over recession and normal windows (crossterm_split.py)."""
    N, T = X.shape; rho, sd, ww, yrs = [], [], [], []
    for t in range(win - 1, T):
        seg = X[:, t - win + 1:t + 1]; seg = seg - seg.mean(1, keepdims=True)
        rho.append(np.corrcoef(seg)); sd.append(seg.std(1)); ww.append(W[:, t]); yrs.append(years[t])
    rho, sd, ww, yrs = map(np.array, (rho, sd, ww, yrs))
    cm = np.isin(yrs, events); nm = ~cm; off = ~np.eye(N, dtype=bool)

    def cross(R, S, Wv): return (np.outer(Wv * S, Wv * S) * R)[off].sum()
    Rc, Rn, Sc, Sn, Wc, Wn = rho[cm].mean(0), rho[nm].mean(0), sd[cm].mean(0), sd[nm].mean(0), ww[cm].mean(0), ww[nm].mean(0)
    base = cross(Rn, Sn, Wn); tot = cross(Rc, Sc, Wc) - base
    only_rho = cross(Rc, Sn, Wn) - base; only_sd = cross(Rn, Sc, Wn) - base
    return {'recession_windows': [int(y) for y in yrs[cm]], 'corr_normal': float(Rn[off].mean()), 'corr_crisis': float(Rc[off].mean()),
            'sd_normal': float(Sn.mean()), 'sd_crisis': float(Sc.mean()), 'rise': float(tot),
            'from_correlation': float(only_rho / tot), 'from_swing_size': float(only_sd / tot),
            'interaction': float((tot - only_rho - only_sd) / tot)}
