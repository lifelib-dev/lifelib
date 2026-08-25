"""Golden and structural tests for WOL_UK_S.

The golden values are the worked example in
products/whole_of_life/technical-notes.md ("Worked example"), which projects the
over-50s anchor cell: entry age 70 last birthday, non-smoker, GBP 30.00 a month for a
GBP 5,000 cash sum, premiums ceasing at month 240.  They are hard-coded here rather than
pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the penny, in-force to five
decimals.  The notes' table **omits expenses** "for clarity", so it is asserted against
``premiums(t)`` and ``claims(t, "DEATH")`` rather than against ``net_cf``.

Beyond the worked example this module asserts the product facts the notes call out as
modelling pitfalls, because each is a way an implementation can look right and be wrong:

* the month-12/13 moratorium boundary is a step, not a curve;
* the year-one refund base is cumulative premiums paid, not the cash sum;
* the accidental multiplier applies past the moratorium only;
* lapse must stop when premiums cease;
* and the two cells must not be given each other's mortality basis.
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
INFORCE = 5e-6        # in-force displayed to 5 d.p.

MODEL_DIR = LIB / MODELS["WOL_UK_S"][0]

# t: (policy year, CumPrem, DB non-accidental, DB accidental, l(t-1),
#     E[premium], E[death outgo])
WORKED_EXAMPLE = {
    1:   (1,  30.00,   30.00, 5000.0, 1.00000, 30.00,  0.36),
    6:   (1, 180.00,  180.00, 5000.0, 0.95613, 28.68,  0.63),
    12:  (1, 360.00,  360.00, 5000.0, 0.90601, 27.18,  0.91),
    13:  (2, 390.00, 5000.00, 5000.0, 0.89792, 26.94, 10.00),
    24:  (2, 720.00, 5000.00, 5000.0, 0.82785, 24.84,  9.22),
    60:  (5, 1800.00, 5000.00, 5000.0, 0.66359, 19.91,  9.88),
    120: (10, 3600.00, 5000.00, 5000.0, 0.42564, 12.77, 10.31),
    166: (14, 4980.00, 5000.00, 5000.0, 0.27420,  8.23,  9.85),
    167: (14, 5010.00, 5000.00, 5000.0, 0.27131,  8.14,  9.74),
    240: (20, 7200.00, 5000.00, 5000.0, 0.09992,  3.00,  6.57),
    241: (21, 7200.00, 5000.00, 5000.0, 0.09828,  0.00,  7.16),
}

# The notes' derived month-1 factors.
Q_M_1 = 0.0020223         # 1 - (1 - 0.024)^(1/12)
W_M_1 = 0.0069244         # 1 - (1 - 0.08)^(1/12)
Q_M_13 = 0.0022271        # q(2) = 0.0264


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_o50_anchor, t):
    """Every cell of the notes' eleven-row table, to the displayed precision."""
    year, cum, db_na, db_ac, pols, prem, death = WORKED_EXAMPLE[t]
    p = uk_o50_anchor
    assert p.policy_year(t) == year
    assert p.prem_cum_pp(t) == pytest.approx(cum, abs=PENNY)
    assert p.benefit_pp(t, "NON_ACC") == pytest.approx(db_na, abs=PENNY)
    assert p.benefit_pp(t, "ACC") == pytest.approx(db_ac, abs=PENNY)
    assert p.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert p.premiums(t) == pytest.approx(prem, abs=PENNY)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=PENNY)


def test_worked_example_month_one_trace(uk_o50_anchor):
    """E[death] = 1.0 x 0.0020223 x (0.97 x 30 + 0.03 x 5,000) = 0.0020223 x 179.10."""
    p = uk_o50_anchor
    assert p.mort_rate(1) == pytest.approx(0.024, rel=1e-12)
    assert p.mort_rate_mth(1) == pytest.approx(Q_M_1, abs=5e-8)
    assert p.lapse_rate(1) == 0.08
    assert p.lapse_rate_mth(1) == pytest.approx(W_M_1, abs=5e-8)
    assert p.benefit_pp(1, "DEATH") == pytest.approx(179.10, abs=PENNY)
    assert p.claims(1, "DEATH") == pytest.approx(Q_M_1 * 179.10, abs=PENNY)


