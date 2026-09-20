"""Golden and structural tests for WholeLife_KR_S.

The golden values are the worked example in ``products/whole_life/technical-notes.md``
("Worked example"), which projects the anchor cell: 남자, 보험나이 40 on a **보험나이**
basis, 보험가입금액 ₩100,000,000 (1억원), 보험기간 종신, 납입기간 20년, the
저해지환급형 (*jeohaeji hwangeup hyeong*, low-surrender-value) form at ``k = 0.50``, and
an annual 영업보험료 of ₩2,776,140.  They are hard-coded here rather than pickled so that
a reviewer can lay the module beside the notes and compare by eye.

Tolerances follow the precision the notes display: money to the won's second decimal,
in-force to six decimals, mortality rates to eight and lapse rates and decrement totals to
ten.

**The grid is monthly.**  ``t`` is the 0-based policy-**month** index: ``t = 0`` is the
first policy month, period ``t`` runs from month-end ``t`` to month-end ``t + 1``, the frame
is ``range(proj_len())`` with ``proj_len() = 12 x proj_years()``, and the contractual policy
year is the derived label ``policy_year(t) = t // 12 + 1``.  The anchor projects 912 rows.
Contract terms stay in years — the 납입기간, the 해약공제기간, the 보험계약대출 drawdown year
and the 감액 year — with month-count companions where the grid needs one, and this module
asserts both.

**Two indices.**  The value cells — ``pol_val_pp``, ``surr_chg_pp``, ``cv_std_pp``,
``cv_pp``, ``cv_susp_pp``, ``cum_prem_pp``, ``refund_ratio``, ``bonus_pp``, ``cv_mult``,
``sa_factor``, ``loan_pp`` — are indexed by the **month-end** ``d``, ``d = 0`` at issue, and
a 계약해당일 is ``d = 12y``, which is where a published 해지환급금 grid is quoted.  So the
cash-flow goldens below are keyed by the month and the surrender-value goldens by the
month-end, and a row of ``result_val()`` at month ``t`` carries the month-end ``d = t + 1``
that closes it.

**What the grid moved.**  The sourced decrement basis stays annual and the monthly
decrements are its ``1 - (1 - q)^(1/12)`` conversions, so the in-force at every 계약해당일
reproduces the annual-step model this replaced —
:func:`test_the_monthly_decrements_reproduce_the_annual_survivorship` is that check, and
:data:`ANNIVERSARY_INFORCE` carries the values.  The **계약자적립액 does move, by about
1.2%**, because the account now accrues monthly on a 월납순보험료 struck by monthly
equivalence, which is what 감독규정 제7-66조제1항제4호 describes and what an annual grid could
only approximate under 제7-65조제2항's separate permission.  That is the conversion's
substantive gain and it is asserted rather than absorbed.

This is the library's **savings/protection chassis** — four other products inherit the
account recursion, the surrender value, the suppressed forms, the policy loan and the
premium waiver from it — so the module carries a good deal more than a cash-flow
comparison.  Every entry in the notes' **Known modeling pitfalls** list earns a test named
after it, because each is a way an implementation can look right and be wrong:

* the 무해지 / 저해지 cliff is a **step** and not a ramp, and on a 전기납 contract it never
  happens at all;
* a surrender in policy year ``m`` is paid on the **full** value, and both values exist at
  that anniversary;
* there is **one** 계약자적립액 and **one** multiplier on it, not two account runs;
* the step is **not** the surrender charge running off — the 해약공제기간 is capped at
  seven years and died thirteen years earlier;
* ``P`` and ``P₂₀`` are different annuities and coincide only when ``m = 20``;
* the 보험가입금액 entering the 표준해약공제액 is taken **before** any 감액;
* premiums stop at 납입완료 and **nothing else does**;
* the 보험계약대출 does not exist on a 무해지 contract during 납입기간;
* every payment is floored at zero, and on this product the floor bites;
* the 유지보너스 cannot be booked without the supervisor's ≥ 30 point lapse spike;
* the prospective identity is **withdrawn**, not forced, on a 금리연동형 point;
* ``pol_val_pp`` is a 계약자적립액, not a 책임준비금, and never a cash flow;
* waived premiums count as **paid**, and a waived policy is a state rather than a
  discounted premium;
* lapse in Korea is **behavioural**, not funded — there is no 자동대출납입 to import from
  ``jplib``;
* 감액완납 and 연장정기보험 are not Korean features on the retrieved evidence;
* a refused claim is not a zero payment; and
* the 환급률 test and the value test are not the same test.

The optional modules are asserted in **both** positions — off in the base run, and
switched on — because a module that is only ever exercised off is machinery nobody has
run.  ``test_model_conventions_kr.py`` owns the single sweep that calls every ``check_*``
on every model point of every model, so this module does not repeat it; what it does
instead is name the nine checks, which a generic sweep cannot do, and rebuild the two
roll-forward identities from the decrements rather than from the recursions that produced
them.
"""
import math
import re
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import model_path

MODEL_DIR = model_path("WholeLife_KR_S")

WON = 0.005           # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.
MORT = 5e-9           # mortality rates displayed to 8 d.p.
PROB = 5e-11          # lapse rates and decrement totals displayed to 10 d.p.
RATIO = 5e-7          # 환급률 displayed to 6 d.p.
TRACE = 5e-6          # the hand traces' full-precision intermediates
TOTAL = 5e-6          # the undiscounted totals, displayed to 6 d.p.


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


def product_copy(tmp_path, name):
    """A throwaway copy of the whole product directory, model and input CSVs together.

    The inputs are **external files** in the model folder's parent, so a test that wants
    to move an assumption has to move a file, and moving one inside the repository would
    leave an orphan CSV that ``test_model_conventions_kr.py`` fails on.  Copying the
    directory instead keeps every such test off the shipped tree entirely;
    ``input_dir()`` resolves to ``_model.path.parent`` at run time, so the copy reads its
    own CSVs with no formula changed.
    """
    dest = tmp_path / "whole_life"
    shutil.copytree(MODEL_DIR.parent, dest,
                    ignore=shutil.ignore_patterns("__pycache__"))
    return mx.read_model(dest / MODEL_DIR.name, name=name)


# ---------------------------------------------------------------------------
# The notes' worked example, hard-coded
#
# "Derived scalars, at full precision" — the closed-form quantities the whole projection
# hangs on.  Two of them are the point of the anchor: P20 equals P only because m = 20.
A40 = 0.332153184440                 # A(40) on the 예정이율 and the shipped table
ANNUITY_DUE_40_20 = 15.766511588794  # a-double-dot(40, 20)
P_NET = 2106700.5378440050           # 연납순보험료, P = SA A(40) / a(40, 20), the 별표 14 quantity
P_NET_MTH = 179777.0581452671        # 월납순보험료, what the monthly account consumes
P_NET_20YR = 2106700.5378440050      # the same annual premium on the 별표 14 20년납 footing
G_GROSS = 2776140.0                  # 영업보험료 p.a., sourced [S1] [S4]
G_GROSS_MTH = 231345.0               # the published monthly figure the annual column is 12x
G_CALC = 2776167.8347600726          # the model's own [std] loading rule, annual
SURR_CHG_CAP = 3106700.5378440050    # 표준해약공제액 = P20 + 1% of SA, 별표 14
ACQ_COST = 3106700.5378440050        # 계약체결비용, set at the cap [std]
COMM_INIT = 2019355.3495986033       # 0.65 x 계약체결비용, inside the 제4-32조제5항 cap
ACQ_EXPENSE = 1087345.1882454017     # the residual booked as acquisition expense
PROJ_YEARS = 76                      # T_y = omega - x + 1 = 115 - 40 + 1
PROJ_LEN = 912                       # T = 12 T_y, the months projected
SURR_CHG_PERIOD = 7                  # n_sc = min(m, 7) years, 제7-66조제1항제2호
SURR_CHG_PERIOD_MTHS = 84            # the same in months, which is what surr_chg_pp runs off
PREM_PERIOD_MTHS = 240               # 12m, the 납입기간 in months

# "The anchor's mortality and lapse rates, policy years 1 ... 25".  The **annual** rates are
# the sourced quantities — both disclosed 적용위험률 grids are annual by age [S2] [S8] and
# the FSS 원칙모형 lapse vector is annual by 경과기간 [REG-R27] — and the monthly decrements
# beside them are their `1 - (1 - q)^(1/12)` conversions, which are what the roll-forward
# applies.  Each row is read at the first month of its policy year, `t = 12 (y - 1)`, and
# holds for all twelve.
# y: (attained 보험나이 = 39 + y, mort_rate, mort_rate_mth, lapse_rate, lapse_rate_mth)
WORKED_EXAMPLE_RATES = {
    1:  (40, 0.00085000, 0.0000708609, 0.1000000000, 0.0087416110),
    2:  (41, 0.00092944, 0.0000774863, 0.0784759970, 0.0067873987),
    3:  (42, 0.00101630, 0.0000847311, 0.0615848211, 0.0052828967),
    4:  (43, 0.00111127, 0.0000926530, 0.0483293024, 0.0041195089),
    5:  (44, 0.00121513, 0.0001013173, 0.0379269019, 0.0032168852),
    6:  (45, 0.00132869, 0.0001107917, 0.0297635144, 0.0025147858),
    7:  (46, 0.00145286, 0.0001211524, 0.0233572147, 0.0019675882),
    8:  (47, 0.00158864, 0.0001324832, 0.0183298071, 0.0015404689),
    9:  (48, 0.00173710, 0.0001448737, 0.0143844989, 0.0012066846),
    10: (49, 0.00189944, 0.0001584246, 0.0112883789, 0.0009456007),
    11: (50, 0.00207696, 0.0001732450, 0.0088586679, 0.0007412367),
    12: (51, 0.00227106, 0.0001894523, 0.0069519280, 0.0005811815),
    13: (52, 0.00248330, 0.0002071776, 0.0054555948, 0.0004557737),
    14: (53, 0.00271538, 0.0002265638, 0.0042813324, 0.0003574797),
    15: (54, 0.00296914, 0.0002477657, 0.0033598183, 0.0002804169),
    16: (55, 0.00324662, 0.0002709551, 0.0026366509, 0.0002199869),
    17: (56, 0.00355003, 0.0002963183, 0.0020691381, 0.0001725919),
    18: (57, 0.00388180, 0.0003240603, 0.0016237767, 0.0001354155),
    19: (58, 0.00424458, 0.0003544050, 0.0012742750, 0.0001062517),
    20: (59, 0.00464125, 0.0003875960, 0.0010000000, 0.0000833716),
    21: (60, 0.00507500, 0.0004239036, 0.0080000000, 0.0006691237),
    22: (61, 0.00551816, 0.0004610138, 0.0080000000, 0.0006691237),
    23: (62, 0.00600277, 0.0005016124, 0.0080000000, 0.0006691237),
    24: (63, 0.00653292, 0.0005460469, 0.0080000000, 0.0006691237),
    25: (64, 0.00711315, 0.0005947038, 0.0080000000, 0.0006691237),
}

# "The first policy year of the base run, and the milestone months", per policy issued,
# income-positive, two decimals.  Thirteen rows carry the whole of policy year 1 and the
# turn into year 2, where the expense inflation factor steps and the renewal commission
# starts; the milestones are the months around 납입완료 at `t = 239 / 240` and four rows
# spread over the sixty years after it.
# t: (pols_if, premiums, claims_death, claims_lapse, claim_expenses, expenses,
#     commissions, net_cf)
#
# ``expenses`` is acquisition plus maintenance plus the premium-related component; the
# claim handling expense stands beside it in its own column, which is the settled column
# vocabulary of the six libraries.  ``claims_reduction`` is identically zero on this cell
# and is asserted separately.
WORKED_EXAMPLE = {
    0:   (1.000000, 231345.00,  7086.09,      0.00, 21.26, 1096972.09, 2019355.35, -2892089.79),
    1:   (0.991188, 229306.42,  7023.65,      0.00, 21.07,    9542.07,       0.00,   212719.63),
    2:   (0.982454, 227285.81,  6961.76,      0.00, 20.89,    9457.99,       0.00,   210845.18),
    3:   (0.973797, 225283.00,  6900.42,      0.00, 20.70,    9374.64,       0.00,   208987.24),
    4:   (0.965216, 223297.84,  6839.61,      0.00, 20.52,    9292.04,       0.00,   207145.67),
    5:   (0.956710, 221330.17,  6779.34,      0.00, 20.34,    9210.16,       0.00,   205320.34),
    6:   (0.948280, 219379.84,  6719.60,      0.00, 20.16,    9129.00,       0.00,   203511.08),
    7:   (0.939924, 217446.70,  6660.39,      0.00, 19.98,    9048.55,       0.00,   201717.77),
    8:   (0.931641, 215530.59,  6601.70,      0.00, 19.81,    8968.82,       0.00,   199940.27),
    9:   (0.923432, 213631.37,  6543.53,      0.00, 19.63,    8889.79,       0.00,   198178.42),
    10:  (0.915295, 211748.88,  6485.87,      0.00, 19.46,    8811.45,       0.00,   196432.10),
    11:  (0.907229, 209882.98,  6428.71,      0.00, 19.29,    8733.81,       0.00,   194701.17),
    12:  (0.899235, 208033.52,  6967.84,      0.00, 20.90,    8746.77,    6241.01,   186057.00),
    60:  (0.708946, 164011.16,  7854.53,   9201.72, 23.56,    7193.89,    4920.33,   134817.12),
    120: (0.637513, 147485.53, 11044.60,   5535.20, 33.13,    6835.34,    4424.57,   119612.69),
    228: (0.597934, 138328.95, 23175.67,   1223.61, 69.53,    7121.96,    4149.87,   102588.32),
    239: (0.594843, 137614.06, 23055.90,   2579.03, 69.17,    7085.15,    4128.42,   100696.39),
    240: (0.594563,      0.00, 25203.75,  20722.80, 75.61,    4417.45,       0.00,   -50419.61),
    241: (0.593914,      0.00, 25176.21,  20734.74, 75.53,    4412.62,       0.00,   -50399.10),
    276: (0.570828,      0.00, 31169.90,  21116.60, 93.51,    4500.69,       0.00,   -56880.71),
    468: (0.402873,      0.00, 91539.53,  19702.26, 274.62,   4360.59,       0.00,  -115877.00),
    708: (0.067131,      0.00, 114443.72,  4053.15, 343.33,   1079.70,       0.00,  -119919.90),
    911: (0.000000,      0.00,      4.21,      0.00, 0.01,       0.00,       0.00,       -4.22),
}

