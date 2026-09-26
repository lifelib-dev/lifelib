"""Golden and structural tests for Sofort_DE_S.

The golden values are the worked example in
``products/sofortrente/technical-notes.md`` ("Worked example"), which is a
**configuration** rather than a scenario: a *sofortbeginnende private
Rentenversicherung* bought with one *Einmalbeitrag* of 100 000,00 EUR by a man aged 65 at
*Vertragsbeginn* in 2025 and born in 1960; no *Aufschubzeit*, so the annuity begins at
once; a ten-year *Rentengarantiezeit*, so the first 120 monthly instalments are payable
whether the annuitant is alive or not; no *Kapitalrückgewähr* and no
*Hinterbliebenenrente*; monthly instalments *vorschüssig*, the first at ``t = 0``; a
tariff *Rechnungszins* of 1,00 %, the *Höchstrechnungszins* in force for 2025 business;
*Überschussverwendung* **teildynamisch**, so the *Überschussrente* opens at a tenth of the
*garantierte Rente* and steps up 1 % at each policy anniversary; the guaranteed annuity
**derived by equivalence** rather than given; and one policy in force from ``t = 0``.
``proj_len() = 672``, the frame's exclusive end, so the notes' table is a slice of a
672-month projection ``t = 0 ... 671`` rather than
the whole of it, and every row it prints is asserted here with the totals at full
precision.

Beyond the worked example it asserts: the derived quantities and the notes' three
independent rebuilds — the instalment from the printed annuity factor by one division,
month 1 from the two rows of ``mort_table.csv``, and month 0 from the parameter list; the
closure identities, including the *Rentengarantiezeit* computed in closed form with no
mortality table at all, against which the two opposite-signed errors it guards are 7,13 %
below and 92,87 % above; the three variants the notes print in full — the same cell
*nachschüssig*, the in-force cell carrying a **given** annuity, and the cell with the
*Überschussrente* switched off; all nine ``check_*`` identities, delib's mandatory
``check_net_cf`` and its residual among them; **one test per numbered modeling pitfall**,
eighteen of them; and the structural facts a reader relies on — the ``result_cf()`` column
vocabulary, both signs of the net flow, the docstrings and the shipped tables' provenance.

The whole-model-point-table sweep belongs to ``test_model_conventions_de.py``, which is
also where every ``check_*()`` is called on every point; this module does not repeat it.
"""
import math
import shutil

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if and the survival probabilities to 6 d.p.

MODEL_DIR = LIB / MODELS["Sofort_DE_S"][0]

INPUT_CSVS = {
    "model_point_table.csv", "mort_table.csv", "improvement_table.csv",
    "surplus_scale_table.csv", "hoechstrechnungszins_table.csv",
}


def alt_model(tmp_path, name, edits):
    """A private copy of the model whose model point table carries ``edits``.

    ``edits`` maps ``point_id`` to a dict of column overrides.  The model folder and its
    five CSVs are copied into ``tmp_path`` and the copy is read from there, so
    ``Data.input_dir()`` resolves to ``tmp_path`` and the shipped files are never touched.
    This is how the three pitfalls that need *the same cell with one attribute changed*
    are asserted: no such pair exists in the shipped table, and inventing one would put a
    model point in the library whose only purpose is a test.
    """
    import pandas as pd

    dest = tmp_path / MODEL_DIR.name
    if not dest.exists():
        shutil.copytree(MODEL_DIR, dest)
        for csv_path in MODEL_DIR.parent.glob("*.csv"):
            shutil.copy(csv_path, tmp_path / csv_path.name)
    table = pd.read_csv(tmp_path / "model_point_table.csv", index_col="point_id")
    for point_id, columns in edits.items():
        for column, value in columns.items():
            table.loc[point_id, column] = value
    table.to_csv(tmp_path / "model_point_table.csv")
    return mx.read_model(dest, name=name)


# The worked example's golden values, transcribed from technical-notes.md
# The four numbers everything else follows from, and the frame they live in.
DERIVED = {
    "net_single_prem": 97500.0000,
    "annuity_factor": 263.5711140230,
    "a12": 21.9642595019,          # annuity_factor() / payment_freq()
    "refund_pv": 0.0,
    "annuity_pp_derived": 362.6658241684,
    "annuity_surp_pp_0": 36.2665824168,
    "annuity_pp_0": 398.9324065852,
    "first_pay_mth": 0, "guar_end_mth": 120,
    "t_start": 0, "proj_len": 672, "rows": 672,
}

# t: (pols_if, premiums, annuity_payments, claims_guarantee, claims_refund,
#     expenses, liability_cf, net_cf) -- every row the notes' table prints.
WORKED_EXAMPLE = {
    0:   (1.000000, 100000.00, 398.93,  0.00, 0.00, 2206.50, -97394.57, 97394.57),
    1:   (1.000000,      0.00, 398.54,  0.40, 0.00,    6.50,    405.43,  -405.43),
    2:   (1.000000,      0.00, 398.14,  0.79, 0.00,    6.50,    405.43,  -405.43),
    3:   (1.000000,      0.00, 397.75,  1.19, 0.00,    6.50,    405.43,  -405.43),
    4:   (1.000000,      0.00, 397.35,  1.58, 0.00,    6.50,    405.43,  -405.43),
    5:   (1.000000,      0.00, 396.96,  1.97, 0.00,    6.50,    405.43,  -405.43),
    6:   (1.000000,      0.00, 396.57,  2.37, 0.00,    6.50,    405.43,  -405.43),
    7:   (1.000000,      0.00, 396.17,  2.76, 0.00,    6.50,    405.43,  -405.43),
    8:   (1.000000,      0.00, 395.78,  3.15, 0.00,    6.50,    405.43,  -405.43),
    9:   (1.000000,      0.00, 395.39,  3.54, 0.00,    6.50,    405.43,  -405.43),
    10:  (1.000000,      0.00, 395.00,  3.94, 0.00,    6.50,    405.43,  -405.43),
    11:  (1.000000,      0.00, 394.60,  4.33, 0.00,    6.50,    405.43,  -405.43),
    12:  (1.000000,      0.00, 394.57,  4.72, 0.00,    6.60,    405.89,  -405.89),
    60:  (1.000000,      0.00, 373.69, 27.09, 0.00,    7.00,    407.78,  -407.78),
    119: (1.000000,      0.00, 338.58, 63.75, 0.00,    7.43,    409.76,  -409.76),
    120: (0.839834,      0.00, 338.22,  0.00, 0.00,    6.34,    344.56,  -344.56),
    121: (0.837965,      0.00, 337.47,  0.00, 0.00,    6.32,    343.79,  -343.79),
    240: (0.555887,      0.00, 226.20,  0.00, 0.00,    4.87,    231.07,  -231.07),
    360: (0.189111,      0.00,  77.83,  0.00, 0.00,    1.92,     79.75,   -79.75),
    480: (0.007818,      0.00,   3.26,  0.00, 0.00,    0.09,      3.35,    -3.35),
    600: (0.000000,      0.00,   0.00,  0.00, 0.00,    0.00,      0.00,    -0.00),
    671: (0.000000,      0.00,   0.00,  0.00, 0.00,    0.00,      0.00,    -0.00),
}

# The notes' Total row: summed over all 672 rows at full precision, then rounded.
TOTALS = {
    "pols_if": 258.921518, "premiums": 100000.00, "annuity_payments": 101091.33,
    "claims_guarantee": 3428.03, "claims_refund": 0.00, "expenses": 4228.28,
    "liability_cf": 8747.64, "net_cf": -8747.64,
}

# What the same columns come to if the 672 *rounded* cells are added instead.  The notes
# state the divergence rather than hiding it, and this module asserts it exists.
ROUNDED_CELL_SUMS = {
    "annuity_payments": 101091.23, "claims_guarantee": 3428.04, "net_cf": -8747.47,
}

# t: (lives_if_1, certain_floor, payment_factor, annuity_guar_pp, annuity_surp_pp,
#     annuity_pp, cum_annuity_guar_pp) -- the notes' state table behind the cash flows.
STATE = {
    0:   (1.000000, 1.0, 1.000000, 362.67, 36.27, 398.93,    362.67),
    11:  (0.989151, 1.0, 1.000000, 362.67, 36.27, 398.93,   4351.99),
    12:  (0.988171, 1.0, 1.000000, 362.67, 36.63, 399.30,   4714.66),
    119: (0.841553, 1.0, 1.000000, 362.67, 39.66, 402.33,  43519.90),
    120: (0.839834, 0.0, 0.839834, 362.67, 40.06, 402.73,  43882.56),
    240: (0.555887, 0.0, 0.555887, 362.67, 44.25, 406.92,  87402.46),
    360: (0.189111, 0.0, 0.189111, 362.67, 48.88, 411.55, 130922.36),
    671: (0.000000, 0.0, 0.000000, 362.67, 62.69, 425.35, 243711.43),
}

