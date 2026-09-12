"""Golden and structural tests for Rente_FR_S.

The golden values are the worked example in
products/rente_viagere/technical-notes.md ("Worked example"), which is a **scenario**:
EUR 200,000 of capital converted on 1 April 2026 for a male 65 born 1961, with a
reversion at 60% to a female 61 born 1965, monthly in arrears, taux de rente 3.30% on a
zero taux technique, reversion coefficient 0.76, frais d'arrerages 3.00%, revalorisation
1.50% a year credited at 31 December and pro-rated 9/12 in 2026 -- and the annuitant dies
in month 25, the 26th month of service, while the reversionary survives throughout.  Model
point 1 is that cell.  They are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

The month index ``t`` is **0-based**: ``t = 0`` is the first projected month and the frame
is ``t = 0 .. proj_len() - 1``, as in the notes' worked-example table.  ``lives_if(t, life)``
is the exception a reader should keep in mind: it is a **time-point** cells, the survival
to time t with t = 0 at the effective date, so month t opens at ``lives_if(t)`` and closes
at ``lives_if(t + 1)`` and its own index does not shift with the frame.

Tolerances follow the precision the notes display: money to the cent, the revalorisation
index to six decimals.

Beyond the worked example there is a test for each of the fourteen ways the notes say an
implementation of *this* product can look right and be wrong, each named for the failure
it catches: the generational table taking no improvement scale and no projection year; the
tariff and best-estimate tables staying separate objects; revalorisation as a calendar
event with a first-year pro-rata; the *arrerage* of the month of death paid in full and
the reversion opening the month after it; the *annuites garanties* as a floor that gates
the *prorata* off; the definitive reversion coefficient applied once; the absence of any
surrender and the commutation threshold as an admission test; the two charges, one of
which never touches an instalment; the *taux technique* reaching no cash flow; and the
*palier* never reaching the reversion stream.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built: they read the cells docstrings
    by importing ``Projection`` and ``Data``.  Those caches are not part of the model and
    must not make a round-trip comparison fail for anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
SIX = 5e-7            # the revalorisation index, displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Rente_FR_S"][0]

# t: (R(t), gross arrerage, frais at 3%, net to the payee)
# The notes' worked-example table, verbatim.  "Gross" is what leaves the insurer on the
# annuity account in month t: the scheduled instalment while the annuitant lives, the
# *prorata d'arrerages* in the month of death, the reversion instalment afterwards.
WORKED_EXAMPLE = {
    0:  (1.000000, 418.00, 12.54, 405.46),
    8:  (1.000000, 418.00, 12.54, 405.46),
    9:  (1.011250, 422.70, 12.68, 410.02),
    11: (1.011250, 422.70, 12.68, 410.02),
    20: (1.011250, 422.70, 12.68, 410.02),
    21: (1.026419, 429.04, 12.87, 416.17),
    24: (1.026419, 429.04, 12.87, 416.17),
    25: (1.026419, 429.04, 12.87, 416.17),   # annuitant dies; prorata to the heirs
    26: (1.026419, 257.43,  7.72, 249.70),   # reversion begins at 60%
    29: (1.026419, 257.43,  7.72, 249.70),
    32: (1.026419, 257.43,  7.72, 249.70),
    33: (1.041815, 261.29,  7.84, 253.45),
    35: (1.041815, 261.29,  7.84, 253.45),
}


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_rente_anchor, t):
    """Every cell of the notes' table, to the displayed precision."""
    revalo, gross, frais, net = WORKED_EXAMPLE[t]
    p = fr_rente_anchor
    assert p.revalo_factor(t) == pytest.approx(revalo, abs=SIX)
    paid = p.annuity_payments(t) + p.claims(t, "PRORATA")
    assert paid == pytest.approx(gross, abs=CENT)
    assert p.arrerage_charges(t) == pytest.approx(frais, abs=CENT)
    assert paid - p.arrerage_charges(t) == pytest.approx(net, abs=CENT)


def test_the_conversion_arithmetic(fr_rente_anchor):
    """A0 = C rho kappa = 200,000 x 0.0330 x 0.76 = 5,016.00, so 418.00 a month."""
    p = fr_rente_anchor
    assert p.purchase_price() == 200000.0
    assert p.annuity_rate() == 0.033
    assert p.reversion_pct() == 0.60
    assert p.option_coeff() == 0.76
    assert p.annual_income_init() == pytest.approx(5016.00, abs=CENT)
    assert p.annuity_pp(0) == pytest.approx(418.00, abs=CENT)
    # And it clears the statutory commutation threshold, so the point projects.
    assert p.check_commutation_floor() is True


def test_the_instalment_schedule(fr_rente_anchor):
    """Monthly terme echu: every month pays, and survival is measured at the end of it."""
    p = fr_rente_anchor
    assert p.payment_freq() == 12 and p.payment_timing() == "arrears"
    assert all(p.is_payment_mth(t) for t in (0, 8, 25, 399))
    # Arrears: the instalment of month t needs survival to time t + 1, its end.
    assert all(p.payment_surv_mth(t) == t + 1 for t in (0, 8, 25))
    assert p.annuity_pp(8) == pytest.approx(418.00, abs=CENT)
    assert p.annuity_pp(9) == pytest.approx(422.7025, abs=1e-4)
    assert p.annuity_pp(21) == pytest.approx(429.043038, abs=1e-4)
    # 5,016.00 x 1.011250 / 12 is the month-9 instalment, a different way.
    assert 5016.00 * 1.011250 / 12 == pytest.approx(422.7025, abs=1e-4)


