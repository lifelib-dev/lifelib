"""Golden and product-specific tests for IUL_US_S.

The golden values are the worked example in products/indexed_ul/technical-notes.md
("Worked example"), which prices one segment year at cap 10.00%, participation 100% and
floor 0% under two index scenarios, plus the two variant credit bases the notes price
alongside it in the same paragraph: Transamerica's half-weighted adjusted beginning
value (1,191.00) and the guaranteed-cap-only credit (236.40).  They are hard-coded here
rather than pickled so a reviewer can compare them against the notes by eye.

The worked example is a **standalone illustration of the crediting engine** -- the
12,000.00 creation balance and the 15.00 x 12 of deductions are stipulated example
values, not projection output -- so it is asserted against the engine cells with those
exact inputs.  The full monthly projection is pinned separately by the notes' own
parameters at the anchor model point, by the four roll-forward self-checks, and by one
test per entry in the notes' "Known modeling pitfalls" list.

Tolerances follow the precision the notes display: money to the cent, rates to the
displayed decimals.
"""
import math

import modelx as mx
import pytest

from us_registry import LIB

def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9).  Those caches are not part of the
    model and must not make a round-trip comparison fail for anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


MODEL_PATH = LIB / "products/indexed_ul/IUL_US_S"

CENT = 0.005          # money displayed to 2 d.p.
RATE = 5e-7           # rates displayed as percentages to 2 d.p.
INFORCE = 5e-7

# --------------------------------------------------------------------------
# technical-notes.md, "Worked example": one segment year, two index scenarios.
# key -> (seg_bal_init, deductions, index_start, index_end,
#         balance_at_maturity, index_change, credited_rate, credit, matured_value)
WORKED_EXAMPLE = {
    "A": (12000.00, 180.00, 4500.00, 5040.00, 11820.00,  0.1200, 0.1000, 1182.00, 13002.00),
    "B": (12000.00, 180.00, 4500.00, 3825.00, 11820.00, -0.1500, 0.0000,    0.00, 11820.00),
}

# The same paragraph's two variant credits, both on scenario A.
WORKED_EXAMPLE_ADJ_BEGIN_CREDIT = 1191.00      # 10.00% x (12,000.00 - 90.00) [S3]
WORKED_EXAMPLE_GUAR_CAP_CREDIT = 236.40        # 2.00% x 11,820.00 [S2 guaranteed cap]

# --------------------------------------------------------------------------
# The anchor model point traced through the notes' own parameters: M45 / NT /
# 250,000 / Option A / GPT, 10,000 annual premium, load 5%, policy fee 10.00,
# per-unit 0.30 x 250 = 75.00, cap 10.00% on a 6.40% level index return.
# t -> (av_bef_prem, net_prem, index_credit, av_bef_fee, db, naar, coi, md,
#       av_bef_inv, interest, av)
ANCHOR = {
    1:  (0.00, 9500.00, 0.00,  9500.00, 250000.00, 240292.79, 31.36, 116.36,  9383.64, 0.00,  9383.64),
    2:  (9383.64,  0.00, 0.00,  9383.64, 250000.00, 240409.15, 31.38, 116.38,  9267.26, 0.00,  9267.26),
    12: (8219.17,  0.00, 0.00,  8219.17, 250000.00, 241573.62, 31.53, 116.53,  8102.64, 0.00,  8102.64),
    13: (8102.64, 9310.00, 518.57, 17931.21, 250000.00, 231861.58, 32.75, 117.75, 17813.46, 0.00, 17813.46),
    14: (17813.46, 0.00, 0.00, 17813.46, 250000.00, 231979.33, 32.77, 117.77, 17695.68, 0.00, 17695.68),
}


@pytest.fixture(scope="module")
def indexed_ul():
    """The IUL_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(indexed_ul):
    """Model point 1 - the baseline cell."""
    proj = indexed_ul.Projection[1]
    proj.result_cf()          # walk t in order so no cells recurses deeply
    return proj


# ===========================================================================
# The worked example


@pytest.mark.parametrize("scenario", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, scenario):
    """Every row and column of the notes' worked example, to the displayed precision."""
    (bal0, ded, i_start, i_end, bal_mat, chg, rate, credit,
     matured) = WORKED_EXAMPLE[scenario]

    # Segment balance at creation and the deductions charged to it are the notes'
    # stipulated example values; the rows below are all computed.
    assert anchor.seg_credit_base(bal0, ded) == pytest.approx(bal_mat, abs=CENT)
    assert anchor.index_change(i_start, i_end) == pytest.approx(chg, abs=RATE)
    assert anchor.index_credit_rate(chg) == pytest.approx(rate, abs=RATE)
    assert anchor.index_credit_rate(
        anchor.index_change(i_start, i_end)) == pytest.approx(rate, abs=RATE)
    assert anchor.index_credit(bal0, ded, chg) == pytest.approx(credit, abs=CENT)
    assert anchor.seg_matured_value(bal0, ded, chg) == pytest.approx(matured, abs=CENT)


def test_worked_example_cap_and_floor_are_what_bind(anchor):
    """The notes label scenario A "cap binds" and scenario B "floor binds"."""
    assert anchor.index_credit_rate(0.1200) == anchor.index_cap_at(1) == 0.10
    assert anchor.index_credit_rate(-0.1500) == anchor.index_floor == 0.0
    # 100% participation, so between the two the credited rate is the index change.
    assert anchor.index_par == 1.0
    assert anchor.index_credit_rate(0.064) == pytest.approx(0.064, abs=RATE)


def test_worked_example_transamerica_credit_base_variation(anchor):
    """The notes' variant: 10.00% x (12,000.00 - 90.00) = 1,191.00 [S3].

    Transamerica's contractual adjusted beginning value subtracts one *half* of the
    monthly deductions taken during the segment, where the baseline subtracts them in
    full.  Both conventions are shipped; ``seg_credit_base_conv`` records the choice,
    and the notes list keeping the credit, death benefit and cash value formulas
    consistent with it among the modeling pitfalls.
    """
    bal0, ded = 12000.00, 180.00
    assert anchor.seg_credit_base(bal0, ded, "ADJ_BEGIN") == pytest.approx(
        11910.00, abs=CENT)
    assert anchor.index_credit(bal0, ded, 0.12, "ADJ_BEGIN") == pytest.approx(
        WORKED_EXAMPLE_ADJ_BEGIN_CREDIT, abs=CENT)
    # ... and the baseline convention is the one the model runs on.
    assert anchor.seg_credit_base_conv == "REMAINING"
    assert anchor.index_credit(bal0, ded, 0.12) == pytest.approx(1182.00, abs=CENT)


