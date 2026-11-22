"""CashValue_ME_G2PP: lifelib's CashValue_ME_EX4 driven by the ESG space.

The integration tests of section 8 of the design note, ``_research/g2pp_design.md``, use
EX4's single-premium model points 1, 2, 5, 6 and 9, which mature at month 120 with no fees
or decrements. The level-premium points build up account values far above the sum
assured, so their GMAB cost is zero.
"""
import shutil
import uuid

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from modelx.core.errors import FormulaError
from scipy import stats

from g2pp_registry import INPUT, MODEL_DIR, ROOT, write_workbook

CV_DIR = ROOT / "CashValue_ME_G2PP"
SINGLE, LEVEL = [1, 2, 5, 6, 9], [3, 4, 7, 8]
T = 120                                   # maturity month of every model point
FUNDS = ["CASH", "BOND_MIX", "BOND_10Y"]


def read_cv():
    if not (CV_DIR / "__init__.py").exists():
        pytest.skip("CashValue_ME_G2PP has not been built; run scripts/build_cashvalue_g2pp.py")
    return mx.read_model(CV_DIR, name=f"CashValue_ME_G2PP_{uuid.uuid4().hex[:8]}")


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    """run(fund_id): the model on the default input with that fund, read once per fund."""
    models = {}

    def get(fund_id):
        if fund_id not in models:
            path = write_workbook(tmp_path_factory.mktemp("input") / "input.xlsx",
                                  params=dict(fund_id=fund_id))
            model = read_cv()
            model.ESG.input_file = str(path)
            models[fund_id] = model
        return models[fund_id]
    yield get
    for model in models.values():
        model.close()


def by_point(model, values):
    """Reshape a per-row array of Projection to (model point, scenario)."""
    return np.asarray(values).reshape(model.Projection.point_size(), -1)


def point_amounts(model):
    """Total sum assured maturing at T and account value after the premium at 0, by point."""
    proj = model.Projection
    sa = by_point(model, proj.sum_assured() * proj.pols_maturity(T))[:, 0]
    av0 = by_point(model, proj.av_at(0, "BEF_FEE"))[:, 0]
    return pd.DataFrame({"sa": sa, "av0": av0}, index=proj.model_point_table_ext().index)


# ---- structure -----------------------------------------------------------------------

def test_structure():
    model = read_cv()
    try:
        source = mx.read_model(MODEL_DIR, name=f"BasicG2PP_{uuid.uuid4().hex[:8]}")
        try:
            assert sorted(model.ESG.cells) == sorted(source.G2PP.cells)
            for name in source.G2PP.cells:
                assert model.ESG.cells[name].formula.source == source.G2PP.cells[name].formula.source
        finally:
            source.close()
        proj = model.Projection
        assert proj.esg is model.ESG
        for name in ("scen_size", "scen_id", "std_norm_rand", "disc_rate_ann", "disc_rate_mth",
                     "formula_option_put"):
            assert not hasattr(proj, name), name
        assert {"result_tvog", "formula_gmab_g2pp"} <= set(proj.cells)
        assert not (CV_DIR / "disc_rate_ann.xlsx").exists()
        assert model.ESG.input_path().resolve() == INPUT.resolve()
    finally:
        model.close()


def test_scenarios_come_from_the_esg(run):
    model = run("BOND_MIX")
    proj, esg = model.Projection, model.ESG
    assert proj.scen_index().equals(esg.scen_index())
    n_scen = len(esg.scen_index())
    assert len(proj.model_point()) == proj.point_size() * n_scen
    assert np.array_equal(by_point(model, proj.inv_return_table()[:, 5])[3],
                          esg.fund_return_paths()[:, 5])
    assert np.array_equal(by_point(model, proj.disc_factors(60))[3], esg.disc_factor_paths()[:, 60])


def test_checks_of_the_projection(run):
    proj = run("BOND_MIX").Projection
    assert proj.check_av_roll_fwd()
    assert proj.check_pv_net_cf()


# ---- the GMAB against the ESG paths, scenario by scenario ------------------------------

