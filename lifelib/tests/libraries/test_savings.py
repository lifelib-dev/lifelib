import pathlib
import pytest
import numpy as np

modelx = pytest.importorskip("modelx")

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
