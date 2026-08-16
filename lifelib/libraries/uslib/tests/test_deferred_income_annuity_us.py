"""Golden and product-specific tests for DIA_US_S.

The golden values are the worked example in
products/deferred_income_annuity/technical-notes.md ("Worked example"), which
projects the anchor cell: Female 60 ANB, nonqualified, Life with Cash Refund, monthly
in arrears, return-of-premium death benefit in deferral, no COLA, $100,000 at issue plus
$50,000 at the start of policy year 6, income start at attained age 80 (T = 240 months).
They are hard-coded here rather than pickled so that a reviewer can compare them against
the notes by eye.

Tolerances follow the precision the notes display: money to the cent, survival to six
decimals, factors to the six decimals they are printed with.

Note the projection index: `t` counts policy months from issue and is **0-based**, the
notes' own convention ("Monthly, indexed t = 0, 1, 2, ... from issue").  The anchor
cell's premiums fall at months 0 and 60 and its income start month is T = 240.
"""
import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/deferred_income_annuity/DIA_US_S"

CENT = 0.005          # money displayed to 2 d.p.
SURV = 5e-7           # survival displayed to 6 d.p.
FACTOR = 2e-6         # factors displayed to 6 d.p.; see test_slice_pricing

# technical-notes.md, "Worked example", the projection table.
# policy year: (age at start, premium at start, CP(t), B(t), l(t), E[DB], E[income])
WORKED_EXAMPLE = {
    1:  (60, 100000.0, 100000.0, 32176.50, 0.994949,  505.08, None),
    5:  (64,      0.0, 100000.0, 32176.50, 0.975000,  494.95, None),
    6:  (65,  50000.0, 150000.0, 44259.65, 0.963743, 1688.54, None),
    10: (69,      0.0, 150000.0, 44259.65, 0.920000, 1611.90, None),
    15: (74,      0.0, 150000.0, 44259.65, 0.838000, 2369.01, None),
    19: (78,      0.0, 150000.0, 44259.65, 0.738063, 3571.09, None),
    20: (79,      0.0, 150000.0, 44259.65, 0.715000, 3459.50, None),
    21: (80,      0.0, 150000.0, 44259.65, 0.680338,    None, 30111.54),
    25: (84,      0.0, 150000.0, 44259.65, 0.557700,    None, 24683.61),
}

# technical-notes.md, "Worked example", "Illustrative factors [std]" and
# "Slice pricing, equation (4)".
SLICES = {
    #  premium month: (premium, deferral yrs, _d p_x, v^d, a_def, A_rop, pr, B_slice)
    0:  (100000.0, 20.0, 0.715000, 0.395293, 2.430657, 0.157900, 0.321765, 32176.50),
    60: ( 50000.0, 15.0, 0.733333, 0.498528, 3.144050, 0.180200, 0.241663, 12083.15),
}

PAYOUT_FACTOR = 8.60          # a^(12)_80(cash refund, female; 4.75%)
TOTAL_INCOME = 44259.65       # B from T, per annum
GUARANTEE_YRS = 3.3891        # n_g = 150,000 / 44,259.65


@pytest.fixture(scope="module")
def deferred_income_annuity():
    """The DIA_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(deferred_income_annuity):
    """Model point 1 - the worked-example anchor cell."""
    return deferred_income_annuity.Projection[1]


# ---------------------------------------------------------------- worked example

@pytest.mark.parametrize("y", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, y):
    """Every cell of the notes' nine-row projection table, to the displayed precision."""
    age, prem, cp, income, surv, db, inc = WORKED_EXAMPLE[y]
    assert anchor.age(12 * (y - 1), 1) == age
    assert sum(anchor.premium_pp(t) for t in range(12 * (y - 1), 12 * y)) == prem
    assert anchor.cum_premium_pp(12 * y - 1) == pytest.approx(cp, abs=CENT)
    assert anchor.annual_income(12 * y - 1) == pytest.approx(income, abs=CENT)
    assert anchor.lives_if_ann(y) == pytest.approx(surv, abs=SURV)
    if db is None:
        assert anchor.claims_ann(y, "DEATH") == 0.0
    else:
        assert anchor.claims_ann(y, "DEATH") == pytest.approx(db, abs=CENT)
    if inc is None:
        assert anchor.annuity_payments_ann(y) == 0.0
    else:
        assert anchor.annuity_payments_ann(y) == pytest.approx(inc, abs=CENT)


def test_worked_example_rows_are_the_result_annual_rows(anchor):
    """result_annual() is the notes' display grid, not a second computation."""
    df = anchor.result_annual()
    for y, (age, prem, cp, income, surv, db, inc) in WORKED_EXAMPLE.items():
        r = df.loc[y]
        assert r["age"] == age
        assert r["premium_pp"] == prem
        assert r["cum_premium_pp"] == pytest.approx(cp, abs=CENT)
        assert r["annual_income"] == pytest.approx(income, abs=CENT)
        assert r["lives_if"] == pytest.approx(surv, abs=SURV)
        assert r["claims_death"] == pytest.approx(db or 0.0, abs=CENT)
        assert r["annuity_payments"] == pytest.approx(inc or 0.0, abs=CENT)