@pytest.mark.parametrize("fund_id", FUNDS)
def test_gmab_cost_equals_the_payoff_in_every_scenario(run, fund_id):
    """PV of the GMAB = D(T) (SA - AV0 * growth)+ in every scenario, CE included."""
    model = run(fund_id)
    proj, esg = model.Projection, model.ESG
    pv = by_point(model, proj.pv_claims_over_av("MATURITY"))
    growth = np.prod(1 + esg.fund_return_paths()[:, :T], axis=1)
    deflator = esg.disc_factor_paths()[:, T]
    amounts = point_amounts(model)
    for k, point in enumerate(amounts.index):
        if point in SINGLE:
            sa, av0 = amounts.loc[point]
            expected = deflator * np.maximum(sa - av0 * growth, 0)
            np.testing.assert_allclose(pv[k], expected, rtol=0, atol=1e-10 * sa,
                                       err_msg=f"point {point}")
        else:
            assert not pv[k].any(), f"level-premium point {point}"


@pytest.mark.parametrize("fund_id", FUNDS)
def test_ce_value_is_the_intrinsic_value(run, fund_id):
    model = run(fund_id)
    tvog = model.Projection.result_tvog()["GMAB"]
    amounts = point_amounts(model).loc[SINGLE]
    intrinsic = np.maximum(amounts["sa"] * model.ESG.mkt_zcb(T) - amounts["av0"], 0)
    np.testing.assert_allclose(tvog.loc[SINGLE, "CE"], intrinsic, rtol=0,
                               atol=1e-10 * amounts["sa"].max())


def test_result_tvog_table(run):
    tvog = run("BOND_MIX").Projection.result_tvog()
    assert tvog.columns.get_level_values(0).unique().tolist() == ["GMAB", "GMDB", "net cash flow"]
    assert tvog.index.tolist() == list(range(1, 10))
    for measure in ("GMAB", "GMDB", "net cash flow"):
        np.testing.assert_allclose(tvog[measure]["TVOG"], tvog[measure]["mean"] - tvog[measure]["CE"])
    assert (tvog["GMDB"] == 0).all().all()     # EX4 has no mortality


# ---- the GMAB against its closed form --------------------------------------------------

@pytest.mark.parametrize("fund_id", ["CASH", "BOND_10Y"])
def test_gmab_mean_matches_the_closed_form(run, fund_id):
    proj = run(fund_id).Projection
    tvog = proj.result_tvog()["GMAB"].loc[SINGLE]
    formula = proj.formula_gmab_g2pp(T)
    assert formula.index.tolist() == SINGLE
    z = (tvog["mean"] - formula) / tvog["SE"]
    limit = stats.norm.isf(0.00135 / len(z))      # the rule of the Validation space
    assert z.abs().max() < limit, z.to_dict()


def test_closed_form_needs_a_single_maturity_fund(run):
    with pytest.raises(FormulaError, match="needs an all-cash or single-maturity fund"):
        run("BOND_MIX").Projection.formula_gmab_g2pp(T)


def test_all_cash_closed_form_is_black_scholes_with_the_g2pp_variance(run):
    """With P = exp(-rT) and V(0,T) = sigma^2 T the closed form is EX1's BSM put."""
    model = run("CASH")
    proj, esg = model.Projection, model.ESG
    amounts = point_amounts(model).loc[SINGLE]
    r = -np.log(esg.mkt_zcb(T)) / (T / 12)
    vol = np.sqrt(esg.V_t_T(0, T) / (T / 12))
    S, X, tau = amounts["av0"], amounts["sa"], T / 12
    d1 = (np.log(S / X) + (r + vol**2 / 2) * tau) / (vol * np.sqrt(tau))
    d2 = d1 - vol * np.sqrt(tau)
    bsm_put = X * np.exp(-r * tau) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    np.testing.assert_allclose(proj.formula_gmab_g2pp(T), bsm_put, rtol=1e-12)


# ---- horizon and round trip ------------------------------------------------------------

def test_projection_longer_than_the_scenarios(workbook):
    model = read_cv()
    try:
        model.ESG.input_file = str(workbook(params=dict(step_size=60, scen_size=10)))
        with pytest.raises(FormulaError, match="the projection needs 121 months"):
            model.Projection.inv_return_table()
    finally:
        model.close()


def test_read_write_read_round_trip(tmp_path):
    model = read_cv()
    try:
        before = model.Projection.result_tvog()
        shutil.copy(INPUT, tmp_path / INPUT.name)
        mx.write_model(model, tmp_path / "CashValue_ME_G2PP", backup=False)
        copy = mx.read_model(tmp_path / "CashValue_ME_G2PP", name=f"copy_{uuid.uuid4().hex[:8]}")
        try:
            pd.testing.assert_frame_equal(copy.Projection.result_tvog(), before)
        finally:
            copy.close()
    finally:
        model.close()
