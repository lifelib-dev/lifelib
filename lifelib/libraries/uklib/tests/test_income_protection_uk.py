"""Golden and structural tests for IP_UK_S.

The golden values are the worked example in
products/income_protection/technical-notes.md ("Worked example"), which is a
**claims-in-payment** recursion: a claim in payment from duration zero on the base cell's
level-cover variant, benefit GBP 2,000 a month, duration-year-1 termination rates,
discounted at a flat 3%.  Model point 2 is that cell.  The notes also give the month-one
active-lives figures beside it, and model point 1 is that cell.

They are hard-coded here rather than pickled so that a reviewer can compare them against
the notes by eye.  Tolerances follow the precision the notes display: money to the penny,
state probabilities to six decimals.

Beyond the worked example this module asserts the product facts the notes call out as
modelling pitfalls, because each is a way an implementation can look right and be wrong:

* the in-claim population must keep its duration dimension;
* premium income must come from state H alone, never from lives in claim;
* the disabled-life annuity must truncate at the policy end date;
* and the amount payable is bounded above by the chosen benefit, never below it.
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
STATE = 2e-6          # state probabilities to 6 d.p. -- see the note below

MODEL_DIR = LIB / MODELS["IP_UK_S"][0]

# m: (l_S at start, recoveries, deaths in claim, l_S at end, benefit, v^m, PV)
WORKED_EXAMPLE = {
    1: (1.000000, 0.041675, 0.002429, 0.955895, 1911.79, 0.997540, 1907.09),
    2: (0.955895, 0.039837, 0.002322, 0.913735, 1827.47, 0.995086, 1818.49),
    3: (0.913735, 0.038080, 0.002220, 0.873434, 1746.87, 0.992638, 1734.01),
}
WORKED_EXAMPLE_PV3 = 5459.59        # three-month PV of benefit outgo

# The notes chain their *displayed* (rounded) survival factors down the table, so by the
# third row the sixth decimal of the state column has drifted about 1.3e-6 from the
# unrounded product s_S^3.  The money columns are unaffected -- every one of them still
# agrees to the penny -- so the state tolerance is set just wide enough to absorb the
# notes' own rounding rather than the goldens being restated.

# The notes' derived monthly factors for duration year 1.
RHO_M = 0.041675          # 1 - 0.60^(1/12)
Q_S_M = 0.002535          # 1 - 0.97^(1/12)
S_S = 0.955895            # (1 - rho_m)(1 - q_S_m)
V_M = 0.997540            # 1.03^(-1/12)


# ---------------------------------------------------------------------------
# The claims-in-payment worked example


@pytest.mark.parametrize("m", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_ip_claim, m):
    """Every cell of the notes' three-month table, to the displayed precision."""
    start, rec, dth, end, ben, v, pv = WORKED_EXAMPLE[m]
    p = uk_ip_claim
    assert p.pols_sick(m) == pytest.approx(start, abs=STATE)
    assert p.pols_recovery(m) == pytest.approx(rec, abs=STATE)
    assert p.pols_death_sick(m) == pytest.approx(dth, abs=STATE)
    assert p.pols_sick_surv(m) == pytest.approx(end, abs=STATE)
    assert p.claims(m, "BENEFIT") == pytest.approx(ben, abs=PENNY)
    assert p.disc_factor(m) == pytest.approx(v, abs=5e-7)
    assert p.claims(m, "BENEFIT") * p.disc_factor(m) == pytest.approx(pv, abs=PENNY)


def test_worked_example_three_month_pv(uk_ip_claim):
    """The notes' headline: GBP 5,459.59 per claim in payment over three months."""
    p = uk_ip_claim
    total = sum(p.claims(m, "BENEFIT") * p.disc_factor(m) for m in (1, 2, 3))
    assert total == pytest.approx(WORKED_EXAMPLE_PV3, abs=PENNY)


def test_worked_example_monthly_factors(uk_ip_claim):
    """The notes' derived factors: rho_m, q_S_m, s_S and v, all at duration year 1."""
    p = uk_ip_claim
    assert p.rec_rate(1) == 0.40
    assert p.mort_rate_sick(1) == 0.03
    assert p.rec_rate_mth(1) == pytest.approx(RHO_M, abs=5e-7)
    assert p.mort_rate_sick_mth(1) == pytest.approx(Q_S_M, abs=5e-7)
    assert p.claim_surv_step(1) == pytest.approx(S_S, abs=5e-7)
    assert p.claim_surv_step(1) == pytest.approx(
        (1 - p.rec_rate_mth(1)) * (1 - p.mort_rate_sick_mth(1)), rel=1e-14)
    assert p.disc_factor(1) == pytest.approx(V_M, abs=5e-7)