# The notes' closed-form check on the Rentengarantiezeit, and the two errors it catches.
GUARANTEE = {
    "instalments_120R": 43519.8989002072, "s_due_10": 10.4622125411,
    "surplus_part": 4553.1443206206, "total": 48073.0432208278,
    "annuitant_leg_only": 44645.0162147316, "additive_floor": 92718.0594355593,
}

# Model point 9: the anchor cell nachschüssig, and nothing else changed.
ARREARS_DERIVED = {
    "annuity_factor": 262.6685503335, "annuity_pp_derived": 363.9119916441,
    "first_pay_mth": 1, "guar_end_mth": 121, "tariff_lives_120": 0.8923696956,
    "factor_gap": 0.9025636895, "certain_gain": 0.0974363105,
}

# t: (pols_if, premiums, annuity_payments, claims_guarantee, expenses, net_cf)
ARREARS = {
    0:   (1.000000, 100000.00,   0.00,  0.00, 2205.00, 97795.00),
    1:   (1.000000,      0.00, 399.91,  0.40,    6.50,  -406.80),
    2:   (1.000000,      0.00, 399.51,  0.79,    6.50,  -406.80),
    3:   (1.000000,      0.00, 399.11,  1.19,    6.50,  -406.80),
    12:  (1.000000,      0.00, 395.93,  4.74,    6.60,  -407.26),
    120: (1.000000,      0.00, 339.39, 64.72,    7.54,  -411.65),
    121: (0.837965,      0.00, 338.63,  0.00,    6.32,  -344.95),
    240: (0.555887,      0.00, 226.98,  0.00,    4.87,  -231.84),
}
ARREARS_TOTALS = {
    "pols_if": 259.081684, "premiums": 100000.00, "annuity_payments": 101038.39,
    "claims_guarantee": 3504.53, "expenses": 4227.99, "net_cf": -8770.91,
}

# Model point 10: an in-force cell carrying an annuity struck in 2012 at 1,75 %.
# t: (pols_if, premiums, annuity_payments, claims_guarantee, expenses, net_cf)
INFORCE = {
    156: (1.000000, 0.00, 516.00,  0.00, 7.89, -523.89),
    157: (1.000000, 0.00, 514.26,  1.74, 7.89, -523.89),
    168: (1.000000, 0.00, 495.50, 20.50, 8.01, -524.01),
    179: (1.000000, 0.00, 475.88, 40.12, 8.01, -524.01),
    180: (0.918857, 0.00, 474.13,  0.00, 7.47, -481.60),
    240: (0.689197, 0.00, 355.63,  0.00, 6.03, -361.66),
}
INFORCE_TOTALS = {
    "pols_if": 135.648915, "premiums": 0.00, "annuity_payments": 69516.79,
    "claims_guarantee": 478.05, "expenses": 1192.84, "net_cf": -71187.68,
}

# Model point 14: the anchor with surplus_form = none.
SURPLUS_OFF_TOTALS = {
    "annuity_payments": 90804.02, "claims_guarantee": 3097.97,
    "expenses": 4228.28, "net_cf": 1869.74,
}

# Model point 3: the Kapitalrückgewähr cell, where R is solved and not evaluated.
REFUND = {
    "annuity_factor": 258.2307278976, "annuity_pp_derived": 298.8347765669,
    "refund_pv": 18788.3116885525, "r_max_naive": 370.1659987267,
    "refund_pv_at_r_max": 13546.3741961946, "r_naive": 318.7361819732,
    "refund_pp_0": 99701.1652234331, "instalments_to_exhaust": 335,
}

# The two rows of mort_table.csv the notes rebuild month 1 from, and the anchor of the
# shipped [std] proxy: the 0,45 / 0,55 unisex blend reproduces q_base(65).
MORT = {
    "first_m_65": 0.009857796019, "first_f_65": 0.006273146506,
    "unisex_first_65": 0.007886238787, "q_base_65": 0.0078862368150,
    "second_m_65": 0.011829355222, "mort_rate_mth_0": 0.000991165035,
    "lives_if_1": 0.999008834965,
}


