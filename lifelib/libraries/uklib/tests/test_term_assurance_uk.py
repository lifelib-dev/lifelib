"""Golden and structural tests for Term_UK_S.

The golden values are the worked example in
products/term_assurance/technical-notes.md ("Worked example"), which projects the
anchor cell M35 / non-smoker / level shape / 25-year term / GBP 150,000 sum assured /
GBP 12.00 per month.  They are hard-coded here rather than pickled so that a reviewer
can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the penny, in-force to six
decimals.

The time index ``t`` is 0-based and counts policy **months** from issue: the worked
example's rows are ``t = 0, 1, 11, 12, 24``, the frame is ``range(proj_len())`` with
``proj_len() = term_mths() = 12 x policy_term()`` rows, and an in-force point opens at
``t = 12 x duration_inforce()``.

Beyond the worked example this module asserts the product facts the notes call out as
modelling pitfalls, because each of them is a way an implementation can look right and
be wrong:

* the annual decrement tables are converted with ``1 - (1 - r)^(1/12)``, which is what
  makes the in-force at every anniversary agree with an annual-grid roll-forward of the
  same table — the cheapest check there is on a monthly implementation;
* terminal illness is an acceleration, not a second decrement;
* family income benefit instalments are an annuity-certain and must not be decremented
  by mortality or lapse;
* the decreasing schedule's monthly convention is effective, not nominal, and its death
  benefit is the month's own balance rather than an annual grid's mid-year reading;
* a lapse pays nothing, unlike the US models with cash surrender values;
* and there are **no tail states** — nothing survives the end of the term.
"""
import contextlib

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


@contextlib.contextmanager
def _model_point_column(model, column, value):
    """Run the body with ``column`` of model point 1 overridden, on a temporary CSV.

    Editing the DataFrame in place will not do: the model re-reads the file, and a
    ``set_formula`` closure loses its cell when modelx recompiles the source.  Writing a
    variant CSV beside the model and repointing ``model_point_file`` goes through the
    model's own input machinery, which is also the point being demonstrated.
    """
    import pandas as pd

    src = MODEL_DIR.parent / "model_point_table.csv"
    table = pd.read_csv(src, index_col="point_id")
    table.loc[1, column] = value
    alt_name = f"model_point_table_{column}_{value}.csv"
    alt_path = MODEL_DIR.parent / alt_name
    table.to_csv(alt_path)
    try:
        model.Data.model_point_file = alt_name
        model.Data.clear_all()
        model.Projection.clear_all()
        yield
    finally:
        alt_path.unlink(missing_ok=True)


PENNY = 0.005         # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Term_UK_S"][0]

# t: (l(t), premiums, claims, claim expense, maint + initial expense, commission,
#     net CF) -- t = 0 is the issue month.
WORKED_EXAMPLE = {
    0:  (1.000000, 12.00, 6.88, 0.0115, 152.50, 216.00, -363.39),
    1:  (0.991213, 11.89, 6.82, 0.0114,   2.48,   0.00,    2.59),
    11: (0.907479, 10.89, 6.24, 0.0104,   2.27,   0.00,    2.37),
    12: (0.899505, 10.79, 6.75, 0.0112,   2.32,   0.27,    1.45),
    24: (0.827048,  9.92, 6.72, 0.0112,   2.19,   0.25,    0.75),
}

# Policy-year totals of the same projection, the notes' second table: policy year ->
# (premiums, claims, claim expense, expenses, commission, net CF).
WORKED_EXAMPLE_YEARS = {
    1: (137.24, 78.65, 0.13, 178.59, 216.00, -336.13),
    2: (124.67, 77.94, 0.13,  26.75,   3.12,   16.73),
    3: (115.19, 78.02, 0.13,  25.46,   2.88,    8.70),
}

# The notes' illustrative **annual** mortality vector for policy years 1-3.  Not a CMI
# table: the current UK assured lives tables are subscriber-only [R11].
WORKED_EXAMPLE_Q = (0.00055, 0.00060, 0.00065)

# The annual lapse table, policy years 1-5 then the clamped "6+" tail.
WORKED_EXAMPLE_W = (0.10, 0.08, 0.07, 0.05, 0.06)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_term_anchor, t):
    """Every cell of the notes' monthly table, to the displayed precision."""
    pols, prem, clm, clm_exp, exp, comm, net = WORKED_EXAMPLE[t]
    a = uk_term_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=PENNY)
    assert a.claims(t, "DEATH") == pytest.approx(clm, abs=PENNY)
    assert a.claim_expenses(t) == pytest.approx(clm_exp, abs=PENNY)
    assert a.expenses(t) == pytest.approx(exp, abs=PENNY)
    assert a.commissions(t) == pytest.approx(comm, abs=PENNY)
    assert a.net_cf(t) == pytest.approx(net, abs=PENNY)


@pytest.mark.parametrize("year", sorted(WORKED_EXAMPLE_YEARS))
def test_worked_example_policy_year_totals(uk_term_anchor, year):
    """The notes' policy-year totals: twelve monthly rows summed, to the penny.

    Premium income is materially below the annual grid's ``P_a x l(t)`` — 137.24 against
    144.00 in policy year 1 — because the monthly grid stops collecting from a policy
    the month it leaves.  That difference *is* the annual-in-advance bias, now removed
    rather than offset against the decreasing shape's mid-year benefit.
    """
    prem, clm, clm_exp, exp, comm, net = WORKED_EXAMPLE_YEARS[year]
    a = uk_term_anchor
    months = range(12 * (year - 1), 12 * year)
    assert sum(a.premiums(t) for t in months) == pytest.approx(prem, abs=PENNY)
    assert sum(a.claims(t, "DEATH") for t in months) == pytest.approx(clm, abs=PENNY)
    assert sum(a.claim_expenses(t) for t in months) == pytest.approx(clm_exp, abs=PENNY)
    assert sum(a.expenses(t) for t in months) == pytest.approx(exp, abs=PENNY)
    assert sum(a.commissions(t) for t in months) == pytest.approx(comm, abs=PENNY)
    assert sum(a.net_cf(t) for t in months) == pytest.approx(net, abs=PENNY)