def test_worked_example_is_a_survival_product(uk_ip_claim):
    """l_S(m) = s_S^m while the duration-year-1 rates hold: exits leave for good."""
    p = uk_ip_claim
    s = p.claim_surv_step(1)
    for m in (1, 2, 3, 12):
        assert p.pols_sick_surv(m) == pytest.approx(s ** m, rel=1e-12)


def test_worked_example_active_side(income_protection):
    """The notes' month-one active-lives figures: premium 35.00 and n(1) = 0.000108."""
    p = income_protection.Projection[1]
    assert p.premiums(1) == pytest.approx(35.00, abs=PENNY)
    assert p.pols_active(1) == 1.0
    assert p.inception_rate(1) == pytest.approx(0.0013, rel=1e-12)
    assert p.inception_rate_mth(1) == pytest.approx(0.000108, abs=5e-7)
    # n(1) is the inception rate net of the month's mortality and lapse, so a shade under.
    assert p.pols_inception(1) == pytest.approx(0.000107, abs=5e-7)
    assert p.pols_inception(1) < p.inception_rate_mth(1)


# ---------------------------------------------------------------------------
# The duration dimension


def test_the_recovery_rate_falls_with_claim_duration(uk_ip_claim):
    """40 / 25 / 15 / 10 / 5 percent by duration year, then level.

    The gradient is the defining feature of income protection terminations, which is why
    the model tracks cohorts rather than a single in-claim bucket.
    """
    p = uk_ip_claim
    assert [p.rec_rate(z) for z in (1, 13, 25, 37, 49, 61, 200)] == [
        0.40, 0.25, 0.15, 0.10, 0.05, 0.05, 0.05]
    assert p.claim_dur_year(1) == 1 and p.claim_dur_year(12) == 1
    assert p.claim_dur_year(13) == 2 and p.claim_dur_year(24) == 2
    # In-claim mortality is flat in the shipped proxy - the crudest part of the basis.
    assert all(p.mort_rate_sick(z) == 0.03 for z in (1, 13, 61, 200))


def test_collapsing_the_duration_dimension_would_misstate_the_runoff(uk_ip_claim):
    """A single bucket at the year-one rate runs a claim off far faster than the cohorts.

    The notes' first-listed pitfall, quantified: after five years the duration-aware
    survival is several times the flat-rate one, because most survivors have long since
    left the 40% band.
    """
    p = uk_ip_claim
    cohort_surv = p.pols_sick(61)                    # start of month 61, i.e. 5 years
    flat = p.claim_surv_step(1) ** 60                # as if every month were year one
    assert cohort_surv > 4 * flat                    # 0.281 against 0.067


def test_the_cohort_vector_and_the_two_dimensional_view_agree(uk_ip_claim):
    """pols_sick(t) is the sum of pols_sick_dur(t, z) over every tracked duration."""
    p = uk_ip_claim
    for t in (1, 2, 13, 100):
        by_cohort = sum(p.pols_sick_dur(t, z) for z in range(1, p.max_dur() + 1))
        assert p.pols_sick(t) == pytest.approx(by_cohort, rel=1e-12)
    assert p.pols_sick_dur(1, 1) == 1.0              # the seeded claim, at duration 1
    assert p.pols_sick_dur(1, 2) == 0.0
    assert p.pols_sick_dur(5, 0) == 0.0              # out of range, not an error
    assert p.pols_sick_dur(5, 10**6) == 0.0


def test_a_seeded_claim_starts_at_its_stated_duration(income_protection):
    """Model point 5 is a claim already 30 months old, so it enters cohort 31."""
    p = income_protection.Projection[5]
    assert p.claim_duration_months() == 30
    assert p.pols_sick_dur(1, 31) == 1.0
    assert p.pols_sick_dur(1, 1) == 0.0
    # And it is therefore in duration year 3, where recovery has fallen to 15%.
    assert p.claim_dur_year(31) == 3
    assert p.rec_rate(31) == 0.15


