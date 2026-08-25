"""Product tests for ``Cancer_JP_S``, the がん保険 reference model.

The house-style contract is asserted once, for every model in the library, in
``test_model_conventions_jp.py``. What is asserted here is this product: the worked
example of ``products/cancer/technical-notes.md`` **hard-coded** so that a reviewer can
check it against the notes by eye, every one of the notes' *Known modeling pitfalls* —
each pitfall being a way an implementation can look right and be wrong — the seven
roll-forward and ledger identities on every shipped model point, each optional module in
both positions, and the structural product facts this product turns on.

The anchor cell is male, 契約年齢 40 (満年齢), 終身 chassis, 終身払, 基本給付金額 ¥10,000;
がん診断一時金 ¥1,000,000 on a 24-month repeat cycle with no lifetime cap; 上皮内新生物 at 50% of
that, once; がん入院給付金日額 ¥10,000 with **no day limit**; がん手術給付金 ¥200,000; がん治療給付金
¥100,000 per qualifying month capped at 60 months; がん通院給付金日額 ¥10,000; 先進医療特約
attached; 保険料払込免除 on the first 悪性新生物 diagnosis; office premium ¥3,000 a month; a 90-day
waiting period that is three months of the grid. Every row of the worked example sits at
age 40 in policy year 1, so one set of rates drives all of them.

Two things about this product shape almost every test below. Premiums ride on the
**never-diagnosed** sub-population and claims on the **diagnosed** one, because the waiver
fires on the same event that starts every benefit; and the model carries **three states**
rather than one, because the repeating diagnosis benefit, the unlimited-day inpatient
benefit and the monthly treatment benefit are all integrals over post-diagnosis survival.

Tolerances follow the precision the notes display: money to ¥0.01, ``pols_if`` and the
healthy/diagnosed split to six decimals, the diagnosed state to eight, the ledgers to
four.
"""
import math
from contextlib import contextmanager

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from jp_registry import model_path

MODEL_DIR = model_path("Cancer_JP_S")

YEN = 5e-3           # money displayed to 0.01
INFORCE = 5e-7       # pols_if and the healthy split, 6 d.p.
DIAGNOSED = 5e-9     # the diagnosed state, 8 d.p.
LEDGER = 5e-5        # the treatment-month ledger, 4 d.p.

CARE_KINDS = ("DIAG", "INSITU", "HOSP", "SURGERY", "TREAT", "OUTPATIENT", "ADVANCED")


@contextmanager
def switched(name, **refs):
    """A private copy of the model with one or more References moved off their base value.

    ``Projection.clear_all()`` discards the ItemSpaces along with their caches, so the
    ItemSpace is re-fetched after the change rather than held across it.
    """
    model = mx.read_model(MODEL_DIR, name=name)
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        model.Projection.clear_all()
        yield model
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The worked example, hard-coded to the precision the notes display


# t: pols_if, pols_healthy, pols_cancer, premiums, expenses, claim_expenses, commissions
#
# ``expenses`` is acquisition plus maintenance and ``claim_expenses`` the claim handling
# cost, in two columns rather than one -- the library-wide split.  The notes' month traces
# narrate the two in one arithmetic line and their sum is asserted below alongside them.
WORKED_EXAMPLE_STATE = {
    0: (1.000000, 1.000000, 0.00000000, 3000.00, 20250.00, 0.0000, 54000.00),
    1: (0.992093, 0.992093, 0.00000000, 2976.28,   248.02, 0.0000,     0.00),
    2: (0.984249, 0.984249, 0.00000000, 2952.75,   246.06, 0.0000,     0.00),
    3: (0.976466, 0.976466, 0.00000000, 2929.40,   244.12, 0.6733,     0.00),
    4: (0.968745, 0.968626, 0.00011909, 2905.88,   242.19, 0.6753,     0.00),
    5: (0.961085, 0.960849, 0.00023631, 2882.55,   240.27, 0.6773,     0.00),
}

# t: claims_diag, claims_insitu, claims_hosp, claims_surgery, claims_treat,
#    claims_outpatient, claims_advanced, the claims(t) total, net_cf.
# The total is the ``claims(t)`` cells; ``result_cf`` publishes the splits and no
# subtotal column beside them, so it is asserted off the cells and not off the table.
WORKED_EXAMPLE_CLAIMS = {
    0: (0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,   0.00, -71250.00),
    1: (0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,   0.00,   2728.26),
    2: (0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,   0.00,   2706.68),
    3: (120.02, 7.32, 0.00, 2.34, 0.00, 0.00, 0.00, 129.68, 2554.93),
    4: (119.05, 7.26, 0.36, 2.50, 1.19, 0.11, 0.08, 130.55, 2532.47),
    5: (118.10, 7.20, 0.71, 2.65, 2.36, 0.22, 0.16, 131.39, 2510.20),
}

# The notes' policy-year-1 aggregates, t = 0..11, displayed to four decimals.
POLICY_YEAR_1 = {
    "premiums": 34462.5629,
    "claims_diag": 1046.0977,
    "claims_insitu": 63.8082,
    "claims_hosp": 12.3980,
    "claims_surgery": 26.4454,
    "claims_treat": 41.3265,
    "claims_outpatient": 3.7883,
    "claims_advanced": 2.7275,
    "expenses": 22872.9134,
    "claim_expenses": 6.1269,
    "commissions": 54000.0000,
    "net_cf": -43613.0689,
}

# The benefit total over the same twelve months. It is a constant of its own rather than
# a row of POLICY_YEAR_1 because ``result_cf`` publishes no ``claims`` column: a cash flow
# statement must not carry its own subtotal beside its parts.
POLICY_YEAR_1_CLAIMS = 1196.5915

# The five care benefits are fixed yen amounts per diagnosed life-month at the anchor
# cell's parameters, and the notes call the five numbers worth memorising.
PER_DIAGNOSED_LIFE_MONTH = {
    "HOSP": 3000.00,
    "SURGERY": 1458.33,
    "TREAT": 10000.00,
    "OUTPATIENT": 916.67,
    "ADVANCED": 660.00,
}
PER_DIAGNOSED_LIFE_MONTH_TOTAL = 16035.00


def test_the_anchor_cell_is_the_worked_examples_model_point(jp_cancer_anchor):
    """Model point 1 is the cell the notes' worked example projects."""
    p = jp_cancer_anchor
    assert p.issue_age() == 40
    assert p.sex() == "M"
    assert p.chassis() == "shushin"
    assert p.base_amount() == 10_000.0
    assert p.diag_benefit() == 1_000_000.0
    assert p.cycle_months() == 24
    assert p.insitu_pct() == 0.50
    assert p.daily_amount() == 10_000.0
    assert p.surg_mult() == 20.0
    assert p.treat_benefit() == 100_000.0
    assert p.treat_cap() == 60
    assert p.outp_daily() == 10_000.0
    assert p.wait_months() == 3
    assert p.prem_period_type() == "whole_life"
    assert p.premium_mth_pp() == 3_000.0
    assert p.waiver_trigger() == "cancer_diag"
    assert p.adv_rider() is True
    assert p.disch_rider() is False
    assert p.repeat_conditioned() is False
    assert p.proj_len() == 924            # 12 x (116 - 40 + 1), the male terminal age


def test_the_worked_examples_assumption_values(jp_cancer_anchor):
    """Every rate the notes quote for the worked example, to the digits they show.

    The incidence limb is the one genuinely sourced assumption in the model; the sex
    split, the survival basis, the relapse hazard and the care frequencies are all
    **[std]**, and each is pinned here at the value the notes publish.
    """
    p = jp_cancer_anchor
    assert p.inc_rate_both(0) == pytest.approx(220.28 / 100_000, rel=1e-14)
    assert p.sex_factor(42.5) == pytest.approx(0.669559, abs=5e-7)
    assert p.inc_rate(0) == pytest.approx(0.00147490, abs=5e-9)
    assert p.inc_rate_mth(0) == pytest.approx(0.000122909, abs=5e-10)
    assert p.insitu_rate_mth(0) == pytest.approx(0.0000149949, abs=5e-11)
    assert p.mort_rate_at_age(40) == 0.00076          # 第三分野標準生命表2018 男 q(40)
    assert p.mort_rate(0) == pytest.approx(0.00095, abs=5e-9)
    assert p.mort_rate_mth(0) == pytest.approx(0.0000792012, abs=5e-11)
    assert p.surv_5y() == 0.6317                     # 5年相対生存率, male, all sites
    assert p.mu_ex() == pytest.approx(0.0918681, abs=5e-8)
    assert p.mort_rate_canc_mth(0) == pytest.approx(0.0077050451, abs=5e-11)
    assert p.lapse_rate(0) == 0.09
    assert p.lapse_rate_mth(0) == pytest.approx(0.0078284203, abs=5e-11)
    assert p.lapse_rate_canc_mth(0) == 0.0           # a waived life cannot lapse
    assert p.relapse_rate_mth(0) == 0.005
    assert p.hosp_stay_days(0) == 14.4
    assert p.hosp_rate_mth(0) == pytest.approx(0.25 / 12, rel=1e-14)
    assert p.adv_freq_mth() == pytest.approx(0.012 / 12, rel=1e-14)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_STATE))
