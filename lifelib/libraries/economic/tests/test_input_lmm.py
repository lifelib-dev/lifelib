"""lmm_input.xlsx reads into pandas as specified.

The specification is section 5 of the design note, ``_research/lmm_design.md``.
"""
import numpy as np
import pandas as pd

from lmm_registry import G2PP_INPUT, INPUT

PARAM_TYPES = {
    "shift": float, "tenor_mth": int, "maturity_size": int, "scen_size": int,
    "step_size": int, "seed": int, "antithetic": bool, "curve_id": str,
    "compounding": str, "fund_id": str,
}
# The example volatility table: two exponential factors with correlation RHO, written as
# two independent ones, f1 = S1 exp(-K1 u) + RHO S2 exp(-K2 u) and
# f2 = sqrt(1 - RHO^2) S2 exp(-K2 u), at time to expiry u in years
S1, K1, S2, K2, RHO = 0.30, 0.8, 0.20, 0.08, -0.7


def read_params():
    return pd.read_excel(INPUT, sheet_name="Params", index_col="parameter")["value"]


def test_sheets():
    assert {"Params", "Curve", "Vol", "Fund"} <= set(pd.ExcelFile(INPUT).sheet_names)


def test_params_have_expected_types():
    values = read_params()
    assert set(values.index) == set(PARAM_TYPES)
    for name, typ in PARAM_TYPES.items():
        assert type(values[name]) is typ, name


def test_curve_and_fund_are_those_of_g2pp_input():
    for sheet in ("Curve", "Fund"):
        pd.testing.assert_frame_equal(pd.read_excel(INPUT, sheet_name=sheet),
                                      pd.read_excel(G2PP_INPUT, sheet_name=sheet), obj=sheet)


def test_vol_table_is_the_example_rounded_to_six_decimals():
    vol = pd.read_excel(INPUT, sheet_name="Vol", index_col="maturity")
    assert vol.columns.tolist() == ["f1", "f2"]
    u = vol.index.to_numpy(dtype=float)
    assert len(u) == 25 and u[0] == 0 and u[-1] == 150 and (np.diff(u) > 0).all()
    f1 = S1 * np.exp(-K1 * u) + RHO * S2 * np.exp(-K2 * u)
    f2 = np.sqrt(1 - RHO**2) * S2 * np.exp(-K2 * u)
    assert vol["f1"].tolist() == [round(float(v), 6) for v in f1]
    assert vol["f2"].tolist() == [round(float(v), 6) for v in f2]


def test_example_run_needs_no_extrapolation_from_any_curve():
    p = read_params()
    tenor, shift = p["tenor_mth"], p["shift"]
    assert tenor in (1, 2, 3, 4, 6, 12) and 0 <= shift < 12 / tenor
    assert p["maturity_size"] >= tenor
    rates = -(-(p["step_size"] + p["maturity_size"]) // tenor)     # number of forward rates
    curve = pd.read_excel(INPUT, sheet_name="Curve", index_col="maturity")
    assert curve[p["curve_id"]].dropna().index[-1] >= rates * tenor / 12
    vol = pd.read_excel(INPUT, sheet_name="Vol", index_col="maturity")
    assert vol.index[-1] >= ((rates - 1) * tenor - 0.5) / 12      # the last rate's expiry
    fund = pd.read_excel(INPUT, sheet_name="Fund", index_col="maturity")[p["fund_id"]]
    bonds = [years for years, share in fund.fillna(0.0).items() if years != "cash" and share > 0]
    assert 12 * max(bonds, default=0) <= p["maturity_size"]
    # Instantaneous forward rates above -shift keep the forward rates of any tenor above
    # -shift too, since (exp(f tau) - 1) / tau >= f. So every curve can start the model.
    years = curve.index.to_numpy(dtype=float)
    spot = curve.to_numpy()
    lnp = -years[:, None] * (np.log1p(spot) if p["compounding"] == "annual" else spot)
    inst_fwd = -np.diff(np.vstack([np.zeros(len(curve.columns)), lnp]), axis=0)
    inst_fwd /= np.diff(np.concatenate([[0.0], years]))[:, None]
    assert (inst_fwd > -shift).all()


def test_write_workbook_keeps_the_types_of_values(lmm_workbook):
    vol = pd.read_excel(INPUT, sheet_name="Vol").head(5)
    path = lmm_workbook(params=dict(tenor_mth=3, shift=0.01, antithetic=False),
                        drop_params=["seed"], vol=vol)
    values = pd.read_excel(path, sheet_name="Params", index_col="parameter")["value"]
    assert "seed" not in values.index
    for name, value in dict(tenor_mth=3, shift=0.01, antithetic=False).items():
        assert values[name] == value and type(values[name]) is type(value), name
    pd.testing.assert_frame_equal(pd.read_excel(path, sheet_name="Vol"), vol)
    for sheet in ("Curve", "Fund", "Notes"):
        pd.testing.assert_frame_equal(pd.read_excel(path, sheet_name=sheet),
                                      pd.read_excel(INPUT, sheet_name=sheet), obj=sheet)
