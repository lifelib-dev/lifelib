"""Golden and product tests for MYGA_US_S.

The golden values are the worked example in
products/fixed_deferred_annuity/technical-notes.md ("Worked example"), which projects
the anchor cell M60 ANB / non-qualified / $100,000 single premium / 5-year guarantee
period / 4.45% declared / 2.80% GMSV rate / 9-8-7-6-5 surrender charge / 10% free
withdrawal.  They are hard-coded here rather than pickled so that a reviewer can compare
them against the notes by eye.

Three blocks are asserted: the seven-row account value and Model #805 floor table; the
full surrender trace at the end of month 30 (contract year 3, MVA reference yield 6.50%,
neither the cap nor the floor binding); and the full surrender trace at the end of month
6 under the 10.00% stress yield, where the symmetric cap **and** the nonforfeiture floor
both bind.  The first two run on model point 1, the third on model point 2, which is the
same contract on the stress scenario.

The notes' own "Known modeling pitfalls" list is a test list in disguise; there is one
test per entry below.
"""
import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/fixed_deferred_annuity/MYGA_US_S"

# Half a cent, plus a hair.  The notes round half-up for display and AV(24) =
# 104,920.025 sits exactly on the boundary (shown as 104,920.03), so a strict 0.005 would
# fail on a value that is right to the twelfth significant figure.
CENT = 0.006

# The notes state that "the surrender traces below are computed from the cent-rounded
# values shown, so they reproduce by hand".  One quantity is visibly affected: E(30) is
# printed as AV(30) - FW = 107,229.09 - 10,492.00 = 96,737.09 where full precision gives
# 96,737.0843.  This tolerance covers that and nothing larger.
ROUNDED = 0.01

INFORCE = 5e-7          # in-force probabilities

# Worked example, "Worked example" table.
# t: (AV(t-1), W(t), AV'(t), AV(t), MGSV(t))
WORKED_EXAMPLE = {
    1:  (100000.00,    0.00, 100000.00, 100363.48, 87701.59),
    2:  (100363.48,    0.00, 100363.48, 100728.28, 87903.65),
    3:  (100728.28,    0.00, 100728.28, 101094.40, 88106.17),
    12: (104071.72,    0.00, 104071.72, 104450.00, 89950.00),
    13: (104450.00, 4000.00, 100450.00, 100815.11, 86148.02),
    24: (104540.04,    0.00, 104540.04, 104920.03, 88356.60),
    30: (106840.74,    0.00, 106840.74, 107229.09, 89585.05),
}

# Worked example, "Surrender trace, end of month 30" -- model point 1, it = 6.50%.
SURRENDER_30 = {
    "free_wd": 10492.00,
    "excess": 96737.09,
    "charge": 6771.60,
    "mva_term": 2.5,
    "mva_rate": -0.037500,
    "mva_raw": -3627.64,
    "mva": -3627.64,          # symmetric cap |M| <= C = 6,771.60, not binding
    "surr_value": 96829.85,
    "mgsv": 89585.05,         # floor not binding
    "benefit": 96829.85,
    "charged_excess": 86337.85,
}

# Worked example, "A case where the floor binds" -- model point 2, it = 10.00%.
SURRENDER_6 = {
    "av": 102200.78,
    "free_wd": 10000.00,      # year-1 base is purchase payments
    "excess": 92200.78,
    "charge": 8298.07,
    "mva_term": 4.5,
    "mva_rate": -0.225,
    "mva_raw": -20745.18,
    "mva": -8298.07,          # capped by the symmetric rule
    "surr_value": 85604.64,
    "mgsv": 88716.54,
    "benefit": 88716.54,      # the Model #805 floor binds
    "floor_top_up": 3111.90,
    "wrong_multiplicative": 83804.64,   # AV x (1 - 2 sc) -- NOT the answer
}


@pytest.fixture(scope="module")
def fixed_deferred_annuity():
    """The MYGA_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(fixed_deferred_annuity):
    """Model point 1 - the worked-example anchor cell."""
    return fixed_deferred_annuity.Projection[1]


@pytest.fixture(scope="module")
def stress(fixed_deferred_annuity):
    """Model point 2 - the anchor cell on the 10.00% stress reference yield."""
    return fixed_deferred_annuity.Projection[2]


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, t):
    """Every cell of the notes' seven-row account value table, to the cent."""
    av_bef, wd, av_bef_inv, av, mgsv = WORKED_EXAMPLE[t]
    assert anchor.av_pp_at(t, "BEF_WD") == pytest.approx(av_bef, abs=CENT)
    assert anchor.wd_pp(t) == pytest.approx(wd, abs=CENT)
    assert anchor.av_pp_at(t, "BEF_INV") == pytest.approx(av_bef_inv, abs=CENT)
    assert anchor.av_pp(t) == pytest.approx(av, abs=CENT)
    assert anchor.mgsv_pp(t) == pytest.approx(mgsv, abs=CENT)


def test_worked_example_is_result_av(anchor):
    """result_av() reproduces the same table, so the printed output is the golden one."""
    df = anchor.result_av()
    for t, (av_bef, wd, av_bef_inv, av, mgsv) in WORKED_EXAMPLE.items():
        assert df.loc[t, "av_pp_bef_wd"] == pytest.approx(av_bef, abs=CENT)
        assert df.loc[t, "wd_pp"] == pytest.approx(wd, abs=CENT)
        assert df.loc[t, "av_pp_bef_inv"] == pytest.approx(av_bef_inv, abs=CENT)
        assert df.loc[t, "av_pp"] == pytest.approx(av, abs=CENT)
        assert df.loc[t, "mgsv_pp"] == pytest.approx(mgsv, abs=CENT)


def test_monthly_factors(anchor):
    """f = 1.0445^(1/12) = 1.0036348 and g = 1.028^(1/12) = 1.0023039, both derived."""
    assert 1.0 + anchor.credit_rate_mth(1) == pytest.approx(1.0036348, abs=5e-8)
    assert 1.0 + anchor.mgsv_rate_mth() == pytest.approx(1.0023039, abs=5e-8)