def test_the_worked_examples_in_force_and_non_claim_lines(jp_cancer_anchor, t):
    """The notes' first six-row table: the state split and the three non-claim lines.

    ``pols_healthy`` and ``pols_cancer`` are published beside ``pols_if`` because the
    premium rides on the first and the five care benefits on the second, and the table is
    where that asymmetry becomes visible.
    """
    p = jp_cancer_anchor
    pols_if, healthy, cancer, prem, exp, claim_exp, comm = WORKED_EXAMPLE_STATE[t]
    assert p.pols_if(t) == pytest.approx(pols_if, abs=INFORCE)
    assert p.pols_healthy(t) == pytest.approx(healthy, abs=INFORCE)
    assert p.pols_cancer(t) == pytest.approx(cancer, abs=DIAGNOSED)
    assert p.premiums(t) == pytest.approx(prem, abs=YEN)
    assert p.expenses(t) == pytest.approx(exp, abs=YEN)
    assert p.claim_expenses(t) == pytest.approx(claim_exp, abs=5e-5)
    assert p.commissions(t) == pytest.approx(comm, abs=YEN)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CLAIMS))
def test_the_worked_examples_claim_lines(jp_cancer_anchor, t):
    """The notes' second six-row table: seven claim lines, their total and ``net_cf``."""
    p = jp_cancer_anchor
    row = WORKED_EXAMPLE_CLAIMS[t]
    for kind, expected in zip(CARE_KINDS, row):
        assert p.claims(t, kind) == pytest.approx(expected, abs=YEN), kind
    assert p.claims(t) == pytest.approx(row[7], abs=YEN)
    assert p.net_cf(t) == pytest.approx(row[8], abs=YEN)


def test_the_worked_examples_month_0_trace(jp_cancer_anchor):
    """The notes' month-0 trace: premium collected, every cancer term a hard zero.

    ``expenses(0)`` is the ¥250 maintenance plus the ¥20,000 acquisition expense and
    nothing else — there is no claim expense because there are no claim events — and the
    initial commission is 1.5 x the annualized premium.
    """
    p = jp_cancer_anchor
    assert p.pols_healthy(0) == 1.0
    assert p.pols_cancer(0) == 0.0
    assert p.premiums(0) == pytest.approx(3_000.0 * 1.0, abs=YEN)
    assert p.cover(0) == 0.0
    assert p.claims(0) == 0.0
    assert p.claim_expenses(0) == 0.0
    assert p.expenses(0) == pytest.approx(250.0 + 20_000.0, abs=YEN)
    assert p.commissions(0) == pytest.approx(1.5 * 36_000.0, abs=YEN)
    assert p.net_cf(0) == pytest.approx(
        3_000.0 - 20_250.0 - 0.0 - 54_000.0, abs=YEN)
    assert p.pols_healthy(1) == pytest.approx(
        1.0 * (1 - 0.0000792012) * (1 - 0.0078284203), abs=INFORCE)
    assert p.pols_cancer(1) == 0.0
    assert p.insitu_avail(1) == 1.0        # the in-situ ledger cannot move before t = 3


def test_the_worked_examples_month_1_and_2_traces(jp_cancer_anchor):
    """Month 2 is month 1 scaled again: the same rates on a smaller healthy population."""
    p = jp_cancer_anchor
    assert p.premiums(1) == pytest.approx(2976.2790, abs=5e-5)
    assert p.expenses(1) == pytest.approx(248.0232, abs=5e-5)
    assert p.commissions(1) == 0.0                  # renewal commission starts at t = 12
    assert p.claim_expenses(1) == 0.0
    assert p.net_cf(1) == pytest.approx(2976.2790 - 248.0232, abs=YEN)
    assert p.pols_healthy(2) == pytest.approx(0.992093 * 0.992093, abs=INFORCE)
    assert p.premiums(2) == pytest.approx(2952.7456, abs=5e-5)
    assert p.expenses(2) == pytest.approx(246.0621, abs=5e-5)
    assert p.pols_healthy(3) == pytest.approx(0.976466, abs=INFORCE)


def test_the_worked_examples_month_3_trace_when_cover_attaches(jp_cancer_anchor):
    """The notes' month-3 trace: the first claims, from a still-empty diagnosed state.

    Every surgery yen in month 3 is in-situ surgery, because ``pols_cancer(3)`` is zero —
    an in-situ diagnosis pays the reduced lump sum and the surgery benefit in the month it
    arises, and nothing continuing.
    """
    p = jp_cancer_anchor
    assert p.cover(3) == 1.0
    assert p.diag_first(3) == pytest.approx(0.000120016, abs=5e-10)
    assert p.claims(3, "DIAG") == pytest.approx(120.0161, abs=5e-5)
    assert p.insitu_ev(3) == pytest.approx(0.0000146420, abs=5e-11)
    assert p.claims(3, "INSITU") == pytest.approx(7.3210, abs=5e-5)
    assert p.claims(3, "SURGERY") == pytest.approx(2.3427, abs=5e-5)
    assert p.pols_cancer(3) == 0.0
    for kind in ("HOSP", "TREAT", "OUTPATIENT", "ADVANCED"):
        assert p.claims(3, kind) == 0.0, kind
    assert p.claims(3) == pytest.approx(120.0161 + 7.3210 + 2.3427, abs=5e-4)
    assert p.expenses(3) == pytest.approx(244.1165, abs=5e-4)
    assert p.claim_expenses(3) == pytest.approx(0.6733, abs=5e-5)
    assert p.pols_healthy(4) == pytest.approx(
        (0.976466 - 0.000120016) * 0.992093, abs=INFORCE)
    assert p.pols_locked(4) == pytest.approx(0.000119091, abs=5e-9)
    assert p.unlock(4) == 0.0                       # t + 1 < C, nothing can have unlocked
    assert p.insitu_avail(4) == pytest.approx(0.999985, abs=5e-7)


def test_the_worked_examples_month_4_trace_when_the_diagnosed_state_is_live(
        jp_cancer_anchor):
    """The notes' month-4 trace: the five care benefits are ``pols_cancer`` times a rate.

    ``premiums(4)`` is ``pols_healthy``, not ``pols_if``: the 0.000119 of diagnosed lives
    pay nothing. The maintenance expense is on ``pols_if``, because a waived policy is
    still serviced.
    """
    p = jp_cancer_anchor
    assert p.pols_cancer(4) == pytest.approx(0.00011909, abs=DIAGNOSED)
    assert p.claims(4, "HOSP") == pytest.approx(0.3573, abs=5e-5)
    assert p.claims(4, "TREAT") == pytest.approx(1.1909, abs=5e-5)
    assert p.paid_months(4) == 0.10                 # M(4) = 0, so the cap does not bite
    assert p.claims(4, "OUTPATIENT") == pytest.approx(0.1092, abs=5e-5)
    assert p.claims(4, "ADVANCED") == pytest.approx(0.0786, abs=5e-5)
    assert p.insitu_ev(4) == pytest.approx(0.0000145242, abs=5e-11)
    assert p.claims(4, "SURGERY") == pytest.approx(2.4975, abs=5e-5)
    assert p.diag_first(4) == pytest.approx(0.000119053, abs=5e-10)
    assert p.claims(4, "DIAG") == pytest.approx(119.0525, abs=5e-5)
    assert p.diag_rep(4) == 0.0                     # pols_open(4) is still empty
    assert p.claims(4) == pytest.approx(130.5481, abs=5e-4)
    assert p.premiums(4) == pytest.approx(3_000.0 * 0.968626, abs=5e-3)
    assert p.premiums(4) < 3_000.0 * p.pols_if(4)
    assert p.expenses(4) == pytest.approx(242.1863, abs=5e-4)
    assert p.claim_expenses(4) == pytest.approx(0.6679 + 0.0074, abs=5e-5)
    assert p.net_cf(4) == pytest.approx(
        2905.8782 - 130.5481 - 242.1863 - 0.6753, abs=YEN)


def test_policy_year_1_in_aggregate(jp_cancer_anchor):
    """The notes' strongest single test target: twelve months on one set of rates.

    It exercises the waiting-period boundary and the first months of the diagnosed state
    together, and the totals are sums of **unrounded** monthly values.
    """
    p = jp_cancer_anchor
    df = p.result_cf().head(12)
    for column, total in POLICY_YEAR_1.items():
        assert df[column].sum() == pytest.approx(total, abs=5e-5), column
    ts = range(12)
    assert sum(p.claims(t) for t in ts) == pytest.approx(
        POLICY_YEAR_1_CLAIMS, abs=5e-5)
    assert sum(p.pols_if(t) for t in ts) == pytest.approx(11.491654, abs=INFORCE)
    assert sum(p.pols_healthy(t) for t in ts) == pytest.approx(11.487521, abs=INFORCE)
    assert sum(p.pols_cancer(t) for t in ts) == pytest.approx(0.004133, abs=INFORCE)
    assert p.pols_if(12) == pytest.approx(0.909137, abs=INFORCE)
    assert p.pols_healthy(12) == pytest.approx(0.908130, abs=INFORCE)
    assert p.pols_cancer(12) == pytest.approx(0.001006, abs=INFORCE)
    assert p.treat_months(12) == pytest.approx(0.4002, abs=LEDGER)
    assert p.adv_paid(12) == pytest.approx(2401.31, abs=YEN)
    assert p.insitu_avail(12) == pytest.approx(0.999865, abs=INFORCE)


