"""Golden and structural tests for Annuity_JP_S.

The golden values are the worked example in
``products/individual_annuity/technical-notes.md`` ("Worked example"), which projects the
anchor cell: male, 保険年齢 30 at issue, a level office premium of JPY 180,000 payable for
`m` = 30 years, a 据置期間 (*sueoki kikan*, deferral gap) of `d` = 5 years, the 年金支払開始日
(*nenkin shiharai kaishi bi*, annuity commencement date) at `n` = 35 and age 65, and a
10年確定年金 (*kakutei nenkin*, ten-year annuity-certain).  They are hard-coded here rather
than pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the yen-cent, in-force and
survivorship to eight decimals, the fund to six.

**Three clocks.**  The projection index ``t`` is 0-based and counts **policy months**:
``t = 0`` is the first policy month, month ``t`` runs from time ``t`` to time ``t + 1``,
``age(t) = x + t // 12`` and ``pols_if(0) = 1``.  ``proj_len()`` is the *number* of
projected months and the exclusive end of the frame, so ``result_cf()`` covers
``t = 0 ... proj_len() - 1`` in ``proj_len()`` rows — **540** on the anchor cell, forty-five
policy years of twelve.  The 年金支払開始日 is the month ``annuitisation_t()`` = 420.

Beside it runs the **anniversary index ``s``, in years**: ``av_pp``, ``db_pp``, ``cv_pp``,
``surr_charge_pp``, ``loan_pp``, ``apl_bal`` and ``div_acc_pp`` are time-point values at
anniversary ``s``, and **every literal for them in this module is unchanged from the annual
model** — the conversion moved the projection index and left the contractual construction
alone.  A value read between anniversaries uses a third index, the **elapsed month ``u``**,
through ``av_at_m``, ``db_at_m``, ``surr_charge_at_m`` and ``cv_at_m``; the claims of month
``t`` are struck on their ``t + 1`` reading.  ``db_at_m`` is not an interpolation but the
contract's own 月払保険料 x 経過月数 clause, which the annual grid could only sample at
anniversaries.

That the conversion preserved the annual model is asserted rather than assumed: mortality
and 解約・失効 convert on the effective convention ``r_m = 1 - (1 - r)^(1/12)``, so twelve
months compound back to the annual rate exactly, ``pols_if(12 j)`` reproduces the annual
model's ``pols_if(j)``, and every ``*_at_m(12 s)`` returns its anniversary cells exactly.

This product is the library's **payout chassis**, and it is really two contracts joined at
one date, so the module carries far more than a cash-flow comparison.  Every product fact
the notes list under **Known modeling pitfalls** earns its own test, named after the
pitfall, because each of them is a way an implementation can look right and be wrong:

* two mortality tables run in one projection and the best-estimate margin **reverses sign**
  at the join;
* 確定年金 instalments are **certain**, so the payout phase must not be decremented by
  mortality — ``lives_if`` falls by 14.7% over the ten payout years without moving a yen;
* the 解約返戻金 never exceeds the 死亡給付金 but the **fund does**, and that excess is what
  buys the annuity;
* the lapse decrement must stop **before** the 年金支払開始日, where surrender is unavailable;
* 払込満了 and the 年金支払開始日 are **different dates**, five years apart on the anchor cell;
* there are **two** 予定利率, one accumulating and a lower one converting;
* the 死亡給付金 **stops growing** at 払込満了;
* the published 年金の一括払 factors are **not** the model's payout basis;
* the one published lapse rate is measured on 契約高, not on policy count;
* dividends are **zero in the base run, not absent**, and may never be paid in cash;
* 自動振替貸付 is an **election, not a no-lapse rule**; and
* the 基本年金額 is struck once from the issue basis, while the life-annuity election is
  priced on a basis no model can know.

The six optional modules are asserted in **both** positions — off in the base run, and
switched on — because a module that is only ever exercised off is machinery nobody has run.
Four of them are switched by a model point column rather than by a Space Reference, so the
other position is reached either through one of the shipped non-anchor points or, where a
counterfactual is wanted against the anchor cell itself, through :func:`variant_model`,
which copies the model *and its external inputs* to a temporary directory and edits the
copy.  The shipped product directory is never written to.
"""
import math
import re
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from jp_registry import model_path

MODEL_DIR = model_path("Annuity_JP_S")

