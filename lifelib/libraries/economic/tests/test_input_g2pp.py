"""g2pp_input.xlsx reads into pandas as specified.

The specification is section 5 of the design note, ``_research/g2pp_design.md``.
"""
import numpy as np
import pandas as pd

from g2pp_registry import INPUT, sibling_library_path

PARAM_TYPES = {
    "a": float, "b": float, "sigma": float, "eta": float, "rho": float,
    "scen_size": int, "step_size": int, "seed": int, "antithetic": bool,
    "curve_id": str, "compounding": str, "fund_id": str,
}
CURVE_IDS = [f"{ccy}_{scen}" for ccy in ("EUR", "GBP", "JPY", "USD")
             for scen in ("BASE", "UP", "DOWN")]


def test_sheets():
    assert {"Params", "Curve", "Fund"} <= set(pd.ExcelFile(INPUT).sheet_names)


def test_params_have_expected_types():
    values = pd.read_excel(INPUT, sheet_name="Params", index_col="parameter")["value"]
    assert set(values.index) == set(PARAM_TYPES)
    for name, typ in PARAM_TYPES.items():
        assert type(values[name]) is typ, name


def test_curve_layout():
    curve = pd.read_excel(INPUT, sheet_name="Curve", index_col="maturity")
    assert curve.index.tolist() == list(range(1, 151))
    assert curve.columns.tolist() == CURVE_IDS
    assert not curve.isna().any().any()
    assert ((curve > -0.05) & (curve < 0.2)).all().all()


def test_curve_matches_appliedlife_source():
    source = sibling_library_path("appliedlife", "economic_data", "risk_free_202312.xlsx")
    curve = pd.read_excel(INPUT, sheet_name="Curve", index_col="maturity")
    for scen in ("BASE", "UP", "DOWN"):
        src = pd.read_excel(source, sheet_name=scen, index_col=0)
        for ccy in src.columns:
            np.testing.assert_array_equal(curve[f"{ccy}_{scen}"].to_numpy(),
                                          src[ccy].to_numpy())


def test_funds():
    fund = pd.read_excel(INPUT, sheet_name="Fund", index_col="maturity")
    assert fund.index.tolist() == ["cash", 5, 10]
    assert fund.columns.tolist() == ["CASH", "BOND_MIX", "BOND_10Y"]
    shares = fund.fillna(0.0)
    assert (shares >= 0).all().all()
    np.testing.assert_allclose(shares.sum().to_numpy(), 1.0, rtol=0, atol=1e-12)