def test_the_year_one_outgo_is_dominated_by_the_accidental_tail(uk_o50_anchor):
    """0.03 x 5,000 = 150 of the 179.10 blended benefit; only 29.10 is the refund.

    An implementation that dropped the accidental split would understate year-one claims
    by five sixths.
    """
    p = uk_o50_anchor
    accidental_part = 0.03 * 5000.0
    assert accidental_part / p.benefit_pp(1, "DEATH") > 0.83
    assert p.benefit_pp(1, "DEATH") == pytest.approx(
        0.97 * 30.0 + 0.03 * 5000.0, abs=PENNY)


def test_worked_example_month_thirteen_trace(uk_o50_anchor):
    """The moratorium ends: E[death] = 0.89792 x 0.0022271 x 5,000 = 10.00."""
    p = uk_o50_anchor
    assert p.mort_rate(13) == pytest.approx(0.0264, rel=1e-12)     # q(2) = 0.024 x 1.10
    assert p.mort_rate_mth(13) == pytest.approx(Q_M_13, abs=5e-8)
    assert p.benefit_pp(13, "DEATH") == pytest.approx(5000.0, abs=PENNY)
    assert p.claims(13, "DEATH") == pytest.approx(
        p.pols_if(13) * Q_M_13 * 5000.0, abs=PENNY)


def test_the_walk_through_basis_is_the_shipped_population_table(uk_o50_anchor):
    """q(y) = 0.024 x 1.10^(y-1) is the population table times the 120% loading.

    The notes describe their walk-through basis as "a 0.020 population-style rate at 70
    x the 120% anti-selection loading, with 10% p.a. age progression", so the shipped
    table is that and no special-casing is needed to reproduce the example.
    """
    p = uk_o50_anchor
    assert p.mort_basis() == "population"
    assert p.mort_loading() == 1.20
    for y in (1, 2, 5, 10, 20):
        t = 12 * (y - 1) + 1
        assert p.mort_rate(t) == pytest.approx(0.024 * 1.10 ** (y - 1), rel=1e-9)


# ---------------------------------------------------------------------------
# The moratorium


def test_the_moratorium_boundary_is_a_step(uk_o50_anchor):
    """An elevenfold jump in expected death outgo between months 12 and 13.

    The signature discontinuity of this product, and the notes' first-listed pitfall:
    an annual grid must split policy year 1 rather than smoothing across it.
    """
    p = uk_o50_anchor
    assert p.in_moratorium(12) is True
    assert p.in_moratorium(13) is False
    assert p.claims(13, "DEATH") / p.claims(12, "DEATH") > 10.0
    # The step is in the benefit, not in the mortality or the in-force.
    assert p.benefit_pp(12, "DEATH") < 600.0
    assert p.benefit_pp(13, "DEATH") == 5000.0
    assert p.pols_if(13) < p.pols_if(12)          # in-force moves smoothly across it


def test_the_refund_base_is_cumulative_premiums_paid(uk_o50_anchor):
    """Not the cash sum, and not an annualized premium - the notes' second pitfall."""
    p = uk_o50_anchor
    for t in range(1, 13):
        assert p.benefit_pp(t, "NON_ACC") == pytest.approx(30.0 * t, abs=PENNY)
        assert p.benefit_pp(t, "NON_ACC") < p.sum_assured()
    assert p.benefit_pp(1, "NON_ACC") == 30.0     # one month's premium, not nothing
    assert p.benefit_pp(12, "NON_ACC") == 360.0
    assert p.benefit_pp(13, "NON_ACC") == 5000.0


