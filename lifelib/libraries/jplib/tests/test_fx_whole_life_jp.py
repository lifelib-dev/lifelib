"""Product tests for ``FXWholeLife_JP_S``, the 外貨建終身保険 reference model.

The house-style contract is asserted once, for every model in the library, in
``test_model_conventions_jp.py``. What is asserted here is this product: the worked example
of ``products/fx_whole_life/technical-notes.md`` **hard-coded** so a reviewer can check it
against the notes by eye, every one of the notes' *Known modeling pitfalls* — each pitfall
being a way an implementation can look right and be wrong — the roll-forward and ledger
identities, and each optional module in both positions.

The anchor cell is male, 契約年齢 40 (満年齢), the LEVEL shape, 米ドル建, 基本保険金額 US$100,000,
保険期間 終身, 60歳払込満了 (240 monthly premiums), 月払保険料 US$239.60, 低解約返戻金特則 off, 積立利率
held at the guaranteed floor of 3.00%, TTM ¥159.43 per US$1 held flat with a ±¥0.50 spread.
``T = 12 x (109 - 40 + 1) = 840`` months.

The goldens are hard-coded in module-level tables — ``TRACE`` for the three month traces,
``FIRST_PERIODS`` for the printed cash-flow table, ``CALIBRATION`` for the nine-duration
charge-stack fit and ``MVA_ROW`` for the rate-move row — carrying the digits the notes
display and nothing further, so the comparison against the document is one of reading
rather than of unpickling. The map below pairs each pitfall with the test that fails if it
is committed.

Two things about this product make its tests different from the rest of the library's.
Everything the model computes is in **US dollars** and the yen columns are a three-rate
translation, so several assertions below exist only to pin the difference between
``net_cf_jpy`` and ``net_cf`` times an exchange rate. And the crediting rate in the base run
sits on the contract's own 予定利率, which makes the 増加死亡保険金額 and the 特別積立金 vanish
identically — so *zero* is the assertion, and a non-zero value there is a bug rather than a
refinement.
"""
import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from jp_registry import model_path

# The model folder, located through the registry rather than by walking the tree, so that
# a copy made by ``lifelib.create()`` tests *that copy's* model.
MODEL_DIR = model_path("FXWholeLife_JP_S")

# Every model point the CSV ships, read at collection time because a parametrization has to
# be built before any fixture exists.  This was written out as ``[1, 2, 3, 4, 5, 6, 7, 8]``
# in three places, which matched the file and would have gone on matching it silently: an
# added model point would simply not have been parametrized over, and the tests would have
# kept passing over less of the table.
POINT_IDS = list(
    pd.read_csv(MODEL_DIR.parent / "model_point_table.csv")["point_id"])


# Every entry of the notes' "Known modeling pitfalls" list, and the test that would fail
# if the pitfall were committed.  The list is the contract between the notes and this
# module: a pitfall without a test is a claim nobody checks.
#
#   the policy currency is the model currency
#       test_the_policy_currency_is_the_model_currency
#   net_cf_jpy(t) != net_cf(t) x e(t)
#       test_net_cf_jpy_is_not_net_cf_times_the_exchange_rate
#   the account-value charges are not cash flows
#       test_the_account_value_charges_are_not_cash_flows
#   av_pp is not cv_pp
#       test_av_pp_is_not_cv_pp
#   the MVA is not a charge: symmetric, and negative where rates fall
#       test_the_mva_is_symmetric_and_can_be_negative,
#       test_the_zero_move_column_is_not_zero,
#       test_the_mva_is_zero_on_a_rate_basis_date,
#       test_the_mva_is_absent_on_the_level_shape
#   the surrender charge's base is the 積立金
#       test_the_surrender_charge_base_is_the_account_value_not_the_sum_assured
#   the target test runs on the surrender value, after FX and the MVA
#       test_the_target_test_runs_on_the_surrender_value
#   the one-year dead zone is real
#       test_the_one_year_dead_zone_is_contractual
#   the uplift and the top-up are identically zero on the guaranteed run
#       test_the_uplift_and_the_top_up_are_identically_zero_at_the_floor
#   mort_be_factor must not move the cost-of-insurance charge
#       test_mort_be_factor_moves_the_decrement_and_never_the_charge
#   the APL is absent on the SINGLE shape
#       test_the_apl_is_structurally_absent_on_the_single_shape
#   the crediting month is the policy month
#       test_the_crediting_month_is_the_policy_month
#   (1 + ic)^(1/12), not ic/12
#       test_the_monthly_interest_convention_is_the_geometric_twelfth_root
#   the 低解約返戻金 release is a step
#       test_the_low_cv_release_is_a_step_not_a_ramp
#   the account value can overtake the sum assured
#       test_the_account_value_can_overtake_the_sum_assured
#   the account value can also be exhausted, and the charge stops there
#       test_the_account_value_never_runs_negative
#   a refused claim still pays the fund
#       test_a_refused_claim_still_pays_the_fund


# ---------------------------------------------------------------------------
# The worked example, hard-coded to the precision the notes display


def test_the_anchor_cell_is_the_worked_examples_model_point(jp_fxwl_anchor):
    """Model point 1 is the cell the notes' worked example projects."""
    p = jp_fxwl_anchor
    assert p.shape() == "LEVEL"
    assert p.sex() == "M"
    assert p.issue_age() == 40
    assert p.currency() == "USD"
    assert p.sum_assured() == 100_000.0
    assert p.premium_mth_pp() == 239.60          # sourced, not constructed [S2]
    assert p.prem_months() == 240                # 60歳払込満了
    assert p.credit_rate() == 0.0300
    assert p.guar_floor() == 0.0300              # the base run sits on the floor
    assert p.low_cv() is False
    assert p.idb_basis() == "fund"
    assert p.target_on() is False
    assert p.mort_be_factor() == 1.00
    assert p.fx_rate(0) == 159.43
    assert p.fx_spread() == 0.50
    assert p.omega_age() == 109
    assert p.proj_len() == 840                   # 12 x (109 - 40 + 1)


def test_the_worked_examples_assumption_values(jp_fxwl_anchor):
    """Every rate the notes quote for the worked example, to the digits they show.

    The mortality rates are the notes' own quoted values, built by log-linear
    interpolation between the sourced anchors of 生保標準生命表2018（死亡保険用）男 and rounded to
    five decimals.  The interpolation is [std]; the anchors are not.
    """
    p = jp_fxwl_anchor
    assert p.mort_rate(0) == 0.00118             # q40, a sourced anchor
    assert p.mort_rate(12) == 0.00128            # q41, interpolated
    assert p.mort_rate(24) == 0.00139            # q42
    assert p.mort_rate(36) == 0.00151            # q43
    assert p.mort_rate(48) == 0.00163            # q44
    assert p.mort_rate(60) == 0.00177            # q45, a sourced anchor
    assert p.mort_rate(120) == 0.00285           # q50, a sourced anchor
    assert p.mort_rate(240) == 0.00653           # q60, a sourced anchor
    assert p.mort_rate(600) == 0.15760           # q90, a sourced anchor
    assert p.mort_rate(828) == 1.00000           # q109, the terminal rate
    assert p.mort_rate_mth(0) == pytest.approx(0.0000983866, abs=5e-11)
    assert p.lapse_rate(0) == 0.08
    assert p.lapse_rate_mth(0) == pytest.approx(0.0069243826, abs=5e-11)
    assert 1 + p.credit_rate_mth() == pytest.approx(1.0024662698, abs=5e-11)
    assert p.prem_charge_rate(0) == 0.38         # phi1, months 0-23
    assert p.prem_charge_rate(23) == 0.38
    assert p.prem_charge_rate(24) == 0.13        # phi2, months 24-239
    assert p.maint_rate() == 0.005


# The notes' three month-by-month traces ("Trace, month 0 / 1 / 2"), transcribed as the
# notes print them — as strings, so that the number of digits carried here is the number
# of digits the notes display and the tolerance below follows from it rather than being
# chosen.  A reviewer checks this block against the document by eye; nothing is pickled.
TRACE = {
    0: {"premiums": "239.6000000",      # P x l(0), l(0) = 1
        "charge_init": "91.0480",       # 0.38 x 239.60
        "av_aft_prem": "148.5520",      # AVg(0)
        "charge_maint": "0.0618967",    # (0.005/12) x AVg(0)
        "av_aft_maint": "148.4901033",  # the fund the net amount at risk is measured on
        "charge_coi": "9.8240461",      # 0.0000983866 x 99,851.5098967
        "av_next": "139.0080451",       # AV(1)
        "cv_next": "129.2774820",       # CV(1) = AV(1) x 0.93
        "claims_death": "9.8386555",    # 100,000 x D(0)
        "claims_lapse": "0.8950787",    # CV(1) x S(0)
        "claim_expenses": "0.0147580",  # 150 x D(0)
        "expenses": "305.0000000",      # 300.00 acquisition + 5.0000 maintenance
        "commissions": "2587.6800",     # 0.90 x 12 x 239.60
        "net_cf": "-2663.8284922",
        "pols_next": "0.9929779"},      # l(1)
    1: {"premiums": "237.9175077",
        "av_aft_prem": "287.5600451",
        "charge_maint": "0.1198167",
        "charge_coi": "9.8103753",
        "av_next": "278.3145633",
        "cv_next": "258.8325438",
        "claims_death": "9.7695676",
        "claims_lapse": "1.7794951",
        "claim_expenses": "0.0146544",
        "expenses": "4.9648896",        # maintenance only
        "commissions": "0.0000000",     # renewal commission starts at t = 12
        "net_cf": "221.3889011"},
    2: {"premiums": "236.2468301",
        "av_aft_prem": "426.8665633",
        "charge_maint": "0.1778611",
        "charge_coi": "9.7966751",
        "av_next": "417.9201953",
        "cv_next": "388.6657816",
        "claims_death": "9.7009649",
        "claims_lapse": "2.6533455",
        "claim_expenses": "0.0145514",
        "expenses": "4.9300257",
        "net_cf": "218.9479426"},
}


