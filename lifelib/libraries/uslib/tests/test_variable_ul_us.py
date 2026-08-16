"""Golden and product-specific tests for VUL_US_S.

The golden values are the worked example in products/variable_ul/technical-notes.md
("Worked example - one month, two subaccounts"), which traces one monthiversary of the
anchor cell: male 45 standard nonsmoker, F_0 = 500,000, Option A, GPT, policy year 3
(surrender charge factor 12/14), planned premium $500/month paid, allocation 60/40, no
fixed balance and no debt; gamma = 4%, c = $0.04 per $1,000 NAAR, e_1 = 0.75%,
e_2 = 0.55%, m = 0.45%; scenario month r_1 = +1.00%, r_2 = -0.50%; kappa(45) = 215%.

They are hard-coded here rather than pickled so that a reviewer can compare them
against the notes by eye.  Model point 1 is that cell, with duration_mth = 24 so that
projection month t = 1 is the worked example's month.

Tolerances follow the precision the notes display: money to the cent, growth factors to
six decimals.  Two totals in the notes' table are the sum of the *displayed* subaccount
values rather than the sum of the exact ones, and so sit half a cent away from the
model; test_worked_example_total_av_is_a_sum_of_rounded_parts pins that gap open.
"""
import math

import modelx as mx
import pytest

from us_registry import LIB

def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9).  Those caches are not part of the
    model and must not make a round-trip comparison fail for anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


MODEL_PATH = LIB / "products/variable_ul/VUL_US_S"

CENT = 0.005          # money displayed to 2 d.p.
FACTOR = 5e-7         # growth factors displayed to 6 d.p.
RATE = 5e-7           # rates displayed to 6 d.p.

# products/variable_ul/technical-notes.md, "Worked example - one month, two
# subaccounts".  Keys are the notes' step numbers.
WE = {
    # step 0  BOM balances
    "sa1_bom": 30000.00, "sa2_bom": 20000.00, "av_bom": 50000.00,
    # step 2  Premium 500.00; load 4% = 20.00; net 480.00 split 60/40
    "premium": 500.00, "load": 20.00, "net_premium": 480.00,
    "sa1_prem": 288.00, "sa2_prem": 192.00, "av_bef_fee": 50480.00,
    # step 5  DB = max(500,000; 2.15 x 50,480 = 108,532.00) = 500,000.00
    "corridor_factor": 2.15, "db_corridor": 108532.00,
    "db": 500000.00, "naar": 449520.00,
    # step 6  COI = 0.04 x 449.520 = 17.98; expense = 10.00 + 0.20 x 500 = 110.00;
    #         MD = 127.98, pro rata 60/40
    "coi_rate": 0.04, "coi": 17.98, "maint_fee": 110.00, "md": 127.98,
    "md_sa1": 76.79, "md_sa2": 51.19, "av_bef_inv": 50352.02,
    # step 7  growth factor (1+r)(1-e/12)(1-m/12)
    "fund_factor_1": 0.999375, "fund_factor_2": 0.999542, "me_factor": 0.999625,
    "growth_1": 1.008990, "growth_2": 0.994171,
    "sa1_eom": 30482.82, "sa2_eom": 20023.41, "av_eom": 50506.23,
    # memo  M&E collected via unit values ~ 11.44 + 7.51 = 18.95;
    #       insurer margin this month = 20.00 + 127.98 + 18.95 = 166.93
    "me_1": 11.44, "me_2": 7.51, "me_total": 18.95, "margin": 166.93,
    # memo  SC = 18.00 x (12/14) x 500 = 7,714.29; CSV = 50,506.23 - 7,714.29
    "sc_rate": 15.428571, "sc": 7714.29, "csv": 42791.94,
    # memo  EOM DB = 500,000.00; EOM NAAR = 449,493.77
    "db_eom": 500000.00, "naar_eom": 449493.77,
}


