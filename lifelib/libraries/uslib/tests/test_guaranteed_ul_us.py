"""Golden and product-specific tests for ULSG_US_S.

The golden values are the worked example in products/guaranteed_ul/technical-notes.md
("Worked example"), which projects the anchor cell male 60 ANB / NT Standard /
$500,000 / lifetime guarantee / level P* = $10,800, over the notes' policy months
301-305.  They are hard-coded here rather than pickled so that a reviewer can compare
them against the notes by eye.  The notes' months 301-305 are t = 1..5 in the model:
model point 1 is an in-force cell with duration_mth = 300.

Tolerance.  The notes display money to the cent but compute the table from cent-rounded
intermediates and from a net-amount-at-risk discount rounded to the whole dollar
(499,176 rather than 499,175.57 on the base account, 497,774 rather than 497,774.10 on
the shadow account), and they say so: "Independent recomputation may differ by cents
due to rounding."  The gap that leaves is at most 6 cents, on the shadow balance in the
fifth month, where five months of the notes' own one-cent interest roundings have
accumulated.  NOTES_ROUNDING is that bound, and
test_worked_example_gap_is_only_the_notes_rounding pins it so it cannot widen
unnoticed.

The one divergence that is *not* rounding -- the notes' worked example uses COI scales
quoted to the cent per $1,000 while the notes' own rule takes exact percentages of the
guaranteed maximum -- is shipped both ways and tested in
test_coi_scale_precision_divergence_is_shipped_not_resolved.
"""
import re

import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/guaranteed_ul/ULSG_US_S"

NOTES_ROUNDING = 0.06     # see the module docstring
CENT = 0.005
EXACT = 1e-9

# t: (premium_pp, prem_to_av_pp, mth_deduction_pp, inv_income_pp, av_pp,
#     prem_to_sg_pp, sg_deduction_pp, sg_inv_income_pp, sg_pp,
#     mth_deduction_forgone_pp, status)
WORKED_EXAMPLE = {
    1: (10800.00, 8100.00, 2842.68, 21.98, 7679.30,
        9936.00, 1778.15, 564.13, 126721.98, 0.00, "IN FORCE"),
    2: (0.00, 0.00, 2858.47, 13.84, 4834.67,
        0.00, 1783.90, 558.66, 125496.74, 0.00, "IN FORCE"),
    3: (0.00, 0.00, 2874.40, 5.63, 1965.90,
        0.00, 1789.71, 553.16, 124260.19, 0.00, "IN FORCE"),
    4: (0.00, 0.00, 2890.47, 0.00, 0.00,
        0.00, 1795.57, 547.62, 123012.24, 924.57, "IN FORCE - GUARANTEE"),
    5: (0.00, 0.00, 2900.89, 0.00, 0.00,
        0.00, 1801.49, 542.01, 121752.76, 2900.89, "IN FORCE - GUARANTEE"),
}

# IRC 7702(d)(2), the applicable percentage table [R4][REG-R13], as percentages: the
# value at each breakpoint of "more than / but not more than", plus one interior year
# of each ratable decrease.  The statute's last row is "more than 95: 100".
IRC_7702D2 = {
    18: 250, 40: 250, 41: 243, 45: 215, 47: 203, 50: 185, 53: 164, 55: 150,
    58: 138, 60: 130, 63: 124, 65: 120, 68: 117, 70: 115, 73: 109, 75: 105,
    85: 105, 90: 105, 91: 104, 92: 103, 93: 102, 94: 101, 95: 100, 100: 100,
    121: 100,
}

# The notes' "Model point attributes" table and the state variables it seeds, against
# the cells that carry them.  Every pair must appear as a row of the Projection
# docstring's naming table - that table is the model's index of the notes.
NOTES_MODEL_POINT_SYMBOLS = [
    ("issue_age", "age_at_entry"),
    ("sex", "sex"),
    ("risk_class", "rate_class"),
    ("face_amount, F", "sum_assured"),
    ("guarantee_age", "guarantee_age"),
    ("premium_pattern", "premium_type"),
    ("annual_premium", "premium_pp_ann"),
    ("premium_mode", "premium_mode"),
    ("duration_months", "duration_mth_init"),
    ("av_init", "av_pp_init"),
    ("sg_init", "sg_pp_init"),
    ("loan_init", "loan_bal_init"),
    ("rop_elected", "rop_elected"),
    ("CumPrem_0", "cum_prem_init"),
    ("(l_0)", "pols_if_init"),
]


@pytest.fixture(scope="module")
def guaranteed_ul():
    """The ULSG_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(guaranteed_ul):
    """Model point 1 - the worked-example anchor cell, in force at 300 months."""
    return guaranteed_ul.Projection[1]


@pytest.fixture(scope="module")
def new_biz(guaranteed_ul):
    """Model point 2 - the same policy from issue, on the notes' behavioural basis."""
    return guaranteed_ul.Projection[2]


@pytest.fixture(scope="module")
def single_pay(guaranteed_ul):
    """Model point 3 - the lifetime guarantee funded with one premium."""
    return guaranteed_ul.Projection[3]


@pytest.fixture(scope="module")
def underfunded(guaranteed_ul):
    """Model point 4 - a guarantee to age 90 that is not funded to reach it."""
    return guaranteed_ul.Projection[4]


# ---------------------------------------------------------------------------
# The worked example

