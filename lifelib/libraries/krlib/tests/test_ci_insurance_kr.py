"""Golden and structural tests for CI_KR_S.

The golden values are the worked example in
products/ci_insurance/technical-notes.md ("Worked example"), which projects the anchor
cell 남자 / 보험나이 40 / 보험가입금액 KRW 100,000,000 (1억원) / 종신 with CI cover to the
100세 계약해당일 / 20년납 / 80% 선지급형 / 저해지환급형 k = 0.50, at an annual premium of
KRW 3,680,880 — twelve times the KRW 306,740 monthly figure one carrier publishes for
exactly that cell.  They are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the won's second decimal,
in-force in the cash flow table to the six decimals it prints, the decrement basis to the
eight or ten decimals of its own columns, and the hand traces' counts to the sixteen the
traces carry.

**What this module is about is the acceleration.**  The chassis this product sits on —
the 종신보험 whole life model — supplies the 계약자적립액, the 해약환급금 net of a
해약공제액 capped by the 표준해약공제액, the 저해지환급형 suppression and its step at
납입완료, the 보험계약대출 and the 납입면제.  None of that is retested here.  What is new
is that **one decrement produces two payments at two dates on one sum assured**: the
선지급 of 80% of the 기본보험금 at the CI date, and a residual death benefit of the
complement whenever death follows, floored at 105% of an account that keeps growing.  So
the projection runs two cohorts, the post-CI one indexed by the anniversary it accelerated
at, and almost every test below is a statement about that structure.

The time index ``t`` is **0-based**: ``t = 0`` is the first policy year, the frame is
``range(proj_len())`` and the contractual policy year label is ``t + 1``.  The contract's
*state* -- ``pol_val_pp``, ``surr_chg_pp``, ``cv_std_pp``, ``cv_pp``, ``cv_pp_ci``,
``base_benefit_pp``, ``cum_prem_pp``, ``resid_db_pp``, ``loan_avail_pp``, ``pol_loan_draw``
and the post-CI cohort label ``s`` -- is carried on the **anniversary** clock instead, which
runs ``0 ... proj_len()`` with 0 at issue and does not move with the frame.  Period ``t``
opens at anniversary ``t`` and closes at anniversary ``t + 1``, so a claim or a surrender
arising in period ``t`` is paid the anniversary-``t + 1`` amount.  Constants below whose
*name* carries a year number are **contractual policy-year labels** (policy year 1 is
``t = 0``); constants naming an anniversary did not move at all.

Every product fact the notes list under "Known modeling pitfalls" earns its own test,
named after the pitfall, because each of them is a way an implementation can look right
and be wrong:

* the acceleration is a **transition**, not an exit, so the roll-forward has four terms;
* the residual floor is **two-sided**, and its two limbs bind at opposite ends;
* the nominal is read off the entry anniversary and the floor off the current one;
* collapsing the post-CI cohorts loses the first-year 감액 one — invisible on a male
  cell at 0.15% of year-one claims and 17.86% on the female twin;
* the premium annuity must carry the CI decrement, worth 4.8% of the annuity;
* the post-CI cohort never pays a premium;
* the suppression has **two** exits and one of them is random;
* the step at 납입완료 is exactly 1 / k on one anniversary, not the adjacent-year ratio;
* the step is not a surrender-charge effect — the charge is gone thirteen years earlier;
* the 표준해약공제액 is computed on the pre-acceleration sum assured;
* CI before death before lapse, an ordering worth a factor of seven at attained 60;
* the two payments are one policy year apart, never simultaneous;
* the CI decrement stops at n_CI and nothing else does — three end dates, one horizon;
* ``ci_rate`` is a first-event rate and not a sum of marginal incidences;
* there is no survival period, the Korean supervisor having refused one;
* ``pols_if`` is the total in force, both states, and it weights maintenance expense;
* the claim expense is charged on three kinds of event, not one;
* every loan-netted payment is floored at zero and the 선지급 is not netted at all; and
* the two decrement tables are this product's, not the chassis's.

The nine ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep cannot notice a check that has quietly disappeared; that they are *true* on
every shipped model point is asserted once, in ``test_model_conventions_kr.py``, whose
sweep discovers them generically.  The optional modules are asserted in **both** positions
of their switch, and the [std] scalar assumptions the notes state are read off the model,
so that a silent change to an assumption fails a test rather than moving a result.
"""
import io
import re
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

