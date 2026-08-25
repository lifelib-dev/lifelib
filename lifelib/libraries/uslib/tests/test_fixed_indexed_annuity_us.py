"""Golden and product-specific tests for FIA_US_S.

The golden values are the worked example in
products/fixed_indexed_annuity/technical-notes.md ("Worked example"), which projects
the anchor cell Male 62 ANB / single life / P = $100,000 / b = 7% / GLWB elected at issue
/ first lifetime withdrawal at anniversary 8 (attained age 70).  They are hard-coded here
rather than pickled so that a reviewer can compare them against the notes by eye.

Model point 1 enters the projection **in force at anniversary 7** on the balances the
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
# technical-notes.md, "Worked example", the sixteen-row table at anniversary 8:
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
    (1, "index return R(8)", lambda p: p.index_return(8), 0.090000, RATE),
    (2, "credit rate cr(8)", lambda p: p.credit_rate(8), 0.052500, RATE),
    (3, "index credit IC(8)", lambda p: p.index_credit_pp(8), 6720.00, CENT),
    (4, "AV after credit", lambda p: p.av_pp_at(8, "BEF_FEE"), 134720.00, CENT),
    (5, "rider charge Phi(8)", lambda p: p.rider_charge_pp(8), 1710.00, CENT),
    (6, "AV(2) after charge", lambda p: p.av_pp_at(8, "BEF_WD"), 133010.00, CENT),
    (7, "guaranteed rollup", lambda p: p.rollup_pp(8), 5000.00, CENT),
    (8, "stacking credit", lambda p: p.stack_pp(8), 10080.00, CENT),
    (9, "BB(3) before step-up",
     lambda p: p.benefit_base_pp_at(8, "BEF_STEP_UP"), 195080.00, CENT),
    (10, "BB(4) after step-up",
     lambda p: p.benefit_base_pp_at(8, "BEF_WD"), 195080.00, CENT),
    (11, "lifetime withdrawal LW(8)",
     lambda p: p.lw_pp_at(8, "BEF_WD"), 10144.16, CENT),
    (12, "free withdrawal amount FW(8)", lambda p: p.free_wd_allow(8), 12800.00, CENT),
    (13, "excess E(8)", lambda p: p.wd_excess_pp(8), 0.00, CENT),
    (14, "account value AV(8)", lambda p: p.av_pp(8), 122865.84, CENT),
    (15, "guaranteed minimum MGV(8)", lambda p: p.mgsv_pp(8), 84605.80, CENT),
    (16, "closing benefit base BB(8)", lambda p: p.benefit_base_pp(8), 195080.00, CENT),
]


@pytest.mark.parametrize(
    "item,label,getter,expected,tol", WORKED_EXAMPLE,
    ids=["%02d %s" % (row[0], row[1]) for row in WORKED_EXAMPLE])
def test_worked_example_row(anchor, item, label, getter, expected, tol):
    """Every row of the notes' sixteen-item table, to the precision it displays."""
    assert getter(anchor) == pytest.approx(expected, abs=tol)


def test_worked_example_opening_state(anchor):
    """The stated in-force position at anniversary 7 that the table is computed from."""
    assert anchor.entry_year() == 7
    assert anchor.av_pp(7) == pytest.approx(128000.00, abs=CENT)
    assert anchor.benefit_base_pp(7) == pytest.approx(180000.00, abs=CENT)
    assert anchor.rollup_base_pp(7) == pytest.approx(100000.00, abs=CENT)
    assert anchor.mgsv_pp(7) == pytest.approx(93811.84, abs=CENT)
    assert anchor.wd_cum_pp(7) == 0.0
    assert anchor.phase(7) == "ACCUM"
    # MGV(7) is 87,500 x 1.01^7, which the notes give as the derivation of 93,811.84.
    assert 0.875 * anchor.premium_pp() * 1.01 ** 7 == pytest.approx(93811.84, abs=CENT)


def test_the_step_up_does_not_bind_on_the_blended_baseline(anchor):
    """Row 10: the stack dominates, so max(195,080.00, 133,010.00) is the base itself."""
    assert anchor.step_up_applies(8) is True
    assert (anchor.benefit_base_pp_at(8, "BEF_WD")
            == anchor.benefit_base_pp_at(8, "BEF_STEP_UP"))
    assert anchor.benefit_base_pp_at(8, "BEF_WD") > anchor.av_pp_at(8, "BEF_WD")


def test_a_guaranteed_withdrawal_leaves_the_guarantee_untouched(anchor):
    """Row 13 and row 16: E(8) = 0, so rho = 0 and BB, LW and RB are unchanged [S9]."""
    assert anchor.wd_pp(8) == pytest.approx(anchor.lw_pp_at(8, "BEF_WD"), abs=EXACT)
    assert anchor.wd_excess_pp(8) == 0.0
    assert anchor.wd_reduction_rate(8) == 0.0
    assert anchor.wd_charge_base_pp(8) == 0.0
    assert anchor.wd_charge_pp(8) == 0.0
    assert anchor.wd_clawback_pp(8) == 0.0
    assert anchor.wd_mva_pp(8) == 0.0
    assert anchor.benefit_base_pp(8) == pytest.approx(195080.00, abs=CENT)
    assert anchor.lw_pp(8) == pytest.approx(10144.16, abs=CENT)
    assert anchor.rollup_base_pp(8) == pytest.approx(100000.00, abs=CENT)


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
    assert anchor.free_wd_allow(8) == pytest.approx(12800.00, abs=CENT)
    assert anchor.wd_free_pp(8) == pytest.approx(10144.16, abs=CENT)
    assert anchor.free_wd_remain(8) == pytest.approx(2655.84, abs=CENT)
    assert anchor.surr_charge_base_pp(8) == pytest.approx(120210.00, abs=CENT)


