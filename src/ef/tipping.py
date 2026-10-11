"""Early-warning (tipping) indicators on r(t) (Methods 6.7).

Fluctuations of r around a Gaussian-smoothed trend; on trailing windows: lag-1 autocorrelation phi, variance, the
recovery rate lambda = -ln(phi) and the restoring time 1/lambda. Critical slowing down before a bifurcation means
phi and variance rise and the recovery rate falls (the restoring time rises).

Coupling as the bifurcation parameter: inverting the mean-field Kuramoto relation r = sqrt(1 - Kc/K) gives the
implied coupling K/Kc = 1 / (1 - r^2).
"""
import numpy as np
from scipy.ndimage import gaussian_filter1d


def fluctuations(r, sigma=5.0):
    return r - gaussian_filter1d(r, sigma, axis=-1)


def rolling_ar1_var(r, win=15, sigma=5.0):
    """Lag-1 autocorrelation and variance of the fluctuations on trailing windows (csd_surrogate.py)."""
    fl = fluctuations(r, sigma); T = fl.shape[-1]; shp = fl.shape[:-1]
    ar = np.full(shp + (T,), np.nan); va = np.full(shp + (T,), np.nan)
    for t in range(win - 1, T):
        seg = fl[..., t - win + 1:t + 1]; seg = seg - seg.mean(axis=-1, keepdims=True)
        x1, x2 = seg[..., :-1], seg[..., 1:]; s1 = x1.std(axis=-1); s2 = x2.std(axis=-1)
        with np.errstate(invalid='ignore', divide='ignore'):
            ar[..., t] = np.where((s1 > 0) & (s2 > 0), (x1 * x2).mean(axis=-1) / (s1 * s2), np.nan)
        va[..., t] = seg.var(axis=-1)
    return ar, va


def recovery_rate(r, win=12, sigma=5.0):
    """lambda(t) = -ln(phi), phi the trailing lag-1 autocorrelation clipped to [1e-4, 0.9999] (kuramoto_bifurcation.py)."""
    fl = fluctuations(r, sigma); T = fl.shape[-1]; lam = np.full(fl.shape[:-1] + (T,), np.nan)
    for t in range(win - 1, T):
        seg = fl[..., t - win + 1:t + 1]; seg = seg - seg.mean(axis=-1, keepdims=True)
        x1, x2 = seg[..., :-1], seg[..., 1:]; s1 = x1.std(axis=-1); s2 = x2.std(axis=-1)
        with np.errstate(invalid='ignore', divide='ignore'):
            phi = np.clip(np.where((s1 > 0) & (s2 > 0), (x1 * x2).mean(axis=-1) / (s1 * s2), np.nan), 1e-4, 0.9999)
            lam[..., t] = -np.log(phi)
    return lam


def restoring_time(r, win=15, sigma=5.0):
    """1 / lambda in years, from the same trailing lag-1 autocorrelation as rolling_ar1_var. A reconstruction of the
    third indicator, whose script (csd_fast.py) was lost (open issue 10): its exact definition is not recorded."""
    return 1.0 / recovery_rate(r, win, sigma)


def implied_coupling(r):
    """K/Kc = 1 / (1 - r^2) from the mean-field Kuramoto relation (clipped below at 1e-6)."""
    return 1.0 / np.clip(1.0 - r ** 2, 1e-6, None)


def post_minus_base(lam, years, events, post=(0, 1, 2)):
    """Mean recovery rate in the years t..t+2 after each event minus its mean in all other years."""
    yi = {int(y): i for i, y in enumerate(years)}; T = len(years)
    idx = sorted({yi[o + k] for o in events for k in post if (o + k) in yi})
    mask = np.zeros(T, bool); mask[idx] = True
    with np.errstate(invalid='ignore'):
        return np.nanmean(np.where(mask, lam, np.nan), axis=-1) - np.nanmean(np.where(~mask, lam, np.nan), axis=-1)
