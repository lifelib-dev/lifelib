"""Golden and structural tests for Riester_DE_S.

The golden values are the worked example in
products/riester_rente/technical-notes.md ("Worked example"), which is a **configuration**
rather than a scenario: an in-force *klassische Riester-Rentenversicherung* -- a certified
Altersvorsorgevertrag under the AltZertG, Schicht 2 -- at the 1 January 2027 valuation
date.  The saver is female (reporting only: the tariff, the decrements and the
*Rentenfaktor* are unisex); the contract was concluded at attained age 47 on 1 January 2024
and has run three complete contract years, so ``age(0) = 50``, ``duration(0) = 3`` -- the
0-based count, i.e. contract year 4 -- and ``calendar_year(0) = 2027``.  *Rentenbeginn* is 67, the *Rechnungszins* 0,25 %, the
*Beitragssumme* 33 600,00 EUR; the contribution form is ``mindest`` at
``contrib_ratio = 1.00``, with no unsubsidised second pool and no biometric rider; the
earnings path is ``grow2`` from 42 000,00 EUR and the entitlement path ``k1_2010`` -- one
child born in 2010 drawing *Kindergeld* to 2028, so 475,00 EUR of entitlement in
contribution years 2027 and 2028 and 175,00 EUR after -- with 475,00 EUR credited at
``t = 0`` for the 2026 contribution year.  Payment is annual
(``prem_freq_load = 1.0000``), there is no *Beitragsfreistellung*, and the opening balances
are ``dk_pp_init = 3 860,50``, ``surplus_pp_init = 150,48`` and ``guar_pp_init = 4 369,92``,
so the cell opens 358,94 EUR **under** its own guarantee.  A 30 % *Teilkapitalauszahlung* is
elected, the guaranteed *Rentenfaktor* is 29,00 EUR per 10 000 EUR per month, the
*Rentengarantiezeit* is ten years and the declared-rate scenario is ``base`` at 2,30 %.
Hence ``t_conv() = 17`` (attained 67, calendar 2044) and ``proj_len() = 61`` periods on the
0-based frame ``t = 0 ... 60``: accumulation runs ``t = 0 ... 16`` and the lifelong annuity
``t = 17 ... 60``.  Model point 1 is that cell.

The goldens are hard-coded rather than pickled so a reviewer can compare them with the notes
by eye.  Tolerances follow the precision the notes display: money to the cent, counts to six
decimals.  The projection is sixty-one periods long, so the notes print the eighteen
accumulation-and-conversion rows in full and a representative set of payout rows; both are
asserted here, with the **full-precision** totals -- ``net_cf`` of -7 827,39 EUR that way
against -7 827,43 EUR if the sixty-one already-rounded cells are added.

Beyond the worked example this module asserts the notes' four independent rebuilds
(the first period ``t = 0`` from the statute up, the conversion year, the aggregate account
roll-forward with the exit charge that closes it, and the four-way decrement closure to
1.00000000), the two variants (model point 11's binding *Garantielücke* of 518,28 EUR and
model point 5's *Kleinbetragsrenten-Abfindung*), the six ``check_*`` identities with their
residuals, the product's own invariants, and **one test per numbered modeling pitfall** --
the eighteen ways an implementation of *this* product looks right and is wrong:

1.  the two subsidy lags are **different lags**, one calendar and one projection;
2.  the final contribution year's Zulage is credited **at** ``t_conv()``;
3.  the § 86 Kürzung is **proportional**, not a cliff edge;
4.  the Zulage is a **contribution**, published in its own positive column;
5.  the *Günstigerprüfung* top-up is not a contract cash flow and has no cells;
6.  the two *Kinderzulage* rates are a **birth-cohort** split and run together;
7.  the *Beitragsgarantie* is tested **once**, at *Rentenbeginn*, and floors no benefit;
8.  the biometric carve-out is capped at 20 % of total contributions;
9.  **unsubsidised** contributions are inside the guarantee;
10. the declared rate **includes** the *Rechnungszins* and is not added to it;
11. the *Ratenzuschlag* is a **charge** and never reaches the account;
12. the acquisition charge is spread over five contract years and survives a paid-up year;
13. an *Anbieterwechsel* is a **separate decrement** from a *Kündigung*;
14. *Beitragsfreistellung* is a **state change**, not a termination;
15. the two phases use **different mortality bases**, and the annuity basis is generational;
16. the *Kleinbetragsrente* is tested on the **post-lump-sum** annuity against a flat threshold;
17. the *Rentengarantiezeit* changes the **payment count**, never the payment;
18. every benefit is published **gross** of the *Rückzahlungsbetrag*.

The whole-model-point-table sweep is deliberately absent: it belongs to
tests/test_model_conventions_de.py, which owns the library's single sweep.
"""
import modelx as mx
import pytest
from pytest import approx
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which is
    routine once the autodoc API pages have been built, and is not part of the model.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Riester_DE_S"][0]
INPUT_DIR = MODEL_DIR.parent

CLAIM_KINDS = ("DEATH", "LAPSE", "TRANSFER", "LUMPSUM", "COMMUTATION", "ANNUITY")

RESULT_CF_COLUMNS = [
    "pols_if", "pols_annuity_pay", "premiums", "zulagen",
    "claims_death", "claims_lapse", "claims_transfer", "claims_lumpsum",
    "claims_commutation", "claims_annuity", "expenses", "commissions",
    "net_cf", "liability_cf",
]

# The notes' worked-example table in full, on the ANNUAL clock: the monthly frame summed
# into projection years by result_cf_annual(), with int_credited read from result_acct(),
# the annual state.
# k: (pols_if, premiums, zulagen, int_credited, claims_death, claims_lapse,
#     claims_transfer, claims_lumpsum, claims_annuity, expenses, commissions, net_cf)
# claims_commutation is 0.00 at every k here -- the anchor's annuity clears the
# Kleinbetragsrente threshold -- and is asserted in the row test rather than tabulated.
WORKED_EXAMPLE = {
    0:  (1.000000, 1205.00, 475.00, 125.21,   6.62,  43.39,  65.90,      0.00,   0.00, 33.21, 25.20,  1505.67),
    1:  (0.978920, 1212.49, 464.99, 158.37,   9.21,  54.88,  83.52,      0.00,   0.00, 33.14, 25.16,  1471.56),
    2:  (0.958169, 1507.08, 455.13, 201.64,  12.93,  52.48,  79.96,      0.00,   0.00, 32.75, 29.43,  1754.65),
    3:  (0.942478, 1515.34, 164.93, 239.74,  16.91,  62.39,  95.15,      0.00,   0.00, 32.85, 25.20,  1447.77),
    4:  (0.926909, 1523.36, 162.21, 278.17,  21.59,  72.38, 110.47,      0.00,   0.00, 32.93, 25.28,  1422.92),
    5:  (0.911451, 1531.11, 159.50, 316.90,  27.05,  82.45, 125.90,      0.00,   0.00, 33.02, 25.36,  1396.83),
    6:  (0.896093, 1538.55, 156.82, 355.91,  33.42,  92.59, 141.44,      0.00,   0.00, 33.10, 25.43,  1369.38),
    7:  (0.880824, 1545.66, 154.14, 395.18,  40.91,  68.62, 104.84,      0.00,   0.00, 32.90, 25.50,  1427.04),
    8:  (0.869997, 1560.24, 152.25, 436.87,  49.75,  75.86, 115.91,      0.00,   0.00, 33.14, 25.69,  1412.15),
    9:  (0.859103, 1574.53, 150.34, 479.17,  60.03,  83.19, 127.15,      0.00,   0.00, 33.37, 25.87,  1395.26),
    10: (0.848126, 1588.46, 148.42, 522.04,  71.94,  90.62, 138.53,      0.00,   0.00, 33.60, 26.05,  1376.14),
    11: (0.837051, 1602.01, 146.48, 565.45,  85.71,  98.14, 150.05,      0.00,   0.00, 33.83, 26.23,  1354.54),
    12: (0.825864, 1589.79, 144.53, 608.79, 101.51, 105.64, 161.54,      0.00,   0.00, 34.04, 26.01,  1305.57),
    13: (0.814546, 1568.00, 142.55, 651.80, 119.55, 113.08, 172.94,      0.00,   0.00, 34.25, 25.66,  1245.07),
    14: (0.803079, 1545.93, 140.54, 694.42, 140.11, 120.45, 184.22,      0.00,   0.00, 34.44, 25.30,  1181.95),
    15: (0.791444, 1523.53, 138.50, 736.58, 163.47, 127.73, 195.38,      0.00,   0.00, 34.62, 24.93,  1115.90),
    16: (0.779621, 1500.77, 136.43, 778.20, 189.98, 134.91, 206.38,      0.00,   0.00, 34.79, 24.56,  1046.59),
    17: (0.767588,    0.00, 134.33,   0.00,   0.00,   0.00,   0.00, 10536.61, 855.57, 18.81,  0.00, -11276.67),
}

# The first thirteen months of the monthly frame -- the saw-tooth the annual table hides.
# The whole year's contribution and Zulage land in month 0 and nothing else does; the other
# eleven carry a twelfth of the maintenance expense and that month's exits.
# t: (pols_if, premiums, zulagen, claims_death, claims_lapse, claims_transfer, expenses,
#     commissions, net_cf)
MONTHS_YEAR_0 = {
    0:  (1.000000, 1205.00, 475.00, 0.56, 3.65, 5.55, 2.79, 25.20, 1642.25),
    1:  (0.998226,    0.00,   0.00, 0.56, 3.64, 5.54, 2.79,  0.00,  -12.53),
    11: (0.980659,    0.00,   0.00, 0.55, 3.58, 5.44, 2.74,  0.00,  -12.31),
    12: (0.978920, 1212.49, 464.99, 0.78, 4.62, 7.03, 2.79, 25.16,  1637.10),
}

# The notes' Total row: all sixty-one years, summed at full precision and then rounded.
TOTALS = {
    "premiums": 25631.84, "zulagen": 3627.10, "int_credited": 7544.45,
    "claims_death": 1150.72, "claims_lapse": 1478.78, "claims_transfer": 2259.27,
    "claims_lumpsum": 10536.61, "claims_commutation": 0.00, "claims_annuity": 19793.08,
    "expenses": 1057.57, "commissions": 436.87, "net_cf": -7453.96,
}

# What the annual-step model this replaced produced.  The contribution, the Zulage, the
# interest credited, the commission and the lump sum are unchanged -- and so are both
# balances, the guarantee accumulator, the capital at Rentenbeginn and the
# Kleinbetragsrente verdict.  The annuity falls because the instalment now stops with the
# month of death; the expenses fall because a mid-year exit bears only the months it was
# there; and the three decrements redistribute because they now compete month by month
# instead of running in sequence at a year end.
ANNUAL_GRID_WAS = {
    "claims_death": 1156.35, "claims_lapse": 1481.42, "claims_transfer": 2250.97,
    "claims_annuity": 20154.82, "expenses": 1069.29, "net_cf": -7827.39,
}
ANNUAL_GRID_UNCHANGED = {
    "premiums": 25631.84, "zulagen": 3627.10, "claims_lumpsum": 10536.61,
    "commissions": 436.87,
}

# The same columns if the sixty-one *rounded* annual cells are added instead.  Ten of the
# eleven differ; the notes say so, and so does the test below.
ROUNDED_CELL_SUMS = {
    "premiums": 25631.85, "zulagen": 3627.09, "int_credited": 7544.44,
    "claims_death": 1150.69, "claims_lapse": 1478.80, "claims_transfer": 2259.28,
    "claims_lumpsum": 10536.61, "claims_annuity": 19793.06, "expenses": 1057.53,
    "commissions": 436.86, "net_cf": -7453.97,
}

# The notes' payout table: (age, pols_if, pols_annuity_pay, claims_annuity, expenses,
# net_cf), all at the start of projection year k, and the k = 18 ... 60 subtotal beneath it.
PAYOUT_ROWS = {
    17: (67, 0.767588, 0.767588, 855.57, 18.81, -11276.67),
    18: (68, 0.762677, 0.767588, 855.57, 18.85, -874.43),
    26: (76, 0.701403, 0.767588, 855.57, 19.33, -874.91),
    27: (77, 0.690013, 0.690013, 762.71, 17.42, -780.13),
    28: (78, 0.677530, 0.677530, 748.18, 17.20, -765.39),
    34: (84, 0.574463, 0.574463, 628.63, 15.35, -643.98),
    44: (94, 0.273819, 0.273819, 286.52, 9.02, -295.54),
    54: (104, 0.016013, 0.016013, 13.95, 0.85, -14.81),
    60: (110, 0.000079, 0.000079, 0.09, 0.01, -0.10),
}
PAYOUT_SUBTOTAL = {"pols_if": 17.024474, "pols_annuity_pay": 17.314559,
                   "claims_annuity": 18937.51, "expenses": 468.77, "net_cf": -19406.28}

