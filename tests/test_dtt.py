"""DTT (src/ef/dtt.py): the variance laws against Monte Carlo, the fibrillation identity, the equilibria, the
controls and fixed seeds."""
import numpy as np
import pytest

from ef import dtt


def _phases(rng, N, spread):
    """Phases around a common angle with a chosen spread (0 = aligned, large = incoherent)."""
    return rng.uniform(0, 2 * np.pi) + spread * rng.standard_normal(N)


@pytest.mark.parametrize('spread', [0.3, 1.0, 3.0])
def test_variance_law_equal_swings(spread):
    rng = np.random.default_rng(dtt.SEED); th = _phases(rng, 31, spread)
    theory = dtt.var_law(th, sigma=0.7); R = np.abs(dtt.z_a(th))
    assert theory == pytest.approx(0.7 ** 2 * R ** 2 / 2, rel=1e-12)                  # sigma^2 R^2 / 2
    assert dtt.mc_var(th, 400_000, rng, sigma=0.7) == pytest.approx(theory, rel=0.01)
    assert dtt.n_eff(R) == pytest.approx(1 / R ** 2)


@pytest.mark.parametrize('spread', [0.3, 1.0, 3.0])
def test_variance_law_unequal_swings_is_the_fibrillation_identity(spread):
    rng = np.random.default_rng(dtt.SEED + 1); th = _phases(rng, 31, spread); A = rng.lognormal(0, 0.6, 31)
    Z, Abar, RA = dtt.identity_parts(th, A)
    assert Z == pytest.approx(Abar * RA, rel=1e-12)                                    # |Z_A| = Abar R_A, algebraically
    theory = dtt.var_law(th, A=A)
    assert theory == pytest.approx((Abar * RA) ** 2 / 2, rel=1e-12)
    assert dtt.mc_var(th, 400_000, rng, A=A) == pytest.approx(theory, rel=0.01)


@pytest.mark.parametrize('rho', [0.0, 0.3, 0.7, 1.0])
def test_variance_law_partly_shared_shock(rho):
    rng = np.random.default_rng(dtt.SEED + 2); th = _phases(rng, 31, 1.0); A = rng.lognormal(0, 0.6, 31)
    theory = dtt.var_law(th, A=A, rho=rho)
    want = (rho * np.abs(dtt.z_a(th, A)) ** 2 + (1 - rho) * (A ** 2).mean() / 31) / 2         # Sid's derivation
    assert theory == pytest.approx(want, rel=1e-12)
    assert dtt.mc_var(th, 400_000, rng, A=A, rho=rho) == pytest.approx(theory, rel=0.015)
    R = np.abs(dtt.z_a(th))                                                                  # equal swings: N_eff
    assert 1 / (2 * dtt.var_law(th, rho=rho)) == pytest.approx(dtt.n_eff(R, rho, 31), rel=1e-12)


def test_equilibria():
    lo, mid, hi = dtt.equilibria(0.2)
    assert (round(lo, 3), round(mid, 3), round(hi, 3)) == (-0.879, -0.209, 1.088)
    assert (lo, mid, hi) == pytest.approx((-0.878885, -0.209149, 1.088034), abs=1e-6)        # the report's values


def test_fixed_seed_gives_identical_output():
    p = dtt.Params(K=1.0, T=5.0)
    a, Ra = dtt.dynamic(p, 50, np.random.default_rng(dtt.SEED), kinds=('instantaneous', 'permuted'))
    b, Rb = dtt.dynamic(p, 50, np.random.default_rng(dtt.SEED), kinds=('instantaneous', 'permuted'))
    assert np.array_equal(Ra, Rb)
    for k in a: assert np.array_equal(a[k][0], b[k][0]) and np.array_equal(a[k][1], b[k][1], equal_nan=True)


def test_controls_keep_what_they_should():
    rng = np.random.default_rng(dtt.SEED); p = dtt.Params(K=1.5, T=10.0)
    R = dtt.kuramoto_R(p, 40, rng).astype(float)
    inst = dtt.noise_scale(R, p); rms = dtt.noise_scale(R, p, 'rms_trial')
    assert np.allclose((inst ** 2).mean(axis=1), rms[:, 0] ** 2)                          # same mean square per trial
    perm = dtt.noise_scale(R, p, 'permuted', rng); blk = dtt.noise_scale(R, p, 'block_permuted', rng, block=100)
    assert np.allclose(np.sort(perm, axis=1), np.sort(inst, axis=1)) and np.allclose(np.sort(blk, axis=1), np.sort(inst, axis=1))
    q = dtt.Params(K=1.5, T=10.0, rho=0.0)                                                   # rho = 0 is independent noise
    assert np.allclose(dtt.noise_scale(R, q), dtt.noise_scale(R, q, 'independent'))
    # uncoupled phases: E[R^2] = 1/N
    R0 = dtt.kuramoto_R(dtt.Params(K=0.0, T=20.0), 200, rng).astype(float)
    assert (R0 ** 2).mean() == pytest.approx(1 / 31, rel=0.05)
