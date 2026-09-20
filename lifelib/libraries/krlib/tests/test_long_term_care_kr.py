"""Golden and structural tests for ``LTC_KR_S``, the 간병보험 reference model.

The house-style contract — the two-Space layout, external inputs with no orphan CSV, the
``provenance`` column and its citation tag, the docstrings and the phrases they must carry,
the ``result_cf()`` shape, the read-once property, the round trip, and that every
``check_*()`` is ``True`` on **every** shipped model point — is asserted once for every
model in the library in ``test_model_conventions_kr.py``.  What is asserted here is this
product.

The golden values are the worked example in
``products/long_term_care/technical-notes.md`` ("Worked example"), which projects the
anchor cell: male, 만나이 40 at the 계약일, 90세만기, 20년납, 월납, 해약환급금 미지급형,
일반심사; 장기요양(1~2등급) 진단급여금 ₩10,000,000, 간병연금 **on** at ₩500,000 / ₩300,000 a
month with a 12-month guarantee and a 120-month cap, 치매 rider **off**, 보장개시일 3 months,
감액기간 12 months, ``lapse_form = mujihae``, office premium ₩5,600 a month.  They are
**hard-coded** here rather than pickled so that a reviewer can compare them against the notes
by eye.  Every row of the first-year table sits at 만나이 40 in policy year 1, so one set of
rates drives all thirteen of them.

Tolerances follow the precision the notes display: the first-year cash flow table to six
decimals, the compartment table to ten, the milestone rows and the undiscounted totals to
four, the decrement totals to twelve, and the assumption values — which the notes print at
full precision — to a relative 1e-12.

**This is a three-state model and the tests are shaped by that.**  The trigger is the public
scheme's own 장기요양등급 under 노인장기요양보험법, so the benefit definition belongs to a
statute rather than to a carrier, and the basis is built from a **prevalence** — the
국민건강보험공단 노인장기요양보험 통계연보 연령별 인정률 — and not from an incidence.  The
prevalence-to-incidence conversion is therefore the thing most worth protecting, and it is
asserted term by term: the analytic derivative of the fitted logistic, the **full product
rule** on ``P_C = s_G P``, the excess-mortality term with ``mu_bar`` in it, the closing
``direct_entry_share``, and the sub-65 carry-down on the one disclosed 예정위험률's gradient.
Each of those has a pitfall test that fails if the term were dropped, with the notes' own
figure for what dropping it costs.

Beyond the worked example this module asserts, one test each, every entry in the notes'
*Known modeling pitfalls* list, because each of them is a way an implementation can look
right and be wrong:

* 인정률 is a **prevalence**, not an incidence, and the ratio between them is not a constant;
* the excess-mortality term is not a refinement, and neither is ``mu_bar``;
* ``P_C'`` is taken by the **full product rule**, whose visible symptom is ``claims_lump``
  *falling* between ``t = 239`` and ``t = 240``;
* the 감액 is **frozen at first certification** and must not be re-tested at each instalment;
* the annuity's first instalment falls in the **month of certification**;
* the claim expense is per **event**, not per instalment;
* ``care_surv`` is a **partial product**, never a ratio of cumulative products;
* premium rides on ``pols_act``, never on ``pols_if``;
* lapse must not touch the care compartment — and the roll-forward check will not catch it;
* a certification inside the 보장개시일 window is a **decrement**, not a deferred claim;
* the surrender-value cliff has a **direction**, and three Korean forms differ only in which
  side of 납입완료 the 50% attaches to;
* ``claims_death`` is the **계약자적립액**, not a death benefit;
* the light compartment pays premium and lapses and the care compartment does neither;
* ``prog_rate_at`` is deliberately **not** scaled below 65;
* widening ``benefit_grade`` is not a re-scaling;
* the two modules run in opposite sex directions and the model does not reproduce that;
* the care state is absorbing because the **contract** makes it so;
* the disclosed 예정위험률 is not this model's level;
* and ``proj_len()`` is a **row count**, not the last index.

The six ``check_*`` cells are asserted **by name**, because a generic sweep cannot notice a
check that has quietly disappeared, and the [std] scalar assumptions are read off the model
so that a silent change to an assumption fails a test rather than moving a result.  The
whole-table sweep belongs to ``test_model_conventions_kr.py``; the second model points taken
here are the ones that exercise a particular mechanic — 2 for the female basis, 3 and 7 for
the 감액 freeze at the top of the issue-age range, 4 for the 간병연금 switched off, 5 for the
``g6`` gate that leaves no light state and for the 치매 rider, 6 for the
납입중50%해약환급금지급형 form, 7 again for the 표준형 surrender value, the 표준형 lapse
vector and the 60-month annuity cap, 8 for the 간편심사 loading, and 9 for the 우체국-style
180-day 보장개시일 and two-year 감액기간.

Where a sensitivity is quoted against a **model point column** or an assumption **table**
rather than against a Space Reference, :func:`variant_model` and :func:`variant_table` copy
the model *and its external inputs* to a temporary directory and edit the copy, so the
shipped product directory is never written to.
"""
import math
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS


MODEL_DIR = LIB / MODELS["LTC_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

WON6 = 5e-7        # the first policy year's cash flow table, six decimals
WON4 = 5e-5        # the milestone rows, the totals and the present values, four decimals
INFORCE = 5e-11    # the compartment table, ten decimals
COUNT = 5e-13      # the decrement and state totals, twelve decimals
FULL = 1e-12       # values the notes print at full precision, as a relative tolerance


def _fresh_copy(tmp_path, name):
    """The model folder and every CSV beside it, copied into ``tmp_path / name``.

    Each variant gets its **own** directory rather than sharing one per test.  Inputs are
    external, so a variant is made by editing a file; two variants sharing a directory
    would compose their edits, and a test asking for a 100세만기 after a test asking for a
    flat grade share would silently get both.
    """
    root = tmp_path / name
    if not root.exists():
        shutil.copytree(MODEL_DIR, root / MODEL_DIR.name)
        for csv in CSV_DIR.glob("*.csv"):
            shutil.copy(csv, root / csv.name)
    return root


def variant_model(tmp_path, name, point_id=1, **overrides):
    """A copy of the model whose model point table has been edited.

    Most of this product's switches — the 보험기간, the 등급 threshold, the surrender-value
    form, the lapse vector, the 감액기간, the 간병연금 — are **model point columns**, not
    Space References, so exercising the other position means changing an input file.  The
    whole model folder and every CSV beside it are copied to ``tmp_path`` first, inputs
    being external and therefore having to travel with the model, and the copy is edited.
    """
    root = _fresh_copy(tmp_path, name)
    table = pd.read_csv(root / "model_point_table.csv", index_col="point_id")
    for column, value in overrides.items():
        table.loc[point_id, column] = value
    table.to_csv(root / "model_point_table.csv")
    return mx.read_model(root / MODEL_DIR.name, name=name)


def variant_table(tmp_path, name, filename, mutate):
    """A copy of the model one of whose **assumption tables** has been edited.

    The companion to :func:`variant_model`, for the one sensitivity the notes quote against
    an input file rather than against a model point column — replacing the age-varying
    1·2등급 share with the national all-ages figure.  ``mutate`` takes the loaded
    ``DataFrame`` and returns the edited one.
    """
    root = _fresh_copy(tmp_path, name)
    table = pd.read_csv(root / filename)
    mutate(table).to_csv(root / filename, index=False)
    return mx.read_model(root / MODEL_DIR.name, name=name)


def lifetime(p):
    """The lifetime totals the notes' sensitivities are quoted against, undiscounted.

    ``range(p.proj_len())`` is the whole frame, ``t = 0 ... proj_len() - 1``; the last row
    is the maturity month and contributes nothing to any of these sums.
    """
    ts = range(p.proj_len())
    lump = sum(p.claims(t, "LUMP") for t in ts)
    annuity = sum(p.claims(t, "ANNUITY") for t in ts)
    return {
        "premiums": sum(p.premiums(t) for t in ts),
        "claims_lump": lump,
        "claims_annuity": annuity,
        "benefit": lump + annuity,
        "claims_lapse": sum(p.claims(t, "LAPSE") for t in ts),
        "net_cf": sum(p.net_cf(t) for t in ts),
        "entries": sum(p.pols_entry_care(t) for t in ts),
    }


def pv_benefit_over_premium(p):
    """PV(장기요양 benefit) / PV(premium) at the 예정이율, the notes' calibration ratio.

    The model does not publish present values — this library projects gross undiscounted
    cash flows and leaves discounting to the layer above — so the discounting is done here,
    at the same 2.0% 연단위 복리 the account is accumulated at.
    """
    j = (1.0 + p.prem_int_rate) ** (1.0 / 12.0) - 1.0
    ts = range(p.proj_len())
    pv_prem = sum(p.premiums(t) * (1.0 + j) ** -t for t in ts)
    pv_ben = sum((p.claims(t, "LUMP") + p.claims(t, "ANNUITY")) * (1.0 + j) ** -t
                 for t in ts)
    return pv_ben / pv_prem


def first_entry_rate(p, x):
    """The model's own annual rate of a **first** entry at or above the benefit grade.

    Direct entry plus progression by lives already certified at a light grade, which is the
    quantity :func:`disclosed_inc_ratio_at` compares with the disclosed 예정위험률 and the
    quantity the notes compare with the prevalence.  Rebuilt here from its three parts so
    that the pitfall tests read it the way the notes write it.
    """
    xe = max(float(x), float(p.sub65_age))
    return (p.inc_rate_direct_at(x)
            + p.prev_light_at(xe) * p.prog_rate_at(xe) * p.sub65_factor_at(x)
            / (1.0 - p.prev_care_at(xe)))


# ---------------------------------------------------------------------------
# The worked example, hard-coded to the precision the notes display


def test_the_anchor_cell_is_the_worked_examples_model_point(kr_ltc_anchor):
    """Model point 1 is the cell the notes' worked example projects.

    Every golden value below is read off that one model point, so an edit to its row in
    ``model_point_table.csv`` must fail here rather than silently move the goldens.  The
    contract is 비갱신형 with a fixed 납입기간, which is the opposite of the Korean
    *medical* market's annual renewal and the right answer for a benefit whose claim
    arrives thirty years after issue.
    """
    p = kr_ltc_anchor
    assert p.policy_id() == "LTC-000001"
    assert p.issue_age() == 40
    assert p.sex() == "M"
    assert p.term_age() == 90
    assert p.prem_period_years() == 20
    assert p.prem_period_mths() == 240
    assert p.prem_mode() == "monthly"
    assert p.benefit_grade() == "g2"
    assert p.lump_amount() == 10_000_000.0
    assert p.annuity_on() is True
    assert p.annuity_high() == 500_000.0
    assert p.annuity_low() == 300_000.0
    assert p.annuity_max_mths() == 120
    assert p.annuity_guar_mths() == 12
    assert p.dementia_rider() is False
    assert p.wait_mths() == 3
    assert p.red_mths() == 12
    assert p.cv_form() == "mijigeup"
    assert p.lapse_form() == "mujihae"
    assert p.uw_loading() == 1.0
    assert p.premium_mth_pp() == 5_600.0
    assert p.pols_if_init() == 1.0
    assert p.proj_len() == 601                       # 12 x (90 - 40) + 1
    assert len(p.result_cf()) == 601                 # proj_len() rows, t = 0 .. 600


def test_the_worked_examples_assumption_values(kr_ltc_anchor):
    """Every rate the notes quote for the worked example, to the digits they print.

    The notes list these under "Every assumption value the first rows use", which makes
    them the model's contract with the document: the thirteen-row cash flow table below is
    only meaningful if the rates driving it are the notes' own.  All of them sit at 만나이
    40 in policy year 1, so this one set drives rows ``t = 0 ... 11``.
    """
    p = kr_ltc_anchor
    assert p.mort_rate(0) == 0.00097601273
    assert p.mort_rate_mth(0) == pytest.approx(0.0000813708009308467, rel=FULL)
    assert p.mort_rate_light(0) == pytest.approx(0.001756822914, rel=FULL)
    assert p.mort_rate_light_mth(0) == pytest.approx(0.0001465199263399608, rel=FULL)
    assert p.mort_rate_care(0) == pytest.approx(0.00292803819, rel=FULL)
    assert p.mort_rate_care_mth(0) == pytest.approx(0.00024433125292278035, rel=FULL)
    assert p.lapse_rate(0) == 0.08
    assert p.lapse_rate_mth(0) == pytest.approx(0.006924382628299419, rel=FULL)
    assert p.prev_rate_at(40) == pytest.approx(0.00038039917723430234, rel=FULL)
    assert p.prev_care_at(40) == pytest.approx(0.00008444861734601512, rel=FULL)
    assert p.prev_light_at(40) == pytest.approx(0.0002959505598882872, rel=FULL)
    assert p.share_ge_at("g2", 40) == 0.222
    assert p.sub65_factor_at(40) == pytest.approx(0.04710884458012182, rel=FULL)
    assert p.inc_rate_direct_at(40) == pytest.approx(0.0000022292964462128687, rel=FULL)
    assert p.inc_rate_light_at(40) == pytest.approx(0.00010426974412244515, rel=FULL)
    assert p.prog_rate_at(40) == pytest.approx(0.03396845379835368, rel=FULL)
    assert p.inc_rate_direct_mth(0) == pytest.approx(
        0.00000018577470385107238, rel=FULL)
    assert p.inc_rate_light_mth(0) == pytest.approx(0.000008689145343537096, rel=FULL)
    assert p.prog_rate_mth(0) == pytest.approx(0.0028307044831961396, rel=FULL)
    assert p.disclosed_inc_at(40) == pytest.approx(0.000046, rel=FULL)
    assert p.disclosed_inc_ratio_at(40) == pytest.approx(0.23993880644434135, rel=FULL)
    assert p.red_factor(0) == 0.525
    assert p.red_factor(11) == 0.525
    assert p.red_factor(12) == 1.0
    assert p.ann_amount_at(0) == pytest.approx(207495.7410562181, rel=FULL)
    assert p.ann_amount_at(12) == pytest.approx(395229.98296422494, rel=FULL)
    assert p.expense_acq_mths * p.premium_mth_pp() == 29_120.0
    assert p.expense_maint == 200.0
    assert p.comm_init_pp() == 43_680.0
    assert p.expense_claim == 30_000.0
    assert p.net_prem_ratio() == pytest.approx(0.7931662309087683, rel=FULL)
    assert p.sub65_gradient() == pytest.approx(0.12221178050285361, rel=FULL)


def test_the_monthly_rates_are_the_annual_ones_compounded_not_divided(kr_ltc_anchor):
    """``1 - (1 - q)^(1/12)`` for the three mortalities and for lapse, ``/12`` for entry.

    The distinction is deliberate and the notes' dimensional check turns on it.  The three
    mortality rates and the lapse rate are **probabilities** and are converted by
    compounding; the three transition rates are **rates per year** and are divided, uniform
    within the policy year.  A model that divided the probabilities, or compounded the
    rates, would move every row of the worked example by a little and no check would fail.
    """
    p = kr_ltc_anchor
    for t in (0, 12, 240, 480):
        assert p.mort_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - p.mort_rate(t)) ** (1.0 / 12.0), rel=FULL)
        assert p.mort_rate_light_mth(t) == pytest.approx(
            1.0 - (1.0 - p.mort_rate_light(t)) ** (1.0 / 12.0), rel=FULL)
        assert p.mort_rate_care_mth(t) == pytest.approx(
            1.0 - (1.0 - p.mort_rate_care(t)) ** (1.0 / 12.0), rel=FULL)
        assert p.lapse_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - p.lapse_rate(t)) ** (1.0 / 12.0), rel=FULL)
        assert p.inc_rate_direct_mth(t) == pytest.approx(
            p.inc_rate_direct(t) / 12.0, rel=FULL)
        assert p.inc_rate_light_mth(t) == pytest.approx(
            p.inc_rate_light(t) / 12.0, rel=FULL)
        assert p.prog_rate_mth(t) == pytest.approx(p.prog_rate(t) / 12.0, rel=FULL)
    assert p.mort_rate_light(0) == pytest.approx(1.8 * p.mort_rate(0), rel=FULL)
    assert p.mort_rate_care(0) == pytest.approx(3.0 * p.mort_rate(0), rel=FULL)


def test_the_prevalence_logistic_is_fitted_through_the_five_sourced_injeongryul(
        long_term_care, kr_ltc_anchor):
    """The three fitted parameters, and the fit against the five 인정률 they were fitted to.

    ``prevalence_table.csv`` carries the five sourced band rates as well as the three fitted
    parameters, so the fit can be checked against its own anchors rather than against a
    remembered number.  The notes put the male residuals inside +/-5.2%; the female fit is
    inside +/-7.9%, and neither is better than that because a three-parameter logistic
    cannot reproduce five band rates exactly.

    **Nothing above 만나이 88.5 is sourced, and that is where the claims are.**  How much
    the ceiling is worth is a separate sensitivity; what is pinned here is that the curve
    still passes through the data it was fitted to.
    """
    p = kr_ltc_anchor
    assert p.prev_param("prev_ceil") == 0.7480
    assert p.prev_param("prev_beta") == 0.14692252
    assert p.prev_param("prev_x_mid") == 91.61515338
    table = long_term_care.Data.prevalence_table()
    for age, key in ((67, "prev_obs_67"), (72, "prev_obs_72"), (77, "prev_obs_77"),
                     (82, "prev_obs_82"), (88.5, "prev_obs_88")):
        observed = float(table.loc[("M", key), "value"])
        assert p.prev_rate_at(age) == pytest.approx(observed, rel=0.052), age
    assert p.prev_rate_at(65) == pytest.approx(0.014691, abs=5e-7)
    assert p.prev_rate_at(85) == pytest.approx(0.205325, abs=5e-7)
    # The derivative is the analytic one, beta P (1 - P / ceil), not a difference quotient.
    for age in (40, 65, 85):
        assert p.prev_slope_at(age) == pytest.approx(
            p.prev_param("prev_beta") * p.prev_rate_at(age)
            * (1.0 - p.prev_rate_at(age) / p.prev_param("prev_ceil")), rel=FULL)