def test_the_benefit_per_diagnosed_life_month(jp_cancer_anchor):
    """The notes' five memorable numbers, summing to ¥16,035.00 per diagnosed life-month.

    The five care benefits are ``pols_cancer(t)`` times a fixed yen amount at the anchor
    cell's parameters, so the whole of the diagnosed-state liability is that one figure
    integrated over post-diagnosis survival. The surgery line is the only one that needs
    care: its **second** limb is the surgeries recognised in the month of an in-situ
    diagnosis, and those do not sit on the diagnosed state at all.
    """
    p = jp_cancer_anchor
    t = 200
    assert p.pols_cancer(t) > 0.0
    insitu_surgery = p.surg_mult() * p.base_amount() * 0.80 * p.insitu_ev(t)
    on_state = {
        "HOSP": p.claims(t, "HOSP"),
        "SURGERY": p.claims(t, "SURGERY") - insitu_surgery,
        "TREAT": p.claims(t, "TREAT"),
        "OUTPATIENT": p.claims(t, "OUTPATIENT"),
        "ADVANCED": p.claims(t, "ADVANCED"),
    }
    total = 0.0
    for kind, per_month in PER_DIAGNOSED_LIFE_MONTH.items():
        assert on_state[kind] / p.pols_cancer(t) == pytest.approx(
            per_month, abs=YEN), kind
        total += per_month
    assert total == pytest.approx(PER_DIAGNOSED_LIFE_MONTH_TOTAL, abs=YEN)
    assert sum(on_state.values()) / p.pols_cancer(t) == pytest.approx(
        PER_DIAGNOSED_LIFE_MONTH_TOTAL, abs=YEN)
    assert insitu_surgery > 0.0
    # The inpatient limb is the sourced 14.4-day mean stay at the [std] admission rate.
    assert p.daily_amount() * p.hosp_stay_days(t) * p.hosp_rate_mth(t) == pytest.approx(
        3000.0, abs=YEN)
    # The admission rate's own derivation, on two sourced counts in which the population
    # cancels: 2.707020 admissions per diagnosed person over a cancer lifetime, 38.98
    # inpatient days at 14.4 each, and 0.250293 a year over the 10.815-year mean
    # diagnosed-state duration — rounded to the shipped 0.25 [std].
    admissions = (106_100 * 365 / 14.4) / 993_469
    duration_years = 1.0 / (12.0 * p.mort_rate_canc_mth(0))
    assert admissions == pytest.approx(2.707020, abs=5e-7)
    assert admissions * 14.4 == pytest.approx(38.98, abs=0.01)
    assert duration_years == pytest.approx(10.815, abs=5e-4)
    assert admissions / duration_years == pytest.approx(0.250293, abs=5e-7)
    assert round(admissions / duration_years, 2) == 12 * p.hosp_rate_mth(t)


def test_the_relapse_hazards_calibration_target(jp_cancer_anchor):
    """1.485593 diagnosis payments per diagnosed life, the notes' stated calibration.

    The target is quoted at the anchor cell's decrement rates **held flat**, so it is an
    arithmetic property of ``relapse_rate_mth`` and ``mort_rate_canc_mth`` rather than of
    the projection, and it is asserted as such. The per-cycle probability and the expected
    count are different numbers and the notes read them apart: 32.7% of diagnosed lives
    collect at least a second lump sum and 10.7% at least a third, and it is the lives paid
    three and more times that lift the expected count to 0.4856.
    """
    p = jp_cancer_anchor
    r, q_c = p.relapse_rate_mth(0), p.mort_rate_canc_mth(0)
    survive_lock = (1.0 - q_c) ** p.cycle_months()
    race = r / (r + q_c)
    per_cycle = survive_lock * race
    assert survive_lock == pytest.approx(0.830575, abs=5e-7)
    assert race == pytest.approx(0.393544, abs=5e-7)
    assert per_cycle == pytest.approx(0.326868, abs=5e-7)
    assert per_cycle ** 2 == pytest.approx(0.106843, abs=5e-7)
    assert per_cycle / (1.0 - per_cycle) == pytest.approx(0.485593, abs=5e-7)
    # The expected count exceeds the proportion paid twice; they are not the same number.
    assert per_cycle / (1.0 - per_cycle) > per_cycle


# ---------------------------------------------------------------------------
# The notes' known modeling pitfalls, one test each


def test_the_waiting_period_is_a_hard_zero_not_a_reduced_rate(jp_cancer_anchor):
    """No cancer benefit of any kind in months 0, 1 and 2, and nobody transitions.

    A model that starts the incidence at ``t = 0`` pays three months of benefit that no
    contract in the retrieved set pays. ``cover(t)`` multiplies every benefit, the
    incidence transition and the in-situ transition alike, so the diagnosed state and the
    in-situ ledger are both still untouched when cover attaches.
    """
    p = jp_cancer_anchor
    for t in (0, 1, 2):
        assert p.cover(t) == 0.0
        assert p.claims(t) == 0.0
        assert all(p.claims(t, kind) == 0.0 for kind in CARE_KINDS)
        assert p.diag_first(t) == 0.0
        assert p.insitu_ev(t) == 0.0
        assert p.pols_cancer(t) == 0.0
        assert p.insitu_avail(t) == 1.0
    assert p.cover(3) == 1.0
    assert p.claims(3) > 0.0
    assert p.pols_healthy(3) == pytest.approx(p.pols_if(3), rel=1e-15)


def test_the_premium_is_still_charged_during_the_waiting_period(jp_cancer_anchor):
    """Cover is suppressed and the premium is not: suppressing both is another product.

    Five of the six carriers that state it charge from inception, and the one that does
    not says explicitly that its three free months are not a discount.
    """
    p = jp_cancer_anchor
    for t in (0, 1, 2):
        assert p.premiums(t) == pytest.approx(3_000.0 * p.pols_healthy(t), rel=1e-14)
        assert p.premiums(t) > 0.0
        assert p.net_cf(t) > 0.0 or t == 0        # only the outset strain is negative
    assert sum(p.premiums(t) for t in range(3)) == pytest.approx(8929.02, abs=YEN)


def test_an_in_window_diagnosis_voids_the_contract_it_does_not_lapse_it(jp_cancer_anchor):
    """A de-recognition at outset, not a decrement — and the base run omits it, stated.

    Putting an in-window diagnosis in the lapse column keeps premium income the insurer
    never earned. The switch scales the initial exposure instead, which releases the
    premium already collected together with the future benefit; the acquisition expense
    and the initial commission are deliberately not scaled, because they were incurred.
    """
    p = jp_cancer_anchor
    assert p.void_prob() == 0.0                   # off in the base run
    assert p.pols_if_init() == 1.0
    with switched("Cancer_JP_S_void", void_adjust=True) as model:
        q = model.Projection[1]
        assert q.void_prob() == pytest.approx(0.000368681, abs=5e-10)
        assert q.void_prob() == pytest.approx(
            1.0 - (1.0 - q.inc_rate_mth(0)) ** q.wait_months(), rel=1e-14)
        assert round(q.void_prob() * 100, 3) == 0.037          # 0.037% of policies
        assert q.pols_if_init() == pytest.approx(1.0 - q.void_prob(), rel=1e-15)
        assert q.premiums(0) == pytest.approx(3_000.0 * q.pols_if_init(), rel=1e-14)
        # The acquisition expense and the initial commission ride through unscaled.
        assert q.expenses(0) == pytest.approx(
            20_000.0 + 250.0 * q.pols_if_init(), abs=1e-9)
        assert q.claim_expenses(0) == 0.0
        assert q.commissions(0) == 54_000.0
        assert q.pols_lapse(0) == pytest.approx(
            p.pols_lapse(0) * q.pols_if_init(), rel=1e-12)        # scaled, not loaded


def test_insitu_is_a_second_benefit_tier_not_a_discount_on_the_first(jp_cancer_anchor):
    """Own once-only cap, no state change, no cycle, no waiver.

    Implementing it as ``insitu_pct x claims_diag`` inside the main diagnosis benefit gets
    the amount right and the cap, the cycle and the waiver all wrong. It attaches to
    ``pols_healthy`` alone, carries its own ledger, and the life that collects it goes on
    paying premium and stays eligible for the full-rate benefit.
    """
    p = jp_cancer_anchor
    t = 3
    assert p.claims(t, "INSITU") == pytest.approx(
        p.insitu_pct() * p.diag_benefit() * p.insitu_ev(t), rel=1e-14)
    # Not a share of the main line: the two are driven by different event counts.
    assert p.claims(t, "INSITU") != pytest.approx(
        p.insitu_pct() * p.claims(t, "DIAG"), rel=1e-6)
    # Its own ledger, which the diagnosis benefit does not touch.
    assert p.insitu_avail(t) == 1.0
    assert p.insitu_avail(t + 1) == pytest.approx(
        1.0 - p.insitu_rate_mth(t), rel=1e-14)
    # No state change: the diagnosed state is built from diag_first alone.
    assert p.pols_cancer(t + 1) == pytest.approx(
        p.diag_first(t) * p.surv_canc(t), rel=1e-14)
    assert p.insitu_ev(t) > 0.0
    # No cycle: an in-situ event is not a payment trigger.
    assert p.trig(t) == pytest.approx(p.diag_first(t), rel=1e-15)
    # No waiver: the premium base is pols_healthy, which in-situ does not reduce.
    assert p.pols_payer(t + 1) == pytest.approx(p.pols_healthy(t + 1), rel=1e-15)


def test_premiums_are_weighted_by_pols_healthy_and_claims_by_pols_cancer(cancer):
    """The single largest arithmetic error available in this product, asserted away.

    The waiver fires on the same first invasive diagnosis that starts every benefit, so
    the two weights are disjoint. Weighting the premium by ``pols_if`` overstates lifetime
    income by exactly the waived population — 6.1% on the anchor cell — and it is
    invisible in the first three months, because there the two are equal.
    """
    p = cancer.Projection[1]
    ts = range(p.proj_len())
    for t in (0, 1, 2):
        assert p.pols_healthy(t) == p.pols_if(t)
    for t in (4, 120, 600):
        assert p.premiums(t) == pytest.approx(3_000.0 * p.pols_healthy(t), rel=1e-14)
        assert p.premiums(t) < 3_000.0 * p.pols_if(t)
    on_healthy = sum(p.premiums(t) for t in ts)
    on_if = sum(p.premium_mth_pp() * p.pols_if(t) for t in ts)
    assert on_if / on_healthy - 1.0 == pytest.approx(0.0614, abs=0.002)
    # And the claims side of the asymmetry: the care benefits ride on pols_cancer alone.
    t = 200
    assert p.claims(t, "HOSP") == pytest.approx(
        p.daily_amount() * p.hosp_stay_days(t) * p.hosp_rate_mth(t) * p.pols_cancer(t),
        rel=1e-14)


