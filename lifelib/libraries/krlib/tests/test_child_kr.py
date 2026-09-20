"""Golden and structural tests for Child_KR_S.

The golden values are the worked example in
products/child/technical-notes.md ("Worked example"), which projects the anchor cell
CH-KR-0001: a **태아가입** contract priced male because the sex is not known at issue,
계약나이 0 at the 계약일, **birth at policy month 5**, 보험기간 to the 100세 계약해당일
(the terminal index ``n = proj_len() - 1 = 1200``, so ``proj_len() == 1201`` rows on a
0-based frame ``t = 0 … 1200``), 20년납 (``m = 240``), 월납, 표준형, both premium waivers
on, the 계약자
male 만 33, and an office premium of KRW 31,000 a month to ``t = 16`` and KRW 28,000 from
``t = 17`` to ``t = 239``.  They are hard-coded here rather than pickled so that a
reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the four decimals the cash
flow statement prints, in-force counts and the decrement rates to the ten decimals of
``result_pols()``, mortality to the eight of its own column, and the hand traces to full
double precision, because that is how the notes print them.

**What this module is about is the two mechanics that have no counterpart in any sister
library.**  The diagnosis machinery — the tier ladder, the 면책기간, the 감액기간, the
유사암 tier, the 최초 1회한 ledgers — belongs to ``Cancer_KR_S``, this library's
fixed-benefit (정액) 제3보험 chassis, and is asserted there rather than here, except where
this product switches it off.  What is new is that the contract is written **before the
insured exists**, so the projection opens on a life with no age, no mortality and no
morbidity and a **void** decrement instead of a lapse; and that the premium stops on a
**decrement drawn from a life who is not the insured**, the 계약자, so the in-force block
runs in two compartments and the premium stream ends on the earlier of two events read out
of two different rows of one mortality table.  Almost every test below is a statement about
one of those two.

Every product fact the notes list under "Known modeling pitfalls" earns its own test,
named after the pitfall, because each of them is a way an implementation can look right
and be wrong:

* cover attaches at **birth**, not at the 계약일, and the insured's mortality with it;
* the pre-birth void is **not** a lapse — nothing is retained and both streams come back;
* 보험나이 and 만나이 differ by exactly ``b`` months for the life of the contract;
* the two ``hosp_*`` causes are **days**, so the monthly conversion is not even real;
* the 면책기간 is decided at the **계약일** and never re-tested;
* a 태아 contract carries no 감액 whatever the model point says;
* the child's waiver limb does not run over the 신생아 block — the P코드 carve-out;
* the parent is a **decrement**, not a benefit, and the two are not interchangeable;
* the waiver stops at 납입완료, and the waived cohort is not exposed to lapse;
* the 기본계약 is 보험가입금액 × 장해지급률, not a lump sum — a factor of 8.3;
* the ``frac_open`` ledgers are per policy, never weighted by ``pols_if``;
* renewal commission runs ``12 <= t <= 239`` and nowhere else;
* there is no 만기환급금, and the account does not start at the surrender charge;
* [별표 15] 제9호 is evaluated at 남자 만 40세 and not at the insured's own age;
* there are **four** exits, not two;
* the incidence grid is graduated log-linearly and returns its pivots exactly;
* the sex relativity has no fixed sign, so the male-rate convention implies no refund; and
* the displayed rows are rounded and the totals are not, so they do not re-add.

The thirteen ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep cannot notice a check that has quietly disappeared; that they are *true* on
every shipped model point is asserted once, in ``test_model_conventions_kr.py``, whose
sweep discovers them generically.  The optional modules are asserted in **both** positions
of their switch, and the [std] scalar assumptions the notes state are read off the model
and off the input tables, so that a silent change to an assumption fails a test rather
than moving a result somewhere else in this module.
"""
import io
import math
import re
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

MODEL_DIR = LIB / MODELS["Child_KR_S"][0]
CSV_DIR = MODEL_DIR.parent

WON = 0.005          # money displayed to 2 d.p.
CASH = 5e-5          # money displayed to 4 d.p., the statement's own precision
INFORCE = 5e-11      # counts displayed to 10 d.p.
RATE = 5e-11         # lapse_rate and waiver_rate, displayed to 10 d.p.
MORT = 5e-9          # mort_rate, displayed to 8 d.p.
TRACE = 1e-12        # relative, for the hand traces printed at full precision


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


def edited_model(tmp_path, name, edits):
    """A private copy of the model and its inputs, with the model point table edited.

    Inputs are external files, so a copy of the model folder alone is not a model: the
    CSVs must travel with it.  Copying both and editing one cell of
    ``model_point_table.csv`` is how a switch the shipped table does not exercise — a
    감액 on a 태아 contract, an invalid enumeration — can be tested without touching the
    shipped inputs.
    """
    dest = tmp_path / MODEL_DIR.name
    shutil.copytree(MODEL_DIR, dest)
    for csv in CSV_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)
    table = pd.read_csv(tmp_path / "model_point_table.csv", index_col="point_id")
    for (point_id, column), value in edits.items():
        table.loc[point_id, column] = value
    table.to_csv(tmp_path / "model_point_table.csv")
    return mx.read_model(dest, name=name)


# ---------------------------------------------------------------------------
# The notes' worked example, hard-coded
#
# "The first eighteen policy months": result_cf() rows t = 0 .. 17.
# t: (pols_if,
#     premiums, claims_disability, claims_diagnosis, claims_surgery, claims_hospital,
#     claims_event, claims_liability, claims_neonatal,
#     claims_death, claims_lapse, claims_maturity, claims_void,
#     claim_expenses, expenses, commissions, net_cf)
WORKED_EXAMPLE_CF = {
     0: (1.0000000000,
         31000.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 66.0413, 0.0000, 0.0000, 30.1663, 116610.0000, 212940.0000,
         -298646.2076),
     1: (0.9947337283,
         30834.5604, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 64.6018, 0.0000, 31.0077, 30.0074, 1940.2787, 0.0000,
         28768.6648),
     2: (0.9895656205,
         30672.1777, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 63.1986, 0.0000, 61.6931, 29.8515, 1930.7437, 0.0000,
         28586.6907),
     3: (0.9844932382,
         30512.7761, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 61.8306, 0.0000, 92.0653, 29.6985, 1921.3905, 0.0000,
         28407.7911),
     4: (0.9795142152,
         30356.2821, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 60.4968, 0.0000, 122.1330, 29.5483, 1912.2146, 0.0000,
         28231.8894),
     5: (0.9746262555,
         30202.6242, 414.8570, 185.1917, 70.8281, 7472.1346, 227.9207, 195.2835,
         50960.7703,
         24.4953, 59.2432, 0.0000, 0.0000, 47.4875, 1903.2117, 0.0000,
         -31358.7996),
     6: (0.9706008315,
         30075.7076, 413.1436, 184.4245, 70.5346, 7441.2730, 226.9793, 194.4770,
         5132.0519,
         28.6453, 58.0199, 0.0000, 0.0000, 47.2914, 1895.8889, 0.0000,
         14382.9781),
     7: (0.9666551736,
         29951.2731, 411.4641, 183.6725, 70.2469, 7411.0230, 226.0566, 193.6864,
         5111.1892,
         32.7629, 56.8258, 0.0000, 0.0000, 47.0991, 1888.7182, 0.0000,
         14318.5284),
     8: (0.9627873748,
         29829.2615, 409.8177, 182.9353, 69.9649, 7381.3699, 225.1521, 192.9114,
         5090.7382,
         36.8488, 55.6602, 0.0000, 0.0000, 46.9107, 1881.6959, 0.0000,
         14255.2563),
     9: (0.9589955828,
         29709.6152, 408.2037, 182.2126, 69.6884, 7352.2995, 224.2654, 192.1516,
         5070.6891,
         40.9041, 54.5223, 0.0000, 0.0000, 46.7259, 1874.8187, 0.0000,
         14193.1339),
    10: (0.9552779980,
         29592.2781, 406.6213, 181.5040, 69.4173, 7323.7980, 223.3960, 191.4068,
         5051.0324,
         44.9297, 53.4112, 0.0000, 0.0000, 46.5448, 1868.0831, 0.0000,
         14132.1337),
    11: (0.9516328712,
         29477.1960, 405.0697, 180.8091, 69.1515, 7295.8520, 222.5436, 190.6764,
         5031.7588,
         48.9264, 52.3262, 0.0000, 0.0000, 46.3671, 1861.4858, 0.0000,
         14072.2293),
    12: (0.9480585027,
         29364.3159, 403.5483, 180.1277, 68.8909, 7268.4485, 221.7077, 189.9602,
         5012.8593,
         52.8951, 51.2664, 0.0000, 0.0000, 46.1930, 1855.0237, 880.9295,
         13132.4657),
    13: (0.9445532569,
         29253.4383, 402.0562, 179.4595, 68.6352, 7241.5750, 220.8880, 189.2579,
         4994.3253,
         56.8367, 72.6440, 0.0000, 0.0000, 46.0222, 1848.6861, 877.6031,
         13055.4490),
    14: (0.9411155266,
         29144.6625, 400.5929, 178.8041, 68.3845, 7215.2190, 220.0841, 188.5691,
         4976.1483,
         60.7520, 96.5221, 0.0000, 0.0000, 45.8547, 1842.4776, 874.3399,
         12976.9142),
    15: (0.9377437493,
         29037.9400, 399.1577, 178.1613, 68.1386, 7189.3687, 219.2956, 187.8935,
         4958.3201,
         64.6417, 122.7277, 0.0000, 0.0000, 45.6904, 1836.3953, 871.1382,
         12897.0114),
    16: (0.9344364051,
         28933.2234, 397.7499, 177.5307, 67.8973, 7164.0124, 218.5221, 187.2308,
         4940.8325,
         67.0866, 151.0962, 0.0000, 0.0000, 45.5292, 1830.4361, 867.9967,
         12817.3027),
    17: (0.9311920157,
         26040.4216, 223.6387, 130.3535, 52.0636, 3512.4563, 358.2944, 280.1288,
         0.0000,
         6.7821, 177.0176, 0.0000, 0.0000, 50.1247, 1685.0952, 781.2126,
         18783.2542),
}

CF_COLUMNS = (
    "premiums", "claims_disability", "claims_diagnosis", "claims_surgery",
    "claims_hospital", "claims_event", "claims_liability", "claims_neonatal",
    "claims_death", "claims_lapse", "claims_maturity", "claims_void",
    "claim_expenses", "expenses", "commissions", "net_cf",
)

# The same months in result_pols(), where the two ages, the two compartments and the void
# decrement can be read side by side.
# t: (pols_pay, pols_waived, pols_void, pols_death, pols_lapse,
#     age, age_man, mort_rate, lapse_rate, waiver_rate)
WORKED_EXAMPLE_POLS = {
     0: (1.0000000000, 0.0000000000, 0.0010055425, 0.0000000000, 0.0042607292,
         0, -1, 0.00000000, 0.0500000000, 0.0008464125),
     1: (0.9946632375, 0.0000704908, 0.0010002471, 0.0000000000, 0.0041678607,
         0, -1, 0.00000000, 0.0491916016, 0.0008464125),
     2: (0.9894250860, 0.0001405345, 0.0009950503, 0.0000000000, 0.0040773320,
         0, -1, 0.00000000, 0.0483962733, 0.0008464125),
     3: (0.9842830996, 0.0002101386, 0.0009899498, 0.0000000000, 0.0039890731,
         0, -1, 0.00000000, 0.0476138039, 0.0008464125),
     4: (0.9792349051, 0.0002793102, 0.0009849432, 0.0000000000, 0.0039030165,
         0, -1, 0.00000000, 0.0468439855, 0.0008464125),
     5: (0.9742781992, 0.0003480564, 0.0000000000, 0.0002032802, 0.0038221439,
         0, 0, 0.00250000, 0.0460866134, 0.0008464125),
     6: (0.9701841153, 0.0004167162, 0.0000000000, 0.0002024406, 0.0037432174,
         0, 0, 0.00250000, 0.0453414865, 0.0008464125),
     7: (0.9661701006, 0.0004850729, 0.0000000000, 0.0002016176, 0.0036661811,
         0, 0, 0.00250000, 0.0446084068, 0.0008464125),
     8: (0.9622342426, 0.0005531322, 0.0000000000, 0.0002008109, 0.0035909810,
         0, 0, 0.00250000, 0.0438871795, 0.0008464125),
     9: (0.9583746833, 0.0006208996, 0.0000000000, 0.0002000200, 0.0035175649,
         0, 0, 0.00250000, 0.0431776130, 0.0008464125),
    10: (0.9545896174, 0.0006883806, 0.0000000000, 0.0001992447, 0.0034458821,
         0, 0, 0.00250000, 0.0424795187, 0.0008464125),
    11: (0.9508772907, 0.0007555805, 0.0000000000, 0.0001984844, 0.0033758841,
         0, 0, 0.00250000, 0.0417927112, 0.0008464125),
    12: (0.9472359982, 0.0008225044, 0.0000000000, 0.0001977389, 0.0033075069,
         1, 0, 0.00250000, 0.0411170080, 0.0009071625),
    13: (0.9436593010, 0.0008939558, 0.0000000000, 0.0001970078, 0.0032407225,
         1, 0, 0.00250000, 0.0404522295, 0.0009071625),
    14: (0.9401504048, 0.0009651219, 0.0000000000, 0.0001962908, 0.0031754866,
         1, 0, 0.00250000, 0.0397981991, 0.0009071625),
    15: (0.9367077416, 0.0010360077, 0.0000000000, 0.0001955875, 0.0031117567,
         1, 0, 0.00250000, 0.0391547431, 0.0009071625),
    16: (0.9333297866, 0.0011066185, 0.0000000000, 0.0001948977, 0.0030494917,
         1, 0, 0.00250000, 0.0385216905, 0.0009071625),
    17: (0.9300150566, 0.0011769591, 0.0000000000, 0.0000194021, 0.0029891516,
         1, 1, 0.00025000, 0.0378988730, 0.0011521489),
}

# "The months where the product does something".
# t: (pols_if, premiums, claims_diagnosis, claims_hospital, claims_death, claims_lapse,
#     expenses, commissions, net_cf)
LATER_MONTHS = {
      17: (0.9311920157, 26040.4216, 130.3535, 3512.4563, 6.7821,
           177.0176, 1685.0952, 781.2126, 18783.2542),
     120: (0.7926463831, 21873.0675, 79.3435, 1353.1380, 15.6820,
           1149.8680, 1480.1460, 656.1920, 15651.7364),
     239: (0.7675760087, 20562.2638, 183.5349, 1515.4096, 106.0073,
           344.4363, 1483.5920, 616.8679, 14908.0252),
     240: (0.7674946541, 0.0000, 183.5125, 1515.2490, 106.2627,
           2726.2032, 456.1827, 0.0000, -6391.6508),
     241: (0.7669843661, 0.0000, 183.3875, 1514.2415, 106.3913,
           2729.4233, 456.6323, 0.0000, -6393.3820),
     360: (0.7078397483, 0.0000, 420.1765, 1703.7898, 210.9298,
           3069.2282, 512.8615, 0.0000, -7124.0431),
     600: (0.5935620502, 0.0000, 2415.7974, 2921.8469, 1143.9560,
           3634.3597, 639.0498, 0.0000, -12923.9553),
     720: (0.5298765721, 0.0000, 4738.1131, 4570.1874, 2608.6828,
           3560.3727, 695.4165, 0.0000, -19465.9226),
    1080: (0.1441715821, 0.0000, 2342.3611, 7506.8138, 8685.6915,
           519.2086, 342.7324, 0.0000, -21825.3293),
    1140: (0.0614770783, 0.0000, 920.2036, 3665.8156, 1110.9823,
           40.1461, 161.3576, 0.0000, -6998.6611),
    1199: (0.0161892160, 0.0000, 223.1971, 1078.0805, 7.9723,
           0.1737, 46.8367, 0.0000, -1662.7690),
    1200: (0.0157346742, 0.0000, 0.0000, 0.0000, 0.0000,
           0.0000, 0.0000, 0.0000, 0.0000),
}

LATER_COLUMNS = ("premiums", "claims_diagnosis", "claims_hospital", "claims_death",
                 "claims_lapse", "expenses", "commissions", "net_cf")

# The account and the surrender value at the nodes the 상품요약서 publishes.
# t: (years, cum_prem_pp, refund_ratio, cv_std_pp, surr_chg_pp, av_pp)
VALUE_GRID = {
       0: (0, 0.0000, 0.00000000, 0.0000, 364000.0000, 0.0000),
      12: (1, 336000.0000, 0.00000000, 0.0000, 312000.0000, 252000.0000),
      36: (3, 1008000.0000, 0.45600000, 459648.0000, 208000.0000, 667648.0000),
      60: (5, 1680000.0000, 0.62500000, 1050000.0000, 104000.0000, 1154000.0000),
      84: (7, 2352000.0000, 0.66980000, 1575369.6000, 0.0000, 1575369.6000),
     120: (10, 3360000.0000, 0.73700000, 2476320.0000, 0.0000, 2476320.0000),
     180: (15, 5040000.0000, 0.78300000, 3946320.0000, 0.0000, 3946320.0000),
     240: (20, 6720000.0000, 0.82600000, 5550720.0000, 0.0000, 5550720.0000),
     360: (30, 6720000.0000, 1.01200000, 6800640.0000, 0.0000, 6800640.0000),
     480: (40, 6720000.0000, 1.22500000, 8232000.0000, 0.0000, 8232000.0000),
     600: (50, 6720000.0000, 1.44100000, 9683520.0000, 0.0000, 9683520.0000),
     720: (60, 6720000.0000, 1.58900000, 10678080.0000, 0.0000, 10678080.0000),
    1140: (95, 6720000.0000, 0.16001230, 1075282.6560, 0.0000, 1075282.6560),
    1200: (100, 6720000.0000, 0.00000000, 0.0000, 0.0000, 0.0000),
}