YEN = 0.005           # money displayed to 2 d.p.
FUND = 5e-7           # the 保険料積立金, displayed to 6 d.p.
INFORCE = 5e-9        # in-force and survivorship, displayed to 8 d.p.
RATE = 5e-9           # rates, displayed to 8 d.p.


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    These docstrings are hard-wrapped prose.  Searching the raw text for a sentence
    fragment finds it or not depending on where the wrap fell, which would make the
    assertions below test the line breaks rather than the content.
    """
    return re.sub(r"\s+", " ", doc)


def variant_model(tmp_path, name, point_id, **overrides):
    """A copy of the model whose model point table has been edited.

    Most of the optional modules and every structural parameter of the contract are
    switched by a **model point column**, not by a Space Reference, so a counterfactual
    against the anchor cell means changing an input file.  The whole model folder and
    every CSV beside it are copied to ``tmp_path`` first — inputs are external, so they
    have to travel with the model — and the copy is edited.
    """
    root = tmp_path / name
    shutil.copytree(MODEL_DIR, root / MODEL_DIR.name)
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, root / csv.name)

    table = pd.read_csv(root / "model_point_table.csv", index_col="point_id")
    for column, value in overrides.items():
        table.loc[point_id, column] = value
    table.to_csv(root / "model_point_table.csv")

    return mx.read_model(root / MODEL_DIR.name, name=name)


# ---------------------------------------------------------------------------
# The notes' worked example, hard-coded to the precision the notes display
#
# "Annuitisation quantities".  F is the 年金原資 (nenkin genshi, annuity fund), B the
# 基本年金額 (kihon nenkin gaku, basic annuity amount).

FUND_AT_ANNUITISATION = 6_261_482.075674      # F = V(35)
CUMULATIVE_PREMIUMS = 5_400_000.0             # P m
LUMP_SUM_RATIO = 1.159534                     # 一括受取率 = F / Pm
FUND_NET_OF_CHARGE = 6_198_867.2549           # F (1 - theta)
ANNUITY_DUE_10_065 = 9.71433757               # a-double-dot(10, 0.65%)
ANNUITY_AMOUNT_RAW = 638_115.281              # B before the rounding step
ANNUITY_AMOUNT = 638_100.0                    # B, rounded down to the nearest 100 yen
ANNUITY_TOTAL = 6_381_000.0                   # 年金受取総額 = k B
ANNUITY_RATIO = 1.181667                      # 年金受取率 = k B / Pm

# The published specimen at the identical model point [S6], which the 予定事業費率 and the
# 年金支払開始時費用 are calibrated against.  Sourced figures, quoted to compare against.
SPECIMEN_ANNUITY_AMOUNT = 638_300.0
SPECIMEN_FUND = 6_260_000.0

# "Deferral phase, the first thirteen months", per policy issued, income-positive.
# ``expenses`` is acquisition plus a twelfth of the annual maintenance charge; the claim
# expense is its own column, as it is in result_cf().  The 年払 premium and the renewal
# commission that follows it are non-zero in one month out of twelve.
# t: (pols_if, lives_if, premiums, claims_death, claims_lapse, expenses, claim_expenses,
#     commissions, net_cf)
DEFERRAL_ROWS = {
    0:  (1.00000000, 1.00000000, 180_000.00, 0.72,  0.00, 30_333.33, 0.24,
         72_000.00, 77_665.70),
    1:  (0.99480906, 0.99995182,       0.00, 1.44,  0.00,    331.60, 0.24,
         0.00,          -333.28),
    2:  (0.98964506, 0.99990364,       0.00, 2.15,  0.00,    329.88, 0.24,
         0.00,          -332.27),
    11: (0.94435879, 0.99947015,       0.00, 8.19, 38.74,    314.79, 0.23,
         0.00,          -361.94),
    12: (0.93945668, 0.99942200, 169_102.20, 8.96, 95.29,    316.28, 0.23,
         3_382.04,   165_299.40),
}

# "Fund, benefit and surrender value: the anniversaries".  Keyed by the ANNIVERSARY s, in
# years, and every literal here is unchanged from the annual model — the 保険料積立金 is a
# net-level-premium recursion defined at the 年単位の契約応当日 and it stayed there.
# s: (av_pp, surr_charge_pp, db_pp, cv_pp)
FUND_ROWS = {
    0:  (0.000000,        180_000.0,        0.0,       0.000000),
    1:  (169_976.183805,  162_000.0,  180_000.0,   7_976.183805),
    2:  (341_646.281577,  144_000.0,  360_000.0, 197_646.281577),
    3:  (515_028.264178,  126_000.0,  540_000.0, 389_028.264178),
    12: (2_155_556.812834,      0.0, 2_160_000.0, 2_155_556.812834),
    13: (2_347_105.257270,      0.0, 2_340_000.0, 2_340_000.000000),
    34: (6_191_563.274447,      0.0, 5_400_000.0, 5_400_000.000000),
    35: (6_261_482.075674,      0.0, 5_400_000.0,         0.000000),
}

# "... and the months that changed the answer": the same four read at an ELAPSED MONTH u.
# db_at_m is the contract's own 月払保険料 x 経過月数 — 15,000 yen a month on this cell — and
# not an interpolation of the annual schedule.
# u: (av_at_m, surr_charge_at_m, db_at_m, cv_at_m)
FUND_AT_M_ROWS = {
    1:   (14_164.681984,     178_500.0,    15_000.0,          0.000000),
    6:   (84_988.091902,     171_000.0,    90_000.0,          0.000000),
    11:  (155_811.501821,    163_500.0,   165_000.0,          0.000000),
    12:  (169_976.183805,    162_000.0,   180_000.0,      7_976.183805),
    148: (2_219_406.294313,        0.0, 2_220_000.0, 2_219_406.294313),
    149: (2_235_368.664682,        0.0, 2_235_000.0, 2_235_000.000000),
    156: (2_347_105.257270,        0.0, 2_340_000.0, 2_340_000.000000),
    408: (6_191_563.274447,        0.0, 5_400_000.0, 5_400_000.000000),
}
CROSSOVER_MONTH = 149        # the elapsed month at which V first exceeds DB

# "The annuitisation transition and the payout phase", by MONTH.  The last premium falls
# at t = 348 and the first instalment at t = 420; the eleven months after each instalment
# carry maintenance expense and nothing else.
# t: (pols_if, lives_if, premiums, claims_annuity, claims_death, claims_lapse, expenses,
#     claim_expenses, net_cf)
PAYOUT_ROWS = {
    347: (0.34178987, 0.94894365,      0.00,       0.00, 694.03, 4_521.13, 150.53,
          0.66,   -5_366.36),
    348: (0.34079080, 0.94857451, 61_342.34,       0.00, 757.46, 4_520.71, 151.60,
          0.72,   54_685.01),
    359: (0.32986272, 0.94415377,      0.00,       0.00, 756.28, 4_513.66, 146.73,
          0.70,   -5_417.37),
    419: (0.30572833, 0.91328591,      0.00,       0.00, 1_090.33,   0.00, 142.94,
          1.01,   -1_234.28),
    420: (0.30552641, 0.91268274,      0.00, 194_956.41,     0.00,   0.00,  72.13,
          0.00, -195_028.54),
    421: (0.30552641, 0.91187495,      0.00,       0.00,     0.00,   0.00,  72.13,
          0.00,      -72.13),
    431: (0.30552641, 0.90383623,      0.00,       0.00,     0.00,   0.00,  72.13,
          0.00,      -72.13),
    432: (0.30552641, 0.90303627,      0.00, 194_956.41,     0.00,   0.00,  72.86,
          0.00, -195_029.26),
    539: (0.30552641, 0.77995430,      0.00,       0.00,     0.00,   0.00,  78.89,
          0.00,      -78.89),
}
RENEWAL_COMMISSION_348 = 1_226.85     # the last renewal commission, at t = 348

# The notes' trace, year by year.  Base table rates first, then the best-estimate rates
# the two factors produce from them, then the decrements.
Q_BASE_0 = 0.00068          # 死亡保険用 table at age 30 - a sourced anchor [REG-R18]
Q_BASE_1 = 0.00069          # ... at age 31 - also a sourced anchor
Q_BASE_34 = 0.00929         # ... at age 64, log-linear between the anchors at 60 and 65
Q_BASE_35 = 0.00960851      # 年金開始後用 table at age 65, the first payout year
Q_0 = 0.000578              # 0.85 x Q_BASE_0, per ANNUM
Q_1 = 0.0005865
Q_34 = 0.0078965
Q_35 = 0.0105693625         # 1.10 x Q_BASE_35 - the factor points the other way
# ... and the same four converted to the month, 1 - (1 - q)^(1/12), which is what the
# in-force recursion actually applies.
QM_0 = 0.0000481794
QM_1 = 0.0000488881
QM_34 = 0.0006604354
QM_35 = 0.0008850760
WM_0 = 0.0051430128         # 1 - (1 - 0.06)^(1/12)
DEATHS_0 = 0.0000481794     # D(0) = l(0) q_m(0)
DEATHS_1 = 0.0000479293
DEATHS_419 = 0.0002019138
LAPSES_0 = 0.0051427650

# "Key sensitivities", items 4 and 7, and the totals at the foot of the worked example.
FUND_AT_29 = 5_699_454.498584          # av_pp(29)
SURRENDER_AT_29 = 5_220_000.0          # cv_pp(29) = db_pp(29) = twenty-nine premiums
FUND_KEPT_AT_29 = 479_454.498584       # av_pp(29) - cv_pp(29)
FUND_WITHOUT_DEFERRAL_GAP = 5_929_599.05   # F if d were 0 instead of 5
DEFERRAL_GAP_UPLIFT = 0.0560
FUND_EXCESS_AT_34 = 791_563.274447     # av_pp(34) - db_pp(34)
UNDISCOUNTED_TOTAL = -461_523.46
DISCOUNTED_AT_1PCT = 96_786.79      # sum CF(t) / 1.01 ** (t / 12), the monthly frame
FIRST_NEGATIVE_YEAR = 28            # 0-based: the twelve-month block of policy year 29

# "Known modeling pitfalls": the lapse curve's two weightings, both read at the
# anniversaries of the deferral phase, s = 0 .. n_y - 1.
LAPSE_MEAN_COUNT = 0.034160
LAPSE_MEAN_FUND = 0.024754
LAPSE_PUBLISHED = 0.034               # market-wide FY2024, measured on 契約高 [R15]

# The 年金の一括払 factor table [S2], verbatim over 1-14 remaining instalments.
COMMUTE_FACTORS = {
    1: 1.010, 2: 2.016, 3: 3.018, 4: 4.016, 5: 5.010, 6: 6.000, 7: 6.986,
    8: 7.968, 9: 8.946, 10: 9.921, 11: 10.891, 12: 11.858, 13: 12.821, 14: 13.780,
}
COMMUTE_VALUE = 6_330_590.10          # B x factor(10) at the anchor cell
COMMUTE_EXCESS = 0.011037             # ... over the gross 年金原資

# The 保証期間付終身年金 election at the anchor cell's fund, model point 9.
LIFE_ANNUITY_DUE = 22.032668
LIFE_ANNUITY_AMOUNT = 281_300.0

# The published spot rates the shipped constructions are anchored to.  On 死亡保険用 both
# sexes carry their own sourced anchors — the canonical library-wide table — and the ages
# between them are the log-linear graduation.  On 年金開始後用 only male rates were retrieved,
# so three anchors per sex there and the female rows a four-year setback.
PUBLISHED_ANCHORS = {
    ("death_cover_2018", "M"): {30: 0.00068, 60: 0.00653, 90: 0.15760},
    ("death_cover_2018", "F"): {30: 0.00037, 60: 0.00363, 90: 0.09357},
    ("annuity_payout_2007", "M"): {60: 0.00642, 80: 0.03357, 100: 0.17469},
}
# The table whose female rows really are a setback of the male construction.
SETBACK_TABLE = "annuity_payout_2007"
OMEGA = {("death_cover_2018", "M"): 109, ("death_cover_2018", "F"): 113,
         ("annuity_payout_2007", "M"): 122, ("annuity_payout_2007", "F"): 126}


# ---------------------------------------------------------------------------
# The worked example


def test_worked_example_annuitisation_quantities(jp_annuity_anchor):
    """The whole annuitisation step, in the notes' own order and precision.

    F = V(n) is struck once; 一括受取率 is F over cumulative premiums; the 年金原資 is charged
    theta and divided by the annuity-due factor at the **payout** 予定利率; and the result is
    rounded down to the nearest JPY 100.  Every one of those five numbers is displayed in
    the notes, so every one of them is asserted rather than inferred from the last.
    """
    a = jp_annuity_anchor
    assert a.annuitisation_y() == 35
    assert a.annuitisation_t() == 420          # the MONTH the 年金支払開始日 falls in
    assert a.annuity_fund_pp() == pytest.approx(FUND_AT_ANNUITISATION, abs=FUND)
    assert a.annuity_fund_pp() / CUMULATIVE_PREMIUMS == pytest.approx(
        LUMP_SUM_RATIO, abs=5e-7)
    assert a.annuity_fund_pp() * (1 - a.annuitisation_charge()) == pytest.approx(
        FUND_NET_OF_CHARGE, abs=5e-5)
    assert a.annuity_due_factor() == pytest.approx(ANNUITY_DUE_10_065, abs=5e-9)
    raw = a.annuity_fund_pp() * (1 - a.annuitisation_charge()) / a.annuity_due_factor()
    assert raw == pytest.approx(ANNUITY_AMOUNT_RAW, abs=5e-4)
    assert a.annuity_amount_pp() == ANNUITY_AMOUNT
    assert a.payout_term_y() * a.annuity_amount_pp() == ANNUITY_TOTAL
    assert (a.payout_term_y() * a.annuity_amount_pp() / CUMULATIVE_PREMIUMS
            == pytest.approx(ANNUITY_RATIO, abs=5e-7))


def test_the_annuity_amount_is_rounded_down_to_the_nearest_hundred_yen(
        jp_annuity_anchor):
    """B is a contractual amount at JPY 100 granularity, not a display convention.

    Japanese specimens are published at that granularity [S3] [S5] [S6] [S10], so the
    rounding happens inside the model and JPY 15.281 a year of annuity is given up.  A
    model that rounds only on the way to the screen pays a different benefit from the one
    the contract states.
    """
    a = jp_annuity_anchor
    raw = a.annuity_fund_pp() * (1 - a.annuitisation_charge()) / a.annuity_due_factor()
    assert raw > a.annuity_amount_pp()                    # rounded down, never up
    assert raw - a.annuity_amount_pp() == pytest.approx(15.281, abs=5e-4)
    assert a.annuity_amount_pp() % 100 == 0.0


def test_the_loading_calibration_reproduces_the_published_specimen(jp_annuity_anchor):
    """beta and theta are calibrated at one model point against one published specimen.

    The 算出方法書 is a 基礎書類 filed with the FSA and not published [REG-R2], so the two
    loadings are the only free parameters between the contract and the specimen [S6].
    They reproduce the specimen's 基本年金額 of JPY 638,300 to within 0.04% and its 年金原資 of
    approximately JPY 6,260,000 to within 0.03%.  A production user should re-fit across
    all six of the specimen's points rather than inherit a one-point calibration.
    """
    a = jp_annuity_anchor
    assert a.expense_loading() == 0.065
    assert a.annuitisation_charge() == 0.010
    assert abs(a.annuity_amount_pp() / SPECIMEN_ANNUITY_AMOUNT - 1) < 0.0004
    assert abs(a.annuity_fund_pp() / SPECIMEN_FUND - 1) < 0.0003


@pytest.mark.parametrize("t", sorted(DEFERRAL_ROWS))
def test_worked_example_deferral_row(jp_annuity_anchor, t):
    """Every cell of the notes' first thirteen deferral months, to the displayed precision.

    ``t`` = 11 and ``t`` = 12 are the pair worth reading together: the twelfth month of a
    年払 contract collects nothing and the thirteenth collects a whole premium, which is the
    sawtooth the annual grid could not draw.
    """
    pols, lives, prem, death, lapse, exp, claim_exp, comm, net = DEFERRAL_ROWS[t]
    a = jp_annuity_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.lives_if(t) == pytest.approx(lives, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=YEN)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=YEN)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=YEN)
    assert a.claims(t, "ANNUITY") == 0.0
    assert a.expenses(t) == pytest.approx(exp, abs=YEN)
    assert a.claim_expenses(t) == pytest.approx(claim_exp, abs=YEN)
    assert a.commissions(t) == pytest.approx(comm, abs=YEN)
    assert a.net_cf(t) == pytest.approx(net, abs=YEN)


@pytest.mark.parametrize("s", sorted(FUND_ROWS))
def test_worked_example_fund_row(jp_annuity_anchor, s):
    """The 保険料積立金, the 解約控除, the 死亡給付金 and the 解約返戻金 at the notes' anniversaries.

    Four quantities that are routinely collapsed into one "policy value" and are not one:
    the fund accumulates past the death benefit, the surrender charge runs off over ten
    years, the death benefit is a function of premiums paid, and the surrender value is
    the fund net of the charge and capped at the death benefit.

    Indexed by the anniversary ``s``, in **years**, not by the projection's month: these
    are the contractual construction, and every literal here is what the annual model
    produced.
    """
    av, sc, db, cv = FUND_ROWS[s]
    a = jp_annuity_anchor
    assert a.av_pp(s) == pytest.approx(av, abs=FUND)
    assert a.surr_charge_pp(s) == pytest.approx(sc, abs=YEN)
    assert a.db_pp(s) == pytest.approx(db, abs=YEN)
    assert a.cv_pp(s) == pytest.approx(cv, abs=FUND)


@pytest.mark.parametrize("u", sorted(FUND_AT_M_ROWS))
def test_worked_example_fund_row_at_an_elapsed_month(jp_annuity_anchor, u):
    """The same four read at an elapsed month, which is what a benefit between
    anniversaries is actually paid on.

    ``db_at_m`` is the contract's own 月払保険料 x 経過月数 [S2] [S4] — JPY 15,000 for every
    elapsed month on this cell — and not an interpolation of the annual schedule, which is
    all the annual grid could carry.  ``av_at_m`` is a declared linear interpolation
    **[std]**, because the 算出方法書 that would give the real within-year rule is unpublished
    [REG-R2].
    """
    av, sc, db, cv = FUND_AT_M_ROWS[u]
    a = jp_annuity_anchor
    assert a.av_at_m(u) == pytest.approx(av, abs=FUND)
    assert a.surr_charge_at_m(u) == pytest.approx(sc, abs=YEN)
    assert a.db_at_m(u) == pytest.approx(db, abs=YEN)
    assert a.cv_at_m(u) == pytest.approx(cv, abs=FUND)
    assert a.db_at_m(u) == pytest.approx(15_000.0 * min(u, 360), abs=YEN)


def test_the_elapsed_month_readings_agree_with_the_anniversaries(jp_annuity_anchor):
    """Every ``*_at_m(12 s)`` returns its anniversary cells exactly.

    That is what makes the monthly grid agree with the annual one wherever both are
    defined, and it is why the 年金原資, the 基本年金額 and the published calibration did not
    move when the projection index became a month.
    """
    a = jp_annuity_anchor
    for s in range(a.annuitisation_y() + 1):
        assert a.av_at_m(12 * s) == pytest.approx(a.av_pp(s), abs=1e-9)
        assert a.db_at_m(12 * s) == pytest.approx(a.db_pp(s), abs=1e-9)
        assert a.surr_charge_at_m(12 * s) == pytest.approx(a.surr_charge_pp(s), abs=1e-9)
        assert a.cv_at_m(12 * s) == pytest.approx(a.cv_pp(s), abs=1e-9)


def test_the_conversion_preserves_anniversary_survivorship(individual_annuity):
    """(1 - r_m)^12 = 1 - r, so twelve months compound back to the annual rate exactly.

    This is the hook the whole conversion hangs on: mortality and 解約・失効 are quoted per
    annum in the input tables and applied per month on the effective convention, so the
    in-force ladder at the anniversaries is the one the annual model produced and every
    anniversary reading of the contractual construction is unchanged.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        a = individual_annuity.Projection[point_id]
        for t in range(0, a.proj_len(), 12):
            assert (1.0 - a.mort_rate_mth(t)) ** 12 == pytest.approx(
                1.0 - a.mort_rate(t), rel=1e-13)
            if a.lapse_rate(t) > 0.0:
                assert (1.0 - a.lapse_rate_mth(t)) ** 12 == pytest.approx(
                    1.0 - a.lapse_rate(t), rel=1e-13)

    # Twelve months of the deferral recursion reproduce one year of the annual one.
    a = individual_annuity.Projection[1]
    l = 1.0
    for s in range(a.annuitisation_y()):
        assert a.pols_if(12 * s) == pytest.approx(l, abs=5e-9)
        l = l * (1.0 - a.mort_rate(12 * s)) * (1.0 - a.lapse_rate(12 * s))
    assert a.pols_if(a.annuitisation_t()) == pytest.approx(l, abs=5e-9)


@pytest.mark.parametrize("t", sorted(PAYOUT_ROWS))
def test_worked_example_payout_row(jp_annuity_anchor, t):
    """The last premium month, the last deferral month and the payout rows.

    The five-year 据置期間 shows here as sixty months of no premium and a 1% annual lapse
    rate before the annuity starts, which is the part of the shape a single-term model
    cannot express; and the payout phase shows as one large month followed by eleven
    carrying maintenance expense and nothing else, which is the part the annual grid could
    not draw.
    """
    pols, lives, prem, annuity, death, lapse, exp, claim_exp, net = PAYOUT_ROWS[t]
    a = jp_annuity_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.lives_if(t) == pytest.approx(lives, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=YEN)
    assert a.claims(t, "ANNUITY") == pytest.approx(annuity, abs=YEN)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=YEN)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=YEN)
    assert a.expenses(t) == pytest.approx(exp, abs=YEN)
    assert a.claim_expenses(t) == pytest.approx(claim_exp, abs=YEN)
    assert a.net_cf(t) == pytest.approx(net, abs=YEN)


