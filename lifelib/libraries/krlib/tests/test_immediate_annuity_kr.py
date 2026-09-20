"""Golden and structural tests for Immediate_KR_S.

The golden values are the worked example in
products/immediate_annuity/technical-notes.md ("Worked example"), which projects the
anchor cell 남자 / 보험나이 60 / 일시납 ₩100,000,000 (1억원) / 종신연금형 with a ten-year
보증지급기간 on the ``decl_2017`` crediting basis — the cell that sits on the tax boundary
the product is designed around, the ₩100,000,000 being both the median of the only public
dataset and exactly the 소득세법 ten-year exemption cap.  They are hard-coded here rather
than pickled so that a reviewer can compare them against the notes by eye.

The projection runs on a **monthly** grid — ``t`` counts policy months, the annuity is the
연금월액 the contract actually pays 매월 in arrears, and the anchor's frame is 612 rows — while
the contract terms stay in years and the assumptions stay annual, which is what the paired
``mort_rate`` / ``mort_rate_mth``, ``lapse_rate`` / ``lapse_rate_mth`` and
``crediting_rate`` / ``crediting_rate_mth`` cells are for.

Tolerances follow the precision the notes display: money to the won's second decimal in the
tables and to a fraction of a won in the hand traces, in-force to six decimals, the survival
curve and the payment weight to the nine the notes print them at, mortality to eight, and
the annuity and accumulation factors to ten.

This is the library's **payout-phase chassis**, so the module carries more than a cash-flow
comparison.  A single premium arrives at inception and an annuity is in payment thereafter,
so there is no premium term, no lapse machinery of the usual kind and — the structural
difference from every other model in ``krlib`` — **no acquisition strain after t = 0**.
Three shapes are model point columns of one projection and they are three different
liabilities, so the panels the notes print for each of them are asserted beside the anchor:

* points **6 and 7** are one 상속연금형 contract on the two readings of the 만기보험금
  지급재원, which is the **즉시연금 과소지급 분쟁** in a column — the retention that stood in
  the 산출방법서 and not in the 약관, ordered away by 금융분쟁조정위원회 조정결정
  제2017-17호 and restored by the Supreme Court in 2025 for the contracts before it;
* point **8** is the only shipped point whose crediting rate is not constant, so it is the
  one that exercises the 최저보증이율 stepping and the retention being re-struck each month;
* point **9** is the 확정기간연금형, which carries no mortality in its annuity at all and is
  therefore the sharpest available test of the expense load — and the one shape on which the
  monthly grid and the annual grid it replaced agree to the won, there being no mortality for
  a monthly annuity to pick up.

Each of the twenty-one product facts the notes list under **Known modeling pitfalls** earns
its own test, named after the pitfall and naming it again in its docstring, because each of
them is a way an implementation can look right and be wrong — beginning with the two the
whole shape turns on, that ``pols_if`` is the probability a **payment obligation remains**
rather than a survival probability, and that the 보증지급기간 is a ``max`` on that
obligation and never a second stream.

The eleven ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep cannot notice a check that has quietly disappeared, and the [std] parameters
the notes state are read off the model so that a silent change to an assumption fails a test
rather than moving a result.  That every check is *True* on every shipped model point is
``test_model_conventions_kr.py``'s single sweep and is not repeated here.
"""
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
SUB_WON = 5e-7       # the hand traces' full-precision won amounts
INFORCE = 5e-7       # pols_if, displayed to 6 d.p.
PROB = 5e-10         # lives_if and payment_factor, displayed to 9 d.p.
RATE = 5e-9          # mort_rate, displayed to 8 d.p.
FACTOR = 5e-10       # annuity and accumulation factors, displayed to 10 d.p.
EXACT = 5e-13        # probabilities the notes print to 12 d.p.