def test_surrender_trace_charge_clawback_and_mva(anchor):
    """sc(8) = 3% and v(8) = 70% [S5]; the MVA factor to its eight printed decimals."""
    assert anchor.surr_charge_rate(8) == pytest.approx(0.03, abs=RATE)
    assert anchor.vest_rate(8) == pytest.approx(0.70, abs=RATE)
    assert anchor.surr_charge_pp(8) == pytest.approx(3606.30, abs=CENT)
    assert anchor.surr_clawback_pp(8) == pytest.approx(2359.26, abs=CENT)
    assert anchor.mva_term(8) == 2.0                       # n = 24 months
    assert anchor.mva_ref_yield_at_issue() == pytest.approx(0.0300, abs=RATE)
    assert anchor.mva_ref_yield(8) == pytest.approx(0.0350, abs=RATE)
    assert anchor.mva_rate(8) == pytest.approx(-0.00963850, abs=FACTOR)
    assert anchor.mva_pp(8) == pytest.approx(-1158.64, abs=CENT)


def test_surrender_trace_mva_collar_does_not_bind(anchor):
    """The limit max(0, G - SC - CB - MGV) = 32,294.48 [S10], well outside -1,158.64."""
    limit = max(0.0, anchor.av_pp(8) - anchor.surr_charge_pp(8)
                - anchor.surr_clawback_pp(8) - anchor.mgsv_pp(8))
    assert limit == pytest.approx(32294.48, abs=CENT)
    assert abs(anchor.mva_pp(8)) < limit


def test_surrender_trace_net_proceeds_is_a_cent_rounding_artefact(anchor):
    """The notes' 115,741.64 is the sum of the *displayed* cent-rounded components.

    Every component reproduces exactly to the cent, but the clawback (2,359.26168) and
    the MVA (-1,158.64384) each carry fractions of a cent that the notes' displayed
    subtraction drops.  Carried at full precision - which is what the notes' own rounding
    convention asks for, "full precision internally, cents on reported cash flows [std]"
    - the net is 0.55 cents lower.  Both readings are pinned here rather than either
    being tuned away.
    """
    gross = anchor.av_pp(8)
    sc, cb, mva = (anchor.surr_charge_pp(8), anchor.surr_clawback_pp(8),
                   anchor.mva_pp(8))
    from_displayed = round(gross, 2) - round(sc, 2) - round(cb, 2) + round(mva, 2)
    assert from_displayed == pytest.approx(115741.64, abs=CENT)      # the notes' figure
    assert anchor.surr_value_pp(8) == pytest.approx(115741.634475, abs=CENT)
    assert from_displayed - anchor.surr_value_pp(8) == pytest.approx(0.0055, abs=1e-4)
    # The nonforfeiture floor does not bind: CSV = the surrender value, not MGV.
    assert anchor.surr_benefit_pp(8) == pytest.approx(anchor.surr_value_pp(8), abs=EXACT)
    assert anchor.surr_benefit_pp(8) > anchor.mgsv_pp(8)


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
    assert p.benefit_base_pp(7) == pytest.approx(121000.00, abs=CENT)
    assert p.stack_factor() == 0.0
    assert p.rollup_rate(8) == pytest.approx(0.03, abs=RATE)
    assert p.rider_charge_pp(8) == pytest.approx(1149.50, abs=CENT)
    assert p.av_pp_at(8, "BEF_WD") == pytest.approx(133570.50, abs=CENT)
    assert p.rollup_pp(8) == pytest.approx(3000.00, abs=CENT)
    assert p.stack_pp(8) == 0.0
    assert p.benefit_base_pp_at(8, "BEF_STEP_UP") == pytest.approx(124000.00, abs=CENT)
    assert p.benefit_base_pp_at(8, "BEF_WD") == pytest.approx(133570.50, abs=CENT)
    assert p.lw_pp_at(8, "BEF_WD") == pytest.approx(6945.67, abs=CENT)


def test_step_up_binds_in_year_one_on_a_new_issue(fixed_indexed_annuity):
    """The notes' "rarely, not never" case, spelled out in the step 3 commentary.

    "the account-value bonus starts AV(0) = 107,000 above BB(0) = 100,000, so a first
    contract year with a zero index credit gives AV(2)(1) = 106,050 against
    BB(3)(1) = 105,000 and the step-up binds.  Test it at every anniversary rather than
    assuming the stack dominates."
    """
    p = fixed_indexed_annuity.Projection[2]
    assert p.entry_year() == 0
    assert p.av_pp(0) == pytest.approx(107000.00, abs=CENT)     # P x (1 + b) [S5]
    assert p.benefit_base_pp(0) == pytest.approx(100000.00, abs=CENT)   # bonus excluded
    assert p.rollup_base_pp(0) == pytest.approx(100000.00, abs=CENT)
    assert p.mgsv_pp(0) == pytest.approx(87500.00, abs=CENT)    # 0.875 x P, no bonus
    assert p.index_credit_pp(1) == 0.0
    assert p.rider_charge_pp(1) == pytest.approx(950.00, abs=CENT)
    assert p.av_pp_at(1, "BEF_WD") == pytest.approx(106050.00, abs=CENT)
    assert p.benefit_base_pp_at(1, "BEF_STEP_UP") == pytest.approx(105000.00, abs=CENT)
    assert p.benefit_base_pp(1) == pytest.approx(106050.00, abs=CENT)   # the step-up
    # ... and the same cell rolled forward seven years reaches the notes' MGV(7).
    assert p.mgsv_pp(7) == pytest.approx(93811.84, abs=CENT)


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
    """LW + Phi = 10,144.16 + 1,853.26, constant because the base stops growing."""
    drain = anchor.lw_pp(8) + 0.0095 * anchor.benefit_base_pp(8)
    assert drain == pytest.approx(11997.42, abs=CENT)
    for t in range(9, 19):
        assert anchor.index_credit_pp(t) == 0.0
        assert anchor.rider_charge_pp(t) == pytest.approx(1853.26, abs=CENT)
        assert anchor.wd_pp(t) == pytest.approx(10144.16, abs=CENT)
        assert (anchor.av_pp(t - 1) - anchor.av_pp(t)) == pytest.approx(11997.42,
                                                                       abs=CENT)