def test_the_cumulative_arrerages_and_the_total_charge(fr_rente_anchor):
    """26 amounts over 26 months of service: 9 + 12 + 5, the last of the five a prorata."""
    p = fr_rente_anchor
    total = 9 * 418.00 + 12 * 422.7025 + 5 * 429.043038
    assert total == pytest.approx(10979.65, abs=CENT)
    assert p.cum_annuity_pp(25, "ALL") == pytest.approx(10979.65, abs=CENT)
    retained = sum(p.arrerage_charges(t) for t in range(26))
    assert retained == pytest.approx(329.39, abs=CENT)
    assert p.cum_annuity_pp(25, "ALL") - retained == pytest.approx(10650.26, abs=CENT)
    # Nothing more is paid to the annuitant or his heirs after month 25.
    assert p.cum_annuity_pp(26, "ALL") - p.cum_annuity_pp(25, "ALL") == pytest.approx(
        257.4258, abs=1e-4)


def test_the_full_liability_cash_flow_at_two_months(fr_rente_anchor):
    """liability_cf(9) = 412.56 and liability_cf(26) = 252.28, with net_cf the negative."""
    p = fr_rente_anchor
    assert p.liability_cf(9) == pytest.approx(422.7025 * 0.97 + 2.5 * 1.015, abs=1e-6)
    assert p.liability_cf(9) == pytest.approx(412.56, abs=CENT)
    assert p.liability_cf(26) == pytest.approx(
        257.425822 * 0.97 + 2.5 * 1.015 ** 2, abs=1e-4)
    assert p.liability_cf(26) == pytest.approx(252.28, abs=CENT)
    assert p.net_cf(9) == pytest.approx(-p.liability_cf(9), rel=1e-15)


def test_the_scenario_basis_is_a_step_function(fr_rente_anchor):
    """1{t <= death_mth}: the annuitant dies in month 25, the reversionary never."""
    p = fr_rente_anchor
    assert p.mort_basis() == "scenario"
    assert p.death_mth(1) == 25 and p.death_mth(2) == -1
    # lives_if is survival to *time* t, so the annuitant is alive at time 25 - the start
    # of the month he dies in - and gone from time 26, its end.  The index is a time
    # point and does not shift with the frame.
    assert [p.lives_if(t, 1) for t in (24, 25, 26, 27)] == [1.0, 1.0, 0.0, 0.0]
    assert all(p.lives_if(t, 2) == 1.0 for t in (0, 100, 700))
    assert p.lives_death(25, 1) == 1.0
    assert sum(p.lives_death(t, 1) for t in range(p.proj_len())) == 1.0


# ---------------------------------------------------------------------------
# Pitfall 1: an improvement scale on top of a generational table


def test_no_improvement_scale_on_a_generational_table(rente_viagere):
    """q is a pure table lookup: no improvement factor, no calendar-year argument.

    TGH05/TGF05 are prospective, so the trend is inside the table; any improvement scale
    applied on top of it double-counts the trend.
    """
    names = set(rente_viagere.Projection.cells) | set(rente_viagere.Projection.refs)
    for absent in ("improve_factor", "improve_rate", "improve_rate_base",
                   "improve_flat_age", "improve_taper_age", "mort_table_year",
                   "annuitant_adj", "rating_factor"):
        assert absent not in names
    p = rente_viagere.Projection[2]
    table = rente_viagere.Data.mort_table()
    raw = float(table.loc[("M", 1961, 65), "mort_rate"])
    assert p.mort_rate(0, 1) == raw          # no factor of any kind on top
    # And it is flat across the twelve months of a year of age: q moves with the attained
    # age and with nothing else, least of all the projection year.
    assert len({p.mort_rate(t, 1) for t in range(12)}) == 1
    assert p.calendar_year(0) == 2026 and p.calendar_year(9) == 2027
    assert p.mort_rate(0, 1) == p.mort_rate(8, 1)     # 2026 and 2026
    assert p.mort_rate(8, 1) == p.mort_rate(9, 1)     # 2026 and 2027, same age


# ---------------------------------------------------------------------------
# Pitfall 2: indexing the table by the projection year instead of the millesime


def test_the_table_is_keyed_on_the_millesime_not_the_projection_year(rente_viagere):
    """Two annuitants aged 65 at entry, born 1961 and 1963, must differ at age 65.

    A period-table implementation reads the rate for the attained age in the projection
    calendar year and walks diagonally across generations; a generational one reads
    (g, x) whatever the year.  The two model points make the difference visible.
    """
    older, younger = rente_viagere.Projection[2], rente_viagere.Projection[10]
    assert older.age_at_entry(1) == younger.age_at_entry(1) == 65
    assert older.birth_year(1) == 1961 and younger.birth_year(1) == 1963
    assert older.effective_year() == 2026 and younger.effective_year() == 2028
    assert older.age(0, 1) == younger.age(0, 1) == 65
    assert younger.mort_rate(0, 1) < older.mort_rate(0, 1)
    # Two years of the shipped table's own improvement, and nothing else: the proxy
    # improves the force of mortality at 1.0% a millesime, so the ratio of the rates is
    # 0.99 squared up to the convexity of q = 1 - exp(-mu).
    assert younger.mort_rate(0, 1) / older.mort_rate(0, 1) == pytest.approx(
        0.99 ** 2, rel=1e-3)
    # The millesime is a model point attribute read from the table, never derived from
    # the calendar, and no mortality cells takes the calendar year as an argument.
    proj = rente_viagere.Projection
    assert "effective_year" not in proj.cells["birth_year"].formula.source
    assert "calendar_year" not in proj.cells["birth_year"].formula.source
    for cells in ("mort_rate", "mort_rate_at_age", "mort_rate_mth", "lives_if",
                  "tariff_lives"):
        assert "calendar_year" not in proj.cells[cells].formula.source


# ---------------------------------------------------------------------------
# Pitfall 3: using the tariff table as the best estimate


