"""Phase 1 'done when': the data build reproduces every atlas file, and the S26 Maddison panel reproduces r(t) to 1e-12.

The build runs twice into temporary folders from the pinned sources (about 10 seconds each): as used (GMD read as
float64, decision of 11 October 2026) and with --float32, the precision of the frozen as-run scripts.
"""
import hashlib
import json
import os

import numpy as np
import pytest
from scipy.signal import butter, filtfilt, hilbert

from ef import config
from ef.data import maddison
from ef.repro import compare

ROOT = config.repo_root()
ATLAS = ('panel.csv', 'global.csv', 'meta.json', 'stats.json', 'sync.json')
from conftest import needs_data

pytestmark = needs_data


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


@pytest.mark.slow
@pytest.mark.parametrize('name', ATLAS)
def test_atlas_file_reproduces_stored(built, name):
    t = compare(built / 'atlas' / name, os.path.join(ROOT, 'atlas', name))
    assert t.status() in ('EXACT', 'MATCH'), t.note()


@pytest.mark.slow
def test_channel_anatomy_reproduces_stored(built):
    t = compare(built / 'panel26_results.json', os.path.join(ROOT, 'paper1/results/panel26_results.json'))
    assert t.status() in ('EXACT', 'MATCH'), t.note()


@pytest.mark.slow
def test_float64_changes_no_repair_decision(built):
    """Every data repair (meta.json) is the same as in the stored atlas: the threshold rules all fall the same way."""
    assert sha(built / 'atlas' / 'meta.json') == sha(os.path.join(ROOT, 'atlas', 'meta.json'))


@pytest.mark.slow
@pytest.mark.parametrize('name', ['panel26_results.json'] + [f'atlas/{f}' for f in ATLAS])
def test_port_at_asrun_precision_is_byte_identical_to_asrun_scripts(built32, name):
    """Same machine, same precision, same bytes: the ported code is the as-run code. Needs make asrun to have run."""
    asrun = os.path.join(ROOT, 'build/asrun', 'internal/panel26_results.json' if name == 'panel26_results.json' else name)
    if not os.path.exists(asrun): pytest.skip("run make asrun first")
    assert sha(built32 / name) == sha(asrun)


def r_convention_P(wide, y0=1970, y1=2022):
    """Paper 1's r(t): band-pass and Hilbert transform on the whole 1950-2022 series, keep 1970-2022."""
    b, a = butter(2, [(1/9)/0.5, 0.49/0.5], btype='band')
    lg = np.log(wide.values); ph = np.angle(hilbert(filtfilt(b, a, lg - lg.mean(0), axis=0), axis=0))
    keep = (wide.index >= y0) & (wide.index <= y1)
    return np.abs(np.exp(1j * ph[keep]).mean(1))


@pytest.mark.slow
def test_S26_panel_reproduces_paper_r(built):
    W = maddison.wide(maddison.read(built / 'maddison_S26.csv'))
    ref = json.load(open(os.path.join(ROOT, 'paper1/results/kose_terrones_results.json')))['r_by_year']
    assert np.abs(r_convention_P(W) - np.array([ref[str(y)] for y in range(1970, 2023)])).max() < 1e-12


@pytest.mark.slow
def test_S30_panel_is_complete_and_exact(built):
    L = maddison.read(built / 'maddison_S30.csv')
    assert list(dict.fromkeys(L.iso)) == config.sample('S30')
    assert L.groupby('iso').year.agg(['min', 'max', 'count']).eq([1950, 2022, 73]).all().all()
    assert not L[['gdppc', 'pop']].isna().any().any()
    assert (L[['gdppc', 'pop']].values == maddison.panel('S30')[['gdppc', 'pop']].values).all()


def test_uae_fails_the_inclusion_rule():
    with pytest.raises(ValueError, match='ARE'):
        maddison.panel(['ARE'])
