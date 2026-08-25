"""Golden and structural tests for IncomeTerm_JP_S.

The golden values are the worked example in
``products/income_guarantee/technical-notes.md`` ("Worked example"), which projects the
anchor cell M30 / 非喫煙者優良体 / 65歳満了 (``N = 420`` months) / 最低支払保証期間 2年 (``G = 24``
months) / 年金月額 JPY 150,000 / JPY 2,565 a month.  They are hard-coded here rather than
pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the yen's second decimal,
in-force to six decimals, the claim and ledger populations to nine, and the decrement
rates to twelve — the last because ``q_m`` at attained age 30 is about 3.17e-05, so six
decimals would leave it with two significant figures (0.000032), a 0.8% distortion carried
into every claim of the first policy year.

The notes' four present-value diagnostics are asserted too, even though discounting is out
of scope for the library and no cells computes them, because they reproduce only under the
notes' own split timing and a reader applying a single timing gets different numbers.

収入保障保険 (*shūnyū hoshō hoken*) is a **death** benefit paid as a level monthly income to
a fixed expiry date.  It is not income protection in ``uklib``'s sense, where ``IP_UK_S``
insures disability; nothing here models a disability decrement.

Beyond the worked example this module asserts, one test each, every entry in the notes'
**Known modeling pitfalls** list, because each of them is a way an implementation can look
right and be wrong:

* the projection horizon is ``N + G - 1``, not ``N``;
* 最低支払保証期間 is a term extension, not a benefit floor — the totals agree and the shapes
  do not;
* the in-payment ledger is never decremented, by anything;
* premiums stop on the annuity event and the benefit does not;
* ``pols_if`` and ``annuities_if`` are disjoint and must never be summed;
* the ledger peaks at exactly month ``N``;
* 高度障害 is one decrement with death, not a second one;
* there is no 更新 on this chassis;
* a lapse pays nothing, and the 低解約返戻金型 cliff has no analogue here;
* there is no 自動振替貸付;
* a full 一括受取 settles the claim instead of opening the stream;
* the リビング・ニーズ cap binds early rather than late;
* and the table is read at the attained age on the death basis alone.
"""
import shutil

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from jp_registry import LIB, MODELS


MODEL_DIR = LIB / MODELS["IncomeTerm_JP_S"][0]

YEN = 0.005           # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.
LEDGER = 5e-10        # claim and ledger populations displayed to 9 d.p.
RATE = 5e-13          # decrement rates displayed to 12 d.p.

# The notes' worked-example table, verbatim.
#
# t: (l(t), premiums, D(t), R(t), annuity claims, claim + annuity expense,
#     "Maint. + acq.", "Comm.", CF(t))
#
# The last two columns follow the notes' *table* presentation, which puts E0 + c0 in the
# "Maint. + acq." column and reserves "Comm." for the renewal commission.  The model
# follows the notes' own Notation table instead, where E0 is expense_acq and both c0 and
# c_r are commissions; :func:`notes_columns` maps between them.  The notes' totals table
# separates the two and the model reproduces both — see TOTALS below.
WORKED_EXAMPLE = {
    1:   (1.000000, 2565.00, 0.000031739, 0.000031739,    4.76, 0.96, 30723.33,   0.00, -28164.05),
    2:   (0.992140, 2544.84, 0.000031489, 0.000063228,    9.48, 0.96,   330.71,   0.00,   2203.68),
    3:   (0.984342, 2524.84, 0.000031242, 0.000094470,   14.17, 0.96,   328.11,   0.00,   2181.60),
    13:  (0.909653, 2333.26, 0.000029296, 0.000394122,   59.12, 0.96,   306.25, 116.66,   1850.27),
    420: (0.145023,  371.98, 0.000063023, 0.016779783, 2516.97, 5.25,    67.80,  18.60,  -2236.63),
    421: (0.000000,    0.00, 0.000000000, 0.001463980,  219.60, 0.29,     0.00,   0.00,   -219.89),
    443: (0.000000,    0.00, 0.000000000, 0.000063023,    9.45, 0.01,     0.00,   0.00,     -9.47),
}

# The notes' decrement vector at the three months where something changes: month 1, month
# 13 (attained age and lapse row both move) and month 420 (the last month of cover).
# t: (q(t), q_m(t), w(t), w_m(t))
WORKED_EXAMPLE_RATES = {
    1:   (0.000380800, 0.000031738873, 0.09, 0.007828420342),
    13:  (0.000386400, 0.000032205704, 0.07, 0.006029308066),
    420: (0.005202400, 0.000434570514, 0.05, 0.004265318778),
}

# The male table rates the notes display.  Four are sourced anchors read from
# 生保標準生命表2018（死亡保険用）— ages 30, 31, 32 and 45 — and three are the log-linear
# interpolations in ln q between the neighbouring anchors that the projection also uses.
# Reproducing these is what makes the worked example checkable.
TABLE_RATES_M = {30: 0.00068, 31: 0.00069, 32: 0.00070, 44: 0.00163,
                 45: 0.00177, 63: 0.00851, 64: 0.00929}

# The notes' totals over the 443 projected months, undiscounted, per policy issued.
TOTALS = {
    "premiums": 461030.83,
    "claims_annuity": 443313.69,
    "annuity_expenses": 591.08,
    "claim_expenses": 503.39,
    "maintenance": 67706.86,
    "commission_renewal": 21577.36,
    "acquisition": 30390.00,
    "net_cf": -103051.56,
}

# The notes' present-value diagnostics, per policy issued, at flat annual effective rates.
# Discounting is out of scope for the library and no cells computes these; they are the
# notes' own statement of how far the answer moves on a product whose claim leg discounts
# far harder than its premium leg.  rate -> present value of the projection.
PV_DIAGNOSTICS = {0.0: -103051.56, 0.005: -73865.82, 0.01: -49216.50,
                  0.02: -10895.85}

# The structural quantities the notes print behind those totals.
SUM_DEATHS = 0.016779783          # expected claims over the term
SUM_INSTALMENTS = 2.955425        # expected instalments per policy issued
BENEFIT_PER_CLAIM = 26419511.96   # average total benefit per claim, JPY
LAPSES = 0.838878                 # lapses over the term
SURVIVORS = 0.144342              # survivors at expiry, paid nothing
TAIL_CLAIMS = 2645.21             # claim outgo falling after the expiry date
TAIL_SHARE_PCT = 0.5967           # ... as a percentage of the total


def notes_columns(proj, t):
    """The notes' "Maint. + acq." and "Comm." columns, from the model's own cells.

    The notes' table groups the initial commission with the acquisition expense; the
    model follows the notes' Notation table, where ``c0`` is commission.  One
    presentation, two column allocations, identical numbers.
    """
    init = proj.comm_init_pp() * proj.pols_if(1) if t == 1 else 0.0
    return proj.expenses(t) + init, proj.commissions(t) - init


def model_copy(tmp_path, name):
    """A private copy of the model and its external inputs, under *tmp_path*.

    Inputs are external files resolved from ``_model.path.parent``, so a test that wants
    to swap one copies the whole product directory rather than writing into the
    repository — an orphan CSV left beside the shipped model would fail the library's
    own "every CSV is actually read" convention test.
    """
    dest = tmp_path / MODEL_DIR.name
    shutil.copytree(MODEL_DIR, dest)
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)
    return mx.read_model(dest, name=name)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(jp_income_anchor, t):
    """Every cell of the notes' seven-row table, to the precision the notes display."""
    (pols, prem, deaths, ledger, annuity, claim_exp,
     maint_acq, comm, net) = WORKED_EXAMPLE[t]
    a = jp_income_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=YEN)
    assert a.pols_death(t) == pytest.approx(deaths, abs=LEDGER)
    assert a.annuities_if(t) == pytest.approx(ledger, abs=LEDGER)
    assert a.claims(t, "ANNUITY") == pytest.approx(annuity, abs=YEN)
    assert a.claim_expenses(t) + a.annuity_expenses(t) == pytest.approx(
        claim_exp, abs=YEN)
    notes_maint_acq, notes_comm = notes_columns(a, t)
    assert notes_maint_acq == pytest.approx(maint_acq, abs=YEN)
    assert notes_comm == pytest.approx(comm, abs=YEN)
    assert a.net_cf(t) == pytest.approx(net, abs=YEN)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_RATES))
