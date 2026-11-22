"""BasicG2PP against the numpy reference, input checks and the round trip."""
import re
import shutil
import uuid
from pathlib import Path

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from g2pp_registry import INPUT, ROOT, write_workbook
from reference_g2pp import ReferenceG2PP, read_inputs

RTOL, ATOL = 1e-12, 1e-15
FUNDS = pd.read_excel(INPUT, sheet_name="Fund")


def use(model, path):
    """Point the model at another input workbook, given as an absolute path."""
    model.G2PP.input_file = str(path)
    return model.G2PP


def raises(message):
    """modelx wraps errors raised in formulas in FormulaError, keeping the message."""
    return pytest.raises(FormulaError, match=re.escape(message))


# ---- the model equals the reference ------------------------------------------------

@pytest.mark.parametrize("params", [
    None,                                     # the workbook as delivered: BOND_MIX, 600 months
    dict(antithetic=False, scen_size=301, step_size=240, curve_id="USD_UP",
         compounding="continuous", fund_id="BOND_10Y", seed=99),
])
def test_outputs_equal_reference(model, workbook, params):
    path = workbook(params=params) if params else INPUT
    g, ref = use(model, path), ReferenceG2PP(**read_inputs(path))
    n = g.step_size()
    for name in ("disc_factor_paths", "bank_return_paths", "fund_return_paths",
                 "short_rate_paths"):
        np.testing.assert_allclose(getattr(g, name)(), getattr(ref, name)(),
                                   rtol=RTOL, atol=ATOL, err_msg=name)
    np.testing.assert_allclose(g.spot_rate_paths(120), ref.spot_rate_paths(120),
                               rtol=RTOL, atol=ATOL)
    np.testing.assert_allclose(g.E_rt(), ref.phi(np.arange(n + 1)), rtol=RTOL, atol=ATOL)
    np.testing.assert_allclose(g.Var_rt(), ref.var_r(np.arange(n + 1)), rtol=RTOL, atol=ATOL)
    np.testing.assert_allclose(g.cov_step(), ref.cov_step(), rtol=RTOL, atol=0)
    np.testing.assert_allclose(g.P_t_T(60, 240), ref.P(60, 240), rtol=RTOL)
    np.testing.assert_allclose(g.swap_rate(24, 10), ref.swap_rate(24, 10), rtol=RTOL)


@pytest.mark.parametrize("fund_id, j", [("BOND_10Y", 120), ("BOND_10Y", 600), ("CASH", 120)])
def test_fund_logvar_equals_quadratic_form(model, workbook, fund_id, j):
    path = workbook(params=dict(fund_id=fund_id))
    g, ref = use(model, path), ReferenceG2PP(**read_inputs(path))
    assert g.fund_logvar(j) == pytest.approx(ref.fund_logvar(j), rel=RTOL)
    if fund_id == "CASH":
        assert g.fund_logvar(j) == g.V_t_T(0, j)


def test_fund_logvar_rejects_mixed_funds(model):
    with raises("needs an all-cash or single-maturity fund"):
        model.G2PP.fund_logvar(120)


# ---- types, shapes and identities ---------------------------------------------------

def test_types_and_shapes(model):
    g = model.G2PP
    N, n = g.scen_size(), g.step_size()
    assert (N, n) == (1000, 600)
    assert isinstance(g.input_path(), Path) and g.input_path().resolve() == INPUT.resolve()
    assert isinstance(g.param_table(), pd.Series) and g.param_table().dtype == object
    for name, typ in [("a", float), ("rho", float), ("scen_size", int), ("seed", int),
                      ("antithetic", bool), ("curve_id", str), ("fund_id", str)]:
        assert type(getattr(g, name)()) is typ, name
    assert isinstance(g.curve_table(), pd.DataFrame) and g.curve_table().shape == (150, 12)
    knots_t, knots_lnp = g.curve_knots()
    assert knots_t[0] == knots_lnp[0] == 0 and len(knots_t) == len(knots_lnp) == 151
    assert isinstance(g.mkt_zcb(12), float) and isinstance(g.mkt_fwd(12), float)
    index = g.scen_index()
    assert isinstance(index, pd.RangeIndex) and index.name == "scen_id" and len(index) == N + 1
    assert g.std_norm_rand().shape == (n, N, 3)
    assert g.chol_step().shape == (3, 3) and g.shocks(0).shape == (N, 3)
    for name in ("x", "y", "accum_xy", "short_rate", "disc_factor", "bank_return_mth",
                 "fund_return_mth"):
        assert getattr(g, name)(12).shape == (N,), name
    assert g.disc_factor_paths().shape == g.short_rate_paths().shape == (N + 1, n + 1)
    assert g.bank_return_paths().shape == g.fund_return_paths().shape == (N + 1, n)
    assert g.fund_cash_share() == 0.2
    assert g.fund_bond_shares().to_dict() == {60: 0.3, 120: 0.5}
    table = g.scenario_table()
    assert table.index.names == ["scen_id", "t"] and table.shape == ((N + 1) * (n + 1), 4)
    assert table.xs(n, level="t")[["bank_return_mth", "fund_return_mth"]].isna().all().all()
    np.testing.assert_array_equal(table["disc_factor"].unstack().to_numpy(),
                                  g.disc_factor_paths())