def trace_actual(p, t):
    """What the model says for each line of the notes' month-``t`` trace."""
    return {
        "premiums": p.premiums(t),
        "charge_init": p.charge_init(t),
        "av_aft_prem": p.av_pp_at(t, "AFT_PREM"),
        "charge_maint": p.charge_maint(t),
        "av_aft_maint": p.av_pp_at(t, "AFT_CHARGE_MAINT"),
        "charge_coi": p.charge_coi(t),
        "av_next": p.av_pp(t + 1),
        "cv_next": p.cv_pp(t + 1),
        "claims_death": p.claims(t, "DEATH"),
        "claims_lapse": p.claims(t, "LAPSE"),
        "claim_expenses": p.claim_expenses(t),
        "expenses": p.expenses(t),
        "commissions": p.commissions(t),
        "net_cf": p.net_cf(t),
        "pols_next": p.pols_if(t + 1),
    }


def displayed_tolerance(printed):
    """Half a unit in the last place the notes actually print."""
    decimals = len(printed.partition(".")[2])
    return 0.5 * 10.0 ** -decimals


@pytest.mark.parametrize("t", sorted(TRACE))
def test_the_worked_example_trace(jp_fxwl_anchor, t):
    """The notes' month-``t`` trace, line by line, to the digits the notes print.

    This is the whole account-value recursion in the order the notes fix it — premium in,
    契約初期費用, 維持費, then the 保障部分 charge on the net amount at risk measured *after* the
    維持費, then interest — plus the decrements it feeds and the cash flow they produce.
    Any reordering inside the month moves these figures in the third decimal.
    """
    actual = trace_actual(jp_fxwl_anchor, t)
    for line, printed in TRACE[t].items():
        assert actual[line] == pytest.approx(
            float(printed), abs=displayed_tolerance(printed)), line


def test_the_worked_example_surrender_charge_at_month_one(jp_fxwl_anchor):
    """CV(1) = AV(1) x 0.93: the notes' 7.0% 解約控除 in policy year one, and nothing else.

    The 市場価格調整 and the 低解約返戻金割合 are both inert on this cell, so the whole gap between
    the 積立金 and the 解約返戻金 here is the 解約控除.
    """
    p = jp_fxwl_anchor
    assert p.surr_charge_rate(1) == 0.07
    assert p.mva_rate(1) == 0.0
    assert p.low_cv_rate(1) == 1.0
    assert p.cv_pp(1) == pytest.approx(p.av_pp(1) * 0.93, abs=1e-12)


# The notes' "First periods of the base run" table, verbatim:
# t -> pols_if, premiums, claims_death, claims_lapse, claim_expenses, expenses,
#      commissions, net_cf, av_pp, cv_pp
#      (av_pp and cv_pp stated at the END of the month)
FIRST_PERIODS = {
    0: (1.000000, 239.6000, 9.8387, 0.8951, 0.0148, 305.0000, 2587.6800,
        -2663.8285, 139.01, 129.28),
    1: (0.992978, 237.9175, 9.7696, 1.7795, 0.0147, 4.9649, 0.0000,
        221.3889, 278.31, 258.83),
    2: (0.986005, 236.2468, 9.7010, 2.6533, 0.0146, 4.9300, 0.0000,
        218.9479, 417.92, 388.67),
    3: (0.979081, 234.5879, 9.6328, 3.5167, 0.0144, 4.8954, 0.0000,
        216.5285, 557.83, 518.78),
    4: (0.972206, 232.9406, 9.5652, 4.3697, 0.0143, 4.8610, 0.0000,
        214.1303, 698.03, 649.17),
    5: (0.965379, 231.3049, 9.4980, 5.2125, 0.0142, 4.8269, 0.0000,
        211.7532, 838.54, 779.84),
    119: (0.554213, 132.7893, 11.9760, 58.7416, 0.0180, 3.0307, 3.9837,
          55.0395, 24854.87, 24854.87),
    239: (0.353031, 84.5862, 17.6411, 68.8206, 0.0265, 2.1325, 2.5376,
          -6.5721, 57431.26, 57431.26),
    240: (0.351656, 0.0000, 19.1935, 51.2541, 0.0288, 2.1454, 0.0000,
          -72.6218, 57525.60, 57525.60),
}


@pytest.mark.parametrize("t", sorted(FIRST_PERIODS))
def test_the_first_periods_table(fx_whole_life, t):
    """Every printed cell of the notes' cash-flow table, to the digits shown.

    Money to four decimal places and the account and surrender values to the cent, which
    is the precision the notes state as the tests' target; ``pols_if`` to six decimals.
    """
    row = fx_whole_life.Projection[1].result_cf().loc[t]
    want = FIRST_PERIODS[t]
    assert row["pols_if"] == pytest.approx(want[0], abs=5e-7)
    assert row["premiums"] == pytest.approx(want[1], abs=5e-5)
    assert row["claims_death"] == pytest.approx(want[2], abs=5e-5)
    assert row["claims_lapse"] == pytest.approx(want[3], abs=5e-5)
    assert row["claim_expenses"] == pytest.approx(want[4], abs=5e-5)
    assert row["expenses"] == pytest.approx(want[5], abs=5e-5)
    assert row["commissions"] == pytest.approx(want[6], abs=5e-5)
    assert row["net_cf"] == pytest.approx(want[7], abs=5e-5)
    assert row["av_pp"] == pytest.approx(want[8], abs=5e-3)
    assert row["cv_pp"] == pytest.approx(want[9], abs=5e-3)


# The calibration table: duration -> (sc, model AV, model CV, published 解約返戻金 [S2])
CALIBRATION = {
    3: (0.049, 5895.43, 5606.56, 5557),
    5: (0.035, 11030.45, 10644.39, 10822),
    7: (0.021, 16389.60, 16045.42, 16332),
    10: (0.000, 24854.87, 24854.87, 25082),
    15: (0.000, 40224.87, 40224.87, 40128),
    20: (0.000, 57431.26, 57431.26, 57329),
    30: (0.000, 69377.65, 69377.65, 69516),
    40: (0.000, 81529.59, 81529.59, 81350),
    50: (0.000, 90686.78, 90686.78, 90715),
}


@pytest.mark.parametrize("dur", sorted(CALIBRATION))
def test_the_charge_stack_calibration(fx_whole_life, dur):
    """The back-solved charge stack reproduces the notes' fit table to the cent.

    Three [std] parameters against nine published dollar figures spanning forty-seven
    years [S2].  The published values are carried here too, so the second assertion is
    the actual claim being made about the product: within 1.75% at every duration, and
    within 0.03% at duration 50.
    """
    p = fx_whole_life.Projection[1]
    sc, av, cv, published = CALIBRATION[dur]
    assert p.surr_charge_rate(12 * dur) == pytest.approx(sc, abs=5e-5)
    assert p.av_pp(12 * dur) == pytest.approx(av, abs=5e-3)
    assert p.cv_pp(12 * dur) == pytest.approx(cv, abs=5e-3)
    assert abs(cv - published) / published <= 0.0176      # worst is -1.75% at duration 7


def test_the_cumulative_premium_reconciles_to_the_published_booklet(jp_fxwl_anchor):
    """240 x 239.60 = 57,504.00, the published 払込保険料累計額 at twenty years [S2]."""
    p = jp_fxwl_anchor
    assert 240 * p.premium_mth_pp() == 57_504.00
    assert 36 * p.premium_mth_pp() == 8_625.60   # published as 8,626, rounded up


def test_the_whole_run_totals(fx_whole_life):
    """The notes' undiscounted whole-run totals, per policy issued."""
    df = fx_whole_life.Projection[1].result_cf()
    tot = df.sum()
    assert tot["premiums"] == pytest.approx(34_036.04, abs=5e-3)
    assert tot["claims_death"] == pytest.approx(20_911.81, abs=5e-3)
    assert tot["claims_lapse"] == pytest.approx(23_345.07, abs=5e-3)
    assert tot["claim_expenses"] == pytest.approx(31.37, abs=5e-3)
    assert tot["expenses"] == pytest.approx(1_536.77, abs=5e-3)
    assert tot["commissions"] == pytest.approx(3_525.76, abs=5e-3)
    assert tot["net_cf"] == pytest.approx(-15_314.73, abs=5e-3)
    assert tot["conversions"] == 0.0             # no target rider on this cell


def test_the_decrement_totals_close_on_the_cohort(fx_whole_life):
    """Sum D = 0.209118071 and sum S = 0.790881929, summing to one exactly.

    Surrenders take 79.1% of the cohort out against mortality's 20.9%: a lapse-driven
    liability wearing a mortality product's clothes.
    """
    p = fx_whole_life.Projection[1]
    d = sum(p.pols_death(t) for t in range(p.proj_len()))
    s = sum(p.pols_lapse(t) for t in range(p.proj_len()))
    assert d == pytest.approx(0.209118071, abs=5e-10)
    assert s == pytest.approx(0.790881929, abs=5e-10)
    assert d + s == pytest.approx(1.0, abs=1e-12)
    assert p.pols_if(p.proj_len()) == pytest.approx(0.0, abs=1e-12)


