"""Golden and structural tests for RLV_DE_S, the German Risikolebensversicherung.

The golden values are the worked example in
``products/risikolebensversicherung/technical-notes.md`` ("Worked example"), which is a
**configuration** rather than a scenario.  Model point 1 is that cell: a participating
individual *Risikolebensversicherung* on a male aged 35 at entry, non-smoker, with a
*konstante Versicherungssumme* of 300 000 EUR, a *Versicherungsdauer* and a
*Beitragszahlungsdauer* of 25 years each, a level *Bruttobeitrag* payable *jaehrlich* (so
the *Ratenzahlungszuschlag* is 1.000), the *Ueberschussbeteiligung* applied as
*Beitragsverrechnung*, no *Nachversicherungsgarantie*, one life, a *Risikozuschlag* of
1.00 and ``duration_y = 0``.  Cover runs to attained age 60, ``t0 = 0``,
``proj_len() = 300`` months, and the notes' annual table is the **entire** projection
rather than a slice of one -- so every row of it is asserted here, not three of them.

**The frame counts policy months, and the worked example is two tables.**  ``t = 0`` is
the first policy *month*, ``proj_len() = 12 x policy_term`` is the frame's *exclusive* end,
so ``result_cf()`` runs ``t = proj_start() .. proj_len() - 1`` and an in-force point opens
at ``t = 12 x duration_y``.  :data:`WORKED_EXAMPLE` is the notes' annual table, asserted
against ``result_cf_annual()`` and keyed on the contractual **1-based** ``policy_year``;
:data:`MONTHS_YEAR_1` is the twelve months of policy year 1 on the monthly frame, keyed on
``t``.  The three schedule CSVs stay keyed on the 1-based ``policy_year``, so the CSV
assertions near the bottom of the module are unmoved.

The goldens are hard-coded rather than pickled so that a reviewer can compare them against
the notes by eye.  Tolerances follow the precision the notes display: money to the cent,
``pols_if`` to six decimals, and the **totals at full precision** -- 12 243,75 EUR of
billed premium that way against 12 243,73 EUR if the twenty-five rounded cells are added.

What the monthly grid moved, and what it did not, is asserted rather than described:
``G``, ``Gn``, ``v_d`` and the first-order *Deckungskapital* are annual constructions and
are **bit-identical** to the annual-step model's, while the cash flows are not and are not
meant to be -- claims fall in the month of claim, maintenance accrues a twelfth a month on
that month's in-force, and a fractionated *Zahlbeitrag* is collected in instalments on a
block that has already lost lives.  ``pols_if`` at every anniversary is unchanged, which
is what the two grids share and what makes them comparable at all.

What this module asserts, beyond the worked example's rows and totals:

* the pricing engine -- ``G = 1 275,411882`` from the closed form and again from the
  equivalence it solves, and ``v_d = 0,42527476`` from its definition and again from the
  one-line identity that never forms ``G`` at all;
* the notes' three independent rebuilds -- the first period ``t = 0`` from the table rate
  up, the third period ``t = 2`` through two decrement steps, the expense line component by
  component -- and its three closure identities: the decrements summing to one, the
  paragraph 161 wedge being the only thing between claim events and claim amounts, and the
  cash flow statement itself;
* the first-order *Deckungskapital*: zero at policy year 0 by the equivalence, zero at
  policy year ``n`` by exhaustion, a peak of 7 553,29 EUR at policy year 15, and the
  Thiele step -- all on policy-year arguments, the reserve being an annual construction;
* the two variant tables the notes print -- the declaration withdrawn (``decl_scale = 0``)
  and the *Einmalbeitrag* form (model point 7);
* the five published ``check_*`` identities with their per-``t`` residuals, including
  ``check_net_cf`` and the delib ruling behind it, and the two scalar equivalences the
  notes deliberately keep out of a ``check_*`` cells;
* **one test per numbered modeling pitfall**, eighteen of them, named for the pitfall;
* the frame's shape and both signs of the net flow, the monthly-to-annual reconciliation
  (``result_cf_annual()`` regrouping the frame rather than reprojecting it, and the
  *Zahlweise* finally being charged for), the shipped tables' provenance and anchors, an
  input swapped without touching a formula, and a stable round trip.

There is deliberately **no sweep of the whole model point table** here: a model point's
first evaluation is the most expensive thing in the run, and the conventions suite owns
the library's single sweep.
"""
import re

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB

AP = pytest.approx        # used throughout, so an assertion fits on one line
CENT = 0.005              # money displayed to 2 d.p.
SIX_DP = 0.0000005        # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["RLV_DE_S"][0]
PRODUCT_DIR = MODEL_DIR.parent


def flat(doc):
    """Collapse whitespace, so a phrase split across a hard wrap still matches -- the
    helper ``test_model_conventions_de`` uses, for the same reason.
    """
    return re.sub(r"\s+", " ", doc)


def model_files(folder):
    """The model's own file names, ignoring ``__pycache__`` left by the doc build."""
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


# policy_year: (attained age, pols_if, prem_gross, premiums, prem_rebate, claims_death,
#     expenses, commissions, net_cf) -- the notes' worked-example table, in full, on the
# **annual** view result_cf_annual().  claims_lapse, claims_maturity and liability_cf are
# omitted there for width and asserted in the row test all the same: the two zeros are a
# statutory fact about this product.  pols_if is the count at the start of the policy year,
# which is the number the annual-step model this replaced carried on the same row and is
# unchanged by the conversion.
WORKED_EXAMPLE = {
    1:  (35, 1.000000, 1275.41, 733.01, 542.40, 178.15, 269.04, 637.71, -351.88),
    2:  (36, 0.939408, 1198.13, 688.60, 509.54, 185.01, 105.44, 6.89, 391.26),
    3:  (37, 0.901210, 1149.41, 660.60, 488.82, 194.35, 102.78, 6.61, 356.86),
    4:  (38, 0.864508, 1102.60, 633.69, 468.91, 211.46, 100.58, 6.34, 315.32),
    5:  (39, 0.837880, 1068.64, 614.18, 454.47, 224.41, 99.08, 6.14, 284.55),
    6:  (40, 0.812008, 1035.64, 595.21, 440.43, 238.14, 97.59, 5.95, 253.53),
    7:  (41, 0.786867, 1003.58, 576.78, 426.80, 252.69, 96.13, 5.77, 222.20),
    8:  (42, 0.762432, 972.41, 558.87, 413.54, 268.11, 94.68, 5.59, 190.50),
    9:  (43, 0.738680, 942.12, 541.46, 400.66, 284.43, 93.25, 5.41, 158.36),
    10: (44, 0.715587, 912.67, 524.53, 388.13, 301.71, 91.84, 5.25, 125.73),
    11: (45, 0.693130, 884.03, 508.07, 375.95, 320.01, 90.45, 5.08, 92.53),
    12: (46, 0.671287, 856.17, 492.06, 364.11, 339.37, 89.07, 4.92, 58.70),
    13: (47, 0.650036, 829.06, 476.48, 352.58, 359.84, 87.70, 4.76, 24.17),
    14: (48, 0.629355, 802.69, 461.32, 341.36, 381.49, 86.35, 4.61, -11.13),
    15: (49, 0.609224, 777.01, 446.57, 330.44, 404.37, 85.01, 4.47, -47.28),
    16: (50, 0.589621, 752.01, 432.20, 319.81, 428.54, 83.68, 4.32, -84.34),
    17: (51, 0.570527, 727.66, 418.20, 309.45, 454.06, 82.35, 4.18, -122.39),
    18: (52, 0.551923, 703.93, 404.57, 299.36, 480.98, 81.04, 4.05, -161.50),
    19: (53, 0.533788, 680.80, 391.27, 289.53, 509.37, 79.73, 3.91, -201.74),
    20: (54, 0.516105, 658.25, 378.31, 279.94, 539.28, 78.42, 3.78, -243.18),
    21: (55, 0.498853, 636.24, 365.67, 270.58, 570.78, 77.12, 3.66, -285.89),
    22: (56, 0.482016, 614.77, 353.32, 261.45, 603.90, 75.82, 3.53, -329.94),
    23: (57, 0.465576, 593.80, 341.27, 252.53, 638.72, 74.52, 3.41, -375.38),
    24: (58, 0.449515, 573.32, 329.50, 243.82, 675.27, 73.22, 3.29, -422.28),
    25: (59, 0.433815, 553.29, 317.99, 235.30, 723.59, 72.78, 3.18, -481.56),
}
# t: (pols_if, prem_gross, premiums, prem_rebate, claims_death, expenses, commissions,
#     net_cf) -- the twelve months of policy year 1 on the monthly frame, which is the
# shape the annual grid could not show.  The whole year's *Zahlbeitrag* is collected in
# month 0 on this annual-*Zahlweise* cell, against the acquisition cost and the initial
# commission; the other eleven months carry claims and a twelfth of the admin charge and
# nothing else.  Their sum is policy year 1 of WORKED_EXAMPLE, which is asserted.
MONTHS_YEAR_1 = {
    0:  (1.000000, 1275.41, 733.01, 542.40, 15.27, 188.93, 637.71, -108.90),
    1:  (0.994805, 0.00, 0.00, 0.00, 15.20, 7.47, 0.00, -22.67),
    2:  (0.989637, 0.00, 0.00, 0.00, 15.12, 7.44, 0.00, -22.55),
    3:  (0.984495, 0.00, 0.00, 0.00, 15.04, 7.40, 0.00, -22.43),
    4:  (0.979380, 0.00, 0.00, 0.00, 14.96, 7.36, 0.00, -22.32),
    5:  (0.974292, 0.00, 0.00, 0.00, 14.88, 7.32, 0.00, -22.20),
    6:  (0.969231, 0.00, 0.00, 0.00, 14.80, 7.28, 0.00, -22.09),
    7:  (0.964195, 0.00, 0.00, 0.00, 14.73, 7.24, 0.00, -21.97),
    8:  (0.959186, 0.00, 0.00, 0.00, 14.65, 7.21, 0.00, -21.86),
    9:  (0.954203, 0.00, 0.00, 0.00, 14.57, 7.17, 0.00, -21.74),
    10: (0.949246, 0.00, 0.00, 0.00, 14.50, 7.13, 0.00, -21.63),
    11: (0.944314, 0.00, 0.00, 0.00, 14.42, 7.09, 0.00, -21.52),
}
# The notes' Total row, summed at full precision and then rounded -- and, beside it, the
# same columns summed from the twenty-five *rounded* annual cells.  Four of the seven
# differ.  The premium columns are the annual-step model's own totals, an annual
# *Zahlweise* collecting on the anniversary under either grid; claims, expenses and
# net_cf are not, and that gap is the point of the finer grid.
TOTALS = {"prem_gross": 21303.65, "premiums": 12243.75, "prem_rebate": 9059.91,
          "claims_death": 9768.05, "claims_lapse": 0.00, "claims_maturity": 0.00,
          "expenses": 2367.66, "commissions": 752.81, "net_cf": -644.78}
