"""Golden and product tests for VA_US_S.

The golden values are the worked example in
products/variable_annuity/technical-notes.md ("Worked example -- one month, two
subaccounts, charge stack, GMDB claim test"), which projects the anchor cell M60 ANB /
single Designated Life / non-qualified / $100,000 single premium / 60-40 allocation /
Flex GMWB Single Core (phi_G 1.25%, b 6.00%, annual CV step-up, s 105%) / Roll-up GMDB
(phi_D 0.90%, rho 6.00%) / m + alpha 1.30% / e_1 0.95%, e_2 0.65%.  They are hard-coded
here rather than pickled so that a reviewer can compare them against the notes by eye.

The example is stated as a **carried state** at the beginning of policy month 27, so it
is asserted twice, on two model points that reach that state by different routes:

* **model point 1** projects from issue on an illustrative return path reverse-engineered
  so that the notes' own narrative -- GWB 100,000 -> 106,000 -> 112,000 -> stepped up to
  112,500, RB = 100,000 x 1.06^2, contract values 104,000 at anniversary 1 and 112,500 at
  anniversary 2, and 66,000 / 44,000 at the beginning of month 27 -- falls out of the
  projection exactly.  Policy month 27 is ``t = 27`` there.
* **model point 2** enters the same carried state directly as an in-force cell, so the
  charge stack reproduces without depending on that return path.  Policy month 27 is
  ``t = 1`` there.

The notes' "Known modeling pitfalls" list is a test list in disguise; there is one test
per entry below.
"""
import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/variable_annuity/VA_US_S"

CENT = 0.005            # money displayed to 2 d.p.
WEIGHT = 5e-7           # value weights displayed to 6 d.p.
FACTOR = 5e-8           # growth factors displayed to 7 d.p.
RATIO = 5e-5            # moneyness ratios displayed to 4 d.p.

# Worked example, the six printed steps.  Per contract, in dollars.
WORKED_EXAMPLE = {
    "sa1_bom": 66000.00,
    "sa2_bom": 44000.00,
    "av_bom": 110000.00,
    "growth_1": 1.0101034,          # 1.0120 x (1 - 0.0095/12) x (1 - 0.0130/12)
    "growth_2": 0.9953805,          # 0.9970 x (1 - 0.0065/12) x (1 - 0.0130/12)
    "sa1_aft_growth": 66666.82,
    "sa2_aft_growth": 43796.74,
    "av_aft_growth": 110463.56,
    "fee_glwb": 351.56,             # (0.0125/4) x GWB 112,500.00
    "fee_gmdb": 252.81,             # (0.0090/4) x RB  112,360.00
    "fee_total": 604.37,
    "weight_1": 0.603519,
    "weight_2": 0.396481,
    "fee_sa1": -364.75,
    "fee_sa2": -239.62,
    "maint_fee": 0.00,              # not an anniversary month, and AV >= $50,000 anyway
    "sa1_eom": 66302.07,
    "sa2_eom": 43557.12,
    "av_eom": 109859.19,
    # Memo lines
    "gross_factor_1": 1.0111988,    # 1.0120 x (1 - 0.0095/12), before the asset charge
    "gross_factor_2": 0.9964600,    # 0.9970 x (1 - 0.0065/12), before the asset charge
    "asset_charge_1": 72.30,
    "asset_charge_2": 47.50,
    "asset_charge": 119.80,
    "fund_expense_1": 52.88,
    "fund_expense_2": 23.76,
    "fund_expense": 76.64,
    "charge_income": 724.17,        # 604.37 + 119.80; the fund expense is NOT included
    "db": 112360.00,
    "gmdb_claim": 2500.81,
    "moneyness_glwb": 1.0240,
    "moneyness_gmdb": 1.0228,
    "lapse_mult": 1.000,
    "lapse_base_ann": 0.040,
    "lapse_mth": 0.003396,
    "cdsc_years": 2,
    "cdsc_rate": 0.065,
    "earnings": 9859.19,
    "free_wd": 10000.00,            # 10% x RP, earnings being the smaller of the two
    "gawa_pct": 0.0400,             # band 60-64, Core, at attained age 62
    "gawa_if_taken_now": 4500.00,   # 4.00% x 112,500.00
}

# The carried state the notes narrate, per contract.
CARRIED_STATE = {
    "av_anniv_1": 104000.00,        # [std illustrative]; below GWB, so no step-up
    "gwb_bonus_1": 106000.00,       # 100,000 + 6% x BB 100,000
    "av_anniv_2": 112500.00,        # [std illustrative]
    "gwb_bonus_2": 112000.00,       # 106,000 + 6% x BB 100,000, before the step-up
    "gwb_anniv_2": 112500.00,       # stepped up to the anniversary contract value
    "bb_anniv_2": 112500.00,
    "bonus_end_anniv_2": 12,        # Bonus Period restarts: y + 10
    "rb_anniv_2": 112360.00,        # 100,000 x 1.06^2
    "np": 100000.00,
    "rp": 100000.00,
    "adj": 105000.00,               # 105% x net premium at endorsement
    "av_month_26": 110000.00,
}


@pytest.fixture(scope="module")
def variable_annuity():
    """The VA_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(variable_annuity):
    """Model point 1 - the worked-example anchor cell, projected from issue."""
    return variable_annuity.Projection[1]


@pytest.fixture(scope="module")
def inforce(variable_annuity):
    """Model point 2 - the worked example's carried state entered as an in-force cell."""
    return variable_annuity.Projection[2]


@pytest.fixture(scope="module")
def depleting(variable_annuity):
    """Model point 3 - the decline scenario that exhausts the contract value."""
    return variable_annuity.Projection[3]


@pytest.fixture(scope="module")
def excess(variable_annuity):
    """Model point 4 - the excess-withdrawal and subsequent-premium variant."""
    return variable_annuity.Projection[4]


@pytest.fixture(scope="module")
def never_wd(variable_annuity):
    """Model point 8 - the never-withdraw cell on the Roll-up GMDB."""
    return variable_annuity.Projection[8]


@pytest.fixture(scope="module")
def basic_gmdb(variable_annuity):
    """Model point 9 - the proportional return-of-premium GMDB, withdrawing from age 70."""
    return variable_annuity.Projection[9]


@pytest.fixture(params=["anchor", "inforce"])
def reading(request, anchor, inforce):
    """Both readings of the worked example, with the projection index of policy month 27.

    Returns ``(projection, t)`` where ``t`` is 27 on the at-issue cell and 1 on the
    in-force cell.  Every worked-example assertion runs against both.
    """
    proj = anchor if request.param == "anchor" else inforce
    return proj, proj.t_of_month(27)


# ---------------------------------------------------------------------------
# The worked example, asserted on both readings


def test_worked_example_step_1_bom_balances(reading):
    """Step 1: BOM balances 66,000.00 / 44,000.00, total 110,000.00."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.sa_pp_at(t, 1, "BEF_PREM") == pytest.approx(g["sa1_bom"], abs=CENT)
    assert p.sa_pp_at(t, 2, "BEF_PREM") == pytest.approx(g["sa2_bom"], abs=CENT)
    assert p.av_pp_at(t, "BEF_PREM") == pytest.approx(g["av_bom"], abs=CENT)


def test_worked_example_steps_2_and_3_no_premium_no_withdrawal(reading):
    """Steps 2-3: no premium and no withdrawal, so AV is unchanged at 110,000.00."""
    p, t = reading
    assert p.premium_pp(t) == 0.0
    assert p.wd_pp(t) == 0.0
    assert p.av_pp_at(t, "BEF_INV") == pytest.approx(
        WORKED_EXAMPLE["av_bom"], abs=CENT)


def test_worked_example_step_4_growth(reading):
    """Step 4: the two growth factors to seven decimals and the resulting balances."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.inv_return_mth(t, 1) == 0.0120
    assert p.inv_return_mth(t, 2) == -0.0030
    assert p.unit_growth(t, 1) == pytest.approx(g["growth_1"], abs=FACTOR)
    assert p.unit_growth(t, 2) == pytest.approx(g["growth_2"], abs=FACTOR)
    assert p.sa_pp_at(t, 1, "BEF_FEE") == pytest.approx(g["sa1_aft_growth"], abs=CENT)
    assert p.sa_pp_at(t, 2, "BEF_FEE") == pytest.approx(g["sa2_aft_growth"], abs=CENT)
    assert p.av_pp_at(t, "BEF_FEE") == pytest.approx(g["av_aft_growth"], abs=CENT)