# The Rentengarantiezeit is 12 x 10 = 120 monthly instalments, t = 204 ... 323, and inside
# it the count is frozen -- so those ten years are the annual-step model's TO THE CENT.
GUARANTEE_WINDOW = {"first": 204, "last": 323, "instalments": 120, "total": 8555.73}

# The anchor's conversion at k = 17, from the notes' second independent rebuild.
CONVERSION = {
    "dk_pp": 36172.815098, "surplus_acct_pp": 8224.490372, "raw_account": 44553.305470,
    "slueb_pp": 757.544616, "bewres_pp": 445.533055, "account_conv_pp": 45756.383140,
    "guar": 37877.2308, "ann_factor": 20.8722287915, "rentenfaktor_curr": 27.947822,
    "teilkapital_pp": 13726.914942, "annuity_capital_pp": 32029.468198,
    "annuity_month_pp": 92.885458, "annuity_pp": 1114.625493, "pols_conv": 0.7675876849,
}

# The notes' four-way decrement closure over the whole 732-month projection.
CLOSURE = {"deaths_accum": 0.04110900, "deaths_payout": 0.76758768,
           "lapses": 0.07648390, "transfers": 0.11481942}

# Variant 1 -- model point 11, the low declared-rate cell on which the guarantee binds.
# Same column order as WORKED_EXAMPLE.
VARIANT_LOW = {
    0:  (1.000000, 1625.00, 475.00, 35.08, 21.75,  54.89,  83.51,    0.00,   0.00, 33.34, 31.50,  1875.01),
    1:  (0.977045, 1587.70, 464.10, 43.81, 29.87,  68.53, 104.44,    0.00,   0.00, 33.21, 30.78,  1784.97),
    2:  (0.954320, 1837.07, 453.30, 53.94, 40.55,  63.36,  96.64,    0.00,   0.00, 32.76, 34.36,  2022.69),
    3:  (0.936516, 1802.79, 163.89, 62.58, 51.76,  73.50, 112.18,    0.00,   0.00, 32.79, 29.50,  1666.97),
    4:  (0.918697, 1768.49, 160.77, 70.91, 64.50,  83.25, 127.13,    0.00,   0.00, 32.80, 28.94,  1592.64),
    5:  (0.900842, 1734.12, 157.65, 78.90, 78.95,  92.62, 141.48,    0.00,   0.00, 32.81, 28.38,  1517.53),
    6:  (0.882930, 1699.64, 154.51, 86.57, 95.28, 101.59, 155.23,    0.00,   0.00, 32.80, 27.81,  1441.44),
    7:  (0.864938,    0.00, 151.36,  0.00,  0.00,   0.00,   0.00, 5449.11, 442.47, 21.28,  0.00, -5761.50),
    8:  (0.858363,    0.00,   0.00,  0.00,  0.00,   0.00,   0.00,    0.00, 442.47, 21.33,  0.00,  -463.80),
    19: (0.731563,    0.00,   0.00,  0.00,  0.00,   0.00,   0.00,    0.00, 369.87, 18.84,  0.00,  -388.71),
    50: (0.000061,    0.00,   0.00,  0.00,  0.00,   0.00,   0.00,    0.00,   0.03,  0.01,  0.00,    -0.04),
}
VARIANT_LOW_TOTALS = {
    "premiums": 12054.81, "zulagen": 2180.59, "int_credited": 431.80,
    "claims_death": 382.67, "claims_lapse": 537.73, "claims_transfer": 820.61,
    "claims_lumpsum": 5449.11, "claims_commutation": 0.00, "claims_annuity": 9937.96,
    "expenses": 765.94, "commissions": 211.26, "net_cf": -3869.89,
}
VARIANT_LOW_CONVERSION = {
    "raw_account": 19863.088636, "slueb_pp": 420.00, "bewres_pp": 198.630886,
    "account_conv_pp": 20481.719523, "garantieluecke_conv_pp": 518.280477,
    "pols_conv": 0.8649383502,
}

# Variant 2 -- model point 5, the *mittelbar* eligible spouse at the Sockelbeitrag, which
# commutes rather than annuitising, so claims_commutation stands where the lump sum would.
# k: (pols_if, premiums, zulagen, int_credited, claims_death, claims_lapse,
#     claims_transfer, claims_commutation, expenses, commissions, net_cf)
VARIANT_FIXED = {
    0:  (1.000000, 60.00, 175.00, 32.74,  3.07,  8.52, 12.60,    0.00, 34.88, 3.52,   172.40),
    1:  (0.982960, 58.98, 172.02, 37.75,  3.90,  9.82, 14.60,    0.00, 34.96, 3.46,   164.24),
    10: (0.856985, 51.42, 149.97, 81.96, 20.01, 14.21, 21.50,    0.00, 36.10, 3.02,   106.55),
    11: (0.843758,  0.00, 147.66,  0.00,  0.00,  0.00,  0.00, 3828.31,  0.00, 0.00, -3680.65),
    12: (0.000000,  0.00,   0.00,  0.00,  0.00,  0.00,  0.00,    0.00,  0.00, 0.00,     0.00),
    54: (0.000000,  0.00,   0.00,  0.00,  0.00,  0.00,  0.00,    0.00,  0.00, 0.00,     0.00),
}
VARIANT_FIXED_TOTALS = {
    "premiums": 609.80, "zulagen": 1926.26, "int_credited": 631.80,
    "claims_death": 108.18, "claims_lapse": 123.53, "claims_transfer": 185.58,
    "claims_lumpsum": 0.00, "claims_commutation": 3828.31, "claims_annuity": 0.00,
    "expenses": 388.54, "commissions": 35.83, "net_cf": -2133.91,
}


# --------------------------------------------------------------------------- worked example

@pytest.mark.parametrize("k", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_riester_anchor, k):
    """Every cell of the notes' eighteen accumulation-and-conversion rows, to the cent.

    The cash flows come from ``result_cf_annual()`` -- the monthly frame summed into
    projection years -- and the interest credit from ``result_acct()``, the annual state.
    Both are indexed by ``k``, which is the annual-step model's own ``t``.

    ``claims_commutation`` is zero at every k here: 92,89 EUR a month clears the 39,55 EUR
    *Kleinbetragsrente* threshold comfortably.
    """
    pols, prem, zul, intc, cd, cl, ct, clump, cann, exp, comm, net = WORKED_EXAMPLE[k]
    p = de_riester_anchor
    row = p.result_cf_annual().loc[k]
    assert row["pols_if"] == approx(pols, abs=SIX_DP)
    assert p.pols_if(12 * k) == approx(pols, abs=SIX_DP)
    assert row["premiums"] == approx(prem, abs=CENT)
    assert row["zulagen"] == approx(zul, abs=CENT)
    assert p.int_credited(k) == approx(intc, abs=CENT)
    assert p.result_acct().loc[k, "int_credited"] == approx(intc, abs=CENT)
    assert row["claims_death"] == approx(cd, abs=CENT)
    assert row["claims_lapse"] == approx(cl, abs=CENT)
    assert row["claims_transfer"] == approx(ct, abs=CENT)
    assert row["claims_lumpsum"] == approx(clump, abs=CENT)
    assert row["claims_annuity"] == approx(cann, abs=CENT)
    assert row["claims_commutation"] == 0.0
    assert row["expenses"] == approx(exp, abs=CENT)
    assert row["commissions"] == approx(comm, abs=CENT)
    assert row["net_cf"] == approx(net, abs=CENT)
    assert row["liability_cf"] == approx(-net, abs=CENT)
    # The annual row is the twelve monthly rows and nothing else, and the whole year's
    # contribution and Zulage fall in its first month.
    months = p.result_cf().iloc[12 * k:12 * k + 12]
    assert months["net_cf"].sum() == approx(net, abs=CENT)
    assert p.premiums(12 * k) == approx(prem, abs=CENT)
    assert p.zulagen(12 * k) == approx(zul, abs=CENT)
    assert all(p.premiums(12 * k + i) == 0.0 for i in range(1, 12))
    assert all(p.zulagen(12 * k + i) == 0.0 for i in range(1, 12))


@pytest.mark.parametrize("t", sorted(MONTHS_YEAR_0))
def test_the_first_months_of_the_monthly_frame(de_riester_anchor, t):
    """The saw-tooth the annual table hides: one month of contribution, eleven without.

    The *Ratenzuschlag* prices a fractionated payment mode by loading the **amount**, so the
    whole year's *Eigenbeitrag* falls in the first month of a projection year whatever
    ``prem_freq`` says; the ZfA does not fractionate at all.
    """
    pols, prem, zul, cd, cl, ct, exp, comm, net = MONTHS_YEAR_0[t]
    p = de_riester_anchor
    assert p.pols_if(t) == approx(pols, abs=SIX_DP)
    assert p.premiums(t) == approx(prem, abs=CENT)
    assert p.zulagen(t) == approx(zul, abs=CENT)
    assert p.claims(t, "DEATH") == approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == approx(cl, abs=CENT)
    assert p.claims(t, "TRANSFER") == approx(ct, abs=CENT)
    assert p.expenses(t) == approx(exp, abs=CENT)
    assert p.commissions(t) == approx(comm, abs=CENT)
    assert p.net_cf(t) == approx(net, abs=CENT)
    assert p.prem_due(t) is (t % 12 == 0)


@pytest.mark.parametrize("k", sorted(PAYOUT_ROWS))
def test_the_payout_phase_rows(de_riester_anchor, k):
    """The notes' payout table, and the five columns that are zero from k = 17 onward.

    The account is extinguished at conversion, so there is no interest to credit and a death
    pays nothing outside the *Rentengarantiezeit*.  ``zulagen`` is the exception at k = 17:
    the final contribution year's subsidy lands in the conversion year.
    """
    age, pols, pay, ann, exp, net = PAYOUT_ROWS[k]
    p = de_riester_anchor
    row = p.result_cf_annual().loc[k]
    assert p.age_y(k) == age == p.age(12 * k)
    assert row["pols_if"] == approx(pols, abs=SIX_DP)
    assert row["pols_annuity_pay"] == approx(pay, abs=SIX_DP)
    assert row["claims_annuity"] == approx(ann, abs=CENT)
    assert row["expenses"] == approx(exp, abs=CENT)
    assert row["net_cf"] == approx(net, abs=CENT)
    assert row["premiums"] == 0.0 and p.int_credited(k) == 0.0
    assert row["claims_death"] == row["claims_lapse"] == row["claims_transfer"] == 0.0
    assert row["zulagen"] == (approx(134.33, abs=CENT) if k == 17 else 0.0)


def test_the_rente_is_paid_one_instalment_a_month(de_riester_anchor):
    """What the monthly grid buys on this product, and what it leaves alone.

    Inside the *Rentengarantiezeit* the count is frozen, so 120 monthly instalments on a
    fixed count are ten annual payments on it and the two grids agree **to the cent**.  After
    the window the instalment stops with the month of death rather than being paid for the
    whole year of it, which is the whole of the 361,74 EUR difference.
    """
    p = de_riester_anchor
    df = p.result_cf()
    first, last = GUARANTEE_WINDOW["first"], GUARANTEE_WINDOW["last"]
    assert p.t_conv() == first == 12 * p.k_conv()
    assert last == first + 12 * p.rentengarantie_years() - 1
    assert p.annuity_month_pp() == approx(CONVERSION["annuity_month_pp"], abs=5e-6)
    assert 12 * p.annuity_month_pp() == approx(p.annuity_pp(p.k_conv()), rel=1e-12)
    # Every instalment in the window is the same amount on the same frozen count.
    for t in (first, first + 1, last):
        assert p.pols_annuity_pay(t) == approx(p.pols_conv(), rel=1e-12)
        assert p.claims(t, "ANNUITY") == approx(
            p.annuity_month_pp() * p.pols_conv(), abs=CENT)
    assert p.pols_annuity_pay(last + 1) == approx(p.pols_if(last + 1), rel=1e-12)
    assert df["claims_annuity"].iloc[first:last + 1].sum() == approx(
        GUARANTEE_WINDOW["total"], abs=CENT)
    assert GUARANTEE_WINDOW["total"] == approx(
        GUARANTEE_WINDOW["instalments"] * p.annuity_month_pp() * p.pols_conv(), abs=CENT)
    # And the whole payout phase is below the annual booking it replaced.
    assert df["claims_annuity"].sum() == approx(TOTALS["claims_annuity"], abs=CENT)
    assert (ANNUAL_GRID_WAS["claims_annuity"]
            - df["claims_annuity"].sum()) == approx(361.74, abs=0.01)