MODEL_DIR = LIB / MODELS["CI_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

WON = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-7       # pols_if in the cash flow table, displayed to 6 d.p.
TRACE = 5e-16        # the hand traces' counts, displayed to 16 d.p.
RATE = 5e-11         # ci_rate and lapse_rate, displayed to 10 d.p.
MORT = 5e-9          # mort_rate and mort_rate_ci, displayed to 8 d.p.
CAUSE = 5e-10        # the per-cause incidence grid, displayed to 9 d.p.
SPLIT = 5e-11        # the decrement split, displayed to 10 d.p.


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
# "Derived scalars, at full precision", the anchor cell's own table.
OMEGA = 110
PROJ_YEARS = 71                      # policy years
PROJ_LEN = 852                        # months, 12 x PROJ_YEARS
CI_COVER_END = 720                   # months of CI cover, to the 100세 계약해당일
PREM_PERIOD = 20                     # 납입기간, policy years
PREM_PERIOD_MTHS = 240               # 납입기간, months
SURR_CHG_YEARS = 7
SURR_CHG_PERIOD_MTHS = 84            # 해약공제기간, months
DISC_FACTOR = 0.9756097560975611       # 1 / (1 + i), annual
DISC_FACTOR_MTH = 0.9979443979338495   # 1 / (1 + j), the one the EPVs use
PREM_INT_RATE_MTH = 0.0020598362698427 # j = (1 + i) ** (1 / 12) - 1
I_LOAN_MTH = 0.0032737397821989        # j_L, the monthly 보험계약대출이율
A0_1 = 45439079.6117764339          # epv_ben(0), the issue instant
A1_1 = 8242810.7636089316           # epv_resid(0)
ANNUITY_DUE_1 = 178.7102998490        # annuity_due(0), in MONTHS of premium
P_NET_MTH = 254261.1122592268       # prem_net_level_mth_pp()
P_NET = 3051133.3471107213        # prem_net_level_pp(), 12 x the monthly one
G_GROSS = 3680880.0000000000      # premium_pp(), sourced at 12 x KRW 306,740 [S4]
G_GROSS_MTH = 306740.0000000000    # premium_mth_pp(), the published monthly rate itself
LOADING = 1.2063976173            # G / P
P_NET_ANNUAL_STEP = 2968483.2020010490   # what the annual-step model solved for
MODAL_EFFECT = 1.0278425511        # P / P_NET_ANNUAL_STEP
SC_CAP = 3944704.00                  # surr_chg_cap_pp(), the 표준해약공제액
SC_CAP_RULE_OF_THUMB = 3987620.0     # 13 x the monthly premium [REG-R29]
SC_STEP = 46960.7619047619           # SC* / 84, one month's run-off
ACCEL_RATE = 0.80
BREAST_SHARE_M = 0.005
CI_WAIT_FACTOR = 0.7534246575342466    # 1 - 90/365, the first policy year's own exposure
CI_WAIT_SHARE_40 = 0.3675235630        # (cancer + ltc) / total at attained 40
LAPSE_ULT = 0.008

# The 90-day 보장개시일, month by month: nothing for two months, a twenty-fifth of the
# third, all of it thereafter.  The twelve sum to 12 x CI_WAIT_FACTOR = 9.0411 months.
CI_WAIT_FACTOR_MTH = {
    0: 0.0000000000,
    1: 0.0000000000,
    2: 0.0410958904,
    3: 1.0000000000,
    4: 1.0000000000,
}
CI_WAIT_MONTHS_YEAR_ONE = 9.0410958904   # sum over the first twelve months

# "Two cross-checks that fell out of the model rather than being imposed", and the one
# that does not agree.  The 50%% form is model point 3.
A0_1_HALF = 42142821.74             # epv_ben(0) at a = 0.50
P_NET_HALF_MTH = 235816.41          # prem_net_level_mth_pp() at a = 0.50
FORM_RELATIVITY_MODEL = 1.0782      # P(80%) / P(50%)
FORM_RELATIVITY_PUBLISHED = 338100 / 311640     # 1.085 at 남40 / 17대 / 기본환급형 [S4]

# "The decrement basis at the anchor", read at the LAST month of policy years 1 to 25.
# The unsuffixed rates are the ANNUAL ones the sources tabulate; the ``_m`` ones are the
# monthly conversions the roll-forward applies, and twelve of each compound back to it.
# policy year -> (age, ci, ci_m, mort, mort_m, mort_ci, mort_ci_m, lapse, lapse_m)
WORKED_EXAMPLE_BASIS = {
     1: (40, 0.0027834950, 0.0002322544, 0.00068000, 0.0000566843, 0.00204000, 0.0001701592, 0.1000000000, 0.0087416110),
     2: (41, 0.0030721810, 0.0002563763, 0.00070525, 0.0000587898, 0.00211575, 0.0001764837, 0.0784759970, 0.0067873987),
     3: (42, 0.0033921090, 0.0002831162, 0.00073395, 0.0000611831, 0.00220185, 0.0001836729, 0.0615848211, 0.0052828967),
     4: (43, 0.0037467810, 0.0003127692, 0.00076660, 0.0000639058, 0.00229980, 0.0001918523, 0.0483293024, 0.0041195089),
     5: (44, 0.0041401050, 0.0003456652, 0.00080372, 0.0000670014, 0.00241116, 0.0002011524, 0.0379269019, 0.0032168852),
     6: (45, 0.0045764400, 0.0003821723, 0.00084593, 0.0000705215, 0.00253779, 0.0002117289, 0.0297635144, 0.0025147858),
     7: (46, 0.0050606550, 0.0004227026, 0.00089392, 0.0000745239, 0.00268176, 0.0002237552, 0.0233572147, 0.0019675882),
     8: (47, 0.0055981780, 0.0004677161, 0.00094850, 0.0000790760, 0.00284550, 0.0002374348, 0.0183298071, 0.0015404689),
     9: (48, 0.0061950720, 0.0005177277, 0.00101056, 0.0000842524, 0.00303168, 0.0002529917, 0.0143844989, 0.0012066846),
    10: (49, 0.0068581080, 0.0005733133, 0.00108113, 0.0000901388, 0.00324339, 0.0002706851, 0.0112883789, 0.0009456007),
    11: (50, 0.0075948480, 0.0006351179, 0.00116137, 0.0000968324, 0.00348411, 0.0002908072, 0.0088586679, 0.0007412367),
    12: (51, 0.0084137370, 0.0007038632, 0.00125261, 0.0001044441, 0.00375783, 0.0003136932, 0.0069519280, 0.0005811815),
    13: (52, 0.0093242150, 0.0007803585, 0.00135635, 0.0001130995, 0.00406905, 0.0003397215, 0.0054555948, 0.0004557737),
    14: (53, 0.0103368310, 0.0008655108, 0.00147431, 0.0001229423, 0.00442293, 0.0003693268, 0.0042813324, 0.0003574797),
    15: (54, 0.0114633740, 0.0009603373, 0.00160843, 0.0001341347, 0.00482529, 0.0004029995, 0.0033598183, 0.0002804169),
    16: (55, 0.0127170250, 0.0010659796, 0.00176092, 0.0001468619, 0.00528276, 0.0004412995, 0.0026366509, 0.0002199869),
    17: (56, 0.0141125250, 0.0011837200, 0.00193430, 0.0001613347, 0.00580290, 0.0004848659, 0.0020691381, 0.0001725919),
    18: (57, 0.0156663570, 0.0013149989, 0.00213143, 0.0001777929, 0.00639429, 0.0005344256, 0.0016237767, 0.0001354155),
    19: (58, 0.0173969630, 0.0014614368, 0.00235554, 0.0001965072, 0.00706662, 0.0005908010, 0.0012742750, 0.0001062517),
    20: (59, 0.0193249700, 0.0016248567, 0.00261034, 0.0002177890, 0.00783102, 0.0006549391, 0.0010000000, 0.0000833716),
    21: (60, 0.0214734650, 0.0018073127, 0.00290000, 0.0002419885, 0.00870000, 0.0007279071, 0.0080000000, 0.0006691237),
    22: (61, 0.0236169160, 0.0019897067, 0.00325949, 0.0002720308, 0.00977847, 0.0008185476, 0.0080000000, 0.0006691237),
    23: (62, 0.0257338530, 0.0021702051, 0.00366355, 0.0003058097, 0.01099065, 0.0009205338, 0.0080000000, 0.0006691237),
    24: (63, 0.0278056050, 0.0023471993, 0.00411769, 0.0003437901, 0.01235307, 0.0010352973, 0.0080000000, 0.0006691237),
    25: (64, 0.0298164800, 0.0025193236, 0.00462814, 0.0003864989, 0.01388442, 0.0011644640, 0.0080000000, 0.0006691237),
}
BASIS_COLUMNS = ("age", "ci_rate", "ci_rate_mth", "mort_rate", "mort_rate_mth",
                 "mort_rate_ci", "mort_rate_ci_mth", "lapse_rate", "lapse_rate_mth")

# The first policy year's CI decrement, month by month: the 보장개시일 at work.
CI_RATE_MTH_YEAR_ONE = {
    0: 0.0001468954,
    1: 0.0001468954,
    2: 0.0001504033,
    3: 0.0002322544,
}



# "Per-cause incidence, male, at the ages worth printing":
# attained age -> (cancer, ami, stroke, other, ltc).
WORKED_EXAMPLE_CAUSES = {
    20: (0.000144000, 0.000027000, 0.000038000, 0.000021945, 0.0),
    40: (0.001023000, 0.000589000, 0.000907000, 0.000264495, 0.0),
    50: (0.003364142, 0.001604531, 0.001904493, 0.000721682, 0.0),
    60: (0.011063000, 0.004371000, 0.003999000, 0.002040465, 0.0),
    80: (0.028353209, 0.009653117, 0.007188769, 0.004745485, 0.008565526),
    99: (0.031734378, 0.010613464, 0.007711596, 0.005256241, 0.103263346),
}
CAUSE_ORDER = ("cancer", "ami", "stroke", "other", "ltc")
CI_TABLE_SUM_40 = 0.0027834950      # the age-40 sum, which IS ci_rate(0) on this grid

# "The first-year 감액 cohorts", the anchor beside its female twin (point_id = 2).
# The counts are the first policy year's months; the cohort labels are month-ends, and
# the reduced ones are negative.  The first two months carry no 중대한 암 at all.
REDUCED_SHARE_M = 0.0018376178     # ci_reduced_share(3), the first fully covered month
REDUCED_SHARE_F = 0.1945881241     # the same month on the female twin
REDUCED_SHARE_M_MONTH_2 = 0.0001166165   # the 보장개시일 month, 4.1% of a month's cover
POLS_CI_YEAR_1_M = 0.0024029515    # sum pols_ci over the first policy year
POLS_CI_YEAR_1_F = 0.0023722599    # the female twin's
POLS_CI_IN_REDUCED_M = 0.0000036240  # sum into the reduced cohorts, first policy year
POLS_CI_IN_REDUCED_F = 0.0004217215  # the female twin's
ACCEL_COHORT_REDUCED = 40000000.0      # a f B(d) at a month-end where B = SA
RESID_COHORT_REDUCED = 60000000.0      # (1 - a f) B(d)
ACCEL_COHORT_FULL = 80000000.0         # a B(d)
RESID_COHORT_FULL = 20000000.0         # r B(d)

# "First months of the base run", per policy issued, income-positive, two decimals.
# t: (pols_if, premiums, claims_ci, claims_death, claims_death_ci, claims_lapse,
#     claims_lapse_ci, claim_expenses, expenses, commissions, net_cf)
WORKED_EXAMPLE = {
      0: (1.000000, 306740.00, 11751.63, 5667.60, 0.00, 0.00,
         0.00, 61.07, 505000.00, 2944704.00, -3160444.31),
      1: (0.991203, 303989.10, 11646.53, 5616.91, 0.50, 0.00,
         0.00, 60.53, 4956.02, 0.00, 281708.60),
      2: (0.982486, 301262.87, 11817.32, 5566.66, 1.00, 0.00,
         0.00, 61.03, 4912.43, 0.00, 278904.44),
      3: (0.973846, 298560.04, 18069.60, 5516.40, 1.50, 0.00,
         0.00, 84.39, 4869.23, 0.00, 270018.92),
      4: (0.965284, 295857.24, 17906.47, 5466.60, 2.27, 0.00,
         0.00, 83.64, 4826.42, 0.00, 267571.84),
      5: (0.956799, 293178.91, 17744.81, 5417.25, 3.03, 0.00,
         0.00, 82.90, 4783.99, 0.00, 265146.93),
      6: (0.948390, 290524.82, 17584.61, 5368.34, 3.79, 0.00,
         0.00, 82.16, 4741.95, 0.00, 262743.97),
      7: (0.940058, 287894.76, 17425.85, 5319.88, 4.54, 0.00,
         0.00, 81.43, 4700.29, 0.00, 260362.77),
      8: (0.931800, 285288.51, 17268.53, 5271.85, 5.28, 0.00,
         0.00, 80.71, 4659.00, 0.00, 258003.14),
      9: (0.923617, 282705.85, 17112.63, 5224.25, 6.02, 0.00,
         0.00, 79.99, 4618.09, 0.00, 255664.87),
     10: (0.915508, 280146.58, 16958.14, 5177.09, 6.75, 0.00,
         0.00, 79.28, 4577.54, 0.00, 253347.78),
     11: (0.907472, 277610.47, 16805.04, 5130.35, 7.47, 0.00,
         0.00, 78.58, 4537.36, 0.00, 251051.68),
     12: (0.899508, 275097.32, 18399.84, 5272.75, 8.49, 0.00,
         0.00, 84.94, 4542.51, 8252.92, 238535.87),
    228: (0.608660, 159194.63, 67848.29, 11349.16, 3744.04, 1363.74,
         1816.95, 305.51, 3676.64, 4775.84, 64314.46),
    238: (0.606214, 156116.70, 66553.12, 11132.51, 4285.20, 1408.90,
         2079.56, 301.48, 3661.86, 4683.50, 62010.56),
    239: (0.605967, 155812.20, 66424.98, 11111.08, 4341.08, 2826.89,
         2106.68, 301.08, 3660.37, 4674.37, 60365.68),
    240: (0.605719, 0.00, 73741.61, 12319.65, 4868.12, 22667.51,
         2125.48, 334.39, 3695.46, 0.00, -119752.21),
    241: (0.605154, 0.00, 73541.28, 12286.18, 4915.89, 22633.78,
         2146.33, 333.71, 3692.01, 0.00, -119549.20),
    252: (0.598961, 0.00, 78576.26, 13401.87, 6115.11, 22263.96,
         2374.06, 360.73, 3690.77, 0.00, -126782.76),
    348: (0.531791, 0.00, 95102.91, 23839.03, 30875.10, 17161.62,
         4667.32, 546.14, 3548.39, 0.00, -175740.51),
    468: (0.371825, 0.00, 65052.01, 37511.32, 123279.12, 9195.05,
         5613.40, 782.15, 2740.58, 0.00, -244173.64),
    588: (0.114484, 0.00, 26919.45, 35290.28, 155130.16, 2829.31,
         1961.05, 698.96, 932.10, 0.00, -223761.32),
    708: (0.003217, 0.00, 2941.30, 6751.46, 8788.88, 156.83,
         17.59, 57.74, 28.93, 0.00, -18742.74),
    719: (0.001913, 0.00, 1852.44, 4252.10, 3986.07, 98.67,
         7.98, 31.71, 17.20, 0.00, -10246.18),
    720: (0.001829, 0.00, 0.00, 4746.85, 5509.41, 95.63,
         6.96, 30.84, 16.62, 0.00, -10406.31),
    840: (0.000000, 0.00, 0.00, 1.07, 0.00, 0.01,
         0.00, 0.00, 0.00, 0.00, -1.08),
}
CF_COLUMNS = ("pols_if", "premiums", "claims_ci", "claims_death", "claims_death_ci",
              "claims_lapse", "claims_lapse_ci", "claim_expenses", "expenses",
              "commissions", "net_cf")

# "The values run at the same month-ends", keyed by the frame's month t.  The five
# state columns are read at the month-end that closes the month, t + 1;
# resid_db_avg_pp is on the month clock.
# t -> (pol_val_pp, surr_chg_pp, cv_std_pp, cv_pp, cv_pp_ci, resid_db_avg_pp).
WORKED_EXAMPLE_VALUES = {
      0: (236200.67, 3897743.24, 0.00, 0.00, 0.00, 0.00),
      1: (472933.85, 3850782.48, 0.00, 0.00, 0.00, 20000000.00),
      2: (709893.51, 3803821.71, 0.00, 0.00, 0.00, 20000000.00),
     11: (2802441.49, 3381174.86, 0.00, 0.00, 0.00, 20059094.14),
     12: (3035404.10, 3334214.10, 0.00, 0.00, 0.00, 20060358.33),
     14: (3502979.17, 3240292.57, 262686.60, 131343.30, 262686.60, 20050662.03),
     59: (14444029.87, 1127058.29, 13316971.59, 6658485.79, 13316971.59, 20010759.51),
     83: (20581370.16, 0.00, 20581370.16, 10290685.08, 20581370.16, 21617332.91),
     84: (20840123.32, 0.00, 20840123.32, 10420061.66, 20840123.32, 21888878.45),
    119: (30195074.67, 0.00, 30195074.67, 15097537.34, 30195074.67, 31707981.03),
    227: (62465421.89, 0.00, 62465421.89, 31232710.94, 62465421.89, 65588692.98),
    238: (66134800.56, 0.00, 66134800.56, 33067400.28, 66134800.56, 69441540.59),
    239: (66476050.15, 0.00, 66476050.15, 66476050.15, 66476050.15, 69799852.66),
    240: (66557770.20, 0.00, 66557770.20, 66557770.20, 66557770.20, 69885658.71),
    251: (67476674.44, 0.00, 67476674.44, 67476674.44, 67476674.44, 70850508.16),
    348: (74766740.78, 0.00, 74766740.78, 74766740.78, 74766740.78, 78505077.82),
    468: (82745956.16, 0.00, 82745956.16, 82745956.16, 82745956.16, 86883253.97),
    708: (94916943.77, 0.00, 94916943.77, 94916943.77, 94916943.77, 99662790.95),
    840: (98775050.80, 0.00, 98775050.80, 98775050.80, 98775050.80, 0.00),
}
VALUE_COLUMNS = ("pol_val_pp", "surr_chg_pp", "cv_std_pp", "cv_pp", "cv_pp_ci",
                 "resid_db_avg_pp")

# The 기본보험금, flat at SA and then following the account.
CUM_PREM_AT_PAID_UP = 73617600.0
BASE_BENEFIT_FIRST_ABOVE_SA = 730       # the month-end the 105% account limb takes over
BASE_BENEFIT_730 = 100027274.71
BASE_BENEFIT_840 = 103607571.76

# "The policy-loan room at the same month-ends, showing the doubling the carve-out
# produces".  Keyed by the **month-end**:
# d -> (loan_avail_pp, loan_avail_ci_pp).
LOAN_ROOM = {
     60: (5326788.64, 10653577.27),
     84: (8232548.06, 16465096.13),
    120: (12078029.87, 24156059.74),
    180: (18958250.95, 37916501.90),
    228: (24986168.76, 49972337.51),
    239: (26453920.22, 52907840.45),
    240: (53180840.12, 53180840.12),
    252: (53981339.55, 53981339.55),
}


# "Hand trace, month 1" -- t = 0.  The ``*_2`` keys are the state at the start of
# month t = 1.
TRACE_1 = {
    "ci_rate_mth": 0.0001468954155330,
    "phi": 0.0000000000000000,
    "pols_ci_in_full": 0.0001468954155330,
    "pols_ci_in_reduced": 0.0000000000000000,
    "pols_death": 0.0000566760087853,
    "pols_lapse": 0.0087398314125038,
    "pols_if_pre_2": 0.9910565971631780,
    "pols_if_ci_2": 0.0001468954155330,
    "pols_if_2": 0.9912034925787109,
    "pols_waived_2": 0.0000247798223393,
    "pols_if_pay_2": 0.9910318173408387,
}
CLAIMS_CI_1 = 11751.63
POL_VAL_1 = 236200.6664
SURR_CHG_1 = 3897743.2381
CV_FIRST_POSITIVE = 15            # the first month-end at which cv_pp is not nil

# "Hand trace, month 2" -- t = 1, the first month with a residual death claim.
TRACE_2 = {
    "pols_ci": 0.0001455816706570,
    "pols_death": 0.0000561691324076,
    "pols_death_ci": 0.0000000249956001,
    "pols_lapse": 0.0086616675794559,
    "pols_lapse_ci": 0.0000000490467908,
}
FLOOR_2 = 496580.55                  # c V(2), below both nominals
CV_2 = 0.0000000000
CV_CI_2 = 0.0000000000
RESID_DB_AVG_1 = 20000000.00            # the mean residual in month t = 1
CLAIM_EXPENSE_EVENTS_2 = 0.0002017757987

# "Hand trace, the month the 105% floor takes over" -- the crossing is at d = 79,
# so the trace is month t = 78.
FLOOR_CROSS_D = 79
TRACE_FLOOR_COUNTS = {
    "pols_if_pre": 0.6637142821915645,
    "pols_if_ci": 0.0180480553322628,
    "pols_if": 0.6817623375238273,
    "pols_waived": 0.0012931755802854,
    "pols_if_pay": 0.6624211066112791,
}
FLOOR_BEFORE = 19973041.0352267362       # c V(d - 1), below the KRW 20,000,000 nominal
FLOOR_AFTER = 20244219.6032280400        # c V(d), above it
POLS_DEATH_CI_FLOOR = 0.0000040383455043
RESID_DB_AVG_FLOOR = 20251912.3179601543
INFLATION_FLOOR = 1.0615201506010
NET_CF_FLOOR = 153361.90

# "Hand trace, month 240" -- the first premium-free month.
TRACE_PAID_UP = {
    "pols_if_pre": 0.5100224688890150,
    "pols_if_ci": 0.0956967694066161,
    "pols_if": 0.6057192382956311,
    "pols_ci": 0.0009217700918919,
    "pols_death": 0.0001231965034270,
    "pols_death_ci": 0.0000696583587527,
    "pols_lapse": 0.0003405688984958,
    "pols_lapse_ci": 0.0000319342922532,
}
FLOOR_PAID_UP = 69885658.71
INFLATION_PAID_UP = 1.2201900399480
CLAIM_EXPENSE_EVENTS_PAID_UP = 0.0011146249541
PAID_UP_SWING = 180117.89          # net_cf(239) - net_cf(240)

# "Roll-forward and undiscounted totals": the four exits and the transition beside them.
SUM_DEATH = 0.1400281094
SUM_DEATH_CI = 0.4045046008
SUM_LAPSE = 0.4326271583
SUM_LAPSE_CI = 0.0228401315
SUM_CI = 0.4273447323
POLICY_MONTHS = 315.7478320763          # sum pols_if, in MONTHS
POLICY_MONTHS_PRE = 246.9486445020
POLICY_MONTHS_CI = 68.7991875744
POLICY_MONTHS_PAY = 155.0451674103
POST_CI_PEAK_T = 420
POST_CI_PEAK = 0.2178167855

TOTALS = {
    "premiums": 47558554.65,
    "claims_ci": 34187433.63,
    "claims_death": 14003973.11,
    "claims_death_ci": 36093568.46,
    "claims_lapse": 6186437.80,
    "claims_lapse_ci": 1713420.66,
    "claim_expenses": 291563.23,
    "expenses": 2441629.84,
    "commissions": 4266347.86,
    "net_cf": -51625819.94,
}
PHASE_PAYING = 30170319.26           # sum net_cf, t = 0 ... 239
PHASE_RUN_OFF = -81796139.20         # sum net_cf, t = 240 ... 851


# "Reading the shape of the result" and "Key sensitivities".
TOTAL_BENEFITS = 92184833.65
CI_ORIGINATED = 70281002.09
CI_ORIGINATED_SHARE = 0.7624
DEATH_SHARE = 0.1519
RESID_ON_NOMINAL = 8090217.24        # the residual stream with the floor removed
FLOOR_WORTH = 4.46                     # claims_death_ci / RESID_ON_NOMINAL
CLAIMS_AFTER_CI_COVER_TAIL = 183916.56  # all claims from t = 720, after CI cover ends
DEATH_CI_AFTER_YEAR_40 = 0.6902       # share of claims_death_ci from t = 480
BENEFITS_AFTER_YEAR_40 = 0.4229       # share of all benefits from t = 480
INFLATION_TOTAL = 2.01                 # 1.01 ** 70
CARVE_OUT_WORTH = 64704.62           # paid less the suppressed counterfactual
SUPPRESSED_LAPSE_CI = 1648716.04
SPURIOUS_PREMIUM_MONTHS = 8.730436      # post-CI person-months inside the 납입기간
SPURIOUS_PREMIUM_WON = 2677973.86
SPURIOUS_PREMIUM_MONTHS_ALL = 9.150272  # post-CI plus the 장해 50%+ waived subset
SPURIOUS_PREMIUM_WON_ALL = 2806754.28
CLAIM_EXPENSE_UNDERSTATEMENT = 0.44    # charging on deaths alone
POST_CI_SHARE_OF_INFORCE_T = 552
POST_CI_SHARE_OF_INFORCE = 0.601
POST_CI_SHARE_OF_PERSON_MONTHS = 0.218
A0_1_NO_ACCEL = 36649058.63          # epv_ben(0) with a = 0, r = 1
P_NET_NO_ACCEL_MTH = 205075.25         # and its monthly net premium
ACCELERATION_COST = 0.23984            # P^m / P^m(a = 0) - 1
ANNUITY_DUE_ORDINARY = 187.9209941962      # the annuity without the CI decrement
P_NET_ORDINARY_MTH = 241798.85          # and the premium it would give


# Sensitivities the notes quantify, as undiscounted sum net_cf on the anchor cell.
SENS_NO_WAIT = -51651624.44          # ci_wait_days = 0
SENS_NO_FIRST_YEAR_CUT = -51625960.22  # first_year_factor = 1.00
SENS_FULL_POST_CI_LAPSE = -51275060.15  # lapse_ci_factor = 1.00
SENS_LEVEL_4_PCT_LAPSE = -34030199.11   # a level 4% paying-period rate

CHECK_CELLS = {
    "check_pols_roll_fwd",
    "check_ci_state_roll_fwd",
    "check_decrement_sum",
    "check_pol_val_roll_fwd",
    "check_accel_complement",
    "check_resid_floor",
    "check_cv_carve_out",
    "check_loan_roll_fwd",
    "check_net_cf",
}


# ---------------------------------------------------------------------------
# The worked example


def test_the_anchor_cell_is_the_one_the_notes_describe(kr_ci_anchor):
    """남자 40 / 1억원 / 종신 / 20년납 / 80% 선지급 / 저해지 k = 0.50, at KRW 3,680,880.

    Every golden number below is conditional on the model point, so it is asserted first
    and in full.  A row silently edited in ``model_point_table.csv`` would otherwise move
    the whole of this module's expected values at once and read as a model failure.
    """
    a = kr_ci_anchor
    assert a.model_point()["policy_id"] == "CI-KR-0001"
    assert a.sex() == "M"
    assert a.age_at_entry() == 40
    assert a.sum_assured() == 100000000.0
    assert a.prem_term() == PREM_PERIOD
    assert a.premium_pp() == G_GROSS
    assert a.premium_pp() / 12 == 306740.0        # the published monthly figure [S4]
    assert a.pols_if_init() == 1.0
    assert a.accel_rate() == ACCEL_RATE
    assert a.resid_rate() == pytest.approx(0.20, abs=1e-15)
    assert a.cv_floor_ratio() == 0.50
    assert a.resid_floor_mult() == 1.05
    assert a.first_year_scope() == "breast"
    assert a.lapse_basis() == "log_linear"
    assert a.waiver_rate(0) == 0.0003
    assert a.pol_loan_util() == 0.0 and a.pol_loan_year() == 0
    assert a.mort_be_factor() == 1.0 and a.ci_be_factor() == 1.0
    assert a.mort_ci_factor() == 3.0


def test_worked_example_derived_scalars(kr_ci_anchor):
    """The notes' table of derived scalars, at the precision it prints them.

    These are the quantities every later number rests on — the horizon, the two
    boundaries, the three EPVs and the two premiums — so they are asserted once, here,
    rather than being inferred from a cash flow that happens to agree.
    """
    a = kr_ci_anchor
    assert a.omega_age() == OMEGA
    assert a.proj_years() == PROJ_YEARS == OMEGA - 40 + 1
    assert a.proj_len() == PROJ_LEN == 12 * PROJ_YEARS
    assert a.ci_cover_end() == CI_COVER_END == 12 * (100 - 40)
    assert a.prem_period() == a.prem_end() == PREM_PERIOD
    assert a.prem_period_mths() == PREM_PERIOD_MTHS == 12 * PREM_PERIOD
    assert a.surr_chg_period_mths() == SURR_CHG_PERIOD_MTHS == 12 * SURR_CHG_YEARS
    # proj_len() is the number of projected months: the last index is proj_len() - 1.
    assert list(a.result_cf().index)[-1] == a.proj_len() - 1
    assert a.disc_factor() == pytest.approx(DISC_FACTOR, abs=5e-16)
    assert a.disc_factor_mth() == pytest.approx(DISC_FACTOR_MTH, abs=5e-16)
    assert (1.0 + a.prem_int_rate_mth()) ** 12 == pytest.approx(1.025, rel=1e-14)
    assert (1.0 + a.i_loan_mth()) ** 12 == pytest.approx(1.04, rel=1e-14)
    assert a.epv_ben(0) == pytest.approx(A0_1, abs=WON)
    assert a.epv_resid(0) == pytest.approx(A1_1, abs=WON)
    assert a.annuity_due(0) == pytest.approx(ANNUITY_DUE_1, abs=5e-9)
    assert a.prem_net_level_mth_pp() == pytest.approx(P_NET_MTH, abs=WON)
    assert a.prem_net_level_pp() == pytest.approx(P_NET, abs=WON)
    assert a.prem_net_level_pp() == pytest.approx(
        12.0 * a.prem_net_level_mth_pp(), rel=1e-14)
    assert a.premium_pp() == G_GROSS
    assert a.premium_mth_pp() == G_GROSS_MTH == 306740.0
    assert a.premium_pp() / a.prem_net_level_pp() == pytest.approx(LOADING, abs=5e-11)
    assert a.surr_chg_cap_pp() == pytest.approx(SC_CAP, abs=WON)
    assert a.breast_share() == BREAST_SHARE_M
    assert a.ci_wait_factor() == pytest.approx(CI_WAIT_FACTOR, abs=5e-16)
    assert a.lapse_rate_ult() == LAPSE_ULT
    # A0(0) is 0.454391 of the sum assured, the figure the notes quote beside it.
    assert a.epv_ben(0) / a.sum_assured() == pytest.approx(0.454391, abs=5e-7)
    # The monthly equivalence is 2.78% above the annual-step model's own net premium,
    # which is the ordinary modal effect of paying monthly in advance.
    assert a.prem_net_level_pp() / P_NET_ANNUAL_STEP == pytest.approx(
        MODAL_EFFECT, abs=5e-9)


def test_the_equivalence_principle_is_asserted_rather_than_assumed(kr_ci_anchor):
    """P x a-double-dot(0) reproduces A0(0) to the won.

    The net premium is *solved* from the two EPVs, so this is not a tautology about the
    division: it is the statement that the annuity and the benefit EPV are computed on
    the same decrements and the same discount factor.  A CI decrement present in one and
    absent from the other passes every cash flow test in this module and fails here.
    """
    a = kr_ci_anchor
    assert a.prem_net_level_mth_pp() * a.annuity_due(0) == pytest.approx(A0_1, abs=WON)
    assert a.prem_net_level_mth_pp() == pytest.approx(
        a.epv_ben(0) / a.annuity_due(0), rel=1e-14)
    # The annuity is in MONTHS of premium, so the premium it solves for is a monthly one.
    assert a.annuity_due(0) > 12.0 * PREM_PERIOD * 0.5


def test_the_standard_surrender_charge_cap_is_the_byeolpyo_14_arithmetic(kr_ci_anchor):
    """SC* = 0.80 G x 5% x 20 + 1% SA = KRW 2,944,704 + 1,000,000, in one line.

    The 표준해약공제액 is the statutory ceiling on what a surrender may be made to repay
    [REG-R20], and this model reproduces it from published quantities alone — the gross
    premium and the sum assured — rather than from its own pricing basis.  The notes'
    cross-check against the FSC's 13-times-monthly rule of thumb is asserted to the 1.1%
    they state, because an agreement quoted and not tested is an agreement that drifts.
    """
    a = kr_ci_anchor
    assert a.surr_chg_cap_pp() == pytest.approx(
        0.80 * G_GROSS * 0.05 * 20 + 0.01 * a.sum_assured(), rel=1e-14)
    assert 0.80 * G_GROSS * 0.05 * 20 == pytest.approx(2944704.0, abs=WON)
    assert 0.01 * a.sum_assured() == 1000000.0
    assert SC_CAP_RULE_OF_THUMB == pytest.approx(13 * 306740.0, abs=WON)
    gap = abs(a.surr_chg_cap_pp() / SC_CAP_RULE_OF_THUMB - 1.0)
    assert gap == pytest.approx(0.011, abs=5e-4)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(kr_ci_anchor, t):
    """Every cell of the notes' 23-row cash flow table, to the displayed precision.

    The five ``claims_*`` columns are asserted separately rather than as a total, which
    is the point of publishing them separately: ``claims_ci`` and ``claims_death_ci`` are
    two payments arising from **one** decrement at two different dates, and on this form
    the second is the larger of the two over the life of the contract.
    """
    a = kr_ci_anchor
    expected = dict(zip(CF_COLUMNS, WORKED_EXAMPLE[t]))
    assert a.pols_if(t) == pytest.approx(expected["pols_if"], abs=INFORCE)
    assert a.premiums(t) == pytest.approx(expected["premiums"], abs=WON)
    assert a.claims(t, "CI") == pytest.approx(expected["claims_ci"], abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(expected["claims_death"], abs=WON)
    assert a.claims(t, "DEATH_CI") == pytest.approx(
        expected["claims_death_ci"], abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(expected["claims_lapse"], abs=WON)
    assert a.claims(t, "LAPSE_CI") == pytest.approx(
        expected["claims_lapse_ci"], abs=WON)
    assert a.claim_expenses(t) == pytest.approx(expected["claim_expenses"], abs=WON)
    assert a.expenses(t) == pytest.approx(expected["expenses"], abs=WON)
    assert a.commissions(t) == pytest.approx(expected["commissions"], abs=WON)
    assert a.net_cf(t) == pytest.approx(expected["net_cf"], abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_BASIS))
def test_worked_example_decrement_basis_row(kr_ci_anchor, t):
    """The notes' basis table, policy years 1 to 25: the attained age and the rates.

    The whole product is a race between the CI decrement and the death decrement, and
    the notes print both beside the post-CI rate and the surrender rate so a reader can
    see the race.  ``mort_rate`` at attained 40 and 60 must return [S3]'s own disclosed
    anchors, 0.00068 and 0.00290, with nothing applied to them.

    The table is read at the **last month of each policy year**, which is where the
    annual rates the sources tabulate and their monthly conversions can be compared
    without the 90-day 보장개시일 of the first three months interfering.
    """
    a = kr_ci_anchor
    (attained, ci, ci_m, mort, mort_m, mort_ci, mort_ci_m,
     lapse, lapse_m) = WORKED_EXAMPLE_BASIS[t]
    u = 12 * (t - 1) + 11               # the last month of policy year t
    assert a.policy_year(u) == t
    assert a.age(u) == attained == 40 + t - 1
    assert a.ci_rate(u) == pytest.approx(ci, abs=RATE)
    assert a.mort_rate(u) == pytest.approx(mort, abs=MORT)
    assert a.mort_rate_ci(u) == pytest.approx(mort_ci, abs=MORT)
    assert a.lapse_rate(u) == pytest.approx(lapse, abs=RATE)
    # The monthly companions, and the statement that twelve of each compound back to the
    # annual rate the sources tabulate.  This is the conversion, in one line per rate.
    assert a.ci_rate_mth(u) == pytest.approx(ci_m, abs=RATE)
    assert a.mort_rate_mth(u) == pytest.approx(mort_m, abs=RATE)
    assert a.mort_rate_ci_mth(u) == pytest.approx(mort_ci_m, abs=RATE)
    assert a.lapse_rate_mth(u) == pytest.approx(lapse_m, abs=RATE)
    for annual, monthly in ((a.ci_rate(u), a.ci_rate_mth(u)),
                            (a.mort_rate(u), a.mort_rate_mth(u)),
                            (a.mort_rate_ci(u), a.mort_rate_ci_mth(u)),
                            (a.lapse_rate(u), a.lapse_rate_mth(u))):
        assert 1.0 - (1.0 - monthly) ** 12 == pytest.approx(annual, rel=1e-12)
        # Dividing by twelve is a different number, and on the first year's lapse rate
        # it is 4.9% different.
        assert monthly >= annual / 12.0
    # q' is exactly three times q on the ANNUAL rate, which is what the 3.00 means.
    assert a.mort_rate_ci(u) == pytest.approx(3.0 * a.mort_rate(u), rel=1e-14)
    assert a.mort_rate_ci_mth(u) > 3.0 * a.mort_rate_mth(u)


def test_the_two_sourced_mortality_anchors_are_returned_unmodified(kr_ci_anchor):
    """q(40) = 0.00068 and q(60) = 0.00290 are read, not fitted.

    The table is a Makeham construction everywhere else, so these two rows and q(20) are
    the only mortality in this model that rests on a document.  ``mort_be_factor`` is a
    lever on the decrement and not a change to the 산출방법서 basis, so at 1.00 the
    projection rate and the pricing rate must coincide exactly.
    """
    a = kr_ci_anchor
    assert a.mort_rate_at_age(20) == 0.00051
    assert a.mort_rate_at_age(40) == 0.00068
    assert a.mort_rate_at_age(60) == 0.00290
    assert a.mort_rate(0) == a.mort_rate_base(0) == a.mort_rate_at_age(40)
    assert a.mort_rate(240) == a.mort_rate_base(240) == a.mort_rate_at_age(60)


@pytest.mark.parametrize("attained", sorted(WORKED_EXAMPLE_CAUSES))
def test_worked_example_per_cause_incidence(kr_ci_anchor, attained):
    """The notes' five-cause grid, male, at the ages worth printing.

    The three headline causes at 20, 40 and 60 are [S3]'s disclosed 예정위험률 and are
    the only published Korean CI morbidity anywhere in this library; ``other`` and
    ``ltc`` are constructions.  The last row carries the warning the notes attach to it:
    at attained 99 the 장기요양 limb is two thirds of the whole rate and rests on nothing
    published, so it is asserted as a number rather than trusted as a basis.
    """
    a = kr_ci_anchor
    expected = WORKED_EXAMPLE_CAUSES[attained]
    for cause, value in zip(CAUSE_ORDER, expected):
        assert a.ci_rate_at_age(attained, cause) == pytest.approx(value, abs=CAUSE), cause
    total = sum(a.ci_rate_at_age(attained, c) for c in CAUSE_ORDER)
    assert total == pytest.approx(sum(expected), abs=CAUSE)
    if attained == 99:
        ltc = a.ci_rate_at_age(99, "ltc")
        assert ltc / total > 0.65
    if attained <= 60:
        assert a.ci_rate_at_age(attained, "ltc") == 0.0


def test_the_ninety_day_waiting_period_is_a_date_and_not_a_proration(kr_ci_anchor):
    """No 중대한 암 cover for two months, a twenty-fifth of the third, all of it after.

    This is the conversion's clearest gain on this product.  The 보장개시일 is 「계약일
    부터 그 날을 포함하여 90일이 지난날의 다음날」 [S1 제7조] [S1 별표1 주1] — a **date** —
    and an annual grid could only smear it across the whole first policy year as a
    0.7534 proration on the assumption that incidence is uniform within it.  The monthly
    grid puts the cover where the contract puts it.

    Only the ``cancer`` and ``ltc`` limbs carry the wait; the other seven 중대한 질병, the
    four 중대한 수술 and 중대한 화상 및 부식 are covered from the 계약일 [S1]
    [S2 별표1 주1].  A model applying the wait to the whole first-year rate cuts the other
    three limbs' cover for ninety days the contract does not cut.

    The twelve monthly factors sum to exactly twelve times the annual one, so the
    conversion **moves** the wait without resizing the first policy year's exposure.
    """
    a = kr_ci_anchor
    table_sum = sum(a.ci_rate_at_age(40, c) for c in CAUSE_ORDER)
    assert table_sum == pytest.approx(CI_TABLE_SUM_40, abs=CAUSE)
    # The ANNUAL rate is now the table sum itself: the wait belongs to the month.
    assert a.ci_rate(0) == pytest.approx(table_sum, abs=1e-15)
    assert a.ci_rate(0) == pytest.approx(a.ci_rate(11), rel=1e-14)

    for t, factor in CI_WAIT_FACTOR_MTH.items():
        assert a.ci_wait_factor_mth(t) == pytest.approx(factor, abs=5e-11)
    assert a.ci_wait_factor_mth(0) == a.ci_wait_factor_mth(1) == 0.0
    assert all(a.ci_wait_factor_mth(t) == 1.0 for t in (3, 11, 100))
    assert sum(a.ci_wait_factor_mth(t) for t in range(12)) == pytest.approx(
        CI_WAIT_MONTHS_YEAR_ONE, abs=5e-10)
    assert CI_WAIT_MONTHS_YEAR_ONE == pytest.approx(12.0 * CI_WAIT_FACTOR, abs=5e-10)

    # The decrement in the first two months is the table sum net of the two waiting
    # limbs, converted; from the fourth month it is the whole of it, converted.
    share = a.ci_wait_share(0)
    assert share == pytest.approx(CI_WAIT_SHARE_40, abs=5e-10)
    assert share == pytest.approx(
        (a.ci_rate_at_age(40, "cancer") + a.ci_rate_at_age(40, "ltc")) / table_sum,
        rel=1e-14)
    full = 1.0 - (1.0 - table_sum) ** (1.0 / 12.0)
    assert a.ci_rate_mth(0) == pytest.approx(full * (1.0 - share), rel=1e-14)
    assert a.ci_rate_mth(3) == pytest.approx(full, rel=1e-14)
    for t, rate in CI_RATE_MTH_YEAR_ONE.items():
        assert a.ci_rate_mth(t) == pytest.approx(rate, abs=RATE)
    assert a.ci_rate_mth(0) < a.ci_rate_mth(2) < a.ci_rate_mth(3)


def test_the_ci_decrement_dominates_the_mortality_decrement(kr_ci_anchor):
    """3.72 times the death rate in policy year 1 and 7.40 times it at attained 60.

    The notes call this the reason a projection of this product is a morbidity
    projection with a mortality tail rather than the reverse, and it is the arithmetic
    behind the processing order: routing an acceleration into the death decrement moves a
    claim to a rate several times smaller.
    """
    a = kr_ci_anchor
    assert a.ci_rate(0) / a.mort_rate(0) == pytest.approx(4.09, abs=5e-3)
    assert a.ci_rate(240) / a.mort_rate(240) == pytest.approx(7.40, abs=5e-3)
    # And the same race on the monthly decrements the roll-forward actually applies.
    assert a.ci_rate_mth(11) / a.mort_rate_mth(11) == pytest.approx(4.10, abs=5e-3)


def test_the_first_year_reduced_cohorts_on_both_sexes(ci_insurance, kr_ci_anchor):
    """The notes' 감액 table: a rounding error on the male cell, 19.5% on the female.

    The negative labels are the first-year breast-cancer cohorts, paid ``a f B(d)`` and
    leaving a residual of ``(1 - a f) B(d)``.  On the anchor a reduced claim is 0.18% of
    a month's accelerations and on the female twin it is 19.5% — which is the whole
    reason the female twin is in the shipped table, and the reason a model tested only on
    the anchor will not notice a bug in the cohort machinery.

    **The monthly grid turns one reduced cohort into twelve, and empties the first two.**
    No 중대한 암 is covered before the 보장개시일, so the reduced share is zero in months
    0 and 1 and a twenty-fifth of its level in month 2 — a fact the annual grid could not
    represent at all, having only one first-year cohort to put the whole of it in.
    """
    male, female = kr_ci_anchor, ci_insurance.Projection[2]
    assert male.ci_reduced_share(3) == pytest.approx(REDUCED_SHARE_M, abs=RATE)
    assert female.ci_reduced_share(3) == pytest.approx(REDUCED_SHARE_F, abs=RATE)
    assert male.ci_reduced_share(0) == male.ci_reduced_share(1) == 0.0
    assert female.ci_reduced_share(0) == female.ci_reduced_share(1) == 0.0
    assert male.ci_reduced_share(2) == pytest.approx(
        REDUCED_SHARE_M_MONTH_2, abs=RATE)
    assert sum(male.pols_ci(t) for t in range(12)) == pytest.approx(
        POLS_CI_YEAR_1_M, abs=RATE)
    assert sum(female.pols_ci(t) for t in range(12)) == pytest.approx(
        POLS_CI_YEAR_1_F, abs=RATE)
    assert sum(male.pols_ci_in(t, -(t + 1)) for t in range(12)) == pytest.approx(
        POLS_CI_IN_REDUCED_M, abs=RATE)
    assert sum(female.pols_ci_in(t, -(t + 1)) for t in range(12)) == pytest.approx(
        POLS_CI_IN_REDUCED_F, abs=RATE)
    for p in (male, female):
        for d in (3, 7, 12):
            assert p.accel_benefit_pp(-d) == ACCEL_COHORT_REDUCED
            assert p.resid_nominal_pp(-d) == RESID_COHORT_REDUCED
            assert p.accel_benefit_pp(d) == ACCEL_COHORT_FULL
            assert p.resid_nominal_pp(d) == pytest.approx(
                RESID_COHORT_FULL, abs=1e-6)
        # The share is a share of that month's own decrement and nil past the first
        # policy year, the 감액 running for a policy year and not for a projection step.
        assert all(p.ci_reduced_share(t) == 0.0 for t in (12, 13, 60, 240, 700))
    # The share is the breast-cancer part of the covered cancer limb, not of the whole.
    total = sum(male.ci_rate_at_age(40, c) for c in CAUSE_ORDER)
    full = 1.0 - (1.0 - total) ** (1.0 / 12.0)
    assert male.ci_reduced_share(3) == pytest.approx(
        0.005 * full * male.ci_rate_at_age(40, "cancer") / total / male.ci_rate_mth(3),
        rel=1e-14)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_VALUES))
