"""Golden and product-specific tests for SPIA_US_S.

The golden values are the worked example in
products/immediate_annuity/technical-notes.md ("Worked example"), which projects the
anchor cell: P = $100,000, B(1) = $6,000 p.a. (inst = $500.00/month), joint form with
primary male ANB 65 and joint annuitant female ANB 62, monthly (m = 12) in arrears,
3% compound COLA, survivor percentage 2/3, no certain period, and the scenario "the
joint (secondary) annuitant dies during month 14; the primary survives throughout".
The notes run the two survivor-reduction triggers side by side -- this is the death that
distinguishes them -- so the table has two cash flow columns, reproduced here by model
point 1 (trig = either) and model point 2 (trig = primary).

They are hard-coded rather than pickled so that a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent,
payment factors to the four decimals of the notes' trace.

The notes' "Known modeling pitfalls" section is a test list in disguise; there is one
test below per pitfall that can be asserted against the shipped model points.
"""
import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/immediate_annuity/SPIA_US_S"

CENT = 0.005          # money displayed to 2 d.p.
FACTOR = 5e-5         # payment factors quoted to 4 d.p. in the notes' trace

# Worked example, "Worked example" table:
#   t: (unreduced inst(t), CF with trig = either, CF with trig = primary)
WORKED_EXAMPLE = {
    1:  (500.00, 500.00, 500.00),   # first monthly instalment (arrears)
    12: (500.00, 500.00, 500.00),   # 12th instalment
    13: (515.00, 515.00, 515.00),   # anniversary: B <- 6,180.00
    14: (515.00, 343.33, 515.00),   # joint annuitant dies during the month
    15: (515.00, 343.33, 515.00),
    24: (515.00, 343.33, 515.00),
    25: (530.45, 353.63, 530.45),   # anniversary: B <- 6,365.40
}

# "Income levels: year 1 B = 6,000.00; year 2 B = 6,180.00; year 3 B = 6,365.40."
INCOME_LEVELS = {1: 6000.00, 2: 6180.00, 3: 6365.40}


