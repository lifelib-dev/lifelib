"""Golden and structural tests for Cancer_KR_S.

The golden values are the worked example in
products/cancer/technical-notes.md ("Worked example"), which projects the anchor cell
M40 / 100세 만기 20년납 / 비갱신형 / 해약환급금 미지급형 / KRW 30,000,000 of
보험가입금액 / KRW 45,000 a month — the cell 감독규정 제1-2조제2호 itself computes at, the
기준연령 요건 being 「전기납 및 월납 조건으로 남자가 만 40세에 보험에 가입하는 경우」.  They
are hard-coded here rather than pickled so that a reviewer can lay the module beside the
notes and compare by eye.

Tolerances follow the precision the notes display: the sixteen-month table to the ten
decimals it prints, the boundary rows to six, the hand traces' diagnosis flows to the
fourteen decimals they are written out at, and the decrement and incidence bases to the
ten or twelve their own lines carry.

This is the library's **fixed-benefit (정액) 제3보험 chassis**, so what is asserted here is
what ``LTC_KR_S`` and ``Child_KR_S`` inherit rather than restate: the **two** waiting
periods and the hard zero inside the invasive one, the 감액기간 as a first-year phenomenon,
the 유사암 tier as an additive second benefit on its own once-only ledger, the three-state
population with its six select-duration cohorts, and the 계약자적립액 that a 제3보험
contract must pay on a death it does not cover.

Beyond the worked example this module asserts every product fact the notes list under
"Known modeling pitfalls", because each of them is a way an implementation can look right
and be wrong.  There is one ``test_pitfall_*`` per bullet, naming the pitfall in its
docstring: two waiting periods rather than one, and a 면책기간 that stops the *transition*
as well as the benefit while the premium goes on being charged; an in-window diagnosis that
voids rather than lapses; premium riding on ``pols_healthy + pols_minor`` while the
maintenance expense rides on ``pols_if``; 특정소액암 neither waiving nor being barred from
lapsing where a waived life is; 고액암 as a subset paid **in addition** and 유사암 as
**additive** with a share that exceeds 1.0; the 감액기간 that must not be baked into a
benefit ratio; diagnosis lines on flows against care lines on stocks, the care limbs
starting a month later; a cohort delay of thirteen months and not twelve; a treatment
ledger that is per diagnosed life with a zero ultimate hazard, and a 유사암 ledger that is
per policy; relative survival converted to an excess hazard rather than multiplied into
survivorship; a 유사암 tier with neither excess mortality nor a care benefit; a notional
보험가입금액 inside the 표준해약공제액; a 7-year 해약공제기간 that is *not* the 납입완료
cliff, and two prescribed steps landing in the same row; ``claims_lapse`` identically zero
through the 납입기간; a payment on death with no death benefit, and an account floor that
binds; ``risk_prem_pp`` excluding the two lines paid out of the account; nothing paid at
expiry; ten ``claims_*`` splits and no ``claims`` column; rounded lines that do not re-add
and a commission carrying its own floating-point residue; ``proj_len()`` as the row count
rather than the last index; log-linear incidence against linear tier shares; [std]
incidence rows above age 80 that the projection reaches; 부활 re-running the 90 days; and
the indemnity machinery of ``Medical_KR_S`` that this chassis must not borrow.

The ten ``check_*`` cells are asserted **by name**, because a generic sweep cannot notice a
check that has quietly disappeared, and the [std] scalar assumptions are read off the model
so that a silent change to an assumption fails a test rather than moving a result.  The
whole-table sweep belongs to ``test_model_conventions_kr.py``; the model points taken here
are the ones that exercise a particular mechanic.
"""
import math

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
MONEY = 5e-9         # money displayed to 10 d.p.
SIX = 5e-7           # money displayed to 6 d.p.
INFORCE = 5e-11      # policy counts, displayed to 10 d.p.
FLOW = 1e-14         # diagnosis flows, displayed to 14 d.p.
RATE = 5e-13         # decrement and incidence rates, displayed to 12 d.p.