def test_the_cohort_vector_is_rebuilt_not_mutated(uk_ip_claim):
    """Holding a returned list cannot corrupt the cache."""
    p = uk_ip_claim
    v = p.sick_cohorts(3)
    before = p.pols_sick(3)
    v[0] = 999.0                                     # mutate the caller's copy
    assert p.sick_cohorts(3)[0] != 999.0 or p.pols_sick(3) == before
    assert p.pols_sick(3) == pytest.approx(before, rel=1e-14)


# ---------------------------------------------------------------------------
# Premiums come from state H alone


def test_premiums_are_never_carried_on_lives_in_claim(income_protection):
    """The notes' second pitfall: premiums are waived from the start of benefit payment.

    Projecting income from l_S overstates it by the whole in-claim population.
    """
    for point_id in income_protection.Data.model_point_table().index:
        proj = income_protection.Projection[point_id]
        for t in (1, 13, 60):
            if t > proj.proj_len():
                continue
            assert proj.premiums(t) == pytest.approx(
                proj.premium_pp(t) * proj.pols_active(t), rel=1e-14)


def test_a_claims_in_payment_cell_pays_no_premium_at_all(uk_ip_claim):
    """Everything is in S on the exit basis, so premium income is zero throughout."""
    p = uk_ip_claim
    assert p.status() == "in_claim"
    assert (p.result_cf()["premiums"] == 0.0).all()
    assert (p.result_cf()["pols_active"] == 0.0).all()


def test_result_cf_publishes_the_waived_population(income_protection):
    """pols_if minus pols_active is the population whose premiums are waived."""
    p = income_protection.Projection[1]
    df = p.result_cf()
    assert (df["pols_if"] - df["pols_active"] - df["pols_sick"]).abs().max() == (
        pytest.approx(0.0, abs=1e-12))
    assert df["pols_sick"].max() > 0.0        # some population is in claim at some point


def test_lives_in_claim_never_lapse(income_protection):
    """Premiums are waived and the benefit is valuable, so lapse applies to H only."""
    p = income_protection.Projection[1]
    for t in (1, 13, 100):
        assert p.pols_lapse(t) == pytest.approx(
            p.pols_active(t) * (1 - p.mort_rate_mth(t)) * p.lapse_rate_mth(t),
            rel=1e-14)
    assert all(income_protection.Projection[2].pols_lapse(t) == 0.0
               for t in (1, 13, 100))


# ---------------------------------------------------------------------------
# Payment timing


def test_a_new_inception_is_not_paid_in_the_month_it_incepts(income_protection):
    """Monthly in arrears: a claim incepting at the end of month t is paid at t + 1.

    Paying the new inceptions would hand over a full month's benefit at the instant
    payment starts and break the inception-annuity equivalence.
    """
    p = income_protection.Projection[1]
    assert p.pols_sick(1) == 0.0                      # nobody in claim yet
    assert p.claims(1, "BENEFIT") == 0.0              # so nothing is paid
    assert p.pols_inception(1) > 0.0                  # even though claims incepted
    assert p.pols_sick_dur(2, 1) == pytest.approx(p.pols_inception(1), rel=1e-14)
    assert p.claims(2, "BENEFIT") > 0.0
    # The benefit excludes the cohort seeded this month, in every month.
    for t in (5, 50, 200):
        paid_on = p.claims(t, "BENEFIT") / p.amount_payable_pp(t)
        assert paid_on == pytest.approx(p.pols_sick_surv(t), rel=1e-12)
        assert paid_on < p.pols_sick(t) + p.pols_inception(t)


# ---------------------------------------------------------------------------
# Expiry truncation


def test_everything_terminates_at_the_policy_end_date(uk_ip_claim):
    """All cover and any claim in payment cease at expiry with no value."""
    p = uk_ip_claim
    assert p.proj_len() == 360 == 12 * (p.expiry_age() - p.age_at_entry())
    assert p.pols_sick(360) > 0.0
    assert p.pols_sick(361) == 0.0
    assert p.pols_if(361) == 0.0
    assert p.pols_if_at(360, "AFT_DECR") == 0.0
    for t in (1, 100, 359):
        assert p.pols_maturity(t) == 0.0
    assert p.pols_maturity(360) > 0.0
    assert p.check_pols_roll_fwd() is True


