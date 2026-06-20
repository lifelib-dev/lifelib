"""Tests for ``risk_life`` in the ``TradLife_A_EX1`` Solvency II model.

``Projection.risk_life(t, risk)`` is the life underwriting capital
requirement for each life sub-risk: the baseline less the stressed
present value of ``pv_net_cf`` taken from the inner projection
``InnerProj``, floored at zero, with the lapse risk taking the worst of
the up/down/mass shocks. This mirrors ``SCR_life.Life`` / ``LapseRisk``
in the ``solvency2`` library.

Because ``TradLife_A_EX1`` reads ``input.xlsx`` from its parent directory
(``_model.path.parent / input_file_name``), we copy both the model and
the workbook into a temporary directory so the model loads from a
self-contained location during the tests.
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
TRADLIFE_A_EX1_MODEL = LIBRARIES / "annuallife" / "TradLife_A_EX1"
TRADLIFE_A_EX1_INPUT = LIBRARIES / "annuallife" / "input.xlsx"

IDXS = [0, 100, 200]

# Life sub-risks for which InnerProj applies a stress.
SHOCKED_RISKS = ["MORT", "LONGV", "EXPS"]
# Life sub-risks not modelled by InnerProj (no stress -> zero requirement).
UNSHOCKED_RISKS = ["DISAB", "REV", "CAT"]


@pytest.fixture(scope="module")
def ex1_model():
    # tempfile.mkdtemp() + shutil.rmtree(ignore_errors=True) is the
    # version-agnostic equivalent of
    # TemporaryDirectory(ignore_cleanup_errors=...), which is only
    # available on Python 3.10+. ignore_errors tolerates lingering file
    # handles on Windows.
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        shutil.copytree(TRADLIFE_A_EX1_MODEL, tmp / "TradLife_A_EX1")
        shutil.copy(TRADLIFE_A_EX1_INPUT, tmp / "input.xlsx")
        model = modelx.read_model(tmp / "TradLife_A_EX1")
        try:
            yield model
        finally:
            model.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@pytest.mark.parametrize("idx", IDXS)
@pytest.mark.parametrize("risk_name", SHOCKED_RISKS + UNSHOCKED_RISKS + ["LAPSE"])
def test_risk_life_is_nonnegative(ex1_model, idx, risk_name):
    """The max(., 0) floor makes every requirement non-negative."""
    proj = ex1_model.Projection[idx]
    risk = getattr(ex1_model.Enums.LifeRiskID, risk_name)
    assert proj.risk_life(0, risk) >= 0


@pytest.mark.parametrize("idx", IDXS)
@pytest.mark.parametrize("risk_name", SHOCKED_RISKS)
def test_risk_life_equals_floored_difference(ex1_model, idx, risk_name):
    """For a non-lapse risk: max(baseline_pv - stressed_pv, 0)."""
    proj = ex1_model.Projection[idx]
    risk = getattr(ex1_model.Enums.LifeRiskID, risk_name)
    base_pv = proj.InnerProj[0].pv_net_cf(0)
    stressed_pv = proj.InnerProj[0, risk].pv_net_cf(0)
    expected = max(base_pv - stressed_pv, 0)
    assert math.isclose(
        proj.risk_life(0, risk), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
@pytest.mark.parametrize("risk_name", UNSHOCKED_RISKS)
def test_risk_life_zero_for_unshocked_risks(ex1_model, idx, risk_name):
    """Risks InnerProj does not model leave pv_net_cf unchanged -> 0."""
    proj = ex1_model.Projection[idx]
    risk = getattr(ex1_model.Enums.LifeRiskID, risk_name)
    assert proj.risk_life(0, risk) == 0


@pytest.mark.parametrize("idx", IDXS)
def test_risk_life_lapse_is_worst_shock(ex1_model, idx):
    """The lapse requirement is the worst loss over up/down/mass shocks."""
    proj = ex1_model.Projection[idx]
    risk = ex1_model.Enums.LifeRiskID.LAPSE
    shock = ex1_model.Enums.LapseShockID
    base_pv = proj.InnerProj[0].pv_net_cf(0)
    expected = max(
        max(base_pv - proj.InnerProj[0, risk, s].pv_net_cf(0), 0)
        for s in (shock.UP, shock.DOWN, shock.MASS))
    assert math.isclose(
        proj.risk_life(0, risk), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
def test_risk_life_base_is_zero(ex1_model, idx):
    """The unstressed baseline has no capital requirement."""
    proj = ex1_model.Projection[idx]
    assert proj.risk_life(0, ex1_model.Enums.LifeRiskID.BASE) == 0
