"""G1: simulated worlds of coupled economies with known coupling, for the Paper 1 pipeline (docs/preregistration_G1.md).

Two models, each economy i = 1..31 (S31) an oscillator, plus a world node W that forces every economy equally:

  Kuramoto       d theta_i = [omega_i + kappa sum_j W_ij(t) sin(theta_j - theta_i) + phi sin(theta_W - theta_i)] dt
                             + sigma dB_i
                 d theta_W = omega_W dt + sigma dB_W                       cycle_i = A_i cos(theta_i)

  Stuart-Landau  d z_i = [(mu + i omega_i) z_i - |z_i|^2 z_i + kappa sum_j W_ij(t) (z_j - z_i) + phi (z_W - z_i)] dt
                         + sigma (dB_i + i dB'_i)
                 d z_W = [(mu + i omega_W) z_W - |z_W|^2 z_W] dt + sigma (dB_W + i dB'_W)
                                                                           cycle_i = A_i Re(z_i) / m

W_ij(t) is the real trade network (G0, imf_imts_s31): goods exports of j to i as a share of i's GDP (the primary weight,
the mean of the exporter's and the importer's reports where both exist), the matrix of year t; years before 1970 use
1970's; a masked weight is no link (0). kappa and phi are the known couplings. omega_i is economy i's observed mean
frequency, A_i its observed mean swing size (S31, convention P, 1970-2022). m is the mean |z| of the uncoupled
Stuart-Landau world, so that coupling can change swing sizes.

Each world is integrated with Euler-Maruyama (dt = 0.01 years) from 1850 (a 100-year burn-in with 1970's network) to
2022; log GDP per capita of year y is a_i + g_i (y - 1950) + the mean of cycle_i over year y (GDP is a flow), with a_i,
g_i the linear trend of i's real series 1950-2022; GDP = exp(log GDP per capita) x i's real population. The years
1950-2022 go through the Paper 1 pipeline (ef.paper1) exactly as the real data do.
"""
import os

import numpy as np
import pandas as pd

from ef import config, order, paper1
from ef.phases import analytic

SPAN = (1950, 2022)
BURN_FROM = 1850
DT = 0.01
MODELS = ('kuramoto', 'stuart_landau')


def trade_network(g0_dir=None, years=range(SPAN[0], SPAN[1] + 1)):
    """W[y, i, j]: exports of j to i / GDP of i, from the G0 trade edges; mean of the two reports where both exist,
    0 where both are masked. Years before 1970 take 1970's matrix."""
    g0_dir = g0_dir or os.path.join(config.load()['paths']['build'], 'gnn', 'g0')
    e = pd.read_csv(os.path.join(g0_dir, 'edges_trade.csv'), usecols=['year', 'src', 'dst', 'w_exports_share_dst_gdp', 'w_mirror_share_dst_gdp'])
    isos = config.sample('S31'); ix = {c: k for k, c in enumerate(isos)}
    w = e[['w_exports_share_dst_gdp', 'w_mirror_share_dst_gdp']].mean(axis=1, skipna=True).fillna(0.0).to_numpy()
    T = np.zeros((2023 - 1970, len(isos), len(isos)))
    T[e.year.to_numpy() - 1970, e.dst.map(ix).to_numpy(), e.src.map(ix).to_numpy()] = w
    years = list(years)
    return np.stack([T[max(y, 1970) - 1970] for y in years]), isos


def targets(isos=None):
    """The real S31 quantities the simulator is calibrated to (convention P, 1970-2022), and the pieces it reuses:
    mean frequency and swing size per economy, the linear trends and the population."""
    D = paper1.load_data('S31', SPAN); assert isos is None or isos == D.isos
    z = analytic(D.logs, D.years, (1970, 2022), 'P'); th = np.angle(z); A = np.abs(z)
    omega = (np.unwrap(th, axis=1)[:, -1] - np.unwrap(th, axis=1)[:, 0]) / 52
    t = D.years - SPAN[0]; g, a = np.polyfit(t, D.logs.T, 1)
    return {'isos': D.isos, 'omega': omega, 'A': A.mean(axis=1), 'trend_a': a, 'trend_g': g,
            'pop': D.levels / np.exp(D.logs), 'years': D.years, **stats(z)}


def stats(z):
    """Calibration statistics of analytic signals z (economies x years, or worlds x economies x years): the median over
    economies of the sd of annual phase steps, the median coefficient of variation of the swing size, and mean r."""
    dth = np.angle(np.exp(1j * np.diff(np.angle(z), axis=-1))); A = np.abs(z)
    return {'sd_phase_step': np.median(dth.std(axis=-1), axis=-1), 'cv_amplitude': np.median(A.std(axis=-1) / A.mean(axis=-1), axis=-1),
            'mean_r': order.r(z).mean(axis=-1)}