@pytest.fixture(scope="module")
def variable_ul():
    """The VUL_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(variable_ul):
    """Model point 1 - the worked-example anchor cell."""
    return variable_ul.Projection[1]


# ---------------------------------------------------------------------------
# The worked example, step by step


def test_worked_example_step0_opening_balances(anchor):
    """Step 0: the model point opens where the worked example opens."""
    assert anchor.age_at_entry() == 45
    assert anchor.sex() == "M"
    assert anchor.rate_class() == "StdNT"
    assert anchor.sum_assured() == 500000.0
    assert anchor.db_option() == "A"
    assert anchor.qual_test() == "GPT"
    assert anchor.policy_year(1) == 3          # "policy year 3"
    assert anchor.sa_pp_at(1, 1, "BEF_PREM") == pytest.approx(WE["sa1_bom"], abs=CENT)
    assert anchor.sa_pp_at(1, 2, "BEF_PREM") == pytest.approx(WE["sa2_bom"], abs=CENT)
    assert anchor.fa_pp_at(1, "BEF_PREM") == 0.0
    assert anchor.loan_bal_pp(0) == 0.0
    assert anchor.av_pp_at(1, "BEF_PREM") == pytest.approx(WE["av_bom"], abs=CENT)


def test_worked_example_step2_premium_load_and_allocation(anchor):
    """Step 2: premium 500.00, load 4% = 20.00, net 480.00 split 60/40."""
    assert anchor.premium_pp(1) == pytest.approx(WE["premium"], abs=CENT)
    assert anchor.load_prem_rate() == 0.04
    assert (anchor.premium_pp(1) * anchor.load_prem_rate()
            == pytest.approx(WE["load"], abs=CENT))
    assert anchor.prem_to_av_pp(1) == pytest.approx(WE["net_premium"], abs=CENT)
    assert anchor.alloc(1) == 0.60
    assert anchor.alloc(2) == 0.40
    assert anchor.alloc_fixed() == 0.00
    assert (anchor.alloc(1) * anchor.prem_to_av_pp(1)
            == pytest.approx(WE["sa1_prem"], abs=CENT))
    assert (anchor.alloc(2) * anchor.prem_to_av_pp(1)
            == pytest.approx(WE["sa2_prem"], abs=CENT))
    assert anchor.sa_pp_at(1, 1, "BEF_FEE") == pytest.approx(
        WE["sa1_bom"] + WE["sa1_prem"], abs=CENT)
    assert anchor.sa_pp_at(1, 2, "BEF_FEE") == pytest.approx(
        WE["sa2_bom"] + WE["sa2_prem"], abs=CENT)
    assert anchor.av_pp_at(1, "BEF_FEE") == pytest.approx(WE["av_bef_fee"], abs=CENT)


def test_worked_example_step5_death_benefit_and_naar(anchor):
    """Step 5: DB = max(500,000; 2.15 x 50,480 = 108,532.00); NAAR = 449,520.00."""
    assert anchor.corridor_factor(1) == pytest.approx(WE["corridor_factor"], abs=RATE)
    assert anchor.db_corridor_pp(1) == pytest.approx(WE["db_corridor"], abs=CENT)
    assert anchor.db_pp(1) == pytest.approx(WE["db"], abs=CENT)
    assert anchor.net_amt_at_risk(1) == pytest.approx(WE["naar"], abs=CENT)


def test_worked_example_step6_monthly_deduction(anchor):
    """Step 6: COI 17.98 + 110.00 fixed = MD 127.98, taken pro rata 60/40."""
    assert anchor.coi_rate(1) == pytest.approx(WE["coi_rate"], abs=RATE)
    assert anchor.coi_pp(1) == pytest.approx(WE["coi"], abs=CENT)
    assert anchor.expense_pol_mth == 10.00
    assert anchor.expense_unit_mth == 0.20
    assert anchor.units() == 500.0                       # F_0 / 1000
    assert anchor.maint_fee_pp(1) == pytest.approx(WE["maint_fee"], abs=CENT)
    assert anchor.mth_deduction_pp(1) == pytest.approx(WE["md"], abs=CENT)
    assert anchor.mth_deduction_sa_pp(1, 1) == pytest.approx(WE["md_sa1"], abs=CENT)
    assert anchor.mth_deduction_sa_pp(1, 2) == pytest.approx(WE["md_sa2"], abs=CENT)
    assert anchor.mth_deduction_fa_pp(1) == 0.0
    assert anchor.av_pp_at(1, "BEF_INV") == pytest.approx(WE["av_bef_inv"], abs=CENT)


def test_worked_example_step7_growth_factors(anchor):
    """Step 7: 1.0100 x 0.999375 x 0.999625 and 0.9950 x 0.999542 x 0.999625."""
    assert anchor.gross_return_mth(1, 1) == pytest.approx(0.0100, abs=RATE)
    assert anchor.gross_return_mth(1, 2) == pytest.approx(-0.0050, abs=RATE)
    assert 1 - anchor.fund_expense_ann(1) / 12 == pytest.approx(
        WE["fund_factor_1"], abs=FACTOR)
    assert 1 - anchor.fund_expense_ann(2) / 12 == pytest.approx(
        WE["fund_factor_2"], abs=FACTOR)
    assert 1 - anchor.me_rate_ann / 12 == pytest.approx(WE["me_factor"], abs=FACTOR)
    assert 1 + anchor.inv_return_mth(1, 1) == pytest.approx(WE["growth_1"], abs=FACTOR)
    assert 1 + anchor.inv_return_mth(1, 2) == pytest.approx(WE["growth_2"], abs=FACTOR)


def test_worked_example_step7_end_of_month_balances(anchor):
    """Step 7: 30,482.82 and 20,023.41 at the end of the month."""
    assert anchor.sa_pp(1, 1) == pytest.approx(WE["sa1_eom"], abs=CENT)
    assert anchor.sa_pp(1, 2) == pytest.approx(WE["sa2_eom"], abs=CENT)
    assert anchor.fa_pp(1) == 0.0
    assert anchor.la_pp(1) == 0.0
    # Each end-of-month balance is the post-deduction balance times its own factor.
    assert anchor.sa_pp(1, 1) == pytest.approx(
        anchor.sa_pp_at(1, 1, "BEF_INV") * WE["growth_1"], rel=1e-6)
    assert anchor.sa_pp(1, 2) == pytest.approx(
        anchor.sa_pp_at(1, 2, "BEF_INV") * WE["growth_2"], rel=1e-6)


def test_worked_example_total_av_is_a_sum_of_rounded_parts(anchor):
    """The notes' 50,506.23 total is the sum of the two *displayed* subaccounts.

    Summing the exact balances gives 50,506.2245, which displays as 50,506.22.  The
    notes' table adds the rounded column entries instead, so its total and its EOM net
    amount at risk each sit 0.0055 away from the model.  Both readings are asserted
    here so the half-cent cannot be closed silently in either direction, and neither is
    a modelling difference: the recursion is identical.
    """
    exact = anchor.av_pp(1)
    assert exact == pytest.approx(50506.2245, abs=CENT)
    assert round(anchor.sa_pp(1, 1), 2) + round(anchor.sa_pp(1, 2), 2) == pytest.approx(
        WE["av_eom"], abs=1e-9)
    assert exact == pytest.approx(WE["av_eom"], abs=0.01)
    assert round(exact, 2) != WE["av_eom"]              # the gap is real, not rounding


def test_worked_example_memo_me_charge_and_insurer_margin(anchor):
    """Memo: M&E 11.44 + 7.51 = 18.95; margin 20.00 + 127.98 + 18.95 = 166.93."""
    assert anchor.me_charge_pp(1, 1) == pytest.approx(WE["me_1"], abs=CENT)
    assert anchor.me_charge_pp(1, 2) == pytest.approx(WE["me_2"], abs=CENT)
    assert anchor.me_charge_pp(1) == pytest.approx(WE["me_total"], abs=CENT)
    margin = (anchor.premium_pp(1) * anchor.load_prem_rate()
              + anchor.mth_deduction_pp(1) + anchor.me_charge_pp(1))
    assert margin == pytest.approx(WE["margin"], abs=CENT)


def test_worked_example_memo_surrender_charge_and_cash_value(anchor):
    """Memo: SC = 18.00 x (12/14) x 500 = 7,714.29; CSV = 42,791.94."""
    assert anchor.surr_charge_rate(1) == pytest.approx(WE["sc_rate"], abs=RATE)
    assert anchor.surr_charge_rate(1) == pytest.approx(18.00 * 12 / 14, rel=1e-12)
    assert anchor.surr_charge_pp(1) == pytest.approx(WE["sc"], abs=CENT)
    assert anchor.csv_pp(1) == pytest.approx(WE["csv"], abs=CENT)
    assert anchor.ncsv_pp(1) == pytest.approx(WE["csv"], abs=CENT)   # no debt


def test_worked_example_memo_end_of_month_db_and_naar(anchor):
    """Memo: EOM DB = 500,000.00; EOM NAAR = 449,493.77 (on the rounded total AV)."""
    assert anchor.db_pp_eom(1) == pytest.approx(WE["db_eom"], abs=CENT)
    # The notes compute this as 500,000 - 50,506.23, their sum-of-rounded total.
    assert (WE["db_eom"] - round(anchor.sa_pp(1, 1), 2) - round(anchor.sa_pp(1, 2), 2)
            == pytest.approx(WE["naar_eom"], abs=1e-9))
    assert anchor.net_amt_at_risk_eom(1) == pytest.approx(449493.7755, abs=CENT)
    assert anchor.net_amt_at_risk_eom(1) == pytest.approx(WE["naar_eom"], abs=0.01)


# ---------------------------------------------------------------------------
# The divergence the notes leave open


def test_the_two_age_lookups_are_shipped_both_ways(variable_ul):
    """The worked example looks up two age-dependent parameters at the issue age.

    It sits in policy year 3, attained age 47, but quotes kappa(45) = 215% and the
    disclosed year-1 current COI anchor $0.04.  Model point 1 pins both in month 1 so
    the worked example reproduces; model point 2 is the same cell with the pins blank
    and takes the rule from month 1.  Neither is "correct" - the test exists so the gap
    cannot be closed silently in either direction.
    """
    p1, p2 = variable_ul.Projection[1], variable_ul.Projection[2]
    assert p1.age(1) == 47 and p2.age(1) == 47
    # the pinned reading
    assert p1.corridor_factor(1) == 2.15
    assert p1.coi_rate(1) == 0.04
    # the rule
    assert p2.corridor_factor(1) == pytest.approx(2.03, abs=RATE)
    assert p2.coi_rate(1) == pytest.approx(0.5 * p2.coi_rate_guar(1), rel=1e-12)
    assert p1.corridor_factor(1) != pytest.approx(p2.corridor_factor(1), abs=1e-3)
    assert p1.coi_rate(1) != pytest.approx(p2.coi_rate(1), abs=1e-3)
    # the pin is confined to month 1; from month 2 the two points coincide
    assert p1.corridor_factor(2) == p2.corridor_factor(2)
    assert p1.coi_rate(2) == p2.coi_rate(2)
    assert p1.coi_rate(2) != pytest.approx(p1.coi_rate(1), abs=1e-3)


def test_the_disclosed_coi_anchor_is_not_the_placeholder(anchor):
    """The notes' own acknowledged gap: 0.04 disclosed vs 0.11 = 50% of 0.22 [S4]."""
    assert anchor.coi_rate_guar_at(1) == pytest.approx(0.22, abs=1e-9)
    assert anchor.coi_curr_factor == 0.5
    assert anchor.coi_rate_at(1) == pytest.approx(0.11, abs=1e-9)