MODEL_DIR = LIB / MODELS["Immediate_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "First months of the base run": t -> (pols_if, premiums, annuity_payments,
# commissions, expenses, net_cf).  claims_death, claims_lapse and claims_maturity are
# 0.00 in every row of this model point and are asserted separately, as zeros.
WORKED_EXAMPLE_CF = {
    0:   (1.000000, 100000000.00, 403369.60, 2000000.00, 1503226.96, 96093403.44),
    1:   (1.000000, 0.00, 403369.60, 0.00, 3226.96, -406596.56),
    2:   (1.000000, 0.00, 403369.60, 0.00, 3226.96, -406596.56),
    11:  (1.000000, 0.00, 403369.60, 0.00, 3226.96, -406596.56),
    12:  (1.000000, 0.00, 403369.60, 0.00, 3226.96, -406596.56),
    119: (1.000000, 0.00, 403369.60, 0.00, 3226.96, -406596.56),
    120: (0.953470, 0.00, 384366.72, 0.00, 3074.93, -387441.65),
    121: (0.952890, 0.00, 384132.75, 0.00, 3073.06, -387205.82),
    239: (0.837189, 0.00, 337076.63, 0.00, 2696.61, -339773.24),
    240: (0.835652, 0.00, 336364.96, 0.00, 2690.92, -339055.88),
    359: (0.493177, 0.00, 197347.75, 0.00, 1578.78, -198926.53),
    360: (0.489248, 0.00, 195517.24, 0.00, 1564.14, -197081.38),
    479: (0.043078, 0.00, 16736.70, 0.00, 133.89, -16870.60),
    480: (0.041492, 0.00, 16019.08, 0.00, 128.15, -16147.23),
    600: (0.000000, 0.00, 0.12, 0.00, 0.00, -0.13),
    611: (0.000000, 0.00, 0.00, 0.00, 0.00, 0.00),
}

# "The state behind those rows, from result_pols()":
# t -> (보험나이, mort_rate, mort_rate_mth, lives_if, payment_factor, av_pp).  annuity_pp
# is 403,369.60 in every row and is asserted once, as the level it is.  ``mort_rate`` is
# the **annual** rate the table publishes, level across the twelve months of a policy year;
# ``mort_rate_mth`` is the uniform-force conversion the projection applies.
WORKED_EXAMPLE_STATE = {
    0:   (60, 0.00353000, 0.0002946437, 1.000000000, 1.000000000, 96500000.00),
    1:   (60, 0.00353000, 0.0002946437, 0.999705356, 1.000000000, 96295404.60),
    11:  (60, 0.00353000, 0.0002946437, 0.996763690, 1.000000000, 94226127.93),
    12:  (61, 0.00369813, 0.0003087008, 0.996470000, 1.000000000, 94016848.73),
    119: (69, 0.00659390, 0.0005511592, 0.953995829, 1.000000000, 68941669.34),
    120: (70, 0.00728000, 0.0006087004, 0.953470025, 0.952889648, 68680308.29),
    121: (70, 0.00728000, 0.0006087004, 0.952889648, 0.952309623, 68418408.87),
    239: (79, 0.02181222, 0.0018361145, 0.837189204, 0.835652028, 33403315.14),
    240: (80, 0.02504325, 0.0021112823, 0.835652028, 0.833887731, 33068750.90),
    359: (89, 0.09151992, 0.0079666234, 0.493176902, 0.489247948, -12088782.79),
    360: (90, 0.10580035, 0.0092755649, 0.489247948, 0.484709897, -12517053.30),
    479: (99, 0.36237864, 0.0368064377, 0.043077769, 0.041492230, -70322514.23),
    480: (100, 0.40896710, 0.0428772519, 0.041492230, 0.039713157, -70870736.70),
    600: (110, 1.00000000, 0.0833333333, 0.000000338, 0.000000309, -145568384.91),
    611: (110, 1.00000000, 1.0000000000, 0.000000028, 0.000000000, -153383930.43),
}

# "Derived quantities at inception, at the precision the model produces them", and the
# hand traces' intermediate values, at the precision the notes print them.
AV_PP_INIT = 96500000.0000000000
ANNUITY_FACTOR = 239.2346855912        # the **monthly** annuity factor, ~12 x the annual
FACTOR_GUARANTEED = 106.2228107533     # SUM t=0..119 v^(t+1), the annuity-certain half
FACTOR_TAIL = 133.0118748379           # SUM t=120..611 v^(t+1) l(t+1), the life half
ANNUITY_PP = 403369.6023698976         # the 연금월액, what a row actually pays
ANNUITY_PP_ANNUAL = 4840435.2284387713  # the 연금연액 an illustration quotes, 12 x it
PROJ_LEN = 612                         # the row count; the last row index is 611
PROJ_YEARS = 51                        # the same horizon in policy years
CREDITING_RATE_MTH = 0.0020598363      # (1.025)^(1/12) - 1
EXPENSE_CHARGE = 3226.9568189592       # 0.80% of the 연금월액, at a weight of one
EXPENSES_0 = 1503226.9568189592
NET_CF_0 = 96093403.4408111423
NET_CF_1 = -406596.5591888567
AV_PP_1 = 96295404.5976699144
AV_PP_1_CREDITED = 96698774.2000398189  # V(0) x (1 + j), before the instalment
ANN_120 = 384366.7182455019
EXPENSES_120 = 3074.9337459640
NET_CF_120 = -387441.6519914659
POLS_IF_120 = 0.953470025140           # l(120): the obligation after the guarantee
PAYMENT_FACTOR_120 = 0.952889647577    # l(121): the first payment the guarantee misses
POLS_EXIT_119 = 0.046529974860         # the whole cohort that died inside the guarantee
AV_PP_324 = 2358767.07                 # the last month-end at which the fund is positive
AV_PP_330 = -44645.38                  # six months later, and negative for good
AV_PP_611 = -153383930.43
ANN_611 = 0.00                         # the terminal row, where the weight has reached 0
PAYMENT_FACTOR_611 = 0.000000000

# "Undiscounted totals", over t = 0 … 611, per policy, income-positive.
TOTALS = {
    "pols_if": 341.116217,
    "premiums": 100000000.00,
    "annuity_payments": 137211311.88,
    "claims_death": 0.00,
    "claims_lapse": 0.00,
    "claims_maturity": 0.00,
    "commissions": 2000000.00,
    "expenses": 2597690.50,
    "liability_cf": 41809002.38,
    "net_cf": -41809002.38,
}
SUM_LIVES = 338.649237                 # Σ l(t) over t = 0 … 611, in months
SUM_LIVES_GUARANTEE = 117.533020       # Σ l(t) over t = 0 … 119
GUARANTEE_MONTHS_ADDED = 2.466980      # 120 − Σ l(t) inside the guarantee
ACQ_EXPENSE_0 = 1500000.00             # the day-one acquisition and admin expense
ANNUITY_CHARGE_TOTAL = 1097690.50      # 0.0080 x the annuity total
BREAK_EVEN_MONTH = 263                 # the month the annuity total passes the premium
CUM_ANNUITY_262 = 99745332.34          # below the premium at the end of row 262
CUM_ANNUITY_263 = 100064499.96         # above it at the end of row 263

# The readings of the factor the notes take, and the reconciliation to the annual grid.
GROSS_FACTOR = 20.6593                 # P / the 연금연액; the published 23.81 / 23.15 at 55
GROSS_PREMIUM_ANNUITY = 417999.587948  # P / ä, had the gross premium been converted
LOAD_FROM_THE_INCOME_SIDE = 0.0362694  # 3.63%: the 3.50% load grossed up by itself
FACTOR_NO_GUARANTEE = 237.109770
ANNUITY_NO_GUARANTEE = 406984.50       # a month, with no 보증지급기간 at all
GUARANTEE_COST = 0.008882              # 0.89% of income, for ten guaranteed months-in-120
E60_COMPLETE = 28.2208                 # complete e(60) in years, Σ l(t) / 12
I_TWELVE = 0.024718035238              # i^(12) at 2.50%
I_OVER_I_TWELVE = 1.0114072482
ANNUAL_STEP_ANNUITY = 4948039.1569365682  # what the annual-step model solved for
ANNUAL_STEP_MONTHLY_NAIVE = 412336.60     # that annuity / 12
ANNUAL_STEP_MONTHLY_TRUE = 407686.02      # its monthly-in-arrears equal-value equivalent
MODAL_EFFECT = 0.9894123972               # ANNUITY_PP / ANNUAL_STEP_MONTHLY_TRUE

# Pitfall 2: the additive construction, and what it would pay.
ADDITIVE_FACTOR = 343.332581
ADDITIVE_ANNUITY = 281068.58
ADDITIVE_SHARE = 0.6968                # 69.68% of the right answer, for life

# Pitfall 5: reading q at the attained age at the **end** of the policy year.
WRONG_END_ANNUITY = 412381.78
WRONG_END_UPLIFT = 0.0223422           # +2.23%

# ---------------------------------------------------------------------------
# The dispute panel — model points 6 and 7, one contract on two bases

AV_PP_INIT_LOADED = 95029999.9999999851   # P (1 − 0.0350 − 0.0147), the two other shapes
MATURITY_BENEFIT = 100000000.00           # 만기보험금 = the **gross** single premium
S_120_MTH = 135.9741782864                # s(120, j), the retention's denominator
DISC_120 = 0.781198401726                 # v(120) on the crediting path

# t = 0 hand trace, as designed (point 6) and as ordered (point 7).
DESIGNED = {
    "annuity_pp": 159195.1832897901,
    "retention_pp": 36551.0574333656,
    "av_pp_1": 95066551.0574333519,
    "payment_factor": 0.9997053563200,
    "annuity_payments": 159148.2774351536,
    "pols_death": 0.0002946436800,
    "claims_death": 30957.1952443041,
    "pols_lapse": 0.0016816469201,
    "claims_lapse": 159868.3727871836,
    "expenses": 1501273.1862194813,
    "net_cf": 96148752.9683138877,
}
ORDERED = {
    "annuity_pp": 195746.2407231556,
    "retention_pp": 0.0,
    "av_pp_1": 95029999.9999999851,
    "payment_factor": 0.9997053563200,
    "annuity_payments": 195688.5653304506,
    "pols_death": 0.0002946436800,
    "claims_death": 30946.4257062355,
    "pols_lapse": 0.0016816469201,
    "claims_lapse": 159806.9068140256,
    "expenses": 1501565.5085226437,
    "net_cf": 96111992.5936266482,
}

# "The two liabilities side by side", undiscounted totals.
DISPUTE_TOTALS = {
    6: {"annuity_payments": 16976657.3468, "claims_death": 4494012.5082,
        "claims_lapse": 15854560.3876, "claims_maturity": 79495349.9719,
        "expenses": 1635813.2588, "net_cf": -20456393.4733},
    7: {"annuity_payments": 20874481.1684, "claims_death": 4385780.0077,
        "claims_lapse": 15517362.9412, "claims_maturity": 79495349.9719,
        "expenses": 1666995.8493, "net_cf": -23939969.9386},
}
DISPUTE_NET_CF_DIFFERENCE = -3483576.4653
RETENTION_SHORTFALL = 3882556.0565769221
ANNUITY_UPLIFT_AS_ORDERED = 0.2296            # +22.96% of income on one boolean
DESIGNED_ANNUAL = 1910342.20                  # 12 x the 연금월액
ORDERED_ANNUAL = 2348954.89
RETENTION_PATH = [                            # R(12y), y = 0 … 9, on point 6
    36551.06, 37464.83, 38401.45, 39361.49, 40345.53,
    41354.17, 42388.02, 43447.72, 44533.91, 45647.26,
]
RETENTION_PATH_MONTHS = [                     # R(t), t = 0 … 11: it rises every month
    36551.06, 36626.35, 36701.79, 36777.39, 36853.15, 36929.06,
    37005.13, 37081.35, 37157.73, 37234.27, 37310.97, 37387.82,
]
MATURITY_EARLIER_WEIGHT = 79539188.73         # pitfall 18: IF(N−1) M instead of IF(N) M

# ---------------------------------------------------------------------------
# The floor-stepping panel — model point 8, 여자 70, 상속연금형 20년, min_guar

# t -> (crediting_rate, annuity_pp, retention_pp, av_pp)
FLOOR_STEP = {
    0:   (0.0125, 80175.2482050112, 18251.6955717737, 95030000.00),
    48:  (0.0125, 80175.2482050129, 19181.5343519293, 95927747.87),
    59:  (0.0125, 80175.2482050133, 19401.2088066262, 96139840.85),
    60:  (0.0100, 59974.7776499095, 19792.9786825209, 96159242.06),
    119: (0.0100, 59974.7776499096, 20785.3772540911, 97355568.73),
    120: (0.0075, 39588.3970942395, 21063.6142111074, 97376354.11),
    228: (0.0075, 39588.3970942428, 22528.8168917276, 99728726.14),
    239: (0.0075, 39588.3970942352, 22683.6542366892, 99977316.35),
}
S_240_AT_125 = 272.3034679411
S_180_AT_100 = 194.0464851297
AV_PP_59_POINT_8 = 96139840.8476033062
AV_PP_60_POINT_8 = 96159242.0564099401
AV_PP_240_POINT_8 = 100000000.00
FIRST_STEP_FALL = -0.2520               # −25.20% on a −20.0% move in the rate
SECOND_STEP_FALL = -0.3399              # −33.99%
TWO_STEP_FALL = -0.5062                 # −50.62% from the first month to the 121st
FLOOR_MONTHLY = (80175.25, 39588.40)

# ---------------------------------------------------------------------------
# The load cross-check — model point 9, 확정기간연금형 10년

A_120_MTH = 106.2228107533
CERTAIN_ANNUITY = 894628.9344641458     # a month
CERTAIN_ANNUITY_ANNUAL = 10735547.21
CERTAIN_PUBLISHED = 900000.0            # 교보's published 90만원 a month
CERTAIN_LAST_INSTALMENT = 745894.87     # 0.77% of the annuity total, not 9.1%
CERTAIN_TOTALS = {
    "annuity_payments": 97370154.63,
    "claims_death": 417574.03,
    "claims_lapse": 9187258.64,
    "expenses": 2278961.24,
    "net_cf": -11253948.54,
}

# ---------------------------------------------------------------------------
# The eleven check cells this model publishes, and the six that carry a residual

CHECKS = {
    "check_annuity_basis",
    "check_av_roll_fwd",
    "check_av_terminal",
    "check_guarantee_certain",
    "check_lives_roll_fwd",
    "check_net_cf",
    "check_payment_factor",
    "check_pols_roll_fwd",
    "check_premium_split",
    "check_rate_level",
    "check_surr_value",
}
CHECKS_WITH_RESID = {
    "check_annuity_basis",     # the only residual taking no argument: it is one number
    "check_av_roll_fwd",
    "check_lives_roll_fwd",
    "check_net_cf",
    "check_payment_factor",
    "check_pols_roll_fwd",
}

# The charge basis, by shape, every rate of it [std] in its adoption or its derivation.
CHARGE_RATES = {
    "life": {"acq_charge_rate": 0.0220, "admin_charge_rate": 0.0130,
             "risk_prem_rate": 0.0000, "comm_rate": 0.0200,
             "acq_expense_rate": 0.0150, "annuity_charge_rate": 0.0080,
             "db_rate": 0.00},
    "inheritance": {"acq_charge_rate": 0.0220, "admin_charge_rate": 0.0130,
                    "risk_prem_rate": 0.0147, "comm_rate": 0.0200,
                    "acq_expense_rate": 0.0150, "annuity_charge_rate": 0.0080,
                    "db_rate": 0.10},
    "certain": {"acq_charge_rate": 0.0220, "admin_charge_rate": 0.0130,
                "risk_prem_rate": 0.0147, "comm_rate": 0.0200,
                "acq_expense_rate": 0.0150, "annuity_charge_rate": 0.0080,
                "db_rate": 0.10},
}

# The 최저보증이율 schedule, by the **month** whose completed policy year the band
# contains: the table is published in years and the grid reads it at ``t // 12``.
MIN_GUAR_SCHEDULE = {0: 0.0125, 59: 0.0125, 60: 0.0100, 119: 0.0100,
                     120: 0.0075, 360: 0.0075}
DECL_RATE = 0.0250
OMEGA_AGE = 110

# "The ten shipped model points": point_id -> (proj_len(), proj_years()), the notes' own
# column, as a month count and the policy years it covers; the last row index is one less.
SHIPPED_HORIZONS = {1: (612, 51), 2: (612, 51), 3: (612, 51), 4: (792, 66), 5: (372, 31),
                    6: (120, 10), 7: (120, 10), 8: (240, 20), 9: (120, 10), 10: (360, 30)}

# The two published 개인연금사망률 the construction reproduces exactly, per sex.
SOURCED_MORT_ANCHORS = {("M", 60): 0.00353, ("M", 70): 0.00728,
                        ("F", 60): 0.00118, ("F", 70): 0.00251}


def _true_monthly(annual, rate=0.025):
    """The monthly-in-arrears annuity of the same present value as an annual one.

    ``A / 12 x i^(12) / i``.  This is the **interest-only** conversion: it is what the
    annual-step model's 연금연액 was worth as a monthly instalment ignoring the mortality
    the monthly mode picks up, and it is worth 1.14% at 2.50% against a naive ``A / 12``.
    The model now pays a monthly instalment directly, so this function survives for exactly
    two purposes: reconciling against the annual-step model this replaced, and converting
    a carrier's published annual figure where only an annual figure is published.  On a
    shape with no mortality in its annuity — the 확정기간연금형 — the conversion is exact
    and the model reproduces it to the won.
    """
    i12 = 12.0 * ((1.0 + rate) ** (1.0 / 12.0) - 1.0)
    return annual / 12.0 * (i12 / rate)


# ---------------------------------------------------------------------------
# The worked example — the quantities struck at inception


def test_worked_example_annuity_factor_decomposition(kr_immediate_anchor):
    """ä(60, 10, 2.5%) = 106.222810753287 + 133.011874837888, and only the second half reads.

    The factor is the one quantity in the notes a reader cannot check by inspection, so it
    is decomposed there and asserted here.  It is a **monthly** annuity factor — about twelve
    times an annual one — because the grid pays a 연금월액 매월, and the first sum is exactly
    the monthly annuity-certain ``a(120, j)`` over the 보증지급기간's 120 months, because
    inside the guarantee the weight is one whatever the annuitant does; 44.4% of the factor
    is that certain block and 55.6% is the life-contingent tail.
    """
    a = kr_immediate_anchor
    j = a.crediting_rate_mth(0)
    v = 1.0 / (1.0 + j)
    g = a.annuity_term_mths()
    guaranteed = sum(v ** (t + 1) * a.pricing_factor(t) for t in range(0, g))
    tail = sum(v ** (t + 1) * a.pricing_factor(t) for t in range(g, a.proj_len()))
    assert g == 120
    assert guaranteed == pytest.approx(FACTOR_GUARANTEED, abs=FACTOR)
    assert guaranteed == pytest.approx(a.annuity_factor_certain(g, j), abs=FACTOR)
    assert tail == pytest.approx(FACTOR_TAIL, abs=FACTOR)
    assert guaranteed + tail == pytest.approx(a.annuity_factor(), rel=1e-14)
    assert guaranteed / a.annuity_factor() == pytest.approx(0.444, abs=5e-4)
    assert tail / a.annuity_factor() == pytest.approx(0.556, abs=5e-4)
    # Only the tail reads the mortality table: inside the guarantee the weight is one.
    assert all(a.pricing_factor(t) == 1.0 for t in range(0, g))
    assert all(a.pricing_factor(t) < 1.0 for t in range(g, a.proj_len()))


def test_worked_example_the_three_readings_of_the_factor(kr_immediate_anchor):
    """The gross factor of 20.6593, the 3.63% load and the 0.89% the guarantee costs.

    Three sanity checks the notes take on a number that cannot be compared with a published
    one, no carrier publishing an annuity factor.  The premium divided by the **annual**
    annuity is 20.6593 against implied factors of 23.81 and 23.15 at 55 — not comparable as
    they stand, and the notes run the model onto 교보's own cell rather than waving at the
    age difference; converting the **gross** premium rather than the fund would raise the
    annuity by 3.63%, the 3.50% load grossed up by itself, a ratio that is invariant to the
    grid; and the same fund with no 보증지급기간 at all buys ₩406,984.50 a month instead of
    ₩403,369.60, so ten guaranteed years cost **0.89% of income** — the quantitative reason
    97.3% of life-shape buyers take them.  On the annual grid the same guarantee cost 0.99%,
    and the difference is real: a monthly annuity already pays part-year instalments to a
    life that dies inside a year, so there is less for the guarantee to add.  Ten years also
    sits far inside the complete ``e(60)`` of 28.2208 years on the shipped table, the
    소득세법 시행령 제25조제4항제3호 test a tax-exempt 종신형 must clear.
    """
    a = kr_immediate_anchor
    assert a.prem_pp() / a.annuity_pp_annual(0) == pytest.approx(GROSS_FACTOR, abs=5e-5)
    gross = a.prem_pp() / a.annuity_factor()
    assert gross == pytest.approx(GROSS_PREMIUM_ANNUITY, abs=WON)
    assert gross / a.annuity_pp(0) - 1.0 == pytest.approx(
        LOAD_FROM_THE_INCOME_SIDE, abs=5e-7)
    assert gross / a.annuity_pp(0) - 1.0 == pytest.approx(
        0.0350 / (1.0 - 0.0350), rel=1e-12)
    v = 1.0 / (1.0 + a.crediting_rate_mth(0))
    no_guarantee = sum(v ** (t + 1) * a.lives_if(t + 1)
                       for t in range(0, a.proj_len()))
    assert no_guarantee == pytest.approx(FACTOR_NO_GUARANTEE, abs=5e-6)
    assert a.av_pp_init() / no_guarantee == pytest.approx(ANNUITY_NO_GUARANTEE, abs=WON)
    assert 1.0 - a.annuity_pp(0) / (a.av_pp_init() / no_guarantee) == pytest.approx(
        GUARANTEE_COST, abs=5e-6)
    # e(60) is a number of **years**, so the monthly survival sum is divided by twelve.
    complete = sum(a.lives_if(t) for t in range(0, a.proj_len())) / 12.0
    assert complete == pytest.approx(E60_COMPLETE, abs=5e-5)
    assert a.annuity_term() < complete


def test_worked_example_monthly_reconciliation(kr_immediate_anchor):
    """The model pays ₩403,369.60 a month where the annual-step model implied ₩407,686.02.

    The reconciliation against the annual grid this replaced, and it does not close on
    interest alone.  The annual-step model solved a 연금연액 of ₩4,948,039.16 payable once a
    year in arrears; converting it to a monthly-in-arrears instalment of the same present
    value — ``A / 12 x i^(12) / i``, the 1.14% of within-year interest the monthly mode pays
    and the annual mode does not, which is exactly the 「신공시이율로 계산한 이자를
    가산합니다」 of the two carriers who state it — gives ₩407,686.02.  The model's own
    monthly annuity is **1.06% below that**, and the residual is mortality, not interest: a
    monthly annuity pays part-year instalments to a life that dies inside a policy year,
    where an annual-in-arrears annuity pays that life nothing for the year, so the monthly
    obligation is genuinely larger and the same fund buys less of it.  The interest-only
    conversion is exact only where no mortality enters the annuity at all, which is the
    확정기간연금형 and is asserted there.
    """
    a = kr_immediate_anchor
    i = a.crediting_rate(0)
    i12 = 12.0 * ((1.0 + i) ** (1.0 / 12.0) - 1.0)
    assert i12 == pytest.approx(I_TWELVE, abs=5e-13)
    assert i / i12 == pytest.approx(I_OVER_I_TWELVE, abs=5e-11)
    assert a.crediting_rate_mth(0) == pytest.approx(CREDITING_RATE_MTH, abs=5e-10)
    assert (1.0 + a.crediting_rate_mth(0)) ** 12 - 1.0 == pytest.approx(i, rel=1e-13)
    assert ANNUAL_STEP_ANNUITY / 12.0 == pytest.approx(
        ANNUAL_STEP_MONTHLY_NAIVE, abs=WON)
    assert _true_monthly(ANNUAL_STEP_ANNUITY) == pytest.approx(
        ANNUAL_STEP_MONTHLY_TRUE, abs=WON)
    assert a.annuity_pp(0) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.annuity_pp(0) / ANNUAL_STEP_MONTHLY_TRUE == pytest.approx(
        MODAL_EFFECT, abs=5e-8)
    assert a.annuity_pp(0) < ANNUAL_STEP_MONTHLY_TRUE < ANNUAL_STEP_MONTHLY_NAIVE


def test_worked_example_assumption_table(kr_immediate_anchor):
    """The notes' "assumption values used, in full, with tags", read off the model.

    Every quantitative parameter of the anchor cell in one place, so that a change to any
    of them fails a test rather than moving a result.  Three of the rows are contractual and
    the rest are [std] in their adoption; which is which is in the notes and in the CSVs'
    ``provenance`` columns, not here.
    """
    a = kr_immediate_anchor
    assert a.acq_charge_rate() == 0.0220
    assert a.admin_charge_rate() == 0.0130
    assert a.expense_load_rate() == pytest.approx(0.0350, rel=1e-15)
    assert a.risk_prem_rate() == 0.0000
    assert a.comm_rate() == 0.0200
    assert a.acq_expense_rate() == 0.0150
    assert a.annuity_charge_rate() == 0.0080
    assert a.db_rate() == 0.00
    assert a.decl_rate() == DECL_RATE
    assert [a.min_guar_rate(t) for t in (0, 59, 60, 119, 120, 600)] == [
        0.0125, 0.0125, 0.0100, 0.0100, 0.0075, 0.0075]
    assert all(a.crediting_rate(t) == DECL_RATE for t in range(0, a.proj_len()))
    assert a.mort_rate(0) == 0.00353 and a.mort_rate(120) == 0.00728
    assert all(a.lapse_rate(t) == 0.0 for t in range(0, a.proj_len()))
    assert all(a.lapse_rate_mth(t) == 0.0 for t in range(0, a.proj_len()))
    assert a.shape() == "life" and a.sex() == "M" and a.age_at_entry() == 60
    assert a.prem_pp() == 100000000.0 and a.annuity_term() == 10
    assert a.annuity_term_mths() == 120
    assert a.crediting_basis() == "decl_2017" and a.pols_if_init() == 1.0


# ---------------------------------------------------------------------------
# The worked example — the cash flow statement and the state behind it


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_worked_example_cash_flow_row(kr_immediate_anchor, t):
    """Every cell of the notes' twenty-one-row cash flow table, to the displayed precision.

    Asserted against the cells **and** against the published ``result_cf()`` row, because a
    column that dropped out of the frame would leave the cells intact and the statement
    wrong — and the statement is what a reader of the notes is holding.
    """
    pols, prem, ann, comm, exp, net = WORKED_EXAMPLE_CF[t]
    a = kr_immediate_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=WON)
    assert a.annuity_payments(t) == pytest.approx(ann, abs=WON)
    assert a.commissions(t) == pytest.approx(comm, abs=WON)
    assert a.expenses(t) == pytest.approx(exp, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)
    row = a.result_cf().loc[t]
    assert row["pols_if"] == pytest.approx(pols, abs=INFORCE)
    assert row["premiums"] == pytest.approx(prem, abs=WON)
    assert row["annuity_payments"] == pytest.approx(ann, abs=WON)
    assert row["commissions"] == pytest.approx(comm, abs=WON)
    assert row["expenses"] == pytest.approx(exp, abs=WON)
    assert row["net_cf"] == pytest.approx(net, abs=WON)
    assert row["liability_cf"] == pytest.approx(-net, abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_STATE))
