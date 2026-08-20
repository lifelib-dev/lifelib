"""Golden and structural tests for CI_UK_S.

The golden values are the worked example in
products/critical_illness/technical-notes.md ("Worked example"), which projects the
anchor cell M40 / non-smoker / accelerated / 25-year term / GBP 100,000 sum assured /
GBP 55.00 per month.  They are hard-coded here rather than pickled so that a reviewer
can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the penny, in-force to six
decimals.

Beyond the worked example this module asserts the four product facts the notes call out
as modelling pitfalls, because each is a way an implementation can look right and be
wrong:

* death and CI must not be added without netting the overlap ``k``;
* the survival-period slippage bites on the standalone contract only;
* the additional-payment and children's benefits must not deplete the sum assured;
* and they must not decrement the in-force either.
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

MODEL_DIR = LIB / MODELS["CI_UK_S"][0]

# t: (l(t-1), premium, main claim, claim expense, additional payment, children's,
#     maintenance, notes' Net CF, l(t))
#
# The notes' Net CF column EXCLUDES the GBP 200 initial expense, which they carry
# separately: month 1 is 31.88 in the table and -168.12 in total.
WORKED_EXAMPLE = {
    1: (1.000000, 55.00, 19.27, 0.05, 0.47, 0.83, 2.50, 31.88, 0.991067),
    2: (0.991067, 54.51, 19.10, 0.05, 0.46, 0.83, 2.48, 31.59, 0.982215),
    3: (0.982215, 54.02, 18.93, 0.05, 0.46, 0.82, 2.46, 31.31, 0.973441),
}

# The notes' month-1 rate trace for the anchor cell.
Q_CLAIM = 0.00231            # 0.0015 + 0.0009 x 0.90
Q_M = 0.00019270             # 1 - (1 - 0.00231)^(1/12)
W_M = 0.0087416              # 1 - 0.90^(1/12)
A_M = 0.00001875             # 0.15 x 0.0015 / 12
LAMBDA_M = 0.0004 / 12


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_ci_anchor, t):
    """Every cell of the notes' three-month table, to the displayed precision."""
    pols, prem, main, clm_exp, ap, child, maint, net, pols_end = WORKED_EXAMPLE[t]
    a = uk_ci_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=PENNY)
    assert a.claims(t, "MAIN") == pytest.approx(main, abs=PENNY)
    assert a.claim_expenses(t) == pytest.approx(clm_exp, abs=PENNY)
    assert a.claims(t, "AP") == pytest.approx(ap, abs=PENNY)
    assert a.claims(t, "CHILD") == pytest.approx(child, abs=PENNY)
    # The notes' maintenance column is the monthly expense excluding the initial one.
    initial = 200.0 if t == 1 else 0.0
    assert a.expenses(t) - initial == pytest.approx(maint, abs=PENNY)
    assert a.net_cf(t) + initial == pytest.approx(net, abs=PENNY)
    assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(pols_end, abs=INFORCE)


def test_month_one_total_includes_the_initial_expense(uk_ci_anchor):
    """The notes' Net CF column is 31.88; the month's total cash flow is -168.12.

    The initial expense is carried outside the table, so a reader comparing the two by
    eye needs the difference stated rather than discovered.
    """
    a = uk_ci_anchor
    assert a.net_cf(1) == pytest.approx(-168.12, abs=PENNY)
    assert a.net_cf(1) + 200.0 == pytest.approx(31.88, abs=PENNY)
    assert a.expenses(1) == pytest.approx(202.50, abs=PENNY)
    assert a.expenses(2) == pytest.approx(2.50 * a.pols_if(2), abs=PENNY)


def test_worked_example_rate_trace(uk_ci_anchor):
    """The notes' month-1 rate trace, line by line."""
    a = uk_ci_anchor
    assert a.ci_rate(1) == pytest.approx(0.0015, rel=1e-12)
    assert a.mort_rate(1) == pytest.approx(0.0009, rel=1e-12)
    assert a.claim_rate(1) == pytest.approx(Q_CLAIM, rel=1e-12)
    assert a.claim_rate_mth(1) == pytest.approx(Q_M, abs=5e-9)
    assert a.lapse_rate(1) == 0.10
    assert a.lapse_rate_mth(1) == pytest.approx(W_M, abs=5e-8)
    assert a.ap_rate_mth(1) == pytest.approx(A_M, rel=1e-12)
    assert a.child_rate_mth() == pytest.approx(LAMBDA_M, rel=1e-12)
    assert a.benefit_pp(1, "AP") == 25000.0
    assert a.benefit_pp(1, "CHILD") == 25000.0


