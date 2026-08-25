"""Golden and structural tests for WholeLife_JP_A.

The golden values are the worked example in ``products/whole_life/technical-notes.md``
("Worked example"), which projects the anchor cell: male, 契約年齢 30 on a 満年齢 basis,
保険金額 JPY 5,000,000, 保険期間 終身, 保険料払込期間 15 years, the 低解約返戻金型
(*tei-kaiyaku-henreikin-gata*, suppressed-surrender-value) form on at k = 0.70, and an
annual premium of JPY 174,960.  They are hard-coded here rather than pickled so that a
reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the yen-cent, in-force to
six decimals, decrement totals to nine.

This is the library's **savings chassis**, so the module carries more than a cash-flow
comparison.  Every product fact the notes list under **Known modeling pitfalls** earns
its own test, named after the pitfall, because each of them is a way an implementation
can look right and be wrong:

* the 低解約返戻金型 cliff is a **step** and not a ramp, and on a 終身払 contract it never
  happens at all;
* a surrender in policy year m is paid on the **full** value, and both values exist at
  that anniversary;
* there is **one** policy value and **one** multiplier on it, not two reserve runs;
* lapse on this chassis is a **funded event** — the 自動振替貸付 (*jidō furikae
  kashitsuke*, automatic premium loan, APL) carries the contract until the continuation
  test fails;
* an APL advance is **not cash income**;
* the APL test runs on the **suppressed** value, which is worth one advance against
  thirteen on the same underlying policy value;
* the APL clawback **survives the step**, which is worth sixteen years of in force;
* premiums stop at 払込満了 and **nothing else does**;
* the horizon is the mortality table's terminal age, not a round number;
* 高度障害 is inside the death rate and リビング・ニーズ accelerates rather than adds;
* every payment is floored at zero; and
* 責任準備金 is not 解約返戻金.

The optional modules are asserted in **both** positions — off in the base run, and
switched on — because a module that is only ever exercised off is machinery nobody has
run.
"""
import math
import re
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from jp_registry import model_path

MODEL_DIR = model_path("WholeLife_JP_A")

YEN = 0.005           # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.
PROB = 5e-10          # decrement totals displayed to 9 d.p.


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    These docstrings are hard-wrapped prose.  Searching the raw text for a sentence
    fragment finds it or not depending on where the wrap fell, which would make the
    assertions below test the line breaks rather than the content.
    """
    return re.sub(r"\s+", " ", doc)


# ---------------------------------------------------------------------------
# The notes' worked example, hard-coded
#
# "First periods of the base run", per policy issued, income-positive, two decimals.
# t: (q(t), pols_if(t), premiums, claims_death, claims_lapse, claim_expenses, expenses,
#     commissions, net_cf)
#
# ``expenses`` is acquisition plus maintenance only; the claim handling expense stands
# beside it in its own column, which is the settled column vocabulary of the library.
WORKED_EXAMPLE = {
    1:  (0.00068, 1.000000, 174960.00, 3400.00,   3747.52, 13.60, 58000.00, 157464.00,
         -47665.12),
    2:  (0.00069, 0.959347, 167847.39, 3309.75,   6352.17, 13.24,  7751.53,   5035.42,
         145385.28),
    3:  (0.00070, 0.929925, 162699.62, 3254.74,   6502.46, 13.02,  7588.93,   4880.99,
         140459.49),
    4:  (0.00072, 0.910688, 159334.02, 3278.48,   8750.23, 13.11,  7506.26,   4780.02,
         135005.91),
    5:  (0.00074, 0.891832, 156034.91, 3299.78,  10936.27, 13.20,  7424.35,   4681.05,
         129680.27),
    14: (0.00151, 0.736765, 128904.33, 5562.57,  27910.33, 22.25,  6708.05,   3867.13,
         84833.99),
    15: (0.00163, 0.720939, 126135.49, 5875.65, 358347.00, 23.50,  6629.61,   3784.06,
         -248524.33),
    16: (0.00177, 0.597404,      0.00, 5287.03,  35399.47, 21.15,  5548.54,      0.00,
         -46256.18),
}

# "Surrender values at the same anniversaries", the notes' own list.
WORKED_EXAMPLE_CV = {
    1: 93751.86, 2: 220864.08, 3: 349867.80, 4: 480764.69, 5: 613589.14,
    14: 1896979.14, 15: 2928631.87, 16: 2968027.59,
}

# "Calibration of the cash-value construction".
A30 = 0.47678817                 # A(30) on i_cv and the shipped table
ANNUITY_DUE_30_15 = 13.49765934  # a-double-dot(30, 15)
PI = 176618.83                   # pi = SA x A(30) / a(30, 15)
ALPHA = 0.0090                   # the acquisition-deduction rate
LOW_CV_PREMIUM_RATIO = 0.837     # the suppressed form's price, 17,040 / 20,350 [S7]
SC0 = 45000.00                   # alpha x SA, the initial 解約控除

# The eight-point fit against the published surrender-value run [S4]: the model's own
# CV, with the pre-step value at t = 15 carried separately.  The published figures the
# notes compare against are sourced and are not reproduced here.
SURRENDER_FIT = {
    5: 613589.14, 10: 1306475.85, 15: 2928631.87, 20: 3128399.27,
    30: 3547057.08, 40: 3977949.06, 50: 4386411.27,
}
CV15_PRE_STEP = 2050042.31       # k V(15), the value an instant before the step

# "Roll-forward check": undiscounted totals per policy issued over the full 80 years.
TOTALS = {
    "premiums": 2212542.21,
    "claims_death": 1525331.95,
    "claims_lapse": 1692538.36,
    "claim_expenses": 6101.33,
    "expenses": 329814.38,    # acquisition and maintenance only, per R1
    "commissions": 218591.47,
    "dividends": 0.00,
    "net_cf": -1559835.29,
}
CLAIM_EXPENSES_TOTAL = 6101.33   # also a published result_cf column, see TOTALS
SUM_DEATHS = 0.305066391
SUM_SURRENDERS = 0.694933609
DEATHS_AFTER_YEAR_40 = 0.230566   # of 0.305066 — the horizon sensitivity

# "自動振替貸付 trace (module on)", on the anchor cell's policy value.
APL_PREMIUM_WITH_INTEREST = 179771.40    # P (1 + i_L)
APL_BENEFIT_ON_FAILURE = 41092.68        # max(0, CV(2) - L(3)) on the suppressed form
APL_L15_ORDINARY = 2764330.63            # L(15) on the ordinary form, k = 1.00
APL_FAIL_YEAR_CLAWBACK_ON = 53           # the cohort defaulting at s = 10
APL_FAIL_YEAR_CLAWBACK_OFF = 69


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(jp_wl_anchor, t):
    """Every cell of the notes' eight-row cash flow table, to the displayed precision."""
    q, pols, prem, death, lapse, claim_exp, exp, comm, net = WORKED_EXAMPLE[t]
    a = jp_wl_anchor
    assert a.mort_rate(t) == pytest.approx(q, rel=1e-12)
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=YEN)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=YEN)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=YEN)
    assert a.claim_expenses(t) == pytest.approx(claim_exp, abs=YEN)
    assert a.expenses(t) == pytest.approx(exp, abs=YEN)
    assert a.commissions(t) == pytest.approx(comm, abs=YEN)
    assert a.dividends(t) == 0.0
    assert a.net_cf(t) == pytest.approx(net, abs=YEN)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CV))