MODEL_DIR = LIB / MODELS["Cancer_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "First periods of the base run", table 1: t -> (pols_if, healthy, minor, waived).
WE_POLS = {
    0:  (1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000),
    1:  (0.9959914690, 0.9959914690, 0.0000000000, 0.0000000000),
    2:  (0.9919990063, 0.9919990063, 0.0000000000, 0.0000000000),
    3:  (0.9880225475, 0.9880225475, 0.0000000000, 0.0000000000),
    4:  (0.9840612075, 0.9839518955, 0.0000197422, 0.0000895698),
    5:  (0.9801149387, 0.9798980147, 0.0000392427, 0.0001776813),
    6:  (0.9761836936, 0.9758608358, 0.0000585040, 0.0002643538),
    7:  (0.9722674247, 0.9718402900, 0.0000775283, 0.0003496064),
    8:  (0.9683660844, 0.9678363090, 0.0000963178, 0.0004334576),
    9:  (0.9644796254, 0.9638488243, 0.0001148748, 0.0005159263),
    10: (0.9606080001, 0.9598777680, 0.0001332015, 0.0005970306),
    11: (0.9567511612, 0.9559230725, 0.0001513001, 0.0006767886),
    12: (0.9529090613, 0.9519846704, 0.0001691728, 0.0007552182),
    13: (0.9497671846, 0.9487370834, 0.0001898413, 0.0008402599),
    14: (0.9466348029, 0.9455005753, 0.0002102819, 0.0009239457),
    15: (0.9435118979, 0.9422751081, 0.0002304966, 0.0010062932),
}

# Table 2: t -> (premiums, diag_gen, diag_high, diag_minor, diag_similar).
WE_DIAG = {
    0:  (45000.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 177.9475000000),
    1:  (44819.6161043715, 0.0000000000, 0.0000000000, 0.0000000000, 177.2236791336),
    2:  (44639.9552831831, 0.0000000000, 0.0000000000, 0.0000000000, 176.5028024875),
    3:  (44461.0146379684, 1360.1145372945, 49.7602879498, 179.1334279764, 175.7848580859),
    4:  (44278.7236965491, 1354.5380432401, 49.5562698746, 178.3953984216, 175.0696879449),
    5:  (44097.1765825684, 1348.9843037453, 49.3530842834, 177.6604095480, 174.3572831176),
    6:  (43916.3702899898, 1343.4532268520, 49.1507278117, 176.9284488278, 173.6476346630),
    7:  (43736.3018246864, 1337.9447209662, 48.9491971085, 176.1995037851, 172.9407336464),
    8:  (43556.9682043961, 1332.4586948569, 48.7484888362, 175.4735619952, 172.2365711397),
    9:  (43378.3664586762, 1326.9950576548, 48.5485996703, 174.7506110849, 171.5351382220),
    10: (43200.4936288586, 1321.5537188506, 48.3495262994, 174.0306387316, 170.8364259796),
    11: (43023.3467680051, 1316.1345882941, 48.1512654254, 173.3136326638, 170.1404255064),
    12: (42846.9229408627, 2862.2789611635, 103.9867356580, 397.5372102810, 360.2731924222),
    13: (42701.7116126315, 2852.5784887687, 103.6343170181, 396.1810575071, 359.0626773615),
    14: (42556.9885736717, 2842.9106353042, 103.2830834255, 394.8295310933, 357.8559029089),
    15: (42412.7522107091, 2833.2752929993, 102.9330309649, 393.4826152575, 356.6528614724),
}

# Table 3: t -> (claims_hosp, claims_surgery, claims_treat, claims_death, claims_lapse).
WE_CARE = {
    0:  (0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0),
    1:  (0.0000000000, 0.0000000000, 0.0000000000, 3.5064829465, 0.0),
    2:  (0.0000000000, 0.0000000000, 0.0000000000, 6.9920489980, 0.0),
    3:  (0.0000000000, 0.0000000000, 0.0000000000, 10.5917132184, 0.0),
    4:  (13.6639954092, 30.0607899003, 59.9916774089, 14.1079661237, 0.0),
    5:  (27.1155078447, 59.6541172583, 119.0504497901, 17.6764456658, 0.0),
    6:  (40.3572320206, 88.7859104453, 177.1881482675, 21.2953107206, 0.0),
    7:  (53.3918300637, 117.4620261402, 234.4164608907, 24.9627590288, 0.0),
    8:  (66.2219319043, 145.6882501894, 290.7469343496, 28.6770264535, 0.0),
    9:  (78.8501356613, 173.4702984548, 346.1909756681, 32.4363862524, 0.0),
    10: (91.2790080240, 200.8138176528, 400.7598538775, 36.2391483628, 0.0),
    11: (103.5110846284, 227.7243861826, 454.4647016704, 40.0836587013, 0.0),
    12: (115.5488704295, 254.2075149449, 507.3165170339, 47.1268021938, 0.0),
    13: (128.7626505282, 283.2778311620, 565.3315272335, 51.1537996721, 0.0),
    14: (141.7784544051, 311.9125996912, 622.4773241996, 55.2230020278, 0.0),
    15: (154.5987250024, 340.1171950053, 678.7646336531, 59.3328420042, 0.0),
}

# Table 4: t -> (expenses, claim_expenses, commissions, net_cf).
WE_TAIL = {
    0:  (302500.0000000000, 8.8973750000, 323999.9999999999, -581686.8448750000),
    1:  (2489.9786724651, 8.8611839567, 0.0000000000, 42140.0460858697),
    2:  (2479.9975157324, 8.8251401244, 0.0000000000, 41967.6377758408),
    3:  (2470.0563687760, 25.3759454102, 0.0000000000, 40190.1974992572),
    4:  (2460.1530187687, 25.8186812864, 0.0000000000, 39917.3681681708),
    5:  (2450.2873468075, 26.2533343329, 0.0000000000, 39646.7843001748),
    6:  (2440.4592340447, 26.6800107630, 0.0000000000, 39378.4244055737),
    7:  (2430.6685616925, 27.0988154909, 0.0000000000, 39112.2672158733),
    8:  (2420.9152110277, 27.5098521483, 0.0000000000, 38848.2916814952),
    9:  (2411.1990633969, 27.9132230988, 0.0000000000, 38586.4769695119),
    10: (2401.5200002211, 28.3090294540, 0.0000000000, 38326.8024614052),
    11: (2391.8779030002, 28.6973710878, 0.0000000000, 38069.2477508447),
    12: (2429.9181063839, 31.2529895192, 1285.4076882259, 34452.0683526068),
    13: (2421.9063208058, 31.6914742116, 1281.0513483789, 34227.0801199841),
    14: (2413.9187473808, 32.1223350179, 1276.7096572102, 34003.9673010072),
    15: (2405.9553395705, 32.5456687957, 1272.3825663213, 33782.7114396626),
}

# "Where the product does something else": t -> (pols_if, premiums, diag_gen, diag_high,
# diag_minor, diag_similar, hosp, surgery, treat, death, lapse, expenses, claim_expenses,
# commissions, net_cf), to the six decimals the notes print.
BOUNDARY_ROWS = {
    11:  (0.956751, 43023.346768, 1316.134588, 48.151265, 173.313633, 170.140426,
          103.511085, 227.724386, 454.464702, 40.083659, 0.000000,
          2391.877903, 28.697371, 0.000000, 38069.247751),
    12:  (0.952909, 42846.922941, 2862.278961, 103.986736, 397.537210, 360.273192,
          115.548870, 254.207515, 507.316517, 47.126802, 0.000000,
          2429.918106, 31.252990, 1285.407688, 34452.068353),
    119: (0.785353, 34901.656258, 4692.290682, 159.964455, 944.437226, 451.865648,
          489.334401, 880.077229, 1420.255917, 906.917956, 0.000000,
          2346.422980, 68.585360, 1047.049688, 21494.454715),
    120: (0.784650, 34865.602577, 5113.201637, 172.743299, 1073.232817, 471.395893,
          492.943174, 886.344818, 1429.357941, 978.544115, 0.000000,
          2391.210442, 72.461331, 1045.968077, 20738.199034),
    239: (0.721042, 31258.960304, 9080.571642, 278.670238, 2657.890070, 466.293749,
          1151.998683, 2027.265221, 3078.597257, 4120.391242, 0.000000,
          2626.054278, 143.816539, 937.768809, 4689.642576),
    240: (0.720477, 0.000000, 9780.214009, 296.370121, 2966.565180, 451.223219,
          1159.012327, 2039.351451, 3095.888707, 4450.535298, 1891.707642,
          2676.477235, 149.922328, 0.000000, -28957.267518),
    241: (0.719468, 0.000000, 9763.318813, 295.858146, 2960.815303, 450.542932,
          1167.052480, 2053.328281, 3116.263786, 4447.499178, 1885.957387,
          2672.727355, 150.239115, 0.000000, -28963.602775),
    446: (0.434675, 0.000000, 14822.256894, 461.034429, 4456.604822, 334.746937,
          2217.452034, 3741.323495, 5042.783514, 25.822052, 1.934041,
          2261.052691, 255.173569, 0.000000, -33620.184478),
    447: (0.432786, 0.000000, 14744.458887, 458.614584, 4430.480887, 333.247172,
          2214.916824, 3736.203514, 5031.635754, 0.000000, 0.000000,
          2251.226614, 254.448004, 0.000000, -33455.232240),
    479: (0.371671, 0.000000, 13198.968285, 411.824283, 3919.401998, 259.848037,
          2094.778916, 3508.796918, 4602.302173, 0.000000, 0.000000,
          2011.433308, 235.406752, 0.000000, -30242.760672),
    480: (0.369770, 0.000000, 13596.651745, 424.895367, 4052.271541, 243.921552,
          2089.888822, 3499.843779, 4586.811501, 0.000000, 0.000000,
          2041.166555, 237.864350, 0.000000, -30773.315212),
    599: (0.135885, 0.000000, 4993.011333, 156.031604, 1366.066002, 100.166614,
          932.150480, 1505.615216, 1708.177851, 0.000000, 0.000000,
          896.438531, 101.361693, 0.000000, -11759.019323),
    600: (0.134236, 0.000000, 4996.240153, 156.132505, 1365.911126, 100.330241,
          921.926541, 1488.725694, 1687.021137, 0.000000, 0.000000,
          903.268232, 100.728268, 0.000000, -11720.283897),
    719: (0.010679, 0.000000, 347.231748, 10.850992, 86.923956, 7.855782,
          78.614795, 122.553239, 116.006557, 0.000000, 0.000000,
          85.878313, 8.311038, 0.000000, -864.226420),
    720: (0.010345, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
          0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
          0.000000, 0.000000, 0.000000, 0.000000),
}

BOUNDARY_COLUMNS = (
    "pols_if", "premiums", "claims_diag_gen", "claims_diag_high", "claims_diag_minor",
    "claims_diag_similar", "claims_hosp", "claims_surgery", "claims_treat",
    "claims_death", "claims_lapse", "expenses", "claim_expenses", "commissions",
    "net_cf",
)

# "The 계약자적립액 and 해약환급금 path": t -> (av_pp, surr_chg_pp, cv_std_pp, cv_pp).
ACCOUNT_PATH = {
    0:   (0.000000, 585000.000000, 0.000000, 0.000000),
    12:  (444655.755936, 501428.571429, 0.000000, 0.000000),
    60:  (2112717.620900, 167142.857143, 1945574.763757, 0.000000),
    84:  (2959163.646787, 0.000000, 2959163.646787, 0.000000),
    120: (4229470.390949, 0.000000, 4229470.390949, 0.000000),
    180: (6290272.153544, 0.000000, 6290272.153544, 0.000000),
    240: (8157073.574228, 0.000000, 8157073.574228, 4078536.787114),
    300: (7152135.393646, 0.000000, 7152135.393646, 3576067.696823),
    360: (5077515.345012, 0.000000, 5077515.345012, 2538757.672506),
    420: (1763350.342298, 0.000000, 1763350.342298, 881675.171149),
    446: (15717.315280, 0.000000, 15717.315280, 7858.657640),
    447: (0.000000, 0.000000, 0.000000, 0.000000),
    480: (0.000000, 0.000000, 0.000000, 0.000000),
    720: (0.000000, 0.000000, 0.000000, 0.000000),
}

# "In force by state": t -> (만나이, pols_if, healthy, minor, waived, diagnosed share %).
INFORCE_BY_STATE = {
    0:   (40, 1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000),
    12:  (41, 0.9529090613, 0.9519846704, 0.0001691728, 0.0007552182, 0.0970),
    60:  (45, 0.8431922656, 0.8375419523, 0.0012144885, 0.0044358248, 0.6701),
    120: (50, 0.7846501682, 0.7714827635, 0.0033084048, 0.0098589998, 1.6781),
    240: (60, 0.7204769811, 0.6811234744, 0.0127869424, 0.0265665643, 5.4621),
    360: (70, 0.5768966301, 0.4963813345, 0.0285510129, 0.0519642827, 13.9566),
    480: (80, 0.3697699075, 0.2690451225, 0.0354016049, 0.0653231801, 27.2399),
    600: (90, 0.1342357333, 0.0788584939, 0.0184172276, 0.0369600118, 41.2537),
    720: (100, 0.0103446076, 0.0048522513, 0.0016895927, 0.0038027636, 53.0939),
}

# "Policy-year summary": year -> (premiums, diagnosis, care, account, expenses,
# claim_expenses, commissions, net_cf).
POLICY_YEAR_SUMMARY = {
    1:  (528108.3335, 16156.8527, 3600.8595, 236.5689, 329347.1129, 270.2400,
         324000.0000, -145503.3006),
    2:  (504685.8326, 43865.2474, 14139.4730, 833.3878, 28635.6020, 394.1291,
         15140.5750, 401677.4184),
    3:  (486058.3546, 46250.3749, 17031.4817, 1532.3999, 28160.4757, 446.0625,
         14581.7506, 378055.8094),
    5:  (458838.1313, 52319.2751, 20775.9723, 3266.8413, 27720.2984, 537.3050,
         13765.1439, 340453.2955),
    10: (421209.1499, 75412.9020, 32167.3867, 10299.0744, 28295.7767, 811.6382,
         12636.2745, 261586.0973),
    20: (377292.4863, 150701.6939, 72574.8191, 48193.7008, 31647.9226, 1703.3232,
         11318.7746, 61152.2520),
    21: (0.0000, 160367.6591, 78181.0999, 75494.9085, 31870.6249, 1818.9219,
         0.0000, -347733.2144),
    30: (0.0000, 253861.6670, 128988.1784, 79819.9808, 31224.4443, 2975.4877,
         0.0000, -496869.7581),
    40: (0.0000, 220968.4916, 124332.8961, 0.0000, 24830.5872, 2884.0816,
         0.0000, -373016.0565),
    50: (0.0000, 85584.8773, 53091.1787, 0.0000, 11514.6009, 1297.6658,
         0.0000, -151488.3227),
    60: (0.0000, 6560.8739, 4570.4500, 0.0000, 1235.0473, 119.3753,
         0.0000, -12485.7465),
}

# "Policy year 1 in aggregate": the notes' twenty-line table, column -> total.
YEAR_ONE = {
    "pols_if": 11.7388451584,
    "pols_healthy": 11.7350500326,
    "pols_minor": 0.0006907114,
    "pols_waived": 0.0031044144,
    "premiums": 528108.3334792526,
    "claims_diag_gen": 12042.1768917546,
    "claims_diag_high": 440.5674472593,
    "claims_diag_minor": 1585.8856330344,
    "claims_diag_similar": 2088.2227399267,
    "claims_hosp": 474.3907255562,
    "claims_surgery": 1043.6595962237,
    "claims_treat": 2082.8092019227,
    "claims_death": 236.5689464717,
    "claims_lapse": 0.0000000000,
    "claims_maturity": 0.0000000000,
    "expenses": 329347.1128959327,
    "claim_expenses": 270.2399621534,
    "commissions": 323999.9999999999,
    "net_cf": -145503.3005609827,
}

# "Undiscounted totals over the whole 721-month projection".
TOTALS = {
    "pols_if": 366.4984840894,
    "pols_healthy": 331.1710420033,
    "pols_minor": 11.9942246536,
    "pols_waived": 23.3332174325,
    "premiums": 8586707.2756349239,
    "claims_diag_gen": 5914035.4962362796,
    "claims_diag_high": 185529.4660782705,
    "claims_diag_minor": 1673333.4821757083,
    "claims_diag_similar": 236970.6303129040,
    "claims_hosp": 824790.0641291471,
    "claims_surgery": 1408120.3468910458,
    "claims_treat": 1959782.9114945314,
    "claims_death": 1262932.8398376363,
    "claims_lapse": 211242.1285261842,
    "claims_maturity": 0.0000000000,
    "expenses": 1712032.6226109765,
    "claim_expenses": 98964.8080386155,
    "commissions": 565757.9682646699,
    "net_cf": -7466785.4889610466,
}

# "The other nine model points": id -> (sex, 만나이, pay_term_y, S, premium, proj_len,
# PV outgo / PV premiums, sum of net_cf).
MODEL_POINT_SUMMARY = {
    1:  ("M", 40, 20, 30000000.0, 45000.0, 721, 1.2352, -7466785.49),
    2:  ("F", 40, 20, 30000000.0, 54000.0, 721, 1.0202, -5576954.27),
    3:  ("M", 40, 0, 30000000.0, 62000.0, 721, 0.8769, -4619382.83),
    4:  ("F", 30, 20, 50000000.0, 65000.0, 841, 1.0271, -9387556.77),
    5:  ("M", 15, 20, 30000000.0, 39000.0, 1021, 1.0478, -11195873.06),
    6:  ("M", 65, 10, 50000000.0, 331000.0, 421, 0.9882, -5612192.29),
    7:  ("F", 55, 0, 30000000.0, 52000.0, 541, 0.9206, -2356283.74),
    8:  ("M", 45, 20, 30000000.0, 34000.0, 661, 1.0806, -3712985.12),
    9:  ("F", 50, 20, 100000000.0, 194000.0, 601, 0.9568, -10552299.99),
    10: ("M", 35, 30, 10000000.0, 23000.0, 781, 1.1010, -4471108.86),
}

# The male select excess hazards of survival_table.csv, both tiers, and the five-year sums
# they are calibrated to reproduce.
EXCESS_HAZARD_M = {
    "general": (0.14596111, 0.10425794, 0.07089540, 0.05421413, 0.04170317, 0.020),
    "minor": (0.04850043, 0.03464316, 0.02355735, 0.01801444, 0.01385726, 0.008),
}
FIVE_YEAR_SURVIVAL_M = {"general": 0.659, "minor": 0.8706}

# treat_avail(k), k = 1 .. 6, at the midpoint of each select year.
TREAT_AVAIL = (0.5488116361, 0.2725317930, 0.2369277587,
               0.2220172938, 0.2122479738, 0.2080451824)

# Expected payments per policy issued, each benefit line divided by its own amount.
EXPECTED_PAYMENTS = {
    "claims_diag_gen": (30000000.0, 0.1971),
    "claims_diag_high": (30000000.0, 0.0062),
    "claims_diag_minor": (18000000.0, 0.0930),
    "claims_diag_similar": (6000000.0, 0.0395),
    "claims_treat": (10000000.0, 0.1960),
}

# The ten check_* cells the model publishes, and the ranges of t their own definitions
# sweep.  check_cancer_roll_fwd reads pols_cancer(t + 1) and so stops one month short.
CHECKS = frozenset([
    "check_pols_roll_fwd", "check_cancer_roll_fwd", "check_canc_dur_ledger",
    "check_similar_ledger", "check_treat_ledger", "check_tier_shares",
    "check_waiting_period", "check_cv_floor", "check_net_cf", "check_hosp_cap",
])

CLAIM_KINDS = ("DIAG_GEN", "DIAG_HIGH", "DIAG_MINOR", "DIAG_SIMILAR", "HOSP",
               "SURGERY", "TREAT", "DEATH", "LAPSE", "MATURITY")


def _reread(suffix):
    """A private copy of the model, for tests that move a Reference."""
    return mx.read_model(MODEL_DIR, name="Cancer_KR_S_" + suffix)


def _claim_cols(df):
    """The ten claims_* split columns of a result_cf() frame, in table order."""
    return [c for c in df.columns if c.startswith("claims_")]


def _pv(df, rate=0.025):
    """(PV premiums, PV of all outgo) at the 예정이율, discounted from the start of month t.

    The notes' equivalence calculation: every line of result_cf() at ``1.025 ** (-t / 12)``.
    """
    factor = pd.Series([(1.0 + rate) ** (-t / 12.0) for t in df.index], index=df.index)
    outgo = df[_claim_cols(df) + ["expenses", "claim_expenses", "commissions"]].sum(axis=1)
    return float((df["premiums"] * factor).sum()), float((outgo * factor).sum())


# ---------------------------------------------------------------------------
# The worked example — the anchor cell's derived scalars and benefit ladder


def test_worked_example_anchor_cell_configuration(kr_cancer_anchor):
    """The anchor cell is the cell 감독규정 제1-2조제2호 itself computes at.

    The 기준연령 요건 is 「전기납 및 월납 조건으로 남자가 만 40세에」 [REG-R9], and the
    표준해약공제액 comparison, the [별표 15] 보험가입금액 computation and the 보장성/저축성
    test are all performed there.  Reading the configuration off the model rather than
    trusting the notes' prose is what keeps the regulatory reference point and the model
    point the same cell.
    """
    a = kr_cancer_anchor
    assert a.policy_id() == "KR-CA-0001"
    assert a.sex() == "M" and a.issue_age() == 40 and a.expiry_age() == 100
    assert a.chassis() == "bi_gaengsin" and a.pay_term() == 20
    assert a.sum_assured() == 30000000.0 and a.premium_mth_pp() == 45000.0
    assert a.wait_months() == 3 and a.reduction_months() == 12
    assert a.similar_ratio() == 0.20
    assert a.waiver_trigger() == "cancer_diag" and a.cv_form() == "mijigeup"
    assert (a.diag_module(), a.hosp_module(), a.surg_module(), a.treat_module()) == (
        1, 1, 1, 1)


def test_worked_example_derived_scalars(kr_cancer_anchor):
    """proj_len 721 on 721 rows, pay_months 240, 해약공제기간 84 and the 585,000 cap.

    ``surr_chg_cap_pp()`` is the one derived scalar with a whole regulatory chain behind it:
    [별표 14]'s formula gives 459,000 + 180,000 = 639,000 and the FSC's 13-months-of-premium
    ceiling then binds at 585,000 [REG-R20] [REG-R29].  A model that took the formula
    without the cap, or the cap without the formula, would be right here by accident.
    """
    a = kr_cancer_anchor
    assert a.proj_len() == 721 == 12 * (100 - 40) + 1
    assert len(a.result_cf()) == 721
    assert a.pay_months() == 240 and a.surr_chg_months() == 84
    assert a.pols_if_init() == 1.0
    ann_net = 12.0 * 45000.0 * (1.0 - 0.10 - 0.05)
    assert ann_net == 459000.0
    formula = ann_net * 0.05 * 20.0 + 30000000.0 * 0.60 * 0.01
    assert formula == pytest.approx(639000.0, abs=WON)
    assert a.surr_chg_cap_pp() == pytest.approx(585000.0, abs=WON)
    assert a.surr_chg_cap_pp() == 13.0 * a.premium_mth_pp()


def test_worked_example_benefit_ladder_and_the_two_start_dates(kr_cancer_anchor):
    """200 / 100 / 60 / 20 per cent of S, and 3 / 3 / 3 / **0** months of 면책기간.

    The ladder is read off the one retrieved 약관 stating every tier as an amount at
    보험가입금액 1,000만원 [S3 별표 1]; the 고액암 row is a **top-up**, so its 1.00 is added
    to the general tier's and a 고액암 draws 200% in total.  The zero in the fourth column is
    the product's second start date and the commonest thing to lose.
    """
    a = kr_cancer_anchor
    assert a.benefit_ratio("high") == 1.00
    assert a.benefit_ratio("general") == 1.00
    assert a.benefit_ratio("minor") == 0.60
    assert a.benefit_ratio("similar") == 0.20
    S = a.sum_assured()
    assert [a.benefit_ratio(j) * S for j in ("high", "general", "minor", "similar")] == [
        30000000.0, 30000000.0, 18000000.0, 6000000.0]
    assert a.tier_wait_months("high") == 3
    assert a.tier_wait_months("general") == 3
    assert a.tier_wait_months("minor") == 3
    assert a.tier_wait_months("similar") == 0
    assert a.cover(0) == a.cover(1) == a.cover(2) == 0.0
    assert a.cover(3) == 1.0
    assert all(a.cover_similar(t) == 1.0 for t in (0, 1, 2, 3))


def test_worked_example_event_module_amounts_scale_off_the_reference(cancer,
                                                                    kr_cancer_anchor):
    """₩50,000 a day to 180 days, ₩5,000,000 관혈, ₩1,000,000 비관혈, ₩10,000,000 treatment.

    Each is ``base × S / 30,000,000`` **[std]**, so the anchor cell prints the contractual
    amounts exactly and a model point at a different 보험가입금액 scales linearly.  Model
    point 9 at 1억원 is the check that the scaling is on and not a coincidence of the anchor.
    """
    a = kr_cancer_anchor
    assert a.hosp_daily() == 50000.0 and a.hosp_day_cap() == 180.0
    assert a.surg_open_amt() == 5000000.0 and a.surg_closed_amt() == 1000000.0
    assert a.treat_benefit() == 10000000.0
    p9 = cancer.Projection[9]
    assert p9.sum_assured() == 100000000.0
    assert p9.hosp_daily() == pytest.approx(50000.0 * 100.0 / 30.0, abs=WON)
    assert p9.treat_benefit() == pytest.approx(10000000.0 * 100.0 / 30.0, abs=WON)


# ---------------------------------------------------------------------------
# The worked example — the assumption basis


def test_worked_example_incidence_basis_is_sourced_not_standardized(kr_cancer_anchor):
    """inc_rate(0) = 0.001343 read verbatim [R5] [REG-R61]; 만나이 41 is log-linear [std].

    This is the one decrement basis in the model that is **published**: 보험개발원's
    「기타피부암 및 갑상선암 이외의 암 발생률」 for the 참조순보험요율 in force from
    2024-04-01.  Only the interpolation between the published ten-year points is a
    standardization, and ``inc_be_factor`` is at the identity because the loading inside a
    참조순보험요율 is [unverified].
    """
    a = kr_cancer_anchor
    assert a.inc_rate(0) == 0.001343
    assert a.inc_be_factor == 1.0
    expected = math.exp(math.log(0.001343)
                        + 0.1 * (math.log(0.003567) - math.log(0.001343)))
    assert a.inc_rate(12) == pytest.approx(expected, rel=1e-15)
    assert a.inc_rate(12) == pytest.approx(0.0014808079, abs=5e-11)
    assert a.inc_rate(240) == 0.008540 and a.inc_rate(480) == 0.027892


def test_worked_example_tier_shares_at_forty_and_forty_one(kr_cancer_anchor):
    """0.180 / 0.030 / 0.530 at 만나이 40, and 0.188 / 0.0295 / 0.511 at 41.

    The shares are the model's biggest [std] lever and the notes say so: the base rate is
    sourced and the split into four tiers is not.  Interpolation is **linear** in age off the
    20 / 40 / 60 / 80 anchors, and the age-41 row is the one-twentieth step toward the
    age-60 anchor written out.
    """
    a = kr_cancer_anchor
    assert (a.minor_share(0), a.high_share(0), a.similar_share(0)) == (0.18, 0.03, 0.53)
    assert a.minor_share(12) == pytest.approx(0.180 + (0.340 - 0.180) / 20.0, rel=1e-14)
    assert a.high_share(12) == pytest.approx(0.030 + (0.020 - 0.030) / 20.0, rel=1e-14)
    assert a.similar_share(12) == pytest.approx(0.530 + (0.150 - 0.530) / 20.0, rel=1e-14)
    assert (round(a.minor_share(12), 6), round(a.high_share(12), 6),
            round(a.similar_share(12), 6)) == (0.188, 0.0295, 0.511)


def test_worked_example_monthly_tier_incidences(kr_cancer_anchor):
    """i_g, i_m, i_h, i_z at 만나이 40 and 41, to the fourteen decimals the notes print."""
    a = kr_cancer_anchor
    assert a.inc_rate_gen_mth(0) == pytest.approx(0.00009177166667, abs=FLOW)
    assert a.inc_rate_minor_mth(0) == pytest.approx(0.00002014500000, abs=FLOW)
    assert a.inc_rate_high_mth(0) == pytest.approx(0.00000335750000, abs=FLOW)
    assert a.inc_rate_similar_mth(0) == pytest.approx(0.00005931583333, abs=FLOW)
    assert a.inc_rate_gen_mth(12) == pytest.approx(0.00010020133449, abs=FLOW)
    assert a.inc_rate_minor_mth(12) == pytest.approx(0.00002319932375, abs=FLOW)
    assert a.inc_rate_high_mth(12) == pytest.approx(0.00000364031942, abs=FLOW)
    assert a.inc_rate_similar_mth(12) == pytest.approx(0.00006305773636, abs=FLOW)


def test_worked_example_mortality_basis(kr_cancer_anchor):
    """q(40) = 0.0011068200 off the [std] Makeham, and its monthly form.

    ``mort_be_factor = 1.0`` and that is right rather than lazy: the shipped table is a
    **population all-cause** basis calibrated to the 국가데이터처 생명표's published 2024
    기대여명 [REG-R38], not a valuation table with a prudential margin, so there is no margin
    to unwind.  Scaling it would be inventing one.
    """
    a = kr_cancer_anchor
    assert a.mort_be_factor == 1.0
    assert a.mort_rate(0) == pytest.approx(0.0011068200, abs=5e-11)
    assert a.mort_rate_mth(0) == pytest.approx(0.000092281823, abs=RATE)
    assert a.mort_rate_mth(0) == pytest.approx(
        1.0 - (1.0 - a.mort_rate(0)) ** (1.0 / 12.0), rel=1e-15)


@pytest.mark.parametrize("tier", sorted(EXCESS_HAZARD_M))
def test_worked_example_excess_hazard_vector(kr_cancer_anchor, tier):
    """The five select hazards sum to −ln(the published five-year relative survival).

    The 일반암 row reproduces 남 **65.9%** excluding thyroid and the 특정소액암 row the
    [R1]-derived **87.06%**; the grading across the five years and the non-zero ultimate are
    [std].  The sum is the tell that relative survival was converted into a hazard rather
    than multiplied into survivorship: it is −ln(p), not p.
    """
    a = kr_cancer_anchor
    hazards = EXCESS_HAZARD_M[tier]
    for k, mu in enumerate(hazards, start=1):
        assert a.excess_hazard(tier, k) == pytest.approx(mu, abs=5e-9)
    total = sum(hazards[:5])
    assert total == pytest.approx(-math.log(FIVE_YEAR_SURVIVAL_M[tier]), abs=5e-8)
    assert math.exp(-total) == pytest.approx(FIVE_YEAR_SURVIVAL_M[tier], abs=5e-8)
    # Monotonically front-loaded, and the ultimate below the fifth select year.
    assert list(hazards[:5]) == sorted(hazards[:5], reverse=True)
    assert hazards[5] < hazards[4]


def test_worked_example_diagnosed_mortality_is_the_base_plus_the_hazard(kr_cancer_anchor):
    """q_w(t,1) = 0.01218091654617 and q_n(t,1) = 0.00412545541339 at 만나이 40.

    Two orders of magnitude above the 0.000092281823 healthy rate, which is what every
    post-diagnosis limb is integrated over, and the 특정소액암 rate a third of the 일반암
    one — a data fact from the three named sites' own published survivals, not a modelling
    choice [R1].
    """
    a = kr_cancer_anchor
    assert a.mort_rate_waived_mth(0, 1) == pytest.approx(0.01218091654617, abs=FLOW)
    assert a.mort_rate_minor_mth(0, 1) == pytest.approx(0.00412545541339, abs=FLOW)
    assert a.mort_rate_waived_mth(0, 1) == pytest.approx(
        1.0 - (1.0 - a.mort_rate_mth(0)) * math.exp(-0.14596111 / 12.0), abs=1e-15)
    assert a.mort_rate_waived_mth(0, 1) > 100 * a.mort_rate_mth(0)
    assert a.mort_rate_minor_mth(0, 1) < a.mort_rate_waived_mth(0, 1) / 2.0


def test_worked_example_lapse_basis_is_the_prescribed_shape(kr_cancer_anchor):
    """4.6% in year 1, log-linear to **0.1% at 완납**, stepping to a **0.8%** ultimate.

    The functional form is prescribed rather than fitted — the FSS's November 2024 계리가정
    ruling makes the 로그-선형 model converging to 0.1% at 완납 the 원칙모형 for 무.저해지
    business [REG-R27] — so only the starting level is standardized.  ``lapse_rate_canc_mth``
    is identically zero under the waiver.
    """
    a = kr_cancer_anchor
    assert a.lapse_rate(0) == 0.046
    assert a.lapse_rate_mth(0) == pytest.approx(0.003916610623, abs=RATE)
    assert a.lapse_rate(228) == pytest.approx(0.001, rel=1e-14)   # policy year 20 = 완납
    assert a.lapse_rate(240) == 0.008 and a.lapse_rate(719) == 0.008
    for y in range(1, 20):
        assert a.lapse_rate(12 * y) < a.lapse_rate(12 * (y - 1))
    assert a.lapse_rate(12) == pytest.approx(
        0.046 * (0.001 / 0.046) ** (1.0 / 19.0), rel=1e-14)
    assert all(a.lapse_rate_canc_mth(t) == 0.0 for t in (0, 12, 240, 600))


def test_worked_example_care_intensities_and_the_per_life_month_amounts(kr_cancer_anchor):
    """₩125,000.00, ₩275,000.00 and ₩548,811.64 per diagnosed life-month in select year 1.

    The three numbers worth memorising as an implementation check, and their ultimate
    counterparts ₩8,125.00 / ₩10,833.33 / **₩0.00** — the treatment limb is 최초 1회한 and
    its ultimate hazard is exactly zero, which is what makes the once-only bound hold at any
    horizon.
    """
    a = kr_cancer_anchor
    care = a.data.care_table()
    row1 = care.loc[1]
    assert (row1["hosp_adm_yr"], row1["hosp_days_adm"]) == (2.00, 15.0)
    assert (row1["surg_open_yr"], row1["surg_closed_yr"]) == (0.60, 0.30)
    assert row1["treat_hazard_yr"] == 1.20
    assert float(care.loc[6, "treat_hazard_yr"]) == 0.0
    hosp1 = a.hosp_daily() * (2.00 / 12.0) * 15.0
    surg1 = a.surg_open_amt() * 0.60 / 12.0 + a.surg_closed_amt() * 0.30 / 12.0
    treat1 = a.treat_benefit() * (1.20 / 12.0) * a.treat_avail(1)
    assert hosp1 == pytest.approx(125000.00, abs=WON)
    assert surg1 == pytest.approx(275000.00, abs=WON)
    assert treat1 == pytest.approx(548811.64, abs=WON)
    row6 = care.loc[6]
    hosp6 = a.hosp_daily() * (float(row6["hosp_adm_yr"]) / 12.0) * float(
        row6["hosp_days_adm"])
    surg6 = (a.surg_open_amt() * float(row6["surg_open_yr"])
             + a.surg_closed_amt() * float(row6["surg_closed_yr"])) / 12.0
    assert hosp6 == pytest.approx(8125.00, abs=WON)
    assert surg6 == pytest.approx(10833.33, abs=0.005)
    assert a.treat_benefit() * float(row6["treat_hazard_yr"]) / 12.0 == 0.0


def test_worked_example_treat_avail_is_read_at_the_midpoint(kr_cancer_anchor):
    """The six availabilities, starting at exp(−1.20 × 0.5) = 0.5488116361 and not at 1.0.

    ``treat_avail`` is a per-**diagnosed-life** quantity evaluated at the **midpoint** of
    select year k, so an entrant already carries half a year of exhaustion.  Reading it at
    the start of the year pays every entrant at full availability; reading it at the end
    understates.
    """
    a = kr_cancer_anchor
    for k, value in enumerate(TREAT_AVAIL, start=1):
        assert a.treat_avail(k) == pytest.approx(value, abs=5e-11)
    assert a.treat_avail(1) == pytest.approx(math.exp(-1.20 * 0.5), rel=1e-15)
    assert a.treat_avail(2) == pytest.approx(math.exp(-(1.20 + 0.20 * 0.5)), rel=1e-15)
    assert a.treat_avail(6) > 0.0                       # the ultimate hazard is zero


def test_the_std_scalar_assumptions_the_notes_state(cancer, kr_cancer_anchor):
    """Every [std] Reference the notes list, read off the model rather than restated.

    A silent change to any of them would move a printed result rather than fail a test,
    which is exactly the failure mode a golden-value module exists to prevent.  The five
    switches are asserted at their inert base values in the same breath, because the base
    run's reproducibility depends on them.
    """
    refs = cancer.Projection.refs
    assert refs["sa_ref"] == 30000000.0
    assert refs["hosp_daily_base"] == 50000.0 and refs["hosp_day_cap_days"] == 180
    assert refs["surg_open_base"] == 5000000.0 and refs["surg_closed_base"] == 1000000.0
    assert refs["treat_base"] == 10000000.0
    assert refs["prem_int_rate"] == 0.025
    assert refs["prem_load_acq"] == 0.10 and refs["prem_load_maint"] == 0.05
    assert refs["surr_chg_period_y"] == 7 and refs["surr_chg_coef"] == 20.0
    assert refs["surr_chg_cap_months"] == 13.0 and refs["notional_sa_ratio"] == 0.60
    assert refs["cv_floor_ratio"] == 0.0 and refs["cv_post_pay_ratio"] == 0.5
    assert refs["expense_acq"] == 300000.0 and refs["expense_maint"] == 2500.0
    assert refs["expense_claim_diag"] == 150000.0
    assert refs["expense_claim_hosp"] == 30000.0
    assert refs["inflation_rate"] == 0.02
    assert refs["comm_init_rate"] == 0.6 and refs["comm_renewal_rate"] == 0.03
    assert refs["comm_renewal_start"] == 12
    # The five inert switches.
    assert refs["void_adjust"] is False
    assert refs["inc_be_factor"] == 1.0 and refs["mort_be_factor"] == 1.0
    assert refs["lapse_canc_factor"] == 1.0
    assert refs["renew_reprice_rate"] == 0.0 and refs["renewal_months"] == 120
    a = kr_cancer_anchor
    assert a.prem_int_rate_used() == 0.025
    assert a.prem_alloc_pp(0) == pytest.approx(45000.0 * 0.85, abs=WON) == 38250.0
    assert a.void_prob() == 0.0 and a.pols_if_init() == 1.0


# ---------------------------------------------------------------------------
# The worked example — the first sixteen months, row by row


@pytest.mark.parametrize("t", sorted(WE_POLS))
def test_worked_example_inforce_row(kr_cancer_anchor, t):
    """The three states and their total, to the ten decimals the notes print.

    ``pols_if`` is a start-of-month count and is the sum of the three states exactly; the
    diagnosed states are empty through ``t = 3`` because the 면책기간 stops the transition
    and not merely the benefit.
    """
    pols_if, healthy, minor, waived = WE_POLS[t]
    a = kr_cancer_anchor
    assert a.pols_if(t) == pytest.approx(pols_if, abs=INFORCE)
    assert a.pols_healthy(t) == pytest.approx(healthy, abs=INFORCE)
    assert a.pols_minor(t) == pytest.approx(minor, abs=INFORCE)
    assert a.pols_waived(t) == pytest.approx(waived, abs=INFORCE)
    assert a.pols_if(t) == pytest.approx(
        a.pols_healthy(t) + a.pols_minor(t) + a.pols_waived(t), rel=1e-15)
    assert a.pols_cancer(t) == pytest.approx(a.pols_minor(t) + a.pols_waived(t),
                                             rel=1e-15)


@pytest.mark.parametrize("t", sorted(WE_DIAG))
def test_worked_example_premium_and_diagnosis_row(kr_cancer_anchor, t):
    """Premium and the four diagnosis lines, to the ten decimals the notes print.

    The first three rows carry a 유사암 benefit and nothing else, which is the whole of the
    two-start-date structure visible in the table itself.
    """
    prem, gen, high, minor, similar = WE_DIAG[t]
    a = kr_cancer_anchor
    assert a.premiums(t) == pytest.approx(prem, abs=MONEY)
    assert a.claims(t, "DIAG_GEN") == pytest.approx(gen, abs=MONEY)
    assert a.claims(t, "DIAG_HIGH") == pytest.approx(high, abs=MONEY)
    assert a.claims(t, "DIAG_MINOR") == pytest.approx(minor, abs=MONEY)
    assert a.claims(t, "DIAG_SIMILAR") == pytest.approx(similar, abs=MONEY)


@pytest.mark.parametrize("t", sorted(WE_CARE))
def test_worked_example_care_and_account_row(kr_cancer_anchor, t):
    """The three care limbs and the two account payments, to ten decimals.

    ``claims_lapse`` is zero in all sixteen rows because the 미지급형 form pays nothing on a
    surrender for the whole 납입기간, and ``claims_maturity`` is zero in every row of the
    projection because nothing is paid at the 100세 계약해당일.
    """
    hosp, surgery, treat, death, lapse = WE_CARE[t]
    a = kr_cancer_anchor
    assert a.claims(t, "HOSP") == pytest.approx(hosp, abs=MONEY)
    assert a.claims(t, "SURGERY") == pytest.approx(surgery, abs=MONEY)
    assert a.claims(t, "TREAT") == pytest.approx(treat, abs=MONEY)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=MONEY)
    assert a.claims(t, "LAPSE") == lapse == 0.0
    assert a.claims(t, "MATURITY") == 0.0


