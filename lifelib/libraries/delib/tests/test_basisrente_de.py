"""Golden and structural tests for Basis_DE_S, the German Basisrente (Rürup, Schicht 1).

The golden values are the worked example in
``products/basisrente/technical-notes.md`` ("Worked example"), which is a **configuration**
rather than a scenario.  Model point 1 is that cell: policy ``DE-BAS-0001``, a male aged 45 at
conclusion (``sex`` is reporting only -- pricing is unisex), concluded in **2026** with
``duration_init = 0``, *Rentenbeginn* at attained age **67**, one policy in force, a **regular**
*laufender Beitrag* of **6 000,00 EUR** a year paid **annually in advance** so the
*Ratenzahlungszuschlag* is 1,000, a **2 % *Beitragsdynamik***, an annual ***Zuzahlung*** of
**4 000,00 EUR** to policy duration 22, not paid-up at the valuation date, no opening account
value and no annuity in payment, a *Rechnungszins* of **1,00 %**, a **guaranteed *Rentenfaktor*
of 28,00 EUR** per month per 10 000 EUR, **no *Rentengarantiezeit*, no survivor's annuity and no
BUZ**, on tariff ``de_basis_std`` with the ``base`` behaviour, surplus and *Rentenfaktor*
scenarios.  Hence ``age(0) = 45``, ``ret_y() = 22`` and ``ret_t() = 264``,
``omega_age() = 121``, ``proj_len_y() = 77`` and ``proj_len() = 924``: twenty-two years of
*Aufschubphase*, fifty-five of *Rentenphase*.

**The model runs on two clocks and so do these goldens.**  ``t`` counts projection **months**
from the valuation date and ``k = t // 12`` projection **years**; a cells' argument says which
it is on.  The annual goldens below are keyed on ``k``, which is the annual-step model's own
``t``, and are read from ``result_cf_annual()`` -- the monthly frame summed into projection
years -- and from ``result_pols()``, the annual state.  Both are 0-based, so every golden is
keyed one index lower than the projection year a reader counting from one would name.

Because the projection is that long the notes print **eighteen selected rows** -- every year of
the first six, a five-yearly sample of the accumulation phase, the conversion year and its
neighbours, and a decade sample of the payout phase -- plus a **Total** row summed at full
precision and then rounded.  Every one of those rows is asserted here, cell by cell, with the
full-precision totals and the fact that adding the *rounded* cells instead gives a different
answer in four of the six money columns.  A second golden opens the first payout year **month
by month**, which is the view the annual grid could not give and the reason the model was moved
onto a monthly one.  The goldens are hard-coded rather than pickled so a
reviewer can compare them with the notes by eye, and the tolerances follow the precision the
notes display: money to the cent, the two policy counts to six decimals.

What this module asserts, beyond those rows:

* the notes' **three independent checks** -- the first year's account rebuilt from the charge
  scale up, the year-one decrement split rebuilt from the shipped mortality table, and the
  conversion rebuilt from the fund and the applied *Rentenfaktor* -- and the two **closure
  identities**, that the decrements sum to exactly one and that the Total row reconciles;
* the two documented **variant tables**: model point 5, the *Einmalbeitrag*, and model point 13,
  the cell on which the guaranteed *Rentenfaktor* binds instead of the current one;
* all six published ``check_*`` identities and their residuals -- three of which take a
  **month** and three a projection **year**, because the *Deckungskapital*, the conversion and
  the *Überschussrente* move once a *Versicherungsjahr* -- including ``check_net_cf()``, delib's
  first ruling, and the shape and sign of ``result_cf()``;
* **one test per numbered modeling pitfall** in the technical notes, named for the pitfall: no
  surrender value and none of the names that carry one (1); a *Beitragsfreistellung* absent from
  the in-force roll-forward (2); the two account blocks not averaged (3); an account charge that
  is not also an expense (4); the *Zillmerung* spread over five **contract** years (5); the
  declared rate as a ``max`` and not a sum (6); the premium stream keyed to the policy duration
  and stopping at *Rentenbeginn* (7); the *Ratenzahlungszuschlag* on the *laufender Beitrag*
  alone (8); no death benefit with the rider off (9), and with it on, only where an eligible
  survivor exists and never as a lump sum (10); the conversion invariant to ``mort_be_factor``
  (11); the annuity paid one instalment a month in advance, on the count in force at the start
  of each month (12); both branches of
  ``max(garantiert, aktuell)`` (13); the *Rentengarantiezeit* running from *Rentenbeginn* and
  never commuted (14); the generational basis (15); the guarantee vintage attaching at
  conclusion (16); and the BUZ as a premium share that reaches no cash flow (17).

The whole-model-point-table sweep is deliberately **not** here: ``test_model_conventions_de.py``
owns the single sweep, because a model point's first evaluation is the most expensive thing in
the run.  This module instantiates only the points the worked example and the pitfalls need.
"""
import pandas as pd
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if / pols_paying displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Basis_DE_S"][0]
INPUT_DIR = MODEL_DIR.parent

# The seven external CSVs, which live beside run.py and not inside the model folder.
INPUT_FILES = {
    "model_point_table.csv", "mort_table.csv", "surplus_table.csv",
    "rentenfaktor_table.csv", "charge_table.csv", "behaviour_table.csv",
    "option_table.csv",
}

# ---------------------------------------------------------------------------
# The notes' worked-example table, in full, on the ANNUAL clock: the monthly frame summed into
# projection years by result_cf_annual(), with av read from result_pols().
#
# k: (age, pols_if, pols_paying, av, premiums, zuzahlungen, claims_annuity, expenses,
#     commissions, net_cf).  claims_death and claims_survivor are 0.00 at every one of the
# 924 months on this cell -- the survivor rider is off and there is no
# Rentengarantiezeit -- and are asserted in the row test all the same.
#
# Every Aufschubphase figure here is the annual-step model's to the last bit, because twelve
# geometric monthly death rates compound back to the annual one exactly.  What moved when the
# grid did is the payout phase and the expenses, and ANNUAL_GRID_WAS below names both.
WORKED_EXAMPLE = {
    0:  (45, 1.000000, 1.000000,      0.00, 6000.00, 2800.00,    0.00, 309.96, 4094.85,  4395.19),
    1:  (46, 0.998560, 0.958618,   7366.75, 5866.74, 2684.13,    0.00,  60.77,  128.26,  8361.84),
    2:  (47, 0.997024, 0.918857,  14688.72, 5735.87, 2572.80,    0.00,  61.58,  124.63,  8122.46),
    3:  (48, 0.995385, 0.880653,  21968.46, 5607.33, 2465.83,    0.00,  62.40,  121.10,  7889.66),
    4:  (49, 0.993635, 0.843941,  29208.23, 5481.05, 2363.03,    0.00,  63.22,  117.66,  7663.20),
    5:  (50, 0.991769, 0.808662,  36410.00, 5356.97, 2749.45,    0.00,  64.05,  121.60,  7920.77),
    10: (55, 0.980403, 0.686467,  78013.70, 5020.79, 2333.99,    0.00,  68.18,  110.32,  7176.28),
    15: (60, 0.964766, 0.610615, 119589.52, 4930.84, 2198.21,    0.00,  72.24,  106.94,  6949.88),
    20: (65, 0.943366, 0.539704, 162771.09, 4811.83, 1942.94,    0.00,  76.04,  101.32,  6577.40),
    21: (66, 0.938235, 0.526033, 171114.15, 4783.75, 1893.72,    0.00,  76.75,  100.16,  6500.55),
    22: (67, 0.932780, 0.512516, 179426.24,    0.00,    0.00, 7033.50,  46.46,    0.00, -7079.96),
    23: (68, 0.926985, 0.509331,      0.00,    0.00,    0.00, 7058.31,  46.86,    0.00, -7105.16),
    32: (77, 0.856165, 0.470419,      0.00,    0.00,    0.00, 7111.92,  49.36,    0.00, -7161.28),
    42: (87, 0.724266, 0.397948,      0.00,    0.00,    0.00, 6610.57,  48.20,    0.00, -6658.77),
    52: (97, 0.521776, 0.286689,      0.00,    0.00,    0.00, 5205.94,  39.88,    0.00, -5245.82),
    62: (107, 0.272931, 0.149962,     0.00,    0.00,    0.00, 2945.81,  23.71,    0.00, -2969.52),
    72: (117, 0.074193, 0.040765,     0.00,    0.00,    0.00,  847.29,   7.16,    0.00,  -854.46),
    76: (121, 0.032209, 0.017697,     0.00,    0.00,    0.00,  416.84,   3.60,    0.00,  -420.43),
}

# The twelve months of the first payout year, t = 264 .. 275, straight off result_cf().  The
# instalment per annuitant is the same 630,16 EUR in each; what falls across the rows is the
# COUNT, which is the whole of what the monthly grid buys on this product.
# t: (pols_if, claims_annuity, expenses, net_cf)
MONTHS_FIRST_PAYOUT_YEAR = {
    264: (0.932780, 587.80, 3.88, -591.68),
    265: (0.932296, 587.50, 3.88, -591.38),
    266: (0.931812, 587.19, 3.88, -591.07),
    267: (0.931328, 586.89, 3.88, -590.76),
    268: (0.930845, 586.58, 3.87, -590.46),
    269: (0.930361, 586.28, 3.87, -590.15),
    270: (0.929878, 585.97, 3.87, -589.84),
    271: (0.929395, 585.67, 3.87, -589.54),
    272: (0.928913, 585.36, 3.87, -589.23),
    273: (0.928430, 585.06, 3.86, -588.92),
    274: (0.927948, 584.76, 3.86, -588.62),
    275: (0.927467, 584.45, 3.86, -588.31),
}
ANN_MTH_PP_CONV = 630.1594591876          # ann_pp(22) / 12, the instalment actually paid
ANNUAL_BOOKING_YEAR_22 = 7053.6043684572  # 12 x that x pols_if(264): what the annual grid paid

# The notes' Total row: summed over all 924 months at full precision, then rounded.
TOTALS = {
    "premiums": 113761.91, "zuzahlungen": 51236.28, "claims_death": 0.00,
    "claims_annuity": 265725.57, "claims_survivor": 0.00, "expenses": 3695.91,
    "commissions": 6437.82, "net_cf": -110861.12,
}