def test_worked_example_mortality_vector(uk_term_anchor):
    """The annual rates 0.00055 / 0.00060 / 0.00065 apply through their policy years.

    ``mort_rate`` is the annual rate, constant across the twelve months of a policy
    year because the attained age advances on the anniversary; ``mort_rate_mth`` is what
    the projection decrements by.
    """
    a = uk_term_anchor
    for year, q in enumerate(WORKED_EXAMPLE_Q, start=1):
        for t in (12 * (year - 1), 12 * year - 1):
            assert a.mort_rate(t) == pytest.approx(q, rel=1e-12)
            assert a.mort_rate_mth(t) == pytest.approx(
                1 - (1 - q) ** (1 / 12), rel=1e-14)


def test_monthly_rates_compound_back_to_the_annual_table(uk_term_anchor):
    """1 - (1 - r)^(1/12) and not r/12: twelve months must rebuild the table rate.

    The nominal ``r/12`` is the pitfall the notes name.  It leaves
    ``(1 - r/12)^12 > 1 - r``, so it understates the decrement and breaks the
    anniversary identity below - which is the symptom to look for.  The effective
    monthly rate is correspondingly a little *above* ``r/12``, by more the larger the
    rate: negligible on a 0.055% mortality rate, visible on a 10% lapse rate.
    """
    a = uk_term_anchor
    for t in (0, 5, 12, 60, 299):
        assert (1 - a.mort_rate_mth(t)) ** 12 == pytest.approx(
            1 - a.mort_rate(t), rel=1e-14)
        assert (1 - a.lapse_rate_mth(t)) ** 12 == pytest.approx(
            1 - a.lapse_rate(t), rel=1e-14)
        assert a.mort_rate_mth(t) > a.mort_rate(t) / 12
        assert a.lapse_rate_mth(t) > a.lapse_rate(t) / 12
        # the nominal conversion would leave lives behind at the anniversary
        assert (1 - a.lapse_rate(t) / 12) ** 12 > 1 - a.lapse_rate(t)
    # 0.874% a month against a nominal 0.833%, on the 10% year-one lapse rate
    assert a.lapse_rate_mth(0) == pytest.approx(0.00874161, abs=5e-8)


def test_anniversary_inforce_matches_an_annual_grid_rollforward(uk_term_anchor):
    """l(12y) is exactly what an annual-step projection of the same table reports.

    Both decrements are constant within a policy year and both compound back to the
    annual rate over twelve months, so the monthly recursion reproduces
    ``prod (1 - q(u))(1 - w(u))`` at every anniversary.  The notes give
    ``l(12) = 0.899505`` and ``l(24) = 0.827048``, which are the annual model's own
    figures; this asserts the identity for the whole projection rather than two rows of
    it.
    """
    a = uk_term_anchor
    annual = 1.0
    for year in range(1, a.policy_term() + 1):
        t = 12 * (year - 1)
        annual *= (1 - a.mort_rate(t)) * (1 - a.lapse_rate(t))
        if 12 * year < a.proj_len():
            assert a.pols_if(12 * year) == pytest.approx(annual, rel=1e-12)
    assert a.pols_if(12) == pytest.approx(0.899505, abs=INFORCE)
    assert a.pols_if(24) == pytest.approx(0.827048, abs=INFORCE)


def test_worked_example_first_month_trace(uk_term_anchor):
    """The notes' first-month trace (t = 0), line by line.

    D(0) = 1.0 x q_m; claims = 150,000 x D(0) = 6.88; claim expense = 250 x D(0);
    expenses = E0 + e(0) = 150 + 30/12; commission = c0 = 1.5 x 144.
    """
    a = uk_term_anchor
    q_m = 1 - (1 - 0.00055) ** (1 / 12)
    assert a.pols_death(0) == pytest.approx(q_m, rel=1e-12)
    assert a.benefit_pp(0) == 150000.0
    assert a.premium_pp(0) == 12.00                # P_m, not the annualized premium
    assert a.comm_init_pp() == pytest.approx(216.00, abs=PENNY)   # 1.5 x 12 x P_m
    assert a.expenses(0) == pytest.approx(150.00 + 30.00 / 12, abs=PENNY)
    assert a.net_cf(0) == pytest.approx(
        12.00 - 150000 * q_m - 250 * q_m - 152.50 - 216.00, abs=1e-9)


def test_worked_example_inforce_update(uk_term_anchor):
    """l(1) = 1.0 x (1 - q_m) x (1 - w_m), the notes' monthly update step."""
    a = uk_term_anchor
    assert a.lapse_rate(0) == 0.10
    assert a.lapse_rate_mth(0) == pytest.approx(1 - 0.90 ** (1 / 12), rel=1e-14)
    assert a.pols_if(1) == pytest.approx(
        1.0 * (1 - a.mort_rate_mth(0)) * (1 - a.lapse_rate_mth(0)), rel=1e-14)
    assert a.pols_if(13) == pytest.approx(
        a.pols_if(12) * (1 - a.mort_rate_mth(12)) * (1 - a.lapse_rate_mth(12)),
        rel=1e-14)


def test_new_business_strain_then_thin_margins(uk_term_anchor):
    """The characteristic shape of guaranteed term, asserted rather than described.

    A deep strain in the issue month from upfront commission and acquisition expense
    against one month's premium, then positive margins while the level premium runs
    ahead of the rising mortality cost.
    """
    a = uk_term_anchor
    assert a.net_cf(0) < -300.0
    assert all(a.net_cf(t) > 0.0 for t in (1, 2, 12, 24))
    assert a.net_cf(a.proj_len() - 1) < 0.0    # mortality cost has overtaken by the end


# ---------------------------------------------------------------------------
# No tail states — the structural contrast with Term_US_S


