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


@pytest.mark.parametrize("model_name", [
    "CashValue_ME",
    "CashValue_ME_EX1",
    "CashValue_ME_EX2",
    "CashValue_ME_EX4",
    "CashValue_SE",
])
def test_cashvalue_model_point_table_index_name(model_name):
    model_path = HERE.parents[2] / "libraries" / "savings" / model_name
    model = modelx.read_model(model_path)
    try:
        assert model.Projection.model_point_table.index.name == "point_id"
    finally:
        model.close()