def test_worked_example_step_5_rider_fees(reading):
    """Step 5: 351.56 on the GWB plus 252.81 on the RB, cancelled pro rata."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.is_quarterly_anniv(t) is True          # the 9th Contract Quarterly Anniv.
    assert p.contract_quarter(t) == 9
    assert p.fee_glwb_pp(t) == pytest.approx(g["fee_glwb"], abs=CENT)
    assert p.fee_gmdb_pp(t) == pytest.approx(g["fee_gmdb"], abs=CENT)
    assert p.charge_pp(t) == pytest.approx(g["fee_total"], abs=CENT)
    assert p.sa_weight(t, 1) == pytest.approx(g["weight_1"], abs=WEIGHT)
    assert p.sa_weight(t, 2) == pytest.approx(g["weight_2"], abs=WEIGHT)
    assert (p.sa_pp(t, 1) - p.sa_pp_at(t, 1, "BEF_FEE")) == pytest.approx(
        g["fee_sa1"], abs=CENT)
    assert (p.sa_pp(t, 2) - p.sa_pp_at(t, 2, "BEF_FEE")) == pytest.approx(
        g["fee_sa2"], abs=CENT)


def test_worked_example_step_6_contract_fee_is_not_charged(reading):
    """Step 6: not an anniversary month, and AV >= $50,000 so it would be waived."""
    p, t = reading
    assert p.is_anniv(t) is False
    assert p.maint_fee_pp(t) == pytest.approx(WORKED_EXAMPLE["maint_fee"], abs=CENT)
    assert p.av_pp(t) >= 50000.0


def test_worked_example_eom_balances(reading):
    """EOM: 66,302.07 / 43,557.12, total 109,859.19.  110,463.56 - 604.37 traces."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.sa_pp(t, 1) == pytest.approx(g["sa1_eom"], abs=CENT)
    assert p.sa_pp(t, 2) == pytest.approx(g["sa2_eom"], abs=CENT)
    assert p.av_pp(t) == pytest.approx(g["av_eom"], abs=CENT)
    assert p.av_pp_at(t, "BEF_FEE") - p.charge_pp(t) == pytest.approx(
        g["av_eom"], abs=CENT)
    # The account fell $140.81 over the month while the guarantee bases did not move.
    assert p.av_pp(t - 1) - p.av_pp(t) == pytest.approx(140.81, abs=CENT)


def test_worked_example_memo_asset_charge(reading):
    """Memo: M&E + admin collected inside the unit value = 72.30 + 47.50 = 119.80."""
    p, t = reading
    g = WORKED_EXAMPLE
    rate = 0.0130 / 12.0
    sa1 = p.sa_pp_at(t, 1, "BEF_INV") * (1 + p.inv_return_mth(t, 1)) * (1 - 0.0095 / 12)
    sa2 = p.sa_pp_at(t, 2, "BEF_INV") * (1 + p.inv_return_mth(t, 2)) * (1 - 0.0065 / 12)
    assert sa1 / p.sa_pp_at(t, 1, "BEF_INV") == pytest.approx(
        g["gross_factor_1"], abs=FACTOR)
    assert sa2 / p.sa_pp_at(t, 2, "BEF_INV") == pytest.approx(
        g["gross_factor_2"], abs=FACTOR)
    assert sa1 * rate == pytest.approx(g["asset_charge_1"], abs=CENT)
    assert sa2 * rate == pytest.approx(g["asset_charge_2"], abs=CENT)
    assert p.asset_charge_pp(t) == pytest.approx(g["asset_charge"], abs=CENT)


def test_worked_example_memo_fund_expense_is_not_insurer_revenue(reading):
    """Memo: fund expense 52.88 + 23.76 = 76.64, paid to the funds, not the insurer."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.fund_expense_pp(t) == pytest.approx(g["fund_expense"], abs=CENT)
    assert p.charge_income_pp(t) == pytest.approx(g["charge_income"], abs=CENT)
    assert g["fund_expense"] not in (p.charge_income_pp(t),)
    # charge income = rider fees + asset charge, and nothing else
    assert p.charge_income_pp(t) == pytest.approx(
        g["fee_total"] + g["asset_charge"], abs=CENT)


def test_worked_example_gmdb_test(reading):
    """DB = max(109,859.19, 100,000.00, 112,360.00) = 112,360.00; claim = 2,500.81."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.np_pp(t) == pytest.approx(CARRIED_STATE["np"], abs=CENT)
    assert p.rb_pp(t) == pytest.approx(CARRIED_STATE["rb_anniv_2"], abs=CENT)
    assert p.db_pp(t) == pytest.approx(g["db"], abs=CENT)
    assert p.gmdb_claim_pp(t) == pytest.approx(g["gmdb_claim"], abs=CENT)
    assert p.db_pp(t) - p.av_pp(t) == pytest.approx(g["gmdb_claim"], abs=CENT)


def test_worked_example_memo_moneyness_and_lapse(reading):
    """Memo: M_G 1.0240, M_D 1.0228, lambda 1.000, base 4.0% p.a., monthly 0.3396%."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.moneyness_glwb(t) == pytest.approx(g["moneyness_glwb"], abs=RATIO)
    assert p.moneyness_gmdb(t) == pytest.approx(g["moneyness_gmdb"], abs=RATIO)
    assert p.lapse_dyn_mult(t) == pytest.approx(g["lapse_mult"], abs=1e-9)
    assert p.lapse_rate_base(t) == pytest.approx(g["lapse_base_ann"], abs=1e-12)
    assert p.lapse_rate(t) == pytest.approx(g["lapse_base_ann"], abs=1e-12)
    assert p.lapse_rate_mth(t) == pytest.approx(g["lapse_mth"], abs=5e-7)


def test_worked_example_memo_cdsc_and_free_withdrawal(reading):
    """Memo: 2 completed years -> 6.5%; earnings 9,859.19 so the free amount is 10,000."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.duration(t) == g["cdsc_years"]
    assert p.surr_charge_rate(t) == pytest.approx(g["cdsc_rate"], abs=1e-12)
    assert p.av_pp(t) - p.rp_pp(t) == pytest.approx(g["earnings"], abs=CENT)
    assert p.free_wd_allow(t) == pytest.approx(g["free_wd"], abs=CENT)
    assert p.rp_pp(t) == pytest.approx(CARRIED_STATE["rp"], abs=CENT)


def test_worked_example_memo_gawa_if_a_first_withdrawal_were_taken_now(reading):
    """Memo: attained age 62 fixes g = 4.00%, so GAWA would be 4,500.00."""
    p, t = reading
    g = WORKED_EXAMPLE
    assert p.age(t) == 62
    assert p.gawa_pct_at_age(62) == pytest.approx(g["gawa_pct"], abs=1e-12)
    assert p.gawa_pct_fixed(t) == 0.0                       # not yet fixed
    assert p.gawa_pp(t) == 0.0
    assert p.gawa_pct_at_age(62) * p.gwb_pp(t) == pytest.approx(
        g["gawa_if_taken_now"], abs=CENT)


def test_worked_example_carried_guarantee_bases(reading):
    """The state the notes carry into month 27: GWB 112,500, BB 112,500, RB 112,360."""
    p, t = reading
    c = CARRIED_STATE
    assert p.gwb_pp_at(t, "BEF_ANNIV") == pytest.approx(c["gwb_anniv_2"], abs=CENT)
    assert p.bb_pp_bef_anniv(t) == pytest.approx(c["bb_anniv_2"], abs=CENT)
    assert p.rb_pp_at(t, "BEF_ANNIV") == pytest.approx(c["rb_anniv_2"], abs=CENT)
    assert p.adj_pp(t) == pytest.approx(c["adj"], abs=CENT)
    assert p.bonus_end(t) == c["bonus_end_anniv_2"]
    assert p.has_wd_by(t) is False


def test_the_two_readings_agree_to_the_cent(anchor, inforce):
    """The at-issue projection and the in-force entry give the same month 27."""
    ta, ti = anchor.t_of_month(27), inforce.t_of_month(27)
    assert (ta, ti) == (27, 1)
    for i in (1, 2):
        assert anchor.sa_pp(ta, i) == pytest.approx(inforce.sa_pp(ti, i), abs=CENT)
    for name in ("av_pp", "fee_glwb_pp", "fee_gmdb_pp", "asset_charge_pp",
                 "fund_expense_pp", "db_pp", "gmdb_claim_pp", "gwb_pp", "rb_pp"):
        assert getattr(anchor, name)(ta) == pytest.approx(
            getattr(inforce, name)(ti), abs=CENT), name


