"""Product tests for ``Endowment_JP_S``, the 養老保険 / 学資保険 reference model.

The house-style contract is asserted once, for every model in the library, in
``test_model_conventions_jp.py``. What is asserted here is this product: the worked
example of ``products/endowment/technical-notes.md`` **hard-coded** so that a reviewer can
check it against the notes by eye, every one of the notes' *Known modeling pitfalls* —
each pitfall being a way an implementation can look right and be wrong — the roll-forward
identities and every ``check_*`` cells on every shipped model point, and each optional
module in both of its positions.

The composite has **two cells and one model**, and both are anchors. ``point_id = 1`` is
the 養老保険 (*yōrō hoken*, endowment assurance) cell: male, 契約年齢 30, 基準保険金額 ¥5,000,000,
30-year term and 30-year premium term, annual premium ¥181,140. ``point_id = 2`` is the
学資保険 (*gakushi hoken*, education endowment) cell: 契約者 male 30, 被保険者 (the child) 0,
22-year term, 17-year premium term, 基準保険金額 ¥1,000,000, annual premium ¥108,564, the S型
staged grid, and 保険料払込免除 (*hokenryō haraikomi menjo*, waiver of premium) on the 契約者 —
**a second decrement on a second life who is not the insured**, which has no analogue in
``uslib`` or ``uklib``.

Tolerances follow the precision the notes display: money to the yen at two decimal places,
in-force probabilities to six decimals.

**Three indices.** The projection index ``t`` is 0-based and counts **policy months** —
``t = 0`` is the first policy month, ``t = proj_len() - 1 = 12n - 1`` the last — so every
cash-flow and in-force literal here is a month. The per-policy value construction
(``pol_val_pp``, ``cv_pp``, ``surr_charge_pp``, ``benefit_pct``, ``prem_cum_pp``,
``loan_pp``) is indexed by the **anniversary** ``k`` instead, in **years**, ``k = 0`` at
issue — and **every one of those literals is unchanged from the annual model**, because the
conversion moved the projection index and left the contractual constructions alone. The
months in between read them through a third index, the **elapsed month** ``u``, by linear
interpolation **[std]**: ``pol_val_pre_at_m(u)``, ``cv_at_m(u)`` and their companions, read
at ``u = t + 1`` by the flows of month ``t`` and equal to the anniversary value exactly at
``u = 12k``. Loop and parameter names below say which index is meant.

That the conversion preserved the annual model is asserted directly rather than assumed:
mortality and surrender convert on the effective convention ``r_m = 1 - (1 - r)^(1/12)``, so
twelve months compound back to the annual rate and ``pols_if(12j)`` reproduces the annual
model's ``pols_if(j)`` at every anniversary.
"""
import math
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from jp_registry import MODELS, LIB


YEN = 0.005           # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["Endowment_JP_S"][0]


def variant_model(tmp_path, rows, name):
    """A copy of the shipped model whose model point table carries extra rows.

    The model and its four CSVs are copied to ``tmp_path`` and the extra points are
    appended to the copied ``model_point_table.csv``, so ``Data.input_dir()`` — which
    resolves to the model folder's parent at run time — picks them up with no formula
    change and nothing at all is written into the product directory.

    ``rows`` maps a new ``point_id`` to ``(source point_id, {column: value})``.
    """
    shutil.copytree(MODEL_DIR, tmp_path / MODEL_DIR.name)
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    table = pd.read_csv(tmp_path / "model_point_table.csv", index_col="point_id")
    for new_id, (src_id, edits) in rows.items():
        row = table.loc[src_id].copy()
        for column, value in edits.items():
            row[column] = value
        table.loc[new_id] = row
    table.to_csv(tmp_path / "model_point_table.csv")

    return mx.read_model(tmp_path / MODEL_DIR.name, name=name)


# ---------------------------------------------------------------------------
# The worked example, hard-coded to the precision the notes display
#
# 養老 anchor cell (point_id = 1).  t (0-based policy MONTH): (pols_if, premiums,
# claims_death, claims_maturity, claims_lapse, expenses, claim_expenses, commissions,
# net_cf)
#
# ``pols_if`` is the TOTAL in force and equals ``pols_if_pay`` on this cell, which has no
# waiver.  ``expenses`` is a twelfth of the annual maintenance charge, plus the single
# acquisition charge at t = 0; the claim handling expense is the separate
# ``claim_expenses`` column beside it.  The 年払 premium and the renewal commission that
# follows it are non-zero in one month out of twelve, and the maturity payment in one
# month out of the whole 360.

ANCHOR_CF = {
    0:   (1.000000, 181_140.00,   283.42,         0.00,     0.00, 50_666.67,
          1.13, 163_026.00,   -32_837.22),
    1:   (0.996547,      0.00,    282.44,         0.00,     0.00,    664.36,
          1.13,       0.00,       -947.94),
    2:   (0.993107,      0.00,    281.47,         0.00,     0.00,    662.07,
          1.13,       0.00,       -944.67),
    11:  (0.962671,      0.00,    272.84,         0.00,   327.82,    641.78,
          1.09,       0.00,     -1_243.53),
    12:  (0.959347, 173_776.15,   275.90,         0.00,   273.66,    645.96,
          1.10,   5_213.28,    167_366.24),
    358: (0.496231,      0.00,  1_239.84,         0.00, 4_157.88,    441.48,
          4.96,       0.00,     -5_844.16),
    359: (0.495148,      0.00,  1_237.14, 2_474_504.99,     0.00,    440.52,
          4.95,       0.00, -2_476_187.59),
}

# The notes' cash-value table, keyed by the ANNIVERSARY k (k = 0 at issue, so k is
# unchanged by the 0-based period convention): k: (W(k), SC(k), CV(k), cum. premiums).
ANCHOR_VALUES = {
    1:    (144_053.26, 43_775.50,   100_277.76,   181_140.0),
    5:    (735_250.45, 37_737.50,   697_512.95,   905_700.0),
    15: (2_313_975.49, 22_642.50, 2_291_332.99, 2_717_100.0),
    29: (4_804_598.71,  1_509.50, 4_803_089.21, 5_253_060.0),
    30: (5_000_000.00,      0.00, 5_000_000.00, 5_434_200.0),
}

# 生保標準生命表2018（死亡保険用）男 at attained ages 30 .. 59: the rates read at the anchor
# ages and the [std] log-linear fill in ln q between them, at the table's own five
# decimals.  Ages 30-35, 40, 45, 50, 55 and 60 are anchors; the rest are the fill.
ANCHOR_Q = (
    0.00068, 0.00069, 0.00070, 0.00072, 0.00074, 0.00077, 0.00084, 0.00091,
    0.00099, 0.00108, 0.00118, 0.00128, 0.00139, 0.00151, 0.00163, 0.00177,
    0.00195, 0.00214, 0.00236, 0.00259, 0.00285, 0.00308, 0.00333, 0.00361,
    0.00390, 0.00422, 0.00461, 0.00503, 0.00548, 0.00598,
)

# Undiscounted totals per policy issued, income-positive.
ANCHOR_TOTALS = {
    "premiums": 3_931_162.67,
    "claims_death": 213_842.47,
    "claims_staged": 0.00,
    "claims_maturity": 2_474_504.99,
    "claims_lapse": 899_875.29,
    "claims_ph_death": 0.00,
    "expenses": 245_871.00,
    "claim_expenses": 855.37,
    "commissions": 275_526.68,
    "net_cf": -179_313.13,
}

# 学資 cell (point_id = 2).  t (0-based policy MONTH): (pols_if, pols_if_pay, pols_wv,
# premiums, claims_death, claims_staged, claims_lapse, expenses, claim_expenses,
# commissions, net_cf).  Here the two in-force series differ: pols_if is the whole
# surviving block and pols_if_pay the part of it still paying.
#
# The staged 学資金 due at anniversary k falls in the SINGLE month t = 12k - 1 — 35, 71,
# 143, 179, 215 and 239 on this cell — and is zero in the other eleven months of its
# policy year.
EDU_CF = {
    0:   (1.000000, 1.000000, 0.000000, 108_564.00,  7.33,       0.00,     0.00,
          50_666.67, 1.35, 97_707.60,  -39_818.95),
    1:   (0.996537, 0.996480, 0.000056,       0.00,  7.31,       0.00,     0.00,
          664.36, 1.35,       0.00,        -673.01),
    2:   (0.993085, 0.992973, 0.000113,       0.00,  7.28,       0.00,     3.95,
          662.06, 1.34,       0.00,        -674.63),
    35:  (0.912569, 0.910734, 0.001835,       0.00,  9.01,  45_627.11,   408.37,
          620.61, 0.53,       0.00,     -46_665.63),
    36:  (0.911007, 0.909123, 0.001884,  98_698.00,  6.42,       0.00,   422.51,
          625.74, 0.33,   2_960.94,      94_682.06),
    192: (0.699318, 0.687606, 0.011712,  74_649.23, 28.35,       0.00, 1_905.39,
          546.67, 0.35,   2_239.48,      69_928.99),
    204: (0.685126, 0.672338, 0.012788,       0.00, 37.76,       0.00, 2_005.55,
          540.93, 0.43,       0.00,      -2_584.68),
    215: (0.672321, 0.659771, 0.012549,       0.00, 37.41, 470_609.46, 1_195.15,
          530.82, 0.43,       0.00,    -472_373.26),
    239: (0.645072, 0.633031, 0.012041,       0.00, 30.17,  64_504.36, 1_062.39,
          519.54, 0.56,       0.00,     -66_117.02),
    263: (0.618782, 0.607233, 0.011550,       0.00, 31.98,       0.00,     0.00,
          508.39, 0.64,       0.00,    -619_291.48),
}

# The child's rates at attained ages 0 .. 21, same table and same [std] interpolation.
EDU_Q = (
    0.00081, 0.00056, 0.00035, 0.00022, 0.00015, 0.00010, 0.00010, 0.00010,
    0.00010, 0.00010, 0.00010, 0.00012, 0.00014, 0.00016, 0.00019, 0.00023,
    0.00030, 0.00038, 0.00046, 0.00052, 0.00059, 0.00062,
)

EDU_TOTALS = {
    "premiums": 1_521_101.61,
    "claims_death": 3_988.78,
    "claims_staged": 771_160.39,
    "claims_maturity": 618_750.47,
    "claims_lapse": 308_128.19,
    "claims_ph_death": 0.00,
    "expenses": 201_918.51,
    "claim_expenses": 99.25,
    "commissions": 140_083.73,
    "net_cf": -523_027.70,
}

# The S型 grid the second cell runs: 5 / 5 / 10 / 10 / 70 / 10 percent of S, keyed by the
# ANNIVERSARY k, in years, that the payment falls on.  A payment at anniversary k falls at
# the end of the single month t = 12k - 1, which is the row of result_cf() that carries it.
EDU_SCHEDULE = {3: 0.05, 6: 0.05, 12: 0.10, 15: 0.10, 18: 0.70, 20: 0.10}


# ---------------------------------------------------------------------------
# The 養老 anchor cell


def test_the_anchor_cell_is_the_worked_examples_model_point(jp_endowment_anchor):
    """Model point 1 is the cell the notes' worked example projects.

    Male, 契約年齢 30 on a 満年齢 basis, 基準保険金額 ¥5,000,000, 保険期間 and 保険料払込期間 both 30
    years, annual premium ¥181,140 — twelve times a monthly premium published for exactly
    this cell.  No waiver, no loan, no APL, no dividend.
    """
    p = jp_endowment_anchor
    assert p.policy_id() == "EN-JP-0001"
    assert p.cell() == "endowment"
    assert (p.sex(), p.issue_age()) == ("M", 30)
    assert p.sum_assured() == 5_000_000.0
    assert (p.policy_term(), p.prem_term()) == (30, 30)
    assert p.premium_pp() == 181_140.0
    assert p.schedule_id() == "none"
    assert p.waiver() is False
    assert p.dividend_type() == "none"
    assert p.pol_loan_util() == 0.0 and p.apl_default_mult() == 0.0
    assert p.mort_be_factor() == 1.00 and p.wv_load() == 1.00
    assert p.wv_frac() == 1.00 and p.wv_lapse_mult() == 1.00