def test_twelve_monthly_factors_reproduce_the_annual_rate_exactly(anchor):
    """The notes' own checks on the table, asserted at full precision, not to the cent.

    AV(12) = 100,000 x 1.0445 exactly; AV(24) = 100,450 x 1.0445 = 104,920.025 (the table
    displays 104,920.03); MGSV(12) = 87,500 x 1.028 and, with the month-13 withdrawal
    deducted gross, MGSV(24) = (89,950 - 4,000) x 1.028 = 88,356.60.
    """
    assert anchor.av_pp(12) == pytest.approx(100000.0 * 1.0445, rel=1e-12)
    assert anchor.av_pp(24) == pytest.approx(100450.0 * 1.0445, rel=1e-12)
    assert anchor.av_pp(24) == pytest.approx(104920.025, rel=1e-12)
    assert anchor.mgsv_pp(0) == 87500.0
    assert anchor.mgsv_pp(12) == pytest.approx(87500.0 * 1.028, rel=1e-12)
    assert anchor.mgsv_pp(24) == pytest.approx((89950.0 - 4000.0) * 1.028, rel=1e-12)


def test_month_13_withdrawal_is_free_of_charge_and_mva(anchor):
    """Contract year 2 allowance = 10% x AV(12) = 10,445.00, so the $4,000 is all free."""
    assert anchor.free_wd_allow(2) == pytest.approx(10445.00, abs=CENT)
    assert anchor.free_wd_avail(13) == pytest.approx(10445.00, abs=CENT)
    assert anchor.wd_free_pp(13) == pytest.approx(4000.00, abs=CENT)
    assert anchor.wd_excess_pp(13) == 0.0
    assert anchor.wd_charge_pp(13) == 0.0
    assert anchor.wd_mva_pp(13) == 0.0
    assert anchor.wd_payment_pp(13) == pytest.approx(4000.00, abs=CENT)
    assert anchor.free_wd_remain(13) == pytest.approx(6445.00, abs=CENT)


# ---------------------------------------------------------------------------
# Surrender trace, end of month 30


def test_surrender_trace_month_30(anchor):
    """The notes' month-30 trace, line by line: cap not binding, floor not binding."""
    g = SURRENDER_30
    assert anchor.free_wd_allow(3) == pytest.approx(g["free_wd"], abs=CENT)
    assert anchor.free_wd_remain(30) == pytest.approx(g["free_wd"], abs=CENT)
    assert anchor.surr_excess_pp(30) == pytest.approx(g["excess"], abs=ROUNDED)
    assert anchor.surr_charge_rate(30) == 0.07
    assert anchor.surr_charge_pp(30) == pytest.approx(g["charge"], abs=CENT)
    assert anchor.mva_term(30) == pytest.approx(g["mva_term"], rel=1e-12)
    assert anchor.mva_rate(30) == pytest.approx(g["mva_rate"], abs=5e-7)
    raw = anchor.mva_rate(30) * anchor.surr_excess_pp(30)
    assert raw == pytest.approx(g["mva_raw"], abs=CENT)
    assert anchor.mva_pp(30) == pytest.approx(g["mva"], abs=CENT)
    assert abs(anchor.mva_pp(30)) < anchor.surr_charge_pp(30)     # cap not binding
    assert anchor.surr_value_pp(30) == pytest.approx(g["surr_value"], abs=CENT)
    assert anchor.mgsv_pp(30) == pytest.approx(g["mgsv"], abs=CENT)
    assert anchor.surr_value_pp(30) > anchor.mgsv_pp(30)          # floor not binding
    assert anchor.surr_benefit_pp(30) == pytest.approx(g["benefit"], abs=CENT)
    assert (anchor.surr_benefit_pp(30) - anchor.free_wd_remain(30)
            == pytest.approx(g["charged_excess"], abs=CENT))


def test_mva_reference_yields_at_month_30(anchor):
    """i0 = 5.00% locked at issue, it = 6.50% at surrender, both **[std]**."""
    assert anchor.mva_ref_yield_locked(30) == 0.0500
    assert anchor.mva_ref_yield(30) == 0.0650
    assert anchor.mva_ref_yield_at_issue() == 0.0500


def test_mva_term_is_six_months_plus_two_whole_years(anchor):
    """T = 0.5 + 2: to the end of contract year 3, plus years 4 and 5 of the MVA period."""
    months_to_year_end = 12 * anchor.policy_year(30) - 30
    whole_years_left = anchor.guar_period() * anchor.gp_index(30) - anchor.policy_year(30)
    assert months_to_year_end == 6
    assert whole_years_left == 2
    assert anchor.mva_term(30) == 2.5


# ---------------------------------------------------------------------------
# Surrender trace, end of month 6 -- cap and floor both binding


def test_surrender_trace_month_6_floor_binds(stress):
    """The notes' month-6 stress trace: the symmetric cap bites, then the floor does."""
    g = SURRENDER_6
    assert stress.av_pp(6) == pytest.approx(g["av"], abs=CENT)
    assert stress.free_wd_allow(1) == pytest.approx(g["free_wd"], abs=CENT)
    assert stress.free_wd_remain(6) == pytest.approx(g["free_wd"], abs=CENT)
    assert stress.surr_excess_pp(6) == pytest.approx(g["excess"], abs=CENT)
    assert stress.surr_charge_rate(6) == 0.09
    assert stress.surr_charge_pp(6) == pytest.approx(g["charge"], abs=CENT)
    assert stress.mva_term(6) == pytest.approx(g["mva_term"], rel=1e-12)
    assert stress.mva_rate(6) == pytest.approx(g["mva_rate"], abs=5e-7)
    raw = stress.mva_rate(6) * stress.surr_excess_pp(6)
    assert raw == pytest.approx(g["mva_raw"], abs=CENT)
    assert stress.mva_pp(6) == pytest.approx(g["mva"], abs=CENT)
    assert stress.mva_pp(6) == pytest.approx(-stress.surr_charge_pp(6), abs=CENT)
    assert stress.surr_value_pp(6) == pytest.approx(g["surr_value"], abs=CENT)
    assert stress.mgsv_pp(6) == pytest.approx(g["mgsv"], abs=CENT)
    assert stress.surr_benefit_pp(6) == pytest.approx(g["benefit"], abs=CENT)
    assert (stress.surr_benefit_pp(6) - stress.surr_value_pp(6)
            == pytest.approx(g["floor_top_up"], abs=CENT))


def test_symmetric_cap_worst_case_is_not_the_multiplicative_form(stress):
    """The notes' ordering lesson: the worst case is AV - 2 sc E, not AV x (1 - 2 sc).

    They coincide only when the free amount is zero.  Here the free amount is $10,000, so
    the multiplicative reading understates the surrender value by 2 sc x FW.
    """
    g = SURRENDER_6
    two_charges = (stress.av_pp(6) - 2 * 0.09 * stress.surr_excess_pp(6))
    assert two_charges == pytest.approx(g["surr_value"], abs=CENT)
    multiplicative = stress.av_pp(6) * (1 - 2 * 0.09)
    assert multiplicative == pytest.approx(g["wrong_multiplicative"], abs=CENT)
    assert two_charges - multiplicative == pytest.approx(
        2 * 0.09 * stress.free_wd_remain(6), abs=CENT)