@pytest.mark.parametrize("t", sorted(WE_TAIL))
def test_worked_example_expense_commission_and_net_cf_row(kr_cancer_anchor, t):
    """Expense, claim handling, commission and net cash flow, to ten decimals.

    ``net_cf`` is rebuilt here from the model's own claim total as well as compared with the
    printed figure, so a benefit line that exists in ``claims()`` and is missing from the
    printed row cannot pass both halves.
    """
    expenses, claim_exp, comm, net = WE_TAIL[t]
    a = kr_cancer_anchor
    assert a.expenses(t) == pytest.approx(expenses, abs=MONEY)
    assert a.claim_expenses(t) == pytest.approx(claim_exp, abs=MONEY)
    assert a.commissions(t) == pytest.approx(comm, abs=MONEY)
    assert a.net_cf(t) == pytest.approx(net, abs=MONEY)
    assert a.net_cf(t) == pytest.approx(
        a.premiums(t) - a.claims(t) - a.expenses(t) - a.claim_expenses(t)
        - a.commissions(t), abs=1e-9)


def test_worked_example_the_four_features_of_the_first_sixteen_rows(kr_cancer_anchor):
    """The notes' four numbered features, each of which is the product rather than a detail.

    (1) ``t = 0, 1, 2`` pay a 유사암 benefit and nothing else; (2) ``t = 3`` starts all three
    invasive lines from an empty diagnosed population; (3) ``t = 4`` is the first month with
    any care benefit and ``claims_death`` starts a month earlier still because ``av_pp(0)``
    is nil; (4) ``t = 12`` ends the 감액기간 and starts the renewal commission, every
    diagnosis line stepping by rather more than 2.0.
    """
    a = kr_cancer_anchor
    for t in (0, 1, 2):
        assert a.claims(t, "DIAG_SIMILAR") > 0.0
        assert a.claims(t) == pytest.approx(a.claims(t, "DIAG_SIMILAR")
                                            + a.claims(t, "DEATH"), abs=1e-9)
    assert a.pols_minor(3) == 0.0 and a.pols_waived(3) == 0.0
    assert a.claims(3, "HOSP") == a.claims(3, "SURGERY") == a.claims(3, "TREAT") == 0.0
    assert a.claims(3, "DIAG_GEN") > 0.0
    assert a.claims(4, "HOSP") > 0.0
    assert a.claims(0, "DEATH") == 0.0 and a.claims(1, "DEATH") > 0.0
    ratios = {kind: a.claims(12, kind) / a.claims(11, kind)
              for kind in ("DIAG_GEN", "DIAG_HIGH", "DIAG_MINOR", "DIAG_SIMILAR")}
    assert round(ratios["DIAG_GEN"], 4) == 2.1748
    assert round(ratios["DIAG_HIGH"], 4) == 2.1596
    assert round(ratios["DIAG_MINOR"], 4) == 2.2937
    assert round(ratios["DIAG_SIMILAR"], 4) == 2.1175
    assert a.commissions(11) == 0.0 and a.commissions(12) > 0.0


# ---------------------------------------------------------------------------
# The worked example — the hand traces


def test_worked_example_month_zero_trace(kr_cancer_anchor):
    """The acquisition month, with the 유사암 tier alone in force.

    ₩624,000 of acquisition expense and initial commission against ₩45,000 of premium —
    13.9 months' worth — and ₩177.95 of benefit.  The decrements and the account's first
    step are traced with it, because the month is where every front-end mechanic of the
    product lands at once.
    """
    a = kr_cancer_anchor
    assert a.pols_healthy(0) == 1.0 and a.pols_minor(0) == a.pols_waived(0) == 0.0
    assert a.similar_avail(0) == 1.0 and a.reduction_factor(0) == 0.50
    assert a.cover(0) == 0.0 and a.cover_similar(0) == 1.0
    assert a.premiums(0) == 45000.0
    assert a.diag_gen(0) == a.diag_high(0) == a.diag_minor(0) == 0.0
    assert a.diag_similar(0) == pytest.approx(0.00005931583333, abs=FLOW)
    assert a.claims(0, "DIAG_SIMILAR") == pytest.approx(
        0.20 * 30000000.0 * 0.50 * a.diag_similar(0), rel=1e-15)
    assert a.claims(0, "DIAG_SIMILAR") == pytest.approx(177.9475000000, abs=MONEY)
    assert a.claims(0, "DEATH") == a.claims(0, "LAPSE") == 0.0
    assert a.expenses(0) == pytest.approx(2500.0 * 1.0 + 300000.0, abs=1e-9)
    assert a.claim_expenses(0) == pytest.approx(150000.0 * a.diag_similar(0), rel=1e-14)
    assert a.pols_death(0) == pytest.approx(0.00009228182324, abs=FLOW)
    assert a.pols_lapse(0) == pytest.approx(0.00391624919073, abs=FLOW)
    assert a.surv_healthy(0) == pytest.approx(0.99599146898603, abs=FLOW)
    assert a.pols_healthy(1) == pytest.approx(0.9959914690, abs=INFORCE)
    assert a.similar_avail(1) == pytest.approx(0.999940684167, abs=1e-12)
    assert a.av_pp(1) == pytest.approx(
        (38250.0 - 177.9475) * 1.025 ** (1.0 / 12.0), abs=SIX)
    assert a.av_pp(1) == pytest.approx(38150.474695, abs=SIX)
    assert a.expense_acq + a.commissions(0) == pytest.approx(624000.0, abs=WON)
    assert (a.expense_acq + a.commissions(0)) / a.premium_mth_pp() == pytest.approx(
        13.9, abs=0.05)


def test_worked_example_month_three_trace(kr_cancer_anchor):
    """암보장개시일, from an empty diagnosed state, written out flow by flow.

    Two things to notice, and both are asserted: ``claims_surgery(3)`` is **exactly zero**,
    because the surgery limb rides on the diagnosed **stock** and the stock is still empty;
    and ``n_h`` does **not** reduce ``n_g`` — ₩1,360.11 and ₩49.76 are both paid on
    overlapping flows, which is what "pays in addition" means.
    """
    a = kr_cancer_anchor
    assert a.similar_avail(3) == pytest.approx(0.999822063055, abs=1e-12)
    assert a.diag_gen_h(3) == pytest.approx(0.00009067247589, abs=FLOW)
    assert a.diag_gen_m(3) == pytest.approx(0.00000000182660, abs=FLOW)
    assert a.diag_gen(3) == pytest.approx(0.00009067430249, abs=FLOW)
    assert a.diag_minor(3) == pytest.approx(0.00001990371422, abs=FLOW)
    assert a.diag_high(3) == pytest.approx(0.00000331735253, abs=FLOW)
    assert a.diag_similar(3) == pytest.approx(0.00005859495270, abs=FLOW)
    assert a.diag_first(3) == pytest.approx(a.diag_gen_h(3) + a.diag_minor(3), rel=1e-15)
    assert a.diag_gen_m(3) == pytest.approx(
        (a.pols_minor(3) + a.diag_minor(3)) * a.inc_rate_gen_mth(3), rel=1e-14)
    assert a.claims(3, "SURGERY") == 0.0
    assert a.claims(3, "DIAG_GEN") == pytest.approx(1360.1145372945, abs=MONEY)
    assert a.claims(3, "DIAG_HIGH") == pytest.approx(49.7602879498, abs=MONEY)
    assert a.claims(3, "DEATH") == pytest.approx(a.av_pp(3) * a.pols_death(3), rel=1e-15)
    assert a.av_pp(3) == pytest.approx(114687.368900, abs=SIX)
    assert a.pols_death(3) == pytest.approx(0.00009235291837, abs=FLOW)
    assert a.claim_expenses(3) == pytest.approx(
        150000.0 * (a.diag_gen(3) + a.diag_minor(3) + a.diag_similar(3)), rel=1e-14)
    # The cohorts entered in month 3 are carried into month 4 on their own survival.
    assert a.surv_waived(3, 1) == pytest.approx(0.98781908345383, abs=FLOW)
    assert a.surv_minor(3, 1) == pytest.approx(0.99188305665071, abs=FLOW)
    assert a.pols_waived_dur(4, 1) == pytest.approx(0.00008956980637, abs=FLOW)
    assert a.pols_minor_dur(4, 1) == pytest.approx(0.00001974215690, abs=FLOW)