def test_a_claim_near_expiry_is_truncated(income_protection):
    """Model point 5 has 15 years to run, so its annuity stops well short of run-off.

    An untruncated disabled-life annuity materially overstates the liability for claims
    incepting near expiry - the notes' third pitfall.
    """
    p = income_protection.Projection[5]
    assert p.proj_len() == 180
    assert p.pols_sick(180) > 0.0                 # still paying in the final month
    assert p.pols_sick(181) == 0.0                # and nothing after it
    # Its annuity factor is bounded by the months remaining, obviously - but the
    # binding fact is that a fifth of a claim is still in payment when cover ceases.
    assert p.annuity_dis() < 180
    assert p.pols_sick(180) > 0.10


# ---------------------------------------------------------------------------
# Where recoveries go


def test_the_exit_basis_is_a_pure_disabled_life_annuity(uk_ip_claim):
    """Recovered lives leave the model, so nothing returns to H and nothing re-incepts."""
    p = uk_ip_claim
    assert p.recovery_basis() == "exit"
    assert all(p.pols_active(t) == 0.0 for t in (1, 2, 50, 360))
    assert all(p.pols_inception(t) == 0.0 for t in (1, 2, 50, 360))
    for t in (1, 50):
        assert p.pols_exit(t) == p.pols_recovery(t)
    assert p.pols_exit_cum(361) > 0.0


def test_the_return_to_h_basis_gives_a_bigger_liability(income_protection):
    """Model point 7 is point 2 with recoveries returning: recovered lives claim again.

    Both readings are shipped because the choice is a valuation question - a
    claims-in-payment reserve is the disabled-life annuity, a full contract-boundary
    best estimate carries the post-recovery active phase too.
    """
    p2, p7 = income_protection.Projection[2], income_protection.Projection[7]
    assert p2.recovery_basis() == "exit"
    assert p7.recovery_basis() == "return_to_h"
    assert p2.status() == p7.status() == "in_claim"
    assert p7.pv_benefits() > p2.pv_benefits()
    assert p7.pols_active(50) > 0.0               # recovered lives are back in H
    assert p7.pols_inception(50) > 0.0            # and exposed to inception again
    assert all(p7.pols_exit(t) == 0.0 for t in (1, 50, 200))
    # They also start paying premiums again, which the exit basis never sees.
    assert p7.premiums(50) > 0.0 and p2.premiums(50) == 0.0


def test_the_two_bases_agree_in_the_first_month(income_protection):
    """Nothing has recovered yet, so the worked-example window cannot distinguish them."""
    p2, p7 = income_protection.Projection[2], income_protection.Projection[7]
    assert p2.claims(1, "BENEFIT") == pytest.approx(p7.claims(1, "BENEFIT"), rel=1e-14)
    assert p2.claims(2, "BENEFIT") == pytest.approx(p7.claims(2, "BENEFIT"), rel=1e-14)


# ---------------------------------------------------------------------------
# The three-state population identity


def test_the_population_identity_closes(income_protection):
    """H + S + cumulative deaths + lapses + exits equals the starting population.

    The check that catches a leak in the cohort machinery: a mis-indexed duration shift
    drops population out of S with no corresponding exit, and nothing else would notice.
    """
    for point_id in income_protection.Data.model_point_table().index:
        proj = income_protection.Projection[point_id]
        assert proj.check_states() is True, point_id
        for t in (1, 13, proj.proj_len()):
            assert proj.check_states_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_the_rollforward_closes(income_protection):
    """pols_if(t) - pols_if(t+1) is deaths, lapses, exits and the expiry - not moves."""
    p = income_protection.Projection[1]
    assert p.check_pols_roll_fwd() is True
    for t in (1, 50, 360):
        out = (p.pols_death_active(t) + p.pols_death_sick(t) + p.pols_lapse(t)
               + p.pols_exit(t) + p.pols_maturity(t))
        assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12)
    # Inceptions and returning recoveries are moves between states, not exits.
    assert p.pols_inception(50) > 0.0 and p.pols_recovery(50) > 0.0
    assert p.pols_exit(50) == 0.0


def test_deaths_come_from_both_states(income_protection):
    """Two mortality rates on two clocks, and they are different cells."""
    p = income_protection.Projection[1]
    for t in (13, 100):
        assert p.pols_death_active(t) == pytest.approx(
            p.pols_active(t) * p.mort_rate_mth(t), rel=1e-14)
        assert p.pols_death_sick(t) > 0.0
    # mort_rate is the active-life rate; the claimant rate is keyed by claim duration.
    assert p.mort_rate(1) != pytest.approx(p.mort_rate_sick(1), rel=1e-3)
    assert p.mort_rate(1) < p.mort_rate_sick(1)      # claimants die faster


