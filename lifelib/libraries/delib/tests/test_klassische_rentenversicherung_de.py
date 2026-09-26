"""Golden and structural tests for RV_DE_S.

The golden values are the worked example in
products/klassische_rentenversicherung/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: model point 1, ``DE-RV-0001``, a *klassische
aufgeschobene private Rentenversicherung* on a male aged 50 at issue in 2026, new business
(``duration_init = 0``) so the frame opens at month ``t = 0``, one policy in force; a *laufender
Beitrag* of 3 000,00 EUR a year payable annually (``freq_load = 1,000``) for seventeen years
over a seventeen-year *Aufschubzeit*, so the *Rentenbeginn* falls at the end of policy year 17
at attained age 67; a *Rechnungszins* of 1,00 %, the 2026 vintage; the ``zillmer_25`` charge
set, hence a *Beitragssumme* of 51 000,00 EUR and a zillmered acquisition charge of
1 275,00 EUR taken in full from the first premium; a *garantierter Rentenfaktor* of 28,00 EUR
against a ``base`` *aktueller Rentenfaktor* of 32,00 EUR, so the current factor wins the
``max``; a ``base`` declared *laufende Verzinsung* of 2,55 %, hence an interest-surplus rate
of 1,55 %; a *Beitragsrückgewähr* death benefit on premiums only; no guaranteed contract
value; a *Rentengarantiezeit* of ten years; a *Kapitalwahlrecht* take-up of 30 %; the
``konstant`` payout system; no *Dynamik*, no *Beitragsfreistellung*, no opening balances.
Hence ``proj_len_y() = 121 - 50 = 71`` and ``proj_len() = 852``.

**The grid is monthly and the product is mostly not.**  The model runs on two clocks: cells that
state an annual account take a policy year ``k`` — the premium and its decomposition, both account
balances, the § 169 Abs. 3 floor, the surrender value, the death benefit — and cells that state a
month take ``t``.  The notes' worked example is therefore stated on
:func:`result_cf_annual`, the monthly frame summed into policy years, and that is what
:data:`WORKED_EXAMPLE` is asserted against, keyed on the 0-based policy year ``k``;
:data:`MONTHS_YEAR_1` asserts the twelve months of policy year 1 on the monthly frame beside it,
and :data:`ANNUAL_GRID_TOTALS` records what the conversion moved against the annual-step model
this replaced, so that what changed is on the record rather than merely absent.

The notes print the whole accumulation phase and sample the payout at ``k = 17, 26, 27, 39, 54``
and ``70``.  All twenty-three rows are asserted here, with the totals, which the notes sum **at
full precision and then round** — 23 115,89 EUR of annuity payments that way against 23 115,83 EUR
from the rounded cells.  The goldens are hard-coded rather than pickled so a reviewer can compare
them with the notes by eye, at the precision the notes display: money to the cent, ``pols_if`` to
six decimals.

Beyond the worked example this module asserts the notes' three independent rebuilds and its two
closure identities; both documented variants, the *Einmalbeitrag* form (model point 2) and the
2,75 % legacy vintage (model point 6), row by row and in total; all nine ``check_*`` identities
and their residuals — monthly for six of them, per policy **year** for the two account
roll-forwards, the premium split and the § 169 floor — on the anchor and on the six points that
switch an option on, ``check_net_cf()`` among them, this library's first ruling; **one test per
numbered modeling pitfall in the technical notes**, eighteen of them, each named for its pitfall;
the conversion's own group — that the annual layer is unchanged, that the two decrement rates
compound rather than divide, that the annual view regroups rather than reprojects, and that the
annuity is now a monthly instalment; and the frame's shape and sign convention, the enum
accessors, the docstrings, the shipped tables' own provenance, and that an input can be swapped
without touching a formula.

There is **no whole-model-point-table sweep here**: the conventions suite owns the single
sweep, because a model point's first evaluation is the most expensive thing in the run.
"""
import contextlib
import re

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


@contextlib.contextmanager
def model_reading(reference, path, name):
    """A second copy of the model, reading ``path`` in place of one of its input files.

    The filename References live on ``Data``, so pointing one at another same-schema file and
    clearing the caches is the whole of an input swap: no formula changes.
    """
    model = mx.read_model(MODEL_DIR, name=name)
    try:
        setattr(model.Data, reference, str(path))
        model.Data.clear_all()
        model.Projection.clear_all()
        yield model
    finally:
        model.close()


def flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    The conventions suite normalises the same way, and for the same reason.
    """
    return re.sub(r"\s+", " ", doc)


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["RV_DE_S"][0]
INPUT_DIR = MODEL_DIR.parent

CSV_FILES = {"model_point_table.csv", "mort_table.csv", "decl_rate_table.csv",
             "rentenfaktor_table.csv", "charge_table.csv", "lapse_table.csv",
             "freq_load_table.csv", "param_table.csv"}

# The notes' worked-example table, model point 1, read off ``result_cf_annual()`` -- the monthly
# frame summed into policy years.  Rows 0-16 are the whole accumulation phase; 17, 26, 27, 39, 54
# and 70 sample the payout at the first annuity year, the last guaranteed year, the first
# survivor-weighted year and three points down the tail.  `av` and `av_sur` are the two balances
# at the **start** of the row's year, from ``result_pols()``, and are state rather than cash flow.
# The key is the 0-based policy year ``k = policy_year - 1``, so row ``k`` covers months
# ``12k .. 12k + 11``.
#
# k: (pols_if, av, av_sur, premiums, claims_death, claims_lapse, claims_commutation,
#     annuity_payments, expenses, net_cf)

WORKED_EXAMPLE = {
    0:  (1.000000,     0.00,    0.00, 3000.00,   4.88,  158.67,    0.00,   0.00, 451.10,  2385.34),
    1:  (0.938426,  1517.10,   23.28, 2815.28,   9.89,  249.12,    0.00,   0.00,  47.87,  2508.41),
    2:  (0.889902,  4032.52,   84.53, 2669.71,  15.14,  320.11,    0.00,   0.00,  45.76,  2288.69),
    3:  (0.848216,  6335.16,  179.84, 2544.65,  20.70,  362.97,    0.00,   0.00,  43.99,  2116.98),
    4:  (0.812600,  8474.57,  306.74, 2437.80,  26.62,  445.58,    0.00,   0.00,  42.92,  1922.68),
    5:  (0.778360, 10439.40,  461.52, 2335.08,  32.85,  526.51,    0.00,   0.00,  41.87,  1733.85),
    6:  (0.745440, 12238.83,  641.09, 2236.32,  39.41,  601.95,    0.00,   0.00,  40.83,  1554.13),
    7:  (0.713787, 13881.56,  842.56, 2141.36,  46.41,  588.10,    0.00,   0.00,  39.48,  1467.37),
    8:  (0.686908, 15455.93, 1068.70, 2060.72,  53.95,  648.43,    0.00,   0.00,  38.70,  1319.64),
    9:  (0.660906, 16904.27, 1313.89, 1982.72,  61.92,  705.09,    0.00,   0.00,  37.94,  1177.77),
    10: (0.635750, 18232.03, 1575.91, 1907.25,  70.35,  758.18,    0.00,   0.00,  37.18,  1041.55),
    11: (0.611408, 19444.42, 1852.62, 1834.22,  78.94, 1384.79,    0.00,   0.00,  37.86,   332.64),
    12: (0.572603, 20013.45, 2086.42, 1717.81,  87.98,  713.03,    0.00,   0.00,  34.50,   882.30),
    13: (0.553206, 21091.10, 2390.82, 1659.62,  99.18,  752.73,    0.00,   0.00,  33.97,   773.74),
    14: (0.534287, 22078.63, 2706.76, 1602.86, 111.26,  790.09,    0.00,   0.00,  33.43,   668.08),
    15: (0.515827, 22978.50, 3032.52, 1547.48, 124.27,  825.12,    0.00,   0.00,  32.90,   565.19),
    16: (0.497806, 23793.00, 3366.34, 1493.42, 138.27,  857.84, 8596.26,   0.00,  49.65, -8148.61),
    17: (0.336143,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 862.65,  14.36,  -877.01),
    26: (0.311032,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 862.65,  17.36,  -880.01),
    27: (0.307034,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 782.87,  16.14,  -799.01),
    39: (0.229120,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 576.71,  15.74,  -592.45),
    54: (0.055062,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 128.34,   5.64,  -133.99),
    70: (0.000000,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00,   0.00,   0.00,    -0.00),
}

# The twelve months of policy year 1 on the monthly frame -- the view the annual grid could not
# show.  The whole year's Beitrag falls in month 0 (the Versicherungsperiode of this tariff is the
# year, per Sec. 12(1) VVG) together with the acquisition expense; the other eleven months carry a
# death claim, a surrender claim and a twelfth of the maintenance expense.  A surrender in any of
# them is paid cv_pp(0), the value struck at the end of the current Versicherungsperiode.
#
# t: (pols_if, premiums, claims_death, claims_lapse, expenses, net_cf, liability_cf)

MONTHS_YEAR_1 = {
    0:  (1.000000, 3000.00, 0.42, 13.61, 404.38, 2581.59, -2581.59),
    1:  (0.994718,    0.00, 0.42, 13.54,   4.36,  -18.32,    18.32),
    2:  (0.989464,    0.00, 0.41, 13.47,   4.34,  -18.22,    18.22),
    3:  (0.984238,    0.00, 0.41, 13.40,   4.31,  -18.12,    18.12),
    4:  (0.979039,    0.00, 0.41, 13.33,   4.29,  -18.03,    18.03),
    5:  (0.973868,    0.00, 0.41, 13.26,   4.27,  -17.93,    17.93),
    6:  (0.968724,    0.00, 0.41, 13.19,   4.25,  -17.84,    17.84),
    7:  (0.963607,    0.00, 0.40, 13.12,   4.22,  -17.74,    17.74),
    8:  (0.958517,    0.00, 0.40, 13.05,   4.20,  -17.65,    17.65),
    9:  (0.953455,    0.00, 0.40, 12.98,   4.18,  -17.56,    17.56),
    10: (0.948418,    0.00, 0.40, 12.91,   4.16,  -17.46,    17.46),
    11: (0.943409,    0.00, 0.40, 12.84,   4.14,  -17.37,    17.37),
}

# The notes' Total row: summed over all 852 months at full precision, then rounded.
TOTALS = {
    "premiums": 35986.30, "claims_death": 1022.04, "claims_lapse": 10688.30,
    "claims_commutation": 8596.26, "annuity_payments": 23115.89, "expenses": 1646.77,
    "net_cf": -9082.96,
}

# The same columns summed from the *rounded* annual cells, which the notes say the Total row is
# not.
ROUNDED_CELL_TOTALS = {
    "premiums": 35986.30, "claims_death": 1022.02, "claims_lapse": 10688.31,
    "claims_commutation": 8596.26, "annuity_payments": 23115.83, "expenses": 1646.75,
    "net_cf": -9082.97,
}

# What the conversion from the annual step moved, and what it did not.  Premiums and the whole
# annual layer are unchanged; three columns moved, each for a stated reason.  Recorded so the
# change is on the record rather than merely absent.
ANNUAL_GRID_TOTALS = {
    "claims_death": 1038.91,        # deaths and surrenders now compete month by month
    "claims_lapse": 10670.70,       # the other side of the same shift
    "annuity_payments": 23485.03,   # twelve instalments through the year, not one lump at its start
    "expenses": 1669.77,            # a mid-year leaver bears the months it was there
}
ANNUAL_GRID_UNCHANGED = ("premiums", "claims_commutation")

# The notes' independent check 1 -- the first year, t = 0, rebuilt from the tariff parameters
# alone.
YEAR_ONE = {
    "beitragssumme": 51000.00, "alpha_total": 1275.00, "beta": 120.00, "gamma": 0.00,
    "mort_rate_guar": 0.00145610, "rho": 4.3683, "charges_due": 1399.3683,
    "prem_to_av": 1600.6317, "int_credited": 16.0063, "av_end": 1616.6380,
    "spread_diff": 1030.2000, "cv_floor": 2646.8380, "cv_tariff": 1608.6189,
    # The decrements are where the month enters: the annual rates, their geometric twelfths, the
    # first month's exits and the year's totals as a sum of twelve.
    "mort_rate": 0.00167451, "mort_rate_mth": 0.00013965,
    "lapse_rate": 0.06, "lapse_rate_mth": 0.00514301,
    "deaths_mth_0": 0.00013965, "lapses_mth_0": 0.00514229,
    "deaths": 0.00162796, "lapses": 0.05994608,
    "claims_death": 4.8839, "claims_lapse": 158.6676, "expenses": 451.1043,
    "net_cf": 2385.3442,
    # What the annual grid gave for the same year: the same survivors at the anniversary, a
    # different split between the two decrements.
    "annual_grid_deaths": 0.00167451, "annual_grid_lapses": 0.05989953,
}

# The notes' independent check 3 -- the Rentenbeginn rebuilt from the two balances.
CONVERSION = {
    "av_pp": 51070.4278, "av_sur_pp": 7718.5532, "capital_gross": 58788.9809,
    "val_reserve": 881.8347, "capital_conv": 59670.8156,
    "rate_guar": 28.00, "rate_curr": 32.00, "rate_appl": 32.00,
    "annuity_guar_mth": 190.9466, "annuity_sur_mth": 22.9136, "annuity_pp": 213.8602,
    "pols_surv_rb": 0.480205, "pols_if_203": 0.481648,
    "pols_death_203": 0.000222, "pols_lapse_203": 0.001220,
    "commutations": 0.144061, "claims_commutation": 8596.2645,
    "annuitisations": 0.336143, "annuity_payments_year_18": 862.6523,
}

# The notes' closure split, summed over all 852 months at full precision.
CLOSURE = {"deaths": 0.371014, "lapses": 0.484924, "commutations": 0.144061,
           "survivors": 0.000000}

# Variant A -- the Einmalbeitrag form, model point 2, on the annual view.
# k: (pols_if, av, av_sur, premiums, claims_death, claims_lapse, annuity_payments,
#     expenses, net_cf)
EINMAL = {
    0:  (1.000000,     0.00,    0.00, 50000.00,  76.88, 2891.05,    0.00, 451.10, 46580.97),
    1:  (0.938426, 44310.12,  680.01,     0.00,  78.45, 2267.01,    0.00,  47.87, -2393.33),
    11: (0.611187, 31246.12, 5757.88,     0.00, 117.65, 2222.96,    0.00,  37.85, -2378.46),
    12: (0.572308,     0.00,    0.00,     0.00,   0.00,    0.00, 1548.54,  22.06, -1570.60),
    23: (0.532497,     0.00,    0.00,     0.00,   0.00,    0.00, 1433.87,  25.74, -1459.61),
    39: (0.370668,     0.00,    0.00,     0.00,   0.00,    0.00,  982.17,  25.57, -1007.74),
    65: (0.000285,     0.00,    0.00,     0.00,   0.00,    0.00,    0.77,   0.07,    -0.84),
}
EINMAL_TOTALS = {"premiums": 50000.00, "claims_death": 1128.88, "claims_lapse": 21374.96,
                 "claims_commutation": 0.00, "annuity_payments": 46844.86,
                 "expenses": 1908.71, "net_cf": -21257.42}
EINMAL_ROUNDED_NET_CF = -21257.45

# Variant B -- the 2,75 % legacy vintage, model point 6, an in-force cell whose frame opens at
# month t = 240 (duration_init = 20) and whose Rentenbeginn falls at the end of month 299.
# k: (pols_if, av, av_sur, premiums, int_credited, bonus_credited, claims_death,
#     claims_lapse, claims_commutation, annuity_payments, net_cf)
LEGACY = {
    20: (1.000000, 61190.90, 3200.00, 2592.00, 1747.81, 81.60, 259.29, 2052.23,     0.00,    0.00,    210.52),
    21: (0.965315, 63039.53, 3167.78, 2502.10, 1796.18, 80.78, 283.18, 2104.86,     0.00,    0.00,     45.22),
    22: (0.931471, 64758.71, 3134.66, 2414.37, 1841.04, 79.93, 308.66, 2153.51,     0.00,    0.00,   -115.50),
    23: (0.898434, 66348.31, 3100.58, 2328.74, 1882.41, 79.06, 335.83, 2198.15,     0.00,    0.00,   -271.80),
    24: (0.866171, 67807.93, 3065.46, 2245.12, 1920.26, 78.17, 364.77, 2238.75, 21974.56,    0.00, -22428.44),
    25: (0.584254,     0.00,    0.00,    0.00,    0.00,  0.00,   0.00,    0.00,     0.00, 2343.02,  -2372.27),
    49: (0.342195,     0.00,    0.00,    0.00,    0.00,  0.00,   0.00,    0.00,     0.00, 1337.26,  -1365.93),
    78: (0.000000,     0.00,    0.00,    0.00,    0.00,  0.00,   0.00,    0.00,     0.00,    0.00,     -0.00),
}
LEGACY_TOTALS = {"premiums": 12082.32, "int_credited": 9187.70, "bonus_credited": 399.55,
                 "claims_death": 1551.74, "claims_lapse": 10747.50,
                 "claims_commutation": 21974.56, "annuity_payments": 60594.20,
                 "expenses": 1445.06, "net_cf": -84230.73}

# What a single global 1,00 % Rechnungszins does to the legacy cell (pitfall 15).  The point is
# that it is a misallocation between the two accounts, not a hole in the total.
LEGACY_VINTAGE_PROBE = {
    "av_own": 82833.3752, "av_global": 76439.8722,
    "sur_own": 3629.3454, "sur_global": 9292.7587,
    "conv_own": 87759.6614, "conv_global": 87018.6203,
}

# The counterfactual of pitfall 1: crediting the declared rate *on top of* the guarantee.
DOUBLE_CREDIT = {"year_one": 56.8224, "correct_year_one": 40.8161,
                 "capital_gross": 63768.6926, "av_sur": 12698.2649}

CHECKS = ("check_net_cf", "check_pols_roll_fwd", "check_decrement_closure",
          "check_av_roll_fwd", "check_av_sur_roll_fwd", "check_prem_split",
          "check_cv_floor", "check_annuity_conv", "check_annuity_guarantee")


# --- The worked example
@pytest.mark.parametrize("k", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_rv_anchor, k):
    """Every cell of the notes' twenty-three-row table, to the displayed precision.

    Read off ``result_cf_annual()`` and ``result_pols()``: the cash flows are the policy year's
    twelve months summed, the two balances are the year's own annual state, and ``pols_if`` is
    the count at the year's start -- which is ``pols_if(12k)`` on the monthly frame.
    """
    (pols_if, av, av_sur, prem, cd, cl, cc, ann, exp, net) = WORKED_EXAMPLE[k]
    p = de_rv_anchor
    row = p.result_cf_annual().loc[k + 1]
    state = p.result_pols().loc[k + 1]
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_if(12 * k) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(k) == pytest.approx(av, abs=CENT) == pytest.approx(state["av"], abs=CENT)
    assert p.av_sur(k) == pytest.approx(av_sur, abs=CENT)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_lapse"] == pytest.approx(cl, abs=CENT)
    assert row["claims_commutation"] == pytest.approx(cc, abs=CENT)
    assert row["annuity_payments"] == pytest.approx(ann, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)
    assert row["liability_cf"] == pytest.approx(-net, abs=CENT)


@pytest.mark.parametrize("t", sorted(MONTHS_YEAR_1))
def test_the_twelve_months_of_policy_year_one(de_rv_anchor, t):
    """The monthly frame inside policy year 1 -- the view the annual grid could not show.

    Month 0 collects the whole year's *Beitrag* -- the *Versicherungsperiode* of this tariff is
    the year, so ``prem_due`` is true there and nowhere else in the year -- and bears the
    acquisition expense; months 1 to 11 collect nothing and carry a death claim, a surrender
    claim and a twelfth of the maintenance expense.  Every surrender in the year is paid
    ``cv_pp(0)``, the value Sec. 169(3) VVG strikes at the end of the current
    *Versicherungsperiode*.
    """
    pols_if, prem, cd, cl, exp, net, liab = MONTHS_YEAR_1[t]
    p = de_rv_anchor
    assert p.age(t) == 50 and p.duration(t) == 0 and p.policy_year(t) == 1
    assert p.calendar_year(t) == 2026
    assert p.is_anniv(t) == (t == 11)
    assert p.prem_due(t) == (t == 0)
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "COMMUTATION") == 0.0
    assert p.annuity_payments(t) == 0.0
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(liab, abs=CENT)
    # The amounts a claim is paid are the policy year's, in every month of it.
    assert p.cv_pp(0) == pytest.approx(YEAR_ONE["cv_floor"], abs=CENT)
    assert p.db_pp(0) == pytest.approx(3000.00, abs=CENT)


def test_the_annual_view_regroups_the_monthly_frame_rather_than_reprojecting_it(de_rv_anchor):
    """``result_cf_annual()`` is the same numbers, grouped: every cash flow column is the sum of
    that policy year's twelve months, ``pols_if`` and ``pols_annuity`` are the counts at its
    start.  A second projection on an annual grid would not satisfy both at once.
    """
    p = de_rv_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert len(df) == 852 and len(ann) == 71
    assert list(ann.index) == list(range(1, 72)) and ann.index.name == "policy_year"
    for k in (0, 11, 17, 70):
        months = df.loc[12 * k:12 * k + 11]
        for column in ("premiums", "claims_death", "claims_lapse", "claims_commutation",
                       "annuity_payments", "expenses", "net_cf"):
            assert ann.loc[k + 1, column] == pytest.approx(months[column].sum(), rel=1e-12), (
                k, column)
        assert ann.loc[k + 1, "pols_if"] == pytest.approx(p.pols_if(12 * k), rel=1e-15)
        assert ann.loc[k + 1, "pols_annuity"] == pytest.approx(p.pols_annuity(12 * k), rel=1e-15)
    for column in df.columns:
        if column not in ("pols_if", "pols_annuity"):
            assert ann[column].sum() == pytest.approx(df[column].sum(), rel=1e-12), column


def test_the_worked_example_totals_are_summed_at_full_precision(de_rv_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells.

    The largest gap is ``annuity_payments``, 23 115,89 EUR against 23 115,83 EUR.

    The monthly frame totals to the same money as the annual view, the grouping being a
    regrouping; and the four columns the conversion moved are asserted against the annual-step
    model's own totals, so that what changed is on the record rather than merely absent.
    """
    df = de_rv_anchor.result_cf_annual()
    monthly = de_rv_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
        assert monthly[column].sum() == pytest.approx(total, abs=CENT), column
        assert sum(round(v, 2) for v in df[column]) == pytest.approx(
            ROUNDED_CELL_TOTALS[column], abs=CENT), column
    assert TOTALS["net_cf"] != ROUNDED_CELL_TOTALS["net_cf"]
    # Undiscounted, the cell collects 35 986,30 EUR and pays out 45 069,26 EUR.
    outgo = (df["claims_death"] + df["claims_lapse"] + df["claims_commutation"]
             + df["annuity_payments"] + df["expenses"]).sum()
    assert outgo == pytest.approx(45069.26, abs=CENT)
    # What the finer grid moved, against the annual grid's own totals -- and what it did not.
    for column, old in ANNUAL_GRID_TOTALS.items():
        assert TOTALS[column] != pytest.approx(old, abs=0.5), column
    for column in ANNUAL_GRID_UNCHANGED:
        assert TOTALS[column] == pytest.approx(
            {"premiums": 35986.30, "claims_commutation": 8596.26}[column], abs=CENT), column
    # The annuity fell and the expenses fell; the two decrements swapped, keeping their total.
    assert TOTALS["annuity_payments"] < ANNUAL_GRID_TOTALS["annuity_payments"]
    assert TOTALS["expenses"] < ANNUAL_GRID_TOTALS["expenses"]
    assert TOTALS["claims_death"] < ANNUAL_GRID_TOTALS["claims_death"]
    assert TOTALS["claims_lapse"] > ANNUAL_GRID_TOTALS["claims_lapse"]
    assert (TOTALS["claims_death"] + TOTALS["claims_lapse"]) == pytest.approx(
        ANNUAL_GRID_TOTALS["claims_death"] + ANNUAL_GRID_TOTALS["claims_lapse"], abs=1.0)