# The worked example
@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_sofort_anchor, t):
    """Every cell of every row the notes' table prints, to the displayed precision.

    672 rows is not a table anyone prints in full, so the notes show the first policy year
    in full and the first month of the second, where the *Überschussrente* steps, then the
    two months either side of the guarantee's expiry and one row every ten years; the
    totals below cover the 650 rows in between.
    """
    pols_if, prem, ann, guar, refund, exp, liab, net = WORKED_EXAMPLE[t]
    p = de_sofort_anchor
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.annuity_payments(t) == pytest.approx(ann, abs=CENT)
    assert p.claims(t, "GUARANTEE") == pytest.approx(guar, abs=CENT)
    assert p.claims(t, "REFUND") == pytest.approx(refund, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(liab, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    row = de_sofort_anchor.result_cf().loc[t]
    assert row["annuity_payments"] == pytest.approx(ann, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)


def test_the_worked_example_totals_are_summed_at_full_precision(de_sofort_anchor):
    """The Total row is a full-precision sum then rounded, not a sum of rounded cells.

    On this table the difference is visible: 672 half-cent roundings do not cancel, and
    ``net_cf`` comes to -8 747,47 EUR from the rounded cells against -8 747,64 EUR at full
    precision.  A test that summed the printed table would enshrine the wrong number.
    """
    df = de_sofort_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    for column, rounded in ROUNDED_CELL_SUMS.items():
        assert sum(round(v, 2) for v in df[column]) == pytest.approx(rounded, abs=CENT)
        assert abs(rounded - TOTALS[column]) > CENT, column
    # And the statement closes: premiums less the four outgo columns is net_cf.
    outgo = (df["annuity_payments"] + df["claims_guarantee"]
             + df["claims_refund"] + df["expenses"])
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    assert df["annuity_payments"].sum() == pytest.approx(101091.3334710770, abs=1e-6)
    assert df["claims_guarantee"].sum() == pytest.approx(3428.0270060962, abs=1e-6)
    assert df["expenses"].sum() == pytest.approx(4228.2772978315, abs=1e-6)
    assert df["net_cf"].sum() == pytest.approx(-8747.6377750047, abs=1e-6)


def test_the_derived_quantities(de_sofort_anchor):
    """The four numbers the example follows from, the frame, and the market's own unit:
    ``annuity_factor()`` is the notes' ``ä`` and **not** the market's ``a12``, which is it
    divided by the payment frequency."""
    p = de_sofort_anchor
    assert p.single_prem() == 100000.0
    assert p.net_single_prem() == pytest.approx(DERIVED["net_single_prem"], abs=CENT)
    assert p.net_single_prem() == pytest.approx(
        100000.0 * (1 - p.expense_load_alpha), rel=1e-12)
    assert p.annuity_factor() == pytest.approx(DERIVED["annuity_factor"], abs=5e-10)
    assert p.annuity_factor() / p.payment_freq() == pytest.approx(
        DERIVED["a12"], abs=5e-10)
    assert p.refund_pv() == DERIVED["refund_pv"]
    assert p.annuity_pp_derived() == pytest.approx(
        DERIVED["annuity_pp_derived"], abs=5e-10)
    assert p.annuity_surp_pp(0) == pytest.approx(DERIVED["annuity_surp_pp_0"], abs=5e-10)
    assert p.annuity_pp(0) == pytest.approx(DERIVED["annuity_pp_0"], abs=5e-10)
    assert p.first_pay_mth() == DERIVED["first_pay_mth"]
    assert p.guar_end_mth() == DERIVED["guar_end_mth"]
    assert p.max_tariff_int_rate() == 0.01 and p.tariff_int_rate() == 0.01
    # The frame: 672 rows, t = 0 ... 671, contiguous and indexed by t.
    df = p.result_cf()
    assert (p.t_start(), p.proj_len(), len(df)) == (
        DERIVED["t_start"], DERIVED["proj_len"], DERIVED["rows"])
    assert list(df.index) == list(range(0, 672)) and df.index.name == "t"
    assert df.index[-1] == p.proj_len() - 1
    assert len(df) == p.proj_len() - p.t_start()
    assert p.horizon_mths(1) == 12 * (p.omega_age - 65) == 672
    # The notes' first independent check: one division, from the printed factor.  The
    # model builds ä by summing 672 discounted survival-weighted payment months; a reader
    # does 97 500,00 / (263,5711140230 x 1,02).  The opening total instalment is then
    # R x 1,10, the 1,10 being 1 + u0 with the growth exponent still zero.
    r = DERIVED["net_single_prem"] / (DERIVED["annuity_factor"] * 1.02)
    assert r == pytest.approx(362.6658241684, abs=5e-9)
    assert p.annuity_pp_derived() == pytest.approx(r, abs=5e-9)
    assert 100000.0 * 0.975 / (12 * DERIVED["a12"] * 1.02) == pytest.approx(
        362.67, abs=CENT)
    assert DERIVED["annuity_factor"] * 1.02 == pytest.approx(268.8425363035, abs=5e-10)
    assert p.surplus_init_pct() == 0.10 and p.surplus_growth() == 0.01
    assert p.annuity_pp(0) == pytest.approx(p.annuity_pp_derived() * 1.10, rel=1e-12)


def test_month_one_rebuilt_from_the_mortality_table(de_sofort_anchor):
    """The notes' second independent check, and the shipped proxy's own anchor.

    The cohort exponent is zero at age 65 for a 1960 cohort, so the surface returns the
    shipped rate unmodified and the month-1 split follows arithmetically; and the unisex
    rate off the same two rows reproduces the research file's ``q_base(65)`` to
    2,5 x 10^-7 relative, which is what lets every annuity factor printed there be traced
    into this model.
    """
    p = de_sofort_anchor
    assert p.mort_rate_at_age(65, "M", "FIRST") == MORT["first_m_65"]
    assert p.mort_rate_at_age(65, "F", "FIRST") == MORT["first_f_65"]
    assert p.mort_rate_at_age(65, "M", "SECOND") == pytest.approx(
        1.20 * MORT["first_m_65"], rel=1e-12)
    assert p.mort_rate(0, 1) == pytest.approx(MORT["second_m_65"], rel=1e-12)
    assert p.mort_rate_mth(0, 1) == pytest.approx(MORT["mort_rate_mth_0"], abs=5e-13)
    assert (1 - p.mort_rate_mth(0, 1)) ** 12 == pytest.approx(
        1 - p.mort_rate(0, 1), rel=1e-12)
    assert p.lives_if(1, 1) == pytest.approx(MORT["lives_if_1"], abs=5e-13)
    assert p.annuity_payments(1) == pytest.approx(
        DERIVED["annuity_pp_0"] * MORT["lives_if_1"], abs=5e-9)
    assert p.claims(1, "GUARANTEE") == pytest.approx(
        DERIVED["annuity_pp_0"] * MORT["mort_rate_mth_0"], abs=5e-9)
    assert p.annuity_payments(1) + p.claims(1, "GUARANTEE") == pytest.approx(
        p.annuity_pp(1), abs=1e-9)
    blend = 0.45 * MORT["first_m_65"] + 0.55 * MORT["first_f_65"]
    assert blend == pytest.approx(MORT["unisex_first_65"], abs=5e-13)
    assert p.mort_rate_at_age(65, "U", "FIRST") == pytest.approx(blend, rel=1e-12)
    assert blend / MORT["q_base_65"] - 1 == pytest.approx(2.5e-7, rel=0.05)
    # The notes' third check: month 0, from the parameter list, with no survival in
    # either line -- and the *Kostenüberschuss* visible in them, 2 500,00 EUR of loading
    # against 2 200,00 EUR of acquisition expense incurred.
    assert p.expense_acq_rate == 0.02 and p.expense_acq_fixed == 200.0
    assert p.expense_maint_pp == 60.0 and p.expense_pay_pp == 1.50
    assert p.infl_factor(0) == 1.0
    assert p.expenses(0) == pytest.approx(2000.00 + 200.00 + 5.00 + 1.50, abs=1e-9)
    assert p.expenses(0) == pytest.approx(2206.50, abs=CENT)
    assert p.premiums(0) == 100000.0
    assert p.net_cf(0) == pytest.approx(100000.00 - 398.93 - 0.00 - 2206.50, abs=CENT)
    loading = p.expense_load_alpha * p.single_prem()
    incurred = p.expense_acq_rate * p.single_prem() + p.expense_acq_fixed
    assert loading - incurred == pytest.approx(300.00, abs=CENT)
    assert p.expenses(1) == pytest.approx(60.0 / 12 + 1.50, abs=1e-9)
    assert p.expenses(12) == pytest.approx((60.0 / 12 + 1.50) * 1.015, abs=1e-9)


@pytest.mark.parametrize("t", sorted(STATE))
def test_the_state_behind_the_cash_flows(de_sofort_anchor, t):
    """The notes' second table: survival, the certain floor and the split instalment."""
    lives, floor, factor, guar, surp, total, cum = STATE[t]
    p = de_sofort_anchor
    assert p.lives_if(t, 1) == pytest.approx(lives, abs=SIX_DP)
    assert p.certain_floor(t) == floor
    assert p.payment_factor(t) == pytest.approx(factor, abs=SIX_DP)
    assert p.annuity_guar_pp(t) == pytest.approx(guar, abs=CENT)
    assert p.annuity_surp_pp(t) == pytest.approx(surp, abs=CENT)
    assert p.annuity_pp(t) == pytest.approx(total, abs=CENT)
    assert p.cum_annuity_guar_pp(t) == pytest.approx(cum, abs=CENT)
    assert p.lives_if(t, 2) == 0.0          # no Hinterbliebenenrente on this cell
    assert p.refund_pp(t) == 0.0            # and no Kapitalrückgewähr


def test_the_decrements_close(de_sofort_anchor):
    """Death is the only decrement, so deaths plus survivors are the whole cohort.

    It closes to the last printed digit because ``q = 1`` at attained age 120 forces the
    survival path to zero inside the horizon -- eleven months inside it, which is why the
    horizon is an upper bound and not an equality.
    """
    p = de_sofort_anchor
    n = p.proj_len()
    deaths = sum(p.lives_death(t, 1) for t in range(0, n))
    assert deaths == pytest.approx(1.0, abs=1e-12)
    assert p.lives_if(n, 1) == 0.0
    assert deaths + p.lives_if(n, 1) == pytest.approx(p.lives_if(0, 1), abs=1e-12)
    assert p.check_lives_roll_fwd() is True
    zero_at = min(t for t in range(0, n + 1) if p.lives_if(t, 1) == 0.0)
    assert zero_at <= p.horizon_mths(1)
    assert p.mort_rate_at_age(120, "M", "SECOND") == 1.0


def test_the_guarantee_period_computed_in_closed_form(de_sofort_anchor):
    """The notes' third check, and the one worth having: no mortality table at all.

    Inside the *Rentengarantiezeit* the outgo does not depend on survival, so the first ten
    years follow from ``R``, ``u0``, ``psi`` and an annuity-certain-due alone, and the two
    errors it closes off are large and point in opposite directions.
    """
    p = de_sofort_anchor
    r = p.annuity_pp_derived()
    s_due = (1.01 ** 10 - 1) / 0.01
    assert s_due == pytest.approx(GUARANTEE["s_due_10"], abs=5e-11)
    guaranteed = 120 * r
    surplus = 12 * r * p.surplus_init_pct() * s_due
    assert guaranteed == pytest.approx(GUARANTEE["instalments_120R"], abs=5e-9)
    assert surplus == pytest.approx(GUARANTEE["surplus_part"], abs=5e-9)
    assert guaranteed + surplus == pytest.approx(GUARANTEE["total"], abs=5e-9)

    paid = sum(p.annuity_payments(t) + p.claims(t, "GUARANTEE") for t in range(0, 120))
    assert paid == pytest.approx(GUARANTEE["total"], abs=1e-8)
    annuitant_only = sum(p.annuity_payments(t) for t in range(0, 120))
    assert annuitant_only == pytest.approx(GUARANTEE["annuitant_leg_only"], abs=CENT)
    assert annuitant_only / paid - 1 == pytest.approx(-0.0713, abs=5e-5)
    additive = sum(p.pols_if_init() * p.annuity_pp(t)
                   * (p.certain_floor(t) + p.lives_if(t, 1)) for t in range(0, 120))
    assert additive == pytest.approx(GUARANTEE["additive_floor"], abs=CENT)
    assert additive / paid - 1 == pytest.approx(0.9287, abs=5e-5)


# The three variants the notes print
@pytest.mark.parametrize("t", sorted(ARREARS))
def test_the_nachschuessig_variant_row(sofortrente, t):
    """Model point 9 is model point 1 with payment_timing = arrears, nothing else."""
    pols_if, prem, ann, guar, exp, net = ARREARS[t]
    p = sofortrente.Projection[9]
    assert p.payment_timing() == "arrears"
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.annuity_payments(t) == pytest.approx(ann, abs=CENT)
    assert p.claims(t, "GUARANTEE") == pytest.approx(guar, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_nachschuessig_factor_gap_is_checkable_in_one_line(
        sofortrente, de_sofort_anchor):
    """263,5711 - 262,6686 = 0,9026, and that difference has two named halves.

    Arrears does not pay the instalment at t = 0, worth 1; against that, its guarantee
    window is 1 ... 120, so the instalment at t = 120 is certain for it and
    survival-contingent for advance, worth ``v^10 (1 - l~(120))``.  The guaranteed annuity
    rises in exactly the inverse proportion -- 0,34 %, not the 5 % of the research file,
    which is an annual-annuity identity applied to a monthly one.
    """
    adv, arr = de_sofort_anchor, sofortrente.Projection[9]
    assert arr.first_pay_mth() == ARREARS_DERIVED["first_pay_mth"]
    assert arr.guar_end_mth() == ARREARS_DERIVED["guar_end_mth"]
    assert arr.annuity_factor() == pytest.approx(
        ARREARS_DERIVED["annuity_factor"], abs=5e-10)
    assert arr.annuity_pp_derived() == pytest.approx(
        ARREARS_DERIVED["annuity_pp_derived"], abs=5e-10)
    gap = adv.annuity_factor() - arr.annuity_factor()
    assert gap == pytest.approx(ARREARS_DERIVED["factor_gap"], abs=5e-10)
    assert adv.tariff_lives(120, 1) == pytest.approx(
        ARREARS_DERIVED["tariff_lives_120"], abs=5e-10)
    certain_gain = (1 / 1.01) ** 10 * (1 - adv.tariff_lives(120, 1))
    assert certain_gain == pytest.approx(ARREARS_DERIVED["certain_gain"], abs=5e-10)
    assert 1.0 - certain_gain == pytest.approx(gap, abs=1e-9)
    ratio = arr.annuity_pp_derived() / adv.annuity_pp_derived()
    assert ratio == pytest.approx(adv.annuity_factor() / arr.annuity_factor(), rel=1e-12)
    assert ratio - 1 == pytest.approx(0.0034, abs=5e-5)
    # Its first month is better by one instalment plus that instalment's running cost,
    # and it repays the difference over the following fifty-six years.
    df = arr.result_cf()
    for column, total in ARREARS_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert arr.net_cf(0) - 97394.5676 == pytest.approx(398.93 + 1.50, abs=0.02)
    assert df["net_cf"].sum() < TOTALS["net_cf"]


@pytest.mark.parametrize("t", sorted(INFORCE))
def test_the_in_force_variant_row(sofortrente, t):
    """Model point 10 carries an annuity struck in 2012 on a 1,75 % tariff and the model
    uses it rather than striking one; ``surplus_form = konstant`` has zero growth, so the
    instalment is 430,00 + 20 % = 516,00 EUR and only expense inflation moves."""
    pols_if, prem, ann, guar, exp, net = INFORCE[t]
    p = sofortrente.Projection[10]
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == prem
    assert p.annuity_payments(t) == pytest.approx(ann, abs=CENT)
    assert p.claims(t, "GUARANTEE") == pytest.approx(guar, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_cell_with_the_ueberschussrente_switched_off(sofortrente, de_sofort_anchor):
    """Model point 14 derives the identical guaranteed instalment and nothing else.

    That is the arithmetic statement that ``ä`` does not depend on ``surplus_form``.  The
    whole modelled surplus is 10 617,37 EUR undiscounted, and it turns the sign of the
    undiscounted total.
    """
    off, on = sofortrente.Projection[14], de_sofort_anchor
    assert off.surplus_form() == "none"
    assert off.surplus_init_pct() == 0.0 and off.surplus_growth() == 0.0
    assert off.annuity_factor() == pytest.approx(on.annuity_factor(), rel=1e-15)
    assert off.annuity_pp_derived() == pytest.approx(on.annuity_pp_derived(), rel=1e-15)
    assert all(off.annuity_surp_pp(t) == 0.0 for t in (0, 12, 240, 671))
    assert all(off.annuity_pp(t) == off.annuity_guar_pp(t) for t in (0, 12, 240, 671))
    df, on_df = off.result_cf(), on.result_cf()
    for column, total in SURPLUS_OFF_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    # Summed at full precision and then rounded, like every other total here; the
    # difference of the two *printed* totals is -10 617,38, half a cent the other side.
    assert (on_df["net_cf"].sum() - df["net_cf"].sum()) == pytest.approx(
        -10617.3748, abs=CENT)
    assert TOTALS["net_cf"] - SURPLUS_OFF_TOTALS["net_cf"] == pytest.approx(
        -10617.38, abs=CENT)
    assert (on_df["pols_if"] - df["pols_if"]).abs().max() == 0.0
    assert (on_df["expenses"] - df["expenses"]).abs().max() == 0.0
    assert df["net_cf"].sum() > 0.0 and on_df["net_cf"].sum() < 0.0


# The published check_* identities, and delib's first ruling
def test_every_check_closes_on_the_anchor_cell(de_sofort_anchor):
    """All nine, each a bool over all t, with the residuals zero where one exists.

    ``check_equivalence`` is the pricing identity ``SP_net == R x ä x (1 + beta) +
    refund_pv()``, to ``roll_fwd_tol`` scaled by ``net_single_prem()``; it is rebuilt here
    from the published parts rather than only called.
    """
    p = de_sofort_anchor
    for name in ("check_net_cf", "check_lives_roll_fwd", "check_annuity_roll_fwd",
                 "check_refund_run_off", "check_payment_factor",
                 "check_guarantee_certain", "check_equivalence",
                 "check_death_option_xor", "check_tariff_int_rate"):
        value = getattr(p, name)()
        assert isinstance(value, bool), name
        assert value is True, name
    for name in ("check_net_cf_resid", "check_lives_roll_fwd_resid",
                 "check_annuity_roll_fwd_resid", "check_refund_run_off_resid",
                 "check_payment_factor_resid", "check_guarantee_certain_resid"):
        for t in (0, 1, 11, 12, 119, 120, 240, 360, 671):
            assert getattr(p, name)(t) == pytest.approx(0.0, abs=1e-8), (name, t)
    rebuilt = (p.annuity_pp_derived() * p.annuity_factor()
               * (1 + p.expense_load_beta) + p.refund_pv())
    assert rebuilt == pytest.approx(p.net_single_prem(), abs=1e-6)
    assert p.check_equivalence_resid() == pytest.approx(0.0, abs=1e-6)
    assert p.roll_fwd_tol == 1e-8
    assert p.solve_tol == 1e-10 and p.solve_max_iter == 200


def test_check_net_cf_rebuilds_the_statement_a_different_way(de_sofort_anchor):
    """delib's first ruling: net_cf reconciles in code, not only in prose.

    ``net_cf(t) == premiums(t) - 1{payment month} pols_if_init A(t) payment_factor(t)
    - claims(t, "REFUND") - expenses(t)``.  **Not** a restatement of the definition:
    ``net_cf`` reaches the instalment outgo through the two published legs while this
    rebuilds it through the single ``max()`` factor, so it asserts that the split into
    those legs is exhaustive and non-overlapping.
    """
    p = de_sofort_anchor
    assert p.check_net_cf() is True
    for t in (0, 1, 60, 119, 120, 121, 240, 360, 480, 671):
        rebuilt = (p.premiums(t)
                   - p.pols_if_init() * p.annuity_pp(t) * p.payment_factor(t)
                   - p.claims(t, "REFUND") - p.expenses(t))
        assert p.net_cf(t) == pytest.approx(rebuilt, abs=1e-9), t
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9), t
    for t in (0, 60, 119, 120, 240):
        assert p.annuity_payments(t) + p.claims(t, "GUARANTEE") == pytest.approx(
            p.pols_if_init() * p.annuity_pp(t) * p.payment_factor(t), abs=1e-9)


def test_the_two_configuration_checks(sofortrente, de_sofort_anchor):
    """``check_tariff_int_rate`` is an inequality; ``check_death_option_xor`` an exclusion.

    A carrier may price below the *Höchstrechnungszins* and one in the corpus is observed
    doing so, and the cap is read at the contract's own ``entry_year``: model point 13 is a
    2022 vintage capped at 0,25 %, model point 10 a 2012 vintage at 1,75 %.  A point
    combining a *Kapitalrückgewähr* with a *Rentengarantiezeit* or a *Hinterbliebenenrente*
    would price a guarantee the refund solve does not see, so the shipped table has none.
    """
    assert de_sofort_anchor.check_tariff_int_rate() is True
    old = sofortrente.Projection[13]
    assert old.entry_year() == 2022
    assert old.max_tariff_int_rate() == 0.0025 and old.tariff_int_rate() == 0.0025
    assert old.check_tariff_int_rate() is True
    legacy = sofortrente.Projection[10]
    assert legacy.max_tariff_int_rate() == 0.0175
    assert legacy.tariff_int_rate() <= legacy.max_tariff_int_rate()
    table = sofortrente.Data.model_point_table()
    for point_id, row in table.iterrows():
        both = (str(row["refund_form"]) != "none"
                and (int(row["guar_years"]) > 0 or float(row["surv_pct"]) > 0))
        assert not both, point_id
    for point_id in (1, 3, 6):
        assert sofortrente.Projection[point_id].check_death_option_xor() is True


# Pitfall 1 -- projecting only the guaranteed annuity
def test_pitfall_1_the_ueberschussrente_is_a_projected_cash_flow(
        sofortrente, de_sofort_anchor):
    """Not guaranteed, but projected: publishing only the *garantierte Rente* models less
    than the payment.  Model point 14 switches the surplus off and is the equality case."""
    p = de_sofort_anchor
    assert p.surplus_form() == "teildynamisch"
    for t in (0, 1, 11, 12, 119, 240, 671):
        assert p.annuity_pp(t) > p.annuity_guar_pp(t), t
        assert p.annuity_pp(t) == pytest.approx(
            p.annuity_guar_pp(t) + p.annuity_surp_pp(t), rel=1e-12)
    assert p.annuity_surp_pp(0) / p.annuity_guar_pp(0) == pytest.approx(0.10, rel=1e-12)
    off = sofortrente.Projection[14]
    for t in (0, 12, 240, 671):
        assert off.annuity_pp(t) == off.annuity_guar_pp(t)


# Pitfall 2 -- decrementing the guaranteed instalments
def test_pitfall_2_the_guaranteed_instalments_are_not_decremented(de_sofort_anchor):
    """Inside the *Rentengarantiezeit* the instalment is certain, so the two legs add back
    to the whole of it at every one of the 120 payment months, exactly."""
    p = de_sofort_anchor
    for t in range(0, p.guar_end_mth()):
        assert p.is_payment_mth(t)
        assert p.annuity_payments(t) + p.claims(t, "GUARANTEE") == pytest.approx(
            p.pols_if_init() * p.annuity_pp(t), abs=1e-9), t
        assert p.pols_if(t) == 1.0, t
    assert p.claims(120, "GUARANTEE") == 0.0
    assert p.annuity_payments(120) == pytest.approx(
        p.annuity_pp(120) * p.lives_if(120, 1), abs=1e-9)
    assert p.pols_if(120) < 1.0


# Pitfall 3 -- adding the certain floor instead of taking a max
def test_pitfall_3_the_certain_floor_is_a_max_and_not_a_sum(sofortrente,
                                                            de_sofort_anchor):
    """``gamma + l_a`` pays ``1 + l_a`` for the whole guarantee -- nearly double.

    The factor is exactly 1 inside the guarantee on a single-life cell and never exceeds
    ``1 + surv_pct`` anywhere; on a joint-life cell it is still exactly 1 inside its
    guarantee, because the survivor's leg is gated off.
    """
    p = de_sofort_anchor
    assert p.surv_pct() == 0.0
    for t in (0, 1, 60, 119):
        assert p.payment_factor(t) == 1.0, t
        assert p.payment_factor(t) == max(p.certain_floor(t), p.lives_if(t, 1))
        assert p.payment_factor(t) < p.certain_floor(t) + p.lives_if(t, 1) + 1e-12
    for t in (120, 240, 360):
        assert p.payment_factor(t) == pytest.approx(p.lives_if(t, 1), rel=1e-15)
    joint = sofortrente.Projection[5]
    assert joint.surv_pct() == 1.0 and joint.guar_years() == 20
    assert joint.payment_factor(0) == joint.payment_factor(120) == 1.0
    assert joint.payment_factor(239) == 1.0
    for q in (p, joint):
        assert max(q.payment_factor(t)
                   for t in range(0, q.proj_len())) <= 1.0 + q.surv_pct()
        assert q.check_guarantee_certain() is True


# Pitfall 4 -- paying the survivor on top during the guarantee
def test_pitfall_4_the_survivor_leg_is_gated_inside_the_guarantee(sofortrente):
    """Model point 5 has a 20-year guarantee and a 100 % *Hinterbliebenenrente*, so the
    survivor's leg is zero for each of the first 240 months and only then comes into
    payment; on the anchor cell, which buys no rider, it is zero everywhere."""
    p = sofortrente.Projection[5]
    assert p.guar_end_mth() == 240 and p.surv_pct() == 1.0
    for t in range(0, 240):
        assert p.annuity_payments(t, "SURVIVOR") == 0.0, t
    assert p.annuity_payments(240, "SURVIVOR") == pytest.approx(88.7902217357, abs=CENT)
    assert any(p.annuity_payments(t, "SURVIVOR") > 0.0 for t in range(240, 400))
    assert p.certain_floor(239) == 1.0 and p.certain_floor(240) == 0.0
    assert p.check_payment_factor() is True
    single = sofortrente.Projection[1]
    assert all(single.annuity_payments(t, "SURVIVOR") == 0.0
               for t in (0, 60, 120, 240, 671))


# Pitfall 5 -- evaluating the Kapitalrückgewähr instead of solving it
def test_pitfall_5_the_refund_is_solved_not_evaluated(sofortrente):
    """The equation is implicit in R, and the naive answer is 6,7 % too high.

    The naive route computes the plain annuity ``R_max``, values the refund leg *at that
    annuity* and divides the remainder by ``ä (1 + beta)``: 318,7362 EUR against the solved
    298,8348 EUR, and a refund leg of 13 546,37 EUR against 18 788,31 EUR, because a
    smaller annuity runs the refund off more slowly.
    """
    p = sofortrente.Projection[3]
    assert p.refund_form() == "full"
    assert p.annuity_factor() == pytest.approx(REFUND["annuity_factor"], abs=5e-10)
    assert p.annuity_pp_derived() == pytest.approx(
        REFUND["annuity_pp_derived"], abs=5e-9)
    assert p.refund_pv() == pytest.approx(REFUND["refund_pv"], abs=1e-6)
    assert p.check_equivalence() is True

    load = 1.0 + p.expense_load_beta
    r_max = p.net_single_prem() / (p.annuity_factor() * load)
    assert r_max == pytest.approx(REFUND["r_max_naive"], abs=5e-9)
    # The refund leg valued at R_max, rebuilt here rather than read from the model.
    v = 1.0 / (1.0 + p.tariff_int_rate())
    per, fp, sp = p.pay_period_mths(), p.first_pay_mth(), p.single_prem()
    pv_at_r_max = 0.0
    for t in range(0, p.proj_len()):
        d = p.tariff_lives(t, 1) - p.tariff_lives(t + 1, 1)
        if d <= 0.0:
            continue
        n = 0 if t < fp else (t - fp) // per + 1
        pv_at_r_max += v ** (t / 12.0) * d * max(sp - n * r_max, 0.0)
    assert pv_at_r_max == pytest.approx(REFUND["refund_pv_at_r_max"], abs=1e-6)

    naive = (p.net_single_prem() - pv_at_r_max) / (p.annuity_factor() * load)
    assert naive == pytest.approx(REFUND["r_naive"], abs=5e-9)
    assert abs(naive - p.annuity_pp_derived()) > 19.0     # not a rounding
    assert naive / p.annuity_pp_derived() - 1 == pytest.approx(0.0666, abs=5e-4)
    assert p.refund_pv() > pv_at_r_max


def test_the_refund_runs_off_one_instalment_at_a_time(sofortrente):
    """It opens at the *Einmalbeitrag* less the first instalment and reaches zero at
    ``ceil(SP / R)`` payments, counted directly rather than off the recursion; where none
    was bought it is identically zero, and inside an *Aufschubzeit* it is the whole
    *Einmalbeitrag*."""
    p = sofortrente.Projection[3]
    r = p.annuity_guar_pp(0)
    assert p.refund_pp(0) == pytest.approx(REFUND["refund_pp_0"], abs=CENT)
    assert p.refund_pp(0) == pytest.approx(p.single_prem() - r, abs=1e-9)
    for t in (1, 12, 120, 240):
        assert p.refund_pp(t) == pytest.approx(
            max(p.refund_pp(t - 1) - r, 0.0), abs=1e-9), t
    n_req = math.ceil(p.single_prem() / r)
    assert n_req == REFUND["instalments_to_exhaust"]
    t_zero = p.first_pay_mth() + (n_req - 1) * p.pay_period_mths()
    assert p.refund_pp(t_zero) == 0.0 and p.refund_pp(t_zero - 1) > 0.0
    assert p.check_refund_run_off() is True
    plain = sofortrente.Projection[1]
    assert plain.refund_form() == "none"
    assert all(plain.refund_pp(t) == 0.0 for t in (0, 120, 240, 671))
    assert plain.check_refund_run_off() is True
    # Model point 6 pairs the refund with a five-year *Aufschubzeit*: no instalment has
    # been paid inside the window, so C(t) = 0 and the refund is the whole
    # *Einmalbeitrag* -- the deferment death benefit out of the same machinery.
    p = sofortrente.Projection[6]
    assert p.defer_mths() == 60 and p.first_pay_mth() == 60
    assert all(p.cum_annuity_guar_pp(t) == 0.0 for t in (0, 30, 59))
    assert all(p.refund_pp(t) == p.single_prem() for t in (0, 30, 59))
    assert all(p.annuity_payments(t) == 0.0 for t in (0, 30, 59))
    assert p.annuity_payments(60) > 0.0
    assert p.refund_pp(60) < p.single_prem()
    assert p.claims(0, "REFUND") > 0.0        # deaths inside the deferment are settled
    assert p.check_refund_run_off() is True


# Pitfall 6 -- measuring the refund against the total annuity
def test_pitfall_6_the_refund_is_netted_against_the_guaranteed_annuity(
        sofortrente, tmp_path):
    """Model point 3 against a copy of it with the surplus switched off.

    ``refund_pp`` must be **identical** in the two, because it accumulates
    ``annuity_guar_pp`` alone while ``annuity_pp`` differs by the whole *Überschussrente*.
    A refund netted against the total annuity would retire the capital sooner.
    """
    base = sofortrente.Projection[3]
    alt = alt_model(tmp_path, "Sofort_DE_S_nosurp", {3: {"surplus_form": "none"}})
    try:
        off = alt.Projection[3]
        assert off.surplus_form() == "none" and base.surplus_form() == "teildynamisch"
        assert off.annuity_pp_derived() == pytest.approx(
            base.annuity_pp_derived(), rel=1e-15)
        for t in (0, 1, 12, 120, 240, 334):
            assert off.refund_pp(t) == pytest.approx(base.refund_pp(t), rel=1e-15), t
            assert off.cum_annuity_guar_pp(t) == pytest.approx(
                base.cum_annuity_guar_pp(t), rel=1e-15), t
        for t in (0, 120, 240):
            assert off.annuity_pp(t) < base.annuity_pp(t), t
        assert math.ceil(off.single_prem() / off.annuity_guar_pp(0)) == (
            REFUND["instalments_to_exhaust"])
        assert off.check_refund_run_off() is True
    finally:
        alt.close()


# Pitfalls 7, 8 and 9 -- the generational surface and its first-order margin
def test_pitfall_7_the_surface_is_indexed_by_birth_year_not_projection_year(
        sofortrente, de_sofort_anchor):
    """Two cells with the same entry age and different cohorts, read at the same age.

    A period table would give a 65-year-old born in 1960 and one born in 1947 the same
    rate; a generational surface does not, and the earlier cohort reads **heavier**
    mortality because its exponent is negative and is not floored.
    """
    young, old = de_sofort_anchor, sofortrente.Projection[10]
    assert young.entry_age(1) == old.entry_age(1) == 65
    assert young.birth_year(1) == 1960 and old.birth_year(1) == 1947
    assert young.age(0, 1) == old.age(0, 1) == 65
    assert old.mort_rate(0, 1) != young.mort_rate(0, 1)
    assert old.mort_rate(0, 1) > young.mort_rate(0, 1)
    assert young.mort_rate(0, 1) == pytest.approx(
        young.mort_rate_at_age(65, "M", "SECOND"), rel=1e-12)   # exponent zero
    lam = young.improve_rate_at_age(65, "SECOND")
    assert old.mort_rate(0, 1) == pytest.approx(
        old.mort_rate_at_age(65, "M", "SECOND") * (1 - lam) ** (1947 + 65 - 2025),
        rel=1e-12)
    assert 1947 + 65 - 2025 == -13


def test_pitfall_8_a_period_proxy_would_be_a_different_model(de_sofort_anchor):
    """The improvement lives inside the surface, and it is worth 4,9 % of the factor.

    Rebuilding the annuity factor here with ``lambda == 0`` -- independently of the model,
    on its own table -- gives 250,6755 against 263,5711, so the guaranteed annuity a period
    proxy would strike is 381,32 EUR rather than 362,67 EUR.
    """
    p = de_sofort_anchor
    assert p.mort_base_year == 2025
    assert p.improve_rate_at_age(70, "FIRST") > 0.0
    assert p.mort_rate_gen(70, "U", 1960, "FIRST") != p.mort_rate_at_age(70, "U", "FIRST")
    assert p.mort_rate_gen(70, "U", 1960, "FIRST") < p.mort_rate_at_age(70, "U", "FIRST")
    assert p.mort_rate_gen(65, "M", 1960, "SECOND") == pytest.approx(
        p.mort_rate_at_age(65, "M", "SECOND"), rel=1e-15)     # 1960 + 65 == 2025
    v, lives, factor = 1.0 / 1.01, 1.0, 0.0
    for k in range(0, p.proj_len()):
        if p.is_payment_mth(k):
            factor += v ** (k / 12.0) * max(p.certain_floor(k), lives)
        q = min(p.mort_rate_at_age(p.age(k, 1), "U", "FIRST"), 1.0)
        lives *= (1.0 - q) ** (1.0 / 12.0)
    assert factor == pytest.approx(250.6754599050, abs=5e-9)
    assert factor < p.annuity_factor()
    assert factor / p.annuity_factor() - 1 == pytest.approx(-0.0489, abs=5e-5)
    assert p.net_single_prem() / (factor * 1.02) == pytest.approx(381.32, abs=CENT)


def test_pitfall_9_the_first_order_margin_reaches_the_trend(de_sofort_anchor):
    """Lighter in level **and** improving faster, so the ratio of the two moves.

    It falls from 0,666667 at t = 0 to 0,638433 at t = 240 as the trend margin compounds.
    A level-only margin would hold it at 2/3 -- which is what it returns to once the
    *Trendfunktion* has tapered to zero at attained age 105.
    """
    p = de_sofort_anchor
    assert all(p.mort_rate_tariff(t, 1) < p.mort_rate(t, 1) for t in range(0, 400))
    assert p.improve_rate_at_age(65, "FIRST") == pytest.approx(
        1.25 * p.improve_rate_at_age(65, "SECOND"), rel=1e-12)
    ratios = [p.mort_rate_tariff(t, 1) / p.mort_rate(t, 1) for t in range(0, 241, 12)]
    assert ratios[0] == pytest.approx(0.6666668334, abs=5e-9)
    assert ratios[-1] == pytest.approx(0.6384325119, abs=5e-9)
    assert all(b < a for a, b in zip(ratios, ratios[1:])), "the ratio does not fall"
    assert p.improve_rate_at_age(105, "SECOND") == 0.0
    assert p.age(480, 1) == 105
    assert p.mort_rate_tariff(480, 1) / p.mort_rate(480, 1) == pytest.approx(
        2.0 / 3.0, abs=1e-6)


# Pitfall 10 -- letting sex into the tariff
def test_pitfall_10_the_tariff_is_unisex_and_the_decrement_is_not(
        de_sofort_anchor, tmp_path):
    """The anchor cell as a woman: the same annuity, a different survival path.

    German new business has had to be unisex since 21 December 2012, so ``sex`` reaches
    only the projected decrement.  Letting it into ``ä`` would reproduce an unlawful tariff
    -- and would look perfectly plausible in the output.
    """
    male = de_sofort_anchor
    alt = alt_model(tmp_path, "Sofort_DE_S_female", {1: {"sex": "F"}})
    try:
        female = alt.Projection[1]
        assert female.sex(1) == "F" and male.sex(1) == "M"
        assert female.annuity_factor() == pytest.approx(male.annuity_factor(), rel=1e-15)
        assert female.annuity_pp_derived() == pytest.approx(
            male.annuity_pp_derived(), rel=1e-15)
        assert female.mort_rate_tariff(0, 1) == pytest.approx(
            male.mort_rate_tariff(0, 1), rel=1e-15)
        assert female.mort_rate(0, 1) < male.mort_rate(0, 1)
        assert female.lives_if(120, 1) > male.lives_if(120, 1)
        assert female.result_cf()["annuity_payments"].sum() > (
            male.result_cf()["annuity_payments"].sum())
    finally:
        alt.close()
    # The blend itself is computed, not a row of the CSV.
    assert set(male.data.mort_table().index.get_level_values("sex")) == {"M", "F"}
    assert male.mix_male == 0.45
    assert male.mort_rate_at_age(70, "U", "FIRST") == pytest.approx(
        0.45 * male.mort_rate_at_age(70, "M", "FIRST")
        + 0.55 * male.mort_rate_at_age(70, "F", "FIRST"), rel=1e-12)


# Pitfalls 11 and 12 -- the in-force model point
def test_pitfalls_11_and_12_the_in_force_point_neither_collects_nor_reopens(
        sofortrente, de_sofort_anchor):
    """An in-force point's frame contains no t = 0, so it collects no *Einmalbeitrag* and
    carries no acquisition expense -- both happened before the valuation date -- and it
    opens at the duration the contract has already run rather than at zero."""
    p = sofortrente.Projection[10]
    df = p.result_cf()
    assert (df["premiums"] == 0.0).all() and df["premiums"].sum() == 0.0
    assert all(p.premiums(t) == 0.0 for t in range(156, 672))
    anchor_df = de_sofort_anchor.result_cf()
    assert anchor_df["premiums"].sum() == pytest.approx(
        de_sofort_anchor.single_prem() * de_sofort_anchor.pols_if_init(), abs=1e-9)
    assert (anchor_df["premiums"] > 0).sum() == 1
    # 516 rows, a given annuity the model uses as it stands, and an equivalence that
    # returns True without asserting anything.
    assert len(df) == 516 and list(df.index) == list(range(156, 672))
    for column, total in INFORCE_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert p.annuity_pp_init() == 430.0
    assert p.annuity_guar_pp(156) == 430.0 and p.annuity_guar_pp(500) == 430.0
    assert p.surplus_init_pct() == 0.20 and p.surplus_growth() == 0.0
    assert p.annuity_pp(156) == pytest.approx(516.00, abs=CENT)
    assert p.annuity_pp(400) == pytest.approx(516.00, abs=CENT)
    assert p.check_equivalence() is True and p.check_equivalence_resid() == 0.0
    assert p.entry_year() == 2012
    assert p.max_tariff_int_rate() == 0.0175 and p.tariff_int_rate() == 0.0175
    assert p.duration_mth_init() == 156 and p.t_start() == 156
    assert df.index[0] == 156
    assert p.pols_if(p.t_start()) == pytest.approx(p.pols_if_init(), rel=1e-12)
    assert p.lives_if(p.t_start(), 1) == 1.0
    assert p.expense_acq_rate * p.single_prem() + p.expense_acq_fixed > 2000.0
    assert df["expenses"].max() < 20.0
    assert p.expenses(156) == pytest.approx(
        (60.0 / 12 + 1.50) * p.infl_factor(156), abs=1e-9)
    assert (p.duration_mth(156) == 156 and p.duration(156) == 13
            and p.policy_year(156) == 14)


# Pitfall 13 -- the arrears offset
def test_pitfall_13_the_arrears_offset_and_the_instalment_count(sofortrente,
                                                                de_sofort_anchor):
    """Under arrears the first instalment falls at ``defer_mths() + p``, and a G-year
    guarantee still covers ``G x m`` instalments -- at every frequency."""
    arr = sofortrente.Projection[9]
    assert arr.first_pay_mth() == 1
    assert not arr.is_payment_mth(0) and arr.is_payment_mth(1)
    assert arr.annuity_payments(0) == 0.0 and arr.claims(0, "GUARANTEE") == 0.0
    assert arr.annuity_payments(1) > 0.0
    counted = [sum(1 for t in range(0, q.proj_len())
                   if q.is_payment_mth(t) and q.certain_floor(t) == 1.0)
               for q in (de_sofort_anchor, arr)]
    assert counted == [120, 120]
    assert arr.guar_end_mth() - arr.first_pay_mth() == 12 * arr.guar_years()
    for point_id in (7, 8, 11):
        q = sofortrente.Projection[point_id]
        n = sum(1 for t in range(0, q.proj_len())
                if q.is_payment_mth(t) and q.certain_floor(t) == 1.0)
        assert n == q.guar_years() * q.payment_freq(), point_id
        assert q.pay_period_mths() == 12 // q.payment_freq()


# Pitfalls 14 and 15 -- the Überschussrente
def test_pitfall_14_the_surplus_steps_only_at_the_policy_anniversary(de_sofort_anchor):
    """Compounding an annual rate monthly is the obvious wrong reading on this grid:
    ``annuity_surp_pp`` is flat across each block of twelve months and steps by exactly
    ``1 + psi`` at every multiple of twelve."""
    p = de_sofort_anchor
    psi = p.surplus_growth()
    for t in range(1, 60):
        if t % 12 == 0:
            assert p.annuity_surp_pp(t) == pytest.approx(
                p.annuity_surp_pp(t - 1) * (1 + psi), rel=1e-12), t
        else:
            assert p.annuity_surp_pp(t) == pytest.approx(
                p.annuity_surp_pp(t - 1), rel=1e-15), t
        assert p.check_annuity_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-9), t
    assert len({round(p.annuity_surp_pp(t), 10) for t in range(0, 12)}) == 1
    assert p.annuity_surp_pp(12) < p.annuity_surp_pp(0) * (1 + psi) ** 12
    assert p.annuity_surp_pp(12) == pytest.approx(
        p.annuity_surp_pp(0) * (1 + psi), rel=1e-12)


def test_pitfall_15_the_total_annuity_ratchets(sofortrente, de_sofort_anchor):
    """The *Bonusrente* mechanic stated arithmetically: an increment, once bought as
    paid-up annuity, does not come back off.  A constant form does not fall either; it
    simply does not rise."""
    p = de_sofort_anchor
    n = p.proj_len()
    assert all(p.annuity_pp(t) >= p.annuity_pp(t - 1) for t in range(1, n))
    assert p.annuity_pp(n - 1) > p.annuity_pp(0)
    assert p.check_annuity_roll_fwd() is True
    konstant = sofortrente.Projection[10]
    assert konstant.surplus_form() == "konstant"
    assert all(konstant.annuity_pp(t) == konstant.annuity_pp(t - 1)
               for t in range(157, 300))
    assert konstant.check_annuity_roll_fwd() is True


# Pitfall 16 -- discounting the published cash flows at the tariff rate
def test_pitfall_16_the_tariff_rate_reaches_the_projection_only_through_the_factor(
        sofortrente, tmp_path):
    """The published flows are undiscounted: ``i`` enters through ``ä`` and ``refund_pv()``
    and nowhere else, so model point 10 -- which carries a **given** annuity, closing both
    channels -- has a cash flow frame invariant to the tariff rate, to the last bit."""
    base = sofortrente.Projection[10]
    before = base.result_cf()
    alt = alt_model(tmp_path, "Sofort_DE_S_rate", {10: {"tariff_int_rate": 0.0050}})
    try:
        moved = alt.Projection[10]
        assert moved.tariff_int_rate() == 0.0050
        assert moved.check_tariff_int_rate() is True
        after = moved.result_cf()
        assert list(after.columns) == list(before.columns)
        assert (after - before).abs().max().max() == 0.0
        assert alt.Projection[1].annuity_pp_derived() == pytest.approx(
            sofortrente.Projection[1].annuity_pp_derived(), rel=1e-15)
    finally:
        alt.close()


# Pitfall 17 -- there is no lapse, no surrender value and no paid-up state
def test_pitfall_17_no_lapse_no_surrender_no_paid_up_anywhere(sofortrente,
                                                              de_sofort_anchor):
    """Once the *Rentenbezug* has begun the contract cannot be terminated, so the model
    carries none of the machinery a reader arriving from a savings product would add.  The
    absent names are asserted rather than assumed: each is one somebody would plausibly
    introduce, and every total would still look sane afterwards."""
    names = set(sofortrente.Projection.cells) | set(sofortrente.Projection.refs)
    for absent in ("lapse_rate", "lapse_rate_mth", "lapse_table", "pols_lapse", "av_at",
                   "av_pp_at", "cv_pp", "prem_to_av_pp", "surr_charge_rate", "mvr",
                   "surr_value_pp", "paid_up_factor", "withdrawals", "wd_free_pp",
                   "claims_surr", "asset_share", "commuted_value", "commute_amount",
                   "premium_mth_pp", "prem_pp"):
        assert absent not in names, absent
    # The enum accessors validate, so a typo is an error and not a wrong lookup.
    for bad in (lambda: de_sofort_anchor.claims(1, "LAPSE"),
                lambda: de_sofort_anchor.claims(1, "SURRENDER"),
                lambda: de_sofort_anchor.annuity_payments(0, "BENEFICIARY"),
                lambda: de_sofort_anchor.entry_age(3),
                lambda: de_sofort_anchor.sex(3)):
        with pytest.raises(FormulaError):
            bad()
    assert set(de_sofort_anchor.result_cf().columns) == {
        "pols_if", "premiums", "annuity_payments", "claims_guarantee",
        "claims_refund", "expenses", "liability_cf", "net_cf"}
    joint = sofortrente.Projection[4]
    assert joint.check_lives_roll_fwd() is True
    for life in (1, 2):
        n = joint.proj_len()
        deaths = sum(joint.lives_death(t, life) for t in range(0, n))
        assert deaths + joint.lives_if(n, life) == pytest.approx(
            joint.lives_if(0, life), abs=1e-12), life


# Pitfall 18 -- the projection must outlive the second life, not the annuitant
def test_pitfall_18_proj_len_takes_the_second_lifes_horizon(sofortrente):
    """Model point 4: annuitant 65, second life 62, so the frame runs three years past the
    annuitant's own horizon and the survivor's tail is not truncated."""
    p = sofortrente.Projection[4]
    assert p.surv_pct() == 0.60
    assert p.entry_age(1) == 65 and p.entry_age(2) == 62
    assert p.horizon_mths(1) == 672 and p.horizon_mths(2) == 708
    assert p.proj_len() == 12 * (p.omega_age - p.entry_age(2)) == 708
    assert p.proj_len() > p.horizon_mths(1)
    assert len(p.result_cf()) == 708 and p.result_cf().index[-1] == 707
    assert math.isfinite(p.annuity_payments(p.proj_len() - 1))
    assert p.annuity_payments(p.proj_len() - 1) >= 0.0
    assert p.lives_if(672, 1) == 0.0 and p.lives_if(672, 2) > 0.0
    assert any(p.annuity_payments(t, "SURVIVOR") > 0.0 for t in range(600, 700))
    long_guar = sofortrente.Projection[12]
    assert long_guar.guar_years() == 30 and long_guar.guar_end_mth() == 360
    assert long_guar.proj_len() == max(long_guar.horizon_mths(1),
                                       long_guar.guar_end_mth())


# Structure, documentation and the shipped inputs
def test_result_cf_shape_and_both_signs_of_the_net_flow(de_sofort_anchor):
    """The notes' eight columns in order, pols_if first and net_cf income-positive, with
    ``liability_cf`` exactly its negative -- so the sign convention is verifiable in the
    frame rather than only in prose."""
    df = de_sofort_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "annuity_payments", "claims_guarantee",
        "claims_refund", "expenses", "liability_cf", "net_cf"]
    assert "claims" not in df.columns          # no subtotal beside its own parts
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert df["pols_if"].iloc[0] == de_sofort_anchor.pols_if_init()
    assert (df["pols_if"] >= 0.0).all()
    assert df["net_cf"].iloc[0] == pytest.approx(97394.57, abs=CENT)
    assert (df["net_cf"].iloc[1:] <= 0.0).all()
    # result_pols() is the state behind it, on the same index and with pols_if in both.
    dp = de_sofort_anchor.result_pols()
    assert list(dp.columns) == [
        "lives_if_1", "lives_if_2", "certain_floor", "payment_factor",
        "annuity_guar_pp", "annuity_surp_pp", "annuity_pp", "refund_pp",
        "cum_annuity_guar_pp", "pols_if"]
    assert dp.index.name == "t" and list(dp.index) == list(df.index)
    assert (dp["pols_if"] - df["pols_if"]).abs().max() == 0.0
    assert (dp["lives_if_2"] == 0.0).all() and (dp["refund_pp"] == 0.0).all()


def test_docstrings_and_the_chassis_vocabulary(sofortrente):
    """Specifics a reader relies on, asserted so they cannot go stale silently."""
    doc = sofortrente.doc
    assert "Rentenversicherung" in doc and "mechanics demonstration" in doc
    assert "external" in doc                    # inputs are not stored in the model
    assert "once per model" in doc              # why Data exists
    assert "Rentengarantiezeit" in doc and "Hinterbliebenenrente" in doc
    proj = sofortrente.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "payment_factor", "certain_floor",
                  "annuity_factor", "annuity_pp_derived", "refund_pp",
                  "mort_rate_tariff", "tariff_lives"):
        assert cells in proj, cells
    data = sofortrente.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table",
                  "improvement_table", "surplus_scale_table"):
        assert cells in data, cells
    assert "DAV 2004 R" in data and "not redistributed" in data
    # pols_if earns the conventions suite's payout exemption by docstring, not by list.
    assert "payment obligation remains" in sofortrente.Projection.cells["pols_if"].doc
    # The payout-annuity chassis vocabulary SPIA_US_S, PA_UK_S and Rente_FR_S share
    # must mean the same thing here, and the two of theirs this product deliberately
    # does not carry must stay away.
    shared = {
        "model_point", "proj_len", "age", "duration_mth", "duration", "policy_year",
        "calendar_year", "horizon_mths", "pols_if", "pols_if_init", "mort_rate",
        "mort_rate_mth", "lives_if", "lives_death", "is_payment_mth", "certain_floor",
        "payment_factor", "annuity_pp", "annuity_payments", "claims", "expenses",
        "net_cf", "liability_cf", "result_cf", "result_pols",
        "check_lives_roll_fwd", "check_payment_factor",
    }
    names = set(sofortrente.Projection.cells) | set(sofortrente.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    # And the names this product deliberately does not share, for stated reasons.
    assert "cum_annuity_pp" not in names        # it is cum_annuity_guar_pp here
    assert "payment_surv_mth" not in names and "payment_factor_life" not in names


def test_the_shipped_tables_mark_their_own_provenance():
    """Five CSVs beside run.py, each saying what it is and, for mortality, what it is not.

    The decrement tables are a **[std]** proxy: DAV 2004 R and DAV 2004 R-Bestand are DAV
    property, are cited by name and never shipped.  The anchor a replacement must preserve
    is that the 0,45 / 0,55 unisex blend of the FIRST series reproduces the research file's
    ``q_base``, with ``q = 1`` at attained age 120 as the closing row.
    """
    import pandas as pd

    parent = MODEL_DIR.parent
    assert INPUT_CSVS == {p.name for p in parent.iterdir() if p.suffix == ".csv"}

    mort = pd.read_csv(parent / "mort_table.csv", index_col=["basis", "sex", "age"])
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert any("DAV 2004 R" in p for p in mort["provenance"])
    assert set(mort.index.get_level_values("basis")) == {"FIRST", "SECOND"}
    assert set(mort.index.get_level_values("sex")) == {"M", "F"}
    assert sorted(set(mort.index.get_level_values("age"))) == list(range(50, 121))
    assert mort["mort_rate"].max() <= 1.0
    assert float(mort.loc[("FIRST", "M", 65), "mort_rate"]) == MORT["first_m_65"]
    assert float(mort.loc[("FIRST", "F", 65), "mort_rate"]) == MORT["first_f_65"]
    for sex in ("M", "F"):
        assert float(mort.loc[("FIRST", sex, 120), "mort_rate"]) == 1.0
        assert float(mort.loc[("SECOND", sex, 120), "mort_rate"]) == 1.0
    male_80 = float(mort.loc[("FIRST", "M", 80), "mort_rate"])
    blend = male_80 * 0.45 + 0.55 * float(mort.loc[("FIRST", "F", 80), "mort_rate"])
    assert blend / male_80 * 1.25 == pytest.approx(1.0, abs=1e-6)

    impr = pd.read_csv(parent / "improvement_table.csv", index_col=["basis", "age"])
    assert all(p.startswith("[std]") for p in impr["provenance"])
    assert float(impr.loc[("SECOND", 65), "improve_rate"]) == 0.015
    assert float(impr.loc[("FIRST", 65), "improve_rate"]) == pytest.approx(
        1.25 * 0.015, rel=1e-12)
    assert float(impr.loc[("SECOND", 105), "improve_rate"]) == 0.0
    assert float(impr.loc[("SECOND", 120), "improve_rate"]) == 0.0

    scale = pd.read_csv(parent / "surplus_scale_table.csv", index_col="surplus_form")
    assert set(scale.index) == {"none", "konstant", "teildynamisch", "volldynamisch"}
    assert all(p.startswith("[std]") for p in scale["provenance"])
    assert float(scale.loc["teildynamisch", "surplus_init_pct"]) == 0.10
    assert float(scale.loc["teildynamisch", "surplus_growth"]) == 0.010
    assert float(scale.loc["none", "surplus_init_pct"]) == 0.0

    caps = pd.read_csv(parent / "hoechstrechnungszins_table.csv", index_col="year_from")
    assert [float(caps.loc[y, "max_rate"]) for y in (2025, 2022, 2012)] == [
        0.0100, 0.0025, 0.0175]
    assert int(caps.loc[2025, "year_to"]) == 9999
    assert all(p.strip() for p in caps["provenance"])

    points = pd.read_csv(parent / "model_point_table.csv", index_col="point_id")
    assert "provenance" not in points.columns    # a configuration, not an assumption
    assert len(points) == 14 and str(points.loc[1, "policy_id"]) == "SOF-000001"
    assert float(points.loc[1, "single_prem"]) == 100000.00
