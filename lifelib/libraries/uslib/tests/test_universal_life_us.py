"""Golden and product-specific tests for UL_US_S.

The golden values are the worked example in
products/universal_life/technical-notes.md ("Worked example"), which projects the
specimen anchor cell Male 35 Standard NT / $100,000 / Option A / GPT, $150 a month of
planned premium, on the monthly grid.  They are hard-coded here rather than pickled so
that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the cent.  Everything the
notes' three-row table prints is asserted, column by column, plus the full-precision
issue-month trace printed underneath it and one test per entry in the notes' "Known
modeling pitfalls" list.

The time index is 0-based, as in the notes and the rest of the library: ``t = 0`` is
the issue month of the anchor cell (the first projected month of the in-force point),
the frame is ``t = 0 .. proj_len() - 1``, and the contractual policy year is
``policy_year(t) = duration(t) + 1``.  The month literals below are ``t`` values; a
policy year ``y`` starts at ``t = 12 * (y - 1)``.

Four tests in the "Roll-forwards and invariants" section exist because a review found
the model wrong, and each fails against the behaviour it replaced: the death benefit
floor, the shortfall table across all three model points and the whole projection, the
annual free-withdrawal allowance, and the latching MEC flag.  They are regression tests;
do not weaken them without re-deriving from the notes.

Three more pin the library-wide cash flow conventions this model was harmonized onto:
a partial withdrawal is ``withdrawals(t)`` and not a ``kind`` of ``claims``, the
``result_cf()`` flow columns sum to an income-positive ``net_cf``, and ``pols_if(t)`` is
the start-of-month count that weights that same row.
"""
import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/universal_life/UL_US_S"

CENT = 0.005          # money displayed to 2 d.p. in the notes

# Worked example, technical-notes.md "Worked example" table; t = 0 is the issue month.
# t: (AV(t-1), NP, AV', DB, NAAR, COI, MD, AV'-MD, interest, AV(t))
WORKED_EXAMPLE = {
    0: (0.00, 141.00, 141.00, 100000.0, 99694.11, 6.04, 39.54, 101.46, 0.33, 101.80),
    1: (101.80, 141.00, 242.80, 100000.0, 99592.32, 6.03, 39.53, 203.27, 0.67, 203.93),
    2: (203.93, 141.00, 344.93, 100000.0, 99490.18, 6.02, 39.52, 305.41, 1.00, 306.41),
}

# The trace printed under the table (the issue month, t = 0), at the precision the
# notes give it.
TRACE = {
    "i_m": 0.0032737,               # (1 + 4.00%)^(1/12) - 1
    "naar_factor": 1.0016516,       # (1 + 2.00%)^(1/12)
    "db_discounted": 99835.11,      # 100,000 x 0.9983511
    "coi_rate_guar_yr1": 0.10090,   # specimen guaranteed maximum, policy year 1 [S3]
    "coi_rate_yr1": 0.060540,       # 60% of it [std]
    "coi_pp_0": 6.0355,             # 0.060540/1000 x 99,694.11
    "mth_deduction_pp_0": 39.5355,  # 7.50 + 26.00 + 6.0355
    "corridor_min_0": 352.50,       # 2.50 x 141.00, which does not bind
}

# The grace trigger by model point: (proj_len, months in shortfall, first such t).
# The notes' cascade is not implemented, so the trigger is a diagnostic - but it is not
# inert, and the README carries this same table.  Point 2 (Option B) keeps a ~$100,000
# net amount at risk for life, so the COI charge at attained age 91 overtakes a level
# $150 a month.
SHORTFALL = {
    1: (1032, 0, None),
    2: (1032, 356, 676),
    3: (912, 0, None),
}


def _wd_ten_percent_monthly(t):
    """Withdraw 10% of the account value every month from the first anniversary.

    Used to override ``wd_pp`` - no shipped model point withdraws anything, and this is
    the pattern that exposes a monthly rather than annual free-withdrawal allowance.
    The first anniversary is the start of policy month ``t = 12``.
    """
    return 0.10 * av_pp_at(t, "BEF_WD") if t >= 12 else 0.0          # noqa: F821


def _premium_far_above_the_seven_pay_limit():
    """A planned annual premium that fails the 7-pay test in policy year 1."""
    return 24000.0