ROUNDED_CELL_SUMS = {"prem_gross": 21303.64, "premiums": 12243.73, "prem_rebate": 9059.91,
                     "claims_death": 9768.03, "expenses": 2367.67, "commissions": 752.81,
                     "net_cf": -644.78}
# The pricing quantities behind every row above, at the precision the notes print them.
PRICING = {"tariff_annuity": 21.6374941, "tariff_claims_pv": 23472.374330,
           "tariff_sum_pv": 6491248.23, "prem_gross_level_pp": 1275.411882,
           "prem_net_level_pp": 1084.800958, "beitragsverrechnung_rate": 0.42527476,
           "prem_paid_pp": 733.011403, "zahl_over_brutto": 0.574725}
# The expiring cohort is the annual-step model's own figure to the last digit -- it is a
# survivorship the two grids share.  The split between deaths and lapses moved by 0.00044,
# which is what interleaving the two decrements monthly genuinely changes: on an annual
# grid a year's lapses are taken from a block that has borne the whole year's mortality.
CLOSURE = {"deaths": 0.03261764, "lapses": 0.53597922, "expiries": 0.43140314}
# On policy-year arguments, and every value here is bit-identical to the annual-step
# model's: the first-order Deckungskapital never left the annual grid.
RESERVE = {"peak_y": 15, "peak": 7553.290695, "next": 7511.937517,
           "q1_at_peak": 0.00414558817, "zillmer_at_0": -797.132426}
# Variant 1 -- the declaration withdrawn, decl_scale = 0, on model point 1.  The notes
# print these six rows and the Total.  t: (pols_if, prem_gross, premiums, prem_rebate,
# claims_death, expenses, commissions, net_cf).
DECL_WITHDRAWN = {
    1:  (1.000000, 1275.41, 1275.41, 0.00, 178.15, 285.31, 637.71, 174.25),
    2:  (0.939408, 1198.13, 1198.13, 0.00, 185.01, 120.72, 11.98, 880.42),
    3:  (0.901210, 1149.41, 1149.41, 0.00, 194.35, 117.45, 11.49, 826.12),
    13: (0.650036, 829.06, 829.06, 0.00, 359.84, 98.28, 8.29, 362.65),
    24: (0.449515, 573.32, 573.32, 0.00, 675.27, 80.53, 5.73, -188.22),
    25: (0.433815, 553.29, 553.29, 0.00, 723.59, 79.84, 5.53, -255.68),
}
DECL_TOTALS = {"prem_gross": 21303.65, "premiums": 21303.65, "prem_rebate": 0.00,
               "claims_death": 9768.05, "expenses": 2639.46, "commissions": 837.99,
               "net_cf": 8058.16}
# Variant 2 -- the Einmalbeitrag form, model point 7: 50 M N, 100 000 EUR konstant, ten
# years' cover, k = 1.  The whole table, short enough to assert entire.  Same columns as
# WORKED_EXAMPLE.
EINMAL = {
    1:  (50, 1.000000, 6676.93, 3728.98, 2947.95, 231.67, 174.98, 133.54, 3188.79),
    2:  (51, 0.937691, 0.00, 0.00, 0.00, 240.16, 28.75, 0.00, -268.91),
    3:  (52, 0.897762, 0.00, 0.00, 0.00, 251.77, 28.12, 0.00, -279.89),
    4:  (53, 0.859312, 0.00, 0.00, 0.00, 273.33, 27.62, 0.00, -300.96),
    5:  (54, 0.830845, 0.00, 0.00, 0.00, 289.39, 27.29, 0.00, -316.67),
    6:  (55, 0.803073, 0.00, 0.00, 0.00, 306.29, 26.95, 0.00, -333.24),
    7:  (56, 0.775968, 0.00, 0.00, 0.00, 324.06, 26.61, 0.00, -350.68),
    8:  (57, 0.749502, 0.00, 0.00, 0.00, 342.75, 26.27, 0.00, -369.02),
    9:  (58, 0.723645, 0.00, 0.00, 0.00, 362.36, 25.93, 0.00, -388.29),
    10: (59, 0.698372, 0.00, 0.00, 0.00, 388.29, 25.95, 0.00, -414.24),
}
EINMAL_TOTALS = {"prem_gross": 6676.93, "premiums": 3728.98, "prem_rebate": 2947.95,
                 "claims_death": 3010.07, "expenses": 418.47, "commissions": 133.54,
                 "net_cf": 166.90}
EINMAL_PRICING = {"tariff_annuity": 1.0, "tariff_claims_pv": 5895.894609,
                  "prem_gross_level_pp": 6676.929360,
                  "beitragsverrechnung_rate": 0.44151243}
# The scalar References the base run must carry, so that a silent edit to one of them
# fails here rather than inside a total.
BASE_REFS = {"rechnungszins": 0.01, "sicherheitszuschlag_m": 1.25, "sex_mix_male": 0.5,
             "mort_be_factor": 1.0, "surplus_share": 0.9, "decl_scale": 1.0,
             "v_max": 0.95, "zillmer_rate": 0.025, "comm_rate_init": 0.02,
             "beta_tariff": 0.05, "gamma_rate": 0.0003, "maint_prem_pct": 0.03,
             "comm_rate_renew": 0.01, "expense_infl": 0.02, "claim_expense": 250.0,
             "suicide_share": 0.03, "suicide_years": 3, "shock_lapse_lambda": 0.0,
             "sel_lapse_lambda": 0.0, "sel_lapse_ref": 0.25}


# The worked example
@pytest.mark.parametrize("y", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_rlv_anchor, y):
    """Every cell of the notes' twenty-five-row annual table, to the displayed precision --
    with the two zero claim columns and ``liability_cf``, which the table omits for width.
    Read off ``result_cf_annual()``, which regroups the monthly frame rather than
    reprojecting it, and keyed on the contractual 1-based policy year.
    """
    age, pols, gross, prem, rebate, cd, exp, comm, net = WORKED_EXAMPLE[y]
    p = de_rlv_anchor
    row = p.result_cf_annual().loc[y]
    assert p.age(12 * (y - 1)) == age and row["pols_if"] == AP(pols, abs=SIX_DP)
    assert row["prem_gross"] == AP(gross, abs=CENT)
    assert row["premiums"] == AP(prem, abs=CENT)
    assert row["prem_rebate"] == AP(rebate, abs=CENT)
    assert row["claims_death"] == AP(cd, abs=CENT)
    assert row["expenses"] == AP(exp, abs=CENT)
    assert row["commissions"] == AP(comm, abs=CENT)
    assert row["net_cf"] == AP(net, abs=CENT)
    assert row["claims_lapse"] == 0.0 and row["claims_maturity"] == 0.0
    assert row["liability_cf"] == AP(-row["net_cf"], rel=1e-15)


@pytest.mark.parametrize("t", sorted(MONTHS_YEAR_1))
def test_the_twelve_months_of_policy_year_one(de_rlv_anchor, t):
    """The monthly frame inside policy year 1 -- the view the annual grid could not show.

    Month 0 collects the whole annual *Zahlbeitrag* on this *jaehrlich* cell and bears the
    acquisition cost and the initial commission; months 1 to 11 collect nothing and carry
    a death claim and a twelfth of the sum-related admin charge.  ``pols_if`` falls every
    month rather than once at the anniversary.
    """
    pols, gross, prem, rebate, cd, exp, comm, net = MONTHS_YEAR_1[t]
    p = de_rlv_anchor
    assert p.age(t) == 35 and p.policy_year(t) == 1 and p.duration(t) == 0
    assert p.pols_if(t) == AP(pols, abs=SIX_DP)
    assert p.prem_gross(t) == AP(gross, abs=CENT)
    assert p.premiums(t) == AP(prem, abs=CENT)
    assert p.prem_rebate(t) == AP(rebate, abs=CENT)
    assert p.claims(t, "DEATH") == AP(cd, abs=CENT)
    assert p.expenses(t) == AP(exp, abs=CENT)
    assert p.commissions(t) == AP(comm, abs=CENT)
    assert p.net_cf(t) == AP(net, abs=CENT)
    assert p.claims(t, "LAPSE") == 0.0 and p.claims(t, "MATURITY") == 0.0
    assert p.liability_cf(t) == AP(-p.net_cf(t), rel=1e-15)
    # The annual amount is flat across the year; only the collection is not.
    assert p.prem_paid_pp(t) == AP(733.011403, abs=5e-7)
    assert p.prem_due(t) == (t == 0)


def test_the_annual_view_regroups_the_monthly_frame_rather_than_reprojecting_it(
        de_rlv_anchor):
    """``result_cf_annual()`` is the same numbers, grouped: every cash flow column is the
    sum of that policy year's twelve months and ``pols_if`` is the count at its start.
    A second projection on an annual grid would not satisfy both at once.
    """
    p = de_rlv_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert len(df) == 300 and len(ann) == 25
    assert list(ann.index) == list(range(1, 26)) and ann.index.name == "policy_year"
    for y in (1, 7, 25):
        months = df.loc[12 * (y - 1):12 * y - 1]
        for column in ("premiums", "claims_death", "expenses", "commissions", "net_cf"):
            assert ann.loc[y, column] == AP(months[column].sum(), rel=1e-12), (y, column)
        assert ann.loc[y, "pols_if"] == AP(p.pols_if(12 * (y - 1)), rel=1e-15)
    for column in df.columns:
        if column != "pols_if":
            assert ann[column].sum() == AP(df[column].sum(), rel=1e-12), column


def test_the_worked_example_totals_are_summed_at_full_precision(de_rlv_anchor):
    """The Total row is a full-precision sum, then rounded -- not a sum of rounded cells.
    Four of the seven money columns differ by a cent, and the notes print both; asserting
    the rounded-cell sums instead would be testing the rounding.
    """
    df = de_rlv_anchor.result_cf_annual()
    for column, total in TOTALS.items():
        assert df[column].sum() == AP(total, abs=CENT), column
    for column, rounded in ROUNDED_CELL_SUMS.items():
        cells = sum(round(float(df.loc[y, column]), 2) for y in df.index)
        assert cells == AP(rounded, abs=CENT), column
    differ = {c for c in ROUNDED_CELL_SUMS if abs(ROUNDED_CELL_SUMS[c] - TOTALS[c]) > 1e-3}
    assert differ == {"prem_gross", "premiums", "claims_death", "expenses"}
    # The monthly frame totals to the same money, the grouping being a regrouping.
    assert de_rlv_anchor.result_cf()["net_cf"].sum() == AP(TOTALS["net_cf"], abs=CENT)