def test_worked_example_values_row(kr_ci_anchor, t):
    """The notes' values run: the account, the charge, and the three surrender values.

    ``cv_std_pp`` is the 표준형 twin's value, ``cv_pp`` what a pre-CI policyholder is
    actually paid and ``cv_pp_ci`` what a post-CI one is — three quantities that coincide
    only after 납입완료, and whose separation is the CI-specific delta on the chassis.

    The row is keyed by the month ``t``; the five state columns are read on the month-end
    clock at ``t + 1``, the month-end that closes the month and at which a surrender
    arising in it is paid.
    """
    a = kr_ci_anchor
    expected = dict(zip(VALUE_COLUMNS, WORKED_EXAMPLE_VALUES[t]))
    assert a.pol_val_pp(t + 1) == pytest.approx(expected["pol_val_pp"], abs=WON)
    assert a.surr_chg_pp(t + 1) == pytest.approx(expected["surr_chg_pp"], abs=WON)
    assert a.cv_std_pp(t + 1) == pytest.approx(expected["cv_std_pp"], abs=WON)
    assert a.cv_pp(t + 1) == pytest.approx(expected["cv_pp"], abs=WON)
    assert a.cv_pp_ci(t + 1) == pytest.approx(expected["cv_pp_ci"], abs=WON)
    assert a.resid_db_avg_pp(t) == pytest.approx(expected["resid_db_avg_pp"], abs=WON)


def test_the_published_frames_carry_the_same_numbers_as_the_cells(kr_ci_anchor):
    """``result_cf()`` and ``result_val()`` reproduce the two tables the notes print.

    The cells and the frames are two routes to the same numbers and either could drift
    from the other — a column built from the wrong cells, or a row index off by one —
    without any single-cell assertion above noticing.
    """
    cf, val = kr_ci_anchor.result_cf(), kr_ci_anchor.result_val()
    for t, expected in WORKED_EXAMPLE.items():
        for column, value in zip(CF_COLUMNS, expected):
            tol = INFORCE if column == "pols_if" else WON
            assert cf.loc[t, column] == pytest.approx(value, abs=tol), (t, column)
    for t, expected in WORKED_EXAMPLE_VALUES.items():
        for column, value in zip(VALUE_COLUMNS, expected):
            assert val.loc[t, column] == pytest.approx(value, abs=WON), (t, column)


def test_the_average_residual_starts_above_the_nominal_and_then_leaves_it(kr_ci_anchor):
    """Exactly the nominal in month 1, then the reduced cohorts, then the 105% floor.

    Three effects move the in-force mean residual and they must not be confused, and the
    monthly grid separates all three where the annual grid could only show the last two.
    In months 0 and 1 there is **no** reduced cohort at all, the 보장개시일 not having
    passed, so the mean is exactly the KRW 20,000,000 nominal.  From month 2 the reduced
    cohorts' KRW 60,000,000 enters the average and decays as the full cohorts accumulate.
    From the month-end ``FLOOR_CROSS_D`` it is the 105% account floor, and the decay
    reverses for good.
    """
    a = kr_ci_anchor
    assert a.resid_db_avg_pp(1) == pytest.approx(20000000.0, abs=WON)
    assert a.resid_db_avg_pp(12) > a.resid_db_avg_pp(1)         # the reduced cohorts
    assert a.resid_db_avg_pp(12) == pytest.approx(20060358.33, abs=WON)
    assert a.resid_db_avg_pp(60) < a.resid_db_avg_pp(12)        # and their decay
    assert a.resid_db_avg_pp(60) == pytest.approx(20010564.39, abs=WON)
    assert a.resid_db_avg_pp(FLOOR_CROSS_D) > a.resid_db_avg_pp(FLOOR_CROSS_D - 1)
    for t in range(FLOOR_CROSS_D, 480):
        assert a.resid_db_avg_pp(t) >= a.resid_db_avg_pp(t - 1)
    assert a.resid_db_avg_pp(468) / 20000000.0 == pytest.approx(4.344, abs=5e-4)


def test_the_base_benefit_is_flat_and_then_follows_the_account(kr_ci_anchor):
    """B(d) = SA to month-end 729 and c V(d) from 730; cumulative premiums never bind.

    The 기본보험금 is a maximum of three limbs and the notes say plainly that only one of
    them binds on this cell, and only at the very end of a 71-year projection.  Asserting
    the crossing **month** pins the statement where the annual grid could only pin the
    year: a model whose ``cum_prem_pp`` limb bound early would be paying a different
    benefit, and one whose ``c V`` limb never bound would have the definition of the
    기본보험금 wrong at the top of the table.
    """
    a = kr_ci_anchor
    assert a.cum_prem_pp(PREM_PERIOD_MTHS) == CUM_PREM_AT_PAID_UP
    assert a.cum_prem_pp(700) == CUM_PREM_AT_PAID_UP    # capped at 12m, not at d
    assert a.cum_prem_pp(PREM_PERIOD_MTHS) == pytest.approx(
        PREM_PERIOD_MTHS * G_GROSS_MTH, rel=1e-14)
    assert CUM_PREM_AT_PAID_UP < a.sum_assured()
    for d in (1, 12, 240, 480, BASE_BENEFIT_FIRST_ABOVE_SA - 1):
        assert a.base_benefit_pp(d) == a.sum_assured()
        assert a.accel_benefit_pp(d) == pytest.approx(80000000.0, abs=1e-6)
        assert a.resid_nominal_pp(d) == pytest.approx(20000000.0, abs=1e-6)
    d0 = BASE_BENEFIT_FIRST_ABOVE_SA
    assert a.base_benefit_pp(d0) == pytest.approx(BASE_BENEFIT_730, abs=WON)
    assert a.base_benefit_pp(d0) == pytest.approx(1.05 * a.pol_val_pp(d0), rel=1e-14)
    assert a.base_benefit_pp(840) == pytest.approx(BASE_BENEFIT_840, abs=WON)
    # V(T) is zero by construction, so the final month falls back to the face amount.
    assert a.pol_val_pp(PROJ_LEN) == 0.0
    assert a.base_benefit_pp(PROJ_LEN) == a.sum_assured()


@pytest.mark.parametrize("d", sorted(LOAN_ROOM))
def test_the_policy_loan_room_doubles_at_the_acceleration_date(kr_ci_anchor, d):
    """The notes' loan-room table: a ratio of exactly 2.00 inside the 납입기간.

    The 보험계약대출 limit is 80% of the *payable* value [REG-R25 제33조], and the payable
    value for a post-CI policy is the unsuppressed one at every duration.  So a diagnosis
    doubles the borrowing room with no other change to the contract — a consequence of
    the carve-out that is invisible unless both limits are published.  The table is keyed
    by the **month-end**, including the two either side of 납입완료, where the monthly
    grid shows the step as the single-row event it is.
    """
    a = kr_ci_anchor
    pre, post = LOAN_ROOM[d]
    assert a.loan_avail_pp(d) == pytest.approx(pre, abs=WON)
    assert a.loan_avail_ci_pp(d) == pytest.approx(post, abs=WON)
    expected_ratio = 1.0 if d >= a.prem_period_mths() else 2.0
    assert a.loan_avail_ci_pp(d) / a.loan_avail_pp(d) == pytest.approx(
        expected_ratio, rel=1e-14)
    assert a.loan_avail_pp(d) == pytest.approx(0.8 * a.cv_pp(d), rel=1e-14)
    assert a.loan_avail_ci_pp(d) == pytest.approx(0.8 * a.cv_pp_ci(d), rel=1e-14)


