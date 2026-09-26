"""Golden and structural tests for BU_DE_S.

The golden values are the worked example in
products/berufsunfaehigkeit/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: a *selbstaendige
Berufsunfaehigkeitsversicherung* on a woman aged 30 at entry, occupational class BG1
(*Buerotaetigkeit*, ``occ_factor`` 1.00), an agreed *BU-Rente* of 1 500,00 EUR a month,
cover and benefit both to attained age 67, **no** *Karenzzeit*, a *Leistungsdynamik* of
2 % a year on each anniversary of onset, a **level** *Bruttobeitrag* with no
*Beitragsdynamik*, **monthly** payment (``prem_mode_months = 1``, ``freq_load`` 1.05), no
premium override so the *Bruttobeitrag* is **derived by equivalence**, a
*Beitragsverrechnung* of 0.70, no *Risikozuschlag*, the *AU-Klausel* off, a
*Wiedereingliederungshilfe* of six monthly *Renten*, and a new-business valuation date
(``duration_init_months = 0``).  Model point 1 is that cell.  ``pols_if_init() = 1.0`` and
``proj_len() = 12 x (67 - 30) = 444``, so the frame is 444 monthly rows ``t = 0 ... 443``
and the notes
print eighteen of them plus a Total row over all of them.  The equivalence gives
``P = 1,013.0697368527`` EUR p.a. of *Bruttobeitrag*, an instalment of
``P x 1.05 / 12 = 88.6436019746`` EUR and a *Zahlbeitrag* of ``0.70 x`` that.

Goldens are hard-coded rather than pickled so a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent, the
``pols_*`` ledgers to six decimals, and the totals at **full precision** -- 13 151,35 EUR
of *BU-Rente* that way against 13 151,28 EUR if the 444 rounded cells are added, and
-0,79 EUR of ``net_cf`` against -0,85 EUR.  The notes print both, and both are asserted.

What this module asserts, beyond the eighteen printed rows and the totals: the derived
*Bruttobeitrag* reached two independent ways; month 0 rebuilt term by term with a
calculator; the first inception and the first *BU-Rente* rebuilt from the annual rates
through the model's stated processing order; the Sec. 174 run-off traced through a single
cohort from its recovery to its *Wiedereingliederungshilfe*; the decrement closure, with
inception, recovery and reactivation **absent** from it; the *Brutto* / *Zahl* ratio
surviving aggregation to fifteen figures; the *Beitragsdynamik* variant (model point 4)
and its totals; what the two escalation options cost, from model point 12; the seven
published ``check_*`` identities with their per-``t`` residuals, ``check_net_cf`` --
delib's first ruling -- among them; and **one test per numbered modeling pitfall** in the
technical notes, eighteen of them, from weighting the premium by the wrong count to
assuming a *Beitragsdynamik* increase buys proportional cover.

The whole-model-point-table sweep is deliberately **not** here: the conventions suite owns
the library's single sweep, because a model point's first evaluation is by far the most
expensive thing in the run.
"""
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

MODEL_DIR = LIB / MODELS["BU_DE_S"][0]

# The notes' worked-example table, in full -- eighteen of the 444 monthly rows.
# t: (age, pols_if, pols_dis, pols_runoff, premiums, surplus_credit,
#     claims_bu_rente, claims_reintegration, expenses, claim_expenses, net_cf)
# claims_lapse is 0.00 at every t and is omitted from the notes' table for width; it is
# asserted in the row test all the same.
WORKED_EXAMPLE = {
    0:   (30, 1.000000, 0.000000, 0.000000, 88.64, 26.59,  0.00, 0.00, 946.57, 0.06, -884.58),
    1:   (30, 0.996575, 0.000073, 0.000000, 88.33, 26.50,  0.11, 0.00,   9.44, 0.06,   52.22),
    2:   (30, 0.993162, 0.000144, 0.000002, 88.02, 26.41,  0.22, 0.00,   9.41, 0.06,   51.93),
    3:   (30, 0.989760, 0.000213, 0.000005, 87.72, 26.31,  0.33, 0.00,   9.38, 0.06,   51.63),
    4:   (30, 0.986371, 0.000281, 0.000010, 87.41, 26.22,  0.44, 0.02,   9.35, 0.06,   51.33),
    5:   (30, 0.982994, 0.000346, 0.000015, 87.10, 26.13,  0.54, 0.03,   9.31, 0.06,   51.02),
    6:   (30, 0.979628, 0.000409, 0.000020, 86.80, 26.04,  0.64, 0.05,   9.28, 0.06,   50.73),
    11:  (30, 0.962974, 0.000701, 0.000042, 85.30, 25.59,  1.11, 0.11,   9.12, 0.07,   49.29),
    12:  (31, 0.959678, 0.000755, 0.000046, 85.00, 25.50,  1.20, 0.13,   9.09, 0.07,   49.01),
    59:  (34, 0.841342, 0.002980, 0.000098, 74.31, 22.29,  4.77, 0.30,   7.95, 0.10,   38.90),
    119: (39, 0.758020, 0.005878, 0.000124, 66.66, 20.00,  9.71, 0.38,   7.14, 0.15,   29.29),
    179: (44, 0.682155, 0.009149, 0.000151, 59.64, 17.89, 15.66, 0.46,   6.39, 0.20,   19.04),
    239: (49, 0.612199, 0.013550, 0.000218, 53.05, 15.91, 23.89, 0.67,   5.69, 0.30,    6.58),
    299: (54, 0.546787, 0.020491, 0.000347, 46.62, 13.99, 36.69, 1.06,   5.02, 0.47,  -10.61),
    359: (59, 0.484038, 0.030671, 0.000541, 40.14, 12.04, 55.29, 1.66,   4.34, 0.73,  -33.92),
    419: (64, 0.420930, 0.044223, 0.000811, 33.32, 10.00, 79.84, 2.48,   3.63, 1.08,  -63.71),
    442: (66, 0.395646, 0.050038, 0.000931, 30.55,  9.17, 90.30, 2.85,   3.34, 1.25,  -76.36),
    443: (66, 0.394543, 0.050263, 0.000936, 30.44,  9.13, 90.71, 2.87,   3.33, 1.25,  -76.85),
}

# The notes' Total row, summed at full precision and then rounded.
TOTALS = {
    "pols_if": 286.977233, "pols_dis": 7.397640, "pols_runoff": 0.134049,
    "premiums": 24771.06, "surplus_credit": 7431.32, "claims_bu_rente": 13151.35,
    "claims_reintegration": 409.61, "expenses": 3596.95, "claim_expenses": 182.61,
    "net_cf": -0.79,
}

# What the notes get if the 444 already-rounded cells are added instead -- printed there
# precisely because it is not the same number.
ROUNDED_CELL_TOTALS = {
    "pols_dis": 7.397656,
    "premiums": 24770.99, "surplus_credit": 7431.29, "claims_bu_rente": 13151.28,
    "claims_reintegration": 409.65, "expenses": 3596.99, "claim_expenses": 182.64,
    "net_cf": -0.85,
}

# The equivalence the notes print, per 1 EUR p.a. of Bruttobeitrag and per policy at
# inception, on the first-order shadow ledgers.
EQUIVALENCE = {
    "pv_prem": 29.0716529817, "pv_rente": 24452.4895291302,
    "pv_wgh": 531.1897520089, "pv_cost": 335.6805156244,
    "pv_admin": 544.5174674852, "bs_unit": 37.0,
}
PREM_GROSS_ANN = 1013.0697368527      # P
PREM_INSTALMENT = 88.6436019746       # P x 1.05 / 12
PREM_ZAHL = 62.0505213822             # 0.70 x the instalment
SURPLUS_CREDIT_PP = 26.5930805924     # 0.30 x the instalment

# The notes' closure split: death and lapse are the only exits.
CLOSURE = {"deaths": 0.069864886996, "lapses": 0.536693205531,
           "survivors": 0.393441907473}