def test_worked_example_decrement_rates(jp_income_anchor, t):
    """q, q_m, w and w_m at the three months where the notes quote them.

    The monthly rates are the effective convention, ``1 - (1 - q)^(1/12)``, not a
    nominal ``q / 12``; the notes state the convention and the values to twelve
    decimals, which is what makes the two distinguishable.
    """
    q, q_m, w, w_m = WORKED_EXAMPLE_RATES[t]
    a = jp_income_anchor
    assert a.mort_rate(t) == pytest.approx(q, rel=1e-12)
    assert a.mort_rate_mth(t) == pytest.approx(q_m, abs=RATE)
    assert a.lapse_rate(t) == pytest.approx(w, rel=1e-14)
    assert a.lapse_rate_mth(t) == pytest.approx(w_m, abs=RATE)
    assert a.mort_rate_mth(t) == pytest.approx(
        1.0 - (1.0 - q) ** (1.0 / 12.0), rel=1e-14)
    assert a.mort_rate_mth(t) != pytest.approx(q / 12.0, rel=1e-6)


def test_worked_example_basis_is_the_std_adjustment_of_the_table(jp_income_anchor):
    """q(t) = 0.80 x 0.70 x q_x, the chassis factor and the rate class factor.

    The 0.80 is the protection chassis's [std] best-estimate factor and the 0.70 the
    [std] 非喫煙者優良体 class factor; the table rate itself is the one sourced number in the
    chain.  Naming all three separately is what keeps a sourced value from being mistaken
    for a modelling assumption.
    """
    a = jp_income_anchor
    assert a.class_factor() == pytest.approx(0.70, rel=1e-14)
    assert a.mort_rate_base(1) == pytest.approx(0.00068, rel=1e-14)
    assert a.mort_rate(1) == pytest.approx(0.80 * 0.70 * 0.00068, rel=1e-14)


@pytest.mark.parametrize("age,rate", sorted(TABLE_RATES_M.items()))
def test_the_shipped_table_reproduces_the_rates_the_notes_display(age, rate):
    """The [std] construction hits the notes' anchor and its interpolated rates exactly.

    ``mort_table.csv`` is a construction, not a copy of 生保標準生命表2018（死亡保険用）, whose
    publisher prohibits redistribution.  What makes it usable is that it reproduces
    every rate the worked example quotes, so a reader can check the projection against
    the notes without the publisher's file.
    """
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv",
                        index_col=["sex", "age"])
    assert table.loc[("M", age), "mort_rate"] == pytest.approx(rate, rel=1e-14)


def test_worked_example_month_one_trace(jp_income_anchor):
    """The notes' month-one trace, line by line.

    The claim opens a stream and pays no lump sum, so R(1) = D(1) and the whole benefit
    of the month is one instalment of 150,000 x D(1).
    """
    a = jp_income_anchor
    assert a.pols_if_init() == 1.0
    assert a.pols_death(1) == pytest.approx(0.000031738873, abs=RATE)
    assert a.annuities_open(1) == pytest.approx(a.pols_death(1), rel=1e-14)
    assert a.annuities_if(1) == pytest.approx(a.pols_death(1), rel=1e-14)
    assert a.claims(1, "ANNUITY") == pytest.approx(4.76083098, abs=1e-6)
    assert a.annuity_expenses(1) == pytest.approx(0.00634777, abs=1e-6)
    assert a.claim_expenses(1) == pytest.approx(0.95216620, abs=1e-6)
    assert a.expenses(1) == pytest.approx(15000.0 + 4000.0 / 12.0, abs=1e-8)
    assert a.comm_init_pp() == pytest.approx(0.50 * 12 * 2565.0, abs=1e-9)
    assert a.net_cf(1) == pytest.approx(-28164.05267828, abs=1e-6)


def test_worked_example_inforce_update(jp_income_anchor):
    """l(2) = l(1)(1 - q_m)(1 - w_m), the notes' update step, death before lapse."""
    a = jp_income_anchor
    assert a.pols_if(2) == pytest.approx(
        1.0 * (1 - 0.000031738873) * (1 - 0.007828420342), rel=1e-12)
    assert a.pols_if(3) == pytest.approx(0.9843419567, abs=1e-10)
    for t in (1, 200, 419):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate_mth(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t), rel=1e-14)


def test_worked_example_month_thirteen_changes_three_things_at_once(jp_income_anchor):
    """Attained age, lapse row and expense inflation all step at month 13.

    The notes call this out because an implementation can get any of the three wrong and
    still produce a plausible row.  It is also the first month renewal commission is paid.
    """
    a = jp_income_anchor
    assert a.age(12) == 30 and a.age(13) == 31
    assert a.policy_year(12) == 1 and a.policy_year(13) == 2
    assert a.mort_rate_base(13) == pytest.approx(0.00069, rel=1e-14)
    assert a.lapse_rate(12) == 0.09 and a.lapse_rate(13) == 0.07
    assert a.inflation_factor(13) == pytest.approx(1.01, rel=1e-14)
    assert a.expenses(13) == pytest.approx(
        (4000.0 / 12.0) * 1.01 * a.pols_if(13), rel=1e-14)
    assert a.commissions(12) == 0.0
    assert a.commissions(13) == pytest.approx(0.05 * a.premiums(13), rel=1e-14)


def test_worked_example_totals(jp_income_anchor):
    """The notes' totals table over all 443 months, undiscounted, per policy issued."""
    a = jp_income_anchor
    df = a.result_cf()
    n = a.proj_len()
    assert df["premiums"].sum() == pytest.approx(TOTALS["premiums"], abs=YEN)
    assert df["claims_annuity"].sum() == pytest.approx(
        TOTALS["claims_annuity"], abs=YEN)
    assert df["annuity_expenses"].sum() == pytest.approx(
        TOTALS["annuity_expenses"], abs=YEN)
    assert df["claim_expenses"].sum() == pytest.approx(
        TOTALS["claim_expenses"], abs=YEN)
    assert df["net_cf"].sum() == pytest.approx(TOTALS["net_cf"], abs=YEN)
    # The notes split the two expense/commission lines the way the Notation table does.
    acquisition = 15000.0 + a.comm_init_pp()
    maintenance = df["expenses"].sum() - 15000.0
    renewal = df["commissions"].sum() - a.comm_init_pp()
    assert acquisition == pytest.approx(TOTALS["acquisition"], abs=YEN)
    assert maintenance == pytest.approx(TOTALS["maintenance"], abs=YEN)
    assert renewal == pytest.approx(TOTALS["commission_renewal"], abs=YEN)
    assert len(df) == n == 443


def test_worked_example_structural_quantities(jp_income_anchor):
    """Expected claims, instalments, benefit per claim, lapses and survivors.

    ``sum R(t) = 2.955425`` instalments against ``sum D(s) = 0.016780`` claims is an
    average of 176 instalments a claim — the number that says this is an income product
    and not a sum-assured one.
    """
    a = jp_income_anchor
    n, horizon = a.term_m(), a.proj_len()
    deaths = sum(a.pols_death(t) for t in range(1, n + 1))
    instalments = sum(a.annuities_if(t) for t in range(1, horizon + 1))
    assert deaths == pytest.approx(SUM_DEATHS, abs=LEDGER)
    assert instalments == pytest.approx(SUM_INSTALMENTS, abs=INFORCE)
    assert a.annuity_mth() * instalments / deaths == pytest.approx(
        BENEFIT_PER_CLAIM, abs=YEN)
    assert sum(a.pols_lapse(t) for t in range(1, n + 1)) == pytest.approx(
        LAPSES, abs=INFORCE)
    assert a.pols_maturity(n) == pytest.approx(SURVIVORS, abs=INFORCE)


