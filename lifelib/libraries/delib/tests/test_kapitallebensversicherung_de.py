"""Golden and structural tests for KLV_DE_S.

The golden values are the worked example in
``products/kapitallebensversicherung/technical-notes.md`` ("Worked example"), which is a
**configuration** rather than a scenario: the classic German *kapitalbildende
Lebensversicherung* -- the *gemischte Versicherung auf den Todes- und Erlebensfall* -- on a
male aged 37 last birthday at issue, non-smoker, written in 2026 as new business
(``duration_init = 0``, so the frame opens at ``t = 0`` on one policy). The
*Versicherungsdauer* is 25 years and the *Beitragszahlungsdauer* the same 25, so the
contract is premium-paying to the *Ablauf*, which falls at attained age **62**, the age the
income-tax half-income rule requires of a contract concluded after 31 December 2011. The
*Versicherungssumme* is 50 000 EUR with ``death_ratio = 1.00``, so the guaranteed death sum
equals the guaranteed survival sum. The *Beitrag* is annual and ``unterjaehrig_form`` is
``unecht``, so the *Ratenzahlungszuschlag* is 1.000 and inert. The *Rechnungszins* is
1.00 %, the *Höchstrechnungszins* for new business from 1 January 2025; the contract is
*gezillmert* at the 25 permille ceiling; the *Überschussverwendung* is ``ansammlung`` and
the declared-rate path is ``base``, a *laufende Verzinsung* of 2.70 % held level. There is
no *Risikozuschlag*, no opening *Überschussguthaben* and no *Beitragsfreistellung*.

**The model carries two clocks and this module asserts both.** ``t`` is the policy
**month**, 0-based from issue, so ``proj_len() = 12 * policy_term = 300`` and
``result_cf()`` covers ``t = 0 ... 299``; ``k = duration(t) = t // 12`` is the 0-based policy
year every annual cells takes, and ``policy_year(t) = k + 1`` the contractual 1-based label.
:data:`WORKED_EXAMPLE` is the notes' annual table, asserted against ``result_cf_annual()``
and keyed on ``policy_year``; :data:`MONTHS_YEAR_1` is the twelve months of policy year 1 on
the monthly frame; :data:`STATE` is the annual state of ``result_surplus()``, also keyed on
``policy_year``. The notes' annual table is the **entire** projection rather than a slice of
one, and every one of its twenty-five rows is asserted here.

**What the conversion moved, and what it did not, is asserted rather than described.** The
whole annual layer is **bit-identical** to the annual-step model this replaced -- the
*Bruttobeitrag*, the *Beitragssumme*, the Zillmer cost, all three reserves at every
duration, the § 169 value, the declared credit, the *Ansammlung* balance, the accrued
terminal share and the paid-up sum -- because the monthly decrement rates compound back to
their policy year's annual values and so leave ``pols_if`` at every anniversary where it
was. The cash flows are not identical and are not meant to be: claims fall in the month of
exit and are paid the balances standing at the **last** anniversary, maintenance accrues a
twelfth a month, and a fractionated *Beitrag* is collected on a block that has already lost
lives.

The goldens are hard-coded rather than pickled so a reviewer can compare them against the
notes by eye. Tolerances follow the precision the notes display: money to the cent,
``pols_if`` to six decimals, and the totals at full precision -- 33 365,26 EUR of premium
that way against 33 365,24 EUR if the twenty-five rounded annual cells are added.

Beyond the worked example this module asserts: the ten printed rows of the notes' state
table; the derived tariff and the notes' four independent rebuilds -- the premium from the
equivalence principle, the first anniversary's reserve by Fackler computed forwards, the
year-2 surplus credit, and the year-12 surrender payment from its three parts; the closure
identity; the *Einmalbeitrag* variant and the three *Überschussverwendung* systems; all ten
``check_*()`` cells and their residuals, including ``check_net_cf()``, this library's first
ruling, and ``check_surr_nonneg()``, which the monthly grid needed because it quotes a
*Rückkaufswert* in eleven months of each year the annual grid never priced; the shape of
``result_cf()``, both signs of the net flow, the in-force model point,
the *echte* / *unechte* frequency pair, the shipped tables' provenance, an input swap and a
round trip; and **one test per numbered modeling pitfall** -- the declared rate derived by
subtraction, the surplus base being the *Deckungskapital* at the allocation date, the zero
floor on that base shown on a pre-2015 40 permille cohort where it actually bites, three
reserves rather than one, the § 4 DeckRV cap and the § 169 Abs. 3 spreading asserted
separately, the *Stornoabzug* sparing the *Überschussguthaben*, § 161 VVG substituting
rather than forfeiting, *Beitragsfreistellung* succeeding and failing the
*Mindestversicherungsleistung* test, a paid-up policy staying in ``pols_if``, the lapse
table being [std] and not GDV's *Stornoquote*, the premium-cessation rule applied once, the
*Risikozuschlag* reaching the pricing death leg and nothing else, one first-order table
serving both legs, the two mortality bases kept apart, the surplus systems' maturity/death
asymmetry, the *Zahlbeitrag* not being guaranteed, ``sex`` never reaching the premium, and
the *Ablauf* year carrying no surrender.

The whole-model-point-table sweep lives in ``test_model_conventions_de.py``, which owns the
library's single sweep; this module touches individual model points by name only.
"""
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB

CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["KLV_DE_S"][0]
PRODUCT_DIR = MODEL_DIR.parent

# The seven external CSVs, the annuallife/TradLife_A layout.
INPUT_CSVS = {
    "model_point_table.csv", "mort_table.csv", "lapse_table.csv",
    "surplus_rate_table.csv", "cost_table.csv", "freq_loading_table.csv",
    "deckrv_table.csv",
}

# The notes' worked-example table, in full, on the **annual** view result_cf_annual():
# policy_year -> (attained age, pols_if, premiums, claims_death, claims_maturity,
# claims_lapse, expenses, commissions, net_cf).  `expenses` excludes commission, so the six
# flow columns sum to net_cf.  `pols_if` is the count at the start of the policy year, which
# is the number the annual-step model this replaced carried and is unchanged.
WORKED_EXAMPLE = {
    1:  (37, 1.000000, 2004.04,  43.08,     0.00,    2.88, 350.04, 1252.53,    355.51),
    2:  (38, 0.949145, 1902.13,  44.26,     0.00,   40.88,  48.26,   28.53,   1740.20),
    3:  (39, 0.900810, 1805.26,  45.90,     0.00,   86.60,  45.20,   27.08,   1600.47),
    4:  (40, 0.868365, 1740.24,  49.00,     0.00,  142.18,  44.30,   26.10,   1478.66),
    5:  (41, 0.837014, 1677.41,  51.41,     0.00,  195.02,  43.41,   25.16,   1362.41),
    6:  (42, 0.806716, 1616.69,  54.04,     0.00,  251.21,  42.54,   24.25,   1244.66),
    7:  (43, 0.777431, 1558.00,  56.89,     0.00,  293.79,  41.68,   23.37,   1142.27),
    8:  (44, 0.749121, 1501.27,  60.00,     0.00,  334.28,  40.84,   22.52,   1043.63),
    9:  (45, 0.721747, 1446.41,  63.83,     0.00,  213.02,  38.97,   21.70,   1108.90),
    10: (46, 0.706081, 1415.02,  68.58,     0.00,  237.51,  38.78,   21.23,   1048.91),
    11: (47, 0.690646, 1384.08,  73.79,     0.00,  268.03,  38.60,   20.76,    982.91),
    12: (48, 0.675431, 1353.59,  78.01,     0.00,  876.44,  40.95,   20.30,    337.88),
    13: (49, 0.633469, 1269.50,  82.09,     0.00,  378.76,  36.95,   19.04,    752.66),
    14: (50, 0.616105, 1234.70,  88.23,     0.00,  404.57,  36.56,   18.52,    686.82),
    15: (51, 0.599079, 1200.58,  94.94,     0.00,  429.56,  36.17,   18.01,    621.91),
    16: (52, 0.582376, 1167.11, 102.28,     0.00,  464.10,  35.77,   17.51,    547.45),
    17: (53, 0.565979, 1134.25, 110.30,     0.00,  487.85,  35.37,   17.01,    483.71),
    18: (54, 0.549875, 1101.97, 119.08,     0.00,  510.74,  34.97,   16.53,    420.66),
    19: (55, 0.534048, 1070.25, 128.67,     0.00,  532.76,  34.56,   16.05,    358.22),
    20: (56, 0.518483, 1039.06, 139.15,     0.00,  553.89,  34.14,   15.59,    296.29),
    21: (57, 0.503165, 1008.36, 150.61,     0.00,  574.14,  33.71,   15.13,    234.78),
    22: (58, 0.488079,  978.13, 163.12,     0.00,  593.48,  33.28,   14.67,    173.58),
    23: (59, 0.473210,  948.33, 176.78,     0.00,  611.91,  32.84,   14.22,    112.58),
    24: (60, 0.458543,  918.94, 191.69,     0.00,  629.39,  32.39,   13.78,     51.69),
    25: (61, 0.444064,  889.92, 210.36, 28750.90,    0.00,  83.85,   13.35, -28168.54),
}

# The twelve months of policy year 1 on the monthly frame -- the view the annual grid could
# not show.  t -> (pols_if, premiums, claims_death, claims_maturity, claims_lapse, expenses,
# commissions, net_cf).  Month 0 collects the whole year's *Beitrag* on this annual
# *Zahlweise* cell and bears the acquisition cost and the initial commission; the other
# eleven collect nothing, carry a death claim and a twelfth of the maintenance expense, and
# -- the conversion's signature -- pay a surrender **nothing guaranteed**, the § 169 value at
# issue on a *gezillmert* contract being zero.  Only month 11, the anniversary, carries a
# surrender claim at all.
MONTHS_YEAR_1 = {
    0:  (1.000000, 2004.04, 3.68, 0.00, 0.00, 304.27, 1252.53, 443.57),
    1:  (0.995660,    0.00, 3.66, 0.00, 0.00,   4.25,    0.00,  -7.91),
    2:  (0.991339,    0.00, 3.64, 0.00, 0.00,   4.23,    0.00,  -7.88),
    3:  (0.987036,    0.00, 3.63, 0.00, 0.00,   4.22,    0.00,  -7.84),
    4:  (0.982753,    0.00, 3.61, 0.00, 0.00,   4.20,    0.00,  -7.81),
    5:  (0.978487,    0.00, 3.60, 0.00, 0.00,   4.18,    0.00,  -7.78),
    6:  (0.974241,    0.00, 3.58, 0.00, 0.00,   4.16,    0.00,  -7.74),
    7:  (0.970012,    0.00, 3.57, 0.00, 0.00,   4.14,    0.00,  -7.71),
    8:  (0.965803,    0.00, 3.55, 0.00, 0.00,   4.12,    0.00,  -7.68),
    9:  (0.961611,    0.00, 3.54, 0.00, 0.00,   4.11,    0.00,  -7.64),
    10: (0.957438,    0.00, 3.52, 0.00, 0.00,   4.09,    0.00,  -7.61),
    11: (0.953282,    0.00, 3.51, 0.00, 2.88,   4.07,    0.00, -10.46),
}

# The notes' Total row, summed at full precision and then rounded.
TOTALS = {
    "pols_if": 16.648981, "premiums": 33365.26, "claims_death": 2446.09,
    "claims_maturity": 28750.90, "claims_lapse": 9112.99, "expenses": 1314.12,
    "commissions": 1722.94, "net_cf": -9981.79,
}

# The four columns where adding the *printed* annual cells gives a different answer, and what
# it gives.  The notes say so in as many words; this is that sentence as an assertion.
ROUNDED_CELL_TOTALS = {
    "pols_if": 16.648982, "premiums": 33365.24, "expenses": 1314.13,
    "net_cf": -9981.78,
}

# The annual-step model's own totals for the four cash flow columns the conversion moved,
# kept as the cross-check the notes print beside the new ones.
ANNUAL_GRID_TOTALS = {
    "claims_death": 2506.85, "claims_lapse": 10104.99, "expenses": 1327.88,
    "net_cf": -11048.31,
}

# The notes' state table at the ten policy years it prints, on result_surplus():
# policy_year -> (res_pp, surplus_base_pp, surplus_credit_pp, av_sur_pp, term_bonus_pp,
# surr_value_pp at that year's anniversary).  **Every value here is bit-identical to the
# annual-step model's**: the whole annual layer is untouched by the conversion.
STATE = {
    1:  (-1252.53,   570.75,   9.70,     0.00,    0.00,   708.73),
    2:  (  570.75,  2410.10,  40.97,     9.70,    2.28,  2590.38),
    3:  ( 2410.10,  4265.63,  72.52,    50.94,   11.92,  4518.89),
    5:  ( 6137.47,  8025.74, 136.44,   232.53,   53.54,  8521.62),
    10: (15747.00, 17720.63, 301.25,  1321.31,  290.92, 18779.50),
    12: (19712.27, 21722.40, 369.28,  2038.12,  440.65, 23755.21),
    15: (25800.39, 27869.68, 473.78,  3450.48,  725.75, 31007.41),
    20: (36372.42, 38561.55, 655.55,  6811.60, 1367.70, 45521.12),
    24: (45313.89, 47636.03, 809.81, 10540.47, 2038.44, 58136.33),
    25: (47636.03, 50000.00, 850.00, 11634.87, 2228.98, 61549.01),
}

