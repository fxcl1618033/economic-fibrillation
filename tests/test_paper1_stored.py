"""Beyond the golden numbers: every other stored Paper 1 result the library recomputes, compared with the stored
results files (1e-9) or, for scripts that only printed, with their printout at the printed precision."""
import json
import os

import numpy as np
import pytest

from conftest import needs_data
from ef import config

pytestmark = [needs_data, pytest.mark.slow]
ROOT = config.repo_root()
S = lambda f: json.load(open(os.path.join(ROOT, 'paper1/results', f)))
PRINTED = lambda f: open(os.path.join(ROOT, 'paper1/results/printed', f)).read()
LABELS = ['2 yr before', '1 yr before', 'crisis year', '1 yr after', '2 yr after']
KEYS = ['lead2', 'lead1', 'crisis', 'after1', 'after2']


def close(a, b, tol=1e-9):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return a.shape == b.shape and np.allclose(a, b, rtol=0, atol=tol, equal_nan=True)


def test_arc_bootstrap_epoch_and_two_sided_p(paper1):
    kt, R = S('kose_terrones_results.json'), paper1['arc']
    for k, s in (('recession', 'mean_recession'), ('downturn', 'mean_downturn'), ('normal', 'mean_normal')):
        assert close(R['mean_ci'][k], kt[s])
    assert close([R['arc'][k]['p_two'] for k in KEYS], [kt['arc'][l]['p_two'] for l in LABELS])
    assert close(R['epoch_mean_t-4..t+4'], kt['epoch_mean'])
    assert close([R['r_by_year'][y] for y in range(1970, 2023)], [kt['r_by_year'][str(y)] for y in range(1970, 2023)])


def test_multiplicity_corrections(paper1):
    """Registry A8/A9 (Methods 7.4). Bonferroni for lead-1 and after-2 is 5/53 = 0.0943 exactly; the Methods print
    0.095 (5 x the rounded 0.019)."""
    b, q = paper1['arc']['bonferroni'], paper1['arc']['benjamini_hochberg']
    assert round(b['lead1'], 4) == round(b['after2'], 4) == 0.0943 and round(b['lead2'], 3) == 0.189
    assert round(q['lead1'], 3) == round(q['after2'], 3) == 0.047 and round(q['lead2'], 3) == 0.063


def test_amplitude(paper1):
    am, R = S('amplitude_results.json'), paper1['amplitude']
    assert close([R['corr_detrended'], R['p_shift']], am['corr_r_A_detr']) and close(R['corr_raw'], am['corr_r_A_raw'])
    assert close(R['null_mean'], am['null_mean'])


@pytest.mark.parametrize('kind,f', [('gdp_end', 'diversification_results.json'), ('equal', 'diversification_equal_results.json')])
def test_diversification(paper1, kind, f):
    d, R = S(f), paper1['diversification'][kind]
    for k in ('p_surrogate', 'corr_rbar_r', 'excess_from_own', 'excess_from_cross'):
        assert close(R[k], d[k], 1e-12 if k == 'p_surrogate' else 1e-9), k


def test_diversification_methods_weights(paper1):
    """Methods 6.1 and registry D1/D4: within-window mean GDP weights give 82.4%, cross shares 0.723 and 0.669."""
    g = paper1['diversification']['gdp_mean']
    assert (round(100 * g['cross_fraction_of_excess'], 1), round(g['cross_share_crisis'], 3), round(g['cross_share_normal'], 3)) == (82.4, 0.723, 0.669)


def test_cross_split_matches_printout(paper1):
    txt = PRINTED('crossterm_split_output.txt')
    for kind in ('gdp_end', 'equal'):
        c = paper1['cross_split'][kind]
        assert f"mean pairwise corr: normal {c['corr_normal']:.3f} -> crisis {c['corr_crisis']:.3f}" in txt
        assert f"mean cycle s.d.:    normal {c['sd_normal']:.4f} -> crisis {c['sd_crisis']:.4f}  (x{c['sd_crisis'] / c['sd_normal']:.2f})" in txt
        assert (f"({c['from_correlation']:.0%}) | from swing size alone {c['from_swing_size'] * c['rise']:.2e} ({c['from_swing_size']:.0%}) "
                f"| interaction {c['interaction']:.0%}") in txt


def test_structure(paper1):
    st, R = S('structure_results.json'), paper1['structure']
    assert close([R['dZ'], R['dA'], R['dR']], [st['dZ'], st['dA'], st['dR']])
    assert (R['blocA'], R['blocB']) == (st['blocA'], st['blocB'])
    assert R['identity_err'] < 1e-18
    for k, k2 in (('r (all)', 'r'), ('r_within blocs', 'r_within'), ('r_between blocs', 'r_between')):
        assert close([[x[1], x[2]] for x in st['hier'][k]], [[R['hier'][k2][l]['corr'], R['hier'][k2][l]['p']] for l in ('lead2', 'lead1', 'crisis', 'after2')])


def test_mst(paper1):
    ms, R = S('mst_results.json'), paper1['mst']
    assert close([R['tau_lambdamax'], R['p_fragility']], [ms['tau_lambdamax'], ms['p_fragility']], 1e-12)
    assert close([R['L_by_year'][y] for y in range(1971, 2023)], [ms['L_by_year'][str(y)] for y in range(1971, 2023)])
    assert close([R['lambdamax_by_year'][y] for y in range(1971, 2023)], [ms['lambdamax_by_year'][str(y)] for y in range(1971, 2023)])
    assert close([R['centrality'][c] for c in ms['central']], list(ms['central'].values()))


def test_phase_lags(paper1):
    pl, R = S('phase_lag_results.json'), paper1['phase_lags']
    assert close([R['lead_years'][c] for c in pl['lead_years']], list(pl['lead_years'].values()))
    assert close([R['per_crisis'][o][c] for o in (2009, 2020) for c in pl['per_crisis'][str(o)]],
                 [pl['per_crisis'][str(o)][c] for o in (2009, 2020) for c in pl['per_crisis'][str(o)]])
    assert R['p_spread_upper_as_run'] == pl['p_spread'] == 1.0          # what was stored (open issue 8)
    assert abs(R['p_spread_lower'] - 1 / 5001) < 1e-15                    # what the Methods report: every surrogate wider


def test_csd_and_bifurcation(paper1):
    cs, kb = S('csd_surrogate_results.json'), S('kuramoto_bifurcation_results.json')
    assert close([paper1['csd']['tau_ar1'], paper1['csd']['tau_var']], [cs['tau_ar_real'], cs['tau_va_real']])
    assert close(paper1['bifurcation']['null_mean'], kb['null_mean'])
    assert close([paper1['bifurcation']['KKc_by_year'][y] for y in range(1962, 2023)], [kb['KKc_by_year'][str(y)] for y in range(1962, 2023)])


def test_robustness_matches_printout(paper1):
    """Every row of robustness.py's printout (registry B1-B15), at the printed precision."""
    txt = PRINTED('robustness_output.txt')
    for tag, res in paper1['robustness'].items():
        s = lambda k: f"{res[k][0]:+.2f}(p={res[k][1]:.3f}){'*' if res[k][1] < 0.05 else ' '}"
        line = f"  {tag:32s} lead2 {s('lead2')}  lead1 {s('lead1')}  crisis {s('crisis')}  after2 {s('after2')}"
        assert line.rstrip() in txt, line
