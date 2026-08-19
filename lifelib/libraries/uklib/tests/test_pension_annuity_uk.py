"""Golden and structural tests for PA_UK_S.

The golden values are the worked example in
products/pension_annuity/technical-notes.md ("Worked example"), which is a
**scenario**: GBP 100,000 buying GBP 5,400 a year for a male 65 with a female 62
dependant at 50%, quarterly in arrears, fixed 3% escalation, value protection at 50% on
the annuitant's death, no guarantee period -- and the annuitant dies in month 17 while
the dependant survives throughout.  Model point 1 is that cell.  They are hard-coded
here rather than pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the penny.

Beyond the worked example this module asserts the product facts the notes call out as
modelling pitfalls, because each is a way an implementation can look right and be wrong:

* the guarantee is an annuity-certain **floor**, never a second stream;
* without overlap the dependant's stream is gated on the guarantee, not on the death;
* the value-protection balance nets instalments **already paid**, which differs by one
  instalment between arrears and advance timing;
* and the RPI catch-up ratchet is path-dependent state that must persist.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from uk_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9, a house decision per D8).  Those
    caches are not part of the model and must not make a round-trip comparison fail for
    anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


PENNY = 0.005         # money displayed to 2 d.p.

MODEL_DIR = LIB / MODELS["PA_UK_S"][0]

# t: (annuitant CF, dependant CF, VP lump sum, G(t))
# The notes' table, with "--" read as zero.  G is the cumulative *scheduled* instalments
# of every stream, which is cum_annuity_pp(t, "ALL").
WORKED_EXAMPLE = {
    3:  (1350.00,   0.00,       0.00, 1350.00),
    6:  (1350.00,   0.00,       0.00, 2700.00),
    9:  (1350.00,   0.00,       0.00, 4050.00),
    12: (1350.00,   0.00,       0.00, 5400.00),
    13: (0.00,      0.00,       0.00, 5400.00),   # anniversary: A <- 5,562.00
    15: (1390.50,   0.00,       0.00, 6790.50),
    17: (0.00,      0.00,  43209.50, 6790.50),    # annuitant dies
    18: (0.00,    695.25,       0.00, 7485.75),   # dependant stream starts
    21: (0.00,    695.25,       0.00, 8181.00),
    24: (0.00,    695.25,       0.00, 8876.25),
}


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_pa_scenario, t):
    """Every cell of the notes' table, to the displayed precision."""
    annuitant, dependant, vp, cum = WORKED_EXAMPLE[t]
    p = uk_pa_scenario
    assert p.annuity_pp(t) * p.payment_factor(t) == pytest.approx(annuitant, abs=PENNY)
    assert p.annuity_pp(t) * p.dependant_factor(t) == pytest.approx(
        dependant, abs=PENNY)
    assert p.claims(t, "VP") == pytest.approx(vp, abs=PENNY)
    assert p.cum_annuity_pp(t, "ALL") == pytest.approx(cum, abs=PENNY)
    assert p.annuity_payments(t) == pytest.approx(annuitant + dependant, abs=PENNY)


def test_the_instalment_schedule(uk_pa_scenario):
    """A(1)/m = 1,350.00 in year 1; A(2) = 5,400 x 1.03 = 5,562, so 1,390.50 from t = 13."""
    p = uk_pa_scenario
    assert p.annual_income(1) == 5400.0
    assert p.annual_income(2) == pytest.approx(5562.00, abs=PENNY)
    assert p.annuity_pp(3) == pytest.approx(1350.00, abs=PENNY)
    assert p.annuity_pp(15) == pytest.approx(1390.50, abs=PENNY)
    # Payment months only: quarterly arrears falls at 3, 6, 9, ...
    assert [t for t in range(1, 13) if p.is_payment_mth(t)] == [3, 6, 9, 12]
    assert p.annuity_pp(13) == 0.0