def test_a_diagnosed_life_cannot_lapse(cancer):
    """No premium to miss and no surrender value to take, so lapse is a healthy-only exit.

    Applying the healthy lapse rate to the diagnosed state deletes exactly the claimants
    the product exists to pay. The rate is not hard-coded to zero: on the no-waiver design
    the premium does not stop and the diagnosed can lapse, which is model point 7.
    """
    p = cancer.Projection[1]
    for t in (0, 100, 600):
        assert p.lapse_rate_canc_mth(t) == 0.0
        assert p.surv_canc(t) == pytest.approx(1.0 - p.mort_rate_canc_mth(t), rel=1e-15)
        assert p.pols_lapse(t) == pytest.approx(
            (p.pols_healthy(t) - p.diag_first(t)) * (1.0 - p.mort_rate_mth(t))
            * p.lapse_rate_mth(t), rel=1e-14)
    p7 = cancer.Projection[7]
    assert p7.waiver_trigger() == "none"
    assert p7.lapse_rate_canc_mth(200) > 0.0


def test_there_is_no_l1_no_la_and_no_benefit_driven_termination(cancer):
    """No per-hospitalization day ledger, no 通算 lifetime day ledger, no exhaustion.

    Inheriting the medical chassis's 60/120-day per-hospitalization cap or its 1,095-day
    aggregate caps a benefit every source says is uncapped, and the termination they
    create ends a contract that cannot exhaust. The inpatient benefit's coefficient is the
    same in month 10 and in month 900.
    """
    p = cancer.Projection[1]
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    for absent in ("l1", "la", "day_limit", "days_limit", "days_per_hosp",
                   "hosp_days_ledger", "tsusan_days", "pols_exhaust", "pols_term"):
        assert absent not in names, f"{absent} is medical-chassis day-ledger machinery"
    assert not [n for n in names if "limit" in n or "exhaust" in n]
    for t in (10, 400, 900):
        assert p.pols_cancer(t) > 0.0
        assert p.claims(t, "HOSP") / p.pols_cancer(t) == pytest.approx(3000.0, abs=YEN)
    # The roll-forward has only two ways out, and a payment is not one of them.
    for t in (3, 200, 700):
        assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(
            p.pols_death(t) + p.pols_lapse(t), abs=1e-14)
        assert p.trig(t) > 0.0


def test_the_two_year_cycle_is_not_the_180_day_one_hospitalization_rule(cancer):
    """Different length, different trigger, different consequence.

    The medical chassis's clock groups admissions within 180 days into one hospitalization
    and is keyed to a discharge; this one measures 24 months from a payment trigger and
    governs eligibility. Sharing one clock between the two products breaks both.
    """
    p = cancer.Projection[1]
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    assert p.cycle_months() == 24
    assert not [n for n in names if "180" in n or "one_hosp" in n or "hosp_group" in n]
    # Eligibility, not grouping: the first unlock is C months after the first trigger,
    # which cannot arise before the waiting period ends.
    first_trigger = p.wait_months()
    assert p.trig(first_trigger) > 0.0
    assert all(p.unlock(t) == 0.0 for t in range(first_trigger + p.cycle_months()))
    assert p.unlock(first_trigger + p.cycle_months()) > 0.0
    assert p.pols_open(first_trigger + p.cycle_months()) > 0.0
    assert p.diag_rep(first_trigger + p.cycle_months()) > 0.0


def test_the_cycle_clock_runs_from_the_previous_trigger(cancer):
    """``unlock`` reads the trigger history, first diagnoses **and** repeats.

    Reading it off ``diag_first`` alone would restart the clock only for lives being paid
    for the first time, so every repeat payment would silently never lock. The two differ
    from the first month in which a repeat can arise.
    """
    p = cancer.Projection[1]
    c = p.cycle_months()
    t = p.wait_months() + 2 * c                # the first month whose cohort has repeats
    factor = 1.0
    for v in range(t - c, t):
        factor *= p.surv_canc(v)
    assert p.diag_rep(t - c) > 0.0
    assert p.unlock(t) == pytest.approx(p.trig(t - c) * factor, rel=1e-12)
    assert p.unlock(t) > p.diag_first(t - c) * factor
    assert p.check_cycle_ledger() is True


def test_the_treatment_benefits_unit_is_a_month_not_a_day_and_not_an_event(cancer):
    """``B_tr x paid_months x pols_cancer``: no day count reaches it, by construction.

    The medical chassis's benefit is 日額 x days and this one is 月額 x months; the two have
    different dimensions and cannot share a formula. Changing the **mean stay in days** —
    the one input a day-count formula would pick up — moves the inpatient benefit and
    leaves the treatment benefit untouched.
    """
    p = cancer.Projection[1]
    t = 200
    assert p.claims(t, "TREAT") == pytest.approx(
        p.treat_benefit() * p.paid_months(t) * p.pols_cancer(t), rel=1e-14)
    assert p.paid_months(t) <= 1.0             # an indicator per month, not a count
    with switched("Cancer_JP_S_days", hosp_age_gradient=True) as model:
        q = model.Projection[1]
        assert q.hosp_stay_days(t) != p.hosp_stay_days(t)
        assert q.claims(t, "HOSP") != pytest.approx(p.claims(t, "HOSP"), rel=1e-6)
        assert q.claims(t, "TREAT") == pytest.approx(p.claims(t, "TREAT"), rel=1e-12)


def test_the_60_month_cap_is_a_ledger_on_months_per_diagnosed_life(cancer):
    """Diluted by ``diag_first`` alone, because a repeat trigger is an already-diagnosed life.

    Weighting the ledger by ``pols_cancer`` would measure the block's consumption rather
    than the individual's and defer the cap forever; diluting it with ``diag_rep`` as well
    would reset a ledger that should keep running.
    """
    p = cancer.Projection[1]
    t = 100
    entering = p.pols_cancer(t) + p.diag_first(t)
    assert p.diag_rep(t) > 0.0
    assert p.treat_months(t + 1) == pytest.approx(
        (p.treat_months(t) + p.paid_months(t)) * p.pols_cancer(t) / entering, rel=1e-14)
    wrong = ((p.treat_months(t) + p.paid_months(t)) * p.pols_cancer(t)
             / (p.pols_cancer(t) + p.trig(t)))
    assert p.treat_months(t + 1) > wrong
    assert p.check_treat_cap() is True
    # The cap is a number of months, and the ledger is denominated in months.
    assert p.treat_cap() == 60
    assert max(p.treat_months(s) for s in range(p.proj_len())) < p.treat_cap()


def test_a_ledger_that_reads_small_is_not_deletable(cancer):
    """``M(12) = 0.4002`` months and ``V(12) = ¥2,401.31`` — and the cap still binds.

    ``E[min(sum, K)] != min(E[sum], K)``, and unlike the medical chassis's 通算 day ledger
    this one is reached by a real minority of diagnosed lives: on model point 4, whose cap
    is twelve months, the ledger reaches it and the monthly draw is cut for 423 months of
    the projection.
    """
    p = cancer.Projection[1]
    assert p.treat_months(12) == pytest.approx(0.4002, abs=LEDGER)
    assert p.adv_paid(12) == pytest.approx(2401.31, abs=YEN)
    p4 = cancer.Projection[4]
    assert p4.treat_cap() == 12
    capped = [t for t in range(p4.proj_len()) if p4.paid_months(t) < 0.10 - 1e-15]
    assert capped, "the twelve-month cap never binds"
    assert len(capped) == 423
    assert max(p4.treat_months(t) for t in range(p4.proj_len())) == pytest.approx(
        12.0, abs=1e-9)
    assert p4.check_treat_cap() is True


def test_insitu_diagnoses_generate_surgery_and_nothing_continuing(cancer):
    """A documented simplification with a stated direction of error, not an omission.

    An in-situ life stays in ``pols_healthy``, so it contributes no inpatient, treatment
    or outpatient benefit — the sourced 推計患者数 and 平均在院日数 figures are for 悪性新生物 and do
    not measure in-situ exposure. It does pay the surgery benefit in full, which is the
    second limb of ``claims(t, "SURGERY")``.
    """
    p = cancer.Projection[1]
    t = 3
    assert p.insitu_ev(t) > 0.0
    assert p.claims(t, "SURGERY") == pytest.approx(
        p.surg_mult() * p.base_amount() * 0.80 * p.insitu_ev(t), rel=1e-14)
    # No continuing exposure: the diagnosed state carries first diagnoses only.
    assert p.pols_cancer(t + 1) == pytest.approx(
        p.diag_first(t) * p.surv_canc(t), rel=1e-14)
    assert p.pols_healthy(t + 1) == pytest.approx(
        (p.pols_healthy(t) - p.diag_first(t)) * (1.0 - p.mort_rate_mth(t))
        * (1.0 - p.lapse_rate_mth(t)), rel=1e-14)


def test_claims_lapse_is_zero_and_claims_death_does_not_exist(cancer):
    """No surrender value under 終身払 and no death benefit in the composite.

    A non-zero column for either is a benefit the contract does not have. The zero column
    is published rather than dropped, because a missing column would only hide the fact.
    """
    for point_id in cancer.Data.model_point_table().index:
        p = cancer.Projection[point_id]
        df = p.result_cf()
        assert (df["claims_lapse"] == 0.0).all(), point_id
        assert p.claims(0, "LAPSE") == 0.0
    cells = set(cancer.Projection.cells)
    assert "claims_death" not in cells
    assert "cv_pp" not in cells                       # no surrender value at any duration
    assert not [c for c in cells if "apl" in c or "auto_prem" in c]
    with pytest.raises(FormulaError):
        cancer.Projection[1].claims(0, "DEATH")


