"""Golden and structural tests for ADE_FR_S.

The golden values are the worked example in
products/assurance_emprunteur/technical-notes.md ("Worked example"): the base cell — male
aged 52, EUR 200 000 borrowed at a 3.00 % *taux nominal* over 240 months, *quotité* 1.00,
a level 0.84 % premium on the *capital initial*, *forfaitaire* indemnity, a 90-day
*franchise*, the 1 095-day ITT cap, IPT paid as the *échéance*, and cover to ages 85 / 70
/ 70 — run from issue for fifteen months.  Model point 1 is that cell.  The notes also
give a supplementary table following one ITT cohort through the cap, and present values
over the whole 240 months at a flat 2.5 %; both are asserted here.

They are hard-coded rather than pickled so that a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent,
state probabilities to six decimals.

The time index is the library-wide **0-based** policy month: ``t = 0`` is the contract's
first month and ``result_cf()`` runs ``t = 0 ... proj_len() - 1``, so the notes' fifteen
rows are ``t = 0 ... 14``.  Two indices here are not that clock and do not move with it:
``crd(k)`` is a time point with ``k = 0`` at adhesion, so month ``t`` closes on
``crd(t + 1)``, and ``z`` is the claim duration, running 1 to 36 from the start of claim
payment.

Beyond the worked example this module asserts, one test each, the nine modeling
pitfalls the notes name - each a way an implementation can look right and be wrong.
Every test is named for the failure it catches.

Model points 2 to 12 carry the variants: the second premium basis, the *indemnitaire*
indemnity, the ``crd`` IPT basis, a *quotité* of 0.60, the *franchise* menu, a cell whose
ITT/IPT cover ends 180 months before its loan, and one claim in payment in each of the
two disabled states.
"""
import shutil

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
STATE = 5e-7          # state probabilities to 6 d.p.
RATE = 5e-10          # monthly rates displayed to 9 d.p.

MODEL_DIR = LIB / MODELS["ADE_FR_S"][0]

# t: (crd, l_h, l_itt, l_ipt, prem, ben_deces, ben_ptia, ben_itt, ben_ipt)
#
# ``t`` is the 0-based policy month, so the notes' first row is t = 0.  The state columns
# are the notes' END-of-month quantities - the state at time t + 1 - so they are read off
# pols_healthy_close / pols_itt_close / pols_ipt_close, and the CRD column is likewise the
# balance at the end of the month, crd(t + 1) on the loan's own time-point index.  The
# cash flows are the flows of month t.
WORKED_EXAMPLE = {
    0: (199390.80, 0.995344, 0.000901, 0.000000, 140.00, 65.25, 6.51, 0.00, 0.00),
    1: (198780.09, 0.990768, 0.001737, 0.000001, 139.35, 65.03, 6.46, 0.93, 0.00),
    2: (198167.84, 0.986267, 0.002513, 0.000004, 138.71, 64.79, 6.41, 1.80, 0.00),
    3: (197554.07, 0.981837, 0.003232, 0.000008, 138.08, 64.54, 6.36, 2.60, 0.01),
    4: (196938.76, 0.977474, 0.003898, 0.000013, 137.46, 64.28, 6.32, 3.34, 0.01),
    5: (196321.91, 0.973174, 0.004516, 0.000019, 136.85, 64.01, 6.27, 4.03, 0.02),
    6: (195703.52, 0.968933, 0.005088, 0.000026, 136.24, 63.72, 6.22, 4.67, 0.03),
    7: (195083.58, 0.964750, 0.005617, 0.000034, 135.65, 63.42, 6.17, 5.26, 0.04),
    8: (194462.09, 0.960620, 0.006107, 0.000043, 135.06, 63.12, 6.13, 5.81, 0.05),
    9: (193839.05, 0.956540, 0.006561, 0.000053, 134.49, 62.81, 6.08, 6.32, 0.06),
    10: (193214.46, 0.952509, 0.006980, 0.000063, 133.92, 62.48, 6.04, 6.79, 0.07),
    11: (192588.30, 0.948524, 0.007367, 0.000074, 133.35, 62.16, 5.99, 7.22, 0.08),
    12: (191960.57, 0.937659, 0.007789, 0.000085, 132.79, 67.31, 6.49, 7.62, 0.09),
    13: (191331.28, 0.926937, 0.008184, 0.000099, 131.27, 66.54, 6.40, 8.07, 0.11),
    14: (190700.41, 0.916356, 0.008553, 0.000114, 129.77, 65.77, 6.30, 8.49, 0.13),
}

# The notes' column sums over t = 0..14.
WORKED_EXAMPLE_SUMS = {
    "premiums": 2032.99,
    "DEATH": 965.23,
    "PTIA": 94.16,
    "ITT": 72.95,
    "IPT": 0.71,
    "expenses": 38.10,
}

# The notes' derived constants at attained age 52, policy years 1 and 2.
ECHEANCE = 1109.1951957
PREM_PP = 140.00
Q_H_52 = 0.000327255
Q_PTIA_52 = 0.000032673
IOTA_52 = 0.000904486
W_YEAR1 = 0.003396053
W_YEAR2 = 0.010596241
Q_H_53 = 0.000357368
IOTA_53 = 0.000980268
RHO_1 = 0.064376669
TAU_1 = 0.001682143
Q_S_1 = 0.001682143
S_ITT_1 = 0.932478274

# The notes' supplementary table: z -> (rho, tau, q_s, s_itt, S(z)).
ITT_COHORT = {
    1: (0.064377, 0.001682, 0.001682, 0.932478, 0.932478),
    6: (0.064377, 0.001682, 0.001682, 0.932478, 0.657404),
    12: (0.064377, 0.001682, 0.001682, 0.932478, 0.432180),
    13: (0.029286, 0.005143, 0.002535, 0.963274, 0.416308),
    24: (0.029286, 0.005143, 0.002535, 0.963274, 0.275843),
    25: (0.013452, 0.010596, 0.003396, 0.972779, 0.268335),
    35: (0.013452, 0.010596, 0.003396, 0.972779, 0.203620),
    36: (0.013452, 0.010596, 0.003396, 0.972779, 0.198077),
}
ITT_ANNUITY_MONTHS = 14.721231
ITT_BENEFIT_PER_INCEPTION = 16328.72