def test_accidental_death_pays_the_full_cash_sum_from_day_one(uk_o50_anchor):
    """No moratorium on the accidental benefit."""
    p = uk_o50_anchor
    assert all(p.benefit_pp(t, "ACC") == 5000.0 for t in (1, 6, 12, 13, 240))


def test_the_accidental_multiplier_applies_past_the_moratorium_only(whole_of_life):
    """Model point 2 doubles accidental death, but not inside the first twelve months.

    Applying it in year 1 - where the accidental benefit is already the full cash sum -
    or to all deaths, overstates outgo.  The notes list both as pitfalls.
    """
    p1, p2 = whole_of_life.Projection[1], whole_of_life.Projection[2]
    assert p2.adb_multiplier() == 2.0
    for t in range(1, 13):
        assert p2.benefit_pp(t, "ACC") == 5000.0            # unchanged in the moratorium
        assert p2.claims(t, "DEATH") == pytest.approx(p1.claims(t, "DEATH"), rel=1e-12)
    assert p2.benefit_pp(13, "ACC") == 10000.0
    assert p2.claims(13, "DEATH") > p1.claims(13, "DEATH")
    # And it moves only the accidental share, so the blended benefit rises by 3% of SA.
    assert p2.benefit_pp(13, "DEATH") == pytest.approx(
        5000.0 + 0.03 * 5000.0, abs=PENNY)


def test_the_underwritten_cell_has_no_moratorium_but_a_suicide_carve_out(whole_of_life):
    """A different rule with a different denominator: a refund, not a return of cover."""
    p = whole_of_life.Projection[5]
    assert p.cell() == "UW"
    assert p.moratorium_mths() == 0
    assert all(p.in_moratorium(t) is False for t in (1, 6, 12))
    # Inside the first twelve months, 1% of deaths refund premiums instead of paying SA.
    assert p.benefit_pp(1, "DEATH") == pytest.approx(
        0.99 * 150000.0 + 0.01 * 101.25, abs=PENNY)
    assert p.benefit_pp(13, "DEATH") == 150000.0
    assert p.benefit_pp(1, "NON_ACC") == 150000.0       # the non-accidental benefit is SA
    # The carve-out is small: a fraction of a percent of the benefit.
    assert p.benefit_pp(1, "DEATH") / 150000.0 > 0.98


# ---------------------------------------------------------------------------
# Lapse pays nothing, and stops when premiums do


def test_lapse_pays_nothing_on_either_cell(whole_of_life):
    """No surrender or paid-up value at any duration, on any model point."""
    for point_id in whole_of_life.Data.model_point_table().index:
        proj = whole_of_life.Projection[point_id]
        assert (proj.result_cf()["claims_lapse"] == 0.0).all()
    p = whole_of_life.Projection[1]
    assert p.pols_lapse(6) > 0.0                  # lapses happen
    assert p.claims(6, "LAPSE") == 0.0            # and pay nothing


def test_lapse_stops_when_premiums_cease(uk_o50_anchor):
    """Nothing left to stop paying - applying a decrement there destroys liability."""
    p = uk_o50_anchor
    assert p.cessation_mths() == 240
    assert p.lapse_rate(240) == 0.04
    assert p.lapse_rate(241) == 0.0
    assert p.lapse_rate_mth(241) == 0.0
    assert p.pols_lapse(241) == 0.0
    assert all(p.lapse_rate(t) == 0.0 for t in (241, 300, 500))


def test_the_post_cessation_period_is_pure_outgo(uk_o50_anchor):
    """Premium income stops at 241 but death outgo continues - and rises."""
    p = uk_o50_anchor
    assert p.premium_pp(240) == 30.0
    assert p.premium_pp(241) == 0.0
    assert p.premiums(241) == 0.0
    assert p.claims(241, "DEATH") > p.claims(240, "DEATH")
    assert p.net_cf(241) < 0.0
    # And the in-force runs off on mortality alone from there.
    assert p.pols_if(242) == pytest.approx(
        p.pols_if(241) * (1 - p.mort_rate_mth(241)), rel=1e-14)