@pytest.fixture(scope="module")
def universal_life():
    """The UL_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(universal_life):
    """Model point 1 - the worked-example anchor cell."""
    return universal_life.Projection[1]


@pytest.fixture(scope="module")
def option_b(universal_life):
    """Model point 2 - the anchor cell switched to death benefit Option B."""
    return universal_life.Projection[2]


@pytest.fixture(scope="module")
def in_force(universal_life):
    """Model point 3 - an in-force cell at 120 completed months, with a policy loan."""
    return universal_life.Projection[3]


@pytest.fixture(scope="module")
def withdrawing():
    """The anchor cell in a separate model, withdrawing 10% of its account value a month.

    A separate model instance because overriding a formula mutates the Space for every
    ItemSpace under it; the shared ``universal_life`` fixture must stay as shipped.
    """
    model = mx.read_model(MODEL_PATH, name="UL_US_S_wd")
    model.Projection.wd_pp.formula = _wd_ten_percent_monthly
    yield model.Projection[1]
    model.close()


@pytest.fixture(scope="module")
def over_funded():
    """The anchor cell in a separate model, paying $24,000 a year instead of $1,800."""
    model = mx.read_model(MODEL_PATH, name="UL_US_S_mec")
    model.Projection.premium_pp_ann.formula = _premium_far_above_the_seven_pay_limit
    yield model.Projection[1]
    model.close()


# ---------------------------------------------------------------------------
# The worked example

@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, t):
    """Every cell of the notes' three-row table, to the displayed precision."""
    av_prev, np_, av_dash, db, naar, coi, md, av_bef_inv, interest, av = WORKED_EXAMPLE[t]
    assert anchor.av_pp_at(t, "BEF_PREM") == pytest.approx(av_prev, abs=CENT)
    assert anchor.prem_to_av_pp(t) == pytest.approx(np_, abs=CENT)
    assert anchor.av_pp_at(t, "BEF_FEE") == pytest.approx(av_dash, abs=CENT)
    assert anchor.db_pp(t) == pytest.approx(db, abs=CENT)
    assert anchor.net_amt_at_risk(t) == pytest.approx(naar, abs=CENT)
    assert anchor.coi_pp(t) == pytest.approx(coi, abs=CENT)
    assert anchor.mth_deduction_pp(t) == pytest.approx(md, abs=CENT)
    assert anchor.av_pp_at(t, "BEF_INV") == pytest.approx(av_bef_inv, abs=CENT)
    assert anchor.inv_income_pp(t) == pytest.approx(interest, abs=CENT)
    assert anchor.av_pp(t) == pytest.approx(av, abs=CENT)


def test_worked_example_trace(anchor):
    """The full-precision trace the notes print under the table, at t = 0."""
    assert anchor.inv_return_mth(0) == pytest.approx(TRACE["i_m"], abs=5e-8)
    assert anchor.naar_factor() == pytest.approx(TRACE["naar_factor"], abs=5e-8)
    assert anchor.db_pp(0) / anchor.naar_factor() == pytest.approx(
        TRACE["db_discounted"], abs=CENT)
    assert anchor.coi_rate_guar(0) == pytest.approx(TRACE["coi_rate_guar_yr1"], abs=5e-6)
    assert anchor.coi_rate(0) == pytest.approx(TRACE["coi_rate_yr1"], abs=5e-7)
    assert anchor.coi_pp(0) == pytest.approx(TRACE["coi_pp_0"], abs=5e-5)
    assert anchor.mth_deduction_pp(0) == pytest.approx(
        TRACE["mth_deduction_pp_0"], abs=5e-5)
    # The corridor minimum in the issue month is 2.50 x AV', far below the $100,000 face.
    assert (anchor.corridor_factor(0) * anchor.av_pp_at(0, "BEF_FEE")
            == pytest.approx(TRACE["corridor_min_0"], abs=CENT))
    assert anchor.db_pp(0) == 100000.0


def test_worked_example_charge_components(anchor):
    """NP = 141.00, e_pol = 7.50, e_unit x U = 26.00, and MD is their sum plus COI."""
    assert anchor.premium_pp(0) == pytest.approx(150.00, abs=CENT)
    assert anchor.load_prem_rate() == 0.06
    assert anchor.prem_to_av_pp(0) == pytest.approx(141.00, abs=CENT)
    assert anchor.units(0) == 100.0
    assert anchor.maint_fee_pp(0) == pytest.approx(7.50 + 26.00, abs=CENT)
    assert anchor.rider_charge_pp(0) == 0.0
    assert anchor.mth_deduction_pp(0) == pytest.approx(
        anchor.maint_fee_pp(0) + anchor.coi_pp(0), rel=1e-12)


def test_policy_date_rule(anchor):
    """AV on the policy date is net premium less the first monthly deduction [S3].

    The opening balance of the issue month is the model point's ``av_pp_init()``,
    read through the ``"BEF_PREM"`` timing; ``av_pp(0)`` is the *closing* balance of
    the issue month and is not zero.
    """
    assert anchor.av_pp_at(0, "BEF_PREM") == 0.0
    assert anchor.av_pp_at(0, "BEF_INV") == pytest.approx(
        anchor.prem_to_av_pp(0) - anchor.mth_deduction_pp(0), rel=1e-12)
    assert anchor.av_pp(0) > 0.0


def test_no_grace_in_the_issue_month(anchor):
    """The notes' issue-month shortfall test: AV' (141.00) >= MD (39.54), no grace."""
    assert anchor.is_shortfall(0) is False
    assert anchor.av_pp_at(0, "BEF_FEE") == pytest.approx(141.00, abs=CENT)
    assert anchor.mth_deduction_pp(0) == pytest.approx(39.54, abs=CENT)


# ---------------------------------------------------------------------------
# One test per entry in the notes' "Known modeling pitfalls"