def test_most_death_claims_arrive_after_the_premiums_stop(fx_whole_life):
    """85.2% of expected death claims fall after 払込満了.

    Which is why truncating the projection at 払込満了, or at age 100, is a direct
    understatement rather than a simplification.
    """
    p = fx_whole_life.Projection[1]
    after = sum(p.claims(t, "DEATH") for t in range(240, p.proj_len()))
    total = sum(p.claims(t, "DEATH") for t in range(p.proj_len()))
    assert after / total == pytest.approx(0.852, abs=5e-4)


# ---------------------------------------------------------------------------
# The currency layer — the first pitfall, and the one this product punishes hardest


def test_the_yen_ledger_is_three_translations_not_one(jp_fxwl_anchor):
    """Premiums at e + s, benefits at e - s, expenses and commission at the plain e.

    The notes' month-0 yen trace, to the yen.
    """
    p = jp_fxwl_anchor
    assert p.premiums_jpy(0) == pytest.approx(38_319.23, abs=5e-3)
    assert p.benefits_jpy(0) == pytest.approx(1_705.91, abs=5e-3)
    assert p.expenses_jpy(0) == pytest.approx(461_182.33, abs=5e-3)
    assert p.net_cf_jpy(0) == pytest.approx(-424_569.01, abs=5e-3)


def test_net_cf_jpy_is_not_net_cf_times_the_exchange_rate(jp_fxwl_anchor):
    """The gap is the insurer's spread income, and the model publishes it apart.

    ¥125.17 in month 0 — exactly ``0.50 x (premiums + benefits)`` — against a
    single-rate translation of ¥-424,694.18.  A model that publishes only the second has
    silently given the spread away.
    """
    p = jp_fxwl_anchor
    single_rate = p.net_cf(0) * p.fx_rate(0)
    assert single_rate == pytest.approx(-424_694.18, abs=5e-3)
    assert p.net_cf_jpy(0) != pytest.approx(single_rate, abs=1.0)
    assert p.fx_spread_jpy(0) == pytest.approx(125.17, abs=5e-3)
    assert p.fx_spread_jpy(0) == pytest.approx(
        0.50 * (p.premiums(0) + p.benefits_usd(0)), abs=1e-9)
    assert p.net_cf_jpy(0) == pytest.approx(single_rate + p.fx_spread_jpy(0), abs=1e-6)


def test_the_whole_run_yen_ledger_and_its_spread(fx_whole_life):
    """¥-2,402,482 against ¥-2,441,628, the ¥39,146 gap being the whole-run spread."""
    p = fx_whole_life.Projection[1]
    df = p.result_cf()
    tot = df.sum()
    assert sum(p.premiums_jpy(t) for t in range(840)) == pytest.approx(
        5_443_383, abs=0.5)
    assert sum(p.benefits_jpy(t) for t in range(840)) == pytest.approx(
        7_033_745, abs=0.5)
    assert sum(p.expenses_jpy(t) for t in range(840)) == pytest.approx(
        812_120, abs=0.5)
    assert tot["net_cf_jpy"] == pytest.approx(-2_402_482, abs=0.5)
    assert tot["net_cf"] * 159.43 == pytest.approx(-2_441_628, abs=0.5)
    assert tot["fx_spread_jpy"] == pytest.approx(39_146, abs=0.5)


def test_the_whole_run_yen_identity_has_to_be_summed_on_the_path(fx_whole_life):
    """sum(net_cf_jpy) = sum(net_cf(t) e(t)) + sum(fx_spread_jpy), path or no path.

    ``run.py`` prints the middle term and has to accumulate it month by month.  Summing
    ``net_cf`` first and translating once at ``fx_rate(0)`` reproduces the identity only
    where the rate is flat; on model point 7, which reads ``fx_path_table.csv``, the
    issue-date rate is not the rate the ledger used and the one-rate figure is out by
    over a million yen -- the whole-run form of the first pitfall.
    """
    p = fx_whole_life.Projection[7]
    assert p.fx_path() is True and p.fx_rate(600) != p.fx_rate(0)
    ts = range(p.proj_len())
    on_path = sum(p.net_cf(t) * p.fx_rate(t) for t in ts)
    spread = sum(p.fx_spread_jpy(t) for t in ts)
    assert sum(p.net_cf_jpy(t) for t in ts) == pytest.approx(
        on_path + spread, abs=5e-3)
    at_issue = sum(p.net_cf(t) for t in ts) * p.fx_rate(0)
    assert at_issue - on_path == pytest.approx(-1_234_982, abs=0.5)


def test_the_round_trip_costs_063_percent_before_anything_happens(jp_fxwl_anchor):
    """(e + s)/(e - s) - 1 = 0.6292%, and one leg is s/e = 0.3136%.

    Which is why every carrier warns that a loss can arise with no exchange-rate
    movement at all.
    """
    p = jp_fxwl_anchor
    e, s = p.fx_rate(0), p.fx_spread()
    assert (e + s) / (e - s) - 1 == pytest.approx(0.006292, abs=5e-7)
    assert s / e == pytest.approx(0.003136, abs=5e-7)


def test_a_usd_settled_policy_has_no_spread_at_all(fx_whole_life):
    """Model point 8 attaches neither yen rider, so the yen ledger is one rate.

    The parameter position the whole currency layer is measured against: the difference
    between it and the anchor cell is exactly two conversion spreads.
    """
    p = fx_whole_life.Projection[8]
    assert p.yen_in() is False and p.yen_out() is False
    df = p.result_cf()
    assert df["fx_spread_jpy"].abs().max() == 0.0
    assert (df["net_cf_jpy"] - df["net_cf"] * p.fx_rate(0)).abs().max() == (
        pytest.approx(0.0, abs=1e-6))


def test_the_policy_currency_is_the_model_currency(fx_whole_life):
    """Move the exchange rate and the dollar ledger does not stir; the yen ledger scales.

    Every state variable and every cash flow is in US dollars, and yen enters only through
    ``fx_rate`` and ``fx_spread``.  The rate is a **model point column**: an exchange rate
    buried in a recursion is an economic assumption disguised as a product feature, and a
    model carrying one would show the dollar figures moving here.
    """
    p = fx_whole_life.Projection[1]
    months = (0, 1, 119, 240)
    usd = [p.net_cf(t) for t in months]
    fund = [p.av_pp(t) for t in months]
    jpy = [p.net_cf_jpy(t) for t in months]

    table = fx_whole_life.Data.model_point_table()
    saved = table.loc[1, "fx_ttm"]
    table.loc[1, "fx_ttm"] = 200.0
    try:
        fx_whole_life.Projection[1].clear_all()
        moved = fx_whole_life.Projection[1]
        assert [moved.net_cf(t) for t in months] == pytest.approx(usd, rel=1e-15)
        assert [moved.av_pp(t) for t in months] == pytest.approx(fund, rel=1e-15)
        assert moved.fx_rate(0) == 200.0
        assert all(a != pytest.approx(b, rel=1e-6)
                   for a, b in zip([moved.net_cf_jpy(t) for t in months], jpy))
        assert moved.check_fx_ledger() is True
    finally:
        table.loc[1, "fx_ttm"] = saved
        fx_whole_life.Projection[1].clear_all()


# ---------------------------------------------------------------------------
# Known modeling pitfalls — each one a way to look right and be wrong


def test_the_account_value_charges_are_not_cash_flows(jp_fxwl_anchor):
    """C_init, C_maint and C_coi move av_pp and appear in no cash-flow column.

    Booking a charge as revenue alongside the premium that funded it double-counts the
    premium.  The premium column is the **gross** premium: 239.60, not the 148.5520 that
    reaches the fund and not 239.60 plus the charge.
    """
    p = jp_fxwl_anchor
    assert p.premiums(0) == pytest.approx(239.60, abs=1e-9)
    assert p.prem_to_av_pp(0) == pytest.approx(148.5520, abs=5e-5)
    assert p.charge_init(0) + p.prem_to_av_pp(0) == pytest.approx(239.60, abs=1e-9)
    rebuilt = (p.premiums(0) - p.claims(0) - p.conversions(0)
               - p.claim_expenses(0) - p.expenses(0) - p.commissions(0))
    assert p.net_cf(0) == pytest.approx(rebuilt, abs=1e-9)
    assert p.check_net_cf() is True


def test_av_pp_is_not_cv_pp(jp_fxwl_anchor):
    """CV = AV (1 - mva - sc) kl, and paying a surrender on the fund overstates it.

    At month 1 the 解約控除 alone is 7% of the fund.
    """
    p = jp_fxwl_anchor
    assert p.cv_pp(1) < p.av_pp(1)
    assert p.cv_pp(1) == pytest.approx(p.av_pp(1) * 0.93, abs=1e-9)
    assert p.claims(0, "LAPSE") == pytest.approx(
        p.cv_pp(1) * p.pols_lapse(0), abs=1e-9)
    assert p.check_cv_ledger() is True


def test_the_surrender_charge_base_is_the_account_value_not_the_sum_assured(
        jp_fxwl_anchor):
    """7.0% of the 積立金, not of the 基本保険金額.

    Three different bases are in use across the market and a rate quoted against one
    means nothing against another; applying 7.0% to SA would be wrong by a factor of
    several hundred at month 1.
    """
    p = jp_fxwl_anchor
    charge = p.av_pp(1) - p.cv_pp(1)
    assert charge == pytest.approx(0.07 * p.av_pp(1), abs=1e-9)
    assert charge < 0.07 * p.sum_assured() / 100