# The published nodes of the 환급률 grid [S2], and the durations in years they sit at.
PUBLISHED_REFUND_NODES = {12: 0.000, 36: 0.456, 60: 0.625, 120: 0.737, 180: 0.783,
                          240: 0.826, 360: 1.012, 480: 1.225, 600: 1.441, 720: 1.589}

# "Policy year 1 in aggregate", t = 0 .. 11, on unrounded values.
YEAR_ONE = {
    "pols_if": 11.6888828896,
    "premiums": 362213.7519,
    "claims_disability": 2869.1771,
    "claims_diagnosis": 1280.7497,
    "claims_surgery": 489.8319,
    "claims_hospital": 51677.7500,
    "claims_event": 1576.3138,
    "claims_liability": 1350.5931,
    "claims_neonatal": 81448.2301,
    "claims_death": 257.5124,
    "claims_lapse": 706.1779,
    "claims_maturity": 0.0000,
    "claims_void": 306.8991,
    "claim_expenses": 477.6984,
    "expenses": 137488.5297,
    "commissions": 212940.0000,
    "net_cf": -130655.7114,
}

# "Undiscounted totals over the whole 1,201-month projection".
TOTALS = {
    "pols_if": 651.7356,
    "premiums": 5458037.9345,
    "claims_disability": 957652.5232,
    "claims_diagnosis": 2844503.4398,
    "claims_surgery": 1094506.2990,
    "claims_hospital": 5033285.2166,
    "claims_event": 466414.7324,
    "claims_liability": 195939.3565,
    "claims_neonatal": 106330.7157,
    "claims_death": 3693345.7287,
    "claims_lapse": 2695713.6444,
    "claims_maturity": 0.0000,
    "claims_void": 306.8991,
    "claim_expenses": 79991.4163,
    "expenses": 1009668.2371,
    "commissions": 365814.7255,
    "net_cf": -13085434.9998,
}

# The four exits, over the whole projection, at the ten decimals the notes print.
EXIT_SPLIT = {"pols_void": 0.0049757330, "pols_death": 0.4688979472,
              "pols_lapse": 0.5103916457, "pols_maturity": 0.0157346742}

# "The equivalence premium".
EPV_OUTGO = 4694583.10870084
EPV_PREM_UNIT = 151.0503621937853
EQUIV_PREMIUM = 31079.588559199034

# The [별표 14] chain, at full precision.
RISK_PREM_ANN = 145537.04939942522
SA_NOTIONAL = 132306408.54493201
PREM_NET_ANN = 252000.0
SURR_CHG_CAP = 364000.0
SURR_CHG_FORMULA = 1575064.08544932
ACQ_COST = 327600.0
COMM_INIT = 212940.0
ACQ_COST_MONTHS = 11.7

# The 태아 module, per birth.
NEONATAL_BIRTH = 47000.0
NEONATAL_BLOCK = 63450.0

# The incidence assumptions the notes tabulate for the first eighteen months, at 만나이 0
# and 1, male.  Every one of them is [std] save the 만나이 5 disability anchor.
INCIDENCE_AT_0_AND_1 = {
    "disability": (0.000100265, 0.00012761),
    "disease_disab": (0.0026, 0.0009),
    "cancer": (0.00018, 0.00015),
    "minor_cancer": (0.00003, 0.000025),
    "cerebral": (0.00004, 0.000012),
    "cardiac": (0.000002, 0.000001),
    "fracture": (0.004, 0.009),
    "burn": (0.006, 0.005),
    "hosp_acc": (0.10, 0.13),
    "hosp_dis": (2.40, 1.10),
    "liability": (0.004, 0.006),
}

# 일반상해 후유장해 발생률(3~100%), 기본계약, 5세, 상해 1급 [S1] — the only 적용위험률
# published anywhere in this product's source set.
PUBLISHED_DISABILITY_RATE = {"M": 0.0001823, "F": 0.0001163}

# The thirteen identities this model publishes.
CHECK_CELLS = {
    "check_pols_roll_fwd", "check_waiver_split", "check_exit_total",
    "check_cover_at_birth", "check_once_only", "check_neonatal_term",
    "check_cv_floor", "check_av_bounds", "check_surr_chg_cap",
    "check_acq_cost_cap", "check_refund_grid", "check_equiv_premium",
    "check_net_cf",
}

CAUSES = ("disability", "disease_disab", "cancer", "minor_cancer", "cerebral",
          "cardiac", "fracture", "burn", "hosp_acc", "hosp_dis", "liability")

BENEFIT_KINDS = ("DISABILITY", "DIAGNOSIS", "SURGERY", "HOSPITAL", "EVENT",
                 "LIABILITY", "NEONATAL")

CHILD_LIFE_KINDS = ("DISABILITY", "DIAGNOSIS", "SURGERY", "HOSPITAL", "EVENT",
                    "LIABILITY", "DEATH")

INPUT_CSVS = {"model_point_table.csv", "mort_table.csv", "incidence_table.csv",
              "basis_table.csv", "neonatal_table.csv", "lapse_table.csv",
              "av_table.csv"}


# ---------------------------------------------------------------------------
# The worked example


def test_the_anchor_cell_is_the_one_the_notes_describe(kr_child_anchor):
    """Model point 1 is the 태아가입 cell the worked example projects, attribute by attribute.

    Every golden number below is conditional on the anchor being this contract and not
    another.  A model point table edited in the ordinary course — a sum insured moved, a
    payment term changed — would leave every other test in this module asserting the wrong
    thing while still comparing numbers, so the cell is pinned first.
    """
    a = kr_child_anchor
    assert a.policy_id() == "CH-KR-0001"
    assert a.sex() == "M" and a.payer_sex() == "M"
    assert a.foetal() is True and a.birth_month() == 5
    assert a.issue_age() == 0 and a.issue_age_man() == 0
    assert a.term_age() == 100 and a.proj_len() == 1201
    assert a.prem_period_years() == 20 and a.prem_period_mths() == 240
    assert a.prem_end() == 239
    assert a.premium_mth() == 28000.0 and a.premium_foetal_mth() == 3000.0
    assert a.foetal_cover_end() == 17 and a.foetal_prem_end() == 16
    assert a.cv_form() == "std" and a.cv_floor_ratio() == 1.0
    assert a.waiver_child() is True and a.waiver_payer() is True
    assert a.payer_age() == 33
    assert a.waiting_mths() == 0 and a.reduction_mths() == 0
    assert a.broad_def() is False
    assert a.prem_discount_rate() == 0.0 and a.prem_discount_mths() == 0
    assert a.lapse_basis() == "loglinear" and a.mort_be_factor() == 1.0
    assert a.pols_if_init() == 1.0
    assert a.hosp_daily() == 40000.0
    for cover, amount in (("disability", 100000000.0), ("disease_disab", 10000000.0),
                          ("cancer", 10000000.0), ("minor_cancer", 2000000.0),
                          ("cerebral", 10000000.0), ("cardiac", 10000000.0),
                          ("surgery", 5000000.0), ("fracture", 400000.0),
                          ("burn", 200000.0), ("liability", 100000000.0),
                          ("neonatal", 10000000.0)):
        assert a.sum_assured(cover) == amount, cover


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_worked_example_cash_flow_row(kr_child_anchor, t):
    """Every cell of the notes' eighteen-row cash flow table, to the four decimals it prints.

    This is the table a reader checks the model against, and it is the only place the
    pre-birth period, the month of birth and the end of the 태아 module can be seen in one
    view.  Reading it off ``result_cf()`` rather than off the cells is deliberate: the
    frame is what the notes print and what a user sees.
    """
    df = kr_child_anchor.result_cf()
    expected = WORKED_EXAMPLE_CF[t]
    assert df.loc[t, "pols_if"] == pytest.approx(expected[0], abs=INFORCE)
    for name, value in zip(CF_COLUMNS, expected[1:]):
        assert df.loc[t, name] == pytest.approx(value, abs=CASH), (t, name)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_POLS))
def test_worked_example_decrement_row(kr_child_anchor, t):
    """Every cell of the notes' ``result_pols()`` table for the same eighteen months.

    The two compartments, the four decrements and — the point of the table — the two ages
    side by side.  ``age_man`` is **−1** before birth, which is not a sentinel bolted on
    but the value the definition produces, and the covers switch on because it stops being
    negative rather than because a flag was set.
    """
    dp = kr_child_anchor.result_pols()
    (pay, waived, void, death, lapse, age, age_man,
     mort, lapse_rate, waiver) = WORKED_EXAMPLE_POLS[t]
    assert dp.loc[t, "pols_pay"] == pytest.approx(pay, abs=INFORCE)
    assert dp.loc[t, "pols_waived"] == pytest.approx(waived, abs=INFORCE)
    assert dp.loc[t, "pols_void"] == pytest.approx(void, abs=INFORCE)
    assert dp.loc[t, "pols_death"] == pytest.approx(death, abs=INFORCE)
    assert dp.loc[t, "pols_lapse"] == pytest.approx(lapse, abs=INFORCE)
    assert int(dp.loc[t, "age"]) == age
    assert int(dp.loc[t, "age_man"]) == age_man
    assert dp.loc[t, "mort_rate"] == pytest.approx(mort, abs=MORT)
    assert dp.loc[t, "lapse_rate"] == pytest.approx(lapse_rate, abs=RATE)
    assert dp.loc[t, "waiver_rate"] == pytest.approx(waiver, abs=RATE)


@pytest.mark.parametrize("t", sorted(LATER_MONTHS))
def test_the_months_where_the_product_does_something(kr_child_anchor, t):
    """The notes' second table: 납입완료, the sign change, and the eighty paid-up years.

    Twelve rows chosen because each of them is a structural event — the end of the 태아
    module, 납입완료 and the month after it, the crossings of the surrender value, the
    peak of the diagnosis line, and the 100세 계약해당일 on which nothing at all is paid.
    A projection that is right for eighteen months and wrong at ``t = 720`` would pass the
    table above and fail here.
    """
    df = kr_child_anchor.result_cf()
    expected = LATER_MONTHS[t]
    assert df.loc[t, "pols_if"] == pytest.approx(expected[0], abs=INFORCE)
    for name, value in zip(LATER_COLUMNS, expected[1:]):
        assert df.loc[t, name] == pytest.approx(value, abs=CASH), (t, name)


@pytest.mark.parametrize("t", sorted(VALUE_GRID))
def test_worked_example_account_and_surrender_value(kr_child_anchor, t):
    """The account, the charge and the surrender value at the notes' fourteen nodes.

    Ten of the fourteen are durations at which a current 상품요약서 publishes a 환급률
    [S2], so this table is the one place a reader can check a computed quantity against a
    figure looked up in a document.  ``t = 84`` is the end of the 해약공제기간 and
    ``t = 1140`` the published 16.0% at 95 years the terminal taper is calibrated on.
    """
    dv = kr_child_anchor.result_val()
    years, cum_prem, ratio, cv_std, charge, av = VALUE_GRID[t]
    assert kr_child_anchor.duration_years(t) == years
    assert dv.loc[t, "cum_prem_pp"] == pytest.approx(cum_prem, abs=CASH)
    assert dv.loc[t, "refund_ratio"] == pytest.approx(ratio, abs=5e-9)
    assert dv.loc[t, "cv_std_pp"] == pytest.approx(cv_std, abs=CASH)
    assert dv.loc[t, "surr_chg_pp"] == pytest.approx(charge, abs=CASH)
    assert dv.loc[t, "av_pp"] == pytest.approx(av, abs=CASH)
    # On the 표준형 the amount payable is the notional value itself.
    assert dv.loc[t, "cv_pp"] == pytest.approx(cv_std, abs=CASH)


def test_the_assumption_table_the_first_eighteen_months_use(kr_child_anchor):
    """The notes' assumption table, every quantitative row, read off the model.

    The notes tabulate every value the opening eighteen months consume together with its
    tag, so that a reader can see at a glance how little of this product is sourced.  Read
    them back here and a silent change to any of them fails a test rather than moving a
    row of the worked example and being explained away as a rounding difference.
    """
    a = kr_child_anchor
    assert a.basis_param("void_rate_ann") == 0.012
    assert a.void_rate_mth(0) == pytest.approx(0.0010055425391276573, rel=TRACE)
    assert a.void_rate_mth(5) == 0.0                       # from birth, there is no void
    assert a.mort_rate(4) == 0.0                           # a 태아 has no mortality [R3]
    assert a.mort_rate(5) == 0.0025
    assert a.mort_rate_mth(5) == pytest.approx(0.00020857243058891584, rel=TRACE)
    assert a.mort_rate(17) == 0.00025
    assert a.mort_rate_mth(17) == pytest.approx(0.00002083572086741814, rel=TRACE)
    assert a.mort_rate_payer(0) == pytest.approx(0.00067713, rel=TRACE)
    assert a.mort_rate_payer(12) == pytest.approx(0.00072573, rel=TRACE)
    assert a.basis_param("payer_disab_ratio") == 0.25
    assert a.waiver_rate_payer(0) == pytest.approx(0.00067713 * 1.25, rel=TRACE)
    assert a.waiver_rate_mth(0) == pytest.approx(0.00007056175284536614, rel=TRACE)
    assert a.waiver_rate_child(16) == 0.0                  # the P코드 carve-out [S2]
    assert a.waiver_rate_child(17) == pytest.approx(0.0002452088, rel=1e-9)
    assert a.lapse_rate(0) == pytest.approx(0.05, rel=1e-14)
    assert a.lapse_rate_mth(0) == pytest.approx(0.004265318777560645, rel=TRACE)
    for cause, (at_zero, at_one) in INCIDENCE_AT_0_AND_1.items():
        assert a.inc_rate(5, cause) == pytest.approx(at_zero, rel=1e-12), cause
        assert a.inc_rate(17, cause) == pytest.approx(at_one, rel=1e-12), cause
    assert a.basis_param("disab_severity") == 0.12
    assert a.basis_param("disease_disab_severity") == 0.15
    assert a.basis_param("surgery_rate_cancer") == 0.85
    assert a.basis_param("surgery_rate_cerebral") == 0.50
    assert a.basis_param("surgery_rate_cardiac") == 0.70
    assert a.basis_param("hosp_cap_factor") == 0.92
    assert a.basis_param("liability_severity") == 600000.0
    assert a.basis_param("leak_share") == 0.40
    assert a.neonatal_cost_pp("birth") == NEONATAL_BIRTH
    assert a.neonatal_cost_pp("block") == NEONATAL_BLOCK
    assert a.acq_cost_pp() == pytest.approx(ACQ_COST, rel=TRACE)
    assert a.comm_init_pp() == pytest.approx(COMM_INIT, rel=TRACE)


def test_the_one_published_korean_child_morbidity_rate_reproduces_exactly(
        child, kr_child_anchor):
    """일반상해 후유장해 발생률(3~100%) at 5세, 상해 1급 — 남 0.0001823, 여 0.0001163 [S1].

    It is the only 적용위험률 published anywhere in this product's source set, the anchor
    the whole of ``incidence_table.csv`` is shaped around, and the one number in the file
    a reader can look up.  It must come back to its last digit — which it does only
    because the graduation short-circuits at a pivot rather than interpolating through it.
    """
    assert kr_child_anchor.inc_rate_at(5, "disability") == \
        PUBLISHED_DISABILITY_RATE["M"]
    female = child.Projection[3]
    assert female.sex() == "F"
    assert female.inc_rate_at(5, "disability") == PUBLISHED_DISABILITY_RATE["F"]
    # And it reaches the projection unaltered: model point 2 is a male 보험나이 5 issue,
    # so the rate at t = 0 is the published one and nothing has been applied to it.
    male_five = child.Projection[2]
    assert male_five.issue_age() == 5 and male_five.age_man(0) == 5
    assert male_five.inc_rate(0, "disability") == PUBLISHED_DISABILITY_RATE["M"]


