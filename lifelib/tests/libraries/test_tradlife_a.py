"""Compare TradLife_A and simplelife/model on PV of net cashflow at t=0.

The two models should produce the same projection results for a given
model point, despite the cell-name refactor between them. We verify
this for three policies.

Because TradLife_A reads ``input.xlsx`` from its parent directory
(``_model.path.parent / input_file_name``), we copy both the model and
the workbook into a temporary directory so the model loads from a
self-contained location during the test.
"""
import math
import pathlib
import shutil
import tempfile
import tokenize

import pytest

modelx = pytest.importorskip("modelx")

# modelx 0.28+ tightened DocstringParser to require the docstring at
# line 1, but lifelib's serialized models prefix it with a four-line
# "# modelx: pseudo-python" comment header. Relax the check so the
# model files load.
try:
    from modelx.serialize import serializer_6 as _s6

    @classmethod
    def _docstring_condition(cls, stmt):
        return (
            stmt.section == "DEFAULT"
            and len(stmt) == 1
            and stmt[0].type == tokenize.STRING
        )

    _s6.DocstringParser.condition = _docstring_condition
except (ImportError, AttributeError):
    pass


HERE = pathlib.Path(__file__).resolve()
LIBRARIES = HERE.parents[2] / "libraries"
SIMPLELIFE_MODEL = LIBRARIES / "simplelife" / "model"
TRADLIFE_A_MODEL = LIBRARIES / "annuallife" / "TradLife_A"
TRADLIFE_A_INPUT = LIBRARIES / "annuallife" / "input.xlsx"

# (PolicyID for simplelife, idx for TradLife_A)
POLICY_PAIRS = [(1, 0), (101, 100), (201, 200)]


@pytest.mark.parametrize("policy_id, idx", POLICY_PAIRS)
def test_pv_net_cf_matches_simplelife(policy_id, idx):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        shutil.copytree(TRADLIFE_A_MODEL, tmp / "TradLife_A")
        shutil.copy(TRADLIFE_A_INPUT, tmp / "input.xlsx")

        simplelife_model = modelx.read_model(SIMPLELIFE_MODEL)
        tradlife_model = modelx.read_model(tmp / "TradLife_A")
        try:
            expected = simplelife_model.Projection[policy_id].PV_NetCashflow(0)
            actual = tradlife_model.Projection[idx].pv_net_cf(0)
        finally:
            simplelife_model.close()
            tradlife_model.close()

        assert math.isclose(actual, expected, rel_tol=1e-9), (
            f"PolicyID={policy_id}, idx={idx}: "
            f"TradLife_A.pv_net_cf(0)={actual!r}, "
            f"simplelife.PV_NetCashflow(0)={expected!r}"
        )