def test_worked_example_survivor_factor(uk_ci_anchor):
    """s = (1 - q_m)(1 - w_m) = 0.9910674, so l(t) = s^t while the rates hold."""
    a = uk_ci_anchor
    s = (1 - a.claim_rate_mth(1)) * (1 - a.lapse_rate_mth(1))
    assert s == pytest.approx(0.9910674, abs=5e-8)
    for t in (1, 2, 3):
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(s ** t, rel=1e-12)


# ---------------------------------------------------------------------------
# The combined decrement, and both overlap pitfalls


def test_death_and_ci_are_not_simply_added(uk_ci_anchor):
    """q_claim = i_ci + q_d(1 - k), not i_ci + q_d.

    Summing the two rates double-counts lives that are both diagnosed and die in the
    same period - the notes' first-listed pitfall.
    """
    a = uk_ci_anchor
    for t in (1, 60, 200):
        naive = a.ci_rate(t) + a.mort_rate(t)
        assert a.claim_rate(t) == pytest.approx(
            a.ci_rate(t) + a.mort_rate(t) * 0.90, rel=1e-12)
        assert a.claim_rate(t) < naive


def test_the_overlap_factor_is_a_reference_not_a_literal(critical_illness):
    """k is the notes' third-largest lever, with bounds 0 and 0.25 either side."""
    model = mx.read_model(MODEL_DIR, name="CI_UK_S_overlap")
    try:
        base = model.Projection[1].claim_rate(1)
        model.Projection.overlap_k = 0.0          # maximal double-counting
        model.Projection.clear_all()
        assert model.Projection[1].claim_rate(1) == pytest.approx(
            0.0015 + 0.0009, rel=1e-12)
        assert model.Projection[1].claim_rate(1) > base
        model.Projection.overlap_k = 0.25
        model.Projection.clear_all()
        assert model.Projection[1].claim_rate(1) < base
    finally:
        model.close()


def test_the_survival_period_does_not_bite_on_the_accelerated_contract(uk_ci_anchor):
    """Death inside the 14 days still pays SA as a death claim, so delta is not applied.

    Applying the slippage to the accelerated main benefit is the notes' second pitfall.
    """
    a = uk_ci_anchor
    assert a.contract_type() == "accelerated"
    for t in (1, 100, 300):
        assert a.claim_rate_paid(t) == a.claim_rate(t)
        assert a.claim_rate_paid_mth(t) == a.claim_rate_mth(t)
        assert a.claim_rate_exit_mth(t) == 0.0


def test_the_survival_period_bites_on_the_standalone_contract(critical_illness):
    """q_pay = i_ci(1 - delta); death pays nothing and delta slips 3% of diagnoses."""
    p = critical_illness.Projection[2]
    assert p.contract_type() == "standalone"
    for t in (1, 100, 300):
        assert p.claim_rate_paid(t) == pytest.approx(p.ci_rate(t) * 0.97, rel=1e-12)
        assert p.claim_rate_paid(t) < p.claim_rate(t)
        assert p.claim_rate_exit_mth(t) > 0.0


def test_the_overlap_factor_stays_off_the_paid_decrement(critical_illness):
    """k belongs to the non-paying exit; applying it to q_pay understates claims.

    The mirror image of the double-counting pitfall, and the reason the two decrements
    are separate cells rather than one scaled by a share.
    """
    p = critical_illness.Projection[2]
    for t in (1, 150):
        # q_pay depends on i_ci and delta alone - no k anywhere in it.
        assert p.claim_rate_paid(t) == pytest.approx(
            p.ci_rate(t) * (1 - 0.03), rel=1e-12)
        # and the exit rate carries it.
        q_exit = p.mort_rate(t) * 0.90 + p.ci_rate(t) * 0.03
        assert p.claim_rate(t) == pytest.approx(
            p.claim_rate_paid(t) + q_exit, rel=1e-12)


def test_the_standalone_runoff_matches_the_accelerated_one(critical_illness):
    """Same total decrement, so the in-force paths coincide; only the outgo differs."""
    p1, p2 = critical_illness.Projection[1], critical_illness.Projection[2]
    for t in (1, 60, 180, 300):
        assert p2.claim_rate(t) == pytest.approx(p1.claim_rate(t), rel=1e-12)
        assert p2.pols_if(t) == pytest.approx(p1.pols_if(t), rel=1e-12)
        assert p2.claims(t, "MAIN") < p1.claims(t, "MAIN")