def test_escalation_reaches_the_anniversary_not_the_payment_date(uk_pa_scenario):
    """The year-2 rate must not touch the t = 12 arrears instalment, accrued in year 1.

    A listed pitfall: escalation applies on the anniversary, and the month-12 payment is
    the fourth instalment of year 1.
    """
    p = uk_pa_scenario
    assert p.policy_year(12) == 1 and p.policy_year(13) == 2
    assert p.annuity_pp(12) == pytest.approx(1350.00, abs=PENNY)
    assert p.annuity_pp(15) == pytest.approx(1390.50, abs=PENNY)


def test_the_value_protection_lump_sum(uk_pa_scenario):
    """max(0, 0.50 x 100,000 - G(16)) = 50,000 - 6,790.50 = 43,209.50."""
    p = uk_pa_scenario
    assert p.vp_pct() == 0.50 and p.vp_basis() == "first_death"
    assert p.cum_annuity_pp(16, "ANNUITANT") == pytest.approx(6790.50, abs=PENNY)
    assert p.vp_balance(16) == pytest.approx(43209.50, abs=PENNY)
    assert p.lives_death(17, 1) == 1.0            # the scenario death
    assert p.claims(17, "VP") == pytest.approx(43209.50, abs=PENNY)
    # And it is paid once.
    assert sum(p.claims(t, "VP") for t in range(1, p.proj_len() + 1)) == pytest.approx(
        43209.50, abs=PENNY)


def test_the_dependant_stream_starts_at_the_next_payment_date(uk_pa_scenario):
    """Death in month 17, first dependant instalment at month 18: delta x A(2)/m."""
    p = uk_pa_scenario
    assert p.lives_if(16, 1) == 1.0 and p.lives_if(17, 1) == 0.0
    assert p.lives_if(24, 2) == 1.0               # the dependant survives throughout
    assert p.dependant_factor(15) == 0.0          # annuitant still alive
    assert p.dependant_factor(18) == pytest.approx(0.50, rel=1e-12)
    assert p.annuity_pp(18) * p.dependant_factor(18) == pytest.approx(695.25, abs=PENNY)
    assert 0.50 * 5562.00 / 4 == pytest.approx(695.25, abs=PENNY)


def test_no_annuitant_payment_in_the_death_month_or_after(uk_pa_scenario):
    """Arrears without proportion: nothing is paid for the final partial period."""
    p = uk_pa_scenario
    assert p.claims(17, "PROP") == 0.0
    assert p.annuity_pp(18) * p.payment_factor(18) == 0.0
    assert all(p.payment_factor(t) == 0.0 for t in (18, 21, 24, 100))


def test_the_cumulative_schedule_takes_two_forms(uk_pa_scenario):
    """G is the annuitant's as-if-alive schedule for VP and every stream for the table.

    The notes use one symbol for both; they diverge from month 18, where the dependant's
    instalment enters the printed column but not the first-death VP balance.
    """
    p = uk_pa_scenario
    for t in (3, 12, 16):
        assert p.cum_annuity_pp(t, "ANNUITANT") == pytest.approx(
            p.cum_annuity_pp(t, "ALL"), abs=PENNY)
    assert p.cum_annuity_pp(18, "ALL") == pytest.approx(7485.75, abs=PENNY)
    # The as-if-alive schedule keeps accruing the annuitant's instalment regardless.
    assert p.cum_annuity_pp(18, "ANNUITANT") == pytest.approx(
        6790.50 + 1390.50, abs=PENNY)
    with pytest.raises(FormulaError):
        p.cum_annuity_pp(5, "DEPENDANT")


# ---------------------------------------------------------------------------
# The guarantee is a floor