# ---------------------------------------------------------------------------
# The sourced deviation from the universal-life chassis


def test_naar_carries_no_one_month_discount(anchor):
    """The one sourced deviation from the fixed-UL chassis [S2].

    The VUL prospectuses define the net amount at risk as death benefit less account
    value outright, so there is no division by (1 + i_gm) and no naar_factor cells.
    Applying the chassis's discount would cut the net amount at risk - and with it the
    cost of insurance - by about one month's guaranteed interest on the death benefit.
    """
    assert anchor.net_amt_at_risk(1) == pytest.approx(
        anchor.db_pp(1) - anchor.av_pp_at(1, "BEF_FEE"), rel=1e-12)
    assert "naar_factor" not in anchor.cells
    chassis = anchor.db_pp(1) / (1 + 0.02) ** (1 / 12) - anchor.av_pp_at(1, "BEF_FEE")
    assert anchor.net_amt_at_risk(1) - chassis == pytest.approx(824.0, abs=1.0)


def test_the_chassis_differences_the_docstring_claims_are_real(anchor):
    """The model docstring lists the differences from UL_US_S; pin them all.

    The list is meant to be complete - the README tabulates the same set - so each
    entry, including the four names the chassis has and this model deliberately does
    not, is asserted here rather than left as prose.
    """
    for gone in ("naar_factor", "wd_free_pp", "gpt_ok", "is_mec"):
        assert gone not in anchor.cells
    assert anchor.net_amt_at_risk(1) == pytest.approx(
        anchor.db_pp(1) - anchor.av_pp_at(1, "BEF_FEE"), rel=1e-12)
    assert anchor.units() == anchor.sum_assured() / 1000        # F_0, not F_t
    assert anchor.surr_charge_rate(1) == anchor.surr_charge_rate(12)  # steps by year
    assert anchor.inflation_rate == 0.0                         # not the chassis 2.5%
    assert anchor.lapse_shock_mult == 1.0                       # a one-month spike, off
    assert "lapse_rate_cap" not in anchor.refs                  # no 35% total cap
    assert anchor.lapse_rate(1) == pytest.approx(
        anchor.lapse_rate_base(1) * anchor.lapse_rate_dyn_mult(1)
        * anchor.lapse_rate_sc_mult(1), rel=1e-12)