def test_the_monthly_split_artefact_is_bounded_not_hidden(critical_illness):
    """check_claim_split bounds the notes' two inconsistent conventions.

    The notes add the annual paying and non-paying parts but convert each
    geometrically, which cannot both hold.  The exit rate is defined as the residual so
    the split is exact; this check says how far that residual is from the notes' own
    conversion of q_exit.
    """
    p = critical_illness.Projection[2]
    assert p.check_claim_split() is True
    resids = [abs(p.check_claim_split_resid(t)) for t in range(1, p.proj_len() + 1)]
    assert max(resids) < 1e-4            # inside the shipped tolerance
    assert max(resids) > 0.0             # but genuinely non-zero: it is a real artefact
    # Exact on the accelerated contract, where there is no split to make.
    assert all(critical_illness.Projection[1].check_claim_split_resid(t) == 0.0
               for t in (1, 150, 300))


# ---------------------------------------------------------------------------
# The non-terminating benefits


def test_the_ancillary_benefits_do_not_deplete_the_sum_assured(uk_ci_anchor):
    """SA is unmoved by additional-payment and children's claims.

    Modelling them as accelerations of SA - a plan-account depletion design - is a
    different product, and is the notes' third pitfall.
    """
    a = uk_ci_anchor
    for t in (1, 100, 300):
        assert a.benefit_pp(t, "MAIN") == 100000.0
        assert a.benefit_pp(t, "AP") == 25000.0
        assert a.benefit_pp(t, "CHILD") == 25000.0


def test_the_ancillary_benefits_do_not_decrement_the_inforce(uk_ci_anchor):
    """Only the main benefit ends the policy - the notes' fourth pitfall.

    The roll-forward closes on main claims, lapses and expiries alone, so an
    implementation that terminated on an additional-payment claim would fail here.
    """
    a = uk_ci_anchor
    assert a.check_pols_roll_fwd() is True
    for t in range(1, a.proj_len() + 1):
        out = a.pols_claim(t) + a.pols_lapse(t) + a.pols_maturity(t)
        assert a.pols_if(t) - a.pols_if(t + 1) == pytest.approx(out, abs=1e-12)
    # The decrement is the combined claim rate alone, with no frequency loading in it.
    for t in (1, 150):
        assert a.pols_claim(t) == pytest.approx(
            a.pols_if(t) * a.claim_rate_mth(t), rel=1e-14)


def test_the_ancillary_frequencies_are_divided_by_twelve_not_transformed(uk_ci_anchor):
    """A repeatable claim frequency has no survival transform to apply.

    ``rate/12``, not ``1 - (1 - rate)^(1/12)`` - the two differ in the fifth decimal
    here, but the reason is structural rather than numerical.
    """
    a = uk_ci_anchor
    for t in (1, 150, 300):
        assert a.ap_rate_mth(t) == pytest.approx(a.ap_rate(t) / 12.0, rel=1e-14)
        assert a.ap_rate_mth(t) != pytest.approx(
            1 - (1 - a.ap_rate(t)) ** (1 / 12), rel=1e-9)
    assert a.child_rate_mth() == pytest.approx(0.0004 / 12.0, rel=1e-14)


def test_children_cover_can_be_switched_off(critical_illness):
    """Model point 5 is the anchor cell without children's cover."""
    p5 = critical_illness.Projection[5]
    assert p5.children_cover() is False
    assert p5.child_rate_mth() == 0.0
    assert p5.benefit_pp(1, "CHILD") == 0.0
    assert all(p5.claims(t, "CHILD") == 0.0 for t in range(1, p5.proj_len() + 1))
    # Everything else is unchanged, so the difference is exactly the children's outgo.
    p1 = critical_illness.Projection[1]
    for t in (1, 150):
        assert p5.net_cf(t) - p1.net_cf(t) == pytest.approx(
            p1.claims(t, "CHILD"), abs=1e-9)