def test_worked_example_month_one_trace(kr_ci_anchor):
    """The notes' first-month trace, line by line: t = 0.

    One month's premium on the whole cohort; the acquisition expense and the 80% initial
    commission, computed on the **annual** premium because that is the unit a Korean
    commission scale is written in; the CI transition, which in this month carries **no**
    reduced cohort at all because the 보장개시일 has not passed; deaths among those who
    did not accelerate; surrenders paid nothing because CV(1) is zero, the account
    standing far below the 해약공제액; and the claim expense on two kinds of event.

    The first month is where the monthly grid states the acquisition strain properly: the
    whole of the first year's commission and expense falls against **one** instalment of
    premium, so ``net_cf(0)`` is ten times the month's income and negative.
    """
    a = kr_ci_anchor
    assert a.pols_if_pre(0) == 1.0 and a.pols_if_ci(0) == 0.0
    assert a.pols_if(0) == 1.0 and a.pols_waived(0) == 0.0 and a.pols_if_pay(0) == 1.0
    assert a.premiums(0) == pytest.approx(G_GROSS_MTH, abs=WON)
    assert a.expenses(0) == pytest.approx(500000.0 + 5000.0, abs=WON)
    assert a.inflation_factor(0) == 1.0
    assert a.commissions(0) == pytest.approx(0.80 * G_GROSS, abs=WON)
    assert a.net_cf(0) < -10.0 * a.premiums(0)

    assert a.ci_rate_mth(0) == pytest.approx(TRACE_1["ci_rate_mth"], abs=TRACE)
    assert a.ci_reduced_share(0) == pytest.approx(TRACE_1["phi"], abs=TRACE)
    assert a.pols_ci_in(0, -1) == pytest.approx(
        TRACE_1["pols_ci_in_reduced"], abs=TRACE)
    assert a.pols_ci_in(0, 1) == pytest.approx(TRACE_1["pols_ci_in_full"], abs=TRACE)
    assert a.pols_ci_in(0, -1) + a.pols_ci_in(0, 1) == pytest.approx(
        a.pols_ci(0), rel=1e-14)
    assert a.pols_ci_in(0, -1) == 0.0            # no 중대한 암 cover in month 0
    assert a.claims(0, "CI") == pytest.approx(CLAIMS_CI_1, abs=WON)
    assert a.claims(0, "CI") == pytest.approx(
        a.pols_ci_in(0, 1) * ACCEL_COHORT_FULL, abs=WON)

    assert a.pols_death(0) == pytest.approx(TRACE_1["pols_death"], abs=TRACE)
    assert a.pols_death(0) == pytest.approx(
        1.0 * (1 - a.ci_rate_mth(0)) * a.mort_rate_mth(0), rel=1e-14)
    assert a.claims(0, "DEATH") == pytest.approx(
        1e8 * TRACE_1["pols_death"], abs=WON)

    assert a.lapse_rate(0) == 0.10               # the annual rate the guideline states
    assert a.lapse_rate_mth(0) == pytest.approx(
        1.0 - 0.9 ** (1.0 / 12.0), rel=1e-14)
    assert a.pols_lapse(0) == pytest.approx(TRACE_1["pols_lapse"], abs=TRACE)
    # The first month's surrenders fall at its close, month-end 1.
    assert a.pol_val_pp(1) == pytest.approx(POL_VAL_1, abs=WON)
    assert a.surr_chg_pp(1) == pytest.approx(SURR_CHG_1, abs=WON)
    assert a.pol_val_pp(1) < a.surr_chg_pp(1)
    assert a.cv_std_pp(1) == 0.0 and a.cv_pp(1) == 0.0
    assert a.claims(0, "LAPSE") == 0.0
    assert a.claims(0, "LAPSE_CI") == 0.0
    assert a.claims(0, "DEATH_CI") == 0.0        # no post-CI cohort exists yet
    # The payable value stays nil for fifteen months, a date an annual grid could only
    # place inside a policy year.
    assert a.cv_pp(CV_FIRST_POSITIVE - 1) == 0.0
    assert a.cv_pp(CV_FIRST_POSITIVE) > 0.0

    assert a.claim_expenses(0) == pytest.approx(
        300000.0 * (a.pols_ci(0) + a.pols_death(0)), rel=1e-14)
    assert a.net_cf(0) == pytest.approx(WORKED_EXAMPLE[0][-1], abs=WON)

    assert a.pols_if_pre(1) == pytest.approx(TRACE_1["pols_if_pre_2"], abs=TRACE)
    assert a.pols_if_ci(1) == pytest.approx(TRACE_1["pols_if_ci_2"], abs=TRACE)
    assert a.pols_if(1) == pytest.approx(TRACE_1["pols_if_2"], abs=TRACE)
    assert a.pols_waived(1) == pytest.approx(TRACE_1["pols_waived_2"], abs=TRACE)
    assert a.pols_if_pay(1) == pytest.approx(TRACE_1["pols_if_pay_2"], abs=TRACE)


def test_worked_example_month_two_trace(kr_ci_anchor):
    """The notes' second-month trace, t = 1 — the first month with a residual claim.

    One post-CI cohort exists and there is still no reduced one, the 보장개시일 not
    having passed, so the in-force mean residual is **exactly** the KRW 20,000,000
    nominal — a reading the annual grid could not produce, its single first-year cohort
    carrying the reduced claims of the whole year.  Both surrender lines are nil, the
    payable value being zero for fifteen months.
    """
    a = kr_ci_anchor
    assert a.premiums(1) == pytest.approx(G_GROSS_MTH * a.pols_if_pay(1), rel=1e-14)
    assert a.expenses(1) == pytest.approx(5000.0 * a.pols_if(1), abs=WON)
    assert a.inflation_factor(1) == 1.0          # the step is on the 계약해당일
    assert a.commissions(1) == 0.0               # renewal starts in policy year 2

    assert a.ci_reduced_share(1) == 0.0
    assert a.pols_ci(1) == pytest.approx(TRACE_2["pols_ci"], abs=TRACE)
    assert a.claims(1, "CI") == pytest.approx(
        TRACE_2["pols_ci"] * ACCEL_COHORT_FULL, abs=WON)

    assert a.pols_death(1) == pytest.approx(TRACE_2["pols_death"], abs=TRACE)
    assert a.pols_death_ci(1) == pytest.approx(TRACE_2["pols_death_ci"], abs=TRACE)
    assert 1.05 * a.pol_val_pp(2) == pytest.approx(FLOOR_2, abs=WON)
    assert FLOOR_2 < RESID_COHORT_FULL
    assert a.resid_db_pp(2, 1) == pytest.approx(RESID_COHORT_FULL, abs=1e-6)
    assert a.claims(1, "DEATH_CI") == pytest.approx(
        a.pols_if_ci_at(1, 1) * a.mort_rate_ci_mth(1) * a.resid_db_pp(2, 1), abs=WON)
    assert a.resid_db_avg_pp(1) == pytest.approx(RESID_DB_AVG_1, abs=WON)

    assert a.pols_lapse(1) == pytest.approx(TRACE_2["pols_lapse"], abs=TRACE)
    assert a.pols_lapse_ci(1) == pytest.approx(TRACE_2["pols_lapse_ci"], abs=TRACE)
    assert a.cv_pp(2) == CV_2 == 0.0
    assert a.cv_pp_ci(2) == CV_CI_2 == 0.0
    assert a.claims(1, "LAPSE") == 0.0
    assert a.claims(1, "LAPSE_CI") == 0.0

    assert a.claim_expenses(1) == pytest.approx(
        300000.0 * CLAIM_EXPENSE_EVENTS_2, abs=WON)
    assert a.net_cf(1) == pytest.approx(WORKED_EXAMPLE[1][-1], abs=WON)


def test_worked_example_the_month_the_account_floor_takes_over(kr_ci_anchor):
    """The crossing is one **month**, d = 79, not one policy year.

    ``1.05 V(78)`` is KRW 19,973,041.04, below the KRW 20,000,000 nominal, and
    ``1.05 V(79)`` is KRW 20,244,219.60, above it.  From that month-end every full
    cohort carries an identical residual and only the first-year reduced cohorts, at
    KRW 60,000,000, are still on their own nominal.  An annual grid could say only that
    the crossing fell inside policy year 7; the monthly one names the month, which is the
    seventh of it.
    """
    a = kr_ci_anchor
    t = FLOOR_CROSS_D - 1
    for name, value in TRACE_FLOOR_COUNTS.items():
        assert getattr(a, name)(t) == pytest.approx(value, abs=TRACE), name
    assert a.policy_year(t) == 7
    assert a.premiums(t) == pytest.approx(
        G_GROSS_MTH * TRACE_FLOOR_COUNTS["pols_if_pay"], abs=WON)
    assert a.inflation_factor(t) == pytest.approx(INFLATION_FLOOR, abs=5e-14)
    assert a.expenses(t) == pytest.approx(
        5000.0 * INFLATION_FLOOR * TRACE_FLOOR_COUNTS["pols_if"], abs=WON)
    assert a.commissions(t) == pytest.approx(0.03 * a.premiums(t), rel=1e-14)

    assert 1.05 * a.pol_val_pp(t) == pytest.approx(FLOOR_BEFORE, abs=1e-6)
    assert 1.05 * a.pol_val_pp(FLOOR_CROSS_D) == pytest.approx(FLOOR_AFTER, abs=1e-6)
    assert FLOOR_BEFORE < 20000000.0 < FLOOR_AFTER

    ids = a.ci_cohort_ids(t)
    assert ids == [-s for s in range(1, 13)] + list(range(1, t + 1))
    for s in ids:
        expected = RESID_COHORT_REDUCED if s < 0 else FLOOR_AFTER
        assert a.resid_db_pp(FLOOR_CROSS_D, s) == pytest.approx(expected, abs=1e-6), s
    assert sum(a.pols_if_ci_at(t, s) for s in ids) == pytest.approx(
        a.pols_if_ci(t), abs=TRACE)
    assert a.pols_death_ci(t) == pytest.approx(POLS_DEATH_CI_FLOOR, abs=TRACE)
    assert a.resid_db_avg_pp(t) == pytest.approx(RESID_DB_AVG_FLOOR, abs=1e-5)

    # The 해약공제액 is still running off: it reaches zero at month-end 84, five months
    # later, and thirteen years before 납입완료.
    assert a.surr_chg_pp(t) > 0.0
    assert a.surr_chg_pp(SURR_CHG_PERIOD_MTHS) == 0.0
    assert a.cv_pp(FLOOR_CROSS_D) == pytest.approx(0.50 * a.cv_std_pp(FLOOR_CROSS_D),
                                                   rel=1e-14)
    assert a.cv_pp_ci(FLOOR_CROSS_D) == pytest.approx(a.cv_std_pp(FLOOR_CROSS_D),
                                                      rel=1e-14)
    assert a.net_cf(t) == pytest.approx(NET_CF_FLOOR, abs=WON)


def test_worked_example_the_first_premium_free_month(kr_ci_anchor):
    """t = 240 — the first premium-free month and the largest step in the run.

    Three things change in this row: the premium stops, the renewal commission stops with
    it, and the pre-CI lapse rate steps eightfold from 0.001 to 0.008 onto a surrender
    value that has itself just doubled.  The monthly grid states the swing between the
    two **months** either side of 납입완료 — KRW 180,117.89 — where the annual grid
    compared two whole years; ``net_cf`` never returns to positive.
    """
    a = kr_ci_anchor
    for name, value in TRACE_PAID_UP.items():
        assert getattr(a, name)(240) == pytest.approx(value, abs=TRACE), name
    assert a.pols_if_pay(240) == 0.0
    assert a.premiums(240) == 0.0 and a.commissions(240) == 0.0
    assert a.premiums(239) > 0.0 and a.commissions(239) > 0.0
    assert a.inflation_factor(240) == pytest.approx(INFLATION_PAID_UP, abs=5e-13)
    assert a.expenses(240) == pytest.approx(
        5000.0 * INFLATION_PAID_UP * TRACE_PAID_UP["pols_if"], abs=WON)

    assert a.claims(240, "CI") == pytest.approx(
        TRACE_PAID_UP["pols_ci"] * ACCEL_COHORT_FULL, abs=WON)
    assert a.claims(240, "DEATH") == pytest.approx(
        1e8 * TRACE_PAID_UP["pols_death"], abs=WON)
    assert 1.05 * a.pol_val_pp(241) == pytest.approx(FLOOR_PAID_UP, abs=WON)
    assert all(a.resid_db_pp(241, s) == pytest.approx(FLOOR_PAID_UP, abs=WON)
               for s in (1, 60, 240))
    assert a.claims(240, "DEATH_CI") == pytest.approx(
        TRACE_PAID_UP["pols_death_ci"] * FLOOR_PAID_UP, abs=WON)

    assert a.lapse_rate(239) == pytest.approx(0.001, abs=5e-16)
    assert a.lapse_rate(240) == 0.008
    assert a.cv_mult(241) == 1.0
    assert a.cv_mult(240) == 1.0 and a.cv_mult(239) == 0.50
    assert a.claims(240, "LAPSE") == pytest.approx(
        a.cv_pp(241) * TRACE_PAID_UP["pols_lapse"], abs=WON)
    assert a.claim_expenses(240) == pytest.approx(
        300000.0 * CLAIM_EXPENSE_EVENTS_PAID_UP, abs=WON)
    assert a.net_cf(239) == pytest.approx(WORKED_EXAMPLE[239][-1], abs=WON)
    assert a.net_cf(240) == pytest.approx(WORKED_EXAMPLE[240][-1], abs=WON)
    assert a.net_cf(239) - a.net_cf(240) == pytest.approx(PAID_UP_SWING, abs=0.02)
    assert all(a.net_cf(t) < 0.0 for t in range(240, a.proj_len()))


def test_worked_example_undiscounted_totals(kr_ci_anchor):
    """The notes' undiscounted totals over the full 852 months, column by column."""
    df = kr_ci_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert df["pols_if"].sum() == pytest.approx(POLICY_MONTHS, abs=SPLIT)
    assert df.loc[0:239, "net_cf"].sum() == pytest.approx(PHASE_PAYING, abs=WON)
    assert df.loc[240:, "net_cf"].sum() == pytest.approx(PHASE_RUN_OFF, abs=WON)
    # Undiscounted, the contract loses money; discounting is out of scope.
    assert df["net_cf"].sum() < 0.0


def test_worked_example_decrement_split(kr_ci_anchor):
    """Four exits summing to exactly 1, with the CI transition standing outside them.

    This is the product's signature identity.  0.4273447323 of the cohort accelerates and
    none of that leaves: 0.4045046008 die having accelerated and 0.1400281094 die without,
    so of the 54.45% who die in force three quarters die post-CI.  A model that counted
    the acceleration as an exit would produce five terms summing above 1.
    """
    a = kr_ci_anchor
    ts = range(a.proj_len())
    deaths = sum(a.pols_death(t) for t in ts)
    deaths_ci = sum(a.pols_death_ci(t) for t in ts)
    lapses = sum(a.pols_lapse(t) for t in ts)
    lapses_ci = sum(a.pols_lapse_ci(t) for t in ts)
    accelerations = sum(a.pols_ci(t) for t in ts)
    assert deaths == pytest.approx(SUM_DEATH, abs=SPLIT)
    assert deaths_ci == pytest.approx(SUM_DEATH_CI, abs=SPLIT)
    assert lapses == pytest.approx(SUM_LAPSE, abs=SPLIT)
    assert lapses_ci == pytest.approx(SUM_LAPSE_CI, abs=SPLIT)
    assert deaths + deaths_ci + lapses + lapses_ci == pytest.approx(1.0, abs=1e-10)
    assert accelerations == pytest.approx(SUM_CI, abs=SPLIT)
    assert accelerations > lapses_ci + deaths      # far too large to be an exit
    assert a.pols_if(a.proj_len()) == 0.0
    assert (deaths + deaths_ci) == pytest.approx(0.544533, abs=5e-7)
    assert deaths_ci / (deaths + deaths_ci) == pytest.approx(0.7428, abs=5e-5)


def test_worked_example_person_months_and_the_post_ci_peak(kr_ci_anchor):
    """315.75 person-months, of which 68.80 are post-CI.

    The in-force sum is now in **months**, twelve to a policy year, which is the unit the
    maintenance expense is charged in.  The post-CI cohort peaks at 0.2178167855 policies
    at t = 420, attained age 75.  These are the weights on maintenance expense and on
    premium respectively, and getting either cohort's person-months wrong moves a whole
    expense or income line without moving any benefit.
    """
    a = kr_ci_anchor
    ts = range(a.proj_len())
    assert sum(a.pols_if(t) for t in ts) == pytest.approx(POLICY_MONTHS, abs=SPLIT)
    assert sum(a.pols_if_pre(t) for t in ts) == pytest.approx(
        POLICY_MONTHS_PRE, abs=SPLIT)
    assert sum(a.pols_if_ci(t) for t in ts) == pytest.approx(
        POLICY_MONTHS_CI, abs=SPLIT)
    assert sum(a.pols_if_pay(t) for t in ts) == pytest.approx(
        POLICY_MONTHS_PAY, abs=SPLIT)
    peak = max(ts, key=a.pols_if_ci)
    assert peak == POST_CI_PEAK_T
    assert a.pols_if_ci(peak) == pytest.approx(POST_CI_PEAK, abs=SPLIT)
    assert a.age(peak) == 75
    share_peak = max(ts, key=lambda t: a.pols_if_ci(t) / max(a.pols_if(t), 1e-300))
    assert share_peak == POST_CI_SHARE_OF_INFORCE_T
    assert a.pols_if_ci(share_peak) / a.pols_if(share_peak) == pytest.approx(
        POST_CI_SHARE_OF_INFORCE, abs=5e-4)
    assert POLICY_MONTHS_CI / POLICY_MONTHS == pytest.approx(
        POST_CI_SHARE_OF_PERSON_MONTHS, abs=5e-4)


def test_the_two_cross_checks_that_fell_out_of_the_model(ci_insurance, kr_ci_anchor):
    """The 80% form at 1.0782 times the 50% form, against [S4]'s published 1.085.

    Nothing in the construction was fitted to this.  Model point 3 is the anchor's own
    cell at a = 0.50 — same sex, same age, same sum assured, same 납입기간 — and the
    pricing quantities do not see the suppression factor or the lapse basis, so the ratio
    of the two net premiums is a clean second route to the price of thirty percentage
    points of acceleration.  Two independent routes agreeing to five parts in a thousand
    is a cross-check; quoting one and not testing it is a hostage.
    """
    a, half = kr_ci_anchor, ci_insurance.Projection[3]
    assert half.sex() == a.sex() and half.age_at_entry() == a.age_at_entry()
    assert half.sum_assured() == a.sum_assured()
    assert half.prem_period() == a.prem_period()
    assert half.accel_rate() == 0.50
    assert half.epv_ben(0) == pytest.approx(A0_1_HALF, abs=WON)
    assert half.prem_net_level_mth_pp() == pytest.approx(P_NET_HALF_MTH, abs=WON)
    relativity = a.prem_net_level_mth_pp() / half.prem_net_level_mth_pp()
    assert relativity == pytest.approx(FORM_RELATIVITY_MODEL, abs=5e-5)
    assert abs(relativity / FORM_RELATIVITY_PUBLISHED - 1.0) < 0.008
    # The annuity is identical on the two forms: only the benefit EPV moves.
    assert half.annuity_due(0) == pytest.approx(a.annuity_due(0), rel=1e-14)


def test_the_gross_to_net_loading_is_not_the_published_premium_index(kr_ci_anchor):
    """1.2064 sits beside a disclosed 보험료지수 of 130.1% and is a different ratio.

    The index is computed against the 금융감독원's prescribed 표준순보험료 and this is
    against the model's own net premium, so the agreement is one of order only and
    neither figure was used to calibrate the other.  The test states the relationship the
    notes state — same order, not equal — so that nobody later "fixes" one to the other.
    """
    a = kr_ci_anchor
    loading = a.premium_pp() / a.prem_net_level_pp()
    assert loading == pytest.approx(LOADING, abs=5e-11)
    assert loading == pytest.approx(
        a.premium_mth_pp() / a.prem_net_level_mth_pp(), rel=1e-14)
    assert 1.15 < loading < 1.35
    assert loading != pytest.approx(1.301, rel=1e-3)
    assert a.prem_net_level_pp() < a.premium_pp()


