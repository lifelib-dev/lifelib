"""Golden and structural tests for ``LTC_JP_S``, the 介護保険 reference model.

The house-style contract — external inputs, the ``Data`` / ``Projection`` split, the
read-once property, the docstring contract, the ``check_*`` shape — is asserted once for
every model in the library in ``test_model_conventions_jp.py``. What is asserted here is
this product.

The golden values are the worked example in
``products/nursing_care/technical-notes.md`` ("Worked example"), which projects the anchor
cell: male, 契約年齢 60, 終身/終身払, 介護一時金 ¥3,000,000 on 要介護2以上, 介護年金 ¥600,000 a
year from 要介護3以上 capped at ten instalments and survival-tested, 保険料払込免除 from
要介護1以上, company-basis limb on, 認知症一時金特約 off, 1-year 不担保期間 off, office premium
¥11,500 a month. They are **hard-coded** here rather than pickled so that a reviewer can
compare them against the notes by eye. Every row of the notes' table sits at age 60 in
policy year 1, so one set of rates drives all of them.

Tolerances follow the precision the notes display: money to ¥0.01, in-force and the care
ledgers to six decimals, rates to the ten decimals the notes print them at.

Beyond the worked example this module asserts, one test each, every entry in the notes'
*Known modeling pitfalls* list, because each of them is a way an implementation can look
right and be wrong:

* 認定率 is a **prevalence**, not an incidence, and the conversion between them is a
  two-term identity whose second term is not a refinement;
* the care state is absorbing, the annuity is survival-tested, and the ``state`` switch is
  a no-op unless the recovery rate is moved off zero;
* premium rides on ``pols_act`` and lapse is taken from ``pols_act``, because the waiver
  fires one grade below the lump sum and two below the annuity;
* the three care ledgers are **nested** marginal distributions and must never be summed;
* the ten-instalment cap **binds**, unlike every limit on the ``medical`` chassis;
* the annuity is paid **in advance**, from the entry month itself;
* care-state survival is a **partial product**, never a ratio of cumulative products;
* incidence steps by a factor of about six at **exactly** age 65;
* "180日" names two different mechanisms and only one of them is a waiting period;
* the prevalence tail above age 82 is **unsourced extrapolation** and 40% of the anchor
  cell's benefit outgo falls up there;
* a recovery under the ``state`` switch never restores the premium, which is a documented
  limit of that switch and not a defect in it;
* and there is **no surrender value, no 自動振替貸付 and no death benefit**.

Model points 4 to 8 carry the optional modules, and each is asserted in both positions —
off in the base run, and switched on. Where switching one on means changing a model point
column rather than a Space Reference, :func:`variant_model` copies the model *and its
external inputs* to a temporary directory and edits the copy, so the shipped table is
never touched.
"""
import shutil

import modelx as mx
import numpy as np
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from jp_registry import LIB, MODELS


MODEL_DIR = LIB / MODELS["LTC_JP_S"][0]

YEN = 5e-3            # money displayed to 0.01
INFORCE = 5e-7        # in-force and the care ledgers, displayed to 6 d.p.
RATE = 5e-11          # decrement and incidence rates, displayed to 10 d.p.


def _fresh_copy(tmp_path, name):
    """The model folder and every CSV beside it, copied into ``tmp_path / name``.

    Each variant gets its **own** directory rather than sharing one per test. Inputs are
    external, so a variant is made by editing a file; two variants sharing a directory
    would compose their edits, and a test asking for "half the lapse table" after a test
    asking for "no lapse at all" would silently get no lapse again.
    """
    root = tmp_path / name
    if not root.exists():
        shutil.copytree(MODEL_DIR, root / MODEL_DIR.name)
        for csv in MODEL_DIR.parent.glob("*.csv"):
            shutil.copy(csv, root / csv.name)
    return root


def variant_model(tmp_path, name, point_id, **overrides):
    """A copy of the model whose model point table has been edited.

    Four of the optional modules are switched by a **model point column**, not by a Space
    Reference, so exercising the other position means changing an input file. The whole
    model folder and every CSV beside it are copied to ``tmp_path`` first — inputs are
    external, so they have to travel with the model — and the copy is edited. The shipped
    product directory is never written to.
    """
    root = _fresh_copy(tmp_path, name)
    table = pd.read_csv(root / "model_point_table.csv", index_col="point_id")
    for column, value in overrides.items():
        table.loc[point_id, column] = value
    table.to_csv(root / "model_point_table.csv")
    return mx.read_model(root / MODEL_DIR.name, name=name)


def variant_table(tmp_path, name, filename, mutate):
    """A copy of the model one of whose **assumption tables** has been edited.

    The companion to :func:`variant_model`, for the sensitivities the notes quote against
    an input file rather than against a model point column or a Space Reference — the
    lapse table and the grade shares. ``mutate`` takes the loaded ``DataFrame`` and
    returns the edited one; the shipped product directory is never written to.
    """
    root = _fresh_copy(tmp_path, name)
    table = pd.read_csv(root / filename)
    mutate(table).to_csv(root / filename, index=False)
    return mx.read_model(root / MODEL_DIR.name, name=name)


def lifetime(p):
    """The four lifetime totals the notes' sensitivities are quoted against."""
    ts = range(p.proj_len())
    return {
        "premiums": sum(p.premiums(t) for t in ts),
        "claims": sum(p.claims(t) for t in ts),
        "claims_lump": sum(p.claims(t, "LUMP") for t in ts),
        "claims_annuity": sum(p.claims(t, "ANNUITY") for t in ts),
    }


# ---------------------------------------------------------------------------
# The worked example, hard-coded to the precision the notes display


def test_the_anchor_cell_is_the_worked_examples_model_point(jp_ltc_anchor):
    """Model point 1 is the cell the notes' worked example projects.

    Every golden value below is read off that one model point, so an edit to its row in
    ``model_point_table.csv`` must fail here rather than silently move the goldens.
    """
    p = jp_ltc_anchor
    assert p.issue_age() == 60
    assert p.sex() == "M"
    assert p.lump_amount() == 3_000_000.0
    assert p.annuity_amount() == 600_000.0
    assert (p.grade_lump(), p.grade_annuity(), p.grade_waiver()) == (
        "care2", "care3", "care1")
    assert p.annuity_max() == 10
    assert p.annuity_test() == "survival"
    assert p.premium_mth_pp() == 11_500.0
    assert p.company_limb() is True
    assert p.dementia_rider() is False
    assert p.waiting_1y() is False
    assert p.sel_lapse_lambda() == 0.0
    assert p.proj_len() == 684        # 12 x (116 - 60 + 1), the male terminal age


def test_the_worked_examples_assumption_values(jp_ltc_anchor):
    """Every rate the notes quote for the worked example, to the digits they show.

    The notes list these as "Assumption values used, every one of them", which makes them
    the model's contract with the document: the four-row table below is only meaningful if
    the rates driving it are the notes' own.
    """
    p = jp_ltc_anchor
    assert p.mort_rate_base(0) == 0.00548              # 第三分野標準生命表2018 男 q60
    assert p.mort_rate(0) == pytest.approx(0.00685, abs=5e-9)
    assert p.mort_rate_care(0) == pytest.approx(0.0188375, abs=5e-9)
    assert p.mort_rate_mth(0) == pytest.approx(0.0005726334, abs=RATE)
    assert p.mort_rate_care_mth(0) == pytest.approx(0.0015835104, abs=RATE)
    assert p.lapse_rate(0) == 0.09
    assert p.lapse_rate_mth(0) == pytest.approx(0.0078284203, abs=RATE)
    assert p.prev_rate(0) == pytest.approx(0.0064240463, abs=RATE)
    assert p.prev_slope(0) == pytest.approx(0.0012382778, abs=RATE)
    assert p.prev_grade(0, "care1") == pytest.approx(0.0045931931, abs=RATE)
    assert p.prev_grade(0, "care2") == pytest.approx(0.0032634155, abs=RATE)
    assert p.prev_grade(0, "care3") == pytest.approx(0.0021841757, abs=RATE)
    assert p.f_age(0) == 0.20
    assert p.inc_rate_w(0) == pytest.approx(0.0001889030, abs=RATE)
    assert p.inc_rate_l(0) == pytest.approx(0.0001340450, abs=RATE)
    assert p.inc_rate_n(0) == pytest.approx(0.0000896238, abs=RATE)
    assert p.inc_rate_w_mth(0) == pytest.approx(0.0000157419, abs=RATE)
    assert p.inc_rate_l_mth(0) == pytest.approx(0.0000111704, abs=RATE)
    assert p.inc_rate_n_mth(0) == pytest.approx(0.0000074686, abs=RATE)
    assert p.comm_init_pp() == 207_000.0               # 1.5 x 12 x 11,500


