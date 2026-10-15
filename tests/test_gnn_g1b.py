"""G1b (docs/preregistration_G1b_dtt.md, amendment 1): checks written before the run."""
import json
import os

import numpy as np
import pytest

from ef import paper1
from ef.gnn import g1, g1b, simulator as S

pytestmark = pytest.mark.skipif(not os.path.exists(os.path.join(g1.OUT, 'calibration.json')), reason='needs the G1 calibration')


def test_hook_does_not_change_the_worlds():
    """The true-phase recorder draws nothing, so G1b's worlds are G1's."""
    cal = json.load(open(os.path.join(g1.OUT, 'calibration.json')))['kuramoto']; T = S.targets(); Wy, _ = g1.network()
    a = S.simulate('kuramoto', Wy, T['omega'], cal['kappa_star'], 0.0, cal['sigma'], np.random.default_rng([2001, 0, 3]), 2)
    b, rec = g1b.worlds('network', 2, [2001, 0, 3], theta=True)
    assert np.array_equal(a, b) and rec.k == g1b.STEPS
    assert np.allclose(rec.r, np.abs(np.exp(1j * rec.th.astype(float)).mean(axis=2)).T, atol=5e-3)


def test_pipeline_r_is_the_paper1_pipeline():
    sig, _ = g1b.worlds('null', 1, [7, 7])
    cfg = g1.run_config(); D = S.to_data(sig[0], S.targets(), 'kuramoto')
    rP, rC = g1b.pipeline_r(sig[0])
    arc = paper1.TESTS['arc'](D, cfg, dict(cfg['tests']['arc'], bootstrap=10))
    conv = paper1.TESTS['conventions'](D, cfg, dict(cfg['tests']['conventions'], conventions=['C']))
    assert np.allclose(rP, [arc['r_by_year'][y] for y in g1b.WYEARS], rtol=0, atol=1e-12)
    assert np.allclose(rC, [conv['C']['r_by_year'][y] for y in g1b.WYEARS], rtol=0, atol=1e-12)


def test_refractory_rule():
    esc = np.zeros((3, len(g1b.YEARS)), bool); ix = lambda y: y - g1b.FROM
    for y in (1968, 1970, 1971, 1972, 1973, 1980): esc[:, ix(y)] = True
    got = [g1b.WYEARS[r].tolist() for r in (g1b.recessions(esc[:1], 0)[0], g1b.recessions(esc[:1], 2)[0], g1b.recessions(esc[:1], 4)[0])]
    assert got == [[1970, 1971, 1972, 1973, 1980], [1970, 1973, 1980], [1970, 1980]]     # 1968 neither counts nor blocks


def test_escape_layer():
    n = 20; zero = np.zeros((n, g1b.STEPS), np.float32)
    assert not g1b.world_layer(zero, 0.2, 1.0, 1).any()                       # no noise, no escape
    loud = g1b.world_layer(zero + 3.0, 0.2, 1.0, 1)
    assert loud.mean() > 0.8                                                    # reset at once: escapes go on in most years
    a = g1b.world_layer(zero + 0.5, 0.2, 1.0, 5); b = g1b.world_layer(zero + 0.5, 0.2, 1.0, 5)
    assert np.array_equal(a, b)                                                 # the seed fixes the run


def test_block_shuffle_moves_whole_years():
    rng = np.random.default_rng(0); x = np.arange(2 * g1b.STEPS, dtype=float).reshape(2, g1b.STEPS)
    perm = g1b.block_permutation(2, rng); y = g1b.shuffle_steps(x, perm)
    assert np.array_equal(np.sort(y, axis=1), x)
    for w in range(2):
        for j in range(len(g1b.YEARS)):
            assert np.array_equal(y[w, j * g1b.SPY:(j + 1) * g1b.SPY], x[w, perm[w, j] * g1b.SPY:(perm[w, j] + 1) * g1b.SPY])


def test_per_economy_constant_control_matches_mean_square():
    N = 31; r = np.full((1, 10), 1.0, np.float32)
    assert g1b.alignment_share(r, N)[0] == pytest.approx(1.0)
    r = np.full((1, 10), 1 / np.sqrt(N), np.float32); assert g1b.alignment_share(r, N)[0] == pytest.approx(0.0, abs=1e-6)
    r = np.full((1, 10), 0.5, np.float32); c = g1b.alignment_share(r, N)[0]
    assert c + (1 - c) / N == pytest.approx(0.25, rel=1e-6)                  # the world-average noise keeps r^2 on average
