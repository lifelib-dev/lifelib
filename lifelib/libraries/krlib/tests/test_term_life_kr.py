"""Golden and structural tests for Term_KR_S.

The golden values are the worked example in
products/term_life/technical-notes.md ("Worked example"), which projects the anchor cell
M40 / 20년만기 전기납 / 비갱신형 / KRW 100,000,000 of cover / KRW 15,080 a month — the cell
that is doubly prescribed in Korea, being both the 감독규정 기준연령 요건 and the
생명보험협회 disclosure's 대표계약, so its premium is a published figure rather than a
standardization.  They are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

**The grid is monthly**, which is the grid the contract is paid on: 월납 is the only
premium mode on seven of the retrieved products and the disclosure's own basis [S5], and
the rate card is quoted per month [S12].  ``t`` is a **policy month**, the anchor projects
``proj_len() = 240`` rows, and the contractual policy year is the derived label
``policy_year(t) = t // 12 + 1``.  Two consequences shape this module.

First, the **decrement basis stays annual and is converted**: every Korean 예정
경험사망률 disclosure and the supervisor's own 적용해지율 vector are published as annual
rates [S12] [REG-R27], so ``mort_rate`` and ``lapse_rate`` are asserted at the annual
values the sources publish and ``mort_rate_mth`` and ``lapse_rate_mth`` against
``1 - (1 - q)^(1/12)``.  :func:`test_the_monthly_decrements_compound_back_to_the_annual_ones`
is the check that ties the two together, and it is the strongest single statement this
module makes: twelve monthly exits leave exactly the in-force an annual step leaves, so
the conversion moved the **timing** of the exposure and nothing else.

Second, the worked example is printed the way the library's other monthly models print
theirs — a **first policy year** table at ``t = 0 ... 12``, **milestone rows** at
``t = 12, 60, 120, 180, 239``, and the undiscounted totals — rather than as 240 rows
nobody can read.  The decrement basis keeps its twenty rows, one per policy year, because
that is the unit the rates are published in.

Tolerances follow the precision the notes display: money to the won's second decimal,
in-force and the exit split to the ten decimals the notes print them at, and the decrement
rates to the eight the basis table prints.

The 갱신형 (*gaengsinhyeong*, renewable) panel is asserted beside the anchor, because the
mechanic that makes this the library's protection chassis does not appear on the anchor
cell at all: model points 3 and 4 are one policy on the two contract-boundary readings, and
the published renewal ladder — 9,000 -> 21,000 -> 56,000 -> 201,000 won a month — is a
sourced quantity in Korea where it is a standardization everywhere else in this repository.

Beyond the worked example this module asserts every product fact the notes list under
"Known modeling pitfalls", because each of them is a way an implementation can look right
and be wrong.  There is one ``test_pitfall_*`` per bullet, naming the pitfall in its
docstring: the renewal decline that is not lapse and whose processing order is not
cosmetic; truncation that shortens the **cycle** and not the horizon; a 비갱신형 contract
that never renews; a premium indexed by the renewal cycle and not by the policy year; a
premium waiver that does not survive a 갱신 where the suicide and contestability clocks do;
a waiver incidence that must not be scaled off ``mort_rate``; a 재해사망 uplift that splits
the death decrement rather than adding one; a lapse that pays nothing and a zero that must
be published rather than inferred; a 전기납 resolution that couples ``pay_term`` to the
contract boundary; a ``qbar`` built on **table** rates and not best-estimate ones; a premium
that rounds to 10 won *before* annualization and an annualization exact in amount and
standardized only in timing; a 선지급 cap reached exactly at the anchor and an accelerated
amount taken out of the death benefit rather than beside it; a 부활 pool carried by vintage
that renewal declines never enter; tables read at 보험나이 and at nothing else; a 장해 state
that is not a benefit, Korea having no 高度障害保険金 analogue; and the absence of a
``claims`` aggregate column beside the split ones.

The seven ``check_*`` cells are asserted **by name**, because a generic sweep cannot notice
a check that has quietly disappeared, and the [std] scalar assumptions are read off the
model so that a silent change to an assumption fails a test rather than moving a result.
The whole-table sweep belongs to ``test_model_conventions_kr.py``; the model points taken
here are the ones that exercise a particular mechanic.
"""
import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-11      # in-force and exit counts, displayed to 10 d.p.
RATE = 5e-9          # the decrement basis table's rates, displayed to 8 d.p.

MODEL_DIR = LIB / MODELS["Term_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "The decrement basis, policy year by policy year": y -> (보험나이, q_x^tab, q, q^m, w,
# w^m, l at the start of the year).  The **annual** rates are the sourced quantity — every
# Korean 예정 경험사망률 disclosure and the supervisor's 적용해지율 vector are annual — and
# the monthly ones are their uniform-force conversions, which are what the roll-forward
# applies.  ``y`` is the contractual 1-based policy year; policy year ``y`` opens at month
# ``t = 12 (y - 1)``.
WORKED_EXAMPLE_BASIS = {
    1:  (40, 0.00065000, 0.00055250, 0.0000460533, 0.0460000000, 0.0039166106, 1.0000000000),
    2:  (41, 0.00069504, 0.00059078, 0.0000492453, 0.0376048847, 0.0031890865, 0.9534729150),
    3:  (42, 0.00074482, 0.00063310, 0.0000527734, 0.0307418990, 0.0025986464, 0.9170755621),
    4:  (43, 0.00079985, 0.00067987, 0.0000566737, 0.0251314254, 0.0021188032, 0.8883201687),
    5:  (44, 0.00086067, 0.00073157, 0.0000609846, 0.0205448773, 0.0017284095, 0.8654066502),
    6:  (45, 0.00092789, 0.00078871, 0.0000657493, 0.0167953857, 0.0014105066, 0.8470068787),
    7:  (46, 0.00100219, 0.00085186, 0.0000710162, 0.0137301857, 0.0011514463, 0.8321242517),
    8:  (47, 0.00108431, 0.00092166, 0.0000768378, 0.0112243924, 0.0009402128, 0.8199999093),
    9:  (48, 0.00117508, 0.00099882, 0.0000832730, 0.0091759127, 0.0007678942, 0.8100486275),
    10: (49, 0.00127541, 0.00108410, 0.0000903865, 0.0075012856, 0.0006272667, 0.8018140251),
    11: (50, 0.00138630, 0.00117836, 0.0000982493, 0.0061322822, 0.0005124655, 0.7949366641),
    12: (51, 0.00150887, 0.00128254, 0.0001069412, 0.0050131253, 0.0004187234, 0.7891309148),
    13: (52, 0.00164435, 0.00139770, 0.0001165495, 0.0040982174, 0.0003421613, 0.7841678848),
    14: (53, 0.00179408, 0.00152497, 0.0001271696, 0.0033502824, 0.0002796198, 0.7798626566),
    15: (54, 0.00195959, 0.00166565, 0.0001389104, 0.0027388475, 0.0002285243, 0.7760646153),
    16: (55, 0.00214252, 0.00182114, 0.0001518887, 0.0022390010, 0.0001867752, 0.7726499798),
    17: (56, 0.00234471, 0.00199300, 0.0001662355, 0.0018303777, 0.0001526596, 0.7695160610),
    18: (57, 0.00256820, 0.00218297, 0.0001820964, 0.0014963292, 0.0001247797, 0.7665767149),
    19: (58, 0.00281521, 0.00239293, 0.0001996297, 0.0012232453, 0.0001019943, 0.7637587538),
    20: (59, 0.00308823, 0.00262500, 0.0002190132, 0.0010000000, 0.0000833716, 0.7609991050),
}

# "The cash flow statement, the first policy year": t -> (pols_if, premiums, claims_death,
# claim_expenses, expenses, commissions, net_cf).  Thirteen rows, ``t = 0 ... 12``, so that
# the year closes and the first row of policy year 2 — where the inflation factor steps and
# the renewal commission starts — is visible beside it.  The four other claims_* columns
# are 0.00 in every row of this model point; the notes say so and the row test asserts it.
WORKED_EXAMPLE_CF = {
    0:  (1.0000000000, 15080.00, 4605.33, 13.82, 122000.00, 108576.00, -220115.15),
    1:  (0.9960375164, 15020.25, 4587.08, 13.76,   1992.08,      0.00,    8427.33),
    2:  (0.9920907341, 14960.73, 4568.91, 13.71,   1984.18,      0.00,    8393.93),
    3:  (0.9881595909, 14901.45, 4550.80, 13.65,   1976.32,      0.00,    8360.67),
    4:  (0.9842440247, 14842.40, 4532.77, 13.60,   1968.49,      0.00,    8327.54),
    5:  (0.9803439739, 14783.59, 4514.81, 13.54,   1960.69,      0.00,    8294.54),
    6:  (0.9764593770, 14725.01, 4496.92, 13.49,   1952.92,      0.00,    8261.68),
    7:  (0.9725901728, 14666.66, 4479.10, 13.44,   1945.18,      0.00,    8228.94),
    8:  (0.9687363002, 14608.54, 4461.35, 13.38,   1937.47,      0.00,    8196.33),
    9:  (0.9648976985, 14550.66, 4443.68, 13.33,   1929.80,      0.00,    8163.86),
    10: (0.9610743072, 14493.00, 4426.07, 13.28,   1922.15,      0.00,    8131.51),
    11: (0.9572660661, 14435.57, 4408.53, 13.23,   1914.53,      0.00,    8099.29),
    12: (0.9534729150, 14378.37, 4695.41, 14.09,   1945.08,    431.35,    7292.44),
}

# "The milestone rows": the first month of policy years 2, 6 and 11, the first month of the
# second half of the term, and the last projected month.  Reading 240 rows is not reading;
# these are the five the notes print in full beneath the first-year table.
MILESTONE_CF = {
    12:  (0.9534729150, 14378.37,  4695.41, 14.09, 1945.08, 431.35,  7292.44),
    60:  (0.8470068787, 12772.86,  5569.01, 16.71, 1870.33, 383.19,  4933.63),
    120: (0.7949366641, 11987.64,  7810.20, 23.43, 1938.05, 359.63,  1856.34),
    180: (0.7726499798, 11651.56, 11735.68, 35.21, 2079.77, 349.55, -2548.64),
    239: (0.7584718208, 11437.76, 16611.54, 49.83, 2209.90, 343.13, -7776.65),
}

# "Load-bearing values at full float64 precision", printed in the notes so that a reader
# reconciling to the model rather than to the rounded table has something exact to
# reconcile to.  ``pols_if(12)`` is the one worth staring at: it is the annual-grid model's
# ``pols_if(1)`` to the last bit, which is what makes the monthly step a re-timing of the
# same decrement basis rather than a different one.
FULL_PRECISION = {
    "pols_if(1)": 0.9960375164203861,
    "pols_if(12)": 0.9534729149999999,
    "pols_if(120)": 0.7949366641324892,
    "pols_if(239)": 0.7584718208001523,
    "premiums(1)": 15020.245747619421,
    "claims_death(0)": 4605.332987672738,
    "claim_expenses(0)": 13.815998963018217,
    "expenses(0)": 122000.0,
    "commissions(0)": 108576.0,
    "net_cf(0)": -220115.14898663576,
    "net_cf(1)": 8427.325030154227,
    "net_cf(12)": 7292.4400417024035,
    "net_cf(120)": 1856.3392698344896,
    "net_cf(239)": -7776.65049712519,
    "mort_rate_mth(0)": 4.605332987672739e-05,
    "lapse_rate_mth(0)": 0.003916610622698213,
}

# The in-force at each 계약해당일 of the annual-grid model this one replaced, which the
# monthly roll-forward must reproduce **exactly**: twelve monthly exits at
# ``1 - (1 - q)^(1/12)`` compound to the year's annual rate, so the anniversary in-force is
# unchanged and only the exposure inside the year has moved.
ANNIVERSARY_INFORCE = {
    12: 0.953472915, 24: 0.917075562112279, 108: 0.8018140250566161,
    228: 0.7609991050099496,
}

TOTAL_POLS_IF = 196.5791307004
TOTAL_PREMIUMS = 2964413.29
TOTAL_CLAIMS_DEATH = 2063167.17
TOTAL_CLAIM_EXPENSES = 6189.50
TOTAL_EXPENSES = 594050.31
TOTAL_COMMISSIONS = 192196.36
TOTAL_NET_CF = 108809.94
TOTAL_POLS_DEATH = 0.0206316717
TOTAL_POLS_LAPSE = 0.2211258440
POLS_MATURITY_LAST = 0.7582424843     # pols_maturity(proj_len() - 1) on the anchor

# The published 갱신형 ladder: (cycle k, first month t of the cycle, attained 보험나이,
# P_m, P_a).  ``k`` stays the contractual 1-based cycle label; ``t`` is the 0-based month,
# so a ten-year cycle starts at t = 0, 120, 240, 360.
RENEWAL_LADDER = [
    (1,   0, 40,   9000.0,  108000.0),
    (2, 120, 50,  21000.0,  252000.0),
    (3, 240, 60,  56000.0,  672000.0),
    (4, 360, 70, 201000.0, 2412000.0),
]

# The notes' boundary-row table for model point 3, the long boundary reading:
# t -> (pols_if, renewal_decline_rate, pols_decline, wop_waived_frac, net_cf).  A boundary
# is now the **last month** of a cycle — t = 119, 239, 359 — and the repriced premium takes
# effect the month after.
GAENGSIN_BOUNDARY_ROWS = {
    108: (0.7405136863, 0.0, 0.0000000000, 0.0071770030, -2065.00),
    119: (0.7268743823, 0.2, 0.1451293946, 0.0079050974, -2031.58),
    120: (0.5805175782, 0.0, 0.0000000000, 0.0000000000,  4689.19),
    239: (0.5080959106, 0.2, 0.1015364175, 0.0079050974, -2373.66),
    240: (0.4061456699, 0.0, 0.0000000000, 0.0000000000, 11060.04),
    359: (0.3708404546, 0.2, 0.0741053844, 0.0079050974, -4501.81),
    360: (0.2964215375, 0.0, 0.0000000000, 0.0000000000, 36093.65),
    479: (0.2533886360, 0.0, 0.0000000000, 0.0079050974,   897.53),
}

# deaths, lapses, declines at t = 119, the first boundary month of model point 3
BOUNDARY_EXITS = (0.0000656996, 0.0011617099, 0.1451293946)
GAENGSIN_TOTAL_NET_CF = 2919193.21
CURRENT_TERM_NET_CF = -181055.18
GAENGSIN_FIRST_CYCLE_NET_CF = -172034.54
WAIVED_AT_CYCLE_END = 0.007905097430285151

# "The other eight shipped model points, undiscounted":
# pid -> (proj_len in months, proj_years, premium_mth_pp(0), premiums, all claims, net_cf).
POINT_SUMMARY = {
    1:  (240, 20,  15080.0,  2964413.29,  2063167.17,   108809.94),
    2:  (240, 20,   8010.0,  1580824.99,  1063462.97,  -184214.97),
    3:  (480, 40,   9000.0, 11517624.04,  7375134.92,  2919193.21),
    4:  (120, 10,   9000.0,   968241.62,   700446.17,  -181055.18),
    5:  (240, 20,   6620.0,   716061.64,   508324.88,  -485830.35),
    6:  (240, 20,  44250.0,  8690062.33,  8740412.26, -1214843.72),
    7:  (180, 15,  40040.0,  5860602.54,  3839438.58,  1075806.25),
    8:  (360, 30,  15640.0,  4564295.78,  3173412.41,   243765.26),
    9:  (420, 35, 109490.0, 21576403.98, 13656519.59,  5476158.69),
    10: (240, 20,  49480.0,  9566175.55,  6702926.27,  1633298.41),
}

MORT_BE_SENSITIVITY = {0.75: 352224.81, 0.85: 108809.94, 1.00: -255045.47}
LAPSE_BE_SENSITIVITY = {0.5: 110995.14, 1.0: 108809.94, 2.0: 99649.28}
DECLINE_SENSITIVITY = {                      # d -> (net_cf, premium income)
    0.00: (5550691.22, 19670798.49),
    0.05: (4789398.01, 17333567.38),
    0.20: (2919193.21, 11517624.04),
    0.40: (1258323.02,  6188656.20),
}

CHECKS = {
    "check_pols_roll_fwd", "check_lapse_pool", "check_pols_payer", "check_prem_level",
    "check_decline_timing", "check_waiver_reset", "check_net_cf",
}
CHECKS_WITH_RESID = {
    "check_pols_roll_fwd", "check_lapse_pool", "check_pols_payer", "check_prem_level",
    "check_net_cf",
}

# The scalar assumptions the notes tabulate; every one of them [std].
STD_SCALARS = {
    "mort_be_factor": 0.85, "lapse_be_factor": 1.0, "prem_int_rate": 0.025,
    "renewal_decline_base": 0.20, "renewal_decline_beta": 0.0,
    "renewal_decline_max": 0.40, "expense_acq": 120000.0, "expense_maint": 2000.0,
    "expense_claim": 300000.0, "inflation_rate": 0.02, "comm_init_rate": 0.60,
    "comm_renewal_rate": 0.03, "comm_new_term_rate": 0.0, "accel_cap": 50000000.0,
    "accel_full_limit": 10000000.0, "accel_share_max": 0.5, "accel_take_up": 0.10,
    "wop_inc_rate": 0.0008, "wop_rec_rate": 0.0, "reinstate_rate": 0.10,
}

# The diagnostic qbar values the notes publish as "checkable from the shipped table".
QBAR_DIAGNOSTICS = {
    ("M", 40, 20): 0.00152337, ("F", 40, 20): 0.00077569, ("M", 30, 20): 0.00070037,
    ("M", 65, 15): 0.01348403, ("F", 45, 35): 0.00370477, ("M", 19, 30): 0.00053910,
    ("M", 55, 20): 0.00655454,
}

# The three 예정 경험사망률 rates per sex that every 상품요약서 must print, and which the
# shipped Makeham law is fitted to exactly.
SOURCED_ANCHORS = {
    ("M", 20): 0.000280, ("M", 40): 0.000650, ("M", 60): 0.003390,
    ("F", 20): 0.000200, ("F", 40): 0.000430, ("F", 60): 0.001390,
}


def _reread(suffix):
    """A private copy of the model, for tests that move a Reference."""
    return mx.read_model(MODEL_DIR, name="Term_KR_S_" + suffix)


def _totals(projection):
    """(premiums, all benefit outgo, net_cf) summed over a projection's result_cf()."""
    df = projection.result_cf()
    claims = df[[c for c in df.columns if c.startswith("claims_")]].sum().sum()
    return df["premiums"].sum(), claims, df["net_cf"].sum()


# ---------------------------------------------------------------------------
# The worked example — the decrement basis


@pytest.mark.parametrize("y", sorted(WORKED_EXAMPLE_BASIS))
def test_worked_example_decrement_basis_row(kr_term_anchor, y):
    """Every cell of the notes' twenty-row decrement basis table, at its own precision.

    One row per **policy year**, because that is the unit the rates are published in: the
    annual table rate and the annual 적용해지율 are the sourced quantities and the monthly
    decrements beside them are their conversions.  Every won in the cash flow statement is
    built from this table, so a drift in any one of its six columns would move the whole
    statement without any single printed figure obviously being wrong.

    The row is read at ``t = 12 (y - 1)``, the first month of the policy year, and the
    rates are asserted to hold for **every** month of it: 보험나이 increments on the
    계약해당일 [S2 제22조], so a within-year drift would mean the model had invented an age
    the contract does not recognize.
    """
    age, q_tab, q, q_mth, w, w_mth, pols = WORKED_EXAMPLE_BASIS[y]
    a = kr_term_anchor
    t0 = 12 * (y - 1)
    assert a.policy_year(t0) == y
    assert a.age(t0) == age
    assert a.mort_rate_at_age(age) == pytest.approx(q_tab, abs=RATE)
    assert a.mort_rate(t0) == pytest.approx(q, abs=RATE)
    assert a.mort_rate_mth(t0) == pytest.approx(q_mth, abs=INFORCE)
    assert a.lapse_rate(t0) == pytest.approx(w, abs=INFORCE)
    assert a.lapse_rate_mth(t0) == pytest.approx(w_mth, abs=INFORCE)
    assert a.pols_if(t0) == pytest.approx(pols, abs=INFORCE)
    for t in range(t0, t0 + 12):
        assert a.age(t) == age
        assert a.policy_year(t) == y
        assert a.mort_rate(t) == pytest.approx(q, abs=RATE)
        assert a.lapse_rate(t) == pytest.approx(w, abs=INFORCE)


def test_the_monthly_decrements_compound_back_to_the_annual_ones(kr_term_anchor):
    """Twelve monthly exits leave exactly the in-force one annual exit leaves.

    This is the statement the whole conversion rests on, and it is checkable in two
    directions.  Term by term, ``1 - (1 - q^m)^12 == q`` for both decrements, because the
    monthly rate is defined as the uniform-force conversion and nothing else.  And end to
    end, ``pols_if`` at each 계약해당일 reproduces the annual-grid model's own in-force to
    the last bit — :data:`ANNIVERSARY_INFORCE` carries four of those values as the annual
    model printed them.  So the monthly step re-times the **exposure** inside the year,
    which is what moves premium income and the mortality cost, and leaves the survivorship
    the sourced annual rates imply exactly where it was.

    A model that divided the annual rates by twelve instead of compounding would pass
    neither leg, and would understate the year's total decrement by about half a per cent
    of itself at the first-year lapse rate.
    """
    a = kr_term_anchor
    for t in (0, 11, 12, 119, 239):
        assert a.mort_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - a.mort_rate(t)) ** (1.0 / 12.0), rel=1e-15)
        assert a.lapse_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - a.lapse_rate(t)) ** (1.0 / 12.0), rel=1e-15)
        assert 1.0 - (1.0 - a.mort_rate_mth(t)) ** 12 == pytest.approx(
            a.mort_rate(t), rel=1e-14)
        assert 1.0 - (1.0 - a.lapse_rate_mth(t)) ** 12 == pytest.approx(
            a.lapse_rate(t), rel=1e-14)
        assert a.mort_rate_mth(t) < a.mort_rate(t)
        assert a.lapse_rate_mth(t) < a.lapse_rate(t)
    for t, expected in ANNIVERSARY_INFORCE.items():
        assert a.pols_if(t) == pytest.approx(expected, rel=1e-13), t
    assert a.pols_maturity(a.proj_len() - 1) == pytest.approx(
        POLS_MATURITY_LAST, abs=INFORCE)


