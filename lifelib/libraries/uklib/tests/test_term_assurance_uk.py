"""Golden and structural tests for Term_UK_A.

The golden values are the worked example in
products/term_assurance/technical-notes.md ("Worked example"), which projects the
anchor cell M35 / non-smoker / level shape / 25-year term / GBP 150,000 sum assured /
GBP 12.00 per month.  They are hard-coded here rather than pickled so that a reviewer
can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the penny, in-force to six
decimals.

Beyond the worked example this module asserts the product facts the notes call out as
modelling pitfalls, because each of them is a way an implementation can look right and
be wrong:

* terminal illness is an acceleration, not a second decrement;
* family income benefit instalments are an annuity-certain and must not be decremented
  by mortality or lapse;
* the decreasing schedule's monthly convention is effective, not nominal;
* a lapse pays nothing, unlike the US models with cash surrender values;
* and there are **no tail states** — nothing survives the end of the term.
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
INFORCE = 5e-7        # in-force displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Term_UK_A"][0]

# t: (l(t), premiums, claims, claim expense, maint + initial expense, commission,
#     net CF, l(t+1))
WORKED_EXAMPLE = {
    1: (1.000000, 144.00, 82.50, 0.14, 180.00, 216.00, -334.64, 0.899505),
    2: (0.899505, 129.53, 80.96, 0.13,  27.79,   3.24,   17.41, 0.827048),
    3: (0.827048, 119.09, 80.64, 0.13,  26.32,   2.98,    9.02, 0.768655),
}

# The notes' illustrative mortality vector, q(1) .. q(3).  Not a CMI table: the current
# UK assured lives tables are subscriber-only [R11].
WORKED_EXAMPLE_Q = (0.00055, 0.00060, 0.00065)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_term_anchor, t):
    """Every cell of the notes' three-row table, to the displayed precision."""
    pols, prem, clm, clm_exp, exp, comm, net, pols_next = WORKED_EXAMPLE[t]
    a = uk_term_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=PENNY)
    assert a.claims(t, "DEATH") == pytest.approx(clm, abs=PENNY)
    assert a.claim_expenses(t) == pytest.approx(clm_exp, abs=PENNY)
    assert a.expenses(t) == pytest.approx(exp, abs=PENNY)
    assert a.commissions(t) == pytest.approx(comm, abs=PENNY)
    assert a.net_cf(t) == pytest.approx(net, abs=PENNY)
    assert a.pols_if(t + 1) == pytest.approx(pols_next, abs=INFORCE)


def test_worked_example_mortality_vector(uk_term_anchor):
    """q(1..3) = 0.00055 / 0.00060 / 0.00065, the notes' illustrative values."""
    for t, q in enumerate(WORKED_EXAMPLE_Q, start=1):
        assert uk_term_anchor.mort_rate(t) == pytest.approx(q, rel=1e-12)


def test_worked_example_year_one_trace(uk_term_anchor):
    """The notes' year-one trace, line by line.

    D(1) = 1.0 x 0.00055; claims = 150,000 x D(1) = 82.50; claim expense = 250 x D(1);
    expenses = E0 + e(1) = 150 + 30; commission = c0 = 1.5 x 144.
    """
    a = uk_term_anchor
    assert a.pols_death(1) == pytest.approx(0.00055, rel=1e-12)
    assert a.benefit_pp(1) == 150000.0
    assert a.premium_pp(1) == 144.00               # P_a = 12 x P_m
    assert a.comm_init_pp() == pytest.approx(216.00, abs=PENNY)
    assert a.expenses(1) == pytest.approx(150.00 + 30.00, abs=PENNY)
    assert a.net_cf(1) == pytest.approx(
        144.00 - 82.50 - 0.1375 - 180.00 - 216.00, abs=1e-9)


def test_worked_example_inforce_update(uk_term_anchor):
    """l(2) = 1.0 x (1 - 0.00055) x (1 - 0.10), the notes' update step."""
    a = uk_term_anchor
    assert a.lapse_rate(1) == 0.10
    assert a.pols_if(2) == pytest.approx(1.0 * (1 - 0.00055) * (1 - 0.10), rel=1e-14)
    assert a.lapse_rate(2) == 0.08
    assert a.pols_if(3) == pytest.approx(
        a.pols_if(2) * (1 - 0.00060) * (1 - 0.08), rel=1e-14)