# ---------------------------------------------------------------------------
# The geometric MVA branch -- the Nationwide arithmetic unit test [S4]


def test_geometric_branch_factors(anchor):
    """5-year GPO, a = 8%, 985 days to maturity, 25 bp expense adder.

    The notes say to assert the factors rather than the dollar figures: recomputing the
    printed surrender values from the printed five-decimal factors reproduces them only
    to within three cents.
    """
    tau = 985 / 365.25
    assert anchor.mva_factor_geometric(0.08, 0.07, tau) == pytest.approx(1.01897, abs=5e-6)
    assert anchor.mva_factor_geometric(0.08, 0.09, tau) == pytest.approx(0.96944, abs=5e-6)
    assert 12067.96 * anchor.mva_factor_geometric(0.08, 0.07, tau) == pytest.approx(
        12296.89, abs=0.03)
    assert 12067.96 * anchor.mva_factor_geometric(0.08, 0.09, tau) == pytest.approx(
        11699.17, abs=0.05)


def test_geometric_branch_reference_maturity_rounds_up(anchor):
    """985 / 365.25 = 2.69 years selects the 3-year yield; the exponent keeps 2.69."""
    assert anchor.mva_ref_term_years(985 / 365.25) == 3
    assert anchor.mva_ref_term_years(0.1) == 1
    assert anchor.mva_ref_term_years(9.0) == anchor.guar_period()   # capped at the period


def test_geometric_branch_expense_adder_alone(anchor):
    """Appendix A: a 10-year GPO with a = b = 8% and 9 years left shows -2.06%.

    That is the pure effect of the 25 bp adder, and it is why the adder is a parameter.
    """
    assert anchor.mva_factor_geometric(0.08, 0.08, 9.0) - 1.0 == pytest.approx(
        -0.0206, abs=5e-5)


def test_geometric_family_is_selectable(fixed_deferred_annuity):
    """Model point 4 runs the geometric family end to end, uncapped [S3][S4]."""
    p4 = fixed_deferred_annuity.Projection[4]
    assert p4.mva_family() == "geometric"
    expected = p4.mva_factor_geometric(
        p4.mva_ref_yield_locked(30), p4.mva_ref_yield(30), p4.mva_term(30)) - 1.0
    assert p4.mva_rate(30) == pytest.approx(expected, rel=1e-12)


# ---------------------------------------------------------------------------
# Known modeling pitfalls -- one test each


def test_pitfall_composition_order(anchor):
    """MVA then charge then floor, both computed on the pre-deduction excess E [S8].

    Applying the charge first and the MVA to the net figure understates the adjustment by
    sc x |M|; this asserts the model does not do that.
    """
    t = 30
    excess = anchor.surr_excess_pp(t)
    charge = anchor.surr_charge_rate(t) * excess
    mva = anchor.mva_rate(t) * excess
    assert anchor.surr_charge_pp(t) == pytest.approx(charge, rel=1e-12)
    assert anchor.mva_pp(t) == pytest.approx(mva, rel=1e-12)
    assert anchor.surr_value_pp(t) == pytest.approx(
        anchor.av_pp(t) + mva - charge, rel=1e-12)

    charge_first = anchor.av_pp(t) - charge
    wrong = charge_first + anchor.mva_rate(t) * (charge_first - anchor.free_wd_remain(t))
    assert wrong - anchor.surr_value_pp(t) == pytest.approx(
        anchor.surr_charge_rate(t) * abs(mva), rel=1e-9)


def test_pitfall_floor_before_mva_would_remove_the_downside(stress):
    """Flooring before the MVA silently removes the downside protection.

    At month 6 the raw SV is below MGSV, so max() before the MVA is applied would return
    the account value less the charge only and lose the (capped) -8,298.07 adjustment.
    """
    floor_first = max(stress.av_pp(6) - stress.surr_charge_pp(6), stress.mgsv_pp(6))
    assert floor_first > stress.surr_benefit_pp(6)
    assert stress.surr_benefit_pp(6) == pytest.approx(
        max(stress.surr_value_pp(6), stress.mgsv_pp(6)), rel=1e-12)


def test_pitfall_free_amount_mva_interaction(fixed_deferred_annuity):
    """free_wd_mva_exempt is a real product difference and is not hard-coded.

    Model point 2 exempts the free amount [S2][S9][S10][S15][S16] and gives
    E = AV - FW; model point 4 does not [S3][S4] and gives E = AV, so the surrender value
    collapses to the multiplicative form.
    """
    p2 = fixed_deferred_annuity.Projection[2]
    p4 = fixed_deferred_annuity.Projection[4]
    assert p2.free_wd_mva_exempt() is True
    assert p4.free_wd_mva_exempt() is False
    assert p2.surr_excess_pp(30) == pytest.approx(
        p2.av_pp(30) - p2.free_wd_remain(30), rel=1e-12)
    assert p4.surr_excess_pp(30) == pytest.approx(p4.av_pp(30), rel=1e-12)
    assert p4.surr_value_pp(30) == pytest.approx(
        p4.av_pp(30) * (1 + p4.mva_rate(30) - p4.surr_charge_rate(30)), rel=1e-12)
    assert p2.surr_excess_pp(30) < p4.surr_excess_pp(30)


def test_pitfall_withdrawals_are_gross(anchor):
    """W(t) is the gross amount removed from the account value, not the check written."""
    assert anchor.av_pp_at(13, "BEF_INV") == pytest.approx(
        anchor.av_pp(12) - 4000.0, rel=1e-12)
    assert anchor.wd_pp(13) == 4000.0
    assert anchor.wd_from_av(13) == pytest.approx(
        4000.0 * anchor.pols_if_at(13, "BEF_DECR"), rel=1e-12)