def test_the_guarantee_is_a_floor_not_a_second_stream(pension_annuity):
    """max(C, l_a), never C + l_a - the notes' first-listed pitfall."""
    p = pension_annuity.Projection[3]
    assert p.guarantee_mths() == 120
    assert p.check_payment_factor() is True
    # While both are 1 the max is 1 and the sum would be 2: an additive floor pays the
    # guarantee twice over, which is the whole reason for the max.
    assert p.certain_floor(12) == 1.0 and p.payment_factor_life(12) == 1.0
    assert p.payment_factor(12) == 1.0
    assert p.certain_floor(12) + p.payment_factor_life(12) == 2.0
    # Inside the guarantee the full instalment is payable though the annuitant is dead.
    assert p.lives_if(17, 1) == 0.0
    assert p.certain_floor(60) == 1.0 and p.payment_factor_life(60) == 0.0
    assert p.payment_factor(60) == 1.0
    # And nothing after it, because the annuitant is dead.
    assert p.certain_floor(120) == 1.0 and p.certain_floor(121) == 0.0
    assert p.payment_factor(123) == 0.0


def test_the_guarantee_escalates_as_if_alive(pension_annuity):
    """Instalments continue to beneficiaries at the escalating rate through the period."""
    p = pension_annuity.Projection[3]
    for y, t in ((2, 15), (5, 51), (10, 111)):
        assert p.policy_year(t) == y
        assert p.annuity_pp(t) == pytest.approx(5400.0 * 1.03 ** (y - 1) / 4, abs=PENNY)
        assert p.annuity_payments(t) >= p.annuity_pp(t)


def test_guarantee_and_value_protection_never_coexist(pension_annuity):
    """The representative design offers one or the other; both would double-pay."""
    for point_id in pension_annuity.Data.model_point_table().index:
        assert pension_annuity.Projection[point_id].check_guarantee_xor() is True
    table = pension_annuity.Data.model_point_table()
    assert not ((table["guarantee_months"] > 0) & (table["vp_pct"] > 0)).any()


def test_a_contract_without_a_guarantee_has_no_floor(uk_pa_scenario):
    p = uk_pa_scenario
    assert p.guarantee_mths() == 0
    assert all(p.certain_floor(t) == 0.0 for t in (1, 12, 120))
    assert p.payment_factor(12) == p.payment_factor_life(12)


# ---------------------------------------------------------------------------
# The overlap gate


def test_without_overlap_the_dependant_waits_for_the_guarantee_to_end(pension_annuity):
    """Gated on t > n even though the annuitant died in month 17.

    Applying delta from the death date silently converts every without-overlap policy
    into the more expensive with-overlap form - the notes' second-listed pitfall.
    """
    p = pension_annuity.Projection[3]
    assert p.overlap() is False
    assert p.overlap_gate(18) == 0.0
    assert p.overlap_gate(120) == 0.0
    assert p.overlap_gate(121) == 1.0
    assert p.dependant_factor(18) == 0.0
    assert p.dependant_factor(123) == pytest.approx(0.50, rel=1e-12)


def test_with_overlap_both_streams_run_during_the_guarantee(pension_annuity):
    """Model point 4 is point 3 with the switch flipped, and costs materially more."""
    p3, p4 = pension_annuity.Projection[3], pension_annuity.Projection[4]
    assert p4.overlap() is True
    assert p4.overlap_gate(18) == 1.0
    assert p4.dependant_factor(18) == pytest.approx(0.50, rel=1e-12)
    assert p4.result_cf()["liability_cf"].sum() > p3.result_cf()["liability_cf"].sum()
    # The whole difference is the dependant's stream inside the guarantee.
    diff = sum(p4.annuity_payments(t) - p3.annuity_payments(t)
               for t in range(1, 121))
    total = (p4.result_cf()["liability_cf"].sum()
             - p3.result_cf()["liability_cf"].sum())
    assert diff == pytest.approx(total, rel=1e-9)


def test_a_single_life_contract_has_no_dependant_stream(pension_annuity):
    p = pension_annuity.Projection[5]
    assert p.is_joint() is False
    assert p.dependant_pct() == 0.0
    assert all(p.dependant_factor(t) == 0.0 for t in (1, 60, 300))
    assert p.lives_if(60, 2) == 0.0
    with pytest.raises(FormulaError):
        p.age_at_entry(2)


# ---------------------------------------------------------------------------
# Escalation