def test_worked_example_state_row(kr_immediate_anchor, t):
    """Every cell of the notes' state table from ``result_pols()``, at its own precision.

    The attained 보험나이, the **annual** 개인연금사망률 at it, the monthly conversion the
    projection applies, the survival probability, the payment weight and the 계약자적립액 —
    the six quantities the cash flow rows are built out of.  The annuity is level at
    ₩403,369.60 a month in every row and is asserted as the level it is.
    """
    age, q, q_mth, lives, weight, av = WORKED_EXAMPLE_STATE[t]
    a = kr_immediate_anchor
    assert a.age(t) == age == a.age_at_entry() + t // 12
    assert a.policy_year(t) == t // 12 + 1
    assert a.mort_rate(t) == pytest.approx(q, abs=RATE)
    assert a.mort_rate_mth(t) == pytest.approx(q_mth, abs=RATE)
    # Twelve monthly decrements compound back to exactly the year's annual rate, except at
    # the limiting age, where the certain death is spread uniformly over the year instead.
    # The round trip is driven from the model's own annual rate rather than from the
    # eight-decimal constant above, which could not carry it.
    if q < 1.0:
        assert 1.0 - (1.0 - a.mort_rate_mth(t)) ** 12 == pytest.approx(
            a.mort_rate(t), rel=1e-13)
        assert a.mort_rate_mth(t) > a.mort_rate(t) / 12.0
    else:
        assert a.mort_rate_mth(t) == pytest.approx(1.0 / (12 - t % 12), rel=1e-13)
    assert a.lives_if(t) == pytest.approx(lives, abs=PROB)
    assert a.payment_factor(t) == pytest.approx(weight, abs=PROB)
    assert a.av_pp(t) == pytest.approx(av, abs=WON)
    assert a.annuity_pp(t) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    row = a.result_pols().loc[t]
    assert row["lives_if"] == pytest.approx(lives, abs=PROB)
    assert row["payment_factor"] == pytest.approx(weight, abs=PROB)
    assert row["av_pp"] == pytest.approx(av, abs=WON)
    assert row["cv_pp"] == 0.0                 # nil at every t, and omitted from the notes
    assert row["surr_if"] == 1.0               # surrender is contractually impossible
    assert row["crediting_rate"] == DECL_RATE  # the **annual** rate, as published


def test_the_three_claims_columns_are_zero_at_every_t(kr_immediate_anchor):
    """claims_death, claims_lapse and claims_maturity are 0.00 in every row, as columns.

    Each zero is a product fact — no death benefit after annuitisation, no surrender at all,
    no maturity on a 종신연금형 — and each is published as a column all the same, because a
    statement whose columns appear and disappear with the model point cannot be compared
    across model points.  The notes omit them from the printed table and say so; omitting
    them from the *frame* would be a different statement.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    for column in ("claims_death", "claims_lapse", "claims_maturity"):
        assert column in df.columns
        assert (df[column] == 0.0).all(), column
    assert all(a.claims(t, "DEATH") == 0.0 for t in range(0, a.proj_len()))
    assert all(a.claims(t, "LAPSE") == 0.0 for t in range(0, a.proj_len()))
    assert all(a.claims(t, "MATURITY") == 0.0 for t in range(0, a.proj_len()))


# ---------------------------------------------------------------------------
# The worked example — the hand traces


def test_worked_example_period_zero_trace(kr_immediate_anchor):
    """The notes' period-0 trace, line by line, at full precision.

    The six quantities struck at inception open it — V(0), ä, A(0), B, M and N — and
    everything else on the anchor cell is a function of them and of the mortality table, so
    an error in any one of them moves every row of the statement; ``N`` is 12(ω − x + 1) =
    12 x (110 − 60 + 1) = 612 and is a **month count, not a last row index**, which is the
    pitfall the notes list fourth.

    V(0) = P(1 − c − b); ä decomposed; A(0) = V(0)/ä; F(0) = max(l(1), 1{1 ≤ 120}) = 1;
    ANN(0) = A(0); COM(0) = 0.0200 P; EXP(0) = 0.0150 P + 0.0080 A(0); and net_cf(0) =
    +₩96,093,403.44, the only positive row in the statement.  **The premium split reads
    straight off this line**: ₩2,000,000 of commission and ₩1,500,000 of expense sum to the
    ₩3,500,000 deducted from the premium to make V(0), with nothing left over in either
    direction, which is what "no acquisition strain" means arithmetically.
    """
    a = kr_immediate_anchor
    assert a.av_pp_init() == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert a.av_pp_init() == pytest.approx(
        a.prem_pp() * (1.0 - 0.0350 - 0.0000), rel=1e-15)
    assert a.annuity_factor() == pytest.approx(ANNUITY_FACTOR, abs=FACTOR)
    assert a.annuity_factor() == pytest.approx(
        FACTOR_GUARANTEED + FACTOR_TAIL, abs=FACTOR)
    assert a.annuity_pp(0) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.annuity_pp(0) == pytest.approx(
        a.av_pp_init() / a.annuity_factor(), rel=1e-15)
    assert a.annuity_pp_annual(0) == pytest.approx(ANNUITY_PP_ANNUAL, abs=SUB_WON)
    assert a.risk_prem_pp() == 0.0 and a.maturity_benefit() == 0.0
    assert a.retention_shortfall_pp() == 0.0
    assert a.proj_years() == PROJ_YEARS == OMEGA_AGE - a.age_at_entry() + 1
    assert a.proj_len() == PROJ_LEN == 12 * PROJ_YEARS == 612
    assert len(a.result_cf()) == PROJ_LEN
    assert a.payment_factor(0) == pytest.approx(1.0, abs=EXACT)
    assert a.payment_factor(0) == max(a.lives_if(1), 1.0)
    assert a.lives_if(1) == pytest.approx(0.9997053563200, abs=EXACT)
    assert a.annuity_payments(0) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.premiums(0) == 100000000.0
    assert a.commissions(0) == pytest.approx(2000000.0, abs=SUB_WON)
    assert a.expenses(0) == pytest.approx(EXPENSES_0, abs=SUB_WON)
    assert a.expenses(0) - ACQ_EXPENSE_0 == pytest.approx(EXPENSE_CHARGE, abs=SUB_WON)
    assert a.net_cf(0) == pytest.approx(NET_CF_0, abs=SUB_WON)
    assert a.net_cf(0) == pytest.approx(
        100000000.0 - ANNUITY_PP - 2000000.0 - EXPENSES_0, abs=SUB_WON)
    # The split, read off the same line.
    assert a.check_premium_split() is True
    assert (a.commissions(0) + ACQ_EXPENSE_0 + a.risk_prem_pp()
            + a.av_pp_init()) == pytest.approx(a.prem_pp(), abs=SUB_WON)
    assert a.commissions(0) + ACQ_EXPENSE_0 == pytest.approx(
        a.expense_load_rate() * a.prem_pp(), abs=SUB_WON)


def test_worked_example_period_one_trace(kr_immediate_anchor):
    """The notes' month-1 trace: the recursion runs, and the annuity does not move.

    V(1) = V(0)(1 + j) − A(0) = 96,698,774.2000398189 − 403,369.6023698976 where ``j`` is
    the monthly crediting rate; l(1) = 1 − q^m(60); F(1) is again one, the guarantee covering
    the payment at the end of month 1; and A(1) is A(0), struck once at commencement against
    「연금개시시의 계약자적립액」.  **The fund is falling by about ₩2.5m a year and has no
    contractual role at all on this shape.**  Rows 1 to 119 are this row repeated to the last
    digit, because nothing inside the guarantee moves but the fund.
    """
    a = kr_immediate_anchor
    assert a.av_pp(0) * (1.0 + a.crediting_rate_mth(0)) == pytest.approx(
        AV_PP_1_CREDITED, abs=SUB_WON)
    assert a.av_pp(1) == pytest.approx(AV_PP_1, abs=SUB_WON)
    assert a.av_pp(1) == pytest.approx(
        a.av_pp(0) * (1.0 + a.crediting_rate_mth(0)) - a.annuity_pp(0), rel=1e-15)
    assert a.lives_if(1) == pytest.approx(1.0 * (1.0 - a.mort_rate_mth(0)), rel=1e-15)
    assert a.payment_factor(1) == pytest.approx(1.0, abs=EXACT)
    assert a.annuity_pp(1) == a.annuity_pp(0)
    assert a.annuity_payments(1) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.expenses(1) == pytest.approx(EXPENSE_CHARGE, abs=SUB_WON)
    assert a.net_cf(1) == pytest.approx(NET_CF_1, abs=SUB_WON)
    # Rows 1 to 119 are identical, and the fund alone moves.
    assert all(a.net_cf(t) == pytest.approx(NET_CF_1, abs=SUB_WON) for t in range(1, 120))
    assert 2.4e6 < a.av_pp(1) - a.av_pp(13) < 2.6e6     # "roughly 2.5m a year"
    assert all(a.av_pp(t) > a.av_pp(t + 1) for t in range(0, 120))


def test_worked_example_period_ten_guarantee_cliff_trace(kr_immediate_anchor):
    """The notes' month-120 trace: **two different things step, to two different numbers**.

    IF steps from 1.000000 to l(120) = 0.953470025140 — everyone who died in the first ten
    years leaves the obligation at once, and ``pols_exit(119)`` is that whole cohort,
    0.046529974860, in a single month.  Both figures are the annual-step model's to the last
    printed digit, because twelve monthly decrements compound to the year's.  The payment
    weight steps to l(121) = 0.952889647577, because the payment on row 120 falls at the end
    of month 120 and is the first one the guarantee does not cover.  The cash flow falls
    4.71% between rows 119 and 120 and a further 0.06% between rows 120 and 121: the first
    step is the guarantee expiring, the second is one **month** of mortality — where the
    annual grid's second step was a whole year's.
    """
    a = kr_immediate_anchor
    assert a.pols_if(119) == pytest.approx(1.0, abs=EXACT)
    assert a.pols_if(120) == pytest.approx(POLS_IF_120, abs=EXACT)
    assert a.pols_if(120) == a.lives_if(120)
    assert a.pols_exit(119) == pytest.approx(POLS_EXIT_119, abs=EXACT)
    assert a.pols_exit(119) == pytest.approx(
        a.pols_if_init() - a.lives_if(120), rel=1e-14)
    assert a.pols_if(119) - a.pols_exit(119) - a.pols_if(120) == pytest.approx(
        0.0, abs=1e-14)
    assert a.payment_factor(120) == pytest.approx(PAYMENT_FACTOR_120, abs=EXACT)
    assert a.payment_factor(120) == a.lives_if(121)
    assert a.pols_if(120) != a.payment_factor(120)
    assert a.annuity_payments(120) == pytest.approx(ANN_120, abs=SUB_WON)
    assert a.expenses(120) == pytest.approx(EXPENSES_120, abs=SUB_WON)
    assert a.net_cf(120) == pytest.approx(NET_CF_120, abs=SUB_WON)
    assert a.net_cf(120) / a.net_cf(119) - 1.0 == pytest.approx(-0.0471, abs=5e-5)
    assert a.net_cf(121) / a.net_cf(120) - 1.0 == pytest.approx(-0.0006, abs=5e-5)


def test_worked_example_the_tail_and_the_fund_that_goes_negative(kr_immediate_anchor):
    """The 계약자적립액 crosses zero between t = 324 and t = 330, and that is not a defect.

    V(324) = ₩2,358,767.07 and V(330) = −₩44,645.38, falling to −₩153,383,930.43 at
    t = 611.  A life annuity's fund is not its reserve: the annuitant still alive at 87 is
    being paid out of the mortality of the cohort he was priced with.  The monthly grid also
    dates the crossing properly — it happens *inside* the twenty-eighth policy year, not at
    its boundary, which is all an annual grid could say.  At the far end
    ``lives_if(612)`` is exactly zero: q(110) = 1 and the monthly conversion spreads that
    certain death over the twelve months of the limiting age's policy year, so the last of
    the in-force leaves in month 611 and the obligation is **exhausted rather than
    truncated**.
    """
    a = kr_immediate_anchor
    assert a.av_pp(324) == pytest.approx(AV_PP_324, abs=WON)
    assert a.av_pp(330) == pytest.approx(AV_PP_330, abs=WON)
    assert a.av_pp(324) > 0.0 > a.av_pp(330)
    assert a.av_pp(325) == pytest.approx(
        a.av_pp(324) * (1.0 + a.crediting_rate_mth(324)) - a.annuity_pp(324), rel=1e-14)
    assert a.av_pp(611) == pytest.approx(AV_PP_611, abs=WON)
    assert a.cv_pp(330) == 0.0                      # nothing can be paid out of it
    assert a.mort_rate(600) == 1.0
    assert a.mort_rate_mth(611) == pytest.approx(1.0, rel=1e-13)
    assert a.lives_if(612) == 0.0
    assert a.payment_factor(611) == pytest.approx(PAYMENT_FACTOR_611, abs=5e-13)
    assert a.annuity_payments(611) == pytest.approx(ANN_611, abs=WON)
    assert a.net_cf(611) == 0.0
    assert a.check_av_roll_fwd() is True            # the closed form holds past the crossing
    assert a.check_av_terminal() is True            # True on this shape by design


# ---------------------------------------------------------------------------
# The worked example — totals and the shape of the result


def test_worked_example_undiscounted_totals(kr_immediate_anchor):
    """The notes' undiscounted totals over t = 0 … 611, column by column.

    ₩137.2m of annuity outgo against ₩100m of premium, ₩2.6m of expense and
    **−₩41,809,002.38** of net cash flow.  Undiscounted the contract loses money and must:
    the insurer receives the premium at time 0 and pays out over half a century, and the
    sign becomes meaningful only when the stream is discounted, which this library does not
    do.  Every total is a little below the annual-step model's — ₩137.2m of annuity against
    ₩138.2m — because the same fund buys a smaller instalment once the annuity is valued as
    the monthly stream the contract actually pays.
    """
    df = kr_immediate_anchor.result_cf()
    for column, total in TOTALS.items():
        tol = 5e-6 if column == "pols_if" else WON
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert df["liability_cf"].sum() == pytest.approx(-df["net_cf"].sum(), rel=1e-15)
    assert df["annuity_payments"].sum() / df["premiums"].sum() == pytest.approx(
        1.3721, abs=5e-5)


def test_worked_example_the_obligation_years_decompose(kr_immediate_anchor):
    """Σ IF(t) = 341.116217 months = Σ l(t) + (120 − Σ l(t) inside the guarantee).

    The expected number of **months** the payment obligation stays open, and it decomposes
    exactly: 338.649237 of survival plus 2.466980 of guarantee.  **The ten-year guarantee
    extends the obligation by 2.5 months in expectation** on a 60-year-old male — a cheap
    option, which the market buys almost universally, and the arithmetic behind the 0.89% of
    income it costs.  The annual grid put the same quantity at 2.2 months, and the monthly
    figure is the larger one because a monthly annuity already pays part-year instalments
    to a life that dies inside a policy year.
    """
    a = kr_immediate_anchor
    ts = range(0, a.proj_len())
    obligation = sum(a.pols_if(t) for t in ts)
    survival = sum(a.lives_if(t) for t in ts)
    inside = sum(a.lives_if(t) for t in range(0, a.annuity_term_mths()))
    assert obligation == pytest.approx(TOTALS["pols_if"], abs=5e-6)
    assert survival == pytest.approx(SUM_LIVES, abs=5e-6)
    assert inside == pytest.approx(SUM_LIVES_GUARANTEE, abs=5e-6)
    added = a.annuity_term_mths() * a.pols_if_init() - inside
    assert added == pytest.approx(GUARANTEE_MONTHS_ADDED, abs=5e-6)
    assert obligation == pytest.approx(survival + added, abs=5e-8)
    assert added == pytest.approx(2.5, abs=0.05)             # 2.5 months, read directly


def test_worked_example_the_expense_total_and_the_break_even(kr_immediate_anchor):
    """₩2,597,690.50 = ₩1,500,000 + ₩1,097,690.50, and break-even at the 264th instalment.

    The second expense term is exactly 0.0080 × the annuity total, because the
    연금수령기간 중 비용 is measured on the annuity and carried at the payment's own weight
    rather than per policy in force — on the monthly grid that is 0.80% of each 연금월액,
    which over twelve months is the 0.80% of the 연금연액 the cost table discloses — and
    **no other expense exists in this projection**: there is no maintenance expense and no
    inflation, the only recurring charge any retrieved 즉시연금 document publishes being this
    one.  The expected cumulative payments cross the premium inside month 263, which is the
    **264th** instalment, at attained age 81 — a date the annual grid could only place to the
    nearest year.  On the nominal annuity, ignoring the survival weight, the gross factor of
    20.6593 years puts the crossing at the 248th instalment — the number a Korean buyer's own
    arithmetic produces, and the reason the shape is understood as a longevity hedge.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    total = df["expenses"].sum()
    assert total == pytest.approx(TOTALS["expenses"], abs=WON)
    assert total - ACQ_EXPENSE_0 == pytest.approx(ANNUITY_CHARGE_TOTAL, abs=WON)
    assert total - ACQ_EXPENSE_0 == pytest.approx(
        0.0080 * df["annuity_payments"].sum(), rel=1e-12)
    assert total / df["annuity_payments"].sum() == pytest.approx(0.019, abs=5e-4)
    for absent in ("expense_maint", "inflation_factor", "inflation_rate"):
        assert absent not in set(a.cells), f"{absent}: no maintenance expense here"
    cum_before = sum(a.annuity_payments(t) for t in range(0, BREAK_EVEN_MONTH))
    cum_after = sum(a.annuity_payments(t) for t in range(0, BREAK_EVEN_MONTH + 1))
    assert cum_before == pytest.approx(CUM_ANNUITY_262, abs=WON)
    assert cum_after == pytest.approx(CUM_ANNUITY_263, abs=WON)
    assert cum_before < a.prem_pp() < cum_after
    # Row 263 pays at the end of month 263: the crossing instalment is the 264th, at 81.
    assert a.age(BREAK_EVEN_MONTH) == 81
    # The buyer's own nominal arithmetic puts it 16 instalments earlier.
    nominal = a.prem_pp() / a.annuity_pp(0)
    assert 247.0 < nominal < 248.0
    assert BREAK_EVEN_MONTH + 1 - nominal == pytest.approx(16.0, abs=1.0)