# The notes' aggregates over the full 240 months, discounted at a flat 2.5 %.
PV_PREMIUMS = 12602.19
PV_PREMIUMS_CRD_BASIS = 12588.82
PV = {"DEATH": 7170.56, "PTIA": 635.87, "ITT": 1932.71, "IPT": 1293.18}
PV_EXPENSES = 334.17
PV_OUTGO = 11366.49


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_ade_anchor, t):
    """Every cell of the notes' fifteen-month table, to the displayed precision."""
    crd, l_h, l_itt, l_ipt, prem, dec, ptia, itt, ipt = WORKED_EXAMPLE[t]
    p = fr_ade_anchor
    assert p.crd(t + 1) == pytest.approx(crd, abs=CENT)
    assert p.pols_healthy_close(t) == pytest.approx(l_h, abs=STATE)
    assert p.pols_itt_close(t) == pytest.approx(l_itt, abs=STATE)
    assert p.pols_ipt_close(t) == pytest.approx(l_ipt, abs=STATE)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(dec, abs=CENT)
    assert p.claims(t, "PTIA") == pytest.approx(ptia, abs=CENT)
    assert p.claims(t, "ITT") == pytest.approx(itt, abs=CENT)
    assert p.claims(t, "IPT") == pytest.approx(ipt, abs=CENT)