@pytest.fixture(scope="module")
def immediate_annuity():
    """The SPIA_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(immediate_annuity):
    """Model point 1 -- the worked-example anchor cell, trig = either."""
    return immediate_annuity.Projection[1]


@pytest.fixture(scope="module")
def anchor_primary(immediate_annuity):
    """Model point 2 -- the same cell run with trig = primary."""
    return immediate_annuity.Projection[2]


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, anchor_primary, t):
    """Every cell of the notes' worked-example table, to the displayed precision.

    The table's "CF" column is the annuity instalment, not the notes' own
    ``CF(t) = E[ANN] + E[CR] + E[COMM] + E[EXP]``: at t = 1 it shows 500.00, not the
    505.00 that definition gives once the $5.00 monthly maintenance expense is added.
    It is therefore asserted against ``annuity_payments``; ``liability_cf`` is checked
    separately in :func:`test_liability_cf_adds_the_maintenance_expense`.
    """
    inst, cf_either, cf_primary = WORKED_EXAMPLE[t]
    assert anchor.annuity_pp(t) == pytest.approx(inst, abs=CENT)
    assert anchor_primary.annuity_pp(t) == pytest.approx(inst, abs=CENT)
    assert anchor.annuity_payments(t) == pytest.approx(cf_either, abs=CENT)
    assert anchor_primary.annuity_payments(t) == pytest.approx(cf_primary, abs=CENT)


def test_income_levels_escalate_at_each_anniversary(anchor):
    """B(1) = 6,000.00; B(2) = 6,180.00; B(3) = 6,365.40, compound at g = 3% [S1][S4]."""
    for y, b in INCOME_LEVELS.items():
        assert anchor.annual_income(y) == pytest.approx(b, abs=CENT)
    assert anchor.annuity_pp_sched(12) == pytest.approx(500.00, abs=CENT)
    assert anchor.annuity_pp_sched(13) == pytest.approx(515.00, abs=CENT)
    assert anchor.annuity_pp_sched(25) == pytest.approx(530.45, abs=CENT)


def test_trigger_split_at_month_14(anchor, anchor_primary):
    """The notes' trace: L = 0.6667 on `either`, L = 1 on `primary`, at the payment point.

    "The death is decremented at the end of month 14, so the scenario values at the
    payment point are l1 = 1, l2 = 0."
    """
    assert anchor.lives_if(14, 1) == 1.0
    assert anchor.lives_if(14, 2) == 0.0
    assert anchor.lives_if(13, 2) == 1.0
    assert anchor.payment_factor_life(14) == pytest.approx(2 / 3, abs=FACTOR)
    assert anchor.certain_floor(14) == 0.0
    assert anchor.payment_factor(14) == pytest.approx(2 / 3, abs=FACTOR)
    assert anchor_primary.payment_factor_life(14) == pytest.approx(1.0, abs=FACTOR)
    assert anchor.annuity_payments(14) == pytest.approx(515.00 * 2 / 3, abs=CENT)


def test_the_timing_convention_bites_at_14_not_15(anchor):
    """"The instalment due at the end of the month of death is already the first
    scheduled payment date after the death" -- so t = 14 is reduced, not t = 15.
    """
    assert anchor.annuity_payments(13) == pytest.approx(515.00, abs=CENT)
    assert anchor.annuity_payments(14) == pytest.approx(343.33, abs=CENT)
    assert anchor.payment_surv_mth(14) == 14          # arrears: end of the month


def test_reversing_the_death_makes_the_two_triggers_coincide(immediate_annuity):
    """The notes' reverse check: primary dies in month 14, joint annuitant survives.

    "L_either = 0 + (2/3)(0 + 1 - 0) = 2/3 and L_primary = 0 + (2/3)(1)(1) = 2/3.
    Both conventions pay 343.33 from t = 14."  The two triggers coincide on the
    primary's death and differ only on the secondary's -- which is why the trigger must
    be a model switch, not a footnote.
    """
    either, primary = immediate_annuity.Projection[3], immediate_annuity.Projection[4]
    for p in (either, primary):
        assert p.lives_if(14, 1) == 0.0
        assert p.lives_if(14, 2) == 1.0
        assert p.payment_factor_life(14) == pytest.approx(2 / 3, abs=FACTOR)
        assert p.annuity_payments(13) == pytest.approx(515.00, abs=CENT)
        assert p.annuity_payments(14) == pytest.approx(343.33, abs=CENT)
        assert p.annuity_payments(25) == pytest.approx(353.63, abs=CENT)


def test_cola_continues_after_the_survivor_reduction(anchor):
    """delta applies to the *current* income payment [S2], so 343.33 becomes 353.63 at
    t = 25 -- not a frozen 343.33."""
    assert anchor.annuity_payments(24) == pytest.approx(343.33, abs=CENT)
    assert anchor.annuity_payments(25) == pytest.approx(353.63, abs=CENT)
    assert anchor.annuity_payments(25) != pytest.approx(343.33, abs=0.01)


def test_a_certain_period_defers_the_reduction_to_its_end(immediate_annuity):
    """The notes' 10-year-certain check, reproduced with no extra logic [S5].

    "With a 10-year certain period (n = 120): C(t) = 1 for t <= 120, so
    Phi(t) = max(1, L(t)) = 1 and every instalment from t = 14 to t = 120 is the full
    515.00 / 530.45 / ..., with the reduction to delta beginning only at t = 121."
    """
    p = immediate_annuity.Projection[5]
    assert p.certain_mths_eff() == 120
    for t in (14, 15, 24):
        assert p.certain_floor(t) == 1.0
        assert p.payment_factor(t) == pytest.approx(1.0, abs=FACTOR)
        assert p.annuity_payments(t) == pytest.approx(515.00, abs=CENT)
    assert p.annuity_payments(25) == pytest.approx(530.45, abs=CENT)
    # B(10) = 6,000 x 1.03^9 = 7,828.6391 => 652.39 a month, still unreduced at t = 120.
    full_120 = 6000.0 * 1.03 ** 9 / 12
    assert p.annuity_payments(120) == pytest.approx(full_120, abs=CENT)
    # t = 121: the floor is gone, the reduction to delta finally applies.
    full_121 = 6000.0 * 1.03 ** 10 / 12
    assert p.certain_floor(121) == 0.0
    assert p.annuity_payments(121) == pytest.approx(full_121 * 2 / 3, abs=CENT)


def test_cash_refund_lump_sum(immediate_annuity):
    """"Single-life with cash refund, death in month 14: lump sum =
    max(0, 100,000 - G(13)) = 100,000 - (12 x 500.00 + 515.00) = 93,485.00" [S1][S3][S5].
    """
    p = immediate_annuity.Projection[6]
    assert p.cum_annuity_pp(13) == pytest.approx(12 * 500.00 + 515.00, abs=CENT)
    assert p.claim_pp(14, "REFUND") == pytest.approx(93485.00, abs=CENT)
    assert p.claims(14) == pytest.approx(93485.00, abs=CENT)
    assert p.claims(14, "REFUND") == pytest.approx(93485.00, abs=CENT)
    # Paid once, at the terminating death, and never again.
    assert p.claims(13) == 0.0
    assert p.claims(15) == 0.0


def test_derived_installment_refund_period(immediate_annuity):
    """"On installment refund (level path, no COLA) the derived certain period is
    12 x 100,000/6,000 = 200 months" [S5]."""
    p = immediate_annuity.Projection[7]
    assert p.certain_mths_refund() == 200
    assert p.certain_mths_eff() == 200
    assert p.cum_annuity_pp(200) == pytest.approx(100000.00, abs=CENT)
    assert p.cum_annuity_pp(199) < 100000.00
    assert p.certain_floor(200) == 1.0
    assert p.certain_floor(201) == 0.0