def test_worked_example_month_zero_trace(kr_child_anchor):
    """The notes' first hand trace, line by line: issue, and the insured does not exist.

    Three premium streams are collected on a contract whose insured has no legal
    personality; every cover on the child's own life is nil; and ``claims_void(0)`` is
    zero **because no premium has yet been collected**, not because the decrement is
    absent — 0.10055% of contracts are voided in the month and it costs nothing.
    """
    a = kr_child_anchor
    assert a.born(0) is False
    assert a.pols_if(0) == 1.0 and a.pols_pay(0) == 1.0 and a.pols_waived(0) == 0.0
    assert a.premiums(0) == pytest.approx((28000.0 + 3000.0) * 1.0 * 1.0, rel=TRACE)
    for kind in CHILD_LIFE_KINDS:
        assert a.claims(0, kind) == 0.0, kind
    assert a.cum_prem_pp(0) == 0.0 and a.prem_foetal_paid_pp(0) == 0.0
    assert a.pols_void(0) == pytest.approx(0.0010055425391276573, rel=TRACE)
    assert a.claims(0, "VOID") == 0.0
    assert a.unearned_prem_pp(0) == 0.5 * 31000.0
    assert a.cv_pp(0) == 0.0
    assert a.claims(0, "LAPSE") == pytest.approx(
        15500.0 * 0.004260729152353977, rel=TRACE)
    assert a.claims(0, "LAPSE") == pytest.approx(66.0413018615, abs=CASH)
    assert a.claim_expenses(0) == pytest.approx(
        30000.0 * (0.0 + 0.0 + 0.0010055425391276573), rel=TRACE)
    assert a.expenses(0) == pytest.approx(
        (ACQ_COST - COMM_INIT) * 1.0 + 400.0 * 1.0 + 0.05 * 31000.0, rel=TRACE)
    assert a.expenses(0) == pytest.approx(116610.0, abs=CASH)
    assert a.commissions(0) == pytest.approx(COMM_INIT, rel=TRACE)
    assert a.net_cf(0) == pytest.approx(-298646.2075780353, abs=CASH)


def test_worked_example_month_zero_decrements(kr_child_anchor):
    """The notes' decrement trace for month 0, in the order void → waiver → death → lapse.

    Every intermediate the notes print, and then the roll-forward closing on them:
    ``1 − l(1) = 0.0052662716914816`` against ``v + q + w`` of the same.  The order is the
    product's own — a voided contract never existed, a waived one still counts, and only a
    paying one can lapse — and the arithmetic below is different under any other.
    """
    a = kr_child_anchor
    assert a.void_rate_mth(0) == pytest.approx(0.0010055425391276573, rel=TRACE)
    assert a.waiver_rate(0) == pytest.approx(0.0008464125, rel=1e-9)
    assert a.waiver_rate_mth(0) == pytest.approx(0.00007056175284536614, rel=TRACE)
    assert a.pols_waiver_entry(0) == pytest.approx(
        (1.0 - 0.0010055425391276573) * 0.00007056175284536614, rel=TRACE)
    assert a.pols_waiver_entry(0) == pytest.approx(0.00007049080000124472, rel=TRACE)
    assert a.mort_rate_mth(0) == 0.0
    assert a.lapse_rate_mth(0) == pytest.approx(0.004265318777560645, rel=TRACE)
    assert a.pols_void(0) == pytest.approx(0.0010055425391276573, rel=TRACE)
    assert a.pols_death(0) == 0.0
    assert a.pols_lapse(0) == pytest.approx(0.0042607291523540, abs=INFORCE)
    assert a.pols_pay(1) == pytest.approx(0.9946632375085172, rel=TRACE)
    assert a.pols_waived(1) == pytest.approx(0.0000704908000012, abs=INFORCE)
    assert a.pols_if(1) == pytest.approx(0.9947337283085184, rel=TRACE)
    assert 1.0 - a.pols_if(1) == pytest.approx(0.0052662716914816, abs=INFORCE)
    assert (a.pols_void(0) + a.pols_death(0) + a.pols_lapse(0)) == pytest.approx(
        0.0052662716914816, abs=INFORCE)


def test_worked_example_month_five_trace(kr_child_anchor):
    """The notes' birth trace: seven per-policy benefit build-ups, then the weighting.

    Month 5 is the month the contract acquires an insured.  Every limb switches on at
    once, the 태아보장기간 pays its whole ₩47,000 in this single month plus one twelfth of
    the ₩63,450 신생아 block, and **the month is the only negative one between issue and
    납입완료** — which is what the trace is for.
    """
    a = kr_child_anchor
    assert a.born(5) is True and a.age_man(5) == 0
    assert a.pols_if(5) == pytest.approx(0.9746262555490346, rel=TRACE)
    assert a.premiums(5) == pytest.approx(31000.0 * a.pols_pay(5), rel=TRACE)
    assert a.premiums(5) == pytest.approx(30202.6241744982, abs=CASH)

    assert a.benefit_pp(5, "DISABILITY") == pytest.approx(
        100000000.0 * 0.12 * 0.000008355800662718238
        + 10000000.0 * 0.15 * 0.00021692529081551726, rel=TRACE)
    assert a.benefit_pp(5, "DISABILITY") == pytest.approx(425.6575441759, abs=CASH)
    assert a.benefit_pp(5, "DIAGNOSIS") == pytest.approx(190.0130578292, abs=CASH)
    assert a.benefit_pp(5, "SURGERY") == pytest.approx(
        5000000.0 * (0.85 * 0.000015001237642309206
                     + 0.50 * 0.0000033333944460256504
                     + 0.70 * 0.00000016666681945665118), rel=TRACE)
    assert a.benefit_pp(5, "SURGERY") == pytest.approx(72.6720799630, abs=CASH)
    assert a.benefit_pp(5, "HOSPITAL") == pytest.approx(
        40000.0 * (0.10 + 2.40) / 12.0 * 0.92, rel=TRACE)
    assert a.benefit_pp(5, "HOSPITAL") == pytest.approx(7666.6666666667, abs=CASH)
    assert a.benefit_pp(5, "EVENT") == pytest.approx(
        400000.0 * 0.0003339460107422143
        + 200000.0 * 0.0005013802940021517, rel=TRACE)
    assert a.benefit_pp(5, "LIABILITY") == pytest.approx(
        0.0003339460107422143 * 600000.0, rel=TRACE)
    assert a.benefit_pp(5, "NEONATAL") == pytest.approx(
        NEONATAL_BIRTH + NEONATAL_BLOCK / 12.0, rel=TRACE)
    assert a.benefit_pp(5, "NEONATAL") == 52287.5

    # and the weighting by l(5) is what produces the row of the table
    for kind, weighted in (("DISABILITY", 414.8570184264),
                           ("DIAGNOSIS", 185.1917150575),
                           ("SURGERY", 70.8281171773),
                           ("HOSPITAL", 7472.1346258759),
                           ("EVENT", 227.9206997120),
                           ("LIABILITY", 195.2835300031),
                           ("NEONATAL", 50960.7703370201)):
        assert a.claims(5, kind) == pytest.approx(
            a.benefit_pp(5, kind) * a.pols_if(5), rel=TRACE), kind
        assert a.claims(5, kind) == pytest.approx(weighted, abs=CASH), kind

    assert a.av_pp(5) == 105000.0 and a.unearned_prem_pp(5) == 15500.0
    assert a.claims(5, "DEATH") == pytest.approx(
        120500.0 * 0.00020328016703563597, rel=TRACE)
    assert a.claims(5, "LAPSE") == pytest.approx(
        15500.0 * 0.003822143851874877, rel=TRACE)
    assert a.claims(5, "VOID") == 0.0
    assert a.claim_expenses(5) == pytest.approx(
        30000.0 * (0.0014155547402482371 * a.pols_if(5)
                   + 0.00020328016703563597), rel=TRACE)
    assert a.expenses(5) == pytest.approx(
        400.0 * 1.0082852288053106 * a.pols_if(5) + 0.05 * a.premiums(5), rel=TRACE)
    assert a.commissions(5) == 0.0
    assert a.net_cf(5) == pytest.approx(-31358.7995796528, abs=CASH)


def test_the_neonatal_module_is_most_of_the_month_of_birth(kr_child_anchor):
    """₩50,960.77 in one month — 85.6% of the month's ₩59,526.99 of morbidity outgo.

    The 태아 module is not spread over the pregnancy: the 태아보장기간 limbs are paid on
    events of the pregnancy and the delivery and they are paid **at birth** [S2] [S8
    제59조].  A model that amortised them would move the whole of the product's early
    strain and leave the rest of the table looking right.
    """
    a = kr_child_anchor
    morbidity = sum(a.claims(5, k) for k in BENEFIT_KINDS)
    assert morbidity == pytest.approx(59526.9860432723, abs=CASH)
    assert a.claims(5, "NEONATAL") / morbidity == pytest.approx(0.8561, abs=5e-5)


def test_worked_example_month_seventeen_trace(kr_child_anchor):
    """The notes' third hand trace: the 태아 module ends and 만나이 turns 1, together.

    Two structural things happen in the same month and pull in opposite directions.  The
    hospital limb halves because ``hosp_dis`` falls from 2.40 to 1.10 days a year, while
    the fracture and liability limbs rise; the 태아 stream stops, so the 미경과보험료 is
    half of ₩28,000 and not of ₩31,000; and the child's waiver limb switches on as the
    신생아 block — and with it the P코드 carve-out — ends.
    """
    a = kr_child_anchor
    assert a.age(17) == 1 and a.age_man(17) == 1
    assert a.premium_mth_pp(17) == 28000.0
    assert a.premiums(17) == pytest.approx(28000.0 * a.pols_pay(17), rel=TRACE)
    assert a.premiums(17) == pytest.approx(26040.4215845963, abs=CASH)
    assert a.benefit_pp(17, "HOSPITAL") == pytest.approx(
        40000.0 * (0.13 + 1.10) / 12.0 * 0.92, rel=TRACE)
    assert a.benefit_pp(17, "HOSPITAL") == pytest.approx(3772.0, abs=CASH)
    assert a.benefit_pp(17, "HOSPITAL") < 0.5 * a.benefit_pp(16, "HOSPITAL") * 1.02
    assert a.benefit_pp(17, "EVENT") == pytest.approx(384.7695804916, abs=CASH)
    assert a.benefit_pp(17, "EVENT") > a.benefit_pp(16, "EVENT")
    assert a.benefit_pp(17, "LIABILITY") == pytest.approx(300.8281764013, abs=CASH)
    assert a.benefit_pp(17, "LIABILITY") > a.benefit_pp(16, "LIABILITY")
    assert a.benefit_pp(17, "NEONATAL") == 0.0
    assert a.unearned_prem_pp(17) == 14000.0
    assert a.av_pp(17) == pytest.approx(335553.3333333334, rel=TRACE)
    assert a.claims(17, "DEATH") == pytest.approx(
        349553.3333333334 * 0.000019402056913845515, rel=TRACE)
    assert a.claims(17, "DEATH") == pytest.approx(6.7820536678, abs=CASH)
    assert a.cv_pp(17) == pytest.approx(45220.0, abs=CASH)
    assert a.claims(17, "LAPSE") == pytest.approx(
        59220.0 * 0.002989151566722004, rel=TRACE)
    assert a.expenses(17) == pytest.approx(
        400.0 * 1.028450933381417 * a.pols_if(17) + 0.05 * a.premiums(17), rel=TRACE)
    assert a.commissions(17) == pytest.approx(0.03 * a.premiums(17), rel=TRACE)
    assert a.net_cf(17) == pytest.approx(18783.2542124813, abs=CASH)
    # The waiver step in the same month, the signature of the P코드 carve-out.
    assert a.waiver_rate(16) == pytest.approx(0.0009071625, rel=1e-9)
    assert a.waiver_rate(17) == pytest.approx(
        1.0 - (1.0 - 0.0002452088) * (1.0 - 0.0009071625), rel=1e-9)
    assert a.waiver_rate(17) == pytest.approx(0.0011521489, abs=RATE)


def test_worked_example_month_two_hundred_and_forty_trace(kr_child_anchor):
    """The notes' 납입완료 trace, and the swing of ₩21,299.68 in one month.

    Four things move at once and the notes attribute each: the premium stops, renewal
    commission stops, premium-related maintenance stops, and ``claims_lapse`` jumps
    because the ultimate lapse rate is nearly eight times the rate an instant earlier and
    is now paid on a surrender value of ₩5,550,720.
    """
    a = kr_child_anchor
    assert a.premium_mth_pp(240) == 0.0 and a.unearned_prem_pp(240) == 0.0
    assert a.waiver_rate(240) == 0.0
    assert a.lapse_rate(239) == pytest.approx(0.0010164336671732908, rel=TRACE)
    assert a.lapse_rate(240) == 0.008
    assert a.lapse_rate(240) / a.lapse_rate(239) == pytest.approx(7.87, abs=0.01)
    assert a.premiums(240) == 0.0 and a.commissions(240) == 0.0
    assert a.expenses(240) == pytest.approx(
        400.0 * 1.485947395978355 * a.pols_if(240), rel=TRACE)
    assert a.cv_pp(240) == 5550720.0
    assert a.claims(240, "LAPSE") == pytest.approx(
        5550720.0 * 0.0004911440743415418, rel=TRACE)
    assert a.claims(240, "DEATH") == pytest.approx(
        5550720.0 * 0.000019143942790725917, rel=TRACE)
    assert a.net_cf(240) == pytest.approx(-6391.6508213043, abs=CASH)

    # the attribution of the swing
    assert a.net_cf(239) - a.net_cf(240) == pytest.approx(21299.68, abs=0.005)
    assert a.premiums(239) == pytest.approx(20562.2638448677, abs=CASH)
    assert a.commissions(239) == pytest.approx(616.8679153460, abs=CASH)
    assert a.expenses(239) - a.expenses(240) == pytest.approx(1027.41, abs=0.005)
    assert a.claims(240, "LAPSE") - a.claims(239, "LAPSE") == pytest.approx(
        2381.77, abs=0.005)


def test_the_sign_of_the_cash_flow_changes_once_and_never_changes_back(kr_child_anchor):
    """One negative month at birth, twenty positive years, then eighty of pure outgo.

    The notes state the shape as a fact about the product rather than as a description:
    ``net_cf`` is negative at issue, negative for exactly one month at birth, positive
    every other month to 납입완료, and negative in **every one** of the 960 months after
    it.  A model that let renewal commission run past ``t = 239``, or that kept the waiver
    running there, would break the second half of that statement without breaking a total.
    """
    a = kr_child_anchor
    assert a.net_cf(0) < -290000.0
    assert a.net_cf(5) < 0.0
    assert all(a.net_cf(t) > 0.0 for t in range(1, 5))
    assert all(a.net_cf(t) > 0.0 for t in range(6, 240))
    assert all(a.net_cf(t) < 0.0 for t in range(240, 1200))
    assert a.net_cf(1200) == 0.0


def test_worked_example_policy_year_one_aggregate(kr_child_anchor):
    """The notes' year-1 table, every line, summed over ``t = 0 … 11`` unrounded.

    Year 1 of this product is unlike year 1 of anything else in the library: it spans the
    pre-birth period, the birth, and seven months of the 신생아 block, so 57.4% of its
    benefit outgo is the 태아 module and 39.2% of the premium goes back out as benefit
    before a single adult-disease limb has any exposure at all.
    """
    df = kr_child_anchor.result_cf().loc[0:11]
    assert df["pols_if"].sum() == pytest.approx(YEAR_ONE["pols_if"], abs=5e-9)
    for name in CF_COLUMNS:
        assert df[name].sum() == pytest.approx(YEAR_ONE[name], abs=CASH), name
    benefits = sum(df["claims_" + k.lower()].sum() for k in
                   ("DISABILITY", "DIAGNOSIS", "SURGERY", "HOSPITAL", "EVENT",
                    "LIABILITY", "NEONATAL", "DEATH", "LAPSE", "MATURITY", "VOID"))
    assert benefits == pytest.approx(141963.2351, abs=CASH)
    assert benefits / df["premiums"].sum() == pytest.approx(0.392, abs=0.0005)
    assert df["claims_neonatal"].sum() / benefits == pytest.approx(0.574, abs=0.0005)
    assert ACQ_COST / 31000.0 == pytest.approx(10.57, abs=0.005)


def test_worked_example_undiscounted_totals(kr_child_anchor):
    """The notes' whole-projection totals, every line, over all 1,201 months.

    ₩5,458,038 of premium against ₩17,087,999 of benefit and ₩1,455,474 of expense and
    commission.  The number is heavily negative and that is the product rather than a
    defect: it is what a hundred-year contract with a twenty-year premium term looks like
    before discounting, which is why the equivalence diagnostics exist.
    """
    df = kr_child_anchor.result_cf()
    assert len(df) == 1201
    assert df["pols_if"].sum() == pytest.approx(TOTALS["pols_if"], abs=CASH)
    for name in CF_COLUMNS:
        assert df[name].sum() == pytest.approx(TOTALS[name], abs=CASH), name
    benefits = sum(df[c].sum() for c in df.columns if c.startswith("claims_"))
    assert benefits == pytest.approx(17087998.5554, abs=CASH)
    outgo = df["claim_expenses"].sum() + df["expenses"].sum() + df["commissions"].sum()
    assert outgo == pytest.approx(1455474.3789, abs=CASH)
    assert df["premiums"].sum() - benefits - outgo == pytest.approx(
        TOTALS["net_cf"], abs=CASH)