# The derived tariff of the anchor cell, at the precision the notes print it. The
# *Bruttobeitrag* is not a model point column: no German endowment rate card is public.
TARIFF = {
    "prem_gross_pp": 2004.0420, "beitragssumme": 50101.05, "alpha_cost": 1252.5263,
    "prem_net_level_pp": 1811.1493, "prem_zill_pp": 1868.9208,
    "pv_death_1st": 3611.698493, "pv_maturity_1st": 35655.282574,
    "pv_benefit_1st": 39266.981067, "ann_due_prem_1st": 21.680698,
    "ann_due_term_1st": 21.680698,
}

# The notes' closure split of the original policy.
# The maturing cohort is the annual-step model's own figure to the last digit -- it is a
# survivorship the two grids share, lapse being zero through the whole final policy year.
# The split between deaths and surrenders moved by 0.00054, which is what interleaving the
# two decrements monthly genuinely changes.
CLOSURE = {"deaths": 0.04355790, "lapses": 0.51566656, "maturities": 0.44077554}

# The *Einmalbeitrag* variant, model point 2 -- the anchor cell with prem_term = 1 and
# nothing else: t -> (pols_if, premiums, claims_death, claims_maturity, claims_lapse,
# expenses, commissions, net_cf).
EINMALBEITRAG = {
    1:  (1.000000, 43273.05,  43.19,     0.00,  147.82, 350.04, 1081.83,  41650.17),
    2:  (0.949145,     0.00,  45.68,     0.00, 1728.58,  48.26,    0.00,  -1822.52),
    3:  (0.900810,     0.00,  48.10,     0.00, 1181.37,  45.20,    0.00,  -1274.68),
    24: (0.458543,     0.00, 236.84,     0.00,  813.28,  32.39,    0.00,  -1082.51),
    25: (0.444064,     0.00, 260.17, 35570.54,    0.00,  83.85,    0.00, -35914.55),
}
EINMALBEITRAG_TOTALS = {
    "pols_if": 16.648981, "premiums": 43273.05, "claims_death": 2894.48,
    "claims_maturity": 35570.54, "claims_lapse": 22825.77, "expenses": 1314.12,
    "commissions": 1081.83, "net_cf": -20413.68,
}

# The notes' Überschussverwendung comparison: point -> (surplus_use, maturity benefit per
# policy, death benefit per policy at t = 4 (the fifth policy year), premiums collected,
# net_cf total).
SURPLUS_SYSTEMS = {
    1: ("ansammlung",          65227.99, 50460.89, 33365.26,  -9981.79),
    8: ("bonus",               63562.77, 50532.10, 33365.26,  -8089.89),
    9: ("beitragsverrechnung", 52428.98, 50085.64, 28016.10,  -8318.08),
}