def test_worked_example_reading_the_shape_of_the_result(kr_immediate_anchor):
    """Three regions: one positive row, nine identical rows, then a decaying tail.

    Row 0 is almost the whole of the insurer's cash and there is never another positive row;
    rows 1 to 119 are a flat annuity-certain, identical to the last digit, because the
    guarantee makes survival irrelevant and the level rate makes the annuity level; rows 120
    onward are the same 연금월액 weighted by a survival probability falling from 0.9529 to
    zero.  The liability is front-loaded in *certainty* and back-loaded in *duration*,
    which is the risk profile that makes longevity and not interest the dominant model risk.
    """
    a = kr_immediate_anchor
    assert a.net_cf(0) > 0.0
    assert all(a.net_cf(t) < 0.0 for t in range(1, a.proj_len() - 1))
    assert a.net_cf(611) == 0.0
    assert len({round(a.net_cf(t), 6) for t in range(1, 120)}) == 1
    tail = [a.payment_factor(t) for t in range(120, a.proj_len())]
    assert tail == sorted(tail, reverse=True) and tail[-1] == 0.0
    assert tail[0] == pytest.approx(PAYMENT_FACTOR_120, abs=PROB)
    guaranteed = sum(a.annuity_payments(t) for t in range(0, 120))
    assert guaranteed / TOTALS["annuity_payments"] == pytest.approx(0.353, abs=5e-4)


# ---------------------------------------------------------------------------
# The dispute panel — 즉시연금 과소지급 분쟁, model points 6 and 7


def test_the_dispute_panel_period_zero_trace_as_designed(immediate_annuity):
    """The notes' month-0 trace on point 6, line by line, at full precision.

    R(0) = (M − V(0)) / s(120, j) = ₩36,551.06; A(0) = V(0) j − R(0) = ₩159,195.1833;
    the annuity is weighted by survival to the payment date; the 사망보험금 is
    q^m × (0.10 P + V(1)); the surrender is taken after the deaths, so its weight carries
    a (1 − q^m); and net_cf(0) = +₩96,148,752.97.
    """
    p = immediate_annuity.Projection[6]
    j = p.crediting_rate_mth(0)
    assert p.retention_pp(0) == pytest.approx(DESIGNED["retention_pp"], abs=SUB_WON)
    assert p.retention_pp(0) == pytest.approx(
        (p.maturity_benefit() - p.av_pp(0)) / p.accum_factor(120, j), rel=1e-14)
    assert p.annuity_pp(0) == pytest.approx(DESIGNED["annuity_pp"], abs=SUB_WON)
    assert p.annuity_pp(0) == pytest.approx(
        p.av_pp(0) * j - p.retention_pp(0), rel=1e-14)
    assert p.payment_factor(0) == pytest.approx(DESIGNED["payment_factor"], abs=EXACT)
    assert p.annuity_payments(0) == pytest.approx(
        DESIGNED["annuity_payments"], abs=SUB_WON)
    assert p.av_pp(1) == pytest.approx(DESIGNED["av_pp_1"], abs=SUB_WON)
    assert p.pols_death(0) == pytest.approx(DESIGNED["pols_death"], abs=EXACT)
    assert p.claims(0, "DEATH") == pytest.approx(DESIGNED["claims_death"], abs=SUB_WON)
    assert p.claims(0, "DEATH") == pytest.approx(
        p.pols_death(0) * (0.10 * p.prem_pp() + p.av_pp(1)), rel=1e-14)
    assert p.pols_lapse(0) == pytest.approx(DESIGNED["pols_lapse"], abs=EXACT)
    assert p.claims(0, "LAPSE") == pytest.approx(DESIGNED["claims_lapse"], abs=SUB_WON)
    assert p.commissions(0) == pytest.approx(2000000.0, abs=SUB_WON)
    assert p.expenses(0) == pytest.approx(DESIGNED["expenses"], abs=SUB_WON)
    assert p.net_cf(0) == pytest.approx(DESIGNED["net_cf"], abs=SUB_WON)


def test_the_dispute_panel_period_zero_trace_as_ordered(immediate_annuity):
    """The notes' period-0 trace on point 7: one term goes to zero and everything moves.

    R(0) = 0, so A(0) is the whole month's interest ₩195,746.24, V(1) = V(0) — **the fund
    stands still** — and the death benefit, the surrender value and the expense all follow it
    down or up.  net_cf(0) = +₩96,111,992.59, ₩36,760.37 below the designed basis in the
    first row alone.
    """
    p = immediate_annuity.Projection[7]
    assert p.retention_pp(0) == 0.0
    assert all(p.retention_pp(t) == 0.0 for t in range(0, p.proj_len()))
    assert p.annuity_pp(0) == pytest.approx(ORDERED["annuity_pp"], abs=SUB_WON)
    assert p.annuity_pp(0) == pytest.approx(
        p.av_pp(0) * p.crediting_rate_mth(0), rel=1e-15)
    assert p.av_pp(1) == pytest.approx(ORDERED["av_pp_1"], abs=SUB_WON)
    assert p.av_pp(1) == pytest.approx(p.av_pp(0), abs=1e-6)
    assert p.annuity_payments(0) == pytest.approx(
        ORDERED["annuity_payments"], abs=SUB_WON)
    assert p.claims(0, "DEATH") == pytest.approx(ORDERED["claims_death"], abs=SUB_WON)
    assert p.claims(0, "LAPSE") == pytest.approx(ORDERED["claims_lapse"], abs=SUB_WON)
    assert p.expenses(0) == pytest.approx(ORDERED["expenses"], abs=SUB_WON)
    assert p.net_cf(0) == pytest.approx(ORDERED["net_cf"], abs=SUB_WON)


@pytest.mark.parametrize("point_id", sorted(DISPUTE_TOTALS))
def test_the_dispute_panel_totals(immediate_annuity, point_id):
    """The notes' side-by-side table of undiscounted totals, column by column.

    ``claims_maturity`` is ₩79,495,349.97 on **both**, the maturity benefit being
    contractually the gross premium either way: the dispute was never about whether the
    ₩100m came back, but about whether the policyholder had been told that part of his
    interest was being taken to fund it.
    """
    p = immediate_annuity.Projection[point_id]
    df = p.result_cf()
    for column, total in DISPUTE_TOTALS[point_id].items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert p.check_net_cf() is True


def test_the_dispute_costs_the_insurer_the_whole_first_day_deduction(immediate_annuity):
    """One contract, one differing column, +22.96% of income and ₩3.48m of outgo.

    Points 6 and 7 differ in ``retention_basis`` and in nothing else, which is what makes the
    difference between their statements the quantity that was litigated from 2017 to 2025
    rather than a comparison of two products.  Both open at V(0) = P(1 − 0.0350 − 0.0147) and
    both carry a 만기보험금 of the **gross** premium — the fund opens below the benefit it
    must reach, which is the whole mechanic of the retention.  With R = 0 the fund never
    grows, so that benefit has to be found from somewhere the contract does not fund;
    ``retention_shortfall_pp()`` is what that costs at inception, (M − V(0)) v(10), and it
    appears on the right-hand side of ``check_annuity_basis()`` rather than being tolerated
    away, because under ``as_ordered`` the pricing identity does **not** close on V(0) and
    should not.
    """
    designed, ordered = immediate_annuity.Projection[6], immediate_annuity.Projection[7]
    table = immediate_annuity.Data.model_point_table()
    assert [c for c in table.columns
            if str(table.loc[6, c]) != str(table.loc[7, c]) and c != "policy_id"] == [
        "retention_basis"]
    assert designed.retention_basis() == "as_designed"
    assert ordered.retention_basis() == "as_ordered"
    for p in (designed, ordered):
        assert p.shape() == "inheritance"
        assert p.annuity_term() == 10 and p.proj_len() == 120
        assert p.av_pp_init() == pytest.approx(AV_PP_INIT_LOADED, abs=SUB_WON)
        assert p.av_pp_init() == pytest.approx(
            p.prem_pp() * (1.0 - 0.0350 - 0.0147), rel=1e-15)
        assert p.maturity_benefit() == MATURITY_BENEFIT == p.prem_pp() > p.av_pp_init()
        assert p.accum_factor(120, p.crediting_rate_mth(0)) == pytest.approx(
            S_120_MTH, abs=FACTOR)
    assert ordered.annuity_pp(0) / designed.annuity_pp(0) - 1.0 == pytest.approx(
        ANNUITY_UPLIFT_AS_ORDERED, abs=5e-5)
    difference = (ordered.result_cf()["net_cf"].sum()
                  - designed.result_cf()["net_cf"].sum())
    assert difference == pytest.approx(DISPUTE_NET_CF_DIFFERENCE, abs=WON)
    assert designed.retention_shortfall_pp() == 0.0
    assert ordered.retention_shortfall_pp() == pytest.approx(
        RETENTION_SHORTFALL, abs=SUB_WON)
    assert ordered.disc_factor(120) == pytest.approx(DISC_120, abs=5e-13)
    assert ordered.retention_shortfall_pp() == pytest.approx(
        (ordered.maturity_benefit() - ordered.av_pp_init()) * ordered.disc_factor(120),
        rel=1e-14)
    # Both close their own pricing identity, the second only with the shortfall in it.
    assert designed.check_annuity_basis() is True
    assert ordered.check_annuity_basis() is True


def test_the_retention_rises_every_year_even_on_a_level_rate(immediate_annuity):
    """R(t) runs 36,551.06 → 45,647.26 over the ten 계약해당일 while A(t) stays exactly level.

    The remaining term shortens faster than the shortfall M − V(t) closes, so the retention
    rises; the interest V(t) j rises by precisely the same amount, which is the algebraic
    content of V(t) = V(0) + R s(t, j).  On the monthly grid it rises **every month** and not
    only every anniversary, which is the one thing the annual grid could not show.  **On a
    falling rate the two move the same way instead of opposite ways**, and that is model
    point 8.
    """
    p = immediate_annuity.Projection[6]
    path = [p.retention_pp(12 * y) for y in range(0, 10)]
    for got, printed in zip(path, RETENTION_PATH):
        assert got == pytest.approx(printed, abs=WON)
    assert path == sorted(path)
    months = [p.retention_pp(t) for t in range(0, 12)]
    for got, printed in zip(months, RETENTION_PATH_MONTHS):
        assert got == pytest.approx(printed, abs=WON)
    assert months == sorted(months)
    assert all(p.annuity_pp(t) == pytest.approx(DESIGNED["annuity_pp"], abs=SUB_WON)
               for t in range(0, 120))
    j = p.crediting_rate_mth(0)
    for t in range(1, 120):
        assert (p.av_pp(t) * j - p.av_pp(t - 1) * j) == pytest.approx(
            p.retention_pp(t) - p.retention_pp(t - 1), abs=1e-6)
    # The fund lands on the maturity benefit exactly, which is what R was sized to do.
    assert p.av_pp(120) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    assert p.check_av_terminal() is True


def test_the_external_check_on_the_inheritance_annuity(immediate_annuity):
    """₩159,195.18 a month against ``product-spec.md``'s independent ₩161,000.

    The strongest external check the inheritance shape has: the spec reconstructs the
    ten-year 만기형 monthly annuity from published figures without touching the model.  The
    model now pays a monthly instalment directly rather than a twelfth of an annual one, so
    the comparison is made on the figure the projection actually pays, and the two
    constructions agree to within 1.1% — the residual being the within-month interest and the
    retention's own monthly re-striking, neither of which the spec's annual reconstruction
    carries.
    """
    designed, ordered = immediate_annuity.Projection[6], immediate_annuity.Projection[7]
    assert designed.annuity_pp_annual(0) == pytest.approx(DESIGNED_ANNUAL, abs=WON)
    assert ordered.annuity_pp_annual(0) == pytest.approx(ORDERED_ANNUAL, abs=WON)
    assert designed.annuity_pp(0) == pytest.approx(161000.0, rel=0.012)
    assert ordered.annuity_pp(0) / designed.annuity_pp(0) - 1.0 == pytest.approx(
        ANNUITY_UPLIFT_AS_ORDERED, abs=5e-5)


# ---------------------------------------------------------------------------
# The floor-stepping panel — model point 8


@pytest.mark.parametrize("t", sorted(FLOOR_STEP))
def test_the_floor_stepping_panel_row(immediate_annuity, t):
    """Every row of the notes' point-8 table: the rate, the annuity, R(t) and the fund.

    여자 70, ₩100,000,000, 상속연금형 만기형 20년 on the ``min_guar`` basis, where the
    declared rate is zero so that Max[공시이율, 최저보증이율] resolves to the floor at every
    duration: 1.25% for t = 0 … 59, 1.00% for t = 60 … 119 and 0.75% from t = 120.  The band
    table is published in policy years and the grid reads it at ``t // 12``, so the floor
    steps on the 계약해당일 and is level across the twelve months between.
    """
    rate, annuity, retention, av = FLOOR_STEP[t]
    p = immediate_annuity.Projection[8]
    assert p.crediting_rate(t) == rate
    assert p.crediting_rate(t) == p.min_guar_rate(t)      # the floor binds, not the rate
    assert p.annuity_pp(t) == pytest.approx(annuity, abs=SUB_WON)
    assert p.retention_pp(t) == pytest.approx(retention, abs=SUB_WON)
    assert p.av_pp(t) == pytest.approx(av, abs=WON)