# ---------------------------------------------------------------------------
# The carried state, reproduced from issue on model point 1


def test_anniversary_1_bonus_then_no_step_up(anchor):
    """GWB 100,000 + 6% x BB 100,000 = 106,000; contract value 104,000 is below it."""
    c = CARRIED_STATE
    assert anchor.av_pp(12) == pytest.approx(c["av_anniv_1"], abs=CENT)
    assert anchor.bonus_pp(12) == pytest.approx(6000.00, abs=CENT)
    assert anchor.gwb_pp_aft_bonus(12) == pytest.approx(c["gwb_bonus_1"], abs=CENT)
    assert anchor.is_stepup(12) is False
    assert anchor.gwb_pp(12) == pytest.approx(c["gwb_bonus_1"], abs=CENT)
    assert anchor.bb_pp(12) == pytest.approx(100000.00, abs=CENT)
    assert anchor.rb_pp(12) == pytest.approx(106000.00, abs=CENT)


def test_anniversary_2_bonus_then_step_up_restarts_the_bonus_period(anchor):
    """106,000 + 6,000 = 112,000, then stepped up to the contract value 112,500."""
    c = CARRIED_STATE
    assert anchor.av_pp(24) == pytest.approx(c["av_anniv_2"], abs=CENT)
    assert anchor.bonus_pp(24) == pytest.approx(6000.00, abs=CENT)
    assert anchor.gwb_pp_aft_bonus(24) == pytest.approx(c["gwb_bonus_2"], abs=CENT)
    assert anchor.is_stepup(24) is True
    assert anchor.gwb_pp(24) == pytest.approx(c["gwb_anniv_2"], abs=CENT)
    assert anchor.bb_pp(24) == pytest.approx(c["bb_anniv_2"], abs=CENT)
    assert anchor.bonus_end(23) == 10                       # ten years from issue
    assert anchor.bonus_end(24) == c["bonus_end_anniv_2"]   # restarted at y + 10
    assert anchor.rb_pp(24) == pytest.approx(100000.0 * 1.06 ** 2, rel=1e-12)


def test_month_26_carried_contract_value(anchor):
    """AV(26) = 110,000.00, split exactly 60/40 - which takes two conditions, not one.

    Pro-rata unit cancellation leaves the value weights untouched, and the illustrative
    ``base`` path is reverse-engineered so that the two subaccounts grow at the same rate
    net of fund expense.  Both are needed: unequal growth moves the weights whatever the
    charges do, as the worked-example month itself shows.
    """
    assert anchor.av_pp(26) == pytest.approx(CARRIED_STATE["av_month_26"], abs=CENT)
    assert anchor.sa_pp(26, 1) == pytest.approx(66000.00, abs=CENT)
    assert anchor.sa_pp(26, 2) == pytest.approx(44000.00, abs=CENT)
    assert anchor.sa_pp(26, 1) / anchor.av_pp(26) == pytest.approx(0.60, abs=WEIGHT)
    # Equal net growth up to here: the weight has not moved since issue.
    for t in (1, 12, 13, 25, 26):
        assert anchor.sa_pp(t, 1) / anchor.av_pp(t) == pytest.approx(0.60, abs=WEIGHT)
    # One month of unequal growth and it does move, charges or no charges.
    assert anchor.unit_growth(27, 1) > anchor.unit_growth(27, 2)
    assert anchor.sa_weight(27, 1) == pytest.approx(
        WORKED_EXAMPLE["weight_1"], abs=WEIGHT)
    assert anchor.sa_weight(27, 1) > 0.60 + 100 * WEIGHT


def test_roll_up_is_exactly_compound_before_any_withdrawal(anchor):
    """RB(12y) = 100,000 x 1.06^y for every anniversary before the first withdrawal."""
    for y in range(1, 11):
        assert anchor.rb_pp(12 * y) == pytest.approx(
            100000.0 * 1.06 ** y, rel=1e-12)


# ---------------------------------------------------------------------------
# Known modeling pitfalls -- one test each


def test_pitfall_gross_versus_net_death_claim(anchor):
    """Project DB(t) as the outflow and derive max(0, guarantee - AV) as the strain.

    Never the reverse, never both: the ledger's death line is the gross benefit and the
    general-account strain is a memo, exactly equal to claims - claims_from_av.
    """
    t = 27
    assert anchor.claim_pp(t, "DEATH") == pytest.approx(anchor.db_pp(t), rel=1e-12)
    assert anchor.claims(t, "DEATH") == pytest.approx(
        anchor.db_pp(t) * anchor.pols_death(t), rel=1e-12)
    assert anchor.claims_over_av(t, "DEATH") == pytest.approx(
        anchor.gmdb_claims(t), rel=1e-12)
    assert anchor.gmdb_claims(t) == pytest.approx(
        anchor.gmdb_claim_pp(t) * anchor.pols_death(t), rel=1e-12)
    # The gross benefit is materially larger than the strain, so they cannot be swapped.
    assert anchor.claims(t, "DEATH") > 40 * anchor.gmdb_claims(t)
    assert "gmdb_claims" not in set(anchor.result_cf().columns)


def test_pitfall_the_fee_stops_at_av_zero(depleting):
    """Accruing rider income after depletion flatters the CTE70 tail [S4]."""
    d = next(t for t in range(1, depleting.proj_len() + 1)
             if depleting.depleted_flag(t))
    assert depleting.av_pp(d) == pytest.approx(0.0, abs=0.005)
    for t in range(d + 1, d + 40):
        assert depleting.fee_glwb_pp(t) == 0.0
        assert depleting.fee_gmdb_pp(t) == 0.0
        assert depleting.maint_fee_pp(t) == 0.0
        assert depleting.asset_charge_pp(t) == 0.0
        assert depleting.charge_income_pp(t) == 0.0
    # ... and the guarantee is paying precisely then.
    assert sum(depleting.glwb_payment_pp(t)
               for t in range(d + 1, depleting.proj_len() + 1)) > 0.0
    # No death benefit is payable on subsequent death [S1].
    assert depleting.db_pp(d + 12) == 0.0
    # Surrender at AV = 0 is 0% for a GMWB contract [R1].
    assert depleting.lapse_rate(d + 12) == 0.0


def test_pitfall_withdrawals_are_measured_gross_of_charges(excess):
    """Using net proceeds would understate the benefit-base reduction [S1]."""
    p, t = excess, 61
    assert p.wd_pp(t) == pytest.approx(20000.00, abs=CENT)      # the scheduled gross
    # The contract value falls by the gross amount, not by the cash paid.
    assert p.av_pp_at(t, "BEF_INV") == pytest.approx(
        p.av_pp_at(t, "BEF_WD") - p.wd_pp(t), rel=1e-12)
    assert p.wd_payment_pp(t) == pytest.approx(
        p.wd_pp(t) - p.wd_charge_pp(t), rel=1e-12)
    assert p.wd_charge_pp(t) > 0.0
    assert p.wd_payment_pp(t) < p.wd_pp(t)
    # ... and every guarantee calculation uses the gross figure.
    assert p.sum_wd_pp(t) == pytest.approx(p.wd_pp(t), rel=1e-12)
    assert p.wd_excess_pp(t) + p.wd_nonexcess_pp(t) == pytest.approx(
        p.wd_pp(t), rel=1e-12)


