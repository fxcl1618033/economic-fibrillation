"""Phase and amplitude of each economy's cycle from the analytic signal z = cycle + i * Hilbert(cycle):
theta = angle(z), A = |z|.

Where the Hilbert transform is applied changes the results near the edges of the sample (open issue 1), so every
convention is named and available:

  P  the paper's: cycles and Hilbert transform on the whole span (1950-2022), then keep the window (1970-2022)
  W  cycles on the span, cut to the window, then Hilbert (amplitude_test, phase_lags, the companion figures;
     with window 1962-2022 for csd_surrogate and kuramoto_bifurcation)
  N  cycles and Hilbert transform on the window only (no run-in)
  E  edge-robust (new): as P, but each cycle is mirrored at both ends before the Hilbert transform, so the
     transform's edge errors fall on the mirrored years
  C  causal (new): for each year t, cycles and Hilbert transform on the span up to t only, keeping year t. Uses
     past data only, as a forecast must (CLAUDE.md rule 7); the band-pass is still two-sided inside that past.

Inputs are log levels with economies in rows and the years of `years` in columns.
"""
import numpy as np
from scipy.signal import hilbert

from ef.filters import BAND, cycles

CONVENTIONS = ('P', 'W', 'N', 'E', 'C')


def _mask(years, window):
    years = np.asarray(years)
    return (years >= window[0]) & (years <= window[1])


def window_cycles(logs, years, window=(1970, 2022), band=BAND, method='bp'):
    """Cycles computed on the whole span and cut to the window (no Hilbert transform)."""
    c = cycles(logs, method, **({'lo_period': band[0], 'hi_freq': band[1]} if method == 'bp' else {}))
    return c[..., _mask(years, window)]


def analytic(logs, years, window=(1970, 2022), convention='P', band=BAND, method='bp', pad=None):
    """Analytic signal z (economies x window years) under a convention.

    pad: mirror length for convention E (default: the longest period in the band, 9 years) and an optional
    end mirror for C (default none)."""
    logs = np.asarray(logs, dtype=float); years = np.asarray(years); m = _mask(years, window)
    kw = {'lo_period': band[0], 'hi_freq': band[1]} if method == 'bp' else {}
    if convention == 'P':
        return hilbert(cycles(logs, method, **kw), axis=-1)[..., m]
    if convention == 'W':
        return hilbert(cycles(logs, method, **kw)[..., m], axis=-1)
    if convention == 'N':
        return hilbert(cycles(logs[..., m], method, **kw), axis=-1)
    if convention == 'E':
        p = int(round(band[0])) if pad is None else int(pad)
        c = cycles(logs, method, **kw)
        z = hilbert(np.pad(c, [(0, 0)] * (c.ndim - 1) + [(p, p)], mode='reflect'), axis=-1)[..., p:p + c.shape[-1]]
        return z[..., m]
    if convention == 'C':
        idx = np.flatnonzero(m); out = np.empty(logs.shape[:-1] + (len(idx),), dtype=complex)
        for k, t in enumerate(idx):
            c = cycles(logs[..., :t + 1], method, **kw)
            if pad: c = np.pad(c, [(0, 0)] * (c.ndim - 1) + [(0, int(pad))], mode='reflect')
            out[..., k] = hilbert(c, axis=-1)[..., t]
        return out
    raise ValueError(f"unknown convention {convention!r}; one of {CONVENTIONS}")