def test_the_liability_falls_as_lapses_rise(whole_of_life):
    """The arithmetic meaning of lapse support, asserted rather than described.

    With no surrender value every lapse extinguishes a liability for nothing, so the
    projected outgo falls monotonically in the lapse rate.  It is the assumption to
    govern hardest on this product.
    """
    model = mx.read_model(MODEL_DIR, name="WOL_UK_S_lapse")
    try:
        def total_outgo(proj):
            df = proj.result_cf()
            return (df["claims_death"] + df["claims_death_pu"]).sum()

        base = total_outgo(model.Projection[1])
        # Raise lapse through the model's own crossover stress dial, which doubles the
        # rate past the tipping point, rather than shipping a second lapse table.
        model.Projection.lapse_crossover_beta = 1.0
        model.Projection.clear_all()
        stressed = total_outgo(model.Projection[1])
        assert stressed < base
    finally:
        model.close()


def test_the_crossover_stress_is_off_in_the_base_run(uk_o50_anchor):
    """beta = 0, so the table rate applies on both sides of the tipping point."""
    p = uk_o50_anchor
    assert p.lapse_rate(166) == p.lapse_rate_base(166)
    assert p.lapse_rate(167) == p.lapse_rate_base(167)
    assert p.lapse_rate(167) == 0.04


# ---------------------------------------------------------------------------
# The crossover


def test_the_crossover_month(uk_o50_anchor):
    """floor(5000/30) + 1 = 167 months: thirteen years and eleven months."""
    p = uk_o50_anchor
    assert p.crossover_mth() == 167
    assert 167 // 12 == 13 and 167 % 12 == 11
    assert p.prem_cum_pp(166) == pytest.approx(4980.0, abs=PENNY)
    assert p.prem_cum_pp(166) < p.cover_pp(166)
    assert p.prem_cum_pp(167) == pytest.approx(5010.0, abs=PENNY)
    assert p.prem_cum_pp(167) > p.cover_pp(167)


def test_total_premiums_are_capped_at_cessation(uk_o50_anchor):
    """P x T_cess = 7,200 against a 5,000 cash sum, so a crossover exists."""
    p = uk_o50_anchor
    assert p.prem_cum_pp(240) == pytest.approx(7200.0, abs=PENNY)
    assert p.prem_cum_pp(241) == pytest.approx(7200.0, abs=PENNY)   # no more premiums
    assert p.prem_cum_pp(600) == pytest.approx(7200.0, abs=PENNY)
    assert 7200.0 > p.sum_assured()


def test_no_crossover_where_the_cash_sum_exceeds_total_premiums(whole_of_life):
    """The underwritten anchor never crosses over: cover is 150,000 on 101.25 a month."""
    p = whole_of_life.Projection[5]
    assert p.crossover_mth() == 0
    assert p.prem_cum_pp(p.proj_len()) < p.sum_assured()


# ---------------------------------------------------------------------------
# The pro-rata paid-up variant


def test_pu_variant_converts_lapses_to_paid_up_after_the_halfway_point(whole_of_life):
    """N_paid >= N_expected/2 - month 120 on the anchor - and PU = SA x N_paid/N_expected."""
    p = whole_of_life.Projection[3]
    assert p.pu_variant() is True
    assert p.payments_expected() == 240
    assert p.pu_eligible(119) is False
    assert p.pu_eligible(120) is True
    assert p.pols_convert(119) == 0.0
    assert p.pols_convert(120) > 0.0
    assert p.benefit_pp(120, "PAID_UP") == pytest.approx(2500.0, abs=PENNY)
    assert p.benefit_pp(240, "PAID_UP") == pytest.approx(5000.0, abs=PENNY)
    # Before the halfway point a lapse is still a total loss.
    assert p.pols_lapse(119) > 0.0
    assert p.pols_lapse(120) == 0.0