# "Surrender values at the same month-ends".  Keyed by the **month-end** ``d``, ``d = 0`` at
# issue: the value on the row of month ``t`` is the one at ``d = t + 1``, the month-end that
# closes it.  A 계약해당일 is ``d = 12y``, which is where a published 해지환급금 grid is
# quoted; ``d = 1`` and ``d = 6`` are here because a monthly account has values **inside** the
# policy year that an annual grid could not state at all.
# d: (pol_val_pp, surr_chg_pp, cv_std_pp, cv_pp, cv_susp_pp, cum_prem_pp, refund_ratio)
WORKED_EXAMPLE_VAL = {
    1:   (  173073.54, 3069716.01,        0.00,        0.00,        0.00,   231345.00, 0.000000),
    6:   ( 1043988.88, 2884793.36,        0.00,        0.00,        0.00,  1388070.00, 0.000000),
    12:  ( 2101396.55, 2662886.18,        0.00,        0.00,        0.00,  2776140.00, 0.000000),
    24:  ( 4249377.45, 2219071.81,  2030305.64,  1015152.82,  1015152.82,  5552280.00, 0.182835),
    36:  ( 6444786.36, 1775257.45,  4669528.91,  2334764.46,  2334764.46,  8328420.00, 0.280337),
    48:  ( 8688485.75, 1331443.09,  7357042.66,  3678521.33,  3678521.33, 11104560.00, 0.331262),
    60:  (10981357.96,  887628.73, 10093729.24,  5046864.62,  5046864.62, 13880700.00, 0.363589),
    72:  (13324313.14,  443814.36, 12880498.78,  6440249.39,  6440249.39, 16656840.00, 0.386643),
    84:  (15718292.14,       0.00, 15718292.14,  7859146.07,  7859146.07, 19432980.00, 0.404423),
    96:  (18164272.12,       0.00, 18164272.12,  9082136.06,  9082136.06, 22209120.00, 0.408937),
    108: (20663275.63,       0.00, 20663275.63, 10331637.81, 10331637.81, 24985260.00, 0.413509),
    120: (23216376.79,       0.00, 23216376.79, 11608188.39, 11608188.39, 27761400.00, 0.418141),
    132: (25824712.38,       0.00, 25824712.38, 12912356.19, 12912356.19, 30537540.00, 0.422836),
    144: (28489495.44,       0.00, 28489495.44, 14244747.72, 14244747.72, 33313680.00, 0.427595),
    180: (36836090.86,       0.00, 36836090.86, 18418045.43, 18418045.43, 41642100.00, 0.442294),
    216: (45745067.40,       0.00, 45745067.40, 22872533.70, 22872533.70, 49970520.00, 0.457721),
    228: (48848924.03,       0.00, 48848924.03, 24424462.02, 24424462.02, 52746660.00, 0.463052),
    239: (51755813.04,       0.00, 51755813.04, 25877906.52, 25877906.52, 55291455.00, 0.468027),
    240: (52023973.59,       0.00, 52023973.59, 52023973.59, 26011986.79, 55522800.00, 0.936984),
    241: (52110834.07,       0.00, 52110834.07, 52110834.07, 26055417.03, 55522800.00, 0.938548),
    252: (53080662.78,       0.00, 53080662.78, 53080662.78, 26540331.39, 55522800.00, 0.956016),
    276: (55226450.40,       0.00, 55226450.40, 55226450.40, 27613225.20, 55522800.00, 0.994663),
    288: (56314255.07,       0.00, 56314255.07, 56314255.07, 28157127.53, 55522800.00, 1.014255),
    300: (57411045.18,       0.00, 57411045.18, 57411045.18, 28705522.59, 55522800.00, 1.034008),
    360: (63000180.99,       0.00, 63000180.99, 63000180.99, 31500090.50, 55522800.00, 1.134672),
    480: (74269001.52,       0.00, 74269001.52, 74269001.52, 37134500.76, 55522800.00, 1.337631),
    720: (92405944.03,       0.00, 92405944.03, 92405944.03, 46202972.01, 55522800.00, 1.664288),
    900: (98673877.93,       0.00, 98673877.93, 98673877.93, 49336938.96, 55522800.00, 1.777178),
    912: (       0.00,       0.00,        0.00,        0.00,        0.00, 55522800.00, 0.000000),
}

# The in-force at each 계약해당일 of the annual-step model this one replaced, which the
# monthly roll-forward must reproduce: twelve monthly exits at `1 - (1 - q)^(1/12)` compound
# to the year's annual rate, so the anniversary survivorship is unchanged and only the
# exposure inside the year has moved.
ANNIVERSARY_INFORCE = {
    12: 0.899235,
    60: 0.7089461981788684,
    120: 0.6375133511220556,
    240: 0.5945633056475697,
    480: 0.38888872710378286,
    720: 0.054177838185085904,
}

# "Undiscounted totals per policy issued, t = 0 ... 911".
TOTALS = {
    "pols_if": 338.873413,
    "premiums": 37680384.400292,
    "claims_death": 50620740.892497,
    "claims_lapse": 9294573.995749,
    "claims_reduction": 0.000000,
    "claim_expenses": 151862.222677,
    "expenses": 4604344.667170,
    "commissions": 3070402.823829,
    "net_cf": -30061540.201631,
}
SUM_DEATHS = 0.5062074089
SUM_SURRENDERS = 0.4937925911
DEATHS_AFTER_YEAR_40 = 0.352136       # of 0.506207, from t = 480 — the horizon sensitivity
NET_CF_WHILE_PAYING = 27631707.90     # t = 0 ... 239, the 240 premium-paying months
NET_CF_AFTER_PAYING = -57693248.10    # t = 240 ... 911
CLIFF_SWING = 151116.00               # net_cf(239) - net_cf(240), a month either side

# "The flat basis, and the disclosure the guidance obliges" — the identical anchor cell
# re-run on the level 4% comparison vector the 2024-11 계리가정 decision requires an
# insurer to disclose against the 원칙모형 [REG-R27].
FLAT_BASIS = {
    "lapse_rate_228": 0.04,
    "lapse_rate_239": 0.04,
    "lapse_rate_240": 0.04,
    "claims_lapse_228": 36851.71,
    "claims_lapse_239": 74889.03,
    "claims_lapse_240": 74727.62,
    "net_cf_239": -1267.84,
    "pols_if_239": 0.424042,
    "sum_claims_lapse": 23294606.96,
    "sum_claims_death": 17702650.52,
    "sum_net_cf": -10160522.69,
}

# "Calibration against the published grid" — the model's own 표준형 surrender value
# against DB생명's published 1종 표준형 run at the identical cell [S4].  Keyed by the
# **policy year**, because that is what a published 해지환급금 grid is quoted at; the model
# is read at the 계약해당일 ``d = 12y``.
# y: (model cv_std_pp at d = 12y, published 해지환급금, ratio)
CALIBRATION = {
    1:  (       0.00,         0, None),
    3:  ( 4669528.91,   5087095, 0.9179),
    5:  (10093729.24,  10940547, 0.9226),
    10: (23216376.79,  25283000, 0.9183),
    15: (36836090.86,  40501000, 0.9095),
    20: (52023973.59,  57838000, 0.8995),
    40: (74269001.52,  86326000, 0.8603),
    60: (92405944.03, 104604000, 0.8834),
}

# "The other nine model points, and what each one is for" — the signature number of each.
POINT_2_CROSSING = 29                 # the policy year the twin's 환급률 crosses 100% at
POINT_2_REFUND_20 = 0.843286
POINT_3_REFUND_20 = 1.081135          # the 무해지 form's, above the twin's
POINT_4_PROJ_LEN = 1032               # F30 to omega = 115, in months
POINT_5_PREM_PERIOD = 51              # 전기납: m is the whole projection, in years
POINT_6_LOAN_DRAW = 8265310.25        # 80% of the suppressed value at the 계약해당일 d = 108
POINT_6_LOAN_END = 114044264.36       # above the ₩100,000,000 sum assured well before the end
POINT_7_WAIVED_228 = 0.042858         # the month t = 228, the start of policy year 20
POINT_8_LAPSE_SPIKE_MTH = 0.3000833715521976   # the one month, t = 83, carrying the spike
POINT_8_REFUND_7 = 0.972448
POINT_9_PROSP_GAP = 0.091163          # pol_val_pp(240) / prosp_val_pp(240) - 1, at d = 240
POINT_10_REDUCTION = 165583123.99     # the 감액 of month t = 179, at the 계약해당일 d = 180
POINT_10_NET_CF_179 = -166799687.05

# The nine identities this model publishes.  Named here because a generic sweep can call
# whatever it discovers but cannot notice a check that has stopped being discovered.
CHECK_CELLS = {
    "check_acq_cost_cap",
    "check_cv_cliff",
    "check_decrement_sum",
    "check_loan_roll_fwd",
    "check_net_cf",
    "check_pol_val_prosp",
    "check_pol_val_roll_fwd",
    "check_pols_roll_fwd",
    "check_surr_chg_cap",
}

# The [std] scalar assumptions the notes state, as Projection References.
STD_SCALARS = {
    "prem_int_rate": 0.025,           # 예정이율, centre of a 2.25%-2.75% disclosed band
    "min_guar_rate": 0.0075,          # 최저보증이율, verbatim in the one full 약관 [S5]
    "prem_loading": 1.4642,           # calibrated once on the 표준형 anchor [S4]
    "surr_chg_prem_rate": 0.05,       # 별표 14: 연납순보험료 x 5%
    "surr_chg_coef": 20,              # 별표 14 주2: 해약공제계수, 보험기간 capped at 20
    "surr_chg_sa_rate": 0.01,         # 별표 14: 보험가입금액 x 10/1000
    "surr_chg_prem_years": 20,        # 별표 14 주3: the 20년납 footing for P20
    "surr_chg_max_years": 7,          # 제7-66조제1항제2호: 해약공제기간 capped at 7년
    "acq_cost_ratio": 1.0,            # 계약체결비용 set at the 표준해약공제액
    "acq_cost_tolerance": 1.4,        # 제7-45조제11항 disclosure tolerance
    "comm_init_share": 0.65,          # first-year share of the 계약체결비용
    "comm_cap_rate": 1.0,             # 제4-32조제5항: within the first year's premium
    "comm_renewal_rate": 0.03,        # renewal commission, years 2 ... m
    "expense_maint_pp": 5000.0,       # 계약관리비용 per policy per month
    "expense_maint_prem_rate": 0.02,  # 유지관련비용 on premium collected
    "expense_claim_pp": 300000.0,     # claim handling expense per death claim
    "inflation_rate": 0.02,           # the Bank of Korea target
    "loan_spread": 0.015,             # 보험계약대출이율 = 적용이율 + 1.5%
    "loan_limit": 0.8,                # 80% of the *payable* 해약환급금
    "lapse_bonus_spike": 0.3,         # 「30% 이상」 at a 유지보너스 date [REG-R27]
    "roll_fwd_tol": 1e-10,
    "val_tol": 1e-07,
}


# ---------------------------------------------------------------------------
# The worked example


def test_worked_example_derived_scalars(kr_whole_life_anchor):
    """The notes' table of derived scalars, at the precision it prints them.

    Every cash flow in the projection hangs on these seven numbers, and none of them is a
    model point input: ``P`` comes from equivalence, ``SC*`` from 별표 14, and the
    acquisition and commission split from two published caps.  A change in any of them
    moves the whole worked example, so they are asserted here as scalars before a single
    row of the table is compared.
    """
    a = kr_whole_life_anchor
    assert a.omega_age() == 115
    assert a.proj_years() == PROJ_YEARS == 115 - 40 + 1
    assert a.proj_len() == PROJ_LEN == 12 * PROJ_YEARS
    assert a.prem_period() == 20 and a.prem_end() == 20
    assert a.prem_period_mths() == PREM_PERIOD_MTHS == 240
    assert a.surr_chg_period() == SURR_CHG_PERIOD
    assert a.surr_chg_period_mths() == SURR_CHG_PERIOD_MTHS == 12 * SURR_CHG_PERIOD
    assert a.epv_death(40) == pytest.approx(A40, abs=5e-12)
    assert a.annuity_due(40, 20) == pytest.approx(ANNUITY_DUE_40_20, abs=5e-12)
    assert a.prem_net_level_pp() == pytest.approx(P_NET, abs=TRACE)
    assert a.prem_net_level_pp() == pytest.approx(
        a.sum_assured() * A40 / ANNUITY_DUE_40_20, rel=1e-10)
    # The 월납순보험료 is struck by **monthly** equivalence and is not P / 12: a monthly
    # equivalence discounts eleven of each year's twelve instalments and exposes them to the
    # year's mortality, so 12 P^m sits 2.4% above the 연납순보험료.  The account consumes
    # P^m; 별표 14 and the loading rule consume P.
    assert a.prem_net_level_mth_pp() == pytest.approx(P_NET_MTH, abs=TRACE)
    assert a.prem_net_level_mth_pp() == pytest.approx(
        a.sum_assured() * a.epv_death_mth(0) / a.annuity_due_mth(0, 240), rel=1e-12)
    assert a.prem_net_level_mth_pp() > P_NET / 12.0
    assert 12 * a.prem_net_level_mth_pp() / P_NET == pytest.approx(1.024, abs=5e-4)
    assert a.premium_pp() == G_GROSS
    assert a.premium_mth_pp() == G_GROSS_MTH == G_GROSS / 12.0
    assert a.prem_gross_calc_pp() == pytest.approx(G_CALC, abs=TRACE)
    assert a.surr_chg_cap_pp() == pytest.approx(SURR_CHG_CAP, abs=TRACE)
    assert a.acq_cost_pp() == pytest.approx(ACQ_COST, abs=TRACE)
    assert a.comm_init_pp() == pytest.approx(COMM_INIT, abs=TRACE)
    assert a.acq_cost_pp() - a.comm_init_pp() == pytest.approx(ACQ_EXPENSE, abs=TRACE)
    assert a.acc_int_rate() == 0.025
    assert a.acc_int_rate_mth() == pytest.approx(1.025 ** (1 / 12) - 1, rel=1e-15)
    assert (1 + a.acc_int_rate_mth()) ** 12 == pytest.approx(1.025, rel=1e-14)
    assert a.loan_int_rate() == pytest.approx(0.04, rel=1e-12)
    assert (1 + a.loan_int_rate_mth()) ** 12 == pytest.approx(1.04, rel=1e-14)


def test_the_model_loading_rule_reproduces_the_sourced_premium_without_driving_it(
        whole_life):
    """G is an input and ``prem_gross_calc_pp`` is a fit, and the notes report the gap.

    The anchor's premium is a sourced number — ₩257,050 a month for exactly this cell
    [S4], annualized and scaled by the 90.0% suppression price [S1] — and it must stay
    one.  ``prem_loading`` was calibrated once on the 표준형 twin, so the *same* relative
    error appears on both cells; a model that quietly used the calculated premium instead
    would move every cash flow by that error and nothing else would notice.
    """
    a, twin = whole_life.Projection[1], whole_life.Projection[2]
    assert a.premium_pp() == G_GROSS
    assert twin.premium_pp() == 3084600.0 == 12 * 257050.0
    assert a.premium_pp() == pytest.approx(0.900 * twin.premium_pp(), abs=WON)
    assert a.prem_gross_calc_pp() / a.premium_pp() == pytest.approx(1.0000100, abs=5e-8)
    assert twin.prem_gross_calc_pp() == pytest.approx(3084630.93, abs=WON)
    assert twin.prem_gross_calc_pp() / twin.premium_pp() == pytest.approx(
        a.prem_gross_calc_pp() / a.premium_pp(), rel=1e-12)
    # P / G(표준형) = 0.682974, not the 80% loading a reader might assume.
    assert a.prem_net_level_pp() / twin.premium_pp() == pytest.approx(
        0.682974, abs=5e-7)


@pytest.mark.parametrize("y", sorted(WORKED_EXAMPLE_RATES))
def test_worked_example_rate_row(kr_whole_life_anchor, y):
    """The notes' 25-row rate table: attained 보험나이, the annual rates and their conversions.

    One row per **policy year**, because that is the unit the rates are published in.  The
    ageing is the product's own — 보험나이 increments on the 계약해당일, so the attained age
    is ``x + y - 1`` through all twelve months of policy year ``y`` — and the lapse vector is
    the supervisor's, log-linear from 10% to 0.1% at 납입완료 and then flat at 0.8%.  Both
    are asserted before the cash flows, because a cash flow row that agrees on a wrong rate
    agrees by accident.
    """
    age, q, q_mth, w, w_mth = WORKED_EXAMPLE_RATES[y]
    a = kr_whole_life_anchor
    t0 = 12 * (y - 1)
    assert a.policy_year(t0) == y
    assert a.age(t0) == age == 39 + y
    assert a.mort_rate(t0) == pytest.approx(q, abs=MORT)
    assert a.mort_rate(t0) == pytest.approx(a.mort_rate_at_age(age), rel=1e-14)
    assert a.mort_rate_mth(t0) == pytest.approx(q_mth, abs=PROB)
    assert a.lapse_rate(t0) == pytest.approx(w, abs=PROB)
    assert a.lapse_rate_mth(t0) == pytest.approx(w_mth, abs=PROB)
    # Both annual rates are level through the twelve months of the policy year, and so are
    # their conversions: 보험나이 steps on the 계약해당일 and the lapse vector is published
    # by 경과기간 in years, so a within-year drift in either would be an invention.
    for t in range(t0, t0 + 12):
        assert a.age(t) == age
        assert a.policy_year(t) == y
        assert a.mort_rate(t) == pytest.approx(q, abs=MORT)
        assert a.lapse_rate(t) == pytest.approx(w, abs=PROB)