def test_pitfall_model_805_withdrawal_convention(fixed_deferred_annuity):
    """gross [S11] and net_of_charges [S9] are both live and give different floors.

    Model point 1 deducts the gross $4,000 at month 13.  Model point 5 takes the
    net convention, and its month-30 excess withdrawal is charged and adjusted, so the
    two deductions genuinely differ there.
    """
    anchor = fixed_deferred_annuity.Projection[1]
    p5 = fixed_deferred_annuity.Projection[5]
    assert anchor.mgsv_wd_convention() == "gross"
    assert anchor.mgsv_wd_deduct_pp(13) == pytest.approx(anchor.wd_pp(13), rel=1e-12)
    assert p5.mgsv_wd_convention() == "net_of_charges"
    assert p5.mgsv_wd_deduct_pp(30) == pytest.approx(p5.wd_payment_pp(30), rel=1e-12)
    assert p5.wd_payment_pp(30) < p5.wd_pp(30)          # charged and adjusted downwards
    assert p5.mgsv_wd_deduct_pp(30) != pytest.approx(p5.wd_pp(30), abs=1.0)


def test_pitfall_nonforfeiture_floor_is_15bp_not_1pct(anchor):
    """The retrieved Model #805 print floors the indexed rate at 15 bp [R1 4.B].

    Implementing the folklore 1% floor overstates the minimum in low-rate environments.
    """
    assert anchor.mgsv_rate_statutory(0.0100) == pytest.approx(0.0015, rel=1e-12)
    assert anchor.mgsv_rate_statutory(0.0000) == pytest.approx(0.0015, rel=1e-12)
    assert anchor.mgsv_rate_statutory(0.0140) != pytest.approx(0.0100, abs=1e-9)


def test_statutory_rate_is_a_minimum_not_a_cap(anchor):
    """i_nf >= i_stat is the constraint; the reverse inequality is not what 4.B says.

    At CMT5 = 2.00% the statutory rate is 0.75%, so the representative 2.80% GMSV rate is
    legal and simply produces a higher floor.  Capping i_nf at round(CMT5) - 1.25% would
    make 2.80% illegal at any CMT5 below 4.05%.
    """
    assert anchor.mgsv_rate() == 0.0280
    assert anchor.mgsv_rate_statutory(0.0200) == pytest.approx(0.0075, rel=1e-12)
    assert anchor.mgsv_rate_is_compliant(0.0200) is True
    assert anchor.mgsv_rate_is_compliant(0.0000) is True
    assert anchor.mgsv_rate_statutory(0.0405) == pytest.approx(0.0280, rel=1e-12)
    assert anchor.mgsv_rate_statutory(0.0800) == pytest.approx(0.0300, rel=1e-12)  # capped


def test_pitfall_surrender_charge_clock_resets_on_renewal(anchor):
    """Under rollover the clock restarts at each guarantee-period boundary [S1][S2][S11].

    Getting this wrong relocates the shock lapse by years.
    """
    assert anchor.renewal_architecture() == "rollover"
    assert anchor.surr_charge_id(60) == "initial"
    assert anchor.surr_charge_id(62) == "renewal"
    assert anchor.surr_charge_year(60) == 5
    assert anchor.surr_charge_year(62) == 1
    assert anchor.surr_charge_year(122) == 1                # and again a period later
    assert anchor.surr_charge_rate(62) == 0.05              # renewal year 1
    assert anchor.surr_charge_rate(74) == 0.04              # renewal year 2
    assert anchor.surr_charge_rate(122) == 0.05             # third period, year 1


def test_pitfall_mortality_is_second_order_and_the_table_is_not_published(
        anchor, fixed_deferred_annuity):
    """Death pays the full account value with no charge and no MVA [S1][S2][S13].

    And the shipped table is explicitly illustrative: the prescribed 2012 IAM Basic /
    Scale G2 / Table 6.7 basis may not be redistributed here.
    """
    for t in (1, 30, 61, 200):
        assert anchor.claim_pp(t, "DEATH") == pytest.approx(
            max(anchor.av_pp(t), anchor.surr_benefit_pp(t)), rel=1e-12)
    assert anchor.claim_pp(30, "DEATH") > anchor.claim_pp(30, "LAPSE")
    table = fixed_deferred_annuity.Data.mort_table()
    assert (table["provenance"].str.contains(r"\[std\]")).all()
    assert (table["provenance"].str.contains("not a published table")).all()


# ---------------------------------------------------------------------------
# Surrender charge schedule, guarantee period boundary and renewal


def test_initial_surrender_charge_schedule(anchor):
    """9, 8, 7, 6, 5 over contract years 1 to 5 [S10]; the period ends at t = 60."""
    expected = [0.09, 0.08, 0.07, 0.06, 0.05]
    for year, rate in enumerate(expected, start=1):
        assert anchor.surr_charge_rate(12 * year) == pytest.approx(rate, rel=1e-12)
    assert anchor.gp_index(60) == 1
    assert anchor.gp_index(61) == 2
    assert anchor.gp_end(60) == 0


def test_guarantee_period_end_window(anchor):
    """Month 61 is the 30-day window: full account value, no charge, no MVA [S1][S2]."""
    assert anchor.in_gp_window(61) is True
    assert anchor.in_gp_window(121) is True
    assert anchor.in_gp_window(1) is False
    assert anchor.in_gp_window(60) is False
    assert anchor.in_gp_window(62) is False
    assert anchor.surr_charge_rate(61) == 0.0
    assert anchor.mva_rate(61) == 0.0
    assert anchor.mva_in_force(61) is False
    assert anchor.surr_benefit_pp(61) == pytest.approx(anchor.av_pp(61), rel=1e-12)
    assert anchor.annuitization_pp(61) == pytest.approx(
        anchor.av_pp_at(61, "BEF_INV"), rel=1e-12)


def test_mva_expires_with_the_guarantee_period(anchor):
    """mu = 0 once the MVA period has run out [S8][S13][S16]."""
    assert anchor.mva_term(60) == 0.0
    assert anchor.mva_rate(60) == 0.0
    assert anchor.mva_in_force(59) is True
    assert anchor.mva_term(59) == pytest.approx(1.0 / 12.0, rel=1e-12)


def test_mva_term_equals_time_to_the_end_of_the_mva_period(anchor):
    """The notes' two-part T collapses to (12 n k - t) / 12 on a monthly grid."""
    n12 = 12 * anchor.guar_period()
    for t in (1, 6, 13, 30, 59, 62, 90, 119):
        expected = (n12 * anchor.gp_index(t) - t) / 12.0
        assert anchor.mva_term(t) == pytest.approx(expected, rel=1e-12)


