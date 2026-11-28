"""BasicLMM's Validation space, and the statistical tests of the library's design note.

The fast tests check the space itself. The tests marked slow run the statistical checks of
section 8 of the design note, ``_research/lmm_design.md``: 10,000 antithetic scenarios over
20 years, 2,000 over
50 years and 500 over 140 years with annual forward rates, and 2,000 over 10 years with
monthly ones. They run by default; ``-m "not slow"`` leaves them out.

A test with m z-scores passes if its largest |z| is below Phi^-1(1 - 0.00135/m): the same
chance of a false alarm as a single 3-sigma check, and a limit of 3 when m = 1.
"""
import ast
import inspect
import textwrap
import uuid

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from scipy import stats

from lmm_registry import INPUT, MODEL_DIR, write_workbook
from reference_lmm import ReferenceLMM, read_inputs

VALIDATION_CELLS = {"martingale_test", "fund_martingale_test", "curve_fit_test",
                    "zcb_martingale_test", "caplet_cf", "caplet_mc", "caplet_test", "fwd_swap",
                    "swaption_vol", "swaption_test", "summary"}


def z_limit(m):
    return stats.norm.isf(0.00135 / m)


def assert_within_limit(df):
    z = df["z"].abs()
    limit = z_limit(len(z))
    assert z.max() < limit, (f"max |z| = {z.max():.2f} at {z.idxmax()}, "
                             f"limit {limit:.2f} for {len(z)} z-scores")


def read_model_on(path):
    model = mx.read_model(MODEL_DIR, name=f"BasicLMM_{uuid.uuid4().hex[:8]}")
    model.LMM.input_file = str(path)
    return model