def test_liability_cf_adds_the_maintenance_expense(anchor):
    """The notes' CF(t) = E[ANN] + E[CR] + E[COMM] + E[EXP] **[std]**.

    $60 p.a. paid monthly, inflating at 2.5% from the second policy year, while any
    payment obligation remains.  This is what the worked-example table's "CF" column
    leaves out.
    """
    assert anchor.expenses(1) == pytest.approx(5.00, abs=CENT)
    assert anchor.expenses(13) == pytest.approx(5.00 * 1.025, abs=CENT)
    assert anchor.expenses(25) == pytest.approx(5.00 * 1.025 ** 2, abs=CENT)
    assert anchor.liability_cf(1) == pytest.approx(505.00, abs=CENT)
    assert anchor.liability_cf(14) == pytest.approx(343.33 + 5.00 * 1.025, abs=CENT)
    assert anchor.net_cf(14) == pytest.approx(-anchor.liability_cf(14), abs=1e-12)


# ---------------------------------------------------------------------------
# Known modeling pitfalls, one test each


def test_pitfall_certain_period_is_not_double_counted(immediate_annuity):
    """"max(C, L) prevents paying 1 + L; an additive construction silently doubles the
    guarantee."  Model point 13 kills both lives inside the certain period.
    """
    p = immediate_annuity.Projection[13]
    assert p.check_payment_factor() is True        # no argument, every projected month
    for t in (14, 30, 60, 120):
        assert p.check_payment_factor_resid(t) == 0.0
        assert p.payment_factor(t) == pytest.approx(1.0, abs=FACTOR)
    assert p.lives_if_last(30) == 0.0                # both annuitants dead
    assert p.payment_factor_life(30) == 0.0
    assert p.payment_factor(30) == 1.0               # not 1 + 0, and not 0
    assert p.annuity_payments(30) == pytest.approx(6000.0 * 1.03 ** 2 / 12, abs=CENT)
    assert p.pols_if(120) == 1.0                     # the obligation is still open
    assert p.annuity_payments(121) == 0.0            # and closes with the certain period
    assert p.pols_if(121) == 0.0
    assert p.expenses(121) == 0.0


def test_pitfall_mort_ae_factor_sits_on_the_projected_basis(immediate_annuity):
    """"1.084 belongs on 2012 IAM Basic *projected with G2*; on the unprojected table the
    study's own answer is 99.6%."  Applying it to the wrong base misstates the mortality
    level by about 8%.
    """
    p = immediate_annuity.Projection[8]
    k = p.calendar_year(1) - p.mort_table_year
    assert k == 2026 - 2012
    base = p.mort_rate_base(1, 1)
    g2 = p.improvement_rate(1, 1)
    assert p.mort_rate(1, 1) == pytest.approx(
        p.mort_ae_factor * base * (1 - g2) ** k, rel=1e-12)
    assert p.mort_rate(1, 1) != pytest.approx(p.mort_ae_factor * base, rel=1e-6)