def test_worked_example_guaranteed_cap_credit(anchor):
    """The notes' guaranteed-basis figure: 2.00% x 11,820.00 = 236.40 [S2]."""
    assert anchor.index_cap_guar == 0.02
    assert anchor.index_credit_rate(0.12, anchor.index_cap_guar) == pytest.approx(
        0.02, abs=RATE)
    assert anchor.index_credit(12000.00, 180.00, 0.12, None,
                               anchor.index_cap_guar) == pytest.approx(
        WORKED_EXAMPLE_GUAR_CAP_CREDIT, abs=CENT)


def test_seg_credit_base_rejects_an_unknown_convention(anchor):
    with pytest.raises(Exception):
        anchor.seg_credit_base(12000.0, 180.0, "HALF_WEIGHTED")


# ===========================================================================
# The anchor model point


@pytest.mark.parametrize("t", sorted(ANCHOR))
def test_anchor_account_value_row(anchor, t):
    """The account value roll-forward at the notes' own parameters, to the cent."""
    (av0, np_, credit, av_fee, db, naar, coi, md, av_inv, interest,
     av) = ANCHOR[t]
    assert anchor.av_pp_at(t, "BEF_PREM") == pytest.approx(av0, abs=CENT)
    assert anchor.prem_to_av_pp(t) == pytest.approx(np_, abs=CENT)
    assert anchor.index_credit_pp(t) == pytest.approx(credit, abs=CENT)
    assert anchor.av_pp_at(t, "BEF_FEE") == pytest.approx(av_fee, abs=CENT)
    assert anchor.db_pp(t) == pytest.approx(db, abs=CENT)
    assert anchor.net_amt_at_risk(t) == pytest.approx(naar, abs=CENT)
    assert anchor.coi_pp(t) == pytest.approx(coi, abs=CENT)
    assert anchor.mth_deduction_pp(t) == pytest.approx(md, abs=CENT)
    assert anchor.av_pp_at(t, "BEF_INV") == pytest.approx(av_inv, abs=CENT)
    assert anchor.inv_income_pp(t) == pytest.approx(interest, abs=CENT)
    assert anchor.av_pp(t) == pytest.approx(av, abs=CENT)


def test_anchor_month_1_trace(anchor):
    """The month-1 arithmetic, at full precision, term by term.

    Premium 10,000.00 less the 5% load is 9,500.00; the death benefit is the face
    amount because the 215% corridor factor at attained age 45 on 9,500.00 is far below
    it; the net amount at risk discounts the death benefit one month at the *guaranteed*
    1.00% and subtracts the account value *before* the deduction; the monthly deduction
    is the $10 policy fee plus $0.30 x 250 units plus the cost of insurance; and the
    whole post-deduction balance is swept into the first segment, so no fixed-account
    interest is credited.
    """
    assert anchor.premium_pp(1) == 10000.0
    assert anchor.load_prem_rate() == 0.05
    assert anchor.prem_to_av_pp(1) == pytest.approx(9500.0, abs=1e-9)
    assert anchor.corridor_factor(1) == 2.15
    assert anchor.db_pp(1) == 250000.0
    assert anchor.naar_factor() == pytest.approx(1.01 ** (1 / 12), rel=1e-12)
    assert anchor.net_amt_at_risk(1) == pytest.approx(
        250000.0 / 1.01 ** (1 / 12) - 9500.0, rel=1e-12)
    assert anchor.maint_fee_pp(1) == pytest.approx(10.0 + 0.30 * 250, abs=1e-9)
    assert anchor.coi_rate(1) == pytest.approx(0.65 * anchor.coi_rate_guar(1), rel=1e-12)
    assert anchor.coi_pp(1) == pytest.approx(
        anchor.coi_rate(1) / 1000 * anchor.net_amt_at_risk(1), rel=1e-12)
    assert anchor.mth_deduction_pp(1) == pytest.approx(116.363015, abs=1e-5)
    assert anchor.sweep_pp(1) == pytest.approx(9383.636985, abs=1e-5)
    assert anchor.inv_income_pp(1) == 0.0
    assert anchor.av_pp(1) == pytest.approx(9383.636985, abs=1e-5)


def test_first_segment_credit_reproduces_from_its_own_ladder(anchor):
    """Month 13: the segment born at month 1 matures and is credited 6.40%.

    It bore eleven in-segment deductions, one for each of months 2 to 12; the
    month-13 deduction is taken after it has already matured and rolled into the
    fixed account.  Its credit is the level index return because 0% < 6.40% < 10.00%.
    """
    assert anchor.seg_new_pp(1) == pytest.approx(9383.636985, abs=1e-5)
    assert anchor.seg_bal_pp(12, 1) == pytest.approx(8102.641000, abs=1e-5)
    assert anchor.seg_ded_cum_pp(12, 1) == pytest.approx(1280.995985, abs=1e-5)
    assert anchor.seg_return(13) == pytest.approx(0.064, rel=1e-12)
    assert anchor.index_credit_pp(13) == pytest.approx(
        0.064 * 8102.641000, abs=1e-5)
    # the credit base is the remaining balance, so the eleven deductions earn nothing
    assert anchor.index_credit_pp(13) == pytest.approx(
        anchor.index_credit(anchor.seg_new_pp(1), anchor.seg_ded_cum_pp(12, 1), 0.064),
        rel=1e-12)


# ===========================================================================
# Known modeling pitfalls - the notes' list, one test each


def test_pitfall_segment_bookkeeping_keeps_per_segment_index_levels(indexed_ul):
    """Pitfall 1: a monthly ladder, up to 12 concurrent, each with its own I(m).

    Model point 4 pays monthly, so a segment is created every month and twelve are
    live from month 12 onwards.  Each carries its own index start level, so the twelve
    credits paid in a year are twelve separate point-to-point calculations, not one.
    """
    p = indexed_ul.Projection[4]
    p.result_cf()
    assert p.premium_mode() == "MONTHLY"
    assert p.seg_count(1) == 1
    assert p.seg_count(12) == p.seg_term_mth == 12
    assert max(p.seg_count(t) for t in range(1, 200)) == 12
    starts = {p.index_level(m) for m in range(1, 13)}
    assert len(starts) == 12                         # twelve distinct start levels
    credits = [p.index_credit_pp(t) for t in range(13, 25)]
    assert all(c > 0 for c in credits)               # twelve separate credits
    assert p.check_seg_ladder()