# What the annual-step model this replaced produced, for the two columns the finer grid moved.
# The difference is the whole point of the conversion and is asserted, not hidden: the annuity
# because a life that dies during a payout year is no longer paid the whole of it, the expenses
# because a mid-year leaver bears only the months it was there.
ANNUAL_GRID_WAS = {"claims_annuity": 270016.08, "expenses": 3731.36}
# And the three columns it did not move, which is the other half of the statement.
ANNUAL_GRID_UNCHANGED = {"premiums": 113761.91, "zuzahlungen": 51236.28,
                         "commissions": 6437.82}

# Adding the seventy-seven *rounded* annual cells instead gives a different answer in four
# columns.  The notes say so explicitly; this module asserts both numbers so the difference
# cannot be quietly "fixed" in either direction.
ROUNDED_CELL_SUMS = {
    "claims_annuity": 265725.58, "expenses": 3695.88, "commissions": 6437.83,
    "net_cf": -110861.14,
}

# The notes' three independent checks, at full precision.
S_ANCHOR = 163793.9012327640          # beitragssumme_pp(): 6 000 x (1.02^22 - 1) / 0.02
ALPHA_TOTAL_ANCHOR = 4094.8475308191  # 0.025 x S -- the same number as commissions(0)
ALPHA_INSTALMENT = 818.9695061638     # alpha_total / zill_spread_y
N_ANCHOR_T0 = 7215.0304938362         # prem_to_av_pp(0), the first projected year
AV_PP_AFT_INT_T0 = 7377.3686799475    # N(0) x (1 + 0.026 - 0.0035)
AV_ANCHOR_T1 = 7366.7479330812        # that, after the first year's death decrement
QX45_TABLE = 0.0023263433             # 0.014000 x 1.085^(45 - 67), the shipped table at 45
TREND_2005_TO_2026 = 0.7280493868     # (1 - 0.015)^21
Q_FIRST_ORDER_T0 = 0.0016936928       # mort_rate_base(0); mort_rate(0) is 0.85 x it
Q_BEST_ESTIMATE_T0 = 0.0014396389
Q_MTH_T0 = 0.0001200491               # 1 - (1 - q)^(1/12), the rate the recursion applies
FREEZE_T0 = POLS_PAIDUP_T1 = 0.0399424144
POLS_PAYING_T1 = 0.9586179467
FUND_PER_ANNUITANT = 200050.6219643070
ANN_PP_CONV = 7561.9135102508             # ann_pp at ret_y(), which is k = 22
ANN_PP_CONV_IF_GUARANTEE_BOUND = 6721.70  # what 28,00 EUR would have given

# The Einmalbeitrag variant -- model point 5, a 58-year-old paying 60 000,00 EUR once and
# deferring to 67.  t: (age, pols_if, av, premiums, claims_annuity, expenses, commissions,
# net_cf).
SINGLE_PREMIUM = {
    0:  (58, 1.000000,     0.00, 60000.00,    0.00, 309.89, 1500.00, 58190.11),
    1:  (59, 0.995842, 56170.68,     0.00,    0.00,  60.52,    0.00,   -60.52),
    2:  (60, 0.991418, 56838.16,     0.00,    0.00,  61.15,    0.00,   -61.15),
    4:  (62, 0.981702, 58157.41,     0.00,    0.00,  62.36,    0.00,   -62.36),
    8:  (66, 0.958317, 61584.00,     0.00,    0.00,  64.56,    0.00,   -64.56),
    9:  (67, 0.951537, 62484.63,     0.00, 2447.87,  39.03,    0.00, -2486.90),
    10: (68, 0.944341,     0.00,     0.00, 2453.07,  39.31,    0.00, -2492.37),
    19: (77, 0.857193,     0.00,     0.00, 2427.85,  40.67,    0.00, -2468.52),
    39: (97, 0.468265,     0.00,     0.00, 1587.41,  29.35,    0.00, -1616.77),
    63: (121, 0.014921,    0.00,     0.00,   65.92,   1.37,    0.00,   -67.29),
}

SINGLE_TOTALS = {
    "premiums": 60000.00, "zuzahlungen": 0.00, "claims_annuity": 84666.77,
    "expenses": 2292.11, "commissions": 1500.00, "net_cf": -28458.88,
}
SINGLE_NET_CF_ROUNDED_CELL_SUM = -28458.87   # one cent away from the full-precision total
N_SINGLE_T0 = 55164.0000000000               # 60 000 x 0.925 - 300 - 36
AV_PP_SINGLE_T1 = 56405.1900000000
AV_SINGLE_T1 = 56170.6811550510

# The notes' Rentenfaktor table: the anchor, where the current factor binds, and model point 13,
# where the guaranteed one does.  (ret_y, av(T), fund_at_conv, per annuitant, gtd, curr,
# applied, ann_pp(T), ann_mth_pp).
CONVERSION = {
    1:  (22, 179426.24, 186603.29, 200050.62, 28.00, 31.50, 31.50, 7561.91, 630.16),
    13: (21,  98185.81, 102113.25, 109428.02, 34.00, 27.72, 34.00, 4464.66, 372.06),
}
MP13_ANN_IF_CURRENT_BOUND = 3640.01   # 109 428,02 / 10 000 x 27,72 x 12
MP13_GUARANTEE_WORTH = 824.65         # 4 464,66 - 3 640,01, a year


def alt_model(name):
    """A private copy of the model, for tests that mutate a Reference or swap an input.

    The module-scoped ``basisrente`` fixture is shared, so mutating it would leak into every
    later test.  Each such test reads its own copy and closes it in a ``finally``.
    """
    return mx.read_model(MODEL_DIR, name=name)


# The worked example