def test_paid_up_policies_neither_lapse_nor_pay_premium(whole_of_life):
    """They roll forward on mortality alone, taking conversions in."""
    p = whole_of_life.Projection[3]
    for t in (150, 200, 300):
        assert p.pols_pu(t + 1) == pytest.approx(
            p.pols_pu(t) * (1 - p.mort_rate_mth(t)) + p.pols_convert(t), rel=1e-12)
    assert p.pols_pu(300) > 0.0
    # Premium income is carried on the full-cover strand only.
    assert p.premiums(150) == pytest.approx(p.premium_pp(150) * p.pols_if(150), rel=1e-14)


def test_the_paid_up_strand_carries_its_own_benefit_total(whole_of_life):
    """pu_benefit is the aggregate cover, which is why no cohort dimension is needed."""
    p = whole_of_life.Projection[3]
    for t in (150, 250):
        assert p.pu_benefit(t + 1) == pytest.approx(
            p.pu_benefit(t) * (1 - p.mort_rate_mth(t))
            + p.pols_convert(t) * p.benefit_pp(t, "PAID_UP"), rel=1e-12)
        assert p.claims(t, "DEATH_PU") == pytest.approx(
            p.pu_benefit(t) * p.mort_rate_mth(t), rel=1e-14)
    # The average paid-up payout sits between half and all of the cash sum.
    avg = p.pu_benefit(300) / p.pols_pu(300)
    assert 2500.0 <= avg <= 5000.0


def test_pu_variant_collapses_the_lapse_support(whole_of_life):
    """It converts lapse profit into a retained liability - a variant, not an adjustment."""
    p1, p3 = whole_of_life.Projection[1], whole_of_life.Projection[3]
    assert p3.result_cf()["net_cf"].sum() < p1.result_cf()["net_cf"].sum()
    assert p1.result_cf()["claims_death_pu"].sum() == 0.0
    assert p3.result_cf()["claims_death_pu"].sum() > 0.0


def test_pu_variant_needs_a_cessation_date(whole_of_life):
    """N_expected is measured to it, so the underwritten cell cannot carry the variant."""
    table = whole_of_life.Data.model_point_table()
    combined = (table["variant_paid_up"] & (table["cessation_months"] <= 0))
    assert not combined.any()


def test_the_other_cells_have_no_paid_up_strand(whole_of_life):
    for point_id in (1, 2, 4, 5, 6, 7):
        proj = whole_of_life.Projection[point_id]
        assert proj.pu_variant() is False
        assert (proj.result_cf()["pols_pu"] == 0.0).all()
        assert proj.pols_all(50) == proj.pols_if(50)


# ---------------------------------------------------------------------------
# The two bases


def test_the_cell_determines_the_basis(whole_of_life):
    """Derived, not a free parameter, so the two cells cannot be given each other's."""
    o50, uw = whole_of_life.Projection[1], whole_of_life.Projection[5]
    assert (o50.mort_basis(), o50.mort_loading()) == ("population", 1.20)
    assert (uw.mort_basis(), uw.mort_loading()) == ("assured", 1.00)
    names = set(whole_of_life.Projection.cells) | set(whole_of_life.Projection.refs)
    assert "mort_basis" in names
    # It is not a model point column, so no model point can override it.
    assert "mort_basis" not in whole_of_life.Data.model_point_table().columns


def test_the_population_basis_is_heavier_than_the_assured_one(whole_of_life):
    """The whole point of the split, at a common age and rating."""
    model = mx.read_model(MODEL_DIR, name="WOL_UK_S_bases")
    try:
        tbl = model.Data.mort_table()
        for age in (60, 70, 80):
            pop = float(tbl.loc[("population", "M", "NS", age), "mort_rate"])
            ass = float(tbl.loc[("assured", "M", "NS", age), "mort_rate"])
            assert pop > ass
    finally:
        model.close()