def test_surrender_charge_steps_by_policy_year_not_by_month(anchor):
    """18.00 x (runoff + 1 - y) / runoff, level within a policy year.

    The fixed-UL chassis amortizes its surrender charge every month; the variable-UL
    notes step it by policy year and the worked example pins the step at 12/14 in
    policy year 3.  Carrying the chassis recursion across would give a different figure
    in every month of the year.
    """
    for t in range(1, 13):                        # all of policy year 3
        assert anchor.policy_year(t) == 3
        assert anchor.surr_charge_rate(t) == pytest.approx(18.00 * 12 / 14, rel=1e-12)
    assert anchor.surr_charge_rate(13) == pytest.approx(18.00 * 11 / 14, rel=1e-12)


def test_charges_are_quoted_on_the_initial_face(anchor):
    """units() takes no t: the $0.20 charge and the surrender charge both use F_0."""
    assert anchor.units() == anchor.sum_assured() / 1000
    assert anchor.maint_fee_pp(1) == pytest.approx(
        10.00 + 0.20 * anchor.sum_assured() / 1000, abs=CENT)
    assert anchor.surr_charge_pp(1) == pytest.approx(
        anchor.surr_charge_rate(1) * anchor.sum_assured() / 1000, rel=1e-12)


def test_maintenance_expense_does_not_inflate(anchor):
    """The variable-UL notes give a flat $75/policy/year, not the chassis's 2.5%."""
    assert anchor.inflation_rate == 0.0
    assert anchor.expense_maint == 75.0
    assert anchor.inflation_factor(1) == 1.0
    assert anchor.inflation_factor(600) == 1.0
    assert anchor.expenses(1) == pytest.approx(75.0 / 12 * anchor.pols_if(1), abs=1e-9)


# ---------------------------------------------------------------------------
# The notes' "Known modeling pitfalls", one test each


def test_pitfall_coi_scale_is_not_the_death_decrement(anchor):
    """"Conflating COI-scale mortality (charge) with decrement mortality (experience)."

    They are different tables here on purpose: the guaranteed COI basis stands in for
    the 2017 CSO maximum, the decrement for best-estimate 2015 VBT-style experience,
    and the best estimate must sit well below the guaranteed charge basis.
    """
    coi_implied_annual = anchor.coi_rate_guar_at(1) * 12 / 1000
    assert coi_implied_annual == pytest.approx(0.00264, abs=1e-9)
    assert anchor.mort_rate(1) < coi_implied_annual
    assert anchor.mort_rate(1) != pytest.approx(coi_implied_annual, rel=0.1)


def test_pitfall_the_claim_is_the_full_death_benefit(anchor):
    """"Projecting DB - AV as the death outflow" - the notes' explicit warning.

    The gross claim is the whole death benefit less policy debt; DB - AV is the net
    general-account strain and belongs to the derived net view only.
    """
    assert anchor.claim_pp(1, "DEATH") == pytest.approx(
        anchor.db_pp_eom(1) - anchor.loan_bal_pp(1), rel=1e-12)
    assert anchor.claims(1, "DEATH") == pytest.approx(
        anchor.claim_pp(1, "DEATH") * anchor.pols_death(1), rel=1e-12)
    assert anchor.claims_net(1) == pytest.approx(
        anchor.net_amt_at_risk_eom(1) * anchor.pols_death(1), rel=1e-12)
    # the gross claim is an order of magnitude larger at these funding levels
    assert anchor.claims(1, "DEATH") > anchor.claims_net(1)
    assert anchor.claims(1, "DEATH") - anchor.claims_net(1) == pytest.approx(
        anchor.av_pp(1) * anchor.pols_death(1), rel=1e-12)


def test_pitfall_naar_is_floored_at_zero(variable_ul):
    """"Forgetting the NAAR floor at zero."

    Once the corridor factor reaches 1.00 at age 95 an Option A policy funded above its
    face has DB = AV, so the net amount at risk is zero and no cost of insurance is
    charged - not a negative one.
    """
    p = variable_ul.Projection[2]
    late = [t for t in range(1, p.proj_len() + 1) if p.age(t) >= 95]
    assert late
    for t in late[:24]:
        assert p.net_amt_at_risk(t) >= 0.0
        assert p.net_amt_at_risk_eom(t) >= 0.0
        assert p.coi_pp(t) >= 0.0
    # constructed: a corridor of 1.00 on a policy funded above its face
    t = late[0]
    assert p.corridor_factor(t) == pytest.approx(1.00, abs=RATE)
    if p.av_pp_at(t, "BEF_FEE") > p.sum_assured_at(t):
        assert p.net_amt_at_risk(t) == 0.0


def test_pitfall_corridor_is_interpolated_not_stepped(anchor):
    """"Letting corridor factors create discontinuous DB jumps at quinquennial ages."

    The notes quote the factors five years apart and standardize linear interpolation
    between them, so the factor moves by an equal step every year rather than jumping.
    The last segment runs 130% at 60 to 100% at 95 - see
    test_corridor_grades_to_100_at_95 - and its step, 0.30/35, does not terminate in
    four decimals; corridor_factors.csv carries six, so the annual differences agree
    with the segment step to the table's own precision rather than exactly.
    """
    assert anchor.corridor_factor_at(40) == pytest.approx(2.50, abs=RATE)
    assert anchor.corridor_factor_at(45) == pytest.approx(2.15, abs=RATE)
    assert anchor.corridor_factor_at(50) == pytest.approx(1.85, abs=RATE)
    assert anchor.corridor_factor_at(55) == pytest.approx(1.50, abs=RATE)
    assert anchor.corridor_factor_at(60) == pytest.approx(1.30, abs=RATE)
    assert anchor.corridor_factor_at(95) == pytest.approx(1.00, abs=RATE)
    for a0, a1 in [(40, 45), (45, 50), (50, 55), (55, 60), (60, 95)]:
        step = (anchor.corridor_factor_at(a1)
                - anchor.corridor_factor_at(a0)) / (a1 - a0)
        for a in range(a0, a1):
            assert (anchor.corridor_factor_at(a + 1)
                    - anchor.corridor_factor_at(a)) == pytest.approx(step, abs=1e-6)