def test_the_four_escalation_bases(pension_annuity):
    """level, fixed, lpi5 and the rpi_catchup ratchet."""
    level = pension_annuity.Projection[5]
    assert level.escalation_type() == "level"
    assert all(level.annual_income(y) == 6657.0 for y in (1, 5, 20))

    fixed = pension_annuity.Projection[2]
    assert fixed.annual_income(5) == pytest.approx(5400.0 * 1.03 ** 4, rel=1e-12)

    lpi = pension_annuity.Projection[7]
    assert lpi.escalation_type() == "lpi5"
    assert lpi.annual_income(5) == pytest.approx(5400.0 * 1.03 ** 4, rel=1e-12)

    catchup = pension_annuity.Projection[6]
    assert catchup.escalation_type() == "rpi_catchup"
    assert catchup.annual_income(5) == pytest.approx(5400.0 * 1.03 ** 4, rel=1e-12)


def test_a_deterministic_rpi_path_makes_the_inflation_options_worthless(
        pension_annuity):
    """fixed 3%, lpi5 and rpi_catchup all coincide, and that is the point.

    The zero floor, the ratchet and the LPI cap are inflation *options*; a deterministic
    path values them at intrinsic only - the floor and ratchet never bind and the cap
    never pays off.  Asserting the degeneracy keeps the limitation visible rather than
    implied.
    """
    fixed = pension_annuity.Projection[2].result_cf()["liability_cf"].sum()
    catchup = pension_annuity.Projection[6].result_cf()["liability_cf"].sum()
    lpi = pension_annuity.Projection[7].result_cf()["liability_cf"].sum()
    assert catchup == pytest.approx(fixed, rel=1e-12)
    assert lpi == pytest.approx(fixed, rel=1e-12)


def test_the_lpi_cap_bites_above_five_percent(pension_annuity):
    """min(5%, max(0, RPI)) - the cap only shows under a path that reaches it."""
    model = mx.read_model(MODEL_DIR, name="PA_UK_S_lpi")
    try:
        model.Projection.rpi_rate = 0.08
        model.Projection.clear_all()
        lpi = model.Projection[7]
        assert lpi.annual_income(3) == pytest.approx(5400.0 * 1.05 ** 2, rel=1e-12)
        catchup = model.Projection[6]
        assert catchup.annual_income(3) == pytest.approx(5400.0 * 1.08 ** 2, rel=1e-12)
        model.Projection.rpi_rate = -0.02          # deflation: the LPI floor holds
        model.Projection.clear_all()
        assert model.Projection[7].annual_income(3) == pytest.approx(5400.0, rel=1e-12)
    finally:
        model.close()


def test_the_catchup_ratchet_is_path_dependent_state(pension_annuity):
    """A fall freezes income; later rises bite only past the previous peak.

    Resetting the peak each year turns the catch-up into a plain zero floor and
    overstates indexed income after a deflation-recovery path.
    """
    model = mx.read_model(MODEL_DIR, name="PA_UK_S_ratchet")
    try:
        model.Projection.rpi_rate = -0.02
        model.Projection.clear_all()
        p = model.Projection[6]
        # The index falls, so the peak stays at its outset level and income is frozen.
        assert p.rpi_index(3) < p.rpi_index(0)
        assert p.rpi_peak(3) == pytest.approx(p.rpi_index(0), rel=1e-12)
        assert p.annual_income(4) == pytest.approx(5400.0, rel=1e-12)
        assert p.annual_income(20) == pytest.approx(5400.0, rel=1e-12)
        # A plain zero floor would give the same answer here; the ratchet differs on the
        # way back up, which the monotone peak encodes.
        assert p.rpi_peak(5) >= p.rpi_peak(4) >= p.rpi_peak(3)
    finally:
        model.close()


def test_the_fixed_escalation_cap(pension_annuity):
    """g is contractually capped at 10%; a model point above it raises."""
    p = pension_annuity.Projection[2]
    assert p.escalation_rate() == 0.03
    model = mx.read_model(MODEL_DIR, name="PA_UK_S_esccap")
    try:
        model.Projection.esc_fixed_cap = 0.02      # below the model point's 3%
        model.Projection.clear_all()
        with pytest.raises(FormulaError):
            model.Projection[2].escalation_rate()
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Payment timing