def test_the_tariff_table_and_the_best_estimate_table_are_different_objects(
        rente_viagere):
    """The tariff is TGF05 for every life; the projection decrements on the life's own.

    Collapsing them makes the unisex prudence margin invisible - no surplus, so no source
    for the revalorisation the contract shares.
    """
    p = rente_viagere.Projection[2]
    assert rente_viagere.Projection.tariff_table_sex == "F"
    assert p.sex(1) == "M"
    # The tariff factor is struck on the female table whatever the annuitant's sex, and
    # the shipped proxy is anchored so it reproduces the notes' placeholder rho exactly.
    assert p.annuity_factor("F") == pytest.approx(29.630420, abs=1e-5)
    assert p.taux_rente_tariff() == pytest.approx(0.0330, abs=1e-9)
    assert p.annuity_rate() == 0.0330
    # His own table would give 3.73% - spec footnote 7 - and 13.0% more income.
    assert p.annuity_factor("M") == pytest.approx(26.214580, abs=1e-5)
    assert p.taux_rente_own_table() == pytest.approx(0.0373, abs=1e-9)
    assert p.unisex_gap() == pytest.approx(0.1303, abs=5e-5)
    assert 200000 * p.taux_rente_own_table() * 0.76 == pytest.approx(5669.60, abs=CENT)
    assert 200000 * p.taux_rente_own_table() * 0.76 / 12 == pytest.approx(
        472.47, abs=CENT)
    # The projection decrements him on the male table, which is heavier than the tariff.
    assert p.mort_rate(0, 1) > p.mort_rate_at_age("F", 1961, 65)
    # A female annuitant's own table *is* the tariff table, so there is no gap.
    f = rente_viagere.Projection[8]
    assert f.sex(1) == "F"
    assert f.unisex_gap() == pytest.approx(0.0, abs=1e-9)
    # And a ``mix`` model point blends the two best-estimate tables at theta without
    # ever becoming a tariff basis: the tariff stays the female table.
    blend = rente_viagere.Projection[9]
    theta = rente_viagere.Projection.portfolio_male_share
    assert blend.sex(1) == "mix" and theta == 0.45
    male, female = blend.mort_rate_at_age("M", 1956, 70), blend.mort_rate_at_age("F", 1956, 70)
    assert blend.mort_rate(0, 1) == pytest.approx(
        theta * male + (1 - theta) * female, rel=1e-14)
    assert female < blend.mort_rate(0, 1) < male
    assert blend.taux_rente_tariff() == pytest.approx(blend.annuity_rate(), abs=1e-6)
    assert blend.unisex_gap() > 0.0


# ---------------------------------------------------------------------------
# Pitfalls 4 and 5: the revalorisation date and the first-year pro-rata


def test_revalorisation_falls_on_31_december_not_the_anniversary(fr_rente_anchor):
    """k(t) counts 31 Decembers: nine months at the initial level, not twelve.

    On a policy-anniversary convention the uplift would not arrive until t = 12 and the
    March 2027 row would still read 418.00.
    """
    p = fr_rente_anchor
    assert p.effective_month() == 4 and p.effective_year() == 2026
    assert [p.cal_year_index(t) for t in (0, 8, 9, 20, 21, 32, 33)] == [
        0, 0, 1, 1, 2, 2, 3]
    assert p.civil_month(8) == 12 and p.civil_month(9) == 1
    assert p.annuity_pp(8) == pytest.approx(418.00, abs=CENT)
    assert p.annuity_pp(9) > p.annuity_pp(8)
    assert p.annuity_pp(11) == pytest.approx(422.7025, abs=1e-4)   # March 2027
    assert p.annuity_pp(12) == p.annuity_pp(11)                    # no anniversary step
    assert p.check_calendar_index() is True
    assert p.check_revalo_roll_fwd() is True


def test_the_first_year_pro_rata_and_the_january_application(rente_viagere):
    """The first uplift is nu(13 - M0)/12, and the credit reaches January instalments.

    Applying the full nu overstates the annuity for the whole of its remaining life,
    because R is a running product; applying the credit to the December arrears instalment
    adds one instalment a year at the new level.
    """
    p = rente_viagere.Projection[1]
    nu = rente_viagere.Projection.revalo_rate
    assert nu == 0.015
    assert p.revalo_factor(8) == 1.0
    assert p.revalo_factor(9) == pytest.approx(1 + nu * 9 / 12, rel=1e-15)
    assert p.revalo_factor(21) == pytest.approx((1 + nu * 9 / 12) * (1 + nu), rel=1e-15)
    assert p.revalo_factor(33) == pytest.approx(
        (1 + nu * 9 / 12) * (1 + nu) ** 2, rel=1e-15)
    # A 1 January effective date degenerates to the full nu: the general form is right.
    jan = rente_viagere.Projection[5]
    assert jan.effective_month() == 1
    assert jan.revalo_factor(11) == 1.0
    assert jan.revalo_factor(12) == pytest.approx(1 + nu, rel=1e-15)
    # And the uplift is floored at zero in every configuration.
    for point_id in rente_viagere.Data.model_point_table().index:
        assert rente_viagere.Projection[point_id].check_revalo_floor() is True


def test_a_negative_revalorisation_rate_cannot_cut_the_annuity(rente_viagere):
    """The contractual floor is zero: a rente in payment can stand still, never fall."""
    model = mx.read_model(MODEL_DIR, name="Rente_FR_S_floor")
    try:
        model.Projection.revalo_rate = -0.02
        model.Projection.clear_all()
        p = model.Projection[1]
        assert all(p.revalo_factor(t) == 1.0 for t in (0, 9, 21, 99))
        assert p.check_revalo_floor() is True
        assert p.annuity_pp(21) == pytest.approx(418.00, abs=CENT)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall 6: losing the arrerage of the month of death