@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, t):
    """Every cell of the notes' five-row table, to the notes' own rounding bound."""
    (prem, net_prem, ded, interest, av,
     sg_net_prem, sg_ded, sg_interest, sg, forgone, status) = WORKED_EXAMPLE[t]
    assert anchor.premium_pp(t) == pytest.approx(prem, abs=CENT)
    assert anchor.prem_to_av_pp(t) == pytest.approx(net_prem, abs=CENT)
    assert anchor.mth_deduction_pp(t) == pytest.approx(ded, abs=NOTES_ROUNDING)
    assert anchor.inv_income_pp(t) == pytest.approx(interest, abs=NOTES_ROUNDING)
    assert anchor.av_pp(t) == pytest.approx(av, abs=NOTES_ROUNDING)
    assert anchor.prem_to_sg_pp(t) == pytest.approx(sg_net_prem, abs=CENT)
    assert anchor.sg_deduction_pp(t) == pytest.approx(sg_ded, abs=NOTES_ROUNDING)
    assert anchor.sg_inv_income_pp(t) == pytest.approx(sg_interest, abs=NOTES_ROUNDING)
    assert anchor.sg_pp(t) == pytest.approx(sg, abs=NOTES_ROUNDING)
    assert anchor.mth_deduction_forgone_pp(t) == pytest.approx(
        forgone, abs=NOTES_ROUNDING)
    assert anchor.status(t) == status


def test_worked_example_gap_is_only_the_notes_rounding(anchor):
    """No figure in the notes' table is more than 6 cents from a clean recomputation.

    The bound exists so the divergence cannot widen silently.  It is dominated by the
    shadow balance in month 305, where the notes' interest column is one cent low in
    each of the five rows and the error accumulates.
    """
    worst = 0.0
    for t, row in WORKED_EXAMPLE.items():
        got = (anchor.premium_pp(t), anchor.prem_to_av_pp(t),
               anchor.mth_deduction_pp(t), anchor.inv_income_pp(t), anchor.av_pp(t),
               anchor.prem_to_sg_pp(t), anchor.sg_deduction_pp(t),
               anchor.sg_inv_income_pp(t), anchor.sg_pp(t),
               anchor.mth_deduction_forgone_pp(t))
        worst = max(worst, max(abs(g - n) for g, n in zip(got, row[:10])))
    assert worst < NOTES_ROUNDING
    assert worst > 0.0          # it is not zero; the notes' table is cent-rounded


def test_notes_naar_constants_are_dollar_roundings(anchor):
    """The notes' 499,176 and 497,774 are the discounted death benefit, to the dollar.

    Naming them here is what makes the residual gap in the worked example legible: the
    notes' arithmetic line uses the rounded constants, this model uses the exact ones.
    """
    assert anchor.db_pp(1) == 500000.0
    assert anchor.db_pp(1) / anchor.naar_factor() == pytest.approx(
        499175.57, abs=CENT)
    assert round(anchor.db_pp(1) / anchor.naar_factor()) == 499176
    assert anchor.db_pp(1) / anchor.sg_naar_factor() == pytest.approx(
        497774.10, abs=CENT)
    assert round(anchor.db_pp(1) / anchor.sg_naar_factor()) == 497774


def test_worked_example_monthly_factors(anchor):
    """The three monthly factors the notes print: base current, guaranteed, shadow."""
    assert anchor.inv_return_mth(1) == pytest.approx(0.0028709, abs=5e-8)
    assert anchor.guar_rate_mth() == pytest.approx(0.0016516, abs=5e-8)
    assert anchor.sg_rate_mth() == pytest.approx(0.0044717, abs=5e-8)
    assert anchor.naar_factor() == pytest.approx(1.0016516, abs=5e-8)
    assert anchor.sg_naar_factor() == pytest.approx(1.0044717, abs=5e-8)


def test_worked_example_charges(anchor):
    """The notes' arithmetic line: per-policy 5.50 + per-unit 100.00; shadow 0 + 25.00."""
    assert anchor.units(1) == 500.0
    assert anchor.maint_fee_pp(1) == pytest.approx(5.50 + 100.00, abs=EXACT)
    assert anchor.sg_maint_fee_pp(1) == pytest.approx(25.00, abs=EXACT)
    assert anchor.coi_rate_guar(1) == pytest.approx(8.615, abs=5e-4)
    assert anchor.coi_rate(1) == 5.60
    assert anchor.sg_coi_rate(1) == 4.74


def test_coi_scale_precision_divergence_is_shipped_not_resolved(anchor, new_biz):
    """Documented divergence: the notes' rule gives 5.59975, their table uses 5.60.

    The rule is 65% and 55% of the guaranteed maximum; the worked example is computed
    with those figures rounded to the cent per $1,000, which is how the notes quote
    them.  Point 1 carries coi_rate_dp = 2 so the golden table reproduces; point 2 is
    the same cell and leaves the column blank, taking the rule at full precision.
    Neither is "correct" - the whole scale is a standardization - and the test exists
    so the gap cannot be closed silently in either direction.
    """
    t85 = 301                                   # attained age 85 on the from-issue cell
    assert new_biz.age(t85) == 85 == anchor.age(1)
    assert anchor.coi_rate_dp() == 2
    assert new_biz.coi_rate_dp() == -1

    assert new_biz.coi_rate(t85) == pytest.approx(0.65 * 8.615, abs=1e-9)
    assert new_biz.sg_coi_rate(t85) == pytest.approx(0.55 * 8.615, abs=1e-9)
    assert anchor.coi_rate(1) == 5.60 != pytest.approx(new_biz.coi_rate(t85), abs=1e-6)
    assert anchor.sg_coi_rate(1) == 4.74 != pytest.approx(
        new_biz.sg_coi_rate(t85), abs=1e-6)

    # The size of the gap, on the worked example's own net amounts at risk.
    base_gap = (5.60 - 0.65 * 8.615) / 1000 * anchor.net_amt_at_risk(1)
    sg_gap = (4.74 - 0.55 * 8.615) / 1000 * anchor.sg_net_amt_at_risk(1)
    assert base_gap == pytest.approx(0.12, abs=0.01)
    assert sg_gap == pytest.approx(0.65, abs=0.01)