def test_the_anchor_cell_is_the_configuration_the_notes_describe(de_rlv_anchor):
    """Model point 1 attribute by attribute, and the five quantities derived from it --
    ``cover_end_age`` and ``proj_len`` among them, so the two cannot disagree.
    """
    p = de_rlv_anchor
    assert (p.policy_id(), p.issue_age(), p.sex(), p.smoker()) == ("RLV-000001", 35, "M", "N")
    assert (p.sum_assured(), p.policy_term(), p.prem_term()) == (300000.0, 25, 25)
    assert (p.premium_form(), p.prem_freq()) == ("laufend", "jaehrlich")
    assert (p.benefit_schedule_id(), p.nvg_schedule_id()) == ("konstant", "keine")
    assert (p.surplus_form(), p.mort_table_id()) == ("beitragsverrechnung", "dav2008t_proxy")
    assert (p.lives(), p.issue_age2(), p.smoker2()) == (1, 0, "-")
    assert (p.rating_factor(), p.duration_y(), p.issue_date()) == (1.0, 0, "2026-01-01")
    assert (p.proj_start(), p.proj_len_y(), p.proj_len()) == (0, 25, 300)
    assert p.cover_end_age() == 60
    assert (p.pols_if_init(), p.prem_freq_load(), p.instalments()) == (1.0, 1.0, 1)
    assert (p.prem_cycle(), p.duration_mth(37), p.duration(37), p.policy_year(37)) \
        == (12, 37, 3, 4)


def test_the_base_run_references_are_the_notes_assumption_tables(risikolebensversicherung):
    """Every scalar the worked example depends on, so an edit fails here, not in a total."""
    proj = risikolebensversicherung.Projection
    for name, value in BASE_REFS.items():
        assert getattr(proj, name) == value, name


# The pricing engine, reached two independent ways each
def test_the_bruttobeitrag_solves_the_equivalence_it_was_derived_from(de_rlv_anchor):
    """G = 1 275,411882 from the closed form and from the equivalence it solves,
    ``G ae = A + z k G + beta G ae + gamma Gamma`` -- two sides of 27 596,717080 each.
    """
    p = de_rlv_anchor
    assert p.tariff_annuity() == AP(PRICING["tariff_annuity"], abs=5e-7)
    assert p.tariff_claims_pv() == AP(PRICING["tariff_claims_pv"], abs=5e-6)
    assert p.tariff_sum_pv() == AP(PRICING["tariff_sum_pv"], abs=0.005)
    g, ae, a_pv = p.prem_gross_level_pp(), p.tariff_annuity(), p.tariff_claims_pv()
    assert g == AP(PRICING["prem_gross_level_pp"], abs=5e-6)
    lhs = g * ae
    rhs = a_pv + 0.025 * 25 * g + 0.05 * lhs + 0.00030 * p.tariff_sum_pv()
    assert lhs == AP(27596.717080, abs=5e-5) and rhs == AP(lhs, rel=1e-12)
    assert 0.025 * 25 * g == AP(797.132426, abs=5e-6)   # the Zillmer charge at issue


def test_the_beitragsverrechnungssatz_is_reached_without_forming_the_premium(de_rlv_anchor):
    """v_d = 0,42527476 from its definition, and again from the one-line identity: the
    surplus share times the margin fraction of the risk element times the risk share of
    the gross premium.  The first two multiply to exactly one half on this calibration.
    """
    p = de_rlv_anchor
    v_d, g, ae = p.beitragsverrechnung_rate(), p.prem_gross_level_pp(), p.tariff_annuity()
    assert v_d == AP(PRICING["beitragsverrechnung_rate"], abs=5e-9)
    loadings = 0.00030 * p.tariff_sum_pv() + 0.025 * 25 * g
    assert loadings == AP(2744.506896, abs=5e-6)
    risk_share = 1.0 - 0.05 - loadings / (g * ae)
    assert risk_share == AP(0.85054952, abs=5e-9)
    assert 0.90 * (1.25 / 2.25) == AP(0.5, rel=1e-15)
    assert 0.5 * risk_share == AP(v_d, rel=1e-12)
    assert v_d * g * ae == AP(0.90 * (1.25 / 2.25) * p.tariff_claims_pv(), rel=1e-12)
    assert p.prem_paid_pp(0) == AP(PRICING["prem_paid_pp"], abs=5e-7)
    ratio = p.prem_paid_pp(0) / p.prem_gross_pp(0)
    assert ratio == AP(PRICING["zahl_over_brutto"], abs=5e-7)
    # Every one of these is an annual construction and none of them moved to the month:
    # the equivalence sums over policy years, so G, Gn and v_d are what they always were.
    assert p.tariff_annuity() == AP(sum(p.disc_factor(y) * p.pols_tariff(y)
                                        for y in range(25)), rel=1e-15)


def test_the_first_month_rebuilt_from_the_table_rate_up(de_rlv_anchor):
    """The notes' second check, arithmetic a reader can follow, now on month 0 of policy
    year 1: the **annual** ``q2(0) = 0,00040 x 1,095^5``, the **monthly**
    ``q2m = 1 - (1 - q2)^(1/12)`` derived from it, a claim inside the paragraph 161 window
    paying 291 000 EUR, and an expense line of four numbers of which only one is large.
    """
    p = de_rlv_anchor
    q2 = 0.00040 * 1.095 ** 5
    assert q2 == AP(0.00062969550, abs=5e-12) and p.mort_rate(0) == AP(q2, rel=1e-12)
    q2m = 1.0 - (1.0 - q2) ** (1.0 / 12.0)
    assert q2m == AP(0.000052489776, abs=5e-13)
    assert p.mort_rate_mth(0) == AP(q2m, rel=1e-15)
    # Twelve of the monthly rate compound back to exactly the year's rate.
    assert 1.0 - (1.0 - q2m) ** 12 == AP(q2, rel=1e-14)
    assert p.benefit_pp(0) == 300000.0
    assert p.benefit_paid_pp(0) == AP(0.97 * 300000.0, rel=1e-15)
    assert p.claims(0, "DEATH") == AP(291000.0 * q2m, abs=5e-6)   # = 15,274525
    g = p.prem_gross_level_pp()
    acq_net = (0.025 - 0.020) * 25 * g
    admin = 0.00030 * 300000.0 / 12.0
    collection = 0.03 * p.prem_inst_pp(0)
    claim_exp = 250.0 * q2m
    assert acq_net == AP(159.426485, abs=5e-6) and admin == AP(7.5, rel=1e-15)
    assert collection == AP(21.990342, abs=5e-6) and claim_exp == AP(0.013122, abs=5e-6)
    assert p.expenses(0) == AP(acq_net + admin + collection + claim_exp, rel=1e-12)
    assert p.expenses(0) == AP(188.929950, abs=5e-6)
    assert p.commissions(0) == AP(0.020 * 25 * g, rel=1e-12)
    assert p.commissions(0) == AP(637.705941, abs=5e-6)
    assert p.net_cf(0) == AP(-108.899012, abs=5e-6)
    # The first month's strain is the initial commission: 87 % of the premium collected.
    assert p.commissions(0) / p.premiums(0) == AP(0.87, abs=0.005)
    # The whole first policy year, which the annual grid published as one row.
    assert p.result_cf_annual().loc[1, "net_cf"] == AP(-351.883322, abs=5e-6)


def test_the_third_policy_year_rebuilt_through_two_decrement_steps(de_rlv_anchor):
    """The notes' third check: l(12) and l(24) built by hand from the **monthly** rates,
    then the third policy year's death claims.

    Twelve months of ``(1 - q2m)(1 - wm)`` collapse to the annual ``(1 - q2)(1 - w)``, so
    the in-force at each anniversary is exactly the annual-step model's -- 0,93940809 and
    0,90120993, the figures the notes have always printed.  The contractual 300 000 EUR
    instead of the paragraph 161 benefit gives 200,36 against 194,35 -- a 3 % error
    running three years, which a totals-only test would miss.
    """
    p = de_rlv_anchor
    q_a = [0.00040 * 1.095 ** k for k in (5, 6, 7)]
    q_m = [1.0 - (1.0 - q) ** (1.0 / 12.0) for q in q_a]
    w_m = [1.0 - (1.0 - w) ** (1.0 / 12.0) for w in (0.06, 0.04, 0.04)]
    l1 = ((1.0 - q_m[0]) * (1.0 - w_m[0])) ** 12
    l2 = l1 * ((1.0 - q_m[1]) * (1.0 - w_m[1])) ** 12
    assert l1 == AP(0.93940809, abs=5e-9) and l2 == AP(0.90120993, abs=5e-9)
    assert p.pols_if(12) == AP(l1, rel=1e-12) and p.pols_if(24) == AP(l2, rel=1e-12)
    # The annual form the monthly recursion collapses to, term for term.
    assert l1 == AP((1.0 - q_a[0]) * (1.0 - 0.06), rel=1e-12)
    assert p.mort_rate(12) == AP(q_a[1], rel=1e-12) and p.mort_rate(24) == AP(q_a[2], rel=1e-12)
    assert p.mort_rate_mth(24) == AP(q_m[2], rel=1e-15)
    year3 = p.result_cf_annual().loc[3, "claims_death"]
    deaths = sum(p.pols_death(t) for t in range(24, 36))
    assert year3 == AP(291000.0 * deaths, abs=5e-6)
    assert year3 == AP(194.349377, abs=5e-6)
    wrong = 300000.0 * deaths
    assert wrong == AP(200.36, abs=CENT)
    assert wrong / year3 == AP(1.0 / 0.97, rel=1e-12)


def test_closure_one_the_decrements_account_for_the_whole_policy(de_rlv_anchor):
    """Deaths + lapses + expiries = pols_if_init() exactly, and pols_if(proj_len()) = 0 --
    the state one month past the last projected one.  The split between the last two is
    what the zero lapse rate of the final **policy year** decides and no cash flow moves
    either way, which is why the identity and not the split is load-bearing.

    The expiring cohort is the annual-step model's own 0,43140314: lapse is zero through
    the whole final policy year under either grid, so the survivorship into the expiry is
    a quantity the two share.  The split between deaths and lapses is not -- interleaving
    the two decrements monthly moves 0,00044 from one to the other, because each now
    erodes the exposure the other works on.
    """
    p = de_rlv_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    expiries = sum(p.pols_maturity(t) for t in range(n))
    assert deaths == AP(CLOSURE["deaths"], abs=5e-9)
    assert lapses == AP(CLOSURE["lapses"], abs=5e-9)
    assert expiries == AP(CLOSURE["expiries"], abs=5e-9)
    assert deaths + lapses + expiries == AP(1.0, abs=1e-12)
    assert p.pols_maturity(n - 1) == AP(expiries, rel=1e-15)
    assert p.pols_maturity(0) == p.pols_maturity(n - 2) == 0.0
    assert p.pols_if(n) == 0.0 and p.pols_if_at(n - 1, "AFT_DECR") == 0.0
    # Lapse is zero through the whole of the final policy year, not merely its last month.
    assert all(p.lapse_rate(t) == 0.0 and p.lapse_rate_mth(t) == 0.0
               for t in range(n - 12, n))
    assert p.lapse_rate(n - 13) > 0.0
    assert p.lapse_rate_base(n - 1) == 0.03     # the table is live there; the model zeroes