def test_worked_example_month_four_trace(kr_cancer_anchor):
    """The diagnosed state is live, the care limbs start, and the premium weight bites.

    ``premiums(4)`` is 45,000 × **0.9839716377**, not 45,000 × ``pols_if(4)`` = 0.9840612075
    — a difference of ₩4.03 in this row and of the whole premium stream by 납입완료 — while
    ``expenses(4)`` is 2,500 × ``pols_if(4)``, because a waived policy is still administered.
    Two weights, two lines, one row.
    """
    a = kr_cancer_anchor
    assert a.pols_diag_dur(4, 1) == pytest.approx(0.00010931196327, abs=FLOW)
    assert all(a.pols_waived_dur(4, k) == 0.0 for k in range(2, 7))
    assert all(a.pols_minor_dur(4, k) == 0.0 for k in range(2, 7))
    assert a.pols_payer(4) == pytest.approx(0.9839716377, abs=INFORCE)
    assert a.pols_if(4) == pytest.approx(0.9840612075, abs=INFORCE)
    assert a.premiums(4) == pytest.approx(45000.0 * a.pols_payer(4), rel=1e-15)
    assert 45000.0 * (a.pols_if(4) - a.pols_payer(4)) == pytest.approx(4.03, abs=0.005)
    assert a.expenses(4) == pytest.approx(2500.0 * a.pols_if(4), rel=1e-14)
    assert a.claims(4, "HOSP") == pytest.approx(
        50000.0 * (2.00 / 12.0) * 15.0 * a.pols_diag_dur(4, 1), rel=1e-14)
    assert a.claims(4, "SURGERY") == pytest.approx(
        275000.0 * a.pols_diag_dur(4, 1), rel=1e-14)
    assert a.claims(4, "TREAT") == pytest.approx(
        10000000.0 * (1.20 / 12.0) * a.treat_avail(1) * a.pols_diag_dur(4, 1), rel=1e-14)
    assert a.claim_expenses(4) == pytest.approx(
        150000.0 * (a.diag_gen(4) + a.diag_minor(4) + a.diag_similar(4))
        + 30000.0 * (2.00 / 12.0) * a.pols_diag_dur(4, 1), rel=1e-13)
    assert a.claims(4, "DEATH") == pytest.approx(14.1079661237, abs=MONEY)


def test_worked_example_month_twelve_trace(kr_cancer_anchor):
    """The 감액기간 ends, the age steps and the renewal commission starts, in one row.

    The 일반암 line goes ×2.1748 across the boundary and the model publishes both factors
    separately: 2.0 of it is ``reduction_factor`` stepping to 1.00, and the residual 1.0874
    is the incidence step against the general share falling and the in-force falling.  All
    six cohort counts are still concentrated in ``k = 1``: the first graduation cannot occur
    before ``t = 16``, thirteen months after the first diagnosis at ``t = 3``.
    """
    a = kr_cancer_anchor
    assert a.age(12) == 41 and a.policy_year(12) == 2
    assert a.reduction_factor(11) == 0.50 and a.reduction_factor(12) == 1.00
    assert a.diag_gen_h(12) == pytest.approx(0.00009539013438, abs=FLOW)
    assert a.diag_gen_m(12) == pytest.approx(0.00000001916432, abs=FLOW)
    assert a.diag_gen(12) == pytest.approx(0.00009540929871, abs=FLOW)
    assert a.claims(12, "DIAG_GEN") == pytest.approx(2862.2789611635, abs=MONEY)
    assert a.pols_waived_dur(12, 1) == pytest.approx(0.00075521819673, abs=FLOW)
    assert a.pols_minor_dur(12, 1) == pytest.approx(0.00016917276671, abs=FLOW)
    assert a.pols_diag_dur(12, 1) == pytest.approx(0.00092439096344, abs=FLOW)
    assert all(a.pols_diag_dur(12, k) == 0.0 for k in range(2, 7))
    assert all(a.waived_grad(t, 1) == 0.0 for t in range(0, 16))
    assert a.waived_grad(16, 1) > 0.0
    assert a.expenses(12) == pytest.approx(2500.0 * 1.02 * a.pols_if(12), rel=1e-14)
    assert a.commissions(12) == pytest.approx(0.03 * a.premiums(12), rel=1e-15)
    assert a.commissions(12) == pytest.approx(1285.4076882259, abs=MONEY)


def test_worked_example_month_240_trace(kr_cancer_anchor):
    """납입완료 — the only row with two prescribed steps in it.

    The premium stops because ``t = pay_months()``; the lapse rate steps from 0.1% to 0.8%
    because the [REG-R27] 로그-선형 model converges to 0.1% at 완납; and the surrender value
    steps from nil to 50% of the 표준형 value.  The treatment limb is worth reading term by
    term: the ultimate cohort holds more than half the diagnosed population and contributes
    **nothing at all**, because its hazard is zero and the benefit is 최초 1회한.
    """
    a = kr_cancer_anchor
    assert a.pols_healthy(240) == pytest.approx(0.6811234744, abs=INFORCE)
    assert a.pols_minor(240) == pytest.approx(0.0127869424, abs=INFORCE)
    assert a.pols_waived(240) == pytest.approx(0.0265665643, abs=INFORCE)
    assert a.age(240) == 60 and a.inc_rate(240) == 0.008540
    assert a.prem_payable(240) == 0.0 and a.premiums(240) == 0.0
    assert a.commissions(240) == 0.0
    assert a.inc_rate_gen_mth(240) == pytest.approx(0.008540 * 0.66 / 12.0, rel=1e-14)
    assert a.inc_rate_minor_mth(240) == pytest.approx(0.008540 * 0.34 / 12.0, rel=1e-14)
    assert a.diag_gen_h(240) == pytest.approx(0.00031992369591, abs=FLOW)
    assert a.diag_minor(240) == pytest.approx(0.00016480917668, abs=FLOW)
    assert a.diag_gen_m(240) == pytest.approx(0.00000608343772, abs=FLOW)
    assert a.diag_gen(240) == pytest.approx(0.00032600713363, abs=FLOW)
    assert a.claims(240, "DIAG_GEN") == pytest.approx(9780.2140089950, abs=MONEY)
    assert a.claims(240, "DIAG_MINOR") == pytest.approx(2966.5651802476, abs=MONEY)
    assert a.claims(240, "HOSP") == pytest.approx(1159.0123272870, abs=MONEY)
    assert a.claims(240, "TREAT") == pytest.approx(3095.8887072601, abs=MONEY)
    assert a.claims(240, "DEATH") == pytest.approx(
        a.av_pp(240) * a.pols_death(240), rel=1e-15)
    assert a.claims(240, "LAPSE") == pytest.approx(
        a.cv_pp(240) * a.pols_lapse(240), rel=1e-15)
    assert a.claims(240, "LAPSE") == pytest.approx(1891.7076416342, abs=MONEY)
    assert a.expenses(240) == pytest.approx(
        2500.0 * 1.02 ** 20 * a.pols_if(240), rel=1e-13)
    assert a.claims(240) == pytest.approx(26130.8679545, abs=1e-6)
    assert a.net_cf(240) == pytest.approx(-28957.2675176, abs=1e-6)
    # The ultimate cohort is more than half the diagnosed population and pays no treatment.
    diagnosed = sum(a.pols_diag_dur(240, k) for k in range(1, 7))
    assert a.pols_diag_dur(240, 6) == pytest.approx(0.0203245508, abs=5e-11)
    assert a.pols_diag_dur(240, 6) > 0.5 * diagnosed


# ---------------------------------------------------------------------------
# The worked example — aggregates


@pytest.mark.parametrize("column", sorted(YEAR_ONE))
def test_worked_example_policy_year_one_aggregate(kr_cancer_anchor, column):
    """Policy year 1 line by line, ``t = 0 … 11``, from unrounded monthly values.

    Twelve months at 만나이 40, all inside the 감액기간, the last nine inside cover: the
    strongest single test target in the notes, because it exercises both waiting-period
    boundaries and the first nine months of the diagnosed state on one set of rates.
    """
    df = kr_cancer_anchor.result_cf().loc[0:11]
    assert df[column].sum() == pytest.approx(YEAR_ONE[column], abs=MONEY)


def test_worked_example_policy_year_one_shape(kr_cancer_anchor):
    """Benefit outgo of ₩19,994.28 against ₩528,108.33 of premium — **3.79%**.

    That low figure is the product and not an error: the first quarter pays nothing for an
    invasive cancer, the diagnosed stock the care limbs ride on is still 0.0970% of the
    in-force after twelve months, and the 감액기간 halves every diagnosis benefit for the
    whole year.  Against it, ₩624,000 of acquisition cost lands in ``t = 0``.
    """
    df = kr_cancer_anchor.result_cf().loc[0:11]
    benefit = df[_claim_cols(df)].sum().sum()
    assert benefit == pytest.approx(19994.28, abs=WON)
    assert benefit / df["premiums"].sum() == pytest.approx(0.0379, abs=5e-5)
    care = df[["claims_hosp", "claims_surgery", "claims_treat"]].sum().sum()
    assert care == pytest.approx(3600.86, abs=WON)
    assert df["net_cf"].sum() == pytest.approx(-145503.30, abs=WON)


@pytest.mark.parametrize("t", sorted(BOUNDARY_ROWS))
def test_where_the_product_does_something_else_row(kr_cancer_anchor, t):
    """The notes' fifteen boundary rows, every column, to the six decimals they print.

    Four boundaries in the order the product reaches them: the 감액기간 ending at 12, the
    120-month mark, 납입완료 at 240, the account's exhaustion at 447 and expiry at 720.  The
    rows are the product's whole shape in fifteen lines.
    """
    row = kr_cancer_anchor.result_cf().loc[t]
    for name, expected in zip(BOUNDARY_COLUMNS, BOUNDARY_ROWS[t]):
        assert row[name] == pytest.approx(expected, abs=SIX), f"t={t}, {name}"


def test_the_four_boundaries_the_notes_read_off_those_rows(kr_cancer_anchor):
    """Each boundary asserted as a *difference*, which is what makes it a boundary.

    The 감액기간 ending costs ₩3,617.18 of ``net_cf`` although the premium barely moves;
    납입완료 swings ``net_cf`` by ₩33,646.91 and turns it negative for all 480 remaining
    months; the account's exhaustion at ``t = 447`` takes ``claims_death`` and
    ``claims_lapse`` to exactly zero and keeps them there; and expiry pays nothing at all.
    """
    a = kr_cancer_anchor
    df = a.result_cf()
    assert df.loc[11, "net_cf"] - df.loc[12, "net_cf"] == pytest.approx(3617.18, abs=WON)
    assert df.loc[240, "net_cf"] - df.loc[239, "net_cf"] == pytest.approx(
        -33646.91, abs=WON)
    assert (df.loc[240:719, "net_cf"] < 0.0).all() and len(df.loc[240:719]) == 480
    assert df.loc[720, "net_cf"] == 0.0
    assert a.av_pp(446) > 0.0 and a.av_pp(447) == 0.0
    assert (df.loc[447:720, "claims_death"] == 0.0).all()
    assert (df.loc[447:720, "claims_lapse"] == 0.0).all()
    assert a.age(447) == 77
    assert (df.loc[720] == 0.0)[[c for c in df.columns if c != "pols_if"
                                 and not c.startswith("pols_")]].all()
    assert a.pols_maturity(720) == pytest.approx(0.0103446076, abs=INFORCE)
    assert a.claims(720, "MATURITY") == 0.0


@pytest.mark.parametrize("t", sorted(ACCOUNT_PATH))
def test_the_account_and_surrender_value_path(kr_cancer_anchor, t):
    """av_pp, surr_chg_pp, cv_std_pp and cv_pp at the notes' fourteen durations.

    Four facts live in this table and each is asserted elsewhere as well: ``cv_pp`` is
    exactly nil for the whole 납입기간 and steps at ``t = 240``; the 해약공제액 runs off to
    zero at ``t = 84``, thirteen years earlier; the 표준형 value becomes positive between 60
    and 84 while ``cv_pp`` stays nil; and the account peaks at 납입완료 and is exhausted at
    ``t = 447``.
    """
    av, charge, cv_std, cv = ACCOUNT_PATH[t]
    a = kr_cancer_anchor
    assert a.av_pp(t) == pytest.approx(av, abs=SIX)
    assert a.surr_chg_pp(t) == pytest.approx(charge, abs=SIX)
    assert a.cv_std_pp(t) == pytest.approx(cv_std, abs=SIX)
    assert a.cv_pp(t) == pytest.approx(cv, abs=SIX)


@pytest.mark.parametrize("t", sorted(INFORCE_BY_STATE))
def test_in_force_by_state_across_the_projection(kr_cancer_anchor, t):
    """The three states at ten-year intervals, and the diagnosed share they imply.

    The whole cost of this product is in the second half of the projection: the diagnosed
    population is 0.10% of the in-force after twelve months, 5.46% at 납입완료, 27.24% at
    만나이 80 and 41.25% at 90.  A ten-year projection sees almost none of the liability.
    """
    age, pols_if, healthy, minor, waived, share = INFORCE_BY_STATE[t]
    a = kr_cancer_anchor
    assert a.age(t) == age
    assert a.pols_if(t) == pytest.approx(pols_if, abs=INFORCE)
    assert a.pols_healthy(t) == pytest.approx(healthy, abs=INFORCE)
    assert a.pols_minor(t) == pytest.approx(minor, abs=INFORCE)
    assert a.pols_waived(t) == pytest.approx(waived, abs=INFORCE)
    assert 100.0 * a.pols_cancer(t) / a.pols_if(t) == pytest.approx(share, abs=5e-5)


@pytest.mark.parametrize("year", sorted(POLICY_YEAR_SUMMARY))
def test_the_policy_year_summary(kr_cancer_anchor, year):
    """The notes' eleven policy years, grouped as diagnosis / care / account.

    Year 1 is the only negative year before 납입완료 and year 21 the first negative one
    after it; the swing across that boundary is ₩408,885.47 and the projection is negative
    for the whole of its second half.  The account column goes to zero from policy year 39
    because ``av_pp`` and ``cv_pp`` are both exhausted.
    """
    prem, diagnosis, care, account, expenses, claim_exp, comm, net = POLICY_YEAR_SUMMARY[
        year]
    df = kr_cancer_anchor.result_cf().loc[12 * (year - 1):12 * (year - 1) + 11]
    assert df["premiums"].sum() == pytest.approx(prem, abs=1e-4)
    assert df[["claims_diag_gen", "claims_diag_high", "claims_diag_minor",
               "claims_diag_similar"]].sum().sum() == pytest.approx(diagnosis, abs=1e-4)
    assert df[["claims_hosp", "claims_surgery",
               "claims_treat"]].sum().sum() == pytest.approx(care, abs=1e-4)
    assert df[["claims_death", "claims_lapse",
               "claims_maturity"]].sum().sum() == pytest.approx(account, abs=1e-4)
    assert df["expenses"].sum() == pytest.approx(expenses, abs=1e-4)
    assert df["claim_expenses"].sum() == pytest.approx(claim_exp, abs=1e-4)
    assert df["commissions"].sum() == pytest.approx(comm, abs=1e-4)
    assert df["net_cf"].sum() == pytest.approx(net, abs=1e-4)


def test_the_swing_across_the_payment_boundary(kr_cancer_anchor):
    """Policy year 20 closes at +₩61,152 and year 21 at −₩347,733: a swing of ₩408,885.47.

    The premium stops and the same block goes on claiming for forty more years.  That is the
    single sentence the product's shape reduces to, and it is asserted rather than described.
    """
    df = kr_cancer_anchor.result_cf()
    year20 = df.loc[228:239, "net_cf"].sum()
    year21 = df.loc[240:251, "net_cf"].sum()
    assert year20 > 0.0 > year21
    assert year20 - year21 == pytest.approx(408885.47, abs=WON)


@pytest.mark.parametrize("column", sorted(TOTALS))
def test_the_undiscounted_totals_over_721_months(kr_cancer_anchor, column):
    """Every column of the notes' totals table, summed over the whole projection."""
    df = kr_cancer_anchor.result_cf()
    assert len(df) == 721
    assert df[column].sum() == pytest.approx(TOTALS[column], abs=5e-8)


def test_the_total_groupings_the_notes_carry(kr_cancer_anchor):
    """Diagnosis 8,009,869.07, care 4,192,693.32, account 1,474,174.97, outgo 16,053,492.76.

    Read together they are the answer to what a Korean cancer contract costs: the care limbs
    are 30.7% of benefit on a table (``care_table.csv``) whose every row is [std], which is
    the notes' third-ranked model risk stated as an amount.
    """
    df = kr_cancer_anchor.result_cf()
    diagnosis = df[["claims_diag_gen", "claims_diag_high", "claims_diag_minor",
                    "claims_diag_similar"]].sum().sum()
    care = df[["claims_hosp", "claims_surgery", "claims_treat"]].sum().sum()
    account = df[["claims_death", "claims_lapse", "claims_maturity"]].sum().sum()
    benefit = df[_claim_cols(df)].sum().sum()
    assert diagnosis == pytest.approx(8009869.07, abs=WON)
    assert care == pytest.approx(4192693.32, abs=WON)
    assert account == pytest.approx(1474174.97, abs=WON)
    assert benefit == pytest.approx(13676737.37, abs=WON)
    assert diagnosis + care + account == pytest.approx(benefit, abs=1e-6)
    assert df["expenses"].sum() + df["claim_expenses"].sum() == pytest.approx(
        1810997.43, abs=WON)
    outgo = benefit + df["expenses"].sum() + df["claim_expenses"].sum() + df[
        "commissions"].sum()
    assert outgo == pytest.approx(16053492.76, abs=WON)
    assert care / benefit == pytest.approx(0.307, abs=5e-4)