def test_new_business_strain_then_thin_margins(uk_term_anchor):
    """The characteristic shape of guaranteed term, asserted rather than described.

    A deep year-one strain from upfront commission and acquisition expense against one
    year's premium, then positive margins while the level premium runs ahead of the
    rising mortality cost.
    """
    a = uk_term_anchor
    assert a.net_cf(1) < -300.0
    assert all(a.net_cf(t) > 0.0 for t in (2, 3, 4))
    assert a.net_cf(a.proj_len()) < 0.0        # mortality cost has overtaken by the end


# ---------------------------------------------------------------------------
# No tail states — the structural contrast with Term_US_A


def test_projection_ends_with_the_term(uk_term_anchor):
    """proj_len() is the term exactly; nothing survives past it.

    Cover ceases at the end of the term with no maturity value, no renewal and no
    conversion.  A US-style post-level-term tail would show up here as a projection
    running past year 25.
    """
    a = uk_term_anchor
    assert a.proj_len() == 25 == a.policy_term()
    assert a.age(25) == 59                       # attained age in the final year
    assert a.pols_if(25) > 0.0
    assert a.pols_if(26) == 0.0
    assert a.pols_if_at(25, "AFT_DECR") == 0.0
    assert len(a.result_cf()) == 25


def test_no_post_level_term_machinery(term_assurance):
    """None of Term_US_A's tail cells exist here, and that is a product fact.

    A UK term policy expires; it does not jump to ART rates, shock-lapse, deteriorate
    or convert.  Importing that machinery materially misstates UK term liabilities,
    which is why its absence is asserted rather than left to inspection.
    """
    names = set(term_assurance.Projection.cells) | set(term_assurance.Projection.refs)
    for absent in ("phase", "jump_ratio", "shock_lapse_rate", "plt_mort_factor",
                   "conv_rate", "conv_elig", "conv_credits", "expiry_age"):
        assert absent not in names, f"{absent} is US post-level-term machinery"


def test_maturity_is_confined_to_the_final_year_and_pays_nothing(uk_term_anchor):
    """pols_maturity closes the roll-forward; it is not a benefit."""
    a = uk_term_anchor
    for t in range(1, a.proj_len()):
        assert a.pols_maturity(t) == 0.0
    assert a.pols_maturity(a.proj_len()) > 0.0
    # No maturity value: the only benefit kinds are DEATH and FIB, and neither fires
    # on the expiring survivors.
    assert a.claims(a.proj_len()) == pytest.approx(
        a.claims(a.proj_len(), "DEATH"), rel=1e-12)


def test_inforce_rollforward_closes(uk_term_anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + expiries, in every year."""
    a = uk_term_anchor
    assert a.check_pols_roll_fwd() is True
    for t in range(1, a.proj_len() + 1):
        out = a.pols_death(t) + a.pols_lapse(t) + a.pols_maturity(t)
        assert a.pols_if(t) - a.pols_if(t + 1) == pytest.approx(out, abs=1e-12)


def test_death_is_decremented_before_lapse(uk_term_anchor):
    """The notes' processing order: lapses are taken from the survivors of mortality."""
    a = uk_term_anchor
    for t in (1, 5, 12):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate(t), rel=1e-14)


def test_inforce_is_a_decreasing_probability(uk_term_anchor):
    a = uk_term_anchor
    for t in range(1, a.proj_len() + 2):
        assert 0.0 <= a.pols_if(t) <= 1.0
        assert a.pols_if(t + 1) <= a.pols_if(t) + 1e-15


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
                   for t in range(proj.proj_start(), proj.proj_len() + 1))


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
    """(1+j_m)^12 = 1+j, so B(12t) closes in annual terms."""
    p = term_assurance.Projection[2]
    j = p.sched_rate()
    n = p.policy_term()
    for t in (1, 5, 10):
        annual = p.sum_assured() * ((1 + j) ** n - (1 + j) ** t) / ((1 + j) ** n - 1)
        assert p.benefit_sched(12 * t) == pytest.approx(annual, rel=1e-12)


def test_decreasing_death_benefit_is_the_mid_year_balance(term_assurance):
    """DB(t) = B(12(t-1) + 6), the annual grid's reading of a monthly step-down."""
    p = term_assurance.Projection[2]
    for t in (1, 6, 20):
        assert p.benefit_pp(t) == pytest.approx(p.benefit_sched(12 * (t - 1) + 6),
                                                rel=1e-14)
    assert p.benefit_pp(1) < p.sum_assured()      # already stepped down by six months