def test_closure_two_the_suicide_wedge_is_the_only_gap_between_events_and_amounts(
        de_rlv_anchor):
    """9 785,29 of events at the contractual sum against 9 768,05 paid, and the 17,24 gap
    is exactly ``0,03 x 300 000`` times the deaths of the **first thirty-six months**,
    which are policy years 1 to 3.  A switch applied to every month, to a lapse, or over
    the wrong window breaks this and no total.

    That the window is thirty-six months and not three rows is the whole of what the
    conversion did to paragraph 161: the statute measures three years from conclusion, the
    boundary falls on an anniversary either way, and the finer grid resolves it exactly
    rather than approximately.
    """
    p = de_rlv_anchor
    n = p.proj_len()
    events = sum(p.pols_death(t) for t in range(n))
    paid = sum(p.claims(t, "DEATH") for t in range(n))
    assert 300000.0 * events == AP(9785.291238, abs=5e-6)
    assert paid == AP(9768.048760, abs=5e-6)
    wedge = 300000.0 * events - paid
    assert wedge == AP(17.242478, abs=5e-6)
    first_three_years = sum(p.pols_death(t) for t in range(36))
    assert first_three_years == AP(0.00191583088, abs=5e-12)
    assert 0.03 * 300000.0 * first_three_years == AP(wedge, rel=1e-9)
    assert p.suicide_factor(35) == AP(0.97, rel=1e-15)
    assert p.suicide_factor(36) == 1.0


def test_closure_three_the_cash_flow_statement_is_check_net_cf(de_rlv_anchor):
    """12 243,747304 - 9 768,048760 - 2 367,661171 - 752,813300 = -644,775928.  Which
    columns are *not* in it is the point: ``prem_gross`` is the guaranteed stream and
    ``prem_rebate`` must not be subtracted again.  That is why delib requires the check.
    """
    df = de_rlv_anchor.result_cf()
    prem, exp, comm = df["premiums"].sum(), df["expenses"].sum(), df["commissions"].sum()
    claims = df[["claims_death", "claims_lapse", "claims_maturity"]].sum().sum()
    assert prem == AP(12243.747304, abs=5e-6) and claims == AP(9768.048760, abs=5e-6)
    assert exp == AP(2367.661171, abs=5e-6) and comm == AP(752.813300, abs=5e-6)
    assert prem - claims - exp - comm == AP(-644.775928, abs=5e-6)
    assert df["net_cf"].sum() == AP(prem - claims - exp - comm, abs=1e-9)
    assert df["prem_gross"].sum() > prem     # not in the identity, and the larger column
    assert (df["prem_gross"] - df["premiums"] - df["prem_rebate"]).abs().max() < 1e-9


def test_the_first_order_deckungskapital_opens_and_closes_at_zero(de_rlv_anchor):
    """res(0) = 0 by the equivalence, res(n) = 0 by exhaustion, a peak of 7 553,29 EUR in
    policy year 15, and a Thiele step.  The *gezillmerte* companion opens at ``-z k G``;
    the two are formed by different summations, so the 1e-9 tolerances are headroom rather
    than a residual the shipped calibration actually shows.

    Every figure here is on a **policy-year** argument and every one of them is unchanged
    by the monthly grid: a first-order *Deckungskapital* is struck on annual bases against
    an annual *Rechnungszins*, and moving it to the month would be a different quantity.
    """
    p = de_rlv_anchor
    n, k = p.proj_len_y(), RESERVE["peak_y"]
    assert p.res_pp_at(0, "BEF_PREM") == AP(0.0, abs=1e-9)
    assert p.res_pp_at(n, "BEF_PREM") == 0.0
    assert p.res_pp_at(k, "BEF_PREM") == AP(RESERVE["peak"], abs=5e-6)
    assert p.res_pp_at(k, "BEF_PREM") / p.sum_assured() == AP(0.0252, abs=5e-5)
    gn = p.prem_net_level_pp()
    assert gn == AP(PRICING["prem_net_level_pp"], abs=5e-7)
    assert p.res_pp_at(k, "AFT_PREM") == AP(p.res_pp_at(k, "BEF_PREM") + gn, rel=1e-12)
    q1 = p.mort_rate_tar(12 * k)
    assert q1 == AP(RESERVE["q1_at_peak"], abs=5e-12)
    lhs = (p.res_pp_at(k, "BEF_PREM") + gn) * 1.01
    rhs = q1 * 300000.0 + (1.0 - q1) * p.res_pp_at(k + 1, "BEF_PREM")
    assert lhs == AP(8724.472569, abs=5e-6) and rhs == AP(lhs, abs=1e-6)
    assert p.res_pp_at(k + 1, "BEF_PREM") == AP(RESERVE["next"], abs=5e-6)
    zill = p.res_zill_pp_at(0, "BEF_PREM")
    assert zill == AP(RESERVE["zillmer_at_0"], abs=5e-6) and zill < 0.0
    assert zill == AP(-0.025 * 25 * p.prem_gross_level_pp(), abs=1e-9)


# The two variant tables the notes print
@pytest.mark.parametrize("y", sorted(DECL_WITHDRAWN))
def test_the_declaration_withdrawn_variant_row(risikolebensversicherung, y):
    """decl_scale = 0: the billed premium becomes the guaranteed one and nothing else
    moves -- ``pols_if``, ``claims_death`` and ``prem_gross`` to the last bit.  On the
    annual view, which is the one the notes print.
    """
    pols, gross, prem, rebate, cd, exp, comm, net = DECL_WITHDRAWN[y]
    model = mx.read_model(MODEL_DIR, name="RLV_DE_S_decl0")
    try:
        model.Projection.decl_scale = 0.0
        model.Projection.clear_all()
        p = model.Projection[1]
        row = p.result_cf_annual().loc[y]
        assert p.beitragsverrechnung_rate() == 0.0
        assert row["pols_if"] == AP(pols, abs=SIX_DP)
        assert row["prem_gross"] == AP(gross, abs=CENT)
        assert row["premiums"] == AP(prem, abs=CENT)
        assert row["prem_rebate"] == AP(rebate, abs=CENT)
        assert row["claims_death"] == AP(cd, abs=CENT)
        assert row["expenses"] == AP(exp, abs=CENT)
        assert row["commissions"] == AP(comm, abs=CENT)
        assert row["net_cf"] == AP(net, abs=CENT)
        assert row["premiums"] == AP(row["prem_gross"], rel=1e-15)
    finally:
        model.close()


@pytest.mark.parametrize("y", sorted(EINMAL))
def test_the_einmalbeitrag_variant_row(risikolebensversicherung, y):
    """Model point 7, the same engine at k = 1: one large inflow then nine years of pure
    outgo, the shape inverting against the level-premium cell.  The single premium falls
    in month 0 and nowhere else, which is what ``duration(t) >= prem_term()`` says.
    """
    age, pols, gross, prem, rebate, cd, exp, comm, net = EINMAL[y]
    p = risikolebensversicherung.Projection[7]
    row = p.result_cf_annual().loc[y]
    assert p.premium_form() == "einmal" and p.prem_term() == 1
    assert p.age(12 * (y - 1)) == age
    assert row["pols_if"] == AP(pols, abs=SIX_DP) and row["net_cf"] == AP(net, abs=CENT)
    assert row["prem_gross"] == AP(gross, abs=CENT)
    assert row["premiums"] == AP(prem, abs=CENT)
    assert row["prem_rebate"] == AP(rebate, abs=CENT)
    assert row["claims_death"] == AP(cd, abs=CENT)
    assert row["expenses"] == AP(exp, abs=CENT) and row["commissions"] == AP(comm, abs=CENT)
    if y == 1:
        assert p.prem_due(0) and p.premiums(0) == AP(prem, abs=CENT)
        assert all(p.premiums(t) == 0.0 for t in range(1, 12))


def test_the_einmalbeitrag_is_the_same_engine_at_a_boundary(risikolebensversicherung):
    """ae = 1, so G = (A + gamma Gamma)/(1 - beta - z), and v_d is *higher* than the
    anchor's: with one premium the Zillmer charge is 25 permille of a much smaller
    *Beitragssumme*, so more of the gross premium is risk and more of it comes back.
    """
    p = risikolebensversicherung.Projection[7]
    assert p.tariff_annuity() == AP(EINMAL_PRICING["tariff_annuity"], rel=1e-15)
    assert p.tariff_claims_pv() == AP(EINMAL_PRICING["tariff_claims_pv"], abs=5e-6)
    assert p.prem_net_level_pp() == AP(p.tariff_claims_pv(), rel=1e-15)
    closed = (p.tariff_claims_pv() + 0.00030 * p.tariff_sum_pv()) / (1.0 - 0.05 - 0.025)
    assert closed == AP(EINMAL_PRICING["prem_gross_level_pp"], abs=5e-6)
    assert p.prem_gross_level_pp() == AP(closed, rel=1e-12)
    v_d = p.beitragsverrechnung_rate()
    assert v_d == AP(EINMAL_PRICING["beitragsverrechnung_rate"], abs=5e-9) and v_d > 0.4253
    df = p.result_cf_annual()
    for column, total in EINMAL_TOTALS.items():
        assert df[column].sum() == AP(total, abs=CENT), column
    # Only net_cf drifts against its rounded cells, by one cent.
    assert sum(round(float(df.loc[y, "net_cf"]), 2) for y in df.index) == AP(166.89, abs=CENT)
    assert all(p.commissions(t) == 0.0 for t in range(12, 120))
    assert all(df.loc[y, "claims_death"] > 0.0 and df.loc[y, "net_cf"] < 0.0
               for y in range(2, 11))


# Pitfall 1 -- confusing the three "netto"s
def test_pitfall_1_the_three_nettos_are_three_different_things(
        risikolebensversicherung, de_rlv_anchor):
    """P < Gn < G: 733,01 < 1 084,80 < 1 275,41.  The billed *Zahlbeitrag* sits **below**
    the actuarial *Nettopraemie*, because ``Gn`` is struck on the loaded first-order rate
    and 90 % of that loading comes back; ``Gn < P`` would deny the central mechanic.
    """
    p = de_rlv_anchor
    phi = p.prem_freq_load()
    paid, gn, gross = p.prem_paid_pp(0) / phi, p.prem_net_level_pp(), p.prem_gross_pp(0) / phi
    assert paid < gn < gross
    assert paid == AP(733.011403, abs=5e-6) and gn == AP(1084.800958, abs=5e-6)
    # Gn is a pricing quantity and never a cash flow: nothing in the frame equals it.
    df = p.result_cf()
    assert "prem_net_level_pp" not in df.columns
    assert not (df == AP(gn, abs=1e-9)).any().any()
    names = set(risikolebensversicherung.Projection.cells) | set(
        risikolebensversicherung.Projection.refs)
    for absent in ("prem_net_pp", "nettobeitrag", "netto_beitrag", "premium_net_pp",
                   "nettotarif", "honorartarif"):
        assert absent not in names, absent