def test_worked_example_first_month_trace(jp_annuity_anchor):
    """The notes' first-month trace, line by line.

    q(0) = 0.85 x 0.00068 is the **annual** rate and q_m(0) the decrement actually
    applied; D(0) = l(0) q_m(0); DB(1) = rho (P/12) min(1, 12m) = 15,000 — one 月払保険料
    for one 経過月, the contract's own clause; W(0) = l(0)(1 - q_m(0)) w_m(0), death before
    lapse; expenses = E0 + e(0) with e(0) a twelfth of the annual charge; commission
    = c0 P, the whole 年払 premium falling in this one month.

    **The surrender benefit is nil**, and that is the product rather than a rounding: the
    interpolated fund is JPY 14,164.68 against a 解約控除 of JPY 178,500, so ``cv_at_m(1)``
    floors at zero.  The annual grid could report only CV(1) = JPY 7,976.18 at the first
    anniversary and say nothing about the eleven months before it.
    """
    a = jp_annuity_anchor
    assert a.mort_rate_base(0) == pytest.approx(Q_BASE_0, abs=RATE)
    assert a.mort_rate(0) == pytest.approx(Q_0, abs=RATE)
    assert a.mort_rate_mth(0) == pytest.approx(QM_0, abs=RATE)
    assert a.lapse_rate(0) == 0.06
    assert a.lapse_rate_mth(0) == pytest.approx(WM_0, abs=RATE)
    assert a.premiums(0) == pytest.approx(180_000.00, abs=YEN)
    assert a.pols_death(0) == pytest.approx(DEATHS_0, abs=INFORCE)
    assert a.db_at_m(1) == 15_000.0
    assert a.claims(0, "DEATH") == pytest.approx(15_000.0 * DEATHS_0, abs=YEN)
    assert a.claim_expenses(0) == pytest.approx(5_000 * DEATHS_0, abs=YEN)
    assert a.pols_lapse(0) == pytest.approx(LAPSES_0, abs=INFORCE)
    assert a.av_at_m(1) == pytest.approx(14_164.681984, abs=FUND)
    assert a.surr_charge_at_m(1) == pytest.approx(178_500.0, abs=YEN)
    assert a.cv_at_m(1) == 0.0
    assert a.claims(0, "LAPSE") == 0.0
    assert a.cv_pp(1) == pytest.approx(7_976.183805, abs=FUND)   # at the anniversary
    assert min(u for u in range(1, 13) if a.cv_at_m(u) > 0.0) == 12
    assert a.expenses(0) == pytest.approx(30_000 + 4_000 / 12, abs=YEN)
    assert a.commissions(0) == pytest.approx(0.40 * 180_000, abs=YEN)
    assert a.net_cf(0) == pytest.approx(77_665.70, abs=YEN)
    assert a.pols_if(1) == pytest.approx(1.0 * (1 - QM_0) * (1 - WM_0), abs=INFORCE)
    assert a.lives_if(1) == pytest.approx(1.0 * (1 - QM_0), abs=INFORCE)


def test_worked_example_second_month_trace(jp_annuity_anchor):
    """The notes' second-month trace: no premium, no commission, twice the death benefit.

    The second month of a 年払 contract collects nothing, and the rates do not move because
    neither the attained age nor the policy year has changed.  What does move is the death
    benefit, which is JPY 30,000 — two months' premium — against JPY 15,000 a month
    earlier: the monthly clause showing through where the annual grid had one figure for
    the whole policy year.
    """
    a = jp_annuity_anchor
    assert a.premiums(1) == 0.0
    assert a.commissions(1) == 0.0
    assert a.mort_rate(1) == pytest.approx(Q_0, abs=RATE)      # same policy year
    assert a.mort_rate_mth(1) == pytest.approx(QM_0, abs=RATE)
    assert a.pols_death(1) == pytest.approx(DEATHS_1, abs=INFORCE)
    assert a.db_at_m(2) == 30_000.0
    assert a.claims(1, "DEATH") == pytest.approx(30_000.0 * DEATHS_1, abs=YEN)
    assert a.claims(1, "LAPSE") == 0.0
    assert a.expenses(1) == pytest.approx(4_000 / 12 * a.pols_if(1), abs=YEN)
    assert a.net_cf(1) == pytest.approx(-333.28, abs=YEN)


def test_worked_example_second_premium_trace(jp_annuity_anchor):
    """t = 12: the second premium, the age step and the fund's second annual step.

    V(2) = [(V(1) + NP(1)) (1 + i_d) - q'(31) DB(2)] / (1 - q'(31)) on the **anniversary**
    clock, where q' is the 予定死亡率 at 100% of the table and not the best-estimate rate that
    decrements the in-force.  The fund recursion is annual and stays annual: rolling it
    monthly would be checking ``av_at_m``'s interpolation rather than the construction.
    """
    a = jp_annuity_anchor
    assert a.premiums(11) == 0.0 and a.commissions(11) == 0.0
    assert a.premiums(12) == pytest.approx(169_102.20, abs=YEN)
    assert a.commissions(12) == pytest.approx(0.02 * a.premiums(12), abs=YEN)
    assert a.age(12) == 31
    assert a.mort_rate_base(12) == pytest.approx(Q_BASE_1, abs=RATE)
    assert a.mort_rate(12) == pytest.approx(Q_1, abs=RATE)
    assert a.mort_rate_mth(12) == pytest.approx(QM_1, abs=RATE)
    assert a.lapse_rate(12) == 0.05
    assert a.prem_to_av_pp(1) == pytest.approx(180_000 * (1 - 0.065), abs=YEN)
    q_pricing = a.mort_rate_pricing(1)
    assert q_pricing == pytest.approx(Q_BASE_1, abs=RATE)
    assert a.av_pp(2) == pytest.approx(
        ((a.av_pp(1) + a.prem_to_av_pp(1)) * 1.01 - q_pricing * 360_000)
        / (1 - q_pricing), abs=1e-9)
    assert a.cv_pp(2) == pytest.approx(197_646.281577, abs=FUND)
    assert a.claims(11, "LAPSE") == pytest.approx(38.74, abs=YEN)   # the first one
    assert a.claims(12, "LAPSE") == pytest.approx(95.29, abs=YEN)
    assert a.expenses(12) == pytest.approx(4_000 / 12 * 1.01 * a.pols_if(12), abs=YEN)
    assert a.net_cf(12) == pytest.approx(165_299.40, abs=YEN)
    assert a.net_cf(11) < 0.0          # the sawtooth is the contract


def test_worked_example_crossover_trace(jp_annuity_anchor):
    """The crossover at the elapsed month 149, where the 解約返戻金 cap starts to bind.

    At u = 148 the fund is under the 死亡給付金 and the surrender value is the fund; one
    **month** later the fund passes it and the surrender value is the death benefit
    exactly.  The annual grid saw the same event at the anniversary 13 and could locate it
    no more precisely than "during policy year 13"; here it is the fifth month of that
    year, because DB steps by one 月払保険料 a month while V runs between two anniversaries.
    From here to the 年金支払開始日 the two are literally the same number, which is what
    「一定期間経過後は死亡給付金と同額になります」 asserts [S4].
    """
    a = jp_annuity_anchor
    assert a.av_at_m(CROSSOVER_MONTH - 1) < a.db_at_m(CROSSOVER_MONTH - 1)
    assert a.cv_at_m(CROSSOVER_MONTH - 1) == pytest.approx(
        a.av_at_m(CROSSOVER_MONTH - 1), abs=1e-9)
    assert a.av_at_m(CROSSOVER_MONTH) > a.db_at_m(CROSSOVER_MONTH)
    assert a.cv_at_m(CROSSOVER_MONTH) == 2_235_000.0
    assert CROSSOVER_MONTH // 12 == 12 and CROSSOVER_MONTH % 12 == 5
    for u in range(CROSSOVER_MONTH, a.annuitisation_t()):
        assert a.cv_at_m(u) == pytest.approx(a.db_at_m(u), abs=1e-9)
        assert a.av_at_m(u) > a.db_at_m(u)
    assert a.cv_at_m(a.annuitisation_t()) == 0.0   # surrender ends at the 年金支払開始日
    # and at the anniversaries, which is all the annual grid could read
    assert a.av_pp(12) < a.db_pp(12)
    assert a.av_pp(13) > a.db_pp(13)
    assert a.cv_pp(13) == 2_340_000.0


def test_worked_example_last_deferral_month_trace(jp_annuity_anchor):
    """t = 419: no premium, no lapse, and the last step of the fund recursion.

    The policy year ends on the 年金支払開始日, so the lapse rate is zero for the whole of it
    and the only decrement is mortality; and V(35) out of the annual step is F itself.
    """
    a = jp_annuity_anchor
    assert a.premiums(419) == 0.0
    assert a.premiums(348) > 0.0                  # the last one, seventy-one months back
    assert a.lapse_rate(419) == 0.0
    assert a.pols_lapse(419) == 0.0
    assert all(a.lapse_rate(t) == 0.0 for t in range(408, 420))
    assert a.mort_rate_base(419) == pytest.approx(Q_BASE_34, abs=RATE)
    assert a.mort_rate(419) == pytest.approx(Q_34, abs=RATE)
    assert a.mort_rate_mth(419) == pytest.approx(QM_34, abs=RATE)
    assert a.pols_death(419) == pytest.approx(DEATHS_419, abs=INFORCE)
    assert a.db_at_m(420) == 5_400_000.0
    assert a.claims(419, "DEATH") == pytest.approx(5_400_000 * DEATHS_419, abs=YEN)
    assert a.claim_expenses(419) == pytest.approx(5_000 * DEATHS_419, abs=YEN)
    assert a.expenses(419) == pytest.approx(
        4_000 / 12 * 1.01 ** 34 * a.pols_if(419), abs=YEN)
    assert a.net_cf(419) == pytest.approx(-1_234.28, abs=YEN)
    assert a.pols_if(420) == pytest.approx(a.pols_if(419) * (1 - QM_34), abs=INFORCE)
    assert a.av_pp(35) == pytest.approx(FUND_AT_ANNUITISATION, abs=FUND)


def test_worked_example_first_annuity_month_trace(jp_annuity_anchor):
    """t = 420: the first 年金支払日, paid in advance to every open contract.

    q(420) is on the **payout** table at the **1.10** factor, and it moves no cash flow at
    all: the instalment is paid to ``pols_if``, which does not decrement.  The maintenance
    charge halves, because the contract is in payment.  And the eleven months after it
    carry maintenance expense and nothing else, which is the shape the annual grid could
    not draw.
    """
    a = jp_annuity_anchor
    assert a.mort_table_name(420) == "annuity_payout_2007"
    assert a.mort_rate_base(420) == pytest.approx(Q_BASE_35, abs=RATE)
    assert a.mort_rate(420) == pytest.approx(Q_35, abs=RATE)
    assert a.mort_rate_mth(420) == pytest.approx(QM_35, abs=RATE)
    assert a.annuity_pp(420) == ANNUITY_AMOUNT
    assert a.claims(420, "ANNUITY") == pytest.approx(
        ANNUITY_AMOUNT * a.pols_if(420), abs=YEN)
    assert a.claims(420, "DEATH") == 0.0
    assert a.claims(420, "LAPSE") == 0.0
    assert a.premiums(420) == 0.0
    assert a.expenses(420) == pytest.approx(
        2_000 / 12 * 1.01 ** 35 * a.pols_if(420), abs=YEN)
    assert a.net_cf(420) == pytest.approx(-195_028.54, abs=YEN)
    assert a.pols_if(421) == a.pols_if(420)
    assert a.lives_if(421) == pytest.approx(a.lives_if(420) * (1 - QM_35), abs=INFORCE)
    # eleven months of maintenance expense and nothing else, then the next instalment
    for t in range(421, 432):
        assert a.annuity_pp(t) == 0.0
        assert a.claims(t) == 0.0
        assert a.net_cf(t) == pytest.approx(-a.expenses(t), abs=YEN)
    assert a.annuity_pp(432) == ANNUITY_AMOUNT


def test_worked_example_totals_and_shape(jp_annuity_anchor):
    """The shape the notes describe, asserted rather than restated.

    A large **positive** first month — Japanese annuity acquisition cost is small against a
    JPY 180,000 premium, the mirror image of UK term assurance — then thirty policy years
    of one large positive month against eleven small negative ones, the twelve-month block
    turning negative in policy year 29, and then a decade of one very large negative month
    a year against eleven small ones.

    The sawtooth is asserted directly, because it is the shape the monthly grid exists to
    show and a model that smeared the 年払 premium across the year would fail here and
    nowhere else.
    """
    a = jp_annuity_anchor
    df = a.result_cf()
    assert df["net_cf"].sum() == pytest.approx(UNDISCOUNTED_TOTAL, abs=YEN)
    discounted = sum(a.net_cf(t) / 1.01 ** (t / 12.0) for t in range(a.proj_len()))
    assert discounted == pytest.approx(DISCOUNTED_AT_1PCT, abs=YEN)
    assert a.net_cf(0) > 70_000.0
    # the deferral sawtooth: the premium month is positive, the other eleven are not
    for y in range(1, 28):
        assert a.net_cf(12 * y) > 0.0, y
        assert a.net_cf(12 * y + 6) < 0.0, y
    # the twelve-month blocks, which is the annual grid's row
    blocks = [sum(a.net_cf(t) for t in range(12 * y, 12 * y + 12))
              for y in range(a.proj_years())]
    assert all(b > 0.0 for b in blocks[:FIRST_NEGATIVE_YEAR])
    assert blocks[FIRST_NEGATIVE_YEAR] < 0.0
    # the payout sawtooth: one instalment month a year, eleven months of expense
    n = a.annuitisation_t()
    for j in range(a.payout_term_y()):
        assert a.net_cf(n + 12 * j) < -190_000.0
        assert all(-200.0 < a.net_cf(t) < 0.0 for t in range(n + 12 * j + 1,
                                                            n + 12 * j + 12))