@pytest.mark.parametrize("t", sorted(SLICES))
def test_slice_pricing(anchor, t):
    """Equation (4) slice by slice, against the notes' printed intermediate values.

    a_def is asserted to 2e-6 rather than 5e-7 because the notes evaluate
    `v^20 x _20p_60 x 8.60` from a six-decimal `v^20 = 0.395293`, while the model
    carries `v^20 = 0.39529322`; the two differ in the seventh decimal of a_def.
    """
    prem, defer, surv, disc, a_def, a_rop, pr, b_slice = SLICES[t]
    assert anchor.premium_pp(t) == prem
    assert anchor.deferral_yrs(t) == defer
    assert anchor.surv_to_income_start(t) == pytest.approx(surv, abs=SURV)
    assert anchor.pricing_disc_factor(defer) == pytest.approx(disc, abs=FACTOR)
    assert anchor.payout_factor() == PAYOUT_FACTOR
    assert anchor.rop_factor(t) == a_rop
    assert anchor.annuity_factor_def(t) == pytest.approx(a_def, abs=FACTOR)
    assert anchor.purchase_rate(t) == pr
    assert prem * pr == pytest.approx(b_slice, abs=CENT)


def test_income_is_additive_across_slices(anchor):
    """B = 32,176.50 + 12,083.15 = 44,259.65 per year = 3,688.30 per month.

    "Income is additive across slices, each priced at the annuitant's attained age and
    the remaining deferral at its own payment date."  Nothing accumulates.
    """
    assert anchor.annual_income(0) == pytest.approx(32176.50, abs=CENT)
    assert anchor.annual_income(59) == pytest.approx(32176.50, abs=CENT)
    assert anchor.annual_income(60) == pytest.approx(TOTAL_INCOME, abs=CENT)
    assert anchor.annual_income(240) == pytest.approx(TOTAL_INCOME, abs=CENT)
    assert anchor.annual_income(240) / 12 == pytest.approx(3688.30, abs=CENT)


def test_derived_guarantee_period(anchor):
    """n_g = 150,000/44,259.65 = 3.3891 years, exhausted at attained age about 83.4."""
    assert anchor.guarantee_yrs() == pytest.approx(GUARANTEE_YRS, abs=5e-5)
    assert 80 + anchor.guarantee_yrs() == pytest.approx(83.4, abs=0.05)


def test_death_benefit_fork(deferred_income_annuity, anchor):
    """Setting 1{ROP} = 0 in equation (4) buys 21.2% more income for the same $150,000.

    That difference is the price of the return-of-premium guarantee, and it is mortality
    gain in the insurer's hands if the annuitant dies in deferral: at a year-10 death the
    ROP form pays $150,000 and the no-death-benefit form pays nothing.
    """
    fork = deferred_income_annuity.Projection[4]
    assert fork.db_form() == "NONE"
    assert fork.purchase_rate(0) == 0.386727
    assert fork.purchase_rate(60) == 0.298977
    assert fork.annual_income(60) == pytest.approx(53621.55, abs=CENT)
    uplift = fork.annual_income(60) / anchor.annual_income(60) - 1.0
    assert round(100 * uplift, 1) == 21.2
    assert fork.rop_factor(0) == 0.0
    assert fork.claims_ann(10, "DEATH") == 0.0
    assert anchor.claims_ann(10, "DEATH") == pytest.approx(1611.90, abs=CENT)


def test_policy_year_6_trace(anchor):
    """The notes' trace: the year-6 premium arrives while the annuitant is alive.

    "Expected premium income is 50,000 x l(5) = $48,750.00; it buys slice 2 at the
    age-65 / 15-year purchase rate, taking B from $32,176.50 to $44,259.65 by (8) and CP
    to $150,000 by (7).  Deaths during year 6 (l(5) - l(6) = 0.0112569) now attract the
    larger benefit CP(6) = 150,000, giving E[DB] = $1,688.54."
    """
    assert sum(anchor.premiums(t) for t in range(60, 72)) == pytest.approx(48750.00, abs=CENT)
    assert anchor.lives_if(60, 1) == pytest.approx(0.975000, abs=SURV)
    assert (anchor.lives_if_ann(5) - anchor.lives_if_ann(6)
            == pytest.approx(0.0112569, abs=SURV))
    assert anchor.cum_premium_pp(60) == 150000.0
    assert anchor.claims_ann(6, "DEATH") == pytest.approx(1688.54, abs=CENT)


def test_survival_anchors(anchor):
    """The notes' illustrative five-year survival anchors, reproduced exactly.

    _5p_60 = 0.975000, _10p_60 = 0.920000, _15p_60 = 0.838000, _20p_60 = 0.715000 and
    _5p_80 = 0.780000, with geometric interpolation inside each band - hence
    _15p_65 = 0.715000/0.975000 = 0.733333.
    """
    for yrs, p in ((5, 0.975), (10, 0.920), (15, 0.838), (20, 0.715), (25, 0.715 * 0.78)):
        assert anchor.lives_if(12 * yrs, 1) == pytest.approx(p, abs=SURV)
    assert (anchor.lives_if(300, 1) / anchor.lives_if(240, 1)
            == pytest.approx(0.780000, abs=SURV))
    assert (anchor.lives_if(240, 1) / anchor.lives_if(60, 1)
            == pytest.approx(0.733333, abs=SURV))


# ------------------------------------------------- divergences shipped, not resolved