def test_the_third_sector_table_is_a_valuation_table_not_experience(cancer):
    """``mort_be_factor = 1.25`` unwinds the sourced 70-85% risk-theory band and nothing more.

    Using the valuation table unadjusted as a best estimate understates mortality, which
    on a morbidity product **overstates** the liability, because every month of survival
    it adds is a month of benefit. The same factor must be used here and on the medical
    chassis. 1.25 is the reciprocal of 0.80, a round value **inside** the band and not its
    arithmetic midpoint, which is 0.775 and would give 1.29.
    """
    p = cancer.Projection[1]
    assert cancer.Projection.mort_be_factor == 1.25
    assert 1.25 == pytest.approx(1.0 / 0.80, rel=1e-14)       # inside the 70-85% band
    assert 0.70 < 0.80 < 0.85
    assert 1.0 / ((0.70 + 0.85) / 2) == pytest.approx(1.2903, abs=5e-5)   # not the midpoint
    for t in (0, 120, 480):
        assert p.mort_rate(t) == pytest.approx(
            min(1.0, 1.25 * p.mort_rate_at_age(p.age(t))), rel=1e-14)
        assert p.mort_rate(t) > p.mort_rate_at_age(p.age(t))
    assert p.mort_rate(p.proj_len() - 1) == 1.0                # the table terminates


def test_relative_survival_is_not_a_mortality_table(cancer):
    """5年相対生存率 nets out background mortality, so it converts into an **added** hazard.

    Multiplying survivorship by a relative-survival figure double-counts the background.
    The diagnosed rate is the baseline plus the excess, so it is strictly above both the
    baseline alone and the excess alone.
    """
    p = cancer.Projection[1]
    assert p.mu_ex() == pytest.approx(-math.log(p.surv_5y()) / 5.0, rel=1e-14)
    for t in (0, 240, 600):
        q, q_c = p.mort_rate_mth(t), p.mort_rate_canc_mth(t)
        assert 1.0 - q_c == pytest.approx(
            (1.0 - q) * math.exp(-p.mu_ex() / 12.0), rel=1e-14)
        assert q_c > q
        assert q_c > 1.0 - math.exp(-p.mu_ex() / 12.0)     # the baseline is not replaced


def test_cancer_deaths_sit_on_both_sides_of_the_mortality_basis(cancer):
    """A double count, stated rather than discovered, with a switch that removes it.

    The never-diagnosed carry a population table that already contains cancer deaths and
    the diagnosed carry them again as an excess hazard. At the anchor age the baseline is
    1% of the excess hazard; at 80 it is 56%.
    """
    p = cancer.Projection[1]
    assert cancer.Projection.net_of_cancer is False
    assert cancer.Projection.cancer_death_share == 0.28           # a [std] placeholder
    monthly_excess = p.mu_ex() / 12.0
    assert p.mort_rate_mth(0) / monthly_excess == pytest.approx(0.0103, abs=0.001)
    assert p.mort_rate_mth(12 * 40) / monthly_excess == pytest.approx(0.56, abs=0.01)
    with switched("Cancer_JP_S_netcanc", net_of_cancer=True) as model:
        q = model.Projection[1]
        assert q.mort_rate(0) == pytest.approx(0.00095 * (1.0 - 0.28), rel=1e-12)
        assert q.mort_rate(0) < p.mort_rate(0)


def test_age_band_incidence_steps_it_does_not_glide(cancer):
    """The registry publishes five-year bands, so the rate is flat inside one and jumps.

    Interpolating within a band is a choice, not a correction, and it would have to be the
    same choice in the model and in the CSV's ``provenance`` column. The sex factor is
    read at the **band midpoint** for the same reason, so the whole annual rate steps.
    """
    p = cancer.Projection[1]
    assert p.inc_band_at_age(40) == p.inc_band_at_age(42) == p.inc_band_at_age(44) == 40
    assert p.inc_band_at_age(45) == 45
    band = [p.inc_rate(12 * y) for y in range(5)]           # ages 40 to 44
    assert band[1:] == pytest.approx(band[:-1], rel=1e-15)
    assert p.inc_rate(12 * 5) > band[0]                      # age 45, a new band
    assert p.inc_rate(12 * 5) / band[0] == pytest.approx(
        340.48 / 220.28 * p.sex_factor(47.5) / p.sex_factor(42.5), rel=1e-12)


def test_reinstatement_re_runs_the_waiting_period(cancer):
    """復活 enters as a new model point, never as a negative lapse.

    A reinstated cancer policy has 90 days of no cover in front of it, which is a real
    anti-selection control; restoring it as a negative lapse would hand back cover the
    contract does not restore. So there is no reinstatement machinery, lapse is absorbing,
    and ``cover(t)`` is measured from this model point's own issue.
    """
    p = cancer.Projection[1]
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    assert not [n for n in names
                if "reinstat" in n or "revival" in n or "fukkatsu" in n]
    assert all(p.pols_healthy(t + 1) <= p.pols_healthy(t) + 1e-18
               for t in range(p.proj_len() - 1))
    assert all(p.pols_lapse(t) >= 0.0 for t in range(p.proj_len()))
    assert p.cover(p.wait_months() - 1) == 0.0 and p.cover(p.wait_months()) == 1.0


def test_rounded_lines_do_not_re_add(jp_cancer_anchor):
    """Assert against the unrounded aggregation, never against a sum of displayed figures.

    The month-5 claim components displayed to ¥0.01 sum to 131.40 against a ``claims``
    value of 131.39, and the seven policy-year-1 claim lines displayed to four decimals
    sum to 1,196.5916 against a ``claims`` total of 1,196.5915.
    """
    p = jp_cancer_anchor
    displayed = sum(round(p.claims(5, kind), 2) for kind in CARE_KINDS)
    assert displayed == pytest.approx(131.40, abs=1e-9)
    assert round(p.claims(5), 2) == pytest.approx(131.39, abs=1e-9)
    assert p.claims(5) == pytest.approx(sum(p.claims(5, k) for k in CARE_KINDS),
                                        rel=1e-15)
    df = p.result_cf().head(12)
    lines = ["claims_diag", "claims_insitu", "claims_hosp", "claims_surgery",
             "claims_treat", "claims_outpatient", "claims_advanced"]
    assert sum(round(df[c].sum(), 4) for c in lines) == pytest.approx(1196.5916, abs=1e-9)
    assert round(df[lines].sum(axis=1).sum(), 4) == pytest.approx(1196.5915, abs=1e-9)


# ---------------------------------------------------------------------------
# Roll-forward identities and the ledger checks


def test_the_seven_check_cells_are_published_with_their_residuals(cancer):
    """These seven identities, and no others, each with its per-month residual beside it.

    That they *close*, on all eight model points, is asserted in
    ``test_model_conventions_jp.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library. Running them again here,
    on a second instance of the same model, meant a second cold projection of the whole
    table to reach a verdict that had already been reached.

    What generic discovery cannot say is *which* checks ought to exist — a check that
    disappears simply stops being discovered, and the sweep passes. That is the statement
    left here.
    """
    checks = ("check_pols_roll_fwd", "check_cancer_roll_fwd", "check_cycle_ledger",
              "check_insitu_ledger", "check_treat_cap", "check_adv_cap",
              "check_net_cf")
    cells = set(cancer.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(checks)
    for check in checks:
        assert check + "_resid" in cells, check


def test_the_in_force_roll_forward_names_every_decrement(jp_cancer_anchor):
    """Death and lapse are the only ways out; a diagnosis moves a life, it does not remove one.

    There is no maturity term and no benefit-driven termination to add, so a first
    diagnosis cancels out of the identity: it takes a life from ``pols_healthy`` and puts
    it in ``pols_cancer`` in the same month.
    """
    p = jp_cancer_anchor
    for t in (0, 3, 11, 240, 900):
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-14)
        assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(
            p.pols_death(t) + p.pols_lapse(t), abs=1e-14)


def test_pols_if_at_reads_the_month_in_order(jp_cancer_anchor):
    """The library timing vocabulary, over a book whose two states decrement differently.

    ``"BEF_LAPSE"`` is the sum over the two states, each on its own mortality basis --
    the never-diagnosed on ``mort_rate_mth`` and the diagnosed on ``mort_rate_canc_mth``
    -- so a single blended rate applied to ``pols_if`` does not reproduce it. And the
    movement that defines this product is invisible to all three timings: a first
    diagnosis is not a decrement, so ``diag_first`` changes which benefits and which
    premium a life carries while leaving ``pols_if`` identical at every one of them.
    """
    p = jp_cancer_anchor
    for t in (0, 3, 11, 240, 900):
        assert p.pols_if_at(t, "BEF_DECR") == p.pols_if(t)
        assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(p.pols_if(t + 1), rel=1e-14)
        assert p.pols_if(t) - p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_death(t), abs=1e-14)
        assert p.pols_if_at(t, "BEF_LAPSE") - p.pols_if_at(t, "AFT_DECR") == (
            pytest.approx(p.pols_lapse(t), abs=1e-14))
    # The diagnosis transition is not one of the timings: it moves a life between states
    # inside the month and leaves the total untouched at all three points.
    t = 240
    blended = p.pols_if(t) * (1.0 - p.mort_rate_mth(t))
    assert p.diag_first(t) > 0.0 and p.pols_cancer(t) > 0.0
    assert p.pols_if_at(t, "BEF_LAPSE") != pytest.approx(blended, rel=1e-12)
    with pytest.raises(FormulaError):
        p.pols_if_at(1, "BEF_NOTHING")