def test_the_present_value_diagnostics_need_the_notes_own_split_timing(jp_income_anchor):
    """The four present values the notes print, and the timing convention behind them.

    Discounting is out of scope for the library, so nothing in the model computes these.
    They are asserted here because they reproduce to the yen only under the notes' own
    **split timing** — the start-of-month leg (premiums, maintenance, renewal commission)
    at ``(t - 1) / 12`` and the end-of-month leg (the instalments, the claim expense, the
    annuity administration expense) at ``t / 12``, which is what the notes' timing section
    specifies.  Applying one timing to ``net_cf(t)`` instead gives a different set of
    numbers, and on this product, where the benefit runs for up to 35 years after a claim
    that itself arises over 35 years, which convention produced a printed figure is not a
    detail.
    """
    a = jp_income_anchor
    horizon = a.proj_len()
    for rate, expected in PV_DIAGNOSTICS.items():
        pv = 0.0
        for t in range(1, horizon + 1):
            start = a.premiums(t) - a.expenses(t) - a.commissions(t)
            end = -a.claims(t) - a.claim_expenses(t) - a.annuity_expenses(t)
            pv += (start * (1.0 + rate) ** (-(t - 1) / 12.0)
                   + end * (1.0 + rate) ** (-t / 12.0))
        assert pv == pytest.approx(expected, abs=YEN), f"at {rate:.3%}"
    # At zero interest the convention cannot matter, and the diagnostic is the total.
    assert PV_DIAGNOSTICS[0.0] == pytest.approx(TOTALS["net_cf"], abs=YEN)
    # One timing applied to the whole of net_cf is a different number, by enough to see.
    single = sum(a.net_cf(t) * 1.005 ** (-t / 12.0) for t in range(1, horizon + 1))
    assert single == pytest.approx(-73998.78, abs=YEN)
    assert abs(single - PV_DIAGNOSTICS[0.005]) > 100.0


def test_new_business_strain_then_a_margin_that_turns(jp_income_anchor):
    """The characteristic shape: a deep month-one strain, then margin, then loss.

    Month 1 carries E0 and the whole initial commission against one month's premium;
    the middle of the projection runs positive while the level premium is ahead of the
    accumulating ledger; and the last month of cover is negative because the ledger has
    grown to its peak while the surviving population has decayed to 0.14.
    """
    a = jp_income_anchor
    assert a.net_cf(1) < -28000.0
    assert all(a.net_cf(t) > 0.0 for t in (2, 3, 13, 120))
    assert a.net_cf(a.term_m()) < 0.0
    assert all(a.net_cf(t) < 0.0 for t in range(a.term_m() + 1, a.proj_len() + 1))


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test each, named for the pitfall


def test_pitfall_the_projection_horizon_is_not_the_policy_term(income_guarantee):
    """T = N + G - 1, and truncating at N drops JPY 2,645.21 of contractual outgo.

    The most natural error to make on this product and the least visible: every
    remaining number still looks reasonable.  Asserted on every shipped point, since a
    horizon derived from the term alone would be wrong on all of them.
    """
    for point_id in income_guarantee.Data.model_point_table().index:
        proj = income_guarantee.Projection[point_id]
        assert proj.proj_len() == proj.term_m() + proj.guar_m() - 1
        assert proj.proj_len() > proj.term_m()
        assert len(proj.result_cf()) == proj.proj_len()

    a = income_guarantee.Projection[1]
    n, horizon = a.term_m(), a.proj_len()
    tail = sum(a.claims(t, "ANNUITY") for t in range(n + 1, horizon + 1))
    total = sum(a.claims(t, "ANNUITY") for t in range(1, horizon + 1))
    assert tail == pytest.approx(TAIL_CLAIMS, abs=YEN)
    assert 100.0 * tail / total == pytest.approx(TAIL_SHARE_PCT, abs=5e-5)


def test_pitfall_the_guarantee_is_a_term_extension_not_a_benefit_floor(
        jp_income_anchor):
    """Both readings pay max(N - m + 1, G) instalments; only the timing distinguishes them.

    A floor implementation compresses the guaranteed instalments inside the term and
    produces zero cash flow after month N.  So the total cannot be the test — months
    421 to 443 have to be checked individually, and every one of them must carry an
    instalment and its administration expense and nothing else.
    """
    a = jp_income_anchor
    n, g, horizon = a.term_m(), a.guar_m(), a.proj_len()
    assert a.check_pay_count() is True
    for m in (1, 10, 181, 243, 361, 419, 420):
        assert a.pay_count(m) == max(n - m + 1, g)
        assert a.pay_end(m) == max(n, m + g - 1)
        assert a.pay_count(m) == a.pay_end(m) - m + 1
    # The notes' published instalment illustrations.
    assert (a.pay_count(1), a.pay_count(181), a.pay_count(361)) == (420, 240, 60)
    assert (a.pay_count(10), a.pay_count(243)) == (411, 178)
    # The tail is not empty, and it is instalments only.
    for t in range(n + 1, horizon + 1):
        assert a.claims(t, "ANNUITY") > 0.0
        assert a.annuity_expenses(t) > 0.0
        assert a.net_cf(t) == pytest.approx(
            -a.claims(t, "ANNUITY") - a.annuity_expenses(t), abs=1e-9)
    assert a.pay_end(419) == 442        # twenty-two months past the expiry date


def test_pitfall_the_in_payment_ledger_is_never_decremented(jp_income_anchor):
    """R(t) carries no survival condition — the largest single error available here.

    Applying the surviving-policy factor (1 - q_m)(1 - w_m) to the ledger, the natural
    thing to do if R is mistaken for a population of policies, cuts annuity outgo from
    JPY 443,313.69 to JPY 245,605.66, an understatement of 44.6%.  The counterfactual is
    built here so the test fails loudly rather than merely differing.
    """
    a = jp_income_anchor
    horizon = a.proj_len()
    assert a.check_annuity_ledger() is True
    assert a.check_annuity_total() is True
    for t in (1, 2, 13, 240, 420, 421, 443):
        assert a.check_annuity_ledger_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert a.check_annuity_total_resid(t) == pytest.approx(0.0, abs=1e-12)

    # The recursion moves only by claims opening and streams ending.
    for t in range(2, horizon + 1):
        assert a.annuities_if(t) == pytest.approx(
            a.annuities_if(t - 1) - a.annuities_ended(t) + a.annuities_open(t),
            abs=1e-15)
    # ... and never falls while claims are still arising.
    for t in range(2, a.term_m() + 1):
        assert a.annuities_if(t) >= a.annuities_if(t - 1)

    decremented, outgo = 0.0, 0.0
    for t in range(1, horizon + 1):
        decremented = (decremented
                       * (1.0 - a.mort_rate_mth(t)) * (1.0 - a.lapse_rate_mth(t))
                       - a.annuities_ended(t) + a.annuities_open(t))
        outgo += a.annuity_mth() * decremented
    assert outgo == pytest.approx(245605.66, abs=YEN)
    assert outgo < 0.56 * TOTALS["claims_annuity"]


def test_pitfall_premiums_stop_on_the_annuity_event_the_benefit_does_not(
        jp_income_anchor):
    """Premium income carries l(t) and only l(t).

    Netting premiums against claims on one combined population would collect
    JPY 7,535.43 of premium — 1.63% of the total — from policies that are in claim and
    paying nothing.  A policy in claim has already left ``pols_if``, so the model needs
    no term for it; what it must not do is give the ledger a premium.
    """
    a = jp_income_anchor
    n = a.term_m()
    for t in (1, 2, 13, 240, 420):
        assert a.premiums(t) == pytest.approx(
            a.prem_due_pp(t) * a.pols_payer(t), rel=1e-14)
    assert a.pols_payer(1) == a.pols_if(1)          # no waiver on the anchor
    wrongly_collected = a.premium_mth_pp() * sum(
        a.annuities_if(t) for t in range(1, n + 1))
    assert wrongly_collected == pytest.approx(7535.43, abs=YEN)
    assert wrongly_collected / TOTALS["premiums"] == pytest.approx(0.0163, abs=5e-5)
    assert all(a.premiums(t) == 0.0 for t in range(n + 1, a.proj_len() + 1))