# Pitfall 2 -- carrying only one premium stream
def test_pitfall_2_the_model_carries_two_premium_streams(
        risikolebensversicherung, de_rlv_anchor):
    """prem_gross > premiums wherever a premium is due -- except on model point 12, the
    paragraph 153-excluded tariff, where the billed premium *is* the guaranteed one.
    """
    p = de_rlv_anchor
    assert all(p.prem_gross_pp(t) > p.prem_paid_pp(t) > 0.0 and p.prem_rebate_pp(t) > 0.0
               for t in range(p.proj_len()))
    # And in every month an instalment is actually collected, which on this annual
    # *Zahlweise* cell is one month in twelve.
    due = [t for t in range(p.proj_len()) if p.prem_due(t)]
    assert len(due) == 25 and due[:2] == [0, 12]
    assert all(p.prem_gross(t) > p.premiums(t) > 0.0 and p.prem_rebate(t) > 0.0
               for t in due)
    none = risikolebensversicherung.Projection[12]
    assert none.surplus_form() == "keine" and none.beitragsverrechnung_rate() == 0.0
    assert all(none.prem_gross(t) == none.premiums(t) for t in range(300))
    df = none.result_cf()
    assert (df["prem_rebate"] == 0.0).all()
    assert df["premiums"].sum() == AP(df["prem_gross"].sum(), rel=1e-15)


# Pitfall 3 -- treating the Zahlbeitrag as guaranteed
def test_pitfall_3_only_the_bruttobeitrag_is_guaranteed():
    """decl_scale = 0 raises premiums to prem_gross and changes no claim and no decrement:
    a 74,0 % increase in the bill for no change in cover.  Only the flows that scale with
    the *billed* premium follow -- collection at 3 % and renewal commission at 1 %.
    """
    base = mx.read_model(MODEL_DIR, name="RLV_DE_S_decl_base")
    stressed = mx.read_model(MODEL_DIR, name="RLV_DE_S_decl_str")
    try:
        stressed.Projection.decl_scale = 0.0
        stressed.Projection.clear_all()
        b, s = base.Projection[1].result_cf(), stressed.Projection[1].result_cf()
        assert (b["pols_if"] - s["pols_if"]).abs().max() == 0.0
        assert (b["claims_death"] - s["claims_death"]).abs().max() == 0.0
        assert (b["prem_gross"] - s["prem_gross"]).abs().max() == 0.0
        assert (s["premiums"] - s["prem_gross"]).abs().max() < 1e-9
        assert s["prem_rebate"].abs().max() == 0.0
        assert s["premiums"].sum() / b["premiums"].sum() - 1.0 == AP(0.740, abs=0.0005)
        s_ann = stressed.Projection[1].result_cf_annual()
        for column, total in DECL_TOTALS.items():
            assert s_ann[column].sum() == AP(total, abs=CENT), column
        delta = s["premiums"].sum() - b["premiums"].sum()
        assert s["expenses"].sum() - b["expenses"].sum() == AP(0.03 * delta, abs=CENT)
        # The renewal commission starts in policy year 2, so the first twelve months'
        # extra premium earns none of it.
        year_one = s["premiums"].iloc[:12].sum() - b["premiums"].iloc[:12].sum()
        renewed = delta - year_one
        assert s["commissions"].sum() - b["commissions"].sum() == AP(0.01 * renewed, abs=CENT)
    finally:
        base.close()
        stressed.close()


# Pitfall 4 -- inventing a Rueckkaufswert
def test_pitfall_4_a_lapse_pays_nothing_at_any_duration(
        risikolebensversicherung, de_rlv_anchor):
    """Paragraph 169 Abs. 1 VVG does not reach a term assurance, so the columns are zeros.
    The absent names are asserted too -- they are what a reader arriving from a US model
    would add, and every total would still look sane.  Only the benefit is nil.
    """
    p = de_rlv_anchor
    n = p.proj_len()
    assert all(p.claims(t, "LAPSE") == p.claims(t, "MATURITY") == 0.0
               for t in range(n))
    df = p.result_cf()
    assert (df["claims_lapse"] == 0.0).all() and (df["claims_maturity"] == 0.0).all()
    assert p.check_no_cash_value() is True
    assert all(p.check_no_cash_value_resid(t) == 0.0 for t in (0, 137, n - 1))
    assert p.pols_lapse(0) > 0.0 and p.pols_maturity(n - 1) > 0.0
    names = set(risikolebensversicherung.Projection.cells) | set(
        risikolebensversicherung.Projection.refs)
    for absent in ("av_pp_at", "av_at", "prem_to_av_pp", "cv_pp", "surr_charge_rate",
                   "surr_value_pp", "paid_up_factor", "beitragsfreie_summe", "mvr",
                   "asset_share", "claims_surr", "withdrawals", "rueckkaufswert"):
        assert absent not in names, absent
    assert "claims_surr" not in df.columns and "claims_wd" not in df.columns


# Pitfall 5 -- concluding there is no Deckungskapital
def test_pitfall_5_a_level_premium_against_a_rising_rate_builds_a_reserve(de_rlv_anchor):
    """Small, fully consumed by expiry, strictly positive inside.  "No *Sparanteil*,
    therefore no reserve" is the wrong inference and fails the closure check; the
    *gezillmerte* companion is negative from the first day and zero at expiry.
    """
    p = de_rlv_anchor
    n = p.proj_len_y()
    assert p.res_pp_at(0, "BEF_PREM") == AP(0.0, abs=1e-9)
    assert p.res_pp_at(n, "BEF_PREM") == 0.0
    interior = [p.res_pp_at(y, "BEF_PREM") for y in range(1, n)]
    assert all(v > 0.0 for v in interior) and max(interior) / p.sum_assured() < 0.03
    assert max(interior) == AP(RESERVE["peak"], abs=5e-6)
    assert p.res_zill_pp_at(0, "BEF_PREM") == AP(
        -0.025 * 25 * p.prem_gross_level_pp(), abs=1e-9)
    assert p.res_zill_pp_at(n, "BEF_PREM") == AP(0.0, abs=1e-9)
    assert p.check_res_roll_fwd() is True
    assert all(p.check_res_roll_fwd_resid(y) == AP(0.0, abs=1e-6)
               for y in (0, 7, 15, n - 1))
    # The reserve is a pricing diagnostic: it enters no cash flow and no result_cf column.
    assert "res_pp" not in p.result_cf().columns
    assert "res_pp" in p.result_pols().columns
    # It is published against the policy year of each month, and so is flat across one.
    pols = p.result_pols()
    assert pols.loc[12, "res_pp"] == AP(pols.loc[23, "res_pp"], rel=1e-15)
    assert pols.loc[12, "res_pp"] == AP(p.res_pp_at(1, "BEF_PREM"), rel=1e-15)


# Pitfall 6 -- letting sex into the price
def test_pitfall_6_sex_never_reaches_the_premium(risikolebensversicherung):
    """Model points 1 and 2 differ only in ``sex`` and pay the same premium exactly, while
    the DAV tables behind the tariff stay sex-distinct -- so the cross-subsidy appears in
    the cash flows: claim totals differing by a factor near two on identical premiums.
    """
    male = risikolebensversicherung.Projection[1]
    female = risikolebensversicherung.Projection[2]
    assert male.sex() == "M" and female.sex() == "F"
    assert male.issue_age() == female.issue_age() == 35
    assert female.prem_gross_level_pp() == AP(male.prem_gross_level_pp(), rel=1e-12)
    assert female.beitragsverrechnung_rate() == AP(
        male.beitragsverrechnung_rate(), rel=1e-12)
    for t in (0, 132, 288):
        assert female.prem_gross_pp(t) == AP(male.prem_gross_pp(t), rel=1e-12)
        assert female.prem_paid_pp(t) == AP(male.prem_paid_pp(t), rel=1e-12)
        assert female.mort_rate_tar(t) == AP(male.mort_rate_tar(t), rel=1e-12)
        # The projection is not unisex: her own-sex rate is half his, annual and monthly.
        assert female.mort_rate(t) == AP(0.5 * male.mort_rate(t), rel=1e-12)
        assert female.mort_rate_mth(t) < 0.5001 * male.mort_rate_mth(t)
    m_df, f_df = male.result_cf(), female.result_cf()
    assert m_df["claims_death"].sum() / f_df["claims_death"].sum() == AP(1.98, abs=0.05)
    assert m_df["net_cf"].sum() == AP(-644.78, abs=CENT)
    assert f_df["net_cf"].sum() == AP(4252.82, abs=CENT)


# Pitfall 7 -- applying the Sicherheitszuschlag to the projection
def test_pitfall_7_q1_prices_and_q2_projects(risikolebensversicherung):
    """claims_death is invariant to ``sicherheitszuschlag_m`` and prem_gross is not, and
    the ratio between the orders is ``2.25 x (blend / own-sex rate)`` -- 1,6875 male and
    3,375 female.  Moving m over 1.0 to 1.5 moves G by 22,5 % and the Zahlbeitrag by 6,0 %.
    """
    male = risikolebensversicherung.Projection[1]
    female = risikolebensversicherung.Projection[2]
    for t in (0, 144, 288):
        assert male.mort_rate_tar(t) / male.mort_rate(t) == AP(1.6875, rel=1e-9)
        assert female.mort_rate_tar(t) / female.mort_rate(t) == AP(3.375, rel=1e-9)
    blend = male.mort_rate_blend(0)
    assert blend == AP(0.75 * male.mort_rate_at_age("M", "N", 35), rel=1e-12)
    assert male.mort_rate_tar(0) == AP(2.25 * blend, rel=1e-12)
    base_claims = male.result_cf()["claims_death"].sum()
    seen = {}
    for value, name in ((1.0, "RLV_DE_S_m100"), (1.5, "RLV_DE_S_m150")):
        model = mx.read_model(MODEL_DIR, name=name)
        try:
            model.Projection.sicherheitszuschlag_m = value
            model.Projection.clear_all()
            p = model.Projection[1]
            assert p.result_cf()["claims_death"].sum() == AP(base_claims, rel=1e-12)
            seen[value] = (p.prem_gross_level_pp(), p.prem_paid_pp(0))
        finally:
            model.close()
    assert seen[1.0] == AP((1146.33, 711.63), abs=CENT)
    assert seen[1.5] == AP((1404.05, 754.34), abs=CENT)
    assert seen[1.5][0] / seen[1.0][0] - 1.0 == AP(0.225, abs=0.001)
    assert seen[1.5][1] / seen[1.0][1] - 1.0 == AP(0.060, abs=0.001)


