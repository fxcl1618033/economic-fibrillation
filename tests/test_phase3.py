"""Phase 3 building blocks: sample variants, the band-pass-only surrogate source, the channel tests and the report."""
import json
import os

import numpy as np
import pytest

from conftest import needs_data
from ef import channels, comparison, config
from ef.paper1 import TESTS, cycle_source, load_data, load_run_config
from ef.phases import window_cycles

pytestmark = needs_data
ROOT = config.repo_root(); REC = [1975, 1982, 1991, 2009, 2020]


def test_phase3_config_names_only_known_tests():
    cfg = load_run_config(os.path.join(ROOT, 'configs/runs/phase3.yaml'))
    assert set(cfg['tests']) <= set(TESTS) and set(cfg['variants']['strict_inside_1970_2022']['tests']) <= set(TESTS)


def test_drop_and_named_sample_agree():
    a, b = load_data('S30', drop=['IRN']), load_data([i for i in config.sample('S30') if i != 'IRN'])
    assert a.isos == b.isos and np.array_equal(a.logs, b.logs) and 'IRN' not in a.isos and len(a.isos) == 29


def test_gmd_growth_swap_changes_only_the_named_years():
    a = load_data('S26'); b = load_data('S26', gmd_growth={'economies': ['NOR'], 'years': [1991, 2011]})
    j = a.isos.index('NOR'); y = a.years; ga, gb = np.diff(a.logs[j]), np.diff(b.logs[j])
    same = (y[1:] < 1991) | (y[1:] > 2011)
    assert np.allclose(ga[same], gb[same]) and not np.allclose(ga[~same], gb[~same])
    assert np.array_equal(np.delete(a.logs, j, 0), np.delete(b.logs, j, 0))


def test_P_surrogate_source_cuts_the_full_span_cycles():
    D = load_data('S26'); X, Xsrc, cut = cycle_source(D, (1962, 2022), 'P', (9.0, 0.49))
    assert Xsrc.shape[-1] == 73 and np.array_equal(cut(Xsrc), X) and np.array_equal(X, window_cycles(D.logs, D.years, (1962, 2022)))


@pytest.mark.slow
def test_channel_sync_reproduces_the_atlas(built):
    s = channels.sync(str(built / 'atlas'), config.sample('S26'), REC, 'P'); ref = json.load(open(built / 'atlas' / 'sync.json'))
    for ch in ('GDP', 'inv', 'strate'):
        assert s[ch]['tests_rounded'] == ref['tests'][ch] and np.abs(np.array(s[ch]['r_t']) - np.array(ref['r_t'][ch])).max() < 1e-12


@pytest.mark.slow
def test_contracting_and_coupling_reproduce_the_atlas(built):
    A = str(built / 'atlas'); S26 = config.sample('S26'); st = json.load(open(built / 'atlas' / 'stats.json'))
    assert channels.contracting(A, S26, REC) == {1975: 11, 1982: 8, 1991: 8, 2009: 22, 2020: 25}
    c = channels.coupling(A, S26)
    assert abs(c['1970-1989'] - np.mean([st[i]['coup_7089'] for i in S26])) < 1e-12
    assert abs(c['1990-2022'] - np.mean([st[i]['coup_9022'] for i in S26])) < 1e-12


def test_past_only_channel_phase_ignores_the_future():
    import pandas as pd
    s = pd.Series(np.cumsum(np.random.default_rng(0).standard_normal(73)), index=np.arange(1950, 2023))
    t = s.copy(); t.loc[2001:] += 5
    a, b = channels._phases(s, 'C'), channels._phases(t, 'C')
    assert np.array_equal(a[:31], b[:31]) and not np.allclose(a[31:], b[31:])


def test_report_readings():
    assert comparison.verdict((0.2, 0.019), (0.21, 0.019), 'sig') == 'replicates'
    assert comparison.verdict((0.2, 0.019), (0.21, 0.06), 'sig') == '**weakens**'
    assert comparison.verdict((0.2, 0.019), (-0.1, 0.5), 'sig') == '**reverses**'
    assert comparison.verdict((0.1, 0.3), (0.1, 0.03), 'null') == '**becomes significant**'
    assert comparison.flag((0.2, 0.019), (-0.2, 0.019)) == 'sign change' and comparison.flag((0.2, 0.019), (0.2, 0.06)) == 'crosses 0.05'


def test_csd_by_event_reproduces_csd_and_averages_events():
    """The leave-one-crisis-out follow-up uses the Phase 3 test's own trends and surrogates: the full set is run_csd."""
    from ef.paper1 import run_csd, run_csd_by_event
    cfg = load_run_config(os.path.join(ROOT, 'configs/runs/phase3.yaml')); t = dict(cfg['tests']['csd'], surrogates=300)
    D = load_data('S26'); a = run_csd(D, cfg, t); b = run_csd_by_event(D, cfg, t)['sets']
    for n in ('ar1', 'var'): assert b['all'][f'tau_{n}'] == a[f'tau_{n}'] and b['all'][f'p_{n}'] == a[f'p_{n}']
    assert b['all']['events'] == [1982, 1991, 2009, 2020] and 'only_1975' not in b
    one = [b[f'only_{e}']['tau_var'] for e in b['all']['events']]
    assert np.isclose(np.mean(one), a['tau_var']) and np.isclose(b['without_2009_2020']['tau_var'], np.mean(one[:2]))
