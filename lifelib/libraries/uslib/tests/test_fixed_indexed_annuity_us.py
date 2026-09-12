"""Golden and product-specific tests for FIA_US_S.

The golden values are the worked example in
products/fixed_indexed_annuity/technical-notes.md ("Worked example"), which projects
the anchor cell Male 62 ANB / single life / P = $100,000 / b = 7% / GLWB elected at issue
/ first lifetime withdrawal at anniversary 8 (attained age 70).  They are hard-coded here
rather than pickled so that a reviewer can compare them against the notes by eye.

``t`` is the 0-based **month** index.  Every contractual transaction is annual and falls
in the anniversary month, the last month of a contract year, so nearly every golden value
is read at :func:`anniv`: the notes' anniversary-8 table is month ``anniv(8) = 95``, and
the opening state the notes state at anniversary 7 is that contract year's opening timing.
Quantities the notes state as *opening* the contract year are read through
``av_pp_year_open`` and the ``"BEF_ROLLUP"`` timing rather than through ``t - 1``, which on
a monthly grid is the previous month and not the previous year.

Model point 1 enters the projection **in force at anniversary 7** - seven completed
contract years, so its first projected month is ``entry_mth() = 84`` - on the balances the
notes state there - AV 128,000.00, BB 180,000.00, RB 100,000.00, MGV 93,811.84 - because
the notes describe those as illustrative and "broadly consistent with a seven-year
deferral at these parameters" [std] rather than derived from one.  Deriving them would
mean retuning assumptions to force a match.  Model point 2 is the same cell issued at
t = 0 and carries the notes' Initialisation block instead.

Tolerances follow the precision the notes display: money to the cent, rates to the four
decimals of a percentage, the MVA factor to the eight decimals it is printed at.
"""
import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/fixed_indexed_annuity/FIA_US_S"

CENT = 0.005          # money displayed to 2 d.p.
RATE = 5e-7           # rates displayed as a percentage to 4 d.p.
FACTOR = 5e-9         # the MVA factor, displayed to 8 d.p.
EXACT = 1e-9

A8 = 95               # the worked example's anniversary: 12 x 8 - 1


def anniv(year):
    """The month index of the anniversary that **closes** contract year ``year``.

    ``12 * year - 1``.  Every one of the notes' eight processing steps happens here and
    nowhere else, so this is where a golden value is read.
    """
    return 12 * year - 1


def opens(year):
    """The **first month** of contract year ``year``: ``12 * (year - 1)``."""
    return 12 * (year - 1)


def raises_value_error(call, message):
    """A formula that raises ValueError surfaces as modelx's FormulaError wrapper.

    modelx re-raises formula exceptions wrapped in ``FormulaError`` with the original
    type and message in the text, so the guard is asserted on the message rather than on
    a modelx-internal exception class.
    """
    with pytest.raises(Exception) as excinfo:
        call()
    text = str(excinfo.value)
    assert "ValueError" in text and message in text, text


@pytest.fixture(scope="module")
def fixed_indexed_annuity():
    """The FIA_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(fixed_indexed_annuity):
    """Model point 1 - the worked-example anchor cell, in force at anniversary 7."""
    return fixed_indexed_annuity.Projection[1]


# ---------------------------------------------------------------------------
# The worked example, item by item.
#
# technical-notes.md, "Worked example", the sixteen-row table at anniversary 8, which
# closes contract year 8 - month anniv(8) = 95 on this grid:
#
#   1  Index return, year 8          5,450 / 5,000 - 1                    9.0000%
#   2  Credit rate                   max(0, min(5.25%, 9.00%))            5.2500%
#   3  Index credit IC(8)            128,000.00 x 0.0525                  6,720.00
#   4  Account value after credit    128,000.00 + 6,720.00              134,720.00
#   5  Rider charge Phi(8)           0.0095 x 180,000.00                  1,710.00
#   6  Account value after charge    134,720.00 - 1,710.00              133,010.00
#   7  Guaranteed rollup             0.0500 x 100,000.00                  5,000.00
#   8  Stacking credit               1.50 x 6,720.00                     10,080.00
#   9  Benefit base before step-up   180,000 + 5,000 + 10,080           195,080.00
#  10  Step-up test                  max(195,080.00, 133,010.00)        195,080.00
#  11  Lifetime withdrawal LW(8)     0.0520 x 195,080.00                 10,144.16
#  12  Free withdrawal amount FW(8)  0.10 x 128,000.00                   12,800.00
#  13  Excess E(8)                   max(0, 10,144.16 - 10,144.16)            0.00
#  14  Account value AV(8)           133,010.00 - 10,144.16             122,865.84
#  15  Guaranteed minimum MGV(8)     93,811.84 x 1.01 - 10,144.16        84,605.80
#  16  Closing benefit base BB(8)    unchanged by a guaranteed withdrawal 195,080.00
# ---------------------------------------------------------------------------

WORKED_EXAMPLE = [
    (1, "index return R(8)", lambda p: p.index_return(A8), 0.090000, RATE),
    (2, "credit rate cr(8)", lambda p: p.credit_rate(A8), 0.052500, RATE),
    (3, "index credit IC(8)", lambda p: p.index_credit_pp(A8), 6720.00, CENT),
    (4, "AV after credit", lambda p: p.av_pp_at(A8, "BEF_FEE"), 134720.00, CENT),
    (5, "rider charge Phi(8)", lambda p: p.rider_charge_pp(A8), 1710.00, CENT),
    (6, "AV(2) after charge", lambda p: p.av_pp_at(A8, "BEF_WD"), 133010.00, CENT),
    (7, "guaranteed rollup", lambda p: p.rollup_pp(A8), 5000.00, CENT),
    (8, "stacking credit", lambda p: p.stack_pp(A8), 10080.00, CENT),
    (9, "BB(3) before step-up",
     lambda p: p.benefit_base_pp_at(A8, "BEF_STEP_UP"), 195080.00, CENT),
    (10, "BB(4) after step-up",
     lambda p: p.benefit_base_pp_at(A8, "BEF_WD"), 195080.00, CENT),
    (11, "lifetime withdrawal LW(8)",
     lambda p: p.lw_pp_at(A8, "BEF_WD"), 10144.16, CENT),
    (12, "free withdrawal amount FW(8)", lambda p: p.free_wd_allow(A8), 12800.00, CENT),
    (13, "excess E(8)", lambda p: p.wd_excess_pp(A8), 0.00, CENT),
    (14, "account value AV(8)", lambda p: p.av_pp(A8), 122865.84, CENT),
    (15, "guaranteed minimum MGV(8)", lambda p: p.mgsv_pp(A8), 84605.80, CENT),
    (16, "closing benefit base BB(8)", lambda p: p.benefit_base_pp(A8), 195080.00, CENT),
]


@pytest.mark.parametrize(
    "item,label,getter,expected,tol", WORKED_EXAMPLE,
    ids=["%02d %s" % (row[0], row[1]) for row in WORKED_EXAMPLE])
def test_worked_example_row(anchor, item, label, getter, expected, tol):
    """Every row of the notes' sixteen-item table, to the precision it displays."""
    assert getter(anchor) == pytest.approx(expected, abs=tol)


def test_worked_example_opening_state(anchor):
    """The stated in-force position at anniversary 7 that the table is computed from.

    Anniversary 7 opens contract year 8, so the notes' opening state is that year's
    opening timing rather than a row of its own: there is no issue-instant row, and no
    pre-entry row on an in-force cell either.  On the monthly grid it is the state at
    month ``entry_mth() = 84``, eleven months before the table's own anniversary.
    """
    assert anchor.entry_year() == 7
    assert anchor.entry_mth() == 84
    assert opens(8) == anchor.entry_mth()
    assert anchor.av_pp_year_open(A8) == pytest.approx(128000.00, abs=CENT)
    assert anchor.av_pp_at(opens(8), "BEF_INV") == pytest.approx(128000.00, abs=CENT)
    assert anchor.benefit_base_pp_at(A8, "BEF_ROLLUP") == pytest.approx(180000.00,
                                                                       abs=CENT)
    assert anchor.rollup_base_pp_init() == pytest.approx(100000.00, abs=CENT)
    assert anchor.mgsv_pp_init() == pytest.approx(93811.84, abs=CENT)
    # Nothing was withdrawn before entry, so the first contract year's own withdrawal is
    # the whole of Wcum at the end of it.
    assert anchor.wd_cum_pp(A8) == pytest.approx(10144.16, abs=CENT)
    assert anchor.phase_init() == "ACCUM"
    assert anchor.phase_open(A8) == "INCOME"      # promoted by the first exercise
    # MGV(7) is 87,500 x 1.01^7, which the notes give as the derivation of 93,811.84.
    assert 0.875 * anchor.premium_pp() * 1.01 ** 7 == pytest.approx(93811.84, abs=CENT)


def test_the_step_up_does_not_bind_on_the_blended_baseline(anchor):
    """Row 10: the stack dominates, so max(195,080.00, 133,010.00) is the base itself."""
    assert anchor.step_up_applies(A8) is True
    assert (anchor.benefit_base_pp_at(A8, "BEF_WD")
            == anchor.benefit_base_pp_at(A8, "BEF_STEP_UP"))
    assert anchor.benefit_base_pp_at(A8, "BEF_WD") > anchor.av_pp_at(A8, "BEF_WD")


def test_a_guaranteed_withdrawal_leaves_the_guarantee_untouched(anchor):
    """Row 13 and row 16: E(8) = 0, so rho = 0 and BB, LW and RB are unchanged [S9]."""
    assert anchor.wd_pp(A8) == pytest.approx(anchor.lw_pp_at(A8, "BEF_WD"), abs=EXACT)
    assert anchor.wd_excess_pp(A8) == 0.0
    assert anchor.wd_reduction_rate(A8) == 0.0
    assert anchor.wd_charge_base_pp(A8) == 0.0
    assert anchor.wd_charge_pp(A8) == 0.0
    assert anchor.wd_clawback_pp(A8) == 0.0
    assert anchor.wd_mva_pp(A8) == 0.0
    assert anchor.benefit_base_pp(A8) == pytest.approx(195080.00, abs=CENT)
    assert anchor.lw_pp(A8) == pytest.approx(10144.16, abs=CENT)
    assert anchor.rollup_base_pp(A8) == pytest.approx(100000.00, abs=CENT)


# ---------------------------------------------------------------------------
# The surrender test at the same anniversary.
#
#   A full surrender of G = AV(8) = 122,865.84 with 12,800.00 - 10,144.16 = 2,655.84 of
#   free amount remaining gives X = 120,210.00; SC = 3% x 120,210.00 = 3,606.30;
#   clawback = 0.30 x (0.07/1.07) x 120,210.00 = 2,359.26; with i0 = 3.00%, it = 3.50%
#   and n = 24 months remaining, MVA = 120,210.00 x [(1.03/1.035)^2 - 1]
#   = 120,210.00 x (-0.00963850) = -1,158.64, inside the limit
#   max(0, 122,865.84 - 5,965.56 - 84,605.80) = 32,294.48.  Net proceeds
#   = 122,865.84 - 3,606.30 - 2,359.26 - 1,158.64 = 115,741.64, and
#   CSV = max(115,741.64, 84,605.80) = 115,741.64.
# ---------------------------------------------------------------------------

