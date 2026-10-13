"""G0 dataset: past-only phases, masks never filled, gap classes complete, edges as specified."""
import os

import numpy as np
import pandas as pd
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
    assert (t[t.gap == 'observed'][['raw_exports_fob_usd', 'raw_mirror_imports_cif_usd']].notna().any(axis=1)).all()
    assert t[t.gap != 'observed'][['raw_exports_fob_usd', 'raw_mirror_imports_cif_usd']].isna().all().all()
    for e in E.values():                                   # a weight is present exactly where its gap class says so
        for c in [c for c in e.columns if c.startswith('gap_')]:
            w = {'gap_w_exports': 'w_exports_share_dst_gdp', 'gap_w_mirror': 'w_mirror_share_dst_gdp',
                 'gap_s_exports': 's_exports_share_src_total', 'gap_s_mirror': 's_mirror_share_src_total',
                 'gap_w_claims': 'w_claims_share_dst_gdp', 'gap_s_claims': 's_claims_share_src_total'}[c]
            assert ((e[c] == 'observed') == e[w].notna()).all()


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
    assert set(E['oil'].dst) == {g.WORLD}
    assert 'correlation' not in ' '.join(E)
    assert (b[(b.dst == 'RUS') & (b.year < 1993)].w_claims_share_dst_gdp.isna()).all()
    o = E['oil']; assert (o[(o.src == 'RUS') & (o.year < g.RUSSIA_OIL_FROM)].gap == 'entity').all()


def test_weights_are_flows_over_the_stated_denominators(built):
    n, E = built
    gdp = pd.read_csv(os.path.join(OUT, 'gdp_current_usd.csv'), index_col=0); gdp.columns = gdp.columns.astype(str)
    t = E['trade'].dropna(subset=['w_exports_share_dst_gdp'])
    den = np.array([gdp.at[y, j] for y, j in zip(t.year, t.dst)])
    assert np.allclose(t.w_exports_share_dst_gdp, t.raw_exports_fob_usd / den)
    b = E['bank'].dropna(subset=['w_claims_share_dst_gdp', 's_claims_share_src_total'])
    assert np.allclose(b.w_claims_share_dst_gdp, b.raw_claims_usd / np.array([gdp.at[y, j] for y, j in zip(b.year, b.dst)]))
    assert np.allclose(b.s_claims_share_src_total, b.raw_claims_usd / b.raw_lender_claims_all_countries_usd)
    # a known size: US goods exports to Mexico in 2022, about a fifth of Mexico's GDP
    us_mx = E['trade'].query('year == 2022 and src == "USA" and dst == "MEX"').w_exports_share_dst_gdp.item()
    assert 0.15 < us_mx < 0.30


def test_oil_weight_is_the_stated_conversion(built):
    n, E = built
    assert abs(g.BBL_PER_TWH - 630266.6) < 0.1
    o = E['oil'].dropna(subset=['w_net_oil_exports_share_gdp'])
    gdp = pd.read_csv(os.path.join(OUT, 'gdp_current_usd.csv'), index_col=0); gdp.columns = gdp.columns.astype(str)
    v = (o.raw_oil_production_twh - o.raw_oil_consumption_twh) * g.BBL_PER_TWH * o.oil_price_usd_per_bbl
    assert np.allclose(o.w_net_oil_exports_share_gdp, v / np.array([gdp.at[y, i] for y, i in zip(o.year, o.src)]))
    price, src, check = g.oil_price_nominal()
    assert check < 0.01 and (src[src.index >= g.OIL_PRICE_SWITCH] == 'eia_brent').all()
    sau = o.query('src == "SAU" and year == 1980').w_net_oil_exports_share_gdp.item()
    jpn = o.query('src == "JPN" and year == 1980').w_net_oil_exports_share_gdp.item()
    assert sau > 0.5 and -0.1 < jpn < 0                    # a large net exporter and a large net importer


def test_raw_dollars_are_never_model_inputs(built):
    n, E = built
    for variant in ('primary', 'sensitivity'):
        for k, d in g.model_inputs(E, variant).items():
            assert not [c for c in d.columns if c.startswith('raw_')]
            assert all(c.startswith(('w_', 's_', 'mask_')) or c in ('year', 'src', 'dst') or c in g.MODEL_INPUTS[k]['flags'] for c in d.columns)


def test_oil_production_sources_follow_the_stated_rules(built):
    """EIA only for 2017-22 and only where the comparison agrees; true zeros only for the five classed economies;
    the BP-price flag exactly before 1987."""
    n, E = built
    o = E['oil']; S, L = g.eia_comparison(list(n['nodes'][:-1]))
    eia = o[o.production_from_eia]
    assert eia.year.between(*g.EIA_EXTEND).all() and set(eia.src) == set(S[S.agree & ~S.true_zero].iso)
    assert not set(eia.src) & {'JPN', 'ZAF'}                            # both fail the tolerance fixed beforehand
    tz = o[o.production_true_zero]
    assert set(tz.src) == set(g.TRUE_ZERO_PRODUCERS) and (tz.raw_oil_production_twh == 0).all()
    assert (o[o.src.isin(g.TRUE_ZERO_PRODUCERS)].raw_oil_production_twh == 0).all()
    assert (o.price_from_bp_series == (o.year < g.OIL_PRICE_SWITCH)).all()
    # the rule itself: d_t = |EIA - OWID| / max(OWID, 10 TWh)
    assert np.allclose(L.d, (L.eia_twh - L.owid_twh).abs() / np.maximum(L.owid_twh, g.EIA_FLOOR_TWH))
    for x in S.itertuples():
        d = L[L.iso == x.iso]
        ok = d.d.median() <= g.EIA_TOL and all(((d.year == y) & (d.d <= g.EIA_TOL)).any() for y in range(2012, 2017))
        assert ok == x.agree


def test_world_bank_denominator_is_the_pinned_file(built):
    """The fresh World Bank download failed the exact-match check, so the denominators are still the pinned file's."""
    gdp = pd.read_csv(os.path.join(OUT, 'gdp_current_usd.csv'), index_col=0); gdp.columns = gdp.columns.astype(str)
    assert gdp.loc[1970:1988, 'BRA'].isna().all()
    V = g.wb_vintage_comparison(list(gdp.columns)).dropna(subset=['old', 'new'])
    assert (V.rel.abs() > 1e-3).any()                                   # why the condition fails