def test_the_floor_stepping_hand_trace_across_the_first_step(immediate_annuity):
    """The notes' t = 59 → t = 60 trace: s(181, j₁) and s(180, j₂), and the fund between.

    **The rate falls by one fifth and the annuity falls by one quarter.** 1.25% → 1.00% is
    −20.0%; ₩80,175.25 → ₩59,974.78 is −25.20%.  The extra 5.2 points are the retention
    *rising*, from ₩19,401.21 to ₩19,792.98, at the same moment as the interest it is
    deducted from falls.  The step lands on the fifth 계약해당일, which on this grid is month
    60, and it is a single step rather than a gradual move: the band table is published in
    policy years.
    """
    p = immediate_annuity.Projection[8]
    j1, j2 = p.crediting_rate_mth(59), p.crediting_rate_mth(60)
    assert p.accum_factor(240, p.crediting_rate_mth(0)) == pytest.approx(
        S_240_AT_125, abs=FACTOR)
    assert p.accum_factor(180, j2) == pytest.approx(S_180_AT_100, abs=FACTOR)
    assert p.av_pp(59) == pytest.approx(AV_PP_59_POINT_8, abs=SUB_WON)
    assert p.retention_pp(59) == pytest.approx(
        (p.maturity_benefit() - p.av_pp(59)) / p.accum_factor(181, j1), rel=1e-13)
    assert p.annuity_pp(59) == pytest.approx(
        p.av_pp(59) * j1 - p.retention_pp(59), rel=1e-13)
    assert p.av_pp(60) == pytest.approx(AV_PP_60_POINT_8, abs=SUB_WON)
    assert p.av_pp(60) == pytest.approx(
        p.av_pp(59) * (1.0 + j1) - p.annuity_pp(59), rel=1e-14)
    assert p.retention_pp(60) == pytest.approx(
        (p.maturity_benefit() - p.av_pp(60)) / p.accum_factor(180, j2), rel=1e-13)
    assert p.annuity_pp(60) / p.annuity_pp(59) - 1.0 == pytest.approx(
        FIRST_STEP_FALL, abs=5e-5)
    assert p.retention_pp(60) > p.retention_pp(59)
    assert p.crediting_rate(60) / p.crediting_rate(59) - 1.0 == pytest.approx(-0.20)
    # The annuity is level inside the band and steps only at the 계약해당일.
    assert all(p.annuity_pp(t) == pytest.approx(p.annuity_pp(0), abs=SUB_WON)
               for t in range(0, 60))


# ---------------------------------------------------------------------------
# The load cross-check — model point 9, the shape with no mortality in its annuity


def test_the_certain_shape_load_cross_check(immediate_annuity):
    """A(0) = V(0)/a(120, j) = ₩894,628.93 a month, against 교보's published 90만원.

    **This shape is where the monthly grid and the annual one agree exactly**, and that is
    the point of asserting it here: the 확정기간연금형 carries no mortality in its annuity at
    all, so the annual-step model's 연금연액 converted to a monthly instalment of equal value
    — ``A / 12 x i^(12) / i`` — is precisely what the monthly grid solves for directly, to
    the won.  Everywhere else in this module the two grids differ by the mortality a monthly
    annuity picks up; here there is none to pick up.

    Against 교보's published 90만원 on a 2.52% basis the model's ₩894,628.93 is **−0.60%** at
    this model's 2.50%; ``product-spec.md``'s own cross-check table puts the same cell at
    −0.5% because it solves the identity on 교보's 2.52%, and the 0.10-point gap between the
    two is those 0.02 points of declared rate.  **The annuitant's age and sex are irrelevant
    to a 확정기간연금형**, so a 남자 55 published figure is directly comparable with the
    model's 남자 60 one, and because this shape carries no mortality in its annuity it is the
    sharpest available test of the expense load.  The notes' undiscounted totals are asserted
    beside it: the fund runs off to zero on its own, which is what ``check_av_terminal()``
    asserts, and ``claims_lapse`` is nil through the final policy year because the surrender
    rate is suppressed there on every shape.
    """
    p = immediate_annuity.Projection[9]
    j = p.crediting_rate_mth(0)
    assert p.shape() == "certain"
    assert p.av_pp_init() == pytest.approx(AV_PP_INIT_LOADED, abs=SUB_WON)
    assert p.annuity_factor_certain(120, j) == pytest.approx(A_120_MTH, abs=FACTOR)
    assert p.annuity_pp(0) == pytest.approx(CERTAIN_ANNUITY, abs=SUB_WON)
    assert p.annuity_pp(0) == pytest.approx(
        p.av_pp_init() / p.annuity_factor_certain(120, j), rel=1e-15)
    assert p.annuity_pp_annual(0) == pytest.approx(CERTAIN_ANNUITY_ANNUAL, abs=WON)
    # The interest-only conversion of the annual-step model's own annuity, to the won.
    annual_step = p.av_pp_init() / p.annuity_factor_certain(10, 0.025)
    assert _true_monthly(annual_step) == pytest.approx(p.annuity_pp(0), abs=WON)
    assert round(p.annuity_pp(0) / 10000.0, 1) == 89.5
    # -0.60% at this model's 2.50%, against the spec's -0.5% solved on 교보's 2.52%.
    assert p.annuity_pp(0) / CERTAIN_PUBLISHED - 1.0 == pytest.approx(-0.0060, abs=5e-5)
    assert p.decl_rate() == DECL_RATE < 0.0252
    # No mortality in the annuity: the factor is pure interest on this shape.
    assert all(p.pricing_factor(t) == 1.0 for t in range(0, p.proj_len()))
    with pytest.raises(FormulaError):
        p.annuity_factor()
    # The notes' point-9 totals, and the fund that runs off to zero on its own.
    df = p.result_cf()
    for column, total in CERTAIN_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert p.av_pp(120) == pytest.approx(0.0, abs=1e-6)
    assert abs(p.av_pp(120)) < 1e-7 * p.prem_pp()
    assert p.check_av_terminal() is True
    assert all(p.claims(t, "LAPSE") == 0.0 for t in range(108, 120))
    assert p.annuity_payments(119) == pytest.approx(CERTAIN_LAST_INSTALMENT, abs=WON)
    assert p.annuity_payments(119) / df["annuity_payments"].sum() == pytest.approx(
        0.0077, abs=5e-5)
    assert df["claims_maturity"].sum() == 0.0     # the instalments exhaust the fund


# ---------------------------------------------------------------------------
# Which check_* cells this model publishes


def test_which_checks_this_model_publishes(immediate_annuity, kr_immediate_anchor):
    """The eleven check cells, asserted **by name**, with the six that carry a residual.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared: it
    would call the ten that remain, pass, and prove less than it did before.  Naming the set
    here is what turns "every check passes" into a statement about *which* checks.  That
    every one of them is True on **every** shipped model point is
    ``test_model_conventions_kr.py``'s single sweep and is not repeated here.

    ``check_annuity_basis_resid`` is the one residual taking no argument, because the
    pricing identity is a single statement about the contract at inception rather than a
    per-period one.  ``check_av_terminal``, ``check_premium_split``, ``check_rate_level``,
    ``check_guarantee_certain`` and ``check_surr_value`` carry no residual at all: each is a
    statement about *where* a quantity stands rather than about how far an identity misses.
    """
    cells = set(immediate_annuity.Projection.cells)
    published = {n for n in cells
                 if n.startswith("check_") and not n.endswith("_resid")}
    assert published == CHECKS
    resid = {n[:-len("_resid")] for n in cells
             if n.startswith("check_") and n.endswith("_resid")}
    assert resid == CHECKS_WITH_RESID
    a = kr_immediate_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True, f"{name}() is not True on the anchor cell"
        assert isinstance(value, bool), f"{name}() must return a real bool"
    assert a.check_annuity_basis_resid() == pytest.approx(0.0, abs=1e-4)
    money = {"check_av_roll_fwd", "check_net_cf"}
    for name in sorted(CHECKS_WITH_RESID - {"check_annuity_basis"}):
        residual = getattr(a, name + "_resid")
        tol = 1e-12 * a.prem_pp() if name in money else 1e-10
        for t in range(0, a.proj_len()):
            assert residual(t) == pytest.approx(0.0, abs=tol), f"{name}_resid({t})"


def test_the_check_tolerances_are_named_references(immediate_annuity,
                                                   kr_immediate_anchor):
    """``roll_fwd_tol`` for the probability identities, ``val_tol`` scaled by the premium.

    The two are different quantities and must not collapse into one.  ``roll_fwd_tol``
    closes dimensionless identities between probabilities near 1.0.  ``val_tol`` is
    *relative* and is multiplied by ``prem_pp()`` at every use, because this product's
    monetary quantities run from ₩10,000,000 to ₩5,000,000,000 across the shipped table and
    a fixed absolute tolerance would be slack at one end and impossible at the other.  Both
    are far below one won at every shipped premium.
    """
    refs = immediate_annuity.Projection.refs
    assert "roll_fwd_tol" in refs and "val_tol" in refs
    assert refs["roll_fwd_tol"] == 1e-10 and refs["val_tol"] == 1e-12
    assert refs["omega_age"] == OMEGA_AGE
    table = immediate_annuity.Data.model_point_table()
    assert refs["val_tol"] * table["prem_pp"].max() < 1.0
    # The tolerance is not slack the checks hide behind.
    a = kr_immediate_anchor
    worst = max(abs(a.check_net_cf_resid(t)) for t in range(0, a.proj_len()))
    assert worst < refs["val_tol"] * a.prem_pp() / 100.0


# ---------------------------------------------------------------------------
# The product's own invariants, recursions and processing order


def test_the_obligation_rolls_forward_on_its_own_decrements(immediate_annuity,
                                                            kr_immediate_anchor):
    """IF(t) − exits(t) − IF(t + 1) = 0, with ``pols_exit`` built independently of IF.

    On the life shape the identity has real content: nothing exits inside the 보증지급기간,
    the whole cohort that died in it exits at t = g − 1, and the deaths of each later period
    exit as they fall.  Asserted here on the anchor and on one point of each other shape,
    where the exits are the decrements themselves.
    """
    a = kr_immediate_anchor
    assert a.check_pols_roll_fwd() is True
    for t in range(0, a.proj_len()):
        assert a.pols_if(t) - a.pols_exit(t) - a.pols_if(t + 1) == pytest.approx(
            0.0, abs=1e-12)
    assert sum(a.pols_exit(t) for t in range(0, a.proj_len())) == pytest.approx(
        1.0, abs=1e-9)
    for point_id, expected in ((6, "inheritance"), (9, "certain")):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == expected
        assert p.check_pols_roll_fwd() is True
        for t in range(0, p.proj_len()):
            built = (p.pols_lapse(t) if p.shape() == "certain"
                     else p.pols_death(t) + p.pols_lapse(t))
            assert p.pols_exit(t) == pytest.approx(built, rel=1e-14), (point_id, t)