# ---------------------------------------------------------------------------
# Rates, interpolation and the deferred period


def test_inception_interpolation_is_linear(income_protection):
    """Linear between pivot ages - the notes' rule, and not the log-linear CI one."""
    p = income_protection.Projection[1]
    # The pivots come back exactly at the pivot ages.
    assert p.age(1) == 35 and p.inception_rate(1) == pytest.approx(0.0013, rel=1e-12)
    assert p.age(61) == 40 and p.inception_rate(61) == pytest.approx(0.0018, rel=1e-12)
    # Inside a segment the rate is the linear reading, not the geometric one.
    t38 = 37                                         # policy year 4, attained age 38
    assert p.age(t38) == 38
    arithmetic = 0.0013 + (0.0018 - 0.0013) * 3 / 5
    geometric = 0.0013 * (0.0018 / 0.0013) ** (3 / 5)
    assert p.inception_rate(t38) == pytest.approx(arithmetic, rel=1e-12)
    assert p.inception_rate(t38) != pytest.approx(geometric, rel=1e-6)


def test_the_deferred_period_enters_only_through_the_inception_rate(income_protection):
    """No fourth state: iota is a claim *payment* inception rate specific to the DP.

    A sickness spell recovering inside the deferred period never leaves H, and a life
    sick but not yet in payment stays in H and keeps paying premiums.
    """
    p = income_protection.Projection[1]
    assert p.deferred_weeks() == 26
    names = set(income_protection.Projection.cells)
    assert not [n for n in names if "deferred" in n and n != "deferred_weeks"]
    # A shorter deferred period admits more claims to payment; a longer one fewer.
    model = mx.read_model(MODEL_DIR, name="IP_UK_S_dp")
    try:
        rates = {}
        for dp in (4, 13, 26, 52):
            row = model.Data.inception_table().loc[("M", 1, dp, 35), "inception_rate"]
            rates[dp] = float(row)
        assert rates[4] > rates[13] > rates[26] > rates[52]
        assert rates[26] == pytest.approx(0.0013, rel=1e-12)
    finally:
        model.close()


def test_occupation_class_and_sex_move_the_inception_rate(income_protection):
    """Heavier occupation classes and female lives carry higher inception rates."""
    model = mx.read_model(MODEL_DIR, name="IP_UK_S_occ")
    try:
        tbl = model.Data.inception_table()
        base = float(tbl.loc[("M", 1, 26, 45), "inception_rate"])
        assert float(tbl.loc[("M", 2, 26, 45), "inception_rate"]) > base
        assert float(tbl.loc[("M", 4, 26, 45), "inception_rate"]) > float(
            tbl.loc[("M", 3, 26, 45), "inception_rate"])
        assert float(tbl.loc[("F", 1, 26, 45), "inception_rate"]) == pytest.approx(
            base * 1.25, rel=1e-9)
    finally:
        model.close()


def test_the_economic_cycle_overlay_is_off_and_moves_both_rates(income_protection):
    """M_cycle raises inceptions and slows recoveries at once; 1 in the base run."""
    p = income_protection.Projection[1]
    base_inception = p.inception_rate(1)
    base_recovery = p.rec_rate(1)

    model = mx.read_model(MODEL_DIR, name="IP_UK_S_cycle")
    try:
        model.Projection.cycle_factor = 1.25
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.inception_rate(1) == pytest.approx(base_inception * 1.25, rel=1e-12)
        assert proj.rec_rate(1) == pytest.approx(base_recovery / 1.25, rel=1e-12)
        assert proj.rec_rate(1) < base_recovery
    finally:
        model.close()


def test_the_shipped_tables_mark_their_own_provenance():
    """Only the M / OC1 / DP26 inception pivots are the notes' own values."""
    import pandas as pd

    inc = pd.read_csv(MODEL_DIR.parent / "inception_table.csv")
    assert inc["provenance"].notna().all()
    notes = inc[inc["provenance"] == "notes [std] proxy pivot"]
    assert len(notes) == 8
    assert set(notes["sex"]) == {"M"} and set(notes["occ_class"]) == {1}
    assert set(notes["deferred_weeks"]) == {26}
    assert list(notes.sort_values("age")["inception_rate"]) == [
        0.0010, 0.0013, 0.0018, 0.0026, 0.0040, 0.0065, 0.0100, 0.0140]

    term = pd.read_csv(MODEL_DIR.parent / "termination_table.csv")
    assert list(term["recovery_rate"]) == [0.40, 0.25, 0.15, 0.10, 0.05]
    assert set(term["mort_rate_sick"]) == {0.03}

    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert set(mort["provenance"]) == {"[std] ONS-shaped proxy"}