def test_pitfall_deduction_before_interest(anchor):
    """Interest is credited on the post-deduction balance, not before it.

    Reversing the order overstates the account value by about one month's interest on
    the deduction every month and compounds over decades.
    """
    for t in (0, 1, 2, 59, 239):
        correct = (anchor.av_pp_at(t, "BEF_FEE") - anchor.mth_deduction_pp(t)) * (
            1 + anchor.inv_return_mth(t))
        assert anchor.av_pp(t) == pytest.approx(correct, rel=1e-12)
        reversed_order = (anchor.av_pp_at(t, "BEF_FEE") * (1 + anchor.inv_return_mth(t))
                          - anchor.mth_deduction_pp(t))
        assert reversed_order > anchor.av_pp(t)


def test_pitfall_naar_uses_guaranteed_rate_and_pre_deduction_av(anchor):
    """NAAR discounts DB at the *guaranteed* rate off the *pre-deduction* AV [S3]."""
    t = 0
    assert anchor.naar_factor() == pytest.approx(1.02 ** (1 / 12), rel=1e-14)
    assert anchor.net_amt_at_risk(t) == pytest.approx(
        anchor.db_pp(t) / anchor.naar_factor() - anchor.av_pp_at(t, "BEF_FEE"),
        rel=1e-12)
    # Using the credited rate in the discount, or the post-deduction account value,
    # both move the answer - which is exactly the systematic COI error the notes warn
    # about.
    with_credited = (anchor.db_pp(t) / (1 + anchor.inv_return_mth(t))
                     - anchor.av_pp_at(t, "BEF_FEE"))
    with_post_deduction = (anchor.db_pp(t) / anchor.naar_factor()
                           - anchor.av_pp_at(t, "BEF_INV"))
    assert abs(with_credited - anchor.net_amt_at_risk(t)) > 1.0
    assert abs(with_post_deduction - anchor.net_amt_at_risk(t)) > 1.0


def test_pitfall_option_b_corridor_has_no_simultaneity(option_b):
    """Under Option B, DB and NAAR both key off AV', so nothing is circular."""
    assert option_b.db_option() == "B"
    t = 0
    av_dash = option_b.av_pp_at(t, "BEF_FEE")
    assert option_b.db_pp(t) == pytest.approx(
        max(option_b.sum_assured_at(t) + av_dash,
            option_b.corridor_factor(t) * av_dash), rel=1e-12)
    assert option_b.db_pp(t) == pytest.approx(100000.0 + av_dash, rel=1e-12)
    assert option_b.net_amt_at_risk(t) > option_b.net_amt_at_risk(t) - 1  # finite
    assert option_b.result_av().shape[0] == option_b.proj_len()


def test_pitfall_corridor_binds_when_the_policy_is_well_funded(anchor):
    """The corridor is not decoration: at high attained ages it lifts the benefit."""
    binding = [t for t in range(anchor.proj_len())
               if anchor.db_pp(t) > anchor.sum_assured_at(t) + CENT]
    assert binding, "the GPT corridor never binds - check corridor_factors.csv"
    t = binding[0]
    assert anchor.db_pp(t) == pytest.approx(
        anchor.corridor_factor(t) * anchor.av_pp_at(t, "BEF_FEE"), rel=1e-12)


def test_pitfall_monthly_not_daily_compounding(anchor):
    """Twelve monthly credits compound back to the declared annual rate exactly."""
    assert (1 + anchor.inv_return_mth(0)) ** 12 == pytest.approx(1.04, rel=1e-14)
    assert (1 + anchor.guar_rate_mth()) ** 12 == pytest.approx(1.02, rel=1e-14)
    daily = (1 + 0.04) ** (1 / 365)
    assert (daily ** 30 - 1) != pytest.approx(anchor.inv_return_mth(0), abs=1e-6)


def test_pitfall_anb_age_changes_on_the_anniversary(anchor):
    """Attained age is x + y - 1: it steps on the policy anniversary, not monthly.

    ``t = 0 .. 11`` is policy year 1 at age 35; the first anniversary is the start of
    ``t = 12``, policy year 2, age 36.
    """
    assert anchor.age(0) == 35
    assert anchor.age(11) == 35
    assert anchor.age(12) == 36
    assert anchor.policy_year(0) == 1
    assert anchor.policy_year(11) == 1
    assert anchor.policy_year(12) == 2
    assert anchor.duration_mth(0) == 0
    assert anchor.duration_mth(12) == 12
    assert anchor.duration(11) == 0
    assert anchor.duration(12) == 1