def test_the_ancillary_caps_track_the_indexed_sum_assured(critical_illness):
    """min(25% of SA(t), 25,000) and min(50% of SA(t), 25,000), on the indexed SA.

    At the anchor sum assured the cash cap binds either way; the test uses a small sum
    assured, where the percentage binds, to see which SA the cap is struck against.
    """
    model = mx.read_model(MODEL_DIR, name="CI_UK_S_caps")
    try:
        proj = model.Projection[4]                # the indexed point
        assert proj.indexation() is True
        t_year3 = 25                             # policy year 3
        main = proj.benefit_pp(t_year3, "MAIN")
        assert main == pytest.approx(100000.0 * 1.03 ** 2, rel=1e-12)
        # The cash caps bind at this size, so both are 25,000 regardless.
        assert proj.benefit_pp(t_year3, "AP") == 25000.0
        assert proj.benefit_pp(t_year3, "CHILD") == 25000.0
        # Raise the caps out of the way and the percentages track the indexed SA.
        model.Projection.ap_cap = 1e9
        model.Projection.child_cap = 1e9
        model.Projection.clear_all()
        proj = model.Projection[4]
        assert proj.benefit_pp(t_year3, "AP") == pytest.approx(
            0.25 * 100000.0 * 1.03 ** 2, rel=1e-12)
        assert proj.benefit_pp(t_year3, "CHILD") == pytest.approx(
            0.50 * 100000.0 * 1.03 ** 2, rel=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The rate basis


def test_pivot_interpolation_is_log_linear(uk_ci_anchor):
    """r(x) = r0 (r1/r0)^((x-x0)/(x1-x0)), geometric in the rate and linear in age."""
    a = uk_ci_anchor
    # The pivots themselves come back exactly.
    assert a.pivot_interp(40, "M", "NS", "i_ci") == pytest.approx(0.0015, rel=1e-12)
    assert a.pivot_interp(45, "M", "NS", "i_ci") == pytest.approx(0.0025, rel=1e-12)
    assert a.pivot_interp(65, "M", "NS", "q_d") == pytest.approx(0.0100, rel=1e-12)
    # The midpoint of a segment is the geometric mean of its ends, not the arithmetic.
    mid = a.pivot_interp(42.5, "M", "NS", "i_ci")
    assert mid == pytest.approx((0.0015 * 0.0025) ** 0.5, rel=1e-12)
    assert mid < (0.0015 + 0.0025) / 2
    # And a whole-year age inside the segment.
    assert a.pivot_interp(42, "M", "NS", "i_ci") == pytest.approx(
        0.0015 * (0.0025 / 0.0015) ** (2 / 5), rel=1e-12)


def test_pivot_extrapolation_continues_the_end_segments(uk_ci_anchor):
    """Outside 40-65 the nearest segment's gradient continues, and it is an extrapolation."""
    a = uk_ci_anchor
    below = a.pivot_interp(35, "M", "NS", "i_ci")
    assert below == pytest.approx(0.0015 * (0.0025 / 0.0015) ** (-1.0), rel=1e-12)
    assert below < 0.0015
    above = a.pivot_interp(70, "M", "NS", "i_ci")
    assert above == pytest.approx(0.0110 * (0.0170 / 0.0110) ** 2, rel=1e-12)
    assert above > 0.0170


def test_the_rates_are_monotone_in_age_over_the_projection(critical_illness):
    """Diagnosis and mortality both rise with age on every shipped model point."""
    for point_id in critical_illness.Data.model_point_table().index:
        proj = critical_illness.Projection[point_id]
        years = range(1, proj.proj_len() + 1, 12)
        ci = [proj.ci_rate(t) for t in years]
        qd = [proj.mort_rate(t) for t in years]
        assert ci == sorted(ci), point_id
        assert qd == sorted(qd), point_id


def test_the_shipped_rate_table_marks_its_own_provenance():
    """Only the male non-smoker pivots are the notes' own; the rest are flat factors.

    The table is a [std] proxy and must not be presented as CMI or ONS values, which is
    what the provenance column exists to prevent.
    """
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "ci_rate_table.csv")
    assert table["provenance"].notna().all()
    notes = table[table["provenance"] == "notes [std] proxy pivot"]
    assert sorted(notes["age"]) == [40, 45, 50, 55, 60, 65]
    assert set(notes["sex"]) == {"M"} and set(notes["smoker"]) == {"NS"}
    assert list(notes.sort_values("age")["i_ci"]) == [
        0.0015, 0.0025, 0.0040, 0.0070, 0.0110, 0.0170]
    assert list(notes.sort_values("age")["q_d"]) == [
        0.0009, 0.0014, 0.0022, 0.0036, 0.0060, 0.0100]
    assert len(table) == 24            # six pivots x two sexes x two smoker statuses