def test_surrender_trace_free_amount_and_charge_base(anchor):
    """The guaranteed withdrawal consumes the free amount [std], leaving 2,655.84."""
    assert anchor.free_wd_allow(A8) == pytest.approx(12800.00, abs=CENT)
    assert anchor.wd_free_pp(A8) == pytest.approx(10144.16, abs=CENT)
    assert anchor.free_wd_remain(A8) == pytest.approx(2655.84, abs=CENT)
    assert anchor.surr_charge_base_pp(A8) == pytest.approx(120210.00, abs=CENT)


def test_surrender_trace_charge_clawback_and_mva(anchor):
    """sc = 3% and v = 70% in contract year 8 [S5]; the MVA factor to eight decimals.

    ``mva_ref_yield`` is keyed by **anniversary number**, not by the frame's month index,
    so the 3.50% in force at the transaction is read at anniversary 8 - the one that
    closes contract year 8 - and its argument does not move with the grid.
    """
    assert anchor.policy_year(A8) == 8
    assert anchor.surr_charge_rate(A8) == pytest.approx(0.03, abs=RATE)
    assert anchor.vest_rate(A8) == pytest.approx(0.70, abs=RATE)
    assert anchor.surr_charge_pp(A8) == pytest.approx(3606.30, abs=CENT)
    assert anchor.surr_clawback_pp(A8) == pytest.approx(2359.26, abs=CENT)
    assert anchor.mva_term(A8) == 2.0                      # n = 24 months
    # The notes state n in months, so the monthly grid carries it exactly: six months
    # earlier a surrender has 30 months left, not the anniversary's 24.
    assert anchor.mva_term(A8 - 6) == pytest.approx(30 / 12, rel=1e-12)
    assert anchor.mva_ref_yield_at_issue() == pytest.approx(0.0300, abs=RATE)
    assert anchor.mva_ref_yield(8) == pytest.approx(0.0350, abs=RATE)
    assert anchor.duration(A8) + 1 == 8                    # the anniversary it reads at
    assert anchor.mva_rate(A8) == pytest.approx(-0.00963850, abs=FACTOR)
    assert anchor.mva_pp(A8) == pytest.approx(-1158.64, abs=CENT)


def test_surrender_trace_mva_collar_does_not_bind(anchor):
    """The limit max(0, G - SC - CB - MGV) = 32,294.48 [S10], well outside -1,158.64."""
    limit = max(0.0, anchor.av_pp(A8) - anchor.surr_charge_pp(A8)
                - anchor.surr_clawback_pp(A8) - anchor.mgsv_pp(A8))
    assert limit == pytest.approx(32294.48, abs=CENT)
    assert abs(anchor.mva_pp(A8)) < limit


def test_surrender_trace_net_proceeds_is_a_cent_rounding_artefact(anchor):
    """The notes' 115,741.64 is the sum of the *displayed* cent-rounded components.

    Every component reproduces exactly to the cent, but the clawback (2,359.26168) and
    the MVA (-1,158.64384) each carry fractions of a cent that the notes' displayed
    subtraction drops.  Carried at full precision - which is what the notes' own rounding
    convention asks for, "full precision internally, cents on reported cash flows [std]"
    - the net is 0.55 cents lower.  Both readings are pinned here rather than either
    being tuned away.
    """
    gross = anchor.av_pp(A8)
    sc, cb, mva = (anchor.surr_charge_pp(A8), anchor.surr_clawback_pp(A8),
                   anchor.mva_pp(A8))
    from_displayed = round(gross, 2) - round(sc, 2) - round(cb, 2) + round(mva, 2)
    assert from_displayed == pytest.approx(115741.64, abs=CENT)      # the notes' figure
    assert anchor.surr_value_pp(A8) == pytest.approx(115741.634475, abs=CENT)
    assert from_displayed - anchor.surr_value_pp(A8) == pytest.approx(0.0055, abs=1e-4)
    # The nonforfeiture floor does not bind: CSV = the surrender value, not MGV.
    assert anchor.surr_benefit_pp(A8) == pytest.approx(anchor.surr_value_pp(A8),
                                                       abs=EXACT)
    assert anchor.surr_benefit_pp(A8) > anchor.mgsv_pp(A8)


# ---------------------------------------------------------------------------
# "Where the step-up binds" - the notes' variant (a) block, on model point 3.
#
#   Under variant (a) - 3% simple rollup on RB, no stacking [S9] - the same cell carries
#   BB(7) = 121,000.00, so Phi(8) = 1,149.50, AV(2) = 133,570.50 and BB(3) = 124,000.00.
#   The step-up then binds: BB(8) = 133,570.50 and LW(8) = 0.0520 x 133,570.50 = 6,945.67.
# ---------------------------------------------------------------------------

def test_step_up_binds_under_the_pure_rollup_variant(fixed_indexed_annuity):
    """Growth mechanism (a): the step-up matters when credits outrun the rollup."""
    p = fixed_indexed_annuity.Projection[3]
    assert p.benefit_base_pp_at(A8, "BEF_ROLLUP") == pytest.approx(121000.00, abs=CENT)
    assert p.stack_factor() == 0.0
    assert p.rollup_rate(A8) == pytest.approx(0.03, abs=RATE)
    assert p.rider_charge_pp(A8) == pytest.approx(1149.50, abs=CENT)
    assert p.av_pp_at(A8, "BEF_WD") == pytest.approx(133570.50, abs=CENT)
    assert p.rollup_pp(A8) == pytest.approx(3000.00, abs=CENT)
    assert p.stack_pp(A8) == 0.0
    assert p.benefit_base_pp_at(A8, "BEF_STEP_UP") == pytest.approx(124000.00, abs=CENT)
    assert p.benefit_base_pp_at(A8, "BEF_WD") == pytest.approx(133570.50, abs=CENT)
    assert p.lw_pp_at(A8, "BEF_WD") == pytest.approx(6945.67, abs=CENT)


def test_step_up_binds_in_year_one_on_a_new_issue(fixed_indexed_annuity):
    """The notes' "rarely, not never" case, spelled out in the step 3 commentary.

    "the account-value bonus opens the first contract year at 107,000 above a benefit
    base of 100,000, so a first contract year with a zero index credit gives
    AV(2) = 106,050 against BB(3) = 105,000 and the step-up binds.  Test it at every
    anniversary rather than assuming the stack dominates."
    """
    p = fixed_indexed_annuity.Projection[2]
    assert p.entry_year() == 0
    assert p.entry_mth() == 0
    a1 = anniv(1)
    # The Initialisation block is the opening state of month 0, not a row of its own.
    assert p.av_pp_at(0, "BEF_INV") == pytest.approx(107000.00, abs=CENT)   # P(1+b) [S5]
    assert p.av_pp_year_open(a1) == pytest.approx(107000.00, abs=CENT)
    assert p.benefit_base_pp_at(a1, "BEF_ROLLUP") == pytest.approx(
        100000.00, abs=CENT)                                    # bonus excluded
    assert p.rollup_base_pp_init() == pytest.approx(100000.00, abs=CENT)
    assert p.mgsv_pp_init() == pytest.approx(87500.00, abs=CENT)  # 0.875 x P, no bonus
    assert p.index_credit_pp(a1) == 0.0
    assert p.rider_charge_pp(a1) == pytest.approx(950.00, abs=CENT)
    assert p.av_pp_at(a1, "BEF_WD") == pytest.approx(106050.00, abs=CENT)
    assert p.benefit_base_pp_at(a1, "BEF_STEP_UP") == pytest.approx(105000.00, abs=CENT)
    assert p.benefit_base_pp(a1) == pytest.approx(106050.00, abs=CENT)   # the step-up
    # ... and the same cell rolled forward seven years reaches the notes' MGV(7), the
    # value closing contract year 7 and opening contract year 8.  The floor accrues
    # monthly, so this is 87,500 x 1.01^(84/12) and not a coarser approximation of it.
    assert p.mgsv_pp(anniv(7)) == pytest.approx(93811.84, abs=CENT)


# ---------------------------------------------------------------------------
# "Where the liability lands" - the depletion arithmetic.
#
#   Holding index credits at zero from anniversary 8, the account value drains by
#   LW + Phi = 10,144.16 + 0.0095 x 195,080.00 = 11,997.42 a year and is exhausted during
#   contract year 19, at attained age about 81.  From that point the insurer pays
#   $10,144.16 a year for the rest of the contract holder's life, with no account value,
#   no surrender value, no death benefit and no possibility of lapse.
# ---------------------------------------------------------------------------

def test_the_account_value_drains_by_11997_42_a_year(anchor):
    """LW + Phi = 10,144.16 + 1,853.26, constant because the base stops growing.

    The drain is a *yearly* figure and still is: the withdrawal and the charge both fall
    at the anniversary, so the account value steps down once a contract year rather than
    twelve times.
    """
    drain = anchor.lw_pp(A8) + 0.0095 * anchor.benefit_base_pp(A8)
    assert drain == pytest.approx(11997.42, abs=CENT)
    for year in range(9, 19):
        t = anniv(year)
        assert anchor.index_credit_pp(t) == 0.0
        assert anchor.rider_charge_pp(t) == pytest.approx(1853.26, abs=CENT)
        assert anchor.wd_pp(t) == pytest.approx(10144.16, abs=CENT)
        assert (anchor.av_pp_year_open(t) - anchor.av_pp(t)) == pytest.approx(
            11997.42, abs=CENT)


def test_the_account_value_is_exhausted_during_contract_year_19(anchor):
    """At attained age 81, and the phase is DEPLETED - not TERMINATED."""
    t = anniv(19)
    assert anchor.policy_year(t) == 19
    assert anchor.av_pp(anniv(18)) > 0.0
    assert anchor.av_pp(anniv(18)) == pytest.approx(2891.64, abs=CENT)
    assert anchor.av_pp(t) == 0.0
    assert anchor.exercise_age(t) == 81           # at the closing anniversary
    assert anchor.phase(anniv(18)) == "INCOME"
    assert anchor.phase(t) == "DEPLETED"
    assert anchor.depletion_cause(t) is False
    # The insurer funds the shortfall in the depletion year itself.
    assert anchor.av_depletion_pp(t) == pytest.approx(
        10144.16 - anchor.av_pp_at(t, "BEF_WD"), abs=CENT)


def test_the_income_stream_survives_exhaustion(anchor):
    """The guarantee: LW a year for life, from the insurer's own funds [S1][S3][S9]."""
    for year in range(20, 31):
        t = anniv(year)
        assert anchor.phase(t) == "DEPLETED"
        assert anchor.av_pp(t) == 0.0
        assert anchor.wd_pp(t) == pytest.approx(10144.16, abs=CENT)
        assert anchor.rider_charge_pp(t) == 0.0        # nothing to deduct it from [S9]
        assert anchor.index_credit_pp(t) == 0.0        # steps 1-3 are skipped
        assert anchor.lapse_rate(t) == 0.0             # lapse is impossible [S1][S9]
        assert anchor.lapse_rate_mth(t) == 0.0         # ... in every month of the year
        assert anchor.claim_pp(t, "DEATH") == 0.0      # no death benefit
        assert anchor.surr_benefit_pp(t) == 0.0        # no surrender value
        assert anchor.income_payments(t) == pytest.approx(
            10144.16 * anchor.pols_if(t), abs=CENT)    # weighted by who reaches it
        assert anchor.wd_guar(t) == 0.0                # reported on the income line only