def test_the_arrerage_of_the_month_of_death_is_paid_in_full(fr_rente_anchor):
    """At m = 12 the prorata is one whole instalment, and 26 are paid over 26 months."""
    p = fr_rente_anchor
    assert p.mths_since_payment(25) == 0
    assert p.prorata_pp(25) == pytest.approx(429.043038, abs=1e-4)
    assert p.prorata_factor(25) == 1.0
    assert p.claims(25, "PRORATA") == pytest.approx(429.04, abs=CENT)
    # No scheduled instalment in the death month: survival at the end of it, l_a(26),
    # is 0, so the payment factor is 0.
    assert p.annuity_payments(25) == 0.0
    paid = [t for t in range(p.proj_len())
            if p.annuity_payments(t) + p.claims(t, "PRORATA") > 0]
    assert len([t for t in paid if t <= 25]) == 26
    # Losing it would understate the outgo by exactly one arrerage.
    assert sum(p.claims(t, "PRORATA") for t in range(p.proj_len())) == (
        pytest.approx(429.04, abs=CENT))


def test_the_prorata_fraction_at_a_quarterly_frequency(rente_viagere):
    """h(t) = t mod 3: one third in the first month of a quarter, two thirds in the second."""
    p = rente_viagere.Projection[6]
    assert p.payment_freq() == 4
    assert [t for t in range(12) if p.is_payment_mth(t)] == [2, 5, 8, 11]
    assert [p.mths_since_payment(t) for t in (24, 25, 26)] == [0, 1, 2]
    quarter = p.annuity_pp(26) if p.is_payment_mth(26) else None
    assert quarter is not None
    assert p.prorata_pp(24) == pytest.approx(quarter / 3, rel=1e-12)
    assert p.prorata_pp(25) == pytest.approx(2 * quarter / 3, rel=1e-12)
    assert p.prorata_pp(26) == pytest.approx(quarter, rel=1e-12)
    # The scenario death falls in the second month of the quarter.
    assert p.death_mth(1) == 25
    assert p.claims(25, "PRORATA") == pytest.approx(2 * quarter / 3, rel=1e-12)
    assert p.annuity_payments(26) == 0.0


# ---------------------------------------------------------------------------
# Pitfall 7: starting the reversion in the month of death


def test_the_reversion_starts_the_month_after_death(fr_rente_anchor):
    """The gate is (1 - l_a(t)): gating on the month's end pays it 1 + delta times."""
    p = fr_rente_anchor
    assert p.reversion_factor(24) == 0.0
    assert p.reversion_factor(25) == 0.0          # l_a(25) = 1, so the gate is shut
    assert p.reversion_factor(26) == pytest.approx(0.60, rel=1e-14)
    assert p.annuity_pp(26) * p.reversion_factor(26) == pytest.approx(257.43, abs=CENT)
    # 60% of the rente atteinte at death, a different way.
    assert 0.60 * 429.043038 == pytest.approx(257.4258, abs=1e-4)
    # The month of death is paid exactly once, as a prorata and not as 1 + delta.
    paid_death_mth = p.annuity_payments(25) + p.claims(25, "PRORATA")
    assert paid_death_mth == pytest.approx(p.annuity_pp(24), abs=1e-4)
    assert paid_death_mth < (1 + 0.60) * p.annuity_pp(24)


# ---------------------------------------------------------------------------
# Pitfall 8: the guarantee is a floor, and it gates the prorata off


def test_the_guarantee_is_a_floor_not_a_second_stream(rente_viagere):
    """max(gamma, l_a), never gamma + l_a, which would pay 1 + l_a for the whole term."""
    p = rente_viagere.Projection[3]
    assert p.guarantee_mths() == 180
    assert p.reversion_pct() == 0.0
    assert p.check_payment_factor() is True
    assert p.certain_floor(11) == 1.0 and p.payment_factor_life(11) == 1.0
    assert p.payment_factor(11) == 1.0
    assert p.certain_floor(11) + p.payment_factor_life(11) == 2.0
    # Inside the guarantee the full instalment is payable though the annuitant is dead.
    assert p.lives_if(26, 1) == 0.0               # a time point: dead from time 26
    assert p.certain_floor(99) == 1.0 and p.payment_factor_life(99) == 0.0
    assert p.payment_factor(99) == 1.0
    # And nothing after it: there is no reversion in that configuration.
    assert p.certain_floor(179) == 1.0 and p.certain_floor(180) == 0.0
    assert p.payment_factor(180) == 0.0
    assert p.liability_cf(180) == 0.0
    # And no prorata is due while the floor holds: the full instalment is already
    # payable, so settling an accrued one on top double-pays the month of death.
    assert p.lives_death(25, 1) == 1.0 and p.certain_floor(25) == 1.0
    assert p.prorata_factor(25) == 0.0
    assert all(p.claims(t, "PRORATA") == 0.0 for t in range(180))


def test_the_annuites_garanties_variant_reproduces_the_notes(rente_viagere):
    """The coefficient is derived, so a 25-year term costs more than a 5-year one."""
    p = rente_viagere.Projection[3]
    assert p.certain_excess_years() == pytest.approx(0.5431, abs=5e-5)
    assert p.guarantee_coeff() == pytest.approx(0.982002, abs=5e-7)
    assert p.option_coeff() == p.guarantee_coeff()
    assert p.annual_income_init() == pytest.approx(6481.21, abs=CENT)
    assert p.annuity_pp(0) == pytest.approx(540.10, abs=CENT)
    assert p.annuity_pp(9) == pytest.approx(546.18, abs=CENT)
    assert p.annuity_pp(21) == pytest.approx(554.37, abs=CENT)
    # The death in month 25 changes nothing at all: the instalment continues unchanged
    # to the designated beneficiaries and rises with the same revalorisation index.
    assert p.annuity_payments(25) == pytest.approx(554.37, abs=CENT)
    assert p.annuity_payments(26) == pytest.approx(554.37, abs=CENT)
    # In expectation the same flows come out of the table basis while the floor holds.
    expected = rente_viagere.Projection[4]
    assert expected.mort_basis() == "table"
    for t in (0, 9, 21, 99, 179):
        assert expected.annuity_payments(t) == pytest.approx(
            p.annuity_payments(t), abs=CENT)
    assert expected.annuity_payments(180) < p.annuity_pp(180)


