"""The Validation space, and the statistical tests of the library's design note.

The fast tests check the space itself. The tests marked slow run the statistical checks of
section 8 of the design note, ``_research/g2pp_design.md``, with 10,000 antithetic
scenarios over 50 years, and with 2,000 scenarios over 150 years. They run by default;
``-m "not slow"`` leaves them out.

A test with m z-scores passes if its largest |z| is below Phi^-1(1 - 0.00135/m): the same
chance of a false alarm as a single 3-sigma check, and a limit of 3 when m = 1.
"""
import uuid

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from scipy import stats

from g2pp_registry import INPUT, MODEL_DIR, write_workbook

VALIDATION_CELLS = {"martingale_test", "fund_martingale_test", "curve_fit_test",
                    "zcb_martingale_test", "moments_test", "zbp_cf", "zbp_mc",
                    "deflator_call_test", "summary"}


def z_limit(m):
    return stats.norm.isf(0.00135 / m)


def assert_within_limit(df):
    z = df["z"].abs()
    limit = z_limit(len(z))
    assert z.max() < limit, (f"max |z| = {z.max():.2f} at {z.idxmax()}, "
                             f"limit {limit:.2f} for {len(z)} z-scores")


def read_model_on(path):
    model = mx.read_model(MODEL_DIR, name=f"BasicG2PP_{uuid.uuid4().hex[:8]}")
    model.G2PP.input_file = str(path)
    return model


# ---- the space and its helper ------------------------------------------------------

def test_validation_space(model):
    v = model.Validation
    assert VALIDATION_CELLS <= set(v.cells)
    assert v.g2pp is model.G2PP


def test_mcstats_check(model):
    check = model.Validation.mcstats.check
    df = check(np.array([1.0, 2.0, 3.0, 4.0]), 2.5, antithetic=False)
    assert df.loc[0, "mc"] == 2.5 and df.loc[0, "z"] == 0
    assert df.loc[0, "se"] == pytest.approx(np.std([1, 2, 3, 4], ddof=1) / 2)
    # antithetic pairs are (k, k + N/2): pair means 2 and 3, SE 0.5
    df = check(np.array([1.0, 2.0, 3.0, 4.0]), 2.0, antithetic=True)
    assert (df.loc[0, "mc"], df.loc[0, "se"], df.loc[0, "z"]) == pytest.approx((2.5, 0.5, 1.0))
    # exact by construction: z is 0 on a match and infinite on a mismatch
    assert check(np.array([0.5, 0.25, -0.5, -0.25]), 0.0, antithetic=True).loc[0, "z"] == 0
    assert check(np.ones(4), 1.5, antithetic=True).loc[0, "z"] == -np.inf
    df = check(np.array([[1.0, 10.0], [3.0, 30.0]]), [2.0, 20.0], antithetic=False)
    assert df["mc"].tolist() == [2.0, 20.0] and df["z"].tolist() == [0.0, 0.0]


def test_summary_on_a_small_run(model, workbook):
    model.G2PP.input_file = str(workbook(params=dict(scen_size=200, step_size=120)))
    summary = model.Validation.summary()
    assert summary.columns.tolist() == ["checks", "max_abs_z", "limit", "ok", "at"]
    assert len(summary) == 7 and np.isfinite(summary["max_abs_z"]).all()
    assert summary.loc["martingale_test()", "checks"] == 121
    assert summary.loc["martingale_test()", "limit"] == pytest.approx(z_limit(121))


def test_all_cash_fund_is_exactly_a_martingale(model, workbook):
    model.G2PP.input_file = str(workbook(params=dict(fund_id="CASH", scen_size=200,
                                                     step_size=120)))
    df = model.Validation.fund_martingale_test()
    assert (df["z"] == 0).all()
    np.testing.assert_allclose(df["mc"], 1.0, rtol=1e-12)


def test_curve_fit_with_continuous_compounding(model, workbook):
    model.G2PP.input_file = str(workbook(params=dict(compounding="continuous",
                                                     scen_size=200, step_size=120)))
    df = model.Validation.curve_fit_test()
    assert df.index.tolist() == [float(k) for k in range(1, 11)]
    spot = pd.read_excel(INPUT, sheet_name="Curve")["EUR_BASE"].head(10)
    np.testing.assert_array_equal(df["theory"].to_numpy(), spot.to_numpy())
    assert_within_limit(df)