# ---------------------------------------------------------------------------
# Benefit, escalation and the amount payable


def test_the_two_band_benefit_maximum(income_protection):
    """65% to the GBP 60,000 breakpoint and 50% above it, capped and floored."""
    p1 = income_protection.Projection[1]
    assert p1.earnings_annual() == 40000.0
    assert p1.benefit_max_pp() == pytest.approx(0.65 * 40000 / 12, rel=1e-12)
    assert p1.benefit_mth() < p1.benefit_max_pp()

    p6 = income_protection.Projection[6]          # earnings cross the breakpoint
    assert p6.earnings_annual() == 80000.0
    assert p6.benefit_max_pp() == pytest.approx(
        (0.65 * 60000 + 0.50 * 20000) / 12, rel=1e-12)
    assert p6.benefit_mth() < p6.benefit_max_pp()


def test_the_benefit_guarantee_and_cap_bound_the_formula(income_protection):
    """The GBP 1,500 a month guarantee floors it and the GBP 20,000 cap tops it out."""
    model = mx.read_model(MODEL_DIR, name="IP_UK_S_bandcheck")
    try:
        proj = model.Projection[1]
        # A tiny earnings figure floors at the guarantee rather than going to zero.
        assert proj.benefit_max_pp() > 0
        model.Projection.ben_guarantee_mth = 5000.0
        model.Projection.clear_all()
        assert model.Projection[1].benefit_max_pp() == 5000.0
        model.Projection.ben_guarantee_mth = 1500.0
        model.Projection.ben_cap_mth = 1000.0
        model.Projection.clear_all()
        # Cap first, then the guarantee floor - so a cap below the floor loses.
        assert model.Projection[1].benefit_max_pp() == 1500.0
    finally:
        model.close()


def test_every_model_point_is_inside_its_benefit_maximum(income_protection):
    """check_benefit_max validates the model point, not the projection.

    A benefit above the contractual maximum is a policy that could not have been
    written, and the underwriting record sits on the model point so that it can be
    checked.
    """
    for point_id in income_protection.Data.model_point_table().index:
        assert income_protection.Projection[point_id].check_benefit_max() is True


def test_escalation_compounds_benefit_and_premium(income_protection):
    """Flat 3% RPI: benefit x 1.03 and premium x 1.045 per policy anniversary."""
    p = income_protection.Projection[1]
    assert p.escalation() == "RPI"
    assert p.esc_rate() == pytest.approx(0.03, rel=1e-12)
    for y, t in ((1, 1), (2, 13), (5, 49)):
        assert p.policy_year(t) == y
        assert p.benefit_pp(t) == pytest.approx(2000.0 * 1.03 ** (y - 1), rel=1e-12)
        assert p.premium_pp(t) == pytest.approx(35.0 * 1.045 ** (y - 1), rel=1e-12)
    assert p.benefit_pp(12) == p.benefit_pp(1)      # steps on anniversaries only


def test_escalation_continues_in_claim(income_protection):
    """The benefit escalates in claim while the premium that would fund it does not.

    That asymmetry is why the escalation option is inflation-sensitive on exactly the
    claims that are longest, and the 10% cap is an embedded inflation option.
    """
    p = income_protection.Projection[1]
    assert p.amount_payable_pp(13) == pytest.approx(
        p.amount_payable_pp(1) * 1.03, rel=1e-12)
    assert p.premiums(13) == pytest.approx(p.premium_pp(13) * p.pols_active(13),
                                           rel=1e-14)
    # Escalation is capped at 10% and floored at 0.
    model = mx.read_model(MODEL_DIR, name="IP_UK_S_esc")
    try:
        model.Projection.rpi_rate = 0.25
        model.Projection.clear_all()
        assert model.Projection[1].esc_rate() == pytest.approx(0.10, rel=1e-12)
        model.Projection.rpi_rate = -0.02
        model.Projection.clear_all()
        assert model.Projection[1].esc_rate() == 0.0
    finally:
        model.close()