# ---------------------------------------------------------------------------
# The pitfalls the notes list, one test each

def test_naar_discount_convention_and_its_floor(anchor):
    """NAAR = max(DB/(1+j) - max(AV', 0), 0), with AV' after expenses, before COI.

    The notes' pitfall list opens with the discount convention, and the floor is what
    the guarantee-support regime turns on: in month 305 the account value after the
    expense charges is -105.50, yet the cost of insurance is charged on the whole
    discounted death benefit rather than on something larger.
    """
    for t in (1, 2, 3, 4, 5):
        assert anchor.net_amt_at_risk(t) == pytest.approx(
            max(0.0, anchor.db_pp(t) / anchor.naar_factor()
                - max(anchor.av_pp_at(t, "BEF_COI"), 0.0)), abs=EXACT)
        assert anchor.sg_net_amt_at_risk(t) == pytest.approx(
            max(0.0, anchor.db_pp(t) / anchor.sg_naar_factor()
                - max(anchor.sg_pp_at(t, "BEF_COI"), 0.0)), abs=EXACT)
    assert anchor.av_pp_at(5, "BEF_COI") == pytest.approx(-105.50, abs=CENT)
    assert anchor.net_amt_at_risk(5) == pytest.approx(499175.57, abs=CENT)


def test_the_two_accounts_discount_at_their_own_rates(anchor):
    """The shadow NAAR discounts at the shadow rate, not the base guaranteed rate."""
    assert anchor.naar_factor() != anchor.sg_naar_factor()
    assert anchor.net_amt_at_risk(1) != pytest.approx(
        anchor.sg_net_amt_at_risk(1), abs=1.0)


def test_monthly_coi_is_the_simple_twelfth(anchor, guaranteed_ul):
    """Contractual COI is annual/12; experience mortality is the compound conversion.

    The notes fix the simple twelfth for the COI and say expressly not to mix it with
    1 - (1-q)^(1/12), which differs materially above age 85 where q exceeds 0.10.
    """
    scale = guaranteed_ul.Data.coi_rates().loc[("M", "StdNT", 85), "coi_rate_guar_ann"]
    assert scale == pytest.approx(8.615 * 12, abs=5e-4)
    assert anchor.coi_rate_guar(1) == pytest.approx(scale / 12, abs=1e-12)

    q = scale / 1000
    compound = 1 - (1 - q) ** (1 / 12)
    assert compound / (q / 12) > 1.05        # 5% apart at age 85; not interchangeable
    assert anchor.mort_rate_mth(1) == pytest.approx(
        1 - (1 - anchor.mort_rate(1)) ** (1 / 12), abs=1e-15)


def test_account_value_floors_at_zero_and_the_shortfall_is_forgone(anchor):
    """Month 304: 2,890.47 due, 1,965.90 taken, 924.57 forgone, account value zero."""
    assert anchor.av_pp(3) == pytest.approx(1965.90, abs=NOTES_ROUNDING)
    assert anchor.mth_deduction_pp(4) == pytest.approx(2890.47, abs=NOTES_ROUNDING)
    assert anchor.mth_deduction_taken_pp(4) == pytest.approx(
        1965.90, abs=NOTES_ROUNDING)
    assert anchor.mth_deduction_forgone_pp(4) == pytest.approx(
        924.57, abs=NOTES_ROUNDING)
    assert anchor.av_pp(4) == 0.0
    assert anchor.is_shortfall(4) is True
    assert anchor.is_guar_supported(4) is True      # so it is forgone, not a grace
    assert anchor.grace_mth(4) == 0
    assert anchor.status(4) == "IN FORCE - GUARANTEE"


def test_the_zero_floor_is_unconditional_and_that_is_a_deviation(anchor):
    """Shipped, not resolved: the notes floor AV only while the guarantee is active.

    The notes' pitfall list says `AV` "floors at 0 only while the guarantee is active",
    and their step 6 sets ``AV''_t = 0`` in the guarantee branch alone - the grace
    branch gets no account-value recursion at all.  This model floors it
    unconditionally, in grace and after a lapse too, because a negative balance would
    break check_av_roll_fwd(), which closes on the deduction actually *taken* and
    nothing is taken from an exhausted account.

    Nothing in the cash flows moves, and this test says so.  What does follow is that
    two per-policy columns keep running where the notes define nothing: the forgone
    deduction in the grace months, and the whole account value after the lapse.  Both
    are pinned here so the deviation cannot be forgotten or quietly closed.
    """
    # The grace months: the guarantee has failed and the floor binds anyway.
    for t in (81, 82):
        assert anchor.is_guar_active(t) is False
        assert anchor.is_guar_supported(t) is False
        assert anchor.status(t) == "GRACE"
        assert anchor.av_pp_at(t, "BEF_COI") == pytest.approx(-105.50, abs=CENT)
        assert anchor.av_pp_at(t, "BEF_INV") == 0.0     # the notes would leave it < 0
        assert anchor.av_pp(t) == 0.0
        # ... and the forgone-deduction cells reports the shortfall there, where the
        # notes' D_t is not defined - it is their required grace payment instead.
        assert anchor.mth_deduction_forgone_pp(t) == pytest.approx(5007.40, abs=CENT)
        assert anchor.mth_deduction_forgone_pp(t) == pytest.approx(
            anchor.mth_deduction_pp(t), abs=EXACT)
        assert anchor.mth_deduction_taken_pp(t) == 0.0
        assert anchor.cure_premium_pp(t) == pytest.approx(
            anchor.mth_deduction_forgone_pp(t) / 0.75, abs=EXACT)

    # No cash flow moves either way: the policy leaves grace with nothing.
    assert anchor.claims(82, "GRACE") == 0.0
    assert anchor.claims_from_av(82, "GRACE") == 0.0
    assert anchor.check_av_roll_fwd() is True

    # After the lapse the per-policy account goes on projecting, weighted by nothing:
    # the next annual premium credits its full 8,100 to an account no policy holds.
    assert anchor.status(85) == "LAPSED"
    assert anchor.pols_if(85) == 0.0
    assert anchor.premium_pp(85) == 10800.0
    assert anchor.av_pp_at(85, "BEF_WD") == pytest.approx(8100.0, abs=EXACT)
    assert anchor.av_pp(85) == pytest.approx(2731.95, abs=CENT)
    assert anchor.premiums(85) == 0.0
    assert anchor.mth_deduction_forgone(85) == 0.0
    assert anchor.net_cf(85) == 0.0


