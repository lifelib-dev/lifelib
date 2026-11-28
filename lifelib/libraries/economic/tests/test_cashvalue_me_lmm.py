"""CashValue_ME_LMM: lifelib's CashValue_ME_EX4 driven by an LMM ESG space.

The integration tests of section 8 of the design note, ``_research/lmm_design.md``, use
EX4's single-premium model points 1, 2, 5, 6 and 9, which mature at month 120 with no fees
or decrements. The level-premium points build up account values far above the sum assured,
so their GMAB cost is zero. For the closed form, the policies are made to mature at the
second tenor date, where an all-cash fund makes the guarantee a floorlet.
"""
import shutil
import uuid

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from modelx.core.errors import FormulaError
from scipy import stats

from lmm_registry import INPUT, MODEL_DIR, ROOT, write_workbook

CV_DIR = ROOT / "CashValue_ME_LMM"
SINGLE, LEVEL = [1, 2, 5, 6, 9], [3, 4, 7, 8]
T = 120                                   # maturity month of every model point
FUNDS = ["CASH", "BOND_MIX", "BOND_10Y"]


def read_cv():
    if not (CV_DIR / "__init__.py").exists():
        pytest.skip("CashValue_ME_LMM has not been built; run scripts/build_cashvalue_lmm.py")
    return mx.read_model(CV_DIR, name=f"CashValue_ME_LMM_{uuid.uuid4().hex[:8]}")


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


def point_amounts(model, t=T):
    """Total sum assured maturing at t and account value after the premium at 0, by point."""
    proj = model.Projection
    sa = by_point(model, proj.sum_assured() * proj.pols_maturity(t))[:, 0]
    av0 = by_point(model, proj.av_at(0, "BEF_FEE"))[:, 0]
    return pd.DataFrame({"sa": sa, "av0": av0}, index=proj.model_point_table_ext().index)


# ---- structure -----------------------------------------------------------------------

def test_structure():
    model = read_cv()
    try:
        source = mx.read_model(MODEL_DIR, name=f"BasicLMM_{uuid.uuid4().hex[:8]}")
        try:
            assert sorted(model.ESG.cells) == sorted(source.LMM.cells)
            for name in source.LMM.cells:
                assert (model.ESG.cells[name].formula.source
                        == source.LMM.cells[name].formula.source), name
        finally:
            source.close()
        proj = model.Projection
        assert proj.esg is model.ESG
        assert model.ESG.input_path().resolve() == INPUT.resolve()
        for name in ("scen_size", "scen_id", "std_norm_rand", "disc_rate_ann", "disc_rate_mth",
                     "formula_option_put", "formula_gmab_g2pp"):
            assert not hasattr(proj, name), name
        assert {"result_tvog", "formula_gmab_floorlet"} <= set(proj.cells)
    finally:
        model.close()


def test_projection_is_that_of_cashvalue_me_g2pp_apart_from_the_closed_form():
    model = read_cv()
    g2pp = mx.read_model(ROOT / "CashValue_ME_G2PP", name=f"G2PP_{uuid.uuid4().hex[:8]}")
    try:
        ours, theirs = model.Projection, g2pp.Projection
        assert set(ours.cells) - set(theirs.cells) == {"formula_gmab_floorlet"}
        assert set(theirs.cells) - set(ours.cells) == {"formula_gmab_g2pp"}
        for name in set(ours.cells) & set(theirs.cells):
            assert ours.cells[name].formula.source == theirs.cells[name].formula.source, name
    finally:
        g2pp.close()
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


# ---- the GMAB against its closed form at the second tenor date -------------------------

@pytest.mark.parametrize("tenor, term", [(12, 2), (6, 1)])
def test_gmab_at_the_second_tenor_date_matches_the_floorlet(lmm_workbook, tenor, term):
    """Policies of `term` years with an all-cash fund mature at the second tenor date."""
    model = read_cv()
    try:
        proj = model.Projection
        model.ESG.input_file = str(lmm_workbook(params=dict(
            fund_id="CASH", tenor_mth=tenor, scen_size=4_000, step_size=60)))
        proj.model_point_table = proj.model_point_moneyness.assign(policy_term=term)
        gmab = proj.result_tvog()["GMAB"].loc[SINGLE]
        formula = proj.formula_gmab_floorlet(2 * tenor)
        assert formula.index.tolist() == SINGLE
        exact = (gmab["SE"] == 0).to_numpy()
        assert exact.sum() == 1 and formula[exact].eq(0).all() and gmab["mean"][exact].eq(0).all()
        z = ((gmab["mean"] - formula) / gmab["SE"])[~exact]
        assert z.abs().max() < stats.norm.isf(0.00135 / len(z)), z.to_dict()
        amounts = point_amounts(model, 2 * tenor).loc[SINGLE]
        intrinsic = np.maximum(amounts["sa"] * model.ESG.mkt_zcb(2 * tenor) - amounts["av0"], 0)
        np.testing.assert_allclose(gmab["CE"], intrinsic, rtol=0, atol=1e-10 * 50e6)
    finally:
        model.close()


def test_closed_form_needs_the_second_tenor_date_and_an_all_cash_fund(run):
    with pytest.raises(FormulaError, match="needs the maturity at the second tenor date"):
        run("CASH").Projection.formula_gmab_floorlet(T)
    with pytest.raises(FormulaError, match="needs an all-cash fund"):
        run("BOND_MIX").Projection.formula_gmab_floorlet(24)


# ---- horizon and round trip ------------------------------------------------------------

def test_projection_longer_than_the_scenarios(lmm_workbook):
    model = read_cv()
    try:
        model.ESG.input_file = str(lmm_workbook(params=dict(step_size=60, scen_size=10)))
        with pytest.raises(FormulaError, match="the projection needs 121 months"):
            model.Projection.inv_return_table()
    finally:
        model.close()


def test_read_write_read_round_trip(tmp_path):
    model = read_cv()
    try:
        before = model.Projection.result_tvog()
        shutil.copy(INPUT, tmp_path / INPUT.name)
        mx.write_model(model, tmp_path / "CashValue_ME_LMM", backup=False)
        copy = mx.read_model(tmp_path / "CashValue_ME_LMM", name=f"copy_{uuid.uuid4().hex[:8]}")
        try:
            pd.testing.assert_frame_equal(copy.Projection.result_tvog(), before)
        finally:
            copy.close()
    finally:
        model.close()
