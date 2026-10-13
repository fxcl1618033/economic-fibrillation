"""Diversification-type tipping (DTT): a clean implementation of the equations of Sid's report (dtt/legacy/, 13 October
2026; there is no original code). Seed 1310 throughout.

Section A, the variance law. N economies with phases theta_i and swing sizes A_i; a common shock in a random direction
u = (cos phi, sin phi) and, with shared fraction rho, an idiosyncratic part eps_i (independent, mean 0, variance 1/2):

    q_i = sigma [ sqrt(rho) A_i u.v_i + sqrt(1 - rho) A_i eps_i ],   v_i = (cos theta_i, sin theta_i),  qbar = mean_i q_i
    Var(qbar | phases) = sigma^2 [ rho |Z_A|^2 + (1 - rho) mean(A^2) / N ] / 2,     Z_A = mean_i A_i exp(i theta_i)

and |Z_A| = Abar R_A, Paper 1's fibrillation identity (R_A = |sum A_i e^(i theta_i)| / sum A_i). With equal swing sizes
(A_i = 1) and rho = 1 it is the report's sigma^2 R^2 / 2, and the effective number of economies that still diversify
one another is N_eff = 1 / (rho R^2 + (1 - rho) / N), 1/R^2 when the whole shock is shared.

Sections C-E, escape. A bistable state dx = (mu + x - x^3) dt + g(t) dW starts in its lower well and "tips" when it
first reaches x >= 0 within the horizon T. The noise scale g(t) is set by the oscillators' synchrony: the report's
dynamic shared-shock model uses g = sigma R(t) (generalized: g = sigma sqrt(rho R^2 + (1 - rho) / N)); the controls use
independent noise sigma / sqrt(N), each trial's constant RMS of sigma R(t), the ensemble RMS, or R(t) with its time
order permuted. The oscillators are the noisy mean-field Kuramoto model
    d theta_i = [omega_i + K Im(Z e^(-i theta_i))] dt + sqrt(2 D) dW_i,   omega_i ~ Normal(0, omega_sd^2) per trial,
started from uniform phases, as in the report. Euler-Maruyama throughout; the state does not feed back on the
oscillators, so R(t) traces can be computed first and reused across noise formulations with the same Brownian
increments for x (common random numbers).

Section F, the stress-threshold prototype: x[t+1] = a x[t] + sigma sqrt(V / N) eps[t], an event when |x| >= 0.8 for two
consecutive steps.
"""
from dataclasses import dataclass, replace

import numpy as np

SEED = 1310
MU = 0.2


# ------------------------------------------------------------------ section A: the variance laws

def z_a(theta, A=None):
    """Z_A = mean_i A_i exp(i theta_i) over the last axis (A = 1: the Kuramoto Z)."""
    A = np.ones_like(theta) if A is None else A
    return (A * np.exp(1j * theta)).mean(axis=-1)


def var_law(theta, sigma=1.0, A=None, rho=1.0):
    """Var(qbar | phases) = sigma^2 [rho |Z_A|^2 + (1 - rho) mean(A^2) / N] / 2."""
    A = np.ones_like(theta) if A is None else A; N = theta.shape[-1]
    return sigma ** 2 * (rho * np.abs(z_a(theta, A)) ** 2 + (1 - rho) * (A ** 2).mean(axis=-1) / N) / 2


def n_eff(R, rho=1.0, N=None):
    """Effective number of economies, equal swing sizes: 1 / (rho R^2 + (1 - rho) / N)."""
    return 1.0 / (rho * np.asarray(R) ** 2 + ((1 - rho) / N if rho < 1 else 0.0))


def identity_parts(theta, A):
    """(|Z_A|, Abar, R_A): |Z_A| = Abar R_A is Paper 1's fibrillation identity."""
    Z = np.abs(z_a(theta, A)); Abar = A.mean(axis=-1); RA = np.abs((A * np.exp(1j * theta)).sum(axis=-1)) / A.sum(axis=-1)
    return Z, Abar, RA


def mc_var(theta, n, rng, sigma=1.0, A=None, rho=1.0):
    """Monte Carlo variance of qbar for fixed phases: n draws of the shock direction and of the idiosyncratic parts."""
    A = np.ones_like(theta) if A is None else A; N = theta.shape[-1]
    phi = rng.uniform(0, 2 * np.pi, size=n); eps = rng.normal(0, np.sqrt(0.5), size=(n, N))
    q = sigma * (np.sqrt(rho) * A * np.cos(theta[None, :] - phi[:, None]) + np.sqrt(1 - rho) * A * eps)
    return q.mean(axis=1).var()


# ------------------------------------------------------------------ the bistable state

def equilibria(mu=MU):
    """The three equilibria of mu + x - x^3 (lower stable, separator, upper stable)."""
    return np.sort(np.roots([-1.0, 0.0, 1.0, mu]).real)


# ------------------------------------------------------------------ the dynamic models

@dataclass(frozen=True)
class Params:
    N: int = 31
    K: float = 0.0
    D: float = 0.02            # oscillator diffusion
    omega_sd: float = 1.0      # frequency dispersion
    mu: float = MU
    sigma: float = 0.82
    T: float = 40.0            # horizon
    dt: float = 0.01
    rho: float = 1.0           # shared fraction of the shock

    @property
    def steps(self): return int(round(self.T / self.dt))

    @property
    def x0(self): return float(equilibria(self.mu)[0])