@pytest.mark.parametrize("k", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_basis_anchor, k):
    """Every cell of the notes' eighteen printed rows, to the precision the notes display.

    The cash flows come from ``result_cf_annual()`` -- the monthly frame summed into projection
    years -- and the counts, the age and the *Deckungskapital* from ``result_pols()``, the
    annual state.  Both are indexed by ``k``, which is the annual-step model's own ``t``.
    """
    age, pols_if, pols_paying, av, prem, zuz, ann, exp, comm, net = WORKED_EXAMPLE[k]
    p = de_basis_anchor
    row = p.result_cf_annual().loc[k]
    state = p.result_pols().loc[k]
    assert p.age_y(k) == age == state["age"]
    assert p.age(12 * k) == age                     # the same age, read from a month
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_if(12 * k) == pytest.approx(pols_if, abs=SIX_DP)
    assert row["pols_paying"] == pytest.approx(pols_paying, abs=SIX_DP)
    assert p.av(k) == pytest.approx(av, abs=CENT) == state["av"]
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["zuzahlungen"] == pytest.approx(zuz, abs=CENT)
    assert row["claims_annuity"] == pytest.approx(ann, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["commissions"] == pytest.approx(comm, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)
    # The two columns the notes omit for space are structurally zero on this cell.
    assert row["claims_death"] == 0.0 and row["claims_survivor"] == 0.0
    assert row["liability_cf"] == pytest.approx(-net, abs=CENT)
    # The annual row is the twelve monthly rows and nothing else.
    months = p.result_cf().iloc[12 * k:12 * k + 12]
    assert months["net_cf"].sum() == pytest.approx(net, abs=CENT)
    assert months["premiums"].sum() == pytest.approx(prem, abs=CENT)
    # The whole year's contribution falls in its first month, whatever prem_mode says.
    assert p.premiums(12 * k) == pytest.approx(prem, abs=CENT)
    assert all(p.premiums(12 * k + m) == 0.0 for m in range(1, 12))


@pytest.mark.parametrize("t", sorted(MONTHS_FIRST_PAYOUT_YEAR))
def test_the_twelve_months_of_the_first_payout_year(de_basis_anchor, t):
    """The view the annual grid could not give: one instalment a month, on a falling count.

    Every instalment is the same 630,16 EUR per annuitant -- ``ann_pp(22) / 12`` -- so what
    falls across the twelve rows is the count in force at the start of each month.
    """
    pols_if, ann, exp, net = MONTHS_FIRST_PAYOUT_YEAR[t]
    p = de_basis_anchor
    assert p.proj_year(t) == 22 and p.age(t) == 67
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.ann_mth_pp(t) == pytest.approx(ANN_MTH_PP_CONV, abs=5e-6)
    assert p.ann_mth_pp(t) == pytest.approx(p.ann_pp(22) / 12.0, rel=1e-12)
    assert p.claims(t, "ANNUITY") == pytest.approx(ann, abs=CENT)
    assert p.claims(t, "ANNUITY") == pytest.approx(ANN_MTH_PP_CONV * pols_if, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.premiums(t) == 0.0 and p.commissions(t) == 0.0


def test_the_payout_year_is_below_the_annual_booking_it_replaced(de_basis_anchor):
    """Twelve instalments on twelve counts, not twelve on the opening one.

    The annual-step model booked the whole year at the start of the payout year, which paid a
    life that died in its first month for the whole of it.  The difference is 20,11 EUR in the
    first payout year and 4 290,52 EUR over the fifty-five.
    """
    p = de_basis_anchor
    df = p.result_cf()
    year = df["claims_annuity"].iloc[264:276].sum()
    assert year == pytest.approx(7033.4955825855, abs=CENT)
    assert ANNUAL_BOOKING_YEAR_22 == pytest.approx(
        12 * ANN_MTH_PP_CONV * p.pols_if(264), rel=1e-12)
    assert ANNUAL_BOOKING_YEAR_22 - year == pytest.approx(20.11, abs=CENT)
    assert year < ANNUAL_BOOKING_YEAR_22
    total = df["claims_annuity"].sum()
    # Both sides of these two are rounded to the cent, so the difference is good to two.
    assert ANNUAL_GRID_WAS["claims_annuity"] - total == pytest.approx(4290.52, abs=0.01)
    assert ANNUAL_GRID_WAS["expenses"] - df["expenses"].sum() == pytest.approx(35.45, abs=0.01)
    for column, unchanged in ANNUAL_GRID_UNCHANGED.items():
        assert df[column].sum() == pytest.approx(unchanged, abs=CENT), column


def test_the_worked_example_totals_are_summed_at_full_precision(de_basis_anchor):
    """The Total row is a full-precision sum over all 924 months, then rounded.

    Adding the *rounded* annual cells instead costs one to three cents in four of the six money
    columns, and the notes say so.  Asserting both numbers is what stops the difference being
    quietly "corrected" in either direction, and it is why a test that summed the printed cells
    would be asserting the wrong number.  The Total row also closes on itself, which is
    ``check_net_cf()`` evaluated over all 924 months at once.
    """
    p = de_basis_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert len(df) == 924 and len(ann) == 77
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
        assert ann[column].sum() == pytest.approx(df[column].sum(), abs=1e-9), column
    for column, rounded_sum in ROUNDED_CELL_SUMS.items():
        assert round(sum(round(v, 2) for v in ann[column]), 2) == pytest.approx(
            rounded_sum, abs=CENT), column
        assert abs(rounded_sum - TOTALS[column]) >= 0.01, column
    # premiums and zuzahlungen happen to agree at the cent, and the notes say that too.
    for column in ("premiums", "zuzahlungen"):
        assert round(sum(round(v, 2) for v in ann[column]), 2) == pytest.approx(
            TOTALS[column], abs=CENT), column
    total = (df["premiums"].sum() + df["zuzahlungen"].sum() - df["claims_death"].sum()
             - df["claims_annuity"].sum() - df["claims_survivor"].sum()
             - df["expenses"].sum() - df["commissions"].sum())
    assert total == pytest.approx(-110861.1186897786, abs=CENT)
    assert total == pytest.approx(df["net_cf"].sum(), rel=1e-12)


def test_check_1_the_first_year_account_rebuilt_from_the_charge_scale(de_basis_anchor):
    """The notes' first independent check: N(0) and the account, from the charge scale up.

    ``S = 6 000 x (1.02^22 - 1) / 0.02``; the *Zillmerung* is ``0.025 x S`` in five instalments;
    the *Zuzahlung* paid is ``4 000 x 0.70`` and carries its own 2,5 % charge rather than a share
    of the *Zillmerung*; the residue is credited at ``0.026 - 0.0035``.  The ``av`` the table
    prints at ``k = 1`` is that figure **after** the year's death decrement, at the **annual**
    rate -- which is exactly what the twelve monthly rates compound to.
    """
    p = de_basis_anchor
    assert p.beitragssumme_pp() == pytest.approx(S_ANCHOR, rel=1e-12)
    assert S_ANCHOR == pytest.approx(6000.00 * (1.02 ** 22 - 1) / 0.02, rel=1e-12)
    assert p.alpha_total_pp() == pytest.approx(ALPHA_TOTAL_ANCHOR, rel=1e-12)
    assert p.alpha_amort_pp(0) == pytest.approx(ALPHA_INSTALMENT, rel=1e-12)
    assert p.zuz_pp(0) == pytest.approx(4000.00 * 0.70, rel=1e-12)
    assert p.alpha_zuz_pp(0) == pytest.approx(0.025 * 2800.00, rel=1e-12)
    assert p.unit_cost_pp(0) == 36.00
    assert p.prem_to_av_pp(0) == pytest.approx(
        8140.00 - ALPHA_INSTALMENT - 70.00 - 36.00, rel=1e-12)
    assert p.prem_to_av_pp(0) == pytest.approx(N_ANCHOR_T0, rel=1e-12)
    assert p.cred_rate(0) == pytest.approx(0.026, rel=1e-12)
    assert p.av_pp_at(0, "AFT_INT") == pytest.approx(AV_PP_AFT_INT_T0, rel=1e-12)
    assert p.av_pp_at(0, "AFT_INT") == pytest.approx(
        N_ANCHOR_T0 * (1 + 0.026 - 0.0035), rel=1e-9)
    # The fund-level value the table publishes, one death decrement later.
    assert p.av(1) == pytest.approx(AV_ANCHOR_T1, rel=1e-12)
    assert p.av(1) == pytest.approx(AV_PP_AFT_INT_T0 * (1 - Q_BEST_ESTIMATE_T0), rel=1e-8)
    # 2,5 % of the Beitragssumme, twice: what the insurer pays out at inception is sized to
    # what it may write into the reserve.  One is an outgo and the other is only an account
    # deduction, which is why the commission is in net_cf and the instalment is not.
    assert p.commissions(0) == pytest.approx(ALPHA_TOTAL_ANCHOR, rel=1e-12)
    # The acquisition expense falls in month 0 with a twelfth of the year's maintenance beside
    # it; the year's expense is the acquisition plus twelve twelfths on a falling count.
    assert p.expenses(0) == pytest.approx(250.00 + 60.00 / 12.0, abs=CENT)
    assert p.result_cf_annual().loc[0, "expenses"] == pytest.approx(309.96, abs=CENT)
    assert p.commissions(12) == pytest.approx(
        0.015 * (p.premiums(12) + p.zuzahlungen(12)), rel=1e-12)
    assert all(p.commissions(t) == 0.0 for t in range(1, 12))


def test_check_2_the_year_one_decrement_split_and_the_rate_behind_it(de_basis_anchor):
    """The notes' second check: the shipped table's rate at 45, improved, and the split.

    The 4 % *Beitragsfreistellung* rate cancels out of ``pols_if`` entirely.
    """
    p = de_basis_anchor
    # The shipped CSV carries qx to ten decimals, so the closed form agrees to that and no
    # further: the table is the input and the formula behind it is documentation.
    assert p.mort_rate_at_age(45, 2005) == pytest.approx(QX45_TABLE, abs=5e-11)
    assert QX45_TABLE == pytest.approx(0.014000 * 1.085 ** (45 - 67), abs=5e-11)
    assert (1 - 0.015) ** 21 == pytest.approx(TREND_2005_TO_2026, abs=5e-10)
    assert p.cal_year_y(0) == 2026 and p.cal_year(11) == 2026
    assert p.mort_rate_base(0) == pytest.approx(Q_FIRST_ORDER_T0, abs=5e-10)
    assert p.mort_rate(0) == pytest.approx(Q_BEST_ESTIMATE_T0, abs=5e-10)
    assert p.mort_rate(0) == pytest.approx(0.85 * p.mort_rate_base(0), rel=1e-12)
    # The annual rate is flat across the year's twelve months and the recursion applies its
    # geometric twelfth, which compounds back to it exactly.
    assert all(p.mort_rate(t) == p.mort_rate(0) for t in range(12))
    assert p.mort_rate_mth(0) == pytest.approx(Q_MTH_T0, abs=5e-11)
    assert (1 - p.mort_rate_mth(0)) ** 12 == pytest.approx(
        1 - p.mort_rate(0), rel=1e-14)
    assert p.mort_rate_mth(0) > Q_BEST_ESTIMATE_T0 / 12.0
    assert sum(p.pols_death(t) for t in range(12)) == pytest.approx(
        Q_BEST_ESTIMATE_T0, abs=5e-10)
    assert p.bf_rate(0) == 0.04
    # The freeze falls once, in the year's last month, on the survivors of its deaths.
    assert all(p.pols_freeze(t) == 0.0 for t in range(11))
    assert p.pols_freeze(11) == pytest.approx(FREEZE_T0, abs=5e-10)
    assert p.pols_freeze(11) == pytest.approx((1 - Q_BEST_ESTIMATE_T0) * 0.04, rel=1e-8)
    assert p.pols_paying(12) == pytest.approx(POLS_PAYING_T1, abs=5e-10)
    assert p.pols_paidup(12) == pytest.approx(POLS_PAIDUP_T1, abs=5e-10)
    assert p.pols_if(12) == pytest.approx(POLS_PAYING_T1 + POLS_PAIDUP_T1, abs=5e-10)
    assert p.pols_if(12) == pytest.approx(1.0 - Q_BEST_ESTIMATE_T0, abs=5e-10)


def test_check_3_the_conversion_and_the_branch_of_the_max_that_binds(de_basis_anchor):
    """The notes' third check: the fund, the terminal bonus, the factor and the annuity."""
    p = de_basis_anchor
    assert p.ret_y() == 22 and p.ret_t() == 264
    assert p.av(22) == pytest.approx(179426.2405488701, abs=CENT)
    assert p.fund_at_conv() == pytest.approx(p.av(22) * 1.04, rel=1e-12)
    assert p.fund_at_conv() == pytest.approx(186603.2901708250, abs=CENT)
    per_annuitant = p.fund_at_conv() / p.pols_if(264)
    assert per_annuitant == pytest.approx(FUND_PER_ANNUITANT, abs=CENT)
    assert float(p.model_point()["rentenfaktor_gtd"]) == 28.00
    assert p.rentenfaktor_curr() == 31.50 and p.rf_option_factor() == 1.0
    assert p.rentenfaktor_applied() == pytest.approx(31.50, rel=1e-12)
    assert p.ann_pp(22) == pytest.approx(per_annuitant / 10000.0 * 378.00, rel=1e-9)
    assert p.ann_pp(22) == pytest.approx(ANN_PP_CONV, abs=5e-5)
    # And what is paid is a twelfth of it, once a month, to the lives in force that month.
    assert p.ann_mth_pp(264) == pytest.approx(ANN_MTH_PP_CONV, abs=5e-6)
    assert p.claims(264, "ANNUITY") == pytest.approx(
        ANN_MTH_PP_CONV * 0.9327803550, abs=CENT)
    ann = p.result_cf_annual()
    assert ann.loc[22, "claims_annuity"] == pytest.approx(7033.4955825855, abs=CENT)
    assert ann.loc[23, "claims_annuity"] == pytest.approx(7058.3052858204, abs=CENT)
    # The uplift compounds once a year and nowhere else.
    assert p.ann_pp(23) == pytest.approx(ANN_PP_CONV * 1.01, rel=1e-12)
    assert p.ann_mth_pp(276) == pytest.approx(p.ann_mth_pp(275) * 1.01, rel=1e-12)
    assert p.ann_mth_pp(275) == pytest.approx(p.ann_mth_pp(264), rel=1e-12)


def test_the_decrements_close_to_exactly_one(de_basis_anchor):
    """Deaths over the whole projection plus ``pols_if(proj_len())`` equal the policy.

    Not one policy leaves by any other route, and the 0,441765 of the cohort that went
    *beitragsfrei* is **inside** that 1,000000 rather than beside it.
    """
    p = de_basis_anchor
    n = p.proj_len()
    assert n == 924
    deaths = sum(p.pols_death(t) for t in range(n))
    assert p.pols_if(n) == pytest.approx(0.0, abs=1e-12)
    assert deaths + p.pols_if(n) == pytest.approx(p.pols_if_init(), abs=1e-10)
    assert sum(p.pols_freeze(t) for t in range(n)) == pytest.approx(
        0.4417651793, abs=5e-9)
    # The whole cohort dies in the terminal year's LAST month, not a twelfth in each of them.
    assert p.mort_rate(n - 1) == 1.0 and p.mort_rate_mth(n - 1) == 1.0
    assert all(p.mort_rate_mth(t) == 0.0 for t in range(n - 12, n - 1))
    assert p.claims(n - 1, "ANNUITY") > 0.0


# The published checks and the frame


def test_every_published_check_holds_and_its_residual_is_zero(de_basis_anchor):
    """All six identities, and their residuals at the periods that could break them.

    **The residual's argument follows its cells' clock.**  Three are statements about payments
    and take a **month**; three are statements about the *Deckungskapital*, the conversion and
    the *Überschussrente*, which move once a *Versicherungsjahr*, and take a projection **year**.
    """
    p = de_basis_anchor
    for check in ("check_net_cf", "check_pols_roll_fwd", "check_av_roll_fwd",
                  "check_conversion", "check_no_capital", "check_annuity_roll_fwd"):
        assert getattr(p, check)() is True, check
    for t in (0, 1, 11, 12, 263, 264, 275, 923):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-8)
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-10)
        assert p.check_no_capital_resid(t) == pytest.approx(0.0, abs=1e-9)
    for k in (0, 1, 4, 21, 22, 23, 76):
        assert p.check_av_roll_fwd_resid(k) == pytest.approx(0.0, abs=1e-6)
        assert p.check_conversion_resid(k) == pytest.approx(0.0, abs=1e-6)
        assert p.check_annuity_roll_fwd_resid(k) == pytest.approx(0.0, abs=1e-8)
    # delib ruling 1 in full: net_cf rebuilt from result_cf()'s own published columns.  The two
    # excluded columns are counts, and the Deckungskapital is not a column of this frame at all
    # -- it is a balance on the annual clock and lives in result_pols().
    df = p.result_cf()
    for t in (0, 120, 264, 588, 923):
        row = df.loc[t]
        assert float(row["premiums"] + row["zuzahlungen"] - row["claims_death"]
                     - row["claims_annuity"] - row["claims_survivor"] - row["expenses"]
                     - row["commissions"]) == pytest.approx(float(row["net_cf"]), rel=1e-12)
    assert "av" not in df.columns
    assert p.result_pols()["av"].sum() > 0.0