def test_corridor_grades_to_100_at_95(variable_ul, anchor):
    """The corridor tail reaches 100% at attained age 95, not at 90.

    The technical notes write the tail as "to 100% at 90-95", which does not say which
    end of the range reaches 100%.  The product spec's footnote 11 does: "The reference
    model linearly interpolates between the quoted ages and grades to 100% at 95."  So
    130% at 60 is joined by one straight line to 100% at 95, and the factor is still
    above 1.00 at every age from 61 to 94.

    The consequence is real, which is why this is pinned rather than left to the CSV.
    A corridor of exactly 1.00 makes DB = AV on an Option A policy funded above its
    face, and the anchor cell is funded above its face long before age 90: the net
    amount at risk - and with it the cost of insurance - would fall to zero for the
    whole tail of the projection.
    """
    assert anchor.corridor_factor_at(60) == pytest.approx(1.30, abs=RATE)
    assert anchor.corridor_factor_at(95) == pytest.approx(1.00, abs=RATE)
    assert anchor.corridor_factor_at(121) == pytest.approx(1.00, abs=RATE)
    # every age strictly inside the last segment is strictly above 1.00
    for a in range(61, 95):
        expected = 1.30 - 0.30 * (a - 60) / 35
        assert anchor.corridor_factor_at(a) == pytest.approx(expected, abs=1e-6)
        assert anchor.corridor_factor_at(a) > 1.00
    assert anchor.corridor_factor_at(90) == pytest.approx(1.042857, abs=RATE)

    # the anchor cell at attained age 90: the corridor, not the face, sets the DB
    t = next(t for t in range(1, anchor.proj_len() + 1) if anchor.age(t) == 90)
    av = anchor.av_pp_at(t, "BEF_FEE")
    assert av > anchor.sum_assured_at(t)
    assert anchor.db_pp(t) == pytest.approx(anchor.corridor_factor(t) * av, rel=1e-12)
    assert anchor.net_amt_at_risk(t) == pytest.approx(av * (1.042857 - 1), rel=1e-6)
    assert anchor.net_amt_at_risk(t) > 30000.0     # zero if the tail graded to 90
    assert anchor.coi_pp(t) > 0.0
    # and it stays positive right up to the age the tail does reach 100%
    for a in (91, 92, 93, 94):
        u = next(t for t in range(1, anchor.proj_len() + 1) if anchor.age(t) == a)
        assert anchor.net_amt_at_risk(u) > 0.0
        assert anchor.coi_pp(u) > 0.0
    # model point 2, the same cell without the month-1 pins, behaves the same way
    p2 = variable_ul.Projection[2]
    assert p2.corridor_factor(t) == pytest.approx(1.042857, abs=RATE)
    assert p2.net_amt_at_risk(t) > 30000.0


def test_pitfall_me_is_charged_once_in_the_unit_value(anchor):
    """"Applying M&E both in the unit-value factor and as a monthly deduction."

    This model picks the unit-value factor, so the monthly deduction is exactly the
    cost of insurance plus the two fixed charges and nothing else, and the M&E is
    recoverable from the balance it was taken off.
    """
    assert anchor.mth_deduction_pp(1) == pytest.approx(
        anchor.coi_pp(1) + anchor.maint_fee_pp(1), rel=1e-12)
    assert anchor.mth_deduction_pp(1) == pytest.approx(WE["md"], abs=CENT)
    for i in (1, 2):
        assert anchor.me_charge_pp(1, i) == pytest.approx(
            anchor.sa_pp_at(1, i, "BEF_ME") * anchor.me_rate_ann / 12, rel=1e-12)
        assert anchor.sa_pp(1, i) == pytest.approx(
            anchor.sa_pp_at(1, i, "BEF_ME") - anchor.me_charge_pp(1, i), rel=1e-12)


def test_pitfall_pro_rata_deduction_guards_the_denominator(variable_ul):
    """"Pro-rata deduction allocation breaking on zero unloaned balances."

    Model point 3 runs its account down to nothing in policy year 50, so the allocation
    denominator goes through zero and turns negative.  Nothing raises, the shares still
    sum to one, and the account value roll-forward stays exact on both sides of it.
    """
    p = variable_ul.Projection[3]
    m = p.first_shortfall_month()
    assert m > 0
    dry = [t for t in range(m, p.proj_len() + 1)
           if p.unloaned_av_pp_at(t, "BEF_FEE") <= 0]
    assert dry, "expected model point 3 to exhaust its unloaned accounts"
    for t in dry[:6]:
        taken = (sum(p.mth_deduction_sa_pp(t, i) for i in p.subaccount_ids())
                 + p.mth_deduction_fa_pp(t))
        assert taken == pytest.approx(p.mth_deduction_pp(t), rel=1e-12)
    assert p.check_av_roll_fwd() is True


def test_pitfall_loan_account_earns_the_credited_rate(variable_ul):
    """"Ignoring the loan account: loaned value earns i_C, not fund returns."

    Model point 4 carries an $8,000 loan.  The collateral grows at the 1.0% credited
    rate, the debt at the 2.0% charged rate, the gap is the insurer's spread, and both
    the death benefit and the cash surrender value are debt-reduced.
    """
    p = variable_ul.Projection[4]
    assert p.loan_bal_init() == 8000.0
    assert p.la_pp(0) == 8000.0
    assert p.loan_cr_rate_ann(1) == 0.01
    assert p.loan_rate_ann(1) == 0.0105          # policy year 11: the preferred tier
    assert p.la_pp(1) == pytest.approx(8000.0 * 1.01 ** (1 / 12), rel=1e-12)
    assert p.loan_bal_pp(1) == pytest.approx(8000.0 * 1.0105 ** (1 / 12), rel=1e-12)
    assert p.loan_bal_pp(1) > p.la_pp(1)
    assert p.loan_spread(1) == pytest.approx(
        8000.0 * (1.0105 ** (1 / 12) - 1.01 ** (1 / 12)) * p.pols_if(1), rel=1e-12)
    # the loan account is part of AV but is excluded from the deduction base
    assert p.av_pp_at(1, "BEF_FEE") == pytest.approx(
        p.unloaned_av_pp_at(1, "BEF_FEE") + p.la_pp(0), rel=1e-12)
    assert p.unloaned_av_pp_at(1, "BEF_FEE") < p.av_pp_at(1, "BEF_FEE")
    # DB and CSV are debt-reduced
    assert p.claim_pp(1, "DEATH") == pytest.approx(
        p.db_pp_eom(1) - p.loan_bal_pp(1), rel=1e-12)
    assert p.ncsv_pp(1) == pytest.approx(p.csv_pp(1) - p.loan_bal_pp(1), rel=1e-12)