def test_the_monthly_decrements_reproduce_the_annual_survivorship(kr_whole_life_anchor):
    """Twelve monthly exits leave exactly the in-force one annual exit leaves.

    The statement the whole conversion rests on, checkable in two directions.  Term by term,
    ``1 - (1 - q^m)^12 == q`` for both decrements, because the monthly rate is defined as the
    uniform-force conversion and nothing else.  End to end, ``pols_if`` at each 계약해당일
    reproduces the annual-step model's own in-force — :data:`ANNIVERSARY_INFORCE` carries
    five of those values as that model printed them.  So the monthly step re-times the
    **exposure** inside the year, which is what moves premium income and the mortality cost,
    and leaves the survivorship the sourced annual rates imply exactly where it was.

    A model that divided the annual rates by twelve would pass neither leg.
    """
    a = kr_whole_life_anchor
    for t in (0, 11, 12, 239, 240, 600):
        assert a.mort_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - a.mort_rate(t)) ** (1.0 / 12.0), rel=1e-15)
        assert a.lapse_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - a.lapse_rate(t)) ** (1.0 / 12.0), rel=1e-15)
        assert 1.0 - (1.0 - a.mort_rate_mth(t)) ** 12 == pytest.approx(
            a.mort_rate(t), rel=1e-14)
        assert a.mort_rate_mth(t) < a.mort_rate(t)
        assert a.lapse_rate_mth(t) < a.lapse_rate(t)
    for t, expected in ANNIVERSARY_INFORCE.items():
        assert a.pols_if(t) == pytest.approx(expected, rel=1e-12), t
    # The terminal year is the one place the conversion does not apply: the table rate is 1
    # at omega, so the certain death is spread uniformly over the twelve months — 1/(12-j)
    # in the j-th — rather than killing the cohort in the first of them and leaving eleven
    # empty rows.  The year still ends with nobody alive.
    last = a.proj_len() - 1
    assert a.age(last) == 115 and a.mort_rate(last) == 1.0
    assert a.mort_rate_mth(last) == 1.0
    assert a.mort_rate_mth(last - 11) == pytest.approx(1.0 / 12.0, rel=1e-15)
    assert a.mort_rate_mth(last - 1) == pytest.approx(0.5, rel=1e-15)
    assert a.pols_if(a.proj_len()) == 0.0


def test_the_lapse_vector_hits_its_two_regulatory_endpoints_exactly(
        kr_whole_life_anchor):
    """w(0) = 10%, w(m-1) = 0.1% at 납입완료 and w(m) = 0.8%, with the shape between them [std].

    ``m`` is a count of policy years, so policy year 1 is the period ``t = 0`` and the
    completion year ``m`` is the period ``t = m - 1``.  The endpoints are the FSS 원칙모형's
    and the interpolation is this library's, so a change to the shape must leave the ends
    alone.  Asserting the ends separately from the 25-row table is what keeps that
    distinction visible: the first and twentieth values are sourced, the eighteen between
    them are not.
    """
    a = kr_whole_life_anchor
    m = a.prem_period()
    assert a.lapse_rate(0) == 0.10
    assert a.lapse_rate(12 * (m - 1)) == pytest.approx(0.001, abs=PROB)
    assert a.lapse_rate(12 * m) == 0.008
    assert all(a.lapse_rate(12 * y) == 0.008
               for y in (20, 39, 59, a.proj_years() - 1))
    assert a.lapse_rate_base(12 * 4) == pytest.approx(
        0.10 * (0.001 / 0.10) ** (4 / 19), rel=1e-12)
    # Monotone decay while the premium runs, and no spike anywhere in the base run.
    assert all(a.lapse_rate(12 * y) > a.lapse_rate(12 * (y + 1)) for y in range(m - 1))
    assert a.lapse_spike() == 0.0


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_cash_flow_row(kr_whole_life_anchor, t):
    """Every cell of the notes' first-year and milestone cash flow rows, to the precision shown.

    This is the module's main statement: the shipped model reproduces the document beside
    it, cell by cell.  ``claims_reduction`` is zero on this cell and is asserted with the
    rest, because a column that is only ever zero is exactly the one an implementation can
    drop without anybody noticing.
    """
    pols, prem, death, lapse, claim_exp, exp, comm, net = WORKED_EXAMPLE[t]
    a = kr_whole_life_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=WON)
    assert a.claims(t, "REDUCTION") == 0.0
    assert a.claim_expenses(t) == pytest.approx(claim_exp, abs=WON)
    assert a.expenses(t) == pytest.approx(exp, abs=WON)
    assert a.commissions(t) == pytest.approx(comm, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)


@pytest.mark.parametrize("d", sorted(WORKED_EXAMPLE_VAL))
def test_worked_example_surrender_value_row(kr_whole_life_anchor, d):
    """The notes' surrender-value table, all seven columns, by month-end.

    Indexed by the month-end ``d`` and not by the month: these are values *at* a point in
    time, and the surrender benefit of month ``t`` is paid on the month-end ``d = t + 1``
    that closes it.  ``d = 1`` and ``d = 6`` are in the table because a monthly account has
    values **inside** the policy year that an annual grid could not state at all.  They carry the whole of the product's signature mechanic — the account,
    the statutory deduction, the twin's value, the payable value, the suppressed value on both
    sides of the step, cumulative premiums and the 환급률 — so they are asserted in their own
    table rather than inferred from the cash flow row that consumes one of them.
    """
    val, chg, std, cv, susp, cum, ratio = WORKED_EXAMPLE_VAL[d]
    a = kr_whole_life_anchor
    assert a.pol_val_pp(d) == pytest.approx(val, abs=WON)
    assert a.surr_chg_pp(d) == pytest.approx(chg, abs=WON)
    assert a.cv_std_pp(d) == pytest.approx(std, abs=WON)
    assert a.cv_pp(d) == pytest.approx(cv, abs=WON)
    assert a.cv_susp_pp(d) == pytest.approx(susp, abs=WON)
    assert a.cum_prem_pp(d) == pytest.approx(cum, abs=WON)
    assert a.refund_ratio(d) == pytest.approx(ratio, abs=RATIO)


def test_worked_example_month_one_trace(kr_whole_life_anchor):
    """The notes' first trace — month 0, the acquisition month.

    One month's premium of ₩231,345 against the whole acquisition charge of ₩3,106,701:
    the account opens at ``V(1) = (P^m (1 + j)) - q^m SA`` over ``1 - q^m``, ``SC(1)`` has
    amortised by one eighty-fourth of the 해약공제기간, ``W(1)`` is floored at zero because
    the account sits ₩2.9m **below** the deduction, and the month's expenses are the
    unremunerated part of the acquisition cost plus one month's maintenance plus 2% of the
    month's premium.

    The monthly grid changes what this row says about the product.  An annual step netted
    the acquisition charge against a whole year's premium of ₩2,776,140 and printed a
    first-year strain of ₩531,338; the charge actually falls against **one month's**
    premium, and the strain the contract really starts from is ₩2,892,090 — 12.5 times the
    month's premium.
    """
    a = kr_whole_life_anchor
    assert a.pols_if(0) == 1.0 and a.pols_if_pay(0) == 1.0
    assert a.pols_waived(0) == 0.0
    assert a.premiums(0) == pytest.approx(G_GROSS_MTH, abs=WON)
    assert a.mort_rate_mth(0) == pytest.approx(
        1.0 - (1.0 - 0.00085) ** (1.0 / 12.0), rel=1e-15)
    assert a.pols_death(0) == pytest.approx(a.mort_rate_mth(0), rel=1e-14)
    assert a.claims(0, "DEATH") == pytest.approx(1e8 * a.mort_rate_mth(0), abs=WON)
    assert a.claim_expenses(0) == pytest.approx(300000.0 * a.mort_rate_mth(0), abs=WON)

    j = a.acc_int_rate_mth()
    assert a.pol_val_pp(1) == pytest.approx(173073.53922300023, abs=TRACE)
    assert a.pol_val_pp(1) == pytest.approx(
        ((0.0 + P_NET_MTH) * (1 + j) - a.mort_rate_mth(0) * 1e8)
        / (1 - a.mort_rate_mth(0)), rel=1e-12)
    assert a.surr_chg_pp(1) == pytest.approx(SURR_CHG_CAP * (1 - 1 / 84), abs=TRACE)
    assert a.pol_val_pp(1) - a.surr_chg_pp(1) == pytest.approx(-2896642.47, abs=WON)
    assert a.cv_std_pp(1) == 0.0
    assert a.cv_pp(1) == 0.0 and a.cv_susp_pp(1) == 0.0
    assert a.claims(0, "LAPSE") == 0.0            # a nil value costs nothing to lapse

    assert a.pols_if_at(0, "BEF_LAPSE") == pytest.approx(
        1.0 - a.mort_rate_mth(0), rel=1e-14)
    assert a.pols_lapse(0) == pytest.approx(0.0087409915, abs=PROB)
    assert a.expenses(0) == pytest.approx(
        ACQ_EXPENSE + 5000.0 + 0.02 * G_GROSS_MTH, abs=TRACE)
    assert a.commissions(0) == pytest.approx(COMM_INIT, abs=TRACE)
    assert a.net_cf(0) == pytest.approx(
        231345.00 - 7086.09 - 0.00 - 21.26 - 1096972.09 - 2019355.35, abs=WON)
    assert a.pols_if(1) == pytest.approx(0.9911881475402914, rel=1e-13)
    # The strain is against one month's premium, which is what the monthly grid is for.
    assert a.acq_cost_pp() / a.premium_mth_pp() == pytest.approx(13.43, abs=5e-3)
    assert -a.net_cf(0) / a.premium_mth_pp() == pytest.approx(12.50, abs=5e-3)


def test_worked_example_second_month_and_the_turn_of_the_policy_year(
        kr_whole_life_anchor):
    """The notes' t = 1 and t = 12 traces: an ordinary month, then the 계약해당일.

    ``t = 1`` is the first month of the steady state — one month's premium, one month's
    decrements, one month's maintenance expense and **no commission at all**, the renewal
    commission being a policy-year-2 charge.  ``t = 12`` is where three things move at once:
    the attained 보험나이 turns 41, the expense inflation factor makes its first step, and
    the renewal commission starts.  On a monthly grid each of those is a date; on an annual
    one they were all just "year 2".
    """
    a = kr_whole_life_anchor
    assert a.premiums(1) == pytest.approx(G_GROSS_MTH * 0.9911881475, abs=WON)
    assert a.pols_death(1) == pytest.approx(0.0000702365276, abs=PROB)
    assert a.claims(1, "DEATH") == pytest.approx(7023.65, abs=WON)
    assert a.inflation_factor(1) == 1.0
    assert a.expenses(1) == pytest.approx(
        5000.0 * 0.9911881475 + 0.02 * a.premiums(1), abs=TRACE)
    assert a.commissions(1) == 0.0
    assert all(a.commissions(t) == 0.0 for t in range(1, 12))
    assert a.pols_if_at(1, "BEF_LAPSE") == pytest.approx(0.9911179110126589, rel=1e-12)
    assert a.pols_lapse(1) == pytest.approx(0.0086639672, abs=PROB)
    assert a.pols_if(2) == pytest.approx(0.9824539438243545, rel=1e-13)
    assert a.pol_val_pp(2) == pytest.approx(346515.871886832, abs=TRACE)
    assert a.surr_chg_pp(2) == pytest.approx(SURR_CHG_CAP * (1 - 2 / 84), abs=TRACE)

    assert a.age(11) == 40 and a.age(12) == 41
    assert a.policy_year(11) == 1 and a.policy_year(12) == 2
    assert a.premiums(12) == pytest.approx(G_GROSS_MTH * 0.899235, abs=1e-2)
    assert a.inflation_factor(12) == pytest.approx(1.02, rel=1e-14)
    assert a.expenses(12) == pytest.approx(
        5000.0 * 1.02 * a.pols_if(12) + 0.02 * a.premiums(12), abs=TRACE)
    assert a.commissions(12) == pytest.approx(0.03 * a.premiums(12), rel=1e-12)
    assert a.commissions(12) == pytest.approx(6241.01, abs=WON)
    assert a.net_cf(12) == pytest.approx(186057.00, abs=WON)
    # The 계약해당일 closing policy year 1 reproduces the annual-step model's own l(1).
    assert a.pols_if(12) == pytest.approx(0.899235, abs=INFORCE)


def test_worked_example_the_surrender_value_becomes_payable_inside_a_policy_year(
        kr_whole_life_anchor):
    """``W(d)`` crosses zero at a **month-end**, and an annual grid could not say which.

    The account overtakes the unamortised 해약공제액 partway through policy year 2, not on
    its anniversary: ``cv_std_pp`` is still nil at ``d = 12`` and positive from ``d = 15``,
    so the contract acquires a payable surrender value in the **third month of the second
    policy year**.  The suppression is applied to it from that instant, which is what a
    policyholder surrendering in month 15 of a 저해지 contract is actually paid, and an
    annual grid could only say that the value was nil at one anniversary and positive at the
    next.
    """
    a = kr_whole_life_anchor
    first = min(d for d in range(1, 60) if a.cv_std_pp(d) > 0.0)
    assert first == 15 and a.policy_year(first - 1) == 2
    assert a.cv_std_pp(14) == 0.0 and a.cv_std_pp(15) > 0.0
    assert a.cv_pp(15) == pytest.approx(0.5 * a.cv_std_pp(15), rel=1e-14)
    assert a.pol_val_pp(15) > a.surr_chg_pp(15)
    assert a.pol_val_pp(14) < a.surr_chg_pp(14)
    # The surrender charge amortises monthly over the 84 months of the 해약공제기간, so
    # it too has a value inside the policy year, and it is gone at d = 84 exactly.
    assert a.surr_chg_pp(84) == 0.0 and a.surr_chg_pp(83) > 0.0
    assert a.surr_chg_pp(42) == pytest.approx(SURR_CHG_CAP * 0.5, abs=TRACE)


def test_worked_example_cliff_trace(kr_whole_life_anchor):
    """The notes' cliff trace — the months either side of 납입완료 at ``d = 240``.

    ``t = 239`` is the last paying month: the surrender benefit is paid on the **post-step**
    value at ``d = 240``, because a surrender in the month that closes the 납입기간 is paid
    on the full value.  ``t = 240`` is the first premium-free month, and the value the
    survivors of it are paid has doubled.

    The monthly grid makes the cliff a **date** and shrinks the cash it moves.  On an annual
    step the whole of policy year 20 carried the 0.1% convergence rate and the whole of year
    21 the 0.8% ultimate, so the swing across 납입완료 was ₩1.82m; month to month it is
    ₩151,116, and the eight-fold jump in surrender outgo is between two adjacent months
    rather than two years.  The finding is unchanged and sharper: the value steps by 1/k and
    almost nobody is there to be paid the step, because the supervisor put the lapse rate at
    0.1% in exactly that year.
    """
    a = kr_whole_life_anchor
    m = a.prem_period_mths()
    assert m == 240 and a.prem_period() == 20
    assert a.pols_if(239) == pytest.approx(0.5948434384, abs=PROB)
    assert a.lapse_rate(239) == pytest.approx(0.001, abs=PROB)
    assert a.lapse_rate_mth(239) == pytest.approx(0.0000833716, abs=PROB)
    assert a.pols_if_at(239, "BEF_LAPSE") == pytest.approx(0.5946128794462873, rel=1e-13)
    assert a.pols_lapse(239) == pytest.approx(0.0000495738, abs=PROB)
    assert a.pol_val_pp(240) == pytest.approx(52023973.58836918, abs=TRACE)
    assert a.surr_chg_pp(240) == 0.0
    assert a.cv_std_pp(240) == pytest.approx(52023973.58836918, abs=TRACE)
    assert a.cv_mult(240) == 1.0 and a.cv_mult(239) == 0.5
    assert a.cv_pp(240) == pytest.approx(52023973.58836918, abs=TRACE)
    assert a.cv_susp_pp(240) == pytest.approx(26011986.79418459, abs=TRACE)
    assert a.claims(239, "LAPSE") == pytest.approx(
        a.cv_pp(240) * a.pols_lapse(239), rel=1e-12)
    assert a.claims(239, "LAPSE") == pytest.approx(2579.03, abs=WON)
    assert a.expenses(239) == pytest.approx(
        5000.0 * 1.02 ** 19 * 0.5948434384 + 0.02 * a.premiums(239), abs=1e-3)
    assert a.commissions(239) == pytest.approx(0.03 * a.premiums(239), rel=1e-12)
    assert a.net_cf(239) == pytest.approx(100696.39, abs=WON)
    assert a.pols_if(240) == pytest.approx(0.5945633056475711, rel=1e-13)
    # The value doubles across the step; the cash moves by a month's worth.
    assert a.cv_pp(240) / a.cv_pp(239) == pytest.approx(2.0104, abs=5e-5)