def test_the_account_value_is_exhausted_during_contract_year_19(anchor):
    """At attained age 81, and the phase is DEPLETED - not TERMINATED."""
    assert anchor.av_pp(18) > 0.0
    assert anchor.av_pp(18) == pytest.approx(2891.64, abs=CENT)
    assert anchor.av_pp(19) == 0.0
    assert anchor.age(19) == 81
    assert anchor.phase(18) == "INCOME"
    assert anchor.phase(19) == "DEPLETED"
    assert anchor.depletion_cause(19) is False
    # The insurer funds the shortfall in the depletion year itself.
    assert anchor.av_depletion_pp(19) == pytest.approx(
        10144.16 - anchor.av_pp_at(19, "BEF_WD"), abs=CENT)


def test_the_income_stream_survives_exhaustion(anchor):
    """The guarantee: LW a year for life, from the insurer's own funds [S1][S3][S9]."""
    for t in range(20, 31):
        assert anchor.phase(t) == "DEPLETED"
        assert anchor.av_pp(t) == 0.0
        assert anchor.wd_pp(t) == pytest.approx(10144.16, abs=CENT)
        assert anchor.rider_charge_pp(t) == 0.0        # nothing to deduct it from [S9]
        assert anchor.index_credit_pp(t) == 0.0        # steps 1-3 are skipped
        assert anchor.lapse_rate(t) == 0.0             # lapse is impossible [S1][S9]
        assert anchor.claim_pp(t, "DEATH") == 0.0      # no death benefit
        assert anchor.surr_benefit_pp(t) == 0.0        # no surrender value
        assert anchor.income_payments(t) == pytest.approx(
            10144.16 * anchor.pols_if(t), abs=CENT)      # pols_if(t) opens the year
        assert anchor.wd_guar(t) == 0.0                # reported on the income line only


def test_income_runs_to_the_end_of_the_projection(anchor):
    """Nothing but death exits the depleted state, so the payment runs to the horizon."""
    assert anchor.phase(anchor.proj_len()) == "DEPLETED"
    assert anchor.pols_if(anchor.proj_len() - 1) > 0.0
    assert sum(anchor.income_payments(t)
               for t in range(20, anchor.proj_len() + 1)) > 0.0


# ---------------------------------------------------------------------------
# One test per entry in the notes' "Known modeling pitfalls" list.
# ---------------------------------------------------------------------------

def test_pitfall_the_floor_is_on_the_credit_not_the_account_value(fixed_indexed_annuity):
    """"Rider charges and strategy fees can exceed interest credited" [S7].

    Flooring the account value at its prior balance silently removes the charge drag
    that produces depletion.  Model point 2 has a zero index credit in year 1 and a $950
    rider charge, so the account value must *fall*.
    """
    p = fixed_indexed_annuity.Projection[2]
    assert p.credit_rate(1) == 0.0                       # the credit is floored at zero
    assert p.credit_rate_on(-0.30, "cap") == 0.0         # ... however bad the index year
    assert p.av_pp(1) < p.av_pp(0)                       # ... the account value is not


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
    for t in range(8, 9):
        assert p.rollup_pp(t) == pytest.approx(0.05 * p.rollup_base_pp(t - 1), abs=CENT)
    assert p.rollup_pp(8) == pytest.approx(5000.00, abs=CENT)
    assert p.rollup_base_pp(7) == pytest.approx(100000.00, abs=CENT)
    # Simple interest on the *grown* base would have been 0.05 x 180,000 = 9,000.
    assert p.rollup_pp(8) != pytest.approx(0.05 * p.benefit_base_pp(7), abs=1.0)


def test_pitfall_attribution_at_depletion(fixed_indexed_annuity, anchor):
    """"a model testing only AV <= 0 will either give the guarantee away ... or destroy it".

    Point 1 withdraws exactly LW and reaches DEPLETED with the income intact.  Point 7 is
    the identical cell overdrawing at 105% of the maximum, so every year carries an excess
    withdrawal, depletion_cause is set and the same exhaustion TERMINATES the contract.
    """
    p7 = fixed_indexed_annuity.Projection[7]
    assert p7.utilization_intensity() == 1.05
    assert p7.wd_excess_pp(8) > 0.0
    assert p7.depletion_cause(8) is True
    assert anchor.depletion_cause(8) is False

    terminated = [t for t in range(8, p7.proj_len() + 1) if p7.phase(t) == "TERMINATED"]
    depleted = [t for t in range(8, anchor.proj_len() + 1)
                if anchor.phase(t) == "DEPLETED"]
    assert terminated and depleted
    assert p7.av_pp(terminated[0]) == 0.0
    assert anchor.av_pp(depleted[0]) == 0.0
    # Same exhaustion, opposite outcome: the guarantee survives on one and not the other.
    # pols_if opens the contract year, so the deemed full surrender shows up as a zero
    # opening count in the year *after* the one that terminates.
    assert p7.pols_if(terminated[0]) > 0.0
    assert p7.pols_if(terminated[0] + 1) == 0.0
    assert p7.pols_if_at(terminated[0], "AFT_DECR") == 0.0
    assert anchor.pols_if(depleted[0]) > 0.0
    assert all(p7.income_payments(t) == 0.0 for t in range(8, p7.proj_len() + 1))
    assert sum(anchor.income_payments(t)
               for t in range(8, anchor.proj_len() + 1)) > 0.0