def test_the_surrender_charge_runs_to_zero_at_exactly_ten_years(jp_fxwl_anchor):
    """0.7 points per completed policy year, constant within the year, zero from ten."""
    p = jp_fxwl_anchor
    assert p.surr_charge_rate(0) == pytest.approx(0.070, abs=1e-12)
    assert p.surr_charge_rate(11) == pytest.approx(0.070, abs=1e-12)
    assert p.surr_charge_rate(12) == pytest.approx(0.063, abs=1e-12)
    assert p.surr_charge_rate(119) == pytest.approx(0.007, abs=1e-12)
    assert p.surr_charge_rate(120) == 0.0
    assert p.surr_charge_rate(600) == 0.0


def test_the_uplift_and_the_top_up_are_identically_zero_at_the_floor(fx_whole_life):
    """IDB(t) = 0 and 特別積立金 = 0 for every t whenever ic = i0.

    The published guaranteed column shows 特別積立金 of (0) at both 10 and 20 years, so a
    non-zero value on the base run is a bug and not a refinement.
    """
    p = fx_whole_life.Projection[1]
    assert p.credit_rate() == p.guar_floor()
    assert max(p.idb_pp(t) for t in range(p.proj_len() + 1)) == 0.0
    assert max(abs(p.av_pp(t) - p.av0_pp(t))
               for t in range(p.proj_len() + 1)) == pytest.approx(0.0, abs=1e-9)
    assert p.special_reserve_pp(120) == 0.0
    assert p.special_reserve_pp(240) == 0.0
    assert p.benefit_pp(0) == p.sum_assured()
    assert p.benefit_pp(600) == p.sum_assured()


def test_the_uplift_and_the_top_up_come_alive_above_the_floor(fx_whole_life):
    """Model point 5 credits 3.50% over a 3.00% floor, and both mechanics engage.

    The same switch in the other position: the machinery is not merely set to zero, it is
    zero because the guaranteed run makes it so.
    """
    p = fx_whole_life.Projection[5]
    assert p.credit_rate() > p.guar_floor()
    assert p.av_pp(120) > p.av0_pp(120)
    assert p.idb_pp(120) > 0.0
    assert p.benefit_pp(120) > p.sum_assured()
    assert p.special_reserve_pp(120) > 0.0
    assert p.special_reserve_pp(240) > 0.0
    assert p.special_reserve_pp(121) == 0.0      # only at ten and twenty years


# The 特別積立金 shares and the four published amounts they were fitted to: the anchor cell
# run at each of the two illustration rates, against 147 / 527 at 3.50% and 302 / 1,120 at
# 4.00% [S2].  The rates are 0.24 and 0.16 and the notes claim a worst deviation of 3.7%;
# without this test the fit is described in three places and checked in none.
SPECIAL_RESERVE_FIT = {
    0.035: (147, 527),
    0.040: (302, 1_120),
}


@pytest.mark.parametrize("rate", sorted(SPECIAL_RESERVE_FIT))
def test_the_special_reserve_shares_reproduce_the_published_amounts(
        fx_whole_life, rate):
    """0.24 and 0.16 against 147 / 527 at 3.50% and 302 / 1,120 at 4.00%, worst 3.7%.

    The top-up is a **[std]** reconstruction — the 約款 publishes no formula — so the two
    shares only mean anything against the amounts they were fitted to.  The 20-year figure
    is computed on a fund that already carries the compounded 10-year top-up, which is what
    the recursion does and what the fit assumed.
    """
    p = fx_whole_life.Projection[1]
    assert p.charge_param("special_reserve_rate_10") == 0.24
    assert p.charge_param("special_reserve_rate_20") == 0.16

    table = fx_whole_life.Data.model_point_table()
    saved = table.loc[1, "credit_rate"]
    table.loc[1, "credit_rate"] = rate
    try:
        fx_whole_life.Projection[1].clear_all()
        run = fx_whole_life.Projection[1]
        assert run.credit_rate() == rate and run.guar_floor() == 0.03
        want10, want20 = SPECIAL_RESERVE_FIT[rate]
        got10 = run.special_reserve_pp(120)
        got20 = run.special_reserve_pp(240)
        assert got10 > 0.0 and got20 > 0.0
        assert abs(got10 - want10) / want10 <= 0.040
        assert abs(got20 - want20) / want20 <= 0.040
        # The 20-year share is applied to the fund *including* the compounded ten-year
        # top-up, not to the excess the ten-year point measured: dropping it would shift
        # the twenty-year fit by about a tenth and the 3.0% bound would not hold.
        assert got20 == pytest.approx(
            0.16 * (run.av_pp_bef_sr(240) - run.av0_pp(240)), abs=5e-3)
        assert run.av_pp(120) > run.av_pp_bef_sr(120)
    finally:
        table.loc[1, "credit_rate"] = saved
        fx_whole_life.Projection[1].clear_all()
    assert fx_whole_life.Projection[1].special_reserve_pp(120) == 0.0


def test_the_uplift_ratchet_is_a_switch(fx_whole_life):
    """The ratchet holds IDB at its running maximum; it is [unverified] and optional.

    Point 5 has it on, point 7 off.  With it on the uplift is monotone; with it off it
    tracks the raw excess, which can fall.
    """
    on = fx_whole_life.Projection[5]
    off = fx_whole_life.Projection[7]
    assert on.idb_ratchet() is True
    assert off.idb_ratchet() is False
    vals = [on.idb_pp(t) for t in range(0, 700, 12)]
    assert all(b >= a for a, b in zip(vals, vals[1:]))
    raw = [max(0.0, off.av_pp(t) - off.av0_pro_pp(t)) for t in range(0, 700, 12)]
    assert [off.idb_pp(t) for t in range(0, 700, 12)] == pytest.approx(raw, abs=1e-9)


def test_the_prospective_uplift_basis_is_the_other_defensible_definition(
        fx_whole_life):
    """AV - AV0 of -21,818.29 / +8.73 / +67.86 / +22,617.69 on the anchor cell.

    The near-zero crossing at 払込満了 is an independent check on the back-solved charge
    stack — actuarial equivalence predicts a contract almost exactly self-funding at the
    floor — but a definition that manufactures a positive uplift on the guaranteed run
    contradicts the only document that shows that run, so it is the switch and not the
    base.
    """
    p = fx_whole_life.Projection[1]
    for t, want in ((120, -21_818.29), (240, 8.73), (600, 67.86),
                    (839, 22_617.69)):
        assert p.av_pp(t) - p.av0_pro_pp(t) == pytest.approx(want, abs=5e-3)
    assert p.av0_pro_pp(p.proj_len()) == p.sum_assured()


def test_the_uplift_benchmark_basis_is_a_switch_in_both_positions(fx_whole_life):
    """``idb_basis`` selects which ``AV0`` the uplift is measured against, and it matters.

    The base is ``"fund"`` — the same recursion at ``i0`` — under which the uplift is
    identically zero on a guaranteed run.  Model point 7 elects ``"prospective"``, the
    fund needed to carry SA with no future premiums, and the two disagree on that point by
    the whole uplift at ten years: the prospective benchmark is still above the fund there
    while the fund benchmark is already below it.
    """
    base = fx_whole_life.Projection[1]
    assert base.idb_basis() == "fund"
    assert base.idb_pp(240) == pytest.approx(
        max(0.0, base.av_pp(240) - base.av0_pp(240)), abs=1e-9)

    pro = fx_whole_life.Projection[7]
    assert pro.idb_basis() == "prospective"
    for t in (120, 300, 600):
        assert pro.idb_pp(t) == pytest.approx(
            max(0.0, pro.av_pp(t) - pro.av0_pro_pp(t)), abs=1e-9)
    assert pro.idb_pp(120) == 0.0                     # the prospective benchmark still wins
    assert pro.av_pp(120) - pro.av0_pp(120) > 0.0     # the fund benchmark would not
    assert pro.av0_pro_pp(pro.proj_len()) == pro.sum_assured()


def test_mort_be_factor_moves_the_decrement_and_never_the_charge(fx_whole_life):
    """The decrement is an experience assumption; the charge basis is a pricing element.

    Model point 7 runs mort_be_factor = 1.20.  Wiring one lever to both would make the model
    absorb its own mortality sensitivity inside the account value instead of showing it
    in the cash flow.
    """
    p = fx_whole_life.Projection[7]
    assert p.mort_be_factor() == 1.20
    assert p.mort_rate(0) == pytest.approx(1.20 * p.coi_rate(0), abs=1e-12)
    assert p.coi_rate(0) == p.mort_rate(0) / 1.20
    base = fx_whole_life.Projection[1]
    assert p.coi_rate(0) != base.coi_rate(0)     # different issue age, same table read
    assert p.coi_rate_mth(0) < p.mort_rate_mth(0)
    # The load moves the decrement only, so it empties the cohort a year before the
    # table's terminal age — at attained 108, where 1.20 x 0.90733 is capped at 1 — while
    # the charge basis still reads the published rate at that age.
    assert p.mort_rate(876) == 1.0 and p.coi_rate(876) == pytest.approx(0.87193)
    assert p.age(876) == 108 < p.omega_age()
    assert p.pols_if(877) == pytest.approx(0.0, abs=1e-15)