def test_projection_ends_with_the_term(uk_term_anchor):
    """proj_len() is 12n, the term in months; nothing survives past it.

    Cover ceases at the end of the term with no maturity value, no renewal and no
    conversion.  A US-style post-level-term tail would show up here as a projection
    running past t = 299, the last month of the 25th and final policy year.
    """
    a = uk_term_anchor
    assert a.proj_len() == 300 == a.term_mths() == 12 * a.policy_term()
    assert a.proj_start() == 0                   # projected from issue
    assert a.age(0) == 35 and a.age(299) == 59   # attained age, first and final month
    assert a.age(11) == 35 and a.age(12) == 36   # advances on the anniversary
    assert a.pols_if(299) > 0.0
    assert a.pols_if(300) == 0.0                 # t = proj_len() is off the frame
    assert a.pols_if_at(299, "AFT_DECR") == 0.0
    assert len(a.result_cf()) == 300 == a.proj_len()


def test_no_post_level_term_machinery(term_assurance):
    """None of Term_US_S's tail cells exist here, and that is a product fact.

    A UK term policy expires; it does not jump to ART rates, shock-lapse, deteriorate
    or convert.  Importing that machinery materially misstates UK term liabilities,
    which is why its absence is asserted rather than left to inspection.
    """
    names = set(term_assurance.Projection.cells) | set(term_assurance.Projection.refs)
    for absent in ("phase", "jump_ratio", "shock_lapse_rate", "plt_mort_factor",
                   "conv_rate", "conv_elig", "conv_credits", "expiry_age"):
        assert absent not in names, f"{absent} is US post-level-term machinery"


def test_maturity_is_confined_to_the_final_month_and_pays_nothing(uk_term_anchor):
    """pols_maturity closes the roll-forward in the final month t = proj_len() - 1."""
    a = uk_term_anchor
    last = a.proj_len() - 1
    for t in range(last):
        assert a.pols_maturity(t) == 0.0
    assert a.pols_maturity(last) > 0.0
    # No maturity value: the only benefit kinds are DEATH and FIB, and neither fires
    # on the expiring survivors.
    assert a.claims(last) == pytest.approx(a.claims(last, "DEATH"), rel=1e-12)


def test_inforce_rollforward_closes(uk_term_anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + expiries, in every month."""
    a = uk_term_anchor
    assert a.check_pols_roll_fwd() is True
    for t in range(a.proj_len()):
        out = a.pols_death(t) + a.pols_lapse(t) + a.pols_maturity(t)
        assert a.pols_if(t) - a.pols_if(t + 1) == pytest.approx(out, abs=1e-12)


def test_death_is_decremented_before_lapse(uk_term_anchor):
    """The notes' processing order: lapses are taken from the survivors of mortality."""
    a = uk_term_anchor
    for t in (0, 4, 11, 60, 250):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate_mth(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t), rel=1e-14)


def test_inforce_is_a_decreasing_probability(uk_term_anchor):
    a = uk_term_anchor
    for t in range(a.proj_len() + 1):            # through the zero at t = proj_len()
        assert 0.0 <= a.pols_if(t) <= 1.0
        assert a.pols_if(t + 1) <= a.pols_if(t) + 1e-15


# ---------------------------------------------------------------------------
# The 1-based lapse table is read through policy_year(t)