def test_the_anchor_cells_assumption_values(jp_endowment_anchor, endowment):
    """Every assumption the notes quote for the worked example, to the digits shown.

    ``i_cv`` is the published 予定利率 adopted directly; ``alpha`` = 0.25 of one annual
    premium, so the deduction at issue is ¥45,285; the surrender rates are 4 / 3 / 2
    percent **per annum** and zero in the final **month**; the expense and commission
    scale is inherited unchanged from the savings chassis.

    The rates are read at months here, not at policy years: ``lapse_rate(t)`` returns the
    annual rate applying in month ``t``, and ``lapse_rate_mth(t)`` is the monthly decrement
    derived from it.
    """
    p = jp_endowment_anchor
    assert endowment.Projection.i_cv == 0.01
    assert endowment.Projection.i_std == 0.01
    assert endowment.Projection.alpha == 0.25
    assert endowment.Projection.i_loan == 0.024
    assert endowment.Projection.expense_acq == 50_000.0
    assert endowment.Projection.expense_maint == 8_000.0
    assert endowment.Projection.expense_claim == 20_000.0
    assert endowment.Projection.inflation_rate == 0.01
    assert endowment.Projection.comm_init_rate == 0.90
    assert endowment.Projection.comm_renewal_rate == 0.03
    assert p.surr_charge_pp(0) == pytest.approx(45_285.0, abs=YEN)   # anniversary 0
    assert [p.lapse_rate(t) for t in (0, 12, 24, 348, 358, 359)] == [
        0.04, 0.03, 0.02, 0.02, 0.02, 0.0]
    # the conversion, stated as an identity rather than a constant
    for t in (0, 12, 24, 348):
        assert (1.0 - p.lapse_rate_mth(t)) ** 12 == pytest.approx(
            1.0 - p.lapse_rate(t), rel=1e-14)
        assert (1.0 - p.mort_rate_mth(t)) ** 12 == pytest.approx(
            1.0 - p.mort_rate(t), rel=1e-14)


def test_the_anchor_cells_mortality_vector(jp_endowment_anchor):
    """q at attained ages 30 .. 59, the notes' two rate tables.

    Not illustrative placeholders: every rate is either read from the published table at
    a quoted age or log-linearly interpolated between two rates that were.

    The table is read at ``age(t) = x + t // 12``, so the rate steps once a policy year
    and holds for the twelve months of it — which is asserted here rather than assumed,
    because a monthly grid that stepped the age monthly would be reading the table
    twelve times too fast.
    """
    p = jp_endowment_anchor
    for k, q in enumerate(ANCHOR_Q):
        assert p.age(12 * k) == 30 + k
        assert p.mort_rate(12 * k) == pytest.approx(q, abs=5e-9)
        for month in range(12):
            assert p.age(12 * k + month) == 30 + k
            assert p.mort_rate(12 * k + month) == pytest.approx(q, abs=5e-9)


def test_the_cash_value_construction_on_the_anchor_cell(jp_endowment_anchor):
    """A(30,30) = 0.74664983, ae(30,30) = 25.58836739, pi = ¥145,896.34.

    An endowment assurance carries the death benefit **inside** the EPV, so the net level
    premium is ``S x A(x, n) / a-due(x, m)``.  The implied loading of 19.451% of the gross
    premium is a derived output and not an input: the premium and the 予定利率 are sourced
    and the loading is what falls out.
    """
    p = jp_endowment_anchor
    assert p.endow_epv(30, 30, 0.01) == pytest.approx(0.74664983, abs=5e-9)
    assert p.annuity_due(30, 30, 0.01) == pytest.approx(25.58836739, abs=5e-9)
    assert p.prem_net_level_pp() == pytest.approx(145_896.34, abs=YEN)
    loading = p.premium_pp() - p.prem_net_level_pp()
    assert loading == pytest.approx(35_243.66, abs=YEN)
    assert loading / p.premium_pp() == pytest.approx(0.19457, abs=5e-6)


@pytest.mark.parametrize("k", sorted(ANCHOR_VALUES))
def test_the_anchor_cells_value_table(jp_endowment_anchor, k):
    """Every row of the notes' W / SC / CV table, and the ratio to cumulative premiums.

    Indexed by the anniversary ``k``, in **years**, not by the projection's month index:
    these are values *at a point in time*, ``k = 0`` at issue, and every literal here is
    unchanged from the annual model — the conversion moved the projection index and left
    the contractual construction alone.  The month-by-month reading ``cv_at_m(u)``
    reproduces this table exactly at ``u = 12k``, which its own test asserts.

    The last column never reaches 100%: this contract does not return its premiums even at
    maturity, which is the sourced constraint that the surrender value sits below
    cumulative premiums at every duration.
    """
    p = jp_endowment_anchor
    w, sc, cv, cum = ANCHOR_VALUES[k]
    assert p.pol_val_pp(k) == pytest.approx(w, abs=YEN)
    assert p.surr_charge_pp(k) == pytest.approx(sc, abs=YEN)
    assert p.cv_pp(k) == pytest.approx(cv, abs=YEN)
    assert p.prem_cum_pp(k) == cum
    assert p.cv_pp(k) < p.prem_cum_pp(k)
    assert p.cv_pp(30) / p.prem_cum_pp(30) == pytest.approx(0.920099, abs=5e-7)


@pytest.mark.parametrize("t", sorted(ANCHOR_CF))
def test_the_anchor_cells_worked_example_row(jp_endowment_anchor, t):
    """Every cell of the notes' cash flow table for the 養老 anchor cell, by month."""
    pols, prem, death, maturity, lapse, exp, cexp, comm, net = ANCHOR_CF[t]
    p = jp_endowment_anchor
    assert p.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert p.pols_if_pay(t) == pytest.approx(pols, abs=INFORCE)
    assert p.pols_wv(t) == 0.0
    assert p.premiums(t) == pytest.approx(prem, abs=YEN)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=YEN)
    assert p.claims(t, "STAGED") == 0.0
    assert p.claims(t, "MATURITY") == pytest.approx(maturity, abs=YEN)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse, abs=YEN)
    assert p.claims(t, "PH_DEATH") == 0.0
    assert p.expenses(t) == pytest.approx(exp, abs=YEN)
    assert p.claim_expenses(t) == pytest.approx(cexp, abs=YEN)
    assert p.commissions(t) == pytest.approx(comm, abs=YEN)
    assert p.net_cf(t) == pytest.approx(net, abs=YEN)


def test_the_anchor_cells_first_month_trace(jp_endowment_anchor):
    """The notes' first-month trace, line by line: ``t = 0``.

    q(0) = 0.00068 is the annual table rate and q_m(0) = 0.0000566843 the decrement
    actually applied; claims = 5,000,000 x D(0); claim expense = 20,000 x D(0);
    Sr(0) = (1 - q_m) x w_m; expenses = E0 + e(0) with e(0) a twelfth of the annual
    charge; commission = 0.90 x P, the whole 年払 premium falling in this one month.

    **The surrender benefit is nil, and that is the product rather than a rounding.**  At
    the end of the first month the interpolated value is ¥12,004.44 against a 解約控除 of
    ¥45,159.21, so ``CV`` floors at zero — the 約款's
    「ご契約後短期間で解約されたときには、解約返還金がない場合があります」 stated as a number, which the annual grid
    could not do because at the first *anniversary* the value has already outrun the
    deduction at ¥100,277.76.
    """
    p = jp_endowment_anchor
    assert p.mort_rate(0) == pytest.approx(0.00068, abs=1e-12)
    assert p.mort_rate_mth(0) == pytest.approx(0.0000566843, abs=5e-11)
    assert p.pols_death(0) == pytest.approx(0.0000566843, abs=5e-11)
    assert p.claim_expenses(0) == pytest.approx(1.13, abs=YEN)
    assert p.pols_surv(0) == pytest.approx(0.999943316, abs=1e-9)
    assert p.lapse_rate_mth(0) == pytest.approx(0.0033960532, abs=5e-11)
    assert p.pols_lapse(0) == pytest.approx(0.0033958607, abs=1e-9)
    assert p.pol_val_pre_at_m(1) == pytest.approx(12_004.44, abs=YEN)
    assert p.surr_charge_at_m(1) == pytest.approx(45_159.21, abs=YEN)
    assert p.cv_at_m(1) == 0.0
    assert p.claims(0, "LAPSE") == 0.0
    assert p.cv_pp(1) == pytest.approx(144_053.259234 - 43_775.50, abs=1e-5)
    assert min(u for u in range(1, 13) if p.cv_at_m(u) > 0.0) == 4
    assert p.expenses(0) == pytest.approx(50_000.00 + 8_000.00 / 12.0, abs=YEN)
    assert p.commissions(0) == pytest.approx(0.90 * 181_140.0, abs=YEN)
    assert p.net_cf(0) == pytest.approx(
        181_140.00 - 283.42 - 1.13 - 0.00 - 50_666.67 - 163_026.00, abs=YEN)
    assert p.pols_if_pay(1) == pytest.approx(0.996547455, abs=1e-9)


def test_the_anchor_cells_first_anniversary_trace(jp_endowment_anchor):
    """The notes' trace of the twelfth and thirteenth months, ``t = 11`` and ``t = 12``.

    Everything the 年払 premium does happens at ``t = 12``: the premium falls again, the
    renewal commission with it, the attained age steps to 31 and the surrender rate steps
    to 3%.  At ``t = 11`` — the month before — both money columns are **zero**, which is
    the shape of a 年払 contract and the thing the annual grid could not draw.

    Maintenance inflates once a policy year and is charged a twelfth at a time, so it
    steps at ``t = 12`` and not before.
    """
    p = jp_endowment_anchor
    assert p.premiums(11) == 0.0 and p.commissions(11) == 0.0
    assert p.maint_expenses(11) == pytest.approx(641.78, abs=YEN)
    assert p.mort_rate(11) == pytest.approx(0.00068, abs=5e-9)
    assert p.lapse_rate(11) == 0.04
    assert p.pols_death(11) == pytest.approx(0.0000545684, abs=5e-11)
    assert p.pols_surv(11) == pytest.approx(0.962616296, abs=1e-9)
    assert p.pols_lapse(11) == pytest.approx(0.003269096, abs=1e-9)
    assert p.pols_if_pay(12) == pytest.approx(0.959347200, abs=1e-9)

    assert p.premiums(12) == pytest.approx(173_776.15, abs=YEN)
    assert p.commissions(12) == pytest.approx(5_213.28, abs=YEN)
    assert p.commissions(12) == pytest.approx(0.03 * p.premiums(12), abs=YEN)
    assert p.age(12) == 31 and p.mort_rate(12) == pytest.approx(0.00069, abs=5e-9)
    assert p.lapse_rate(12) == 0.03
    assert p.maint_expenses(12) == pytest.approx(645.96, abs=YEN)
    assert p.maint_expenses(12) == pytest.approx(
        8_000.0 / 12.0 * 1.01 * p.pols_if(12), abs=YEN)
    assert p.pols_death(12) == pytest.approx(0.0000551799, abs=5e-11)
    assert p.pols_lapse(12) == pytest.approx(0.002431852, abs=1e-9)
    assert p.net_cf(12) == pytest.approx(167_366.24, abs=YEN)


def test_the_anchor_cells_maturity_month_trace(jp_endowment_anchor):
    """The notes' maturity-month trace: 0.494900998 of policies are paid ¥5,000,000.

    The 満期保険金 falls at anniversary 30, which is the close of the month 359, so it is
    **one month wide** rather than one year.  The surrender carve-out is that same single
    month: ``lapse_rate`` is zero at ``t = 359`` and 2% at ``t = 358``, so eleven months of
    ordinary surrender run inside the final policy year — which is why the maturing
    fraction is 0.4949 here where the annual grid said 0.5042.
    """
    p = jp_endowment_anchor
    assert p.pols_if_pay(359) == pytest.approx(0.495148426, abs=1e-9)
    assert p.mort_rate(359) == pytest.approx(0.00598, abs=5e-9)
    assert p.mort_rate_mth(359) == pytest.approx(0.000499704, abs=5e-10)
    assert p.pols_death(359) == pytest.approx(0.000247428, abs=1e-9)
    assert p.lapse_rate(359) == 0.0
    assert p.pols_lapse(359) == 0.0
    assert p.lapse_rate(358) == 0.02              # the eleven months before are ordinary
    assert p.pols_lapse(358) == pytest.approx(0.000834314, abs=1e-9)
    assert p.pols_surv(359) == pytest.approx(0.494900998, abs=1e-9)
    assert p.pols_maturity(359) == pytest.approx(0.494900998, abs=1e-9)
    assert p.pols_maturity(358) == 0.0
    assert p.claims(359, "MATURITY") == pytest.approx(2_474_504.99, abs=YEN)
    assert p.maint_expenses(359) == pytest.approx(440.52, abs=YEN)
    assert p.net_cf(359) == pytest.approx(-2_476_187.59, abs=YEN)
    assert p.net_cf(358) == pytest.approx(-5_844.16, abs=YEN)