def test_pitfall_the_basis_is_generational_not_period(immediate_annuity):
    """"The 2012 IAM Period Table is one calendar year's rates ... Using the Period Table
    without projection understates longevity throughout."

    The same attained age reached in a later calendar year must carry a lower rate, and
    the improvement must be taken from the *base* rate each time rather than compounded
    off an already-projected prior-year value.
    """
    p = immediate_annuity.Projection[8]
    # attained age 66 for the primary is reached at t = 13, calendar year 2027.
    assert p.age(13, 1) == 66 and p.calendar_year(13) == 2027
    base66 = p.mort_rate_base(13, 1)
    g66 = p.improvement_rate(13, 1)
    assert p.mort_rate(13, 1) == pytest.approx(
        p.mort_ae_factor * base66 * (1 - g66) ** 15, rel=1e-12)
    assert p.mort_rate(13, 1) < p.mort_ae_factor * base66        # improvement applied
    # A later duration at the same age would be lighter still: the exponent grows with k.
    assert p.mort_rate(25, 1) < p.mort_ae_factor * p.mort_rate_base(25, 1)


def test_pitfall_survival_measurement_timing(immediate_annuity):
    """"Arrears instalments require survival at the payment date, advance instalments at
    the period start ... understates the liability by about one period's mortality per
    payment."

    Model points 6 (arrears) and 10 (advance) are the same single life dying in month
    14; the two conventions differ by exactly one instalment.
    """
    arrears, advance = immediate_annuity.Projection[6], immediate_annuity.Projection[10]
    assert arrears.payment_surv_mth(14) == 14
    assert advance.payment_surv_mth(14) == 13
    assert arrears.annuity_payments(13) == pytest.approx(515.00, abs=CENT)
    assert arrears.annuity_payments(14) == 0.0
    assert advance.annuity_payments(14) == pytest.approx(515.00, abs=CENT)
    assert advance.annuity_payments(15) == 0.0


def test_advance_survival_is_the_period_start_at_every_frequency(immediate_annuity):
    """The same pitfall away from m = 12, where the notes' two statements disagree.

    The notes put an advance instalment "at the start of month 12(k-1)/m + 1" but write
    the survival point as ``t - 12/m``.  The second is measured from the *arrears* month
    of the same instalment, one payment period later; indexed by the month the advance
    instalment falls in, as ``is_payment_mth`` does, the survival point is ``t - 1`` at
    every frequency.  The two readings coincide only at m = 12.

    Model point 14 is quarterly in advance, single male 65, dying in month 3.  The second
    instalment falls at the start of month 4, by which time the life is dead, so the
    contract pays 1,500.00 in year one and nothing after.  Reading ``t - 12/m`` literally
    would measure survival at month 1 and pay it in full -- 3,000.00 in year one, to a
    life the projection has already recorded as dead.
    """
    q = immediate_annuity.Projection[14]
    assert q.payment_freq() == 4 and q.payment_timing() == "advance"
    assert [t for t in range(1, 15) if q.is_payment_mth(t)] == [1, 4, 7, 10, 13]
    for t in (1, 4, 7, 10, 13):
        assert q.payment_surv_mth(t) == t - 1
    assert q.payment_surv_mth(1) == 0            # ... and 0 for the first instalment
    assert q.lives_if(0, 1) == 1.0
    assert q.lives_if(2, 1) == 1.0 and q.lives_if(3, 1) == 0.0
    assert q.annuity_pp(4) == pytest.approx(1500.00, abs=CENT)   # scheduled ...
    assert q.annuity_payments(1) == pytest.approx(1500.00, abs=CENT)
    assert q.annuity_payments(4) == 0.0                          # ... but not payable
    year_one = q.result_cf().loc[1:12, "annuity_payments"].sum()
    assert year_one == pytest.approx(1500.00, abs=CENT)