def test_income_runs_to_the_end_of_the_projection(anchor):
    """Nothing but death exits the depleted state, so the payment runs to the horizon.

    The in-force reaches the final contract year and the guarantee is still being paid
    there.  It does not reach the final *month*: the shipped table's terminal rate is
    q = 1.000000, which converts to a monthly rate of 1.0, so the survivors all die in
    the first month of that year.  That is what an annual rate of one means once it is
    spread; the annual grid could only say "during the year".
    """
    assert anchor.phase(anchor.proj_len() - 1) == "DEPLETED"
    last_year_opens = anchor.proj_len() - 12
    assert anchor.pols_if(last_year_opens) > 0.0
    assert anchor.mort_rate_mth(last_year_opens) == 1.0
    assert anchor.pols_if(last_year_opens + 1) == 0.0
    assert sum(anchor.income_payments(t)
               for t in range(anniv(20), anchor.proj_len())) > 0.0


# ---------------------------------------------------------------------------
# One test per entry in the notes' "Known modeling pitfalls" list.
# ---------------------------------------------------------------------------

def test_pitfall_the_floor_is_on_the_credit_not_the_account_value(fixed_indexed_annuity):
    """"Rider charges and strategy fees can exceed interest credited" [S7].

    Flooring the account value at its prior balance silently removes the charge drag
    that produces depletion.  Model point 2 has a zero index credit in year 1 and a $950
    rider charge, so the account value must *fall* over its first contract year.
    """
    p = fixed_indexed_annuity.Projection[2]
    a1 = anniv(1)
    assert p.credit_rate(a1) == 0.0                      # the credit is floored at zero
    assert p.credit_rate_on(-0.30, "cap") == 0.0         # ... however bad the index year
    assert p.av_pp(a1) < p.av_pp_year_open(a1)           # ... the account value is not


def test_pitfall_the_clawback_factor_is_b_over_one_plus_b(anchor):
    """"The clawback factor is b/(1+b), not b" [S10]; using b over-recovers by (1+b).

    Worked verbatim at [S10] in the product spec: contract year 5, bonus 16%, gross
    $100,000, free $7,000 gives 70% x 0.1379 x $93,000 = $8,979.
    """
    assert anchor.bonus_factor() == pytest.approx(0.07 / 1.07, rel=1e-12)
    assert anchor.bonus_clawback_on(93000.0, 0.30, 0.16) == pytest.approx(8979.0, abs=0.5)
    assert anchor.bonus_clawback_on(93000.0, 0.30, 0.16) == pytest.approx(
        0.70 * (0.16 / 1.16) * 93000.0, rel=1e-12)
    # Using b directly would over-recover by exactly (1 + b).
    naive = 0.70 * 0.16 * 93000.0
    assert naive / anchor.bonus_clawback_on(93000.0, 0.30, 0.16) == pytest.approx(1.16)


def test_pitfall_the_simple_rollup_is_a_flat_dollar_increment(anchor):
    """"The 'simple rollup' is a flat dollar increment", never on the grown base [S2][S9].

    Compounding it inflates the base and every downstream charge and payment.  The
    increment stays at 5% of the *rollup base*, which is untouched by a guaranteed
    withdrawal, while the benefit base itself nearly doubles.
    """
    p = anchor
    assert p.rollup_pp(A8) == pytest.approx(0.05 * p.rollup_base_pp_init(), abs=CENT)
    assert p.rollup_pp(A8) == pytest.approx(5000.00, abs=CENT)
    assert p.rollup_base_pp_init() == pytest.approx(100000.00, abs=CENT)
    # Simple interest on the *grown* base would have been 0.05 x 180,000 = 9,000.
    assert p.rollup_pp(A8) != pytest.approx(
        0.05 * p.benefit_base_pp_at(A8, "BEF_ROLLUP"), abs=1.0)


def test_pitfall_attribution_at_depletion(fixed_indexed_annuity, anchor):
    """"a model testing only AV <= 0 will either give the guarantee away ... or destroy it".

    Point 1 withdraws exactly LW and reaches DEPLETED with the income intact.  Point 7 is
    the identical cell overdrawing at 105% of the maximum, so every year carries an excess
    withdrawal, depletion_cause is set and the same exhaustion TERMINATES the contract.
    """
    p7 = fixed_indexed_annuity.Projection[7]
    assert p7.utilization_intensity() == 1.05
    assert p7.wd_excess_pp(A8) > 0.0
    assert p7.depletion_cause(A8) is True
    assert anchor.depletion_cause(A8) is False

    terminated = [t for t in range(p7.entry_mth(), p7.proj_len())
                  if p7.phase(t) == "TERMINATED"]
    depleted = [t for t in range(anchor.entry_mth(), anchor.proj_len())
                if anchor.phase(t) == "DEPLETED"]
    assert terminated and depleted
    # The phase turns only at an anniversary, so the first month carrying it is one.
    assert terminated[0] % 12 == 11
    assert depleted[0] % 12 == 11
    assert p7.av_pp(terminated[0]) == 0.0
    assert anchor.av_pp(depleted[0]) == 0.0
    # Same exhaustion, opposite outcome: the guarantee survives on one and not the other.
    # The deemed full surrender takes the survivors in the terminating month itself, so
    # the opening count of the month after it is zero.
    assert p7.pols_if(terminated[0]) > 0.0
    assert p7.pols_if(terminated[0] + 1) == 0.0
    assert p7.pols_if_at(terminated[0], "AFT_DECR") == 0.0
    assert anchor.pols_if(depleted[0]) > 0.0
    assert all(p7.income_payments(t) == 0.0
               for t in range(p7.entry_mth(), p7.proj_len()))
    assert sum(anchor.income_payments(t)
               for t in range(anchor.entry_mth(), anchor.proj_len())) > 0.0


def test_the_terminating_branch_pays_only_what_the_account_value_holds(
        fixed_indexed_annuity, anchor):
    """The attribution has to reach the cash, not only the phase label.

    Points 1 and 7 exhaust in the same contract year and the notes send them opposite
    ways.  On the DEPLETED branch the insurer funds the whole shortfall from its own funds
    - that stream is the guarantee.  On the TERMINATED branch it funds none of it: the
    balance is gone and the rider that would have covered the rest was destroyed by the
    very withdrawal being paid, [S5] treating the contract "as well as the rider" as
    Surrendered at that point.  Paying the request in full on both branches would honour
    the guarantee in the year the excess withdrawal kills it - the same failure the
    attribution test exists to prevent, one step further downstream.
    """
    p7 = fixed_indexed_annuity.Projection[7]
    t = anniv(19)
    assert p7.phase(anniv(18)) == "INCOME"
    assert p7.phase(t) == "TERMINATED"

    # What the contract could meet, against what was asked for.
    assert p7.av_pp_at(t, "BEF_WD") == pytest.approx(765.92, abs=CENT)
    assert p7.wd_pp(t) == pytest.approx(7856.61, abs=CENT)
    assert p7.lw_pp_at(t, "BEF_WD") == pytest.approx(7482.49, abs=CENT)
    assert p7.wd_excess_pp(t) == pytest.approx(374.12, abs=CENT)
    assert p7.av_depletion_pp(t) == pytest.approx(7090.69, abs=CENT)

    # None of that shortfall is payable, so the cash is the balance and nothing more.
    assert p7.wd_unfunded_pp(t) == pytest.approx(7090.69, abs=CENT)
    assert p7.wd_payment_pp(t) == pytest.approx(765.92, abs=CENT)
    assert p7.withdrawals(t) == pytest.approx(765.92 * p7.pols_if(t), abs=CENT)
    # The excess goes unpaid first and the guaranteed portion only after it [S9], [std].
    assert p7.wd_excess_paid_pp(t) == 0.0
    assert p7.wd_guar_paid_pp(t) == pytest.approx(765.92, abs=CENT)
    assert p7.wd_excess(t) == 0.0
    assert p7.wd_guar(t) == pytest.approx(p7.withdrawals(t), abs=EXACT)
    # ... and nothing at all is paid once the contract has terminated.
    assert all(p7.withdrawals(u) == 0.0 for u in range(t + 1, p7.proj_len()))

    # The cap is on the payment, not on the withdrawal: the guarantee is still destroyed.
    assert p7.depletion_cause(t) is True
    assert p7.wd_reduction_rate(t) == 1.0
    assert p7.benefit_base_pp(t) == 0.0

    # The contrast, in the same contract year: on the DEPLETED branch it IS all paid.
    assert anchor.phase(t) == "DEPLETED"
    assert anchor.av_pp_at(t, "BEF_WD") == pytest.approx(1038.38, abs=CENT)
    assert anchor.av_depletion_pp(t) == pytest.approx(9105.78, abs=CENT)
    assert anchor.wd_unfunded_pp(t) == 0.0
    assert anchor.wd_payment_pp(t) == pytest.approx(10144.16, abs=CENT)


def test_pitfall_an_overdraw_permanently_reduces_the_guarantee(fixed_indexed_annuity,
                                                               anchor):
    """"a 5% overdraw permanently reduces the guarantee" - efficiency is not free [R1]."""
    p7 = fixed_indexed_annuity.Projection[7]
    assert p7.lw_pp_at(A8, "BEF_WD") == pytest.approx(10144.16, abs=CENT)
    assert p7.wd_pp(A8) == pytest.approx(1.05 * 10144.16, abs=CENT)
    assert p7.wd_excess_pp(A8) == pytest.approx(0.05 * 10144.16, abs=CENT)
    rho = p7.wd_reduction_rate(A8)
    assert rho > 0.0
    assert p7.benefit_base_pp(A8) == pytest.approx(195080.00 * (1 - rho), abs=CENT)
    assert p7.benefit_base_pp(A8) < anchor.benefit_base_pp(A8)
    assert p7.lw_pp(A8) < anchor.lw_pp(A8)
    assert p7.rollup_base_pp(A8) == pytest.approx(100000.00 * (1 - rho), abs=CENT)


def test_pitfall_no_lapse_in_depleted(anchor):
    """"Leaving the surrender decrement on silently truncates the ... liability."

    Both the annual rate and the monthly one it converts to are zero, so no month of a
    depleted contract year loses a life to surrender.
    """
    depleted = [t for t in range(anchor.entry_mth(), anchor.proj_len() - 1)
                if anchor.phase(t) == "DEPLETED"]
    assert depleted
    for t in depleted:
        assert anchor.lapse_rate(t) == 0.0
        assert anchor.lapse_rate_mth(t) == 0.0
        assert anchor.pols_lapse(t) == 0.0
        # only mortality exits: the count closing month t opens it, less that month's
        # deaths
        assert anchor.pols_if(t + 1) == pytest.approx(
            anchor.pols_if(t) * (1 - anchor.mort_rate_mth(t)), rel=1e-12)
        assert anchor.pols_if_at(t, "AFT_DECR") == pytest.approx(
            anchor.pols_if(t + 1), rel=1e-12)


def test_pitfall_rider_charge_base_and_ordering(anchor):
    """"The charge is on the benefit base ... and is taken after index credits" [S9].

    "In the worked example the benefit base closes at 1.59x the account value at
    anniversary 8 (195,080.00 against 122,865.84), so charging on the account value
    understates the deduction by a growing margin."
    """
    assert anchor.rider_charge_pp(A8) == pytest.approx(0.0095 * 180000.00, abs=CENT)
    # ... on the OPENING base, because the base is updated after the charge.
    assert anchor.rider_charge_pp(A8) == pytest.approx(
        0.0095 * anchor.benefit_base_pp_at(A8, "BEF_ROLLUP"), abs=CENT)
    # ... and after the index credit: the charge lands on AV(1), not on the opening AV.
    assert anchor.av_pp_at(A8, "BEF_WD") == pytest.approx(
        anchor.av_pp_at(A8, "BEF_FEE") - anchor.rider_charge_pp(A8), abs=EXACT)
    assert anchor.av_pp_at(A8, "BEF_FEE") > anchor.av_pp_year_open(A8)
    ratio = anchor.benefit_base_pp(A8) / anchor.av_pp(A8)
    assert ratio == pytest.approx(1.59, abs=0.005)
    # Charging on the account value would understate the deduction.
    assert 0.0095 * anchor.av_pp_at(A8, "BEF_FEE") < anchor.rider_charge_pp(A8)