def test_the_totals_are_summed_at_full_precision(de_riester_anchor):
    """The Total row is a full-precision sum over all 732 months, then rounded.

    Ten of the eleven columns differ from the sum of the already-rounded **annual** cells.
    The payout subtotal is checked here too: 17.314559 instalment-years paid against
    17.024474 policy-years in force, the whole difference being the *Rentengarantiezeit*.
    """
    p = de_riester_anchor
    df, ann, acct = p.result_cf(), p.result_cf_annual(), p.result_acct()
    assert len(df) == 732 and len(ann) == 61
    for column, total in TOTALS.items():
        if column == "int_credited":
            assert acct[column].sum() == approx(total, abs=CENT), column
            continue
        assert df[column].sum() == approx(total, abs=CENT), column
        assert ann[column].sum() == approx(df[column].sum(), abs=1e-9), column
    for column, rounded in ROUNDED_CELL_SUMS.items():
        source = acct if column == "int_credited" else ann
        assert sum(round(v, 2) for v in source[column]) == approx(rounded, abs=CENT), column
    differing = sorted(c for c in ROUNDED_CELL_SUMS
                       if abs(ROUNDED_CELL_SUMS[c] - TOTALS[c]) > 1e-9)
    assert differing == sorted(["premiums", "zulagen", "int_credited", "claims_death",
                                "claims_lapse", "claims_transfer", "claims_annuity",
                                "expenses", "commissions", "net_cf"])
    tail = ann.loc[18:60]
    for column, total in PAYOUT_SUBTOTAL.items():
        tol = SIX_DP if column.startswith("pols") else CENT
        assert tail[column].sum() == approx(total, abs=tol), column
    assert tail["pols_annuity_pay"].sum() - tail["pols_if"].sum() == approx(0.290085,
                                                                            abs=SIX_DP)


def test_what_the_monthly_grid_moved_and_what_it_did_not(de_riester_anchor):
    """The accumulation is the annual-step model's; the Rente and the exit split are not.

    Naming both halves is the point: a conversion that changed the contribution, the Zulage
    or the guarantee would be a different model rather than a finer grid.
    """
    p = de_riester_anchor
    df = p.result_cf()
    for column, unchanged in ANNUAL_GRID_UNCHANGED.items():
        assert df[column].sum() == approx(unchanged, abs=CENT), column
    assert p.result_acct()["int_credited"].sum() == approx(7544.45, abs=CENT)
    assert p.capital_conv_pp() == approx(CONVERSION["account_conv_pp"], abs=CENT)
    assert p.garantieluecke_conv_pp() == 0.0
    assert p.is_kleinbetrag() is False
    # The three accumulation decrements now compete month by month, where the annual model
    # ran them in sequence at one year end: deaths and surrenders fall, transfers rise, and
    # the survivorship at every anniversary is unchanged.
    assert df["claims_death"].sum() < ANNUAL_GRID_WAS["claims_death"]
    assert df["claims_lapse"].sum() < ANNUAL_GRID_WAS["claims_lapse"]
    assert df["claims_transfer"].sum() > ANNUAL_GRID_WAS["claims_transfer"]
    assert ANNUAL_GRID_WAS["claims_death"] - df["claims_death"].sum() == approx(5.62, abs=0.01)
    assert df["claims_transfer"].sum() - ANNUAL_GRID_WAS["claims_transfer"] == approx(
        8.30, abs=0.01)
    # A mid-year exit bears only the months it was there.
    assert ANNUAL_GRID_WAS["expenses"] - df["expenses"].sum() == approx(11.72, abs=0.01)
    assert df["net_cf"].sum() == approx(TOTALS["net_cf"], abs=CENT)


# --------------------------------------------------------------------------- the rebuilds

def test_projection_year_one_rebuilt_from_the_statute_up(de_riester_anchor):
    """The first projected **month**, ``t = 0``, reconstructed a different way, in one pass.

    ``Y(0) = 42 000``; ``Z*(0) = 175 + 300 = 475``; ``M(0) = max(60, min(0,04 x 42 000,
    2 100) - 475) = 1 205``; ``K_a = 0,025 x 33 600 / 5 = 168``; ``K_v = 0,04 x 1 680 + 12``;
    ``S(0) = 1 432,80``; interest ``0,023 x (3 860,50 + 1 432,80 + 150,48)``.
    """
    p = de_riester_anchor
    assert p.income_ref(0) == approx(42000.00, abs=CENT)
    assert p.zulage_entitlement_pp(0) == approx(175.00 + 300.00, abs=CENT)
    assert p.mindesteigenbeitrag_pp(0) == approx(
        max(60.0, min(0.04 * 42000.0, 2100.0) - 475.0), abs=CENT)
    assert p.mindesteigenbeitrag_pp(0) == approx(1205.00, abs=CENT)
    assert p.eigenbeitrag_pp(0) == p.eigenbeitrag_paid_pp(0) == approx(1205.0, abs=CENT)
    assert p.zulage_pp(0) == approx(475.00, abs=CENT)
    assert p.contrib_total_pp(0) == approx(1680.00, abs=CENT)
    assert p.acq_charge_pp(0) == approx(0.025 * 33600.0 / 5, abs=CENT)
    assert p.admin_charge_pp(0) == approx(0.04 * 1680.0 + 12.0, abs=CENT)
    assert p.prem_to_av_pp(0) == approx(1680.00 - 168.00 - 79.20, abs=CENT)
    assert p.int_credited_pp(0) == approx(0.023 * (3860.50 + 1432.80 + 150.48), abs=CENT)
    assert p.int_credited_pp(0) == approx(125.206940, abs=CENT)
    assert p.av_total_pp(1) == approx(5568.986940, abs=CENT)
    # The decrements at attained age 50, contract duration 4: the ANNUAL rates, and the
    # geometric twelfths the recursion applies, in the stated order within the month.
    assert p.mort_rate(0) == approx(0.001500 * 0.80, rel=1e-12)
    assert p.lapse_rate(0) == 0.008 and p.transfer_rate(0) == 0.012
    q_mth = 1.0 - (1.0 - 0.0012) ** (1.0 / 12.0)
    w_mth = 1.0 - (1.0 - 0.008) ** (1.0 / 12.0)
    th_mth = 1.0 - (1.0 - 0.012) ** (1.0 / 12.0)
    assert p.mort_rate_mth(0) == approx(q_mth, rel=1e-12)
    assert p.lapse_rate_mth(0) == approx(w_mth, rel=1e-12)
    assert p.transfer_rate_mth(0) == approx(th_mth, rel=1e-12)
    assert p.pols_death(0) == approx(q_mth, rel=1e-12)
    assert p.pols_lapse(0) == approx((1 - q_mth) * w_mth, rel=1e-12)
    assert p.pols_transfer(0) == approx((1 - q_mth) * (1 - w_mth) * th_mth, rel=1e-12)
    # Twelve of each compound back to the annual rate, so the year's survivorship -- and
    # every account balance that hangs off it -- is the annual-step model's exactly.
    assert (1 - q_mth) ** 12 == approx(1 - 0.0012, rel=1e-14)
    assert p.pols_if(12) == approx(0.9988 * 0.992 * 0.988, rel=1e-12)
    # The benefits struck on the ANNUAL A(1), then the expenses: a twelfth of the annual
    # maintenance, inflated on *contract* duration, plus the per-event claim expense whole.
    assert p.claims(0, "DEATH") == approx(5568.986940 * q_mth, abs=CENT)
    assert p.claims(0, "LAPSE") == approx(
        0.98 * 5568.98694 * (1 - q_mth) * w_mth, abs=CENT)
    assert p.claims(0, "TRANSFER") == approx(
        (5568.98694 - 50.0) * (1 - q_mth) * (1 - w_mth) * th_mth, abs=CENT)
    assert p.expenses(0) == approx(
        30.0 * 1.02 ** 3 / 12.0
        + 80.0 * (p.pols_death(0) + p.pols_lapse(0) + p.pols_transfer(0)), abs=CENT)
    assert p.commissions(0) == approx(0.015 * (1205.00 + 475.00), abs=CENT)
    assert p.net_cf(0) == approx(
        1680.00 - p.claims(0, "DEATH") - p.claims(0, "LAPSE") - p.claims(0, "TRANSFER")
        - p.expenses(0) - 25.20, abs=CENT)
    assert p.net_cf(0) == approx(1642.25, abs=CENT)


def test_the_conversion_year_rebuilt_a_different_way(de_riester_anchor):
    """Everything struck at t = 17, rebuilt from its own parts.

    The raw account is ``D(17) + S(17) + U(17)``, the *Sparbeitrag* being the last Zulage net
    of its charge, ``175 - (0,04 x 175 + 12) = 156,00``.  The *Schlussüberschussanteil* is 2 %
    of the contributions credited over the life of the contract -- exactly the guarantee
    accumulator -- and the *Bewertungsreserven* share is 1 % of the raw account.
    """
    p = de_riester_anchor
    T = p.k_conv()
    assert T == 17 and p.t_conv() == 204
    assert p.dk_pp(T) == approx(CONVERSION["dk_pp"], abs=CENT)
    assert p.surplus_acct_pp(T) == approx(CONVERSION["surplus_acct_pp"], abs=CENT)
    assert p.prem_to_av_pp(T) == approx(175.0 - (0.04 * 175.0 + 12.0), abs=CENT)
    raw = p.dk_pp(T) + p.prem_to_av_pp(T) + p.surplus_acct_pp(T)
    assert raw == approx(CONVERSION["raw_account"], abs=CENT)
    assert p.slueb_pp() == approx(0.02 * p.guar_pp(T + 1), abs=CENT)
    assert p.slueb_pp() == approx(CONVERSION["slueb_pp"], abs=CENT)
    assert p.bewres_pp() == approx(0.01 * raw, abs=CENT)
    assert p.bewres_pp() == approx(CONVERSION["bewres_pp"], abs=CENT)
    assert p.account_conv_pp() == approx(CONVERSION["account_conv_pp"], abs=CENT)
    # The guarantee rebuilt without the recursion: the seed plus the subsidised pool.
    assert p.guar_pp(T + 1) == approx(p.guar_pp_init() + p.pool_gefoerdert_pp(T), abs=CENT)
    assert p.guar_pp(T + 1) == approx(CONVERSION["guar"], abs=CENT)
    assert p.account_conv_pp() - p.guar_pp(T + 1) == approx(7879.15, abs=CENT)
    assert p.capital_conv_pp() == approx(CONVERSION["account_conv_pp"], abs=CENT)
    assert p.garantieluecke_conv_pp() == 0.0
    # The annuity basis, and the two-Rentenfaktor comparison the guarantee wins.
    assert p.ann_factor() == approx(CONVERSION["ann_factor"], abs=5e-9)
    assert p.rentenfaktor_curr() == approx(0.70 * 10000.0 / (12.0 * p.ann_factor()),
                                           rel=1e-12)
    assert p.rentenfaktor_curr() == approx(CONVERSION["rentenfaktor_curr"], abs=5e-7)
    assert p.rentenfaktor_curr() < p.rentenfaktor_guar()
    assert p.rentenfaktor_applied() == approx(29.00, abs=1e-12)
    # The disposal of the capital, and the two conversion-year cash flows of row 17.
    assert p.teilkapital_pp() == approx(0.30 * p.capital_conv_pp(), rel=1e-12)
    assert p.teilkapital_pp() == approx(CONVERSION["teilkapital_pp"], abs=CENT)
    assert p.annuity_capital_pp() == approx(CONVERSION["annuity_capital_pp"], abs=CENT)
    assert p.annuity_month_pp() == approx(
        CONVERSION["annuity_capital_pp"] / 10000.0 * 29.00, abs=CENT)
    assert p.annuity_pp(T) == approx(12.0 * p.annuity_month_pp(), rel=1e-12)
    assert p.annuity_pp(T) == approx(CONVERSION["annuity_pp"], abs=CENT)
    assert p.pols_conv() == approx(CONVERSION["pols_conv"], abs=SIX_DP)
    # Paid in the conversion MONTH, and the annuity one instalment at a time from it.
    assert p.claims(p.t_conv(), "LUMPSUM") == approx(
        p.teilkapital_pp() * p.pols_conv(), rel=1e-12)
    assert p.claims(p.t_conv(), "LUMPSUM") == approx(10536.61, abs=CENT)
    assert all(p.claims(t, "LUMPSUM") == 0.0 for t in (p.t_conv() - 1, p.t_conv() + 1))
    assert p.claims(p.t_conv(), "ANNUITY") == approx(
        p.annuity_month_pp() * p.pols_conv(), abs=CENT)
    assert p.result_cf_annual().loc[T, "claims_annuity"] == approx(855.57, abs=CENT)