def test_pitfall_excess_withdrawal_ordering(excess):
    """d-f-d on the non-excess portion first, then pro rata against the CV after it [S1].

    Reversing the order changes both GWB and GAWA.  The test pins the notes' algebra
    line by line and then shows that the naive reading -- one proportional reduction for
    the whole withdrawal -- gives a different, lower GWB.
    """
    p, t = excess, 61
    assert p.is_first_wd(t) is True
    assert p.age(t) == 65
    assert p.gawa_pct_at_age(65) == 0.0555
    gwb_pre = p.gwb_pp_at(t, "BEF_WD")
    limit = p.wd_limit_pp(t)
    assert limit == pytest.approx(0.0555 * gwb_pre, rel=1e-12)      # fixed pre-withdrawal
    n = p.wd_nonexcess_pp(t)
    e = p.wd_excess_pp(t)
    assert n == pytest.approx(limit, rel=1e-12)
    assert e == pytest.approx(p.wd_pp(t) - limit, rel=1e-12)
    cv_pre = p.cv_pre_excess_pp(t)
    assert cv_pre == pytest.approx(p.av_pp_at(t, "BEF_WD") - n, rel=1e-12)
    factor = 1.0 - e / cv_pre
    assert p.excess_factor(t) == pytest.approx(factor, rel=1e-12)
    assert p.gwb_pp_at(t, "BEF_ANNIV") == pytest.approx(
        (gwb_pre - n) * factor, rel=1e-12)
    assert p.gawa_pp_at(t, "BEF_ANNIV") == pytest.approx(
        min(limit * factor, p.gwb_pp_at(t, "BEF_ANNIV")), rel=1e-12)
    assert p.bb_pp_bef_anniv(t) == pytest.approx(
        p.gwb_pp_at(t, "BEF_ANNIV"), rel=1e-12)                     # min(GWB, BB)
    # The naive single-proportional reading is materially different.
    naive = gwb_pre * (1.0 - p.wd_pp(t) / p.av_pp_at(t, "BEF_WD"))
    assert naive < p.gwb_pp_at(t, "BEF_ANNIV") - 1.0


def test_pitfall_any_withdrawal_kills_the_years_bonus(anchor):
    """Including automatic withdrawals and RMDs; pro-rating a partial year is wrong [S1]."""
    assert anchor.wd_start_age() == 70
    assert anchor.is_wd_month(121) is True          # first month of contract year 11
    assert anchor.is_wd_year(120) is False          # contract year 10, no withdrawal
    assert anchor.is_wd_year(132) is True           # contract year 11, withdrawal at 121
    assert anchor.bonus_pp(120) > 0.0
    assert anchor.bonus_pp(132) == 0.0
    # The bonus is killed by the withdrawal, not by the Bonus Period running out.
    assert anchor.policy_year(132) <= anchor.bonus_end(131)


def test_pitfall_bonus_period_restarts_on_a_bonus_base_increasing_step_up(
        anchor, never_wd):
    """A hard-coded 10-year window from issue understates the guarantee [S1].

    The restart is asserted on the anchor, where the step-up at anniversary 2 moves the
    end of the Bonus Period from contract year 10 to year 12.  What the restart is
    *worth* has to be shown on the never-withdraw cell, because on the anchor the year-11
    withdrawal suppresses every later bonus anyway - the preceding test asserts exactly
    that - so the anchor demonstrates the open window and point 8 the credits inside it.
    """
    assert anchor.bonus_end(11) == 10               # ten Contract Years from issue
    assert anchor.is_stepup(24) is True
    assert anchor.gwb_pp_aft_stepup(24) > anchor.bb_pp_bef_anniv(24)   # BB increases
    assert anchor.age_at_anniv(24) == 62            # on or before the age-81 anniversary
    assert anchor.bonus_end(24) == 24 // 12 + 10
    # The window is open in contract years 11 and 12, where a hard-coded window from
    # issue would have closed at year 10 ...
    assert anchor.policy_year(144) == 12
    assert anchor.policy_year(144) <= anchor.bonus_end(143)
    # ... but on the anchor no bonus is credited in either year: the first withdrawal at
    # month 121 kills every year's bonus from then on.
    assert anchor.bonus_pp(132) == 0.0
    assert anchor.bonus_pp(144) == 0.0
    # On the never-withdraw cell the two extra years are actually credited, and stop the
    # year after the restarted period ends.
    assert never_wd.wd_start_age() == 0
    assert never_wd.is_stepup(24) is True
    assert never_wd.bonus_end(143) == 12
    assert never_wd.bonus_pp(132) > 0.0             # contract year 11
    assert never_wd.bonus_pp(144) > 0.0             # contract year 12
    assert never_wd.bonus_pp(156) == 0.0            # year 13, the window has closed
    assert never_wd.gwb_pp(144) == pytest.approx(
        never_wd.gwb_pp(120) + never_wd.bonus_pp(132) + never_wd.bonus_pp(144),
        rel=1e-9)


def test_pitfall_gmdb_adjustment_is_applied_at_contract_year_end(excess):
    """Applying it at the withdrawal changes the base the roll-up compounds on [S1]."""
    p, t = excess, 61
    assert p.gmdb_option() == "rollup"
    # The withdrawal accrues but does not move RB in the month it is taken.
    assert p.rb_pp_at(t, "BEF_ANNIV") == pytest.approx(p.rb_pp(t - 1), rel=1e-12)
    assert p.rb_pp(t) == pytest.approx(p.rb_pp(t - 1), rel=1e-12)    # month 61, not an anniv
    assert p.gmdb_dfd_acc_pp(t) > 0.0
    assert p.gmdb_factor_acc(t) < 1.0
    # It lands at the Contract Year end, month 72.
    anniv = 72
    bef = p.rb_pp_at(anniv, "BEF_ANNIV")
    adjusted = (bef - p.gmdb_dfd_acc_pp(anniv)) * p.gmdb_factor_acc(anniv)
    assert p.rb_pp(anniv) == pytest.approx(
        adjusted * (1.0 + p.rollup_rate(anniv)), rel=1e-12)
    assert p.rb_pp(anniv) < bef * (1.0 + p.rollup_rate(anniv))       # the adjustment bit
    # The d-f-d allowance is rho x RB at the *previous* anniversary.
    assert p.gmdb_allow_pp(t) == pytest.approx(0.06 * p.rb_pp(60), rel=1e-12)


def test_pitfall_growth_cutoffs_are_age_based_not_duration_based(anchor, never_wd):
    """Roll-up stops at the anniversary preceding the 81st birthday [S1].

    An issue-age-60 cell therefore gets 20 roll-up credits and an issue-age-75 cell 5.
    Asserted on the never-withdraw cell, whose Benefit Base compounds cleanly with no
    withdrawal adjustment to muddy the arithmetic and whose account is still funded far
    past the cutoff (it does deplete eventually, on rider fees alone - see
    :func:`test_the_never_withdraw_cell_depletes_on_rider_fees_alone`).
    """
    assert anchor.age_at_anniv(240) == 80           # contract year 20
    assert anchor.age_at_anniv(252) == 81           # contract year 21
    credits = [y for y in range(1, 41)
               if anchor.age_at_anniv(12 * y) <= 80]
    assert credits == list(range(1, 21))
    assert never_wd.gmdb_option() == "rollup"
    assert never_wd.depleted_flag(480) is False     # still funded well past the cutoff
    for y in range(1, 21):
        assert never_wd.rb_pp(12 * y) == pytest.approx(
            100000.0 * 1.06 ** y, rel=1e-12)
    plateau = 100000.0 * 1.06 ** 20
    for y in (21, 25, 40):
        assert never_wd.rb_pp(12 * y) == pytest.approx(plateau, rel=1e-12)


def test_the_never_withdraw_cell_depletes_on_rider_fees_alone(never_wd):
    """Point 8 takes no withdrawal and still runs out of account value.

    The two rider charges are levied on benefit bases that only ever rise, so on the
    illustrative return path they exhaust the contract at policy month 555 - attained
    age 106 - with no withdrawal ever taken.  Pinned here because the model point's own
    ``provenance`` says so, and because the depletion turns on the whole post-depletion
    routine: the GAWA% is fixed at the attained-age band at that moment even though no
    withdrawal ever fixed it, and insurer-funded payments follow.
    """
    assert never_wd.wd_start_age() == 0
    assert all(never_wd.wd_pp(t) == 0.0 for t in range(1, 556))
    assert never_wd.depleted_flag(554) is False
    assert never_wd.av_pp(554) > 0.0
    assert never_wd.depleted_flag(555) is True
    assert never_wd.av_pp(555) == pytest.approx(0.0, abs=CENT)
    assert never_wd.age(555) == 106
    # The GAWA% had never been fixed by a withdrawal, so depletion fixes it [S1].
    assert never_wd.gawa_pct_fixed(554) == 0.0
    assert never_wd.gawa_pct_fixed(555) == pytest.approx(0.062, abs=1e-12)
    assert never_wd.gawa_pp(555) == pytest.approx(
        0.062 * never_wd.gwb_pp(555), rel=1e-9)
    # ... and the insurer funds the payments from the next contract year onwards.
    pays = [t for t in range(556, never_wd.proj_len() + 1)
            if never_wd.glwb_payment_pp(t) > 0.0]
    assert pays and pays[0] == 565
    assert all((t - pays[0]) % 12 == 0 for t in pays)
    assert never_wd.glwb_payment_pp(pays[0]) == pytest.approx(
        never_wd.gawa_pp(555), rel=1e-12)