def test_loan_rate_steps_to_the_preferred_tier(variable_ul):
    """2.0% charged in policy years 1-9, 1.05% from the 10th anniversary [S1]."""
    p = variable_ul.Projection[3]                # new business, so t tracks duration
    assert p.policy_year(12 * 8 + 1) == 9
    assert p.loan_rate_ann(12 * 8 + 1) == 0.02
    assert p.policy_year(12 * 9 + 1) == 10
    assert p.loan_rate_ann(12 * 9 + 1) == 0.0105
    assert p.loan_cr_rate_ann(12 * 9 + 1) == 0.01


def test_pitfall_age_121_regime_switch(anchor):
    """"Missing the age-121 regime switch (charges stop; asset drags continue)."

    From the anniversary at attained age 121 no premium is accepted and no monthly
    deduction is taken, but the fund expenses and the M&E charge keep coming out of the
    unit values.
    """
    t = next(t for t in range(1, anchor.proj_len() + 1) if anchor.age(t) >= 121)
    assert anchor.age(t - 1) == 120
    assert anchor.premium_pp(t - 1) > 0
    assert anchor.mth_deduction_pp(t - 1) > 0
    assert anchor.premium_pp(t) == 0.0
    assert anchor.coi_pp(t) == 0.0
    assert anchor.maint_fee_pp(t) == 0.0
    assert anchor.mth_deduction_pp(t) == 0.0
    assert anchor.wd_pp(t) == 0.0
    assert anchor.me_charge_pp(t) > 0.0          # asset charges continue
    assert anchor.pols_maturity(t) == 0.0        # and there is no maturity


def test_pitfall_grace_collapse_is_a_diagnostic_only(variable_ul):
    """The default test is reported, not acted on; and read literally it fires at issue.

    On a front-loaded design AV - SC is negative in policy year 1 on a perfectly
    healthy new policy, which is what model point 3 shows.  is_shortfall is the
    companion diagnostic that answers the question the default rule is really asking.
    """
    p = variable_ul.Projection[3]
    assert p.is_default(1) is True               # the notes' literal test, at issue
    assert p.first_default_month() == 1
    assert p.is_shortfall(1) is False            # the account can pay its charges
    assert p.first_shortfall_month() > 1
    assert p.pols_if(2) > 0.0                    # nothing was terminated
    assert p.pols_lapse(1) == pytest.approx(
        p.pols_if(1) * (1 - p.mort_rate_mth(1)) * p.lapse_rate_mth(1), rel=1e-12)


# ---------------------------------------------------------------------------
# Structure, identities and invariants


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + maturities, death before lapse."""
    for t in range(1, 400):
        out = anchor.pols_death(t) + anchor.pols_lapse(t) + anchor.pols_maturity(t)
        assert anchor.pols_if(t) - anchor.pols_if(t + 1) == pytest.approx(
            out, abs=1e-12)
        assert anchor.pols_lapse(t) == pytest.approx(
            anchor.pols_if(t) * (1 - anchor.mort_rate_mth(t))
            * anchor.lapse_rate_mth(t), rel=1e-12)


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(1, anchor.proj_len() + 1):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


@pytest.mark.parametrize("point_id", [1, 2, 3, 4])
def test_account_value_roll_forward_closes(variable_ul, point_id):
    """The notes' processing order, pinned month by month for every model point."""
    assert variable_ul.Projection[point_id].check_av_roll_fwd() is True


@pytest.mark.parametrize("point_id", [1, 2, 3, 4])
def test_margin_identity_closes(variable_ul, point_id):
    assert variable_ul.Projection[point_id].check_margin() is True