def test_purchase_rate_rounding_divergence(deferred_income_annuity, anchor):
    """The worked example prices off a six-decimal purchase rate; full precision differs.

    100,000 x 0.321765 = 32,176.50 is the notes' arithmetic.  At full precision
    pr_1 = 0.3217647 and the same premium buys 32,176.47.  Point 1 carries
    purchase_rate_dp = 6 so the golden table reproduces; point 2 is otherwise identical
    and leaves it blank.  Neither is "correct" - the rounding is a [std] convention -
    and the test exists so the 3.6-cent gap cannot be closed silently either way.
    """
    full = deferred_income_annuity.Projection[2]
    assert anchor.purchase_rate_dp() == 6
    assert full.purchase_rate_dp() == -1
    assert full.purchase_rate(0) == pytest.approx(0.3217647212, abs=5e-10)
    assert full.annual_income(60) == pytest.approx(44259.6144, abs=5e-5)
    assert anchor.annual_income(60) - full.annual_income(60) == pytest.approx(0.0356, abs=5e-5)


def test_rop_factor_divergence(deferred_income_annuity, anchor):
    """The notes' A_rop(60, 20) does not reproduce from the recipe the notes state.

    "A_rop is computed from the same survival anchors with a mid-band death-timing
    approximation: A_rop(60, 20) = 0.157900, A_rop(65, 15) = 0.180200."  Run that recipe
    on those anchors and the fifteen-year factor comes out at 0.180241 - agreement to
    four decimals - while the twenty-year factor comes out at 0.161605 against a printed
    0.157900.  Point 1 takes the printed factors and reproduces the worked example;
    point 3 is otherwise identical and computes them.  Both are shipped.
    """
    calc = deferred_income_annuity.Projection[3]
    assert anchor.factor_basis() == "table"
    assert calc.factor_basis() == "formula"
    assert anchor.rop_factor(0) == 0.157900
    assert anchor.rop_factor(60) == 0.180200
    assert calc.rop_factor(0) == pytest.approx(0.161605, abs=5e-7)
    assert calc.rop_factor(60) == pytest.approx(0.180241, abs=5e-7)
    # the fifteen-year slice agrees to the notes' displayed precision, the other does not
    assert abs(calc.rop_factor(60) - 0.180200) < 5e-5
    assert abs(calc.rop_factor(0) - 0.157900) > 5e-4
    assert calc.annual_income(60) == pytest.approx(44106.53, abs=CENT)


def test_the_two_pricing_bases_agree_on_the_payout_factor(deferred_income_annuity, anchor):
    """The shipped mortality table is calibrated so equation (2) returns the notes' 8.60.

    The notes call their illustrative factors "mutually consistent"; the [std] geometric
    continuation of the survival curve past age 85 is chosen so that they are.  What is
    left over is the A_rop divergence above - which is exactly the point of isolating it.
    """
    calc = deferred_income_annuity.Projection[3]
    assert anchor.payout_factor() == PAYOUT_FACTOR
    assert calc.payout_factor() == pytest.approx(PAYOUT_FACTOR, abs=5e-5)
    assert anchor.payout_factor_calc() == pytest.approx(PAYOUT_FACTOR, abs=5e-5)


# ------------------------------------------------------------------ timing and phase

def test_the_first_instalment_falls_at_the_end_of_month_T(anchor):
    """"The income start date is the start of month index T = 240 (20 years from issue);
    under arrears the first payment falls one month later, 241 months from issue - which
    is why policy year 20 (months 228-239) still shows a deferral death benefit and
    policy year 21 (months 240-251) carries the first twelve payments."
    """
    assert anchor.income_start_mth() == 240
    assert anchor.is_payment_mth(239) is False
    assert anchor.is_payment_mth(240) is True
    assert sum(anchor.is_payment_mth(t) for t in range(240, 252)) == 12
    assert anchor.phase(239) == "DEFERRAL"
    assert anchor.phase(240) == "PAYOUT"
    assert anchor.payment_surv_mth(240) == 241
    assert anchor.claims(239, "DEATH") > 0.0
    assert anchor.claims(240, "DEATH") == 0.0
    assert anchor.annuity_payments(239) == 0.0
    assert anchor.annuity_payments(240) > 0.0


def test_a_death_in_the_first_payment_month_refunds_the_whole_of_cp(anchor):
    """"Under arrears, a death between T and T + 1/m yields a cash refund of the full
    CP(T), no payment having been made."
    """
    assert anchor.claim_pp(240, "REFUND") == 150000.0
    assert anchor.claim_pp(241, "REFUND") == pytest.approx(150000.0 - 3688.3042, abs=CENT)
    assert anchor.refund_balance(240) == 150000.0


def test_the_refund_base_is_cumulative_premiums(anchor):
    """A listed pitfall: "For a flexible-premium DIA the cash-refund and
    installment-refund bases are cumulative premiums CP(T), not the initial premium."
    """
    assert anchor.premium_pp(0) == 100000.0
    assert anchor.cum_premium_pp(anchor.income_start_mth()) == 150000.0
    assert anchor.claim_pp(240, "REFUND") == anchor.cum_premium_pp(240)
    assert anchor.claim_pp(240, "REFUND") != anchor.premium_pp(0)


