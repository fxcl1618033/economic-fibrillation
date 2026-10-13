"""G1 simulator: the network it reads, the exact rejection rates, the own-dated recessions and the coupling terms."""
import os

import numpy as np
import pandas as pd
import pytest

from conftest import needs_data
from ef import config, paper1
from ef.gnn import g1_report, simulator as S

G0 = os.path.join(config.load()['paths']['build'], 'gnn', 'g0')


@needs_data
def test_network_is_the_g0_primary_trade_weight():
    if not os.path.exists(os.path.join(G0, 'edges_trade.csv')): pytest.skip("run make gnn-g0 first")
    W, isos = S.trade_network(); e = pd.read_csv(os.path.join(G0, 'edges_trade.csv'))
    row = e.query('year == 2022 and src == "USA" and dst == "MEX"').iloc[0]
    want = np.nanmean([row.w_exports_share_dst_gdp, row.w_mirror_share_dst_gdp])
    assert W[2022 - 1950, isos.index('MEX'), isos.index('USA')] == pytest.approx(want)          # Mexico pulled by the US
    assert np.array_equal(W[0], W[1970 - 1950])                                                  # before 1970: 1970's
    assert (W[:1992 - 1950, isos.index('RUS'), :] == 0).all() and (W[:, np.arange(31), np.arange(31)] == 0).all()


def test_exact_rates():
    """Below 0.05 a circular-shift p over 53 years can only be 1/53 or 2/53; with 199 surrogates p <= 0.05 iff k <= 9."""
    ps = (1 + np.arange(53)) / 53
    assert g1_report.EXACT['shift'] == pytest.approx((ps <= 0.05).sum() / 53)
    assert g1_report.EXACT['surrogate'] == pytest.approx(((1 + np.arange(200)) / 200 <= 0.05).sum() / 200)
    lo, hi = g1_report.wilson(50, 1000); assert lo == pytest.approx(0.0381, abs=1e-4) and hi == pytest.approx(0.0653, abs=1e-4)


def test_own_dated_recessions_take_the_worst_years_apart():
    years = np.arange(1950, 2023); n = len(years); g = np.full(n, 0.02)
    for y, v in ((1980, -0.05), (1981, -0.04), (1990, -0.03), (2001, -0.02), (2008, -0.01), (2015, -0.005), (2020, -0.06)):
        g[years == y] = v
    logs = np.cumsum(g)[None, :].repeat(2, axis=0); D = paper1.Data('t', ['A', 'B'], years, logs, np.exp(logs))
    rec, down = S.world_recessions(D, n=5, n_down=1, gap=5)
    assert rec == [1980, 1990, 2001, 2008, 2020] and 1981 not in rec and down == [2015]       # 1981 is too close to 1980


def test_uncoupled_worlds_ignore_the_network():
    """With kappa = phi = 0 the network has no effect: the same seed gives the same world for any W."""
    om = np.array([1.0, 1.2, 0.9]); W0 = np.zeros((73, 3, 3)); W1 = np.random.default_rng(0).uniform(0, 0.3, (73, 3, 3))
    for m in S.MODELS:
        a = S.simulate(m, W0, om, 0.0, 0.0, 0.5, np.random.default_rng(1), 2, mu=-1.0)
        b = S.simulate(m, W1, om, 0.0, 0.0, 0.5, np.random.default_rng(1), 2, mu=-1.0)
        c = S.simulate(m, W1, om, 5.0, 0.0, 0.5, np.random.default_rng(1), 2, mu=-1.0)
        assert np.array_equal(a, b) and not np.allclose(a, c)