def test_pitfall_segment_bookkeeping_no_segment_when_nothing_is_allocated(indexed_ul):
    """The control run: model point 3 allocates 0% to the indexed account.

    Nothing is ever swept, no segment is ever created, no index credit is ever paid,
    and the whole balance compounds at the fixed-account rate instead.  Read against
    model point 1 it isolates what the segment ladder is doing.
    """
    p = indexed_ul.Projection[3]
    p.result_cf()
    assert p.index_alloc_rate() == 0.0
    assert all(p.seg_count(t) == 0 for t in range(1, 200))
    assert all(p.sweep_pp(t) == 0.0 for t in range(1, 200))
    assert all(p.index_credit_pp(t) == 0.0 for t in range(1, 200))
    assert p.fa_pp(1) == pytest.approx(p.av_pp(1), abs=1e-9)
    # the fixed account earns one month's interest at (1 + 4.50%)^(1/12) - 1
    assert p.inv_return_mth(1) == pytest.approx(1.045 ** (1 / 12) - 1, rel=1e-12)
    assert p.inv_income_pp(1) == pytest.approx(
        p.fa_pp_at(1, "BEF_INV") * p.inv_return_mth(1), rel=1e-12)


def test_pitfall_deduction_sourcing_matches_the_credit_base(anchor):
    """Pitfall 2: one sourcing convention, and the credit base agrees with it.

    Deductions are taken from the fixed account first and then pro rata from live
    segments; the credit base is the balance those deductions leave behind.  The two
    must reconcile exactly, which is what :func:`check_seg_ladder` asserts segment by
    segment.
    """
    for t in (2, 6, 12, 14, 30):
        assert (anchor.mth_deduction_from_fa_pp(t)
                + anchor.mth_deduction_from_seg_pp(t)) == pytest.approx(
            anchor.mth_deduction_pp(t), rel=1e-12)
    # months 2-12: nothing in the fixed account, so the whole deduction is pro rata
    assert anchor.fa_pp(1) == pytest.approx(0.0, abs=1e-9)
    assert anchor.mth_deduction_from_fa_pp(5) == pytest.approx(0.0, abs=1e-9)
    assert anchor.mth_deduction_from_seg_pp(5) == pytest.approx(
        anchor.mth_deduction_pp(5), rel=1e-12)
    assert anchor.check_seg_ladder()


def test_the_two_draws_on_the_segment_pool_cannot_together_overdraw_it(indexed_ul):
    """Pitfall 2, the sharp edge: step 3 and step 6 share one pool, in that order.

    The withdrawal and the new loan collateral are sourced from the live segments at
    step 3; the monthly deduction from the same segments at step 6.  Both are capped
    against ``seg_bal_active_pp(t)``, which is measured at the end of month ``t - 1``
    -- so the deduction must be capped against what the *draw leaves*, not against the
    pre-draw pool.

    Capping both against the pre-draw pool let the two together take more than the
    segments held.  On model point 5 at month 384 the pool was 265.29, the draw took
    200.00 and the deduction was allowed 177.38 -- 377.38 out of 265.29 -- which drove
    the segment born at month 373 to -112.09 and, at its maturity in month 385, paid an
    index credit of 0.0640 x (-112.0873) = -7.17.  A negative index credit breaches the
    contractual 0% floor of ``cr_k = max(f, min(c, p x r))`` [S2][R1].
    """
    p = indexed_ul.Projection[5]
    p.result_cf()

    # the month the old cap broke, term by term
    t = 384
    assert p.seg_bal_active_pp(t) == pytest.approx(265.29, abs=CENT)
    assert p.draw_from_seg_pp(t) == pytest.approx(200.00, abs=CENT)
    assert p.mth_deduction_from_seg_pp(t) == pytest.approx(65.29, abs=CENT)
    assert p.seg_bal_pp(t, 373) == pytest.approx(0.0, abs=1e-8)
    assert p.index_credit_pp(385) >= 0.0 - 1e-8          # was -7.17

    # ... and the invariant behind it, every month of the projection
    for u in range(1, p.proj_len() + 1):
        assert (p.draw_from_seg_pp(u) + p.mth_deduction_from_seg_pp(u)
                <= p.seg_bal_active_pp(u) + 1e-8)
        assert p.index_credit_pp(u) >= -1e-8
        for m in range(max(1, u - p.seg_term_mth + 1), u + 1):
            assert p.seg_bal_pp(u, m) >= -1e-8

    # the deduction is still charged in full: the fixed account carries the excess
    assert (p.mth_deduction_from_fa_pp(t)
            + p.mth_deduction_from_seg_pp(t)) == pytest.approx(
        p.mth_deduction_pp(t), rel=1e-12)
    assert p.fa_pp_at(t, "BEF_SWEEP") < 0.0

    # and check_seg_ladder() now carries the two bounds, so it fails on the old
    # behaviour instead of closing its accounting identity over a negative balance
    assert p.check_seg_ladder()


def test_pitfall_floor_is_not_an_in_segment_guarantee(anchor):
    """Pitfall 3: a 0% annual floor is not an in-segment 0.75% credit.

    Segments earn no interim interest at all: the whole of a segment's return arrives
    as an index credit at maturity.  Mixing the two double-counts the guarantee.
    """
    assert anchor.index_floor == 0.0
    # a live segment loses exactly its deductions, month after month, and gains nothing
    for t in range(2, 12):
        assert anchor.seg_bal_pp(t, 1) == pytest.approx(
            anchor.seg_bal_pp(t - 1, 1) - anchor.seg_ded_pp(t, 1), rel=1e-12)
    # interest credited to the account value comes from the fixed and collateral
    # accounts only, never from a segment
    for t in (3, 7, 11):
        assert anchor.inv_income_pp(t) == pytest.approx(
            anchor.fa_pp_at(t, "BEF_INV") * anchor.inv_return_mth(t)
            + anchor.lca_pp_at(t, "BEF_INV") * anchor.loan_credit_rate_mth(t),
            rel=1e-12)
    # and there is no shadow accumulation account: the retrospective 2% cumulative
    # guarantee is a documented variation, not the baseline.
    assert "shadow" not in set(anchor.cells)