# ---------------------------------------------------------------------------
# The family income benefit ledger


def test_fib_ledger_closes_against_an_independent_rebuild(term_assurance):
    """check_fib_ledger rebuilds the year's instalments straight off the death vector."""
    p = term_assurance.Projection[3]
    assert p.shape() == "fib"
    assert p.check_fib_ledger() is True
    for t in range(1, p.proj_len() + 1):
        assert p.check_fib_ledger_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_fib_total_is_the_annuity_certain_total(term_assurance):
    """A death in year s pays 6 + 12(n-s) instalments — exactly N - k at k = 12(s-1)+6.

    Summed over the projection this is the whole liability, and it is the identity an
    implementation that pays only the year-of-death instalments fails.
    """
    p = term_assurance.Projection[3]
    n, income = p.policy_term(), p.fib_income()
    total = sum(p.claims(t, "FIB") for t in range(1, n + 1))
    built = sum(p.pols_death(s) * income * (6 + 12 * (n - s)) for s in range(1, n + 1))
    assert total == pytest.approx(built, rel=1e-12)
    for s in (1, 10, 25):
        k = 12 * (s - 1) + 6
        assert 6 + 12 * (n - s) == p.term_mths() - k


def test_fib_stream_is_not_decremented_by_mortality_or_lapse(term_assurance):
    """The ledger is a running total of deaths, untouched by later decrements.

    This is the notes' pitfall: the instalments are an annuity-certain once the claim is
    admitted, so only *new* claims carry l(t).
    """
    p = term_assurance.Projection[3]
    for t in range(2, p.proj_len() + 1):
        assert p.fib_cum(t) == pytest.approx(
            p.fib_cum(t - 1) + p.pols_death(t - 1), abs=1e-15)
        assert p.fib_cum(t) >= p.fib_cum(t - 1)   # never falls
    assert p.fib_cum(1) == 0.0


def test_fib_pays_no_lump_sum_when_uncommuted(term_assurance):
    """With take-up at zero the whole liability runs through claims(t, "FIB")."""
    p = term_assurance.Projection[3]
    assert p.fib_commute_rate() == 0.0
    assert all(p.claims(t, "DEATH") == 0.0 for t in range(1, p.proj_len() + 1))
    assert any(p.claims(t, "FIB") > 0.0 for t in range(1, p.proj_len() + 1))


def test_fib_commutation_replaces_the_stream_with_a_lump_sum(term_assurance):
    """Model point 4 is point 3 with take-up at 100%: all lump sum, no instalments."""
    p3, p4 = term_assurance.Projection[3], term_assurance.Projection[4]
    assert p4.fib_commute_rate() == 1.0
    assert all(p4.claims(t, "FIB") == 0.0 for t in range(1, p4.proj_len() + 1))
    assert any(p4.claims(t, "DEATH") > 0.0 for t in range(1, p4.proj_len() + 1))
    # a(294) at r_c = 3%: the value of the instalments a year-one death would generate.
    assert p4.fib_commute_pp(1) == pytest.approx(1000.0 * 208.932248, abs=0.01)
    # Commuting at 3% is worth less than paying the instalments out undiscounted.
    tot3 = sum(p3.claims(t) for t in range(1, p3.proj_len() + 1))
    tot4 = sum(p4.claims(t) for t in range(1, p4.proj_len() + 1))
    assert tot4 < tot3


def test_annuity_certain_factor(term_assurance):
    """a(m) = [1 - (1+r_c)^(-m/12)] / [(1+r_c)^(1/12) - 1], instalments in arrears."""
    p = term_assurance.Projection[4]
    r = 0.03
    for m in (12, 120, 294):
        expected = (1 - (1 + r) ** (-m / 12)) / ((1 + r) ** (1 / 12) - 1)
        assert p.annuity_certain_factor(m) == pytest.approx(expected, rel=1e-12)
    assert p.annuity_certain_factor(0) == 0.0
    assert p.annuity_certain_factor(-5) == 0.0


def test_fib_premiums_stop_at_death_though_instalments_do_not(term_assurance):
    """Premium income always carries l(t); the FIB ledger never touches it."""
    p = term_assurance.Projection[3]
    for t in (1, 10, 25):
        assert p.premiums(t) == pytest.approx(p.premium_pp(t) * p.pols_if(t), rel=1e-14)