def test_policy_year_is_the_one_based_label_of_the_zero_based_t(uk_term_anchor):
    """policy_year(t) = t // 12 + 1, the contractual label, never the index itself."""
    a = uk_term_anchor
    assert a.policy_year(0) == a.policy_year(11) == 1
    assert a.policy_year(12) == 2
    assert a.policy_year(299) == 25
    assert all(a.policy_year(t) == t // 12 + 1 for t in range(a.proj_len()))
    assert all(a.duration(t) == t // 12 for t in range(a.proj_len()))
    assert all(a.duration_mth(t) == t for t in range(a.proj_len()))


def test_the_lapse_table_keeps_its_one_based_key_and_is_read_through_policy_year(
        term_assurance, uk_term_anchor):
    """The CSV key is a contractual policy year, so the reader maps through t + 1.

    lapse_table.csv holds policy years 1...6 at 10 / 8 / 7 / 5 / 6 / 4 %, the last row
    being the clamped "6 and later" tail.  The index shift lives entirely in
    policy_year(t); the file itself was not re-keyed.
    """
    a = uk_term_anchor
    assert list(term_assurance.Data.lapse_table().index) == [1, 2, 3, 4, 5, 6]
    for year, rate in enumerate(WORKED_EXAMPLE_W, start=1):
        # the same annual rate across all twelve months of the policy year
        assert a.lapse_rate_base(12 * (year - 1)) == rate     # CSV row policy_year
        assert a.lapse_rate_base(12 * year - 1) == rate
    # the clamped "6+" row applies from policy year 6 to the end of the frame
    assert (a.lapse_rate_base(60) == a.lapse_rate_base(120)
            == a.lapse_rate_base(a.proj_len() - 1) == 0.04)


# ---------------------------------------------------------------------------
# Lapse pays nothing


def test_lapse_pays_nothing(term_assurance):
    """No surrender or paid-up value at any duration, on any shape.

    The notes list a non-zero lapse row as a pitfall imported from US models with cash
    surrender values.  The zero column is published rather than dropped so the product
    fact is stated.
    """
    for point_id in term_assurance.Data.model_point_table().index:
        proj = term_assurance.Projection[point_id]
        df = proj.result_cf()
        assert (df["claims_lapse"] == 0.0).all()
        assert all(proj.claims(t, "LAPSE") == 0.0
                   for t in range(proj.proj_start(), proj.proj_len()))


# ---------------------------------------------------------------------------
# Terminal illness is one decrement


def test_terminal_illness_is_not_a_second_decrement(term_assurance):
    """One decrement, one payment: there is no separate TI rate anywhere in the model.

    The 16-Series assured lives tables the shipped table proxies already include
    terminal illness [R10], so a separate TI decrement double-counts claims.
    """
    names = set(term_assurance.Projection.cells) | set(term_assurance.Projection.refs)
    assert not [n for n in names if n.startswith("ti_") or "_ti_" in n]
    doc = term_assurance.Projection.doc
    assert "acceleration" in doc


# ---------------------------------------------------------------------------
# The decreasing shape


def test_decreasing_schedule_anchor(term_assurance):
    """B(60) = GBP 134,588, the notes' validation anchor for the amortization."""
    p = term_assurance.Projection[2]
    assert p.shape() == "decreasing"
    assert p.benefit_sched(60) == pytest.approx(134588.0, abs=0.5)
    assert p.benefit_sched(0) == pytest.approx(p.sum_assured(), rel=1e-12)
    assert p.benefit_sched(p.term_mths()) == pytest.approx(0.0, abs=1e-9)


def test_decreasing_monthly_convention_is_effective_not_nominal(term_assurance):
    """j_m = (1+j)^(1/12) - 1, not j/12 — the notes state the convention as a pitfall.

    The two agree at whole years and differ in between; at k = 60 (a whole year) they
    differ because the *horizon* discounting differs, by about GBP 310 on the anchor
    cell.  A test that only checked B(0) and B(N) would not see it.
    """
    p = term_assurance.Projection[2]
    j = p.sched_rate()
    assert p.sched_rate_mth() == pytest.approx((1 + j) ** (1 / 12) - 1, rel=1e-14)
    assert p.sched_rate_mth() != pytest.approx(j / 12, rel=1e-6)

    jm_nominal = j / 12
    n_m = p.term_mths()
    nominal_b60 = p.sum_assured() * (
        (1 + jm_nominal) ** n_m - (1 + jm_nominal) ** 60) / (
            (1 + jm_nominal) ** n_m - 1)
    assert abs(nominal_b60 - p.benefit_sched(60)) > 250.0


def test_decreasing_whole_year_identity(term_assurance):
    """(1+j_m)^12 = 1+j, so B(12y), the balance after y whole years, closes annually."""
    p = term_assurance.Projection[2]
    j = p.sched_rate()
    n = p.policy_term()
    for y in (1, 5, 10):
        annual = p.sum_assured() * ((1 + j) ** n - (1 + j) ** y) / ((1 + j) ** n - 1)
        assert p.benefit_sched(12 * y) == pytest.approx(annual, rel=1e-12)


def test_decreasing_death_benefit_is_the_months_own_balance(term_assurance):
    """DB(t) = B(t) exactly: the schedule steps down monthly and so does the benefit.

    The annual grid had to read this as the mid-year balance ``B(12t + 6)``; on a
    monthly grid there is nothing to approximate, and carrying the mid-year correction
    across would double-count it.  ``benefit_pp(0)`` is the full sum assured, where the
    annual grid's first-year benefit was already six months down the schedule.
    """
    p = term_assurance.Projection[2]
    for t in (0, 1, 60, 239, 299):
        assert p.benefit_pp(t) == pytest.approx(p.benefit_sched(t), rel=1e-14)
    assert p.benefit_pp(0) == pytest.approx(p.sum_assured(), rel=1e-12)
    assert p.benefit_pp(60) == pytest.approx(134588.0, abs=0.5)   # five years in
    mid_year = p.benefit_sched(6)                 # what an annual grid would have used
    assert p.benefit_pp(0) > mid_year
    # monotone down to nil at the end of the term
    assert all(p.benefit_pp(t + 1) < p.benefit_pp(t) for t in range(0, 299, 37))


# ---------------------------------------------------------------------------
# The family income benefit ledger


def test_fib_ledger_closes_against_an_independent_rebuild(term_assurance):
    """check_fib_ledger rebuilds the month's instalments straight off the death vector."""
    p = term_assurance.Projection[3]
    assert p.shape() == "fib"
    assert p.check_fib_ledger() is True
    for t in range(p.proj_len()):
        assert p.check_fib_ledger_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_fib_total_is_the_annuity_certain_total(term_assurance):
    """A death in month s pays exactly N - s instalments, the contractual count.

    Summed over the projection this is the whole liability, and it is the identity an
    implementation that pays only the month-of-death instalment fails.  On the monthly
    grid there is no rounding left in it: the annual grid's "six in the year of death,
    twelve thereafter" was an approximation to this.
    """
    p = term_assurance.Projection[3]
    n_m, income = p.term_mths(), p.fib_income()
    total = sum(p.claims(t, "FIB") for t in range(n_m))
    built = sum(p.pols_death(s) * income * (n_m - s) for s in range(n_m))
    assert total == pytest.approx(built, rel=1e-12)
    assert n_m == 300 == p.proj_len()


def test_fib_stream_is_not_decremented_by_mortality_or_lapse(term_assurance):
    """The ledger is a running total of deaths, untouched by later decrements.

    This is the notes' pitfall: the instalments are an annuity-certain once the claim is
    admitted, so only *new* claims carry l(t).
    """
    p = term_assurance.Projection[3]
    for t in range(1, p.proj_len()):
        assert p.fib_cum(t) == pytest.approx(
            p.fib_cum(t - 1) + p.pols_death(t - 1), abs=1e-15)
        assert p.fib_cum(t) >= p.fib_cum(t - 1)   # never falls
    assert p.fib_cum(0) == 0.0
    # every stream in payment, the month's new claims included, pays one instalment
    for t in (0, 1, 120, 299):
        assert p.claims(t, "FIB") == pytest.approx(
            p.fib_income() * (p.pols_death(t) + p.fib_cum(t)), rel=1e-14)


def test_fib_pays_no_lump_sum_when_uncommuted(term_assurance):
    """With take-up at zero the whole liability runs through claims(t, "FIB")."""
    p = term_assurance.Projection[3]
    assert p.fib_commute_rate() == 0.0
    assert all(p.claims(t, "DEATH") == 0.0 for t in range(p.proj_len()))
    assert any(p.claims(t, "FIB") > 0.0 for t in range(p.proj_len()))


def test_fib_commutation_replaces_the_stream_with_a_lump_sum(term_assurance):
    """Model point 4 is point 3 with take-up at 100%: all lump sum, no instalments."""
    p3, p4 = term_assurance.Projection[3], term_assurance.Projection[4]
    assert p4.fib_commute_rate() == 1.0
    assert all(p4.claims(t, "FIB") == 0.0 for t in range(p4.proj_len()))
    assert any(p4.claims(t, "DEATH") > 0.0 for t in range(p4.proj_len()))
    # a(300) at r_c = 3%: the value of the instalments a death in the issue month
    # (t = 0, so k = 0 and N - k = 300) would generate.  The annual grid had to place
    # that death at k = 6 and take a(294) instead.
    assert p4.fib_commute_pp(0) == pytest.approx(1000.0 * 211.815608, abs=0.01)
    assert p4.fib_commute_pp(0) == pytest.approx(
        1000.0 * p4.annuity_certain_factor(300), rel=1e-14)
    # Commuting at 3% is worth less than paying the instalments out undiscounted.
    tot3 = sum(p3.claims(t) for t in range(p3.proj_len()))
    tot4 = sum(p4.claims(t) for t in range(p4.proj_len()))
    assert tot4 < tot3


def test_annuity_certain_factor(term_assurance):
    """a(m) = [1 - (1+r_c)^(-m/12)] / [(1+r_c)^(1/12) - 1], instalments in arrears."""
    p = term_assurance.Projection[4]
    r = 0.03
    for m in (12, 120, 294, 300):
        expected = (1 - (1 + r) ** (-m / 12)) / ((1 + r) ** (1 / 12) - 1)
        assert p.annuity_certain_factor(m) == pytest.approx(expected, rel=1e-12)
    assert p.annuity_certain_factor(0) == 0.0
    assert p.annuity_certain_factor(-5) == 0.0


def test_fib_premiums_stop_at_death_though_instalments_do_not(term_assurance):
    """Premium income always carries l(t); the FIB ledger never touches it."""
    p = term_assurance.Projection[3]
    for t in (0, 9, 120, 299):
        assert p.premiums(t) == pytest.approx(p.premium_pp(t) * p.pols_if(t), rel=1e-14)
    # the ledger grows while the in-force falls, so the two cannot be the same weight
    assert p.fib_cum(299) > p.fib_cum(120) and p.pols_if(299) < p.pols_if(120)


# ---------------------------------------------------------------------------
# Premium mode, which the monthly grid can see


def test_premium_mode_is_live_on_the_monthly_grid(term_assurance):
    """Monthly collects P_m every month; annual collects 12 P_m in the first of each.

    On the annual grid the two modes annualized to the same number and ``premium_mode``
    was inert.  Here the timing differs within the policy year, which is a real
    difference in income: the annual payer's premium arrives earlier and is collected in
    full from a life that may leave during the year.  The amount due over a policy year
    is the same, so the *per-policy* premium sums to ``12 P_m`` either way.
    """
    model = mx.read_model(MODEL_DIR, name="Term_UK_S_mode")
    try:
        assert set(model.Data.model_point_table()["premium_mode"]) == {"monthly"}
        monthly = model.Projection[1]
        assert all(monthly.premium_pp(t) == 12.00 for t in (0, 1, 11, 12, 299))
        monthly_year_one = sum(monthly.premiums(t) for t in range(12))

        with _model_point_column(model, "premium_mode", "annual"):
            annual = model.Projection[1]
            assert annual.premium_pp(0) == pytest.approx(144.00, rel=1e-12)
            assert all(annual.premium_pp(t) == 0.0 for t in range(1, 12))
            assert annual.premium_pp(12) == pytest.approx(144.00, rel=1e-12)
            # The amount due over a policy year is the same in either mode.
            assert sum(annual.premium_pp(t) for t in range(12)) == pytest.approx(
                12 * 12.00, rel=1e-12)
            # Collected earlier and from a larger in-force, so income is higher.
            assert sum(annual.premiums(t) for t in range(12)) > monthly_year_one
    finally:
        model.close()


def test_invalid_premium_mode_raises(term_assurance):
    """The enum validates rather than silently falling through to the monthly branch."""
    model = mx.read_model(MODEL_DIR, name="Term_UK_S_badmode")
    try:
        with _model_point_column(model, "premium_mode", "weekly"):
            with pytest.raises(FormulaError):
                model.Projection[1].premium_pp(0)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Indexation


def test_indexation_compounds_cover_and_premium_at_the_notes_rates(term_assurance):
    """Flat 3% RPI: cover x 1.03 and premium x 1.045, the x1.5 premium factor.

    The increase is an anniversary event, so both factors step once a policy year and
    are level through its twelve months.
    """
    p = term_assurance.Projection[5]
    assert p.indexation() is True
    assert p.idx_increase() == pytest.approx(0.03, rel=1e-12)
    for year in (0, 1, 2):
        for t in (12 * year, 12 * year + 11):
            assert p.idx_factor(t) == pytest.approx(1.03 ** year, rel=1e-12)
            assert p.idx_prem_factor(t) == pytest.approx(1.045 ** year, rel=1e-12)
    assert p.idx_factor(11) != p.idx_factor(12)   # it does step, on the anniversary
    assert p.benefit_pp(24) == pytest.approx(150000.0 * 1.03 ** 2, rel=1e-12)
    assert p.premium_pp(24) == pytest.approx(12.0 * 1.045 ** 2, rel=1e-12)


def test_indexation_caps(term_assurance):
    """Cover increase capped at 10% and the premium increase at 15%.

    ``Projection.clear_all()`` discards the ItemSpaces along with their caches, so the
    ItemSpace is re-fetched after each change of Reference rather than held across it.
    """
    model = mx.read_model(MODEL_DIR, name="Term_UK_S_idxcap")
    try:
        model.Projection.rpi_rate = 0.25          # far above both caps
        model.Projection.clear_all()
        proj = model.Projection[5]
        assert proj.idx_increase() == pytest.approx(0.10, rel=1e-12)
        # 1.5 x 10% = 15%, exactly at the premium cap, after the first anniversary.
        assert proj.idx_prem_factor(12) == pytest.approx(1.15, rel=1e-12)
        model.Projection.rpi_rate = -0.02         # deflation floors the increase at 0
        model.Projection.clear_all()
        proj = model.Projection[5]
        assert proj.idx_increase() == 0.0
        assert proj.idx_factor(48) == 1.0
    finally:
        model.close()


def test_indexation_is_off_on_the_other_model_points(term_assurance):
    """Unelected, both factors stay at 1 for the whole projection."""
    p = term_assurance.Projection[1]
    assert p.indexation() is False
    assert all(p.idx_factor(t) == 1.0 and p.idx_prem_factor(t) == 1.0
               for t in range(p.proj_len()))


def test_indexation_is_restricted_to_the_level_shape(term_assurance):
    """No fetched insurer offers indexed decreasing cover, so the combination is barred."""
    model = mx.read_model(MODEL_DIR, name="Term_UK_S_idxshape")
    try:
        table = model.Data.model_point_table()
        assert not (table["indexation"] & (table["shape"] != "level")).any()
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Joint first death


def test_joint_first_death_is_one_policy_with_one_decrement(term_assurance):
    """q_joint = 1 - (1-q1)(1-q2): the policy pays once and ends."""
    p = term_assurance.Projection[6]
    assert p.is_joint() is True
    assert p.age_at_entry(2) == 33 and p.sex(2) == "F"
    for t in (0, 7, 120, 250):
        q1, q2 = p.mort_rate_life(t, 1), p.mort_rate_life(t, 2)
        assert p.mort_rate(t) == pytest.approx(1 - (1 - q1) * (1 - q2), rel=1e-14)
        assert p.mort_rate(t) < q1 + q2           # not the sum of the two rates
    assert p.check_pols_roll_fwd() is True


def test_single_life_collapses_to_the_first_life(term_assurance):
    p = term_assurance.Projection[1]
    assert p.is_joint() is False
    for t in (0, 9, 120):
        assert p.mort_rate(t) == p.mort_rate_life(t, 1)
    with pytest.raises(FormulaError):
        p.age_at_entry(2)          # modelx wraps the formula's ValueError


# ---------------------------------------------------------------------------
# The two mortality bases


def test_applied_basis_takes_the_table_as_it_stands(uk_term_anchor):
    """No select factor and no proxy scaling on the applied basis."""
    a = uk_term_anchor
    assert a.mort_basis() == "applied"
    for t in (0, 3, 19, 120, 299):
        assert a.mort_rate(t) == pytest.approx(a.mort_rate_base(t), rel=1e-14)


def test_select_basis_applies_the_select_factor_and_the_proxy_scaling(term_assurance):
    """table x select_factor(duration) x 0.75, with a 5-year select period."""
    p = term_assurance.Projection[7]
    assert p.mort_basis() == "select"
    for t in (0, 11, 12, 48, 60, 120):
        assert p.mort_rate(t) == pytest.approx(
            p.mort_rate_base(t) * p.select_factor(t) * 0.75, rel=1e-14)
    # The select discount wears off over five years and is gone from duration 5.  The
    # table key is duration(t) = t // 12, so the factor is level within a policy year.
    assert p.select_factor(0) == p.select_factor(11) == 0.55      # duration 0
    assert p.select_factor(12) == 0.65                            # duration 1
    assert p.select_factor(48) == p.select_factor(59) == 0.93     # duration 4
    assert p.select_factor(60) == 1.00                            # duration 5, ultimate
    assert p.select_factor(239) == 1.00
    assert p.mort_rate(0) < p.mort_rate_base(0)


def test_the_two_bases_disagree_and_that_is_shipped_not_resolved(term_assurance):
    """Both readings are standardizations; the gap must not be closed silently.

    The notes' three illustrative applied rates rise at 9% a year, which no graduated
    select structure produces, so neither basis is derivable from the other.
    """
    model = mx.read_model(MODEL_DIR, name="Term_UK_S_bases")
    try:
        proj = model.Projection[1]
        applied = proj.mort_rate(0)
        table = model.Data.mort_table()
        select = table.loc[("M", "N", 35), "mort_rate"] * 0.55 * 0.75
        assert applied == pytest.approx(0.00055, rel=1e-12)
        assert select == pytest.approx(0.00055 * 0.55 * 0.75, rel=1e-12)
        assert abs(applied - select) > 1e-4
    finally:
        model.close()


def test_invalid_enum_values_raise(term_assurance):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    p = term_assurance.Projection[1]
    with pytest.raises(FormulaError):
        p.pols_if_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        p.claims(0, "SURRENDER")


# ---------------------------------------------------------------------------
# Modules that are off in the base run


def test_selective_lapsation_is_off_and_works_when_switched_on(term_assurance):
    """q_eff = q (1 + lambda max(0, w_cum - w_ref)); lambda = 0 in the base run."""
    p = term_assurance.Projection[1]
    assert all(p.sel_lapse_factor(t) == 1.0 for t in range(p.proj_len()))
    assert p.lapse_cum(0) == 0.0
    assert p.lapse_cum(48) > 0.0

    model = mx.read_model(MODEL_DIR, name="Term_UK_S_sel")
    try:
        base_late = model.Projection[1].mort_rate(240)
        model.Projection.sel_lapse_lambda = 0.25
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.sel_lapse_factor(0) == 1.0            # nothing has lapsed yet
        assert proj.sel_lapse_factor(240) > 1.0           # w_cum has passed w_ref
        assert proj.mort_rate(240) > base_late
    finally:
        model.close()


def test_rebroking_is_off_and_works_when_switched_on(term_assurance):
    """M_reb = min(2, max(1, P_inforce / P_market)); the ratio is 1 in the base run."""
    p = term_assurance.Projection[1]
    assert all(p.rebroke_factor(t) == 1.0 for t in range(p.proj_len()))
    assert p.lapse_rate(0) == p.lapse_rate_base(0)

    model = mx.read_model(MODEL_DIR, name="Term_UK_S_reb")
    try:
        model.Projection.premium_market_ratio = 1.5
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.rebroke_factor(0) == pytest.approx(1.5)
        assert proj.lapse_rate(24) == pytest.approx(0.07 * 1.5)  # policy year 3
        model.Projection.premium_market_ratio = 5.0       # above the cap
        model.Projection.clear_all()
        assert model.Projection[1].rebroke_factor(0) == 2.0
        model.Projection.premium_market_ratio = 0.4       # cheaper in force, no rebroking
        model.Projection.clear_all()
        assert model.Projection[1].rebroke_factor(0) == 1.0
    finally:
        model.close()


def test_commission_clawback_is_off_and_works_when_switched_on(term_assurance):
    """Linear over 48 months; off by default, so commission is never negative.

    The monthly grid counts months in force exactly - ``t + 1`` at the end of month
    ``t`` - where the annual grid could only step twelve at a time, so the run-off is a
    straight line rather than four steps.
    """
    p = term_assurance.Projection[1]
    assert all(p.comm_clawback(t) == 0.0 for t in range(p.proj_len()))

    model = mx.read_model(MODEL_DIR, name="Term_UK_S_claw")
    try:
        model.Projection.clawback_mths = 48
        model.Projection.clear_all()
        proj = model.Projection[1]
        # A lapse at the end of the issue month has 1 month in force: 47 of 48 months
        # remaining, so 47/48 of c0 per lapsed policy.
        assert proj.comm_clawback(0) == pytest.approx(
            216.0 * 47 / 48 * proj.pols_lapse(0), rel=1e-12)
        # A lapse at the end of month 11 has 12 months in force: 36 of 48 remaining,
        # which is the only point the annual grid could see.
        assert proj.comm_clawback(11) == pytest.approx(
            216.0 * 0.75 * proj.pols_lapse(11), rel=1e-12)
        assert proj.comm_clawback(47) == 0.0              # window closed at 48 months
        assert proj.comm_clawback(48) == 0.0
        assert proj.commissions(12) < 0.025 * proj.premiums(12)
    finally:
        model.close()


def test_waiver_of_premium_is_off_and_works_when_switched_on(term_assurance):
    """The waived fraction is a two-state chain; zero unless the rider is in force.

    The 26-week deferred period is six months on this grid, carried explicitly, so
    nobody is waived before ``t = 7``: the first month whose entrants became
    incapacitated six months earlier.  An annual grid could only round that to a year.
    """
    p1 = term_assurance.Projection[1]
    assert p1.wop() is False
    assert all(p1.wop_waived_frac(t) == 0.0 for t in range(p1.proj_len()))
    assert all(p1.pols_payer(t) == p1.pols_if(t) for t in range(p1.proj_len()))

    p7 = term_assurance.Projection[7]
    assert p7.wop() is True
    inc_m = 1 - (1 - 0.004) ** (1 / 12)
    rec_m = 1 - (1 - 0.35) ** (1 / 12)
    assert p7.wop_inc_rate_mth() == pytest.approx(inc_m, rel=1e-14)
    assert p7.wop_rec_rate_mth() == pytest.approx(rec_m, rel=1e-14)
    assert all(p7.wop_waived_frac(t) == 0.0 for t in range(7))   # deferred period
    assert p7.wop_waived_frac(7) == pytest.approx(
        inc_m * (1 - rec_m) ** 6, rel=1e-12)
    assert p7.wop_waived_frac(8) > p7.wop_waived_frac(7)  # not yet at equilibrium
    assert p7.pols_payer(24) < p7.pols_if(24)
    # The rider carries a premium loading, also [std]; the premium is monthly.
    assert p7.premium_pp(0) == pytest.approx(45.00 * 1.05, rel=1e-12)


def test_waived_fraction_converges_below_one(term_assurance):
    """The chain's equilibrium, with the deferred period's survival factor on entry.

    ``u rec_m = inc_m (1 - u)(1 - rec_m)^defer`` at rest, so the lag lowers the resting
    waived fraction below the deferred-period-free ``inc / (inc + rec)``.
    """
    p = term_assurance.Projection[7]
    inc_m = 1 - (1 - 0.004) ** (1 / 12)
    rec_m = 1 - (1 - 0.35) ** (1 / 12)
    survive = (1 - rec_m) ** 6
    equilibrium = inc_m * survive / (rec_m + inc_m * survive)
    assert p.wop_waived_frac(p.proj_len() - 1) == pytest.approx(equilibrium, abs=1e-5)
    assert equilibrium < 0.004 / (0.004 + 0.35)   # the lag costs waived months


# ---------------------------------------------------------------------------
# In-force model points


def test_an_inforce_model_point_starts_at_its_duration(term_assurance):
    """duration_inforce = 5 years means the projection opens at t = 60, policy year 6.

    The model point carries the elapsed count in **years**, the unit a contract speaks
    in, and proj_start() converts it: 12 x duration_inforce().  proj_len() keeps the
    term in months, so the frame is range(60, 300), 240 rows.  An in-force policy never
    sees the acquisition expense or the initial commission, but does pay renewal
    commission, and its expense inflation is measured from issue.
    """
    p = term_assurance.Projection[8]
    assert p.duration_inforce() == 5 and p.proj_start() == 60
    assert p.proj_len() == 300 == 12 * p.policy_term()
    df = p.result_cf()
    assert list(df.index) == list(range(60, 300))
    assert len(df) == p.proj_len() - p.proj_start() == 240
    assert p.pols_if(59) == 0.0 and p.pols_if(60) == 1.0
    assert p.expenses(60) == pytest.approx(
        30.0 / 12 * 1.03 ** 5, rel=1e-12)                            # no E0
    assert p.commissions(60) == pytest.approx(0.025 * p.premiums(60), rel=1e-12)
    assert p.lapse_cum(60) == 0.0
    assert p.check_pols_roll_fwd() is True


def test_an_inforce_point_uses_the_same_rates_as_the_issued_one(term_assurance):
    """Duration is measured from entry, not from the start of the projection."""
    p1, p8 = term_assurance.Projection[1], term_assurance.Projection[8]
    for t in range(60, 300, 17):
        assert p8.mort_rate(t) == p1.mort_rate(t)
        assert p8.lapse_rate(t) == p1.lapse_rate(t)
        assert p8.duration(t) == t // 12 == p1.duration(t)
        assert p8.age(t) == p1.age(t)


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_term_anchor):
    """One row per month t = 0 .. proj_len() - 1, lifelib's range(proj_len())."""
    a = uk_term_anchor
    df = a.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(a.proj_len())) == list(range(300))
    assert df.index[0] == 0 and df.index[-1] == a.proj_len() - 1
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_fib", "claims_lapse",
        "claim_expenses", "expenses", "commissions", "net_cf",
    ]
    assert df.loc[0, "pols_if"] == a.pols_if_init()
    assert df.loc[0, "net_cf"] == pytest.approx(-363.39, abs=PENNY)
    assert list(a.result_pols().index) == list(df.index)
    # the published decrement columns are the monthly rates the projection applies
    assert "mort_rate_mth" in a.result_pols().columns
    assert "lapse_rate_mth" in a.result_pols().columns