def test_the_account_value_can_overtake_the_sum_assured(fx_whole_life):
    """AV crosses US$100,000 at month 740, attained age 101, and the charge stops there.

    C_coi must be floored at zero and the death benefit must **not** be silently floored
    at the fund in exchange.  In force there is 0.000579, so the effect is immaterial in
    expectation and structural in the code.
    """
    p = fx_whole_life.Projection[1]
    cross = next(t for t in range(p.proj_len() + 1) if p.av_pp(t) >= 100_000.0)
    assert cross == 740
    assert p.age(cross) == 101
    assert p.pols_if(cross) == pytest.approx(0.000579, abs=5e-7)
    assert p.charge_coi(cross) == 0.0
    assert p.benefit_pp(cross) == p.sum_assured()      # not floored at the fund
    assert p.benefit_pp(cross) < p.av_pp(cross)


def test_the_monthly_interest_convention_is_the_geometric_twelfth_root(
        jp_fxwl_anchor):
    """(1 + ic)^(1/12), not ic/12 — the published run is reproduced to the dollar."""
    p = jp_fxwl_anchor
    assert p.credit_rate_mth() == pytest.approx(1.03 ** (1 / 12) - 1, abs=1e-15)
    assert p.credit_rate_mth() != pytest.approx(0.03 / 12, abs=1e-6)
    assert p.mort_rate_mth(0) == pytest.approx(
        1 - (1 - 0.00118) ** (1 / 12), abs=1e-15)
    assert p.lapse_rate_mth(0) == pytest.approx(
        1 - (1 - 0.08) ** (1 / 12), abs=1e-15)


def test_the_crediting_month_is_the_policy_month(fx_whole_life):
    """Everything steps on the 月単位の契約応当日, never on a calendar month end.

    ``t`` counts completed policy months from 契約日, so the attained age, the policy year,
    the mortality rate, the 解約控除 scale and the 特別積立金 durations all turn over at exact
    multiples of twelve from issue.  A model crediting on calendar month ends is wrong by
    the anniversary offset for the whole life of the contract — a fixed error, not a
    rounding one.
    """
    p = fx_whole_life.Projection[1]
    assert p.policy_year(0) == 1 and p.policy_year(11) == 1
    assert p.policy_year(12) == 2
    assert p.age(11) == 40 and p.age(12) == 41
    assert p.mort_rate(11) == 0.00118 and p.mort_rate(12) == 0.00128
    assert p.surr_charge_rate(11) == pytest.approx(0.070, abs=1e-12)
    assert p.surr_charge_rate(12) == pytest.approx(0.063, abs=1e-12)
    # Twelve monthly creditings, and only twelve, take AV(0) to AV(12).
    fund = 0.0
    for t in range(12):
        fund = ((fund + p.prem_to_av_pp(t) - p.charge_maint(t) - p.charge_coi(t))
                * (1 + p.credit_rate_mth()))
    assert p.av_pp(12) == pytest.approx(fund, abs=1e-9)
    # The 特別積立金 dates are policy months 120 and 240 exactly, on the one shipped point
    # where the top-up is not zero.
    live = fx_whole_life.Projection[5]
    assert live.special_reserve_pp(120) > 0.0 and live.special_reserve_pp(240) > 0.0
    assert all(live.special_reserve_pp(t) == 0.0
               for t in (119, 121, 132, 239, 241, 252))


def test_the_low_cv_release_is_a_step_not_a_ramp(fx_whole_life):
    """kl moves 0.70 -> 0.775 -> 0.85 -> 0.925 -> 1.00 on whole remaining years, up.

    Interpolating across the boundary is wrong: the published run shows US$27,706 at
    duration 15 against US$53,029 at duration 20.
    """
    p = fx_whole_life.Projection[2]
    assert p.low_cv() is True
    assert p.low_cv_rate(180) == 0.70            # ceil(60/12) = 5 years remain
    assert p.low_cv_rate(192) == 0.70            # ceil(48/12) = 4, still suppressed
    assert p.low_cv_rate(203) == 0.70            # ceil(37/12) = 4, the last month at 0.70
    assert p.low_cv_rate(204) == 0.775           # ceil(36/12) = 3, the first step
    assert p.low_cv_rate(216) == 0.85            # ceil(24/12) = 2
    assert p.low_cv_rate(228) == 0.925           # ceil(12/12) = 1
    assert p.low_cv_rate(240) == 1.00            # 払込満了: the cliff
    assert p.low_cv_rate(600) == 1.00


def test_the_low_cv_form_reproduces_the_published_cross_check(fx_whole_life):
    """The same three charge parameters, a different premium, a different contract.

    A genuine cross-validation and looser than the primary fit, as it should be: the
    worst deviation is -5.20% at duration 15 against a published run [S2].
    """
    p = fx_whole_life.Projection[2]
    assert p.premium_mth_pp() == 225.00
    model = {3: 3669.20, 5: 6966.38, 7: 10498.61, 10: 16252.70, 15: 26266.61,
             20: 53475.52}
    published = {3: 3560, 5: 7081, 7: 10824, 10: 16892, 15: 27706, 20: 53029}
    for dur, want in model.items():
        assert p.cv_pp(12 * dur) == pytest.approx(want, abs=5e-3)
        assert abs(want - published[dur]) / published[dur] <= 0.0520


def test_the_low_cv_special_condition_is_inert_in_the_base_run(fx_whole_life):
    """The other position of the same switch: ``kl`` is 1.00 everywhere on the anchor.

    The suppression is an elected 特則, not a property of the chassis, so a model point
    that does not elect it must see no suppression at any duration — including in the
    months around 払込満了, where the elected form has its cliff.
    """
    p = fx_whole_life.Projection[1]
    assert p.low_cv() is False
    assert all(p.low_cv_rate(t) == 1.00 for t in range(0, 840, 7))
    assert all(p.low_cv_rate(t) == 1.00 for t in (203, 204, 239, 240, 241))
    on = fx_whole_life.Projection[2]
    assert on.cv_pp(120) == pytest.approx(0.70 * on.av_pp(120), abs=1e-9)


def test_a_refused_claim_still_pays_the_fund(fx_whole_life):
    """免責 incidence is zero in the base run, and a refusal is not a zero-payment event.

    Where a death benefit is excluded the contract still pays the 積立金 or the 解約返戻金 —
    an account-value product's habit that a pure protection model does not have.  So the
    model carries no exclusion decrement at all rather than one that pays nothing, and the
    amount such an event would pay is published on every row: ``av_pp`` and ``cv_pp`` are
    positive from the first month and never written down to zero by a claim.
    """
    names = set(fx_whole_life.Projection.cells) | set(fx_whole_life.Projection.refs)
    for absent in ("excl_rate", "exclusion_rate", "menseki_rate", "pols_excluded",
                   "claims_refused"):
        assert absent not in names, f"{absent}: a zero-payment exclusion decrement"
    p = fx_whole_life.Projection[1]
    for t in (0, 1, 120, 240, 600):
        assert p.claims(t, "DEATH") == pytest.approx(
            p.benefit_pp(t) * p.pols_death(t), abs=1e-9)
        assert p.av_pp(t + 1) > 0.0
        assert p.cv_pp(t + 1) > 0.0
    df = p.result_cf()
    assert (df["av_pp"] > 0.0).all()


def test_the_account_value_never_runs_negative(fx_whole_life):
    """The 積立金 is an account, not a debt, so the charge is capped at what it holds.

    On the 低解約返戻金特則 point the back-solved charge stack does not make the lower premium
    self-funding to the terminal age; without the cap the shortfall compounds into the
    net amount at risk and the projection diverges.
    """
    p = fx_whole_life.Projection[2]
    assert min(p.av_pp(t) for t in range(p.proj_len() + 1)) >= 0.0
    assert min(p.cv_pp(t) for t in range(p.proj_len() + 1)) >= 0.0
    assert p.check_av_roll_fwd() is True


# ---------------------------------------------------------------------------
# The SINGLE shape: the MVA and the target conversion


def test_the_mva_is_absent_on_the_level_shape(jp_fxwl_anchor):
    """Identically zero on the whole LEVEL shape, and rate_period_y is zero with it."""
    p = jp_fxwl_anchor
    assert p.rate_period_y() == 0
    assert all(p.mva_rate(t) == 0.0 for t in range(0, 840, 37))
    assert all(p.mva_rem(t) == 0.0 for t in range(0, 840, 37))


# delta -> (mva(36), CV(36)) from the notes' table, twelve years remaining
MVA_ROW = {
    0.02: (0.155947, 87_194.38),
    0.01: (0.085368, 94_934.87),
    0.0: (0.008118, 103_406.90),
    -0.01: (-0.076506, 112_687.73),
    -0.02: (-0.169292, 122_863.68),
}