def test_pitfall_illustrated_rate_anchoring(anchor):
    """Pitfall 4: the level rate is a disclosure anchor, not a best estimate.

    The base run credits 6.40% -- the carrier-published lookback [S2] -- because a
    6.40% index return sits between the 0% floor and the 10.00% cap.  A stochastic
    run at the same expected index growth credits less, because the cap truncates the
    right tail while the floor only offsets the left: the model makes that visible by
    routing the level rate through the same crediting formula rather than crediting it
    directly.
    """
    assert anchor.index_return_ann == 0.064
    assert anchor.index_credit_rate(anchor.index_return_ann) == pytest.approx(
        0.064, abs=RATE)
    # the formula is piecewise linear, not linear: symmetric index shocks around the
    # level return do not give symmetric credits.
    up = anchor.index_credit_rate(0.064 + 0.16)
    down = anchor.index_credit_rate(0.064 - 0.16)
    assert up == 0.10                                  # cap truncates the upside
    assert down == 0.0                                 # floor offsets the downside
    assert (up + down) / 2 < anchor.index_credit_rate(0.064)


def test_pitfall_corridor_interplay(indexed_ul):
    """Pitfall 5: the corridor raises the death benefit, the net amount at risk and COI.

    Model point 2 is Option B, where the death benefit is face plus account value, so
    the net amount at risk does not run off as the account value grows -- and the
    corridor factor is live in the death benefit formula for both options.
    """
    p = indexed_ul.Projection[2]
    p.result_cf()
    assert p.db_option() == "B"
    assert p.db_pp(1) == pytest.approx(
        p.sum_assured() + p.av_pp_at(1, "BEF_FEE"), abs=CENT)
    # Option B keeps the net amount at risk near the face amount as the fund grows,
    # where Option A lets it run off.
    a = indexed_ul.Projection[1]
    a.result_cf()
    assert p.net_amt_at_risk(600) > a.net_amt_at_risk(600)
    assert p.coi_pp(600) > a.coi_pp(600)
    # the corridor table is the IRC 7702(d) grading, 250% to 40 down to 100% at 90-95
    assert a.corridor_factor(1) == 2.15                # attained age 45
    assert indexed_ul.Data.corridor_factors().loc[40, "corridor_factor"] == 2.50
    assert indexed_ul.Data.corridor_factors().loc[95, "corridor_factor"] == 1.00


def test_pitfall_maturity_mechanics(anchor):
    """Pitfall 6: age-121 behaviour is [unverified], so nothing depends on it.

    The projection horizon runs to attained age 121 and stops; no policy is treated as
    maturing, because the spec says the contract continues in force with no further
    charges.  ``pols_maturity`` is identically zero and the run is truncated by the
    horizon, not by a contractual event.
    """
    assert anchor.maturity_age == 121
    assert anchor.proj_len() == 12 * (121 - 45)
    assert anchor.age(anchor.proj_len()) == 120
    assert anchor.age(1) == 45
    assert all(anchor.pols_maturity(t) == 0.0 for t in range(1, anchor.proj_len() + 1))


# ===========================================================================
# Chassis conventions carried over from universal life


def test_naar_uses_the_guaranteed_rate_and_the_pre_deduction_account_value(anchor):
    """The universal life base convention, unchanged: DB x v_g - AV', floored at 0.

    Discounting at the credited or index rate, or measuring the account value after
    the deduction, produces small systematic cost-of-insurance errors.  The guaranteed
    rate here is 1.00%, not the chassis' 2.00%.
    """
    assert anchor.guar_rate_ann == 0.01
    assert anchor.naar_factor() == pytest.approx(1.01 ** (1 / 12), rel=1e-12)
    for t in (1, 13, 200):
        assert anchor.net_amt_at_risk(t) == pytest.approx(
            max(0.0, anchor.db_pp(t) / anchor.naar_factor()
                - anchor.av_pp_at(t, "BEF_FEE")), rel=1e-12)
    # the discount is not at the fixed-account rate
    assert anchor.naar_factor() != pytest.approx(1.045 ** (1 / 12), rel=1e-6)


def test_interest_is_credited_after_the_deduction(indexed_ul):
    """The chassis' first pitfall: interest on the post-deduction balance.

    Model point 3 keeps everything in the fixed account, which is where the ordering is
    visible: the closing balance is ``(opening + net premium - deduction) x (1 + i_m)``,
    not ``(opening + net premium) x (1 + i_m) - deduction``.
    """
    p = indexed_ul.Projection[3]
    p.result_cf()
    for t in (1, 2, 50):
        correct = (p.av_pp_at(t, "BEF_FEE") - p.mth_deduction_pp(t)) * (
            1 + p.inv_return_mth(t))
        wrong = p.av_pp_at(t, "BEF_FEE") * (1 + p.inv_return_mth(t)) - p.mth_deduction_pp(t)
        assert p.av_pp(t) == pytest.approx(correct, rel=1e-12)
        assert p.av_pp(t) < wrong


def test_surrender_charge_runs_off_over_ten_years(anchor):
    """$25.00 per $1,000 of initial face, linear to zero at the end of policy year 10.

    The notes' month index counts the current month, so the issue month already carries
    one twelfth of a year's run-off.
    """
    assert anchor.surr_charge_rate(1) == pytest.approx(25.0 - 2.5 / 12, abs=1e-9)
    assert anchor.surr_charge_pp(1) == pytest.approx(6197.92, abs=CENT)
    assert anchor.surr_charge_rate(120) == pytest.approx(0.0, abs=1e-9)
    assert anchor.surr_charge_rate(121) == 0.0
    assert anchor.lapse_shock_year() == 11


def test_lapse_has_the_surrender_charge_expiry_spike(anchor):
    """6% in policy years 1-10, 4% after, doubled in policy year 11 **[std]**."""
    assert anchor.lapse_rate_base(1) == 0.06
    assert anchor.lapse_rate_base(120) == 0.06          # policy year 10
    assert anchor.lapse_rate_base(121) == 0.04          # policy year 11
    assert anchor.lapse_rate_sc_mult(121) == 2.0
    assert anchor.lapse_rate(120) == pytest.approx(0.06, abs=1e-12)
    assert anchor.lapse_rate(121) == pytest.approx(0.08, abs=1e-12)
    assert anchor.lapse_rate(133) == pytest.approx(0.04, abs=1e-12)   # policy year 12