def test_the_three_totals_the_notes_read_directly(kr_child_anchor):
    """``claims_hospital`` is the largest line; ``claims_death`` is not a death benefit.

    Both readings are contrary to the chassis and both are asserted rather than described.
    A ₩40,000-a-day 입원일당 written to 100세 costs 47.0% of all morbidity outgo and 92.2%
    of the whole premium collected; and the second largest line is the 계약자적립액 paid on
    a death 상법 제732조 forbids covering, which grows into the biggest single monthly
    outgo late in the projection.
    """
    df = kr_child_anchor.result_cf()
    morbidity = sum(df["claims_" + k.lower()].sum() for k in BENEFIT_KINDS)
    assert morbidity == pytest.approx(10698632.2832, abs=CASH)
    account = sum(df["claims_" + k].sum()
                  for k in ("death", "lapse", "maturity", "void"))
    assert account == pytest.approx(6389366.2722, abs=CASH)
    assert df["claims_hospital"].sum() / morbidity == pytest.approx(0.470, abs=0.0005)
    assert df["claims_hospital"].sum() / df["premiums"].sum() == pytest.approx(
        0.922, abs=0.0005)
    assert df["claims_lapse"].sum() / (morbidity + account) == pytest.approx(
        0.158, abs=0.0005)
    # the two peaks, and the window in which the account outgo leads every other column
    assert df["claims_hospital"].idxmax() == 965
    assert df["claims_hospital"].max() == pytest.approx(10877.56, abs=WON)
    assert df["claims_death"].idxmax() == 1013
    assert df["claims_death"].max() == pytest.approx(15452.17, abs=WON)
    claim_cols = [c for c in df.columns if c.startswith("claims_")]
    leader = df[claim_cols].idxmax(axis=1)
    assert (leader.loc[929:1094] == "claims_death").all()
    assert leader.loc[928] == "claims_hospital"
    assert leader.loc[1150] == "claims_hospital"


def test_the_neonatal_module_costs_what_a_birth_costs_less_the_contracts_that_left(
        kr_child_anchor):
    """₩106,330.72 in total, 0.9627 of the ₩110,450 per-birth cost, all inside 13 months.

    The shortfall is the 3.7% of contracts already voided or lapsed by the time the block
    runs, and it is the only place in the projection where a cost is quoted per *birth*
    rather than per policy issued.  Every won of it falls inside the first thirteen months
    of a hundred-year contract.
    """
    a = kr_child_anchor
    df = a.result_cf()
    per_birth = NEONATAL_BIRTH + NEONATAL_BLOCK
    assert per_birth == 110450.0
    assert df["claims_neonatal"].sum() == pytest.approx(106330.7157, abs=CASH)
    assert df["claims_neonatal"].sum() / per_birth == pytest.approx(0.9627, abs=5e-5)
    assert df.loc[0:17, "claims_neonatal"].sum() == pytest.approx(
        df["claims_neonatal"].sum(), abs=1e-9)
    assert df.loc[17:, "claims_neonatal"].sum() == 0.0


def test_worked_example_exit_split(kr_child_anchor):
    """The four exits over the projection, each to ten decimals, summing exactly to one.

    Four exits and not two: a voided contract has not lapsed and has not died, and a
    maturity is not a lapse at zero value.  Netting any of them into another closes the
    per-month roll-forward just as well and loses the cash flow that goes with it.
    """
    a = kr_child_anchor
    ts = range(0, a.proj_len())
    totals = {name: sum(getattr(a, name)(t) for t in ts) for name in EXIT_SPLIT}
    for name, value in EXIT_SPLIT.items():
        assert totals[name] == pytest.approx(value, abs=INFORCE), name
    assert sum(totals.values()) == pytest.approx(1.0, abs=1e-12)
    assert a.check_exit_total() is True
    assert a.check_exit_total_resid() == pytest.approx(0.0, abs=1e-12)


def test_worked_example_equivalence_premium(kr_child_anchor):
    """The three pricing diagnostics, at the precision the notes print them.

    ₩4,694,583.11 of discounted outgo over 151.0504 discounted premium units gives
    ₩31,079.59 against a shipped ₩28,000, so **the shipped basis is 11.00% short** and, by
    the product's own statement, the computed figure governs.  The second number is the
    model's whole behaviour in one place: out of 240 scheduled instalments the projection
    expects to collect the discounted equivalent of 62.9%.
    """
    a = kr_child_anchor
    assert a.epv_outgo_pp() == pytest.approx(EPV_OUTGO, rel=TRACE)
    assert a.epv_prem_unit_pp() == pytest.approx(EPV_PREM_UNIT, rel=TRACE)
    assert a.equiv_premium_mth_pp() == pytest.approx(EQUIV_PREMIUM, rel=TRACE)
    assert a.equiv_premium_mth_pp() / a.premium_mth() - 1.0 == pytest.approx(
        0.1100, abs=5e-5)
    assert a.epv_prem_unit_pp() / a.prem_period_mths() == pytest.approx(
        0.629, abs=0.0005)
    assert a.check_equiv_premium() is True
    assert a.check_equiv_premium_resid() == pytest.approx(0.0, abs=1e-6)


def test_the_byeolpyo_14_chain(kr_child_anchor):
    """The five links of the 표준해약공제액 computation, each to the notes' precision.

    ₩145,537.05 of first-year risk premium → a notional 보험가입금액 of ₩132,306,409 under
    [별표 15] 제9호 → a [별표 14] formula limb of ₩1,575,064.09, which is 56.25 months of
    core premium and **does not bind**: the 표준해약공제액 is the FSC's 13-month reading of
    the same cap, ₩364,000.00, and the 계약체결비용 at 90% of it is **11.70 months of core
    premium**.  Every input to it is [std]; the arithmetic between them is the
    regulation's.
    """
    a = kr_child_anchor
    assert a.risk_prem_ann_pp() == pytest.approx(RISK_PREM_ANN, rel=TRACE)
    assert a.risk_prem_ann_pp() == pytest.approx(
        sum(a.benefit_cost_pp(t) for t in range(0, 12)), rel=TRACE)
    assert a.sa_notional_pp() == pytest.approx(SA_NOTIONAL, rel=TRACE)
    assert a.prem_net_ann_pp() == PREM_NET_ANN == 12.0 * 28000.0 * 0.75
    assert a.surr_chg_coef() == 20
    assert 0.05 * PREM_NET_ANN * 20 + 0.01 * SA_NOTIONAL == pytest.approx(
        SURR_CHG_FORMULA, rel=TRACE)
    assert a.surr_chg_cap_pp() == pytest.approx(SURR_CHG_CAP, rel=TRACE)
    assert a.surr_chg_cap_pp() == pytest.approx(
        min(SURR_CHG_FORMULA, 13.0 * 28000.0), rel=TRACE)
    assert SURR_CHG_FORMULA / 28000.0 == pytest.approx(56.25, abs=0.005)
    assert a.acq_cost_pp() == pytest.approx(0.9 * SURR_CHG_CAP, rel=TRACE)
    assert a.acq_cost_months() == pytest.approx(ACQ_COST_MONTHS, rel=TRACE)
    assert a.surr_chg_period() == 84
    assert a.check_acq_cost_cap() is True and a.check_surr_chg_cap() is True


def test_the_surrender_charge_runs_off_linearly_and_is_gone_at_seven_years(
        kr_child_anchor):
    """From the whole 표준해약공제액 at issue to nil at ``t = 84``, and nil thereafter.

    감독규정 제7-66조제1항제2호 caps the 해약공제기간 at seven years, which is what binds on
    a 20년납 contract [REG-R19].  The shape between the two ends is [std] — the regulation
    caps the amount and not the run-off — so it is asserted here rather than assumed.
    """
    a = kr_child_anchor
    assert a.surr_chg_pp(0) == pytest.approx(SURR_CHG_CAP, rel=TRACE)
    for t in (0, 12, 36, 60, 83):
        assert a.surr_chg_pp(t) == pytest.approx(
            SURR_CHG_CAP * (1.0 - t / 84.0), rel=TRACE), t
    assert a.surr_chg_pp(84) == 0.0
    assert all(a.surr_chg_pp(t) == 0.0 for t in (84, 120, 240, 1200))


def test_the_surrender_value_crosses_premiums_paid_at_about_year_thirty(
        kr_child_anchor):
    """A shape no other krlib protection product produces, and only a hundred-year term can.

    The 적립부분 compounds at the 공시이율 while the 보장부분 reserve is still building, so
    the published grid crosses 100% of premiums paid between years 20 and 30 [S2].  The
    crossing month is asserted, not the description: it is ``t = 353``, and the value at
    ``t = 240`` is below premiums paid while the value at ``t = 360`` is above.
    """
    a = kr_child_anchor
    paid = 6720000.0
    assert a.cum_prem_pp(240) == paid and a.cum_prem_pp(1200) == paid
    assert a.cv_std_pp(240) < paid < a.cv_std_pp(360)
    crossing = min(t for t in range(240, 361) if a.cv_std_pp(t) >= paid)
    assert crossing == 353
    assert a.duration_years(crossing) == pytest.approx(29.42, abs=0.005)
    assert a.refund_ratio(1200) == 0.0


# ---------------------------------------------------------------------------
# Pitfall: cover attaches at birth, not at the 계약일


def test_pitfall_cover_attaches_at_birth_and_not_at_the_contract_date(kr_child_anchor):
    """Every benefit on the child's own life is identically zero for ``t < b``.

    「제53조의 태아는 출생시에 피보험자가 됩니다」 [S8 제54조], and in 2016 sixteen carriers
    were ordered to stop advertising 「태아 때부터 보장」 [R2].  A model that lets the
    hospital or disability limbs run from ``t = 0`` adds five months of the **infant**
    rate — the highest in the whole table below age 60 — to a period in which nobody is at
    risk, and overstates year-1 benefit outgo by about 30%.
    """
    a = kr_child_anchor
    for t in range(0, 5):
        assert a.born(t) is False
        assert a.mort_rate(t) == 0.0 and a.mort_rate_mth(t) == 0.0
        for cause in CAUSES:
            assert a.inc_rate(t, cause) == 0.0, (t, cause)
        for cover in ("cancer", "minor_cancer", "disability", "fracture"):
            assert a.cover_open(t, cover) == 0.0, (t, cover)
        for kind in CHILD_LIFE_KINDS:
            assert a.claims(t, kind) == 0.0, (t, kind)
        assert a.claim_count_pp(t) == 0.0
        assert a.check_cover_at_birth_resid(t) == 0.0
    assert a.check_cover_at_birth() is True
    # and the rate that would have been used is the highest in the childhood range
    assert a.inc_rate_at(0, "hosp_dis") == 2.40
    assert all(a.inc_rate_at(x, "hosp_dis") < 2.40 for x in range(1, 56))


def test_pitfall_the_pre_birth_void_is_not_a_lapse(child, kr_child_anchor):
    """유산 or 사산 makes the contract 무효 and returns **every premium on both streams**.

    「계약을 무효로 합니다 … 이미 납입한 보험료를 돌려드립니다」 [S8 제56조] [S9].  Netting
    it into ``claims_lapse`` destroys the refund — on the 표준형 the surrender value at
    ``t = 4`` is nil, so the lapse column would pay the 미경과보험료 alone — and loses a
    decrement from the roll-forward.
    """
    a = kr_child_anchor
    assert a.cum_prem_pp(4) == 4 * 28000.0
    assert a.prem_foetal_paid_pp(4) == 4 * 3000.0
    assert a.claims(4, "VOID") == pytest.approx(124000.0 * a.pols_void(4), rel=TRACE)
    assert a.claims(4, "VOID") == pytest.approx(122.1329581771, abs=CASH)
    assert a.cv_pp(4) == 0.0                      # nothing is retained and nothing paid
    assert a.claims(4, "LAPSE") == pytest.approx(
        a.unearned_prem_pp(4) * a.pols_lapse(4), rel=TRACE)
    # the void is its own term of the roll-forward: drop it and the identity opens up
    residual = (a.pols_if(4) - a.pols_if(5) - a.pols_death(4) - a.pols_lapse(4)
                - a.pols_maturity(4))
    assert residual == pytest.approx(a.pols_void(4), rel=TRACE)
    assert a.pols_void(4) > 0.0
    # and on a 무해지 point the refund is unchanged although the surrender value is nil
    susp = child.Projection[4]
    assert susp.cv_form() == "susp" and susp.foetal() is True
    assert susp.cv_pp(4) == 0.0 and susp.cv_pp(239) == 0.0
    assert susp.claims(4, "VOID") == pytest.approx(
        (susp.cum_prem_pp(4) + susp.prem_foetal_paid_pp(4)) * susp.pols_void(4),
        rel=TRACE)
    assert susp.claims(4, "VOID") > 0.0


def test_pitfall_the_two_ages_are_not_one_age(kr_child_anchor):
    """보험나이 and 만나이 differ by exactly ``b`` months for the life of the contract.

    Reading the decrement tables at 보험나이 ages the insured by five months everywhere
    and — worse — makes ``age_man`` non-negative before birth, which quietly re-enables
    the covers the birth gate exists to suppress.  The contract expires when the insured
    is **99 years and 7 months** old: ``age(1200)`` is 100 and ``age_man(1200)`` is 99.
    """
    a = kr_child_anchor
    assert a.age(0) == 0 and a.age(11) == 0 and a.age(12) == 1
    assert a.age_man(4) == -1 and a.age_man(5) == 0 and a.age_man(16) == 0
    assert a.age_man(17) == 1
    assert a.age(1200) == 100 and a.age_man(1200) == 99
    for t in range(0, 1201):
        assert a.age(t) == a.issue_age() + t // 12
        if t < a.birth_month():
            assert a.age_man(t) == -1
        else:
            assert a.age_man(t) == (t - 5) // 12
            assert a.age(t) - a.age_man(t) in (0, 1)
    # the decrement tables are read at 만나이, never at 보험나이
    assert a.mort_rate(12) == a.mort_rate_at_age(0, "M")   # 보험나이 1, 만나이 0
    assert a.mort_rate(17) == a.mort_rate_at_age(1, "M")
    assert a.mort_rate_at_age(0, "M") != a.mort_rate_at_age(1, "M")


def test_pitfall_a_day_count_is_not_a_probability(kr_child_anchor):
    """``hosp_acc`` and ``hosp_dis`` are expected **days** a year.  Divide by twelve.

    ``1 − (1 − 2.40)^(1/12)`` is a complex number and ``1 − (1 − 0.55)^(1/12)`` is a real
    number that is simply wrong, so the hospital limb must never route through
    ``inc_rate_mth``.  The demonstration is left in the assertion: the monthly conversion
    of the infant day count is not even a real number.
    """
    a = kr_child_anchor
    assert isinstance(a.inc_rate_mth(5, "hosp_dis"), complex)
    assert a.inc_rate(5, "hosp_dis") == 2.40 > 1.0
    for t in (5, 17, 240, 1199):
        days = (a.inc_rate(t, "hosp_acc") + a.inc_rate(t, "hosp_dis")) / 12.0
        assert a.benefit_pp(t, "HOSPITAL") == pytest.approx(
            a.hosp_daily() * days * a.basis_param("hosp_cap_factor"), rel=1e-14), t
    # the U-shape the notes describe: an infant peak, a childhood trough, old age
    assert a.inc_rate_at(0, "hosp_dis") == 2.40
    assert a.inc_rate_at(5, "hosp_dis") == 0.55
    assert a.inc_rate_at(10, "hosp_dis") == 0.35
    assert a.inc_rate_at(100, "hosp_dis") == 20.0
    assert 20.0 / 0.35 == pytest.approx(57.14, abs=0.01)


def test_pitfall_the_waiting_period_is_tested_at_the_contract_date(child,
                                                                  kr_child_anchor):
    """The under-15 disapplication is decided at the **계약일** and never re-tested.

    「최초계약과 부활계약의 면책기간은 보험나이 15세 이상인 경우에만 적용」 [S3], and a
    태아가입용 cover has 「면책기간 없음」 at all.  A contract issued at 계약나이 0 therefore
    has no cancer waiting period at any point in its hundred-year life, including the
    eighty-five years in which the insured is an adult; a model that switches the 90 days
    back on at 보험나이 15 is modelling a contract nobody sells.
    """
    a = kr_child_anchor
    assert a.waiting_mths() == 0
    assert a.age(180) == 15                        # the anniversary a naive model uses
    for t in (5, 6, 179, 180, 181, 600, 1199):
        assert a.cover_open(t, "cancer") == 1.0, t
        assert a.cover_open(t, "minor_cancer") == 1.0, t
    assert a.cover_open(1200, "cancer") == 0.0     # nothing is on risk at the 만기

    older = child.Projection[7]
    assert older.issue_age() == 15 and older.waiting_mths() == 3
    assert older.cover_open(0, "cancer") == 0.0
    assert older.cover_open(2, "cancer") == 0.0
    assert older.cover_open(3, "cancer") == 1.0
    assert older.cover_open(2, "fracture") == 1.0  # only the cancer limbs are waiting
    assert older.reduction_factor(2) == 0.5
    assert older.claims(2, "DIAGNOSIS") == pytest.approx(
        (older.sum_assured("cerebral") * older.inc_rate_mth(2, "cerebral")
         * older.frac_open(2, "cerebral")
         + older.sum_assured("cardiac") * older.inc_rate_mth(2, "cardiac")
         * older.frac_open(2, "cardiac"))
        * older.reduction_factor(2) * older.pols_if(2), rel=1e-12)