def test_worked_example_first_premium_free_month_trace(kr_whole_life_anchor):
    """The notes' t = 240 trace — the month the stream turns permanently negative.

    Premium and renewal commission go to zero in the same row while maintenance expense,
    death claims and surrender benefits all continue; the premium-related expense goes with
    the premium and the per-policy one does not.  Surrender outgo is eight times the
    previous month's, because the rate returned to 0.8% against a value that has doubled.
    """
    a = kr_whole_life_anchor
    assert a.premiums(240) == 0.0
    assert a.commissions(240) == 0.0
    assert a.pols_death(240) == pytest.approx(0.0002520375, abs=PROB)
    assert a.claims(240, "DEATH") == pytest.approx(25203.75, abs=WON)
    assert a.pol_val_pp(241) == pytest.approx(52110834.06671206, abs=TRACE)
    assert a.pol_val_pp(241) == pytest.approx(
        (52023973.58836918 * (1 + a.acc_int_rate_mth())
         - a.mort_rate_mth(240) * 1e8) / (1 - a.mort_rate_mth(240)), rel=1e-12)
    assert a.cv_pp(241) == pytest.approx(a.cv_std_pp(241), rel=1e-14)
    assert a.pols_if_at(240, "BEF_LAPSE") == pytest.approx(0.5943112681278924, rel=1e-13)
    assert a.pols_lapse(240) == pytest.approx(0.0003976677, abs=PROB)
    assert a.claims(240, "LAPSE") == pytest.approx(20722.80, abs=WON)
    # Maintenance only: no premium, so no premium-related component.
    assert a.expenses(240) == pytest.approx(
        5000.0 * 1.02 ** 20 * 0.5945633056, abs=1e-3)
    assert a.net_cf(240) == pytest.approx(-50419.61, abs=WON)
    assert a.net_cf(239) - a.net_cf(240) == pytest.approx(CLIFF_SWING, abs=WON)
    assert a.claims(240, "LAPSE") / a.claims(239, "LAPSE") == pytest.approx(
        8.0351, abs=5e-5)


def test_worked_example_undiscounted_totals(kr_whole_life_anchor):
    """The notes' undiscounted totals over the full 912 months, column by column.

    Nine columns and nine totals, to the six decimals the notes print.  Summing the frame
    rather than the cells is deliberate: it is the published statement that must add up,
    and a column that has quietly stopped being published fails here on the key rather
    than on the value.
    """
    df = kr_whole_life_anchor.result_cf()
    assert set(df.columns) == set(TOTALS)
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=TOTAL), column
    # Undiscounted, the contract loses ₩29.8m per policy issued; discounting, the
    # investment return on the account and the CSM all belong to a later layer.
    assert df["net_cf"].sum() < 0.0
    assert df["claims_death"].sum() + df["claims_lapse"].sum() == pytest.approx(
        59915314.89, abs=WON)


def test_worked_example_decrement_split(kr_whole_life_anchor):
    """Sum D = 0.5062074089 and Sum S = 0.4937925911, summing to exactly 1.

    Because the table terminates, every policy issued leaves by a modelled decrement:
    there is no residual population, no maturity and no tail state anywhere in this model.
    Asserting the split to ten decimals is what makes an accidental change to omega or to
    the terminal rate visible as a failure rather than as a slightly different answer.
    """
    a = kr_whole_life_anchor
    ts = range(a.proj_len())
    deaths = sum(a.pols_death(t) for t in ts)
    surrenders = sum(a.pols_lapse(t) for t in ts)
    assert deaths == pytest.approx(SUM_DEATHS, abs=PROB)
    assert surrenders == pytest.approx(SUM_SURRENDERS, abs=PROB)
    assert deaths + surrenders == pytest.approx(1.0, abs=PROB)
    assert a.pols_if(a.proj_len()) == 0.0
    assert a.mort_rate(a.proj_len() - 1) == 1.0
    assert a.mort_rate_mth(a.proj_len() - 1) == 1.0
    assert a.pols_lapse(a.proj_len() - 1) == 0.0  # nobody survives to surrender


def test_worked_example_reading_the_shape_of_the_result(kr_whole_life_anchor):
    """The four features the notes read off the stream, each as its own number.

    A back-ended liability (69.5% of expected death claims from t = 40 on), a profitable
    payment period against an unprofitable run-off, a surrender benefit small relative to
    the death benefit, and an expense block dominated by the first year.  Each is a
    statement a reader takes from the document and would otherwise have no way to check.
    """
    a = kr_whole_life_anchor
    late = sum(a.pols_death(t) for t in range(480, a.proj_len()))
    assert late == pytest.approx(DEATHS_AFTER_YEAR_40, abs=INFORCE)
    assert late / SUM_DEATHS == pytest.approx(0.696, abs=5e-4)

    assert sum(a.net_cf(t) for t in range(240)) == pytest.approx(
        NET_CF_WHILE_PAYING, abs=WON)
    assert sum(a.net_cf(t) for t in range(240, a.proj_len())) == pytest.approx(
        NET_CF_AFTER_PAYING, abs=WON)

    df = a.result_cf()
    assert df["claims_lapse"].sum() < 0.2 * df["claims_death"].sum()
    assert a.expenses(0) / df["expenses"].sum() == pytest.approx(0.238, abs=5e-4)
    # The whole [std] expense and commission block, against the premium stream.
    block = df["expenses"].sum() + df["commissions"].sum()
    assert block == pytest.approx(7674747.49, abs=WON)
    assert block / df["premiums"].sum() == pytest.approx(0.204, abs=5e-4)
    assert a.expenses(0) + a.commissions(0) == pytest.approx(3116327.44, abs=WON)


def test_the_refund_ratio_crossings_are_five_years_apart_on_one_account(whole_life):
    """The anchor crosses 100% at the month-end d = 280 and the 표준형 twin at d = 347.

    The 환급률 is a month-end quantity, so the crossing is quoted at a month-end — and the
    monthly grid can say **which month**: the anchor crosses in the fifth month of policy
    year 24 and the twin in the eleventh of policy year 29, where an annual grid could only
    say which anniversary each had passed.  On the **identical** account: the two points
    differ only in the premium and in k, and the account is a function of neither.  That is
    the whole of the refund-ratio argument that sells this product, and it is the one number
    a reader is most likely to want to reproduce, so it is asserted from both sides — the
    crossing month-ends, and the equality of the two policy values that makes them comparable
    at all.
    """
    a, twin = whole_life.Projection[1], whole_life.Projection[2]
    assert a.refund_ratio(279) < 1.0 < a.refund_ratio(280)
    assert a.policy_year(279) == 24
    assert twin.refund_ratio(346) < 1.0 < twin.refund_ratio(347)
    assert twin.policy_year(346) == POINT_2_CROSSING == 29
    assert twin.refund_ratio(12 * (POINT_2_CROSSING - 1)) < 1.0

    for d in (1, 6, 12, 120, 240, 480, 912):
        assert a.pol_val_pp(d) == pytest.approx(twin.pol_val_pp(d), abs=1e-9)
    assert a.cum_prem_pp(240) < twin.cum_prem_pp(240)


@pytest.mark.parametrize("y", sorted(CALIBRATION))
def test_the_calibration_against_the_published_grid(kr_whole_life_anchor, y):
    """The notes' eight-point fit of ``cv_std_pp`` against DB생명's published run [S4].

    Keyed by the **policy year**, which is the duration a published 해지환급금 grid quotes,
    and read at the 계약해당일 ``d = 12y``.  The model side of the comparison, plus the ratio
    the notes report.  Durations 3 to 20 sit in a 0.899-0.923 band — a level offset from
    setting 계약체결비용 **at** the statutory cap, not a shape error — and the widening past
    duration 20 has a stated cause: the published product carries a 전환나이 60세 step-up its
    duration-60 value of ₩104,604,000 gives away, being above the ₩100,000,000 sum assured.

    The monthly account improves the fit at every sourced duration, by the same 1.2% it
    raises the whole account: the published grid is a real Korean contract whose own account
    accrues monthly, and the annual grid was reading it with an annual one.
    """
    model_cv, published, ratio = CALIBRATION[y]
    a = kr_whole_life_anchor
    d = 12 * y
    assert a.cv_std_pp(d) == pytest.approx(model_cv, abs=WON)
    if ratio is None:
        assert a.cv_std_pp(d) == 0.0 and published == 0
        return
    assert a.cv_std_pp(d) / published == pytest.approx(ratio, abs=5e-5)
    if y <= 20:
        assert 0.899 <= a.cv_std_pp(d) / published <= 0.923
    assert published < 1e8 or y == 60          # the tell: a level account cannot do that


def test_the_flat_basis_run_is_the_disclosure_the_guidance_obliges(tmp_path):
    """The notes' ``flat`` comparison table, on the identical anchor cell.

    The November 2024 계리가정 decision makes the 원칙모형 the base and obliges an insurer
    departing from it to disclose the difference [REG-R27], so the level 4% vector is not
    an alternative assumption but the comparison itself.  What it shows is that the cliff
    moves far less cash on the supervised vector than a reader expects: on ``flat`` the same
    step lands on a 4% annual lapse rate and the last paying month ``t = 239`` turns
    **negative**, where on the 원칙모형 it is the best month of the projection.  Without this
    test the two bases would be shipped side by side and only one ever run.
    """
    model = product_copy(tmp_path, "WholeLife_KR_S_flat")
    try:
        table = pd.read_csv(
            model.Data.input_dir() / "model_point_table.csv", index_col="point_id")
        assert table.loc[1, "lapse_basis"] == "loglinear"
        table.loc[1, "lapse_basis"] = "flat"
        table.to_csv(model.Data.input_dir() / "model_point_table.csv")
        model.Data.clear_all()
        model.Projection.clear_all()

        p = model.Projection[1]
        assert p.lapse_basis() == "flat"
        for t in (228, 239, 240):
            assert p.lapse_rate(t) == FLAT_BASIS[f"lapse_rate_{t}"]
            assert p.claims(t, "LAPSE") == pytest.approx(
                FLAT_BASIS[f"claims_lapse_{t}"], abs=WON)
        assert p.net_cf(239) == pytest.approx(FLAT_BASIS["net_cf_239"], abs=WON)
        assert p.pols_if(239) == pytest.approx(FLAT_BASIS["pols_if_239"], abs=INFORCE)
        assert p.net_cf(239) < 0.0 < WORKED_EXAMPLE[239][7]

        df = p.result_cf()
        assert df["claims_lapse"].sum() == pytest.approx(
            FLAT_BASIS["sum_claims_lapse"], abs=WON)
        assert df["claims_death"].sum() == pytest.approx(
            FLAT_BASIS["sum_claims_death"], abs=WON)
        assert df["net_cf"].sum() == pytest.approx(FLAT_BASIS["sum_net_cf"], abs=WON)

        # The contractual step is untouched: only the rate it lands on has moved.
        assert p.cv_pp(240) == pytest.approx(WORKED_EXAMPLE_VAL[240][3], abs=WON)
        assert p.cv_pp(240) / p.cv_susp_pp(240) == pytest.approx(2.0, rel=1e-14)
        # The headline improvement is a shorter book, not a better product.
        assert df["claims_death"].sum() < 0.36 * TOTALS["claims_death"]
        assert p.check_net_cf() is True and p.check_pols_roll_fwd() is True
    finally:
        model.close()


def test_the_ten_shipped_model_points_reach_their_signature_numbers(whole_life):
    """One number per model point, the notes' own table of what each one is for.

    A model point table is a claim about coverage, and a point whose signature number has
    drifted is a point that no longer demonstrates what the documentation says it does.
    Each of these numbers is checked in depth by its own pitfall test below; this asserts
    the whole table at once, so a point that has been renumbered or re-parameterized is a
    single failure rather than a scattering of them.
    """
    p = whole_life.Projection
    table = whole_life.Data.model_point_table()
    assert list(table.index) == list(range(1, 11))

    assert p[1].cv_pp(240) / p[1].cv_susp_pp(240) == pytest.approx(2.0, rel=1e-14)
    assert p[2].refund_ratio(240) == pytest.approx(POINT_2_REFUND_20, abs=RATIO)
    assert p[3].cv_pp(228) == 0.0 and p[3].loan_draw(108) == 0.0
    assert p[3].refund_ratio(240) == pytest.approx(POINT_3_REFUND_20, abs=RATIO)
    assert p[4].proj_len() == POINT_4_PROJ_LEN == 12 * p[4].proj_years()
    assert p[5].prem_period() == POINT_5_PREM_PERIOD == p[5].proj_years()
    assert p[5].prem_period_mths() == p[5].proj_len()
    assert p[6].loan_draw(108) == pytest.approx(POINT_6_LOAN_DRAW, abs=WON)
    assert p[6].loan_pp(p[6].proj_len() - 1) == pytest.approx(POINT_6_LOAN_END, abs=WON)
    assert p[7].pols_waived(228) == pytest.approx(POINT_7_WAIVED_228, abs=INFORCE)
    assert p[8].lapse_rate_mth(83) == pytest.approx(POINT_8_LAPSE_SPIKE_MTH, abs=PROB)
    assert p[8].refund_ratio(84) == pytest.approx(POINT_8_REFUND_7, abs=RATIO)
    assert p[9].pol_val_pp(240) / p[9].prosp_val_pp(240) - 1.0 == pytest.approx(
        POINT_9_PROSP_GAP, abs=5e-6)
    assert p[10].claims(179, "REDUCTION") == pytest.approx(POINT_10_REDUCTION, abs=WON)
    assert p[10].net_cf(179) == pytest.approx(POINT_10_NET_CF_179, abs=WON)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_the_cliff_is_a_step_not_a_ramp(kr_whole_life_anchor):
    """CV(m) / (k W(m)) is exactly 1 / k; anything between is an interpolation.

    The multiplier takes two values and only two — k before 납입완료 and 1 from it — so a
    model that grades, interpolates or smooths across the boundary fails here.  This is
    the notes' first-listed pitfall and the product's signature mechanic, and the step is
    discontinuous in a way the underlying account is not: the payable value doubles in the
    year the account moves by 6.5%.  ``m`` is a count of policy years, so the step falls at
    the anniversary ``d = m``.
    """
    a = kr_whole_life_anchor
    m = a.prem_period_mths()
    assert m == 240 and a.prem_period() == 20
    assert a.cv_pp(m) / a.cv_susp_pp(m) == pytest.approx(1.0 / 0.50, rel=1e-14)
    assert a.cv_pp(m) / a.cv_susp_pp(m) == pytest.approx(2.0, abs=5e-12)
    assert {a.cv_mult(d) for d in range(1, a.proj_len() + 1)} == {0.50, 1.0}
    assert a.cv_mult(m - 1) == 0.50 and a.cv_mult(m) == 1.0
    assert a.cv_pp(m) / a.cv_pp(m - 1) > 2.0
    # The account moves by a **month's** accrual across the step, which is what makes the
    # discontinuity visible for what it is: 0.5% against a doubling of the payable value.
    assert a.cv_std_pp(m) / a.cv_std_pp(m - 1) == pytest.approx(1.005, abs=5e-4)
    assert a.cv_pp(m + 1) / a.cv_pp(m) < 1.01
    assert a.check_cv_cliff() is True
    for d in (1, 15, 120, 239, 240, 241, 480):
        assert a.check_cv_cliff_resid(d) == pytest.approx(0.0, abs=1e-6)


def test_pitfall_the_cliff_never_happens_on_a_whole_of_life_premium_point(whole_life):
    """On 전기납 (prem_term = 0) the suppressed period runs for life and m is the horizon.

    Model point 5 is that configuration, and it is in the table because it is the one in
    which the product's signature mechanic is absent by construction.  A model that steps
    the value up at some inferred anniversary invents a 납입완료 the contract does not
    have; one that credits a 유지보너스 there invents a date for it too.
    """
    p = whole_life.Projection[5]
    assert p.prem_term() == 0
    assert p.prem_period() == p.proj_years() == POINT_5_PREM_PERIOD
    assert p.prem_period_mths() == p.proj_len()
    assert p.prem_end() == p.proj_years()
    assert all(p.cv_mult(d) == 0.50 for d in range(1, p.proj_len() + 1))
    assert all(p.cv_pp(d) == pytest.approx(0.50 * p.cv_std_pp(d), rel=1e-14)
               for d in (1, 12, 120, 300, 600))
    assert all(p.cv_pp(d) == pytest.approx(p.cv_susp_pp(d), rel=1e-14)
               for d in (1, 12, 120, 300, 600))
    assert p.premiums(p.proj_len() - 1) > 0.0  # premiums run to the very last month
    assert all(p.bonus_pp(d) == 0.0 for d in range(1, p.proj_len() + 1))
    # The 해약공제기간 is still seven years: it never depended on 납입완료.
    assert p.surr_chg_period() == 7 and p.surr_chg_period_mths() == 84
    assert p.surr_chg_pp(83) > 0.0 and p.surr_chg_pp(84) == 0.0
    assert p.check_cv_cliff() is True