def test_pitfall_pols_if_and_annuities_if_are_disjoint(income_guarantee):
    """l(t) is a probability of being in force; R(t) is a count of instalments due.

    On the anchor cell R(420) = 0.016780 while l(420) = 0.145023, and adding them
    produces a number with no meaning.  The model keeps them apart by name — the ledger
    is deliberately not spelled ``pols_*`` — and by which cash flow line each weights.
    """
    a = income_guarantee.Projection[1]
    assert a.annuities_if(420) == pytest.approx(0.016779783, abs=LEDGER)
    assert a.pols_if(420) == pytest.approx(0.145023, abs=INFORCE)
    names = set(income_guarantee.Projection.cells)
    assert "pols_annuity" not in names and "pols_annuities" not in names
    df = a.result_cf()
    # The two annuity lines are exactly the ledger; the other three are exactly pols_if.
    for t in (13, 240, 420):
        assert df.loc[t, "claims_annuity"] == pytest.approx(
            a.annuity_mth() * a.annuities_if(t), rel=1e-14)
        assert df.loc[t, "expenses"] == pytest.approx(
            (4000.0 / 12.0) * a.inflation_factor(t) * a.pols_if(t), rel=1e-14)
    # Past the term one is zero and the other is not, which is the cleanest statement
    # available that they are different quantities.
    assert a.pols_if(421) == 0.0 and a.annuities_if(421) > 0.0


def test_pitfall_the_ledger_peaks_at_exactly_month_n(jp_income_anchor):
    """R(N) equals the sum of every claim the contract has ever made.

    Every stream opened in months 1 ... N - G + 1 ends at month N whenever it opened,
    because the expiry date is fixed at issue.  An implementation that ends streams one
    month early gets this identity wrong by one month's claims and nothing else visibly
    changes.
    """
    a = jp_income_anchor
    n, g, horizon = a.term_m(), a.guar_m(), a.proj_len()
    deaths = sum(a.pols_death(t) for t in range(1, n + 1))
    assert a.annuities_if(n) == pytest.approx(deaths, abs=1e-15)
    assert a.annuities_if(n) == pytest.approx(SUM_DEATHS, abs=LEDGER)
    assert a.annuities_if(n) == max(a.annuities_if(t) for t in range(1, horizon + 1))
    # Only the last G - 1 months' claims survive into month N + 1.
    assert a.annuities_ended(n + 1) == pytest.approx(
        sum(a.annuities_open(s) for s in range(1, n - g + 2)), abs=1e-15)
    assert a.annuities_if(n + 1) == pytest.approx(
        sum(a.annuities_open(s) for s in range(n - g + 2, n + 1)), abs=1e-15)
    # ... and from there the ledger runs down one month's claims at a time.
    for t in range(n + 2, horizon + 1):
        assert a.annuities_ended(t) == pytest.approx(a.annuities_open(t - g), abs=1e-18)
    assert a.annuities_if(horizon) == pytest.approx(a.pols_death(n), abs=1e-15)


def test_pitfall_kodo_shogai_is_not_a_second_decrement(income_guarantee):
    """One decrement, one benefit: 生保標準生命表2018（死亡保険用）already includes 高度障害.

    The 死亡年金 and the 高度障害年金 are contractually mutually exclusive, so an added 高度障害
    incidence on top of the table double-counts the benefit.  There is no second
    incidence cells anywhere in the model, and the one decrement is the table rate.
    """
    names = (set(income_guarantee.Projection.cells)
             | set(income_guarantee.Projection.refs))
    for absent in ("disab_rate", "disability_rate", "kodo_shogai_rate",
                   "ti_rate", "accel_rate", "morb_rate"):
        assert absent not in names
    a = income_guarantee.Projection[1]
    assert a.pols_death(1) == pytest.approx(
        a.pols_if(1) * a.mort_rate_mth(1), rel=1e-14)
    assert a.annuities_open(1) == pytest.approx(a.pols_death(1), rel=1e-14)
    doc = income_guarantee.Projection.doc + income_guarantee.doc
    assert "高度障害" in doc


def test_pitfall_there_is_no_renewal_on_this_chassis(income_guarantee):
    """歳満了 only: the term is derived from the expiry age and the premium is level.

    No retrieved document offers 更新 and one states its absence in terms.  Importing the
    protection chassis's renewal repricing and decline decrement would invent a decision,
    a premium ladder and a decrement the contract does not have.
    """
    names = (set(income_guarantee.Projection.cells)
             | set(income_guarantee.Projection.refs))
    for absent in ("renewal_age", "renew_rate", "decline_rate", "jump_ratio",
                   "shock_lapse_rate", "phase", "reprice_factor", "conv_rate"):
        assert absent not in names
    table = income_guarantee.Data.model_point_table()
    assert "policy_term" not in table.columns    # the term is not an input
    assert "expiry_age" in table.columns
    for point_id in table.index:
        proj = income_guarantee.Projection[point_id]
        assert proj.term_m() == 12 * (proj.expiry_age() - proj.issue_age())
        assert all(proj.prem_due_pp(t) in (0.0, proj.premium_mth_pp()
                                           * proj.prem_mode_months())
                   for t in range(1, proj.term_m() + 1))