def test_dynamic_lapse_is_neutral_in_the_base_run(anchor):
    """r_alt = r_cred in the base run, so the multiplier is exactly 1.

    The trailing credited rate is the maturing segment's own credited rate once the
    ladder is running, and the fixed-account rate before that.
    """
    assert anchor.cred_rate_ann(1) == pytest.approx(0.045, rel=1e-12)
    assert anchor.cred_rate_ann(200) == pytest.approx(0.064, rel=1e-9)
    assert anchor.comp_rate_ann(200) == anchor.cred_rate_ann(200)
    assert anchor.lapse_rate_dyn_mult(200) == pytest.approx(1.0, abs=1e-12)
    assert anchor.lapse_dyn_cap == 2.0 and anchor.lapse_dyn_floor == 0.5


def test_premium_persistency_compounds_at_98_percent(anchor):
    """The notes give it in closed form: expected premium_y = planned x 0.98^(y-1)."""
    assert anchor.prem_persistency(1) == 1.0
    assert anchor.prem_persistency(13) == pytest.approx(0.98, rel=1e-12)
    assert anchor.prem_persistency(121) == pytest.approx(0.98 ** 10, rel=1e-12)
    assert anchor.premium_pp(13) == pytest.approx(10000 * 0.98, abs=CENT)


def test_premium_falls_only_on_the_policy_anniversary(anchor):
    """Annual mode **[std]**: the whole premium at BOM of month 1 of each policy year."""
    assert anchor.premium_mode() == "ANNUAL"
    assert anchor.premium_pp(1) == 10000.0
    assert all(anchor.premium_pp(t) == 0.0 for t in range(2, 13))
    assert anchor.premium_pp(13) > 0.0
    assert all(anchor.premium_pp(t) == 0.0 for t in range(14, 25))


# ===========================================================================
# No-lapse guarantee


def test_no_lapse_guarantee_suppresses_lapse_while_it_is_in_effect(indexed_ul):
    """The notes' NLG-tested behaviour, exercised by model point 5.

    Model point 5 is funded at 6,000 a year on a 250,000 face, so the $25 per $1,000
    surrender charge exceeds the account value throughout policy year 1 and the cash
    surrender value is zero.  Cumulative premium still clears cumulative MNLP, so the
    guarantee is in effect and voluntary lapse is suppressed; from month 13 the cash
    surrender value turns positive and normal lapse resumes.
    """
    p = indexed_ul.Projection[5]
    p.result_cf()
    assert p.mnlp_rate() == 20.80
    assert p.mnlp_pp_mth() == pytest.approx(20.80 * 250 / 12, rel=1e-12)
    assert p.nlg_period_years() == 20
    for t in range(1, 13):
        assert p.ncsv_pp(t) == 0.0
        assert p.nlg_in_effect(t) is True
        assert p.lapse_rate(t) == 0.0
        assert p.pols_lapse(t) == 0.0
    assert p.ncsv_pp(13) > 0.0
    assert p.lapse_rate(13) == pytest.approx(0.06, abs=1e-12)


def test_the_two_cumulative_premium_accumulators_differ(indexed_ul):
    """CumP_t nets loans as well as withdrawals; the GPT / 7-pay base does not."""
    p = indexed_ul.Projection[5]
    p.result_cf()
    t = 241                                    # policy year 21, first loan drawn
    assert p.loan_new_pp(t) == 6000.0
    assert p.cum_prem_pp(t) - p.cum_prem_net_pp(t) == pytest.approx(6000.0, abs=CENT)


def test_guideline_and_seven_pay_are_flags_not_cash_flows(anchor):
    """The anchor stays inside both limits and neither generates a cash flow."""
    assert anchor.gpt_limit(1) == max(anchor.gsp(), anchor.glp())
    assert all(anchor.gpt_ok(t) for t in (1, 121, 601))
    assert not anchor.is_mec(1) and not anchor.is_mec(80)
    assert anchor.seven_pay_limit(85) == anchor.seven_pay_prem() * 7   # capped at 7


# ===========================================================================
# Loans


def test_standard_loan_moves_collateral_without_reducing_the_account_value(indexed_ul):
    """A loan advance moves value into the collateral account, inside AV.

    The account value is unchanged by the advance -- the cash surrender value falls,
    because the loan is netted from it -- and the advance is a liability cash flow of
    its own.
    """
    p = indexed_ul.Projection[5]
    p.result_cf()
    t = 241
    assert p.lca_pp(t - 1) == 0.0
    assert p.loan_new_pp(t) == 6000.0
    assert p.av_pp_at(t, "BEF_FEE") == pytest.approx(
        p.av_pp_at(t, "BEF_WD") - p.wd_pp(t), rel=1e-12)   # the loan is not subtracted
    assert p.lca_pp(t) > 6000.0                             # collateral plus interest
    assert p.loan_bal_pp(t) > 6000.0
    assert p.net_loan_cf(t) == pytest.approx(-6000.0 * p.pols_if(t), rel=1e-12)
    assert p.loan_credit_rate_ann(t) == 0.03                # policy year 21, the wash
    assert p.loan_credit_rate_ann(1) == 0.02
    assert p.loan_rate_ann == 0.03


def test_heavy_late_life_loans_can_overrun_the_cash_value(indexed_ul):
    """The notes' loan sensitivity: without overloan protection the debt overtakes AV.

    Model point 5 borrows 6,000 a year from policy year 21; by policy year 32 the loan
    balance exceeds the cash value, the net cash surrender value floors at zero and the
    shortfall test fires.  The Overloan Protection Rider that prevents this is described
    in the product spec and not modeled, so the model point shows the exposure.
    """
    p = indexed_ul.Projection[5]
    p.result_cf()
    overloan = [t for t in range(241, p.proj_len() + 1)
                if p.loan_bal_pp(t) > p.csv_pp(t)]
    assert overloan, "model point 5 should eventually go overloaned"
    t = overloan[0]
    assert t == 384 and p.policy_year(t) == 32
    assert p.ncsv_pp(t) == 0.0
    assert any(p.is_shortfall(u) for u in range(t, min(t + 24, p.proj_len())))