@pytest.mark.parametrize("column", sorted(EXPECTED_PAYMENTS))
def test_the_expected_payment_counts_each_benefit_line_implies(kr_cancer_anchor, column):
    """Each line divided by its own amount: 0.1971 / 0.0062 / 0.0930 / 0.0395 / 0.1960.

    A once-only fixed-benefit product is the one shape where this division is meaningful,
    and the counts are the epidemiological sanity check on the whole model: against a
    lifetime cancer risk of 44.6% for Korean men, with lapse and mortality removing
    two-thirds of the block from 만나이 40, 0.1971 일반암 plus 0.0930 특정소액암 payments is
    the order the registry implies.
    """
    amount, expected = EXPECTED_PAYMENTS[column]
    df = kr_cancer_anchor.result_cf()
    assert df[column].sum() / amount == pytest.approx(expected, abs=5e-5)


def test_the_equivalence_premium_on_the_shipped_basis(kr_cancer_anchor):
    """The PV ratio at ₩45,000, and the ₩55,586 lower bound it scales to.

    ``product-spec.md`` states that ₩45,000 is a modelling input and that the notes' figure
    governs, so the equivalence calculation is part of the worked example rather than a
    commentary on it.  **The ratio-scaled ₩55,586 is a lower bound and not the equivalence
    premium**: ``claims_death`` and ``claims_lapse`` are the 계약자적립액 and the
    해약환급금 multiplied by decrements, so they rise with the premium, and ``commissions``
    is proportional to it.  The notes solve the equivalence level at **₩66,289**, which is
    what ₩45,000 is 32.1% below; the numbers asserted here are the PV pair the solve starts
    from.  The gap is not hidden anywhere: it is why ``av_pp`` is exhausted at ``t = 447``
    and why the undiscounted ``net_cf`` total is −₩7,466,785.49.
    """
    a = kr_cancer_anchor
    df = a.result_cf()
    pv_prem, pv_outgo = _pv(df)
    assert pv_prem == pytest.approx(6873383.677006, abs=1e-4)
    assert pv_outgo == pytest.approx(8490332.868460, abs=1e-4)
    ratio = pv_outgo / pv_prem
    assert ratio == pytest.approx(1.2352479168, abs=5e-10)
    assert pv_prem - pv_outgo == pytest.approx(-1616949.191455, abs=1e-4)
    assert pv_prem / a.premium_mth_pp() == pytest.approx(152.7418594890, abs=5e-9)
    assert 45000.0 * ratio == pytest.approx(55586.16, abs=WON)
    # The lower bound understates because two outgo lines ride on the account: they are
    # ₩1,474,174.97 of the ₩16,053,492.76 of undiscounted outgo, and they scale with P.
    account_lines = df["claims_death"].sum() + df["claims_lapse"].sum()
    assert account_lines == pytest.approx(1474174.9683638205, abs=WON)
    assert 45000.0 / 66289.05 - 1.0 == pytest.approx(-0.321, abs=5e-4)


@pytest.mark.parametrize("point_id", sorted(MODEL_POINT_SUMMARY))
def test_the_shipped_model_point_summary_table(cancer, point_id):
    """The notes' ten-row table: configuration, horizon, PV ratio and total net cash flow.

    Each point carries its own approximate equivalence premium, which is why point 1 is the
    only cell whose account is exhausted anywhere near the middle of its term.  Point 3's
    ratio of 0.8769 is the clearest statement of what the 갱신형 flag does: removing the
    면책기간 and the 감액기간 raises the benefit, and paying premium for the whole term
    instead of twenty years raises the premium PV far more.
    """
    sex, age, pay_term, sa, premium, proj_len, ratio, net = MODEL_POINT_SUMMARY[point_id]
    p = cancer.Projection[point_id]
    assert (p.sex(), p.issue_age(), p.pay_term()) == (sex, age, pay_term)
    assert (p.sum_assured(), p.premium_mth_pp()) == (sa, premium)
    assert p.proj_len() == proj_len == 12 * (100 - age) + 1
    df = p.result_cf()
    pv_prem, pv_outgo = _pv(df)
    assert pv_outgo / pv_prem == pytest.approx(ratio, abs=5e-5)
    assert df["net_cf"].sum() == pytest.approx(net, abs=WON)


# ---------------------------------------------------------------------------
# The check_* cells, the roll-forward identities and the processing order


def test_which_checks_this_model_publishes(cancer, kr_cancer_anchor):
    """The ten check cells, asserted **by name**, each with its own per-t residual.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared: it
    would call the nine that remain, pass, and prove less than it did before.  Naming the
    set turns "every check passes" into a statement about *which* checks — and on this
    product the set is the specification: three roll-forwards, two once-only ledgers, the
    tier algebra, the waiting period, the surrender-value bounds, the published statement
    and the inpatient cap.
    """
    published = {n for n in cancer.Projection.cells
                 if n.startswith("check_") and not n.endswith("_resid")}
    assert published == CHECKS
    resid = {n[:-len("_resid")] for n in cancer.Projection.cells
             if n.startswith("check_") and n.endswith("_resid")}
    assert resid == CHECKS
    a = kr_cancer_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True and isinstance(value, bool), name


def test_every_check_residual_is_zero_on_the_anchor_cell(kr_cancer_anchor):
    """The signed residuals themselves, month by month, not merely the booleans.

    ``check_cancer_roll_fwd_resid`` reads ``pols_cancer(t + 1)`` and so is only defined to
    ``proj_len() - 2``; its own ``check`` sweeps exactly that range and the test follows it,
    because a residual asserted outside the range a check covers proves nothing about the
    check.
    """
    a = kr_cancer_anchor
    n = a.proj_len()
    for name in sorted(CHECKS):
        stop = n - 1 if name == "check_cancer_roll_fwd" else n
        residual = getattr(a, name + "_resid")
        worst = max(abs(residual(t)) for t in range(stop))
        assert worst < 1e-8, f"{name}_resid worst = {worst}"


def test_the_check_tolerance_is_a_named_reference_and_is_scaled(cancer, kr_cancer_anchor):
    """``roll_fwd_tol = 1e-10``, scaled by the quantity each identity is stated in.

    One Reference and no bare literal, but three scalings: the count identities scale it by
    ``pols_if_init()``, the money identities by ``sum_assured()``, and the ledgers — which
    are dimensionless probabilities — take it unscaled.  Collapsing the three would either
    reject a float64 round trip through a 3e7 column or accept a real error in a count near
    1.0.
    """
    refs = cancer.Projection.refs
    assert refs["roll_fwd_tol"] == 1e-10
    a = kr_cancer_anchor
    n = a.proj_len()
    cash = max(abs(a.check_net_cf_resid(t)) for t in range(n))
    counts = max(abs(a.check_pols_roll_fwd_resid(t)) for t in range(n))
    assert cash < 1e-10 * a.sum_assured() / 100.0
    assert counts < 1e-10 * a.pols_if_init() / 100.0


def test_the_inforce_rollforward_is_the_notes_identity(cancer):
    """l(t) − l(t+1) = deaths + lapses + maturities, on every model point.

    There is no benefit-driven termination to add: paying a diagnosis benefit neither ends
    nor exhausts the contract [S1] [S3] [S4], so a diagnosis cancels out of the identity
    because it moves a life between states rather than out of the book.  A model that
    treated a diagnosis as an exit would fail here in the first month of cover.
    """
    for point_id in cancer.Data.model_point_table().index:
        p = cancer.Projection[point_id]
        for t in range(0, p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12), (
                point_id, t)
        assert p.check_pols_roll_fwd() is True


def test_the_diagnosed_state_rolls_forward_and_the_graduations_telescope(kr_cancer_anchor):
    """l_c(t+1) = Σ_k (E_w s_w + E_n s_n), with no graduation term in the sum at all.

    Every duration bucket carries a graduation term of opposite sign to its neighbour's, so
    their sum telescopes to one line.  A sign slip or an off-by-one in the twelve-month
    delay shows up here and nowhere else in the aggregate in-force figures — which is why
    ``check_canc_dur_ledger`` exists beside it, rebuilding cohort 1 from the entry history.
    """
    a = kr_cancer_anchor
    for t in (0, 3, 12, 16, 120, 240, 600, 719):
        built = sum(a.pols_waived_exp(t, k) * a.surv_waived(t, k)
                    + a.pols_minor_exp(t, k) * a.surv_minor(t, k)
                    for k in range(1, 7))
        assert a.pols_cancer(t + 1) == pytest.approx(built, abs=1e-14)
    assert a.check_cancer_roll_fwd() is True
    assert a.check_canc_dur_ledger() is True


def test_the_decrements_are_taken_in_the_notes_processing_order(kr_cancer_anchor):
    """Transition, then mortality, then lapse — asserted through the intra-month timings.

    The order is not cosmetic and the quantity that reveals it is ``pols_if_at(t,
    "BEF_LAPSE")``: it is the three states each decremented **on its own basis**, the
    diagnosed ones bucket by bucket, so a single blended rate applied to ``pols_if`` does
    not reproduce it.  A life diagnosed in month t takes its **new** state's mortality for
    the rest of that month, which is what ``pols_waived_exp`` carries and ``pols_waived_dur``
    does not.
    """
    a = kr_cancer_anchor
    for t in (0, 3, 4, 12, 240):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "AFT_DECR") == a.pols_if(t + 1)
        built = (a.pols_healthy(t) - a.diag_first(t)) * (1.0 - a.mort_rate_mth(t))
        for k in range(1, 7):
            built += a.pols_waived_exp(t, k) * (1.0 - a.mort_rate_waived_mth(t, k))
            built += (a.pols_minor_exp(t, k)
                      * (1.0 - a.inc_rate_gen_mth(t) * a.cover(t))
                      * (1.0 - a.mort_rate_minor_mth(t, k)))
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(built, rel=1e-15)
        # Lapse is taken from the survivors of mortality, never from the start-of-month
        # count: a blended rate on pols_if would exceed the model's own figure here.
        assert a.pols_if_at(t, "BEF_LAPSE") < a.pols_if(t)
        assert a.pols_if(t + 1) < a.pols_if_at(t, "BEF_LAPSE")
    # The entrants of month t are exposed to their new state, not to the healthy one.
    assert a.pols_waived_exp(3, 1) == pytest.approx(
        a.pols_waived_dur(3, 1) + a.diag_gen(3), rel=1e-15)
    assert a.pols_minor_exp(3, 1) == pytest.approx(
        a.pols_minor_dur(3, 1) + a.diag_minor(3), rel=1e-15)
    with pytest.raises(FormulaError):
        a.pols_if_at(1, "BEF_NOTHING")