def test_pitfall_excess_withdrawal_denominator(anchor):
    """"the two differ by exactly LW" - and the [S9] worked case pins the post form.

    "account value $100,000, base $200,000, annual benefit amount $10,000, withdrawal
    $28,000 -> denominator $90,000, excess $18,000, reduction 20%, base -> $160,000,
    benefit amount -> $8,000."
    """
    assert anchor.wd_reduction_rate_on(100000.0, 10000.0, 28000.0) == pytest.approx(
        0.20, abs=1e-12)
    assert 200000.0 * (1 - 0.20) == 160000.0
    assert 10000.0 * (1 - 0.20) == 8000.0
    # Pre-exercise the denominator is the gross account value: rho = G / AV.
    assert anchor.wd_reduction_rate_on(100000.0, 0.0, 28000.0) == pytest.approx(
        0.28, abs=1e-12)
    # A non-positive denominator sends the base to zero and terminates the rider [S9].
    assert anchor.wd_reduction_rate_on(10000.0, 10000.0, 28000.0) == 1.0


def test_pitfall_mva_sign_collar_and_scope(anchor, fixed_indexed_annuity):
    """"Negative when yields rise; applies only above the free amount, only inside the
    MVA period, never to the death benefit, never below the nonforfeiture minimum" [S10].
    """
    # Negative when the reference yield has risen above the issue level.
    assert anchor.mva_ref_yield(8) > anchor.mva_ref_yield_at_issue()
    assert anchor.mva_rate(A8) < 0.0
    # Only inside the ten-year MVA period: the remaining term runs out at anniversary 10,
    # so a transaction carries an adjustment in contract years 1-9 and none in year 10.
    assert anchor.mva_in_force(anniv(9)) is True          # contract year 9
    assert anchor.mva_term(anniv(10)) == 0.0              # contract year 10
    assert anchor.mva_in_force(anniv(10)) is False
    assert anchor.mva_rate(anniv(10)) == 0.0
    assert anchor.mva_pp(anniv(11)) == 0.0
    # Never on the death benefit: it is max(AV, MGV), with no charge and no adjustment,
    # and that holds in every month, not only at the anniversary.
    for t in (anniv(9), anniv(9) - 5):
        assert anchor.claim_pp(t, "DEATH") == pytest.approx(
            max(anchor.av_pp(t), anchor.mgsv_pp(t)), abs=EXACT)
        assert anchor.claim_pp(t, "DEATH") > anchor.claim_pp(t, "LAPSE")
    # Never below the nonforfeiture minimum: the collar and then the floor.
    for year in range(8, 12):
        t = anniv(year)
        assert anchor.surr_benefit_pp(t) >= anchor.mgsv_pp(t) - EXACT
    # The ratio form is naturally bounded; a rate rise cannot make it explode.
    assert anchor.mva_rate(A8) > -0.02


def test_pitfall_the_model_805_floor_is_15bp_not_1_percent(anchor):
    """"the composite's 1.00% is a [std] pick inside the corridor, not the statutory floor".

    The statute *defines the minimum*, so the test is
    ``mgsv_rate >= mgsv_rate_statutory(...)``, never the reverse.
    """
    # CMT5 = 1.00% would give -0.25% before the floor; the floor is 15 bp, not 1%.
    assert anchor.mgsv_rate_statutory(0.0100, 0.0) == pytest.approx(0.0015, abs=1e-12)
    assert anchor.mgsv_rate_statutory(0.0100, 0.0) != pytest.approx(0.01, abs=1e-4)
    # 2.00% CMT5 -> 0.75%; capped at 3% however high CMT5 goes.
    assert anchor.mgsv_rate_statutory(0.0200, 0.0) == pytest.approx(0.0075, abs=1e-12)
    assert anchor.mgsv_rate_statutory(0.0800, 0.0) == pytest.approx(0.0300, abs=1e-12)
    # Section 4C: the extra reduction needs an option cost of at least 25 bp ...
    assert anchor.mgsv_rate_statutory(0.0200, 0.0010) == pytest.approx(0.0075, abs=1e-12)
    # ... and is then min(100 bp, option cost).
    assert anchor.mgsv_rate_statutory(0.0200, 0.0050) == pytest.approx(0.0025, abs=1e-12)
    assert anchor.mgsv_rate_statutory(0.0400, 0.0200) == pytest.approx(0.0175, abs=1e-12)
    # The composite's 1.00% is compliant at these levels, which is the direction to test.
    assert anchor.mgsv_rate_is_compliant(0.0200, 0.0) is True
    assert anchor.mgsv_rate_is_compliant(0.0400, 0.0) is False


def test_pitfall_the_mva_collar_on_a_partial_withdrawal_is_shipped_both_ways(
        fixed_indexed_annuity, anchor):
    """The notes are silent on applying a *surrender-value* collar to a partial withdrawal.

    Read literally the limit is measured against the gross withdrawal, so a partial
    withdrawal smaller than the nonforfeiture floor gets no adjustment at all; measured
    against the account value it gets the adjustment its rate produces.  The two are
    identical on the surrender path, which is the only case the worked example shows, so
    neither reading can be preferred on the evidence and both are shipped behind
    ``mva_collar_basis``.  This test pins the gap open.
    """
    base, small = anchor.surr_charge_base_pp(A8), 20000.0
    # Same input, two readings, on the withdrawal path.
    assert anchor.mva_pp_on(A8, base, small) == 0.0                   # "gross", default
    model = mx.read_model(MODEL_PATH, name="FIA_collar")
    try:
        model.Projection.mva_collar_basis = "surrender_value"
        alt = model.Projection[1]
        assert alt.mva_pp_on(A8, base, small) == pytest.approx(-1158.64, abs=CENT)
        # ... but the worked example's surrender trace is invariant, because G = AV there.
        assert alt.mva_pp(A8) == pytest.approx(anchor.mva_pp(A8), abs=1e-9)
        assert alt.surr_value_pp(A8) == pytest.approx(anchor.surr_value_pp(A8), abs=1e-9)
    finally:
        model.close()


def test_pitfall_monthly_sum_is_not_implemented(anchor):
    """The notes call the monthly-sum floor convention ambiguous and exclude it.

    The grid is monthly, but the *index path* is not: ``rate_scenario.csv`` states index
    levels at anniversaries only, so there are no monthly returns to sum.  Every
    implemented method is reachable; the unimplemented one raises rather than silently
    returning something plausible.
    """
    for method in ("cap", "par", "par_cap", "spread", "trigger"):
        assert anchor.credit_rate_on(0.10, method) >= 0.0
    raises_value_error(lambda: anchor.credit_rate_on(0.10, "monthly_sum"),
                       "invalid credit_method")


def test_pitfall_index_costs_are_deducted_before_the_cap_and_participation_rate(anchor):
    """"embedded servicing, transaction and financing costs ... which reduce R(t) *before*
    the cap or participation rate" [S2][S10].

    The other half of the "Interim values and index costs" pitfall.  The interim-value
    structures it names are not implemented at all; this haircut is, and it is zero in the
    base run [std], so the only way to see it is to switch it on.
    """
    assert anchor.index_cost_rate == 0.0                 # off in the base run [std]
    model = mx.read_model(MODEL_PATH, name="FIA_index_cost")
    try:
        model.Projection.index_cost_rate = 0.005
        p = model.Projection[1]
        # Off R before the cap: a 4% index year credits 3.5%, not 4%.
        assert anchor.credit_rate_on(0.04, "cap") == pytest.approx(0.0400, abs=RATE)
        assert p.credit_rate_on(0.04, "cap") == pytest.approx(0.0350, abs=RATE)
        # ... and before the participation rate: 0.8 x (10% - 0.5%), not 0.8 x 10% - 0.5%.
        assert p.credit_rate_on(0.10, "par") == pytest.approx(0.8 * 0.095, abs=RATE)
        assert p.credit_rate_on(0.10, "par") != pytest.approx(0.8 * 0.10 - 0.005,
                                                              abs=RATE)
        # The cap still binds after the haircut, and the floor is still on the credit.
        assert p.credit_rate_on(0.10, "cap") == pytest.approx(0.0525, abs=RATE)
        assert p.credit_rate_on(0.004, "cap") == 0.0
        # It reaches the projection, not just the engine: the worked example's 9.00% year
        # is capped either way, but a year inside the cap is not.
        assert p.credit_rate(A8) == pytest.approx(0.0525, abs=RATE)
        assert p.credit_rate_on(anchor.index_return(A8) / 3.0, "cap") == pytest.approx(
            0.03 - 0.005, abs=RATE)
    finally:
        model.close()


def test_the_spread_and_trigger_levels_are_marked_std(anchor, fixed_indexed_annuity):
    """The notes give the index-margin and trigger *forms* but declare no level.

    ``max(f, p x R - s)`` [S8][R1] and ``d x 1{R >= 0}`` [R1] are printed; neither
    technical-notes.md nor product-spec.md states a value for ``s`` or ``d``.  Every
    number that is not from a source must carry [std], so the two levels the unsourced
    branches need are marked at the point of use.  Contrast ``par_rate``, which is [R1]'s
    own 80%, and ``cap_rate``, which is [S2]'s 5.25%.
    """
    assert anchor.spread_rate == pytest.approx(0.0200, abs=RATE)
    assert anchor.trigger_rate == pytest.approx(0.0450, abs=RATE)
    doc = fixed_indexed_annuity.Projection.credit_rate_on.doc
    assert "``spread_rate`` = 2.00% **[std]**" in doc
    assert "``trigger_rate`` = 4.50% **[std]**" in doc
    # The sourced pair keeps its citation instead of the mark.
    assert anchor.par_rate == pytest.approx(0.80, abs=RATE)
    assert anchor.cap_rate() == pytest.approx(0.0525, abs=RATE)
    assert "min(80% x 10%, 6%) = 6%" in doc and "[R1]" in doc
    # Both levels are live: they are what the two branches credit.
    assert anchor.credit_rate_on(0.10, "spread") == pytest.approx(
        0.80 * 0.10 - 0.0200, abs=RATE)
    assert anchor.credit_rate_on(0.10, "trigger") == pytest.approx(0.0450, abs=RATE)


# ---------------------------------------------------------------------------
# Crediting engine, schedules and behaviour.
# ---------------------------------------------------------------------------

def test_crediting_engine_reproduces_the_R1_worked_case(fixed_indexed_annuity):
    """"worked at [R1] as min(80% x 10%, 6%) = 6%" - model point 4 carries p and c."""
    p = fixed_indexed_annuity.Projection[4]
    assert p.par_rate == 0.80
    assert p.cap_rate_in_force() == pytest.approx(0.06, abs=RATE)
    assert p.credit_rate_on(0.10, "par_cap") == pytest.approx(0.06, abs=RATE)
    assert p.credit_rate_on(0.05, "par_cap") == pytest.approx(0.04, abs=RATE)
    assert p.credit_rate_on(0.10, "par") == pytest.approx(0.08, abs=RATE)
    assert p.credit_rate_on(-0.10, "par") == 0.0
    assert p.credit_rate_on(-0.10, "trigger") == 0.0
    assert p.credit_rate_on(0.00, "trigger") == pytest.approx(p.trigger_rate, abs=RATE)