def test_the_refund_runs_out_during_the_fourth_payment_year(anchor):
    """n_g = 3.3891 years, so the guarantee is exhausted during the fourth payment year.

    41 instalments of 3,688.30 total 151,220 > 150,000, so the balance reaches zero
    between the fortieth and the forty-first.
    """
    assert anchor.refund_balance(279) > 0.0            # 40th payment still pending
    assert anchor.refund_balance(280) == pytest.approx(2467.83, abs=CENT)
    assert anchor.refund_balance(281) == 0.0
    assert anchor.claims(281, "REFUND") == 0.0


def test_advance_timing_moves_the_refund_balance_by_one_instalment(
        deferred_income_annuity, anchor):
    """"An advance instalment paid at the start of the death month has been paid - use
    G(t) there or the cash refund is overstated by one instalment."
    """
    adv = deferred_income_annuity.Projection[17]
    assert adv.payment_timing() == "advance"
    assert adv.payment_surv_mth(240) == 240
    assert adv.claim_pp(240, "REFUND") == pytest.approx(
        150000.0 - adv.annuity_pp_sched(240), abs=CENT)
    assert anchor.claim_pp(240, "REFUND") == 150000.0


# ---------------------------------------------------- the payout chassis, DIA-adjusted

def test_cash_refund_carries_no_certain_floor(anchor):
    """Equation (5) is a *pricing* approximation; the projection must not repeat it.

    "For cash refund the benefit is instead a lump-sum shortfall paid at death, so (2)
    is an approximation."  The kernel treats the form as certain-and-life with
    n_g = CP(T)/B; the projected stream is life-contingent with a lump sum at death.
    Carrying the pricing guarantee into the projection would pay it twice.
    """
    assert anchor.payout_form() == "CR"
    assert anchor.guarantee_mths_pricing() == pytest.approx(40.6691, abs=5e-4)
    assert anchor.certain_mths_eff() == 0
    assert anchor.certain_floor(250) == 0.0
    assert anchor.payment_factor(250) == anchor.payment_factor_life(250)


def test_installment_refund_derives_its_certain_period(deferred_income_annuity):
    """n_R: "payments continue in the same amount and frequency until they equal the
    purchase payments", so the guarantee is 41 monthly instalments on this cell.
    """
    ir = deferred_income_annuity.Projection[5]
    assert ir.payout_form() == "IR"
    assert ir.certain_mths_refund() == 41
    assert ir.certain_mths_eff() == 41
    assert ir.certain_floor(240) == 1.0
    assert ir.certain_floor(280) == 1.0
    assert ir.certain_floor(281) == 0.0
    assert ir.cum_annuity_pp(280) >= ir.cum_premium_pp(240)
    assert ir.cum_annuity_pp(279) < ir.cum_premium_pp(240)
    assert ir.claim_pp(250, "REFUND") == 0.0      # delivered as payments, not a lump sum


def test_the_certain_floor_is_conditional_on_reaching_the_income_phase(
        deferred_income_annuity):
    """The one place the payout chassis cannot be carried across unexamined.

    A SPIA is already in payment, so its certain floor is an unweighted indicator.  A
    DIA's guarantee only begins if the contract reaches the income start date: an
    annuitant who dies in deferral takes the return of premium and no instalment is ever
    paid.  Phi inside the guarantee is therefore l_last(T) = 0.715, not 1.0 - an
    absolute 0.285 on the payment factor, a **39.9% overstatement** of the guaranteed
    leg (1/0.715 - 1) if the chassis formula were copied across.  README.md quotes the
    same 39.9%.
    """
    for pid in (5, 7):
        p = deferred_income_annuity.Projection[pid]
        assert p.surv_to_payout() == pytest.approx(0.715000, abs=SURV)
        t = p.income_start_mth() + 10
        assert p.certain_floor(t) == 1.0
        assert p.payment_factor(t) == pytest.approx(0.715000, abs=SURV)
        assert p.payment_factor(t) < 1.0
        assert p.payment_factor(t) > p.payment_factor_life(t)


def test_the_payment_factor_is_a_max_not_a_sum(deferred_income_annuity):
    """The chassis' first-listed pitfall: an additive floor silently doubles the guarantee."""
    for pid in (1, 5, 7):
        p = deferred_income_annuity.Projection[pid]
        assert p.check_payment_factor() is True
        for t in range(0, p.proj_len() + 1, 17):
            assert p.check_payment_factor_resid(t) == 0.0
            assert p.payment_factor(t) <= 1.0


def test_period_certain_pays_the_guarantee_then_reverts_to_the_life_tail(
        deferred_income_annuity):
    """A ten-year period certain covers months 240-359; month 360 is life-contingent."""
    pc = deferred_income_annuity.Projection[7]
    assert pc.certain_mths_eff() == 120
    assert pc.certain_floor(359) == 1.0
    assert pc.certain_floor(360) == 0.0
    assert pc.payment_factor(359) == pytest.approx(0.715000, abs=SURV)
    assert pc.payment_factor(360) == pytest.approx(0.400565, abs=5e-6)
    assert pc.payment_factor(360) == pc.payment_factor_life(360)


