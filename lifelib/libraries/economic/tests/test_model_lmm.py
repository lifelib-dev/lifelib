"""BasicLMM against the numpy reference, its identities, input checks and the round trip."""
import ast
import re
import shutil
import textwrap
import uuid
from pathlib import Path

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from lmm_registry import INPUT, write_workbook
from reference_lmm import ReferenceLMM, read_inputs

RTOL, ATOL = 1e-10, 1e-15
CURVE = pd.read_excel(INPUT, sheet_name="Curve")
VOL = pd.read_excel(INPUT, sheet_name="Vol")

# Cells whose code is that of the same cells of BasicG2PP's G2PP space
SHARED_WITH_G2PP = [
    "input_path", "curve_table", "fund_table", "scen_size", "step_size", "seed", "antithetic",
    "curve_id", "compounding", "fund_id", "mkt_zcb", "fund_cash_share", "fund_bond_shares",
    "fund_return_mth", "bank_return_mth", "spot_rate", "swap_rate", "ce_disc_factor",
    "ce_bank_return_mth", "ce_spot_rate", "scen_index", "disc_factor_paths",
    "bank_return_paths", "fund_return_paths", "spot_rate_paths",
]


def use(model, path):
    """Point the model at another input workbook, given as an absolute path."""
    model.LMM.input_file = str(path)
    return model.LMM


def raises(message):
    """modelx wraps errors raised in formulas in FormulaError, keeping the message."""
    return pytest.raises(FormulaError, match=re.escape(message))


def three_factors():
    """The example volatility table with a third factor."""
    return VOL.assign(f3=(0.05 * np.exp(-0.3 * VOL["maturity"])).round(6))


# ---- the model equals the reference ------------------------------------------------

SECOND_INPUT = dict(shift=0.01, tenor_mth=3, maturity_size=120, antithetic=False,
                    scen_size=301, step_size=240, curve_id="USD_UP", compounding="continuous",
                    fund_id="BOND_10Y", seed=99)


@pytest.mark.parametrize("delivered", [True, False], ids=["delivered", "second input"])
def test_outputs_equal_reference(lmm_model, lmm_workbook, delivered):
    path = INPUT if delivered else lmm_workbook(params=SECOND_INPUT, vol=three_factors())
    g = use(lmm_model, path)
    ref = ReferenceLMM(**read_inputs(path), keep=(120,), snapshots=(24, 60))
    for name in ("disc_factor_paths", "bank_return_paths", "fund_return_paths",
                 "libor_rate_paths"):
        np.testing.assert_allclose(getattr(g, name)(), getattr(ref, name)(),
                                   rtol=RTOL, atol=ATOL, err_msg=name)
    np.testing.assert_allclose(g.spot_rate_paths(120), ref.spot_rate_paths(120),
                               rtol=RTOL, atol=ATOL)
    np.testing.assert_allclose(g.mkt_fwd_rates(), ref.F0, rtol=RTOL)
    np.testing.assert_allclose(g.vol_loadings(), ref.lam, rtol=RTOL, atol=0)
    np.testing.assert_allclose(g.P_t_T(60, 240), ref.P(60, 240), rtol=RTOL)
    np.testing.assert_allclose(g.swap_rate(24, 10), ref.swap_rate(24, 10), rtol=RTOL)
    for k in (2, 5, 20):
        expiry = (k - 1) * ref.tau
        assert g.caplet_vol(k) == pytest.approx(ref.caplet_total_vol(k) / np.sqrt(expiry),
                                                rel=RTOL)


# ---- types, shapes and identities ---------------------------------------------------