def test_pitfall_a_foetal_contract_carries_no_reduction_period(child, tmp_path):
    """``reduction_mths()`` returns zero on a 태아 contract whatever the model point says.

    A 변경권고 of 2015-06-17 inserted 「단, 피보험자가 보험가입 당시 태아인 경우에는 보험금의
    100%를 지급합니다」 across 17 carriers and 56 products [R2].  Reading ``reduction_mths``
    straight off the model point re-imposes a reduction the supervisor removed, so the
    shipped table cannot demonstrate the disapplication and an edited copy is used: set the
    anchor's own ``reduction_mths`` to 12 and the model must still return 0.
    """
    edited = edited_model(tmp_path, "Child_KR_S_reduction",
                          {(1, "reduction_mths"): 12})
    try:
        a = edited.Projection[1]
        assert a.foetal() is True
        assert int(a.model_point()["reduction_mths"]) == 12
        assert a.reduction_mths() == 0
        assert a.reduction_factor(0) == 1.0 and a.reduction_factor(11) == 1.0
        assert a.claims(5, "DIAGNOSIS") == pytest.approx(185.1917150575, abs=CASH)
    finally:
        edited.close()

    # and on a non-foetal point the switch does bite, at the published first-year 50%
    older = child.Projection[7]
    assert older.foetal() is False and older.reduction_mths() == 12
    assert older.reduction_factor(11) == 0.5 and older.reduction_factor(12) == 1.0


def test_pitfall_the_child_waiver_limb_does_not_run_over_the_neonatal_block(
        child, kr_child_anchor):
    """「출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를 적용하지 않음」 [S2].

    The covers most likely to pay in the first year of a foetal contract are precisely the
    ones that cannot stop the premium, which is coherent — a neonatal condition is not a
    lifelong impairment — and is implemented rather than averaged away.  The signature is
    the step in ``waiver_rate`` at ``t = 17``; a model without the carve-out has no step.
    """
    a = kr_child_anchor
    assert a.foetal_cover_end() == 17
    assert all(a.waiver_rate_child(t) == 0.0 for t in range(0, 17))
    assert a.waiver_rate_child(17) > 0.0
    assert a.waiver_rate(17) > a.waiver_rate(16)
    assert a.waiver_rate(17) - a.waiver_rate(16) == pytest.approx(
        0.0011521489 - 0.0009071625, abs=RATE)
    # over the block the whole waiver is the 계약자's limb and nothing else
    assert a.waiver_rate(16) == pytest.approx(a.waiver_rate_payer(16), rel=1e-14)
    # on an ordinary contract the child's limb runs from t = 0
    ordinary = child.Projection[2]
    assert ordinary.foetal() is False and ordinary.waiver_child() is True
    assert ordinary.waiver_rate_child(0) > 0.0


def test_pitfall_the_policyholder_is_a_decrement_and_not_a_benefit(child,
                                                                  kr_child_anchor):
    """A waiver removes a premium stream; a 부양자 rider adds an outgo.  Not interchangeable.

    On the 생명보험 chassis the 계약자's death is a **waiver trigger** in the main clause
    [S10 제22조제1항]; on the 손해보험 chassis the same economics arrive as a compulsory
    부양자 death rider paying a lump sum [S5] [S11].  Here it is the former, so the parent's
    event produces no benefit column at all: there is no claim kind for it, and the whole
    of its effect is on ``pols_pay`` and therefore on ``premiums``.
    """
    a = kr_child_anchor
    assert a.waiver_payer() is True
    assert a.waiver_rate_payer(0) == pytest.approx(
        a.mort_rate_payer(0) * 1.25, rel=TRACE)
    assert a.mort_rate_payer(0) == a.mort_rate_at_age(33, "M")
    assert a.mort_rate_payer(240) == a.mort_rate_at_age(53, "M")
    with pytest.raises(FormulaError):
        a.claims(100, "PAYER")
    with pytest.raises(FormulaError):
        a.claims(100, "WAIVER")
    for t in (0, 5, 100, 239):
        assert a.premiums(t) == pytest.approx(
            a.premium_mth_pp(t) * a.prem_discount_factor(t) * a.pols_pay(t), rel=1e-14)
    assert a.pols_pay(100) < a.pols_if(100)        # some are waived and pay nothing
    assert a.check_waiver_split() is True
    # the parent's limb dominates the child's for the whole payment period
    assert a.waiver_rate_child(0) == 0.0 and a.waiver_rate_payer(0) > 0.0
    assert a.waiver_rate_payer(239) == pytest.approx(0.0038416625, rel=1e-9)
    assert a.waiver_rate_child(239) == pytest.approx(0.0003484597, abs=RATE)
    assert a.waiver_rate_payer(239) > 10.0 * a.waiver_rate_child(239)
    # and switching the module off is a model point, not a code path
    without = child.Projection[8]
    assert without.waiver_payer() is False and without.waiver_child() is False
    assert all(without.waiver_rate(t) == 0.0 for t in (0, 12, 120, 239))
    assert all(without.pols_waived(t) == 0.0 for t in (0, 12, 120, 240))


def test_pitfall_the_waiver_stops_at_paid_up(kr_child_anchor):
    """``ω(240) = 0``: waiving a premium nobody pays would suppress eighty years of lapses.

    The only remaining difference between the two compartments after 납입완료 is that the
    waived one is **not exposed to lapse**, so a waiver that kept firing there would
    silently remove the ₩2,695,714 of ``claims_lapse`` that is 15.8% of all benefit outgo.
    """
    a = kr_child_anchor
    assert a.prem_end() == 239
    assert a.waiver_rate_child(240) == 0.0 and a.waiver_rate_payer(240) == 0.0
    assert all(a.waiver_rate(t) == 0.0 for t in (240, 241, 600, 1199))
    assert a.waiver_rate(239) > 0.0
    assert all(a.pols_waiver_entry(t) == 0.0 for t in (240, 600, 1199))
    # the waived cohort thereafter only runs off by mortality
    assert a.pols_waived(241) == pytest.approx(
        a.pols_waived(240) * (1.0 - a.mort_rate_mth(240)), rel=1e-14)
    # and lapses continue for the whole of the paid-up period
    assert all(a.pols_lapse(t) > 0.0 for t in (240, 600, 1000, 1199))
    df = a.result_cf()
    assert df.loc[240:, "claims_lapse"].sum() > 0.9 * df["claims_lapse"].sum()


def test_pitfall_the_waived_compartment_is_not_exposed_to_lapse(kr_child_anchor):
    """``pols_lapse`` is drawn from ``pols_pay`` alone — a policy paying nothing cannot lapse.

    The mirror of the error above.  Lapsing the whole block would take the rate off
    ``pols_if_at(t, "BEF_LAPSE")``, which includes the waived cohort; the model takes it
    off the paying part of that population, and the difference is exactly the waived
    cohort times the monthly rate.
    """
    a = kr_child_anchor
    for t in (12, 100, 239):
        base = (a.pols_pay(t) * (1.0 - a.void_rate_mth(t))
                - a.pols_waiver_entry(t)) * (1.0 - a.mort_rate_mth(t))
        assert a.pols_lapse(t) == pytest.approx(
            base * a.lapse_rate_mth(t), rel=1e-14), t
        whole_block = a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t)
        assert a.pols_lapse(t) < whole_block, t
        assert a.pols_waived(t) > 0.0
    assert a.check_waiver_split() is True
    assert a.check_pols_roll_fwd() is True


def test_pitfall_the_basic_cover_is_a_percentage_scale_not_a_lump_sum(kr_child_anchor):
    """보험가입금액 × 장해지급률 on a continuous 3~100% band [R12] [S1] [S2] [S11].

    The 기본계약 carries the largest 보험가입금액 in the contract and the most heavily
    standardized parameter attached to it.  At ``disab_severity = 0.12`` the accident limb
    costs ₩555,177.98 over the term; read as a lump sum at the full 가입금액 it costs
    ₩4,626,483.18.  **The error is a factor of 8.3 and it lands on ₩100,000,000 of cover.**
    """
    a = kr_child_anchor
    n = a.proj_len() - 1        # the terminal row carries no benefit; sum the term itself
    sev = a.basis_param("disab_severity")
    assert sev == 0.12
    accident = sum(a.sum_assured("disability") * sev * a.inc_rate_mth(t, "disability")
                   * a.pols_if(t) for t in range(0, n))
    lump = sum(a.sum_assured("disability") * 1.0 * a.inc_rate_mth(t, "disability")
               * a.pols_if(t) for t in range(0, n))
    assert accident == pytest.approx(555177.98, abs=WON)
    assert lump == pytest.approx(4626483.18, abs=WON)
    assert lump / accident == pytest.approx(8.33, abs=0.005)
    # the disease twin sits beside it on its own severity
    assert a.benefit_pp(100, "DISABILITY") == pytest.approx(
        a.sum_assured("disability") * sev * a.inc_rate_mth(100, "disability")
        + a.sum_assured("disease_disab") * a.basis_param("disease_disab_severity")
        * a.inc_rate_mth(100, "disease_disab"), rel=1e-14)


def test_pitfall_the_once_only_ledgers_are_per_policy(kr_child_anchor):
    """``frac_open`` is a per-policy ledger and is never weighted by ``pols_if``.

    Weighting it by the in-force probability measures the *block's* consumption and defers
    exhaustion forever, which on a hundred-year term is worth a great deal: the general
    tier runs from 1.0000 to **0.4023**, not to something near 1, and a quarter of the line
    has been used by the time the contract ends.
    """
    a = kr_child_anchor
    for cause in ("cancer", "minor_cancer", "cerebral", "cardiac"):
        assert a.frac_open(0, cause) == 1.0, cause
        for t in (1, 100, 600, 1200):
            assert a.frac_open(t, cause) == pytest.approx(
                a.frac_open(t - 1, cause) * (1.0 - a.inc_rate_mth(t - 1, cause)),
                rel=1e-14), (cause, t)
    assert a.frac_open(1200, "cancer") == pytest.approx(0.4023261296, abs=5e-11)
    assert a.frac_open(1200, "cancer") < 0.5
    # the ledger is untouched for decades and then drains
    assert a.frac_open(360, "cancer") > 0.99
    assert a.check_once_only() is True
    assert all(a.check_once_only_resid(t) == 0.0 for t in (0, 1, 360, 720, 1200))


def test_pitfall_renewal_commission_runs_from_month_twelve_to_paid_up(kr_child_anchor):
    """``12 <= t <= 239`` and nowhere else.

    Charging it from ``t = 1`` is worth about ₩925 a month in months 1–11; charging it
    after 납입완료 is worth eighty years of commission on a premium nobody pays.  Initial
    commission falls once, at ``t = 0``, and is not a rate on anything.
    """
    a = kr_child_anchor
    assert a.commissions(0) == pytest.approx(COMM_INIT, rel=TRACE)
    assert all(a.commissions(t) == 0.0 for t in range(1, 12))
    assert 0.03 * a.premiums(1) == pytest.approx(925.04, abs=WON)
    for t in (12, 100, 239):
        assert a.commissions(t) == pytest.approx(0.03 * a.premiums(t), rel=1e-14), t
    assert a.commissions(12) == pytest.approx(880.9294783452, abs=CASH)
    assert all(a.commissions(t) == 0.0 for t in (240, 241, 600, 1199, 1200))
    df = a.result_cf()
    assert df["commissions"].sum() == pytest.approx(TOTALS["commissions"], abs=CASH)
    assert df.loc[240:, "commissions"].sum() == 0.0


def test_pitfall_there_is_no_maturity_benefit(kr_child_anchor):
    """``claims_maturity`` is a column of zeros, and it is published rather than dropped.

    There is no 만기환급금 on the protection part [S1] [S2] and the shipped taper reaches
    zero at 만기, so the 1.57% of policies that reach the 100세 계약해당일 receive nothing.
    A model that paid ``av_pp`` at maturity without the taper would pay them ₩10,678,080
    each — which is exactly what the untapered build value comes to.
    """
    a = kr_child_anchor
    df = a.result_cf()
    assert (df["claims_maturity"] == 0.0).all()
    assert a.pols_maturity(1200) == pytest.approx(0.0157346742, abs=INFORCE)
    assert a.pols_maturity(1199) == 0.0
    assert a.refund_ratio(1200) == 0.0 and a.av_pp(1200) == 0.0
    assert a.cv_pp(1200) == 0.0
    assert a.refund_taper(1.0) == 0.0
    # what a model without the taper would pay
    assert a.refund_build(a.duration_years(1200)) * a.cum_prem_pp(1200) == \
        pytest.approx(10678080.0, abs=CASH)
    # the last row carries the survivors and nothing else
    last = df.loc[1200]
    assert last["pols_if"] == pytest.approx(0.0157346742, abs=INFORCE)
    assert all(last[c] == 0.0 for c in CF_COLUMNS)


def test_pitfall_the_account_does_not_start_at_the_surrender_charge(kr_child_anchor):
    """``av_pp(0) = 0`` on a contract that has collected nothing.

    The published grid is 「순보험료식 계약자적립액에서 해약공제액을 공제한 금액」 [S2] —
    already net of the charge and floored at zero — so adding the unamortised charge back
    where the floor binds would give an account of ₩364,000 at issue.  The cap at
    ``net_prem_ratio × cum_prem_pp(t)`` is what prevents it.
    """
    a = kr_child_anchor
    assert a.cv_std_pp(0) + a.surr_chg_pp(0) == pytest.approx(SURR_CHG_CAP, rel=TRACE)
    assert a.av_pp(0) == 0.0
    assert a.basis_param("net_prem_ratio") == 0.75
    assert a.av_pp(12) == pytest.approx(0.75 * a.cum_prem_pp(12), rel=1e-14)
    assert a.av_pp(12) == 252000.0
    for t in (0, 12, 36, 60, 84, 240, 720, 1200):
        gross = a.cv_std_pp(t) + a.surr_chg_pp(t)
        cap = max(a.cv_std_pp(t), 0.75 * a.cum_prem_pp(t))
        assert a.av_pp(t) == pytest.approx(min(gross, cap), rel=1e-14), t
        assert a.cv_pp(t) <= a.av_pp(t) + 1e-9, t
    assert a.check_av_bounds() is True


def test_pitfall_the_notional_face_amount_is_read_at_the_reference_age(
        child, kr_child_anchor):
    """[별표 15] 제9호 is evaluated at the **기준연령 요건, 남자 만 40세**, not at the insured's.

    At 만나이 5 the mortality rate is 0.00012, which would put the notional 보험가입금액
    above ₩1.2 billion and the [별표 14] formula limb at ₩12,380,087.45 — 442.1 months of
    premium, absurd on its face.  At 40 that limb is ₩1,575,064.09, or 56.25 months, still
    far enough above the FSC's 13-month reading of the same cap that the cap binds at
    ₩364,000.00 and the 계약체결비용 at 90% of it at 11.70 months
    [REG-R21] [REG-R9 제1-2조제2호] [REG-R29].
    """
    a = kr_child_anchor
    refs = child.Projection.refs
    assert refs["ref_age"] == 40 and refs["ref_sex"] == "M"
    assert a.mort_rate_at_age(40, "M") == 0.0011
    assert a.sa_notional_pp() == pytest.approx(
        a.risk_prem_ann_pp() / 0.0011, rel=TRACE)
    assert a.surr_chg_cap_pp() / a.premium_mth() == pytest.approx(13.00, abs=0.005)
    assert a.acq_cost_months() == pytest.approx(11.70, abs=0.005)
    # the counterfactual the notes quantify, on the [별표 14] formula limb
    at_five = a.risk_prem_ann_pp() / a.mort_rate_at_age(5, "M")
    cap_at_five = 0.05 * a.prem_net_ann_pp() * a.surr_chg_coef() + 0.01 * at_five
    assert a.mort_rate_at_age(5, "M") == 0.00012
    assert cap_at_five == pytest.approx(12380087.45, abs=WON)
    assert cap_at_five / a.premium_mth() == pytest.approx(442.15, abs=0.005)
    assert cap_at_five > 3.0 * SURR_CHG_FORMULA


def test_pitfall_there_are_four_exits_not_two(kr_child_anchor):
    """Dropping the void or the maturity loses mass the per-month identity would not catch.

    ``check_pols_roll_fwd`` closes on four terms.  Drop the void and the residual is the
    void; drop the maturity and it is the maturity — and a projection that netted either
    into lapse would still close every month while paying the wrong cash flow.
    """
    a = kr_child_anchor
    assert a.check_pols_roll_fwd() is True
    for t in (0, 4, 5, 240, 1199, 1200):
        assert a.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-14), t
    without_void = (a.pols_if(0) - a.pols_if(1) - a.pols_death(0) - a.pols_lapse(0)
                    - a.pols_maturity(0))
    assert without_void == pytest.approx(a.pols_void(0), rel=TRACE)
    assert without_void > 0.0
    without_maturity = (a.pols_if(1200) - a.pols_if(1201) - a.pols_void(1200)
                        - a.pols_death(1200) - a.pols_lapse(1200))
    assert without_maturity == pytest.approx(a.pols_maturity(1200), rel=TRACE)
    assert without_maturity > 0.0


