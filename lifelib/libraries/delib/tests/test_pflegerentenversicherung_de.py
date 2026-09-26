"""Golden and structural tests for Pflege_DE_S.

The golden values are the worked example in
products/pflegerentenversicherung/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: an individual, single-life, underwritten German
*Pflegerentenversicherung* on a woman aged 45 at entry, new business
(``duration_mth_init = 0``, ``status = aktiv``), a *vereinbarte Pflegerente* of
1 000,00 EUR a month at *Pflegegrad* 5, the ``delib_std`` *Leistungsstaffel* of
0 / 30 / 50 / 75 / 100 % across grades 1 to 5, a **level monthly Beitrag payable for
life** (``prem_end_age = 110`` equal to ``omega_age``, ``prem_mode = monthly`` so
``prem_mode_months = 1``), no premium override — ``premium_mth = 0.0`` is the sentinel
that makes the model strike the *Beitrag* by equivalence — standard rates
(``rating_factor = 1.00``), and **every switchable option off**: no *Wartezeit*, no
*Karenzzeit*, no *Leistungsdynamik*, no *Beitragsrückgewähr*, no *Stornoabzug*, no
*Überschussbeteiligung* and no behaviour module.  Model point 1 is that cell.
``pols_if_init() = 1.0`` and ``proj_len() = 12 x (110 - 45) = 780`` -- the number of
projected months, the frame's exclusive end -- so the frame is ``range(0, 780)``:
780 monthly rows, ``t = 0 ... 779``, covering attained ages 45 to 109, of which the notes print fourteen plus
a Total row over all of them.  The equivalence gives ``premium_mth_pp() = 64.198409`` EUR
a month, from ``A = 17,789.761930``, ``U = 313.500018``, ``G = 892.884210`` and
``C = 69.389246``.

Goldens are hard-coded rather than pickled so a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent, the
``pols_*`` ledgers to six decimals, and the totals at **full precision** -- 13 200,11 EUR
of *Pflegerente* that way against 13 200,02 EUR if the 780 rounded cells are added, and
-1 527,65 EUR of ``net_cf`` against -1 527,51 EUR.  The notes print both, and both are
asserted, with the reason the gap does not cancel: 107 of the 780 ``claims_annuity`` cells
are positive amounts below half a cent and every one of them rounds down.

What this module asserts, beyond the fourteen printed rows and the totals: the equivalence
premium reached two independent ways from ``A``, ``U``, ``G`` and ``C``; month 0 rebuilt
term by term with a calculator; the first month's decrements rebuilt from the two annual
rates through the forces, in the declared processing order with lapse acting **last**; the
first *Pflegerente* payment rebuilt grade by grade; the closure identity at the limiting
age; the sign pattern and where ``net_cf`` crosses zero; the male twin's ten printed rows
and the unisex cross-subsidy; the four-cell variant table (anchor, male twin, ``bahr``
grid, *Leistungsdynamik*); the six published ``check_*`` identities with their per-``t``
residuals, ``check_net_cf`` -- delib's first ruling -- among them; and **one test per
numbered modeling pitfall** in the technical notes, seventeen of them.

The whole-model-point-table sweep is deliberately **not** here: the conventions suite owns
the library's single sweep, because a model point's first evaluation is by far the most
expensive thing in the run.
"""
import math

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # the pols_* ledgers displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Pflege_DE_S"][0]

# The notes' worked-example table, in full -- fourteen of the 780 monthly rows.
# t: (age, pols_if, pols_care, pols_prem, premiums, claims_annuity, claims_lapse,
#     expenses, claim_expenses, net_cf)
# claims_death is a column of the frame, is structurally 0.00 at every t here
# (beitragsrueckgewaehr = False) and is omitted from the notes' table rather than printed
# as 780 zeros; it is asserted in the row test all the same.
WORKED_EXAMPLE = {
    0:   (45, 1.000000, 0.000000, 1.000000, 64.20,  0.00,  0.00, 774.31, 0.00, -710.11),
    1:   (45, 0.994793, 0.000056, 0.994748, 63.86,  0.02,  0.00,   3.91, 0.00,   59.93),
    2:   (45, 0.989613, 0.000111, 0.989523, 63.53,  0.04,  0.00,   3.89, 0.00,   59.59),
    12:  (46, 0.939288, 0.000644, 0.938758, 60.27,  0.26,  0.00,   3.71, 0.00,   56.29),
    60:  (50, 0.798781, 0.003771, 0.795452, 51.07,  1.86,  1.60,   3.25, 0.01,   44.35),
    120: (55, 0.698284, 0.009864, 0.689306, 44.25,  5.52,  3.92,   2.95, 0.02,   31.85),
    240: (65, 0.547048, 0.035456, 0.514343, 33.02, 21.39,  5.65,   2.46, 0.07,    3.45),
    360: (75, 0.391509, 0.080375, 0.318167, 20.43, 45.97,  5.83,   1.84, 0.17,  -33.38),
    420: (80, 0.276904, 0.092056, 0.193720, 12.44, 49.35,  4.20,   1.31, 0.21,  -42.64),
    480: (85, 0.143383, 0.073044, 0.078218,  5.02, 36.02,  1.87,   0.67, 0.18,  -33.71),
    540: (90, 0.039295, 0.028934, 0.013981,  0.90, 12.90,  0.30,   0.18, 0.07,  -12.56),
    600: (95, 0.003283, 0.003060, 0.000696,  0.04,  1.20,  0.01,   0.02, 0.01,   -1.19),
    660: (100, 0.000055, 0.000053, 0.000015, 0.00,  0.02,  0.00,   0.00, 0.00,   -0.02),
    779: (109, 0.000000, 0.000000, 0.000000, 0.00,  0.00,  0.00,   0.00, 0.00,    0.00),
}

# The notes' Total row: summed over all 780 rows at full precision, then rounded.
TOTALS = {
    "pols_if": 268.956131, "pols_care": 24.241784, "pols_prem": 247.014740,
    "premiums": 15857.95, "claims_annuity": 13200.11, "claims_lapse": 2191.72,
    "claims_death": 0.00, "expenses": 1941.10, "claim_expenses": 52.67,
    "net_cf": -1527.65,
}

# What the notes get if the 780 already-rounded cells are added instead -- printed there
# precisely because it is not the same number.  The gap does not cancel: 107 of the
# claims_annuity cells are positive amounts below half a cent and all round down.
ROUNDED_CELL_TOTALS = {
    "premiums": 15857.92, "claims_annuity": 13200.02, "claims_lapse": 2191.67,
    "expenses": 1941.02, "claim_expenses": 52.58, "net_cf": -1527.51,
}
SUB_CENT_ANNUITY_CELLS = 107

# The four actuarial values the equivalence is struck from, and what falls out of them.
# P = (A + G + C) / [ U (1 - beta) - a1 ], beta = admin_prem_pct = 0.030,
# a1 = 0.025 x 12 x (85 - 45) = 12.000000 units of P.
A_EPV_BENEFITS = 17789.761930
U_EPV_PREM_UNITS = 313.500018
G_EPV_ADMIN = 892.884210
C_EPV_CLAIM_EXPENSE = 69.389246
PREMIUM_MTH_PP = 64.198409
PREM_NET_LEVEL_PP = 56.745649
BEITRAGSSUMME = 30815.24
ACQ_EXPENSE_PP = 770.38
ZILLMER_UNITS = 12.000000
ADMIN_PREM_PCT = 0.030

# Check 2 of the notes: the first month's decrements, from the two annual rates at
# age 45 female, converted to forces and allocated over one month, with lapse applied
# afterwards -- to the survivors of both insured decrements, not to the opening cohort.
FIRST_MONTH = {
    "mort_rate": 0.00077956, "inc_rate": 0.00066891,
    "mort_force": 0.00077986, "inc_force": 0.00066913, "force_total": 0.00144900,
    "p_act_stay": 0.99987926, "p_act_death": 0.00006498, "p_act_care": 0.00005576,
    "lapse_rate_mth": 0.00514301,
    "pols_act_1": 0.99473687, "pols_lapse_0": 0.00514239,
    "pols_death_0": 0.00006498, "pols_care_1": 0.00005576, "pols_if_1": 0.99479262,
}
# What applying lapse to the opening cohort instead would cost, in the first month alone.
LAPSE_ORDER_GAP = 6.2e-7

# Check 3 of the notes: the first Pflegerente payment, grade by grade.  With
# karenz_months = 0 the month-0 entrants graduate in the same month, so
# pols_pg(1, g) = esc_pg(1, g) = pols_entry(0, g).
# g: (inc_share, pols_pg(1, g), benefit_pct, contribution to claims_annuity(1))
FIRST_ANNUITY = {
    1: (0.20, 0.0000111516, 0.00, 0.00000000),
    2: (0.38, 0.0000211880, 0.30, 0.00635640),
    3: (0.24, 0.0000133819, 0.50, 0.00669095),
    4: (0.13, 0.0000072485, 0.75, 0.00543638),
    5: (0.05, 0.0000027879, 1.00, 0.00278789),
}
FIRST_ANNUITY_TOTAL = 0.02127162

# The entry mix's mean benefit percentage, and the stock-weighted mean the projection
# actually produces -- pitfalls 1 and 17.  The entry-mix mean applied to the whole
# pols_care exposure understates the benefit by 30 %.
ENTRY_MIX_MEAN_PCT = 0.3815
STOCK_WEIGHTED_MEAN_PCT = 0.544519
NAIVE_ANNUITY_TOTAL = 9248.24
# Stock share by Pflegegrad over the whole projection, against entry_share.
STOCK_SHARE = {1: 0.094894, 2: 0.242527, 3: 0.276439, 4: 0.210395, 5: 0.175745}
ENTRY_SHARE = {1: 0.20, 2: 0.38, 3: 0.24, 4: 0.13, 5: 0.05}

# The closure identity at the limiting age: mort_rate is forced to 1.0 at age 109, so the
# two absorbing counts account for the whole policy exactly.
POLS_DEAD_CUM_END = 0.493968
POLS_LAPSE_CUM_END = 0.506032

# The sign pattern the notes read off the frame.
NET_CF_FIRST_NEGATIVE_T = 252          # attained age 66
ANNUITY_PEAK = (407, 49.82)            # month, EUR -- attained age 78
CARE_PEAK = (417, 0.092120)            # month, policies -- attained age 79
TOTAL_OUTGO = 17385.60