def test_pitfall_charge_base_confusion(reading):
    """Four bases in one stack; putting the rider fee on account value is the error.

    M&E and admin are on **account value**, the rider fees on **benefit bases**, the
    contract fee **per contract**, the CDSC on **Remaining Premium**.
    """
    p, t = reading
    assert p.fee_glwb_pp(t) == pytest.approx(
        (p.phi_glwb(t) / 4.0) * p.gwb_pp_at(t, "BEF_ANNIV"), rel=1e-12)
    assert p.fee_gmdb_pp(t) == pytest.approx(
        (p.phi_gmdb(t) / 4.0) * p.rb_pp_at(t, "BEF_ANNIV"), rel=1e-12)
    # The rider fee on the account value would be a different number entirely.
    assert p.fee_glwb_pp(t) != pytest.approx(
        (p.phi_glwb(t) / 4.0) * p.av_pp(t), abs=1.0)
    assert p.maint_fee_pp(t) in (0.0, 35.0)
    assert p.surr_charge_pp(t) == pytest.approx(
        p.surr_charge_rate(t) * p.surr_chargeable_pp(t), rel=1e-12)
    assert p.surr_chargeable_pp(t) <= p.rp_pp(t) + 1e-9
    assert p.check_charge_split_resid(t) == pytest.approx(0.0, abs=1e-9)


def test_pitfall_no_fixed_account_and_no_mva(variable_annuity):
    """The Roll-up GMDB election removes the Fixed Account Options [S1].

    So there is no market value adjustment and no Model #805 floor: Model #805 expressly
    excludes variable annuities and reaches a VA only through its fixed account under
    Model #250 7.B [REG-R42][REG-R43].  The chassis' `mgsv_pp` and `surr_value_pp` are
    deliberately absent, and the surrender benefit is AV less the CDSC with nothing
    underneath it.
    """
    names = set(variable_annuity.Projection.cells) | set(
        variable_annuity.Projection.refs)
    for absent in ("mgsv_pp", "mgsv_rate", "surr_value_pp", "mva_rate", "mva_pp",
                   "mva_term", "credit_rate"):
        assert absent not in names, absent
    p = variable_annuity.Projection[1]
    assert p.surr_benefit_pp(27) == pytest.approx(
        p.av_pp(27) - p.surr_charge_pp(27), rel=1e-12)


def test_pitfall_rate_sheet_vintage_is_carried(variable_annuity):
    """Every current parameter is dated; an in-force model must carry the vintage [S3]."""
    proj = variable_annuity.Projection
    assert proj.rate_sheet_date == "2026-04-27"
    assert proj.phi_glwb_curr == 0.0125
    assert proj.phi_gmdb_curr == 0.0090
    assert proj.bonus_pct == 0.06
    assert proj.gwb_adj_pct == 1.05
    assert proj.rollup_pct_young == 0.06 and proj.rollup_pct_old == 0.05


def test_pitfall_discretization_drift_three_clocks(anchor):
    """Monthly unit growth, quarterly fee assessment, annual roll-up and bonus [S1][S2]."""
    # Monthly: the unit value moves every month.
    assert anchor.unit_growth(5, 1) != 1.0
    # Quarterly: the rider fees are assessed only at a Contract Quarterly Anniversary.
    assert [t for t in range(1, 13) if anchor.fee_glwb_pp(t) > 0.0] == [3, 6, 9, 12]
    assert [t for t in range(1, 13) if anchor.fee_gmdb_pp(t) > 0.0] == [3, 6, 9, 12]
    # Annual: the roll-up and the bonus are credited only at a Contract Anniversary.
    assert [t for t in range(1, 25) if anchor.bonus_pp(t) > 0.0] == [12, 24]
    assert anchor.rb_pp(11) == pytest.approx(anchor.rb_pp(1), rel=1e-12)
    assert anchor.rb_pp(12) == pytest.approx(anchor.rb_pp(11) * 1.06, rel=1e-12)


# ---------------------------------------------------------------------------
# Guarantee mechanics beyond the worked example


def test_glwb_activation_fixes_the_percentage_on_the_pre_withdrawal_gwb(anchor):
    """Base run [std]: activate at attained age 70 and withdraw 100% of GAWA [R1]."""
    t = 121
    assert anchor.age(t) == 70
    assert anchor.is_first_wd(t) is True
    assert anchor.gawa_pct_at_age(70) == 0.0575
    gwb_pre = anchor.gwb_pp_at(t, "BEF_WD")
    assert anchor.gawa_pct_fixed(t) == 0.0575
    assert anchor.wd_limit_pp(t) == pytest.approx(0.0575 * gwb_pre, rel=1e-12)
    assert anchor.wd_pp(t) == pytest.approx(anchor.wd_limit_pp(t), rel=1e-12)
    # Within the limit, so dollar-for-dollar and no withdrawal charge [S1].
    assert anchor.wd_excess_pp(t) == 0.0
    assert anchor.wd_charge_pp(t) == 0.0
    assert anchor.gwb_pp_at(t, "BEF_ANNIV") == pytest.approx(
        gwb_pre - anchor.wd_pp(t), rel=1e-12)
    # ... and it recurs at the start of every contract year thereafter.
    assert anchor.is_wd_month(133) is True
    assert anchor.is_wd_month(134) is False


def test_gawa_percentage_grid(anchor):
    """35-59 4.00%; 60-64 4.00%; 65-69 5.55%; 70-74 5.75%; 75-80 5.95%; 81+ 6.20% [S3]."""
    expected = {40: 0.0400, 59: 0.0400, 60: 0.0400, 64: 0.0400, 65: 0.0555,
                69: 0.0555, 70: 0.0575, 74: 0.0575, 75: 0.0595, 80: 0.0595,
                81: 0.0620, 95: 0.0620}
    for age, pct in expected.items():
        assert anchor.gawa_pct_at_age(age) == pytest.approx(pct, abs=1e-12)


def test_for_life_guarantee_is_in_effect_from_issue(anchor):
    """Issue age 60 ANB is exactly an actual age of 59 1/2 or more [S1]."""
    assert anchor.forlife_flag() is True
    assert anchor.age_at_entry() == 60


def test_post_depletion_payments_are_life_contingent(depleting):
    """With For Life in effect, GAWA is paid for the life of the Designated Life [S1]."""
    d = next(t for t in range(1, depleting.proj_len() + 1)
             if depleting.depleted_flag(t))
    gawa = depleting.gawa_pp(d)
    assert gawa > 0.0
    assert depleting.forlife_flag() is True
    pay_months = [t for t in range(d + 1, depleting.proj_len() + 1)
                  if depleting.glwb_payment_pp(t) > 0.0]
    assert pay_months, "no post-depletion payment was made"
    # One payment a year, at the start of each contract year, all equal to GAWA.
    assert all((m - pay_months[0]) % 12 == 0 for m in pay_months)
    assert all(depleting.glwb_payment_pp(m) == pytest.approx(gawa, rel=1e-12)
               for m in pay_months)
    # The GWB is not run down, because the payments do not stop at GWB depletion.
    assert depleting.gwb_pp(depleting.proj_len() - 1) == pytest.approx(
        depleting.gwb_pp(d), rel=1e-12)
    # They are weighted by survivorship, so the block runs off with mortality.
    assert depleting.glwb_payments(pay_months[-1]) < depleting.glwb_payments(
        pay_months[0])


def test_gwb_adjustment_date_and_its_voiding(variable_annuity):
    """Later of the anniversary on/after age 70 and the 12th; voided by any withdrawal."""
    never = variable_annuity.Projection[7]
    anchor = variable_annuity.Projection[1]
    assert never.gwb_adj_year() == 12                   # max(12, 70 - 60)
    assert never.is_gwb_adj_date(144) is True
    assert never.wd_start_age() == 0
    assert never.has_wd_by(144) is False
    assert never.adj_pp_bef_anniv(144) == pytest.approx(105000.0, abs=CENT)
    assert never.gwb_pp(144) == pytest.approx(
        max(never.gwb_pp_aft_stepup(144), 105000.0), rel=1e-12)
    assert never.adj_pp(144) == 0.0                     # the provision terminates
    # On the anchor the first withdrawal at month 121 voids it before the date arrives.
    assert anchor.adj_pp(11) == pytest.approx(105000.0, abs=CENT)
    assert anchor.adj_pp(120) == pytest.approx(105000.0, abs=CENT)   # still alive
    assert anchor.is_first_wd(121) is True
    assert anchor.adj_pp(121) == 0.0                                 # voided, no value
    assert anchor.has_wd_by(144) is True
    assert anchor.adj_pp(144) == 0.0
    assert anchor.gwb_pp(144) == pytest.approx(
        anchor.gwb_pp_aft_stepup(144), rel=1e-12)                    # no uplift