def test_the_anchor_cells_undiscounted_totals(jp_endowment_anchor):
    """The notes' totals per policy issued, column by column.

    Undiscounted, the contract loses money; discounting is out of scope and is what makes
    the sign meaningful.  The expense total splits into maintenance, claim expense and the
    single acquisition charge exactly as the notes print it.
    """
    p = jp_endowment_anchor
    df = p.result_cf()
    for column, total in ANCHOR_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=YEN)
    n = p.proj_len()
    assert n == 360
    assert sum(p.maint_expenses(t) for t in range(n)) == pytest.approx(
        195_871.00, abs=YEN)
    assert sum(p.claim_expenses(t) for t in range(n)) == pytest.approx(
        855.37, abs=YEN)
    assert sum(p.acq_expenses(t) for t in range(n)) == pytest.approx(
        50_000.00, abs=YEN)
    # premium income is unchanged from the annual grid: the premium is 年払 and falls at
    # the same anniversaries on the same survivorship.
    assert sum(p.premiums(12 * k) for k in range(30)) == pytest.approx(
        3_931_162.67, abs=YEN)


def test_the_anchor_cells_roll_forward_sums_to_one(jp_endowment_anchor):
    """Every policy leaves by exactly one route, and half the block reaches maturity.

    Sum D + sum (1 - wv_frac) Dp + sum Sr + R(12n - 1) = 1, with l(12n) = h(12n) = 0.
    That 0.4949 of policies issued are still there at maturity is the structural
    difference from every protection product in this library.
    """
    p = jp_endowment_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    terms = sum(p.pols_ph_term(t) for t in range(n))
    assert deaths == pytest.approx(0.042768495, abs=5e-10)
    assert lapses == pytest.approx(0.462330508, abs=5e-10)
    assert terms == 0.0
    assert p.pols_maturity(n - 1) == pytest.approx(0.494900998, abs=5e-10)
    assert deaths + lapses + terms + p.pols_maturity(n - 1) == pytest.approx(
        1.0, abs=1e-12)
    assert p.pols_if_pay(n) == 0.0 and p.pols_wv(n) == 0.0


def test_the_anchor_cells_derived_ratios(jp_endowment_anchor):
    """henreiritsu = 92.0099% and the implied internal rate = -0.4239% p.a.

    The 返戻率 is the number the product is sold on and it is **not** a rate of return:
    restated as one, this cell's guaranteed cash flows imply a negative rate.  Both are
    derived diagnostics and neither is an input.
    """
    p = jp_endowment_anchor
    assert p.henreiritsu() == pytest.approx(0.920099, abs=5e-7)
    assert p.henreiritsu() == pytest.approx(5_000_000.0 / 5_434_200.0, rel=1e-12)
    assert p.implied_rate() == pytest.approx(-0.004239, abs=5e-7)
    assert p.implied_rate() < 0.01           # below i_cv, because the loading is positive


# ---------------------------------------------------------------------------
# The 学資 cell


def test_the_education_cell_is_the_worked_examples_second_cell(endowment):
    """Model point 2 is the 学資保険 cell of the same worked example.

    契約者 male 30, child 0, 22-year term, 17-year premium term, S型 grid, waiver written.
    The 基準保険金額 here is a **benefit-scaling unit and not a sum assured**: total premiums
    of ¥1,845,588 are 1.85 times it.
    """
    p = endowment.Projection[2]
    assert p.policy_id() == "EN-JP-0002"
    assert p.cell() == "education"
    assert (p.sex(), p.issue_age()) == ("M", 0)
    assert (p.ph_sex(), p.ph_issue_age()) == ("M", 30)
    assert p.sum_assured() == 1_000_000.0
    assert (p.policy_term(), p.prem_term()) == (22, 17)
    assert p.premium_pp() == 108_564.0
    assert p.premium_pp() * p.prem_term() == 1_845_588.0
    assert p.schedule_id() == "S_0_1"
    assert p.waiver() is True
    assert p.benefit_schedule() == EDU_SCHEDULE
    assert p.surr_charge_pp(0) == pytest.approx(27_141.0, abs=YEN)   # anniversary 0


def test_the_education_cells_two_mortality_vectors(endowment):
    """The child's rates at 0 .. 21 and the 契約者's at 30 .. 46, read at two ages.

    The 契約者 rates over ages 30-46 are the anchor cell's first seventeen, which is what
    makes reading one table at one age for both lives invisible on the anchor cell and
    visible here.
    """
    p = endowment.Projection[2]
    for k, q in enumerate(EDU_Q):
        assert p.age(12 * k) == k
        assert p.mort_rate(12 * k) == pytest.approx(q, abs=5e-9)
    for k in range(17):
        assert p.age_ph(12 * k) == 30 + k
        assert p.mort_rate_ph(12 * k) == pytest.approx(ANCHOR_Q[k], abs=5e-9)


def test_the_education_cells_negative_loading_is_published_not_hidden(endowment):
    """pi_g = ¥110,458.94 against a gross premium of ¥108,564: a -1.745% loading.

    No real product carries a net premium above its gross premium.  The number is an
    artefact of the composite's seam — this premium is one carrier's and the 予定利率 is
    another's — and it is a derived output printed beside its restatement as a rate, so
    that the seam is visible rather than smoothed away.
    """
    p = endowment.Projection[2]
    assert p.prem_net_level_pp() == pytest.approx(110_458.94, abs=YEN)
    loading = (p.premium_pp() - p.prem_net_level_pp()) / p.premium_pp()
    assert loading == pytest.approx(-0.017455, abs=5e-6)
    assert p.implied_rate() == pytest.approx(0.011592, abs=5e-7)
    assert p.implied_rate() > 0.01           # above i_cv, because the loading is negative


@pytest.mark.parametrize("t", sorted(EDU_CF))
def test_the_education_cells_worked_example_row(endowment, t):
    """Every cell of the notes' cash flow table for the 学資 cell, by month.

    ``claims_ph_death`` is zero in every month because ``wv_frac`` = 1.00, and
    ``claims_maturity`` is confined to the last month, ``t = 263``.
    """
    tot, pols, wv, prem, death, staged, lapse, exp, cexp, comm, net = EDU_CF[t]
    p = endowment.Projection[2]
    assert p.pols_if(t) == pytest.approx(tot, abs=INFORCE)
    assert p.pols_if_pay(t) == pytest.approx(pols, abs=INFORCE)
    assert p.pols_wv(t) == pytest.approx(wv, abs=INFORCE)
    assert p.pols_if(t) == pytest.approx(p.pols_if_pay(t) + p.pols_wv(t), rel=1e-14)
    assert p.premiums(t) == pytest.approx(prem, abs=YEN)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=YEN)
    assert p.claims(t, "STAGED") == pytest.approx(staged, abs=YEN)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse, abs=YEN)
    assert p.claims(t, "PH_DEATH") == 0.0
    assert p.expenses(t) == pytest.approx(exp, abs=YEN)
    assert p.claim_expenses(t) == pytest.approx(cexp, abs=YEN)
    assert p.commissions(t) == pytest.approx(comm, abs=YEN)
    assert p.net_cf(t) == pytest.approx(net, abs=YEN)
    assert p.claims(t, "MATURITY") == pytest.approx(
        618_750.47 if t == 263 else 0.0, abs=YEN)


def test_the_education_cells_first_month_trace(endowment):
    """The notes' first-month trace: two decrements out of one policy in ``t = 0``.

    D(0) reads the child's 0.00081 and Dp(0) the 契約者's 0.00068, both converted to the
    month, and all of the latter goes into the waived state because ``wv_frac`` = 1.00.

    **The death benefit's premium limb binds, and on the annual grid it never did.**  The
    whole 年払 premium of ¥108,564 has fallen by the end of the first month while the
    interpolated value has reached only ¥9,304.50, so the ``max`` takes the refund limb.
    At the first *anniversary* the value is ¥111,653.97 against the same one premium and
    the value limb binds instead — which is the only reading the annual grid could take.
    """
    p = endowment.Projection[2]
    assert p.mort_rate(0) == pytest.approx(0.00081, abs=1e-12)
    assert p.pols_death(0) == pytest.approx(0.0000675251, abs=5e-11)
    assert p.prem_cum_pp_m(1) == 108_564.0
    assert p.pol_val_pre_at_m(1) == pytest.approx(9_304.50, abs=YEN)
    assert p.death_ben_pp(0) == pytest.approx(108_564.0, abs=YEN)   # the premium limb
    assert p.pol_val_pre_pp(1) == pytest.approx(111_653.970487, abs=1e-5)
    assert p.death_ben_pp(11) == pytest.approx(111_653.970487, abs=1e-5)  # the value limb
    assert p.claim_expenses(0) == pytest.approx(1.35, abs=YEN)
    assert p.mort_rate_ph_mth(0) == pytest.approx(0.0000566843, abs=5e-11)
    assert p.pols_ph_decr(0) == pytest.approx(0.0000566805, abs=5e-11)
    assert p.pols_waived(0) == pytest.approx(0.0000566805, abs=5e-11)
    assert p.pols_ph_term(0) == 0.0
    assert p.pols_if_pay_at(0, "BEF_LAPSE") == pytest.approx(0.999875794, abs=1e-9)
    assert p.pols_wv_at(0, "BEF_LAPSE") == pytest.approx(0.0000566805, abs=5e-11)
    assert p.pols_surv(0) == pytest.approx(0.999932475, abs=1e-9)
    assert p.benefit_pct(1) == 0.0                # no 学資金 at the first anniversary
    assert p.pols_lapse(0) == pytest.approx(0.003395824, abs=1e-9)
    assert p.cv_at_m(1) == 0.0                    # the 解約控除 still exceeds the value
    assert p.cv_pp(1) == pytest.approx(86_109.499898, abs=1e-5)
    assert p.pols_if_pay(1) == pytest.approx(0.996480163, abs=1e-9)
    assert p.pols_wv(1) == pytest.approx(0.0000564880, abs=5e-11)


def test_the_education_cells_first_staged_benefit_trace(endowment):
    """The notes' trace of ``t = 35``, the one month the first 学資金 falls in.

    ``g(3)`` = 5% of S falls at anniversary 3, which is the close of the month 35, so the
    payment is **one month wide**: it is paid to everything in force in both states in
    that month and is zero in the other eleven months of policy year 3.  The death
    benefit's value limb binds at ¥338,386.30 over the cumulative-premium limb of
    ¥325,692.00, and the surrender value is computed on the value *after* the payment.
    """
    p = endowment.Projection[2]
    assert p.benefit_pct(3) == 0.05
    assert p.pols_death(35) == pytest.approx(0.0000266209, abs=5e-11)
    assert p.pol_val_pre_at_m(36) == pytest.approx(338_386.301776, abs=1e-5)
    assert p.pol_val_pre_pp(3) == pytest.approx(338_386.301776, abs=1e-5)
    assert p.prem_cum_pp(3) == 325_692.0
    assert p.prem_cum_pp_m(36) == 325_692.0
    assert p.death_ben_pp(35) == pytest.approx(338_386.30, abs=YEN)
    assert p.pols_ph_decr(35) == pytest.approx(0.0000531417, abs=5e-11)
    assert p.pols_surv(35) == pytest.approx(0.912542247, abs=1e-9)
    assert p.claims(35, "STAGED") == pytest.approx(45_627.11, abs=YEN)
    # and nowhere else in the policy year
    assert [t for t in range(24, 36) if p.claims(t, "STAGED") > 0.0] == [35]
    assert p.pol_val_pp(3) == pytest.approx(288_386.301776, abs=1e-5)
    assert p.cv_pp(3) == pytest.approx(266_034.890011, abs=1e-5)
    assert p.pols_lapse(35) == pytest.approx(0.001535026, abs=1e-9)


def test_the_education_cells_seventy_percent_payment_trace(endowment):
    """The notes' trace of ``t = 215``: the 70% payment, and the months after 払込満了.

    No premium and therefore no renewal commission from ``t = 12m`` = 204 on;
    ``q_p`` is zero from that month, so ``pols_wv`` peaks there and then runs off on child
    mortality and surrender alone; and the surrender value falls by exactly the ¥700,000
    paid at anniversary 18.
    """
    p = endowment.Projection[2]
    assert p.premiums(204) == 0.0 and p.commissions(204) == 0.0
    assert p.premiums(192) == pytest.approx(74_649.23, abs=YEN)   # the last one
    assert p.mort_rate_ph(203) == pytest.approx(0.00195, abs=5e-9)
    assert p.mort_rate_ph(204) == 0.0
    assert p.pols_ph_decr(215) == 0.0
    assert p.pols_wv(204) > p.pols_wv(203)        # the last transition still arrived
    assert p.pols_wv(205) < p.pols_wv(204)        # and it now runs off
    assert p.pols_if_pay_at(215, "BEF_LAPSE") == pytest.approx(0.659750480, abs=1e-9)
    assert p.pols_death(215) == pytest.approx(0.0000212939, abs=5e-11)
    assert p.pol_val_pre_at_m(216) == pytest.approx(1_756_811.077206, abs=1e-5)
    assert p.death_ben_pp(215) == pytest.approx(1_756_811.08, abs=YEN)
    assert p.pols_surv(215) == pytest.approx(0.672299224, abs=1e-9)
    assert p.claims(215, "STAGED") == pytest.approx(470_609.46, abs=YEN)
    assert [t for t in range(204, 216) if p.claims(t, "STAGED") > 0.0] == [215]
    assert p.cv_pp(17) == pytest.approx(1_738_755.93, abs=YEN)
    assert p.cv_pp(18) == pytest.approx(1_056_811.08, abs=YEN)
    assert p.net_cf(215) == pytest.approx(-472_373.26, abs=YEN)