# Model point 2 -- the male twin: model point 1 with sex = M and nothing else changed.
# t: (age, pols_if, pols_care, pols_prem, premiums, claims_annuity, claims_lapse,
#     expenses, claim_expenses, net_cf)
MALE_TWIN = {
    0:   (45, 1.000000, 0.000000, 1.000000, 64.20,  0.00, 0.00, 774.31, 0.00, -710.11),
    1:   (45, 0.994719, 0.000045, 0.994683, 63.86,  0.02, 0.00,   3.91, 0.00,   59.93),
    12:  (46, 0.938452, 0.000517, 0.938027, 60.22,  0.21, 0.00,   3.71, 0.00,   56.30),
    120: (55, 0.688060, 0.007570, 0.681181, 43.73,  4.20, 3.87,   2.91, 0.01,   32.74),
    240: (65, 0.517213, 0.024372, 0.494872, 31.77, 14.23, 5.44,   2.35, 0.05,    9.71),
    360: (75, 0.332372, 0.045899, 0.291187, 18.69, 24.19, 5.37,   1.60, 0.10,  -12.56),
    420: (80, 0.214158, 0.047250, 0.172470, 11.07, 22.80, 3.80,   1.05, 0.11,  -16.68),
    480: (85, 0.098388, 0.033682, 0.069319,  4.45, 14.73, 1.72,   0.49, 0.08,  -12.58),
    540: (90, 0.023361, 0.012108, 0.013274,  0.85,  4.73, 0.33,   0.12, 0.03,   -4.36),
    600: (95, 0.001538, 0.001188, 0.000612,  0.04,  0.40, 0.01,   0.01, 0.00,   -0.38),
}
MALE_TOTALS = {
    "pols_if": 251.397804, "pols_care": 13.561865, "pols_prem": 239.326567,
    "premiums": 15364.38, "claims_annuity": 6936.34, "claims_lapse": 2086.29,
    "expenses": 1871.13, "claim_expenses": 28.29, "net_cf": 4442.33,
}
UNISEX_CROSS_SUBSIDY = 5969.98         # net_cf(male) - net_cf(female), undiscounted

# The rates that drive the two cells apart: male active mortality is higher at every age,
# male incidence lower, and incidence wins.
SEX_RATES = {
    ("M", 45, "mort"): 0.0016636521, ("F", 45, "mort"): 0.0007795609,
    ("M", 85, "mort"): 0.1049833018, ("F", 85, "mort"): 0.0699052076,
    ("M", 85, "inc"): 0.1342986651, ("F", 85, "inc"): 0.1808911145,
}

# The notes' switchable-variant table: four cells on the same tables, differing only in
# the model point.  Totals over the whole frame, summed at full precision then rounded.
VARIANTS = {
    1: {"premium": 64.198409, "proj_len": 780, "premiums": 15857.95,
        "claims_annuity": 13200.11, "claims_lapse": 2191.72, "expenses": 1941.10,
        "claim_expenses": 52.67, "net_cf": -1527.65},
    2: {"premium": 64.198409, "proj_len": 780, "premiums": 15364.38,
        "claims_annuity": 6936.34, "claims_lapse": 2086.29, "expenses": 1871.13,
        "claim_expenses": 28.29, "net_cf": 4442.33},
    5: {"premium": 55.444644, "proj_len": 720, "premiums": 12289.30,
        "claims_annuity": 10110.36, "claims_lapse": 1482.02, "expenses": 1556.50,
        "claim_expenses": 57.74, "net_cf": -917.32},
    8: {"premium": 72.038378, "proj_len": 780, "premiums": 17794.54,
        "claims_annuity": 15101.44, "claims_lapse": 2459.37, "expenses": 2093.27,
        "claim_expenses": 52.67, "net_cf": -1912.22},
}

# Pitfall 10 -- what a 2 % Leistungsdynamik actually costs on this basis.
DYNAMIK_ANNUITY_UPLIFT = 0.1440        # +14,4 % on the projected annuity total
DYNAMIK_PREMIUM_UPLIFT = 0.1221        # +12,2 % on the equivalence premium

# Pitfall 9 -- what a six-month Karenzzeit removes, on model point 7.
KARENZ_ENTRIES = 0.253723
KARENZ_GRADUATIONS = 0.228177

# Pitfall 2 -- the in-care mortality multiple is on the FORCE.  On rates the grade-5
# ratio compresses towards 1 as the rate saturates; that compression is the scale, not
# the basis.  age: rate ratio q_5(x) / q_A(x).
CARE_RATE_RATIO_PG5 = {45: 8.97, 85: 6.85, 95: 4.31, 109: 1.00}
MORT_MULT = {1: 1.5, 2: 2.5, 3: 3.5, 4: 6.0, 5: 9.0}

# Pitfall 3 -- the paying state has three exits and only death is absorbing.
REACTIVATION_TOTAL = 0.013768          # sum_t pols_reactiv(t), the flow to aktiv
HERABSTUFUNG_OUT_OF_PG2 = 0.020835     # the flow that ends an annuity and revives a Beitrag
NO_RECOVERY_ANNUITY_TOTAL = 13847.52   # what suppressing Reaktivierung would cost

# The nine input CSVs beside run.py.  model_point_table.csv is the one file with no
# provenance column -- a model point is a configuration, not an assumption, and that is
# the only exemption from the library's second ruling.
INPUT_CSVS = {
    "model_point_table.csv", "benefit_scale_table.csv", "mort_table.csv",
    "incidence_table.csv", "care_table.csv", "lapse_table.csv",
    "surrender_table.csv", "expense_table.csv", "basis_table.csv",
}