# Pitfall 8 -- applying the paragraph 161 switch beyond three years
def test_pitfall_8_the_suicide_switch_runs_three_years_and_touches_death_alone(
        risikolebensversicherung, de_rlv_anchor):
    """0,97 for t in {0,1,2} -- policy years 1 to 3 -- and 1 thereafter, and nothing else
    moves.  On the in-force point 8, opening at t = duration_y = 12, the factor is 1 at
    every projected t -- the window is keyed to duration, not to the frame's first row --
    and on point 13 it covers three of five.
    """
    p = de_rlv_anchor
    n = p.proj_len()
    # Thirty-six months, and the boundary falls on an anniversary because the statute
    # measures the window in years.
    assert all(p.suicide_factor(t) == 0.97 for t in range(36))
    assert all(p.suicide_factor(t) == 1.0 for t in range(36, n))
    assert p.benefit_paid_pp(35) == AP(0.97 * p.benefit_pp(35), rel=1e-15)
    # It never reaches a lapse or an expiry, both of which pay nothing in any event.
    assert p.claims(1, "LAPSE") == 0.0 and p.claims(n - 1, "MATURITY") == 0.0
    assert p.pols_lapse(1) > 0.0
    inforce = risikolebensversicherung.Projection[8]
    assert inforce.duration_y() == 12 and inforce.proj_start() == 144
    assert all(inforce.suicide_factor(t) == 1.0 for t in range(144, 360))
    assert list(inforce.result_cf().index) == list(range(144, 360))
    short = risikolebensversicherung.Projection[13]
    assert short.proj_len_y() == 5 and short.proj_len() == 60
    assert short.issue_age() == 60
    assert [short.suicide_factor(12 * y) for y in range(5)] == [0.97, 0.97, 0.97, 1.0, 1.0]


# Pitfall 9 -- the clock restarts for a Nachversicherungsgarantie increment
def test_pitfall_9_each_increment_carries_its_own_three_year_window(
        risikolebensversicherung):
    """Model point 9 steps the sum to 1.2 at policy year 6 (``t = 5``) and 1.4 at policy
    year 12 (``t = 11``).  In the period of and the two after each step the base tranche is
    out of its window and the increment inside it, so the ratio is strictly between 0,97
    and 1.
    """
    p = risikolebensversicherung.Projection[9]
    assert p.nvg_schedule_id() == "nvg_zwei_erhoehungen"
    assert (p.sum_uplift_y(4), p.sum_uplift_y(5)) == (1.0, 1.2)
    assert (p.sum_uplift_y(10), p.sum_uplift_y(11)) == (1.2, 1.4)
    # The step lands on the anniversary and is flat across the year it opens.
    assert (p.sum_uplift(59), p.sum_uplift(60), p.sum_uplift(71)) == (1.0, 1.2, 1.2)
    assert p.benefit_pp(60) == AP(1.2 * p.sum_assured(), rel=1e-12)
    assert all(p.suicide_factor(12 * y) == AP(0.97, rel=1e-15) for y in (0, 1, 2))
    assert all(p.suicide_factor(12 * y) == AP(1.0, rel=1e-15)
               for y in (3, 4, 8, 9, 10, 14, 27))
    for y in (5, 6, 7):
        assert p.suicide_factor(12 * y) == AP(1.0 - 0.03 * (0.2 / 1.2), rel=1e-12)
        assert 0.97 < p.suicide_factor(12 * y) < 1.0
    for y in (11, 12, 13):
        assert p.suicide_factor(12 * y) == AP(1.0 - 0.03 * (0.2 / 1.4), rel=1e-12)
        assert 0.97 < p.suicide_factor(12 * y) < 1.0
    # Each increment's window is three whole years from its own anniversary, so it opens
    # and closes on one: months 60 to 95 for the first.
    assert p.suicide_factor(95) == AP(p.suicide_factor(60), rel=1e-15)
    assert p.suicide_factor(96) == AP(1.0, rel=1e-15)
    assert {risikolebensversicherung.Projection[1].sum_uplift(t)
            for t in range(300)} == {1.0}


# Pitfall 10 -- mishandling the Ratenzahlungszuschlag
def test_pitfall_10_the_frequency_loading_is_applied_once(risikolebensversicherung):
    """phi multiplies the **annual** billed amount, so both streams and the rebate carry
    it: on the monthly point ``prem_gross_pp(0)`` is exactly 1.05 times the unloaded level
    premium, and the instalment is a twelfth of that.  Loading each stream separately, or
    loading the instalment again after dividing, breaks the split identity.

    On the monthly grid the ``instalments`` column is finally load-bearing: it sets the
    collection cycle, so the surcharge is at last charging for a service the model renders.
    """
    monthly = risikolebensversicherung.Projection[4]
    assert monthly.prem_freq() == "monatlich"
    assert monthly.prem_freq_load() == 1.05 and monthly.instalments() == 12
    assert monthly.prem_cycle() == 1 and all(monthly.prem_due(t) for t in range(12))
    g, v_d = monthly.prem_gross_level_pp(), monthly.beitragsverrechnung_rate()
    assert monthly.prem_gross_pp(0) == AP(1.05 * g, rel=1e-12)
    assert monthly.prem_rebate_pp(0) == AP(1.05 * v_d * g, rel=1e-12)
    assert monthly.prem_paid_pp(0) == AP(
        monthly.prem_gross_pp(0) - monthly.prem_rebate_pp(0), rel=1e-15)
    # The instalment is the annual amount divided once, never loaded twice.
    assert monthly.prem_inst_pp(0) == AP(monthly.prem_paid_pp(0) / 12.0, rel=1e-15)
    assert sum(monthly.prem_inst_pp(t) for t in range(12)) == AP(
        monthly.prem_paid_pp(0), rel=1e-12)
    # The ratio Zahl/Brutto is untouched by the loading: it cancels in both streams.
    assert monthly.prem_paid_pp(0) / monthly.prem_gross_pp(0) == AP(1.0 - v_d, rel=1e-15)
    quarterly = risikolebensversicherung.Projection[5]
    half = risikolebensversicherung.Projection[6]
    annual = risikolebensversicherung.Projection[1]
    assert quarterly.prem_freq_load() == 1.03 and quarterly.instalments() == 4
    assert quarterly.prem_cycle() == 3
    assert [t for t in range(12) if quarterly.prem_due(t)] == [0, 3, 6, 9]
    assert half.prem_freq_load() == 1.02 and half.instalments() == 2
    assert half.prem_cycle() == 6
    assert [t for t in range(12) if half.prem_due(t)] == [0, 6]
    assert annual.prem_freq_load() == 1.0 and annual.instalments() == 1
    assert annual.prem_cycle() == 12
    assert [t for t in range(12) if annual.prem_due(t)] == [0]
    for p in (monthly, quarterly, half, annual):
        assert p.check_prem_split() is True
        assert p.check_prem_split_resid(0) == AP(0.0, abs=1e-9)
        assert p.check_prem_split_resid(7) == AP(0.0, abs=1e-9)


# Pitfall 11 -- double-counting premium cessation at death
def test_pitfall_11_the_premium_cessation_rule_is_applied_once(de_rlv_anchor):
    """Instalments are collected at the start of the month and claims fall at its end, so
    a claimant has already paid.  A further ``(1 - q2m)`` factor applies the rule twice,
    costing 0,038 EUR in the first month here and more as the death rate climbs.

    The finer grid narrows the error without removing the trap: the rule is now applied
    once per month rather than once per year, so the wrong factor is smaller and there are
    twelve times as many chances to apply it.
    """
    p = de_rlv_anchor
    for t in (0, 144, 288):
        assert p.premiums(t) == AP(p.prem_inst_pp(t) * p.pols_if(t), rel=1e-15)
        assert p.prem_gross(t) == AP(p.prem_gross_inst_pp(t) * p.pols_if(t), rel=1e-15)
        assert p.prem_rebate(t) == AP(p.prem_rebate_inst_pp(t) * p.pols_if(t), rel=1e-15)
    twice = p.prem_inst_pp(0) * p.pols_if(0) * (1.0 - p.mort_rate_mth(0))
    assert p.premiums(0) - twice == AP(733.011403 * p.mort_rate_mth(0), abs=5e-9)
    assert p.premiums(0) - twice == AP(0.038475, abs=5e-6)
    # The claim expense, by contrast, *is* charged on the deaths and only on them.
    assert p.expenses(288) - p.maint_pp(288) * p.pols_if(288) == AP(
        250.0 * p.pols_death(288), rel=1e-12)


# Pitfall 12 -- running the premium past the Beitragszahlungsdauer
def test_pitfall_12_the_premium_stops_at_the_beitragszahlungsdauer(
        risikolebensversicherung):
    """Model point 6 has k = 12 years against n = 20: the last instalment falls in month
    138 -- the second of a *halbjaehrlich* cycle in policy year 12 -- and all three
    premium cells are zero from month 144 while ``claims_death`` runs to expiry and the
    reserve falls.  ``check_prem_split()`` guards the zero branch as well as the paying
    one, and the boundary is an anniversary because the *Beitragszahlungsdauer* is stated
    in whole years.
    """
    p = risikolebensversicherung.Projection[6]
    assert p.prem_term() == 12 and p.policy_term() == 20 and p.proj_len() == 240
    assert p.instalments() == 2 and p.prem_cycle() == 6
    assert p.prem_gross_pp(143) > 0.0 and p.prem_inst_pp(138) > 0.0
    assert p.prem_inst_pp(139) == 0.0          # no instalment due in that month
    for t in range(144, 240):
        assert p.prem_gross_pp(t) == p.prem_rebate_pp(t) == p.prem_paid_pp(t) == 0.0
        assert p.premiums(t) == p.prem_gross(t) == p.commissions(t) == 0.0
        assert p.claims(t, "DEATH") > 0.0
    assert p.check_prem_split() is True
    reserve = [p.res_pp_at(y, "BEF_PREM") for y in range(12, 20)]
    assert all(a > b for a, b in zip(reserve, reserve[1:]))
    assert p.res_pp_at(20, "BEF_PREM") == 0.0