def test_the_published_statement_adds_up_on_every_model_point(cancer):
    """result_cf's own columns rebuild net_cf, which is what check_net_cf asserts.

    The guard is against a benefit kind that exists in ``claims()`` but was never given a
    column — the statement would then be silently short of outgo in the very table a reader
    is looking at.  It is asserted off the frame rather than off the cells, on every point.
    """
    for point_id in cancer.Data.model_point_table().index:
        df = cancer.Projection[point_id].result_cf()
        outgo = df[_claim_cols(df) + ["expenses", "claim_expenses",
                                      "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-6)
        assert cancer.Projection[point_id].check_net_cf() is True


def test_inforce_is_a_decreasing_probability_on_every_model_point(cancer):
    """One policy, projected on an expected basis, and nothing creates lives.

    Lapse is absorbing on this chassis — 부활 is not modelled — so ``pols_if`` is monotone
    and bounded by ``pols_if_init()``.  A reinstatement modelled as a negative lapse would
    break the monotonicity here as well as restoring cover the contract does not restore.
    """
    for point_id in cancer.Data.model_point_table().index:
        p = cancer.Projection[point_id]
        for t in range(0, p.proj_len() + 1):
            assert 0.0 <= p.pols_if(t) <= 1.0
            assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15


# ---------------------------------------------------------------------------
# Pitfall: there are two waiting periods, not one


def test_pitfall_there_are_two_waiting_periods_not_one(cancer, kr_cancer_anchor):
    """The invasive tiers attach at t = 3 and the 유사암 tier at t = 0 [S1] [S2] [S7].

    A model that reads one ``wait_months`` off the model point and applies it to all four
    tiers loses ``claims_diag_similar(0) = 177.9475000000``, the only non-zero benefit in
    the first three rows.  At young female ages the error is not small: at 만나이 30 the
    model's 유사암 incidence, 0.001136 a year, **exceeds** the invasive base rate of
    0.001005 that it is a ratio of.
    """
    a = kr_cancer_anchor
    assert a.wait_months() == 3
    assert a.tier_wait_months("similar") == 0 < a.tier_wait_months("general")
    for t in (0, 1, 2):
        assert a.cover(t) == 0.0 and a.cover_similar(t) == 1.0
        assert a.claims(t, "DIAG_SIMILAR") > 0.0
        assert a.claims(t, "DIAG_GEN") == a.claims(t, "DIAG_HIGH") == 0.0
        assert a.claims(t, "DIAG_MINOR") == 0.0
    assert a.claims(0, "DIAG_SIMILAR") == pytest.approx(177.9475000000, abs=MONEY)
    p4 = cancer.Projection[4]                       # female, 만나이 30
    assert p4.sex() == "F" and p4.issue_age() == 30
    assert p4.inc_rate(0) == pytest.approx(0.001005, abs=5e-9)
    assert p4.inc_rate(0) * p4.similar_share(0) == pytest.approx(0.001136, abs=5e-7)
    assert p4.similar_share(0) > 1.0


def test_pitfall_the_waiting_period_is_a_hard_zero_and_stops_the_transition(
        kr_cancer_anchor):
    """A hard zero, not a reduced rate, and it gates the transition as well as the benefit.

    Gating only the claim leaves a diagnosed population the contract says does not exist:
    ``pols_minor(3)`` and ``pols_waived(3)`` are **exactly** 0.0, so every care line at
    ``t = 3`` is exactly zero too.  ``check_waiting_period()`` sums the three invasive
    diagnosis benefits **and** ``diag_first`` for every ``t < 3``.
    """
    a = kr_cancer_anchor
    for t in (0, 1, 2):
        assert a.diag_gen(t) == a.diag_minor(t) == a.diag_high(t) == 0.0
        assert a.diag_first(t) == 0.0
        assert a.check_waiting_period_resid(t) == 0.0
    assert a.pols_minor(3) == 0.0 and a.pols_waived(3) == 0.0
    assert a.pols_healthy(3) == a.pols_if(3)
    assert a.claims(3, "HOSP") == a.claims(3, "SURGERY") == a.claims(3, "TREAT") == 0.0
    assert a.check_waiting_period() is True
    # The 유사암 tier is deliberately not in the residual: it has no waiting period, and a
    # check asserting a zero there would be asserting the wrong product.
    assert a.diag_similar(0) > 0.0 and a.check_waiting_period_resid(0) == 0.0


def test_pitfall_the_premium_is_still_charged_inside_the_waiting_period(kr_cancer_anchor):
    """premiums(0) = 45,000.0000000000, at full rate, with no invasive cover in force.

    The 유사암 tier and every non-cancer cover are already in force from day 1, and the
    invalidity rule returns the premium for the *affected cover* if a diagnosis falls inside
    the window [S1] [S2] [S3].  Suppressing the premium and the benefit together is a
    different product.
    """
    a = kr_cancer_anchor
    assert a.premiums(0) == 45000.0
    assert a.prem_payable(0) == 1.0 and a.cover(0) == 0.0
    assert a.premiums(1) == pytest.approx(45000.0 * a.pols_payer(1), rel=1e-15)
    assert a.premiums(2) > 0.0
    assert a.prem_alloc_pp(0) == 38250.0            # and it feeds the account from t = 0
    assert a.av_pp(1) > 0.0


def test_pitfall_an_in_window_diagnosis_voids_the_cover_it_does_not_lapse_it():
    """상법 제644조 makes the cover 무효 and its premiums returnable — a de-recognition.

    It releases the premium already collected as well as the future benefit, so it belongs
    in a validity adjustment at outset rather than in the lapse column; putting it there
    keeps premium income the insurer never earned.  The base run leaves the adjustment off,
    so ``void_prob()`` returns 0.0 and ``pols_if_init()`` is exactly 1.0; switched on it is
    0.0003357124 and scales the whole exposure down.
    """
    model = _reread("void")
    try:
        base = model.Projection[1]
        assert base.void_prob() == 0.0 and base.pols_if_init() == 1.0
        base_lapse = float(base.pols_lapse(0))
        model.Projection.void_adjust = True
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.void_prob() == pytest.approx(0.0003357124, abs=5e-11)
        assert p.void_prob() == pytest.approx(
            1.0 - (1.0 - p.inc_rate(0) / 12.0) ** 3, rel=1e-14)
        assert p.pols_if_init() == pytest.approx(1.0 - 0.0003357124, abs=5e-11)
        assert p.pols_if(0) == p.pols_if_init()
        # It scales the exposure; it is not a lapse, so the roll-forward still closes.
        assert p.check_pols_roll_fwd() is True
        assert p.pols_lapse(0) < base_lapse
        assert p.pols_lapse(0) == pytest.approx(
            base_lapse * p.pols_if_init(), rel=1e-14)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: two weights on two lines of the same row


def test_pitfall_premiums_ride_on_the_payers_and_expenses_on_the_whole_book(cancer,
                                                                           kr_cancer_anchor):
    """premiums on pols_healthy + pols_minor; the maintenance expense on pols_if.

    Weighting the premium by ``pols_if`` is the single largest arithmetic error available in
    this product, and it is **invisible for the first four rows**, where the two weights are
    equal — which is exactly why it survives a first-year test.  At ``t = 4`` the difference
    is ₩4.03; by 납입완료 the waived state is 3.69% of the block.
    """
    a = kr_cancer_anchor
    for t in (0, 1, 2, 3):
        assert a.pols_payer(t) == a.pols_if(t)
    assert a.pols_payer(4) < a.pols_if(4)
    for t in (4, 12, 120, 239):
        assert a.pols_payer(t) == pytest.approx(
            a.pols_healthy(t) + a.pols_minor(t), rel=1e-15)
        assert a.premiums(t) == pytest.approx(45000.0 * a.pols_payer(t), rel=1e-15)
        assert a.expenses(t) == pytest.approx(
            2500.0 * a.inflation_factor(t) * a.pols_if(t), rel=1e-14)
    assert a.pols_if(240) - a.pols_payer(240) == pytest.approx(
        a.pols_waived(240), rel=1e-15)
    assert a.pols_waived(240) / a.pols_if(240) == pytest.approx(0.0369, abs=5e-5)
    # On the waiver_trigger = "none" design the two weights coincide by construction.
    p9 = cancer.Projection[9]
    assert p9.waiver_trigger() == "none"
    assert all(p9.pols_payer(t) == p9.pols_if(t) for t in (0, 12, 120, 239))


def test_pitfall_the_reduced_tiers_do_not_waive_the_premium(cancer, kr_cancer_anchor):
    """특정소액암 does not waive and 유사암 does not either — the 약관 says so by name.

    「특정 소액암 … 은 보험료 납입을 면제하지 않습니다」 [S3 제14조제1항] [S1 제9조제1항].
    Folding the 특정소액암 state into the waived state stops a premium the contract goes on
    charging: at ``t = 240`` that is 0.0127869424 of the block, 1.77% of the in-force, and
    for the twenty years before it, real money.
    """
    a = kr_cancer_anchor
    tiers = a.data.tier_table()
    assert int(tiers.loc["general", "waives_premium"]) == 1
    assert int(tiers.loc["high", "waives_premium"]) == 1
    assert int(tiers.loc["minor", "waives_premium"]) == 0
    assert int(tiers.loc["similar", "waives_premium"]) == 0
    assert a.pols_minor(240) == pytest.approx(0.0127869424, abs=INFORCE)
    assert a.pols_minor(240) / a.pols_if(240) == pytest.approx(0.0177, abs=5e-5)
    assert a.pols_payer(240) > a.pols_healthy(240)
    # A 유사암 diagnosis moves no life anywhere at all, so it cannot stop a premium.
    assert a.diag_similar(0) > 0.0
    assert a.pols_minor(1) == a.pols_waived(1) == 0.0


def test_pitfall_a_minor_life_can_lapse_and_a_waived_life_cannot(kr_cancer_anchor):
    """lapse_rate_canc_mth is identically zero; the 특정소액암 state carries the full rate.

    A waived life has no premium to miss and, on the 미지급형 form, no surrender value to
    take [S3 제41조] [REG-R28], so there is no mechanism by which a waived policy leaves the
    book other than death.  Applying one rule to both diagnosed states either deletes
    exactly the claimants the product exists to pay, or keeps ghosts.
    """
    a = kr_cancer_anchor
    assert all(a.lapse_rate_canc_mth(t) == 0.0 for t in (0, 12, 240, 600, 719))
    for t in (12, 120, 240):
        assert a.surv_waived(t, 1) == pytest.approx(
            1.0 - a.mort_rate_waived_mth(t, 1), rel=1e-15)
        assert a.surv_minor(t, 1) == pytest.approx(
            (1.0 - a.inc_rate_gen_mth(t) * a.cover(t))
            * (1.0 - a.mort_rate_minor_mth(t, 1))
            * (1.0 - a.lapse_rate_mth(t)), rel=1e-15)
        # The lapse flow carries a 특정소액암 limb and no waived limb.
        minor_limb = sum(
            a.pols_minor_exp(t, k) * (1.0 - a.inc_rate_gen_mth(t) * a.cover(t))
            * (1.0 - a.mort_rate_minor_mth(t, k)) * a.lapse_rate_mth(t)
            for k in range(1, 7))
        healthy_limb = ((a.pols_healthy(t) - a.diag_first(t))
                        * (1.0 - a.mort_rate_mth(t)) * a.lapse_rate_mth(t))
        assert a.pols_lapse(t) == pytest.approx(minor_limb + healthy_limb, rel=1e-14)
        assert minor_limb > 0.0


def test_the_diagnosed_lapse_loading_is_inert_under_the_waiver_and_live_without_it():
    """lapse_canc_factor reaches a cash flow only on the waiver_trigger = "none" design.

    It is inert rather than off: under the waiver ``lapse_rate_canc_mth`` returns zero
    whatever the factor is, so the switch is a statement about the *product* and not about
    the base run's calibration.
    """
    model = _reread("cancl")
    try:
        model.Projection.lapse_canc_factor = 2.0
        model.Projection.clear_all()
        assert model.Projection[1].lapse_rate_canc_mth(0) == 0.0
        p9 = model.Projection[9]
        assert p9.lapse_rate_canc_mth(0) == pytest.approx(
            2.0 * p9.lapse_rate_mth(0), rel=1e-15)
        assert p9.check_pols_roll_fwd() is True
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: the tier algebra — a partition, a subset and an addition


def test_pitfall_high_cost_cancer_pays_in_addition_not_instead(kr_cancer_anchor):
    """claims_diag_gen(3) and claims_diag_high(3) are both paid on overlapping flows.

    ₩1,360.11 and ₩49.76, so a leukaemia collects 200% of ``S`` and a stomach cancer 100%
    [S3].  ``i_h`` is a **subset** of the general tier, so ``check_tier_shares()`` asserts
    ``i_h ≤ i_g`` and **not** that the four shares sum to one; treating 고액암 as a fifth
    slice of a partition halves it.
    """
    a = kr_cancer_anchor
    assert a.claims(3, "DIAG_GEN") == pytest.approx(1360.1145372945, abs=MONEY)
    assert a.claims(3, "DIAG_HIGH") == pytest.approx(49.7602879498, abs=MONEY)
    for t in (3, 12, 240, 600):
        assert a.inc_rate_high_mth(t) <= a.inc_rate_gen_mth(t)
        assert a.diag_high(t) < a.diag_gen(t)
        assert a.claims(t, "DIAG_GEN") + a.claims(t, "DIAG_HIGH") == pytest.approx(
            a.sum_assured() * a.reduction_factor(t)
            * (a.diag_gen(t) + a.diag_high(t)), rel=1e-14)
    # 고액암 does not reduce the general flow: n_g is built without reference to n_h.
    assert a.diag_gen(3) == pytest.approx(a.diag_gen_h(3) + a.diag_gen_m(3), rel=1e-15)


def test_pitfall_the_similar_tier_is_additive_to_the_base_rate(cancer, kr_cancer_anchor):
    """similar_share can and does exceed 1.0 — 1.60 at female 만나이 20.

    The published grid **excludes** 기타피부암 (C44) and 갑상선암 (C73) by construction
    [R5] [REG-R61], which is exactly the 유사암 boundary, so the tier is outside the base
    rate's own definition rather than a slice of it.  A model that constrains the four
    shares to sum to one prices the reduced tier out of existence at precisely the ages
    where it dominates.
    """
    shares = cancer.Data.tier_share_table()
    assert float(shares.loc[("F", 20), "similar_share"]) == 1.60
    a = kr_cancer_anchor
    for t in (0, 12, 240, 480):
        assert a.inc_rate_gen_mth(t) + a.inc_rate_minor_mth(t) == pytest.approx(
            a.inc_rate(t) / 12.0, rel=1e-15)
        assert a.inc_rate_similar_mth(t) >= 0.0
        assert a.check_tier_shares_resid(t) == pytest.approx(0.0, abs=1e-15)
    # The four shares emphatically do not sum to one at the anchor's own age.
    assert (a.minor_share(0) + (1.0 - a.minor_share(0)) + a.high_share(0)
            + a.similar_share(0)) > 1.0
    assert a.check_tier_shares() is True


def test_pitfall_the_reduction_period_is_a_first_year_phenomenon(cancer, kr_cancer_anchor):
    """g(t) = 0.50 for t < 12 and 1.00 after, on the four diagnosis lines and nothing else.

    Baking 0.50 into the benefit ratio halves the liability for sixty years instead of one.
    It does not touch the inpatient, surgery or treatment limbs — whose real clock runs to
    the 수술일 rather than the 진단확정일 [S4] [S5] — and on a 갱신계약 it is disapplied
    altogether [S2] [S4], which the model point carries as ``reduction_months = 0``.
    """
    a = kr_cancer_anchor
    assert a.reduction_months() == 12
    assert all(a.reduction_factor(t) == 0.50 for t in range(0, 12))
    assert all(a.reduction_factor(t) == 1.00 for t in (12, 13, 240, 720))
    for t in (3, 11, 12):
        assert a.claims(t, "DIAG_GEN") == pytest.approx(
            1.00 * a.sum_assured() * a.reduction_factor(t) * a.diag_gen(t), rel=1e-15)
        assert a.claims(t, "DIAG_MINOR") == pytest.approx(
            0.60 * a.sum_assured() * a.reduction_factor(t) * a.diag_minor(t), rel=1e-15)
    # The care limbs are untouched by it: the t = 11 -> 12 step is not 2.0 on them.
    assert a.claims(12, "HOSP") / a.claims(11, "HOSP") < 1.2
    assert a.claims(12, "SURGERY") / a.claims(11, "SURGERY") < 1.2
    # The 갱신형 chassis flag disapplies it, and the 24-month design is exercised too.
    p3 = cancer.Projection[3]
    assert p3.chassis() == "gaengsin" and p3.reduction_months() == 0
    assert all(p3.reduction_factor(t) == 1.00 for t in (0, 6, 11))
    assert p3.tier_wait_months("general") == 0 and p3.cover(0) == 1.0
    p4 = cancer.Projection[4]
    assert p4.reduction_months() == 24
    assert p4.reduction_factor(23) == 0.50 and p4.reduction_factor(24) == 1.00


# ---------------------------------------------------------------------------
# Pitfall: flows, stocks and the cohort clock


def test_pitfall_diagnosis_lines_ride_on_flows_and_care_lines_on_stocks(kr_cancer_anchor):
    """claims_diag_* use the month's new diagnoses; claims_hosp/surgery/treat use the stock.

    Multiplying a care intensity by a diagnosis flow understates the care limbs by the mean
    diagnosed duration, which on this basis runs from 57 at 만나이 50 to 148 at 80 and goes on
    rising.  The two are different objects with different dimensions, and the model publishes
    both.
    """
    a = kr_cancer_anchor
    care = a.data.care_table()
    for t in (4, 12, 240, 480):
        stock = sum(a.pols_diag_dur(t, k) for k in range(1, 7))
        assert a.claims(t, "HOSP") == pytest.approx(
            a.hosp_daily() * sum(float(care.loc[k, "hosp_adm_yr"]) / 12.0
                                 * min(float(care.loc[k, "hosp_days_adm"]),
                                       a.hosp_day_cap())
                                 * a.pols_diag_dur(t, k) for k in range(1, 7)),
            rel=1e-13)
        assert a.claims(t, "SURGERY") == pytest.approx(
            sum((a.surg_open_amt() * float(care.loc[k, "surg_open_yr"])
                 + a.surg_closed_amt() * float(care.loc[k, "surg_closed_yr"])) / 12.0
                * a.pols_diag_dur(t, k) for k in range(1, 7)), rel=1e-13)
        assert stock == pytest.approx(a.pols_cancer(t), rel=1e-14)
    # Once the diagnosed population has accumulated, the stock outgrows the flow it came
    # from by the mean diagnosed duration, and that ratio is the size of the error: 57 at
    # 만나이 50, 80 at 60 and 148 at 80, rising for as long as survival improves on the
    # incidence curve.
    ratios = []
    for t in (120, 240, 480):
        stock = sum(a.pols_diag_dur(t, k) for k in range(1, 7))
        ratios.append(stock / (a.diag_gen(t) + a.diag_minor(t)))
    assert ratios == sorted(ratios)
    assert ratios[0] > 50.0 and ratios[-1] > 100.0
    assert a.pols_diag_dur(12, 1) == pytest.approx(
        a.pols_waived_dur(12, 1) + a.pols_minor_dur(12, 1), rel=1e-15)


def test_pitfall_the_care_limbs_start_one_month_after_the_diagnosis_limbs(
        kr_cancer_anchor):
    """claims_hosp(3) = 0 and claims_hosp(4) = 13.6639954092.

    A life diagnosed in month 3 is in the diagnosed **stock** from month 4, because the care
    lines ride on ``D`` and not on ``E``: the month's own entrants do not draw a care benefit
    in their diagnosis month.  A model that recognises a treatment episode in the diagnosis
    month shifts the whole care stream forward by a month.
    """
    a = kr_cancer_anchor
    assert a.claims(3, "DIAG_GEN") > 0.0
    assert a.claims(3, "HOSP") == a.claims(3, "SURGERY") == a.claims(3, "TREAT") == 0.0
    assert a.claims(4, "HOSP") == pytest.approx(13.6639954092, abs=MONEY)
    assert a.claims(4, "SURGERY") == pytest.approx(30.0607899003, abs=MONEY)
    assert a.claims(4, "TREAT") == pytest.approx(59.9916774089, abs=MONEY)
    assert all(a.pols_diag_dur(3, k) == 0.0 for k in range(1, 7))
    assert a.pols_diag_dur(4, 1) > 0.0


def test_pitfall_the_cohort_delay_is_thirteen_months_not_twelve(kr_cancer_anchor):
    """waived_grad(t, 1) reads diag_gen(t − 13), the entry month being a full month of it.

    ``check_canc_dur_ledger()`` rebuilds cohort 1 independently from the entry history and
    is the **only** check that fails on an off-by-one here: ``check_cancer_roll_fwd()`` and
    ``check_pols_roll_fwd()`` both still close, because the graduation terms telescope out
    of the state total.
    """
    a = kr_cancer_anchor
    first_entry = 3                                  # the 암보장개시일
    assert all(a.waived_grad(t, 1) == 0.0 for t in range(0, first_entry + 13))
    assert a.waived_grad(first_entry + 13, 1) > 0.0
    factor = 1.0
    for u in range(first_entry, first_entry + 13):
        factor *= a.surv_waived(u, 1)
    assert a.waived_grad(16, 1) == pytest.approx(a.diag_gen(3) * factor, rel=1e-14)
    assert a.minor_grad(16, 1) > 0.0 and a.minor_grad(15, 1) == 0.0
    # Cohort 1 rebuilt straight off the entry history, which is the check's own identity.
    for t in (16, 24, 120):
        built = 0.0
        factor = 1.0
        for s in range(t - 1, max(t - 13, -1), -1):
            factor *= a.surv_waived(s, 1)
            built += a.diag_gen(s) * factor
        assert a.pols_waived_dur(t, 1) == pytest.approx(built, abs=1e-16)
    assert a.check_canc_dur_ledger() is True


# ---------------------------------------------------------------------------
# Pitfall: the two once-only ledgers


def test_pitfall_the_treatment_ledger_is_per_diagnosed_life(kr_cancer_anchor):
    """treat_cum_pp converges to 0.7516253263 and never passes 1, because θ_ultimate = 0.

    ``treat_avail(k)`` is a per-life availability read at the **midpoint** of select year k,
    so ``treat_avail(1) = 0.5488116361`` and not 1.0.  Weighting it by ``pols_cancer``
    measures the block's consumption rather than the individual's and defers exhaustion for
    ever; and a non-zero ultimate hazard would break the 최초 1회한 bound at long horizons.
    """
    a = kr_cancer_anchor
    assert a.treat_avail(1) == pytest.approx(0.5488116361, abs=5e-11)
    assert float(a.data.care_table().loc[6, "treat_hazard_yr"]) == 0.0
    assert a.treat_cum_pp(720) == pytest.approx(0.7516253263, abs=5e-11)
    assert a.treat_cum_pp(720) == a.treat_cum_pp(719)      # the ultimate adds nothing
    assert a.treat_cum_pp(600) == a.treat_cum_pp(720)
    for t in range(0, 721, 60):
        assert 0.0 <= a.treat_cum_pp(t) <= 1.0
        assert a.check_treat_ledger_resid(t) == 0.0
    assert a.check_treat_ledger() is True
    # It is a function of elapsed duration alone, so it does not scale with the block.
    assert a.treat_cum_pp(12) > a.pols_cancer(12)


def test_pitfall_the_similar_ledger_rides_on_pols_if_not_pols_healthy(kr_cancer_anchor):
    """A life who has already had an invasive cancer can still collect a 유사암 benefit.

    No payment terminates or exhausts the contract [S1] [S3] [S4], so the tier's flow
    attaches to the **whole in-force** against a per-policy availability ledger.
    ``check_similar_ledger()`` asserts ``similar_avail(t) + similar_used(t) = 1`` with the
    used side accumulated off the **published claim line**, so the identity cannot close by
    construction.
    """
    a = kr_cancer_anchor
    for t in (0, 12, 240, 480, 720):
        assert a.diag_similar(t) == pytest.approx(
            a.pols_if(t) * a.similar_avail(t) * a.inc_rate_similar_mth(t)
            * a.cover_similar(t) * a.diag_module(), rel=1e-14)
        assert a.similar_avail(t) + a.similar_used(t) == pytest.approx(1.0, abs=1e-13)
    assert a.similar_avail(720) == pytest.approx(0.9172290909, abs=5e-11)
    assert 1.0 - a.similar_avail(720) == pytest.approx(0.0828, abs=5e-5)
    assert a.check_similar_ledger() is True
    # It rides on pols_if: at t = 480 the diagnosed are 27% of the book and are included.
    assert a.pols_if(480) > a.pols_healthy(480)
    assert a.diag_similar(480) > (a.pols_healthy(480) * a.similar_avail(480)
                                  * a.inc_rate_similar_mth(480))


# ---------------------------------------------------------------------------
# Pitfall: the post-diagnosis basis


def test_pitfall_relative_survival_is_an_excess_hazard_not_a_table(kr_cancer_anchor):
    """The public quantity is a **ratio to expected general-population survival** [R1].

    So it converts into an excess hazard **added to** the base table, never into a
    replacement for it; multiplying survivorship by a relative-survival figure double-counts
    the background.  The tell is the five select-year hazards summing to −ln(0.659) rather
    than to anything resembling a survival probability.
    """
    a = kr_cancer_anchor
    for t in (0, 120, 480):
        for k in (1, 3, 6):
            assert a.mort_rate_waived_mth(t, k) == pytest.approx(
                1.0 - (1.0 - a.mort_rate_mth(t))
                * math.exp(-a.excess_hazard("general", k) / 12.0), rel=1e-15)
            assert a.mort_rate_waived_mth(t, k) > a.mort_rate_mth(t)
    # A flat hazard fitted to the same five-year point would kill long survivors far too
    # fast, which is the reason the six buckets exist at all.
    flat = -math.log(0.659) / 5.0
    assert flat == pytest.approx(0.0834063, abs=5e-8)
    assert a.excess_hazard("general", 1) > flat > a.excess_hazard("general", 5)
    assert a.excess_hazard("general", 6) < a.excess_hazard("general", 5)


def test_pitfall_the_similar_tier_carries_no_excess_mortality_and_no_care(cancer,
                                                                         kr_cancer_anchor):
    """The 유사암 tier appears in **no row** of survival_table.csv, by design.

    갑상선 five-year relative survival is 100.2% and lifetime 갑상선 mortality risk 0.1%
    [R1].  Routing 유사암 into the diagnosed population credits it with an exposure no
    retrieved statistic measures, and gives it a mortality the registry says it does not
    have; it draws the lump sum and nothing continuing.
    """
    table = cancer.Data.survival_table()
    assert set(table.index.get_level_values("tier")) == {"general", "minor"}
    with pytest.raises(KeyError):
        table.loc[("M", "similar", 1)]
    a = kr_cancer_anchor
    with pytest.raises(FormulaError):
        a.excess_hazard("similar", 1)
    # A 유사암 diagnosis moves no life: months 0-2 pay the tier and the states stay empty.
    assert a.diag_similar(0) > 0.0 and a.diag_similar(1) > 0.0
    assert a.pols_minor(1) == a.pols_waived(1) == a.pols_cancer(1) == 0.0
    assert a.pols_healthy(1) == a.pols_if(1)
    assert a.claims(1, "HOSP") == a.claims(1, "SURGERY") == a.claims(1, "TREAT") == 0.0


# ---------------------------------------------------------------------------
# Pitfall: the surrender-value machinery


def test_pitfall_the_surrender_charge_cap_uses_a_notional_face_amount(cancer,
                                                                     kr_cancer_anchor):
    """This product has no death benefit, so [별표 15] 제9호 supplies a *notional* face.

    Feeding the headline 보험가입금액 into the [별표 14] formula gives 459,000 + 300,000 =
    759,000 instead of 459,000 + 180,000 = 639,000 on the anchor cell — and because the
    13-month cap of ₩585,000 binds either way, **the error is invisible there**.  It is
    visible on model point 10, where the formula binds instead of the cap.
    """
    a = kr_cancer_anchor
    assert a.notional_sa_ratio == 0.60
    headline = 459000.0 * 0.05 * 20.0 + 30000000.0 * 0.01
    notional = 459000.0 * 0.05 * 20.0 + 30000000.0 * 0.60 * 0.01
    assert (headline, notional) == (759000.0, 639000.0)
    assert min(headline, 585000.0) == min(notional, 585000.0) == 585000.0
    assert a.surr_chg_cap_pp() == 585000.0
    p10 = cancer.Projection[10]
    ann_net = 12.0 * 23000.0 * 0.85
    formula_notional = ann_net * 0.05 * 20.0 + 10000000.0 * 0.60 * 0.01
    formula_headline = ann_net * 0.05 * 20.0 + 10000000.0 * 0.01
    cap = 13.0 * 23000.0
    assert p10.surr_chg_cap_pp() == pytest.approx(formula_notional, abs=WON)
    assert p10.surr_chg_cap_pp() < cap < formula_headline
    assert p10.surr_chg_cap_pp() != pytest.approx(min(formula_headline, cap), abs=1.0)


def test_pitfall_the_cliff_at_completion_is_not_the_surrender_charge_running_off(
        kr_cancer_anchor):
    """surr_chg_pp(84) = 0 — thirteen years before the 미지급형 cliff at t = 240.

    The 해약공제기간 is capped at seven years by 제7-66조제1항제2호 [REG-R19].  Two
    independent mechanisms, thirteen years apart; conflating them puts the cliff in the
    wrong place on every model point whose 납입기간 exceeds seven years.
    """
    a = kr_cancer_anchor
    assert a.surr_chg_months() == 84 == 12 * 7
    assert a.surr_chg_pp(0) == a.surr_chg_cap_pp() == 585000.0
    assert a.surr_chg_pp(42) == pytest.approx(585000.0 * 0.5, abs=SIX)
    assert a.surr_chg_pp(84) == 0.0 and a.surr_chg_pp(240) == 0.0
    # The 표준형 value is already positive long before the cliff, and cv_pp is still nil.
    assert a.cv_std_pp(84) > 0.0 and a.cv_pp(84) == 0.0
    assert a.cv_std_pp(239) > 0.0 and a.cv_pp(239) == 0.0
    assert a.cv_pp(240) == pytest.approx(0.5 * a.cv_std_pp(240), rel=1e-15)


def test_pitfall_two_prescribed_steps_land_in_the_same_row(kr_cancer_anchor):
    """The surrender value steps to ₩4,078,536.79 and the lapse rate from 0.1% to 0.8%.

    Both are prescribed rather than chosen — [S3 제41조] and [REG-R27] — and together they
    produce the model's only discontinuity in ``claims_lapse``, from ₩0.00 to ₩1,891.71.
    Implementing one and not the other gives a plausible-looking row that is wrong by the
    whole of the other factor.
    """
    a = kr_cancer_anchor
    assert a.cv_pp(239) == 0.0
    assert a.cv_pp(240) == pytest.approx(4078536.787114, abs=SIX)
    assert a.lapse_rate(239) == pytest.approx(0.001, rel=1e-14)
    assert a.lapse_rate(240) == 0.008
    assert a.claims(239, "LAPSE") == 0.0
    assert a.claims(240, "LAPSE") == pytest.approx(1891.7076416342, abs=MONEY)
    assert a.premiums(239) > 0.0 and a.premiums(240) == 0.0


def test_pitfall_claims_lapse_is_identically_zero_through_the_payment_period(cancer,
                                                                            kr_cancer_anchor):
    """cv_pp(t) = 0 for every t < 240 on the 미지급형 form, so twenty years cost nothing.

    On a **전기납** 미지급형 contract — model point 7 — it is zero at *every* duration,
    because the payment period never ends [S3 제41조].  ``check_cv_floor()`` asserts the nil
    as well as the two bounds, because a model that let a suppressed-surrender-value
    contract pay during the payment period would be modelling a 표준형 product under a
    무해지 premium.
    """
    a = kr_cancer_anchor
    df = a.result_cf()
    assert (df.loc[0:239, "claims_lapse"] == 0.0).all()
    assert df.loc[240, "claims_lapse"] > 0.0
    assert all(a.cv_pp(t) == 0.0 for t in (0, 12, 84, 120, 239))
    assert any(a.pols_lapse(t) > 0.0 for t in (0, 12, 120, 239))
    assert a.check_cv_floor() is True
    p7 = cancer.Projection[7]
    assert p7.pay_term() == 0 and p7.cv_form() == "mijigeup"
    assert (p7.result_cf()["claims_lapse"] == 0.0).all()
    assert all(p7.cv_pp(t) == 0.0 for t in (0, 120, 300, 539))
    assert p7.check_cv_floor() is True
    # And the 표준형 comparator, which cannot be bought, does pay: model point 9.
    p9 = cancer.Projection[9]
    assert p9.cv_form() == "pyojun"
    assert all(p9.cv_pp(t) == p9.cv_std_pp(t) for t in (0, 60, 120, 240))
    assert p9.result_cf()["claims_lapse"].sum() > 0.0


# ---------------------------------------------------------------------------
# Pitfall: the account, and a payment on death with no death benefit


def test_pitfall_there_is_a_payment_on_death_and_no_death_benefit(cancer,
                                                                 kr_cancer_anchor):
    """claims_death(t) = av_pp(t) × pols_death(t) — the 계약자적립액, not a sum assured.

    감독규정 제7-63조제1항제1호 requires a 제3보험 product to be designed so that death from
    a cause the policy does not cover pays the 계약자적립액 and terminates the contract
    [REG-R17] [REG-R25 제22조].  Modelling it as a sum assured invents a benefit; omitting it
    drops a requirement ``LTC_KR_S``, ``Child_KR_S`` and ``Medical_KR_S`` all inherit.
    """
    a = kr_cancer_anchor
    for t in (0, 1, 12, 240, 446, 447):
        assert a.claims(t, "DEATH") == pytest.approx(
            a.av_pp(t) * a.pols_death(t), rel=1e-15)
    assert a.claims(0, "DEATH") == 0.0 and a.av_pp(0) == 0.0
    assert a.pols_death(0) > 0.0                     # deaths happen; nothing is paid
    assert a.claims(1, "DEATH") > 0.0
    # It is never a multiple of the sum assured.
    assert a.claims(12, "DEATH") < 1e-3 * a.sum_assured() * a.pols_death(12) * 1e3
    assert a.av_pp(12) < a.sum_assured()
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    for absent in ("death_benefit", "sum_assured_death", "claims_death_sa"):
        assert absent not in names, f"{absent} would invent a death benefit"


def test_pitfall_the_account_floor_binds_and_the_lines_that_ride_on_it_stop(
        kr_cancer_anchor):
    """av_pp(447) = 0 and stays zero to expiry, at 만나이 77 — 62% through the term.

    A recursion allowed to go negative would carry a fictitious asset and would keep paying
    ``claims_death`` out of it; one whose floor is forgotten produces a negative
    ``claims_death``, which ``check_net_cf()`` will **not** catch because the identity still
    balances.  So the floor is asserted on the account and on both lines that ride on it.
    """
    a = kr_cancer_anchor
    assert a.av_pp(446) > 0.0 and a.av_pp(447) == 0.0
    assert all(a.av_pp(t) == 0.0 for t in (447, 480, 600, 720))
    assert all(a.av_pp(t) >= 0.0 for t in range(0, 721, 12))
    df = a.result_cf()
    assert (df["claims_death"] >= 0.0).all() and (df["claims_lapse"] >= 0.0).all()
    assert (df.loc[447:720, "claims_death"] == 0.0).all()
    assert a.av_pp(240) == pytest.approx(8157073.574228, abs=SIX)   # the peak
    assert a.av_pp(240) > a.av_pp(241)
    assert a.age(447) == 77


def test_pitfall_risk_prem_pp_excludes_the_accounts_own_payments(kr_cancer_anchor):
    """The seven cancer benefit lines, and neither DEATH nor LAPSE.

    They are payments *out of* the account, so including them in the account's own outgo
    makes the recursion self-referential — modelx would raise rather than silently
    mis-answer, but a hand implementation will not.
    """
    a = kr_cancer_anchor
    seven = ("DIAG_GEN", "DIAG_HIGH", "DIAG_MINOR", "DIAG_SIMILAR", "HOSP",
             "SURGERY", "TREAT")
    for t in (0, 3, 12, 240):
        assert a.risk_prem_pp(t) == pytest.approx(
            sum(a.claims(t, k) for k in seven) / a.pols_if(t), rel=1e-14)
        assert a.risk_prem_pp(t) * a.pols_if(t) < a.claims(t) + 1e-9
    assert a.risk_prem_pp(240) * a.pols_if(240) == pytest.approx(
        a.claims(240) - a.claims(240, "DEATH") - a.claims(240, "LAPSE")
        - a.claims(240, "MATURITY"), rel=1e-13)
    assert a.av_pp(1) == pytest.approx(
        max(0.0, (a.av_pp(0) + a.prem_alloc_pp(0) - a.risk_prem_pp(0))
            * 1.025 ** (1.0 / 12.0)), rel=1e-15)


def test_pitfall_nothing_is_paid_at_the_hundredth_birthday(cancer, kr_cancer_anchor):
    """claims_maturity is 0.0000000000 in every row, on a real surviving exposure.

    ``pols_maturity(720) = 0.0103446076`` of cover simply ends [S8]; the kind exists so that
    the zero is stated rather than left to inference, and the column is published rather
    than dropped.  A maturity benefit is a different product — the 만기환급형 2종 variant,
    out of scope.
    """
    a = kr_cancer_anchor
    df = a.result_cf()
    assert "claims_maturity" in df.columns
    assert (df["claims_maturity"] == 0.0).all()
    assert a.pols_maturity(720) == pytest.approx(0.0103446076, abs=INFORCE)
    assert a.pols_maturity(720) == a.pols_if(720)
    assert all(a.pols_maturity(t) == 0.0 for t in (0, 12, 240, 719))
    assert a.in_force(719) == 1.0 and a.in_force(720) == 0.0
    assert a.pols_death(720) == a.pols_lapse(720) == 0.0
    for point_id in cancer.Data.model_point_table().index:
        p = cancer.Projection[point_id]
        last = p.proj_len() - 1
        assert p.claims(last, "MATURITY") == 0.0
        assert p.pols_maturity(last) == p.pols_if(last) > 0.0
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    for absent in ("maturity_benefit", "maturity_ratio", "claims_maturity_pp"):
        assert absent not in names, f"{absent} belongs to a 만기환급형 design"


# ---------------------------------------------------------------------------
# Pitfall: reading the published statement


def test_pitfall_no_claims_aggregate_column_beside_the_splits(cancer, kr_cancer_anchor):
    """Ten ``claims_*`` split columns and nothing named ``claims``.

    A statement carrying its own subtotal among its parts is silently non-additive for any
    reader who sums the row, and it would double the benefit side of ``check_net_cf()``.
    The total remains available as the ``claims(t, kind)`` cells with ``kind`` omitted; it is
    the *column* that is not published.
    """
    df = kr_cancer_anchor.result_cf()
    assert "claims" not in df.columns
    assert len(_claim_cols(df)) == 10
    assert list(df.columns) == [
        "pols_if", "pols_healthy", "pols_minor", "pols_waived", "premiums",
        "claims_diag_gen", "claims_diag_high", "claims_diag_minor",
        "claims_diag_similar", "claims_hosp", "claims_surgery", "claims_treat",
        "claims_death", "claims_lapse", "claims_maturity", "expenses",
        "claim_expenses", "commissions", "net_cf"]
    assert df.index.name == "t" and list(df.index) == list(range(0, 721))
    assert "claims" in cancer.Projection.cells
    for t in (0, 12, 240):
        assert kr_cancer_anchor.claims(t) == pytest.approx(
            df.loc[t, _claim_cols(df)].sum(), abs=1e-9)
    with pytest.raises(FormulaError):
        kr_cancer_anchor.claims(1, "NOT_A_KIND")


def test_pitfall_rounded_lines_do_not_re_add(kr_cancer_anchor):
    """The displayed monthly rows do not re-add to the notes' year-1 totals, and must not.

    The totals are sums of **unrounded** monthly values, so a test written against a sum of
    displayed figures would fail against a correct model.  The gap is asserted here so the
    convention is visible rather than discovered.
    """
    a = kr_cancer_anchor
    df = a.result_cf()
    exact = df.loc[0:11, "claims_diag_gen"].sum()
    displayed = sum(WE_DIAG[t][1] for t in range(0, 12))
    assert exact == pytest.approx(YEAR_ONE["claims_diag_gen"], abs=MONEY)
    assert displayed == pytest.approx(exact, abs=1e-8)
    # And the displayed values are genuinely rounded: they are not the model's own floats.
    assert any(df.loc[t, "claims_diag_gen"] != WE_DIAG[t][1] for t in range(3, 12))


def test_pitfall_the_initial_commission_carries_its_floating_point_residue(
        kr_cancer_anchor):
    """commissions(0) is 323,999.9999999999 and not 324,000.00, because 0.6 × 12 is not 7.2.

    The notes print the model's value; a test written against a hand-cleaned 324,000.00 at
    ten decimals fails, and correctly so.  It is paid once, on the policy, at issue — not
    scaled by ``pols_if(0)`` — and the renewal commission starts at ``t = 12``.
    """
    a = kr_cancer_anchor
    assert a.commissions(0) == 0.6 * 12.0 * 45000.0
    assert a.commissions(0) != 324000.0
    assert a.commissions(0) == pytest.approx(323999.9999999999, abs=MONEY)
    assert round(a.commissions(0), 10) == 323999.9999999999
    assert all(a.commissions(t) == 0.0 for t in range(1, 12))
    assert a.commissions(12) == pytest.approx(0.03 * a.premiums(12), rel=1e-15)
    assert a.commissions(240) == 0.0                 # no premium, no renewal commission


def test_pitfall_proj_len_is_a_row_count_not_the_last_index(cancer, kr_cancer_anchor):
    """result_cf() has proj_len() rows, and the last of them is the expiry row.

    ``proj_len()`` is the frame's **exclusive end**, so the last projected month is
    ``proj_len() - 1``: indexing ``result_cf()`` at ``proj_len()`` is a ``KeyError`` and
    sweeping ``range(proj_len() + 1)`` runs a month past the end of the contract.  The frame
    is 0-based because ``t = 0`` is the month beginning at the 보험계약일, which is where the
    acquisition cost and the first premium both land; the 720 months of cover on the anchor
    cell are ``t = 0 ... 719`` and ``t = 720`` is the 100세 계약해당일 itself, the one row
    where every cash flow is zero and ``pols_maturity`` is not.
    """
    a = kr_cancer_anchor
    assert a.proj_len() == 721
    assert len(a.result_cf()) == 721 == a.proj_len()
    assert len(a.result_pols()) == 721
    assert a.result_cf().index[0] == 0 and a.result_cf().index[-1] == 720
    assert a.result_cf().index[-1] == a.proj_len() - 1
    with pytest.raises(KeyError):
        a.result_cf().loc[a.proj_len()]
    for point_id in cancer.Data.model_point_table().index:
        p = cancer.Projection[point_id]
        assert len(p.result_cf()) == p.proj_len()
        assert p.result_cf().index[0] == 0
        assert p.result_cf().index[-1] == p.proj_len() - 1


# ---------------------------------------------------------------------------
# Pitfall: interpolation, and the [std] tail of the incidence grid


def test_pitfall_incidence_interpolates_log_linearly_and_shares_linearly(cancer,
                                                                        kr_cancer_anchor):
    """Two conventions, and they must not be swapped.

    The incidence grid is published on ten-year ages and rises by a factor of 20.8 across
    the projection, so linear interpolation of it **overstates** the mid-decade rate
    materially; the tier shares are bounded ratios anchored at 20 / 40 / 60 / 80, and
    log-linear interpolation of a share that may exceed 1.0 is meaningless.  The
    ``provenance`` column of each CSV says which convention its rows are on.
    """
    a = kr_cancer_anchor
    linear = 0.001343 + 0.1 * (0.003567 - 0.001343)
    assert a.inc_rate(12) < linear
    assert a.inc_rate(12) == pytest.approx(
        0.001343 * (0.003567 / 0.001343) ** 0.1, rel=1e-14)
    # Halfway between two grid ages the log-linear rate is the geometric mean.
    assert a.inc_rate(60) == pytest.approx(
        math.sqrt(0.001343 * 0.003567), rel=1e-13)
    # The shares are the arithmetic midpoints, not the geometric ones.
    assert a.minor_share(240) == 0.34 and a.high_share(240) == 0.02
    assert a.minor_share(120) == pytest.approx((0.18 + 0.34) / 2.0, rel=1e-14)
    assert a.similar_share(120) == pytest.approx((0.53 + 0.15) / 2.0, rel=1e-14)
    inc = cancer.Data.incidence_table()
    assert (inc["provenance"].str.contains("log-linear")
            | inc["provenance"].str.contains("[R5]", regex=False)).all()
    shares = cancer.Data.tier_share_table()
    assert (shares["provenance"].str.contains(r"\[std\]")).all()


def test_pitfall_the_incidence_rows_above_age_eighty_are_std_and_reached(cancer,
                                                                        kr_cancer_anchor):
    """The published grid stops at 80; the anchor cell projects to 만나이 100.

    The 90 and 100 rows are the age-80 rate × 1.15, flat, and they carry **22.6%** of the
    anchor cell's diagnosis benefit.  A model that stopped at the published endpoint would
    be extrapolating implicitly instead of explicitly, which is the difference the
    ``provenance`` column exists to record.
    """
    inc = cancer.Data.incidence_table()
    for sex in ("M", "F"):
        base = float(inc.loc[(sex, 80), "inc_rate"])
        assert float(inc.loc[(sex, 90), "inc_rate"]) == pytest.approx(
            base * 1.15, abs=5e-7)
        assert float(inc.loc[(sex, 100), "inc_rate"]) == float(
            inc.loc[(sex, 90), "inc_rate"])
        assert "[std]" in str(inc.loc[(sex, 90), "provenance"])
        assert "[R5]" in str(inc.loc[(sex, 40), "provenance"])
    a = kr_cancer_anchor
    assert a.age(720) == 100 and a.inc_rate(720) == float(inc.loc[("M", 100), "inc_rate"])
    df = a.result_cf()
    diag = ["claims_diag_gen", "claims_diag_high", "claims_diag_minor",
            "claims_diag_similar"]
    share = df.loc[480:, diag].sum().sum() / df[diag].sum().sum()
    assert round(100.0 * share, 1) == 22.6
    # And the rate really does rise by a factor of 20.8 across the projection.
    assert a.inc_rate(480) / a.inc_rate(0) == pytest.approx(20.8, abs=0.05)


# ---------------------------------------------------------------------------
# Pitfall: what this chassis is not


def test_pitfall_reinstatement_is_not_a_negative_lapse(cancer):
    """부활 re-runs the 90 days, so lapse is absorbing here and that is conservative.

    A reinstated Korean cancer policy has 90 days of no invasive cover in front of it [S1]
    [S3] [S7], so it is not the policy that lapsed.  Modelling reinstatement as a negative
    lapse restores cover the contract does not restore and deletes a real anti-selection
    control; the machinery is therefore absent rather than switched off.
    """
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    for absent in ("pols_reinstate", "reinstate_rate", "reinstate_rate_eff",
                   "reinstate_window", "pols_lapse_pool", "pols_lapse_expire",
                   "reinstatement", "check_lapse_pool"):
        assert absent not in names, f"{absent} would restore cover the 약관 does not"
    assert not [n for n in names if "reinstat" in n or "buhwal" in n]
    p = cancer.Projection[1]
    for t in range(0, 200):
        assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15


def test_pitfall_this_is_not_the_indemnity_chassis(cancer):
    """No 급여/비급여 split, no 자기부담금, no annual limit, no 재가입 — that is Medical_KR_S.

    No benefit here is a reimbursement of a cost, and the one shared mechanic is the 제3보험
    requirement to pay the 계약자적립액 on death [REG-R17].  The names are asserted absent
    because borrowing the indemnity machinery would silently turn a 정액 contract into a
    reimbursement one.
    """
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    for absent in ("np_share", "annual_limit", "oop_ceiling", "oop_incurred_ge",
                   "visit_cap", "claims_ge_pp", "claims_np_pp", "reld_surcharge",
                   "nhi_covered", "self_pay", "coinsurance", "deductible"):
        assert absent not in names, f"{absent} belongs to Medical_KR_S"
    assert not [n for n in names if "deduct" in n or "copay" in n or "coins" in n]
    assert not [n for n in names if "reentry" in n or "jaegaip" in n]
    # Every benefit is a stated amount times a count, never a cost times a share.
    p = cancer.Projection[1]
    assert p.claims(12, "DIAG_GEN") == pytest.approx(
        p.benefit_ratio("general") * p.sum_assured() * p.reduction_factor(12)
        * p.diag_gen(12), rel=1e-15)


# ---------------------------------------------------------------------------
# The modules, in both positions of their switches


def test_the_diagnosis_module_gates_the_claims_and_not_the_transitions(cancer):
    """Model point 8 is the treatment-cost-only shape of [S5]: no diagnosis lump sum at all.

    The state transitions, the premium waiver and the excess mortality still run, because
    the contract has no diagnosis benefit — not no cancer.  So the switch removes four
    benefit lines and nothing else, and ``diag_similar`` goes with them only because the
    유사암 tier has no other consequence.
    """
    p = cancer.Projection[8]
    assert p.diag_module() == 0
    assert (p.hosp_module(), p.surg_module(), p.treat_module()) == (1, 1, 1)
    df = p.result_cf()
    for column in ("claims_diag_gen", "claims_diag_high", "claims_diag_minor",
                   "claims_diag_similar"):
        assert (df[column] == 0.0).all(), column
    assert df["claims_hosp"].sum() > 0.0 and df["claims_treat"].sum() > 0.0
    # The transitions are untouched: lives still move and the premium is still waived.
    assert p.diag_gen(12) > 0.0 and p.diag_minor(12) > 0.0
    assert p.pols_waived(60) > 0.0 and p.pols_minor(60) > 0.0
    assert p.pols_payer(60) < p.pols_if(60)
    # The 유사암 ledger stands still, because nothing is paid off it.
    assert p.diag_similar(12) == 0.0 and p.similar_avail(720) == 1.0
    assert p.check_similar_ledger() is True


def test_the_three_event_modules_are_off_together_on_the_diagnosis_only_point(cancer):
    """Model point 7 is the diagnosis-only shape [S3] [S6] [S7]: a lump sum and nothing else.

    The three care columns are identically zero and the diagnosis lines are not, which is
    the mirror image of model point 8 and the reason both are shipped.
    """
    p = cancer.Projection[7]
    assert (p.hosp_module(), p.surg_module(), p.treat_module()) == (0, 0, 0)
    assert p.diag_module() == 1
    df = p.result_cf()
    for column in ("claims_hosp", "claims_surgery", "claims_treat"):
        assert (df[column] == 0.0).all(), column
    assert df["claims_diag_gen"].sum() > 0.0
    assert df["claims_diag_similar"].sum() > 0.0
    # The diagnosed states still exist, because the waiver and the mortality still run.
    assert p.pols_waived(120) > 0.0
    assert p.check_hosp_cap() is True


def test_the_renewal_repricing_is_off_and_steps_the_premium_when_switched_on():
    """renew_reprice_rate = 0 holds the issue rate flat and records the boundary tension.

    A Korean renewal recomputes the premium at the attained age on the basis then in force
    [S4 제2-11조의6], which on the ordinary reading closes the K-IFRS 1117 contract boundary
    at each renewal [REG-R60].  The base run projects through it and does not resolve it;
    the switch is what makes the choice visible rather than implicit, and it moves nothing
    on a 비갱신형 point.
    """
    model = _reread("reprice")
    try:
        base = model.Projection[3]
        assert base.chassis() == "gaengsin"
        assert all(base.premium_factor(t) == 1.0 for t in (0, 120, 240, 719))
        model.Projection.renew_reprice_rate = 0.5
        model.Projection.clear_all()
        p3 = model.Projection[3]
        assert p3.premium_factor(0) == 1.0 and p3.premium_factor(119) == 1.0
        assert p3.premium_factor(120) == pytest.approx(1.5, rel=1e-15)
        assert p3.premium_factor(240) == pytest.approx(2.25, rel=1e-15)
        assert p3.premiums(120) > p3.premiums(119)
        # A 비갱신형 point is untouched: the flag is a chassis property, not a rate.
        p1 = model.Projection[1]
        assert p1.chassis() == "bi_gaengsin"
        assert all(p1.premium_factor(t) == 1.0 for t in (0, 120, 240))
    finally:
        model.close()


def test_the_best_estimate_incidence_factor_is_the_identity_and_scales_when_moved():
    """inc_be_factor = 1.0, because the loading inside a 참조순보험요율 is [unverified].

    The shipped rate is a **net premium rate with a safety loading already inside it**
    [REG-R4], not a best estimate, and it carries no trend allowance at all while Korea's
    crude incidence has risen 161% since 1999 [R1].  Two errors of opposite sign, neither
    quantified, so the factor stays at the identity rather than resting the model on an
    unconfirmed number.
    """
    model = _reread("incbe")
    try:
        assert model.Projection[1].inc_rate(0) == 0.001343
        model.Projection.inc_be_factor = 0.9
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.inc_rate(0) == pytest.approx(0.9 * 0.001343, rel=1e-15)
        assert p.inc_rate(12) == pytest.approx(0.9 * 0.0014808079, abs=5e-11)
        assert p.check_tier_shares() is True         # the algebra is scale-free
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_the_two_published_frames_and_the_sign_they_carry(cancer, kr_cancer_anchor):
    """result_cf is income-positive and result_pols makes the state movement legible.

    The notes write "+ = inflow", which is already the library-wide convention, so there is
    no outgo-positive ``liability_cf`` companion here: one stream, one sign, one name.
    ``result_pols`` is the second frame because the decrements, the diagnosis flows and both
    surrender values are unreadable next to a cash-flow statement.
    """
    assert "liability_cf" not in cancer.Projection.cells
    a = kr_cancer_anchor
    assert a.net_cf(0) < 0.0                          # the acquisition month
    assert a.net_cf(1) > 0.0                          # a positive-margin month
    assert a.net_cf(240) < 0.0                        # after 납입완료
    pols = a.result_pols()
    assert pols.index.name == "t" and list(pols.columns)[0] == "pols_if"
    for column in ("pols_healthy", "pols_minor", "pols_waived", "pols_death",
                   "pols_lapse", "pols_maturity", "diag_gen", "diag_high", "diag_minor",
                   "diag_similar", "similar_avail", "inc_rate", "mort_rate",
                   "lapse_rate", "av_pp", "cv_pp", "cv_std_pp", "surr_chg_pp"):
        assert column in pols.columns, column
    assert pols.notna().all().all()
    assert pols.loc[240, "cv_pp"] == pytest.approx(4078536.787114, abs=SIX)
    assert pols.loc[239, "cv_pp"] == 0.0


def test_cells_names_follow_basicterm_s(cancer):
    """Names shared with lifelib's basiclife/BasicTerm_S must not drift apart."""
    shared = {
        "model_point", "sex", "issue_age", "sum_assured", "proj_len", "age",
        "pols_if", "pols_if_init", "pols_if_at", "pols_death", "pols_lapse",
        "pols_maturity", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "premiums", "claims", "expenses", "claim_expenses", "inflation_factor",
        "commissions", "net_cf", "result_cf", "premium_mth_pp", "av_pp", "cv_pp",
        "expense_acq", "expense_maint", "inflation_rate", "roll_fwd_tol",
    }
    names = set(cancer.Projection.cells) | set(cancer.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    assert all(n.islower() or "_" in n for n in cancer.Projection.cells)


def test_the_docstrings_carry_this_products_own_reference_material(cancer):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = cancer.doc
    assert "mechanics demonstration" in doc
    assert "external" in doc and "once per model" in doc
    assert "fixed-benefit 제3보험 chassis" in doc
    assert "two start dates" in doc
    proj = cancer.Projection.doc
    assert "Notes symbol" in proj
    assert "만나이" in proj and "보험나이" in proj
    for cells in ("proj_len", "model_point", "pols_healthy", "pols_minor", "pols_waived",
                  "cover_similar", "reduction_factor", "similar_avail", "treat_avail",
                  "excess_hazard", "av_pp", "cv_pp"):
        assert cells in proj, cells
    data = cancer.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "incidence_table", "survival_table",
                  "care_table", "tier_table", "tier_share_table", "lapse_table",
                  "mort_table"):
        assert cells in data, cells


def test_inputs_live_beside_the_model_and_carry_their_provenance(cancer):
    """Eight external CSVs in the model folder's parent, seven of them source-tagged.

    ``model_point_table.csv`` is the one file exempt from the ``provenance`` column, because
    a model point is a *configuration* — one policy's own terms — rather than an assumption.
    The other seven sit at three different levels of authority and the column is where a
    reader is told which: ``incidence_table.csv`` is published data reproduced verbatim,
    ``mort_table.csv`` is a [std] construction, and ``care_table.csv`` says on every row
    that nothing anchors it.
    """
    expected = {"model_point_table.csv", "mort_table.csv", "incidence_table.csv",
                "tier_share_table.csv", "tier_table.csv", "survival_table.csv",
                "care_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in CSV_DIR.iterdir() if p.suffix == ".csv"}
    for csv in CSV_DIR.glob("*.csv"):
        assert csv.open("rb").read(3) != b"\xef\xbb\xbf", f"{csv.name} carries a BOM"
        csv.read_text(encoding="utf-8")
    for name in sorted(expected - {"model_point_table.csv"}):
        table = pd.read_csv(CSV_DIR / name)
        assert "provenance" in table.columns, name
        assert table["provenance"].notna().all(), name
        assert (table["provenance"].str.len() > 0).all(), name
    assert "provenance" not in pd.read_csv(CSV_DIR / "model_point_table.csv").columns
    mort = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert (mort["provenance"].str.contains(r"\[std\]")).all()
    care = pd.read_csv(CSV_DIR / "care_table.csv")
    assert (care["provenance"].str.contains(r"\[std\]")).all()
    inc = pd.read_csv(CSV_DIR / "incidence_table.csv")
    sourced = inc[inc["age"] <= 80]
    assert (sourced["provenance"].str.contains("[REG-R61]", regex=False)).all()


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a user with a company
    incidence basis does: it drops in as a same-schema CSV, no formula change.
    """
    doubled = pd.read_csv(CSV_DIR / "incidence_table.csv", index_col=["sex", "age"])
    doubled["inc_rate"] = doubled["inc_rate"] * 2.0

    model = _reread("swap")
    try:
        alt = "incidence_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt)
        try:
            base = float(model.Projection[1].claims(3, "DIAG_MINOR"))
            model.Data.incidence_table_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].claims(3, "DIAG_MINOR") == pytest.approx(
                2.0 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_model_point_table_exercises_the_product(cancer):
    """Both sexes, both chassis, both surrender forms, both waiver designs, every module.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows: the three observed 감액기간 designs, the
    three observed 유사암 ratios, the issue-age envelope from 15 to 65 and the sum-insured
    envelope from ₩10,000,000 to ₩100,000,000.
    """
    table = cancer.Data.model_point_table()
    assert len(table) == 10 and list(table.index) == list(range(1, 11))
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["chassis"]) == {"bi_gaengsin", "gaengsin"}
    assert set(table["cv_form"]) == {"mijigeup", "pyojun"}
    assert set(table["waiver_trigger"]) == {"cancer_diag", "none"}
    assert set(table["reduction_months"]) == {0, 12, 24}
    assert set(table["wait_months"]) == {0, 3}
    assert 0.20 in set(table["similar_ratio"]) and 0.70 in set(table["similar_ratio"])
    for module in ("hosp_module", "surg_module", "treat_module", "diag_module"):
        assert set(table[module]) == {0, 1}, f"{module} is not exercised both ways"
    assert table["issue_age"].min() == 15 and table["issue_age"].max() == 65
    assert table["sum_assured"].min() == 10000000
    assert table["sum_assured"].max() == 100000000
    assert set(table["pay_term_y"] > 0) == {True, False}   # 전기납 and a stated 납입기간
    assert (table["expiry_age"] == 100).all()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = _reread("rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in CSV_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Cancer_KR_S_rt")
    try:
        a = reread.Projection[1]
        assert a.proj_len() == 721 and a.surr_chg_cap_pp() == 585000.0
        for t in (0, 3, 4, 12):
            assert a.pols_if(t) == pytest.approx(WE_POLS[t][0], abs=INFORCE)
            assert a.net_cf(t) == pytest.approx(WE_TAIL[t][3], abs=MONEY)
        assert a.claims(0, "DIAG_SIMILAR") == pytest.approx(177.9475000000, abs=MONEY)
        assert "Notes symbol" in reread.Projection.doc
        assert a.check_waiting_period() is True
    finally:
        reread.close()

    src_files = {p.name for p in MODEL_DIR.rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts}
    dest_files = {p.name for p in dest.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts}
    assert dest_files == src_files