# The worked example
@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_pflege_anchor, t):
    """Every cell of the notes' fourteen printed rows, to the displayed precision.

    ``claims_death`` is omitted from the notes' table for width and is asserted here as a
    structural zero: the anchor cell carries no *Beitragsrückgewähr*, so the column exists
    and is empty rather than being dropped from the frame.
    """
    age, pols_if, care, prem_pols, prem, ann, lapse, exp, cexp, net = WORKED_EXAMPLE[t]
    p = de_pflege_anchor
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_care(t) == pytest.approx(care, abs=SIX_DP)
    assert p.pols_prem(t) == pytest.approx(prem_pols, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse, abs=CENT)
    assert p.claims(t, "DEATH") == 0.0
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.claim_expenses(t) == pytest.approx(cexp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(-net, abs=CENT)


def test_the_worked_example_totals_are_summed_at_full_precision(de_pflege_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells.

    The notes print both, because the gap does not cancel: **107 of the 780
    ``claims_annuity`` cells are positive amounts below half a cent**, and every one of
    them rounds down.  ``claim_expenses`` does the same on a 1e-5 paying population.
    """
    df = de_pflege_anchor.result_cf()
    for column, total in TOTALS.items():
        tol = SIX_DP if column.startswith("pols_") else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    for column, total in ROUNDED_CELL_TOTALS.items():
        assert df[column].round(2).sum() == pytest.approx(total, abs=CENT), column
    assert df["net_cf"].sum() - df["net_cf"].round(2).sum() == pytest.approx(
        -0.14, abs=CENT)
    sub_cent = [t for t in df.index if 0.0 < df["claims_annuity"].loc[t] < 0.005]
    assert len(sub_cent) == SUB_CENT_ANNUITY_CELLS
    assert all(round(df["claims_annuity"].loc[t], 2) == 0.0 for t in sub_cent)


def test_the_frame_spans_the_whole_projection(de_pflege_anchor):
    """780 contiguous monthly rows, 0-based, ending at ``proj_len() - 1`` and not at ``proj_len()``.

    ``proj_len()`` is the **number of projected months**, the exclusive end of the frame,
    and it depends on the entry age and the terminal age alone -- reading it as the last
    index, or as a horizon ``duration_mth_init`` shifts, is a listed pitfall.
    """
    p = de_pflege_anchor
    df = p.result_cf()
    assert p.proj_len() == 12 * (110 - 45) == 780
    assert p.duration_mth_init() == 0
    assert df.index.name == "t"
    assert list(df.index) == list(range(p.duration_mth_init(), p.proj_len()))
    assert list(df.index) == list(range(0, 780))
    assert df.index[-1] == p.proj_len() - 1 == 779
    assert len(df) == p.proj_len() - p.duration_mth_init() == 780
    assert df["pols_if"].iloc[0] == p.pols_if_init() == 1.0
    assert p.age(0) == 45 and p.age(779) == 109
    assert p.omega_age() == 110


def test_the_equivalence_premium_is_reached_two_independent_ways(de_pflege_anchor):
    """P = (A + G + C) / [ U (1 - beta) - a1 ], and P also equals ``premium_mth_pp()``.

    There is **no published German rate card for this product to reproduce**, so the four
    actuarial values are published as cells and the closed form is recomputed from them.
    ``U`` is 26,13 years' worth of discounted premium and the expense loading over the net
    level premium is 13,13 %, of which the *Zillmerung* allowance alone is 2,53 EUR.
    """
    p = de_pflege_anchor
    assert p.premium_mth() == 0.0            # the sentinel: derive by equivalence
    assert p.epv_benefits() == pytest.approx(A_EPV_BENEFITS, abs=5e-6)
    assert p.epv_prem_units() == pytest.approx(U_EPV_PREM_UNITS, abs=5e-6)
    assert p.epv_admin() == pytest.approx(G_EPV_ADMIN, abs=5e-6)
    assert p.epv_claim_expense() == pytest.approx(C_EPV_CLAIM_EXPENSE, abs=5e-6)
    numerator = A_EPV_BENEFITS + G_EPV_ADMIN + C_EPV_CLAIM_EXPENSE
    denominator = U_EPV_PREM_UNITS * (1.0 - ADMIN_PREM_PCT) - ZILLMER_UNITS
    assert numerator == pytest.approx(18752.035386, abs=5e-6)
    assert denominator == pytest.approx(292.095018, abs=5e-6)
    assert numerator / denominator == pytest.approx(PREMIUM_MTH_PP, abs=5e-6)
    assert p.premium_mth_pp() == pytest.approx(PREMIUM_MTH_PP, abs=5e-6)
    assert p.prem_net_level_pp() == pytest.approx(PREM_NET_LEVEL_PP, abs=5e-6)
    assert p.prem_net_level_pp() == pytest.approx(
        p.epv_benefits() / p.epv_prem_units(), rel=1e-12)
    assert p.premium_mth_pp() / p.prem_net_level_pp() == pytest.approx(
        1.131336, abs=5e-6)
    assert p.epv_prem_units() / 12.0 == pytest.approx(26.13, abs=0.006)
    # Strike the Zillmerung allowance out of the denominator and the premium falls.
    without_a1 = numerator / (U_EPV_PREM_UNITS * (1.0 - ADMIN_PREM_PCT))
    assert without_a1 == pytest.approx(61.665, abs=0.001)
    assert p.premium_mth_pp() - without_a1 == pytest.approx(2.53, abs=0.006)
    # It lands in the lower half of the argued 50,00-100,00 EUR band, which is a sanity
    # check on the bases and never a market observation.
    assert 50.0 < p.premium_mth_pp() < 100.0


def test_month_zero_rebuilt_with_a_calculator(de_pflege_anchor):
    """``64.198409 - 774.306859 = -710.108450``, and each expense term separately.

    ``expenses(0)`` is the 25 permille *Zillmerung* allowance on the *Beitragssumme*, plus
    one month's per-policy administration, plus 3,0 % of the *Beitrag* just collected.
    Almost the whole of month 0's strain is the first of those three.
    """
    p = de_pflege_anchor
    assert p.pols_if(0) == 1.0
    assert p.pols_prem(0) == 1.0
    assert p.premiums(0) == pytest.approx(PREMIUM_MTH_PP, abs=5e-6)
    assert p.beitragssumme() == pytest.approx(BEITRAGSSUMME, abs=CENT)
    assert p.beitragssumme() == pytest.approx(
        p.premium_mth_pp() * 12.0 * (85 - 45), rel=1e-12)
    assert p.acq_expense_pp() == pytest.approx(ACQ_EXPENSE_PP, abs=CENT)
    assert p.acq_expense_pp() == pytest.approx(
        0.025 * p.beitragssumme(), rel=1e-12)
    assert p.expense_infl_factor(0) == 1.0
    assert p.expenses(0) == pytest.approx(
        770.380907 + 2.000000 + 1.925952, abs=CENT)
    assert 0.03 * p.premiums(0) == pytest.approx(1.925952, abs=5e-6)
    assert p.claim_expenses(0) == 0.0
    assert p.claims(0) == 0.0
    assert p.net_cf(0) == pytest.approx(-710.108450, abs=CENT)
    assert p.net_cf(0) == pytest.approx(p.premiums(0) - p.expenses(0), rel=1e-12)


def test_the_first_months_decrements_from_the_annual_rates(de_pflege_anchor):
    """Check 2 of the notes, which needs nothing but the two CSV rates and a calculator.

    Convert ``q_A(45)`` and ``i(45)`` to forces, allocate one month's exits in proportion,
    then apply the monthly lapse probability **to the survivors of both insured
    decrements**, which is where the declared processing order puts it.  Both orderings
    close ``check_pols_roll_fwd()`` -- which is exactly why the order has to be declared.
    """
    p = de_pflege_anchor
    f = FIRST_MONTH
    assert p.mort_rate(0) == pytest.approx(f["mort_rate"], abs=5e-8)
    assert p.inc_rate(0) == pytest.approx(f["inc_rate"], abs=5e-8)
    assert p.mort_force(0) == pytest.approx(f["mort_force"], abs=5e-8)
    assert p.inc_force(0) == pytest.approx(f["inc_force"], abs=5e-8)
    assert p.mort_force(0) + p.inc_force(0) == pytest.approx(
        f["force_total"], abs=5e-8)
    assert p.p_act_stay(0) == pytest.approx(f["p_act_stay"], abs=5e-8)
    assert p.p_act_death(0) == pytest.approx(f["p_act_death"], abs=5e-8)
    assert p.p_act_care(0) == pytest.approx(f["p_act_care"], abs=5e-8)
    assert p.p_act_stay(0) + p.p_act_death(0) + p.p_act_care(0) == pytest.approx(
        1.0, abs=1e-15)
    assert p.lapse_rate(0) == 0.06
    assert p.lapse_rate_mth(0) == pytest.approx(f["lapse_rate_mth"], abs=5e-8)
    assert p.pols_act(1) == pytest.approx(f["pols_act_1"], abs=5e-8)
    assert p.pols_act(1) == pytest.approx(
        p.p_act_stay(0) * (1.0 - p.lapse_rate_mth(0)), rel=1e-12)
    assert p.pols_lapse(0) == pytest.approx(f["pols_lapse_0"], abs=5e-8)
    assert p.pols_death(0) == pytest.approx(f["pols_death_0"], abs=5e-8)
    assert p.pols_care(1) == pytest.approx(f["pols_care_1"], abs=5e-8)
    assert p.pols_if(1) == pytest.approx(f["pols_if_1"], abs=5e-8)
    assert p.pols_if(1) == pytest.approx(
        1.0 - p.pols_death(0) - p.pols_lapse(0), abs=1e-15)
    # Lapse falls on the survivors, not on the opening cohort -- and the gap is real.
    assert p.lapse_rate_mth(0) - p.pols_lapse(0) == pytest.approx(
        LAPSE_ORDER_GAP, rel=0.02)


def test_the_first_annuity_payment_grade_by_grade(de_pflege_anchor):
    """Check 3 of the notes: ``claims_annuity(1)`` rebuilt from the five entry shares.

    With ``karenz_months = 0`` the month-0 entrants graduate in the month they enter, so
    ``pols_pg(1, g) = esc_pg(1, g) = pols_entry(0, g)`` and the annuity is a five-term
    weighted sum -- never an average percentage on an average survival curve.
    """
    p = de_pflege_anchor
    assert p.karenz_months() == 0
    total = 0.0
    for g, (share, count, pct, contribution) in FIRST_ANNUITY.items():
        assert p.inc_share(g) == pytest.approx(share, rel=1e-12)
        assert p.benefit_pct(g) == pytest.approx(pct, rel=1e-12)
        assert p.pols_entry(0, g) == pytest.approx(count, abs=5e-10)
        assert p.pols_pg(1, g) == pytest.approx(p.pols_entry(0, g), rel=1e-12)
        assert p.esc_pg(1, g) == pytest.approx(p.pols_pg(1, g), rel=1e-12)
        assert p.rente_mth() * pct * p.pols_pg(1, g) == pytest.approx(
            contribution, abs=5e-8)
        total += contribution
    assert total == pytest.approx(FIRST_ANNUITY_TOTAL, abs=5e-9)
    assert p.claims(1, "ANNUITY") == pytest.approx(FIRST_ANNUITY_TOTAL, abs=5e-8)
    assert sum(p.pols_entry(0, g) for g in range(1, 6)) == pytest.approx(
        p.pols_care(1), rel=1e-12)


def test_the_decrements_close_at_the_limiting_age(de_pflege_anchor):
    """Deaths and surrenders account for the whole policy, exactly.

    ``mort_rate`` is forced to 1.0 at ``omega_age() - 1``, so the system is closed rather
    than truncated: the two cumulative counts sum to 1,000000000000 and what survives to
    ``proj_len()`` -- one month past the last projected row, which is ``proj_len() - 1`` --
    is of the order of 1e-23 of a policy.
    """
    p = de_pflege_anchor
    end = p.proj_len()
    assert p.mort_rate(779) == 1.0
    assert p.inc_force(779) == 0.0
    assert p.pols_dead_cum(end) == pytest.approx(POLS_DEAD_CUM_END, abs=SIX_DP)
    assert p.pols_lapse_cum(end) == pytest.approx(POLS_LAPSE_CUM_END, abs=SIX_DP)
    assert p.pols_dead_cum(end) + p.pols_lapse_cum(end) == pytest.approx(
        1.0, abs=1e-12)
    assert p.pols_if(end) < 1e-20
    assert p.check_states() is True


def test_the_sign_pattern_is_the_products_economic_story(de_pflege_anchor):
    """Strain, then thirty years of margin, then a long run-off -- and where it crosses.

    Month 0 is a 710,11 EUR strain, almost all *Zillmerung*.  ``net_cf`` turns negative at
    ``t = 252``, attained age 66, where the incidence curve overtakes the level *Beitrag*
    and where the *Deckungskapital* this model does not compute peaks.  Undiscounted the
    contract collects 15 857,95 EUR and pays 17 385,60 EUR -- not a loss, but the
    consequence of publishing a stream whose income falls thirty years before its outgo.
    """
    p = de_pflege_anchor
    df = p.result_cf()
    assert p.net_cf(0) < -700.0
    assert all(p.net_cf(t) > 0.0 for t in range(1, 251))
    assert p.net_cf(251) > 0.0 and p.net_cf(252) < 0.0
    assert p.age(NET_CF_FIRST_NEGATIVE_T) == 66
    first_negative = min(t for t in range(1, p.proj_len()) if p.net_cf(t) < 0.0)
    assert first_negative == NET_CF_FIRST_NEGATIVE_T
    assert p.net_cf(1) == pytest.approx(59.93, abs=CENT)
    assert p.net_cf(240) == pytest.approx(3.45, abs=CENT)
    peak_t, peak_v = ANNUITY_PEAK
    assert df["claims_annuity"].idxmax() == peak_t
    assert df["claims_annuity"].max() == pytest.approx(peak_v, abs=CENT)
    assert p.age(peak_t) == 78
    care_t, care_v = CARE_PEAK
    assert df["pols_care"].idxmax() == care_t
    assert df["pols_care"].max() == pytest.approx(care_v, abs=SIX_DP)
    assert p.age(care_t) == 79
    outgo = (df["claims_annuity"].sum() + df["claims_lapse"].sum()
             + df["claims_death"].sum() + df["expenses"].sum()
             + df["claim_expenses"].sum())
    assert outgo == pytest.approx(TOTAL_OUTGO, abs=CENT)
    assert df["premiums"].sum() - outgo == pytest.approx(TOTALS["net_cf"], abs=CENT)


# The male twin, and the unisex cross-subsidy
@pytest.mark.parametrize("t", sorted(MALE_TWIN))
def test_male_twin_row(pflegerentenversicherung, t):
    """Model point 2 is model point 1 with ``sex = M`` and nothing else changed."""
    age, pols_if, care, prem_pols, prem, ann, lapse, exp, cexp, net = MALE_TWIN[t]
    p = pflegerentenversicherung.Projection[2]
    assert p.sex() == "M"
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_care(t) == pytest.approx(care, abs=SIX_DP)
    assert p.pols_prem(t) == pytest.approx(prem_pols, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.claim_expenses(t) == pytest.approx(cexp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_male_twin_totals_and_the_unisex_cross_subsidy(
        pflegerentenversicherung, de_pflege_anchor):
    """Priced identically, projecting differently -- the unisex tension, quantified.

    The male cell's annuity total is 52,5 % of the female cell's and its ``net_cf`` total
    is +4 442,33 EUR against -1 527,65 EUR.  That 5 969,98 EUR gap **is** the cross-subsidy
    the unisex rule requires, priced on a 50 / 50 mix.  Two drivers pull opposite ways and
    incidence wins: male mortality is higher, so fewer men survive to claim, and male
    incidence is lower, so fewer of the survivors claim.
    """
    male = pflegerentenversicherung.Projection[2]
    female = de_pflege_anchor
    df = male.result_cf()
    for column, total in MALE_TOTALS.items():
        tol = SIX_DP if column.startswith("pols_") else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert male.premium_mth_pp() == pytest.approx(female.premium_mth_pp(), rel=1e-15)
    assert MALE_TOTALS["claims_annuity"] / TOTALS["claims_annuity"] == pytest.approx(
        0.525, abs=0.001)
    assert MALE_TOTALS["net_cf"] - TOTALS["net_cf"] == pytest.approx(
        UNISEX_CROSS_SUBSIDY, abs=CENT)
    mort = pflegerentenversicherung.Data.mort_table()
    inc = pflegerentenversicherung.Data.incidence_table()
    for (sex, age, kind), value in SEX_RATES.items():
        table = mort if kind == "mort" else inc
        column = "mort_rate" if kind == "mort" else "inc_rate"
        assert float(table.at[(sex, age), column]) == pytest.approx(value, abs=5e-11)
    assert SEX_RATES[("M", 45, "mort")] > SEX_RATES[("F", 45, "mort")]
    assert SEX_RATES[("M", 85, "mort")] > SEX_RATES[("F", 85, "mort")]
    assert SEX_RATES[("M", 85, "inc")] < SEX_RATES[("F", 85, "inc")]


# The switchable variants beside the anchor
@pytest.mark.parametrize("point_id", sorted(VARIANTS))
def test_the_switchable_variant_table(pflegerentenversicherung, point_id):
    """The notes' four-cell table: same tables, different model point.

    Model point 5 enters five years later, so its premium is not comparable with the
    anchor's; the *shape* is.  Model point 8 differs from the anchor only in carrying a
    2 % *Leistungsdynamik*.
    """
    expected = VARIANTS[point_id]
    p = pflegerentenversicherung.Projection[point_id]
    assert p.proj_len() == expected["proj_len"]
    assert p.premium_mth_pp() == pytest.approx(expected["premium"], abs=5e-6)
    df = p.result_cf()
    for column in ("premiums", "claims_annuity", "claims_lapse", "expenses",
                   "claim_expenses", "net_cf"):
        assert df[column].sum() == pytest.approx(expected[column], abs=CENT), column


def test_the_bahr_grid_is_not_simply_a_cheaper_contract(pflegerentenversicherung,
                                                        de_pflege_anchor):
    """Model point 5 insures *Pflegegrad* 1, and the effect surfaces in claim expenses.

    The middle steps are roughly two thirds of ``delib_std``'s, but grade 1 is insured, so
    a grade-1 life generates an annuity payment and a per-payment cost: ``claim_expenses``
    is **higher** on point 5 (57,74 EUR) than on the anchor (52,67 EUR) despite a frame
    sixty months shorter.  The same life is **waived** on ``bahr`` and **pays** on
    ``delib_std``.
    """
    bahr = pflegerentenversicherung.Projection[5]
    assert bahr.staffel_id() == "bahr"
    assert [bahr.benefit_pct(g) for g in range(1, 6)] == [0.1, 0.2, 0.3, 0.4, 1.0]
    assert [bahr.waiver_flag(g) for g in range(1, 6)] == [True] * 5
    assert [de_pflege_anchor.waiver_flag(g) for g in range(1, 6)] == [
        False, True, True, True, True]
    assert bahr.proj_len() == 720 < de_pflege_anchor.proj_len()
    assert bahr.result_cf()["claim_expenses"].sum() > (
        de_pflege_anchor.result_cf()["claim_expenses"].sum())
    assert bahr.result_cf()["claim_expenses"].sum() == pytest.approx(57.74, abs=CENT)
    # On bahr the waived population is the whole care ledger; on delib_std it is not.
    for t in (120, 360):
        assert bahr.pols_pg(t, 1) > 0.0
        assert bahr.pols_waived(t) == pytest.approx(
            sum(bahr.pols_pg(t, g) for g in range(1, 6)), rel=1e-12)


# Pitfall 1 -- an average benefit percentage on an average survival curve
def test_pitfall_01_the_annuity_is_a_grade_by_grade_sum(de_pflege_anchor):
    """Grade and mortality are correlated: PG5 pays most and is lived in shortest.

    ``claims(t, "ANNUITY")`` is ``R x sum_g pi_g esc_pg(t, g)``.  Replacing it by
    ``pi_bar x R x pols_care(t)`` with the **entry-mix** mean 0.3815 understates the
    annuity total by 30 % -- 9 248,24 EUR against 13 200,11 EUR -- and the trap is that the
    substitution is *exact* at ``t = 1``, opening only as deterioration moves the stock to
    a stock-weighted mean of 0.544519, which reproduces the total by construction.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    for t in (1, 120, 360, 480):
        rebuilt = p.rente_mth() * sum(
            p.benefit_pct(g) * p.esc_pg(t, g) for g in range(1, 6))
        assert p.claims(t, "ANNUITY") == pytest.approx(rebuilt, rel=1e-12)
    entry_mean = sum(p.benefit_pct(g) * p.inc_share(g) for g in range(1, 6))
    assert entry_mean == pytest.approx(ENTRY_MIX_MEAN_PCT, abs=5e-7)
    # Exact at t = 1, because the stock there is the entry mix.
    assert entry_mean * p.rente_mth() * p.pols_care(1) == pytest.approx(
        p.claims(1, "ANNUITY"), rel=1e-12)
    exposure = sum(p.pols_care(t) for t in range(n))
    assert exposure == pytest.approx(TOTALS["pols_care"], abs=SIX_DP)
    naive = entry_mean * p.rente_mth() * exposure
    assert naive == pytest.approx(NAIVE_ANNUITY_TOTAL, abs=CENT)
    actual = p.result_cf()["claims_annuity"].sum()
    assert naive / actual == pytest.approx(0.70, abs=0.005)
    stock_mean = sum(
        p.benefit_pct(g) * sum(p.pols_pg(t, g) for t in range(n))
        for g in range(1, 6)) / exposure
    assert stock_mean == pytest.approx(STOCK_WEIGHTED_MEAN_PCT, abs=5e-7)
    assert stock_mean * p.rente_mth() * exposure == pytest.approx(actual, rel=1e-9)


# Pitfall 2 -- pricing the annuity in payment on an annuity table
def test_pitfall_02_in_care_mortality_is_a_multiple_of_the_force(de_pflege_anchor):
    """The multiple is on the **force** and is exactly ``mort_mult(g)`` at every age.

    On *rates* the same multiple compresses towards 1 as the rate saturates: at grade 5 it
    falls from 8,97 at age 45 to 6,85 at 85, 4,31 at 95 and 1,00 at the limiting age.  That
    compression is the scale, not the basis.  Pricing this benefit on DAV 2004 R -- built
    to be prudent about people living *longer* -- would be prudent the wrong way round.
    """
    p = de_pflege_anchor
    for t in (0, 120, 360, 480, 600):
        assert p.mort_force(t) > 0.0
        previous = 0.0
        for g in range(1, 6):
            assert p.mort_force_care(t, g) / p.mort_force(t) == pytest.approx(
                MORT_MULT[g], rel=1e-12)
            assert p.mort_rate_care(t, g) == pytest.approx(
                1.0 - math.exp(-p.mort_force_care(t, g)), rel=1e-9)
            assert p.mort_rate_care(t, g) >= p.mort_rate(t)
            assert p.mort_rate_care(t, g) > previous
            previous = p.mort_rate_care(t, g)
    for age, ratio in CARE_RATE_RATIO_PG5.items():
        t = (age - 45) * 12
        assert p.age(t) == age
        assert p.mort_rate_care(t, 5) / p.mort_rate(t) == pytest.approx(ratio, abs=0.005)
    # The force ratio, by contrast, is 9.0 at every one of those ages but the limiting one.
    for age in (45, 85, 95):
        t = (age - 45) * 12
        assert p.mort_force_care(t, 5) / p.mort_force(t) == pytest.approx(9.0, rel=1e-12)


# Pitfall 3 -- "in claim" is not one state exited only by death
def test_pitfall_03_the_paying_state_has_three_exits(de_pflege_anchor):
    """Death, deterioration and *Herabstufung* compete out of every *Pflegegrad*.

    Only death is absorbing.  Recovery out of grade 1 is a *Reaktivierung* to the active
    state, where the life pays its *Beitrag* again and is exposed to lapse again; out of
    the higher grades it moves the life **down** the schedule.  Both flows are small and
    both non-zero, which is why the tests assert the flow and never a non-monotone stock.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    assert sum(p.pols_reactiv(t) for t in range(n)) == pytest.approx(
        REACTIVATION_TOTAL, abs=5e-7)
    for t in (120, 360, 480):
        for g in range(1, 6):
            assert p.p_pg_death(t, g) > 0.0
            assert p.p_pg_better(t, g) > 0.0        # every grade can be downgraded
            assert (p.p_pg_worse(t, g) > 0.0) == (g < 5)
    # A downgrade out of grade 1 goes to aktiv, not to grade 0.
    for t in (120, 360):
        assert p.pols_reactiv(t) == pytest.approx(
            p.pols_pg(t, 1) * p.p_pg_better(t, 1), rel=1e-12)


def test_pitfall_03b_suppressing_recovery_raises_the_liability():
    """Zero the recovery rates and the annuity total rises; the flow really is priced.

    The swap is done on the CSV rather than on a formula, which is also the way a user
    substitutes a licensed or company basis.
    """
    import pandas as pd
    care = pd.read_csv(MODEL_DIR.parent / "care_table.csv", index_col="pflegegrad")
    care["rec_rate"] = 0.0
    alt_name = "care_table_no_recovery.csv"
    model = mx.read_model(MODEL_DIR, name="Pflege_DE_S_norec")
    try:
        care.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_annuity"].sum()
            assert base == pytest.approx(TOTALS["claims_annuity"], abs=CENT)
            model.Data.care_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            assert sum(p.pols_reactiv(t) for t in range(p.proj_len())) == 0.0
            raised = p.result_cf()["claims_annuity"].sum()
            assert raised == pytest.approx(NO_RECOVERY_ANNUITY_TOTAL, abs=CENT)
            assert raised > base
            assert p.check_states() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


# Pitfall 4 -- insuring Pflegegrad 1 by accident
def test_pitfall_04_grade_one_pays_nothing_on_the_delib_std_grid(de_pflege_anchor):
    """``pi_1 = 0``, so grade 1 is in force, in care, unpaid -- and **still paying**.

    The annuity is invariant to ``pols_pg(t, 1)``: dropping grade 1 from the sum changes
    nothing.  A grade-1 life is counted in ``pols_prem`` and not in ``pols_waived``, which
    is the whole reason ``waiver_flag`` exists as its own cells rather than being read off
    membership of the care ledger.
    """
    p = de_pflege_anchor
    assert p.staffel_id() == "delib_std"
    assert p.benefit_pct(1) == 0.0
    assert p.waiver_flag(1) is False
    for t in (120, 360, 480):
        assert p.pols_pg(t, 1) > 0.0
        without_grade_one = p.rente_mth() * sum(
            p.benefit_pct(g) * p.esc_pg(t, g) for g in range(2, 6))
        assert p.claims(t, "ANNUITY") == pytest.approx(without_grade_one, rel=1e-12)
        assert p.claim_expenses(t) == pytest.approx(
            1.5 * p.expense_infl_factor(t)
            * sum(p.pols_pg(t, g) for g in range(2, 6)), rel=1e-12)
        # The grade-1 population is inside pols_care but outside pols_waived.
        assert p.pols_waived(t) == pytest.approx(
            sum(p.pols_pg(t, g) for g in range(2, 6)), rel=1e-12)
        assert p.pols_care(t) > p.pols_waived(t)


# Pitfall 5 -- waiving the premium at the wrong grade
def test_pitfall_05_the_waiver_runs_with_the_leistungsstaffel(
        pflegerentenversicherung, de_pflege_anchor):
    """The same life is waived on ``bahr`` and pays on ``delib_std``.

    ``pols_waived`` is ``sum_{g : waiver_flag(g)} pols_pg(t, g)`` restricted to the
    premium term -- driven by whether an annuity is payable, not by whether the life is in
    care.  ``check_waiver()`` closes on both schedules, which is why the membership itself
    has to be asserted beside it.
    """
    std = de_pflege_anchor
    bahr = pflegerentenversicherung.Projection[5]
    assert std.benefit_pct(1) == 0.0 and bahr.benefit_pct(1) == 0.1
    assert std.waiver_flag(1) is False and bahr.waiver_flag(1) is True
    for t in (120, 360):
        assert std.pols_waived(t) == pytest.approx(
            std.pols_care(t) - std.pols_pg(t, 1), rel=1e-12)
        assert bahr.pols_waived(t) == pytest.approx(bahr.pols_care(t), rel=1e-12)
    assert std.check_waiver() is True
    assert bahr.check_waiver() is True
    for t in (0, 120, 360, 600):
        assert std.check_waiver_resid(t) == pytest.approx(0.0, abs=1e-14)
        assert bahr.check_waiver_resid(t) == pytest.approx(0.0, abs=1e-14)


# Pitfall 6 -- the premium revives on a Herabstufung
def test_pitfall_06_the_premium_revives_and_it_is_a_flow(de_pflege_anchor):
    """Assert the *flow* out of the lowest insured grade, never a non-monotone stock.

    Lives leaving grade 2 downward stop being paid and start paying again; that flow is
    0,020835 of a policy.  ``pols_prem(t)`` is therefore at least ``pols_act(t)``, strictly
    wherever a grade-1 population exists.  The **stock** is nevertheless monotone
    decreasing here -- attrition dominates the revival flow by three orders of magnitude --
    so a test asserting non-monotonicity would assert a coincidence, not the mechanic.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    revival = sum(p.pols_pg(t, 2) * p.p_pg_better(t, 2) for t in range(n))
    assert revival == pytest.approx(HERABSTUFUNG_OUT_OF_PG2, abs=5e-7)
    assert revival > 0.0
    assert all(p.pols_prem(t) >= p.pols_act(t) - 1e-15 for t in range(n))
    for t in (1, 120, 360, 600):
        assert p.pols_pg(t, 1) > 0.0
        assert p.pols_prem(t) > p.pols_act(t)
        assert p.pols_prem(t) == pytest.approx(
            p.pols_act(t) + p.pols_pg(t, 1), rel=1e-12)
    assert all(p.pols_prem(t + 1) <= p.pols_prem(t) + 1e-15 for t in range(n - 1))
    assert p.check_waiver() is True


# Pitfall 7 -- adding monthly transition probabilities
def test_pitfall_07_one_survival_is_allocated_not_several_added(de_pflege_anchor):
    """``p_stay + sum p_j = 1`` exactly, by construction, in both state families.

    Every shipped rate is annual and every month is stepped with forces held constant
    over the month, the competing transitions sharing one survival probability in
    proportion to their forces.  That is what makes ``check_states()`` an identity rather
    than an approximation.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    worst_act = 0.0
    worst_pg = 0.0
    for t in range(n):
        total = p.p_act_stay(t) + p.p_act_death(t) + p.p_act_care(t)
        worst_act = max(worst_act, abs(total - 1.0))
        for g in range(1, 6):
            s = (p.p_pg_stay(t, g) + p.p_pg_death(t, g)
                 + p.p_pg_worse(t, g) + p.p_pg_better(t, g))
            worst_pg = max(worst_pg, abs(s - 1.0))
    assert worst_act < 1e-12
    assert worst_pg < 1e-12
    # And the allocation really is proportional to the forces, not a set of added rates.
    for t in (0, 240, 480):
        total_force = p.mort_force(t) + p.inc_force(t)
        assert p.p_act_death(t) / p.p_act_care(t) == pytest.approx(
            p.mort_force(t) / p.inc_force(t), rel=1e-12)
        assert p.p_act_stay(t) == pytest.approx(
            math.exp(-total_force / 12.0), rel=1e-9)


# Pitfall 8 -- dividing an annual rate by twelve
def test_pitfall_08_the_monthly_rates_are_compounded_not_divided(de_pflege_anchor):
    """``q_mth = 1 - (1 - q)**(1/12)``, and ``q/12`` is strictly **below** it.

    The house convention is that ``*_rate`` is annual and ``*_rate_mth`` monthly, the
    monthly one smaller.  The pitfall's direction is the opposite of the intuition:
    dividing by twelve **understates** the monthly decrement, so twelve monthly rates
    *added* overshoot the annual rate while twelve *compounded* reproduce it exactly.
    """
    p = de_pflege_anchor
    for t in (0, 12, 240, 480, 600):
        assert p.mort_rate_mth(t) == pytest.approx(
            1.0 - pow(1.0 - p.mort_rate(t), 1.0 / 12.0), rel=1e-12)
        assert p.lapse_rate_mth(t) == pytest.approx(
            1.0 - pow(1.0 - p.lapse_rate(t), 1.0 / 12.0), rel=1e-12)
        if p.mort_rate(t) > 0.0:
            assert p.mort_rate_mth(t) < p.mort_rate(t)          # the house convention
            assert p.mort_rate(t) / 12.0 < p.mort_rate_mth(t)   # the pitfall's direction
            assert 1.0 - pow(1.0 - p.mort_rate_mth(t), 12) == pytest.approx(
                p.mort_rate(t), rel=1e-12)
        if p.lapse_rate(t) > 0.0:
            assert p.lapse_rate_mth(t) < p.lapse_rate(t)
            assert p.lapse_rate(t) / 12.0 < p.lapse_rate_mth(t)
            assert 1.0 - pow(1.0 - p.lapse_rate_mth(t), 12) == pytest.approx(
                p.lapse_rate(t), rel=1e-12)
    # The projection works in forces; the two agree by construction.
    for t in (0, 240, 480):
        assert p.mort_rate_mth(t) == pytest.approx(
            1.0 - math.exp(-p.mort_force(t) / 12.0), rel=1e-9)


# Pitfall 9 -- the Karenzzeit is a clock per onset, not a gate on the aggregate
def test_pitfall_09_the_karenzzeit_is_a_deferral_clock_per_onset(
        pflegerentenversicherung, de_pflege_anchor):
    """On model point 7, graduations fall strictly short of entries: 0,2282 against 0,2537.

    The shortfall is the deaths and recoveries recorded **inside** the deferral, and it is
    larger than six months of a four-year spell suggests because mortality is highest
    immediately after onset.  With ``karenz_months = 0`` the ledger is empty and
    ``pols_grad`` degenerates to ``pols_entry``, which is the base run.
    """
    p = pflegerentenversicherung.Projection[7]
    n = p.proj_len()
    assert p.karenz_months() == 6 and p.wartezeit_months() == 36
    entries = sum(p.pols_entry(t, g) for t in range(n) for g in range(1, 6))
    grads = sum(p.pols_grad(t, g) for t in range(n) for g in range(1, 6))
    assert entries == pytest.approx(KARENZ_ENTRIES, abs=5e-7)
    assert grads == pytest.approx(KARENZ_GRADUATIONS, abs=5e-7)
    assert grads < entries
    assert grads / entries == pytest.approx(0.899, abs=0.001)
    # A life inside its Karenzzeit is in care, in force, unpaid -- and pays its Beitrag.
    for t in (400, 500):
        deferred = sum(p.pols_karenz(t, g, z)
                       for g in range(1, 6) for z in range(1, 7))
        assert deferred > 0.0
        assert p.pols_care(t) == pytest.approx(
            deferred + sum(p.pols_pg(t, g) for g in range(1, 6)), rel=1e-12)
        assert p.pols_waived(t) == pytest.approx(
            sum(p.pols_pg(t, g) for g in range(2, 6)), rel=1e-12)
    assert p.check_states() is True and p.check_waiver() is True
    # The base run is the degenerate case, and the two cells then coincide exactly.
    base = de_pflege_anchor
    assert base.karenz_months() == 0
    for t in (0, 120, 360):
        for g in range(1, 6):
            assert base.pols_grad(t, g) == pytest.approx(
                base.pols_entry(t, g), rel=1e-15)
            assert base.pols_karenz(t, g, 1) == 0.0
    # The Wartezeit is the other device: it runs from inception and denies cover, and it
    # gates the *force* so that inc_rate stays the tariff-comparable table rate at every
    # age.  Conflating the two is the routine consumer-material error.
    assert all(p.inc_force(t) == 0.0 for t in range(0, 36))
    assert all(p.inc_rate(t) > 0.0 for t in range(0, 36))
    assert all(p.p_act_care(t) == 0.0 for t in range(0, 36))
    assert p.inc_force(36) > 0.0
    assert sum(p.pols_entry(t, g) for t in range(0, 36) for g in range(1, 6)) == 0.0


# Pitfall 10 -- escalating the annuity at general-population duration
def test_pitfall_10_the_leistungsdynamik_costs_more_than_a_short_spell_suggests(
        pflegerentenversicherung, de_pflege_anchor):
    """+14,4 % on the annuity total and +12,2 % on the premium, not "less than 5 %".

    An earlier draft of the notes predicted the smaller figure from a four-year spell and
    the model contradicts it: the escalation compounds over elapsed time in **care**,
    *Pflegegrad* 1 months included where nothing is paid, and deterioration puts the
    largest benefit percentages at the end of a spell.  ``ln(1.144) / ln(1.02) = 6,8``
    years of payment-weighted duration against a mean insured spell of 5,5 years.
    """
    dyn = pflegerentenversicherung.Projection[8]
    base = de_pflege_anchor
    assert dyn.leistungsdynamik() == 0.02 and base.leistungsdynamik() == 0.0
    assert dyn.age_at_entry() == base.age_at_entry() and dyn.sex() == base.sex()
    dyn_annuity = dyn.result_cf()["claims_annuity"].sum()
    assert dyn_annuity == pytest.approx(VARIANTS[8]["claims_annuity"], abs=CENT)
    assert dyn_annuity / TOTALS["claims_annuity"] - 1.0 == pytest.approx(
        DYNAMIK_ANNUITY_UPLIFT, abs=0.0005)
    assert dyn.premium_mth_pp() / base.premium_mth_pp() - 1.0 == pytest.approx(
        DYNAMIK_PREMIUM_UPLIFT, abs=0.0005)
    # The head count is identical -- only the value ledger moves.
    for t in (120, 480):
        assert dyn.pols_care(t) == pytest.approx(base.pols_care(t), rel=1e-12)
        for g in range(1, 6):
            assert dyn.pols_pg(t, g) == pytest.approx(base.pols_pg(t, g), rel=1e-12)
    assert dyn.esc_pg(480, 3) / dyn.pols_pg(480, 3) == pytest.approx(1.1035, abs=5e-5)
    assert dyn.check_esc_ledger() is True
    # On the anchor the two ledgers agree at every t and g.  The two recursions add
    # their terms in a different order, so the agreement is to floating-point rounding
    # rather than bit for bit; the largest difference anywhere in the frame is 1e-17.
    n = base.proj_len()
    worst = max(abs(base.esc_pg(t, g) - base.pols_pg(t, g))
                for t in range(n) for g in range(1, 6))
    assert worst < 1e-15
    assert base.check_esc_ledger() is True


# Pitfall 11 -- netting the annuity off a Beitragsrueckgewaehr in aggregate
def test_pitfall_11_the_beitragsrueckgewaehr_is_paid_gross(pflegerentenversicherung,
                                                           de_pflege_anchor):
    """``claims_death = cum_prem_max_pp(t) x pols_death(t)`` on point 9, and 0 on point 1.

    The market's commoner form nets the annuity already paid off the return of premiums,
    but that netting is floored at zero **per life** while these ledgers are aggregates, so
    netting in aggregate would let one life subsidise another.  The model pays the
    **gross** form and so overstates the benefit, which is stated rather than hidden.  The
    option's price is the other half of the point: 622,92 EUR against the anchor's 64,20.
    """
    brg = pflegerentenversicherung.Projection[9]
    assert brg.beitragsrueckgewaehr() is True
    assert brg.prem_end_age() == 65
    assert brg.premium_mth_pp() == pytest.approx(622.920626, abs=5e-6)
    assert brg.premium_mth_pp() / de_pflege_anchor.premium_mth_pp() == pytest.approx(
        9.7, abs=0.05)
    for t in (0, 120, 300, 600):
        assert brg.brg_pp(t) == pytest.approx(brg.cum_prem_max_pp(t), rel=1e-15)
        assert brg.claims(t, "DEATH") == pytest.approx(
            brg.cum_prem_max_pp(t) * brg.pols_death(t), rel=1e-12)
    # The Beitragssumme is capped at the premium term, so cum_prem stops at age 65.
    assert brg.cum_prem_max_pp(300) == pytest.approx(brg.cum_prem_max_pp(600), rel=1e-15)
    assert brg.result_cf()["claims_death"].sum() > 80000.0
    assert brg.check_net_cf() is True and brg.check_prem_equiv() is True
    # Structurally zero on the base run, and published rather than dropped.
    base = de_pflege_anchor
    assert base.beitragsrueckgewaehr() is False
    assert all(base.brg_pp(t) == 0.0 for t in (0, 120, 600))
    assert base.result_cf()["claims_death"].sum() == 0.0


# Pitfall 12 -- paying a surrender value out of the paying state
def test_pitfall_12_nothing_in_care_lapses(pflegerentenversicherung, de_pflege_anchor):
    """Lapse acts on the active state only, and stops with the premium term.

    A claimant with a waived premium has no premium to default on and a live annuity to
    forfeit.  Model point 12 opens with its whole cohort in *Pflegegrad* 3 and no active
    lives, so both the surrender decrement and the surrender benefit are exactly zero
    there; model point 4 is the other boundary, paid up at 65 with ``lapse_rate`` zero.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    assert all(p.pols_lapse(t) <= p.pols_act(t) for t in range(n))
    in_claim = pflegerentenversicherung.Projection[12]
    assert in_claim.status_init() == "pg3"
    assert in_claim.duration_mth_init() == 336
    assert in_claim.pols_act(336) == 0.0
    assert in_claim.pols_pg(336, 3) == 1.0
    assert in_claim.pols_lapse(336) == 0.0
    assert in_claim.claims(336, "LAPSE") == 0.0
    assert in_claim.claims(336, "ANNUITY") == pytest.approx(500.0, abs=CENT)
    assert in_claim.premiums(336) == 0.0
    assert in_claim.pols_waived(336) == 1.0
    paid_up = pflegerentenversicherung.Projection[4]
    assert paid_up.prem_end_age() == 65
    first_paid_up = 12 * (65 - paid_up.age_at_entry())
    assert paid_up.age(first_paid_up) == 65
    assert paid_up.lapse_rate(first_paid_up - 1) > 0.0
    assert paid_up.lapse_rate(first_paid_up) == 0.0
    assert paid_up.pols_lapse(first_paid_up) == 0.0
    assert paid_up.claims(first_paid_up, "LAPSE") == 0.0
    assert paid_up.premiums(first_paid_up) == 0.0
    assert paid_up.pols_in_term(first_paid_up) == 0.0
    assert paid_up.pols_if(first_paid_up) > 0.0      # the cover runs on
    # And what is paid where a surrender does happen: the guaranteed ratio on premiums
    # paid, less any contractual Stornoabzug.  Model point 10 carries 5 %; the base run
    # carries none, because a deduction is admissible only if agreed, appropriate and
    # quantified in the contract and no German Pflegerenten level was established.  The
    # first two policy years are zero, the Zillmerung allowance being unamortised.
    storno = pflegerentenversicherung.Projection[10]
    surrender = pflegerentenversicherung.Data.surrender_table()
    assert storno.stornoabzug_rate() == 0.05 and p.stornoabzug_rate() == 0.0
    assert storno.policy_year(60) == 6
    assert storno.rkw_pp(60) == pytest.approx(
        float(surrender.at[6, "rkw_prem_ratio"])
        * storno.cum_prem_max_pp(60) * 0.95, rel=1e-12)
    assert storno.rkw_pp(60) == pytest.approx(1060.485, abs=CENT)
    assert float(surrender.at[1, "rkw_prem_ratio"]) == 0.0
    assert float(surrender.at[2, "rkw_prem_ratio"]) == 0.0
    assert float(surrender.at[3, "rkw_prem_ratio"]) > 0.0
    assert storno.rkw_pp(0) == 0.0


# Pitfall 13 -- charging the Zillmerung on the wrong base
def test_pitfall_13_the_zillmerung_is_charged_on_the_beitragssumme(
        pflegerentenversicherung, de_pflege_anchor):
    """25 permille of the *Beitragssumme*, at ``t = 0`` only -- not of the annual premium.

    ``beitragssumme_cap_age = 85`` is the convention that gives a lifelong-premium contract
    a finite *Beitragssumme*; what is cited is the § 4 DeckRV ceiling the per-mille sits
    exactly at.  Charging it on an annual premium instead understates it by a factor of the
    paying term -- forty-fold here -- and an **in-force point never incurs the charge**.
    """
    p = de_pflege_anchor
    expected = 0.025 * p.premium_mth_pp() * 12.0 * (min(110, 85) - 45)
    assert p.acq_expense_pp() == pytest.approx(expected, rel=1e-12)
    assert p.acq_expense_pp() == pytest.approx(ACQ_EXPENSE_PP, abs=CENT)
    on_annual_premium = 0.025 * p.premium_mth_pp() * 12.0
    assert p.acq_expense_pp() / on_annual_premium == pytest.approx(40.0, rel=1e-12)
    # Charged at t = 0 and nowhere else.
    assert p.expenses(0) - p.acq_expense_pp() < 5.0
    for t in (1, 12, 360):
        admin = (2.0 * p.expense_infl_factor(t) * p.pols_if(t)
                 + 0.03 * p.premiums(t))
        assert p.expenses(t) == pytest.approx(admin, rel=1e-12)
    in_force = pflegerentenversicherung.Projection[11]
    assert in_force.duration_mth_init() == 240
    assert in_force.result_cf().index[0] == 240
    assert in_force.acq_expense_pp() > 0.0          # the charge exists
    admin_only = (2.0 * in_force.expense_infl_factor(240) * in_force.pols_if(240)
                  + 0.03 * in_force.premiums(240))
    assert in_force.expenses(240) == pytest.approx(admin_only, rel=1e-12)
    assert in_force.expenses(240) < 10.0             # ... and is not charged here


# Pitfall 14 -- striking the equivalence premium on the projection basis
def test_pitfall_14_the_premium_is_struck_on_the_first_order_basis(de_pflege_anchor):
    """The tariff ledgers carry margins, blend the sexes, and carry **no lapse at all**.

    ``tar_inc_rate`` exceeds the **unisex-blended** best estimate by exactly ``inc_margin``;
    against the anchor's own *female* incidence the ratio is 1.128 at 45, **not** 1.25,
    because the blend and the margin are two operations and only the second is prudence.
    Prudence forks by risk: fewer deaths before claim, longer annuities, more incidence,
    faster deterioration, fewer recoveries.
    """
    p = de_pflege_anchor
    assert p.check_prem_equiv() is True
    assert p.check_prem_equiv_resid(0) != 0.0            # individual months are large
    total = sum(p.check_prem_equiv_resid(t) for t in range(p.proj_len()))
    assert total == pytest.approx(0.0, abs=1e-9)
    # Margins, and their directions.  For an active life prudence means *lower*
    # mortality -- a life that survives is a life that can claim -- so the margin is
    # 0.90 and not 1.10; for a life in care it means lower mortality too, because that
    # lengthens the annuity.  Deterioration is loaded up and recovery down.
    for t in (0, 240, 480):
        assert p.tar_det_rate(t, 2) == pytest.approx(1.15 * p.det_rate(2), rel=1e-12)
        assert p.tar_det_rate(t, 2) > p.det_rate(2)
        assert p.tar_rec_rate(t, 2) == pytest.approx(0.80 * p.rec_rate(t, 2), rel=1e-12)
        assert p.tar_rec_rate(t, 2) < p.rec_rate(t, 2)


def test_pitfall_14b_the_blend_and_the_margin_are_two_operations(
        pflegerentenversicherung, de_pflege_anchor):
    """``tar_inc_rate = 1.25 x [0.5 i_M(x) + 0.5 i_F(x)]``, capped at ``inc_cap``."""
    p = de_pflege_anchor
    inc = pflegerentenversicherung.Data.incidence_table()
    for t, expected_ratio_to_own in ((0, 1.128), (480, 1.089)):
        x = p.age(t)
        blended = 0.5 * float(inc.at[("M", x), "inc_rate"]) + 0.5 * float(
            inc.at[("F", x), "inc_rate"])
        assert p.tar_inc_rate(t) == pytest.approx(1.25 * blended, rel=1e-12)
        assert p.tar_inc_rate(t) / p.inc_rate(t) == pytest.approx(
            expected_ratio_to_own, abs=0.001)
        assert p.tar_inc_rate(t) / p.inc_rate(t) != pytest.approx(1.25, abs=0.05)


def test_pitfall_14c_the_premium_is_invariant_to_every_lapse_rate():
    """Halve the whole lapse table: the premium does not move by one bit.

    German first-order practice carries no lapse, and that is also what keeps the model
    acyclic -- a pricing quantity must not depend on a behavioural assumption that depends
    on the path that depends on the premium.  The projection, of course, moves a great
    deal: fewer surrenders mean less *Rückkaufswert* paid and far more annuity.
    """
    import pandas as pd
    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    lapse["lapse_rate"] = lapse["lapse_rate"] * 0.5
    alt_name = "lapse_table_half.csv"
    model = mx.read_model(MODEL_DIR, name="Pflege_DE_S_halflapse")
    try:
        lapse.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1]
            base_premium = base.premium_mth_pp()
            base_lapse_claims = base.result_cf()["claims_lapse"].sum()
            assert base_premium == pytest.approx(PREMIUM_MTH_PP, abs=5e-6)
            model.Data.lapse_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            assert p.lapse_rate(0) == 0.03
            assert p.premium_mth_pp() == base_premium      # bit for bit
            assert p.result_cf()["claims_lapse"].sum() < base_lapse_claims
            assert p.result_cf()["claims_annuity"].sum() > TOTALS["claims_annuity"]
            assert p.check_prem_equiv() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


# Pitfall 15 -- pricing on the model point's own sex
def test_pitfall_15_sex_does_not_price(pflegerentenversicherung, de_pflege_anchor):
    """Equal premium, unequal projection -- the unisex rule, in two model points.

    Sex may not enter the premium of a contract concluded from 21 December 2012, so the
    pricing engine reads ``unisex_mix_male`` and never ``sex()``, while ``mort_rate`` and
    ``inc_rate`` read nothing else.  The female cell's projected annuity is the larger,
    which is the direction the cross-subsidy runs.
    """
    female = de_pflege_anchor
    male = pflegerentenversicherung.Projection[2]
    assert female.sex() == "F" and male.sex() == "M"
    assert female.age_at_entry() == male.age_at_entry() == 45
    assert female.rente_mth() == male.rente_mth()
    assert female.staffel_id() == male.staffel_id()
    assert female.premium_mth_pp() == male.premium_mth_pp()          # bit for bit
    assert female.epv_benefits() == male.epv_benefits()
    assert female.epv_prem_units() == male.epv_prem_units()
    assert female.tar_inc_rate(0) == male.tar_inc_rate(0)
    assert female.inc_rate(0) != male.inc_rate(0)
    assert female.result_cf()["claims_annuity"].sum() > (
        male.result_cf()["claims_annuity"].sum())


# Pitfall 16 -- collecting a premium in a month that is not a due date
def test_pitfall_16_instalments_fall_on_due_months_only(pflegerentenversicherung,
                                                        de_pflege_anchor):
    """A quarterly contract pays three months' worth three times a year, not a twelfth.

    ``premium_due`` keys off **issue**, not off the frame's first row, and
    ``premium_pp(t)`` is ``P x m`` on a due month and zero otherwise.  The
    *Einmalbeitrag* is the degenerate case: ``m = 0`` is a sentinel meaning one payment at
    ``t = 0`` and nothing thereafter, and ``U`` is then exactly 1.
    """
    monthly = de_pflege_anchor
    assert monthly.prem_mode_months() == 1
    assert all(monthly.premium_due(t) for t in range(0, 24))
    for point_id, m in ((3, 3), (4, 6), (5, 12)):
        p = pflegerentenversicherung.Projection[point_id]
        assert p.prem_mode_months() == m
        due = [t for t in range(0, 60) if p.premium_due(t)]
        assert due == list(range(0, 60, m))
        for t in range(0, 60):
            if t % m == 0:
                assert p.premium_pp(t) == pytest.approx(
                    p.premium_mth_pp() * m, rel=1e-12)
                assert p.premiums(t) > 0.0
            else:
                assert p.premium_pp(t) == 0.0
                assert p.premiums(t) == 0.0
    single = pflegerentenversicherung.Projection[6]
    assert single.prem_mode() == "single"
    assert single.prem_mode_months() == 0
    assert [t for t in range(0, 60) if single.premium_due(t)] == [0]


# Pitfall 17 -- using the Pflegegrad stock distribution as the entry mix
def test_pitfall_17_entrants_are_not_the_stock(de_pflege_anchor):
    """``entry_share`` sums to one and is **lower** than the stock the model produces.

    The German stock runs about 9 / 44 / 27 / 14 / 6 % across the five grades; entrants do
    not, because deterioration moves people up over a spell.  The arithmetic statement of
    that is the model's own stock share at grades 4 and 5 exceeding the entry share --
    21,0 % against 13 %, and 17,6 % against 5 %.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    assert sum(p.inc_share(g) for g in range(1, 6)) == pytest.approx(1.0, abs=1e-12)
    for g, share in ENTRY_SHARE.items():
        assert p.inc_share(g) == pytest.approx(share, rel=1e-12)
    exposure = sum(p.pols_care(t) for t in range(n))
    for g in range(1, 6):
        share = sum(p.pols_pg(t, g) for t in range(n)) / exposure
        assert share == pytest.approx(STOCK_SHARE[g], abs=5e-7)
    assert STOCK_SHARE[4] > ENTRY_SHARE[4]
    assert STOCK_SHARE[5] > ENTRY_SHARE[5]
    assert STOCK_SHARE[1] < ENTRY_SHARE[1]
    assert STOCK_SHARE[2] < ENTRY_SHARE[2]


# The published identities
def test_every_published_check_closes_on_the_anchor_cell(de_pflege_anchor):
    """Six no-argument bools over all ``t``, each with a per-``t`` signed residual."""
    p = de_pflege_anchor
    assert p.check_net_cf() is True
    assert p.check_pols_roll_fwd() is True
    assert p.check_states() is True
    assert p.check_waiver() is True
    assert p.check_esc_ledger() is True
    assert p.check_prem_equiv() is True
    for t in (0, 1, 60, 240, 480, 700, 779):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_states_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_waiver_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_esc_ledger_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_check_net_cf_is_delib_ruling_one(de_pflege_anchor):
    """``net_cf = premiums - annuity - lapse - death - expenses - claim_expenses``.

    Every term is a **column of** ``result_cf()``, and the residual re-derives the headline
    number from the three ``claims`` **kinds** separately rather than from their subtotal,
    so a benefit dropped from ``claims(t)``, or a column added without being subtracted,
    fails here instead of silently changing the answer.  The largest residual is 1e-14.
    """
    p = de_pflege_anchor
    n = p.proj_len()
    worst = max(abs(p.check_net_cf_resid(t)) for t in range(n))
    assert worst < 1e-12
    df = p.result_cf()
    rebuilt = (df["premiums"] - df["claims_annuity"] - df["claims_lapse"]
               - df["claims_death"] - df["expenses"] - df["claim_expenses"])
    assert (rebuilt - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-12)
    for t in (0, 240, 480):
        assert p.claims(t) == pytest.approx(
            p.claims(t, "ANNUITY") + p.claims(t, "LAPSE") + p.claims(t, "DEATH"),
            rel=1e-15)


def test_check_states_is_not_the_roll_forward_made_twice(de_pflege_anchor):
    """One telescopes the ledgers' recursions; the other sums them independently.

    ``check_pols_roll_fwd`` says lives leave the in-force population only by death or
    surrender.  ``check_states`` is assembled by direct summation over the three live
    ledgers and the two absorbing counts, with no reference to the recursions -- which
    catches a wrong seeding, a life in two grades at once, or a double graduation.
    """
    p = de_pflege_anchor
    for t in (0, 120, 360, 600):
        parts = (p.pols_act(t) + sum(p.pols_pg(t, g) for g in range(1, 6))
                 + p.pols_dead_cum(t) + p.pols_lapse_cum(t))
        assert parts == pytest.approx(p.pols_if_init(), abs=1e-12)
        assert p.pols_if(t + 1) == pytest.approx(
            p.pols_if(t) - p.pols_death(t) - p.pols_lapse(t), abs=1e-12)
    # The components are not constant -- the identity has work to do.
    assert p.pols_act(600) < p.pols_act(0)
    assert p.pols_dead_cum(600) > p.pols_dead_cum(120) > 0.0
    assert p.pols_lapse_cum(600) > p.pols_lapse_cum(120) > 0.0
    assert sum(p.pols_pg(360, g) for g in range(1, 6)) > 0.0


def test_check_prem_equiv_is_true_by_construction_where_the_premium_is_supplied(
        pflegerentenversicherung):
    """Model point 10 carries its own *Beitrag*, so no equivalence was struck to check.

    An equivalence that was never struck cannot be checked, and the model says so with a
    zero residual rather than by pretending to verify a number it did not produce.
    """
    p = pflegerentenversicherung.Projection[10]
    assert p.premium_mth() == 75.0
    assert p.premium_mth_pp() == 75.0
    assert p.check_prem_equiv() is True
    assert all(p.check_prem_equiv_resid(t) == 0.0 for t in (0, 12, 240))


def test_the_risikozuschlag_loads_the_premium_and_never_the_benefit(
        pflegerentenversicherung):
    """Model point 13 prices at exactly 1,50 times its own unrated premium.

    A *Risikozuschlag* buys the same annuity at a higher price, so it multiplies the gross
    premium after the equivalence and ``claims`` is invariant to it.
    """
    p = pflegerentenversicherung.Projection[13]
    assert p.rating_factor() == 1.5
    assert p.premium_mth_pp() == pytest.approx(283.130286, abs=5e-6)
    assert p.premium_mth_pp() / p.rating_factor() == pytest.approx(
        188.753524, abs=5e-6)
    unrated = (p.epv_benefits() + p.epv_admin() + p.epv_claim_expense()) / (
        p.epv_prem_units() * (1.0 - ADMIN_PREM_PCT) - 0.025 * 12.0 * (85 - 65))
    assert unrated == pytest.approx(188.753524, abs=5e-6)
    assert p.premium_mth_pp() == pytest.approx(1.5 * unrated, rel=1e-12)
    assert p.check_prem_equiv() is True


# Structure, documentation and inputs
def test_result_cf_shape_and_both_signs_of_the_net_flow(de_pflege_anchor):
    """Twelve columns, ``pols_if`` first, and the two orientations of the same stream."""
    df = de_pflege_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "pols_act", "pols_care", "pols_prem",
        "premiums", "claims_annuity", "claims_lapse", "claims_death",
        "expenses", "claim_expenses", "net_cf", "liability_cf",
    ]
    # A cash flow statement must not publish its own subtotal beside its parts.
    assert "claims" not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    # The three-way split of pols_if a reader follows the projection with.
    assert (df["pols_act"] + df["pols_care"] - df["pols_if"]).abs().max() == (
        pytest.approx(0.0, abs=1e-12))
    assert (df["pols_prem"] <= df["pols_if"] + 1e-12).all()
    assert (df["pols_if"] >= 0.0).all()
    assert df["pols_if"].iloc[0] == de_pflege_anchor.pols_if_init()
    # pols_if is a start-of-period count; end-of-period state lives in pols_if_at.
    for t in (0, 120, 480):
        assert de_pflege_anchor.pols_if_at(t, "BEG") == de_pflege_anchor.pols_if(t)
        assert de_pflege_anchor.pols_if_at(t, "END") == de_pflege_anchor.pols_if(t + 1)


def test_invalid_enum_values_raise(de_pflege_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_pflege_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        de_pflege_anchor.pols_if_at(1, "AFTER_LAPSE")


def test_the_annual_and_monthly_rate_pairs_follow_the_house_convention(de_pflege_anchor):
    """``*_rate`` is annual, ``*_rate_mth`` is monthly, and both are published."""
    names = set(de_pflege_anchor.cells)
    assert {"mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth"} <= names
    p = de_pflege_anchor
    for t in (0, 240, 480):
        assert 0.0 < p.mort_rate_mth(t) < p.mort_rate(t)
        if p.lapse_rate(t) > 0.0:
            assert 0.0 < p.lapse_rate_mth(t) < p.lapse_rate(t)


def test_docstrings_describe_the_current_structure(pflegerentenversicherung):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = pflegerentenversicherung.doc
    assert "Pflegerente" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "Data" in doc and "Projection" in doc
    assert "DAV 2008 P" in doc and "not redistributed here" in doc
    assert "Beitragsbefreiung" in doc
    proj = pflegerentenversicherung.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "pols_pg", "esc_pg", "pols_karenz",
                  "mort_force_care", "waiver_flag", "check_prem_equiv", "pols_if_at"):
        assert cells in proj, cells
    data = pflegerentenversicherung.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "care_table", "incidence_table",
                  "mort_table"):
        assert cells in data, cells
    # The Data docstring states the anchors a replacement table must preserve.
    assert "q(65)" in data and "q(85)" in data


def test_the_multi_state_vocabulary_is_present(pflegerentenversicherung):
    """The shared names, plus the ones this chassis adds over a single-decrement model."""
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_act", "pols_care", "pols_prem", "pols_waived", "pols_in_term",
        "pols_pg", "esc_pg", "pols_karenz", "pols_entry", "pols_grad", "pols_reactiv",
        "pols_death", "pols_lapse", "pols_dead_cum", "pols_lapse_cum",
        "mort_rate", "mort_rate_mth", "mort_force", "mort_rate_care", "mort_force_care",
        "inc_rate", "inc_force", "inc_share", "det_rate", "rec_rate",
        "lapse_rate", "lapse_rate_mth", "benefit_pct", "waiver_flag",
        "premium_mth_pp", "prem_net_level_pp", "premium_pp", "premiums",
        "claims", "expenses", "claim_expenses", "net_cf", "liability_cf",
        "result_cf", "result_states",
        "check_net_cf", "check_net_cf_resid", "check_pols_roll_fwd", "check_states",
        "check_waiver", "check_esc_ledger", "check_prem_equiv",
    }
    names = set(pflegerentenversicherung.Projection.cells) | set(
        pflegerentenversicherung.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    # Retired names must not come back.
    retired = {"lapse_rate_ann", "prem_net_pp", "check_pols_if", "pols_init", "omega",
               "mort_rate_table", "check_cf_ledger"}
    assert not (retired & names), f"retired: {sorted(retired & names)}"


def test_result_states_publishes_the_ledgers_behind_the_cash_flows(de_pflege_anchor):
    """The frame a reader needs to follow the multi-state machinery, indexed by ``t``."""
    df = de_pflege_anchor.result_states()
    assert df.index.name == "t"
    assert list(df.index) == list(range(0, 780))
    assert list(df.columns) == [
        "pols_pg1", "pols_pg2", "pols_pg3", "pols_pg4", "pols_pg5",
        "pols_karenz", "pols_entry", "pols_grad", "pols_reactiv",
        "pols_death", "pols_lapse",
        "mort_rate", "mort_rate_care_pg5", "inc_rate", "lapse_rate", "premium_pp",
    ]
    assert df["pols_karenz"].sum() == 0.0            # no Karenzzeit on the anchor
    assert (df["pols_entry"] - df["pols_grad"]).abs().max() == pytest.approx(
        0.0, abs=1e-15)
    assert (df["mort_rate_care_pg5"] >= df["mort_rate"]).all()


def test_the_shipped_tables_mark_their_own_provenance():
    """Nine CSVs beside run.py, and each says what it is -- especially what it is not.

    Every file but ``model_point_table.csv`` carries a ``provenance`` column, one tag per
    row -- delib's second ruling, the model point table being the only exemption because a
    model point is a configuration rather than an assumption.  The decrement tables are
    **[std]** proxies, and the anchors a substitute must preserve are asserted here.
    """
    import pandas as pd
    assert INPUT_CSVS == {p.name for p in MODEL_DIR.parent.iterdir()
                          if p.suffix == ".csv"}
    assert not any(p.suffix == ".csv" for p in MODEL_DIR.rglob("*"))
    assert model_files(MODEL_DIR) == {"__init__.py", "_system.json"}
    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col=["sex", "age"])
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert all("not redistributed" in mort.at[(s, a), "provenance"]
               for s in ("M", "F") for a in (18, 45, 65, 85, 108))
    assert all("limiting-age convention" in mort.at[(s, 109), "provenance"]
               for s in ("M", "F"))
    assert float(mort.at[("M", 65), "mort_rate"]) == pytest.approx(0.0135, rel=2e-3)
    assert float(mort.at[("M", 85), "mort_rate"]) == pytest.approx(0.1050, rel=2e-3)
    assert float(mort.at[("F", 65), "mort_rate"]) == pytest.approx(0.0075, rel=2e-3)
    assert float(mort.at[("F", 85), "mort_rate"]) == pytest.approx(0.0700, rel=2e-3)
    assert float(mort.at[("M", 109), "mort_rate"]) == 1.0
    assert float(mort.at[("F", 109), "mort_rate"]) == 1.0
    assert mort["mort_rate"].max() <= 1.0
    inc = pd.read_csv(MODEL_DIR.parent / "incidence_table.csv",
                      index_col=["sex", "age"])
    assert all(p.startswith("[std]") for p in inc["provenance"])
    assert float(inc.at[("F", 65), "inc_rate"]) == pytest.approx(0.0110, rel=1e-9)
    assert float(inc.at[("M", 65), "inc_rate"]) == pytest.approx(0.0085, rel=1e-9)
    assert inc["inc_rate"].max() == 0.5           # the inc_cap shape device
    care = pd.read_csv(MODEL_DIR.parent / "care_table.csv", index_col="pflegegrad")
    assert list(care.index) == [1, 2, 3, 4, 5]
    assert care["entry_share"].sum() == pytest.approx(1.0, abs=1e-12)
    assert list(care["mort_mult"]) == [1.5, 2.5, 3.5, 6.0, 9.0]
    assert float(care.at[5, "det_rate"]) == 0.0   # grade 5 has nowhere to go
    assert all(care.at[g, "det_rate"] > care.at[g, "rec_rate"] for g in (1, 2, 3, 4))
    assert "FORCE" in care.at[1, "provenance"]
    scale = pd.read_csv(MODEL_DIR.parent / "benefit_scale_table.csv",
                        index_col=["staffel_id", "pflegegrad"])
    assert [float(scale.at[("delib_std", g), "benefit_pct"]) for g in range(1, 6)] == [
        0.0, 0.30, 0.50, 0.75, 1.0]
    assert [float(scale.at[("bahr", g), "benefit_pct"]) for g in range(1, 6)] == [
        0.10, 0.20, 0.30, 0.40, 1.0]
    assert all("[R8]" in scale.at[("bahr", g), "provenance"] for g in range(1, 6))
    expense = pd.read_csv(MODEL_DIR.parent / "expense_table.csv", index_col="item")
    assert float(expense.at["acq_permille", "value"]) == 25.0
    assert "Hoechstzillmersatz" in expense.at["acq_permille", "provenance"]
    assert all(p.startswith("[std]") for p in expense["provenance"])
    basis = pd.read_csv(MODEL_DIR.parent / "basis_table.csv", index_col="param")
    assert float(basis.at["rechnungszins", "value"]) == 0.01
    assert basis.at["rechnungszins", "provenance"].startswith("[REG-R14]")
    assert float(basis.at["omega_age", "value"]) == 110.0
    assert float(basis.at["unisex_mix_male", "value"]) == 0.5
    assert float(basis.at["beitragssumme_cap_age", "value"]) == 85.0
    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    assert list(lapse.index) == list(range(1, 41))
    assert float(lapse.at[1, "lapse_rate"]) == 0.06
    assert float(lapse.at[40, "lapse_rate"]) == 0.015
    assert all(p.startswith("[std]") for p in lapse["provenance"])
    assert "no lapse rate for a German Pflegerente" in lapse.at[1, "provenance"]
    surrender = pd.read_csv(MODEL_DIR.parent / "surrender_table.csv",
                            index_col="policy_year")
    assert float(surrender.at[1, "rkw_prem_ratio"]) == 0.0
    assert float(surrender.at[40, "rkw_prem_ratio"]) == 0.70
    assert surrender["rkw_prem_ratio"].is_monotonic_increasing
    points = pd.read_csv(MODEL_DIR.parent / "model_point_table.csv",
                         index_col="point_id")
    assert "provenance" not in points.columns    # the one exemption
    assert list(points.index) == list(range(1, 15))
    assert points.at[1, "policy_id"] == "PFL-000001"


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a licensed or company biometric basis.

    Point ``Data.mort_table_file`` at another same-schema file and the projection follows;
    no formula changes, and the model reads the replacement once per model as before.
    """
    import pandas as pd
    lighter = pd.read_csv(MODEL_DIR.parent / "mort_table.csv",
                          index_col=["sex", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5
    lighter.loc[("M", 109), "mort_rate"] = 1.0
    lighter.loc[("F", 109), "mort_rate"] = 1.0
    model = mx.read_model(MODEL_DIR, name="Pflege_DE_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_annuity"].sum()
            assert base == pytest.approx(TOTALS["claims_annuity"], abs=CENT)
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            # Lighter mortality means more lives reach the risk period and stay in care.
            assert p.result_cf()["claims_annuity"].sum() > base
            assert p.result_cf()["premiums"].sum() > TOTALS["premiums"]
            assert p.check_states() is True
            assert p.check_net_cf() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil
    model = mx.read_model(MODEL_DIR, name="Pflege_DE_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)
    reread = mx.read_model(dest, name="Pflege_DE_S_rt")
    try:
        p = reread.Projection[1]
        assert p.premium_mth_pp() == pytest.approx(PREMIUM_MTH_PP, abs=5e-6)
        for t, row in WORKED_EXAMPLE.items():
            assert p.pols_if(t) == pytest.approx(row[1], abs=SIX_DP)
            assert p.premiums(t) == pytest.approx(row[4], abs=CENT)
            assert p.claims(t, "ANNUITY") == pytest.approx(row[5], abs=CENT)
            assert p.net_cf(t) == pytest.approx(row[9], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_net_cf() is True
        assert p.check_states() is True
    finally:
        reread.close()
    assert model_files(dest) == model_files(MODEL_DIR)