def test_pitfall_era_the_coi_table_is_the_specimen_scale(anchor):
    """The guaranteed COI anchors are the specimen's own printed values [S3].

    ``coi_rate_guar`` is indexed by policy *month*, so each policy year y is read at
    its first month, ``t = 12 * (y - 1)``.
    """
    def m(y):
        return 12 * (y - 1)

    assert anchor.coi_rate_guar(m(1)) == pytest.approx(0.10090, abs=5e-6)
    assert anchor.coi_rate_guar(m(5)) == pytest.approx(0.12840, abs=5e-6)
    assert anchor.coi_rate_guar(m(10)) == pytest.approx(0.19940, abs=5e-6)
    assert anchor.coi_rate_guar(m(20)) == pytest.approx(0.45950, abs=5e-6)
    assert anchor.coi_rate_guar(m(77)) == pytest.approx(77.62690, abs=5e-6)
    # attained ages 112-120: a single month's charge equals the whole NAAR
    assert anchor.coi_rate_guar(m(78)) == pytest.approx(1000 / 12, abs=5e-5)
    assert anchor.coi_rate_guar(m(86)) == pytest.approx(1000 / 12, abs=5e-5)
    # interpolated years sit strictly between their anchors
    assert 0.10090 < anchor.coi_rate_guar(m(3)) < 0.12840
    # the current scale is 60% of the guaranteed maximum at every duration
    for y in (1, 5, 20, 60):
        assert anchor.coi_rate(m(y)) == pytest.approx(
            0.60 * anchor.coi_rate_guar(m(y)), rel=1e-12)


def test_pitfall_mec_and_gpt_are_flags_not_cash_flows(anchor):
    """Compliance tests cap or flag; they never generate a cash flow of their own."""
    assert anchor.gpt_limit(0) == pytest.approx(max(34138.15, 2825.52), abs=CENT)
    assert anchor.gpt_limit(119) == pytest.approx(          # last month of policy year 10
        max(34138.15, 2825.52 * 10), abs=CENT)
    assert anchor.seven_pay_limit(0) == pytest.approx(6702.10, abs=CENT)
    assert anchor.seven_pay_limit(199) == pytest.approx(7 * 6702.10, abs=CENT)
    assert all(anchor.gpt_ok(t) for t in range(199))
    assert not any(anchor.is_mec(t) for t in range(199))
    for t in (0, 11, 99):
        assert anchor.net_cf(t) == pytest.approx(
            anchor.premiums(t) - anchor.claims(t) - anchor.withdrawals(t)
            - anchor.expenses(t) - anchor.premium_taxes(t), rel=1e-12)


def test_pitfall_surrender_charge_month_index(anchor):
    """SC(t) = max(0, 9.00 - (t + 1)/12) x U: the run-off counts the current month.

    One twelfth of a year is already amortized in the issue month ``t = 0``, so the
    charge there is $8.916667 per $1,000, not $9.00; it reaches $8.00 at ``t = 11``,
    the last month of policy year 1, and zero at ``t = 107``, the last month of policy
    year 9.  Using ``duration_mth(t)`` alone shifts the whole schedule by a month.
    """
    assert anchor.surr_charge_rate(0) == pytest.approx(9.00 - 1 / 12, rel=1e-12)
    assert anchor.surr_charge_pp(0) == pytest.approx(100 * (9.00 - 1 / 12), abs=CENT)
    assert anchor.surr_charge_rate(11) == pytest.approx(8.00, rel=1e-12)
    assert anchor.surr_charge_rate(106) == pytest.approx(9.00 - 107 / 12, rel=1e-12)
    assert anchor.surr_charge_rate(107) == 0.0
    assert anchor.surr_charge_pp(199) == 0.0


# ---------------------------------------------------------------------------
# Roll-forwards and invariants

def test_av_roll_forward_closes(anchor, option_b, in_force):
    for proj in (anchor, option_b, in_force):
        assert proj.check_av_roll_fwd() is True


def test_margin_identity_holds(anchor, option_b, in_force):
    """net_cf = expense margin + mortality margin + av_change - inv_income + loan."""
    for proj in (anchor, option_b, in_force):
        assert proj.check_margin() is True


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + maturities, every month."""
    assert anchor.pols_if(0) == anchor.pols_if_init()
    for t in range(anchor.proj_len()):
        out = anchor.pols_death(t) + anchor.pols_lapse(t) + anchor.pols_maturity(t)
        assert anchor.pols_if(t) - anchor.pols_if(t + 1) == pytest.approx(
            out, abs=1e-15)


def test_no_maturity_on_this_contract(anchor):
    """Universal life has no maturity date [S2][S3]; the projection ends on mortality.

    ``proj_len()`` counts the months projected, so the last row is
    ``t = proj_len() - 1``, the last month at attained age 120, where the annual
    mortality rate is 1.0; the count in force at the start of the month after it,
    ``pols_if(proj_len())``, is zero.
    """
    assert all(anchor.pols_maturity(t) == 0.0
               for t in range(0, anchor.proj_len(), 37))
    assert anchor.proj_len() == 12 * (120 - 35 + 1)
    assert anchor.age(anchor.proj_len() - 1) == 120
    assert anchor.age(anchor.proj_len() - 12) == 120
    assert anchor.age(anchor.proj_len() - 13) == 119
    assert anchor.pols_if(anchor.proj_len()) == pytest.approx(0.0, abs=1e-12)


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(anchor.proj_len()):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


def test_death_before_lapse(anchor):
    """The [std] decrement order: lapses act on the survivors of the month's deaths."""
    t = 24
    assert anchor.pols_death(t) == pytest.approx(
        anchor.pols_if(t) * anchor.mort_rate_mth(t), rel=1e-12)
    assert anchor.pols_lapse(t) == pytest.approx(
        anchor.pols_if(t) * (1 - anchor.mort_rate_mth(t))
        * anchor.lapse_rate_mth(t), rel=1e-12)