def test_the_smoker_and_female_cells_are_flat_factors(uk_ci_anchor):
    """Crude by design, and stated as such: i_ci x1.75 / x0.95, q_d x2.00 / x0.70."""
    a = uk_ci_anchor
    for age in (40, 55, 65):
        base_ci = a.pivot_interp(age, "M", "NS", "i_ci")
        base_qd = a.pivot_interp(age, "M", "NS", "q_d")
        assert a.pivot_interp(age, "M", "S", "i_ci") == pytest.approx(
            base_ci * 1.75, rel=1e-6)
        assert a.pivot_interp(age, "F", "NS", "q_d") == pytest.approx(
            base_qd * 0.70, rel=1e-6)
        assert a.pivot_interp(age, "F", "S", "i_ci") == pytest.approx(
            base_ci * 1.75 * 0.95, rel=1e-6)


def test_the_ci_trend_is_off_and_works_when_switched_on(critical_illness):
    """tau = 0 in the base run; it is the notes' first-listed sensitivity anyway."""
    a = critical_illness.Projection[1]
    assert all(a.ci_trend_factor(t) == 1.0 for t in (1, 150, 300))

    model = mx.read_model(MODEL_DIR, name="CI_UK_S_trend")
    try:
        model.Projection.ci_trend = 0.02
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.ci_trend_factor(1) == 1.0                     # policy year 1
        assert proj.ci_trend_factor(13) == pytest.approx(1.02, rel=1e-12)
        assert proj.ci_trend_factor(300) == pytest.approx(1.02 ** 24, rel=1e-12)
        assert proj.ci_rate(300) > a.ci_rate(300)
        assert proj.mort_rate(300) == a.mort_rate(300)            # trend is CI-only
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The reviewable variant


def test_the_reviewable_snapshot_is_identical_to_the_guaranteed_run(critical_illness):
    """rho_review = 0, so model point 3 differs from point 1 in nothing but the flag."""
    p1, p3 = critical_illness.Projection[1], critical_illness.Projection[3]
    assert p3.premium_guarantee() == "reviewable"
    assert p3.reviews_passed(300) == 4                # months 61, 121, 181, 241
    assert all(not p3.review_shock_active(t) for t in (61, 65, 121, 300))
    df1, df3 = p1.result_cf(), p3.result_cf()
    assert (df1 - df3).abs().max().max() == pytest.approx(0.0, abs=1e-12)


def test_guaranteed_premiums_are_never_reviewed(uk_ci_anchor):
    """Nothing on a guaranteed policy can move the premium, review Reference or not."""
    a = uk_ci_anchor
    assert a.premium_guarantee() == "guaranteed"
    assert all(a.reviews_passed(t) == 0 for t in (1, 61, 121, 300))
    assert all(a.premium_pp(t) == 55.0 for t in (1, 61, 121, 300))
    assert a.ci_sel_factor(300) == 1.0


def test_a_review_raises_the_premium_and_shocks_lapse(critical_illness):
    """The 5-yearly cycle, the twelve-month shock window and the anti-selection loading."""
    model = mx.read_model(MODEL_DIR, name="CI_UK_S_review")
    try:
        model.Projection.review_prem_shock = 0.20     # well past the 5% threshold
        model.Projection.clear_all()
        proj = model.Projection[3]
        # First review bites in month 61, not month 60.
        assert proj.premium_pp(60) == pytest.approx(55.0, rel=1e-12)
        assert proj.premium_pp(61) == pytest.approx(55.0 * 1.20, rel=1e-12)
        assert proj.premium_pp(121) == pytest.approx(55.0 * 1.20 ** 2, rel=1e-12)
        # Shock lapse for twelve months, then back to the table rate.
        base = proj.lapse_rate_base(61)
        assert proj.review_shock_active(61) is True
        assert proj.review_shock_active(72) is True
        assert proj.review_shock_active(73) is False
        assert proj.lapse_rate(61) == pytest.approx(
            min(0.30, base + 2.0 * (0.20 - 0.05)), rel=1e-12)
        assert proj.lapse_rate(73) == pytest.approx(base, rel=1e-12)
        # Anti-selection loads the diagnosis rate from the first shock onwards.
        assert proj.ci_sel_factor(60) == 1.0
        assert proj.ci_sel_factor(61) == pytest.approx(1.10, rel=1e-12)
        assert proj.ci_sel_factor(300) == pytest.approx(1.10, rel=1e-12)
    finally:
        model.close()