def test_zbp_closed_form_matches_put_call_parity(model):
    """ZBC - ZBP = P(0,S) - K P(0,T); ZBC from Brigo and Mercurio's call formula."""
    v, g = model.Validation, model.G2PP
    i, j, K = 120, 180, 0.85
    put = v.zbp_cf(i, j, K)
    p_T, p_S = g.mkt_zcb(i), g.mkt_zcb(j)
    a, b, s, e, r = g.a(), g.b(), g.sigma(), g.eta(), g.rho()
    T, S = i / 12, j / 12
    var = (s**2 / (2 * a**3) * (1 - np.exp(-a * (S - T)))**2 * (1 - np.exp(-2 * a * T))
           + e**2 / (2 * b**3) * (1 - np.exp(-b * (S - T)))**2 * (1 - np.exp(-2 * b * T))
           + 2 * r * s * e / (a * b * (a + b)) * (1 - np.exp(-a * (S - T)))
           * (1 - np.exp(-b * (S - T))) * (1 - np.exp(-(a + b) * T)))
    vol = np.sqrt(var)
    h = np.log(p_S / (K * p_T)) / vol + vol / 2
    call = p_S * stats.norm.cdf(h) - K * p_T * stats.norm.cdf(h - vol)
    assert call - put == pytest.approx(p_S - K * p_T, rel=1e-12)


# ---- statistical tests: 10,000 antithetic scenarios over 50 years ------------------

@pytest.fixture(scope="module")
def v10k(tmp_path_factory):
    path = write_workbook(tmp_path_factory.mktemp("v10k") / "input.xlsx",
                          params=dict(scen_size=10_000))
    model = read_model_on(path)
    yield model.Validation
    model.close()


@pytest.mark.slow
@pytest.mark.parametrize("name", ["martingale_test", "fund_martingale_test",
                                  "curve_fit_test", "moments_test"])
def test_statistics_over_all_months(v10k, name):
    assert_within_limit(getattr(v10k, name)())


@pytest.mark.slow
@pytest.mark.parametrize("i, j", [(12, 120), (60, 180), (120, 360), (300, 600)])
def test_deflated_bond_prices(v10k, i, j):
    assert_within_limit(v10k.zcb_martingale_test(i, j))


@pytest.mark.slow
@pytest.mark.parametrize("moneyness", [0.98, 1.0, 1.02])
def test_bond_put(v10k, moneyness):
    g = v10k.g2pp
    strike = moneyness * g.mkt_zcb(180) / g.mkt_zcb(120)
    assert_within_limit(v10k.zbp_mc(120, 180, strike))


@pytest.mark.slow
@pytest.mark.parametrize("i, k", [(120, 0.8), (120, 0.9), (120, 1.0), (600, 0.9)])
def test_deflator_call(v10k, i, k):
    assert_within_limit(v10k.deflator_call_test(i, k))


@pytest.mark.slow
def test_summary_passes(v10k):
    summary = v10k.summary()
    assert summary["ok"].all(), summary.to_string()


@pytest.mark.slow
def test_single_maturity_fund_is_a_martingale(tmp_path):
    model = read_model_on(write_workbook(tmp_path / "input.xlsx",
                                         params=dict(scen_size=10_000, fund_id="BOND_10Y")))
    try:
        assert_within_limit(model.Validation.fund_martingale_test())
    finally:
        model.close()


# ---- statistical tests: 2,000 scenarios over 150 years -----------------------------

@pytest.mark.slow
def test_150_years(tmp_path):
    model = read_model_on(write_workbook(tmp_path / "input.xlsx",
                                         params=dict(scen_size=2_000, step_size=1_800)))
    try:
        v = model.Validation
        for name in ("martingale_test", "fund_martingale_test", "curve_fit_test"):
            df = getattr(v, name)()
            assert_within_limit(df)
        assert len(v.martingale_test()) == 1_801 and len(v.curve_fit_test()) == 150
    finally:
        model.close()