def test_benefit_bases_are_capped_at_ten_million(variable_annuity):
    """GWB and Bonus Base are each capped at $10,000,000 [S1]."""
    proj = variable_annuity.Projection
    assert proj.gwb_cap == 10000000.0
    p = variable_annuity.Projection[1]
    for t in (12, 120, 240, 480):
        assert p.gwb_pp(t) <= proj.gwb_cap
        assert p.bb_pp(t) <= proj.gwb_cap


def test_cdsc_band_is_keyed_on_contract_duration_not_premium_vintage(excess):
    """A shipped divergence from the notes, pinned open rather than papered over.

    The notes key the withdrawal charge on "completed years since receipt of the premium
    being withdrawn" [S2]; the model reads the band off the contract duration, because
    ``rp_pp`` carries Remaining Premium as one undifferentiated pool.  The two coincide
    only while the contract is single premium, and model point 4 is not: it pays a second
    $25,000 at policy month 73, which under the notes' own rule would start again in the
    8.5% band.  Splitting the pool needs a withdrawal-ordering rule across tranches that
    no retrieved source states, so the gap is named in the model docstring's and the
    README's *not implemented* lists and asserted here so it cannot change silently.
    """
    p, t = excess, 73
    assert p.premium_pp(t) == pytest.approx(25000.00, abs=CENT)
    assert p.duration(t) == 6                       # completed *contract* years
    assert p.surr_charge_rate(t) == pytest.approx(0.020, abs=1e-12)
    grid = p.data.cdsc_table().loc[p.cdsc_schedule()]
    assert float(grid.loc[0, "surr_charge_rate"]) == pytest.approx(0.085, abs=1e-12)
    # One pool: the new tranche is indistinguishable from the original premium.
    assert p.rp_pp(t) == pytest.approx(
        p.rp_pp(t - 1) + p.premium_pp(t), rel=1e-12)


def test_subsequent_premium_raises_every_base(excess):
    """A premium after the first withdrawal adds g x P(1-tau) to GAWA as well [S1]."""
    t = 73
    p = excess
    assert p.premium_pp(t) == pytest.approx(25000.00, abs=CENT)
    net = p.prem_to_av_pp(t)
    assert p.gwb_pp_at(t, "BEF_WD") == pytest.approx(
        p.gwb_pp_at(t, "BEF_PREM") + net, rel=1e-12)
    assert p.gawa_pp_at(t, "BEF_WD") == pytest.approx(
        p.gawa_pp_at(t, "BEF_PREM") + p.gawa_pct_fixed(t - 1) * net, rel=1e-12)
    assert p.rb_pp_at(t, "BEF_WD") == pytest.approx(
        p.rb_pp_at(t, "BEF_PREM") + net, rel=1e-12)
    assert p.np_pp(t) == pytest.approx(p.np_pp(t - 1) + net, rel=1e-12)
    assert p.rp_pp(t) == pytest.approx(p.rp_pp(t - 1) + p.premium_pp(t), rel=1e-12)
    assert p.av_pp_at(t, "BEF_WD") == pytest.approx(
        p.av_pp(t - 1) + net, rel=1e-12)


def test_dynamic_lapse_multiplier(anchor):
    """lambda(M) = min[1.00, max(0.50, 1 - 1.25(M - 1.10))] [R1]."""
    assert anchor.lapse_itm_mult(1.00) == 1.00          # out of the money, no suppression
    assert anchor.lapse_itm_mult(1.10) == 1.00          # at the threshold
    assert anchor.lapse_itm_mult(1.50) == pytest.approx(1 - 1.25 * 0.40, rel=1e-12)
    assert anchor.lapse_itm_mult(1.60) == pytest.approx(0.50, rel=1e-12)
    assert anchor.lapse_itm_mult(3.00) == 0.50          # floored at 50%
    # The contract carries both a VAGLB and a GMDB, so the lower of the two is used.
    t = 300
    assert anchor.lapse_dyn_mult(t) == pytest.approx(
        min(anchor.lapse_itm_mult(anchor.moneyness_glwb(t)),
            anchor.lapse_itm_mult(anchor.moneyness_gmdb(t))), rel=1e-12)


def test_base_surrender_table_and_the_withdrawal_year_factor(anchor):
    """4.0% in the CDSC period, 25.0% in year 8, 15.0% thereafter; x 0.60 in a wd year."""
    assert anchor.lapse_rate_base(12) == 0.040          # contract year 1
    assert anchor.lapse_rate_base(84) == 0.040          # contract year 7
    assert anchor.lapse_rate_base(96) == 0.250          # contract year 8
    assert anchor.lapse_rate_base(120) == 0.150         # contract year 10
    assert anchor.lapse_wd_factor(120) == 1.00          # no withdrawal in year 10
    assert anchor.lapse_wd_factor(132) == 0.60          # year 11 has one
    assert anchor.lapse_rate(132) == pytest.approx(
        min(1.0, 0.150 * anchor.lapse_dyn_mult(132) * 0.60), rel=1e-12)


def test_highest_quarterly_step_up_basis(variable_annuity):
    """The highest contract value over the four most recent quarterly anniversaries [S1]."""
    p = variable_annuity.Projection[5]
    assert p.stepup_basis() == "highest_quarterly_CV"
    for t in (12, 24, 36):
        assert p.stepup_base_pp(t) == pytest.approx(
            max(p.av_pp(t), p.av_pp(t - 3), p.av_pp(t - 6), p.av_pp(t - 9)), rel=1e-12)
        assert p.stepup_base_pp(t) >= p.av_pp(t)
    # It differs from the annual-CV basis in at least one year, or it is not a variant.
    assert any(p.stepup_base_pp(12 * y) > p.av_pp(12 * y) + 0.01
               for y in range(1, 11))


def test_ratchet_gmdb_and_the_free_basic_death_benefit(variable_annuity):
    """HQAV ratchets to contract value; the included basic benefit carries no charge."""
    ratchet = variable_annuity.Projection[5]
    basic = variable_annuity.Projection[7]
    assert ratchet.gmdb_option() == "HQAV"
    assert ratchet.rb_pp(12) == pytest.approx(
        max(ratchet.rb_pp(11), ratchet.av_pp(12)), rel=1e-12)
    assert ratchet.rb_pp(24) >= ratchet.rb_pp(12)       # never falls without a withdrawal
    assert basic.gmdb_option() == "basic"
    assert basic.phi_gmdb(1) == 0.0
    assert all(basic.fee_gmdb_pp(t) == 0.0 for t in (3, 12, 60, 120))
    assert basic.rb_pp(120) == pytest.approx(100000.0, rel=1e-12)   # no growth, no wd
    # Never withdrawing, the unreduced NP floor and the return-of-premium base coincide.
    assert basic.np_pp(120) == pytest.approx(basic.rb_pp(120), rel=1e-12)
    assert basic.gmdb_guarantee_pp(120) == pytest.approx(100000.0, rel=1e-12)