# The notes' "The first policy year, cash flow" table, to the six decimals it displays.
# claims_dementia, claims_lapse and claims_maturity are identically zero over this range and
# are omitted from the notes' table; they are asserted as zeros in their own test.
# t -> (pols_if, premiums, claims_lump, claims_annuity, claims_death, claims_void,
#       expenses, claim_expenses, commissions, net_cf)
WORKED_EXAMPLE_CF = {
    0:  (1.000000, 5600.000000, 0.000000, 0.000000, 0.000000, 0.001040,
         29320.000000, 0.000000, 43680.000000, -67400.001040),
    1:  (0.992995, 5560.769900, 0.000000, 0.000000, 0.359493, 0.002340,
         198.598925, 0.000000, 0.000000, 5361.809142),
    2:  (0.986038, 5521.814482, 0.000000, 0.000000, 0.714544, 0.003891,
         197.207660, 0.000000, 0.000000, 5323.888388),
    3:  (0.979131, 5483.131826, 1.333122, 0.052689, 1.065193, 0.000000,
         195.826137, 0.007618, 0.000000, 5284.847067),
    4:  (0.972272, 5444.720021, 1.448226, 0.109927, 1.411483, 0.000000,
         194.454337, 0.008276, 0.000000, 5247.287772),
    5:  (0.965461, 5406.577174, 1.561294, 0.171634, 1.753454, 0.000000,
         193.092148, 0.008922, 0.000000, 5209.989723),
    6:  (0.958698, 5368.701402, 1.672351, 0.237731, 2.091145, 0.000000,
         191.739501, 0.009556, 0.000000, 5172.951118),
    7:  (0.951982, 5331.090836, 1.781423, 0.308138, 2.424598, 0.000000,
         190.396330, 0.010180, 0.000000, 5136.170167),
    8:  (0.945313, 5293.743621, 1.888537, 0.382778, 2.753852, 0.000000,
         189.062569, 0.010792, 0.000000, 5099.645094),
    9:  (0.938691, 5256.657915, 1.993717, 0.461576, 3.078946, 0.000000,
         187.738151, 0.011393, 0.000000, 5063.374132),
    10: (0.932115, 5219.831887, 2.096990, 0.544455, 3.399919, 0.000000,
         186.423012, 0.011983, 0.000000, 5027.355528),
    11: (0.925585, 5183.263720, 2.198380, 0.631342, 3.716809, 0.000000,
         185.117086, 0.012562, 0.000000, 4991.587540),
    12: (0.919102, 5146.951609, 4.601130, 0.813192, 4.308813, 0.000000,
         187.496714, 0.013803, 154.408548, 4795.309407),
}

# The notes' "The compartments, first policy year" table, to the ten decimals it displays.
# t -> (pols_healthy, pols_light, pols_care, pols_entry_light, pols_entry_care_direct,
#       pols_entry_care_prog, pols_entry_care, pols_void, pols_death_act, pols_lapse)
WORKED_EXAMPLE_POLS = {
    0:  (1.0000000000, 0.0000000000, 0.0000000000, 0.0000086891, 0.0000001858,
         0.0000000000, 0.0000000000, 0.0000001858, 0.0000813714, 0.0069238179),
    1:  (0.9929859973, 0.0000086277, 0.0000000000, 0.0000086282, 0.0000001845,
         0.0000000244, 0.0000000000, 0.0000002089, 0.0000808019, 0.0068753138),
    2:  (0.9860211908, 0.0000171097, 0.0000000000, 0.0000085677, 0.0000001832,
         0.0000000484, 0.0000000000, 0.0000002316, 0.0000802364, 0.0068271493),
    3:  (0.9791052354, 0.0000254477, 0.0000000000, 0.0000085076, 0.0000001819,
         0.0000000720, 0.0000002539, 0.0000000000, 0.0000796748, 0.0067793220),
    4:  (0.9722377886, 0.0000336437, 0.0000002539, 0.0000084479, 0.0000001806,
         0.0000000952, 0.0000002759, 0.0000000000, 0.0000791172, 0.0067318297),
    5:  (0.9654185101, 0.0000416995, 0.0000005296, 0.0000083887, 0.0000001794,
         0.0000001180, 0.0000002974, 0.0000000000, 0.0000785635, 0.0066846698),
    6:  (0.9586470621, 0.0000496168, 0.0000008268, 0.0000083298, 0.0000001781,
         0.0000001405, 0.0000003185, 0.0000000000, 0.0000780137, 0.0066378402),
    7:  (0.9519231089, 0.0000573975, 0.0000011450, 0.0000082714, 0.0000001768,
         0.0000001625, 0.0000003393, 0.0000000000, 0.0000774677, 0.0065913385),
    8:  (0.9452463176, 0.0000650433, 0.0000014840, 0.0000082134, 0.0000001756,
         0.0000001841, 0.0000003597, 0.0000000000, 0.0000769255, 0.0065451624),
    9:  (0.9386163574, 0.0000725560, 0.0000018433, 0.0000081558, 0.0000001744,
         0.0000002054, 0.0000003798, 0.0000000000, 0.0000763871, 0.0064993096),
    10: (0.9320328997, 0.0000799372, 0.0000022225, 0.0000080986, 0.0000001731,
         0.0000002263, 0.0000003994, 0.0000000000, 0.0000758525, 0.0064537779),
    11: (0.9254956184, 0.0000871887, 0.0000026213, 0.0000080418, 0.0000001719,
         0.0000002468, 0.0000004187, 0.0000000000, 0.0000753216, 0.0064085651),
    12: (0.9190041896, 0.0000943121, 0.0000030393, 0.0000090234, 0.0000001929,
         0.0000002672, 0.0000004601, 0.0000000000, 0.0000799758, 0.0050125240),
}


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_the_worked_examples_first_year_cash_flow(kr_ltc_anchor, t):
    """Every cell of the notes' thirteen-row cash flow table, to the six decimals shown.

    This is the test module's main job.  A change anywhere in the basis, in the expense
    calibration or in the processing order moves one of these numbers, and the notes and
    the model then disagree — which is the failure this library exists to make loud.
    """
    p = kr_ltc_anchor
    (pols_if, prem, lump, annuity, death, void,
     exp, claim_exp, comm, ncf) = WORKED_EXAMPLE_CF[t]
    assert p.pols_if(t) == pytest.approx(pols_if, abs=WON6)
    assert p.premiums(t) == pytest.approx(prem, abs=WON6)
    assert p.claims(t, "LUMP") == pytest.approx(lump, abs=WON6)
    assert p.claims(t, "ANNUITY") == pytest.approx(annuity, abs=WON6)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=WON6)
    assert p.claims(t, "VOID") == pytest.approx(void, abs=WON6)
    assert p.expenses(t) == pytest.approx(exp, abs=WON6)
    assert p.claim_expenses(t) == pytest.approx(claim_exp, abs=WON6)
    assert p.commissions(t) == pytest.approx(comm, abs=WON6)
    assert p.net_cf(t) == pytest.approx(ncf, abs=WON6)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_POLS))
def test_the_worked_examples_first_year_compartments(kr_ltc_anchor, t):
    """Every cell of the notes' compartment table, to the ten decimals shown.

    The counts are what the cash flow table is built on, and they are published to ten
    decimals precisely because the interesting ones are of order 1e-7: a certification rate
    at 만나이 40 of one in 450,000 a year does not survive rounding to the nearest won.
    """
    p = kr_ltc_anchor
    (healthy, light, care, entry_light, entry_direct,
     entry_prog, entry_care, void, death_act, lapse) = WORKED_EXAMPLE_POLS[t]
    assert p.pols_healthy(t) == pytest.approx(healthy, abs=INFORCE)
    assert p.pols_light(t) == pytest.approx(light, abs=INFORCE)
    assert p.pols_care(t) == pytest.approx(care, abs=INFORCE)
    assert p.pols_entry_light(t) == pytest.approx(entry_light, abs=INFORCE)
    assert p.pols_entry_care_direct(t) == pytest.approx(entry_direct, abs=INFORCE)
    assert p.pols_entry_care_prog(t) == pytest.approx(entry_prog, abs=INFORCE)
    assert p.pols_entry_care(t) == pytest.approx(entry_care, abs=INFORCE)
    assert p.pols_void(t) == pytest.approx(void, abs=INFORCE)
    assert p.pols_death_act(t) == pytest.approx(death_act, abs=INFORCE)
    assert p.pols_lapse(t) == pytest.approx(lapse, abs=INFORCE)


def test_the_worked_examples_month_0_trace(kr_ltc_anchor):
    """The notes' month-0 trace, term by term.

    Month 0 decides the whole of the first row: one policy, one set of entry rates, 5.2
    months of acquisition expense and the whole 7.8 months of initial commission against a
    single month's premium.  It is also where the two 보장개시일 facts are visible at once —
    a certification happens, ``pols_entry_care(0)`` is nevertheless nil because ``0 < W``,
    and ``claims_void(0)`` is nevertheless **not** nil, because the month-0 premium fell at
    the start of the month and a cover voided at the end of it is void ab initio: the refund
    is ``cum_prem_pp(t + 1)``, not ``cum_prem_pp(t)``.
    """
    p = kr_ltc_anchor
    assert p.pols_healthy(0) == 1.0
    assert p.pols_light(0) == 0.0 and p.pols_care(0) == 0.0
    assert p.pols_act(0) == 1.0 and p.pols_if(0) == 1.0
    assert p.premiums(0) == 5_600.0
    assert p.pols_entry_light(0) == pytest.approx(0.000008689145343537096, rel=FULL)
    assert p.pols_entry_care_direct(0) == pytest.approx(
        0.00000018577470385107238, rel=FULL)
    assert p.pols_entry_care_prog(0) == 0.0          # no light compartment to progress out of
    assert p.pols_entry_care(0) == 0.0               # 0 = t < W = 3
    assert p.pols_void(0) == pytest.approx(0.00000018577470385107238, rel=FULL)
    assert p.cum_prem_pp(0) == 0.0                   # paid before month 0's own premium
    assert p.cum_prem_pp(1) == 5_600.0               # ...which is what the void returns
    assert p.claims(0, "VOID") == pytest.approx(
        5_600.0 * 0.00000018577470385107238, abs=WON6)
    assert p.pols_healthy_mid(0) == pytest.approx(0.9999911250799526, rel=FULL)
    assert p.pols_light_mid(0) == pytest.approx(0.000008689145343537096, rel=FULL)
    assert p.pols_care_mid(0) == 0.0
    assert p.pols_death_act(0) == pytest.approx(
        0.9999911250799526 * 0.0000813708009308467
        + 0.000008689145343537096 * 0.0001465199263399608, rel=FULL)
    assert p.av_pp(0) == 0.0
    assert p.claims(0, "DEATH") == 0.0               # the account opens at nil
    assert p.pols_lapse(0) == pytest.approx(0.0069238178955, abs=5e-13)
    assert p.expenses(0) == pytest.approx(5.2 * 5_600 + 200.0, abs=WON6)
    assert p.commissions(0) == pytest.approx(7.8 * 5_600, abs=WON6)
    assert p.claim_expenses(0) == 0.0
    assert p.net_cf(0) == pytest.approx(
        5_600.0 - 0.001040 - 29_320.0 - 43_680.0, abs=WON6)
    # The roll forward out of month 0, term by term.
    assert p.pols_healthy(1) == pytest.approx(
        0.9999911250799526 * (1.0 - 0.0000813708009308467)
        * (1.0 - 0.006924382628299419), rel=FULL)
    assert p.pols_light(1) == pytest.approx(
        0.000008689145343537096 * (1.0 - 0.0001465199263399608)
        * (1.0 - 0.006924382628299419), rel=FULL)
    assert p.pols_care(1) == 0.0


def test_the_worked_examples_month_1_trace(kr_ltc_anchor):
    """The notes' month-1 trace: the first progression, the first refund, the first account.

    Every per-policy rate is unchanged from month 0 — ``age(1) = 40``, policy year still 1 —
    so what moves is the population.  Three firsts land in this row: the first progression
    out of the light compartment, the second and larger ``claims_void`` now that two
    premiums have been paid, and the first non-zero ``claims_death``, the account having one
    month in it.
    """
    p = kr_ltc_anchor
    assert p.age(1) == 40 and p.policy_year(1) == 1
    assert p.premiums(1) == pytest.approx(5_600.0 * 0.992994624977843, abs=WON6)
    assert p.pols_act(1) == pytest.approx(0.992994624977843, rel=FULL)
    assert p.pols_entry_light(1) == pytest.approx(
        0.9929859973 * 0.000008689145343537096, abs=INFORCE)
    assert p.pols_entry_care_direct(1) == pytest.approx(
        0.9929859973 * 0.00000018577470385107238, abs=INFORCE)
    assert p.pols_entry_care_prog(1) == pytest.approx(
        p.pols_light(1) * 0.0028307044831961396, rel=FULL)
    assert p.pols_entry_care_prog(1) > 0.0           # the first progression in the model
    assert p.pols_entry_care(1) == 0.0               # 1 = t < W = 3
    assert p.pols_void(1) == pytest.approx(0.00000020889418843702306, rel=FULL)
    assert p.cum_prem_pp(1) == 5_600.0
    assert p.claims(1, "VOID") == pytest.approx(
        11_200.0 * 0.00000020889418843702306, abs=WON6)
    assert p.prem_accum_factor(1) == pytest.approx(1.0016515813, abs=5e-11)
    assert p.av_pp(1) == pytest.approx(4449.066773, abs=WON6)
    assert p.claims(1, "DEATH") == pytest.approx(
        p.av_pp(1) * p.pols_death_act(1), rel=FULL)
    assert p.expenses(1) == pytest.approx(200.0 * 0.992994624977843, abs=WON6)
    assert p.commissions(1) == 0.0                   # no renewal commission before t = 12
    assert p.claim_expenses(1) == 0.0                # nothing payable happened
    assert p.net_cf(1) == pytest.approx(
        5560.769900 - 0.359493 - 0.002340 - 198.598925, abs=WON6)


def test_the_worked_examples_month_3_trace_is_the_first_payable_certification(
        kr_ltc_anchor):
    """The notes' month-3 trace: 보장개시일 closes, and the lump sum and the annuity start.

    ``t = 3 >= W = 3`` is the boundary, and three things happen in the same row for the
    first time: ``claims_lump``, ``claims_annuity`` — the first instalment falls in the
    **month of certification**, so the ``u = 0`` term of the ledger is ``n_C(3)`` itself —
    and ``claim_expenses``, one event, the certification.  ``pols_void`` is nil from here
    on, the window having closed.
    """
    p = kr_ltc_anchor
    assert p.wait_mths() == 3
    assert p.pols_healthy(3) == pytest.approx(0.9791052354319798, rel=FULL)
    assert p.pols_light(3) == pytest.approx(0.0000254477, abs=INFORCE)
    assert p.pols_care(3) == 0.0                     # month-3 entrants arrive at t = 4
    assert p.pols_entry_care_direct(3) == pytest.approx(
        0.00000018189298515141055, rel=FULL)
    assert p.pols_entry_care_prog(3) == pytest.approx(
        0.00000007203498063473715, rel=FULL)
    assert p.pols_entry_care(3) == pytest.approx(0.0000002539279657861477, rel=FULL)
    assert p.pols_void(3) == 0.0
    assert p.red_factor(3) == 0.525
    assert p.claims(3, "LUMP") == pytest.approx(
        10_000_000 * 0.525 * 0.0000002539279657861477, abs=WON6)
    # The frozen annuity amount is the grade blend read at 만나이 65, times r(3).
    assert p.share_ge_at("g1", 65) == pytest.approx(0.07985714285714286, rel=FULL)
    assert p.share_ge_at("g2", 65) == pytest.approx(0.1677142857142857, rel=FULL)
    blended = ((0.07985714285714286 * 500_000
                + (0.1677142857142857 - 0.07985714285714286) * 300_000)
               / 0.1677142857142857)
    assert blended == pytest.approx(395229.98296422494, rel=FULL)
    assert p.ann_amount_at(3) == pytest.approx(blended * 0.525, rel=FULL)
    assert p.ann_amount_at(3) == pytest.approx(207495.7410562181, rel=FULL)
    assert p.ann_count(3) == pytest.approx(p.pols_entry_care(3), rel=FULL)
    assert p.claims(3, "ANNUITY") == pytest.approx(
        207495.7410562181 * 0.0000002539279657861477, abs=WON6)
    assert p.claim_expenses(3) == pytest.approx(
        30_000 * 0.0000002539279657861477, abs=WON6)
    assert p.ann_tests(3) == 0.0                     # the first annual test is twelve months on
    assert p.av_pp(3) == pytest.approx(13369.256441, abs=WON6)
    assert p.claims(3, "DEATH") == pytest.approx(
        13369.256441 * p.pols_death_act(3), abs=WON6)
    assert p.net_cf(3) == pytest.approx(
        5483.131826 - 1.333122 - 0.052689 - 1.065193 - 195.826137 - 0.007618,
        abs=WON6)