def test_the_escalation_lapse_shock_is_off_at_a_three_percent_rpi(income_protection):
    """1.5 x 3% = 4.5%, below the 5% threshold, so M_esc is 1 in the base run."""
    p = income_protection.Projection[1]
    assert all(p.esc_lapse_factor(t) == 1.0 for t in (1, 13, 100))
    assert p.lapse_rate(13) == p.lapse_rate_base(13)

    model = mx.read_model(MODEL_DIR, name="IP_UK_S_escshock")
    try:
        model.Projection.rpi_rate = 0.10          # at the cap: 15% premium growth
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.esc_lapse_factor(1) == 1.0    # no uplift in policy year 1
        assert proj.esc_lapse_factor(13) == pytest.approx(1.2, rel=1e-12)
        assert proj.lapse_rate(13) > proj.lapse_rate_base(13)
    finally:
        model.close()


def test_a_level_cover_cell_does_not_escalate(income_protection):
    p = income_protection.Projection[3]
    assert p.escalation() == "none"
    assert p.esc_rate() == 0.0
    assert all(p.benefit_pp(t) == 2000.0 for t in (1, 13, 360))
    assert all(p.premium_pp(t) == 35.0 for t in (1, 13, 360))
    assert all(p.esc_lapse_factor(t) == 1.0 for t in (1, 13, 360))


def test_amount_payable_never_exceeds_the_chosen_benefit(income_protection):
    """AP <= B always: the base run's AP = B overstates outgo and understates nothing."""
    p = income_protection.Projection[1]
    assert p.amount_payable_pp(1) == p.benefit_pp(1)

    model = mx.read_model(MODEL_DIR, name="IP_UK_S_ap")
    try:
        model.Projection.ap_ratio = 0.85          # offsets biting
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.amount_payable_pp(1) == pytest.approx(0.85 * 2000.0, rel=1e-12)
        assert proj.amount_payable_pp(1) < proj.benefit_pp(1)
        assert proj.claims(50, "BENEFIT") < income_protection.Projection[1].claims(
            50, "BENEFIT")
    finally:
        model.close()


# ---------------------------------------------------------------------------
# What the product does not have


def test_death_and_lapse_pay_nothing(income_protection):
    """No death benefit on this composite, and no cash-in value at any time."""
    for point_id in income_protection.Data.model_point_table().index:
        df = income_protection.Projection[point_id].result_cf()
        assert (df["claims_death"] == 0.0).all()
        assert (df["claims_lapse"] == 0.0).all()


def test_there_is_no_account_value_or_surrender_machinery(income_protection):
    """The only state is the insured population itself."""
    names = set(income_protection.Projection.cells) | set(
        income_protection.Projection.refs)
    for absent in ("av_pp_at", "av_at", "cv_pp", "asset_share", "mvr",
                   "surr_charge_rate", "dyn_lapse_factor"):
        assert absent not in names


def test_invalid_enum_values_raise(uk_ip_claim):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        uk_ip_claim.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        uk_ip_claim.claims(1, "MATURITY")


# ---------------------------------------------------------------------------
# Discounting, which the rest of the library does not do


def test_nothing_in_result_cf_is_discounted(uk_ip_claim):
    """The discount companion is not part of the cash flow projection."""
    p = uk_ip_claim
    df = p.result_cf()
    assert df.loc[1, "claims_benefit"] == pytest.approx(1911.79, abs=PENNY)
    assert df.loc[1, "claims_benefit"] != pytest.approx(1907.09, abs=0.5)
    assert "disc_factor" not in df.columns


def test_the_disabled_life_annuity_factor(uk_ip_claim):
    """a_dis = pv_benefits / AP(1), the notes' claims-in-payment liability per unit."""
    p = uk_ip_claim
    assert p.annuity_dis() == pytest.approx(
        p.pv_benefits() / p.amount_payable_pp(1), rel=1e-12)
    assert p.pv_benefits() == pytest.approx(
        sum(p.claims(t, "BENEFIT") * p.disc_factor(t)
            for t in range(1, p.proj_len() + 1)), rel=1e-12)
    # A level-cover claim discounted at 3% is worth fewer months than it runs.
    assert 0 < p.annuity_dis() < p.proj_len()