# ---------------------------------------------------------------------------
# Indexation


def test_indexation_compounds_cover_and_premium_at_the_notes_rates(term_assurance):
    """Flat 3% RPI: cover x 1.03 and premium x 1.045, the x1.5 premium factor."""
    p = term_assurance.Projection[5]
    assert p.indexation() is True
    assert p.idx_increase() == pytest.approx(0.03, rel=1e-12)
    for t in (1, 2, 3):
        assert p.idx_factor(t) == pytest.approx(1.03 ** (t - 1), rel=1e-12)
        assert p.idx_prem_factor(t) == pytest.approx(1.045 ** (t - 1), rel=1e-12)
    assert p.benefit_pp(3) == pytest.approx(150000.0 * 1.03 ** 2, rel=1e-12)
    assert p.premium_pp(3) == pytest.approx(144.0 * 1.045 ** 2, rel=1e-12)


def test_indexation_caps(term_assurance):
    """Cover increase capped at 10% and the premium increase at 15%.

    ``Projection.clear_all()`` discards the ItemSpaces along with their caches, so the
    ItemSpace is re-fetched after each change of Reference rather than held across it.
    """
    model = mx.read_model(MODEL_DIR, name="Term_UK_A_idxcap")
    try:
        model.Projection.rpi_rate = 0.25          # far above both caps
        model.Projection.clear_all()
        proj = model.Projection[5]
        assert proj.idx_increase() == pytest.approx(0.10, rel=1e-12)
        # 1.5 x 10% = 15%, exactly at the premium cap.
        assert proj.idx_prem_factor(2) == pytest.approx(1.15, rel=1e-12)
        model.Projection.rpi_rate = -0.02         # deflation floors the increase at 0
        model.Projection.clear_all()
        proj = model.Projection[5]
        assert proj.idx_increase() == 0.0
        assert proj.idx_factor(5) == 1.0
    finally:
        model.close()


def test_indexation_is_off_on_the_other_model_points(term_assurance):
    """Unelected, both factors stay at 1 for the whole projection."""
    p = term_assurance.Projection[1]
    assert p.indexation() is False
    assert all(p.idx_factor(t) == 1.0 and p.idx_prem_factor(t) == 1.0
               for t in range(1, p.proj_len() + 1))


def test_indexation_is_restricted_to_the_level_shape(term_assurance):
    """No fetched insurer offers indexed decreasing cover, so the combination is barred."""
    model = mx.read_model(MODEL_DIR, name="Term_UK_A_idxshape")
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
    for t in (1, 8, 20):
        q1, q2 = p.mort_rate_life(t, 1), p.mort_rate_life(t, 2)
        assert p.mort_rate(t) == pytest.approx(1 - (1 - q1) * (1 - q2), rel=1e-14)
        assert p.mort_rate(t) < q1 + q2           # not the sum of the two rates
    assert p.check_pols_roll_fwd() is True


def test_single_life_collapses_to_the_first_life(term_assurance):
    p = term_assurance.Projection[1]
    assert p.is_joint() is False
    for t in (1, 10):
        assert p.mort_rate(t) == p.mort_rate_life(t, 1)
    with pytest.raises(FormulaError):
        p.age_at_entry(2)          # modelx wraps the formula's ValueError


# ---------------------------------------------------------------------------
# The two mortality bases


def test_applied_basis_takes_the_table_as_it_stands(uk_term_anchor):
    """No select factor and no proxy scaling on the applied basis."""
    a = uk_term_anchor
    assert a.mort_basis() == "applied"
    for t in (1, 4, 20):
        assert a.mort_rate(t) == pytest.approx(a.mort_rate_base(t), rel=1e-14)


def test_select_basis_applies_the_select_factor_and_the_proxy_scaling(term_assurance):
    """table x select_factor(duration) x 0.75, with a 5-year select period."""
    p = term_assurance.Projection[7]
    assert p.mort_basis() == "select"
    for t in range(1, 8):
        assert p.mort_rate(t) == pytest.approx(
            p.mort_rate_base(t) * p.select_factor(t) * 0.75, rel=1e-14)
    # The select discount wears off over five years and is gone from duration 5.
    assert p.select_factor(1) == 0.55             # duration 0
    assert p.select_factor(5) == 0.93             # duration 4
    assert p.select_factor(6) == 1.00             # duration 5, ultimate
    assert p.select_factor(20) == 1.00
    assert p.mort_rate(1) < p.mort_rate_base(1)