def simulate(model, Wy, omega, kappa, phi, sigma, rng, n_worlds, mu=0.0, omega_w=None, years=range(SPAN[0], SPAN[1] + 1), hook=None):
    """Annual means of the cycle signal for n_worlds worlds: complex array (worlds, economies, years); for Kuramoto
    exp(i theta), for Stuart-Landau z. Wy: the network of each year in `years` (W[y, i, j], i pulled by j).
    hook(year, theta), Kuramoto only: called with the true phases at the start of every Euler step (G1b reads them);
    it draws nothing from rng, so the worlds are the same with or without it."""
    years = list(years); N = len(omega); spy = int(round(1 / DT)); omega_w = float(np.mean(omega)) if omega_w is None else omega_w
    steps = [(BURN_FROM + k, Wy[0]) for k in range(years[0] - BURN_FROM)] + [(y, Wy[k]) for k, y in enumerate(years)]
    sq = sigma * np.sqrt(DT); out = np.empty((n_worlds, N, len(years)), dtype=complex)
    if model == 'kuramoto':
        th = rng.uniform(0, 2 * np.pi, (n_worlds, N)); thw = rng.uniform(0, 2 * np.pi, n_worlds)
    else:
        r0 = np.sqrt(max(mu, 0.0)) or 0.5
        z = r0 * np.exp(1j * rng.uniform(0, 2 * np.pi, (n_worlds, N))); zw = r0 * np.exp(1j * rng.uniform(0, 2 * np.pi, n_worlds))
    for y, W in steps:
        Wk = kappa * W; rs = Wk.sum(axis=1); acc = np.zeros((n_worlds, N), dtype=complex)
        for _ in range(spy):
            if model == 'kuramoto':
                if hook is not None: hook(y, th)
                u = np.exp(1j * th)
                drift = omega + np.imag(np.conj(u) * (u @ Wk.T)) + phi * np.sin(thw[:, None] - th)
                th = th + drift * DT + sq * rng.standard_normal((n_worlds, N))
                thw = thw + omega_w * DT + sq * rng.standard_normal(n_worlds)
                acc += np.exp(1j * th)
            else:
                drift = (mu + 1j * omega) * z - (np.abs(z) ** 2) * z + z @ Wk.T - rs * z + phi * (zw[:, None] - z)
                z = z + drift * DT + sq * (rng.standard_normal((n_worlds, N)) + 1j * rng.standard_normal((n_worlds, N)))
                zw = zw + ((mu + 1j * omega_w) * zw - (np.abs(zw) ** 2) * zw) * DT + sq * (rng.standard_normal(n_worlds) + 1j * rng.standard_normal(n_worlds))
                acc += z
        if y >= years[0]: out[:, :, y - years[0]] = acc / spy
    return out


def to_data(sig, T, model, m=1.0, name='sim'):
    """A world's annual cycle signal (economies x years) as a paper1.Data: log GDP per capita = trend + cycle, levels =
    GDP per capita x population. Kuramoto: cycle = A cos(theta) (the real part of the annual mean of exp(i theta));
    Stuart-Landau: A Re(z) / m."""
    cyc = T['A'][:, None] * np.real(sig) / (1.0 if model == 'kuramoto' else m)
    t = T['years'] - SPAN[0]; logs = T['trend_a'][:, None] + T['trend_g'][:, None] * t[None, :] + cyc
    return paper1.Data(name, list(T['isos']), T['years'], logs, np.exp(logs) * T['pop'])


def pipeline_z(sig, T, model, m=1.0):
    """Analytic signals of a batch of worlds (worlds, economies, 1970-2022) through the Paper 1 band-pass and Hilbert
    transform (convention P), for calibration."""
    return np.stack([analytic(to_data(s, T, model, m).logs, T['years'], (1970, 2022), 'P') for s in sig])


def world_recessions(D, n=5, n_down=3, gap=5, window=(1970, 2022)):
    """Recession years defined from a simulated world itself, as Kose, Sugawara and Terrones define global recessions
    from world GDP per capita: the n years of lowest growth of the 31's total real GDP per capita in the window, taken
    lowest first and at least `gap` years from any year already taken; the next n_down are the downturns."""
    pop = D.levels / np.exp(D.logs); Y = np.log(D.levels.sum(axis=0) / pop.sum(axis=0)); g = np.diff(Y)
    yrs = D.years[1:]; m = (yrs >= window[0]) & (yrs <= window[1]); order_ = np.argsort(g[m], kind='stable'); cand = yrs[m][order_]
    taken = []
    for y in cand:
        if all(abs(int(y) - t) >= gap for t in taken): taken.append(int(y))
        if len(taken) == n + n_down: break
    return sorted(taken[:n]), sorted(taken[n:])
