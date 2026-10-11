"""The two nulls of Paper 1.

Circular shift: the recession indicator is rotated by k = 1..T-1 years and the statistic recomputed, keeping the
autocorrelation of r(t) and the spacing of the recessions. p = (1 + number of shifts at least as extreme) / T,
so the smallest possible p is 1/T (1/53 = 0.019 for 1970-2022).

Surrogate economies: each economy's cycle keeps its Fourier amplitudes (its spectrum) and gets independent random
phases, which destroys every relation between economies. Phases are drawn U(0, 2 pi) in the order
(set, economy, frequency); the zero frequency, and the Nyquist frequency for an even length, stay real. That is
the as-run draw order, so with the as-run seed the p-values come out exactly as stored. The stream does not
depend on the batch size. p = (1 + surrogates at least as extreme) / (1 + n), floor 1/5001 = 0.0002 for 5,000.
"""
import numpy as np
from scipy.stats import pearsonr


def lagcorr(x, g, lag):
    """corr(x(t), g(t+lag)): lag > 0 puts x first (x leads g), lag < 0 puts g first."""
    if lag > 0: u, v = x[:-lag], g[lag:]
    elif lag < 0: u, v = x[-lag:], g[:lag]
    else: u, v = x, g
    return pearsonr(u, v)[0]


def shift_null(x, g, lag):
    """The lagged correlation for every circular shift k = 1..T-1 of g."""
    return np.array([lagcorr(x, np.roll(g, k), lag) for k in range(1, len(g))])


def p_upper(obs, null): return (1 + np.sum(null >= obs)) / (1 + len(null))


def p_lower(obs, null): return (1 + np.sum(null <= obs)) / (1 + len(null))


def p_two(obs, null): return (1 + np.sum(np.abs(null) >= abs(obs))) / (1 + len(null))


def shift_corr_test(x, y):
    """corr(x, y) and its upper-tail p over circular shifts of y (used for r against swing size)."""
    obs = pearsonr(x, y)[0]
    null = np.array([pearsonr(x, np.roll(y, k))[0] for k in range(1, len(y))])
    return float(obs), float(p_upper(obs, null))


def surrogates(X, n, rng, batch=250):
    """Yield batches (nb, economies, T) of spectrum-preserving surrogates of the cycles X (economies, T)."""
    X = np.asarray(X, dtype=float); N, T = X.shape
    amp = np.abs(np.fft.rfft(X, axis=-1)); nf = amp.shape[-1]
    for s0 in range(0, n, batch):
        nb = min(batch, n - s0)
        ph = rng.uniform(0, 2 * np.pi, size=(nb, N, nf)); ph[..., 0] = 0
        if T % 2 == 0: ph[..., -1] = 0
        yield np.fft.irfft(amp[None] * np.exp(1j * ph), n=T, axis=-1)