def test_the_two_bases_disagree_and_that_is_shipped_not_resolved(term_assurance):
    """Both readings are standardizations; the gap must not be closed silently.

    The notes' three illustrative applied rates rise at 9% a year, which no graduated
    select structure produces, so neither basis is derivable from the other.
    """
    model = mx.read_model(MODEL_DIR, name="Term_UK_A_bases")
    try:
        proj = model.Projection[1]
        applied = proj.mort_rate(1)
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
        p.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        p.claims(1, "SURRENDER")


# ---------------------------------------------------------------------------
# Modules that are off in the base run


def test_selective_lapsation_is_off_and_works_when_switched_on(term_assurance):
    """q_eff = q (1 + lambda max(0, w_cum - w_ref)); lambda = 0 in the base run."""
    p = term_assurance.Projection[1]
    assert all(p.sel_lapse_factor(t) == 1.0 for t in range(1, p.proj_len() + 1))
    assert p.lapse_cum(1) == 0.0
    assert p.lapse_cum(5) > 0.0

    model = mx.read_model(MODEL_DIR, name="Term_UK_A_sel")
    try:
        base_late = model.Projection[1].mort_rate(20)
        model.Projection.sel_lapse_lambda = 0.25
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.sel_lapse_factor(1) == 1.0            # nothing has lapsed yet
        assert proj.sel_lapse_factor(20) > 1.0            # w_cum has passed w_ref
        assert proj.mort_rate(20) > base_late
    finally:
        model.close()


def test_rebroking_is_off_and_works_when_switched_on(term_assurance):
    """M_reb = min(2, max(1, P_inforce / P_market)); the ratio is 1 in the base run."""
    p = term_assurance.Projection[1]
    assert all(p.rebroke_factor(t) == 1.0 for t in range(1, p.proj_len() + 1))
    assert p.lapse_rate(1) == p.lapse_rate_base(1)

    model = mx.read_model(MODEL_DIR, name="Term_UK_A_reb")
    try:
        model.Projection.premium_market_ratio = 1.5
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.rebroke_factor(1) == pytest.approx(1.5)
        assert proj.lapse_rate(3) == pytest.approx(0.07 * 1.5)
        model.Projection.premium_market_ratio = 5.0       # above the cap
        model.Projection.clear_all()
        assert model.Projection[1].rebroke_factor(1) == 2.0
        model.Projection.premium_market_ratio = 0.4       # cheaper in force, no rebroking
        model.Projection.clear_all()
        assert model.Projection[1].rebroke_factor(1) == 1.0
    finally:
        model.close()


def test_commission_clawback_is_off_and_works_when_switched_on(term_assurance):
    """Linear over four years; off by default, so commission is never negative."""
    p = term_assurance.Projection[1]
    assert all(p.comm_clawback(t) == 0.0 for t in range(1, p.proj_len() + 1))

    model = mx.read_model(MODEL_DIR, name="Term_UK_A_claw")
    try:
        model.Projection.clawback_mths = 48
        model.Projection.clear_all()
        proj = model.Projection[1]
        # Year 1: 36 of 48 months remaining, so 75% of c0 per lapsed policy.
        assert proj.comm_clawback(1) == pytest.approx(
            216.0 * 0.75 * proj.pols_lapse(1), rel=1e-12)
        assert proj.comm_clawback(4) == 0.0               # window closed at 48 months
        assert proj.comm_clawback(5) == 0.0
        assert proj.commissions(2) < 0.025 * proj.premiums(2)
    finally:
        model.close()


def test_waiver_of_premium_is_off_and_works_when_switched_on(term_assurance):
    """The waived fraction is a two-state chain; zero unless the rider is in force."""
    p1 = term_assurance.Projection[1]
    assert p1.wop() is False
    assert all(p1.wop_waived_frac(t) == 0.0 for t in range(1, p1.proj_len() + 1))
    assert all(p1.pols_payer(t) == p1.pols_if(t) for t in range(1, p1.proj_len() + 1))

    p7 = term_assurance.Projection[7]
    assert p7.wop() is True
    assert p7.wop_waived_frac(1) == 0.0                   # 26-week deferred period
    assert p7.wop_waived_frac(2) == pytest.approx(0.004, rel=1e-12)
    assert p7.wop_waived_frac(3) > p7.wop_waived_frac(2)  # not yet at equilibrium
    assert p7.pols_payer(5) < p7.pols_if(5)
    # The rider carries a premium loading, also [std].
    assert p7.premium_pp(1) == pytest.approx(12 * 45.00 * 1.05, rel=1e-12)