def test_joint_triggers_differ_and_the_primary_trigger_costs_more(
        deferred_income_annuity):
    """The two conventions coincide on the primary's death and differ only on the
    secondary's, so the *primary* trigger promises strictly more and buys less income
    per dollar of premium.
    """
    either = deferred_income_annuity.Projection[8]
    primary = deferred_income_annuity.Projection[9]
    assert either.is_joint() and primary.is_joint()
    assert either.reduction_trigger() == "either"
    assert primary.reduction_trigger() == "primary"
    assert primary.payment_factor(300) > either.payment_factor(300)
    assert primary.annual_income(240) < either.annual_income(240)
    # with the primary dead the two formulas coincide: L = delta * l_2 either way
    d, l2 = either.survivor_pct(), 0.5
    assert (0.0 * l2 + d * (0.0 + l2 - 0.0)) == pytest.approx(0.0 + d * 1.0 * l2)


def test_the_joint_rop_factor_prices_the_benefit_the_projection_pays(
        deferred_income_annuity):
    """A listed pitfall read strictly: the purchase rate and the cash flows must carry
    the *same* benefit.

    "Double-counting the deferral death benefit.  Its cost belongs in the purchase rate
    (4) *and* in the projected cash flows."  Equation (3) is written on a single life,
    and on a joint contract this model pays the return of premium on the **last** death
    - "if one annuitant dies in deferral the contract continues on the option chosen at
    issue" [S2] - so `A_rop` is computed on the last-death curve.  Pricing the primary
    life's own density instead would charge 0.161605 for a benefit that costs 0.064820,
    two and a half times the projected exposure, and understate the joint income by
    11.2% (42,358.20 against 47,711.31).
    """
    j = deferred_income_annuity.Projection[8]
    assert j.is_joint()
    assert j.factor_basis() == "formula"
    # the exposure priced is the exposure projected, not the primary life's
    assert 1.0 - j.lives_if(240, 1) == pytest.approx(0.285000, abs=SURV)
    assert 1.0 - j.lives_if_last(240) == pytest.approx(0.128767, abs=SURV)
    assert j.rop_factor(0) == pytest.approx(0.064820, abs=5e-6)
    assert j.rop_factor(60) == pytest.approx(0.080104, abs=5e-6)
    assert j.rop_factor(0) < 0.5 * 0.161605          # not the primary-life factor
    assert j.annual_income(240) == pytest.approx(47711.31, abs=CENT)
    # PV of the projected death claims reconciles to sum_k P_k v^t_k l_last(t_k) A_rop,
    # to the accuracy of the notes' five-year mid-band death-timing approximation
    pv_claims = sum(j.claims(t, "DEATH") * j.pricing_disc_factor((t + 1) / 12.0)
                    for t in range(0, j.income_start_mth()))
    priced = sum(j.premium_pp(tk) * j.pricing_disc_factor(tk / 12.0)
                 * j.lives_if_last(tk) * j.rop_factor(tk)
                 for tk in j.premium_by_mth())
    assert pv_claims == pytest.approx(priced, rel=0.02)
    # a single life is untouched: l_last is the primary curve there
    calc = deferred_income_annuity.Projection[3]
    assert calc.is_joint() is False
    assert calc.rop_factor(0) == pytest.approx(0.161605, abs=5e-7)


def test_cola_is_a_fixed_compound_escalator_on_the_income_start_anniversary(
        deferred_income_annuity):
    """Every observed option is a fixed compound increase, not a CPI adjustment."""
    cola = deferred_income_annuity.Projection[10]
    assert cola.cola_rate() == 0.02
    assert cola.cola_factor(240) == 1.0
    assert cola.cola_factor(251) == 1.0
    assert cola.cola_factor(252) == pytest.approx(1.02)
    assert cola.cola_factor(264) == pytest.approx(1.02 ** 2)
    base = cola.annuity_pp_sched(240)
    assert cola.annuity_pp_sched(251) == pytest.approx(base)
    assert cola.annuity_pp_sched(252) == pytest.approx(base * 1.02)
    assert cola.annuity_pp_sched(264) == pytest.approx(base * 1.02 ** 2)


# ------------------------------------------------------------------ in-force options

def test_start_date_adjustment_repricing_direction(deferred_income_annuity):
    """Equation (11): a_def decreases in d, so deferring raises the payment.

    "Advancing the date reduces the payment; deferring increases it."  Point 13 defers
    the income start by five years at month 120.
    """
    adj = deferred_income_annuity.Projection[13]
    assert adj.adjust_mth() == 120
    assert adj.income_start_mth_init() == 240
    assert adj.income_start_mth() == 300
    assert adj.income_start_mth() - adj.income_start_mth_init() == 60     # +5 years
    assert adj.repricing_rate() == pytest.approx(0.0475)                 # Baa - 100 bp
    assert adj.adjust_income_factor() > 1.0
    assert adj.annual_income(120) == pytest.approx(
        adj.annual_income(119) * adj.adjust_income_factor(), abs=CENT)
    # the premiums were priced to the original date, the payout runs to the new one
    assert adj.income_start_mth_at(0) == 240
    assert adj.income_start_mth_at(120) == 300