def test_the_prevalence_logistic_is_pinned_to_the_two_sourced_certification_rates(
        jp_ltc_anchor, nursing_care):
    """prev(70) = 4.3% and prev(82) = 31.1%, the two 認定率 the curve was fitted through.

    The published parameters are rounded to six decimals, so the curve reproduces the
    sourced rates to the three significant figures they are published at and no further.
    Everything above age 82 is unpinned extrapolation and is marked as such in the notes;
    how much of the liability sits in that region is asserted separately, in
    :func:`test_pitfall_the_prevalence_tail_is_an_unsourced_extrapolation`.
    """
    p = jp_ltc_anchor
    assert p.prev_param("prev_ceil") == 0.95
    assert p.prev_param("prev_beta") == 0.194069
    assert p.prev_param("prev_x_mid") == 85.710591
    assert p.prev_rate(12 * 10) == pytest.approx(0.043, abs=5e-4)     # age 70
    assert p.prev_rate(12 * 22) == pytest.approx(0.311, abs=5e-4)     # age 82
    table = nursing_care.Data.prevalence_table()
    assert table.loc["prev_rate_low", "value"] == 0.043
    assert table.loc["prev_rate_high", "value"] == 0.311


# t: pols_if, care_w, premiums, claims_lump, claims_annuity, expenses, commissions, net_cf
# The notes' `expenses` column is the **combined** expense of the month - acquisition,
# maintenance and claim handling - and the notes say so under the table. The model keeps
# them apart in `expenses` and `claim_expenses`, so the assertion below adds the two model
# columns back together to meet the document. The split itself is asserted in the month
# traces, which print both parts.
WORKED_EXAMPLE = {
    0: (1.000000, 0.000000, 11500.00, 33.51, 4.48, 20250.09, 207000.00, -215788.09),
    1: (0.991604, 0.000016, 11403.26, 33.23, 4.44, 247.99, 0.00, 11117.59),
    2: (0.983278, 0.000031, 11307.33, 32.95, 4.41, 245.91, 0.00, 11024.07),
    3: (0.975022, 0.000047, 11212.21, 32.67, 4.37, 243.85, 0.00, 10931.33),
}

# Policy year 1 in aggregate: the notes' strongest single test target, because it
# exercises the whole annual cycle on one set of rates.
WORKED_EXAMPLE_YEAR_1 = {
    "premiums": 131790.85,
    "claims_lump": 384.05,
    "claims_annuity": 51.36,
    "expenses": 22865.27,            # acquisition + maintenance, the model's own column
    "claim_expenses": 1.07,
    "expenses_combined": 22866.34,   # the single figure the notes' table prints
    "commissions": 207000.00,
    "net_cf": -98510.90,
}


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_the_worked_examples_four_rows(jp_ltc_anchor, t):
    """Every cell of the notes' four-row table, to the displayed precision."""
    p = jp_ltc_anchor
    pols_if, care_w, prem, lump, ann, exp, comm, ncf = WORKED_EXAMPLE[t]
    assert p.pols_if(t) == pytest.approx(pols_if, abs=INFORCE)
    assert p.care_w(t) == pytest.approx(care_w, abs=INFORCE)
    assert p.premiums(t) == pytest.approx(prem, abs=YEN)
    assert p.claims(t, "LUMP") == pytest.approx(lump, abs=YEN)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=YEN)
    assert p.expenses(t) + p.claim_expenses(t) == pytest.approx(exp, abs=YEN)
    assert p.commissions(t) == pytest.approx(comm, abs=YEN)
    assert p.net_cf(t) == pytest.approx(ncf, abs=YEN)


def test_the_worked_examples_month_0_trace(jp_ltc_anchor):
    """The notes' month-0 trace, term by term.

    Month 0 is where the whole of the first row is decided: one policy, one set of entry
    rates, the acquisition expense and the initial commission against a single month's
    premium. The annuity cohort of month 0 is paid **at once**, which is the in-advance
    convention seen at its first opportunity.
    """
    p = jp_ltc_anchor
    assert p.pols_act(0) == 1.0
    assert p.pols_entry_w(0) == pytest.approx(0.0000157419, abs=RATE)
    assert p.pols_entry_l(0) == pytest.approx(0.0000111704, abs=RATE)
    assert p.pols_entry_n(0) == pytest.approx(0.0000074686, abs=RATE)
    assert p.ann_count(0) == pytest.approx(0.0000074686, abs=RATE)
    assert p.claims(0, "LUMP") == pytest.approx(3_000_000 * 0.0000111704, abs=5e-4)
    assert p.claim_expenses(0) == pytest.approx(0.0932, abs=5e-5)
    assert p.expenses(0) == pytest.approx(250.00 + 20_000.00, abs=5e-4)
    assert p.expenses(0) + p.claim_expenses(0) == pytest.approx(
        250.00 + 0.0932 + 20_000.00, abs=5e-4)
    assert p.pols_term(0) == 0.0                 # no cohort is 108 months old
    assert p.pols_act(1) == pytest.approx(0.99158782, abs=5e-9)
    assert p.care_w(1) == pytest.approx(0.00001572, abs=5e-9)
    assert p.care_l(1) == pytest.approx(0.00001115, abs=5e-9)
    assert p.care_n(1) == pytest.approx(0.00000746, abs=5e-9)


def test_the_worked_examples_month_1_and_2_traces(jp_ltc_anchor):
    """The notes' month-1 and month-2 traces, including the maintenance/claim split.

    Month 1 is where premium income and the in-force count part company: the premium rides
    on ``pols_act`` and the two already differ in the fifth decimal. It is also where the
    month-0 annuity cohort is **not** paid again — the next instalment is at t = 12.
    """
    p = jp_ltc_anchor
    assert p.premiums(1) == pytest.approx(11403.2599, abs=5e-5)
    assert p.premiums(1) < p.premium_mth_pp() * p.pols_if(1)
    assert p.pols_entry_l(1) == pytest.approx(0.0000110765, abs=RATE)
    assert p.claims(1, "LUMP") == pytest.approx(33.2295, abs=5e-5)
    assert p.pols_entry_n(1) == pytest.approx(0.0000074059, abs=RATE)
    assert p.ann_count(1) == pytest.approx(0.0000074059, abs=RATE)
    assert p.claims(1, "ANNUITY") == pytest.approx(4.4435, abs=5e-5)
    assert p.claim_expenses(1) == pytest.approx(0.0924, abs=5e-5)
    assert p.expenses(1) == pytest.approx(247.9009, abs=5e-5)
    assert p.expenses(1) + p.claim_expenses(1) == pytest.approx(
        247.9009 + 0.0924, abs=5e-5)

    assert p.pols_act(2) == pytest.approx(0.98324640, abs=5e-9)
    assert p.premiums(2) == pytest.approx(11307.3336, abs=5e-5)
    assert p.pols_entry_l(2) == pytest.approx(0.0000109834, abs=RATE)
    assert p.claims(2, "LUMP") == pytest.approx(32.9501, abs=5e-5)
    assert p.pols_entry_n(2) == pytest.approx(0.0000073436, abs=RATE)
    assert p.claims(2, "ANNUITY") == pytest.approx(4.4062, abs=5e-5)
    assert p.expenses(2) == pytest.approx(245.8194, abs=5e-5)
    assert p.expenses(2) + p.claim_expenses(2) == pytest.approx(
        245.9111, abs=5e-5)                                    # 245.8194 + 0.0916