def model_files(folder):
    """The model's own file names, ignoring ``__pycache__``, which is not part of it."""
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def variant_model(tmp_path, name, edits):
    """A copy of the whole product directory with its CSVs rewritten, read as a model.

    Three pitfalls concern behaviour the *shipped* parameters deliberately do not exhibit --
    the negative-reserve guard, inert at the post-2015 25 permille ceiling, and two
    invariances needing an otherwise-identical model point. Inputs are external, so a copy
    of the parent is a complete model, and copying keeps the shipped directory clean if a
    test fails mid-way. Each ``(filename, old, new)`` substitution is asserted to match, so
    a CSV edited upstream fails loudly instead of silently testing nothing.
    """
    dest = tmp_path / PRODUCT_DIR.name
    shutil.copytree(PRODUCT_DIR, dest,
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.md"))
    for filename, old, new in edits:
        path = dest / filename
        text = path.read_text(encoding="utf-8")
        assert old in text, f"{filename}: {old!r} no longer present"
        path.write_text(text.replace(old, new), encoding="utf-8")
    return mx.read_model(dest / MODEL_DIR.name, name=name)


# --- The worked example ------------------------------------------------------

@pytest.mark.parametrize("y", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_klv_anchor, y):
    """Every cell of the notes' twenty-five-row annual table, to the displayed precision.

    Read off ``result_cf_annual()``, which regroups the monthly frame rather than
    reprojecting it, and keyed on the contractual 1-based policy year.  ``pols_if`` is the
    count at the **start** of the policy year -- the number the annual-step model carried on
    the same row, and unchanged by the conversion.
    """
    age, pols_if, prem, cd, cm, cl, exp, comm, net = WORKED_EXAMPLE[y]
    p = de_klv_anchor
    t0 = 12 * (y - 1)
    assert p.age(t0) == age and p.age_y(y - 1) == age
    assert p.duration(t0) == y - 1
    assert p.policy_year(t0) == y and p.policy_year(t0 + 11) == y
    row = p.result_cf_annual().loc[y]
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_maturity"] == pytest.approx(cm, abs=CENT)
    assert row["claims_lapse"] == pytest.approx(cl, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["commissions"] == pytest.approx(comm, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)
    assert row["liability_cf"] == pytest.approx(-net, abs=CENT)


@pytest.mark.parametrize("t", sorted(MONTHS_YEAR_1))
def test_the_twelve_months_of_policy_year_one(de_klv_anchor, t):
    """The monthly frame inside policy year 1 -- the view the annual grid could not show.

    Month 0 collects the whole year's *Beitrag* on this annual *Zahlweise* cell and bears
    the acquisition cost and the initial commission; months 1 to 11 collect nothing and carry
    a death claim and a twelfth of the maintenance expense.  **Only month 11 carries a
    surrender claim**, because the § 169 value standing in the first eleven months is the one
    struck at issue, which on a *gezillmert* contract is zero.
    """
    pols_if, prem, cd, cm, cl, exp, comm, net = MONTHS_YEAR_1[t]
    p = de_klv_anchor
    assert p.age(t) == 37 and p.duration(t) == 0 and p.policy_year(t) == 1
    assert p.is_anniv(t) == (t == 11)
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "MATURITY") == pytest.approx(cm, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    # The guaranteed leg of a surrender is nil for the whole first policy year, and the
    # § 169 value struck at the first anniversary appears only in month 11.
    assert p.res_guar_close_pp(t) == pytest.approx(0.0 if t < 11 else 776.70, abs=CENT)
    assert p.surr_value_pp(t) == pytest.approx(0.0 if t < 11 else 708.73, abs=CENT)
    assert p.prem_due(t) == (t == 0)


def test_the_annual_view_regroups_the_monthly_frame_rather_than_reprojecting_it(
        de_klv_anchor):
    """``result_cf_annual()`` is the same numbers, grouped: every cash flow column is the sum
    of that policy year's twelve months and ``pols_if`` is the count at its start.  A second
    projection on an annual grid would not satisfy both at once.
    """
    p = de_klv_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert len(df) == 300 and len(ann) == 25
    assert list(ann.index) == list(range(1, 26)) and ann.index.name == "policy_year"
    for y in (1, 12, 25):
        months = df.loc[12 * (y - 1):12 * y - 1]
        for column in ("premiums", "claims_death", "claims_lapse", "expenses",
                       "commissions", "net_cf"):
            assert ann.loc[y, column] == pytest.approx(months[column].sum(), rel=1e-12), (
                y, column)
        assert ann.loc[y, "pols_if"] == pytest.approx(p.pols_if(12 * (y - 1)), rel=1e-15)
    for column in df.columns:
        if column != "pols_if":
            assert ann[column].sum() == pytest.approx(df[column].sum(), rel=1e-12), column


def test_the_worked_example_frame_matches_the_cells(de_klv_anchor):
    """result_cf() publishes the same numbers the cells do, row for row.

    Asserted separately because ``check_net_cf()`` reads the *frame*: a column dropped,
    renamed or mis-signed on the way into it leaves every cells assertion above passing.
    """
    df = de_klv_anchor.result_cf()
    assert list(df.index) == list(range(300))
    for t, row in MONTHS_YEAR_1.items():
        assert df.loc[t, "pols_if"] == pytest.approx(row[0], abs=SIX_DP)
        assert df.loc[t, "premiums"] == pytest.approx(row[1], abs=CENT)
        assert df.loc[t, "claims_death"] == pytest.approx(row[2], abs=CENT)
        assert df.loc[t, "claims_maturity"] == pytest.approx(row[3], abs=CENT)
        assert df.loc[t, "claims_lapse"] == pytest.approx(row[4], abs=CENT)
        assert df.loc[t, "expenses"] == pytest.approx(row[5], abs=CENT)
        assert df.loc[t, "commissions"] == pytest.approx(row[6], abs=CENT)
        assert df.loc[t, "net_cf"] == pytest.approx(row[7], abs=CENT)


def test_the_worked_example_totals_are_summed_at_full_precision(de_klv_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells.

    On this cell the two differ in three columns and in ``pols_if``, by one or two cents:
    twenty-five roundings of at most half a cent each. Both are asserted, because "summed
    at full precision" is a convention a reader can only check against the alternative.

    The monthly frame totals to the same money as the annual view, the grouping being a
    regrouping; and the four columns the conversion moved are asserted against the
    annual-step model's own totals, so that what changed is on the record rather than merely
    absent.
    """
    df = de_klv_anchor.result_cf_annual()
    for column, total in TOTALS.items():
        tol = SIX_DP if column == "pols_if" else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    printed = {"pols_if": sum(r[1] for r in WORKED_EXAMPLE.values()),
               "premiums": sum(r[2] for r in WORKED_EXAMPLE.values()),
               "expenses": sum(r[6] for r in WORKED_EXAMPLE.values()),
               "net_cf": sum(r[8] for r in WORKED_EXAMPLE.values())}
    for column, value in ROUNDED_CELL_TOTALS.items():
        tol = SIX_DP if column == "pols_if" else CENT
        assert printed[column] == pytest.approx(value, abs=tol), column
        assert printed[column] != pytest.approx(TOTALS[column], abs=tol / 10), column
    monthly = de_klv_anchor.result_cf()
    assert monthly["net_cf"].sum() == pytest.approx(TOTALS["net_cf"], abs=CENT)
    # What the finer grid moved, against the annual grid's own totals.
    for column, old in ANNUAL_GRID_TOTALS.items():
        assert TOTALS[column] != pytest.approx(old, abs=0.5), column
        assert abs(TOTALS[column]) < abs(old) + 1e-9, column


@pytest.mark.parametrize("y", sorted(STATE))
def test_the_state_behind_the_cash_flows(de_klv_anchor, y):
    """The notes' state table: the reserve, the surplus and what a surrender would pay.

    All of it on **policy-year** arguments, ``k = y - 1``: ``res_pp(k)`` is the
    *Deckungskapital* at the **start** of policy year ``y``, ``surplus_base_pp(k)`` the same
    reserve at the **end** of it -- the *Deckungskapital* "at the allocation date" the
    declared rate multiplies -- and ``surr_value_pp`` the *Rückkaufswert* at that year's
    anniversary, month ``12k + 11``.  Every value here is bit-identical to the annual-step
    model's: the conversion did not touch the annual layer.
    """
    res, base, credit, av_sur, term, surr = STATE[y]
    p = de_klv_anchor
    k = y - 1
    assert p.res_pp(k) == pytest.approx(res, abs=CENT)
    assert p.surplus_base_pp(k) == pytest.approx(base, abs=CENT)
    assert p.surplus_credit_pp(k) == pytest.approx(credit, abs=CENT)
    assert p.av_sur_pp(k) == pytest.approx(av_sur, abs=CENT)
    assert p.term_bonus_pp(k) == pytest.approx(term, abs=CENT)
    assert p.surr_value_pp(12 * k + 11) == pytest.approx(surr, abs=CENT)
    row = p.result_surplus().loc[y]
    assert row["res_pp"] == pytest.approx(res, abs=CENT)
    assert row["surplus_base_pp"] == pytest.approx(base, abs=CENT)
    assert row["surr_value_pp"] == pytest.approx(surr, abs=CENT)
    # A surrender in the eleven other months is paid the value struck at the LAST
    # anniversary, which is the previous row of this very table.
    if k > 0:
        assert p.surr_value_pp(12 * k) < p.surr_value_pp(12 * k + 11)
        assert p.res_guar_close_pp(12 * k) == pytest.approx(
            p.res_guar_pp(k - 1), rel=1e-15)


def test_the_two_rows_that_carry_the_product(de_klv_anchor):
    """At t = 0 the reserve is exactly -alpha_cost; at t = 24 the closing reserve is SE.

    The first is the arithmetic of *Zillmerung* and the reason § 169 Abs. 3 VVG needs a
    floor at all. The second is what an endowment *is*: the last policy year's
    *Deckungskapital* **is** the *Erlebensfallleistung*.
    """
    p = de_klv_anchor
    assert p.res_pp(0) == pytest.approx(-p.alpha_cost(), rel=1e-12)
    assert p.res_pp(0) == pytest.approx(-1252.5263, abs=CENT)
    assert p.res_net_pp(0) == pytest.approx(0.0, abs=1e-9)  # the equivalence, as a reserve
    assert p.surplus_base_pp(0) == pytest.approx(570.75, abs=CENT)
    assert p.res_pp_at(24, "AFT_INT") == pytest.approx(50000.00, abs=CENT)
    assert p.res_pp(25) == pytest.approx(p.sum_assured(), abs=1e-6)


def test_the_derived_tariff(de_klv_anchor):
    """The *Bruttobeitrag* is derived, not given, and the two annuities coincide here."""
    p = de_klv_anchor
    for name, value in TARIFF.items():
        got = getattr(p, name)()
        tol = CENT if abs(value) > 100 else 5e-7
        assert got == pytest.approx(value, abs=max(tol, abs(value) * 1e-9)), name
    assert "prem_gross_pp" not in p.model_point().index
    assert p.beitragssumme() == pytest.approx(p.prem_gross_pp() * p.prem_term(), rel=1e-12)
    assert p.ann_due_prem_1st() == pytest.approx(p.ann_due_term_1st(), rel=1e-15)


def test_the_bruttobeitrag_rebuilt_from_the_equivalence(de_klv_anchor):
    """The notes' first independent check, in arithmetic a reader can follow.

    Numerator 39 266,981067 + 0,0015 x 50 000 x 21,680698 = 40 893,033435; denominator
    0,97 x 21,680698 - 0,025 x 25 = 20,405277; the quotient is 2 004,0420 EUR. The rebuild
    runs on the notes' **printed** figures rather than on the model's own, which is the
    point of it, so the tolerances are those of a six-figure annuity factor.
    """
    p = de_klv_anchor
    numerator = 39266.981067 + 0.0015 * 50000 * 21.680698
    denominator = 0.97 * 21.680698 - 0.025 * 25
    assert numerator == pytest.approx(40893.033435, abs=5e-5)
    assert denominator == pytest.approx(20.405277, abs=5e-7)
    assert numerator / denominator == pytest.approx(2004.0420, abs=1e-4)
    assert p.prem_gross_pp() == pytest.approx(numerator / denominator, rel=1e-7)
    assert p.prem_net_level_pp() == pytest.approx(39266.981067 / 21.680698, abs=5e-4)
    assert p.prem_zill_pp() == pytest.approx(1811.1493 + 1252.5263 / 21.680698, abs=5e-4)
    assert p.prem_zill_pp() - p.prem_net_level_pp() == pytest.approx(57.7715, abs=5e-5)
    assert p.check_equivalence() is True
    assert p.check_equivalence_resid(0) == pytest.approx(0.0, abs=1e-8)


def test_the_first_anniversary_reserve_by_fackler(de_klv_anchor):
    """The notes' second check: the reserve rebuilt forwards, not as a present value.

    (-1 252,5263 + 1 868,9208) x 1,01 = 622,5584; deduct the death outgo
    0,001048144253 x 50 000 = 52,4072; divide 570,1512 by the survivors 0,998951856. It
    holds only if the premium, the first-order mortality, the *Rechnungszins* and the
    prospective formula are mutually consistent.
    """
    p = de_klv_anchor
    q1 = p.mort_rate_at_age(37)
    assert q1 == pytest.approx(0.001048144253, abs=5e-13)
    rolled = (-1252.5263 + 1868.9208) * 1.01
    assert rolled == pytest.approx(622.5584, abs=5e-5)
    assert q1 * 50000.0 == pytest.approx(52.4072, abs=5e-5)
    assert (rolled - q1 * 50000.0) / (1.0 - q1) == pytest.approx(570.7495, abs=5e-4)
    assert p.res_pp(1) == pytest.approx(570.7495, abs=5e-4)
    assert p.res_pp_at(0, "AFT_INT") == pytest.approx(p.res_pp(1), rel=1e-12)
    assert p.check_res_roll_fwd() is True


def test_the_year_two_surplus_credit_and_the_ansammlung_it_builds(de_klv_anchor):
    """The notes' third check: 1,70 pp on the year's *closing* reserve.

    2,70 % declared less a 1,00 % guarantee is 1,70 pp, derived by subtraction and never
    added on top. 0,017 x 2 410,101960 = 40,9717 EUR; the balance then compounds at
    ``ans_rate`` and the terminal share accrues on the same base. Policy year 2 is the
    **policy year** ``k = 1``, and every figure here is unmoved by the monthly grid.
    """
    p = de_klv_anchor
    assert p.decl_rate(1) == 0.0270 and p.rechnungszins() == 0.0100
    assert p.zins_ueberschuss_rate(1) == pytest.approx(0.0170, abs=1e-15)
    assert p.surplus_base_pp(1) == pytest.approx(2410.101960, abs=5e-5)
    assert p.surplus_credit_pp(1) == pytest.approx(0.017 * 2410.101960, abs=5e-5)
    assert p.surplus_credit_pp(1) == pytest.approx(40.9717, abs=5e-5)
    assert p.av_sur_pp(2) == pytest.approx(9.702741 * 1.027 + 40.971733, abs=5e-5)
    assert p.av_sur_pp(2) == pytest.approx(50.9364, abs=5e-4)
    assert p.term_bonus_pp(2) == pytest.approx(2.282998 + 0.004 * 2410.101960, abs=5e-5)
    assert p.term_bonus_pp(2) == pytest.approx(11.9234, abs=5e-4)
    assert p.check_surplus_roll_fwd() is True


def test_the_year_twelve_surrender_payment_from_its_three_parts(de_klv_anchor):
    """The notes' fourth check: the one row where all three rules bite at once.

    **Policy year 12 is ``k = 11``, months 132 to 143.** Amount: the § 169 value is the
    **floor** ``res_min_pp(12)`` = 22 413,4564 EUR, exceeding the Zillmer reserve by
    691,06 EUR; the 5 % *Stornoabzug* applies to that and nothing else; the
    *Überschussguthaben* is added **undeducted**.  That is the value a surrender **at the
    anniversary**, month 143, is paid.

    Count: 0,675431 in force at the start of the year, decremented month by month at the
    6,0 % spike the twelve-year tax threshold produces, which over the twelve months gives
    0,04047664 surrenders -- against 0,04043417 on the annual grid, the difference being the
    monthly interleaving of the two decrements.

    And the conversion's own point: the eleven non-anniversary months are paid the value
    struck at the **last** anniversary, 21 467,9479 EUR, not this one.  That is what takes
    the year's surrender claims from 960,52 EUR on the annual grid to 876,44 EUR here.
    """
    p = de_klv_anchor
    k, t_anniv = 11, 12 * 11 + 11
    lapses = sum(p.pols_lapse(t) for t in range(12 * k, 12 * k + 12))
    assert lapses == pytest.approx(0.04047664, abs=5e-9)
    assert p.mort_rate(12 * k) == pytest.approx(0.00226204, abs=5e-9)
    assert p.lapse_rate(12 * k) == 0.06 and p.storno_rate(k) == 0.05
    assert p.lapse_rate_mth(12 * k) == pytest.approx(
        1.0 - 0.94 ** (1.0 / 12.0), abs=5e-12)
    assert p.res_min_pp(12) == pytest.approx(22413.4564, abs=CENT)
    assert p.res_zill_pp(12) == pytest.approx(21722.3990, abs=CENT)
    assert p.res_min_pp(12) - p.res_zill_pp(12) == pytest.approx(691.06, abs=CENT)
    assert p.res_guar_pp(k) == pytest.approx(22413.4564, abs=CENT)
    assert 22413.4564 * 0.95 == pytest.approx(21292.7836, abs=CENT)
    assert p.av_sur_pp_at(k, "AFT_CREDIT") == pytest.approx(2462.4255, abs=CENT)
    assert p.surr_value_pp(t_anniv) == pytest.approx(21292.7836 + 2462.4255, abs=CENT)
    assert p.surr_value_pp(t_anniv) == pytest.approx(23755.2091, abs=CENT)
    # The eleven other months are paid the previous anniversary's value.
    assert p.surr_value_pp(12 * k) == pytest.approx(21467.9479, abs=CENT)
    assert p.res_guar_close_pp(12 * k) == pytest.approx(p.res_guar_pp(k - 1), rel=1e-15)
    assert p.result_cf_annual().loc[12, "claims_lapse"] == pytest.approx(876.4406, abs=CENT)


def test_the_cash_flow_statement_closes_row_by_row(de_klv_anchor):
    """The notes rebuild policy year 12's net_cf from the six flow columns; check_net_cf()
    does every month.  Policy year 12 is ``k = 11``, months 132 to 143."""
    p = de_klv_anchor
    rebuilt = 1353.591433 - 78.012539 - 0.0 - 876.440599 - 40.954555 - 20.303871
    assert rebuilt == pytest.approx(337.879869, abs=5e-6)
    assert p.result_cf_annual().loc[12, "net_cf"] == pytest.approx(337.879869, abs=5e-6)
    assert p.check_net_cf() is True
    assert all(p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)
               for t in range(0, 300, 7))


def test_the_decrements_close_three_ways(de_klv_anchor):
    """Deaths, surrenders and maturities sum to exactly the original policy.

    There is no fourth term: the *Ablauf* falls at the end of the last policy year
    ``t = proj_len() - 1``, so the survivors of that year's mortality all leave as a maturity
    and nothing is carried past it. ``check_decrement_closure()`` builds the same sum by
    direct summation over the exit cells, with no reference to the recursion that produced
    ``pols_if``.
    """
    p = de_klv_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    maturities = sum(p.pols_maturity(t) for t in range(n))
    assert deaths == pytest.approx(CLOSURE["deaths"], abs=5e-9)
    assert lapses == pytest.approx(CLOSURE["lapses"], abs=5e-9)
    assert maturities == pytest.approx(CLOSURE["maturities"], abs=5e-9)
    assert deaths + lapses + maturities == pytest.approx(1.0, abs=1e-12)
    assert p.pols_if(n) == pytest.approx(maturities, rel=1e-12)
    assert p.check_decrement_closure() is True and p.check_pols_roll_fwd() is True


# --- The two variants the notes print ----------------------------------------

@pytest.mark.parametrize("y", sorted(EINMALBEITRAG))
def test_the_einmalbeitrag_variant_row(kapitallebensversicherung, y):
    """Model point 2 is the anchor cell with prem_term = 1 and nothing else.

    The single premium falls in month 0 and nowhere else, which is what
    ``duration(t) < prem_term()`` says once the frame counts months.
    """
    pols_if, prem, cd, cm, cl, exp, comm, net = EINMALBEITRAG[y]
    p = kapitallebensversicherung.Projection[2]
    row = p.result_cf_annual().loc[y]
    assert p.prem_term() == 1 and p.ann_due_prem_1st() == 1.0
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_maturity"] == pytest.approx(cm, abs=CENT)
    assert row["claims_lapse"] == pytest.approx(cl, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["commissions"] == pytest.approx(comm, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)
    if y == 1:
        assert p.premiums(0) == pytest.approx(prem, abs=CENT)
        assert all(p.premiums(t) == 0.0 for t in range(1, 300))


def test_the_einmalbeitrag_reverses_the_reserve_ordering(kapitallebensversicherung):
    """On a single premium the § 169 floor is **slack** from the first anniversary.

    39 648,80 EUR of Zillmer reserve against a 38 783,34 EUR floor -- the reverse of the
    level-premium ordering, a single premium leaving almost nothing to amortise. That is the
    correct answer, not a degenerate case, and it is why the model publishes all three
    constructions rather than assuming which one wins. The two forms' undiscounted totals
    are *not* comparable: the equivalence holds in present value on tariff survivorship.
    """
    p = kapitallebensversicherung.Projection[2]
    assert p.beitragssumme() == pytest.approx(p.prem_gross_pp(), rel=1e-12)
    assert p.prem_gross_pp() == pytest.approx(43273.05, abs=CENT)
    assert p.alpha_cost() == pytest.approx(1081.83, abs=CENT)
    assert p.res_zill_pp(1) == pytest.approx(39648.80, abs=CENT)
    assert p.res_min_pp(1) == pytest.approx(38783.34, abs=CENT)
    assert p.res_zill_pp(1) > p.res_min_pp(1)
    assert p.res_guar_pp(0) == pytest.approx(p.res_zill_pp(1), rel=1e-12)
    df = p.result_cf_annual()
    for column, total in EINMALBEITRAG_TOTALS.items():
        tol = SIX_DP if column == "pols_if" else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert p.benefit_maturity_pp(p.proj_len() - 1) == pytest.approx(80699.89, abs=CENT)
    assert df["claims_lapse"].sum() > 2.4 * TOTALS["claims_lapse"]


@pytest.mark.parametrize("point_id", sorted(SURPLUS_SYSTEMS))
def test_the_three_ueberschussverwendung_systems(kapitallebensversicherung, point_id):
    """Model points 1, 8 and 9 differ in ``surplus_use`` alone; the notes' table."""
    use, maturity, death5, premiums, net = SURPLUS_SYSTEMS[point_id]
    p = kapitallebensversicherung.Projection[point_id]
    assert p.surplus_use() == use
    assert p.benefit_maturity_pp(p.proj_len() - 1) == pytest.approx(maturity, abs=CENT)
    # The fifth policy year's **anniversary** death benefit, month 59: that is the instant
    # the annual-step model priced, and it is unchanged.
    assert p.benefit_death_pp(59) == pytest.approx(death5, abs=CENT)
    # A death earlier in that year is paid the balances of the previous anniversary, so it
    # is strictly smaller -- the conversion's rule, visible on every system.
    assert p.benefit_death_pp(48) < p.benefit_death_pp(59)
    df = p.result_cf()
    assert df["premiums"].sum() == pytest.approx(premiums, abs=CENT)
    assert df["net_cf"].sum() == pytest.approx(net, abs=CENT)
    assert p.check_surplus_roll_fwd() is True


# --- Pitfall 1: the declared rate is a total, not an add-on -------------------

def test_the_interest_surplus_is_derived_by_subtraction(kapitallebensversicherung,
                                                        de_klv_anchor):
    """The *laufende Verzinsung* **is** the guarantee plus the interest surplus.

    A declared 2,70 % on a 1,00 % guarantee is a **1,70 pp** credit, never 2,70 pp on top of
    1,00 pp. The outer ``max`` is the other half: on the ``nil`` path the declared rate falls
    **below** the guarantee, which the reserve roll-forward still meets in full, so the
    surplus is zero rather than negative.
    """
    p = de_klv_anchor
    for t in range(25):
        assert p.zins_ueberschuss_rate(t) == pytest.approx(
            max(0.0, p.decl_rate(t) - p.rechnungszins()), abs=1e-15)
    assert p.zins_ueberschuss_rate(0) == pytest.approx(0.017, abs=1e-15)
    assert p.zins_ueberschuss_rate(0) != pytest.approx(0.027, abs=1e-6)
    nil = kapitallebensversicherung.Projection[14]
    assert nil.scenario_id() == "nil"
    assert nil.decl_rate(0) == 0.0 and nil.rechnungszins() == 0.01
    assert all(nil.zins_ueberschuss_rate(t) == 0.0 for t in range(12))
    assert all(nil.surplus_credit_pp(t) == 0.0 for t in range(12))
    assert nil.check_res_roll_fwd() is True
    assert nil.res_pp(12) == pytest.approx(nil.sum_assured(), abs=1e-6)


# --- Pitfall 2: the base is the reserve, not the sum insured or the premium ---

def test_the_surplus_base_is_the_reserve_at_the_allocation_date(de_klv_anchor):
    """A percentage of the *Deckungskapital* calculated at the allocation date.

    The same rate on ``sum_assured`` would credit 850,00 EUR in the first policy year
    (``t = 0``) instead of 9,70 EUR, and on the *Bruttobeitrag* 34,07 EUR -- two orders of
    magnitude apart early and converging only at the *Ablauf*, which is why a wrong base
    survives a late-duration spot check.
    """
    p = de_klv_anchor
    for t in range(25):
        assert p.surplus_base_pp(t) == pytest.approx(
            max(p.res_pp_at(t, "AFT_INT"), 0.0), rel=1e-12)
        assert p.surplus_credit_pp(t) == pytest.approx(
            p.zins_ueberschuss_rate(t) * p.surplus_base_pp(t), rel=1e-12)
    assert p.surplus_credit_pp(0) == pytest.approx(9.7027, abs=5e-5)
    assert p.zins_ueberschuss_rate(0) * p.sum_assured() == pytest.approx(850.0, abs=CENT)
    assert p.zins_ueberschuss_rate(0) * p.prem_gross_pp() == pytest.approx(34.07, abs=CENT)
    assert p.surplus_base_pp(24) == pytest.approx(p.sum_assured(), abs=CENT)


# --- Pitfall 3: the base is floored at zero ----------------------------------

def test_the_negative_reserve_guard(de_klv_anchor, tmp_path):
    """A positive rate on a negative base would credit a **negative** surplus.

    On the shipped 25 permille basis the guard is **inert**: the base is the *closing*
    reserve and is already +570,75 EUR in the first policy year (``t = 0``) against an
    opening -1 252,53 EUR, so asserting it on the anchor cell alone would be vacuous. The
    notes say so, and this test therefore exercises the guard directly on the pre-2015
    **40 permille** ceiling, where the closing reserve of the first year really is negative.
    """
    p = de_klv_anchor
    assert all(p.surplus_base_pp(k) >= 0.0 for k in range(25))
    assert [k for k in range(25) if p.res_pp_at(k, "AFT_INT") < 0.0] == []
    assert p.res_pp(0) < 0.0 < p.res_pp_at(0, "AFT_INT")
    model = variant_model(tmp_path, "KLV_DE_S_zill40", [
        ("cost_table.csv", "std_2026,0.0250,", "std_2026,0.0400,"),
        ("model_point_table.csv",
         "1,DE-KLV-0001,M,N,2026,37,0,1.0,25,25,50000.0,1.0,annual,unecht,0.01,1,",
         "1,DE-KLV-0001,M,N,2014,37,0,1.0,25,25,50000.0,1.0,annual,unecht,0.01,1,")])
    try:
        q = model.Projection[1]
        assert q.zillmer_max() == 0.040 and q.alpha_rate() == 0.040
        assert q.res_pp_at(0, "AFT_INT") == pytest.approx(-190.22, abs=CENT)
        assert q.surplus_base_pp(0) == 0.0 and q.surplus_credit_pp(0) == 0.0
        assert q.zins_ueberschuss_rate(0) > 0.0    # the rate is positive; the base is not
        assert [k for k in range(25) if q.res_pp_at(k, "AFT_INT") < 0.0] == [0]
        assert q.check_res_roll_fwd() is True
        assert q.check_zillmer_cap() is True
        assert q.check_surplus_roll_fwd() is True
    finally:
        model.close()


# --- Pitfall 4: three reserves, and the one the customer gets -----------------

def test_the_product_has_three_reserves_and_the_floor_normally_binds(
        kapitallebensversicherung, de_klv_anchor):
    """``res_guar_pp`` is the maximum of the two constructions and of zero.

    On a long *gezillmert* contract the § 169 Abs. 3 floor binds at **every** duration but 0
    and ``m``, so a model publishing only the Zillmer reserve as the surrender value
    understates it essentially everywhere. With ``zillmer_on = 0`` all three coincide and the
    floor is slack -- the invariance test -- and the price is unchanged, because
    ``zillmer_on`` decides where the cost sits in the reserve, not whether it is charged.
    """
    p = de_klv_anchor
    binding = 0
    for t in range(25):
        assert p.res_guar_pp(t) >= p.res_zill_pp(t + 1) - 1e-9
        assert p.res_guar_pp(t) >= p.res_min_pp(t + 1) - 1e-9
        assert p.res_guar_pp(t) >= 0.0
        if p.res_min_pp(t + 1) > p.res_zill_pp(t + 1) + 1e-6:
            binding += 1
    assert binding >= 20, "the § 169 floor should bind at almost every duration"
    assert p.res_min_pp(1) > p.res_zill_pp(1)
    assert p.res_min_pp(0) == pytest.approx(p.res_zill_pp(0), rel=1e-12)    # duration 0
    assert p.res_min_pp(25) == pytest.approx(p.res_zill_pp(25), rel=1e-12)  # duration m
    assert p.check_surr_floor() is True
    flat = kapitallebensversicherung.Projection[13]
    assert flat.zillmer_on() == 0 and flat.alpha_cost() == 0.0
    for t in (0, 1, 2, 5, 24, 25):
        assert flat.res_zill_pp(t) == pytest.approx(flat.res_net_pp(t), rel=1e-12)
        assert flat.res_min_pp(t) == pytest.approx(flat.res_net_pp(t), rel=1e-12)
    assert flat.prem_gross_pp() == pytest.approx(p.prem_gross_pp(), rel=1e-12)
    assert flat.check_surr_floor() is True


# --- Pitfall 5: the § 4 cap and the § 169 spreading are different rules -------

def test_the_zillmer_cap_and_the_surrender_floor_are_asserted_separately(
        kapitallebensversicherung, de_klv_anchor):
    """§ 4 DeckRV caps the **charge**; § 169 Abs. 3 VVG floors the **value**.

    One search summary in the research corpus states the five-year spreading and the 2,5 %
    ceiling as though both came from § 169 Abs. 3. They do not, they do different work, and
    the model asserts them through two cells against two quantities. A 2012 cohort carries
    the *pre-LVRG* ceiling for its whole term, so the cap is a cohort fact and the floor is
    not.
    """
    p = de_klv_anchor
    assert p.alpha_rate() == 0.025 and p.zillmer_max() == 0.025
    assert p.alpha_cost() == pytest.approx(0.025 * p.beitragssumme(), rel=1e-12)
    assert p.check_zillmer_cap() is True
    assert p.check_zillmer_cap_resid(0) == pytest.approx(0.0, abs=1e-9)
    for t in range(26):
        assert p.res_min_pp(t) == pytest.approx(
            p.res_net_pp(t) - p.alpha_cost() * max(0.0, 1.0 - t / 5.0), rel=1e-12)
    assert p.res_min_pp(5) == pytest.approx(p.res_net_pp(5), rel=1e-12)   # k = 5
    assert p.check_surr_floor() is True
    inforce = kapitallebensversicherung.Projection[10]
    assert inforce.issue_year() == 2012 and inforce.alpha_rate() == 0.025
    assert inforce.zillmer_max() == 0.040 and inforce.hrz_max() == 0.0175
    assert inforce.check_zillmer_cap() is True and inforce.check_surr_floor() is True


# --- Pitfall 6: the Stornoabzug bites on the guaranteed value alone -----------

def test_the_stornoabzug_spares_the_ueberschussguthaben(de_klv_anchor):
    """The only published deduction in the corpus is a percentage of the *Deckungskapital*.

    So the accumulated *Überschussguthaben* passes through **undeducted**: the surrender
    value less that balance is exactly the deducted guaranteed value. Taking the deduction on
    the whole payment would cost 123,12 EUR in policy year 12.
    ``term_surr_share = 0``, so the accrued terminal share is not paid on surrender at all.

    Asserted **in every month**, not only at anniversaries: the deduction band is a
    policy-year band and steps on the anniversary, while the value it bites on is the one
    standing at the end of the month.
    """
    p = de_klv_anchor
    for t in range(0, 300, 5):
        assert p.surr_value_pp(t) - p.av_sur_close_pp(t) == pytest.approx(
            p.res_guar_close_pp(t) * (1.0 - p.storno_rate(p.duration(t))), rel=1e-12)
    assert p.storno_rate(0) == 0.10 and p.storno_rate(11) == 0.05
    assert p.storno_rate(19) == 0.025
    # The band steps on the anniversary and nowhere else.
    assert p.storno_rate(p.duration(59)) == 0.10 and p.storno_rate(p.duration(60)) == 0.075
    t_anniv = 12 * 11 + 11
    whole = (p.res_guar_pp(11) + p.av_sur_pp_at(11, "AFT_CREDIT")) * (1.0 - 0.05)
    assert p.surr_value_pp(t_anniv) - whole == pytest.approx(0.05 * 2462.4255, abs=CENT)
    assert p.surr_value_pp(t_anniv) > whole and p.term_bonus_pp(12) > 0.0
    assert p.surr_value_pp(t_anniv) == pytest.approx(
        p.res_guar_pp(11) * 0.95 + p.av_sur_pp_at(11, "AFT_CREDIT"), rel=1e-12)


# --- Pitfall 7: § 161 VVG substitutes, it does not forfeit --------------------

def test_a_suicide_inside_three_years_is_paid_the_rueckkaufswert(de_klv_anchor):
    """The insurer is *leistungsfrei* **and** must pay the *Rückkaufswert* under § 169.

    A benefit **substitution**, not a forfeiture -- materially unlike art. L. 132-7 of the
    French code, where the cover is of no effect in the first year and there is no surrender
    value to fall back on. At the **first anniversary**, month 11, the substituted amount is
    only 708,73 EUR against a full benefit of 50 011,99 EUR, so the effect is visible in the
    numbers. The window is policy years 1 to 3, which is the **first thirty-six months** --
    its boundary falls on an anniversary because the statute measures it in years, so the
    monthly grid resolves it exactly rather than approximately.
    """
    p = de_klv_anchor
    assert p.suicide_share == 0.02
    for t in (0, 11, 12, 23, 35):
        assert p.benefit_death_pp(t) == pytest.approx(
            0.98 * p.benefit_full_pp(t) + 0.02 * p.surr_value_pp(t), rel=1e-12)
    for t in (36, 48, 143, 299):
        assert p.benefit_death_pp(t) == pytest.approx(p.benefit_full_pp(t), rel=1e-12)
    assert p.benefit_full_pp(11) == pytest.approx(50011.99, abs=CENT)
    assert p.surr_value_pp(11) == pytest.approx(708.73, abs=CENT)
    assert p.benefit_death_pp(11) == pytest.approx(49025.92, abs=CENT)
    assert 0.9 * p.sum_assured() < p.benefit_death_pp(11) < p.benefit_full_pp(11)
    # In the first eleven months there is no surrender value to substitute at all, so the
    # excluded share is paid nothing -- which is § 161 read exactly, not a forfeiture.
    assert p.surr_value_pp(0) == 0.0
    assert p.benefit_death_pp(0) == pytest.approx(0.98 * 50000.0, rel=1e-12)


# --- Pitfall 8: Beitragsfreistellung is tested, and can fail ------------------

def test_beitragsfreistellung_succeeds_on_one_point_and_fails_on_another(
        kapitallebensversicherung):
    """§ 165 VVG: below the *Mindestversicherungsleistung* the election becomes a surrender.

    Model point 11 elects at the end of year 10 on a 50 000 EUR contract and succeeds: the
    contract runs to the *Ablauf* with no further premium and a reduced sum insured, the
    paid-up sum bought at exactly the § 169 value -- which is what makes the reserve
    roll-forward still close in the election year. Model point 12 elects at the end of year 3
    on a 6 000 EUR contract, buys only 897,49 EUR against a 2 500 EUR minimum, and the
    projection terminates there with a ``claims_lapse`` payment and nothing after it.

    ``bfz_year`` is the **contractual, 1-based** policy year, so an election at the end of
    policy year ``y`` falls at the end of the 0-based policy year ``y - 1`` -- month
    ``12(y - 1) + 11`` -- and the contract is paid-up from policy year ``y`` onwards.

    **On the monthly grid the failing election is a month-specific event.** § 165 VVG makes
    it fall at the end of the election *Versicherungsperiode*, so the whole cohort leaves in
    that policy year's **last month** and in no other: ``lapse_rate`` is 1.0 for the year, and
    ``lapse_rate_mth`` is 1.0 at the anniversary and 0 in the eleven months before it.
    Spreading the annual 1.0 geometrically would have emptied the cohort in the year's first
    month, eleven months early.
    """
    ok = kapitallebensversicherung.Projection[11]
    assert ok.bfz_year() == 10
    assert ok.bfz_si_pp() == pytest.approx(21403.08, abs=CENT)
    assert ok.bfz_si_pp() >= kapitallebensversicherung.Projection.bfz_min_si
    assert ok.is_paid_up(9) is False and ok.is_paid_up(10) is True
    assert ok.bfz_fails() is False
    assert ok.prem_paid_pp(9) == pytest.approx(2004.0420, abs=CENT)
    assert all(ok.prem_paid_pp(k) == 0.0 for k in range(10, 25))
    assert all(ok.prem_inst_pp(t) == 0.0 for t in range(120, 300))
    df_ok = ok.result_cf()
    assert list(df_ok.index) == list(range(300))
    assert df_ok.loc[299, "claims_maturity"] > 0.0
    assert ok.benefit_maturity_pp(299) == pytest.approx(31621.11, abs=CENT)
    assert ok.bfz_si_pp() * ok.pu_single_prem(10) == pytest.approx(
        ok.res_guar_pp(9), rel=1e-12)
    assert ok.bfz_uplift_pp(9) == pytest.approx(779.31, abs=CENT)
    assert ok.check_res_roll_fwd() is True

    failed = kapitallebensversicherung.Projection[12]
    assert failed.bfz_year() == 3 and failed.sum_assured() == 6000.0
    assert failed.bfz_si_pp() == pytest.approx(897.49, abs=CENT)
    assert failed.bfz_si_pp() < kapitallebensversicherung.Projection.bfz_min_si
    assert failed.is_paid_up(3) is False and failed.bfz_fails() is True
    assert failed.lapse_rate(24) == 1.0            # the annual statement for policy year 3
    assert [t for t in range(24, 36) if failed.lapse_rate_mth(t) == 1.0] == [35]
    assert all(failed.lapse_rate_mth(t) == 0.0 for t in range(24, 35))
    df_bad = failed.result_cf()
    assert df_bad.loc[35, "claims_lapse"] == pytest.approx(634.72, abs=CENT)
    assert df_bad.loc[35, "claims_lapse"] == pytest.approx(
        failed.pols_lapse(35) * failed.surr_value_pp(35), rel=1e-12)
    assert (df_bad.loc[24:34, "claims_lapse"] == 0.0).all()
    assert (df_bad.loc[36:, "net_cf"] == 0.0).all()
    assert (df_bad.loc[36:, "pols_if"] == 0.0).all()
    assert df_bad["claims_maturity"].sum() == 0.0
    assert failed.check_decrement_closure() is True


# --- Pitfall 9: a paid-up policy stays in force ------------------------------

def test_a_paid_up_policy_is_not_removed_from_the_in_force(kapitallebensversicherung,
                                                           de_klv_anchor):
    """*Beitragsfreistellung* keeps the contract alive; only a *Kündigung* removes it.

    Model point 11 differs from the anchor in ``bfz_year`` alone, so its ``pols_if`` must be
    **bit-identical** at every ``t`` while the premium stops and the maturity benefit falls.
    Removing the policy instead would look plausible in every total.
    """
    ok = kapitallebensversicherung.Projection[11]
    p = de_klv_anchor
    for t in range(301):
        assert ok.pols_if(t) == p.pols_if(t), t
    assert ok.pols_lapse(120) > 0.0       # surrenders continue on a paid-up contract
    assert ok.pols_maturity(299) == pytest.approx(p.pols_maturity(299), rel=1e-12)
    assert ok.result_cf()["premiums"].sum() < p.result_cf()["premiums"].sum()
    assert ok.benefit_maturity_pp(299) < p.benefit_maturity_pp(299)
    assert ok.benefit_full_pp(143) < p.benefit_full_pp(143)
    assert ok.check_pols_roll_fwd() is True and ok.check_decrement_closure() is True


# --- Pitfall 10: the lapse table is [std], not GDV's Stornoquote --------------

def test_the_lapse_decrement_is_std_and_not_the_gdv_stornoquote(de_klv_anchor):
    """GDV's headline measure counts conversions to *beitragsfrei* **as well as** surrenders.

    So it is not a surrender rate, and a second GDV measure gives an irreconcilable 1,2 % for
    the same year. Every rate in ``lapse_table.csv`` is therefore [std] and the file says so
    on every row; only the *shape* -- suppressed approaching duration 12 and spiking at it,
    on the twelve-year income-tax threshold -- is what the evidence supports.

    The file's key column is the **contractual, 1-based** ``policy_year`` and is left that
    way; the model reads it through ``policy_year(t) = duration(t) + 1``, which is what the
    pairing below asserts.  ``lapse_rate`` stays the **annual** rate of that policy year and
    is flat across its twelve months; ``lapse_rate_mth`` is what the recursion applies, and
    twelve of it compound back to the year's rate exactly.
    """
    p = de_klv_anchor
    table = pd.read_csv(PRODUCT_DIR / "lapse_table.csv", index_col="policy_year")
    assert list(table.columns) == ["lapse_rate", "storno_rate", "provenance"]
    assert all(prov.lstrip().startswith("[std]") for prov in table["provenance"])
    assert not any("2.72" in prov or "2,72" in prov for prov in table["provenance"])
    assert all("[R20]" in prov for prov in table["provenance"])
    assert list(table.index[:3]) == [1, 2, 3]      # the label is 1-based, not the frame's t
    for year, rate in ((1, 0.05), (2, 0.05), (3, 0.035), (8, 0.035), (9, 0.02),
                       (11, 0.02), (12, 0.06), (13, 0.025), (24, 0.025)):
        t0 = 12 * (year - 1)
        assert float(table.loc[year, "lapse_rate"]) == rate, year
        assert p.policy_year(t0) == year and p.policy_year(t0 + 11) == year
        assert p.lapse_rate(t0) == rate and p.lapse_rate(t0 + 11) == rate, year
        assert 1.0 - (1.0 - p.lapse_rate_mth(t0)) ** 12 == pytest.approx(rate, rel=1e-14)
    assert p.lapse_rate(132) > 2.0 * p.lapse_rate(120)
    assert p.lapse_rate(120) < p.lapse_rate(0) and p.lapse_rate(144) < p.lapse_rate(132)


# --- Pitfall 11: the premium-cessation rule is applied once -------------------

def test_the_premium_cessation_rule_is_applied_once(de_klv_anchor):
    """*Beiträge* are in advance and decrements at the month end, so a decedent has paid.

    Multiplying ``premiums(t)`` by ``(1 - qm)`` as well applies the rule twice.  The finer
    grid narrows the error -- 0,15 EUR in month 0 against 1,80 EUR in the first policy year
    on the annual grid -- without removing the trap: there are now twelve times as many
    chances to apply it.
    """
    p = de_klv_anchor
    for t in (0, 48, 132, 288):
        assert p.premiums(t) == pytest.approx(p.prem_inst_pp(t) * p.pols_if(t), rel=1e-12)
    twice = p.prem_inst_pp(0) * p.pols_if(0) * (1.0 - p.mort_rate_mth(0))
    assert p.premiums(0) - twice == pytest.approx(
        p.prem_gross_pp() * p.mort_rate_mth(0), rel=1e-12)
    assert p.premiums(0) - twice == pytest.approx(0.15, abs=CENT)
    assert p.prem_charged_pp(24) > 0.0


def test_an_abgekuerzte_beitragszahlungsdauer_stops_the_premium_and_not_the_cover(
        kapitallebensversicherung):
    """Model point 3 pays for 15 years and is covered for 25, on the ``low`` scenario.

    Once the premium stops ``ann_due_prem_fut`` is zero and the reserve rolls forward on
    interest and mortality alone -- which is what ``check_res_roll_fwd()`` is testing when it
    credits ``prem_zill_pp`` only while ``k < prem_term``: the fifteen premiums fall in
    policy years ``k = 0 ... 14``, months 0 to 179.
    """
    p = kapitallebensversicherung.Projection[3]
    assert p.prem_term() == 15 and p.policy_term() == 25
    assert p.proj_len_y() == 25 and p.proj_len() == 300
    assert p.prem_charged_pp(14) > 0.0 and p.prem_charged_pp(15) == 0.0
    assert p.prem_inst_pp(168) > 0.0 and p.prem_inst_pp(180) == 0.0
    assert p.ann_due_prem_fut(15) == 0.0
    assert p.scenario_id() == "low" and p.decl_rate(0) == 0.012
    assert p.zins_ueberschuss_rate(0) == pytest.approx(0.002, abs=1e-15)
    assert p.result_cf()["premiums"].sum() == pytest.approx(36089.52, abs=CENT)
    assert p.check_res_roll_fwd() is True and p.check_net_cf() is True


# --- Pitfall 12: the Risikozuschlag reaches the pricing death leg only --------

def test_the_risikozuschlag_reaches_the_price_and_not_the_benefit(
        kapitallebensversicherung, tmp_path):
    """``rating_factor`` loads the first-order mortality in the **death leg** of the pricing.

    Model point 14 carries 1.50 on the ``nil`` scenario. Against the same point at 1.00 it
    prices 80,55 EUR a year dearer -- ``pv_death_1st`` exactly 1.5 times as large -- while
    the survivorship, the best-estimate decrement and what a death claim pays are untouched.
    Inside the § 161 window the *claim* does move, and correctly so: the substituted amount
    is the *Rückkaufswert*, whose reserve carries the loading.
    """
    rated = kapitallebensversicherung.Projection[14]
    assert rated.rating_factor() == 1.5 and rated.smoker() == "S"
    assert rated.prem_gross_pp() == pytest.approx(2611.4527, abs=5e-4)
    assert rated.pv_death_1st() == pytest.approx(2495.0595, abs=5e-4)
    assert rated.benefit_full_pp(59) == pytest.approx(rated.sum_death(), rel=1e-12)
    model = variant_model(tmp_path, "KLV_DE_S_rate100", [
        ("model_point_table.csv", ",ansammlung,nil,1.5,", ",ansammlung,nil,1.0,")])
    try:
        std = model.Projection[14]
        assert std.rating_factor() == 1.0
        assert std.prem_gross_pp() == pytest.approx(2530.8989, abs=5e-4)
        assert rated.prem_gross_pp() > std.prem_gross_pp()
        assert rated.pv_death_1st() == pytest.approx(1.5 * std.pv_death_1st(), rel=1e-12)
        assert rated.pv_maturity_1st() == pytest.approx(std.pv_maturity_1st(), rel=1e-12)
        assert rated.tpx_1st(12) == pytest.approx(std.tpx_1st(12), rel=1e-12)
        assert rated.mort_rate(0) == pytest.approx(std.mort_rate(0), rel=1e-15)
        assert rated.mort_rate_mth(0) == pytest.approx(std.mort_rate_mth(0), rel=1e-15)
        assert rated.pols_death(0) == pytest.approx(std.pols_death(0), rel=1e-15)
        assert rated.benefit_full_pp(59) == pytest.approx(
            std.benefit_full_pp(59), rel=1e-12)
        assert rated.claims(59, "DEATH") == pytest.approx(
            std.claims(59, "DEATH"), rel=1e-12)
        # Inside the § 161 window the claim does move -- through the Rückkaufswert, whose
        # reserve carries the loading.  Month 11 is the first month that has one.
        assert rated.claims(11, "DEATH") != pytest.approx(
            std.claims(11, "DEATH"), rel=1e-9)
        assert rated.benefit_full_pp(11) == pytest.approx(
            std.benefit_full_pp(11), rel=1e-12)
        assert rated.check_res_roll_fwd() is True and std.check_res_roll_fwd() is True
    finally:
        model.close()


# --- Pitfall 13: one first-order table, used for both legs -------------------

def test_one_first_order_table_serves_both_legs(kapitallebensversicherung, de_klv_anchor):
    """The direction of prudence forks, and the model uses one table anyway -- visibly.

    A death benefit wants mortality assumed higher than expected and a survival benefit
    lower, so no single first-order table is prudent for both; German practice resolves that
    in the tariff rather than in the table. Both legs are rebuilt here from
    ``mort_table.csv`` on the same unisex blend, so the compromise is asserted, not described.
    """
    p = de_klv_anchor
    table = kapitallebensversicherung.Data.mort_table()
    share = kapitallebensversicherung.Projection.unisex_share

    def q1(x):
        return (share * float(table.loc[("M", x), "mort_rate_1st"])
                + (1.0 - share) * float(table.loc[("F", x), "mort_rate_1st"]))

    v = 1.0 / 1.01
    death, survive, annuity = 0.0, 1.0, 0.0
    for k in range(25):
        annuity += v ** k * survive
        death += v ** (k + 1) * survive * q1(37 + k)
        survive *= 1.0 - q1(37 + k)
    assert 50000.0 * death == pytest.approx(p.pv_death_1st(), rel=1e-12)
    assert 50000.0 * v ** 25 * survive == pytest.approx(p.pv_maturity_1st(), rel=1e-12)
    assert annuity == pytest.approx(p.ann_due_prem_1st(), rel=1e-12)
    assert survive == pytest.approx(p.tpx_1st(25), rel=1e-12)
    assert set(table.columns) == {"mort_rate_1st", "provenance"}   # no second table


# --- Pitfall 14: the first- and second-order bases are not crossed ------------

def test_the_two_mortality_bases_are_not_crossed(kapitallebensversicherung, de_klv_anchor):
    """``mort_rate_at_age`` prices and reserves; ``mort_rate`` projects.

    ``mort_rate(t) = mort_rate_base(t) x 0.75``, so the first-order table carries a 33 %
    safety loading. That wedge is the *Sicherheitszuschlag* whose systematic release **is**
    the *Risikoüberschuss*, which a model reserving on the best estimate would have thrown
    away -- so ``res_pp`` and the price must be invariant to ``mort_be_factor`` while
    ``pols_death`` moves with it.
    """
    p = de_klv_anchor
    assert kapitallebensversicherung.Projection.mort_be_factor == 0.75
    for t in (0, 4, 11, 24):
        assert p.mort_rate(t) == pytest.approx(p.mort_rate_base(t) * 0.75, rel=1e-12)
    assert p.mort_rate_base(0) == pytest.approx(0.001200, abs=5e-13)
    assert p.mort_rate(0) == pytest.approx(0.000900, abs=5e-13)
    assert p.mort_rate(0) < p.mort_rate_at_age(37) < p.mort_rate_base(0)
    reserves = [p.res_pp(t) for t in (0, 4, 11, 24)]
    premium, deaths = p.prem_gross_pp(), p.pols_death(4)
    model = mx.read_model(MODEL_DIR, name="KLV_DE_S_be90")
    try:
        model.Projection.mort_be_factor = 0.90
        model.Projection.clear_all()
        q = model.Projection[1]
        assert q.mort_rate(0) == pytest.approx(0.001200 * 0.90, rel=1e-12)
        assert [q.res_pp(t) for t in (0, 4, 11, 24)] == reserves
        assert q.prem_gross_pp() == premium
        assert q.mort_rate_at_age(37) == p.mort_rate_at_age(37)
        assert q.pols_death(4) > deaths
        assert q.result_cf()["claims_death"].sum() > TOTALS["claims_death"]
        assert q.check_res_roll_fwd() is True
    finally:
        model.close()


# --- Pitfall 15: the two surplus systems do not give the same benefits --------

def test_the_ansammlung_pays_more_at_maturity_and_the_bonus_more_on_death(
        kapitallebensversicherung, de_klv_anchor):
    """"The *verzinsliche Ansammlung* leads to a higher payment at maturity, while the
    *Bonussystem* produces higher death benefits."

    Model points 1 and 8 differ in ``surplus_use`` alone, and the asymmetry is arithmetic:
    the *Ansammlung* compounds at ``ans_rate`` = 2,70 % while bonus sum insured accumulates
    at ``rechnungszins`` = 1,00 %, but the bonus is **paid-up insurance** whose whole face
    amount falls due at once on death. A model setting the two rates equal loses the
    distinction, correctly.
    """
    ans = de_klv_anchor
    bonus = kapitallebensversicherung.Projection[8]
    assert ans.surplus_use() == "ansammlung" and bonus.surplus_use() == "bonus"
    assert ans.ans_rate(0) == 0.027 and ans.rechnungszins() == 0.01
    assert bonus.prem_gross_pp() == pytest.approx(ans.prem_gross_pp(), rel=1e-12)
    for k in (0, 4, 11, 24):
        assert bonus.surplus_credit_pp(k) == pytest.approx(
            ans.surplus_credit_pp(k), rel=1e-12)
    assert ans.benefit_maturity_pp(299) - bonus.benefit_maturity_pp(299) == pytest.approx(
        1665.22, abs=CENT)
    # At the fifth policy year's anniversary, month 59 -- the instant the annual grid priced.
    assert bonus.benefit_death_pp(59) - ans.benefit_death_pp(59) == pytest.approx(
        71.21, abs=CENT)
    # And the asymmetry survives the finer grid: it holds in a mid-year month too, on the
    # balances standing at the last anniversary.
    assert bonus.benefit_death_pp(48) > ans.benefit_death_pp(48)
    assert bonus.av_sur_pp(25) == 0.0 and ans.av_sur_pp(25) > 0.0
    assert bonus.bonus_si_pp(25) > 0.0 and ans.bonus_si_pp(25) == 0.0
    assert bonus.check_surplus_roll_fwd() is True


# --- Pitfall 16: the Zahlbeitrag is not guaranteed ----------------------------

def test_the_zahlbeitrag_is_not_guaranteed_under_beitragsverrechnung(
        kapitallebensversicherung, de_klv_anchor, tmp_path):
    """The policyholder pays the *Bruttobeitrag* less a **discretionary** surplus offset.

    On model point 9 last year's declared surplus reduces this year's *Zahlbeitrag* while
    ``prem_charged_pp`` -- the tariff premium -- is unchanged from the anchor, and the renewal
    commission reads the tariff premium: the intermediary is paid on the price, the offset
    being a rebate. On the ``nil`` scenario the offset is zero and the two coincide, which is
    what "discretionary" means in cash.
    """
    bv = kapitallebensversicherung.Projection[9]
    p = de_klv_anchor
    assert bv.surplus_use() == "beitragsverrechnung"
    assert bv.prem_offset_pp(0) == 0.0        # there is no previous year to carry
    for k in range(1, 25):
        assert bv.prem_offset_pp(k) == pytest.approx(
            min(bv.prem_charged_pp(k), bv.surplus_credit_pp(k - 1)), rel=1e-12)
        assert bv.prem_paid_pp(k) < bv.prem_charged_pp(k)
        assert bv.prem_charged_pp(k) == pytest.approx(p.prem_charged_pp(k), rel=1e-12)
    assert bv.prem_offset_pp(4) == pytest.approx(104.3370, abs=5e-4)
    assert bv.prem_paid_pp(4) == pytest.approx(1899.7051, abs=5e-4)
    # The commission is charged on the instalment of the **tariff** premium, month 48 being
    # the first month of policy year 5 and so the one an annual payer is billed in.
    assert bv.commissions(48) == pytest.approx(
        0.015 * bv.prem_charged_inst_pp(48) * bv.pols_if(48), rel=1e-12)
    assert bv.commissions(48) > 0.015 * bv.prem_inst_pp(48) * bv.pols_if(48)
    assert bv.result_cf()["commissions"].sum() == pytest.approx(
        TOTALS["commissions"], abs=CENT)
    model = variant_model(tmp_path, "KLV_DE_S_bv_nil", [
        ("model_point_table.csv",
         ",beitragsverrechnung,base,", ",beitragsverrechnung,nil,")])
    try:
        nil = model.Projection[9]
        assert nil.scenario_id() == "nil"
        assert all(nil.prem_offset_pp(k) == 0.0 for k in range(25))
        assert all(nil.prem_paid_pp(k) == nil.prem_charged_pp(k) for k in range(25))
        assert nil.result_cf()["premiums"].sum() > bv.result_cf()["premiums"].sum()
        assert nil.check_surplus_roll_fwd() is True
    finally:
        model.close()


# --- Pitfall 17: sex never reaches the premium -------------------------------

def test_the_tariff_is_unisex_while_the_decrement_is_not(kapitallebensversicherung,
                                                         de_klv_anchor):
    """New business has been unisex since 21 December 2012, so ``sex`` may not price.

    Model points 1 and 7 differ in ``sex`` (and in payment frequency) and both price at
    2 004,0420 EUR before the *Ratenzahlungszuschlag*. What ``sex`` does reach is the
    **decrement**: 0,000672 against 0,000900 in the first policy year. Pricing off the policy's own row
    instead of the fixed unisex blend is silent, and it moved this premium by 9,15 EUR when
    the model was first written that way.
    """
    male, female = de_klv_anchor, kapitallebensversicherung.Projection[7]
    assert male.sex() == "M" and female.sex() == "F"
    assert female.prem_gross_pp() == male.prem_gross_pp()
    assert female.prem_gross_pp() == pytest.approx(2004.0420, abs=5e-4)
    assert female.pv_death_1st() == pytest.approx(male.pv_death_1st(), rel=1e-15)
    assert female.res_pp(4) == pytest.approx(male.res_pp(4), rel=1e-15)
    assert female.res_guar_pp(4) == pytest.approx(male.res_guar_pp(4), rel=1e-15)
    assert female.mort_rate(0) == pytest.approx(0.00067221637875, abs=5e-13)
    assert male.mort_rate(0) == pytest.approx(0.000900, abs=5e-13)
    assert female.mort_rate_mth(0) < male.mort_rate_mth(0)
    assert female.pols_if(108) > male.pols_if(108)
    assert female.result_cf()["claims_death"].sum() < TOTALS["claims_death"]
    blend = kapitallebensversicherung.Data.mort_table()
    expected = 0.5 * float(blend.loc[("M", 37), "mort_rate_1st"]) + 0.5 * float(
        blend.loc[("F", 37), "mort_rate_1st"])
    assert male.mort_rate_at_age(37) == pytest.approx(expected, rel=1e-15)
    assert kapitallebensversicherung.Projection.unisex_share == 0.5


# --- Pitfall 18: the Ablauf year carries no surrender ------------------------

def test_nothing_runs_past_the_ablauf_and_the_last_year_has_no_surrender(
        kapitallebensversicherung, de_klv_anchor):
    """``proj_len() = 12 * policy_term`` is the frame's **exclusive** end: the last row is
    ``t = proj_len() - 1`` and there is no ``t = proj_len()`` row.

    ``lapse_rate`` is 0 through the whole last **policy year** [std], so the survivors of its
    mortality all leave as a maturity -- and unlike a term product the two exits do **not**
    pay the same thing, a surrender paying the § 169 value and a maturity the sum insured
    plus the whole accumulated surplus: 61 549,01 EUR against 65 227,99 EUR. A real payment
    decision, not a bookkeeping split.
    """
    p = de_klv_anchor
    n = p.proj_len()
    assert n == 12 * p.policy_term() == 300 and p.proj_len_y() == 25
    last = n - 1
    df = p.result_cf()
    assert list(df.index) == list(range(300))
    assert df.index.name == "t" and df.index[-1] == last
    assert all(p.lapse_rate(t) == 0.0 for t in range(288, 300))
    assert p.lapse_rate(287) == 0.025
    assert all(p.pols_lapse(t) == 0.0 for t in range(288, 300))
    assert df.loc[288:, "claims_lapse"].sum() == 0.0
    assert p.pols_maturity(last) == pytest.approx(
        p.pols_if(last) * (1.0 - p.mort_rate_mth(last)), rel=1e-12)
    assert p.pols_maturity(last) == pytest.approx(
        p.pols_if_at(last, "AFT_MORT"), rel=1e-12)
    assert p.pols_if(n) == pytest.approx(p.pols_maturity(last), rel=1e-12)
    assert p.pols_if(n + 1) == 0.0
    assert p.surr_value_pp(last) == pytest.approx(61549.01, abs=CENT)
    assert p.benefit_maturity_pp(last) == pytest.approx(65227.99, abs=CENT)
    assert p.benefit_maturity_pp(last) > p.surr_value_pp(last)
    assert p.benefit_maturity_pp(last - 1) == 0.0
    assert p.check_decrement_closure_resid(last) == pytest.approx(0.0, abs=1e-12)
    names = set(kapitallebensversicherung.Projection.cells) | set(
        kapitallebensversicherung.Projection.refs)
    for absent in ("pols_expiry", "renewal_rate", "conv_rate", "claims_surr",
                   "withdrawals", "prem_to_av_pp", "lapse_rate_ann", "prem_net_pp",
                   "mort_ae_factor", "mort_rate_table", "check_pols_if", "pols_init"):
        assert absent not in names, absent


# --- The published identities ------------------------------------------------

def test_every_check_closes_on_the_anchor_cell(kapitallebensversicherung, de_klv_anchor):
    """Ten ``check_*()`` cells, each a no-argument bool with a per-argument residual.

    ``check_net_cf()`` is this library's first ruling and is asserted here beside the rest:
    the cash flow statement reconciles from ``result_cf()``'s own published columns, so the
    headline number of a cash flow model is not the one quantity nothing checks.

    **Their arguments say which clock each identity lives on.** The three that state an
    annual identity -- the Fackler roll-forward, the surplus ledgers and the § 169 floor --
    take a policy year ``k``; the rest take a month ``t``.  ``check_surr_nonneg`` is the one
    the conversion added: the monthly grid quotes a *Rückkaufswert* in eleven months of each
    policy year the annual grid never priced.
    """
    p = de_klv_anchor
    cells = kapitallebensversicherung.Projection.cells
    checks = sorted(c for c in cells
                    if c.startswith("check_") and not c.endswith("_resid"))
    assert checks == [
        "check_decrement_closure", "check_equivalence", "check_net_cf",
        "check_pols_roll_fwd", "check_rechnungszins_cap", "check_res_roll_fwd",
        "check_surplus_roll_fwd", "check_surr_floor", "check_surr_nonneg",
        "check_zillmer_cap"]
    annual = {"check_res_roll_fwd", "check_surplus_roll_fwd", "check_surr_floor"}
    for name in checks:
        assert cells[name].parameters == (), name
        value = getattr(p, name)()
        assert isinstance(value, bool) and value is True, name
        arg = "k" if name in annual else "t"
        assert cells[name + "_resid"].parameters == (arg,), name
        points = (0, 11, 24) if arg == "k" else (0, 11, 143, 299)
        for x in points:
            assert getattr(p, name + "_resid")(x) == pytest.approx(0.0, abs=1e-8), (name, x)


def test_the_reserve_roll_forward_is_the_strongest_check(de_klv_anchor):
    """Fackler, computed retrospectively on the left and prospectively on the right.

    ``(V(k) + P^Z)(1 + i1) = q1(k) SD + (1 - q1(k)) V(k+1)`` on the anchor cell, where the
    *Risikozuschlag* is 1.00. It fails on a loading applied to the survivorship, a Zillmer
    premium amortised over the wrong annuity, a reserve read at the wrong duration, and a
    premium still credited after the *Beitragszahlungsdauer* has ended.

    A **policy-year** identity, and it stays one on the monthly grid: an annual Fackler
    recursion at an annual *Rechnungszins*, which is what the tariff defines.
    """
    p = de_klv_anchor
    for k in (0, 1, 11, 23, 24):
        q1 = p.mort_rate_at_age(p.age_y(k))
        left = (p.res_pp(k) + p.prem_zill_pp()) * (1.0 + p.rechnungszins())
        right = q1 * p.sum_death() + (1.0 - q1) * p.res_pp(k + 1)
        assert left == pytest.approx(right, abs=1e-6), k
        assert p.res_pp_at(k, "AFT_INT") == pytest.approx(p.res_pp(k + 1), abs=1e-6), k
    assert p.check_res_roll_fwd() is True


def test_the_deckrv_cohort_ceilings_are_parameter_invariants(kapitallebensversicherung,
                                                             de_klv_anchor):
    """A 4,00 % guarantee on a 2026 issue year is not a stress, it is a data error.

    Both ceilings travel with the contract for its whole term, which is why they are keyed by
    ``issue_year`` and why the in-force point carries 1,75 % against new business's 1,00 %.
    """
    p = de_klv_anchor
    assert p.issue_year() == 2026
    assert p.hrz_max() == 0.01 and p.rechnungszins() == 0.01
    assert p.check_rechnungszins_cap() is True
    inforce = kapitallebensversicherung.Projection[10]
    assert inforce.hrz_max() == 0.0175 and inforce.rechnungszins() == 0.0175
    assert inforce.check_rechnungszins_cap() is True
    deckrv = pd.read_csv(PRODUCT_DIR / "deckrv_table.csv", index_col="issue_year")
    assert float(deckrv.loc[2025, "hoechstrechnungszins"]) == 0.01
    assert float(deckrv.loc[2024, "hoechstrechnungszins"]) == 0.0025
    assert float(deckrv.loc[2014, "hoechstzillmersatz"]) == 0.040
    assert float(deckrv.loc[2015, "hoechstzillmersatz"]) == 0.025
    # The split years take the higher of the two published rates [std].
    assert float(deckrv.loc[1994, "hoechstrechnungszins"]) == 0.04
    assert float(deckrv.loc[2000, "hoechstrechnungszins"]) == 0.04
    assert all("[std]" in deckrv.loc[y, "provenance"] for y in (1994, 2000))


# --- The in-force point and the payment frequencies --------------------------

def test_the_in_force_point_opens_where_it_should(kapitallebensversicherung):
    """Model point 10 is a 2012 cohort valued at duration 14, with an opening balance.

    The frame opens at ``t_start() = 12 * duration_init() = 168`` -- ``duration_init`` is an
    elapsed count of policy **years**, so the conversion is a multiplication -- ``pols_if``
    opens at ``pols_if_init()`` exactly, and neither the acquisition expense nor the initial
    commission is charged: both were incurred at conclusion. Expense inflation is
    nevertheless measured from **issue**, so the maintenance expense opens already inflated
    by fourteen years.
    """
    p = kapitallebensversicherung.Projection[10]
    assert p.duration_init() == 14 and p.k_start() == 14
    assert p.t_start() == 168 and p.proj_len() == 360 and p.proj_len_y() == 30
    df = p.result_cf()
    assert list(df.index) == list(range(168, 360))
    assert df["pols_if"].iloc[0] == p.pols_if_init() == 1.0
    assert p.av_sur_pp(14) == p.av_sur_pp_init() == 6000.0
    assert p.commissions(168) == 0.0 and p.commissions(180) > 0.0
    assert p.expenses_pp(168) == pytest.approx(45.0 / 12.0 * 1.018 ** 14, rel=1e-12)
    assert p.inflation_factor(14) == pytest.approx(1.018 ** 14, rel=1e-12)
    assert p.result_cf_annual().loc[15, "expenses"] == pytest.approx(60.46, abs=CENT)
    assert df["net_cf"].sum() == pytest.approx(-40333.21, abs=CENT)
    for name in ("check_net_cf", "check_pols_roll_fwd", "check_res_roll_fwd",
                 "check_surplus_roll_fwd", "check_decrement_closure"):
        assert getattr(p, name)() is True, name


def test_the_frequency_loading_applies_to_an_unechte_zahlweise_only(
        kapitallebensversicherung, de_klv_anchor):
    """Model points 4 and 5 are the same monthly contract under the two readings.

    ``unecht`` means the *Versicherungsperiode* stays the year and the monthly payment is an
    **instalment** of an annual premium, which is what the loading compensates. ``echt``
    means the period is genuinely monthly, and then no loading applies at all -- a
    distinction entirely lost on a model that treats frequency as a single multiplier.
    """
    unecht = kapitallebensversicherung.Projection[4]
    echt = kapitallebensversicherung.Projection[5]
    assert unecht.prem_freq() == echt.prem_freq() == "monthly"
    assert unecht.instalments() == echt.instalments() == 12
    assert unecht.unterjaehrig_form() == "unecht" and echt.unterjaehrig_form() == "echt"
    assert unecht.prem_freq_load() == 1.05 and echt.prem_freq_load() == 1.0
    assert unecht.prem_gross_pp() == pytest.approx(echt.prem_gross_pp(), rel=1e-15)
    assert unecht.prem_charged_pp(0) == pytest.approx(
        1.05 * echt.prem_charged_pp(0), rel=1e-12)
    # On the monthly grid the distinction is in the frame as well as in the multiplier: both
    # collect twelve instalments a year, and the loaded one collects 5 % more in each.
    assert unecht.prem_cycle() == echt.prem_cycle() == 1
    assert all(unecht.prem_due(t) for t in range(12))
    assert unecht.prem_inst_pp(0) == pytest.approx(
        1.05 * echt.prem_inst_pp(0), rel=1e-12)
    assert unecht.prem_inst_pp(0) == pytest.approx(
        unecht.prem_charged_pp(0) / 12.0, rel=1e-12)
    assert unecht.result_cf()["premiums"].sum() == pytest.approx(34490.50, abs=CENT)
    assert echt.result_cf()["premiums"].sum() == pytest.approx(32848.10, abs=CENT)
    # Both collect less than the annual-mode cell, the later instalments falling on a block
    # that has already lost lives -- which is the premium-cessation rule biting where an
    # annual grid could not express it.
    assert echt.result_cf()["premiums"].sum() < TOTALS["premiums"]
    # The loading is a premium-income assumption and touches nothing else.
    assert (unecht.result_cf()["claims_death"]
            - echt.result_cf()["claims_death"]).abs().max() < 1e-9
    assert unecht.beitragssumme() == pytest.approx(echt.beitragssumme(), rel=1e-15)
    half, quarterly = (kapitallebensversicherung.Projection[6],
                       kapitallebensversicherung.Projection[7])
    assert half.prem_freq_load() == 1.02 and half.instalments() == 2
    assert half.prem_cycle() == 6
    assert [t for t in range(12) if half.prem_due(t)] == [0, 6]
    assert quarterly.prem_freq_load() == 1.03 and quarterly.instalments() == 4
    assert quarterly.prem_cycle() == 3
    assert [t for t in range(12) if quarterly.prem_due(t)] == [0, 3, 6, 9]
    assert de_klv_anchor.prem_freq_load() == 1.0 and de_klv_anchor.instalments() == 1
    assert de_klv_anchor.prem_cycle() == 12


# --- Structure, documentation and inputs -------------------------------------

def test_result_cf_shape_and_both_signs_of_the_net_flow(de_klv_anchor):
    """The notes' eight columns plus ``liability_cf``, the notes' own outgo orientation.

    The six flow columns sum to ``net_cf`` because ``expenses`` excludes commission. A model
    on the frlib convention, where the expense column carries the commission, must not
    subtract both -- and publishing ``claims`` beside its own parts would do the same damage
    from the other direction.
    """
    df = de_klv_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_maturity", "claims_lapse",
        "expenses", "commissions", "net_cf", "liability_cf"]
    assert "claims" not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    outgo = (df["claims_death"] + df["claims_maturity"] + df["claims_lapse"]
             + df["expenses"] + df["commissions"])
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert list(df.index) == list(range(300)) and df.index.name == "t"
    # Read by policy year: the first year very nearly washes and the strain of a gezillmert
    # endowment is in the reserve, not in the cash flow.
    ann = de_klv_anchor.result_cf_annual()
    assert (ann["commissions"] > ann["expenses"]).sum() == 1     # policy year 1 only
    assert ann["net_cf"].loc[1] == pytest.approx(355.51, abs=CENT)
    assert (ann["net_cf"].iloc[:-1] > 0).all()
    assert ann["net_cf"].iloc[-1] == pytest.approx(-28168.54, abs=CENT)
    assert de_klv_anchor.res_pp(0) == pytest.approx(-1252.53, abs=CENT)


def test_invalid_enum_values_raise(de_klv_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_klv_anchor.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        de_klv_anchor.res_pp_at(0, "AFTER_PREMIUM")
    with pytest.raises(FormulaError):
        de_klv_anchor.av_sur_pp_at(0, "AFTER_INTEREST")
    with pytest.raises(FormulaError):
        de_klv_anchor.pols_if_at(0, "AFTER_LAPSE")


def test_docstrings_describe_the_current_structure(kapitallebensversicherung):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = kapitallebensversicherung.doc
    assert "kapitalbildende Lebensversicherung" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                      # inputs are not stored in the model
    assert "once per model" in doc                # why Data exists
    assert "Überschussbeteiligung" in doc and "gemischte Versicherung" in doc
    assert "DAV 2008 T" in doc and "check_net_cf()" in doc
    proj = kapitallebensversicherung.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "res_pp", "res_guar_pp", "surr_value_pp",
                  "av_sur_pp_at", "bfz_si_pp", "zins_ueberschuss_rate", "storno_rate",
                  "mort_rate_at_age", "liability_cf", "policy_year",
                  "duration_mth", "is_anniv", "mort_rate_mth", "lapse_rate_mth",
                  "prem_inst_pp", "av_sur_close_pp", "res_guar_close_pp",
                  "result_cf_annual"):
        assert cells in proj, cells
    # The time index counts policy months and the contractual policy year is derived.
    assert "0-based" in proj and "policy_year(t) = duration(t) + 1" in proj
    # The conversion's own decisions are named on the page, not merely implemented.
    assert "Two clocks, and which cells carries which" in proj
    assert "What the monthly grid changes, and what it does not" in proj
    for phrase in ("policy months", "bit-identical", "anniversary",
                   "1 - (1 - r)^(1/12)"):
        assert phrase in proj, phrase
    data = kapitallebensversicherung.Data.doc
    assert "TradLife_A" in data
    assert "0.001200" in data                     # the mortality proxy's anchor
    assert "provenance" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "lapse_table",
                  "surplus_rate_table", "cost_table", "freq_loading_table",
                  "deckrv_table"):
        assert cells in data, cells


def test_the_endowment_chassis_vocabulary_is_present(kapitallebensversicherung):
    """Names the other Überschussbeteiligung products inherit must mean the same here."""
    shared = {
        "model_point", "proj_len", "proj_len_y", "t_start", "k_start", "age", "age_y",
        "duration", "duration_mth", "is_anniv", "policy_year",
        "pols_if", "pols_if_at", "pols_if_init", "pols_death", "pols_lapse",
        "pols_maturity", "mort_rate", "mort_rate_base", "mort_rate_at_age",
        "lapse_rate", "storno_rate", "prem_gross_pp", "prem_net_level_pp",
        "prem_zill_pp", "prem_charged_pp", "prem_paid_pp", "premiums",
        "res_pp", "res_pp_at", "res_net_pp", "res_zill_pp", "res_min_pp",
        "res_guar_pp", "surr_value_pp", "decl_rate", "zins_ueberschuss_rate",
        "term_rate", "ans_rate", "surplus_base_pp", "surplus_credit_pp",
        "term_bonus_pp", "av_sur_pp", "av_sur_pp_at", "av_sur", "av_sur_at", "bonus_si_pp",
        "benefit_death_pp", "benefit_maturity_pp", "claims", "claim_expenses",
        "expenses", "commissions", "inflation_factor", "net_cf", "liability_cf",
        "result_cf", "result_cf_annual", "result_surplus",
        "mort_rate_mth", "lapse_rate_mth", "prem_cycle", "prem_due",
        "prem_charged_inst_pp", "prem_inst_pp",
        "av_sur_close_pp", "bonus_si_close_pp", "term_bonus_close_pp",
        "res_guar_close_pp"}
    names = set(kapitallebensversicherung.Projection.cells) | set(
        kapitallebensversicherung.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    # The two-speed pair the library requires wherever a grid is monthly: the annual rate
    # the notes tabulate, and the monthly rate derived from it.  Both **compound** back to
    # the year's rate -- a twelfth of an annual rate would undershoot, and asserting only the
    # inequality would not tell the two apart.
    proj = kapitallebensversicherung.Projection[1]
    for t in (0, 60, 200):
        assert proj.mort_rate_mth(t) < proj.mort_rate(t)
        assert proj.lapse_rate_mth(t) < proj.lapse_rate(t)
        assert 1.0 - (1.0 - proj.mort_rate_mth(t)) ** 12 == pytest.approx(
            proj.mort_rate(t), rel=1e-14)
        assert 1.0 - (1.0 - proj.lapse_rate_mth(t)) ** 12 == pytest.approx(
            proj.lapse_rate(t), rel=1e-14)
        assert proj.mort_rate_mth(t) > proj.mort_rate(t) / 12.0
        assert proj.lapse_rate_mth(t) > proj.lapse_rate(t) / 12.0


def test_the_shipped_tables_mark_their_own_provenance():
    """Seven CSVs beside run.py, and each says what it is -- especially what it is not.

    The mortality table is a **[std]** proxy: DAV 2008 T is cited by name and never shipped,
    and the anchor a substitute must preserve is the male rate at age 37. The surplus table's
    only sourced number is the 2,70 % declared rate, and the cost table carries first- and
    second-order parameters on one row because the difference between them *is* the
    *Kostenüberschuss*.
    """
    assert {p.name for p in PRODUCT_DIR.iterdir() if p.suffix == ".csv"} == INPUT_CSVS
    mort = pd.read_csv(PRODUCT_DIR / "mort_table.csv")
    assert set(mort.columns) == {"sex", "age", "mort_rate_1st", "provenance"}
    assert all(prov.lstrip().startswith("[std]") for prov in mort["provenance"])
    assert all("DAV 2008 T" in prov for prov in mort["provenance"])
    male = mort[mort["sex"] == "M"].set_index("age")
    female = mort[mort["sex"] == "F"].set_index("age")
    assert float(male.loc[37, "mort_rate_1st"]) == 0.001200
    assert float(female.loc[37, "mort_rate_1st"]) == pytest.approx(0.000896288505, abs=5e-13)
    assert float(male.loc[38, "mort_rate_1st"]) - 0.00022 == pytest.approx(
        1.10 * (float(male.loc[37, "mort_rate_1st"]) - 0.00022), rel=1e-9)
    assert mort["mort_rate_1st"].max() <= 1.0
    assert list(male.index) == list(range(0, 121))

    surplus = pd.read_csv(PRODUCT_DIR / "surplus_rate_table.csv")
    assert set(surplus["scenario_id"]) == {"base", "low", "nil"}
    base = surplus[surplus["scenario_id"] == "base"]
    assert set(base["decl_rate"]) == {0.0270} and set(base["ans_rate"]) == {0.0270}
    assert set(base["term_rate"]) == {0.0040}
    assert all("[S11]" in prov for prov in base["provenance"])
    nil = surplus[surplus["scenario_id"] == "nil"]
    assert set(nil["decl_rate"]) == {0.0}
    assert all("[std]" in prov for prov in nil["provenance"])

    cost = pd.read_csv(PRODUCT_DIR / "cost_table.csv", index_col="cost_id").loc["std_2026"]
    assert float(cost["alpha_rate"]) == 0.0250 and float(cost["beta_rate"]) == 0.0300
    assert float(cost["gamma_rate"]) == 0.0015
    assert float(cost["acq_expense"]) == 300.0 and float(cost["maint_expense"]) == 45.0
    assert float(cost["expense_infl"]) == 0.0180 and float(cost["claim_expense"]) == 120.0
    assert float(cost["comm_init_rate"]) == 0.0250
    assert float(cost["comm_renew_rate"]) == 0.0150
    assert "[std]" in cost["provenance"] and "gap 7" in cost["provenance"]

    freq = pd.read_csv(PRODUCT_DIR / "freq_loading_table.csv", index_col="prem_freq")
    assert list(freq.index) == ["annual", "half_yearly", "quarterly", "monthly"]
    assert list(freq["instalments"]) == [1, 2, 4, 12]
    assert list(freq["prem_freq_load"]) == [1.0, 1.02, 1.03, 1.05]
    assert all("[R28]" in prov for prov in freq["provenance"])

    points = pd.read_csv(PRODUCT_DIR / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns      # the one exemption in the library
    assert len(points) == 14 and points.loc[1, "policy_id"] == "DE-KLV-0001"
    # Every point satisfies the Mindesttodesfallschutz: a design constraint checked when the
    # table is built rather than a model formula.
    assert (points["death_ratio"] >= 0.5).all()


def test_the_behaviour_modules_are_off_and_reachable(kapitallebensversicherung,
                                                     de_klv_anchor):
    """Base run values, so the worked example reproduces with the machinery still there."""
    proj = kapitallebensversicherung.Projection
    assert proj.beta_shock == 0.0 and proj.lapse_gap_a == 0.0 and proj.ref_rate == 0.03
    assert proj.bwr_rate == 0.0 and proj.term_surr_share == 0.0
    assert proj.roll_fwd_tol == 1e-10
    p = de_klv_anchor
    # bwr_rate off: no Bewertungsreserven share leaks into the maturity benefit.
    assert p.benefit_maturity_pp(299) == pytest.approx(
        p.sum_assured() + p.av_sur_pp(25) + p.bonus_si_pp(25) + p.term_bonus_pp(25), rel=1e-12)
    # term_surr_share off: the accrued terminal share is not paid on surrender, at the
    # anniversary of policy year 24 or in any month of it.
    assert p.surr_value_pp(12 * 23 + 11) == pytest.approx(
        p.res_guar_pp(23) * (1.0 - p.storno_rate(23)) + p.av_sur_pp_at(23, "AFT_CREDIT"),
        rel=1e-12)
    assert p.surr_value_pp(12 * 23) == pytest.approx(
        p.res_guar_pp(22) * (1.0 - p.storno_rate(23)) + p.av_sur_pp(23), rel=1e-12)


def test_the_bewertungsreserven_switch_is_reachable():
    """``bwr_rate`` is exposed so the reasoning behind the zero is visible and reversible.

    § 153 Abs. 3 VVG allocates half the *Bewertungsreserven* determined on termination, but
    § 139 VAG permits participation only to the extent they exceed the *Sicherungsbedarf*,
    and that need has routinely exhausted them -- a fact about the market rather than about
    the contract, so the parameter stays rather than the branch being deleted.
    """
    model = mx.read_model(MODEL_DIR, name="KLV_DE_S_bwr")
    try:
        model.Projection.bwr_rate = 0.02
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.benefit_maturity_pp(299) == pytest.approx(
            65227.99 + 0.02 * p.res_guar_pp(24), abs=CENT)
        assert p.result_cf()["claims_maturity"].sum() > TOTALS["claims_maturity"]
        assert p.check_net_cf() is True
        # It touches the maturity benefit and nothing else.
        assert p.result_cf()["claims_lapse"].sum() == pytest.approx(
            TOTALS["claims_lapse"], abs=CENT)
    finally:
        model.close()


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """This is what a production user does with a company or licensed mortality basis.

    Inputs are external, so the swap is a filename Reference and not a formula change.
    Lighter first-order mortality is a cheaper death leg and a dearer survival leg on an
    endowment, so the premium moves -- which a term model's would not.
    """
    lighter = pd.read_csv(PRODUCT_DIR / "mort_table.csv")
    lighter["mort_rate_1st"] = lighter["mort_rate_1st"] * 0.5
    alt = tmp_path / "mort_table_light.csv"
    lighter.to_csv(alt, index=False)
    model = mx.read_model(MODEL_DIR, name="KLV_DE_S_swap")
    try:
        target = model.Data.input_dir() / alt.name
        shutil.copy(alt, target)
        try:
            base = model.Projection[1].result_cf()["claims_death"].sum()
            assert base == pytest.approx(TOTALS["claims_death"], abs=CENT)
            model.Data.mort_table_file = alt.name
            model.Data.clear_all()
            model.Projection.clear_all()
            swapped = model.Projection[1]
            assert swapped.mort_rate_base(0) == pytest.approx(0.0006, abs=5e-13)
            assert swapped.result_cf()["claims_death"].sum() < base
            assert swapped.prem_gross_pp() != pytest.approx(
                TARIFF["prem_gross_pp"], abs=5e-4)
            assert swapped.check_res_roll_fwd() is True
            assert swapped.check_equivalence() is True
        finally:
            target.unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set.

    Inputs are external, so they must travel with the model: the CSVs are copied to the new
    parent before re-reading. That is exactly the trade-off this layout makes, and the reason
    it is worth asserting in both directions.
    """
    model = mx.read_model(MODEL_DIR, name="KLV_DE_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()
    for csv_path in PRODUCT_DIR.glob("*.csv"):
        shutil.copy(csv_path, tmp_path / csv_path.name)
    reread = mx.read_model(dest, name="KLV_DE_S_rt")
    try:
        p = reread.Projection[1]
        ann = p.result_cf_annual()
        for y, row in WORKED_EXAMPLE.items():
            assert ann.loc[y, "premiums"] == pytest.approx(row[2], abs=CENT)
            assert ann.loc[y, "claims_lapse"] == pytest.approx(row[5], abs=CENT)
            assert ann.loc[y, "net_cf"] == pytest.approx(row[8], abs=CENT)
        assert p.prem_gross_pp() == pytest.approx(TARIFF["prem_gross_pp"], abs=5e-4)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_net_cf() is True and p.check_res_roll_fwd() is True
        assert p.check_decrement_closure() is True
    finally:
        reread.close()
    assert model_files(dest) == model_files(MODEL_DIR)