def test_basic_gmdb_is_reduced_proportionally_and_np_does_not_floor_it(basic_gmdb, anchor):
    """The return-of-premium form falls by ``G <- G x (1 - W/AV_pre)`` [S1][S2].

    The notes' GMDB form table makes the reduction *proportional*, "**not**
    dollar-for-dollar", while their state table updates ``NP`` by premium alone and their
    ``DB = max(AV, NP, RB)`` reads ``NP`` as a floor.  Under ``gmdb_option = "basic"``
    those two are the *same* guarantee, so keeping ``NP`` as a second floor would make
    the emphasized rule unreachable and the election a dead switch: the guarantee would
    sit at the unreduced premium sum for ever.  The elected form governs instead, and the
    two are far apart once the contract has withdrawn - which is the whole content of the
    election.
    """
    p = basic_gmdb
    assert p.gmdb_option() == "basic"
    assert p.wd_start_age() == 70
    t = 121                                     # the first withdrawal, attained age 70
    assert p.is_first_wd(t) is True
    pre = p.rb_pp_at(t, "BEF_WD")
    factor = 1.0 - p.wd_pp(t) / p.av_pp_at(t, "BEF_WD")
    assert pre == pytest.approx(100000.0, rel=1e-12)            # premiums, ungrown
    assert p.rb_pp(t) == pytest.approx(pre * factor, rel=1e-12)
    assert p.rb_pp(t) < pre - 1000.0                            # proportional, not d-f-d
    # NP is not reduced ...
    assert p.np_pp(t) == pytest.approx(100000.0, abs=CENT)
    # ... and does not floor the elected form, or the election would do nothing.
    assert p.gmdb_guarantee_pp(t) == pytest.approx(p.rb_pp(t), rel=1e-12)
    assert p.db_pp(t) == pytest.approx(max(p.av_pp(t), p.rb_pp(t)), rel=1e-12)
    assert p.moneyness_gmdb(t) == pytest.approx(p.rb_pp(t) / p.av_pp(t), rel=1e-12)
    # Ten more years of withdrawals and the gap is the size of the guarantee itself.
    t2 = 240
    assert p.rb_pp(t2) < 0.5 * p.np_pp(t2)
    assert p.gmdb_guarantee_pp(t2) == pytest.approx(p.rb_pp(t2), rel=1e-12)
    assert p.db_pp(t2) == pytest.approx(max(p.av_pp(t2), p.rb_pp(t2)), rel=1e-12)
    # The other elections are untouched: there NP is the *included* return of premium and
    # RB a separately elected base, so the notes' DB = max(AV, NP, RB) stands as printed.
    assert anchor.gmdb_option() == "rollup"
    for t3 in (27, 120, 132, 240):
        assert anchor.gmdb_guarantee_pp(t3) == pytest.approx(
            max(anchor.np_pp(t3), anchor.rb_pp(t3)), rel=1e-12)


def test_vix_linked_fee_reset_reproduces_the_disclosed_examples(variable_annuity):
    """1.45% + 0.05% x (204.42/33 - 10) = 1.26%; 602.30 gives 1.86%, clipped to 1.82%."""
    p = variable_annuity.Projection[6]
    assert p.fee_reset_rule() == "vix"
    # The disclosed figures are printed to two decimals of a percent, so 5e-5 is half a
    # displayed unit: 204.42 gives 1.259728% and 602.30 gives 1.862576%.
    assert p.fee_rate_vix_raw(0.0145, 204.42) == pytest.approx(0.0126, abs=5e-5)
    assert p.fee_rate_vix_raw(0.0145, 602.30) == pytest.approx(0.0186, abs=5e-5)
    assert p.fee_rate_vix_clip(0.0142, 0.0186) == pytest.approx(0.0182, abs=5e-6)
    assert p.fee_rate_vix_clip(0.0142, 0.0126) == pytest.approx(0.0126, abs=5e-6)
    # The absolute corridor is [0.60%, 2.50%].
    assert p.fee_rate_vix_clip(0.0080, 0.0020) == pytest.approx(0.0060, abs=1e-12)
    assert p.fee_rate_vix_clip(0.0245, 0.0400) == pytest.approx(0.0250, abs=1e-12)
    # And the rate actually in force moves quarter by quarter within the band.
    assert p.phi_glwb(3) == 0.0125                      # the initial quarter
    assert p.phi_glwb(6) == pytest.approx(
        p.fee_rate_vix_raw(0.0125, 204.42), abs=5e-7)


def test_cmt_linked_rollup_rate(variable_annuity):
    """10-year CMT + 1.00%, or 1.50% before the first withdrawal, floored 4% capped 8%."""
    p = variable_annuity.Projection[6]
    assert p.rollup_rule() == "cmt_linked"
    assert p.has_wd_by(12) is False
    assert p.rollup_rate(12) == pytest.approx(0.0450 + 0.0150, abs=1e-12)
    assert p.rollup_rate(24) == pytest.approx(0.0300 + 0.0150, abs=1e-12)
    assert p.rollup_rate(240) >= 0.04 and p.rollup_rate(240) <= 0.08
    # The base run's fixed rule is 6.00% at election ages up to 69.
    base = variable_annuity.Projection[1]
    assert base.rollup_rule() == "fixed"
    assert base.rollup_pct() == 0.06
    assert base.rollup_rate(12) == 0.06


def test_quinquennial_fee_increase(variable_annuity):
    """+0.25% at each fifth Contract Anniversary, capped at the 3.00% maximum [S1]."""
    p = variable_annuity.Projection[7]
    assert p.fee_reset_rule() == "quinquennial"
    assert p.phi_glwb(1) == 0.0125                      # contract years 1-5
    assert p.phi_glwb(61) == pytest.approx(0.0150, abs=1e-12)     # after 5 completed
    assert p.phi_glwb(121) == pytest.approx(0.0175, abs=1e-12)
    assert p.phi_glwb(600) == pytest.approx(0.0300, abs=1e-12)    # capped
    assert p.phi_glwb(700) <= 0.0300


# ---------------------------------------------------------------------------
# Roll-forwards, ledger discipline and coverage


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + surrenders + horizon survivors.

    The no-argument boolean is the library-wide form; the per-month signed residual is
    asserted alongside it so a failure says which month broke.
    """
    assert anchor.check_pols_roll_fwd() is True
    for t in range(1, anchor.proj_len() + 1):
        assert anchor.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_account_value_rollforward_closes(anchor):
    """check_av_roll_fwd() is True, and the residual is zero at every month."""
    assert anchor.check_av_roll_fwd() is True
    for t in range(1, anchor.proj_len() + 1):
        assert anchor.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_charge_split_identity_closes(anchor):
    """gross fund return = fund expense + asset charge + the change in AV."""
    assert anchor.check_charge_split() is True
    for t in range(1, anchor.proj_len() + 1):
        assert anchor.check_charge_split_resid(t) == pytest.approx(0.0, abs=1e-8)


def test_the_checks_take_no_argument_and_return_a_bool(anchor):
    """Every ``check_*`` is a no-arg bool over all t, with a ``_resid(t)`` companion.

    So one test can call the same check across the whole library while a debugging
    session can still ask which month failed and by how much.
    """
    for name in ("check_av_roll_fwd", "check_pols_roll_fwd", "check_charge_split"):
        assert getattr(anchor, name)() is True
        assert isinstance(getattr(anchor, name + "_resid")(27), float)


def test_pols_if_is_the_start_of_period_count_and_the_row_weight(anchor):
    """pols_if(t) opens month t, and is the weight on that same row's cash flows.

    The library-wide convention (``Term_US_A``, ``savings.CashValue_SE``): the printed
    in-force column reconciles with the cash flows printed beside it.  The notes' own
    end-of-month ``l(t)`` is ``pols_if_at(t, "AFT_DECR")`` and is one row further down.
    """
    assert anchor.pols_if(0) == anchor.pols_if_init()
    assert anchor.pols_if(1) == anchor.pols_if_init()
    for t in (1, 27, 121, 300):
        assert anchor.pols_if(t) == anchor.pols_if_at(t, "BEF_DECR")
        assert anchor.pols_if(t + 1) == pytest.approx(
            anchor.pols_if_at(t, "AFT_DECR"), rel=1e-15)
        # every weighted line on row t carries exactly pols_if(t)
        assert anchor.premiums(t) == pytest.approx(
            anchor.premium_pp(t) * anchor.pols_if(t), rel=1e-12)
        assert anchor.withdrawals(t) == pytest.approx(
            anchor.wd_payment_pp(t) * anchor.pols_if(t), rel=1e-12)
        assert anchor.asset_charges(t) == pytest.approx(
            anchor.asset_charge_pp(t) * anchor.pols_if(t), rel=1e-12)
        assert anchor.pols_death(t) == pytest.approx(
            anchor.pols_if(t) * anchor.mort_rate_mth(t), rel=1e-12)
    df = anchor.result_cf()
    t = 121                                     # the first withdrawal month
    assert df.loc[t, "premiums"] == pytest.approx(anchor.premiums(t), rel=1e-12)
    assert df.loc[t, "withdrawals"] / anchor.wd_payment_pp(t) == pytest.approx(
        df.loc[t, "pols_if"], rel=1e-12)
    # In the horizon month the survivors leave as pols_maturity, so nothing opens t+1.
    assert anchor.pols_if(anchor.proj_len() + 1) == 0.0
    assert anchor.pols_if_at(anchor.proj_len(), "AFT_DECR") > 0.0


def test_wd_free_pp_is_the_free_allowance_portion(excess):
    """`wd_free_pp` is the free-allowance portion; `wd_exempt_pp` the whole exempt part.

    The chassis (`MYGA_US_S`) uses `wd_free_pp` for the allowance-covered
    portion of a withdrawal, and so does this model.  On this product a second exemption
    stacks on it -- no CDSC within `L` -- so the portion bearing no charge at all is the
    wider `wd_exempt_pp`, and it is that, not `wd_free_pp`, that complements
    `wd_chargeable_pp`.
    """
    p, t = excess, 61
    assert p.wd_excess_pp(t) > 0.0              # an excess withdrawal, so both bite
    assert p.wd_free_pp(t) == pytest.approx(
        min(p.free_wd_avail(t), p.wd_excess_pp(t)), rel=1e-12)
    assert p.wd_exempt_pp(t) == pytest.approx(
        p.wd_nonexcess_pp(t) + p.wd_free_pp(t), rel=1e-12)
    assert p.wd_free_pp(t) < p.wd_exempt_pp(t)           # they are not the same quantity
    assert p.wd_chargeable_pp(t) == pytest.approx(
        p.wd_pp(t) - p.wd_exempt_pp(t), rel=1e-12)
    assert p.wd_charge_pp(t) == pytest.approx(
        p.surr_charge_rate(t) * p.wd_chargeable_pp(t), rel=1e-12)
    # The year-to-date cumulative carries the allowance used so far in the contract year.
    assert p.is_year_start(t) is True                    # month 61 opens contract year 6
    assert p.free_wd_used_cum_pp(t - 1) == 0.0
    assert p.free_wd_used_cum_pp(t) == pytest.approx(p.wd_free_pp(t), rel=1e-12)
    assert p.free_wd_avail(t) == pytest.approx(p.free_wd_allow(t), rel=1e-12)
    assert p.free_wd_used_cum_pp(t + 1) == pytest.approx(
        p.free_wd_used_cum_pp(t) + p.wd_free_pp(t + 1), rel=1e-12)


def test_maturity_is_confined_to_the_last_month(anchor):
    for t in range(1, anchor.proj_len()):
        assert anchor.pols_maturity(t) == 0.0
    assert anchor.pols_maturity(anchor.proj_len()) > 0.0
    assert anchor.pols_if(anchor.proj_len() + 1) == 0.0
    assert anchor.proj_len() == 12 * (120 - 60)


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(0, anchor.proj_len() + 1):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


def test_cdsc_is_reported_but_not_double_counted(excess):
    """The notes' ledger lists the withdrawal charge twice; net_cf counts it once."""
    t = 61
    assert excess.wd_charges(t) == pytest.approx(
        excess.wd_charge_pp(t) * excess.pols_if(t), rel=1e-12)
    assert excess.withdrawals(t) == pytest.approx(
        (excess.wd_pp(t) - excess.wd_charge_pp(t))
        * excess.pols_if(t), rel=1e-12)
    assert "wd_charges" not in set(excess.result_cf().columns)
    assert excess.charge_income(t) == pytest.approx(
        excess.asset_charges(t) + excess.fees_glwb(t)
        + excess.fees_gmdb(t) + excess.maint_fees(t), rel=1e-12)