def test_worked_example_lapse_curve(jp_annuity_anchor):
    """The [std] duration curve, segment by segment, including its two zeros.

    6.0 / 5.0 / 4.5 / 4.0 percent **per annum** over the first ten policy years — the CSV's
    ``from_year`` keys being a 0-based count of completed policy years, which the model
    reads as ``duration(t) = t // 12`` — 3.0% for the rest of the 保険料払込期間, 1.0% through
    the 据置期間 where no premium is due, and zero from the last deferral policy year.

    The rate is annual and holds for the twelve months of its policy year; the monthly
    decrement the recursion applies is ``lapse_rate_mth``.
    """
    a = jp_annuity_anchor
    expected = {0: 0.060, 1: 0.050, 2: 0.045, 3: 0.040, 9: 0.040,
                10: 0.030, 29: 0.030, 30: 0.010, 33: 0.010, 34: 0.000, 40: 0.000}
    for year, rate in expected.items():
        for month in range(12):
            t = 12 * year + month
            assert a.lapse_rate(t) == pytest.approx(rate, abs=1e-12), f"t={t}"
            if rate > 0.0:
                assert (1.0 - a.lapse_rate_mth(t)) ** 12 == pytest.approx(
                    1.0 - rate, rel=1e-13)
            else:
                assert a.lapse_rate_mth(t) == 0.0
    assert a.lapse_dyn_factor(0) == 1.0          # rate_new = i_d in the base run


# ---------------------------------------------------------------------------
# Known modeling pitfalls, one test each


def test_pitfall_two_mortality_tables_with_the_margin_running_opposite_ways(
        individual_annuity, jp_annuity_anchor):
    """The deferral and payout phases read different tables, adjusted in opposite senses.

    生保標準生命表2018（死亡保険用）to t = n - 1 and 生保標準生命表2007（年金開始後用）from t = n [REG-R10]
    [REG-R11].  Both are valuation tables, and their margins run opposite ways — against
    death before annuitisation, against **longevity** after it — so the best-estimate
    factor is 0.85 on the first and 1.10 on the second.  A model applying one factor to
    both has one of the two wrong, and a model reading one table throughout overstates
    payout-phase deaths materially.

    The notes' 49% at age 80 and 89% at age 90 are comparisons of the two **published**
    tables [R3] [REG-R18].  The death-cover halves come back exactly, being sourced anchors
    of the canonical table; the payout halves do not, that table being anchored only at
    60/80/100 — so the assertion here is that the overstatement is at least that large, not
    that it is exactly that.
    """
    a = jp_annuity_anchor
    n = a.annuitisation_t()
    assert a.mort_table_name(n - 1) == "death_cover_2018"
    assert a.mort_table_name(n) == "annuity_payout_2007"
    assert a.mort_be_factor(n - 1) == 0.85
    assert a.mort_be_factor(n) == 1.10
    assert a.mort_rate(n - 1) == pytest.approx(0.85 * a.mort_rate_base(n - 1), rel=1e-14)
    assert a.mort_rate(n) == pytest.approx(1.10 * a.mort_rate_base(n), rel=1e-14)

    # The payout table is materially lighter at every adult age, which is why reading the
    # death-cover table after annuitisation is wrong in the expensive direction.
    for age, floor in ((80, 1.49), (90, 1.89)):
        heavy = a.mort_rate_at_age("death_cover_2018", age)
        light = a.mort_rate_at_age("annuity_payout_2007", age)
        assert heavy / light >= floor, f"age {age}: {heavy} against {light}"
    for age in range(65, 105):
        assert (a.mort_rate_at_age("death_cover_2018", age)
                > a.mort_rate_at_age("annuity_payout_2007", age))

    # And the tables run to different terminal ages, which is what bounds the life form.
    for (table, sex), omega in OMEGA.items():
        point = 1 if sex == "M" else 8
        assert individual_annuity.Projection[point].omega_age(table) == omega


def test_pitfall_kakutei_nenkin_instalments_are_certain_not_life_contingent(
        jp_annuity_anchor):
    """The payout phase must not be decremented by mortality [S2] [R16].

    Deaths inside the certain period pay the PV of the unpaid instalments, or the
    recipient elects continuation; the base run assumes continuation at 100% **[std]**, so
    the stream is unchanged.  ``lives_if`` falls from 0.91268274 to 0.77848987 over the ten
    payout years — 14.70% of the annuitants alive at 65 die — without moving a single yen,
    which is the clearest statement of why ``pols_if`` and ``lives_if`` are two cells.
    """
    a = jp_annuity_anchor
    n, k = a.annuitisation_t(), a.payout_term_y()
    for t in range(n, a.proj_len()):
        assert a.pols_if(t) == a.pols_if(n), f"pols_if moved at t={t}"
        assert a.pols_death(t) == 0.0
        assert a.claims(t, "DEATH") == 0.0
    # one instalment a policy year, of the same amount, and nothing in the eleven between
    for j in range(k):
        assert a.claims(n + 12 * j, "ANNUITY") == pytest.approx(
            a.claims(n, "ANNUITY"), abs=1e-9)
        assert all(a.claims(t, "ANNUITY") == 0.0
                   for t in range(n + 12 * j + 1, n + 12 * j + 12))
    assert a.lives_if(n) == pytest.approx(0.91268274, abs=INFORCE)
    assert a.lives_if(a.proj_len()) == pytest.approx(0.77848987, abs=INFORCE)
    assert 1 - a.lives_if(a.proj_len()) / a.lives_if(n) == pytest.approx(
        0.1470, abs=5e-5)
    # Survivorship still rolls forward on the payout table, month by month, weighting
    # nothing: a hundred and twenty steps, not ten.
    for t in range(n, a.proj_len()):
        assert a.lives_if(t + 1) == pytest.approx(
            a.lives_if(t) * (1 - a.mort_rate_mth(t)), rel=1e-14)


def test_pitfall_the_surrender_value_is_capped_but_the_fund_is_not(
        individual_annuity, jp_annuity_anchor):
    """CV(u) <= DB(u) at every deferral month, while the fund runs past it.

    The ceiling is sourced — 「解約返還金は…死亡給付金の額を限度とします」 [S2] [S4] — and it applies to the
    surrender value alone.  Clipping ``av_pp`` instead would pass the same check and
    destroy the 年金原資: it is the un-clipped excess of the fund over the death benefit,
    JPY 791,563.274447 by t = 34, that buys the annuity.
    """
    a = jp_annuity_anchor
    assert a.check_cv_cap() is True
    # asserted at every deferral MONTH, which is stronger than the anniversary form: the
    # two sides move on different clocks between anniversaries, DB by one 月払保険料 a month
    # and CV by interpolation.
    for u in range(0, a.annuitisation_t() + 1):
        assert a.cv_at_m(u) <= a.db_at_m(u) + 1e-9, f"u={u}"
    for s in range(0, a.annuitisation_y()):
        assert a.cv_pp(s) <= a.db_pp(s) + 1e-9, f"s={s}"
    assert a.av_pp(34) - a.db_pp(34) == pytest.approx(FUND_EXCESS_AT_34, abs=FUND)
    assert a.annuity_fund_pp() > CUMULATIVE_PREMIUMS
    # A model that had clipped the fund would annuitise cumulative premiums instead, and
    # buy 13.7% less annuity.
    clipped = int(CUMULATIVE_PREMIUMS * (1 - a.annuitisation_charge())
                  / a.annuity_due_factor() / 100) * 100
    assert clipped < a.annuity_amount_pp()
    assert clipped / a.annuity_amount_pp() - 1 < -0.13
    for point_id in individual_annuity.Data.model_point_table().index:
        assert individual_annuity.Projection[point_id].check_cv_cap() is True


def test_pitfall_the_lapse_decrement_stops_before_the_annuity_start_date(
        individual_annuity):
    """No lapse through the last deferral policy year, and no surrender value from t = n.

    That policy year ends on the 年金支払開始日, where surrender is no longer available [S2]
    [S4].  A lapse applied inside it would remove contracts at t = n, where the surrender
    value is zero: in-force disappears against no payment and the annuity outgo is
    understated.  The carve-out is the whole twelve months, not one of them, because the
    rate is an annual one that the segment switches off.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        n = p.annuitisation_t()
        assert p.lapse_rate_base(n - 12) == 0.0
        for t in range(n - 12, p.proj_len()):
            assert p.lapse_rate(t) == 0.0, f"point {point_id}, t={t}"
            assert p.lapse_rate_mth(t) == 0.0
            assert p.pols_lapse(t) == 0.0
            assert p.claims(t, "LAPSE") == 0.0
        assert p.lapse_rate(n - 13) > 0.0          # and only that policy year
        for s in range(p.annuitisation_y(), p.proj_years() + 1):
            assert p.cv_pp(s) == 0.0
        for u in range(n, p.proj_len() + 1):
            assert p.cv_at_m(u) == 0.0
        # The only decrement in the last deferral policy year is mortality.
        assert p.pols_if(n) == pytest.approx(
            p.pols_if(n - 12) * math.prod(
                1 - p.mort_rate_mth(t) for t in range(n - 12, n)), rel=1e-12)


def test_pitfall_premium_end_and_annuity_start_are_different_dates(
        jp_annuity_anchor, tmp_path):
    """m = 30 and n = 35 are five years apart, and the gap is worth 5.60% of the fund.

    Collapsing the 据置期間 is not a rounding difference [S6]: on the anchor cell F falls
    from JPY 6,261,482.08 to JPY 5,929,599.05, of which 5.10% is the interest factor
    1.01^5 and the rest is five more years of survivorship release.  A model with one
    "term" parameter cannot express the composite at all.
    """
    a = jp_annuity_anchor
    assert a.premium_term_y() == 30
    assert a.defer_gap_y() == 5
    assert a.annuitisation_y() == 35 == a.premium_term_y() + a.defer_gap_y()
    assert a.annuitisation_t() == 420 == 12 * a.annuitisation_y()
    assert a.annuity_start_age() == 65 == a.issue_age() + a.annuitisation_y()
    for t in range(360, 420):                          # the sixty 据置期間 months
        assert a.premiums(t) == 0.0
        assert a.lapse_rate(t) in (0.01, 0.0)          # the 据置期間 rate, then zero
    for s in range(30, 35):
        assert a.prem_to_av_pp(s) == 0.0
        assert a.av_pp(s + 1) > a.av_pp(s)             # the fund still accumulates

    model = variant_model(tmp_path, "Annuity_JP_S_no_gap", 1,
                          defer_gap_y=0, annuity_start_age=60)
    try:
        flat = model.Projection[1]
        assert flat.annuitisation_t() == 360
        assert flat.annuity_fund_pp() == pytest.approx(
            FUND_WITHOUT_DEFERRAL_GAP, abs=YEN)
        assert (a.annuity_fund_pp() / flat.annuity_fund_pp() - 1
                == pytest.approx(DEFERRAL_GAP_UPLIFT, abs=5e-5))
        assert flat.annuity_amount_pp() < a.annuity_amount_pp()
    finally:
        model.close()


def test_pitfall_two_yotei_riritsu_not_one(jp_annuity_anchor):
    """1.00% accumulating and 0.65% converting, and the lower one buys the annuity.

    Using the deferral rate to buy the annuity overstates B by 1.55% at k = 10 [S5] [S8] —
    in the direction a reader would not guess, since the payout rate is the *lower* one,
    so each yen of 年金原資 buys **less** annuity, not more.
    """
    a = jp_annuity_anchor
    i_d, i_p = a.int_rate_defer(), a.int_rate_payout()
    assert (i_d, i_p) == (0.0100, 0.0065)
    assert i_p < i_d
    k = a.payout_term_y()
    wrong = (1 - (1 + i_d) ** -k) / i_d * (1 + i_d)
    assert wrong < a.annuity_due_factor()
    assert a.annuity_due_factor() / wrong - 1 == pytest.approx(0.0155, abs=5e-5)
    # The fund itself is accumulated at i_d and nothing else.
    assert a.av_pp_at(0, "AFT_INT") == pytest.approx(
        a.av_pp_at(0, "AFT_PREM") * (1 + i_d), rel=1e-14)


def test_pitfall_the_death_benefit_stops_growing_at_premium_end(individual_annuity):
    """DB(u) = rho (P/12) min(u, 12m): the clause as written, flat from 払込満了.

    The contractual base is 月払保険料 x 経過月数 [S2] [S4], which 所令211①ロ requires to increase
    with cumulative premiums [R10] — and no further premium is paid after 払込満了.  A model
    that keeps accruing it to n overstates deferral-phase claims by d years' worth of
    premium; a model that rounds it to whole policy years, as the annual grid had to,
    misstates every individual death claim by up to eleven months of premium.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        m, n_y = p.premium_term_y(), p.annuitisation_y()
        for s_ in range(0, n_y + 1):
            assert p.db_pp(s_) == pytest.approx(
                p.db_ratio() * p.premium_pp() * min(s_, m), abs=1e-9), f"{point_id}/{s_}"
        assert p.db_pp(m) == p.db_pp(n_y)
        if n_y > m:
            assert p.db_pp(m - 1) < p.db_pp(m)
        # the monthly clause, and its agreement with the annual schedule
        for u in range(0, 12 * n_y + 1):
            assert p.db_at_m(u) == pytest.approx(
                p.db_ratio() * p.premium_pp() / 12 * min(u, 12 * m), abs=1e-9)
        for s_ in range(0, n_y + 1):
            assert p.db_at_m(12 * s_) == pytest.approx(p.db_pp(s_), abs=1e-9)
        assert p.db_at_m(12 * m) == p.db_at_m(12 * n_y)