# ---------------------------------------------------------------------------
# Pitfall 9: mishandling the reversion coefficient


def test_the_reversion_coefficient_is_definitive_and_applies_once(rente_viagere):
    """kappa reduces the annuitant's own annuity at conversion and nothing else.

    It must not also scale the reversion stream - the survivor receives delta times the
    *already reduced* annuity reached at death - and it is not released if the
    reversionary predeceases the annuitant.
    """
    p = rente_viagere.Projection[1]
    assert p.birth_year(2) - p.birth_year(1) == 4     # younger by 4 years
    assert p.reversion_coeff() == 0.76                # "younger by 4-7 / 60%"
    assert p.annual_income_init() == pytest.approx(200000 * 0.033 * 0.76, abs=CENT)
    # The reversion is delta x the already reduced instalment: 0.76 is applied once.
    assert p.annuity_pp(26) * p.reversion_factor(26) == pytest.approx(
        0.60 * p.annuity_pp(26), rel=1e-14)
    assert p.annuity_pp(26) * p.reversion_factor(26) != pytest.approx(
        0.60 * 0.76 * p.annuity_pp(26), rel=1e-6)
    # A different band and a different published column give a different coefficient.
    older = rente_viagere.Projection[9]
    assert older.birth_year(2) - older.birth_year(1) == -6      # older by 6 years
    assert older.reversion_pct() == 1.00
    assert older.reversion_coeff() == 0.83
    # No option, no coefficient.
    assert rente_viagere.Projection[5].option_coeff() == 1.0


def test_a_taux_de_reversion_off_the_published_grid_raises(rente_viagere):
    """The [S6] table publishes 60%, 80% and 100%; the model refuses to guess the rest."""
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Rente_FR_S_revcoeff")
    try:
        src = model.Data.input_dir() / "reversion_coeff_table.csv"
        trimmed = pd.read_csv(src)
        trimmed = trimmed[trimmed["reversion_pct"] != 0.60]
        alt = "reversion_coeff_table_trimmed.csv"
        trimmed.to_csv(model.Data.input_dir() / alt, index=False)
        try:
            assert model.Projection[1].reversion_coeff() == 0.76
            model.Data.reversion_coeff_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            with pytest.raises(FormulaError):
                model.Projection[1].reversion_coeff()
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_two_options_are_never_cumulative(rente_viagere):
    """Compounding two definitive reductions would price an option pair nobody sells."""
    table = rente_viagere.Data.model_point_table()
    assert not ((table["reversion_pct"] > 0) & (table["guarantee_years"] > 0)).any()
    for point_id in table.index:
        assert rente_viagere.Projection[point_id].check_options_xor() is True


# ---------------------------------------------------------------------------
# Pitfall 10: modelling a surrender


def test_there_is_no_surrender_machinery_anywhere(rente_viagere):
    """No surrender value at any duration, no lapse, no paid-up - a cited product feature."""
    names = set(rente_viagere.Projection.cells) | set(rente_viagere.Projection.refs)
    for absent in ("lapse_rate", "lapse_rate_mth", "lapse_rate_ann", "pols_lapse",
                   "surr_charge_rate", "surr_value", "dyn_lapse_factor", "av_pp_at",
                   "av_at", "cv_pp", "asset_share", "prem_to_av_pp", "withdrawals",
                   "claims_surr", "claims_wd", "paid_up_factor"):
        assert absent not in names
    df = rente_viagere.Projection[1].result_cf()
    assert "claims_surr" not in df.columns and "withdrawals" not in df.columns


def test_the_commutation_threshold_is_an_admission_test(rente_viagere):
    """check_commutation_floor rejects a point rather than projecting a small answer."""
    for point_id in rente_viagere.Data.model_point_table().index:
        assert rente_viagere.Projection[point_id].check_commutation_floor() is True
    # The smallest shipped quittance still clears EUR 110 a month comfortably.
    small = rente_viagere.Projection[8]
    assert small.annual_income_init() / 12 == pytest.approx(247.50, abs=CENT)
    # Raise the threshold above it and the point is refused, not truncated.
    model = mx.read_model(MODEL_DIR, name="Rente_FR_S_commut")
    try:
        model.Projection.commutation_floor = 1000.0
        model.Projection.clear_all()
        assert model.Projection[8].check_commutation_floor() is False
        assert model.Projection[8].result_cf()["liability_cf"].sum() > 0.0
    finally:
        model.close()
    # At a quarterly frequency the threshold scales with the payment period.
    quarterly = rente_viagere.Projection[6]
    assert quarterly.payment_freq() == 4
    assert quarterly.annual_income_init() / 4 > 110.0 * 3
    # The rule reaches the reversion annuity too: at a 20% taux de reversion the
    # survivor's quittance would be 0.20 x 429.043038 = 85.81, below the threshold.
    p = rente_viagere.Projection[1]
    assert 0.20 * p.prorata_pp(25) == pytest.approx(85.81, abs=CENT)
    assert 0.20 * p.prorata_pp(25) < p.commutation_floor
    assert p.reversion_pct() * p.prorata_pp(25) > p.commutation_floor


# ---------------------------------------------------------------------------
# Pitfalls 11 and 12: the two charges