def test_the_terminating_branch_pays_only_what_the_account_value_holds(
        fixed_indexed_annuity, anchor):
    """The attribution has to reach the cash, not only the phase label.

    Points 1 and 7 exhaust at the same anniversary and the notes send them opposite ways.
    On the DEPLETED branch the insurer funds the whole shortfall from its own funds -
    that stream is the guarantee.  On the TERMINATED branch it funds none of it: the
    balance is gone and the rider that would have covered the rest was destroyed by the
    very withdrawal being paid, [S5] treating the contract "as well as the rider" as
    Surrendered at that point.  Paying the request in full on both branches would honour
    the guarantee in the year the excess withdrawal kills it - the same failure the
    attribution test exists to prevent, one step further downstream.
    """
    p7 = fixed_indexed_annuity.Projection[7]
    assert p7.phase(18) == "INCOME"
    assert p7.phase(19) == "TERMINATED"

    # What the contract could meet, against what was asked for.
    assert p7.av_pp_at(19, "BEF_WD") == pytest.approx(765.92, abs=CENT)
    assert p7.wd_pp(19) == pytest.approx(7856.61, abs=CENT)
    assert p7.lw_pp_at(19, "BEF_WD") == pytest.approx(7482.49, abs=CENT)
    assert p7.wd_excess_pp(19) == pytest.approx(374.12, abs=CENT)
    assert p7.av_depletion_pp(19) == pytest.approx(7090.69, abs=CENT)

    # None of that shortfall is payable, so the cash is the balance and nothing more.
    assert p7.wd_unfunded_pp(19) == pytest.approx(7090.69, abs=CENT)
    assert p7.wd_payment_pp(19) == pytest.approx(765.92, abs=CENT)
    assert p7.withdrawals(19) == pytest.approx(
        765.92 * p7.pols_if(19), abs=CENT)
    # The excess goes unpaid first and the guaranteed portion only after it [S9], [std].
    assert p7.wd_excess_paid_pp(19) == 0.0
    assert p7.wd_guar_paid_pp(19) == pytest.approx(765.92, abs=CENT)
    assert p7.wd_excess(19) == 0.0
    assert p7.wd_guar(19) == pytest.approx(p7.withdrawals(19), abs=EXACT)
    # ... and nothing at all is paid once the contract has terminated.
    assert all(p7.withdrawals(t) == 0.0 for t in range(20, p7.proj_len() + 1))

    # The cap is on the payment, not on the withdrawal: the guarantee is still destroyed.
    assert p7.depletion_cause(19) is True
    assert p7.wd_reduction_rate(19) == 1.0
    assert p7.benefit_base_pp(19) == 0.0

    # The contrast, at the same anniversary: on the DEPLETED branch it IS all paid.
    assert anchor.phase(19) == "DEPLETED"
    assert anchor.av_pp_at(19, "BEF_WD") == pytest.approx(1038.38, abs=CENT)
    assert anchor.av_depletion_pp(19) == pytest.approx(9105.78, abs=CENT)
    assert anchor.wd_unfunded_pp(19) == 0.0
    assert anchor.wd_payment_pp(19) == pytest.approx(10144.16, abs=CENT)


def test_pitfall_an_overdraw_permanently_reduces_the_guarantee(fixed_indexed_annuity,
                                                               anchor):
    """"a 5% overdraw permanently reduces the guarantee" - efficiency is not free [R1]."""
    p7 = fixed_indexed_annuity.Projection[7]
    assert p7.lw_pp_at(8, "BEF_WD") == pytest.approx(10144.16, abs=CENT)
    assert p7.wd_pp(8) == pytest.approx(1.05 * 10144.16, abs=CENT)
    assert p7.wd_excess_pp(8) == pytest.approx(0.05 * 10144.16, abs=CENT)
    rho = p7.wd_reduction_rate(8)
    assert rho > 0.0
    assert p7.benefit_base_pp(8) == pytest.approx(195080.00 * (1 - rho), abs=CENT)
    assert p7.benefit_base_pp(8) < anchor.benefit_base_pp(8)
    assert p7.lw_pp(8) < anchor.lw_pp(8)
    assert p7.rollup_base_pp(8) == pytest.approx(100000.00 * (1 - rho), abs=CENT)


def test_pitfall_no_lapse_in_depleted(anchor):
    """"Leaving the surrender decrement on silently truncates the ... liability."""
    depleted = [t for t in range(8, anchor.proj_len()) if anchor.phase(t) == "DEPLETED"]
    assert depleted
    for t in depleted:
        assert anchor.lapse_rate(t) == 0.0
        assert anchor.pols_lapse(t) == 0.0
        # only mortality exits: the count closing year t is the one opening it, less deaths
        assert anchor.pols_if(t + 1) == pytest.approx(
            anchor.pols_if(t) * (1 - anchor.mort_rate(t)), rel=1e-12)
        assert anchor.pols_if_at(t, "AFT_DECR") == pytest.approx(
            anchor.pols_if(t + 1), rel=1e-12)


def test_pitfall_rider_charge_base_and_ordering(anchor):
    """"The charge is on the benefit base ... and is taken after index credits" [S9].

    "In the worked example the benefit base closes at 1.59x the account value at
    anniversary 8 (195,080.00 against 122,865.84), so charging on the account value
    understates the deduction by a growing margin."
    """
    assert anchor.rider_charge_pp(8) == pytest.approx(0.0095 * 180000.00, abs=CENT)
    # ... on the OPENING base, because the base is updated after the charge.
    assert anchor.rider_charge_pp(8) == pytest.approx(
        0.0095 * anchor.benefit_base_pp(7), abs=CENT)
    # ... and after the index credit: the charge lands on AV(1), not on AV(t-1).
    assert anchor.av_pp_at(8, "BEF_WD") == pytest.approx(
        anchor.av_pp_at(8, "BEF_FEE") - anchor.rider_charge_pp(8), abs=EXACT)
    assert anchor.av_pp_at(8, "BEF_FEE") > anchor.av_pp_at(8, "BEF_INV")
    ratio = anchor.benefit_base_pp(8) / anchor.av_pp(8)
    assert ratio == pytest.approx(1.59, abs=0.005)
    # Charging on the account value would understate the deduction.
    assert 0.0095 * anchor.av_pp_at(8, "BEF_FEE") < anchor.rider_charge_pp(8)


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
    assert anchor.mva_rate(8) < 0.0
    # Only inside the ten-year MVA period.
    assert anchor.mva_in_force(9) is True
    assert anchor.mva_term(10) == 0.0
    assert anchor.mva_in_force(10) is False
    assert anchor.mva_rate(10) == 0.0
    assert anchor.mva_pp(11) == 0.0
    # Never on the death benefit: it is max(AV, MGV), with no charge and no adjustment.
    assert anchor.claim_pp(9, "DEATH") == pytest.approx(
        max(anchor.av_pp(9), anchor.mgsv_pp(9)), abs=EXACT)
    assert anchor.claim_pp(9, "DEATH") > anchor.claim_pp(9, "LAPSE")
    # Never below the nonforfeiture minimum: the collar and then the floor.
    for t in range(8, 12):
        assert anchor.surr_benefit_pp(t) >= anchor.mgsv_pp(t) - EXACT
    # The ratio form is naturally bounded; a rate rise cannot make it explode.
    assert anchor.mva_rate(8) > -0.02


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
    base, small = anchor.surr_charge_base_pp(8), 20000.0
    # Same input, two readings, on the withdrawal path.
    assert anchor.mva_pp_on(8, base, small) == 0.0                    # "gross", default
    model = mx.read_model(MODEL_PATH, name="FIA_collar")
    try:
        model.Projection.mva_collar_basis = "surrender_value"
        alt = model.Projection[1]
        assert alt.mva_pp_on(8, base, small) == pytest.approx(-1158.64, abs=CENT)
        # ... but the worked example's surrender trace is invariant, because G = AV there.
        assert alt.mva_pp(8) == pytest.approx(anchor.mva_pp(8), abs=1e-9)
        assert alt.surr_value_pp(8) == pytest.approx(anchor.surr_value_pp(8), abs=1e-9)
    finally:
        model.close()