@pytest.mark.parametrize("delta", sorted(MVA_ROW))
def test_the_mva_reconstruction_at_month_36(fx_whole_life, delta):
    """The notes' rate-move row, reproduced from the [std] reconstruction.

    ``1 - (1 + (Delta + A)/(1 + r0))^(-d rem)`` with A = 0.10%, r0 = 3.00%, d = 0.70.
    """
    p = fx_whole_life.Projection[3]
    assert p.mva_rem(36) == pytest.approx(12.0, abs=1e-12)
    a = p.charge_param("mva_spread")
    r0 = p.charge_param("mva_base_rate")
    d = p.charge_param("mva_damping")
    mva = 1 - (1 + (delta + a) / (1 + r0)) ** (-d * p.mva_rem(36))
    want_mva, want_cv = MVA_ROW[delta]
    assert mva == pytest.approx(want_mva, abs=5e-7)
    cv = p.av_pp(36) * (1 - mva - p.surr_charge_rate(36))
    assert cv == pytest.approx(want_cv, abs=5e-3)

    # Two of the five columns ship as model points, and on those the assertion is made
    # against the model's own cells rather than against the formula rebuilt here: point 3
    # is the zero-move column and point 4 the -1.0% one.  Without this the row would be
    # checked against an expression the test itself writes, which a mis-wired mva_rate()
    # would survive.
    shipped = {0.0: 3, -0.01: 4}
    if delta in shipped:
        live = fx_whole_life.Projection[shipped[delta]]
        assert live.mva_delta(36) == pytest.approx(delta, abs=1e-12)
        assert live.av_pp(36) == pytest.approx(p.av_pp(36), abs=1e-9)
        assert live.mva_rate(36) == pytest.approx(want_mva, abs=5e-7)
        assert live.cv_pp(36) == pytest.approx(want_cv, abs=5e-3)


def test_the_mva_is_symmetric_and_can_be_negative(fx_whole_life):
    """A fall in rates **increases** the surrender value.

    Implementing the adjustment as a deduction floored at zero models a different
    product.  Model point 4 runs Delta = -1.0% and its CV exceeds its AV.
    """
    p = fx_whole_life.Projection[4]
    assert p.mva_delta(36) == -0.01
    assert p.mva_rate(36) < 0.0
    assert p.cv_pp(36) > p.av_pp(36)
    base = fx_whole_life.Projection[3]
    assert base.mva_rate(36) > 0.0               # zero move still charges 0.81%
    assert p.cv_pp(36) > base.cv_pp(36)


def test_the_zero_move_column_is_not_zero(fx_whole_life):
    """The published table's zero column sits at Delta = -0.1%, which is what A is.

    So a contract surrendered with the market exactly where it started still pays an MVA:
    +0.0095 at fourteen years remaining, +0.0081 at twelve.
    """
    p = fx_whole_life.Projection[3]
    assert p.mva_delta(12) == 0.0
    assert p.mva_rate(12) == pytest.approx(0.0095, abs=5e-5)
    assert p.mva_rate(36) == pytest.approx(0.008118, abs=5e-7)


def test_the_mva_is_zero_on_a_rate_basis_date(fx_whole_life):
    """Zero on an 積立利率計算基準日 — a discontinuity a monthly model must place correctly."""
    p = fx_whole_life.Projection[3]
    assert p.rate_period_y() == 15
    assert p.mva_rate(0) == 0.0
    assert p.mva_rate(180) == 0.0                # the first reset date
    assert p.mva_rate(181) != 0.0
    assert p.mva_rem(180) == pytest.approx(15.0, abs=1e-12)


def test_the_single_shape_death_benefit_follows_the_higher_of_fund_and_value(
        fx_whole_life):
    """max(AV, CV): no sum assured above the fund, and the max binds where mva < 0."""
    neg = fx_whole_life.Projection[4]
    assert neg.benefit_pp(36) == pytest.approx(neg.cv_pp(36), abs=1e-9)
    assert neg.benefit_pp(36) > neg.av_pp(36)
    pos = fx_whole_life.Projection[3]
    assert pos.benefit_pp(36) == pytest.approx(pos.av_pp(36), abs=1e-9)
    assert pos.idb_pp(36) == 0.0                 # no uplift on this shape at all


def test_the_single_shape_carries_no_in_force_charge(fx_whole_life):
    """Its costs sit inside the declared 積立利率; only the front-end charge is outside.

    Which is what reproducing its published surrender-value run requires: the fund grows
    at the declared rate exactly.
    """
    p = fx_whole_life.Projection[3]
    assert p.maint_rate() == 0.0
    assert p.coi_charged() is False
    assert p.charge_init(0) == pytest.approx(0.045 * 100_000.0, abs=1e-9)
    assert p.av_pp_at(0, "AFT_PREM") == pytest.approx(95_500.00, abs=5e-3)
    assert p.charge_maint(36) == 0.0
    assert p.charge_coi(36) == 0.0
    assert p.av_pp(36) == pytest.approx(95_500.0 * 1.0472 ** 3, abs=5e-3)


def test_the_target_test_runs_on_the_surrender_value(fx_whole_life):
    """Month 52, and testing the account value converts thirteen months early.

    The two counterfactuals that drop one deduction at a time land at month 41 (no
    解約控除, the larger of the two over this window) and month 50 (no MVA).  The notes
    order the two counterfactuals by naming the deductions at the two months that bound
    the window, so those four figures are asserted here as well: the 解約控除 moves the
    trigger further because 4.9% and 4.2% dwarf 0.78% and 0.72%.
    """
    p = fx_whole_life.Projection[3]
    assert p.premium_jpy0() == pytest.approx(15_993_000.0, abs=0.5)
    assert p.target_amount_jpy() == pytest.approx(17_592_300.0, abs=0.5)
    assert p.target_month() == 52
    assert p.av_pp(52) == pytest.approx(116_626.82, abs=5e-3)
    assert p.mva_rate(52) == pytest.approx(0.007219, abs=5e-7)
    assert p.surr_charge_rate(52) == pytest.approx(0.042, abs=5e-5)
    assert p.cv_pp(52) == pytest.approx(110_886.51, abs=5e-3)
    assert p.cv_pp(52) * (p.fx_rate(52) - p.fx_spread()) == pytest.approx(
        17_623_193, abs=0.5)
    assert p.surr_charge_rate(41) == pytest.approx(0.049, abs=5e-5)
    assert p.mva_rate(41) == pytest.approx(0.0078, abs=5e-5)
    assert p.mva_rate(52) == pytest.approx(0.0072, abs=5e-5)
    assert p.surr_charge_rate(41) > 6 * p.mva_rate(41)
    assert p.surr_charge_rate(52) > 5 * p.mva_rate(52)

    out = p.fx_rate(0) - p.fx_spread()
    target = p.target_amount_jpy()
    assert next(t for t in range(12, 600)
                if p.av_pp(t) * out >= target) == 39
    assert next(t for t in range(12, 600)
                if p.av_pp(t) * (1 - p.mva_rate(t)) * out >= target) == 41
    assert next(t for t in range(12, 600)
                if p.av_pp(t) * (1 - p.surr_charge_rate(t)) * out >= target) == 50


def test_the_one_year_dead_zone_is_contractual(fx_whole_life):
    """A target reached inside the first year does not trigger the conversion."""
    p = fx_whole_life.Projection[4]
    assert p.target_hit(11) is False
    hit_ignoring_the_zone = [t for t in range(0, 12) if
                             p.cv_pp(t) * (p.fx_rate(t) - p.fx_spread())
                             >= p.target_amount_jpy()]
    assert all(p.target_hit(t) is False for t in hit_ignoring_the_zone)
    assert p.target_month() >= 12


def test_a_fall_in_rates_alone_triggers_the_conversion(fx_whole_life):
    """At Delta = -1.0% the yen-converted CV is above the 目標額 at duration three.

    Entirely without help from the crediting rate or the currency: ¥17,909,461 against a
    目標額 of ¥17,592,300.

    The trigger itself lands at month 33, not at the notes' month 52: this point runs the
    negative 市場価格調整 and dynamic surrender, which is the deliberate variant, so a reader
    must not read it against the notes' anchor.  The month is pinned here rather than
    bounded so that the distinction is recorded rather than inferred.
    """
    p = fx_whole_life.Projection[4]
    assert p.cv_pp(36) * (p.fx_rate(36) - p.fx_spread()) == pytest.approx(
        17_909_461, abs=0.5)
    assert p.target_month() == 33
    flat = fx_whole_life.Projection[3]
    assert flat.target_month() == 52
    assert p.target_month() < flat.target_month()


def test_the_two_target_elections_book_the_value_in_different_places(fx_whole_life):
    """convert -> conversions; surrender -> claims_lapse.  Neither is a default.

    The contract converts to a yen whole life; the observed population surrenders and
    re-buys.  The dollar ledger stops either way, and where the money is booked is the
    difference the model can show.
    """
    conv = fx_whole_life.Projection[3]
    surr = fx_whole_life.Projection[4]
    assert conv.target_action() == "convert"
    assert surr.target_action() == "surrender"

    m = conv.target_month()
    assert conv.conversions(m - 1) > 0.0
    assert conv.result_cf()["conversions"].sum() > 0.0
    assert conv.pols_target(m - 1) > 0.0
    assert conv.pols_if(m) == 0.0                # the dollar ledger stops

    ms = surr.target_month()
    assert surr.conversions(ms - 1) == 0.0
    assert surr.result_cf()["conversions"].sum() == 0.0
    assert surr.pols_target(ms - 1) > 0.0
    assert surr.pols_if(ms) == 0.0


def test_the_target_rider_is_off_in_the_base_run(fx_whole_life):
    """The other position of the switch: no rider, no conversion month, no column.

    ``conversions`` is a column of zeros on every model point without the rider, and
    ``target_month()`` sits past the horizon so that nothing downstream is truncated by
    a conversion that never happens.
    """
    for pid in (1, 2, 5, 6, 7, 8):
        p = fx_whole_life.Projection[pid]
        assert p.target_on() is False
        assert p.target_month() == p.proj_len() + 1
        assert all(p.pols_target(t) == 0.0 for t in range(0, p.proj_len(), 11))
        assert p.result_cf()["conversions"].abs().max() == 0.0
        # The ledger runs on to the mortality horizon instead of stopping at a hit: on
        # every one of these points the cohort is emptied by the terminal rate, not by a
        # conversion, and the last month anyone is in force is a mortality event.
        last = max(t for t in range(p.proj_len()) if p.pols_if(t) > 0.0)
        assert p.mort_rate(last) == 1.0
        assert p.pols_death(last) == pytest.approx(p.pols_if(last), abs=1e-15)