def test_the_mortality_improvement_dial_is_off_and_lightens_the_tail(whole_of_life):
    """Zero in the base run; improvements lengthen exactly the pure-outgo part."""
    p = whole_of_life.Projection[1]
    assert all(p.mort_improve_factor(t) == 1.0 for t in (1, 120, 500))

    model = mx.read_model(MODEL_DIR, name="WOL_UK_S_improve")
    try:
        model.Projection.mort_improvement = 0.01
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.mort_improve_factor(1) == 1.0
        assert proj.mort_improve_factor(13) == pytest.approx(0.99, rel=1e-12)
        assert proj.mort_rate(241) < p.mort_rate(241)
        assert proj.pols_if(500) > p.pols_if(500)      # more survivors in the tail
    finally:
        model.close()


def test_mortality_is_capped_at_one(whole_of_life):
    """The tables reach 1 before the limiting age, which is what exhausts the population."""
    p = whole_of_life.Projection[1]
    assert p.mort_rate(p.proj_len()) == 1.0
    assert p.mort_rate_mth(p.proj_len()) == 1.0
    assert all(p.mort_rate(t) <= 1.0 for t in range(1, p.proj_len() + 1, 12))


# ---------------------------------------------------------------------------
# Escalation


def test_the_underwritten_increasing_variant_raises_cover_5_and_premium_10(whole_of_life):
    """Two percent of premium for each one percent of cover."""
    p = whole_of_life.Projection[6]
    assert p.escalation() == "fixed_5pct"
    assert p.esc_cover_step() == 0.05
    assert p.esc_prem_step() == 0.10
    for y, t in ((1, 1), (2, 13), (5, 49)):
        assert p.cover_pp(t) == pytest.approx(150000.0 * 1.05 ** (y - 1), rel=1e-12)
        assert p.premium_pp(t) == pytest.approx(101.25 * 1.10 ** (y - 1), rel=1e-12)
    assert p.cover_pp(12) == p.cover_pp(1)       # steps on anniversaries only


def test_the_rpi_variant_keeps_indexing_the_cash_sum_after_premiums_cease(whole_of_life):
    """Cover +RPI capped at 10%, premium +1.5 x RPI capped at 15% while premiums are due."""
    p = whole_of_life.Projection[4]
    assert p.escalation() == "rpi"
    assert p.esc_cover_step() == pytest.approx(0.03, rel=1e-12)
    assert p.esc_prem_step() == pytest.approx(0.045, rel=1e-12)
    for y, t in ((1, 1), (2, 13), (10, 109)):
        assert p.cover_pp(t) == pytest.approx(5000.0 * 1.03 ** (y - 1), rel=1e-12)
        assert p.premium_pp(t) == pytest.approx(30.0 * 1.045 ** (y - 1), rel=1e-12)
    # Premiums stop at cessation; the cash sum keeps indexing past it.
    assert p.premium_pp(241) == 0.0
    assert p.cover_pp(241) > p.cover_pp(240)
    assert p.cover_pp(360) > p.cover_pp(241)


def test_the_rpi_caps(whole_of_life):
    """min(max(RPI, 0), 10%) on cover and min(max(1.5 RPI, 0), 15%) on premium."""
    model = mx.read_model(MODEL_DIR, name="WOL_UK_S_rpi")
    try:
        model.Projection.rpi_rate = 0.25
        model.Projection.clear_all()
        proj = model.Projection[4]
        assert proj.esc_cover_step() == pytest.approx(0.10, rel=1e-12)
        assert proj.esc_prem_step() == pytest.approx(0.15, rel=1e-12)
        model.Projection.rpi_rate = -0.02          # the source defines an increase only
        model.Projection.clear_all()
        proj = model.Projection[4]
        assert proj.esc_cover_step() == 0.0
        assert proj.esc_prem_step() == 0.0
    finally:
        model.close()