def test_worked_example_surrender_value(jp_wl_anchor, t):
    """The notes' list of 解約返戻金 at the same anniversaries, to the yen-cent.

    These carry the whole surrender-benefit stream, the largest outgo line after death
    claims, so they are asserted separately from the cash flow row that consumes them.
    """
    assert jp_wl_anchor.cv_pp(t) == pytest.approx(WORKED_EXAMPLE_CV[t], abs=YEN)


def test_worked_example_calibration(jp_wl_anchor):
    """A(30), a-double-dot(30, 15) and pi, the two-parameter cash-value construction.

    ``i_cv`` and ``alpha`` are the only free parameters in the surrender value; the notes
    derive them rather than asserting them, and these are the derived values.
    """
    a = jp_wl_anchor
    assert a.epv_death(30) == pytest.approx(A30, abs=5e-9)
    assert a.annuity_due(30, 15) == pytest.approx(ANNUITY_DUE_30_15, abs=5e-9)
    assert a.prem_net_level_pp() == pytest.approx(PI, abs=YEN)
    assert a.prem_net_level_pp() == pytest.approx(
        a.sum_assured() * A30 / ANNUITY_DUE_30_15, rel=1e-8)
    assert a.surr_charge_pp(0) == pytest.approx(SC0, abs=YEN)
    assert a.surr_charge_pp(0) == pytest.approx(ALPHA * a.sum_assured(), rel=1e-12)
    assert a.surr_charge_pp(15) == pytest.approx(0.0, abs=1e-9)


def test_pi_is_not_the_priced_net_premium(jp_wl_anchor):
    """pi exceeds the gross premium, which the notes name rather than smooth over.

    The construction stands the valuation table's margin-loaded q in for the insurer's
    unpublished 予定死亡率 and lets the 解約控除 absorb the difference.  It reproduces the
    contractual **value**; it is not a pricing model, and a reader who takes pi for a
    priced premium reads a negative expense loading out of it.
    """
    a = jp_wl_anchor
    assert a.prem_net_level_pp() > a.premium_pp()
    assert a.premium_pp() == 174960.0        # 12 x the published monthly premium
    assert 15 * a.premium_pp() == 2624400.0  # the published 払込保険料累計


@pytest.mark.parametrize("d", sorted(SURRENDER_FIT))
def test_surrender_value_fit_table(jp_wl_anchor, d):
    """The notes' eight-point fit against the published 解約払戻金 run, model side."""
    assert jp_wl_anchor.cv_pp(d) == pytest.approx(SURRENDER_FIT[d], abs=YEN)


def test_the_surrender_value_crosses_cumulative_premiums_after_the_step(jp_wl_anchor):
    """70.1% of premiums paid at duration 5, 111.6% an instant after the step.

    The 払戻率 crossing is what the product is sold on, and it is a consequence of the
    step rather than of the value's own growth: the ratio moves from 0.774 to 1.116 in
    one year while the underlying policy value moves by a tenth of that.
    """
    a = jp_wl_anchor
    assert a.cv_pp(5) / a.cum_prem_pp(5) == pytest.approx(0.7014, abs=5e-4)
    assert a.cv_pp(14) / a.cum_prem_pp(14) < 1.0
    assert a.cv_pp(15) / a.cum_prem_pp(15) == pytest.approx(1.1159, abs=5e-4)


def test_worked_example_year_one_trace(jp_wl_anchor):
    """The notes' year-one trace, line by line.

    D(1) = 0.00068; death claims = 5,000,000 D(1); claim expense = 20,000 D(1);
    S(1) = (1 - q) x 4%; V(1) = W(1) - SC(1); CV(1) = 0.70 V(1); expenses = E0 + e(1),
    with the claim expense ec D(1) beside it rather than inside it; commission = 0.90 P.
    """
    a = jp_wl_anchor
    assert a.pols_death(1) == pytest.approx(0.00068, rel=1e-12)
    assert a.claims(1, "DEATH") == pytest.approx(5000000.0 * 0.00068, abs=YEN)
    assert a.claim_expenses(1) == pytest.approx(13.60, abs=YEN)
    assert a.lapse_rate(1) == 0.04
    assert a.pols_lapse(1) == pytest.approx((1 - 0.00068) * 0.04, rel=1e-12)
    assert a.prosp_val_pp(1) == pytest.approx(175931.231, abs=0.0005)
    assert a.surr_charge_pp(1) == pytest.approx(42000.0, abs=YEN)
    assert a.pol_val_pp(1) == pytest.approx(133931.231, abs=0.0005)
    assert a.cv_pp(1) == pytest.approx(0.70 * a.pol_val_pp(1), rel=1e-14)
    assert a.expenses(1) == pytest.approx(50000.0 + 8000.0, abs=YEN)
    assert a.commissions(1) == pytest.approx(0.90 * 174960.0, abs=YEN)
    assert a.net_cf(1) == pytest.approx(
        174960.00 - 3400.00 - 13.60 - 3747.52 - 50000.00 - 8000.00 - 157464.00,
        abs=YEN)
    assert a.pols_if(2) == pytest.approx(1.0 * (1 - 0.00068) * 0.96, rel=1e-14)


def test_worked_example_year_two_and_three_traces(jp_wl_anchor):
    """The notes' second- and third-year traces, expense inflation factor included."""
    a = jp_wl_anchor
    assert a.pol_val_pp(2) == pytest.approx(315520.1189, abs=0.0005)
    assert a.cv_pp(2) == pytest.approx(0.70 * 315520.1189, abs=YEN)
    assert a.inflation_factor(2) == pytest.approx(1.01, rel=1e-14)
    assert a.expenses(2) == pytest.approx(8000.0 * 1.01 * a.pols_if(2), abs=YEN)
    assert a.commissions(2) == pytest.approx(0.03 * 174960.0 * a.pols_if(2), abs=YEN)
    assert a.pols_if(3) == pytest.approx(
        a.pols_if(2) * (1 - 0.00069) * 0.97, rel=1e-14)

    assert a.pol_val_pp(3) == pytest.approx(499811.1402, abs=0.0005)
    assert a.cv_pp(3) == pytest.approx(0.70 * 499811.1402, abs=YEN)
    assert a.inflation_factor(3) == pytest.approx(1.01 ** 2, rel=1e-14)
    assert a.pols_if(4) == pytest.approx(
        a.pols_if(3) * (1 - 0.00070) * 0.98, rel=1e-14)


def test_worked_example_cliff_trace(jp_wl_anchor):
    """The notes' trace at t = 15, the largest single feature of the stream.

    l(15) = 0.720939, survivors of mortality 0.719763905, S(15) = 0.122359864 on a 17%
    surrender rate, and the benefit paid on the **post-step** value.
    """
    a = jp_wl_anchor
    assert a.pols_if(15) == pytest.approx(0.720939, abs=INFORCE)
    assert a.lapse_rate(15) == pytest.approx(0.17, rel=1e-12)
    assert a.pols_if_at(15, "BEF_LAPSE") == pytest.approx(0.719763905, abs=5e-9)
    assert a.pols_lapse(15) == pytest.approx(0.122359864, abs=5e-9)
    assert a.cv_pp(15) == pytest.approx(2928631.87, abs=YEN)
    assert a.cv_pp_susp(15) == pytest.approx(CV15_PRE_STEP, abs=YEN)
    assert a.claims(15, "LAPSE") == pytest.approx(358347.00, abs=YEN)
    assert a.claims(15, "LAPSE") == pytest.approx(
        a.cv_pp(15) * a.pols_lapse(15), rel=1e-12)
    # One year either side: +84,833.99 before, -248,524.33 at the cliff.
    assert a.net_cf(14) == pytest.approx(84833.99, abs=YEN)
    assert a.net_cf(15) == pytest.approx(-248524.33, abs=YEN)
    assert a.net_cf(14) - a.net_cf(15) > 300000.0