def test_net_cf_is_the_notes_ledger_and_net_cf_ga_is_the_memo(anchor):
    for t in (0, 27, 121, 300):
        assert anchor.net_cf(t) == pytest.approx(
            anchor.premiums(t) + anchor.charge_income(t)
            - anchor.withdrawals(t) - anchor.glwb_payments(t) - anchor.claims(t)
            - anchor.expenses(t) - anchor.commissions(t) - anchor.premium_taxes(t),
            rel=1e-9)
        assert anchor.net_cf_ga(t) == pytest.approx(
            anchor.charge_income(t) - anchor.gmdb_claims(t)
            - anchor.glwb_payments(t) - anchor.expenses(t)
            - anchor.commissions(t) - anchor.premium_taxes(t), rel=1e-9)
    assert anchor.premiums(0) == 100000.0
    assert anchor.commissions(0) == 0.0                 # not modelled in the base run
    assert anchor.premium_taxes(0) == 0.0


def test_prescribed_maintenance_expense(anchor):
    """[100 x 1.025^(vy - 2015)]/12 per contract per month plus 7 bps of AV [R1]."""
    t = 1
    per_contract = (100.0 / 12.0) * 1.025 ** (2026 - 2015)
    per_av = (0.0007 / 12.0) * anchor.av_pp(t)
    assert anchor.inflation_factor(t) == pytest.approx(1.025 ** 11, rel=1e-12)
    assert anchor.expenses(t) == pytest.approx(
        (per_contract + per_av) * anchor.pols_if(t), rel=1e-12)
    assert anchor.inflation_factor(13) == pytest.approx(1.025 ** 12, rel=1e-12)


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(0, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert set(df.columns) == {
        "pols_if", "premiums", "asset_charges", "fees_glwb", "fees_gmdb",
        "maint_fees", "withdrawals", "glwb_payments", "claims_death",
        "claims_lapse", "claims_maturity", "expenses", "commissions",
        "premium_taxes", "net_cf",
    }
    assert df.loc[0, "premiums"] == pytest.approx(100000.0, abs=CENT)


def test_result_tables_shape(anchor):
    pols = anchor.result_pols()
    assert set(pols.columns) == {
        "pols_if", "pols_death", "pols_lapse", "pols_maturity", "pols_if_aft_decr"}
    av = anchor.result_av()
    assert {"sa_pp_1", "sa_pp_2", "av_pp", "av_pp_bef_fee", "fee_glwb_pp",
            "fee_gmdb_pp", "maint_fee_pp", "asset_charge_pp", "fund_expense_pp",
            "surr_benefit_pp"} == set(av.columns)
    assert av.loc[27, "av_pp"] == pytest.approx(WORKED_EXAMPLE["av_eom"], abs=CENT)
    bases = anchor.result_bases()
    assert {"gwb_pp", "gawa_pp", "bb_pp", "rb_pp", "np_pp", "rp_pp", "adj_pp",
            "wd_pp", "db_pp", "gmdb_claim_pp", "moneyness_glwb",
            "moneyness_gmdb"} == set(bases.columns)
    assert bases.loc[27, "db_pp"] == pytest.approx(WORKED_EXAMPLE["db"], abs=CENT)
    for df in (pols, av, bases):
        assert df.index.name == "t"
        assert len(df) == anchor.proj_len() + 1


def test_every_model_point_projects(variable_annuity):
    """Each of the nine switch combinations must run and close both roll-forwards."""
    for point_id in variable_annuity.Data.model_point_table().index:
        proj = variable_annuity.Projection[point_id]
        df = proj.result_cf()
        assert len(df) == proj.proj_len() + 1
        assert df["net_cf"].notna().all()
        for t in (1, 61, 121, 300):
            if t <= proj.proj_len():
                assert proj.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
                assert proj.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_every_switch_is_exercised_by_a_model_point(variable_annuity):
    """No branch of the notes' parameter set is dead code."""
    table = variable_annuity.Data.model_point_table()
    assert set(table["gmdb_option"]) == {"rollup", "HQAV", "basic"}
    assert set(table["glwb_stepup_basis"]) == {"annual_CV", "highest_quarterly_CV"}
    assert set(table["fee_reset_rule"]) == {"none", "quinquennial", "vix"}
    assert set(table["rollup_rule"]) == {"fixed", "cmt_linked"}
    assert set(table["cdsc_schedule"]) == {"commission_7yr", "none"}
    assert set(table["duration_mth_init"]) == {0, 26}
    assert set(table["wd_start_age"]) == {0, 70}


def test_mortality_table_is_illustrative_not_published(variable_annuity):
    """The prescribed 2012 IAM Basic / Scale G2 basis may not be redistributed here."""
    table = variable_annuity.Data.mort_table()
    assert table["provenance"].str.contains(r"\[std\]").all()
    assert table["provenance"].str.contains("not a published table").all()


def test_invalid_timing_and_kind_arguments_raise(anchor):
    """Unknown timing or kind strings raise ValueError, as CashValue_SE does."""
    with pytest.raises(Exception):
        anchor.av_pp_at(12, "BEF_XYZ")
    with pytest.raises(Exception):
        anchor.pols_if_at(12, "BEF_XYZ")
    with pytest.raises(Exception):
        anchor.gwb_pp_at(12, "BEF_XYZ")
    with pytest.raises(Exception):
        anchor.claim_pp(12, "ANNUITIZATION")