def test_pitfall_the_incidence_grid_is_graduated_log_linearly(kr_child_anchor):
    """Log-linear between pivots: a linear interpolation is wrong by a factor of two mid-span.

    Every one of these rates spans two or more orders of magnitude across the age range,
    so the graduation is not a refinement.  The interpolator returns a pivot **exactly**,
    which is why the one published rate in the file comes back to its last digit, and it
    is held flat outside the pivot range.
    """
    a = kr_child_anchor
    for age in (0, 1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100):
        rate = a.inc_rate_at(age, "cancer")
        assert rate > 0.0
    assert a.inc_rate_at(20, "cancer") == 0.00025
    assert a.inc_rate_at(30, "cancer") == 0.00055
    assert a.inc_rate_at(25, "cancer") == pytest.approx(
        math.sqrt(0.00025 * 0.00055), rel=1e-14)
    assert a.inc_rate_at(25, "cancer") != pytest.approx(
        0.5 * (0.00025 + 0.00055), rel=1e-3)
    # held flat outside the pivots, and the terminal pivot caps the projection
    assert a.inc_rate_at(-3, "cancer") == a.inc_rate_at(0, "cancer")
    assert a.inc_rate_at(120, "cancer") == a.inc_rate_at(100, "cancer")
    # the projection reads the grid at 만나이, which on this cell reaches 99 and not 100
    assert a.age_man(1199) == 99
    assert a.inc_rate(1199, "cancer") == a.inc_rate_at(99, "cancer")
    with pytest.raises(FormulaError):
        a.inc_rate_at(5, "not_a_cause")


def test_pitfall_the_sex_relativity_has_no_fixed_sign():
    """The male-rate convention on a 태아 contract implies no refund on the birth of a girl.

    Four carriers on the comparison board price the female above the male and seven below,
    the spread running 62% to 114% [S11], so the composite adopts the male rate and does
    **not** model the true-up.  The shipped incidence table carries the same absence of a
    sign, which is what makes the omission honest rather than convenient.
    """
    table = pd.read_csv(CSV_DIR / "incidence_table.csv")
    wide = table.pivot_table(index=["cause", "age"], columns="sex", values="rate")
    higher = wide[wide["F"] > wide["M"]]
    lower = wide[wide["F"] < wide["M"]]
    assert len(higher) > 0 and len(lower) > 0
    assert {"cancer", "minor_cancer", "hosp_dis", "fracture"} <= set(
        higher.index.get_level_values("cause"))
    assert wide.loc[("cancer", 30), "F"] > wide.loc[("cancer", 30), "M"]
    assert wide.loc[("cancer", 5), "F"] < wide.loc[("cancer", 5), "M"]


def test_pitfall_the_true_up_on_a_foetal_contract_is_not_modelled(child,
                                                                 kr_child_anchor):
    """A 태아 contract is priced male and the model says so rather than inventing a refund.

    Nothing in the model reads a post-birth sex, and no cells exists to do it.  Names
    alone are not coverage, so the arithmetic guard is beside them: on the anchor every
    rate is the male one at every duration, including the eighty years after 납입완료.
    """
    a = kr_child_anchor
    names = set(child.Projection.cells) | set(child.Projection.refs)
    for absent in ("true_up", "trueup", "sex_at_birth", "sex_true_up",
                   "premium_refund", "sex_adjust"):
        assert absent not in names, f"{absent} would model a true-up the notes disclaim"
    assert a.foetal() is True and a.sex() == "M"
    for t in (5, 17, 240, 1199):
        assert a.mort_rate(t) == a.mort_rate_at_age(a.age_man(t), "M"), t
        assert a.inc_rate(t, "cancer") == a.inc_rate_at(
            min(a.age_man(t), 100), "cancer"), t
    assert "male-rate convention" in flat(child.Projection.cells["sex"].doc)


def test_pitfall_the_displayed_rows_do_not_re_add(kr_child_anchor):
    """Rounded rows and unrounded totals differ in the last displayed digit.

    The worked example prints money to four decimals and the aggregates are sums of the
    unrounded values, so re-adding the printed rows reproduces neither.  The aggregates
    asserted in this module are therefore taken from the frame, never from the golden
    table above — and the two really do differ, on eight of the seventeen columns.
    """
    df = kr_child_anchor.result_cf()
    differing = []
    for name in CF_COLUMNS:
        from_rows = round(sum(round(df.loc[t, name], 4) for t in range(0, 12)), 4)
        unrounded = round(df.loc[0:11, name].sum(), 4)
        if from_rows != unrounded:
            differing.append(name)
    assert len(differing) >= 6
    assert "net_cf" in differing and "premiums" in differing
    # the golden rows themselves are the rounded ones, and they do not re-add either
    from_golden = round(sum(WORKED_EXAMPLE_CF[t][CF_COLUMNS.index("net_cf") + 1]
                            for t in range(0, 12)), 4)
    assert from_golden != round(YEAR_ONE["net_cf"], 4)


# ---------------------------------------------------------------------------
# The product's own identities and boundaries


def test_thirteen_check_cells_are_published_each_with_its_residual(child):
    """Thirteen identities, asserted **by name**, each with the signed residual beside it.

    That they are *true*, on all ten model points, is asserted in
    ``test_model_conventions_kr.py``, whose sweep discovers every ``check_*`` generically
    and calls it on every model point of every model in the library.  Generic discovery
    cannot notice a check that has *gone*: it simply stops being discovered.  Naming them
    is the statement left here, and on this product four of the thirteen exist only
    because the contract is written before the insured does.
    """
    cells = set(child.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == CHECK_CELLS
    for name in published:
        assert name + "_resid" in cells, name
    # the four that are this product's rather than the chassis's
    assert {"check_cover_at_birth", "check_neonatal_term", "check_waiver_split",
            "check_exit_total"} <= published


def test_the_check_tolerances_are_named_references(child, kr_child_anchor):
    """No bare literal tolerance: ``roll_fwd_tol`` for the counts, ``val_tol`` for money.

    The two are different quantities and must not collapse into one.  ``roll_fwd_tol``
    closes identities between counts near 1.0, where the residual is a unit or two in the
    last place.  ``val_tol`` closes checks on won amounts of order 1e8 — the 계약자적립액,
    the 표준해약공제액, the equivalence identity's 1,201-term summations — where float64
    rounding leaves a residual ``roll_fwd_tol`` would reject.  Both are far below one won.
    """
    refs = child.Projection.refs
    assert "roll_fwd_tol" in refs and "val_tol" in refs
    assert refs["roll_fwd_tol"] == 1e-10
    assert refs["val_tol"] == 1e-07
    assert refs["val_tol"] > refs["roll_fwd_tol"]
    assert refs["val_tol"] < 1.0
    a = kr_child_anchor
    worst = max(abs(a.check_pols_roll_fwd_resid(t))
                for t in range(0, a.proj_len()))
    assert worst < refs["roll_fwd_tol"] / 100.0


def test_the_in_force_roll_forward_is_the_notes_identity(kr_child_anchor):
    """``l(t) − l(t+1) = voids + deaths + lapses + maturities``, in every projected month.

    The library-wide form of a roll-forward check, with the product's own fourth term.
    Asserted here on the anchor at every one of the 1,201 months rather than at a sample,
    because the decrements switch on and off at four different dates — birth, the end of
    the 신생아 block, 납입완료 and the 만기 — and a residual could hide in any of them.
    """
    a = kr_child_anchor
    assert a.check_pols_roll_fwd() is True
    for t in range(0, a.proj_len()):
        out = (a.pols_void(t) + a.pols_death(t) + a.pols_lapse(t)
               + a.pols_maturity(t))
        assert a.pols_if(t) - a.pols_if(t + 1) == pytest.approx(out, abs=1e-12), t
    assert a.pols_if(a.proj_len()) == 0.0
    assert a.pols_if(-1) == 0.0


def test_the_decrements_are_taken_in_the_notes_processing_order(kr_child_anchor):
    """Void, then the waiver, then mortality, then lapse — asserted by an ordering effect.

    Order matters and the assertion is arithmetic rather than documentary: the population
    lapses are drawn from is the paying compartment **after** the void and the waiver have
    taken their share and **after** mortality.  Taking the waiver after mortality, or
    lapse before it, moves ``pols_lapse`` by a computable amount at every duration, and
    the equality below holds under one order only.
    """
    a = kr_child_anchor
    for t in (0, 5, 12, 100, 239):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            (a.pols_if(t) - a.pols_void(t)) * (1.0 - a.mort_rate_mth(t)), rel=1e-15)
        assert a.pols_if_at(t, "AFT_DECR") == a.pols_if(t + 1)
        # the waiver is drawn after the void and before mortality
        assert a.pols_waiver_entry(t) == pytest.approx(
            a.pols_pay(t) * (1.0 - a.void_rate_mth(t)) * a.waiver_rate_mth(t),
            rel=1e-15), t
        # and lapse from what is left of the paying compartment after mortality
        assert a.pols_lapse(t) == pytest.approx(
            (a.pols_pay(t) * (1.0 - a.void_rate_mth(t)) - a.pols_waiver_entry(t))
            * (1.0 - a.mort_rate_mth(t)) * a.lapse_rate_mth(t), rel=1e-15), t
    with pytest.raises(FormulaError):
        a.pols_if_at(5, "AFT_LAPSE")


def test_the_neonatal_module_pays_inside_its_own_two_terms_and_nowhere_else(
        child, kr_child_anchor):
    """The 태아보장기간 at birth and the 1년만기 신생아 block over the twelve months after it.

    The module merges two terms the sources state separately [S2] [S5] [R5], so it must
    pay in ``b <= t < b + 12`` and nowhere else, and nothing at all on a contract that is
    not a 태아가입.  It is the one thing in the model that may pay in respect of an event
    occurring before the insured legally exists, which is why it is tested apart from the
    birth gate.
    """
    a = kr_child_anchor
    assert a.check_neonatal_term() is True
    assert all(a.claims(t, "NEONATAL") == 0.0 for t in range(0, 5))
    assert a.claims(5, "NEONATAL") > 0.0
    assert all(a.claims(t, "NEONATAL") > 0.0 for t in range(5, 17))
    assert all(a.claims(t, "NEONATAL") == 0.0 for t in (17, 18, 240, 1200))
    assert a.benefit_pp(5, "NEONATAL") == pytest.approx(
        NEONATAL_BIRTH + NEONATAL_BLOCK / 12.0, rel=1e-14)
    for t in range(6, 17):
        assert a.benefit_pp(t, "NEONATAL") == pytest.approx(
            NEONATAL_BLOCK / 12.0, rel=1e-14), t
    ordinary = child.Projection[2]
    assert ordinary.foetal() is False
    assert ordinary.neonatal_cost_pp("birth") == 0.0
    assert ordinary.neonatal_cost_pp("block") == 0.0
    assert ordinary.check_neonatal_term() is True
    assert ordinary.result_cf()["claims_neonatal"].sum() == 0.0


def test_the_liability_leak_limb_is_off_for_three_months_of_every_renewal_cycle(
        child, kr_child_anchor):
    """The 누수사고 90-day 보장개시일 resets at every renewal of the 3년만기 갱신형 block.

    The one place in this model where the renewal mechanic has a cash consequence [S5]
    [S3].  ``leak_share`` of the cost is off for the first three months of each 36-month
    cycle, so the liability column steps down at ``t = 36`` and back up at ``t = 39`` —
    a signature no smooth implementation produces.
    """
    a = kr_child_anchor
    assert a.basis_param("leak_share") == 0.40
    assert child.Projection.refs["liability_cycle_mths"] == 36
    severity = a.basis_param("liability_severity")
    scale = a.sum_assured("liability") / 100000000.0
    for t in (36, 37, 38, 72, 73, 74):
        assert a.benefit_pp(t, "LIABILITY") == pytest.approx(
            0.60 * a.inc_rate_mth(t, "liability") * severity * scale, rel=1e-14), t
    for t in (17, 35, 39, 40, 71, 75):
        assert a.benefit_pp(t, "LIABILITY") == pytest.approx(
            a.inc_rate_mth(t, "liability") * severity * scale, rel=1e-14), t
    assert a.benefit_pp(35, "LIABILITY") > a.benefit_pp(36, "LIABILITY")
    assert a.benefit_pp(39, "LIABILITY") > a.benefit_pp(38, "LIABILITY")


