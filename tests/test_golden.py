"""Phase 2 'done when': the library reproduces tests/golden_paper1.json on S26 (configs/runs/paper1_S26_asrun.yaml).

Deterministic values within 1e-9; surrogate p-values within their stated Monte Carlo tolerance, and in fact exactly,
because the surrogates are drawn in the as-run order. The atlas_sync values come from the src data build.
"""
import json
import os

import pytest

from conftest import needs_data
from ef import config
from ef.paper1 import golden_view

pytestmark = [needs_data, pytest.mark.slow]
GOLDEN = json.load(open(os.path.join(config.repo_root(), 'tests/golden_paper1.json')))['values']


@pytest.fixture(scope='module')
def view(paper1, built):
    return golden_view(paper1, json.load(open(built / 'atlas' / 'sync.json')))


@pytest.mark.parametrize('g', GOLDEN, ids=[f"{i:03d}-{g['key']}" for i, g in enumerate(GOLDEN)])
def test_golden_value(view, g):
    assert g['key'] in view, f"{g['key']} not computed"
    assert abs(view[g['key']] - g['value']) <= g['tol'], f"{g['key']}: stored {g['value']!r}, computed {view[g['key']]!r} ({g['source']})"


def test_surrogate_p_values_are_exact(view):
    """With the as-run seeds and draw order the Monte Carlo p-values are not just within tolerance but identical."""
    mc = [g for g in GOLDEN if 'surrogate p' in g['note']]
    assert len(mc) == 7
    assert all(abs(view[g['key']] - g['value']) <= 1e-12 for g in mc), [(g['key'], g['value'], view[g['key']]) for g in mc]