def test_lapse_shock_at_surrender_charge_expiry(anchor):
    """M_sc = 2.0 in policy year 10, the first year with no surrender charge.

    Policy year 10 is ``t = 108 .. 119``; ``t = 107`` is the last month of year 9 and
    ``t = 120`` the first of year 11.
    """
    assert anchor.lapse_shock_year() == 10
    assert anchor.lapse_rate_base(108) == pytest.approx(0.04, abs=1e-12)
    assert anchor.lapse_rate_sc_mult(107) == 1.0          # policy year 9
    assert anchor.lapse_rate_sc_mult(108) == 2.0          # policy year 10
    assert anchor.lapse_rate_sc_mult(119) == 2.0          # still policy year 10
    assert anchor.lapse_rate_sc_mult(120) == 1.0          # policy year 11
    assert anchor.lapse_rate(108) == pytest.approx(0.08, abs=1e-12)
    assert anchor.lapse_rate(120) == pytest.approx(0.03, abs=1e-12)


def test_dynamic_lapse_is_neutral_in_the_base_run(anchor):
    """r_comp = i_cr in the base deterministic run, so M_rate = 1 throughout."""
    for t in (0, 59, 599):
        assert anchor.comp_rate_ann(t) == anchor.crediting_rate_ann(t)
        assert anchor.lapse_rate_dyn_mult(t) == 1.0


def test_premium_persistency_scale(anchor):
    """pp(y): 100% in year 1, -2pp a year, 70% floor from year 16."""
    assert anchor.prem_persistency(0) == pytest.approx(1.00)
    assert anchor.prem_persistency(11) == pytest.approx(1.00)     # still policy year 1
    assert anchor.prem_persistency(12) == pytest.approx(0.98)     # policy year 2
    assert anchor.prem_persistency(12 * 14) == pytest.approx(0.72)   # year 15
    assert anchor.prem_persistency(12 * 15) == pytest.approx(0.70)   # year 16
    assert anchor.prem_persistency(12 * 30) == pytest.approx(0.70)   # floor
    assert anchor.premium_pp(12) == pytest.approx(1800 / 12 * 0.98, abs=CENT)


def test_charges_and_premiums_cease_at_attained_age_121(anchor):
    """From attained age 121 the deduction is zero and premiums are not accepted."""
    far = 12 * (121 - 35)                         # first month at attained age 121
    assert anchor.age(far - 1) == 120
    assert anchor.age(far) == 121
    assert anchor.mth_deduction_pp(far) == 0.0
    assert anchor.coi_pp(far) == 0.0
    assert anchor.maint_fee_pp(far) == 0.0
    assert anchor.premium_pp(far) == 0.0
    assert anchor.wd_pp(far) == 0.0


def test_per_unit_charge_steps_down_after_year_ten(anchor):
    """$0.26 per $1,000 a month in policy years 1-10, $0.156 from year 11 [S3].

    ``t = 119`` is the last month of policy year 10 and ``t = 120`` the first of year 11.
    """
    assert anchor.maint_fee_pp(119) == pytest.approx(7.50 + 0.26 * 100, abs=CENT)
    assert anchor.maint_fee_pp(120) == pytest.approx(7.50 + 0.156 * 100, abs=CENT)


def test_loan_rolls_forward_at_the_charged_rate(in_force):
    """L(t) = L(t-1) x (1 + 2.75%)^(1/12), from the model point's opening balance.

    ``loan_bal_pp_bom(0)`` is the opening balance; ``loan_bal_pp(t)`` is the closing
    balance of month ``t``, so twelve months of accrual is ``loan_bal_pp(11)``.
    """
    assert in_force.loan_bal_pp_bom(0) == 2000.0
    assert in_force.loan_bal_pp(0) == pytest.approx(2000.0 * 1.0275 ** (1 / 12), rel=1e-12)
    assert in_force.loan_bal_pp(11) == pytest.approx(2000.0 * 1.0275, rel=1e-12)
    assert in_force.loan_bal_pp_bom(12) == in_force.loan_bal_pp(11)
    assert in_force.ncsv_pp(0) == pytest.approx(
        in_force.csv_pp(0) - in_force.loan_bal_pp(0), abs=CENT)
    # the loaned slice of the account value earns the guaranteed rate, not the current
    for t in (0, 1):
        unloaned = in_force.av_pp_at(t, "BEF_INV") - in_force.loan_bal_pp_bom(t)
        assert in_force.inv_income_pp(t) == pytest.approx(
            unloaned * in_force.inv_return_mth(t)
            + in_force.loan_bal_pp_bom(t) * in_force.guar_rate_mth(), rel=1e-12)