def test_pitfall_refund_balance_timing(immediate_annuity):
    """"G must net instalments *paid before death* on arrears (G(t-1)), but an advance
    instalment paid at the **start** of the death month has been paid -- use G(t) there
    or the cash refund is overstated by one instalment."
    """
    arrears, advance = immediate_annuity.Projection[6], immediate_annuity.Projection[11]
    assert arrears.claim_pp(14, "REFUND") == pytest.approx(93485.00, abs=CENT)
    assert advance.claim_pp(14, "REFUND") == pytest.approx(92970.00, abs=CENT)
    # Exactly one instalment apart, and the advance figure is the smaller of the two.
    assert arrears.claim_pp(14, "REFUND") - advance.claim_pp(14, "REFUND") == (
        pytest.approx(515.00, abs=CENT))


def test_pitfall_refund_period_moves_with_the_pricing_input(immediate_annuity):
    """"n_R is derived from P/B(1) and moves with the pricing input; hard-coding it
    (e.g. at 200 months) breaks every sensitivity run on B(1)."

    Model point 12 is the same contract at B(1) = 4,800: 100,000/400 = 250 months.
    """
    at6000, at4800 = immediate_annuity.Projection[7], immediate_annuity.Projection[12]
    assert at6000.annual_income(1) == 6000.0 and at6000.certain_mths_refund() == 200
    assert at4800.annual_income(1) == 4800.0 and at4800.certain_mths_refund() == 250
    assert at4800.cum_annuity_pp(250) == pytest.approx(100000.00, abs=CENT)


def test_pitfall_joint_life_independence_is_explicit(immediate_annuity):
    """"The l1*l2 products assume independence **[std]**."

    The identity is asserted rather than assumed so the assumption is visible where it
    is made: ``l_last = l1 + l2 - l1*l2``, and on a single-life contract ``l_last = l1``.
    """
    joint = immediate_annuity.Projection[8]
    for t in (1, 12, 60, 240):
        l1, l2 = joint.lives_if(t, 1), joint.lives_if(t, 2)
        assert joint.lives_if_last(t) == pytest.approx(l1 + l2 - l1 * l2, rel=1e-14)
        assert joint.check_lives_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-14)
    single = immediate_annuity.Projection[7]
    for t in (1, 60, 240):
        assert single.lives_if_last(t) == single.lives_if(t, 1)
        assert single.lives_if(t, 2) == 0.0


def test_pitfall_commutation_touches_only_the_certain_slice(tmp_path):
    """"A withdrawal reduces certain-period instalments only; applying theta_cum to the
    life-contingent tail contradicts every retrieved contract" [S1][S2][S5].

    Utilization is zero in the base run, so this test reads its own model instance and
    turns ``commute_util_base`` up to 10% on model point 9 (life with 10-year certain,
    commutation enabled).
    """
    model = mx.read_model(MODEL_PATH, name="SPIA_US_S_commute")
    try:
        base = model.Projection[9]
        assert base.commute_util_base == 0.0
        assert base.result_cf()["commutations"].sum() == 0.0
        assert base.commute_frac_cum(200) == 0.0

        model.Projection.commute_util_base = 0.10
        model.Projection.clear_all()
        p = model.Projection[9]

        # One withdrawal per contract year, first available in month 13 (year 2) [S1].
        assert p.commute_elig(1) is False and p.commute_elig(13) is True
        assert p.commute_elig(14) is False
        cv = p.commuted_value(13)
        w = p.commute_amount(13)
        assert w == pytest.approx(0.10 * cv, rel=1e-12)
        assert w >= p.commute_min_amount
        assert p.surr_charge_rate(2) == 0.08
        assert p.commutations(13) == pytest.approx(w * 0.92, rel=1e-12)
        assert p.surr_charge(13) == pytest.approx(w * 0.08, rel=1e-12)
        # theta_cum applies from the following month, pro rata [S5].
        assert p.commute_frac_cum(13) == 0.0
        assert p.commute_frac_cum(14) == pytest.approx(0.10, rel=1e-12)
        assert p.annuity_payments(13) == pytest.approx(515.00, abs=CENT)
        assert p.annuity_payments(14) == pytest.approx(515.00 * 0.90, abs=CENT)
        # ... to certain-period instalments only.  After n_eff the factor is switched
        # off by C(t) and the life-contingent tail is paid in full.
        assert p.certain_floor(120) == 1.0 and p.certain_floor(121) == 0.0
        untouched = (p.annuity_pp(121) * p.payment_factor(121))
        assert p.annuity_payments(121) == pytest.approx(untouched, rel=1e-12)
        assert p.annuity_pp_paid(121) == p.annuity_pp(121)
    finally:
        model.close()