def test_pitfall_monthly_sum_is_not_implemented(anchor):
    """The notes call the monthly-sum floor convention ambiguous and exclude the grid.

    Every implemented method is reachable; the unimplemented one raises rather than
    silently returning something plausible.
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
        assert p.credit_rate(8) == pytest.approx(0.0525, abs=RATE)
        assert p.credit_rate_on(anchor.index_return(8) / 3.0, "cap") == pytest.approx(
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
        assert g.credit_rate(8) == pytest.approx(0.0025, abs=RATE)
        assert g.av_pp(8) < anchor.av_pp(8)
    finally:
        model.close()


def test_the_surrender_charge_and_vesting_schedules(anchor):
    """9.1% grading to 0% and 0% grading to 100% over eleven contract years [S5]."""
    expected_sc = [0.091, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.0]
    expected_v = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for t, (sc, v) in enumerate(zip(expected_sc, expected_v), start=1):
        assert anchor.surr_charge_rate(t) == pytest.approx(sc, abs=RATE)
        assert anchor.vest_rate(t) == pytest.approx(v, abs=RATE)
    assert anchor.surr_charge_rate(25) == 0.0        # the last row holds
    assert anchor.vest_rate(25) == 1.0


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
    assert anchor.is_exercise(8) is True
    assert anchor.age(8) == 70
    assert anchor.payout_rate_locked(8) == pytest.approx(0.052, abs=RATE)
    for t in range(9, 25):
        assert anchor.is_exercise(t) is False
        assert anchor.payout_rate_locked(t) == pytest.approx(0.052, abs=RATE)
    # The 80+ band is never re-read even though the annuitant passes 80 at t = 18.
    assert anchor.age(18) == 80
    assert anchor.payout_rate(80, "single") == pytest.approx(0.057, abs=RATE)
    assert anchor.payout_rate_locked(18) == pytest.approx(0.052, abs=RATE)


def test_the_joint_basis_reads_the_younger_life(fixed_indexed_annuity):
    """joint = single - 0.50%, on the younger covered person [S1][S3]."""
    p = fixed_indexed_annuity.Projection[5]
    assert p.glwb_basis() == "joint"
    assert p.joint_age() == 60
    assert p.age_at_entry() == 62
    exercise = [t for t in range(1, 40) if p.is_exercise(t)]
    assert exercise == [10]                      # the younger life reaches 70 at t = 10
    assert p.covered_age(10) == 70
    assert p.age(10) == 72                       # the annuitant is already 72
    assert p.payout_rate_locked(10) == pytest.approx(0.047, abs=RATE)


def test_income_never_decreases_after_exercise(fixed_indexed_annuity):
    """"After exercise the ratchet still applies ... so income never decreases" [S3]."""
    p = fixed_indexed_annuity.Projection[5]
    started = [t for t in range(1, p.proj_len() + 1) if p.phase(t) == "INCOME"]
    for t in started[1:]:
        assert p.lw_pp_at(t, "BEF_WD") >= p.lw_pp(t - 1) - EXACT


def test_benefit_base_growth_stops_at_the_first_lifetime_withdrawal(anchor):
    """T_g = min(first lifetime withdrawal, contract year 20) [S1][S2].

    The exercise anniversary is still inside the window - the worked example credits both
    the rollup and the stack at t = 8 - and every later one is outside it.
    """
    assert anchor.in_growth_period(8) is True
    assert anchor.rollup_pp(8) > 0.0
    assert anchor.stack_pp(8) > 0.0
    for t in range(9, 21):
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
    assert q.is_exercise(23) is True              # after the window, not before it
    assert q.in_growth_period(20) is True
    assert q.in_growth_period(21) is False
    assert q.rollup_pp(21) == 0.0
    assert q.stack_pp(21) == 0.0
    frozen = q.benefit_base_pp(20)
    for t in range(21, 24):
        assert q.benefit_base_pp(t) == pytest.approx(frozen, abs=CENT)
    # A model point with no rider has nothing to grow at all.
    p = fixed_indexed_annuity.Projection[6]
    assert p.glwb_elected() is False
    assert p.in_growth_period(20) is False


def test_the_rollup_schedule_steps_down_in_year_eleven(fixed_indexed_annuity):
    """5.00% in contract years 1-10, 2.00% in 11-20, zero after [S2]."""
    q = fixed_indexed_annuity.Projection[9]
    assert q.rollup_id() == "blended"
    for t in (1, 5, 10):
        assert q.rollup_rate(t) == pytest.approx(0.0500, abs=RATE)
    for t in (11, 15, 20):
        assert q.rollup_rate(t) == pytest.approx(0.0200, abs=RATE)
    for t in (21, 30):
        assert q.rollup_rate(t) == 0.0
    assert q.rollup_pp(20) == pytest.approx(0.02 * q.rollup_base_pp(19), abs=CENT)
    # The Nassau schedule is a flat 3% over fifteen anniversaries instead [S9].
    p = fixed_indexed_annuity.Projection[3]
    assert p.rollup_id() == "nassau"
    assert p.rollup_rate(1) == pytest.approx(0.03, abs=RATE)
    assert p.rollup_rate(15) == pytest.approx(0.03, abs=RATE)
    assert p.rollup_rate(16) == 0.0


def test_the_payout_percentage_locks_in_the_80_plus_band(fixed_indexed_annuity):
    """The [std] extension of [S3]'s single "80" row, reached by a late exerciser."""
    q = fixed_indexed_annuity.Projection[9]
    assert q.age(23) == 85
    assert q.payout_rate_locked(23) == pytest.approx(0.0570, abs=RATE)
    assert q.lw_pp_at(23, "BEF_WD") == pytest.approx(
        0.0570 * q.benefit_base_pp_at(23, "BEF_WD"), abs=CENT)