def test_in_force_model_point_starts_at_its_duration(in_force):
    """Model point 3 opens 120 completed months in, with no surrender charge left.

    Its frame still starts at ``t = 0``; the elapsed months are carried by
    ``duration_mth_init()``, so ``duration_mth(0) == 120`` and the first projected month
    is the first month of policy year 11.
    """
    assert in_force.duration_mth_init() == 120
    assert in_force.duration_mth(0) == 120
    assert in_force.policy_year(0) == 11
    assert in_force.age(0) == 45
    assert in_force.proj_len() == 12 * (120 - 35 + 1) - 120
    assert list(in_force.result_cf().index) == list(range(in_force.proj_len()))
    assert in_force.surr_charge_pp(0) == 0.0
    assert in_force.av_pp_at(0, "BEF_PREM") == 15000.0
    assert in_force.av_pp(0) > 15000.0
    assert in_force.wd_used_year(0) == 0.0


def test_csv_floor_binds_while_the_surrender_charge_exceeds_the_account_value(anchor):
    """Early on the scheduled charge is larger than the fund, so NCSV is zero."""
    assert anchor.surr_charge_pp(0) > anchor.av_pp(0)
    assert anchor.csv_pp(0) == 0.0
    assert anchor.ncsv_pp(0) == 0.0
    assert anchor.claims(0, "LAPSE") == 0.0
    # the charge actually collected is capped by the account value
    assert anchor.surr_charge(0) == pytest.approx(
        anchor.av_pp(0) * anchor.pols_lapse(0), rel=1e-12)
    # and later the fund overtakes the schedule
    assert anchor.ncsv_pp(119) > 0.0


def test_death_benefit_never_falls_below_the_face_amount(universal_life):
    """DB >= F, and no death claim is ever negative, in every month of every point.

    The notes set the Option B death benefit to ``F + AV'(t)`` on the premise that
    ``AV'`` is a real account balance.  It is not one for model point 2 past ``t = 676``:
    the grace cascade is not implemented, so nothing terminates a policy in permanent
    shortfall and its account value runs to about -$1.84m.  Taken literally the formula
    then pays a death benefit below the face amount, and eventually a negative one - a
    death claim collected *from* the beneficiary.  ``av_pp_db_basis`` floors the balance
    at zero **[std]** so that cannot happen.
    """
    for point_id in universal_life.Data.model_point_table().index:
        proj = universal_life.Projection[point_id]
        for t in range(proj.proj_len()):
            assert proj.db_pp(t) >= proj.sum_assured_at(t) - 1e-9, (point_id, t)
            assert proj.claim_pp(t, "DEATH") >= 0.0, (point_id, t)
        assert (proj.result_cf()["claims_death"] >= 0.0).all(), point_id

    # The floor is load-bearing, not decoration: point 2's AV' really does go negative,
    # and it is the floor alone that holds the death benefit at the face amount there.
    option_b = universal_life.Projection[2]
    t = 699
    assert option_b.av_pp_at(t, "BEF_FEE") < 0.0
    assert option_b.av_pp_db_basis(t) == 0.0
    assert option_b.db_pp(t) == pytest.approx(option_b.sum_assured_at(t), rel=1e-12)
    assert option_b.net_amt_at_risk(t) == pytest.approx(
        option_b.db_pp(t) / option_b.naar_factor(), rel=1e-12)
    # and where AV' is positive the floor changes nothing, so the worked example stands
    assert option_b.av_pp_at(0, "BEF_FEE") > 0.0
    assert option_b.av_pp_db_basis(0) == option_b.av_pp_at(0, "BEF_FEE")
    assert option_b.db_pp(0) == pytest.approx(
        100000.0 + option_b.av_pp_at(0, "BEF_FEE"), rel=1e-12)


def test_shortfall_trigger_is_live_on_point_2_and_inert_on_1_and_3(universal_life):
    """The grace trigger over the *whole* projection, model point by model point.

    The notes' grace and lapse-for-insufficiency cascade is not implemented, so this is
    a diagnostic - but it is not inert, and the README carries the same table.  Points 1
    and 3 never trigger it; point 2 is in shortfall from ``t = 676`` (policy year 57,
    attained age 91) to the end, and nothing terminates it.
    """
    for point_id, (length, count, first) in SHORTFALL.items():
        proj = universal_life.Projection[point_id]
        assert proj.proj_len() == length, point_id
        months = [t for t in range(length) if proj.is_shortfall(t)]
        assert len(months) == count, (point_id, len(months))
        if first is None:
            assert months == [], point_id
        else:
            # contiguous, from the first trigger to the end of the projection
            assert months == list(range(first, length)), point_id
            assert proj.policy_year(first) == 57
            assert proj.age(first) == 91
            assert (proj.av_pp_at(first, "BEF_FEE") - proj.loan_bal_pp_bom(first)
                    < proj.mth_deduction_pp(first))

    # No policy is terminated for insufficiency: point 2's in force keeps running off on
    # mortality and lapse alone, exactly as the funded points do.
    option_b = universal_life.Projection[2]
    for t in (675, 699, 899):
        assert option_b.pols_if(t + 1) == pytest.approx(
            option_b.pols_if(t) - option_b.pols_death(t) - option_b.pols_lapse(t),
            rel=1e-12)


