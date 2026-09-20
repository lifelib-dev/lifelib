"""Golden and structural tests for Medical_KR_S.

The golden values are the worked example in
products/indemnity_medical/technical-notes.md ("Worked example"), which projects the
anchor cell M40 / 4세대 실손의료보험 / all five 보장종목 held / ₩50,000,000 a policy year
per 보장종목 / ₩200,000 a 통원 / ₩11,982 a month — the cell Korean supervisory disclosure
is quoted on, being the 기준연령 요건 of 감독규정 제1-2조제2호, and the cell the joint
FSC/FSS launch release prints a 10-carrier 손해보험 average premium for.  They are
hard-coded here rather than pickled so that a reviewer can compare them against the notes
by eye.

Tolerances follow the precision the notes display: money to ₩0.0001, in-force and the exit
split to the ten decimals the notes print them at, band shares and loss ratios to six.

**This product is the repository's only indemnity contract**, and the tests are shaped by
that.  There is no 보험가입금액 that determines a claim, only an annual limit that caps one,
so the assertions run down the reimbursement machinery in the order the notes fix — the
본인부담상한제 as an exclusion from covered loss, then the co-payment and the kinked
deductible taken over the severity *distribution*, then the ₩2,000,000 inpatient cap on the
retention that survives the ceiling, then the 3대비급여 sub-limits with their shared
counters and their injection carve-out, then the four ₩50,000,000 aggregates.  Each step is
asserted where it bites and, where it does not bite on a shipped cell, asserted to be wired
anyway: ``check_annual_limits()`` returning True says the limits are *wired*, not that they
are *exercised*, and the tests say which.

The 비급여 할인·할증 loop — the feedback from this year's non-covered claim to next year's
rider premium — is asserted as a loop and not as a table of numbers: the band mix is
recomputed from the claim-shape distribution against fixed money thresholds every year, the
band-1 discount is **solved** from revenue neutrality rather than read off a constant, and
the migration into the surcharge bands as the claim level trends is what makes the [std] 5%
discount cap bind from policy year 5.  ``result_prem()`` is the frame that carries it and
its ten rows are asserted one by one.

Beyond the worked example this module asserts every product fact the notes list under
"Known modeling pitfalls", because each of them is a way an implementation can look right
and be wrong.  There is one ``test_pitfall_*`` per bullet, naming the pitfall in its
docstring: a rate multiplied by the annual limit; a deductible applied to a mean instead of
to a distribution; the public ceiling applied to the finished benefit instead of to the
covered loss; the ₩2,000,000 cap taken in the wrong order against that ceiling; a renewal
corridor measured against the un-aged prior premium; a relativity applied to the whole
office premium instead of to the rider; a band-1 discount hard-coded at the wording's 95%
instead of solved; a 무사고 할인 given on one clean year instead of two; a band state
accumulated into a no-claims ladder the wording explicitly removes; an injection carve-out
counted twice; a utilisation table frozen at the issue age; an annual lapse rate used on a
monthly grid; a renewal decline folded into lapse; 3대비급여 limbs pushed through the annual
aggregate they replace; a rating exemption taken out of the benefit instead of out of the
rating count; a 상급병실료 cap applied per night instead of to the daily average; a slack
limit deleted; a ``claims`` subtotal column beside the splits; a claim-driven expense folded
into the premium-driven one; an acquisition strain invented on a contract that has none; the
two Korean age conventions silently collapsed; and a first-year premium re-read in every
later year, which throws the whole renewal machinery away.

The ten ``check_*`` cells are asserted **by name**, because a generic sweep cannot notice a
check that has quietly disappeared, and the [std] scalar assumptions are read off the model
so that a silent change to an assumption fails a test rather than moving a result.  The
whole-table sweep belongs to ``test_model_conventions_kr.py``; the model points taken here
are the ones that exercise a particular mechanic — 5 for the 급여-only election, 6 for
3대비급여형 not held, 7 for the lower 보험가입금액 rung where the per-visit cap actually
binds, 8 for the top-decile user on the lowest 본인부담상한액 where the public truncation is
the one limit that binds anywhere in the shipped table, 9 for 개인실손 중지, and 10 for the
40% non-NHI branch under a cost-trend stress that makes the ±25% corridor clip.
"""
import pathlib

import modelx as mx
import pandas as pd
import pytest

from kr_registry import LIB, MODELS

WON = 5e-5           # cash displayed to 0.0001 won
INFORCE = 5e-11      # in-force and exit counts, displayed to 10 d.p.
SHARE = 5e-7         # band shares and loss ratios, displayed to 6 d.p.
RELD = 5e-11         # the relativities, displayed to 10 d.p.