def test_pitfall_no_tax_cash_flow(anchor):
    """"Treating exclusion-ratio tax as a cash flow ... generates no insurer flow;
    modeling it as an outgo distorts the liability."  There is no tax line at all."""
    cols = set(anchor.result_cf().columns)
    assert not any("tax" in c for c in cols)
    names = set(anchor.cells)
    assert not any("exclusion" in n or "tax" in n for n in names if n != "premium_tax_rate")


# ---------------------------------------------------------------------------
# Product invariants


def test_there_is_no_lapse_decrement(immediate_annuity):
    """"No lapse decrement" is a cited product property, not an omission [R2][REG-R36].

    The contract has no account value and no surrender right [S1][S4][S5], so VM-22
    declares the prescribed lapse table inapplicable and the annuitization rate 0%.
    """
    names = set(immediate_annuity.Projection.cells) | set(immediate_annuity.Projection.refs)
    for forbidden in ("pols_lapse", "lapse_rate", "surr_value", "cash_value",
                      "av_pp", "pols_new_biz"):
        assert forbidden not in names, forbidden


def test_there_is_no_premium_income_in_the_projection(anchor):
    """"There is no premium income in the projection (the single premium at t = 0 is a
    pricing input) and no surrender outgo" [S1][S4][S5]."""
    assert "premiums" not in anchor.result_cf().columns
    assert anchor.premium_pp() == 100000.0
    assert anchor.premium_net_pp() == 100000.0          # tau = 0 in the base run
    for t in (1, 14, 120):
        assert anchor.liability_cf(t) == pytest.approx(
            anchor.annuity_payments(t) + anchor.claims(t)
            + anchor.commutations(t) + anchor.expenses(t), rel=1e-12)


def test_the_model_is_undiscounted(immediate_annuity):
    """Gross liability cash flows only; discounting is a separate layer.

    The one discounting inside the model is contractual -- the commuted value -- and it
    is named for what it is.
    """
    names = set(immediate_annuity.Projection.cells) | set(immediate_annuity.Projection.refs)
    assert not any(n.startswith("pv_") or n.startswith("disc_") for n in names)
    assert "commute_disc_rate" in names                 # the contractual exception


def test_the_stop_rule_follows_the_younger_life(immediate_annuity):
    """"Stopping on the primary's age alone would truncate a younger joint annuitant's
    tail" -- proj_len runs to the notes' age rule on the *youngest* covered life."""
    joint = immediate_annuity.Projection[8]
    assert joint.age_at_entry(1) == 65 and joint.age_at_entry(2) == 62
    assert joint.omega_age == 120
    assert joint.horizon_mths() == 12 * (120 - 62)
    assert joint.proj_len() == 696
    single = immediate_annuity.Projection[6]
    assert single.proj_len() == 12 * (120 - 65)
    # A certain period longer than the mortality horizon would extend the projection.
    certain = immediate_annuity.Projection[5]
    assert certain.proj_len() == max(certain.horizon_mths(), 120)


def test_the_age_stop_rule_does_not_subsume_the_if_stop_test(immediate_annuity):
    """The notes give two stop tests and the age one does not imply the other.

    "Stop when IF(t) < 1e-6, or when every covered life has passed the limiting age."
    ``age(t, life)`` advances on policy anniversaries, so the age rule's last month is the
    one in which the youngest life is ``omega_age - 1``, not ``omega_age``: the q = 1 row
    is never reached inside the projection and the run ends with IF above 1e-6.  Pinned so
    the docstrings cannot quietly claim subsumption again.
    """
    p = immediate_annuity.Projection[8]
    last = p.proj_len()
    assert last == 696
    assert p.age(last, 2) == 119                      # one short of omega_age
    assert p.age(last + 1, 2) == 120                  # where q = 1 would bite
    assert p.mort_rate_base(last + 1, 2) == 1.0
    assert p.pols_if(last) == pytest.approx(3.4078e-06, rel=1e-3)
    assert p.pols_if(last) > 1e-6                     # the notes' other test is not met