def test_result_cf_shape_and_both_signs_of_the_net_flow(de_basis_anchor):
    """Eleven monthly columns in the notes' order, ``pols_if`` first, contiguous over the frame.

    The *Deckungskapital* is **not** among them: it is a balance on the annual clock and lives in
    ``result_pols()``, beside the rates and per-policy amounts that move with it.  And the two
    accessors that take an enum raise on an unknown one rather than returning a
    zero, which on this product would be a claim kind that cannot exist.
    """
    p = de_basis_anchor
    df = p.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(p.proj_len()))
    assert df.index[0] == 0 and df.index[-1] == p.proj_len() - 1 == 923
    assert list(df.columns) == [
        "pols_if", "pols_paying", "premiums", "zuzahlungen", "claims_death",
        "claims_annuity", "claims_survivor", "expenses", "commissions", "net_cf",
        "liability_cf",
    ]
    assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12)
    assert not df.isna().any().any()
    # A cash flow statement must not publish its own subtotal beside its parts, and there is no
    # surrender column of any name.
    for absent in ("claims", "claims_lapse", "claims_surr", "claims_wd", "claims_commute",
                   "av"):
        assert absent not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    # The two annual frames beside it: the same stream summed into projection years, and the
    # annual state.
    ann, state = p.result_cf_annual(), p.result_pols()
    assert ann.index.name == "k" and list(ann.index) == list(range(p.proj_len_y()))
    assert list(ann.columns) == list(df.columns)
    assert state.index.name == "k" and len(state) == p.proj_len_y() == 77
    assert {"av", "av_pp", "mort_rate", "mort_rate_mth", "ann_pp", "ann_mth_pp",
            "policy_year"} <= set(state.columns)
    # The monthly saw-tooth: the year's whole contribution in its first month, a twelfth of the
    # maintenance expense in each of the other eleven and nothing else.
    assert df["net_cf"].iloc[0] == pytest.approx(4450.15, abs=CENT)
    assert df["net_cf"].iloc[1] == pytest.approx(-5.00, abs=CENT)
    prem_month = df["premiums"] > 0.0
    assert int(prem_month.sum()) == 22            # one a year, to Rentenbeginn
    assert (df.loc[prem_month, "net_cf"] > 0).all()
    assert (df.loc[~prem_month, "net_cf"] < 0).all()
    # The shape the notes print: a first-year strain that is all commission, then positive
    # accumulation-phase margin, then a payout tail that never turns.
    assert ann["net_cf"].iloc[0] == pytest.approx(4395.19, abs=CENT)
    assert (ann["net_cf"].iloc[1:22] > 0).all() and (ann["net_cf"].iloc[22:] < 0).all()
    # The enum accessors validate rather than propagating a typo into a lookup.  "SURRENDER" in
    # particular: there is no fourth kind of claim and there can be none, so asking for one is
    # an error and not a zero.
    for call in (lambda: p.claims(0, "SURRENDER"), lambda: p.claims(0, "LAPSE"),
                 lambda: p.pols_if_at(0, "AFTER_LAPSE"), lambda: p.av_pp_at(0, "AFT_SURR")):
        with pytest.raises(FormulaError):
            call()


# The variants the notes print


@pytest.mark.parametrize("k", sorted(SINGLE_PREMIUM))
def test_einmalbeitrag_variant_row(basisrente, k):
    """Model point 5, the *Einmalbeitrag*: the notes' ten printed rows, by projection year."""
    age, pols_if, av, prem, ann, exp, comm, net = SINGLE_PREMIUM[k]
    p = basisrente.Projection[5]
    row = p.result_cf_annual().loc[k]
    assert p.model_point()["prem_form"] == "single"
    assert p.age_y(k) == age
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(k) == pytest.approx(av, abs=CENT)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_annuity"] == pytest.approx(ann, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["commissions"] == pytest.approx(comm, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)
    assert row["zuzahlungen"] == 0.0
    assert row["claims_death"] == 0.0


def test_the_einmalbeitrag_totals_and_its_first_year_account(basisrente):
    """The single premium's own totals, and the two features that are the point of the variant.

    The *Beitragssumme* of a single-premium contract **is** the single premium, so the
    *Zillmerung* and the initial commission are an order of magnitude below the anchor's; and the
    five instalments still run, so from ``k = 1`` the account is debited by an acquisition charge
    the one premium has already come and gone without covering.
    """
    p = basisrente.Projection[5]
    df, ann = p.result_cf(), p.result_cf_annual()
    assert p.proj_len_y() == 64 and p.proj_len() == 768
    assert p.ret_y() == 9 and p.ret_t() == 108
    for column, total in SINGLE_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert round(sum(round(v, 2) for v in ann["net_cf"]), 2) == pytest.approx(
        SINGLE_NET_CF_ROUNDED_CELL_SUM, abs=CENT)
    assert p.beitragssumme_pp() == 60000.00
    assert p.alpha_total_pp() == pytest.approx(0.025 * 60000.00, rel=1e-12)
    assert p.commissions(0) == pytest.approx(p.alpha_total_pp(), rel=1e-12)
    assert [p.alpha_amort_pp(k) for k in range(5)] == [300.00] * 5
    assert p.alpha_amort_pp(5) == 0.0
    assert p.prem_to_av_pp(0) == pytest.approx(N_SINGLE_T0, rel=1e-12)
    assert p.av_pp(1) == pytest.approx(AV_PP_SINGLE_T1, rel=1e-12)
    assert p.av(1) == pytest.approx(AV_SINGLE_T1, rel=1e-12)
    # Every account balance is the annual-step model's; the single premium falls in month 0 and
    # nowhere else, whatever the mode.
    assert p.premiums(0) == 60000.00 and df["premiums"].iloc[1:].sum() == 0.0
    # No premium left to stop, so no Beitragsfreistellung and no premium-free block at all, and
    # a single payment carries no Ratenzahlungszuschlag.
    assert all(p.bf_rate(t) == 0.0 for t in (0, 11, 47, 100))
    assert all(p.pols_paidup(t) == 0.0 for t in (0, 48, 108))
    assert all(p.pols_freeze(t) == 0.0 for t in range(p.proj_len()))
    assert p.prem_freq_load() == 1.0


@pytest.mark.parametrize("point_id", sorted(CONVERSION))
def test_the_conversion_table_of_the_notes(basisrente, point_id):
    """The notes' *Rentenfaktor* table: the anchor and model point 13, both branches shipped."""
    ret_y, av_T, fund, per, gtd, curr, applied, ann, ann_mth = CONVERSION[point_id]
    p = basisrente.Projection[point_id]
    assert p.ret_y() == ret_y and p.ret_t() == 12 * ret_y
    assert p.av(ret_y) == pytest.approx(av_T, abs=CENT)
    assert p.fund_at_conv() == pytest.approx(fund, abs=CENT)
    assert p.fund_at_conv() / p.pols_if(p.ret_t()) == pytest.approx(per, abs=CENT)
    assert float(p.model_point()["rentenfaktor_gtd"]) == gtd
    assert p.rentenfaktor_curr() == pytest.approx(curr, abs=5e-5)
    assert p.rentenfaktor_applied() == pytest.approx(applied, abs=5e-5)
    assert p.rentenfaktor_applied() == max(gtd, curr) * p.rf_option_factor()
    assert p.ann_pp(ret_y) == pytest.approx(ann, abs=CENT)
    # The factor is quoted in euro a MONTH, and that is what is paid.
    assert p.ann_mth_pp(p.ret_t()) == pytest.approx(ann_mth, abs=CENT)
    assert p.ann_mth_pp(p.ret_t()) == pytest.approx(p.ann_pp(ret_y) / 12.0, rel=1e-12)
    # The printed per-annuitant figure is rounded to the cent, so the identity is closed on the
    # model's own full-precision fund rather than on the table's transcription of it.
    per_exact = p.fund_at_conv() / p.pols_if(p.ret_t())
    assert p.ann_pp(ret_y) == pytest.approx(per_exact / 10000.0 * applied * 12, rel=1e-12)
    # What the branch that did not bind would have given: 6 721,70 EUR on the anchor, where the
    # guarantee is worth nothing, and 3 640,01 EUR on model point 13, where it is worth 824,65.
    unused = min(gtd, curr)
    if point_id == 13:
        assert per_exact / 10000.0 * unused * 12 == pytest.approx(
            MP13_ANN_IF_CURRENT_BOUND, abs=CENT)
        assert p.ann_pp(ret_y) - per_exact / 10000.0 * unused * 12 == pytest.approx(
            MP13_GUARANTEE_WORTH, abs=CENT)
        assert p.model_point()["rf_scenario_id"] == "low"
    else:
        assert per_exact / 10000.0 * unused * 12 == pytest.approx(
            ANN_PP_CONV_IF_GUARANTEE_BOUND, abs=CENT)