def test_a_level_cell_does_not_escalate(uk_o50_anchor):
    p = uk_o50_anchor
    assert p.escalation() == "level"
    assert p.esc_cover_step() == 0.0 and p.esc_prem_step() == 0.0
    assert all(p.cover_pp(t) == 5000.0 for t in (1, 13, 240, 600))


# ---------------------------------------------------------------------------
# Roll-forward and truncation


def test_the_rollforward_closes(whole_of_life):
    """pols_all(t) - pols_all(t+1) is deaths and terminating lapses, not conversions."""
    for point_id in whole_of_life.Data.model_point_table().index:
        proj = whole_of_life.Projection[point_id]
        assert proj.check_pols_roll_fwd() is True, point_id
    p = whole_of_life.Projection[3]               # the strand-splitting one
    for t in (50, 150, 300):
        out = p.pols_death(t) + p.pols_death_pu(t) + p.pols_lapse(t)
        assert p.pols_all(t) - p.pols_all(t + 1) == pytest.approx(out, abs=1e-12)
    assert p.pols_convert(150) > 0.0              # conversions move between strands
    assert p.pols_lapse(150) == 0.0


def test_the_truncation_residual_is_negligible(whole_of_life):
    """Whole of life has no maturity, so anything left at the limiting age is dropped.

    The check exists to say the limiting age is high enough, not that a benefit is paid:
    pols_maturity here is a truncation artefact and pays nothing.
    """
    for point_id in whole_of_life.Data.model_point_table().index:
        proj = whole_of_life.Projection[point_id]
        assert proj.check_truncation() is True, point_id
        assert proj.pols_maturity(proj.proj_len()) < 1e-9
    p = whole_of_life.Projection[1]
    assert all(p.pols_maturity(t) == 0.0 for t in (1, 240, 599))


def test_the_projection_runs_to_the_limiting_age(uk_o50_anchor):
    p = uk_o50_anchor
    assert p.proj_len() == 600 == 12 * (120 - 70)
    assert p.age(1) == 70
    assert p.age(600) == 119
    assert p.pols_if(601) == 0.0


# ---------------------------------------------------------------------------
# What the product does not have


def test_none_of_the_us_whole_life_machinery_exists(whole_of_life):
    """No cash value, no dividends, no paid-up additions, no loans - a product fact.

    WholeLife_US_A is built around all four; these two UK cells are pure decrement
    protection models, and importing that chassis would invent a benefit that does not
    exist.
    """
    names = set(whole_of_life.Projection.cells) | set(whole_of_life.Projection.refs)
    for absent in ("cv_pp", "div_base", "div_credited", "div_accum", "pua_face",
                   "pua_cv", "loan_bal", "nsp", "np_guar", "net_amt_at_risk",
                   "av_pp_at", "asset_share", "mvr"):
        assert absent not in names


def test_terminal_illness_is_not_a_second_decrement(whole_of_life):
    """It accelerates the death benefit; it does not add one.

    The base model ignores the acceleration and pays at death, which understates the
    present value slightly.  Modelling it as an extra decrement would double-count.
    """
    names = set(whole_of_life.Projection.cells) | set(whole_of_life.Projection.refs)
    assert not [n for n in names if n.startswith("ti_") or "_ti_" in n]


def test_invalid_enum_values_raise(uk_o50_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        uk_o50_anchor.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        uk_o50_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        uk_o50_anchor.benefit_pp(1, "MATURITY")


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_o50_anchor):
    df = uk_o50_anchor.result_cf()
    assert list(df.index) == list(range(1, 601))
    assert list(df.columns) == [
        "pols_if", "pols_pu", "premiums", "claims_death", "claims_death_pu",
        "claims_lapse", "expenses", "commissions", "net_cf",
    ]