def test_the_worked_examples_month_12_trace_is_the_gamaek_expiring(kr_ltc_anchor):
    """The notes' month-12 trace: the 감액기간 expires and the renewal commission starts.

    Two steps in one row.  ``claims_lump`` roughly doubles because ``red_factor`` goes from
    0.525 to 1.0, and ``commissions`` goes from nil to 3% of premium.  ``claims_annuity``
    does **not** step, and that is the freeze doing its work: the cohorts of months 3 to 11
    are still carried at ₩207,495.74 and only the month-12 cohort is at ₩395,229.98.  The
    ``expenses`` line steps too, from 185.117086 to 187.496714, because the 2% expense
    inflation factor increments at the 계약해당일 even though the in-force count has fallen.
    """
    p = kr_ltc_anchor
    assert p.age(12) == 41 and p.policy_year(12) == 2
    assert p.lapse_rate(12) == pytest.approx(0.06352246697177472, rel=FULL)
    assert p.red_factor(12) == 1.0
    assert p.pols_entry_care(12) == pytest.approx(0.00000046011303806134214, rel=FULL)
    assert p.claims(12, "LUMP") == pytest.approx(
        10_000_000 * 1.0 * 0.00000046011303806134214, abs=WON6)
    step = p.claims(12, "LUMP") / p.claims(11, "LUMP")
    assert step == pytest.approx(2.09, abs=0.005)
    assert 1.0 / 0.525 == pytest.approx(1.90, abs=0.005)   # of which the 감액 is this much
    # Every cohort still inside the twelve-month guarantee, so every weight is 1.
    assert p.ann_pay(12) == pytest.approx(0.813192, abs=WON6)
    assert p.ann_pay(12) == pytest.approx(
        sum(p.ann_amount_at(s) * p.pols_entry_care(s) for s in range(0, 13)), rel=FULL)
    assert p.ann_amount_at(11) == pytest.approx(207495.7410562181, rel=FULL)
    assert p.ann_amount_at(12) == pytest.approx(395229.98296422494, rel=FULL)
    assert p.commissions(12) == pytest.approx(0.03 * 5146.951609, abs=WON6)
    assert p.expenses(12) == pytest.approx(
        200.0 * 1.02 ** 1 * p.pols_if(12), abs=WON6)
    assert p.expenses(12) > p.expenses(11)
    assert p.pols_if(12) < p.pols_if(11)
    assert p.claim_expenses(12) == pytest.approx(
        30_000 * 0.00000046011303806134214, abs=WON6)
    assert p.ann_tests(12) == 0.0                    # the first cohort's anniversary is month 15
    assert p.ann_tests(15) > 0.0
    assert p.net_cf(12) == pytest.approx(4795.309407, abs=WON6)
    assert p.net_cf(12) == pytest.approx(
        5146.951609 - 4.601130 - 0.813192 - 4.308813 - 187.496714 - 0.013803
        - 154.408548, abs=5e-6)      # seven displayed terms, so seven roundings


def test_the_worked_examples_month_240_trace_is_the_surrender_value_cliff(kr_ltc_anchor):
    """The notes' month-240 trace: 납입완료, and the contract turns over in one month.

    Two things step at once and their product is the cliff.  The lapse rate goes from the
    0.1% convergence point to the 0.8% post-완납 ultimate, a factor of eight, and the value
    paid on each of those lapses goes from nil to ₩654,528 — a 환급률 of exactly 48.700000%
    against cumulative premiums, which is the published figure to three decimals.  The
    account's two branches meet here by construction, because ``net_prem_ratio()`` is
    *derived* from the run-off's first anchor rather than assumed.
    """
    p = kr_ltc_anchor
    n = p.prem_period_mths()
    assert n == 240
    assert p.prem_accum_factor(240) == pytest.approx(294.7175395152288, rel=FULL)
    assert p.av_pp(240) == pytest.approx(1_309_056.0, abs=WON4)
    assert p.av_pp(240) == pytest.approx(
        p.net_prem_ratio() * 5_600 * 294.7175395152288, rel=FULL)
    assert p.av_pp(240) == pytest.approx(0.974 * 5_600 * 240, rel=FULL)
    assert p.check_av_continuity_resid(240) == pytest.approx(0.0, abs=1e-9)
    assert p.cv_pp(239) == 0.0
    assert p.cv_pp(240) == pytest.approx(654_528.0, abs=WON4)
    assert p.cum_prem_pp(240) == 1_344_000.0
    assert p.cv_pp(240) / p.cum_prem_pp(240) == pytest.approx(0.487000, abs=5e-7)
    assert p.lapse_rate(239) == 0.001
    assert p.lapse_rate(240) == 0.008
    assert p.pols_lapse(239) == pytest.approx(0.0000536909, abs=INFORCE)
    assert p.pols_lapse(240) == pytest.approx(0.0004306951, abs=INFORCE)
    assert p.pols_lapse(240) / p.pols_lapse(239) == pytest.approx(8.0, abs=0.05)
    assert p.claims(239, "LAPSE") == 0.0
    assert p.claims(240, "LAPSE") == pytest.approx(281.9020, abs=WON4)
    assert p.premiums(239) > 0.0 and p.premiums(240) == 0.0
    assert p.net_cf(239) == pytest.approx(2496.2682, abs=WON4)
    assert p.net_cf(240) == pytest.approx(-1284.5196, abs=WON4)


# The notes' "Milestone rows", to the four decimals it displays.
# t -> (age, pols_if, pols_act, pols_care, premiums, claims_lump, claims_annuity,
#       claims_death, claims_lapse, expenses, claim_expenses, commissions, net_cf)
MILESTONE_ROWS = {
    12:  (41, 0.9191, 0.9191, 0.0000, 5146.9516, 4.6011, 0.8132, 4.3088, 0.0000,
          187.4967, 0.0138, 154.4085, 4795.3094),
    120: (50, 0.6891, 0.6889, 0.0002, 3857.6317, 37.4014, 80.2047, 69.6691, 0.0000,
          167.9928, 0.5636, 115.7290, 3386.0712),
    239: (59, 0.6453, 0.6442, 0.0011, 3607.7963, 139.1227, 361.8337, 311.9062, 0.0000,
          188.0242, 2.4075, 108.2339, 2496.2682),
    240: (60, 0.6450, 0.6439, 0.0011, 0.0000, 101.8715, 364.1340, 342.5724, 281.9020,
          191.6972, 2.3426, 0.0000, -1284.5196),
    241: (60, 0.6443, 0.6432, 0.0011, 0.0000, 102.8477, 366.4506, 342.5552, 281.8690,
          191.4910, 2.3662, 0.0000, -1287.5797),
    300: (65, 0.6016, 0.5999, 0.0017, 0.0000, 124.6609, 493.3706, 534.0717, 277.9321,
          197.3947, 3.0831, 0.0000, -1630.5131),
    360: (70, 0.5513, 0.5488, 0.0025, 0.0000, 252.6475, 651.6038, 826.1459, 268.1912,
          199.7145, 4.3504, 0.0000, -2202.6533),
    480: (80, 0.4151, 0.4096, 0.0056, 0.0000, 771.8873, 1656.5015, 1546.9336, 185.4590,
          183.3274, 11.6465, 0.0000, -4355.7552),
    540: (85, 0.3212, 0.3128, 0.0084, 0.0000, 1681.5930, 2788.4692, 1004.5705, 70.6471,
          156.5864, 20.6729, 0.0000, -5722.5392),
    599: (89, 0.2120, 0.2017, 0.0103, 0.0000, 1844.5927, 3756.1556, 17.0540, 0.7571,
          111.8860, 24.9810, 0.0000, -5755.4264),
    600: (90, 0.2102, 0.1999, 0.0102, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
          0.0000, 0.0000, 0.0000, 0.0000),
}


@pytest.mark.parametrize("t", sorted(MILESTONE_ROWS))
def test_the_notes_milestone_rows(kr_ltc_anchor, t):
    """Every cell of the notes' eleven milestone rows, to the four decimals shown.

    They are where the contract's whole shape is visible: the 감액 expiring at 12, the
    납입완료 cliff between 239 and 240, the mortality table stepping at the 계약해당일 at 300
    and 480, the claims peaking at 85, and the last row — the 90세 계약해당일 — carrying an
    in-force count and **every cash flow zero**.
    """
    p = kr_ltc_anchor
    (age, pols_if, pols_act, pols_care, prem, lump, annuity, death, lapse,
     exp, claim_exp, comm, ncf) = MILESTONE_ROWS[t]
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=WON4)
    assert p.pols_act(t) == pytest.approx(pols_act, abs=WON4)
    assert p.pols_care(t) == pytest.approx(pols_care, abs=WON4)
    assert p.premiums(t) == pytest.approx(prem, abs=WON4)
    assert p.claims(t, "LUMP") == pytest.approx(lump, abs=WON4)
    assert p.claims(t, "ANNUITY") == pytest.approx(annuity, abs=WON4)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=WON4)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse, abs=WON4)
    assert p.expenses(t) == pytest.approx(exp, abs=WON4)
    assert p.claim_expenses(t) == pytest.approx(claim_exp, abs=WON4)
    assert p.commissions(t) == pytest.approx(comm, abs=WON4)
    assert p.net_cf(t) == pytest.approx(ncf, abs=WON4)


def test_the_mortality_table_steps_at_the_gyeyak_haedangil(kr_ltc_anchor):
    """``claims_death`` jumps between 299 and 300 and between 479 and 480, and only there.

    ``q(x)`` increments once a year on the 계약해당일 and the account is large by then, so
    the 계약자적립액 payable on a non-covered death steps with it: 487.5506 to 534.0717 at
    만나이 65 and 1,412.0604 to 1,546.9336 at 80.  Inside a policy year the same line moves
    only with the falling in-force count.  A model that read the mortality table at a
    fractional age, or on 보험나이 rather than on the 만나이 the public series is published
    on, would smooth these steps away.
    """
    p = kr_ltc_anchor
    assert p.claims(299, "DEATH") == pytest.approx(487.5506, abs=WON4)
    assert p.claims(300, "DEATH") == pytest.approx(534.0717, abs=WON4)
    assert p.claims(479, "DEATH") == pytest.approx(1412.0604, abs=WON4)
    assert p.claims(480, "DEATH") == pytest.approx(1546.9336, abs=WON4)
    assert p.age(299) == 64 and p.age(300) == 65
    assert p.mort_rate(299) == p.mort_rate_at_age(64)
    assert p.mort_rate(300) == p.mort_rate_at_age(65)
    for t in range(301, 312):                        # flat for the rest of the policy year
        assert p.mort_rate(t) == p.mort_rate(300)


# The notes' "Policy year 1 in aggregate", to the six decimals it displays.  The notes call
# it the strongest single test target in the file, because it exercises the whole annual
# cycle on one set of rates.
YEAR_1 = {
    "pols_if": 11.548279,
    "pols_act": 11.548268,
    "pols_light": 0.000538,
    "pols_care": 0.000011,
    "premiums": 64670.302783,
    "claims_lump": 15.974040,
    "claims_annuity": 2.900270,
    "claims_death": 22.769436,
    "claims_void": 0.007271,
    "expenses": 31429.655856,
    "claim_expenses": 0.091280,
    "commissions": 43680.000000,
    "net_cf": -10481.095370,
}


def test_policy_year_1_in_aggregate(kr_ltc_anchor):
    """The notes' year-1 totals, summed from unrounded monthly values.

    Every month of policy year 1 sits at 만나이 40 and in policy year 1, so one set of rates
    drives the whole cycle: the acquisition strain, the 보장개시일 window opening and
    closing, the 감액 running for the whole year, and the renewal commission still switched
    off.  The gap between the two in-force sums — 0.000011 over the year — is the waiver
    already biting on a block that has claimed almost nothing.
    """
    p = kr_ltc_anchor
    ts = range(12)
    assert sum(p.pols_if(t) for t in ts) == pytest.approx(YEAR_1["pols_if"], abs=WON6)
    assert sum(p.pols_act(t) for t in ts) == pytest.approx(YEAR_1["pols_act"], abs=WON6)
    assert sum(p.pols_light(t) for t in ts) == pytest.approx(
        YEAR_1["pols_light"], abs=WON6)
    assert sum(p.pols_care(t) for t in ts) == pytest.approx(
        YEAR_1["pols_care"], abs=WON6)
    assert sum(p.premiums(t) for t in ts) == pytest.approx(
        YEAR_1["premiums"], abs=WON6)
    assert sum(p.claims(t, "LUMP") for t in ts) == pytest.approx(
        YEAR_1["claims_lump"], abs=WON6)
    assert sum(p.claims(t, "ANNUITY") for t in ts) == pytest.approx(
        YEAR_1["claims_annuity"], abs=WON6)
    assert sum(p.claims(t, "DEATH") for t in ts) == pytest.approx(
        YEAR_1["claims_death"], abs=WON6)
    assert sum(p.claims(t, "VOID") for t in ts) == pytest.approx(
        YEAR_1["claims_void"], abs=WON6)
    assert sum(p.expenses(t) for t in ts) == pytest.approx(
        YEAR_1["expenses"], abs=WON6)
    assert sum(p.claim_expenses(t) for t in ts) == pytest.approx(
        YEAR_1["claim_expenses"], abs=WON6)
    assert sum(p.commissions(t) for t in ts) == pytest.approx(
        YEAR_1["commissions"], abs=WON6)
    assert sum(p.net_cf(t) for t in ts) == pytest.approx(YEAR_1["net_cf"], abs=WON6)
    assert sum(p.pols_if(t) for t in ts) > sum(p.pols_act(t) for t in ts)


# The notes' "Undiscounted totals, t = 0 ... 600", to the four decimals it displays.  These
# are sums of the whole result_cf() frame, so the maturity row is inside them.
TOTALS = {
    "pols_if": 343.1313,
    "pols_act": 341.3953,
    "pols_healthy": 330.6077,
    "pols_light": 10.7877,
    "pols_care": 1.7360,
    "premiums": 973533.0572,
    "claims_lump": 268065.6927,
    "claims_annuity": 546912.1402,
    "claims_dementia": 0.0000,
    "claims_death": 326783.9323,
    "claims_lapse": 70149.7799,
    "claims_void": 0.0073,
    "claims_maturity": 0.0000,
    "expenses": 135756.2503,
    "claim_expenses": 3774.5847,
    "commissions": 70945.8826,
    "net_cf": -448855.2128,
}


def test_the_undiscounted_totals_over_the_whole_projection(kr_ltc_anchor):
    """Every column total the notes print, off ``result_cf()`` itself.

    Reading them off the published frame rather than off the cells is deliberate: it is the
    frame a user consumes, and a column that had quietly stopped being published would fail
    here rather than pass by not being looked at.
    """
    p = kr_ltc_anchor
    totals = p.result_cf().sum()
    assert set(totals.index) == set(TOTALS)
    for column, value in TOTALS.items():
        assert totals[column] == pytest.approx(value, abs=WON4), column


# The notes' "Decrement and state totals over the whole projection", to twelve decimals.
DECREMENT_TOTALS = {
    "pols_entry_care": 0.026808014544,
    "pols_void": 0.000000626279,
    "pols_death": 0.354308072159,
    "pols_death_act": 0.337733821029,
    "pols_death_care": 0.016574251130,
    "pols_lapse": 0.435534876925,
    "ann_count": 1.453879542900,
    "ann_tests": 0.099011476675,
}


def test_the_decrement_and_state_totals(kr_ltc_anchor):
    """The cohort's whole fifty-year history, per policy issued, to twelve decimals.

    Over fifty years only 2.68% of the cohort is ever certified at the benefit grade,
    against 43.6% who lapse and 35.4% who die.  The split of the deaths matters and is
    asserted with the total: 0.0166 of the 0.3543 die **in** the care state and are paid
    nothing, the rest die uncertified and are paid the 계약자적립액.  ``ann_count`` against
    ``ann_tests`` is the monthly instalment against the annual proof of life, and the ratio
    of about fifteen is what the claim-expense basis turns on.
    """
    p = kr_ltc_anchor
    ts = range(p.proj_len())
    actual = {
        "pols_entry_care": sum(p.pols_entry_care(t) for t in ts),
        "pols_void": sum(p.pols_void(t) for t in ts),
        "pols_death": sum(p.pols_death(t) for t in ts),
        "pols_death_act": sum(p.pols_death_act(t) for t in ts),
        "pols_death_care": sum(p.pols_death_care(t) for t in ts),
        "pols_lapse": sum(p.pols_lapse(t) for t in ts),
        "ann_count": sum(p.ann_count(t) for t in ts),
        "ann_tests": sum(p.ann_tests(t) for t in ts),
    }
    for name, value in DECREMENT_TOTALS.items():
        assert actual[name] == pytest.approx(value, abs=COUNT), name
    assert p.pols_if(600) == pytest.approx(0.210156424636, abs=COUNT)
    assert actual["pols_death"] == pytest.approx(
        actual["pols_death_act"] + actual["pols_death_care"], abs=COUNT)
    # Certified, lapsed, dead and matured: the four exits, and they close on one policy.
    assert (actual["pols_death"] + actual["pols_lapse"] + actual["pols_void"]
            + p.pols_if(600)) == pytest.approx(1.0, abs=1e-12)


# The notes' "Present values at the 예정이율 of 2.0%", to the four decimals it displays.
# The model does not publish these; they are the calibration check that the premium, the
# incidence basis and the expense basis are mutually consistent.
PRESENT_VALUES = {
    "premiums": 814356.0041,
    "claims_lump": 120884.7459,
    "claims_annuity": 253930.5911,
    "claims_death": 166819.3187,
    "claims_lapse": 38211.9050,
    "claims_void": 0.0073,
    "expenses": 97088.7515,
    "claim_expenses": 1746.6060,
    "commissions": 66187.8032,
    "net_cf": 69486.2754,
}