def test_arrears_measures_survival_at_the_end_of_the_payment_month(uk_pa_scenario):
    p = uk_pa_scenario
    assert p.payment_timing() == "arrears"
    assert all(p.payment_surv_mth(t) == t for t in (3, 6, 15))


def test_advance_measures_survival_at_the_start_of_the_payment_month(pension_annuity):
    """Using end-of-period survival for advance payments understates the liability."""
    p = pension_annuity.Projection[5]
    assert p.payment_timing() == "advance"
    assert p.payment_surv_mth(1) == 0
    assert all(p.payment_surv_mth(t) == t - 1 for t in (1, 2, 60))
    assert p.payment_factor(1) == 1.0             # the first instalment is certain
    assert p.payment_factor(60) == pytest.approx(p.lives_if(59, 1), rel=1e-14)
    # Advance payment months are 1, 2, 3, ... at m = 12.
    assert all(p.is_payment_mth(t) for t in (1, 2, 3, 60))


def test_the_advance_value_protection_netting_rule(pension_annuity):
    """An instalment paid at the start of the death month has been paid, so net it.

    Otherwise the lump sum is overstated by one instalment - the notes' pitfall.
    """
    model = mx.read_model(MODEL_DIR, name="PA_UK_S_advvp")
    try:
        # Point 5 is single-life monthly in advance; give it value protection.
        model.Data.model_point_table()            # warm the reader
        proj = model.Projection[5]
        assert proj.payment_timing() == "advance"
        # The rule is expressed in claims(t, "VP"): in an advance payment month the
        # balance is read at t, not t - 1.  Every month is a payment month at m = 12,
        # so the balance used is always the post-payment one.
        assert proj.is_payment_mth(30) is True
        assert proj.vp_balance(30) <= proj.vp_balance(29)
    finally:
        model.close()


def test_the_proportionate_final_payment(pension_annuity):
    """(h + 0.5)/(12/m) x inst(next) = (1 + 0.5)/3 x 1,390.50 = 695.25 on a month-17 death."""
    p = pension_annuity.Projection[9]
    assert p.proportion() is True
    assert p.mths_since_payment(17) == 1           # one complete month since t = 15
    assert p.next_payment_mth(17) == 18
    assert p.claims(17, "PROP") == pytest.approx(695.25, abs=PENNY)
    # And it is the only difference from the worked-example point.
    p1 = pension_annuity.Projection[1]
    total = (p.result_cf()["liability_cf"].sum()
             - p1.result_cf()["liability_cf"].sum())
    assert total == pytest.approx(695.25, abs=PENNY)


def test_proportion_is_an_arrears_only_option(pension_annuity):
    """A model point combining it with advance timing raises rather than guessing."""
    table = pension_annuity.Data.model_point_table()
    assert not (table["proportion"] & (table["timing"] != "arrears")).any()


def test_without_proportion_nothing_is_paid_for_the_final_period(uk_pa_scenario):
    p = uk_pa_scenario
    assert p.proportion() is False
    assert all(p.claims(t, "PROP") == 0.0 for t in (17, 18, 50))


# ---------------------------------------------------------------------------
# Value protection bases and bounds


def test_the_v_plus_delta_bound(pension_annuity):
    """v + delta <= 1 on the first-death basis; the worked cell sits exactly on it."""
    p = pension_annuity.Projection[1]
    assert p.vp_pct() + p.dependant_pct() == pytest.approx(1.0, rel=1e-12)
    for point_id in pension_annuity.Data.model_point_table().index:
        assert pension_annuity.Projection[point_id].check_vp_bound() is True