def test_pitfall_off_by_one_at_the_boundary(kr_whole_life_anchor):
    """A surrender in the last paying month is paid on the **full** value, not the suppressed one.

    The 납입기간 closes at the month-end ``d = 12m``, so the last paying month is
    ``t = 12m - 1`` and its surrenders are settled on the value at that month-end, where both
    quantities exist and the model publishes both; the notes state the ordering rule because
    it is worth real money.  Paying that row's surrenders on the suppressed value would halve
    its surrender outgo, and a model that carried only one of the two could not state which
    rule it was using.

    The monthly grid narrows the window the rule applies to from a year to a month, which is
    what the contract actually says: a surrender on the last day of the 납입기간 is paid in
    full, and one the day before is not.
    """
    a = kr_whole_life_anchor
    m = a.prem_period_mths()
    assert a.claims(m - 1, "LAPSE") == pytest.approx(
        a.cv_pp(m) * a.pols_lapse(m - 1), rel=1e-12)
    suppressed = a.cv_susp_pp(m) * a.pols_lapse(m - 1)
    assert a.claims(m - 1, "LAPSE") - suppressed == pytest.approx(1289.51, abs=WON)
    assert a.claims(m - 1, "LAPSE") == pytest.approx(2.0 * suppressed, rel=1e-12)
    # The month before is on the suppressed value, and both cells publish their own.
    assert a.claims(m - 2, "LAPSE") == pytest.approx(
        a.cv_susp_pp(m - 1) * a.pols_lapse(m - 2), rel=1e-12)
    assert a.cv_pp(m - 1) == pytest.approx(a.cv_susp_pp(m - 1), rel=1e-14)
    assert a.cv_pp(m) != pytest.approx(a.cv_susp_pp(m), rel=1e-6)
    assert "cv_susp_pp" in a.result_val().columns and "cv_pp" in a.result_val().columns


def test_pitfall_one_policy_value_one_multiplier(whole_life):
    """The suppression is a haircut on a common account, not a second reserve basis.

    Model points 1 and 2 are the same policy — same issue age, same sum assured, same
    payment term — at k = 0.50 and k = 1.00 on **different premiums**.  Their accounts are
    identical at every duration, and that is exactly the point: ``cv_pp`` is independent
    of the sold form's own premium, which is the whole of the refund-ratio arithmetic.
    Deriving the suppressed form's value from the suppressed form's own premium destroys
    the product's economics while still producing plausible numbers.
    """
    low, ordinary = whole_life.Projection[1], whole_life.Projection[2]
    assert low.cv_floor_ratio() == 0.50 and ordinary.cv_floor_ratio() == 1.00
    assert low.premium_pp() < ordinary.premium_pp()
    assert low.prem_net_level_pp() == pytest.approx(
        ordinary.prem_net_level_pp(), rel=1e-14)
    for d in range(low.proj_len() + 1):
        assert low.pol_val_pp(d) == pytest.approx(ordinary.pol_val_pp(d), abs=1e-9)
        assert low.cv_std_pp(d) == pytest.approx(ordinary.cv_std_pp(d), abs=1e-9)
    for d in (15, 60, 239):
        assert low.cv_pp(d) == pytest.approx(0.50 * ordinary.cv_pp(d), rel=1e-14)
    for d in (240, 360, 480, 720):
        assert low.cv_pp(d) == pytest.approx(ordinary.cv_pp(d), rel=1e-14)
    # One series, one multiplier: there is no second account cells anywhere.
    names = set(whole_life.Projection.cells)
    for absent in ("pol_val_low_pp", "pol_val_susp_pp", "reserve_pp", "reserve_low_pp"):
        assert absent not in names, f"{absent}: a second account run"


def test_pitfall_the_step_is_not_the_surrender_charge_running_off(kr_whole_life_anchor):
    """surr_chg_pp(84) = 0, thirteen years before the cliff at the month-end d = 240.

    제7-66조제1항제2호 caps the 해약공제기간 at seven years, so on a 20년납 contract the
    deduction is fully amortised long before 납입완료 and the step at ``d = 20`` cannot be an
    amortisation effect.  Grading the charge to m instead of to min(m, 7) is a common and
    detectable error, and it would put a charge on the books in the very year the step
    happens — which is how a modeller talks themselves into a ramp.
    """
    a = kr_whole_life_anchor
    n_sc = a.surr_chg_period_mths()
    assert a.surr_chg_period() == 7 == min(a.prem_period(), 7)
    assert n_sc == 84
    assert a.surr_chg_pp(0) == pytest.approx(a.surr_chg_cap_pp(), abs=TRACE)
    # The deduction amortises **monthly**, so it has a value inside the policy year as well
    # as at the anniversary; an annual grid could only step it once a year.
    for d in range(1, 84):
        assert a.surr_chg_pp(d) == pytest.approx(
            a.surr_chg_cap_pp() * (1 - d / 84), abs=TRACE)
        assert a.surr_chg_pp(d) > a.surr_chg_pp(d + 1)
    assert all(a.surr_chg_pp(d) == 0.0 for d in (84, 96, 156, 239, 240, 241, 480))
    assert a.cv_std_pp(84) == pytest.approx(a.pol_val_pp(84), rel=1e-14)
    assert a.check_surr_chg_cap() is True
    assert all(a.surr_chg_pp(d) <= a.surr_chg_cap_pp() + 1e-6
               for d in range(a.proj_len() + 1))
    # A charge graded to m instead would still be running at the cliff.
    assert a.surr_chg_cap_pp() * (1 - 240 / a.prem_period_mths()) == 0.0
    assert a.surr_chg_cap_pp() * (1 - 228 / a.prem_period_mths()) > 150000.0


def test_pitfall_p_and_p20_are_different_annuities(whole_life):
    """별표 14 주3 puts the 연납순보험료 on a 20년납 footing; P and P20 coincide only at m = 20.

    The anchor satisfies m = 20, so **a model tested only on the anchor cannot see this
    confusion at all** — which is why it is tested on the 7년납 and 10년납 points, where
    reusing P in the cap formula would overstate the statutory surrender charge by 97% on
    the one and by 54% on the other.
    """
    a = whole_life.Projection[1]
    assert a.prem_period() == 20
    assert a.prem_net_level_pp() == pytest.approx(a.prem_net_20yr_pp(), rel=1e-14)
    assert a.prem_net_20yr_pp() == pytest.approx(P_NET_20YR, abs=TRACE)

    short = whole_life.Projection[8]          # 7년납
    assert short.prem_period() == 7 and short.prem_period_mths() == 84
    assert short.prem_net_level_pp() == pytest.approx(5118388.52, abs=WON)
    assert short.prem_net_20yr_pp() == pytest.approx(P_NET_20YR, abs=TRACE)
    assert short.prem_net_level_pp() / short.prem_net_20yr_pp() == pytest.approx(
        2.429576, abs=5e-6)
    assert short.surr_chg_cap_pp() == pytest.approx(
        0.05 * 20 * short.prem_net_20yr_pp() + 0.01 * short.sum_assured(), rel=1e-14)
    assert short.surr_chg_cap_pp() == pytest.approx(SURR_CHG_CAP, abs=TRACE)
    wrong = 0.05 * 20 * short.prem_net_level_pp() + 0.01 * short.sum_assured()
    assert wrong / short.surr_chg_cap_pp() == pytest.approx(1.969, abs=5e-4)

    ten = whole_life.Projection[10]           # 10년납, on a ₩1,000,000,000 cover
    assert ten.prem_period() == 10 and ten.prem_period_mths() == 120
    assert ten.prem_net_level_pp() == pytest.approx(46935599.64, abs=WON)
    assert ten.prem_net_20yr_pp() == pytest.approx(26906012.12, abs=WON)
    assert ten.surr_chg_cap_pp() == pytest.approx(
        0.05 * 20 * ten.prem_net_20yr_pp() + 0.01 * ten.sum_assured(), rel=1e-14)
    wrong_ten = 0.05 * 20 * ten.prem_net_level_pp() + 0.01 * ten.sum_assured()
    assert wrong_ten / ten.surr_chg_cap_pp() == pytest.approx(1.543, abs=5e-4)
    assert ten.check_surr_chg_cap() is True


def test_pitfall_the_sum_assured_entering_the_cap_is_taken_before_any_reduction(
        whole_life):
    """별표 15 제3호·제8호: the 보험가입금액 in the cap is the pre-체증, pre-감액 amount.

    On model point 10 half the cover is surrendered at duration 15, and the sum assured,
    the premium and the account all restate pro rata — but the **cap** does not, because
    it is a property of the contract as filed rather than of the benefit in force.  A
    model that recomputed it from ``sum_assured_at(t)`` would shrink the statutory
    allowance a carrier is entitled to at exactly the moment it stops mattering.
    """
    p = whole_life.Projection[10]
    assert p.reduce_year() == 15 and p.reduce_frac() == 0.5
    assert p.sum_assured() == 1e9
    # Policy year 15 closes at the 계약해당일 d = 180, where the reduction is made, so the
    # last month of it is t = 179: that month's cover is still whole and the next is half.
    # The monthly grid puts the 감액 on its own date, where an annual one put it in a year.
    assert p.sum_assured_at(179) == 1e9 and p.sum_assured_at(180) == 0.5e9
    assert p.sa_factor(180) == 1.0 and p.sa_factor(181) == 0.5
    assert p.surr_chg_cap_pp() == pytest.approx(
        0.05 * 20 * p.prem_net_20yr_pp() + 0.01 * 1e9, rel=1e-14)
    assert p.surr_chg_cap_pp() == pytest.approx(36906012.12, abs=WON)
    # The account and the premium do restate, exactly and by the same factor.
    assert p.pol_val_pp(181) == pytest.approx(0.5 * p.pol_val_base_pp(181), rel=1e-14)
    assert p.premium_mth_at_pp(180) == pytest.approx(
        0.5 * p.premium_mth_pp(), rel=1e-14)
    assert p.check_pol_val_roll_fwd() is True


def test_pitfall_premiums_stop_at_m_and_nothing_else_does(kr_whole_life_anchor):
    """Premium and renewal commission end at 납입완료; every other line runs for life.

    A projection truncated at 납입완료 misses the majority of the liability — 69.6% of
    expected death claims fall from ``t = 480`` on this cell — and one that keeps charging
    renewal commission past it charges commission on a premium nobody pays.  So does one
    that keeps the 2%-of-premium maintenance component running on zero premium, which is
    the subtler half of the same mistake.  ``prem_end()`` is a count of policy years and
    ``prem_period_mths()`` the month count, so the last paying month is ``t = 12m - 1``.
    """
    a = kr_whole_life_anchor
    m = a.prem_period_mths()
    assert a.prem_end() == 20 and m == 240
    assert a.premiums(m - 1) > 0.0 and a.commissions(m - 1) > 0.0
    for t in (m, 360, 600, a.proj_len() - 1):
        assert a.premiums(t) == 0.0
        assert a.commissions(t) == 0.0
        assert a.claims(t, "DEATH") > 0.0
    for t in (m, 360, 600):
        assert a.expenses(t) > 0.0
    assert a.claims(m, "LAPSE") > 0.0
    assert a.cum_prem_pp(m) == a.cum_prem_pp(a.proj_len()) == 55522800.0
    # The premium-related expense goes with the premium; the per-policy one does not.
    assert a.expenses(240) == pytest.approx(
        5000.0 * a.inflation_factor(240) * a.pols_if(240), rel=1e-12)
    assert a.expenses(239) - 5000.0 * a.inflation_factor(239) * a.pols_if(239) == (
        pytest.approx(0.02 * a.premiums(239), rel=1e-12))
    # The account keeps growing after the premiums stop, and so does the payable value.
    assert a.cv_pp(a.proj_len() - 1) > a.cv_pp(m)
    assert all(a.net_cf(t) < 0.0 for t in range(240, a.proj_len()))


def test_pitfall_the_policy_loan_does_not_exist_on_a_muhaeji_contract(whole_life):
    """loan_draw is **exactly zero** at loan_util = 1.0 on the 무해지 point.

    There is no payable value to lend against during 납입기간, which is the FSS's 2019
    소비자경보 reproduced as arithmetic [R4] [REG-R28].  A model computing the limit off
    ``cv_std_pp`` rather than ``cv_pp`` lends against a value the policyholder cannot
    claim — and on the 저해지 point at k = 0.50 it lends exactly twice too much, which is
    the same bug in a form that does not look like a bug.
    """
    nil = whole_life.Projection[3]
    assert nil.cv_floor_ratio() == 0.0
    assert nil.loan_util() == 1.0 and nil.loan_year() == 10
    assert all(nil.cv_pp(d) == 0.0 for d in range(1, 240))
    assert all(nil.claims(t, "LAPSE") == 0.0 for t in range(239))
    assert nil.cv_std_pp(108) > 10000000.0      # there is a value; it is not payable
    assert nil.loan_draw(108) == 0.0            # policy year 10 opens at the month t = 108
    assert all(nil.loan_pp(d) == 0.0 for d in range(nil.proj_len() + 1))
    assert nil.check_loan_roll_fwd() is True
    # At 납입완료 the whole 표준형 value appears at once.
    assert nil.cv_pp(240) == pytest.approx(nil.cv_std_pp(240), rel=1e-14)
    assert nil.cv_pp(240) == pytest.approx(52023973.59, abs=WON)

    low = whole_life.Projection[6]
    assert low.cv_floor_ratio() == 0.50
    assert low.loan_draw(108) == pytest.approx(0.8 * low.cv_pp(108), rel=1e-14)
    assert low.loan_draw(108) == pytest.approx(POINT_6_LOAN_DRAW, abs=WON)
    assert low.loan_draw(108) == pytest.approx(
        0.5 * 0.8 * low.cv_std_pp(108), rel=1e-14)
    # The draw falls in one month and nowhere else, which is what a monthly grid can say.
    assert all(low.loan_draw(t) == 0.0 for t in range(low.proj_len()) if t != 108)


def test_pitfall_everything_is_floored_at_zero(whole_life):
    """No amount in this model may produce a negative payment, and the floor bites.

    V - SC is ₩2,896,642 negative at the month-end d = 1 on the anchor, which is why every
    published Korean grid shows nil at duration 1.  And on model point 6 an unrepaid loan
    compounds at 4% a year against an account growing at 2.5% until it exceeds the
    ₩100,000,000 sum assured at the month-end d = 871 — the seventh month of policy year 73,
    a date an annual grid could only place in a year — from which month both the death
    benefit and the surrender payout are exactly zero rather than negative.
    """
    a = whole_life.Projection[1]
    assert a.pol_val_pp(1) - a.surr_chg_pp(1) < 0.0
    assert a.cv_std_pp(1) == 0.0 and a.cv_pp(1) == 0.0

    p = whole_life.Projection[6]
    crossing = min(d for d in range(1, p.proj_len() + 1)
                   if p.loan_pp(d) > p.sum_assured())
    assert crossing == 871 and p.policy_year(crossing) == 73
    # The balance opening month 871 exceeds both the cover and the value closing it.
    assert p.loan_pp(871) > p.sum_assured()
    assert p.loan_pp(871) > p.cv_pp(872)
    assert p.pols_if(871) > 0.0                 # the floor bites on a live cohort
    for t in (871, 872, 900):
        assert p.claims(t, "DEATH") == 0.0
        assert p.claims(t, "LAPSE") == 0.0
    assert p.claims(870, "DEATH") > 0.0
    for t in range(p.proj_len()):
        assert p.claims(t, "DEATH") >= 0.0
        assert p.claims(t, "LAPSE") >= 0.0
        assert p.claims(t, "REDUCTION") >= 0.0
    assert all(p.cv_pp(d) >= 0.0 for d in range(p.proj_len() + 1))
    # Korea has no loan-excess lapse: the balance absorbs the payout, it does not
    # terminate the contract, so the policy is still in force with a zero benefit.
    assert p.pols_lapse(871) > 0.0
    assert p.check_pols_roll_fwd() is True