def test_payment_acceleration_is_a_timing_shift_not_a_withdrawal(
        deferred_income_annuity):
    """"It is a timing shift expressly labelled 'not a liquidity feature'; the only
    economic cost is (12)."  Six payments in one sum, then five months without.

    What separates a timing shift from a withdrawal is what the *lifetime* income outgo
    does.  Point 14 is point 3 with an acceleration at month 252 and nothing else, and
    over the whole payout the two differ by **153.52** on a 372,585 base - exactly
    `inst * sum_j [ l(t_a+1) - l(t_a+1+j) ]`, the mortality element of equation (12)
    weighted by the cohort in payment when the lump sum falls.  Equation (12)'s interest
    element does not appear because the projection is undiscounted.

    Paying the five accelerated instalments to the whole *initial* cohort - unweighted,
    as if 100% of it were alive and in payment at t_a - would put 6,079.84 there instead,
    fourteen times equation (12)'s own cost of 435.11 and a withdrawal in all but name.
    """
    acc = deferred_income_annuity.Projection[14]
    base = deferred_income_annuity.Projection[3]
    t_a = acc.accel_mth()
    assert t_a == 252
    inst = acc.annuity_pp_sched(t_a)
    assert acc.accel_blackout(t_a) is False
    assert all(acc.accel_blackout(t) for t in range(t_a + 1, t_a + 6))
    assert acc.accel_blackout(t_a + 6) is False
    assert all(acc.annuity_payments(t) == 0.0 for t in range(t_a + 1, t_a + 6))
    assert acc.annuity_payments(t_a + 6) > 0.0
    # six instalments in one sum, all at the one weight the lump sum's own date carries
    phi = acc.payment_factor(t_a)
    assert phi == pytest.approx(0.677527, abs=SURV)
    assert acc.accel_payment_factor(t_a + 3) == phi
    assert acc.accel_payment_factor(t_a + 3) >= acc.payment_factor_life(t_a)
    assert acc.annuity_payments(t_a) == pytest.approx(6 * inst * phi, abs=CENT)
    assert acc.annuity_payments(t_a) == pytest.approx(14941.68, abs=CENT)
    assert acc.annuity_payments(t_a) < inst * phi + 5 * inst      # not the unweighted form
    assert (sum(acc.annuity_payments(t) for t in range(t_a, t_a + 6))
            == pytest.approx(acc.annuity_payments(t_a), abs=CENT))
    # lifetime outgo moves by (12)'s mortality element, not by five whole instalments
    lifetime = sum(acc.annuity_payments(t) for t in range(240, acc.proj_len() + 1))
    unaccel = sum(base.annuity_payments(t) for t in range(240, base.proj_len() + 1))
    eq12_mortality = inst * sum(
        acc.lives_if(t_a + 1, 1) - acc.lives_if(t_a + 1 + j, 1) for j in range(1, 6))
    assert lifetime - unaccel == pytest.approx(eq12_mortality, abs=CENT)
    assert lifetime - unaccel == pytest.approx(153.52, abs=CENT)
    assert 0.0 < lifetime - unaccel < inst          # under one instalment, not five
    assert acc.accel_cost() == pytest.approx(435.1064, abs=5e-4)
    assert 0.0 < acc.accel_cost() < 2 * inst


def test_commutation_leaves_the_life_contingent_tail(deferred_income_annuity):
    """"If you are still living at the end of the period when your guaranteed income
    payments would have stopped, Pacific Life will resume income payments until your
    death" - the life-contingent tail survives commutation, and only Period Certain is
    fully extinguished.
    """
    com = deferred_income_annuity.Projection[15]
    t_c = com.commute_mth()
    assert t_c == 252
    assert com.commute_frac() == 1.0
    assert com.certain_mths_eff() == 120                # months 240-359
    assert com.commute_disc_rate(t_c) == pytest.approx(0.0525)   # i_p + 0 + 50 bp
    assert com.commuted_value(t_c) == pytest.approx(199020.4160, abs=5e-4)
    assert com.commuted_value(t_c - 1) == 0.0
    assert com.commute_frac_cum(t_c - 1) == 0.0
    assert com.commute_frac_cum(t_c) == 1.0
    assert com.commutations(t_c) > 0.0
    assert com.annuity_payments(t_c - 1) > 0.0
    # the commuting cohort's guaranteed instalments stop; what is left over months
    # 252-359 is the beneficiaries' - see the next test
    residual = com.annuity_pp_sched(300) * (com.surv_to_payout()
                                            - com.commute_weight(t_c))
    assert all(com.annuity_payments(t) == pytest.approx(residual, abs=CENT)
               for t in (t_c, 300, 359))
    assert residual < 0.06 * com.annuity_payments(t_c - 1)
    assert com.annuity_payments(360) > 0.0              # the tail resumes
    assert com.annuity_payments(360) > 10 * residual
    assert com.certain_floor(360) == 0.0