def test_ce_row_follows_the_initial_curve(model):
    g = model.G2PP
    n = g.step_size()
    p = np.array([g.mkt_zcb(i) for i in range(n + 1)])
    assert np.array_equal(g.disc_factor_paths()[0], p)
    assert np.array_equal(g.bank_return_paths()[0], p[:-1] / p[1:] - 1)
    assert np.array_equal(g.fund_return_paths()[0], g.bank_return_paths()[0])


def test_all_cash_fund_earns_the_bank_return(model, workbook):
    g = use(model, workbook(params=dict(fund_id="CASH", scen_size=200, step_size=120)))
    assert np.array_equal(g.fund_return_paths(), g.bank_return_paths())


@pytest.mark.parametrize("i", [0, 1, 59, 599])
def test_bond_returns_equal_ratio_of_full_bond_prices(model, i):
    g = model.G2PP
    full = g.P_t_T(i + 1, i + 120) / g.P_t_T(i, i + 120) - 1
    np.testing.assert_allclose(g.zcb_return_mth(i, 120), full, rtol=0, atol=1e-13)


def test_reproducible_after_clear_all(model):
    g = model.G2PP
    before = g.fund_return_paths()
    model.clear_all()
    assert np.array_equal(g.fund_return_paths(), before)


def test_extending_step_size_keeps_earlier_months(model, workbook):
    g = use(model, workbook(params=dict(step_size=120, scen_size=200)))
    short_d, short_f = g.disc_factor_paths(), g.fund_return_paths()
    g = use(model, workbook(params=dict(step_size=240, scen_size=200)))
    assert np.array_equal(g.disc_factor_paths()[:, :121], short_d)
    assert np.array_equal(g.fund_return_paths()[:, :120], short_f)


def test_antithetic_pairs_are_exact_negatives(model):
    g = model.G2PP
    half = g.scen_size() // 2
    assert np.array_equal(g.x(60)[:half], -g.x(60)[half:])
    assert np.array_equal(g.y(60)[:half], -g.y(60)[half:])
    assert abs(g.x(60).mean()) < 1e-15


def test_bond_fund_needs_no_curve_beyond_the_horizon(model, workbook):
    g = use(model, workbook(params=dict(step_size=1800, scen_size=10, fund_id="BOND_10Y")))
    assert np.isfinite(g.fund_return_paths()).all()
    with raises("past the last maturity"):
        g.spot_rate(1740, 120)


def test_input_edited_in_place_needs_clear_all(model, tmp_path):
    path = write_workbook(tmp_path / "input.xlsx")
    g = use(model, path)
    assert g.a() == 0.773
    write_workbook(path, params=dict(a=0.5))
    assert g.a() == 0.773                     # still cached
    model.clear_all()
    assert g.a() == 0.5


# ---- input checks ------------------------------------------------------------------

@pytest.mark.parametrize("params, message", [
    (dict(a=0), "a must be > 0"),
    (dict(b=-0.1), "b must be > 0"),
    (dict(sigma=0), "sigma must be > 0"),
    (dict(eta=-0.01), "eta must be >= 0"),
    (dict(rho=1.5), "rho must be in [-1, 1]"),
    (dict(scen_size=999), "scen_size must be even when antithetic is TRUE"),
    (dict(step_size=0), "step_size must be >= 1"),
    (dict(seed=1.5), "seed must be a whole number"),
    (dict(antithetic="maybe"), "antithetic must be TRUE or FALSE"),
    (dict(compounding="semiannual"), "compounding must be annual or continuous"),
    (dict(a="fast"), "a must be a number"),
])
def test_invalid_params(model, workbook, params, message):
    g = use(model, workbook(params=params))
    with raises(message):
        g.param_table()


def test_missing_param(model, workbook):
    g = use(model, workbook(drop_params=["fund_id"]))
    with raises("fund_id is missing"):
        g.param_table()


