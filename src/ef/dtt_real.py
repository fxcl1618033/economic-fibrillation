"""DTT D3: the effective number of economies on real data, descriptive only (no p-values).

    python -m ef.dtt_real      # -> dtt/results/d3_neff.json, dtt/D3_real_data.md

N_eff(t) = 1 / r(t)^2 (equal swing sizes, the whole shock shared); the amplitude-weighted 1 / R_A(t)^2; and the count
the variance law implies exactly when swing sizes differ, mean(A^2) / |Z_A|^2 = (1 + CV_A^2) / R_A^2 (with
Z_A = mean_i A_i exp(i theta_i) = Abar R_A). Samples S31 (main), S30, S26; convention P with past-only C beside it.

The link to the variance decomposition (Methods 6.1): the cycle is the real part of the analytic signal,
x_i = Re z_i = A_i cos(theta_i), and over one shock direction the variance law gives world variance |sum w_i z_i|^2 / 2
and own variance sum w_i^2 |z_i|^2 / 2. A window's time variance equals these exactly when, inside the window, swing
sizes and phase gaps are fixed and the common phase turns through whole cycles; otherwise the two are close, not equal.
The comparison below measures how close on the real windows.
"""
import json
import os

import numpy as np

from ef import config, crisis, decomposition, order, paper1
from ef.phases import analytic, window_cycles

SAMPLES = ('S31', 'S30', 'S26')
OUT = os.path.join(config.repo_root(), 'dtt')
REC = crisis.RECESSIONS; DOWN = crisis.DOWNTURNS


def series(D, conv):
    z = analytic(D.logs, D.years, (1970, 2022), conv); A = np.abs(z); r = order.r(z); RA = order.amplitude_alignment(z)
    A2, ZA2 = (A ** 2).mean(axis=0), np.abs(z.mean(axis=0)) ** 2                     # mean(A^2) and |Z_A|^2 = (Abar R_A)^2
    return {'years': np.arange(1970, 2023), 'N': len(D.isos), 'r': r, 'RA': RA, 'A2': A2, 'ZA2': ZA2,
            'neff': 1 / r ** 2, 'inv_RA2': 1 / RA ** 2, 'neffA': A2 / ZA2}


def groups(years):
    y = np.asarray(years); rec = np.isin(y, REC)
    return {'all years': np.ones(len(y), bool), 'recession years': rec, 'lead-1 years': np.isin(y, [e - 1 for e in REC]),
            'normal years': ~rec & ~np.isin(y, DOWN)}


def summarize(s):
    """Per group of years, the report's definition N_eff = 1 / E[R^2] (the variance-equivalent count over the group), its
    amplitude-weighted analogues 1 / E[R_A^2] and E[mean A^2] / E[|Z_A|^2], and medians of the yearly values. The
    arithmetic mean of 1/r^2 is kept for the record only: years with r near 0 make it explode."""
    out = {}
    for g, m in groups(s['years']).items():
        out[g] = {'neff': float(1 / (s['r'][m] ** 2).mean()), 'inv_RA2': float(1 / (s['RA'][m] ** 2).mean()),
                  'neffA': float(s['A2'][m].mean() / s['ZA2'][m].mean()), 'median_neff': float(np.median(s['neff'][m])),
                  'median_inv_RA2': float(np.median(s['inv_RA2'][m])), 'median_neffA': float(np.median(s['neffA'][m])),
                  'mean_of_yearly_neff_unstable': float(s['neff'][m].mean()), 'n_years': int(m.sum())}
    yi = list(s['years'])
    out['by_year'] = {int(y): {'r': float(s['r'][k]), 'neff': float(s['neff'][k]), 'inv_RA2': float(s['inv_RA2'][k]), 'neffA': float(s['neffA'][k])}
                      for k, y in enumerate(yi)}
    return out