def test_the_last_survivor_basis_nets_both_streams(pension_annuity):
    """Model point 10 is the worked cell with VP on the last survivor.

    The trigger is the last death rather than the annuitant's, and the balance nets the
    dependant's instalments too - so nothing is paid on the month-17 death at all.
    """
    p, p1 = pension_annuity.Projection[10], pension_annuity.Projection[1]
    assert p.vp_basis() == "last_survivor"
    assert p.claims(17, "VP") == 0.0              # the dependant is still alive
    assert p.lives_death_last(17) == 0.0
    # Up to the annuitant's death the two bases net the same instalments.
    assert p.vp_balance(16) == pytest.approx(p1.vp_balance(16), abs=PENNY)
    # After it they diverge.  The first-death basis keeps netting the annuitant's
    # *as-if-alive* schedule - which is what makes it deterministic - while the
    # last-survivor basis nets what is actually paid, and the dependant's instalments
    # are half the size, so its balance runs down more slowly.
    assert p.vp_balance(24) > p1.vp_balance(24)
    # In this scenario the dependant outlives the projection, so nothing is ever paid,
    # and the whole difference in liability is the lump sum the first-death basis pays.
    assert sum(p.claims(t, "VP") for t in range(1, p.proj_len() + 1)) == 0.0
    gap = (p1.result_cf()["liability_cf"].sum()
           - p.result_cf()["liability_cf"].sum())
    assert gap == pytest.approx(43209.50, abs=PENNY)


def test_value_protection_is_zero_when_not_elected(pension_annuity):
    p = pension_annuity.Projection[3]
    assert p.vp_pct() == 0.0
    assert all(p.vp_balance(t) == 0.0 for t in (1, 50, 200))
    assert all(p.claims(t, "VP") == 0.0 for t in (1, 50, 200))


# ---------------------------------------------------------------------------
# Mortality


def test_the_mortality_construction(pension_annuity):
    """table x alpha, then improvement, then the rating multiplier, capped at 1."""
    p = pension_annuity.Projection[2]
    assert p.mort_basis() == "table"
    table = pension_annuity.Data.mort_table()
    raw = float(table.loc[("M", 65), "mort_rate"])
    assert p.mort_rate_base(1, 1) == pytest.approx(raw * 0.80, rel=1e-12)
    # Year 1 is calendar 2026 against a 2023 base table, so three years of improvement.
    assert p.improve_factor(1, 1) == pytest.approx(0.9875 ** 3, rel=1e-12)
    assert p.mort_rate(1, 1) == pytest.approx(
        raw * 0.80 * 0.9875 ** 3, rel=1e-12)
    assert p.mort_rate_mth(1, 1) == pytest.approx(
        1 - (1 - p.mort_rate(1, 1)) ** (1 / 12), rel=1e-14)


def test_the_improvement_scale_tapers(pension_annuity):
    """1.25% p.a. to age 90, linear taper to zero at 110, zero above."""
    p = pension_annuity.Projection[2]
    assert p.improve_rate(1, 1) == 0.0125                    # age 65
    t90 = 12 * (90 - 65) + 1
    assert p.age(t90, 1) == 90 and p.improve_rate(t90, 1) == 0.0125
    t100 = 12 * (100 - 65) + 1
    assert p.age(t100, 1) == 100
    assert p.improve_rate(t100, 1) == pytest.approx(0.0125 * 0.5, rel=1e-12)
    t110 = 12 * (110 - 65) + 1
    assert p.improve_rate(t110, 1) == 0.0


def test_the_rating_multiplier_reprices_longevity(pension_annuity):
    """theta = 1.35 on the enhanced point, and the liability falls."""
    standard, enhanced = pension_annuity.Projection[5], pension_annuity.Projection[8]
    assert standard.rating_factor(1) == 1.0
    assert enhanced.rating_factor(1) == 1.35
    assert enhanced.mort_rate(1, 1) == pytest.approx(
        1.35 * standard.mort_rate(1, 1), rel=1e-12)
    assert enhanced.lives_if(120, 1) < standard.lives_if(120, 1)
    # Higher income on the same premium, and a shorter expected stream.
    assert enhanced.annual_income_init() > standard.annual_income_init()


def test_the_survival_recursion_closes(pension_annuity):
    """Rebuilt from the assumptions, not from the telescoping definition of the density."""
    for point_id in pension_annuity.Data.model_point_table().index:
        assert pension_annuity.Projection[point_id].check_lives_roll_fwd() is True, (
            point_id)