def test_worked_example_undiscounted_totals(jp_wl_anchor):
    """The notes' undiscounted totals over the full 80 years, column by column."""
    df = jp_wl_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=YEN)
    a = jp_wl_anchor
    assert sum(a.claim_expenses(t) for t in range(1, a.proj_len() + 1)) == (
        pytest.approx(CLAIM_EXPENSES_TOTAL, abs=YEN))
    # Undiscounted, the contract loses money; discounting is out of scope.
    assert df["net_cf"].sum() < 0.0


def test_worked_example_decrement_split(jp_wl_anchor):
    """Sum D = 0.305066391 and Sum S = 0.694933609, summing to exactly 1.

    Because the table terminates, every policy issued leaves by a modelled decrement:
    there is no residual population and no tail state anywhere in this model.
    """
    a = jp_wl_anchor
    ts = range(1, a.proj_len() + 1)
    deaths = sum(a.pols_death(t) for t in ts)
    surrenders = sum(a.pols_lapse(t) for t in ts)
    assert deaths == pytest.approx(SUM_DEATHS, abs=PROB)
    assert surrenders == pytest.approx(SUM_SURRENDERS, abs=PROB)
    assert deaths + surrenders == pytest.approx(1.0, abs=PROB)
    assert a.pols_if(a.proj_len() + 1) == 0.0


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_the_cliff_is_a_step_not_a_ramp(jp_wl_anchor):
    """CV(m) / (k V(m)) is exactly 1 / k; anything between is an interpolation.

    The multiplier takes two values and only two — k before the step and 1 from it — so
    a model that grades, interpolates or smooths across the boundary fails here.  This is
    the notes' first-listed pitfall and the product's signature mechanic.
    """
    a = jp_wl_anchor
    m = a.prem_period()
    assert m == 15
    assert a.cv_pp(m) / a.cv_pp_susp(m) == pytest.approx(1.0 / 0.70, rel=1e-14)
    assert a.cv_pp(m) / a.cv_pp_susp(m) == pytest.approx(1.4285714286, abs=5e-10)
    assert {a.cv_mult(t) for t in range(1, a.proj_len() + 1)} == {0.70, 1.0}
    assert a.cv_mult(m - 1) == 0.70 and a.cv_mult(m) == 1.0
    # The step is discontinuous in a way the underlying value is not: CV jumps by half
    # in the year the policy value moves by under a tenth.
    assert a.cv_pp(m) / a.cv_pp(m - 1) > 1.5
    assert a.pol_val_pp(m) / a.pol_val_pp(m - 1) < 1.10
    assert a.cv_pp(m + 1) / a.cv_pp(m) < 1.05


def test_pitfall_the_cliff_never_happens_on_a_whole_of_life_premium_point(whole_life):
    """On 終身払 (prem_term = 0) the suppressed period runs for life and m is infinite.

    Model point 3 is that configuration, and it is in the table because it is the one in
    which the product's signature mechanic is absent by construction.  A model that steps
    the value up at some inferred anniversary — or that spikes the lapse rate there —
    invents a 払込満了 the contract does not have.
    """
    p = whole_life.Projection[3]
    assert p.prem_term() == 0
    assert p.prem_period() == p.proj_len()
    assert all(p.cv_mult(t) == 0.70 for t in range(1, p.proj_len() + 1))
    assert all(p.cv_pp(t) == pytest.approx(0.70 * p.pol_val_pp(t), rel=1e-14)
               for t in (1, 15, 40, 79))
    # No spike anywhere, even though lapse_spike is set on the model point.
    assert p.lapse_spike() == 0.15
    assert all(p.lapse_rate(t) == p.lapse_rate_base(t)
               for t in range(1, p.proj_len() + 1))
    # The 解約控除 has no end date to grade to, so it is held flat for life.
    assert all(p.surr_charge_pp(t) == pytest.approx(0.0090 * p.sum_assured(), rel=1e-14)
               for t in (1, 40, 79))


def test_pitfall_off_by_one_at_the_boundary(jp_wl_anchor):
    """A surrender in policy year m is paid on the **full** value, not the suppressed one.

    Both quantities exist at t = m and the published table prints both; the model must
    produce both and lose neither.  Paying year-m surrenders on the suppressed basis
    costs roughly a quarter of a million yen per policy issued in that one year.
    """
    a = jp_wl_anchor
    m = a.prem_period()
    assert a.claims(m, "LAPSE") == pytest.approx(a.cv_pp(m) * a.pols_lapse(m), rel=1e-12)
    suppressed = a.cv_pp_susp(m) * a.pols_lapse(m)
    assert a.claims(m, "LAPSE") - suppressed > 100000.0
    # The year before is on the suppressed value, and both cells publish their own.
    assert a.claims(m - 1, "LAPSE") == pytest.approx(
        a.cv_pp_susp(m - 1) * a.pols_lapse(m - 1), rel=1e-12)
    assert a.cv_pp(m - 1) == pytest.approx(a.cv_pp_susp(m - 1), rel=1e-14)
    assert a.cv_pp(m) != pytest.approx(a.cv_pp_susp(m), rel=1e-6)


def test_pitfall_one_policy_value_one_multiplier(whole_life):
    """The suppression is a haircut on a common value, not a second reserve basis.

    Model points 1 and 6 are the same policy — same issue age, same sum assured, same
    premium, same payment term — with the suppression on and off.  Their policy values
    are identical at every duration and their surrender values differ by exactly k while
    the suppression bites and not at all after it.  At duration 40 the two products have
    identical surrender values, which is the sourced fact that settles what the
    suppression *is*.
    """
    low, ordinary = whole_life.Projection[1], whole_life.Projection[6]
    assert low.low_cv() is True and ordinary.low_cv() is False
    assert low.premium_pp() == ordinary.premium_pp()
    for t in range(0, low.proj_len() + 1):
        assert low.pol_val_pp(t) == pytest.approx(ordinary.pol_val_pp(t), abs=1e-9)
    for t in (1, 5, 14):
        assert low.cv_pp(t) == pytest.approx(0.70 * ordinary.cv_pp(t), rel=1e-14)
    for t in (15, 20, 40):
        assert low.cv_pp(t) == pytest.approx(ordinary.cv_pp(t), rel=1e-14)
    # One series, one multiplier: there is no second policy value cells anywhere.
    names = set(whole_life.Projection.cells)
    assert "pol_val_low_pp" not in names and "reserve_low_pp" not in names


def test_pitfall_lapse_is_a_funded_event(whole_life):
    """A premium default moves a policy into the APL state; it does not lapse it.

    Applying a lapse rate to unpaid premiums without first running the continuation test
    models a decrement the contract does not have.  On model point 5 the defaulting
    policies are still in force — they appear in pols_if and in the death exposure — and
    they leave only when the test fails, through pols_apl_exit rather than pols_lapse.
    """
    p = whole_life.Projection[5]
    assert p.default_rate(3) == 0.01
    assert p.pols_default(3) == pytest.approx(p.pols_if_pay(3) * 0.01, rel=1e-12)
    # Defaulters are carried, not removed: in force exceeds the paying cohort.
    assert p.pols_apl_carried(5) > 0.0
    assert p.pols_if(5) == pytest.approx(
        p.pols_if_pay(5) + p.pols_apl_carried(5), rel=1e-14)
    assert p.pols_if(5) > p.pols_if_pay(5)
    # The exit is its own decrement, and the roll-forward needs it to close.
    assert any(p.pols_apl_exit(t) > 0.0 for t in range(1, p.proj_len() + 1))
    assert p.check_pols_roll_fwd() is True
    # No premium is due after prem_end, so no policy can default into the APL there.
    assert p.default_rate(p.prem_end() + 1) == 0.0
    # A default in policy year 1 terminates at once: the value cannot carry a premium.
    assert p.apl_fires(1, 1) is False
    assert p.cv_pp(1) < APL_PREMIUM_WITH_INTEREST