def test_target_action_has_no_default(fx_whole_life):
    """A model point electing the rider must choose; the model refuses to assume.

    ``"none"`` is legal only where the rider is not elected, and the two elections are
    the only other values the cells accepts.
    """
    assert fx_whole_life.Projection[3].target_action() == "convert"
    assert fx_whole_life.Projection[4].target_action() == "surrender"
    assert fx_whole_life.Projection[1].target_on() is False
    assert fx_whole_life.Projection[1].target_action() == "none"


# ---------------------------------------------------------------------------
# The 自動振替貸付 — a decrement set, not a decrement rate


def test_the_apl_is_structurally_absent_on_the_single_shape(fx_whole_life):
    """A SINGLE point carrying a premium-default decrement is rejected by name.

    There is no premium to advance, so the two shapes have different decrement *sets*.
    """
    for pid in (3, 4, 8):
        assert fx_whole_life.Projection[pid].apl_on() is False
        assert fx_whole_life.Projection[pid].pols_if_apl(60) == 0.0
        assert fx_whole_life.Projection[pid].loan_pp(60) == 0.0


def test_the_apl_is_off_on_the_anchor_and_on_where_it_is_elected(fx_whole_life):
    """Off in the base run; on model point 6 it engages once the fund can carry a premium.

    A policy does not lapse while the account value can advance the premium, so applying
    a lapse rate to unpaid premiums without running that test models a decrement the
    contract does not have.
    """
    off = fx_whole_life.Projection[1]
    assert off.apl_on() is False
    assert max(off.pols_if_apl(t) for t in range(0, 840, 12)) == 0.0
    assert off.pols_payer(120) == off.pols_if(120)

    on = fx_whole_life.Projection[6]
    assert on.apl_on() is True
    assert on.apl_intercept(0) is False           # no surrender value yet
    start = next(t for t in range(on.proj_len()) if on.apl_intercept(t))
    assert on.cv_pp(start) >= on.prem_due_pp(start)
    assert on.cv_pp(start - 1) < on.prem_due_pp(start - 1)
    assert on.pols_if_apl(start + 1) > 0.0
    assert on.loan_pp(start + 2) > 0.0
    assert on.pols_payer(start + 12) < on.pols_if(start + 12)
    assert on.premiums(start + 12) == pytest.approx(
        on.prem_due_pp(start + 12) * on.pols_payer(start + 12), abs=1e-9)


def test_the_apl_suppresses_the_non_payment_share_of_the_decrement(fx_whole_life):
    """The intercepted mass is redirected, not lost: the roll-forward still closes."""
    p = fx_whole_life.Projection[6]
    start = next(t for t in range(p.proj_len()) if p.apl_intercept(t))
    assert p.pols_lapse(start) < p.pols_lapse(start - 1) * 1.05
    assert p.pols_if(start) == pytest.approx(
        p.pols_payer(start) + p.pols_if_apl(start), abs=1e-12)
    assert p.check_pols_roll_fwd() is True


# ---------------------------------------------------------------------------
# Dynamic surrender and the FX path — the two remaining optional modules


def test_dynamic_surrender_is_off_in_the_base_run_and_on_where_elected(fx_whole_life):
    """The multiplier is 1 everywhere with the module off, and moves with it on."""
    off = fx_whole_life.Projection[3]
    assert off.dyn_lapse() is False
    assert all(off.lapse_dyn_factor(t) == 1.0 for t in range(0, 600, 37))
    assert off.lapse_rate(0) == off.lapse_rate_base(0)

    on = fx_whole_life.Projection[4]
    assert on.dyn_lapse() is True
    factors = [on.lapse_dyn_factor(t) for t in range(0, 400, 12)]
    assert min(factors) >= 0.5 and max(factors) <= 2.5
    assert len(set(round(f, 6) for f in factors)) > 1
    assert on.lapse_rate(120) != on.lapse_rate_base(120)
    # The multiplier is the notes' own expression in the yen-profit ratio, and a policy in
    # yen profit surrenders faster: at month 36 the surrender value is worth more yen than
    # the premium bought, so the factor is above 1 and the annual rate above the table's.
    ratio = on.cv_pp(36) * (on.fx_rate(36) - on.fx_spread()) / on.premium_jpy0()
    assert ratio > 1.0
    assert on.lapse_dyn_factor(36) == pytest.approx(
        min(2.5, max(0.5, 1 + 2.0 * (ratio - 1))), abs=1e-12)
    assert on.lapse_rate(36) == pytest.approx(
        on.lapse_rate_base(36) * on.lapse_dyn_factor(36), abs=1e-12)
    assert on.lapse_rate(36) > on.lapse_rate_base(36)
    assert on.lapse_rate_mth(36) == pytest.approx(
        1 - (1 - on.lapse_rate(36)) ** (1 / 12), abs=1e-15)


def test_the_fx_path_module_is_off_in_the_base_run_and_on_where_elected(fx_whole_life):
    """The base run holds the rate flat; model point 7 reads the path table."""
    off = fx_whole_life.Projection[1]
    assert off.fx_path() is False
    assert all(off.fx_rate(t) == 159.43 for t in range(0, 840, 37))

    on = fx_whole_life.Projection[7]
    assert on.fx_path() is True
    assert on.fx_rate(0) == 159.43
    assert on.fx_rate(120) != 159.43
    assert on.fx_rate(600) == on.fx_rate(840)    # the last row is carried forward


# ---------------------------------------------------------------------------
# The model refuses inputs that describe a contract that does not exist


@pytest.mark.parametrize("point_id,column,value,cells", [
    (1, "shape", "YEN_PREMIUM", "shape"),
    (1, "currency", "AUD", "currency"),
    (1, "idb_basis", "retrospective", "idb_basis"),
    (1, "target_action", "hold", "target_action"),
    (1, "sex", "X", "sex"),
    (3, "apl_on", True, "apl_on"),
    (1, "target_on", True, "target_on"),
    (1, "dyn_lapse", True, "dyn_lapse"),
    (5, "low_cv", True, "low_cv"),
])
def test_an_out_of_scope_model_point_is_rejected_by_name(
        fx_whole_life, point_id, column, value, cells):
    """Scope limits are stated and enforced, not smoothed over.

    Three of these are contracts that do not exist rather than parameters out of range.
    The third market shape — a level *yen* premium converted to US dollars each month —
    is a different cash-flow object, and only USD and AUD are inside the 標準責任準備金
    regime, of which the composite writes USD.  The 自動振替貸付 has no premium to advance
    on the single-premium shape; the target rider and the FX-driven dynamic surrender are
    single-premium options; and the 低解約返戻金特則 is a cliff released at 払込満了, so a 終身払
    contract gives it no release date.  Each is refused by name rather than given a
    silent default.
    """
    table = fx_whole_life.Data.model_point_table()
    saved = table.loc[point_id, column]
    table.loc[point_id, column] = value
    try:
        fx_whole_life.Projection[point_id].clear_all()
        with pytest.raises((FormulaError, ValueError)):
            getattr(fx_whole_life.Projection[point_id], cells)()
    finally:
        table.loc[point_id, column] = saved
        fx_whole_life.Projection[point_id].clear_all()


# ---------------------------------------------------------------------------
# Structural product facts: the horizon, the decrements and the shipped table


def test_the_horizon_is_the_tables_terminal_age_for_that_life(fx_whole_life):
    """``proj_len() = 12 (omega - x + 1)``, with omega read off the table, not hard-coded.

    A 終身 contract has no maturity date, so the horizon is the mortality table's own
    terminal age — 109 male and 113 female — and replacing the table moves the horizon
    with it.  The two sexes therefore project different lengths from the same issue age.
    """
    male = fx_whole_life.Projection[1]
    assert male.sex() == "M" and male.omega_age() == 109
    assert male.proj_len() == 12 * (109 - 40 + 1) == 840

    female = fx_whole_life.Projection[5]
    assert female.sex() == "F" and female.omega_age() == 113
    assert female.proj_len() == 12 * (113 - 55 + 1) == 708
    assert female.mort_rate(female.proj_len() - 1) == 1.0
    assert female.pols_if(female.proj_len()) == pytest.approx(0.0, abs=1e-12)


def test_a_whole_of_life_premium_term_runs_to_the_horizon(fx_whole_life):
    """``prem_months = 0`` denotes 終身払, which has no 払込満了 at all.

    ``prem_months_eff()`` resolves it against the projection horizon rather than leaving
    a zero to be read as "no premiums", and the premium is still due in the final month.
    """
    p = fx_whole_life.Projection[5]
    assert p.prem_months() == 0
    assert p.prem_months_eff() == p.proj_len()
    assert p.prem_due_pp(0) == 120.00
    assert p.prem_due_pp(p.proj_len() - 1) == 120.00
    assert p.premiums(p.proj_len() - 12) > 0.0   # the last month anyone is in force