def test_the_education_cells_undiscounted_totals(endowment):
    """The notes' totals per policy issued for the second cell, column by column."""
    df = endowment.Projection[2].result_cf()
    for column, total in EDU_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=YEN)


def test_the_education_cells_roll_forward_sums_to_one(endowment):
    """Sum D + sum Sr + R(263) = 1, with nothing terminated by a refused waiver."""
    p = endowment.Projection[2]
    n = p.proj_len()
    assert n == 264
    deaths = sum(p.pols_death(t) for t in range(n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    terms = sum(p.pols_ph_term(t) for t in range(n))
    assert deaths == pytest.approx(0.004962269, abs=5e-10)
    assert lapses == pytest.approx(0.376287258, abs=5e-10)
    assert terms == 0.0
    assert p.pols_maturity(n - 1) == pytest.approx(0.618750473, abs=5e-10)
    assert deaths + lapses + terms + p.pols_maturity(n - 1) == pytest.approx(
        1.0, abs=1e-12)


def test_the_education_cells_derived_ratio_matches_the_published_one(endowment):
    """henreiritsu = 113.7849% against the "approx. 113.7%" published for this plan.

    The carrier truncates where the model rounds, which is the whole of the difference.
    """
    p = endowment.Projection[2]
    assert p.henreiritsu() == pytest.approx(0.1137849e1, abs=5e-7)
    assert p.henreiritsu() == pytest.approx(2_100_000.0 / 1_845_588.0, rel=1e-12)
    assert 1.137 <= p.henreiritsu() < 1.138


def test_what_the_waiver_is_worth_on_the_education_cell(endowment):
    """1.861464% cumulative entry probability against an EPV of ¥11,384.94 of premium.

    Small probability, large amount, running off on a different schedule from every other
    cash flow in the model — the shape of error that survives a sensibility check on the
    base case.  The amount at risk starts at ¥1,845,588, which is 1.85 times the 満期保険金
    the contract will pay, and reaches zero at anniversary ``m`` while maturity is still
    five years away.
    """
    p = endowment.Projection[2]
    m_, prem, v = p.prem_term(), p.premium_pp(), 1.0 / 1.01

    # An annual calculation on an annual quantity: what the waiver is worth is the value
    # of premiums not paid, and premiums fall once a year.  The rates are read at the
    # anniversary months, ``mort_rate(12k)``, so this is the same arithmetic the annual
    # grid ran and the same answer it gave.
    entered, paying, waived, epv = 0.0, 1.0, 0.0, 0.0
    for k in range(m_):
        q, qp = p.mort_rate(12 * k), p.mort_rate_ph(12 * k)
        epv += prem * v ** k * waived
        decr = paying * (1.0 - q) * qp
        entered += decr
        waived = waived * (1.0 - q) + decr
        paying = paying * (1.0 - q) * (1.0 - qp)

    assert entered == pytest.approx(0.01861464, abs=5e-9)
    assert epv == pytest.approx(11_384.94, abs=YEN)
    prem_epv = prem * p.annuity_due(0, m_, 0.01)
    assert prem_epv == pytest.approx(1_702_626.54, abs=YEN)
    assert epv / prem_epv == pytest.approx(0.006687, abs=5e-7)
    assert prem * (m_ - 0) == 1_845_588.0
    assert prem * (m_ - m_) == 0.0


# ---------------------------------------------------------------------------
# The conversion to the monthly grid


def test_the_conversion_preserves_anniversary_survivorship(endowment):
    """(1 - r_m)^12 = 1 - r, so twelve months compound back to the annual rate exactly.

    This is the hook the whole conversion hangs on.  Mortality and surrender are quoted
    per annum in the input tables and applied per month on the **effective** convention
    ``r_m = 1 - (1 - r)^(1/12)``, so the in-force ladder at the anniversaries is the one
    the annual model produced and every anniversary reading of it — the surrender values,
    the policy value, the roll-forward at each anniversary — is unchanged.

    What is NOT converted is the premium-default proportion: it is the failure to pay one
    premium on one date, not a hazard per unit time, so it is applied once per premium.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        for t in range(0, p.proj_len(), 12):
            assert (1.0 - p.mort_rate_mth(t)) ** 12 == pytest.approx(
                1.0 - p.mort_rate(t), rel=1e-14)
            assert (1.0 - p.mort_rate_ph_mth(t)) ** 12 == pytest.approx(
                1.0 - p.mort_rate_ph(t), rel=1e-14)
            if p.lapse_rate(t) > 0.0:
                assert (1.0 - p.lapse_rate_mth(t)) ** 12 == pytest.approx(
                    1.0 - p.lapse_rate(t), rel=1e-14)

    # Twelve months of the monthly recursion reproduce one year of the annual one, on a
    # cell with no waiver and therefore one state.
    anchor = endowment.Projection[1]
    ladder, l = [1.0], 1.0
    for k in range(30):
        q, w = anchor.mort_rate(12 * k), anchor.lapse_rate(12 * k)
        if k == 29:                                # the final-month carve-out
            break
        l = l * (1.0 - q) * (1.0 - w)
        ladder.append(l)
    for k, expected in enumerate(ladder):
        assert anchor.pols_if(12 * k) == pytest.approx(expected, abs=5e-9)


def test_the_value_readings_agree_with_the_anniversaries_they_interpolate(endowment):
    """Every ``*_at_m(u)`` cells returns its anniversary value exactly at ``u = 12k``.

    The contractual constructions stayed annual — they are defined at the 年単位の契約応当日
    and the 算出方法書 that would give the within-year rule is unpublished — so the monthly
    grid reads them by linear interpolation **[std]** and must agree with them wherever
    they are both defined.  Between anniversaries the interpolation runs from the value
    *after* the staged benefit at one to the value *before* the one at the next, which is
    the curve the contract traces.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        for k in range(p.policy_term() + 1):
            assert p.pol_val_at_m(12 * k) == pytest.approx(p.pol_val_pp(k), abs=1e-6)
            assert p.pol_val_pre_at_m(12 * k) == pytest.approx(
                p.pol_val_pre_pp(k), abs=1e-6)
            assert p.surr_charge_at_m(12 * k) == pytest.approx(
                p.surr_charge_pp(k), abs=1e-6)
            assert p.cv_at_m(12 * k) == pytest.approx(p.cv_pp(k), abs=1e-6)
        # and it is monotone between them, so no month reads a value the contract never
        # passes through
        edu = p.cell() == "education"
        for k in range(p.policy_term()):
            run = [p.pol_val_pre_at_m(12 * k + j) for j in range(1, 13)]
            assert run == sorted(run), (point_id, k)
            assert edu or p.cv_at_m(12 * k + 12) >= p.cv_at_m(12 * k)


def test_the_premium_stream_is_unchanged_by_the_grid(endowment):
    """The premium is 年払, so it falls at the same anniversaries on the same survivorship.

    That premium income is identical to the annual model's is the second half of the
    conversion's claim: the first is that survivorship at the anniversaries did not move,
    and this follows from it.  What the monthly grid changed is the **shape** of the
    statement — one large inflow a year against expense and claims every month — not the
    total.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        df = p.result_cf()
        annual = sum(p.premiums(12 * k) for k in range(p.prem_term()))
        assert df["premiums"].sum() == pytest.approx(annual, rel=1e-14)
        # exactly one premium month in twelve, and none after 払込満了
        months = [t for t in range(p.proj_len()) if p.premiums(t) > 0.0]
        assert months == [12 * k for k in range(p.prem_term())]
        assert all(p.commissions(t) == 0.0
                   for t in range(1, p.proj_len()) if t % 12 != 0)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test each, named after the pitfall


def test_the_maturity_benefit_is_certain_not_a_decrement(endowment):
    """In the last month the survivors are paid S with probability 1, and nothing runs on.

    Modelling maturity as a rate, or letting the projection run past ``t = 12n - 1`` on a
    terminal age imported from the whole life chassis, is wrong in both directions.  There
    is no ``omega_age`` here and no state at or after ``proj_len()``.

    On this grid the payment is **one month wide**: it falls in the single month whose
    closing instant is the anniversary ``n``, not across the whole final policy year.
    """
    names = set(endowment.Projection.cells) | set(endowment.Projection.refs)
    for absent in ("omega_age", "terminal_age", "maturity_rate", "pols_if_init"):
        assert absent not in names, f"{absent} is whole life chassis tail machinery"
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        n = p.proj_len()
        assert n == 12 * p.policy_term()
        assert len(p.result_cf()) == n
        assert all(p.pols_maturity(t) == 0.0 for t in range(n - 1))
        assert p.pols_maturity(n - 1) == pytest.approx(p.pols_surv(n - 1), rel=1e-14)
        assert p.claims(n - 1, "MATURITY") == pytest.approx(
            p.sum_assured() * p.pols_surv(n - 1), rel=1e-12)
        assert p.pols_if_pay(n) == 0.0 and p.pols_wv(n) == 0.0


def test_lapse_rate_is_zero_in_the_final_month_and_only_in_it(endowment):
    """A surrender at the close of the last month and the maturity payment collide.

    Running both double-counts the terminal payment; running the surrender instead of the
    maturity misclassifies most of the anchor cell's outgo into the wrong column.  The
    zero is a modelling ruling, not a rounding of a small number: the table rate for that
    policy year is 2%.

    **The carve-out is one month, not one policy year**, and that is the conversion's
    largest single effect on this product.  The eleven months before the last one carry
    the ordinary 2%, so genuine surrender runs inside the final policy year and the
    anchor cell's maturing fraction is 0.4949 where the annual grid said 0.5042.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        n = p.proj_len()
        assert p.lapse_rate_base(n - 1) > 0.0    # the table would have given 2%
        assert p.lapse_rate(n - 1) == 0.0
        assert p.pols_lapse(n - 1) == 0.0
        assert p.claims(n - 1, "LAPSE") == 0.0
        # only that one month, not the twelve of the final policy year
        for t in range(n - 12, n - 1):
            assert p.lapse_rate(t) > 0.0
            assert p.pols_lapse(t) > 0.0
    anchor = endowment.Projection[1]
    assert anchor.cv_pp(30) == anchor.sum_assured()      # anniversary 30
    assert anchor.claims(359, "MATURITY") / abs(anchor.net_cf(359)) > 0.9
    assert anchor.pols_maturity(359) == pytest.approx(0.494900998, abs=5e-10)


def test_the_policy_value_converges_on_the_maturity_benefit(endowment):
    """pol_val_pp(n) == sum_assured exactly, on both cells and on every model point.

    ``n`` here is the closing anniversary in **years**, which is the close of the last
    month ``t = 12n - 1``.
    The identity that makes an endowment a real test of a savings model: a whole life
    reserve that drifts can hide for decades, while an endowment reserve that does not
    converge on its own maturity benefit is wrong on the first run.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        n = p.policy_term()                       # the anniversary, in years
        assert p.check_pol_val_terminal() is True
        assert p.pol_val_pp(n) == pytest.approx(p.sum_assured(), abs=1e-6)
        assert p.pol_val_pre_pp(n) == pytest.approx(p.sum_assured(), abs=1e-6)
        assert p.check_pol_val_terminal_resid(n) == pytest.approx(0.0, abs=1e-6)
        assert all(p.check_pol_val_terminal_resid(k) == 0.0 for k in range(n))
        # and the month-by-month reading lands on it too
        assert p.pol_val_at_m(12 * n) == pytest.approx(p.sum_assured(), abs=1e-6)


def test_two_lives_two_decrements_one_policy(endowment):
    """The waiver runs on the 契約者's age; every benefit runs on the 被保険者's.

    Reading one table at one age for both is the most likely implementation error on this
    product, and on the anchor cell the two ages coincide so it would not show there.  On
    the education cell the child is 0 and the 契約者 is 30, and the two decrements differ by
    a factor of five in the first year.
    """
    p = endowment.Projection[2]
    for k in (0, 4, 9, 16):
        t = 12 * k
        assert p.age(t) == k
        assert p.age_ph(t) == 30 + k
        assert p.age(t) != p.age_ph(t)
        assert p.mort_rate(t) == pytest.approx(
            p.mort_rate_at_age("M", k), rel=1e-14)
        assert p.mort_rate_ph(t) == pytest.approx(
            p.mort_rate_at_age("M", 30 + k), rel=1e-14)
    assert p.mort_rate(48) == 0.00015 and p.mort_rate_ph(48) == 0.00074
    # The child decrement runs on both states; the 契約者 decrement on the paying one only.
    # Both are applied per month, on the converted rates.
    for t in (48, 137, 199):
        assert p.pols_death(t) == pytest.approx(
            p.pols_if(t) * p.mort_rate_mth(t), rel=1e-14)
        assert p.pols_ph_decr(t) == pytest.approx(
            p.pols_if_pay(t) * (1 - p.mort_rate_mth(t)) * p.mort_rate_ph_mth(t),
            rel=1e-14)
    # On the endowment cell there is no second life at all, and asking for one raises.
    anchor = endowment.Projection[1]
    assert all(anchor.mort_rate_ph(t) == 0.0 for t in range(anchor.proj_len()))
    assert all(anchor.mort_rate_ph_mth(t) == 0.0 for t in range(anchor.proj_len()))
    assert all(anchor.pols_wv(t) == 0.0 for t in range(anchor.proj_len() + 1))
    with pytest.raises(FormulaError):
        anchor.ph_issue_age()
    with pytest.raises(FormulaError):
        anchor.ph_sex()


def test_the_policyholder_decrement_stops_at_the_premium_term(endowment):
    """q_p(t) = 0 from t = 12m on: after 払込満了 there is no premium to waive.

    The premium-paying months are ``t = 0 .. 12m - 1``.  Every waiver trigger is
    conditional on the event falling during 保険料払込期間, so the composite treats the
    contract as continuing through the 契約者's death by succession.  Carrying the
    decrement through the months 204 to 263 would move a further 0.8250% of policies out
    of the premium-paying state — and, wherever ``wv_frac < 1``, terminate a share of them
    and delete their maturity benefits — in exactly the years in which 86% of this cell's
    receipts fall.
    """
    p = endowment.Projection[2]
    m_, n = p.prem_term(), p.proj_len()
    assert m_ == 17 and n == 264
    assert p.mort_rate_ph(12 * m_ - 1) > 0.0
    assert all(p.mort_rate_ph(t) == 0.0 for t in range(12 * m_, n))
    assert all(p.mort_rate_ph_mth(t) == 0.0 for t in range(12 * m_, n))
    assert all(p.pols_ph_decr(t) == 0.0 for t in range(12 * m_, n))

    # The counterfactual, run as a recursion rather than as a sum against the base
    # in-force: a policy moved out of the paying state in one month is not there to be
    # moved again in the next.
    lp, hh, dropped = 1.0, 0.0, 0.0
    for t in range(n):
        qm = p.mort_rate_mth(t)
        qpm = (p.mort_rate_ph_mth(t) if t < 12 * m_ else
               1.0 - (1.0 - p.mort_rate_at_age("M", 30 + t // 12)) ** (1.0 / 12.0))
        decr = lp * (1.0 - qm) * qpm
        if t >= 12 * m_:
            dropped += decr
        lp_after = lp * (1.0 - qm) * (1.0 - qpm)
        h_after = hh * (1.0 - qm) + p.wv_frac() * decr
        wm = p.lapse_rate_mth(t)
        lp = lp_after * (1.0 - wm)
        hh = h_after * (1.0 - min(1.0, p.wv_lapse_mult() * wm))
    assert dropped == pytest.approx(0.008250, abs=5e-7)


def test_the_waiver_produces_no_benefit_outgo(endowment, tmp_path):
    """Switching the waiver off changes premium income and no claim column at all.

    The waiver is a **state transition, not a benefit**: booking a "waiver benefit"
    double-counts, and because omitting the waiver altogether leaves every claim column
    unchanged, neither error is visible in a benefit reconciliation.  Only a comparison of
    the premium line finds it — here, ¥9,833.17 of premium income that a waived block does
    not pay.
    """
    model = variant_model(tmp_path, {90: (2, {"policy_id": "EN-JP-NOWV",
                                              "waiver": False})},
                          "Endowment_JP_S_nowv")
    try:
        off = model.Projection[90]
        assert off.waiver() is False
        on = endowment.Projection[2]
        a, b = on.result_cf(), off.result_cf()
        for column in ("claims_death", "claims_staged", "claims_maturity",
                       "claims_lapse", "claims_ph_death", "expenses",
                       "claim_expenses"):
            assert (a[column] - b[column]).abs().max() == pytest.approx(0.0, abs=1e-6)
        # The two states together are the same block; only the split moves.  That is
        # exactly what pols_if publishes, so the total column is bit-identical.
        assert (a["pols_if"] - b["pols_if"]).abs().max() == pytest.approx(0.0, abs=1e-12)
        assert ((a["pols_if_pay"] + a["pols_wv"]) - a["pols_if"]
                ).abs().max() == pytest.approx(0.0, abs=1e-12)
        assert (a["pols_wv"] > 0).any() and (b["pols_wv"] == 0.0).all()
        assert b["premiums"].sum() - a["premiums"].sum() == pytest.approx(
            9_833.17, abs=YEN)
        assert b["commissions"].sum() > a["commissions"].sum()
    finally:
        model.close()


def test_premiums_on_a_waived_policy_are_deemed_paid(endowment):
    """prem_cum_pp keeps growing on a policy that pays nothing, and CV is one series.

    The contract provides that each future premium is treated as having been paid on its
    契約応当日, so the return-of-premiums death benefit keeps growing and the surrender value
    is the same in both states.  Netting the waived premiums out of either understates
    both, and a model that carries two value series is modelling a contract nobody wrote.
    """
    p = endowment.Projection[2]
    for k in range(1, p.prem_term() + 1):          # k is the anniversary, in years
        assert p.prem_cum_pp(k) == 108_564.0 * k
        # the elapsed-month reading is a step function of the premiums actually due
        assert p.prem_cum_pp_m(12 * k) == 108_564.0 * k
        assert p.prem_cum_pp_m(12 * k - 11) == 108_564.0 * k
    for k in range(p.prem_term(), p.policy_term() + 1):
        assert p.prem_cum_pp(k) == 1_845_588.0        # capped at m, never at cash paid
    # The refund limb at anniversary 18 counts every premium due, including those of the
    # 1.28% of the block sitting in the waived state that paid nothing.
    assert p.pols_wv(204) > 0.0
    assert p.prem_cum_pp(18) - p.sum_assured() * p.benefit_pct_cum(17) == pytest.approx(
        1_545_588.0, abs=1e-6)
    assert p.prem_cum_pp_m(216) == 1_845_588.0     # the same cap, read at a month
    # There is exactly one value series and one surrender value series.
    names = set(endowment.Projection.cells)
    assert "cv_pp" in names and "av_pp" not in names
    assert not [n for n in names if n.startswith(("cv_wv", "pol_val_wv"))]
    # Cash actually collected is well below cash deemed paid.
    assert p.result_cf()["premiums"].sum() < p.prem_cum_pp(p.prem_term())


def test_severe_disability_is_inside_the_death_rate_but_accident_disability_is_not(
        endowment):
    """One lever, pointing two ways: no extra decrement on the insured, wv_load on the 契約者.

    生保標準生命表2018（死亡保険用）already includes 高度障害, so a separate disability decrement on
    the 被保険者 double-counts and there is none in the model.  The waiver's **third**
    trigger, 身体障害 from a listed accident within 180 days, is genuinely additional and is
    not in the table, so holding ``wv_load`` at 1.00 *understates* the waiver.  The two
    cases point opposite ways and confusing them is the pitfall.
    """
    names = set(endowment.Projection.cells) | set(endowment.Projection.refs)
    assert not [n for n in names if n.startswith(("disab", "tpd_", "ci_"))]
    assert "wv_load" in names
    p = endowment.Projection[2]
    assert p.wv_load() == 1.00
    # The insured decrement is the table rate exactly: nothing is added for 高度障害.
    for k in (0, 7, 19):
        assert p.mort_rate(12 * k) == pytest.approx(
            p.mort_rate_at_age("M", k), rel=1e-14)
    # wv_load moves the 契約者 decrement and nothing else.  Point 4 runs it at 1.50.
    loaded = endowment.Projection[4]
    assert loaded.wv_load() == 1.50
    for k in (0, 7, 16):
        assert loaded.mort_rate_ph(12 * k) == pytest.approx(
            1.50 * p.mort_rate_at_age("M", 30 + k), rel=1e-14)


def test_a_waiver_carve_out_terminates_the_contract(endowment):
    """The complement of wv_frac is not "no waiver" but termination against the 責任準備金.

    Three-year suicide of the 契約者, the 後継保険契約者's intentional act and war each end the
    policy, paying the value to the 契約者's legal heirs.  ``claims_ph_death`` is a column
    of zeros in the base run — the zero being the product fact, published rather than
    dropped — and it must become non-zero as soon as ``wv_frac < 1``.
    """
    base = endowment.Projection[2]
    assert base.wv_frac() == 1.00
    assert (base.result_cf()["claims_ph_death"] == 0.0).all()
    assert all(base.pols_ph_term(t) == 0.0 for t in range(base.proj_len()))
    assert "claims_ph_death" in base.result_cf().columns

    carve = endowment.Projection[4]
    assert carve.wv_frac() == 0.90
    df = carve.result_cf()
    assert (df["claims_ph_death"] > 0.0).any()
    assert df["claims_ph_death"].sum() == pytest.approx(2_219.84, abs=YEN)
    for t in (0, 48, 199):
        assert carve.pols_ph_term(t) == pytest.approx(
            0.10 * carve.pols_ph_decr(t), rel=1e-14)
        assert carve.pols_waived(t) == pytest.approx(
            0.90 * carve.pols_ph_decr(t), rel=1e-14)
        # It pays the value *before* the staged benefit, read at the close of the month,
        # to the heirs.
        assert carve.claims(t, "PH_DEATH") == pytest.approx(
            carve.pol_val_pre_at_m(t + 1) * carve.pols_ph_term(t), rel=1e-12)
    assert carve.check_pols_roll_fwd() is True    # the terminations close the identity


def test_the_staged_benefit_is_not_a_claim_and_not_a_decrement(endowment):
    """S g(k) R(12k-1): paid on survival to all in force, in both states, terminating nothing.

    The payment due at anniversary ``k`` is the staged claim of the **single month**
    ``t = 12k - 1``, and is zero in the other eleven months of that policy year.
    Weighting it by a decrement rate, or paying it only from the premium-paying state,
    understates it.  The in-force roll-forward must not see it at all.
    """
    p = endowment.Projection[2]
    for k, g in EDU_SCHEDULE.items():
        t = 12 * k - 1                             # the one month that carries it
        assert all(p.claims(u, "STAGED") == 0.0 for u in range(t - 11, t))
        assert p.benefit_pct(k) == g
        assert p.claims(t, "STAGED") == pytest.approx(
            p.sum_assured() * g * p.pols_surv(t), rel=1e-12)
        # It is paid to the waived state too, which is a strictly larger population than
        # the paying state alone.
        assert p.pols_wv_at(t, "BEF_LAPSE") > 0.0
        assert p.claims(t, "STAGED") > (
            p.sum_assured() * g * p.pols_if_pay_at(t, "BEF_LAPSE"))
        # And it terminates nothing: the roll-forward in that period has no staged term.
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
    assert all(p.benefit_pct(k) == 0.0 for k in range(23) if k not in EDU_SCHEDULE)
    assert p.benefit_pct_cum(17) == pytest.approx(0.30, rel=1e-12)
    assert p.benefit_pct_cum(18) == pytest.approx(1.00, rel=1e-12)
    assert p.benefit_pct_cum(22) == pytest.approx(1.10, rel=1e-12)


def test_each_staged_benefit_reduces_the_surrender_value_by_its_own_amount(endowment):
    """Wb(k) - W(k) = S g(k): the payment comes out of the value, not beside it.

    One carrier computes the surrender value from the elapsed months **and** the 学資金
    timing, and each 祝金 reduces it.  A model that pays the benefit beside the value
    inflates every later surrender; on this cell the value falls from ¥1,738,755.93 to
    ¥1,056,811.08 across the 70% payment.
    """
    p = endowment.Projection[2]
    assert p.check_staged_value() is True
    for k in range(p.policy_term() + 1):           # k is the anniversary, in years
        assert p.check_staged_value_resid(k) == pytest.approx(0.0, abs=1e-6)
        assert p.pol_val_pre_pp(k) - p.pol_val_pp(k) == pytest.approx(
            p.sum_assured() * p.benefit_pct(k), abs=1e-6)
        # and the elapsed-month reading agrees with the anniversary exactly
        assert p.pol_val_pre_at_m(12 * k) == pytest.approx(
            p.pol_val_pre_pp(k), abs=1e-6)
        assert p.cv_at_m(12 * k) == pytest.approx(p.cv_pp(k), abs=1e-6)
    assert p.cv_pp(17) - p.cv_pp(18) == pytest.approx(681_944.85, abs=1.0)
    assert p.pol_val_pre_pp(18) - p.pol_val_pp(18) == pytest.approx(700_000.0, abs=1e-6)
    # On the endowment cell the two series are the same, because g is identically zero.
    anchor = endowment.Projection[1]
    assert all(anchor.pol_val_pre_pp(k) == anchor.pol_val_pp(k)
               for k in range(anchor.policy_term() + 1))


def test_the_staged_schedule_is_data(endowment):
    """The J grid — one payment of 100%, then maturity — runs without touching the code.

    Observed designs run from a single 100% payment to four payments of 100% each, so an
    implementation that hard-codes a shape is modelling one carrier.  The 満期保険金 is never
    a schedule row: it is always present on both cells and held separately, so a schedule
    with no rows at all still matures.
    """
    j = endowment.Projection[3]
    assert j.schedule_id() == "J"
    assert j.benefit_schedule() == {18: 1.00}      # anniversary 18 = the month t = 215
    assert j.claims(215, "STAGED") == pytest.approx(
        j.sum_assured() * j.pols_surv(215), rel=1e-12)
    assert all(j.claims(t, "STAGED") == 0.0 for t in range(264) if t != 215)
    assert j.claims(263, "MATURITY") == pytest.approx(618_750.47, abs=YEN)
    assert j.henreiritsu() == pytest.approx(2_000_000.0 / 1_845_588.0, rel=1e-12)
    assert j.check_pol_val_terminal() is True

    # schedule_id "none" is a product fact, not a missing value: no rows, still matures.
    anchor = endowment.Projection[1]
    assert anchor.schedule_id() == "none"
    assert anchor.benefit_schedule() == {}
    assert anchor.claims(359, "MATURITY") > 0.0


def test_both_limbs_of_the_education_death_benefit_are_evaluated(endowment, tmp_path):
    """max(deemed-paid premiums less staged benefits less loans, Wb(t+1)), and it switches.

    **On the monthly grid both limbs bind on the shipped cell.**  The annual grid read the
    benefit only at anniversaries, where the value limb dominated at every duration and
    the ``max`` never switched.  Read month by month it switches 85 times in 264: the
    premium limb steps up by a whole 年払 premium in each anniversary month and the value
    accretes through the year to overtake it, so the refund limb binds early in each
    policy year and the value limb late in it, until the value pulls clear for good after
    the first month of policy year 12.  Hard-coding either limb is right eleven months a
    year at best.
    """
    p = endowment.Projection[2]
    refund_months = []
    for t in range(p.proj_len()):
        refund = (p.prem_cum_pp_m(t + 1)
                  - p.sum_assured() * p.benefit_pct_cum(p.duration(t)))
        assert p.death_ben_pp(t) == pytest.approx(
            max(refund, p.pol_val_pre_at_m(t + 1)), rel=1e-12)
        if refund > p.pol_val_pre_at_m(t + 1):
            refund_months.append(t)
    assert len(refund_months) == 85
    assert refund_months[:3] == [0, 1, 2]          # the premium limb, from the first month
    assert max(refund_months) == 132               # policy year 12, and never again
    # at every anniversary the value limb binds, which is all the annual grid could see
    assert all(p.death_ben_pp(12 * k - 1) == pytest.approx(
        p.pol_val_pre_pp(k), rel=1e-12) for k in range(1, 23))

    model = variant_model(tmp_path, {90: (2, {"policy_id": "EN-JP-GROSS",
                                              "premium_annual": 150000})},
                          "Endowment_JP_S_limb")
    try:
        loaded = model.Projection[90]
        assert loaded.premium_pp() > loaded.prem_net_level_pp()   # a positive loading now
        for t in range(loaded.proj_len()):
            refund = (loaded.prem_cum_pp_m(t + 1)
                      - loaded.sum_assured()
                      * loaded.benefit_pct_cum(loaded.duration(t)))
            assert loaded.death_ben_pp(t) == pytest.approx(refund, rel=1e-12)
            assert refund > loaded.pol_val_pre_at_m(t + 1)
    finally:
        model.close()

    # And on the endowment cell the benefit is the sum assured net of loans, not a refund.
    anchor = endowment.Projection[1]
    assert all(anchor.death_ben_pp(t) == 5_000_000.0
               for t in range(anchor.proj_len()))


def test_henreiritsu_is_a_contractual_ratio_not_a_model_output_ratio(endowment):
    """It reads P x m and the scheduled benefits, never the projected cash flows.

    It is undefined on a policy that surrenders and unbounded on one that is waived, which
    is why the denominator is the contractual premium term.  It is not probability
    weighted, not discounted and not net of expenses, so it is emphatically not the ratio
    the cash flow statement produces.
    """
    for point_id in (1, 2, 3):
        p = endowment.Projection[point_id]
        contractual = (p.sum_assured() * (sum(p.benefit_schedule().values()) + 1.0)
                       / (p.premium_pp() * p.prem_term()))
        assert p.henreiritsu() == pytest.approx(contractual, rel=1e-14)
        df = p.result_cf()
        projected = ((df["claims_staged"].sum() + df["claims_maturity"].sum())
                     / df["premiums"].sum())
        assert abs(p.henreiritsu() - projected) > 0.05
    # Points 2 and 3 differ only in their schedule, and the ratio follows the schedule:
    # the S grid pays 110% of S in staged benefits against the J grid's 100%.
    assert endowment.Projection[2].henreiritsu() > endowment.Projection[3].henreiritsu()


def test_there_is_no_cliff_on_this_product(endowment):
    """No 低解約返戻金型 multiplier, no step at 払込満了, and no surrender spike to go with it.

    No retrieved document offers a suppressed-surrender-value form of either cell.
    Importing the whole life chassis's 0.70 suppression multiplier, its step at ``m`` or its
    15% surrender
    spike would model a product that does not exist here, so ``cv_pp`` and ``surr_val_pp``
    are the same series and both are published, and the absence is stated rather than
    inferred.
    """
    names = set(endowment.Projection.cells) | set(endowment.Projection.refs)
    for absent in ("low_cv", "cv_mult", "cv_factor", "low_cv_ratio", "lapse_spike"):
        assert absent not in names, f"{absent} is 低解約返戻金型 machinery"

    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        for k in range(p.policy_term() + 1):       # k is the anniversary, in years
            assert p.cv_pp(k) == p.surr_val_pp(k)

    # Point 7 is the only shipped point with m < n, so it is where a step at 払込満了 would
    # show.  The value crosses 払込満了 smoothly and the surrender rate does not spike.
    short = endowment.Projection[7]
    m_ = short.prem_term()
    assert m_ == 15 and short.policy_term() == 25
    assert short.cv_pp(m_ + 1) / short.cv_pp(m_) < 1.05      # 1/0.70 would be 1.43
    # and the surrender rate does not spike in the months around 払込満了 either
    assert all(short.lapse_rate(t) == 0.02 for t in range(12 * m_ - 3, 12 * m_ + 3))


# ---------------------------------------------------------------------------
# The roll-forward identities and the check_* cells, on every shipped model point


CHECKS = ("check_pols_roll_fwd", "check_pol_val_roll_fwd", "check_pol_val_terminal",
          "check_surr_charge", "check_staged_value", "check_net_cf")


def test_every_check_cells_holds_on_every_model_point(endowment):
    """All six identities close on all nine points, and each is a no-argument bool.

    The library-wide form: ``check_*()`` takes no argument and returns a bool over the
    whole frame, with the signed residual at ``check_*_resid`` for the step that failed.

    **Two of the six run on months and four on anniversaries**, because that is what they
    check.  The in-force and net-cash-flow identities are statements about flows, so they
    are indexed by the month ``t``; the policy-value roll-forward, its terminal value, the
    surrender charge and the staged-value identity are statements about the contractual
    value construction, which is annual and stayed annual, so they are indexed by the
    anniversary ``k`` in years.
    """
    published = {c for c in endowment.Projection.cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(CHECKS)
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        n, years = p.proj_len(), p.policy_term()
        spans = {
            "check_pols_roll_fwd": range(n),          # flows: one per month
            "check_net_cf": range(n),                 # flows: one per month
            "check_pol_val_roll_fwd": range(years),   # one per policy year rolled
            "check_pol_val_terminal": range(years + 1),
            "check_surr_charge": range(years + 1),
            "check_staged_value": range(years + 1),
        }
        for check in CHECKS:
            value = getattr(p, check)()
            assert isinstance(value, bool), f"{check} on point {point_id}"
            assert value is True, f"{check} is False on point {point_id}"
            resid = getattr(p, check + "_resid")
            assert all(abs(resid(i)) < 1e-6 for i in spans[check]), check


def test_the_in_force_roll_forward_closes_on_every_model_point(endowment):
    """(l+h)(t) - (l+h)(t+1) = D(t) + (1-wv_frac) Dp(t) + Sr(t) + maturity, month by month.

    Rebuilt here from the decrement cells rather than read off the check, so that the
    check and the identity are two statements of the same fact rather than one.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        for t in range(p.proj_len()):
            out = (p.pols_death(t) + p.pols_ph_term(t) + p.pols_lapse(t)
                   + p.pols_maturity(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12)
            assert p.pols_if(t) == pytest.approx(
                p.pols_if_pay(t) + p.pols_wv(t), rel=1e-14)
        assert p.pols_if(0) == 1.0
        assert all(p.pols_if(t) >= p.pols_if(t + 1) - 1e-15
                   for t in range(p.proj_len()))


def test_the_processing_order_takes_surrenders_from_the_survivors(endowment):
    """被保険者 death, 契約者 decrement, the staged benefit, maturity, then surrender.

    Surrenders are taken from the survivors of **both** mortality decrements and valued on
    the surrender value net of the staged benefit just paid.
    """
    p = endowment.Projection[2]
    for t in (0, 35, 131, 215):
        assert p.pols_if_pay_at(t, "BEF_DECR") == p.pols_if_pay(t)
        # the total in-force read is the library-wide name, and it is the sum of the two
        # state reads at every timing
        assert p.pols_if_at(t, "BEF_DECR") == pytest.approx(p.pols_if(t), rel=1e-14)
        assert p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(p.pols_surv(t), rel=1e-14)
        assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(
            p.pols_if(t + 1), abs=1e-15)
        assert p.pols_if_pay_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_if_pay(t) * (1 - p.mort_rate_mth(t))
            * (1 - p.mort_rate_ph_mth(t)), rel=1e-14)
        assert p.pols_wv_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_wv(t) * (1 - p.mort_rate_mth(t)) + p.pols_waived(t), rel=1e-14)
        assert p.pols_surv(t) == pytest.approx(
            p.pols_if_pay_at(t, "BEF_LAPSE") + p.pols_wv_at(t, "BEF_LAPSE"), rel=1e-14)
        assert p.pols_lapse(t) == pytest.approx(
            (p.pols_if_pay_at(t, "BEF_LAPSE")
             + p.pols_wv_at(t, "BEF_LAPSE") * p.wv_lapse_mult())
            * p.lapse_rate_mth(t), rel=1e-14)
        # the surrender benefit is valued on the interpolated value at the close of the
        # month, net of the loan balance outstanding at that anniversary
        assert p.claims(t, "LAPSE") == pytest.approx(
            max(0.0, p.cv_at_m(t + 1) - p.loan_pp(p.duration(t))) * p.pols_lapse(t),
            rel=1e-12)



def test_the_policy_value_recursion_pins_the_timing(endowment):
    """(W(k) + pi 1{k<m})(1+i_cv) = q W_death + (1-q) Wb(k+1), on both constructions.

    **This one is annual on a monthly model, and deliberately so.**  The policy value is a
    contractual construction defined at the 年単位の契約応当日, so it rolls from anniversary
    ``k`` to anniversary ``k + 1``: premium credited at the start of the policy year,
    interest for the whole year, death benefit and staged benefit at the end.  Restating
    it per month would require the within-year rule the 算出方法書 does not publish.
    ``pol_val_db_pp`` is what lets one recursion cover both cells: S on the endowment
    cell, where the death benefit is inside the EPV, and zero on the education cell, where
    the death payment releases the value instead.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        n = p.policy_term()
        assert p.check_pol_val_roll_fwd() is True
        expected = p.sum_assured() if p.cell() == "endowment" else 0.0
        assert all(p.pol_val_db_pp(k) == expected for k in (1, 2, n))
        for k in (0, 1, p.prem_term() - 1, n - 1):
            prev = p.pol_val_pp(k)
            prem = p.prem_net_level_pp() if k < p.prem_term() else 0.0
            q = p.mort_rate_at_age(p.sex(), p.age(12 * k))
            assert (prev + prem) * 1.01 == pytest.approx(
                q * p.pol_val_db_pp(k) + (1 - q) * p.pol_val_pre_pp(k + 1), abs=1e-6)


def test_the_surrender_charge_is_the_whole_gap_to_the_reference_reserve(endowment):
    """reserve_pp(k) - cv_pp(k) = surr_charge_pp(k), exactly, while the value exceeds it.

    ``i_std`` defaults to ``i_cv`` because the numeric 標準利率 could not be established from
    any retrieved official document, which is what makes the gap exactly testable.  The
    deduction is re-based on **one annual premium** rather than on the sum assured,
    because 基準保険金額 is a benefit-scaling unit on the education cell.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        assert p.check_surr_charge() is True
        m_ = p.prem_term()
        for k in range(p.policy_term() + 1):       # k is the anniversary, in years
            assert p.surr_charge_pp(k) == pytest.approx(
                0.25 * p.premium_pp() * max(0, m_ - k) / m_, rel=1e-12)
            if p.pol_val_pp(k) >= p.surr_charge_pp(k):
                assert p.reserve_pp(k) - p.cv_pp(k) == pytest.approx(
                    p.surr_charge_pp(k), abs=1e-6)
            # the elapsed-month reading interpolates between the anniversaries and
            # reproduces them exactly
            assert p.surr_charge_at_m(12 * k) == pytest.approx(
                p.surr_charge_pp(k), abs=1e-6)
        assert p.surr_charge_pp(m_) == 0.0
        assert p.surr_charge_pp(p.policy_term()) == 0.0


def test_the_published_columns_reconcile_to_net_cf(endowment):
    """The published columns are a decomposition of net_cf, not a selection from it.

    A benefit that reached ``net_cf`` without reaching a column, or a column counted
    twice, shows up here and nowhere else.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        assert p.check_net_cf() is True
        df = p.result_cf()
        outgo = df[["claims_death", "claims_staged", "claims_maturity", "claims_lapse",
                    "claims_ph_death", "expenses", "claim_expenses",
                    "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9)
        assert p.claims(0) == pytest.approx(
            sum(p.claims(0, kind) for kind in
                ("DEATH", "STAGED", "MATURITY", "LAPSE", "PH_DEATH")), rel=1e-14)


# ---------------------------------------------------------------------------
# Optional modules, in both positions


def test_the_automatic_premium_loan_is_off_and_advances_when_switched_on(endowment):
    """default_rate is the table rate times apl_default_mult, zero on every point but 8.

    An APL is emphatically **not** a lapse: the advance is applied to the premium and the
    policy stays in force, so it moves ``premiums`` and ``loan_pp`` and leaves the in-force
    recursion alone.  The advance is capped at the surrender value still free of loan, so
    the loan can never exceed the value that secures it.
    """
    base = endowment.Projection[1]
    assert base.apl_elected() is True and base.apl_default_mult() == 0.0
    assert all(base.default_rate(t) == 0.0 for t in range(base.proj_len()))
    assert all(base.apl_advance_pp(t) == 0.0 for t in range(base.proj_len()))
    assert all(base.loan_pp(k) == 0.0 for k in range(base.policy_term() + 1))

    apl = endowment.Projection[8]
    assert apl.apl_default_mult() == 1.0
    # The default proportion is a decision on a date and is NOT converted to a monthly
    # rate: it is applied once per premium, in the anniversary months, and is zero in the
    # eleven months between.
    assert (apl.default_rate(0), apl.default_rate(12), apl.default_rate(24)) == (
        0.010, 0.008, 0.006)
    assert all(apl.default_rate(t) == 0.0 for t in range(1, 12))
    assert apl.default_rate(12 * apl.prem_term()) == 0.0
    assert apl.apl_advance_pp(0) == pytest.approx(181_140.0 * 0.010, abs=YEN)
    assert all(apl.apl_advance_pp(t) == 0.0 for t in range(1, 12))
    assert apl.premiums(0) == pytest.approx(181_140.0 - 1_811.40, abs=YEN)
    assert apl.loan_pp(0) == 0.0
    assert apl.loan_pp(1) == pytest.approx(1_811.40 * 1.024, abs=YEN)
    assert apl.loan_pp(29) > apl.loan_pp(1)
    # A default is not a lapse: the in-force roll-forward is untouched by it.
    assert all(apl.pols_if_pay(t) == pytest.approx(base.pols_if_pay(t), rel=1e-14)
               for t in range(base.proj_len() + 1))
    assert apl.check_pols_roll_fwd() is True
    # And the advance never exceeds the value securing it, at the closing anniversary.
    for k in range(apl.prem_term()):
        assert apl.apl_advance_pp(12 * k) <= max(
            0.0, apl.cv_pp(k + 1) - apl.loan_pp(k)) + 1e-9


def test_the_policy_loan_is_off_and_nets_off_the_benefits_when_drawn(endowment):
    """pol_loan_util of the first year's surrender value, drawn at outset at i_loan.

    Zero on every shipped point but 9.  Neither loan produces a cash flow of its own: both
    net off the death benefit and the surrender benefit, which is why every benefit in the
    base run is gross.
    """
    base = endowment.Projection[1]
    assert base.pol_loan_util() == 0.0
    assert all(base.loan_pp(k) == 0.0 for k in range(base.policy_term() + 1))

    loan = endowment.Projection[9]
    assert loan.pol_loan_util() == 0.50
    assert loan.loan_pp(0) == pytest.approx(0.50 * base.cv_pp(1), rel=1e-12)
    assert loan.loan_pp(1) == pytest.approx(loan.loan_pp(0) * 1.024, rel=1e-12)
    assert loan.death_ben_pp(0) == pytest.approx(
        5_000_000.0 - loan.loan_pp(0), rel=1e-12)
    # The balance compounds ANNUALLY, at the 契約応当日, because the 約款 states a 年利
    # capitalised there — so it genuinely does not move between anniversaries and a
    # benefit in month t is settled against loan_pp(duration(t)).
    assert all(loan.loan_pp(loan.duration(t)) == loan.loan_pp(4) for t in range(48, 60))
    assert loan.claims(48, "LAPSE") == pytest.approx(
        (loan.cv_at_m(49) - loan.loan_pp(4)) * loan.pols_lapse(48), rel=1e-12)
    assert loan.claims(48, "LAPSE") < base.claims(48, "LAPSE")
    # The loan itself is not a cash flow line: the ledger still reconciles.
    assert loan.check_net_cf() is True
    assert "loan_pp" not in loan.result_cf().columns


def test_dynamic_surrender_is_off_and_inert_when_switched_on(endowment):
    """w x min(3, max(1, 1 + beta (CV / cumprem - 1))), beta = 2; true only on point 6.

    On this product the module is **inert wherever it is switched on**, and that is the
    finding rather than a defect: the surrender value never reaches cumulative premiums on
    either cell, so an owner is never given a value reason to surrender.  Point 6 exists to
    show the module wired and inert rather than absent.
    """
    base = endowment.Projection[1]
    assert base.dyn_lapse() is False
    assert all(base.dyn_lapse_factor(t) == 1.0 for t in range(base.proj_len()))

    dyn = endowment.Projection[6]
    assert dyn.dyn_lapse() is True
    assert endowment.Projection.dyn_lapse_beta == 2.0
    assert endowment.Projection.dyn_lapse_cap == 3.0
    n, years = dyn.proj_len(), dyn.policy_term()
    assert all(dyn.dyn_lapse_factor(t) == 1.0 for t in range(n))
    assert all(dyn.lapse_rate(t) == dyn.lapse_rate_base(t) for t in range(n - 1))
    assert max(dyn.cv_pp(k) / dyn.prem_cum_pp(k) for k in range(1, years + 1)) < 1.0
    # It would bite if the ratio ever passed 1: the form is live, not stubbed out.
    assert dyn.cv_pp(years) / dyn.prem_cum_pp(years) > 0.85


def test_the_mortality_margins_are_off_and_move_the_projection_only(endowment):
    """mort_be_factor on the insured and wv_load on the 契約者, both 1.00 in the base run.

    Two inputs and not one, because the margin points in opposite directions on the two
    lives.  Point 4 runs them at 1.25 and 1.50, and its **policy value is identical** to
    point 2's: the cash-value construction reads the table unadjusted, because the policy
    value is a contractual quantity on the pricing basis and a best-estimate adjustment to
    the projection must not move it.
    """
    base = endowment.Projection[2]
    assert base.mort_be_factor() == 1.00 and base.wv_load() == 1.00

    loaded = endowment.Projection[4]
    assert loaded.mort_be_factor() == 1.25 and loaded.wv_load() == 1.50
    for t in (0, 48, 192):
        assert loaded.mort_rate(t) == pytest.approx(1.25 * base.mort_rate(t), rel=1e-14)
        assert loaded.mort_rate_ph(t) == pytest.approx(
            1.50 * base.mort_rate_ph(t), rel=1e-14)
    assert max(abs(loaded.pol_val_pp(k) - base.pol_val_pp(k))
               for k in range(base.policy_term() + 1)) == 0.0
    assert loaded.prem_net_level_pp() == base.prem_net_level_pp()
    assert loaded.surv_prob(0, 10) == base.surv_prob(0, 10)
    # But the projected decrement, and therefore the claims, do move.
    assert loaded.result_cf()["claims_death"].sum() > base.result_cf()[
        "claims_death"].sum()


def test_the_waived_state_surrender_multiplier_is_off_and_bites_when_lowered(endowment):
    """wv_lapse_mult = 1.00 in the base run and 0.50 on point 5.

    Almost certainly too high at 1.00: a waived policy receives every benefit for no
    further premium and has a strictly dominant reason to persist.  It is named so that it
    can be moved, and lowering it holds more of the waived state in force.
    """
    base = endowment.Projection[2]
    assert base.wv_lapse_mult() == 1.00
    for t in (48, 137, 215):
        assert base.pols_lapse(t) == pytest.approx(
            base.pols_surv(t) * base.lapse_rate_mth(t), rel=1e-14)

    sticky = endowment.Projection[5]
    assert sticky.wv_lapse_mult() == 0.50
    # The multiplier acts on the MONTHLY rate: a waived policy that surrenders at half
    # the ordinary pace does so at half the pace every month, rather than at half an
    # annual rate spread unevenly over twelve.
    for t in (48, 137, 215):
        assert sticky.pols_lapse(t) == pytest.approx(
            (sticky.pols_if_pay_at(t, "BEF_LAPSE")
             + 0.50 * sticky.pols_wv_at(t, "BEF_LAPSE")) * sticky.lapse_rate_mth(t),
            rel=1e-14)
        assert sticky.pols_lapse(t) < sticky.pols_surv(t) * sticky.lapse_rate_mth(t)
    assert sticky.check_pols_roll_fwd() is True


def test_the_five_year_dividend_variant_is_rejected_by_name(endowment, tmp_path):
    """dividend_type "five_year" raises rather than projecting a 無配当 contract silently.

    The ５年ごと利差配当 variant needs a 配当基準 that sits in the filed but unpublished 算出方法書,
    no retrieved document quantifies it, and the notes' cash flow equation carries no
    dividend term.  Projecting it under a 有配当 label would present a non-guaranteed
    element as certain.
    """
    assert (endowment.Data.model_point_table()["dividend_type"] == "none").all()
    model = variant_model(tmp_path, {90: (2, {"policy_id": "EN-JP-DIV",
                                              "dividend_type": "five_year"})},
                          "Endowment_JP_S_div")
    try:
        with pytest.raises(FormulaError):
            model.Projection[90].dividend_type()
        with pytest.raises(FormulaError):
            model.Projection[90].result_cf()
    finally:
        model.close()
    names = set(endowment.Projection.cells)
    assert not [n for n in names if "dividend" in n and n != "dividend_type"]


# ---------------------------------------------------------------------------
# Structural product facts


def test_there_are_no_tail_states(endowment):
    """proj_len() is 12 x the 保険期間, and everything closes at the end of t = 12n - 1.

    The frame is ``range(proj_len())``, so the last row is ``t = 12n - 1`` and there is no
    state at ``t = 12n``.  The sharpest delta from the savings chassis, which runs to the
    table's terminal age because a 終身保険 has no expiry.  Importing that here would
    project a contract that has already matured.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        n = p.proj_len()
        assert n == 12 * p.policy_term()
        assert list(p.result_cf().index) == list(range(n))
        assert p.pols_if_pay(n - 1) > 0.0
        assert p.pols_if_pay_at(n - 1, "AFT_DECR") == 0.0
        assert p.pols_wv_at(n - 1, "AFT_DECR") == 0.0
        assert p.pols_if_pay(n) == 0.0 and p.pols_wv(n) == 0.0
        assert p.pols_if_pay(0) == 1.0            # the frame opens on one whole policy
        # The guard, not a row: the frame starts at t = 0, and pols_if_pay is documented
        # to return zero outside 0 .. proj_len() - 1.  No formula ever reads t = -1.
        assert p.pols_if_pay(-1) == 0.0


def test_the_short_premium_term_point_stops_collecting_at_m(endowment):
    """Point 7 is 短期払: m = 15 against n = 25, and premiums stop at m, not at n.

    The renewal commission stops with them while the maintenance expense runs on to the
    end of the term, and the acquisition deduction has already graded to zero at 払込満了.
    """
    p = endowment.Projection[7]
    assert (p.policy_term(), p.prem_term()) == (25, 15)
    assert p.prem_period_months() == 180
    assert p.premiums(168) > 0.0 and p.premiums(180) == 0.0
    assert p.commissions(168) > 0.0 and p.commissions(180) == 0.0
    assert p.maint_expenses(299) > 0.0
    # and in between, eleven months of nothing: the premium is 年払
    assert all(p.premiums(t) == 0.0 for t in range(169, 180))
    # The deduction is anniversary-indexed, in years, and has graded to zero at 払込満了.
    assert p.surr_charge_pp(14) > 0.0 and p.surr_charge_pp(15) == 0.0
    assert p.prem_cum_pp(25) == p.prem_cum_pp(15) == 350_241.0 * 15
    assert p.check_pol_val_terminal() is True
    assert p.pol_val_pp(25) == pytest.approx(5_000_000.0, abs=1e-6)


def test_net_cf_carries_the_notes_own_income_positive_sign(endowment):
    """The notes' CF(t) is already income-positive, so there is no liability_cf companion.

    One stream, one sign, one name.  The shape on the monthly grid is a **sawtooth**: a
    deep new business strain in the first month, then one large positive month a year
    against eleven small negative ones, then one very large negative month at maturity.
    That sawtooth is the 年払 premium, and it is the shape the annual grid could not draw.
    """
    assert "liability_cf" not in endowment.Projection.cells
    p = endowment.Projection[1]
    assert p.net_cf(0) < -30_000.0
    assert all(p.net_cf(12 * k) > 0.0 for k in (1, 2, 3, 4, 28))    # premium months
    assert all(p.net_cf(12 * k + 6) < 0.0 for k in (1, 2, 3, 4, 28))  # and the rest
    assert p.net_cf(359) < -2_000_000.0
    assert abs(p.net_cf(359)) > sum(abs(p.net_cf(t)) for t in range(1, 359)) / 6


def test_result_cf_shape_and_columns(jp_endowment_anchor):
    """pols_if first, then pols_if_pay and pols_wv, then the cash flow lines.

    ``claims_staged`` and ``claims_ph_death`` are named for the ``kind`` arguments
    ``"STAGED"`` and ``"PH_DEATH"`` that produce them, and both are published on the
    endowment cell as columns of zeros because the zero is the product fact.
    """
    df = jp_endowment_anchor.result_cf()
    assert list(df.index) == list(range(360))
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "pols_if_pay", "pols_wv", "premiums", "claims_death",
        "claims_staged", "claims_maturity", "claims_lapse", "claims_ph_death",
        "expenses", "claim_expenses", "commissions", "net_cf",
    ]
    assert (df["claims_staged"] == 0.0).all()
    assert (df["claims_ph_death"] == 0.0).all()
    assert (df["pols_wv"] == 0.0).all()
    assert df.loc[0, "net_cf"] == pytest.approx(-32_837.22, abs=YEN)