def test_pitfall_the_apl_advance_is_not_cash_income(whole_life):
    """No cash reaches the insurer, so an APL year produces no premium and no commission.

    Booking the advanced premium as income while also netting the loan off the later
    claim counts it twice.  Premium income is carried on the paying cohort alone, and
    renewal commission follows the premium actually collected.
    """
    p = whole_life.Projection[5]
    for t in (3, 5, 10):
        assert p.pols_apl_carried(t) > 0.0
        assert p.premiums(t) == pytest.approx(
            p.premium_pp() * p.pols_pay_bef_decr(t), rel=1e-14)
        # Strictly less than a run that had booked the advance as income.
        assert p.premiums(t) < p.premium_pp() * p.pols_if(t)
        assert p.commissions(t) == pytest.approx(0.03 * p.premiums(t), rel=1e-14)
    # The advance shows up only as growth in the loan balance.
    assert p.loan_apl_pp(3, 2) == pytest.approx(APL_PREMIUM_WITH_INTEREST, abs=YEN)
    assert p.loan_apl_pp(2, 2) == 0.0


def test_pitfall_the_apl_test_runs_on_the_suppressed_value(whole_life):
    """One advance at k = 0.70 against thirteen at k = 1.00, from the same default.

    The continuation test is run against CV*(t), the suppressed value, not against V.
    Model points 5 and 6 are the same policy with the suppression on and off, and the
    difference is more than a decade of in force.
    """
    low, ordinary = whole_life.Projection[5], whole_life.Projection[6]
    assert low.premium_pp() == ordinary.premium_pp()
    assert low.premium_pp() * (1 + 0.0275) == pytest.approx(
        APL_PREMIUM_WITH_INTEREST, abs=YEN)

    assert low.apl_advances(2) == 1
    assert low.apl_fail_year(2) == 3
    assert ordinary.apl_advances(2) == 13
    assert ordinary.apl_fail_year(2) == 15

    # The test itself, at the year each form fails.
    assert low.apl_test_val(3) == pytest.approx(0.70 * low.pol_val_pp(3), rel=1e-14)
    assert low.apl_test_val(3) < low.loan_apl_pp(3, 2) + APL_PREMIUM_WITH_INTEREST
    assert ordinary.loan_apl_pp(15, 2) == pytest.approx(APL_L15_ORDINARY, abs=YEN)
    assert (ordinary.loan_apl_pp(15, 2) + APL_PREMIUM_WITH_INTEREST
            > ordinary.cv_pp(15) > ordinary.loan_apl_pp(15, 2))

    # The benefit on failure is the previous anniversary's value net of the balance.
    assert max(0.0, low.apl_test_val(2) - low.loan_apl_pp(3, 2)) == pytest.approx(
        APL_BENEFIT_ON_FAILURE, abs=YEN)


def test_pitfall_the_clawback_survives_the_step():
    """A cohort carried by unrepaid advances keeps the suppressed basis after m.

    It has by definition not paid the low-period premiums, which is the contractual
    trigger for the clawback.  Switching it off moves the exhaustion of the cohort
    defaulting at s = 10 from year 53 to year 69 — sixteen years of in force, on one
    boolean.
    """
    model = mx.read_model(MODEL_DIR, name="WholeLife_JP_A_clawback")
    try:
        assert model.Projection.apl_clawback is True
        p = model.Projection[5]
        assert p.apl_fail_year(10) == APL_FAIL_YEAR_CLAWBACK_ON
        # With the clawback on the test value never steps up, even past m.
        assert p.apl_test_val(20) == pytest.approx(0.70 * p.pol_val_pp(20), rel=1e-14)
        assert p.apl_test_val(20) < p.cv_pp(20)

        model.Projection.apl_clawback = False
        model.Projection.clear_all()
        p = model.Projection[5]
        assert p.apl_fail_year(10) == APL_FAIL_YEAR_CLAWBACK_OFF
        assert p.apl_test_val(20) == pytest.approx(p.cv_pp(20), rel=1e-14)
        # Before m the two treatments agree, so the s = 2 cohort is unaffected.
        assert p.apl_advances(2) == 1
    finally:
        model.close()


def test_pitfall_premiums_stop_at_m_and_nothing_else_does(jp_wl_anchor):
    """Premium and renewal commission end at 払込満了; every other line runs for life.

    A projection truncated at the end of the premium term misses the majority of the
    liability — more than three quarters of the expected death claims fall after year 40
    on this cell — and one that keeps charging renewal commission past it charges
    commission on a premium nobody pays.
    """
    a = jp_wl_anchor
    m = a.prem_end()
    assert m == 15
    assert a.premiums(m) > 0.0 and a.commissions(m) > 0.0
    for t in (m + 1, 30, 60, a.proj_len()):
        assert a.premiums(t) == 0.0
        assert a.commissions(t) == 0.0
        assert a.expenses(t) > 0.0
        assert a.claims(t, "DEATH") > 0.0
    assert a.claims(m + 1, "LAPSE") > 0.0
    # The cash value keeps growing after the premiums stop.
    assert a.cv_pp(a.proj_len() - 1) > a.cv_pp(m)
    late = sum(a.pols_death(t) for t in range(41, a.proj_len() + 1))
    assert late == pytest.approx(DEATHS_AFTER_YEAR_40, abs=5e-7)
    assert late / SUM_DEATHS > 0.75


def test_pitfall_terminal_age_and_table_basis(whole_life):
    """omega = 109 (M) / 113 (F), and the horizon is the table's, not a round number.

    Projecting a whole life contract to 100 truncates the liability and projecting to
    120 invents one.  The terminal rate is 1 whatever mort_be_factor is set to, because
    omega_age is a structural property of the projection rather than an assumption.  The
    table is built for 保険年齢 while this product ages on 満年齢, and the notes require
    both to be stated wherever the basis is described.
    """
    male, female = whole_life.Projection[1], whole_life.Projection[4]
    assert male.sex() == "M" and male.omega_age() == 109
    assert female.sex() == "F" and female.omega_age() == 113
    assert male.proj_len() == 109 - 30 + 1 == 80
    assert female.proj_len() == 113 - 45 + 1 == 69
    assert male.age(male.proj_len()) == 109
    assert male.mort_rate(male.proj_len()) == 1.0
    assert male.pols_if(male.proj_len()) > 0.0
    assert male.pols_if(male.proj_len() + 1) == 0.0
    assert len(male.result_cf()) == 80

    # The two age bases are named where the basis is described, and the table is read at
    # the 満年齢 attained age with no mapping applied — an understatement the model owns.
    basis = flat(whole_life.Projection.cells["age_at_entry"].doc)
    assert "満年齢" in basis and "保険年齢" in basis
    assert male.age(1) == male.age_at_entry() == 30
    assert male.mort_rate_base(1) == male.mort_rate_at_age(30)

    # mort_be_factor scales the rate but never the terminal one.
    adjusted = whole_life.Projection[9]
    assert adjusted.mort_be_factor() == 0.85
    assert adjusted.mort_rate(1) == pytest.approx(
        0.85 * adjusted.mort_rate_at_age(60), rel=1e-12)
    assert adjusted.mort_rate(adjusted.proj_len()) == 1.0


