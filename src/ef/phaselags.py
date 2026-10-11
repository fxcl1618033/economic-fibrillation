"""Who leads the world cycle (Methods 6.6): each economy's mean phase relative to the world mean phase psi(t),
converted to years by the mean instantaneous frequency. Descriptive, not causal: it comes from the same cycles."""
import numpy as np


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def mean_frequency(theta):
    """Mean over economies of the mean wrapped year-on-year phase advance (radians a year), theta (N, T)."""
    return float(np.mean([np.mean(wrap(np.diff(theta[i]))) for i in range(theta.shape[0])]))


def leads(theta, omega, psi=None):
    """Lead of each economy over the world phase, in years (positive = ahead). theta (..., N, T)."""
    if psi is None: psi = np.angle(np.exp(1j * theta).mean(axis=-2))
    d = wrap(theta - psi[..., None, :])
    return np.angle(np.exp(1j * d).mean(axis=-1)) / omega