def test_the_frais_sur_encours_never_touch_an_instalment(rente_viagere):
    """They bite on the provision mathematique and reduce the profit-sharing base.

    Subtracting them from an instalment cuts the annuitant's income, which no retrieved
    contract does - so the model carries no such rate at all, and the annuity in force is
    A0 R Pi with nothing netted.
    """
    names = set(rente_viagere.Projection.cells) | set(rente_viagere.Projection.refs)
    for absent in ("encours_charge_rate", "fund_charge_rate", "mgmt_charge_rate"):
        assert absent not in names
    p = rente_viagere.Projection[1]
    for t in (0, 9, 21, 199):
        assert p.annual_income(t) == pytest.approx(
            p.annual_income_init() * p.revalo_factor(t) * p.palier_factor(t),
            rel=1e-15)
        assert p.annuity_pp(t) * 12 == pytest.approx(p.annual_income(t), rel=1e-15)


def test_the_frais_darrerages_are_charged_per_quittance(rente_viagere):
    """f x every payment, including the prorata settled on death - not on the annualised rente."""
    p = rente_viagere.Projection[1]
    assert p.arrerage_charge_rate() == 0.03
    for t in (0, 9, 25, 26):
        assert p.arrerage_charges(t) == pytest.approx(
            0.03 * (p.annuity_payments(t) + p.claims(t, "PRORATA")), rel=1e-14)
    assert p.arrerage_charges(25) == pytest.approx(0.03 * 429.043038, abs=1e-4)
    # At a flat percentage the frequency does not change the total charge over a year.
    q = rente_viagere.Projection[6]
    year = sum(q.arrerage_charges(t) for t in range(12))
    assert year == pytest.approx(
        0.03 * sum(q.annuity_payments(t) + q.claims(t, "PRORATA")
                   for t in range(12)), rel=1e-14)
    # A carrier that charges nothing is a shipped configuration, not a special case.
    free = rente_viagere.Projection[5]
    assert free.arrerage_charge_rate() == 0.0
    assert all(free.arrerage_charges(t) == 0.0 for t in (0, 49, 299))


# ---------------------------------------------------------------------------
# Pitfall 13: discounting at the taux technique


def test_the_taux_technique_reaches_no_cash_flow(rente_viagere):
    """i prices the annuity through rho and appears in no recursion at all.

    Reusing it as a discount rate produces neither a price nor a reserve: the best
    estimate discounts at the risk-free term structure, which this library does not
    compute.
    """
    proj = rente_viagere.Projection
    users = {c for c in proj.cells
             if "technical_rate" in (proj.cells[c].formula.source or "")}
    assert users == {"technical_rate", "annuity_factor", "certain_excess_years"}
    # Nothing in the model discounts: liability_cf is a gross undiscounted flow.
    p = rente_viagere.Projection[11]
    assert p.technical_rate() == 0.01
    assert p.liability_cf(0) == pytest.approx(
        p.annuity_payments(0) + p.claims(0) - p.arrerage_charges(0) + p.expenses(0),
        rel=1e-15)
    # A non-zero i raises the rate the tariff implies, and the model point carries it.
    assert p.taux_rente_tariff() > rente_viagere.Projection[7].taux_rente_tariff()
    assert p.check_taux_rente() is True


# ---------------------------------------------------------------------------
# Pitfall 14: a palier step reaching the reversion stream


def test_a_palier_never_reaches_the_reversion_stream(rente_viagere):
    """The options are mutually exclusive, so no shipped point can combine them."""
    table = rente_viagere.Data.model_point_table()
    stepped = table["palier_scheme"] != "none"
    assert not (stepped & (table["reversion_pct"] > 0)).any()
    for point_id in table.index:
        p = rente_viagere.Projection[point_id]
        if p.palier_scheme() != "none":
            assert p.reversion_pct() == 0.0
            assert all(p.reversion_factor(t) == 0.0 for t in (0, 99, 299))
    # The four published schemes, as steps of duration rather than escalation: the first
    # step runs months 0..59 at S = 5, so month 60 is the first at the second level.
    inc2 = rente_viagere.Projection[7]
    assert inc2.palier_scheme() == "inc2" and inc2.palier_step_years() == 5
    assert [inc2.palier_factor(t) for t in (59, 60, 119, 120)] == [1.0, 1.25, 1.25, 1.5]
    dec1 = rente_viagere.Projection[8]
    assert dec1.palier_scheme() == "dec1" and dec1.palier_step_years() == 10
    assert [dec1.palier_factor(t) for t in (119, 120)] == [1.0, 0.5]
    dec2 = rente_viagere.Projection[5]
    assert [dec2.palier_factor(t) for t in (59, 60, 119, 120)] == [1.0, 0.75, 0.75, 0.5]
    inc1 = rente_viagere.Projection[10]
    assert [inc1.palier_factor(t) for t in (119, 120)] == [1.0, 2.0]
    # A step multiplies the initial level; it does not compound with revalorisation.
    assert inc2.annual_income(120) == pytest.approx(
        inc2.annual_income_init() * inc2.revalo_factor(120) * 1.5, rel=1e-15)
    # And no scheme means a flat multiplier of one, at every month.
    level = rente_viagere.Projection[1]
    assert all(level.palier_factor(t) == 1.0 for t in (0, 99, 699))


# ---------------------------------------------------------------------------
# Timing, horizon and the recursions


def test_advance_timing_measures_survival_at_the_start_of_the_month(rente_viagere):
    """Terme a echoir is unobserved in France and is retained as a model variant only."""
    p = rente_viagere.Projection[11]
    assert p.payment_timing() == "advance"
    assert p.payment_surv_mth(0) == 0
    # Advance: survival is measured at the start of month t, which is time t.
    assert all(p.payment_surv_mth(t) == t for t in (0, 1, 59))
    assert p.payment_factor(0) == 1.0                # the first instalment is certain
    assert p.payment_factor(59) == pytest.approx(p.lives_if(59, 1), rel=1e-14)
    # Nothing has accrued unpaid at death, so there is no prorata to settle [std].
    assert all(p.prorata_pp(t) == 0.0 for t in (0, 25, 299))
    assert all(p.claims(t, "PRORATA") == 0.0 for t in (0, 25, 299))