def test_the_declared_and_guaranteed_scales_are_kept_apart(anchor):
    """Class (a) and class (b) "must not be mixed in the code"."""
    assert anchor.cap_rate_in_force() == pytest.approx(0.0525, abs=RATE)    # declared
    assert anchor.cap_rate_min == pytest.approx(0.0025, abs=RATE)           # guaranteed
    assert anchor.fixed_rate_in_force() == pytest.approx(0.0230, abs=RATE)
    assert anchor.fixed_rate_min == pytest.approx(0.0100, abs=RATE)
    model = mx.read_model(MODEL_PATH, name="FIA_guaranteed")
    try:
        model.Projection.use_guaranteed_scale = True
        g = model.Projection[1]
        assert g.cap_rate_in_force() == pytest.approx(0.0025, abs=RATE)
        assert g.fixed_rate_in_force() == pytest.approx(0.0100, abs=RATE)
        assert g.credit_rate(A8) == pytest.approx(0.0025, abs=RATE)
        assert g.av_pp(A8) < anchor.av_pp(A8)
    finally:
        model.close()


def test_the_surrender_charge_and_vesting_schedules(anchor):
    """9.1% grading to 0% and 0% grading to 100% over eleven contract years [S5]."""
    expected_sc = [0.091, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.0]
    expected_v = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # The schedules are stated by contract year, which is duration(t) + 1.
    for year, (sc, v) in enumerate(zip(expected_sc, expected_v), start=1):
        t = anniv(year)
        assert anchor.policy_year(t) == year
        assert anchor.surr_charge_rate(t) == pytest.approx(sc, abs=RATE)
        assert anchor.vest_rate(t) == pytest.approx(v, abs=RATE)
        # ... and the year's rate holds for every month inside it, not only the last.
        assert anchor.surr_charge_rate(opens(year)) == pytest.approx(sc, abs=RATE)
        assert anchor.vest_rate(opens(year)) == pytest.approx(v, abs=RATE)
    assert anchor.surr_charge_rate(anniv(25)) == 0.0        # the last row holds
    assert anchor.vest_rate(anniv(25)) == 1.0


def test_the_payout_percentage_bands(anchor):
    """Five bands [S3]; joint is single less 0.50% [S1][S3]; below 50 there is none."""
    for age, single in ((50, 0.037), (54, 0.037), (55, 0.042), (60, 0.047),
                        (69, 0.047), (70, 0.052), (79, 0.052), (80, 0.057),
                        (95, 0.057)):
        assert anchor.payout_rate(age, "single") == pytest.approx(single, abs=RATE)
        assert anchor.payout_rate(age, "joint") == pytest.approx(single - 0.005,
                                                                abs=RATE)
    assert anchor.payout_rate(45, "single") == 0.0
    raises_value_error(lambda: anchor.payout_rate(70, "survivor"), "invalid glwb_basis")


def test_the_payout_percentage_is_locked_at_first_exercise(anchor):
    """pi is fixed by the attained age at the first lifetime withdrawal [std]."""
    assert anchor.is_exercise(A8) is True
    assert anchor.exercise_age(A8) == 70
    assert anchor.payout_rate_locked(A8) == pytest.approx(0.052, abs=RATE)
    for year in range(9, 25):
        t = anniv(year)
        assert anchor.is_exercise(t) is False
        assert anchor.payout_rate_locked(t) == pytest.approx(0.052, abs=RATE)
    # The 80+ band is never re-read even though the annuitant passes 80 in year 18.
    assert anchor.exercise_age(anniv(18)) == 80
    assert anchor.payout_rate(80, "single") == pytest.approx(0.057, abs=RATE)
    assert anchor.payout_rate_locked(anniv(18)) == pytest.approx(0.052, abs=RATE)


def test_the_joint_basis_reads_the_younger_life(fixed_indexed_annuity):
    """joint = single - 0.50%, on the younger covered person [S1][S3]."""
    p = fixed_indexed_annuity.Projection[5]
    assert p.glwb_basis() == "joint"
    assert p.joint_age() == 60
    assert p.age_at_entry() == 62
    exercise = [y for y in range(1, 41) if p.is_exercise(anniv(y))]
    assert exercise == [10]             # the younger life reaches 70 closing year 10
    t = anniv(10)
    assert p.exercise_age(t) == 70
    assert p.age(t) + 1 == 72                    # the annuitant is already 72
    assert p.payout_rate_locked(t) == pytest.approx(0.047, abs=RATE)
    # is_exercise is a property of the contract year, so it holds in all twelve months.
    assert all(p.is_exercise(u) is True for u in range(opens(10), t + 1))


def test_income_never_decreases_after_exercise(fixed_indexed_annuity):
    """"After exercise the ratchet still applies ... so income never decreases" [S3]."""
    p = fixed_indexed_annuity.Projection[5]
    years = [y for y in range(1, p.proj_len() // 12 + 1)
             if p.phase(anniv(y)) == "INCOME"]
    for y in years[1:]:
        assert p.lw_pp_at(anniv(y), "BEF_WD") >= p.lw_pp(anniv(y - 1)) - EXACT


def test_benefit_base_growth_stops_at_the_first_lifetime_withdrawal(anchor):
    """T_g = min(first lifetime withdrawal, contract year 20) [S1][S2].

    The contract year of exercise is still inside the window - the worked example credits
    both the rollup and the stack in contract year 8 - and every later one is outside it.
    """
    assert anchor.in_growth_period(A8) is True
    assert anchor.rollup_pp(A8) > 0.0
    assert anchor.stack_pp(A8) > 0.0
    for year in range(9, 21):
        t = anniv(year)
        assert anchor.in_growth_period(t) is False
        assert anchor.rollup_pp(t) == 0.0
        assert anchor.stack_pp(t) == 0.0
        assert anchor.benefit_base_pp(t) == pytest.approx(195080.00, abs=CENT)


def test_the_growth_period_also_ends_at_contract_year_20(fixed_indexed_annuity):
    """The other leg of T_g = min(first lifetime withdrawal, contract year 20) [S1][S2].

    Model point 9 defers income to attained age 85, so the twenty-year window closes
    first and the benefit base is frozen for three years before the rider is exercised.
    """
    q = fixed_indexed_annuity.Projection[9]
    assert q.income_start_age() == 85
    assert q.is_exercise(anniv(23)) is True       # after the window, not before it
    assert q.in_growth_period(anniv(20)) is True  # contract year 20
    assert q.in_growth_period(anniv(21)) is False  # contract year 21
    assert q.rollup_pp(anniv(21)) == 0.0
    assert q.stack_pp(anniv(21)) == 0.0
    frozen = q.benefit_base_pp(anniv(20))
    for year in range(21, 24):
        assert q.benefit_base_pp(anniv(year)) == pytest.approx(frozen, abs=CENT)
    # A model point with no rider has nothing to grow at all.
    p = fixed_indexed_annuity.Projection[6]
    assert p.glwb_elected() is False
    assert p.in_growth_period(anniv(20)) is False


def test_the_rollup_schedule_steps_down_in_year_eleven(fixed_indexed_annuity):
    """5.00% in contract years 1-10, 2.00% in 11-20, zero after [S2]."""
    q = fixed_indexed_annuity.Projection[9]
    assert q.rollup_id() == "blended"
    for year in (1, 5, 10):
        assert q.rollup_rate(anniv(year)) == pytest.approx(0.0500, abs=RATE)
    for year in (11, 15, 20):
        assert q.rollup_rate(anniv(year)) == pytest.approx(0.0200, abs=RATE)
    for year in (21, 30):
        assert q.rollup_rate(anniv(year)) == 0.0
    assert q.rollup_pp(anniv(20)) == pytest.approx(
        0.02 * q.rollup_base_pp(anniv(19)), abs=CENT)
    # The Nassau schedule is a flat 3% over fifteen anniversaries instead [S9].
    p = fixed_indexed_annuity.Projection[3]
    assert p.rollup_id() == "nassau"
    assert p.rollup_rate(anniv(1)) == pytest.approx(0.03, abs=RATE)
    assert p.rollup_rate(anniv(15)) == pytest.approx(0.03, abs=RATE)
    assert p.rollup_rate(anniv(16)) == 0.0


def test_the_payout_percentage_locks_in_the_80_plus_band(fixed_indexed_annuity):
    """The [std] extension of [S3]'s single "80" row, reached by a late exerciser."""
    q = fixed_indexed_annuity.Projection[9]
    t = anniv(23)
    assert q.exercise_age(t) == 85
    assert q.payout_rate_locked(t) == pytest.approx(0.0570, abs=RATE)
    assert q.lw_pp_at(t, "BEF_WD") == pytest.approx(
        0.0570 * q.benefit_base_pp_at(t, "BEF_WD"), abs=CENT)


def test_the_shock_lapse_is_suppressed_by_the_rider(fixed_indexed_annuity, anchor):
    """33% without a rider, 10% with one idle, 5% once activated [R8], all [std].

    "Applying a plain fixed-deferred shock lapse to a rider-in-force FIA is the most
    consequential error available here."
    """
    shock_t = anniv(anchor.surr_charge_period + 1)    # contract year 11
    assert anchor.policy_year(shock_t) == 11
    no_rider = fixed_indexed_annuity.Projection[6]
    idle = fixed_indexed_annuity.Projection[9]
    assert no_rider.glwb_elected() is False
    assert no_rider.shock_lapse_rate(shock_t) == pytest.approx(0.33, abs=RATE)
    assert idle.phase_open(shock_t) == "ACCUM"          # rider in force, not activated
    assert idle.rider_in_force_open(shock_t) is True
    assert idle.shock_lapse_rate(shock_t) == pytest.approx(0.10, abs=RATE)
    assert anchor.phase_open(shock_t) == "INCOME"       # activated
    assert anchor.shock_lapse_rate(shock_t) == pytest.approx(0.05, abs=RATE)
    assert no_rider.lapse_rate_base(shock_t) == pytest.approx(0.33, abs=RATE)


def test_the_shock_lapse_is_spread_over_its_contract_year(fixed_indexed_annuity):
    """Unlike Term_US_S, where the notes put the shock on a contractual date.

    The FIA notes state the shock as the surrender rate *of contract year 11*, a year
    that carries no surrender charge in any of its months, so there is no date inside it
    for the decision to cluster on and the annual rate is converted like any other.  In
    :mod:`.Term_US_S` the notes say "applied in full at the end of the final level-period
    month" and the whole shock lands in that one month.
    """
    p = fixed_indexed_annuity.Projection[6]           # no rider: the undamped 33%
    year = p.surr_charge_period + 1
    assert p.surr_charge_rate(anniv(year)) == 0.0     # nothing left to charge
    monthly = 1.0 - (1.0 - 0.33) ** (1.0 / 12.0)
    for t in range(opens(year), anniv(year) + 1):
        assert p.lapse_rate(t) == pytest.approx(0.33, abs=RATE)
        assert p.lapse_rate_mth(t) == pytest.approx(monthly, abs=1e-12)
    # Twelve of them compound back to exactly the year's rate.
    assert (1.0 - monthly) ** 12 == pytest.approx(1.0 - 0.33, rel=1e-12)


def test_the_deemed_full_surrender_at_termination_is_not_spread(fixed_indexed_annuity):
    """A contractual event, not a behavioural rate: it lands whole on the anniversary.

    [S5] treats the contract "as well as the rider" as Surrendered on the date the
    account value is destroyed, so the survivors leave in that month and not before.
    """
    p7 = fixed_indexed_annuity.Projection[7]
    t = anniv(19)
    assert p7.phase(t) == "TERMINATED"
    assert p7.lapse_rate(t) == 1.0
    assert p7.lapse_rate_mth(t) == 1.0
    # ... and nothing of it falls in the eleven months before the anniversary.
    for u in range(opens(19), t):
        assert p7.lapse_rate_mth(u) == 0.0
        assert p7.pols_lapse(u) == 0.0
    assert p7.pols_lapse(t) == pytest.approx(p7.pols_if_at(t, "BEF_LAPSE"), rel=1e-12)


def test_the_base_surrender_shape(fixed_indexed_annuity):
    """Low early, rising through the charge period, spiking at expiry, then elevated."""
    p = fixed_indexed_annuity.Projection[6]        # no rider, so no moneyness damping
    expected = {1: 0.02, 3: 0.02, 4: 0.03, 6: 0.03, 7: 0.04, 9: 0.04,
                10: 0.05, 11: 0.33, 12: 0.06, 30: 0.06}
    for year, rate in expected.items():
        t = anniv(year)
        assert p.lapse_rate_base(t) == pytest.approx(rate, abs=RATE)
        assert p.lapse_moneyness_factor(t) == 1.0
        assert p.lapse_rate(t) == pytest.approx(min(0.35, rate), abs=RATE)
        assert p.lapse_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - min(0.35, rate)) ** (1.0 / 12.0), abs=1e-12)