def decomposition_link(D, cfg):
    """Actual rolling decomposition (Phase 3 settings: windows 1962-2022, 10 years) against the variance law averaged
    over the same windows, for GDP (window-mean) and equal weights."""
    t = cfg['tests']['diversification']; w = tuple(t['window']); win = t['win']; m = (D.years >= w[0]) & (D.years <= w[1])
    X = window_cycles(D.logs, D.years, w, cfg['band']); z = analytic(D.logs, D.years, w, 'P'); yrs = D.years[m]
    assert np.allclose(np.real(z), X, atol=1e-12)                       # the cycle is the real part of the analytic signal
    out = {}
    for kind in t['weights']:
        W = decomposition.weights(D.levels[:, m], kind, win); own, cross, tot, _ = decomposition.rolling(X, W, win)
        own_d = np.full(len(yrs), np.nan); tot_d = np.full(len(yrs), np.nan)
        for k in range(win - 1, len(yrs)):
            zw = z[:, k - win + 1:k + 1]; wk = W[:, k][:, None]
            own_d[k] = ((wk ** 2) * np.abs(zw) ** 2).sum(axis=0).mean() / 2
            tot_d[k] = (np.abs((wk * zw).sum(axis=0)) ** 2).mean() / 2
        cross_d = tot_d - own_d; ok = ~np.isnan(tot)
        share, share_d = cross[ok] / tot[ok], cross_d[ok] / tot_d[ok]
        ex = decomposition.crisis_excess(own, cross, tot, yrs, cfg['recessions'])
        ex_d = decomposition.crisis_excess(own_d, cross_d, tot_d, yrs, cfg['recessions'])
        out[kind] = {'windows': int(ok.sum()),
                     'tot_ratio_median': float(np.median(tot_d[ok] / tot[ok])), 'own_ratio_median': float(np.median(own_d[ok] / own[ok])),
                     'cross_share_corr': float(np.corrcoef(share, share_d)[0, 1]), 'cross_share_mean_abs_gap': float(np.mean(np.abs(share - share_d))),
                     'cross_share_mean': float(share.mean()), 'cross_share_mean_law': float(share_d.mean()),
                     'excess_from_cross': ex['cross_fraction_of_excess'], 'excess_from_cross_law': ex_d['cross_fraction_of_excess'],
                     'cross_share_crisis': ex['cross_share_crisis'], 'cross_share_crisis_law': ex_d['cross_share_crisis'],
                     'cross_share_normal': ex['cross_share_normal'], 'cross_share_normal_law': ex_d['cross_share_normal']}
    # the instantaneous identity, equal weights and equal swing sizes: cross share = 1 - N_eff / N
    zz = analytic(D.logs, D.years, (1970, 2022), 'P'); u = np.exp(1j * np.angle(zz)); N = len(D.isos)
    tot_u = np.abs(u.mean(axis=0)) ** 2 / 2; own_u = np.full_like(tot_u, 1 / (2 * N))
    out['identity_equal_swings'] = float(np.max(np.abs((1 - own_u / tot_u) - (1 - (1 / order.r(zz) ** 2) / N))))
    return out


def main():
    res = {}
    for s in SAMPLES:
        cfg = paper1.load_run_config(os.path.join(config.repo_root(), 'configs/runs/phase3_s31.yaml' if s == 'S31' else 'configs/runs/phase3.yaml'))
        D = paper1.load_data(s, tuple(cfg['span']))
        res[s] = {conv: summarize(series(D, conv)) for conv in ('P', 'C')}
        res[s]['N'] = len(D.isos); res[s]['decomposition'] = decomposition_link(D, cfg)
    os.makedirs(os.path.join(OUT, 'results'), exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'results', 'd3_neff.json'), 'w'), indent=1)
    from ef import dtt_text
    open(os.path.join(OUT, 'D3_real_data.md'), 'w').write(dtt_text.d3(res))
    print('wrote dtt/results/d3_neff.json and dtt/D3_real_data.md')
    return res


if __name__ == '__main__':
    main()