def test_the_fund_recursion_closes_against_a_closed_form_on_every_shape(
        immediate_annuity, kr_immediate_anchor):
    """V(t + 1) = V(t)(1 + j(t)) − A(t), against four genuinely different derivations.

    ``check_av_roll_fwd`` rebuilds the fund per shape — the retrospective closed form on the
    life shape, the annuity-certain's own run-off on the certain shape, the algebraic
    reduction ``V + (M − V)/s`` under ``as_designed`` and a standing fund under
    ``as_ordered`` — so it is a second derivation and not the recursion written twice.
    """
    a = kr_immediate_anchor
    assert a.check_av_roll_fwd() is True
    for t in range(0, a.proj_len()):
        assert a.av_pp(t + 1) == pytest.approx(
            a.av_pp(t) * (1.0 + a.crediting_rate_mth(t)) - a.annuity_pp(t), rel=1e-12)
    j0 = a.crediting_rate_mth(0)
    for t in (1, 120, 330, 611):
        assert a.av_pp(t) == pytest.approx(
            a.av_pp_init() * (1.0 + j0) ** t
            - a.annuity_pp(0) * a.accum_factor(t, j0), abs=1e-3)
    for point_id in (6, 7, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_av_roll_fwd() is True, point_id
        assert p.check_av_terminal() is True, point_id


def test_the_pricing_identity_ties_the_projection_to_the_fund(immediate_annuity,
                                                              kr_immediate_anchor):
    """V(0) is the present value of everything it was struck to buy, on all three shapes.

    ``check_annuity_basis`` discounts the projected annuity on the crediting-rate path — so a
    stepping floor is handled without assuming a level rate — and adds the discounted
    만기보험금 where there is one.  It is what holds the **life** shape to its basis, that
    shape having no contractual terminal fund value for ``check_av_terminal`` to test.
    """
    a = kr_immediate_anchor
    assert a.check_annuity_basis() is True
    built = sum(a.annuity_pp(t) * a.pricing_factor(t) * a.disc_factor(t + 1)
                for t in range(0, a.proj_len()))
    assert built == pytest.approx(a.av_pp_init(), abs=1e-6)
    for point_id in (6, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_annuity_basis() is True, point_id
        assert p.check_annuity_basis_resid() == pytest.approx(
            0.0, abs=1e-12 * p.prem_pp()), point_id


def test_the_premium_split_closes_and_there_is_no_acquisition_strain(immediate_annuity):
    """A = B + C + D, on every shape, with nothing left over in either direction.

    The 약관's own division of the single premium into the 보장계약 보험료, the 사업비 and the
    연금계약 순보험료 that becomes the opening fund.  It is the statement that this product
    has **no acquisition strain**: the charge taken from the fund at inception is exactly the
    outgo at inception, so ``net_cf(0)`` is positive on every shipped model point — the only
    model in ``krlib`` of which that is true.
    """
    for point_id in (1, 6, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_premium_split() is True, point_id
        built = (p.prem_pp() * p.comm_rate()
                 + p.prem_pp() * p.acq_expense_rate()
                 + p.risk_prem_pp()
                 + p.av_pp_init())
        assert built == pytest.approx(p.prem_pp(), abs=1e-6), point_id
        assert p.comm_rate() < p.acq_charge_rate()      # the charge covers the commission
        assert p.net_cf(0) > 0.0
        assert all(p.net_cf(t) < 0.0 for t in range(1, p.proj_len() - 1))


def test_the_notes_processing_order_is_the_order_the_model_runs(immediate_annuity):
    """Steps 2 to 6 of the notes' processing order, each by a quantity that would differ.

    The order is not presentational: four of the flows depend on it, so each is asserted by a
    number an out-of-order model would produce differently.

    **Credit, then strike the annuity** — on the certain shape A(t) = V(t)/a(m, j) and not
    V(t)(1 + j)/a(m, j), the two differing by the whole month's interest; the order is what
    exhausts the fund to zero at the end of the term rather than to a residue.
    **Deaths at the end of the period** — the 사망보험금 is measured on the fund carried
    forward, so on point 6 at t = 0 it is q^m × (0.10 P + V(1)) = ₩30,957.20 against
    ₩30,946.43 on the fund at the start, and the two differ in every period.
    **Surrenders after the deaths** — the inheritance branch carries a (1 − q^m) the certain
    branch does not, so the weight is 0.0016816469 rather than the bare w^m; on the certain
    shape the contract survives the annuitant and the decrement bites on persistency alone.
    **The 만기보험금 last, at IF(N)** — one further period of decrement away from the row
    that carries it, and nil at every earlier t and on both other shapes.
    """
    inheritance = immediate_annuity.Projection[6]
    certain = immediate_annuity.Projection[9]

    for t in range(0, certain.proj_len()):
        j = certain.crediting_rate_mth(t)
        m = certain.annuity_term_mths() - t
        assert certain.annuity_pp(t) == pytest.approx(
            certain.av_pp(t) / certain.annuity_factor_certain(m, j), rel=1e-14)
        credited = certain.av_pp(t) * (1.0 + j) / certain.annuity_factor_certain(m, j)
        assert credited / certain.annuity_pp(t) == pytest.approx(1.0 + j, rel=1e-12)
    assert certain.av_pp(certain.proj_len()) == pytest.approx(0.0, abs=1e-6)

    for t in range(0, inheritance.proj_len()):
        rho_p = inheritance.db_rate() * inheritance.prem_pp()
        assert inheritance.claims(t, "DEATH") == pytest.approx(
            inheritance.pols_death(t) * (rho_p + inheritance.av_pp(t + 1)), rel=1e-14)
        assert inheritance.claims(t, "DEATH") != pytest.approx(
            inheritance.pols_death(t) * (rho_p + inheritance.av_pp(t)), rel=1e-9)
        assert inheritance.pols_lapse(t) == pytest.approx(
            inheritance.lives_if(t) * (1.0 - inheritance.mort_rate_mth(t))
            * inheritance.surr_if(t) * inheritance.lapse_rate_mth(t), rel=1e-14)
        assert certain.pols_lapse(t) == pytest.approx(
            certain.surr_if(t) * certain.lapse_rate_mth(t), rel=1e-14)
    assert inheritance.claims(0, "DEATH") == pytest.approx(
        DESIGNED["claims_death"], abs=SUB_WON)
    assert inheritance.pols_death(0) * (0.10 * inheritance.prem_pp()
                                        + inheritance.av_pp(0)) == pytest.approx(
        30946.43, abs=WON)
    assert inheritance.pols_lapse(0) == pytest.approx(0.0016816469201, abs=EXACT)
    assert certain.pols_lapse(0) == pytest.approx(
        certain.lapse_rate_mth(0), rel=1e-14)

    n = inheritance.proj_len() - 1             # the last projected period
    assert inheritance.claims(n, "MATURITY") == pytest.approx(
        inheritance.pols_if(n + 1) * inheritance.maturity_benefit(), rel=1e-14)
    assert all(inheritance.claims(t, "MATURITY") == 0.0 for t in range(0, n))
    assert inheritance.pols_if(n + 1) < inheritance.pols_if(n)
    for point_id in (1, 9):
        q = immediate_annuity.Projection[point_id]
        assert q.maturity_benefit() == 0.0
        assert all(q.claims(t, "MATURITY") == 0.0 for t in range(0, q.proj_len()))


def test_the_published_statement_adds_up(immediate_annuity, kr_immediate_anchor):
    """``net_cf`` equals the published columns of the same row, rebuilt from the frame.

    ``check_net_cf`` re-reads ``result_cf()``'s own columns rather than the formulas, so a
    component missing from the statement fails there rather than being reconciled only in
    prose.  Asserted on the anchor and on one point of each other shape, the three shapes
    having three different sets of non-zero columns.
    """
    for point_id in (1, 6, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_net_cf() is True, point_id
        df = p.result_cf()
        outgo = df[["annuity_payments", "claims_death", "claims_lapse",
                    "claims_maturity", "commissions", "expenses"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-6)
    a = kr_immediate_anchor
    assert "claims" not in a.result_cf().columns


def test_the_two_result_frames_and_the_sign_they_publish(immediate_annuity,
                                                         kr_immediate_anchor):
    """Both frames' columns in order, and both signs of the net flow published as columns.

    ``result_cf()`` puts ``pols_if`` first because the library publishes the in-force measure
    first, and carries the three ``claims_*`` splits with no subtotal beside them;
    ``liability_cf`` is the notes' outgo-positive CF(t) and ``net_cf`` its exact negative, so
    that neither a reader of the notes nor a reader of the library has to negate anything by
    hand.  ``result_pols()`` is the companion frame — everything the statement is built out
    of and nothing that is a cash flow itself, stated at the **start** of the period.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "annuity_payments", "claims_death", "claims_lapse",
        "claims_maturity", "commissions", "expenses", "liability_cf", "net_cf",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(PROJ_LEN))
    assert df.notna().all().all()
    assert df.loc[0, "net_cf"] == pytest.approx(NET_CF_0, abs=WON) and df.loc[
        0, "net_cf"] > 0.0                      # the single premium is income
    assert (df["liability_cf"] + df["net_cf"]).abs().max() == 0.0
    assert "liability_cf" in immediate_annuity.Projection.cells
    pols = a.result_pols()
    assert list(pols.columns) == [
        "pols_if", "lives_if", "surr_if", "pols_death", "pols_lapse", "payment_factor",
        "crediting_rate", "av_pp", "cv_pp", "annuity_pp", "retention_pp",
    ]
    assert pols.index.name == "t" and len(pols) == PROJ_LEN
    assert pols.loc[0, "av_pp"] == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert (pols["retention_pp"] == 0.0).all()  # no maturity benefit on this shape
    assert not any(c.startswith("premium") or c.endswith("_cf") for c in pols.columns)


def test_the_surrender_deduction_is_nil_and_the_statutory_cap_binds_nothing(
        immediate_annuity, kr_immediate_anchor):
    """해약공제액 = 0 at every duration, so 해약환급금 is the 계약자적립액 exactly.

    Not generosity but structure: a single-premium annuity has no unamortised acquisition
    cost to recover, the cost having been taken in full at inception, so 별표 14's
    표준해약공제액 cap binds nothing here.  The zero was **observed** on the published run
    rather than assumed, which is why the cells exists at all instead of the deduction being
    dropped from the formula.
    """
    a = kr_immediate_anchor
    assert all(a.surr_chg_pp(t) == 0.0 for t in range(0, a.proj_len()))
    assert a.check_surr_value() is True
    for point_id in (6, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_surr_value() is True
        for t in range(0, p.proj_len() + 1):
            assert p.surr_chg_pp(t) == 0.0
            assert p.cv_pp(t) == pytest.approx(max(p.av_pp(t), 0.0), abs=1e-6)
        assert p.claims(0, "LAPSE") == pytest.approx(
            p.pols_lapse(0) * p.cv_pp(1), rel=1e-14)


def test_the_crediting_rate_is_a_max_and_the_floor_is_inert_on_the_anchor(
        immediate_annuity, kr_immediate_anchor):
    """i(t) = Max[공시이율, 최저보증이율(t)], the 약관's own rule, both ways round.

    On ``decl_2017`` the declared rate is above every step of the floor, so the rate is level
    and the floor is inert — which is the condition the life shape's once-struck factor
    relies on and ``check_rate_level()`` asserts.  On ``min_guar`` the declared rate is zero
    and the floor binds at every duration.
    """
    a = kr_immediate_anchor
    assert a.check_rate_level() is True
    for t in (0, 59, 60, 119, 120, 600):
        assert a.crediting_rate(t) == max(a.decl_rate(), a.min_guar_rate(t))
        assert a.crediting_rate(t) == a.decl_rate() > a.min_guar_rate(t)
    stepping = immediate_annuity.Projection[8]
    assert stepping.decl_rate() == 0.0
    for t in (0, 59, 60, 119, 120, 239):
        assert stepping.crediting_rate(t) == stepping.min_guar_rate(t)
    # The life shape asserts levelness; the other two carry a stepping rate correctly.
    assert stepping.check_rate_level() is True      # True on a non-life shape by design
    assert stepping.crediting_rate(0) != stepping.crediting_rate(239)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_pols_if_is_not_a_survival_probability(kr_immediate_anchor):
    """Pitfall 1: treating ``pols_if`` as a survival probability.

    It is the probability that a **payment obligation remains**.  On the anchor it is exactly
    1.000000 for 120 months while the annuitant's survival probability has already fallen to
    0.953996 by t = 119, so any per-policy quantity weighted by survival inside the guarantee
    is understated.  The model says so in that cells' own docstring, in the phrase the
    conventions suite reads.
    """
    a = kr_immediate_anchor
    assert all(a.pols_if(t) == 1.0 for t in range(0, 120))
    assert a.lives_if(119) == pytest.approx(0.953995829, abs=PROB)
    assert a.pols_if(119) != a.lives_if(119)
    assert a.pols_if(119) > a.lives_if(119)
    for t in range(0, a.proj_len()):
        assert a.pols_if(t) >= a.lives_if(t)
    doc = a.cells["pols_if"].doc.replace("*", "")
    assert "payment obligation remains" in doc
    assert "not a policy count" in doc
    assert "not a survival probability" in doc


def test_pitfall_the_guarantee_is_a_max_and_not_a_sum(kr_immediate_anchor):
    """Pitfall 2: adding the guarantee to the survival probability instead of taking the max.

    An additive form pays ``1 + l(t + 1)`` for the whole guaranteed term, giving a factor of
    **343.332581** against the correct **239.234686** and an annuity of ₩281,068.58 a month —
    69.68% of the right answer, a 30% under-payment for life.
    """
    a = kr_immediate_anchor
    v = 1.0 / (1.0 + a.crediting_rate_mth(0))
    g = a.annuity_term_mths()
    additive = sum(
        v ** (t + 1) * (a.lives_if(t + 1) + (1.0 if t + 1 <= g else 0.0))
        for t in range(0, a.proj_len()))
    assert additive == pytest.approx(ADDITIVE_FACTOR, abs=5e-6)
    assert a.av_pp_init() / additive == pytest.approx(ADDITIVE_ANNUITY, abs=WON)
    assert (a.av_pp_init() / additive) / a.annuity_pp(0) == pytest.approx(
        ADDITIVE_SHARE, abs=5e-5)
    assert additive > a.annuity_factor()
    # The model takes the max, and the checks that would fail on the sum both pass.
    for t in range(0, a.proj_len()):
        guaranteed = 1.0 if t + 1 <= g else 0.0
        assert a.payment_factor(t) == max(a.lives_if(t + 1), guaranteed)
    assert a.check_guarantee_certain() is True
    assert a.check_payment_factor() is True


def test_pitfall_nothing_exits_inside_the_guarantee(kr_immediate_anchor):
    """Pitfall 3: decrementing the obligation on a death inside the 보증지급기간.

    Nothing exits until the guarantee expires and then the whole cohort that died inside it
    exits at once: ``pols_exit(t) = 0`` for t = 0 … 118 and
    ``pols_exit(119) = 0.046529974860``.  The same pitfall covers confusing the two guarantee
    tests — the obligation is open at time t for t = 0 … 119 while the instalments the
    guarantee covers fall at the ends of months 0 … 119, so ``pols_if(120) = l(120)`` and
    ``payment_factor(120) = l(121)`` are different numbers on the same row, and either error
    shifts the cliff by a month.
    """
    a = kr_immediate_anchor
    assert all(a.pols_exit(t) == 0.0 for t in range(0, 119))
    assert a.pols_exit(118) == 0.0
    assert a.pols_exit(119) == pytest.approx(POLS_EXIT_119, abs=EXACT)
    assert a.pols_exit(119) > 60.0 * a.pols_exit(120)  # a step, not a curve
    assert a.pols_if(120) == pytest.approx(a.lives_if(120), rel=1e-15)
    assert a.payment_factor(120) == pytest.approx(a.lives_if(121), rel=1e-15)
    assert a.pols_if(120) - a.payment_factor(120) == pytest.approx(
        POLS_IF_120 - PAYMENT_FACTOR_120, abs=EXACT)
    assert a.check_pols_roll_fwd() is True
    assert a.check_guarantee_certain() is True


def test_pitfall_proj_len_is_a_row_count_not_a_last_index(immediate_annuity):
    """Pitfall 4: ``proj_len()`` read as the last row index.

    It is the **number of projected months**, the frame's exclusive end, so the frame is
    ``range(proj_len())`` and the last row is ``proj_len() − 1``.  The anchor has 612 rows,
    0 … 611, and 12(ω − x + 1) = 12 x (110 − 60 + 1) = 612.  An off-by-one either drops the
    last instalment on the term shapes — on point 9 that is ₩745,894.87 of outgo, 0.77% of
    the annuity total, a tenth of what the same slip cost on an annual grid — or projects a
    month past the end of the table.  The notes' horizon column is asserted beside it for all
    ten shipped points, N being 12 max(g, ω − x + 1) on the life shape and 12n on the other
    two: a structural property of the shape and not a rounded projection length, so that the
    life shape's obligation is exhausted rather than truncated.
    """
    for point_id, (horizon, years) in SHIPPED_HORIZONS.items():
        p = immediate_annuity.Projection[point_id]
        df = p.result_cf()
        assert len(df) == p.proj_len(), point_id
        assert df.index[0] == 0 and df.index[-1] == p.proj_len() - 1, point_id
        assert p.proj_len() == horizon == 12 * years
        assert p.proj_years() == years
        if p.shape() == "life":
            assert p.proj_years() == max(p.annuity_term(),
                                         OMEGA_AGE - p.age_at_entry() + 1)
            assert p.mort_rate(p.proj_len() - 1) == 1.0
            assert p.lives_if(p.proj_len()) == 0.0
        else:
            assert p.proj_years() == p.annuity_term()
    certain = immediate_annuity.Projection[9]
    dropped = certain.annuity_payments(certain.proj_len() - 1)
    assert dropped == pytest.approx(CERTAIN_LAST_INSTALMENT, abs=WON)
    total = certain.result_cf()["annuity_payments"].sum()
    assert dropped / total == pytest.approx(0.0077, abs=5e-5)


def test_pitfall_the_mortality_rate_is_read_at_the_start_of_the_period(
        kr_immediate_anchor):
    """Pitfall 5: reading the mortality rate at the wrong end of the policy year.

    ``lives_if`` applies q^m at the age attained at the **start** of the policy year the
    month falls in.  Reading the age at the anniversary that ends it — ``x + t // 12 + 1``
    — raises the factor's mortality by a year throughout and gives an annuity of
    ₩412,381.78 a month, +2.23%, which is close enough to the model's own figure to look
    plausible.  ``check_lives_roll_fwd`` rebuilds the curve as an explicit product of
    (1 − q^m) with no reference to the recursion, so the off-by-one shows up from the first
    month rather than as a plausible-looking annuity.
    """
    a = kr_immediate_anchor
    assert a.check_lives_roll_fwd() is True
    for t in range(1, a.proj_len() + 1):
        assert a.lives_if(t) == pytest.approx(
            a.lives_if(t - 1) * (1.0 - a.mort_rate_mth(t - 1)), rel=1e-14)
    built = 1.0                                # the same curve as an explicit product
    for t in range(0, a.proj_len()):
        assert a.lives_if(t) == pytest.approx(built, abs=1e-14)
        built *= (1.0 - a.mort_rate_mth(t))
    assert built == 0.0                        # q(110) = 1 closes the table
    assert a.lives_if(a.proj_len()) == 0.0
    with pytest.raises(FormulaError):
        a.mort_rate(a.proj_len())          # 보험나이 111 is off the shipped table
    # The age read at the end of the policy year rather than at its start.
    table = pd.read_csv(CSV_DIR / "mort_table.csv").set_index(["sex", "age"])

    def wrong_q(t):
        x = min(a.age_at_entry() + t // 12 + 1, OMEGA_AGE)
        q = float(table.loc[(a.sex(), x), "mort_rate"])
        return 1.0 / (12 - t % 12) if q >= 1.0 else 1.0 - (1.0 - q) ** (1.0 / 12.0)

    v = 1.0 / (1.0 + a.crediting_rate_mth(0))
    lives, g = [1.0], a.annuity_term_mths()
    for t in range(0, a.proj_len()):
        lives.append(lives[-1] * (1.0 - wrong_q(t)))
    wrong = sum(v ** (t + 1) * max(lives[t + 1], 1.0 if t + 1 <= g else 0.0)
                for t in range(0, a.proj_len()))
    assert a.av_pp_init() / wrong == pytest.approx(WRONG_END_ANNUITY, abs=WON)
    assert (a.av_pp_init() / wrong) / a.annuity_pp(0) - 1.0 == pytest.approx(
        WRONG_END_UPLIFT, abs=5e-6)


def test_pitfall_the_model_runs_on_boheom_nai_and_not_man_nai(immediate_annuity):
    """Pitfall 6: running the model on 만나이 instead of 보험나이.

    The tables, the model point column and the issue-age band are all 보험나이; the 완전생명표
    and every Korean population statistic are 만나이, and the six-month rule makes the two
    differ for half of all issue dates.  The error is worth about half a year of ageing on
    every row and **raises nothing**, so the basis is recorded in the registry metadata and
    named in the docstring where a reader will meet it.
    """
    assert MODELS["Immediate_KR_S"][1]["age_basis"] == "보험나이"
    assert MODELS["Immediate_KR_S"][1]["grid"] == "monthly"
    proj = immediate_annuity.Projection.doc
    assert "보험나이" in proj and "만나이" in proj
    assert "six-month rule" in proj
    doc = immediate_annuity.Projection.cells["age"].doc
    assert "보험나이" in doc and "계약해당일" in doc
    a = immediate_annuity.Projection[1]
    assert a.age(0) == a.age_at_entry()
    assert a.age(11) == a.age_at_entry()       # 보험나이 steps on the 계약해당일 only
    assert a.age(12) == a.age_at_entry() + 1
    assert a.age(120) == a.age_at_entry() + 10
    assert a.mort_rate(120) == 0.00728         # the published rate at 보험나이 70


def test_pitfall_the_mortality_table_is_never_the_gyeongheom_saengmyeongpyo():
    """Pitfall 7: presenting ``mort_table.csv`` as the 경험생명표.

    It is a **[std]** Makeham construction on three published anchors, it misses the
    보험나이 50 anchor by +22.01% for men, and the 제10회 경험생명표 is not published at all.
    Every row carries a ``provenance`` cell, the two fit-anchor rows per sex say they are the
    published 개인연금사망률 reproduced exactly, and the residual row reports its own miss
    rather than hiding it.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert (table["provenance"].str.strip() != "").all()
    assert table["provenance"].str.contains("NOT published|residual|limiting age").any()
    for (sex, age), rate in SOURCED_MORT_ANCHORS.items():
        row = table[(table["sex"] == sex) & (table["age"] == age)].iloc[0]
        assert row["mort_rate"] == pytest.approx(rate, abs=5e-12)
        assert "fit anchor" in row["provenance"]
        assert "[S1 IV-2]" in row["provenance"]
    residual = table[(table["sex"] == "M") & (table["age"] == 50)].iloc[0]
    assert residual["mort_rate"] / 0.00225 == pytest.approx(1.220, abs=5e-4)
    assert "residual" in residual["provenance"]
    for sex in ("M", "F"):
        sub = table[table["sex"] == sex]
        assert sub["age"].min() == 40 and sub["age"].max() == OMEGA_AGE
        assert sub[sub["age"] == OMEGA_AGE]["mort_rate"].iloc[0] == 1.0
        assert not sub["provenance"].str.contains("경험생명표를 전재").any()


def test_pitfall_the_life_shape_annuity_is_not_re_struck_each_year(immediate_annuity):
    """Pitfall 8: recomputing the life-shape annuity from the fund each year.

    ``av_pp`` on the life shape is **not** the reserve and goes negative at t = 330; an
    annuity re-struck as V(t)/ä(x+t, ·) would collapse toward zero and then turn negative.
    The 약관 bases the annuity on 「연금개시시의 계약자적립액」 and the annuitant-mortality
    ratchet is inert on an immediate annuity, there being no interval between issue and
    annuitisation.
    """
    for point_id in (1, 2, 3, 4, 5):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == "life"
        level = p.annuity_pp(0)
        assert all(p.annuity_pp(t) == level for t in range(0, p.proj_len())), point_id
        assert p.check_rate_level() is True, point_id
    a = immediate_annuity.Projection[1]
    assert a.annuity_pp(360) == a.annuity_pp(0)
    assert a.av_pp(360) < 0.0                   # a re-struck annuity would be negative
    assert a.annuity_pp(0) == pytest.approx(
        a.av_pp_init() / a.annuity_factor(), rel=1e-15)


def test_pitfall_av_pp_is_not_floored_at_zero(kr_immediate_anchor):
    """Pitfall 9: flooring ``av_pp`` at zero on the life shape.

    It would hide the fact that a life annuity's fund is not its reserve and would break the
    retrospective closed form V(0)(1 + j)^t − A s(t, j) from t = 330 onward.  Nothing
    downstream reads the negative value: ``cv_pp`` is nil and surrender is impossible there.
    """
    a = kr_immediate_anchor
    assert a.av_pp(330) < 0.0
    assert min(a.av_pp(t) for t in range(0, a.proj_len() + 1)) < -1.4e8
    assert a.check_av_roll_fwd() is True
    j0 = a.crediting_rate_mth(0)
    for t in (330, 480, 611):
        assert a.av_pp(t) == pytest.approx(
            a.av_pp_init() * (1.0 + j0) ** t
            - a.annuity_pp(0) * a.accum_factor(t, j0), abs=1e-3)
        assert a.cv_pp(t) == 0.0
    assert all(a.claims(t, "LAPSE") == 0.0 for t in range(0, a.proj_len()))
    assert "payment obligation remains" in a.cells["pols_if"].doc


def test_pitfall_the_retention_is_re_struck_every_year(immediate_annuity):
    """Pitfall 10: computing the retention once, at inception, instead of every year.

    On a level rate the two agree and the fund still lands on M, so the error is **invisible
    on model points 6 and 7**.  It appears only on a stepping rate: point 8's retention runs
    18,251.70 → 22,683.65 over 240 months, and the fund reaches ₩100,000,000.00 exactly
    because R is recomputed against the remaining term at the current rate.  On the monthly
    grid "every year" is really every **month**, which is what makes the retention a smooth
    curve inside a band instead of a staircase.
    """
    p = immediate_annuity.Projection[8]
    frozen = p.retention_pp(0)
    path = [p.retention_pp(t) for t in range(0, p.proj_len())]
    assert path[0] == pytest.approx(18251.6955717737, abs=SUB_WON)
    assert path[-1] == pytest.approx(22683.6542366892, abs=SUB_WON)
    assert path == sorted(path)
    assert path[-1] / frozen - 1.0 > 0.23
    for t in (0, 60, 120, 239):
        m = p.annuity_term_mths() - t
        assert p.retention_pp(t) == pytest.approx(
            (p.maturity_benefit() - p.av_pp(t))
            / p.accum_factor(m, p.crediting_rate_mth(t)), rel=1e-13)
    assert p.av_pp(240) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    assert p.check_av_terminal() is True
    assert p.check_av_roll_fwd() is True

    # The error itself, run: an implementation that strikes R once and holds the annuity
    # it implies.  On the level-rate point that reproduces the model's whole fund path to
    # float noise and still lands on M, which is what makes it invisible there; on the
    # stepping rate it lands ₩6,393,965 short of the 만기보험금.
    def frozen_fund(projection):
        annuity, fund = projection.annuity_pp(0), projection.av_pp_init()
        for t in range(0, projection.proj_len()):
            fund = fund * (1.0 + projection.crediting_rate_mth(t)) - annuity
        return fund

    level = immediate_annuity.Projection[6]
    assert frozen_fund(level) == pytest.approx(MATURITY_BENEFIT, abs=1e-3)
    assert level.av_pp(120) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    assert frozen_fund(p) == pytest.approx(93606034.58, abs=WON)
    assert MATURITY_BENEFIT - frozen_fund(p) == pytest.approx(6393965.42, abs=WON)
    assert abs(MATURITY_BENEFIT - frozen_fund(p)) > 0.06 * MATURITY_BENEFIT


def test_pitfall_the_floor_is_a_rate_on_the_fund_not_a_floor_on_the_annuity(
        immediate_annuity):
    """Pitfall 11: reading the 최저보증이율 as a floor on the annuity.

    It is a rate on the fund.  Point 8 is the demonstration and it is the substance of the
    dispute in one table: the monthly annuity falls **50.62%** from the first month to the
    121st — the second step alone costing 33.99% and the income falling from ₩80,175.25 to
    ₩39,588.40 — while the floor is honoured at every step and the fund reaches its
    만기보험금 to the won.  The disputed 2012 contract's own published annuity fell 55.4% in
    five years on the same mechanism.
    """
    p = immediate_annuity.Projection[8]
    assert all(p.crediting_rate(t) == p.min_guar_rate(t)
               for t in range(0, p.proj_len()))
    assert p.annuity_pp(120) / p.annuity_pp(119) - 1.0 == pytest.approx(
        SECOND_STEP_FALL, abs=5e-5)
    assert p.annuity_pp(120) / p.annuity_pp(0) - 1.0 == pytest.approx(
        TWO_STEP_FALL, abs=5e-5)
    assert p.annuity_pp(120) < 0.5 * p.annuity_pp(0)
    assert p.annuity_pp(0) == pytest.approx(FLOOR_MONTHLY[0], abs=WON)
    assert p.annuity_pp(120) == pytest.approx(FLOOR_MONTHLY[1], abs=WON)
    assert p.av_pp(240) == pytest.approx(AV_PP_240_POINT_8, abs=1e-6)
    assert p.check_av_terminal() is True and p.check_av_roll_fwd() is True
    # The floor was honoured at every single step while the annuity halved.
    assert all(p.crediting_rate(t) >= 0.0075 for t in range(0, p.proj_len()))
    assert all(p.av_pp(t + 1) > p.av_pp(t) for t in range(0, p.proj_len()))
    # The floor never touches the annuity: it is applied to the fund and to nothing else.
    for t in (0, 60, 120, 239):
        assert p.annuity_pp(t) == pytest.approx(
            p.av_pp(t) * p.crediting_rate_mth(t) - p.retention_pp(t), rel=1e-13)
    doc = immediate_annuity.Projection.cells["min_guar_rate"].doc
    assert "never a floor on the annuity" in doc


def test_pitfall_the_floor_bands_are_half_open_in_completed_policy_years(
        immediate_annuity):
    """Pitfall 12: getting the floor's duration bands wrong by one.

    The bands are half-open [dur_from, dur_to) in **completed policy years**, and the grid
    counts months, so the test is on ``t // 12``: t = 0 … 59 is 1.25%, t = 60 … 119 is 1.00%,
    t ≥ 120 is 0.75%.  Testing on ``t // 12 + 1`` moves both steps a year early, and testing
    on ``t`` itself moves them eleven years early.
    """
    p = immediate_annuity.Projection[8]
    for t, rate in MIN_GUAR_SCHEDULE.items():
        assert p.min_guar_rate(t) == rate, t
    assert p.crediting_rate(59) == 0.0125 and p.crediting_rate(60) == 0.0100
    assert p.crediting_rate(119) == 0.0100 and p.crediting_rate(120) == 0.0075
    assert [p.min_guar_rate(t) for t in range(0, 60)] == [0.0125] * 60
    assert [p.min_guar_rate(t) for t in range(60, 120)] == [0.0100] * 60
    table = pd.read_csv(CSV_DIR / "crediting_table.csv")
    bands = table[table["basis_id"] == "min_guar"][["dur_from", "dur_to"]]
    assert list(bands["dur_from"]) == [0, 5, 10]
    assert list(bands["dur_to"]) == [5, 10, 999]
    with pytest.raises(FormulaError):
        p.min_guar_rate(12 * 999)               # outside every band, and it says so


def test_pitfall_the_annuity_charge_is_not_netted_off_the_payment(kr_immediate_anchor):
    """Pitfall 13: netting the 0.80% 연금수령기간 중 비용 off the policyholder's payment.

    It is disclosed in the **cost** table and not the benefit table, so it is an insurer
    expense measured on the annuity and the annuitant receives the full amount.  On the
    monthly grid that is 0.80% of each 연금월액, which over twelve months is exactly the
    0.80% of the 연금연액 the cost table discloses.  Netting it would cut the anchor's income
    by ₩3,226.96 a month and would also break the pricing identity, since the fund bought the
    gross annuity.
    """
    a = kr_immediate_anchor
    for t in range(1, a.proj_len()):
        assert a.expenses(t) == pytest.approx(
            0.0080 * a.annuity_payments(t), rel=1e-13), t
    assert a.expenses(1) == pytest.approx(EXPENSE_CHARGE, abs=SUB_WON)
    assert a.annuity_payments(1) == pytest.approx(a.annuity_pp(1), rel=1e-15)
    # Twelve monthly charges are 0.80% of the 연금연액, which is what the table discloses.
    assert sum(a.expenses(t) for t in range(1, 13)) == pytest.approx(
        0.0080 * a.annuity_pp_annual(0), rel=1e-13)
    # The payment is the gross annuity, and the identity closes on the gross annuity.
    assert a.annuity_pp(0) * (1.0 - 0.0080) < a.annuity_payments(0)
    assert a.check_annuity_basis() is True
    # The charge follows the payment's weight, not the policy count.
    assert a.expenses(240) == pytest.approx(
        0.0080 * a.annuity_pp(240) * a.payment_factor(240), rel=1e-14)
    assert a.expenses(611) == 0.0


def test_pitfall_no_death_benefit_is_paid_on_the_jongsin_yeongeum_hyeong(
        immediate_annuity):
    """Pitfall 14: paying a death benefit on the 종신연금형.

    There is none after annuitisation — 「별도의 사망보험금은 지급되지 않습니다」 — the unpaid
    guaranteed instalments being what survives the annuitant, and they are already inside
    ``annuity_payments``.  Adding one double-counts the guarantee.
    """
    for point_id in (1, 2, 3, 4, 5):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == "life"
        assert p.db_rate() == 0.0
        assert p.risk_prem_rate() == 0.0        # and no 위험보험료 is deducted for one
        assert p.risk_prem_pp() == 0.0
        assert all(p.claims(t, "DEATH") == 0.0
                   for t in range(0, p.proj_len())), point_id
        assert p.result_cf()["claims_death"].sum() == 0.0
    a = immediate_annuity.Projection[1]
    # What survives the annuitant is inside the annuity, at a weight of one.
    assert a.payment_factor(5) == 1.0 > a.lives_if(6)
    assert a.annuity_payments(5) == pytest.approx(a.annuity_pp(5), rel=1e-15)


def test_pitfall_the_death_benefit_is_measured_on_the_fund_carried_forward(
        immediate_annuity):
    """Pitfall 15: paying the death benefit on the fund at the start of the period.

    Deaths are taken at the **end**, after the crediting and after the annuity due to the
    survivors, so the 사망보험금 on the inheritance shape is ρP + V(t + 1) and not ρP + V(t).
    On point 6 at t = 0 that is q^m × 105,066,551.06 = ₩30,957.20 rather than
    q^m × 105,030,000.00 = ₩30,946.43.  On the monthly grid the convention costs at most a
    month of fund growth where on the annual grid it cost a year of it.
    """
    p = immediate_annuity.Projection[6]
    assert p.claims(0, "DEATH") == pytest.approx(DESIGNED["claims_death"], abs=SUB_WON)
    assert p.claims(0, "DEATH") == pytest.approx(
        p.mort_rate_mth(0) * (0.10 * p.prem_pp() + p.av_pp(1)), rel=1e-13)
    start_of_period = p.mort_rate_mth(0) * (0.10 * p.prem_pp() + p.av_pp(0))
    assert start_of_period == pytest.approx(30946.43, abs=WON)
    assert p.claims(0, "DEATH") - start_of_period == pytest.approx(10.77, abs=WON)
    # On the certain shape it is the 10% alone: the instalments run on their own dates.
    certain = immediate_annuity.Projection[9]
    assert certain.claims(0, "DEATH") == pytest.approx(
        certain.pols_death(0) * 0.10 * certain.prem_pp(), rel=1e-14)
    assert certain.db_rate() == 0.10


def test_pitfall_no_lapse_decrement_touches_the_life_shape(immediate_annuity):
    """Pitfall 16: applying a lapse decrement to the 종신연금형.

    Surrender is contractually impossible from month one — 「종신연금이 지급개시된 이후에는
    해지할 수 없습니다」 — and on an immediate annuity the annuity begins a month after
    inception, so the contract is irreversible.  A life-shape model point carrying a
    surrender rate is a defect in the table rather than a scenario, and
    ``check_surr_value()`` asserts a nil rate **and** a nil surrender value rather than
    leaving either to the CSV.
    """
    table = immediate_annuity.Data.model_point_table()
    for point_id in (1, 2, 3, 4, 5):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == "life"
        assert float(table.loc[point_id, "lapse_rate"]) == 0.0
        assert p.check_surr_value() is True, point_id
        assert all(p.lapse_rate(t) == 0.0 for t in range(0, p.proj_len()))
        assert all(p.pols_lapse(t) == 0.0 for t in range(0, p.proj_len()))
        assert all(p.cv_pp(t) == 0.0 for t in range(0, p.proj_len()))
        assert all(p.surr_if(t) == 1.0 for t in range(0, p.proj_len()))
        assert p.result_cf()["claims_lapse"].sum() == 0.0


def test_pitfall_no_surrender_fires_in_the_final_period(immediate_annuity):
    """Pitfall 17: letting a surrender fire in the final period.

    ``lapse_rate(t) = 0`` through the whole final **policy year** on every shape.  Without
    it a contract in its last year is surrendered a moment before its 만기보험금 and the
    maturity benefit is diverted into a surrender value of a different amount for no reason
    any contract states.  Suppressing it over the year rather than over the last month is
    what makes the monthly grid's in-force reproduce the annual-step model's at every
    계약해당일.
    """
    for point_id in (6, 7, 9):
        p = immediate_annuity.Projection[point_id]
        n = p.proj_len() - 1                   # the last projected month
        assert p.lapse_rate(n - 12) == 0.02
        assert all(p.lapse_rate(t) == 0.0 for t in range(n - 11, n + 1))
        assert all(p.lapse_rate_mth(t) == 0.0 for t in range(n - 11, n + 1))
        assert p.pols_lapse(n) == 0.0
        assert p.claims(n, "LAPSE") == 0.0, point_id
        assert p.result_cf().loc[n, "claims_lapse"] == 0.0
    inheritance = immediate_annuity.Projection[6]
    assert inheritance.claims(inheritance.proj_len() - 1, "MATURITY") > 0.0
    assert inheritance.cv_pp(inheritance.proj_len()) == pytest.approx(
        MATURITY_BENEFIT, abs=1e-6)          # the two amounts a lapse would confuse


def test_pitfall_the_maturity_benefit_is_weighted_one_period_later(immediate_annuity):
    """Pitfall 18: weighting the 만기보험금 by ``pols_if(N − 1)`` instead of ``pols_if(N)``.

    It is payable on survival **to** maturity, one further period of decrement away:
    ₩79,495,349.97 on point 6, against ₩79,539,188.73 if the earlier weight were used.  The
    gap is now one month of decrement rather than one year's, so the slip is a tenth as
    expensive and correspondingly harder to see.
    """
    p = immediate_annuity.Projection[6]
    n = p.proj_len() - 1                       # the last projected period
    assert p.claims(n, "MATURITY") == pytest.approx(
        DISPUTE_TOTALS[6]["claims_maturity"], abs=WON)
    assert p.claims(n, "MATURITY") == pytest.approx(
        p.pols_if(n + 1) * p.maturity_benefit(), rel=1e-14)
    earlier = p.pols_if(n) * p.maturity_benefit()
    assert earlier == pytest.approx(MATURITY_EARLIER_WEIGHT, abs=WON)
    assert earlier - p.claims(n, "MATURITY") == pytest.approx(43838.76, abs=WON)
    assert p.pols_if(n + 1) < p.pols_if(n)


def test_pitfall_the_hundred_point_one_percent_fund_floor_is_not_applied(
        kr_immediate_anchor):
    """Pitfall 19: applying the 100.1%-of-premiums fund floor.

    It is a **deferred**-contract mechanic — the floor on the fund at annuitisation, where a
    premium has been accumulating — and applying it to an immediate annuity would erase the
    entire 3.50% load on day one and make ``check_premium_split()`` fail by ₩3,600,000.
    """
    a = kr_immediate_anchor
    assert a.av_pp_init() == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert a.av_pp_init() < a.prem_pp()
    floored = 1.001 * a.prem_pp()
    assert floored - a.av_pp_init() == pytest.approx(3600000.0, abs=WON)
    assert a.check_premium_split() is True
    names = set(a.cells) | set(a.refs)
    for absent in ("av_floor_pp", "av_floor_ratio", "prem_floor_rate", "cv_floor_ratio"):
        assert absent not in names, f"{absent}: a deferred-contract mechanic"


def test_pitfall_nothing_discounted_is_published(immediate_annuity, kr_immediate_anchor):
    """Pitfall 20: discounting the projected flows at the crediting rate and calling it a
    reserve.

    ``disc_factor`` exists for the pricing identity and for ``retention_shortfall_pp()``
    only, both being statements about the **contract's own basis** rather than about value.
    The best estimate discounts on a supervisory curve and the reserve is computed under
    감독규정 제6-11조, neither of which is in this model — so the statement carries no
    discounted column and must not acquire one.
    """
    a = kr_immediate_anchor
    columns = set(a.result_cf().columns) | set(a.result_pols().columns)
    for column in columns:
        assert "disc" not in column and "pv_" not in column, column
        assert not column.startswith("pv") and not column.endswith("_pv"), column
    names = set(immediate_annuity.Projection.cells)
    for absent in ("reserve_pp", "bel_pp", "csm_pp", "result_pv", "disc_rate"):
        assert absent not in names, absent
    assert "disc_factor" in names               # it exists, and is not a column
    doc = immediate_annuity.Projection.cells["disc_factor"].doc.replace("*", "")
    assert "not a valuation rate" in doc
    assert a.disc_factor(0) == 1.0
    assert a.disc_factor(120) == pytest.approx(1.025 ** -10, rel=1e-13)


def test_pitfall_no_aggregate_claims_column_stands_beside_the_split(kr_immediate_anchor):
    """Pitfall 21: publishing a ``claims`` column beside the ``claims_*`` columns.

    A statement must not carry its own subtotal beside its parts, or the columns stop summing
    to ``net_cf``.  The ``claims(t, kind)`` cells stays and the column does not, and
    ``check_net_cf()`` rebuilds the ledger from the **published** columns so that the
    difference is load-bearing rather than stylistic.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    assert "claims" not in df.columns
    assert [c for c in df.columns if c.startswith("claims")] == [
        "claims_death", "claims_lapse", "claims_maturity"]
    assert a.check_net_cf() is True
    with pytest.raises(FormulaError):
        a.claims(1, "SURRENDER")                # the kind argument validates
    assert a.claims(1, "DEATH") == 0.0


# ---------------------------------------------------------------------------
# The [std] parameters, and the modules asserted in both positions


@pytest.mark.parametrize("shape", sorted(CHARGE_RATES))
def test_the_std_charge_parameters_the_notes_state(immediate_annuity, shape):
    """The charge basis by shape, read off the model rather than off the CSV.

    Every rate here is [std] in its adoption or in its derivation, and a silent change to any
    of them would move a result rather than fail a test without this.  The two that carry the
    product's structure are ``acq_expense_rate``, which is the load less the commission and
    is what makes the premium split close, and ``comm_rate``, which sits **below** the
    계약체결비용 so that the charge covers the commission at the same moment.
    """
    point_id = {"life": 1, "inheritance": 6, "certain": 9}[shape]
    p = immediate_annuity.Projection[point_id]
    assert p.shape() == shape
    for name, value in CHARGE_RATES[shape].items():
        assert getattr(p, name)() == value, name
    assert p.expense_load_rate() == pytest.approx(0.0350, rel=1e-15)
    assert p.acq_expense_rate() == pytest.approx(
        p.expense_load_rate() - p.comm_rate(), rel=1e-15)
    assert p.av_pp_init() / p.prem_pp() == pytest.approx(
        1.0 - 0.0350 - CHARGE_RATES[shape]["risk_prem_rate"], rel=1e-15)


def test_the_std_rate_and_behaviour_assumptions_the_notes_state(immediate_annuity):
    """공시이율 2.50%, 최저보증이율 1.25 / 1.00 / 0.75%, ω = 110, and w = 2.00%.

    The declared rate is a **scalar** and not a derived quantity — 감독규정 제7-65조제3항
    makes it the product of a 공시기준이율 majority-weighted to the insurer's own
    운용자산이익률, which no model can derive — and the limiting age is what makes the
    life-shape obligation exhausted rather than truncated.  The surrender rate is the one row
    of the model's [std] table that is a **placeholder**: no retrieved source gives a rate for
    즉시연금 by duration, by shape or at all, so it is carried as a model point column where
    its effect can be isolated rather than in a table where it would look like a duration
    curve — and it is not second-order, producing ₩15.9m of ``claims_lapse`` on point 6
    against ₩17.0m of annuity payments.
    """
    a = immediate_annuity.Projection[1]
    assert a.decl_rate() == DECL_RATE
    assert [a.min_guar_rate(t) for t in (0, 59, 60, 119, 120)] == [
        0.0125, 0.0125, 0.0100, 0.0100, 0.0075]
    assert immediate_annuity.Projection.refs["omega_age"] == OMEGA_AGE
    table = pd.read_csv(CSV_DIR / "crediting_table.csv")
    assert set(table["basis_id"]) == {"decl_2017", "min_guar"}
    decl = table[table["basis_id"] == "decl_2017"]
    assert set(decl["decl_rate"]) == {DECL_RATE}     # one rate per basis, never a mean
    assert list(decl["min_guar_rate"]) == [0.0125, 0.0100, 0.0075]
    assert set(table[table["basis_id"] == "min_guar"]["decl_rate"]) == {0.0}
    assert table["provenance"].notna().all()
    doc = immediate_annuity.Projection.cells["decl_rate"].doc.replace("*", "")
    assert "It is a scalar and not a derived quantity" in doc

    points = immediate_annuity.Data.model_point_table()
    assert set(points["lapse_rate"]) == {0.0, 0.02}
    for point_id in (6, 7, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.lapse_rate(0) == 0.02
        assert p.shape() in ("inheritance", "certain")
    df = immediate_annuity.Projection[6].result_cf()
    assert df["claims_lapse"].sum() == pytest.approx(15854560.39, abs=WON)
    assert df["claims_lapse"].sum() / df["annuity_payments"].sum() == pytest.approx(
        0.934, abs=5e-4)
    # There is no lapse table: the assumption has nowhere else to hide, and the monthly
    # conversion is derived from the annual rate rather than being a second assumption.
    assert not (CSV_DIR / "lapse_table.csv").exists()
    assert "lapse_rate_mth" in set(immediate_annuity.Projection.cells)
    p = immediate_annuity.Projection[6]
    assert 1.0 - (1.0 - p.lapse_rate_mth(0)) ** 12 == pytest.approx(
        p.lapse_rate(0), rel=1e-13)
    assert p.lapse_rate_mth(0) > p.lapse_rate(0) / 12.0


def test_the_four_optional_modules_are_asserted_in_both_positions(immediate_annuity):
    """The retention, the stepping floor, voluntary surrender and the longer guarantee.

    The anchor exercises none of the four, which is why its numbers are independent of all
    four; a module that is only ever seen switched off is machinery nobody has run, so each
    is asserted in the position the anchor holds it in **and** on the point that exercises it.
    """
    a = immediate_annuity.Projection[1]
    # 1. The retention: inert on the anchor, and both bases on points 6 and 7.
    assert all(a.retention_pp(t) == 0.0 for t in range(0, a.proj_len()))
    assert immediate_annuity.Projection[6].retention_pp(0) > 0.0
    assert immediate_annuity.Projection[7].retention_pp(0) == 0.0
    # 2. The stepping floor: inert on the anchor, binding at every duration on point 8.
    assert all(a.crediting_rate(t) == a.decl_rate() for t in range(0, a.proj_len()))
    stepping = immediate_annuity.Projection[8]
    assert len({stepping.crediting_rate(t)
                for t in range(0, stepping.proj_len())}) == 3
    # 3. Voluntary surrender: off by contract on the anchor, on for points 6 to 9.
    assert all(a.pols_lapse(t) == 0.0 for t in range(0, a.proj_len()))
    certain = immediate_annuity.Projection[9]
    assert certain.pols_lapse(0) == pytest.approx(certain.lapse_rate_mth(0))
    # 4. The longer guarantee: ten years on the anchor, twenty on point 3.
    longer = immediate_annuity.Projection[3]
    assert a.annuity_term() == 10 and longer.annuity_term() == 20
    assert a.annuity_term_mths() == 120 and longer.annuity_term_mths() == 240
    assert longer.annuity_factor() > a.annuity_factor()
    assert longer.annuity_pp(0) < a.annuity_pp(0)
    assert all(longer.pols_if(t) == 1.0 for t in range(0, 240))
    assert longer.pols_exit(239) == pytest.approx(
        longer.pols_if_init() - longer.lives_if(240), rel=1e-14)
    assert longer.pols_if(240) == pytest.approx(longer.lives_if(240), rel=1e-15)


def test_the_model_point_table_exercises_the_product(immediate_annuity):
    """Both sexes, all three shapes, both retention bases, both crediting bases.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.  The premium envelope runs from the
    ₩10,000,000 carrier minimum through the ₩100,000,000 median and tax cap to the
    ₩5,000,000,000 maximum, and the issue ages span the 45–80 band.
    """
    table = immediate_annuity.Data.model_point_table()
    assert len(table) == 10 and list(table.index) == list(range(1, 11))
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["shape"]) == {"life", "inheritance", "certain"}
    assert set(table["retention_basis"]) == {"as_designed", "as_ordered"}
    assert set(table["crediting_basis"]) == {"decl_2017", "min_guar"}
    assert table["age_at_entry"].min() == 45 and table["age_at_entry"].max() == 80
    assert table["prem_pp"].min() == 10000000
    assert table["prem_pp"].max() == 5000000000
    assert set(table["annuity_term"]) == {10, 20, 30}
    assert set(table["pols_if_init"]) == {1.0}
    # Points 6 and 7 are the same contract, which is what makes the panel a comparison.
    assert (table.loc[6].drop(["policy_id", "retention_basis"]).tolist()
            == table.loc[7].drop(["policy_id", "retention_basis"]).tolist())


def test_the_docstrings_carry_this_products_own_reference_material(immediate_annuity):
    """Product-specific phrases a reader relies on, which a generic sweep cannot know.

    The model docstring names the payout-phase chassis and the three shapes; the Projection
    docstring carries the notes' symbol map, the 보험나이 basis and the four names that
    needed care; and the Data docstring explains why there is no lapse table, no
    surrender-value schedule and no commission scale.  Asserted so that they cannot go stale
    silently while the numbers stay right.
    """
    doc = immediate_annuity.doc
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "no acquisition strain", "종신연금형", "상속연금형", "확정기간연금형",
                   "즉시연금 과소지급"):
        assert phrase in doc, phrase
    proj = immediate_annuity.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "pols_if", "annuity_pp", "retention_pp",
                  "payment_factor", "av_pp", "annuity_factor", "crediting_rate",
                  "retention_shortfall_pp"):
        assert cells in proj, cells
    assert "payment obligation remains" in proj
    assert "보증지급기간" in proj and "산출방법서" in proj
    data = immediate_annuity.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "charge_table",
                  "crediting_table"):
        assert cells in data, cells
    assert "no lapse table" in data