def test_renewal_rate_is_redeclared_at_the_boundary(anchor):
    """Base run: MR = 4.45% and s_ren = 0, so the renewal rate equals the initial rate."""
    assert anchor.credit_rate(60) == 0.0445
    assert anchor.redeclare_month(61) == 61
    assert anchor.credit_rate(61) == pytest.approx(0.0445, rel=1e-12)
    assert anchor.credit_rate(61) >= anchor.gmir()


def test_attained_age_cap_on_the_renewal_charge(anchor):
    """4% at 94, 3% at 95, 2% at 96, 1% at 97, 0% from 98 [S1][S2]."""
    assert anchor.surr_charge_age_cap(1) == 1.0                  # age 60, no cap
    caps = {94: 0.04, 95: 0.03, 96: 0.02, 97: 0.01, 98: 0.0, 99: 0.0}
    for attained, cap in caps.items():
        t = 12 * (attained - anchor.age_at_entry()) + 1
        assert anchor.age(t) == attained
        assert anchor.surr_charge_age_cap(t) == pytest.approx(cap, rel=1e-12)
        assert anchor.surr_charge_rate(t) <= cap + 1e-15


def test_camp_b_drops_the_charge_and_the_mva(fixed_deferred_annuity):
    """annual_redeclare: no new surrender charge and mu = 0 permanently [S13]."""
    p3 = fixed_deferred_annuity.Projection[3]
    assert p3.renewal_architecture() == "annual_redeclare"
    assert p3.surr_charge_rate(30) == 0.07                       # initial term unchanged
    for t in (62, 90, 130, 200):
        assert p3.surr_charge_id(t) == "none"
        assert p3.surr_charge_rate(t) == 0.0
        assert p3.mva_term(t) == 0.0
        assert p3.mva_rate(t) == 0.0
    assert p3.in_gp_window(61) is True                           # exactly one window
    assert p3.in_gp_window(121) is False
    assert p3.redeclare_month(130) == 121                        # annual redeclaration
    assert p3.redeclare_month(133) == 133


# ---------------------------------------------------------------------------
# Behaviour: base lapse, dynamic lapse, annuitization


def test_base_deterministic_run_switches_the_dynamic_term_off(anchor):
    """MR = CR = 4.45% and s_ren = 0, so Market(t) = Rate(t) = 0 exactly."""
    for t in (1, 30, 61, 120, 240):
        assert anchor.market_rate(t) == 0.0445
        assert anchor.credit_rate(t) == pytest.approx(0.0445, rel=1e-12)
        assert anchor.lapse_dyn_market(t) == 0.0
        assert anchor.lapse_dyn_rate(t) == 0.0


def test_base_lapse_and_the_shock(anchor):
    """1.25% in contract years 1-5 and 90% at the shock: 75% x 1.25 capped at 90% [R2]."""
    assert anchor.gmir_factor() == 1.25
    for year in range(1, 6):
        t = 12 * (year - 1) + 1
        assert anchor.lapse_rate_base(t) == 0.01
        assert anchor.lapse_rate(t) == pytest.approx(0.0125, rel=1e-12)
    shock = 12 * 5 + 1
    assert anchor.lapse_rate_base(shock) == 0.75
    assert anchor.lapse_rate(shock) == pytest.approx(0.90, rel=1e-12)
    assert anchor.lapse_rate_mth(shock) == pytest.approx(
        1 - (1 - 0.90) ** (1 / 12), rel=1e-12)


def test_rollover_repeats_the_shock_every_guarantee_period(anchor):
    """Camp A: a repeating shock at contract years 6, 11, 16, ... [S1][S2][S5][S11]."""
    shocks = [y for y in range(1, 41)
              if anchor.lapse_rate_base(12 * (y - 1) + 1) == 0.75]
    assert shocks == [6, 11, 16, 21, 26, 31, 36]


def test_camp_b_shocks_once_then_runs_off(fixed_deferred_annuity):
    """Camp B: 1,1,1,1,1,75,10,7.5,3,3,3,... [R2 Example 1 scaled to five years]."""
    p3 = fixed_deferred_annuity.Projection[3]
    pattern = [p3.lapse_rate_base(12 * (y - 1) + 1) for y in range(1, 12)]
    assert pattern == [0.01, 0.01, 0.01, 0.01, 0.01, 0.75, 0.10, 0.075, 0.03, 0.03, 0.03]


def test_annuitization_only_in_the_window(anchor):
    """a(t) = 1.0% in each window after contract year 1, 0% elsewhere **[std]**."""
    assert anchor.annuitization_rate(61) == 0.01
    assert anchor.annuitization_rate(121) == 0.01
    for t in (1, 12, 60, 62, 100):
        assert anchor.annuitization_rate(t) == 0.0
    assert anchor.pols_annuitization(61) > 0.0
    assert anchor.pols_annuitization(62) == 0.0


def test_mva_lapse_factor_defaults_to_the_best_estimate(anchor):
    """Phi_MVA = 0.35 while an MVA is in force **[std]**, 1 once it has expired [R2]."""
    assert anchor.mva_lapse_factor_at(30) == 0.35
    assert anchor.mva_lapse_factor_at(60) == 1.0                 # MVA period expired
    assert anchor.mva_lapse_factor_at(61) == 1.0                 # the window