def test_year_one_rebuilt_from_the_tariff_parameters(de_rv_anchor):
    """The notes' check 1: the first year, ``t = 0``, from the tariff parameters, reading no
    recursion.

    The acquisition charge takes 42,5 % of the year-one premium, and the Sec. 169(3) floor
    then stands 1 030,20 EUR **above** the tariff *Deckungskapital*.
    """
    p = de_rv_anchor
    assert p.beitragssumme_pp() == pytest.approx(
        17 * 3000.00, abs=CENT) == pytest.approx(YEAR_ONE["beitragssumme"], abs=CENT)
    assert p.alpha_total_pp() == pytest.approx(
        0.025 * p.beitragssumme_pp(), abs=CENT) == pytest.approx(
            YEAR_ONE["alpha_total"], abs=CENT)
    assert p.charge_acq_pp(0) == pytest.approx(YEAR_ONE["alpha_total"], abs=CENT)
    assert p.charge_acq_pp(1) == 0.0                 # zillmered: all of it in the first year
    assert p.charge_prem_pp(0) == pytest.approx(YEAR_ONE["beta"], abs=CENT)
    assert p.charge_admin_pp(0) == YEAR_ONE["gamma"]     # the account is empty
    assert p.mort_rate_guar(0) == pytest.approx(YEAR_ONE["mort_rate_guar"], abs=5e-9)
    assert p.charge_risk_pp(0) == pytest.approx(YEAR_ONE["rho"], abs=5e-5)
    assert p.charge_due_pp(0) == pytest.approx(YEAR_ONE["charges_due"], abs=5e-5)
    assert p.charge_from_av_pp(0) == 0.0                 # the premium meets them all
    assert p.prem_to_av_pp(0) == pytest.approx(YEAR_ONE["prem_to_av"], abs=5e-5)
    assert p.int_credited_pp(0) == pytest.approx(YEAR_ONE["int_credited"], abs=5e-5)
    assert p.av_pp_at(0, "AFT_INT") == pytest.approx(YEAR_ONE["av_end"], abs=5e-5)
    assert p.spread_diff_pp_at(0, "AFT_INT") == pytest.approx(
        (0.0 + 1275.00 - 255.00) * 1.01, abs=5e-5)
    assert p.cv_tariff_pp(0) == pytest.approx(YEAR_ONE["cv_tariff"], abs=5e-5)
    assert p.cv_pp(0) == pytest.approx(YEAR_ONE["cv_floor"], abs=5e-5)   # the floor wins
    # Every line above is annual and is unchanged by the move to a monthly grid.  The decrements
    # are where the month enters: the year's rate, its geometric twelfth, the first month's exits
    # and the year's totals as a sum of twelve.
    assert p.mort_rate(0) == pytest.approx(YEAR_ONE["mort_rate"], abs=5e-9)
    assert p.mort_rate_mth(0) == pytest.approx(YEAR_ONE["mort_rate_mth"], abs=5e-9)
    assert p.lapse_rate(0) == YEAR_ONE["lapse_rate"]
    assert p.lapse_rate_mth(0) == pytest.approx(YEAR_ONE["lapse_rate_mth"], abs=5e-9)
    assert p.pols_death(0) == pytest.approx(YEAR_ONE["deaths_mth_0"], abs=5e-9)
    assert p.pols_lapse(0) == pytest.approx(YEAR_ONE["lapses_mth_0"], abs=5e-9)
    deaths = sum(p.pols_death(t) for t in range(12))
    lapses = sum(p.pols_lapse(t) for t in range(12))
    assert deaths == pytest.approx(YEAR_ONE["deaths"], abs=5e-9)
    assert lapses == pytest.approx(YEAR_ONE["lapses"], abs=5e-9)
    row = p.result_cf_annual().loc[1]
    assert row["claims_death"] == pytest.approx(YEAR_ONE["claims_death"], abs=5e-5)
    assert row["claims_lapse"] == pytest.approx(YEAR_ONE["claims_lapse"], abs=5e-5)
    assert row["expenses"] == pytest.approx(YEAR_ONE["expenses"], abs=5e-5)
    assert row["net_cf"] == pytest.approx(YEAR_ONE["net_cf"], abs=5e-5)
    # The competing-decrement shift: fewer deaths and more surrenders than the annual grid's
    # single year-end ordering gave, and the same survivors at the anniversary either way.
    assert deaths < YEAR_ONE["annual_grid_deaths"]
    assert lapses > YEAR_ONE["annual_grid_lapses"]
    assert p.pols_if(12) == pytest.approx(
        1.0 - YEAR_ONE["annual_grid_deaths"] - YEAR_ONE["annual_grid_lapses"], abs=5e-9)


def test_the_two_credits_sum_to_the_declared_rate_to_ten_decimals(de_rv_anchor):
    """The notes' check 2: guarantee plus interest surplus **is** the declared rate.

    Both are struck on the same base, so the sum is the declared rate applied once.
    """
    p = de_rv_anchor
    base = p.av_pp_at(0, "AFT_PREM")
    guarantee, surplus = 0.0100 * base, 0.0155 * base
    assert guarantee == pytest.approx(16.0063170368, abs=5e-11)
    assert surplus == pytest.approx(24.8097914070, abs=5e-11)
    assert guarantee + surplus == pytest.approx(0.0255 * base, abs=5e-11)
    assert p.int_credited_pp(0) == pytest.approx(guarantee, rel=1e-12)
    assert p.bonus_credited_pp(0) == pytest.approx(surplus, rel=1e-12)


def test_the_rentenbeginn_rebuilt_from_the_two_balances(de_rv_anchor):
    """The notes' check 3, and the policy-year 17 and 18 figures it lands on.

    The *Rentenbeginn* is the end of month 203, which is the end of policy year 16, so every
    balance here is an annual construction struck at an anniversary and is what the annual-step
    model gave.  What changed is the annuity: ``annuity_pp`` is now **one monthly instalment**,
    and the first payout year's outgo is twelve of them.
    """
    p = de_rv_anchor
    assert p.av_pp_at(16, "AFT_INT") == pytest.approx(CONVERSION["av_pp"], abs=CENT)
    assert p.av_sur_pp_at(16, "AFT_INT") == pytest.approx(CONVERSION["av_sur_pp"], abs=CENT)
    assert p.capital_gross_pp() == pytest.approx(
        CONVERSION["av_pp"] + CONVERSION["av_sur_pp"], abs=CENT)
    assert p.val_reserve_pp() == pytest.approx(
        0.015 * p.capital_gross_pp(), rel=1e-12) == pytest.approx(
            CONVERSION["val_reserve"], abs=CENT)
    assert p.capital_conv_pp() == pytest.approx(CONVERSION["capital_conv"], abs=CENT)
    assert p.annuity_rate_appl() == CONVERSION["rate_appl"]
    assert p.annuity_guar_mth_pp() == pytest.approx(
        p.capital_conv_pp() / 10000.0 * 32.00, rel=1e-12)
    assert p.annuity_guar_mth_pp() == pytest.approx(CONVERSION["annuity_guar_mth"], abs=5e-5)
    assert p.annuity_sur_mth_pp(17) == pytest.approx(CONVERSION["annuity_sur_mth"], abs=5e-5)
    assert p.annuity_pp(204) == pytest.approx(CONVERSION["annuity_pp"], abs=5e-5)
    assert p.annuity_pp(204) == pytest.approx(
        p.annuity_guar_mth_pp() + p.annuity_sur_mth_pp(17), rel=1e-12)
    assert p.pols_if(203) == pytest.approx(CONVERSION["pols_if_203"], abs=SIX_DP)
    assert p.pols_death(203) == pytest.approx(CONVERSION["pols_death_203"], abs=SIX_DP)
    assert p.pols_lapse(203) == pytest.approx(CONVERSION["pols_lapse_203"], abs=SIX_DP)
    assert p.pols_surv_rb() == pytest.approx(CONVERSION["pols_surv_rb"], abs=SIX_DP)
    assert p.pols_commutation(203) == pytest.approx(0.30 * p.pols_surv_rb(), rel=1e-12)
    assert p.pols_commutation(203) == pytest.approx(CONVERSION["commutations"], abs=SIX_DP)
    assert p.claims(203, "COMMUTATION") == pytest.approx(
        CONVERSION["claims_commutation"], abs=CENT)
    assert p.pols_annuitization(203) == pytest.approx(p.pols_if(204), rel=1e-12)
    assert p.pols_annuitization(203) == pytest.approx(CONVERSION["annuitisations"], abs=SIX_DP)
    assert p.result_cf_annual().loc[18, "annuity_payments"] == pytest.approx(
        CONVERSION["annuity_payments_year_18"], abs=CENT)
    # Twelve instalments on the fixed guaranteed count -- which is why the first payout year is
    # the annual-step model's figure to the cent.
    assert p.result_cf_annual().loc[18, "annuity_payments"] == pytest.approx(
        12.0 * CONVERSION["annuity_pp"] * CONVERSION["annuitisations"], abs=CENT)
    # Applying the guaranteed factor alone would give 167,0783 EUR, 87,5 % of the answer.
    assert p.capital_conv_pp() / 10000.0 * 28.00 == pytest.approx(167.0783, abs=5e-5)


def test_the_decrements_close_and_the_account_rolls_forward(de_rv_anchor):
    """The notes' two closure identities, rebuilt here rather than read off a check.

    The decrements are summed over all 852 **months**; the account roll-forward is stated per
    policy **year**, because the *Deckungskapital* is defined at anniversaries.  The 99,54 EUR
    released in policy year 0 is the end-of-year balance carried out by the 0,061574 of a policy
    that died or surrendered at any point in that year.
    """
    p = de_rv_anchor
    n = p.proj_len()
    exits = {"deaths": sum(p.pols_death(t) for t in range(n)),
             "lapses": sum(p.pols_lapse(t) for t in range(n)),
             "commutations": sum(p.pols_commutation(t) for t in range(n))}
    for name, value in exits.items():
        assert value == pytest.approx(CLOSURE[name], abs=SIX_DP), name
    assert p.pols_if(n) == CLOSURE["survivors"] == 0.0
    assert sum(exits.values()) == pytest.approx(p.pols_if_init(), abs=1e-12)

    assert p.av_release(0) == pytest.approx(99.5429, abs=5e-5)
    assert p.av_release(0) == pytest.approx(
        p.av_pp_at(0, "AFT_INT") * (p.pols_if(0) - p.pols_if(12)), rel=1e-12)
    assert (p.av(0) + p.prem_to_av(0) + p.int_credited(0) - p.av_release(0)) == (
        pytest.approx(1517.0951, abs=5e-5)) == p.av(1)
    # In the last accumulation policy year the whole balance is released: the annuitants
    # convert and the commuters cash in.
    assert p.av_release(16) == pytest.approx(
        p.av_pp_at(16, "AFT_INT") * p.pols_if(12 * 16), rel=1e-12)