def test_the_shape_of_the_result_is_the_one_the_notes_read(kr_ci_anchor):
    """The residual is the larger stream, and 76.7% of benefits are CI-originated.

    Three readings the notes take off the totals, each of which a plausible alternative
    implementation would break: the 20% residual pays more, undiscounted, than the 80%
    acceleration; the two CI-originated streams are three quarters of all benefits
    against the pre-CI death benefit's 15.2%; and 42.3% of all benefits fall from the
    fortieth 계약해당일, so a projection truncated anywhere convenient understates
    materially.
    """
    a = kr_ci_anchor
    df = a.result_cf()
    benefits = df[["claims_ci", "claims_death", "claims_death_ci", "claims_lapse",
                   "claims_lapse_ci"]]
    assert benefits.sum().sum() == pytest.approx(TOTAL_BENEFITS, abs=WON)
    assert df["claims_death_ci"].sum() > df["claims_ci"].sum()
    assert df["claims_death_ci"].sum() > df["claims_death"].sum()
    ci_originated = df["claims_ci"].sum() + df["claims_death_ci"].sum()
    assert ci_originated == pytest.approx(CI_ORIGINATED, abs=WON)
    assert ci_originated / benefits.sum().sum() == pytest.approx(
        CI_ORIGINATED_SHARE, abs=5e-4)
    assert df["claims_death"].sum() / benefits.sum().sum() == pytest.approx(
        DEATH_SHARE, abs=5e-4)
    assert benefits.loc[480:].sum().sum() / benefits.sum().sum() == pytest.approx(
        BENEFITS_AFTER_YEAR_40, abs=5e-4)
    assert df.loc[480:, "claims_death_ci"].sum() / df["claims_death_ci"].sum() == (
        pytest.approx(DEATH_CI_AFTER_YEAR_40, abs=5e-4))


def test_the_residual_floor_is_worth_four_times_the_nominal_complement(kr_ci_anchor):
    """KRW 36,093,568.46 paid against KRW 8,090,217.24 on the nominal, a factor of 4.46.

    One number, ``resid_floor_mult = 1.05``, carries the largest benefit line in the
    projection.  Recomputing the post-CI death stream on the stated complement alone —
    which is what "80% now, 20% later" describes — collapses it to under a quarter, and
    that gap is the single largest structural feature of this liability and the easiest to
    omit.
    """
    a = kr_ci_anchor
    # The nominal-only stream is the aggregate this model carries as its own recursion,
    # so it is asserted both ways: cohort by cohort and off resid_nom_total_pp.
    on_nominal = sum(
        sum(a.pols_if_ci_at(t, s) * a.mort_rate_ci_mth(t) * a.resid_nominal_pp(s)
            for s in a.ci_cohort_ids(t))
        for t in range(a.proj_len()))
    assert on_nominal == pytest.approx(RESID_ON_NOMINAL, abs=WON)
    aggregate = sum(a.mort_rate_ci_mth(t) * a.resid_nom_total_pp(t)
                    for t in range(a.proj_len()))
    assert aggregate == pytest.approx(on_nominal, abs=WON)
    paid = a.result_cf()["claims_death_ci"].sum()
    assert paid / on_nominal == pytest.approx(FLOOR_WORTH, abs=5e-3)


def test_the_acceleration_costs_a_quarter_of_the_net_premium(kr_ci_anchor):
    """A0(0) = KRW 36,649,058.63 with no acceleration, against KRW 45,439,079.61 with it.

    The counterfactual is the same three-state contract paying the whole sum assured on
    death whenever it falls — a = 0, r = 1 — on the identical table and decrements, so
    the difference is purely the timing effect of moving four fifths of one sum assured
    forward and flooring the remainder.  It is recomputed here from the model's own rate
    cells rather than from a second model point, because ``accel_rate`` validates to the
    open interval and a = 0 is not a contract this product admits.
    """
    a = kr_ci_anchor
    v, sa = a.disc_factor_mth(), a.sum_assured()
    t_end, m = a.proj_len(), a.prem_period_mths()
    resid = 0.0
    resid_by_t = {t_end: 0.0}
    for t in range(t_end - 1, -1, -1):
        q = a.mort_rate_ci_base_mth(t)
        resid = v * (q * sa + (1.0 - q) * resid)
        resid_by_t[t] = resid
    benefit = 0.0
    for t in range(t_end - 1, -1, -1):
        qc, qd = a.ci_rate_mth_base(t), a.mort_rate_base_mth(t)
        benefit = v * ((1.0 - qc) * qd * sa + qc * resid_by_t[t + 1]
                       + (1.0 - qc) * (1.0 - qd) * benefit)
    annuity = 0.0
    for t in range(m - 1, -1, -1):
        annuity = 1.0 + v * (1.0 - a.ci_rate_mth_base(t)) * (
            1.0 - a.mort_rate_base_mth(t)) * annuity
    assert benefit == pytest.approx(A0_1_NO_ACCEL, abs=WON)
    assert annuity == pytest.approx(a.annuity_due(0), rel=1e-14)   # unchanged by a
    assert benefit / annuity == pytest.approx(P_NET_NO_ACCEL_MTH, abs=WON)
    assert a.prem_net_level_mth_pp() / (benefit / annuity) - 1.0 == pytest.approx(
        ACCELERATION_COST, abs=5e-5)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_the_acceleration_is_a_transition_not_an_exit(kr_ci_anchor):
    """l(t) - l(t+1) = D + D' + S + S' — **four** terms, and C(t) is not one of them.

    Adding the CI transition to the in-force roll-forward removes every claimant from the
    population on the day they claim, which is precisely what 감독규정 제7-60조제8호
    forbids the contract to do.  The symptom is a decrement sum above 1 and a post-CI
    cohort that never accumulates, and this is the most natural mistake on the product.
    """
    a = kr_ci_anchor
    assert a.check_pols_roll_fwd() is True
    for t in (0, 1, 78, 239, 240, 420, 719, 720, a.proj_len() - 1):
        exits = (a.pols_death(t) + a.pols_death_ci(t)
                 + a.pols_lapse(t) + a.pols_lapse_ci(t))
        assert a.pols_if(t) - a.pols_if(t + 1) == pytest.approx(exits, abs=1e-12)
        assert a.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        # The five-term version is wrong by exactly the month's accelerations.
        assert a.pols_if(t) - a.pols_if(t + 1) - (exits + a.pols_ci(t)) == (
            pytest.approx(-a.pols_ci(t), abs=1e-12))
    # A claimant is still in force: the post-CI cohort accumulates for decades.
    assert a.pols_ci(1) > 0.0 and a.pols_if_ci(2) > a.pols_if_ci(1)
    assert a.check_decrement_sum() is True


def test_pitfall_the_residual_floor_is_two_sided(kr_ci_anchor):
    """max(r B(s), c V(t)) — the nominal binds early and the account binds late.

    A one-sided maximum is right for most of the projection and wrong at the ends: before
    the month-end 79 the nominal binds on every full cohort and after it the account does,
    while the first-year reduced cohorts' KRW 60,000,000 stays on its own nominal until
    the month-end 212.  ``check_resid_floor()``
    tests the two limbs separately, and both directions are asserted here.
    """
    a = kr_ci_anchor
    assert a.check_resid_floor() is True
    for d in (2, 60, FLOOR_CROSS_D - 1):
        assert 1.05 * a.pol_val_pp(d) < 20000000.0
        assert a.resid_db_pp(d, 1) == pytest.approx(RESID_COHORT_FULL, abs=1e-6)
        assert a.resid_db_pp(d, 1) > 1.05 * a.pol_val_pp(d)          # nominal limb
    for d in (FLOOR_CROSS_D, 240, 480):
        assert 1.05 * a.pol_val_pp(d) > 20000000.0
        assert a.resid_db_pp(d, 1) == pytest.approx(
            1.05 * a.pol_val_pp(d), rel=1e-14)                       # account limb
    # A reduced cohort crosses eleven years later, on its own larger nominal.
    assert a.resid_db_pp(211, -4) == RESID_COHORT_REDUCED
    assert a.resid_db_pp(212, -4) == pytest.approx(1.05 * a.pol_val_pp(212), rel=1e-14)
    assert a.resid_db_pp(212, -4) > RESID_COHORT_REDUCED
    for t in (1, 78, 211, 468, 708):
        for s in a.ci_cohort_ids(t):
            assert a.resid_db_pp(t + 1, s) >= a.resid_nominal_pp(s) - 1e-6
            assert a.resid_db_pp(t + 1, s) >= 1.05 * a.pol_val_pp(t + 1) - 1e-6
        assert a.check_resid_floor_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_pitfall_the_floor_and_the_nominal_are_read_off_different_month_ends(
        kr_ci_anchor):
    """B(s) is the 기본보험금 at the acceleration date; V(t) is the account **now**.

    ``resid_db_pp(t, s)`` mixes two month-ends on purpose, and reading both off t, or
    both off s, is wrong in opposite directions.  Neither error shows before the month-end
    79, when both
    limbs still agree at the nominal — which is why a model can be built, tested on the
    early durations, and be wrong for sixty years.
    """
    a = kr_ci_anchor
    # The nominal moves with s and not with t; the floor moves with t and not with s.
    assert a.resid_nominal_pp(1) == pytest.approx(a.resid_nominal_pp(480), abs=1e-6)
    assert a.resid_nominal_pp(-4) != pytest.approx(a.resid_nominal_pp(4), rel=1e-6)
    assert a.resid_db_pp(480, 1) == a.resid_db_pp(480, 468)      # the shared floor
    assert a.resid_db_pp(480, 1) != pytest.approx(a.resid_db_pp(240, 1), rel=1e-6)
    # Reading the nominal off t instead of s destroys the reduced cohorts' residual.
    assert a.resid_db_pp(120, -4) == RESID_COHORT_REDUCED
    assert a.resid_db_pp(120, 1) < RESID_COHORT_REDUCED
    # Reading the floor off s instead of t freezes the residual at the entry account.
    assert 1.05 * a.pol_val_pp(1) < 1.05 * a.pol_val_pp(480)
    assert a.resid_db_pp(480, 1) > 1.05 * a.pol_val_pp(1)


def test_pitfall_collapsing_the_post_ci_cohorts_loses_the_first_year_reduced_ones(
        ci_insurance):
    """A reduced cohort carries KRW 60,000,000 where every other carries KRW 20,000,000.

    On the male anchor it is 0.18% of a month's accelerations and the error is invisible;
    on the female twin it is 19.5% and it is not.  This is why the test runs on
    ``point_id = 2`` and ``4`` and not only on the anchor: a model that averaged the
    cohorts would agree with the anchor's totals to four significant figures.
    """
    female = ci_insurance.Projection[2]
    assert female.ci_reduced_share(3) == pytest.approx(REDUCED_SHARE_F, abs=RATE)
    assert female.resid_nominal_pp(-4) == RESID_COHORT_REDUCED
    assert female.resid_nominal_pp(4) == pytest.approx(RESID_COHORT_FULL, abs=1e-6)
    assert female.accel_benefit_pp(-4) == 0.5 * female.accel_benefit_pp(4)
    # A reduced cohort survives the whole projection and never merges with the others.
    assert female.pols_if_ci_at(468, -4) > 0.0
    assert female.pols_if_ci_at(4, -4) == pytest.approx(
        female.pols_ci_in(3, -4), abs=1e-15)
    # The claim it produces in its own month is a tenth of that month's outgo.
    reduced = female.pols_ci_in(3, -4) * female.accel_benefit_pp(-4)
    assert reduced / female.claims(3, "CI") == pytest.approx(0.108, abs=5e-3)
    # The all-trigger design routes the whole first policy year into the reduced cohorts
    # and halves it, month by month.
    allpt = ci_insurance.Projection[4]
    assert allpt.first_year_scope() == "all"
    assert allpt.ci_reduced_share(0) == allpt.ci_reduced_share(11) == 1.0
    assert allpt.ci_reduced_share(12) == 0.0
    assert allpt.pols_ci_in(3, 4) == 0.0
    assert allpt.pols_ci_in(3, -4) == pytest.approx(allpt.pols_ci(3), rel=1e-14)
    assert allpt.claims(3, "CI") == pytest.approx(
        0.8 * 0.5 * allpt.sum_assured() * allpt.pols_ci(3), rel=1e-14)
    assert allpt.check_accel_complement() is True


def test_pitfall_the_premium_annuity_must_carry_the_ci_decrement(kr_ci_anchor):
    """178.71 months against an ordinary life annuity's 187.92 — 5.2%.

    Any CI/LTC 지급사유 waives all future 기본보험료, so a premium stream that ran on
    through the post-CI state would over-fund the contract by the whole of the CI
    decrement.  The wrong annuity gives a monthly net premium of KRW 241,798.85 against
    KRW 254,261.11, and ``check_pol_val_roll_fwd()`` fails immediately, which is what it
    is for.
    """
    a = kr_ci_anchor
    ordinary = 0.0
    for t in range(a.prem_period_mths() - 1, -1, -1):
        ordinary = 1.0 + a.disc_factor_mth() * (
            1.0 - a.mort_rate_base_mth(t)) * ordinary
    assert ordinary == pytest.approx(ANNUITY_DUE_ORDINARY, abs=5e-9)
    assert a.annuity_due(0) == pytest.approx(ANNUITY_DUE_1, abs=5e-9)
    assert ordinary / a.annuity_due(0) - 1.0 == pytest.approx(0.052, abs=5e-4)
    assert a.epv_ben(0) / ordinary == pytest.approx(P_NET_ORDINARY_MTH, abs=WON)
    # The annuity that is used discounts on both decrements, at every duration.
    for t in (0, 119, 239):
        assert a.annuity_due(t) == pytest.approx(
            1.0 + a.disc_factor_mth() * (1.0 - a.ci_rate_mth_base(t))
            * (1.0 - a.mort_rate_base_mth(t)) * a.annuity_due(t + 1), rel=1e-14)
    assert a.annuity_due(a.prem_period_mths()) == 0.0
    assert a.check_pol_val_roll_fwd() is True


def test_pitfall_the_post_ci_cohort_never_pays_a_premium(kr_ci_anchor):
    """lp(t) = l0(t) - lw(t): the post-CI count is nowhere in the premium weight.

    Weighting premium by ``pols_if(t)`` reproduces the first month, ``t = 0``, exactly and
    diverges from ``t = 1``
    onward — a slow, quiet error worth 9.150272 person-**months** of spurious premium
    inside the 납입기간, KRW 2,806,754.28 on this cell, of which the post-CI cohort is
    8.730436 (KRW 2,677,973.86) and the 장해 50%+ waived subset the rest.  It is the
    kind of mistake that never fails a roll-forward.
    """
    a = kr_ci_anchor
    assert a.pols_if_pay(0) == a.pols_if(0) == 1.0     # identical in month zero only
    for t in (1, 78, 120, 239):
        assert a.pols_if_pay(t) == pytest.approx(
            a.pols_if_pre(t) - a.pols_waived(t), rel=1e-14)
        assert a.pols_if_pay(t) < a.pols_if(t)
        assert a.premiums(t) == pytest.approx(a.premium_mth_pp() * a.pols_if_pay(t),
                                              rel=1e-14)
        assert a.premiums(t) < a.premium_mth_pp() * a.pols_if(t)
    spurious = sum(a.pols_if_ci(t) for t in range(a.prem_period_mths()))
    assert spurious == pytest.approx(SPURIOUS_PREMIUM_MONTHS, abs=5e-6)
    assert spurious * a.premium_mth_pp() == pytest.approx(
        SPURIOUS_PREMIUM_WON, abs=0.02)
    # The full substitution error is the post-CI cohort *plus* the waived subset.
    spurious_all = sum(a.pols_if(t) - a.pols_if_pay(t)
                       for t in range(a.prem_period_mths()))
    assert spurious_all == pytest.approx(SPURIOUS_PREMIUM_MONTHS_ALL, abs=5e-6)
    assert spurious_all * a.premium_mth_pp() == pytest.approx(
        SPURIOUS_PREMIUM_WON_ALL, abs=0.02)
    # Renewal commission follows the cash, so it inherits the same weight.
    assert a.commissions(120) == pytest.approx(0.03 * a.premiums(120), rel=1e-14)


def test_pitfall_the_suppression_has_two_exits_and_one_of_them_is_random(kr_ci_anchor):
    """CV'(t) = W(t) at **every** duration, not from t = m.

    Applying k to the post-CI cohort halves the surrender benefit of exactly the
    policyholders the carve-out exists to protect.  Over the whole projection the
    carve-out is worth only KRW 64,704.62 — because most post-CI surrenders happen after
    납입완료 anyway — so the bug is nearly invisible in the totals and factor-of-two wrong
    at every individual duration inside the 납입기간.  It is tested at the month-ends, not
    on the sum.
    """
    a = kr_ci_anchor
    assert a.check_cv_carve_out() is True
    for d in (20, 60, 120, 239):
        assert a.cv_pp_ci(d) == pytest.approx(a.cv_std_pp(d), rel=1e-14)
        assert a.cv_mult(d) == 0.50
        assert a.cv_pp_ci(d) == pytest.approx(2.0 * a.cv_pp(d), rel=1e-14)
    for d in (240, 360, 720):
        assert a.cv_pp_ci(d) == pytest.approx(a.cv_pp(d), rel=1e-14)
    suppressed = sum(max(0.0, a.cv_pp(t + 1) - a.loan_pp(t)) * a.pols_lapse_ci(t)
                     for t in range(a.proj_len()))
    assert suppressed == pytest.approx(SUPPRESSED_LAPSE_CI, abs=WON)
    paid = a.result_cf()["claims_lapse_ci"].sum()
    assert paid - suppressed == pytest.approx(CARVE_OUT_WORTH, abs=WON)
    assert (paid - suppressed) / paid < 0.04          # invisible in the totals
    assert a.claims(19, "LAPSE_CI") == pytest.approx(
        2.0 * a.cv_pp(20) * a.pols_lapse_ci(19), rel=1e-14)  # and doubled at that date


def test_pitfall_the_step_at_paid_up_is_one_over_k_on_one_month_end(kr_ci_anchor):
    """CV(240) / (k W(240)) = 2.0000000000; the month-on-month ratio 2.0103 is not it.

    The multiplier takes two values and only two — k inside the 납입기간 and 1 from it —
    so a model that grades, interpolates or smooths across the boundary fails here.  The
    monthly grid is what makes the distinction sharp: the adjacent-**month** ratio is
    2.0103 against the annual grid's 2.1290, because a month of account accrual is a
    twelfth of a year's, so the step is visibly the whole of the movement and not a
    mixture of the two.
    """
    a = kr_ci_anchor
    mm = a.prem_period_mths()
    assert mm == 240
    assert {a.cv_mult(t) for t in range(a.proj_len() + 1)} == {0.50, 1.0}
    assert a.cv_mult(mm - 1) == 0.50 and a.cv_mult(mm) == 1.0
    assert a.cv_pp(mm) / (0.50 * a.cv_std_pp(mm)) == pytest.approx(2.0, abs=5e-11)
    assert a.cv_pp(mm) / (0.50 * a.cv_std_pp(mm)) == pytest.approx(
        1.0 / a.cv_floor_ratio(), rel=1e-14)
    assert a.cv_pp(mm) / a.cv_pp(mm - 1) == pytest.approx(2.0103, abs=5e-5)
    assert a.pol_val_pp(mm) / a.pol_val_pp(mm - 1) < 1.01
    # The last paying month, t = 12m - 1, closes at month-end 12m and is paid on the full
    # value; the month before it is paid on the suppressed one.
    assert a.claims(mm - 1, "LAPSE") == pytest.approx(
        a.cv_std_pp(mm) * a.pols_lapse(mm - 1), rel=1e-14)
    assert a.claims(mm - 2, "LAPSE") == pytest.approx(
        0.50 * a.cv_std_pp(mm - 1) * a.pols_lapse(mm - 2), rel=1e-14)


