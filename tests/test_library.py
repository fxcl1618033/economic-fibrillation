"""Unit tests for the core library: properties that must hold whatever the data, and the conventions on S26."""
import json
import os

import numpy as np
import pytest
from scipy.sparse.csgraph import minimum_spanning_tree

from conftest import needs_data
from ef import config, crisis, decomposition, network, nulls, order, phaselags, tipping
from ef.filters import bandpass, growth_cycle, hp_cycle
from ef.phases import analytic

YEARS = np.arange(1950, 2023)


def random_logs(seed=0, n=4):
    """Random-walk log levels with drift plus a 6-year cycle, n economies over 1950-2022."""
    g = np.random.default_rng(seed); t = np.arange(len(YEARS))
    return np.cumsum(0.02 + 0.01 * g.standard_normal((n, len(t))), axis=1) + 0.03 * np.sin(2 * np.pi * t / 6 + g.uniform(0, 6, (n, 1)))


# ---- phases
@needs_data
def test_conventions_P_W_N_reproduce_the_convention_check():
    from ef.paper1 import load_data
    D = load_data('S26'); stored = json.load(open(os.path.join(config.repo_root(), 'paper1/results/runin_convention_check.json')))['results']
    for conv in 'PWN':
        r = order.r(analytic(D.logs, D.years, (1970, 2022), conv))
        assert np.abs(r - np.array([stored[conv]['r_by_year'][str(y)] for y in range(1970, 2023)])).max() < 1e-12, conv


def test_causal_phases_use_only_the_past():
    x = random_logs(1); z = analytic(x, YEARS, (1970, 2022), 'C')
    y = x.copy(); y[:, YEARS > 2000] += np.random.default_rng(2).standard_normal((x.shape[0], (YEARS > 2000).sum()))
    z2 = analytic(y, YEARS, (1970, 2022), 'C'); past = np.arange(1970, 2023) <= 2000
    assert np.array_equal(z[:, past], z2[:, past]) and not np.allclose(z[:, ~past], z2[:, ~past])


def test_two_sided_phases_do_see_the_future():
    """The reason for convention C: under P a change after 2000 moves phases before 2000."""
    x = random_logs(1); y = x.copy(); y[:, YEARS > 2000] += 0.05
    z, z2 = analytic(x, YEARS, (1970, 2022), 'P'), analytic(y, YEARS, (1970, 2022), 'P')
    assert not np.allclose(z[:, np.arange(1970, 2023) <= 2000], z2[:, np.arange(1970, 2023) <= 2000])


def test_edge_robust_with_no_padding_is_P():
    x = random_logs(3)
    assert np.allclose(analytic(x, YEARS, (1970, 2022), 'E', pad=0), analytic(x, YEARS, (1970, 2022), 'P'), atol=1e-15)


def test_unknown_convention_raises():
    with pytest.raises(ValueError): analytic(random_logs(), YEARS, (1970, 2022), 'X')


# ---- filters
def test_bandpass_gain_is_the_squared_butterworth_response():
    """Forward-backward filtering applies |H(f)|^2: a 6-year cycle keeps about 87% of its size (the band is not
    flat for an order-2 Butterworth), with no phase shift; a linear trend is removed."""
    from scipy.signal import freqz
    from ef.filters import butter_band
    t = np.arange(400.0); cyc = np.sin(2 * np.pi * t / 6)
    gain = np.abs(freqz(*butter_band(), worN=[2 * np.pi / 6])[1][0]) ** 2
    out = bandpass(cyc)[100:-100]
    assert abs(np.std(out) / np.std(cyc[100:-100]) - gain) < 1e-3 and 0.85 < gain < 0.9
    assert np.corrcoef(out, cyc[100:-100])[0, 1] > 0.9999                    # zero phase
    assert np.abs(bandpass(0.01 * t)[100:-100]).max() < 1e-6                # no trend gets through


def test_hp_and_growth_cycles():
    assert np.abs(hp_cycle(np.linspace(0, 1, 60))).max() < 1e-9   # HP leaves a straight line in the trend
    g = growth_cycle(np.log(np.linspace(1, 2, 30))); assert abs(g.mean()) < 1e-15 and g.shape == (30,)


# ---- order parameter and identity
def test_order_parameter_bounds():
    th = np.tile(np.linspace(0, 1, 20), (5, 1)); assert np.allclose(order.r(np.exp(1j * th)), 1)
    th = np.tile(np.arange(4)[:, None] * np.pi / 2, (1, 20)); assert np.allclose(order.r(np.exp(1j * th)), 0, atol=1e-15)


def test_fibrillation_identity_holds_exactly():
    z = np.random.default_rng(4).standard_normal((26, 53)) + 1j * np.random.default_rng(5).standard_normal((26, 53))
    assert order.identity_error(z) < 1e-14
    assert np.allclose(np.abs(order.world_phasor(z)), order.mean_amplitude(z) * order.amplitude_alignment(z))


# ---- nulls
def test_surrogates_keep_each_spectrum_and_ignore_batch_size():
    X = np.random.default_rng(6).standard_normal((5, 53))
    a = np.concatenate(list(nulls.surrogates(X, 30, np.random.default_rng(9), batch=7)))
    b = np.concatenate(list(nulls.surrogates(X, 30, np.random.default_rng(9), batch=30)))
    assert np.array_equal(a, b)
    assert np.allclose(np.abs(np.fft.rfft(a, axis=-1)), np.abs(np.fft.rfft(X, axis=-1))[None], atol=1e-12)