def test_the_rentengarantiezeit_costs_what_the_notes_say(de_rv_anchor):
    """In the last guaranteed policy year the instalment is paid on the annuitised count.

    ``pols_annuity`` holds at 0,336143 through all twelve months of policy year 27 while
    ``pols_if`` falls to 0,307366 by the last of them, so the year's outgo is the full
    862,65 EUR.  The window is 120 guaranteed **instalments**, months 204 to 323, which is what
    a *Rentengarantiezeit* guarantees and what the annual grid could only approximate.
    """
    p = de_rv_anchor
    for t in (204, 300, 323):
        assert p.pols_annuity(t) == pytest.approx(0.336143, abs=SIX_DP)
    assert p.pols_annuity(324) == pytest.approx(p.pols_if(324), rel=1e-15)
    assert p.pols_if(323) == pytest.approx(0.307366, abs=SIX_DP)
    ann = p.result_cf_annual()
    assert ann.loc[27, "annuity_payments"] == pytest.approx(862.6523, abs=CENT)
    survivor_weighted = sum(p.annuity_pp(t) * p.pols_if(t) for t in range(312, 324))
    assert ann.loc[27, "annuity_payments"] - survivor_weighted > 50.0
    # And the first survivor-weighted year is where the two grids part company.
    assert ann.loc[28, "annuity_payments"] < 862.6523


# --- Variant A -- the Einmalbeitrag form (model point 2)
@pytest.mark.parametrize("k", sorted(EINMAL))
def test_einmalbeitrag_variant_row(klassische_rentenversicherung, k):
    """The notes' variant A table: a 55-year-old woman, one premium, twelve-year deferment."""
    (pols_if, av, av_sur, prem, cd, cl, ann, exp, net) = EINMAL[k]
    p = klassische_rentenversicherung.Projection[2]
    row = p.result_cf_annual().loc[k + 1]
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(k) == pytest.approx(av, abs=CENT)
    assert p.av_sur(k) == pytest.approx(av_sur, abs=CENT)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_lapse"] == pytest.approx(cl, abs=CENT)
    assert row["annuity_payments"] == pytest.approx(ann, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)


def test_the_einmalbeitrag_variant_reads_as_the_notes_say(klassische_rentenversicherung):
    """The three things the notes read off variant A, and its totals: a year-one *Sparbeitrag*
    of 93,5 % of the premium against the anchor's 53,4 %, a net amount at risk that is
    identically zero, and a larger conversion capital than the anchor's."""
    p = klassische_rentenversicherung.Projection[2]
    df = p.result_cf_annual()
    for column, total in EINMAL_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert sum(round(v, 2) for v in df["net_cf"]) == pytest.approx(
        EINMAL_ROUNDED_NET_CF, abs=CENT)
    assert p.model_point()["premium_form"] == "einmal"
    assert p.prem_pp(0) == pytest.approx(
        50000.00, abs=CENT) == p.beitragssumme_pp()
    assert all(p.prem_pp(k) == 0.0 for k in range(1, 12))
    # The single premium falls in month 0 and in no other month of the whole run.
    assert p.premiums(0) == pytest.approx(50000.00, abs=CENT)
    assert all(p.premiums(t) == 0.0 for t in range(1, 852))
    assert p.alpha_total_pp() == pytest.approx(1250.00, abs=CENT)
    assert p.prem_to_av_pp(0) == pytest.approx(46750.00, abs=CENT)   # 93,5 % of the premium
    assert all(p.nar_pp(k) == 0.0 and p.charge_risk_pp(k) == 0.0 for k in range(12))
    assert p.capital_conv_pp() == pytest.approx(62913.28, abs=CENT)
    assert p.annuity_guar_mth_pp() == pytest.approx(201.32, abs=CENT)
    assert p.capital_conv_pp() > CONVERSION["capital_conv"]
    assert float(p.model_point()["kapitalwahl_rate"]) == 0.0