def test_worked_example_column_sums(fr_ade_anchor):
    """The notes' totals over the fifteen months, including expenses."""
    p = fr_ade_anchor
    ts = range(15)
    assert sum(p.premiums(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_SUMS["premiums"], abs=CENT)
    for kind in ("DEATH", "PTIA", "ITT", "IPT"):
        assert sum(p.claims(t, kind) for t in ts) == pytest.approx(
            WORKED_EXAMPLE_SUMS[kind], abs=CENT)
    assert sum(p.expenses(t) for t in ts) == pytest.approx(
        WORKED_EXAMPLE_SUMS["expenses"], abs=CENT)


def test_worked_example_derived_constants(fr_ade_anchor):
    """The *échéance*, the premium, and the eight monthly rates the notes tabulate."""
    p = fr_ade_anchor
    assert p.echeance() == pytest.approx(ECHEANCE, abs=5e-8)
    assert p.prem_pp(0) == pytest.approx(PREM_PP, rel=1e-14)
    # Annual rates, read off the [std] pivot tables by linear interpolation at age 52.
    assert p.mort_rate(0) == pytest.approx(0.00392, rel=1e-12)
    assert p.ptia_rate(0) == pytest.approx(0.000392, rel=1e-12)
    assert p.itt_inception_rate(0) == pytest.approx(0.0108, rel=1e-12)
    assert p.lapse_rate(0) == 0.04 and p.lapse_rate(12) == 0.12
    # Monthly, all through 1 - (1 - r)^(1/12).
    assert p.mort_rate_mth(0) == pytest.approx(Q_H_52, abs=RATE)
    assert p.ptia_rate_mth(0) == pytest.approx(Q_PTIA_52, abs=RATE)
    assert p.itt_inception_rate_mth(0) == pytest.approx(IOTA_52, abs=RATE)
    assert p.lapse_rate_mth(0) == pytest.approx(W_YEAR1, abs=RATE)
    assert p.lapse_rate_mth(12) == pytest.approx(W_YEAR2, abs=RATE)
    # The mortality step at the first anniversary, which shows in ben_deces at t = 12.
    assert p.age(11) == 52 and p.age(12) == 53
    assert p.mort_rate(12) == pytest.approx(0.00428, rel=1e-12)
    assert p.mort_rate_mth(12) == pytest.approx(Q_H_53, abs=RATE)
    assert p.itt_inception_rate_mth(12) == pytest.approx(IOTA_53, abs=RATE)
    # Duration-year-1 ITT terminations.
    assert p.itt_recovery_rate_mth(1) == pytest.approx(RHO_1, abs=RATE)
    assert p.itt_to_ipt_rate_mth(1) == pytest.approx(TAU_1, abs=RATE)
    assert p.itt_mort_rate_mth(1) == pytest.approx(Q_S_1, abs=RATE)
    assert p.itt_surv_step(1) == pytest.approx(S_ITT_1, abs=RATE)


def test_the_first_month_decomposes_into_its_four_decrements(fr_ade_anchor):
    """l_h(1) is the product of the four survival factors, and the exits add back to 1.

    The notes' ``l_h(1)`` is the state at time 1, i.e. at the end of month ``t = 0``.
    Pins the **order** out of ``healthy``: death, PTIA, *résiliation*, inception.
    """
    p = fr_ade_anchor
    product = ((1 - Q_H_52) * (1 - Q_PTIA_52) * (1 - W_YEAR1) * (1 - IOTA_52))
    assert p.pols_healthy_close(0) == pytest.approx(product, abs=STATE)
    assert p.pols_death_healthy(0) == pytest.approx(0.000327255, abs=RATE)
    assert p.pols_ptia(0) == pytest.approx(0.000032662, abs=RATE)
    assert p.pols_lapse(0) == pytest.approx(0.003394831, abs=RATE)
    assert p.pols_itt_inception(0) == pytest.approx(0.000901090, abs=RATE)
    exits = (p.pols_death_healthy(0) + p.pols_ptia(0) + p.pols_lapse(0)
             + p.pols_itt_inception(0))
    assert p.pols_healthy_close(0) + exits == pytest.approx(1.0, abs=1e-12)
    # Each exit is smaller than its own rate, because the ones before it went first.
    assert p.pols_ptia(0) < Q_PTIA_52
    assert p.pols_itt_inception(0) < IOTA_52


def test_the_ordering_is_visible_in_the_ptia_to_death_ratio(fr_ade_anchor):
    """ben_ptia(0) / ben_deces(0) is 0.0998, not the ptia_ratio of 0.10.

    The difference is the month of death exposure that precedes PTIA in the order;
    taking the two decrements in parallel would print 0.1000.
    """
    p = fr_ade_anchor
    assert p.claims(0, "DEATH") == pytest.approx(65.251648, abs=CENT)
    assert p.claims(0, "PTIA") == pytest.approx(6.512472, abs=CENT)
    ratio = p.claims(0, "PTIA") / p.claims(0, "DEATH")
    assert ratio == pytest.approx(0.0998, abs=5e-5)
    assert ratio < p.ptia_ratio


def test_the_state_identity_closes_over_the_worked_example_window(fr_ade_anchor):
    """0.925024 in force plus 0.074976 of exits is exactly 1 after fifteen months."""
    p = fr_ade_anchor
    in_force = (p.pols_healthy_close(14) + p.pols_itt_close(14)
                + p.pols_ipt_close(14))
    exits = sum(p.pols_exit(t) for t in range(15))
    assert in_force == pytest.approx(0.925024, abs=STATE)
    assert exits == pytest.approx(0.074976, abs=STATE)
    assert in_force + exits == pytest.approx(1.0, abs=1e-12)


def test_the_lapse_step_at_the_first_anniversary(fr_ade_anchor):
    """l_h falls 0.4598 % a month in year 1 and 1.1455 % in year 2.

    The loi Lemoine substitution assumption arriving: 4 % to 12 % a year, diluted by
    the unchanged mortality and inception decrements.
    """
    p = fr_ade_anchor
    year1 = 1 - p.pols_healthy_close(1) / p.pols_healthy_close(0)
    year2 = 1 - p.pols_healthy_close(12) / p.pols_healthy_close(11)
    assert year1 == pytest.approx(0.004598, abs=5e-7)
    assert year2 == pytest.approx(0.011455, abs=5e-7)
    assert p.lapse_rate_mth(12) / p.lapse_rate_mth(0) == pytest.approx(3.12, abs=5e-3)


# ---------------------------------------------------------------------------
# The loan spine


def test_the_crd_is_computed_and_the_amortisation_closes(fr_ade_anchor):
    """The notes' first pitfall: a CRD read from a table cannot be checked.

    The annuity form against the roll-forward, ``crd(240) = 0``, and the interest.
    """
    p = fr_ade_anchor
    assert p.check_crd() is True
    assert p.crd(0) == 200000.0
    assert p.crd(1) == pytest.approx(199390.8048, abs=1e-4)
    assert p.crd(1) == pytest.approx(200000 * 1.0025 - p.echeance(), rel=1e-14)
    assert p.crd(239) == pytest.approx(1106.4291, abs=1e-4)
    assert p.crd(239) * 1.0025 == pytest.approx(p.echeance(), rel=1e-12)
    assert p.crd(240) == 0.0
    assert 240 * p.echeance() == pytest.approx(266206.85, abs=CENT)
    assert p.loan_interest_total() == pytest.approx(66206.85, abs=CENT)
    # The residual of month t carries crd(t) to crd(t + 1), so the frame's own months
    # 0 .. 239 cover all 240 instalments.
    for t in (0, 119, 238, 239):
        assert p.check_crd_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_the_monthly_loan_rate_is_nominal_over_twelve(fr_ade_anchor):
    """A French loan quotes a *taux nominal annuel*: i = nominal / 12.

    Using the effective conversion ``(1 + nominal)^(1/12) - 1`` instead moves the
    *échéance*, and therefore every benefit and the TAEA.  This is also the one rate in
    the model that is **not** converted with ``1 - (1 - r)^(1/12)`` — that rule is for
    decrements, and a loan is not a decrement.
    """
    p = fr_ade_anchor
    assert p.loan_rate_annual() == 0.03
    assert p.loan_rate_mth() == pytest.approx(0.0025, rel=1e-14)
    effective = 1.03 ** (1 / 12) - 1
    assert p.loan_rate_mth() != pytest.approx(effective, rel=1e-4)
    wrong = 200000 * effective / (1 - (1 + effective) ** -240)
    assert wrong == pytest.approx(1105.15, abs=CENT)
    assert p.echeance() - wrong == pytest.approx(4.05, abs=0.01)
    # EUR 4.05 a month is EUR 971 over the loan, and every ITT and IPT benefit,
    # which is written on the echeance, moves with it.
    assert 240 * (p.echeance() - wrong) > 970.0


def test_the_two_crd_conventions_differ_by_the_month_repayment(fr_ade_anchor):
    """Month 0 opens on crd(0) and closes on crd(1), EUR 609.20 apart.

    ``crd`` is a time-point cells: the benefit of month t is written on the **closing**
    balance ``crd(t + 1)``, and whichever convention is chosen must be used everywhere.
    """
    p = fr_ade_anchor
    assert p.crd(0) - p.crd(1) == pytest.approx(609.20, abs=CENT)
    expected = p.crd(1) * p.quotite() * p.pols_death_healthy(0)
    assert p.claims(0, "DEATH") == pytest.approx(expected, rel=1e-14)
    assert p.benefit_deces_pp(0) == pytest.approx(p.crd(1) * p.quotite(), rel=1e-14)


# ---------------------------------------------------------------------------
# The ITT duration dimension and the 1 095-day cap


@pytest.mark.parametrize("z", sorted(ITT_COHORT))
def test_itt_cohort_survival_row(fr_ade_anchor, z):
    """The notes' supplementary table: one ITT cohort through the 1 095-day cap."""
    rho, tau, q_s, step, surv = ITT_COHORT[z]
    p = fr_ade_anchor
    assert p.itt_recovery_rate_mth(z) == pytest.approx(rho, abs=STATE)
    assert p.itt_to_ipt_rate_mth(z) == pytest.approx(tau, abs=STATE)
    assert p.itt_mort_rate_mth(z) == pytest.approx(q_s, abs=STATE)
    assert p.itt_surv_step(z) == pytest.approx(step, abs=STATE)
    assert p.itt_surv(z) == pytest.approx(surv, abs=STATE)


def test_the_recovery_rate_falls_and_the_ipt_transition_rises(fr_ade_anchor):
    """0.55 / 0.30 / 0.15 against 0.02 / 0.06 / 0.12 by duration year.

    Short claims mostly recover and long claims mostly consolidate; that gradient is
    why the in-claim population needs a duration dimension at all.
    """
    p = fr_ade_anchor
    assert [p.itt_recovery_rate(z) for z in (1, 13, 25, 36)] == [0.55, 0.30, 0.15, 0.15]
    assert [p.itt_to_ipt_rate(z) for z in (1, 13, 25, 36)] == [0.02, 0.06, 0.12, 0.12]
    assert [p.itt_mort_rate(z) for z in (1, 13, 25, 36)] == [0.02, 0.03, 0.04, 0.04]
    assert p.claim_dur_year(12) == 1 and p.claim_dur_year(13) == 2
    assert p.claim_dur_year(24) == 2 and p.claim_dur_year(25) == 3
    # Beyond the table the last row is held, which is the year the cap falls in.
    assert p.claim_dur_year(1000) == 3


def test_collapsing_the_duration_dimension_would_misstate_the_runoff(fr_ade_anchor):
    """A single bucket at the year-one rate runs a claim off far faster than the cohorts.

    At three years the duration-aware survival is 0.198077 against 0.080722 for a flat
    year-one basis - nearly two and a half times as much mass reaching the cap.
    """
    p = fr_ade_anchor
    cohort = p.itt_surv(36)
    flat = p.itt_surv_step(1) ** 36
    assert cohort == pytest.approx(0.198077, abs=STATE)
    assert flat == pytest.approx(0.080722, abs=STATE)
    assert cohort > 2.4 * flat


def test_the_cap_assesses_the_cohort_instead_of_advancing_it(fr_ade_anchor):
    """At z = 36 the survivors are assessed: 35 % to IPT, 65 % back to ``healthy``.

    If cohort 36 advanced to a cohort 37, ITT claims would run for ever and IPT would
    never be fed from the cap.  The vector is exactly ``itt_max_months()`` long.
    """
    p = fr_ade_anchor
    assert p.itt_max_days() == 1095
    assert p.itt_max_months() == 36
    assert len(p.itt_cohorts(49)) == 36
    assert p.pols_itt_dur(49, 37) == 0.0          # out of range, not an error
    assert p.pols_itt_dur(49, 0) == 0.0
    assert p.itt_surv(36) * p.ipt_share_at_cap == pytest.approx(0.069327, abs=STATE)
    assert p.itt_surv(36) * (1 - p.ipt_share_at_cap) == pytest.approx(
        0.128750, abs=STATE)
    # The cap is actually reached in the projection, and it splits both ways.
    t = 59
    assert p.pols_itt_cap(t) > 0.0
    assert p.pols_cap_to_ipt(t) + p.pols_cap_return(t) == pytest.approx(
        p.pols_itt_cap(t), rel=1e-14)
    assert p.pols_cap_to_ipt(t) == pytest.approx(
        p.ipt_share_at_cap * p.pols_itt_cap(t), rel=1e-14)


def test_the_expected_months_of_itt_payment_per_inception(fr_ade_anchor):
    """Sum of S(z) over the 36 duration months, and what it is worth."""
    p = fr_ade_anchor
    assert p.itt_annuity_months() == pytest.approx(ITT_ANNUITY_MONTHS, abs=5e-7)
    assert p.itt_annuity_months() == pytest.approx(
        sum(p.itt_surv(z) for z in range(1, 37)), rel=1e-14)
    assert p.itt_benefit_per_inception() == pytest.approx(
        ITT_BENEFIT_PER_INCEPTION, abs=CENT)
    assert p.itt_benefit_per_inception() == pytest.approx(
        p.benefit_itt_pp() * p.itt_annuity_months(), rel=1e-14)


def test_the_cohort_vector_and_the_two_dimensional_view_agree(fr_ade_anchor):
    """pols_itt(t) is the sum of pols_itt_dur(t, z) over every tracked duration."""
    p = fr_ade_anchor
    for t in (0, 1, 12, 99, 199):
        by_cohort = sum(p.pols_itt_dur(t, z) for z in range(1, p.itt_max_months() + 1))
        assert p.pols_itt(t) == pytest.approx(by_cohort, rel=1e-12)
    assert p.pols_itt(0) == 0.0                   # a healthy cell starts with no claims
    assert p.pols_itt_dur(1, 1) == pytest.approx(p.pols_itt_inception(0), rel=1e-14)


def test_the_cohort_vector_is_rebuilt_not_mutated(fr_ade_anchor):
    """Each month builds a new list, and the shift is by exactly one cohort.

    A recursion that mutated the previous month's vector would rewrite history; one
    that shifted by the wrong index would leak population.
    """
    p = fr_ade_anchor
    a = p.itt_cohorts(29)
    b = p.itt_cohorts(30)
    assert a is not b
    snapshot = list(a)
    p.itt_cohorts(39)                             # force five more steps
    assert p.itt_cohorts(29) == snapshot          # month 29 was not rewritten
    surv = p.itt_rate_vectors()[3]
    assert b[0] == pytest.approx(p.pols_itt_inception(29), rel=1e-14)
    for z in range(2, p.itt_max_months() + 1):
        assert b[z - 1] == pytest.approx(a[z - 2] * surv[z - 2], rel=1e-14)


def test_a_seeded_claim_starts_at_its_stated_duration(assurance_emprunteur):
    """Model point 9 is an ITT claim already 18 months old, so it enters cohort 19."""
    p = assurance_emprunteur.Projection[9]
    assert p.status() == "itt"
    assert p.claim_duration_months() == 18
    assert p.pols_itt_dur(0, 19) == 1.0
    assert p.pols_itt_dur(0, 1) == 0.0
    assert p.pols_healthy(0) == 0.0
    assert p.claim_dur_year(19) == 2              # duration year 2, recovery down to 0.30
    assert p.itt_recovery_rate(19) == 0.30
    # It is paid from the first month, being already in payment.
    assert p.claims(0, "ITT") > 0.0
    # And it reaches the cap eighteen months later, not thirty-six.
    assert p.pols_itt_cap(17) > 0.0
    assert p.pols_itt_cap(16) == 0.0


def test_an_ipt_cell_is_an_annuity_with_no_recovery(assurance_emprunteur):
    """Model point 10 starts in IPT: the only exits are death and the age limit."""
    p = assurance_emprunteur.Projection[10]
    assert p.status() == "ipt"
    assert p.pols_ipt(0) == 1.0
    assert p.pols_itt(0) == 0.0 and p.pols_healthy(0) == 0.0
    assert p.claims(0, "IPT") == pytest.approx(p.benefit_itt_pp() * p.pols_ipt_stay(0),
                                               rel=1e-14)
    # No recovery from IPT: the population only ever falls, until the cover ends.
    assert all(p.pols_ipt(t + 1) < p.pols_ipt(t) for t in (0, 49, 99, 199))
    assert p.premiums(0) == 0.0                   # premiums are waived in claim
    assert p.check_states() is True


# ---------------------------------------------------------------------------
# The guarantees end at different ages


def test_deces_and_ptia_are_separate_decrements(fr_ade_anchor):
    """They pay the identical capital and end fifteen years apart.

    A collapsed decrement either pays PTIA after 70 or stops paying death before 85.
    """
    p = fr_ade_anchor
    assert p.deces_end_age() == 85 and p.ptia_end_age() == 70
    assert p.benefit_deces_pp(99) == p.crd(100) * p.quotite()
    # PTIA switches off at attained age 70, i.e. from t = 216; death never does here.
    assert p.age(215) == 69 and p.age(216) == 70
    assert p.cover_ptia(215) == 1 and p.cover_ptia(216) == 0
    assert all(p.cover_deces(t) == 1 for t in (0, 215, 216, 239))
    assert p.pols_ptia(215) > 0.0 and p.pols_ptia(216) == 0.0
    assert p.claims(216, "PTIA") == 0.0
    assert p.claims(216, "DEATH") > 0.0
    assert p.pols_death_healthy(239) > 0.0


def test_the_premium_does_not_fall_when_the_cover_ceases(fr_ade_anchor):
    """The rate is *nivelé*: 24 months x EUR 140.00 against death cover alone.

    The mirror error is letting the ITT or IPT benefit run past the age limit.
    """
    p = fr_ade_anchor
    assert p.cover_itt(215) == 1 and p.cover_itt(216) == 0
    assert p.crd(216) == pytest.approx(25806.51, abs=CENT)   # owed as month 216 opens
    assert all(p.prem_pp(t) == PREM_PP for t in (0, 215, 216, 239))
    assert sum(PREM_PP for _ in range(216, 240)) == 3360.00
    assert sum(p.premiums(t) for t in range(216, 240)) == pytest.approx(638.67, abs=CENT)
    assert all(p.premiums(t) > 0.0 for t in (216, 239))
    assert p.check_cover_end() is True
    for t in (216, 227, 239):
        assert p.claims(t, "ITT") == 0.0
        assert p.claims(t, "IPT") == 0.0
        assert p.pols_itt(t) == 0.0 and p.pols_ipt(t) == 0.0


def test_the_in_claim_mass_is_moved_not_deleted(fr_ade_anchor):
    """0.009266 in ITT and 0.013982 in IPT move into ``healthy`` at t = 216.

    Deleting them would break the state identity and destroy cover they still hold.
    """
    p = fr_ade_anchor
    assert p.pols_itt_close(215) == pytest.approx(0.009266, abs=STATE)
    assert p.pols_ipt_close(215) == pytest.approx(0.013982, abs=STATE)
    assert p.pols_itt_transfer(216) == pytest.approx(p.pols_itt_close(215), rel=1e-14)
    assert p.pols_ipt_transfer(216) == pytest.approx(p.pols_ipt_close(215), rel=1e-14)
    # The mass lands in healthy, so pols_if does not jump at the transfer.
    assert p.pols_healthy(216) == pytest.approx(
        p.pols_healthy_close(215) + p.pols_itt_transfer(216) + p.pols_ipt_transfer(216),
        rel=1e-14)
    assert p.pols_if(216) == pytest.approx(
        p.pols_healthy_close(215) + p.pols_itt_close(215) + p.pols_ipt_close(215),
        rel=1e-14)
    assert p.check_states() is True
    assert p.check_pols_roll_fwd() is True
    # And nothing moves in any other month.
    assert all(p.pols_itt_transfer(t) == 0.0 for t in (0, 99, 215, 217, 239))


def test_a_cover_can_end_long_before_the_loan(assurance_emprunteur):
    """Model point 8 loses ITT/IPT cover at t = 84 on a loan of 264 months."""
    p = assurance_emprunteur.Projection[8]
    assert p.itt_ipt_end_age() == 65 and p.deces_end_age() == 80
    assert p.proj_len() == 264
    assert p.cover_itt(83) == 1 and p.cover_itt(84) == 0
    assert p.crd(84) > 90000.0                    # most of the loan still outstanding
    assert p.claims(83, "ITT") > 0.0
    assert all(p.claims(t, "ITT") == 0.0 for t in (84, 179, 263))
    assert p.premiums(263) > 0.0                  # still paying, 180 months later
    assert p.cover_deces(263) == 1                # and still death covered
    assert p.check_cover_end() is True


# ---------------------------------------------------------------------------
# Payment timing and the ITT to IPT move


def test_a_new_inception_is_not_paid_in_the_month_it_incepts(fr_ade_anchor):
    """Monthly in arrears: a claim incepting at the end of month t is paid at t + 1."""
    p = fr_ade_anchor
    assert p.pols_itt(0) == 0.0
    assert p.claims(0, "ITT") == 0.0
    assert p.pols_itt_inception(0) > 0.0
    assert p.claims(1, "ITT") == pytest.approx(
        p.echeance() * S_ITT_1 * p.pols_itt_inception(0), rel=1e-9)
    assert p.claims(1, "ITT") == pytest.approx(0.93, abs=CENT)
    # The benefit excludes the cohort seeded this month, in every month.
    for t in (4, 59, 199):
        paid_on = p.claims(t, "ITT") / p.benefit_itt_pp()
        assert paid_on == pytest.approx(p.pols_itt_stay(t), rel=1e-12)
        assert paid_on < p.pols_itt(t) + p.pols_itt_inception(t)


def test_the_itt_to_ipt_movers_are_paid_exactly_once(fr_ade_anchor):
    """The paying-mass identity, including the term an implementation forgets.

    ``ben_itt + ben_ipt = ech Q IR (l_itt(t+1) - n_itt(t) + l_ipt(t+1) + cap_return(t))``.
    The lives sent back to ``healthy`` at the cap were in ITT throughout the month and
    are paid for it, but end it in neither disabled state.
    """
    p = fr_ade_anchor
    assert p.check_benefit_split() is True
    for t in (0, 1, 59, 119, 215, 239):
        assert p.check_benefit_split_resid(t) == pytest.approx(0.0, abs=1e-9)
    # The forgotten term is real: it is non-zero once the cap starts to bite.
    scale = p.benefit_itt_pp()
    worst = max(scale * p.pols_cap_return(t) for t in range(216))
    assert worst > 0.10
    # And an identity without it is wrong by exactly that much in the worst month.
    def naive(t):
        return (p.claims(t, "ITT") + p.claims(t, "IPT")
                - scale * (p.pols_itt_close(t) - p.pols_itt_inception(t)
                           + p.pols_ipt_close(t)))
    assert max(abs(naive(t)) for t in range(216)) == pytest.approx(worst, rel=1e-9)


def test_the_ipt_annuity_includes_the_month_of_the_transition(fr_ade_anchor):
    """A life moving at the end of month t is paid as IPT for that month, not skipped."""
    p = fr_ade_anchor
    t = 59
    assert p.pols_itt_to_ipt(t) > 0.0
    assert p.claims(t, "IPT") == pytest.approx(
        p.benefit_itt_pp() * (p.pols_ipt_stay(t) + p.pols_itt_to_ipt(t)), rel=1e-14)
    assert p.claims(t, "IPT") > p.benefit_itt_pp() * p.pols_ipt_stay(t)


# ---------------------------------------------------------------------------
# Premiums, lapse and the quotité


def test_premiums_are_never_carried_on_lives_in_claim(assurance_emprunteur):
    """Premiums are waived in claim, so income comes from ``healthy`` alone."""
    for point_id in assurance_emprunteur.Data.model_point_table().index:
        proj = assurance_emprunteur.Projection[point_id]
        for t in (0, 12, 59):
            if t >= proj.proj_len():
                continue
            assert proj.premiums(t) == pytest.approx(
                proj.prem_pp(t) * proj.pols_healthy(t), rel=1e-14)
            assert proj.premiums(t) <= proj.prem_pp(t) * proj.pols_if(t) + 1e-12


def test_lives_in_claim_never_lapse(fr_ade_anchor):
    """The *résiliation* decrement applies to ``healthy`` only.

    Applying it to ITT or IPT would silently cancel claims in payment.
    """
    p = fr_ade_anchor
    for t in (0, 12, 99, 215):
        assert p.pols_lapse(t) == pytest.approx(
            p.pols_healthy(t) * (1 - p.mort_rate_mth(t))
            * (1 - p.ptia_rate_mth(t) * p.cover_ptia(t)) * p.lapse_rate_mth(t),
            rel=1e-14)
    assert p.pols_lapse(99) < p.pols_if(99) * p.lapse_rate_mth(99)


def test_the_monthly_decrements_are_below_their_annual_rates(fr_ade_anchor):
    """Every ``*_rate_mth`` is strictly below its annual rate, and twelve compound back."""
    p = fr_ade_anchor
    for t in (0, 12, 99):
        assert 0 < p.mort_rate_mth(t) < p.mort_rate(t)
        assert 0 < p.lapse_rate_mth(t) < p.lapse_rate(t)
        assert 0 < p.itt_inception_rate_mth(t) < p.itt_inception_rate(t)
        assert (1 - p.mort_rate_mth(t)) ** 12 == pytest.approx(
            1 - p.mort_rate(t), rel=1e-12)
        assert (1 - p.lapse_rate_mth(t)) ** 12 == pytest.approx(
            1 - p.lapse_rate(t), rel=1e-12)


def test_quotite_scales_each_leg_exactly_once(assurance_emprunteur):
    """Model point 3 is the anchor at *quotité* 0.60: every cash flow is 0.60 of it.

    Applying it to the CRD and again to the benefit is invisible at 1.00.
    """
    p1 = assurance_emprunteur.Projection[1]
    p3 = assurance_emprunteur.Projection[3]
    assert p3.quotite() == 0.60
    assert p3.crd(50) == pytest.approx(p1.crd(50), rel=1e-14)   # the loan is unscaled
    for t in (0, 12, 99, 239):
        for kind in ("DEATH", "PTIA", "ITT", "IPT"):
            assert p3.claims(t, kind) == pytest.approx(
                0.60 * p1.claims(t, kind), rel=1e-12)
        assert p3.premiums(t) == pytest.approx(0.60 * p1.premiums(t), rel=1e-12)
    # The population is identical: the quotité is a money scale, not a decrement.
    assert p3.pols_healthy(99) == pytest.approx(p1.pols_healthy(99), rel=1e-14)


def test_the_decreasing_premium_rises_first(assurance_emprunteur):
    """On the CRD basis the premium rises for ten years before it falls.

    EUR 125.33 in year 1, EUR 164.03 at the year-10 peak, EUR 31.65 in year 20: the
    attained-age rate climbs faster than the CRD falls.
    """
    p = assurance_emprunteur.Projection[2]
    assert p.premium_basis() == "capital_restant_du"
    assert p.prem_pp(0) == pytest.approx(125.33, abs=CENT)
    assert p.prem_pp(108) == pytest.approx(164.03, abs=CENT)
    assert p.prem_pp(228) == pytest.approx(31.65, abs=CENT)
    by_year = [p.prem_pp(12 * y) for y in range(20)]     # the first month of each year
    assert by_year != sorted(by_year, reverse=True)      # NOT monotonically decreasing
    assert by_year.index(max(by_year)) == 9              # the peak is policy year 10
    # It is re-read on the CRD at the anniversary, and is level within the year.
    assert p.prem_pp(0) == pytest.approx(p.prem_pp(11), rel=1e-14)
    assert p.prem_pp(12) != pytest.approx(p.prem_pp(11), rel=1e-6)
    # The rate is held flat past the last pivot age rather than extrapolated.
    assert p.age(228) == 71 and p.crd_rate(228) == 0.0290


def test_the_two_premium_bases_are_pv_equivalent_on_this_cell(assurance_emprunteur):
    """EUR 12,602.19 against EUR 12,588.82 - a ratio of 1.001062, by construction."""
    p1 = assurance_emprunteur.Projection[1]
    p2 = assurance_emprunteur.Projection[2]
    assert p1.pv_premiums() == pytest.approx(PV_PREMIUMS, abs=CENT)
    assert p2.pv_premiums() == pytest.approx(PV_PREMIUMS_CRD_BASIS, abs=CENT)
    assert p1.pv_premiums() / p2.pv_premiums() == pytest.approx(1.001062, abs=5e-7)
    # The cover is identical, so every benefit is too.
    assert p2.pv_claims("DEATH") == pytest.approx(p1.pv_claims("DEATH"), rel=1e-12)


def test_indemnitaire_is_the_same_formula_with_a_ratio(assurance_emprunteur):
    """Model point 4 pays 0.55 of the *échéance*, and nothing else changes."""
    p1 = assurance_emprunteur.Projection[1]
    p4 = assurance_emprunteur.Projection[4]
    assert p4.indemnity_basis() == "indemnitaire"
    assert p4.income_loss_ratio() == 0.55
    assert p4.indemnity_ratio() == 0.55
    assert p1.indemnity_ratio() == 1.0
    for t in (59, 119, 199):
        for kind in ("ITT", "IPT"):
            assert p4.claims(t, kind) == pytest.approx(
                0.55 * p1.claims(t, kind), rel=1e-12)
        # The death and PTIA legs are untouched.
        assert p4.claims(t, "DEATH") == pytest.approx(p1.claims(t, "DEATH"), rel=1e-12)


def test_the_crd_ipt_basis_pays_a_capital_and_removes_the_life(assurance_emprunteur):
    """Model point 5 pays ``crd(t+1) x quotité`` once on consolidation, then the life goes."""
    p5 = assurance_emprunteur.Projection[5]
    assert p5.ipt_benefit_basis() == "crd"
    assert all(p5.pols_ipt(t) == 0.0 for t in (0, 59, 119, 215, 239))
    assert all(p5.pols_ipt_close(t) == 0.0 for t in (0, 59, 215))
    t = 59
    assert p5.pols_ipt_entry(t) > 0.0
    assert p5.pols_ipt_capital(t) == pytest.approx(p5.pols_ipt_entry(t), rel=1e-14)
    assert p5.claims(t, "IPT") == pytest.approx(
        p5.crd(t + 1) * p5.quotite() * p5.pols_ipt_entry(t), rel=1e-12)
    # They leave the model, exactly as a death does, so the identity still closes.
    assert p5.check_states() is True
    assert p5.check_pols_roll_fwd() is True
    assert p5.check_benefit_split() is True
    # The anchor keeps them as an annuity instead.
    p1 = assurance_emprunteur.Projection[1]
    assert p1.pols_ipt(119) > 0.0
    assert p1.pols_ipt_capital(119) == 0.0


def test_the_franchise_enters_only_through_the_inception_rate(assurance_emprunteur):
    """A shorter *franchise* admits more spells to payment; a longer one fewer."""
    p1 = assurance_emprunteur.Projection[1]
    p6 = assurance_emprunteur.Projection[6]
    p7 = assurance_emprunteur.Projection[7]
    assert (p1.franchise_days(), p1.franchise_factor()) == (90, 1.00)
    assert (p6.franchise_days(), p6.franchise_factor()) == (30, 1.60)
    assert (p7.franchise_days(), p7.franchise_factor()) == (180, 0.65)
    # No fourth state: nothing in the model names the franchise but the factor.
    names = set(assurance_emprunteur.Projection.cells)
    assert {n for n in names if "franchise" in n} == {
        "franchise_days", "franchise_factor"}
    # The female inception loading is in the table, not in a cells.
    tbl = assurance_emprunteur.Data.itt_inception_table()
    assert float(tbl.loc[("F", 50), "itt_inception_rate"]) == pytest.approx(
        1.30 * float(tbl.loc[("M", 50), "itt_inception_rate"]), rel=1e-9)
    mort = assurance_emprunteur.Data.mort_table()
    assert float(mort.loc[("F", 50), "mort_rate"]) == pytest.approx(
        0.60 * float(mort.loc[("M", 50), "mort_rate"]), rel=1e-9)


# ---------------------------------------------------------------------------
# Present values over the full projection


def test_the_present_values_over_the_full_240_months(fr_ade_anchor):
    """The notes' Checks: PV of premium, of each benefit, of expenses, and the margin."""
    p = fr_ade_anchor
    assert p.disc_rate == 0.025
    # Month 11 ends one full year after adhesion.
    assert p.disc_factor(11) == pytest.approx(1 / 1.025, rel=1e-12)
    assert p.pv_premiums() == pytest.approx(PV_PREMIUMS, abs=CENT)
    for kind, value in PV.items():
        assert p.pv_claims(kind) == pytest.approx(value, abs=CENT)
    assert p.pv_expenses() == pytest.approx(PV_EXPENSES, abs=CENT)
    assert p.pv_outgo() == pytest.approx(PV_OUTGO, abs=CENT)
    assert 1 - p.pv_outgo() / p.pv_premiums() == pytest.approx(0.0981, abs=5e-5)
    benefits = p.pv_outgo() - p.pv_expenses()
    death_side = (p.pv_claims("DEATH") + p.pv_claims("PTIA")) / benefits
    assert death_side == pytest.approx(0.708, abs=5e-4)
    assert 1 - death_side == pytest.approx(0.292, abs=5e-4)


def test_nothing_in_result_cf_is_discounted(fr_ade_anchor):
    """The discount companion is not part of the cash flow projection."""
    p = fr_ade_anchor
    df = p.result_cf()
    assert df.loc[0, "claims_death"] == pytest.approx(65.25, abs=CENT)
    assert "disc_factor" not in df.columns
    assert df["premiums"].sum() > p.pv_premiums()      # undiscounted is the upper bound


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(fr_ade_anchor):
    df = fr_ade_anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(240))     # t = 0 .. proj_len() - 1
    assert list(df.columns) == [
        "pols_if", "pols_healthy", "pols_itt", "pols_ipt", "crd", "premiums",
        "claims_death", "claims_ptia", "claims_itt", "claims_ipt", "claims_lapse",
        "claims_maturity", "expenses", "liability_cf", "net_cf",
    ]
    assert "claims" not in df.columns                 # never a subtotal beside its parts