def test_pitfall_the_commutation_factors_are_not_the_models_payout_basis(
        jp_annuity_anchor):
    """The published 年金の一括払 table [S2] and the payout 予定利率 [S5] are two bases.

    The table is used verbatim over 1-14 remaining instalments and an annuity-due at the
    0.40% p.a. it implies outside that range.  The two do not reconcile: at t = n the
    factor for ten remaining instalments returns JPY 6,330,590.10 against a 年金原資 of
    JPY 6,261,482.08, 1.1037% more, which is why base-run take-up is zero.

    The table is not an annuity-due at **any** positive rate either — a single remaining
    instalment is factored at 1.010 and two at 2.016, which implies v > 1 — so a reader who
    "fixes" the factors by re-deriving them at 0.40% is building a different table.  A
    production model must re-derive them on its own payout basis.
    """
    a = jp_annuity_anchor
    for j, factor in COMMUTE_FACTORS.items():
        assert a.commute_factor(j) == factor, f"{j} remaining"
    assert COMMUTE_FACTORS[1] > 1.0 and COMMUTE_FACTORS[2] > 2.0
    i = 0.004
    assert a.commute_factor(15) == pytest.approx(
        (1 - (1 + i) ** -15) / i * (1 + i), rel=1e-12)
    assert a.commute_factor(0) == 0.0
    # ... and the published factor for the whole ten-year period beats the fund.
    assert a.commute_value_pp() == pytest.approx(COMMUTE_VALUE, abs=YEN)
    assert a.commute_value_pp() / a.annuity_fund_pp() - 1 == pytest.approx(
        COMMUTE_EXCESS, abs=5e-6)
    # An annuity-due at 0.40% does not reproduce the published ten-year factor.
    assert a.commute_factor(10) != pytest.approx(
        (1 - (1 + i) ** -10) / i * (1 + i), abs=1e-3)


def test_pitfall_the_published_lapse_rate_is_measured_on_contract_amount(
        jp_annuity_anchor):
    """The 3.4% for FY2024 has 契約高 in its denominator, not policy count [R15] [REG-R31].

    On the anchor cell the shipped curve averages 3.4160% weighted by ``pols_if`` and
    2.4754% weighted by ``av_pp``, both read at the **anniversaries** of the deferral phase
    — a difference of about a quarter, because lapse is front-loaded and the fund is
    back-loaded.  They are annual means of an annual rate curve, which is what the one
    public figure they are calibrated against is; reading them at every month would average
    a monthly decrement against an annual benchmark.  The two weightings are not
    interchangeable, and a calibration that does not say which one it used mis-states the
    deferral decrement.
    """
    a = jp_annuity_anchor
    count = a.lapse_rate_mean("count")
    fund = a.lapse_rate_mean("fund")
    assert count == pytest.approx(LAPSE_MEAN_COUNT, abs=5e-7)
    assert fund == pytest.approx(LAPSE_MEAN_FUND, abs=5e-7)
    assert abs(count - LAPSE_PUBLISHED) < 0.0005      # calibrated against the published
    assert 1 - fund / count == pytest.approx(0.275, abs=0.02)
    # Both are means over the deferral anniversaries only, rebuilt here independently.
    ys = range(0, a.annuitisation_y())
    for weighting, weights in (("count", [a.pols_if(12 * y) for y in ys]),
                               ("fund", [a.av_pp(y) for y in ys])):
        num = sum(w * a.lapse_rate(12 * y) for w, y in zip(weights, ys))
        assert a.lapse_rate_mean(weighting) == pytest.approx(
            num / sum(weights), rel=1e-14)


def test_pitfall_dividends_are_zero_in_the_base_run_not_absent(
        individual_annuity, jp_annuity_anchor, tmp_path):
    """The 契約者配当 machinery is contractual, and it may never be paid in cash.

    Zero declared is a choice [S4]; the cells exist and are exercised at model point 8.
    Under the 税制適格特約 the accumulated dividend cannot be withdrawn before annuitisation
    and must be applied as a single premium **increasing the 基本年金額** [S1] [S2] [R10], so
    a model that pays a declared dividend as a cash outflow before t = n is projecting a
    non-qualifying contract.
    """
    a = jp_annuity_anchor
    assert a.div_rate() == 0.0
    assert all(a.div_credit_pp(s) == 0.0 for s in range(0, a.proj_years()))
    assert all(a.div_acc_pp(s) == 0.0 for s in range(0, a.proj_years()))

    p = individual_annuity.Projection[8]
    n_y = p.annuitisation_y()
    assert p.div_rate() == 0.002
    assert p.div_credit_pp(1) == pytest.approx(0.002 * p.av_pp(1), rel=1e-14)
    assert p.div_acc_pp(n_y) > 0.0
    # The declaration and the accumulation are both ANNUAL: the composite is a
    # 5年ごと利差配当 design and the declared rate, not the frequency, is what moves it.
    for s_ in range(1, n_y):
        assert p.div_acc_pp(s_ + 1) == pytest.approx(
            (p.div_acc_pp(s_) + p.div_credit_pp(s_)) * 1.006, rel=1e-13)
    # Nothing is paid out: the cash flow ledger closes without a dividend term.
    assert p.check_net_cf() is True
    assert "claims_dividend" not in p.result_cf().columns
    # ... and the accumulated dividend lands in B as a single premium.
    gross = p.annuity_fund_pp() * (1 - p.annuitisation_charge())
    assert p.annuity_amount_pp() == pytest.approx(
        int((gross + p.div_acc_pp(n_y)) / p.annuity_due_factor() / 100) * 100, abs=1e-9)
    without = int(gross / p.annuity_due_factor() / 100) * 100
    assert without < p.annuity_amount_pp()

    model = variant_model(tmp_path, "Annuity_JP_S_no_div", 8, div_rate=0.0)
    try:
        off = model.Projection[8]
        assert off.div_acc_pp(n_y) == 0.0
        assert off.annuity_amount_pp() == pytest.approx(without, abs=1e-9)
        assert off.annuity_amount_pp() < p.annuity_amount_pp()
        # The dividend does not touch the fund itself, only the annuity it buys.
        assert off.annuity_fund_pp() == pytest.approx(p.annuity_fund_pp(), abs=1e-9)
    finally:
        model.close()


def test_pitfall_apl_is_an_election_not_a_no_lapse_rule(individual_annuity):
    """自動振替貸付 suppresses lapse only while the 解約返戻金 can carry the balance [S4].

    On model point 7 the facility engages at the premium anniversary 2, is fed one premium
    a year compounding at the contractual cap of 8% p.a., carries the contract for six
    policy years, and then fails: at the anniversary 8 principal and interest have outgrown
    the surrender value and the **whole** in-force lapses.  Wiring it on by default would
    remove lapse from the model for the wrong reason [REG-R14], and one carrier's product
    has no such facility at all [S2].

    The module is **annual on the monthly grid**, and deliberately so: the thing it carries
    is one annual premium, lent on one date and compounding once a year.  The test that
    fires it is read at the anniversary opening each month's policy year.
    """
    p = individual_annuity.Projection[7]
    assert p.apl_on() is True
    assert p.apl_engaged(0) is False and p.apl_engaged(1) is False   # cv < one premium
    assert all(p.apl_engaged(s_) for s_ in range(2, 8))
    assert p.apl_bal(2) == 0.0               # the first premium is lent at anniversary 2
    assert p.apl_bal(3) == pytest.approx(180_000 * 1.08, abs=YEN)
    for s_ in range(3, 8):
        assert p.apl_bal(s_ + 1) == pytest.approx(
            (p.apl_bal(s_) + 180_000) * 1.08, abs=1e-6)
    # While the facility runs the premium is lent, not received, and lapse is suppressed
    # in every month of those policy years.
    for t in range(24, 96):
        assert p.premiums(t) == 0.0
        assert p.lapse_rate(t) == 0.0
        assert p.lapse_rate_mth(t) == 0.0
        assert p.lapse_rate_base(t) > 0.0            # the table rate is not zero
    # ... and the moment the balance outgrows the surrender value, everything lapses:
    # the whole in-force goes in the first month of that policy year.
    assert p.apl_bal(8) > p.cv_pp(8)
    assert p.lapse_rate(96) == 1.0
    assert p.lapse_rate_mth(96) == 1.0
    assert p.pols_if(96) > 0.0
    assert p.pols_if(97) == 0.0
    assert p.annuity_fund_pp() == 0.0
    assert p.check_pols_roll_fwd() is True


def test_pitfall_the_annuity_amount_is_struck_once_from_the_issue_basis(
        individual_annuity, jp_annuity_anchor):
    """B is struck at t = n from the issue basis and never recomputed [S2] [S3].

    The 保証期間付終身年金 election is priced instead on the 基礎率 in force at the 年金支払開始日 [S2]
    [S9], which no model can know; holding it at the issue basis is a **[std]** assumption
    and the reason base-run take-up is zero.  Sharing one code path between the two hides
    that distinction, and the two answers are far apart: model point 9 is the anchor cell
    with nothing changed but the payout form, and the same JPY 6,261,482.08 buys
    JPY 638,100 a year as a ten-year certain annuity and JPY 281,300 as a life annuity with
    a ten-year guarantee.
    """
    a = jp_annuity_anchor
    n, k = a.annuitisation_t(), a.payout_term_y()
    for j in range(k):
        assert a.annuity_pp(n + 12 * j) == ANNUITY_AMOUNT
        assert all(a.annuity_pp(t) == 0.0
                   for t in range(n + 12 * j + 1, n + 12 * j + 12))
    assert a.annuity_pp(n - 1) == 0.0
    assert a.check_annuity_total() is True

    life = individual_annuity.Projection[9]
    assert life.payout_form() == "life_guar"
    assert life.annuity_fund_pp() == pytest.approx(a.annuity_fund_pp(), abs=1e-9)
    assert life.annuity_due_life_factor() == pytest.approx(LIFE_ANNUITY_DUE, abs=5e-7)
    assert life.annuity_amount_pp() == LIFE_ANNUITY_AMOUNT
    assert a.annuity_amount_pp() / life.annuity_amount_pp() > 2.2
    # The two forms are priced on two factors, not one code path with a switch inside it.
    assert life.annuity_due_factor() == pytest.approx(ANNUITY_DUE_10_065, abs=5e-9)
    assert life.annuity_due_life_factor() > life.annuity_due_factor()


# ---------------------------------------------------------------------------
# The roll-forward identities and the check_* cells


ALL_CHECKS = ("check_pols_roll_fwd", "check_lives_roll_fwd", "check_fund",
              "check_cv_cap", "check_annuity_total", "check_net_cf",
              "check_mort_graduation")