def test_the_moneyness_multiplier_suppresses_surrender(anchor):
    """M_money = clamp(1 - 0.6 max(0, BB/AV - 1), 0.2, 1.0) [std]; and the cap at 35%.

    Read on the state **closing** the contract year, so it is one factor for the year
    rather than a number that drifts with the fixed-account accrual inside it.
    """
    t = anniv(11)
    ratio = anchor.benefit_base_pp(t) / anchor.av_pp(t)
    assert ratio > 1.0
    assert anchor.lapse_moneyness_factor(t) == pytest.approx(
        max(0.2, 1.0 - 0.6 * (ratio - 1.0)), abs=1e-12)
    assert all(anchor.lapse_moneyness_factor(u) == anchor.lapse_moneyness_factor(t)
               for u in range(opens(11), t + 1))
    for u in range(anchor.entry_mth(), anchor.proj_len()):
        assert 0.2 <= anchor.lapse_moneyness_factor(u) <= 1.0
        assert anchor.lapse_rate(u) <= anchor.lapse_rate_max


def test_activation_incidence_is_reported_and_rmd_age_is_configurable(anchor):
    """h(a) [std]; rmd_age "must not be hard-coded" [REG-R57][REG-R58]."""
    assert anchor.rmd_age == 73
    assert anchor.activation_rate(55) == 0.0
    assert anchor.activation_rate(60) == pytest.approx(0.05, abs=RATE)
    assert anchor.activation_rate(72) == pytest.approx(0.05, abs=RATE)
    assert anchor.activation_rate(73) == pytest.approx(0.40, abs=RATE)
    assert anchor.activation_rate(80) == pytest.approx(0.15, abs=RATE)
    # The deterministic run activates at income_start_age, not on this table.
    assert anchor.income_start_age() == 70
    assert anchor.is_exercise(A8) is True
    assert anchor.exercise_age(A8) == 70


def test_exercise_is_barred_below_the_contractual_minimum_age(fixed_indexed_annuity):
    """The minimum age for lifetime withdrawals is 50 [S2][S3][S9]."""
    p = fixed_indexed_annuity.Projection[2]
    assert p.min_income_age == 50
    for year in range(1, 8):
        t = anniv(year)
        assert p.is_exercise(t) is False
        assert p.lw_pp(t) == 0.0
        assert p.wd_pp(t) == 0.0


# ---------------------------------------------------------------------------
# The pre-exercise withdrawal path.
# ---------------------------------------------------------------------------

def test_a_pre_exercise_withdrawal_charges_on_the_gross_amount(fixed_indexed_annuity):
    """Before exercise X = max(0, G - FW) and rho = G / AV(2) [S1][S3][S5][S9]."""
    p = fixed_indexed_annuity.Projection[8]
    t = anniv(3)
    assert p.policy_year(t) == 3            # the withdrawal is in contract year 3
    assert p.wd_pp(t) == pytest.approx(60000.00, abs=CENT)
    assert p.phase_open(t) == "ACCUM"
    assert p.lw_pp_at(t, "BEF_WD") == 0.0
    assert p.wd_excess_pp(t) == pytest.approx(60000.00, abs=CENT)   # LW = 0, all excess
    assert p.free_wd_allow(t) == pytest.approx(0.10 * p.av_pp_year_open(t), abs=CENT)
    assert p.wd_charge_base_pp(t) == pytest.approx(
        60000.00 - p.free_wd_allow(t), abs=CENT)
    assert p.wd_charge_pp(t) == pytest.approx(
        0.08 * p.wd_charge_base_pp(t), abs=CENT)                    # sc = 8% in year 3
    assert p.wd_clawback_pp(t) == pytest.approx(
        0.80 * (0.07 / 1.07) * p.wd_charge_base_pp(t), abs=CENT)    # v = 20% in year 3
    assert p.wd_mva_pp(t) < 0.0                                     # the yield has risen
    assert p.wd_reduction_rate(t) == pytest.approx(
        60000.00 / p.av_pp_at(t, "BEF_WD"), rel=1e-12)
    assert p.benefit_base_pp(t) == pytest.approx(
        p.benefit_base_pp_at(t, "BEF_WD") * (1 - p.wd_reduction_rate(t)), abs=CENT)
    assert p.rollup_base_pp(t) == pytest.approx(
        100000.00 * (1 - p.wd_reduction_rate(t)), abs=CENT)
    assert p.depletion_cause(t) is True                             # charge and MVA bit


def test_the_model_point_provenance_names_the_schedule_it_points_at(
        fixed_indexed_annuity):
    """A shipped input file must describe the input it actually points at.

    Point 8's ``wd_schedule_id`` is ``preexercise``, whose one row - keyed by an elapsed
    contract year count, so 2 for the withdrawal at the anniversary closing contract
    year 3 - is $60,000, the same figure the README quotes and the projection returns.
    The key is unchanged by the move to a monthly grid, because it was never the frame's
    own index.  The $20,000 in this README's MVA-collar illustration is a different number
    for a different purpose and must not leak into the model point's own provenance.
    """
    mp = fixed_indexed_annuity.Data.model_point_table()
    wd = fixed_indexed_annuity.Data.withdrawal_table()
    p = fixed_indexed_annuity.Projection[8]
    t = anniv(3)
    assert mp.loc[8, "wd_schedule_id"] == "preexercise"
    amount = float(wd.loc[("preexercise", 2), "wd_amount"])
    assert p.duration(t) == 2
    assert amount == pytest.approx(60000.00, abs=CENT)
    assert p.wd_pp(t) == pytest.approx(amount, abs=CENT)
    provenance = mp.loc[8, "provenance"]
    assert "$60,000" in provenance
    assert "$20,000" not in provenance


def test_the_free_withdrawal_amount_does_not_carry_forward(fixed_indexed_annuity):
    """10% of the account value opening each contract year, no carry-forward [S9][S10]."""
    p = fixed_indexed_annuity.Projection[8]
    assert p.free_wd_allow(anniv(1)) == pytest.approx(
        0.10 * p.av_pp_at(0, "BEF_INV"), abs=CENT)
    for year in range(2, 11):
        assert p.free_wd_allow(anniv(year)) == pytest.approx(
            0.10 * p.av_pp(anniv(year - 1)), abs=CENT)
    # ... and it is the same figure in every month of the year, not a running 10%.
    assert all(p.free_wd_allow(u) == p.free_wd_allow(anniv(5))
               for u in range(opens(5), anniv(5) + 1))
    assert p.free_wd_allow(anniv(4)) < p.free_wd_allow(anniv(3))   # the year-3 withdrawal


# ---------------------------------------------------------------------------
# The monthly grid: what it changes, and what it must leave alone.
# ---------------------------------------------------------------------------

def test_the_monthly_decrement_rates_compound_to_the_annual_ones(fixed_indexed_annuity):
    """1 - (1-q)^(1/12) twelve times over is exactly q, so the anniversaries are unmoved.

    This is what makes the finer grid a redistribution of the same decrement rather than
    a different assumption.  Dividing by twelve instead would overstate it, and the error
    grows with the rate.
    """
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        for t in range(p.entry_mth(), p.proj_len(), 37):
            q, w = p.mort_rate(t), p.lapse_rate(t)
            assert (1.0 - p.mort_rate_mth(t)) ** 12 == pytest.approx(1.0 - q, rel=1e-12)
            if w < 1.0:
                assert (1.0 - p.lapse_rate_mth(t)) ** 12 == pytest.approx(
                    1.0 - w, rel=1e-12)
            # The annual rates are properties of the contract year, not of the month.
            assert p.mort_rate(t) == p.mort_rate(p.anniv_mth(t))
            assert p.lapse_rate(t) == p.lapse_rate(p.anniv_mth(t))


def test_the_fixed_account_accrues_monthly_to_exactly_the_annual_rate(
        fixed_indexed_annuity):
    """(1 + i_F)^(1/12) - 1 a month, twelve of which compound to i_F [S2][S10].

    Model point 4 is the only one with a non-zero fixed allocation, so it is the one that
    exercises this.  The benefit-base stack is computed on the *annual* figure, which is
    why ``fixed_interest_ann_pp`` exists beside the month's own accrual.
    """
    p = fixed_indexed_annuity.Projection[4]
    assert p.alloc_fixed() == pytest.approx(0.20, abs=1e-12)
    i_f = p.fixed_rate_in_force()
    monthly = (1.0 + i_f) ** (1.0 / 12.0) - 1.0
    assert p.fixed_interest_pp(0) == pytest.approx(0.20 * 107000.0 * monthly, abs=CENT)
    a1 = anniv(1)
    assert p.fixed_interest_ann_pp(a1) == pytest.approx(0.20 * 107000.0 * i_f, abs=CENT)
    # The twelve accruals of contract year 1 are the annual figure, to the cent.
    accrued = sum(p.fixed_interest_pp(t) for t in range(opens(1), a1 + 1))
    assert accrued == pytest.approx(p.fixed_interest_ann_pp(a1), abs=1e-8)
    # ... and the balance itself grows by exactly (1 + i_F) over the year.
    assert p.av_fixed_pp_at(a1, "BEF_FEE") == pytest.approx(
        p.av_fixed_pp_year_open(a1) * (1.0 + i_f), abs=1e-8)
    # The annual figure is zero away from the anniversary; the monthly one never is.
    assert p.fixed_interest_ann_pp(a1 - 1) == 0.0
    assert p.fixed_interest_pp(a1 - 1) > 0.0