def test_types_and_shapes(lmm_model):
    g = lmm_model.LMM
    N, n, K, d = g.scen_size(), g.step_size(), g.tenor_size(), g.factor_size()
    assert (N, n, K, d) == (1000, 600, 60, 2)
    assert isinstance(g.input_path(), Path) and g.input_path().resolve() == INPUT.resolve()
    assert isinstance(g.param_table(), pd.Series) and g.param_table().dtype == object
    for name, typ in [("shift", float), ("tenor_mth", int), ("maturity_size", int),
                      ("scen_size", int), ("seed", int), ("antithetic", bool),
                      ("curve_id", str), ("fund_id", str), ("tenor_size", int),
                      ("factor_size", int)]:
        assert type(getattr(g, name)()) is typ, name
    assert g.vol_table().shape == (25, 2) and g.vol_table().index.name == "maturity"
    assert g.vol_loadings().shape == ((K - 1) * 12 + 1, d)
    assert g.mkt_fwd_rates().shape == (K,)
    for value in (g.mkt_zcb(12), g.curve_adj(18), g.caplet_vol(2)):
        assert isinstance(value, float)
    assert g.std_norm_rand().shape == (n, N, d)
    assert g.fwd_rates(0).shape == (N, K) and g.fwd_rates(13).shape == (N, K - 1)
    for name in ("disc_factor", "bank_return_mth", "libor_rate", "fund_return_mth"):
        assert getattr(g, name)(12).shape == (N,), name
    for value in (g.tenor_disc_factor(3), g.defl_tenor_zcb(13, 5), g.defl_zcb(13, 50)):
        assert value.shape == (N,)
    assert g.disc_factor_paths().shape == g.libor_rate_paths().shape == (N + 1, n + 1)
    assert g.bank_return_paths().shape == g.fund_return_paths().shape == (N + 1, n)
    index = g.scen_index()
    assert isinstance(index, pd.RangeIndex) and index.name == "scen_id" and len(index) == N + 1
    assert g.fund_cash_share() == 0.2
    assert g.fund_bond_shares().to_dict() == {60: 0.3, 120: 0.5}
    table = g.scenario_table()
    assert table.index.names == ["scen_id", "t"] and table.shape == ((N + 1) * (n + 1), 4)
    assert table.columns.tolist() == ["disc_factor", "bank_return_mth", "fund_return_mth",
                                      "libor_rate"]
    assert table.xs(n, level="t")[["bank_return_mth", "fund_return_mth"]].isna().all().all()


def test_ce_row_follows_the_initial_curve(lmm_model):
    g = lmm_model.LMM
    n, p = g.step_size(), g.tenor_mth()
    zcb = np.array([g.mkt_zcb(i) for i in range(n + p + 1)])
    assert np.array_equal(g.disc_factor_paths()[0], zcb[:n + 1])
    assert np.array_equal(g.bank_return_paths()[0], zcb[:n] / zcb[1:n + 1] - 1)
    assert np.array_equal(g.fund_return_paths()[0], g.bank_return_paths()[0])
    np.testing.assert_allclose(g.libor_rate_paths()[0], (zcb[:n + 1] / zcb[p:] - 1) / (p / 12),
                               rtol=1e-14)


@pytest.mark.parametrize("tenor", [12, 3])
def test_bonds_start_at_the_initial_curve(lmm_model, lmm_workbook, tenor):
    g = use(lmm_model, lmm_workbook(params=dict(tenor_mth=tenor, scen_size=10, step_size=60)))
    months = range(g.tenor_size() * tenor + 1)
    np.testing.assert_allclose([g.defl_zcb(0, j)[0] for j in months],
                               [g.mkt_zcb(j) for j in months], rtol=1e-14)
    assert all(g.curve_adj(j) == 1 for j in months[::tenor])


def test_bank_return_is_known_at_the_start_of_each_month(lmm_model):
    """The deflated price of a bond does not change in its last month."""
    g = lmm_model.LMM
    for i in (0, 11, 12, 299):
        assert np.array_equal(g.defl_zcb(i, i + 1), g.disc_factor(i + 1))
        np.testing.assert_allclose(g.bank_return_mth(i), 1 / g.P_t_T(i, i + 1) - 1,
                                   rtol=0, atol=1e-15)