# Pitfall 1 -- there is no surrender value, at any duration


def test_pitfall_1_no_surrender_value_and_none_of_the_names_that_carry_one(
        basisrente, de_basis_anchor):
    """*Nicht kapitalisierbar*: no *Rückkaufswert* exists at any duration, so no cells does.

    The absences cannot be asserted from inside the model -- a missing cells has no formula --
    so they are asserted here, against the exact names a modeller reusing the delib endowment or
    Schicht-3 chassis would carry across by habit.
    """
    names = set(basisrente.Projection.cells) | set(basisrente.Projection.refs)
    for absent in ("cv_pp", "cv", "surr_value_pp", "surr_rate", "surr_charge_rate",
                   "lapse_rate", "lapse_rate_mth", "lapse_rate_ann", "pols_lapse",
                   "loan_pp", "loan_bal", "withdrawals", "wd_free_pp", "paid_up_factor",
                   "asset_share", "mvr", "claims_surr", "claims_lapse",
                   "kapitalwahl", "commute_value_pp", "min_surr_value_pp"):
        assert absent not in names, absent
    p = de_basis_anchor
    assert p.check_no_capital() is True
    # The only three kinds of payment there are.
    for t in (0, 108, 264, 468, 923):
        assert p.check_no_capital_resid(t) == 0.0
        assert p.claims(t) == pytest.approx(
            p.claims(t, "DEATH") + p.claims(t, "ANNUITY") + p.claims(t, "SURVIVOR"),
            rel=1e-12)
    # The credit to the account is the raw arithmetic, with no floor of any kind under it.  On
    # model point 10 -- 300,00 EUR a year, the market's minimum recurring premium -- the charges
    # take a third of the first year's contribution before anything reaches the account.
    small = basisrente.Projection[10]
    assert small.prem_pp(0) == pytest.approx(300.00 * 1.05, abs=CENT)
    assert small.prem_to_av_pp(0) == pytest.approx(
        small.prem_pp(0) * (1 - 0.075) - small.alpha_amort_pp(0)
        - small.alpha_zuz_pp(0) - small.unit_cost_pp(0), rel=1e-12)
    assert small.prem_to_av_pp(0) == pytest.approx(199.88, abs=CENT)
    assert small.prem_to_av_pp(0) < 0.70 * small.prem_pp(0)
    # And it converts to a small annuity rather than a lump sum.  That is a property of this
    # model, not of German law: Schicht 1 does permit a Kleinbetragsrenten-Abfindung
    # (EStG s 10 Abs. 1 Nr. 2 Satz 3, on the s 93 Abs. 3 mechanics), and model.md records why
    # the base run leaves the commutation branch out.
    assert small.ann_pp(small.ret_y()) == pytest.approx(292.41, abs=CENT)
    assert small.ann_mth_pp(small.ret_t()) == pytest.approx(24.37, abs=CENT)
    assert small.check_no_capital() is True


def test_pitfall_1_the_account_is_never_floored_at_a_surrender_value():
    """Push the *Stückkosten* past the premium and the account goes negative, as it must.

    The mirror of the missing surrender column is a *Rückkaufswert* computed internally "for
    reference" and used as a floor under the *Deckungskapital*.  There is nothing for such a
    floor to protect here, and this proves there is none.
    """
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="tariff_id")
    charges.loc["de_basis_std", "unit_cost_pp"] = 400.00
    alt = INPUT_DIR / "charge_table_costly.csv"
    model = alt_model("Basis_DE_S_floor")
    try:
        assert model.Projection[10].prem_to_av_pp(0) > 0.0
        charges.to_csv(alt)
        try:
            model.Data.charge_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[10]
            assert p.unit_cost_pp(0) == 400.00
            assert p.prem_to_av_pp(0) < 0.0 and p.av_pp(1) < 0.0 and p.av(1) < 0.0
            assert p.check_av_roll_fwd() is True
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# Pitfall 2 -- a Beitragsfreistellung is not a lapse


def test_pitfall_2_a_beitragsfreistellung_removes_the_premium_not_the_policy(de_basis_anchor):
    """``pols_if(t+1) = pols_if(t) x (1 - mort_rate_mth(t))``, with ``bf_rate`` absent.

    The **monthly** rate, in every month; the freeze is annual and falls in the year's last one,
    § 165 VVG taking effect for the end of the current *Versicherungsperiode*.
    """
    p = de_basis_anchor
    for t in (0, 11, 47, 132, 263, 468, 911):
        assert p.pols_if(t + 1) == pytest.approx(
            p.pols_if(t) * (1 - p.mort_rate_mth(t)), rel=1e-12)
        assert p.pols_if_at(t, "AFT_FREEZE") == pytest.approx(
            p.pols_if_at(t, "AFT_DEATH"), rel=1e-12)
        assert p.pols_paying(t) + p.pols_paidup(t) == pytest.approx(p.pols_if(t), rel=1e-12)
    assert p.check_pols_roll_fwd() is True
    # The freeze falls once a year, in its last month, and nowhere else.
    assert all(p.pols_freeze(t) == 0.0 for t in range(264) if t % 12 != 11)
    assert all(p.pols_freeze(12 * k + 11) > 0.0 for k in range(22))
    assert all(p.pols_freeze(t) == 0.0 for t in range(264, p.proj_len()))
    # Across a whole year the paying ledger is the annual-step model's, exactly.
    for k in (0, 4, 11, 21):
        assert p.pols_paying(12 * (k + 1)) == pytest.approx(
            p.pols_paying(12 * k) * (1 - p.mort_rate(12 * k)) * (1 - p.bf_rate(12 * k)),
            rel=1e-12)
    # The freeze moves policies between the ledgers and nothing else: the paying count falls far
    # faster than the in-force count, and the difference is still in force.
    assert p.pols_paying(264) == pytest.approx(0.512516, abs=SIX_DP)
    assert p.pols_if(264) == pytest.approx(0.932780, abs=SIX_DP)
    assert p.pols_if(264) - p.pols_paying(264) == pytest.approx(0.420265, abs=SIX_DP)


def test_pitfall_2_with_bf_rate_at_zero_the_policy_count_is_unchanged():
    """Set ``bf_rate = 0`` and ``pols_if`` does not move, while ``premiums`` grows.

    That is the arithmetic statement of "not a lapse": a lapse rate that vanished would move the
    in-force count, and this one moves 45 635 EUR of premium income instead.
    """
    beh = pd.read_csv(INPUT_DIR / "behaviour_table.csv", index_col=["beh_table_id", "dur"])
    beh["bf_rate"] = 0.0
    alt = INPUT_DIR / "behaviour_table_nobf.csv"
    model = alt_model("Basis_DE_S_nobf")
    try:
        base = model.Projection[1].result_cf()
        beh.to_csv(alt)
        try:
            model.Data.behaviour_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[1]
            nobf = p.result_cf()
            assert (base["pols_if"] - nobf["pols_if"]).abs().max() < 1e-12
            assert all(p.bf_rate(t) == 0.0 for t in (0, 48, 132, 263))
            assert p.pols_paidup(264) == 0.0
            assert all(p.pols_freeze(t) == 0.0 for t in range(p.proj_len()))
            assert p.pols_paying(264) == pytest.approx(p.pols_if(264), rel=1e-12)
            assert p.check_pols_roll_fwd() is True and p.check_av_roll_fwd() is True
            prem_months = [12 * k for k in range(1, 22)]
            assert (nobf["premiums"] > base["premiums"]).loc[prem_months].all()
            assert nobf["premiums"].sum() == pytest.approx(159397.29, abs=CENT)
            assert p.ann_pp(22) == pytest.approx(10448.66, abs=CENT)
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# Pitfall 3 -- the two account blocks are not one average


def test_pitfall_3_the_paying_and_premium_free_blocks_are_not_averaged(de_basis_anchor):
    """They are equal at the first freeze and diverge from then on, permanently.

    ``av_pp_at`` is per **paying policy** and ``av_pu_at`` is the premium-free block at **fund**
    level; collapsing them loses the whole economic content of a *Beitragsfreistellung*.
    """
    p = de_basis_anchor
    # k = 1 is the first year with a premium-free block, and everyone in it froze together.
    assert p.av_pu_at(1, "BEF_PREM") / p.pols_paidup(12) == pytest.approx(
        p.av_pp(1), rel=1e-12)
    for k in (2, 4, 9, 14, 21):
        assert p.av_pp(k) > p.av_pu_at(k, "BEF_PREM") / p.pols_paidup(12 * k)
    assert p.av_pp(9) == pytest.approx(82934.50, abs=CENT)
    assert p.av_pu_at(9, "BEF_PREM") / p.pols_paidup(12 * 9) == pytest.approx(
        39549.19, abs=CENT)
    # The fund-level total is the only one that rolls forward on mortality alone, at the year's
    # ANNUAL rate -- which is what its twelve monthly rates compound to.
    for k in (1, 9, 21):
        assert p.av_at(k, "BEF_PREM") == pytest.approx(
            p.av_pp_at(k, "BEF_PREM") * p.pols_paying(12 * k) + p.av_pu_at(k, "BEF_PREM"),
            rel=1e-12)
        assert p.av_at(k + 1, "BEF_PREM") == pytest.approx(
            p.av_at(k, "AFT_INT") * (1 - p.mort_rate(12 * k)), rel=1e-12)
    assert p.check_av_roll_fwd() is True
    # A premium-free policy pays the Stueckkosten and the reserve charge and nothing else.
    assert p.av_pu_at(9, "AFT_PREM") == pytest.approx(
        p.av_pu_at(9, "BEF_PREM") - p.unit_cost_pp(9) * p.pols_paidup(12 * 9), rel=1e-12)