def test_free_withdrawal_allowance_is_annual_not_monthly(withdrawing):
    """10% of the account value is a *policy year's* allowance, not a month's.

    The notes' step 3 applies the free-amount rule "10% of AV per policy year" and their
    state variables table carries ``wd_used_year``.  Granted afresh every month, twelve
    monthly withdrawals of 10% of the account value would consume twelve full annual
    allowances and force no Option A face reduction at all.
    """
    proj = withdrawing
    # First withdrawal of policy year 2 (t = 12, the first anniversary): nothing used
    # yet, so the whole 10% is free.
    assert proj.wd_pp(11) == 0.0
    assert proj.wd_used_year(12) == 0.0
    assert proj.wd_free_pp(12) == pytest.approx(
        0.10 * proj.av_pp_at(12, "BEF_WD"), rel=1e-12)
    assert proj.wd_pp(12) == pytest.approx(proj.wd_free_pp(12), rel=1e-12)
    assert proj.face_reduction_pp(12) == 0.0
    assert proj.sum_assured_at(12) == 100000.0

    # Every later month of the *same* policy year (t = 13 .. 23): the allowance is
    # spent, so the whole withdrawal is chargeable and cuts the face.
    spent = proj.wd_pp(12)
    for t in range(13, 24):
        assert proj.wd_used_year(t) == pytest.approx(spent, rel=1e-12), t
        assert proj.wd_free_pp(t) == 0.0, t
        assert proj.face_reduction_pp(t) == pytest.approx(proj.wd_pp(t), rel=1e-12), t
    assert proj.sum_assured_at(23) < 100000.0
    assert proj.units(23) == pytest.approx(proj.sum_assured_at(23) / 1000, rel=1e-12)

    # And it resets on the policy anniversary, t = 24.
    assert proj.wd_used_year(24) == 0.0
    assert proj.wd_free_pp(24) == pytest.approx(
        0.10 * proj.av_pp_at(24, "BEF_WD"), rel=1e-12)
    assert proj.face_reduction_pp(24) == 0.0
    assert proj.face_reduction_pp(25) > 0.0


def test_mec_flag_latches_once_the_seven_pay_test_fails(over_funded, anchor):
    """MEC status is permanent under IRC 7702A, so ``is_mec`` must not switch itself off.

    The in-year test only applies in the first seven policy years; an unlatched flag
    reverts to ``False`` in policy year 8, which is exactly when the failure becomes
    permanent.  The notes ask the base model to "flag (does not project) 7-pay failures".
    """
    proj = over_funded
    assert proj.premium_pp_ann() == 24000.0
    assert proj.seven_pay_prem() == pytest.approx(6702.10, abs=CENT)

    # It fails in policy year 1 (t = 0 .. 11) and the flag is set from then on.
    assert proj.cum_prem_pp(11) > proj.seven_pay_limit(11)
    assert proj.is_mec(11) is True
    # Policy year 8 (t = 84 .. 95): the in-year test no longer applies, but the contract
    # is still a MEC.
    assert proj.policy_year(95) == 8
    assert proj.seven_pay_limit(95) == pytest.approx(7 * 6702.10, abs=CENT)
    assert proj.policy_year(95) > 7
    assert proj.is_mec(95) is True
    assert all(proj.is_mec(t) for t in (84, 95, 299, proj.proj_len() - 1))
    # The flag is still a flag: it moves no cash flow.
    assert proj.net_cf(95) == pytest.approx(
        proj.premiums(95) - proj.claims(95) - proj.withdrawals(95)
        - proj.expenses(95) - proj.premium_taxes(95), rel=1e-12)
    # And a contract inside the limit never trips it.
    assert not any(anchor.is_mec(t) for t in range(0, anchor.proj_len(), 29))


def test_withdrawals_are_off_but_the_mechanics_are_wired(anchor):
    """No shipped model point withdraws; the fee, free amount and face cut are live."""
    assert all(anchor.wd_pp(t) == 0.0 for t in (0, 12, 119, 599))
    assert anchor.wd_fee_pp(12) == 0.0
    assert anchor.face_reduction_pp(12) == 0.0
    assert anchor.sum_assured_at(599) == 100000.0
    assert all(anchor.withdrawals(t) == 0.0 for t in (0, 12, 119))
    assert anchor.wd_pp(5) == 0.0            # before the first anniversary anyway
    assert anchor.wd_used_year(12) == 0.0     # nothing withdrawn, nothing used
    assert anchor.wd_free_pp(12) == pytest.approx(
        0.10 * anchor.av_pp_at(12, "BEF_WD"), rel=1e-12)


def test_a_withdrawal_is_not_a_claim(withdrawing):
    """``withdrawals`` is its own cash flow line, and ``claims`` does not carry it.

    A partial withdrawal is a payment on the owner's election, not a claim on a
    contingency, so it is weighted by the in force at BOM rather than by a decrement,
    it has its own ``result_cf()`` column, and ``"WITHDRAWAL"`` is not a ``kind`` of
    ``claims`` or ``claim_pp``.  Asserted on the withdrawing model point, where the
    amounts are non-zero and a double count would show.
    """
    proj = withdrawing
    t = 12
    assert proj.wd_pp(t) > 0.0
    assert proj.withdrawals(t) == pytest.approx(proj.wd_pp(t) * proj.pols_if(t),
                                                rel=1e-12)
    # not a kind, and not inside the kind-less total
    for call in (lambda: proj.claims(t, "WITHDRAWAL"),
                 lambda: proj.claim_pp(t, "WITHDRAWAL")):
        with pytest.raises(Exception) as excinfo:
            call()
        assert "invalid kind" in str(excinfo.value)
    assert proj.claims(t) == pytest.approx(
        proj.claims(t, "DEATH") + proj.claims(t, "LAPSE"), rel=1e-12)
    # and net_cf still nets it, so the ruling moved no money
    assert proj.net_cf(t) == pytest.approx(
        proj.premiums(t) - proj.claims(t) - proj.withdrawals(t)
        - proj.expenses(t) - proj.premium_taxes(t), rel=1e-12)