def test_pitfall_the_step_is_not_a_surrender_charge_effect(kr_ci_anchor):
    """SC(d) = 0 from month-end 84, thirteen years before the cliff, in 84 equal steps.

    A model that ties the two together will place the step at the wrong duration on any
    point where the 해약공제기간 and the 납입기간 differ — which is every point in this
    table but one, the cap being seven years and the payment terms ten, twenty and thirty.
    The monthly grid runs the line off in 84 steps rather than seven, so the balance
    deducted is the balance outstanding in the month a surrender is actually taken.
    """
    a = kr_ci_anchor
    assert a.surr_chg_cap_pp() == pytest.approx(SC_CAP, abs=WON)
    n = SURR_CHG_PERIOD_MTHS
    for d in (0, 1, 12, 41, 83):
        assert a.surr_chg_pp(d) == pytest.approx(SC_CAP * (n - d) / n, abs=WON)
    assert a.surr_chg_pp(0) - a.surr_chg_pp(1) == pytest.approx(SC_STEP, abs=1e-6)
    assert all(a.surr_chg_pp(d) == 0.0 for d in (84, 85, 239, 240, 241, 720))
    assert SURR_CHG_PERIOD_MTHS < a.prem_period_mths() - 144
    # The value steps at 12m with the charge long gone, so the two are unrelated.
    assert a.surr_chg_pp(a.prem_period_mths()) == 0.0
    assert a.cv_pp(a.prem_period_mths()) > 2.0 * a.cv_pp(a.prem_period_mths() - 1)


def test_pitfall_the_statutory_cap_uses_the_pre_acceleration_sum_assured(kr_ci_anchor):
    """KRW 100,000,000, not the KRW 20,000,000 residual: a 20% under-statement avoided.

    별표 15 제3호 read with 제8호 takes the 일반사망보험금 before any 증감, and a CI
    contract covers death from any cause, so 일반사망 applies directly.  Building the cap
    off the residual would cut it from KRW 3,944,704 to KRW 3,144,704 and shrink every
    early surrender charge with it.
    """
    a = kr_ci_anchor
    assert a.surr_chg_cap_pp() == pytest.approx(SC_CAP, abs=WON)
    on_residual = (0.80 * a.premium_pp() * 0.05 * 20
                   + 0.01 * a.resid_rate() * a.sum_assured())
    assert on_residual == pytest.approx(3144704.0, abs=WON)
    assert a.surr_chg_cap_pp() - on_residual == pytest.approx(800000.0, abs=WON)
    assert on_residual / a.surr_chg_cap_pp() - 1.0 == pytest.approx(-0.203, abs=5e-4)
    # The cap is built from the gross premium and the face amount, nothing else.
    assert a.surr_chg_cap_pp() == pytest.approx(
        0.80 * a.premium_pp() * 0.05 * 20 + 0.01 * a.sum_assured(), rel=1e-14)