def test_the_projection_stops_on_the_youngest_covered_life(rente_viagere):
    """Stopping on the annuitant alone would truncate a younger reversionary's tail."""
    joint = rente_viagere.Projection[1]
    assert joint.horizon_mths() == 12 * (120 - 61)      # the reversionary is younger
    assert joint.proj_len() == 708                      # months projected, t = 0..707
    assert joint.age(joint.proj_len() - 1, 2) == 119    # the last month below omega
    single = rente_viagere.Projection[5]
    assert single.proj_len() == 12 * (120 - 70)
    # A guarantee is never longer than the mortality horizon here, but the max is taken.
    assert rente_viagere.Projection[3].proj_len() == max(12 * (120 - 65), 180)


def test_the_survival_recursion_closes(rente_viagere):
    """Rebuilt from the annual table form, not from the telescoping density definition."""
    for point_id in rente_viagere.Data.model_point_table().index:
        assert rente_viagere.Projection[point_id].check_lives_roll_fwd() is True, point_id


def test_the_cumulative_schedule_closes(rente_viagere):
    """Rebuilt as a direct sum over payment months, with no reference to the recursion."""
    for point_id in rente_viagere.Data.model_point_table().index:
        p = rente_viagere.Projection[point_id]
        assert p.check_cum_annuity_roll_fwd() is True, point_id
    p = rente_viagere.Projection[1]
    assert p.cum_annuity_pp(25, "ANNUITANT") == pytest.approx(10979.65, abs=CENT)
    with pytest.raises(FormulaError):
        p.cum_annuity_pp(4, "REVERSION")


def test_every_check_holds_on_every_model_point(rente_viagere):
    """The whole check_* family, on every shipped configuration."""
    checks = [c for c in rente_viagere.Projection.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    assert len(checks) >= 7
    for point_id in rente_viagere.Data.model_point_table().index:
        p = rente_viagere.Projection[point_id]
        for name in checks:
            value = getattr(p, name)()
            assert isinstance(value, bool), (point_id, name)
            assert value is True, (point_id, name)


def test_the_monthly_mortality_rate_is_below_the_annual_one(rente_viagere):
    """q_m = 1 - (1 - q)^(1/12), the uniform-force reading of an annual table."""
    p = rente_viagere.Projection[2]
    for t in (0, 12, 299):
        annual, monthly = p.mort_rate(t, 1), p.mort_rate_mth(t, 1)
        assert 0.0 < monthly < annual
        assert monthly == pytest.approx(1 - (1 - annual) ** (1 / 12), rel=1e-14)


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(fr_rente_anchor):
    df = fr_rente_anchor.result_cf()
    # The frame is 0-based and proj_len() is the number of months projected.
    assert list(df.index) == list(range(708))
    assert list(df.index) == list(range(fr_rente_anchor.proj_len()))
    assert df.index[0] == 0 and df.index[-1] == fr_rente_anchor.proj_len() - 1
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "annuity_payments", "claims_prorata", "arrerage_charges",
        "expenses", "liability_cf", "net_cf",
    ]
    # A cash flow statement must not publish its own subtotal beside its parts.
    assert "claims" not in df.columns