def test_the_present_values_at_the_yejeong_iyul(kr_ltc_anchor):
    """The notes' present values, and the two ratios the whole basis is calibrated to.

    The 46.03% benefit ratio is what the anchor cell's [S2]-derived ₩5,600 premium buys on
    this model's own basis, and the 20.26% expense ratio is what ``expense_maint`` was set
    to reach — against the 20.68% loading that ``net_prem_ratio()`` implies from the
    published 환급률 progression and the published 예정이율 between them.  A change to the
    expense basis that left the cash flows looking plausible would move the second ratio off
    its calibration target and fail here.
    """
    p = kr_ltc_anchor
    j = (1.0 + p.prem_int_rate) ** (1.0 / 12.0) - 1.0
    df = p.result_cf()
    discount = pd.Series([(1.0 + j) ** -t for t in df.index], index=df.index)
    for column, value in PRESENT_VALUES.items():
        assert (df[column] * discount).sum() == pytest.approx(value, abs=WON4), column
    pv_prem = (df["premiums"] * discount).sum()
    pv_ben = ((df["claims_lump"] + df["claims_annuity"]) * discount).sum()
    pv_exp = ((df["expenses"] + df["claim_expenses"] + df["commissions"])
              * discount).sum()
    assert pv_ben / pv_prem == pytest.approx(0.4602598067, abs=5e-9)
    assert pv_exp / pv_prem == pytest.approx(0.2026425297, abs=5e-9)
    assert pv_benefit_over_premium(p) == pytest.approx(0.4602598067, abs=5e-9)
    # The nine printed lines re-add to net_cf: claims_dementia and claims_maturity are nil.
    outgo = sum(PRESENT_VALUES[c] for c in (
        "claims_lump", "claims_annuity", "claims_death", "claims_lapse", "claims_void",
        "expenses", "claim_expenses", "commissions"))
    assert PRESENT_VALUES["premiums"] - outgo == pytest.approx(
        PRESENT_VALUES["net_cf"], abs=1e-3)


def test_what_the_numbers_say(kr_ltc_anchor):
    """The notes' closing paragraph, asserted rather than described.

    This contract prefunds a cost that essentially does not arise until the block is old.
    Year-1 benefit outgo is ₩18.87 against ₩64,670 of premium — 0.029% — and 39.1% of
    lifetime benefit outgo falls at attained 만나이 85 or over, 63.3% at 80 or over, on a
    contract the 90세만기 truncates at exactly the band with the highest certification rate
    of all.  A model that had turned the prevalence into a claim frequency would show a
    year-1 ratio two or three orders of magnitude larger and would still look plausible row
    by row.
    """
    p = kr_ltc_anchor
    year1_benefit = sum(p.claims(t, "LUMP") + p.claims(t, "ANNUITY") for t in range(12))
    year1_premium = sum(p.premiums(t) for t in range(12))
    assert year1_benefit == pytest.approx(18.87, abs=5e-3)
    assert year1_benefit / year1_premium == pytest.approx(0.00029, abs=5e-6)
    benefit = [p.claims(t, "LUMP") + p.claims(t, "ANNUITY") for t in range(p.proj_len())]
    total = sum(benefit)
    assert total == pytest.approx(814977.8329, abs=WON4)
    over_85 = sum(b for t, b in enumerate(benefit) if p.age(t) >= 85)
    over_80 = sum(b for t, b in enumerate(benefit) if p.age(t) >= 80)
    assert over_85 / total == pytest.approx(0.391, abs=5e-4)
    assert over_80 / total == pytest.approx(0.633, abs=5e-4)
    assert p.prev_rate_at(85) == pytest.approx(0.205, abs=5e-4)
    assert first_entry_rate(p, 85) == pytest.approx(0.0070, abs=5e-5)
    assert first_entry_rate(p, 85) / first_entry_rate(p, 65) == pytest.approx(
        30.0, abs=0.5)
    ts = range(p.proj_len())
    assert sum(p.pols_entry_care(t) for t in ts) == pytest.approx(0.0268, abs=5e-5)
    assert sum(p.pols_lapse(t) for t in ts) == pytest.approx(0.436, abs=5e-4)
    assert sum(p.pols_death(t) for t in ts) == pytest.approx(0.354, abs=5e-4)


def test_the_ganbyeong_yeongeum_is_two_thirds_of_the_benefit(tmp_path):
    """₩546,912 of annuity against ₩268,066 of lump sum, and without it ``net_cf`` turns.

    The optional rider is two thirds of the anchor cell's benefit outgo even though the lump
    sum is the main contract, which is why the post-onset survival basis matters here in a
    way it does not on the cancer chassis.  On a lump-sum-only run of the same cell,
    undiscounted benefit outgo is ₩268,066 and ``net_cf`` turns **positive** at +₩101,027 —
    the whole of this contract's economic content sits in the module whose central
    assumption nobody publishes.
    """
    model = variant_model(tmp_path, "LTC_KR_S_noann", annuity_on=False)
    try:
        q = model.Projection[1]
        assert q.annuity_on() is False
        assert q.ann_amount_at(0) == 0.0
        assert q.ann_count(120) == 0.0 and q.ann_pay(120) == 0.0
        assert q.ann_tests(120) == 0.0
        assert q.check_ann_ledger() is True          # vacuously, and still published
        totals = lifetime(q)
        assert totals["claims_annuity"] == 0.0
        assert totals["claims_lump"] == pytest.approx(268065.6927, abs=WON4)
        assert totals["net_cf"] == pytest.approx(101027.2717, abs=WON4)
        assert totals["net_cf"] > 0.0
    finally:
        model.close()
    assert 546912.1402 / 814977.8329 == pytest.approx(0.671, abs=5e-4)


# ---------------------------------------------------------------------------
# The product's own invariants, recursions and boundaries


def test_the_processing_order_is_certification_then_mortality_then_lapse(kr_ltc_anchor):
    """``pols_if_at`` reads the month in order, and the order is asserted by its effects.

    The order is **certification, then mortality, then lapse**.  What distinguishes it from
    any other order is *which* population each decrement is taken from, so the test checks a
    quantity that would differ if the order changed: between ``BEF_DECR`` and ``BEF_LAPSE``
    exactly the deaths and the voided certifications have gone, and between ``BEF_LAPSE``
    and the next month's opening count exactly the lapses have.  A model that lapsed before
    it certified would take the month's certifications out of a smaller pool and put fewer
    lives into the care state; a model that lapsed before mortality would pay a surrender
    value to lives that had already died.
    """
    p = kr_ltc_anchor
    for t in (0, 1, 3, 12, 240, 599):
        assert p.pols_if_at(t, "BEF_DECR") == p.pols_if(t)
        assert p.pols_if_at(t, "AFT_DECR") == p.pols_if(t + 1)
        assert p.pols_if(t) - p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_death(t) + p.pols_void(t), abs=1e-15)
        assert p.pols_if_at(t, "BEF_LAPSE") - p.pols_if(t + 1) == pytest.approx(
            p.pols_lapse(t), abs=1e-15)
        assert p.pols_if(t) > p.pols_if_at(t, "BEF_LAPSE") > p.pols_if(t + 1)
    # Certification is taken from the start-of-month counts, before any decrement.
    for t in (0, 60, 300):
        assert p.pols_entry_light(t) == pytest.approx(
            p.pols_healthy(t) * p.inc_rate_light_mth(t), rel=FULL)
        assert p.pols_entry_care_direct(t) == pytest.approx(
            p.pols_healthy(t) * p.inc_rate_direct_mth(t), rel=FULL)
        assert p.pols_entry_care_prog(t) == pytest.approx(
            p.pols_light(t) * p.prog_rate_mth(t), rel=FULL)
    # Mortality is taken from the mid-month counts, lapse from the mortality survivors.
    for t in (0, 60, 300):
        assert p.pols_death_act(t) == pytest.approx(
            p.pols_healthy_mid(t) * p.mort_rate_mth(t)
            + p.pols_light_mid(t) * p.mort_rate_light_mth(t), rel=FULL)
        assert p.pols_death_care(t) == pytest.approx(
            p.pols_care_mid(t) * p.mort_rate_care_mth(t), rel=FULL)
        assert p.pols_lapse(t) == pytest.approx(
            (p.pols_healthy_mid(t) * (1.0 - p.mort_rate_mth(t))
             + p.pols_light_mid(t) * (1.0 - p.mort_rate_light_mth(t)))
            * p.lapse_rate_mth(t), rel=FULL)
    with pytest.raises(FormulaError):
        p.pols_if_at(12, "NOWHERE")


def test_the_three_compartments_roll_forward_as_the_notes_write_them(kr_ltc_anchor):
    """The three recursions, term by term, at four points spread over the projection.

    ``h`` and ``l_L`` carry mortality **and** lapse; ``l_C`` carries mortality alone.  The
    lives leaving ``h`` by direct certification leave whether the certification triggers the
    benefit or voids it inside the 보장개시일 window, which is why the same term serves both
    and why ``pols_void`` never appears in ``l_C``.
    """
    p = kr_ltc_anchor
    for t in (0, 5, 200, 500):
        assert p.pols_healthy_mid(t) == pytest.approx(
            p.pols_healthy(t) - p.pols_entry_light(t) - p.pols_entry_care_direct(t),
            rel=FULL)
        assert p.pols_light_mid(t) == pytest.approx(
            p.pols_light(t) + p.pols_entry_light(t) - p.pols_entry_care_prog(t),
            rel=FULL)
        assert p.pols_care_mid(t) == pytest.approx(
            p.pols_care(t) + p.pols_entry_care(t), rel=FULL)
        assert p.pols_healthy(t + 1) == pytest.approx(
            p.pols_healthy_mid(t) * (1.0 - p.mort_rate_mth(t))
            * (1.0 - p.lapse_rate_mth(t)), rel=FULL)
        assert p.pols_light(t + 1) == pytest.approx(
            p.pols_light_mid(t) * (1.0 - p.mort_rate_light_mth(t))
            * (1.0 - p.lapse_rate_mth(t)), rel=FULL)
        assert p.pols_care(t + 1) == pytest.approx(
            p.pols_care_mid(t) * (1.0 - p.mort_rate_care_mth(t)), rel=FULL)
    assert p.pols_act(0) == 1.0 and p.pols_if(0) == 1.0
    for t in (0, 5, 200, 500, 600):
        assert p.pols_act(t) == pytest.approx(
            p.pols_healthy(t) + p.pols_light(t), rel=FULL)
        assert p.pols_if(t) == pytest.approx(p.pols_act(t) + p.pols_care(t), rel=FULL)