def test_result_cf_rows_sum_to_net_cf(uk_term_anchor):
    """The cash flow columns are a decomposition of net_cf, not a selection from it."""
    df = uk_term_anchor.result_cf()
    outgo = df[["claims_death", "claims_fib", "claims_lapse", "claim_expenses",
                "expenses", "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)


def test_net_cf_carries_the_notes_own_sign(term_assurance):
    """The notes write "+ = inflow", which is already the library-wide convention.

    So there is no outgo-positive liability_cf companion here, unlike the whole life and
    payout annuity models whose notes print the other sign.
    """
    assert "liability_cf" not in term_assurance.Projection.cells
    assert term_assurance.Projection[1].net_cf(1) > 0.0    # a positive-margin month


def test_model_docstring_describes_the_current_structure(term_assurance):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = term_assurance.doc
    assert "term assurance" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "no maturity value, no renewal and no conversion" in doc
    assert "Monthly steps" in doc                # the projection basis, not annual


def test_space_docstrings_carry_their_reference_material(term_assurance):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = term_assurance.Projection.doc
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    for cells in ("pols_if", "pols_maturity", "fib_cum", "benefit_sched",
                  "select_factor", "mort_basis", "policy_year", "mort_rate_mth",
                  "lapse_rate_mth", "duration_mth"):
        assert cells in proj
    data = term_assurance.Data.doc
    assert "TradLife_A" in data                  # the pattern it follows
    for cells in ("input_dir", "mort_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_basicterm_s(term_assurance):
    """Names shared with lifelib's basiclife/BasicTerm_S must not drift apart."""
    shared = {
        "model_point", "age_at_entry", "sex", "sum_assured", "policy_term",
        "proj_len", "age", "pols_if", "pols_if_init", "pols_death", "pols_lapse",
        "pols_maturity", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "duration", "duration_mth", "premiums", "claims",
        "expenses", "expense_acq", "expense_maint", "inflation_rate",
        "inflation_factor", "commissions", "net_cf", "result_cf",
    }
    names = set(term_assurance.Projection.cells) | set(term_assurance.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """The four input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv",
                "select_factor_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Every row says where it came from; only three are the notes' own values.

    The shipped table is a [std] construction and not a published table.  Marking the
    rows is what stops it being mistaken for one.
    """
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert table["provenance"].notna().all()
    worked = table[table["provenance"] == "worked example [std]"]
    assert len(worked) == 3
    assert sorted(worked["age"]) == [35, 36, 37]
    assert sorted(worked["mort_rate"]) == list(WORKED_EXAMPLE_Q)
    assert set(worked["sex"]) == {"M"} and set(worked["smoker"]) == {"N"}


def test_projection_shares_one_data_space(term_assurance):
    """`data` resolves to the single Data Space from every ItemSpace."""
    assert term_assurance.Projection[1].data is term_assurance.Data
    assert term_assurance.Projection[1].data is term_assurance.Projection[3].data


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a production
    user does with the licensed CMI tables: they drop in as same-schema CSVs with no
    formula change.

    The swapped table doubles every rate, and the **annual** ``mort_rate`` doubles with
    it exactly.  The monthly claim does not quite double, and that is the monthly grid
    rather than a wiring fault: ``1 - (1 - 2q)^(1/12)`` is slightly more than twice
    ``1 - (1 - q)^(1/12)``, by about a q-sized relative amount.  Asserting the annual
    rate exactly and the claim to a tolerance that size keeps the check sharp without
    asserting something arithmetically false.
    """
    import pandas as pd

    src = MODEL_DIR.parent / "mort_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "smoker", "age"])
    doubled["mort_rate"] = doubled["mort_rate"] * 2

    model = mx.read_model(MODEL_DIR, name="Term_UK_S_swap")
    try:
        alt_name = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base_rate = model.Projection[1].mort_rate(0)
            base_claim = model.Projection[1].claims(0, "DEATH")
            model.Data.mort_table_file = alt_name      # repoint the Reference
            model.Data.clear_all()
            model.Projection.clear_all()
            proj = model.Projection[1]
            assert proj.mort_rate(0) == pytest.approx(2 * base_rate, rel=1e-12)
            assert proj.claims(0, "DEATH") == pytest.approx(
                2 * base_claim, rel=1e-3)
            assert proj.claims(0, "DEATH") > 2 * base_claim
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Term_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Term_UK_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[6], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