def test_pitfall_the_bonus_cannot_be_booked_without_the_lapse_spike(whole_life):
    """유지보너스 on, and the bonus **month**'s lapse rate goes from 0.00008 to 0.30008.

    The supervisor requires an additional lapse of at least 30 points at any bonus **date**
    [REG-R27], so booking the credit alone misstates the liability in the insurer's
    favour — which is precisely what the guidance exists to prevent.  ``lapse_spike()`` is
    wired to ``bonus_rate()`` so the pair cannot be separated by accident, and this test
    asserts the wiring rather than the two values independently.

    The spike is the one behavioural rate this model does **not** convert to a monthly
    equivalent.  It is an election on the day the bonus is credited, not a force acting
    through a year, so it enters whole in the single month whose end is 납입완료 — where an
    annual grid had to smear it over the whole of the last paying year, a twelvefold
    dilution of a date.
    """
    a = whole_life.Projection[1]
    assert a.bonus_rate() == 0.0
    assert a.lapse_spike() == 0.0
    assert all(a.bonus_pp(d) == 0.0 for d in range(1, a.proj_len() + 1))

    p = whole_life.Projection[8]
    assert p.bonus_rate() == 0.138 and p.prem_term() == 7
    assert p.lapse_spike() == 0.30
    # 납입완료 falls at the month-end d = 84, so the spike month is t = 83 and no other.
    assert p.prem_period_mths() == 84
    assert p.lapse_rate_base(83) == pytest.approx(0.001, abs=PROB)
    assert p.lapse_rate_mth(83) == pytest.approx(POINT_8_LAPSE_SPIKE_MTH, abs=PROB)
    assert p.lapse_rate_mth(83) == pytest.approx(
        p.lapse_rate_mth(82) + 0.30, abs=PROB)
    assert p.lapse_rate_mth(82) < 0.001 and p.lapse_rate_mth(84) < 0.001
    assert sum(1 for t in range(p.proj_len()) if p.lapse_rate_mth(t) > 0.1) == 1
    # The credit itself: 13.8% of premiums paid, from 납입완료 onwards.
    assert p.bonus_pp(83) == 0.0
    assert p.bonus_pp(84) == pytest.approx(0.138 * p.cum_prem_pp(84), rel=1e-14)
    assert p.bonus_pp(84) == pytest.approx(6515583.06, abs=WON)
    assert p.cv_pp(84) - p.bonus_pp(84) == pytest.approx(p.cv_std_pp(84), rel=1e-12)
    assert p.refund_ratio(84) == pytest.approx(POINT_8_REFUND_7, abs=RATIO)
    assert p.check_cv_cliff() is True


def test_pitfall_the_prospective_identity_is_withdrawn_on_a_linked_point(whole_life):
    """On 금리연동형 the account is path-dependent, so the identity is defined as zero.

    Model point 9 credits 2.75% while the net premium stays on the 2.50% 예정이율, and the
    forward account runs 9.12% above its prospective form at the month-end d = 240.
    Asserting the identity unconditionally fails there; "fixing" it by discounting the
    account on the pricing rate silently changes the product, which is the trap this pitfall
    names.
    """
    a = whole_life.Projection[1]
    assert a.int_basis() == "fixed"
    assert a.acc_int_rate() == a.model.Projection.prem_int_rate == 0.025
    assert a.check_pol_val_prosp() is True
    # Every month-end before the terminal year closes to a hundredth of a won; the terminal
    # year's 1/(1 - q^m) chain amplifies the float noise twelvefold and nothing else does.
    assert max(abs(a.check_pol_val_prosp_resid(d))
               for d in range(1, a.proj_len() - 12)) < 0.05

    p = whole_life.Projection[9]
    assert p.int_basis() == "linked"
    assert p.decl_rate() == 0.0275
    assert p.acc_int_rate() == pytest.approx(0.0275, rel=1e-14)
    assert p.prem_net_level_pp() == pytest.approx(2084679.09, abs=WON)
    assert p.pol_val_pp(240) == pytest.approx(54077741.85, abs=WON)
    assert p.prosp_val_pp(240) == pytest.approx(49559710.78, abs=WON)
    assert p.pol_val_pp(240) / p.prosp_val_pp(240) - 1.0 == pytest.approx(
        POINT_9_PROSP_GAP, abs=5e-6)
    # Withdrawn, not forced: the residual is zero by definition and the check passes.
    assert all(p.check_pol_val_prosp_resid(d) == 0.0
               for d in (1, 120, 240, p.proj_len() - 1))
    assert p.check_pol_val_prosp() is True
    assert p.check_pol_val_roll_fwd() is True   # the retrospective one still binds
    # The 최저보증이율 is the floor, and the loan rate follows the crediting rate.
    assert p.loan_int_rate() == pytest.approx(0.0275 + 0.015, rel=1e-12)


def test_pitfall_pol_val_pp_is_not_a_reserve_and_never_a_cash_flow(whole_life):
    """계약자적립액, not 책임준비금: no reserve cells, and none of the three in net_cf.

    Under K-IFRS 제1117호 the insurer books no 보험료적립금 as a separate statutory
    reserve, which is why the surrender basis is re-anchored on a contractually defined
    account.  This model computes no 책임준비금, no CSM, no 요구자본 and no
    해약환급금준비금, and a reader who takes ``pol_val_pp`` for a reserve reads a valuation
    out of a projection that deliberately stops before one.
    """
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for absent in ("reserve_pp", "reserve", "book_reserve_pp", "csm", "csm_pp",
                   "risk_adjustment", "req_capital", "surr_reserve_pp"):
        assert absent not in names, f"{absent}: this model computes no reserve"
    a = whole_life.Projection[1]
    cf_columns = set(a.result_cf().columns)
    for absent in ("pol_val_pp", "cv_std_pp", "cv_pp", "cv_susp_pp"):
        assert absent not in cf_columns, f"{absent} is not a cash flow"
        assert absent in set(a.result_val().columns)
    assert a.check_net_cf() is True
    doc = flat(whole_life.Projection.cells["pol_val_pp"].doc)
    assert "책임준비금" in doc and "계약자적립액" in doc


def test_pitfall_waived_premiums_count_as_paid_and_the_waiver_is_a_state(whole_life):
    """A waived policy pays nothing and accrues everything, so it cannot be a rate cut.

    「보험료가 … 정상적으로 납입된 것으로 하여 사망보험금 및 해지환급금을 계산합니다」
    [S2] [S3] [S8].  The premium is weighted by the paying cohort and everything else by
    the whole in-force count — and because the two coincide in the base run, an
    implementation that weights premium by ``pols_if(t)`` reproduces the worked example
    exactly and fails only once the module is switched on.  So it is switched on here.
    """
    a = whole_life.Projection[1]
    assert a.waiver_rate(0) == 0.0
    assert all(a.pols_waived(t) == 0.0 for t in range(a.proj_len()))
    assert all(a.pols_if(t) == a.pols_if_pay(t) for t in range(a.proj_len()))

    p = whole_life.Projection[7]
    assert p.waiver_rate(0) == 0.004
    assert p.waiver_rate_mth(0) == pytest.approx(
        1.0 - (1.0 - 0.004) ** (1.0 / 12.0), rel=1e-15)
    assert 0.004 / 12.0 < p.waiver_rate_mth(0) < 0.004
    assert p.waiver_rate(12 * p.prem_end()) == 0.0   # nothing left to waive
    assert p.pols_waived(228) == pytest.approx(POINT_7_WAIVED_228, abs=INFORCE)
    assert p.pols_if(228) == pytest.approx(
        p.pols_if_pay(228) + p.pols_waived(228), rel=1e-14)
    assert p.pols_if(228) > p.pols_if_pay(228)
    # Premium on the paying cohort alone; everything else on the whole in-force count.
    assert p.premiums(228) == pytest.approx(
        p.premium_mth_pp() * p.pols_pay_exp(228), rel=1e-14)
    assert p.premiums(228) < p.premium_mth_pp() * p.pols_if(228)
    assert p.pols_death(228) == pytest.approx(
        p.pols_if(228) * p.mort_rate_mth(228), rel=1e-14)
    assert p.expenses(240) == pytest.approx(
        5000.0 * p.inflation_factor(240) * p.pols_if(240), rel=1e-12)
    # Weighting premium by pols_if would book ₩1,532,542.77 of premium nobody paid.
    booked = sum(p.premiums(t) for t in range(240))
    naive = sum(p.premium_mth_pp() * p.pols_if(t) for t in range(240))
    assert naive - booked == pytest.approx(1532542.77, abs=WON)
    # The account is a per-policy contractual quantity and knows nothing of the state.
    assert p.check_pol_val_roll_fwd() is True
    assert p.check_pols_roll_fwd() is True


def test_pitfall_lapse_is_behavioural_not_funded(whole_life):
    """There is no 자동대출납입 anywhere in this model, and importing one would be wrong.

    ``jplib``'s whole life chassis turns on the 自動振替貸付, which advances the premium
    against the surrender value so that lapse there is a **funded** event with a
    continuation test.  No such provision was found in any retrieved Korean document, so
    lapse here is a plain behavioural decrement at the end of a 14-day 납입최고기간 — and
    on a 무해지 form the policyholder receives nothing at all.  A reader arriving from
    ``jplib`` will reach for the machinery; it must not be there to reach for.
    """
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for stem in ("apl", "furikae", "auto_loan", "prem_loan", "grace", "continuation",
                 "default_rate", "pols_default"):
        assert not [n for n in names if stem in n], f"{stem}: an APL mechanic"
    a = whole_life.Projection[1]
    assert a.pols_lapse(4) == pytest.approx(
        a.pols_if(4) * (1 - a.mort_rate_mth(4)) * a.lapse_rate_mth(4), rel=1e-14)
    # Lapse is non-terminal in the contract, but through 부활 rather than through a loan.
    assert "pols_reinstate" in names
    assert a.reinstate_rate() == 0.0
    doc = flat(whole_life.Projection.doc)
    assert "자동대출납입" in doc and "unverified" in doc.lower()


def test_pitfall_there_is_no_paid_up_or_extended_term_option(whole_life):
    """감액완납 and 연장정기보험 appear in no retrieved Korean document, so not here.

    Both are in the Japanese 約款 and a reader arriving from ``jplib`` will look for them.
    What Korea offers in that slot is **감액**, a partial surrender paying k W(d) during
    납입기간 and nothing at all on a 무해지 contract — a different mechanic with a
    different consumer consequence, and the only one this model implements.
    """
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for stem in ("pua", "paid_up", "paidup", "extended_term", "ext_term",
                 "reduced_paid"):
        assert not [n for n in names if stem in n], f"{stem}: not a Korean feature"
    assert {"reduce_year", "reduce_frac", "sa_factor", "sum_assured_at"} <= names
    p = whole_life.Projection[10]
    assert p.claims(179, "REDUCTION") == pytest.approx(POINT_10_REDUCTION, abs=WON)
    assert p.premium_mth_at_pp(180) == pytest.approx(
        0.5 * p.premium_mth_pp(), rel=1e-14)
    assert p.premiums(180) == 0.0               # 10년납: the premium had already stopped
    assert "감액완납" in flat(whole_life.Projection.cells["result_cf"].doc)


def test_pitfall_a_refused_claim_is_not_a_zero_payment(whole_life):
    """상법 제736조 obliges the insurer to pay 「보험수익자를 위하여 적립한 금액」.

    The composite carries no exclusion incidence, so nothing is deducted anywhere — and
    that is the safe position.  Modelling an exclusion as forfeiture would overstate the
    insurer's position by the 계약자적립액 rather than by the claim, which is a large
    number on this contract and an easy one to reach for.  There are three benefit kinds
    and no fourth, and an unknown kind raises rather than returning zero.
    """
    a = whole_life.Projection[1]
    for stem in ("exclusion", "suicide", "myeonchaek", "forfeit", "contest"):
        names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
        assert not [n for n in names if stem in n], f"{stem}: an unmodelled exclusion"
    assert a.claims(9) == pytest.approx(
        a.claims(9, "DEATH") + a.claims(9, "LAPSE") + a.claims(9, "REDUCTION"),
        rel=1e-12)
    with pytest.raises(FormulaError):
        a.claims(9, "EXCLUDED")
    assert "제736조" in whole_life.Projection.cells["claims"].doc


def test_pitfall_there_is_no_severe_disability_benefit_to_add(whole_life):
    """One decrement on one amount: Korea puts no 고도장해보험금 at the sum assured here.

    The slot Japanese whole life fills with 高度障害 is filled in Korea by the **premium
    waiver**, which continues the contract rather than extinguishing it.  Adding a
    disability decrement at SA invents a benefit and double-counts an exit at the same
    time, which is the Japanese habit imported wholesale.
    """
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for stem in ("disab", "godo", "tpd", "accel", "living_needs"):
        assert not [n for n in names if stem in n], f"{stem}: a second decrement"
    doc = flat(whole_life.Projection.cells["mort_rate"].doc)
    assert "no separate disability decrement" in doc
    assert "고도장해" in doc
    a = whole_life.Projection[1]
    assert a.pols_death(4) == pytest.approx(
        a.pols_if(4) * a.mort_rate_mth(4), rel=1e-14)
    assert all(a.sum_assured_at(t) == a.sum_assured() for t in (0, 239, 468, 911))
    # The disability trigger is a state transition, not an exit.
    assert "waiver_rate" in names and "pols_waiver" in names


def test_pitfall_the_refund_ratio_test_is_not_the_value_test(whole_life):
    """check_cv_cliff asserts the **value**, never the 환급률 the press release frames.

    On model point 3 the 무해지 form's post-완납 환급률 is 1.081135 against the 표준형's
    0.843286 — above it, because the denominators differ — which satisfies
    제7-66조제4항제2호 나목 as recorded in the 고시 and contradicts the press-release
    reading 「전(全) 보험기간 동안 표준형 보험의 환급률 이내로」.  A model that asserts the
    press-release form fails on a legal design, so neither statement is asserted as a
    ratio and both are recorded as they stand.
    """
    nil, twin = whole_life.Projection[3], whole_life.Projection[2]
    assert nil.check_cv_cliff() is True
    # The value test: never above the twin's, at any month-end.
    for d in (1, 15, 120, 239, 240, 480, 720):
        assert nil.cv_pp(d) <= twin.cv_pp(d) + 1e-6
    assert nil.cv_pp(240) == pytest.approx(twin.cv_pp(240), rel=1e-12)
    # The ratio test: above the twin's from 납입완료, and the notes say so.
    assert nil.refund_ratio(240) == pytest.approx(POINT_3_REFUND_20, abs=RATIO)
    assert twin.refund_ratio(240) == pytest.approx(POINT_2_REFUND_20, abs=RATIO)
    assert nil.refund_ratio(240) > twin.refund_ratio(240) > 0.0
    assert nil.cum_prem_pp(240) < twin.cum_prem_pp(240)
    doc = flat(whole_life.Projection.cells["check_cv_cliff"].doc)
    assert "환급률" in doc and "neither is asserted here as a ratio" in doc


# ---------------------------------------------------------------------------
# Identities, recursions and the processing order


def test_the_nine_check_cells_this_model_publishes(whole_life):
    """Nine identities, named, each with its signed residual beside it.

    ``check_*`` takes no argument and returns one bool over all t, which is the
    library-wide form; the signed residual of the period that failed lives at
    ``check_*_resid(t)``.  That they are *true*, on all ten model points, is asserted by
    the sweep in ``test_model_conventions_kr.py``, which discovers them generically.
    Generic discovery cannot notice a check that has **gone** — it simply stops being
    discovered — so naming the set is the statement left here.
    """
    cells = set(whole_life.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == CHECK_CELLS
    for name in sorted(CHECK_CELLS):
        assert name + "_resid" in cells, name
        assert isinstance(getattr(whole_life.Projection[1], name)(), bool)


def test_the_in_force_roll_forward_closes_rebuilt_from_the_decrements(whole_life):
    """l(t) - l(t+1) = D(t) + S(t) - R(t+1), rebuilt outside the recursion that made it.

    The 부활 term is zero in the base run and is what makes the identity close once the
    module is on: a policy that comes back has not left, and netting it inside the lapse
    count would hide a decrement rather than model one.  Rebuilding the sum here rather
    than calling ``check_pols_roll_fwd`` is the point — the check and the recursion share
    a formula, and a shared formula cannot cross-check itself.
    """
    for point_id, name in ((1, "the anchor"), (10, "감액 + 부활")):
        p = whole_life.Projection[point_id]
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) - p.pols_reinstate(t + 1)
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(
                out, abs=1e-12), (name, t)
        assert p.pols_if(p.proj_len()) == 0.0