def test_both_signs_of_the_net_flow_are_published(fr_rente_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign.

    The frais d'arrerages are the one component that runs the other way: the insurer
    retains them, so the column is positive and the charge is subtracted.
    """
    p = fr_rente_anchor
    df = p.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    outgo = (df["annuity_payments"] + df["claims_prorata"] - df["arrerage_charges"]
             + df["expenses"])
    assert (outgo - df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert (df["arrerage_charges"] >= 0).all()


def test_there_is_no_premium_income(fr_rente_anchor):
    """The capital constitutif is priced at the outset, not a projected cash flow."""
    p = fr_rente_anchor
    assert "premiums" not in p.result_cf().columns
    assert p.purchase_price() == 200000.0
    assert all(p.net_cf(t) <= 0.0 for t in (0, 9, 25, 99))


def test_pols_if_is_the_obligation_indicator_not_a_policy_count(fr_rente_anchor):
    """IF(t): the guarantee certain, the annuitant alive, or the reversion in payment."""
    p = fr_rente_anchor
    assert p.pols_if(0) == 1.0                    # annuitant alive
    assert p.pols_if(26) == 1.0                   # reversion stream in payment
    assert p.pols_if(25) == 0.0                   # the documented one-month gap
    assert p.expenses(26) == pytest.approx(
        30.0 / 12 * 1.015 ** p.cal_year_index(26) * p.pols_if(26), rel=1e-12)
    assert p.expenses(25) == 0.0
    assert all(p.pols_if(t) <= 1.0 for t in range(200))


def test_expense_inflation_steps_at_31_december_without_a_pro_rata(fr_rente_anchor):
    """(1 + pi)^k(t): the calendar turns, and an expense base is not a rente in service."""
    p = fr_rente_anchor
    assert p.inflation_factor(8) == 1.0
    assert p.inflation_factor(9) == pytest.approx(1.015, rel=1e-15)
    assert p.inflation_factor(21) == pytest.approx(1.015 ** 2, rel=1e-15)
    # The revalorisation index is pro-rated in the first year; this is not.
    assert p.revalo_factor(9) < p.inflation_factor(9)


def test_invalid_enum_values_raise(fr_rente_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_rente_anchor.claims(0, "CAPITAL")
    with pytest.raises(FormulaError):
        fr_rente_anchor.cum_annuity_pp(0, "BOTH")
    with pytest.raises(FormulaError):
        fr_rente_anchor.sex(3)
    with pytest.raises(FormulaError):
        fr_rente_anchor.mort_rate_at_age("X", 1961, 65)
    # There are two covered lives at most, and nothing else answers to a life index.
    with pytest.raises(FormulaError):
        fr_rente_anchor.age_at_entry(3)
    with pytest.raises(FormulaError):
        fr_rente_anchor.birth_year(0)


def test_a_single_life_point_has_no_reversion_stream(rente_viagere):
    p = rente_viagere.Projection[5]
    assert p.reversion_pct() == 0.0
    assert all(p.reversion_factor(t) == 0.0 for t in (0, 59, 299))
    assert p.lives_if(60, 2) == 0.0
    with pytest.raises(FormulaError):
        p.age_at_entry(2)


def test_model_docstring_describes_the_current_structure(rente_viagere):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = rente_viagere.doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "generational" in doc
    assert "unisex" in doc
    assert "revalorisation" in doc
    assert "PA_UK_S" in doc                      # the chassis it shares
    assert "Data" in doc and "Projection" in doc


def test_space_docstrings_carry_their_reference_material(rente_viagere):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = rente_viagere.Projection.doc
    assert "Notes symbol" in proj
    assert "proj_len" in proj and "model_point" in proj
    for cells in ("lives_if", "tariff_lives", "payment_factor", "reversion_factor",
                  "cum_annuity_pp", "guarantee_coeff", "reversion_coeff", "mort_basis",
                  "revalo_factor", "palier_factor"):
        assert cells in proj
    data = rente_viagere.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table",
                  "reversion_coeff_table"):
        assert cells in data


def test_cells_names_follow_the_payout_chassis(rente_viagere):
    """Names shared with PA_UK_S and SPIA_US_S must mean the same thing in all three."""
    shared = {
        "model_point", "proj_len", "age", "age_at_entry", "pols_if", "pols_if_init",
        "mort_rate", "mort_rate_mth", "lives_if", "lives_death", "certain_floor",
        "payment_factor", "payment_factor_life", "payment_surv_mth", "is_payment_mth",
        "annual_income", "annuity_pp", "annuity_payments", "cum_annuity_pp",
        "claims", "expenses",
        "expense_maint", "inflation_rate", "inflation_factor", "liability_cf", "net_cf",
        "result_cf", "omega_age", "policy_year", "duration", "duration_mth",
        "calendar_year", "horizon_mths", "purchase_price", "payment_freq",
        "payment_timing", "mort_basis", "death_mth", "mths_since_payment",
    }
    names = set(rente_viagere.Projection.cells) | set(rente_viagere.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """Three CSVs: the model points, the generational table, the [S6] coefficient table."""
    expected = {"model_point_table.csv", "mort_table.csv", "reversion_coeff_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}
    assert {p.name for p in MODEL_DIR.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """A generational proxy, and the file says so - it is not TGH05/TGF05."""
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert set(table["provenance"]) == {"[std] INSEE-shaped generational proxy"}
    assert list(table.columns) == ["sex", "birth_year", "age", "mort_rate", "provenance"]
    assert table["mort_rate"].max() <= 1.0
    assert set(table["sex"]) == {"M", "F"}
    assert table["birth_year"].min() == 1940 and table["birth_year"].max() == 1980
    assert table["age"].min() == 50 and table["age"].max() == 120
    top = table[table["age"] == 120]
    assert (top["mort_rate"] == 1.0).all()
    # Male mortality is above female at every age and millesime shipped.
    male = table[table["sex"] == "M"].set_index(["birth_year", "age"])["mort_rate"]
    female = table[table["sex"] == "F"].set_index(["birth_year", "age"])["mort_rate"]
    assert (male >= female).all()


def test_the_reversion_coefficient_table_marks_its_own_provenance():
    """The only published option-cost table in the sources, adopted [std]."""
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "reversion_coeff_table.csv")
    assert set(table["reversion_pct"]) == {0.60, 0.80, 1.00}
    assert len(table) == 33
    assert set(table["provenance"]) == {
        "[S6 Art. 5.4.3] published coefficient; adoption [std]"}
    # A coefficient falls as the reversionary gets younger and as delta rises.
    sixty = table[table["reversion_pct"] == 0.60].sort_values("gen_diff_lo")
    assert list(sixty["reversion_coeff"]) == sorted(
        sixty["reversion_coeff"], reverse=True)
    band = table[(table["gen_diff_lo"] == 4)].set_index("reversion_pct")
    assert band.loc[0.60, "reversion_coeff"] > band.loc[1.00, "reversion_coeff"]


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a licensed TGH05/TGF05 file."""
    import pandas as pd

    src = MODEL_DIR.parent / "mort_table.csv"
    lighter = pd.read_csv(src, index_col=["sex", "birth_year", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="Rente_FR_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[2].result_cf()["liability_cf"].sum()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Lighter mortality lengthens every annuity stream, so the liability rises,
            # and the tariff the same table implies falls.  No formula changed.
            assert model.Projection[2].result_cf()["liability_cf"].sum() > base
            assert model.Projection[2].taux_rente_tariff() < 0.0330
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_every_model_point_projects(rente_viagere):
    """A point the shipped tables cannot serve is a defect, not a configuration."""
    columns = None
    for point_id in rente_viagere.Data.model_point_table().index:
        df = rente_viagere.Projection[point_id].result_cf()
        assert len(df) > 0
        assert df.notna().all().all()
        assert df["net_cf"].sum() < 0.0
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Rente_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Rente_FR_S_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            paid = p.annuity_payments(t) + p.claims(t, "PRORATA")
            assert paid == pytest.approx(row[1], abs=CENT)
            assert p.arrerage_charges(t) == pytest.approx(row[2], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
