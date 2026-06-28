"""Tests for ``risk_life_sub`` / ``risk_life`` in the ``TradLife_A_EX1`` model.

``Projection.risk_life_sub(t, risk)`` is the Solvency II life
underwriting capital requirement for each life sub-risk: the baseline
less the stressed present value of ``pv_net_cf`` taken from the inner
projection ``InnerProj``, floored at zero, with the lapse risk taking the
worst of the up/down/mass shocks (mirroring ``SCR_life.Life`` /
``LapseRisk`` in the ``solvency2`` library).

``Projection.risk_life(t)`` aggregates those sub-risk requirements with
the life-risk correlation matrix forwarded by ``Assumptions.life_corr``
(mirroring ``SCR_life.SCR_life``).

``Projection.risk_margin(t)`` is the Solvency II risk margin: the
cost-of-capital rate forwarded by ``Assumptions.coc_rate`` (read from the
``CoCRate`` row of ``ConstParams``) applied to the projected
``risk_life`` and discounted to ``t``.

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


# ---------------------------------------------------------------------------
# risk_life_sub: per-sub-risk capital requirement

@pytest.mark.parametrize("idx", IDXS)
@pytest.mark.parametrize("risk_name", SHOCKED_RISKS + UNSHOCKED_RISKS + ["LAPSE"])
def test_risk_life_sub_is_nonnegative(ex1_model, idx, risk_name):
    """The max(., 0) floor makes every requirement non-negative."""
    proj = ex1_model.Projection[idx]
    risk = getattr(ex1_model.Enums.LifeRiskID, risk_name)
    assert proj.risk_life_sub(0, risk) >= 0


@pytest.mark.parametrize("idx", IDXS)
@pytest.mark.parametrize("risk_name", SHOCKED_RISKS)
def test_risk_life_sub_equals_floored_difference(ex1_model, idx, risk_name):
    """For a non-lapse risk: max(baseline_pv - stressed_pv, 0)."""
    proj = ex1_model.Projection[idx]
    risk = getattr(ex1_model.Enums.LifeRiskID, risk_name)
    base_pv = proj.InnerProj[0].pv_net_cf(0)
    stressed_pv = proj.InnerProj[0, risk].pv_net_cf(0)
    expected = max(base_pv - stressed_pv, 0)
    assert math.isclose(
        proj.risk_life_sub(0, risk), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
@pytest.mark.parametrize("risk_name", UNSHOCKED_RISKS)
def test_risk_life_sub_zero_for_unshocked_risks(ex1_model, idx, risk_name):
    """Risks InnerProj does not model leave pv_net_cf unchanged -> 0."""
    proj = ex1_model.Projection[idx]
    risk = getattr(ex1_model.Enums.LifeRiskID, risk_name)
    assert proj.risk_life_sub(0, risk) == 0


@pytest.mark.parametrize("idx", IDXS)
def test_risk_life_sub_lapse_is_worst_shock(ex1_model, idx):
    """The lapse requirement is the worst loss over up/down/mass shocks."""
    proj = ex1_model.Projection[idx]
    risk = ex1_model.Enums.LifeRiskID.LAPSE
    shock = ex1_model.Enums.LapseShockID
    base_pv = proj.InnerProj[0].pv_net_cf(0)
    expected = max(
        max(base_pv - proj.InnerProj[0, risk, s].pv_net_cf(0), 0)
        for s in (shock.UP, shock.DOWN, shock.MASS))
    assert math.isclose(
        proj.risk_life_sub(0, risk), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
def test_risk_life_sub_base_is_zero(ex1_model, idx):
    """The unstressed baseline has no capital requirement."""
    proj = ex1_model.Projection[idx]
    assert proj.risk_life_sub(0, ex1_model.Enums.LifeRiskID.BASE) == 0


# ---------------------------------------------------------------------------
# life_corr: correlation forwarded from InputData by Assumptions

def test_life_corr_forwards_input_data(ex1_model):
    """Assumptions.life_corr returns each LifeCorr coefficient as a native float."""
    corr_df = ex1_model.InputData.life_corr_data()
    asmp = ex1_model.Assumptions
    for i in corr_df.index:
        for j in corr_df.columns:
            coef = asmp.life_corr(i, j)
            # native float (not numpy.float64 / dict) keeps Projection
            # on native scalar types for Cython.
            assert type(coef) is float
            assert coef == corr_df.at[i, j]


# ---------------------------------------------------------------------------
# risk_life: aggregated life underwriting capital requirement

@pytest.mark.parametrize("idx", IDXS)
def test_risk_life_aggregates_subrisks(ex1_model, idx):
    """risk_life(t) = sqrt(sum_ij corr_ij * sub_i * sub_j) over all risks."""
    proj = ex1_model.Projection[idx]
    corr_df = ex1_model.InputData.life_corr_data()
    risks = list(corr_df.index)
    sub = {r: proj.risk_life_sub(0, r) for r in risks}
    expected = math.sqrt(
        sum(sub[i] * sub[j] * corr_df.at[i, j]
            for i in risks for j in risks))
    assert math.isclose(proj.risk_life(0), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
def test_risk_life_at_least_largest_subrisk(ex1_model, idx):
    """Diversified total is never below the worst single sub-risk."""
    proj = ex1_model.Projection[idx]
    risks = list(ex1_model.InputData.life_corr_data().index)
    worst = max(proj.risk_life_sub(0, r) for r in risks)
    assert proj.risk_life(0) >= worst - 1e-9


# ---------------------------------------------------------------------------
# coc_rate / risk_margin

def test_coc_rate_forwards_input_data(ex1_model):
    """Assumptions.coc_rate forwards ConstParams['CoCRate'] as a native float."""
    coc = ex1_model.Assumptions.coc_rate()
    assert type(coc) is float  # native float for Cython, not numpy
    assert coc == ex1_model.InputData.const_params()["CoCRate"]
    assert coc == pytest.approx(0.06)


@pytest.mark.parametrize("idx", IDXS)
def test_risk_margin_equals_closed_form(ex1_model, idx):
    """risk_margin(0) = CoC * sum_s risk_life(s) / prod_{u<=s}(1 + r_u)."""
    proj = ex1_model.Projection[idx]
    coc = ex1_model.Assumptions.coc_rate()
    discount = 1.0
    expected = 0.0
    for s in range(proj.proj_len() + 1):
        discount *= 1 + proj.disc_rate(s)
        expected += proj.risk_life(s) / discount
    expected *= coc
    assert math.isclose(proj.risk_margin(0), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
def test_risk_margin_recursion(ex1_model, idx):
    """risk_margin(t) = (CoC*risk_life(t) + risk_margin(t+1)) / (1 + r_t)."""
    proj = ex1_model.Projection[idx]
    coc = ex1_model.Assumptions.coc_rate()
    expected = (coc * proj.risk_life(0)
                + proj.risk_margin(1)) / (1 + proj.disc_rate(0))
    assert math.isclose(proj.risk_margin(0), expected, rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize("idx", IDXS)
def test_risk_margin_terminal_zero_and_nonnegative(ex1_model, idx):
    """Beyond the projection it is zero, and it is never negative."""
    proj = ex1_model.Projection[idx]
    assert proj.risk_margin(proj.proj_len() + 1) == 0
    assert proj.risk_margin(0) >= 0