# Pitfall 13 -- hard-coding a constant sum insured
def test_pitfall_13_the_three_versicherungssumme_shapes_are_a_schedule(
        risikolebensversicherung, de_rlv_anchor):
    """Flat on point 1; linear to S0/n on point 4; slowly-then-fast on point 5 -- the
    property a linear schedule gets backwards, and the whole reason the *annuitaetisch
    fallende* shape exists.
    """
    flat_cell = de_rlv_anchor
    assert {flat_cell.benefit_pp(t) for t in range(300)} == {300000.0}
    linear = risikolebensversicherung.Projection[4]
    n = linear.proj_len_y()
    assert linear.benefit_schedule_id() == "linear_fallend"
    assert linear.benefit_pp(0) == AP(250000.0, rel=1e-12)
    assert linear.benefit_pp(12 * (n - 1)) == AP(250000.0 / n, rel=1e-12)
    steps = {round(linear.benefit_pp(12 * y) - linear.benefit_pp(12 * (y + 1)), 6)
             for y in range(n - 1)}
    assert len(steps) == 1 and steps.pop() == AP(250000.0 / n, rel=1e-9)
    # The sum steps on the anniversary and is flat inside a policy year: a declining
    # Versicherungssumme does not decline monthly just because the grid does.
    assert linear.benefit_pp(11) == AP(linear.benefit_pp(0), rel=1e-15)
    assert linear.benefit_pp(12) < linear.benefit_pp(11)
    annuity = risikolebensversicherung.Projection[5]
    m = annuity.proj_len_y()
    assert annuity.benefit_schedule_id() == "annuitaet_fallend_3pct"
    assert annuity.benefit_pp(0) == AP(400000.0, rel=1e-12)
    first = annuity.benefit_pp(0) - annuity.benefit_pp(12)
    last = annuity.benefit_pp(12 * (m - 2)) - annuity.benefit_pp(12 * (m - 1))
    assert 0.0 < first < last
    assert first == AP(8407.70, abs=CENT) and last == AP(19236.22, abs=CENT)
    # A linear schedule would have made the two equal; that is the error being guarded.
    assert last / first == AP(2.288, abs=0.005)


# Pitfall 14 -- combining two lives after loading instead of before
def test_pitfall_14_two_lives_are_combined_before_the_loading(risikolebensversicherung):
    """Q = qA + qB - qA qB at table level, then (1 + m) rf on the combined blend.  The
    independence assumption understates the true first-death rate for a couple sharing a
    household, a vehicle and a lifestyle, and no German figure bounds the understatement.
    """
    p = risikolebensversicherung.Projection[10]
    assert p.lives() == 2 and p.issue_age() == 38 and p.issue_age2() == 36
    assert p.smoker() == "N" and p.smoker2() == "N"
    q_a, q_b = p.mort_rate_at_age("M", "N", 38), p.mort_rate_at_age("M", "N", 36)
    assert p.mort_rate_base(0) == AP(q_a + q_b - q_a * q_b, rel=1e-15)
    assert max(q_a, q_b) < p.mort_rate_base(0) < q_a + q_b
    blend_a = 0.5 * q_a + 0.5 * p.mort_rate_at_age("F", "N", 38)
    blend_b = 0.5 * q_b + 0.5 * p.mort_rate_at_age("F", "N", 36)
    combined = blend_a + blend_b - blend_a * blend_b
    assert p.mort_rate_blend(0) == AP(combined, rel=1e-15)
    assert p.mort_rate_tar(0) == AP(2.25 * combined, rel=1e-12)
    # Loading first and combining after inflates the cross term by (1 + m)^2 instead of
    # (1 + m), so the first-death rate comes out understated -- a convention to declare.
    wrong = 2.25 * blend_a + 2.25 * blend_b - (2.25 * blend_a) * (2.25 * blend_b)
    assert wrong < p.mort_rate_tar(0)
    assert p.mort_rate_tar(0) - wrong == AP(2.25 * 1.25 * blend_a * blend_b, rel=1e-12)
    assert p.check_pols_roll_fwd() is True


# Pitfall 15 -- returning the Kostenueberschuss as well as the Risikoueberschuss
def test_pitfall_15_only_the_mortality_margin_is_returned(de_rlv_anchor):
    """prem_rebate is invariant to the modelled expense levels and net_cf is not: the
    tariff's beta is 5,0 % against a modelled 3,0 %, so a cost result emerges in
    ``net_cf`` and stays there.  A stated simplification, not an oversight.
    """
    base = de_rlv_anchor.result_cf()
    model = mx.read_model(MODEL_DIR, name="RLV_DE_S_cost")
    try:
        model.Projection.maint_prem_pct = 0.06
        model.Projection.comm_rate_renew = 0.02
        model.Projection.clear_all()
        df = model.Projection[1].result_cf()
        assert df["prem_rebate"].sum() == AP(base["prem_rebate"].sum(), rel=1e-12)
        assert df["premiums"].sum() == AP(12243.747304, abs=5e-6)
        assert df["claims_death"].sum() == AP(9768.048760, abs=5e-6)
        assert df["net_cf"].sum() < base["net_cf"].sum()
        assert df["net_cf"].sum() == AP(-1127.20, abs=CENT)
    finally:
        model.close()


# Pitfall 16 -- taking the whole-market Stornoquote as the term-life lapse rate
def test_pitfall_16_the_lapse_table_is_the_term_life_one(
        risikolebensversicherung, de_rlv_anchor):
    """6 % / 4 % / 4 % / 3 % **a year**, and zero through the final policy year -- a
    property of the last year, living in the formula and not in the table, whose own row
    still reads 3 %.  The table is keyed on the 1-based ``policy_year``, so the twelve
    months of policy year 1 all read its row 1.  The monthly rate applied is
    ``1 - (1 - w)^(1/12)`` and twelve of them compound back to the year's rate exactly.
    The GDV whole-market *Stornoquote* is nowhere near either and is not used.
    """
    p = de_rlv_anchor
    assert all(p.lapse_rate(t) == 0.06 for t in range(12))
    assert all(p.lapse_rate(t) == 0.04 for t in range(12, 36))
    assert all(p.lapse_rate(t) == 0.03 for t in range(36, 288))
    assert 1.0 - (1.0 - p.lapse_rate_mth(0)) ** 12 == AP(0.06, rel=1e-14)
    assert p.lapse_rate_mth(0) == AP(0.005143, abs=5e-7)
    assert all(p.lapse_rate(t) == 0.0 for t in range(288, 300))
    assert p.lapse_rate_base(299) == 0.03
    assert p.pols_lapse(288) == 0.0 and p.pols_lapse(287) > 0.0
    assert p.lapse_rate(0) > 0.0272 and p.lapse_rate(36) > 0.012
    longest = risikolebensversicherung.Projection[14]
    assert longest.proj_len_y() == 40 and longest.proj_len() == 480
    assert longest.issue_age() == 18
    assert longest.lapse_cum(0) == 0.0
    # Built from the monthly rates, and so equal at the anniversary to the figure the
    # annual-step model reached by multiplying the annual ones.
    assert longest.lapse_cum(468) == AP(0.71063050, abs=5e-9)
    assert longest.lapse_cum(479) == AP(longest.lapse_cum(468), rel=1e-15)
    assert longest.check_pols_roll_fwd() is True


# Pitfall 17 -- letting rating_factor scale the benefit
def test_pitfall_17_a_risikozuschlag_loads_the_mortality_and_never_the_benefit():
    """Model point 11 at rating_factor 1.75 against the same cell at 1.00: both orders are
    loaded, so an impaired life pays more *and* claims more, the *Zahl/Brutto* ratio moves
    by 0,4835 of a percentage point, and the benefit is untouched.
    """
    model = mx.read_model(MODEL_DIR, name="RLV_DE_S_rating")
    try:
        rated = model.Projection[11]
        assert rated.rating_factor() == 1.75 and rated.smoker() == "R"
        rated_ratio = rated.prem_paid_pp(0) / rated.prem_gross_pp(0)
        rated_g = rated.prem_gross_level_pp()
        rated_benefit = [rated.benefit_pp(t) for t in (0, 96, 204)]
        rated_claims = float(rated.result_cf()["claims_death"].sum())
        table = model.Data.model_point_table().copy()
        table.loc[11, "rating_factor"] = 1.0
        alt = model.Data.input_dir() / "model_point_table_rf1.csv"
        table.to_csv(alt)
        try:
            model.Data.model_point_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            plain = model.Projection[11]
            assert plain.rating_factor() == 1.0
            assert [plain.benefit_pp(t) for t in (0, 96, 204)] == rated_benefit
            assert rated_g / plain.prem_gross_level_pp() == AP(1.70, abs=0.01)
            plain_claims = float(plain.result_cf()["claims_death"].sum())
            assert rated_claims / plain_claims == AP(1.69, abs=0.01)
            moved = abs(rated_ratio - plain.prem_paid_pp(0) / plain.prem_gross_pp(0))
            assert moved < 0.01 and moved == AP(0.004835, abs=5e-6)
        finally:
            alt.unlink(missing_ok=True)
    finally:
        model.close()


# Pitfall 18 -- treating the Ueber-Kreuz-Versicherung as a different product
def test_pitfall_18_the_ueber_kreuz_structure_is_not_a_product(risikolebensversicherung):
    """A contracting structure with identical cover and identical cash flows -- only the
    *Erbschaftsteuer* outcome changes.  No cells, Reference, model-point column or CSV
    mentions it, and the documents say why rather than leaving a reader to look.
    """
    names = set(risikolebensversicherung.Projection.cells) | set(
        risikolebensversicherung.Projection.refs)
    names |= set(risikolebensversicherung.Data.cells) | set(
        risikolebensversicherung.Data.refs)
    for absent in ("ueber_kreuz", "kreuz_versicherung", "cross_ownership",
                   "erbschaftsteuer", "freibetrag", "steuerklasse"):
        assert absent not in names, absent
    columns = set(risikolebensversicherung.Data.model_point_table().columns)
    assert not any("kreuz" in c.lower() for c in columns)
    for csv in sorted(PRODUCT_DIR.glob("*.csv")):
        assert "kreuz" not in csv.read_text(encoding="utf-8").lower(), csv.name
    doc = (PRODUCT_DIR / "model.md").read_text(encoding="utf-8")
    assert "Über-Kreuz-Versicherung" in doc and "contracting structure" in doc


# The published identities
def test_all_five_checks_hold_on_the_anchor_with_zero_residuals(de_rlv_anchor):
    """The five per-t identities, and delib's own ruling among them: ``check_net_cf()``
    reconciles the headline number in code rather than only in prose.
    """
    p = de_rlv_anchor
    n = p.proj_len()
    assert p.check_net_cf() is True and p.check_pols_roll_fwd() is True
    assert p.check_prem_split() is True and p.check_res_roll_fwd() is True
    assert p.check_no_cash_value() is True
    for t in (0, 1, 144, n - 2, n - 1):
        assert p.check_net_cf_resid(t) == AP(0.0, abs=1e-9)
        assert p.check_pols_roll_fwd_resid(t) == AP(0.0, abs=1e-12)
        assert p.check_prem_split_resid(t) == AP(0.0, abs=1e-9)
        assert p.check_no_cash_value_resid(t) == 0.0
    # The reserve check is per policy year, the Deckungskapital being annual.
    for y in (0, 1, 12, p.proj_len_y() - 1):
        assert p.check_res_roll_fwd_resid(y) == AP(0.0, abs=1e-6)
    for t in (0, 6, n - 1):
        assert p.net_cf(t) == AP(
            p.premiums(t) - p.claims(t) - p.expenses(t) - p.commissions(t), rel=1e-12)
        assert p.claims(t) == AP(p.claims(t, "DEATH"), rel=1e-15)


