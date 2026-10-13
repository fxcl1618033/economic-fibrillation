"""G0 dataset: past-only phases, masks never filled, gap classes complete, edges as specified."""
import os

import numpy as np
import pytest

from conftest import needs_data
from ef import config
from ef.gnn import dataset as g

pytestmark = needs_data
OUT = os.path.join(config.load()['paths']['build'], 'gnn', 'g0')


@pytest.fixture(scope='module')
def built():
    if not os.path.exists(os.path.join(OUT, 'nodes.npz')): pytest.skip("run make gnn-g0 first")
    return g.load(OUT)


def test_phases_use_only_the_past():
    """The phase in 1990 is the same whether or not the data after 1990 exist."""
    from ef.phases import analytic
    from ef.data import maddison
    L = maddison.panel(['USA', 'RUS']); logs = np.log(maddison.wide(L).values.T); y = maddison.wide(L).index.to_numpy()
    a = analytic(logs, y, (1970, 2022), 'C'); b = analytic(logs[:, y <= 1990], y[y <= 1990], (1970, 1990), 'C')
    assert np.allclose(a[:, :21], b)


def test_masks_match_missing_values_and_nothing_is_filled(built):
    n, E = built
    assert np.array_equal(n['mask'], ~np.isnan(n['X']))
    assert ((n['gap'] == 'observed') == n['mask']).all()
    t = E['trade']
    assert (t[t.gap == 'observed'][['exports_fob_usd', 'mirror_imports_cif_usd']].notna().any(axis=1)).all()
    assert t[t.gap != 'observed'][['exports_fob_usd', 'mirror_imports_cif_usd']].isna().all().all()


def test_every_gap_has_a_known_class(built):
    n, E = built
    known = set(g.GAP_CLASSES) | {'not_a_feature'}
    assert set(np.unique(n['gap'])) <= known and all(set(e.gap) <= known for e in E.values())


def test_edges_as_specified(built):
    n, E = built
    isos = list(n['nodes'][:-1]); assert len(isos) == 31 and n['nodes'][-1] == g.WORLD
    b = E['bank']
    assert set(b.src) == {i for i in isos if g.BIS2[i] in g.LENDERS10} and 'RUS' not in set(b.src)
    assert (b[b.year < 1977].gap == 'before_bis').all()
    t = E['trade']; assert len(t) == 53 * 31 * 30 and (t[(t.year < 1992) & ((t.src == 'RUS') | (t.dst == 'RUS'))].gap == 'entity').all()
    assert set(E['oil'].dst) == {g.WORLD} and E['oil'].net_oil_exports_share_gdp.isna().all()
    assert 'correlation' not in ' '.join(E)