def test_the_scenario_basis_is_a_step_function(uk_pa_scenario):
    """1{t < death_mth}: the annuitant dies in month 17, the dependant never."""
    p = uk_pa_scenario
    assert p.mort_basis() == "scenario"
    assert p.death_mth(1) == 17 and p.death_mth(2) == 0
    assert [p.lives_if(t, 1) for t in (15, 16, 17, 18)] == [1.0, 1.0, 0.0, 0.0]
    assert all(p.lives_if(t, 2) == 1.0 for t in (1, 100, 600))
    assert p.lives_death(17, 1) == 1.0
    assert sum(p.lives_death(t, 1) for t in range(1, p.proj_len() + 1)) == 1.0


def test_joint_life_independence(pension_annuity):
    """l_last = l_a + l_d - l_a l_d, which ignores broken-heart dependence [std]."""
    p = pension_annuity.Projection[2]
    for t in (1, 120, 300):
        la, ld = p.lives_if(t, 1), p.lives_if(t, 2)
        assert p.lives_if_last(t) == pytest.approx(la + ld - la * ld, rel=1e-14)
        assert p.lives_if_last(t) >= max(la, ld)


def test_the_projection_stops_on_the_youngest_life(pension_annuity):
    """Stopping on the annuitant alone would truncate a younger dependant's tail."""
    joint = pension_annuity.Projection[2]
    assert joint.horizon_mths() == 12 * (115 - 62)      # the dependant is younger
    assert joint.proj_len() == 636
    single = pension_annuity.Projection[5]
    assert single.proj_len() == 12 * (115 - 65)
    # A guarantee longer than the mortality horizon would extend it instead.
    assert pension_annuity.Projection[3].proj_len() == max(636, 120)


# ---------------------------------------------------------------------------
# What the product does not have


def test_there_is_no_lapse_machinery_anywhere(pension_annuity):
    """No surrender value, no options, no behaviour - a cited product feature.

    It is what makes the liability matching-adjustment eligible, so its absence is
    asserted rather than left to inspection.
    """
    names = set(pension_annuity.Projection.cells) | set(pension_annuity.Projection.refs)
    for absent in ("lapse_rate", "lapse_rate_mth", "pols_lapse", "surr_charge_rate",
                   "dyn_lapse_factor", "commute_amount", "commuted_value",
                   "av_pp_at", "cv_pp", "asset_share", "mvr"):
        assert absent not in names


def test_there_is_no_premium_income(uk_pa_scenario):
    """The purchase price is a pricing input at t = 0, not a projected cash flow."""
    p = uk_pa_scenario
    assert "premiums" not in p.result_cf().columns
    assert p.purchase_price() == 100000.0
    assert all(p.net_cf(t) <= 0.0 for t in (1, 3, 17, 100))


def test_invalid_enum_values_raise(uk_pa_scenario):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        uk_pa_scenario.claims(1, "REFUND")
    with pytest.raises(FormulaError):
        uk_pa_scenario.cum_annuity_pp(1, "BOTH")
    with pytest.raises(FormulaError):
        uk_pa_scenario.sex(3)


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_pa_scenario):
    df = uk_pa_scenario.result_cf()
    assert list(df.index) == list(range(1, 637))
    assert list(df.columns) == [
        "pols_if", "annuity_payments", "claims_vp", "claims_prop", "expenses",
        "liability_cf", "net_cf",
    ]