def test_the_seven_check_cells_are_the_published_set(individual_annuity):
    """These seven roll-forward and ledger checks are published, and no others.

    The library-wide form: no argument, one bool over all t, with the signed per-period
    residual at ``check_*_resid(t)``.  A check that is only ever run on the anchor cell is
    a check of the anchor cell — which is why they are run on all nine model points, in
    ``test_model_conventions_jp.py``, whose sweep discovers every ``check_*`` generically
    and calls it on every point of every model in the library. Running them again here, on
    a second instance of the same model, meant a second cold projection of the whole table
    to reach a verdict already reached.

    Generic discovery cannot notice a check that has *gone*: it simply stops being
    discovered. Naming the set is the statement left here.
    """
    published = {c for c in individual_annuity.Projection.cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(ALL_CHECKS)


def test_the_inforce_rollforward_closes_term_by_term(individual_annuity):
    """l(t) - l(t+1) = deaths + lapses + commutations + expiries, in every year.

    Expiries are not a decrement and not a benefit — the 確定年金 pays exactly k instalments
    and the contract ends — but without that term the final payout year appears to lose
    contracts with no cause.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        for t in range(0, p.proj_len()):
            out = (p.pols_death(t) + p.pols_lapse(t) + p.pols_commute(t)
                   + p.pols_maturity(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(
                out, abs=1e-12), f"point {point_id}, t={t}"
            assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_death_is_decremented_before_lapse(jp_annuity_anchor):
    """The notes' processing order: lapses are taken from the survivors of mortality."""
    a = jp_annuity_anchor
    for t in (0, 1, 5, 60, 240, 399):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate_mth(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(a.pols_if(t + 1), rel=1e-14)


def test_the_survivorship_rollforward_is_carried_separately(individual_annuity):
    """L(t+1) = L(t)(1 - q(t)) throughout, on whichever table the phase reads.

    Carried separately from the in-force roll-forward because the two measures decrement
    differently; a model that had quietly collapsed them would still close one of the two.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        assert p.lives_if(0) == 1.0
        for t in range(0, p.proj_len()):
            assert p.lives_if(t + 1) == pytest.approx(
                p.lives_if(t) * (1 - p.mort_rate_mth(t)), rel=1e-13)
            assert p.check_lives_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_the_fund_recursion_matches_an_independent_rebuild(individual_annuity):
    """(V(s) + NP(s))(1 + i_d) = q' DB(s+1) + (1 - q') V(s+1) over the deferral phase.

    Rebuilt here from the model's own inputs rather than read back from it, because the
    two ways this recursion is usually built wrongly — putting lapse into it, or using the
    best-estimate rate in place of the 予定死亡率 — both produce a fund that still looks
    plausible.  The survivorship release is the division by (1 - q').

    **This one is annual on a monthly model, and deliberately.**  The 保険料積立金 is a
    contractual accumulation defined at the 年単位の契約応当日; rolling it monthly would be
    checking ``av_at_m``'s interpolation convention rather than the construction under it.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        i_d = p.int_rate_defer()
        value = 0.0
        for s_ in range(0, p.annuitisation_y()):
            assert p.av_pp(s_) == pytest.approx(value, abs=1e-6), f"{point_id}/{s_}"
            q = p.mort_rate_pricing(s_)
            value = ((value + p.prem_to_av_pp(s_)) * (1 + i_d)
                     - q * p.db_pp(s_ + 1)) / (1 - q)
        assert p.av_pp(p.annuitisation_y()) == pytest.approx(value, abs=1e-6)
        assert p.check_fund() is True
        # The fund is dead after annuitisation: there is nothing left to roll forward.
        for s_ in range(p.annuitisation_y() + 1, p.proj_years() + 1):
            assert p.av_pp(s_) == 0.0


def test_the_published_columns_add_up_to_net_cf(individual_annuity):
    """result_cf() is a decomposition of net_cf, not a selection from it.

    The one identity a reader of the output cannot verify for themselves, so it is
    asserted here on every model point as well as inside ``check_net_cf``.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        df = p.result_cf()
        outgo = df[["claims_annuity", "claims_death", "claims_lapse", "claims_commutation",
                    "expenses", "claim_expenses", "commissions",
                    "policy_loans"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9)
        assert p.check_net_cf() is True


def test_the_guaranteed_instalments_sum_to_the_promised_total(individual_annuity):
    """k B on the 確定年金 form and g B over the guarantee on the life form [S2] [R16].

    A model that had decremented the payout phase by mortality, or that had recomputed B
    after annuitisation, would fail here rather than quietly pay a different annuity.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        if p.commute_rate() > 0.0:
            continue                       # the commuted contract pays no instalments
        n = p.annuitisation_t()
        guaranteed = (p.payout_term_y() if p.payout_form() == "certain"
                      else p.guar_term_y())
        # one instalment a policy year, in the anniversary months, and nothing between
        total = sum(p.annuity_pp(t) for t in range(n, n + 12 * guaranteed))
        assert total == pytest.approx(guaranteed * p.annuity_amount_pp(), abs=1e-9)
        if p.annuity_amount_pp() > 0.0:          # point 7 lapses before annuitisation
            assert [t for t in range(n, n + 12 * guaranteed)
                    if p.annuity_pp(t) > 0.0] == [n + 12 * j for j in range(guaranteed)]
        assert p.check_annuity_total() is True


def test_the_mortality_tables_are_still_the_shipped_construction(individual_annuity):
    """The rates in mort_table.csv are the ones mort_anchor_table.csv graduates to.

    The library ships no copy of 生保標準生命表2018 or of the 2007 年金開始後用 table.  What it ships
    is the canonical library-wide 死亡保険用 table, whose sourced anchors [REG-R18] are joined
    log-linearly in ``ln q``, and a Makeham construction fitted to three quoted 年金開始後用
    spot rates [R3] [REG-R19].  This is the assertion that the two files still agree with
    each other.  Once a licensed or company table is dropped in, a False here is the
    correct answer, which is why the cells reports a residual rather than raising.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        assert p.check_mort_graduation() is True
    by_sex = {"M": individual_annuity.Projection[1],
              "F": individual_annuity.Projection[8]}
    for (table, sex), anchors in PUBLISHED_ANCHORS.items():
        p = by_sex[sex]
        for age, rate in anchors.items():
            assert p.mort_rate_at_age(table, age) == pytest.approx(rate, abs=5e-12)

    # The graduation between two anchors is log-linear and rounded to five decimals, so
    # every non-anchor age is rebuildable from the two that bracket it.
    a = by_sex["M"]
    ages = a.mort_anchor_ages("death_cover_2018")
    for x in range(min(ages), max(ages)):
        if x in ages:
            continue
        lo = max(v for v in ages if v < x)
        hi = min(v for v in ages if v > x)
        expected = round(math.exp(
            math.log(a.mort_rate_at_age("death_cover_2018", lo))
            + (x - lo) / (hi - lo) * (math.log(a.mort_rate_at_age("death_cover_2018", hi))
                                      - math.log(a.mort_rate_at_age("death_cover_2018", lo)))), 5)
        assert a.mort_rate_at_age("death_cover_2018", x) == pytest.approx(
            expected, abs=5e-12), f"age {x}"


# ---------------------------------------------------------------------------
# The optional modules, in both positions


def test_the_life_annuity_election_off_and_on(individual_annuity, jp_annuity_anchor):
    """保証期間付終身年金 off at the anchor cell and on at model points 4 and 9.

    With the module on the instalments are unconditional for g years and life-contingent
    after, the horizon runs to the payout table's terminal age instead of n + k, and the
    in-force runs off on the best-estimate payout basis once the guarantee expires.

    ``proj_len()`` is a **count** of projected years there too: ``omega - x + 1`` rows,
    whose last one, ``t = proj_len() - 1 = omega - x``, is the year the annuitant attains
    the terminal age.  The ``+ 1`` is the count, not an off-by-one in the index.
    """
    a = jp_annuity_anchor
    assert a.payout_form() == "certain"
    assert a.proj_len() == 12 * (a.annuitisation_y() + a.payout_term_y())

    p = individual_annuity.Projection[9]
    n, g = p.annuitisation_t(), p.guar_term_y()
    assert p.payout_form() == "life_guar"
    assert p.proj_years() == p.omega_age("annuity_payout_2007") - p.issue_age() + 1 == 93
    # the frame stops at the FIRST MONTH of the terminal-age year, where q is 1
    assert p.proj_len() == 12 * (p.omega_age("annuity_payout_2007") - p.issue_age()) + 1
    assert len(p.result_cf()) == p.proj_len()
    assert p.age(p.proj_len() - 1) == p.omega_age("annuity_payout_2007")
    for t in range(n, n + 12 * g):
        assert p.pols_if(t) == p.pols_if(n)          # unconditional over the guarantee
    for j in range(g):
        assert p.annuity_pp(n + 12 * j) == LIFE_ANNUITY_AMOUNT
    assert p.pols_if(n + 12 * g) < p.pols_if(n)      # life-contingent thereafter
    assert p.pols_maturity(n + 12 * g - 1) == 0.0      # ... and no fixed end
    assert all(p.pols_maturity(t) == 0.0 for t in range(0, p.proj_len()))
    assert p.annuity_pp(p.proj_len() - 1) == LIFE_ANNUITY_AMOUNT
    assert p.check_pols_roll_fwd() is True

    # The life factor is a survivorship sum on the payout table at 100%, not at the
    # best-estimate factor: it is a pricing basis.
    i = p.int_rate_payout()
    total, surv, j = 0.0, 1.0, 0
    a0, omega = p.annuity_start_age(), p.omega_age("annuity_payout_2007")
    while a0 + j <= omega:
        total += max(1.0 if j < g else 0.0, surv) / (1 + i) ** j
        surv *= 1 - p.mort_rate_at_age("annuity_payout_2007", a0 + j)
        j += 1
    assert p.annuity_due_life_factor() == pytest.approx(total, rel=1e-14)

    other = individual_annuity.Projection[4]
    assert other.payout_form() == "life_guar"
    assert other.annuity_due_life_factor() == pytest.approx(19.013626, abs=5e-7)
    assert other.annuity_amount_pp() == 342_300.0


def test_commutation_off_and_on(individual_annuity, jp_annuity_anchor):
    """年金の一括払 off at the anchor cell and on at 100% at model point 5.

    The elector takes the lump sum in place of the instalments and the contract terminates
    [S2] [S4], so a fully commuted block pays one 年金の一括払 at t = n and nothing after.
    """
    a = jp_annuity_anchor
    assert a.commute_rate() == 0.0
    assert all(a.pols_commute(t) == 0.0 for t in range(0, a.proj_len()))
    assert (a.result_cf()["claims_commutation"] == 0.0).all()

    p = individual_annuity.Projection[5]
    n = p.annuitisation_t()
    assert p.commute_rate() == 1.0
    assert p.pols_commute(n) == pytest.approx(p.pols_if(n), rel=1e-14)
    assert all(p.pols_commute(t) == 0.0 for t in range(0, p.proj_len()) if t != n)
    assert p.claims(n, "COMMUTATION") == pytest.approx(
        p.commute_value_pp() * p.pols_if(n), abs=1e-6)
    assert p.claims(n, "ANNUITY") == 0.0
    assert p.pols_if(n + 1) == 0.0
    assert all(p.claims(t, "ANNUITY") == 0.0 for t in range(n, p.proj_len()))
    assert p.check_pols_roll_fwd() is True
    # The composite artefact is visible at this point too: the lump sum beats the fund.
    assert p.commute_value_pp() > p.annuity_fund_pp()


def test_the_apl_module_off_and_on(individual_annuity, jp_annuity_anchor):
    """自動振替貸付 off at the anchor cell and on at model point 7.

    Off, the balance is zero at every duration, the premium is received in cash and the
    table lapse rate applies.  On, the same policy is carried by the facility and then
    terminated by it.  Model point 7 is the anchor cell with nothing changed but the flag.
    """
    a = jp_annuity_anchor
    assert a.apl_on() is False
    assert all(a.apl_bal(s_) == 0.0 for s_ in range(0, a.proj_years()))
    assert all(a.apl_engaged(s_) is False for s_ in range(0, a.proj_years()))
    assert a.db_pp_net(10) == a.db_pp(10)
    assert a.cv_pp_net(10) == a.cv_pp(10)

    p = individual_annuity.Projection[7]
    assert p.issue_age() == a.issue_age() and p.premium_pp() == a.premium_pp()
    assert p.apl_on() is True
    assert p.premiums(0) == a.premiums(0)             # identical until it engages
    assert p.db_pp_net(5) == pytest.approx(p.db_pp(5) - p.apl_bal(5), abs=1e-9)
    assert p.db_pp_net(5) < a.db_pp_net(5)
    assert p.result_cf()["net_cf"].sum() != pytest.approx(
        a.result_cf()["net_cf"].sum(), abs=1.0)


def test_the_policy_loan_module_off_and_on(individual_annuity, jp_annuity_anchor):
    """契約者貸付 off at the anchor cell and on at model point 8.

    A loan of half the 解約返戻金 drawn at the **anniversary** 20 **[std]** — ``loan_draw_year``
    in ``pricing_table.csv`` is an anniversary in years, so the drawdown is the start of the
    twenty-first policy year, the month ``t`` = 240, and ``loan_pp(19)`` is still zero —
    compounding at 2.40% p.a. [S11] [S8] and capped at the 解約返戻金 [S4] [REG-R14].  The
    balance is an **annual** quantity because the rate is a 年利 capitalised at the
    契約応当日, so it genuinely does not move between anniversaries.  Only the drawdown is a
    cash flow; the balance is recovered by deduction from the 死亡給付金, the 解約返戻金 and the
    年金原資, so it never touches the fund itself.
    """
    a = jp_annuity_anchor
    assert a.loan_on() is False
    assert all(a.loan_pp(s_) == 0.0 for s_ in range(0, a.proj_years()))
    assert (a.result_cf()["policy_loans"] == 0.0).all()

    p = individual_annuity.Projection[8]
    n_y = p.annuitisation_y()
    assert p.loan_on() is True
    assert p.loan_pp(19) == 0.0
    assert p.loan_pp(20) == pytest.approx(0.50 * p.cv_pp(20), rel=1e-14)
    assert p.loan_pp(21) == pytest.approx(p.loan_pp(20) * 1.024, rel=1e-14)
    assert p.policy_loans(240) == pytest.approx(
        p.loan_pp(20) * p.pols_if(240), abs=1e-9)
    assert all(p.policy_loans(t) == 0.0 for t in range(0, p.proj_len()) if t != 240)
    for s_ in range(20, n_y):
        assert p.loan_pp(s_) <= p.cv_pp(s_) + 1e-9  # capped at the surrender value
        assert p.db_pp_net(s_) == pytest.approx(p.db_pp(s_) - p.loan_pp(s_), abs=1e-9)
        assert p.cv_pp_net(s_) == pytest.approx(p.cv_pp(s_) - p.loan_pp(s_), abs=1e-9)
    # The balance genuinely does not move between anniversaries, so a benefit in month t
    # is settled against the balance outstanding at duration(t).
    for t in range(240, 251):                    # u = 241 .. 251, all inside year 21
        assert p.db_net_at_m(t + 1) == pytest.approx(
            p.db_at_m(t + 1) - p.loan_pp(20), abs=1e-9)
    assert p.db_net_at_m(252) == pytest.approx(   # and the balance steps at the next one
        p.db_at_m(252) - p.loan_pp(21), abs=1e-9)
    # The fund is untouched; the 年金原資 is what carries the deduction.
    assert p.annuity_fund_pp() == pytest.approx(
        p.av_pp(n_y) - p.loan_pp(n_y), abs=1e-9)
    assert p.annuity_fund_pp() < p.av_pp(n_y)


def test_the_dynamic_lapse_module_off_and_on(
        individual_annuity, jp_annuity_anchor, tmp_path):
    """M(t) = 1 in the base run, where the new-business 予定利率 equals the rate at issue.

    Premiums and the 予定利率 are both fixed at issue, so there is no premium-shock lapse on
    this chassis; the driver runs the other way, a **rise** in new-business rates making an
    in-force contract relatively unattractive [S8].  Model point 8 carries i_new = 1.50%,
    which is M = 1.10; the multiplier is capped at 2.
    """
    a = jp_annuity_anchor
    assert a.rate_new() == a.int_rate_defer()
    assert a.lapse_dyn_factor(0) == 1.0
    assert a.lapse_rate(0) == a.lapse_rate_base(0)

    p = individual_annuity.Projection[8]
    assert p.rate_new() == 0.015
    assert p.lapse_dyn_factor(0) == pytest.approx(1.10, rel=1e-14)
    assert p.lapse_rate(0) == pytest.approx(0.066, rel=1e-14)
    assert p.lapse_rate(0) > a.lapse_rate(0)
    # the zero still binds through the last deferral policy year, multiplier or not
    assert all(p.lapse_rate(t) == 0.0
               for t in range(p.annuitisation_t() - 12, p.proj_len()))

    model = variant_model(tmp_path, "Annuity_JP_S_dyn_cap", 1, rate_new=0.20)
    try:
        capped = model.Projection[1]
        assert capped.lapse_dyn_factor(0) == 2.0     # 1 + 20 x 0.19, capped
        assert capped.lapse_rate(0) == pytest.approx(0.12, rel=1e-14)
        assert capped.lapse_rate_mean("count") > a.lapse_rate_mean("count")
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Structural product facts


def test_no_tail_states_on_the_certain_form(jp_annuity_anchor):
    """The 確定年金 pays exactly k instalments and the contract ends [S2] [S4].

    No maturity value, no continuation, no residual state: ``proj_len`` is 12(n_y + k)
    exactly, the last instalment falls at n + 12(k - 1) = 528, and the whole surviving
    in-force expires at the end of the policy year that instalment opens.  Those eleven
    trailing months carry maintenance expense and nothing else — the right answer, and one
    an annual grid could not give.
    """
    a = jp_annuity_anchor
    n, k = a.annuitisation_t(), a.payout_term_y()
    last_row = a.proj_len() - 1
    assert a.proj_len() == 12 * (a.annuitisation_y() + k) == 540
    assert len(a.result_cf()) == 540
    assert a.annuity_pp(n + 12 * (k - 1)) > 0.0      # the last instalment, at t = 528
    assert all(a.annuity_pp(t) == 0.0 for t in range(n + 12 * (k - 1) + 1, a.proj_len()))
    assert a.pols_if(last_row) > 0.0
    assert a.pols_if(a.proj_len()) == 0.0
    assert a.pols_maturity(last_row) == pytest.approx(a.pols_if(last_row), rel=1e-14)
    assert all(a.pols_maturity(t) == 0.0 for t in range(0, last_row))
    assert a.claims(last_row) == 0.0                 # expiry pays nothing
    assert a.net_cf(last_row) == pytest.approx(-a.expenses(last_row), abs=1e-9)


def test_late_duration_surrender_is_profitable_to_the_insurer(jp_annuity_anchor):
    """Key sensitivity 4: past the crossover a surrender returns less than the fund.

    From the elapsed month 149 the 解約返戻金 *is* the 死亡給付金, which is 月払保険料 x 経過月数 and
    stops growing at 払込満了 [S2] [S4].  A surrender at the anniversary 29 therefore pays
    JPY 5,220,000 — twenty-nine premiums, the benefit not reaching its JPY 5,400,000
    ceiling until the anniversary 30 — against an ``av_pp(29)`` of JPY 5,699,454.498584, so
    the insurer keeps JPY 479,454.50 of fund.  The monthly grid sharpens this rather than
    changing it: the ceiling now steps by one 月払保険料 a month, so a surrender in the
    seventh month of policy year 29 is valued on JPY 5,310,000 rather than on a
    year-rounded figure.  The sign is the reverse of a savings product's, which is why a
    prudent reserving basis loads late-duration lapse **down**, not up.
    """
    a = jp_annuity_anchor
    assert a.av_pp(29) == pytest.approx(FUND_AT_29, abs=FUND)
    assert a.cv_pp(29) == pytest.approx(SURRENDER_AT_29, abs=YEN)
    assert a.cv_pp(29) == a.db_pp(29) == 29 * 180_000.0
    assert a.db_pp(29) < a.db_pp(30) == CUMULATIVE_PREMIUMS
    assert a.av_pp(29) - a.cv_pp(29) == pytest.approx(FUND_KEPT_AT_29, abs=YEN)
    assert a.cv_at_m(12 * 29 + 6) == pytest.approx(5_310_000.0, abs=YEN)
    # ... and it holds at every month from the crossover to the 年金支払開始日.
    for u in range(CROSSOVER_MONTH, a.annuitisation_t()):
        assert a.av_at_m(u) > a.cv_at_m(u), f"u={u}"


def test_there_is_no_maturity_benefit(individual_annuity, jp_annuity_anchor):
    """The contract reaches a scheduled end but nothing is *paid* for reaching it.

    An 養老保険 pays a 満期保険金 and ends; this product pays its last 確定年金 instalment and ends.
    ``pols_maturity`` therefore exists — it is the library-wide count whose cover ends at
    the scheduled end of the contract, paid for or not — while ``claims(t, "MATURITY")``
    and a ``claims_maturity`` column do not.  Both halves are product facts, so both are
    asserted rather than left to inspection.
    """
    names = (set(individual_annuity.Projection.cells)
             | set(individual_annuity.Projection.refs))
    assert "pols_maturity" in names, "the scheduled-end count is part of this product"
    for absent in ("claims_maturity", "maturity_pp", "benefit_pp",
                   "sum_assured", "liability_cf"):
        assert absent not in names, f"{absent} is not part of this product"
    assert "claims_maturity" not in jp_annuity_anchor.result_cf().columns
    with pytest.raises(FormulaError):
        jp_annuity_anchor.claims(420, "MATURITY")
    # The scheduled end is the last row of the frame, and nothing at all is paid there.
    a = jp_annuity_anchor
    last = a.proj_len() - 1
    assert a.pols_maturity(last) > 0.0
    assert a.claims(last) == 0.0
    n, k = a.annuitisation_t(), a.payout_term_y()
    assert a.claims(n + 12 * (k - 1)) == pytest.approx(
        a.claims(n + 12 * (k - 1), "ANNUITY"), abs=YEN)


def test_premium_income_stops_at_payment_end_and_never_returns(individual_annuity):
    """No premium after 払込満了 and none at all once the annuity is in payment.

    Level and guaranteed for the whole 保険料払込期間 with no review right [S2] [S4] [S5] [S6],
    then nothing: the 据置期間 and the payout phase carry no premium.
    """
    for point_id in individual_annuity.Data.model_point_table().index:
        p = individual_annuity.Projection[point_id]
        m = p.premium_term_y()
        # the premium falls in one month of twelve, and in none of the other eleven
        for s_ in range(0, m):
            if not p.apl_on():
                assert p.premiums(12 * s_) == pytest.approx(
                    p.premium_pp() * p.pols_if(12 * s_), abs=1e-9)
            assert all(p.premiums(t) == 0.0
                       for t in range(12 * s_ + 1, 12 * s_ + 12))
        for t in range(12 * m, p.proj_len()):
            assert p.premiums(t) == 0.0, f"point {point_id}, t={t}"
            assert p.commissions(t) == 0.0
        for s_ in range(m, p.proj_years()):
            assert p.prem_to_av_pp(s_) == 0.0


def test_the_zero_deferral_gap_is_a_valid_model_point(individual_annuity):
    """d = 0 is a different product, not an edge case to be smoothed over [S6].

    Model point 3 annuitises at 払込満了, so n = m and the 据置期間 segment of the lapse table
    is never read.  The chassis has to express it without a code branch.
    """
    p = individual_annuity.Projection[3]
    assert p.defer_gap_y() == 0
    assert p.annuitisation_y() == p.premium_term_y() == 15
    assert p.annuitisation_t() == 180
    assert p.annuity_start_age() == 60
    assert p.premiums(168) > 0.0                 # the last premium month ...
    assert p.lapse_rate(168) == 0.0              # ... is inside the year lapse stops
    assert p.claims(180, "ANNUITY") > 0.0
    assert p.check_pols_roll_fwd() is True and p.check_fund() is True


def test_the_tontine_ratio_is_a_model_point_column_not_a_code_branch(
        individual_annuity):
    """rho = 0.70 is the same chassis under a lower death-benefit ceiling [S3] [S10].

    A 生存保障重視型 design pays 70% of cumulative premiums on death, which lowers the
    surrender ceiling with it and leaves a larger survivorship release in the fund.
    """
    p = individual_annuity.Projection[6]
    assert p.db_ratio() == 0.70
    assert p.tax_rider() is False
    m = p.premium_term_y()
    assert p.db_at_m(12 * m) == pytest.approx(p.db_pp(m), abs=1e-9)
    assert p.db_pp(m) == pytest.approx(0.70 * p.premium_pp() * m, abs=1e-9)
    assert p.cv_pp(m) <= p.db_pp(m) + 1e-9
    assert p.annuity_fund_pp() > p.premium_pp() * m      # the fund is not capped
    assert p.check_cv_cap() is True


def test_the_female_basis_is_sourced_on_one_table_and_a_setback_on_the_other(
        individual_annuity):
    """Two tables, two female bases, and the difference is what was retrievable.

    On 死亡保険用 both sexes carry their own sourced anchors [REG-R18], so the female rows are
    **not** a setback of the male ones and must not be asserted to be: the canonical table
    reads q(30) = 0.00037 female against 0.00068 male, which is not four years of male
    mortality.  On 年金開始後用 only male spot rates were retrieved, so its female rows are a
    four-year setback **[std]** — the setback the published terminal ages themselves imply,
    126 against 122 [R3] [REG-R19].  Both tables still run to different terminal ages by
    sex, which is a published fact about each of them.
    """
    male = individual_annuity.Projection[1]
    female = individual_annuity.Projection[8]
    assert male.sex() == "M" and female.sex() == "F"
    for table in ("death_cover_2018", "annuity_payout_2007"):
        assert female.omega_age(table) == male.omega_age(table) + 4
        # The female rate at a given age is the lighter of the two on both tables.
        assert female.mort_rate_at_age(table, 70) < male.mort_rate_at_age(table, 70)

    # The payout table really is a setback ...
    for age in (60, 80, 100):
        assert female.mort_rate_at_age(SETBACK_TABLE, age + 4) == pytest.approx(
            male.mort_rate_at_age(SETBACK_TABLE, age), rel=1e-12)
    # ... and the death-cover table is not.
    for age, rate in PUBLISHED_ANCHORS[("death_cover_2018", "F")].items():
        assert female.mort_rate_at_age("death_cover_2018", age) == pytest.approx(
            rate, abs=5e-12)
        assert female.mort_rate_at_age("death_cover_2018", age + 4) != pytest.approx(
            male.mort_rate_at_age("death_cover_2018", age), rel=1e-6)


def test_the_model_rejects_an_inconsistent_annuity_start_age(tmp_path):
    """annuity_start_age must equal x + m + d, and the model says so by name.

    Two spellings of one date is how a projection silently annuitises on the wrong year,
    so the derived quantity is checked against the model point rather than trusted.
    """
    model = variant_model(tmp_path, "Annuity_JP_S_bad_start", 1, annuity_start_age=64)
    try:
        with pytest.raises(FormulaError):
            model.Projection[1].result_cf()
    finally:
        model.close()


def test_the_tax_rider_conditions_are_validated(individual_annuity, tmp_path):
    """税制適格特約: ten years of premiums, start age 60+, ten years of payments [R10].

    The rider constrains the contract rather than the cash flows, so it validates the
    model point and then does nothing else — but a model point that claims the rider and
    breaks its conditions is projecting a contract that could not be sold with it.
    """
    assert individual_annuity.Projection[1].tax_rider() is True

    model = variant_model(tmp_path, "Annuity_JP_S_bad_rider", 1, payout_term_y=5)
    try:
        with pytest.raises(FormulaError):
            model.Projection[1].tax_rider()
    finally:
        model.close()


def test_invalid_arguments_are_rejected_by_name(individual_annuity, jp_annuity_anchor,
                                                tmp_path):
    """Every string-keyed argument rejects an unknown value rather than returning zero."""
    a = jp_annuity_anchor
    with pytest.raises(FormulaError):
        a.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        a.pols_if_at(0, "END")
    with pytest.raises(FormulaError):
        a.av_pp_at(0, "AFT_DECR")
    with pytest.raises(FormulaError):
        a.lapse_rate_mean("amount")

    model = variant_model(tmp_path, "Annuity_JP_S_bad_sex", 1, sex="X")
    try:
        with pytest.raises(FormulaError):
            model.Projection[1].result_cf()
    finally:
        model.close()

    model = variant_model(tmp_path, "Annuity_JP_S_bad_form", 1, payout_form="unit")
    try:
        with pytest.raises(FormulaError):
            model.Projection[1].result_cf()
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Results, inputs and documentation


def test_result_cf_shape(jp_annuity_anchor):
    """The published statement's frame, columns and their order, which readers depend on.

    The frame is the library-wide 0-based one: indexed by ``t``, opening at ``t = 0`` — the
    year of issue — and running contiguously to ``proj_len() - 1``, so it has exactly
    ``proj_len()`` rows.

    ``claims_commutation`` and ``policy_loans`` are columns of zeros in the base run and are
    published rather than dropped, because a zero states that a module is off where a
    missing column would only hide it.
    """
    a = jp_annuity_anchor
    df = a.result_cf()
    assert df.index.name == "t"
    assert df.index[0] == 0
    assert df.index[-1] == a.proj_len() - 1
    assert len(df) == a.proj_len()
    assert list(df.index) == list(range(a.proj_len()))
    assert list(df.index) == list(range(0, 540))
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_annuity", "claims_death", "claims_lapse",
        "claims_commutation", "expenses", "claim_expenses", "commissions", "policy_loans",
        "net_cf",
    ]
    assert df.loc[0, "net_cf"] == pytest.approx(77_665.70, abs=YEN)
    assert df.loc[420, "claims_annuity"] == pytest.approx(194_956.41, abs=YEN)
    # one premium month in twelve, one instalment month in twelve
    assert (df["premiums"] > 0).sum() == 30
    assert (df["claims_annuity"] > 0).sum() == 10


def test_result_pols_reads_the_crossover(jp_annuity_anchor):
    """The companion table puts the two in-force measures and the three values together.

    Reading the fund, the death benefit and the surrender value in one frame is the
    quickest way to see the crossover, where the fund passes the death benefit and the
    surrender value stops rising — and on this grid that happens at a **month**.

    The three value columns are named for the cells that produce them, ``av_at_m`` /
    ``db_at_m`` / ``cv_at_m``, because they are monthly readings: publishing them as
    ``av_pp`` / ``db_pp`` / ``cv_pp`` would name them after the anniversary quantities they
    equal on one row in twelve.
    """
    df = jp_annuity_anchor.result_pols()
    assert df.index.name == "t"
    assert list(df.index) == list(range(jp_annuity_anchor.proj_len()))
    assert list(df.columns) == [
        "pols_if", "lives_if", "pols_death", "pols_lapse", "pols_commute",
        "pols_maturity", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "av_at_m", "db_at_m", "cv_at_m",
    ]
    assert df.loc[CROSSOVER_MONTH - 1, "av_at_m"] < df.loc[CROSSOVER_MONTH - 1, "db_at_m"]
    assert df.loc[CROSSOVER_MONTH, "av_at_m"] > df.loc[CROSSOVER_MONTH, "db_at_m"]
    assert df.loc[CROSSOVER_MONTH, "cv_at_m"] == 2_235_000.0
    assert (df.loc[CROSSOVER_MONTH:419, "av_at_m"]
            > df.loc[CROSSOVER_MONTH:419, "db_at_m"]).all()
    assert (df.loc[CROSSOVER_MONTH:419, "cv_at_m"]
            == df.loc[CROSSOVER_MONTH:419, "db_at_m"]).all()


def test_net_cf_carries_the_notes_own_sign(individual_annuity, jp_annuity_anchor):
    """The notes print CF(t) income-positive, which is the library-wide sign.

    So there is no outgo-positive ``liability_cf`` companion here, unlike the payout
    annuity models whose notes print the other orientation — and that absence is a fact
    about which sign the notes chose, not an omission.
    """
    assert "liability_cf" not in individual_annuity.Projection.cells
    assert jp_annuity_anchor.net_cf(0) > 0.0          # premium month
    assert jp_annuity_anchor.net_cf(420) < 0.0        # annuity month


def test_inputs_live_beside_the_model():
    """The seven input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "mort_anchor_table.csv",
                "lapse_table.csv", "pricing_table.csv", "expense_table.csv",
                "commute_factor_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_every_assumption_row_marks_its_own_provenance():
    """Each assumption value is source-tagged or marked [std], in the file itself.

    This is the library's core integrity property, and the ``provenance`` column is where
    it lives for the inputs: never a sourced fact and a modelling assumption side by side
    with nothing to tell them apart.
    """
    for name in ("mort_table.csv", "mort_anchor_table.csv", "lapse_table.csv",
                 "pricing_table.csv", "expense_table.csv", "commute_factor_table.csv"):
        table = pd.read_csv(MODEL_DIR.parent / name)
        assert "provenance" in table.columns, name
        assert table["provenance"].notna().all(), name
        assert (table["provenance"].str.len() > 0).all(), name


def test_the_shipped_mortality_table_says_it_is_not_a_copy():
    """mort_table.csv is a [std] construction and every row says so.

    生保標準生命表2018 and the 2007 年金開始後用 table are readable at stable public URLs but their
    publisher's terms prohibit reproduction and transmission [REG-R21], so the library
    ships a documented proxy anchored to a table you can go and read.  Marking the rows is
    what stops the proxy being mistaken for the table.
    """
    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert set(table["table"]) == {"death_cover_2018", "annuity_payout_2007"}
    assert set(table["sex"]) == {"M", "F"}
    assert table["provenance"].str.contains(r"\[std\]", regex=True).all()
    assert not table["provenance"].str.contains("verbatim").any()

    # 死亡保険用 is the canonical library-wide file: every row says so, and every row says
    # whether it is a sourced anchor or a graduated value, on both sexes.
    death = table[table["table"] == "death_cover_2018"]["provenance"]
    assert death.str.contains("canonical jplib").all()
    assert death.str.contains("not a redistribution of the IAJ table").all()
    assert death.str.contains("ANCHOR row|INTERPOLATED row", regex=True).all()
    assert death.str.contains("ANCHOR row").any()
    assert death.str.contains("INTERPOLATED row").any()

    # 年金開始後用 is the fitted construction; its male rows say they are not a copy of the
    # IAJ workbook and its female rows say they are a setback of the male construction.
    payout = table[table["table"] == "annuity_payout_2007"]
    male = payout[payout["sex"] == "M"]["provenance"]
    female = payout[payout["sex"] == "F"]["provenance"]
    assert male.str.contains("Makeham construction").all()
    assert male.str.contains("not a copy").all()
    assert female.str.contains("setback of the male construction").all()

    anchors = pd.read_csv(MODEL_DIR.parent / "mort_anchor_table.csv")
    assert anchors["provenance"].str.contains(r"\[std\]", regex=True).all()
    # Three anchors per sex on 年金開始後用; the canonical anchor set on 死亡保険用.
    payout_anchors = anchors[anchors["table"] == "annuity_payout_2007"]
    assert len(payout_anchors) == 6
    death_anchors = anchors[anchors["table"] == "death_cover_2018"]
    assert len(death_anchors) > 6
    assert death_anchors["provenance"].str.contains("ANCHOR row").all()
    # Every anchor age is in the shipped table with the same rate, and the lowest anchor
    # is at or below the lowest age the table is shipped over, so nothing extrapolates.
    keyed = table.set_index(["table", "sex", "age"])
    for _, row in death_anchors.iterrows():
        shipped = keyed.loc[(row["table"], row["sex"], int(row["age"])), "mort_rate"]
        assert shipped == pytest.approx(row["mort_rate"], abs=5e-12)
    for sex in ("M", "F"):
        shipped_ages = table[(table["table"] == "death_cover_2018")
                             & (table["sex"] == sex)]["age"]
        anchor_ages = death_anchors[death_anchors["sex"] == sex]["age"]
        assert anchor_ages.min() == shipped_ages.min()
        assert anchor_ages.max() == shipped_ages.max()


def test_the_shipped_rates_reproduce_the_published_anchors_exactly():
    """The quoted spot rates are in mort_table.csv unchanged, at the sex they belong to.

    Quoting the rates a worked example needs, and attributing them, is what the publisher's
    terms permit; copying the table is not.  Both constructions reproduce their anchors
    exactly, which is what makes ``check_mort_graduation`` meaningful.
    """
    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv",
                        index_col=["table", "sex", "age"])
    for (name, sex), anchors in PUBLISHED_ANCHORS.items():
        for age, rate in anchors.items():
            assert table.loc[(name, sex, age), "mort_rate"] == pytest.approx(
                rate, abs=5e-12)
    # On the payout table alone, the female row four years later carries the male rate.
    for age, rate in PUBLISHED_ANCHORS[(SETBACK_TABLE, "M")].items():
        assert table.loc[(SETBACK_TABLE, "F", age + 4), "mort_rate"] == pytest.approx(
            rate, abs=5e-12)


def test_model_docstring_describes_the_current_structure(individual_annuity):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = flat(individual_annuity.doc)
    assert "mechanics demonstration" in doc
    assert "external" in doc                       # inputs are not stored in the model
    assert "once per model" in doc                 # why Data exists
    assert "two contracts joined at one date" in doc
    assert "reverses sign" in doc
    assert "no tail states" in doc


def test_space_docstrings_carry_their_reference_material(individual_annuity):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = flat(individual_annuity.Projection.doc)
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "av_pp", "cv_pp", "pols_if", "lives_if",
                  "annuity_fund_pp", "annuity_amount_pp", "mort_rate_pricing"):
        assert cells in proj, f"{cells} missing from the Projection docstring"
    data = flat(individual_annuity.Data.doc)
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_anchor_table"):
        assert cells in data