# --- Variant B -- the 2,75 % legacy vintage (model point 6)
@pytest.mark.parametrize("k", sorted(LEGACY))
def test_legacy_vintage_variant_row(klassische_rentenversicherung, k):
    """The notes' variant B table, including the two crediting columns whose ratio is the point."""
    (pols_if, av, av_sur, prem, interest, bonus, cd, cl, cc, ann, net) = LEGACY[k]
    p = klassische_rentenversicherung.Projection[6]
    row = p.result_cf_annual().loc[k + 1]
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_if(12 * k) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(k) == pytest.approx(av, abs=CENT)
    assert p.av_sur(k) == pytest.approx(av_sur, abs=CENT)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert p.int_credited(k) == pytest.approx(interest, abs=CENT)
    assert p.bonus_credited(k) == pytest.approx(bonus, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_lapse"] == pytest.approx(cl, abs=CENT)
    assert row["claims_commutation"] == pytest.approx(cc, abs=CENT)
    assert row["annuity_payments"] == pytest.approx(ann, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)


def test_the_legacy_vintage_variant_reads_as_the_notes_say(klassische_rentenversicherung):
    """Variant B's totals and its three legacy asymmetries: every euro of the 399,55 EUR of
    surplus is the declared rate on the *Ansammlungsguthaben*'s own balance, because
    ``bonus_rate`` is zero in every policy year; the 2005 *Rentenfaktor* beats the current one;
    and the 40 permille charge set carries no *Stornoabzug*."""
    p = klassische_rentenversicherung.Projection[6]
    df = p.result_cf_annual()
    state = p.result_pols()
    for column, total in LEGACY_TOTALS.items():
        source = state if column in ("int_credited", "bonus_credited") else df
        assert source[column].sum() == pytest.approx(total, abs=CENT), column
    assert p.result_cf().index[0] == 240 == p.t_start()
    assert p.k_start() == 20 == int(p.model_point()["duration_init"])
    assert p.int_rate_guar() == 0.0275
    assert all(p.decl_rate(k) == 0.0255 and p.bonus_rate(k) == 0.0
               and p.bonus_credited_pp(k) == pytest.approx(0.0255 * p.av_sur_pp(k), rel=1e-12)
               for k in range(20, 25))
    assert state["int_credited"].sum() > 20 * state["bonus_credited"].sum()
    assert (p.annuity_rate_guar(), p.annuity_rate_curr(),
            p.annuity_rate_appl()) == (34.00, 32.00, 34.00)      # the guarantee wins
    assert p.capital_conv_pp() == pytest.approx(87759.66, abs=CENT)
    assert p.model_point()["charge_id"] == "zillmer_40"
    assert p.surr_charge_pp(20) == 0.0
    assert p.cv_pp(20) == pytest.approx(68586.25, abs=CENT) == p.cv_tariff_pp(20)
    assert p.cv_floor_pp(20) == pytest.approx(65304.65, abs=CENT)
    assert p.cv_floor_pp(20) < p.cv_tariff_pp(20)               # inoperative twenty years in
    assert p.alpha_total_pp() == pytest.approx(0.040 * 64800.00, abs=CENT)


# --- Pitfall 1: adding the declared rate on top of the guarantee
def test_pitfall_1_the_declared_rate_is_not_added_on_top_of_the_guarantee(
        klassische_rentenversicherung, de_rv_anchor):
    """``bonus_rate = max(0, decl_rate - int_rate_guar)``, on the same base as the guarantee.

    The counterfactual is rebuilt rather than asserted from prose: crediting the whole declared
    rate as a *surplus* reaches 63 768,69 EUR at the *Rentenbeginn* against 58 788,98 EUR.
    """
    p = de_rv_anchor
    for k in (0, 4, 11, 16):
        base = p.av_pp_at(k, "AFT_PREM")
        assert p.bonus_rate(k) == pytest.approx(0.0255 - 0.0100, abs=1e-12)
        assert p.int_credited_pp(k) + p.bonus_rate(k) * base == pytest.approx(
            p.decl_rate(k) * base, rel=1e-12)
    wrong = 0.0                       # the double-credited Ansammlungsguthaben, year by year
    for k in range(17):
        d = p.decl_rate(k)
        wrong = wrong + d * p.av_pp_at(k, "AFT_PREM") + d * wrong
    assert wrong == pytest.approx(DOUBLE_CREDIT["av_sur"], abs=CENT)
    assert p.av_pp_at(16, "AFT_INT") + wrong == pytest.approx(
        DOUBLE_CREDIT["capital_gross"], abs=CENT)
    assert (p.av_pp_at(16, "AFT_INT") + wrong) / p.capital_gross_pp() - 1 == (
        pytest.approx(0.085, abs=0.0005))
    assert 0.0355 * p.av_pp_at(0, "AFT_PREM") == pytest.approx(
        DOUBLE_CREDIT["year_one"], abs=5e-5)                 # 56,82 EUR against 40,82 EUR
    assert p.int_credited_pp(0) + p.bonus_credited_pp(0) == pytest.approx(
        DOUBLE_CREDIT["correct_year_one"], abs=5e-5)
    # The mirror image: a vintage above the declaration receives no interest surplus at all.
    legacy = klassische_rentenversicherung.Projection[6]
    assert all(legacy.bonus_rate(k) == 0.0 and legacy.int_credited_pp(k) > 0.0
               for k in range(20, 25))


# --- Pitfall 2: getting the within-year order wrong
def test_pitfall_2_the_within_year_order_is_premium_then_charges_then_interest(de_rv_anchor):
    """Interest is credited on the post-premium, post-charge balance and on nothing else.

    Crediting it on the opening balance alone would change year-one interest by the whole of
    ``i x (S(0) - C(0))``, 16,01 EUR of a 1 616,64 EUR closing balance.
    """
    p = de_rv_anchor
    for k in (0, 1, 8, 16):
        assert p.av_pp_at(k, "BEF_PREM") == p.av_pp(k)
        assert p.av_pp_at(k, "AFT_PREM") == pytest.approx(
            p.av_pp(k) + p.prem_to_av_pp(k) - p.charge_from_av_pp(k), rel=1e-12)
        assert p.int_credited_pp(k) == pytest.approx(
            p.int_rate_guar() * p.av_pp_at(k, "AFT_PREM"), rel=1e-12)
        assert p.av_pp_at(k, "AFT_INT") == pytest.approx(
            p.av_pp_at(k, "AFT_PREM") + p.int_credited_pp(k), rel=1e-12)
    opening_only = p.av_pp(0) * (1 + p.int_rate_guar()) + p.prem_to_av_pp(0)
    assert p.av_pp_at(0, "AFT_INT") - opening_only == pytest.approx(
        p.int_rate_guar() * (p.prem_to_av_pp(0) - p.charge_from_av_pp(0)), rel=1e-12)
    assert p.av_pp_at(0, "AFT_INT") - opening_only == pytest.approx(16.0063, abs=5e-5)
    # The two charges struck on start-of-year balances, without which it would be circular.
    assert p.charge_admin_pp(1) == pytest.approx(0.0020 * p.av_pp(1), rel=1e-12)
    # The risk charge reads the **annual** first-order rate, at the first month of the year.
    assert p.charge_risk_pp(1) == pytest.approx(p.mort_rate_guar(12) * p.nar_pp(1), rel=1e-12)
    assert p.mort_rate_guar(12) == p.mort_rate_guar(23)       # flat across the policy year
    assert p.nar_pp(1) == pytest.approx(max(0.0, p.db_base_pp(1) - p.av_pp(1)), rel=1e-12)


# --- Pitfall 3: applying only the guaranteed Rentenfaktor
def test_pitfall_3_the_applied_rentenfaktor_is_the_higher_of_two(
        klassische_rentenversicherung, de_rv_anchor):
    """``max(garantierter, aktueller)``, with both branches shipped and both exercised."""
    p = de_rv_anchor
    assert (p.annuity_rate_guar(), p.annuity_rate_curr(), p.annuity_rate_appl()) == (
        28.00, 32.00, 32.00)                                    # the current factor wins
    # Point 13: the guarantee binds over a `low` scenario, and guar_capital_pp binds with it.
    guar = klassische_rentenversicherung.Projection[13]
    assert guar.model_point()["rf_scenario_id"] == "low"
    assert (guar.annuity_rate_guar(), guar.annuity_rate_curr(),
            guar.annuity_rate_appl()) == (27.00, 24.27, 27.00)  # the guarantee wins
    assert guar.capital_gross_pp() == pytest.approx(50930.99, abs=CENT)
    assert guar.capital_conv_pp() == 60000.00                   # the contract-value floor
    assert guar.annuity_guar_mth_pp() == pytest.approx(60000.0 / 10000.0 * 27.00, rel=1e-12)
    for point_id in (1, 2, 5, 6, 9, 13, 14):
        q = klassische_rentenversicherung.Projection[point_id]
        assert q.annuity_rate_appl() >= q.annuity_rate_guar()
        assert q.check_annuity_conv() is True


# --- Pitfall 4: weighting the guaranteed annuity by survivors
def test_pitfall_4_the_guaranteed_annuity_is_not_weighted_by_survivors(
        klassische_rentenversicherung, de_rv_anchor):
    """Inside the *Rentengarantiezeit* the instalment is due whether the annuitant lives or not.

    The window is ``12m`` guaranteed **instalments** on the monthly grid, which is what a
    *Rentengarantiezeit* guarantees: months ``12n`` to ``12n + 12m - 1``.
    """
    p = de_rv_anchor
    n, m = 17, 10
    assert int(p.model_point()["rgz_years"]) == m
    assert all(p.pols_annuity(t) == pytest.approx(p.pols_annuitization(12 * n - 1), rel=1e-12)
               for t in range(12 * n, 12 * (n + m)))
    assert all(p.pols_annuity(t) == pytest.approx(p.pols_if(t), rel=1e-12)
               for t in (12 * (n + m), 12 * (n + m) + 50, 650))
    assert all(p.pols_annuity(t) == 0.0 for t in range(12 * n))
    assert p.pols_annuity(12 * n) == pytest.approx(p.pols_if(12 * n), rel=1e-12)
    assert p.pols_annuity(12 * (n + m) - 1) > p.pols_if(12 * (n + m) - 1)
    assert p.check_annuity_guarantee() is True
    # Point 10 carries a twenty-year window; point 9 carries none at all.
    long_rgz = klassische_rentenversicherung.Projection[10]
    n10 = 12 * int(long_rgz.model_point()["aufschub_y"])
    assert int(long_rgz.model_point()["rgz_years"]) == 20
    assert long_rgz.pols_annuity(n10 + 12 * 20 - 1) == pytest.approx(
        long_rgz.pols_annuitization(n10 - 1), rel=1e-12)
    assert long_rgz.pols_annuity(n10 + 12 * 20) == pytest.approx(
        long_rgz.pols_if(n10 + 12 * 20), rel=1e-12)
    none_rgz = klassische_rentenversicherung.Projection[9]
    n9 = 12 * int(none_rgz.model_point()["aufschub_y"])
    assert int(none_rgz.model_point()["rgz_years"]) == 0
    assert all(none_rgz.pols_annuity(t) == pytest.approx(none_rgz.pols_if(t), rel=1e-12)
               for t in range(n9, n9 + 5))


# --- Pitfall 5: treating Beitragsfreistellung as a lapse
def test_pitfall_5_beitragsfreistellung_is_not_a_lapse(klassische_rentenversicherung):
    """The conversion moves no policy; the contract keeps its vintage and its factor.

    Surrender does **not** cease -- a *beitragsfrei* contract keeps its Sec. 168 VVG
    *Kündigung* right -- and only the Sec. 165 cash-out branch empties a cohort in one year.
    """
    p = klassische_rentenversicherung.Projection[7]
    pup = int(p.model_point()["pup_year"])   # the contractual policy year, so year k = pup - 1
    assert pup == 10 and p.pup_cashout() is False
    assert p.paid_up(pup - 1) is True and p.paid_up(pup - 2) is False
    assert p.prem_pp(pup - 2) == pytest.approx(3600.00, abs=CENT)
    assert all(p.prem_pp(k) == 0.0 for k in (pup - 1, pup, pup + 4))
    assert p.int_rate_guar() == 0.0100 and p.annuity_rate_guar() == 28.00   # both unchanged
    # The conversion itself moves nobody: the exit in the year before, which reads the
    # duration-9 table rate, is the ordinary one.
    assert p.lapse_rate(12 * (pup - 2)) == 0.035
    assert p.pols_lapse(12 * (pup - 2)) == pytest.approx(
        p.pols_if_at(12 * (pup - 2), "BEF_LAPSE") * p.lapse_rate_mth(12 * (pup - 2)),
        rel=1e-12)
    assert p.pols_if(12 * (pup - 1)) == pytest.approx(0.668738, abs=SIX_DP)
    # The reset is real money, and it is credited in the transition row.
    assert p.av_pp_at(pup - 2, "AFT_INT") == pytest.approx(30261.4467, abs=CENT)
    assert p.pup_value_pp() == pytest.approx(30303.9053, abs=CENT) == p.av_pp(pup - 1)
    assert p.pup_uplift(pup - 2) == pytest.approx(28.3937, abs=CENT)
    assert p.pup_uplift(pup - 1) == 0.0
    assert p.spread_diff_pp(pup - 1) == 0.0                   # the two accounts have merged
    # Surrender continues after the election, and the admin charge steps up.
    assert p.result_cf_annual().loc[pup, "claims_lapse"] == pytest.approx(764.5961, abs=CENT)
    assert p.charge_admin_pp(pup - 2) == pytest.approx(0.0020 * p.av_pp(pup - 2), rel=1e-12)
    assert p.charge_admin_pp(pup - 1) == pytest.approx(
        0.0030 * p.av_pp(pup - 1), rel=1e-12) == (
            p.charge_from_av_pp(pup - 1) - p.charge_risk_pp(pup - 1))
    assert p.check_av_roll_fwd() is p.check_pols_roll_fwd() is True
    # Point 8 is the other statutory branch: below the Mindestversicherungsleistung the
    # contract is cashed out instead of made paid-up, and the whole cohort leaves at once.
    cash = klassische_rentenversicherung.Projection[8]
    assert cash.pup_cashout() is True and cash.lapse_rate(12) == 1.0
    assert cash.pup_value_pp() / 10000.0 * cash.annuity_rate_guar() == pytest.approx(
        5.4518, abs=5e-5)
    # An annual rate of 1 is a **dated contractual act**, not an experience rate: Sec. 165 VVG
    # makes the cash-out fall at the end of the Versicherungsperiode, so lapse_rate_mth places
    # the whole decrement in the anniversary month and not a twelfth of the way into the year.
    assert [t for t in range(12, 24) if cash.lapse_rate_mth(t) == 1.0] == [23]
    assert all(cash.lapse_rate_mth(t) == 0.0 for t in range(12, 23))
    assert cash.claims(23, "LAPSE") == pytest.approx(1828.4915, abs=CENT)
    assert (cash.result_cf().loc[12:22, "claims_lapse"] == 0.0).all()
    assert cash.pols_if(24) == 0.0
    assert cash.result_cf().loc[24:].abs().sum().sum() == 0.0


# --- Pitfall 6: booking the Kostenbeitrag as an expense
def test_pitfall_6_the_kostenbeitrag_is_not_an_expense(de_rv_anchor, tmp_path):
    """``expenses`` is invariant to ``beta_rate`` and ``gamma_rate``; ``av_pp(k+1)`` is not."""
    import pandas as pd

    p = de_rv_anchor
    assert p.result_cf_annual().loc[1, "expenses"] == pytest.approx(451.1043, abs=5e-5)
    assert p.charge_due_pp(0) * p.pols_if(0) == pytest.approx(1399.3683, abs=5e-5)
    assert p.net_cf(0) == pytest.approx(
        p.premiums(0) - p.claims(0) - p.annuity_payments(0) - p.expenses(0), rel=1e-12)

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv")
    is_25 = charges["charge_id"] == "zillmer_25"
    charges.loc[is_25 & (charges["item"] == "beta_rate"), "value"] = 0.08
    charges.loc[is_25 & (charges["item"] == "gamma_rate"), "value"] = 0.004
    alt = tmp_path / "charge_table_doubled.csv"
    charges.to_csv(alt, index=False)

    with model_reading("charge_file", alt, "RV_DE_S_charges") as model:
        q = model.Projection[1]
        assert q.charge_prem_pp(0) == pytest.approx(0.08 * 3000.00, abs=CENT)
        assert all(q.expenses(t) == pytest.approx(p.expenses(t), rel=1e-12)
                   for t in (0, 4, 16, 60, 203))
        assert p.av_pp(1) - q.av_pp(1) == pytest.approx(0.04 * 3000.00 * 1.01, abs=CENT)


# --- Pitfall 7: computing the surrender value off the zillmered reserve
def test_pitfall_7_the_surrender_value_is_floored_at_the_spread_reserve(de_rv_anchor):
    """The Sec. 169(3) floor binds through policy year 4 and stops in policy year 5, so both
    branches of ``max(cv_tariff_pp, cv_floor_pp)`` are exercised on the anchor cell alone.

    All of it is annual: the surrender value is struck at the end of the *Versicherungsperiode*
    and a surrender in any month of policy year ``k`` is paid ``cv_pp(k)``.
    """
    p = de_rv_anchor
    assert all(p.cv_pp(k) == pytest.approx(max(p.cv_tariff_pp(k), p.cv_floor_pp(k)), rel=1e-12)
               and p.cv_floor_pp(k) == pytest.approx(
                   p.av_pp_at(k, "AFT_INT") + p.spread_diff_pp_at(k, "AFT_INT"), rel=1e-12)
               for k in range(17))
    assert all(p.cv_floor_pp(k) > p.cv_tariff_pp(k) for k in range(4))
    assert all(p.cv_floor_pp(k) < p.cv_tariff_pp(k) for k in range(4, 17))
    assert p.cv_pp(3) == pytest.approx(10709.9704, abs=CENT)
    assert p.cv_pp(4) == pytest.approx(13724.8830, abs=CENT)
    assert all(p.charge_acq_spread_pp(k) == pytest.approx(1275.00 / 5, abs=CENT)
               for k in range(5))
    assert p.charge_acq_spread_pp(5) == 0.0
    assert p.spread_diff_pp_at(1, "AFT_INT") == pytest.approx(
        (p.spread_diff_pp(1) + p.charge_acq_pp(1) - p.charge_acq_spread_pp(1)) * 1.01,
        rel=1e-12) == pytest.approx(782.952, abs=CENT)
    assert p.spread_diff_pp_at(16, "AFT_INT") > 0.0       # it never returns to zero
    # Omitting the floor would cut the second year's surrender claim by the whole of the gap.
    lapses_year_1 = sum(p.pols_lapse(t) for t in range(12, 24))
    without_floor = p.cv_tariff_pp(1) * lapses_year_1
    assert p.result_cf_annual().loc[2, "claims_lapse"] - without_floor == pytest.approx(
        (p.cv_floor_pp(1) - p.cv_tariff_pp(1)) * lapses_year_1, rel=1e-9)
    assert p.check_cv_floor() is True


# --- Pitfall 8: letting the Stornoabzug recover acquisition costs
def test_pitfall_8_the_stornoabzug_cannot_recover_acquisition_costs(de_rv_anchor, tmp_path):
    """A flat percentage of the pre-deduction value with no duration term, and never below the
    floor however large it is set: a deduction unwinding over the first years would be exactly
    the kind Sec. 169(5) VVG voids."""
    import pandas as pd

    p = de_rv_anchor

    def gross(t):
        return p.av_pp_at(t, "AFT_INT") + p.av_sur_pp_at(t, "AFT_INT")

    for t in (0, 4, 11, 16):
        assert p.surr_charge_pp(t) == pytest.approx(0.020 * gross(t), rel=1e-12)
        assert p.cv_tariff_pp(t) == pytest.approx(gross(t) * 0.98, rel=1e-12)
    # Flat in t: the ratio to the pre-deduction value carries no duration term anywhere.
    assert {round(p.surr_charge_pp(t) / gross(t), 12) for t in range(1, 17)} == {0.02}

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv")
    is_25 = charges["charge_id"] == "zillmer_25"
    charges.loc[is_25 & (charges["item"] == "stornoabzug_rate"), "value"] = 0.50
    alt = tmp_path / "charge_table_storno.csv"
    charges.to_csv(alt, index=False)

    with model_reading("charge_file", alt, "RV_DE_S_storno") as model:
        q = model.Projection[1]
        assert q.cv_tariff_pp(9) < q.cv_floor_pp(9)
        assert all(q.cv_pp(t) == pytest.approx(q.cv_floor_pp(t), rel=1e-12)
                   for t in range(17))
        assert q.check_cv_floor() is True


# --- Pitfall 9: using one mortality basis where the product uses two
def test_pitfall_9_the_product_uses_two_mortality_bases(de_rv_anchor):
    """First order fixes the risk charge and the guarantees; second order drives the projection.

    ``mort_be_factor`` is **above one** on purpose: for an annuity, prudence is lower mortality.
    The library's two speeds sit beside the two bases and are not the same distinction: the
    unsuffixed rates are **annual**, the ``_mth`` ones the geometric twelfths the recursion
    applies, and twelve of each compound back to the year.
    """
    p = de_rv_anchor
    assert p.mort_be_factor() == 1.15 > 1.0
    assert all(p.mort_rate(t) == pytest.approx(min(1.0, p.mort_rate_guar(t) * 1.15), rel=1e-12)
               and p.mort_rate(t) > p.mort_rate_guar(t) for t in (0, 84, 192, 468))
    for k in (0, 8, 16):
        assert p.charge_risk_pp(k) == pytest.approx(
            p.mort_rate_guar(12 * k) * p.nar_pp(k), rel=1e-12)    # first order, annual
        assert p.charge_risk_pp(k) != pytest.approx(
            p.mort_rate(12 * k) * p.nar_pp(k), rel=1e-6)
    for t in (0, 96, 192):
        assert p.pols_death(t) == pytest.approx(
            p.pols_if(t) * p.mort_rate_mth(t), rel=1e-12)         # second order, monthly
        assert 1.0 - (1.0 - p.mort_rate_mth(t)) ** 12 == pytest.approx(
            p.mort_rate(t), rel=1e-14)                            # geometric, never q / 12
        assert p.mort_rate_mth(t) > p.mort_rate(t) / 12.0
    assert p.claims(0, "DEATH") / (
        3000.00 * p.pols_if(0) * p.mort_rate_guar(0) * p.mort_rate_mth(0)
        / p.mort_rate(0)) == pytest.approx(1.15, rel=1e-9)
    assert p.omega_age() == 121 and p.age(852 - 12) == 120
    assert p.mort_rate_guar(840) == p.mort_rate(840) == 1.0       # capped at the terminal age
    # A certainty is not twelfth-rooted: the table's closure convention puts the whole of it in
    # the year's anniversary month, so the survivors are paid their last full year of annuity.
    assert [t for t in range(840, 852) if p.mort_rate_mth(t) == 1.0] == [851]
    assert all(p.mort_rate_mth(t) == 0.0 for t in range(840, 851))


# --- Pitfall 10: using a period mortality table
def test_pitfall_10_the_mortality_surface_is_generational_not_period(de_rv_anchor):
    """``mort_rate_guar`` depends on ``calendar_year(t)`` as well as ``age(t)``.

    The anchor's annuitant reaches 67 in 2043, so the rate is strictly below the same age's
    rate for a life reaching 67 in 2026, by the seventeen further improvement years.
    """
    p = de_rv_anchor
    assert p.age(204) == 67 and p.calendar_year(204) == 2043
    assert p.age_y(17) == 67 and p.calendar_year_y(17) == 2043
    # Both step on the anniversary, not monthly: the table publishes no monthly rate.
    assert p.age(204) == p.age(215) and p.calendar_year(204) == p.calendar_year(215)
    q_base, improve = p.mort_rate_at_age(67), p.improve_rate(67)
    at_2043, at_2026 = p.mort_rate_guar(204), q_base * (1 - improve) ** (2026 - 2005)
    assert at_2043 == pytest.approx(q_base * (1 - improve) ** (2043 - 2005), rel=1e-12)
    assert at_2043 < at_2026
    assert at_2043 / at_2026 == pytest.approx((1 - improve) ** 17, rel=1e-12)
    assert at_2043 == pytest.approx(0.00521377, abs=5e-9)
    assert p.mort_rate_at_age(50) == 0.002000            # the anchor a substitute must keep
    assert p.mort_rate_at_age(51) / p.mort_rate_at_age(50) == pytest.approx(1.09, rel=1e-6)
    assert p.mort_rate_guar(0) < p.mort_rate_at_age(50)
    assert p.mort_rate_guar(468) < p.mort_rate_at_age(p.age(468))


# --- Pitfall 11: charging the risk premium on a zero net amount at risk
def test_pitfall_11_no_risk_premium_on_a_zero_net_amount_at_risk(
        klassische_rentenversicherung, de_rv_anchor):
    """With ``death_benefit_form = deckungskapital`` the benefit **is** the reserve.

    On the anchor the amount at risk **rises** to 4 587,95 EUR at ``t = 5`` and ends the
    deferment at 3 204,24 EUR rather than at zero, because the *Deckungskapital* never
    overtakes the premiums paid: *Beitragsrückgewähr* is real cover here, not a formality.
    """
    p = de_rv_anchor
    assert p.model_point()["death_benefit_form"] == "prem_refund"
    assert all(p.charge_risk_pp(t) > 0.0 for t in range(17))
    assert p.nar_pp(5) == pytest.approx(4587.95, abs=CENT) == max(
        p.nar_pp(t) for t in range(17))
    assert p.nar_pp(16) == pytest.approx(3204.24, abs=CENT) and p.nar_pp(16) > 0.0
    assert p.charge_risk_pp(0) == pytest.approx(4.37, abs=CENT)
    assert p.charge_risk_pp(16) == pytest.approx(15.39, abs=CENT)
    assert all(p.charge_risk_pp(t + 1) > p.charge_risk_pp(t) for t in range(16))
    assert p.db_base_pp(1) == pytest.approx(6000.00, abs=CENT)     # the premiums paid
    for point_id, last in ((2, 12), (12, 22)):
        q = klassische_rentenversicherung.Projection[point_id]
        assert q.model_point()["death_benefit_form"] == "deckungskapital"
        assert all(q.nar_pp(t) == 0.0 and q.charge_risk_pp(t) == 0.0
                   and q.db_base_pp(t) == q.av_pp(t) for t in range(last))
    assert all(p.charge_risk_pp(t) == 0.0 for t in (17, 29, 70))   # none after Rentenbeginn


# --- Pitfall 12: deducting the payout-phase administration charge from the annuity
def test_pitfall_12_the_payout_administration_charge_is_not_deducted(de_rv_anchor):
    """``annuity_admin_rate`` ships at 1,5 % and is never applied: the *Rentenfaktor* already
    carries the tariff's payout loading, so deducting again would charge it twice.

    Payout-phase ``expenses`` are a twelfth of the inflated ``expense_annuity_pp`` on the
    exposed count plus the settlement cost of that month's deaths, and nothing else.
    """
    import pandas as pd

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv")
    recorded = charges[(charges["charge_id"] == "zillmer_25")
                       & (charges["item"] == "annuity_admin_rate")]
    assert float(recorded["value"].iloc[0]) == 0.015
    assert "NOT applied" in recorded["provenance"].iloc[0]

    p = de_rv_anchor
    for t in (204, 312, 324, 468):
        assert p.annuity_payments(t) == pytest.approx(     # no 0,985 anywhere in it
            (p.annuity_guar_mth_pp() + p.annuity_sur_mth_pp(p.duration(t)))
            * p.pols_annuity(t), rel=1e-12)
        assert p.expenses(t) == pytest.approx(
            p.expenses_pp(t) * p.pols_annuity(t) + 120.0 * p.pols_death(t), rel=1e-12)
    assert p.expenses_pp(204) == pytest.approx(30.0 / 12.0 * 1.02 ** 17, rel=1e-12)
    # The konstant system: the Ueberschussrente is level at 12 % of the garantierte Rente,
    # and it steps on the anniversary rather than monthly, because it is redeclared annually.
    assert p.model_point()["payout_system"] == "konstant"
    assert p.annuity_sur_mth_pp(17) == pytest.approx(0.12 * p.annuity_guar_mth_pp(), rel=1e-12)
    assert all(p.annuity_sur_mth_pp(k) == pytest.approx(p.annuity_sur_mth_pp(17), rel=1e-12)
               for k in (26, 39, 59))
    assert p.annuity_pp(204) == p.annuity_pp(215)         # flat across the payout year


# --- Pitfall 13: paying a death benefit after the Rentenbeginn
def test_pitfall_13_no_death_benefit_after_the_rentenbeginn(klassische_rentenversicherung):
    """*Beitragsrückgewähr in der Rentenbezugsphase* was established by no source, so it is not
    asserted: ``claims_death(t) = 0`` for every ``t >= 12n``, on every model point.  Deaths still
    happen there and carry a settlement expense; they simply pay nothing."""
    for point_id in (1, 2, 3, 5, 6, 12, 13, 14):
        p = klassische_rentenversicherung.Projection[point_id]
        n = 12 * int(p.model_point()["aufschub_y"])
        assert p.result_cf().loc[n:, "claims_death"].sum() == 0.0, point_id
        assert all(p.db_pp(k) == 0.0
                   for k in (p.duration(n), p.duration(n) + 4)), point_id
        assert p.pols_death(n) > 0.0, point_id          # the decrement is real
        assert p.pols_if(n + 1) < p.pols_if(n), point_id
    names = set(klassische_rentenversicherung.Projection.cells) | set(
        klassische_rentenversicherung.Projection.refs)
    assert not names & {"db_annuity_pp", "prem_refund_annuity_pp", "claims_survivor",
                        "pols_survivor", "hinterbliebenenrente_pp"}


# --- Pitfall 14: letting the Kapitalwahlrecht leave the account behind
def test_pitfall_14_the_kapitalwahlrecht_leaves_no_account_behind(
        klassische_rentenversicherung, de_rv_anchor):
    """Commuters receive ``capital_conv_pp``, the same capital the annuitants convert."""
    p = de_rv_anchor
    n = 12 * 17                        # the Rentenbeginn falls at the end of month n - 1
    assert float(p.model_point()["kapitalwahl_rate"]) == 0.30
    assert p.claims(n - 1, "COMMUTATION") == pytest.approx(
        p.capital_conv_pp() * 0.30 * p.pols_surv_rb(), rel=1e-12)
    assert p.result_cf()["claims_commutation"].sum() == pytest.approx(
        p.claims(n - 1, "COMMUTATION"), rel=1e-12)      # that month and no other
    assert p.pols_commutation(n - 1) + p.pols_annuitization(n - 1) == pytest.approx(
        p.pols_surv_rb(), rel=1e-12)
    assert all(p.av_pp(k) == 0.0 and p.av_sur_pp(k) == 0.0 for k in (17, 29, 70))
    # Point 9 commutes the whole surviving cohort: nothing survives the Rentenbeginn.
    full = klassische_rentenversicherung.Projection[9]
    n9 = 12 * int(full.model_point()["aufschub_y"])
    assert float(full.model_point()["kapitalwahl_rate"]) == 1.0
    assert full.pols_annuitization(n9 - 1) == 0.0
    assert full.pols_commutation(n9 - 1) == pytest.approx(full.pols_surv_rb(), rel=1e-12)
    assert full.claims(n9 - 1, "COMMUTATION") == pytest.approx(30882.0276, abs=CENT)
    assert full.capital_conv_pp() == pytest.approx(43630.1733, abs=CENT)
    assert full.pols_if(n9) == 0.0 and full.check_decrement_closure() is True
    assert full.result_cf().loc[n9:].abs().sum().sum() == 0.0


# --- Pitfall 15: forgetting that the guarantee vintage is a model-point attribute
def test_pitfall_15_the_guarantee_vintage_is_a_model_point_attribute(
        klassische_rentenversicherung, tmp_path):
    """Three vintages credit three rates in one run, from the same tables.

    A single global rate makes a **misallocation between the two accounts** rather than a hole
    in the total: point 6's *Deckungskapital* at *Rentenbeginn* falls 7,7 % while its
    *Ansammlungsguthaben* rises 156 % and the conversion capital moves 0,8 %.
    """
    import pandas as pd

    rates = {point_id: klassische_rentenversicherung.Projection[point_id].int_rate_guar()
             for point_id in (1, 6, 14)}
    assert rates == {1: 0.0100, 6: 0.0275, 14: 0.0090}
    legacy = klassische_rentenversicherung.Projection[6]
    for name, value in (("av_own", legacy.av_pp_at(24, "AFT_INT")),
                        ("sur_own", legacy.av_sur_pp_at(24, "AFT_INT")),
                        ("conv_own", legacy.capital_conv_pp())):
        assert value == pytest.approx(LEGACY_VINTAGE_PROBE[name], abs=CENT), name

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    points.loc[6, "int_rate_guar"] = 0.0100
    alt = tmp_path / "model_point_table_one_rate.csv"
    points.to_csv(alt)

    with model_reading("model_point_file", alt, "RV_DE_S_one_rate") as model:
        q = model.Projection[6]
        assert q.int_rate_guar() == 0.0100
        for name, value in (("av_global", q.av_pp_at(24, "AFT_INT")),
                            ("sur_global", q.av_sur_pp_at(24, "AFT_INT")),
                            ("conv_global", q.capital_conv_pp())):
            assert value == pytest.approx(LEGACY_VINTAGE_PROBE[name], abs=CENT), name
        assert q.av_pp_at(24, "AFT_INT") / legacy.av_pp_at(24, "AFT_INT") - 1 == (
            pytest.approx(-0.077, abs=0.001))
        assert q.av_sur_pp_at(24, "AFT_INT") / legacy.av_sur_pp_at(24, "AFT_INT") - 1 == (
            pytest.approx(1.560, abs=0.005))
        assert q.bonus_rate(20) == pytest.approx(0.0155, abs=1e-12)   # and now it is positive


# --- Pitfall 16: letting sex reach the tariff
def test_pitfall_16_sex_never_reaches_the_tariff(klassische_rentenversicherung, tmp_path):
    """Unisex has been compulsory since 21 December 2012: ``sex`` reaches the mortality basis
    and nothing else.  The probe is the anchor cell as a woman, so the premium, the charges
    other than the *Risikobeitrag*, and the applied *Rentenfaktor* must all be identical."""
    import pandas as pd

    data = klassische_rentenversicherung.Data
    assert list(data.mort_table().index.names) == ["sex", "age"]
    for table in (data.rentenfaktor_table(), data.charge_table(), data.decl_rate_table(),
                  data.lapse_table(), data.freq_load_table()):
        assert "sex" not in (table.index.names or []) and "sex" not in table.columns

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    twin = points.loc[1].copy()
    twin["sex"], twin["policy_id"] = "F", "DE-RV-0001F"
    points.loc[99] = twin
    alt = tmp_path / "model_point_table_unisex.csv"
    points.to_csv(alt)

    with model_reading("model_point_file", alt, "RV_DE_S_unisex") as model:
        male, female = model.Projection[1], model.Projection[99]
        assert male.model_point()["sex"] == "M" and female.model_point()["sex"] == "F"
        assert female.prem_pp(0) == male.prem_pp(0) == 3000.00
        assert female.annuity_rate_appl() == male.annuity_rate_appl() == 32.00
        for name in ("freq_load", "beitragssumme_pp", "alpha_total_pp",
                     "annuity_rate_guar", "annuity_rate_curr"):
            assert getattr(female, name)() == getattr(male, name)(), name
        for name in ("charge_prem_pp", "charge_acq_pp", "lapse_rate", "decl_rate"):
            assert getattr(female, name)(0) == getattr(male, name)(0), name
        # The one place sex is allowed to reach: the mortality basis, hence the Risikobeitrag.
        assert female.mort_rate_guar(0) / male.mort_rate_guar(0) == pytest.approx(
            0.001300 / 0.002000, rel=1e-9)
        assert female.charge_risk_pp(0) < male.charge_risk_pp(0)
        assert female.capital_conv_pp() > male.capital_conv_pp()


# --- Pitfall 17: amortising against a shrunken Beitragssumme
def test_pitfall_17_the_beitragssumme_survives_a_beitragsfreistellung(
        klassische_rentenversicherung, de_rv_anchor):
    """The Sec. 4 DeckRV base is the premiums payable **as written**, not what is left:
    ``beitragssumme_pp`` sums ``prem_pp_sched``, which ignores ``pup_year``."""
    p = klassische_rentenversicherung.Projection[7]
    assert int(p.model_point()["pup_year"]) == 10
    assert p.beitragssumme_pp() == pytest.approx(22 * 3600.00, abs=CENT)
    assert p.alpha_total_pp() == pytest.approx(0.025 * 79200.00, abs=CENT)
    assert p.prem_pp_sched(9) == pytest.approx(3600.00, abs=CENT)    # as written
    assert p.prem_pp(9) == 0.0                                       # as charged
    assert p.beitragssumme_pp() > sum(p.prem_pp(t) for t in range(22))
    assert all(p.alpha_cum_pp(t) <= p.alpha_total_pp() + 1e-9 for t in (0, 4, 9, 21))
    assert p.alpha_cum_pp(1) == pytest.approx(p.alpha_total_pp(), rel=1e-12)
    # The Dynamik grows the base rather than shrinking it: point 12 at 5 % a year.
    dyn = klassische_rentenversicherung.Projection[12]
    assert float(dyn.model_point()["dynamik_rate"]) == 0.05
    assert dyn.prem_pp(1) == pytest.approx(1500.00 * 1.05, abs=CENT)
    assert dyn.beitragssumme_pp() == pytest.approx(
        sum(1500.00 * 1.05 ** t for t in range(22)), abs=CENT)
    assert dyn.beitragssumme_pp() == pytest.approx(57757.82, abs=CENT)
    assert dyn.alpha_total_pp() == pytest.approx(0.025 * 57757.82, abs=CENT)
    assert de_rv_anchor.beitragssumme_pp() == pytest.approx(51000.00, abs=CENT)


# --- Pitfall 18: truncating the payout phase
def test_pitfall_18_the_payout_phase_is_not_truncated(de_rv_anchor):
    """``proj_len_y() = omega_age - issue_age``, and the frame ends there with no survivors: a
    40-year horizon would strand 0,219599 of a policy at attained age 90 and drop 5 491,22 EUR
    of annuity payments, 23,8 % of the payout phase."""
    p = de_rv_anchor
    df = p.result_cf()
    assert p.proj_len_y() == 121 - 50 == 71
    assert p.proj_len() == 12 * 71 == 852
    assert list(df.index) == list(range(852)) and df.index.name == "t"
    assert df.index[-1] == p.proj_len() - 1
    assert p.pols_if(852) == 0.0 and p.pols_if(840) > 0.0
    assert p.check_decrement_closure() is True
    assert p.pols_if(480) == pytest.approx(0.219599, abs=SIX_DP) and p.age(480) == 90
    dropped = df.loc[480:, "annuity_payments"].sum()
    assert dropped == pytest.approx(5491.22, abs=CENT)
    assert dropped / df["annuity_payments"].sum() == pytest.approx(0.238, abs=0.0005)
    assert p.pols_if(840) < SIX_DP and abs(p.net_cf(851)) < CENT


# --- The published identities
def test_every_check_identity_holds_on_the_anchor(de_rv_anchor):
    """All nine ``check_*`` cells return True, and their residuals are zero at every t."""
    p = de_rv_anchor
    for name in CHECKS:
        assert getattr(p, name)() is True, name
    # The residual's argument follows its cells' clock: months for the five monthly identities
    # and the scalar conversion check, policy **years** for the four annual ones.
    monthly = ("check_net_cf", "check_pols_roll_fwd", "check_decrement_closure",
               "check_annuity_conv", "check_annuity_guarantee")
    annual = ("check_av_roll_fwd", "check_av_sur_roll_fwd", "check_prem_split",
              "check_cv_floor")
    assert set(monthly) | set(annual) == set(CHECKS)
    tol = {"check_net_cf": 1e-9, "check_pols_roll_fwd": 1e-12,
           "check_decrement_closure": 1e-12, "check_annuity_conv": 1e-6,
           "check_annuity_guarantee": 1e-12, "check_av_roll_fwd": 1e-8,
           "check_av_sur_roll_fwd": 1e-8, "check_prem_split": 1e-9, "check_cv_floor": 1e-9}
    for t in (0, 1, 7, 143, 203, 204, 312, 468, 851):
        for name in monthly:
            resid = getattr(p, name + "_resid")(t)
            assert resid == pytest.approx(0.0, abs=tol[name]), f"{name} at t = {t}"
    for k in (0, 1, 4, 11, 16, 17, 26, 39, 70):
        for name in annual:
            resid = getattr(p, name + "_resid")(k)
            assert resid == pytest.approx(0.0, abs=tol[name]), f"{name} at k = {k}"


def test_check_net_cf_rebuilds_the_headline_from_the_published_columns(de_rv_anchor):
    """delib's first ruling, rebuilt from the frame: ``net_cf = premiums - claims_death -
    claims_lapse - claims_commutation - annuity_payments - expenses``, with
    ``liability_cf = -net_cf`` exactly.  The account movements beside them are internal and
    are reported, not summed."""
    df = de_rv_anchor.result_cf()
    rebuilt = (df["premiums"] - df["claims_death"] - df["claims_lapse"]
               - df["claims_commutation"] - df["annuity_payments"] - df["expenses"])
    assert (rebuilt - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert de_rv_anchor.check_net_cf() is True
    # The account movements are annual and live in result_pols(), not in the cash flow
    # statement: a statement whose columns do not all sum to its bottom line is one a reader
    # has to know which columns to skip.
    state = de_rv_anchor.result_pols()
    assert not {"av", "av_sur", "prem_to_av", "int_credited", "bonus_credited"} & set(
        df.columns)
    assert state["prem_to_av"].sum() == pytest.approx(32671.5572, abs=CENT)
    assert state["int_credited"].sum() == pytest.approx(2695.8201, abs=CENT)
    assert state["bonus_credited"].sum() == pytest.approx(4737.8262, abs=CENT)
    internal = (state["prem_to_av"].sum() + state["int_credited"].sum()
                + state["bonus_credited"].sum())
    assert internal > abs(df["net_cf"].sum())


@pytest.mark.parametrize("point_id", [2, 6, 7, 8, 9, 13])
def test_the_check_identities_hold_where_an_option_is_switched_on(
        klassische_rentenversicherung, point_id):
    """The six model points that exercise an option, each closing all nine identities: the
    *Einmalbeitrag*, the legacy vintage, the *Beitragsfreistellung* conversion and its Sec. 165
    cash-out branch, full commutation, and the guaranteed factor with the value floor."""
    p = klassische_rentenversicherung.Projection[point_id]
    for name in CHECKS:
        assert getattr(p, name)() is True, f"{point_id}: {name}"
    df = p.result_cf()
    assert df.index[-1] == p.proj_len() - 1
    assert not df.isna().any().any()
    assert (df["pols_if"] >= -1e-12).all()


# --- Structure, documentation and inputs
def test_result_cf_shape_and_both_signs_of_the_net_flow(de_rv_anchor):
    """The ten published cash flow columns, and the three frames the model publishes.

    The monthly statement carries the six flows that cross the contract boundary and the two
    counts that weight them; the annual view regroups it; the annual **state** -- both
    accounts and the year's credits -- is :func:`result_pols`.
    """
    p = de_rv_anchor
    df = p.result_cf()
    assert list(df.columns) == [
        "pols_if", "pols_annuity", "premiums", "claims_death", "claims_lapse",
        "claims_commutation", "annuity_payments", "expenses", "liability_cf", "net_cf",
    ]
    assert df["pols_if"].iloc[0] == p.pols_if_init()
    # A cash flow statement must not publish its own subtotal beside its parts, and the
    # retired column names must not come back.
    assert not set(df.columns) & {"claims", "claims_surr", "claims_wd", "claims_commute"}
    state = p.result_pols()
    assert state.index.name == "policy_year" and list(state.index) == list(range(1, 72))
    assert {"av", "av_sur", "prem_to_av", "int_credited", "bonus_credited"} <= set(
        state.columns)
    ann = p.result_cf_annual()
    assert ann.index.name == "policy_year" and list(ann.columns) == list(df.columns)
    # The first month of each accumulation year collects the whole Versicherungsperiode's
    # premium and is strongly positive; the other eleven are mildly negative.
    assert df.loc[0, "net_cf"] > 0 and (df.loc[1:11, "net_cf"] < 0).all()
    assert (ann.loc[1:16, "net_cf"] > 0).all()
    assert ann.loc[17, "net_cf"] == pytest.approx(-8148.61, abs=CENT)
    assert (ann.loc[18:70, "net_cf"] < 0).all()


def test_invalid_enum_values_raise(de_rv_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_rv_anchor.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        de_rv_anchor.pols_if_at(0, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        de_rv_anchor.av_pp_at(0, "AFT_LAPSE")
    with pytest.raises(FormulaError):
        de_rv_anchor.av_sur_pp_at(0, "BEF_INT")


def test_docstrings_describe_the_current_structure(klassische_rentenversicherung):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = flat(klassische_rentenversicherung.doc)
    assert "mechanics demonstration" in doc
    assert "external" in doc                      # inputs are not stored in the model
    assert "once per model" in doc                # why Data exists
    assert "Rentenfaktor" in doc and "Rentengarantiezeit" in doc and "Deckungskapital" in doc
    proj = flat(klassische_rentenversicherung.Projection.doc)
    assert "Notes symbol" in proj
    data = flat(klassische_rentenversicherung.Data.doc)
    assert "TradLife_A" in data and "provenance" in data
    for cells in ("proj_len", "model_point", "av_pp_at", "pols_annuity", "bonus_rate",
                  "int_rate_guar", "annuity_rate_appl", "cv_floor_pp"):
        assert cells in proj, cells
    # The two clocks, said once in the Space docstring so a reader knows which argument is which.
    for phrase in ("Two clocks", "policy month", "policy year", "mort_rate_mth",
                   "lapse_rate_mth", "result_cf_annual", "Versicherungsperiode"):
        assert phrase in proj, phrase
    for cells in ("input_dir", "model_point_table", "mort_table", "rentenfaktor_table"):
        assert cells in data, cells


def test_the_annuity_chassis_vocabulary_is_present(klassische_rentenversicherung):
    """Names the sister German models on this chassis share must mean the same thing here."""
    shared = {"model_point", "proj_len", "proj_len_y", "t_start", "k_start", "duration",
              "duration_mth", "is_anniv", "policy_year", "age", "age_y", "calendar_year",
              "calendar_year_y", "pols_if", "pols_if_at",
              "pols_if_init", "pols_death", "pols_lapse", "mort_rate", "mort_rate_guar",
              "mort_rate_mth", "lapse_rate", "lapse_rate_mth", "prem_due",
              "prem_pp", "premiums", "prem_to_av_pp", "prem_to_av", "av_pp",
              "av_pp_at", "av", "av_at", "av_sur_pp", "av_sur", "cv_pp", "claims",
              "expenses", "net_cf", "liability_cf", "result_cf", "result_cf_annual",
              "result_pols", "check_net_cf", "check_net_cf_resid"}
    names = set(klassische_rentenversicherung.Projection.cells) | set(
        klassische_rentenversicherung.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    # The two-speed pair the library requires wherever a grid is monthly: the annual rate the
    # notes tabulate, and the geometric twelfth derived from it.  Both compound back to the
    # year; neither is the annual rate divided by twelve.
    proj = klassische_rentenversicherung.Projection[1]
    for t in (0, 96, 468):
        assert proj.mort_rate_mth(t) < proj.mort_rate(t)
        assert 1.0 - (1.0 - proj.mort_rate_mth(t)) ** 12 == pytest.approx(
            proj.mort_rate(t), rel=1e-14)
        assert proj.mort_rate_mth(t) > proj.mort_rate(t) / 12.0
    for t in (0, 96):          # the accumulation phase; there is no surrender in payment
        assert proj.lapse_rate_mth(t) < proj.lapse_rate(t)
        assert 1.0 - (1.0 - proj.lapse_rate_mth(t)) ** 12 == pytest.approx(
            proj.lapse_rate(t), rel=1e-14)
        assert proj.lapse_rate_mth(t) > proj.lapse_rate(t) / 12.0
    assert proj.lapse_rate(468) == proj.lapse_rate_mth(468) == 0.0
    # The frame's two clocks are consistent: t_start is twelve times k_start, proj_len twelve
    # times proj_len_y, and duration/policy_year the bridge between them.
    assert proj.t_start() == 12 * proj.k_start()
    assert proj.proj_len() == 12 * proj.proj_len_y()
    for t in (0, 11, 12, 203, 204):
        assert proj.duration(t) == t // 12 == proj.duration_mth(t) // 12
        assert proj.policy_year(t) == proj.duration(t) + 1
        assert proj.is_anniv(t) == (t % 12 == 11)


def test_the_shipped_tables_mark_their_own_provenance():
    """Eight CSVs beside run.py, and every one but the model point table says where it came
    from.  The mortality table is a **[std]** proxy anchored at ``q_base(M, 50) = 0.002000``,
    the *Rentenfaktor* table at age 67, and the lapse table's one shaped feature is the
    duration-12 step."""
    import pandas as pd

    assert {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"} == CSV_FILES
    for name in CSV_FILES - {"model_point_table.csv"}:
        frame = pd.read_csv(INPUT_DIR / name)
        assert "provenance" in frame.columns, name
        assert (frame["provenance"].astype(str).str.len() > 0).all(), name
    assert "provenance" not in pd.read_csv(INPUT_DIR / "model_point_table.csv").columns
    mort = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col=["sex", "age"])
    assert [float(mort.loc[key, "q_base"]) for key in (
        ("M", 50), ("F", 50), ("M", 120))] == [0.002000, 0.001300, 1.0]
    assert float(mort.loc[("M", 51), "q_base"]) / float(mort.loc[("M", 50), "q_base"]) == (
        pytest.approx(1.09, rel=1e-6))
    assert float(mort.loc[("M", 55), "improve"]) == 0.015
    assert float(mort.loc[("M", 110), "improve"]) == 0.0
    assert all(p.startswith("[std]") for p in mort["provenance"])
    gompertz = mort[mort["provenance"].str.contains("Gompertz")]["provenance"]
    assert len(gompertz) == len(mort) - 2          # every row but the two age-120 closures
    assert all("DAV 2004 R is DAV property and is not redistributed" in p for p in gompertz)
    factors = pd.read_csv(INPUT_DIR / "rentenfaktor_table.csv",
                          index_col=["rf_scenario_id", "age"])
    assert set(factors.index.get_level_values(0)) == {"base", "low", "high"}
    assert [float(factors.loc[(scen, 67), "annuity_rate_curr"])
            for scen in ("base", "low", "high")] == [32.00, 25.50, 35.00]
    assert all("gap 3" in p for p in factors["provenance"])
    lapse = pd.read_csv(INPUT_DIR / "lapse_table.csv", index_col="duration")
    assert [float(lapse.loc[d, "lapse_rate"]) for d in (1, 11, 12, 13)] == [
        0.060, 0.035, 0.060, 0.030]                # the duration-12 step
    assert "EStG" in lapse.loc[12, "provenance"]
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col=["charge_id", "item"])
    assert [float(charges.loc[key, "value"]) for key in (
        ("zillmer_25", "alpha_rate"), ("zillmer_40", "alpha_rate"),
        ("zillmer_25", "alpha_spread_years"),
        ("zillmer_40", "stornoabzug_rate"))] == [0.025, 0.040, 5, 0.0]
    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert len(points) == 14 and points.loc[1, "policy_id"] == "DE-RV-0001"
    assert set(points["prem_freq"]) == {"annual", "half_yearly", "quarterly", "monthly"}
    assert set(points["death_benefit_form"]) == {"prem_refund", "deckungskapital", "max"}
    assert set(points["payout_system"]) == {"konstant", "teildynamisch", "volldynamisch"}
    assert sorted(set(points["int_rate_guar"])) == [0.0090, 0.0100, 0.0275]


def test_an_input_can_be_swapped_without_touching_formulas(de_rv_anchor, tmp_path):
    """This is what a production user does with a licensed or company generational table."""
    import pandas as pd

    lighter = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col=["sex", "age"])
    lighter["q_base"] = lighter["q_base"] * 0.5
    lighter.loc[(slice(None), 120), "q_base"] = 1.0
    alt = tmp_path / "mort_table_light.csv"
    lighter.to_csv(alt)

    base = de_rv_anchor.result_cf()
    with model_reading("mort_file", alt, "RV_DE_S_swap") as model:
        light = model.Projection[1].result_cf()
        # Lighter mortality: fewer death claims, more premium collected, a longer annuity.
        assert light["claims_death"].sum() < base["claims_death"].sum()
        assert light["premiums"].sum() > base["premiums"].sum()
        assert light["annuity_payments"].sum() > base["annuity_payments"].sum()
        assert model.Projection[1].check_decrement_closure() is True
        assert model.Projection[1].check_net_cf() is True