def test_waived_fraction_converges_below_one(term_assurance):
    """inc / (inc + rec) is the equilibrium of the two-state chain."""
    p = term_assurance.Projection[7]
    equilibrium = 0.004 / (0.004 + 0.35)
    assert p.wop_waived_frac(p.proj_len()) == pytest.approx(equilibrium, abs=1e-5)


# ---------------------------------------------------------------------------
# In-force model points


def test_an_inforce_model_point_starts_at_its_duration(term_assurance):
    """duration_inforce = 5 means the projection starts in policy year 6.

    An in-force policy never sees the acquisition expense or the initial commission,
    but does pay renewal commission, and its expense inflation is measured from issue.
    """
    p = term_assurance.Projection[8]
    assert p.duration_inforce() == 5 and p.proj_start() == 6
    df = p.result_cf()
    assert list(df.index) == list(range(6, 26))
    assert p.pols_if(5) == 0.0 and p.pols_if(6) == 1.0
    assert p.expenses(6) == pytest.approx(30.0 * 1.03 ** 5, rel=1e-12)   # no E0
    assert p.commissions(6) == pytest.approx(0.025 * p.premiums(6), rel=1e-12)
    assert p.lapse_cum(6) == 0.0
    assert p.check_pols_roll_fwd() is True


def test_an_inforce_point_uses_the_same_rates_as_the_issued_one(term_assurance):
    """Duration is measured from entry, not from the start of the projection."""
    p1, p8 = term_assurance.Projection[1], term_assurance.Projection[8]
    for t in range(6, 26):
        assert p8.mort_rate(t) == p1.mort_rate(t)
        assert p8.lapse_rate(t) == p1.lapse_rate(t)
        assert p8.duration(t) == t - 1


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_term_anchor):
    df = uk_term_anchor.result_cf()
    assert list(df.index) == list(range(1, 26))
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_fib", "claims_lapse",
        "claim_expenses", "expenses", "commissions", "net_cf",
    ]
    assert df.loc[1, "net_cf"] == pytest.approx(-334.64, abs=PENNY)


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
    assert term_assurance.Projection[1].net_cf(2) > 0.0    # a positive-margin year


def test_model_docstring_describes_the_current_structure(term_assurance):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = term_assurance.doc
    assert "term assurance" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "no maturity value, no renewal and no conversion" in doc


def test_space_docstrings_carry_their_reference_material(term_assurance):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = term_assurance.Projection.doc
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    for cells in ("pols_if", "pols_maturity", "fib_cum", "benefit_sched",
                  "select_factor", "mort_basis"):
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
        "pols_maturity", "mort_rate", "lapse_rate", "premiums", "claims",
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


def test_inputs_are_read_once_not_once_per_model_point():
    """The readers live in Data, so N model points do not cause N reads."""
    from collections import Counter

    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Term_UK_A_reads")
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
    assert len(reads) == 4           # one per input file, regardless of point count


def test_projection_shares_one_data_space(term_assurance):
    """`data` resolves to the single Data Space from every ItemSpace."""
    assert term_assurance.Projection[1].data is term_assurance.Data
    assert term_assurance.Projection[1].data is term_assurance.Projection[3].data


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a production
    user does with the licensed CMI tables: they drop in as same-schema CSVs with no
    formula change.
    """
    import pandas as pd

    src = MODEL_DIR.parent / "mort_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "smoker", "age"])
    doubled["mort_rate"] = doubled["mort_rate"] * 2

    model = mx.read_model(MODEL_DIR, name="Term_UK_A_swap")
    try:
        alt_name = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].claims(1, "DEATH")
            model.Data.mort_table_file = alt_name      # repoint the Reference
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].claims(1, "DEATH") == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_every_model_point_projects(term_assurance):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in term_assurance.Data.model_point_table().index:
        proj = term_assurance.Projection[point_id]
        df = proj.result_cf()
        assert len(df) > 0
        assert df.notna().all().all()
        assert proj.check_pols_roll_fwd() is True
        assert proj.check_fib_ledger() is True


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Term_UK_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Term_UK_A_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[6], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