def test_inforce_roll_forward_closes(immediate_annuity):
    """lives_if agrees with an independently rebuilt survival path at every month.

    ``check_lives_roll_fwd_resid`` rebuilds the survival path from the monthly rates
    rather than telescoping ``lives_death``, which is *defined* as ``l(t-1) - l(t)`` and
    would close for any ``lives_if`` whatever; the same product is rebuilt here in the
    test so the model is not marking its own homework, and
    :func:`test_the_roll_forward_check_is_not_vacuous` proves the residual can move.

    ``check_lives_roll_fwd()`` is the library-wide form of the same check -- no argument,
    a bool over every projected month -- and is asserted first.
    """
    p = immediate_annuity.Projection[8]
    assert p.check_lives_roll_fwd() is True
    for t in range(1, 121):
        assert p.check_lives_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-13)
    for life in (1, 2):
        built = 1.0
        for t in range(1, 121):
            built *= 1.0 - p.mort_rate_mth(t, life)
            assert p.lives_if(t, life) == pytest.approx(built, rel=1e-12)
    # Deaths and survivors still account for the whole cohort.
    for t in (1, 12, 60, 120):
        cum = sum(p.lives_death(s, 1) for s in range(1, t + 1))
        assert cum + p.lives_if(t, 1) == pytest.approx(1.0, abs=1e-12)


def test_the_roll_forward_check_is_not_vacuous():
    """Break the survival recursion and the roll-forward residual must notice.

    ``lives_if`` is replaced with a misindexed recursion -- ``q_m(t-1)`` where the notes
    write ``q_m(t)`` -- in a throwaway model instance.  The telescoping form of this
    check would still return exactly 0.0, because ``lives_death`` is defined as the
    difference it takes; the reconstruction form does not.
    """
    broken = (
        "def lives_if(t, life):\n"
        "    if life == 2 and not is_joint():\n"
        "        return 0.0\n"
        "    if t <= 0:\n"
        "        return 1.0\n"
        "    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t - 1, life))\n"
    )
    model = mx.read_model(MODEL_PATH, name="SPIA_US_S_rollfwd")
    try:
        assert model.Projection[8].check_lives_roll_fwd_resid(60) == pytest.approx(
            0.0, abs=1e-13)
        model.Projection.lives_if.formula = broken
        model.Projection.clear_all()
        p = model.Projection[8]
        # the telescoping identity the check used to be, still zero on the broken model
        telescoped = sum(p.lives_if(59, i) - p.lives_death(60, i) - p.lives_if(60, i)
                         for i in (1, 2))
        assert telescoped == 0.0
        assert abs(p.check_lives_roll_fwd_resid(60)) > 1e-6
        # ... and the no-arg bool, which the whole library calls, goes False with it.
        assert p.check_lives_roll_fwd() is False
    finally:
        model.close()


def test_certain_only_expense_stops_with_the_last_payment(immediate_annuity):
    """The maintenance expense runs "while any payment obligation remains".

    On ``certain_only`` the notes set L(t) = 0, so the contract's last instalment falls
    at n_eff and nothing is owed afterwards -- but their IF(t) = max(C, l_alive) formula
    is written with the life-contingent forms in mind and ``l_alive`` stays positive for
    the annuitant's remaining lifetime.  Read literally it accrues 1,539.83 of expense
    over the 540 months after the contract ended.  ``pols_if`` follows the prose.
    """
    p = immediate_annuity.Projection[15]
    assert p.form() == "certain_only" and p.certain_mths_eff() == 120
    assert p.payment_factor_life(60) == 0.0            # no life contingency at all
    assert p.lives_if_last(240) == pytest.approx(0.7046, abs=5e-5)   # still alive ...
    assert p.pols_if(120) == 1.0
    assert p.pols_if(121) == 0.0                       # ... but nothing is owed
    assert p.expenses(120) > 0.0
    assert p.expenses(121) == 0.0
    assert p.expenses(240) == 0.0
    df = p.result_cf()
    assert df.loc[121:, "annuity_payments"].sum() == 0.0
    assert df.loc[121:, "expenses"].sum() == 0.0
    assert df.loc[121:, "liability_cf"].sum() == 0.0