def test_forgone_deductions_are_not_receivables(anchor):
    """D_t never accrues against future premiums or account value recoveries.

    From month 305 to the next anniversary the whole deduction is forgone every month,
    nothing is taken and the account value stays exactly zero - it does not go
    negative.  When the next annual premium arrives in month 13 of the projection it is
    credited **in full**: none of the eight months of forgone deductions is recovered
    out of it.  check_av_roll_fwd() closes on the deduction *taken*, which is what
    proves the forgone part never touched the account.
    """
    for t in range(5, 13):
        assert anchor.av_pp(t) == 0.0
        assert anchor.mth_deduction_taken_pp(t) == 0.0
        assert anchor.mth_deduction_forgone_pp(t) == pytest.approx(
            anchor.mth_deduction_pp(t), abs=EXACT)

    arrears = sum(anchor.mth_deduction_forgone_pp(t) for t in range(4, 13))
    assert arrears > 20000.0
    assert anchor.premium_pp(13) == 10800.0
    assert anchor.av_pp_at(13, "BEF_WD") == pytest.approx(
        anchor.av_pp(12) + anchor.prem_to_av_pp(13), abs=EXACT)
    assert anchor.av_pp_at(13, "BEF_WD") == pytest.approx(8100.0, abs=EXACT)
    assert anchor.check_av_roll_fwd() is True


def test_shadow_account_is_never_floored(underfunded):
    """A negative shadow balance is the catch-up shortfall; flooring it destroys C_t.

    Model point 4 runs its guarantee out, so the shadow account net of debt goes
    negative and the catch-up premium becomes the shortfall grossed up for the 8%
    shadow load.
    """
    t = 235
    assert underfunded.sg_net_pp(t) < 0
    assert underfunded.is_guar_active(t) is False
    assert underfunded.catch_up_prem_pp(t) == pytest.approx(
        -underfunded.sg_net_pp(t) / (1 - underfunded.load_prem_rate_sg), abs=EXACT)
    assert underfunded.catch_up_prem_pp(t) > -underfunded.sg_net_pp(t)
    # ... and it keeps growing, which a floor at zero would hide entirely.
    assert underfunded.sg_net_pp(t + 1) < underfunded.sg_net_pp(t)
    assert underfunded.check_sg_roll_fwd() is True


def test_the_guarantee_test_runs_after_the_deduction_attempt(anchor):
    """Order of tests: a failed deduction under a live guarantee is forgone, not grace.

    The anchor's account value fails from month 4 but the shadow account carries it
    for another 77 months; the grace period opens only in the month the guarantee
    itself goes, and the policy lapses two months later.
    """
    assert anchor.is_shortfall(80) is True
    assert anchor.is_guar_active(80) is True
    assert anchor.grace_mth(80) == 0
    assert anchor.status(80) == "IN FORCE - GUARANTEE"

    assert anchor.sg_net_pp(81) < 0
    assert anchor.is_guar_active(81) is False
    assert anchor.grace_mth(81) == 1
    assert anchor.grace_mth(82) == 2
    assert anchor.status(82) == "GRACE"
    assert anchor.is_lapsed(82) is False
    assert anchor.is_lapsed(83) is True
    assert anchor.status(83) == "LAPSED"
    assert anchor.pols_if(83) == 0.0


def test_lapse_for_insufficiency_takes_the_whole_remaining_block(anchor):
    """The grace lapse is contractual termination, not a rate: nothing survives it.

    It also pays nothing - the cash surrender value is zero in grace by construction -
    which is why claims(t, "GRACE") is zero while pols_lapse_grace(t) is not.
    """
    assert anchor.pols_lapse_grace(82) == pytest.approx(
        anchor.pols_if(82) - anchor.pols_death(82) - anchor.pols_lapse(82)
        - anchor.pols_rop(82), abs=EXACT)
    assert anchor.pols_lapse_grace(82) > 0.0
    assert anchor.claims(82, "GRACE") == 0.0
    assert anchor.claims_from_av(82, "GRACE") == 0.0     # the account is exhausted
    assert all(anchor.pols_lapse_grace(t) == 0.0 for t in range(1, 82))