# ---------------------------------------------------------------------------
# Roll-forwards and ledger discipline


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = annuitizations + deaths + surrenders + maturities.

    ``check_pols_roll_fwd()`` takes no argument and returns a bool over every projected
    month, the library convention; the signed per-month residual is
    ``check_pols_roll_fwd_resid(t)``.
    """
    assert anchor.check_pols_roll_fwd() is True
    for t in range(1, anchor.proj_len() + 1):
        assert anchor.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_account_value_rollforward_closes(anchor):
    """check_av_roll_fwd() is a no-argument bool; the residual is zero at every month."""
    assert anchor.check_av_roll_fwd() is True
    for t in range(1, anchor.proj_len() + 1):
        assert anchor.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_pols_if_is_the_start_of_month_count_and_weights_its_own_row(anchor):
    """pols_if(t) opens month t and is the weight on that same row's cash flows.

    The library-wide convention, matching ``Term_US_A.pols_if(1) == pols_if_init()``.
    The notes' end-of-month ``l(t)`` is ``pols_if_at(t, "AFT_DECR")`` and is unchanged.
    """
    assert anchor.pols_if(1) == anchor.pols_if_init()
    assert anchor.pols_if(0) == anchor.pols_if_init()
    for t in (1, 13, 30, 61, 120):
        assert anchor.pols_if(t) == pytest.approx(
            anchor.pols_if_at(t, "BEF_DECR"), rel=1e-15)
        assert anchor.pols_if(t + 1) == pytest.approx(
            anchor.pols_if_at(t, "AFT_DECR"), rel=1e-15)

    # The reconciliation the convention buys: the printed in-force divides the printed
    # flows on the same row.
    assert anchor.wd_pp(13) == 4000.0
    assert anchor.withdrawals(13) / anchor.wd_payment_pp(13) == pytest.approx(
        anchor.pols_if(13), rel=1e-12)
    for t in (1, 13, 30, 120):
        per_contract = (50.0 / 12.0) * anchor.inflation_factor(t)
        assert anchor.expenses(t) / per_contract == pytest.approx(
            anchor.pols_if(t), rel=1e-12)
        assert anchor.result_cf().loc[t, "pols_if"] == pytest.approx(
            anchor.pols_if(t), rel=1e-15)


def test_maturity_is_confined_to_the_last_month(anchor):
    for t in range(1, anchor.proj_len()):
        assert anchor.pols_maturity(t) == 0.0
    assert anchor.pols_maturity(anchor.proj_len()) > 0.0
    # The horizon month still opens with contracts in force; it is the month *after* it
    # that opens empty, the deemed maturity having annuitized the survivors out.
    assert anchor.pols_if(anchor.proj_len()) > 0.0
    assert anchor.pols_if(anchor.proj_len() + 1) == 0.0
    assert anchor.proj_len() == 12 * (100 - 60)


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(0, anchor.proj_len() + 1):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


def test_internal_transfers_are_not_cash_flows(anchor):
    """Interest, the charge, the MVA and the floor movement never appear in the ledger."""
    columns = set(anchor.result_cf().columns)
    for internal in ("inv_income", "surr_charge", "mva_pp", "mgsv_pp",
                     "interest_credited", "claims_over_av"):
        assert internal not in columns
    for t in (0, 1, 30, 61):
        assert anchor.net_cf(t) == pytest.approx(
            anchor.premiums(t) - anchor.withdrawals(t) - anchor.claims(t)
            - anchor.commissions(t) - anchor.expenses(t) - anchor.premium_taxes(t),
            rel=1e-12)


def test_a_binding_floor_is_not_a_separate_cash_flow(stress):
    """It raises SB(t); MGSV - SV is a reconciliation quantity, never a ledger line.

    At month 6 the floor adds $3,111.90 per contract on top of the gross surrender value
    - and the ledger still shows one surrender payment, not a payment plus a top-up.
    """
    top_up = stress.surr_benefit_pp(6) - stress.surr_value_pp(6)
    assert top_up == pytest.approx(SURRENDER_6["floor_top_up"], abs=CENT)
    assert stress.claims(6, "LAPSE") == pytest.approx(
        stress.surr_benefit_pp(6) * stress.pols_lapse(6), rel=1e-12)
    assert stress.claims(6, "LAPSE") == pytest.approx(
        stress.claims_from_av(6, "LAPSE") + stress.claims_over_av(6, "LAPSE"), rel=1e-12)
    # Signed, and negative here: the surrender pays out less than the account value it
    # releases even with the floor binding, because the charge is larger than the top-up.
    assert stress.claims_over_av(6, "LAPSE") == pytest.approx(
        (stress.surr_benefit_pp(6) - stress.av_pp(6)) * stress.pols_lapse(6), rel=1e-12)
    assert stress.claims_over_av(6, "LAPSE") < 0.0
    assert "claims_over_av" not in set(stress.result_cf().columns)


def test_claims_split_by_kind_sums_to_the_total(anchor):
    for t in (1, 30, 61, anchor.proj_len()):
        assert anchor.claims(t) == pytest.approx(
            anchor.claims(t, "DEATH") + anchor.claims(t, "LAPSE")
            + anchor.claims(t, "ANNUITIZATION") + anchor.claims(t, "MATURITY"),
            rel=1e-12)


def test_premium_and_acquisition_costs_fall_at_t_zero(anchor):
    """The notes' ledger indexes the single premium and the commission at t = 0."""
    assert anchor.premiums(0) == 100000.0
    assert anchor.commissions(0) == pytest.approx(2000.0, abs=CENT)
    assert anchor.premium_taxes(0) == 0.0
    assert anchor.net_cf(0) == pytest.approx(98000.0, abs=CENT)
    assert all(anchor.premiums(t) == 0.0 for t in range(1, 25))
    assert all(anchor.commissions(t) == 0.0 for t in range(1, 25))


def test_maintenance_expense_inflates_by_contract_year(anchor):
    """(50 / 12) x 1.025^(y-1) per contract per month **[std]**."""
    assert anchor.expenses(1) == pytest.approx(
        (50.0 / 12.0) * anchor.pols_if_at(1, "BEF_DECR"), rel=1e-12)
    assert anchor.inflation_factor(1) == 1.0
    assert anchor.inflation_factor(13) == pytest.approx(1.025, rel=1e-12)
    assert anchor.inflation_factor(25) == pytest.approx(1.025 ** 2, rel=1e-12)


def test_tax_basis_is_income_first_and_generates_no_cash_flow(anchor):
    """IRC 72(e)(3)(A): the $4,000 at month 13 is all gain, so the basis is untouched."""
    assert anchor.tax_basis_pp(0) == 100000.0
    assert anchor.av_pp_at(13, "BEF_WD") > anchor.tax_basis_pp(12)
    assert anchor.taxable_wd_pp(13) == pytest.approx(4000.0, rel=1e-12)
    assert anchor.tax_basis_pp(13) == pytest.approx(100000.0, rel=1e-12)
    assert "taxable_wd_pp" not in set(anchor.result_cf().columns)