def test_the_discount_rate_is_a_reference_not_a_valuation_basis(income_protection):
    """Flat 3% is the worked example's rate; a valuation uses the PRA risk-free curve."""
    model = mx.read_model(MODEL_DIR, name="IP_UK_S_disc")
    try:
        base = model.Projection[2].pv_benefits()
        model.Projection.disc_rate = 0.0
        model.Projection.clear_all()
        proj = model.Projection[2]
        assert proj.disc_factor(120) == 1.0
        assert proj.pv_benefits() > base          # undiscounted is the upper bound
        assert proj.pv_benefits() == pytest.approx(
            sum(proj.claims(t, "BENEFIT") for t in range(1, proj.proj_len() + 1)),
            rel=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_ip_claim):
    df = uk_ip_claim.result_cf()
    assert list(df.index) == list(range(1, 361))
    assert list(df.columns) == [
        "pols_if", "pols_active", "pols_sick", "premiums", "claims_benefit",
        "claims_death", "claims_lapse", "expenses", "net_cf",
    ]


def test_result_cf_rows_sum_to_net_cf(income_protection):
    """The cash flow columns are a decomposition of net_cf, not a selection from it."""
    df = income_protection.Projection[1].result_cf()
    outgo = df[["claims_benefit", "claims_death", "claims_lapse", "expenses"]].sum(
        axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)


def test_expenses_carry_the_claim_management_load(income_protection):
    """GBP 60 a year on every policy in force plus GBP 300 a year on every claim."""
    p = income_protection.Projection[1]
    for t in (1, 13, 100):
        expected = (60.0 / 12 * 1.03 ** (p.policy_year(t) - 1) * p.pols_if(t)
                    + 300.0 / 12 * 1.03 ** (p.policy_year(t) - 1) * p.pols_sick(t))
        assert p.expenses(t) == pytest.approx(expected, rel=1e-12)
    # On a cell that is wholly in claim, the claim-management load is five sixths of
    # the expense: GBP 300 a year against GBP 60 of maintenance on the same policy.
    claim = income_protection.Projection[2]
    assert claim.expenses(1) == pytest.approx((60.0 + 300.0) / 12, rel=1e-12)
    assert (300.0 / 12) / claim.expenses(1) == pytest.approx(300 / 360, rel=1e-12)


def test_model_docstring_describes_the_current_structure(income_protection):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = income_protection.doc
    assert "income protection" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "three-state" in doc
    assert "two-dimensional" in doc


def test_space_docstrings_carry_their_reference_material(income_protection):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = income_protection.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("pols_active", "pols_sick", "sick_cohorts", "pols_inception",
                  "inception_rate", "rec_rate", "annuity_dis"):
        assert cells in proj
    data = income_protection.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "inception_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_the_library_vocabulary(income_protection):
    """Names shared with lifelib and with the rest of this library must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "proj_len", "age", "pols_if",
        "pols_if_at", "pols_if_init", "pols_lapse", "pols_maturity", "mort_rate",
        "mort_rate_mth", "lapse_rate", "lapse_rate_mth", "premiums", "claims",
        "expenses", "expense_maint", "inflation_rate", "inflation_factor", "net_cf",
        "result_cf", "policy_year", "duration", "duration_mth",
    }
    names = set(income_protection.Projection.cells) | set(
        income_protection.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """The five input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "inception_table.csv",
                "termination_table.csv", "mort_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is what a production user does with a licensed IP11 basis: it drops in as a
    same-schema CSV with no formula change.
    """
    import pandas as pd

    src = MODEL_DIR.parent / "termination_table.csv"
    slower = pd.read_csv(src, index_col="claim_duration_year")
    slower["recovery_rate"] = slower["recovery_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="IP_UK_S_swap")
    try:
        alt_name = "termination_table_slow.csv"
        slower.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[2].pv_benefits()
            model.Data.termination_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Halving recovery rates lengthens every claim, so the annuity is worth more.
            assert model.Projection[2].pv_benefits() > base
            assert model.Projection[2].rec_rate(1) == pytest.approx(0.20, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="IP_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="IP_UK_S_rt")
    try:
        claim = reread.Projection[2]
        for m, row in WORKED_EXAMPLE.items():
            assert claim.pols_sick(m) == pytest.approx(row[0], abs=STATE)
            assert claim.claims(m, "BENEFIT") == pytest.approx(row[4], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