def test_worked_example_the_lapse_curve_is_the_prescribed_shape(term_life,
                                                               kr_term_anchor):
    """w(t) = 0.046 (0.001/0.046)^(t/19) on the 0-based t, from three disclosed endpoints.

    The endpoints are published 적용해지율 figures and the log-linear interpolation between
    them is the 계리가정 가이드라인's 원칙모형 for 무·저해지 business, so the whole curve is
    checkable rather than chosen — which is unique in this repository.  The file therefore
    ships three rows, not a fitted curve: a CSV holding the curve would hide which two
    numbers are sourced.
    """
    table = term_life.Data.lapse_table()
    assert list(table.index) == ["in_payment_start", "in_payment_end", "post_payment"]
    assert float(table.loc["in_payment_start", "lapse_rate"]) == 0.046
    assert float(table.loc["in_payment_end", "lapse_rate"]) == 0.001
    assert float(table.loc["post_payment", "lapse_rate"]) == 0.008
    assert table["provenance"].notna().all()

    a = kr_term_anchor
    assert a.lapse_be_factor == 1.0
    assert a.pay_term() == 20 == a.proj_years() and a.proj_len() == 240
    for t in range(240):
        assert a.lapse_rate(t) == pytest.approx(
            0.046 * (0.001 / 0.046) ** ((t // 12) / 19.0), rel=1e-13)
    rates = [a.lapse_rate(12 * y) for y in range(20)]
    assert rates[0] == pytest.approx(0.046, rel=1e-14)
    assert rates[-1] == pytest.approx(0.001, rel=1e-14)
    assert rates == sorted(rates, reverse=True) and 0.008 not in rates
    # The two means the notes quote for this cell: the flat mean of the twenty annual
    # rates, and the exposure-weighted mean taken over the 240 months the model steps.
    assert sum(rates) / 20.0 == pytest.approx(0.012379, abs=5e-7)
    assert (sum(a.pols_if(t) * a.lapse_rate(t) for t in range(240))
            / sum(a.pols_if(t) for t in range(240))) == pytest.approx(
                0.013332, abs=5e-7)


# ---------------------------------------------------------------------------
# The worked example — the cash flow statement


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF) + sorted(MILESTONE_CF))
def test_worked_example_cash_flow_row(kr_term_anchor, t):
    """Every cell of the notes' first-year and milestone statements, off cells and frame.

    Both, because a column construction error would otherwise hide behind correct cells and
    a cells error behind a correct frame.  The four columns the notes omit from the printed
    table are asserted here too: they are published columns whose zeros the notes state
    rather than imply.
    """
    a = kr_term_anchor
    expected_row = MILESTONE_CF[t] if t in MILESTONE_CF else WORKED_EXAMPLE_CF[t]
    row = a.result_cf().loc[t]
    cells = (a.pols_if(t), a.premiums(t), a.claims(t, "DEATH"), a.claim_expenses(t),
             a.expenses(t), a.commissions(t), a.net_cf(t))
    columns = ("pols_if", "premiums", "claims_death", "claim_expenses", "expenses",
               "commissions", "net_cf")
    for got, column, expected, tol in zip(
            cells, columns, expected_row, (INFORCE,) + (WON,) * 6):
        assert got == pytest.approx(expected, abs=tol), column
        assert row[column] == pytest.approx(expected, abs=tol), column
    for zero in ("claims_acc_death", "claims_accel", "claims_maturity", "claims_lapse"):
        assert row[zero] == 0.0, f"{zero} is not zero at t={t}"


def test_worked_example_assumption_table(kr_term_anchor):
    """"Every assumption value the cell uses", asserted off the model rather than described.

    The premium half of the notes' table is **sourced** — 15,080 won a month appears
    independently in the carrier's 상품요약서 grid and in the cross-carrier disclosure,
    agreeing to the won — and the decrement half is a standardization: q(t) = 0.85 x c_q x
    q_x^tab, with c_q = 1 on a 표준체 point.  That asymmetry is the shape of every Korean
    product document here, so both halves are pinned, and the decomposition is asserted
    rather than only the product: a model that folded ``mort_be_factor`` into the shipped
    table would reproduce every golden and would then move the premium scale with it.
    """
    a = kr_term_anchor
    assert (a.sex(), a.age_at_entry(), a.renewal_type()) == ("M", 40, "bi_gaengsin")
    assert (a.rate_class(), a.maturity_form()) == ("standard", "pure")
    assert (a.policy_term(), a.pay_term(), a.proj_years()) == (20, 20, 20)
    assert a.proj_len() == 240 and len(a.result_cf()) == 240
    assert a.sum_assured() == 100000000.0 and a.contract_boundary() == "ceiling"
    assert (a.acc_death(), a.waiver(), a.accel(), a.reinstatement()) == (
        False, False, False, False)
    assert a.prem_rate_mth(0) == 15080.0 and a.class_prem_ratio() == 1.0
    assert a.pay_factor(1) == 1.0                 # k is the 1-based cycle label
    assert a.premium_mth_pp(0) == 15080.0 and a.prem_pp(0) == 180960.0
    assert a.mort_be_factor == 0.85 and a.class_mort_ratio() == 1.0
    assert a.mort_rate_at_age(40) == 0.000650     # a disclosed anchor, to the digit
    for y in sorted(WORKED_EXAMPLE_BASIS):
        t = 12 * (y - 1)
        assert a.mort_rate_base(t) == pytest.approx(
            a.mort_rate_at_age(a.age(t)), rel=1e-14)
        assert a.mort_rate(t) == pytest.approx(
            0.85 * a.mort_rate_at_age(a.age(t)), rel=1e-14)
    for cells in (a.renewal_decline_rate, a.wop_waived_frac, a.accel_share,
                  a.pols_reinstate):
        assert all(cells(t) == 0.0 for t in range(240)), cells


def test_worked_example_full_precision_values(kr_term_anchor):
    """The fifteen full-float64 values the notes print beneath the rounded statement.

    They exist so that a reader reconciling to the model has something exact to reconcile
    to, which makes them a promise about the arithmetic and not only about the display.
    """
    a = kr_term_anchor
    got = {
        "pols_if(1)": a.pols_if(1), "pols_if(12)": a.pols_if(12),
        "pols_if(120)": a.pols_if(120), "pols_if(239)": a.pols_if(239),
        "premiums(1)": a.premiums(1), "claims_death(0)": a.claims(0, "DEATH"),
        "claim_expenses(0)": a.claim_expenses(0), "expenses(0)": a.expenses(0),
        "commissions(0)": a.commissions(0), "net_cf(0)": a.net_cf(0),
        "net_cf(1)": a.net_cf(1), "net_cf(12)": a.net_cf(12),
        "net_cf(120)": a.net_cf(120), "net_cf(239)": a.net_cf(239),
        "mort_rate_mth(0)": a.mort_rate_mth(0),
        "lapse_rate_mth(0)": a.lapse_rate_mth(0),
    }
    for name, expected in FULL_PRECISION.items():
        assert got[name] == pytest.approx(expected, rel=1e-14, abs=1e-9), name
    assert a.pols_if(240) == 0.0
    assert all(a.premium_mth_pp(t) == 15080.0 for t in range(240))
    assert all(a.prem_pp(t) == 180960.0 for t in range(240))


# ---------------------------------------------------------------------------
# The worked example — the hand traces


def test_worked_example_first_period_trace(kr_term_anchor):
    """The notes' t = 0 hand trace, line by line: the acquisition strain.

    The first **month's** outgo is 235,195.15 won against 15,080.00 of premium, and the
    acquisition charge alone — 120,000 of expense plus 108,576 of commission — is 15.2
    times the month's premium.  That ratio is the strain the protection shape starts from,
    and it is the number the monthly grid exists to show: an annual step netted the same
    charge against a whole year's premium and printed 1.26, which is a real quantity about
    a year and not about the cash flow that actually happens at issue.

    The initial commission is nonetheless computed on the **annualized** premium, 60% of
    ``P_a``, because that is the unit a Korean commission scale is written in [REG-R29].
    """
    a = kr_term_anchor
    assert a.pols_if_init() == 1.0 and a.pols_if(0) == 1.0
    assert a.prem_payable(0) == 1.0 and a.wop_waived_frac(0) == 0.0
    assert a.pols_payer(0) == 1.0
    assert a.premiums(0) == pytest.approx(15080.00, abs=WON)
    assert a.mort_rate_mth(0) == pytest.approx(
        1.0 - (1.0 - 0.0005525) ** (1.0 / 12.0), rel=1e-15)
    assert a.pols_death(0) == pytest.approx(a.mort_rate_mth(0), rel=1e-14)
    assert a.claims(0, "DEATH") == pytest.approx(
        100000000.0 * (1 - 0.0) * a.mort_rate_mth(0), rel=1e-14)
    assert a.claim_expenses(0) == pytest.approx(
        300000.0 * a.mort_rate_mth(0), rel=1e-14)
    assert a.expenses(0) == pytest.approx(120000.0 + 2000.0 * 1.02 ** 0, abs=WON)
    assert a.comm_init_pp() == pytest.approx(0.60 * 180960.0, abs=WON)
    assert a.net_cf(0) == pytest.approx(
        15080.00 - 4605.332987672738 - 13.815998963018217 - 122000.00 - 108576.00,
        abs=1e-9)
    outgo = a.claims(0) + a.claim_expenses(0) + a.expenses(0) + a.commissions(0)
    assert outgo == pytest.approx(235195.15, abs=WON)
    assert (120000.0 + 108576.0) / a.premiums(0) == pytest.approx(15.158, abs=5e-4)


def test_worked_example_first_period_roll_forward(kr_term_anchor):
    """The notes' t = 0 roll-forward, in the processing order and no other.

    After the month's mortality ``1 x (1 - q^m(0))``; then ``w^m(0)`` on the survivors of
    it, giving a lapse of 0.0039164302 and l(1) = 0.9960375164.  d(0) = 0 on a 비갱신형
    point, and neither a reinstatement nor a maturity moves the month.

    The year closes on the annual number: twelve of these months leave
    ``l(12) = 0.953472915``, which is the annual grid's own ``l(1)`` to the last bit.
    """
    a = kr_term_anchor
    qm, wm = a.mort_rate_mth(0), a.lapse_rate_mth(0)
    assert a.pols_if_at(0, "BEF_DECR") == 1.0
    assert a.pols_if_at(0, "BEF_LAPSE") == pytest.approx(1.0 - qm, rel=1e-14)
    assert a.pols_lapse(0) == pytest.approx(0.003916430249737208, rel=1e-12)
    assert a.pols_if_at(0, "BEF_DECLINE") == pytest.approx(
        (1.0 - qm) * (1.0 - wm), rel=1e-14)
    assert a.renewal_decline_rate(0) == 0.0
    assert a.pols_if_at(0, "AFT_DECR") == a.pols_if_at(0, "BEF_DECLINE")
    assert a.pols_reinstate(0) == 0.0 and a.pols_maturity(0) == 0.0
    assert a.pols_if(1) == pytest.approx(0.9960375164203861, rel=1e-15)
    assert a.pols_if(12) == pytest.approx(0.953472915, rel=1e-14)


def test_worked_example_second_month_and_the_turn_of_the_policy_year(kr_term_anchor):
    """The notes' t = 1 and t = 12 traces: an ordinary month, then the anniversary.

    ``expense_acq`` and ``comm_init_pp`` are ``t = 0`` only, so ``t = 1`` is the first
    month of the steady state: one month's premium, one month's decrements, one month's
    maintenance expense and **no commission at all**.  The renewal commission starts at
    ``t = 12`` and not before — it is a policy-year-2 charge, which on a monthly grid is a
    date rather than a convention — and ``t = 12`` is also where the inflation factor makes
    its first step and where the attained 보험나이 turns 41.  Three things changing on one
    row is what makes it the row worth tracing.
    """
    a = kr_term_anchor
    assert a.premiums(1) == pytest.approx(15080.0 * 0.9960375164203861, rel=1e-14)
    assert a.pols_death(1) == pytest.approx(4.5870844313304316e-05, rel=1e-12)
    assert a.claims(1, "DEATH") == pytest.approx(4587.08443133, abs=1e-6)
    assert a.claim_expenses(1) == pytest.approx(13.76125329, abs=1e-7)
    assert a.inflation_factor(1) == 1.0
    assert a.expenses(1) == pytest.approx(2000.0 * 0.9960375164203861, rel=1e-14)
    assert a.commissions(1) == 0.0
    assert a.net_cf(1) == pytest.approx(8427.32503015, abs=1e-6)
    assert a.pols_if_at(1, "BEF_LAPSE") == pytest.approx(0.99599164557607, abs=5e-13)
    assert a.pols_lapse(1) == pytest.approx(0.00390091145918, abs=5e-13)
    assert a.pols_if(2) == pytest.approx(0.9920907341168909, rel=1e-15)
    assert all(a.commissions(t) == 0.0 for t in range(1, 12))

    assert a.age(11) == 40 and a.age(12) == 41
    assert a.policy_year(11) == 1 and a.policy_year(12) == 2
    assert a.premiums(12) == pytest.approx(15080.0 * 0.953472915, rel=1e-14)
    assert a.pols_death(12) == pytest.approx(4.695409394967e-05, rel=1e-12)
    assert a.claims(12, "DEATH") == pytest.approx(4695.40939497, abs=1e-6)
    assert a.claim_expenses(12) == pytest.approx(14.08622818, abs=1e-7)
    assert a.inflation_factor(12) == pytest.approx(1.02, rel=1e-15)
    assert a.expenses(12) == pytest.approx(2000.0 * 1.02 * 0.953472915, rel=1e-14)
    assert a.commissions(12) == pytest.approx(0.03 * a.premiums(12), rel=1e-14)
    assert a.commissions(12) == pytest.approx(431.35114675, abs=1e-6)
    assert a.net_cf(12) == pytest.approx(7292.44004170, abs=1e-6)


def test_worked_example_last_period_trace_and_the_maturity_that_pays_nothing(
        kr_term_anchor):
    """The notes' last-period trace, where the 순수보장형 pays nothing at maturity.

    w(239) = 0.001 annual exactly — the disclosed convergence point, reached at 납입완료,
    held level through the whole of the twentieth policy year — and ``pols_maturity(239)``
    then removes the **entire** surviving cohort, 0.7582424843 of it, for no benefit at
    all.  That count is the annual-grid model's own, to the last bit: the monthly step
    re-times the exposure and leaves the survivorship where the annual rates put it.
    l(240) = 0 exactly one step past the frame, which is what makes the roll-forward close
    in the last month rather than leaving a residual a model with no maturity term would
    carry.

    ``cum_prem_pp(239)`` is 3,619,200 won — 240 monthly premiums of 15,080 — which is what a
    만기환급형 twin would hand back, and is exactly what twenty annualized premiums came to
    on the annual grid.  The amount is not a grid quantity; only its timing was.
    """
    a = kr_term_anchor
    last = a.proj_len() - 1
    assert last == 239
    assert a.lapse_rate(239) == pytest.approx(0.001, rel=1e-14)
    assert a.premiums(239) == pytest.approx(11437.75505767, abs=1e-6)
    assert a.pols_death(239) == pytest.approx(0.00016611537844, abs=5e-13)
    assert a.claims(239, "DEATH") == pytest.approx(16611.53784435, abs=1e-6)
    assert a.claim_expenses(239) == pytest.approx(49.83461353, abs=1e-7)
    assert a.expenses(239) == pytest.approx(
        2000.0 * 1.02 ** 19 * a.pols_if(239), rel=1e-13)
    assert a.commissions(239) == pytest.approx(343.13265173, abs=1e-6)
    assert a.net_cf(239) == pytest.approx(-7776.65049713, abs=1e-6)
    assert a.pols_if_at(239, "BEF_LAPSE") == pytest.approx(0.75830570542171, abs=5e-13)
    assert a.pols_if_at(239, "AFT_DECR") == pytest.approx(0.75824248429801, abs=5e-13)
    assert a.pols_maturity(239) == pytest.approx(POLS_MATURITY_LAST, abs=INFORCE)
    assert a.pols_maturity(239) == a.pols_if_at(239, "AFT_DECR") + a.pols_reinstate(239)
    assert a.maturity_form() == "pure" and a.claims(239, "MATURITY") == 0.0
    assert a.cum_prem_pp(239) == 3619200.0       # what a rop point would have paid
    assert a.pols_if(240) == 0.0
    assert a.check_pols_roll_fwd_resid(239) == pytest.approx(0.0, abs=1e-15)
    assert all(a.pols_maturity(t) == 0.0 for t in range(239))


# ---------------------------------------------------------------------------
# The worked example — totals, decomposition and shape


def test_worked_example_totals(kr_term_anchor):
    """The notes' undiscounted twenty-year totals, column by column.

    Including the exposure column, which is what the per-policy expense and commission
    figures are proportional to and so the one total a reader can re-derive the others from
    by hand.
    """
    df = kr_term_anchor.result_cf()
    assert df["pols_if"].sum() == pytest.approx(TOTAL_POLS_IF, abs=INFORCE)
    assert df["premiums"].sum() == pytest.approx(TOTAL_PREMIUMS, abs=WON)
    assert df["claims_death"].sum() == pytest.approx(TOTAL_CLAIMS_DEATH, abs=WON)
    assert df["claim_expenses"].sum() == pytest.approx(TOTAL_CLAIM_EXPENSES, abs=WON)
    assert df["expenses"].sum() == pytest.approx(TOTAL_EXPENSES, abs=WON)
    assert df["commissions"].sum() == pytest.approx(TOTAL_COMMISSIONS, abs=WON)
    assert df["net_cf"].sum() == pytest.approx(TOTAL_NET_CF, abs=WON)
    for zero in ("claims_acc_death", "claims_accel", "claims_maturity", "claims_lapse"):
        assert df[zero].sum() == 0.0


def test_worked_example_cohort_decomposition(kr_term_anchor):
    """Deaths, lapses, maturities and the residual in force sum to one policy, exactly.

    The roll-forward read as a cohort decomposition over all 240 months: of a hundred
    policies issued, 2.06 die, 22.11 lapse and 75.82 reach the end of the twenty years,
    with no renewal decline on this point at all.  A model losing or creating lives fails
    here even where every single month's residual is inside tolerance, because the errors
    accumulate — and 240 chances to accumulate is twelve times what the annual grid gave.

    The split moves slightly against the annual grid and in a direction with a reason: a
    monthly step exposes each life to lapse before it has served a whole year of mortality,
    so a little more of the cohort leaves by lapse and a little less by death, while the
    total reaching maturity is unchanged to the last bit.
    """
    a = kr_term_anchor
    deaths = sum(a.pols_death(t) for t in range(240))
    lapses = sum(a.pols_lapse(t) for t in range(240))
    declines = sum(a.pols_decline(t) for t in range(240))
    maturities = sum(a.pols_maturity(t) for t in range(240))
    reinstates = sum(a.pols_reinstate(t) for t in range(240))
    assert deaths == pytest.approx(TOTAL_POLS_DEATH, abs=INFORCE)
    assert lapses == pytest.approx(TOTAL_POLS_LAPSE, abs=INFORCE)
    assert declines == 0.0 and reinstates == 0.0
    assert maturities == pytest.approx(POLS_MATURITY_LAST, abs=INFORCE)
    assert deaths + lapses + declines + maturities + a.pols_if(240) == pytest.approx(
        1.0, abs=1e-13)


def test_worked_example_reading_the_shape(kr_term_anchor):
    """The cumulative path the notes describe: strain, crossing, peak at t = 155, giveback.

    Every part of the protection shape is mechanical and the notes assert each part with a
    number, so each is pinned: the strain of -220,115.15 in the first **month**, the
    crossing back through zero at t = 30 — two and a half years, which is what it actually
    takes to earn back an acquisition charge of fifteen months' premium — the peak of
    +436,338.80 at t = 155, and the 327,528.85 given back over the last seven years, 75% of
    the peak, as the level premium falls behind a table rate that has multiplied by 4.75
    between 보험나이 40 and 59.

    The monthly grid moves two of those numbers in ways worth naming.  The crossing is a
    **date** now rather than a year label, and the peak sits inside policy year 13 rather
    than on its anniversary: the turn happens when the month's premium stops covering the
    month's mortality, which is a month and not a year.
    """
    a = kr_term_anchor
    df = a.result_cf()
    cum = df["net_cf"].cumsum()
    assert cum.loc[0] == pytest.approx(-220115.15, abs=WON)
    assert cum.loc[1] == pytest.approx(-211687.82, abs=WON)
    assert cum.loc[12] == pytest.approx(-121937.10, abs=WON)
    assert cum.loc[29] < 0.0 < cum.loc[30]
    assert cum.loc[30] == pytest.approx(2934.05, abs=WON)
    assert cum.idxmax() == 155
    assert a.policy_year(155) == 13
    assert cum.loc[155] == pytest.approx(436338.80, abs=WON)
    assert cum.loc[155] - cum.loc[239] == pytest.approx(327528.85, abs=WON)
    assert (cum.loc[155] - cum.loc[239]) / cum.loc[155] == pytest.approx(0.751, abs=5e-4)
    assert a.net_cf(155) > 0.0 > a.net_cf(156)
    assert all(a.net_cf(t) < 0.0 for t in range(156, 240))
    assert a.mort_rate_at_age(59) / a.mort_rate_at_age(40) == pytest.approx(
        4.751, abs=5e-4)
    assert a.prem_pp(239) == a.prem_pp(0)
    # The answer is a difference of large numbers: premium is 1.44x death claims.
    assert df["premiums"].sum() / df["claims_death"].sum() == pytest.approx(
        1.437, abs=5e-4)
    loading = df["expenses"].sum() + df["commissions"].sum()
    assert loading / df["premiums"].sum() == pytest.approx(0.2652, abs=5e-5)
    assert (122000.0 + 108576.0) / loading == pytest.approx(0.293, abs=5e-4)


@pytest.mark.parametrize("point_id", sorted(POINT_SUMMARY))
def test_the_shipped_model_point_summary_table(term_life, point_id):
    """The notes' ten-row summary: horizon, issue premium, premium, claims and net_cf.

    The table is the worked example's coverage statement — both sexes, both renewal
    structures, both boundary readings, both maturity forms, 전기납 and shortened pay,
    년만기 and 세만기, all four rate classes and every optional module — so a change to any
    of them shows up as one failing row rather than as a moved total somewhere.
    """
    proj_len, proj_years, prem_mth, premiums, claims, net_cf = POINT_SUMMARY[point_id]
    p = term_life.Projection[point_id]
    assert p.proj_len() == proj_len
    assert p.proj_years() == proj_years
    assert p.proj_len() == 12 * p.proj_years()
    assert p.premium_mth_pp(0) == prem_mth
    got_prem, got_claims, got_net = _totals(p)
    assert got_prem == pytest.approx(premiums, abs=WON)
    assert got_claims == pytest.approx(claims, abs=WON)
    assert got_net == pytest.approx(net_cf, abs=WON)


def test_the_maturity_form_point_pays_back_the_premiums_it_collected(term_life):
    """Model point 6: 8,016,046.20 of ``claims_maturity`` beside 724,366.05 of death claims.

    A 만기환급형 hands back 100% of 「이미 납입한 주계약 보험료」, so on an undiscounted gross
    projection it **must** show a loss: the contract is financed out of investment income
    this model never credits.  The loss is evidence that an undiscounted stream is the
    wrong lens for a savings-shaped contract, which is why the savings chassis is
    ``WholeLife_KR_S`` and not this one.
    """
    p = term_life.Projection[6]
    assert p.maturity_form() == "rop"
    df = p.result_cf()
    n = p.proj_len()
    assert df["claims_maturity"].sum() == pytest.approx(8016046.20, abs=WON)
    assert df["claims_death"].sum() == pytest.approx(724366.05, abs=WON)
    assert (df["claims_maturity"][:n - 1] == 0.0).all()
    assert p.claims(n - 1, "MATURITY") == pytest.approx(
        p.cum_prem_pp(n - 1) * p.pols_maturity(n - 1), rel=1e-14)
    # The refund is the 240 **monthly** premiums actually scheduled, which is the same
    # amount twenty annualized premiums came to: the grid moved the timing, not the sum.
    assert p.cum_prem_pp(n - 1) == pytest.approx(
        sum(p.premium_mth_pp(s) for s in range(n)), rel=1e-14)
    assert p.cum_prem_pp(n - 1) == pytest.approx(
        12.0 * sum(p.premium_mth_pp(12 * y) for y in range(p.proj_years())), rel=1e-14)
    assert df["net_cf"].sum() < 0.0


def test_the_accidental_uplift_point_prints_the_split_the_notes_quote(term_life):
    """Model point 10: acc_mort_share 0.1236207830 / 0.0871551347 / 0.0536694127.

    472,623.02 won of ``claims_acc_death`` against 6,230,303.25 of ``claims_death`` is a
    7.6% uplift in claim cost for a **doubled** benefit, which is the order of magnitude
    that lets a carrier bundle 재해사망 into a product 형 rather than price it as a rider.
    The share is taken on the 표준체 **table** basis, so neither the class relativity nor the
    best-estimate factor disturbs it — neither has anything to say about cause of death.
    It is also **level within a policy year**, because it is a ratio of two annual table
    rates read at one attained age: the monthly grid splits a monthly decrement by an
    annual share, which is right, and a model that converted the share as though it were a
    probability would be converting a ratio.
    """
    p = term_life.Projection[10]
    assert p.acc_death() is True and p.rate_class() == "preferred"
    for y, share in ((1, 0.1236207830), (10, 0.0871551347), (20, 0.0536694127)):
        t = 12 * (y - 1)
        assert p.acc_mort_share(t) == pytest.approx(share, abs=INFORCE)
        assert p.acc_mort_share(t) == pytest.approx(
            p.acc_mort_rate_at_age(p.age(t)) / p.mort_rate_at_age(p.age(t)), rel=1e-14)
        assert all(p.acc_mort_share(s) == pytest.approx(share, abs=INFORCE)
                   for s in range(t, t + 12))
    df = p.result_cf()
    assert df["claims_acc_death"].sum() == pytest.approx(472623.02, abs=WON)
    assert df["claims_death"].sum() == pytest.approx(6230303.25, abs=WON)
    assert df["claims_acc_death"].sum() / df["claims_death"].sum() == pytest.approx(
        0.0759, abs=5e-4)


# ---------------------------------------------------------------------------
# The 갱신형 panel of the worked example


def test_the_renewal_ladder_is_read_off_published_cells_with_no_extension(term_life):
    """9,000 -> 21,000 -> 56,000 -> 201,000 a month, and the 2.33 / 2.67 / 3.59 jumps.

    This is the mandatory 예상 갱신보험료 예시 reproduced to the won, and the issue cell
    appears three times independently — in the carrier's 상품요약서, in the cross-carrier
    disclosure and in the projection itself.  A renewable term at attained-age rates
    converges on term-cost pricing, and the accelerating jump is what that convergence looks
    like; it is why carriers stop renewing at 보험나이 80.
    """
    p = term_life.Projection[3]
    assert p.renewal_type() == "gaengsin"
    assert p.policy_term() == 10 and p.renew_ceiling() == 80
    tbl = term_life.Data.prem_rate_table()
    for k, t, entry_age, p_m, p_a in RENEWAL_LADDER:
        assert p.term_index(t) == k
        assert p.term_start_age(k) == entry_age and p.term_len(k) == 10
        assert ("pure", "M", entry_age, 10) in tbl.index    # published, not extended
        assert p.prem_rate_mth(t) == p_m and p.premium_mth_pp(t) == p_m
        assert p.prem_pp(t) == p_a
    assert [round(p.prem_pp(t) / p.prem_pp(0), 2) for _, t, *_ in RENEWAL_LADDER] == [
        1.00, 2.33, 6.22, 22.33]
    jumps = [round(p.prem_pp(t + 1) / p.prem_pp(t), 2) for t in (119, 239, 359)]
    assert jumps == [2.33, 2.67, 3.59] == sorted(jumps)
    # The premium is level for the whole 120 months of a cycle and steps once, on the
    # 계약해당일 the 갱신 falls on -- which is a date the monthly grid can state.
    for _, t, _, p_m, _ in RENEWAL_LADDER:
        assert all(p.premium_mth_pp(s) == p_m for s in range(t, t + 120))


@pytest.mark.parametrize("t", sorted(GAENGSIN_BOUNDARY_ROWS))
def test_the_gaengsin_boundary_rows(term_life, t):
    """The notes' eight-row boundary table on model point 3, cell by cell.

    Three rows per boundary — the period before, the boundary itself and the repriced period
    after — plus the last period, where cover ends at the ceiling rather than renewing.
    Between them they pin the decline rate, the exits it produces, the waiver reset and the
    saw-tooth, which are the four things a 갱신형 model gets wrong independently.
    """
    pols, decline_rate, declines, waived, net_cf = GAENGSIN_BOUNDARY_ROWS[t]
    p = term_life.Projection[3]
    assert p.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert p.renewal_decline_rate(t) == pytest.approx(decline_rate, abs=1e-15)
    assert p.pols_decline(t) == pytest.approx(declines, abs=INFORCE)
    assert p.wop_waived_frac(t) == pytest.approx(waived, abs=INFORCE)
    assert p.net_cf(t) == pytest.approx(net_cf, abs=WON)


def test_the_gaengsin_boundary_period_trace(term_life):
    """The notes' t = 119 trace: the old premium, in the month the contract reprices.

    A boundary is now a single **month** — the last of the 120 in a cycle — and premium
    income in it is collected at the **old** premium, the repricing taking effect at
    ``t = 120`` and not before.  Then the roll-forward in the processing order — mortality,
    ordinary lapse, and the renewal decline on the survivors of both — takes l(119) from
    0.7268743823 to 0.5805175782 in one step.

    That last number is the point of the row.  The decline is a discrete election on a
    single date and the monthly grid puts it on that date: 20% of the in-force leaves in
    one month against 0.0012 that lapse in the ordinary way and 0.00007 that die, so the
    three exits stand in a ratio of roughly 2200 : 18 : 1 — which is what makes calling the
    decline a lapse loading a modelling error rather than a simplification.
    """
    p = term_life.Projection[3]
    assert p.policy_year(119) == 10 and p.term_index(119) == 1
    assert p.pols_if(119) == pytest.approx(0.7268743822842945, rel=1e-14)
    assert p.wop_waived_frac(119) == pytest.approx(WAIVED_AT_CYCLE_END, rel=1e-12)
    assert p.pols_payer(119) == pytest.approx(0.7211283695, abs=INFORCE)
    assert p.prem_pp(119) == 108000.0 and p.premium_mth_pp(119) == 9000.0
    assert p.premiums(119) == pytest.approx(6490.16, abs=WON)
    assert p.mort_rate(119) == pytest.approx(0.85 * 0.00127541, rel=1e-14)
    assert p.mort_rate_mth(119) == pytest.approx(
        1.0 - (1.0 - p.mort_rate(119)) ** (1.0 / 12.0), rel=1e-15)
    assert p.pols_death(119) == pytest.approx(0.0000656996, abs=INFORCE)
    assert p.claims(119, "DEATH") == pytest.approx(6569.96, abs=WON)
    assert p.claim_expenses(119) == pytest.approx(19.71, abs=WON)
    assert p.expenses(119) == pytest.approx(
        2000.0 * 1.02 ** 9 * p.pols_if(119), rel=1e-13)
    assert p.commissions(119) == pytest.approx(0.03 * p.premiums(119), rel=1e-14)
    assert p.net_cf(119) == pytest.approx(-2031.58, abs=WON)
    assert p.lapse_rate(119) == pytest.approx(0.0190127302, abs=INFORCE)
    assert p.lapse_rate_mth(119) == pytest.approx(0.0015983709, abs=INFORCE)
    assert p.pols_if_at(119, "BEF_LAPSE") == pytest.approx(0.7268086827, abs=INFORCE)
    assert p.pols_if_at(119, "BEF_DECLINE") == pytest.approx(0.7256469728, abs=INFORCE)
    assert p.pols_if_at(119, "AFT_DECR") == pytest.approx(0.5805175782, abs=INFORCE)
    assert p.pols_if(120) == pytest.approx(0.5805175782471496, rel=1e-14)


def test_the_gaengsin_repriced_period_trace_and_the_saw_tooth(term_life):
    """88% more premium on 20% fewer policies, then the same shape three times over.

    The crossing is the signature of a 갱신형 contract and no UK or U.S. term model in this
    repository has it.  ``net_cf`` runs -182,419.15 in the first **month**, positive from
    ``t = 1``, decays through the cycle to -2,031.58 in the boundary month, then jumps to
    +4,689.19 — and the amplitude grows at each boundary, because the premium resets to
    attained age while the in-force does not reset at all.

    The cycle totals are the same statement without the noise: -172,034.54, then
    +172,101.53, +496,178.04 and +2,422,948.18.  A contract that reprices to attained age
    every ten years earns nothing in the cycle that carries the acquisition cost and
    progressively more in each one after it, which is the whole economics of 갱신형.
    """
    p = term_life.Projection[3]
    assert p.term_index(120) == 2 and p.term_start_age(2) == 50
    assert p.prem_rate_mth(120) == 21000.0 and p.prem_pp(120) == 252000.0
    assert p.wop_waived_frac(120) == 0.0
    assert p.pols_payer(120) == pytest.approx(p.pols_if(120), rel=1e-15)
    assert p.premiums(120) == pytest.approx(12190.87, abs=WON)
    assert p.net_cf(120) == pytest.approx(4689.19, abs=WON)
    assert p.pols_if(120) < 0.80 * p.pols_if(119)
    assert p.premiums(120) / p.premiums(119) == pytest.approx(1.88, abs=5e-3)
    # The saw-tooth.
    assert p.net_cf(0) == pytest.approx(-182419.15, abs=WON)
    assert p.net_cf(1) > 0.0
    assert p.net_cf(108) == pytest.approx(-2065.00, abs=WON)
    for t in (119, 239, 359):
        assert p.net_cf(t) < 0.0 < p.net_cf(t + 1), f"boundary at {t}"
    jumps = [p.net_cf(t + 1) - p.net_cf(t) for t in (119, 239, 359)]
    assert jumps == sorted(jumps)
    df = p.result_cf()
    cycles = [df["net_cf"].iloc[120 * k:120 * (k + 1)].sum() for k in range(4)]
    assert cycles[0] == pytest.approx(GAENGSIN_FIRST_CYCLE_NET_CF, abs=WON)
    assert cycles == sorted(cycles) and cycles[0] < 0.0 < cycles[1]


def test_the_contract_boundary_is_published_both_ways_and_ruled_on_neither(term_life):
    """+2,919,193.21 to the ceiling against -181,055.18 over the cycle in force.

    Nothing retrieved settles where a Korean 갱신 falls relative to the IFRS 17 boundary —
    the repricing is of the whole 기초율 on a new product code, which argues one way, and it
    is guaranteed-issue at portfolio level, which argues the other — so the model implements
    the long reading and carries the short one as a switch.  The two do not even share a
    sign, which is why naming the convention is part of reporting the number.
    """
    p3, p4 = term_life.Projection[3], term_life.Projection[4]
    assert p3.contract_boundary() == "ceiling" and p3.proj_len() == 480
    assert p4.contract_boundary() == "current_term" and p4.proj_len() == 120
    assert (p3.proj_years(), p4.proj_years()) == (40, 10)
    assert p3.horizon_ceiling() == 40 == p4.horizon_ceiling()
    assert p4.policy_term() == 10 and p3.age(p3.proj_len() - 1) + 1 == 80
    assert p3.result_cf()["net_cf"].sum() == pytest.approx(
        GAENGSIN_TOTAL_NET_CF, abs=WON)
    assert p4.result_cf()["net_cf"].sum() == pytest.approx(CURRENT_TERM_NET_CF, abs=WON)
    assert p3.result_cf()["net_cf"].sum() * p4.result_cf()["net_cf"].sum() < 0.0
    for attr in ("sex", "age_at_entry", "renewal_type", "policy_term", "sum_assured",
                 "rate_class", "maturity_form", "waiver"):
        assert getattr(p3, attr)() == getattr(p4, attr)()


# ---------------------------------------------------------------------------
# The check_* cells and the roll-forward identities


def test_which_checks_this_model_publishes(term_life, kr_term_anchor):
    """The seven check cells, asserted **by name**, and the five that carry a residual.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared: it
    would call the six that remain, pass, and prove less than it did before.  Naming the set
    turns "every check passes" into a statement about *which* checks.
    ``check_decline_timing`` and ``check_waiver_reset`` are the two with no per-t residual,
    each being a statement about *where* a quantity is non-zero rather than about how far an
    identity misses.
    """
    published = {n for n in term_life.Projection.cells
                 if n.startswith("check_") and not n.endswith("_resid")}
    assert published == CHECKS
    resid = {n[:-len("_resid")] for n in term_life.Projection.cells
             if n.startswith("check_") and n.endswith("_resid")}
    assert resid == CHECKS_WITH_RESID
    a = kr_term_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True and isinstance(value, bool), name
    for name in sorted(CHECKS_WITH_RESID):
        residual = getattr(a, name + "_resid")
        for t in range(a.proj_len()):
            assert residual(t) == pytest.approx(0.0, abs=1e-8), f"{name}_resid({t})"


def test_the_check_tolerances_are_named_references(term_life, kr_term_anchor):
    """No bare literal tolerance: ``roll_fwd_tol`` for the ledgers, ``cash_tol`` for cash.

    The two are different quantities and must not collapse into one.  ``roll_fwd_tol``
    closes identities between cells evaluated in one expression, where the residual is a
    unit or two in the last place of a count near 1.0; ``cash_tol`` closes ``check_net_cf``,
    which re-reads won amounts of order 1e7 back out of the frame.  It must therefore be
    wider — and still far below one won, the smallest error a reader could observe.
    """
    refs = term_life.Projection.refs
    assert refs["roll_fwd_tol"] == 1e-12 and refs["cash_tol"] == 1e-6
    assert refs["roll_fwd_tol"] < refs["cash_tol"] < 1.0
    a = kr_term_anchor
    worst = max(abs(a.check_net_cf_resid(t)) for t in range(a.proj_len()))
    assert worst < refs["cash_tol"] / 100.0


def test_the_inforce_rollforward_is_the_notes_identity(term_life):
    """l(t) - l(t+1) = deaths + lapses + declines + maturities - reinstatements.

    Asserted on the four points that exercise the terms separately — the anchor, the 갱신형
    point that has declines, the 부활 point that has reinstatements and the 만기환급형 point
    whose maturity pays — because a term that is identically zero on the cell under test
    proves nothing about the term.  In force is a probability and nothing creates lives,
    except through 부활.
    """
    for point_id in (1, 3, 6, 8):
        p = term_life.Projection[point_id]
        for t in range(p.proj_len()):
            out = (p.pols_death(t) + p.pols_lapse(t) + p.pols_decline(t)
                   + p.pols_maturity(t) - p.pols_reinstate(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-13), (
                f"point {point_id}, t={t}")
            assert 0.0 <= p.pols_if(t) <= 1.0
            if not p.reinstatement():
                assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15
        assert p.check_pols_roll_fwd() is True
        assert p.pols_if(p.proj_len()) == 0.0


def test_the_decrements_are_taken_in_the_notes_processing_order(term_life):
    """Death, then ordinary lapse, then the renewal decline — steps 4, 5 and 6.

    Each timing reads the population the next decrement is taken from, which is what makes
    the decline a decrement on the survivors of lapse rather than one competing with it.
    Asserted on the 갱신형 point, where the third factor is not identically one.
    """
    p = term_life.Projection[3]
    for t in (0, 47, 119, 239, 360, 479):
        assert p.pols_if_at(t, "BEF_DECR") == p.pols_if(t)
        assert p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_if(t) * (1 - p.mort_rate_mth(t)), rel=1e-15)
        assert p.pols_if_at(t, "BEF_DECLINE") == pytest.approx(
            p.pols_if_at(t, "BEF_LAPSE") * (1 - p.lapse_rate_mth(t)), rel=1e-15)
        assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(
            p.pols_if_at(t, "BEF_DECLINE") * (1 - p.renewal_decline_rate(t)), rel=1e-15)
        assert p.pols_death(t) == pytest.approx(
            p.pols_if_at(t, "BEF_DECR") * p.mort_rate_mth(t), rel=1e-15)
        assert p.pols_lapse(t) == pytest.approx(
            p.pols_if_at(t, "BEF_LAPSE") * p.lapse_rate_mth(t), rel=1e-15)
        assert p.pols_decline(t) == pytest.approx(
            p.pols_if_at(t, "BEF_DECLINE") * p.renewal_decline_rate(t), rel=1e-15)
    # The renewal decline is the one rate that is **not** converted: it is a discrete
    # election on a single date, not a force acting through a period, so it enters at its
    # own level in the one month the boundary falls in and nowhere else.
    assert p.renewal_decline_rate(119) == 0.2 == p.renewal_decline_base
    # Both guards of ``if t < 0 or t >= proj_len()``. Neither index is on the frame — the
    # frame is t = 0 .. proj_len() - 1 and nothing in the model reads t = -1; these probe
    # the guard itself, which is what makes the cells safe to call from a window read such
    # as pols_lapse_pool's [max(0, t - 36), t - 1].
    assert p.pols_if_at(-1, "BEF_DECR") == 0.0
    assert p.pols_if_at(p.proj_len(), "BEF_DECR") == 0.0
    with pytest.raises(FormulaError):
        p.pols_if_at(0, "BEF_NOTHING")


def test_the_published_statement_adds_up(term_life):
    """``result_cf`` columns are a decomposition of ``net_cf``, not a selection from it.

    ``check_net_cf`` re-derives the ledger from the **published frame** rather than from the
    cells behind it, so the identity a reader adds up with a calculator is the identity the
    model asserts.  It is the guard against a benefit kind that exists in ``claims()`` but
    was never given a column, which would leave the statement short of the outgo it charges.
    """
    for point_id in (1, 3, 6, 7, 10):
        p = term_life.Projection[point_id]
        df = p.result_cf()
        outgo = df[["claims_death", "claims_acc_death", "claims_accel",
                    "claims_maturity", "claims_lapse", "claim_expenses",
                    "expenses", "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-8)
        assert p.check_net_cf() is True


def test_the_two_published_frames_and_the_sign_they_carry(kr_term_anchor, term_life):
    """``result_cf`` columns in order, and ``result_pols`` making a boundary legible.

    Column order is part of the published artefact — ``run.py`` prints the frames and the
    notes tabulate them — so a reordering is a documentation break even though every number
    is unchanged.  ``net_cf`` is income-positive, which is the notes' own sign as well as the
    library's, so there is no ``liability_cf`` companion.  And the renewal machinery is only
    readable next to the decrements it drives, which is why ``result_pols`` prints
    ``term_index`` and ``prem_pp`` beside ``renewal_decline_rate``: a boundary is the row
    whose decline rate is non-zero and whose premium moves on the next one.
    """
    df = kr_term_anchor.result_cf()
    assert list(df.index) == list(range(240)) and df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_acc_death", "claims_accel",
        "claims_maturity", "claims_lapse", "claim_expenses", "expenses",
        "commissions", "net_cf",
    ]
    assert df.notna().all().all()
    assert "liability_cf" not in term_life.Projection.cells
    assert kr_term_anchor.net_cf(0) < 0.0 < kr_term_anchor.net_cf(1)

    pols = term_life.Projection[3].result_pols()
    assert pols.index.name == "t" and list(pols.columns)[0] == "pols_if"
    for name in ("pols_decline", "renewal_decline_rate", "term_index", "prem_pp",
                 "pols_waived", "pols_lapse_pool"):
        assert name in pols.columns
    # Both the sourced annual rate and the monthly decrement derived from it are printed:
    # a reader checking a disclosure checks the first, a reader checking the roll-forward
    # checks the second, and publishing only one of them makes one of those unreadable.
    for name in ("mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth"):
        assert name in pols.columns
    assert (pols["mort_rate_mth"] < pols["mort_rate"]).all()
    assert (pols["lapse_rate_mth"] < pols["lapse_rate"]).all()
    boundaries = [t for t in pols.index if pols.loc[t, "renewal_decline_rate"] > 0.0]
    assert boundaries == [119, 239, 359]
    for t in boundaries:
        assert pols.loc[t + 1, "prem_pp"] > pols.loc[t, "prem_pp"]
        assert pols.loc[t + 1, "term_index"] == pols.loc[t, "term_index"] + 1


# ---------------------------------------------------------------------------
# Pitfall: the renewal decline is not lapse, and the order is not cosmetic


def test_pitfall_renewal_decline_is_not_lapse_and_the_order_is_not_cosmetic(term_life):
    """A different event, in a different month, from a different population — 99.2% of exits.

    The multiplicative roll-forward is order-invariant, so a model applying the decline
    **first** still balances its policy count to the last digit — and books 20% fewer death
    claims in the boundary month: 5,255.97 won instead of 6,569.96, with l(120) identical
    either way.  Folding the decline into w(t) is worse, because it makes the boundary
    invisible — and the monthly grid makes how bad that would be arithmetically obvious: on
    this row the decline is 0.1451293946 of 0.1463568040 total exits, because a month of
    ordinary lapse is a twelfth of a year's while the decline is the whole election.

    An annual grid put the decline at 90.7% of the year's exits, which reads like a large
    share of a mixed population.  It is not a mixed population at all: it is one date.
    """
    p = term_life.Projection[3]
    deaths, lapses, declines = BOUNDARY_EXITS
    assert p.pols_death(119) == pytest.approx(deaths, abs=INFORCE)
    assert p.pols_lapse(119) == pytest.approx(lapses, abs=INFORCE)
    assert p.pols_decline(119) == pytest.approx(declines, abs=INFORCE)
    total = p.pols_death(119) + p.pols_lapse(119) + p.pols_decline(119)
    # Three values each printed to ten decimals, so the sum carries three roundings.
    assert total == pytest.approx(sum(BOUNDARY_EXITS), abs=3 * INFORCE)
    assert p.pols_if(119) - p.pols_if(120) == pytest.approx(total, abs=1e-13)
    assert p.pols_decline(119) / total == pytest.approx(0.992, abs=5e-4)

    # The counterfactual: decline first, then mortality on the survivors of it.
    l9, q9, w9, d9 = (p.pols_if(119), p.mort_rate_mth(119), p.lapse_rate_mth(119),
                      p.renewal_decline_rate(119))
    reversed_deaths = l9 * (1 - d9) * q9
    assert reversed_deaths == pytest.approx(0.0000525597, abs=INFORCE)
    assert 100000000.0 * reversed_deaths == pytest.approx(5255.97, abs=WON)
    assert reversed_deaths == pytest.approx(0.80 * p.pols_death(119), rel=1e-12)
    assert l9 * (1 - d9) * (1 - q9) * (1 - w9) == pytest.approx(
        p.pols_if(120), rel=1e-14)         # the roll-forward cannot catch it

    # Taken after lapse, from the survivors of it, and only in a boundary month.
    assert p.pols_decline(119) == pytest.approx(
        p.pols_if_at(119, "BEF_DECLINE") * 0.20, rel=1e-14)
    assert p.check_decline_timing() is True
    for t in range(p.proj_len()):
        boundary = (t + 1) % 120 == 0 and t < p.proj_len() - 1
        assert (p.renewal_decline_rate(t) > 0.0) is boundary, t
        assert (p.pols_decline(t) > 0.0) is boundary, t
    # w absorbs nothing: the annual vector steps down at the 계약해당일 and is flat inside
    # the year, so the boundary month carries the same ordinary lapse as the eleven before.
    assert p.lapse_rate(120) < p.lapse_rate(119) == p.lapse_rate(108)

    # A declined renewal is an expiry: nothing is paid, and nobody is re-counted.
    assert p.claims(119, "LAPSE") == 0.0
    assert p.pols_if(120) == pytest.approx(
        p.pols_if_at(119, "BEF_DECLINE") * 0.80, rel=1e-14)
    assert p.pols_lapse(120) == pytest.approx(
        p.pols_if_at(120, "BEF_LAPSE") * p.lapse_rate_mth(120), rel=1e-14)
    assert p.pols_lapse(120) < p.pols_decline(119)
    assert p.renewal_decline_rate(p.proj_len() - 1) == 0.0
    assert p.pols_decline(p.proj_len() - 1) == 0.0


# ---------------------------------------------------------------------------
# Pitfall: truncation shortens the cycle, not the horizon


def test_pitfall_truncation_shortens_the_cycle_not_the_horizon():
    """A 갱신형 issued at 45 on ten-year cycles has a **five**-year final cycle to 80.

    「갱신일부터 최종 갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 … 갱신계약의
    보험기간 종료일까지 이 계약의 보험기간으로 합니다」, so the ceiling truncates rather than
    refuses, and the truncated cycle is priced over its own shorter length.  Shortening the
    *horizon* instead invents or destroys cover.  No shipped point reaches a truncated
    cycle, so the point is supplied through the filename Reference — which is the same
    swappable-input property the library advertises.
    """
    src = pd.read_csv(CSV_DIR / "model_point_table.csv", index_col="point_id")
    row = src.loc[3].copy()
    row["issue_age"] = 45
    row["policy_id"] = "KR-TL-TRUNC"
    alt = pd.DataFrame([row])
    alt.index = pd.Index([99], name="point_id")

    model = _reread("trunc")
    alt_name = "model_point_table_trunc.csv"
    alt_path = model.Data.input_dir() / alt_name
    try:
        alt.to_csv(alt_path)
        model.Data.model_point_file = alt_name
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[99]
        assert p.age_at_entry() == 45 and p.renew_ceiling() == 80
        assert p.horizon_ceiling() == 35 == p.proj_years()
        assert p.proj_len() == 420
        assert p.age(p.proj_len() - 1) + 1 == 80    # the horizon still ends at 80
        assert [p.term_start_age(k) for k in (1, 2, 3, 4)] == [45, 55, 65, 75]
        assert [p.term_len(k) for k in (1, 2, 3, 4)] == [10, 10, 10, 5]
        assert p.term_index(360) == 4 == p.term_index(419)
        assert p.mort_table_mean(75, 5) < p.mort_table_mean(75, 10)
        anchor = model.Data.prem_anchor_table().loc[("pure", "M")]
        assert p.prem_rate_mth(360) == pytest.approx(
            float(anchor["prem_mth_per_100m"]) * p.mort_table_mean(75, 5)
            / p.mort_table_mean(40, 20), rel=1e-12)
        assert p.renewal_decline_rate(359) == 0.20  # the last renewal
        assert p.renewal_decline_rate(419) == 0.0   # the cover ends; it does not renew
        # The truncated cycle is 60 months and not 120, and the premium is level across
        # all of them: truncation shortens the cycle, and the cycle is still one price.
        assert all(p.premium_mth_pp(t) == p.premium_mth_pp(360) for t in range(360, 420))
        assert p.check_pols_roll_fwd() is True
        assert p.check_decline_timing() is True and p.check_prem_level() is True
    finally:
        alt_path.unlink(missing_ok=True)
        model.close()


def test_pitfall_bi_gaengsin_never_renews(term_life):
    """One 보험기간, one premium, no repricing — and the decline rate is 0 at every t.

    Applying the renewal machinery to a 비갱신형 point invents cover the contract does not
    have, and 비갱신형 is the base here because it is the market: only three of the 45
    disclosed products renew at all.  ``check_decline_timing`` asserts the biconditional in
    both directions, which is what catches the opposite error too — a decline invented in
    the final year, where cover ends rather than renewing.
    """
    for point_id in (1, 2, 5, 6, 7, 8, 9, 10):
        p = term_life.Projection[point_id]
        n = p.proj_len()
        assert p.renewal_type() == "bi_gaengsin"
        assert p.horizon_ceiling() == p.policy_term() == p.proj_years()
        assert n == 12 * p.proj_years()
        assert all(p.term_index(t) == 1 for t in range(n))
        assert all(p.term_start_age(k) == p.age_at_entry() for k in (1, 2, 3))
        assert all(p.renewal_decline_rate(t) == 0.0 for t in range(n))
        assert all(p.pols_decline(t) == 0.0 for t in range(n))
        assert all(p.prem_pp(t) == p.prem_pp(0) for t in range(n))
        assert p.check_decline_timing() is True
    p7 = term_life.Projection[7]                    # a 세만기 point: term from expiry age
    assert p7.age_at_entry() == 65 and p7.policy_term() == 15
    assert p7.age(p7.proj_len() - 1) + 1 == 80


def test_pitfall_the_premium_follows_the_renewal_index_not_the_policy_year(term_life):
    """Freezing the premium at the issue value collects 2,195,589.29 of 11,517,624.04.

    That is one-fifth of the right price: indexing the premium by ``t`` converts a 갱신형
    into a 비갱신형 without changing anything a policy roll-forward can see.
    ``check_prem_level`` asserts the complement — level **within** a cycle, changing across
    a boundary — which catches the opposite error, a rate lookup keyed on attained age that
    makes the premium drift period by period instead of stepping.
    """
    p = term_life.Projection[3]
    assert p.check_prem_level() is True
    for t in range(p.proj_len()):
        assert p.check_prem_level_resid(t) == pytest.approx(0.0, abs=1e-12)
    assert all(p.prem_pp(t) == p.prem_pp(0) for t in range(1, 120))
    for t in (119, 239, 359):
        assert p.prem_pp(t + 1) > p.prem_pp(t)
        assert p.check_prem_level_resid(t + 1) == 0.0   # zero by definition, not by luck
    frozen = sum(p.premium_mth_pp(0) * p.pols_payer(t) for t in range(p.proj_len()))
    assert frozen == pytest.approx(2195589.29, abs=WON)
    assert p.result_cf()["premiums"].sum() == pytest.approx(11517624.04, abs=WON)
    assert frozen / p.result_cf()["premiums"].sum() == pytest.approx(0.191, abs=5e-4)


# ---------------------------------------------------------------------------
# Pitfall: the waiver, and what a 갱신 does and does not reset


def test_pitfall_a_premium_waiver_does_not_survive_a_gaengsin(term_life):
    """u(t) is 0.0 exactly at t = 0, 120, 240, 360 and rebuilds to 0.0079050974 by t = 119.

    Sourced, not assumed: 「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료 납입면제 사유로
    인한 보험료 납입면제를 적용하지 않고, 보험료를 계속 납입하여야 합니다」.  A disabled life
    resumes paying at the renewal date, so a model carrying the waived fraction across the
    boundary loses premium income the contract entitles the insurer to collect — invisibly,
    because no policy count moves.
    """
    p = term_life.Projection[3]
    assert p.waiver() is True and p.check_waiver_reset() is True
    for t in (0, 120, 240, 360):
        assert p.wop_waived_frac(t) == 0.0, f"the waiver survived into t={t}"
        assert p.pols_waived(t) == 0.0
        assert p.pols_payer(t) == pytest.approx(p.pols_if(t), rel=1e-15)
    for first in (0, 120, 240, 360):
        run = [p.wop_waived_frac(t) for t in range(first, first + 120)]
        assert run == sorted(run)
        assert run[-1] == pytest.approx(WAIVED_AT_CYCLE_END, rel=1e-12)
    # The incidence is stated annually, because that is the unit a 장해 incidence would be
    # published in, and converted to the step the chain runs on.  It is a **probability**
    # over the year, so the constant-force monthly equivalent sits slightly **above** a
    # twelfth of it — twelve of them have to leave the same fraction unwaived that one
    # annual rate does — and a model that divided by twelve would understate the waived
    # population.  Compare LTC_KR_S, where the transition intensities are rates per year
    # and are divided; which conversion is right depends on what the number is.
    assert p.wop_rec_rate == 0.0 and p.wop_rec_rate_mth() == 0.0
    assert p.wop_inc_rate_mth() == pytest.approx(
        1.0 - (1.0 - 0.0008) ** (1.0 / 12.0), rel=1e-15)
    assert 0.0008 / 12.0 < p.wop_inc_rate_mth() < 0.0008
    assert 1.0 - (1.0 - p.wop_inc_rate_mth()) ** 12 == pytest.approx(0.0008, rel=1e-14)
    for t in range(1, 119):
        u = p.wop_waived_frac(t - 1)
        assert p.wop_waived_frac(t) == pytest.approx(
            u + (1 - u) * p.wop_inc_rate_mth(), rel=1e-13)
    assert p.check_pols_payer() is True
    for t in (47, 119, 288, 479):
        assert p.pols_payer(t) + p.pols_waived(t) == pytest.approx(
            p.pols_if(t) * p.prem_payable(t), rel=1e-15)


def test_pitfall_the_suicide_and_contestability_clocks_do_not_reset_at_a_gaengsin(
        term_life):
    """``pols_if`` is continuous across every boundary — a 갱신 reprices, it does not reissue.

    The contract is fresh for pricing and for the waiver and continuous for the exclusions,
    which run from the original 보장개시일 and restart only on 부활.  The observable
    consequence is asserted: no reset of the in-force to 1, no acquisition expense and no
    initial commission at a renewal, and an inflation clock that runs from issue.
    """
    p = term_life.Projection[3]
    for t in (119, 239, 359):
        assert p.pols_if(t + 1) == pytest.approx(p.pols_if_at(t, "AFT_DECR"), rel=1e-15)
        assert p.pols_if(t + 1) < 0.6                     # never a reset to 1
        assert p.expenses(t + 1) == pytest.approx(
            2000.0 * 1.02 ** ((t + 1) // 12) * p.pols_if(t + 1), rel=1e-13)
        assert p.commissions(t + 1) == pytest.approx(0.03 * p.premiums(t + 1), rel=1e-13)
        assert p.comm_new_term(t + 1) == 0.0
    assert p.expenses(0) - 2000.0 == pytest.approx(120000.0, abs=WON)
    assert p.commissions(0) == pytest.approx(0.60 * p.prem_pp(0), abs=WON)


def test_pitfall_the_waiver_is_cause_neutral_so_it_is_not_scaled_off_mort_rate(
        term_life):
    """``wop_inc_rate`` is a flat placeholder, deliberately not a function of q.

    The trigger is a 장해지급률 of 50% or more from 「동일한 재해 또는 재해이외의 동일한
    원인」 — sickness qualifies equally with accident — so the incidence is a general
    disability incidence.  A number derived from ``mort_rate`` would be a false derivation
    dressed as a real one, and would import the mortality best-estimate factor into a
    disability assumption.  The signature is that the increment is flat while q is not.
    """
    p = term_life.Projection[3]
    assert p.wop_inc_rate == 0.0008
    increments = [p.wop_waived_frac(t) - p.wop_waived_frac(t - 1) for t in range(1, 120)]
    assert max(increments) / min(increments) < 1.01
    assert p.mort_rate(119) / p.mort_rate(0) > 1.6
    assert p.mort_rate_mth(119) / p.mort_rate_mth(0) > 1.6
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("wop_mort_ratio", "wop_rate_factor", "disab_from_mort"):
        assert absent not in names


# ---------------------------------------------------------------------------
# Pitfall: one decrement, and what may be split out of it


def test_pitfall_acc_death_is_a_split_of_the_decrement_never_a_second_decrement(
        term_life):
    """The uplift pays 2 x SA on 재해사망 and 1 x otherwise, on **one** decrement.

    ``claims_acc_death`` is the *second* sum assured on the accidental subset and sits
    beside the full ``claims_death``, so the total on an accidental death is exactly 2 x SA.
    An accidental incidence added as a decrement of its own would double-count the deaths
    and break the roll-forward; the arithmetic guard is that a year's benefit outgo can
    never exceed two sums assured on that year's decrement.
    """
    p = term_life.Projection[10]
    for t in range(p.proj_len()):
        assert p.acc_mort_share(t) <= 1.0
        assert p.claims(t, "DEATH") == pytest.approx(
            p.sum_assured() * p.pols_death(t), rel=1e-14)
        assert p.claims(t, "ACC_DEATH") == pytest.approx(
            p.sum_assured() * p.acc_mort_share(t) * p.pols_death(t), rel=1e-14)
        assert p.claims(t) <= 2.0 * p.sum_assured() * p.pols_death(t) + 1e-9
    assert p.pols_death(0) == pytest.approx(p.pols_if(0) * p.mort_rate_mth(0), rel=1e-15)
    assert p.check_pols_roll_fwd() is True
    for point_id in (1, 3, 7):
        q = term_life.Projection[point_id]
        assert q.acc_death() is False
        assert (q.result_cf()["claims_acc_death"] == 0.0).all()


def test_pitfall_the_disability_state_is_not_a_benefit(term_life):
    """Korea has no 高度障害保険金 analogue: the 장해 state waives premiums and nothing more.

    Adding a disability claim on top of the death decrement invents a benefit the contract
    does not carry, and doing it on the Japanese pattern also double-counts, the table there
    already including the second event.  Names alone are not coverage, so the guard is the
    product fact: on a point without the 재해사망 uplift, benefit outgo never exceeds **one**
    sum assured on the year's decrement.
    """
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("disability_rate", "disab_rate", "ci_rate", "morbidity_rate",
                   "claims_disability", "janghae_rate"):
        assert absent not in names, f"{absent} would invent a benefit"
    assert not [n for n in names if "disab" in n or "morbid" in n]
    for point_id in (1, 3, 5):
        p = term_life.Projection[point_id]
        for t in range(p.proj_len()):
            if p.pols_maturity(t) == 0.0:
                assert p.claims(t) <= p.sum_assured() * p.pols_death(t) + 1e-9, (
                    f"point {point_id}, t={t}: outgo exceeds one sum assured")
    with pytest.raises(FormulaError):
        term_life.Projection[1].claims(0, "DISABILITY")


def test_pitfall_no_claims_aggregate_column_beside_the_splits(term_life):
    """``claims(t, kind)`` stays a cells; ``result_cf()`` publishes only the five splits.

    An aggregate column beside the splits double-counts the whole benefit outgo, and
    ``check_net_cf`` — which re-derives the ledger from the published frame — would then fail
    on every row.  The kind argument is validated rather than defaulted, so a typo in a
    benefit name raises instead of silently returning zero.
    """
    df = term_life.Projection[1].result_cf()
    assert "claims" not in df.columns
    assert [c for c in df.columns if c.startswith("claims")] == [
        "claims_death", "claims_acc_death", "claims_accel", "claims_maturity",
        "claims_lapse"]
    p = term_life.Projection[10]
    for t in (0, 119, 239):
        assert p.claims(t) == pytest.approx(
            sum(p.claims(t, k) for k in
                ("DEATH", "ACC_DEATH", "ACCEL", "MATURITY", "LAPSE")), rel=1e-15)
    with pytest.raises(FormulaError):
        p.claims(0, "SURRENDER")


# ---------------------------------------------------------------------------
# Pitfall: a lapse pays nothing, and what follows from that


def test_pitfall_lapse_pays_nothing_and_the_zero_is_published(term_life):
    """``claims_lapse`` is identically 0.00 on every model point, and is shipped anyway.

    On a 전기납 무해지 contract the 약관 pays nothing at any duration and the published
    해약환급금 예시 shows 환급률 0.0% at every duration printed.  But the **표준형 comparator
    does have a surrender value**, and a shortened-pay 무해지 contract acquires 50% of it
    after 납입완료, so a Korea term chassis cannot assume the absence the way a UK one can:
    the zero is asserted from the composite's own form, which is why the column is published
    rather than dropped.  No surrender value also means no 보험계약대출 and no 자동대출납입 in
    fact, so none of the savings chassis's cash-value machinery may appear here.
    """
    for point_id in sorted(POINT_SUMMARY):
        p = term_life.Projection[point_id]
        df = p.result_cf()
        assert "claims_lapse" in df.columns and (df["claims_lapse"] == 0.0).all()
        assert all(p.claims(t, "LAPSE") == 0.0 for t in range(p.proj_len()))
        assert any(p.pols_lapse(t) > 0.0 for t in range(p.proj_len()))
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("cv_pp", "av_pp", "policy_loan", "loan_bal", "apl", "apl_rate",
                   "surr_charge", "prem_to_av_pp", "cv_rate"):
        assert absent not in names, f"{absent} belongs to a chassis with a cash value"
    assert not [n for n in names if "loan" in n or n.startswith("cv_")]


def test_pitfall_the_jeongi_nap_resolution_couples_pay_term_to_the_boundary(term_life):
    """Model point 4 is **not** model point 3 truncated: -181,055.18 against -172,034.54.

    ``pay_term_y = 0`` means 전기납 and resolves to ``proj_len()``, so truncating a 갱신형
    point at the cycle in force compresses the 적용해지율 curve from forty years to ten with
    it.  That is a consequence of the boundary reading rather than a bug, and it is asserted
    here so that a later change making the two agree fails a test.  Model point 5, a genuine
    10년납 contract, is the mirror image and the only shipped point that reaches the
    ``post_payment`` row at all: its curve runs the disclosed shape at its disclosed length
    and then **steps** to the 0.8% ultimate rather than converging smoothly, the premium
    ceases and cover does not, and the 무해지 post-완납 surrender-value step-up this makes
    possible is the quantity the chassis deliberately does not compute.
    """
    p3, p4 = term_life.Projection[3], term_life.Projection[4]
    # ``pay_term`` is a **contractual term in years** and resolves against proj_years(),
    # not against the 480-month frame: 전기납 means paying for the whole projection, and
    # the projection is forty years however many rows it prints.
    assert p3.pay_term() == 40 and p4.pay_term() == 10
    assert p3.result_cf()["net_cf"][:120].sum() == pytest.approx(
        GAENGSIN_FIRST_CYCLE_NET_CF, abs=WON)
    assert p4.result_cf()["net_cf"].sum() == pytest.approx(CURRENT_TERM_NET_CF, abs=WON)
    assert p3.result_cf()["net_cf"][:120].sum() != pytest.approx(
        p4.result_cf()["net_cf"].sum(), abs=1.0)
    assert p3.lapse_rate(0) == pytest.approx(p4.lapse_rate(0), rel=1e-14)
    assert p4.lapse_rate(119) == pytest.approx(0.001, rel=1e-14)
    assert p3.lapse_rate(119) > p4.lapse_rate(119)
    assert p3.lapse_rate(479) == pytest.approx(0.001, rel=1e-14)

    p = term_life.Projection[5]
    assert p.pay_term() == 10 and p.proj_years() == 20 and p.proj_len() == 240
    assert p.lapse_rate(119) == pytest.approx(0.001, rel=1e-14)
    assert all(p.lapse_rate(t) == 0.008 for t in range(120, 240))
    assert p.prem_payable(119) == 1.0 and p.prem_payable(120) == 0.0
    assert p.pols_payer(120) == 0.0 and p.premiums(120) == 0.0
    assert p.commissions(120) == 0.0 and p.check_pols_payer() is True
    assert p.pols_death(120) > 0.0 and p.claims(120, "DEATH") > 0.0
    assert all(p.claims(t, "LAPSE") == 0.0 for t in range(120, 240))


# ---------------------------------------------------------------------------
# Pitfall: the premium chassis


def test_pitfall_qbar_is_a_mean_of_table_rates_not_best_estimate_rates(term_life):
    """``mort_table_mean`` averages ``mort_rate_at_age``, unadjusted by anything.

    A premium scale is not a best-estimate quantity, so feeding ``mort_rate`` into the
    extension would move a published rate card by an assumption with nothing to do with
    pricing.  A class-adjusted qbar would **cancel in the ratio** and fail silently only on a
    preferred-class point, which is the worst kind of error — so it is the preferred-class
    point that is asserted here.  The seven diagnostic values the notes publish are asserted
    alongside, because they are what lets a reader verify the extension against the shipped
    mortality table with a spreadsheet.
    """
    a = term_life.Projection[1]
    assert a.mort_table_mean(40, 20) == pytest.approx(
        sum(a.mort_rate_at_age(x) for x in range(40, 60)) / 20.0, rel=1e-14)
    assert a.mort_table_mean(40, 1) == a.mort_rate_at_age(40)      # not 0.85 x it
    for (sex, x, m), qbar in sorted(QBAR_DIAGNOSTICS.items()):
        q = term_life.Projection[1 if sex == "M" else 2]
        assert q.sex() == sex
        assert q.mort_table_mean(x, m) == pytest.approx(qbar, abs=5e-9), (sex, x, m)
    p = term_life.Projection[10]
    assert p.rate_class() == "preferred" and p.class_mort_ratio() < 1.0
    anchor = float(term_life.Data.prem_anchor_table().loc[
        ("pure", "M"), "prem_mth_per_100m"])
    assert p.prem_rate_mth(0) == pytest.approx(
        anchor * p.mort_table_mean(55, 20) / p.mort_table_mean(40, 20), rel=1e-12)
    # A class-adjusted qbar would cancel; a best-estimate one would not.
    classed = (anchor * p.mort_table_mean(55, 20) * p.class_mort_ratio()
               / (p.mort_table_mean(40, 20) * p.class_mort_ratio()))
    assert classed == pytest.approx(p.prem_rate_mth(0), rel=1e-12)
    be_scaled = (anchor * sum(p.mort_rate(12 * y) for y in range(20)) / 20.0
                 / p.mort_table_mean(40, 20))
    assert be_scaled != pytest.approx(p.prem_rate_mth(0), rel=1e-3)
    # The class enters through class_prem_ratio, once, and not through qbar.
    raw = p.prem_rate_mth(0) * p.class_prem_ratio() * p.sum_assured() / 100000000.0
    assert p.premium_mth_pp(0) == float(int(raw / 10.0 + 0.5) * 10)


def test_the_premium_scale_uses_published_cells_where_they_exist(term_life):
    """Points 1-6 read published cells only; points 7-10 use the [std] extension.

    The extension is anchored on the age-40 20-year cell of the matching form and sex, so a
    published cell is always used where one exists.  The 10-year rows and the 20-year rows
    come from **different carriers** and the model never mixes them: a 갱신형 point reaches
    published 10-year cells, and an unpublished cell runs off the 20-year anchor.
    """
    tbl = term_life.Data.prem_rate_table()
    published, extended = set(), set()
    for point_id in sorted(POINT_SUMMARY):
        p = term_life.Projection[point_id]
        key = (p.maturity_form(), p.sex(), p.term_start_age(1), p.term_len(1))
        (published if key in tbl.index else extended).add(point_id)
    assert published == {1, 2, 3, 4, 5, 6} and extended == {7, 8, 9, 10}
    anchors = term_life.Data.prem_anchor_table()
    assert set(anchors.index) == {("pure", "M"), ("pure", "F"),
                                  ("rop", "M"), ("rop", "F")}
    for form, sex in anchors.index:
        assert int(anchors.loc[(form, sex), "issue_age"]) == 40
        assert int(anchors.loc[(form, sex), "term_y"]) == 20
    assert float(tbl.loc[("pure", "M", 40, 20), "prem_mth_per_100m"]) == 15080.0
    assert float(tbl.loc[("pure", "F", 40, 20), "prem_mth_per_100m"]) == 8010.0
    assert term_life.Projection[2].prem_rate_mth(0) == 8010.0


def test_pitfall_the_premium_rounds_to_ten_won_before_annualization(term_life):
    """``round_10(r c_p g SA/1e8)`` then ``x 12`` — and the order reproduces 15,080.

    Rounding after annualization, or not at all, breaks the reproduction of the published
    15,080 / 180,960 at the anchor and of 9,000 / 108,000 on the 갱신형 point, and those are
    figures three independent documents agree on.  The extension points are where the
    rounding actually bites, so one of them is asserted explicitly.
    """
    for point_id in sorted(POINT_SUMMARY):
        p = term_life.Projection[point_id]
        raw = (p.prem_rate_mth(0) * p.class_prem_ratio() * p.pay_factor(1)
               * p.sum_assured() / 100000000.0)
        assert p.premium_mth_pp(0) == float(int(raw / 10.0 + 0.5) * 10)
        assert p.premium_mth_pp(0) % 10 == 0
        assert p.prem_pp(0) == 12.0 * p.premium_mth_pp(0)
    p10 = term_life.Projection[10]
    raw10 = p10.prem_rate_mth(0) * p10.class_prem_ratio() * p10.sum_assured() / 1e8
    assert raw10 != pytest.approx(p10.premium_mth_pp(0), abs=1e-9)
    assert abs(raw10 - p10.premium_mth_pp(0)) < 5.0 and p10.premium_mth_pp(0) == 49480.0
    assert term_life.Projection[1].premium_mth_pp(0) == 15080.0
    assert term_life.Projection[3].prem_pp(0) == 108000.0


def test_pitfall_twelve_times_p_m_is_exact_in_amount_and_standardized_only_in_timing(
        term_life):
    """``P_a = 12 P_m`` survives as a reporting quantity; the cash flow is ``P_m`` itself.

    On the annual grid this identity was a **convention**: a year's premium was collected
    in one instalment at the start of the year, which handed the insurer half a year's
    interest on the whole premium that the contract does not give it.  On a monthly grid it
    is nothing of the kind.  ``premiums(t)`` is one month's office premium on the lives in
    force when the month opens, which is what the policyholder pays and what the rate card
    quotes, and ``prem_pp`` survives only because the commission scale is written on an
    annualized premium and because a reader comparing this model with a disclosure needs
    the annual figure.  So no mode discount, no half-year adjustment, and nothing left for
    one to correct.
    """
    for point_id in (1, 3, 9):
        p = term_life.Projection[point_id]
        assert p.premium_mode() == "monthly"
        for t in (0, p.proj_len() - 1):
            assert p.prem_pp(t) == 12.0 * p.premium_mth_pp(t)
    a = term_life.Projection[1]
    for t in (0, 1, 119, 239):
        assert a.premiums(t) == pytest.approx(
            a.premium_mth_pp(t) * a.pols_payer(t), rel=1e-15)
        assert a.premiums(t) == pytest.approx(a.prem_pp(t) * a.pols_payer(t) / 12.0,
                                              rel=1e-15)
    # A year's income is twelve monthly premiums on twelve different exposures, so it sits
    # **below** one annualized premium on the opening exposure: the difference is the
    # premium the annual grid collected from lives that had already left.
    year_one = sum(a.premiums(t) for t in range(12))
    assert year_one < a.prem_pp(0) * a.pols_if(0)
    assert year_one / (a.prem_pp(0) * a.pols_if(0)) == pytest.approx(0.978, abs=5e-4)
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("mode_factor", "prem_mode_discount", "half_year_adj",
                   "prem_timing_adj"):
        assert absent not in names


def test_the_shortened_pay_uplift_is_an_annuity_certain_ratio(term_life):
    """g = 1.781198 on model point 5 and 1.484695 on model point 9, at the 적용이율.

    No Korean document retrieved publishes a shortened-pay premium for a **term** contract
    at all, so an equivalence had to be chosen; a certain annuity rather than a life annuity
    overstates the uplift slightly, by the mortality that would have been shed between the
    two periods.  It is 1.0 on a 전기납 contract, where there is nothing to uplift.
    """
    v = 1.0 / 1.025
    p5, p9 = term_life.Projection[5], term_life.Projection[9]
    assert p5.prem_int_rate == 0.025
    assert p5.pay_factor(1) == pytest.approx(1.781198, abs=5e-7)
    assert p9.pay_factor(1) == pytest.approx(1.484695, abs=5e-7)
    assert p5.pay_factor(1) == pytest.approx((1 - v ** 20) / (1 - v ** 10), rel=1e-14)
    assert p9.pay_factor(1) == pytest.approx((1 - v ** 35) / (1 - v ** 20), rel=1e-14)
    assert p5.term_pay_years(1) == 10 and p5.term_len(1) == 20
    for point_id in (1, 2, 3, 6, 7, 8, 10):
        p = term_life.Projection[point_id]
        assert p.pay_factor(1) == 1.0
        assert p.term_pay_years(1) == p.term_len(1)


# ---------------------------------------------------------------------------
# Pitfall: the 선지급 acceleration


def test_pitfall_the_accel_cap_is_reached_exactly_at_the_anchor_and_reduces_nothing(
        term_life):
    """``accel_cap_binds()`` is a **strict** inequality and is False at SA = 100,000,000.

    The cap is 「사망보험금액의 50% 이내에서 피보험자별로 통산하여 최고 5,000만원까지」, so at
    the anchor's cover the 50% limb gives exactly 50,000,000 and the aggregate cap is exactly
    reached and reduces nothing.  A model reporting it as binding there has a
    strict-versus-weak inequality error.  Model point 9, at 200,000,000 won, genuinely binds.
    """
    a = term_life.Projection[1]
    assert a.accel_share_max * a.sum_assured() == a.accel_cap == 50000000.0
    assert a.accel_cap_binds() is False and a.accel_full_limit == 10000000.0
    p7 = term_life.Projection[7]
    assert p7.accel() is True and p7.sum_assured() == 30000000.0
    assert p7.accel_cap_binds() is False and p7.accel_amount() == 15000000.0
    p9 = term_life.Projection[9]
    assert p9.accel() is True and p9.sum_assured() == 200000000.0
    assert p9.accel_cap_binds() is True and p9.accel_amount() == 50000000.0
    assert p9.accel_share_max * p9.sum_assured() == 100000000.0


def test_pitfall_the_accelerated_amount_comes_out_of_the_death_benefit(term_life):
    """``claims_death`` carries (1 - a(t)) and ``claims_accel`` carries a(t).

    The 보험가입금액 is treated as reduced by the amount paid from the payment date and no
    surrender value arises on the reduction, so the acceleration is a re-timing and
    re-pricing of the death benefit rather than a second claim; adding it on top of a full
    death claim pays the benefit twice.  The payout is discounted over the 12-month
    prognosis, which is why switching the rider off *raises* total benefit outgo.
    """
    p = term_life.Projection[7]
    v = 1.0 / 1.025
    assert (p.accel_take_up, p.accel_disc_rate, p.accel_prognosis_months) == (
        0.10, 0.025, 12)
    for t in range(p.proj_len()):
        assert p.accel_available(t) is True and p.accel_share(t) == 0.10
        assert p.claims(t, "DEATH") == pytest.approx(
            p.sum_assured() * 0.90 * p.pols_death(t), rel=1e-14)
        assert p.claims(t, "ACCEL") == pytest.approx(
            p.accel_payout_pp(t) * 0.10 * p.pols_death(t), rel=1e-14)
        assert p.claims(t) <= p.sum_assured() * p.pols_death(t) + 1e-9
    amount = p.accel_amount()
    assert p.accel_payout_pp(0) == pytest.approx(
        amount * v - 12 * p.premium_mth_pp(0) * amount / p.sum_assured() * v ** 0.5,
        rel=1e-13)
    assert p.accel_payout_pp(0) < amount
    on = sum(p.claims(t) for t in range(p.proj_len()))

    model = _reread("accoff")
    try:
        model.Projection.accel_take_up = 0.0
        model.Projection.clear_all()
        off = model.Projection[7]
        n = off.proj_len()
        assert off.accel_share(0) == 0.0
        assert all(off.pols_death(t) == pytest.approx(p.pols_death(t), abs=1e-15)
                   for t in range(n))
        assert sum(off.claims(t) for t in range(n)) > on
    finally:
        model.close()
    # Off in the base run, with the column published and zero.
    a = term_life.Projection[1]
    assert a.accel() is False and a.accel_amount() == 0.0
    assert (a.result_cf()["claims_accel"] == 0.0).all()


# ---------------------------------------------------------------------------
# Pitfall: the 부활 pool is carried by vintage


def test_pitfall_the_buhwal_window_runs_from_each_life_s_own_lapse(term_life):
    """The pool is the last three years' lapses, each net of its own reinstatements.

    The window runs from **each life's own 실효**, so a single indicator on one balance
    drops a whole cohort early or late.  ``reinstate_window = 36`` is the 약관's own three
    years carried in the projection's months, which is where a monthly grid earns its keep
    on this mechanic: the window closes on the month it actually closes on rather than at
    the next anniversary, and a life that lapsed in month 5 leaves the pool in month 41.
    The clause expressly covers a policy with no surrender value, so a 무해지 policy is
    always eligible; the rate beside it is an arbitrary placeholder, which is why the
    module is off in the base run and why the pool is tracked in both positions of the
    switch.
    """
    p = term_life.Projection[8]
    rho = p.reinstate_rate_eff()
    assert p.reinstatement() is True and p.reinstate_window == 36
    assert rho == pytest.approx(1.0 - 0.9 ** (1.0 / 12.0), rel=1e-15)
    assert 1.0 - (1.0 - rho) ** 12 == pytest.approx(0.10, rel=1e-14)
    assert p.pols_lapse_pool(0) == 0.0
    assert p.pols_reinstate(1) == pytest.approx(rho * p.pols_lapse_pool(1), rel=1e-14)
    assert p.pols_if(2) > p.pols_if_at(1, "AFT_DECR")        # lives come back in
    for t in range(1, p.proj_len()):
        rebuilt = sum(p.pols_lapse(s) * (1.0 - rho) ** (t - 1 - s)
                      for s in range(max(0, t - 36), t))
        assert p.pols_lapse_pool(t) == pytest.approx(rebuilt, abs=1e-14)
    assert p.pols_lapse_expire(35) == 0.0
    assert p.pols_lapse_expire(36) == pytest.approx(
        p.pols_lapse(0) * (1.0 - rho) ** 36, rel=1e-13)
    assert p.check_lapse_pool() is True
    a = term_life.Projection[1]
    assert a.reinstatement() is False and a.reinstate_rate_eff() == 0.0
    assert all(a.pols_reinstate(t) == 0.0 for t in range(a.proj_len()))
    assert a.pols_lapse_pool(3) > 0.0 and a.check_lapse_pool() is True


def test_pitfall_declines_never_enter_the_reinstatement_pool(term_life):
    """A declined 갱신 is an expiry, not a 실효, so there is nothing to reinstate.

    Only ordinary lapses flow into the pool.  Folding the boundary exits in would reinstate
    lives whose contract ended rather than lapsed — and in the 갱신형 anchor's boundary month
    the declines are 99.2% of the exits, so the error would be large as well as wrong.
    """
    p = term_life.Projection[3]
    assert p.pols_decline(119) > 0.0
    for t in (119, 120, 130, 155):
        assert p.pols_lapse_pool(t) == pytest.approx(
            sum(p.pols_lapse(s) for s in range(max(0, t - 36), t)), abs=1e-14)
    assert p.check_lapse_pool() is True
    model = _reread("pool")
    try:
        model.Projection.reinstate_rate = 0.10
        model.Projection.clear_all()
        q = model.Projection[3]
        assert q.reinstatement() is False          # the column, not the Reference
        assert q.pols_lapse_pool(120) == pytest.approx(
            sum(q.pols_lapse(s) for s in range(84, 120)), abs=1e-14)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: read the tables at 보험나이 and at nothing else


def test_pitfall_read_the_tables_at_boheom_nai_and_at_nothing_else(term_life):
    """Reading the anchor cell a year early cuts death claims to 1,897,843.01 — 8.0% out.

    보험나이 is 만나이 with fractions of six months or more rounded up, incrementing on the
    **policy anniversary** and not on the birthday, and the premium grid, the mortality table
    and the model point ages are all on that one basis.  Unlike ``jplib``, where the contract
    age and the table basis differ and an optional shift exists, **no shift is correct
    here** — importing one is the error, and the model carries no lever that could.
    """
    a = term_life.Projection[1]
    assert a.age_at_entry() == 40 and a.age(0) == 40 and a.age(239) == 59
    # The age steps on the 계약해당일 and holds for the twelve months between, which is the
    # monthly grid's own statement of the rule: 보험나이 does not move on a birthday, so
    # interpolating it within the policy year would be modelling an age the contract has
    # no concept of.
    for t in (0, 119, 239):
        assert a.age(t) == a.age_at_entry() + t // 12
        assert a.mort_rate_base(t) == a.mort_rate_at_age(a.age(t)) * a.class_mort_ratio()
    assert a.age(11) == 40 and a.age(12) == 41
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("mort_age_shift", "age_shift", "age_basis_shift", "man_nai_shift"):
        assert absent not in names, f"{absent} would apply a shift this model must not"
    # The counterfactual is the whole projection read a year early — the shifted rate
    # drives the survivorship too, which is what a mis-specified model would actually do.
    understated, pols = 0.0, 1.0
    for t in range(240):
        q = 1.0 - (1.0 - a.mort_be_factor
                   * a.mort_rate_at_age(a.age(t) - 1)) ** (1.0 / 12.0)
        understated += a.sum_assured() * pols * q
        pols *= (1.0 - q) * (1.0 - a.lapse_rate_mth(t))
    assert understated == pytest.approx(1897843.01, abs=WON)
    assert 1.0 - understated / TOTAL_CLAIMS_DEATH == pytest.approx(0.080, abs=5e-4)
    assert TOTAL_CLAIMS_DEATH - understated > TOTAL_NET_CF   # more than the whole answer
    assert "보험나이" in term_life.Projection.doc


# ---------------------------------------------------------------------------
# The [std] parameters the notes state


def test_the_std_scalar_assumptions_the_notes_state(term_life):
    """Every scalar the notes tabulate, read off the model's References.

    The house rule is that every quantitative parameter is source-tagged or marked [std],
    and the notes carry each of these with its tag.  Pinning them means a silent change to
    an assumption fails a **named** test rather than moving a golden and looking like an
    arithmetic problem.  Three parameters beside them are **sourced** and are asserted as
    such: ``reinstate_window = 36`` is the 약관's own three-year 부활 window, carried in
    the projection's own months,
    ``accel_prognosis_months = 12`` is its prognosis (twice Japan's six), and
    ``accel_disc_rate = 0.025`` is the 2026 평균공시이율 the 약관 names for this discount.  That
    the last equals the composite's 적용이율 is a coincidence of level and not an identity of
    concept, so moving one must not move the other.
    """
    refs = term_life.Projection.refs
    for name, value in STD_SCALARS.items():
        assert name in refs, f"{name} is no longer a Reference"
        assert refs[name] == pytest.approx(value, rel=1e-15), name
    assert refs["renewal_decline_base"] < refs["renewal_decline_max"]
    assert 0.0 < refs["wop_inc_rate"] < 0.01
    assert 0.0 < refs["accel_take_up"] < 1.0
    assert 0.0 < refs["reinstate_rate"] < 1.0
    assert refs["reinstate_window"] == 36 and refs["accel_prognosis_months"] == 12
    assert refs["accel_disc_rate"] == 0.025 == refs["prem_int_rate"]
    model = _reread("rates")
    try:
        model.Projection.accel_disc_rate = 0.04
        model.Projection.clear_all()
        p = model.Projection[7]
        assert p.prem_int_rate == 0.025           # unmoved: a different quantity
        assert p.premium_mth_pp(0) == term_life.Projection[7].premium_mth_pp(0)
        assert p.accel_payout_pp(0) < term_life.Projection[7].accel_payout_pp(0)
    finally:
        model.close()


def test_the_shipped_mortality_table_marks_its_own_provenance_and_hits_the_published_e65():
    """Every row says whether it is a disclosed anchor or the [std] fit, and e(65) lands.

    The 제10회 경험생명표 is **not published** — only 평균수명 and 65세 기대여명 are released —
    so the library ships a Makeham construction fitted exactly to the three 예정 경험사망률
    rates per sex that every 상품요약서 must print, tilted above 60 so the table reproduces
    the published e(65) of 23.7 male and 27.1 female.  That reproduction is the only external
    check available, and the four-year gap over the public 완전생명표 is the underwriting
    selection a Korean insured-lives table must show.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "acc_mort_rate",
                                   "provenance"]
    assert table["provenance"].notna().all()
    assert (table["provenance"].str.contains(r"\[std\]")).all()
    assert (table["provenance"].str.contains("[S12]", regex=False)).all()
    anchors = table[table["provenance"].str.contains(" ANCHOR row:", regex=False)]
    assert {(r.sex, int(r.age)): float(r.mort_rate)
            for r in anchors.itertuples()} == SOURCED_ANCHORS
    assert (table["age"].min(), table["age"].max()) == (19, 120)
    assert set(table["sex"]) == {"M", "F"}
    assert (table["mort_rate"] > 0.0).all()
    assert (table["acc_mort_rate"] <= table["mort_rate"]).all()

    for sex, target, population in (("M", 23.7, 19.5), ("F", 27.1, 23.7)):
        q = table[table["sex"] == sex].set_index("age")["mort_rate"]
        lives, expectation = 1.0, 0.0
        for x in range(65, 121):
            rate = min(1.0, float(q.loc[x]))
            expectation += lives * (1.0 - rate / 2.0)
            lives *= (1.0 - rate)
        assert expectation == pytest.approx(target, abs=5e-4), sex
        assert expectation - population > 3.0


def test_the_rate_class_relativities_are_sourced_ratios(term_life):
    """Korea publishes the mortality behind its preferred classes; the ratios are read off it.

    Both a ``mort_ratio`` and a ``prem_ratio`` are shipped, and the premium ratio **exceeds**
    the mortality ratio in every cell, because the expense loading does not scale with the
    risk.  Holding the ratios flat across ages is the only [std] step, the disclosures being
    at three ages between which the ratios move little.
    """
    table = term_life.Data.rate_class_table()
    classes = ("standard", "nonsmoker", "preferred", "super_preferred")
    assert set(table.index) == {(c, s) for c in classes for s in ("M", "F")}
    assert table["provenance"].notna().all()
    for sex in ("M", "F"):
        assert float(table.loc[("standard", sex), "mort_ratio"]) == 1.0
        assert float(table.loc[("standard", sex), "prem_ratio"]) == 1.0
        for cls in classes[1:]:
            mort = float(table.loc[(cls, sex), "mort_ratio"])
            prem = float(table.loc[(cls, sex), "prem_ratio"])
            assert 0.0 < mort < 1.0 and 0.0 < prem < 1.0
        morts = [float(table.loc[(c, sex), "mort_ratio"]) for c in classes]
        assert morts == sorted(morts, reverse=True)
    p8 = term_life.Projection[8]
    assert p8.rate_class() == "super_preferred" and p8.sex() == "M"
    assert p8.class_mort_ratio() == pytest.approx(0.583077, abs=5e-7)
    assert p8.class_prem_ratio() == pytest.approx(0.586207, abs=5e-7)
    assert p8.mort_rate(0) == pytest.approx(
        0.85 * 0.583077 * p8.mort_rate_at_age(19), rel=1e-6)


# ---------------------------------------------------------------------------
# The sensitivities the notes tabulate


@pytest.mark.parametrize("factor", sorted(MORT_BE_SENSITIVITY))
def test_the_mortality_factor_sensitivity_the_notes_tabulate(factor):
    """+361,807.55 at 0.75, +117,619.70 at 0.85 and -247,394.11 at 1.00.

    The range crosses zero inside a plausible band and is more than five times the whole
    answer, which is why the notes name this the model's largest lever: the margin inside a
    Korean 예정 경험사망률 sits in a 기초서류 that is never published, so the factor cannot be
    argued from a stated adjustment the way ``jplib``'s can.
    """
    model = _reread("mbf%d" % round(factor * 100))
    try:
        model.Projection.mort_be_factor = factor
        model.Projection.clear_all()
        assert model.Projection[1].result_cf()["net_cf"].sum() == pytest.approx(
            MORT_BE_SENSITIVITY[factor], abs=WON)
    finally:
        model.close()


@pytest.mark.parametrize("d", sorted(DECLINE_SENSITIVITY))
def test_the_renewal_decline_sensitivity_the_notes_tabulate(d):
    """Net cash flow and premium income at d = 0%, 5%, 20% and 40% on the 갱신형 anchor.

    A factor of 4.4 across a range no document narrows, driven almost entirely by premium
    income — 19.81m to 6.24m won.  The rate is published nowhere in Korea for any product,
    the mandatory disclosure requiring the **price** path and not the persistency path, so
    the sensitivity is the honest form of the answer.
    """
    net_cf, premiums = DECLINE_SENSITIVITY[d]
    model = _reread("dec%d" % round(d * 100))
    try:
        model.Projection.renewal_decline_base = d
        model.Projection.clear_all()
        df = model.Projection[3].result_cf()
        assert df["net_cf"].sum() == pytest.approx(net_cf, abs=WON)
        assert df["premiums"].sum() == pytest.approx(premiums, abs=WON)
    finally:
        model.close()


@pytest.mark.parametrize("factor", sorted(LAPSE_BE_SENSITIVITY))
def test_the_lapse_level_sensitivity_is_third_order_and_that_is_the_finding(factor):
    """+110,995.14 / +108,809.94 / +99,649.28 over 0.5 / 1.0 / 2.0 — 11,000 won of range.

    On a no-surrender-value protection form a lapse forfeits a paying policy and saves its
    claims in nearly equal measure, so the leverage that dominates a savings chassis is
    second-order here: a **fourfold** move in the assumption moves the answer by 10% of
    itself, against the 60% a hundred-basis-point move in ``mort_be_factor`` is worth.

    The monthly grid widens this sensitivity and the reason is worth stating, because the
    annual grid's version of this test reported a range of 3,000 won and called it
    third-order.  That number was an artefact of the timing convention: an annual step
    collected a whole year's premium in advance and only then applied the year's lapse, so
    a lapsing policy paid for the year it left in and the premium the insurer loses to
    lapse was understated by construction.  Stepping monthly stops crediting premium to
    lives that have gone, and the assumption's real leverage — still modest, still not the
    first-order lever a savings form has — becomes visible.
    """
    model = _reread("lbf%d" % round(factor * 10))
    try:
        model.Projection.lapse_be_factor = factor
        model.Projection.clear_all()
        total = model.Projection[1].result_cf()["net_cf"].sum()
        assert total == pytest.approx(LAPSE_BE_SENSITIVITY[factor], abs=WON)
        assert abs(total - TOTAL_NET_CF) < 0.11 * abs(TOTAL_NET_CF)
        # Still an order of magnitude below the mortality lever, which is the finding.
        assert (abs(total - TOTAL_NET_CF)
                < abs(MORT_BE_SENSITIVITY[1.00] - TOTAL_NET_CF) / 3.0)
    finally:
        model.close()


def test_commission_at_a_gaengsin_is_off_and_changes_the_sign_when_switched_on():
    """Setting the rate to 0.60 turns t = 120 from +4,689.19 to -83,085.07.

    A 갱신 is issued on a new product code, which argues for paying commission on it, and it
    takes no 고지, which argues against; no document discloses a scale at all, so the base run
    pays nothing and exposes the switch.

    A monthly grid changes how this reads, and for the better.  The commission is a
    **single month's** charge on an annualized premium, so it lands in one row as a cliff
    of the same shape as the acquisition commission at issue, and every boundary it lands
    on goes sharply negative — where an annual step netted it against a whole year of the
    repriced premium and left the third boundary looking marginal.  Whether the *cycle*
    recovers is then a separate question with a separate answer, which is the distinction
    worth having.
    """
    model = _reread("comm")
    try:
        base = model.Projection[3]
        assert base.comm_new_term_rate == 0.0
        assert all(base.comm_new_term(t) == 0.0 for t in range(480))
        before = {t: base.net_cf(t) for t in (120, 240, 360)}
        model.Projection.comm_new_term_rate = 0.60
        model.Projection.clear_all()
        p = model.Projection[3]
        for t in (119, 239, 359):
            assert p.comm_new_term(t + 1) == pytest.approx(
                0.60 * p.prem_pp(t + 1) * p.pols_if(t + 1), rel=1e-13)
            assert p.net_cf(t + 1) < before[t + 1]
            assert p.net_cf(t + 1) < 0.0
        assert p.comm_new_term(0) == 0.0        # not the first cycle
        assert p.comm_new_term(121) == 0.0      # only the cycle's first month
        assert p.comm_new_term(130) == 0.0
        assert p.net_cf(120) == pytest.approx(-83085.07, abs=WON)
        assert p.result_cf()["net_cf"].sum() == pytest.approx(2238679.76, abs=WON)
        assert p.result_cf()["net_cf"].sum() < GAENGSIN_TOTAL_NET_CF
        assert p.check_net_cf() is True
    finally:
        model.close()


def test_the_renewal_decline_elasticity_is_off_and_works_when_switched_on():
    """d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta); beta = 0 gives the flat 20%.

    The premium jump the elasticity responds to accelerates — 2.33, 2.67, 3.59 — so a
    non-zero beta makes the later boundaries shed more than the earlier ones, and
    ``renewal_decline_max`` is what stops it running away.  At beta = 2 every boundary is
    already at the cap, which is the behaviour the cap exists to produce.
    """
    model = _reread("beta")
    try:
        base = model.Projection[3]
        assert base.renewal_decline_beta == 0.0
        assert [base.renewal_decline_rate(t) for t in (119, 239, 359)] == [0.20] * 3
        model.Projection.renewal_decline_beta = 0.5
        model.Projection.clear_all()
        p = model.Projection[3]
        rates = [p.renewal_decline_rate(t) for t in (119, 239, 359)]
        assert rates == sorted(rates) and all(r < p.renewal_decline_max for r in rates)
        assert rates[0] == pytest.approx(0.20 * (252000.0 / 108000.0) ** 0.5, rel=1e-13)
        assert rates[-1] == pytest.approx(
            0.20 * (2412000.0 / 672000.0) ** 0.5, rel=1e-13)
        assert p.result_cf()["net_cf"].sum() < GAENGSIN_TOTAL_NET_CF
        assert p.check_decline_timing() is True
        model.Projection.renewal_decline_beta = 2.0    # above the cap everywhere
        model.Projection.clear_all()
        q = model.Projection[3]
        assert [q.renewal_decline_rate(t) for t in (119, 239, 359)] == [0.40] * 3
        assert q.result_cf()["net_cf"].sum() == pytest.approx(
            DECLINE_SENSITIVITY[0.40][0], abs=WON)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Documentation and inputs


def test_the_docstrings_carry_this_product_s_own_reference_material(term_life):
    """Product-specific phrases a reader relies on, which a generic sweep cannot know.

    The model docstring names the chassis and the 갱신형 split, the Projection docstring
    carries the notes' symbol map and the 보험나이 basis, and the Data docstring explains the
    layout it follows.  Asserted so that they cannot go stale silently while the numbers
    stay right.
    """
    doc = term_life.doc
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "protection chassis", "갱신형", "비갱신형", "보험나이"):
        assert phrase in doc, phrase
    proj = term_life.Projection.doc
    assert "Notes symbol" in proj and "no tail state of any kind" in proj
    for cells in ("proj_len", "model_point", "pols_if", "term_index",
                  "renewal_decline_rate", "pols_lapse_pool", "prem_rate_mth",
                  "wop_waived_frac", "accel_share"):
        assert cells in proj, cells
    data = term_life.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "prem_rate_table",
                  "lapse_table", "rate_class_table"):
        assert cells in data, cells


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a user with a company
    mortality basis does: a same-schema CSV drops in with no formula change.  It is also the
    mechanism the truncation test above uses to supply a model point the shipped table does
    not carry.

    Doubling the table doubles the **annual** rate, and the monthly claim it produces is
    therefore *not* twice the original: ``1 - (1 - 2q)^(1/12)`` is slightly **larger** than
    ``2 (1 - (1 - q)^(1/12))``, because doubling an annual probability more than doubles
    the force behind it — ``-ln(1 - 2q) > -2 ln(1 - q)`` — and the monthly step sees the
    force.  The gap is 0.03% at this level and would be percentage points at a
    claims-inducement one, so the right assertion is on the conversion and not on the
    linearity: asserting that the monthly claim doubled would be asserting that the model
    converts by dividing, which is the error this whole grid exists not to make.
    """
    doubled = pd.read_csv(CSV_DIR / "mort_table.csv", index_col=["sex", "age"])
    doubled["mort_rate"] = doubled["mort_rate"] * 2
    model = _reread("swap")
    alt_name = "mort_table_doubled.csv"
    try:
        alt_path = model.Data.input_dir() / alt_name
        doubled.to_csv(alt_path)
        try:
            p = model.Projection[1]
            base_annual, base_claim = p.mort_rate(0), p.claims(0, "DEATH")
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            q = model.Projection[1]
            assert q.mort_rate(0) == pytest.approx(2 * base_annual, rel=1e-12)
            assert q.mort_rate_mth(0) == pytest.approx(
                1.0 - (1.0 - 2 * base_annual) ** (1.0 / 12.0), rel=1e-12)
            claim = q.claims(0, "DEATH")
            assert claim == pytest.approx(2 * base_claim, rel=1e-3)
            assert claim > 2 * base_claim
        finally:
            alt_path.unlink(missing_ok=True)
    finally:
        model.close()


def test_the_model_point_table_exercises_the_product(term_life):
    """Both sexes, both renewal structures, both boundaries, both forms, every module.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.
    """
    table = term_life.Data.model_point_table()
    assert len(table) == 10 and list(table.index) == list(range(1, 11))
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["renewal_type"]) == {"gaengsin", "bi_gaengsin"}
    assert set(table["contract_boundary"]) == {"ceiling", "current_term"}
    assert set(table["maturity_form"]) == {"pure", "rop"}
    assert set(table["rate_class"]) == {"standard", "nonsmoker", "preferred",
                                        "super_preferred"}
    for module in ("acc_death", "waiver", "accel", "reinstatement"):
        assert set(table[module]) == {0, 1}, f"{module} is not exercised both ways"
    assert table["issue_age"].min() == 19 and table["issue_age"].max() == 65
    assert table["sum_assured"].min() == 30000000
    assert table["sum_assured"].max() == 500000000
    assert set(table["term_y"] > 0) == {True, False}       # 년만기 and 세만기
    assert set(table["pay_term_y"] > 0) == {True, False}   # 전기납 and shortened pay