def test_the_decrements_sum_to_one_with_and_without_reinstatement(whole_life):
    """Every policy issued leaves by a modelled decrement, net of every 부활.

    On the anchor Sum D + Sum S = 1 outright.  On model point 10, where a fifth of each
    month's lapses returns **twelve months** later, the identity only closes once the
    returns are netted off — Sum D + Sum S - Sum R = 1 against a gross Sum S of 0.853 —
    which is the structural statement that lapse on this chassis is **not terminal**.  The
    lag is a real twelve-month interval on this grid where an annual step could only make
    it one period.
    """
    a = whole_life.Projection[1]
    ts = range(a.proj_len())
    assert sum(a.pols_death(t) + a.pols_lapse(t) for t in ts) == pytest.approx(
        1.0, abs=PROB)
    assert sum(a.pols_reinstate(t) for t in ts) == 0.0
    assert a.check_decrement_sum_resid(a.proj_len() - 1) == pytest.approx(0.0, abs=1e-10)

    p = whole_life.Projection[10]
    ts = range(p.proj_len())
    deaths = sum(p.pols_death(t) for t in ts)
    lapses = sum(p.pols_lapse(t) for t in ts)
    returns = sum(p.pols_reinstate(t) for t in ts)
    assert p.reinstate_rate() == 0.2
    assert returns == pytest.approx(0.2 * lapses, rel=1e-7)
    assert lapses > 0.85                        # gross of the returns, above one half
    assert deaths + lapses - returns == pytest.approx(1.0, abs=1e-10)
    assert p.pols_if(p.proj_len()) == 0.0
    assert p.check_decrement_sum() is True


def test_death_is_decremented_before_lapse(kr_whole_life_anchor):
    """The notes' [std] processing order: surrenders come from the survivors of mortality.

    Reversing it applies the lapse rate to the full in-force count, and the difference is
    not a rounding: the decrements would sum to 1.000356 rather than to 1, so the projection
    would no longer close at all, and surrender outgo would be overstated by ₩25,910 per
    policy issued over the run.  The order is asserted by checking a quantity that differs
    under the other one, not by reading the formula back.

    The monthly grid shrinks the damage by roughly the twelve it shrinks the step, which is
    the honest reading: an ordering error inside a month costs a twelfth of what the same
    error cost inside a year.  It is still an error, and it still stops the projection
    closing.
    """
    a = kr_whole_life_anchor
    ts = range(a.proj_len())
    for t in (0, 4, 239, 240, 468):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate_mth(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(a.pols_if(t + 1), abs=1e-14)
        assert a.pols_lapse(t) < a.pols_if(t) * a.lapse_rate_mth(t)

    reversed_lapses = sum(a.pols_if(t) * a.lapse_rate_mth(t) for t in ts)
    assert reversed_lapses == pytest.approx(0.4941486953, abs=PROB)
    assert reversed_lapses + SUM_DEATHS == pytest.approx(1.000356, abs=5e-7)
    overstatement = sum(
        (a.pols_if(t) * a.lapse_rate_mth(t) - a.pols_lapse(t)) * a.cv_pp(t + 1)
        for t in ts)
    assert overstatement == pytest.approx(25909.64, abs=WON)


def test_the_waiver_transition_precedes_the_premium(whole_life):
    """Step 2 of the processing order runs before step 3, and the difference is cash.

    ``waiver(t) = lp(t) u^m(t)`` moves out of the paying cohort **before** the premium is
    taken, so a policy waived in month t pays nothing in month t.  Taking the premium first
    would collect ₩87.26 of premium in the first month alone on model point 7 from policies
    whose premiums the contract has just waived — and that error is invisible in the base
    run, where u is identically zero.
    """
    p = whole_life.Projection[7]
    assert p.waiver_rate(0) == 0.004
    assert p.pols_waiver(0) == pytest.approx(
        p.pols_if_pay(0) * p.waiver_rate_mth(0), rel=1e-14)
    assert p.pols_pay_exp(0) == pytest.approx(p.pols_if_pay(0) - p.pols_waiver(0),
                                              rel=1e-14)
    assert p.premiums(0) == pytest.approx(
        p.premium_mth_pp() * (1 - p.waiver_rate_mth(0)), abs=WON)
    assert p.premium_mth_pp() * p.pols_if(0) - p.premiums(0) == pytest.approx(
        87.26, abs=WON)
    assert p.commissions(0) == pytest.approx(p.comm_init_pp() * p.pols_if(0), rel=1e-12)
    # And the waived cohort is exposed to the same decrements in the same month.
    assert p.pols_waived_exp(0) == pytest.approx(p.pols_waiver(0), rel=1e-14)
    assert p.pols_waived(1) == pytest.approx(
        p.pols_waiver(0) * (1 - p.mort_rate_mth(0)) * (1 - p.lapse_rate_mth(0)),
        rel=1e-14)


def test_the_reduction_is_taken_after_both_decrements(whole_life):
    """Step 9 follows steps 7 and 8: 감액 is paid on the policies continuing after both.

    Taking it on the start-of-month count would pay a partial surrender to policies that
    died or surrendered at the same month-end — ₩653,191.38 too much on model point 10, on a
    single row.  It is asserted here rather than left to ``check_net_cf``, because a ledger
    check verifies that the row adds up, not that the weight is right.
    """
    p = whole_life.Projection[10]
    assert p.reduce_year() == 15
    # Policy year 15 closes at the 계약해당일 d = 180, so the 감액 falls in the month
    # t = 179 and in no other: a monthly grid can put it on its date.
    assert p.claims(179, "REDUCTION") == pytest.approx(
        0.5 * max(0.0, p.cv_pp(180) - p.loan_pp(179)) * p.pols_if_at(179, "AFT_DECR"),
        rel=1e-12)
    assert p.pols_if_at(179, "AFT_DECR") < p.pols_if(179)
    naive = 0.5 * p.cv_pp(180) * p.pols_if(179)
    assert naive - p.claims(179, "REDUCTION") == pytest.approx(653191.38, abs=WON)
    assert all(p.claims(t, "REDUCTION") == 0.0
               for t in range(p.proj_len()) if t != 179)
    assert p.check_net_cf() is True


def test_the_account_rolls_forward_on_its_own_basis(kr_whole_life_anchor):
    """(V(t) + P^m 1{t<12m}) (1 + j_acc) = q^m SA + (1 - q^m) V(t+1), the retrospective form.

    The roll runs across month ``t``, from its opening month-end ``d = t`` to the closing one
    ``d = t + 1``, on the monthly table rate and the monthly accrual rate.  The account is a function of
    the anniversary, P, i_acc and q alone — not of the in-force count, the lapse rate or the
    waiver — because it is a per-policy contractual quantity, and that is exactly what lets
    the 표준형 twin be priced 「해지율을 적용하지 않고」 and still be the object the sold form's
    value is a fraction of.  A mis-set 납입기간, a rate applied on the wrong side of the
    equation or an off-by-one in the age q is read at all show up here and nowhere else.
    """
    a = kr_whole_life_anchor
    j = a.acc_int_rate_mth()
    assert a.check_pol_val_roll_fwd() is True
    for t in (0, 4, 83, 239, 240, 468, 828):
        assert a.check_pol_val_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-5)
        q = a.mort_rate_mth_at(t)
        prem = P_NET_MTH if t < 240 else 0.0
        assert (a.pol_val_pp(t) + prem) * (1 + j) == pytest.approx(
            q * 1e8 + (1 - q) * a.pol_val_pp(t + 1), abs=1e-5)
    assert a.pol_val_pp(0) == 0.0
    assert a.pol_val_pp(a.proj_len()) == 0.0    # V(T) is defined, not solved
    # No premium term in the recursion once premiums have stopped.
    q = a.mort_rate_mth_at(360)
    assert a.pol_val_pp(360) * (1 + j) == pytest.approx(
        q * 1e8 + (1 - q) * a.pol_val_pp(361), abs=1e-5)


def test_the_loan_balance_accumulates_at_the_vintage_loan_rate(whole_life):
    """L(t+1) = (L(t) + D(t)) (1 + i_L), with i_L = 예정이율 + 1.5% for the contract's life.

    Identically zero in the base run, where there is no loan at all, and non-trivial the
    moment the module is switched on — which is why it is asserted in both positions.  The
    advance is **not** a cash flow: no premium and no benefit moves in the draw year, and
    the loan shows up only later, as a deduction from every exit.
    """
    base = whole_life.Projection[1]
    assert base.loan_util() == 0.0
    assert base.check_loan_roll_fwd() is True
    assert all(base.loan_pp(d) == 0.0 for d in range(base.proj_len() + 1))
    assert all(base.loan_draw(t) == 0.0 for t in range(base.proj_len()))

    p = whole_life.Projection[6]
    assert p.loan_int_rate() == pytest.approx(0.025 + 0.015, rel=1e-12)
    assert (1 + p.loan_int_rate_mth()) ** 12 == pytest.approx(1.04, rel=1e-14)
    assert p.check_loan_roll_fwd() is True
    jl = p.loan_int_rate_mth()
    for t in range(p.proj_len() - 1):
        draw = p.loan_draw(t)
        assert p.loan_pp(t + 1) == pytest.approx(
            (p.loan_pp(t) + draw) * (1 + jl), abs=1e-6)
    assert p.loan_pp(109) == pytest.approx(p.loan_draw(108) * (1 + jl), rel=1e-12)
    assert p.loan_pp(120) == pytest.approx(
        p.loan_draw(108) * (1 + jl) ** 12, rel=1e-12)
    assert p.loan_pp(p.proj_len() - 1) == pytest.approx(POINT_6_LOAN_END, abs=WON)
    # The advance is not income and not outgo: the draw month is identical to the anchor's.
    assert p.net_cf(107) == pytest.approx(base.net_cf(107), rel=1e-14)
    assert p.net_cf(109) > base.net_cf(109)     # it shows up in reduced benefits
    assert p.claims(109, "DEATH") == pytest.approx(
        (p.sum_assured() - p.loan_pp(109)) * p.pols_death(109), rel=1e-12)