def test_result_cf_rows_sum_to_net_cf(uk_o50_anchor):
    """The cash flow columns are a decomposition of net_cf, not a selection from it."""
    df = uk_o50_anchor.result_cf()
    outgo = df[["claims_death", "claims_death_pu", "claims_lapse", "expenses",
                "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)


def test_the_notes_table_omits_expenses(uk_o50_anchor):
    """So net_cf equals no column of it - the goldens are premiums and death outgo."""
    p = uk_o50_anchor
    assert p.expenses(1) > 0.0
    assert p.commissions(1) > 0.0
    assert p.net_cf(1) != pytest.approx(30.00 - 0.36, abs=0.5)
    assert p.net_cf(1) == pytest.approx(
        p.premiums(1) - p.claims(1) - p.expenses(1) - p.commissions(1), rel=1e-14)


def test_expenses_differ_by_cell(whole_of_life):
    """Acquisition 150 / 300 and maintenance 30 / 50 a year, both [std]."""
    o50, uw = whole_of_life.Projection[1], whole_of_life.Projection[5]
    assert (o50.expense_acq_pp(), o50.expense_maint_pp()) == (150.0, 30.0)
    assert (uw.expense_acq_pp(), uw.expense_maint_pp()) == (300.0, 50.0)
    assert o50.expenses(1) == pytest.approx(150.0 + 30.0 / 12, abs=PENNY)
    assert o50.expenses(13) == pytest.approx(
        30.0 / 12 * 1.03 * o50.pols_all(13), rel=1e-12)


def test_commission_is_first_year_only(uk_o50_anchor):
    p = uk_o50_anchor
    assert p.commissions(1) == pytest.approx(0.25 * p.premiums(1), rel=1e-12)
    assert p.commissions(12) > 0.0
    assert p.commissions(13) == 0.0


def test_model_docstring_describes_the_current_structure(whole_of_life):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = whole_of_life.doc
    assert "whole of life" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "moratorium" in doc
    assert "WholeLife_US_A" in doc               # the contrast it is drawn against


def test_space_docstrings_carry_their_reference_material(whole_of_life):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = whole_of_life.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("pols_if", "pols_pu", "prem_cum_pp", "crossover_mth",
                  "benefit_pp", "mort_basis"):
        assert cells in proj
    data = whole_of_life.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "mort_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_the_library_vocabulary(whole_of_life):
    """Names shared with lifelib and with the rest of this library must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "sum_assured", "proj_len", "age",
        "pols_if", "pols_if_at", "pols_if_init", "pols_death", "pols_lapse",
        "pols_maturity", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "premiums", "claims", "benefit_pp", "expenses", "inflation_rate",
        "inflation_factor", "commissions", "net_cf", "result_cf", "policy_year",
        "duration", "duration_mth",
    }
    names = set(whole_of_life.Projection.cells) | set(whole_of_life.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """The three input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Both bases are [std] proxies, and the file says which cells are the anchors."""
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert table["provenance"].notna().all()
    assert set(table["basis"]) == {"population", "assured"}
    anchor = table[table["provenance"] == "notes walk-through anchor [std]"]
    assert set(anchor["basis"]) == {"population"}
    assert set(anchor["sex"]) == {"F"} and set(anchor["smoker"]) == {"NS"}
    row70 = anchor[anchor["age"] == 70]["mort_rate"].iloc[0]
    assert row70 == pytest.approx(0.020, rel=1e-12)
    assert row70 * 1.20 == pytest.approx(0.024, rel=1e-12)


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows."""
    import pandas as pd

    src = MODEL_DIR.parent / "mort_table.csv"
    lighter = pd.read_csv(src, index_col=["basis", "sex", "smoker", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="WOL_UK_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].claims(13, "DEATH")
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].mort_rate(1) == pytest.approx(0.012, rel=1e-12)
            assert model.Projection[1].claims(13, "DEATH") < base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="WOL_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="WOL_UK_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[4], abs=INFORCE)
            assert anchor.claims(t, "DEATH") == pytest.approx(row[6], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