def test_age_basis_is_anb_throughout(new_biz):
    """Attained age advances on the policy anniversary, never mid-year."""
    assert new_biz.age(1) == 60
    assert new_biz.age(12) == 60
    assert new_biz.age(13) == 61
    assert new_biz.policy_year(12) == 1
    assert new_biz.policy_year(13) == 2


def test_guarantee_test_is_strictly_positive(underfunded):
    """`SG - L > 0`, not `>= 0`: the notes warn about the monthly grid boundary."""
    p = underfunded.no_lapse_premium()
    assert underfunded.guar_min_sg(p) > 0
    assert underfunded.guar_min_sg(p - 1.0) <= 0


# ---------------------------------------------------------------------------
# Roll-forwards and structure

def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + surrenders + refunds + grace lapses."""
    for t in range(1, anchor.proj_len() + 1):
        out = (anchor.pols_death(t) + anchor.pols_lapse(t) + anchor.pols_rop(t)
               + anchor.pols_lapse_grace(t) + anchor.pols_maturity(t))
        assert anchor.pols_if(t) - anchor.pols_if(t + 1) == pytest.approx(
            out, abs=1e-12)


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(1, anchor.proj_len() + 1):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


@pytest.mark.parametrize("point_id", [1, 2, 3, 4])
def test_roll_forwards_close(guaranteed_ul, point_id):
    """The account value, the shadow account and the margin identity all close."""
    proj = guaranteed_ul.Projection[point_id]
    assert proj.check_av_roll_fwd() is True
    assert proj.check_sg_roll_fwd() is True
    assert proj.check_margin() is True


def test_maturity_is_identically_zero(anchor):
    """Guaranteed UL has no maturity date; coverage continues past age 121 [S7]."""
    assert all(anchor.pols_maturity(t) == 0.0
               for t in range(1, anchor.proj_len() + 1))


def test_projection_horizon_is_attained_age_121(anchor, new_biz):
    """proj_len = 12 x (121 - issue age) - elapsed months, the notes' maximum."""
    assert new_biz.proj_len() == 12 * (121 - 60)
    assert anchor.proj_len() == 12 * (121 - 60) - 300
    assert anchor.duration_mth(1) == 300
    assert anchor.age(anchor.proj_len()) == 120
    assert anchor.age(anchor.proj_len()) + 1 == 121


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(1, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert set(df.columns) == {
        "pols_if", "premiums", "claims_death", "claims_lapse", "claims_rop",
        "withdrawals", "expenses", "premium_taxes", "net_cf",
    }
    assert df.loc[1, "premiums"] == pytest.approx(10800.0, abs=CENT)


def test_result_cf_columns_sum_to_net_cf(anchor):
    """The cash flow columns reconcile to net_cf, income-positive.

    `pols_if` is the weight, not a cash flow; everything else nets to `net_cf` with
    income positive, which is what makes the column comparable across the library.
    """
    df = anchor.result_cf()
    net = (df["premiums"] - df["claims_death"] - df["claims_lapse"]
           - df["claims_rop"] - df["withdrawals"] - df["expenses"]
           - df["premium_taxes"])
    assert (net - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    # Income-positive: premium income raises net_cf, claim outgo lowers it.
    assert df.loc[1, "premiums"] > 0 and df.loc[2, "premiums"] == 0
    assert anchor.net_cf(1) == pytest.approx(
        anchor.premiums(1) - anchor.claims(1) - anchor.withdrawals(1)
        - anchor.expenses(1) - anchor.premium_taxes(1), abs=EXACT)


def test_pols_if_weights_its_own_row(anchor):
    """`pols_if(t)` is the start-of-month count and the weight on that same row.

    So the printed in-force column reconciles with the cash flows beside it:
    `premiums(t) / premium_pp(t)` is exactly it, and `pols_if_at` agrees at every
    timing because nothing changes the count before the end-of-month decrements.
    """
    df = anchor.result_cf()
    assert anchor.pols_if(1) == anchor.pols_if_init()
    for t in (1, 13, 25):
        assert anchor.premium_pp(t) > 0
        assert df.loc[t, "premiums"] / anchor.premium_pp(t) == pytest.approx(
            df.loc[t, "pols_if"], abs=EXACT)
    for timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"):
        assert anchor.pols_if_at(40, timing) == anchor.pols_if(40)


def test_withdrawals_are_a_payment_not_a_claim(anchor, guaranteed_ul):
    """A withdrawal is the owner's election, so it is `withdrawals`, never a claim.

    `claims(t, "WITHDRAWAL")` raises, and the `kind is None` total therefore cannot
    double-count the `withdrawals` column of `result_cf()`.  The per-policy branch of
    `claim_pp` stays, because `withdrawals` weights it, and so does the
    `claims_from_av` branch, because a withdrawal does release account value.
    """
    _raises_invalid(anchor.claims, 1, "WITHDRAWAL")

    t = 1
    assert anchor.withdrawals(t) == pytest.approx(
        anchor.claim_pp(t, "WITHDRAWAL") * anchor.pols_if(t), abs=EXACT)
    assert anchor.claim_pp(t, "WITHDRAWAL") == anchor.wd_pp(t)
    assert anchor.claims_from_av(t, "WITHDRAWAL") == anchor.withdrawals(t)

    # Utilisation is zero in every shipped model point, so the column is zero and the
    # claims total is the three termination kinds alone.
    for point_id in guaranteed_ul.Data.model_point_table().index:
        proj = guaranteed_ul.Projection[point_id]
        assert proj.result_cf()["withdrawals"].abs().max() == 0.0
    for t in (1, 40, 81):
        assert anchor.claims(t) == pytest.approx(
            anchor.claims(t, "DEATH") + anchor.claims(t, "LAPSE")
            + anchor.claims(t, "REFUND") + anchor.claims(t, "GRACE"), abs=EXACT)


def test_checks_take_no_argument_and_return_bool(anchor):
    """Every `check_*` is a no-arg bool over the whole projection, library-wide."""
    for check in (anchor.check_av_roll_fwd, anchor.check_sg_roll_fwd,
                  anchor.check_margin):
        got = check()
        assert isinstance(got, bool)
        assert got is True


def test_result_av_carries_the_worked_example_columns(anchor):
    df = anchor.result_av()
    assert list(df.columns) == [
        "premium_pp", "prem_to_av_pp", "mth_deduction_pp", "inv_income_pp", "av_pp",
        "prem_to_sg_pp", "sg_deduction_pp", "sg_inv_income_pp", "sg_pp",
        "forgone_pp", "status",
    ]
    assert df.loc[1, "sg_pp"] == pytest.approx(126721.98, abs=NOTES_ROUNDING)
    assert df.loc[4, "status"] == "IN FORCE - GUARANTEE"


def test_every_model_point_projects(guaranteed_ul):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in guaranteed_ul.Data.model_point_table().index:
        df = guaranteed_ul.Projection[point_id].result_cf()
        assert len(df) > 0


def test_corridor_table_is_the_irc_7702d2_applicable_percentages(guaranteed_ul, anchor):
    """corridor_factors.csv is labelled `sourced [R4]`, so every row must be sourced.

    The cited source is the IRC 7702(d)(2) applicable-percentage table.  Its last row
    is "more than 95: 100", so the factor is 1.00 from attained age 95 on - not 1.01,
    which no row of the statute contains and which the provenance column would have
    been claiming as sourced.
    """
    tbl = guaranteed_ul.Data.corridor_factors()
    assert set(tbl["provenance"]) == {"sourced [R4]"}
    for a, pct in IRC_7702D2.items():
        assert tbl.loc[a, "corridor_factor"] == pytest.approx(pct / 100, abs=1e-12)
    assert tbl["corridor_factor"].loc[95:].eq(1.00).all()
    assert anchor.corridor_factor(1) == 1.05             # attained age 85

    # It never binds on any shipped point - which is why the death benefit is a max.
    for point_id in guaranteed_ul.Data.model_point_table().index:
        proj = guaranteed_ul.Projection[point_id]
        assert all(proj.db_pp(t) == proj.sum_assured_at(t)
                   for t in range(1, proj.proj_len() + 1))


def test_projection_docstring_maps_every_notes_model_point_symbol(guaranteed_ul):
    """The naming table is the model's index of the notes, so it must be complete.

    Every attribute of the notes' "Model point attributes" table that has a cells, and
    every state variable initial value it seeds, appears as a row of the naming table
    in the Projection docstring - `risk_class -> rate_class` above all, which is the
    one model point attribute this model renames.
    """
    rows = {}
    for line in guaranteed_ul.Projection.doc.splitlines():
        parts = re.split(r"\s{2,}", line.rstrip())
        if len(parts) >= 2 and not line.startswith(" "):
            rows.setdefault(parts[0], parts[1])
    for symbol, cells in NOTES_MODEL_POINT_SYMBOLS:
        assert symbol in rows, "no naming-table row for the notes' " + symbol
        assert cells in rows[symbol], (
            "the naming-table row for " + symbol + " does not name " + cells)
    assert rows["risk_class"] == "rate_class"


def _raises_invalid(fn, *args):
    """modelx wraps a formula's exception, so match on the message, not the type."""
    with pytest.raises(Exception) as excinfo:
        fn(*args)
    assert "invalid" in str(excinfo.value)


def test_invalid_arguments_raise(anchor):
    for bad in ("BEF_COI_X", "EOM", ""):
        _raises_invalid(anchor.av_pp_at, 1, bad)
        _raises_invalid(anchor.sg_pp_at, 1, bad)
    _raises_invalid(anchor.claim_pp, 1, "ANNUITIZATION")
    _raises_invalid(anchor.claims, 1, "ANNUITIZATION")
    _raises_invalid(anchor.claims_from_av, 1, "ANNUITIZATION")
    _raises_invalid(anchor.pols_if_at, 1, "BEF_INV")


# ---------------------------------------------------------------------------
# Product features

def test_rop_window_and_cap(anchor):
    """The year-25 window refunds 100% of premiums, capped at 40% of face [S1]."""
    assert anchor.rop_anniversary(1) == 25
    assert anchor.rop_ratio(1) == 1.00
    assert anchor.rop_rate(1) == 0.10
    assert anchor.cum_prem_pp(1) == pytest.approx(280800.0, abs=CENT)
    assert anchor.claim_pp(1, "REFUND") == 200000.0            # the cap binds
    assert anchor.claim_pp(1, "REFUND") < anchor.cum_prem_pp(1)
    assert anchor.pols_rop(1) == pytest.approx(
        anchor.pols_if(1) * (1 - anchor.mort_rate_mth(1))
        * (1 - anchor.lapse_rate_mth(1)) * 0.10, abs=EXACT)


def test_rop_windows_are_confined_to_the_two_anniversaries(new_biz, underfunded):
    """Exercise only at anniversaries 20 and 25, and only when the rider is elected."""
    on = [t for t in range(1, new_biz.proj_len() + 1) if new_biz.rop_rate(t) > 0]
    assert on == [12 * 20 + 1, 12 * 25 + 1]
    assert new_biz.rop_ratio(12 * 20 + 1) == 0.50
    assert new_biz.rop_rate(12 * 20 + 1) == 0.05
    assert new_biz.rop_ratio(12 * 25 + 1) == 1.00
    assert new_biz.rop_rate(12 * 25 + 1) == 0.10
    assert underfunded.rop_elected() is False
    assert all(underfunded.rop_rate(t) == 0.0
               for t in range(1, underfunded.proj_len() + 1))


def test_rop_is_an_option_against_the_insurer(anchor):
    """The refund dwarfs the account value released, which is what makes it an option."""
    assert anchor.margin_rop(1) < 0
    assert anchor.margin_rop(1) == pytest.approx(
        (anchor.av_pp(1) - 200000.0) * anchor.pols_rop(1), abs=EXACT)


def test_lifetime_guarantee_lapse_multiplier(anchor, underfunded):
    """G = 0.55 for a lifetime election [R7-anchored], 1.0 for a guarantee to 90."""
    assert anchor.guarantee_age() == 121
    assert anchor.lapse_rate_guar_mult() == 0.55
    assert underfunded.guarantee_age() == 90
    assert underfunded.lapse_rate_guar_mult() == 1.0


def test_premium_pattern_lapse_multiplier(anchor, single_pay):
    """Phi: 1.0 level, 0.6 single-pay - higher lapses for level payers [R8]."""
    assert anchor.lapse_rate_pattern_mult() == 1.0
    assert single_pay.lapse_rate_pattern_mult() == 0.6


def test_dynamic_lapse_factor_tracks_funding_status(anchor, underfunded):
    """Psi: 1.0 funded, 0.6 on the guarantee alone, 2.0 once the guarantee has gone."""
    assert anchor.av_pp(1) > 0 and anchor.is_guar_active(1)
    assert anchor.lapse_rate_dyn_mult(1) == 1.0
    assert anchor.av_pp(5) == 0.0 and anchor.is_guar_active(5)
    assert anchor.lapse_rate_dyn_mult(5) == 0.6
    assert underfunded.is_guar_active(235) is False
    assert underfunded.lapse_rate_dyn_mult(235) == 2.0


def test_lapse_rate_floor_and_cap(anchor):
    """min(0.5, max(0.003, b G Phi Psi)) - the floor is applied after the dynamic factor."""
    for t in range(1, anchor.proj_len() + 1):
        assert 0.003 <= anchor.lapse_rate(t) <= 0.5
    # 0.0075 base x 0.55 x 1.0 x 0.6 = 0.002475, below the 0.3% floor
    assert anchor.lapse_rate_base(5) == 0.0075
    assert anchor.lapse_rate(5) == 0.003


def test_surrender_charge_runs_off_over_fifteen_years(new_biz):
    """18 x max(0, (180 - m)/180) per $1,000 of initial face, m the current month."""
    assert new_biz.surr_charge_rate(1) == pytest.approx(17.90, abs=EXACT)
    assert new_biz.surr_charge_pp(1) == pytest.approx(17.90 * 500, abs=EXACT)
    assert new_biz.surr_charge_rate(179) == pytest.approx(0.10, abs=1e-12)
    assert new_biz.surr_charge_rate(180) == 0.0
    assert new_biz.surr_charge_rate(181) == 0.0


def test_notes_csv_symbol_is_ncsv(new_biz):
    """The notes' CSV_t = max(AV - SC - L, 0) is this model's ncsv_pp, not csv_pp."""
    t = 200
    assert new_biz.ncsv_pp(t) == pytest.approx(
        max(0.0, new_biz.av_pp(t) - new_biz.surr_charge_pp(t)
            - new_biz.loan_bal_pp(t)), abs=EXACT)
    assert new_biz.claim_pp(t, "LAPSE") == new_biz.ncsv_pp(t)


def test_mortality_improvement_grades_and_stops(new_biz):
    """1%/yr to age 85, grading to 0% at 95, applied for at most 20 years."""
    assert new_biz.mort_improve_rate(1) == 0.01               # attained age 60
    assert new_biz.mort_improve_rate(12 * 30 + 1) == pytest.approx(0.005)  # age 90
    assert new_biz.mort_improve_rate(12 * 35 + 1) == 0.0      # age 95
    assert new_biz.mort_improve_factor(1) == 1.0
    assert new_biz.mort_improve_factor(13) == pytest.approx(0.99, abs=1e-12)
    assert new_biz.mort_improve_factor(12 * 20 + 1) == pytest.approx(
        0.99 ** 20, abs=1e-12)
    # capped at 20 years: no further improvement after that
    assert new_biz.mort_improve_factor(new_biz.proj_len()) == pytest.approx(
        new_biz.mort_improve_factor(12 * 20 + 1), abs=1e-12)


def test_premium_persistency_is_applied_once(anchor, new_biz):
    """phi multiplies the premium received, so account, shadow and income agree.

    The anchor overrides it to 1.00 because the notes' worked example is a
    contract-mechanics view with the behavioural assumptions suppressed; the
    from-issue point takes the notes' 98%.
    """
    assert anchor.prem_persistency(1) == 1.00
    assert anchor.premium_pp(1) == 10800.0
    assert new_biz.prem_persistency(1) == 0.98
    assert new_biz.premium_pp(1) == pytest.approx(10800.0 * 0.98, abs=CENT)
    assert new_biz.prem_to_av_pp(1) == pytest.approx(
        new_biz.premium_pp(1) * 0.75, abs=EXACT)
    assert new_biz.prem_to_sg_pp(1) == pytest.approx(
        new_biz.premium_pp(1) * 0.92, abs=EXACT)
    assert new_biz.premiums(1) == pytest.approx(
        new_biz.premium_pp(1) * new_biz.pols_if(1), abs=EXACT)


def test_premium_falls_on_anniversaries_only(new_biz):
    assert new_biz.premium_mode() == "A"
    assert new_biz.premium_freq() == 1
    on = [t for t in range(1, 37) if new_biz.is_premium_mth(t)]
    assert on == [1, 13, 25]
    assert all(new_biz.premium_pp(t) == 0.0 for t in (2, 5, 12, 14, 24))


def test_single_pay_takes_one_premium(single_pay):
    assert single_pay.premium_pp(1) == pytest.approx(152300.0, abs=CENT)
    assert all(single_pay.premium_pp(t) == 0.0 for t in range(2, 40))
    assert single_pay.cum_prem_pp(40) == pytest.approx(152300.0, abs=CENT)


# ---------------------------------------------------------------------------
# The funding-premium solve

def test_no_lapse_premium_reproduces_the_notes_calibration(new_biz):
    """P* for the from-issue anchor cell is the notes' illustrative $10,800 **[std]**.

    The notes calibrate the standardized shadow parametrization so that the solved
    level lifetime premium for male 60 NT Standard / $500,000 lands near $10,800; the
    illustrative guaranteed-maximum COI curve shipped with the model is fitted so that
    it does.  Both the target and the curve are standardizations.
    """
    p = new_biz.no_lapse_premium()
    assert p == pytest.approx(10800.0, abs=10.0)
    assert new_biz.guar_min_sg(p) > 0
    assert new_biz.guar_min_sg(p - 1.0) <= 0
    assert new_biz.solve_len() == 12 * (121 - 60)


def test_solve_is_monotone_in_the_premium(new_biz):
    """g(P) is non-decreasing in P, which is what makes bisection safe."""
    vals = [new_biz.guar_min_sg(p) for p in (5000.0, 8000.0, 11000.0, 14000.0)]
    assert vals == sorted(vals)


def test_premium_persistency_shifts_the_guarantee_failure_time(new_biz):
    """The notes' third sensitivity, measured: 98% moves the failure from 112 to 101.

    Point 2 pays the notes' P* = $10,800, which is $3.93 *under* this model's own
    solved $10,803.93 - so it is marginally underfunded before persistency enters at
    all, and its lifetime guarantee fails even at 100%: on the contractual path,
    attained age 112.  The 98% is what moves that to attained age 101.

    Asserting only that the premium paid is under P* would not pin the effect this
    test is named for: 10,800 < 10,803.93 holds at 100% persistency too.  So the shift
    itself is asserted, by replaying the same contractual recursion at the scheduled
    premium and at 98% of it.
    """
    p_star = new_biz.no_lapse_premium()
    assert p_star == pytest.approx(10803.93, abs=0.01)
    assert new_biz.premium_pp_ann() == 10800.0 < p_star      # under P* before phi
    assert new_biz.prem_persistency(1) == 0.98
    assert new_biz.premium_pp(1) == pytest.approx(10800.0 * 0.98, abs=CENT)

    def first_fail(prem):
        """The first month of the contractual shadow path with SG - L <= 0."""
        for t in range(1, new_biz.solve_len() + 1):
            if new_biz.sg_pp_solve(t, prem) - new_biz.loan_bal_pp(t) <= 0:
                return t
        return None

    full = first_fail(10800.0)                    # persistency off: the solve's basis
    with_phi = first_fail(10800.0 * 0.98)
    assert new_biz.age(full) == 112               # already short of 121 at 100%
    assert new_biz.age(with_phi) == 101           # ... and eleven years worse at 98%
    assert full == 632 and with_phi == 503

    # The projection's own path agrees with the 98% replay, month for month.
    failed = [t for t in range(1, new_biz.proj_len() + 1)
              if not new_biz.is_guar_active(t)]
    assert failed, "the guarantee should fail on a 98% payer"
    assert failed[0] == with_phi
    assert new_biz.age(failed[0]) == 101 < 121
    assert any(new_biz.status(t) == "LAPSED"
               for t in range(1, new_biz.proj_len() + 1))


def test_single_pay_point_is_funded_for_life(single_pay):
    """Point 3 pays above its solved single premium, so the guarantee never fails."""
    assert single_pay.premium_pp(1) > single_pay.no_lapse_premium()
    assert all(single_pay.is_guar_active(t)
               for t in range(1, single_pay.proj_len() + 1))
    assert all(single_pay.grace_mth(t) == 0
               for t in range(1, single_pay.proj_len() + 1))


def test_in_force_anchor_is_not_a_fully_funded_lifetime_guarantee(anchor):
    """The notes' opening shadow balance does not support the notes' own P* to 121.

    $118,000 at duration 300 is far less than a policy funded at P* = $10,800 from
    issue would carry, so the anchor's guarantee fails at attained age 91 and the
    premium that would sustain it from here is several times $10,800.  Both figures
    in the notes are labelled illustrative; the model ships them as given rather than
    adjusting either, and this test records the consequence.
    """
    assert anchor.sg_pp_init() == 118000.0
    assert anchor.premium_pp_ann() == 10800.0
    assert anchor.no_lapse_premium() > 2.5 * anchor.premium_pp_ann()
    assert anchor.is_guar_active(80) is True
    assert anchor.is_guar_active(81) is False
    assert anchor.age(81) == 91