def test_libor_rate_on_a_tenor_date_is_the_rate_just_set(lmm_model):
    g = lmm_model.LMM
    for i in (0, 12, 360):
        np.testing.assert_allclose(g.libor_rate(i), g.fwd_rates(i)[:, 0], rtol=1e-12)


@pytest.mark.parametrize("i", [0, 11, 12, 599])
def test_bond_returns_equal_ratio_of_bond_prices(lmm_model, i):
    g = lmm_model.LMM
    full = g.P_t_T(i + 1, i + 120) / g.P_t_T(i, i + 120) - 1
    np.testing.assert_allclose(g.zcb_return_mth(i, 120), full, rtol=0, atol=1e-14)


def test_all_cash_fund_earns_the_bank_return(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(params=dict(fund_id="CASH", scen_size=200, step_size=120)))
    assert np.array_equal(g.fund_return_paths(), g.bank_return_paths())


def test_zero_volatility_gives_the_ce_scenario(lmm_model, lmm_workbook):
    vol = VOL.assign(f1=0.0, f2=0.0)
    g = use(lmm_model, lmm_workbook(vol=vol, params=dict(scen_size=10, step_size=120)))
    for paths in (g.disc_factor_paths(), g.bank_return_paths(), g.fund_return_paths(),
                  g.libor_rate_paths(), g.spot_rate_paths(120)):
        np.testing.assert_allclose(paths[1:], np.broadcast_to(paths[0], paths[1:].shape),
                                   rtol=1e-12, atol=1e-15)


def test_rates_stay_above_minus_the_shift(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(params=dict(curve_id="JPY_DOWN", scen_size=200,
                                                step_size=240)))
    assert all((g.fwd_rates(i) > -g.shift()).all() for i in range(241))


def test_reproducible_after_clear_all(lmm_model):
    g = lmm_model.LMM
    before = g.fund_return_paths()
    lmm_model.clear_all()
    assert np.array_equal(g.fund_return_paths(), before)


@pytest.mark.parametrize("longer", [dict(step_size=240), dict(maturity_size=240)])
def test_extending_the_run_keeps_earlier_months(lmm_model, lmm_workbook, longer):
    """Equal up to rounding: the matrix products of longer arrays can round differently."""
    base = dict(step_size=120, scen_size=200)
    g = use(lmm_model, lmm_workbook(params=base))
    short_d, short_f = g.disc_factor_paths(), g.fund_return_paths()
    g = use(lmm_model, lmm_workbook(params={**base, **longer}))
    np.testing.assert_allclose(g.disc_factor_paths()[:, :121], short_d, rtol=1e-12)
    np.testing.assert_allclose(g.fund_return_paths()[:, :120], short_f, rtol=1e-12, atol=1e-15)


def test_antithetic_random_numbers(lmm_model):
    g = lmm_model.LMM
    z, half = g.std_norm_rand(), g.scen_size() // 2
    assert np.array_equal(z[:, :half], -z[:, half:])


def test_input_edited_in_place_needs_clear_all(lmm_model, tmp_path):
    path = write_workbook(tmp_path / "input.xlsx")
    g = use(lmm_model, path)
    assert g.shift() == 0.02
    write_workbook(path, params=dict(shift=0.03))
    assert g.shift() == 0.02                  # still cached
    lmm_model.clear_all()
    assert g.shift() == 0.03


# ---- input checks ------------------------------------------------------------------

@pytest.mark.parametrize("params, message", [
    (dict(shift=-0.01), "shift must be >= 0 and below 12/tenor_mth"),
    (dict(shift=1.0), "shift must be >= 0 and below 12/tenor_mth"),
    (dict(tenor_mth=5), "tenor_mth must be 1, 2, 3, 4, 6 or 12"),
    (dict(maturity_size=6), "maturity_size must be >= tenor_mth"),
    (dict(scen_size=999), "scen_size must be even when antithetic is TRUE"),
    (dict(step_size=0), "step_size must be >= 1"),
    (dict(seed=1.5), "seed must be a whole number"),
    (dict(antithetic="maybe"), "antithetic must be TRUE or FALSE"),
    (dict(compounding="semiannual"), "compounding must be annual or continuous"),
    (dict(shift="high"), "shift must be a number"),
])
def test_invalid_params(lmm_model, lmm_workbook, params, message):
    g = use(lmm_model, lmm_workbook(params=params))
    with raises(message):
        g.param_table()