def test_circular_shift_floor():
    years = np.arange(1970, 2023); x = crisis.indicator(years) + 0.001 * np.arange(53)
    a = crisis.arc(x, years); assert a['crisis']['p'] == pytest.approx(1 / 53) and a['crisis']['corr'] > 0.99


# ---- crisis helpers
def test_multiplicity_corrections_known_values():
    p = [0.01, 0.04, 0.03, 0.005]
    assert np.allclose(crisis.bonferroni(p), [0.04, 0.16, 0.12, 0.02])
    assert np.allclose(crisis.benjamini_hochberg(p), [0.02, 0.04, 0.04, 0.02])


def test_tau_pre_of_a_rising_series_is_one():
    years = np.arange(1962, 2023); assert crisis.tau_pre(years.astype(float), years) == pytest.approx(1.0)


# ---- decomposition
def test_own_plus_cross_is_the_world_variance():
    g = np.random.default_rng(7); X = g.standard_normal((6, 40)); W = g.uniform(1, 2, (6, 40)); W /= W.sum(0)
    own, cross, tot, _ = decomposition.rolling(X, W, 10)
    world = [(W[:, t] * (X[:, t - 9:t + 1] - X[:, t - 9:t + 1].mean(1, keepdims=True)).T).sum(1).var() for t in range(9, 40)]
    assert np.allclose(tot[9:], world) and np.allclose(own + cross, tot, equal_nan=True)


def test_window_mean_weights():
    lev = np.vstack([np.ones(12), 3 * np.ones(12)]); W = decomposition.weights(lev, 'gdp_mean', 10)
    assert np.isnan(W[:, :9]).all() and np.allclose(W[:, 9:], [[0.25], [0.75]])


# ---- network
def test_vectorized_prim_matches_scipy():
    g = np.random.default_rng(8); P = g.uniform(0.1, 1, (20, 9, 9)); D = (P + P.transpose(0, 2, 1)) / 2
    ref = [minimum_spanning_tree(d * (1 - np.eye(9))).sum() for d in D]
    for d in D: np.fill_diagonal(d, np.inf)
    assert np.allclose(network._mst_length(D), ref)


# ---- phase lags and tipping
def test_leads_recover_a_known_shift():
    t = np.arange(53); omega = 2 * np.pi / 6; th = np.vstack([omega * t, omega * t + 0.5 * omega, omega * t - 0.5 * omega])
    assert np.allclose(phaselags.leads(th, omega), [0, 0.5, -0.5], atol=1e-12)


def test_tipping_formulas():
    assert tipping.implied_coupling(np.array([0.0, np.sqrt(0.5)])) == pytest.approx([1.0, 2.0])
    r = np.random.default_rng(10).uniform(0.2, 0.8, 61)
    assert np.allclose(tipping.restoring_time(r, 15, 5.0), 1 / tipping.recovery_rate(r, 15, 5.0), equal_nan=True)


def test_restoring_time_moves_with_the_autocorrelation():
    """Why it was dropped (open issue 22): 1/(-ln phi) is increasing in phi, so its rank trend equals phi's."""
    r = np.random.default_rng(11).uniform(0.2, 0.8, 61); years = np.arange(1962, 2023)
    phi = np.clip(tipping.rolling_ar1_var(r, 15, 5.0)[0], 1e-4, 0.9999)
    assert crisis.tau_pre(tipping.restoring_time(r, 15, 5.0), years) == pytest.approx(crisis.tau_pre(phi, years))


def test_strict_pre_windows_skip_partly_undefined_events():
    years = np.arange(1970, 2023); x = years.astype(float); x[years < 1979] = np.nan   # defined from 1979, like L(t)
    assert crisis.tau_pre(x, years, (1982, 2009), strict=False) < crisis.tau_pre(x, years, (1982, 2009), strict=True) == 1.0


@needs_data
def test_mst_decade_means_with_windows_inside_1970_2022():
    """Registry E1/E3 and Methods edits A2/A3: 0.677 vs 0.379 (1.8x); 0.652 was L(1979) alone; windows reaching back
    to 1962 leave every value from 1979 onward unchanged."""
    from ef.paper1 import load_data
    from ef.phases import window_cycles
    D = load_data('S26'); out = {}
    for w in ((1970, 2022), (1962, 2022)):
        L, _ = network.mst_stats(network.corr_windows(window_cycles(D.logs, D.years, w), 10)[None], 10)
        out[w] = dict(zip(range(w[0], 2023), L[0]))
    a = np.mean([out[(1970, 2022)][y] for y in range(1979, 1990)]); b = np.mean([out[(1970, 2022)][y] for y in range(2013, 2023)])
    assert (round(a, 3), round(b, 3), round(a / b, 1), round(out[(1970, 2022)][1979], 3)) == (0.677, 0.379, 1.8, 0.652)
    assert np.isnan(out[(1970, 2022)][1978]) and all(out[(1970, 2022)][y] == out[(1962, 2022)][y] for y in range(1979, 2023))