def test_policy_year_1_in_aggregate(jp_ltc_anchor):
    """The notes' year-1 totals, the closing ledgers and the two in-force sums.

    The gap between the sum of ``pols_if`` and the sum of ``pols_act`` — 0.001003 over the
    year — is the waiver already biting in policy year 1, on a block where nothing has been
    claimed yet.
    """
    p = jp_ltc_anchor
    ts = range(12)
    assert sum(p.pols_if(t) for t in ts) == pytest.approx(11.461077, abs=INFORCE)
    assert sum(p.pols_act(t) for t in ts) == pytest.approx(11.460074, abs=INFORCE)
    assert sum(p.premiums(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["premiums"], abs=YEN)
    assert sum(p.claims(t, "LUMP") for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["claims_lump"], abs=YEN)
    assert sum(p.claims(t, "ANNUITY") for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["claims_annuity"], abs=YEN)
    assert sum(p.expenses(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["expenses"], abs=YEN)
    assert sum(p.claim_expenses(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["claim_expenses"], abs=YEN)
    assert sum(p.expenses(t) + p.claim_expenses(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["expenses_combined"], abs=YEN)
    assert sum(p.commissions(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["commissions"], abs=YEN)
    assert sum(p.net_cf(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_YEAR_1["net_cf"], abs=YEN)
    assert p.pols_if(12) == pytest.approx(0.903774, abs=INFORCE)
    assert p.care_w(12) == pytest.approx(0.000179, abs=INFORCE)
    assert p.care_l(12) == pytest.approx(0.000127, abs=INFORCE)
    assert p.care_n(12) == pytest.approx(0.000085, abs=INFORCE)


def test_year_one_claims_are_a_third_of_a_percent_of_year_one_premium(jp_ltc_anchor):
    """The notes' "what the numbers say": 0.33%, an order thinner than the medical chassis.

    This product prefunds a cost that essentially does not arise for twenty-five years,
    which is the fact behind the notes' first sensitivity — lapse, not incidence, is the
    dominant lever. A model that had turned the prevalence into a claim frequency would
    show a year-1 ratio two or three orders of magnitude larger and would still look
    plausible row by row.
    """
    p = jp_ltc_anchor
    claims = sum(p.claims(t) for t in range(12))
    premiums = sum(p.premiums(t) for t in range(12))
    assert claims == pytest.approx(435.41, abs=YEN)
    assert claims / premiums == pytest.approx(0.0033, abs=5e-5)


# The notes' entry-rate ladder into 要介護2以上 by attained age, section (c) step 4.
# Every rate is an output of the shipped [std] proxy mortality, because the identity's
# second term reads the mortality basis at every age. Under the canonical table six of
# these ages - 60, 65, 75, 80, 85 and 90 for a male - sit on a rate quoted from
# 第三分野標準生命表2018 rather than on an interpolated one; 64 and 70 are interpolated.
NOTES_INCIDENCE_LADDER = {
    60: 0.000134,
    64: 0.000295,
    65: 0.001795,
    70: 0.004795,
    75: 0.012413,
    80: 0.030456,
    85: 0.065003,
    90: 0.115568,
}


def test_the_notes_entry_rate_ladder_by_age(jp_ltc_anchor):
    """The notes' eight quoted entry rates into 要介護2以上, to the six decimals they show.

    This ladder is the model's most exposed contract with the document, because it is the
    one place where the two must agree at ages other than the pinned age 60. The identity's
    second term is ``prev_G x (k - 1) x mort_rate(x)``, so every rate above 60 reads the
    mortality basis — which means a change to ``mort_table.csv`` moves this list and nothing
    else in the worked example. The notes say so in terms, and this test is what holds the
    two documents together when it happens.

    The 65-to-90 gradient the notes quote is a factor of 64, and the whole span from the
    gated rate at 60 to the ungated rate at 90 is a factor of 862.
    """
    p = jp_ltc_anchor
    for age, rate in NOTES_INCIDENCE_LADDER.items():
        t = 12 * (age - 60)
        assert p.age(t) == age
        assert p.inc_rate_l(t) == pytest.approx(rate, abs=5e-7), age
    assert (NOTES_INCIDENCE_LADDER[90] / NOTES_INCIDENCE_LADDER[65]
            == pytest.approx(64, abs=0.5))
    assert (p.inc_rate_l(12 * 30) / p.inc_rate_l(0)) == pytest.approx(862, abs=1.0)


def test_new_business_strain_then_thin_positive_margins(jp_ltc_anchor):
    """The characteristic shape of the block, asserted rather than described.

    A deep month-0 strain from the upfront commission and acquisition expense against one
    month's premium, then thin positive margins for nineteen years, then a negative tail
    once the incidence curve has overtaken the level premium. The crossover falls in policy
    month 228, at attained age 79 — long before the claims themselves peak.
    """
    p = jp_ltc_anchor
    assert p.net_cf(0) < -200_000.0
    assert all(p.net_cf(t) > 0.0 for t in (1, 2, 3, 60, 120, 180))
    first_negative = next(t for t in range(1, p.proj_len()) if p.net_cf(t) < 0.0)
    assert first_negative == 228 and p.age(first_negative) == 79
    assert all(p.net_cf(t) < 0.0 for t in (240, 300, 360))


# ---------------------------------------------------------------------------
# The notes' known modeling pitfalls, one test each


def test_pitfall_certification_rate_is_a_prevalence_not_an_incidence(jp_ltc_anchor):
    """認定率 is a point-in-time proportion; the entry rate is orders of magnitude smaller.

    Multiplying the published 19.4% — or its 50.8% 要介護2以上 share — by a benefit amount,
    or treating it as an annual claim frequency, is the notes' first-listed pitfall and the
    single commonest error in a Japanese nursing-care model. The conversion is the two-term
    identity, and at the anchor age its output is 0.000134 a year against a prevalence of
    0.0033.
    """
    p = jp_ltc_anchor
    assert p.prev_grade(0, "care2") == pytest.approx(0.0032634155, abs=RATE)
    assert p.inc_rate_l(0) == pytest.approx(0.0001340450, abs=RATE)
    assert p.inc_rate_l(0) < p.prev_grade(0, "care2") / 20
    # A prevalence is dimensionless and a rate is per year: the identity adds two rates.
    assert p.inc_rate_l(0) == pytest.approx(
        p.f_age(0) * (
            p.grade_share("care2") * p.prev_slope(0) / (1.0 - p.prev_grade(0, "care2"))
            + p.prev_grade(0, "care2") * (2.75 - 1.0) * p.mort_rate(0)),
        rel=1e-12)


def test_pitfall_the_excess_mortality_term_is_not_a_refinement(tmp_path):
    """Setting the care-state multiple to 1 drops the second term and cuts claims by ~31%.

    A rising prevalence understates incidence, because the certified population is
    simultaneously being drained by its own excess mortality. Dropping the term — which is
    what happens if the multiple is set to 1 "because there is no impaired-life table" —
    cuts lifetime lump-sum claims on the anchor cell by about 31%, and the notes put the
    figure at 31.0%. The multiple is a ``Projection`` Reference, so the run is made on a
    model instance of this test's own rather than on the shared fixture.
    """
    model = mx.read_model(MODEL_DIR, name="LTC_JP_S_k1")
    try:
        p = model.Projection[1]
        base = sum(p.claims(t, "LUMP") for t in range(p.proj_len()))
        share_at_60 = 1.0 - (
            p.grade_share("care2") * p.prev_slope(0) / (1.0 - p.prev_grade(0, "care2"))
        ) / (p.inc_rate_l(0) / p.f_age(0))
        assert share_at_60 == pytest.approx(0.058, abs=0.001)     # 5.8% at age 60
        model.Projection.care_mort_mult = 1.0
        model.Projection.clear_all()
        q = model.Projection[1]
        assert q.inc_rate_l(0) == pytest.approx(
            q.f_age(0) * q.grade_share("care2") * q.prev_slope(0)
            / (1.0 - q.prev_grade(0, "care2")), rel=1e-12)
        without = sum(q.claims(t, "LUMP") for t in range(q.proj_len()))
        assert 1.0 - without / base == pytest.approx(0.31, abs=0.01)
    finally:
        model.close()


def test_pitfall_the_care_state_is_absorbing_and_the_benefit_does_not_stop(
        nursing_care, tmp_path):
    """``rec_rate`` is a named input set to zero, and the ``state`` switch needs it to bite.

    On the composite's survival-tested annuity a recovery does not stop payment and a paid
    lump sum cannot be unpaid, so recovery has nothing to act on: the base run's zero is a
    modelling position, not an omission. The switch and the rate must therefore be tested
    together — with ``rec_rate = 0`` the ``state`` test reproduces the ``survival`` test
    cash flow for cash flow, which is exactly what the notes say it does.
    """
    p1 = nursing_care.Projection[1]
    assert p1.rec_rate() == 0.0 and p1.rec_rate_mth() == 0.0
    assert p1.care_surv(0, 12) == pytest.approx(
        (1.0 - p1.mort_rate_care_mth(0)) ** 12, rel=1e-12)

    noop = variant_model(tmp_path, "LTC_JP_S_stateoff", 5, rec_rate=0.0)
    try:
        state_no_recovery = noop.Projection[5].result_cf()
    finally:
        noop.close()
    survival = variant_model(
        tmp_path, "LTC_JP_S_surv", 5, rec_rate=0.0, annuity_test="survival")
    try:
        assert (state_no_recovery - survival.Projection[5].result_cf()
                ).abs().max().max() == pytest.approx(0.0, abs=1e-12)
    finally:
        survival.close()


def test_pitfall_lapse_stops_at_the_waiver_trigger(jp_ltc_anchor):
    """Lapse is taken from ``pols_act`` only; lives on waiver carry mortality alone.

    Once 要介護1以上 is certified the premium is waived and treated as paid, so there is no
    premium to miss, and with no 解約返戻金 there is nothing to surrender for. Applying lapse
    to ``pols_if`` destroys the annuity liability it took thirty years to build.
    """
    p = jp_ltc_anchor
    t = 240
    survivors = (p.pols_act(t) - p.pols_entry_w(t)) * (1.0 - p.mort_rate_mth(t))
    assert p.pols_lapse(t) == pytest.approx(survivors * p.lapse_rate_mth(t), rel=1e-12)
    assert p.care_w(t) > 0.0
    assert p.pols_lapse(t) < p.pols_if(t) * p.lapse_rate_mth(t)
    # The care ledgers roll forward on mortality alone: no lapse term anywhere in them.
    assert p.care_l(t + 1) == pytest.approx(
        (p.care_l(t) + p.pols_entry_l(t)) * (1.0 - p.mort_rate_care_mth(t))
        - p.pols_term(t), rel=1e-12)


def test_pitfall_premium_income_rides_on_pols_act_never_on_pols_if(nursing_care):
    """Charging premium to the whole in-force block overstates lifetime income by 5.85%.

    The waiver fires two grades below the annuity and one below the lump sum, so there is a
    real band of lives for whom the contract has stopped collecting premium and has not yet
    paid anything. At age 85 the notes put that band at 30.1% of the surviving block.

    The two readings of the same yen are asserted separately, because conflating them is
    itself an error: the waiver takes 5.53% out of the in-force-weighted premium, which
    means the in-force-weighted figure **overstates** the correct one by 5.85%.
    """
    p = nursing_care.Projection[1]
    ts = range(p.proj_len())
    on_act = sum(p.premiums(t) for t in ts)
    on_if = sum(p.premium_mth_pp() * p.pols_if(t) for t in ts)
    assert on_act < on_if
    assert on_if - on_act == pytest.approx(92_738.26, abs=0.01)
    assert 1.0 - on_act / on_if == pytest.approx(0.0553, abs=0.0005)
    assert on_if / on_act - 1.0 == pytest.approx(0.0585, abs=0.0005)
    t85 = 12 * 25
    assert p.care_w(t85) / p.pols_if(t85) == pytest.approx(0.301, abs=0.002)
    # Renewal commission rides on the premium, so it stops when the waiver stops it.
    assert p.commissions(t85) == pytest.approx(0.03 * p.premiums(t85), rel=1e-12)


def test_pitfall_the_three_care_ledgers_are_nested_and_never_summed(nursing_care):
    """care_n <= care_l <= care_w <= pols_if at every t, on every shipped model point.

    They are three marginal first-entry distributions riding on one survival ledger, not
    three disjoint compartments. Independent entry hazards without the ordering let a life
    start the annuity before its lump sum has been paid, which the contract forbids — the
    unpaid lump sum is paid *with* the first instalment. Only ``care_w`` is a component of
    ``pols_if``; adding the three ledgers together counts the same lives three times.
    """
    for point_id in nursing_care.Data.model_point_table().index:
        p = nursing_care.Projection[point_id]
        assert p.check_nesting() is True, point_id
        for t in (0, 1, 120, 360, p.proj_len() - 1):
            assert p.check_nesting_resid(t) >= -1e-12
            assert p.care_n(t) <= p.care_l(t) <= p.care_w(t) <= p.pols_if(t) + 1e-12
            assert p.pols_if(t) == pytest.approx(p.pols_act(t) + p.care_w(t), rel=1e-12)
    p = nursing_care.Projection[1]
    t = 480
    assert p.care_l(t) > 0.0 and p.care_n(t) > 0.0
    assert p.care_l(t) + p.care_n(t) > p.care_w(t)      # so the sum is not a population


def test_pitfall_the_ten_payment_cap_binds(nursing_care, tmp_path):
    """Entrants take 4.62 instalments on average and 15% of them reach the tenth.

    The 通算 day ledger that reads zero forever on the ``medical`` chassis has no
    counterpart here: ``pols_term`` is non-zero, the average instalment count sits strictly
    inside ``(1, n_A)``, and removing the cap raises lifetime annuity cost by about 11%.
    """
    p = nursing_care.Projection[1]
    ts = range(p.proj_len())
    entrants = sum(p.pols_entry_n(t) for t in ts)
    instalments = sum(p.ann_count(t) for t in ts)
    terminations = sum(p.pols_term(t) for t in ts)
    capped = sum(p.claims(t, "ANNUITY") for t in ts)
    assert entrants > 0.0
    assert 1.0 < instalments / entrants < p.annuity_max()
    assert instalments / entrants == pytest.approx(4.62, abs=0.05)
    assert terminations / entrants == pytest.approx(0.149, abs=0.005)

    uncapped = variant_model(tmp_path, "LTC_JP_S_nocap", 1, annuity_max=60)
    try:
        q = uncapped.Projection[1]
        assert sum(q.pols_term(t) for t in range(q.proj_len())) == 0.0
        assert sum(q.claims(t, "ANNUITY") for t in range(q.proj_len())) / capped - 1.0 \
            == pytest.approx(0.114, abs=0.005)
    finally:
        uncapped.close()


def test_pitfall_the_annuity_is_in_advance_and_starts_on_the_entry_date(jp_ltc_anchor):
    """The j = 0 term of ``ann_count`` is ``pols_entry_n`` itself.

    The month-0 cohort is paid at once, is **not** paid again at t = 1, and is paid again
    at t = 12 — which is what distinguishes an in-advance annuity from a deferred one.
    Deferring the first instalment by a year removes roughly a tenth of the annuity
    liability and misdates all of it.
    """
    p = jp_ltc_anchor
    assert p.ann_count(0) == pytest.approx(p.pols_entry_n(0), rel=1e-12)
    assert p.ann_count(1) == pytest.approx(p.pols_entry_n(1), rel=1e-12)
    second = p.pols_entry_n(0) * p.care_surv(0, 12)
    assert second > 0.0
    assert p.ann_count(12) == pytest.approx(p.pols_entry_n(12) + second, rel=1e-12)
    assert p.claims(0, "ANNUITY") > 0.0                # paid in the month of entry


def test_pitfall_care_state_survival_is_a_partial_product(jp_ltc_anchor):
    """``care_surv`` is multiplicative in the middle point and survives the terminal age.

    A ratio of cumulative products divides by zero at the terminal age, where the
    care-state mortality rate reaches 1 — which is exactly where the tail of this liability
    lives. The partial product simply returns zero there, and the ledger keeps closing.
    """
    p = jp_ltc_anchor
    s, mid, t = 300, 348, 408
    assert p.care_surv(s, t) == pytest.approx(
        p.care_surv(s, mid) * p.care_surv(mid, t), rel=1e-12)
    assert p.care_surv(t, t) == 1.0
    last = p.proj_len() - 1
    assert p.mort_rate_care(last) == 1.0
    assert p.care_surv(last - 1, last + 1) == 0.0
    assert p.check_ann_ledger() is True                # the tail still closes


def test_pitfall_there_is_a_step_in_incidence_at_exactly_age_65(nursing_care):
    """Entry into 要介護2以上 jumps 6.1x between age 64 and age 65, and it belongs there.

    Below 65 the public limb fires only on one of the 16 特定疾病, and the company-basis
    limb that partly fills the hole is restricted to lives 満65歳未満. A smooth curve through
    65 misprices every issue age in the lower half of the 40-79 issue range, which is most
    of it.
    """
    p = nursing_care.Projection[1]
    t64, t65 = 12 * 4, 12 * 5
    assert p.age(t64) == 64 and p.age(t65) == 65
    assert p.f_age(t64) == 0.20 and p.f_age(t65) == 1.0
    assert p.inc_rate_l(t65) / p.inc_rate_l(t64) == pytest.approx(6.1, abs=0.1)
    # The step is the gate alone: the ungated identity is smooth across the birthday.
    ungated_64 = p.inc_rate_l(t64) / p.f_age(t64)
    ungated_65 = p.inc_rate_l(t65) / p.f_age(t65)
    assert 1.0 < ungated_65 / ungated_64 < 1.3


def test_pitfall_180_days_names_two_mechanisms_and_only_one_is_a_waiting_period(
        nursing_care):
    """A persistence test is not a 不担保期間, and the composite has no 不担保期間 on care.

    "180日" names two different mechanisms in this market: a 不担保期間 or a
    認知症診断責任開始期 means cover has not started, while the 180-day (90-day for dementia)
    test inside the company-basis trigger means the care state must have *persisted*. The
    composite carries the second and not the first on the care benefits, so a model that
    implemented the persistence test as a waiting period would suppress a year of claims
    that the contract pays. The one waiting period in the model belongs to the rider alone.
    """
    p = nursing_care.Projection[1]
    assert p.company_limb() is True            # the 180-day persistence test is written
    assert p.waiting_1y() is False and p.waiting_mths() == 0
    assert p.inc_rate_l_mth(0) > 0.0
    assert p.claims(0, "LUMP") > 0.0           # and the claim is dated at month 0
    # The rider's 認知症診断責任開始期 is six months and applies to the rider alone.
    p6 = nursing_care.Projection[6]
    assert p6.waiting_mths() == 0
    assert p6.dem_inc_rate_mth(5) == 0.0
    assert p6.dem_inc_rate_mth(6) > 0.0
    assert p6.claims(0, "LUMP") > 0.0


def test_pitfall_no_surrender_value_no_apl_and_no_death_benefit(nursing_care):
    """Three absences that are product facts, asserted so they cannot be added back.

    There is no 解約返戻金 at any duration, so a lapse pays nothing and there is nothing for
    an 自動振替貸付 to lend against; the contract terminates on death with nothing payable.
    Importing the ``whole_life`` 自動振替貸付 logic suppresses lapses that really happen, and
    adding a death benefit invents one that does not exist. ``claims_lapse`` is published as
    a column of zeros rather than dropped, because a missing column would hide the fact.
    """
    p = nursing_care.Projection[1]
    cells = set(nursing_care.Projection.cells) | set(nursing_care.Projection.refs)
    assert "cv_pp" not in cells
    assert "claims_death" not in cells
    assert not [c for c in cells if "apl" in c or "auto_prem" in c or "surr" in c]
    for t in (0, 60, 360):
        assert p.claims(t, "LAPSE") == 0.0
    df = p.result_cf()
    assert "claims_lapse" in df.columns
    assert (df["claims_lapse"] == 0.0).all()
    assert p.pols_lapse(60) > 0.0                      # the decrement is real
    with pytest.raises(FormulaError):
        p.claims(0, "DEATH")


def test_pitfall_the_prevalence_tail_is_an_unsourced_extrapolation(nursing_care):
    """Above age 82 the curve is extrapolation, and 40% of the claims are up there.

    The logistic has **three** parameters and **two** sourced anchors, so one degree of
    freedom is not identified by the data at all — and the free one, ``prev_ceil``, is
    precisely the one that sets the tail. ``prev(90) = 0.662`` and ``prev(100) = 0.894``
    are therefore outputs of a **[std]** choice, not fitted values, and no retrieved
    document reports a 認定率 at any age above the 75+ band.

    The reason that matters, and the reason this is a first-order model risk rather than a
    detail of the fit: on the anchor cell 40.2% of lifetime benefit outgo falls at attained
    age 83 or over, and on the oldest shipped issue age it is 74.7%. Quoting a tail rate as
    though it carried the [R4] [REG-R30] provenance of the two anchors would misrepresent
    where this model's evidence stops, so both rates and both shares are pinned here.
    """
    table = nursing_care.Data.prevalence_table()
    assert "[std]" in table.loc["prev_ceil", "provenance"]
    assert "no sourced value" in table.loc["prev_ceil", "provenance"]

    p = nursing_care.Projection[1]
    assert p.prev_rate(12 * 30) == pytest.approx(0.662, abs=5e-4)      # age 90
    assert p.prev_rate(12 * 40) == pytest.approx(0.894, abs=5e-4)      # age 100

    def extrapolated_share(point_id):
        q = nursing_care.Projection[point_id]
        df = q.result_cf()
        benefit = df["claims_lump"] + df["claims_annuity"]
        above = sum(benefit.iloc[t] for t in range(q.proj_len())
                    if q.age(t) >= 83)
        return above / benefit.sum()

    assert extrapolated_share(1) == pytest.approx(0.402, abs=5e-4)
    assert extrapolated_share(8) == pytest.approx(0.747, abs=5e-4)


# ---------------------------------------------------------------------------
# Roll-forward identities and the check_* cells


def test_the_four_check_cells_are_published_with_their_residuals(nursing_care):
    """These four ``check_*`` cells are published, and no others, each with its residual.

    ``check_pols_roll_fwd`` closes the in-force against the month's decrements,
    ``check_nesting`` the ledger ordering, ``check_ann_ledger`` the annuity ledger against
    an independent rebuild, and ``check_net_cf`` the cash flow statement against
    ``net_cf``. Each returns a bool over all t, with the signed per-month residual at
    ``<name>_resid(t)``.

    That they *hold*, on all eight model points, is asserted in
    ``test_model_conventions_jp.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library. Running them again here,
    on a second instance of the same model, meant a second cold projection of the whole
    table to reach a verdict already reached.

    Generic discovery cannot notice a check that has *gone*: it simply stops being
    discovered. Naming the set is the statement left here.
    """
    checks = ("check_pols_roll_fwd", "check_nesting", "check_ann_ledger",
              "check_net_cf")
    cells = set(nursing_care.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(checks)
    for check in checks:
        assert check + "_resid" in cells, check


def test_the_in_force_roll_forward_names_every_decrement(nursing_care):
    """Deaths, lapses and the benefit-driven termination are the only ways out.

    There is no maturity and no recovery out of ``pols_if``, so nothing else may move it.
    The identity is asserted directly, on every model point, rather than only through the
    check cells that compute it.
    """
    for point_id in nursing_care.Data.model_point_table().index:
        p = nursing_care.Projection[point_id]
        for t in (0, 11, 120, min(480, p.proj_len() - 2)):
            assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(
                p.pols_death(t) + p.pols_lapse(t) + p.pols_term(t), abs=1e-12)


def test_the_annuity_ledger_closes_against_an_independent_rebuild(jp_ltc_anchor):
    """``check_ann_ledger`` scans every month in the cap window instead of stepping in 12s.

    A ledger that paid the first instalment a year late, that ran past the cap, or that
    used a ratio form of ``care_surv`` shows up in the residual rather than in the totals,
    where it would be invisible.
    """
    p = jp_ltc_anchor
    assert p.check_ann_ledger() is True
    for t in (0, 1, 12, 130, 400):
        assert p.check_ann_ledger_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_net_cf_re_adds_from_the_published_columns(jp_ltc_anchor):
    """``check_net_cf`` re-adds the statement from exactly the columns ``result_cf`` prints.

    A cash flow that exists in ``net_cf`` but not in the statement, or the reverse, shows up
    here — which is the failure a reader of the printed table could never see.
    """
    p = jp_ltc_anchor
    assert p.check_net_cf() is True
    for t in (0, 1, 12, 360):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)


def test_pols_if_at_reads_the_month_in_order(jp_ltc_anchor):
    """The processing order: incidence, then mortality, then lapse, then termination."""
    p = jp_ltc_anchor
    t = 120
    assert p.pols_if_at(t, "BEF_DECR") == p.pols_if(t)
    assert p.pols_if_at(t, "AFT_DECR") == p.pols_if(t + 1)
    assert p.pols_if(t) > p.pols_if_at(t, "BEF_LAPSE") > p.pols_if(t + 1)
    assert p.pols_if(t) - p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
        p.pols_death(t), abs=1e-14)
    with pytest.raises(FormulaError):
        p.pols_if_at(t, "NOWHERE")


def test_in_force_is_a_decreasing_probability(jp_ltc_anchor):
    """One policy at outset, never more, and never rising."""
    p = jp_ltc_anchor
    assert p.pols_if(0) == 1.0
    for t in range(0, p.proj_len(), 24):
        assert 0.0 <= p.pols_if(t) <= 1.0
        assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15
    assert p.pols_if(p.proj_len()) == 0.0


# ---------------------------------------------------------------------------
# The optional modules, each in both positions


def test_the_state_tested_annuity_is_off_on_the_anchor_and_on_at_point_5(nursing_care):
    """Recovery cuts point 5's lifetime annuity claims by about 12%.

    The composite's annuity is survival-tested — four carriers against one — so the anchor
    carries no recovery decrement at all. Point 5 carries the ``state`` switch together with
    the notes' suggested 5% p.a. placeholder, which is the only combination in which either
    does anything: recovery is scoped to the annuity ledger, so the lump sum, once paid,
    stays paid.
    """
    p1 = nursing_care.Projection[1]
    assert p1.annuity_test() == "survival" and p1.rec_rate() == 0.0
    p5 = nursing_care.Projection[5]
    assert p5.annuity_test() == "state"
    assert p5.rec_rate() == 0.05
    assert p5.rec_rate_mth() == pytest.approx(1 - 0.95 ** (1 / 12), rel=1e-12)
    assert sum(p5.claims(t, "ANNUITY") for t in range(p5.proj_len())) == pytest.approx(
        360_416.0, rel=5e-4)
    assert p5.care_surv(0, 12) == pytest.approx(
        (1.0 - p5.mort_rate_care_mth(0)) ** 12 * (1.0 - p5.rec_rate_mth()) ** 12,
        rel=1e-12)


def test_recovery_only_touches_the_annuity_limb(nursing_care, tmp_path):
    """The lump sum, once paid, cannot be unpaid, so recovery must not move ``claims_lump``.

    Scoping the recovery decrement to the annuity ledger is a **[std scope]** decision the
    notes name; a recovery decrement applied to ``care_l`` would let the same life claim the
    once-only lump sum twice.
    """
    p5 = nursing_care.Projection[5]
    with_recovery = sum(p5.claims(t, "LUMP") for t in range(p5.proj_len()))
    model = variant_model(tmp_path, "LTC_JP_S_rec0", 5, rec_rate=0.0)
    try:
        q = model.Projection[5]
        without = sum(q.claims(t, "LUMP") for t in range(q.proj_len()))
        assert with_recovery == pytest.approx(without, rel=1e-12)
        annuity_without = sum(q.claims(t, "ANNUITY") for t in range(q.proj_len()))
    finally:
        model.close()
    annuity_with = sum(p5.claims(t, "ANNUITY") for t in range(p5.proj_len()))
    assert 1.0 - annuity_with / annuity_without == pytest.approx(0.124, abs=0.005)


def test_a_recovered_life_keeps_its_waiver_for_life(nursing_care, tmp_path):
    """The documented limit of the ``state`` switch, pinned so it cannot become silent.

    ``rec_rate`` is the rate of falling **below the annuity grade** ``G_N`` = 要介護3, not a
    recovery-to-health rate, and it is applied to ``care_n`` alone. So a life it moves
    leaves the annuity ledger and may re-qualify on a new 介護年金支払基準日, but stays in
    ``care_w``: it never re-enters ``pols_act``, never resumes premium and is never again
    exposed to lapse.

    For the step modelled that is contractually right — ``G_W`` = 要介護1 is two grades below
    ``G_N``, so a 要介護3 → 要介護2 downgrade stops a state-tested annuity and leaves the waiver
    running. Recovery *below* ``G_W`` is **not modelled**, because no retrieved source
    publishes a between-grade transition matrix and one rate cannot carry two thresholds.
    The direction of the resulting bias is known and asserted here: premium income under
    that switch is a **lower bound**, because it is identical to the run with no recovery
    at all even though the annuity ledger is materially smaller.
    """
    p5 = nursing_care.Projection[5]
    assert p5.annuity_test() == "state" and p5.rec_rate() == 0.05
    model = variant_model(tmp_path, "LTC_JP_S_waiver_rec0", 5, rec_rate=0.0)
    try:
        q = model.Projection[5]
        n = p5.proj_len()
        assert q.proj_len() == n
        # recovery is doing something: the annuity ledger is materially smaller
        assert p5.care_n(12 * 30) < 0.98 * q.care_n(12 * 30)
        # ... and nothing whatever to the active block or the premium it pays
        for t in (0, 12 * 10, 12 * 25, 12 * 40):
            assert p5.pols_act(t) == pytest.approx(q.pols_act(t), rel=1e-12)
        assert sum(p5.premiums(t) for t in range(n)) == pytest.approx(
            sum(q.premiums(t) for t in range(n)), rel=1e-12)
        # the waiver ledger moves only *upward*, and only through the annuity cap:
        # a recovered life takes no tenth instalment, so `pols_term` extinguishes fewer
        # contracts. It is never released back to `pols_act`.
        for t in (12 * 25, 12 * 40):
            assert p5.care_w(t) > q.care_w(t)
        assert sum(p5.pols_term(t) for t in range(n)) < sum(
            q.pols_term(t) for t in range(n))
    finally:
        model.close()


def test_the_anti_selective_lapse_module_is_off_on_the_anchor_and_on_at_point_8(
        nursing_care):
    """``lam = 0`` leaves the loading at 1.0; point 8 turns it on and loads *incidence*.

    Healthy lives lapse first, so the persisting block is progressively impaired on the
    incidence basis rather than on mortality — the opposite direction from a death-benefit
    product, which is why the loading sits on ``inc_rate_mth``. It bites only once
    cumulative lapse has passed the 20% reference point.
    """
    p1 = nursing_care.Projection[1]
    assert p1.sel_lapse_lambda() == 0.0
    for t in (0, 120, 480):
        assert p1.sel_lapse_factor(t) == 1.0
        assert p1.inc_rate_l_mth(t) == pytest.approx(p1.inc_rate_l(t) / 12.0, rel=1e-12)
    p8 = nursing_care.Projection[8]
    assert p8.sel_lapse_lambda() == 0.30
    assert p8.sel_lapse_factor(0) == 1.0             # nothing has lapsed yet
    late = p8.proj_len() - 1
    assert p8.lapse_cum(late) > 0.20
    assert p8.sel_lapse_factor(late) == pytest.approx(
        1.0 + 0.30 * (p8.lapse_cum(late) - 0.20), rel=1e-12)
    assert p8.inc_rate_l_mth(late) > p8.inc_rate_l(late) / 12.0


def test_the_dementia_rider_is_off_on_the_anchor_and_on_at_point_6(nursing_care):
    """The 認知症一時金特約 pays ``(1 + mci_fraction) x dementia_amount`` per first diagnosis.

    The rider's incidence has no published basis in any retrieved source, so it is a
    **[std]** placeholder: a share of the entry rate into the lump-sum grade, after a
    six-month 認知症診断責任開始期. The MCI limb and the dementia limb are carried as one event
    at the dementia date, which gets the amount right and dates the 10% MCI limb late.
    """
    p1 = nursing_care.Projection[1]
    p6 = nursing_care.Projection[6]
    assert p1.dementia_rider() is False
    assert sum(p1.claims(t, "DEMENTIA") for t in range(p1.proj_len())) == 0.0
    assert all(p1.dem_inc_rate_mth(t) == 0.0 for t in (0, 6, 120))
    assert p6.dementia_rider() is True
    assert p6.dem_inc_rate_mth(12) == pytest.approx(0.35 * p6.inc_rate_l_mth(12),
                                                    rel=1e-12)
    on = sum(p6.claims(t, "DEMENTIA") for t in range(p6.proj_len()))
    assert on == pytest.approx(47_673.0, rel=5e-4)
    t = 300
    assert p6.claims(t, "DEMENTIA") == pytest.approx(
        1.1 * 1_000_000.0 * p6.pols_entry_dem(t), rel=1e-12)
    assert p6.care_dem(t) <= p6.pols_if(t)           # a first-event counter, not a sum


def test_the_one_year_waiting_period_is_off_on_the_anchor_and_on_at_point_7(
        nursing_care, tmp_path):
    """``waiting_1y`` zeroes the entry rates for twelve months, on every benefit limb.

    A state arising inside the 不担保期間 is excluded for good rather than deferred, which is
    why the flag zeroes incidence rather than claims. It is the explicit price of
    three-question simplified underwriting; the composite is fully underwritten and does not
    carry it. Forcing it off on the same model point recovers the year-1 claims it excludes.
    """
    p1 = nursing_care.Projection[1]
    assert p1.waiting_mths() == 0 and sum(p1.claims(t) for t in range(12)) > 0.0
    p7 = nursing_care.Projection[7]
    assert p7.waiting_1y() is True and p7.waiting_mths() == 12
    for t in range(12):
        assert p7.inc_rate_l_mth(t) == 0.0
        assert p7.pols_entry_l(t) == 0.0
        assert p7.claims(t) == 0.0
    assert p7.inc_rate_l_mth(12) > 0.0
    assert sum(p7.claims(t) for t in range(p7.proj_len())) > 0.0

    model = variant_model(tmp_path, "LTC_JP_S_nowait", 7, waiting_1y=False)
    try:
        q = model.Projection[7]
        assert q.waiting_mths() == 0
        assert sum(q.claims(t) for t in range(12)) == pytest.approx(2.8694, abs=5e-4)
    finally:
        model.close()


def test_the_company_basis_limb_is_written_on_the_anchor_and_off_at_point_4(nursing_care):
    """The limb's only effect in this model is the height of the sub-65 gate.

    It is an alternative 約款-defined trigger for lives 満65歳未満, adjudicated against a
    definition the carrier itself says differs from the public certification standard, so it
    is not modelled as a separate decrement. Writing it off drops the gate from 0.20 to
    0.05 and cuts pre-65 incidence by three quarters; at 65 and over both settings are 1.00.
    """
    p1 = nursing_care.Projection[1]
    assert p1.company_limb() is True and p1.f_age(0) == 0.20
    p4 = nursing_care.Projection[4]
    assert p4.company_limb() is False
    assert p4.issue_age() == 45
    assert p4.f_age(0) == 0.05
    assert p4.f_age(12 * 20) == 1.0 and p4.age(12 * 20) == 65
    ungated = p4.inc_rate_l(0) / p4.f_age(0)
    assert p4.inc_rate_l(0) == pytest.approx(0.05 * ungated, rel=1e-12)
    assert p4.inc_rate_l(0) == pytest.approx(0.25 * 0.20 * ungated, rel=1e-12)


# ---------------------------------------------------------------------------
# The notes' key sensitivities, held in place


def test_sensitivity_lapse_not_incidence_is_the_dominant_lever(nursing_care, tmp_path):
    """34.7% of lifetime premium on the base table, 53.5% with lapse off, 43.5% at half.

    The notes' first sensitivity, and the reason it is first: the claims are twenty-five
    years out and the [std] lapse table removes most of the block before they arrive, so
    persistency moves the lifetime loss ratio further than the morbidity basis does. The
    only sourced anchor is a 5.6% sum-assured-weighted industry figure measured on a book of
    death cover, which is why the table's *shape* is the standardization it is.
    """
    base = lifetime(nursing_care.Projection[1])
    assert base["claims"] / base["premiums"] == pytest.approx(0.347, abs=0.001)

    off = variant_table(tmp_path, "LTC_JP_S_nolapse", "lapse_table.csv",
                        lambda t: t.assign(lapse_rate=0.0))
    try:
        r = lifetime(off.Projection[1])
        assert r["claims"] / r["premiums"] == pytest.approx(0.535, abs=0.001)
    finally:
        off.close()

    half = variant_table(tmp_path, "LTC_JP_S_halflapse", "lapse_table.csv",
                         lambda t: t.assign(lapse_rate=t["lapse_rate"] * 0.5))
    try:
        r = lifetime(half.Projection[1])
        assert r["claims"] / r["premiums"] == pytest.approx(0.435, abs=0.001)
    finally:
        half.close()


def test_sensitivity_the_care_state_multiple_pulls_the_two_limbs_opposite_ways(
        nursing_care):
    """k = 4 raises lump-sum claims 12.4% and cuts annuity claims 8.3%, at the same time.

    ``k`` is the model's one parameter with two jobs: it is the excess-mortality term of the
    incidence identity *and* it is how fast the annuity runs off. Heavier post-onset
    mortality therefore lengthens the incidence it shortens the annuity into, and a
    sensitivity run that reported only a total would net the two against each other and show
    almost nothing.
    """
    base = lifetime(nursing_care.Projection[1])
    model = mx.read_model(MODEL_DIR, name="LTC_JP_S_k4")
    try:
        model.Projection.care_mort_mult = 4.0
        model.Projection.clear_all()
        r = lifetime(model.Projection[1])
        assert r["claims_lump"] / base["claims_lump"] - 1.0 == pytest.approx(
            0.124, abs=0.002)
        assert r["claims_annuity"] / base["claims_annuity"] - 1.0 == pytest.approx(
            -0.083, abs=0.002)
    finally:
        model.close()


def test_sensitivity_the_constant_grade_composition(nursing_care, tmp_path):
    """Raising all three grade shares by 10% relative lifts lifetime claims by 7.5%.

    The published composition is one all-ages figure, so the model holds it flat across
    ages; severity mix in fact worsens with age, so the direction of the error is known and
    the size of it is not. This test fixes the model's response to the share level, which is
    what makes the unquantified direction reportable at all.
    """
    base = lifetime(nursing_care.Projection[1])
    grades = ("care1", "care2", "care3")

    def raise_shares(table):
        rows = table["grade"].isin(grades)
        table.loc[rows, "share_ge"] = table.loc[rows, "share_ge"] * 1.1
        return table

    model = variant_table(tmp_path, "LTC_JP_S_shares", "grade_share_table.csv",
                          raise_shares)
    try:
        p = model.Projection[1]
        assert p.grade_share("care2") == pytest.approx(0.508 * 1.1, rel=1e-12)
        r = lifetime(p)
        assert r["claims"] / base["claims"] - 1.0 == pytest.approx(0.075, abs=0.002)
    finally:
        model.close()


def test_sensitivity_cutting_the_cap_to_five_instalments(nursing_care, tmp_path):
    """Five instalments instead of ten cuts annuity cost by 25.9%, not by half.

    The cap is a contractual parameter at one carrier and a payout-shape election at
    another, and it is genuinely live on the expectation. Halving it removes only a quarter
    of the cost, because on the [std] basis most entrants die before the sixth instalment —
    the same fact the average of 4.62 instalments states from the other side.
    """
    base = lifetime(nursing_care.Projection[1])
    model = variant_model(tmp_path, "LTC_JP_S_cap5", 1, annuity_max=5)
    try:
        p = model.Projection[1]
        assert p.annuity_max() == 5
        r = lifetime(p)
        assert r["claims_annuity"] / base["claims_annuity"] - 1.0 == pytest.approx(
            -0.259, abs=0.003)
    finally:
        model.close()


def test_sensitivity_the_sub65_gate_moves_the_early_years_not_the_lifetime_total(
        nursing_care):
    """f_sub65 = 1 moves the loss ratio 34.7% -> 36.1%, but the first five years by 5x.

    The gate is the sixth sensitivity by lifetime leverage and the first by leverage on the
    tests: almost every early-duration figure in the notes is five times smaller because of
    it, while the lifetime totals barely notice, because on this product the lifetime totals
    are made after age 80.
    """
    base = lifetime(nursing_care.Projection[1])
    early = sum(nursing_care.Projection[1].claims(t) for t in range(60))
    model = mx.read_model(MODEL_DIR, name="LTC_JP_S_gate1")
    try:
        model.Projection.f_sub65 = 1.0
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.f_age(0) == 1.0
        r = lifetime(p)
        assert base["claims"] / base["premiums"] == pytest.approx(0.347, abs=0.001)
        assert r["claims"] / r["premiums"] == pytest.approx(0.361, abs=0.001)
        assert sum(p.claims(t) for t in range(60)) / early == pytest.approx(5.0, abs=0.1)
    finally:
        model.close()


def test_the_undiscounted_claims_against_the_two_published_premium_scales(nursing_care):
    """41.8% of the lump-sum limb's specimen premium and 27.3% of the annuity limb's.

    The two premium scales are the only sourced prices on this product, and the [std] basis
    reproduces well under half of each as undiscounted expected claims. That is low for a
    retail loss ratio, and the notes report it as the honest signal that the prevalence
    tail, the flat grade composition and the inherited lapse table are calibration targets
    rather than results — so the figure is asserted, not smoothed.
    """
    p = nursing_care.Projection[1]
    ts = range(p.proj_len())
    exposure = sum(p.pols_act(t) for t in ts)
    assert exposure == pytest.approx(137.87, abs=0.01)
    lump = sum(p.claims(t, "LUMP") for t in ts)
    annuity = sum(p.claims(t, "ANNUITY") for t in ts)
    assert lump / (5_820 * exposure) == pytest.approx(0.418, abs=0.002)
    assert annuity / (5_730 * exposure) == pytest.approx(0.273, abs=0.002)


def test_the_block_left_in_force_where_the_claims_are(jp_ltc_anchor):
    """0.126 of the block survives to age 85, which is where the liability lives.

    The two halves of the notes' first sensitivity are this number and the loss ratio: a
    product that prefunds a cost arising after 85 is priced by how much of the block is
    still there to receive it.
    """
    p = jp_ltc_anchor
    t85 = 12 * 25
    assert p.age(t85) == 85
    assert p.pols_if(t85) == pytest.approx(0.126, abs=0.001)


# ---------------------------------------------------------------------------
# Structural product facts


def test_the_waiver_fires_strictly_below_both_benefit_thresholds(nursing_care):
    """G_W < G_L < G_N, and the resulting entry rates are ordered the same way.

    That ordering is the product fact behind two of the pitfalls at once: it creates a band
    of lives paying nothing and receiving nothing, and it is what makes ``care_w`` the only
    care ledger inside ``pols_if``.
    """
    p = nursing_care.Projection[1]
    assert p.grade_share("care1") > p.grade_share("care2") > p.grade_share("care3")
    for t in (0, 120, 360):
        assert p.inc_rate_w(t) > p.inc_rate_l(t) > p.inc_rate_n(t)
        assert p.care_w(t) >= p.care_l(t) >= p.care_n(t)
    # Point 8 elects the lower pair of thresholds; the ordering still holds.
    p8 = nursing_care.Projection[8]
    assert (p8.grade_waiver(), p8.grade_lump(), p8.grade_annuity()) == (
        "care1", "care1", "care2")
    assert p8.inc_rate_w(0) >= p8.inc_rate_l(0) > p8.inc_rate_n(0)


def test_the_lump_sum_is_once_only_and_does_not_terminate_the_contract(jp_ltc_anchor):
    """Paying the 介護一時金 moves no ledger but ``care_l``; only the cap terminates.

    ``pols_entry_l`` is drawn from the lives who have not yet reached the grade, so no life
    can be paid twice, and the in-force roll-forward has no lump-sum term in it at all.
    """
    p = jp_ltc_anchor
    t = 300
    assert p.pols_entry_l(t) == pytest.approx(
        (p.pols_if(t) - p.care_l(t)) * p.inc_rate_l_mth(t), rel=1e-12)
    assert p.claims(t, "LUMP") == pytest.approx(3_000_000.0 * p.pols_entry_l(t), rel=1e-12)
    assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
    assert p.pols_term(t) > 0.0                # the only benefit-driven termination


def test_there_is_no_day_ledger_anywhere_in_this_model(nursing_care):
    """The 支払限度日数 machinery of the third-sector chassis has no counterpart here.

    ``medical`` is frequency x severity x limit — a 日額 times paid days, capped per
    hospitalization and again in aggregate. This product is incidence into an absorbing
    state, so there is no ``d_pay``, no ``d_ben``, no ``agg_days_*`` and no daily amount:
    the unit of account is an annual annuity instalment.
    """
    names = set(nursing_care.Projection.cells) | set(nursing_care.Projection.refs)
    for absent in ("d_pay", "d_ben", "agg_days_dis", "agg_days_acc", "daily_amount",
                   "benefit_days", "days_limit"):
        assert absent not in names, f"{absent} is medical-chassis day-ledger machinery"
    assert not [n for n in names if "days" in n]


def test_the_cover_is_whole_of_life_with_no_maturity(nursing_care):
    """``proj_len`` is set by the mortality table's terminal age, not by a policy term.

    Cover and premiums are both 終身, so nothing but the table ends the projection: there is
    no maturity, no maturity benefit, no renewal and no policy term to carry. What empties
    the block is the table's terminal rate of 1, which takes the survivors within the first
    month of the terminal age — and premium is still being collected in the month before it,
    because the payment period is 終身払.
    """
    for point_id, omega in ((1, 116), (2, 118)):
        p = nursing_care.Projection[point_id]
        assert p.omega_age() == omega
        assert p.proj_len() == 12 * (omega - p.issue_age() + 1)
        assert p.mort_rate(p.proj_len() - 1) == 1.0
        assert p.prem_period_type() == "whole_life"
        last_inforce = 12 * (omega - p.issue_age())      # the first month of age omega
        assert p.pols_act(last_inforce) > 0.0
        assert p.premiums(last_inforce) > 0.0
        assert p.pols_if(last_inforce + 1) == 0.0
    cells = set(nursing_care.Projection.cells)
    assert not [c for c in cells if "maturity" in c]
    assert "policy_term" not in cells


def test_the_mortality_cap_at_one_is_a_documented_guard(jp_ltc_anchor):
    """``mort_rate_care`` is capped at 1; on the shipped table it binds from male age 105.

    Without the cap the monthly conversion ``1 - (1 - q)^(1/12)`` returns a complex number
    at the terminal age, where ``2.75 q`` exceeds 1. The cap is a **[std]** guard and is
    asserted here so that it cannot be removed on the grounds that it never binds — and the
    binding age is pinned either side, so that a re-graduated table cannot move it silently
    while the documents keep quoting 105 and 111.
    """
    p = jp_ltc_anchor
    t104, t105, t107 = 12 * 44, 12 * 45, 12 * 47
    assert p.age(t104) == 104 and p.age(t105) == 105 and p.age(t107) == 107
    assert 2.75 * p.mort_rate(t104) < 1.0
    assert p.mort_rate_care(t104) == pytest.approx(2.75 * p.mort_rate(t104), rel=1e-12)
    assert 2.75 * p.mort_rate(t105) > 1.0
    assert p.mort_rate_care(t105) == 1.0
    assert 2.75 * p.mort_rate(t107) > 1.0
    assert p.mort_rate_care(t107) == 1.0
    assert isinstance(p.mort_rate_care_mth(t107), float)
    assert p.mort_rate_care_mth(t107) == 1.0
    f = p.model.Projection[2]                      # female, terminal age 118
    t110, t111 = 12 * (110 - 55), 12 * (111 - 55)
    assert f.age(t110) == 110 and f.age(t111) == 111
    assert 2.75 * f.mort_rate(t110) < 1.0
    assert 2.75 * f.mort_rate(t111) > 1.0
    assert f.mort_rate_care(t111) == 1.0


def test_result_cf_publishes_the_worked_examples_columns(nursing_care, jp_ltc_anchor):
    """The statement carries the notes' own columns, in the notes' own sign.

    ``pols_if`` leads, ``pols_act`` sits beside it because premium rides on it, the three
    care ledgers are published so the nesting is visible, ``expenses`` (acquisition and
    maintenance) and ``claim_expenses`` are two columns rather than one, and ``net_cf`` is
    income positive — the notes' own orientation, so there is no ``liability_cf``
    companion.
    """
    df = jp_ltc_anchor.result_cf()
    assert list(df.columns)[0] == "pols_if"
    for col in ("pols_act", "care_w", "care_l", "care_n", "premiums", "claims_lump",
                "claims_annuity", "claims_dementia", "claims_lapse", "expenses",
                "claim_expenses", "commissions", "net_cf"):
        assert col in df.columns
    assert df.index.name == "t"
    assert list(df.index) == list(range(jp_ltc_anchor.proj_len()))
    assert "liability_cf" not in nursing_care.Projection.cells
    rebuilt = (df["premiums"] - df["claims_lump"] - df["claims_annuity"]
               - df["claims_dementia"] - df["claims_lapse"] - df["expenses"]
               - df["claim_expenses"] - df["commissions"])
    assert (rebuilt - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-6)
    assert df.loc[0, "net_cf"] == pytest.approx(-215788.09, abs=YEN)


# The rates the shipped table quotes from 第三分野標準生命表2018, by sex and age. Every one of
# them is an ANCHOR row of the canonical [std] construction and is reproduced exactly; the
# rows between two anchors are interpolated. The same eighteen values, with the same
# provenance strings, ship with every jplib product that reads this table.
QUOTED_ANCHORS = {
    ("M", 40): 0.00076, ("M", 60): 0.00548, ("M", 65): 0.00845,
    ("M", 75): 0.02242, ("M", 80): 0.04046, ("M", 85): 0.07110,
    ("M", 90): 0.11657, ("M", 115): 0.58241, ("M", 116): 1.0,
    ("F", 40): 0.00043, ("F", 60): 0.00209, ("F", 65): 0.00317,
    ("F", 70): 0.00510, ("F", 75): 0.00967, ("F", 80): 0.01899,
    ("F", 85): 0.03843, ("F", 90): 0.07574, ("F", 118): 1.0,
}


def test_the_shipped_mortality_table_is_a_construction_not_a_copy(nursing_care):
    """Every row says so, and every sourced rate the library quotes is reproduced exactly.

    第三分野標準生命表2018 is free to read at a stable public URL, but its publisher's site
    terms prohibit reproduction, so the library ships a documented proxy anchored to a table
    a reader can go and check — never the table itself. Marking every row is what stops the
    file being mistaken for one.

    The construction is quoted **anchors** joined by a log-linear graduation, so it
    reproduces every anchor exactly by construction: nothing sourced is disturbed by the
    fitting, which is the property the previous single-pin curve fit did not have. The
    anchors are asserted by value, and the graduation between them by the constancy of the
    log step, so the file can be read off in two lines.
    """
    tbl = nursing_care.Data.mort_table()
    assert tbl["provenance"].str.contains(r"\[std\]").all()
    assert "第三分野標準生命表2018" in tbl.loc[("M", 60), "provenance"]

    for (sex, age), rate in QUOTED_ANCHORS.items():
        assert tbl.loc[(sex, age), "mort_rate"] == rate, (sex, age)
        assert "ANCHOR" in tbl.loc[(sex, age), "provenance"], (sex, age)
    anchors = tbl["provenance"].str.contains("ANCHOR")
    assert anchors.sum() == len(QUOTED_ANCHORS)

    # Between two adjacent anchors the log of the rate is linear in age, so the step is
    # constant on each segment. A curve fitted to the whole range would not reproduce the
    # anchors; a copy of the published table would not have constant segments at all. The
    # tolerance is the shipped file's own rounding to eight decimals - a thousandth of the
    # smallest step, so a genuinely different shape could not hide inside it. The segment
    # closing on a terminal age is skipped: q jumps to 1 there by definition.
    for sex, omega in (("M", 116), ("F", 118)):
        rows = tbl.loc[sex, "mort_rate"]
        ages = sorted(a for (s, a) in QUOTED_ANCHORS if s == sex)
        for a, b in zip(ages, ages[1:]):
            if b - a < 2 or b == omega:
                continue
            steps = np.diff(np.log(rows.loc[a:b].to_numpy()))
            assert steps.max() - steps.min() == pytest.approx(0.0, abs=1e-4), (sex, a, b)
            assert steps.mean() > 0.0, (sex, a, b)
    assert tbl.loc[("M", 40), "mort_rate"] < tbl.loc[("M", 90), "mort_rate"]
    assert (tbl.loc[("F", 60), "mort_rate"] < tbl.loc[("M", 60), "mort_rate"])


def test_every_assumption_table_carries_a_provenance_column():
    """No shipped input value may sit in the library without saying where it came from."""
    for name in ("mort_table.csv", "lapse_table.csv", "prevalence_table.csv",
                 "grade_share_table.csv"):
        table = pd.read_csv(MODEL_DIR.parent / name)
        assert "provenance" in table.columns, name
        assert table["provenance"].notna().all(), name


def test_the_model_point_table_covers_the_products_variants(nursing_care):
    """Eight points: the anchor, both sexes, the issue-age range and every module.

    A model point table that stopped exercising a module would leave the module's second
    position untested while every test above still passed.
    """
    table = nursing_care.Data.model_point_table()
    assert len(table) == 8
    assert list(table.index) == list(range(1, 9))
    assert set(table["sex"]) == {"M", "F"}
    assert table["issue_age"].min() == 40 and table["issue_age"].max() == 79
    assert (~table["company_limb"]).sum() == 1
    assert (table["annuity_test"] == "state").sum() == 1
    assert table["dementia_rider"].sum() == 1
    assert table["waiting_1y"].sum() == 1
    assert (table["sel_lapse_lambda"] > 0).sum() == 1
    assert set(table["prem_period"]) == {"whole_life"}