def test_the_model_805_floor_accrues_monthly_and_deducts_at_the_anniversary(anchor):
    """Accrete, then deduct - now at (1 + i_nf)^(1/12) a month [S10][R2].

    A mid-year death or surrender is valued on the floor it actually has, which is the
    point of accruing it monthly; the anniversary value is unchanged, so the worked
    example's ``93,811.84 x 1.01 - 10,144.16 = 84,605.80`` still holds exactly.
    """
    i_nf = anchor.mgsv_rate
    opening = anchor.mgsv_pp_init()
    for t in range(anchor.entry_mth(), A8):
        assert anchor.mgsv_pp(t) == pytest.approx(
            opening * (1.0 + i_nf) ** ((t - anchor.entry_mth() + 1) / 12.0), rel=1e-12)
    assert anchor.mgsv_pp(A8 - 1) == pytest.approx(
        opening * (1.0 + i_nf) ** (11.0 / 12.0), rel=1e-12)
    assert anchor.mgsv_pp(A8) == pytest.approx(
        opening * (1.0 + i_nf) - anchor.wd_pp(A8), abs=CENT)
    assert anchor.mgsv_pp(A8) == pytest.approx(84605.80, abs=CENT)
    # The charge it would carry is annual too, and zero in this composite [std].
    assert anchor.mgsv_charge_pp(A8 - 1) == 0.0
    assert anchor.mgsv_charge_pp(A8) == 0.0


def test_no_contractual_cash_moves_between_anniversaries(fixed_indexed_annuity):
    """Every one of the notes' eight steps is annual, so eleven months in twelve are quiet.

    The finer grid resolves the decrements, the fixed accrual, the nonforfeiture roll and
    the maintenance expense.  It must not move a withdrawal, a charge or an index credit
    off the date the contract puts it on.
    """
    annual = ("wd_pp", "index_credit_pp", "rider_charge_pp", "rollup_pp", "stack_pp",
              "withdrawals", "wd_guar", "wd_excess", "income_payments",
              "fixed_interest_ann_pp", "wd_charge_pp", "wd_clawback_pp", "wd_mva_pp")
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        for t in range(p.entry_mth(), p.proj_len()):
            if p.is_anniv(t):
                continue
            for cells in annual:
                assert getattr(p, cells)(t) == 0.0, (point_id, t, cells)
            assert p.step_up_applies(t) is False
            assert p.wd_reduction_rate(t) == 0.0


def test_the_indexed_account_is_flat_between_anniversaries(fixed_indexed_annuity):
    """The annual point-to-point segment locks only at maturity [S1], so nothing accrues.

    That is the sourced rule "withdrawals are not credited with index interest in the year
    they are taken" carried to mid-year exits [std]; crediting a part year would be the
    daily interim value variant the notes exclude.  The fixed account is the balance that
    does move.
    """
    p = fixed_indexed_annuity.Projection[4]        # 80/20 indexed/fixed
    for year in (2, 5, 9):
        opening = p.av_indexed_pp(opens(year) - 1)
        for t in range(opens(year), anniv(year)):
            assert p.av_indexed_pp(t) == pytest.approx(opening, abs=1e-9), (year, t)
            assert p.av_fixed_pp(t) > p.av_fixed_pp(t - 1)
            assert p.index_credit_pp(t) == 0.0
    # The credit the segment earns arrives whole, in the anniversary month.
    a = anniv(1)
    assert p.index_credit_pp(a) > 0.0
    assert p.av_indexed_pp(a) != pytest.approx(p.av_indexed_pp(a - 1), abs=1.0)


def test_the_anniversary_state_is_what_an_annual_step_would_have_produced(anchor):
    """The invariant the conversion rests on, stated as arithmetic rather than as a diff.

    Each annual state cells steps once a contract year from the value at the previous
    anniversary, and carries it unchanged in between, so a reader can check the whole
    rider layer by reading twelve-month strides.
    """
    for year in range(9, 20):
        a, prev = anniv(year), anniv(year - 1)
        assert anchor.benefit_base_pp_at(a, "BEF_ROLLUP") == pytest.approx(
            anchor.benefit_base_pp(prev), abs=EXACT)
        assert anchor.av_pp_year_open(a) == pytest.approx(anchor.av_pp(prev), abs=EXACT)
        for t in range(opens(year), a):
            assert anchor.benefit_base_pp(t) == pytest.approx(
                anchor.benefit_base_pp(prev), abs=EXACT)
            assert anchor.rollup_base_pp(t) == pytest.approx(
                anchor.rollup_base_pp(prev), abs=EXACT)
            assert anchor.lw_pp(t) == pytest.approx(anchor.lw_pp(prev), abs=EXACT)
            assert anchor.phase(t) == anchor.phase(prev)
            assert anchor.payout_rate_locked(t) == anchor.payout_rate_locked(prev)


# ---------------------------------------------------------------------------
# Structural invariants.
# ---------------------------------------------------------------------------

def test_inforce_rollforward_closes(fixed_indexed_annuity):
    """pols_if(t) - pols_if(t+1) = deaths + surrenders + horizon exits, every model point.

    The no-argument ``check_pols_roll_fwd()`` is the library-wide form - one call covering
    every projected ``t`` - and ``check_pols_roll_fwd_resid(t)`` is the signed residual a
    debugging session needs when it fails.
    """
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        assert p.check_pols_roll_fwd() is True, point_id
        for t in range(p.entry_mth(), p.proj_len()):
            assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12), (
                point_id, t)


def test_account_value_rollforward_closes(fixed_indexed_annuity):
    """The account value roll-forward closes on every model point, including at depletion."""
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        assert p.check_av_roll_fwd() is True, point_id
        for t in range(p.entry_mth(), p.proj_len()):
            assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6), (
                point_id, t)


def test_the_two_accounts_sum_to_the_account_value(fixed_indexed_annuity):
    """AV = F + A at every timing, which is what makes av_indexed_pp a derived quantity."""
    p = fixed_indexed_annuity.Projection[4]        # 80/20 indexed/fixed
    assert p.alloc_fixed() == pytest.approx(0.20, abs=1e-12)
    assert p.av_fixed_pp_at(0, "BEF_INV") == pytest.approx(0.20 * 107000.0, abs=CENT)
    for t in range(0, p.proj_len()):
        for timing in ("BEF_PREM", "BEF_INV", "BEF_FEE", "BEF_WD", "EOY"):
            assert (p.av_fixed_pp_at(t, timing) + p.av_indexed_pp_at(t, timing)
                    == pytest.approx(p.av_pp_at(t, timing), abs=1e-6)), (t, timing)


def test_the_stack_uses_the_gross_index_credit_not_the_starved_one(
        fixed_indexed_annuity):
    """Design (b): 250% reaches the benefit base while kappa sends 50% to the AV [S3][S4].

    The stack is computed on the contract year's *annual* fixed interest; the account
    value receives that same interest one month at a time.
    """
    p = fixed_indexed_annuity.Projection[4]
    a1 = anniv(1)
    assert p.av_int_factor() == 0.50
    assert p.stack_factor() == 2.50
    assert p.rollup_rate(a1) == 0.0                # pure stacking: g = 0
    assert p.rollup_pp(a1) == 0.0
    ic = p.index_credit_pp(a1)
    fi_ann = p.fixed_interest_ann_pp(a1)
    assert p.stack_pp(a1) == pytest.approx(2.50 * (ic + fi_ann), abs=CENT)
    assert p.inv_income_pp(a1) == pytest.approx(
        0.50 * ic + p.fixed_interest_pp(a1), abs=CENT)


def test_withdrawals_partition_into_the_three_ledger_lines(fixed_indexed_annuity):
    """withdrawals = guaranteed + excess + post-depletion income, in every month."""
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        for t in range(p.entry_mth(), p.proj_len()):
            assert p.withdrawals(t) == pytest.approx(
                p.wd_guar(t) + p.wd_excess(t) + p.income_payments(t), abs=1e-9), (
                point_id, t)


def test_internal_transfers_are_not_cash_flows(anchor):
    """"SC, CB and Phi(t) are internal transfers ... not separate cash flows."

    Reporting them as fee income while also projecting the account value net of them
    double-counts.
    """
    df = anchor.result_cf()
    assert "rider_charge" not in df.columns
    assert "surr_charge" not in df.columns
    assert "index_credit" not in df.columns
    assert anchor.rider_charge_pp(A8) > 0.0   # it exists, it just is not a ledger line
    assert anchor.net_cf(A8) == pytest.approx(
        anchor.premiums(A8) - anchor.withdrawals(A8) - anchor.claims(A8)
        - anchor.commissions(A8) - anchor.expenses(A8) - anchor.premium_taxes(A8),
        abs=EXACT)


def test_expenses_follow_the_notes_ledger(fixed_indexed_annuity):
    """6.0% of premium at issue and $80 a year inflating at 2.5%, both [std].

    The maintenance charge is an insurer cost accruing continuously rather than a
    contractual event, so on the finer grid it falls a twelfth at a time and inflates by
    a fractional power.  With no issue-instant row the acquisition expense falls in month
    0 beside that month's own maintenance charge, so the first row carries both.
    """
    p = fixed_indexed_annuity.Projection[2]
    assert p.expenses(0) == pytest.approx(
        0.06 * 100000.0 + 80.0 / 12.0 * p.pols_if(0), abs=CENT)
    assert p.expenses(1) == pytest.approx(
        80.0 / 12.0 * 1.025 ** (1 / 12) * p.pols_if(1), abs=CENT)
    assert p.expenses(48) == pytest.approx(
        80.0 / 12.0 * 1.025 ** 4 * p.pols_if(48), abs=CENT)
    # A contract year of it is the annual charge, give or take the mid-year inflation.
    year_one = sum(p.expenses(t) for t in range(opens(1), anniv(1) + 1))
    assert year_one - 0.06 * 100000.0 == pytest.approx(80.0, rel=0.02)
    assert p.commissions(0) == 0.0                 # folded into the acquisition expense
    assert p.premium_taxes(0) == 0.0               # composite state basis [std]


def test_an_in_force_model_point_pays_no_premium(anchor, fixed_indexed_annuity):
    """Point 1 entered at anniversary 7, so the premium and acquisition cost are behind it."""
    assert all(anchor.premiums(t) == 0.0
               for t in range(anchor.entry_mth(), anchor.proj_len()))
    # Its first row carries maintenance only: the acquisition term keys off premiums(t).
    assert anchor.expenses(84) == pytest.approx(
        80.0 / 12.0 * 1.025 ** 7 * anchor.pols_if(84), abs=CENT)
    issued = fixed_indexed_annuity.Projection[2]
    assert issued.premiums(0) == pytest.approx(100000.0, abs=CENT)
    assert issued.expenses(0) > 0.06 * 100000.0


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(anchor.entry_mth(), anchor.proj_len()))
    assert set(df.columns) == {
        "pols_if", "premiums", "withdrawals", "wd_guar", "wd_excess",
        "income_payments", "claims_death", "claims_lapse", "claims_maturity",
        "commissions", "expenses", "premium_taxes", "net_cf",
    }
    assert df.loc[A8, "wd_guar"] == pytest.approx(
        10144.16 * anchor.pols_if(A8), abs=CENT)