def test_net_cf_is_the_negative_of_the_notes_liability_cf(fr_ade_anchor):
    """The notes print the stream outgo-positive; ``net_cf`` is income-positive."""
    df = fr_ade_anchor.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == 0.0
    outgo = df[["claims_death", "claims_ptia", "claims_itt", "claims_ipt",
                "claims_lapse", "claims_maturity", "expenses"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    assert df.loc[0, "net_cf"] > 0.0                  # premium exceeds outgo early on


def test_resiliation_and_expiry_pay_nothing(assurance_emprunteur):
    """No surrender value at any time and no maturity benefit."""
    for point_id in assurance_emprunteur.Data.model_point_table().index:
        df = assurance_emprunteur.Projection[point_id].result_cf()
        assert (df["claims_lapse"] == 0.0).all()
        assert (df["claims_maturity"] == 0.0).all()
    p = assurance_emprunteur.Projection[1]
    assert p.pols_lapse(49) > 0.0                     # lapses happen; they just pay nothing
    assert p.pols_maturity(239) > 0.0                 # the last month, proj_len() - 1
    assert all(p.pols_maturity(t) == 0.0 for t in (0, 99, 238))


def test_expenses_carry_the_claim_management_load(fr_ade_anchor):
    """EUR 30 a year on every policy in force plus EUR 250 a year on every claim."""
    p = fr_ade_anchor
    for t in (0, 12, 99):
        expected = (30.0 / 12 * 1.018 ** (p.policy_year(t) - 1) * p.pols_if(t)
                    + 250.0 / 12 * 1.018 ** (p.policy_year(t) - 1)
                    * (p.pols_itt(t) + p.pols_ipt(t)))
        assert p.expenses(t) == pytest.approx(expected, rel=1e-12)
    assert p.expenses(0) == pytest.approx(30.0 / 12, rel=1e-12)   # nobody in claim yet


def test_every_model_point_projects_and_every_check_closes(assurance_emprunteur):
    """Twelve cells, five checks each, and the same columns on every one."""
    ids = list(assurance_emprunteur.Data.model_point_table().index)
    assert len(ids) == 12
    columns = None
    for point_id in ids:
        proj = assurance_emprunteur.Projection[point_id]
        df = proj.result_cf()
        assert len(df) == proj.proj_len() > 0
        assert df.notna().all().all()
        assert df["net_cf"].abs().sum() < float("inf")
        for name in ("check_crd", "check_states", "check_pols_roll_fwd",
                     "check_benefit_split", "check_cover_end"):
            value = getattr(proj, name)()
            assert value is True, (point_id, name)
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns, point_id


def test_the_shipped_tables_mark_their_own_provenance():
    """Every decrement CSV says in words that it is a [std] proxy."""
    import pandas as pd

    for name in ("mort_table.csv", "itt_inception_table.csv",
                 "itt_termination_table.csv", "franchise_table.csv",
                 "lapse_table.csv", "crd_rate_table.csv"):
        tbl = pd.read_csv(MODEL_DIR.parent / name)
        assert "provenance" in tbl.columns, name
        assert tbl["provenance"].notna().all(), name
        assert all("[std]" in v for v in tbl["provenance"]), name

    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    male = mort[mort["sex"] == "M"].sort_values("age")
    assert list(male["age"]) == [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
    assert list(male["mort_rate"]) == [
        0.0006, 0.0008, 0.0012, 0.0020, 0.0032, 0.0050,
        0.0076, 0.0115, 0.0175, 0.0270, 0.0450, 0.0780]

    term = pd.read_csv(MODEL_DIR.parent / "itt_termination_table.csv")
    assert list(term["itt_recovery_rate"]) == [0.55, 0.30, 0.15]
    assert list(term["itt_to_ipt_rate"]) == [0.02, 0.06, 0.12]
    assert list(term["itt_mort_rate"]) == [0.02, 0.03, 0.04]

    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv")
    assert list(lapse["lapse_rate"]) == [0.04, 0.12, 0.12, 0.10, 0.10, 0.07]


def test_inputs_live_beside_the_model():
    """The seven input CSVs sit in the model folder's parent directory.

    There is deliberately no loan schedule file: the *échéancier* is computed.
    """
    expected = {"model_point_table.csv", "mort_table.csv", "itt_inception_table.csv",
                "itt_termination_table.csv", "franchise_table.csv", "lapse_table.csv",
                "crd_rate_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}
    assert {p.name for p in MODEL_DIR.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows."""
    import pandas as pd

    src = MODEL_DIR.parent / "lapse_table.csv"
    heavier = pd.read_csv(src, index_col="policy_year")
    heavier["lapse_rate"] = heavier["lapse_rate"] * 2.0

    model = mx.read_model(MODEL_DIR, name="ADE_FR_S_swap")
    try:
        alt_name = "lapse_table_heavy.csv"
        heavier.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].pv_premiums()
            model.Data.lapse_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            proj = model.Projection[1]
            assert proj.lapse_rate(0) == pytest.approx(0.08, rel=1e-12)
            # Twice the substitution rate empties the book faster, so less premium.
            assert proj.pv_premiums() < base
            assert proj.check_states() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_dynamic_substitution_response_is_off_in_the_base_run():
    """gap = 0, so the loi Lemoine uplift is dormant and the table rate stands."""
    p_model = mx.read_model(MODEL_DIR, name="ADE_FR_S_gap")
    try:
        proj = p_model.Projection[1]
        assert proj.market_prem_ratio == 1.0
        assert all(proj.prem_gap(t) == 0.0 for t in (0, 12, 99))
        assert all(proj.lapse_rate(t) == proj.lapse_rate_base(t) for t in (0, 12, 99))
        # Price the book 20 % above the market and the decrement responds.
        p_model.Projection.market_prem_ratio = 1 / 1.2
        p_model.Projection.clear_all()
        proj = p_model.Projection[1]
        assert proj.prem_gap(0) == pytest.approx(0.2, rel=1e-9)
        expected = 0.04 * (1 + 3.0 * 0.88 * 0.2)
        assert proj.lapse_rate(0) == pytest.approx(expected, rel=1e-9)
        assert proj.lapse_rate(0) > proj.lapse_rate_base(0)
        # And it is capped.
        p_model.Projection.market_prem_ratio = 0.2
        p_model.Projection.clear_all()
        assert p_model.Projection[1].lapse_rate(12) == pytest.approx(0.35, rel=1e-12)
    finally:
        p_model.close()


def test_invalid_enum_values_raise(fr_ade_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_ade_anchor.pols_if_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        fr_ade_anchor.claims(0, "SURRENDER")


def test_model_docstring_describes_the_current_structure(assurance_emprunteur):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = assurance_emprunteur.doc
    assert "assurance emprunteur" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "four-state" in doc
    assert "two-dimensional" in doc
    assert "capital restant" in doc


def test_space_docstrings_carry_their_reference_material(assurance_emprunteur):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = assurance_emprunteur.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "crd", "echeance", "itt_cohorts",
                  "pols_healthy", "pols_itt_close", "pols_cap_return", "quotite"):
        assert cells in proj
    data = assurance_emprunteur.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "itt_termination_table"):
        assert cells in data


def test_cells_names_follow_the_library_vocabulary(assurance_emprunteur):
    """Names shared with lifelib and with the rest of this library must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "proj_len", "age", "pols_if",
        "pols_if_at", "pols_if_init", "pols_lapse", "pols_maturity", "mort_rate",
        "mort_rate_mth", "lapse_rate", "lapse_rate_mth", "premiums", "claims",
        "expenses", "expense_maint", "inflation_rate", "inflation_factor", "net_cf",
        "result_cf", "policy_year", "duration", "duration_mth",
    }
    names = (set(assurance_emprunteur.Projection.cells)
             | set(assurance_emprunteur.Projection.refs))
    assert shared <= names, f"missing: {sorted(shared - names)}"
    retired = {"lapse_rate_ann", "free_wd_used_pp", "free_wd_taken_pp", "prem_net_pp",
               "mort_a_e_factor", "ae_factor", "omega", "check_tol"}
    assert not (names & retired)
    # No account value machinery: the only state is the population and the loan.
    for absent in ("av_pp_at", "av_at", "cv_pp", "asset_share", "surr_charge_rate"):
        assert absent not in names


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    model = mx.read_model(MODEL_DIR, name="ADE_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="ADE_FR_S_rt")
    try:
        proj = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert proj.pols_healthy_close(t) == pytest.approx(row[1], abs=STATE)
            assert proj.claims(t, "DEATH") == pytest.approx(row[5], abs=CENT)
        assert proj.check_crd() is True
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