# Pitfall 4 -- a charge is not an expense


def test_pitfall_4_the_account_charges_are_income_and_never_an_expense():
    """``expenses`` is invariant to beta, gamma and the *Zillmersatz*; the annuity is not.

    Raise all three -- beta 7,5 % to 10 %, gamma 0,35 % to 0,60 %, the *Zillmersatz* 25 permille
    to 40 -- and not one euro of ``expenses`` or ``commissions`` moves.  What moves is the
    *Deckungskapital*, and through it the annuity: 245 916,54 EUR against 265 725,57 EUR.
    """
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="tariff_id")
    charges.loc["de_basis_std", "beta_prem"] = 0.10
    charges.loc["de_basis_std", "gamma_av"] = 0.006
    charges.loc["de_basis_std", "zill_rate"] = 0.040
    alt = INPUT_DIR / "charge_table_alt.csv"
    model = alt_model("Basis_DE_S_charges")
    try:
        base = model.Projection[1].result_cf()
        charges.to_csv(alt)
        try:
            model.Data.charge_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            loaded = model.Projection[1].result_cf()
            for column in ("expenses", "commissions", "premiums", "zuzahlungen", "pols_if"):
                assert (base[column] - loaded[column]).abs().max() == 0.0, column
            base_av = model.Projection[1].result_pols()["av"]
            assert (base_av - model.Projection[1].result_pols()["av"]).abs().max() == 0.0
            assert loaded["claims_annuity"].sum() == pytest.approx(245916.54, abs=CENT)
            assert loaded["claims_annuity"].sum() < base["claims_annuity"].sum()
            assert model.Projection[1].check_net_cf() is True
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# Pitfall 5 -- the Zillmerung is spread, and capped


def test_pitfall_5_the_zillmerung_is_five_equal_instalments_of_the_contract(basisrente,
                                                                           de_basis_anchor):
    """Equal at ``t = 0..4``, zero from ``t = 5``, summing to ``zill_rate x S`` exactly.

    The window belongs to the **contract**: model point 6, in force at ``duration_init = 17``,
    sees none of it at any ``t``.
    """
    p = de_basis_anchor
    instalments = [p.alpha_amort_pp(t) for t in range(5)]
    assert instalments == [pytest.approx(ALPHA_INSTALMENT, rel=1e-12)] * 5
    assert len(set(instalments)) == 1
    assert all(p.alpha_amort_pp(t) == 0.0 for t in (5, 11, 21))
    assert sum(p.alpha_amort_pp(t) for t in range(p.proj_len())) == pytest.approx(
        0.025 * p.beitragssumme_pp(), rel=1e-9)
    assert p.zill_spread_y == 5
    in_force = basisrente.Projection[6]
    assert in_force.duration(0) == 17
    assert all(in_force.alpha_amort_pp(t) == 0.0
               for t in range(in_force.proj_len()))
    # And the pre-2015 cohort carries the older 40 permille cap on its own tariff.
    assert in_force.model_point()["tariff_id"] == "de_basis_zill40"
    assert in_force.alpha_total_pp() == pytest.approx(
        0.040 * in_force.beitragssumme_pp(), rel=1e-12)


# Pitfall 6 -- the declared rate is a max, not a sum


def test_pitfall_6_the_credited_rate_is_a_maximum_and_not_a_sum(basisrente, de_basis_anchor):
    """A German *laufende Verzinsung* already includes the *Rechnungszins*.

    The anchor's 1,00 % sits below the whole declared path so the declared rate binds; model
    point 8's 2,75 % sits above it so the guarantee binds.  A sum would give 3,60 % in year one.
    """
    p = de_basis_anchor
    assert float(p.model_point()["gtd_rate"]) == 0.0100
    for t, decl in ((0, 0.026), (9, 0.026), (10, 0.024), (19, 0.024), (20, 0.022), (76, 0.022)):
        assert p.decl_rate(t) == pytest.approx(decl, rel=1e-12)
        assert p.cred_rate(t) == pytest.approx(decl, rel=1e-12)
        assert p.cred_rate(t) == max(0.0100, decl)
        assert p.cred_rate(t) != pytest.approx(0.0100 + decl, rel=1e-12)
    high = basisrente.Projection[8]
    assert float(high.model_point()["gtd_rate"]) == 0.0275
    for t in (0, 4, 29):
        assert high.cred_rate(t) == pytest.approx(0.0275, rel=1e-12)
        assert high.cred_rate(t) > high.decl_rate(t)


# Pitfall 7 -- the premium stream is keyed to the duration and stops at Rentenbeginn


def test_pitfall_7_premiums_and_zuzahlungen_stop_at_rentenbeginn(basisrente, de_basis_anchor):
    """Nothing is collected from ``k = ret_y()``, and the *Dynamik* runs off the duration."""
    p = de_basis_anchor
    for k in (22, 23, 39, 76):
        assert p.prem_pp(k) == 0.0 and p.zuz_pp(k) == 0.0
        assert p.prem_to_av_pp(k) == 0.0
    # On the monthly frame: nothing from ret_t(), and nothing in eleven months of twelve before.
    assert p.ret_t() == 264
    for t in (264, 265, 276, 468, 923):
        assert p.premiums(t) == 0.0 and p.zuzahlungen(t) == 0.0
        assert p.bf_rate(t) == 0.0 and p.pols_freeze(t) == 0.0
    assert all(p.premiums(t) == 0.0 for t in range(1, 12))
    assert p.premiums(0) > 0.0 and p.premiums(12) > 0.0
    # The Zuzahlung stops at zuzahlung_end_dur anyway, which is a policy duration and not a k.
    assert int(p.model_point()["zuzahlung_end_dur"]) == 22
    assert p.duration_y(21) == 21 and p.zuz_pp(21) > 0.0 and p.prem_pp(21) > 0.0
    # The Dynamik compounds on the policy duration, not on k.
    for k in (0, 4, 21):
        assert p.prem_base_pp(k) == pytest.approx(
            6000.00 * 1.02 ** p.duration_y(k), rel=1e-12)
    in_force = basisrente.Projection[6]
    assert in_force.duration_y(0) == 17 and in_force.duration(0) == 17
    assert in_force.prem_base_pp(0) == pytest.approx(3600.00 * 1.02 ** 17, rel=1e-12)
    assert 3600.00 < in_force.prem_base_pp(0) == pytest.approx(5040.87, abs=CENT)


# Pitfall 8 -- the Ratenzahlungszuschlag loads the laufender Beitrag alone


def test_pitfall_8_the_frequency_loading_is_applied_once_and_to_one_thing(basisrente,
                                                                         de_basis_anchor):
    """``prem_pp(t) / prem_base_pp(t) = phi`` exactly, and the *Zuzahlung* carries none."""
    p = de_basis_anchor
    assert p.model_point()["prem_mode"] == "annual"
    assert p.prem_freq_load() == 1.000
    for t in (0, 4, 21):
        assert p.prem_pp(t) / p.prem_base_pp(t) == pytest.approx(1.000, rel=1e-12)
    monthly = basisrente.Projection[2]
    assert monthly.prem_freq_load() == 1.050
    assert monthly.prem_pp(0) == pytest.approx(3000.00 * 1.05, abs=CENT)
    for t in (0, 4, 19):
        assert monthly.prem_pp(t) / monthly.prem_base_pp(t) == pytest.approx(1.050, rel=1e-12)
    quarterly = basisrente.Projection[3]
    assert quarterly.prem_freq_load() == 1.030
    assert quarterly.prem_pp(0) == pytest.approx(7200.00 * 1.03, abs=CENT)
    # The Zuzahlung is a single payment and carries no loading whatever the mode; nor does an
    # Einmalbeitrag.
    assert quarterly.zuz_pp(0) == pytest.approx(3000.00 * 0.70, rel=1e-12)
    assert basisrente.Projection[4].prem_freq_load() == 1.020
    assert basisrente.Projection[5].prem_freq_load() == 1.0


# Pitfall 9 -- death before Rentenbeginn pays nothing with the rider off


def test_pitfall_9_death_pays_nothing_with_the_survivor_rider_off(basisrente,
                                                                  de_basis_anchor):
    """*Nicht vererblich*: the reserve is released as a mortality profit and nothing is paid.

    The account still closes -- the released reserve leaves the fund either way.
    """
    p = de_basis_anchor
    assert float(p.model_point()["surv_annuity_rate"]) == 0.0
    assert all(p.claims(t, "DEATH") == 0.0 for t in range(77))
    assert p.result_cf()["claims_death"].sum() == 0.0
    assert p.pols_death(4) > 0.0 and p.db_pp(4) > 0.0   # the deaths and the reserve are real
    assert p.check_av_roll_fwd() is True and p.check_no_capital() is True
    # Every shipped point without the rider behaves the same way.
    for point_id in (2, 5, 9, 13):
        q = basisrente.Projection[point_id]
        assert float(q.model_point()["surv_annuity_rate"]) == 0.0
        assert q.result_cf()["claims_death"].sum() == 0.0


# Pitfall 10 -- with the rider on, only to an eligible survivor, and never a lump sum