def test_the_account_rolls_forward_and_the_exit_charge_closes_it(de_riester_anchor):
    """The aggregate account, and the residue that closes it.

    The account an exiting policy releases either leaves as a benefit or stays with the
    insurer as ``exit_charge_pp``.  Dropping the second -- a *Stornoabzug* and a transfer
    charge look like income rather than like account released -- leaves a residual of
    1,48 EUR in the first period, which is exactly the usual way this identity fails.
    """
    p = de_riester_anchor
    opening_next = p.av_total_at(1, "BEF_PREM")
    assert opening_next == approx(5451.592054, abs=CENT)
    # The account is annual, so the identity is stated per projection year and the year's
    # exits and charges are summed over its twelve months.
    months = range(12)
    charge = sum(p.exit_charge_pp(t) for t in months)
    assert charge == approx(1.482574, abs=CENT)
    out = sum(p.claims(t, "DEATH") + p.claims(t, "LAPSE") + p.claims(t, "TRANSFER")
              for t in months)
    rebuilt = (p.av_total_at(0, "BEF_PREM") + p.prem_to_av_pp(0) * p.pols_if(0)
               + p.int_credited(0) - out - charge)
    assert rebuilt == approx(opening_next, abs=1e-9)
    assert p.check_av_roll_fwd_resid(0) == approx(0.0, abs=1e-9)
    assert rebuilt + charge - opening_next == approx(1.48, abs=CENT)
    # It closes whatever the split of the year's exits between the three decrements, all
    # three releasing the same annual end-of-year account value.
    assert p.db_pp(0) == p.av_total_pp(1)
    assert p.cv_pp(0) == approx(0.98 * p.av_total_pp(1), rel=1e-12)
    # From the conversion year on, the identity asserts that the account is *gone*.
    assert all(p.av_total_pp(k) == 0.0 for k in (18, 19, 39, 60))
    assert p.check_av_roll_fwd() is True