def test_a_commutation_extinguishes_exactly_the_guarantee_it_pays_for(
        deferred_income_annuity):
    """A commutation is an exchange, not a benefit: what is paid must equal what stops.

    The cohort that can exercise is the one **alive at t_c** - `l_last(252) = 0.680338` -
    not the one that reached the income phase, `l_last(240) = 0.715000`.  A contract
    whose annuitant died between T and t_c is paying its guarantee to a beneficiary and
    could not have commuted at all.  Weighting the payment by the first and the
    suppression by the second cancels 4.85% more guaranteed liability than the commuted
    value buys - 6,898.37 of present value at i_c on this cell - and that residual is
    precisely the beneficiaries' stream, which the model now keeps paying.
    """
    com = deferred_income_annuity.Projection[15]
    t_c = com.commute_mth()
    assert com.commute_weight(t_c) == pytest.approx(0.680338, abs=SURV)
    assert com.surv_to_payout() == pytest.approx(0.715000, abs=SURV)
    assert com.commute_weight(t_c) < com.surv_to_payout()
    assert com.commute_weight(239) == 0.0          # before the income phase
    assert com.commute_weight(t_c - 1) == 0.0      # before the exercise
    assert com.commute_weight(360) == 0.0          # the life tail is not commutable
    # the identity: PV at i_c of the suppressed instalments is the commutation paid
    assert com.check_commutation_value() is True
    assert com.check_commutation_value_resid(t_c) == pytest.approx(0.0, abs=1e-6)
    assert com.commutations(t_c) == pytest.approx(
        com.commuted_value(t_c) * com.commute_weight(t_c), abs=CENT)
    # and what the mismatched weights would have cancelled for nothing
    i_c = com.commute_disc_rate(t_c)
    residual = sum(com.annuity_payments(s) * (1.0 + i_c) ** (-(s - t_c) / 12.0)
                   for s in range(t_c, 360))
    assert residual == pytest.approx(6898.37, abs=0.05)
    assert residual == pytest.approx(
        com.commuted_value(t_c) * (com.surv_to_payout() - com.commute_weight(t_c)),
        abs=CENT)
    assert residual / (com.commuted_value(t_c) * com.surv_to_payout()) == pytest.approx(
        0.0485, abs=5e-5)


def test_the_commuted_value_is_zero_where_there_is_nothing_guaranteed(anchor):
    """A cash refund is a lump sum at death, not a schedule of payments."""
    assert anchor.certain_mths_eff() == 0
    assert anchor.commute_mth() == -1
    assert anchor.commuted_value(250) == 0.0
    assert all(anchor.commutations(t) == 0.0 for t in range(0, 400, 37))


# ------------------------------------------------------------------- QLAC overlay

def test_qlac_overlay_flags_but_generates_no_cash_flows(deferred_income_annuity):
    """"It generates no cash flows of its own - it caps premiums, restricts forms,
    constrains T, disables features and raises compliance flags."  The 2026 limit is
    $210,000 and there is no percentage-of-account-balance test.
    """
    ok = deferred_income_annuity.Projection[11]
    bad = deferred_income_annuity.Projection[12]
    assert ok.is_qlac() and bad.is_qlac()
    assert ok.qlac_premium_limit == 210000.0
    assert ok.cum_premium_pp(0) == 210000.0
    assert ok.qlac_room(0) == 0.0
    assert ok.qlac_flags() == []
    assert bad.cum_premium_pp(0) == 250000.0
    assert bad.qlac_room(0) == -40000.0
    assert "premium limit exceeded" in bad.qlac_flags()
    # the flag changes no cash flow: the two differ only through the premium itself
    assert bad.annual_income(300) / ok.annual_income(300) == pytest.approx(
        250000.0 / 210000.0, rel=1e-9)
    assert ok.age(ok.income_start_mth(), 1) == 85       # the regulation's outside date


def test_a_nonqualified_contract_raises_no_qlac_flags(anchor):
    assert anchor.market_type() == "NQ"
    assert anchor.is_qlac() is False
    assert anchor.qlac_flags() == []


# ------------------------------------------------------------------ mortality basis

def test_generational_construction(deferred_income_annuity, anchor):
    """q^(2012+k) = q^(2012) x (1 - G2_x)^k, k = calendar year less the table year.

    The shipped scale is 1% at ages up to 85, and the anchor cell is issued in 2026, so
    the issue-age rate is the table rate times 0.99^14.
    """
    gen = deferred_income_annuity.Projection[16]
    assert gen.mort_basis() == "generational"
    assert anchor.mort_basis() == "anchor"
    assert gen.calendar_year(0) - gen.mort_table_year == 14
    assert gen.improvement_rate(0, 1) == 0.01
    assert gen.mort_rate(0, 1) == pytest.approx(
        anchor.mort_rate_base(0, 1) * 0.99 ** 14, rel=1e-12)
    assert gen.mort_rate(0, 1) < anchor.mort_rate(0, 1)
    assert gen.annual_income(240) < anchor.annual_income(240)   # lighter mortality costs more


# ------------------------------------------------------------ roll-forwards and shape

def test_inforce_rollforward_closes(anchor):
    """l(t) - d(t) - l(t+1) = 0 for every month; mortality is the only decrement.

    `check_lives_roll_fwd()` takes no argument and covers every projected month in one
    call - the library-wide `check_*` shape; `check_lives_roll_fwd_resid(t)` is the
    signed residual a failure would be diagnosed with.
    """
    assert anchor.check_lives_roll_fwd() is True
    for t in range(0, anchor.proj_len() + 1, 7):
        assert anchor.check_lives_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-14)


def test_income_rollforward_closes(anchor):
    """B(t) - B(t-1) - P_k * pr = 0: income moves only when a premium is paid.

    There is no credited rate, no index, no charge and no balance in this product, so
    nothing else can move B.
    """
    assert anchor.check_income_roll_fwd() is True
    for t in range(0, 300):
        assert anchor.check_income_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-9)