def test_point_5_account_value_runs_away_after_month_605(indexed_ul):
    """The disclosed boundary: point 5's ``result_av()`` stops meaning anything at 605.

    No policy is terminated for insufficiency in this model -- the grace and
    lapse-for-insufficiency cascade is in the *Not implemented* list, because the notes
    leave the in-grace account value treatment and the cure-payment cash flow
    undetermined.  So an exhausted policy goes on being charged: the deduction is taken
    in full, the fixed account carries what the segments cannot, and the account value
    turns negative.  From there it compounds, because
    ``NAAR_t = max(0, DB_t x v_g - AV'_t)`` rises one for one as ``AV'_t`` falls and the
    cost of insurance is charged against ``AV'_t`` again the next month.

    This test pins the boundary rather than the fix.  Flooring the account value would
    stop the compounding but is a rule the notes do not give, and it would break
    :func:`check_av_components` and :func:`check_av_roll_fwd`.  The behaviour is
    disclosed in the model docstring and the README instead, and asserted here so it
    cannot move -- in either direction -- without a test failing.
    """
    p = indexed_ul.Projection[5]
    p.result_cf()

    boundary = 605
    assert all(p.av_pp(t) > 0 for t in range(1, boundary))
    assert p.av_pp(boundary) < 0
    assert p.av_pp(boundary) == pytest.approx(-241.18, abs=CENT)
    assert p.policy_year(boundary) == 51
    assert p.av_pp(p.proj_len()) < -1e10          # about -1.3e10 at the horizon

    # the cash flows are a different matter and stay finite and bounded: the death
    # benefit is the (withdrawal-reduced) face amount, the corridor multiplies a
    # negative account value so it never binds, and both claim legs floor at zero.
    df = p.result_cf()
    assert math.isfinite(df["net_cf"].sum())
    assert df["net_cf"].abs().max() < 1e5
    assert p.db_pp(p.proj_len()) == pytest.approx(70000.0, abs=CENT)
    assert p.claim_pp(p.proj_len(), "DEATH") == 0.0
    assert p.ncsv_pp(p.proj_len()) == 0.0

    # points 1-4 never get near it
    for point_id in (1, 2, 3, 4):
        q = indexed_ul.Projection[point_id]
        q.result_cf()
        assert min(q.av_pp(t) for t in range(1, q.proj_len() + 1)) > 0

    # and the boundary is disclosed where a reader will find it
    assert "605" in indexed_ul.doc


def test_the_two_five_hundred_dollar_withdrawal_limits_are_not_enforced(indexed_ul):
    """The sourced $500 minimum and $500 CSV floor [S3] are named, not implemented.

    Spec Table 3 reads "$25 per withdrawal; minimum withdrawal $500; CSV may not fall
    below $500" [S3].  The $25 fee is implemented; neither $500 limit is.  ``wd_pp`` is
    whatever the model point's column says -- model point 5 deliberately asks for $200 a
    month, because a compliant $500 a month against a $6,000 annual premium empties the
    policy long before the year-21 loan module that point exists to exercise -- and
    ``ncsv_pp`` floors at zero rather than at $500.

    Both are limits on what a policyholder may *request*, and the notes give no
    behaviour for a refused request, so the mechanics are implemented and the limits are
    left to the data.  This test pins the gap open and pins the disclosure that names
    it, so the model docstring cannot claim the minimum is carried while no cells
    enforces it.
    """
    p = indexed_ul.Projection[5]
    p.result_cf()
    assert p.wd_pp(13) == 200.0 < 500.0            # below the sourced minimum
    assert p.wd_fee_pp(13) == 25.0                 # the fee, which *is* implemented
    assert p.ncsv_pp(384) == 0.0                   # floors at zero, not at 500

    names = set(indexed_ul.Projection.cells) | set(indexed_ul.Projection.refs)
    assert not any("wd_min" in n or "min_wd" in n or "csv_floor" in n for n in names)

    doc = indexed_ul.doc
    assert "$500 withdrawal minimum" in doc
    assert "The two $500 withdrawal limits" in doc


# ===========================================================================
# Roll-forwards and invariants


@pytest.mark.parametrize("point_id", [1, 2, 3, 4, 5])
def test_account_value_decomposition_holds(indexed_ul, point_id):
    """AV(t) = fixed account + live segments + loan collateral, every month.

    :func:`av_pp` is built from the notes' aggregate recursion while the three
    components are each built from their own; this is the strongest single check that
    the segment bookkeeping has not drifted.
    """
    p = indexed_ul.Projection[point_id]
    p.result_cf()
    assert p.check_av_components()


@pytest.mark.parametrize("point_id", [1, 2, 3, 4, 5])
def test_account_value_roll_forward_closes(indexed_ul, point_id):
    p = indexed_ul.Projection[point_id]
    p.result_cf()
    assert p.check_av_roll_fwd()


@pytest.mark.parametrize("point_id", [1, 2, 3, 4, 5])
def test_segment_ladder_closes(indexed_ul, point_id):
    """At most 12 live segments, each accounting for its creation balance exactly.

    ``check_seg_ladder()`` also carries the 0% floor as a bound -- no segment balance
    and no index credit may be negative -- because the accounting identity alone closes
    over a negative balance as happily as over a positive one.
    """
    p = indexed_ul.Projection[point_id]
    p.result_cf()
    assert p.check_seg_ladder()


