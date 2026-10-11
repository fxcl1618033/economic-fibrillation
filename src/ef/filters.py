"""Cycle extraction: the 2-9 year band-pass (the paper's), the HP filter and growth rates (robustness), all applied
to log levels.

Arrays are (economies, years) or one series. The band-pass runs row by row, as the as-run scripts did: filtering
all rows at once gives the same numbers only to about 1e-15, enough to break exact reproduction of surrogate
p-values built on discrete statistics.
"""
from functools import lru_cache

import numpy as np
from scipy.signal import butter, filtfilt

BAND = (9.0, 0.49)          # longest period in years, highest frequency in cycles per year: 2.04-9 years
ORDER = 2


@lru_cache(maxsize=None)
def butter_band(lo_period=BAND[0], hi_freq=BAND[1], order=ORDER):
    """Butterworth band-pass coefficients for annual data (Nyquist 0.5 cycles a year)."""
    return butter(order, [(1 / lo_period) / 0.5, hi_freq / 0.5], btype='band')


def bandpass(x, lo_period=BAND[0], hi_freq=BAND[1], order=ORDER):
    """Forward-backward (zero-phase) band-pass of each row minus its own mean. scipy's filtfilt defaults
    (odd padding, padlen 3 x max(len(a), len(b)) = 15)."""
    b, a = butter_band(lo_period, hi_freq, order)
    x = np.asarray(x, dtype=float)
    if x.ndim == 1: return filtfilt(b, a, x - x.mean())
    return np.array([filtfilt(b, a, row - row.mean()) for row in x])


def hp_cycle(y, lamb=100.0):
    """Hodrick-Prescott cycle of one series (lambda = 100 for annual data), by solving (I + lambda K'K) trend = y."""
    y = np.asarray(y, dtype=float); n = len(y); I = np.eye(n)
    K = np.zeros((n - 2, n))
    for i in range(n - 2): K[i, i], K[i, i + 1], K[i, i + 2] = 1.0, -2.0, 1.0
    return y - np.linalg.solve(I + lamb * K.T @ K, y)


def growth_cycle(y):
    """Year-on-year change of a log series (0 in the first year), minus its mean."""
    g = np.diff(np.asarray(y, dtype=float), prepend=y[0])
    return g - g.mean()


def cycles(x, method='bp', **kw):
    """Cycle of each row by method: 'bp' (band-pass), 'hp' or 'growth'."""
    x = np.asarray(x, dtype=float)
    if method == 'bp': return bandpass(x, **kw)
    f = {'hp': hp_cycle, 'growth': growth_cycle}[method]
    return f(x, **kw) if x.ndim == 1 else np.array([f(row, **kw) for row in x])