def test_pitfall_10_the_death_benefit_is_conditional_and_buys_an_annuity(basisrente):
    """Model point 3: ``elig_surv_prob x mort_rate(t) x av_at(t, "AFT_INT")``, and nothing else.

    Not a lump sum to a beneficiary: what is booked is the *Deckungskapital* leaving as the
    single premium of a survivor's annuity, the cover being paid for through the *Rentenfaktor*.
    """
    p = basisrente.Projection[3]
    ann = p.result_cf_annual()
    assert float(p.model_point()["surv_annuity_rate"]) == 0.60
    assert p.elig_surv_prob == 0.55
    # The month decides WHEN the reserve is released; the amount is the annual one, struck at
    # the end of the Versicherungsjahr, so a year's deaths release the annual-step figure.
    for t in (0, 7, 48, 132, 227):
        k = p.proj_year(t)
        assert p.claims(t, "DEATH") == pytest.approx(
            0.55 * p.mort_rate_mth(t)
            * (p.db_pp(k) * p.pols_paying(t) + p.db_pu_pp(k) * p.pols_paidup(t)),
            rel=1e-12)
        assert p.db_pp(k) == p.av_pp_at(k, "AFT_INT")
    for k in (0, 4, 11, 18):
        assert ann.loc[k, "claims_death"] == pytest.approx(
            0.55 * p.mort_rate(12 * k) * p.av_at(k, "AFT_INT"), rel=1e-9)
    assert ann.loc[0, "claims_death"] == pytest.approx(8.16, abs=CENT)
    assert ann.loc[18, "claims_death"] == pytest.approx(556.79, abs=CENT)
    assert p.claims(0, "DEATH") == pytest.approx(0.68, abs=CENT)
    # It stops at Rentenbeginn: after that the annuity simply ends.
    assert p.ret_y() == 19 and p.ret_t() == 228
    assert all(p.claims(t, "DEATH") == 0.0 for t in (228, 240, 468))
    # The cover is bought out of the annuity.
    assert p.rf_option_factor() == pytest.approx(0.930, rel=1e-12)
    assert p.rentenfaktor_applied() == pytest.approx(31.50 * 0.930, rel=1e-12)
    assert p.check_no_capital() is True


def test_pitfall_10_with_no_eligible_survivor_nothing_is_paid():
    """``elig_surv_prob = 0`` removes the whole death benefit and moves no other column.

    The annuity stays reduced by the option factor, because a German tariff pays for the cover
    out of the annuity whether or not a survivor is found -- so this is not a rider-off run.
    """
    model = alt_model("Basis_DE_S_nosurv")
    try:
        base = model.Projection[3].result_cf()
        assert base["claims_death"].sum() == pytest.approx(3828.51, abs=CENT)
        model.Projection.elig_surv_prob = 0.0
        model.Projection.clear_all()
        nosurv = model.Projection[3].result_cf()
        assert nosurv["claims_death"].abs().max() == 0.0
        for column in ("pols_if", "pols_paying", "premiums", "zuzahlungen",
                       "claims_annuity", "claims_survivor", "expenses", "commissions"):
            assert (base[column] - nosurv[column]).abs().max() == pytest.approx(
                0.0, abs=1e-9), column
        assert (base["net_cf"] - nosurv["net_cf"]).abs().max() > 1.0
        assert model.Projection[3].rentenfaktor_applied() == pytest.approx(
            31.50 * 0.930, rel=1e-12)
    finally:
        model.close()


# Pitfall 11 -- the conversion is struck on the contractual basis


def test_pitfall_11_the_conversion_is_invariant_to_the_best_estimate_mortality():
    """``ann_pp(ret_t())`` does not move with ``mort_be_factor``; ``claims_annuity`` does.

    The wedge between the contractual first-order basis and the projection's best estimate is
    the payout phase's *Risikoüberschuss*; converting on its own mortality would abolish it.
    """
    model = alt_model("Basis_DE_S_mort")
    try:
        base_ann = model.Projection[1].ann_pp(22)
        base_claims = model.Projection[1].result_cf()["claims_annuity"].sum()
        assert base_ann == pytest.approx(ANN_PP_CONV, abs=5e-5)
        model.Projection.mort_be_factor = 0.70
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.mort_be_factor == 0.70
        assert p.ann_pp(22) == pytest.approx(base_ann, rel=1e-12)
        assert p.rentenfaktor_applied() == pytest.approx(31.50, rel=1e-12)
        lighter = p.result_cf()["claims_annuity"].sum()
        assert lighter == pytest.approx(292090.33, abs=CENT) and lighter > base_claims
        assert p.check_conversion() is True and p.check_pols_roll_fwd() is True
    finally:
        model.close()


# Pitfall 12 -- the annuity is booked in advance on the opening count