def test_the_published_cash_flow_statement_closes(kr_child_anchor):
    """``net_cf`` equals the published columns of the same row, in every one of 1,201 rows.

    A twelfth benefit kind added to ``claims`` and left out of the statement would vanish
    silently without this; it shows up here instead.  The claim handling expense is
    published in its own column and deducted explicitly, as it is in every model in the
    six libraries.
    """
    a = kr_child_anchor
    assert a.check_net_cf() is True
    df = a.result_cf()
    outgo = df[[c for c in df.columns
                if c.startswith("claims_")] + ["claim_expenses", "expenses",
                                               "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-8)
    assert max(abs(a.check_net_cf_resid(t)) for t in (0, 5, 17, 240, 1200)) < 1e-6
    # the eleven kinds are the whole of claims(t), with no subtotal column beside them
    assert "claims" not in df.columns
    for t in (0, 5, 240, 1200):
        assert a.claims(t) == pytest.approx(
            sum(df.loc[t, c] for c in df.columns if c.startswith("claims_")),
            rel=1e-14), t


def test_the_surrender_value_forms_and_their_floors(child, kr_child_anchor):
    """표준형, 미지급형 and 미지급형Ⅲ, each asserted against its own regulatory floor.

    The suppressed form's value is a **cliff, not a curve**: nil through the whole
    납입기간 and then 50% of the notional 표준형 value [REG-R19 제7-66조제4항제2호], while
    the graded form climbs the published ten-step ladder [S1].  The same lapse rate
    produces a very different cash flow depending on whether anything is paid on it, which
    is why the lapse assumption over that period became a supervisory matter.
    """
    assert kr_child_anchor.check_cv_floor() is True
    assert kr_child_anchor.cv_pp(120) == kr_child_anchor.cv_std_pp(120)

    susp = child.Projection[4]
    assert susp.cv_form() == "susp" and susp.cv_floor_ratio() == 0.50
    assert all(susp.cv_pp(t) == 0.0 for t in (0, 12, 120, 238, 239))
    assert susp.cv_pp(240) == pytest.approx(0.50 * susp.cv_std_pp(240), rel=1e-14)
    assert susp.cv_pp(240) > 0.0
    assert susp.check_cv_floor() is True
    assert susp.claims(120, "LAPSE") == pytest.approx(
        susp.unearned_prem_pp(120) * susp.pols_lapse(120), rel=1e-14)

    graded = child.Projection[5]
    assert graded.cv_form() == "graded" and graded.cv_floor_ratio() == 0.50
    assert graded.cv_grade_ratio(239) == 0.0
    for step, t in enumerate(range(240, 240 + 24 * 10, 24)):
        assert graded.cv_grade_ratio(t) == pytest.approx(
            min(0.05 * (step + 1), 0.50), rel=1e-14), t
    assert graded.cv_grade_ratio(240 + 24 * 9) == 0.50
    assert graded.cv_grade_ratio(1000) == 0.50
    assert graded.check_cv_floor() is True


def test_the_published_refund_grid_reproduces_every_node_it_reaches(kr_child_anchor):
    """Ten published 환급률 nodes [S2], returned exactly while the terminal taper is still 1.

    The one check in this model that ties a computed quantity to a number a reader can
    look up, and what catches an interpolation that is smooth and wrong.  The 16.0% at 95
    years is the calibration point of the taper and is asserted beside them.
    """
    a = kr_child_anchor
    assert a.check_refund_grid() is True
    for t, published in PUBLISHED_REFUND_NODES.items():
        assert a.refund_build(a.duration_years(t)) == pytest.approx(
            published, rel=1e-14), t
        assert a.refund_taper(a.runoff(t)) == 1.0, t
        assert a.refund_ratio(t) == pytest.approx(published, rel=1e-14), t
    assert a.refund_ratio(1140) == pytest.approx(0.16001230, abs=5e-9)
    assert a.refund_build(95.0) == 1.589
    assert a.refund_taper(1140 / 1200) == pytest.approx(0.1007, rel=1e-14)
    # held flat beyond the last published node, and taken down by the taper alone
    assert a.refund_build(70.0) == 1.589 and a.refund_build(100.0) == 1.589
    assert a.refund_taper(0.0) == 1.0 and a.refund_taper(0.85) == 1.0
    assert a.refund_ratio(1020) == pytest.approx(1.589, rel=1e-14)   # t/n = 0.85
    assert a.refund_ratio(1080) == pytest.approx(1.589 * 0.55, rel=1e-14)


# ---------------------------------------------------------------------------
# The modules and the switches, in both positions


def test_the_shipped_model_points_exercise_every_switch(child):
    """Ten points covering both sexes, both age bases, every module and every form.

    The composite is one contract; the switches are what make the rest of the market
    representable, and each of them has to be exercised somewhere or the code path that
    reads it is never run.  This is the inventory, asserted so that a point silently
    changed to duplicate another shows up as a gap rather than as nothing.
    """
    table = child.Data.model_point_table()
    assert len(table) == 10
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["foetal"]) == {0, 1}
    assert set(table["cv_form"]) == {"std", "susp", "graded"}
    assert set(table["lapse_basis"]) == {"loglinear", "disclosed", "flat"}
    assert set(table["term_age"]) == {30, 100, 110}
    assert set(table["prem_period_years"]) == {20, 30}
    assert set(table["waiver_child"]) == {0, 1}
    assert set(table["waiver_payer"]) == {0, 1}
    assert set(table["broad_def"]) == {0, 1}
    assert set(table["waiting_mths"]) == {0, 3}
    assert set(table["reduction_mths"]) == {0, 12}
    assert set(table["prem_discount_rate"]) == {0.0, 0.05}
    assert set(table["mort_be_factor"]) == {1.0, 1.1}
    assert sorted(set(table["issue_age"])) == [0, 5, 15, 30]
    assert int(table.loc[1, "foetal"]) == 1 and int(table.loc[1, "birth_month"]) == 5


def test_the_broad_definition_switch_multiplies_the_two_adult_limbs(child,
                                                                   kr_child_anchor):
    """뇌혈관질환 / 허혈성심장질환 against 뇌출혈 / 급성심근경색증, at a [std] factor of four.

    The composite prices the **narrow** pair against the grain of current practice,
    because every published premium in the file is quoted on the comparison basis's
    specification [R12] — pricing the broad definitions against a premium collected for
    the narrow ones would make the anchor cell internally inconsistent [S11] [S2].
    """
    a = kr_child_anchor
    assert a.broad_def() is False
    assert a.basis_param("broad_def_factor") == 4.0
    for t in (100, 600):
        assert a.inc_rate(t, "cerebral") == a.inc_rate_at(a.age_man(t), "cerebral")

    broad = child.Projection[8]
    assert broad.broad_def() is True and broad.age_man(0) == 30
    assert broad.inc_rate(0, "cerebral") == pytest.approx(
        4.0 * broad.inc_rate_at(30, "cerebral"), rel=1e-14)
    assert broad.inc_rate(0, "cardiac") == pytest.approx(
        4.0 * broad.inc_rate_at(30, "cardiac"), rel=1e-14)
    # and only those two limbs move
    assert broad.inc_rate(0, "cancer") == broad.inc_rate_at(30, "cancer")
    assert broad.inc_rate(0, "fracture") == broad.inc_rate_at(30, "fracture")


def test_the_2026_low_birthrate_discount_runs_for_twelve_months(child, kr_child_anchor):
    """From 2026-04-01 every Korean insurer runs a 1%–5% discount for one year [R6].

    Off in the base run and on at 5% on model point 10, where it multiplies the whole
    office premium for twelve months and then stops.  Whether it applies to the 영업보험료
    or the 보장보험료 is not stated and is [unverified]; the model applies it to the whole
    premium and says so.
    """
    a = kr_child_anchor
    assert a.prem_discount_rate() == 0.0
    assert all(a.prem_discount_factor(t) == 1.0 for t in (0, 11, 12, 239))

    discounted = child.Projection[10]
    assert discounted.prem_discount_rate() == 0.05
    assert discounted.prem_discount_mths() == 12
    assert all(discounted.prem_discount_factor(t) == 0.95 for t in range(0, 12))
    assert all(discounted.prem_discount_factor(t) == 1.0 for t in (12, 13, 239))
    assert discounted.premium_mth() == 24000.0
    assert discounted.premium_foetal_mth() == 3000.0
    assert discounted.premiums(0) == pytest.approx(
        (24000.0 + 3000.0) * 0.95 * 1.0, rel=1e-14)
    assert discounted.premiums(12) == pytest.approx(
        27000.0 * discounted.pols_pay(12), rel=1e-14)
    assert discounted.premiums(17) == pytest.approx(
        24000.0 * discounted.pols_pay(17), rel=1e-14)


def test_the_best_estimate_mortality_lever_is_one_in_the_base_run(child,
                                                                 kr_child_anchor):
    """``mort_be_factor`` is 1.0 on the shipped table and 1.10 on model point 10.

    The table is a [std] population construction with no prudential margin to unwind, so
    scaling it would invent one.  The hook exists for a user replacing ``mort_table.csv``
    with a company valuation table, and it must reach the insured's mortality and nothing
    else — the 계약자's limb is read straight off the table.
    """
    a = kr_child_anchor
    assert a.mort_be_factor() == 1.0
    assert a.mort_rate(100) == a.mort_rate_at_age(a.age_man(100), "M")

    stressed = child.Projection[10]
    assert stressed.mort_be_factor() == 1.1
    assert stressed.mort_rate(100) == pytest.approx(
        1.1 * stressed.mort_rate_at_age(stressed.age_man(100), "M"), rel=1e-14)
    assert stressed.mort_rate_payer(0) == stressed.mort_rate_at_age(
        stressed.payer_age(), stressed.payer_sex())
    assert stressed.mort_rate(0) == 0.0            # still nothing before birth


def test_the_three_lapse_bases_run_side_by_side(child, kr_child_anchor):
    """원칙모형, 적용해지율 and a level comparison vector, each with its own shape.

    Shipping the first two beside each other is exactly the comparison the 2024 계리가정
    guideline obliges an insurer departing from the 원칙모형 to disclose [REG-R27] [R11].
    The undiscounted difference they make is the notes' own sensitivity: −₩8,061,541 on
    model point 5 against −₩13,085,435 on the anchor.
    """
    a = kr_child_anchor
    assert a.lapse_basis() == "loglinear"
    assert a.lapse_rate(0) == pytest.approx(0.05, rel=1e-14)
    assert a.lapse_rate(240) == 0.008
    assert a.lapse_rate(239) == pytest.approx(
        math.exp(math.log(0.05) + (239 / 240) * (math.log(0.001) - math.log(0.05))),
        rel=1e-14)
    assert a.lapse_rate(239) < 0.0011           # converging on the guideline's 0.1%

    disclosed = child.Projection[5]
    assert disclosed.lapse_basis() == "disclosed"
    assert disclosed.lapse_rate(0) == 0.05 and disclosed.lapse_rate(119) == 0.05
    assert disclosed.lapse_rate(120) == 0.03 and disclosed.lapse_rate(179) == 0.03
    assert disclosed.lapse_rate(180) == 0.01 and disclosed.lapse_rate(239) == 0.01
    assert disclosed.lapse_rate(240) == 0.005
    assert disclosed.result_cf()["net_cf"].sum() == pytest.approx(-8061541.17, abs=WON)

    level = child.Projection[8]
    assert level.lapse_basis() == "flat"
    assert all(level.lapse_rate(t) == 0.03 for t in (0, 100, 239, 240, 800))


def test_the_term_and_the_payment_term_envelopes(child, kr_child_anchor):
    """110세만기, 30세만기 and 30년납, each changing the horizon and nothing else.

    ``proj_len()`` is ``12 × (term_age − issue_age) + 1`` — the **number** of projected
    months, so the last index is ``proj_len() - 1`` — and the 환급률 taper is indexed on
    the **fraction** of the term run off, which is what lets one shipped grid serve a
    30세만기, a 100세만기 and a 110세만기 contract without re-basing the published figures.
    """
    assert kr_child_anchor.proj_len() == 1201

    long_term = child.Projection[6]
    assert long_term.term_age() == 110 and long_term.issue_age() == 0
    assert long_term.proj_len() == 1321
    assert long_term.foetal() is True and long_term.birth_month() == 3
    assert long_term.foetal_cover_end() == 15 and long_term.age_man(1320) == 109

    short = child.Projection[9]
    assert short.term_age() == 30 and short.proj_len() == 361
    assert short.refund_ratio(360) == 0.0
    assert short.refund_ratio(120) == pytest.approx(0.737, rel=1e-14)
    assert short.runoff(180) == 0.5
    assert short.equiv_premium_mth_pp() == pytest.approx(2968.47, abs=WON)
    assert short.premium_mth() == 3026.0

    long_pay = child.Projection[10]
    assert long_pay.prem_period_years() == 30 and long_pay.prem_end() == 359
    assert long_pay.surr_chg_period() == 84         # still the seven-year cap
    assert long_pay.premium_mth_pp(359) > 0.0 and long_pay.premium_mth_pp(360) == 0.0


def test_the_model_point_premiums_are_inputs_and_the_computed_one_governs(child):
    """No Korean carrier publishes a rate table by age and duration, so the premium is an input.

    ``equiv_premium_mth_pp()`` computes what the shipped basis actually implies, and where
    the two differ the computed figure governs.  Model point 9 is the closest of the ten —
    ₩3,026 shipped against ₩2,968.47 computed, 1.90% **over**, the only shipped point on
    the far side of its own equivalence premium — and the anchor is 11.00% short: reading
    the two against each other is the only calibration this file can make.
    """
    short = child.Projection[9]
    assert short.equiv_premium_mth_pp() / short.premium_mth() - 1.0 == pytest.approx(
        -0.0190, abs=0.0005)
    anchor = child.Projection[1]
    assert anchor.equiv_premium_mth_pp() > anchor.premium_mth()
    assert anchor.equiv_premium_mth_pp() / anchor.premium_mth() - 1.0 == pytest.approx(
        0.1100, abs=5e-5)


def test_invalid_enumerations_raise_rather_than_defaulting(tmp_path):
    """A mistyped ``sex``, ``cv_form``, ``payer_sex`` or ``lapse_basis`` is an error.

    Four columns of the model point table are enumerations, and a silent fallback on any
    of them would project a contract nobody described — a female cell priced male, a
    suppressed form paying a 표준형 value.  Each is validated where it is read.
    """
    edited = edited_model(tmp_path, "Child_KR_S_enums", {
        (2, "sex"): "X",
        (3, "cv_form"): "nil",
        (5, "payer_sex"): "?",
        (7, "lapse_basis"): "guess",
    })
    try:
        with pytest.raises(FormulaError):
            edited.Projection[2].sex()
        with pytest.raises(FormulaError):
            edited.Projection[3].cv_form()
        with pytest.raises(FormulaError):
            edited.Projection[5].payer_sex()
        with pytest.raises(FormulaError):
            edited.Projection[7].lapse_basis()
        # and the untouched anchor still projects
        assert edited.Projection[1].net_cf(0) == pytest.approx(
            -298646.2075780353, abs=CASH)
    finally:
        edited.close()


# ---------------------------------------------------------------------------
# The [std] assumptions, read off the model


def test_the_std_scalar_references_are_the_ones_the_notes_state(child):
    """Every [std] scalar the notes and ``model.md`` tabulate, read off the References.

    These are not derived quantities: they are the choices the reference implementation
    makes where Korea publishes nothing, and each is listed with a rationale in
    ``model.md`` under *Standardizations used*.  Asserting them here means a silent change
    to an assumption fails a test rather than quietly moving a result somewhere else in
    this module.
    """
    refs = child.Projection.refs
    assert refs["prem_int_rate"] == 0.0275        # 보장부분 적용이율, observed 2.50–3.00%
    assert refs["decl_rate"] == 0.017             # 공시이율 at 2026-07 [S2]
    assert refs["min_guar_rate"] == 0.003         # 최저보증이율 [S2]
    assert refs["avg_decl_rate"] == 0.025         # 평균공시이율 [S2]
    assert refs["ref_age"] == 40                  # 기준연령 요건, 남자 만 40세 [REG-R9]
    assert refs["ref_sex"] == "M"
    assert refs["surr_chg_prem_rate"] == 0.05     # [별표 14]'s 5%
    assert refs["surr_chg_sa_rate"] == 0.01       # 10/1000 of the 보험가입금액
    assert refs["surr_chg_cap_months"] == 13.0    # the FSC's 보장성보험 13배 [REG-R29]
    assert refs["surr_chg_max_coef"] == 20        # 보험기간(최대 20년) [REG-R20]
    assert refs["surr_chg_max_years"] == 7        # 해약공제기간 [REG-R19]
    assert refs["acq_cost_ratio"] == 0.9          # of the 표준해약공제액
    assert refs["comm_init_share"] == 0.65
    assert refs["comm_renewal_rate"] == 0.03
    assert refs["expense_maint_pp"] == 400.0
    assert refs["expense_maint_prem_rate"] == 0.05
    assert refs["expense_claim_pp"] == 30000.0
    assert refs["inflation_rate"] == 0.02         # the Bank of Korea's own target
    assert refs["liability_cycle_mths"] == 36     # the 3년만기 갱신형 block
    assert refs["roll_fwd_tol"] == 1e-10
    assert refs["val_tol"] == 1e-07


def test_the_std_basis_table_is_the_one_the_notes_state(child):
    """Thirteen scalars that turn an incidence into a cost, each with its own provenance.

    ``basis_table.csv`` is where this product keeps the assumptions that are neither rates
    nor amounts — a mean 장해지급률, a surgery rate given a diagnosis, a per-stay cap
    factor, a foetal-loss rate.  Every one of them is [std] and every row says so, because
    for this product the retrieved documents bound almost none of them.
    """
    table = child.Data.basis_table()
    expected = {
        "disab_severity": 0.12, "disease_disab_severity": 0.15,
        "surgery_rate_cancer": 0.85, "surgery_rate_cerebral": 0.50,
        "surgery_rate_cardiac": 0.70, "liability_severity": 600000.0,
        "hosp_cap_factor": 0.92, "waiver_disab_share": 0.08,
        "payer_disab_ratio": 0.25, "leak_share": 0.40, "void_rate_ann": 0.012,
        "broad_def_factor": 4.0, "net_prem_ratio": 0.75,
    }
    assert set(table.index) == set(expected)
    for name, value in expected.items():
        assert float(table.loc[name, "value"]) == value, name
    assert table["provenance"].str.startswith("[std]").all()


def test_the_neonatal_module_limbs_are_the_ones_the_notes_state(child):
    """Nine limbs, two timings, and two of them **day-capped rather than amount-capped**.

    ``incubator`` is ₩50,000 × max(0, min(days, 60) − 2) and ``perinatal_cash`` is
    ₩10,000 × max(0, min(days, 120) − 3) [S1] [S8], so their ``units`` are expected paid
    days after the contractual deduction and inside the cap.  The module's cost is a
    length-of-stay question, and the supervisor's own worked claim — ₩16,836,420 on a
    32-week, 1.84 kg birth [R3] — is two orders of magnitude above the expected cost.
    """
    table = child.Data.neonatal_table()
    assert len(table) == 9
    assert set(table["timing"]) == {"birth", "block"}
    assert set(table.index[table["timing"] == "birth"]) == {
        "birth_risk_low", "birth_risk_disab", "birth_risk_severe", "preterm"}
    assert set(table.index[table["timing"] == "block"]) == {
        "incubator", "perinatal_cash", "congenital_diag", "congenital_surg",
        "neonatal_haem"}
    assert float(table.loc["incubator", "amount"]) == 50000.0
    assert float(table.loc["incubator", "units"]) == 8.0
    assert float(table.loc["perinatal_cash", "amount"]) == 10000.0
    assert float(table.loc["perinatal_cash", "units"]) == 7.5
    assert float(table.loc["neonatal_haem", "amount_ratio"]) == 0.2
    assert table["provenance"].str.startswith("[std]").all()

    a = child.Projection[1]
    sa = a.sum_assured("neonatal")
    for timing, total in (("birth", NEONATAL_BIRTH), ("block", NEONATAL_BLOCK)):
        rows = table[table["timing"] == timing]
        built = sum(float(r["freq"]) * float(r["units"])
                    * (float(r["amount"]) + float(r["amount_ratio"]) * sa)
                    for _, r in rows.iterrows())
        assert a.neonatal_cost_pp(timing) == pytest.approx(built, rel=1e-14)
        assert a.neonatal_cost_pp(timing) == pytest.approx(total, rel=1e-14)


def test_expense_inflation_compounds_over_a_hundred_years(kr_child_anchor):
    """2% a year compounds to **7.24**, so the assumption is not a detail on this product.

    Per-policy maintenance is ₩400 a month at issue and ₩2,898 at the 100세 계약해당일, it
    runs for the whole term rather than to 납입완료, and it is the largest single expense
    item in the projection.  At 1% the terminal charge would be ₩1,081.93 and at 3%
    ₩7,687.45 — a spread of seven times on the same charge, and no Korean expense basis
    exists to anchor any of the three.
    """
    a = kr_child_anchor
    assert a.inflation_factor(0) == 1.0
    assert a.inflation_factor(1200) == pytest.approx(7.244646118252348, rel=TRACE)
    assert 400.0 * a.inflation_factor(1200) == pytest.approx(2897.86, abs=WON)
    assert 400.0 * 1.01 ** 100 == pytest.approx(1081.93, abs=WON)
    assert 400.0 * 1.03 ** 100 == pytest.approx(7687.45, abs=WON)
    # maintenance runs for the whole term, not to 납입완료
    assert a.expenses(1199) == pytest.approx(
        400.0 * a.inflation_factor(1199) * a.pols_if(1199), rel=1e-14)
    assert a.expenses(1200) == 0.0
    df = a.result_cf()
    assert df.loc[240:, "expenses"].sum() > 0.5 * df["expenses"].sum()


def test_the_claim_expense_is_its_own_column_and_is_charged_on_events(
        child, kr_child_anchor):
    """₩30,000 per event on the month's claim events, deaths and voids, uninflated.

    It is published in its own column and deducted explicitly in ``net_cf``; it is **not**
    inside ``expenses``.  The exposure is a count of discrete claim events — the two
    후유장해 limbs, the four diagnosis limbs, 골절, 화상 and 배상책임 — and not hospital
    days, which are metered rather than counted.
    """
    a = kr_child_anchor
    assert child.Projection.refs["expense_claim_pp"] == 30000.0
    for t in (0, 5, 240, 1199):
        assert a.claim_expenses(t) == pytest.approx(
            30000.0 * (a.claim_count_pp(t) * a.pols_if(t) + a.pols_death(t)
                       + a.pols_void(t)), rel=1e-14), t
    # hospital days are not events
    assert a.claim_count_pp(5) == pytest.approx(
        a.inc_rate_mth(5, "disability") + a.inc_rate_mth(5, "disease_disab")
        + sum(a.inc_rate_mth(5, c) * a.frac_open(5, c) * a.cover_open(5, c)
              for c in ("cancer", "minor_cancer", "cerebral", "cardiac"))
        + a.inc_rate_mth(5, "fracture") + a.inc_rate_mth(5, "burn")
        + a.inc_rate_mth(5, "liability"), rel=1e-14)
    df = a.result_cf()
    assert "claim_expenses" in df.columns and "expenses" in df.columns
    assert df["claim_expenses"].sum() == pytest.approx(TOTALS["claim_expenses"],
                                                       abs=CASH)


# ---------------------------------------------------------------------------
# Inputs


def test_inputs_live_beside_the_model():
    """The seven input CSVs sit in the model folder's parent directory, and nothing else.

    Inputs are **external files** following ``annuallife.TradLife_A``, so the model folder
    holds formulas only and a diff of the model shows logic changes alone.  The
    consequence worth knowing is that the model is not portable on its own: copying
    ``Child_KR_S`` without its parent's CSVs produces a model that reads and then fails on
    first evaluation.
    """
    assert INPUT_CSVS == {p.name for p in CSV_DIR.iterdir() if p.suffix == ".csv"}
    assert not [p for p in MODEL_DIR.rglob("*.csv")]
    assert (CSV_DIR / "run.py").is_file()
    assert (CSV_DIR / "model.md").is_file()


def test_the_csvs_are_utf8_without_a_bom():
    """The provenance columns are Korean, so the encoding is load-bearing."""
    for name in sorted(INPUT_CSVS):
        raw = (CSV_DIR / name).read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"{name} carries a BOM"
        raw.decode("utf-8")


def test_the_runner_prints_pure_ascii():
    """``run.py`` and everything it prints survive a Windows console under any code page.

    Korean is romanized there rather than written in hangul and amounts are labelled
    ``KRW``, which is the house rule for every runner in this repository and the reason
    this product's runner writes "eorini boheom" and "taea gaip".
    """
    raw = (CSV_DIR / "run.py").read_bytes()
    raw.decode("ascii")
    text = raw.decode("ascii")
    assert "eorini boheom" in text and "KRW" in text
    assert "boheom nai" in text and "man nai" in text


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Every row is a [std] construction, and marking them is what stops a mistake.

    Korea publishes no life table this model could ship: 보험개발원 releases only 평균수명
    and 기대여명 from the 경험생명표 [REG-R33] [REG-R34], so the file is shaped on the
    통계청 완전생명표 age pattern [REG-R38] [REG-R39] and is **not** a 경험생명표 rate.
    The shape a child policy is exposed to is the infant peak and the childhood trough,
    neither of which a table graduated from age 20 upwards would carry.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert len(table) == 242                      # two sexes, ages 0 to 120
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith("[std]").all()
    assert table["provenance"].str.contains("경험생명표").all()
    male = table[table["sex"] == "M"].set_index("age")["mort_rate"]
    assert male.loc[0] == 0.0025                  # the infant peak
    assert male.loc[5] == 0.00012
    assert male.loc[10] == 0.00009                # the childhood trough
    assert male.loc[0] > male.loc[1] > male.loc[10] < male.loc[20]
    assert male.loc[120] == 1.0


def test_the_shipped_incidence_table_marks_its_own_provenance():
    """Eleven causes at fourteen pivots, every row [std] save the two that are not.

    Nothing on Korean child incidence was retrieved from 보험개발원, 국가암정보센터 or
    통계청 [REG-R4] [REG-R2], so every rate is a construction whose provenance names the
    authority its *shape* rests on.  The exception is the row that anchors the file: the
    일반상해 후유장해 발생률 at 5세 [S1], which is cited as the observation it is.
    """
    table = pd.read_csv(CSV_DIR / "incidence_table.csv")
    assert list(table.columns) == ["cause", "sex", "age", "rate", "provenance"]
    assert len(table) == 11 * 2 * 14
    assert set(table["cause"]) == set(CAUSES)
    assert sorted(set(table["age"])) == [0, 1, 5, 10, 15, 20, 30, 40, 50, 60, 70,
                                         80, 90, 100]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith(("[std]", "[S1]")).all()
    assert (table["rate"] > 0).all()
    anchored = table[(table["cause"] == "disability") & (table["age"] == 5)]
    assert set(anchored["rate"]) == set(PUBLISHED_DISABILITY_RATE.values())
    assert anchored["provenance"].str.contains(r"\[S1\]").all()


def test_the_lapse_table_carries_the_principle_model_and_its_disclosed_comparator():
    """Three bases, and the pair the 2024 계리가정 guideline asks an insurer to compare.

    ``loglinear`` is the guideline's 원칙모형 with its two prescribed endpoints — 0.1% at
    납입완료, 0.8% afterwards [REG-R27] [R11] — and ``disclosed`` is the only 적용해지율
    any Korean child product publishes [S1].  The functional form between the endpoints was
    never converted from HWP and is [unverified] at instrument level, which the file says.
    """
    table = pd.read_csv(CSV_DIR / "lapse_table.csv", index_col="lapse_basis")
    assert set(table.index) == {"loglinear", "disclosed", "flat"}
    assert float(table.loc["loglinear", "first_year_rate"]) == 0.05
    assert float(table.loc["loglinear", "completion_rate"]) == 0.001
    assert float(table.loc["loglinear", "ultimate_rate"]) == 0.008
    assert float(table.loc["disclosed", "first_year_rate"]) == 0.05
    assert float(table.loc["disclosed", "ultimate_rate"]) == 0.005
    assert (table.loc["flat"][["first_year_rate", "completion_rate",
                              "ultimate_rate"]].astype(float) == 0.03).all()
    assert "unverified" in table.loc["loglinear", "provenance"]
    assert table["provenance"].str.contains(r"\[REG-R27\]|\[S1\]|\[std\]").all()


def test_the_refund_grid_is_the_published_one_plus_a_calibrated_taper():
    """``build`` is the 상품요약서 grid [S2]; ``taper`` is the [std] terminal collapse.

    Splitting the progression in two is what lets one shipped grid serve every 보험기간
    without re-basing the published figures, and the taper's 0.95 node is calibrated so
    that 1.589 × 0.1007 reproduces the published 16.0% at 95 years on a 100세만기 contract.
    """
    table = pd.read_csv(CSV_DIR / "av_table.csv")
    assert list(table.columns) == ["curve", "key", "value", "provenance"]
    build = table[table["curve"] == "build"].set_index("key")["value"]
    for years, published in ((1, 0.0), (3, 0.456), (5, 0.625), (10, 0.737),
                             (15, 0.783), (20, 0.826), (30, 1.012), (40, 1.225),
                             (50, 1.441), (60, 1.589)):
        assert build.loc[years] == published, years
    taper = table[table["curve"] == "taper"].set_index("key")["value"]
    assert taper.loc[0.0] == 1.0 and taper.loc[0.85] == 1.0
    assert taper.loc[0.95] == 0.1007 and taper.loc[1.0] == 0.0
    assert 1.589 * 0.1007 == pytest.approx(0.16001230, abs=5e-9)
    published_rows = table[table["provenance"].str.startswith("[S2]")]
    assert len(published_rows) == 11          # the grid prints 0.0% at both 0 and 1 year
    assert set(published_rows["curve"]) == {"build"}
    shaped = table[table["provenance"].str.startswith("[std]")]
    assert set(shaped["curve"]) == {"build", "taper"}


def test_an_input_can_be_swapped_without_touching_a_formula(tmp_path):
    """Point a filename Reference at a different file and the projection follows it.

    The promise ``Data`` makes is that a company basis replaces a shipped one by swapping
    a same-schema CSV, with no formula change anywhere.  Halving every incidence rate must
    halve the morbidity benefit of a month exactly, because nothing between the table and
    the benefit rescales it.
    """
    dest = tmp_path / MODEL_DIR.name
    shutil.copytree(MODEL_DIR, dest)
    for csv in CSV_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)
    table = pd.read_csv(tmp_path / "incidence_table.csv")
    table["rate"] = table["rate"] * 0.5
    table.to_csv(tmp_path / "half_incidence.csv", index=False)

    model = mx.read_model(dest, name="Child_KR_S_swap")
    try:
        before = model.Projection[1].inc_rate(240, "fracture")
        before_benefit = model.Projection[1].benefit_pp(240, "EVENT")
        model.Data.incidence_file = "half_incidence.csv"
        model.Data.clear_all()
        model.Projection.clear_all()
        after = model.Projection[1].inc_rate(240, "fracture")
        assert after == pytest.approx(0.5 * before, rel=1e-14)
        # the benefit follows it, to within the convexity of the monthly conversion
        assert model.Projection[1].benefit_pp(240, "EVENT") == pytest.approx(
            0.5 * before_benefit, rel=0.01)
        assert model.Data.incidence_table()["rate"].max() == pytest.approx(10.0)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Structure and documentation