def test_the_enum_accessors_validate_rather_than_propagating_a_typo(endowment):
    """An invalid cell, kind or timing raises by name instead of reaching a lookup."""
    p = endowment.Projection[1]
    with pytest.raises(FormulaError):
        p.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        p.pols_if_pay_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        p.pols_wv_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        p.pols_if_at(0, "AFTER_DECR")


ANCHOR_AGES = {
    "M": {0, 1, 3, 5, 10, 15, 17, 18, 20, 22, 25,
          30, 31, 32, 33, 34, 35, 40, 45, 50, 55, 60},
    "F": {0, 1, 3, 5, 10, 15, 17, 18, 20, 22, 25, 30, 35, 40, 45, 50, 55, 60},
}


@pytest.mark.parametrize("sex", ["M", "F"])
def test_the_mortality_table_marks_every_row_anchor_or_interpolated(sex):
    """A row may claim to be a published rate only at an age a document actually quotes.

    The IAJ's site terms forbid redistribution, so the library's position is that it
    **cites** 生保標準生命表2018（死亡保険用）by URL and **quotes** the individual rates its worked
    example needs, shipping everything else as a [std] construction.  That position is
    only true if the file says so row by row: an ANCHOR row at an age no document quotes
    would be claiming to reproduce a rate this library never had, which is the failure the
    whole framing exists to prevent.

    The file is the **canonical** construction shared across the library, so the anchor
    set is the union of the sourced anchors of every product that ships it — which is why
    the male column carries 31 to 34 and 55 and the female column does not carry 31 to 34.
    """
    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    col = mort[mort["sex"] == sex].set_index("age")

    anchors = {age for age, row in col.iterrows()
               if "ANCHOR row" in row["provenance"]}
    interpolated = {age for age, row in col.iterrows()
                    if "INTERPOLATED row" in row["provenance"]}
    assert anchors == ANCHOR_AGES[sex]
    assert anchors | interpolated == set(range(0, 61))
    assert not (anchors & interpolated)

    # Every anchor row quotes its own rate inside its provenance string, so the value and
    # the claim about the value cannot drift apart.
    for age in sorted(anchors):
        assert "q({}) = {:.5f}".format(age, col.loc[age, "mort_rate"]) in (
            col.loc[age, "provenance"]), age

    # And every interpolated row is exactly what its own label says it is: log-linear in
    # ln q between the two anchors that bracket it, at 5 d.p.  There is no extrapolation:
    # age 0 is an anchor on both sexes, so every fill is bracketed on both sides.
    quoted = sorted(anchors)
    for age in sorted(interpolated):
        lo = max(a for a in quoted if a < age)
        hi = min(a for a in quoted if a > age)
        lv, hv = math.log(col.loc[lo, "mort_rate"]), math.log(col.loc[hi, "mort_rate"])
        expected = round(math.exp(lv + (hv - lv) * (age - lo) / (hi - lo)), 5)
        assert col.loc[age, "mort_rate"] == pytest.approx(expected, abs=1e-12), age

    # Nothing in the file claims to be a redistribution of the IAJ table.
    assert col["provenance"].str.contains(
        "not a redistribution of the IAJ table").all()