def test_the_diagnosed_state_roll_forward_collapses_to_one_line(jp_cancer_anchor):
    """``pols_cancer(t+1) = (pols_cancer(t) + diag_first(t)) sc(t)``.

    The ``locked`` and ``open`` recursions each carry an ``unlock`` term of opposite sign,
    so their sum must collapse to this one line; a sign slip or an off-by-one in the delay
    shows up here and nowhere else in the in-force figures.
    """
    p = jp_cancer_anchor
    assert p.check_cancer_roll_fwd() is True
    for t in (3, 26, 27, 100, 500):
        assert p.check_cancer_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-14)
        assert p.pols_cancer(t) == pytest.approx(
            p.pols_locked(t) + p.pols_open(t), rel=1e-15)


def test_the_insitu_ledger_closes_where_it_is_observable(jp_cancer_anchor):
    """Benefit paid plus availability remaining is one, per never-diagnosed policy.

    ``insitu_used`` is accumulated off the published claim line rather than off the ledger
    recursion, so the identity fails if the benefit is paid at a rate the ledger is not
    decremented by. Once ``pols_healthy`` reaches zero at the terminal age the identity is
    read off nobody, and those months are excluded rather than papered over.
    """
    p = jp_cancer_anchor
    assert p.check_insitu_ledger() is True
    for t in (0, 3, 12, 600):
        assert p.insitu_avail(t) + p.insitu_used(t) == pytest.approx(1.0, abs=1e-12)
    last = p.proj_len() - 1
    assert p.pols_healthy(last) == 0.0
    assert p.insitu_ev(last) == 0.0
    assert p.insitu_avail(last) > 0.0            # still running, against nobody