def test_the_shock_lapse_is_suppressed_by_the_rider(fixed_indexed_annuity, anchor):
    """33% without a rider, 10% with one idle, 5% once activated [R8], all [std].

    "Applying a plain fixed-deferred shock lapse to a rider-in-force FIA is the most
    consequential error available here."
    """
    shock_year = anchor.surr_charge_period + 1
    assert shock_year == 11
    no_rider = fixed_indexed_annuity.Projection[6]
    idle = fixed_indexed_annuity.Projection[9]
    assert no_rider.glwb_elected() is False
    assert no_rider.shock_lapse_rate(shock_year) == pytest.approx(0.33, abs=RATE)
    assert idle.phase_open(shock_year) == "ACCUM"           # rider in force, not activated
    assert idle.rider_in_force(shock_year - 1) is True
    assert idle.shock_lapse_rate(shock_year) == pytest.approx(0.10, abs=RATE)
    assert anchor.phase_open(shock_year) == "INCOME"        # activated
    assert anchor.shock_lapse_rate(shock_year) == pytest.approx(0.05, abs=RATE)
    assert no_rider.lapse_rate_base(shock_year) == pytest.approx(0.33, abs=RATE)


def test_the_base_surrender_shape(fixed_indexed_annuity):
    """Low early, rising through the charge period, spiking at expiry, then elevated."""
    p = fixed_indexed_annuity.Projection[6]        # no rider, so no moneyness damping
    expected = {1: 0.02, 3: 0.02, 4: 0.03, 6: 0.03, 7: 0.04, 9: 0.04,
                10: 0.05, 11: 0.33, 12: 0.06, 30: 0.06}
    for t, rate in expected.items():
        assert p.lapse_rate_base(t) == pytest.approx(rate, abs=RATE)
        assert p.lapse_moneyness_factor(t) == 1.0
        assert p.lapse_rate(t) == pytest.approx(min(0.35, rate), abs=RATE)


def test_the_moneyness_multiplier_suppresses_surrender(anchor):
    """M_money = clamp(1 - 0.6 max(0, BB/AV - 1), 0.2, 1.0) [std]; and the cap at 35%."""
    ratio = anchor.benefit_base_pp(11) / anchor.av_pp(11)
    assert ratio > 1.0
    assert anchor.lapse_moneyness_factor(11) == pytest.approx(
        max(0.2, 1.0 - 0.6 * (ratio - 1.0)), abs=1e-12)
    assert 0.2 <= anchor.lapse_moneyness_factor(11) <= 1.0
    for t in range(8, anchor.proj_len()):
        assert 0.2 <= anchor.lapse_moneyness_factor(t) <= 1.0
        assert anchor.lapse_rate(t) <= anchor.lapse_rate_max


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
    assert anchor.is_exercise(8) is True
    assert anchor.age(8) == 70


def test_exercise_is_barred_below_the_contractual_minimum_age(fixed_indexed_annuity):
    """The minimum age for lifetime withdrawals is 50 [S2][S3][S9]."""
    p = fixed_indexed_annuity.Projection[2]
    assert p.min_income_age == 50
    for t in range(1, 8):
        assert p.is_exercise(t) is False
        assert p.lw_pp(t) == 0.0
        assert p.wd_pp(t) == 0.0


# ---------------------------------------------------------------------------
# The pre-exercise withdrawal path.
# ---------------------------------------------------------------------------

def test_a_pre_exercise_withdrawal_charges_on_the_gross_amount(fixed_indexed_annuity):
    """Before exercise X = max(0, G - FW) and rho = G / AV(2) [S1][S3][S5][S9]."""
    p = fixed_indexed_annuity.Projection[8]
    assert p.wd_pp(3) == pytest.approx(60000.00, abs=CENT)
    assert p.phase_open(3) == "ACCUM"
    assert p.lw_pp_at(3, "BEF_WD") == 0.0
    assert p.wd_excess_pp(3) == pytest.approx(60000.00, abs=CENT)   # LW = 0, all excess
    assert p.free_wd_allow(3) == pytest.approx(0.10 * p.av_pp(2), abs=CENT)
    assert p.wd_charge_base_pp(3) == pytest.approx(
        60000.00 - p.free_wd_allow(3), abs=CENT)
    assert p.wd_charge_pp(3) == pytest.approx(
        0.08 * p.wd_charge_base_pp(3), abs=CENT)                    # sc(3) = 8%
    assert p.wd_clawback_pp(3) == pytest.approx(
        0.80 * (0.07 / 1.07) * p.wd_charge_base_pp(3), abs=CENT)    # v(3) = 20%
    assert p.wd_mva_pp(3) < 0.0                                     # the yield has risen
    assert p.wd_reduction_rate(3) == pytest.approx(
        60000.00 / p.av_pp_at(3, "BEF_WD"), rel=1e-12)
    assert p.benefit_base_pp(3) == pytest.approx(
        p.benefit_base_pp_at(3, "BEF_WD") * (1 - p.wd_reduction_rate(3)), abs=CENT)
    assert p.rollup_base_pp(3) == pytest.approx(
        100000.00 * (1 - p.wd_reduction_rate(3)), abs=CENT)
    assert p.depletion_cause(3) is True                             # charge and MVA bit