def test_the_check_cells_are_no_argument_booleans_with_signed_residuals(
        individual_annuity, jp_annuity_anchor):
    """Each check_*() has a check_*_resid(t) beside it, and neither takes the other's job.

    The bool is what one test can call across the whole library; the residual is what tells
    you which year failed and by how much.
    """
    cells = set(individual_annuity.Projection.cells)
    for name in ALL_CHECKS:
        assert name in cells
        assert name + "_resid" in cells
        assert isinstance(getattr(jp_annuity_anchor, name)(), bool)
        assert isinstance(getattr(jp_annuity_anchor, name + "_resid")(0), float)


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a production user
    does with a licensed table or a company lapse study: they drop in as same-schema CSVs
    with no formula change.  ``check_mort_graduation`` then reports False, which is the
    correct answer once the shipped construction has been replaced.
    """
    shutil.copytree(MODEL_DIR, tmp_path / MODEL_DIR.name)
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    doubled = pd.read_csv(tmp_path / "mort_table.csv",
                          index_col=["table", "sex", "age"])
    doubled["mort_rate"] = doubled["mort_rate"] * 2
    doubled.to_csv(tmp_path / "mort_doubled.csv")

    model = mx.read_model(tmp_path / MODEL_DIR.name, name="Annuity_JP_S_swap")
    try:
        base = model.Projection[1].mort_rate(0)
        model.Data.mort_table_file = "mort_doubled.csv"
        model.Data.clear_all()
        model.Projection.clear_all()
        assert model.Projection[1].mort_rate(0) == pytest.approx(2 * base, rel=1e-12)
        assert model.Projection[1].check_mort_graduation() is False
    finally:
        model.close()


def test_round_trip_reproduces_the_worked_example(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set.

    Inputs are external, so they must travel with the model: the CSVs are copied to the
    new parent directory before re-reading.  Without that the re-read model loads and then
    fails on first evaluation, which is exactly the trade-off this layout makes.
    """
    model = mx.read_model(MODEL_DIR, name="Annuity_JP_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Annuity_JP_S_rt")
    try:
        anchor = reread.Projection[1]
        assert anchor.annuity_fund_pp() == pytest.approx(
            FUND_AT_ANNUITISATION, abs=FUND)
        assert anchor.annuity_amount_pp() == ANNUITY_AMOUNT
        for t, row in DEFERRAL_ROWS.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[8], abs=YEN)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