def test_pitfall_12_the_annuity_is_one_instalment_a_month_on_the_months_own_count(
        de_basis_anchor):
    """``claims_annuity(t) = ann_mth_pp(t) x pols_if(t)`` exactly, in every payout month.

    The annual-step model booked twelve instalments together at the start of the payout year on
    that year's opening count, so a life that died in its first month was paid for the whole of
    it -- a stated approximation of a monthly grid on an annual one.  Here the instalment is
    paid to whoever is alive at the start of each month, and the approximation is gone.
    """
    p = de_basis_anchor
    assert p.ann_freq == 12 and p.rf_unit == 10000.0
    for t in (264, 270, 275, 276, 468, 923):
        assert p.claims(t, "ANNUITY") == pytest.approx(
            p.ann_mth_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.ann_mth_pp(t) == pytest.approx(p.ann_pp(p.proj_year(t)) / 12.0, rel=1e-12)
    # Not twelve of them on the year's opening count, which is what the annual grid did.
    year = p.result_cf_annual().loc[22, "claims_annuity"]
    assert year < 12 * p.ann_mth_pp(264) * p.pols_if(264)
    # Nothing before Rentenbeginn, and afterwards the annuity compounds at the
    # Ueberschussrente once a year and nothing else touches it.
    assert all(p.ann_mth_pp(t) == 0.0 and p.claims(t, "ANNUITY") == 0.0
               for t in (0, 108, 263))
    assert all(p.ann_pp(k) == 0.0 for k in (0, 9, 21))
    for k in (23, 39, 76):
        assert p.ann_pp(k) == pytest.approx(
            p.ann_pp(k - 1) * (1 + p.ann_bonus_rate(k - 1)), rel=1e-12)
        assert all(p.ann_mth_pp(12 * k + m) == pytest.approx(p.ann_pp(k) / 12.0, rel=1e-12)
                   for m in range(12))
    assert p.ann_bonus_rate(29) == 0.01 and p.check_annuity_roll_fwd() is True


# Pitfall 13 -- max(garantiert, aktuell), both branches


def test_pitfall_13_the_higher_of_the_two_rentenfaktoren_applies(basisrente,
                                                                de_basis_anchor):
    """The anchor converts at the current factor, model points 6 and 13 at the guaranteed one."""
    p = de_basis_anchor
    assert p.rentenfaktor_applied() == pytest.approx(31.50, rel=1e-12)
    assert p.rentenfaktor_curr() > float(p.model_point()["rentenfaktor_gtd"])
    for point_id, gtd, curr in ((6, 26.00, 24.76), (13, 34.00, 27.72)):
        q = basisrente.Projection[point_id]
        assert float(q.model_point()["rentenfaktor_gtd"]) == gtd
        assert q.rentenfaktor_curr() == pytest.approx(curr, abs=5e-5)
        assert q.rentenfaktor_applied() == pytest.approx(gtd * q.rf_option_factor(), rel=1e-12)
        assert q.rentenfaktor_applied() > curr
    # The higher factor is taken and the other is not consulted at all -- a discontinuity, not
    # a blend.
    for point_id in (1, 6, 13):
        q = basisrente.Projection[point_id]
        assert q.rentenfaktor_applied() == pytest.approx(
            max(float(q.model_point()["rentenfaktor_gtd"]), q.rentenfaktor_curr())
            * q.rf_option_factor(), rel=1e-12)


# Pitfall 14 -- the Rentengarantiezeit runs from Rentenbeginn and is never commuted


def test_pitfall_14_the_guarantee_period_runs_from_rentenbeginn(basisrente):
    """Model point 4: ten years from ``ret_t()``, closing at ``gtd_end_t()``, whatever the death.

    Each death contributes ``elig_surv_prob`` of a continuation, the ledger is monotone inside
    the window and zero outside it, and the stream is never discounted into a capital sum.
    """
    p = basisrente.Projection[4]
    assert int(p.model_point()["guarantee_period_y"]) == 10
    assert p.ret_y() == 15 and p.ret_t() == 180
    # Ten years is 120 monthly INSTALMENTS, and a continuation starts in the month after the
    # death that triggered it rather than in the following year.
    assert p.gtd_end_t() == 180 + 120 - 1 == 299
    assert p.pols_gtd(180) == 0.0
    assert p.pols_gtd(181) == pytest.approx(p.pols_death(180) * p.elig_surv_prob, rel=1e-12)
    inside = [p.pols_gtd(t) for t in range(181, 300)]
    assert all(b >= a for a, b in zip(inside, inside[1:])) and p.pols_gtd(299) > 0.0
    assert all(p.pols_gtd(t) == 0.0 for t in range(300, p.proj_len()))
    # The continuation is a stream of instalments, weighted by the same annuity, never commuted.
    for t in (181, 240, 299):
        assert p.claims(t, "SURVIVOR") == pytest.approx(
            p.ann_mth_pp(t) * p.pols_gtd(t), rel=1e-12)
    assert p.claims(300, "SURVIVOR") == 0.0
    assert p.rf_option_factor() == pytest.approx(0.995, rel=1e-12)
    # Both options together on model point 12: twenty years, and a survivor's annuity.
    both = basisrente.Projection[12]
    assert int(both.model_point()["guarantee_period_y"]) == 20
    assert both.gtd_end_t() == both.ret_t() + 12 * 20 - 1 == 419
    assert both.rf_option_factor() == pytest.approx(0.974 * 0.930, rel=1e-12)
    assert all(both.pols_gtd(t) == 0.0 for t in range(420, both.proj_len()))


# Pitfall 15 -- the mortality basis is generational


def test_pitfall_15_the_basis_is_generational_and_not_a_period_table(basisrente,
                                                                    de_basis_anchor):
    """The improvement lives inside the table, so a calendar year changes the rate at an age."""
    p = de_basis_anchor
    for age in (45, 60, 67, 90):
        assert (p.mort_rate_at_age(age, 2050) < p.mort_rate_at_age(age, 2026)
                < p.mort_rate_at_age(age, 2005))
        assert p.mort_rate_at_age(age, 2026) == pytest.approx(
            p.mort_rate_at_age(age, 2005) * (1 - 0.015) ** 21, rel=1e-9)
    assert p.mort_rate_at_age(67, 2005) == pytest.approx(0.014000, rel=1e-12)
    assert p.mort_rate_at_age(67, 2026) == pytest.approx(0.01019269, abs=5e-9)
    # Two model points reaching the same attained age in different calendar years.
    older = basisrente.Projection[6]      # concluded 2009, reaches age 60 in 2029
    newer = basisrente.Projection[9]      # concluded 2026, reaches age 60 in 2036
    assert older.age_y(3) == 60 and older.cal_year_y(3) == 2029
    assert newer.age_y(10) == 60 and newer.cal_year_y(10) == 2036
    # The age and the calendar year step on the ANNIVERSARY, so every month of a projection
    # year sees the same generational rate.
    assert all(older.age(t) == 60 and older.cal_year(t) == 2029 for t in range(36, 48))
    assert older.mort_rate(36) == pytest.approx(0.00467744, abs=5e-9)
    assert newer.mort_rate(120) == pytest.approx(0.00420787, abs=5e-9)
    assert newer.mort_rate(120) < older.mort_rate(36)
    # The terminal age is absorbing whatever the trend and whatever mort_be_factor says, and
    # the certainty falls in the terminal year's LAST month.
    assert p.omega_age() == 121 and p.age_y(76) == 121 and p.mort_rate(12 * 76) == 1.0
    assert p.mort_rate(12 * 75) == pytest.approx(0.19920354, abs=5e-9)
    assert p.mort_rate_at_age(121, 2101) < 1.0     # the table's own rate, before the rule
    assert p.mort_rate_mth(923) == 1.0 and p.mort_rate_mth(922) == 0.0
    assert p.pols_if(924) == 0.0


# Pitfall 16 -- the guarantee vintage attaches at conclusion


def test_pitfall_16_the_rechnungszins_attaches_at_conclusion_and_stays(basisrente):
    """Four distinct vintages ship, and each in-force point carries its own, not today's."""
    table = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert set(table["gtd_rate"]) == {0.0100, 0.0175, 0.0225, 0.0275}
    for point_id, year, gtd in ((1, 2026, 0.0100), (6, 2009, 0.0225),
                                (7, 2014, 0.0175), (8, 2006, 0.0275)):
        assert table.loc[point_id, "conclusion_year"] == year
        assert table.loc[point_id, "gtd_rate"] == gtd
    for point_id in (1, 6, 7, 8, 13):
        p = basisrente.Projection[point_id]
        gtd = float(p.model_point()["gtd_rate"])
        for k in (0, 1, min(4, p.proj_len_y() - 1)):
            assert p.cred_rate(k) == max(gtd, p.decl_rate(k)) >= gtd
    # The other two in-force shapes: already beitragsfrei, and already in payment.
    paid_up = basisrente.Projection[7]
    assert int(paid_up.model_point()["paidup_at_init"]) == 1
    assert paid_up.pols_paying(0) == 0.0
    assert paid_up.pols_paidup(0) == pytest.approx(paid_up.pols_if_init(), rel=1e-12)
    assert paid_up.av(0) == pytest.approx(42000.00, abs=CENT)
    assert paid_up.prem_pp(0) == 0.0 and paid_up.zuz_pp(0) == 0.0
    assert paid_up.commissions(0) == 0.0        # the acquisition cost fell before the valuation
    # A twelfth of the annual maintenance expense in the month, twelve of them in the year.
    assert paid_up.expenses(0) == pytest.approx(60.00 / 12.0, abs=CENT)
    assert paid_up.result_cf_annual().loc[0, "expenses"] == pytest.approx(59.94, abs=CENT)
    in_payment = basisrente.Projection[8]
    assert in_payment.ret_y() == -3 and in_payment.ret_t() == -36
    assert in_payment.ann_pp(0) == pytest.approx(7200.00, abs=CENT)
    assert in_payment.ann_mth_pp(0) == pytest.approx(600.00, abs=CENT)
    assert in_payment.claims(0, "ANNUITY") == pytest.approx(600.00, abs=CENT)
    assert in_payment.result_cf_annual().loc[0, "claims_annuity"] == pytest.approx(
        7168.93, abs=CENT)
    assert in_payment.fund_at_conv() == 0.0 and in_payment.rentenfaktor_curr() == 0.0
    assert in_payment.av(0) == 0.0
    assert in_payment.check_conversion() is True             # vacuously: no conversion occurs
    assert all(in_payment.check_conversion_resid(k) == 0.0 for k in (0, 1, 9))


# Pitfall 17 -- the BUZ is a premium share and reaches no cash flow


def test_pitfall_17_the_buz_is_a_premium_share_that_enters_nothing(basisrente,
                                                                   de_basis_anchor):
    """``buz_prem_share < 0.50`` on every shipped point, and ``prem_total_pp`` is inert.

    ``prem_base_pp`` is the **old-age** contribution; the BUZ premium buys a cover this model
    does not project.  The 50 % rule is the one thing about the rider this model owns.
    """
    table = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert (table["buz_prem_share"] < 0.50).all()
    assert table["buz_prem_share"].max() == 0.49              # model point 11, the boundary
    boundary = basisrente.Projection[11]
    assert float(boundary.model_point()["buz_prem_share"]) == 0.49
    assert boundary.prem_total_pp(0) == pytest.approx(
        (boundary.prem_pp(0) + boundary.zuz_pp(0)) / 0.51, rel=1e-12)
    assert boundary.prem_total_pp(0) == pytest.approx(9329.41, abs=CENT)
    assert boundary.prem_total_pp(0) > boundary.prem_pp(0) + boundary.zuz_pp(0)
    assert "prem_total_pp" not in boundary.result_cf().columns   # and in no cash flow
    assert boundary.net_cf(0) == pytest.approx(
        boundary.premiums(0) + boundary.zuzahlungen(0)
        - boundary.claims(0, "DEATH") - boundary.claims(0, "ANNUITY")
        - boundary.claims(0, "SURVIVOR") - boundary.expenses(0)
        - boundary.commissions(0), rel=1e-12)
    # With no BUZ the reporting cells is the contribution itself.
    p = de_basis_anchor
    assert float(p.model_point()["buz_prem_share"]) == 0.0
    assert p.prem_total_pp(0) == pytest.approx(p.prem_pp(0) + p.zuz_pp(0), rel=1e-12)


# Structure, documentation and inputs


def test_docstrings_describe_the_current_structure(basisrente):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = basisrente.doc
    for phrase in ("Basisrente", "mechanics demonstration", "external", "once per model",
                   "Beitragsfreistellung", "Rentenfaktor", "nicht kapitalisierbar",
                   "Data", "Projection"):
        assert phrase in doc, phrase
    proj = basisrente.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "ret_t", "bf_rate", "av_pu_at",
                  "rentenfaktor_applied", "prem_total_pp", "pols_gtd"):
        assert cells in proj, cells
    data = basisrente.Data.doc
    assert "TradLife_A" in data
    assert "0.014000" in data                      # the anchor a replacement must preserve
    for cells in ("input_dir", "model_point_table", "mort_table", "behaviour_table"):
        assert cells in data, cells


def test_the_shipped_tables_mark_their_own_provenance():
    """Seven CSVs beside run.py, six of them tagged row by row -- delib's second ruling.

    The mortality table is a **[std]** proxy: DAV 2004 R is cited and never shipped, and the
    anchor a substitute must preserve is ``qx(67) = 0.014000``.
    """
    found = {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"}
    assert found == INPUT_FILES
    for name in INPUT_FILES - {"model_point_table.csv"}:
        frame = pd.read_csv(INPUT_DIR / name)
        assert "provenance" in frame.columns, name
        assert frame["provenance"].notna().all(), name
        assert (frame["provenance"].str.len() > 0).all(), name
    # A model point is a configuration, not an assumption: the one exemption.
    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns and len(points) == 13
    mort = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col="age")  # a [std] proxy
    assert list(mort.index) == list(range(20, 122))
    assert float(mort.loc[67, "qx"]) == 0.014000        # the anchor of the worked example
    assert float(mort.loc[121, "qx"]) == 1.0 and mort["qx"].max() <= 1.0
    assert (mort["trend"] == 0.015).all()
    assert float(mort.loc[68, "qx"]) / float(mort.loc[67, "qx"]) == pytest.approx(
        1.085, rel=1e-6)
    assert all(t.startswith("[std]") and "DAV 2004 R" in t for t in mort["provenance"])
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="tariff_id")
    assert set(charges.index) == {"de_basis_std", "de_basis_zill40"}
    assert float(charges.loc["de_basis_std", "zill_rate"]) == 0.025
    assert float(charges.loc["de_basis_zill40", "zill_rate"]) == 0.040
    assert all("Hoechstzillmersatz" in t for t in charges["provenance"])
    surplus = pd.read_csv(INPUT_DIR / "surplus_table.csv",
                          index_col=["scenario_id", "t"])
    # surplus_table.csv is keyed on the projection index t itself, so it is 0-based like the
    # frame: 2,60 % at t = 0..9, 2,40 % at t = 10..19, 2,20 % thereafter.
    assert list(surplus.loc["base"].index) == list(range(95))
    assert [float(surplus.loc[("base", t), "decl_rate"]) for t in (0, 9, 10, 19, 20, 94)] == [
        0.0260, 0.0260, 0.0240, 0.0240, 0.0220, 0.0220]
    assert all(float(surplus.loc[("base", t), "ann_bonus_rate"]) == 0.0100
               for t in (0, 20, 94))
    # behaviour_table.csv's dur is the contractual policy year, duration(t) + 1, so it stays
    # 1-based: it is not the frame's t.
    behaviour = pd.read_csv(INPUT_DIR / "behaviour_table.csv",
                            index_col=["beh_table_id", "dur"])
    assert [float(behaviour.loc[("base", d), "bf_rate"]) for d in (1, 6, 11)] == [
        0.0400, 0.0300, 0.0200]
    assert float(behaviour.loc[("base", 1), "zuz_take_up"]) == 0.7000
    assert all("no German insurer publishes" in t for t in behaviour["provenance"])
    factors = pd.read_csv(INPUT_DIR / "option_table.csv",
                          index_col=["option_id", "option_key"])
    assert float(factors.loc[("prem_mode", "annual"), "factor"]) == 1.000
    assert float(factors.loc[("prem_mode", "monthly"), "factor"]) == 1.050
    assert float(factors.loc[("survivor", "0.60"), "factor"]) == 0.930
    assert float(factors.loc[("guarantee_period", "20"), "factor"]) == 0.974
