"""Synchronization measures from analytic signals z (economies in the second-to-last axis, years in the last).

  r(t)     Kuramoto order parameter |mean_i exp(i theta_i)|: phase alignment only
  psi(t)   its angle, the world mean phase
  Abar(t)  mean amplitude (swing size)
  Z(t)     world phasor mean_i A_i exp(i theta_i)
  R_A(t)   amplitude-weighted alignment |sum A_i exp(i theta_i)| / sum A_i
Fibrillation identity: |Z| = Abar x R_A exactly, so world swing = swing size x alignment.
"""
import numpy as np


def r_psi(z, weights=None):
    """Order parameter and mean phase. weights (economies x years, summing to 1 over economies) gives the
    weighted version used by the diversification scripts."""
    u = np.exp(1j * np.angle(z))
    if weights is None:      # NaN marks an economy with no phase that year (a late entrant): mean over the others
        m = np.nanmean(u, axis=-2) if np.isnan(z).any() else u.mean(axis=-2)
    else:
        m = (weights * u).sum(axis=-2)
    return np.abs(m), np.angle(m)


def r(z, weights=None):
    return r_psi(z, weights)[0]


def mean_amplitude(z):
    return np.nanmean(np.abs(z), axis=-2) if np.isnan(z).any() else np.abs(z).mean(axis=-2)


def world_phasor(z):
    return z.mean(axis=-2)


def amplitude_alignment(z):
    """R_A: alignment of the phases weighted by each economy's swing size."""
    return np.abs(z.sum(axis=-2)) / np.abs(z).sum(axis=-2)


def identity_error(z):
    """max | |Z|^2 - Abar^2 R_A^2 |: zero up to floating-point rounding."""
    A = np.abs(z); TH = np.angle(z)
    Zs = (A * np.exp(1j * TH)).mean(axis=-2); Abar = A.mean(axis=-2)
    RA = np.abs((A * np.exp(1j * TH)).sum(axis=-2)) / A.sum(axis=-2)
    return float(np.max(np.abs(np.abs(Zs) ** 2 - Abar ** 2 * RA ** 2)))