@pytest.mark.parametrize("point_id", [1, 2, 3, 4])
def test_margin_identity_holds(indexed_ul, point_id):
    """net_cf reconciles to the expense and mortality margins on every unloaned point.

    Model point 5 is excluded on purpose: once its loan overruns the cash value the
    ``ncsv_pp`` floor binds and the identity opens up by the unrecoverable debt, which
    is exactly the exposure ``test_heavy_late_life_loans_can_overrun_the_cash_value``
    pins.
    """
    p = indexed_ul.Projection[point_id]
    p.result_cf()
    assert p.check_margin()


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + maturities, every month."""
    for t in range(1, anchor.proj_len() + 1):
        out = (anchor.pols_death(t) + anchor.pols_lapse(t)
               + anchor.pols_maturity(t))
        assert anchor.pols_if(t) - anchor.pols_if(t + 1) == pytest.approx(
            out, abs=1e-12)


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(1, anchor.proj_len() + 1):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15
    assert anchor.pols_if(1) == 1.0


def test_decrement_conversions_are_the_notes_own(anchor):
    """q_m = 1 - (1 - q)^(1/12) and i_m = (1 + i)^(1/12) - 1 **[std]**."""
    assert anchor.mort_rate_mth(1) == pytest.approx(
        1 - (1 - anchor.mort_rate(1)) ** (1 / 12), rel=1e-12)
    assert anchor.lapse_rate_mth(1) == pytest.approx(
        1 - (1 - anchor.lapse_rate(1)) ** (1 / 12), rel=1e-12)
    assert anchor.inv_return_mth(1) == pytest.approx(
        (1 + anchor.fixed_rate_ann(1)) ** (1 / 12) - 1, rel=1e-12)


def test_timing_arguments_reject_unknown_values(anchor):
    for cells, bad in ((anchor.av_pp_at, "BEF_MAT"), (anchor.fa_pp_at, "MID_MTH"),
                       (anchor.lca_pp_at, "BEF_FEE"), (anchor.pols_if_at, "EOM")):
        with pytest.raises(Exception):
            cells(1, bad)
    with pytest.raises(Exception):
        anchor.claims(1, "ANNUITIZATION")


# ===========================================================================
# The guaranteed basis


def test_guaranteed_basis_diverges_dramatically():
    """Key sensitivity 1: the guaranteed-basis run uses class (a) elements only.

    Cap 2.00% instead of 10.00%, fixed account 1.00% instead of 4.50%, premium load 8%
    instead of 5%, policy fee $15 instead of $10, the per-unit charge $0.40 in all
    years instead of $0.30 for ten, and the full guaranteed COI scale instead of 65% of
    it.  The notes say the two projections diverge dramatically; this asserts they do,
    and in the right direction.
    """
    model = mx.read_model(MODEL_PATH, name="IUL_US_S_guar")
    try:
        curr = model.Projection[1]
        curr.result_cf()
        base_av = curr.av_pp(120)
        model.Projection.basis = "GUARANTEED"
        model.Projection.clear_all()
        guar = model.Projection[1]
        guar.result_cf()
        assert guar.is_guaranteed_basis() is True
        assert guar.index_cap_at(1) == 0.02
        assert guar.fixed_rate_ann(1) == 0.01
        assert guar.load_prem_rate() == 0.08
        assert guar.expense_pol_mth_at(1) == 15.0
        assert guar.expense_unit_mth_at(1) == 0.40
        assert guar.expense_unit_mth_at(200) == 0.40      # all years, not just 1-10
        assert guar.coi_rate(1) == guar.coi_rate_guar(1)
        assert guar.index_credit_rate(0.064) == pytest.approx(0.02, abs=RATE)
        assert guar.av_pp(120) < base_av
    finally:
        model.close()


def test_basis_rejects_an_unknown_value():
    model = mx.read_model(MODEL_PATH, name="IUL_US_S_badbasis")
    try:
        model.Projection.basis = "BEST_ESTIMATE"
        with pytest.raises(Exception):
            model.Projection[1].load_prem_rate()
    finally:
        model.close()


# ===========================================================================
# Results and model points


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(1, anchor.proj_len() + 1))
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "withdrawals",
        "expenses", "premium_taxes", "net_loan_cf", "net_cf",
    ]
    assert df.loc[1, "premiums"] == pytest.approx(10000.0, abs=CENT)
    assert df.loc[1, "net_cf"] == pytest.approx(
        10000.0 - anchor.claims(1) - anchor.withdrawals(1) - anchor.expenses(1)
        - anchor.premium_taxes(1),
        abs=CENT)


def test_the_cash_flow_columns_sum_to_net_cf(indexed_ul):
    """Income-positive, and the lines reconcile to ``net_cf`` on every model point.

    ``pols_if`` is the in-force weight on the row, not a cash flow; every other column
    is a term of ``net_cf`` under the library-wide inflow-positive sign.  Model point 5
    is included: its account value runs away but its cash flows stay finite, so the
    identity has to hold there too.
    """
    for point_id in (1, 2, 3, 4, 5):
        p = indexed_ul.Projection[point_id]
        df = p.result_cf()
        recomputed = (df["premiums"] - df["claims_death"] - df["claims_lapse"]
                      - df["withdrawals"] - df["expenses"] - df["premium_taxes"]
                      + df["net_loan_cf"])
        assert (recomputed - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-8)


def test_a_withdrawal_is_not_a_claim(indexed_ul):
    """Withdrawals are ``withdrawals(t)``, not a ``kind`` of :func:`claims`.

    A partial withdrawal is a payment on the owner's election, so it is a cash flow of
    its own rather than a claim leg.  ``claims(t, "WITHDRAWAL")`` therefore raises, and
    the ``kind is None`` total is the death and surrender legs only -- if the kind were
    still accepted, ``net_cf`` would count the withdrawal twice, once through
    ``claims(t)`` and once through ``withdrawals(t)``.

    The per-policy rule stays in ``claim_pp``, because that is where the
    fee-inside-``W_t`` convention is stated; model point 5 is the one that takes a
    withdrawal.
    """
    p = indexed_ul.Projection[5]
    p.result_cf()
    t = 13                                       # first month of policy year 2

    with pytest.raises(Exception):
        p.claims(t, "WITHDRAWAL")
    assert p.claims(t) == pytest.approx(
        p.claims(t, "DEATH") + p.claims(t, "LAPSE"), rel=1e-12)

    # the payment is W_t less the fee the insurer keeps, weighted by the in-force at
    # BOM -- a withdrawal is not a decrement
    assert p.wd_pp(t) == 200.0 and p.wd_fee_pp(t) == 25.0
    assert p.claim_pp(t, "WITHDRAWAL") == pytest.approx(175.0, abs=CENT)
    assert p.withdrawals(t) == pytest.approx(175.0 * p.pols_if(t), rel=1e-12)
    assert p.result_cf().loc[t, "withdrawals"] == pytest.approx(
        p.withdrawals(t), rel=1e-12)

    # and the anchor, which never withdraws, carries a column of zeros
    a = indexed_ul.Projection[1]
    assert a.result_cf()["withdrawals"].abs().max() == 0.0


def test_result_tables_are_indexed_by_t(anchor):
    for df in (anchor.result_pols(), anchor.result_av(), anchor.result_seg()):
        assert df.index.name == "t"
        assert list(df.index) == list(range(1, anchor.proj_len() + 1))


def test_the_model_docstring_describes_the_shipped_model_points(indexed_ul):
    """The ``**Model points.**`` paragraph must match ``model_point_table.csv``.

    The docstring is the deliverable, not decoration: a reader who takes point 4 for the
    underfunded withdrawal-and-loan cell, when it is the monthly-premium cell that builds
    the twelve-concurrent-segment ladder, is reading the wrong model point for the notes'
    first pitfall.
    """
    tbl = indexed_ul.Data.model_point_table()
    assert len(tbl) == 5
    doc = indexed_ul.doc
    assert "carries five points" in doc
    assert "four points" not in doc

    # point 4 is the monthly-premium cell, the only one with a full ladder
    p4 = indexed_ul.Projection[4]
    assert p4.premium_mode() == "MONTHLY"
    assert p4.wd_pp(13) == 0.0 and p4.loan_new_pp(241) == 0.0
    assert "Point 4 pays **monthly**" in doc

    # point 5 is the underfunded withdrawal-and-loan cell
    p5 = indexed_ul.Projection[5]
    assert p5.premium_mode() == "ANNUAL" and p5.premium_pp_ann() == 6000.0
    assert p5.wd_pp(13) == 200.0 and p5.loan_new_pp(241) == 6000.0
    assert "Point 5 is underfunded at $6,000 a year" in doc


def _symbol_map(doc):
    """The `Cells` column of the Projection docstring's notes-symbol mapping table."""
    lines = doc.split("\n")
    bars = [i for i, l in enumerate(lines)
            if l.startswith("=========================  ")]
    names = set()
    for line in lines[bars[1] + 1:bars[2]]:
        cell = line[27:59].strip()
        if cell and not cell.startswith("("):
            names.add(cell.split("(")[0])
    return names