MODEL_DIR = LIB / MODELS["Medical_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "The cash flow statement, policy year 1" and "The rows where the product does something",
# merged.  t -> (pols_if, premiums, claims_ge_in, claims_ge_out, claims_np_in,
# claims_np_out, claims_np_three, expenses, claim_expenses, commissions, net_cf).
WORKED_EXAMPLE_CF = {
    0:   (1.0000000000, 11982.0000, 1116.1173, 3556.9008, 1574.4890, 1717.4122,
          1956.2861,  838.7400, 297.6362,  718.9200,   205.4984),
    1:   (0.9911492689, 11875.9505, 1106.2389, 3525.4196, 1560.5536, 1702.2119,
          1938.9715,  831.3165, 295.0019,  712.5570,   203.6796),
    2:   (0.9823768732, 11770.8397, 1096.4479, 3494.2171, 1546.7416, 1687.1460,
          1921.8102,  823.9588, 292.3909,  706.2504,   201.8769),
    3:   (0.9736821197, 11666.6592, 1086.7435, 3463.2907, 1533.0518, 1672.2136,
          1904.8008,  816.6661, 289.8030,  699.9995,   200.0901),
    4:   (0.9650643210, 11563.4007, 1077.1250, 3432.6380, 1519.4832, 1657.4133,
          1887.9419,  809.4380, 287.2380,  693.8040,   198.3192),
    5:   (0.9565227962, 11461.0561, 1067.5917, 3402.2567, 1506.0346, 1642.7439,
          1871.2322,  802.2739, 284.6958,  687.6634,   196.5639),
    6:   (0.9480568701, 11359.6174, 1058.1427, 3372.1442, 1492.7051, 1628.2044,
          1854.6705,  795.1732, 282.1760,  681.5770,   194.8242),
    7:   (0.9396658737, 11259.0765, 1048.7774, 3342.2983, 1479.4936, 1613.7936,
          1838.2553,  788.1354, 279.6785,  675.5446,   193.0998),
    8:   (0.9313491437, 11159.4254, 1039.4949, 3312.7165, 1466.3990, 1599.5104,
          1821.9854,  781.1598, 277.2032,  669.5655,   191.3908),
    9:   (0.9231060229, 11060.6564, 1030.2946, 3283.3965, 1453.4203, 1585.3536,
          1805.8595,  774.2459, 274.7497,  663.6394,   189.6968),
    10:  (0.9149358597, 10962.7615, 1021.1758, 3254.3361, 1440.5564, 1571.3220,
          1789.8763,  767.3933, 272.3180,  657.7657,   188.0179),
    11:  (0.9068380084, 10865.7330, 1012.1376, 3225.5328, 1427.8065, 1557.4147,
          1774.0346,  760.6013, 269.9078,  651.9440,   186.3538),
    12:  (0.8898237107, 11671.5892, 1003.0791, 3196.9486, 1514.5001, 1644.1587,
          1891.8205,  817.0112, 277.5152,  700.2954,   626.2604),
    24:  (0.8269420725, 11255.2428,  941.5160, 3001.0022, 1521.4795, 1636.8789,
          1909.8972,  787.8670, 270.3232,  675.3146,   510.9643),
    36:  (0.7807303037, 11657.8250,  897.7905, 2861.8800, 1551.7139, 1652.4968,
          1957.3942,  816.0477, 267.6383,  699.4695,   953.3941),
    47:  (0.7546309860, 11268.1113,  867.7779, 2766.2092, 1499.8410, 1597.2548,
          1891.9597,  788.7678, 258.6913,  676.0867,   921.5228),
    48:  (0.7447790095, 12234.0846,  865.0133, 2757.6339, 1592.1640, 1686.8368,
          2022.0773,  856.3859, 267.7118,  734.0451,  1452.2165),
    59:  (0.7232591474, 11880.5894,  840.0193, 2677.9540, 1546.1596, 1638.0969,
          1963.6508,  831.6413, 259.9764,  712.8354,  1410.2557),
    60:  (0.7141205641, 12896.5596, 1047.0651, 3151.5278, 2064.9814, 2052.2614,
          2600.0030,  902.7592, 327.4752,  773.7936,   -23.3071),
    72:  (0.6874997399, 13729.9031, 1018.1132, 3064.6451, 2138.8820, 2113.3143,
          2709.8504,  961.0932, 331.3441,  823.7942,   568.8666),
    118: (0.6087150719, 16301.6322,  928.7562, 2796.3637, 2363.0410, 2142.5505,
          3033.2096, 1141.1143, 337.9176,  978.0979,  2580.5814),
    119: (0.6075906434, 16271.5195,  927.0406, 2791.1982, 2358.6760, 2138.5928,
          3027.6066, 1139.0064, 337.2934,  976.2912,  2575.8145),
}

# "Every assumption value the anchor cell uses" — the two utilisation rows the anchor reads,
# (M, 40) in policy years 1-5 and (M, 45) in years 6-10, and the ratio between them.
UTILISATION = {
    40: (0.014140, 7.500000, 1.885433, 0.236694, 0.092047, 0.078898, 0.015780),
    45: (0.017674, 8.250000, 2.224811, 0.279298, 0.112298, 0.096255, 0.020198),
}
UTILISATION_RATIO = (1.2499293, 1.100000, 1.1800000, 1.1799961,
                     1.2200072, 1.2199929, 1.2799747)

# The eight severity streams: (cost, probability) points, the mean, and the expected
# payment per event at trend 1.0 — which is what policy year 1 uses.  The right-hand
# figure is not any simple function of the mean, and that is the point of the table.
SEVERITY = {
    "ge_in":   ([(250000, .40), (700000, .32), (1800000, .20), (5000000, .07),
                 (15000000, .01)], 1184000.0, 947200.0),
    "ge_out":  ([(8000, .30), (18000, .30), (40000, .25), (90000, .12),
                 (250000, .03)], 36100.0, 22638.20),
    "np_in":   ([(400000, .40), (1200000, .33), (3000000, .20), (8000000, .07)],
                1716000.0, 1201200.0),
    "np_room": ([(0, .55), (300000, .30), (1200000, .15)], 270000.0, 135000.0),
    "np_out":  ([(45000, .35), (90000, .30), (180000, .22), (400000, .10),
                 (900000, .03)], 149350.0, 76970.0),
    "physio":  ([(80000, .35), (120000, .35), (180000, .22), (400000, .08)],
                141600.0, 97020.0),
    "inject":  ([(60000, .40), (120000, .30), (250000, .20), (700000, .10)],
                180000.0, 121200.0),
    "mri":     ([(450000, .45), (700000, .35), (1100000, .20)], 667500.0, 467250.0),
}
GE_OUT_CLINIC = 24540.0        # the ₩10,000-tier expected payment per visit
GE_OUT_HOSPITAL = 19400.0      # the ₩20,000-tier expected payment per visit

# "Claim shape" — bucket -> (claim_amount, share, shape_rel, amount at C(1), band at the
# year-2 renewal).  The amounts are read as multiples of the table's own mean and rescaled.
CLAIM_SHAPE = {
    0: (0,       0.729012,  0.0000000000,        0.00, 1),
    1: (2184,    0.011039,  0.0407989477,     2184.03, 2),
    2: (6551,    0.017901,  0.1223781623,     6551.09, 2),
    3: (15285,   0.048628,  0.2855365915,    15285.21, 2),
    4: (32753,   0.052805,  0.6118534499,    32753.44, 2),
    5: (65506,   0.056385,  1.2237068998,    65506.88, 2),
    6: (152847,  0.066230,  2.8553098725,   152849.05, 2),
    7: (1200000, 0.008000, 22.4170042396,  1200016.10, 3),
    8: (2000000, 0.007000, 37.3616737326,  2000026.83, 4),
    9: (4500000, 0.003000, 84.0637658985,  4500060.37, 5),
}
SHAPE_MEAN = 53530.7923920000

# The decrement basis the notes print for the anchor cell.
MORT_Q = {40: 0.00132019, 41: 0.00136205, 44: 0.00152503,
          45: 0.00159477, 49: 0.00198242}
LAPSE_W = {1: 0.100, 2: 0.060, 3: 0.045, 4: 0.035, 5: 0.030,
           6: 0.026, 7: 0.024, 8: 0.022, 9: 0.021, 10: 0.020}
MORT_MTH_0 = 0.0001100825
LAPSE_MTH_0 = 0.0087416110
LAPSE_MTH_12 = 0.0051430128

# "The renewal and experience-rating ledger" — result_prem(), one row a policy year.
# y -> (claims_np_rated_pp, band_1..band_5, reld_surcharge, reld_solved, reld_one,
#       reld_avg, noclaim_share, prem_ge_base, prem_np_base, prem_gross_mth).
LEDGER = {
    1:  (53531.5106, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000,
         1.0000000000, 1.0000000000, 1.0000000000, 0.0000000000,
         4792.8000, 7189.2000, 11982.0000),
    2:  (57893.3650, 0.729012, 0.252988, 0.008000, 0.007000, 0.003000, 0.301988,
         0.9574766945, 0.9574766945, 1.0000000000, 0.0000000000,
         5034.3571, 8082.3862, 13116.7433),
    3:  (62514.9072, 0.729012, 0.252988, 0.008000, 0.007000, 0.003000, 0.301988,
         0.9574766945, 0.9574766945, 1.0000000000, 0.5314584961,
         5288.0887, 9086.5419, 13610.6786),
    4:  (67434.7704, 0.729012, 0.252988, 0.008000, 0.007000, 0.003000, 0.301988,
         0.9574766945, 0.9574766945, 1.0000000000, 0.5314584961,
         5554.6084, 10215.4538, 14931.9489),
    5:  (72600.0553, 0.729012, 0.252988, 0.000000, 0.015000, 0.003000, 0.309988,
         0.9465029382, 0.9500000000, 1.0025494000, 0.5314584961,
         5834.5607, 11484.6218, 16426.4626),
    6:  (95944.4532, 0.729012, 0.252988, 0.000000, 0.015000, 0.003000, 0.309988,
         0.9465029382, 0.9500000000, 1.0025494000, 0.5314584961,
         6128.6225, 12911.4712, 18059.3589),
    7:  (103291.4952, 0.729012, 0.252988, 0.000000, 0.008000, 0.010000, 0.316988,
         0.9369009015, 0.9500000000, 1.0095494000, 0.5314584961,
         6437.5051, 14515.5924, 19970.7757),
    8:  (110408.5397, 0.729012, 0.252988, 0.000000, 0.008000, 0.010000, 0.316988,
         0.9369009015, 0.9500000000, 1.0095494000, 0.5314584961,
         6761.9553, 16319.0096, 22001.8621),
    9:  (118056.8805, 0.729012, 0.252988, 0.000000, 0.008000, 0.010000, 0.316988,
         0.9369009015, 0.9500000000, 1.0095494000, 0.5314584961,
         7102.7579, 18346.4834, 24262.6066),
    10: (126324.7368, 0.729012, 0.252988, 0.000000, 0.008000, 0.010000, 0.316988,
         0.9369009015, 0.9500000000, 1.0095494000, 0.5314584961,
         7460.7369, 20625.8505, 26780.3985),
}

# "The annual per-policy claim quantities" — y -> (age, band, oop_incurred_ge, oop_trunc,
# claims_ge_in_pp, claims_ge_out_pp, claims_np_in_pp, claims_np_out_pp,
# claims_np_three_pp, claims_ann_pp, loss_incurred_pp, claims_np_rated_pp).
ANNUAL_CLAIMS = {
    1:  (40, 40,  84805.8913, 1.0,  13393.4080, 42682.8093, 18893.8680, 20608.9466,
         23475.4331, 119054.4651, 186006.8254,  53531.5106),
    2:  (41, 40,  85653.9502, 1.0,  13527.3421, 43113.4649, 20424.2713, 22172.8241,
         25512.7458, 124750.6482, 195052.1600,  57893.3650),
    3:  (42, 40,  86510.4897, 1.0,  13662.6155, 43548.4269, 22078.6373, 23753.2315,
         27715.0809, 130757.9921, 204769.9545,  62514.9072),
    4:  (43, 40,  87375.5946, 1.0,  13799.2417, 43987.7386, 23850.1902, 25399.2461,
         30085.5877, 137122.0043, 215214.0760,  67434.7704),
    5:  (44, 40,  88249.3506, 1.0,  13937.2341, 44431.4435, 25653.2049, 27178.5880,
         32580.0369, 143780.5073, 226442.7489,  72600.0553),
    6:  (45, 45, 106406.0369, 1.0,  17594.7625, 52957.9121, 34699.7101, 34485.9651,
         43690.1521, 183428.5019, 288743.9336,  95944.4532),
    7:  (46, 45, 107470.0973, 1.0,  17770.7101, 53492.0076, 37333.2268, 36886.9549,
         47299.2243, 192782.1238, 304577.3636, 103291.4952),
    8:  (47, 45, 108544.7983, 1.0,  17948.4172, 54031.4440, 40180.0584, 38542.0111,
         51170.3302, 201872.2610, 321617.7532, 110408.5397),
    9:  (48, 45, 109630.2463, 1.0,  18127.9014, 54576.2748, 43257.4834, 40317.8373,
         55315.1269, 211594.6238, 339962.1105, 118056.8805),
    10: (49, 45, 110726.5487, 1.0,  18309.1804, 55126.5540, 46584.1798, 42237.5054,
         59795.6522, 222053.0718, 359715.2940, 126324.7368),
}

# "Policy-year totals" — y -> (pols_if months, premiums, claims, expenses, claim_expenses,
# commissions, net_cf, loss ratio).
POLICY_YEAR_TOTALS = {
    1:  (11.432747, 136987.1764, 113426.6331,  9589.1024, 3402.7990,  8219.2306,
          2349.4114, 0.828009),
    2:  (10.374553, 136080.3438, 107852.6803,  9525.6241, 3235.5804,  8164.8206,
          7301.6384, 0.792566),
    3:  ( 9.710708, 132169.3262, 105812.7236,  9251.8528, 3174.3817,  7930.1596,
          6000.2085, 0.800585),
    4:  ( 9.211361, 137543.5718, 105256.6906,  9628.0500, 3157.7007,  8252.6143,
         11248.5162, 0.765261),
    5:  ( 8.807655, 144678.6216, 105530.7628, 10127.5035, 3165.9229,  8680.7173,
         17173.7150, 0.729415),
    6:  ( 8.460681, 152794.4700, 129327.4993, 10695.6129, 3879.8250,  9167.6682,
          -276.1354, 0.846415),
    7:  ( 8.152615, 162814.0368, 130973.1958, 11396.9826, 3929.1959,  9768.8422,
          6745.8204, 0.804434),
    8:  ( 7.871220, 173181.5075, 132415.0893, 12122.7055, 3972.4527, 10390.8905,
         14280.3696, 0.764603),
    9:  ( 7.610823, 184658.3987, 134200.7651, 12926.0879, 4026.0230, 11079.5039,
         22426.0188, 0.726751),
    10: ( 7.365760, 197257.9800, 136299.1308, 13808.0586, 4088.9739, 11835.4788,
         31226.3379, 0.690969),
}

# "Undiscounted totals over the 120 months".
TOTALS = {
    "pols_if": 88.998122,
    "premiums": 1558165.4328,
    "claims_ge_in": 115320.6688,
    "claims_ge_out": 357128.9114,
    "claims_np_in": 222875.2985,
    "claims_np_out": 223623.9771,
    "claims_np_three": 282146.3147,
    "expenses": 109071.5803,
    "claim_expenses": 36032.8551,
    "commissions": 93489.9260,
    "net_cf": 118475.9008,
}
TOTAL_CLAIMS = 1201095.1706
TOTAL_LOSS_RATIO = 0.770839
TOTAL_MARGIN = 0.076036

CHECKS = {
    "check_pols_roll_fwd", "check_net_cf", "check_claim_shape", "check_band_shares",
    "check_relativity_neutral", "check_renewal_corridor", "check_annual_limits",
    "check_indemnity", "check_oop_ceiling", "check_expense_split",
}
CHECKS_PER_T = {"check_pols_roll_fwd", "check_net_cf"}
CHECKS_PER_Y = {"check_band_shares", "check_relativity_neutral", "check_renewal_corridor",
                "check_annual_limits", "check_indemnity", "check_oop_ceiling"}
CHECKS_SCALAR = {"check_claim_shape", "check_expense_split"}

# The scalar References the notes tabulate under "Scalar References, in full".  The first
# group is **contractual** — every one of them a clause of the 표준약관 annexed to the
# 보험업감독업무시행세칙 at 별표 15, so on this product they are cited and not [std], which
# is a citation precision no other product in this repository reaches.
CONTRACTUAL_SCALARS = {
    "retain_rate_ge_base": 0.20, "retain_rate_np_base": 0.30,
    "retain_rate_nonhi": 0.60, "ded_clinic": 10000.0, "ded_hospital": 20000.0,
    "ded_np_out": 30000.0, "cap_inpatient_retain": 2000000.0, "room_rate": 0.50,
    "room_cap_day": 100000.0, "visit_limit_np": 100.0, "act_limit_three": 50.0,
    "physio_gate_acts": 10.0, "limit_physio": 3500000.0, "limit_inject": 2500000.0,
    "limit_mri": 3000000.0, "band_thr_3": 1000000.0, "band_thr_4": 1500000.0,
    "band_thr_5": 3000000.0, "reld_r2": 1.0, "reld_r3": 2.0, "reld_r4": 3.0,
    "reld_r5": 4.0, "renewal_corridor": 0.25, "noclaim_disc": 0.10,
    "reentry_period": 5, "max_cover_age": 100,
}

# The second group is the modeller's view, and every one of them is [std].
STD_SCALARS = {
    "reentry_cycles": 2, "renewal_decline_rate": 0.01, "physio_cont_prob": 0.60,
    "inject_carve_share": 0.25, "share_injury": 0.15, "med_trend_ge": 0.010,
    "med_trend_np": 0.081, "age_load": 0.04, "reld_disc_cap": 0.05,
    "reld_start_year": 4, "reld_exempt_share": 0.15, "comm_rate": 0.06,
    "expense_maint_rate": 0.07, "expense_claim_rate": 0.03,
    "expense_total_rate": 0.16,
}

BREAK_EVEN_LR = 0.87 / 1.03      # 0.8446601942, the two-term identity's own break-even


def _flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    These docstrings are hard-wrapped prose; searching the raw text for a sentence
    fragment would test where the wrap fell rather than what the docstring says.
    """
    return " ".join((doc or "").split())


def _reread(suffix):
    """A private copy of the model, for tests that move a Reference."""
    return mx.read_model(MODEL_DIR, name="Medical_KR_S_" + suffix)


class _swapped:
    """Context manager: a private model reading an alternative CSV for one table.

    The CSV has to live in ``input_dir()``, which is the model folder's parent, because
    that is where :func:`Data.input_dir` resolves to; it is written on entry and removed
    on exit so the directory is left exactly as it was found.  This is the mechanism the
    external-file layout buys and the one a user with a company basis would use.
    """

    def __init__(self, suffix, ref, frame, name, **to_csv):
        self.suffix, self.ref, self.frame, self.name, self.kw = \
            suffix, ref, frame, name, to_csv
        self.model = None
        self.path = None

    def __enter__(self):
        self.model = _reread(self.suffix)
        self.path = pathlib.Path(self.model.Data.input_dir()) / self.name
        self.frame.to_csv(self.path, **self.kw)
        setattr(self.model.Data, self.ref, self.name)
        self.model.clear_all()
        return self.model

    def __exit__(self, *exc):
        if self.model is not None:
            self.model.close()
        if self.path is not None:
            self.path.unlink(missing_ok=True)
        return False


# ---------------------------------------------------------------------------
# The worked example, cell by cell


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_worked_example_cash_flow_row(kr_medical_anchor, t):
    """Every cell of the notes' two cash flow tables, at the precision they display.

    Policy year 1 in full, then the eleven rows the notes single out as "where the product
    does something" — the renewal, the first 무사고 할인 year, the year the relativity goes
    live, the year the discount cap first binds, the 재가입 and the utilisation band step,
    and the horizon.  Nothing else in this suite would notice a limb quietly moving between
    columns, because ``check_net_cf`` only requires the row to add up.
    """
    (pols, prem, ge_in, ge_out, np_in, np_out, np_three,
     exp, cexp, comm, net) = WORKED_EXAMPLE_CF[t]
    a = kr_medical_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=WON)
    assert a.claims(t, "GE_IN") == pytest.approx(ge_in, abs=WON)
    assert a.claims(t, "GE_OUT") == pytest.approx(ge_out, abs=WON)
    assert a.claims(t, "NP_IN") == pytest.approx(np_in, abs=WON)
    assert a.claims(t, "NP_OUT") == pytest.approx(np_out, abs=WON)
    assert a.claims(t, "NP_THREE") == pytest.approx(np_three, abs=WON)
    assert a.expenses(t) == pytest.approx(exp, abs=WON)
    assert a.claim_expenses(t) == pytest.approx(cexp, abs=WON)
    assert a.commissions(t) == pytest.approx(comm, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_worked_example_row_is_the_published_frame(kr_medical_anchor, t):
    """The same row read out of ``result_cf()`` rather than off the cells.

    The frame is what a reader prints and what ``run.py`` shows, and it is built by a
    separate expression from the cells; a column that was wired to the wrong ``kind``
    would agree with itself and disagree here.
    """
    row = kr_medical_anchor.result_cf().loc[t]
    expected = WORKED_EXAMPLE_CF[t]
    columns = ("pols_if", "premiums", "claims_ge_in", "claims_ge_out", "claims_np_in",
               "claims_np_out", "claims_np_three", "expenses", "claim_expenses",
               "commissions", "net_cf")
    for column, value in zip(columns, expected):
        tol = INFORCE if column == "pols_if" else WON
        assert row[column] == pytest.approx(value, abs=tol), column


def test_worked_example_anchor_cell_attributes(kr_medical_anchor):
    """The anchor's own model point row, and the horizon it implies.

    ``proj_len() = 120`` is two five-year 보장내용 변경주기 — ten policy years, and the
    **number** of projected months, so the frame runs ``t = 0 … 119`` — and it is
    a **stated** horizon rather than a contractual one, which is the distinction the whole
    document turns on: at the fifth 계약해당일 the contract re-enters whatever generation
    the supervisor is then prescribing.
    """
    a = kr_medical_anchor
    assert a.sex() == "M" and a.issue_age() == 40
    assert a.premium_mth_pp() == 11982.0
    assert a.np_share() == 0.60
    assert a.np_rider() is True and a.three_np() is True
    assert a.annual_limit() == 50000000.0 and a.visit_cap() == 200000.0
    assert a.oop_decile() == 6 and a.clinic_share() == 0.63
    assert a.nhi_covered() is True
    assert a.trend_mult() == 1.0 and a.util_mult() == 1.0
    assert a.reld_on() is True and a.noclaim_on() is True
    assert a.suspend_rate() == 0.0
    assert a.proj_len() == 120
    assert len(a.result_cf()) == 120
    assert list(a.result_cf().index) == list(range(120))
    assert a.pols_if_init() == 1.0
    assert a.age(0) == 40 and a.age(119) == 49
    assert a.policy_year(0) == 1 and a.policy_year(59) == 5 and a.policy_year(119) == 10


def test_worked_example_utilisation_rows_and_the_five_year_step(kr_medical_anchor):
    """The two ``utilisation_table.csv`` rows the anchor reads, and the ratio between them.

    The anchor reads (M, 40) in policy years 1-5 and (M, 45) in years 6-10, because the
    table is banded in fives and the band is taken at the **attained** age.  The ratios are
    the size of the step the claim takes in one jump at ``t = 60`` while the premium takes
    its age effect smoothly at every renewal — which is what makes the loss ratio saw-tooth.
    """
    a = kr_medical_anchor
    getters = (a.adm_rate, a.los_days, a.visit_rate_ge, a.visit_rate_np,
               a.act_rate_physio, a.act_rate_inject, a.act_rate_mri)
    for y, band in ((1, 40), (5, 40), (6, 45), (10, 45)):
        assert a.util_band(y) == band
        for getter, value in zip(getters, UTILISATION[band]):
            assert getter(y) == pytest.approx(value, rel=1e-12), (y, getter.name)
    for getter, ratio in zip(getters, UTILISATION_RATIO):
        assert getter(6) / getter(5) == pytest.approx(ratio, abs=5e-8), getter.name


@pytest.mark.parametrize("stream", sorted(SEVERITY))
def test_worked_example_severity_points_and_expected_payment(kr_medical_anchor, stream):
    """Each severity stream's points, its mean, and the expected payment per event.

    The right-hand column of the notes' table is the one that earns the table's place: the
    deductible is ``max(flat floor, percentage x cost)``, so the payment is a kinked
    function of cost and the expectation has to be taken over the distribution.  On
    ``ge_out`` the payment is the two provider tiers blended at ``clinic_share``.
    """
    a = kr_medical_anchor
    points, mean, payment = SEVERITY[stream]
    assert a.sev_points(stream) == [(float(c), p) for c, p in points]
    assert a.sev_mean(stream) == pytest.approx(mean, rel=1e-12)
    if stream == "ge_in":
        got = mean * (1.0 - a.retain_rate_ge())
    elif stream == "ge_out":
        clinic = a.paid_out_per_visit("ge_out", 10000.0, 0.20, 1.0)
        hospital = a.paid_out_per_visit("ge_out", 20000.0, 0.20, 1.0)
        assert clinic == pytest.approx(GE_OUT_CLINIC, abs=WON)
        assert hospital == pytest.approx(GE_OUT_HOSPITAL, abs=WON)
        got = 0.63 * clinic + 0.37 * hospital
    elif stream == "np_in":
        got = mean * (1.0 - a.retain_rate_np())
    elif stream == "np_room":
        got = sum(p * min(0.50 * c, 100000.0 * a.los_days(1)) for c, p in points)
    elif stream == "np_out":
        got = a.paid_out_per_visit("np_out", 30000.0, 0.30, 1.0)
    else:
        got = a.paid_per_act(stream, 1.0)
    assert got == pytest.approx(payment, abs=WON)


@pytest.mark.parametrize("bucket", sorted(CLAIM_SHAPE))
def test_worked_example_claim_shape_bucket(kr_medical_anchor, bucket):
    """The claim-shape table, its rescaling, and the band each bucket lands in.

    The amounts are read as **multiples of the table's own mean** and rescaled to whatever
    claim level is being projected, which is what lets one shape serve every model point and
    every year.  The band at the year-2 renewal is what the rescaled amount falls into
    against the fixed money thresholds, and it is where the published commencement
    distribution 72.9 / 25.3 / 0.8 / 0.7 / 0.3 comes from.
    """
    a = kr_medical_anchor
    amount, share, rel, at_c1, band = CLAIM_SHAPE[bucket]
    table = a.data.claim_shape_table()
    assert float(table.loc[bucket, "claim_amount"]) == amount
    assert a.shape_share(bucket) == pytest.approx(share, rel=1e-12)
    assert a.shape_rel(bucket) == pytest.approx(rel, abs=5e-11)
    scaled = a.shape_rel(bucket) * a.claims_np_rated_pp(1)
    assert scaled == pytest.approx(at_c1, abs=5e-3)
    assert a.band_of(scaled) == band
    assert a.shape_mean() == pytest.approx(SHAPE_MEAN, abs=1e-9)


def test_worked_example_decrement_basis(kr_medical_anchor):
    """The mortality and lapse rates the notes print, annual and monthly.

    ``mort_rate`` is annual and ``mort_rate_mth`` monthly, and the same for lapse; the
    library spells them apart because using one where the other belongs is the commonest
    monthly-grid error there is.  The renewal decline acts only in the twelfth month of a
    policy year, and suspension is off on this cell.
    """
    a = kr_medical_anchor
    for age, q in MORT_Q.items():
        t = (age - 40) * 12
        assert a.age(t) == age
        assert a.mort_rate(t) == pytest.approx(q, rel=1e-12)
    assert a.mort_rate_mth(0) == pytest.approx(MORT_MTH_0, abs=5e-11)
    assert a.mort_rate_mth(0) == pytest.approx(
        1.0 - (1.0 - MORT_Q[40]) ** (1.0 / 12.0), rel=1e-14)
    for y, w in LAPSE_W.items():
        assert a.lapse_rate((y - 1) * 12) == pytest.approx(w, rel=1e-12)
    assert a.lapse_rate_mth(0) == pytest.approx(LAPSE_MTH_0, abs=5e-11)
    assert a.lapse_rate_mth(12) == pytest.approx(LAPSE_MTH_12, abs=5e-11)
    assert a.renewal_decline(11) == 0.01 and a.renewal_decline(119) == 0.01
    assert all(a.renewal_decline(t) == 0.0 for t in (0, 5, 10, 12, 58))
    assert all(a.suspend_rate_mth(t) == 0.0 for t in range(0, 120, 12))


def test_worked_example_the_public_ceiling_has_thirty_eight_fold_headroom(
        kr_medical_anchor):
    """``oop_ceiling()`` is decile 6's ₩3,260,000 and ``oop_trunc`` is 1.0 throughout.

    The 본인부담상한제 is the one limit in this product that binds anywhere in the shipped
    table, and it does not bind here: the anchor's incurred 급여 본인부담금 is ₩84,805.89
    against a ceiling of ₩3,260,000, headroom of a factor of 38.4.  Recording that the
    truncation is inert on the anchor is what makes model point 8, where it is not, worth
    having.
    """
    a = kr_medical_anchor
    assert a.oop_ceiling() == 3260000.0
    assert a.oop_incurred_ge(1) == pytest.approx(84805.8913, abs=WON)
    assert a.oop_ceiling() / a.oop_incurred_ge(1) == pytest.approx(38.44, abs=0.01)
    for y in range(1, 11):
        assert a.oop_trunc(y) == 1.0
    scale = a.data.oop_ceiling_table()
    assert [int(scale.loc[d, "ceiling"]) for d in range(1, 11)] == [
        900000, 1120000, 1120000, 1730000, 1730000, 3260000, 3260000,
        4460000, 5360000, 8430000]


@pytest.mark.parametrize("y", sorted(ANNUAL_CLAIMS))
def test_worked_example_annual_claim_row(kr_medical_anchor, y):
    """The per-policy annual claim table, limb by limb, with the incurred loss beside it.

    This is the layer the monthly statement is a presentation of: every contractual
    mechanism in this product runs on the policy year and resets on it, so the annual
    figures are the unit of account and the month is a grid.  ``loss_incurred_pp`` is
    carried alongside because it is what the indemnity ceiling bounds the claim by.
    """
    a = kr_medical_anchor
    (age, band, incurred, trunc, ge_in, ge_out, np_in, np_out,
     np_three, total, loss, rated) = ANNUAL_CLAIMS[y]
    assert a.age((y - 1) * 12) == age
    assert a.util_band(y) == band
    assert a.oop_incurred_ge(y) == pytest.approx(incurred, abs=WON)
    assert a.oop_trunc(y) == pytest.approx(trunc, abs=1e-10)
    assert a.claims_ge_in_pp(y) == pytest.approx(ge_in, abs=WON)
    assert a.claims_ge_out_pp(y) == pytest.approx(ge_out, abs=WON)
    assert a.claims_np_in_pp(y) == pytest.approx(np_in, abs=WON)
    assert a.claims_np_out_pp(y) == pytest.approx(np_out, abs=WON)
    assert a.claims_np_three_pp(y) == pytest.approx(np_three, abs=WON)
    assert a.claims_ann_pp(y) == pytest.approx(total, abs=WON)
    assert a.loss_incurred_pp(y) == pytest.approx(loss, abs=WON)
    assert a.claims_np_rated_pp(y) == pytest.approx(rated, abs=WON)


@pytest.mark.parametrize("y", sorted(LEDGER))
def test_worked_example_renewal_ledger_row(kr_medical_anchor, y):
    """``result_prem()``, the frame the product's story is actually in.

    One row a policy year, because that is the clock the whole mechanism runs on.  The band
    mix at ``y = 2`` is the published commencement distribution arriving as a *result* of
    the shape table's calibration; the surcharge pool and the solved band-1 relativity are
    the neutrality identity; ``reld_avg`` is 1.0 exactly until the [std] discount cap binds
    at ``y = 5``; and the two base premiums are the renewal recursion.
    """
    a = kr_medical_anchor
    (rated, b1, b2, b3, b4, b5, pool, solved, one, avg, nc,
     ge_base, np_base, gross) = LEDGER[y]
    assert a.claims_np_rated_pp(y) == pytest.approx(rated, abs=WON)
    for b, share in ((1, b1), (2, b2), (3, b3), (4, b4), (5, b5)):
        assert a.band_share(y, b) == pytest.approx(share, abs=SHARE), (y, b)
    assert a.reld_surcharge(y) == pytest.approx(pool, abs=SHARE)
    assert a.reld_solved(y) == pytest.approx(solved, abs=RELD)
    assert a.reld_one(y) == pytest.approx(one, abs=RELD)
    assert a.reld_avg(y) == pytest.approx(avg, abs=RELD)
    assert a.noclaim_share(y) == pytest.approx(nc, abs=RELD)
    assert a.prem_ge_base(y) == pytest.approx(ge_base, abs=WON)
    assert a.prem_np_base(y) == pytest.approx(np_base, abs=WON)
    assert a.prem_gross_mth(y) == pytest.approx(gross, abs=WON)
    row = a.result_prem().loc[y]
    assert row["prem_gross_mth"] == pytest.approx(gross, abs=WON)
    assert row["band_1"] == pytest.approx(b1, abs=SHARE)


@pytest.mark.parametrize("y", sorted(POLICY_YEAR_TOTALS))
def test_worked_example_policy_year_totals(kr_medical_anchor, y):
    """The ten policy-year subtotals and their loss ratios, summed off ``result_cf()``.

    The loss ratio is the whole shape of this product's result, because the ledger collapses
    to ``net_cf = 0.87 x premiums - 1.03 x claims``: the sign of a period is decided by one
    number against the model's own break-even of 0.844660.  Policy year 6 is the only
    negative year and it is the year the utilisation band steps.
    """
    df = kr_medical_anchor.result_cf().loc[(y - 1) * 12: y * 12 - 1]
    months, prem, claims, exp, cexp, comm, net, lr = POLICY_YEAR_TOTALS[y]
    claim_cols = [c for c in df.columns if c.startswith("claims_")]
    assert df["pols_if"].sum() == pytest.approx(months, abs=5e-7)
    assert df["premiums"].sum() == pytest.approx(prem, abs=WON)
    assert df[claim_cols].sum().sum() == pytest.approx(claims, abs=WON)
    assert df["expenses"].sum() == pytest.approx(exp, abs=WON)
    assert df["claim_expenses"].sum() == pytest.approx(cexp, abs=WON)
    assert df["commissions"].sum() == pytest.approx(comm, abs=WON)
    assert df["net_cf"].sum() == pytest.approx(net, abs=WON)
    assert df[claim_cols].sum().sum() / df["premiums"].sum() == pytest.approx(
        lr, abs=SHARE)
    assert (net < 0.0) == (lr > BREAK_EVEN_LR), "the sign is the loss ratio's"


def test_worked_example_undiscounted_totals(kr_medical_anchor):
    """The ten-year totals, the exposure, the loss ratio and the margin.

    ``pols_if`` sums to months of exposure — 88.998122 policy-months, 7.416510
    policy-years — and every money column is per policy issued, so the frame is a unit
    projection and scales linearly.
    """
    df = kr_medical_anchor.result_cf()
    for column, value in TOTALS.items():
        tol = 5e-6 if column == "pols_if" else WON
        assert df[column].sum() == pytest.approx(value, abs=tol), column
    claims = df[[c for c in df.columns if c.startswith("claims_")]].sum().sum()
    assert claims == pytest.approx(TOTAL_CLAIMS, abs=WON)
    assert df["pols_if"].sum() / 12.0 == pytest.approx(7.416510, abs=5e-7)
    assert claims / df["premiums"].sum() == pytest.approx(TOTAL_LOSS_RATIO, abs=SHARE)
    assert df["net_cf"].sum() / df["premiums"].sum() == pytest.approx(
        TOTAL_MARGIN, abs=SHARE)


def test_worked_example_calibration_closing(kr_medical_anchor):
    """Policy year 1 reproduces the published 4세대 2022 상반기 loss ratios.

    The frequency **level** is solved rather than assumed, against one published pair —
    급여 97.5% and 비급여 73.0% on the published ₩11,982 premium anchor, combined 82.8% —
    and this is the assertion that says the solve still closes.  Move a frequency, a
    severity point or the ₩11,982 and it fails here rather than drifting silently through
    every later number in the document.
    """
    a = kr_medical_anchor
    assert a.claims_ge_pp(1) / (a.prem_ge_base(1) * 12.0) == pytest.approx(
        0.9750080, abs=5e-8)
    assert a.claims_np_pp(1) / (a.prem_np_base(1) * 12.0) == pytest.approx(
        0.7300099, abs=5e-8)
    assert a.claims_ann_pp(1) / (a.prem_gross_mth(1) * 12.0) == pytest.approx(
        0.8280091, abs=5e-8)
    assert a.claims_ge_pp(1) == pytest.approx(56076.22, abs=0.005)
    assert a.claims_np_pp(1) == pytest.approx(62978.2477, abs=WON)


# ---------------------------------------------------------------------------
# The notes' hand traces, term by term


def test_hand_trace_t0_the_annual_claim_built_from_nothing(kr_medical_anchor):
    """The ``t = 0`` trace, step by step, in the order the reimbursement machinery runs.

    Step 1 the public ceiling as an exclusion from covered loss; steps 2 and 3 the
    co-payment, the kinked deductible and the ₩2,000,000 inpatient cap; step 4 the three
    named classes and the injection carve-out; step 5 the annual aggregates.  Every
    intermediate the notes print is asserted, because the whole product is the *order* of
    these five and a reader with a calculator has to be able to land on each one.
    """
    a = kr_medical_anchor
    # Step 0: the year's basis.
    assert a.trend_ge(1) == 1.0 and a.trend_np(1) == 1.0
    # Step 1: the public ceiling.
    assert a.adm_rate(1) * a.sev_mean("ge_in") == pytest.approx(16741.76, abs=WON)
    assert a.visit_rate_ge(1) * a.sev_mean("ge_out") == pytest.approx(
        68064.1313, abs=WON)
    assert a.oop_incurred_ge(1) == pytest.approx(84805.8913, abs=WON)
    assert a.oop_trunc(1) == 1.0
    # Steps 2 and 3: 급여 입원 — a flat percentage, with the cap slack.
    cost = a.adm_rate(1) * a.sev_mean("ge_in") * a.trend_ge(1) * a.oop_trunc(1)
    assert cost * a.retain_rate_ge() == pytest.approx(3348.3520, abs=WON)
    assert cost * a.retain_rate_ge() < 2000000.0            # no top-up
    assert a.claims_ge_in_pp(1) == pytest.approx(0.80 * cost, rel=1e-14)
    assert a.claims_ge_in_pp(1) == pytest.approx(13393.4080, abs=WON)
    # Steps 2 and 3: 급여 통원 — the kink, per tier, blended.
    clinic = a.paid_out_per_visit("ge_out", 10000.0, 0.20, 1.0)
    hospital = a.paid_out_per_visit("ge_out", 20000.0, 0.20, 1.0)
    assert clinic == pytest.approx(24540.0, abs=WON)
    assert hospital == pytest.approx(19400.0, abs=WON)
    blend = 0.63 * clinic + 0.37 * hospital
    assert blend == pytest.approx(22638.20, abs=WON)
    assert a.claims_ge_out_pp(1) == pytest.approx(1.885433 * blend, rel=1e-12)
    assert a.claims_ge_out_pp(1) == pytest.approx(42682.8093, abs=WON)
    # 비급여 입원: the base and the 상급병실료 daily-average cap.
    room = sum(p * min(0.50 * c, 100000.0 * a.los_days(1))
               for c, p in a.sev_points("np_room"))
    assert room == pytest.approx(135000.0, abs=WON)
    assert a.claims_np_in_pp(1) == pytest.approx(
        0.014140 * (1201200.0 + 135000.0), abs=WON)
    assert a.claims_np_in_pp(1) == pytest.approx(18893.8680, abs=WON)
    # 비급여 통원: the flat ₩30,000 floor, the ₩200,000 per-visit cap and the 100-visit cap.
    assert a.visits_np_eff(1) == pytest.approx(0.236694, rel=1e-12)
    per_visit = a.paid_out_per_visit("np_out", 30000.0, 0.30, 1.0)
    assert per_visit == pytest.approx(76970.0, abs=WON)
    assert 0.236694 * per_visit == pytest.approx(18218.3372, abs=WON)
    # Step 4: the three named classes and the carve-out.
    assert a.acts_physio_eff(1) == pytest.approx(0.092047, rel=1e-14)   # under the gate
    assert a.acts_inject_eff(1) == pytest.approx(0.75 * 0.078898, rel=1e-14)
    assert a.claims_physio_pp(1) == pytest.approx(8930.3999, abs=WON)
    assert a.claims_inject_pp(1) == pytest.approx(7171.8282, abs=WON)
    assert a.claims_mri_pp(1) == pytest.approx(7373.2050, abs=WON)
    carve = a.claims_np_out_pp(1) - 0.236694 * per_visit
    assert carve == pytest.approx(0.078898 * 0.25 * 121200.0, abs=WON)
    assert carve == pytest.approx(2390.6094, abs=WON)
    assert a.claims_np_out_pp(1) == pytest.approx(20608.9466, abs=WON)
    assert a.claims_np_three_pp(1) == pytest.approx(23475.4331, abs=WON)
    # Step 5: the annual aggregates, both slack.
    assert a.claims_ge_in_pp(1) + a.claims_ge_out_pp(1) == pytest.approx(
        56076.2173, abs=WON)
    assert a.claims_np_in_pp(1) + a.claims_np_out_pp(1) == pytest.approx(
        39502.8146, abs=WON)
    assert a.ge_limit_factor(1) == pytest.approx(1.0, abs=1e-12)
    assert a.np_limit_factor(1) == pytest.approx(1.0, abs=1e-12)
    assert a.claims_ann_pp(1) == pytest.approx(119054.4651, abs=WON)
    assert a.loss_incurred_pp(1) == pytest.approx(186006.8254, abs=WON)
    assert a.claims_ann_pp(1) / a.loss_incurred_pp(1) == pytest.approx(
        0.64005, abs=5e-6)
    # Month 0 itself, and the two-term cross-check.
    assert a.claims(0) == pytest.approx(119054.4651 / 12.0, abs=WON)
    assert a.claims(0) == pytest.approx(9921.2054, abs=WON)
    assert a.expenses(0) == pytest.approx(0.07 * 11982.0, rel=1e-14)
    assert a.claim_expenses(0) == pytest.approx(0.03 * a.claims(0), rel=1e-14)
    assert a.commissions(0) == pytest.approx(0.06 * 11982.0, rel=1e-14)
    assert a.net_cf(0) == pytest.approx(
        0.87 * a.premiums(0) - 1.03 * a.claims(0), abs=1e-9)
    assert a.net_cf(0) == pytest.approx(205.4984, abs=WON)
    # Decrements at the end of month 0: no renewal decline, (0+1) mod 12 != 0.
    assert a.pols_death(0) == pytest.approx(MORT_MTH_0, abs=INFORCE)
    assert a.pols_if_at(0, "BEF_LAPSE") == pytest.approx(0.9998899175, abs=INFORCE)
    assert a.pols_lapse(0) == pytest.approx(0.0087406487, abs=INFORCE)
    assert a.pols_renewal_decline(0) == 0.0
    assert a.pols_if(1) == pytest.approx(0.9911492689, abs=INFORCE)


def test_hand_trace_t1_is_t0_scaled_and_the_year_is_one_set_of_rates(kr_medical_anchor):
    """Month 1 is month 0 multiplied by ``l(1)``, and so is every other month of the year.

    A property of this product rather than a shortcut: every contractual mechanism resets
    annually, so within a policy year the month carries no information the year does not,
    and the monthly grid buys timing and — on an undiscounted projection — nothing at all.
    A model that let a limit, a counter or a deductible accumulate month by month would
    break this immediately.
    """
    a = kr_medical_anchor
    for t in range(1, 12):
        scale = a.pols_if(t)
        assert a.premiums(t) == pytest.approx(a.premiums(0) * scale, rel=1e-13)
        for kind in ("GE_IN", "GE_OUT", "NP_IN", "NP_OUT", "NP_THREE"):
            assert a.claims(t, kind) == pytest.approx(
                a.claims(0, kind) * scale, rel=1e-13), (t, kind)
        assert a.expenses(t) == pytest.approx(a.expenses(0) * scale, rel=1e-13)
        assert a.claim_expenses(t) == pytest.approx(
            a.claim_expenses(0) * scale, rel=1e-13)
        assert a.commissions(t) == pytest.approx(a.commissions(0) * scale, rel=1e-13)
        assert a.net_cf(t) == pytest.approx(a.net_cf(0) * scale, rel=1e-13)
    assert a.pols_if(2) == pytest.approx(
        a.pols_if(1) * (1 - a.mort_rate_mth(1)) * (1 - a.lapse_rate_mth(1)),
        rel=1e-15)
    assert a.pols_if(2) == pytest.approx(0.9823768732, abs=INFORCE)


def test_hand_trace_t11_to_t12_the_renewal(kr_medical_anchor):
    """The annual boundary: the decrements in order, then the re-rate.

    The renewal decline acts **after** mortality, lapse and suspension and only where
    ``(t + 1) mod 12 = 0``, and at every boundary it is the larger of the two voluntary
    exits.  The re-rate is the recursion applied to the **age-adjusted** prior premium, per
    priced unit, which is what reproduces the 표준약관's own illustration; the loop is not
    yet live at ``y = 2`` and the 무사고 할인 needs two clean years, so the step is a pure
    attained-age re-rate of +9.4712%.
    """
    a = kr_medical_anchor
    assert a.pols_if(11) == pytest.approx(0.9068380084, abs=INFORCE)
    assert a.pols_death(11) == pytest.approx(0.0000998270, abs=INFORCE)
    assert a.pols_if_at(11, "BEF_LAPSE") == pytest.approx(0.9067381814, abs=INFORCE)
    assert a.pols_lapse(11) == pytest.approx(0.0079263524, abs=INFORCE)
    assert a.pols_if_at(11, "BEF_SUSPEND") == pytest.approx(0.8988118290, abs=INFORCE)
    assert a.pols_suspend(11) == 0.0
    assert a.pols_if_at(11, "BEF_RENEWAL") == pytest.approx(0.8988118290, abs=INFORCE)
    assert a.pols_renewal_decline(11) == pytest.approx(0.0089881183, abs=INFORCE)
    assert a.pols_if(12) == pytest.approx(0.8898237107, abs=INFORCE)
    assert a.check_pols_roll_fwd_resid(11) == pytest.approx(0.0, abs=1e-14)
    assert a.pols_renewal_decline(11) > a.pols_lapse(11)

    assert a.basis_incr_ge(2) == pytest.approx(0.010, rel=1e-14)
    assert a.basis_incr_np(2) == pytest.approx(0.081, rel=1e-14)
    assert a.prem_ge_base(2) == pytest.approx(4792.80 * 1.04 * 1.010, rel=1e-13)
    assert a.prem_np_base(2) == pytest.approx(7189.20 * 1.04 * 1.081, rel=1e-13)
    assert a.reld_avg(2) == 1.0 and a.noclaim_share(2) == 0.0
    assert a.prem_gross_mth(2) == pytest.approx(13116.7433, abs=WON)
    assert a.prem_gross_mth(2) / a.prem_gross_mth(1) - 1.0 == pytest.approx(
        0.094704, abs=5e-7)
    assert 0.40 * 1.05040 + 0.60 * 1.12424 == pytest.approx(1.094704, rel=1e-14)
    assert a.prem_ge_base(2) / a.prem_ge_base(1) - 1.0 == pytest.approx(
        0.05040, abs=5e-7)
    assert a.prem_np_base(2) / a.prem_np_base(1) - 1.0 == pytest.approx(
        0.12424, abs=5e-7)
    assert a.claims(12) == pytest.approx(
        124750.6482 / 12.0 * 0.8898237107, abs=WON)
    assert a.net_cf(12) == pytest.approx(
        0.87 * a.premiums(12) - 1.03 * a.claims(12), abs=1e-9)
    # The premium falls month by month inside a year and rises at the boundary.
    assert all(a.premiums(t + 1) < a.premiums(t) for t in range(0, 11))
    assert a.premiums(12) > a.premiums(11)


def test_hand_trace_t59_to_t60_the_reentry_that_does_nothing_and_the_band_step(
        kr_medical_anchor):
    """The first 재가입 is a no-op by assumption; the utilisation band step is not.

    ``t = 60`` is the fifth 계약해당일, where a real 4세대 contract re-enters whatever
    generation is then on sale.  This model assumes re-entry on unchanged terms, so nothing
    whatever happens in the cash flows at the 보장내용 변경주기 — and that no-op is the
    assumption made visible.  What does happen is the five-year utilisation band stepping to
    (M, 45), and it takes ``net_cf`` from +₩1,410.26 to −₩23.31, the projection's only
    negative month-of-a-negative-year.
    """
    a = kr_medical_anchor
    assert a.util_band(5) == 40 and a.util_band(6) == 45
    assert a.trend_ge(6) == pytest.approx(1.010 ** 5, rel=1e-14)
    assert a.trend_np(6) == pytest.approx(1.081 ** 5, rel=1e-14)
    assert a.trend_ge(6) == pytest.approx(1.0510100501, abs=5e-11)
    assert a.trend_np(6) == pytest.approx(1.4761431304, abs=5e-11)
    assert a.oop_incurred_ge(6) == pytest.approx(106406.0369, abs=WON)
    assert a.oop_trunc(6) == 1.0
    assert a.claims_ge_in_pp(6) == pytest.approx(17594.7625, abs=WON)
    assert a.claims_ge_out_pp(6) == pytest.approx(52957.9121, abs=WON)
    assert a.claims_np_in_pp(6) == pytest.approx(34699.7101, abs=WON)
    assert a.claims_np_out_pp(6) == pytest.approx(34485.9651, abs=WON)
    assert a.claims_physio_pp(6) == pytest.approx(16430.9164, abs=WON)
    assert a.claims_inject_pp(6) == pytest.approx(13328.1121, abs=WON)
    assert a.claims_mri_pp(6) == pytest.approx(13931.1237, abs=WON)
    assert a.claims_ann_pp(6) == pytest.approx(183428.5019, abs=WON)
    assert a.prem_gross_mth(6) == pytest.approx(
        (6128.6225 + 12911.4712 * 1.0025494) * (1.0 - 0.10 * 0.5314584961), abs=0.001)
    assert a.premiums(60) == pytest.approx(12896.5596, abs=WON)
    assert a.claims(60) == pytest.approx(183428.5019 / 12.0 * 0.7141205641, abs=WON)
    assert a.net_cf(60) == pytest.approx(-23.3071, abs=WON)
    # The step, decomposed: claims x 1.2758 against premium x 1.0994.
    assert a.claims_ann_pp(6) / a.claims_ann_pp(5) == pytest.approx(1.27575, abs=5e-6)
    assert a.prem_gross_mth(6) / a.prem_gross_mth(5) == pytest.approx(
        1.09941, abs=5e-6)
    lr5 = a.claims_ann_pp(5) / (a.prem_gross_mth(5) * 12.0)
    lr6 = a.claims_ann_pp(6) / (a.prem_gross_mth(6) * 12.0)
    assert lr5 == pytest.approx(0.7294, abs=5e-5)
    assert lr6 == pytest.approx(0.8464, abs=5e-5)
    assert lr5 < BREAK_EVEN_LR < lr6, "the band step crosses the break-even loss ratio"


def test_the_horizon_absorbs_the_whole_remaining_in_force_and_pays_nothing(
        kr_medical_anchor):
    """``t = 119``: the renewal decline and the maturity count together take everything.

    ``pols_maturity`` is non-zero only in the last projected month, ``t = proj_len() - 1``
    — 119 on this cell, the frame being ``range(proj_len())`` — and pays **nothing** —
    there is no 만기보험금 on a 순수보장성 contract — but the count is needed for the
    roll-forward to close.  What ends there is the *stated horizon*, not the cover.
    """
    a = kr_medical_anchor
    assert a.pols_maturity(119) == pytest.approx(0.6004036091, abs=INFORCE)
    assert a.pols_renewal_decline(119) == pytest.approx(0.0060646829, abs=INFORCE)
    assert all(a.pols_maturity(t) == 0.0 for t in range(0, 119))
    assert a.pols_if(120) == 0.0
    assert a.pols_maturity(119) + a.pols_renewal_decline(119) + a.pols_death(119) \
        + a.pols_lapse(119) == pytest.approx(a.pols_if(119), abs=1e-12)
    df = a.result_cf()
    assert set(df.columns) & {"claims_maturity", "claims_death", "claims_lapse"} == set()


def test_reading_the_shape_of_the_result(kr_medical_anchor):
    """The composition, the saw-tooth and the migration the notes read off the result.

    Three findings, each of which cuts against the market narrative: 급여 통원 is the single
    largest limb and the 급여 half is the *worse* half throughout; the loss ratio saw-tooths
    downward because the premium takes its 4% age loading nine times while the claim takes
    its age effect in one 21.5% step; and the loop moves nothing on an average cell until
    the discount cap breaks revenue neutrality, its whole effect being cross-sectional.
    """
    a = kr_medical_anchor
    df = a.result_cf()
    claims = df[[c for c in df.columns if c.startswith("claims_")]].sum()
    total = claims.sum()
    assert claims["claims_ge_out"] / total == pytest.approx(0.297336, abs=SHARE)
    assert claims["claims_ge_out"] == claims.max()          # the largest single limb
    ge_half = (claims["claims_ge_in"] + claims["claims_ge_out"]) / total
    assert ge_half == pytest.approx(0.393349, abs=SHARE)
    assert 1.0 - ge_half == pytest.approx(0.606651, abs=SHARE)
    assert claims["claims_np_three"] / total == pytest.approx(0.234908, abs=SHARE)

    ratios = [POLICY_YEAR_TOTALS[y][7] for y in range(1, 11)]
    assert ratios[5] == max(ratios) and ratios[9] == min(ratios)
    assert all(ratios[y] < ratios[y - 1] for y in (1, 3, 4))       # the downward teeth
    assert ratios[5] > ratios[4], "policy year 6 is the band step"
    assert 1.04 ** 9 == pytest.approx(1.4233, abs=5e-5)

    # The migration: the 3단계 buckets empty, the 5단계 contribution more than triples.
    assert a.band_share(4, 3) > 0.0 and a.band_share(5, 3) == 0.0
    assert a.band_share(2, 5) * 4.0 == pytest.approx(0.012, abs=1e-12)
    assert a.band_share(7, 5) * 4.0 == pytest.approx(0.040, abs=1e-12)
    assert a.reld_surcharge(2) - a.band_share(2, 2) == pytest.approx(0.049, abs=1e-12)
    assert a.reld_surcharge(7) - a.band_share(7, 2) == pytest.approx(0.064, abs=1e-12)
    assert max(a.reld_avg(y) for y in range(1, 11)) == pytest.approx(
        1.0095494, abs=RELD)
    # Cross-sectionally the scheme is not small at all: 2.80x against 0.9745x.
    assert 0.40 + 0.60 * a.band_relativity(5) == pytest.approx(2.80, rel=1e-14)
    assert 0.40 + 0.60 * a.reld_solved(2) == pytest.approx(0.9745, abs=5e-5)


# ---------------------------------------------------------------------------
# The check_* cells and the product's own identities


def test_which_checks_this_model_publishes(indemnity_medical, kr_medical_anchor):
    """The ten check cells, asserted **by name**, and the argument each residual takes.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared: it
    would call the nine that remain, pass, and prove less than it did before.  Naming the
    set turns "every check passes" into a statement about *which* checks — and six of these
    ten exist only on this product, because nothing else in the repository has an incurred
    loss to bound a claim by, a public co-payment ceiling to exclude from cover, a
    revenue-neutral experience relativity to solve, a supervisory re-rating corridor per
    위험구분단위, an annual limit stack to prove wired, or a claim-shape distribution that
    must be a distribution.
    """
    published = {n for n in indemnity_medical.Projection.cells
                 if n.startswith("check_") and not n.endswith("_resid")}
    assert published == CHECKS
    resid = {n[:-len("_resid")] for n in indemnity_medical.Projection.cells
             if n.startswith("check_") and n.endswith("_resid")}
    assert resid == CHECKS
    assert CHECKS_PER_T | CHECKS_PER_Y | CHECKS_SCALAR == CHECKS

    a = kr_medical_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True and isinstance(value, bool), name
    for name in sorted(CHECKS_PER_T):
        residual = getattr(a, name + "_resid")
        for t in range(a.proj_len()):
            assert residual(t) == pytest.approx(0.0, abs=1e-8), f"{name}_resid({t})"
    for name in sorted(CHECKS_PER_Y):
        residual = getattr(a, name + "_resid")
        for y in range(1, 11):
            assert residual(y) == pytest.approx(0.0, abs=1e-8), f"{name}_resid({y})"
    for name in sorted(CHECKS_SCALAR):
        assert getattr(a, name + "_resid")() == pytest.approx(0.0, abs=1e-8), name


def test_the_check_tolerances_are_named_references(indemnity_medical, kr_medical_anchor):
    """No bare literal tolerance: ``roll_fwd_tol``, ``cash_tol`` and ``shape_tol``.

    Three different quantities that must not collapse into one.  ``roll_fwd_tol`` closes
    identities between cells evaluated in a single expression; ``cash_tol`` closes
    ``check_net_cf``, which re-reads won amounts of order 1e4 back out of the frame and must
    therefore be wider — and still far below one won, the smallest error a reader adding up
    the printed statement could observe.  ``shape_tol`` closes the claim-shape
    normalisation, where the residual is a sum of ten tabulated shares.
    """
    refs = indemnity_medical.Projection.refs
    assert refs["roll_fwd_tol"] == 1e-10
    assert refs["cash_tol"] == 1e-6
    assert refs["shape_tol"] == 1e-9
    assert refs["roll_fwd_tol"] < refs["cash_tol"] < 1.0
    a = kr_medical_anchor
    worst = max(abs(a.check_net_cf_resid(t)) for t in range(a.proj_len()))
    assert worst < refs["cash_tol"] / 100.0
    worst_roll = max(abs(a.check_pols_roll_fwd_resid(t))
                     for t in range(a.proj_len()))
    assert worst_roll < refs["roll_fwd_tol"] / 100.0


def test_the_inforce_rollforward_is_the_notes_identity(indemnity_medical):
    """l(t) - l(t+1) = deaths + lapses + suspensions + declines + maturities.

    **Five** decrements, and the middle three are what make this roll-forward different from
    a term assurance's: 개인실손 중지 is a supervisory requirement rather than a product
    feature, the renewal decline is an option the policyholder holds and the insurer does
    not, and the maturity count is the stated horizon rather than the end of cover.  Drop
    any of them and the roll-forward loses lives with no cause.
    """
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        for t in range(p.proj_len()):
            out = (p.pols_death(t) + p.pols_lapse(t) + p.pols_suspend(t)
                   + p.pols_renewal_decline(t) + p.pols_maturity(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12), \
                (point_id, t)
            assert 0.0 <= p.pols_if(t) <= 1.0
            assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15


def test_the_decrements_are_taken_in_the_notes_processing_order(indemnity_medical):
    """Mortality, then lapse, then suspension, then the renewal decline — in that order.

    Each timing reads the population the next decrement is taken from, which is what makes
    the renewal decline a decrement on the survivors of lapse rather than a competitor of
    it.  Model point 9 is the one that can tell the third step from the fourth, because it
    is the only shipped point with a non-zero 개인실손 중지 rate: on every other point
    ``BEF_SUSPEND`` and ``BEF_RENEWAL`` coincide and the order is untestable.
    """
    for point_id in (1, 9):
        p = indemnity_medical.Projection[point_id]
        for t in (0, 5, 11, 23, 60, 119):
            assert p.pols_if_at(t, "BEF_DECR") == p.pols_if(t)
            assert p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
                p.pols_if(t) * (1 - p.mort_rate_mth(t)), rel=1e-14)
            assert p.pols_if_at(t, "BEF_SUSPEND") == pytest.approx(
                p.pols_if_at(t, "BEF_LAPSE") * (1 - p.lapse_rate_mth(t)), rel=1e-14)
            assert p.pols_if_at(t, "BEF_RENEWAL") == pytest.approx(
                p.pols_if_at(t, "BEF_SUSPEND") * (1 - p.suspend_rate_mth(t)),
                rel=1e-14)
        for t in (0, 5, 58):
            assert p.pols_if_at(t, "BEF_RENEWAL") == p.pols_if_at(t, "AFT_DECR")
    p9 = indemnity_medical.Projection[9]
    assert p9.suspend_rate() == 0.03
    assert p9.pols_if_at(11, "BEF_SUSPEND") > p9.pols_if_at(11, "BEF_RENEWAL")
    assert p9.pols_suspend(11) > 0.0
    with pytest.raises(Exception):
        p9.pols_if_at(11, "NOT_A_TIMING")


def test_the_published_statement_adds_up(indemnity_medical):
    """The ``result_cf()`` columns are a decomposition of ``net_cf``, not a selection.

    ``check_net_cf`` guards against a benefit limb that exists in ``claims()`` but was never
    given a column, which would leave the statement silently short of outgo.  The five
    claim columns must also sum to ``claims(t)`` exactly, because there is deliberately no
    ``claims`` subtotal column for them to be reconciled against.
    """
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        df = p.result_cf()
        claim_cols = [c for c in df.columns if c.startswith("claims_")]
        outgo = df[claim_cols + ["expenses", "claim_expenses", "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9)
        for t in (0, 11, 60, p.proj_len() - 1):
            assert df.loc[t, claim_cols].sum() == pytest.approx(p.claims(t), abs=1e-9)
        assert df.index.name == "t" and list(df.columns)[0] == "pols_if"
        assert "net_cf" in df.columns and not df.isna().any().any()
        assert len(df) == p.proj_len()


def test_the_premium_recursion_reproduces_the_wordings_own_illustration(
        kr_medical_anchor):
    """The 표준약관's printed row 14,000 → 18,200 → 23,660 → 30,758 → 39,985 → 51,980.

    That row exists only if the corridor is applied to the **age-adjusted** prior premium,
    which is the order of operations the illustration's own label 「기초율 증가분 = 전년도
    기준보험료 x 25%」 disguises: 3,640 is 25% of 14,560 = 14,000 x 1.04.  Reproducing it
    with the model's own recursion factor is the evidence the recursion is the wording's.
    And the composition across the five bands is reproduced at the rider share the
    illustration itself implies, s = 0.4875 — the check that
    ``base_ge + base_np x relativity`` is the right composition and not a guess.
    """
    a = kr_medical_anchor
    factor = (1.0 + a.age_load) * (1.0 + a.renewal_corridor)
    assert factor == pytest.approx(1.30, rel=1e-14)
    printed = [14000, 18200, 23660, 30758, 39985, 51980]
    for prev, following in zip(printed, printed[1:]):
        assert prev * factor == pytest.approx(following, abs=1.0)
    assert 14000.0 * 0.04 == pytest.approx(560.0, rel=1e-14)      # the 나이증가분
    assert 14560.0 * 0.25 == pytest.approx(3640.0, rel=1e-14)     # the 기초율 증가분
    s = 0.4875                       # the rider share the illustration itself implies
    assert 18200.0 * ((1 - s) + s * a.band_relativity(3)) == pytest.approx(
        27073.0, abs=1.0)               # the wording prints whole won
    assert 23660.0 * ((1 - s) + s * a.band_relativity(5)) == pytest.approx(
        58263.0, abs=1.0)
    # And the recursion the model actually runs, unit by unit, on the anchor.
    for y in range(2, 11):
        assert a.prem_ge_base(y) == pytest.approx(
            a.prem_ge_base(y - 1) * 1.04 * 1.010, rel=1e-13)
        assert a.prem_np_base(y) == pytest.approx(
            a.prem_np_base(y - 1) * 1.04 * 1.081, rel=1e-13)
    assert a.prem_np_base(10) == pytest.approx(
        7189.20 * (1.04 * 1.081) ** 9, rel=1e-13)


def test_the_relativity_is_revenue_neutral_until_the_std_cap_breaks_it(
        kr_medical_anchor):
    """``Sum_b w_b r_b = 1`` exactly while the discount cap is slack, and > 1 after.

    The wording fixes the constraint and not the discount — 「매년 상대도 적용 전·후의 총
    보험료 수준이 일치하도록」 — so the band-1 relativity is solved from neutrality.  The
    [std] 5% cap does not bind at commencement, where the solve is 4.2523%; it binds from
    ``y = 5``, when bucket 7 has trended across ₩1,500,000 into 4단계 and the pool would
    fund 5.35%.  **The scheme stops being revenue-neutral at the moment the discount is
    capped**, and after that the loop is a net addition to premium.
    """
    a = kr_medical_anchor
    for y in range(1, 11):
        pool = sum(a.band_share(y, b) * a.band_relativity(b) for b in (2, 3, 4, 5))
        assert a.reld_surcharge(y) == pytest.approx(pool, rel=1e-14)
        if a.band_share(y, 1) > 0.0:
            assert a.reld_solved(y) == pytest.approx(
                (1.0 - pool) / a.band_share(y, 1), rel=1e-14)
        assert a.reld_one(y) == pytest.approx(
            max(a.reld_solved(y), 0.95), rel=1e-14)
        assert sum(a.band_share(y, b) for b in (1, 2, 3, 4, 5)) == pytest.approx(
            1.0, abs=1e-12)
        assert a.reld_avg(y) >= 1.0 - 1e-12, "the scheme never funds what it has not raised"
    assert a.reld_active(3) is False and a.reld_active(4) is True
    for y in (1, 2, 3, 4):
        assert a.reld_avg(y) == pytest.approx(1.0, abs=1e-12)
    assert a.reld_solved(2) == pytest.approx(0.9574766945, abs=RELD)
    assert 1.0 - a.reld_solved(2) == pytest.approx(0.042523, abs=5e-7)
    assert a.reld_solved(5) == pytest.approx(0.9465029382, abs=RELD)
    assert 1.0 - a.reld_solved(5) == pytest.approx(0.0535, abs=5e-5)
    assert a.reld_one(5) == 0.95 and a.reld_avg(5) > 1.0


def test_the_limits_are_wired_and_none_of_them_binds_on_a_deterministic_cell(
        indemnity_medical):
    """``check_annual_limits()`` proves the machinery is wired, not that it is exercised.

    On a deterministic expected-value grid ``E[min(X, L)] != min(E[X], L)``, so a single
    cell's expected annual claim sits two orders of magnitude below every money limit — the
    supervisor's own tail figure is 0.005% of insureds above ₩50,000,000 in 2019.  The
    check is still the only thing that says the limits are in the formulas at all, and the
    per-visit cap **does** bind, on model point 7's ₩100,000 rung.
    """
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        assert p.check_annual_limits() is True
        for y in range(1, 11):
            assert p.check_annual_limits_resid(y) == 0.0
            assert p.ge_limit_factor(y) == pytest.approx(1.0, abs=1e-12)
            assert p.np_limit_factor(y) == pytest.approx(1.0, abs=1e-12)
            assert p.visits_np_eff(y) < p.visit_limit_np
            assert p.acts_physio_eff(y) < p.act_limit_three
            assert p.acts_inject_eff(y) < p.act_limit_three
    p7 = indemnity_medical.Projection[7]
    assert p7.visit_cap() == 100000.0
    assert p7.paid_out_per_visit("ge_out", 10000.0, 0.20, 1.0) == pytest.approx(
        21540.0, abs=WON)
    assert p7.paid_out_per_visit("ge_out", 10000.0, 0.20, 1.0) < GE_OUT_CLINIC
    assert p7.paid_out_per_visit("np_out", 30000.0, 0.30, 1.0) == pytest.approx(
        58250.0, abs=WON)


def test_the_indemnity_ceiling_is_this_products_defining_constraint(indemnity_medical):
    """The claim never exceeds the incurred covered loss, on any point in any year.

    「실제 발생한 손해(비용)를 초과하여 보험금을 지급하지 않습니다」.  A co-payment applied
    as a multiplier instead of a retention, a deductible subtracted twice, or a per-visit cap
    applied to the wrong side of the deduction would all show up here and nowhere else.
    ``Cancer_KR_S`` and ``LTC_KR_S`` have no analogue of this check because they have no
    incurred loss to bound against — it is the 정액 / 실손해 fork in one identity.
    """
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        assert p.check_indemnity() is True
        for y in range(1, 11):
            assert p.claims_ann_pp(y) <= p.loss_incurred_pp(y) + 1e-6, (point_id, y)
            assert p.check_indemnity_resid(y) == 0.0
    a = indemnity_medical.Projection[1]
    assert a.claims_ann_pp(1) == pytest.approx(119054.4651, abs=WON)
    assert a.loss_incurred_pp(1) == pytest.approx(186006.8254, abs=WON)


def test_the_three_published_frames_and_the_sign_they_carry(kr_medical_anchor):
    """``result_cf``, ``result_pols`` and ``result_prem``, and the income-positive sign.

    Three frames on two clocks: the cash flow statement and the in-force movements are
    indexed by policy month, and the renewal ledger by policy year, because that is the clock
    the whole premium mechanism runs on.  ``net_cf`` is income-positive and there is
    deliberately **no** outgo-positive ``liability_cf`` companion — the notes print the
    stream in this sign, so one stream, one sign, one name.
    """
    a = kr_medical_anchor
    cf, pols, prem = a.result_cf(), a.result_pols(), a.result_prem()
    assert list(cf.columns) == [
        "pols_if", "premiums", "claims_ge_in", "claims_ge_out", "claims_np_in",
        "claims_np_out", "claims_np_three", "expenses", "claim_expenses",
        "commissions", "net_cf"]
    assert all(c == c.lower() for c in cf.columns)
    assert pols.index.name == "t" and len(pols) == 120
    assert list(pols.columns) == [
        "pols_if", "pols_death", "pols_lapse", "pols_suspend",
        "pols_renewal_decline", "pols_maturity", "mort_rate", "lapse_rate"]
    assert prem.index.name == "policy_year" and list(prem.index) == list(range(1, 11))
    assert "liability_cf" not in cf.columns
    assert "liability_cf" not in set(kr_medical_anchor.cells)
    assert cf["net_cf"].sum() > 0.0
    assert cf.loc[0, "net_cf"] == pytest.approx(
        cf.loc[0, "premiums"] - cf.loc[0, ["claims_ge_in", "claims_ge_out",
                                           "claims_np_in", "claims_np_out",
                                           "claims_np_three", "expenses",
                                           "claim_expenses", "commissions"]].sum(),
        abs=1e-9)


# ---------------------------------------------------------------------------
# Known modeling pitfalls, one test each


def test_pitfall_do_not_multiply_a_rate_by_the_boheom_gaipgeumaek(indemnity_medical):
    """Pitfall: multiplying a rate by the 보험가입금액. There is no sum assured here.

    The ₩50,000,000 is an annual **cap** and may appear only inside a ``min``.  Any
    expression in which ``annual_limit()`` is a multiplier has the dimensions of money and
    the meaning of nothing, and it is the commonest error an actuary arriving from a
    fixed-benefit 제3보험 product makes.  The arithmetic guard is that the claim is
    *independent* of the limit while the limit is slack and *capped by* it when it is not —
    which is exactly what a multiplier could not do.
    """
    names = set(indemnity_medical.Projection.cells) | set(
        indemnity_medical.Projection.refs)
    for absent in ("sum_assured", "sum_insured", "benefit_pp", "face_amount",
                   "daily_benefit", "hosp_benefit"):
        assert absent not in names, f"{absent} would make this a fixed-benefit product"

    base = indemnity_medical.Projection[1].claims_ann_pp(1)
    table = indemnity_medical.Data.model_point_table()
    tenfold = table.copy()
    tenfold.loc[1, "annual_limit"] = 500000000.0
    with _swapped("lim10", "model_point_file", tenfold,
                  "model_point_table_lim10.csv") as model:
        p = model.Projection[1]
        assert p.annual_limit() == 500000000.0
        assert p.claims_ann_pp(1) == pytest.approx(base, rel=1e-12), \
            "a slack limit moved the claim, so it is not inside a min"
    tiny = table.copy()
    tiny.loc[1, "annual_limit"] = 20000.0
    with _swapped("limtiny", "model_point_file", tiny,
                  "model_point_table_limtiny.csv") as model:
        p = model.Projection[1]
        assert p.ge_limit_factor(1) == pytest.approx(0.5066574378, abs=5e-10)
        assert p.np_limit_factor(1) == pytest.approx(0.6562930379, abs=5e-10)
        assert p.claims_ann_pp(1) == pytest.approx(77812.2879, abs=WON)
        assert p.claims_ann_pp(1) < base
        assert p.check_annual_limits() is True and p.check_indemnity() is True
        # and the 3대비급여 limbs are untouched: their sub-limits replace the aggregate.
        assert p.claims_np_three_pp(1) == pytest.approx(23475.4331, abs=WON)


def test_pitfall_apply_the_deductible_to_the_distribution_not_to_the_mean(
        kr_medical_anchor):
    """Pitfall: taking the deductible against a mean cost instead of a distribution.

    The deductible is ``max(flat floor, percentage x cost)`` — flat below a crossing point
    and a percentage above it — so the payment is kinked and ``E[f(X)] != f(E[X])``.  On the
    비급여 통원 limb the error is **+35.83%**.  The trap is that it can hide: on the 급여
    통원 limb the clinic tier is +6.36% and the hospital tier −17.01%, and the blend at
    ``clinic_share = 0.63`` comes out only −1.05% wrong, so a model that checks the blend
    and not the tiers passes its own test and misprices both providers.
    """
    a = kr_medical_anchor

    def naive(stream, floor, retain):
        mu = a.sev_mean(stream)
        return max(0.0, mu - max(floor, retain * mu))

    np_out = a.paid_out_per_visit("np_out", 30000.0, 0.30, 1.0)
    assert naive("np_out", 30000.0, 0.30) == pytest.approx(104545.0, abs=WON)
    assert naive("np_out", 30000.0, 0.30) / np_out - 1.0 == pytest.approx(
        0.3583, abs=5e-5)
    clinic = a.paid_out_per_visit("ge_out", 10000.0, 0.20, 1.0)
    hospital = a.paid_out_per_visit("ge_out", 20000.0, 0.20, 1.0)
    assert naive("ge_out", 10000.0, 0.20) / clinic - 1.0 == pytest.approx(
        0.0636, abs=5e-5)
    assert naive("ge_out", 20000.0, 0.20) / hospital - 1.0 == pytest.approx(
        -0.1701, abs=5e-5)
    blend = 0.63 * clinic + 0.37 * hospital
    naive_blend = 0.63 * naive("ge_out", 10000.0, 0.20) \
        + 0.37 * naive("ge_out", 20000.0, 0.20)
    assert naive_blend / blend - 1.0 == pytest.approx(-0.0105, abs=5e-5)
    # MRI is the control: every point sits above its crossing, so the mean is exact there.
    assert a.paid_per_act("mri", 1.0) == pytest.approx(
        naive("mri", 30000.0, 0.30), rel=1e-14)


def test_pitfall_the_public_ceiling_is_an_exclusion_from_covered_loss_not_a_benefit_cap(
        indemnity_medical):
    """Pitfall: applying 본인부담상한제 to the finished claim instead of to the loss.

    ``oop_trunc(y)`` multiplies the incurred cost **inside** ``paid_out_per_visit``, so it
    changes where the deductible bites; applying it to the finished claim is linear on the
    inpatient limb and **wrong on the outpatient limb**, where the deductible is kinked.  On
    the anchor ``oop_trunc == 1.0`` and the error is invisible; on model point 8 it is
    +7.26% in policy year 1 and +16.62% by policy year 10.  ``check_oop_ceiling()`` asserts
    the statement about the **loss** and not one about the benefit.
    """
    p = indemnity_medical.Projection[8]
    assert p.util_mult() == 10.0 and p.oop_decile() == 1
    assert p.oop_ceiling() == 900000.0
    assert p.oop_trunc(1) == pytest.approx(0.8018275589, abs=5e-10)
    assert p.oop_trunc(10) == pytest.approx(0.6024410326, abs=5e-10)
    assert p.check_oop_ceiling() is True
    for y in range(1, 11):
        assert p.oop_incurred_ge(y) * p.oop_trunc(y) <= p.oop_ceiling() + 1e-6
    for y, ratio in ((1, 0.0726), (10, 0.1662)):
        tr = p.trend_ge(y)
        r = p.retain_rate_ge()
        blend = p.clinic_share() * p.paid_out_per_visit("ge_out", 10000.0, r, tr) \
            + (1.0 - p.clinic_share()) * p.paid_out_per_visit("ge_out", 20000.0, r, tr)
        after = p.visit_rate_ge(y) * blend * p.oop_trunc(y)   # the wrong order
        assert after / p.claims_ge_out_pp(y) - 1.0 == pytest.approx(ratio, abs=5e-5)
    # On every other shipped point the truncation is inert, and says so.
    for point_id in indemnity_medical.Data.model_point_table().index:
        if point_id == 8:
            continue
        q = indemnity_medical.Projection[point_id]
        assert all(q.oop_trunc(y) == 1.0 for y in range(1, 11)), point_id


def test_pitfall_the_two_million_won_cap_sits_on_the_retention_that_survives_the_ceiling(
        indemnity_medical):
    """Pitfall: taking the ₩2,000,000 inpatient cap before the 본인부담상한제, or beside it.

    Both reduce the insured's retention on heavy 급여 use, so the order is fixed: the
    ceiling **first**, as an exclusion from covered loss, and the cap **second** on what
    remains.  The two are nested rather than parallel, and the nesting has a consequence
    worth stating: inside 국민건강보험 the cap can never bind at all, because the ceiling
    holds the whole 급여 co-payment at ₩8,430,000 even at the top decile and 20% of that is
    ₩1,686,000.  Applying the cap to the *untruncated* retention breaks that: on a
    top-decile cell it inflates the inpatient limb by 12.42%.
    """
    a = indemnity_medical.Projection[1]
    ceiling_max = float(indemnity_medical.Data.oop_ceiling_table()["ceiling"].max())
    assert ceiling_max == 8430000.0
    assert a.retain_rate_ge_base * ceiling_max < a.cap_inpatient_retain
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        for y in range(1, 11):
            cost = p.adm_rate(y) * p.sev_mean("ge_in") * p.trend_ge(y) * p.oop_trunc(y)
            top_up = max(0.0, cost * p.retain_rate_ge() - p.cap_inpatient_retain)
            assert p.claims_ge_in_pp(y) == pytest.approx(
                cost * (1.0 - p.retain_rate_ge()) + top_up, rel=1e-14), (point_id, y)
            assert top_up == 0.0

    table = indemnity_medical.Data.model_point_table()
    heavy = table.copy()
    heavy.loc[8, "util_mult"] = 1000.0
    with _swapped("cap", "model_point_file", heavy,
                  "model_point_table_cap.csv") as model:
        p = model.Projection[8]
        cost_untruncated = p.adm_rate(1) * p.sev_mean("ge_in") * p.trend_ge(1)
        cost = cost_untruncated * p.oop_trunc(1)
        r = p.retain_rate_ge()
        assert cost_untruncated * r > p.cap_inpatient_retain    # the cap would bind
        assert cost * r < p.cap_inpatient_retain                # but it does not
        wrong = (cost_untruncated * (1.0 - r)
                 + max(0.0, cost_untruncated * r - p.cap_inpatient_retain)) \
            * p.oop_trunc(1)
        assert wrong / p.claims_ge_in_pp(1) - 1.0 == pytest.approx(0.1242, abs=5e-5)
        assert p.check_indemnity() is True and p.check_oop_ceiling() is True


def test_pitfall_the_corridor_applies_to_the_age_adjusted_prior_premium(
        indemnity_medical, kr_medical_anchor):
    """Pitfall: reading 「기초율 증가분 = 전년도 기준보험료 x 25%」 as additive.

    3,640 is 25% of 14,000 x 1.04 and not of 14,000, so the corridor applies to the
    **age-adjusted** prior premium.  Getting it wrong costs 4% of the corridor every year
    and compounds: on this cell's rider unit the correct annual factor is 1.04 x 1.081 =
    1.12424 and the additive misreading gives 1.121, which puts the year-10 rider base
    ₩20,096.9929 against ₩20,625.8505 — 2.564% low.  ``check_renewal_corridor()`` measures
    the move against the age-adjusted prior premium and **per 위험구분단위**, so it catches
    the loading applied on the wrong side of the clip.
    """
    a = kr_medical_anchor
    assert a.prem_np_base(10) == pytest.approx(20625.8505, abs=WON)
    additive = 7189.20 * (1.04 + 0.081) ** 9
    assert additive == pytest.approx(20096.9929, abs=WON)
    assert additive / a.prem_np_base(10) - 1.0 == pytest.approx(-0.02564, abs=5e-6)
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        assert p.check_renewal_corridor() is True
        for y in range(2, 11):
            for base in (p.prem_ge_base, p.prem_np_base):
                prev = base(y - 1) * (1.0 + p.age_load)
                if prev > 0.0:
                    assert abs(base(y) / prev - 1.0) <= p.renewal_corridor + 1e-12
    # Model point 10 is the one whose corridor actually clips, per unit and every year.
    p10 = indemnity_medical.Projection[10]
    assert p10.trend_mult() == 4.5
    assert p10.med_trend_np * p10.trend_mult() == pytest.approx(0.36450, rel=1e-14)
    assert p10.basis_incr_np(2) == 0.25              # clipped
    assert p10.basis_incr_ge(2) == pytest.approx(0.045, rel=1e-14)   # not clipped
    for y in range(2, 11):
        assert p10.prem_np_base(y) == pytest.approx(
            p10.prem_np_base(y - 1) * 1.04 * 1.25, rel=1e-13)


def test_pitfall_the_relativity_touches_the_rider_and_nothing_else(kr_medical_anchor):
    """Pitfall: applying ``reld_avg`` to the whole office premium.

    「비급여 특약 보험료만 할증되며 보험료 전체가 할증되는 것은 아닙니다」.  Applying the
    average relativity to the whole premium gives a year-5 gross of ₩16,440.5468 against
    the correct ₩16,426.4626, and the gap grows with the surcharge pool.  The 무사고 할인
    runs the other way — it is the one relief that *does* take the whole premium — so the
    two must not be given the same base.
    """
    a = kr_medical_anchor
    correct = (a.prem_ge_base(5) + a.prem_np_base(5) * a.reld_avg(5)) \
        * (1.0 - 0.10 * a.noclaim_share(5))
    whole = (a.prem_ge_base(5) + a.prem_np_base(5)) * a.reld_avg(5) \
        * (1.0 - 0.10 * a.noclaim_share(5))
    assert a.prem_gross_mth(5) == pytest.approx(correct, rel=1e-14)
    assert a.prem_gross_mth(5) == pytest.approx(16426.4626, abs=WON)
    assert whole == pytest.approx(16440.5468, abs=WON)
    assert whole > a.prem_gross_mth(5)
    # The 무사고 할인 is the relief that does take the whole premium.
    ungrossed = a.prem_ge_base(3) + a.prem_np_base(3) * a.reld_avg(3)
    assert a.prem_gross_mth(3) == pytest.approx(
        ungrossed * (1.0 - 0.10 * a.noclaim_share(3)), rel=1e-14)


def test_pitfall_the_band_one_relativity_is_solved_not_the_wordings_ninety_five(
        kr_medical_anchor):
    """Pitfall: hard-coding the illustration's 95% band-1 relativity.

    Doing so from policy year 2 gives ``reld_avg = 0.729012 x 0.95 + 0.301988 = 0.9945494``
    — a 0.55% leak out of a scheme the wording requires be self-financing, growing as the
    band mix moves.  The solved figure at commencement is 0.9574766945, and it is the
    specification's 0.9575 arriving as a *result* rather than as an input.
    ``check_relativity_neutral()`` asserts the identity while the cap is slack and only the
    no-under-funding half of it once the cap binds.
    """
    a = kr_medical_anchor
    hardcoded = a.band_share(2, 1) * 0.95 + a.reld_surcharge(2)
    assert hardcoded == pytest.approx(0.9945494, abs=5e-8)
    assert hardcoded < 1.0, "hard-coding 0.95 under-funds the scheme"
    assert a.band_share(2, 1) * a.reld_solved(2) + a.reld_surcharge(2) == \
        pytest.approx(1.0, abs=1e-12)
    assert a.reld_solved(2) == pytest.approx(0.9574766945, abs=RELD)
    assert a.check_relativity_neutral() is True
    # The neutrality identity is sensitive to the band distribution, and that is the point:
    # on the FSC's alternative commencement mix the same identity gives 0.9791.
    alt = {1: 0.621, 2: 0.366, 3: 0.013}
    pool = sum(alt[b] * a.band_relativity(b) for b in (2, 3))
    assert (1.0 - pool) / alt[1] == pytest.approx(0.9791, abs=5e-5)
    assert 1.0 - (1.0 - pool) / alt[1] == pytest.approx(0.021, abs=5e-4)


def test_pitfall_the_noclaim_discount_has_a_two_year_lookback(kr_medical_anchor):
    """Pitfall: giving the 무사고 할인 on one clean year instead of two.

    ``noclaim_share(3) = band_share(2, 1) x band_share(3, 1) = 0.729012² = 0.5314584961``,
    not 0.729012.  A one-year lookback gives a year-3 office premium of ₩13,326.7028 against
    the correct ₩13,610.6786 — 2.09% low — and hands the 10% discount to policyholders who
    have earned one clean year rather than two.  The two reliefs also apply to different
    bases: the relativity to the rider, the 무사고 할인 to the whole premium.
    """
    a = kr_medical_anchor
    assert a.noclaim_share(1) == 0.0 and a.noclaim_share(2) == 0.0
    assert a.noclaim_share(3) == pytest.approx(0.729012 ** 2, rel=1e-13)
    assert a.noclaim_share(3) == pytest.approx(0.5314584961, abs=RELD)
    for y in range(3, 11):
        assert a.noclaim_share(y) == pytest.approx(
            a.band_share(y - 1, 1) * a.band_share(y, 1), rel=1e-14)
    assert a.prem_gross_mth(3) == pytest.approx(13610.6786, abs=WON)
    one_year = (a.prem_ge_base(3) + a.prem_np_base(3) * a.reld_avg(3)) \
        * (1.0 - 0.10 * a.band_share(3, 1))
    assert one_year == pytest.approx(13326.7028, abs=WON)
    assert one_year / a.prem_gross_mth(3) - 1.0 == pytest.approx(-0.0209, abs=5e-5)
    # The launch release's three-year timeline: years 1-2 the rider discount only, year 3
    # adds the 10% on the whole premium — so the year-3 premium falls below the un-discounted.
    undiscounted = a.prem_ge_base(3) + a.prem_np_base(3) * a.reld_avg(3)
    assert undiscounted == pytest.approx(14374.6306, abs=WON)
    assert a.prem_gross_mth(3) < undiscounted


def test_pitfall_there_is_no_no_claims_ladder(kr_medical_anchor):
    """Pitfall: accumulating band state across years into a bonus-malus chain.

    「보험금 지급(사고) 이력이 1년마다 초기화됩니다」.  ``band_share(y, b)`` reads
    ``claims_np_rated_pp(y - 1)`` and nothing earlier, so a single bad year cannot compound
    into a permanently higher premium and a single clean year returns the policyholder to
    the discount band.  That memorylessness is what makes the loop tractable in a projection
    model at all, and a model that carried a ladder would invent a persistence the wording
    explicitly removes.
    """
    a = kr_medical_anchor
    for y in range(2, 11):
        level = a.claims_np_rated_pp(y - 1)
        for b in (1, 2, 3, 4, 5):
            expected = sum(a.shape_share(k) for k in a.shape_buckets()
                           if a.band_of(a.shape_rel(k) * level) == b)
            assert a.band_share(y, b) == pytest.approx(expected, rel=1e-14), (y, b)
    # Two years with the same prior-year claim level give the same mix, whatever came before.
    assert a.claims_np_rated_pp(6) < a.claims_np_rated_pp(7)
    assert [a.band_share(7, b) for b in (1, 2, 3, 4, 5)] == \
        [a.band_share(8, b) for b in (1, 2, 3, 4, 5)]
    assert a.band_share(1, 2) == 1.0, "year 1 has no prior year: everyone at 2단계"
    assert a.check_band_shares() is True


def test_pitfall_the_injection_carve_out_is_counted_once(kr_medical_anchor):
    """Pitfall: counting the 항암제·항생제·희귀의약품 injection carve-out twice.

    25% of the injection acts leave the ₩2,500,000 sub-limit for the main ₩50,000,000 limit,
    so ``acts_inject_eff(1) = 0.75 x 0.078898`` and the carved payment ₩2,390.6094 is added
    in ``claims_np_out_pp``, **not** in ``claims_np_three_pp``.  Double-counting it inflates
    the year-1 claim by 2.0%; forgetting the removal from ``acts_inject_eff`` deflates it by
    the same amount and puts the money under the wrong limit.
    """
    a = kr_medical_anchor
    assert a.inject_carve_share == 0.25
    assert a.acts_inject_eff(1) == pytest.approx(0.75 * a.act_rate_inject(1), rel=1e-14)
    carve = a.act_rate_inject(1) * 0.25 * a.paid_per_act("inject", 1.0)
    assert carve == pytest.approx(2390.6094, abs=WON)
    visits = a.visits_np_eff(1) * a.paid_out_per_visit("np_out", 30000.0, 0.30, 1.0)
    assert a.claims_np_out_pp(1) == pytest.approx(visits + carve, rel=1e-14)
    assert a.claims_inject_pp(1) == pytest.approx(
        a.acts_inject_eff(1) * a.paid_per_act("inject", 1.0), rel=1e-14)
    assert carve / a.claims_ann_pp(1) == pytest.approx(0.0201, abs=5e-5)
    # The whole injection frequency is accounted for exactly once, across the two limbs.
    assert a.acts_inject_eff(1) + a.act_rate_inject(1) * 0.25 == pytest.approx(
        a.act_rate_inject(1), rel=1e-14)


def test_pitfall_read_the_utilisation_table_at_the_attained_age(indemnity_medical):
    """Pitfall: freezing the utilisation band at the issue age.

    ``util_band(6) = 45`` and ``adm_rate(6) / adm_rate(5) = 1.2499293``.  Freezing the band
    at issue gives a year-6 claim of ₩150,937.05 against ₩183,428.50 — **17.71% low** — and
    turns the projection's only negative policy year into a comfortably positive one, which
    is the worst kind of error because it removes the one thing the projection had to say.
    The band step and the wording's 4% annual age loading agree to within 0.12%; they simply
    do not arrive at the same time, and that is what makes the loss ratio saw-tooth.
    """
    a = indemnity_medical.Projection[1]
    assert a.claims_ann_pp(6) == pytest.approx(183428.5019, abs=WON)
    table = indemnity_medical.Data.utilisation_table().reset_index()
    frozen = table.copy()
    row40 = frozen[(frozen["sex"] == "M") & (frozen["age_start"] == 40)].iloc[0]
    mask = (frozen["sex"] == "M") & (frozen["age_start"] == 45)
    for column in ("adm_rate", "los_days", "visit_rate_ge", "visit_rate_np",
                   "act_rate_physio", "act_rate_inject", "act_rate_mri"):
        frozen.loc[mask, column] = row40[column]
    with _swapped("frozen", "utilisation_table_file", frozen,
                  "utilisation_table_frozen.csv", index=False) as model:
        p = model.Projection[1]
        assert p.claims_ann_pp(6) == pytest.approx(150937.0485, abs=WON)
        assert p.claims_ann_pp(6) / a.claims_ann_pp(6) - 1.0 == pytest.approx(
            -0.1771, abs=5e-5)
        year6 = sum(p.net_cf(t) for t in range(60, 72))
        assert year6 > 0.0, "the frozen band hides the projection's only negative year"
    assert sum(a.net_cf(t) for t in range(60, 72)) == pytest.approx(-276.1354, abs=WON)
    step = a.claims_ann_pp(6) / 150937.0485
    assert step == pytest.approx(1.215265, abs=5e-7)
    assert step ** (1.0 / 5.0) == pytest.approx(1.0398, abs=5e-5)
    assert 1.04 ** 5 / step - 1.0 == pytest.approx(0.0011, abs=5e-4)


def test_pitfall_lapse_rate_is_annual_and_lapse_rate_mth_is_monthly(kr_medical_anchor):
    """Pitfall: using the annual lapse rate on the monthly grid.

    ``lapse_rate(0) = 0.10`` against ``lapse_rate_mth(0) = 0.0087416110``.  Using the annual
    rate month by month takes ``pols_if(12)`` from 0.8898237107 to about 0.28 — a third of
    the block gone in a year that should lose a tenth of it — and the library spells the two
    names apart for exactly this reason.
    """
    a = kr_medical_anchor
    assert a.lapse_rate(0) == 0.10
    assert a.lapse_rate_mth(0) == pytest.approx(LAPSE_MTH_0, abs=5e-11)
    assert a.lapse_rate_mth(0) == pytest.approx(
        1.0 - 0.90 ** (1.0 / 12.0), rel=1e-14)
    assert (1.0 - a.lapse_rate_mth(0)) ** 12 == pytest.approx(0.90, rel=1e-13)
    assert a.pols_if(12) == pytest.approx(0.8898237107, abs=INFORCE)
    wrong = (1.0 - MORT_MTH_0) ** 12 * (1.0 - 0.10) ** 12 * (1.0 - 0.01)
    assert wrong == pytest.approx(0.28, abs=0.005)
    assert wrong < 0.32 * a.pols_if(12)
    assert a.mort_rate(0) == 0.00132019
    assert a.mort_rate_mth(0) == pytest.approx(
        1.0 - (1.0 - 0.00132019) ** (1.0 / 12.0), rel=1e-14)


def test_pitfall_the_renewal_decline_is_not_lapse(kr_medical_anchor):
    """Pitfall: folding the renewal decline into the lapse rate.

    It is non-zero **only** where ``(t + 1) mod 12 = 0``, it acts **after** mortality, lapse
    and suspension, and it is the **larger** of the two voluntary exits at every annual
    boundary — 0.0089881183 against 0.0079263524 at ``t = 11``, and 0.0083529502 against
    0.0043181413 at ``t = 23``.  ``check_pols_roll_fwd()`` balances either way, so the
    roll-forward will not catch it: on a contract whose whole architecture is annual, folding
    it into ``w(t)`` makes invisible the boundary the model exists to show.
    """
    a = kr_medical_anchor
    assert a.pols_renewal_decline(11) == pytest.approx(0.0089881183, abs=INFORCE)
    assert a.pols_lapse(11) == pytest.approx(0.0079263524, abs=INFORCE)
    assert a.pols_renewal_decline(23) == pytest.approx(0.0083529502, abs=INFORCE)
    assert a.pols_lapse(23) == pytest.approx(0.0043181413, abs=INFORCE)
    for t in range(a.proj_len()):
        if (t + 1) % 12:
            assert a.pols_renewal_decline(t) == 0.0, t
        else:
            assert a.pols_renewal_decline(t) > a.pols_lapse(t), t
    assert a.renewal_decline_rate == 0.01
    total_decline = sum(a.pols_renewal_decline(t) for t in range(a.proj_len()))
    total_lapse = sum(a.pols_lapse(t) for t in range(a.proj_len()))
    total_death = sum(a.pols_death(t) for t in range(a.proj_len()))
    assert total_decline == pytest.approx(0.072409, abs=5e-7)
    assert total_lapse == pytest.approx(0.315540, abs=5e-7)
    assert total_death == pytest.approx(0.011647, abs=5e-7)
    assert total_death < total_decline < total_lapse


def test_pitfall_the_three_named_classes_never_pass_through_the_annual_limit_factor(
        indemnity_medical, kr_medical_anchor):
    """Pitfall: pushing the 3대비급여 limbs through the ₩50,000,000 aggregate.

    Their money caps **replace** the aggregate for those three classes rather than sitting
    inside it, so ``claims_np_three_pp(y)`` is summed apart from ``claims_np_main_pp(y)`` and
    ``np_limit_factor(y)`` is applied only to the latter.  And where 3대비급여형 is not held
    those treatments are **uncovered** — they do not fall back into the main limit.  Model
    point 6 is that election.
    """
    a = kr_medical_anchor
    for y in (1, 6, 10):
        assert a.claims_ann_pp(y, "NP_THREE") == a.claims_np_three_pp(y)
        assert a.claims_ann_pp(y, "NP_IN") == pytest.approx(
            a.claims_np_in_pp(y) * a.np_limit_factor(y), rel=1e-14)
        assert a.claims_np_pp(y) == pytest.approx(
            a.claims_np_main_pp(y) + a.claims_np_three_pp(y), rel=1e-14)
        raw = a.claims_np_in_pp(y) + a.claims_np_out_pp(y)
        capped = min(a.share_injury * raw, a.annual_limit()) \
            + min((1.0 - a.share_injury) * raw, a.annual_limit())
        assert a.np_limit_factor(y) == pytest.approx(capped / raw, rel=1e-14)
    p6 = indemnity_medical.Projection[6]
    assert p6.np_rider() is True and p6.three_np() is False
    for y in range(1, 11):
        assert p6.claims_np_three_pp(y) == 0.0
        assert p6.claims_physio_pp(y) == 0.0
        assert p6.claims_inject_pp(y) == 0.0
        assert p6.claims_mri_pp(y) == 0.0
        # Uncovered, not reassigned: the main limb carries no carve-out either.
        assert p6.claims_np_out_pp(y) == pytest.approx(
            p6.visits_np_eff(y) * p6.paid_out_per_visit(
                "np_out", 30000.0, p6.retain_rate_np(), p6.trend_np(y)), rel=1e-14)
    df6 = p6.result_cf()
    assert (df6["claims_np_three"] == 0.0).all()
    assert (df6["claims_np_out"] > 0.0).all()


def test_pitfall_the_rating_exemption_reduces_the_rating_count_never_the_benefit(
        kr_medical_anchor):
    """Pitfall: applying ``reld_exempt_share`` to the claim instead of to the rating count.

    ``claims_np_pp(1) = 62,978.2477`` is paid **in full**; ``claims_np_rated_pp(1) = 0.85 x
    62,978.2477 = 53,531.5106`` is only what the band is read against.  The severely ill —
    산정특례 conditions and insureds graded 장기요양 1·2등급 — are exempt from the **rating**,
    not from the cover, and applying the 15% to the claim would silently delete a fifteenth
    of the benefit.
    """
    a = kr_medical_anchor
    assert a.reld_exempt_share == 0.15
    assert a.claims_np_pp(1) == pytest.approx(62978.2477, abs=WON)
    assert a.claims_np_rated_pp(1) == pytest.approx(
        0.85 * a.claims_np_pp(1), rel=1e-14)
    assert a.claims_np_rated_pp(1) == pytest.approx(53531.5106, abs=WON)
    # The benefit the cash flow statement pays is the unrated figure, on every year.
    for y in range(1, 11):
        paid = a.claims_ann_pp(y, "NP_IN") + a.claims_ann_pp(y, "NP_OUT") \
            + a.claims_ann_pp(y, "NP_THREE")
        assert paid == pytest.approx(a.claims_np_pp(y), rel=1e-12), y
        assert a.claims_np_rated_pp(y) < paid


def test_pitfall_the_room_cap_is_a_daily_average_not_a_nightly_cap(kr_medical_anchor):
    """Pitfall: applying the 상급병실료 cap per night instead of to the daily average.

    ``min(0.50 x charge, ₩100,000 x D)`` with ``D`` the whole admission's length, so a single
    expensive night inside a long stay is smoothed against the stay rather than capped — a
    materially more generous treatment than a nightly cap.  On the anchor the room payment is
    ₩135,000 over 7.5 days, ₩18,000 a day against a ₩100,000 cap, and the largest capped
    point 0.50 x ₩1,200,000 = ₩600,000 sits below the ₩750,000 stay cap, so the cap is slack
    by a factor of 5.6 and the whole 50% is paid.
    """
    a = kr_medical_anchor
    assert a.room_rate == 0.50 and a.room_cap_day == 100000.0
    assert a.los_days(1) == 7.5
    stay_cap = a.room_cap_day * a.los_days(1)
    assert stay_cap == 750000.0
    room = sum(p * min(0.50 * c, stay_cap) for c, p in a.sev_points("np_room"))
    assert room == pytest.approx(135000.0, abs=WON)
    assert room == pytest.approx(0.50 * a.sev_mean("np_room"), rel=1e-14)   # nothing capped
    assert max(0.50 * c for c, _ in a.sev_points("np_room")) == 600000.0 < stay_cap
    assert room / a.los_days(1) == pytest.approx(18000.0, abs=WON)
    assert a.room_cap_day / (room / a.los_days(1)) == pytest.approx(5.56, abs=0.01)
    # The length of stay enters the model here and only here.
    assert a.claims_np_in_pp(1) == pytest.approx(
        a.adm_rate(1) * (a.sev_mean("np_in") * 0.70 + room), rel=1e-14)


def test_pitfall_do_not_delete_a_limit_because_it_reads_slack(indemnity_medical):
    """Pitfall: deleting a contractual limit because it never binds on the shipped table.

    ``check_annual_limits()`` is True on every shipped model point because
    ``E[min(X, L)] != min(E[X], L)`` and a single cell's expected annual claim is two orders
    of magnitude below every money limit.  The check proves the machinery is **wired**, not
    that it is **exercised** — every one of those limits binds under a seriatim or stochastic
    run, and the References that carry them must survive.
    """
    refs = indemnity_medical.Projection.refs
    for name in ("cap_inpatient_retain", "limit_physio", "limit_inject", "limit_mri",
                 "visit_limit_np", "act_limit_three", "physio_gate_acts",
                 "room_cap_day"):
        assert name in refs, f"{name} is a contractual limit and must not be dropped"
    a = indemnity_medical.Projection[1]
    headroom = {
        "annual aggregate, 급여": 2 * a.annual_limit() / a.claims_ge_pp(1),
        "annual aggregate, 비급여": 2 * a.annual_limit() / a.claims_np_main_pp(1),
        "3대비급여 physio": a.limit_physio / a.claims_physio_pp(1),
        "3대비급여 inject": a.limit_inject / a.claims_inject_pp(1),
        "3대비급여 MRI": a.limit_mri / a.claims_mri_pp(1),
    }
    for name, ratio in headroom.items():
        assert ratio > 100.0, f"{name} is closer to binding than the notes state"
    assert a.visit_limit_np / a.visits_np_eff(1) > 400.0
    assert a.act_limit_three / a.acts_physio_eff(1) > 500.0


def test_pitfall_no_claims_subtotal_column_beside_the_splits(indemnity_medical):
    """Pitfall: publishing a ``claims`` subtotal column beside the five split ones.

    The printed columns must sum to ``net_cf`` with the three expense limbs, which is what
    ``check_net_cf()`` asserts; a subtotal beside the splits invites a limb being counted
    twice invisibly.  The ``claims(t, kind)`` cells stays, and ``claims(t)`` with no ``kind``
    is the sum — the aggregate lives in the cells, not in the frame.
    """
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        df = p.result_cf()
        assert "claims" not in df.columns
        assert [c for c in df.columns if c.startswith("claims_")] == [
            "claims_ge_in", "claims_ge_out", "claims_np_in", "claims_np_out",
            "claims_np_three"]
        assert "claim_expenses" in df.columns
        for t in (0, 60, p.proj_len() - 1):
            assert p.claims(t) == pytest.approx(
                sum(p.claims(t, k) for k in ("GE_IN", "GE_OUT", "NP_IN", "NP_OUT",
                                             "NP_THREE")), rel=1e-14)
    with pytest.raises(Exception):
        indemnity_medical.Projection[1].claims(0, "DEATH")


def test_pitfall_expenses_is_maintenance_only_and_claim_expenses_is_claim_driven(
        indemnity_medical, kr_medical_anchor):
    """Pitfall: folding claim handling into ``expenses``, or charging it on premium.

    7% of premium and 3% of **claims** respectively, on a [std] split of one published 16.1%
    aggregate.  Folding them together makes a premium-driven cost and a claim-driven cost
    move as one, and it breaks the two-term identity ``net_cf = 0.87 x premiums - 1.03 x
    claims`` that the whole shape of this projection rests on — the identity that puts the
    model's own break-even loss ratio at 84.466% just below the FSS's stated 「약 85% 수준」.
    """
    a = kr_medical_anchor
    refs = indemnity_medical.Projection.refs
    assert refs["expense_maint_rate"] == 0.07
    assert refs["expense_claim_rate"] == 0.03
    assert refs["comm_rate"] == 0.06
    assert refs["expense_total_rate"] == 0.16
    assert a.check_expense_split() is True
    assert a.check_expense_split_resid() == pytest.approx(0.0, abs=1e-15)
    for t in (0, 11, 60, 119):
        assert a.expenses(t) == pytest.approx(0.07 * a.premiums(t), rel=1e-14)
        assert a.commissions(t) == pytest.approx(0.06 * a.premiums(t), rel=1e-14)
        assert a.claim_expenses(t) == pytest.approx(0.03 * a.claims(t), rel=1e-14)
        assert a.net_cf(t) == pytest.approx(
            0.87 * a.premiums(t) - 1.03 * a.claims(t), abs=1e-9)
    assert BREAK_EVEN_LR == pytest.approx(0.8446601942, abs=5e-11)
    # The claim expense does not track the premium: policy year 6 is where they part.
    df = a.result_cf()
    y5 = df.loc[48:59]
    y6 = df.loc[60:71]
    assert y6["premiums"].sum() > y5["premiums"].sum()
    assert y6["claim_expenses"].sum() / y5["claim_expenses"].sum() > \
        y6["expenses"].sum() / y5["expenses"].sum()


def test_pitfall_there_is_no_acquisition_strain_and_inventing_one_is_as_wrong(
        indemnity_medical, kr_medical_anchor):
    """Pitfall: expecting — or inventing — the sister libraries' month-0 trough.

    On a one-year renewable contract renewed on a rolling basis the acquisition/renewal
    distinction has no content after year one, so ``commissions(t) = 0.06 x premiums(t)`` is
    level and ``t = 0`` is **positive at ₩205.4984**.  A reader who expects a strain will
    look for a bug that is not there; a modeller who books one will invent a cost the
    contract does not have.
    """
    a = kr_medical_anchor
    assert a.net_cf(0) == pytest.approx(205.4984, abs=WON)
    assert all(a.net_cf(t) > 0.0 for t in range(0, 12))
    names = set(indemnity_medical.Projection.cells) | set(
        indemnity_medical.Projection.refs)
    for absent in ("expense_acq", "comm_init_rate", "comm_init_pp", "acq_expense",
                   "expense_acq_pp", "comm_new_term_rate"):
        assert absent not in names, f"{absent} would invent an acquisition strain"
    for point_id in indemnity_medical.Data.model_point_table().index:
        p = indemnity_medical.Projection[point_id]
        rates = {p.commissions(t) / p.premiums(t) for t in (0, 1, 12, 60, 119)}
        assert max(rates) - min(rates) < 1e-12, point_id


def test_pitfall_the_two_age_conventions_are_both_real(indemnity_medical):
    """Pitfall: silently collapsing 만나이 and 보험나이 into one age.

    The model runs on **만나이** and the contract prices on **보험나이**; the two differ for
    half of all issue dates, so half a year of age sits between the projection basis and the
    pricing basis.  The registry records the basis per model and the Projection docstring has
    to name it, so that a 만나이 model point read against a 보험나이 rate table is a visible
    mismatch rather than an invisible one.
    """
    assert MODELS["Medical_KR_S"][1]["age_basis"] == "만나이"
    assert MODELS["Medical_KR_S"][1]["grid"] == "monthly"
    doc = _flat(indemnity_medical.Projection.doc)
    assert "만나이" in doc and "보험나이" in doc
    assert "The two differ for half of all issue dates" in doc
    a = indemnity_medical.Projection[1]
    assert a.issue_age() == 40
    assert a.age(0) == 40 and a.age(11) == 40 and a.age(12) == 41
    assert a.age(t=59) == 44 and a.age(t=60) == 45


def test_pitfall_the_premium_is_an_input_for_policy_year_one_only(kr_medical_anchor):
    """Pitfall: re-reading the model point premium in every policy year.

    ``premium_mth_pp()`` seeds ``prem_ge_base(1) + prem_np_base(1)`` and nothing else; every
    later year is the renewal recursion.  A model that re-read the input would throw the
    whole renewal machinery away and, on this cell, collect ₩1,066,375.5027 of premium over
    the 120 months instead of ₩1,558,165.4328 — 31.6% less — while leaving the claim
    untouched, which turns a +₩118,476 result into a loss of about ₩309,381.
    """
    a = kr_medical_anchor
    assert a.premium_mth_pp() == 11982.0
    assert a.prem_ge_base(1) + a.prem_np_base(1) == pytest.approx(11982.0, rel=1e-14)
    assert a.prem_ge_base(1) == pytest.approx(11982.0 * 0.40, rel=1e-14)
    assert a.prem_np_base(1) == pytest.approx(11982.0 * 0.60, rel=1e-14)
    assert a.prem_gross_mth(1) == 11982.0
    for y in range(2, 11):
        assert a.prem_gross_mth(y) != pytest.approx(11982.0, abs=1.0)
    df = a.result_cf()
    frozen_premiums = 11982.0 * df["pols_if"].sum()
    assert frozen_premiums == pytest.approx(1066375.5027, abs=WON)
    assert df["premiums"].sum() == pytest.approx(1558165.4328, abs=WON)
    assert frozen_premiums / df["premiums"].sum() - 1.0 == pytest.approx(
        -0.316, abs=5e-4)
    claims = df[[c for c in df.columns if c.startswith("claims_")]].sum().sum()
    frozen_net = frozen_premiums - claims - 0.07 * frozen_premiums \
        - 0.03 * claims - 0.06 * frozen_premiums
    assert frozen_net == pytest.approx(-309381.0, abs=1.0)
    assert df["net_cf"].sum() > 0.0 > frozen_net


# ---------------------------------------------------------------------------
# The [std] parameters, the elections, and the shipped table


def test_the_contractual_scalars_are_the_wordings_own_numbers(indemnity_medical):
    """Every scalar that is a clause of the 표준약관, read off the model's References.

    **This product's benefit half reaches a citation precision no other product in this
    repository reaches**, because its benefit definition is a piece of published subordinate
    legislation — the 표준약관 annexed to the 보험업감독업무시행세칙 at 별표 15 — rather than
    a carrier document.  So these are not [std]: they are the supervisor's text, and a
    silent change to one of them is a change to the contract rather than to an assumption.
    """
    refs = indemnity_medical.Projection.refs
    for name, value in CONTRACTUAL_SCALARS.items():
        assert name in refs, f"{name} is no longer a Reference"
        assert refs[name] == pytest.approx(value, rel=1e-15), name
    # The two co-payment rates are the generation's design statement and must not be equal.
    assert refs["retain_rate_ge_base"] < refs["retain_rate_np_base"] \
        < refs["retain_rate_nonhi"]
    # The band thresholds are a strictly increasing money ladder with flat relativities.
    assert refs["band_thr_3"] < refs["band_thr_4"] < refs["band_thr_5"]
    assert [refs["reld_r2"], refs["reld_r3"], refs["reld_r4"], refs["reld_r5"]] == \
        [1.0, 2.0, 3.0, 4.0]
    assert refs["ded_clinic"] < refs["ded_hospital"] < refs["ded_np_out"]


def test_the_std_scalar_assumptions_the_notes_state(indemnity_medical):
    """Every [std] scalar the notes tabulate, read off the model's References.

    The house rule is that every quantitative parameter is source-tagged or marked [std], and
    the notes carry each of these with its tag and its rationale.  Pinning them means a
    silent change to an assumption fails a **named** test rather than moving a golden and
    looking like an arithmetic problem.  Two of them carry the whole re-rating —
    ``med_trend_ge`` and ``med_trend_np``, one year's national growth rates — and one of them,
    ``reld_disc_cap``, is the single assumption with the largest effect on the loop's
    aggregate behaviour and has two published anchors and no observed range.
    """
    refs = indemnity_medical.Projection.refs
    for name, value in STD_SCALARS.items():
        assert name in refs, f"{name} is no longer a Reference"
        assert refs[name] == pytest.approx(value, rel=1e-15), name
    assert refs["med_trend_np"] > refs["med_trend_ge"] * 8.0, \
        "비급여 compounds at many times the covered co-payment's rate"
    assert 0.0 < refs["reld_disc_cap"] < 1.0
    assert refs["reld_start_year"] == 4              # the three-year deferral to 2024-07
    assert refs["reentry_cycles"] * refs["reentry_period"] == 10
    assert refs["comm_rate"] + refs["expense_maint_rate"] + refs["expense_claim_rate"] \
        == pytest.approx(refs["expense_total_rate"], abs=1e-15)
    # The corridor and the age loading compose: the wording admits 1.30 a year on a unit.
    assert (1.0 + refs["renewal_corridor"]) * (1.0 + refs["age_load"]) == \
        pytest.approx(1.30, rel=1e-14)


def test_the_std_input_tables_mark_their_own_provenance():
    """Every row of every input CSV says where it came from.

    Six of the seven tables are [std] constructions and the seventh —
    ``oop_ceiling_table.csv`` — is a transcription of a published number, and the difference
    has to be legible on the row rather than inferred from the file name.  The reason the
    morbidity basis is [std] is a **positive finding** rather than a failed retrieval:
    보험개발원 is the statutory 요율 산출기관 and 실손의료보험 is not among the categories
    whose 참조순보험요율 it publishes, and the 산출방법서 is a filed and undisclosed
    기초서류, so there is no public Korean indemnity-medical morbidity or severity basis at
    all.
    """
    for name in ("mort_table.csv", "lapse_table.csv", "utilisation_table.csv",
                 "severity_table.csv", "claim_shape_table.csv",
                 "oop_ceiling_table.csv"):
        frame = pd.read_csv(CSV_DIR / name)
        assert "provenance" in frame.columns, name
        assert frame["provenance"].notna().all(), name
        assert (frame["provenance"].str.len() > 20).all(), name
    for name in ("utilisation_table.csv", "severity_table.csv",
                 "claim_shape_table.csv", "lapse_table.csv"):
        frame = pd.read_csv(CSV_DIR / name)
        assert frame["provenance"].str.contains(r"\[std\]").any(), name
    ceilings = pd.read_csv(CSV_DIR / "oop_ceiling_table.csv")
    assert ceilings["provenance"].str.contains(r"\[R10\]").all()
    assert not ceilings["provenance"].str.contains(r"\[std\]").any()
    mort = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert mort["provenance"].str.contains(r"\[REG-R38\]").any()
    assert mort["provenance"].str.contains(r"\[std\]").all()


def test_the_shipped_mortality_runs_the_wrong_way_and_the_table_says_so(
        indemnity_medical, kr_medical_anchor):
    """Death **releases** this liability, so overstating mortality is anti-conservative.

    The reverse of every protection product in this library, and it is worth an assertion
    rather than a sentence: raise the mortality basis and the projected result **improves**,
    because the contract pays nothing on death beyond the 미경과보험료 and the exposure that
    dies takes its claims with it.  There is no ``claims_death`` anywhere in the model.
    """
    a = kr_medical_anchor
    assert a.mort_rate(0) == pytest.approx(MORT_Q[40], rel=1e-14)
    names = set(indemnity_medical.Projection.cells)
    assert "claims_death" not in names and "claims_lapse" not in names
    assert "cv_pp" not in names and "av_pp" not in names
    doubled = indemnity_medical.Data.mort_table().copy()
    doubled["mort_rate"] = doubled["mort_rate"] * 5.0
    with _swapped("mort", "mort_table_file", doubled,
                  "mort_table_x5.csv") as model:
        p = model.Projection[1]
        assert p.mort_rate(0) == pytest.approx(5.0 * MORT_Q[40], rel=1e-12)
        assert p.pols_if(119) < a.pols_if(119)
        base = a.result_cf()
        stressed = p.result_cf()
        assert stressed["premiums"].sum() < base["premiums"].sum()
        claim_cols = [c for c in base.columns if c.startswith("claims_")]
        assert stressed[claim_cols].sum().sum() < base[claim_cols].sum().sum()
        assert p.check_pols_roll_fwd() is True


def test_the_model_point_table_exercises_the_product(indemnity_medical):
    """Both sexes, the age envelope, every 보장종목 election and every optional module.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.  Model point 1 is the worked example's
    anchor and the rest are the elections: the 급여-only contract, 3대비급여형 not held, the
    lower 보험가입금액 rung where the per-visit cap binds, the top-decile user on the lowest
    본인부담상한액, 개인실손 중지 with the relativity off, and the 40% non-NHI branch under a
    cost-trend stress that makes the corridor clip.
    """
    table = indemnity_medical.Data.model_point_table()
    assert len(table) == 10 and list(table.index) == list(range(1, 11))
    assert set(table["sex"]) == {"M", "F"}
    assert table["issue_age"].min() == 0 and table["issue_age"].max() == 65
    for module in ("np_rider", "three_np", "nhi_covered", "reld_on", "noclaim_on"):
        assert set(table[module]) == {0, 1}, f"{module} is not exercised both ways"
    assert set(table["annual_limit"]) == {50000000, 10000000}
    assert set(table["visit_cap"]) == {200000, 100000}
    assert table["oop_decile"].min() == 1 and table["oop_decile"].max() == 8
    assert set(table["util_mult"]) == {1.0, 10.0}
    assert set(table["trend_mult"]) == {1.0, 4.5}
    assert set(table["suspend_rate"]) == {0.0, 0.03}
    assert table.loc[1, "label"].startswith("anchor")
    for point_id in table.index:
        p = indemnity_medical.Projection[point_id]
        assert p.proj_len() == 120
        df = p.result_cf()
        assert len(df) == 120 and not df.isna().any().any()


def test_the_elections_do_what_the_notes_say_they_do(indemnity_medical):
    """The optional modules, in both positions, on the points that carry them.

    Model point 5 removes the rider and with it 60% of the premium, the 100-visit cap, the
    three sub-limits **and the whole loop** — the contract becomes the plain attained-age
    renewable that 1세대 through 3세대 were.  Model point 9 runs 개인실손 중지 at 3% a year
    as a decrement rather than a state, because the contract that resumes is a different
    projection.  Model point 10 is the 40% branch, where both retentions rise to 60% and the
    본인부담상한제 is switched off because a life outside the scheme is not refunded by it.
    """
    p5 = indemnity_medical.Projection[5]
    assert p5.np_rider() is False and p5.three_np() is False
    assert p5.reld_on() is False and p5.noclaim_on() is False
    assert p5.np_share() == 0.0
    for y in range(1, 11):
        assert p5.prem_np_base(y) == 0.0
        assert p5.claims_np_pp(y) == 0.0
        assert p5.reld_avg(y) == 1.0 and p5.noclaim_share(y) == 0.0
        assert p5.prem_gross_mth(y) == pytest.approx(p5.prem_ge_base(y), rel=1e-14)
        assert p5.loss_incurred_pp(y) == pytest.approx(
            p5.oop_incurred_ge(y) * p5.oop_trunc(y), rel=1e-14)
    df5 = p5.result_cf()
    assert (df5[["claims_np_in", "claims_np_out", "claims_np_three"]] == 0.0).all().all()

    p9 = indemnity_medical.Projection[9]
    assert p9.suspend_rate() == 0.03
    assert p9.suspend_rate_mth(0) == pytest.approx(
        1.0 - 0.97 ** (1.0 / 12.0), rel=1e-14)
    assert sum(p9.pols_suspend(t) for t in range(p9.proj_len())) > 0.0
    assert p9.reld_on() is False and p9.noclaim_on() is False
    assert p9.check_pols_roll_fwd() is True

    p10 = indemnity_medical.Projection[10]
    assert p10.nhi_covered() is False
    assert p10.retain_rate_ge() == 0.60 and p10.retain_rate_np() == 0.60
    assert p10.oop_ceiling() == float("inf")
    for y in range(1, 11):
        assert p10.oop_trunc(y) == 1.0
        assert p10.check_oop_ceiling_resid(y) == 0.0
    df10 = p10.result_cf()
    claim_cols = [c for c in df10.columns if c.startswith("claims_")]
    ten_year_lr = df10[claim_cols].sum().sum() / df10["premiums"].sum()
    assert ten_year_lr == pytest.approx(0.5756, abs=5e-4)
    assert p10.claims_ann_pp(1) / (p10.prem_gross_mth(1) * 12.0) == pytest.approx(
        0.5333, abs=5e-4)
    assert p10.claims_ann_pp(10) / (p10.prem_gross_mth(10) * 12.0) == pytest.approx(
        0.5913, abs=5e-4)


def test_an_input_can_be_swapped_without_touching_formulas(indemnity_medical):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a user with company
    experience does: a same-schema CSV drops in with no formula change.  On this product it
    is the whole answer to the basis being [std] — six of the seven tables are constructions
    and every one of them is meant to be replaced.
    """
    base = indemnity_medical.Projection[1].claims_ge_out_pp(1)
    severity = indemnity_medical.Data.severity_table().reset_index()
    doubled = severity["stream"] == "ge_out"
    severity.loc[doubled, "cost"] = severity.loc[doubled, "cost"] * 2.0
    with _swapped("sev", "severity_table_file", severity,
                  "severity_table_alt.csv", index=False) as model:
        p = model.Projection[1]
        assert p.sev_mean("ge_out") == pytest.approx(2 * 36100.0, rel=1e-12)
        assert p.claims_ge_out_pp(1) > base
        assert p.check_indemnity() is True
    assert indemnity_medical.Projection[1].claims_ge_out_pp(1) == pytest.approx(
        base, rel=1e-14)


def test_the_docstrings_carry_this_products_own_reference_material(indemnity_medical):
    """The model and both Spaces document what this product is, not a generic chassis.

    A reader holding the technical notes beside the model has to be able to cross-walk the
    notes' compact symbols to the cells names, and the ``Projection`` docstring's mapping
    table is where that happens.  The model docstring has to say that the inputs are
    external and read once per model, and the ``Data`` docstring has to name the lifelib
    layout it follows.
    """
    model_doc = _flat(indemnity_medical.doc)
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "Data", "Projection"):
        assert phrase in model_doc, phrase
    assert "실손의료보험" in model_doc and "비급여 할인·할증" in model_doc
    data_doc = _flat(indemnity_medical.Data.doc)
    for phrase in ("TradLife_A", "input_dir", "model_point_table"):
        assert phrase in data_doc, phrase
    proj_doc = _flat(indemnity_medical.Projection.doc)
    for phrase in ("Notes symbol", "proj_len", "model_point", "claims_np_rated_pp",
                   "reld_solved", "oop_trunc", "본인부담상한제", "위험구분단위"):
        assert phrase in proj_doc, phrase
    for name in sorted(indemnity_medical.Projection.cells):
        doc = indemnity_medical.Projection.cells[name].doc
        assert doc and doc.strip(), f"{name} has no docstring"