def test_result_cf_carries_the_library_column_vocabulary(kr_child_anchor):
    """``pols_if`` first, ``net_cf`` last, the eleven benefit kinds between, no subtotal.

    The house contract for a result table: a frame indexed by ``t`` with the in-force
    count first, income-positive ``net_cf`` last, the claim handling expense in its own
    column beside ``expenses``, and the benefit outgo published as its kinds rather than
    as a ``claims`` column — so the columns sum to ``net_cf``.
    """
    df = kr_child_anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(0, 1201))
    assert df.columns[0] == "pols_if" and df.columns[-1] == "net_cf"
    assert list(df.columns) == ["pols_if"] + list(CF_COLUMNS)
    assert all(re.fullmatch(r"[a-z][a-z0-9_]*", c) for c in df.columns)
    assert df.notna().all().all()
    assert "claims" not in df.columns
    assert df["premiums"].iloc[0] > 0.0            # income positive
    assert df["net_cf"].iloc[0] < 0.0              # and outgo negative


def test_result_pols_and_result_val_publish_what_the_notes_read(kr_child_anchor):
    """The two ages side by side, the two compartments, and both surrender values.

    ``result_pols()`` is where the five-month offset a foetal contract carries for its
    whole life can be read off any row, and ``result_val()`` is where the notional 표준형
    value and the amount this model point actually pays sit in adjacent columns, so the
    무해지 cliff and the value an instant before it are visible together.
    """
    dp = kr_child_anchor.result_pols()
    assert list(dp.columns) == ["pols_if", "pols_pay", "pols_waived", "pols_void",
                                "pols_death", "pols_lapse", "pols_maturity",
                                "age", "age_man", "mort_rate", "lapse_rate",
                                "waiver_rate"]
    assert dp.index.name == "t" and len(dp) == 1201
    assert dp.notna().all().all()
    assert (dp["pols_pay"] + dp["pols_waived"] - dp["pols_if"]).abs().max() < 1e-12
    assert (dp["age"] - dp["age_man"]).loc[5:].isin([0, 1]).all()

    dv = kr_child_anchor.result_val()
    assert list(dv.columns) == ["cum_prem_pp", "refund_ratio", "cv_std_pp", "cv_pp",
                                "surr_chg_pp", "av_pp"]
    assert dv.index.name == "t" and len(dv) == 1201
    assert dv.notna().all().all()
    assert (dv["cv_pp"] <= dv["av_pp"] + 1e-9).all()


def test_net_cf_carries_the_notes_own_sign(child, kr_child_anchor):
    """Income positive, and no outgo-positive ``liability_cf`` companion beside it.

    The library-wide sign convention, and the notes' own, so the model publishes one
    stream and not two.  A model that flipped the sign would still close every identity in
    this module, which is why the orientation is asserted directly.
    """
    a = kr_child_anchor
    assert a.net_cf(100) == pytest.approx(
        a.premiums(100) - a.claims(100) - a.claim_expenses(100) - a.expenses(100)
        - a.commissions(100), rel=1e-14)
    assert a.net_cf(100) > 0.0                     # a premium-paying month is income
    assert a.net_cf(600) < 0.0                     # a paid-up month is outgo
    assert "liability_cf" not in child.Projection.cells
    assert "income positive" in flat(child.Projection.cells["net_cf"].doc)


def test_the_docstrings_describe_the_current_structure(child):
    """The model, both Spaces and the cells that carry this product's two novelties.

    Documentation drifts and there is no other way to catch it.  The phrases asserted here
    are the ones a reader needs to find: what the model is, what is external, what is read
    once per model, and the two mechanics — cover attaching at birth, a decrement on a life
    who is not the insured — that no other model in the six libraries carries.
    """
    doc = flat(child.doc)
    assert "mechanics demonstration" in doc
    assert "external" in doc and "once per model" in doc
    assert "Data" in doc and "Projection" in doc
    assert "태아가입" in doc and "납입면제" in doc
    assert "1,200" in doc

    proj = flat(child.Projection.doc)
    assert "Notes symbol" in proj
    assert "proj_len" in proj and "model_point" in proj
    assert "보험나이" in proj and "만나이" in proj
    assert "void, then the waiver, then mortality, then lapse" in proj
    assert "birth_month" in proj

    data = flat(child.Data.doc)
    assert "TradLife_A" in data
    assert "input_dir" in data and "model_point_table" in data

    born = flat(child.Projection.cells["born"].doc)
    assert "birth and not at the 계약일" in born
    payer = flat(child.Projection.cells["waiver_payer"].doc)
    assert "decrement on a life who is not the insured" in payer


def test_the_projection_docstring_describes_the_shipped_model_points(child):
    """The model docstring's account of the ten points matches the shipped table.

    A model docstring that describes a table it no longer ships is worse than none, and
    the anchor's own description — a 태아 contract, priced male, with birth at policy
    month 5 — is the sentence a reader checks the worked example against.
    """
    doc = flat(child.doc)
    assert "Ten, covering both sexes" in doc
    assert "birth at policy month 5" in doc
    table = child.Data.model_point_table()
    assert len(table) == 10
    reader = flat(child.Data.cells["model_point_table"].doc)
    assert "point_id = 1" in reader and "anchor" in reader


def test_the_notes_and_the_model_agree_on_the_worked_example_cell():
    """The technical notes print the anchor's own numbers, not a spreadsheet's.

    Six figures are spot-checked in the notes' own text — the issue-month strain, the
    month of birth, the undiscounted total, the equivalence premium, the 표준해약공제액 and
    the once-only ledger at the 만기 — because the worked example is only worth having if
    the document and the model cannot drift apart.  The whole table is asserted cell by
    cell above; this asserts that the *document* carries it.
    """
    notes = io.open(CSV_DIR / "technical-notes.md", encoding="utf-8").read()
    assert "-298,646.2076" in notes or "−298,646.2076" in notes
    assert "50,960.7703370201" in notes
    assert "13,085,434.9998" in notes
    assert "31,079.588559199034" in notes
    assert "364,000.0000" in notes
    assert "0.4023261296" in notes
    assert "99 years and 7 months" in notes


def test_round_trip_is_stable(tmp_path):
    """read → write → re-read reproduces the goldens and the same file set.

    The serialized form is the model, so a formula that survives a write and comes back
    changed is a broken model however it behaves in memory.  Inputs are external and must
    travel with it, which is asserted by copying them and projecting the anchor again.
    """
    model = mx.read_model(MODEL_DIR, name="Child_KR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in CSV_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Child_KR_S_rt")
    try:
        anchor = reread.Projection[1]
        assert anchor.proj_len() == 1201 and anchor.birth_month() == 5
        for t in (0, 5, 17):
            expected = WORKED_EXAMPLE_CF[t]
            assert anchor.pols_if(t) == pytest.approx(expected[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(expected[-1], abs=CASH)
        assert anchor.cv_pp(240) == pytest.approx(5550720.0, abs=CASH)
        assert anchor.surr_chg_cap_pp() == pytest.approx(SURR_CHG_CAP, rel=TRACE)
        assert "Notes symbol" in reread.Projection.doc
        assert {c for c in reread.Projection.cells
                if c.startswith("check_") and not c.endswith("_resid")} == CHECK_CELLS
        assert anchor.check_cover_at_birth() is True
        assert anchor.check_neonatal_term() is True
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