def test_a_small_review_change_produces_no_shock(critical_illness):
    """Below the 5% threshold the premium moves but behaviour does not."""
    model = mx.read_model(MODEL_DIR, name="CI_UK_S_smallreview")
    try:
        model.Projection.review_prem_shock = 0.03
        model.Projection.clear_all()
        proj = model.Projection[3]
        assert proj.premium_pp(61) == pytest.approx(55.0 * 1.03, rel=1e-12)
        assert proj.review_shock_active(61) is False
        assert proj.lapse_rate(61) == proj.lapse_rate_base(61)
        assert proj.ci_sel_factor(300) == 1.0
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Indexation, joint lives and scope limits


def test_indexation_compounds_cover_and_premium(critical_illness):
    """Flat 3% RPI: cover x 1.03 and premium x 1.045 per anniversary, within caps."""
    p = critical_illness.Projection[4]
    assert p.indexation() is True
    assert p.idx_increase() == pytest.approx(0.03, rel=1e-12)
    for y, t in ((1, 1), (2, 13), (3, 25)):
        assert p.policy_year(t) == y
        assert p.idx_factor(t) == pytest.approx(1.03 ** (y - 1), rel=1e-12)
        assert p.idx_prem_factor(t) == pytest.approx(1.045 ** (y - 1), rel=1e-12)
        assert p.premium_pp(t) == pytest.approx(55.0 * 1.045 ** (y - 1), rel=1e-12)
    # It steps on anniversaries, not monthly.
    assert p.idx_factor(12) == p.idx_factor(1)
    assert p.idx_factor(13) > p.idx_factor(12)


def test_joint_first_event_is_one_policy_with_one_decrement(critical_illness):
    """q = 1 - (1-q1)(1-q2): the policy pays once and ends."""
    p = critical_illness.Projection[7]
    assert p.is_joint() is True
    assert p.age_at_entry(2) == 38 and p.sex(2) == "F"
    for t in (1, 150, 300):
        q1, q2 = p.claim_rate_life(t, 1), p.claim_rate_life(t, 2)
        assert p.claim_rate(t) == pytest.approx(1 - (1 - q1) * (1 - q2), rel=1e-12)
        assert p.claim_rate(t) < q1 + q2
    assert p.check_pols_roll_fwd() is True
    # Two lives at risk, so the policy runs off faster than the single-life anchor.
    assert p.pols_if(300) < critical_illness.Projection[1].pols_if(300)


def test_single_life_collapses_to_the_first_life(uk_ci_anchor):
    a = uk_ci_anchor
    assert a.is_joint() is False
    for t in (1, 150):
        assert a.claim_rate(t) == pytest.approx(a.claim_rate_life(t, 1), rel=1e-14)
    with pytest.raises(FormulaError):
        a.age_at_entry(2)          # modelx wraps the formula's ValueError


def test_standalone_joint_is_refused_rather_than_invented(critical_illness):
    """No published basis splits a joint first-event decrement into paying parts.

    Refusing is better than inventing one, so the combination raises.  No shipped model
    point carries it.
    """
    table = critical_illness.Data.model_point_table()
    combined = ((table["contract_type"] == "standalone")
                & (table["life_basis"] == "joint_first_event"))
    assert not combined.any()


def test_only_the_level_cover_basis_is_in_scope(critical_illness):
    """Decreasing and FIB shapes live on the term chassis; these notes scope them out."""
    table = critical_illness.Data.model_point_table()
    assert set(table["cover_basis"]) == {"level"}
    for point_id in table.index:
        assert critical_illness.Projection[point_id].cover_basis() == "level"