def test_the_shipped_tables_mark_their_own_provenance():
    """Every assumption row says where it came from, tag by tag.

    The mortality table is a **[std]** construction anchored to 生保標準生命表2018（死亡保険用）
    and never a copy of it — the publisher's site terms prohibit redistribution.  Marking
    the rows is what stops the file being mistaken for the published table.

    The female column is built from its own sourced anchors and is **not** a multiple of
    the male one.  An earlier revision of this file shipped a flat 0.70 ratio; the real
    table's female-to-male ratio is nowhere near flat, so the test that would have passed
    on that file is the one asserted against here — the ratio must vary with age.
    """
    parent = MODEL_DIR.parent
    assert {p.name for p in parent.iterdir() if p.suffix == ".csv"} == {
        "model_point_table.csv", "mort_table.csv", "lapse_table.csv",
        "benefit_schedule_table.csv"}

    for name in ("mort_table.csv", "lapse_table.csv", "benefit_schedule_table.csv"):
        table = pd.read_csv(parent / name)
        assert table["provenance"].notna().all(), name
        assert (table["provenance"].str.len() > 0).all(), name

    mort = pd.read_csv(parent / "mort_table.csv")
    male = mort[mort["sex"] == "M"].set_index("age")["mort_rate"]
    female = mort[mort["sex"] == "F"].set_index("age")["mort_rate"]
    # Ages 0 to 60: every age these nine model points reach, and no more.  The 養老 anchor
    # cell matures at attained age 60.
    assert set(male.index) == set(female.index) == set(range(0, 61))
    ratios = {age: female[age] / male[age] for age in male.index}
    assert max(ratios.values()) - min(ratios.values()) > 0.30
    assert len({round(r, 3) for r in ratios.values()}) > 20
    assert male[30] == 0.00068 and male[59] == 0.00598
    assert female[30] == 0.00037 and female[59] == 0.00342

    schedule = pd.read_csv(parent / "benefit_schedule_table.csv")
    assert set(schedule["schedule_id"]) == {"S_0_1", "J"}
    s_grid = schedule[schedule["schedule_id"] == "S_0_1"]
    # The key column is ``k``, the anniversary in years, not the projection's month ``t``.
    assert dict(zip(s_grid["k"], s_grid["benefit_pct"])) == EDU_SCHEDULE
    assert schedule["benefit_pct"].max() <= 1.0