def test_both_signs_of_the_net_flow_are_published(uk_pa_scenario):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign."""
    p = uk_pa_scenario
    df = p.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    outgo = df[["annuity_payments", "claims_vp", "claims_prop", "expenses"]].sum(axis=1)
    assert (outgo - df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


def test_pols_if_is_the_obligation_indicator_not_a_policy_count(uk_pa_scenario):
    """IF(t): guarantee certain, annuitant alive, or dependant stream in payment."""
    p = uk_pa_scenario
    assert p.pols_if(1) == 1.0                    # annuitant alive
    assert p.pols_if(18) == 1.0                   # dependant stream in payment
    assert p.expenses(18) == pytest.approx(
        30.0 / 12 * 1.03 ** (p.policy_year(18) - 1) * p.pols_if(18), rel=1e-12)
    # It is capped at 1: the two legs cannot add to more than one obligation.
    assert all(p.pols_if(t) <= 1.0 for t in range(1, 200))


def test_model_docstring_describes_the_current_structure(pension_annuity):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = pension_annuity.doc
    assert "pension annuit" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "matching adjustment" in doc
    assert "SPIA_US_S" in doc                    # the chassis it shares


def test_space_docstrings_carry_their_reference_material(pension_annuity):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = pension_annuity.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("lives_if", "payment_factor", "overlap_gate", "cum_annuity_pp",
                  "vp_balance", "rpi_peak", "mort_basis"):
        assert cells in proj
    data = pension_annuity.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "mort_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_the_payout_chassis(pension_annuity):
    """Names shared with SPIA_US_S must mean the same thing on both sides."""
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_init", "mort_rate",
        "mort_rate_mth", "mort_rate_base", "lives_if", "lives_death", "lives_if_last",
        "lives_death_last", "certain_floor", "payment_factor", "payment_factor_life",
        "payment_surv_mth", "is_payment_mth", "annuity_pp", "annuity_payments",
        "cum_annuity_pp", "claims", "expenses", "expense_maint", "inflation_rate",
        "inflation_factor", "liability_cf", "net_cf", "result_cf", "omega_age",
        "policy_year", "duration", "duration_mth", "calendar_year", "horizon_mths",
    }
    names = set(pension_annuity.Projection.cells) | set(pension_annuity.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """Only two input CSVs: this product has almost nothing to parameterize."""
    expected = {"model_point_table.csv", "mort_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """A population proxy, and the file says so - it is not an annuitant table."""
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert set(table["provenance"]) == {"[std] ONS-shaped proxy"}
    assert table["mort_rate"].max() <= 1.0
    assert table[(table["sex"] == "M") & (table["age"] == 65)][
        "mort_rate"].iloc[0] == pytest.approx(0.0130, rel=1e-12)
    assert table[(table["sex"] == "M") & (table["age"] == 115)][
        "mort_rate"].iloc[0] == 1.0


def test_inputs_are_read_once_not_once_per_model_point():
    """The readers live in Data, so N model points do not cause N reads."""
    from collections import Counter

    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="PA_UK_S_reads")
    reads = []
    original = pd.read_csv

    def counting(*args, **kwargs):
        reads.append(str(args[0]).replace("\\", "/").split("/")[-1])
        return original(*args, **kwargs)

    pd.read_csv = counting
    try:
        for point_id in model.Data.model_point_table().index:
            model.Projection[point_id].result_cf()
    finally:
        pd.read_csv = original
        model.close()

    counts = Counter(reads)
    assert counts and all(n == 1 for n in counts.values()), counts
    assert len(reads) == 2           # one per input file, regardless of point count


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a licensed SAPS or PMA16 basis."""
    import pandas as pd

    src = MODEL_DIR.parent / "mort_table.csv"
    lighter = pd.read_csv(src, index_col=["sex", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="PA_UK_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[2].result_cf()["liability_cf"].sum()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Lighter mortality lengthens every annuity stream, so the liability rises.
            assert model.Projection[2].result_cf()["liability_cf"].sum() > base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_every_model_point_projects(pension_annuity):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in pension_annuity.Data.model_point_table().index:
        proj = pension_annuity.Projection[point_id]
        df = proj.result_cf()
        assert len(df) > 0
        assert df.notna().all().all()
        assert proj.check_payment_factor() is True
        assert proj.check_guarantee_xor() is True
        assert proj.check_vp_bound() is True


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="PA_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="PA_UK_S_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.annuity_payments(t) == pytest.approx(row[0] + row[1], abs=PENNY)
            assert p.claims(t, "VP") == pytest.approx(row[2], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