def test_pitfall_kodo_shogai_is_inside_the_death_rate(whole_life):
    """One decrement on one amount: there is no separate disability rate in the model.

    生保標準生命表2018（死亡保険用）already carries 高度障害 inside the death rate, so a
    separate disability decrement double-counts claims.
    """
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for stem in ("disab", "ti_", "_ti_", "ci_", "shogai", "kodo"):
        assert not [n for n in names if stem in n], f"{stem}: a second decrement"
    doc = flat(whole_life.Projection.cells["mort_rate_at_age"].doc)
    assert "高度障害" in doc and "separate disability decrement" in doc
    a = whole_life.Projection[1]
    assert a.pols_death(5) == pytest.approx(
        (a.pols_pay_bef_decr(5) + a.pols_apl(5)) * a.mort_rate(5), rel=1e-14)


def test_pitfall_living_needs_accelerates_rather_than_adds(whole_life):
    """The rider reduces the sum assured by what it pays, so it is never an addition.

    Zero incidence in the base run, and the model has no cells that could add one: the
    only benefit amount is the sum assured in force, and the only benefit kinds are the
    death benefit and the surrender value.
    """
    a = whole_life.Projection[1]
    assert a.claims(10) == pytest.approx(
        a.claims(10, "DEATH") + a.claims(10, "LAPSE"), rel=1e-12)
    with pytest.raises(FormulaError):
        a.claims(10, "LIVING_NEEDS")
    assert all(a.sum_assured_at(t) == a.sum_assured() for t in (1, 15, 40, 80))
    assert "リビング・ニーズ" in flat(
        whole_life.Projection.cells["pols_death"].doc)


def test_pitfall_everything_is_floored_at_zero(whole_life):
    """No amount in this model may produce a negative payment.

    W - SC is negative in principle at t = 0, and both SA - L and CV - L go negative once
    a loan has outgrown the value.  Model point 7 draws the contractual maximum late and
    reaches the loan-excess termination with the benefit floored at exactly zero.
    """
    a = whole_life.Projection[1]
    assert a.prosp_val_pp(0) - a.surr_charge_pp(0) < 0.0
    assert a.pol_val_pp(0) == 0.0

    p = whole_life.Projection[7]
    fail = p.loan_fail_year()
    assert fail == 53
    assert p.loan_pp(fail) > p.cv_pp(fail - 1)          # the loan has outgrown the value
    assert p.claims(fail, "LAPSE") == 0.0               # and the benefit is exactly zero
    assert p.pols_loan_exit(fail) > 0.0
    for t in range(1, p.proj_len() + 1):
        assert p.claims(t, "DEATH") >= 0.0
        assert p.claims(t, "LAPSE") >= 0.0
        assert p.cv_pp(t) >= 0.0


def test_pitfall_reserve_pp_is_not_cv_pp(whole_life):
    """reserve_pp - pol_val_pp = SC(t), and only because i_std defaults to i_cv.

    平準純保険料式 admits no Zillmer adjustment, so the statutory reserve carries no
    解約控除 — the whole difference between the two quantities is that deduction.  The
    identity is a consequence of the two basis rates coinciding and is not asserted
    otherwise; reserve_pp >= pol_val_pp >= cv_pp is **not** an invariant, and reserve_pp
    never appears in the cash flow statement.
    """
    a = whole_life.Projection[1]
    assert a.check_reserve_identity() is True
    for t in (1, 5, 10, 15, 40):
        assert a.reserve_pp(t) - a.pol_val_pp(t) == pytest.approx(
            a.surr_charge_pp(t), abs=1e-6)
    assert a.reserve_pp(5) > a.cv_pp(5)                    # suppressed, so far below
    assert "reserve_pp" not in a.result_cf().columns

    # Move i_std away from i_cv and the identity is withdrawn rather than forced.
    model = mx.read_model(MODEL_DIR, name="WholeLife_JP_A_istd")
    try:
        model.Projection.i_std = 0.0025
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.check_reserve_identity_resid(10) == 0.0   # not asserted at all
        assert p.reserve_pp(10) - p.pol_val_pp(10) > 10 * p.surr_charge_pp(10)
        assert p.result_cf()["net_cf"].sum() == pytest.approx(
            TOTALS["net_cf"], abs=YEN)                     # no cash flow moved
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Roll-forward identities, on every shipped model point


def test_six_check_cells_are_published_each_with_its_residual(whole_life):
    """Six roll-forward identities, each with the signed residual beside it.

    ``check_*`` takes no argument and returns one bool over all t, which is the
    library-wide form; the signed residual of the year that failed lives at
    ``check_*_resid(t)``.

    That they are *true*, on all ten points, is asserted in
    ``test_model_conventions_jp.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library. Running them again here,
    on a second instance of the same model, meant a second cold projection of the whole
    table to reach a verdict already reached.

    Generic discovery cannot notice a check that has *gone*: it simply stops being
    discovered. Counting them is the statement left here.
    """
    cells = set(whole_life.Projection.cells)
    checks = [c for c in cells
              if c.startswith("check_") and not c.endswith("_resid")]
    assert len(checks) == 6
    for name in checks:
        assert name + "_resid" in cells, name


def test_inforce_rollforward_closes_on_every_model_point(whole_life):
    """l(t) - l(t+1) = deaths + surrenders + APL exhaustions + loan-excess exits.

    The last two terms are zero in the base run and are what makes the identity close
    with the modules on: a policy leaving because its loan outgrew its value has left for
    a reason that is neither a death nor a surrender.
    """
    for point_id in whole_life.Data.model_point_table().index:
        p = whole_life.Projection[point_id]
        for t in range(1, p.proj_len() + 1):
            out = (p.pols_death(t) + p.pols_lapse(t)
                   + p.pols_apl_exit(t) + p.pols_loan_exit(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12)


def test_decrements_sum_to_one_on_every_model_point(whole_life):
    """Every policy issued leaves by a modelled decrement, and l(T+1) is zero.

    This is the structural statement that there are no tail states: the projection ends
    because the mortality table does, not because a contract term ran out.
    """
    for point_id in whole_life.Data.model_point_table().index:
        p = whole_life.Projection[point_id]
        ts = range(1, p.proj_len() + 1)
        total = sum(p.pols_death(t) + p.pols_lapse(t)
                    + p.pols_apl_exit(t) + p.pols_loan_exit(t) for t in ts)
        assert total == pytest.approx(1.0, abs=1e-9)
        assert p.pols_if(p.proj_len() + 1) == 0.0
        assert p.check_decrement_sum_resid(p.proj_len()) == pytest.approx(0.0, abs=1e-10)


def test_death_is_decremented_before_lapse(jp_wl_anchor):
    """The notes' processing order: surrenders come from the survivors of mortality."""
    a = jp_wl_anchor
    for t in (1, 5, 15, 40):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate(t), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(a.pols_if(t + 1), abs=1e-14)


def test_the_policy_value_rolls_forward_on_its_own_basis(jp_wl_anchor):
    """(W(t-1) + pi)(1 + i_cv) = q SA + (1 - q) W(t), the retrospective form.

    The prospective closed form and the retrospective recursion are the same object seen
    from two ends, so this catches a mis-set premium period or a discount factor applied
    on the wrong side — neither of which the prospective formula alone would reveal.
    """
    a = jp_wl_anchor
    assert a.check_pol_val_roll_fwd() is True
    for t in (1, 5, 15, 16, 40):
        assert a.check_pol_val_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-5)
    # No premium term in the recursion once premiums have stopped.
    q = a.mort_rate_at_age(a.age(20))
    assert (a.prosp_val_pp(19) * 1.01468) == pytest.approx(
        q * a.sum_assured() + (1 - q) * a.prosp_val_pp(20), abs=1e-5)