def test_the_model_point_provenance_names_the_schedule_it_points_at(
        fixed_indexed_annuity):
    """A shipped input file must describe the input it actually points at.

    Point 8's ``wd_schedule_id`` is ``preexercise``, whose one row is $60,000 - the same
    figure the README quotes and the projection returns.  The $20,000 in this README's
    MVA-collar illustration is a different number for a different purpose and must not
    leak into the model point's own provenance.
    """
    mp = fixed_indexed_annuity.Data.model_point_table()
    wd = fixed_indexed_annuity.Data.withdrawal_table()
    p = fixed_indexed_annuity.Projection[8]
    assert mp.loc[8, "wd_schedule_id"] == "preexercise"
    amount = float(wd.loc[("preexercise", 3), "wd_amount"])
    assert amount == pytest.approx(60000.00, abs=CENT)
    assert p.wd_pp(3) == pytest.approx(amount, abs=CENT)
    provenance = mp.loc[8, "provenance"]
    assert "$60,000" in provenance
    assert "$20,000" not in provenance


def test_the_free_withdrawal_amount_does_not_carry_forward(fixed_indexed_annuity):
    """10% of the *prior* anniversary account value each year, no carry-forward [S9][S10]."""
    p = fixed_indexed_annuity.Projection[8]
    for t in range(1, 10):
        assert p.free_wd_allow(t) == pytest.approx(0.10 * p.av_pp(t - 1), abs=CENT)
    assert p.free_wd_allow(4) < p.free_wd_allow(3)   # the year-3 withdrawal shrank it


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
        for t in range(p.entry_year() + 1, p.proj_len() + 1):
            assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12), (
                point_id, t)


def test_account_value_rollforward_closes(fixed_indexed_annuity):
    """The account value roll-forward closes on every model point, including at depletion."""
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        assert p.check_av_roll_fwd() is True, point_id
        for t in range(p.entry_year() + 1, p.proj_len() + 1):
            assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6), (
                point_id, t)


def test_the_two_accounts_sum_to_the_account_value(fixed_indexed_annuity):
    """AV = F + A at every timing, which is what makes av_indexed_pp a derived quantity."""
    p = fixed_indexed_annuity.Projection[4]        # 80/20 indexed/fixed
    assert p.alloc_fixed() == pytest.approx(0.20, abs=1e-12)
    assert p.av_fixed_pp(0) == pytest.approx(0.20 * 107000.0, abs=CENT)
    assert p.fixed_interest_pp(1) == pytest.approx(0.20 * 107000.0 * 0.023, abs=CENT)
    for t in range(0, p.proj_len() + 1):
        for timing in ("BEF_INV", "BEF_FEE", "BEF_WD", "EOY"):
            assert (p.av_fixed_pp_at(t, timing) + p.av_indexed_pp_at(t, timing)
                    == pytest.approx(p.av_pp_at(t, timing), abs=1e-6)), (t, timing)


def test_the_stack_uses_the_gross_index_credit_not_the_starved_one(
        fixed_indexed_annuity):
    """Design (b): 250% reaches the benefit base while kappa sends 50% to the AV [S3][S4]."""
    p = fixed_indexed_annuity.Projection[4]
    assert p.av_int_factor() == 0.50
    assert p.stack_factor() == 2.50
    assert p.rollup_rate(1) == 0.0                 # pure stacking: g = 0
    assert p.rollup_pp(1) == 0.0
    ic, fi = p.index_credit_pp(1), p.fixed_interest_pp(1)
    assert p.stack_pp(1) == pytest.approx(2.50 * (ic + fi), abs=CENT)
    assert p.inv_income_pp(1) == pytest.approx(0.50 * ic + fi, abs=CENT)


def test_withdrawals_partition_into_the_three_ledger_lines(fixed_indexed_annuity):
    """withdrawals = guaranteed + excess + post-depletion income, at every anniversary."""
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        for t in range(p.entry_year(), p.proj_len() + 1):
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
    assert anchor.rider_charge_pp(8) > 0.0        # it exists, it just is not a ledger line
    assert anchor.net_cf(8) == pytest.approx(
        anchor.premiums(8) - anchor.withdrawals(8) - anchor.claims(8)
        - anchor.commissions(8) - anchor.expenses(8) - anchor.premium_taxes(8),
        abs=EXACT)


def test_expenses_follow_the_notes_ledger(fixed_indexed_annuity):
    """6.0% of premium at issue and $80 a year inflating at 2.5%, both [std]."""
    p = fixed_indexed_annuity.Projection[2]
    assert p.expenses(0) == pytest.approx(0.06 * 100000.0, abs=CENT)
    assert p.expenses(1) == pytest.approx(80.0 * p.pols_if(1), abs=CENT)
    assert p.expenses(5) == pytest.approx(
        80.0 * 1.025 ** 4 * p.pols_if(5), abs=CENT)
    assert p.commissions(0) == 0.0                 # folded into the acquisition expense
    assert p.premium_taxes(0) == 0.0               # composite state basis [std]


def test_an_in_force_model_point_pays_no_premium(anchor, fixed_indexed_annuity):
    """Point 1 entered at anniversary 7, so the premium and acquisition cost are behind it."""
    assert all(anchor.premiums(t) == 0.0
               for t in range(anchor.entry_year(), anchor.proj_len() + 1))
    assert anchor.expenses(7) == 0.0
    issued = fixed_indexed_annuity.Projection[2]
    assert issued.premiums(0) == pytest.approx(100000.0, abs=CENT)
    assert issued.expenses(0) > 0.0


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(anchor.entry_year(), anchor.proj_len() + 1))
    assert set(df.columns) == {
        "pols_if", "premiums", "withdrawals", "wd_guar", "wd_excess",
        "income_payments", "claims_death", "claims_lapse", "claims_maturity",
        "commissions", "expenses", "premium_taxes", "net_cf",
    }
    assert df.loc[8, "wd_guar"] == pytest.approx(
        10144.16 * anchor.pols_if(8), abs=CENT)