# The Beitragsdynamik variant -- model point 4: entry age 25, BG2 (occ_factor 1.40),
# 1 200,00 EUR a month, premium_form dynamik at 3 %, ANNUAL payment (freq_load 1.00).
# t: (prem_gross_ann_pp, bu_rente_pp, pols_if, premiums, surplus_credit,
#     claims_bu_rente, claims_reintegration, expenses, claim_expenses, net_cf)
DYNAMIK = {
    0:   (1162.07, 1200.00, 1.000000, 1162.07, 348.62,   0.00, 0.00, 2489.01, 0.06, -1675.62),
    1:   (1162.07, 1200.00, 0.996585,    0.00,   0.00,   0.09, 0.00,    1.49, 0.06,    -1.65),
    11:  (1162.07, 1200.00, 0.963088,    0.00,   0.00,   0.93, 0.09,    1.44, 0.07,    -2.54),
    12:  (1196.93, 1236.00, 0.959802, 1147.82, 344.34,   1.01, 0.11,  104.74, 0.07,   697.54),
    13:  (1196.93, 1236.00, 0.956526,    0.00,   0.00,   1.09, 0.12,    1.43, 0.07,    -2.71),
    24:  (1232.84, 1273.08, 0.921229, 1133.87, 340.16,   1.86, 0.18,  103.43, 0.08,   688.16),
    60:  (1347.16, 1391.13, 0.840209, 1127.48, 338.24,   4.35, 0.27,  102.73, 0.11,   681.77),
    120: (1561.73, 1612.70, 0.758279, 1174.26, 352.28,   9.63, 0.40,  106.82, 0.16,   704.97),
    240: (2098.83, 2167.33, 0.615689, 1262.94, 378.88,  27.34, 0.79,  114.59, 0.29,   741.05),
    360: (2820.65, 2912.71, 0.494025, 1314.17, 394.25,  73.12, 2.41,  119.02, 0.65,   724.71),
    480: (3790.72, 3914.45, 0.379086, 1220.31, 366.09, 200.78, 7.37,  110.40, 1.43,   534.24),
    503: (3904.44, 4031.88, 0.355361,    0.00,   0.00, 238.26, 8.88,    0.53, 1.53,  -249.20),
}

DYNAMIK_TOTALS = {
    "pols_if": 312.698320, "premiums": 51825.40, "surplus_credit": 15547.62,
    "claims_bu_rente": 28702.79, "claims_reintegration": 1000.94,
    "expenses": 7516.25, "claim_expenses": 242.02, "net_cf": -1184.22,
}

DYNAMIK_ACQ = 2382.918707             # 0.025 x 1,162.0706385124 x 82.0231964511
DYNAMIK_BS_UNIT = 82.0231964511       # sum of 1.03^(y-1) over 42 policy years