def test_survival_is_a_decreasing_probability(immediate_annuity):
    p = immediate_annuity.Projection[8]
    for t in range(1, p.proj_len() + 1):
        for life in (1, 2):
            assert 0.0 <= p.lives_if(t, life) <= 1.0
            assert p.lives_if(t, life) <= p.lives_if(t - 1, life) + 1e-15
        assert 0.0 <= p.payment_factor(t) <= 1.0


def test_payment_months_follow_the_frequency(anchor):
    """m = 12 in arrears: every month is a payment month, and T is the whole grid."""
    assert anchor.payment_freq() == 12
    assert anchor.payment_timing() == "arrears"
    assert all(anchor.is_payment_mth(t) for t in range(1, 25))
    assert anchor.is_payment_mth(0) is False


def test_invalid_enum_values_raise(anchor):
    """Every string switch validates, as CashValue_SE does with its timing arguments."""
    with pytest.raises(Exception):
        anchor.claim_pp(1, "DEATH")
    with pytest.raises(Exception):
        anchor.age_at_entry(3)
    with pytest.raises(Exception):
        anchor.sex(0)


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(1, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert set(df.columns) == {
        "pols_if", "annuity_payments", "claims", "commutations", "expenses",
        "liability_cf", "net_cf",
    }
    assert df.loc[1, "annuity_payments"] == pytest.approx(500.00, abs=CENT)
    assert df.loc[14, "annuity_payments"] == pytest.approx(343.33, abs=CENT)
    assert df.loc[1, "net_cf"] == pytest.approx(-505.00, abs=CENT)


def test_result_pols_shape(anchor):
    df = anchor.result_pols()
    assert list(df.index) == list(range(1, anchor.proj_len() + 1))
    assert set(df.columns) == {
        "lives_if_1", "lives_if_2", "lives_if_last", "lives_death_last",
        "certain_floor", "payment_factor_life", "payment_factor", "pols_if",
    }


def test_cells_names_follow_the_shared_set(immediate_annuity):
    """Names shared with basiclife/BasicTerm_S and savings/CashValue_SE must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "age", "duration", "duration_mth",
        "policy_year", "proj_len", "pols_if", "pols_if_init", "mort_rate",
        "mort_rate_mth", "claims", "claim_pp", "expenses", "expense_maint",
        "inflation_rate", "inflation_factor", "surr_charge", "surr_charge_rate",
        "net_cf", "result_cf",
    }
    names = (set(immediate_annuity.Projection.cells)
             | set(immediate_annuity.Projection.refs))
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_cross_model_convention_names_are_used(immediate_annuity, anchor):
    """Names settled library-wide, not this product's own shorthand.

    The mortality A/E deviation factor is ``mort_ae_factor`` and the limiting age is
    ``omega_age`` in every model in ``products/``; a ``check_*`` cells takes **no
    argument and returns a bool** over every projected month, with the signed per-month
    residual kept under ``<same>_resid(t)``.  Pinned here because a rename that only
    half-lands is exactly what the cross-model review found.
    """
    names = (set(immediate_annuity.Projection.cells)
             | set(immediate_annuity.Projection.refs))
    for expected in ("mort_ae_factor", "omega_age",
                     "check_lives_roll_fwd", "check_lives_roll_fwd_resid",
                     "check_payment_factor", "check_payment_factor_resid"):
        assert expected in names, expected
    for old in ("ae_factor", "omega"):
        assert old not in names, old
    assert anchor.check_lives_roll_fwd() is True
    assert anchor.check_payment_factor() is True
    assert isinstance(anchor.check_lives_roll_fwd_resid(12), float)
    assert isinstance(anchor.check_payment_factor_resid(12), float)


def test_every_model_point_projects(immediate_annuity):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in immediate_annuity.Data.model_point_table().index:
        df = immediate_annuity.Projection[point_id].result_cf()
        assert len(df) > 0
        assert df["liability_cf"].min() >= 0.0        # gross outgo, never negative
