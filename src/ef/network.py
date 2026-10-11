"""The correlation network of the cycles (Methods 6.5, 6.6).

Rolling correlation matrices on trailing windows; distance d_ij = sqrt(2 (1 - rho_ij)) (Mantegna); the minimum
spanning tree's mean edge length L(t) (shorter = tighter network); the largest eigenvalue lambda_max(t); and the
Fiedler split of the whole-sample correlation network into two blocs with their within- and between-bloc alignment.
"""
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree


def corr_windows(X, win=10):
    """X (..., N, T) -> rolling correlation matrices (..., T, N, N), NaN before the first full window (mst_network.py)."""
    N, T = X.shape[-2:]; out = np.full(X.shape[:-2] + (T, N, N), np.nan)
    for t in range(win - 1, T):
        seg = X[..., :, t - win + 1:t + 1]; seg = seg - seg.mean(axis=-1, keepdims=True)
        sd = seg.std(axis=-1, keepdims=True); sd = np.where(sd > 0, sd, 1e-12)
        z = seg / sd
        out[..., t, :, :] = np.clip(np.einsum('...it,...jt->...ij', z, z) / seg.shape[-1], -1, 1)
    return out


def _mst_length(D):
    """Total MST length for a batch of dense distance matrices (B, N, N), by vectorized Prim."""
    B, N = D.shape[:2]; idx = np.arange(B)
    intree = np.zeros((B, N), bool); intree[:, 0] = True
    mind = D[:, 0, :].copy(); mind[:, 0] = np.inf; total = np.zeros(B)
    for _ in range(N - 1):
        masked = np.where(intree, np.inf, mind); j = np.argmin(masked, axis=1)
        total += masked[idx, j]; intree[idx, j] = True; mind = np.minimum(mind, D[idx, j, :])
    return total


def mst_stats(C, win=10):
    """C (..., T, N, N) -> MST mean edge length L(t) and largest eigenvalue lambda_max(t), each (..., T)."""
    T, N = C.shape[-3], C.shape[-1]; lead = C.shape[:-3]
    flat = C.reshape(-1, T, N, N); B = flat.shape[0]
    Lo = np.full((B, T), np.nan); Mo = np.full((B, T), np.nan)
    for t in range(win - 1, T):
        Ct = flat[:, t, :, :]
        D = np.sqrt(np.clip(2 * (1 - Ct), 0, None)); np.einsum('bii->bi', D)[...] = np.inf
        Lo[:, t] = _mst_length(D) / (N - 1); Mo[:, t] = np.linalg.eigvalsh(Ct)[:, -1]
    return Lo.reshape(lead + (T,)), Mo.reshape(lead + (T,))


def mst_degree(C, win=10):
    """Mean degree of each economy in the yearly MSTs (its centrality), from C (T, N, N)."""
    T, N = C.shape[0], C.shape[-1]; deg = np.zeros((T, N))
    for t in range(win - 1, T):
        D = np.sqrt(np.clip(2 * (1 - C[t]), 0, None)); np.fill_diagonal(D, 0)
        tree = minimum_spanning_tree(D).toarray(); tree = tree + tree.T; deg[t] = (tree > 0).sum(axis=1)
    return np.nanmean(deg[win - 1:], axis=0)


def fiedler(X):
    """Split economies into two blocs by the Fiedler vector of the normalized Laplacian of the positive part of the
    correlation matrix of X (N, T). Returns lambda2 and a boolean mask of bloc A (vector >= 0)."""
    N = X.shape[0]; C = np.corrcoef(X)
    W = np.clip(C, 0, None); np.fill_diagonal(W, 0)
    deg = W.sum(1); Dm = np.diag(1 / np.sqrt(deg)); Ln = np.eye(N) - Dm @ W @ Dm
    ev, evec = np.linalg.eigh(Ln)
    return float(ev[1]), evec[:, 1] >= 0


def bloc_alignment(theta, in_a):
    """Within-bloc alignment (blocs' own r, weighted by size) and between-bloc alignment (of the two bloc phases)."""
    ea = np.exp(1j * theta[..., in_a, :]).mean(axis=-2); eb = np.exp(1j * theta[..., ~in_a, :]).mean(axis=-2)
    rw = (np.abs(ea) * in_a.sum() + np.abs(eb) * (~in_a).sum()) / len(in_a)
    rb = np.abs((np.exp(1j * np.angle(ea)) + np.exp(1j * np.angle(eb))) / 2)
    return rw, rb