def test_expenses_excludes_claim_handling_which_has_its_own_line(jp_cancer_anchor):
    """``expenses`` is acquisition plus maintenance; the claim cost is a line of its own.

    The two ride on different weights on this product -- the maintenance expense on
    ``pols_if``, which the waiver does not reduce, and the claim handling cost on the
    diagnosis and admission counts -- so folding them into one column hides a real
    movement. ``net_cf`` deducts both explicitly, and ``result_cf`` publishes both.
    """
    p = jp_cancer_anchor
    for t in (0, 3, 4, 200, 600):
        assert p.expenses(t) == pytest.approx(
            p.maint_expenses(t) + (20_000.0 if t == 0 else 0.0), rel=1e-14)
        assert p.claim_expenses(t) == pytest.approx(
            5_000.0 * (p.trig(t) + p.insitu_ev(t))
            + 3_000.0 * p.hosp_rate_mth(t) * p.pols_cancer(t), rel=1e-14)
        assert p.net_cf(t) == pytest.approx(
            p.premiums(t) - p.claims(t) - p.expenses(t) - p.claim_expenses(t)
            - p.commissions(t), abs=1e-9)
    # The maintenance expense is on pols_if, so it survives the waiver; the claim expense
    # is not, so at t = 200 the two are moving on different populations.
    t = 200
    assert p.maint_expenses(t) == pytest.approx(
        250.0 * 1.01 ** (t // 12) * p.pols_if(t), rel=1e-14)
    assert p.claim_expenses(t) > 0.0
    df = p.result_cf()
    assert df["claim_expenses"].iloc[:3].sum() == 0.0      # nothing claims before cover
    assert df["claim_expenses"].sum() > 0.0


def test_the_published_statement_re_adds_to_net_cf(jp_cancer_anchor):
    """``check_net_cf`` rebuilds ``net_cf`` from the columns a reader actually sees.

    And the columns a reader sees are the nine ``claims_*`` splits with **no bare
    ``claims`` subtotal** among them, so the row adds up as it stands: a reader summing
    the benefit columns of ``result_cf`` does not have to know which one to skip. The
    ``claims(t)`` cells still returns the total; it is the column that is not published.
    """
    p = jp_cancer_anchor
    assert p.check_net_cf() is True
    df = p.result_cf()
    splits = [c for c in df.columns if c.startswith("claims_")]
    assert len(splits) == 9
    assert "claims" not in df.columns
    outgo = df[splits].sum(axis=1)
    assert (df["premiums"] - outgo - df["expenses"] - df["claim_expenses"]
            - df["commissions"] - df["net_cf"]).abs().max() == pytest.approx(
                0.0, abs=1e-9)
    for t in (0, 3, 4, 200, 600):
        assert outgo.loc[t] == pytest.approx(p.claims(t), abs=1e-9)


# ---------------------------------------------------------------------------
# The optional modules, in both positions


def test_the_validity_adjustment_is_off_and_de_recognises_when_switched_on(cancer):
    """``void_adjust``: off in the base run, and the omission quantified rather than waved at."""
    p = cancer.Projection[1]
    assert cancer.Projection.void_adjust is False
    assert p.pols_if_init() == 1.0 and p.void_prob() == 0.0
    base_premiums = sum(p.premiums(t) for t in range(p.proj_len()))
    base_claims = sum(p.claims(t) for t in range(p.proj_len()))
    with switched("Cancer_JP_S_void2", void_adjust=True) as model:
        q = model.Projection[1]
        scale = 1.0 - 0.000368681
        assert sum(q.premiums(t) for t in range(q.proj_len())) == pytest.approx(
            base_premiums * scale, rel=1e-8)
        assert sum(q.claims(t) for t in range(q.proj_len())) == pytest.approx(
            base_claims * scale, rel=1e-8)


def test_anti_selective_lapse_is_off_and_loads_incidence_when_switched_on(cancer):
    """``inc_eff = inc_rate (1 + lam max(0, w_cum - w_ref))``; ``lam = 0`` in the base run.

    The loading moves **incidence**, not lapse, and on this product the effect is
    amplified by the waiver: the healthiest lives are also the only ones still paying.
    """
    p = cancer.Projection[1]
    assert cancer.Projection.sel_lapse_lambda == 0.0
    assert all(p.sel_lapse_factor(t) == 1.0 for t in (0, 12, 600))
    assert p.lapse_cum(0) == 0.0
    assert p.lapse_cum(600) > 0.20                 # past w_ref, but with lam at zero
    base_late = p.inc_rate(600)
    with switched("Cancer_JP_S_sel", sel_lapse_lambda=0.30) as model:
        q = model.Projection[1]
        assert q.sel_lapse_factor(0) == 1.0        # nothing has lapsed yet
        assert q.sel_lapse_factor(600) == pytest.approx(
            1.0 + 0.30 * (q.lapse_cum(600) - 0.20), rel=1e-12)
        assert q.sel_lapse_factor(600) > 1.0
        assert q.inc_rate(600) > base_late
        assert q.lapse_rate_mth(600) == p.lapse_rate_mth(600)   # lapse itself is unmoved


def test_conditioned_repeats_are_off_on_the_anchor_and_on_at_point_3(cancer):
    """The flag multiplies the relapse hazard by ``treat_prob`` — an order of magnitude.

    Two of the three sourced two-year designs require the insured to be under treatment
    for the second and later payments, so the two designs differ by a factor of ten rather
    than by a rounding.
    """
    p1, p3 = cancer.Projection[1], cancer.Projection[3]
    assert p1.repeat_conditioned() is False
    assert p1.relapse_rate_mth(0) == pytest.approx(0.06 / 12, rel=1e-14)
    assert p3.repeat_conditioned() is True
    assert p3.relapse_rate_mth(0) == pytest.approx(0.06 / 12 * 0.10, rel=1e-14)
    assert p1.relapse_rate_mth(0) / p3.relapse_rate_mth(0) == pytest.approx(10.0,
                                                                            rel=1e-12)
    # Fewer repeats, so fewer diagnosis payments per first diagnosis.
    def repeats(p):
        firsts = sum(p.diag_first(t) for t in range(p.proj_len()))
        return sum(p.trig(t) for t in range(p.proj_len())) / firsts
    assert repeats(p1) > repeats(p3) > 1.0


def test_the_hospital_stay_age_gradient_is_off_and_reads_the_bands_when_switched_on(
        cancer):
    """``hosp_age_gradient``: the all-ages 14.4 days in the base run, the four bands on.

    Both bases are sourced; the base run takes the all-ages figure because the gradient is
    published on four broad bands and the incidence on twenty-one narrow ones.
    """
    p = cancer.Projection[1]
    assert cancer.Projection.hosp_age_gradient is False
    assert all(p.hosp_stay_days(t) == 14.4 for t in (0, 12 * 25, 12 * 40))
    with switched("Cancer_JP_S_stay", hosp_age_gradient=True) as model:
        q = model.Projection[1]
        assert q.hosp_stay_days(0) == 10.7                 # age 40, the 35-64 band
        assert q.hosp_stay_days(12 * 25) == 15.5           # age 65
        assert q.hosp_stay_days(12 * 35) == 17.6           # age 75
        assert q.claims(12 * 35, "HOSP") > p.claims(12 * 35, "HOSP")
        assert q.claims(0, "SURGERY") == pytest.approx(p.claims(0, "SURGERY"),
                                                       rel=1e-12)


def test_the_insurance_age_offset_is_off_and_interpolates_when_switched_on(cancer):
    """``mort_age_offset``: 満年齢 in the base run, ``age(t) + 0.5`` for the 保険年齢 basis.

    第三分野標準生命表2018 is constructed for use on a nearest-birthday basis, so reading it at
    満年齢 understates the valuation age by about half a year.
    """
    p = cancer.Projection[1]
    assert cancer.Projection.mort_age_offset == 0.0
    assert p.mort_rate_at_age(40.5) == pytest.approx(
        0.5 * (p.mort_rate_at_age(40) + p.mort_rate_at_age(41)), rel=1e-14)
    with switched("Cancer_JP_S_offset", mort_age_offset=0.5) as model:
        q = model.Projection[1]
        assert q.mort_rate(0) == pytest.approx(
            1.25 * p.mort_rate_at_age(40.5), rel=1e-14)
        assert q.mort_rate(0) > p.mort_rate(0)


def test_the_cancer_free_baseline_is_off_and_nets_when_switched_on(cancer):
    """``net_of_cancer``: a capability demonstration, not a calibration.

    No document in this product's source set gives the share of Japanese deaths
    attributable to 悪性新生物, so ``cancer_death_share`` is a **[std]** placeholder.
    """
    p = cancer.Projection[1]
    assert cancer.Projection.net_of_cancer is False
    assert p.mort_rate(0) == pytest.approx(0.00095, rel=1e-12)
    with switched("Cancer_JP_S_noc", net_of_cancer=True) as model:
        q = model.Projection[1]
        for t in (0, 240):
            assert q.mort_rate(t) == pytest.approx(
                p.mort_rate(t) * 0.72, rel=1e-12)
            assert q.mort_rate_canc_mth(t) < p.mort_rate_canc_mth(t)


def test_renewal_repricing_is_off_and_steps_the_premium_when_switched_on(cancer):
    """``renew_reprice_rate``: the 定期 flag's real consequence, held flat in the base run.

    The renewal is automatic and neither document states a maximum renewal age, so the
    flag does not shorten the horizon; what it changes is the premium, and ``jplib``
    records that tension rather than resolving it.
    """
    p1, p3 = cancer.Projection[1], cancer.Projection[3]
    assert cancer.Projection.renew_reprice_rate == 0.0
    assert p3.chassis() == "teiki"
    assert all(p3.premium_factor(t) == 1.0 for t in (0, 120, 240))
    assert p3.proj_len() == 12 * (116 - 50 + 1)          # the 定期 flag runs to omega too
    with switched("Cancer_JP_S_reprice", renew_reprice_rate=0.10) as model:
        q3, q1 = model.Projection[3], model.Projection[1]
        assert q3.premium_factor(0) == 1.0
        assert q3.premium_factor(120) == pytest.approx(1.10, rel=1e-14)
        assert q3.premium_factor(240) == pytest.approx(1.21, rel=1e-14)
        assert q3.premiums(120) == pytest.approx(
            1.10 * q3.premium_mth_pp() * q3.pols_healthy(120), rel=1e-14)
        assert q1.premium_factor(240) == 1.0             # 終身 does not reprice
    assert p1.chassis() == "shushin"


def test_the_diagnosed_lapse_loading_is_inert_on_the_anchor_and_live_on_point_7(cancer):
    """``lapse_canc_factor``: a switch whose off position is a product fact, not a zero.

    The base value is 1.0 and it reaches no cash flow wherever the waiver fires, because a
    waived life has no premium to miss and no surrender value to take; it becomes live only
    on the designs where the diagnosed keep paying. Moving it must leave the anchor cell
    bit-for-bit unchanged and must scale the diagnosed exit rate on model point 7.
    """
    assert cancer.Projection.lapse_canc_factor == 1.0
    p1, p7 = cancer.Projection[1], cancer.Projection[7]
    base1 = sum(p1.net_cf(t) for t in range(p1.proj_len()))
    base7 = sum(p7.net_cf(t) for t in range(p7.proj_len()))
    for t in (4, 200, 600):
        assert p1.lapse_rate_canc_mth(t) == 0.0
        assert p7.lapse_rate_canc_mth(t) == pytest.approx(
            p7.lapse_rate_mth(t), rel=1e-14)
    with switched("Cancer_JP_S_canclapse", lapse_canc_factor=0.50) as model:
        q1, q7 = model.Projection[1], model.Projection[7]
        assert sum(q1.net_cf(t) for t in range(q1.proj_len())) == pytest.approx(
            base1, rel=1e-14)
        for t in (4, 200, 600):
            assert q1.lapse_rate_canc_mth(t) == 0.0        # inert under the waiver
            assert q7.lapse_rate_canc_mth(t) == pytest.approx(
                0.50 * q7.lapse_rate_mth(t), rel=1e-14)
        for t in (200, 600):
            assert q7.pols_cancer(t) > p7.pols_cancer(t)   # fewer diagnosed exits
        assert sum(q7.net_cf(t) for t in range(q7.proj_len())) != pytest.approx(
            base7, rel=1e-9)
        assert q7.check_pols_roll_fwd() is True
        assert q7.check_cancer_roll_fwd() is True
        assert q7.check_cycle_ledger() is True


def test_the_discharge_rider_is_off_on_every_point_but_8(cancer):
    """The one cash flow the technical notes do not define, supplied as a **[std]** formula.

    ``product-spec.md`` specifies the がん退院一時金 and puts it in scope but the notes' recursion
    section defines seven claim lines and not this one, so the model carries an eighth
    behind a model-point flag that is off everywhere the worked example can see.
    """
    for point_id in cancer.Data.model_point_table().index:
        p = cancer.Projection[point_id]
        if point_id == 8:
            continue
        assert p.disch_rider() is False, point_id
        assert (p.result_cf()["claims_discharge"] == 0.0).all(), point_id
    p8 = cancer.Projection[8]
    assert p8.disch_rider() is True
    t = 200
    assert p8.claims(t, "DISCHARGE") == pytest.approx(
        10.0 * p8.base_amount() * 0.60 * p8.hosp_rate_mth(t) * p8.pols_cancer(t),
        rel=1e-14)
    assert sum(p8.claims(t, "DISCHARGE") for t in range(p8.proj_len())) > 0.0


# ---------------------------------------------------------------------------
# Structural product facts


def test_the_cover_is_whole_of_life_with_no_maturity_and_no_policy_term(cancer):
    """``proj_len`` is set by the mortality table's terminal age, not by a policy term.

    116 for a male and 118 for a female, and nothing shortens it — there is no maturity
    benefit, no 満期保険金 and no benefit-driven termination, and the 定期 chassis flag renews
    automatically.
    """
    for point_id, omega in ((1, 116), (2, 118), (3, 116), (7, 118)):
        p = cancer.Projection[point_id]
        assert p.omega_age() == omega
        assert p.proj_len() == 12 * (omega - p.issue_age() + 1)
        assert p.mort_rate(p.proj_len() - 1) == 1.0
    cells = set(cancer.Projection.cells)
    assert not [c for c in cells if "maturity" in c]
    assert "policy_term" not in cells


def test_the_three_states_partition_the_in_force(jp_cancer_anchor):
    """``pols_healthy + pols_locked + pols_open = pols_if``, and none of them is negative.

    Two states will not do: the diagnosis benefit repeats on a clock keyed to the previous
    payment, so eligibility has to be carried separately from the diagnosed population.
    """
    p = jp_cancer_anchor
    for t in (0, 3, 27, 200, 900):
        assert p.pols_locked(t) >= -1e-15 and p.pols_open(t) >= -1e-15
        assert p.pols_if(t) == pytest.approx(
            p.pols_healthy(t) + p.pols_locked(t) + p.pols_open(t), rel=1e-14)
    assert p.pols_open(26) == 0.0                  # nothing has completed a cycle yet
    assert p.pols_open(27) > 0.0
    assert p.pols_locked(27) > 0.0


def test_the_sex_split_crosses_and_the_clamp_binds_only_on_the_100_plus_band(cancer):
    """A unisex basis would be materially wrong at every age, because the curves cross.

    Female incidence is well above male at 35-39 and well below it at 70-74. The linear
    construction of ``f_male`` reaches 2 at age 98.87, so above that the female limb would
    go negative; the clamp binds on the 100+ band alone, where it takes female incidence
    to exactly zero and caps the male rate at twice the band rate.
    """
    p1, p2 = cancer.Projection[1], cancer.Projection[2]
    assert p2.sex() == "F" and p2.issue_age() == 35
    assert p2.sex_factor(37.5) == pytest.approx(0.551547, abs=5e-7)
    assert 2.0 - p2.sex_factor(37.5) > p2.sex_factor(37.5)          # female above male
    assert p2.sex_factor(72.5) == pytest.approx(1.377629, abs=5e-7)
    assert 2.0 - p2.sex_factor(72.5) < p2.sex_factor(72.5)          # and below it
    # f_male = 1 at age 56.4995, which the notes display as 56.5 and call a validation
    # target rather than a claim: the sourced crossover is somewhere between about 25 and
    # about 55.
    crossover = 37.5 + (1.0 - 0.551547) * 35.0 / (1.377629 - 0.551547)
    assert round(crossover, 1) == 56.5
    assert p2.sex_factor(crossover) == pytest.approx(1.0, abs=5e-12)
    assert p2.inc_rate(0) == pytest.approx(
        0.0013221 * (2.0 - 0.551547), abs=5e-10)
    # The clamp, and what it does at each limb of the 100+ band.
    assert p2.sex_factor(102.5) == 2.0
    t_f, t_m = 12 * (100 - 35), 12 * (100 - 40)
    assert p2.age(t_f) == 100 and p1.age(t_m) == 100
    assert p2.inc_rate(t_f) == 0.0
    assert p1.inc_rate(t_m) == pytest.approx(2.0 * p1.inc_rate_both(t_m), rel=1e-14)


def test_the_premium_paying_period_stops_at_65_on_the_short_pay_points(cancer):
    """65歳払済 stops the premium and not the cover, nor the maintenance expense.

    That is what makes expense inflation a first-order lever on a short-pay design: the
    expense runs for another half-century with no premium against it.
    """
    p5 = cancer.Projection[5]
    assert p5.prem_period_type() == "to_65" and p5.issue_age() == 20
    t64, t65 = 12 * 44, 12 * 45
    assert p5.age(t64) == 64 and p5.age(t65) == 65
    assert p5.prem_payable(t64) == 1.0 and p5.premiums(t64) > 0.0
    assert p5.prem_payable(t65) == 0.0 and p5.premiums(t65) == 0.0
    assert p5.pols_if(t65) > 0.0                       # cover continues unpaid
    assert p5.maint_expenses(t65) > 0.0
    assert cancer.Projection[1].prem_period_type() == "whole_life"
    assert cancer.Projection[1].prem_payable(12 * 45) == 1.0


def test_the_no_waiver_design_reverses_both_consequences(cancer):
    """On ``waiver_trigger = "none"`` the diagnosed keep paying and can lapse.

    Neither consequence is hard-coded: they both follow from the waiver, which is why
    ``pols_payer`` and ``lapse_rate_canc_mth`` are cells rather than constants.
    """
    p7 = cancer.Projection[7]
    assert p7.waiver_trigger() == "none"
    for t in (4, 200, 600):
        assert p7.pols_payer(t) == pytest.approx(p7.pols_if(t), rel=1e-15)
        assert p7.premiums(t) == pytest.approx(
            p7.premium_mth_pp() * p7.pols_if(t), rel=1e-14)
        assert p7.lapse_rate_canc_mth(t) == pytest.approx(
            p7.lapse_rate_mth(t), rel=1e-14)
        assert p7.surv_canc(t) < 1.0 - p7.mort_rate_canc_mth(t) + 1e-15
    assert p7.check_pols_roll_fwd() is True
    assert p7.check_cancer_roll_fwd() is True


def test_result_cf_publishes_the_notes_columns(jp_cancer_anchor):
    """The statement carries the three counts side by side with the nine benefit lines.

    And it carries **no bare ``claims`` subtotal** among them: a cash flow statement must
    not publish its own subtotal beside its parts, or its columns stop summing to
    ``net_cf`` without a reader knowing which one to skip. The ``claims(t)`` cells is
    still there and still returns the total.
    """
    df = jp_cancer_anchor.result_cf()
    assert list(df.columns)[0] == "pols_if"
    assert list(df.columns) == [
        "pols_if", "pols_healthy", "pols_cancer", "premiums", "claims_diag",
        "claims_insitu", "claims_hosp", "claims_surgery", "claims_treat",
        "claims_outpatient", "claims_advanced", "claims_discharge", "claims_lapse",
        "expenses", "claim_expenses", "commissions", "net_cf",
    ]
    assert "claims" not in df.columns
    assert jp_cancer_anchor.claims(5) == pytest.approx(
        df.loc[5, [c for c in df.columns if c.startswith("claims_")]].sum(), abs=1e-9)
    assert df.index.name == "t"
    assert len(df) == jp_cancer_anchor.proj_len() == 924
    assert df.loc[0, "net_cf"] == pytest.approx(-71250.00, abs=YEN)
    assert "liability_cf" not in set(jp_cancer_anchor.cells)     # one stream, one sign


def test_the_model_point_table_carries_its_eight_variants(cancer):
    """Eight points, each exercising something the anchor cell does not.

    The variants are listed here as well as shipped: the female limb and the 118 terminal
    age, the 定期 flag with conditioned repeats, the ¥5,000 course with no 先進医療 rider and a
    cap that binds, both ends of the 20-75 issue-age range, 65歳払済, a no-waiver design and
    the discharge rider.

    That every row of the table *projects* — a clean frame spanning ``proj_len()``, no NaN,
    ``pols_if`` never negative — is asserted in ``test_model_conventions_jp.py``, over one
    instance of the model rather than a second one built here.
    """
    table = cancer.Data.model_point_table()
    assert len(table) == 8
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["chassis"]) == {"shushin", "teiki"}
    assert set(table["prem_period"]) == {"whole_life", "to_65"}
    assert set(table["waiver_trigger"]) == {"cancer_diag", "none"}
    assert sorted(set(table["insitu_pct"])) == [0.10, 0.50, 1.00]
    assert table["issue_age"].min() == 20 and table["issue_age"].max() == 75
    assert not cancer.Projection[4].adv_rider()
    assert sum(cancer.Projection[4].claims(t, "ADVANCED")
               for t in range(cancer.Projection[4].proj_len())) == 0.0


# The 20 sourced 第三分野標準生命表2018 rates that fall inside the age range this model reads.
# Each is quoted under attribution and each is an ANCHOR of the shipped construction, so
# each must come back out of the file unchanged -- that is the property the graduation was
# chosen for, and the property nine independent curve fits failed to have.
SOURCED_ANCHORS = {
    ("M", 30): 0.00041, ("M", 40): 0.00076, ("M", 60): 0.00548, ("M", 65): 0.00845,
    ("M", 75): 0.02242, ("M", 80): 0.04046, ("M", 85): 0.07110, ("M", 90): 0.11657,
    ("M", 115): 0.58241, ("M", 116): 1.00000,
    ("F", 30): 0.00022, ("F", 40): 0.00043, ("F", 60): 0.00209, ("F", 65): 0.00317,
    ("F", 70): 0.00510, ("F", 75): 0.00967, ("F", 80): 0.01899, ("F", 85): 0.03843,
    ("F", 90): 0.07574, ("F", 118): 1.00000,
}


def test_the_shipped_mortality_table_is_a_construction_not_a_copy(cancer):
    """Every row says so, and every sourced rate inside the read range is pinned.

    第三分野標準生命表2018 can be retrieved and checked by anyone, but its publisher's terms
    prohibit redistribution, so what ships is a **[std]** construction: the individual
    rates the library quotes and attributes, graduated log-linearly (geometrically)
    between adjacent anchors. No conclusion about Japanese third-sector mortality follows
    from it beyond those anchored rates.
    """
    tbl = cancer.Data.mort_table()
    assert tbl["provenance"].str.contains(r"\[std\]").all()
    assert "第三分野標準生命表2018" in tbl.loc[("M", 40), "provenance"]
    for key, rate in SOURCED_ANCHORS.items():
        assert tbl.loc[key, "mort_rate"] == rate, key
        assert "ANCHOR" in tbl.loc[key, "provenance"], key
    # The terminal rate is itself a sourced 1.00000, not a curve closing on one, and the
    # best-estimate factor is capped rather than pushing it past 1.
    assert tbl.loc[("M", 116), "mort_rate"] == 1.0
    assert tbl.loc[("F", 118), "mort_rate"] == 1.0
    assert cancer.Projection[1].mort_rate(cancer.Projection[1].proj_len() - 1) == 1.0


def test_the_graduation_is_log_linear_between_the_sourced_anchors(cancer):
    """Between two anchors the table is geometric in age, and it disturbs neither end.

    ``q(x) = q(a) (q(b)/q(a))^((x-a)/(b-a))``. Every row between two anchors carries the
    pair it was interpolated from in its ``provenance``, and the interpolation is monotone
    between them, so a rate read at any age sits inside the two sourced rates that bracket
    it rather than wherever a fitted curve would put it.
    """
    p = cancer.Projection[1]
    tbl = cancer.Data.mort_table()
    for sex, a, b in (("M", 40, 60), ("M", 90, 115), ("F", 65, 70), ("F", 85, 90)):
        qa, qb = tbl.loc[(sex, a), "mort_rate"], tbl.loc[(sex, b), "mort_rate"]
        for x in range(a + 1, b):
            expected = qa * (qb / qa) ** ((x - a) / (b - a))
            assert tbl.loc[(sex, x), "mort_rate"] == pytest.approx(
                expected, rel=5e-5), (sex, x)
            assert "graduation" in tbl.loc[(sex, x), "provenance"], (sex, x)
            assert "ANCHOR" not in tbl.loc[(sex, x), "provenance"], (sex, x)
    # Cut to the ages this model reads: the composite's 20-75 issue-age range run out to
    # each sex's terminal age, 116 male and 118 female.
    for sex, top in (("M", 116), ("F", 118)):
        ages = sorted(a for (s, a) in tbl.index if s == sex)
        assert ages == list(range(20, top + 1)), sex
    assert p.mort_rate_at_age(40) == 0.00076


def test_the_incidence_basis_is_sourced_and_reproduced(cancer):
    """The contrast with the mortality table, asserted rather than described.

    The age-banded 罹患率 of 全国がん登録 are public and freely downloadable, so they are
    reproduced verbatim with their attribution; what is **[std]** about the incidence
    basis is only the sex split, which lives in a two-row file of sourced ratios.
    """
    inc = cancer.Data.incidence_table()
    assert inc.loc[40, "rate_per_100k"] == 220.28
    assert inc.loc[35, "rate_per_100k"] == 132.21
    assert inc.loc[70, "rate_per_100k"] == 1948.71
    assert inc.index.max() == 100                       # the 100+ open band
    assert inc["provenance"].str.contains("R5").all()
    assert not inc["provenance"].str.contains(r"\[std\]").any()
    # Reproducing the dataset verbatim is conditional on carrying the attribution string
    # the publisher requires, so the string travels in the provenance column [REG-R29].
    attribution = ("Cancer Statistics. Cancer Information Service, "
                   "National Cancer Center, Japan")
    assert inc["provenance"].str.contains(attribution, regex=False).all()
    assert cancer.Data.survival_table()["provenance"].str.contains(
        attribution, regex=False).all()
    sf = cancer.Data.sex_factor_table()
    assert len(sf) == 2
    assert sf.loc[37.5, "f_male"] == pytest.approx(72.92 / 132.21, abs=5e-6)
    assert sf.loc[72.5, "f_male"] == pytest.approx(2684.60 / 1948.71, abs=5e-6)
    surv = cancer.Data.survival_table()
    assert surv.loc["M", "surv_5y"] == 0.6317 and surv.loc["F", "surv_5y"] == 0.6684