# ---------------------------------------------------------------------------
# Result tables and model point coverage


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(0, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert set(df.columns) == {
        "pols_if", "premiums", "withdrawals", "claims_death", "claims_lapse",
        "claims_annuitization", "claims_maturity", "commissions", "expenses",
        "premium_taxes", "net_cf",
    }
    assert df.loc[0, "net_cf"] == pytest.approx(98000.0, abs=CENT)


def test_result_pols_and_result_av_shape(anchor):
    pols = anchor.result_pols()
    assert set(pols.columns) == {
        "pols_if", "pols_annuitization", "pols_death", "pols_lapse",
        "pols_maturity", "pols_if_aft_decr"}
    assert pols.index.name == "t"
    # The movement table closes: opening less the four exits is next month's opening.
    for t in (1, 30, 120):
        exits = sum(pols.loc[t, c] for c in (
            "pols_annuitization", "pols_death", "pols_lapse", "pols_maturity"))
        assert pols.loc[t, "pols_if"] - exits == pytest.approx(
            pols.loc[t + 1, "pols_if"], abs=1e-15)
    av = anchor.result_av()
    assert set(av.columns) == {
        "av_pp_bef_wd", "wd_pp", "av_pp_bef_inv", "av_pp", "mgsv_pp", "free_wd_avail",
        "surr_charge_pp", "mva_pp", "surr_value_pp", "surr_benefit_pp"}
    assert av.index.name == "t"
    assert len(av) == anchor.proj_len() + 1


def test_every_mva_switch_is_exercised_by_a_model_point(fixed_deferred_annuity):
    """The cap, not the formula family, is where the money is - so all five must run.

    All three formula families and both renewal architectures are covered too, so no
    branch of the notes' parameter set is dead code.
    """
    table = fixed_deferred_annuity.Data.model_point_table()
    assert set(table["mva_cap_rule"]) == {
        "sym_sc", "min_sc_interest", "asym_sc_snfl", "gmir_floor", "none"}
    assert set(table["mva_family"]) == {
        "linear_duration", "geometric", "declared_differential"}
    assert set(table["renewal_architecture"]) == {"rollover", "annual_redeclare"}
    assert set(table["mgsv_wd_convention"]) == {"gross", "net_of_charges"}
    assert set(table["free_wd_rule"]) == {"pct_av", "interest_only"}
    assert set(table["free_wd_mva_exempt"]) == {True, False}


def test_declared_differential_family(fixed_deferred_annuity):
    """M = W (Ic - In) F_s on the insurer's own new-money rate [S14][R4 4.I].

    Model point 7 runs it against a 6.00% competitor rate, so the differential is live.
    F_s is read on the Ic < 6% column and interpolated: at T = 2.5 it is
    1.80 + 0.5 (2.60 - 1.80) = 2.20 years of modified duration.
    """
    p7 = fixed_deferred_annuity.Projection[7]
    assert p7.mva_family() == "declared_differential"
    assert p7.credit_rate(30) == 0.0445 and p7.market_rate(30) == 0.0600
    assert p7.mva_duration_factor(30) == pytest.approx(2.20, rel=1e-12)
    assert p7.mva_rate(30) == pytest.approx((0.0445 - 0.0600) * 2.20, rel=1e-12)
    assert p7.mva_pp(30) < 0.0                       # rising rates, negative adjustment
    # The renewal rate is redeclared to max(GMIR, MR) = 6.00%, which flips the table to
    # the Ic >= 6% column: modified durations are uniformly lower there.
    assert p7.credit_rate(90) == pytest.approx(0.0600, rel=1e-12)
    assert p7.mva_duration_factor(90) < 2.60


def test_dynamic_lapse_is_live_when_the_credited_rate_trails_the_market(
        fixed_deferred_annuity):
    """Market(t) = +1.25 (MR - BF - CR)^X below the buffer, gated by the haircut [R2].

    Model point 7 credits 4.45% against a 6.00% competitor rate, so the contract sits
    outside the 50 bp buffer and the dynamic term is positive, damped by the
    surrender-charge and negative-MVA haircut and then by Phi_MVA.
    """
    p7 = fixed_deferred_annuity.Projection[7]
    market = 1.25 * (0.0600 - 0.005 - 0.0445) ** 2
    assert p7.lapse_dyn_exponent(30) == 2.0
    assert p7.lapse_dyn_market(30) == pytest.approx(market, rel=1e-12)

    gate = max(0.0, 1 - 5 * (1 - p7.surr_benefit_pp(30) / p7.av_pp(30)))
    assert 0.0 < gate < 1.0
    assert p7.lapse_dyn_rate(30) == pytest.approx(market * gate, rel=1e-12)
    assert p7.mva_lapse_factor_at(30) == 0.35
    assert p7.lapse_rate(30) == pytest.approx(0.0125 + market * gate * 0.35, rel=1e-12)

    # At month 60 the MVA period has expired, so Phi_MVA is 1 and the same market term
    # comes through undamped: the assumption the notes rank third in sensitivity.
    gate_60 = max(0.0, 1 - 5 * (1 - p7.surr_benefit_pp(60) / p7.av_pp(60)))
    assert p7.mva_lapse_factor_at(60) == 1.0
    assert p7.lapse_rate(60) == pytest.approx(
        0.0125 + p7.lapse_dyn_market(60) * gate_60, rel=1e-12)
    assert p7.lapse_rate(60) > p7.lapse_rate(30)

    # Once the renewal declaration catches the market the dynamic term vanishes again.
    assert p7.credit_rate(90) == pytest.approx(0.0600, rel=1e-12)
    assert p7.lapse_dyn_market(90) == 0.0
    assert p7.lapse_dyn_exponent(90) == 2.5


def test_asymmetric_cap_limits_only_the_upside(fixed_deferred_annuity):
    """asym_sc_snfl: M <= +C, no downside cap; only SB >= MGSV binds below [S12]."""
    p6 = fixed_deferred_annuity.Projection[6]
    assert p6.mva_cap_rule() == "asym_sc_snfl"
    raw = p6.mva_rate(6) * p6.surr_excess_pp(6)
    assert raw < -p6.surr_charge_pp(6)
    assert p6.mva_pp(6) == pytest.approx(raw, rel=1e-12)      # uncapped downwards
    assert p6.surr_benefit_pp(6) == pytest.approx(p6.mgsv_pp(6), rel=1e-12)


def test_gmir_floor_cap_holds_av_plus_mva_above_the_accumulated_premium(
        fixed_deferred_annuity):
    """gmir_floor: AV + M >= premium less prior withdrawals accumulated at the GMIR [S13]."""
    p3 = fixed_deferred_annuity.Projection[3]
    assert p3.mva_cap_rule() == "gmir_floor"
    assert p3.av_pp(6) + p3.mva_pp(6) == pytest.approx(p3.prem_accum_gmir_pp(6), rel=1e-9)
    assert p3.prem_accum_gmir_pp(0) == 100000.0
    assert p3.prem_accum_gmir_pp(12) == pytest.approx(100000.0 * 1.0025, rel=1e-12)


def test_min_sc_interest_cap_and_interest_only_allowance(fixed_deferred_annuity):
    """Model point 5: K = min(C, interest to date) [S8][S9]; allowance = prior interest."""
    p5 = fixed_deferred_annuity.Projection[5]
    assert p5.mva_cap_rule() == "min_sc_interest"
    assert p5.free_wd_rule() == "interest_only"
    assert p5.free_wd_allow(1) == 0.0                            # no prior year
    assert p5.free_wd_allow(2) == pytest.approx(4450.0, abs=CENT)   # 100,000 x 4.45%
    assert p5.free_wd_avail(30) == pytest.approx(p5.free_wd_allow(3), rel=1e-12)
    limit = min(p5.wd_charge_pp(30), p5.interest_credited_pp(30))
    assert p5.wd_mva_pp(30) == pytest.approx(-limit, rel=1e-12)


def test_invalid_timing_and_kind_arguments_raise(anchor):
    """Unknown timing or kind strings raise ValueError, as CashValue_SE does."""
    for call, arg in ((anchor.av_pp_at, "BEF_XYZ"), (anchor.pols_if_at, "BEF_XYZ")):
        with pytest.raises(Exception):
            call(12, arg)
    with pytest.raises(Exception):
        anchor.claim_pp(12, "SPLIT")


# ---------------------------------------------------------------------------
# Claims the documentation makes, pinned open
#
# The model's docstrings and README are part of the deliverable, so the statements
# they make about arithmetic and about resolved ambiguities are asserted here rather
# than left to a reader's good faith.


def _flat(text):
    """Collapse a docstring to single-spaced text so line wrapping cannot hide a phrase."""
    return " ".join(text.split())


def test_annuitization_outside_the_window_is_valued_before_crediting(anchor):
    """The transfer is composed on AV'(t), not on the notes' post-crediting SV(t).

    The notes place annuitization at BOM but name ``SV(t) = AV(t) + M(t) - C(t)``, an EOM
    quantity, for the non-window case.  The model annuitizes at BOM: the amount handed to
    the payout model is AV'(t) less the charge computed on AV'(t), with no MVA, and it is
    the same AV'(t) that ``claim_from_av_pp`` releases.  Reading ``SV(t)`` literally would
    pay a month of interest the block never credited to those contracts.
    """
    t = 30
    assert anchor.in_gp_window(t) is False
    assert anchor.free_wd_mva_exempt() is True

    bom = anchor.av_pp_at(t, "BEF_INV")
    charge = anchor.surr_charge_rate(t) * max(0.0, bom - anchor.free_wd_remain(t))
    assert anchor.annuitization_pp(t) == pytest.approx(bom - charge, rel=1e-12)

    # The release basis agrees with the payment basis: annuitizers exit at BOM.
    assert anchor.claim_from_av_pp(t, "ANNUITIZATION") == pytest.approx(bom, rel=1e-12)

    # The literal EOM reading is a different number, larger by one month's interest net
    # of the charge on it -- and it is not what this cells returns.
    eom = anchor.av_pp(t) - anchor.surr_charge_pp(t)
    interest = anchor.av_pp(t) - bom
    assert interest > 0.0
    assert eom - anchor.annuitization_pp(t) == pytest.approx(
        interest * (1 - anchor.surr_charge_rate(t)), rel=1e-9)

    # In the window it is the full pre-crediting account value, no charge and no MVA.
    assert anchor.in_gp_window(61) is True
    assert anchor.annuitization_pp(61) == pytest.approx(
        anchor.av_pp_at(61, "BEF_INV"), rel=1e-12)

    # Inert as shipped: a(t) is zero outside the window on every model point.
    assert anchor.annuitization_rate(t) == 0.0
    assert anchor.claims(t, "ANNUITIZATION") == 0.0


def test_horizon_is_the_last_age_in_the_sourced_cap_band(fixed_deferred_annuity, anchor):
    """maturity_age = 100 is where the sourced cap band stops; the cap hits zero at 98.

    The horizon justification is stated in three places -- the model docstring, the
    ``Projection`` docstring and the README -- and all three must state the arithmetic the
    shipped table actually shows.
    """
    cap = fixed_deferred_annuity.Data.surr_charge_age_cap_table()["surr_charge_cap"]
    zero_ages = sorted(int(a) for a in cap.index if cap.loc[a] == 0.0)
    assert min(zero_ages) == 98                       # the cap reaches zero at 98 ...
    assert int(cap.index.max()) == 100                # ... and the band stops at 100
    assert anchor.maturity_age == int(cap.index.max())
    assert anchor.proj_len() == 12 * (100 - anchor.age_at_entry())

    readme = (MODEL_PATH.parent / "model.md").read_text(encoding="utf-8")
    for doc in (_flat(fixed_deferred_annuity.doc),
                _flat(fixed_deferred_annuity.Projection.doc),
                _flat(readme)):
        assert "last attained age in the" in doc
        assert "zero at 98" in doc
        # The old, wrong justification: the cap does not reach zero at 100.
        assert "reaches zero [S1][S2]" not in doc


def test_symbol_table_covers_the_gmir_floor_level_and_the_scalar_spreads(
        fixed_deferred_annuity):
    """Every notes symbol the model implements has a row in the mapping table.

    ``P_accum@GMIR`` is a Cells; ``s_ren``, ``BF`` and ``s_adm`` are References, and the
    table says so.
    """
    doc = _flat(fixed_deferred_annuity.Projection.doc)
    for symbol, name in (("P_accum@GMIR", "prem_accum_gmir_pp"),
                         ("s_ren", "renewal_spread"),
                         ("BF", "lapse_buffer"),
                         ("s_adm", "mva_admin_spread")):
        assert symbol in doc, f"{symbol} missing from the Projection symbol table"
        assert name in doc, f"{name} missing from the Projection symbol table"

    proj = fixed_deferred_annuity.Projection
    assert proj.renewal_spread == 0.0                 # base run [std]
    assert proj.lapse_buffer == 0.005                 # BF = 50 bp
    assert proj.mva_admin_spread == 0.0025            # s_adm = 25 bp [S4]
    assert proj[1].prem_accum_gmir_pp(0) == 100000.0


def test_readme_contrasts_t_zero_with_term_life_only():
    """The t = 0 index is contrasted with Term_US_A, not claimed across the library.

    Sibling models in ``products/`` also index their result tables from 0, so the
    library-wide claim this README used to make was false.
    """
    readme = _flat((MODEL_PATH.parent / "model.md").read_text(encoding="utf-8"))
    assert "Every other model in the library starts its result table at 1" not in readme
    assert ("contrast with `Term_US_A`, the model this one takes its structure from, "
            "whose result table starts at `t = 1`") in readme