def test_the_published_cash_flow_statement_closes(whole_life):
    """net_cf equals the published columns of the same row, with no bare claims subtotal.

    A fourth benefit kind added to ``claims`` and left out of the statement would vanish
    silently without this; it shows up here instead.  The absence of a ``claims`` column
    is what makes the columns sum with nothing to skip, so it is asserted alongside.
    """
    for point_id in (1, 6, 7, 8, 10):
        p = whole_life.Projection[point_id]
        assert p.check_net_cf() is True
        df = p.result_cf()
        assert "claims" not in df.columns
        outgo = df[["claims_death", "claims_lapse", "claims_reduction",
                    "claim_expenses", "expenses", "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-6)


def test_the_result_tables_have_the_library_column_vocabulary(kr_whole_life_anchor):
    """pols_if first, net_cf last, one column per cash flow line, indexed by the 0-based t.

    ``result_val()`` publishes ``cv_pp`` and ``cv_susp_pp`` side by side, which is what
    lets the step at 납입완료 be read off one row of one table rather than inferred from
    two runs — on the row of month 239, whose closing month-end ``d = 240`` is where the
    step falls.  ``result_pols()`` publishes both the sourced annual rates and the monthly
    decrements derived from them: a reader checking a disclosure checks the first, a reader
    checking the roll-forward checks the second, and one of them is unreadable without the
    other.
    """
    a = kr_whole_life_anchor
    df = a.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "claims_reduction",
        "claim_expenses", "expenses", "commissions", "net_cf",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(PROJ_LEN))
    assert df.loc[0, "net_cf"] == pytest.approx(-2892089.79, abs=WON)

    val = a.result_val()
    assert list(val.columns) == [
        "pol_val_pp", "surr_chg_pp", "cv_std_pp", "cv_pp", "cv_susp_pp",
        "cum_prem_pp", "refund_ratio", "loan_pp",
    ]
    assert val.loc[239, "cv_pp"] / val.loc[239, "cv_susp_pp"] == pytest.approx(
        2.0, rel=1e-14)
    assert val.loc[239, "cv_pp"] == pytest.approx(WORKED_EXAMPLE_VAL[240][3], abs=WON)

    pols = a.result_pols()
    assert list(pols.columns) == [
        "pols_if", "pols_if_pay", "pols_waived", "pols_death", "pols_lapse",
        "pols_surr", "pols_reinstate", "mort_rate", "mort_rate_mth", "lapse_rate",
        "lapse_rate_mth",
    ]
    # The monthly decrement is below the annual one everywhere except the terminal year,
    # where the annual rate is 1 and the UDD spread runs the monthly rate up to 1 with it.
    ordinary = pols.iloc[:-12]
    assert (ordinary["mort_rate_mth"] < ordinary["mort_rate"]).all()
    assert (pols["lapse_rate_mth"] < pols["lapse_rate"]).all()
    assert pols["mort_rate_mth"].iloc[-1] == 1.0 == pols["mort_rate"].iloc[-1]
    assert (pols["pols_surr"] == pols["pols_lapse"]).all()      # no 부활 in the base run


def test_net_cf_carries_the_notes_own_sign(whole_life):
    """The notes' CF(t) is already income-positive, so there is no liability_cf here.

    One deep negative month at issue, 239 positive ones while the premium runs, and then
    672 negative months with no premium at all.  A model that published the outgo-positive
    orientation under this name would invert every conclusion the notes draw about where
    this contract makes money.
    """
    assert "liability_cf" not in whole_life.Projection.cells
    a = whole_life.Projection[1]
    assert a.net_cf(0) < -2000000.0
    assert all(a.net_cf(t) > 0.0 for t in range(1, 240))
    assert all(a.net_cf(t) < 0.0 for t in range(240, a.proj_len()))
    assert a.net_cf(0) == pytest.approx(
        a.premiums(0) - a.claims(0) - a.claim_expenses(0) - a.expenses(0)
        - a.commissions(0), rel=1e-12)


def test_there_is_no_maturity_benefit_and_no_tail_states(whole_life):
    """종신 means no expiry date and no 만기보험금, so nothing is paid at the horizon.

    Only the death benefit falls in the last period, and it falls on everybody, because the
    table's terminal rate is 1.  There is no maturity cells and no maturity kind, unlike
    the term models in this library whose survivors reach the end of the term with their
    cover simply running out.
    """
    a = whole_life.Projection[1]
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    for absent in ("pols_maturity", "claims_maturity", "policy_term", "maturity_age",
                   "benefit_maturity_pp"):
        assert absent not in names, f"{absent}: this contract does not mature"
    t_end = a.proj_len() - 1
    assert a.claims(t_end) == pytest.approx(a.claims(t_end, "DEATH"), rel=1e-12)
    assert a.pols_lapse(t_end) == 0.0
    assert a.pols_if(t_end + 1) == 0.0
    with pytest.raises(FormulaError):
        a.claims(0, "MATURITY")


def test_the_horizon_is_the_tables_terminal_age_not_a_round_number(whole_life):
    """omega = 115 for both sexes, and T = 12 (omega - x + 1) on every model point.

    Projecting a Korean whole life contract to 100 truncates the liability and projecting
    it to 120 invents one.  The terminal rate is 1 whatever ``mort_be_factor`` is set to,
    because ``omega_age`` is a structural property of the projection rather than an
    experience assumption — model point 10 runs the factor at 0.90 and the terminal rate
    does not move.
    """
    male, female = whole_life.Projection[1], whole_life.Projection[4]
    assert male.omega_age() == female.omega_age() == 115
    assert male.sex() == "M" and female.sex() == "F"
    assert male.proj_years() == 115 - 40 + 1 == PROJ_YEARS
    assert male.proj_len() == 12 * (115 - 40 + 1) == PROJ_LEN
    assert female.proj_len() == 12 * (115 - 30 + 1) == POINT_4_PROJ_LEN
    assert male.age(male.proj_len() - 1) == 115
    assert male.mort_rate(male.proj_len() - 1) == 1.0
    assert male.pols_if(male.proj_len() - 1) > 0.0
    # The terminal year is twelve populated rows, not one: the certain death at omega is
    # spread uniformly over them rather than falling in the first.
    assert male.pols_if(male.proj_len() - 12) > male.pols_if(male.proj_len() - 1) > 0.0
    assert len(female.result_cf()) == POINT_4_PROJ_LEN

    lever = whole_life.Projection[10]
    assert lever.mort_be_factor() == 0.90
    assert lever.mort_rate(0) == pytest.approx(0.90 * lever.mort_rate_base(0), rel=1e-12)
    assert lever.mort_rate(lever.proj_len() - 1) == 1.0
    assert male.mort_be_factor() == 1.00
    assert male.mort_rate(0) == pytest.approx(male.mort_rate_base(0), rel=1e-14)
    # The 산출방법서 basis is not a best-estimate lever, so P reads the table straight.
    assert lever.prem_net_level_pp() == pytest.approx(
        lever.sum_assured() * lever.epv_death(50) / lever.annuity_due(50, 10),
        rel=1e-12)


def test_invalid_enum_values_raise(whole_life):
    """The enum accessors validate rather than propagating a typo into a lookup.

    Five of this model's inputs are enumerations — sex, the crediting basis, the lapse
    basis, the timing of an in-force read and the benefit kind — and a mistyped one that
    silently returned a default would move the answer without moving anything visible.
    """
    a = whole_life.Projection[1]
    with pytest.raises(FormulaError):
        a.pols_if_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        a.claims(0, "SURRENDER")
    assert a.sex() in ("M", "F")
    assert a.int_basis() in ("fixed", "linked")
    assert a.lapse_basis() in tuple(whole_life.Data.lapse_table().index)


# ---------------------------------------------------------------------------
# The [std] parameters, read off the model


def test_the_std_scalar_assumptions_are_the_ones_the_notes_state(whole_life):
    """Twenty-two Projection References, each a number a document commits to.

    Every one of them is either [std] with a stated rationale or a figure copied from
    별표 14, and every one of them moves the worked example.  Reading them off the model
    here means a silent change to an assumption fails a test rather than quietly moving a
    result and leaving the notes describing a model that no longer exists.
    """
    refs = whole_life.Projection.refs
    for name, value in STD_SCALARS.items():
        assert name in refs, name
        assert refs[name] == pytest.approx(value, rel=1e-15), name
    # The 별표 14 parameters reproduce the cap, which is the reason they are separate.
    a = whole_life.Projection[1]
    assert a.surr_chg_cap_pp() == pytest.approx(
        0.05 * 20 * a.prem_net_20yr_pp() + 0.01 * a.sum_assured(), rel=1e-14)
    assert a.surr_chg_cap_pp() == pytest.approx(
        a.prem_net_20yr_pp() + 0.01 * a.sum_assured(), rel=1e-14)
    # And the two published bounds on the acquisition block both hold, without binding.
    assert a.acq_cost_pp() == pytest.approx(a.surr_chg_cap_pp(), rel=1e-14)
    assert a.acq_cost_pp() < 1.4 * a.surr_chg_cap_pp()
    assert 1.4 * a.surr_chg_cap_pp() == pytest.approx(4349380.75, abs=WON)
    assert a.comm_init_pp() == pytest.approx(0.65 * a.acq_cost_pp(), rel=1e-14)
    assert a.comm_init_pp() < a.premium_pp()
    assert a.check_acq_cost_cap() is True


def test_the_first_year_commission_cap_binds_where_the_notes_say_it_does(whole_life):
    """제4-32조제5항 caps first-year remuneration at the first year's expected premium.

    It does **not** bind on the anchor — 0.65 x ₩3,106,700.54 against a premium of
    ₩2,776,140 — and it does bind on model point 4, a 30년납 contract whose premium is
    small against a cap computed on a 20년납 footing.  A cap that never binds anywhere in
    the shipped table is a cap nobody has tested, so the point that reaches it matters.
    """
    a = whole_life.Projection[1]
    assert a.comm_init_pp() == pytest.approx(0.65 * a.acq_cost_pp(), rel=1e-14)
    assert 0.65 * a.acq_cost_pp() < a.premium_pp()

    p = whole_life.Projection[4]
    assert p.prem_term() == 30
    assert 0.65 * p.acq_cost_pp() > p.premium_pp()
    assert p.comm_init_pp() == pytest.approx(p.premium_pp(), rel=1e-14)
    assert p.comm_init_pp() == 716780.0
    assert p.check_acq_cost_cap() is True
    assert p.check_acq_cost_cap_resid(0) == pytest.approx(0.0, abs=1e-6)
    assert p.check_acq_cost_cap_resid(1) == 0.0


def test_the_lapse_table_holds_two_bases_and_three_parameters_each(whole_life):
    """Two rows, not a rate per policy year, because the convergence point is 납입완료.

    A 7년납 contract converges in policy year 7 — the period t = 6 — and a 30년납 one in
    policy year 30 on the same two rows,
    which is why the file is parameterized rather than tabulated — and why the bonus-date
    spike is a Projection Reference rather than a row, so it can be switched off and its
    effect read directly.  Folding either into a duration curve would make a behavioural
    assumption look like an observation.
    """
    table = whole_life.Data.lapse_table()
    assert set(table.index) == {"loglinear", "flat"}
    assert list(table.columns) == [
        "first_year_rate", "completion_rate", "ultimate_rate", "provenance"]
    assert table.loc["loglinear", "first_year_rate"] == 0.10
    assert table.loc["loglinear", "completion_rate"] == 0.001
    assert table.loc["loglinear", "ultimate_rate"] == 0.008
    assert (table.loc["flat"][["first_year_rate", "completion_rate",
                              "ultimate_rate"]] == 0.04).all()
    assert table["provenance"].notna().all()
    assert "[REG-R27]" in table.loc["loglinear", "provenance"]
    assert table.loc["flat", "provenance"].startswith("[std]")
    assert "lapse_spike" not in table.columns
    assert "lapse_bonus_spike" in whole_life.Projection.refs

    # Both endpoints are reached exactly on a 7년납 point as well as on a 20년납 one, at
    # the first month of the policy year each is quoted against.
    short = whole_life.Projection[8]
    assert short.lapse_rate_base(0) == 0.10
    assert short.lapse_rate_base(12 * 6) == pytest.approx(0.001, abs=PROB)
    assert short.lapse_rate_base(12 * 7) == 0.008


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Three row kinds, every row [std], and no row is a 경험생명표 value.

    The 제10회 경험생명표 is not published in full — only its 평균수명 and 기대여명 are
    released — so unlike ``jplib``, where the 生保標準生命表 is free to read, there is no
    published Korean insured rate to anchor a proxy on.  Marking the rows is what stops
    the file being mistaken for the table it stands in for, and asserting the marking is
    what stops the marking going stale.
    """
    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert len(table) == 202
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith("[std]").all()

    anchors = table[table["provenance"].str.contains("ANCHOR")]
    constructed = table[table["provenance"].str.contains("CONSTRUCTED")]
    terminal = table[table["provenance"].str.contains("TERMINAL")]
    assert len(anchors) + len(constructed) + len(terminal) == len(table)
    assert len(anchors) == 6                    # 보험나이 20, 40, 60, both sexes
    assert len(terminal) == 2
    assert set(anchors["age"]) == {20, 40, 60}
    assert anchors["provenance"].str.contains("the mean of the only two Korean").all()
    assert anchors["provenance"].str.contains(r"\[S2\]").all()
    assert anchors["provenance"].str.contains(r"\[S8\]").all()
    assert constructed["provenance"].str.contains("경험생명표").all()

    # The two rates the worked example quotes, and the mean that made each of them.
    male = table[table["sex"] == "M"].set_index("age")
    assert male.loc[40, "mort_rate"] == 0.00085
    assert male.loc[40, "mort_rate"] == pytest.approx((0.00078 + 0.00092) / 2, rel=1e-14)
    assert male.loc[60, "mort_rate"] == 0.005075
    assert male.loc[60, "mort_rate"] == pytest.approx((0.00455 + 0.00560) / 2, rel=1e-14)
    assert "0.00078" in male.loc[40, "provenance"]
    assert "0.00092" in male.loc[40, "provenance"]

    for sex in ("M", "F"):
        sub = table[table["sex"] == sex]
        assert sub["age"].min() == 15 and sub["age"].max() == 115
        assert len(sub) == 101
        assert sub[sub["mort_rate"] >= 1.0]["age"].tolist() == [115]
        assert "omega = 115" in terminal[terminal["sex"] == sex]["provenance"].iloc[0]


def test_the_shipped_mortality_table_obeys_its_own_construction_rule():
    """Every row below 60 is the log-linear fill its provenance claims, to 8 d.p.

    The provenance column states a construction rule; this asserts the file obeys it.  A
    rate edited by hand — or an anchor quietly relabelled — changes a row the rule can
    still reproduce from its neighbours, so nothing but this test would catch it.  Above
    60 the rows follow the Gompertz-with-deceleration whose two solved parameters the
    provenance prints to six significant figures, which is why that limb is checked to a
    relative tolerance rather than to the file's own precision.
    """
    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    for sex in ("M", "F"):
        sub = table[table["sex"] == sex].set_index("age")
        anchors = {age: sub.loc[age, "mort_rate"] for age in (20, 40, 60)}
        for age in range(15, 60):
            if age in anchors:
                continue
            lo, hi = (20, 40) if age < 40 else (40, 60)
            f = (age - lo) / (hi - lo)
            fill = round(math.exp((1 - f) * math.log(anchors[lo])
                                 + f * math.log(anchors[hi])), 8)
            assert sub.loc[age, "mort_rate"] == pytest.approx(fill, abs=5e-11), (
                sex, age)

        prov = sub.loc[61, "provenance"]
        b = float(re.search(r"b = ([\d.]+)", prov).group(1))
        c = float(re.search(r"c = ([\d.]+)", prov).group(1))
        for age in range(61, 115):
            fit = math.exp(math.log(anchors[60]) + b * (age - 60)
                           + c * (age - 60) ** 2)
            assert sub.loc[age, "mort_rate"] == pytest.approx(fit, rel=5e-5), (sex, age)
        assert sub.loc[115, "mort_rate"] == 1.0
        assert all(sub.loc[a, "mort_rate"] < sub.loc[a + 1, "mort_rate"]
                   for a in range(15, 115))


def test_the_model_point_table_ships_ten_points_and_the_anchor_is_sourced(whole_life):
    """Twenty columns, ten points, and point 1 is the cell the notes project.

    Point 2 is the 표준형 comparison twin at the identical cell, so the pair differ in k
    and in the premium alone and every comparison the notes draw between them is a
    comparison of one contract with itself.  The premium relation between them is the one
    quantitative fact the whole worked example rests on, so it is asserted from the CSV as
    well as from the model.
    """
    table = whole_life.Data.model_point_table()
    assert len(table) == 10
    assert list(table.index) == list(range(1, 11))
    assert table.index.name == "point_id"
    for column in ("sex", "issue_age", "sum_assured", "prem_term", "premium_annual",
                   "cv_floor_ratio", "prem_susp_ratio", "int_basis", "decl_rate",
                   "lapse_basis", "waiver_rate", "loan_util", "loan_year", "bonus_rate",
                   "reduce_year", "reduce_frac", "reinstate_rate", "mort_be_factor"):
        assert column in table.columns, column

    assert table.loc[1, "policy_id"] == "WL-KR-0001"
    assert table.loc[1, "sex"] == "M"
    assert int(table.loc[1, "issue_age"]) == 40
    assert float(table.loc[1, "sum_assured"]) == 1e8
    assert int(table.loc[1, "prem_term"]) == 20
    assert float(table.loc[1, "premium_annual"]) == G_GROSS
    assert float(table.loc[1, "cv_floor_ratio"]) == 0.50
    assert float(table.loc[1, "prem_susp_ratio"]) == 0.90
    assert float(table.loc[2, "premium_annual"]) == 3084600.0
    assert float(table.loc[1, "premium_annual"]) == pytest.approx(
        0.90 * float(table.loc[2, "premium_annual"]), abs=WON)

    # The envelope the notes claim: both sexes, four suppression factors, 전기납 present.
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["cv_floor_ratio"]) == {0.0, 0.3, 0.5, 1.0}
    assert 0 in set(table["prem_term"])
    assert table["issue_age"].min() == 30 and table["issue_age"].max() == 65
    assert table["sum_assured"].min() == 1e7 and table["sum_assured"].max() == 1e9
    assert set(table["lapse_basis"]) == {"loglinear", "flat"}
    assert set(table["int_basis"]) == {"fixed", "linked"}
    # Every optional module is exercised somewhere in the table.
    for column in ("waiver_rate", "loan_util", "bonus_rate", "reduce_frac",
                   "reinstate_rate"):
        assert (table[column] > 0).any(), column
    assert (table["mort_be_factor"] != 1.0).any()


# ---------------------------------------------------------------------------
# Inputs


def test_inputs_live_beside_the_model():
    """The three input CSVs sit in the model folder's parent directory.

    The model folder holds formulas only, so a copy of it made without its parent's CSVs
    reads and then fails on first evaluation — which is the trade this layout makes, and
    the reason the file set is asserted rather than assumed.
    """
    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}
    assert not [p for p in MODEL_DIR.rglob("*.csv")]


def test_the_csvs_are_utf8_without_a_bom():
    """The provenance columns are Korean, so the encoding is load-bearing.

    A BOM at the head of a CSV becomes part of the first column name, so the reader stops
    finding ``point_id`` and the failure surfaces a long way from its cause.
    """
    for name in ("model_point_table.csv", "mort_table.csv", "lapse_table.csv"):
        raw = (MODEL_DIR.parent / name).read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"{name} carries a BOM"
        text = raw.decode("utf-8")
        assert text.endswith("\n")
        assert "\r\n" not in text


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a same-schema file and the projection follows.

    This is the property the external-file layout buys, and it is exactly what a user with
    a real 산출방법서 does with the mortality basis: drop the carrier's own 적용위험률 in as
    a CSV, change no formula.

    Doubling every **annual** rate does **not** double the first month's death claims, and
    that is the check rather than a defect: ``1 - (1 - 2q)^(1/12)`` is larger than
    ``2 (1 - (1 - q)^(1/12))``, because doubling an annual probability more than doubles the
    force behind it and the monthly step sees the force.  Asserting linearity here would be
    asserting that the model converts by dividing.
    """
    model = product_copy(tmp_path, "WholeLife_KR_S_swap")
    try:
        src = model.Data.input_dir() / "mort_table.csv"
        doubled = pd.read_csv(src, index_col=["sex", "age"])
        doubled["mort_rate"] = (doubled["mort_rate"] * 2).clip(upper=1.0)
        alt = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt)

        base = model.Projection[1].claims(0, "DEATH")
        assert base == pytest.approx(7086.09, abs=WON)
        model.Data.mort_table_file = alt
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[1]
        assert model.Data.mort_table_file == alt
        assert p.mort_rate_at_age(40) == pytest.approx(2 * 0.00085, rel=1e-12)
        assert p.mort_rate(0) == pytest.approx(2 * 0.00085, rel=1e-12)
        assert p.mort_rate_mth(0) == pytest.approx(
            1.0 - (1.0 - 2 * 0.00085) ** (1.0 / 12.0), rel=1e-12)
        claim = p.claims(0, "DEATH")
        assert claim == pytest.approx(2 * base, rel=1e-3)
        assert claim > 2 * base
    finally:
        model.close()


def test_round_trip_reproduces_the_goldens(tmp_path):
    """read -> write -> re-read reproduces the worked example and the same file set.

    ``test_model_conventions_kr.py`` asserts that the round trip is *stable* across the
    library; what it cannot assert is that this product's own numbers survive it, which is
    the statement a reader of the notes actually needs.  The inputs are external, so they
    have to travel with the model for the re-read to project at all.
    """
    model = mx.read_model(MODEL_DIR, name="WholeLife_KR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="WholeLife_KR_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[7], abs=WON)
        for d, row in WORKED_EXAMPLE_VAL.items():
            assert anchor.cv_pp(d) == pytest.approx(row[3], abs=WON)
            assert anchor.cv_susp_pp(d) == pytest.approx(row[4], abs=WON)
        assert anchor.result_cf()["net_cf"].sum() == pytest.approx(
            TOTALS["net_cf"], abs=TOTAL)
        assert {c for c in reread.Projection.cells
                if c.startswith("check_") and not c.endswith("_resid")} == CHECK_CELLS
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