def test_the_cash_flow_columns_sum_to_net_cf(anchor, option_b, in_force):
    """``net_cf`` is income-positive: premiums less every other flow column."""
    for proj in (anchor, option_b, in_force):
        df = proj.result_cf()
        outgo = (df["claims_death"] + df["claims_lapse"] + df["withdrawals"]
                 + df["expenses"] + df["premium_taxes"])
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9)


def test_pols_if_is_the_start_of_month_weight(anchor, in_force):
    """The reconciliation ``premiums(t) / premium_pp(t) == pols_if(t)``.

    ``pols_if(t)`` is the count in force at the **start** of policy month t, and it is
    the weight applied to that same row's BOM cash flows, so the in-force column of
    ``result_cf()`` reconciles with the row it sits on.
    """
    for proj in (anchor, in_force):
        df = proj.result_cf()
        for t in (0, 1, 12, 119):
            assert proj.premium_pp(t) > 0.0
            assert proj.premiums(t) / proj.premium_pp(t) == pytest.approx(
                proj.pols_if(t), rel=1e-12)
            assert df.loc[t, "pols_if"] == pytest.approx(proj.pols_if(t), rel=1e-12)
        assert proj.pols_if(0) == proj.pols_if_init()
        assert df.loc[0, "pols_if"] == proj.pols_if_init()
        assert all(proj.pols_if_at(0, timing) == proj.pols_if(0)
                   for timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"))


# ---------------------------------------------------------------------------
# Structure

def test_result_cf_shape(anchor):
    """The frame is ``t = 0 .. proj_len() - 1``, ``proj_len()`` rows, indexed by ``t``."""
    df = anchor.result_cf()
    assert list(df.index) == list(range(anchor.proj_len()))
    assert df.index[0] == 0
    assert df.index[-1] == anchor.proj_len() - 1
    assert len(df) == anchor.proj_len()
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "withdrawals",
        "expenses", "premium_taxes", "net_cf",
    ]
    assert df.loc[0, "premiums"] == pytest.approx(150.00, abs=CENT)


def test_result_av_mirrors_the_worked_example_columns(anchor):
    """result_av() prints the notes' table in the notes' order, from t = 0."""
    df = anchor.result_av()
    assert df.index.name == "t"
    assert list(df.index) == list(range(anchor.proj_len()))
    assert list(df.columns)[:10] == [
        "av_pp_bef_prem", "prem_to_av_pp", "av_pp_bef_fee", "db_pp",
        "net_amt_at_risk", "coi_pp", "mth_deduction_pp", "av_pp_bef_inv",
        "inv_income_pp", "av_pp",
    ]
    for t, row in WORKED_EXAMPLE.items():
        assert list(df.loc[t][:10]) == pytest.approx(list(row), abs=CENT)


def test_result_pols_shape(anchor):
    df = anchor.result_pols()
    assert set(df.columns) == {
        "pols_if", "pols_death", "pols_lapse", "pols_maturity",
        "mort_rate_mth", "lapse_rate_mth",
    }
    assert len(df) == anchor.proj_len()
    assert list(df.index) == list(range(anchor.proj_len()))
    assert df.loc[0, "pols_if"] == anchor.pols_if_init()


def test_invalid_arguments_raise(anchor):
    """Unknown timing/kind strings raise, as in CashValue_SE.

    modelx wraps a formula exception in a FormulaError, so the test looks at the
    message rather than the exception class.
    """
    cases = [
        (lambda: anchor.av_pp_at(0, "NOPE"), "invalid timing"),
        (lambda: anchor.av_at(0, "NOPE"), "invalid timing"),
        (lambda: anchor.pols_if_at(0, "NOPE"), "invalid timing"),
        (lambda: anchor.claim_pp(0, "NOPE"), "invalid kind"),
        (lambda: anchor.claims(0, "NOPE"), "invalid kind"),
        (lambda: anchor.claims_from_av(0, "NOPE"), "invalid kind"),
    ]
    for call, message in cases:
        with pytest.raises(Exception) as excinfo:
            call()
        assert message in str(excinfo.value)


def test_model_docstring_names_what_is_not_implemented(universal_life):
    """The absences a reader must know about are in the docstring, not just the README."""
    doc = universal_life.doc
    assert "current-assumption universal life" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc
    assert "once per model" in doc
    assert "Not implemented" in doc
    for gap in ("grace", "Reinstatement", "NGE revision", "Riders"):
        assert gap in doc, gap