def test_missing_param(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(drop_params=["tenor_mth"]))
    with raises("tenor_mth is missing"):
        g.param_table()


def test_curve_shorter_than_the_last_tenor_date(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(curve=CURVE.head(55)))
    with raises("ends at 55 years, before the last tenor date of 60 years"):
        g.curve_knots()


def test_unknown_curve_id(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(params=dict(curve_id="EUR_SIDEWAYS")))
    with raises("curve_id 'EUR_SIDEWAYS' is not a column of the Curve sheet"):
        g.curve_knots()


def test_forward_rate_not_above_minus_the_shift(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(curve=CURVE.assign(EUR_BASE=-0.03)))
    with raises("is not above -shift (-0.02)"):
        g.mkt_fwd_rates()


@pytest.mark.parametrize("change, message", [
    (lambda v: v.assign(maturity=-v["maturity"]), "maturities must be numbers of years"),
    (lambda v: v.iloc[::-1], "maturities must be increasing"),
    (lambda v: v.assign(f2=v["f2"].where(v.index != 3)), "a volatility is blank"),
    (lambda v: v[["maturity"]], "there is no factor column"),
])
def test_invalid_vol_tables(lmm_model, lmm_workbook, change, message):
    g = use(lmm_model, lmm_workbook(vol=change(VOL.copy())))
    with raises(message):
        g.vol_table()


def test_vol_table_shorter_than_the_longest_expiry(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(vol=VOL[VOL["maturity"] <= 50]))
    with raises("the Vol sheet ends at 50 years, before the longest time to expiry"):
        g.vol_loadings()


def test_bond_past_the_last_tenor_date(lmm_model):
    with raises("raise maturity_size (now 120 months)"):
        lmm_model.LMM.defl_zcb(600, 721)


def test_fund_maturity_past_maturity_size(lmm_model, lmm_workbook):
    g = use(lmm_model, lmm_workbook(params=dict(fund_id="BOND_10Y", maturity_size=60,
                                                scen_size=10)))
    with raises("raise maturity_size (now 60 months)"):
        g.fund_return_paths()


# ---- cells shared with BasicG2PP, and the round trip -----------------------------------

def code_of(cells):
    """The formula's code without its docstring, as an AST dump."""
    func = ast.parse(textwrap.dedent(cells.formula.source)).body[0]
    if ast.get_docstring(func) is not None:
        func.body = func.body[1:]
    return ast.dump(func)


def test_shared_cells_have_the_code_of_g2pp(lmm_model, model):
    for name in SHARED_WITH_G2PP:
        assert code_of(lmm_model.LMM.cells[name]) == code_of(model.G2PP.cells[name]), name


def test_read_write_read_round_trip(lmm_model, tmp_path):
    g = lmm_model.LMM
    before = g.fund_return_paths()
    shutil.copy(INPUT, tmp_path / INPUT.name)
    mx.write_model(lmm_model, tmp_path / "BasicLMM", backup=False)
    copy = mx.read_model(tmp_path / "BasicLMM", name=f"copy_{uuid.uuid4().hex[:8]}")
    try:
        c = copy.LMM
        assert sorted(c.cells) == sorted(g.cells)
        for name in g.cells:
            assert c.cells[name].formula.source == g.cells[name].formula.source, name
        assert c.doc == g.doc and copy.doc == lmm_model.doc
        assert c.input_path() == tmp_path / INPUT.name
        assert np.array_equal(c.fund_return_paths(), before)
    finally:
        copy.close()