def test_the_cross_model_names_are_the_canonical_ones(deferred_income_annuity, anchor):
    """The shared vocabulary this model is obliged to spell the library's way.

    `mort_ae_factor` (not `ae_factor`), `omega_age` (not `omega`), and every `check_*`
    as a no-argument bool with a `check_*_resid(t)` companion.  Asserted by name so a
    rename cannot drift back: these are the concepts the library shares across all twelve
    reference models, and a model that spells one of them privately is unusable in a
    cross-model test.
    """
    refs = set(deferred_income_annuity.Projection.refs)
    cells = set(deferred_income_annuity.Projection.cells)
    assert "mort_ae_factor" in refs and "ae_factor" not in refs
    assert "omega_age" in refs and "omega" not in refs
    assert anchor.mort_ae_factor == 1.0
    assert anchor.omega_age == 120
    checks = {n for n in cells if n.startswith("check_") and not n.endswith("_resid")}
    assert checks == {"check_lives_roll_fwd", "check_income_roll_fwd",
                      "check_payment_factor", "check_commutation_value"}
    for n in checks:
        assert deferred_income_annuity.Projection.cells[n].parameters == ()
        assert n + "_resid" in cells
        assert deferred_income_annuity.Projection.cells[n + "_resid"].parameters == ("t",)
        assert getattr(anchor, n)() is True


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(0, anchor.proj_len() + 1, 11):
        assert 0.0 <= anchor.lives_if(t, 1) <= 1.0
        assert anchor.lives_if(t + 1, 1) <= anchor.lives_if(t, 1) + 1e-15


def test_there_is_no_lapse_decrement_and_no_account_value(deferred_income_annuity):
    """A listed pitfall, twice over.

    "Lapse and surrender: exactly zero, at all durations.  A nonzero lapse assumption in
    a DIA model is a defect, not a margin."  And: "Building an account-value
    roll-forward.  The liability is a schedule of income slices keyed on (premium,
    purchase date, income start date, income option), not a balance.  Any credited rate,
    charge or interim value invented to fill a template is fictitious."
    """
    names = set(deferred_income_annuity.Projection.cells)
    names |= set(deferred_income_annuity.Projection.refs)
    names |= set(deferred_income_annuity.Data.cells)
    forbidden = ("lapse", "surr_charge", "surrender", "av_pp", "av_at", "account_value",
                 "crediting", "credit_rate", "interim_value", "benefit_base",
                 "annuitization_rate", "free_withdrawal", "market_value_adj")
    for n in names:
        for bad in forbidden:
            assert bad not in n, "{} looks like a parameter this product does not have".format(n)
    anchor = deferred_income_annuity.Projection[1]
    cf = anchor.result_cf()
    assert set(cf.columns) == {
        "pols_if", "premiums", "annuity_payments", "claims", "commutations",
        "expenses", "liability_cf", "net_cf",
    }


def test_result_cf_shape(anchor):
    """t is 0-based: the frame starts at month 0, the issue month."""
    df = anchor.result_cf()
    assert list(df.index) == list(range(0, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert anchor.proj_len() == 719                # to omega_age = 120, a life aged 60
    assert df.loc[0, "premiums"] == 100000.0
    assert df.loc[60, "premiums"] == pytest.approx(48750.0, abs=CENT)
    assert df.loc[0, "net_cf"] == pytest.approx(
        100000.0 - anchor.claims(0) - anchor.expenses(0), abs=CENT)


def test_result_annual_shape(anchor):
    df = anchor.result_annual()
    assert list(df.index) == list(range(1, 61))
    assert df.index.name == "policy_year"
    assert set(df.columns) == {
        "age", "premium_pp", "cum_premium_pp", "annual_income", "lives_if",
        "claims_death", "claims_refund", "annuity_payments",
    }


def test_result_pols_shape(anchor):
    df = anchor.result_pols()
    assert list(df.index) == list(range(0, anchor.proj_len() + 1))
    assert df.loc[0, "lives_if_1"] == 1.0
    assert df.loc[0, "lives_if_2"] == 0.0       # single-life contract


def test_maintenance_expense(anchor):
    """$50 per contract per year escalated at 2.5%, VM-22's prescribed figure adopted
    as the best estimate [std]."""
    assert anchor.expenses(0) == pytest.approx(50.0 / 12, abs=1e-9)
    assert anchor.inflation_factor(12) == pytest.approx(1.025)
    assert anchor.expenses(12) == pytest.approx(
        50.0 / 12 * 1.025 * anchor.lives_if_last(12), abs=1e-9)


def test_every_model_point_projects(deferred_income_annuity):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in deferred_income_annuity.Data.model_point_table().index:
        proj = deferred_income_annuity.Projection[point_id]
        df = proj.result_cf()
        assert len(df) > 0
        assert df.notna().all().all()
        assert proj.annual_income(proj.income_start_mth()) > 0.0


def test_the_premium_schedule_is_a_separate_table(deferred_income_annuity):
    """A flexible-premium contract takes an unbounded number of slices, so the schedule
    cannot live in a fixed set of model point columns."""
    anchor = deferred_income_annuity.Projection[1]
    assert anchor.premium_by_mth() == {0: 100000.0, 60: 50000.0}
    assert len(anchor.premium_schedule()) == 2
    single = deferred_income_annuity.Projection[11]
    assert single.premium_by_mth() == {0: 210000.0}