def code_of(func):
    """A function's code without its docstring, as an AST dump."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(func))).body[0]
    if ast.get_docstring(tree) is not None:
        tree.body = tree.body[1:]
    return ast.dump(tree)


# ---- the space and its helper ------------------------------------------------------

def test_validation_space(lmm_model):
    v = lmm_model.Validation
    assert VALIDATION_CELLS <= set(v.cells)
    assert v.lmm is lmm_model.LMM


def test_mcstats_has_the_functions_of_basic_g2pp(lmm_model, model):
    ours, theirs = lmm_model.Validation.mcstats, model.Validation.mcstats
    for name in ("mean_se", "check"):
        assert code_of(getattr(ours, name)) == code_of(getattr(theirs, name)), name


def test_summary_on_a_small_run(lmm_model, lmm_workbook):
    lmm_model.LMM.input_file = str(lmm_workbook(params=dict(scen_size=200, step_size=120)))
    summary = lmm_model.Validation.summary()
    assert summary.columns.tolist() == ["checks", "max_abs_z", "limit", "ok", "at"]
    assert len(summary) == 5 and np.isfinite(summary["max_abs_z"]).all()
    assert summary.loc["martingale_test()", "checks"] == 121
    assert summary.loc["caplet_test()", "checks"] == 10
    assert summary.loc["martingale_test()", "limit"] == pytest.approx(z_limit(121))


def test_first_tenor_period_is_exact(lmm_model, lmm_workbook):
    """The deflators of the first year are known at time 0, so their z is 0."""
    lmm_model.LMM.input_file = str(lmm_workbook(params=dict(scen_size=200, step_size=120)))
    v = lmm_model.Validation
    assert (v.martingale_test()["z"].iloc[:13] == 0).all()
    assert v.curve_fit_test().loc[1.0, "z"] == 0


def test_all_cash_fund_is_exactly_a_martingale(lmm_model, lmm_workbook):
    lmm_model.LMM.input_file = str(lmm_workbook(params=dict(fund_id="CASH", scen_size=200,
                                                            step_size=120)))
    df = lmm_model.Validation.fund_martingale_test()
    assert (df["z"] == 0).all()
    np.testing.assert_allclose(df["mc"], 1.0, rtol=1e-12)


def test_curve_fit_with_continuous_compounding(lmm_model, lmm_workbook):
    lmm_model.LMM.input_file = str(lmm_workbook(params=dict(compounding="continuous",
                                                            scen_size=200, step_size=120)))
    df = lmm_model.Validation.curve_fit_test()
    assert df.index.tolist() == [float(k) for k in range(1, 11)]
    spot = pd.read_excel(INPUT, sheet_name="Curve")["EUR_BASE"].head(10)
    np.testing.assert_array_equal(df["theory"].to_numpy(), spot.to_numpy())
    assert_within_limit(df)


@pytest.mark.parametrize("params", [{}, dict(tenor_mth=3, shift=0.0, curve_id="GBP_UP")])
def test_closed_forms_equal_the_reference(lmm_model, lmm_workbook, params):
    path = lmm_workbook(params={**params, "scen_size": 10, "step_size": 120})
    lmm_model.LMM.input_file = str(path)
    v, ref = lmm_model.Validation, ReferenceLMM(**read_inputs(path))
    for k in (2, 7, 20):
        for x in (0.01, ref.F0[k - 1], 0.05):
            assert v.caplet_cf(k, x) == pytest.approx(ref.caplet(k, x), rel=1e-12)
    for a, b in ((1, 5), (5, 5)):
        vol, swap, annuity = ref.swaption_vol(a, b)
        assert v.swaption_vol(a, b) == pytest.approx(vol, rel=1e-12)
        assert v.fwd_swap(a, b) == pytest.approx((swap, annuity), rel=1e-12)


def test_caplet_with_a_strike_below_minus_the_shift_is_a_forward(lmm_model):
    v, g = lmm_model.Validation, lmm_model.LMM
    x = -0.05
    forward = 1.0 * g.mkt_zcb(36) * (g.mkt_fwd_rates()[2] - x)
    assert v.caplet_cf(3, x) == pytest.approx(forward, rel=1e-14)
    df = v.caplet_mc(3, x)
    assert abs(df["z"].iloc[0]) < 3


def test_swaption_test_is_close_at_the_money(lmm_model, lmm_workbook):
    """A diagnostic of an approximation: here only that it runs and is near the price."""
    lmm_model.LMM.input_file = str(lmm_workbook(params=dict(scen_size=2_000, step_size=60)))
    df = lmm_model.Validation.swaption_test(5, 5)
    assert df.index.tolist() == [(5, 5)]
    assert df["mc"].iloc[0] == pytest.approx(df["theory"].iloc[0], rel=0.05)


# ---- statistical tests: 10,000 antithetic scenarios over 20 years ----------------------

@pytest.fixture(scope="module")
def v10k(tmp_path_factory):
    path = write_workbook(tmp_path_factory.mktemp("v10k") / "input.xlsx",
                          params=dict(scen_size=10_000, step_size=240))
    model = read_model_on(path)
    yield model.Validation
    model.close()


@pytest.mark.slow
@pytest.mark.parametrize("name", ["martingale_test", "fund_martingale_test",
                                  "curve_fit_test", "caplet_test"])
def test_statistics_of_20_years(v10k, name):
    assert_within_limit(getattr(v10k, name)())


@pytest.mark.slow
@pytest.mark.parametrize("i, j", [(12, 120), (60, 180), (120, 360), (234, 360)])
def test_deflated_bond_prices(v10k, i, j):
    assert_within_limit(v10k.zcb_martingale_test(i, j))


@pytest.mark.slow
@pytest.mark.parametrize("k", [2, 6, 11])
@pytest.mark.parametrize("moneyness", [0.75, 1.0, 1.5])
def test_caplets(v10k, k, moneyness):
    g = v10k.lmm
    alpha = g.shift()
    strike = moneyness * (g.mkt_fwd_rates()[k - 1] + alpha) - alpha
    assert_within_limit(v10k.caplet_mc(k, strike))


@pytest.mark.slow
def test_summary_passes(v10k):
    summary = v10k.summary()
    assert summary["ok"].all(), summary.to_string()


@pytest.mark.slow
def test_single_maturity_fund_is_a_martingale(tmp_path):
    model = read_model_on(write_workbook(tmp_path / "input.xlsx", params=dict(
        scen_size=4_000, step_size=240, fund_id="BOND_10Y")))
    try:
        assert_within_limit(model.Validation.fund_martingale_test())
    finally:
        model.close()


# ---- statistical tests: long horizons, and a monthly tenor -----------------------------

@pytest.mark.slow
@pytest.mark.parametrize("scen_size, step_size", [(2_000, 600), (500, 1_680)],
                         ids=["50 years", "140 years"])
def test_long_horizons(tmp_path, scen_size, step_size):
    model = read_model_on(write_workbook(tmp_path / "input.xlsx", params=dict(
        scen_size=scen_size, step_size=step_size)))
    try:
        v = model.Validation
        for name in ("martingale_test", "fund_martingale_test", "curve_fit_test"):
            assert_within_limit(getattr(v, name)())
        assert len(v.martingale_test()) == step_size + 1
        assert len(v.curve_fit_test()) == step_size // 12
    finally:
        model.close()


@pytest.mark.slow
def test_monthly_tenor(tmp_path):
    """With tenor_mth 1 nothing is interpolated; 2,000 scenarios over 10 years."""
    model = read_model_on(write_workbook(tmp_path / "input.xlsx", params=dict(
        tenor_mth=1, scen_size=2_000, step_size=120)))
    try:
        v = model.Validation
        for name in ("martingale_test", "fund_martingale_test", "curve_fit_test",
                     "caplet_test"):
            assert_within_limit(getattr(v, name)())
    finally:
        model.close()