def test_pitfall_ci_before_death_before_lapse(kr_ci_anchor):
    """The processing order, asserted through a quantity that would move if it changed.

    Reversing the first two routes lives that would have accelerated into the death
    decrement, which is four times smaller in the first policy year and 7.40 times
    smaller at attained 60.  The order is [std] and is asserted rather than described:
    deaths are taken from the survivors of the CI transition and surrenders from the
    survivors of both — and on the monthly grid the three decrements are the **monthly**
    conversions, not the annual rates.
    """
    a = kr_ci_anchor
    for t in (0, 1, 78, 240, 468):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_death(t) == pytest.approx(
            a.pols_if_pre(t) * (1 - a.ci_rate_mth(t)) * a.mort_rate_mth(t), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_pre(t) * (1 - a.ci_rate_mth(t)) * (1 - a.mort_rate_mth(t))
            * a.lapse_rate_mth(t), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(a.pols_if(t + 1), abs=1e-14)
        # Death first would give a strictly larger death count at every duration.
        death_first = a.pols_if_pre(t) * a.mort_rate_mth(t)
        assert death_first > a.pols_death(t)
    # The re-routing is worth more than the whole pre-CI death stream in month 0.
    assert a.pols_if_pre(0) * a.mort_rate_mth(0) - a.pols_death(0) == pytest.approx(
        a.ci_rate_mth(0) * a.mort_rate_mth(0), rel=1e-12)
    assert a.pols_if_at(0, "BEF_LAPSE") == pytest.approx(
        1.0 * (1 - a.ci_rate_mth(0)) * (1 - a.mort_rate_mth(0)) + a.pols_ci(0),
        rel=1e-14)
    assert a.check_ci_state_roll_fwd() is True


def test_pitfall_the_two_payments_are_one_step_apart(kr_ci_anchor):
    """A life accelerating in month t joins the post-CI state at the start of month t + 1.

    Paying an acceleration and a residual death benefit in the same step on the same life
    double-counts the claim expense and mis-times the residual.  The first month, t = 0,
    is the clean case: accelerations occur and no residual death benefit is paid at all.

    **The lag is now a month where it was a year**, which is the single largest number the
    conversion moves on this product: the post-CI cohort is exposed to its own mortality
    from the month after the claim rather than from the next 계약해당일, and the post-CI
    in-force at the twentieth 계약해당일 is 1.1% lower for that reason alone.
    """
    a = kr_ci_anchor
    assert a.pols_ci(0) > 0.0
    assert a.pols_if_ci(0) == 0.0
    assert a.pols_death_ci(0) == 0.0 and a.claims(0, "DEATH_CI") == 0.0
    assert a.pols_if_ci(1) == pytest.approx(a.pols_ci(0), rel=1e-14)
    assert a.claims(1, "DEATH_CI") > 0.0
    for t in (1, 78, 240):
        # A cohort is labelled by the month-end it was paid at, so no label above t
        # can be populated at the start of month t.
        assert a.ci_cohort_ids(t) == (
            [-s for s in range(1, min(t, 12) + 1)] + list(range(1, t + 1)))
        assert a.pols_if_ci_at(t, t + 1) == 0.0
        assert a.pols_if_ci_at(t + 1, t + 1) == pytest.approx(
            a.pols_ci_in(t, t + 1), rel=1e-14)
    # The claim expense counts the acceleration once, in its own month.
    assert a.claim_expenses(0) == pytest.approx(
        300000.0 * (a.pols_ci(0) + a.pols_death(0)), rel=1e-14)


def test_pitfall_the_ci_decrement_stops_at_n_ci_and_nothing_else_does(kr_ci_anchor):
    """Three end dates in one projection: t = 239, t = 719 and t = 851, the last of each.

    The premium stops at 납입완료, the CI cover at the 100세 계약해당일 and the contract at
    the mortality table's terminal age.  The three counts ``prem_period_mths()``,
    ``ci_cover_end()`` and ``proj_len()`` are 240, 720 and 852 months and are exclusive
    ends.  The eleven post-CI-cover years still carry KRW 183,916.56 of claims, so
    truncating the projection at the end of CI cover — or at attained age 100 —
    understates materially.
    """
    a = kr_ci_anchor
    assert (a.prem_period_mths(), a.ci_cover_end(), a.proj_len()) == (240, 720, 852)
    assert a.age(a.ci_cover_end() - 1) == 99
    assert a.ci_rate(719) > 0.0 and a.ci_rate(720) == 0.0
    assert all(a.ci_rate(t) == 0.0 for t in range(720, a.proj_len()))
    assert a.claims(719, "CI") > 0.0 and a.claims(720, "CI") == 0.0
    assert a.premiums(239) > 0.0 and a.premiums(240) == 0.0
    for t in (720, 780, 840):
        assert a.claims(t, "DEATH") > 0.0
        assert a.claims(t, "LAPSE") > 0.0
        assert a.expenses(t) > 0.0
    assert a.claims(720, "DEATH_CI") > 0.0
    # A fourth date, and it is a consequence rather than a boundary: q' is three times
    # q and caps at 1 from attained age 101, so the post-CI cohort is extinguished at
    # t = 744 while the pre-CI one runs another nine years.
    assert a.mort_rate_ci(732) == 1.0 and a.mort_rate(732) < 1.0
    assert a.pols_if_ci(743) > 0.0 and a.pols_if_ci(744) == 0.0
    assert a.claims(744, "DEATH_CI") == 0.0 and a.claims(744, "DEATH") > 0.0
    tail = sum(a.claims(t) for t in range(a.ci_cover_end(), a.proj_len()))
    assert tail == pytest.approx(CLAIMS_AFTER_CI_COVER_TAIL, abs=WON)
    # The horizon is the table's: q = 1 in the final policy YEAR, and the monthly
    # conversion spreads that certain death uniformly over its twelve months rather
    # than killing the cohort in the first of them.
    assert a.mort_rate(a.proj_len() - 1) == 1.0
    assert a.mort_rate_mth(a.proj_len() - 1) == 1.0
    assert a.mort_rate_mth(a.proj_len() - 12) == pytest.approx(1.0 / 12.0, rel=1e-14)
    assert a.pols_if(a.proj_len() - 1) > 0.0
    assert a.pols_if(a.proj_len()) == 0.0


def test_pitfall_ci_rate_is_a_first_event_rate(ci_insurance, kr_ci_anchor):
    """One rate across the whole trigger set, and one benefit paid once.

    The benefit is payable once only across eight 중대한 질병, four 중대한 수술, 중대한
    화상 및 부식 and 장기요양상태, and the Korean supervisor required the overlap between
    causes to be reflected in the filed rate.  A table built by adding published
    site-specific incidences double-counts every life carrying two qualifying conditions —
    so the model reads one grid, sums it once, and exposes no second CI decrement anywhere.
    """
    a = kr_ci_anchor
    assert a.ci_rate(240) == pytest.approx(
        sum(a.ci_rate_at_age(60, c) for c in CAUSE_ORDER), abs=1e-15)
    # There is exactly one CI decrement and one acceleration benefit kind.
    names = set(ci_insurance.Projection.cells) | set(ci_insurance.Projection.refs)
    for absent in ("ci_rate_cancer", "ci_rate_ami", "ci_rate_stroke",
                   "pols_ci_second", "claims_ci_second", "multi_pay"):
        assert absent not in names, f"{absent}: a second CI event"
    with pytest.raises(FormulaError):
        a.claims(4, "CI_SECOND")
    # A cohort accelerates once: entrants exist only in the month that formed the label.
    assert a.pols_ci_in(40, 41) == pytest.approx(a.pols_ci(40), rel=1e-14)
    assert a.pols_ci_in(41, 41) == 0.0 and a.pols_ci_in(40, 40) == 0.0
    doc = flat(ci_insurance.Projection.cells["ci_rate_base"].doc)
    assert "first-event" in doc


def test_pitfall_there_is_no_survival_period(ci_insurance, kr_ci_anchor):
    """The Korean supervisor refused the overseas 30-day requirement, so none is modelled.

    Importing it would move lives from the CI decrement to the death decrement and change
    what they are paid from ``a B`` plus a later ``r B`` to ``B`` once.  The consequence
    the model does carry instead is post-CI excess mortality — the two decrements are
    correlated and ``mort_ci_factor`` is where that correlation lives.
    """
    a = kr_ci_anchor
    names = set(ci_insurance.Projection.cells) | set(ci_insurance.Projection.refs)
    for absent in ("survival_period", "survival_days", "surv_period_days",
                   "ci_survival_factor"):
        assert absent not in names, f"{absent}: this contract has no survival period"
    # A claimant is paid in the month of the event, whatever happens next.
    assert a.claims(0, "CI") > 0.0
    assert a.mort_ci_factor() == 3.0
    assert a.mort_rate_ci(0) == pytest.approx(3.0 * a.mort_rate(0), rel=1e-14)
    doc = flat(ci_insurance.Projection.cells["mort_ci_factor"].doc)
    assert "survival period" in doc
    assert "not independent competing risks" in doc


def test_pitfall_pols_if_is_the_total_in_force(kr_ci_anchor):
    """Maintenance expense is weighted by l(t), both states, and premium by lp(t).

    A post-CI policy is still a policy: it is administered, it can surrender, it can
    claim.  Weighting maintenance by ``pols_if_pre`` drops 60.1% of the in-force count at
    the peak and 21.8% of the projection's person-months; weighting premium by
    ``pols_if`` adds a cohort that pays nothing.  The two errors point in opposite
    directions and neither breaks a roll-forward.
    """
    a = kr_ci_anchor
    for t in (1, 78, 240, 420, 708):
        assert a.pols_if(t) == pytest.approx(
            a.pols_if_pre(t) + a.pols_if_ci(t), rel=1e-14)
        assert a.expenses(t) == pytest.approx(
            5000.0 * a.inflation_factor(t) * a.pols_if(t), rel=1e-14)
        assert a.expenses(t) > 5000.0 * a.inflation_factor(t) * a.pols_if_pre(t)
    assert a.result_cf().loc[420, "pols_if"] == pytest.approx(
        a.pols_if(420), abs=INFORCE)
    d = POST_CI_SHARE_OF_INFORCE_T
    assert 1.0 - a.pols_if_pre(d) / a.pols_if(d) == pytest.approx(
        POST_CI_SHARE_OF_INFORCE, abs=5e-4)
    # The acquisition expense and initial commission ride on l(0) alone, and the
    # commission is on the ANNUAL premium, the unit a Korean scale is written in.
    assert a.expenses(0) == pytest.approx(500000.0 + 5000.0, abs=WON)
    assert a.commissions(0) == pytest.approx(0.80 * a.premium_pp(), abs=WON)


def test_pitfall_the_claim_expense_is_charged_on_three_events(kr_ci_anchor):
    """CI, pre-CI death and post-CI death; charging on deaths alone loses 44%.

    Two payments mean two claim events and two handling costs, and the CI event is the
    more expensive of the two to adjudicate in practice, the whole dispute record of this
    product being about the 중대한 definitions.  The expense is published in its own
    column and is not inside ``expenses``.
    """
    a = kr_ci_anchor
    for t in (0, 78, 240, 708):
        assert a.claim_expenses(t) == pytest.approx(
            300000.0 * (a.pols_ci(t) + a.pols_death(t) + a.pols_death_ci(t)),
            rel=1e-14)
    total = a.result_cf()["claim_expenses"].sum()
    deaths_only = 300000.0 * sum(
        a.pols_death(t) + a.pols_death_ci(t) for t in range(a.proj_len()))
    assert total == pytest.approx(TOTALS["claim_expenses"], abs=WON)
    assert 1.0 - deaths_only / total == pytest.approx(
        CLAIM_EXPENSE_UNDERSTATEMENT, abs=5e-3)
    # It is beside the expense line, not inside it.
    assert a.expenses(120) == pytest.approx(
        5000.0 * a.inflation_factor(120) * a.pols_if(120), rel=1e-14)
    assert "claim_expenses" in a.result_cf().columns


def test_pitfall_the_loan_is_floored_and_the_acceleration_is_not_netted(ci_insurance):
    """max(0, . - L) on four payments, and the 선지급 paid gross of the balance.

    Model point 7 is the only point with a loan and draws half the available room at
    duration 12, inside the 납입기간 where the base is the suppressed value.  The
    acceleration is paid gross — no retrieved document says the 선지급 is reduced by the
    balance — so the loan stays outstanding against the residual, which is where it bites.
    """
    p = ci_insurance.Projection[7]
    assert p.pol_loan_util() == 0.5 and p.pol_loan_year() == 12
    # The draw is at the 계약해당일 closing policy year 12, which is month-end 144: the
    # contractual duration did not move, only the grid under it.
    assert p.loan_pp(143) == 0.0
    assert p.pol_loan_draw(144) == pytest.approx(0.5 * p.loan_avail_pp(144), rel=1e-14)
    assert p.loan_pp(144) == pytest.approx(
        p.pol_loan_draw(144) * (1.04 ** (1.0 / 12.0)), rel=1e-12)
    assert p.check_loan_roll_fwd() is True
    # Twelve months of the monthly roll compound back to exactly one year at 4.00%.
    assert p.loan_pp(156) / p.loan_pp(144) == pytest.approx(1.04, rel=1e-12)
    for t in (144, 239, 468):
        assert p.claims(t, "DEATH") == pytest.approx(
            max(0.0, p.base_benefit_pp(t + 1) - p.loan_pp(t)) * p.pols_death(t),
            rel=1e-12)
        assert p.claims(t, "LAPSE") == pytest.approx(
            max(0.0, p.cv_pp(t + 1) - p.loan_pp(t)) * p.pols_lapse(t), rel=1e-12)
        assert p.claims(t, "LAPSE_CI") == pytest.approx(
            max(0.0, p.cv_pp_ci(t + 1) - p.loan_pp(t)) * p.pols_lapse_ci(t), rel=1e-12)
        assert p.claims(t, "DEATH_CI") >= 0.0
        assert p.claims(t, "LAPSE") >= 0.0
    # The acceleration is not netted: it is the cohort count times the gross benefit.
    for t in (144, 239):
        assert p.claims(t, "CI") == pytest.approx(
            p.pols_ci_in(t, t + 1) * p.accel_benefit_pp(t + 1), rel=1e-14)
        assert p.loan_pp(t) > 0.0
    # A surrender in month 144 pays the suppressed value net of a loan drawn on it.
    assert p.cv_pp(145) > p.loan_pp(144) > 0.0


def test_pitfall_the_two_decrement_tables_are_not_the_chassis(ci_insurance):
    """omega = 110 here against 115 on the whole life chassis, on different anchors.

    The two files are fitted to different disclosures on different bases, so swapping
    them changes the horizon by five years and the whole mortality level: q(M, 40) is
    0.00068 here, [S3]'s own disclosed CI 예정 경험 사망률, against 0.00085 there.  The
    chassis relationship this product states is about mechanics, not about tables.
    """
    ci_table = pd.read_csv(CSV_DIR / "mort_table.csv")
    chassis = pd.read_csv(CSV_DIR.parent / "whole_life" / "mort_table.csv")
    assert sorted(set(zip(ci_table[ci_table["mort_rate"] >= 1.0]["sex"],
                          ci_table[ci_table["mort_rate"] >= 1.0]["age"]))) == [
        ("F", 110), ("M", 110)]
    assert set(chassis[chassis["mort_rate"] >= 1.0]["age"]) == {115}
    ci_40 = ci_table[(ci_table.sex == "M") & (ci_table.age == 40)]["mort_rate"].iloc[0]
    wl_40 = chassis[(chassis.sex == "M") & (chassis.age == 40)]["mort_rate"].iloc[0]
    assert ci_40 == 0.00068 and wl_40 != ci_40
    assert ci_insurance.Projection[1].omega_age() == 110
    assert ci_insurance.Projection[1].proj_years() == 110 - 40 + 1
    assert ci_insurance.Projection[1].proj_len() == 12 * (110 - 40 + 1)


# ---------------------------------------------------------------------------
# The product's own identities and boundaries


def test_nine_check_cells_are_published_each_with_its_residual(ci_insurance):
    """Nine identities, asserted **by name**, each with the signed residual beside it.

    That they are *true*, on all nine model points, is asserted in
    ``test_model_conventions_kr.py``, whose sweep discovers every ``check_*``
    generically and calls it on every model point of every model in the library.  Generic
    discovery cannot notice a check that has *gone*: it simply stops being discovered.
    Naming them is the statement left here, and on this product the names matter — four
    of the nine exist only because of the acceleration.
    """
    cells = set(ci_insurance.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == CHECK_CELLS
    for name in published:
        assert name + "_resid" in cells, name
    # The four that are this product's rather than the chassis's.
    assert {"check_ci_state_roll_fwd", "check_accel_complement", "check_resid_floor",
            "check_cv_carve_out"} <= published


def test_the_two_state_roll_forward_closes_on_the_anchor(kr_ci_anchor):
    """The pre-CI cohort loses exactly C + D + S and the post-CI cohort gains exactly C.

    The total roll-forward cannot see a policy that leaves one state without arriving in
    the other, because the two errors cancel in the aggregate.  This is the identity that
    catches it, and it is the one an implementation of an acceleration most needs.
    """
    a = kr_ci_anchor
    assert a.check_ci_state_roll_fwd() is True
    for t in range(a.proj_len()):
        pre_out = a.pols_ci(t) + a.pols_death(t) + a.pols_lapse(t)
        assert a.pols_if_pre(t) - a.pols_if_pre(t + 1) == pytest.approx(
            pre_out, abs=1e-12)
        post_in = a.pols_ci(t) - a.pols_death_ci(t) - a.pols_lapse_ci(t)
        assert a.pols_if_ci(t + 1) - a.pols_if_ci(t) == pytest.approx(
            post_in, abs=1e-12)
        assert a.check_ci_state_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_the_cohort_counts_reconstruct_the_post_ci_total(kr_ci_anchor):
    """l1(t) is the sum over cohorts, and every cohort decrements on its own two rates.

    The post-CI cohort is carried by entry **month** because the residual is a cohort
    property.  That decomposition has to be exact, or the aggregate count — which this
    model carries as its own recursion, the cohort table being twelve times longer than
    the annual grid's — and the cohort-by-cohort benefit calculation are describing
    different populations.  The closed form ``pols_if_ci_at`` uses is asserted against
    the step-by-step recursion it replaces, which is the point of this test.
    """
    a = kr_ci_anchor
    for t in (1, 13, 78, 240, 468):
        assert a.pols_if_ci(t) == pytest.approx(
            sum(a.pols_if_ci_at(t, s) for s in a.ci_cohort_ids(t)), rel=1e-12)
        for s in a.ci_cohort_ids(t)[:4] + a.ci_cohort_ids(t)[-4:]:
            assert a.pols_if_ci_at(t, s) == pytest.approx(
                a.pols_ci_in(t - 1, s)
                + a.pols_if_ci_at(t - 1, s) * (1 - a.mort_rate_ci_mth(t - 1))
                * (1 - a.lapse_rate_ci_mth(t - 1)), rel=1e-12)
    # And the aggregate total of the nominal residuals, likewise.
    for t in (13, 78, 240):
        assert a.resid_nom_total_pp(t) == pytest.approx(
            sum(a.pols_if_ci_at(t, s) * a.resid_nominal_pp(s)
                for s in a.ci_cohort_ids(t)), rel=1e-11)
        assert a.resid_db_total_pp(t) == pytest.approx(
            sum(a.pols_if_ci_at(t, s) * a.resid_db_pp(t + 1, s)
                for s in a.ci_cohort_ids(t)), rel=1e-11)
    assert a.pols_death_ci(240) == pytest.approx(
        a.pols_if_ci(240) * a.mort_rate_ci_mth(240), rel=1e-14)
    assert a.pols_lapse_ci(240) == pytest.approx(
        a.pols_if_ci(240) * (1 - a.mort_rate_ci_mth(240))
        * a.lapse_rate_ci_mth(240), rel=1e-14)


def test_the_acceleration_and_its_residual_sum_to_the_base_benefit(kr_ci_anchor):
    """a B + r B = B and a f B + (1 - a f) B = B, cohort by cohort.

    The one thing in this product that is exact rather than standardized: the
    acceleration never adds cover, it redistributes one sum assured across two dates.
    Holding r as the arithmetic complement rather than as a second model point column is
    what makes the identity unfalsifiable, and this asserts it on the cohorts actually
    formed — so a first-year model point checks both the full and the reduced arithmetic.
    """
    a = kr_ci_anchor
    assert a.check_accel_complement() is True
    for d in (3, 7, 12):
        assert a.accel_benefit_pp(-d) + a.resid_nominal_pp(-d) == pytest.approx(
            a.base_benefit_pp(d), rel=1e-14)
    for s in (1, 84, 240, 480):
        assert a.accel_benefit_pp(s) + a.resid_nominal_pp(s) == pytest.approx(
            a.base_benefit_pp(s), rel=1e-14)
        assert a.accel_benefit_pp(s) == pytest.approx(
            0.80 * a.base_benefit_pp(s), rel=1e-14)
    for t in (0, 3, 40, 468):
        assert a.check_accel_complement_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_the_policy_value_rolls_forward_on_the_pricing_basis(kr_ci_anchor):
    """(V(t) + P 1{t<m})(1+i) = the year's expected outgo plus (1-q_ci)(1-q) V(t+1).

    The prospective closed form and the retrospective recursion are the same object seen
    from two ends, so this catches a mis-set 납입기간, a discount factor applied on the
    wrong side, or a CI decrement present in the benefit and absent from the annuity —
    none of which the prospective formula alone would reveal.  The account runs on its own
    clock -- the month-end one, 0 at issue -- and is a function of that index, P^m, j and
    the two pricing decrements, and of no policy count at all.
    """
    a = kr_ci_anchor
    assert a.check_pol_val_roll_fwd() is True
    for t in (0, 1, 78, 239, 240, 468, a.proj_len() - 1):
        assert a.check_pol_val_roll_fwd_resid(t) == pytest.approx(0.0, abs=1.0)
    assert a.pol_val_pp(0) == 0.0
    assert a.pol_val_pp(a.proj_len()) == 0.0
    # No premium term in the recursion once premiums have stopped.
    qc, qd = a.ci_rate_mth_base(348), a.mort_rate_base_mth(348)
    assert a.pol_val_pp(348) * (1.0 + a.prem_int_rate_mth()) == pytest.approx(
        qc * (0.80 * a.sum_assured() + a.epv_resid(349))
        + (1 - qc) * qd * a.sum_assured()
        + (1 - qc) * (1 - qd) * a.pol_val_pp(349), abs=1.0)
    assert a.pol_val_pp(120) == pytest.approx(
        a.epv_ben(120) - a.prem_net_level_mth_pp() * a.annuity_due(120), rel=1e-14)


def test_the_published_cash_flow_statement_closes(kr_ci_anchor):
    """net_cf equals the eleven published columns of the same row, every year.

    A sixth benefit kind added to ``claims`` and left out of the statement would vanish
    silently without this; it shows up here instead.  The columns are published as five
    ``claims_*`` splits rather than one total precisely so that they must sum.
    """
    a = kr_ci_anchor
    assert a.check_net_cf() is True
    df = a.result_cf()
    outgo = df[["claims_ci", "claims_death", "claims_death_ci", "claims_lapse",
                "claims_lapse_ci", "claim_expenses", "expenses",
                "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-6)
    for t in (0, 240, 708):
        assert a.claims(t) == pytest.approx(
            sum(a.claims(t, k) for k in
                ("CI", "DEATH", "DEATH_CI", "LAPSE", "LAPSE_CI")), rel=1e-12)
        assert a.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_the_result_table_has_the_library_column_vocabulary(kr_ci_anchor):
    """pols_if first, net_cf last, five claims splits and no ``claims`` subtotal column.

    The five-way split is the point of the publication order: a three-column statement
    would hide the whole subject of this model, which is that ``claims_ci`` and
    ``claims_death_ci`` are two payments arising from one decrement at two dates.
    """
    df = kr_ci_anchor.result_cf()
    assert list(df.columns) == list(CF_COLUMNS)
    assert "claims" not in df.columns
    assert df.index.name == "t"
    assert list(df.index) == list(range(PROJ_LEN))
    assert df.notna().all().all()
    pols = kr_ci_anchor.result_pols()
    assert list(pols.columns) == [
        "pols_if", "pols_if_pre", "pols_if_ci", "pols_if_pay", "pols_ci",
        "pols_death", "pols_death_ci", "pols_lapse", "pols_lapse_ci",
        "mort_rate_mth", "ci_rate_mth", "lapse_rate_mth"]
    vals = kr_ci_anchor.result_val()
    assert list(vals.columns) == [
        "pol_val_pp", "surr_chg_pp", "cv_std_pp", "cv_pp", "cv_pp_ci",
        "base_benefit_pp", "accel_benefit_pp", "resid_nominal_pp",
        "resid_db_avg_pp", "loan_pp"]


def test_net_cf_carries_the_notes_own_sign(ci_insurance, kr_ci_anchor):
    """Income-positive, so there is no outgo-positive ``liability_cf`` to publish.

    The shape the notes describe: a deep strain in the first **month**, where the whole
    first-year commission and the acquisition expense fall against one instalment of
    premium, a long positive stretch while the premium runs, then a negative step at
    납입완료 from which the stream never recovers.
    """
    assert "liability_cf" not in ci_insurance.Projection.cells
    a = kr_ci_anchor
    assert a.net_cf(0) < 0.0
    assert all(a.net_cf(t) > 0.0 for t in range(1, 240))
    assert all(a.net_cf(t) < 0.0 for t in (240, 348, 588, 840))
    assert a.net_cf(1) > 0.0 > a.net_cf(240)


def test_invalid_enum_values_raise(kr_ci_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    a = kr_ci_anchor
    with pytest.raises(FormulaError):
        a.pols_if_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        a.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        a.claims(0, "MATURITY")
    with pytest.raises(FormulaError):
        a.ci_rate_at_age(40, "thyroid")


def test_there_is_no_maturity_benefit_and_no_tail_states(ci_insurance, kr_ci_anchor):
    """종신 means no expiry date and no 만기보험금; the horizon is the table's.

    Only death benefits fall in the final year, and every policy issued has left by one of
    the four exits.  A maturity cells or a maturity kind would be describing a different
    contract.
    """
    a = kr_ci_anchor
    names = set(ci_insurance.Projection.cells) | set(ci_insurance.Projection.refs)
    for absent in ("pols_maturity", "claims_maturity", "policy_term", "maturity_age"):
        assert absent not in names, f"{absent}: this contract does not mature"
    t_end = a.proj_len() - 1
    assert a.claims(t_end) == pytest.approx(a.claims(t_end, "DEATH"), rel=1e-12)
    assert a.claims(t_end, "CI") == 0.0
    assert a.pols_lapse(t_end) == 0.0        # nobody survives to surrender
    assert a.pols_if(t_end + 1) == 0.0


# ---------------------------------------------------------------------------
# Modules that are off in the base run, asserted in both positions


def test_the_policy_loan_is_off_in_the_base_run_and_doubles_at_a_ci_event_when_on(
        ci_insurance, kr_ci_anchor):
    """Identically zero on the anchor; drawn on point 7 at duration 12.

    The draw is placed inside the 납입기간 on purpose, because that is the only
    configuration in which the carve-out's doubling of the limit is visible: the pre-CI
    room is 80% of the suppressed value and the post-CI room 80% of the full one.
    """
    a = kr_ci_anchor
    assert a.pol_loan_util() == 0.0
    assert all(a.pol_loan_draw(t) == 0.0 for t in range(a.proj_len() + 1))
    assert all(a.loan_pp(t) == 0.0 for t in range(a.proj_len() + 1))
    assert a.check_loan_roll_fwd() is True

    p = ci_insurance.Projection[7]
    d = 12 * p.pol_loan_year()                 # the 계약해당일, month-end 144
    assert d == 144
    assert p.loan_avail_pp(d) == pytest.approx(23945646.45, abs=WON)
    assert p.loan_avail_ci_pp(d) == pytest.approx(47891292.89, abs=WON)
    assert p.loan_avail_ci_pp(d) == pytest.approx(
        2.0 * p.loan_avail_pp(d), rel=1e-14)
    assert p.pol_loan_draw(d) == pytest.approx(11972823.22, abs=WON)
    assert all(p.pol_loan_draw(t) == 0.0
               for t in range(p.proj_len() + 1) if t != d)
    for t in range(d, d + 24):
        assert p.loan_pp(t + 1) == pytest.approx(
            p.loan_pp(t) * (1.04 ** (1.0 / 12.0)), rel=1e-12)
    assert p.check_loan_roll_fwd() is True
    assert p.check_pols_roll_fwd() is True     # the loan is a state, not a decrement


def test_the_fifty_percent_acceleration_form_is_a_different_product(ci_insurance):
    """a = 0.50 on points 3 and 8, and the residual floor then bites far later.

    On the 80% form the account has to pass KRW 19,050,000 for the floor to take over the
    KRW 20,000,000 nominal; on the 50% form it must pass KRW 47,600,000, which is one of
    the three reasons the composite takes the 80% fraction.  Both forms are in the shipped
    table, so the asymmetry is exercised rather than described.
    """
    for point_id in (3, 8):
        p = ci_insurance.Projection[point_id]
        assert p.accel_rate() == 0.50
        assert p.resid_rate() == pytest.approx(0.50, abs=1e-15)
        assert p.accel_benefit_pp(1) == pytest.approx(
            p.resid_nominal_pp(1), rel=1e-14)
        assert p.check_accel_complement() is True
        assert p.check_resid_floor() is True
        threshold = 0.50 * p.sum_assured() / 1.05
        crossing = min(t for t in range(p.proj_len() + 1)
                       if p.pol_val_pp(t) > threshold)
        assert crossing > 84
    half = ci_insurance.Projection[3]
    assert half.pol_val_pp(84) * 1.05 < 0.50 * half.sum_assured()


def test_the_three_suppression_grades_are_all_exercised(ci_insurance):
    """k = 0.00, 0.50 and 1.00 are all in the shipped table, and k = 0 pays nothing.

    On the 무해지 form the pre-CI surrender value is nil throughout the 납입기간, from
    which the FSS's finding that such a contract cannot support a policy loan at all
    during the payment period follows arithmetically.  The carve-out still holds: the
    post-CI value is the full one at every duration on every grade.
    """
    none_form = ci_insurance.Projection[4]
    assert none_form.cv_floor_ratio() == 0.0
    assert all(none_form.cv_pp(t) == 0.0
               for t in range(none_form.prem_period_mths()))
    assert all(none_form.loan_avail_pp(t) == 0.0
               for t in range(none_form.prem_period_mths()))
    assert none_form.cv_pp_ci(120) > 0.0
    assert none_form.claims(119, "LAPSE") == 0.0
    assert none_form.claims(119, "LAPSE_CI") > 0.0
    # The step is still there, at the 계약해당일 closing the 납입기간.
    assert none_form.cv_pp(none_form.prem_period_mths()) > 0.0
    assert none_form.check_cv_carve_out() is True

    ordinary = ci_insurance.Projection[3]
    assert ordinary.cv_floor_ratio() == 1.0
    assert {ordinary.cv_mult(t) for t in range(ordinary.proj_len() + 1)} == {1.0}
    for t in (24, 120, 239, 240):
        assert ordinary.cv_pp(t) == pytest.approx(ordinary.cv_std_pp(t), rel=1e-14)
        assert ordinary.cv_pp_ci(t) == pytest.approx(ordinary.cv_pp(t), rel=1e-14)
    assert ordinary.check_cv_carve_out() is True

    suppressed = ci_insurance.Projection[1]
    assert suppressed.cv_floor_ratio() == 0.50


def test_the_table_lapse_basis_runs_beside_the_principle_model(ci_insurance,
                                                               kr_ci_anchor):
    """The 표준형 duration curve on points 3, 6 and 8; the 로그-선형 원칙모형 elsewhere.

    Carrying both is the comparison the IFRS17 주요 계리가정 가이드라인 requires an
    insurer to disclose, and it is the reason the table survives on a product whose
    representative form does not use it.  No separate 완납 surrender spike is imposed on
    either basis: the eightfold step on the anchor is the guideline's own shape.
    """
    a = kr_ci_anchor
    assert a.lapse_basis() == "log_linear"
    assert a.lapse_rate(0) == 0.10
    assert a.lapse_rate(a.prem_period_mths() - 1) == pytest.approx(0.001, abs=1e-15)
    assert a.lapse_rate(a.prem_period_mths()) == 0.008
    assert a.lapse_rate_ult() == 0.008
    assert a.lapse_rate_ci(0) == pytest.approx(0.004, rel=1e-14)
    assert all(a.lapse_rate_ci(t) == a.lapse_rate_ci(0)
               for t in (1, 239, 240, 708))
    # Every one of those is the ANNUAL rate; the decrement applied is its conversion.
    assert a.lapse_rate_mth(0) == pytest.approx(1.0 - 0.9 ** (1 / 12), rel=1e-14)
    assert a.lapse_rate_ci_mth(0) == pytest.approx(
        1.0 - 0.996 ** (1 / 12), rel=1e-14)
    # The rate is level across the twelve months of a policy year, which is how the
    # guideline states it.
    assert all(a.lapse_rate(t) == a.lapse_rate(0) for t in range(12))
    assert a.lapse_rate(12) < a.lapse_rate(11)

    p = ci_insurance.Projection[3]
    assert p.lapse_basis() == "table"
    # The CSV is keyed by the contractual policy_year label, so month t reads the row
    # policy_year(t) and the file itself is untouched by the grid.
    assert [p.lapse_rate(12 * y) for y in range(7)] == [
        0.09, 0.07, 0.055, 0.045, 0.038, 0.032, 0.028]
    assert p.lapse_rate(348) == 0.028
    assert p.lapse_rate_ult() == 0.028
    assert p.lapse_rate_ci(0) == pytest.approx(0.014, rel=1e-14)
    # No spike at 납입완료 on the table basis: it is a duration curve and nothing else.
    assert p.lapse_rate(p.prem_period_mths() - 1) == p.lapse_rate(
        p.prem_period_mths())
    for point_id in (6, 8):
        assert ci_insurance.Projection[point_id].lapse_basis() == "table"


def test_the_best_estimate_levers_and_the_110_percent_floor(ci_insurance, kr_ci_anchor):
    """The base run is a valuation-basis run; point 9 is where the levers are exercised.

    ``mort_be_factor`` and ``ci_be_factor`` are 1.00 everywhere else, so the shipped
    projection runs on 예정위험률 carrying a 안전할증 nobody has sized against current
    Korean experience.  Point 9 moves both, halves the post-CI mortality multiple towards
    2.00 and runs the 110% residual floor [S3] publishes instead of 105%.
    """
    a = kr_ci_anchor
    assert a.mort_be_factor() == 1.0 and a.ci_be_factor() == 1.0
    for t in (0, 239, 708):
        assert a.mort_rate(t) == pytest.approx(a.mort_rate_base(t), rel=1e-14)
        assert a.ci_rate(t) == pytest.approx(a.ci_rate_base(t), rel=1e-14)
        assert a.mort_rate_mth(t) == pytest.approx(a.mort_rate_base_mth(t), rel=1e-14)
        assert a.ci_rate_mth(t) == pytest.approx(a.ci_rate_mth_base(t), rel=1e-14)

    p = ci_insurance.Projection[9]
    assert p.mort_be_factor() == 0.85 and p.ci_be_factor() == 0.75
    assert p.mort_ci_factor() == 2.0
    assert p.resid_floor_mult() == 1.10
    assert p.waiver_rate(0) == 0.0005
    assert p.mort_rate(0) == pytest.approx(0.85 * p.mort_rate_base(0), rel=1e-14)
    assert p.ci_rate(0) == pytest.approx(0.75 * p.ci_rate_base(0), rel=1e-14)
    assert p.mort_rate_ci(0) == pytest.approx(2.0 * p.mort_rate(0), rel=1e-14)
    # The pricing basis reads the tables straight, so the levers move no reserve.
    assert p.epv_ben(0) == pytest.approx(
        p.disc_factor_mth() * (
            p.ci_rate_mth_base(0) * p.accel_rate() * p.sum_assured()
            + (1 - p.ci_rate_mth_base(0)) * p.mort_rate_base_mth(0) * p.sum_assured()
            + p.ci_rate_mth_base(0) * p.epv_resid(1)
            + (1 - p.ci_rate_mth_base(0)) * (1 - p.mort_rate_base_mth(0))
            * p.epv_ben(1)),
        rel=1e-12)
    # The terminal rate is structural and survives every lever.
    assert p.mort_rate(p.proj_len() - 1) == 1.0
    assert p.resid_db_pp(360, 1) == pytest.approx(1.10 * p.pol_val_pp(360), rel=1e-14)
    assert p.check_resid_floor() is True


def test_the_waiver_runs_on_every_shipped_point_and_is_not_a_module(ci_insurance):
    """0.03% p.a. inside the 납입기간 on eight points and 0.05% on the ninth, never nil.

    On this product the 납입면제 is part of the main contract rather than an option, so
    it is deliberately not in the list of switchable modules.  What is modelled is the
    residual 장해 50%+ limb only: the CI limb fires with essentially every CI claim and is
    already inside the post-CI cohort, which pays nothing at all.
    """
    for point_id in ci_insurance.Data.model_point_table().index:
        p = ci_insurance.Projection[point_id]
        assert p.waiver_rate(0) > 0.0
        assert p.waiver_rate(p.prem_period_mths() - 1) > 0.0
        assert p.waiver_rate(p.prem_period_mths()) == 0.0
        # The rate is annual and the decrement its monthly conversion.
        assert p.waiver_rate_mth(0) == pytest.approx(
            1.0 - (1.0 - p.waiver_rate(0)) ** (1.0 / 12.0), rel=1e-14)
    a = ci_insurance.Projection[1]
    assert a.pols_waived(0) == 0.0
    assert a.pols_waived(1) > 0.0
    # A waived policy stays pre-CI and inside the surrender-value machinery.
    assert a.pols_waived(120) < a.pols_if_pre(120)
    assert a.pols_if_pay(120) == pytest.approx(
        a.pols_if_pre(120) - a.pols_waived(120), rel=1e-14)
    assert a.pols_if_pay(a.prem_period_mths()) == 0.0


# ---------------------------------------------------------------------------
# The [std] assumptions, read off the model


def test_the_std_scalar_assumptions_are_the_ones_the_notes_state(ci_insurance):
    """Every [std] scalar the notes and ``model.md`` tabulate, read off the References.

    These are not derived quantities: they are the choices the reference implementation
    makes where Korea publishes nothing, and each one is listed with a rationale in
    ``model.md`` under *Standardizations used*.  Asserting them here means a silent change
    to an assumption fails a test rather than quietly moving a result somewhere else in
    this module.
    """
    proj = ci_insurance.Projection
    assert proj.prem_int_rate == 0.025           # 예정이율, the chassis's
    assert proj.i_loan == 0.04                   # 예정이율 + 1.5%
    assert proj.loan_cap_rate == 0.8             # of the payable value [REG-R25 제33조]
    assert proj.net_prem_ratio == 0.8            # 연납순보험료 entering 별표 14
    assert proj.surr_chg_rate == 0.05            # 별표 14's 5%
    assert proj.surr_chg_coef_cap == 20          # the 해약공제계수 cap for 보장성
    assert proj.surr_chg_sa_rate == 0.01         # 10/1000 of the 보험가입금액
    assert proj.surr_chg_years_cap == 7          # 해약공제기간 [REG-R19]
    assert proj.ci_cover_end_age == 100          # the 100세 계약해당일
    assert proj.ci_wait_days == 90               # the 보장개시일, sourced four times
    assert proj.first_year_factor == 0.5         # the first-year 감액
    assert proj.breast_share_m == 0.005
    assert proj.breast_share_f == 0.268
    assert proj.lapse_ll_first == 0.1            # the 원칙모형's [std] start
    assert proj.lapse_ll_target == 0.001         # its supervisory endpoint
    assert proj.lapse_post_paidup == 0.008       # its post-완납 ultimate
    assert proj.lapse_ci_factor == 0.5
    assert proj.expense_acq == 500000.0
    assert proj.expense_maint == 5000.0          # per policy per MONTH
    assert proj.expense_claim == 300000.0
    assert proj.inflation_rate == 0.01
    assert proj.comm_init_rate == 0.8
    assert proj.comm_renewal_rate == 0.03
    assert proj.roll_fwd_tol == 1e-10
    assert proj.val_tol == 1e-08


def test_expense_inflation_compounds_over_the_whole_horizon(kr_ci_anchor):
    """1% compounds to 2.01 over 71 years, which is why the rate is not a Western one.

    Over a horizon this long the inflation assumption is not a second-order adjustment: a
    3% rate would compound to 7.9 and produce a different product rather than a stressed
    one.  There is no published Korean expense basis to anchor either figure.
    """
    a = kr_ci_anchor
    assert a.inflation_factor(0) == 1.0
    assert all(a.inflation_factor(t) == 1.0 for t in range(12))   # steps on 계약해당일
    assert a.inflation_factor(12) == pytest.approx(1.01, rel=1e-14)
    assert a.inflation_factor(a.proj_len() - 1) == pytest.approx(1.01 ** 70, rel=1e-14)
    assert a.inflation_factor(a.proj_len() - 1) == pytest.approx(
        INFLATION_TOTAL, abs=5e-3)
    assert 1.03 ** 70 == pytest.approx(7.92, abs=5e-3)


@pytest.mark.parametrize("name,setter,expected", [
    ("ci_wait_days", "ci_wait_days", SENS_NO_WAIT),
    ("first_year_factor", "first_year_factor", SENS_NO_FIRST_YEAR_CUT),
    ("lapse_ci_factor", "lapse_ci_factor", SENS_FULL_POST_CI_LAPSE),
])
def test_the_sensitivities_the_notes_quantify(name, setter, expected):
    """Three levers moved one at a time, against the notes' own figures.

    The notes quantify each of these in *Key sensitivities* and the numbers are what
    justify the treatment: the 90-day wait is worth 0.05% of the liability, so its
    *level* is immaterial while its mechanism is not; the first-year 감액 is worth
    KRW 149.44 on a male cell and is material only on a female one; and doubling post-CI
    lapse moves the whole liability by 0.6%, so the level does not matter much in
    aggregate while the sign of the behavioural story does.
    """
    values = {"ci_wait_days": 0, "first_year_factor": 1.0, "lapse_ci_factor": 1.0}
    model = mx.read_model(MODEL_DIR, name="CI_KR_S_sens_" + name)
    try:
        setattr(model.Projection, setter, values[setter])
        model.Projection.clear_all()
        total = model.Projection[1].result_cf()["net_cf"].sum()
        assert total == pytest.approx(expected, abs=0.02)
        assert total != pytest.approx(TOTALS["net_cf"], abs=1.0)
    finally:
        model.close()


def test_the_lapse_vector_is_a_third_of_the_liability():
    """A level 4% paying-period rate moves sum net_cf from -51.3m to -34.1m.

    Lapse is not a second-order assumption on this product: it removes lives before the
    acceleration reaches them, so a third of the whole undiscounted liability rests on a
    vector whose two endpoints are supervisory and whose interpolation is [std].  The
    comparison holds the 0.8% post-완납 ultimate fixed and moves only the paying-period
    shape, which is the part the guideline's functional form governs.
    """
    model = mx.read_model(MODEL_DIR, name="CI_KR_S_level_lapse")
    try:
        model.Projection.lapse_ll_first = 0.04
        model.Projection.lapse_ll_target = 0.04
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.lapse_rate(0) == 0.04 and p.lapse_rate(239) == 0.04
        assert p.lapse_rate(240) == 0.008         # the ultimate is untouched
        assert p.result_cf()["net_cf"].sum() == pytest.approx(
            SENS_LEVEL_4_PCT_LAPSE, abs=0.02)
        assert p.check_pols_roll_fwd() is True
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Inputs


def test_inputs_live_beside_the_model():
    """The four input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "ci_incidence_table.csv",
                "lapse_table.csv"}
    assert expected == {p.name for p in CSV_DIR.iterdir() if p.suffix == ".csv"}


def test_the_csvs_are_utf8_without_a_bom():
    """The provenance columns are Korean, so the encoding is load-bearing."""
    for name in ("model_point_table.csv", "mort_table.csv", "ci_incidence_table.csv",
                 "lapse_table.csv"):
        raw = (CSV_DIR / name).read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"{name} carries a BOM"
        raw.decode("utf-8")


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Four [S3] anchor rows and 188 rows of Makeham and ramp, each tagged.

    Korea publishes no life table this model could ship: 보험개발원 releases only 평균수명
    and 기대여명 from the 경험생명표.  So the file is a construction, and marking the rows
    is what stops it being mistaken for a published table.  The four anchors are the whole
    documentary basis of the mortality in this product.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith(("[S3]", "[std]")).all()

    anchors = table[table["provenance"].str.startswith("[S3]")]
    assert len(anchors) == 4
    assert sorted(zip(anchors["sex"], anchors["age"])) == [
        ("F", 20), ("M", 20), ("M", 40), ("M", 60)]
    assert anchors["provenance"].str.contains("ANCHOR").all()
    assert list(anchors[anchors["sex"] == "M"]["mort_rate"]) == [
        0.00051, 0.00068, 0.00290]
    assert list(anchors[anchors["sex"] == "F"]["mort_rate"]) == [0.00027]

    constructed = table[table["provenance"].str.startswith("[std]")]
    assert len(constructed) == len(table) - 4
    assert constructed["provenance"].str.contains(
        "Makeham|log-linear|0.5294|terminal age", regex=True).all()
    assert constructed["provenance"].str.contains("terminal age").sum() == 2
    assert table["age"].min() == 15 and table["age"].max() == OMEGA
    assert (table["sex"] == "M").sum() == (table["sex"] == "F").sum() == 96
    terminal = table[table["mort_rate"] >= 1.0]
    assert sorted(zip(terminal["sex"], terminal["age"])) == [("F", 110), ("M", 110)]
    # The female table is the male one scaled, which the notes name as a known defect.
    male = table[table["sex"] == "M"].set_index("age")["mort_rate"]
    female = table[table["sex"] == "F"].set_index("age")["mort_rate"]
    assert (female.loc[30] / male.loc[30]) == pytest.approx(0.5294, abs=5e-4)


def test_the_shipped_incidence_table_marks_its_own_provenance():
    """Eighteen [S3] anchors across three causes and two sexes; everything else [std].

    ``other`` and ``ltc`` have no anchor rows at all, which is the file's own statement
    that they are constructions: the first a flat 10.5% of the three headline rates, the
    second a placeholder above age 65.  The 참조순보험요율 carries no CI item, so this and
    the four mortality anchors are the entire published Korean basis for this product.
    """
    table = pd.read_csv(CSV_DIR / "ci_incidence_table.csv")
    assert list(table.columns) == ["sex", "age", "cause", "ci_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith(("[S3]", "[std]")).all()
    assert sorted(table["cause"].unique()) == sorted(CAUSE_ORDER)
    assert table["age"].min() == 15 and table["age"].max() == 100

    anchors = table[table["provenance"].str.startswith("[S3]")]
    assert len(anchors) == 18
    assert sorted(anchors["age"].unique()) == [20, 40, 60]
    assert sorted(anchors["cause"].unique()) == ["ami", "cancer", "stroke"]
    assert anchors["provenance"].str.contains("ANCHOR").all()
    assert set(anchors["sex"]) == {"M", "F"}

    for cause in ("other", "ltc"):
        rows = table[table["cause"] == cause]
        assert rows["provenance"].str.startswith("[std]").all(), cause
    # The ltc limb is nil below 65 and the largest single limb at the top of the grid.
    ltc = table[(table["cause"] == "ltc") & (table["sex"] == "M")].set_index("age")
    assert (ltc.loc[15:64, "ci_rate"] == 0.0).all()
    assert ltc.loc[65, "ci_rate"] > 0.0
    assert ltc.loc[100, "ci_rate"] > ltc.loc[65, "ci_rate"]


def test_the_lapse_table_is_the_comparison_curve_and_holds_no_spike():
    """Six duration rows and a level tail, all [std], with no 완납 surge folded in.

    The surge at 납입완료 on the suppressed forms is produced by the 원칙모형's own shape
    and is not a row of this table; folding it in would make a behavioural assumption look
    like a duration curve, and would put it on the 기본환급형 points too, where the
    contract has no step to provoke it.
    """
    table = pd.read_csv(CSV_DIR / "lapse_table.csv", index_col="policy_year")
    assert list(table.columns) == ["lapse_rate", "provenance"]
    assert list(table["lapse_rate"]) == [0.09, 0.07, 0.055, 0.045, 0.038, 0.032, 0.028]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith("[std]").all()
    assert table["lapse_rate"].max() < 0.10
    assert table["lapse_rate"].is_monotonic_decreasing
    columns = pd.read_csv(CSV_DIR / "model_point_table.csv").columns
    assert "lapse_spike" not in columns
    assert "lapse_basis" in columns


def test_the_model_point_table_covers_both_sexes_and_every_module():
    """Nine points: both sexes, the age and sum-assured envelopes, every switch moved.

    A model point table that exercised only the anchor's configuration would leave the
    optional machinery untested in the one position that matters, and this product has
    six switches — the acceleration fraction, the suppression grade, the first-year scope,
    the lapse basis, the residual floor multiple and the loan.
    """
    table = pd.read_csv(CSV_DIR / "model_point_table.csv", index_col="point_id")
    assert len(table) == 9
    assert list(table.index) == list(range(1, 10))
    assert set(table["sex"]) == {"M", "F"}
    assert table["issue_age"].min() == 15 and table["issue_age"].max() == 60
    assert table["sum_assured"].min() == 10000000
    assert table["sum_assured"].max() == 200000000
    assert set(table["prem_term"]) == {10, 20, 30}
    assert set(table["accel_rate"]) == {0.5, 0.8}
    assert set(table["cv_floor_ratio"]) == {0.0, 0.5, 1.0}
    assert set(table["first_year_scope"]) == {"breast", "all"}
    assert set(table["lapse_basis"]) == {"log_linear", "table"}
    assert set(table["resid_floor_mult"]) == {1.05, 1.1}
    assert set(table["mort_ci_factor"]) == {2.0, 3.0}
    assert (table["pols_if_init"] == 1).all()
    assert (table.loc[table["pol_loan_util"] > 0].index == [7]).all()
    assert "provenance" not in table.columns     # a configuration, not an assumption


def test_the_model_point_premiums_follow_the_documented_rule(ci_insurance):
    """The anchor's premium is sourced; the other eight are the anchor's loading applied.

    ``model.md`` states the rule under *Standardizations*: each non-anchor cell was the
    annual-step model's own net level premium grossed up by that model's 1.2399868
    loading, times the published form factor — 1.10224 for the 기본환급형, 1.000 for the
    저해지 and 0.937 [std] for the 무해지.  **The file is an input and did not change with
    the grid**, so the rule is asserted against the annual-equivalence premium the rule
    was written on, which this model still reproduces from its own EPVs.  Without this
    test a premium typed into the CSV by hand moves every cash flow on that point and
    nothing in the suite notices.
    """
    anchor = ci_insurance.Projection[1]
    assert anchor.premium_pp() == 12 * 306740.0        # the one sourced premium [S4]
    loading = 1.2399868045                             # the annual-step model's

    def annual_equivalence_net(p):
        """P on the footing the model point file was built on: annual, in advance."""
        v = p.disc_factor()
        resid, rb = 0.0, {p.proj_years(): 0.0}
        for y in range(p.proj_years() - 1, -1, -1):
            q = p.mort_rate_ci_base(12 * y)
            resid = v * (q * p.resid_rate() * p.sum_assured() + (1.0 - q) * resid)
            rb[y] = resid
        wait = p.ci_wait_factor()
        ben = 0.0
        for y in range(p.proj_years() - 1, -1, -1):
            t = 12 * y
            qc = p.ci_rate_base(t)
            if y == 0:
                qc = qc - (1.0 - wait) * (
                    p.ci_rate_at_age(p.age(0), "cancer")
                    + p.ci_rate_at_age(p.age(0), "ltc"))
            qd = p.mort_rate_base(t)
            ben = v * (qc * p.accel_rate() * p.sum_assured()
                       + (1.0 - qc) * qd * p.sum_assured()
                       + qc * rb[y + 1]
                       + (1.0 - qc) * (1.0 - qd) * ben)
        ann = 0.0
        for y in range(p.prem_period() - 1, -1, -1):
            t = 12 * y
            qc = p.ci_rate_base(t)
            if y == 0:
                qc = qc - (1.0 - wait) * (
                    p.ci_rate_at_age(p.age(0), "cancer")
                    + p.ci_rate_at_age(p.age(0), "ltc"))
            ann = 1.0 + v * (1.0 - qc) * (1.0 - p.mort_rate_base(t)) * ann
        return ben / ann

    assert annual_equivalence_net(anchor) == pytest.approx(
        P_NET_ANNUAL_STEP, abs=WON)
    form_factor = {0.0: 0.937, 0.5: 1.000, 1.0: 1.10224}
    for point_id in ci_insurance.Data.model_point_table().index:
        p = ci_insurance.Projection[point_id]
        expected = loading * form_factor[p.cv_floor_ratio()] * annual_equivalence_net(p)
        assert p.premium_pp() == pytest.approx(expected, rel=3e-4), point_id


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a same-schema file and the projection follows.

    This is the property the external-file layout buys, and it is exactly what a user
    holding a real 예정위험률 grid does with it: drop it in as a CSV, change no formula.
    Doubling the incidence table doubles the **annual** first-event rate, which is the
    quantity the file holds; the monthly decrement it converts to is more than doubled,
    because doubling a probability more than doubles the force behind it.
    """
    src = CSV_DIR / "ci_incidence_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "age", "cause"])
    doubled["ci_rate"] = (doubled["ci_rate"] * 2).clip(upper=1.0)

    model = mx.read_model(MODEL_DIR, name="CI_KR_S_swap")
    try:
        alt_name = "ci_incidence_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].ci_rate(0)
            model.Data.ci_incidence_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].ci_rate(0) == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Docstrings and the round trip


def test_the_docstrings_describe_the_current_structure(ci_insurance):
    """Specifics a reader relies on, asserted so they cannot go stale silently."""
    doc = flat(ci_insurance.doc)
    assert "mechanics demonstration" in doc or "demonstrate is the acceleration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "two payments at two dates on one sum assured" in doc
    assert "Data" in doc and "Projection" in doc

    proj = flat(ci_insurance.Projection.doc)
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    assert "보험나이" in proj                     # the age basis, per the registry
    for cells in ("proj_len", "model_point", "pols_if_ci_at", "resid_db_pp",
                  "cv_pp_ci", "accel_benefit_pp", "annuity_due", "ci_cover_end"):
        assert cells in proj, cells
    assert "transition" in proj and "never adds cover" in proj
    assert "two exits" in proj

    data = flat(ci_insurance.Data.doc)
    assert "TradLife_A" in data                  # the layout it follows
    for cells in ("input_dir", "model_point_table", "mort_table",
                  "ci_incidence_table", "lapse_table"):
        assert cells in data, cells


def test_the_projection_docstring_describes_the_shipped_model_points(ci_insurance):
    """The module summary must match the model point table it describes.

    A docstring that names a module the table does not exercise is worse than none: it is
    the one place a reader looks to find out what the shipped points cover.
    """
    proj = flat(ci_insurance.Projection.doc)
    table = ci_insurance.Data.model_point_table()
    assert "model point 7 at duration 12" in proj
    assert int(table.loc[7, "pol_loan_year"]) == 12
    assert float(table.loc[7, "pol_loan_util"]) == 0.5
    assert "model point 4" in proj
    assert table.loc[4, "first_year_scope"] == "all"
    assert "model point 9" in proj
    assert float(table.loc[9, "resid_floor_mult"]) == 1.1


def test_the_notes_and_the_model_agree_on_the_worked_example_cell():
    """The technical notes print the anchor's own numbers, not a spreadsheet's.

    Three figures are spot-checked in the notes' own text — the net cash flow total, the
    post-CI death benefit total and the 표준해약공제액 — because the worked example is
    only worth having if the document and the model cannot drift apart.  The whole table
    is asserted cell by cell above; this asserts that the *document* carries it.
    """
    notes = io.open(CSV_DIR / "technical-notes.md", encoding="utf-8").read()
    assert "−₩51,625,819.94" in notes
    assert "36,093,568.46" in notes
    assert "₩3,944,704" in notes
    assert "178.7102998490" in notes
    assert "0.4273447323" in notes


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    model = mx.read_model(MODEL_DIR, name="CI_KR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in CSV_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="CI_KR_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.claims(t, "CI") == pytest.approx(row[2], abs=WON)
            assert anchor.net_cf(t) == pytest.approx(row[10], abs=WON)
        assert anchor.cv_pp(240) == pytest.approx(
            WORKED_EXAMPLE_VALUES[239][3], abs=WON)
        assert anchor.prem_net_level_mth_pp() == pytest.approx(P_NET_MTH, abs=WON)
        assert "Notes symbol" in reread.Projection.doc
        assert {c for c in reread.Projection.cells
                if c.startswith("check_") and not c.endswith("_resid")} == CHECK_CELLS
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