# The worked example
@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_bu_anchor, t):
    """Every cell of the notes' eighteen printed rows, to the displayed precision."""
    (age, pols_if, pols_dis, pols_runoff, prem, credit, rente, reint,
     exp, claim_exp, net) = WORKED_EXAMPLE[t]
    p = de_bu_anchor
    assert p.age(t) == age
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_dis(t) == pytest.approx(pols_dis, abs=SIX_DP)
    assert p.pols_runoff(t) == pytest.approx(pols_runoff, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.surplus_credit(t) == pytest.approx(credit, abs=CENT)
    assert p.claims(t, "BU_RENTE") == pytest.approx(rente, abs=CENT)
    assert p.claims(t, "REINTEGRATION") == pytest.approx(reint, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.claim_expenses(t) == pytest.approx(claim_exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.claims(t, "LAPSE") == 0.0
    # The three ledgers decompose the in-force count on every printed row.
    assert p.pols_actv(t) == pytest.approx(
        p.pols_if(t) - p.pols_dis(t) - p.pols_runoff(t), abs=1e-12)
    # And on this cell the Karenzzeit is zero, so the premium-paying count is the active one.
    assert p.pols_prem(t) == pytest.approx(p.pols_actv(t), abs=1e-15)


def test_the_worked_example_totals_are_summed_at_full_precision(de_bu_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells.

    On a 444-row frame the difference is visible rather than notional: up to 7 cents on a
    money column and 6 cents on ``net_cf``, which at that magnitude is 8 % of the number
    itself.  The notes print both, so both are asserted.
    """
    df = de_bu_anchor.result_cf()
    for column, total in TOTALS.items():
        tol = SIX_DP * len(df) if column.startswith("pols_") else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    for column, total in ROUNDED_CELL_TOTALS.items():
        places = 6 if column.startswith("pols_") else 2
        assert df[column].round(places).sum() == pytest.approx(total, abs=5e-7), column
    assert df["claims_bu_rente"].sum() - df["claims_bu_rente"].round(2).sum() == (
        pytest.approx(0.07, abs=0.005))


def test_the_frame_spans_the_whole_projection(de_bu_anchor):
    """444 monthly rows, 0-based, ending at proj_len() - 1 -- the library's reading of it."""
    p = de_bu_anchor
    assert p.proj_len() == 12 * (67 - 30) == 444
    df = p.result_cf()
    assert list(df.index) == list(range(0, 444))
    assert df.index.name == "t"
    assert df.index[-1] == p.proj_len() - 1
    assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12) == 1.0
    assert p.age(0) == 30 and p.age(443) == 66


def test_the_bruttobeitrag_is_reached_two_independent_ways(de_bu_anchor):
    """P = 25,863.8772642487 / 25.5302042134 = 1,013.0697368527 EUR p.a.

    First from the five present values the notes print, arithmetic a reader can follow with
    a calculator; then from the model's own ``pv_*`` cells.  The instalment and the
    *Zahlbeitrag* follow, and the *Zahlbeitrag* and the *Beitragsverrechnung* add back to
    the instalment -- the ``check_prem_split`` identity in one line.
    """
    p = de_bu_anchor
    for cells, value in (("pv_prem_unit_first", "pv_prem"), ("pv_rente_first", "pv_rente"),
                         ("pv_wiedereingl_first", "pv_wgh"),
                         ("pv_claim_cost_first", "pv_cost"),
                         ("pv_admin_first", "pv_admin")):
        assert getattr(p, cells)() == pytest.approx(EQUIVALENCE[value], abs=5e-9), cells
    assert p.beitragssumme_unit() == EQUIVALENCE["bs_unit"] == 37.0

    numer = (EQUIVALENCE["pv_rente"] + EQUIVALENCE["pv_wgh"]
             + EQUIVALENCE["pv_cost"] + EQUIVALENCE["pv_admin"])
    denom = EQUIVALENCE["pv_prem"] * (1.0 - 0.09) - 0.025 * EQUIVALENCE["bs_unit"]
    # The quotient of the ten-decimal figures the notes print is P to nine figures; the
    # model carries the present values unrounded, hence the 1e-9 gap between the two.
    assert numer / denom == pytest.approx(PREM_GROSS_ANN, abs=5e-8)
    assert p.prem_gross_level_pp() == pytest.approx(PREM_GROSS_ANN, abs=5e-10)

    assert p.risk_factor() == 1.0
    assert p.gross_prem_ann() == 0.0            # derived, not overridden
    assert p.freq_load() == 1.05 and p.prem_mode_months() == 1
    assert p.prem_gross_pp(0) == pytest.approx(PREM_INSTALMENT, abs=5e-9)
    assert p.prem_gross_pp(0) == pytest.approx(PREM_GROSS_ANN * 1.05 / 12.0, abs=5e-8)
    assert p.prem_zahl_pp(0) == pytest.approx(PREM_ZAHL, abs=5e-9)
    assert p.surplus_credit_pp(0) == pytest.approx(SURPLUS_CREDIT_PP, abs=5e-9)
    # The Beitragssumme and the acquisition charge that sits on 2.5 % of it.
    assert p.prem_gross_level_pp() * p.beitragssumme_unit() == pytest.approx(
        37483.58, abs=CENT)


def test_month_zero_rebuilt_with_a_calculator(de_bu_anchor):
    """The notes' own independent rebuild of month 0, term by term.

    Acquisition ``0.025 x 1,013.0697368527 x 37 = 937.0895065887`` plus proportional
    administration ``0.09 x 88.6436019746 = 7.9779241777`` plus flat ``18 / 12 = 1.50``
    gives 946.5674307664; claim expense is ``800 x 0.000073111651``; and the five terms
    subtract to -884.5753987046.  None of it is the model's ``net_cf`` formula restated.
    """
    p = de_bu_anchor
    acq = 0.025 * PREM_GROSS_ANN * 37.0
    admin_prop = 0.09 * PREM_INSTALMENT
    admin_flat = 18.0 / 12.0
    assert p.expenses(0) == pytest.approx(acq + admin_prop + admin_flat, abs=5e-8)
    assert p.expenses(0) == pytest.approx(946.5674307664, abs=5e-7)
    assert p.claim_expenses(0) == pytest.approx(800.0 * 0.000073111651, abs=5e-9)
    rebuilt = (PREM_INSTALMENT - SURPLUS_CREDIT_PP - 0.0
               - p.expenses(0) - p.claim_expenses(0))
    assert rebuilt == pytest.approx(-884.5753987046, abs=5e-7)
    assert p.net_cf(0) == pytest.approx(rebuilt, abs=5e-9)


def test_the_first_inception_and_the_first_bu_rente_from_the_annual_rates(de_bu_anchor):
    """Composed inception 0.001100 x 1.00 x 0.80 x 1.00, converted and applied in order.

    Mortality first, then lapse on the survivors, then incidence on the survivors of both:
    ``(1 - 0.000029171347)(1 - 0.003396053199) x 0.000073362928 = 0.000073111651``.  Taking
    incidence first gives 0.000073362928 -- 0,34 % out in month 1, compounding over 444.
    """
    p = de_bu_anchor
    assert p.inc_rate(0) == pytest.approx(0.000880, rel=1e-12)
    i_m = p.inc_rate_mth(0)
    q_m = p.mort_rate_mth(0)
    w_m = p.lapse_rate_mth(0)
    assert i_m == pytest.approx(0.000073362928, abs=5e-13)
    assert q_m == pytest.approx(0.000029171347, abs=5e-13)
    assert w_m == pytest.approx(0.003396053199, abs=5e-13)
    ordered = (1.0 - q_m) * (1.0 - w_m) * i_m
    assert ordered == pytest.approx(0.000073111651, abs=5e-13)
    assert p.pols_inception(0) == pytest.approx(ordered, rel=1e-12)
    assert p.pols_dis(1) == pytest.approx(ordered, rel=1e-12)
    # Incidence-first would be visibly different, which is why the order is a [std] choice.
    assert i_m / ordered - 1.0 == pytest.approx(0.00344, abs=5e-6)
    # The first BU-Rente and the first assessment cost follow directly.
    assert p.claims(1, "BU_RENTE") == pytest.approx(1500.0 * ordered, rel=1e-12)
    assert p.claims(1, "BU_RENTE") == pytest.approx(0.1096674758, abs=5e-9)


def test_the_run_off_is_three_months_wide_traced_through_one_cohort(de_bu_anchor):
    """One cohort, from its recovery at the end of month 1 to its reintegration at month 4.

    ``pols_recovery(1) = 0.000073111651 x (1 - q^i_m(1,1)) x r_m(1) = 0.00000173129246``,
    and that is exactly ``pols_runoff(2)``, not a return to ``pols_actv``.  It is still paid
    in month 2, and three months later the survivors complete the run-off and are paid
    ``claims_reintegration(4) = 0.0155802686`` -- the first non-zero cell in that column.
    """
    p = de_bu_anchor
    qi_m = p.mort_rate_dis_mth(1, 1)
    r_m = p.recov_rate_mth(1)
    rec = p.pols_dis_dur(1, 1) * (1.0 - qi_m) * r_m
    assert rec == pytest.approx(0.00000173129246, abs=5e-15)
    assert p.pols_recovery(1) == pytest.approx(rec, rel=1e-12)
    assert p.pols_runoff(2) == pytest.approx(rec, rel=1e-12)
    # It is still being paid while it is in run-off.
    assert p.claims(2, "BU_RENTE") == pytest.approx(
        1500.0 * (p.pols_dis(2) + p.pols_runoff(2)), rel=1e-12)
    assert p.claims(2, "BU_RENTE") == pytest.approx(0.2189128510, abs=5e-9)
    # Three months later it completes the run-off and is reintegrated.
    assert p.claims(3, "REINTEGRATION") == 0.0
    assert p.claims(4, "REINTEGRATION") == pytest.approx(0.0155802686, abs=5e-9)
    assert p.claims(4, "REINTEGRATION") == pytest.approx(
        6 * p.runoff_val(4, 3) * (1.0 - p.mort_rate_mth(4)), rel=1e-12)
    assert p.pols_reactivation(4) > 0.0 and p.pols_reactivation(3) == 0.0


def test_the_decrements_close_three_ways(de_bu_anchor):
    """Deaths plus lapses plus survivors equal exactly one policy.

    Inception, recovery and reactivation are **absent** from the identity: they are
    transfers between the three ledgers, not exits, and a model listing them there has
    already lost mass.  6,99 % of the cohort dies, 53,67 % lapses and 39,34 % survives to
    the *Endalter* with nothing payable.
    """
    p = de_bu_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(0, n))
    lapses = sum(p.pols_lapse(t) for t in range(0, n))
    survivors = p.pols_if_at(n - 1, "END")
    assert deaths == pytest.approx(CLOSURE["deaths"], abs=5e-12)
    assert lapses == pytest.approx(CLOSURE["lapses"], abs=5e-12)
    assert survivors == pytest.approx(CLOSURE["survivors"], abs=5e-12)
    assert deaths + lapses + survivors == pytest.approx(1.0, abs=1e-11)
    # A claim in payment is paid to the horizon and then simply stops.
    assert p.claims(n - 1, "BU_RENTE") > 0.0


def test_the_brutto_zahl_ratio_survives_aggregation(de_bu_anchor):
    """Sum premiums / sum collected = 1 / 0.70 to fifteen figures.

    It has to be: ``freq_load`` scales the *Bruttobeitrag* and the *Beitragsverrechnung*
    together so the *Ratenzahlungszuschlag* cancels, and ``beitragsverrechnung`` is
    constant.  A model carrying one premium stream could not show it.
    """
    p = de_bu_anchor
    df = p.result_cf()
    gross = df["premiums"].sum()
    collected = (df["premiums"] - df["surplus_credit"]).sum()
    assert gross == pytest.approx(24771.0595905881, abs=5e-7)
    assert collected == pytest.approx(17339.7417134117, abs=5e-7)
    assert gross / collected == pytest.approx(1.0 / 0.70, rel=1e-14)
    # And the undiscounted projection very nearly breaks even -- a property of the shipped
    # [std] parameters and emphatically not an identity, since the equivalence is struck
    # discounted, on first-order bases and without lapse.
    outgo = (df["claims_bu_rente"].sum() + df["claims_reintegration"].sum()
             + df["claims_lapse"].sum() + df["expenses"].sum()
             + df["claim_expenses"].sum())
    assert outgo == pytest.approx(17340.53, abs=CENT)
    assert collected - outgo == pytest.approx(-0.79, abs=CENT)


def test_what_the_two_escalation_options_cost(berufsunfaehigkeit, de_bu_anchor):
    """Model point 12 is the anchor with both escalations off: 865,95 against 1 013,07 EUR.

    Everything else is identical, so the difference of 147,12 EUR p.a. is the clean measure
    of what the two options cost -- 14,5 % of the anchor's *Bruttobeitrag*.  It is not
    additive, because both are paid out of the same claim population.
    """
    plain = berufsunfaehigkeit.Projection[12]
    assert plain.leistungsdyn_rate() == 0.0
    assert plain.wiedereingliederung_months() == 0
    assert plain.prem_gross_level_pp() == pytest.approx(865.9512322010, abs=5e-8)
    diff = de_bu_anchor.prem_gross_level_pp() - plain.prem_gross_level_pp()
    assert diff == pytest.approx(147.1185046517, abs=5e-8)
    assert diff / de_bu_anchor.prem_gross_level_pp() == pytest.approx(0.145, abs=0.0005)
    # With the option off the column is structurally zero, not merely small.
    assert plain.result_cf()["claims_reintegration"].sum() == 0.0


# The Beitragsdynamik variant -- model point 4
@pytest.mark.parametrize("t", sorted(DYNAMIK))
def test_dynamik_variant_row(berufsunfaehigkeit, t):
    """The notes' second table: annual payment on the escalating form."""
    (prem_ann, rente, pols_if, prem, credit, bu_rente, reint,
     exp, claim_exp, net) = DYNAMIK[t]
    p = berufsunfaehigkeit.Projection[4]
    assert p.premium_form() == "dynamik" and p.beitragsdyn_rate() == 0.03
    assert p.prem_mode() == "annual" and p.prem_mode_months() == 12
    assert p.prem_gross_ann_pp(t) == pytest.approx(prem_ann, abs=CENT)
    assert p.bu_rente_pp(t) == pytest.approx(rente, abs=CENT)
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.surplus_credit(t) == pytest.approx(credit, abs=CENT)
    assert p.claims(t, "BU_RENTE") == pytest.approx(bu_rente, abs=CENT)
    assert p.claims(t, "REINTEGRATION") == pytest.approx(reint, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.claim_expenses(t) == pytest.approx(claim_exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_dynamik_variant_totals_and_its_zillmerung_base(berufsunfaehigkeit):
    """504 rows, the full-precision totals, and the *Beitragssumme* that escalates too.

    A 42-year escalating *Beitragssumme* is 82,02 times the first year's premium, not 42
    times it, so the *Zillmerung* base grows with the escalation rate as well as the term:
    the month-0 acquisition charge is 2 382,92 EUR of that row's 2 489,01 EUR.
    """
    p = berufsunfaehigkeit.Projection[4]
    assert p.proj_len() == 12 * (67 - 25) == 504
    df = p.result_cf()
    assert list(df.index) == list(range(0, 504))
    for column, total in DYNAMIK_TOTALS.items():
        tol = SIX_DP * len(df) if column.startswith("pols_") else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert p.beitragssumme_unit() == pytest.approx(DYNAMIK_BS_UNIT, abs=5e-9)
    acq = 0.025 * p.prem_gross_level_pp() * p.beitragssumme_unit()
    assert acq == pytest.approx(DYNAMIK_ACQ, abs=5e-7)
    assert p.expenses(0) == pytest.approx(
        acq + 0.09 * p.prem_gross_pp(0) + 18.0 / 12.0, abs=5e-8)
    # Adding the 504 rounded cells gives different totals, and the notes say so.
    assert df["premiums"].round(2).sum() == pytest.approx(51825.44, abs=CENT)
    assert df["claims_bu_rente"].round(2).sum() == pytest.approx(28702.67, abs=CENT)


def test_the_annual_payer_pays_in_month_zero_and_every_twelfth_month(berufsunfaehigkeit):
    """The whole policy year's premium in one instalment, and exactly zero in between.

    That is why the grid is monthly and the frequency a parameter rather than a smoothing:
    in the eleven months between payments ``premiums`` and ``surplus_credit`` are exactly
    zero while claims and the flat administration charge run on.
    """
    p = berufsunfaehigkeit.Projection[4]
    assert [p.prem_due(t) for t in range(0, 14)] == (
        [1.0] + [0.0] * 11 + [1.0, 0.0])
    assert all(p.premiums(t) == 0.0 for t in range(1, 12))
    assert all(p.surplus_credit(t) == 0.0 for t in range(1, 12))
    assert all(p.expenses(t) == pytest.approx(18.0 / 12.0 * p.pols_if(t), rel=1e-12)
               for t in range(1, 12))


# Pitfall 1 -- weighting the premium by pols_if instead of pols_prem
def test_pitfall_01_the_premium_is_weighted_by_the_premium_paying_count(
        berufsunfaehigkeit, de_bu_anchor):
    """The classic German BU error: charging premium to lives in claim.

    It silently deletes the *Beitragsbefreiung* and leaves every total looking plausible.
    ``premiums(t)`` must be ``prem_gross_pp(t) x pols_prem(t)``, and ``pols_prem`` must be
    strictly below ``pols_if`` wherever anyone is in claim past the *Karenzzeit*.
    """
    p = de_bu_anchor
    for t in (0, 1, 12, 240, 443):
        assert p.premiums(t) == pytest.approx(
            p.prem_gross_pp(t) * p.pols_prem(t), rel=1e-15)
    df = p.result_cf()
    claiming = df["pols_dis"] + df["pols_runoff"]
    assert (df.loc[claiming > 0, "pols_prem"] < df.loc[claiming > 0, "pols_if"]).all()
    # The size of the mistake: weighting by pols_if would add this much premium income.
    wrong = sum(p.prem_gross_pp(t) * p.pols_if(t) for t in range(0, p.proj_len()))
    assert wrong > df["premiums"].sum()
    assert wrong / df["premiums"].sum() - 1.0 == pytest.approx(0.026, abs=0.002)
    # An in-force claim pays no premium at all: model point 7 opens leistungspflichtig.
    in_claim = berufsunfaehigkeit.Projection[7]
    assert in_claim.status() == "leistung"
    assert in_claim.pols_actv(0) == 0.0 and in_claim.pols_dis(0) == 1.0
    assert in_claim.pols_prem(0) == 0.0 and in_claim.premiums(0) == 0.0
    assert in_claim.claims(0, "BU_RENTE") == pytest.approx(1800.0, abs=CENT)


# Pitfall 2 -- one premium stream instead of two
def test_pitfall_02_two_premium_streams_are_projected_not_one(de_bu_anchor):
    """A model carrying only the *Zahlbeitrag* assumes the credit is permanent; one carrying
    only the *Bruttobeitrag* overstates collected premium by 42,86 %.  Both columns are
    published and ``check_prem_split`` reconciles them.
    """
    p = de_bu_anchor
    df = p.result_cf()
    assert "premiums" in df.columns and "surplus_credit" in df.columns
    assert p.check_prem_split() is True
    assert p.check_prem_split_resid(240) == pytest.approx(0.0, abs=1e-9)
    gross, credit = df["premiums"].sum(), df["surplus_credit"].sum()
    assert credit / gross == pytest.approx(0.30, rel=1e-14)
    assert gross / (gross - credit) - 1.0 == pytest.approx(0.428571428571, abs=5e-12)
    assert p.prem_gross_pp(0) / p.prem_zahl_pp(0) == pytest.approx(1.0 / 0.70, rel=1e-14)


# Pitfall 3 -- one mortality rate for both states
def test_pitfall_03_disabled_and_active_mortality_are_different_rates(de_bu_anchor):
    """12.0x active mortality in the first claim year, 4.8x ultimately, at every age.

    The shipped disabled column is exactly 4.00 x the nine-decimal active column rather than
    an independently rounded formula, which is what lets this be an **exact** identity.
    """
    p = de_bu_anchor
    for t in (0, 12, 120, 300, 443):
        assert p.mort_rate_dis(t, 1) / p.mort_rate(t) == pytest.approx(12.0, rel=1e-12)
        assert p.mort_rate_dis(t, 61) / p.mort_rate(t) == pytest.approx(4.8, rel=1e-12)
        assert p.mort_rate_dis_at_age(p.age(t)) == pytest.approx(
            4.0 * p.mort_rate_at_age(p.age(t)), rel=1e-12)
    # The select factors, and their monotone decline over the first claim years.
    assert [p.mort_dis_sel_factor(z) for z in (1, 13, 25, 37, 49, 61, 121)] == [
        3.0, 2.0, 1.6, 1.4, 1.3, 1.2, 1.2]


# Pitfall 4 -- a flat reactivation rate
def test_pitfall_04_reactivation_is_front_loaded_not_flat(de_bu_anchor):
    """0.250 in claim year 1 falling to 0.006 ultimately, strictly over the first five.

    A flat rate at the year-1 level roughly halves projected benefit and at the ultimate
    level roughly doubles it: a claim surviving two years runs to the *Leistungsendalter*.
    """
    p = de_bu_anchor
    assert p.recov_rate(1) == pytest.approx(0.250, rel=1e-12)
    assert p.recov_rate(13) == pytest.approx(0.130, rel=1e-12)
    assert p.recov_rate(49) == pytest.approx(0.025, rel=1e-12)
    by_year = [p.recov_rate(12 * (y - 1) + 1) for y in range(1, 12)]
    assert by_year == [0.250, 0.130, 0.070, 0.040, 0.025, 0.018, 0.014, 0.011,
                       0.009, 0.008, 0.006]
    assert all(by_year[i] > by_year[i + 1] for i in range(5))


# Pitfall 5 -- forgetting the Sec. 174 three-month run-off
def test_pitfall_05_the_run_off_is_not_forgotten(de_bu_anchor):
    """A recovery does not stop the annuity in the month it happens.

    Three further monthly payments follow, so ``pols_runoff(t)`` is positive wherever there
    was a recovery in any of the previous three months, and suppressing the run-off would
    strictly reduce benefit -- by 206,41 EUR of the 13 151,35 EUR of *BU-Rente*.
    """
    p = de_bu_anchor
    n = p.proj_len()
    for t in range(1, n):
        recent = sum(p.pols_recovery(t - k) for k in (1, 2, 3) if t - k >= 0)
        if recent > 0.0:
            assert p.pols_runoff(t) > 0.0, t
    run_off_benefit = sum(sum(p.runoff_cohorts(t)[1]) for t in range(0, n))
    assert run_off_benefit == pytest.approx(206.41, abs=CENT)
    total = p.result_cf()["claims_bu_rente"].sum()
    assert run_off_benefit / total == pytest.approx(0.0157, abs=0.0005)


# Pitfall 6 -- recovery and konkrete Verweisung as two decrements
def test_pitfall_06_there_is_exactly_one_claim_termination_rate(
        berufsunfaehigkeit, de_bu_anchor):
    """``recov_rate`` covers recovery **and** *konkrete Verweisung*, which end the benefit
    the same way and which no public data separates, so ``pols_recovery`` is the whole
    claim-termination-other-than-death flow and a second decrement's names must not exist.
    """
    p = de_bu_anchor
    names = set(berufsunfaehigkeit.Projection.cells) | set(
        berufsunfaehigkeit.Projection.refs)
    for absent in ("verweisung_rate", "recov_rate_konkret", "pols_verweisung",
                   "pols_referral", "konkret_rate", "abstract_rate"):
        assert absent not in names, absent
    # pols_recovery is exactly the one rate applied to the disabled cohorts.
    for t in (5, 100, 400):
        rebuilt = sum(
            p.pols_dis_dur(t, z) * (1.0 - p.mort_rate_dis_mth(t, z)) * p.recov_rate_mth(z)
            for z in range(1, t + 2))
        assert p.pols_recovery(t) == pytest.approx(rebuilt, rel=1e-11)


# Pitfall 7 -- the Karenzzeit is not the six-month prognosis period
def test_pitfall_07_the_karenzzeit_is_not_the_prognosis_period(de_bu_anchor):
    """With ``K = 0`` the first *BU-Rente* falls the month **after** an onset.

    The six-month *Prognosezeitraum* is part of the *definition* of *Berufsunfaehigkeit* and
    never defers a payment; a model confusing the two shows the benefit six months late.
    """
    p = de_bu_anchor
    assert p.karenz_months() == 0
    first_claim = min(t for t in range(0, 20) if p.pols_dis(t) > 0.0)
    assert first_claim == 1
    assert p.claims(first_claim, "BU_RENTE") > 0.0
    assert p.claims(0, "BU_RENTE") == 0.0        # nobody is in claim in month 0
    # A model deferring six months would show zeros through month 6 -- it does not.
    assert all(p.claims(t, "BU_RENTE") > 0.0 for t in range(1, 8))


# Pitfall 8 -- waiving the premium during the Karenzzeit
def test_pitfall_08_the_premium_runs_through_the_karenzzeit(
        berufsunfaehigkeit, de_bu_anchor):
    """The *Beitragsbefreiung* runs with the **benefit**, so a life not yet paid still pays.

    Model point 5 carries ``K = 6``: ``pols_prem`` is ``pols_actv`` plus the cohorts at
    ``z <= 6``, and exceeds it at every month but the first.  On the anchor they are equal.
    """
    karenz = berufsunfaehigkeit.Projection[5]
    assert karenz.karenz_months() == 6
    assert karenz.prem_mode() == "quarterly" and karenz.prem_mode_months() == 3
    for t in (1, 12, 100, 323):
        inside = sum(karenz.pols_dis_dur(t, z) for z in range(1, 7))
        assert karenz.pols_prem(t) == pytest.approx(
            karenz.pols_actv(t) + inside, rel=1e-13)
    n = karenz.proj_len()
    above = [t for t in range(0, n)
             if karenz.pols_prem(t) - karenz.pols_actv(t) > 1e-15]
    assert len(above) == n - 1      # every month but the first
    # The anchor has no Karenzzeit at all.
    assert de_bu_anchor.karenz_months() == 0
    assert max(abs(de_bu_anchor.pols_prem(t) - de_bu_anchor.pols_actv(t))
               for t in range(0, 444)) == 0.0


# Pitfall 9 -- escalating the BU-Rente on the wrong clock
def test_pitfall_09_the_two_escalations_run_on_different_clocks(de_bu_anchor):
    """*Leistungsdynamik* steps on the anniversary of **onset**, not of the policy.

    With ``beitragsdyn_rate = 0`` the insured *BU-Rente* is flat at 1 500,00 EUR while the
    amount **in payment** steps at every twelfth month of claim duration.
    """
    p = de_bu_anchor
    assert p.premium_form() == "level" and p.beitragsdyn_rate() == 0.0
    assert p.leistungsdyn_rate() == 0.02
    assert all(p.bu_rente_pp(t) == 1500.0 for t in (0, 11, 12, 200, 443))
    for t in (200, 400):
        assert p.rente_pay_pp(t, 12) == pytest.approx(p.rente_pay_pp(t, 1), rel=1e-15)
        assert p.rente_pay_pp(t, 13) == pytest.approx(
            1.02 * p.rente_pay_pp(t, 12), rel=1e-13)
        assert p.rente_pay_pp(t, 25) == pytest.approx(
            1.02 ** 2 * p.rente_pay_pp(t, 1), rel=1e-13)
    assert p.leistungsdyn_factor(13) == pytest.approx(1.02, rel=1e-15)
    assert p.leistungsdyn_factor(361) == pytest.approx(1.02 ** 30, rel=1e-13)
    # Compounding 2 % over a thirty-year claim raises the final payment to about 1.70x.
    assert p.leistungsdyn_factor(361) == pytest.approx(1.8114, abs=5e-5)


# Pitfall 10 -- double-counting the Anerkennungsquote
def test_pitfall_10_the_inception_rate_composition_is_published(
        berufsunfaehigkeit, de_bu_anchor):
    """``inc_rate = inc_rate_base x occ_factor x accept_factor x au_uplift``, exactly.

    The shipped table is **gross** of declinature and ``accept_factor = 0.80`` sits on top
    of it, so a substituted table already net must use the factor at 1.00.  Publishing the
    composition makes that visible; ``risk_factor`` is deliberately not among the three.
    """
    p = de_bu_anchor
    assert berufsunfaehigkeit.Projection.accept_factor == 0.80
    for t in (0, 60, 240, 443):
        assert p.inc_rate(t) == pytest.approx(
            p.inc_rate_base(t) * p.occ_factor() * 0.80 * p.au_uplift(), rel=1e-15)
        assert p.inc_rate(t) == pytest.approx(0.80 * p.inc_rate_base(t), rel=1e-15)
        assert p.inc_rate(t) < p.inc_rate_base(t)
    # The table's own shape: flat to 30, then two slopes.
    tbl = de_bu_anchor.data.inception_table()
    assert float(tbl.loc[30, "inc_rate"]) == pytest.approx(0.001100, rel=1e-6)
    assert float(tbl.loc[45, "inc_rate"]) / float(tbl.loc[44, "inc_rate"]) == (
        pytest.approx(1.06, rel=1e-6))
    assert float(tbl.loc[60, "inc_rate"]) / float(tbl.loc[59, "inc_rate"]) == (
        pytest.approx(1.13, rel=1e-6))


# Pitfall 11 -- confusing occ_factor with risk_factor
def test_pitfall_11_the_two_rating_multipliers_do_different_things(
        berufsunfaehigkeit, de_bu_anchor):
    """``occ_factor`` loads the inception rate; ``risk_factor`` loads the premium alone.

    Model point 3 is the anchor at BG4: the inception rate scales by exactly 3.00 while the
    premium scales by 2.932141, slightly *below* it, because the flat administration and
    assessment costs do not scale with the risk.  Model point 11 carries a *Risikozuschlag*
    of 1.50: against its own unloaded twin every decrement, claim and claim expense is
    identical to the last bit while premium income scales by exactly 1.50.
    """
    anchor, heavy = de_bu_anchor, berufsunfaehigkeit.Projection[3]
    assert anchor.occ_factor() == 1.0 and heavy.occ_factor() == 3.0
    for t in (0, 120, 443):
        assert heavy.inc_rate(t) == pytest.approx(3.0 * anchor.inc_rate(t), rel=1e-13)
    ratio = heavy.prem_gross_level_pp() / anchor.prem_gross_level_pp()
    assert heavy.prem_gross_level_pp() == pytest.approx(2970.4637021005, abs=5e-7)
    assert ratio == pytest.approx(2.932141, abs=5e-7)
    assert ratio < 3.0

    model = mx.read_model(MODEL_DIR, name="BU_DE_S_rho")
    try:
        loaded = model.Projection[11]
        assert loaded.risk_factor() == 1.5
        loaded_df = loaded.result_cf()
        assert loaded.prem_gross_level_pp() == pytest.approx(2366.8283506001, abs=5e-7)
        table = model.Data.model_point_table().copy()
        table.loc[11, "risk_factor"] = 1.0
        model.Data.model_point_table.clear_all()
        model.Data.model_point_table[()] = table
        model.Projection.clear_all()
        plain = model.Projection[11]
        assert plain.risk_factor() == 1.0
        plain_df = plain.result_cf()
        assert loaded_df["premiums"].sum() == pytest.approx(
            1.5 * plain_df["premiums"].sum(), rel=1e-12)
        assert loaded_df["surplus_credit"].sum() == pytest.approx(
            1.5 * plain_df["surplus_credit"].sum(), rel=1e-12)
        for column in ("pols_if", "pols_actv", "pols_dis", "pols_runoff", "pols_prem",
                       "claims_bu_rente", "claims_reintegration", "claims_lapse",
                       "claim_expenses"):
            assert (loaded_df[column] - plain_df[column]).abs().max() == 0.0, column
        # The loaded contract is therefore projected above its own modelled cost.
        assert loaded_df["net_cf"].sum() > plain_df["net_cf"].sum()
    finally:
        model.close()


# Pitfall 12 -- letting sex price
def test_pitfall_12_sex_does_not_price(berufsunfaehigkeit, de_bu_anchor):
    """Unlawful in Germany for contracts written from 21 December 2012: model points 1 and 2
    differ in ``sex`` alone, so their premium and every column of their frames must be
    identical -- not close, identical.
    """
    female, male = de_bu_anchor, berufsunfaehigkeit.Projection[2]
    assert female.sex() == "F" and male.sex() == "M"
    assert male.entry_age() == female.entry_age() == 30
    assert male.berufsgruppe() == female.berufsgruppe() == "BG1"
    assert male.prem_gross_level_pp() == female.prem_gross_level_pp()
    diff = (male.result_cf() - female.result_cf()).abs().max().max()
    assert diff == 0.0
    with pytest.raises(FormulaError):
        berufsunfaehigkeit.Projection[1].claims(1, "DEATH")


# Pitfall 13 -- running benefit past the Leistungsendalter
def test_pitfall_13_benefit_stops_at_the_leistungsendalter_and_premium_does_not(
        berufsunfaehigkeit):
    """Model point 9: cover to 67, benefit to 63 -- two contractual terms, not one.

    From attained age 63 the *BU-Rente* and the claim-maintenance component of
    ``claim_expenses`` are zero while the premium runs on and collects 2 244,03 EUR more.
    """
    p = berufsunfaehigkeit.Projection[9]
    assert p.cover_end_age() == 67 and p.benefit_end_age() == 63
    assert p.entry_age() == 45 and p.proj_len() == 12 * (67 - 45) == 264
    boundary = min(t for t in range(0, p.proj_len()) if p.age(t) >= 63)
    assert boundary == 216
    assert p.claims(215, "BU_RENTE") > 0.0
    assert all(p.claims(t, "BU_RENTE") == 0.0 for t in range(boundary, p.proj_len()))
    assert all(p.claim_expenses(t) == pytest.approx(800.0 * p.pols_inception(t), rel=1e-12)
               for t in (216, 240, 263))
    assert all(p.premiums(t) > 0.0 for t in range(boundary, p.proj_len()))
    assert sum(p.premiums(t) for t in range(boundary, p.proj_len())) == (
        pytest.approx(2244.03, abs=CENT))
    assert p.check_cover_end() is True
    for t in (0, 215, 216, 263):
        assert p.check_cover_end_resid(t) == pytest.approx(0.0, abs=1e-12)


# Pitfall 14 -- charging acquisition cost to an in-force model point
def test_pitfall_14_no_acquisition_charge_on_an_in_force_point(
        berufsunfaehigkeit, de_bu_anchor):
    """An in-force point has already incurred it, and charging it again would put a spurious
    strain in month 0 of every in-force cell.  On model point 6 (180 policy months elapsed)
    ``expenses(0)`` is exactly the proportional and flat administration charges; on model
    point 7 (200 months, in claim) it is one month of the flat charge alone.
    """
    in_force = berufsunfaehigkeit.Projection[6]
    assert in_force.duration_init_months() == 180
    assert in_force.prem_mode() == "half_yearly"
    assert in_force.proj_len() == 12 * (67 - 30) - 180 == 264
    expected = (0.09 * in_force.prem_gross_pp(0) * in_force.pols_prem(0)
                + 18.0 / 12.0 * in_force.pols_if(0))
    assert in_force.expenses(0) == pytest.approx(expected, rel=1e-15)
    assert in_force.expenses(0) == pytest.approx(48.00, abs=CENT)
    # The shadow still runs from inception, so the in-force cell prices as its own twin did.
    assert in_force.prem_gross_level_pp() == pytest.approx(
        de_bu_anchor.prem_gross_level_pp(), rel=1e-15)

    in_claim = berufsunfaehigkeit.Projection[7]
    assert in_claim.duration_init_months() == 200
    assert in_claim.expenses(0) == pytest.approx(18.0 / 12.0, rel=1e-15)
    # The anchor is new business and does carry it, in month 0 and nowhere else.
    assert de_bu_anchor.duration_init_months() == 0
    assert de_bu_anchor.expenses(0) > 900.0
    assert de_bu_anchor.expenses(1) < 10.0


# Pitfall 15 -- deleting the disabled mass at the Leistungsendalter
def test_pitfall_15_the_disabled_mass_is_held_not_deleted(berufsunfaehigkeit):
    """Deleting the cohorts at the *Leistungsendalter* breaks both state identities.

    On model point 9 the ledgers roll on past attained age 63: ``pols_dis`` is still
    growing, ``pols_if`` is continuous, and both identities still close.
    """
    p = berufsunfaehigkeit.Projection[9]
    assert p.pols_dis(216) > p.pols_dis(215) > 0.0
    step = abs(p.pols_if(216) - p.pols_if(215))
    typical = abs(p.pols_if(215) - p.pols_if(214))
    assert step == pytest.approx(typical, rel=0.05)      # no jump at the boundary
    assert p.check_states() is True
    assert p.check_pols_roll_fwd() is True
    # Those lives do not resume paying premium: the waiver is keyed to the state [std].
    assert p.pols_prem(216) == pytest.approx(p.pols_actv(216), abs=1e-15)
    assert p.pols_prem(216) < p.pols_if(216)


# Pitfall 16 -- paying the Wiedereingliederungshilfe on every recovery
def test_pitfall_16_the_reintegration_benefit_is_paid_on_a_completed_run_off(
        de_bu_anchor):
    """A life that dies inside the run-off never returns to work and is paid nothing.

    ``6 x sum_t V_r(t,3) x (1 - q^a_m(t))`` = 409,61 EUR, strictly below the 418,79 EUR a
    model paying on every recovery would show; the difference is the run-off's mortality.
    """
    p = de_bu_anchor
    n = p.proj_len()
    paid = p.result_cf()["claims_reintegration"].sum()
    identity = sum(6 * p.runoff_val(t, 3) * (1.0 - p.mort_rate_mth(t))
                   for t in range(0, n))
    naive = sum(6 * p.runoff_value_in(t) for t in range(0, n))
    assert paid == pytest.approx(identity, rel=1e-12)
    assert paid == pytest.approx(409.61, abs=CENT)
    assert naive == pytest.approx(418.79, abs=CENT)
    assert paid < naive
    # It is six monthly Renten of the amount the cohort was on, not of the insured amount.
    for t in (10, 200, 443):
        assert p.claims(t, "REINTEGRATION") == pytest.approx(
            6 * p.runoff_val(t, 3) * (1.0 - p.mort_rate_mth(t)), rel=1e-12)


# Pitfall 17 -- inventing a surrender or paid-up cash flow
def test_pitfall_17_a_lapse_pays_nothing_at_any_duration(
        berufsunfaehigkeit, de_bu_anchor):
    """Sec. 169 and Sec. 165 VVG through Sec. 176 give this contract both and the model
    prices neither, both being the release of a reserve it does not compute.  The zero
    column is the scope statement; the absent names are what a savings model would add.
    """
    p = de_bu_anchor
    assert all(p.claims(t, "LAPSE") == 0.0 for t in (0, 1, 120, 443))
    assert (p.result_cf()["claims_lapse"] == 0.0).all()
    names = set(berufsunfaehigkeit.Projection.cells) | set(
        berufsunfaehigkeit.Projection.refs)
    for absent in ("av_pp_at", "av_at", "prem_to_av_pp", "cv_pp", "surr_charge_rate",
                   "surr_value_pp", "paid_up_factor", "asset_share", "mvr",
                   "claims_surr", "withdrawals", "wd_free_pp", "claims_death",
                   "benefit_death_pp", "claims_maturity", "pols_maturity"):
        assert absent not in names, absent
    with pytest.raises(FormulaError):
        p.claims(1, "SURRENDER")


# Pitfall 18 -- assuming the Beitragsdynamik buys proportional cover
def test_pitfall_18_the_beitragsdynamik_escalates_both_sides_by_the_same_factor(
        berufsunfaehigkeit):
    """Model point 4: both grow by exactly 1.03 a year and are flat within a policy year.

    That is internally consistent and **not** the German market's practice, which prices
    each increment at the attained age reached so a given increase buys **less** than
    proportional cover.  The direction is recorded; the construction is what is asserted.
    """
    p = berufsunfaehigkeit.Projection[4]
    assert p.premium_form() == "dynamik" and p.beitragsdyn_rate() == 0.03
    assert p.bu_rente_pp(12) / p.bu_rente_pp(0) == pytest.approx(1.03, rel=1e-14)
    assert p.prem_gross_ann_pp(12) / p.prem_gross_ann_pp(0) == pytest.approx(
        1.03, rel=1e-14)
    # Flat within a policy year, stepping only at the policy anniversary.
    assert len({p.prem_gross_ann_pp(t) for t in range(12, 24)}) == 1
    assert p.dyn_factor(12) == pytest.approx(1.03, rel=1e-15)
    # On the level form the factor is one throughout, and beitragsdyn_rate is forced to 0.
    level = berufsunfaehigkeit.Projection[1]
    assert level.premium_form() == "level" and level.beitragsdyn_rate() == 0.0
    assert all(level.dyn_factor(t) == 1.0 for t in (0, 12, 443))


# The published identities -- delib ruling 1 and the six beside it
def test_every_published_check_closes_on_the_anchor_cell(de_bu_anchor):
    """Seven no-argument bools over all t, each with a per-t residual companion."""
    p = de_bu_anchor
    checks = ("check_net_cf", "check_states", "check_pols_roll_fwd",
              "check_dis_roll_fwd", "check_runoff_roll_fwd", "check_prem_split",
              "check_cover_end")
    for name in checks:
        value = getattr(p, name)()
        assert isinstance(value, bool), name
        assert value is True, name
        resid = getattr(p, name + "_resid")
        for t in (0, 1, 12, 200, 443):
            assert resid(t) == pytest.approx(0.0, abs=1e-9), (name, t)


def test_check_net_cf_crosses_the_brutto_zahl_split(de_bu_anchor):
    """delib's first ruling, and a reconciliation rather than a restatement: the premium leg
    is rebuilt from the *Zahlbeitrag* **actually billed** times the premium-paying count,
    not from ``premiums - surplus_credit``, so it crosses the *Brutto* / *Zahl* split and
    fails if the premium is weighted by ``pols_if``.
    """
    p = de_bu_anchor
    assert p.check_net_cf() is True
    for t in (0, 1, 60, 443):
        rebuilt = (p.prem_zahl_pp(t) * p.pols_prem(t)
                   - p.claims(t, "BU_RENTE") - p.claims(t, "REINTEGRATION")
                   - p.claims(t, "LAPSE") - p.expenses(t) - p.claim_expenses(t))
        assert p.net_cf(t) == pytest.approx(rebuilt, abs=1e-9)
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)
    # A pols_if-weighted premium leg would not reconcile anywhere a claim is running.
    bad = (p.prem_zahl_pp(240) * p.pols_if(240)
           - p.claims(240, "BU_RENTE") - p.claims(240, "REINTEGRATION")
           - p.expenses(240) - p.claim_expenses(240))
    assert abs(p.net_cf(240) - bad) > 0.5


def test_check_states_is_not_trivially_zero(de_bu_anchor):
    """``pols_if`` is built off the two exits, not as the sum of the three ledgers, which is
    what makes ``check_states`` a real test rather than a restatement of its own definition.
    """
    p = de_bu_anchor
    assert p.check_states() is True
    for t in (0, 3, 12, 240, 443, 444):
        assert p.pols_if(t) == pytest.approx(
            p.pols_actv(t) + p.pols_dis(t) + p.pols_runoff(t), abs=1e-12)
    # pols_if really is the roll-forward, which is the definition the check tests against.


# Structure, documentation and inputs
def test_result_cf_shape_and_both_signs_of_the_net_flow(de_bu_anchor):
    """The notes' fourteen columns, in order, with liability_cf the outgo orientation."""
    df = de_bu_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "pols_actv", "pols_dis", "pols_runoff", "pols_prem",
        "premiums", "surplus_credit", "claims_bu_rente", "claims_reintegration",
        "claims_lapse", "expenses", "claim_expenses", "liability_cf", "net_cf",
    ]
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    outgo = (df["surplus_credit"] + df["claims_bu_rente"] + df["claims_reintegration"]
             + df["claims_lapse"] + df["expenses"] + df["claim_expenses"])
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    # The shape: a large month-0 strain, thin positive margins, then a crossing to negative.
    assert df["net_cf"].iloc[0] == pytest.approx(-884.58, abs=CENT)
    assert (df["net_cf"].iloc[1:200] > 0).all()
    assert (df["net_cf"].iloc[266:] < 0).all()


def test_invalid_enum_values_raise(de_bu_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_bu_anchor.claims(1, "REINSTATEMENT")
    with pytest.raises(FormulaError):
        de_bu_anchor.pols_if_at(1, "AFT_DECR")


def test_the_annual_and_monthly_rate_pairs_follow_the_house_convention(de_bu_anchor):
    """``*_rate`` is annual, ``*_rate_mth`` monthly, and the monthly one is strictly below."""
    p = de_bu_anchor
    for t in (0, 12, 36, 120, 443):
        assert p.mort_rate_mth(t) < p.mort_rate(t)
        assert p.lapse_rate_mth(t) < p.lapse_rate(t)
        assert p.inc_rate_mth(t) < p.inc_rate(t)
    assert [p.lapse_rate(12 * (y - 1)) for y in range(1, 8)] == [
        0.040, 0.040, 0.035, 0.030, 0.025, 0.020, 0.020]


def test_docstrings_describe_the_current_structure(berufsunfaehigkeit):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = berufsunfaehigkeit.doc
    assert "Berufsunfaehigkeitsversicherung" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "Bruttobeitrag" in doc and "Zahlbeitrag" in doc
    assert "run-off" in doc
    proj = berufsunfaehigkeit.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "pols_prem", "pols_runoff_slot",
                  "rente_pay_pp", "prem_gross_level_pp", "runoff_val", "pols_if_at"):
        assert cells in proj, cells
    data = berufsunfaehigkeit.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "inception_table",
                  "claim_duration_table", "mortality_table"):
        assert cells in data, cells
    # The Data docstring states the three anchors a replacement table must preserve.
    assert "0.001100" in data and "0.000350" in data


def test_the_multi_state_vocabulary_is_present(berufsunfaehigkeit):
    """The multi-state chassis names must all be present and mean the chassis thing.

    The cohort-vector half (``pols_dis_dur``, ``rente_pay_pp``, ``pols_runoff_slot``,
    ``pols_recovery``) is shared with frlib's ``Dep_FR_S``; ``Pflege_DE_S`` shares the
    surrounding vocabulary (``pols_prem``, ``pols_if_at``, ``check_states``) but indexes
    its ledgers by *Pflegegrad* rather than by claim duration.
    """
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_actv", "pols_dis", "pols_dis_dur", "pols_runoff", "pols_runoff_slot",
        "pols_prem", "pols_inception", "pols_recovery", "pols_reactivation",
        "pols_death", "pols_lapse", "mort_rate", "mort_rate_mth", "mort_rate_dis",
        "lapse_rate", "lapse_rate_mth", "inc_rate", "inc_rate_base", "recov_rate",
        "rente_pay_pp", "runoff_val", "claims", "claim_expenses", "expenses",
        "premiums", "surplus_credit", "net_cf", "liability_cf", "result_cf",
        "check_net_cf", "check_net_cf_resid", "check_states",
    }
    names = set(berufsunfaehigkeit.Projection.cells) | set(
        berufsunfaehigkeit.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Seven CSVs beside run.py, and each says what it is -- especially what it is not.

    The three biometric tables are **[std]** proxies: DAV 1997 I / RI / TI and DAV 2008 T
    are cited by name and never shipped, and the anchors a substitute must preserve are
    ``inc_rate(30) = 0.001100``, ``mort_rate_actv(30) = 0.000350`` and the duration shape.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "inception_table.csv",
                "claim_duration_table.csv", "mortality_table.csv",
                "occupation_table.csv", "lapse_table.csv", "freq_loading_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir() if p.suffix == ".csv"}

    inc = pd.read_csv(MODEL_DIR.parent / "inception_table.csv", index_col="age")
    assert list(inc.index) == list(range(18, 67))
    assert all(p.startswith("[std]") and "[R16]" in p for p in inc["provenance"])
    assert "DAV 1997 I" in inc.loc[18, "provenance"]
    assert "anchor" in inc.loc[30, "provenance"]      # the row a replacement must match
    assert float(inc.loc[30, "inc_rate"]) == pytest.approx(0.001100, rel=1e-6)

    mort = pd.read_csv(MODEL_DIR.parent / "mortality_table.csv", index_col="age")
    assert list(mort.index) == list(range(18, 71))
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert float(mort.loc[30, "mort_rate_actv"]) == pytest.approx(0.000350, rel=1e-6)
    assert (mort["mort_rate_dis"] / mort["mort_rate_actv"] - 4.0).abs().max() < 1e-6

    dur = pd.read_csv(MODEL_DIR.parent / "claim_duration_table.csv", index_col="dur_year")
    assert list(dur.index) == list(range(1, 12))
    assert list(dur["recov_rate"]) == [0.250, 0.130, 0.070, 0.040, 0.025, 0.018,
                                       0.014, 0.011, 0.009, 0.008, 0.006]
    assert all("DAV 1997 RI / TI" in p for p in dur["provenance"])

    occ = pd.read_csv(MODEL_DIR.parent / "occupation_table.csv", index_col="berufsgruppe")
    assert list(occ.index) == ["BG1", "BG2", "BG3", "BG4", "BG5"]
    assert list(occ["occ_factor"]) == [1.00, 1.40, 2.10, 3.00, 4.50]

    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    assert list(lapse["lapse_rate"]) == [0.040, 0.040, 0.035, 0.030, 0.025, 0.020]

    freq = pd.read_csv(MODEL_DIR.parent / "freq_loading_table.csv", index_col="prem_mode")
    assert list(freq["freq_load"]) == [1.00, 1.02, 1.03, 1.05]

    # The model point table is the one file with no provenance column, by ruling.
    points = pd.read_csv(MODEL_DIR.parent / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns
    assert list(points.index) == list(range(1, 14))
    assert (points["au_uplift"] == 1.0).all()          # the AU-Klausel ships inert
    assert (points.loc[points["premium_form"] == "level", "beitragsdyn_rate"] == 0).all()


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a company or licensed DAV basis."""
    import pandas as pd

    lighter = pd.read_csv(MODEL_DIR.parent / "inception_table.csv", index_col="age")
    lighter["inc_rate"] = lighter["inc_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="BU_DE_S_swap")
    try:
        alt_name = "inception_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_bu_rente"].sum()
            model.Data.inception_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            after = model.Projection[1]
            # Half the incidence means far fewer claims and a much smaller premium.
            assert after.result_cf()["claims_bu_rente"].sum() < base
            assert after.prem_gross_level_pp() < 1013.0697368527
            assert after.check_net_cf() is True and after.check_states() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="BU_DE_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="BU_DE_S_rt")
    try:
        p = reread.Projection[1]
        assert p.prem_gross_level_pp() == pytest.approx(PREM_GROSS_ANN, abs=5e-8)
        for t, row in WORKED_EXAMPLE.items():
            assert p.premiums(t) == pytest.approx(row[4], abs=CENT)
            assert p.claims(t, "BU_RENTE") == pytest.approx(row[6], abs=CENT)
            assert p.net_cf(t) == pytest.approx(row[10], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_net_cf() is True
        assert p.check_states() is True
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