def test_pitfall_lapse_pays_nothing_and_there_is_no_surrender_value_cliff(
        income_guarantee):
    """無解約返戻金型: no 解約返戻金 at any duration, so a lapse is a pure decrement.

    The zero column is published rather than dropped, because a non-zero lapse row
    imported from a cash-value chassis is exactly the error being guarded against.  The
    低解約返戻金型 cliff has no analogue here either: 保険料払込期間 equals 保険期間, so there is no
    払込満了 step for a suppressed value to step up at.
    """
    names = (set(income_guarantee.Projection.cells)
             | set(income_guarantee.Projection.refs))
    for absent in ("cv_pp", "cv_rate", "surr_charge", "surr_value",
                   "low_cv_factor", "paidup_value", "prem_paying_term_m"):
        assert absent not in names
    for point_id in income_guarantee.Data.model_point_table().index:
        proj = income_guarantee.Projection[point_id]
        df = proj.result_cf()
        assert (df["claims_lapse"] == 0.0).all()
        assert all(proj.claims(t, "LAPSE") == 0.0
                   for t in range(1, proj.proj_len() + 1))
        # Premium ceases with cover, not before it: 保険料払込期間 equals 保険期間, so there is
        # no 払込満了 step for a suppressed surrender value to step up at.
        n, period = proj.term_m(), proj.prem_mode_months()
        assert sum(proj.prem_due_pp(t) for t in range(n - period + 1, n + 1)) > 0.0
        assert proj.prem_due_pp(n + 1) == 0.0
        assert sum(1 for t in range(1, n + 1) if proj.prem_due_pp(t) > 0.0) == (
            n // period)
    # Lapses do happen; they simply pay nothing.
    a = income_guarantee.Projection[1]
    assert sum(a.pols_lapse(t) for t in range(1, a.term_m() + 1)) == pytest.approx(
        LAPSES, abs=INFORCE)


def test_pitfall_there_is_no_automatic_premium_loan(income_guarantee):
    """With no cash value there is no collateral, so 自動振替貸付 cannot exist here.

    The APL mechanic specified for the savings chassis must not be imported: a policy
    with an unpaid premium here lapses at the end of the 猶予期間 rather than being carried
    by a loan against its surrender value.
    """
    names = (set(income_guarantee.Projection.cells)
             | set(income_guarantee.Projection.refs))
    for absent in ("apl", "apl_balance", "apl_interest", "policy_loan",
                   "loan_balance", "loan_interest"):
        assert absent not in names
    a = income_guarantee.Projection[1]
    # A lapse leaves the projection outright; nothing carries it forward.
    assert a.pols_if(2) == pytest.approx(a.pols_if_at(1, "AFT_DECR"), rel=1e-14)
    assert a.pols_reinst(2) == 0.0        # 復活 is off, and it is not an APL either


def test_pitfall_a_full_commutation_settles_the_claim_and_opens_no_stream(
        income_guarantee):
    """Paying the whole present value extinguishes the contract.

    A model that pays the lump sum *and* opens the stream doubles the benefit.  Model
    point 4 runs the module at the extreme: every claim commuted, so the ledger is
    empty for the whole projection.
    """
    p4 = income_guarantee.Projection[4]
    assert p4.commutation() is True
    horizon = p4.proj_len()
    assert all(p4.annuities_open(t) == 0.0 for t in range(1, horizon + 1))
    assert all(p4.annuities_if(t) == 0.0 for t in range(1, horizon + 1))
    assert all(p4.claims(t, "ANNUITY") == 0.0 for t in range(1, horizon + 1))
    assert any(p4.claims(t, "COMMUTATION") > 0.0 for t in range(1, horizon + 1))
    for t in (1, 100, 360):
        assert p4.pols_commute(t) == pytest.approx(p4.pols_death(t), rel=1e-14)
        assert p4.claims(t, "COMMUTATION") == pytest.approx(
            p4.commute_pp(t) * p4.pols_death(t), rel=1e-14)
        # The administration expense collapses with the benefit: one payment, one
        # charge, instead of one charge per instalment for up to 420 months.
        assert p4.annuity_expenses(t) == pytest.approx(
            200.0 * p4.pols_commute(t), rel=1e-14)
    assert p4.check_annuity_ledger() is True


def test_pitfall_the_living_needs_cap_binds_early_not_late(income_guarantee):
    """The payout is the present value of an income stream, so the cap bites from month 1.

    That is the opposite pattern to a level sum assured, where a JPY 30,000,000 cap
    either always binds or never does.  On the anchor cell parameters the full 年金現価 at
    issue is JPY 56,352,381.90 and the cap stops binding only in month 209, once the
    unpaid stream has run down below it.
    """
    a = income_guarantee.Projection[1]
    n = a.term_m()
    assert a.commute_pp(1) == pytest.approx(56352381.90, abs=YEN)
    assert a.ln_benefit_pp(1) == pytest.approx(30000000.0, abs=1e-6)
    assert all(a.ln_benefit_pp(t) == pytest.approx(30000000.0, abs=1e-6)
               for t in (1, 100, 208))
    assert a.ln_benefit_pp(209) < 30000000.0
    assert a.ln_benefit_pp(209) == pytest.approx(29926898.32, abs=YEN)
    assert a.ln_benefit_pp(300) < a.ln_benefit_pp(209)
    # Barred in the final year before expiry.
    assert a.ln_benefit_pp(n - 12) > 0.0
    assert all(a.ln_benefit_pp(t) == 0.0 for t in range(n - 11, n + 1))


def test_pitfall_the_table_is_read_at_the_attained_age_on_the_death_basis(
        income_guarantee):
    """One rate, read at 満年齢 + elapsed policy years, from the 死亡保険用 table alone.

    The 契約年齢 is 満年齢 while the table is built for 保険年齢, so the base run reads early and
    understates; the bias is stated rather than corrected, and the optional shift must
    move q **up**.  The 年金開始後用 table has no role at all on this product, because the
    instalment stream is an annuity-certain.
    """
    a = income_guarantee.Projection[1]
    assert a.issue_age() == 30
    assert all(a.age(t) == 30 for t in range(1, 13))
    assert a.age(13) == 31 and a.age(25) == 32
    assert all(a.mort_rate_base(t) == pytest.approx(0.00068, rel=1e-14)
               for t in range(1, 13))
    assert a.mort_rate_base(13) == pytest.approx(0.00069, rel=1e-14)
    # No 保険年齢 shift is applied in the base run: the rate is the table rate scaled by
    # the two [std] factors and nothing else.
    assert a.mort_rate(1) == pytest.approx(0.80 * 0.70 * 0.00068, rel=1e-14)
    names = (set(income_guarantee.Projection.cells)
             | set(income_guarantee.Projection.refs))
    for absent in ("mort_rate_annuitant", "annuitant_mort_rate", "recipient_mort_rate",
                   "mort_table_post", "post_annuity_mort_rate"):
        assert absent not in names
    # The mortality basis is a single table keyed by sex and age.
    assert list(income_guarantee.Data.mort_table().index.names) == ["sex", "age"]


# ---------------------------------------------------------------------------
# Roll-forward identities and the check_* cells, on every shipped model point


def test_the_seven_check_cells_are_published_with_their_residuals(income_guarantee):
    """These seven identities, and no others, each with its per-month residual beside it.

    ``check_*`` takes no argument and returns a bool over all t; the per-t signed residual
    lives at ``check_*_resid(t)``.

    That they *hold*, on all nine points, is asserted in ``test_model_conventions_jp.py``:
    its sweep discovers every ``check_*`` generically and calls it on every model point of
    every model in the library, which is what stops an identity from holding on the anchor
    cell alone. Running them again here, on a second instance of the same model, meant a
    second cold projection of the whole table to reach a verdict already reached.

    What generic discovery cannot say is which checks ought to exist — a check that
    disappears simply stops being discovered — so that is the statement left here.
    """
    cells = set(income_guarantee.Projection.cells)
    checks = sorted(c for c in cells
                    if c.startswith("check_") and not c.endswith("_resid"))
    assert checks == ["check_annuity_ledger", "check_annuity_total",
                      "check_class_factor_norm", "check_expired_cover",
                      "check_net_cf", "check_pay_count", "check_pols_roll_fwd"]
    for check in checks:
        assert check + "_resid" in cells, check


def test_the_inforce_rollforward_closes_on_every_model_point(income_guarantee):
    """l(t) + reinstatements - l(t+1) = deaths + lapses + expiries, in every month.

    ``pols_maturity`` has no symbol in the notes; it names the survivors of the last
    month of cover, who neither die nor lapse — their cover simply runs out.  Without it
    the final month appears to lose lives with no cause.
    """
    for point_id in income_guarantee.Data.model_point_table().index:
        proj = income_guarantee.Projection[point_id]
        n = proj.term_m()
        for t in range(1, n + 1):
            out = proj.pols_death(t) + proj.pols_lapse(t) + proj.pols_maturity(t)
            got = proj.pols_if(t) + proj.pols_reinst(t + 1) - proj.pols_if(t + 1)
            assert got == pytest.approx(out, abs=1e-12), f"point {point_id}, t={t}"
            assert proj.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert all(proj.pols_maturity(t) == 0.0 for t in range(1, n))
        assert proj.pols_maturity(n) > 0.0


def test_maturity_is_an_expiry_and_pays_nothing(income_guarantee):
    """Nothing is payable on survival, at any duration, on this product.

    ``pols_maturity`` closes the roll-forward; it is bookkeeping, not a benefit.  There
    is no 満期保険金 and no ``claims_maturity`` column.
    """
    a = income_guarantee.Projection[1]
    n = a.term_m()
    assert "claims_maturity" not in a.result_cf().columns
    assert a.claims(n) == pytest.approx(a.claims(n, "ANNUITY"), rel=1e-14)
    assert a.pols_maturity(n) == pytest.approx(
        a.pols_if_at(n, "BEF_LAPSE") * (1 - a.lapse_rate_mth(n)), rel=1e-14)
    assert a.pols_if_at(n, "AFT_DECR") == 0.0
    assert a.pols_if(n + 1) == 0.0


def test_nothing_is_charged_to_the_in_force_population_after_expiry(income_guarantee):
    """Premiums, expenses, commission and new claims all vanish past the term.

    The annuity instalments and their administration expense do not, which is the
    asymmetry this product exists to model — and the reason ``expense_annuity`` is
    charged against the ledger rather than against ``pols_if``.
    """
    for point_id in income_guarantee.Data.model_point_table().index:
        proj = income_guarantee.Projection[point_id]
        assert proj.check_expired_cover() is True
        for t in range(proj.term_m() + 1, proj.proj_len() + 1):
            assert proj.check_expired_cover_resid(t) == pytest.approx(0.0, abs=1e-12)
            assert proj.pols_if(t) == 0.0
            assert proj.premiums(t) == 0.0
            assert proj.expenses(t) == 0.0
            assert proj.commissions(t) == 0.0
            assert proj.pols_death(t) == 0.0
            # The one expense that survives the term rides the ledger, not pols_if.
            assert proj.annuity_expenses(t) == pytest.approx(
                200.0 * proj.annuities_if(t), rel=1e-14)
    # On the anchor cell the tail is genuinely non-empty: 23 months of instalments and
    # of the administration expense that goes with them, after everything else is zero.
    a = income_guarantee.Projection[1]
    for t in range(a.term_m() + 1, a.proj_len() + 1):
        assert a.claims(t, "ANNUITY") > 0.0
        assert a.annuity_expenses(t) > 0.0


def test_the_rate_class_factors_normalize_to_the_all_lives_table(income_guarantee):
    """The mix-weighted mean of the four [std] class factors is 1.000.

    生保標準生命表2018 is an **all-lives** basis, so a class split whose weighted mean is not
    1.000 silently re-levels the whole table.  Holding the factors in one table rather
    than as a model point column is what makes the normalization checkable at all.
    """
    a = income_guarantee.Projection[1]
    assert a.check_class_factor_norm() is True
    assert a.check_class_factor_norm_resid(1) == pytest.approx(0.0, abs=1e-12)
    table = income_guarantee.Data.rate_class_table()
    assert sorted(table.index) == ["nonsmoker_preferred", "nonsmoker_standard",
                                   "smoker_preferred", "smoker_standard"]
    assert table["provenance"].notna().all()
    weighted = (table["class_factor"] * table["mix_weight"]).sum()
    assert weighted / table["mix_weight"].sum() == pytest.approx(1.0, abs=1e-12)
    assert "class_factor" not in income_guarantee.Data.model_point_table().columns


# ---------------------------------------------------------------------------
# The optional modules, in both positions


def test_commutation_is_off_in_the_base_run_and_on_at_point_4(income_guarantee):
    """Off: every claim opens a stream and no lump sum is paid.

    On: the annuity-certain factor is a(n) = v(1 - v^n)/(1 - v) at the [std] 0.65% p.a.
    commutation basis, and the resulting ratio at 300 remaining instalments is 0.922965
    against the 0.92133-0.92190 the published illustrations show.
    """
    a, p4 = income_guarantee.Projection[1], income_guarantee.Projection[4]
    horizon = a.proj_len()
    assert a.commutation() is False
    assert all(a.pols_commute(t) == 0.0 for t in range(1, horizon + 1))
    assert all(a.claims(t, "COMMUTATION") == 0.0 for t in range(1, horizon + 1))
    assert (a.result_cf()["claims_commutation"] == 0.0).all()

    v = (1 + 0.0065) ** (-1 / 12)
    assert a.commute_disc() == pytest.approx(v, rel=1e-14)
    for n in (24, 300, 420):
        assert a.annuity_certain_factor(n) == pytest.approx(
            v * (1 - v ** n) / (1 - v), rel=1e-12)
    assert a.annuity_certain_factor(0) == 0.0
    assert a.annuity_certain_factor(-5) == 0.0
    assert a.annuity_certain_factor(300) / 300 == pytest.approx(0.922965, abs=5e-7)
    assert a.commute_pp(1) / (150000.0 * 420) == pytest.approx(0.894482, abs=5e-7)

    assert p4.commutation() is True
    total = sum(p4.claims(t) for t in range(1, p4.proj_len() + 1))
    assert total > 0.0
    # Commuting at 0.65% is worth less than paying the instalments out undiscounted.
    uncommuted = sum(p4.annuity_mth() * p4.pols_death(s) * p4.pay_count(s)
                     for s in range(1, p4.term_m() + 1))
    assert total < uncommuted

    # The notes quote the module's effect on the anchor cell's own parameters: claim
    # outgo of JPY 414,176.30 against the JPY 443,313.69 instalment total, 93.43%.  The
    # decrements are untouched by the settlement route, so the counterfactual is built
    # from the anchor's claim vector directly.
    commuted = sum(a.commute_pp(s) * a.pols_death(s) for s in range(1, a.term_m() + 1))
    assert commuted == pytest.approx(414176.30, abs=YEN)
    assert commuted / TOTALS["claims_annuity"] == pytest.approx(0.9343, abs=5e-5)


def test_living_needs_is_off_in_the_base_run_and_on_at_point_5(income_guarantee):
    """Off: no acceleration, and D(t) opens a stream in full.

    On: a [std] proportion of the month's claims is carved **out** of the death
    decrement rather than added to it — the insured is by definition within six months
    of death, so an added decrement would double-count the benefit.
    """
    a, p5 = income_guarantee.Projection[1], income_guarantee.Projection[5]
    assert a.living_needs() is False
    assert all(a.pols_living_needs(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert (a.result_cf()["claims_living_needs"] == 0.0).all()

    assert p5.living_needs() is True
    take_up = income_guarantee.Projection.ln_take_up
    for t in (1, 100, 200):
        assert p5.pols_living_needs(t) == pytest.approx(
            take_up * p5.pols_death(t), rel=1e-14)
        # Carved out, not added: the three settlement routes partition the claims.
        assert (p5.annuities_open(t) + p5.pols_commute(t) + p5.pols_living_needs(t)
                == pytest.approx(p5.pols_death(t), rel=1e-14))
    assert any(p5.claims(t, "LIVING_NEEDS") > 0.0 for t in range(1, p5.proj_len() + 1))
    # An accelerated claim is one payment, so it carries one administration charge
    # alongside the instalments still running on the ledger.
    for t in (1, 100, 200):
        assert p5.annuity_expenses(t) == pytest.approx(
            200.0 * (p5.annuities_if(t) + p5.pols_living_needs(t)), rel=1e-14)
    # This stream is small enough that the JPY 30,000,000 cap does not bind.
    assert p5.ln_benefit_pp(1) < 30000000.0
    assert p5.check_annuity_ledger() is True


def test_waiver_of_premium_is_off_in_the_base_run_and_on_at_point_7(income_guarantee):
    """Off: every in-force policy pays.  On: a two-state chain thins the payers.

    The waiver is in the 主契約 rather than a rider, so it carries no extra premium; and
    because 別表4 is a materially lower bar than the 別表3 高度障害 schedule, its incidence is
    deliberately not ``mort_rate``.
    """
    a, p7 = income_guarantee.Projection[1], income_guarantee.Projection[7]
    assert a.wop() is False
    assert all(a.wop_waived_frac(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.pols_payer(t) == a.pols_if(t) for t in (1, 13, 240, 420))

    assert p7.wop() is True
    assert p7.wop_waived_frac(1) == 0.0
    assert p7.wop_waived_frac(3) > p7.wop_waived_frac(2) > 0.0
    assert p7.pols_payer(5) < p7.pols_if(5)
    assert p7.premiums(5) == pytest.approx(
        p7.prem_due_pp(5) * p7.pols_payer(5), rel=1e-14)
    inc = 1 - (1 - income_guarantee.Projection.wop_inc_rate) ** (1 / 12)
    rec = 1 - (1 - income_guarantee.Projection.wop_rec_rate) ** (1 / 12)
    equilibrium = inc / (inc + rec)
    assert 0.0 < p7.wop_waived_frac(p7.term_m()) < equilibrium
    # The incidence is not the mortality rate wearing another name.
    assert p7.wop_waived_frac(2) != pytest.approx(p7.mort_rate_mth(1), rel=1e-3)


def test_reinstatement_is_off_in_the_base_run_and_on_at_point_8(income_guarantee):
    """Off: a lapse is final.  On: a [std] share of lapses returns after the lag.

    Japanese policies really do come back — 復活 is available for three years from lapse,
    on fresh underwriting and arrears with interest — which is a genuine difference from
    the UK composite, where a lapsed policy terminates finally.
    """
    a, p8 = income_guarantee.Projection[1], income_guarantee.Projection[8]
    assert a.reinstatement() is False
    assert all(a.pols_reinst(t) == 0.0 for t in range(1, a.proj_len() + 1))

    assert p8.reinstatement() is True
    lag = income_guarantee.Projection.reinst_lag_m
    rate = income_guarantee.Projection.reinst_rate
    assert all(p8.pols_reinst(t) == 0.0 for t in range(1, lag + 1))
    assert p8.pols_reinst(lag + 1) == pytest.approx(rate * p8.pols_lapse(1), rel=1e-14)
    assert p8.pols_reinst(lag + 1) > 0.0
    assert lag <= income_guarantee.Projection.reinst_window_m
    # The arrears with interest arrive as premium income, not as a negative claim.
    assert p8.prem_arrears_pp() > lag * p8.premium_mth_pp()
    assert p8.premiums(lag + 1) == pytest.approx(
        p8.prem_due_pp(lag + 1) * p8.pols_payer(lag + 1)
        + p8.prem_arrears_pp() * p8.pols_reinst(lag + 1), rel=1e-14)
    # Reinstatement adds lives back, so the in-force is above the no-復活 roll-forward.
    assert p8.pols_if(lag + 1) > p8.pols_if_at(lag, "AFT_DECR")
    assert p8.check_pols_roll_fwd() is True


def test_selective_lapsation_is_off_in_the_base_run_and_works_when_switched_on(
        tmp_path):
    """q_eff(t) = q(t)[1 + lambda max(0, 1 - l(t)/l_ref)]; lambda = 0 in the base run.

    The mechanism is weaker here than on the protection chassis, which has a periodic
    no-underwriting renewal to select against, but it is not absent: the rate class is
    fixed at issue and cannot be changed, so a life whose health deteriorates keeps a
    preferred rate while a life whose health improves cannot get one and may re-shop.
    """
    model = model_copy(tmp_path, "IncomeTerm_JP_S_sel")
    try:
        base = model.Projection[1]
        assert model.Projection.sel_lapse_lambda == 0.0
        assert all(base.sel_lapse_factor(t) == 1.0 for t in (1, 120, 420))
        base_outgo = sum(base.claims(t, "ANNUITY")
                         for t in range(1, base.proj_len() + 1))
        assert base_outgo == pytest.approx(TOTALS["claims_annuity"], abs=YEN)

        model.Projection.sel_lapse_lambda = 0.25
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.sel_lapse_factor(1) == 1.0          # nothing has lapsed yet
        assert proj.sel_lapse_factor(120) == pytest.approx(
            1.0 + 0.25 * (1.0 - proj.pols_if(120) / 1.0), rel=1e-12)
        assert proj.sel_lapse_factor(420) > proj.sel_lapse_factor(120) > 1.0
        assert proj.mort_rate(120) > 0.000604800
        assert sum(proj.claims(t, "ANNUITY")
                   for t in range(1, proj.proj_len() + 1)) > base_outgo
        assert proj.check_pols_roll_fwd() is True
        assert proj.check_annuity_ledger() is True
    finally:
        model.close()


def test_the_base_run_has_every_module_off(income_guarantee):
    """The anchor cell reproduces the notes only because all five switches are down.

    Stated as its own test so that a module accidentally left on shows up here rather
    than as a mysterious difference in the worked example.
    """
    a = income_guarantee.Projection[1]
    assert (a.commutation(), a.living_needs(), a.wop(), a.reinstatement()) == (
        False, False, False, False)
    assert income_guarantee.Projection.sel_lapse_lambda == 0.0
    df = a.result_cf()
    assert (df["claims_commutation"] == 0.0).all()
    assert (df["claims_living_needs"] == 0.0).all()
    assert (df["claims_annuity"] > 0.0).all()


# ---------------------------------------------------------------------------
# Structural product facts


def test_the_benefit_is_an_annuity_certain(income_guarantee):
    """No survival condition on the instalments, so no post-event mortality basis.

    Confirmed from the contract side by a published factor table that depends on the
    payment period and explicitly not on the annuitant's age or sex.  This is the one
    place where a survivor-income product is *simpler* than a level term policy is
    complicated.
    """
    a = income_guarantee.Projection[1]
    n, g = a.term_m(), a.guar_m()
    # A stream's instalment count depends on the claim month alone.
    assert a.pay_count(1) == n
    assert a.pay_count(n) == g
    assert a.pay_count(n - g + 1) == g
    for m in (1, 50, n - g + 1):
        assert a.pay_end(m) == n
    for m in (n - g + 2, n):
        assert a.pay_end(m) == m + g - 1 > n
    # Total instalments reconcile to sum D(s) x n_pay(s) with no survivorship anywhere.
    built = sum(a.annuities_open(s) * a.pay_count(s) for s in range(1, n + 1))
    assert sum(a.annuities_if(t) for t in range(1, a.proj_len() + 1)) == pytest.approx(
        built, abs=1e-12)


def test_the_guarantee_equals_the_whole_term_at_point_8(income_guarantee):
    """The edge cell G = N: every claim pays exactly G instalments, whenever it arises.

    A 5-year term with a 5-year guarantee, so ``max(N - m + 1, G)`` collapses to G for
    every m and the projection is twice the term less one month.  An off-by-one in the
    guarantee arithmetic that hides inside a 420-month term is unmissable here.
    """
    p8 = income_guarantee.Projection[8]
    n, g = p8.term_m(), p8.guar_m()
    assert n == g == 60
    assert p8.proj_len() == 119
    for m in range(1, n + 1):
        assert p8.pay_count(m) == g
        assert p8.pay_end(m) == m + g - 1
    assert p8.check_pay_count() is True
    assert p8.check_annuity_ledger() is True
    assert p8.check_annuity_total() is True
    # The ledger still peaks at month N, where only the first claim's stream has ended.
    assert p8.annuities_if(n) == max(p8.annuities_if(t) for t in range(1, 120))


def test_premium_mode_is_a_timing_feature_not_an_inert_flag(income_guarantee):
    """12/f months of premium at the start of each payment period, no frequency discount.

    All three frequencies are contractual; the 前納 and frequency discounts are
    insurer-set and unpublished, so none is applied.  The anchor cell is 月払, which is
    the frequency the only published rate grid is quoted in.
    """
    monthly, annual, semi = (income_guarantee.Projection[1],
                             income_guarantee.Projection[3],
                             income_guarantee.Projection[6])
    assert (monthly.premium_mode(), annual.premium_mode(), semi.premium_mode()) == (
        "monthly", "annual", "semiannual")
    assert (monthly.prem_mode_months(), annual.prem_mode_months(),
            semi.prem_mode_months()) == (1, 12, 6)
    assert all(monthly.prem_due_pp(t) == monthly.premium_mth_pp() for t in range(1, 13))
    assert annual.prem_due_pp(1) == pytest.approx(12 * annual.premium_mth_pp(), rel=1e-14)
    assert all(annual.prem_due_pp(t) == 0.0 for t in range(2, 13))
    assert annual.prem_due_pp(13) == pytest.approx(12 * annual.premium_mth_pp(), rel=1e-14)
    assert semi.prem_due_pp(1) == pytest.approx(6 * semi.premium_mth_pp(), rel=1e-14)
    assert all(semi.prem_due_pp(t) == 0.0 for t in range(2, 7))
    assert semi.prem_due_pp(7) == pytest.approx(6 * semi.premium_mth_pp(), rel=1e-14)
    # No frequency discount: a year of premium costs the same at every frequency.
    for proj in (monthly, annual, semi):
        year_one = sum(proj.prem_due_pp(t) for t in range(1, 13))
        assert year_one == pytest.approx(12 * proj.premium_mth_pp(), rel=1e-14)


def test_lapse_relieves_the_liability_on_this_basis(tmp_path):
    """The sign of the lapse sensitivity is the opposite of the protection chassis's.

    On this assumption set expected claims exceed premiums, so lapse *relieves* the
    liability: undiscounted net cash flow is -JPY 269,617.32 at zero lapse against
    -JPY 103,051.56 on the [std] table.  A sensitivity whose sign flips with the basis
    needs both runs reported, not one.
    """
    import pandas as pd

    model = model_copy(tmp_path, "IncomeTerm_JP_S_nolapse")
    try:
        table = pd.read_csv(model.Data.input_dir() / "lapse_table.csv",
                            index_col="policy_year")
        table["lapse_rate"] = 0.0
        table.to_csv(model.Data.input_dir() / "lapse_zero.csv")
        model.Data.lapse_table_file = "lapse_zero.csv"
        model.Data.clear_all()
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.lapse_rate(1) == 0.0
        assert all(proj.pols_lapse(t) == 0.0 for t in range(1, proj.term_m() + 1))
        assert proj.result_cf()["net_cf"].sum() == pytest.approx(-269617.32, abs=YEN)
        assert proj.pols_maturity(proj.term_m()) > SURVIVORS
        assert proj.check_pols_roll_fwd() is True
    finally:
        model.close()


def test_the_mortality_basis_is_the_largest_lever_in_the_file(tmp_path):
    """Annuity outgo runs JPY 443,313.69 at the [std] basis and JPY 552,708.11 raw.

    The 0.80 best-estimate factor and the 0.70 rate-class factor multiply, and neither
    is narrowed by any retrieved document: the raw valuation table lifts claims by a
    quarter, and moving the class factor from 0.70 to 0.90 lifts them to
    JPY 568,289.70 — on a premium the carrier quotes for the cheapest class.
    """
    model = model_copy(tmp_path, "IncomeTerm_JP_S_basis")
    try:
        assert model.Projection.mort_be_factor == 0.8
        model.Projection.mort_be_factor = 1.0
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert sum(proj.claims(t, "ANNUITY")
                   for t in range(1, proj.proj_len() + 1)) == pytest.approx(
                       552708.11, abs=YEN)
        # class_factor 0.90 in place of 0.70, applied through the same product.
        model.Projection.mort_be_factor = 0.8 * 0.90 / 0.70
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert sum(proj.claims(t, "ANNUITY")
                   for t in range(1, proj.proj_len() + 1)) == pytest.approx(
                       568289.70, abs=YEN)
    finally:
        model.close()


def test_the_model_point_envelope_is_enforced_by_name(income_guarantee):
    """The accessors validate rather than propagating a bad value into a lookup.

    The composite's envelopes are product facts — issue age 20-70, expiry age 45-90,
    最低支払保証期間 from the menu {2年, 5年}, 年金月額 at least JPY 50,000 in JPY 10,000 steps —
    so a model point outside them is describing a product the composite does not have.
    """
    a = income_guarantee.Projection[1]
    with pytest.raises(FormulaError):
        a.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        a.claims(1, "SURRENDER")
    table = income_guarantee.Data.model_point_table()
    assert (table["issue_age"].between(20, 70)).all()
    assert (table["expiry_age"].between(45, 90)).all()
    assert (table["expiry_age"] > table["issue_age"]).all()
    assert set(table["guar_m"]) <= {24, 60}
    assert (table["annuity_mth"] >= 50000).all()
    assert (table["annuity_mth"] % 10000 == 0).all()
    assert set(table["premium_mode"]) <= {"monthly", "semiannual", "annual"}
    assert set(table["sex"]) <= {"M", "F"}
    assert "policy_id" in table.columns
    assert table.index.name == "point_id"
    assert list(table.index)[0] == 1


def test_result_cf_shape_and_decomposition(jp_income_anchor):
    """The columns are a decomposition of net_cf, and pols_if leads them.

    ``claims_lapse`` is in the table and identically zero by product design;
    ``annuities_if`` sits beside ``pols_if`` because a reader needs both to make sense
    of any row, and must never add them.

    There is **no bare ``claims`` subtotal column** beside the ``claims_*`` splits: a
    statement that publishes its own subtotal next to its parts stops summing to
    ``net_cf`` unless the reader knows which column to skip.  ``check_net_cf()`` is the
    model's own form of the same assertion.  And there is **no ``claims_death``
    column**, because the contract pays no lump sum on death — the whole death benefit
    is ``claims_annuity``.
    """
    df = jp_income_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "annuities_if", "premiums", "claims_annuity",
        "claims_commutation", "claims_living_needs", "claims_lapse",
        "claim_expenses", "annuity_expenses", "expenses", "commissions", "net_cf",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, 444))
    assert "claims" not in df.columns
    assert "claims_death" not in df.columns
    assert jp_income_anchor.check_net_cf() is True
    outgo = df[["claims_annuity", "claims_commutation", "claims_living_needs",
                "claims_lapse", "claim_expenses", "annuity_expenses",
                "expenses", "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    assert df.loc[1, "net_cf"] == pytest.approx(WORKED_EXAMPLE[1][8], abs=YEN)


def test_net_cf_carries_the_notes_own_income_positive_sign(income_guarantee):
    """The notes write "+ = inflow", which is already the library-wide convention.

    So there is no outgo-positive ``liability_cf`` companion here, unlike the models
    whose notes print the other sign.
    """
    assert "liability_cf" not in income_guarantee.Projection.cells
    a = income_guarantee.Projection[1]
    assert a.net_cf(2) > 0.0
    assert a.net_cf(1) < 0.0
    assert a.net_cf(1) == pytest.approx(
        a.premiums(1) - a.claims(1) - a.claim_expenses(1) - a.annuity_expenses(1)
        - a.expenses(1) - a.commissions(1), abs=1e-9)


def test_the_inputs_live_beside_the_model_and_mark_their_provenance():
    """Four external CSVs, and every assumption row says where its value came from.

    ``model_point_table.csv`` deliberately carries no ``provenance`` column: a model
    point table is not an assumption table, and which premiums are published and which
    are [std] is recorded in ``model.md``.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
                "rate_class_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}
    for name in ("mort_table.csv", "lapse_table.csv", "rate_class_table.csv"):
        table = pd.read_csv(MODEL_DIR.parent / name)
        assert "provenance" in table.columns
        assert table["provenance"].notna().all()
        assert (table["provenance"].str.len() > 0).all()
    assert "provenance" not in pd.read_csv(
        MODEL_DIR.parent / "model_point_table.csv").columns
    # UTF-8 without a BOM, so the files read the same everywhere.
    for name in expected:
        with open(MODEL_DIR.parent / name, "rb") as f:
            assert not f.read(3).startswith(b"\xef\xbb\xbf")


def test_the_docstrings_carry_the_facts_a_reader_relies_on(income_guarantee):
    """Claims a reader relies on, asserted so they cannot go stale silently."""
    doc = income_guarantee.doc
    assert "mechanics demonstration" in doc
    assert "external" in doc
    assert "once per model" in doc
    assert "収入保障保険" in doc
    proj = income_guarantee.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "annuities_if", "pay_count", "pay_end",
                  "pols_maturity", "mort_rate_mth", "lapse_rate_mth"):
        assert cells in proj, f"{cells} missing from the Projection docstring"
    data = income_guarantee.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table"):
        assert cells in data


def test_round_trip_reproduces_the_goldens(tmp_path):
    """read -> write -> re-read reproduces the worked example and the docstrings.

    Inputs are external, so they must travel with the model; that is the trade-off this
    layout makes, and it is worth asserting in both directions.
    """
    model = mx.read_model(MODEL_DIR, name="IncomeTerm_JP_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="IncomeTerm_JP_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.annuities_if(t) == pytest.approx(row[3], abs=LEDGER)
            assert anchor.net_cf(t) == pytest.approx(row[8], abs=YEN)
        assert anchor.check_annuity_ledger() is True
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()