def test_the_symbol_map_covers_the_sourcing_split_and_the_point_attributes(indexed_ul):
    """The notes-symbol -> cells-name table has to be complete to be worth having.

    Both of the notes' core recursions carry sourcing-split symbols --
    ``FA_{t+1} = [FA_t + NP_t - MD^FA_t - W^FA_t - B^FA_t - Sweep_t + Roll^FA_t] x ...``
    and ``S_{k,t+1} = S_{k,t} - MD^seg_{k,t} - W^seg_{k,t} - B^seg_{k,t}`` -- and the
    notes' "Model point attributes" table lists six attributes whose siblings were mapped
    while they were not.  Every name in the map must also resolve to something that
    exists, so a rename cannot leave the table pointing at nothing.
    """
    mapped = _symbol_map(indexed_ul.Projection.doc)
    required = {
        # the sourcing split of both core recursions
        "draw_pp", "draw_from_fa_pp", "draw_from_seg_pp",
        "mth_deduction_from_fa_pp", "mth_deduction_from_seg_pp",
        "seg_share", "seg_wd_pp", "seg_wd_cum_pp", "seg_ded_pp", "seg_ded_cum_pp",
        # the notes' "Model point attributes" rows
        "sex", "rate_class", "db_option", "qual_test", "premium_mode",
        "loan_bal_init",
    }
    assert required <= mapped, f"unmapped: {sorted(required - mapped)}"

    known = set(indexed_ul.Projection.cells) | set(indexed_ul.Projection.refs)
    assert mapped <= known, f"maps to nothing: {sorted(mapped - known)}"


def test_undiscounted_no_present_values(indexed_ul):
    """The library projects gross liability cash flows; discounting is a later layer."""
    names = set(indexed_ul.Projection.cells) | set(indexed_ul.Projection.refs)
    assert not any(n.startswith("pv_") for n in names)
    assert "disc_rate_ann" not in names
    assert "disc_factors" not in names


def test_cells_names_follow_the_universal_life_chassis(indexed_ul):
    """The chassis names for every shared concept, so the two models cannot drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "rate_class", "sum_assured",
        "db_option", "qual_test", "premium_type", "premium_pp_ann",
        "load_prem_rate", "av_pp_init", "loan_bal_init", "pols_if_init",
        "duration_mth_init", "duration_mth", "duration", "policy_year", "age",
        "proj_len", "has_surr_charge", "surr_charge_id", "gsp", "glp",
        "seven_pay_prem", "inv_return_mth", "guar_rate_mth", "naar_factor",
        "loan_rate_mth", "prem_persistency", "premium_pp", "prem_to_av_pp",
        "prem_to_av", "premiums", "wd_pp", "wd_fee_pp", "face_reduction_pp",
        "sum_assured_at", "units", "corridor_factor", "db_pp", "net_amt_at_risk",
        "coi_rate_scale", "coi_rate_guar", "coi_rate", "coi_pp", "coi",
        "rider_charge_pp", "maint_fee_pp", "maint_fee", "mth_deduction_pp",
        "mth_deduction", "av_pp_at", "av_pp", "av_at", "av_change",
        "inv_income_pp", "inv_income", "loan_bal_pp", "surr_charge_rate",
        "surr_charge_pp", "csv_pp", "ncsv_pp", "surr_charge", "is_shortfall",
        "cum_prem_pp", "gpt_limit", "gpt_ok", "seven_pay_limit", "is_mec",
        "class_factor", "mort_rate", "mort_rate_mth", "lapse_rate_base",
        "lapse_shock_year", "lapse_rate_sc_mult", "comp_rate_ann",
        "lapse_rate_dyn_mult", "lapse_rate", "lapse_rate_mth", "pols_if",
        "pols_if_at", "pols_death", "pols_lapse", "pols_maturity", "claim_pp",
        "claims_from_av", "claims_over_av", "claims", "withdrawals", "wd_fees",
        "inflation_factor", "expenses", "premium_taxes", "margin_expense",
        "margin_mortality", "net_cf", "check_av_roll_fwd", "check_margin",
        "result_cf", "result_pols", "result_av",
        # References shared with the chassis
        "point_id", "omega_age", "charges_cease_age", "guar_rate_ann",
        "coi_curr_factor", "expense_pol_mth", "expense_unit_mth_1",
        "expense_unit_mth_2", "expense_unit_step_year", "loan_rate_ann",
        "wd_fee", "mort_ae_factor", "lapse_shock_mult", "lapse_dyn_slope",
        "lapse_dyn_cap", "lapse_rate_cap", "expense_acq", "expense_maint",
        "inflation_rate", "premium_tax_rate",
    }
    names = set(indexed_ul.Projection.cells) | set(indexed_ul.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_PATH, name="IUL_US_S_rt_src")
    try:
        dest = tmp_path / "IUL_US_S"
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in MODEL_PATH.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="IUL_US_S_rt")
    try:
        proj = reread.Projection[1]
        proj.result_cf()
        for scenario, row in WORKED_EXAMPLE.items():
            bal0, ded, i_start, i_end = row[0], row[1], row[2], row[3]
            assert proj.index_credit(
                bal0, ded, proj.index_change(i_start, i_end)) == pytest.approx(
                row[7], abs=CENT)
        for t, row in ANCHOR.items():
            assert proj.av_pp(t) == pytest.approx(row[10], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    written = model_files(dest)
    committed = model_files(MODEL_PATH)
    assert written == committed