def test_the_scalar_equivalences_live_here_and_not_in_a_check_cells(de_rlv_anchor):
    """The two identities that are scalar rather than per-period.  Forcing them into a
    per-``t`` residual would invent a decomposition the product does not have.
    """
    p = de_rlv_anchor
    g, ae, a_pv = p.prem_gross_level_pp(), p.tariff_annuity(), p.tariff_claims_pv()
    assert g * ae == AP(
        a_pv + 0.025 * 25 * g + 0.05 * g * ae + 0.00030 * p.tariff_sum_pv(), rel=1e-12)
    assert p.beitragsverrechnung_rate() * g * ae == AP(
        0.90 * (1.25 / 2.25) * a_pv, rel=1e-12)


# Structure, documentation and inputs
def test_result_cf_shape_and_both_signs_of_the_net_flow(de_rlv_anchor):
    """The notes' eleven columns in order, contiguous from t0 to ``proj_len() - 1`` on the
    0-based **monthly** frame, with ``liability_cf`` the eleventh and ``-net_cf`` exactly.
    """
    df = de_rlv_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "prem_gross", "premiums", "prem_rebate",
        "claims_death", "claims_lapse", "claims_maturity",
        "expenses", "commissions", "net_cf", "liability_cf"]
    assert list(df.index) == list(range(300)) and df.index.name == "t"
    assert df.index[0] == de_rlv_anchor.proj_start() == 0
    assert df.index[-1] == de_rlv_anchor.proj_len() - 1
    assert len(df) == de_rlv_anchor.proj_len() - 12 * de_rlv_anchor.duration_y()
    assert df["pols_if"].iloc[0] == de_rlv_anchor.pols_if_init()
    assert "claims" not in df.columns    # never the subtotal beside its own parts
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == 0.0
    outgo = (df["claims_death"] + df["claims_lapse"] + df["claims_maturity"]
             + df["expenses"] + df["commissions"])
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == AP(0.0, abs=1e-9)
    # Month 0 collects the year's premium against the acquisition cost and the initial
    # commission; the eleven months after it collect nothing and are all negative.
    assert df["net_cf"].iloc[0] == AP(-108.90, abs=CENT)
    assert (df["net_cf"].loc[1:11] < 0.0).all()
    # Read by policy year: a first-year strain, thin positive years, a crossover at 14.
    ann = de_rlv_anchor.result_cf_annual()
    assert ann["net_cf"].loc[1] == AP(-351.88, abs=CENT)
    assert (ann["net_cf"].loc[2:13] > 0.0).all() and (ann["net_cf"].loc[14:25] < 0.0).all()


def test_invalid_enum_values_raise(de_rlv_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_rlv_anchor.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        de_rlv_anchor.pols_if_at(0, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        de_rlv_anchor.res_pp_at(0, "MID_YEAR")


def test_docstrings_describe_the_current_structure(risikolebensversicherung):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = flat(risikolebensversicherung.doc)
    for phrase in ("Risikolebensversicherung", "mechanics demonstration", "external",
                   "once per model", "Bruttobeitrag", "Zahlbeitrag",
                   "Beitragsverrechnung", "Data", "Projection"):
        assert phrase in doc, phrase
    proj = flat(risikolebensversicherung.Projection.doc)
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "mort_rate_tar", "suicide_factor",
                  "benefit_paid_pp", "beitragsverrechnung_rate", "res_pp_at", "lapse_cum",
                  "duration_mth", "policy_year", "mort_rate_mth", "lapse_rate_mth",
                  "prem_inst_pp", "result_cf_annual"):
        assert cells in proj, cells
    # The conversion's own decisions are named on the page, not merely implemented.
    assert "What the monthly grid changes, and what it does not" in proj
    for phrase in ("policy months", "bit-identical", "anniversary",
                   "1 - (1 - r)^(1/12)"):
        assert phrase in proj, phrase
    data = flat(risikolebensversicherung.Data.doc)
    assert "TradLife_A" in data and "DAV 2008 T" in data and "provenance" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "benefit_schedule",
                  "nvg_schedule", "lapse_table", "freq_loading_table"):
        assert cells in data, cells


def test_the_shared_protection_vocabulary_is_present(risikolebensversicherung):
    """The names this model shares with frlib's TD_FR_S, the same product in France --
    and the German delta beside them: two premium streams, and the rate between them.
    """
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_death", "pols_lapse", "pols_maturity", "mort_rate", "mort_rate_base",
        "lapse_rate", "lapse_rate_base", "lapse_cum", "premiums", "benefit_pp",
        "suicide_factor", "claims", "commissions", "expenses", "inflation_factor",
        "net_cf", "liability_cf", "result_cf", "prem_freq_load",
        "duration_mth", "duration", "policy_year", "proj_len_y",
        "mort_rate_mth", "lapse_rate_mth", "result_cf_annual",
        "check_no_cash_value", "check_pols_roll_fwd",
        "prem_gross", "prem_gross_pp", "prem_rebate", "prem_rebate_pp", "prem_paid_pp",
        "beitragsverrechnung_rate", "mort_rate_tar", "res_pp_at", "res_zill_pp_at",
        "check_net_cf", "check_prem_split"}
    names = set(risikolebensversicherung.Projection.cells) | set(
        risikolebensversicherung.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Six CSVs beside run.py, five with a per-row provenance column.  DAV 2008 T is cited
    by name and never shipped, and the three anchors a replacement must preserve are
    asserted here: the 50/50 blend, the female-to-male ratio and the smoker multiplier.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "mort_table.csv", "benefit_schedule.csv",
                "nvg_schedule.csv", "lapse_table.csv", "freq_loading_table.csv"}
    assert expected == {p.name for p in PRODUCT_DIR.iterdir() if p.suffix == ".csv"}
    mort = pd.read_csv(PRODUCT_DIR / "mort_table.csv",
                       index_col=["table_id", "sex", "smoker", "age"])
    assert "DAV 2008 T" in str(mort["provenance"].iloc[0])
    assert float(mort.at[("dav2008t_proxy", "M", "N", 30), "mort_rate"]) == 0.00040
    assert float(mort.at[("dav2008t_proxy", "F", "N", 30), "mort_rate"]) == 0.00020
    for age in (25, 35, 45, 60):
        male = float(mort.at[("dav2008t_proxy", "M", "N", age), "mort_rate"])
        female = float(mort.at[("dav2008t_proxy", "F", "N", age), "mort_rate"])
        smoker = float(mort.at[("dav2008t_proxy", "M", "R", age), "mort_rate"])
        assert female / male == AP(0.50, rel=1e-12) and smoker / male == AP(2.20, rel=1e-12)
        assert 0.5 * male + 0.5 * female == AP(0.00030 * 1.095 ** (age - 30), rel=1e-9)
    assert mort["mort_rate"].max() <= 1.0
    assert sorted(set(mort.index.get_level_values("age"))) == list(range(18, 81))
    lapse = pd.read_csv(PRODUCT_DIR / "lapse_table.csv", index_col="policy_year")
    assert list(lapse["lapse_rate"])[:4] == [0.06, 0.04, 0.04, 0.03]
    assert set(lapse["lapse_rate"]) == {0.06, 0.04, 0.03}
    assert any("Stornoquote" in str(v) for v in lapse["provenance"])
    freq = pd.read_csv(PRODUCT_DIR / "freq_loading_table.csv", index_col="prem_freq")
    assert list(freq["prem_freq_load"]) == [1.0, 1.02, 1.03, 1.05]
    assert list(freq["instalments"]) == [1, 2, 4, 12]
    # The three schedule files are keyed on the contractual 1-based ``policy_year``, which
    # the monthly frame does not move: the readers map through ``policy_year(t)``.
    benefit = pd.read_csv(PRODUCT_DIR / "benefit_schedule.csv",
                          index_col=["schedule_id", "policy_year"])
    assert set(benefit.index.get_level_values(0)) == {
        "konstant", "linear_fallend", "annuitaet_fallend_3pct"}
    assert float(benefit.at[("linear_fallend", 20), "benefit_factor"]) == 0.05
    nvg = pd.read_csv(PRODUCT_DIR / "nvg_schedule.csv", index_col=["nvg_id", "policy_year"])
    assert set(nvg.xs("keine")["sum_uplift"]) == {1.0}
    assert float(nvg.at[("nvg_zwei_erhoehungen", 6), "sum_uplift"]) == 1.2
    assert float(nvg.at[("nvg_zwei_erhoehungen", 12), "sum_uplift"]) == 1.4
    for table in (mort, lapse, freq, benefit, nvg):
        assert all(str(v).startswith("[std]") for v in table["provenance"])
    # The model point table is the one file exempt from the provenance rule.
    points = pd.read_csv(PRODUCT_DIR / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns
    assert len(points) == 14 and points.loc[1, "policy_id"] == "RLV-000001"


def test_an_input_can_be_swapped_without_touching_formulas():
    """What a production user does with a company or licensed basis.  On a German term
    product the swap moves **both** premiums as well as the claims, because the tariff is
    struck off the same table the projection uses, one order up.
    """
    import pandas as pd

    lighter = pd.read_csv(PRODUCT_DIR / "mort_table.csv",
                          index_col=["table_id", "sex", "smoker", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5
    model = mx.read_model(MODEL_DIR, name="RLV_DE_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            swapped = model.Projection[1].result_cf()
            assert swapped["claims_death"].sum() < base["claims_death"].sum()
            assert swapped["prem_gross"].sum() < base["prem_gross"].sum()
            assert swapped["premiums"].sum() < base["premiums"].sum()
            # The mechanic is unchanged: the ratio is nearly invariant to the level.
            ratio_base = base["premiums"].sum() / base["prem_gross"].sum()
            ratio_swap = swapped["premiums"].sum() / swapped["prem_gross"].sum()
            assert abs(ratio_base - ratio_swap) < 0.03
            assert model.Projection[1].check_net_cf() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="RLV_DE_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()
    for csv in PRODUCT_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)
    reread = mx.read_model(dest, name="RLV_DE_S_rt")
    try:
        p = reread.Projection[1]
        ann = p.result_cf_annual()
        for y, row in WORKED_EXAMPLE.items():
            assert ann.loc[y, "prem_gross"] == AP(row[2], abs=CENT)
            assert ann.loc[y, "premiums"] == AP(row[3], abs=CENT)
            assert ann.loc[y, "claims_death"] == AP(row[5], abs=CENT)
            assert ann.loc[y, "net_cf"] == AP(row[8], abs=CENT)
        assert p.prem_gross_level_pp() == AP(1275.411882, abs=5e-6)
        assert "Notes symbol" in flat(reread.Projection.doc)
        assert p.check_net_cf() is True and p.check_no_cash_value() is True
    finally:
        reread.close()
    assert model_files(dest) == model_files(MODEL_DIR)