def test_curve_shorter_than_the_horizon(model, workbook):
    curve = pd.read_excel(INPUT, sheet_name="Curve").head(40)
    g = use(model, workbook(curve=curve))
    with raises("ends at 40 years, before the projection horizon of 50 years"):
        g.curve_knots()


def test_blank_inside_a_curve(model, workbook):
    curve = pd.read_excel(INPUT, sheet_name="Curve")
    curve.loc[9, "EUR_BASE"] = np.nan
    g = use(model, workbook(curve=curve))
    with raises("curve EUR_BASE has a blank inside it"):
        g.curve_table()


def test_shorter_curve_ending_with_blanks_is_valid(model, workbook):
    curve = pd.read_excel(INPUT, sheet_name="Curve")
    curve.loc[100:, "GBP_BASE"] = np.nan      # GBP_BASE ends at 100 years
    g = use(model, workbook(curve=curve, params=dict(curve_id="GBP_BASE")))
    assert g.curve_knots()[0][-1] == 100
    with raises("past the last maturity"):
        g.mkt_zcb(1201)


def test_unknown_curve_id(model, workbook):
    g = use(model, workbook(params=dict(curve_id="EUR_SIDEWAYS")))
    with raises("curve_id 'EUR_SIDEWAYS' is not a column of the Curve sheet"):
        g.curve_knots()


@pytest.mark.parametrize("change, message", [
    (lambda f: f.assign(BOND_MIX=[-0.2, 0.7, 0.5]), "fund BOND_MIX has a negative share"),
    (lambda f: f.assign(BOND_MIX=[0.2, 0.3, 0.4]), "shares of fund BOND_MIX sum to 0.9"),
    (lambda f: f.assign(maturity=["cash", 0.1, 10]), "maturity 0.1 is neither cash nor"),
    (lambda f: f.assign(maturity=["cash", 10, 10]), "a maturity appears more than once"),
])
def test_invalid_funds(model, workbook, change, message):
    g = use(model, workbook(fund=change(FUNDS.copy())))
    with raises(message):
        g.fund_table()


def test_unknown_fund_id(model, workbook):
    g = use(model, workbook(params=dict(fund_id="EQUITY")))
    with raises("fund_id 'EQUITY' is not a column of the Fund sheet"):
        g.fund_bond_shares()


# ---- cross-check against BasicHullWhite, next to BasicG2PP in the library ----------

# BasicHullWhite's docstrings contain LaTeX escapes such as "\{" in non-raw strings,
# which Python reports as SyntaxWarning when modelx reads the model.
@pytest.mark.filterwarnings("ignore::SyntaxWarning")
def test_eta_zero_matches_basic_hull_white(model, workbook):
    hw = mx.read_model(ROOT / "BasicHullWhite",
                       name=f"BasicHullWhite_{uuid.uuid4().hex[:8]}")
    try:
        h = hw.HullWhite
        curve = pd.DataFrame({"maturity": np.arange(1, h.time_len + 1), "FLAT5": 0.05})
        g = use(model, workbook(curve=curve, params=dict(
            a=h.a, b=0.5, sigma=h.sigma, eta=0, rho=0, step_size=h.step_size,
            scen_size=100, curve_id="FLAT5", compounding="continuous")))
        np.testing.assert_allclose(g.E_rt(), h.E_rt(), rtol=1e-12)
        np.testing.assert_allclose(g.Var_rt(), h.Var_rt(), rtol=1e-12, atol=1e-18)
        # eta = 0 makes the step covariance singular, so the symmetric root is used
        with pytest.raises(np.linalg.LinAlgError):
            np.linalg.cholesky(g.cov_step())
        assert np.isfinite(g.disc_factor_paths()).all()
        assert np.abs(g.y(h.step_size)).max() < 1e-15
    finally:
        hw.close()


# ---- round trip ----------------------------------------------------------------------

def test_read_write_read_round_trip(model, tmp_path):
    g = model.G2PP
    before = g.fund_return_paths()
    shutil.copy(INPUT, tmp_path / INPUT.name)
    mx.write_model(model, tmp_path / "BasicG2PP", backup=False)
    copy = mx.read_model(tmp_path / "BasicG2PP", name=f"copy_{uuid.uuid4().hex[:8]}")
    try:
        c = copy.G2PP
        assert sorted(c.cells) == sorted(g.cells)
        for name in g.cells:
            assert c.cells[name].formula.source == g.cells[name].formula.source, name
        assert c.doc == g.doc and copy.doc == model.doc
        assert c.input_path() == tmp_path / INPUT.name
        assert np.array_equal(c.fund_return_paths(), before)
    finally:
        copy.close()