def test_the_decrements_close_four_ways(de_riester_anchor):
    """Deaths in accumulation, deaths in payout, surrenders and transfers sum to one.

    ``mort_rate`` is forced to 1 at ``omega_age = 110`` and ``mort_rate_mth`` places that
    certainty in the terminal year's last month, so ``pols_if(732)`` -- the one index
    beyond the frame -- is exactly zero and the identity is exact.  The split is itself a
    product statement: 23,24 % of the cohort leaves before *Rentenbeginn*, and half again as
    many of those transfer out as surrender.
    """
    p = de_riester_anchor
    n, T = p.proj_len(), p.t_conv()
    assert n == 732 and T == 204
    deaths_accum = sum(p.pols_death(t) for t in range(T))
    deaths_payout = sum(p.pols_death(t) for t in range(T, n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    transfers = sum(p.pols_transfer(t) for t in range(n))
    assert deaths_accum == approx(CLOSURE["deaths_accum"], abs=5e-9)
    assert deaths_payout == approx(CLOSURE["deaths_payout"], abs=5e-9)
    assert lapses == approx(CLOSURE["lapses"], abs=5e-9)
    assert transfers == approx(CLOSURE["transfers"], abs=5e-9)
    assert deaths_accum + deaths_payout + lapses + transfers == approx(1.0, abs=1e-12)
    assert p.pols_if(n) == 0.0 and p.mort_rate(n - 1) == 1.0
    assert p.mort_rate_mth(n - 1) == 1.0 and p.mort_rate_mth(n - 2) == 0.0
    before = deaths_accum + lapses + transfers
    assert before == approx(0.2324, abs=5e-5)
    assert transfers / before == approx(0.494, abs=5e-4)
    assert lapses / before == approx(0.329, abs=5e-4)
    assert p.check_pols_roll_fwd() is True


def test_the_statement_reconciles_on_the_totals(de_riester_anchor):
    """check_net_cf() in aggregate, on the notes' Total row.

    ``25 631,84 + 3 627,10 - 35 218,47 - 1 057,57 - 436,87 = -7 453,96``, the middle term
    being the sum of all six ``claims_*`` columns.  ``int_credited`` of 7 544,45 EUR is
    **not** in it -- and on the monthly grid it is not a column of this frame at all:
    adding it would report the cell's undiscounted deficit as 90,49 EUR.
    """
    p = de_riester_anchor
    df = p.result_cf()
    claims = sum(df["claims_" + k.lower()].sum() for k in CLAIM_KINDS)
    assert claims == approx(35218.47, abs=CENT)
    assert (df["premiums"].sum() + df["zulagen"].sum() - claims - df["expenses"].sum()
            - df["commissions"].sum()) == approx(-7453.96, abs=CENT)
    interest = p.result_acct()["int_credited"].sum()
    assert df["net_cf"].sum() + interest == approx(90.49, abs=CENT)


# --------------------------------------------------------------------------- variant 1

@pytest.mark.parametrize("k", sorted(VARIANT_LOW))
def test_variant_low_scenario_row(riester_rente, k):
    """The notes' Variant 1 table: model point 11 on the ``low`` scenario, by projection year."""
    pols, prem, zul, intc, cd, cl, ct, clump, cann, exp, comm, net = VARIANT_LOW[k]
    p = riester_rente.Projection[11]
    row = p.result_cf_annual().loc[k]
    assert p.scenario_id() == "low"
    assert row["pols_if"] == approx(pols, abs=SIX_DP)
    assert row["premiums"] == approx(prem, abs=CENT)
    assert row["zulagen"] == approx(zul, abs=CENT)
    assert p.int_credited(k) == approx(intc, abs=CENT)
    assert row["claims_death"] == approx(cd, abs=CENT)
    assert row["claims_lapse"] == approx(cl, abs=CENT)
    assert row["claims_transfer"] == approx(ct, abs=CENT)
    assert row["claims_lumpsum"] == approx(clump, abs=CENT)
    assert row["claims_annuity"] == approx(cann, abs=CENT)
    assert row["expenses"] == approx(exp, abs=CENT)
    assert row["commissions"] == approx(comm, abs=CENT)
    assert row["net_cf"] == approx(net, abs=CENT)


def test_the_guarantee_binds_on_the_low_scenario(riester_rente):
    """The number the product exists to produce: garantieluecke_conv_pp() = 518,28 EUR.

    The 2 100 EUR ceiling binds in every contribution year here, so the accumulator lands on
    a round 21 000,00 EUR and the annuity is struck on the **guaranteed** capital rather than
    on the account.  It is a declared-rate result, not a *Rechnungszins* result: the same cell
    on ``base`` reaches an account above the guarantee and the gap is zero.
    """
    p = riester_rente.Projection[11]
    T = p.k_conv()
    assert T == 7 and p.t_conv() == 84
    assert p.proj_len_y() == 51 and p.proj_len() == 612
    raw = p.dk_pp(T) + p.prem_to_av_pp(T) + p.surplus_acct_pp(T)
    assert raw == approx(VARIANT_LOW_CONVERSION["raw_account"], abs=CENT)
    assert p.slueb_pp() == approx(VARIANT_LOW_CONVERSION["slueb_pp"], abs=CENT)
    assert p.bewres_pp() == approx(VARIANT_LOW_CONVERSION["bewres_pp"], abs=CENT)
    assert p.account_conv_pp() == approx(VARIANT_LOW_CONVERSION["account_conv_pp"],
                                         abs=CENT)
    assert p.guar_pp(T + 1) == p.capital_conv_pp() == approx(21000.00, abs=CENT)
    assert p.capital_conv_pp() > p.account_conv_pp()
    assert p.garantieluecke_conv_pp() == approx(518.280477, abs=CENT)
    assert p.garantieluecke_conv_pp() / p.capital_conv_pp() == approx(0.0247, abs=5e-4)
    assert p.teilkapital_pp() == approx(6300.00, abs=CENT)
    assert p.annuity_capital_pp() == approx(14700.00, abs=CENT)
    assert p.annuity_month_pp() == approx(14700.0 / 10000.0 * 29.00, abs=CENT)
    assert p.annuity_pp(T) == approx(511.56, abs=CENT)
    assert p.claims(p.t_conv(), "LUMPSUM") == approx(
        6300.0 * VARIANT_LOW_CONVERSION["pols_conv"], abs=CENT)
    assert p.check_conversion() is True
    df, acct = p.result_cf(), p.result_acct()
    for column, total in VARIANT_LOW_TOTALS.items():
        source = acct if column == "int_credited" else df
        assert source[column].sum() == approx(total, abs=CENT), column


# --------------------------------------------------------------------------- variant 2

@pytest.mark.parametrize("k", sorted(VARIANT_FIXED))
def test_variant_fixed_form_row(riester_rente, k):
    """The *mittelbar* spouse at the 60,00 EUR Sockelbeitrag.

    ``income_id = zero`` and ``contrib_form = fixed``, so ``M(k) = max(60, min(0, 2 100) -
    175) = 60,00`` and the floor binds by construction.  The frame carries zeros to the last
    month rather than being truncated after the *Abfindung*.
    """
    pols, prem, zul, intc, cd, cl, ct, ccom, exp, comm, net = VARIANT_FIXED[k]
    p = riester_rente.Projection[5]
    row = p.result_cf_annual().loc[k]
    assert p.contrib_form() == "fixed" and p.contrib_fixed_pp() == 60.0
    assert row["pols_if"] == approx(pols, abs=SIX_DP)
    assert row["premiums"] == approx(prem, abs=CENT)
    assert row["zulagen"] == approx(zul, abs=CENT)
    assert p.int_credited(k) == approx(intc, abs=CENT)
    assert row["claims_death"] == approx(cd, abs=CENT)
    assert row["claims_lapse"] == approx(cl, abs=CENT)
    assert row["claims_transfer"] == approx(ct, abs=CENT)
    assert row["claims_commutation"] == approx(ccom, abs=CENT)
    assert row["claims_lumpsum"] == row["claims_annuity"] == 0.0
    assert row["expenses"] == approx(exp, abs=CENT)
    assert row["commissions"] == approx(comm, abs=CENT)
    assert row["net_cf"] == approx(net, abs=CENT)


def test_variant_fixed_totals_and_the_subsidy_share(riester_rente):
    """609,80 EUR from the saver against 1 926,26 EUR from the state over the projection.

    The Zulage is 76 % of the contribution on this cell, which is why a statement folding
    ``zulagen`` into ``premiums`` would be describing a different product.
    """
    p = riester_rente.Projection[5]
    df, acct = p.result_cf(), p.result_acct()
    for column, total in VARIANT_FIXED_TOTALS.items():
        source = acct if column == "int_credited" else df
        assert source[column].sum() == approx(total, abs=CENT), column
    share = df["zulagen"].sum() / (df["zulagen"].sum() + df["premiums"].sum())
    assert share == approx(0.76, abs=0.005)
    assert p.mindesteigenbeitrag_pp(0) == approx(60.00, abs=CENT)
    assert p.income_ref(0) == 0.0
    assert p.check_net_cf() is True


# --------------------------------------------------------------------------- pitfall 1

def test_the_two_subsidy_lags_are_not_one_lag(riester_rente, de_riester_anchor):
    """income_ref looks back one *calendar* year; zulage_pp one *projection* year.

    The visible consequence is that ``zulagen`` falls in year 3 while ``premiums`` rises in
    year 2: the entitlement drops a year before the credit does, and the § 86 minimum is 4 % of
    income *less* the entitlement, so a Zulage that stops is a contribution the saver must
    make good.  One offset applied twice reproduces neither.  Both lags are **annual**: the
    monthly grid gives the credit a month, not a different lag.
    """
    p = de_riester_anchor
    ann = p.result_cf_annual()
    schedule = riester_rente.Data.income_schedule()
    assert p.income_ref(0) == approx(p.income_init(), rel=1e-12)
    for k in (1, 4, 9, 16):
        assert p.income_ref(k) == approx(
            float(schedule.at[(p.income_id(), k - 1), "income"]), rel=1e-12)
    assert p.zulage_pp(0) == approx(p.zulage_init_pp(), rel=1e-12)
    for k in range(1, p.k_conv() + 1):
        assert p.zulage_pp(k) == approx(p.zulage_granted_pp(k - 1), rel=1e-12)
    assert p.zulage_entitlement_pp(1) == approx(475.00, abs=CENT)
    assert p.zulage_entitlement_pp(2) == approx(175.00, abs=CENT)
    assert p.zulage_pp(2) == approx(475.00, abs=CENT)
    assert p.zulage_pp(3) == approx(175.00, abs=CENT)
    assert ann.loc[2, "zulagen"] > ann.loc[3, "zulagen"]
    assert ann.loc[2, "premiums"] > ann.loc[1, "premiums"]
    assert p.check_zulage_lag() is True
    assert all(p.check_zulage_lag_resid(k) == approx(0.0, abs=1e-9)
               for k in (0, 1, 2, 3, 16, 17, 18, 60))


# --------------------------------------------------------------------------- pitfall 2

def test_the_last_contribution_years_zulage_is_credited_at_conversion(de_riester_anchor):
    """Contributions stop at t_conv() - 1; the Zulage they earned is credited at t_conv().

    It must be credited, guaranteed and converted before the *Beitragsgarantie* is tested.
    Stopping it with the contribution removes a full year's subsidy from the account **and**
    from the guarantee -- 175,00 EUR on this cell.
    """
    p = de_riester_anchor
    T = p.k_conv()
    assert p.eigenbeitrag_pp(T - 1) > 0.0 and p.eigenbeitrag_pp(T) == 0.0
    assert p.zulage_pp(T) == approx(175.00, abs=CENT)
    assert p.zulagen(p.t_conv()) == approx(134.33, abs=CENT)
    assert p.result_cf_annual().loc[T, "zulagen"] == approx(134.33, abs=CENT)
    assert p.zulage_pp(T + 1) == 0.0
    assert p.guar_pp(T + 1) - p.guar_pp(T) == approx(175.00, abs=CENT)
    assert p.prem_to_av_pp(T) == approx(156.00, abs=CENT)
    assert p.account_conv_pp() - (p.dk_pp(T) + p.surplus_acct_pp(T) + p.slueb_pp()
                                  + p.bewres_pp()) == approx(156.00, abs=CENT)


# --------------------------------------------------------------------------- pitfall 3

def test_the_kuerzung_is_proportional_and_not_a_cliff(riester_rente):
    """Model point 7 pays half the § 86 minimum and draws exactly half the Zulagen.

    Not zero and not the full amount: § 86 reduces the subsidy in the ratio of the
    contribution paid to the minimum.  A model treating the minimum as a cliff misstates every
    path in which the saver reduces contributions, and the German book is full of them.
    """
    p = riester_rente.Projection[7]
    assert p.contrib_ratio() == 0.5
    for k in (0, 1, 2, 4, 9):
        assert p.eigenbeitrag_pp(k) == approx(0.5 * p.mindesteigenbeitrag_pp(k), rel=1e-12)
        assert p.zulage_granted_pp(k) == approx(0.5 * p.zulage_entitlement_pp(k),
                                                rel=1e-12)
        assert p.zulage_granted_pp(k) > 0.0
    assert p.zulage_entitlement_pp(0) == approx(475.00, abs=CENT)
    assert p.zulage_granted_pp(0) == approx(237.50, abs=CENT)
    full = riester_rente.Projection[1]
    assert full.contrib_ratio() == 1.0
    assert full.zulage_granted_pp(0) == approx(475.00, abs=CENT)


# --------------------------------------------------------------------------- pitfall 4

def test_the_zulage_is_a_positive_income_column_of_its_own(de_riester_anchor):
    """Paid by the ZfA to the provider and credited to the contract.

    So it is published beside ``premiums`` and never folded into it, it never appears with a
    negative sign, and ``premiums`` excludes it: ``premiums(t)`` is the *Eigenbeitrag* after
    the *Ratenzuschlag* plus any unsubsidised contribution, and nothing else.
    """
    p = de_riester_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert (df["zulagen"] >= 0.0).all()
    assert (ann.loc[0:17, "zulagen"] > 0.0).all()
    assert (ann.loc[18:, "zulagen"] == 0.0).all()
    # The ZfA pays once a year, so the column is non-zero in one month of twelve.
    assert int((df["zulagen"] > 0.0).sum()) == 18
    for k in (0, 4, 16):
        t = 12 * k
        assert p.zulagen(t) == approx(p.zulage_pp(k) * p.pols_if(t), rel=1e-12)
        assert p.premiums(t) == approx(p.eigenbeitrag_paid_pp(k) * p.pols_if(t), rel=1e-12)
        assert p.premiums(t) != approx(
            (p.eigenbeitrag_paid_pp(k) + p.zulage_pp(k)) * p.pols_if(t), abs=CENT)
    # It is a contribution: it enters the guarantee accumulator and the subsidised pool.
    assert p.guar_pp(1) - p.guar_pp(0) == approx(p.eigenbeitrag_pp(0) + p.zulage_pp(0),
                                                 abs=CENT)
    assert p.pool_gefoerdert_pp(0) == approx(p.eigenbeitrag_pp(0) + p.zulage_pp(0),
                                             abs=CENT)


# --------------------------------------------------------------------------- pitfall 5

def test_the_guenstigerpruefung_has_no_cells_and_no_column(riester_rente):
    """Only the Zulage reaches the policy; the § 10a advantage is a personal tax refund.

    A model crediting the contract with the *Sonderausgabenabzug* would be crediting it with
    money that never arrives.  The absent names are asserted, because they are exactly what a
    reader who has just read the tax section would add.
    """
    names = set(riester_rente.Projection.cells) | set(riester_rente.Projection.refs)
    for absent in ("guenstigerpruefung", "guenstiger_pruefung", "sonderausgabenabzug",
                   "sonderausgaben_pp", "tax_relief_pp", "steuervorteil_pp",
                   "marginal_tax_rate", "tax_refund", "foerderung_10a_pp",
                   "rueckzahlungsbetrag_pp", "einkommensteuer"):
        assert absent not in names, absent
    columns = riester_rente.Projection[1].result_cf().columns
    assert not [c for c in columns if "tax" in c or "steuer" in c or "guenstig" in c]
    assert "zulage_cum_pp" in names       # the reclaimable limb, as a diagnostic only


# --------------------------------------------------------------------------- pitfall 6

def test_both_kinderzulage_rates_run_at_once(riester_rente):
    """Model point 3 has a child born in 2006 and one born in 2010, so it draws both.

    ``175 + 185 + 300 = 660,00 EUR`` at t = 0 and t = 1.  The split is permanent -- a
    birth-cohort rule, not a transition -- so a single rate misprices every family cell
    spanning the 2008 boundary.
    """
    p = riester_rente.Projection[3]
    row = riester_rente.Data.zulage_schedule().loc[(p.zulage_id(), 0)]
    assert float(row["n_kinder_pre2008"]) == float(row["n_kinder_post2008"]) == 1.0
    assert p.zulage_entitlement_pp(0) == approx(175.0 + 185.0 + 300.0, abs=CENT)
    assert p.zulage_entitlement_pp(1) == approx(660.00, abs=CENT)
    assert p.zulage_entitlement_pp(2) == approx(175.0 + 300.0, abs=CENT)
    assert p.zulage_entitlement_pp(0) != approx(175.0 + 2 * 300.0, abs=CENT)
    assert p.zulage_entitlement_pp(0) != approx(175.0 + 2 * 185.0, abs=CENT)
    assert riester_rente.Projection[1].zulage_entitlement_pp(0) == approx(475.0, abs=CENT)


# --------------------------------------------------------------------------- pitfall 7

def test_the_guarantee_is_tested_only_at_rentenbeginn(de_riester_anchor):
    """The anchor opens 358,94 EUR under water and no benefit is floored at the guarantee.

    ``garantieluecke_pp(k)`` is a diagnostic: it peaks at 567,69 EUR in year 2 and reaches zero
    in year 6, and through all of it the death benefit is the account value, the *Rückkaufswert*
    98 % of it and the transfer value it less 50,00 EUR -- every one **below** ``guar_pp``.
    """
    p = de_riester_anchor
    assert p.garantieluecke_pp(0) == approx(358.94, abs=CENT)
    assert p.garantieluecke_pp(2) == approx(567.69, abs=CENT)
    assert p.garantieluecke_pp(6) == 0.0
    assert p.guar_pp(0) > p.av_total_pp(0)
    for k in (0, 1, 2):
        a = p.av_total_pp_at(k, "AFT_INT")
        assert p.db_pp(k) == approx(a, rel=1e-12)
        assert p.cv_pp(k) == approx(0.98 * a, rel=1e-12)
        assert p.transfer_value_pp(k) == approx(a - 50.0, rel=1e-12)
        assert p.db_pp(k) < p.guar_pp(k + 1)      # not floored, and visibly so
        assert p.cv_pp(k) < p.db_pp(k)
    assert p.capital_conv_pp() == approx(
        max(p.account_conv_pp(), p.guar_pp(p.k_conv() + 1)), rel=1e-12)
    assert p.check_guar_roll_fwd() is True


# --------------------------------------------------------------------------- pitfall 8

def test_the_rider_carve_out_is_capped_at_twenty_per_cent(riester_rente):
    """Model point 9 sits on the cap: 400,00 EUR of rider premium carves out 240,00 EUR.

    ``kappa = min(rider, 0.20 x (E + Z + extra + rider)) = 240,00``, **strictly less than**
    the rider premium, so 160,00 EUR of it does not shrink the guarantee at all.  Carving out
    the whole rider premium would understate the accumulator by that much every year.
    """
    p = riester_rente.Projection[9]
    assert p.rider_prem_pp() == 400.0
    for t in (0, 1, 4, 9):
        base = (p.eigenbeitrag_pp(t) + p.zulage_pp(t) + p.contrib_extra_pp()
                + p.rider_prem_pp())
        assert p.guar_carve_out_pp(t) == approx(0.20 * base, rel=1e-12)
        assert p.guar_carve_out_pp(t) < p.rider_prem_pp()
    assert p.guar_carve_out_pp(0) == approx(240.00, abs=CENT)
    assert p.rider_prem_pp() - p.guar_carve_out_pp(0) == approx(160.00, abs=CENT)
    assert p.guar_pp(1) - p.guar_pp(0) == approx(625.0 + 175.0 - 240.0, abs=CENT)
    assert p.guar_pp(1) - p.guar_pp(0) != approx(625.0 + 175.0 - 400.0, abs=CENT)
    assert p.check_guar_roll_fwd() is True
    # The rider premium is not a cash flow of this model at all.
    assert p.premiums(0) == approx(p.eigenbeitrag_paid_pp(0) * p.pols_if(0), rel=1e-12)
    anchor = riester_rente.Projection[1]
    assert anchor.rider_prem_pp() == 0.0
    assert all(anchor.guar_carve_out_pp(t) == 0.0 for t in (0, 4, 16))


# --------------------------------------------------------------------------- pitfall 9

def test_unsubsidised_contributions_enter_the_guarantee(riester_rente):
    """Model point 8 pays 900,00 EUR a year above the § 10a ceiling.

    The undertaking is on the *Altersvorsorgebeiträge* paid in and does not distinguish the
    pools, so the accumulator steps by ``1 925 + 175 + 900 = 3 000,00`` while the entitlement
    never moves off the *Grundzulage*.  The pools are tracked apart because the benefit's
    taxation forks between them.
    """
    p = riester_rente.Projection[8]
    assert p.contrib_extra_pp() == 900.0
    for t in (0, 1, 4):
        assert p.guar_pp(t + 1) - p.guar_pp(t) == approx(
            p.eigenbeitrag_pp(t) + p.zulage_pp(t) + 900.0, abs=CENT)
        assert p.zulage_entitlement_pp(t) == approx(175.00, abs=CENT)
    assert p.guar_pp(1) - p.guar_pp(0) == approx(3000.00, abs=CENT)
    assert p.pool_ungefoerdert_pp(2) == approx(3 * 900.0, abs=CENT)
    assert p.pool_gefoerdert_pp(2) == approx(3 * (1925.0 + 175.0), abs=CENT)
    assert p.premiums(0) == approx((1925.0 + 900.0) * p.pols_if(0), abs=CENT)
    anchor = riester_rente.Projection[1]
    assert anchor.contrib_extra_pp() == 0.0
    assert all(anchor.pool_ungefoerdert_pp(t) == 0.0 for t in (0, 4, 16))


# --------------------------------------------------------------------------- pitfall 10

def test_the_declared_rate_includes_and_is_not_added_to_the_guaranteed_rate(
        de_riester_anchor):
    """int_credited_pp(t) = j(t) x (D + S + U) exactly, never (i + j) x anything.

    The *Deckungskapital* bears ``i`` in ``int_guar_pp`` and only the excess ``j - i`` in
    ``int_surplus_pp``; the *Überschussguthaben* bears the whole declared rate, having no
    guarantee to carve out of it.  Adding the rates credits 2,55 % instead of 2,30 %.
    """
    p = de_riester_anchor
    for t in (0, 4, 9, 16):
        j, i = p.decl_rate(t), p.rechnungszins()
        assert j == approx(0.023, rel=1e-12) and i == approx(0.0025, rel=1e-12)
        base, u = p.dk_pp(t) + p.prem_to_av_pp(t), p.surplus_acct_pp(t)
        assert p.int_guar_pp(t) == approx(i * base, rel=1e-12)
        assert p.int_surplus_pp(t) == approx((j - i) * base + j * u, rel=1e-12)
        assert p.int_credited_pp(t) == approx(j * (base + u), rel=1e-9)
        assert (i + j) * (base + u) > p.int_credited_pp(t) * 1.10
    assert p.int_credited(0) == approx(p.int_credited_pp(0) * p.pols_if(0), rel=1e-12)


def test_setting_the_declared_rate_to_the_guaranteed_rate_empties_the_surplus_leg():
    """With j = i the *Deckungskapital* leg of int_surplus_pp is exactly zero.

    Swapped in through the input file rather than through a formula change, which is the point
    of keeping the scenario outside the model.  It also makes the anchor's own guarantee bind:
    with no surplus the account falls 269,01 EUR short at *Rentenbeginn*.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Riester_DE_S_flat_j")
    alt = None
    try:
        scenario = pd.read_csv(model.Data.input_dir() / "surplus_scenario.csv")
        scenario.loc[scenario["scenario_id"] == "base", "decl_rate"] = 0.0025
        alt = model.Data.input_dir() / "surplus_scenario_flat.csv"
        scenario.to_csv(alt, index=False)
        model.Data.surplus_file = alt.name
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.decl_rate(0) == approx(p.rechnungszins(), rel=1e-12)
        assert p.int_surplus_pp(0) == approx(p.decl_rate(0) * p.surplus_acct_pp(0),
                                             rel=1e-12)
        assert p.int_credited_pp(0) == approx(p.int_guar_pp(0) + p.int_surplus_pp(0),
                                              rel=1e-12)
        assert p.garantieluecke_conv_pp() == approx(269.01, abs=CENT)
        assert p.check_av_roll_fwd() is True
    finally:
        if alt is not None:
            alt.unlink(missing_ok=True)
        model.close()


# --------------------------------------------------------------------------- pitfall 11

def test_the_frequency_loading_is_charged_and_never_credited(riester_rente):
    """Model point 3 is monthly: the saver pays E x 1,03 and only E reaches the account.

    ``admin_charge_pp`` takes the loading straight back out and strikes its percentage on the
    **unloaded** contribution, so the *Sparbeitrag* is algebraically independent of the
    payment frequency while ``premiums`` is larger by exactly ``E(k) x 0,03``.

    It is also why the contribution keeps the **annual** grid on a monthly frame: φ prices the
    mode by loading the amount rather than by moving the contribution year, so the whole
    year's *Eigenbeitrag* falls in the first month of the projection year whatever
    ``prem_freq`` says, and a model that also split the cash into instalments would charge
    for the deferral twice.
    """
    p = riester_rente.Projection[3]
    assert p.prem_freq() == "monthly" and p.prem_freq_load() == 1.03
    for k in (0, 1, 2, 4):
        e, z = p.eigenbeitrag_pp(k), p.zulage_pp(k)
        assert p.eigenbeitrag_paid_pp(k) == approx(1.03 * e, rel=1e-12)
        assert p.premiums(12 * k) == approx(1.03 * e * p.pols_if(12 * k), rel=1e-12)
        assert all(p.premiums(12 * k + i) == 0.0 for i in range(1, 12))
        assert p.contrib_total_pp(k) == approx(1.03 * e + z, rel=1e-12)
        assert p.admin_charge_pp(k) == approx(0.04 * (e + z) + 12.0 + e * 0.03, rel=1e-9)
        assert p.prem_to_av_pp(k) == approx(
            (e + z) - p.acq_charge_pp(k) - (0.04 * (e + z) + 12.0), rel=1e-9)
    anchor = riester_rente.Projection[1]
    assert anchor.prem_freq() == "annual" and anchor.prem_freq_load() == 1.0
    assert anchor.eigenbeitrag_paid_pp(0) == approx(anchor.eigenbeitrag_pp(0), rel=1e-12)


def test_removing_the_loading_moves_premiums_and_nothing_else():
    """Swap the loading table for a flat one: only ``premiums`` moves.

    ``prem_to_av_pp``, ``guar_pp`` and every benefit are identical to the last bit, which is
    the invariance pitfall 11 asserts and the reason the loading is deducted exactly once.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Riester_DE_S_flat_phi")
    alt = None
    try:
        p, ks = model.Projection[3], (0, 1, 2)
        before = {name: [getattr(p, name)(k) for k in ks] for name in
                  ("prem_to_av_pp", "guar_pp", "eigenbeitrag_pp")}
        before["premiums"] = [p.premiums(12 * k) for k in ks]
        before["pols_if"] = [p.pols_if(12 * k) for k in ks]
        before["claims_death"] = [p.claims(12 * k, "DEATH") for k in ks]

        table = pd.read_csv(model.Data.input_dir() / "freq_loading.csv",
                            index_col="prem_freq")
        table["load"] = 1.0
        alt = model.Data.input_dir() / "freq_loading_flat.csv"
        table.to_csv(alt)
        model.Data.freq_loading_file = alt.name
        model.Data.clear_all()
        model.Projection.clear_all()

        q = model.Projection[3]
        assert q.prem_freq_load() == 1.0
        for i, k in enumerate(ks):
            assert q.prem_to_av_pp(k) == approx(before["prem_to_av_pp"][i], rel=1e-12)
            assert q.guar_pp(k) == approx(before["guar_pp"][i], rel=1e-12)
            assert q.pols_if(12 * k) == approx(before["pols_if"][i], rel=1e-12)
            assert q.claims(12 * k, "DEATH") == approx(before["claims_death"][i], rel=1e-12)
            assert before["premiums"][i] - q.premiums(12 * k) == approx(
                0.03 * before["eigenbeitrag_pp"][i] * before["pols_if"][i], rel=1e-9)
        assert q.premiums(0) == approx(1020.00, abs=CENT)
    finally:
        if alt is not None:
            alt.unlink(missing_ok=True)
        model.close()


# --------------------------------------------------------------------------- pitfall 12

def test_the_acquisition_charge_is_spread_over_five_contract_years(riester_rente,
                                                                   de_riester_anchor):
    """Equal in contract years 1 to 5 and zero afterwards, on the **contract** clock.

    The anchor is in force at duration 3, so the first two projected years, k = 0 and k = 1,
    have ``duration_y(k) = 3`` and ``4`` -- contract years 4 and 5 -- and carry 168,00 EUR
    each.  Model point 2 is the same contract
    from its own inception and carries the charge at k = 0 to 4 instead.
    """
    p = de_riester_anchor
    assert p.duration_init() == 3
    assert [p.duration_y(k) for k in (0, 1, 2)] == [3, 4, 5]
    assert [p.duration(t) for t in (0, 11, 12)] == [3, 3, 4]
    assert p.acq_charge_pp(0) == p.acq_charge_pp(1) == approx(168.00, abs=CENT)
    assert all(p.acq_charge_pp(k) == 0.0 for k in (2, 3, 9, 16))
    assert p.prem_to_av_pp(2) - p.prem_to_av_pp(1) == approx(488.90, abs=CENT)
    at_issue = riester_rente.Projection[2]
    assert at_issue.duration_init() == 0
    assert all(at_issue.acq_charge_pp(k) == approx(168.00, abs=CENT) for k in range(5))
    assert at_issue.acq_charge_pp(5) == 0.0
    assert sum(at_issue.acq_charge_pp(k) for k in range(6)) == approx(0.025 * 33600.0,
                                                                      abs=CENT)


def test_the_acquisition_charge_survives_beitragsfreistellung(riester_rente):
    """Model point 10 goes paid-up at t = 3 and the charge keeps biting.

    ``prem_to_av_pp(3) = 175,00 - 168,00 - 19,00 = -12,00``: the last Zulage arrives, the
    acquisition and fixed administration charges do not stop, and the *Deckungskapital* falls.
    Stopping the charge would hide the mechanic this model point exists to show.
    """
    p = riester_rente.Projection[10]
    assert p.bfs_year() == 3 and p.duration_y(3) == 4
    assert p.acq_charge_pp(3) == approx(168.00, abs=CENT)
    assert p.eigenbeitrag_pp(3) == 0.0
    assert p.zulage_pp(3) == approx(175.00, abs=CENT)
    assert p.admin_charge_pp(3) == approx(0.04 * 175.0 + 12.0, abs=CENT)
    assert p.prem_to_av_pp(3) == approx(-12.00, abs=CENT)
    assert p.prem_to_av_pp(4) == approx(-12.00, abs=CENT)
    assert p.acq_charge_pp(4) == 0.0          # contract year 6: the window is over
    assert p.prem_to_av_pp(3) < 0.0 < p.prem_to_av_pp(2)


# --------------------------------------------------------------------------- pitfall 13

def test_a_transfer_is_a_separate_decrement_from_a_surrender(riester_rente,
                                                             de_riester_anchor):
    """Full account less a flat 50,00 EUR, with no *Stornoabzug*, and its own column.

    The *Wechselrecht* carries none of the *schädliche Verwendung* consequences a *Kündigung*
    does, so the transfer rate is set above the surrender rate at every duration and the two
    produce different benefits from the same account.
    """
    p = de_riester_anchor
    for k in (0, 4, 11, 16):
        a = p.av_total_pp_at(k, "AFT_INT")
        assert p.cv_pp(k) == approx(0.98 * a, rel=1e-12)
        assert p.transfer_value_pp(k) == approx(a - 50.0, rel=1e-12)
        assert p.transfer_value_pp(k) > p.cv_pp(k)
        assert p.transfer_rate(12 * k) > p.lapse_rate(12 * k)
        assert p.transfer_rate_mth(12 * k) > p.lapse_rate_mth(12 * k)
    lapse = riester_rente.Data.lapse_table()
    assert (lapse["transfer_rate"] > lapse["lapse_rate"]).all()
    assert [lapse.at[1, "lapse_rate"], lapse.at[1, "transfer_rate"]] == [0.008, 0.012]
    ann = p.result_cf_annual()
    assert (ann["claims_transfer"].loc[0:16] > ann["claims_lapse"].loc[0:16]).all()
    assert p.result_cf()["claims_transfer"].sum() == approx(2259.27, abs=CENT)
    assert p.result_cf()["claims_lapse"].sum() == approx(1478.78, abs=CENT)
    # The charge the insurer retains differs in kind: a percentage against a flat fee, both
    # struck monthly on the annual end-of-year account value.
    assert p.exit_charge_pp(0) == approx(
        0.02 * p.av_total_pp_at(0, "AFT_INT") * p.pols_lapse(0) + 50.0 * p.pols_transfer(0),
        rel=1e-12)


# --------------------------------------------------------------------------- pitfall 14

def test_beitragsfreistellung_is_a_state_change(riester_rente):
    """Model point 10: pols_if continuous, guarantee frozen, Zulagen stopped, account rolling.

    Nothing leaves the in-force at ``bfs_year``; the ordinary decrements carry on and the
    roll-forward closes.  The guarantee freezes only once the **last** Zulage has landed, one
    year after the contribution stops -- the same arrear that makes pitfall 2 a pitfall.
    """
    p = riester_rente.Projection[10]
    b = p.bfs_year()
    # The ledger is continuous across the year boundary, at the year's annual rates.
    assert p.pols_if(12 * b) == approx(
        p.pols_if(12 * (b - 1)) * (1.0 - p.mort_rate(12 * (b - 1)))
        * (1.0 - p.lapse_rate(12 * (b - 1))) * (1.0 - p.transfer_rate(12 * (b - 1))),
        rel=1e-12)
    assert p.pols_if(12 * b) > 0.9 * p.pols_if(12 * (b - 1))
    assert p.check_pols_roll_fwd() is True
    assert p.eigenbeitrag_pp(b - 1) > 0.0
    assert all(p.eigenbeitrag_pp(k) == 0.0 for k in range(b, p.k_conv()))
    assert p.premiums(12 * b) == 0.0 and p.zulage_pp(b) > 0.0
    assert all(p.zulage_pp(k) == 0.0 for k in range(b + 1, p.k_conv() + 1))
    frozen = p.guar_pp(b + 1)
    assert all(p.guar_pp(k) == approx(frozen, abs=CENT) for k in (b + 2, 9, p.k_conv() + 1))
    assert p.av_total_pp(b + 2) > 0.0 and p.av_total_pp(p.k_conv()) > p.av_total_pp(b)
    assert p.check_guar_roll_fwd() is True


# --------------------------------------------------------------------------- pitfall 15

def test_the_two_phases_use_different_mortality_bases(de_riester_anchor):
    """The basis switches at t_conv(), and the two factors run in opposite directions.

    Accumulation is the DAV 2008 T proxy at ``mort_be_factor = 0.80``; payout is the
    generational DAV 2004 R proxy at ``annuity_mort_be_factor = 1.15``.  A first-order death
    table assumes mortality higher than expected and a first-order annuity table lower.
    """
    p = de_riester_anchor
    T = p.t_conv()
    for t in (0, 48, 192):
        assert p.mort_rate(t) == approx(p.mort_rate_at_age(p.age(t)) * 0.80, rel=1e-12)
    for t in (T, T + 1, 468):
        assert p.mort_rate(t) == approx(
            p.annuity_mort_rate(p.age(t), p.calendar_year(t)) * 1.15, rel=1e-12)
    assert p.mort_rate_at_age(67) * 0.80 != approx(p.mort_rate(T), rel=1e-3)
    # Both are ANNUAL rates, flat across the twelve months of a projection year, and the
    # recursion applies their geometric twelfth.
    assert all(p.mort_rate(t) == p.mort_rate(0) for t in range(12))
    assert (1.0 - p.mort_rate_mth(0)) ** 12 == approx(1.0 - p.mort_rate(0), rel=1e-14)
    assert p.mort_rate_mth(0) > p.mort_rate(0) / 12.0


def test_the_annuity_basis_is_generational(de_riester_anchor):
    """annuity_mort_rate(x, tau) depends on **both** arguments and falls with tau.

    A period-table proxy would price a seventeen-year-deferred annuitisation on 2027 mortality
    instead of 2044 mortality: at age 67 the two differ by a quarter, a margin that dwarfs
    every other assumption in the model.
    """
    p = de_riester_anchor
    q2027, q2044 = p.annuity_mort_rate(67, 2027), p.annuity_mort_rate(67, 2044)
    assert q2044 < q2027 and p.annuity_mort_rate(67, 2045) < q2044
    assert q2044 / q2027 == approx((1.0 - 0.0171) ** 17, rel=1e-9)
    assert 1.0 - q2044 / q2027 == approx(0.254, abs=0.005)
    assert p.calendar_year_y(p.k_conv()) == 2044 == p.calendar_year(p.t_conv())
    assert p.ann_factor() == approx(20.87222879, abs=5e-9)
    assert p.mort_rate_at_age(110) == p.annuity_mort_rate(110, 2044) == 1.0


# --------------------------------------------------------------------------- pitfall 16

def test_the_kleinbetragsrente_is_tested_after_the_lump_sum(riester_rente,
                                                            de_riester_anchor):
    """Tested on the annuity payable **after** the elected 30 %, against a flat threshold.

    Model point 5's capital of 4 537,22 EUR would buy 9,21 EUR a month after the lump sum
    against a 39,55 EUR threshold, so it commutes; the anchor's 92,89 EUR clears it.  A
    commuted contract pays the **whole** capital as an *Abfindung*, no lump sum and no annuity
    beside it, and the payment discharges the contract outright.
    """
    small = riester_rente.Projection[5]
    T = small.t_conv()
    assert T == 132 and small.k_conv() == 11
    assert small.capital_conv_pp() == approx(4537.217342, abs=CENT)
    test_annuity = ((1.0 - small.teilkapital_share()) * small.capital_conv_pp()
                    / 10000.0 * small.rentenfaktor_applied())
    assert test_annuity == approx(9.21, abs=CENT) and test_annuity <= 39.55
    assert small.is_kleinbetrag() is True
    assert small.commutation_pp() == approx(small.capital_conv_pp(), rel=1e-12)
    assert small.teilkapital_pp() == small.annuity_capital_pp() == 0.0
    assert small.annuity_pp(small.k_conv()) == 0.0 and small.annuity_month_pp() == 0.0
    assert small.claims(T, "COMMUTATION") == approx(3828.31, abs=CENT)
    assert small.claims(T, "LUMPSUM") == 0.0
    assert all(small.claims(t, "ANNUITY") == 0.0 for t in range(T, small.proj_len()))
    # The Abfindung discharges the contract: no decrement removes the population.
    assert small.pols_if(T + 1) == 0.0 and small.pols_death(T) == 0.0
    assert small.check_pols_roll_fwd() is True
    assert small.result_cf().index[-1] == small.proj_len() - 1 == 659
    # The anchor clears the threshold, which is flat in nominal terms.
    assert de_riester_anchor.annuity_month_pp() == approx(92.885458, abs=CENT)
    assert de_riester_anchor.is_kleinbetrag() is False
    assert riester_rente.Projection.kleinbetrag_threshold_mth == 39.55
    assert [n for n in (4, 5, 10, 13)
            if riester_rente.Projection[n].is_kleinbetrag()] == [4, 5, 10, 13]


# --------------------------------------------------------------------------- pitfall 17

def test_the_rentengarantiezeit_changes_who_is_paid_and_never_how_much(riester_rente,
                                                                       de_riester_anchor):
    """pols_annuity_pay is pols_conv() inside the guarantee period and pols_if after it.

    The instalment does not move: ``annuity_month_pp()`` is 92,885458 EUR in every payout
    month, guarantee period or not, and no cells reads ``rentengarantie_years()`` to set it.
    On this grid the window is ``12m`` **instalments**.  Model
    point 12 has no guarantee period and pays the same instalment to a falling count.
    """
    p = de_riester_anchor
    T, n = p.t_conv(), p.proj_len()
    assert p.rentengarantie_years() == 10
    for t in range(T, T + 120):
        assert p.pols_annuity_pay(t) == approx(p.pols_conv(), rel=1e-12)
        assert p.claims(t, "ANNUITY") == approx(71.301877, abs=CENT)
    for t in (T + 120, T + 121, n - 1):
        assert p.pols_annuity_pay(t) == approx(p.pols_if(t), rel=1e-12)
    assert p.pols_annuity_pay(T + 119) > p.pols_if(T + 119)
    assert all(p.annuity_month_pp() == approx(92.885458, abs=CENT)
               for t in (T, T + 60, T + 240, n - 1))
    assert all(p.annuity_pp(k) == approx(1114.625493, abs=CENT)
               for k in (17, 22, 37, 60))
    cells = riester_rente.Projection.cells
    assert "rentengarantie_years()" not in cells["annuity_pp"].formula.source
    assert "rentengarantie_years()" in cells["pols_annuity_pay"].formula.source
    # Point 12 takes no lump sum either, so it annuitises the whole capital: the anchor's
    # annuity divided by 0.70.
    pure = riester_rente.Projection[12]
    assert pure.rentengarantie_years() == 0 and pure.teilkapital_share() == 0.0
    assert all(pure.pols_annuity_pay(t) == approx(pure.pols_if(t), rel=1e-12)
               for t in (pure.t_conv(), pure.t_conv() + 5, pure.proj_len() - 1))
    assert pure.annuity_capital_pp() == approx(pure.capital_conv_pp(), rel=1e-12)
    assert pure.annuity_pp(pure.k_conv()) == approx(p.annuity_pp(17) / 0.70, rel=1e-9)
    assert pure.claims(pure.t_conv(), "LUMPSUM") == 0.0


# --------------------------------------------------------------------------- pitfall 18

def test_benefits_are_published_gross_of_the_rueckzahlungsbetrag(riester_rente,
                                                                 de_riester_anchor):
    """The provider withholds the Zulagen and the § 10a relief and remits them to the ZfA.

    That is a tax collection, not a reduction in the insurer's obligation, so ``claims_death``
    is the whole account value; netting the reclaimable amount out of it would understate the
    outgo by 4 050,00 EUR of cumulative Zulagen alone by the conversion year.
    """
    p = de_riester_anchor
    cells = riester_rente.Projection.cells
    for t in (0, 48, 192):
        k = p.proj_year(t)
        assert p.claims(t, "DEATH") == approx(
            p.av_total_pp_at(k, "AFT_INT") * p.pols_death(t), rel=1e-12)
        assert p.claims(t, "LAPSE") == approx(
            0.98 * p.av_total_pp_at(k, "AFT_INT") * p.pols_lapse(t), rel=1e-12)
        assert p.db_pp(k) > p.zulage_cum_pp(k)      # nothing has been netted out
    assert p.zulage_cum_pp(0) == approx(475.00, abs=CENT)
    assert p.zulage_cum_pp(17) == approx(4050.00, abs=CENT)
    assert p.zulage_cum_pp(17) == approx(sum(p.zulage_pp(k) for k in range(18)),
                                         abs=CENT)
    # It is a diagnostic and nothing more: no benefit reads it, and no cells attempts the
    # § 10a limb, which contract data cannot support.
    for name in ("claims", "db_pp", "cv_pp", "transfer_value_pp"):
        assert "zulage_cum_pp" not in cells[name].formula.source, name
    assert "zulage_cum_pp" not in list(p.result_cf().columns)


# --------------------------------------------------------------------------- the checks

def test_every_check_identity_closes_on_the_anchor(de_riester_anchor):
    """All six checks, and their residuals at the periods where each could break.

    ``check_net_cf()`` is delib's first ruling: the statement reconstructs its own headline
    number from its published parts, so ``net_cf`` is not the one quantity nothing checks.
    """
    p = de_riester_anchor
    for check in ("check_net_cf", "check_av_roll_fwd", "check_guar_roll_fwd",
                  "check_pols_roll_fwd", "check_conversion", "check_zulage_lag"):
        value = getattr(p, check)()
        assert isinstance(value, bool), check
        assert value is True, check
    # The residual's argument follows its cells' clock: two take a month, four a projection
    # year, because the account, the guarantee, the conversion and the ZfA lag move once a
    # Versicherungsjahr.
    for t in (0, 1, 11, 191, 203, 204, 215, 731):
        assert p.check_net_cf_resid(t) == approx(0.0, abs=1e-9)
        assert p.check_pols_roll_fwd_resid(t) == approx(0.0, abs=1e-12)
    for k in (0, 1, 16, 17, 18, 29, 60):
        assert p.check_av_roll_fwd_resid(k) == approx(0.0, abs=1e-9)
        assert p.check_guar_roll_fwd_resid(k) == approx(0.0, abs=1e-9)
        assert p.check_conversion_resid(k) == approx(0.0, abs=1e-9)
        assert p.check_zulage_lag_resid(k) == approx(0.0, abs=1e-9)


def test_check_net_cf_reconstructs_the_row_from_its_published_parts(de_riester_anchor):
    """The identity in one line, on the frame rather than on the cells.

    Every column of ``result_cf()`` but ``pols_if``, ``pols_annuity_pay`` and
    ``liability_cf`` is in it, each exactly once.
    """
    p = de_riester_anchor
    df = p.result_cf()
    outgo = sum(df["claims_" + k.lower()] for k in CLAIM_KINDS)
    rebuilt = df["premiums"] + df["zulagen"] - outgo - df["expenses"] - df["commissions"]
    assert (rebuilt - df["net_cf"]).abs().max() == approx(0.0, abs=1e-9)
    # int_credited is reported and not summed in -- and on the monthly grid it is not a
    # column of this frame at all, which removes the tempting mistake outright.
    assert "int_credited" not in df.columns
    assert p.result_acct()["int_credited"].sum() > 100.0
    # Commission is a separate column from expenses and is subtracted exactly once.
    assert (df["commissions"] > 0.0).any()
    ann = p.result_cf_annual()
    assert (ann["expenses"].loc[0:16] > ann["commissions"].loc[0:16]).all()


def test_the_conversion_identity_ties_the_factor_to_the_annuity_basis(riester_rente):
    """rentenfaktor_curr() x 12 x ann_factor() = (1 - margin) x 10 000, on every point.

    It holds whether or not the current factor is the one applied, which makes it a check on
    the annuity basis rather than on the conversion outcome, and it catches a Woolhouse
    correction applied twice or a factor struck on the second-order basis.
    """
    margin = riester_rente.Projection.rentenfaktor_margin
    assert margin == 0.30
    for point_id in (1, 5, 11, 12, 13):
        p = riester_rente.Projection[point_id]
        assert p.rentenfaktor_curr() * 12.0 * p.ann_factor() == approx(
            (1.0 - margin) * 10000.0, rel=1e-12)
        assert p.rentenfaktor_applied() == approx(
            max(p.rentenfaktor_guar(), p.rentenfaktor_curr()), rel=1e-12)
        assert p.capital_conv_pp() == approx(
            p.teilkapital_pp() + p.annuity_capital_pp() + p.commutation_pp(), abs=1e-9)
        assert p.check_conversion() is True


# --------------------------------------------------------------------------- structure

def test_result_cf_shape_and_both_signs_of_the_net_flow(de_riester_anchor):
    """Fourteen monthly columns, indexed by t, contiguous, ending at proj_len() - 1.

    ``pols_if`` leads and its first value is ``pols_if_init()`` exactly; there is no bare
    ``claims`` subtotal beside the six parts; ``liability_cf`` is ``net_cf`` outgo-positive.
    ``int_credited`` is **not** a column: it moves once a *Versicherungsjahr*, like the two
    balances it moves between, so it lives in ``result_acct()`` with them.
    """
    p = de_riester_anchor
    df = p.result_cf()
    assert list(df.columns) == RESULT_CF_COLUMNS
    assert "claims" not in df.columns and "int_credited" not in df.columns
    assert list(df.index) == list(range(732))
    assert df.index.name == "t"
    assert df.index[-1] == p.proj_len() - 1 == 731
    assert len(df) == p.proj_len() == 732
    assert df["pols_if"].iloc[0] == approx(p.pols_if_init(), rel=1e-12)
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == approx(0.0, abs=1e-9)
    assert df.notna().all().all()
    # The monthly saw-tooth: the year's contribution in one month, eleven without.
    prem_month = df["premiums"] > 0.0
    assert int(prem_month.sum()) == 17          # one a year, to the last contribution year
    assert (df.loc[prem_month, "net_cf"].iloc[:-1] > 0.0).all()
    assert df["net_cf"].iloc[0] == approx(1642.25, abs=CENT)
    assert df["net_cf"].iloc[1] == approx(-12.53, abs=CENT)
    # The two annual frames beside it, and the shape the notes print.
    ann, acct = p.result_cf_annual(), p.result_acct()
    assert ann.index.name == "k" and list(ann.index) == list(range(61))
    assert list(ann.columns) == list(df.columns)
    assert acct.index.name == "k" and len(acct) == p.proj_len_y() == 61
    assert {"int_credited", "dk_pp", "surplus_acct_pp", "guar_pp", "mort_rate",
            "mort_rate_mth"} <= set(acct.columns)
    assert (ann["net_cf"].loc[0:16] > 0.0).all()
    assert ann["net_cf"].loc[17] == approx(-11276.67, abs=CENT)
    assert (ann["net_cf"].loc[18:] < 0.0).all()


def test_the_accessors_validate_and_the_within_year_reads_are_consistent(
        de_riester_anchor):
    """claims(t) sums the six kinds, the enum accessors validate, and the timings agree."""
    p = de_riester_anchor
    for t in (0, 192, 204, 348):
        assert p.claims(t) == approx(sum(p.claims(t, k) for k in CLAIM_KINDS), rel=1e-12)
    assert p.claims(204) == approx(10536.610861 + 71.301877, abs=CENT)
    with pytest.raises(FormulaError):
        p.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        p.pols_if_at(0, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        p.av_total_pp_at(0, "AFT_DECR")
    # The policy ledger reads take a month; the account reads take a projection year.
    for t in (0, 4, 16, 203):
        assert p.pols_if_at(t, "BEF_DECR") == approx(p.pols_if(t), rel=1e-12)
        assert p.pols_if_at(t, "AFT_DECR") == approx(p.pols_if(t + 1), rel=1e-12)
    for k in (0, 4, 16):
        assert p.av_total_pp_at(k, "BEF_PREM") == approx(p.av_total_pp(k), rel=1e-12)
        assert p.av_total_pp_at(k, "AFT_PREM") == approx(p.av_total_pp(k) + p.prem_to_av_pp(k),
                                                   rel=1e-12)
        assert p.av_total_pp_at(k, "AFT_INT") == approx(p.av_total_pp(k + 1), rel=1e-12)
        assert p.av_total_at(k, "BEF_PREM") == approx(
            p.av_total_pp(k) * p.pols_if(12 * k), rel=1e-12)
    assert p.av_total_pp(0) == approx(p.dk_pp_init() + p.surplus_pp_init(), rel=1e-12)
    assert p.av_total_pp(0) == approx(4010.98, abs=CENT)


def test_the_model_point_is_read_and_sex_reaches_no_rate(riester_rente, de_riester_anchor):
    """Riester tariffs are unisex from a 2006 vintage, so ``sex`` drives nothing.

    Model point 7 is the same attained age and entitlement path with a male life; its
    mortality rate and its *Rentenfaktor* are the anchor's to the last bit.
    """
    p = de_riester_anchor
    assert p.sex() == "F"
    assert p.issue_age() == 47 and p.duration_init() == 3
    assert p.age_y(0) == 50 and p.calendar_year_y(0) == 2027 and p.duration_y(0) == 3
    assert p.age(0) == 50 and p.calendar_year(0) == 2027 and p.duration(0) == 3
    assert p.rentenbeginn_age() == 67 and p.k_conv() == 17 and p.t_conv() == 204
    assert p.proj_len_y() == 110 - 50 + 1 and p.proj_len() == 12 * p.proj_len_y()
    male = riester_rente.Projection[7]
    assert male.sex() == "M" and male.age(0) == p.age(0)
    assert male.mort_rate(0) == approx(p.mort_rate(0), rel=1e-12)
    assert male.rentenfaktor_curr() == approx(p.rentenfaktor_curr(), rel=1e-12)
    cells = riester_rente.Projection.cells
    assert "sex()" not in cells["mort_rate"].formula.source
    assert "sex()" not in cells["ann_factor"].formula.source


def test_docstrings_describe_the_current_structure(riester_rente):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = riester_rente.doc
    assert "Riester" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "Beitragsgarantie" in doc and "Zulage" in doc
    assert "Data" in doc and "Projection" in doc
    proj = riester_rente.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "zulage_pp", "guar_pp", "t_conv",
                  "prem_to_av_pp", "pols_annuity_pay", "garantieluecke_conv_pp"):
        assert cells in proj, cells
    data = riester_rente.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "annuity_mort_table",
                  "zulage_schedule"):
        assert cells in data, cells
    undocumented = [f"{s}.{c}" for s in riester_rente.spaces
                    for c in riester_rente.spaces[s].cells
                    if not riester_rente.spaces[s].cells[c].doc]
    assert not undocumented, undocumented


def test_the_savings_chassis_vocabulary_is_present(riester_rente):
    """Names shared with RV_DE_S, Basis_DE_S and Sofort_DE_S must mean the same thing.

    The second set is the Schicht-2 apparatus this product adds to that chassis.
    """
    shared = {
        "model_point", "proj_len", "age", "duration", "calendar_year", "pols_if",
        "pols_if_init", "pols_if_at", "pols_death", "pols_lapse", "mort_rate",
        "lapse_rate", "claims", "expenses", "commissions", "net_cf", "liability_cf",
        "result_cf", "av_total_pp", "av_total_pp_at", "av_total_at", "prem_to_av_pp", "dk_pp",
        "surplus_acct_pp", "rechnungszins", "decl_rate", "t_conv", "is_accum",
        "is_payout", "ann_factor", "rentenfaktor_guar", "rentenfaktor_applied",
        "annuity_pp", "check_net_cf", "check_net_cf_resid",
    }
    riester = {
        "zulage_entitlement_pp", "zulage_granted_pp", "zulage_pp", "zulage_cum_pp",
        "zulagen", "mindesteigenbeitrag_pp", "eigenbeitrag_pp", "eigenbeitrag_paid_pp",
        "guar_pp", "guar_carve_out_pp", "garantieluecke_pp", "garantieluecke_conv_pp",
        "pool_gefoerdert_pp", "pool_ungefoerdert_pp", "is_kleinbetrag", "teilkapital_pp",
        "commutation_pp", "transfer_rate", "transfer_value_pp",
    }
    names = set(riester_rente.Projection.cells) | set(riester_rente.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    assert riester <= names, f"missing: {sorted(riester - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Eight CSVs beside run.py; every one but the model point table says where it came from.

    The two decrement tables are **[std]** proxies -- DAV 2008 T and DAV 2004 R are
    proprietary and are cited by name, never shipped -- and the anchors a substitute must
    preserve are ``qx`` at age 50 and the generational structure of the annuity table.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "mort_table_accum.csv", "annuity_mort_table.csv",
                "lapse_table.csv", "zulage_schedule.csv", "income_schedule.csv",
                "surplus_scenario.csv", "freq_loading.csv"}
    assert expected == {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"}

    mort = pd.read_csv(INPUT_DIR / "mort_table_accum.csv", index_col="age")
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert "DAV 2008 T" in mort["provenance"].iloc[0]
    assert float(mort.loc[50, "qx"]) == 0.0015
    assert float(mort.loc[51, "qx"]) / float(mort.loc[50, "qx"]) == approx(1.10, rel=1e-6)
    assert float(mort.loc[110, "qx"]) == 1.0
    assert list(mort.index) == list(range(16, 111))

    annuity = pd.read_csv(INPUT_DIR / "annuity_mort_table.csv", index_col="age")
    assert set(annuity.columns) == {"qx_base", "improvement", "provenance"}
    assert all("DAV 2004 R" in p for p in annuity["provenance"])
    assert float(annuity.loc[65, "qx_base"]) == 0.006
    assert float(annuity.loc[65, "improvement"]) == 0.018
    assert float(annuity.loc[110, "qx_base"]) == 1.0
    assert (annuity["improvement"] >= 0.002).all()

    lapse = pd.read_csv(INPUT_DIR / "lapse_table.csv", index_col="duration")
    assert (lapse["transfer_rate"] > lapse["lapse_rate"]).all()
    assert all("[std]" in p for p in lapse["provenance"])

    surplus = pd.read_csv(INPUT_DIR / "surplus_scenario.csv")
    assert set(surplus["scenario_id"]) == {"base", "low"}
    assert set(surplus.loc[surplus["scenario_id"] == "base", "decl_rate"]) == {0.023}
    assert set(surplus.loc[surplus["scenario_id"] == "low", "decl_rate"]) == {0.005}
    assert all(p.startswith("[std]") for p in surplus["provenance"])
    assert all("Rechnungszins" in p
               for p in surplus.loc[surplus["scenario_id"] == "base", "provenance"])

    freq = pd.read_csv(INPUT_DIR / "freq_loading.csv", index_col="prem_freq")
    assert list(freq["load"]) == [1.0, 1.01, 1.02, 1.03]
    assert all("[std]" in p for p in freq["provenance"])

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns      # the one exempt file
    assert list(points.index) == list(range(1, 14))
    assert points.loc[1, "scenario_id"] == "base" and points.loc[11, "scenario_id"] == "low"
    assert (points["teilkapital_share"] <= 0.30).all()
    assert (points["rentenbeginn_age"] >= 62).all()


def test_an_input_can_be_swapped_without_touching_formulas():
    """What a production user does with a company or licensed mortality basis.

    Point ``Data.annuity_mort_file`` at a same-schema file with a heavier annuitant table and
    the conversion follows: a shorter annuity factor lifts the current *Rentenfaktor*, and
    once it passes the guaranteed 29,00 it becomes the factor applied.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="Riester_DE_S_swap")
    alt = None
    try:
        base_factor = model.Projection[1].ann_factor()
        assert model.Projection[1].rentenfaktor_applied() == 29.0

        heavier = pd.read_csv(INPUT_DIR / "annuity_mort_table.csv", index_col="age")
        heavier["qx_base"] = (heavier["qx_base"] * 2.0).clip(upper=1.0)
        alt = model.Data.input_dir() / "annuity_mort_table_heavy.csv"
        heavier.to_csv(alt)
        model.Data.annuity_mort_file = alt.name
        model.Data.clear_all()
        model.Projection.clear_all()

        p = model.Projection[1]
        assert p.ann_factor() < base_factor
        assert p.rentenfaktor_curr() > 29.0
        assert p.rentenfaktor_applied() == approx(p.rentenfaktor_curr(), rel=1e-12)
        assert p.annuity_month_pp() > 92.885458
        assert p.check_conversion() is True
    finally:
        if alt is not None:
            alt.unlink(missing_ok=True)
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set.

    Inputs are external, so they must travel with the model: the CSVs are copied to the new
    parent before re-reading, which is exactly the trade-off this layout makes.
    """
    import shutil

    model = mx.read_model(MODEL_DIR, name="Riester_DE_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in INPUT_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Riester_DE_S_rt")
    try:
        p = reread.Projection[1]
        ann = p.result_cf_annual()
        for k, row in WORKED_EXAMPLE.items():
            assert ann.loc[k, "pols_if"] == approx(row[0], abs=SIX_DP)
            assert ann.loc[k, "premiums"] == approx(row[1], abs=CENT)
            assert ann.loc[k, "zulagen"] == approx(row[2], abs=CENT)
            assert ann.loc[k, "net_cf"] == approx(row[11], abs=CENT)
        for t, row in MONTHS_YEAR_0.items():
            assert p.pols_if(t) == approx(row[0], abs=SIX_DP)
            assert p.net_cf(t) == approx(row[8], abs=CENT)
        assert p.proj_len() == 12 * p.proj_len_y() == 732
        assert p.garantieluecke_pp(0) == approx(358.94, abs=CENT)
        assert p.capital_conv_pp() == approx(45756.383140, abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_net_cf() is True and p.check_conversion() is True
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