@pytest.mark.parametrize("point_id", [1, 2, 3, 4])
def test_gross_and_net_views_reconcile(variable_ul, point_id):
    """"The gross view must reproduce it after adding back the account pass-throughs"."""
    assert variable_ul.Projection[point_id].check_net_view() is True


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(1, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "withdrawals",
        "expenses", "premium_taxes", "net_cf",
    ]
    assert df.loc[1, "premiums"] == pytest.approx(WE["premium"], abs=CENT)
    # the cash flow columns net to net_cf; pols_if is a count, not a cash flow
    cf = df.drop(columns=["pols_if", "net_cf"])
    netted = cf["premiums"] - cf.drop(columns=["premiums"]).sum(axis=1)
    assert (netted - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


def test_result_av_and_result_net_shapes(anchor):
    av = anchor.result_av()
    assert list(av.index) == list(range(1, anchor.proj_len() + 1))
    assert av.loc[1, "av_pp"] == pytest.approx(50506.2245, abs=CENT)
    assert av.loc[1, "sa1_pp"] == pytest.approx(WE["sa1_eom"], abs=CENT)
    assert av.loc[1, "sa2_pp"] == pytest.approx(WE["sa2_eom"], abs=CENT)
    net = anchor.result_net()
    assert set(net.columns) == {
        "prem_gross", "load_income", "md_income", "me_income", "loan_spread",
        "claim_gross", "claim_net", "surr_outgo", "sc_income", "expense",
        "sa_transfer", "av_eop", "naar", "pols_if", "net_cf_ga",
    }
    assert net.loc[1, "load_income"] == pytest.approx(
        WE["load"] * anchor.pols_if(1), abs=CENT)
    assert net.loc[1, "me_income"] == pytest.approx(
        WE["me_total"] * anchor.pols_if(1), abs=CENT)


def test_every_model_point_projects(variable_ul):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in variable_ul.Data.model_point_table().index:
        df = variable_ul.Projection[point_id].result_cf()
        assert len(df) > 0
        assert not df.isna().any().any()


def test_every_model_point_allocates_the_whole_premium(variable_ul):
    """alpha_1 + alpha_2 + alpha_F = 1, or a net premium would vanish."""
    for point_id in variable_ul.Data.model_point_table().index:
        p = variable_ul.Projection[point_id]
        total = sum(p.alloc(i) for i in p.subaccount_ids()) + p.alloc_fixed()
        assert total == pytest.approx(1.0, abs=1e-12)


def test_account_value_is_the_sum_of_its_parts(variable_ul):
    """AV = sum(SA_i) + FA + LA; the debt is not part of it."""
    p = variable_ul.Projection[4]
    assert p.av_pp_init() == pytest.approx(40000 + 25000 + 10000 + 8000, abs=1e-9)
    for t in (0, 1, 12, 120):
        assert p.av_pp(t) == pytest.approx(
            sum(p.sa_pp(t, i) for i in p.subaccount_ids())
            + p.fa_pp(t) + p.la_pp(t), rel=1e-12)


def test_fixed_option_earns_the_declared_rate(variable_ul):
    """FA grows at (1 + i_fix)^(1/12) on the post-deduction balance, floor 1.0%."""
    p = variable_ul.Projection[4]
    assert p.crediting_rate_ann(1) == 0.01
    assert p.fixed_return_mth(1) == pytest.approx(1.01 ** (1 / 12) - 1, rel=1e-12)
    assert p.fa_pp(1) == pytest.approx(
        p.fa_pp_at(1, "BEF_INV") * 1.01 ** (1 / 12), rel=1e-12)


def test_option_b_death_benefit_tracks_the_account_value(variable_ul):
    """Option B: DB = F + AV', so the net amount at risk stays at the face amount."""
    p = variable_ul.Projection[3]
    assert p.db_option() == "B"
    for t in (1, 12, 120):
        assert p.db_pp(t) == pytest.approx(
            max(p.sum_assured_at(t) + p.av_pp_at(t, "BEF_FEE"), p.db_corridor_pp(t)),
            rel=1e-12)
        assert p.net_amt_at_risk(t) == pytest.approx(p.sum_assured_at(t), rel=1e-12)


def test_scenario_is_an_input_and_its_last_month_repeats(anchor):
    """The WE scenario is the worked example's month followed by a level 6% path."""
    level = 1.06 ** (1 / 12) - 1
    assert anchor.gross_return_mth(1, 1) == pytest.approx(0.01, abs=1e-12)
    assert anchor.gross_return_mth(1, 2) == pytest.approx(-0.005, abs=1e-12)
    for t in (2, 3, 500, 900):
        assert anchor.gross_return_mth(t, 1) == pytest.approx(level, abs=1e-9)
        assert anchor.gross_return_mth(t, 2) == pytest.approx(level, abs=1e-9)


def _rejects(message, fn, *args):
    """A formula that raises ValueError(message); modelx wraps it in a FormulaError."""
    with pytest.raises(Exception) as exc:
        fn(*args)
    assert 'raise ValueError("{}")'.format(message) in str(exc.value)


def test_timing_and_kind_arguments_are_validated(anchor):
    """Unknown timing and kind strings raise, as in CashValue_SE, never fall through."""
    for bad in ("BEF_XX", "EOM", ""):
        _rejects("invalid timing", anchor.sa_pp_at, 1, 1, bad)
        _rejects("invalid timing", anchor.fa_pp_at, 1, bad)
        _rejects("invalid timing", anchor.av_pp_at, 1, bad)
    _rejects("invalid timing", anchor.pols_if_at, 1, "BEF_XX")
    _rejects("invalid kind", anchor.claim_pp, 1, "ANNUITIZATION")
    _rejects("invalid kind", anchor.claims, 1, "ANNUITIZATION")
    _rejects("invalid kind", anchor.claims_from_av, 1, "ANNUITIZATION")
    for timing in ("BEF_MAT", "BEF_NB", "BEF_DECR"):
        assert anchor.pols_if_at(1, timing) == anchor.pols_if(1)
    assert anchor.claims_from_av(1, "MATURITY") == 0.0


def test_a_withdrawal_is_not_a_claim(variable_ul, anchor):
    """Withdrawals are `withdrawals(t)`, not a `kind` of `claims(t, kind)`.

    A partial withdrawal is a payment the owner elects, not an event that terminates
    coverage, so it sits in its own `withdrawals` column and is not in the claim total.
    `claim_pp(t, "WITHDRAWAL")` still carries the per-policy amount - it is where the
    rule that the $25 fee is not part of the payment is written - and `withdrawals(t)`
    weights it by `pols_if`, since the withdrawal is taken by policies still in force.
    """
    _rejects("invalid kind", anchor.claims, 1, "WITHDRAWAL")
    assert anchor.claim_pp(1, "WITHDRAWAL") == anchor.wd_pp(1)
    for t in (1, 12, 120):
        assert anchor.withdrawals(t) == pytest.approx(
            anchor.claim_pp(t, "WITHDRAWAL") * anchor.pols_if(t), rel=1e-12)
        # the kind=None total is deaths plus surrenders, and nothing else
        assert anchor.claims(t) == pytest.approx(
            anchor.claims(t, "DEATH") + anchor.claims(t, "LAPSE"), rel=1e-12)
        assert anchor.net_cf(t) == pytest.approx(
            anchor.premiums(t) - anchor.claims(t) - anchor.withdrawals(t)
            - anchor.expenses(t) - anchor.premium_taxes(t), rel=1e-12)
    # every shipped model point has W(t) = 0, the notes' baseline
    for point_id in variable_ul.Data.model_point_table().index:
        p = variable_ul.Projection[point_id]
        assert p.withdrawals(1) == 0.0
        assert p.result_cf()["withdrawals"].abs().max() == 0.0


def test_pols_if_is_the_start_of_month_weight(anchor):
    """`pols_if(t)` is the count at the start of month t and weights that same row.

    The premium row of `result_cf()` divided by the per-policy premium returns the
    in-force column printed beside it, so the two reconcile - which is what makes a
    start-of-period `pols_if` the right weight for a BOM cash flow.
    """
    df = anchor.result_cf()
    for t in (1, 2, 12, 120):
        assert anchor.pols_if_at(t, "BEF_DECR") == anchor.pols_if(t)
        assert (anchor.premiums(t) / anchor.premium_pp(t)
                == pytest.approx(anchor.pols_if(t), rel=1e-12))
        assert df.loc[t, "premiums"] / anchor.premium_pp(t) == pytest.approx(
            df.loc[t, "pols_if"], rel=1e-12)
    assert anchor.pols_if(1) == anchor.pols_if_init()


# ---------------------------------------------------------------------------
# The dynamic behavior module


def test_dynamic_behavior_module_is_off_by_default(anchor):
    """rho = 1 and lambda = 1, so the base run pays the planned premium in full.

    This is what makes the worked example's "$500/month paid" reproduce; Term_US_A
    switches conversion off for the same reason.
    """
    assert anchor.dyn_behavior_on is False
    assert anchor.funding_ratio(1) == 1.0
    assert anchor.prem_persistency(1) == 1.0
    assert anchor.lapse_rate_dyn_mult(1) == 1.0
    assert anchor.premium_pp(1) == pytest.approx(anchor.premium_pp_ann() / 12, abs=CENT)
    assert anchor.lapse_rate(1) == pytest.approx(anchor.lapse_rate_base(1), rel=1e-12)
    # the base scale is still there, and it is not 1
    assert anchor.prem_persistency_base(1) == pytest.approx(0.925, abs=1e-9)


def test_lapse_cliff_spike_is_off_by_default_and_lands_in_one_month(anchor):
    """The notes make the surrender-charge cliff spike optional, magnitude an input."""
    assert anchor.lapse_shock_mult == 1.0
    assert anchor.lapse_shock_month() == 169            # 12 x 14 + 1
    cliff = anchor.lapse_shock_month() - anchor.duration_mth_init()
    assert anchor.duration_mth(cliff) + 1 == 169
    assert anchor.surr_charge_rate(cliff) == 0.0
    assert anchor.surr_charge_rate(cliff - 1) > 0.0
    assert anchor.lapse_rate_sc_mult(cliff) == 1.0     # off
    assert anchor.lapse_rate_sc_mult(cliff + 1) == 1.0


def test_dynamic_behavior_module_can_be_switched_on():
    """Switching it on brings in the pricing path, dynamic lapse and persistency.

    Read in a separate model instance so the shared fixture is not polluted.
    """
    model = mx.read_model(MODEL_PATH, name="VUL_US_S_dyn")
    try:
        model.Projection.dyn_behavior_on = True
        p = model.Projection[3]                        # new business
        # The pricing path is the projection itself when the scenario is the pricing
        # return and the premium is unhaircut, which is policy year 1 here.  They agree
        # to nine figures rather than exactly: the shipped LEVEL6 scenario stores the
        # monthly rate rounded to ten decimals, while the pricing path computes it.
        assert p.scenario_id() == "LEVEL6"
        assert p.pricing_return_mth() == pytest.approx(1.06 ** (1 / 12) - 1, rel=1e-12)
        assert p.av_pricing_pp(0) == 0.0
        assert p.av_pricing_pp(1) == pytest.approx(p.av_pp(1), rel=1e-9)
        assert p.funding_ratio(1) == 1.0               # AV*(0) = 0, guarded
        assert p.funding_ratio(13) == pytest.approx(1.0, rel=1e-9)
        # year 2 drops the premium to the base persistency scale, so funding slips
        assert p.prem_persistency(1) == pytest.approx(1.0, rel=1e-9)
        assert p.funding_ratio(120) < 1.0
        assert p.lapse_rate_dyn_mult(120) > 1.0
        assert p.prem_persistency(120) > p.prem_persistency_base(120)
        # bounds
        for t in (1, 60, 120, 400, 800):
            assert 0.5 <= p.lapse_rate_dyn_mult(t) <= 2.0
            phi = p.funding_ratio(t)
            if phi > 0:
                assert (p.prem_persistency(t) / p.prem_persistency_base(t)
                        == pytest.approx(min(1.3, max(0.7, phi ** -0.25)), rel=1e-12))
        # the identities still close with the module on
        assert p.check_av_roll_fwd() is True
        assert p.check_margin() is True
        assert p.check_net_view() is True
        # an overfunded in-force cell hits the floor and the cap
        q = model.Projection[1]
        assert q.funding_ratio(1) > 1.0
        assert q.lapse_rate_dyn_mult(1) == 0.5
        assert q.prem_persistency(1) == pytest.approx(
            0.7 * q.prem_persistency_base(1), rel=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Round trip


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_PATH)
    try:
        dest = tmp_path / "VUL_US_S"
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in MODEL_PATH.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="VUL_US_S_rt")
    try:
        p = reread.Projection[1]
        assert p.sa_pp(1, 1) == pytest.approx(WE["sa1_eom"], abs=CENT)
        assert p.sa_pp(1, 2) == pytest.approx(WE["sa2_eom"], abs=CENT)
        assert p.net_amt_at_risk(1) == pytest.approx(WE["naar"], abs=CENT)
        assert p.mth_deduction_pp(1) == pytest.approx(WE["md"], abs=CENT)
        assert p.me_charge_pp(1) == pytest.approx(WE["me_total"], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert math.isclose(p.av_pp(1), 50506.2245, abs_tol=CENT)
    finally:
        reread.close()

    written = model_files(dest)
    committed = model_files(MODEL_PATH)
    assert written == committed
