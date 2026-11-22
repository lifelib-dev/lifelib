import pathlib
import pytest
import numpy as np

modelx = pytest.importorskip("modelx")
scipy = pytest.importorskip("scipy")

HERE = pathlib.Path(__file__).resolve()
EX4_PATH = HERE.parents[2] / "libraries" / "savings" / "CashValue_ME_EX4"


def test_cashvalue_me_ex4_formula_option_put():
    model = modelx.read_model(EX4_PATH)
    try:
        res = model.Projection.formula_option_put(120)
        expected = np.array([
            27116.49437741,
            104840.91429683,
            2044594.24701365,
            3793289.6639734,
            10936999.8977298,
        ])
        np.testing.assert_allclose(res, expected, rtol=1e-5)
    finally:
        model.close()


@pytest.mark.parametrize("model_dir, table", [
    # model_point_table is an alias of one of these tables, so each table
    # read from a file is checked, not only the alias.
    ("savings/CashValue_ME", "model_point_samples"),
    ("savings/CashValue_ME_EX1", "model_point_1"),
    ("savings/CashValue_ME_EX1", "model_point_moneyness"),
    ("savings/CashValue_ME_EX2", "model_point_1"),
    ("savings/CashValue_ME_EX2", "model_point_moneyness"),
    ("savings/CashValue_ME_EX4", "model_point_1"),
    ("savings/CashValue_ME_EX4", "model_point_moneyness"),
    ("savings/CashValue_SE", "model_point_samples"),
    # Copied from CashValue_ME_EX4 before the poind_id fix.
    pytest.param(
        "economic/CashValue_ME_G2PP", "model_point_1",
        marks=pytest.mark.xfail(
            strict=True,
            reason="index still named poind_id: "
                   "https://github.com/lifelib-dev/lifelib-products/issues/48",
        ),
    ),
    ("economic/CashValue_ME_G2PP", "model_point_moneyness"),
])
def test_cashvalue_model_point_index_name(model_dir, table):
    model_path = HERE.parents[2] / "libraries" / model_dir
    model = modelx.read_model(model_path)
    try:
        assert getattr(model.Projection, table).index.name == "point_id"
        assert model.Projection.model_point_table.index.name == "point_id"
    finally:
        model.close()