def kuramoto_R(p, n, rng, burn=0.0, record_every=1, dW=None):
    """R(t) at the start of every step for n independent trials (n, steps); burn: time run first and dropped.
    dW: optional pre-drawn standard-normal increments (n, N, steps), for common random numbers across step sizes."""
    N, dt = p.N, p.dt; nb = int(round(burn / dt)); S = p.steps
    om = rng.normal(0, p.omega_sd, size=(n, N)); th = rng.uniform(-np.pi, np.pi, size=(n, N))
    sq = np.sqrt(2 * p.D * dt); out = np.empty((n, (S + record_every - 1) // record_every), dtype=np.float32)
    for k in range(nb + S):
        Z = np.exp(1j * th).mean(axis=1)
        if k >= nb and (k - nb) % record_every == 0: out[:, (k - nb) // record_every] = np.abs(Z)
        xi = dW[:, :, k] if dW is not None else rng.standard_normal((n, N))
        th = th + (om + p.K * np.imag(Z[:, None] * np.exp(-1j * th))) * dt + sq * xi
    return out


def noise_scale(R, p, kind='instantaneous', rng=None, block=None):
    """g(t) (n, steps) or (n, 1) for a formulation on the same R(t) traces:
    instantaneous   sigma sqrt(rho R(t)^2 + (1 - rho) / N)      (rho = 1: the report's sigma R(t))
    rms_trial       each trial's constant sigma sqrt(mean_t R^2)
    rms_ensemble    sigma sqrt(mean over trials and t of R^2)
    independent     sigma / sqrt(N)
    permuted        instantaneous, with each trial's R values in a random time order (step by step)
    block_permuted  the same with blocks of `block` steps kept whole (order of the blocks permuted)"""
    R = R.astype(float); s, N, rho = p.sigma, p.N, p.rho
    inst = lambda r: s * np.sqrt(rho * r ** 2 + (1 - rho) / N)
    if kind == 'instantaneous': return inst(R)
    if kind == 'rms_trial': return s * np.sqrt((R ** 2).mean(axis=1, keepdims=True))
    if kind == 'rms_ensemble': return np.full((R.shape[0], 1), s * np.sqrt((R ** 2).mean()))
    if kind == 'independent': return np.full((R.shape[0], 1), s / np.sqrt(N))
    if kind == 'permuted':
        idx = np.argsort(rng.random(R.shape), axis=1); return inst(np.take_along_axis(R, idx, axis=1))
    if kind == 'block_permuted':
        n, S = R.shape; nb = S // block; head = R[:, :nb * block].reshape(n, nb, block)
        order = np.argsort(rng.random((n, nb)), axis=1)
        Rp = np.concatenate([np.take_along_axis(head, order[:, :, None], axis=1).reshape(n, nb * block), R[:, nb * block:]], axis=1)
        return inst(Rp)
    raise ValueError(kind)


def escape(g, xi, p):
    """First passage of dx = (mu + x - x^3) dt + g dW from the lower well to x >= 0 within the horizon.
    g (n, steps) or (n, 1); xi (n, steps) standard normals (the Brownian increments / sqrt(dt)).
    Returns (tipped, time of first passage, NaN if none)."""
    n, S = xi.shape; x = np.full(n, p.x0); tip = np.full(n, np.nan); alive = np.ones(n, bool); sq = np.sqrt(p.dt)
    gc = g.shape[1] == 1
    for k in range(S):
        gk = g[:, 0] if gc else g[:, k]
        x = x + (p.mu + x - x ** 3) * p.dt + gk * sq * xi[:, k]
        hit = alive & (x >= 0); tip[hit] = (k + 1) * p.dt; alive &= ~hit
        if not alive.any(): break
    return ~np.isnan(tip), tip


def dynamic(p, n, rng, kinds=('instantaneous',), block_time=1.0):
    """The report's dynamic shared-shock test and its controls on common traces: R(t) for n trials, one set of
    Brownian increments for x, and every requested noise formulation. Returns {kind: (tipped, time)} and R."""
    R = kuramoto_R(p, n, rng); xi = rng.standard_normal((n, p.steps)).astype(np.float32)
    out = {k: escape(noise_scale(R, p, k, rng, max(1, int(round(block_time / p.dt)))), xi, p) for k in kinds}
    return out, R


def averaged_noise_escape(p, mean_R2, n, rng):
    """Section C: constant noise sigma sqrt(E[R^2]) (the 'component-derived, averaged-noise' model)."""
    xi = rng.standard_normal((n, p.steps)).astype(np.float32)
    return escape(np.full((n, 1), p.sigma * np.sqrt(mean_R2)), xi, p)


def stationary_R2(p, n_ens, rng, T_run=200.0, burn=50.0):
    """Section B: mean R^2 per ensemble over T_run after a run-in of `burn` (n_ens independent ensembles)."""
    q = replace(p, T=T_run); R = kuramoto_R(q, n_ens, rng, burn=burn)
    return (R.astype(float) ** 2).mean(axis=1), R


# ------------------------------------------------------------------ section F: the stress-threshold prototype

def threshold_events(innov_sd, n, rng, steps=800, a=0.9, level=0.8, run=2):
    """x[t+1] = a x[t] + innov_sd eps[t] from x = 0; an event when |x| >= level for `run` consecutive steps.
    Returns (event, step at which the run is completed, NaN if none)."""
    x = np.zeros(n); c = np.zeros(n, int); t_ev = np.full(n, np.nan)
    for t in range(1, steps + 1):
        x = a * x + innov_sd * rng.standard_normal(n); c = np.where(np.abs(x) >= level, c + 1, 0)
        new = (c >= run) & np.isnan(t_ev); t_ev[new] = t
    return ~np.isnan(t_ev), t_ev


# ------------------------------------------------------------------ statistics

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def same_proportion(k1, n1, k2, n2, z=1.96):
    """Two proportions agree at 95% (two-sided pooled z test does not reject); both 0 or both n count as agreeing."""
    p = (k1 + k2) / (n1 + n2)
    if p in (0.0, 1.0): return True
    return abs(k1 / n1 - k2 / n2) <= z * np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