def test_the_in_force_roll_forward_names_every_decrement(long_term_care):
    """Deaths, lapses, voided certifications and the maturity are the only ways out.

    Nothing else may move ``pols_if``, and the identity is asserted directly, on every
    shipped model point, rather than only through the check cell that computes it.  A lapse
    applied to the care population, a voided certification left inside the block, or a
    maturity not removed on the last row all show up here.
    """
    for point_id in long_term_care.Data.model_point_table().index:
        p = long_term_care.Projection[point_id]
        n = p.proj_len()
        for t in (0, 1, 11, 12, n // 2, n - 2, n - 1):
            assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(
                p.pols_death(t) + p.pols_lapse(t) + p.pols_void(t)
                + p.pols_maturity(t), abs=1e-12), (point_id, t)
        assert p.pols_maturity(n - 1) == p.pols_if(n - 1)
        assert p.pols_maturity(n - 2) == 0.0
        assert p.pols_if(n) == 0.0


def test_in_force_is_a_decreasing_probability(long_term_care):
    """One policy at outset, never more, and never rising, on every shipped model point."""
    for point_id in long_term_care.Data.model_point_table().index:
        p = long_term_care.Projection[point_id]
        assert p.pols_if(0) == 1.0
        for t in range(0, p.proj_len(), 24):
            assert 0.0 <= p.pols_if(t) <= 1.0
            assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15


def test_the_bojang_gaesiil_boundary_is_the_month_and_not_the_day_after(kr_ltc_anchor):
    """``pols_entry_care`` is nil for ``t < W`` and ``pols_void`` nil for ``t >= W``.

    They partition the same gross inflow — the two together are always ``n_D + n_P*`` — and
    the boundary is inclusive at ``t = W``, the 보장개시일 being 「계약일부터 그 날을 포함하여
    90일이 지난 날의 다음 날」.  A model that let a certification inside the window sit in the
    block waiting for the window to close would leave the sum short in the early months and
    long later.
    """
    p = kr_ltc_anchor
    for t in range(0, 24):
        gross = p.pols_entry_care_direct(t) + p.pols_entry_care_prog(t)
        assert p.pols_entry_care(t) + p.pols_void(t) == pytest.approx(gross, rel=FULL)
        if t < p.wait_mths():
            assert p.pols_entry_care(t) == 0.0 and p.pols_void(t) > 0.0
        else:
            assert p.pols_void(t) == 0.0 and p.pols_entry_care(t) > 0.0
    assert p.claims(0, "VOID") > 0.0                 # one month's premium already paid
    assert p.claims(1, "VOID") > 0.0 and p.claims(2, "VOID") > 0.0
    assert p.claims(3, "VOID") == 0.0
    for t in (0, 1, 2):
        assert p.claims(t, "VOID") == pytest.approx(
            p.cum_prem_pp(t + 1) * p.pols_void(t), rel=FULL)


def test_the_gamaek_gigan_is_a_step_and_it_is_frozen_at_certification(kr_ltc_anchor):
    """``red_factor`` steps once, at ``red_mths``, and it is read at ``s`` and never at ``t``.

    ``1 - (1 - red_fraction) x disease_share`` = 0.525 inside the window and 1 outside it.
    The 약관 test is on the **cause** and not on the grade, which is why the blended factor
    is 0.525 and not 0.50: an 상해/재해-caused certification is paid in full, and the
    relative frequency of the two is [std].  ``ann_amount_at(s)`` carries the factor of the
    **certification** month, so a cohort certified inside the window is still carried at
    ₩207,495.74 twelve months later while a cohort certified at month 12 is at ₩395,229.98.
    """
    p = kr_ltc_anchor
    assert p.red_fraction == 0.50 and p.disease_share == 0.95
    for t in range(0, p.red_mths()):
        assert p.red_factor(t) == pytest.approx(1.0 - 0.5 * 0.95, rel=FULL)
    for t in (12, 13, 240, 599):
        assert p.red_factor(t) == 1.0
    # frozen at s: the month-3 cohort keeps its factor for the whole life of its annuity
    assert p.ann_amount_at(3) == pytest.approx(0.525 * p.ann_amount_at(12), rel=FULL)
    assert p.ann_amount_at(11) == pytest.approx(p.ann_amount_at(3), rel=FULL)
    # and the lump sum takes the factor of the month it is paid in, which is the same month
    for t in (3, 11, 12, 120):
        assert p.claims(t, "LUMP") == pytest.approx(
            p.lump_amount() * p.red_factor(t) * p.pols_entry_care(t), rel=FULL)


def test_the_annuity_ledger_is_a_cohort_sum_with_a_guarantee_and_a_cap(kr_ltc_anchor):
    """The ledger, rebuilt from the notes' own formula: the ``u = 0`` term, ``g_A``, ``n_A``.

    ``ann_count(t)`` sums ``n_C(t - u)`` over ``u = 0 ... min(t, n_A - 1)`` with weight 1
    inside the twelve-month guarantee and ``S_C(s, s + 12 floor(u/12))`` after it, so the
    survival test is **annual** while the instalments are **monthly**.  The first instalment
    falls in the month of certification, so the ``u = 0`` term is ``n_C(t)`` itself, and
    nothing is paid on the maturity row ``t = proj_len() - 1`` or after it.
    """
    p = kr_ltc_anchor
    n_a, g_a = p.annuity_max_mths(), p.annuity_guar_mths()
    assert (n_a, g_a) == (120, 12)
    for t in (3, 12, 130, 400, 599):
        built_count = 0.0
        built_pay = 0.0
        for u in range(0, min(t, n_a - 1) + 1):
            s = t - u
            weight = 1.0 if u < g_a else p.care_surv(s, s + 12 * (u // 12))
            built_count += p.pols_entry_care(s) * weight
            built_pay += p.ann_amount_at(s) * p.pols_entry_care(s) * weight
        assert p.ann_count(t) == pytest.approx(built_count, rel=FULL), t
        assert p.ann_pay(t) == pytest.approx(built_pay, rel=FULL), t
        assert p.claims(t, "ANNUITY") == pytest.approx(p.ann_pay(t), rel=FULL)
    # Inside the guarantee every weight is exactly 1; the first release is at u = 12.
    for u in range(0, g_a):
        assert (1.0 if u < g_a else 0.0) == 1.0
    assert p.care_surv(3, 3 + 12) < 1.0
    # The cap and the maturity truncation bind jointly.
    assert p.ann_count(p.proj_len() - 1) == 0.0
    assert p.ann_pay(p.proj_len() - 1) == 0.0
    assert p.ann_count(500) == pytest.approx(
        sum(p.pols_entry_care(500 - u)
            * (1.0 if u < g_a else p.care_surv(500 - u, 500 - u + 12 * (u // 12)))
            for u in range(0, n_a)), rel=FULL)
    assert p.pols_entry_care(500 - n_a) > 0.0        # a cohort just outside the window
    # The annual proof-of-life test falls on the anniversary of the 진단확정일, not monthly.
    assert p.ann_tests(14) == 0.0
    assert p.ann_tests(15) == pytest.approx(
        p.pols_entry_care(3) * p.care_surv(3, 15), rel=FULL)


def test_the_account_and_the_surrender_value_have_two_branches_that_meet(kr_ltc_anchor):
    """``av_pp`` accumulates net premiums to 납입완료 and runs off on the sourced anchors.

    ``net_prem_ratio()`` is **derived** — the fraction that, accumulated at the 예정이율 over
    the paying period, reproduces the sourced 계약자적립액 at 납입완료 — so the join closes by
    construction rather than by luck.  ``check_av_continuity()`` is the cell that says so,
    and it fails the moment someone replaces the derivation with a round number.
    """
    p = kr_ltc_anchor
    n = p.prem_period_mths()
    assert p.net_prem_ratio() == pytest.approx(
        p.av_ratio_at(0.0) * n / p.prem_accum_factor(n), rel=FULL)
    for t in (0, 1, 12, 120, 239, 240):
        assert p.av_pp(t) == pytest.approx(
            p.net_prem_ratio() * p.premium_mth_pp() * p.prem_accum_factor(t), rel=FULL)
    for t in (241, 360, 480, 600):
        assert p.av_pp(t) == pytest.approx(
            p.av_ratio_at((t - n) / (p.proj_len() - 1 - n))
            * p.premium_mth_pp() * n, rel=FULL)
    assert p.av_pp(600) == 0.0                       # av_ratio_at(1) = 0, no 만기환급금
    assert p.prem_accum_factor(0) == 0.0
    # The four sourced anchors of av_table.csv, and the 환급률 they were built from.
    assert p.av_ratio_at(0.0) == 0.974
    assert p.av_ratio_at(0.333333) == 1.088
    assert p.av_ratio_at(0.666667) == 1.010
    assert p.av_ratio_at(1.0) == 0.0
    for fraction, hwangeumnyul in ((0.0, 0.487), (0.333333, 0.544), (0.666667, 0.505)):
        assert 0.5 * p.av_ratio_at(fraction) == pytest.approx(hwangeumnyul, abs=5e-4)


def test_the_three_surrender_value_forms_differ_in_which_side_they_attach_to(
        long_term_care):
    """미지급형, 납입중50%해약환급금지급형 and 표준형, on the three points that carry them.

    They are **different products, not variants**, and three of the four Korean forms differ
    only in which side of 납입완료 the 50% attaches to.  The anchor cell pays nothing during
    and half after; model point 6 pays half during and the whole account after; model point 7
    is the 표준형 and pays the account less the 해약공제액 from year 1.  Reading 「50%」
    without reading which side it attaches to puts the cliff upside down, which is why the
    form is a model point field and not a switch on a ratio.
    """
    p1 = long_term_care.Projection[1]
    assert p1.cv_form() == "mijigeup"
    assert p1.cv_pp(239) == 0.0
    assert p1.cv_pp(240) == pytest.approx(0.5 * p1.av_pp(240), rel=FULL)

    p6 = long_term_care.Projection[6]
    assert p6.cv_form() == "half_during"
    n6 = p6.prem_period_mths()
    assert p6.cv_pp(n6 - 1) == pytest.approx(0.5 * p6.av_pp(n6 - 1), rel=FULL)
    assert p6.cv_pp(n6) == pytest.approx(p6.av_pp(n6), rel=FULL)
    assert p6.cv_pp(n6 - 1) > 0.0                    # not nil during, unlike 미지급형

    p7 = long_term_care.Projection[7]
    assert p7.cv_form() == "pyojun"
    n_chg = 12 * min(p7.surr_chg_years, p7.prem_period_years())
    assert n_chg == 84                               # the seven-year 해약공제기간 cap
    assert p7.surr_chg_pp(0) == pytest.approx(
        13.0 * p7.premium_mth_pp(), rel=FULL)
    assert p7.surr_chg_pp(n_chg - 1) > 0.0
    assert p7.surr_chg_pp(n_chg) == 0.0
    for t in (0, 40, 84, 120, 200):
        assert p7.cv_pp(t) == pytest.approx(
            max(p7.av_pp(t) - p7.surr_chg_pp(t), 0.0), rel=FULL)
    assert p7.cv_pp(120) > 0.0                       # a normal surrender value, from year 1


def test_claims_re_add_to_the_seven_published_kinds(kr_ltc_anchor):
    """``claims(t)`` with no kind is exactly the seven splits, and an unknown kind raises.

    There is no ``claims`` **column** in ``result_cf()`` — an aggregate beside its own parts
    would stop the columns summing to ``net_cf`` — but the ``claims(t, kind)`` cells stays,
    and its no-kind branch has to be the sum of the parts the statement publishes.
    """
    p = kr_ltc_anchor
    kinds = ("LUMP", "ANNUITY", "DEMENTIA", "DEATH", "LAPSE", "VOID", "MATURITY")
    for t in (0, 1, 3, 12, 240, 540, 600):
        assert p.claims(t) == pytest.approx(
            sum(p.claims(t, kind) for kind in kinds), rel=FULL)
    assert "claims" not in p.result_cf().columns
    with pytest.raises(FormulaError):
        p.claims(0, "NOPE")


def test_four_columns_are_zero_on_purpose(kr_ltc_anchor, long_term_care):
    """``claims_maturity`` always, ``claims_lapse`` for 240 months, ``claims_dementia`` off.

    A column that is absent and a column that is zero say different things, and only one of
    them can be tested.  ``claims_maturity`` is zero at every ``t`` on every model point —
    「이 상품은 순수보장성보험으로 … 만기환급금이 없습니다」 — and publishing the zeros of
    ``claims_lapse`` through the whole premium-paying period is what makes the cliff visible
    as a cliff.  ``claims_void`` is **not** zero and is carried in its own column because a
    voided cover is a different mechanism from a refused claim.
    """
    p = kr_ltc_anchor
    df = p.result_cf()
    assert (df["claims_maturity"] == 0.0).all()
    assert (df["claims_dementia"] == 0.0).all()      # the rider is off on the anchor
    assert (df["claims_lapse"].iloc[:240] == 0.0).all()
    assert df["claims_lapse"].iloc[240] > 0.0
    assert df["claims_void"].sum() > 0.0
    assert df["claims_void"].sum() == pytest.approx(0.0073, abs=WON4)
    assert p.pols_maturity(600) > 0.0 and p.claims(600, "MATURITY") == 0.0
    riderless = [pid for pid in long_term_care.Data.model_point_table().index
                 if not long_term_care.Projection[pid].dementia_rider()]
    assert len(riderless) == 7
    for pid in long_term_care.Data.model_point_table().index:
        q = long_term_care.Projection[pid]
        assert (q.result_cf()["claims_maturity"] == 0.0).all(), pid


def test_the_last_row_is_the_maturity_instant_and_pays_nothing(kr_ltc_anchor):
    """``t = proj_len() - 1`` carries an in-force count and every cash flow zero.

    There is no 만기환급금 on a 순수보장성 contract, so the maturity is a decrement with no
    payment attached — and it is still a maturity, which is why the count is published.
    """
    p = kr_ltc_anchor
    n = p.proj_len()
    row = p.result_cf().loc[n - 1]
    assert row["pols_if"] == pytest.approx(0.210156424636, abs=COUNT)
    for column in ("premiums", "claims_lump", "claims_annuity", "claims_dementia",
                   "claims_death", "claims_lapse", "claims_void", "claims_maturity",
                   "expenses", "claim_expenses", "commissions", "net_cf"):
        assert row[column] == 0.0, column
    assert p.pols_maturity(n - 1) == p.pols_if(n - 1)


def test_the_model_point_table_covers_the_products_variants(long_term_care):
    """Nine model points, both sexes, every optional module and every 등급 gate but one.

    The shipped table is what the conventions suite sweeps and what the sensitivities are
    read against, so what it covers is a property of the product rather than of the tests:
    issue ages 30 to 70, maturities 90 / 95 / 100, gates ``g1`` through ``g6``, all three
    surrender-value forms, both lapse vectors, the 간병연금 in both positions, the 치매 rider
    in both, the 간편심사 loading, and the 우체국-style 180-day / two-year combination.
    """
    table = long_term_care.Data.model_point_table()
    assert len(table) == 9
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["cv_form"]) == {"mijigeup", "half_during", "pyojun"}
    assert set(table["lapse_form"]) == {"mujihae", "pyojun"}
    assert {"g1", "g2", "g5", "g6"} <= set(table["benefit_grade"])
    assert set(table["annuity_on"]) == {True, False}
    assert set(table["dementia_rider"]) == {True, False}
    assert set(table["uw_loading"]) == {1.0, 1.4}
    assert table["issue_age"].min() == 30 and table["issue_age"].max() == 70
    assert set(table["term_age"]) == {90, 95, 100}
    assert set(table["wait_mths"]) == {3, 6}
    assert set(table["red_mths"]) == {12, 24}
    assert set(table["prem_mode"]) == {"monthly"}


# ---------------------------------------------------------------------------
# The notes' known modeling pitfalls, one test each


def test_pitfall_injeongryul_is_a_prevalence_not_an_incidence(kr_ltc_anchor):
    """인정률 is a point-in-time proportion, and the ratio to incidence is not a constant.

    10.85% of the 65+ population held a certification at end-2024; 1·2등급 prevalence at
    만나이 65 is 0.246% and the model's own first-entry rate at the same age is 0.0234%.  The
    prevalence is **10.5 times** the incidence at 65, 6.5 times at 75 and 3.8 times at 85.
    Multiplying an 인정률 by a benefit amount, or treating it as an annual claim frequency,
    is the commonest error in a Korean long-term-care model, and using one ratio to convert
    it at every age is the second commonest.
    """
    p = kr_ltc_anchor
    assert p.prev_care_at(65) == pytest.approx(0.00246381, abs=5e-9)
    assert first_entry_rate(p, 65) == pytest.approx(0.00023429, abs=5e-9)
    ratios = {x: p.prev_care_at(x) / first_entry_rate(p, x) for x in (65, 75, 85)}
    assert ratios[65] == pytest.approx(10.5, abs=0.05)
    assert ratios[75] == pytest.approx(6.5, abs=0.05)
    assert ratios[85] == pytest.approx(3.8, abs=0.05)
    assert ratios[65] > ratios[75] > ratios[85]      # not a constant
    # A prevalence is dimensionless; the identity adds two quantities that are rates.
    x = 65
    assert p.inflow_care_at(x) == pytest.approx(
        p.prev_care_slope_at(x)
        + p.prev_care_at(x) * (p.mort_force_care_at(x) - p.mort_force_avg_at(x)),
        rel=FULL)


def test_pitfall_the_excess_mortality_term_and_mu_bar_are_not_refinements():
    """Dropping ``mu_C`` cuts lump-sum claims 37.7%; dropping ``mu_bar`` inflates inflow 8.2%.

    A rising prevalence understates entry because the compartment it measures is being
    drained by an excess mortality the population around it does not carry.  Setting
    ``care_mort_mult`` to 1 — the "there is no impaired-life table so leave it alone" choice
    — drops the term entirely.  And ``mu_bar`` rather than zero is what turns a *count*
    identity into a *proportion* identity: prevalence is measured against a **living**
    population, so the comparison is against the population's own average force.  The two
    errors run in opposite directions, which is why neither is a refinement.
    """
    model = mx.read_model(MODEL_DIR, name="LTC_KR_S_nomort")
    try:
        p = model.Projection[1]
        base = lifetime(p)
        x = 65
        with_bar = p.inflow_care_at(x)
        without_bar = (p.prev_care_slope_at(x)
                       + p.prev_care_at(x) * p.mort_force_care_at(x))
        assert without_bar / with_bar == pytest.approx(1.082, abs=0.002)
        slope_share = p.prev_care_slope_at(x) / with_bar
        assert slope_share == pytest.approx(0.838, abs=0.002)
        assert 1.0 - slope_share == pytest.approx(0.162, abs=0.002)

        model.Projection.care_mort_mult = 1.0
        model.Projection.clear_all()
        q = model.Projection[1]
        assert q.mort_force_care_at(65) == pytest.approx(q.mort_force_at(65), rel=FULL)
        without = lifetime(q)
        assert without["claims_lump"] == pytest.approx(166937.5552, abs=WON4)
        assert 1.0 - without["claims_lump"] / base["claims_lump"] == pytest.approx(
            0.377, abs=0.001)
        assert 1.0 - without["claims_annuity"] / base["claims_annuity"] == pytest.approx(
            0.147, abs=0.001)
        assert without["entries"] == pytest.approx(0.016695, abs=5e-7)
    finally:
        model.close()


def test_pitfall_p_c_prime_needs_the_full_product_rule(kr_ltc_anchor):
    """``s_G'(x) P(x)`` is negative over most of the range and dropping it overstates entry.

    ``P_C = s_G(x) P(x)`` and the severe share is **falling with age** over most of the
    range, so the naive ``s_G(x) P'(x)`` is 1.82x the correct ``P_C'`` at 만나이 65 and 1.19x
    at 75.  The visible symptom of getting it right is that ``claims_lump`` **falls** between
    ``t = 239`` and ``t = 240`` — 139.1227 to 101.8715 — where the 1·2등급 share is at its
    steepest: the claim rate on a severe threshold does not rise monotonically with age even
    though the all-grade certification rate does.
    """
    p = kr_ltc_anchor
    for x, ratio in ((65, 1.82), (75, 1.19)):
        naive = p.share_ge_at("g2", x) * p.prev_slope_at(x)
        assert naive / p.prev_care_slope_at(x) == pytest.approx(ratio, abs=0.005), x
    assert p.prev_care_slope_at(65) == pytest.approx(
        p.share_slope_at("g2", 65) * p.prev_rate_at(65)
        + p.share_ge_at("g2", 65) * p.prev_slope_at(65), rel=FULL)
    assert p.share_slope_at("g2", 65) < 0.0
    assert p.share_slope_at("g2", 75) < 0.0
    assert p.share_ge_at("g2", 72) == pytest.approx(0.1270, abs=5e-5)
    assert p.share_ge_at("g2", 82) == pytest.approx(0.1110, abs=5e-5)
    assert p.claims(239, "LUMP") == pytest.approx(139.1227, abs=WON4)
    assert p.claims(240, "LUMP") == pytest.approx(101.8715, abs=WON4)
    assert p.claims(240, "LUMP") < p.claims(239, "LUMP")
    assert p.prev_rate_at(60) < p.prev_rate_at(70)   # while the all-grade rate rises


def test_pitfall_the_gamaek_is_frozen_and_must_not_be_re_tested(long_term_care):
    """Re-testing the 감액 at each instalment overstates annuity outgo, and by how much.

    「최초 진단 확정일을 기준으로 … 그 이후에 도래하는 매년 진단 확정일이 계약일부터 2년 이상에
    해당하더라도 … 지급액은 변경되지 않습니다」.  A model that re-tests it pays the full amount
    from month 12 onward to cohorts certified in the first year, overstating annuity outgo by
    ₩64.78 on the anchor cell (+0.012%), by ₩596.60 at issue age 60 (+0.097%) and by
    ₩1,065.24 at issue age 70 (+0.315%).  It is nearly worthless at the bottom of the
    issue-age range and first-order at the top, which is why the anchor cell is not the only
    test target here.  Evaluate ``red_factor`` at ``s``, never at ``t``.
    """
    expected = {1: (64.78, 0.00012), 3: (596.60, 0.00097), 7: (1065.24, 0.00315)}
    for point_id, (excess, relative) in expected.items():
        p = long_term_care.Projection[point_id]
        # the cash-flow months, t = 0 ... proj_len() - 2; the last row is the maturity
        # month and pays nothing, so the counterfactual must not reach it either
        n = p.proj_len() - 1
        correct = sum(p.claims(t, "ANNUITY") for t in range(n))
        re_tested = 0.0
        for t in range(n):
            for u in range(0, min(t, p.annuity_max_mths() - 1) + 1):
                s = t - u
                weight = (1.0 if u < p.annuity_guar_mths()
                          else p.care_surv(s, s + 12 * (u // 12)))
                amount = p.ann_amount_at(s) / p.red_factor(s) * p.red_factor(t)
                re_tested += amount * p.pols_entry_care(s) * weight
        assert re_tested - correct == pytest.approx(excess, abs=5e-3), point_id
        assert re_tested / correct - 1.0 == pytest.approx(relative, abs=5e-6), point_id


def test_pitfall_the_annuitys_first_instalment_falls_in_the_month_of_certification(
        kr_ltc_anchor):
    """The ``u = 0`` term of the ledger is ``n_C(t)`` itself, not a cohort a year old.

    Deferring the first instalment by twelve months removes roughly a tenth of the annuity
    liability and misdates all of it.  Related and opposite: the instalments are **monthly**
    while the survival test is **annual**, so a model that pays annually gets the amount
    right and the timing wrong, and a model that tests survival monthly gets the timing right
    and the amount wrong.
    """
    p = kr_ltc_anchor
    assert p.pols_entry_care(3) > 0.0
    assert p.ann_count(3) == pytest.approx(p.pols_entry_care(3), rel=FULL)
    assert p.claims(3, "ANNUITY") == pytest.approx(
        p.ann_amount_at(3) * p.pols_entry_care(3), rel=FULL)
    assert p.claims(3, "ANNUITY") > 0.0              # the same month as the lump sum
    assert p.claims(3, "LUMP") > 0.0
    # Monthly instalments against an annual test: every month inside the window is paid.
    for t in range(4, 15):
        assert p.ann_count(t) > p.ann_count(t - 1)
    # Deferring the whole schedule by a year - the same 120 instalments, starting at
    # s + 12 - costs about a tenth of the liability and misdates all of it.
    # the cash-flow months, t = 0 ... proj_len() - 2, the maturity row paying nothing
    n, n_a, g_a = p.proj_len() - 1, p.annuity_max_mths(), p.annuity_guar_mths()
    deferred = 0.0
    for t in range(n):
        for u in range(0, n_a):
            s = t - 12 - u
            if s < 0:
                continue
            weight = (1.0 if u < g_a
                      else p.care_surv(s + 12, s + 12 + 12 * (u // 12)))
            deferred += p.ann_amount_at(s) * p.pols_entry_care(s) * weight
    correct = sum(p.claims(t, "ANNUITY") for t in range(n))
    assert 1.0 - deferred / correct == pytest.approx(0.104, abs=0.002)


def test_pitfall_the_claim_expense_is_per_event_not_per_instalment(kr_ltc_anchor):
    """``ann_tests`` totals 0.0990 against ``ann_count``'s 1.4539, a factor of about fifteen.

    The proof of life the 약관 requires is **annual** — 「매년 진단 확정일에 피보험자의
    주민등록등본을 제출하여야 합니다」 — so the claim-handling expense is charged on the first
    certification, on each annual survival test and on a dementia diagnosis, and never on a
    monthly instalment.  Charging ₩30,000 per instalment would multiply the annuity's claim
    expense by about fifteen.
    """
    p = kr_ltc_anchor
    ts = range(p.proj_len())
    tests = sum(p.ann_tests(t) for t in ts)
    count = sum(p.ann_count(t) for t in ts)
    assert tests == pytest.approx(0.099011476675, abs=COUNT)
    assert count == pytest.approx(1.453879542900, abs=COUNT)
    assert count / tests == pytest.approx(14.68, abs=0.02)
    for t in (3, 12, 15, 300):
        assert p.claim_expenses(t) == pytest.approx(
            p.expense_claim * (p.pols_entry_care(t) + p.ann_tests(t)
                               + p.pols_entry_dem(t)), rel=FULL)
    assert sum(p.claim_expenses(t) for t in ts) == pytest.approx(3774.5847, abs=WON4)
    per_instalment = p.expense_claim * count
    assert per_instalment / sum(p.claim_expenses(t) for t in ts) > 10.0


def test_pitfall_care_state_survival_is_a_partial_product(kr_ltc_anchor, long_term_care):
    """``care_surv`` multiplies term by term; the ratio form divides by zero at the cap.

    ``mort_rate_care`` is ``min(1, 3 q(x))`` and the cap binds from 만나이 **108** on the
    shipped male table and **112** on the female one, so a cumulative product from issue
    underflows to zero from there on and the ratio form divides by zero exactly where the
    tail of a 종신 variant of this liability would live.  It does not bite on any shipped
    model point, which is precisely why it would be found late.
    """
    p = kr_ltc_anchor
    for s, t in ((0, 0), (3, 15), (100, 220), (400, 500)):
        expected = 1.0
        for u in range(s, t):
            expected *= 1.0 - p.mort_rate_care_mth(u)
        assert p.care_surv(s, t) == pytest.approx(expected, rel=FULL), (s, t)
    assert p.care_surv(50, 50) == 1.0
    assert p.care_surv(50, 40) == 1.0                # t <= s is unit, not an error
    # Where the cap binds, and that a cumulative product from issue is already nil there.
    assert 3.0 * p.mort_rate_at_age(107) < 1.0
    assert 3.0 * p.mort_rate_at_age(108) >= 1.0
    assert p.mort_rate_care_mth(12 * (108 - p.issue_age())) == 1.0
    female = long_term_care.Projection[2]
    assert 3.0 * female.mort_rate_at_age(111) < 1.0
    assert 3.0 * female.mort_rate_at_age(112) >= 1.0


def test_pitfall_premium_rides_on_pols_act_never_on_pols_if(kr_ltc_anchor):
    """Charging the whole in-force block overstates lifetime premium by ₩414.65, 0.043%.

    The 납입면제 waives the main contract and every attached rider from the award of
    1·2등급, and waived premiums are treated as paid.  The error is small here only because
    the certification rate at issue age 40 is small, and it is much larger at the top of the
    issue-age range.  Note that it is the *reverse* of the Japanese product's, where the
    waiver fires below the benefit and the band of lives paying nothing and claiming nothing
    is large: here the waiver and the benefit fire on the same event, so the only lives on
    waiver are lives already claiming.
    """
    p = kr_ltc_anchor
    paying = range(p.prem_period_mths())
    on_act = sum(p.premiums(t) for t in paying)
    on_if = sum(p.premium_mth_pp() * p.pols_if(t) for t in paying)
    assert on_act < on_if
    assert on_if - on_act == pytest.approx(414.65, abs=5e-3)
    assert on_if / on_act - 1.0 == pytest.approx(0.00043, abs=5e-6)
    for t in (0, 120, 239):
        assert p.premiums(t) == pytest.approx(
            p.premium_mth_pp() * p.pols_act(t), rel=FULL)
    assert p.premiums(240) == 0.0                    # 비갱신형, a fixed 납입기간
    # Maintenance expense, by contrast, rides on pols_if including lives on waiver.
    for t in (120, 300, 540):
        assert p.expenses(t) == pytest.approx(
            p.expense_maint * p.inflation_factor(t) * p.pols_if(t), rel=FULL)
    # Renewal commission rides on premium, so the waiver stops it too.
    assert p.commissions(120) == pytest.approx(0.03 * p.premiums(120), rel=FULL)
    assert p.commissions(240) == 0.0


def test_pitfall_lapse_must_not_touch_the_care_compartment_and_the_check_wont_say_so(
        kr_ltc_anchor):
    """Lapsing care lives leaves ``claims_annuity`` unchanged and the roll-forward closing.

    The premium is waived and the 약관 bars surrender outright once the annuity has started
    — 「최초 지급사유가 발생한 후에는 이 특약을 해지할 수 없습니다」 — so zero lapse in the
    care state is a **constraint**, not an assumption.  It is also a **silent** error:
    ``claims_annuity`` does not move at all, the ledger being driven by ``n_C`` and
    ``care_surv`` and not by the compartment, and ``check_pols_roll_fwd()`` still closes
    because the roll-forward would be internally consistent.  The only visible effect is
    ₩489.73 of surrender value paid to lives the contract forbids from surrendering, which
    is why ``cv_pp`` and ``pols_lapse`` have to be read together.
    """
    p = kr_ltc_anchor
    # The shipped lapse decrement never draws on the care compartment.
    for t in (120, 300, 540):
        assert p.pols_care(t) > 0.0
        assert p.pols_lapse(t) < p.pols_if(t) * p.lapse_rate_mth(t)
        assert p.pols_lapse(t) == pytest.approx(
            (p.pols_healthy_mid(t) * (1.0 - p.mort_rate_mth(t))
             + p.pols_light_mid(t) * (1.0 - p.mort_rate_light_mth(t)))
            * p.lapse_rate_mth(t), rel=FULL)
        assert p.pols_care(t + 1) == pytest.approx(
            p.pols_care_mid(t) * (1.0 - p.mort_rate_care_mth(t)), rel=FULL)
    # The shadow ledger a lapse-exposed care state would produce, priced at cv_pp.
    shadow, extra = 0.0, 0.0
    for t in range(p.proj_len()):
        mid = shadow + p.pols_entry_care(t)
        survivors = mid * (1.0 - p.mort_rate_care_mth(t))
        lapses = survivors * p.lapse_rate_mth(t)
        extra += p.cv_pp(t) * lapses
        shadow = survivors - lapses
    assert extra == pytest.approx(489.73, abs=5e-3)
    assert p.check_pols_roll_fwd() is True           # and would still be True with the error


def test_pitfall_a_certification_inside_the_window_is_a_decrement_not_a_deferred_claim(
        kr_ltc_anchor):
    """The cover is 무효, the premiums come back, and the life leaves the model.

    「특약을 무효로 하며, 이미 납입한 보험료를 돌려드립니다」.  There is **no cancellation
    option and no revival** here, unlike the cancer chassis, so a model that imports the
    chassis's 90-day cancellation right invents a term this product does not have.  The
    refund is ``cum_prem_pp(t + 1)`` and not ``cum_prem_pp(t)``: premium falls at the start
    of month ``t`` and the void is recognised at the end of it, so a life voided in month 0
    has paid one month and gets it back.  ``claims_void(3)`` is nil for the opposite reason,
    the window having closed.
    """
    p = kr_ltc_anchor
    assert p.pols_void(0) > 0.0 and p.claims(0, "VOID") > 0.0
    assert p.claims(0, "VOID") == pytest.approx(
        p.premium_mth_pp() * p.pols_void(0), rel=FULL)
    assert p.pols_void(3) == 0.0 and p.claims(3, "VOID") == 0.0
    assert p.pols_entry_care(3) > 0.0
    # The voided lives are a decrement: they are in the roll-forward and not in pols_care.
    assert p.pols_care_mid(1) == pytest.approx(
        p.pols_care(1) + p.pols_entry_care(1), rel=FULL)
    assert p.pols_entry_care(1) == 0.0
    assert p.pols_care(2) == 0.0
    for t in (0, 1, 2):
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
    assert sum(p.pols_void(t) for t in range(p.proj_len())) == pytest.approx(
        0.000000626279, abs=COUNT)
    assert sum(p.claims(t, "VOID") for t in range(p.proj_len())) == pytest.approx(
        0.0073, abs=WON4)


def test_pitfall_the_surrender_value_cliff_has_a_direction(kr_ltc_anchor):
    """미지급형 pays **nil during** and half after; the check asserts the sign, not the size.

    Three of the four Korean forms differ only in which side of 납입완료 the 50% attaches to,
    and getting the side wrong inverts the whole cash-flow shape without moving any total
    enough to notice.  ``check_cv_form()`` therefore asserts ``cv_pp(t) = 0`` **identically**
    for ``t < n_P`` on this form, with its sign, and that the surrender value never exceeds
    the account and is never negative.
    """
    p = kr_ltc_anchor
    n = p.prem_period_mths()
    for t in range(0, n, 12):
        assert p.cv_pp(t) == 0.0
        assert p.check_cv_form_resid(t) == pytest.approx(0.0, abs=1e-12)
    assert p.cv_pp(n) == pytest.approx(0.5 * p.av_pp(n), rel=FULL)
    for t in (n, n + 60, 480, 599):
        assert 0.0 <= p.cv_pp(t) <= p.av_pp(t)
        assert p.check_cv_form_resid(t) >= -1e-12
    assert p.check_cv_form() is True
    assert p.av_pp(n - 1) > 0.0                      # the account is not nil, only the value
    assert p.cv_pp(n - 1) == 0.0


def test_pitfall_claims_death_is_the_gyeyakja_jeongnipaek_not_a_death_benefit(
        kr_ltc_anchor):
    """₩326,784 undiscounted, a third of premium income and larger than the lump sum.

    This contract has no death benefit.  What ``claims_death`` carries is the **계약자적립액**
    that 감독규정 제7-63조제1항제1호 makes payable on a death from a cause the contract does
    not cover, and 35.4% of the cohort dies that way before maturity with an account worth
    close to cumulative premiums.  Reading it as a sum assured, or dropping it because "this
    is a pure protection contract", are both wrong and in opposite directions.  And deaths
    **in** the care state pay nothing, which is why ``pols_death`` is split.
    """
    p = kr_ltc_anchor
    ts = range(p.proj_len())
    total_death = sum(p.claims(t, "DEATH") for t in ts)
    total_prem = sum(p.premiums(t) for t in ts)
    assert total_death == pytest.approx(326783.9323, abs=WON4)
    assert total_death / total_prem == pytest.approx(0.336, abs=5e-4)
    assert total_death > sum(p.claims(t, "LUMP") for t in ts)
    for t in (1, 120, 300, 540):
        assert p.claims(t, "DEATH") == pytest.approx(
            p.av_pp(t) * p.pols_death_act(t), rel=FULL)
        assert p.claims(t, "DEATH") != pytest.approx(
            p.lump_amount() * p.pols_death_act(t), rel=1e-3)
    # Deaths in the care state pay nothing, and there are 0.0166 of them.
    assert sum(p.pols_death_care(t) for t in ts) == pytest.approx(
        0.016574251130, abs=COUNT)
    assert sum(p.pols_death(t) for t in ts) == pytest.approx(0.354308072159, abs=COUNT)
    unpaid = sum(p.av_pp(t) * p.pols_death_care(t) for t in ts)
    assert unpaid > 0.0                              # it would be a real payment if made
    assert total_death == pytest.approx(
        sum(p.av_pp(t) * p.pols_death_act(t) for t in ts), rel=FULL)


def test_pitfall_the_light_compartment_pays_and_lapses_and_the_care_one_does_neither(
        kr_ltc_anchor):
    """Collapsing the two turns the 1·2등급 rate into a healthy-life incidence.

    A 3~5등급 life has been certified by the state, carries impaired mortality and receives
    nothing; the contract goes on charging it and it can still walk away.  Over the anchor
    cell's projection the light compartment accumulates 10.79 policy-months of exposure
    against the care compartment's 1.74.  Progression overtakes direct entry by policy month
    **8** at issue age 40 and is about 80% of gross inflow above 65, so a single-decrement
    model puts the cash flow years too early.
    """
    p = kr_ltc_anchor
    df = p.result_cf()
    assert df["pols_light"].sum() == pytest.approx(10.7877, abs=WON4)
    assert df["pols_care"].sum() == pytest.approx(1.7360, abs=WON4)
    assert df["pols_act"].sum() == pytest.approx(
        df["pols_healthy"].sum() + df["pols_light"].sum(), abs=WON4)
    # The light compartment pays and lapses; it is inside pols_act.
    for t in (120, 300, 540):
        assert p.pols_light(t) > 0.0
        assert p.pols_act(t) == pytest.approx(
            p.pols_healthy(t) + p.pols_light(t), rel=FULL)
        assert p.mort_rate_light(t) > p.mort_rate(t)
        assert p.mort_rate_light(t) < p.mort_rate_care(t)
    # Progression overtakes direct entry at month 8, and dominates above 65.
    assert p.pols_entry_care_prog(7) < p.pols_entry_care_direct(7)
    assert p.pols_entry_care_prog(8) > p.pols_entry_care_direct(8)
    for x in (70, 80):
        t = 12 * (x - p.issue_age())
        gross = p.pols_entry_care_direct(t) + p.pols_entry_care_prog(t)
        assert p.pols_entry_care_prog(t) / gross == pytest.approx(0.80, abs=0.02), x
    assert 1.0 - p.direct_entry_share == 0.80


def test_pitfall_prog_rate_is_not_scaled_below_65_and_that_is_deliberate(kr_ltc_anchor):
    """``rho(40) = 0.0340`` is **higher** than ``rho(65) = 0.0153``, and that is right.

    ``sub65_factor_at`` applies to ``i_D`` and ``i_L``, which are rates of *entering* the
    scheme through a gate the statute narrows below 65 to the closed 노인성 질병 list.
    ``rho`` is a property of a life **already certified**, and a life certified at 만나이 50
    got there through that list and is, if anything, more likely to progress than a
    70-year-old.  It looks wrong on a decrement table and it is right here.
    """
    p = kr_ltc_anchor
    assert p.prog_rate_at(40) == pytest.approx(0.033968, abs=5e-6)
    assert p.prog_rate_at(65) == pytest.approx(0.015254, abs=5e-6)
    assert p.prog_rate_at(40) > p.prog_rate_at(65)
    assert p.prog_rate_at(50) > p.prog_rate_at(60) > p.prog_rate_at(65)
    # and it is emphatically not the age-65 rate carried down on the sub-65 factor
    assert p.prog_rate_at(40) != pytest.approx(
        p.prog_rate_at(65) * p.sub65_factor_at(40), rel=1e-3)
    assert p.prog_rate_at(40) / (p.prog_rate_at(65) * p.sub65_factor_at(40)) > 40.0
    # the sub-65 factor is applied to the two entry rates and to neither of the others
    for x in (40, 50, 60):
        assert p.sub65_factor_at(x) < 1.0
        assert p.inc_rate_direct_at(x) == pytest.approx(
            p.inc_rate_direct_at(65) * p.sub65_factor_at(x), rel=FULL)
        assert p.inc_rate_light_at(x) == pytest.approx(
            p.inc_rate_light_at(65) * p.sub65_factor_at(x), rel=FULL)
    assert p.sub65_factor_at(65) == 1.0
    assert p.sub65_factor_at(70) == 1.0
    assert p.sub65_factor_at(40) == pytest.approx(
        math.exp(-p.sub65_gradient() * 25), rel=FULL)


def test_pitfall_widening_the_threshold_is_not_a_re_scaling(tmp_path):
    """``g2`` to ``g5`` multiplies lifetime benefit outgo by 2.43, and re-times it as well.

    The exposure changes in **frequency and in timing together**, because the light
    compartment shrinks as the gate widens and vanishes entirely at ``g6``.  On the anchor
    cell's unchanged premium, PV(benefit)/PV(premium) goes from 0.4603 at ``g2`` to 1.1233 at
    ``g5`` and 0.1997 at ``g1``.  Treating the threshold as a multiplier on one incidence
    rate is the error the market itself prices against at about 4.5 : 1.
    """
    base_benefit = 814977.8329
    wide = variant_model(tmp_path, "LTC_KR_S_g5", benefit_grade="g5")
    try:
        q = wide.Projection[1]
        assert q.benefit_grade() == "g5"
        totals = lifetime(q)
        assert totals["benefit"] == pytest.approx(1978328.4751, abs=WON4)
        assert totals["benefit"] / base_benefit == pytest.approx(2.43, abs=0.005)
        assert pv_benefit_over_premium(q) == pytest.approx(1.1233, abs=5e-5)
        assert q.prev_care_at(75) > q.prev_light_at(75)     # the light pool has shrunk
    finally:
        wide.close()
    narrow = variant_model(tmp_path, "LTC_KR_S_g1", benefit_grade="g1")
    try:
        q = narrow.Projection[1]
        assert q.benefit_grade() == "g1"
        assert pv_benefit_over_premium(q) == pytest.approx(0.1997, abs=5e-5)
        assert lifetime(q)["benefit"] < base_benefit
    finally:
        narrow.close()


def test_pitfall_the_two_modules_run_in_opposite_sex_directions(long_term_care):
    """The certification basis reproduces the market's sex direction; the 치매 one does not.

    장기요양 covers are dearer for women at every age and 치매 covers are **cheaper**, in the
    same document.  The certification basis gets the first right through the sourced
    prevalence, whose sex crossover is at about 만나이 70 — male above female below it and
    female above male over it.  The dementia basis applies a **flat-in-age** sex factor,
    1.0346 female against 0.9568 male, so the model prices the rider *dearer* for women at
    every age and does not reproduce the second.  A user who switches the rider on and reads
    the sex differential off the output is reading an artefact of that simplification.
    """
    male = long_term_care.Projection[1]
    female = long_term_care.Projection[2]
    assert male.sex() == "M" and female.sex() == "F"
    assert female.premium_mth_pp() / male.premium_mth_pp() == 1.5
    # the certification prevalence crosses over at about 70
    assert female.prev_rate_at(65) < male.prev_rate_at(65)
    assert female.prev_rate_at(68) < male.prev_rate_at(68)
    assert female.prev_rate_at(70) > male.prev_rate_at(70)
    assert female.prev_rate_at(85) > male.prev_rate_at(85)
    assert female.prev_rate_at(85) / male.prev_rate_at(85) == pytest.approx(
        1.82, abs=0.01)
    # the model's own first-entry rate crosses one in the same region
    assert first_entry_rate(female, 60) < first_entry_rate(male, 60)
    assert first_entry_rate(female, 70) > first_entry_rate(male, 70)
    # the dementia sex factor is flat in age, so the ratio never moves
    assert male.dem_param("dem_factor_m") == 0.9568
    assert female.dem_param("dem_factor_f") == 1.0346
    ratios = [female.dem_prev_at(x) / male.dem_prev_at(x) for x in (40, 65, 75, 85)]
    assert ratios == [pytest.approx(1.0346 / 0.9568, rel=FULL)] * 4
    assert all(r > 1.0 for r in ratios)              # dearer, where the market is cheaper


def test_pitfall_the_care_state_is_absorbing_because_the_contract_makes_it_so(
        kr_ltc_anchor):
    """No recovery, no lapse and no re-trigger — and each of the three is a 약관 term.

    Grades move both ways in the public scheme, and 9.2% of current certifications arose
    from a 등급변경신청, but the amount is frozen at first certification, the instalments are
    metered on **survival** rather than on continued certification, and surrender is barred.
    So the simplification is the contract's rather than the model's, and it would **not** be
    available at all for the utilisation-conditioned 지원금 form, which requires the insured
    to be *using* a named public benefit in the month.
    """
    p = kr_ltc_anchor
    # the care compartment leaves only by death
    for t in (120, 300, 540):
        assert p.pols_care(t + 1) == pytest.approx(
            (p.pols_care(t) + p.pols_entry_care(t))
            * (1.0 - p.mort_rate_care_mth(t)), rel=FULL)
    # the annuity is metered on survival, and the survival is the care state's own
    assert p.care_surv(300, 312) == pytest.approx(
        (1.0 - p.mort_rate_care_mth(300)) ** 12, rel=1e-9)
    # the lump sum is once only: it rides on first entries, never on the stock
    for t in (120, 300, 540):
        assert p.claims(t, "LUMP") == pytest.approx(
            p.lump_amount() * p.red_factor(t) * p.pols_entry_care(t), rel=FULL)
        assert p.pols_care(t) > p.pols_entry_care(t)
    # and there is no cells anywhere in this model that moves a life out of the care state
    assert not any(name.startswith("rec_") for name in p.cells)
    assert "pols_recovery" not in p.cells


def test_pitfall_the_disclosed_yejeong_wiheomnyul_is_not_this_models_level(kr_ltc_anchor):
    """The model runs at about a fifth of the one disclosed Korean rate, and publishes it.

    ``disclosed_inc_ratio_at`` is 0.2399 at 만나이 40, 0.2465 at 50 and 0.2399 at 60, so the
    disclosed rate is about **4.2 times** the model's best estimate.  It is a *loaded*
    pricing rate for a select, underwritten, 180-day-waited population quoted on 보험나이, and
    it is read here for its **gradient below 65 and its sex ratio**, never for its level:
    substituting it would multiply benefit outgo by roughly four and contradict the premium
    it was quoted alongside.
    """
    p = kr_ltc_anchor
    for x, ratio in ((40, 0.23993880644434135), (50, 0.24647550031825774),
                     (60, 0.23993880644434137)):
        assert p.disclosed_inc_ratio_at(x) == pytest.approx(ratio, rel=FULL), x
        assert 1.0 / p.disclosed_inc_ratio_at(x) == pytest.approx(4.2, abs=0.15)
        assert p.disclosed_inc_ratio_at(x) == pytest.approx(
            first_entry_rate(p, x) / p.disclosed_inc_at(x), rel=FULL)
    # what the disclosed card is actually used for: the gradient, and nothing else
    assert p.sub65_gradient() == pytest.approx(
        math.log(p.disclosed_inc_at(60) / p.disclosed_inc_at(40)) / 20.0, rel=1e-9)
    assert math.exp(p.sub65_gradient()) - 1.0 == pytest.approx(0.1300, abs=5e-5)


def test_pitfall_proj_len_is_a_row_count_not_the_last_index(kr_ltc_anchor):
    """``proj_len()`` counts rows: 601 of them, ``t = 0 ... 600``, the last the 90세 계약해당일.

    The frame is ``range(proj_len())``, so the last index is ``proj_len() - 1`` and the
    terminal row is the maturity month.  That is why the cash-flow cells guard on
    ``t >= proj_len() - 1`` while the in-force counts guard on ``t >= proj_len()``: the
    maturity is the decrement that closes the roll-forward on that row, and nothing else
    removes the surviving block.  A loop to ``range(proj_len() - 1)`` silently drops it.
    """
    p = kr_ltc_anchor
    n = p.proj_len()
    assert n == 601
    assert n == 12 * (p.term_age() - p.issue_age()) + 1
    df = p.result_cf()
    assert len(df) == n
    assert df.index[-1] == n - 1
    assert df.index.name == "t"
    assert list(df.index) == list(range(n))
    assert p.pols_if(n - 1) > 0.0
    assert (p.pols_death(n - 1) == 0.0 and p.pols_lapse(n - 1) == 0.0
            and p.pols_void(n - 1) == 0.0)
    assert p.pols_maturity(n - 1) == p.pols_if(n - 1)
    assert p.check_pols_roll_fwd_resid(n - 1) == pytest.approx(0.0, abs=1e-12)
    # the residual at the last row is nil only because the maturity term is in it
    assert p.pols_if(n - 1) - p.pols_if(n) == pytest.approx(
        p.pols_maturity(n - 1), abs=1e-12)


# ---------------------------------------------------------------------------
# The check_* cells this model publishes, by name


def test_the_six_check_cells_are_published_with_their_residuals(long_term_care):
    """These six ``check_*`` cells are published, and no others, each with its residual.

    ``check_pols_roll_fwd`` closes the in-force against the month's four decrements,
    ``check_nesting`` the compartment structure, ``check_ann_ledger`` the 간병연금 ledger
    against an independent rebuild, ``check_av_continuity`` the two branches of the
    계약자적립액 at 납입완료, ``check_cv_form`` the sign of the surrender-value cliff, and
    ``check_net_cf`` the cash flow statement against ``net_cf``.  Each returns a bool over
    all ``t``, with the signed per-month residual at ``<name>_resid(t)``.

    That they *hold*, on all nine model points, is asserted in
    ``test_model_conventions_kr.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library.  Generic discovery cannot
    notice a check that has **gone** — it simply stops being discovered — so naming the set
    is the statement left here.
    """
    checks = ("check_ann_ledger", "check_av_continuity", "check_cv_form",
              "check_nesting", "check_net_cf", "check_pols_roll_fwd")
    cells = set(long_term_care.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(checks)
    for check in checks:
        assert check + "_resid" in cells, check
    p = long_term_care.Projection[1]
    for check in checks:
        assert getattr(p, check)() is True, check


def test_check_nesting_holds_the_compartments_and_the_dementia_counter(long_term_care):
    """The three compartments are non-negative, add to ``pols_if``, and contain ``pols_dem``.

    A negative value here would mean progression had drained more lives out of the light
    compartment than were in it, or that the rider's first-event ledger had outgrown the
    block it rides on.  ``pols_dem`` is a **first-event counter**, not a fourth compartment,
    and it is never added to the three: it is nested inside the in-force block.
    """
    for point_id in long_term_care.Data.model_point_table().index:
        p = long_term_care.Projection[point_id]
        assert p.check_nesting() is True, point_id
        for t in (0, 1, 12, p.proj_len() // 2, p.proj_len() - 1):
            assert p.check_nesting_resid(t) >= -1e-12, (point_id, t)
            assert min(p.pols_healthy(t), p.pols_light(t), p.pols_care(t)) >= 0.0
            assert p.pols_dem(t) <= p.pols_if(t) + 1e-12
            assert p.pols_if(t) == pytest.approx(
                p.pols_act(t) + p.pols_care(t), rel=FULL)


def test_check_ann_ledger_closes_against_an_independent_rebuild(kr_ltc_anchor):
    """The rebuild scans every month in the cap window instead of stepping the same loop.

    A ledger that paid the first instalment a year late, that ran past the 120-month cap,
    that lost the twelve-month guarantee, or that used a ratio form of ``care_surv`` shows up
    in the residual rather than in the totals, where it would be invisible.
    """
    p = kr_ltc_anchor
    assert p.check_ann_ledger() is True
    for t in (0, 1, 3, 12, 130, 400, 599, 600):
        assert p.check_ann_ledger_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_check_av_continuity_is_the_derivation_and_not_a_round_number(kr_ltc_anchor):
    """The residual is non-zero only at ``t = n_P``, and there it is nil by derivation.

    ``net_prem_ratio()`` is derived from the run-off's first anchor, so the accumulation
    branch and the sourced branch meet at 납입완료.  Replacing the derivation with a round
    number — 0.80, say — opens the join, and this is the cell that says so.
    """
    p = kr_ltc_anchor
    n = p.prem_period_mths()
    assert p.check_av_continuity() is True
    for t in (0, 1, 120, 239, 241, 600):
        assert p.check_av_continuity_resid(t) == 0.0
    assert p.check_av_continuity_resid(n) == pytest.approx(0.0, abs=1e-9)
    rounded = 0.80 * p.premium_mth_pp() * p.prem_accum_factor(n)
    assert abs(rounded - p.av_ratio_at(0.0) * p.premium_mth_pp() * n) > p.val_tol


def test_check_net_cf_re_adds_from_the_published_columns(long_term_care):
    """``net_cf`` is exactly the eleven columns ``result_cf()`` prints, to ``val_tol``.

    A cash flow that exists in ``net_cf`` but not in the statement, or the reverse, shows up
    here — which is the failure a reader of the printed table could never see.  The house
    contract is that no model's headline number is reconciled only in prose.
    """
    p = long_term_care.Projection[1]
    assert p.check_net_cf() is True
    for t in (0, 1, 3, 12, 240, 600):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)
    df = p.result_cf()
    rebuilt = (df["premiums"] - df["claims_lump"] - df["claims_annuity"]
               - df["claims_dementia"] - df["claims_death"] - df["claims_lapse"]
               - df["claims_void"] - df["claims_maturity"] - df["expenses"]
               - df["claim_expenses"] - df["commissions"])
    assert (rebuilt - df["net_cf"]).abs().max() < p.val_tol
    assert df["net_cf"].iloc[0] < 0.0                # income-positive: the strain is negative
    assert df["net_cf"].iloc[1] > 0.0


def test_result_pols_publishes_the_decrement_view(kr_ltc_anchor):
    """The companion frame, indexed by ``t``, carrying the counts and the rates behind them.

    ``result_cf()`` is the cash flow statement and ``result_pols()`` is what a reviewer reads
    beside it: the compartments, the certifications, the two decrements, the annuity ledger,
    and the five rates and two per-policy values that produced them.
    """
    p = kr_ltc_anchor
    df = p.result_pols()
    assert df.index.name == "t"
    assert len(df) == p.proj_len()
    assert list(df.columns) == [
        "pols_if", "pols_healthy", "pols_light", "pols_care", "pols_dem",
        "pols_entry_light", "pols_entry_care", "pols_death", "pols_lapse",
        "ann_count", "mort_rate", "lapse_rate", "inc_rate_direct", "inc_rate_light",
        "prog_rate", "av_pp", "cv_pp"]
    assert df.notna().all().all()
    assert df["av_pp"].loc[240] == pytest.approx(1_309_056.0, abs=WON4)
    # The account peaks in the run-off branch, on the 1.088 anchor, and not at 납입완료.
    assert df["av_pp"].idxmax() == 360
    assert df["av_pp"].max() == pytest.approx(1462271.8952, abs=WON4)
    assert df["av_pp"].max() < 1.088 * 5_600 * 240        # the grid lands just off the anchor
    assert (df["cv_pp"].iloc[:240] == 0.0).all()


# ---------------------------------------------------------------------------
# The [std] assumptions, read off the model


def test_the_std_scalar_assumptions_are_the_notes_own(long_term_care):
    """Every scalar Reference the notes state, read off the ``Projection`` Space.

    A silent change to one of these moves a result rather than failing a test, which is
    exactly the failure mode this library exists to close: the worked example would move,
    the notes would be wrong, and nothing would say so until a reader compared them by eye.
    Each value carries its rationale in the notes' *Standardizations used* table; what is
    pinned here is the number.
    """
    projection = long_term_care.Projection
    assert projection.care_mort_mult == 3.0
    assert projection.light_mort_mult == 1.8
    assert projection.dem_mort_mult == 2.5
    assert projection.direct_entry_share == 0.20
    assert projection.prog_rate_cap == 1.0
    assert projection.sub65_age == 65
    assert projection.disease_share == 0.95
    assert projection.red_fraction == 0.50
    assert projection.dementia_wait_mths == 15
    assert projection.prem_int_rate == 0.02
    assert projection.surr_chg_ratio == 13.0
    assert projection.surr_chg_years == 7
    assert projection.expense_acq_mths == 5.2
    assert projection.expense_maint == 200.0
    assert projection.expense_claim == 30_000.0
    assert projection.inflation_rate == 0.02
    assert projection.comm_init_mths == 7.8
    assert projection.comm_renewal_rate == 0.03
    assert projection.roll_fwd_tol == 1e-12
    assert projection.val_tol == 1e-06
    # The two expense figures are not free: together they are the 표준해약공제액 of 13 months.
    assert projection.expense_acq_mths + projection.comm_init_mths == pytest.approx(
        projection.surr_chg_ratio, rel=FULL)
    assert projection.comm_init_mths / projection.surr_chg_ratio == pytest.approx(
        0.60, abs=0.001)
    assert projection.prog_rate_cap == 1.0           # a guard that binds on no shipped point


def test_the_std_table_parameters_are_the_notes_own(long_term_care):
    """The lapse vector, the 계약자적립액 anchors and the dementia logistic, off the CSVs.

    The lapse shape and its two convergence points are the regulator's — the 로그-선형
    원칙모형 with a 0.1% practical convergence point at 납입완료 and a 0.8% post-완납 ultimate
    — while the 8.0% first-year level and the 4.0% comparison vector are [std].  The four
    계약자적립액 anchors are the published 환급률 progression doubled.
    """
    p = long_term_care.Projection[1]
    assert p.lapse_param("lapse_year1") == 0.08
    assert p.lapse_param("lapse_completion") == 0.001
    assert p.lapse_param("lapse_ultimate") == 0.008
    assert p.lapse_param("lapse_level_std") == 0.04
    # the log-linear path: geometric in policy year from year 1 to 납입완료, then ultimate
    n = p.prem_period_years()
    for year in (1, 5, 10, 20):
        t = 12 * (year - 1)
        assert p.lapse_rate(t) == pytest.approx(
            0.08 * (0.001 / 0.08) ** ((year - 1) / (n - 1)), rel=FULL), year
    assert p.lapse_rate(12 * (n - 1)) == pytest.approx(0.001, rel=FULL)
    assert p.lapse_rate(12 * n) == 0.008
    assert p.dem_param("dem_ceil") == 0.8298
    assert p.dem_param("dem_beta") == 0.08706045
    assert p.dem_param("dem_x_mid") == 100.12641335
    assert p.av_ratio_at(0.0) == 0.974


def test_the_disclosed_incidence_table_carries_the_sex_ratio_the_notes_read_off_it(
        long_term_care):
    """0.357 / 0.575 / 0.882 on the 1등급 rate, and 0.37 / 0.58 / 0.87 on the combined one.

    The one Korean long-term-care incidence rate anybody publishes is used for two things
    and only two: the log-gradient that carries the entry rates below 65, and the sex ratio,
    which crosses one in the late sixties — exactly where the population data finds the
    prevalence crossover.  That the disclosed pricing basis and the national statistics
    agree on the crossover to within a few years is the strongest internal consistency check
    available here.
    """
    table = long_term_care.Data.incidence_table()
    for age, ratio in ((40, 0.357), (50, 0.575), (60, 0.882)):
        male = float(table.loc[("M", age), "rate_g1"])
        female = float(table.loc[("F", age), "rate_g1"])
        assert female / male == pytest.approx(ratio, abs=5e-4), age
    male_p = long_term_care.Projection[1]
    female_p = long_term_care.Projection[2]
    for age, ratio in ((40, 0.37), (50, 0.58), (60, 0.87)):
        assert (female_p.disclosed_inc_at(age)
                / male_p.disclosed_inc_at(age)) == pytest.approx(ratio, abs=5e-3), age
    assert female_p.sub65_gradient() == pytest.approx(0.16479184, abs=5e-9)
    assert math.exp(female_p.sub65_gradient()) - 1.0 == pytest.approx(0.1791, abs=5e-5)
    assert female_p.sub65_gradient() > male_p.sub65_gradient()


# ---------------------------------------------------------------------------
# The sensitivities the notes quote, each a re-run with one thing changed


def test_sensitivity_the_care_multiple_moves_entry_and_run_off_together():
    """1.0 / 2.0 / 4.0 against the shipped 3.0, on the lump sum and on the annuity.

    ``care_mort_mult`` sets how long the annuity runs **and** it is the excess-mortality term
    of the incidence identity, so it moves entry and run-off in opposite directions at once.
    At 4.0 even the annuity rises, the extra entrants outweighing the shorter run-off.  This
    is the model's largest quantified sensitivity and there is no published table anywhere.
    """
    model = mx.read_model(MODEL_DIR, name="LTC_KR_S_caremult")
    try:
        base = lifetime(model.Projection[1])
        expected = {1.0: (-0.377, -0.147), 2.0: (-0.192, -0.066), 4.0: (0.201, 0.056)}
        for multiple, (lump_move, annuity_move) in expected.items():
            model.Projection.care_mort_mult = multiple
            model.Projection.clear_all()
            totals = lifetime(model.Projection[1])
            assert totals["claims_lump"] / base["claims_lump"] - 1.0 == pytest.approx(
                lump_move, abs=0.001), multiple
            assert (totals["claims_annuity"] / base["claims_annuity"] - 1.0
                    == pytest.approx(annuity_move, abs=0.001)), multiple
    finally:
        model.close()


def test_sensitivity_the_boheom_gigan_truncation_at_90(tmp_path):
    """95세만기 is +41.2% / +37.4% and 100세만기 +70.6% / +59.3% on an unchanged premium.

    The composite stops at 90 because that is the modal Korean maturity and the term of both
    published rate anchors, but it truncates the exposure at exactly the band carrying the
    highest certification rate of all — 41.7% at 85 and over, and still rising — so the
    choice is materially **conservative** on claim cost.  The notes call it the first
    sensitivity a user should run.
    """
    for term, lump_move, annuity_move, pv_ratio in (
            (95, 0.412, 0.374, 0.5976), (100, 0.706, 0.593, 0.6762)):
        model = variant_model(tmp_path, "LTC_KR_S_term%d" % term, term_age=term)
        try:
            q = model.Projection[1]
            assert q.term_age() == term
            assert q.proj_len() == 12 * (term - 40) + 1
            totals = lifetime(q)
            assert totals["claims_lump"] / 268065.6927 - 1.0 == pytest.approx(
                lump_move, abs=0.001), term
            assert totals["claims_annuity"] / 546912.1402 - 1.0 == pytest.approx(
                annuity_move, abs=0.001), term
            assert pv_benefit_over_premium(q) == pytest.approx(pv_ratio, abs=5e-4), term
        finally:
            model.close()


def test_sensitivity_lapse_is_the_dominant_lever_and_its_sign_is_the_opposite_one(
        tmp_path):
    """A level 4.0% cuts lifetime benefit outgo 61.1% and turns ``net_cf`` positive.

    The 표준형 comparison vector looks *higher* than the log-linear path's 0.1% convergence
    point and *lower* than its 8.0% first year, and it is far higher on average over fifty
    years, so it removes most of the block before the claims arrive.  A model whose lapse
    assumption is described only by its first-year value cannot be read at all on this
    product — and the comparison is the one [REG-R27] requires an insurer to disclose.
    """
    model = variant_model(tmp_path, "LTC_KR_S_lapsestd", lapse_form="pyojun")
    try:
        q = model.Projection[1]
        assert q.lapse_form() == "pyojun"
        assert q.lapse_rate(0) == 0.04 and q.lapse_rate(300) == 0.04
        totals = lifetime(q)
        assert totals["benefit"] == pytest.approx(317015.5544, abs=WON4)
        assert 1.0 - totals["benefit"] / 814977.8329 == pytest.approx(0.611, abs=0.001)
        assert totals["net_cf"] == pytest.approx(120119.7979, abs=WON4)
        assert totals["net_cf"] > 0.0
    finally:
        model.close()


def test_sensitivity_direct_entry_share_carries_the_timing_and_not_the_level():
    """0.05 moves lifetime benefit outgo +0.7% and 0.50 moves it -1.8%; the PV moves more.

    That is the expected behaviour of a parameter that reallocates one inflow between two
    routes with different delays, and it is why the closing assumption is defensible even
    though it is unsourced: it is **not carrying the level**.  The PV ratio at the 예정이율
    goes 0.4653 / 0.4603 / 0.4485 across 0.05 / 0.20 / 0.50, which is the timing showing up
    where the total does not.
    """
    model = mx.read_model(MODEL_DIR, name="LTC_KR_S_des")
    try:
        assert pv_benefit_over_premium(model.Projection[1]) == pytest.approx(
            0.4603, abs=5e-4)
        for share, move, pv_ratio in ((0.05, 0.0075, 0.4653), (0.50, -0.0179, 0.4485)):
            model.Projection.direct_entry_share = share
            model.Projection.clear_all()
            q = model.Projection[1]
            assert lifetime(q)["benefit"] / 814977.8329 - 1.0 == pytest.approx(
                move, abs=0.0005), share
            assert pv_benefit_over_premium(q) == pytest.approx(pv_ratio, abs=5e-4), share
    finally:
        model.close()


def test_sensitivity_the_grade_share_moves_the_split_and_re_times_it(tmp_path):
    """The national all-ages 0.1328 moves the total +0.8% and the split -3.2% / +2.7%.

    The "factor of two" the notes quote is a statement about the **rate at a given age** —
    22.2% below 65 against 11.1% at 80-84 — and not about the anchor cell's lifetime total.
    Replacing the age-varying share with one number leaves the total nearly alone and moves
    the lump sum and the annuity in opposite directions, because it re-times both.
    """
    def flatten(table):
        table.loc[table["grade"] == "g2", "share_ge"] = 0.1328
        return table

    model = variant_table(tmp_path, "LTC_KR_S_flatshare", "grade_share_table.csv",
                          flatten)
    try:
        q = model.Projection[1]
        assert q.share_ge_at("g2", 40) == 0.1328
        assert q.share_ge_at("g2", 85) == 0.1328
        assert q.share_slope_at("g2", 70) == 0.0
        totals = lifetime(q)
        assert totals["benefit"] / 814977.8329 - 1.0 == pytest.approx(0.008, abs=0.001)
        assert totals["claims_lump"] / 268065.6927 - 1.0 == pytest.approx(
            -0.032, abs=0.001)
        assert totals["claims_annuity"] / 546912.1402 - 1.0 == pytest.approx(
            0.027, abs=0.001)
    finally:
        model.close()
    anchor = mx.read_model(MODEL_DIR, name="LTC_KR_S_share")
    try:
        p = anchor.Projection[1]
        assert p.share_ge_at("g2", 60) == pytest.approx(0.222, abs=5e-4)
        assert p.share_ge_at("g2", 82) == pytest.approx(0.111, abs=5e-4)
        assert p.share_ge_at("g2", 60) / p.share_ge_at("g2", 82) == pytest.approx(
            2.0, abs=0.02)
    finally:
        anchor.close()


def test_sensitivity_the_gamaek_gigan_is_nearly_worthless_on_this_cell(tmp_path):
    """``red_mths`` 0 and 24 move lifetime benefit outgo by +0.010% and -0.023%.

    At issue age 40 almost nothing is certified in the first year or two, so the mechanic
    barely registers on the anchor cell.  It is **not** negligible in general: the same rule
    mis-modelled — re-tested at each instalment rather than frozen — is worth 0.315% of
    annuity outgo at issue age 70.  A parameter that does nothing on the anchor cell can
    still be a first-order error at the top of the issue-age range.
    """
    for months, move in ((0, 0.00010), (24, -0.00023)):
        model = variant_model(tmp_path, "LTC_KR_S_red%d" % months, red_mths=months)
        try:
            q = model.Projection[1]
            assert q.red_mths() == months
            assert q.red_factor(0) == (1.0 if months == 0 else 0.525)
            assert lifetime(q)["benefit"] / 814977.8329 - 1.0 == pytest.approx(
                move, abs=2e-5), months
        finally:
            model.close()


# ---------------------------------------------------------------------------
# The optional modules, each in both positions


def test_the_ganbyeong_yeongeum_is_on_at_the_anchor_and_off_at_point_4(long_term_care):
    """Model point 4 carries the lump-sum-only form, and every annuity cells goes silent.

    Switching the rider off removes most — not all — of the dependence on the post-onset
    mortality basis, because the waiver still stops the premium for the care state's own
    duration.  That is where post-onset mortality enters even a lump-sum-only version of
    this contract.
    """
    p1 = long_term_care.Projection[1]
    p4 = long_term_care.Projection[4]
    assert p1.annuity_on() is True and p4.annuity_on() is False
    assert p4.term_age() == 95 and p4.benefit_grade() == "g5"
    for t in (0, 12, 200, 400):
        assert p4.ann_count(t) == 0.0
        assert p4.ann_pay(t) == 0.0
        assert p4.ann_tests(t) == 0.0
        assert p4.claims(t, "ANNUITY") == 0.0
    assert p4.ann_amount_at(100) == 0.0
    assert (p4.result_cf()["claims_annuity"] == 0.0).all()
    assert p4.check_ann_ledger() is True
    # the waiver still bites: premium rides on pols_act, which is below pols_if
    t = 300
    assert p4.pols_care(t) > 0.0
    assert p4.premiums(t) < p4.premium_mth_pp() * p4.pols_if(t)


def test_the_dementia_rider_is_off_at_the_anchor_and_on_at_points_5_and_8(
        long_term_care):
    """A different trigger, a different sex basis, and a **fifteen-month** effective wait.

    The rider is behind a one-year 보장개시일 and, inside the definition of the state itself,
    a 90-day persistence test, so the first diagnosis it can pay for falls in month 15.  Its
    incidence is built by the same prevalence-to-incidence identity from a *sourced*
    prevalence — the 2023 치매역학조사 band rates — rather than as a share of the
    certification rate, because the two triggers are correlated but not proportional.
    """
    p1 = long_term_care.Projection[1]
    assert p1.dementia_rider() is False
    for t in (0, 15, 300):
        assert p1.dem_inc_rate_mth(t) == 0.0
        assert p1.pols_entry_dem(t) == 0.0
        assert p1.pols_dem(t) == 0.0
        assert p1.claims(t, "DEMENTIA") == 0.0

    for point_id in (5, 8):
        q = long_term_care.Projection[point_id]
        assert q.dementia_rider() is True
        assert q.dementia_amount() == 10_000_000.0
        assert q.dementia_wait_mths == 15
        for t in range(0, 15):
            assert q.dem_inc_rate_mth(t) == 0.0
            assert q.pols_entry_dem(t) == 0.0
        assert q.dem_inc_rate_mth(15) > 0.0
        assert q.pols_entry_dem(15) > 0.0
        assert q.claims(15, "DEMENTIA") == pytest.approx(
            q.dementia_amount() * q.pols_entry_dem(15), rel=FULL)
        assert sum(q.claims(t, "DEMENTIA") for t in range(q.proj_len())) > 0.0
        # the first-event counter never outgrows the block it rides on
        for t in (16, 200, q.proj_len() - 1):
            assert 0.0 <= q.pols_dem(t) <= q.pols_if(t) + 1e-12
        assert q.check_nesting() is True
        # driven off the sourced dementia prevalence, not off the certification rate
        assert q.dem_inc_rate_at(70) != pytest.approx(q.inc_rate_direct_at(70), rel=1e-3)


def test_the_g6_gate_leaves_no_light_state_at_all(long_term_care):
    """At 1~인지지원등급 every certified life is inside the gate, so ``rho`` is zero.

    ``prev_light_at`` is zero by construction, progression has nothing to draw from, and the
    whole inflow into the care state is direct — by construction rather than by assumption.
    Model point 5 carries it, and it is the branch of ``inc_rate_direct_at`` that the anchor
    cell never reaches.
    """
    p5 = long_term_care.Projection[5]
    assert p5.benefit_grade() == "g6"
    for x in (65, 75, 85):
        assert p5.prev_light_at(x) == pytest.approx(0.0, abs=1e-15)
        assert p5.prog_rate_at(x) == 0.0
        assert p5.prev_care_at(x) == pytest.approx(p5.prev_rate_at(x), rel=FULL)
        assert p5.inc_rate_direct_at(x) == pytest.approx(
            p5.inflow_care_at(x) / (1.0 - p5.prev_rate_at(x)), rel=FULL)
    for t in (0, 120, 400):
        assert p5.pols_light(t) == pytest.approx(0.0, abs=1e-15)
        assert p5.pols_entry_care_prog(t) == 0.0
        assert p5.pols_act(t) == pytest.approx(p5.pols_healthy(t), rel=FULL)
    assert p5.check_nesting() is True


def test_the_ganpyeon_simsa_loading_is_a_premium_multiplier_only(long_term_care, tmp_path):
    """Model point 8's ``uw_loading`` of 1.40 raises the premium and nothing else.

    No retrieved source gives the simplified pool's incidence separately, so on a loaded
    model point the extra premium is **pure margin** in this model and the true claim cost of
    that pool is understated.  Its positive ``net_cf`` of +₩1,152,142 is an artefact of
    exactly that and has to be described as one.  One carrier will not attach its 장기요양
    riders to a simplified chassis at all, which is the market's own view of how much.

    The unloaded counterfactual is the same model point at ``uw_loading = 1.0``: every
    decrement, every transition rate and every benefit outgo is identical, and only the
    premium-driven lines move.  That is the whole content of the assumption, and it is why
    the loaded cell's margin cannot be read as a result.
    """
    p8 = long_term_care.Projection[8]
    assert p8.uw_loading() == 1.4
    table = long_term_care.Data.model_point_table()
    assert p8.premium_mth_pp() == pytest.approx(
        1.4 * float(table.loc[8, "premium"]), rel=FULL)
    assert sum(p8.net_cf(t) for t in range(p8.proj_len())) == pytest.approx(
        1152142.1277, abs=WON4)
    assert all(long_term_care.Projection[pid].uw_loading() == 1.0
               for pid in table.index if pid != 8)

    model = variant_model(tmp_path, "LTC_KR_S_uw1", point_id=8, uw_loading=1.0)
    try:
        plain = model.Projection[8]
        assert plain.premium_mth_pp() == pytest.approx(
            p8.premium_mth_pp() / 1.4, rel=FULL)
        for x in (50, 70, 85):
            assert plain.inc_rate_direct_at(x) == pytest.approx(
                p8.inc_rate_direct_at(x), rel=FULL), x
            assert plain.inc_rate_light_at(x) == pytest.approx(
                p8.inc_rate_light_at(x), rel=FULL), x
            assert plain.prog_rate_at(x) == pytest.approx(p8.prog_rate_at(x), rel=FULL), x
        for t in (0, 120, 300):
            assert plain.pols_entry_care(t) == pytest.approx(
                p8.pols_entry_care(t), rel=FULL), t
            assert plain.claims(t, "LUMP") == pytest.approx(
                p8.claims(t, "LUMP"), rel=FULL), t
            assert plain.claims(t, "ANNUITY") == pytest.approx(
                p8.claims(t, "ANNUITY"), rel=FULL), t
        # only the premium-driven lines move, and they move by exactly the loading
        assert p8.premiums(120) == pytest.approx(1.4 * plain.premiums(120), rel=FULL)
        assert p8.av_pp(120) == pytest.approx(1.4 * plain.av_pp(120), rel=FULL)
        loaded_margin = sum(p8.net_cf(t) for t in range(p8.proj_len()))
        plain_margin = sum(plain.net_cf(t) for t in range(plain.proj_len()))
        assert loaded_margin > plain_margin
    finally:
        model.close()


def test_the_wait_and_reduction_combination_of_point_9(long_term_care):
    """Model point 9 carries the 우체국-style 180-day 보장개시일 and two-year 감액기간.

    Both are on the observed shelf — 90 days at three carriers against 180 at 우체국, and a
    one-year 감액 against a two-year one — and the composite takes the median of each.  The
    boundary moves with the model point rather than with a constant, so the second
    combination has to be projected as well as described.
    """
    p9 = long_term_care.Projection[9]
    assert p9.wait_mths() == 6 and p9.red_mths() == 24
    for t in range(0, 6):
        assert p9.pols_entry_care(t) == 0.0
        assert p9.pols_void(t) > 0.0
    assert p9.pols_void(6) == 0.0 and p9.pols_entry_care(6) > 0.0
    for t in (0, 12, 23):
        assert p9.red_factor(t) == 0.525
    assert p9.red_factor(24) == 1.0
    assert p9.ann_amount_at(23) == pytest.approx(0.525 * p9.ann_amount_at(24), rel=FULL)
    assert p9.check_pols_roll_fwd() is True and p9.check_ann_ledger() is True


def test_the_annuity_cap_of_point_7_is_sixty_months(long_term_care):
    """Model point 7 halves the ceiling, and the ledger's window halves with it.

    The cap is the composite's protection against a post-onset mortality basis nobody
    publishes, and it binds jointly with maturity: nothing is paid on the maturity row
    ``t = proj_len() - 1`` or after it.  Carrying a second ceiling in the shipped table is
    what stops the 120-month window being hard-coded into the ledger.
    """
    p7 = long_term_care.Projection[7]
    assert p7.annuity_max_mths() == 60
    assert p7.annuity_guar_mths() == 12
    t = 200
    assert p7.ann_count(t) == pytest.approx(
        sum(p7.pols_entry_care(t - u)
            * (1.0 if u < 12 else p7.care_surv(t - u, t - u + 12 * (u // 12)))
            for u in range(0, 60)), rel=FULL)
    assert p7.pols_entry_care(t - 60) > 0.0          # a cohort just outside the window
    assert p7.check_ann_ledger() is True
    p1 = long_term_care.Projection[1]
    assert p1.annuity_max_mths() == 120