def test_invalid_enum_values_raise(uk_ci_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        uk_ci_anchor.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        uk_ci_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        uk_ci_anchor.benefit_pp(1, "MATURITY")


# ---------------------------------------------------------------------------
# What the product does not have


def test_lapse_pays_nothing(critical_illness):
    """No surrender or paid-up value at any duration, on any model point."""
    for point_id in critical_illness.Data.model_point_table().index:
        proj = critical_illness.Projection[point_id]
        assert (proj.result_cf()["claims_lapse"] == 0.0).all()


def test_the_product_carries_no_commission_line(critical_illness):
    """Acquisition cost is folded into the GBP 200 initial expense by these notes.

    The term assurance chassis carries commission separately; these notes do not, and
    inventing a commission scale to match the chassis would be adding an assumption the
    notes do not make.
    """
    names = set(critical_illness.Projection.cells) | set(
        critical_illness.Projection.refs)
    assert not [n for n in names if "comm" in n]
    assert "commissions" not in critical_illness.Projection[1].result_cf().columns


def test_there_is_no_account_value_or_dynamic_lapse(critical_illness):
    """No cash value and no credited rate, so nothing to arbitrage and no machinery."""
    names = set(critical_illness.Projection.cells) | set(
        critical_illness.Projection.refs)
    for absent in ("av_pp_at", "av_at", "cv_pp", "asset_share", "mvr",
                   "dyn_lapse_factor", "surr_charge_rate"):
        assert absent not in names


def test_expiry_at_the_end_of_the_term(uk_ci_anchor):
    """proj_len() = 12 x term, and nothing survives past it."""
    a = uk_ci_anchor
    assert a.proj_len() == 300 == 12 * a.policy_term()
    assert a.pols_if(300) > 0.0
    assert a.pols_if(301) == 0.0
    assert a.pols_if_at(300, "AFT_DECR") == 0.0
    for t in range(1, 300):
        assert a.pols_maturity(t) == 0.0
    assert a.pols_maturity(300) > 0.0


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_ci_anchor):
    df = uk_ci_anchor.result_cf()
    assert list(df.index) == list(range(1, 301))
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_main", "claims_ap", "claims_child",
        "claims_lapse", "claim_expenses", "expenses", "net_cf",
    ]
    assert df.loc[1, "net_cf"] == pytest.approx(-168.12, abs=PENNY)


def test_result_cf_rows_sum_to_net_cf(uk_ci_anchor):
    """The cash flow columns are a decomposition of net_cf, not a selection from it."""
    df = uk_ci_anchor.result_cf()
    outgo = df[["claims_main", "claims_ap", "claims_child", "claims_lapse",
                "claim_expenses", "expenses"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)


def test_model_docstring_describes_the_current_structure(critical_illness):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = critical_illness.doc
    assert "critical illness" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "non-terminating" in doc
    assert "Term_UK_A" in doc                    # the chassis it sits on


def test_space_docstrings_carry_their_reference_material(critical_illness):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = critical_illness.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("pols_if", "claim_rate", "claim_rate_paid", "ap_rate",
                  "pivot_interp", "benefit_pp"):
        assert cells in proj
    data = critical_illness.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "ci_rate_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_the_library_vocabulary(critical_illness):
    """Names shared with lifelib and with the rest of this library must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "sum_assured", "policy_term",
        "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init", "pols_lapse",
        "pols_maturity", "mort_rate", "lapse_rate", "lapse_rate_mth", "premiums",
        "claims", "benefit_pp", "expenses", "expense_acq", "expense_maint",
        "inflation_rate", "inflation_factor", "net_cf", "result_cf",
        "policy_year", "duration", "duration_mth",
    }
    names = set(critical_illness.Projection.cells) | set(
        critical_illness.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """The three input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "ci_rate_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_inputs_are_read_once_not_once_per_model_point():
    """The readers live in Data, so N model points do not cause N reads."""
    from collections import Counter

    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="CI_UK_S_reads")
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
    assert len(reads) == 3           # one per input file, regardless of point count


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is what a production user does with a licensed AC04 or "16" Series basis: it
    drops in as a same-schema 24-row CSV with no formula change.
    """
    import pandas as pd

    src = MODEL_DIR.parent / "ci_rate_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "smoker", "age"])
    doubled["i_ci"] = doubled["i_ci"] * 2

    model = mx.read_model(MODEL_DIR, name="CI_UK_S_swap")
    try:
        alt_name = "ci_rate_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].ci_rate(1)
            model.Data.ci_rate_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].ci_rate(1) == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_every_model_point_projects(critical_illness):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in critical_illness.Data.model_point_table().index:
        proj = critical_illness.Projection[point_id]
        df = proj.result_cf()
        assert len(df) > 0
        assert df.notna().all().all()
        assert proj.check_pols_roll_fwd() is True
        assert proj.check_claim_split() is True


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="CI_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="CI_UK_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            initial = 200.0 if t == 1 else 0.0
            assert anchor.net_cf(t) + initial == pytest.approx(row[7], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