def test_the_pols_if_column_is_the_weight_on_its_own_row(fixed_indexed_annuity):
    """pols_if(t) opens contract year t and is the divisor of that row's cash flows.

    The reconciliation the start-of-period convention buys: a cash flow on row ``t``
    divided by its per-contract amount returns the in-force figure printed on the same
    row.  With an end-of-period ``pols_if`` the printed count would be the one *after*
    the decrements, so the column would not reconcile with the row it sits on.
    """
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        df = p.result_cf()
        for t in range(p.entry_year() + 1, p.proj_len() + 1):
            w = df.loc[t, "pols_if"]
            assert w == pytest.approx(p.pols_if(t), abs=EXACT)
            assert df.loc[t, "withdrawals"] == pytest.approx(
                p.wd_payment_pp(t) * w, abs=1e-9), (point_id, t)
            assert df.loc[t, "expenses"] == pytest.approx(
                80.0 * 1.025 ** (t - 1) * w, abs=1e-9), (point_id, t)
            if p.phase_open(t) == "DEPLETED":
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
    assert df.loc[8, "withdrawals"] == pytest.approx(10144.16 * anchor.pols_if(8),
                                                     abs=CENT)


def test_result_pols_opens_and_closes_each_row(anchor):
    """pols_if opens the contract year and pols_if_aft_decr - the notes' l(t) - closes it."""
    df = anchor.result_pols()
    assert list(df.columns) == [
        "pols_if", "mort_rate", "lapse_rate", "pols_death", "pols_lapse",
        "pols_maturity", "pols_if_aft_decr",
    ]
    for t in range(anchor.entry_year() + 1, anchor.proj_len()):
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
            range(anchor.entry_year(), anchor.proj_len() + 1))


def test_invalid_timing_and_kind_arguments_raise(anchor):
    """Every timing and kind argument rejects an unknown value, as CashValue_SE does."""
    for call in (lambda: anchor.av_pp_at(8, "BOM"),
                 lambda: anchor.av_fixed_pp_at(8, "BOM"),
                 lambda: anchor.benefit_base_pp_at(8, "BOM"),
                 lambda: anchor.lw_pp_at(8, "BOM"),
                 lambda: anchor.pols_if_at(8, "BOM"),
                 lambda: anchor.av_at(8, "BOM")):
        raises_value_error(call, "invalid timing")
    for call in (lambda: anchor.claim_pp(9, "ANNUITIZATION"),
                 lambda: anchor.claim_from_av_pp(9, "ANNUITIZATION"),
                 lambda: anchor.pols_decr(9, "ANNUITIZATION")):
        raises_value_error(call, "invalid kind")


def test_the_timings_the_chassis_shares_still_coincide(anchor):
    """BEF_MORT equals BEF_DECR here: this product has no annuitization decrement."""
    assert anchor.pols_if_at(9, "BEF_MORT") == anchor.pols_if_at(9, "BEF_DECR")
    assert anchor.pols_if_at(9, "BEF_DECR") == anchor.pols_if(9)
    # ... and AFT_DECR is the notes' l(t), which opens the next contract year.
    assert anchor.pols_if_at(9, "AFT_DECR") == anchor.pols_if(10)


def test_maturity_is_confined_to_the_horizon(anchor):
    for t in range(anchor.entry_year() + 1, anchor.proj_len()):
        assert anchor.pols_maturity(t) == 0.0
    # pols_if opens the contract year, so nothing is left to open the year past the last.
    assert anchor.pols_if(anchor.proj_len() + 1) == 0.0
    assert anchor.pols_if_at(anchor.proj_len(), "AFT_DECR") == 0.0


def test_inforce_is_a_decreasing_probability(fixed_indexed_annuity):
    for point_id in fixed_indexed_annuity.Data.model_point_table().index:
        p = fixed_indexed_annuity.Projection[point_id]
        for t in range(p.entry_year(), p.proj_len() + 1):
            assert 0.0 <= p.pols_if(t) <= 1.0, (point_id, t)
            if t > p.entry_year():
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


def test_the_grid_is_annual_as_the_notes_state(fixed_indexed_annuity, anchor):
    """The product table records this product as monthly; the notes say annual.

    "Projection frequency: annual [std], with the contract anniversary as the single
    event date."  The docstrings must say so, and t must count contract years: the anchor
    projects 52 rows to attained age 120, not 624.
    """
    assert "annual" in fixed_indexed_annuity.doc.lower()
    assert "contract year" in fixed_indexed_annuity.Projection.doc
    assert anchor.policy_year(8) == 8
    assert anchor.age(8) == anchor.age_at_entry() + 8
    assert anchor.proj_len() == 120 - 62 + 1
    assert len(anchor.result_cf()) == anchor.proj_len() - anchor.entry_year() + 1


def test_mortality_reads_the_age_entering_the_contract_year(anchor):
    """age(t) is the age AT anniversary t, so q(t) is read one year lower.

    The horizon is the contract year *entered* at the mortality table's terminal age, so
    the last year carries q = 1.000000 and the projection closes itself.
    """
    table = anchor.data.mort_table()
    assert anchor.age(8) == 70
    assert anchor.mort_rate(8) == pytest.approx(
        float(table.loc[(69, "M"), "mort_rate"]), rel=1e-12)
    assert anchor.age(anchor.proj_len() - 1) == 120
    assert anchor.mort_rate(anchor.proj_len()) == 1.0
    assert anchor.pols_maturity(anchor.proj_len()) == 0.0


def test_space_docstrings_carry_their_reference_material(fixed_indexed_annuity):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = fixed_indexed_annuity.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("benefit_base_pp", "lw_pp", "mgsv_pp", "wd_excess_pp",
                  "depletion_cause", "shock_lapse_rate", "wd_unfunded_pp"):
        assert cells in proj
    assert "MGSV" in proj and "MGV" in proj      # the terminology bridge is explained
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
