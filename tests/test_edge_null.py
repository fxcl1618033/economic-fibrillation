"""Amendment 4: the edge-matched surrogates keep what they should, and the statistics are Paper 1's."""
import json
import os

import numpy as np
import pytest

from conftest import needs_data
from ef import config, edge_null as E, paper1


def _toy(N=4, T=73, seed=0):
    rng = np.random.default_rng(seed); g = 0.02 + 0.01 * rng.standard_normal((N, T - 1))
    g[1] = 0.7 * g[0] + 0.3 * g[1]                                        # economies 0 and 1 co-move
    return np.concatenate([np.zeros((N, 1)), np.cumsum(g, axis=-1)], axis=-1)


def test_surrogates_keep_the_spectrum_and_have_ends():
    logs = _toy(); g = np.diff(logs, axis=-1)
    for multi in (False, True):
        L = next(E.surrogate_logs(logs, 2000, np.random.default_rng(1), multi, batch=2000)); gs = np.diff(L, axis=-1)
        assert L.shape == (2000,) + logs.shape and np.allclose(L[:, :, 0], logs[:, 0])        # the real first level
        assert np.allclose(gs.mean(axis=(0, 2)), g.mean(axis=1), atol=2e-3)                   # the mean growth
        assert np.allclose(gs.var(axis=(0, 2)), g.var(axis=1), rtol=0.1)                      # the variance
        assert np.abs(gs[:, :, 0] - gs[:, :, -1]).mean() > 0.5 * np.abs(np.diff(g, axis=-1)).mean()   # not circular
        c = np.mean([np.corrcoef(x[0], x[1])[0, 1] for x in gs])
        assert (abs(c - np.corrcoef(g[0], g[1])[0, 1]) < 0.1) if multi else abs(c) < 0.05     # co-movement kept or not


@needs_data
def test_stored_statistics_are_paper1s():
    """Each stored statistic equals the Phase 3 value the current p belongs to (the run checks this; so does the file)."""
    f = os.path.join(config.repo_root(), 'results', 'edge_matched', 'S31.json')
    if not os.path.exists(f): pytest.skip("run make edge-null first")
    R = json.load(open(f)); cur = E.current('S31')
    for k, t in R['tests'].items():
        assert t['stat'] == pytest.approx(cur[k][0], abs=1e-9) and t['p_current'] == cur[k][1]
        assert 1 / 5001 - 1e-12 <= t['p_edge'] <= 1