def test_result_cf_annual_sums_the_months_into_contract_years(anchor):
    """One row per contract year, every cash column the total of its twelve months.

    ``pols_if`` is the count opening the year, ``pols_if(12 * duration)``, which is what
    the annual-step model carried on the same row; the cash columns are not that model's,
    because a withdrawal at the anniversary is now weighted by the contracts that reach
    it and claims and expenses fall where they happen.
    """
    monthly, annual = anchor.result_cf(), anchor.result_cf_annual()
    assert annual.index.name == "policy_year"
    assert list(annual.index) == list(range(8, 8 + len(annual)))
    assert len(annual) == len(monthly) // 12
    assert list(annual.columns) == list(monthly.columns)
    for year in (8, 12, 20):
        rows = monthly.loc[opens(year):anniv(year)]
        assert annual.loc[year, "pols_if"] == pytest.approx(
            anchor.pols_if(opens(year)), abs=EXACT)
        for column in ("withdrawals", "claims_death", "expenses", "net_cf"):
            assert annual.loc[year, column] == pytest.approx(
                rows[column].sum(), abs=1e-9), (year, column)
    # The whole-projection totals are the same however the rows are grouped.
    for column in ("withdrawals", "claims_death", "claims_lapse", "expenses", "net_cf"):
        assert annual[column].sum() == pytest.approx(monthly[column].sum(), rel=1e-12)


def test_the_pols_if_column_is_the_weight_on_its_own_row(fixed_indexed_annuity):
    """pols_if(t) opens month t and is the divisor of that row's cash flows.

    The reconciliation the start-of-period convention buys: a cash flow on row ``t``
    divided by its per-contract amount returns the in-force figure printed on the same
    row.  With an end-of-period ``pols_if`` the printed count would be the one *after*
    the decrements, so the column would not reconcile with the row it sits on.
    """
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        df = p.result_cf()
        for t in range(p.entry_mth(), p.proj_len()):
            w = df.loc[t, "pols_if"]
            assert w == pytest.approx(p.pols_if(t), abs=EXACT)
            assert df.loc[t, "withdrawals"] == pytest.approx(
                p.wd_payment_pp(t) * w, abs=1e-9), (point_id, t)
            # The merged first row of a new issue carries the acquisition expense too;
            # premiums(t) is zero on every later row, so the first term drops out there.
            assert df.loc[t, "expenses"] == pytest.approx(
                0.06 * p.premiums(t) + 80.0 / 12.0 * 1.025 ** (t / 12) * w,
                abs=1e-9), (point_id, t)
            if p.phase_open(t) == "DEPLETED" and p.is_anniv(t):
                assert df.loc[t, "income_payments"] == pytest.approx(
                    p.lw_pp_at(t, "BEF_WD") * w, abs=1e-9), (point_id, t)


def test_the_withdrawals_column_is_published_beside_its_three_part_split(anchor):
    """withdrawals is the library-wide column; wd_guar/wd_excess/income_payments split it.

    Published *alongside* the split, not instead of it, so a reader comparing this model
    with the other annuities finds the same column name carrying the same thing.
    """
    df = anchor.result_cf()
    assert "withdrawals" in df.columns
    for column in ("wd_guar", "wd_excess", "income_payments"):
        assert column in df.columns
    total = df["wd_guar"] + df["wd_excess"] + df["income_payments"]
    assert (df["withdrawals"] - total).abs().max() == pytest.approx(0.0, abs=1e-9)
    # The total is the ledger line net_cf is built from, not the sum of every column.
    assert df.loc[A8, "withdrawals"] == pytest.approx(10144.16 * anchor.pols_if(A8),
                                                      abs=CENT)


def test_result_pols_opens_and_closes_each_row(anchor):
    """pols_if opens the row and pols_if_aft_decr closes it, on the monthly rates.

    Both the annual rates and the monthly ones they convert to are published, so a reader
    can see the assumption at the frequency it is set as well as the one it is applied at.
    """
    df = anchor.result_pols()
    assert list(df.columns) == [
        "pols_if", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "pols_death", "pols_lapse", "pols_maturity", "pols_if_aft_decr",
    ]
    for t in range(anchor.entry_mth(), anchor.proj_len() - 1):
        row = df.loc[t]
        assert row["pols_if"] - row["pols_death"] - row["pols_lapse"] == pytest.approx(
            row["pols_if_aft_decr"], abs=1e-12), t
        assert row["pols_if_aft_decr"] == pytest.approx(df.loc[t + 1, "pols_if"],
                                                        abs=1e-12), t


def test_result_tables_are_indexed_consistently(anchor):
    for frame in (anchor.result_cf(), anchor.result_pols(), anchor.result_av(),
                  anchor.result_glwb()):
        assert frame.index.name == "t"
        assert list(frame.index) == list(
            range(anchor.entry_mth(), anchor.proj_len()))


def test_invalid_timing_and_kind_arguments_raise(anchor):
    """Every timing and kind argument rejects an unknown value, as CashValue_SE does."""
    for call in (lambda: anchor.av_pp_at(A8, "BOM"),
                 lambda: anchor.av_fixed_pp_at(A8, "BOM"),
                 lambda: anchor.benefit_base_pp_at(A8, "BOM"),
                 lambda: anchor.lw_pp_at(A8, "BOM"),
                 lambda: anchor.pols_if_at(A8, "BOM"),
                 lambda: anchor.av_at(A8, "BOM")):
        raises_value_error(call, "invalid timing")
    for call in (lambda: anchor.claim_pp(A8, "ANNUITIZATION"),
                 lambda: anchor.claim_from_av_pp(A8, "ANNUITIZATION"),
                 lambda: anchor.pols_decr(A8, "ANNUITIZATION")):
        raises_value_error(call, "invalid kind")


def test_the_timings_the_chassis_shares_still_coincide(anchor):
    """BEF_MORT equals BEF_DECR here: this product has no annuitization decrement."""
    t = anniv(9)
    assert anchor.pols_if_at(t, "BEF_MORT") == anchor.pols_if_at(t, "BEF_DECR")
    assert anchor.pols_if_at(t, "BEF_DECR") == anchor.pols_if(t)
    # ... and AFT_DECR is the closing count, which opens the next month.
    assert anchor.pols_if_at(t, "AFT_DECR") == anchor.pols_if(t + 1)


def test_maturity_is_confined_to_the_horizon(anchor):
    for t in range(anchor.entry_mth(), anchor.proj_len() - 1):
        assert anchor.pols_maturity(t) == 0.0
    # pols_if opens the month, so nothing is left to open the one past the last.
    assert anchor.pols_if(anchor.proj_len()) == 0.0
    assert anchor.pols_if_at(anchor.proj_len() - 1, "AFT_DECR") == 0.0


def test_inforce_is_a_decreasing_probability(fixed_indexed_annuity):
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        for t in range(p.entry_mth(), p.proj_len()):
            assert 0.0 <= p.pols_if(t) <= 1.0, (point_id, t)
            if t > p.entry_mth():
                assert p.pols_if(t) <= p.pols_if(t - 1) + 1e-15, (point_id, t)


def test_the_model_point_table_ships_the_nine_switch_combinations(
        fixed_indexed_annuity):
    """Nine rows, one per switch combination the product supports.

    That each of them projects, publishes a clean frame and stays inside the four GLWB
    phases is asserted in ``test_model_conventions.py`` — once, on one instance, for every
    model in the library. What is left here is the count, which is this product's own
    statement about what the shipped table covers.
    """
    assert len(fixed_indexed_annuity.Data.model_point_table()) == 9


def test_the_model_name_matches_the_product_folder(fixed_indexed_annuity):
    assert fixed_indexed_annuity.name == "FIA_US_S"
    assert MODEL_PATH.parent.name == "fixed_indexed_annuity"


def test_the_grid_is_monthly_and_every_contract_event_is_annual(fixed_indexed_annuity,
                                                               anchor):
    """The ``_S`` suffix, the product assignment table and the grid now all agree.

    The notes' "Projection frequency: annual [std], with the contract anniversary as the
    single event date" describes the *contract*, and it still holds: every transaction
    falls on the anniversary.  The frame around it is monthly, so the anchor projects
    624 rows to attained age 120 rather than 52, and ``result_cf_annual()`` puts the 52
    contract years back.
    """
    assert "monthly" in fixed_indexed_annuity.doc.lower()
    assert "contract year" in fixed_indexed_annuity.Projection.doc
    assert anchor.policy_year(A8) == 8
    assert anchor.duration(A8) == 7
    assert anchor.duration_mth(A8) == A8
    assert anchor.age(A8) == anchor.age_at_entry() + 7
    assert anchor.is_anniv(A8) is True
    assert anchor.is_anniv(A8 - 1) is False
    assert anchor.anniv_mth(A8 - 5) == A8
    assert anchor.year_open_mth(A8) == anchor.entry_mth() - 1
    assert anchor.policy_term() == 120 - 62 + 1
    assert anchor.proj_len() == 12 * (120 - 62 + 1)
    assert len(anchor.result_cf()) == anchor.proj_len() - anchor.entry_mth()
    assert len(anchor.result_cf()) == 624
    assert len(anchor.result_cf_annual()) == 52


def test_mortality_reads_the_age_entering_the_contract_year(anchor):
    """age(t) is the age opening month t's contract year, so q(t) reads it.

    The horizon is the contract year *entered* at the mortality table's terminal age, so
    the last contract year carries q = 1.000000 - hence a monthly rate of 1.0 - and the
    projection closes itself.
    """
    table = anchor.data.mort_table()
    assert anchor.age(A8) == 69                   # entering contract year 8
    assert anchor.exercise_age(A8) == 70          # ... and 70 at its anniversary
    assert anchor.mort_rate(A8) == pytest.approx(
        float(table.loc[(69, "M"), "mort_rate"]), rel=1e-12)
    # The age is a property of the contract year, so it does not move inside one.
    assert all(anchor.age(t) == 69 for t in range(opens(8), A8 + 1))
    assert anchor.age(anchor.proj_len() - 1) == 120
    assert anchor.mort_rate(anchor.proj_len() - 1) == 1.0
    assert anchor.mort_rate_mth(anchor.proj_len() - 1) == 1.0
    assert anchor.pols_maturity(anchor.proj_len() - 1) == 0.0


def test_space_docstrings_carry_their_reference_material(fixed_indexed_annuity):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = fixed_indexed_annuity.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("benefit_base_pp", "lw_pp", "mgsv_pp", "wd_excess_pp",
                  "depletion_cause", "shock_lapse_rate", "wd_unfunded_pp"):
        assert cells in proj
    assert "MGSV" in proj and "MGV" in proj      # the terminology bridge is explained
    # The monthly vocabulary is documented alongside the notes' own symbols.
    for cells in ("duration", "is_anniv", "anniv_mth", "year_open_mth", "entry_mth",
                  "mort_rate_mth", "lapse_rate_mth", "fixed_interest_ann_pp",
                  "av_pp_year_open", "result_cf_annual"):
        assert cells in proj, cells
    # Every notes symbol gets a row, the in-force entry state included: those are the
    # attributes the worked-example anchor cell is driven by.
    for symbol, cells in (("av_initial", "av_pp_init"),
                          ("bb_initial", "benefit_base_pp_init"),
                          ("mgv_initial", "mgsv_pp_init")):
        assert symbol in proj, symbol
        assert cells in proj, cells
    for cells in ("rollup_base_pp_init", "lw_pp_init", "payout_rate_init", "phase_init"):
        assert cells in proj, cells
    data = fixed_indexed_annuity.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "mort_table", "model_point_table", "rollup_table"):
        assert cells in data


def test_model_docstring_names_the_gaps(fixed_indexed_annuity):
    """Anything not implemented must be named, so a gap cannot pass for an oversight."""
    doc = fixed_indexed_annuity.doc
    assert "mechanics demonstration" in doc
    assert "Not implemented" in doc
    for gap in ("monthly-sum", "interim value", "check_margin", "Scale G2"):
        assert gap in doc
    for name in ("Data", "Projection"):
        assert name in doc