def test_surrenders_are_taken_from_the_survivors_of_mortality(fx_whole_life):
    """The notes' processing order: death before surrender, in every month.

    ``S(t) = l(t)(1 - q_m)w_m``, not ``l(t) w_m``.  The two differ in the fourth decimal
    at these durations and by more at the far end, where the monthly decrement is large.
    """
    p = fx_whole_life.Projection[1]
    for t in (0, 1, 119, 400):
        expected = p.pols_if(t) * (1 - p.mort_rate_mth(t)) * p.lapse_rate_mth(t)
        assert p.pols_lapse(t) == pytest.approx(expected, abs=1e-12)
        assert p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_if(t) * (1 - p.mort_rate_mth(t)), abs=1e-12)
        assert p.pols_lapse(t) < p.pols_if(t) * p.lapse_rate_mth(t)


@pytest.mark.parametrize("point_id", POINT_IDS)
def test_the_in_force_roll_forward_closes_month_by_month(fx_whole_life, point_id):
    """``l(t) - l(t+1) = D(t) + S(t) + conv(t)`` in every month of every model point.

    The target conversion is the third and only other exit, so the identity collapses to
    the notes' two-decrement form wherever the rider is off — and where it is on, the
    converted policies have to appear here or the cohort silently loses mass.
    """
    p = fx_whole_life.Projection[point_id]
    for t in range(0, p.proj_len(), 7):
        out = p.pols_death(t) + p.pols_lapse(t) + p.pols_target(t)
        assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12)
    exits = sum(p.pols_death(t) + p.pols_lapse(t) + p.pols_target(t)
                for t in range(p.proj_len()))
    assert exits == pytest.approx(1.0, abs=1e-9)
    assert p.pols_if(p.proj_len()) == pytest.approx(0.0, abs=1e-12)


def test_the_new_business_strain_then_thin_margins(fx_whole_life):
    """The characteristic shape of the LEVEL contract, asserted rather than described.

    A deep strain in month 0 — upfront commission and acquisition expense against one
    monthly premium — then thin positive margins that thin further as the surrender
    benefit grows, and a negative tail after 払込満了 where claims and maintenance run on
    with no premium behind them.
    """
    p = fx_whole_life.Projection[1]
    assert p.net_cf(0) < -2_500.0
    assert all(p.net_cf(t) > 0.0 for t in (1, 2, 3, 119))
    assert p.net_cf(119) < p.net_cf(1)
    assert p.net_cf(240) < 0.0                   # the month after the last premium
    assert p.net_cf(p.proj_len() - 12) < 0.0     # the last month anyone is in force


def test_the_shipped_mortality_table_marks_its_own_provenance(fx_whole_life):
    """Every row says whether it is a sourced anchor or a [std] interpolation.

    生保標準生命表2018（死亡保険用）may be read and quoted but not redistributed, so what ships
    is a construction anchored to the individual rates the worked example quotes.  Marking
    each row is what stops the file being mistaken for the published table.
    """
    assert fx_whole_life.Data.input_dir() == MODEL_DIR.parent
    table = pd.read_csv(MODEL_DIR.parent / fx_whole_life.Data.mort_table_file)
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert set(table["sex"]) == {"M", "F"}
    assert table["age"].min() == 18
    assert table[table.sex == "M"]["age"].max() == 109
    assert table[table.sex == "F"]["age"].max() == 113
    male = table[table.sex == "M"].set_index("age")["mort_rate"]
    for age, rate in ((30, 0.00068), (40, 0.00118), (60, 0.00653), (90, 0.15760)):
        assert male.loc[age] == rate
    assert male.loc[109] == 1.00000
    female = table[table.sex == "F"].set_index("age")["mort_rate"]
    assert female.loc[30] == 0.00037 and female.loc[60] == 0.00363


def test_an_issue_age_the_shipped_table_cannot_serve_is_not_priced_silently(
        fx_whole_life):
    """The table starts at attained age 18, and a younger life raises on the lookup.

    The 契約年齢 envelope of the representative product reaches below that, so the shipped
    table does not serve the whole of it.  Raising is the honest behaviour: the alternative
    is a projection that looks complete and rests on a rate that was never published.
    """
    table = fx_whole_life.Data.model_point_table()
    saved = table.loc[1, "issue_age"]
    table.loc[1, "issue_age"] = 6
    try:
        fx_whole_life.Projection[1].clear_all()
        with pytest.raises((FormulaError, KeyError)):
            fx_whole_life.Projection[1].mort_rate(0)
    finally:
        table.loc[1, "issue_age"] = saved
        fx_whole_life.Projection[1].clear_all()


# ---------------------------------------------------------------------------
# The check cells the model publishes, and the shape of what it publishes


def test_the_five_check_cells_are_published_with_their_residuals(fx_whole_life):
    """These five identities, and no others, each with its per-month residual beside it.

    ``check_pols_roll_fwd`` closes the in-force roll-forward and the whole-run exits;
    ``check_av_roll_fwd`` the 積立金 recursion; ``check_cv_ledger`` the surrender benefit
    against ``CV(t+1)``; ``check_net_cf`` that no account-value charge leaks into the
    cash flow; ``check_fx_ledger`` the three-rate yen translation.

    That they *close*, on all eight model points, is asserted in
    ``test_model_conventions_jp.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library, so a second evaluation
    here meant a second cold projection to reach a verdict already reached. What generic
    discovery cannot say is which checks ought to exist — a check that disappears simply
    stops being discovered — so that is what is asserted here. The same sweep covers this
    model's frame: non-empty, spanning ``proj_len()``, indexed by ``t``, free of NaN and
    publishing one column vocabulary across all eight points.
    """
    checks = ("check_pols_roll_fwd", "check_av_roll_fwd", "check_cv_ledger",
              "check_net_cf", "check_fx_ledger")
    cells = set(fx_whole_life.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(checks)
    for check in checks:
        assert check + "_resid" in cells, check


def test_the_result_columns_are_the_notes_columns(fx_whole_life):
    """The published column vocabulary, in the notes' order."""
    assert list(fx_whole_life.Projection[1].result_cf().columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "conversions",
        "claim_expenses", "expenses", "commissions", "net_cf", "net_cf_jpy",
        "fx_spread_jpy", "av_pp", "cv_pp"]


def test_there_are_no_tail_states(fx_whole_life):
    """No maturity date, no 満期保険金, and nothing after the table's terminal age."""
    p = fx_whole_life.Projection[1]
    assert p.mort_rate(p.proj_len() - 1) == 1.0
    assert p.pols_if(p.proj_len()) == 0.0
    assert "claims_maturity" not in p.result_cf().columns
    assert p.claims(p.proj_len(), "DEATH") == 0.0


def test_the_terminal_policy_year_empties_in_its_first_month(fx_whole_life):
    """``q = 1`` at the terminal age is an *annual* rate, so the year ends in month one.

    ``q_m = 1 - (1 - 1)^(1/12) = 1``, so every survivor of month ``12(omega - x)`` dies in
    that month and the remaining eleven rows of the terminal policy year are structurally
    empty.  They are carried rather than trimmed because the horizon is stated as
    ``12 (omega - x + 1)`` months; a reader comparing the two must not read the zeros as
    lost lives, and the roll-forward closes at the earlier month.
    """
    for pid in (1, 5, 8):
        p = fx_whole_life.Projection[pid]
        last = p.proj_len() - 12
        assert p.age(last) == p.omega_age()
        assert p.mort_rate(last) == 1.0
        assert p.mort_rate_mth(last) == 1.0
        assert p.pols_if(last) > 0.0
        assert p.pols_if(last + 1) == pytest.approx(0.0, abs=1e-15)
        assert all(p.net_cf(t) == 0.0 for t in range(last + 1, p.proj_len()))
        assert p.check_pols_roll_fwd() is True


# ---------------------------------------------------------------------------
# The external-input bargain, both halves of it


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is what the external-file layout buys, and it is what a user with a real
    算出方法書 does: the back-solved charge stack drops out and the company's own rates drop
    in as a same-schema CSV, with no formula change.  Doubling the 維持費率 here must move
    the 積立金 and nothing about the model's structure.
    """
    src = MODEL_DIR.parent / "charge_table.csv"
    doubled = pd.read_csv(src, index_col=["shape", "item"])
    doubled.loc[("LEVEL", "maint_rate"), "value"] *= 2.0

    model = mx.read_model(MODEL_DIR, name="FXWholeLife_JP_S_swap")
    try:
        alt = "charge_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt)
        try:
            base_maint = model.Projection[1].maint_rate()
            base_av = model.Projection[1].av_pp(120)
            model.Data.charge_table_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].maint_rate() == pytest.approx(
                2 * base_maint, rel=1e-12)
            assert model.Projection[1].av_pp(120) < base_av
            assert model.Projection[1].check_av_roll_fwd() is True
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_reproduces_the_worked_example(tmp_path):
    """read -> write -> re-read reproduces the goldens, inputs travelling alongside.

    Inputs are external, so they must be copied to the new parent before the re-read: the
    model alone reads fine and then fails on first evaluation.  That is the trade-off the
    layout makes, and it is worth asserting in both directions.
    """
    import shutil

    model = mx.read_model(MODEL_DIR, name="FXWholeLife_JP_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="FXWholeLife_JP_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, lines in TRACE.items():
            actual = trace_actual(anchor, t)
            for line, printed in lines.items():
                assert actual[line] == pytest.approx(
                    float(printed), abs=displayed_tolerance(printed)), (t, line)
        for t, row in FIRST_PERIODS.items():
            assert anchor.result_cf().loc[t, "net_cf"] == pytest.approx(row[7], abs=5e-5)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()