def test_loan_balances_accumulate_at_the_loan_rate(whole_life):
    """L(t+1) = (L(t) + advance)(1 + i_L), for the 契約者貸付 and every APL cohort.

    Identically zero in the base run, where there is no loan at all; non-trivial the
    moment either module is switched on, which is the point of asserting it there too.
    """
    base = whole_life.Projection[1]
    assert base.check_loan_roll_fwd() is True
    assert all(base.loan_pp(t) == 0.0 for t in range(1, base.proj_len() + 2))

    apl = whole_life.Projection[5]
    assert apl.check_loan_roll_fwd() is True
    for t in range(3, 15):
        adv = apl.premium_pp() if apl.apl_fires(t, 2) else 0.0
        assert apl.loan_apl_pp(t + 1, 2) == pytest.approx(
            (apl.loan_apl_pp(t, 2) + adv) * 1.0275, abs=1e-6)

    loan = whole_life.Projection[7]
    assert loan.check_loan_roll_fwd() is True
    assert loan.loan_pp(41) == pytest.approx(
        loan.pol_loan_draw(40) * 1.0275, abs=1e-6)


def test_the_published_cash_flow_statement_closes(whole_life):
    """net_cf equals the published columns of the same row, on every model point.

    A third benefit kind added to ``claims`` and left out of the statement would vanish
    silently without this; it shows up here instead.
    """
    for point_id in whole_life.Data.model_point_table().index:
        p = whole_life.Projection[point_id]
        assert p.check_net_cf() is True
        df = p.result_cf()
        outgo = df[["claims_death", "claims_lapse", "claim_expenses", "expenses",
                    "commissions", "dividends"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-8)


# ---------------------------------------------------------------------------
# Modules that are off in the base run, asserted in both positions


def test_premium_default_and_the_apl_are_off_in_the_base_run(jp_wl_anchor):
    """default_rate is zero on the base points, so no policy ever enters the APL state."""
    a = jp_wl_anchor
    assert a.apl_elected() is True          # elected, but never triggered
    assert all(a.default_rate(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.pols_default(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.pols_apl(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.pols_apl_exit(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.pols_if(t) == a.pols_if_pay(t) for t in range(1, a.proj_len() + 1))


def test_premium_default_and_the_apl_run_when_switched_on(whole_life):
    """Model points 5 and 6 run the module on the suppressed and the ordinary form.

    Both keep the policy in force through the default, and both terminate it through the
    continuation test rather than through the lapse decrement.
    """
    for point_id in (5, 6):
        p = whole_life.Projection[point_id]
        assert p.default_rate(2) == 0.01
        assert any(p.pols_apl(t) > 0.0 for t in range(1, p.proj_len() + 1))
        assert any(p.pols_apl_exit(t) > 0.0 for t in range(1, p.proj_len() + 1))
        assert p.check_pols_roll_fwd() is True
        assert p.check_loan_roll_fwd() is True


def test_the_policy_loan_is_off_in_the_base_run_and_terminates_when_switched_on(
        whole_life):
    """pol_loan_util is zero in the base run; point 7 draws the contractual maximum.

    The 9/10-while-paying and 8/10-once-paid-up caps are contractual and bind whatever
    the utilisation is set to.  A draw of the maximum at the fortieth anniversary
    compounds at i_L against a value growing at i_cv and reaches the loan-excess
    termination in year 53 with a zero benefit.
    """
    a = whole_life.Projection[1]
    assert a.pol_loan_util() == 0.0
    assert all(a.pol_loan_draw(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert a.loan_fail_year() == a.proj_len() + 1     # never reached with no loan

    p = whole_life.Projection[7]
    assert p.pol_loan_util() == 0.9
    assert p.pol_loan_year() == 40
    assert p.loan_cap_rate(10) == 0.9 and p.loan_cap_rate(40) == 0.8
    assert p.pol_loan_draw(40) == pytest.approx(0.8 * p.cv_pp(39), rel=1e-14)
    assert all(p.pol_loan_draw(t) == 0.0
               for t in range(1, p.proj_len() + 1) if t != 40)
    assert p.loan_fail_year() == 53
    assert p.pols_if(54) == 0.0
    assert p.result_cf().loc[54:].abs().sum().sum() == 0.0


def test_dynamic_surrender_is_off_in_the_base_run_and_produces_the_spike_when_on(
        whole_life):
    """The 払戻率 ratio crosses 1 exactly at the cliff, so the module reproduces the surge.

    Model point 8 turns the module on **and** sets the cliff spike to zero, so the surge
    at 払込満了 is produced endogenously instead of imposed — a cross-check on the 15%
    [std] choice rather than a replacement for it.
    """
    a = whole_life.Projection[1]
    assert a.dyn_lapse() is False
    assert all(a.lapse_dyn_factor(t) == 1.0 for t in range(1, a.proj_len() + 1))

    p = whole_life.Projection[8]
    assert p.dyn_lapse() is True
    assert p.cv_pp(14) / p.cum_prem_pp(14) < 1.0
    assert p.cv_pp(15) / p.cum_prem_pp(15) > 1.0
    assert p.lapse_dyn_factor(14) == 1.0
    assert p.lapse_dyn_factor(15) == pytest.approx(1.2318, abs=5e-5)
    assert p.lapse_dyn_factor(15) == pytest.approx(
        1.0 + 2.0 * (p.cv_pp(15) / p.cum_prem_pp(15) - 1.0), rel=1e-12)
    assert p.lapse_rate(15) == pytest.approx(0.02 * 1.2318, abs=5e-6)
    assert max(p.lapse_dyn_factor(t) for t in range(1, p.proj_len() + 1)) <= 3.0


def test_the_cliff_spike_is_a_separate_parameter(whole_life):
    """The step in CV is contractual; the surge in surrenders at it is an assumption.

    Nothing in any retrieved document quantifies the surge, so it is held as its own
    parameter and switched off on one model point, which is the right way to read its
    effect.  The step itself is unaffected by that switch.
    """
    a, p = whole_life.Projection[1], whole_life.Projection[8]
    assert a.lapse_spike() == 0.15
    assert a.lapse_rate(15) == pytest.approx(0.02 + 0.15, rel=1e-12)
    assert a.lapse_rate(14) == 0.02 and a.lapse_rate(16) == 0.02

    assert p.lapse_spike() == 0.0
    assert p.lapse_rate(15) < 0.05                 # no imposed surge
    # The contractual step is identical on both points.
    assert p.cv_pp(15) == pytest.approx(a.cv_pp(15), rel=1e-14)
    assert p.cv_pp(15) / p.cv_pp_susp(15) == pytest.approx(1.0 / 0.70, rel=1e-14)


def test_the_paid_up_conversion_is_off_in_the_base_run_and_rebases_when_elected(
        whole_life):
    """払済保険: premiums stop, the sum assured is replaced, and the value is re-based.

    The conversion is made on the value at the previous anniversary, so the resulting
    払済保険金額 is a fraction of the original sum assured.  It is a contractual re-basing
    rather than a roll-forward step, which is why the policy-value check excludes that
    one anniversary — and the 払込満了 lapse spike does not apply to a contract already
    converted [std].
    """
    a = whole_life.Projection[1]
    assert a.pua_year() == 0
    assert a.pua_sum_assured() == 0.0
    assert all(a.is_paid_up(t) is False for t in (1, 15, 40))

    p = whole_life.Projection[4]
    assert p.pua_year() == 10
    assert p.prem_term() == 20 and p.prem_end() == 9
    assert p.premiums(9) > 0.0 and p.premiums(10) == 0.0
    assert p.pua_sum_assured() == pytest.approx(4700513.07, abs=YEN)
    assert p.pua_sum_assured() < 0.5 * p.sum_assured()
    assert p.sum_assured_at(9) == p.sum_assured()
    assert p.sum_assured_at(10) == pytest.approx(p.pua_sum_assured(), rel=1e-14)
    # A single-premium contract has no 解約控除 left to take, and no cliff to spike at.
    assert p.surr_charge_pp(8) > 0.0 and p.surr_charge_pp(10) == 0.0
    assert p.lapse_rate(20) == 0.02
    assert p.check_pol_val_roll_fwd() is True
    assert p.check_pol_val_roll_fwd_resid(9) == 0.0     # the re-basing year, excluded


def test_the_five_year_dividend_is_off_in_the_base_run_and_declares_when_elected(
        whole_life):
    """無配当 composite, 5年ごと利差配当 variant: the column is published either way.

    A column of zeros states the product fact; a missing column would hide it, and the
    participating variant is a real product in the source set.
    """
    a = whole_life.Projection[1]
    assert a.dividend_type() == "none"
    assert "dividends" in a.result_cf().columns
    assert (a.result_cf()["dividends"] == 0.0).all()

    p = whole_life.Projection[9]
    assert p.dividend_type() == "five_year"
    assert p.dividends(4) == 0.0
    assert p.dividends(5) == pytest.approx(12157.08, abs=YEN)
    assert p.dividends(5) == pytest.approx(
        0.0025 * 5 * p.pol_val_pp(5) * p.pols_if_at(5, "BEF_LAPSE"), rel=1e-12)
    assert [t for t in range(1, 46) if p.dividends(t) != 0.0] == list(range(5, 46, 5))
    assert p.result_cf()["dividends"].sum() == pytest.approx(81241.81, abs=YEN)


def test_mort_be_factor_is_one_in_the_base_run_and_is_named_as_a_lever(whole_life):
    """At 1.00 the base run is a valuation-table run, not a best estimate.

    生保標準生命表2018（死亡保険用）carries a roughly-2σ prudential margin and a built-in
    improvement allowance, and no retrieved source sizes either against current insured
    experience — so 1.00 is a stated choice rather than a default.  Model point 9 moves
    it, and claims move proportionately while the cash-value construction, which reads
    the table unadjusted, does not.
    """
    a = whole_life.Projection[1]
    assert a.mort_be_factor() == 1.00
    for t in (1, 20, 60):
        assert a.mort_rate(t) == pytest.approx(a.mort_rate_base(t), rel=1e-14)

    p = whole_life.Projection[9]
    assert p.mort_be_factor() == 0.85
    for t in (1, 10, 30):
        assert p.mort_rate(t) == pytest.approx(0.85 * p.mort_rate_base(t), rel=1e-14)
    # The 算出方法書 basis is not a best-estimate lever, so pi reads the table straight.
    assert p.prem_net_level_pp() == pytest.approx(
        p.sum_assured() * p.epv_death(60) / p.annuity_due(60, 10), rel=1e-12)


# ---------------------------------------------------------------------------
# Structural product facts


def test_there_is_no_maturity_benefit_and_no_tail_states(whole_life):
    """終身 means no expiry date and no 満期保険金, so nothing is paid at the horizon.

    Only the death benefit falls in the final year.  There is no maturity cells and no
    maturity kind, unlike the term models in this library, whose survivors reach the end
    of the term with their cover simply running out.
    """
    a = whole_life.Projection[1]
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for absent in ("pols_maturity", "claims_maturity", "policy_term", "maturity_age"):
        assert absent not in names, f"{absent}: this contract does not mature"
    t_end = a.proj_len()
    assert a.claims(t_end) == pytest.approx(a.claims(t_end, "DEATH"), rel=1e-12)
    assert a.pols_lapse(t_end) == 0.0        # nobody survives to surrender
    with pytest.raises(FormulaError):
        a.claims(1, "MATURITY")


def test_the_result_table_has_the_library_column_vocabulary(jp_wl_anchor):
    """pols_if first, net_cf present, and one column per cash flow line."""
    df = jp_wl_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "claim_expenses",
        "expenses", "commissions", "dividends", "net_cf",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, 81))
    assert df.loc[1, "net_cf"] == pytest.approx(-47665.12, abs=YEN)


def test_net_cf_carries_the_notes_own_sign(whole_life):
    """The notes' CF(t) is already income-positive, so there is no liability_cf here.

    A deep new business strain in year 1, a long positive stretch while the premium runs,
    then one violent negative year at the cliff and a run-off with no premium at all.
    """
    assert "liability_cf" not in whole_life.Projection.cells
    a = whole_life.Projection[1]
    assert a.net_cf(1) < -40000.0
    assert all(a.net_cf(t) > 0.0 for t in (2, 3, 4, 5, 14))
    assert a.net_cf(15) < -200000.0
    assert all(a.net_cf(t) < 0.0 for t in (16, 40, 80))


def test_this_is_a_cash_surrender_value_not_an_account_value(whole_life):
    """cv_pp, never av_pp: the value is a contractual formula, not a fund balance."""
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    assert "cv_pp" in names
    for absent in ("av_pp", "av_pp_at", "av_at", "prem_to_av_pp", "withdrawals"):
        assert absent not in names, f"{absent} belongs to an account-value product"


def test_invalid_enum_values_raise(whole_life):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    a = whole_life.Projection[1]
    with pytest.raises(FormulaError):
        a.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        a.claims(1, "SURRENDER")


def test_the_docstrings_describe_the_current_structure(whole_life):
    """Specifics a reader relies on, asserted so they cannot go stale silently."""
    doc = flat(whole_life.doc)
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "no tail states and no expiry" in doc

    proj = flat(whole_life.Projection.doc)
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    for cells in ("pol_val_pp", "cv_pp", "cv_pp_susp", "loan_apl_pp", "apl_test_val",
                  "prem_end", "proj_len", "model_point"):
        assert cells in proj
    assert "cliff is a step, not a ramp" in proj

    data = flat(whole_life.Data.doc)
    assert "TradLife_A" in data                  # the layout it follows
    for cells in ("input_dir", "model_point_table", "mort_table"):
        assert cells in data


def test_the_projection_docstring_describes_the_shipped_model_points(whole_life):
    """The module summary must match the model point table it describes.

    A docstring that names a drawdown the table does not carry is worse than none: it is
    the one place a reader looks to find out what the shipped points exercise.
    """
    proj = flat(whole_life.Projection.doc)
    table = whole_life.Data.model_point_table()
    assert "fortieth anniversary" in proj
    assert int(table.loc[7, "pol_loan_year"]) == 40
    assert float(table.loc[7, "pol_loan_util"]) == 0.9


# ---------------------------------------------------------------------------
# Inputs


def test_inputs_live_beside_the_model():
    """The three input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_the_csvs_are_utf8_without_a_bom():
    """The provenance columns are Japanese, so the encoding is load-bearing."""
    for name in ("model_point_table.csv", "mort_table.csv", "lapse_table.csv"):
        raw = (MODEL_DIR.parent / name).read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"{name} carries a BOM"
        raw.decode("utf-8")


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """ANCHOR rows are quoted and attributed; every other age is a [std] interpolation.

    The publisher's terms prohibit reproduction of 生保標準生命表2018（死亡保険用）, so this
    library ships a construction rather than a copy.  Marking the rows is what stops the
    file being mistaken for the published table.  The file is the **canonical jplib death
    table**, shipped identically by every product that needs it, so the whole provenance
    string is asserted and not merely its prefix: a cell carrying the same number under a
    different story in another product is exactly the drift this file exists to end.
    """
    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith("[std] canonical jplib").all()

    quoted = table[table["provenance"].str.contains("ANCHOR row")]
    constructed = table[table["provenance"].str.contains("INTERPOLATED row")]
    assert len(quoted) + len(constructed) == len(table)
    assert len(constructed) > len(quoted)        # most of the file is the construction
    assert "log-linear in ln q" in constructed["provenance"].iloc[0]
    assert constructed["provenance"].str.contains("not an IAJ value").all()

    # Every anchor row quotes its own rate back, to the 5 dp the file carries.
    for sex, age, rate, prov in zip(quoted["sex"], quoted["age"],
                                    quoted["mort_rate"], quoted["provenance"]):
        kanji = "男" if sex == "M" else "女"
        assert kanji in prov
        assert "q({}) = {:.5f} is the sourced rate".format(age, rate) in prov
        assert "[REG-R18]" in prov and "[REG-R21]" in prov

    male_quoted = set(quoted[quoted["sex"] == "M"]["age"])
    # The worked example's assumption list quotes q(30) ... q(34) as read rates.
    assert {30, 31, 32, 33, 34} <= male_quoted
    assert {15, 20, 25, 35, 40, 45, 50, 105} <= male_quoted   # the skeleton
    # q(43) and q(44) print in the worked-example table and are fills, not reads.
    assert not ({43, 44} & male_quoted)
    assert 109 in male_quoted and 113 in set(quoted[quoted["sex"] == "F"]["age"])

    terminal = table[table["mort_rate"] >= 1.0]
    assert sorted(zip(terminal["sex"], terminal["age"])) == [("F", 113), ("M", 109)]


def test_the_shipped_mortality_table_interpolates_between_its_anchors():
    """Every INTERPOLATED row is exactly the log-linear fill of its two anchors.

    The provenance column claims a construction rule; this asserts the file obeys it.
    A rate edited by hand — or an anchor quietly relabelled — changes a row that the rule
    can still reproduce from its neighbours, so nothing but this test would catch it.  It
    also pins the shape the notes and ``model.md`` describe: over the shipped range, 27 of
    the 95 male rows and 24 of the 99 female rows are anchors and the rest are fills, and
    nothing is extrapolated at either end.
    """
    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    for sex in ("M", "F"):
        sub = table[table["sex"] == sex]
        quoted = sub[sub["provenance"].str.contains("ANCHOR row")]
        anchors = dict(zip(quoted["age"], quoted["mort_rate"]))
        ages = sorted(anchors)
        # The construction cannot extrapolate: every row sits inside the anchor range.
        assert sub["age"].min() == ages[0] and sub["age"].max() == ages[-1]
        for age, rate, prov in zip(sub["age"], sub["mort_rate"], sub["provenance"]):
            if "INTERPOLATED row" not in prov:
                continue
            lo = max(a for a in ages if a < age)
            hi = min(a for a in ages if a > age)
            f = (age - lo) / (hi - lo)
            fill = round(math.exp((1 - f) * math.log(anchors[lo])
                                  + f * math.log(anchors[hi])), 5)
            assert rate == pytest.approx(fill, abs=5e-11), (sex, age)
            assert "anchors at ages {} and {}".format(lo, hi) in prov

    male = table[table["sex"] == "M"]
    female = table[table["sex"] == "F"]
    assert len(male) == 95 and len(female) == 99
    assert male["provenance"].str.contains("ANCHOR row").sum() == 27
    assert female["provenance"].str.contains("ANCHOR row").sum() == 24
    # The range shipped is the range the model reads: issue age 15 up to each omega.
    assert male["age"].min() == 15 and male["age"].max() == 109
    assert female["age"].min() == 15 and female["age"].max() == 113


def test_the_lapse_table_holds_no_spike():
    """The 払込満了 surge is a model point parameter, not a row of the assumption table.

    Keeping it out of the table is what lets it be switched off and its effect read
    directly; folding it in would make a behavioural assumption look like a duration
    curve.
    """
    table = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    assert list(table["lapse_rate"]) == [0.04, 0.03, 0.02]
    assert table["provenance"].notna().all()
    assert table["lapse_rate"].max() < 0.05
    assert "lapse_spike" in pd.read_csv(
        MODEL_DIR.parent / "model_point_table.csv").columns


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a same-schema file and the projection follows.

    This is the property the external-file layout buys, and it is exactly what a user who
    has downloaded the IAJ PDF does with the real table: drop it in as a CSV, change no
    formula.
    """
    src = MODEL_DIR.parent / "mort_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "age"])
    doubled["mort_rate"] = (doubled["mort_rate"] * 2).clip(upper=1.0)

    model = mx.read_model(MODEL_DIR, name="WholeLife_JP_A_swap")
    try:
        alt_name = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].claims(1, "DEATH")
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].claims(1, "DEATH") == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_model_point_premiums_follow_the_documented_rule(whole_life):
    """Nine of the ten premiums are solved from the anchor's; the anchor's is sourced.

    ``model.md`` states the rule under Standardizations: a suppressed cell is priced at
    the anchor's ratio of gross premium to net level premium, and an ordinary cell
    divides that by the 83.7% the one carrier publishing both scales for one identical
    model point discloses.  Without this test a premium typed into the CSV by hand moves
    every cash flow on that point and nothing in the suite notices — it is exactly the
    four-way drift the parameter tables exist to prevent.
    """
    anchor = whole_life.Projection[1]
    gross_to_net = anchor.premium_pp() / anchor.prem_net_level_pp()
    assert gross_to_net == pytest.approx(174960.0 / PI, rel=1e-6)
    assert gross_to_net == pytest.approx(0.990608, abs=5e-7)

    table = whole_life.Data.model_point_table()
    assert len(table) == 10
    priced_ordinary = set()
    for point_id in table.index:
        p = whole_life.Projection[point_id]
        if point_id == 6:
            # The one documented exception: point 6 is the ordinary form of the anchor
            # held at the anchor's own premium, so that points 5 and 6 differ in k alone
            # and the APL comparison is one advance against thirteen on one price.
            assert p.low_cv() is False
            assert p.premium_pp() == anchor.premium_pp()
            continue
        factor = gross_to_net if p.low_cv() else gross_to_net / LOW_CV_PREMIUM_RATIO
        assert p.premium_pp() == pytest.approx(
            round(factor * p.prem_net_level_pp()), abs=0.5), point_id
        if not p.low_cv():
            priced_ordinary.add(point_id)
    assert priced_ordinary == {2, 4, 10}
    # Point 2 is the anchor's own ordinary twin, at the sourced price.
    assert whole_life.Projection[2].premium_pp() == 209032.0
    assert (anchor.premium_pp() / whole_life.Projection[2].premium_pp()
            == pytest.approx(LOW_CV_PREMIUM_RATIO, abs=5e-6))


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    model = mx.read_model(MODEL_DIR, name="WholeLife_JP_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="WholeLife_JP_A_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[1], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[8], abs=YEN)
        assert anchor.cv_pp(15) == pytest.approx(WORKED_EXAMPLE_CV[15], abs=YEN)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