def test_pols_if_is_the_total_in_force_and_pols_if_pay_the_paying_subset(endowment):
    """pols_if = pols_if_pay + pols_wv, and it is the weight on the result_cf row.

    ``pols_if`` means the same thing here as in every other model in the library: the
    whole surviving block.  The premium and the renewal commission are the only lines that
    read the premium-paying subset — a waived policy is in force, receives every benefit
    and costs the insurer administration, and it pays nothing.  Publishing only the paying
    state as ``pols_if`` would look right on the 養老 cell, where the two coincide, and
    understate the 学資 cell's weights by the whole waived cohort.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        df = p.result_cf()
        assert list(df.columns[:3]) == ["pols_if", "pols_if_pay", "pols_wv"]
        assert (df["pols_if"] - df["pols_if_pay"] - df["pols_wv"]
                ).abs().max() == pytest.approx(0.0, abs=1e-15)
        for t in range(p.proj_len()):
            assert p.pols_if(t) == pytest.approx(
                p.pols_if_pay(t) + p.pols_wv(t), rel=1e-14)
            # benefits and maintenance on the total; premium on the paying state alone
            assert p.pols_death(t) == pytest.approx(
                p.pols_if(t) * p.mort_rate_mth(t), rel=1e-14)
            if t % 12 == 0 and t < p.prem_period_months():
                assert p.premiums(t) == pytest.approx(
                    (p.premium_pp() - p.apl_advance_pp(t)) * p.pols_if_pay(t),
                    rel=1e-12)
            else:
                assert p.premiums(t) == 0.0

    # On the 養老 cell the two are the same series; on the 学資 cell they are not.
    anchor, edu = endowment.Projection[1], endowment.Projection[2]
    assert all(anchor.pols_if(t) == anchor.pols_if_pay(t)
               for t in range(anchor.proj_len()))
    assert any(edu.pols_if(t) > edu.pols_if_pay(t)
               for t in range(edu.proj_len()))


def test_expenses_is_the_policy_expense_and_the_claim_expense_is_its_own_column(
        endowment):
    """expenses = acquisition + maintenance; claim_expenses is deducted separately.

    ``expenses`` carries a per-policy servicing cost in every model in the library, so the
    column can be read across products.  The claim handling expense is a per-claim cost:
    it is its own cells, its own ``result_cf()`` column, and an explicit term in
    ``net_cf``.  Folding it in would leave the ledger reconciling and the column
    incomparable, which is why the ledger check rebuilds from both.
    """
    for point_id in endowment.Data.model_point_table().index:
        p = endowment.Projection[point_id]
        for t in range(p.proj_len()):
            assert p.expenses(t) == pytest.approx(
                p.acq_expenses(t) + p.maint_expenses(t), rel=1e-14)
            assert p.claim_expenses(t) == pytest.approx(
                20_000.0 * p.pols_death(t), rel=1e-14)
            assert p.net_cf(t) == pytest.approx(
                p.premiums(t) - p.claims(t) - p.claim_expenses(t)
                - p.expenses(t) - p.commissions(t), abs=1e-9)
        df = p.result_cf()
        assert "claim_expenses" in df.columns
        assert (df["claim_expenses"] > 0).any()
        assert df["claim_expenses"].sum() < df["expenses"].sum()


def test_the_model_point_table_covers_both_cells_and_every_module(endowment):
    """Nine points: two anchors, both schedule shapes, and each module in its on position.

    ``point_id = 1`` is the notes' 養老 anchor cell and ``point_id = 2`` its 学資 cell, which
    is the library convention that the anchor is point 1.
    """
    table = endowment.Data.model_point_table()
    assert list(table.index) == list(range(1, 10))
    assert set(table["cell"]) == {"endowment", "education"}
    assert list(table.loc[[1, 2], "policy_id"]) == ["EN-JP-0001", "EN-JP-0002"]
    assert set(table["schedule_id"]) == {"none", "S_0_1", "J"}
    assert (table["apl_default_mult"] > 0).sum() == 1
    assert (table["pol_loan_util"] > 0).sum() == 1
    assert (table["wv_frac"] < 1).sum() == 1
    assert (table["wv_lapse_mult"] < 1).sum() == 1
    assert table["dyn_lapse"].sum() == 1
    assert (table["prem_term"] < table["policy_term"]).sum() == 5   # points 2-5 and 7
    assert bool(table["waiver"].any()) and not bool(table["waiver"].all())
