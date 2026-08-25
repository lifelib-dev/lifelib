"""Golden and structural tests for Medical_JP_S.

The golden values are the worked example in ``products/medical/technical-notes.md``
("Worked example"), which projects the anchor cell: male, 契約年齢 40 on a 満年齢 basis,
終身 chassis, 入院給付金日額 JPY 5,000, a 60-day per-hospitalization limit, a 1,095-day
通算 limit per limb, 終身払 at an office premium of JPY 2,100 a month, 手術給付金 at
20x / 5x, the 先進医療特約 attached and every other module off.  They are hard-coded
here rather than pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the yen-cent, in-force to
six decimals, benefit-day ledgers to four decimals of a day.

Beyond the worked example this module asserts every product fact the notes list under
**Known modeling pitfalls**, because each of them is a way an implementation can look
right and be wrong.  This product invites more of them than a death-benefit product
does, because it prices **frequency x severity x limit** rather than a sum assured:

* 入院受療率 is a point-in-time *prevalence*, not a claim frequency;
* the five-day minimum is an *amount*, so it never touches the 通算 day ledger;
* the per-hospitalization limit is applied inside the stay expectation, spell by spell,
  and not to an annual total;
* the two 通算 ledgers are carried per *surviving policy* and there are two of them,
  because the limit runs separately on the 疾病 and 災害 limbs;
* there is no death benefit, no surrender value and hence no 自動振替貸付 to import
  from the savings chassis.

Each pitfall test is named after the pitfall it protects.
"""
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from jp_registry import model_path

MODEL_DIR = model_path("Medical_JP_S")

YEN = 0.005           # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.
DAY = 5e-5            # day ledgers displayed to 4 d.p.


# The notes' worked-example table, verbatim.
# t: (pols_if, premiums, claims_hosp, claims_surgery, claims_advanced,
#     expenses, claim_expenses, commissions, net_cf, agg_days_dis)
WORKED_EXAMPLE = {
    0: (1.000000, 2100.00, 295.25, 150.54, 5.50, 20250.00, 11.65, 37800.00,
        -56412.95, 0.0000),
    1: (0.992093, 2083.40, 292.92, 149.35, 5.46, 248.02, 11.56, 0.00, 1376.09,
        0.0543),
    2: (0.984249, 2066.92, 290.60, 148.17, 5.41, 246.06, 11.47, 0.00, 1365.20,
        0.1087),
    3: (0.976466, 2050.58, 288.30, 147.00, 5.37, 244.12, 11.38, 0.00, 1354.41,
        0.1630),
}

# The notes' policy-year-1 aggregate, t = 0..11, all at age 40 and all in policy year 1
# — the strongest single target in the notes, because it exercises the whole annual
# cycle on one set of rates.  Sums of unrounded monthly values, as the notes say.
YEAR_ONE = {
    "premiums": 24132.47,
    "claims_hosp": 3392.94,
    "claims_surgery": 1729.95,
    "claims_advanced": 63.20,
    "expenses": 22872.91,
    "claim_expenses": 133.93,
    "commissions": 37800.00,
    "net_cf": -41860.47,
}
YEAR_ONE_SUM_POLS_IF = 11.491651
YEAR_ONE_END = {
    "pols_if": 0.909136,
    "agg_days_dis": 0.651917,
    "agg_days_acc": 0.056688,
    "adv_paid": 60.00,
}

# Every assumption value the notes' worked example quotes, in the order it quotes them.
# 第三分野標準生命表2018 男 q40 is the one *sourced* rate here [R4] [REG-R18]; the rest
# are [std] constructions or [std] conversions of published 患者調査 statistics.
Q40_TABLE = 0.00076             # the quoted table rate
MORT_RATE_40 = 0.00095          # 1.25 x the table rate [std]
MORT_RATE_MTH_40 = 0.0000792012
LAPSE_RATE_Y1 = 0.09
LAPSE_RATE_MTH_Y1 = 0.0078284203
INC_RATE_40 = 0.046618812
INC_RATE_MTH_40 = 0.0038849010
D_RAW_35_64 = 20.20             # sourced 平均在院日数 for the 35-64 band [REG-R27]
D_PAY_35_64_L60 = 15.20         # after the 60-day per-hospitalization limit
SURG_PER_HOSP = 38750.0         # 5,000 x (0.35 x 20 + 0.15 x 5)
ADV_PER_EVENT = 165000.0        # 150,000 + min(10%, 500,000)
ADV_FREQ_MTH = 0.0000333333
PROJ_LEN_ANCHOR = 924           # 12 x (116 - 40 + 1), the male terminal age


CHECKS = ("check_pols_roll_fwd", "check_agg_days", "check_day_limits",
          "check_adv_ledger", "check_lump_ledger", "check_waiver_roll_fwd",
          "check_net_cf")


def _sandbox(tmp_path, name):
    """A private copy of the model *and its external CSVs*, safe to mutate.

    Inputs are external files resolved from ``_model.path.parent``, so a test that wants
    to change an input has to move the whole arrangement rather than edit the shipped
    one.  Copying it into ``tmp_path`` keeps the product directory untouched.
    """
    dest = tmp_path / MODEL_DIR.name
    shutil.copytree(MODEL_DIR, dest)
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)
    return mx.read_model(dest, name=name)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(jp_medical_anchor, t):
    """Every cell of the notes' four-row table, to the precision the notes display."""
    (pols, prem, hosp, surg, adv, exp, cexp, comm, net, agg) = WORKED_EXAMPLE[t]
    a = jp_medical_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=YEN)
    assert a.claims(t, "HOSP") == pytest.approx(hosp, abs=YEN)
    assert a.claims(t, "SURGERY") == pytest.approx(surg, abs=YEN)
    assert a.claims(t, "ADVANCED") == pytest.approx(adv, abs=YEN)
    assert a.expenses(t) == pytest.approx(exp, abs=YEN)
    assert a.claim_expenses(t) == pytest.approx(cexp, abs=YEN)
    assert a.commissions(t) == pytest.approx(comm, abs=YEN)
    assert a.net_cf(t) == pytest.approx(net, abs=YEN)
    assert a.agg_days_dis(t) == pytest.approx(agg, abs=DAY)


def test_worked_example_assumption_basis(jp_medical_anchor):
    """Every assumption value the notes quote before the table, in one place.

    The notes quote 第三分野標準生命表2018 男 q40 = 0.00076 because a worked example
    needs it, and build everything else from it or from 患者調査.  If the shipped tables
    drift, the worked example stops being reproducible and this is where that shows.
    """
    a = jp_medical_anchor
    assert a.proj_len() == PROJ_LEN_ANCHOR
    assert a.mort_rate_at_age(40) == pytest.approx(Q40_TABLE, rel=1e-12)
    assert a.mort_rate(0) == pytest.approx(MORT_RATE_40, rel=1e-12)
    assert a.mort_rate_mth(0) == pytest.approx(MORT_RATE_MTH_40, abs=5e-11)
    assert a.lapse_rate(0) == pytest.approx(LAPSE_RATE_Y1, rel=1e-12)
    assert a.lapse_rate_mth(0) == pytest.approx(LAPSE_RATE_MTH_Y1, abs=5e-11)
    assert a.inc_rate(0) == pytest.approx(INC_RATE_40, abs=5e-10)
    assert a.inc_rate_mth(0) == pytest.approx(INC_RATE_MTH_40, abs=5e-11)
    assert a.d_raw(0) == pytest.approx(D_RAW_35_64, abs=5e-9)
    assert a.d_pay(0) == pytest.approx(D_PAY_35_64_L60, abs=5e-9)
    assert a.d_ben(0) == pytest.approx(D_PAY_35_64_L60, abs=5e-9)   # floor is off
    assert a.adv_freq_mth() == pytest.approx(ADV_FREQ_MTH, abs=5e-11)


def test_worked_example_month_zero_trace(jp_medical_anchor):
    """The notes' month-0 trace, line by line, as products rather than as totals.

    claims_hosp = D x d_ben x i(0), and the 92/8 limb split leaves it unchanged because
    both limbs carry the same daily amount and the same stay distribution — which is the
    reason the split is economically inert in the cash flows and structurally essential
    in the ledgers.
    """
    a = jp_medical_anchor
    assert a.pols_if(0) == 1.0
    assert a.premiums(0) == pytest.approx(2100.00, abs=YEN)
    assert a.claims(0, "HOSP") == pytest.approx(
        5000.0 * 15.20 * INC_RATE_MTH_40, abs=YEN)
    assert 0.92 * a.d_ben_dis(0) + 0.08 * a.d_ben_acc(0) == pytest.approx(
        a.d_ben(0), rel=1e-14)
    assert a.claims(0, "SURGERY") == pytest.approx(
        INC_RATE_MTH_40 * SURG_PER_HOSP, abs=YEN)
    assert a.claims(0, "ADVANCED") == pytest.approx(
        ADV_FREQ_MTH * ADV_PER_EVENT, abs=YEN)
    # expenses is acquisition + maintenance only; the claim expense is its own line.
    assert a.claim_expenses(0) == pytest.approx(3000.0 * INC_RATE_MTH_40, abs=YEN)
    assert a.expenses(0) == pytest.approx(250.0 + 20000.0, abs=YEN)
    assert a.commissions(0) == pytest.approx(1.5 * 12 * 2100.0, abs=YEN)
    # Ledgers at the end of month 0, per surviving policy.
    assert a.agg_days_dis(1) == pytest.approx(0.054326, abs=DAY)
    assert a.agg_days_acc(1) == pytest.approx(0.004724, abs=DAY)
    assert a.adv_paid(1) == pytest.approx(5.00, abs=YEN)
    assert a.term_rate(0) == 0.0


def test_worked_example_inforce_update(jp_medical_anchor):
    """l(t+1) = l(t)(1 - q)(1 - w), mortality then lapse, the notes' order."""
    a = jp_medical_anchor
    assert a.pols_if(1) == pytest.approx(
        (1 - MORT_RATE_MTH_40) * (1 - LAPSE_RATE_MTH_Y1), abs=INFORCE)
    assert a.pols_if(2) == pytest.approx(a.pols_if(1) ** 2, rel=1e-14)
    assert a.pols_if(3) == pytest.approx(a.pols_if(1) ** 3, rel=1e-13)


def test_worked_example_policy_year_one_totals(jp_medical_anchor):
    """The notes' policy-year-1 aggregate, line by line, on unrounded monthly values.

    Twelve months at one age on one set of rates, so this exercises the whole annual
    cycle: the level premium, the incidence basis, both surgery limbs, the 先進医療
    rider, the inflating maintenance expense, the acquisition strain and the fact that
    renewal commission has not yet started.
    """
    df = jp_medical_anchor.result_cf().iloc[:12]
    for line, total in YEAR_ONE.items():
        assert df[line].sum() == pytest.approx(total, abs=YEN), line
    assert df["pols_if"].sum() == pytest.approx(YEAR_ONE_SUM_POLS_IF, abs=INFORCE)
    # Renewal commission starts at t = 12, so year 1 is the initial commission alone.
    assert (df["commissions"].iloc[1:] == 0.0).all()


def test_worked_example_year_one_closing_state(jp_medical_anchor):
    """The notes' state at the first anniversary: in force, both ledgers, 先進医療.

    ``pols_if(12)`` is exactly 0.99905 x 0.91 = 0.9091355, a half-unit tie at six
    decimals: the notes display it rounded half away from zero as 0.909136 while Python
    rounds half to even and shows 0.909135.  The tolerance is a half unit plus the tie,
    so a genuine drift still fails while the tie does not.
    """
    a = jp_medical_anchor
    assert a.pols_if(12) == pytest.approx(0.99905 * 0.91, rel=1e-14)
    assert a.pols_if(12) == pytest.approx(YEAR_ONE_END["pols_if"], abs=5.05e-7)
    assert a.agg_days_dis(12) == pytest.approx(YEAR_ONE_END["agg_days_dis"], abs=DAY)
    assert a.agg_days_acc(12) == pytest.approx(YEAR_ONE_END["agg_days_acc"], abs=DAY)
    assert a.adv_paid(12) == pytest.approx(YEAR_ONE_END["adv_paid"], abs=YEN)


def test_year_one_claims_are_a_fifth_of_year_one_premium(jp_medical_anchor):
    """The notes' reading of the numbers: 21.5% of premium at age 40.

    A level premium on a whole-of-life morbidity cost prefunds heavily at the young ages,
    which is the economic shape the aggregate limit and the lifetime horizon exist to
    carry.  Asserted rather than described.
    """
    df = jp_medical_anchor.result_cf().iloc[:12]
    claims = df[["claims_hosp", "claims_surgery", "claims_advanced"]].sum().sum()
    assert claims == pytest.approx(5186.09, abs=YEN)
    assert claims / df["premiums"].sum() == pytest.approx(0.215, abs=0.0005)


def test_new_business_strain_then_thin_margins(jp_medical_anchor):
    """A deep month-0 strain, then positive margins that thin with age.

    JPY 57,800 of acquisition expense and initial commission fall against one month's
    premium of JPY 2,100, and the margin that recovers them thins as incidence rises
    13.8-fold between age 40 and 90 and over.
    """
    a = jp_medical_anchor
    assert a.net_cf(0) < -56000.0
    assert a.expenses(0) + a.commissions(0) - a.expense_maint_pp(0) == pytest.approx(
        57800.0, abs=YEN)
    assert all(a.net_cf(t) > 0.0 for t in (1, 2, 3, 12, 60))
    assert a.net_cf(a.proj_len() - 1) < a.net_cf(12)
    assert a.inc_rate(12 * 50) / a.inc_rate(0) == pytest.approx(13.8, abs=0.05)


# ---------------------------------------------------------------------------
# Known modeling pitfalls, one test each


def test_pitfall_juryoritsu_is_a_prevalence_not_an_incidence(medical):
    """入院受療率 is a point-in-time count per 100,000, not an annual claim frequency.

    The notes call this the single commonest error in a Japanese medical model.  The
    conversion ``inc = (juryoritsu / 100,000) x 365 / alos`` is an explicit [std] step
    flagged as needed by the source itself [REG-R26]; at age 40 it turns 0.00258 into
    0.046619, a factor of 18.07.  A model that used the published figure directly, or
    multiplied it straight by the daily amount, would be out by that factor.
    """
    a = medical.Projection[1]
    table = medical.Data.incidence_table()
    row = table.loc[40]
    prevalence = row["juryoritsu_per_100k"] / 100000.0
    assert prevalence == pytest.approx(0.00258, rel=1e-12)
    assert a.inc_rate(0) == pytest.approx(
        prevalence * 365.0 / row["alos_days"], rel=1e-12)
    assert a.inc_rate(0) / prevalence == pytest.approx(18.069, abs=0.001)
    # The daily benefit multiplies *days*, never the prevalence: the model reached for
    # the prevalence would understate the month's hospitalization claim eighteenfold.
    naive = a.pols_if(0) * a.daily_amount() * a.d_ben(0) * prevalence / 12.0
    assert a.claims(0, "HOSP") / naive == pytest.approx(18.069, abs=0.001)


def test_pitfall_the_five_day_minimum_is_an_amount_not_five_days(medical):
    """The floor raises the benefit and adds nothing to the 通算 ledger.

    The carriers write it as 「入院給付金日額×5」 [S4] [S6] [S7] — a payment, not a
    credit of five days — so it enters ``d_ben`` and never ``d_pay``.  Crediting it to
    the ledger would let a two-day stay consume five days of a lifetime limit it never
    used.  On the notes' 35-64 row with a 60-day limit that is 16.10 benefit days
    against 15.20 ledger days.
    """
    a = medical.Projection[1]
    days, probs = a.los_days(35), a.los_probs(35)
    with_floor = sum(p * max(5.0, min(g, 60)) for g, p in zip(days, probs))
    without = sum(p * min(g, 60) for g, p in zip(days, probs))
    assert without == pytest.approx(15.20, abs=5e-9)
    assert with_floor == pytest.approx(16.10, abs=5e-9)

    # Model point 8 carries the floor: benefit days exceed ledger days, and the ledger
    # advances on the ledger days.
    p8 = medical.Projection[8]
    assert p8.min_days_5() is True
    assert p8.d_ben(0) > p8.d_pay(0)
    assert p8.d_ben(0) == pytest.approx(24.07, abs=5e-9)
    assert p8.d_pay(0) == pytest.approx(23.50, abs=5e-9)
    assert p8.agg_days_dis(1) - p8.agg_days_dis(0) == pytest.approx(
        p8.inc_rate_mth(0) * 0.92 * p8.d_pay_dis(0), rel=1e-14)
    assert p8.agg_days_dis(1) - p8.agg_days_dis(0) != pytest.approx(
        p8.inc_rate_mth(0) * 0.92 * p8.d_ben(0), rel=1e-6)
    # The anchor has the floor off, so the two coincide there.
    assert a.min_days_5() is False
    assert a.d_ben(0) == pytest.approx(a.d_pay(0), rel=1e-14)


def test_pitfall_l1_is_applied_inside_the_stay_expectation(medical):
    """Cap each stay, not the mean of the stays.

    ``Sum_j pi_j min(g_j, L1) = 15.20`` but ``min(Sum_j pi_j g_j, L1) = min(20.20, 60)
    = 20.20``: capping a mean instead of capping each spell silently removes the limit
    altogether.  The 60-day limit removes 24.75% of raw days on the 35-64 row and 33.8%
    on the 65+ row, so the difference is a quarter of the day benefit, not a rounding.
    """
    a, p8 = medical.Projection[1], medical.Projection[8]
    assert a.d_pay_capped(0) == pytest.approx(15.20, abs=5e-9)
    assert min(a.d_raw(0), a.limit_per_hosp()) == pytest.approx(20.20, abs=5e-9)
    assert 1.0 - a.d_pay_capped(0) / a.d_raw(0) == pytest.approx(0.2475, abs=5e-5)
    assert 1.0 - p8.d_pay_capped(0) / p8.d_raw(0) == pytest.approx(0.338, abs=5e-4)
    # No expectation may exceed the limit, in any month, on any model point.
    for point_id in medical.Data.model_point_table().index:
        proj = medical.Projection[point_id]
        assert proj.check_day_limits() is True
        assert all(proj.d_pay_capped(t) <= proj.limit_per_hosp() + 1e-12
                   for t in range(0, proj.proj_len(), 37))


def test_pitfall_the_agg_ledger_is_per_surviving_policy(jp_medical_anchor):
    """The 通算 ledger is one policyholder's consumption, not the block's.

    Weighting it by ``pols_if`` would measure the block and defer the limit forever.  At
    t = 600 the anchor cell has 5.5% of the original cohort left, so a weighted ledger
    would advance eighteen times more slowly than the correct one — and the ledger keeps
    advancing at full speed while the in-force probability falls away.
    """
    a = jp_medical_anchor
    t = 600
    unweighted = a.inc_rate_mth(t) * 0.92 * a.d_pay_dis(t)
    assert a.agg_days_dis(t + 1) - a.agg_days_dis(t) == pytest.approx(
        unweighted, rel=1e-12)
    assert a.pols_if(t) < 0.06
    assert a.agg_days_dis(t + 1) - a.agg_days_dis(t) > 15.0 * (
        a.pols_if(t) * unweighted)
    assert a.check_agg_days() is True
    # result_days() publishes the ledgers on that basis, so the reader can see it.
    days = a.result_days()
    assert days.loc[t, "agg_days_dis"] == pytest.approx(a.agg_days_dis(t), rel=1e-14)


def test_pitfall_two_ledgers_not_one(jp_medical_anchor):
    """The 通算 limit runs separately on the 疾病 and 災害 limbs, and both must fill.

    The limbs consume in the [std] 92 / 8 ratio, so the 災害 ledger fills 11.5 times
    more slowly and it — not the 疾病 ledger — governs termination.  A single combined
    ledger would stand at 53.6% of the limit at the horizon where the binding limb
    stands at 4.3%, and would terminate the contract far earlier than the contract does.
    """
    a = jp_medical_anchor
    last = a.proj_len() - 1
    dis, acc = a.agg_days_dis(last), a.agg_days_acc(last)
    assert dis / acc == pytest.approx(0.92 / 0.08, rel=1e-9)
    combined = (dis + acc) / a.limit_agg()
    binding = min(dis, acc) / a.limit_agg()
    assert combined == pytest.approx(0.536, abs=0.001)
    assert binding == pytest.approx(0.043, abs=0.001)
    assert combined / binding == pytest.approx(12.5, rel=1e-6)
    # Termination needs both limbs, so the 災害 limb is what defers it.
    assert all(a.term_rate(t) == 0.0 for t in range(0, a.proj_len(), 13))


def test_pitfall_the_ledgers_are_live_though_they_read_zero(tmp_path):
    """Do not delete a ledger because it never binds on the shipped expectation.

    ``E[min(Sum, LA)] != min(E[Sum], LA)``, so the deterministic ledger understates the
    limit rather than showing it is absent.  Re-read against a model point whose 通算
    limit is five days and the machinery bites immediately: the paid days are cut to the
    room left, the ledger stops at the limit instead of overflowing it, and the benefit
    days scale down with them.  ``Cancer_JP_S`` and ``LTC_JP_S`` inherit this code with
    limits that do bind.

    The termination indicator still never fires, and that is a property of the
    expectation and not a defect: the ledger advances by ``i x s x min(d_pay, room)``,
    which is a fraction of the room left, so it approaches ``LA`` geometrically and
    never reaches it.  On a seriatim or stochastic run it does.
    """
    model = _sandbox(tmp_path, "Medical_JP_S_bind")
    try:
        table = model.Data.model_point_table()
        tight = table.loc[[1]].copy()
        tight["limit_agg"] = 5
        alt = "model_point_table_tight.csv"
        tight.to_csv(model.Data.input_dir() / alt)
        model.Data.model_point_file = alt
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[1]

        assert p.limit_agg() == 5.0
        assert p.d_pay(0) == pytest.approx(15.20, abs=5e-9)
        assert p.room_dis(0) == 5.0
        assert p.d_pay_dis(0) == 5.0                    # cut to the room left
        assert p.d_ben_dis(0) == pytest.approx(15.20 * 5.0 / 15.20, abs=5e-9)
        assert p.agg_days_dis(1) == pytest.approx(
            p.inc_rate_mth(0) * 0.92 * 5.0, rel=1e-12)
        last = p.proj_len() - 1
        assert p.agg_days_dis(last) < p.limit_agg()     # asymptote, never an overflow
        assert p.agg_days_dis(last) > 0.9 * p.limit_agg()
        assert all(p.term_rate(t) == 0.0 for t in range(0, p.proj_len(), 29))
        for check in CHECKS:
            assert getattr(p, check)() is True, check
    finally:
        model.close()


def test_pitfall_radiation_is_not_a_separate_claim_stream(medical):
    """放射線治療 is folded into 手術給付金, not paid as a benefit of its own.

    The composite pays it through the 放射線治療料 limb of the surgery trigger, subject
    to the 60-day lockout every carrier imposes [S1] [S2] [S6] [S9] [S10], so it sits
    inside the [std] 0.35 in-hospital surgery frequency.  One carrier does pay a
    separate 放射線治療給付金 at 日額 x 10 [S4]; adding that limb here double-counts.
    """
    names = set(medical.Projection.cells) | set(medical.Projection.refs)
    assert not [n for n in names if "radiation" in n or n.startswith("rad_")]
    a = medical.Projection[1]
    kinds = ("HOSP", "SURGERY", "ADVANCED", "LUMP", "LAPSE")
    assert a.claims(0) == pytest.approx(sum(a.claims(0, k) for k in kinds), rel=1e-14)
    assert set(a.result_cf().columns) & {"claims_radiation"} == set()
    assert "放射線治療" in medical.Projection.cells["surg_ih_eff"].doc


def test_pitfall_surgery_after_the_day_limit_is_a_switch_not_a_default(medical):
    """Where the day limit is exhausted, one carrier pays surgery and another does not.

    A contradiction between carriers, not a gap: the composite pays [S4], and the
    alternative [S10] is carried as ``surg_after_limit``.  Reversed, and with surgeries
    assumed uniform over stay-days [std], the truncated day fraction 1 - 15.20/20.20 =
    24.75% of in-hospital surgeries falls outside cover.  The two positions differ by a
    quarter of the in-hospital surgery benefit and cannot be rounded into each other.
    """
    a, p5 = medical.Projection[1], medical.Projection[5]
    assert a.surg_after_limit() is True
    assert a.surg_ih_eff(0) == pytest.approx(0.35, rel=1e-12)

    assert p5.surg_after_limit() is False
    assert p5.surg_ih_eff(0) == pytest.approx(
        0.35 * p5.d_pay_capped(0) / p5.d_raw(0), rel=1e-12)
    assert p5.surg_ih_eff(0) == pytest.approx(0.2634, abs=5e-5)
    assert p5.surg_ih_eff(0) / 0.35 == pytest.approx(0.7525, abs=5e-5)
    assert 1.0 - p5.surg_ih_eff(0) / 0.35 == pytest.approx(0.2475, abs=5e-5)


def test_pitfall_no_surrender_value_no_apl_no_policy_loan(medical):
    """A missed premium really does lapse the policy on this chassis.

    The main contract is 無解約返戻金型 during the premium-paying period, which under
    終身払 is every duration [S1] [S6] [S9], and neither 契約者貸付 nor 自動振替貸付 is
    offered [S1].  So ``claims(t, "LAPSE")`` is identically zero and no lapse-suppression
    term belongs in the recursion — importing ``WholeLife_JP_A``'s automatic-premium-loan
    machinery here would suppress lapses that genuinely happen.
    """
    names = set(medical.Projection.cells) | set(medical.Projection.refs)
    for absent in ("apl", "apl_balance", "policy_loan", "loan_balance", "av_pp",
                   "prem_to_av_pp"):
        assert absent not in names, f"{absent} is savings-chassis machinery"

    for point_id in medical.Data.model_point_table().index:
        proj = medical.Projection[point_id]
        if proj.prem_period_type() == "to_65":
            continue
        df = proj.result_cf()
        assert (df["claims_lapse"] == 0.0).all(), point_id
        assert all(proj.cv_pp(t) == 0.0 for t in range(0, proj.proj_len(), 41))
        # Lapse moves the in-force and nothing else.
        assert proj.pols_lapse(0) > 0.0


def test_pitfall_no_death_benefit(medical):
    """Mortality is a pure liability release; a claims_death column is a benefit that
    does not exist.

    The main contract pays nothing on death [S1] [S4] [S6] [S9] [S10], which is why
    death appears only as a decrement and why ``mort_be_factor`` scales the valuation table
    *up* rather than down: an understatement of mortality on a health product overstates
    the liability.
    """
    names = set(medical.Projection.cells) | set(medical.Projection.refs)
    assert "claims_death" not in names
    a = medical.Projection[1]
    assert "claims_death" not in a.result_cf().columns
    with pytest.raises(FormulaError):
        a.claims(0, "DEATH")
    assert a.pols_death(0) > 0.0
    assert a.mort_be_factor == 1.25
    assert a.mort_rate(0) > a.mort_rate_base(0)


def test_pitfall_the_standard_table_excludes_severe_disability(medical):
    """高度障害 cannot be read out of 第三分野標準生命表2018, so the waiver carries its own
    incidence.

    The 2018 table excludes 高度障害, unlike its 2007 predecessor [R5] [REG-R20], and no
    public Japanese 高度障害 incidence table was retrieved.  The base disability waiver
    therefore has incidence zero in **every** run of this model, not merely the base one,
    and the elected 特定三疾病 特則 runs on a stated [std] placeholder rather than on the
    mortality table's own rate.
    """
    for point_id in medical.Data.model_point_table().index:
        proj = medical.Projection[point_id]
        if proj.waiver_3dis():
            continue
        assert all(proj.waiver_inc_mth(t) == 0.0
                   for t in range(0, proj.proj_len(), 31)), point_id
        assert all(proj.waived(t) == 0.0 for t in range(0, proj.proj_len(), 31))
    p7 = medical.Projection[7]
    assert p7.waiver_3dis() is True
    assert p7.waiver_inc_mth(0) == pytest.approx(
        0.25 * p7.mort_rate(0) / 12.0, rel=1e-14)
    assert p7.waiver_inc_mth(0) != pytest.approx(p7.mort_rate_mth(0), rel=1e-6)


def test_pitfall_the_kata_is_fixed_at_issue(medical):
    """L1, LA and the 三大疾病無制限 特則 are elected at issue and never change.

    They can never be varied after issue [S2] [S4] [S9], so they are model point
    attributes and take no ``t``: a cells that varied them over the projection would
    model a contract term that does not exist.
    """
    cells = medical.Projection.cells
    for name in ("limit_per_hosp", "limit_agg", "tokusoku_3dis", "min_days_5",
                 "surg_mult_ih", "surg_mult_op", "share_free", "surg_after_limit"):
        assert cells[name].parameters == (), name
    a = medical.Projection[1]
    assert a.limit_per_hosp() == 60 and a.limit_agg() == 1095.0
    # d_pay_capped moves only because the length-of-stay band moves with age.
    assert a.d_pay_capped(0) == a.d_pay_capped(12 * 24)      # both in the 35-64 band
    assert a.d_pay_capped(12 * 25) != a.d_pay_capped(0)      # age 65, new band


def test_pitfall_age_basis_mismatch_is_stated_not_absorbed(tmp_path, medical):
    """満年齢 on the contract against 保険年齢方式 in the table: half a year, made visible.

    The contract ages on 満年齢 [S4] [S10] while 第三分野標準生命表2018 is constructed
    for a nearest-birthday basis [R5] [REG-R20].  ``age_basis_offset = 0`` accepts the
    offset [std]; 0.5 reads the table at ``age(t) + 0.5`` by interpolation.  Both
    positions are shipped so the mismatch cannot be silently absorbed.
    """
    a = medical.Projection[1]
    assert a.age_basis_offset == 0.0
    assert a.mort_rate_base(0) == pytest.approx(a.mort_rate_at_age(40), rel=1e-14)
    base_total = a.result_cf()["net_cf"].sum()

    model = _sandbox(tmp_path, "Medical_JP_S_agebasis")
    try:
        model.Projection.age_basis_offset = 0.5
        model.Projection.clear_all()
        p = model.Projection[1]
        half = 0.5 * (p.mort_rate_at_age(40) + p.mort_rate_at_age(41))
        assert p.mort_rate_base(0) == pytest.approx(half, rel=1e-14)
        assert p.mort_rate_base(0) > a.mort_rate_base(0)
        assert p.result_cf()["net_cf"].sum() - base_total == pytest.approx(
            2704.33, abs=YEN)
    finally:
        model.close()


def test_pitfall_the_180_day_rule_groups_spells_it_is_not_a_waiting_period(medical):
    """One hospitalization is one spell, and the day limit is a property of the spell.

    Two admissions inside 180 days of the previous discharge are **one** hospitalization
    against ``L1``, with a new spell starting on the 181st day [S1] [S2].  So the unit of
    account is the spell: the per-hospitalization limit is applied once inside the stay
    expectation, and the claim expense, the surgery benefit and the 入院一時金 all key
    off the spell frequency rather than off days.  An implementation that reset ``L1`` on
    every admission would remove the limit for repeat claimants.
    """
    a, p3 = medical.Projection[1], medical.Projection[3]
    assert a.claim_expenses(0) == pytest.approx(
        3000.0 * a.inc_rate_mth(0) * a.pols_if(0), rel=1e-14)
    assert a.claims(0, "SURGERY") == pytest.approx(
        a.pols_if(0) * a.inc_rate_mth(0) * a.daily_amount()
        * (a.surg_ih_eff(0) * a.surg_mult_ih() + 0.15 * a.surg_mult_op()), rel=1e-14)
    assert p3.lump_claims_pp(0) == pytest.approx(p3.inc_rate_mth(0), rel=1e-14)
    # The spell expectation is capped once, and never exceeds the limit.
    assert a.d_pay_capped(0) <= a.limit_per_hosp()
    assert "181" in medical.Projection.cells["lump_claims_pp"].doc


def test_pitfall_monthly_rounding_does_not_re_add(jp_medical_anchor):
    """Displayed monthly rows do not sum to the displayed annual total.

    The notes say so explicitly and say to assert against the unrounded aggregation.
    Year 1's net_cf is -41,860.4723; the rounded line totals re-add to -41,860.46, a yen
    away.  A test written against the rounded rows would be asserting a display artefact.
    """
    df = jp_medical_anchor.result_cf().iloc[:12]
    unrounded = df["net_cf"].sum()
    assert unrounded == pytest.approx(-41860.4723, abs=5e-5)
    from_rounded_lines = (
        round(df["premiums"].sum(), 2)
        - round(df["claims_hosp"].sum(), 2)
        - round(df["claims_surgery"].sum(), 2)
        - round(df["claims_advanced"].sum(), 2)
        - round(df["expenses"].sum(), 2)
        - round(df["claim_expenses"].sum(), 2)
        - round(df["commissions"].sum(), 2))
    assert round(from_rounded_lines, 2) == -41860.46
    assert abs(from_rounded_lines - unrounded) > 0.005


# ---------------------------------------------------------------------------
# The check cells, and the roll-forward identities behind them


def test_the_seven_check_cells_are_published_with_their_residuals(medical):
    """These seven identities are published, and no others, each with its residual.

    ``check_*`` takes no argument and returns a bool over every projected month, with the
    signed per-month residual at ``check_*_resid(t)``, so a failure is located by calling
    the residual.

    That they *close*, on all nine model points, is asserted in
    ``test_model_conventions_jp.py``: its sweep discovers every ``check_*`` generically and
    calls it on every model point of every model in the library. Running them again here,
    on a second instance of the same model, meant a second cold projection of the whole
    table to reach a verdict already reached.

    Generic discovery cannot notice a check that has *gone*: it simply stops being
    discovered. Naming the set is the statement left here.
    """
    cells = set(medical.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == set(CHECKS)
    for check in CHECKS:
        assert check + "_resid" in cells, check


def test_inforce_rollforward_closes_month_by_month(medical):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + terminations + expiries.

    The last two terms are what makes this product's roll-forward different from a term
    assurance's: cover can cease because the 通算 limits are exhausted, and the 定期 flag
    expires at its final renewal.  Without them the roll-forward would appear to lose
    lives with no cause in the final month.
    """
    for point_id in medical.Data.model_point_table().index:
        proj = medical.Projection[point_id]
        for t in range(0, proj.proj_len(), 17):
            out = (proj.pols_death(t) + proj.pols_lapse(t)
                   + proj.pols_term(t) + proj.pols_maturity(t))
            assert proj.pols_if(t) - proj.pols_if(t + 1) == pytest.approx(
                out, abs=1e-12), (point_id, t)
            assert proj.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_mortality_is_decremented_before_lapse(jp_medical_anchor):
    """The notes' processing order [std]: lapses are taken from the survivors of death."""
    a = jp_medical_anchor
    for t in (0, 11, 120, 600):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate_mth(t)), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate_mth(t), rel=1e-14)
        assert a.pols_death(t) == pytest.approx(
            a.pols_if(t) * a.mort_rate_mth(t), rel=1e-14)


def test_inforce_is_a_decreasing_probability(medical):
    """One policy at a time on an expected basis: pols_if is a probability in [0, 1]."""
    for point_id in medical.Data.model_point_table().index:
        proj = medical.Projection[point_id]
        assert proj.pols_if(0) == 1.0
        for t in range(0, proj.proj_len(), 23):
            assert 0.0 <= proj.pols_if(t) <= 1.0
            assert proj.pols_if(t + 1) <= proj.pols_if(t) + 1e-15
        assert proj.pols_if(proj.proj_len()) == 0.0
        assert proj.pols_if_at(proj.proj_len() - 1, "AFT_DECR") == 0.0


def test_the_monthly_rates_sit_below_their_annual_parents(jp_medical_anchor):
    """mort_rate / mort_rate_mth and lapse_rate / lapse_rate_mth, the library convention.

    Incidence is the exception and deliberately so: ``inc_rate_mth = inc_rate / 12``
    rather than a compounded twelfth, because an incidence is a count per unit time and
    not a probability of survival.
    """
    a = jp_medical_anchor
    for t in (0, 13, 25):
        assert a.mort_rate_mth(t) < a.mort_rate(t)
        assert a.lapse_rate_mth(t) < a.lapse_rate(t)
        assert a.mort_rate_mth(t) == pytest.approx(
            1 - (1 - a.mort_rate(t)) ** (1 / 12), rel=1e-14)
        assert a.inc_rate_mth(t) == pytest.approx(a.inc_rate(t) / 12.0, rel=1e-14)


# ---------------------------------------------------------------------------
# Optional modules, in both positions


def test_anti_selective_lapse_is_off_and_works_when_switched_on(tmp_path,
                                                                jp_medical_anchor):
    """inc_eff = inc (1 + lam max(0, w_cum - w_ref)), with lam = 0 in the base run.

    Healthy lives lapse first, so the persisting block is progressively impaired on the
    **morbidity** basis rather than the mortality one — the reverse of the term assurance
    case, where the loading falls on mortality.  Switched on at the notes' [std] 0.30 the
    anchor cell's lifetime net_cf falls from +48,981.58 to +16,965.77 — two thirds of the
    lifetime margin — which is why leaving it at zero has to be stated.
    """
    a = jp_medical_anchor
    assert a.sel_lapse_lambda == 0.0
    assert all(a.sel_lapse_factor(t) == 1.0 for t in range(0, a.proj_len(), 29))
    assert all(a.inc_rate(t) == a.inc_rate_base(t) for t in range(0, a.proj_len(), 29))
    assert a.lapse_cum(0) == 0.0
    assert a.lapse_cum(60) > 0.20                    # already past w_ref
    assert a.result_cf()["net_cf"].sum() == pytest.approx(48981.58, abs=YEN)

    model = _sandbox(tmp_path, "Medical_JP_S_sel")
    try:
        model.Projection.sel_lapse_lambda = 0.30
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.sel_lapse_factor(0) == 1.0           # nothing has lapsed yet
        assert p.sel_lapse_factor(600) > 1.0
        assert p.sel_lapse_factor(600) == pytest.approx(
            1 + 0.30 * (p.lapse_cum(600) - 0.20), rel=1e-14)
        assert p.inc_rate(600) > p.inc_rate_base(600)
        assert p.result_cf()["net_cf"].sum() == pytest.approx(16965.77, abs=YEN)
    finally:
        model.close()


def test_premium_waiver_is_off_and_works_when_elected(medical):
    """保険料払込免除 is an absorbing state, live only where the 特則 is elected.

    The 特則 waives premiums for life on a first がん diagnosis, 急性心筋梗塞 or 脳卒中
    [S1], so there is no recovery limb: u(t+1) = u(t) + (1 - u(t)) inc(t).  Off on the
    anchor cell, elected on model point 7 at the notes' placeholder 0.25 x mort_rate,
    where 6.89% of the policies in force at ten years are on waiver and 94.5% by the
    horizon.
    """
    a, p7 = medical.Projection[1], medical.Projection[7]
    assert a.waiver_3dis() is False
    assert all(a.waived(t) == 0.0 for t in range(0, a.proj_len(), 31))
    assert all(a.pols_payer(t) == a.pols_if(t) for t in range(0, a.proj_len(), 31))
    assert all(a.premiums(t) == pytest.approx(2100.0 * a.pols_if(t), rel=1e-14)
               for t in range(0, a.proj_len(), 31))

    assert p7.waiver_3dis() is True
    assert p7.waived(0) == 0.0
    assert p7.waived(120) == pytest.approx(0.068908, abs=5e-7)
    assert p7.waived(p7.proj_len() - 1) == pytest.approx(0.945173, abs=5e-5)
    for t in (0, 60, 200, 500):
        u = p7.waived(t)
        assert p7.waived(t + 1) == pytest.approx(
            u + (1 - u) * p7.waiver_inc_mth(t), rel=1e-14)
        assert p7.waived(t + 1) >= u                 # absorbing: never recovers
        assert 0.0 <= p7.waived(t) <= 1.0
    assert p7.pols_payer(120) < p7.pols_if(120)
    assert p7.check_waiver_roll_fwd() is True


def test_three_disease_unlimited_tokusoku_off_and_elected(medical):
    """The 三大疾病無制限 特則 removes L1 for the three diseases and exempts their days.

    It does not merely raise the limits: がん, 心疾患 and 脳血管疾患 days sit outside the
    通算 count entirely [S1] [S2], which raises the benefit and defers the
    benefit-driven termination at once.  Off on the anchor cell, elected on model point
    4, where benefit days per hospitalization rise 15.20 -> 16.70 while ledger-consuming
    days fall 15.20 -> 10.64.
    """
    a, p4 = medical.Projection[1], medical.Projection[4]
    assert a.tokusoku_3dis() is False
    assert a.share_free() == 0.0
    assert a.d_ben(0) == pytest.approx(a.d_pay(0), rel=1e-14)
    assert a.d_ben_free(0) == 0.0

    assert p4.tokusoku_3dis() is True
    assert p4.share_free() == pytest.approx(0.30, rel=1e-12)
    assert p4.d_pay_capped(0) == pytest.approx(15.20, abs=5e-9)
    assert p4.d_ben_raw(0) == pytest.approx(20.20, abs=5e-9)   # no L1 on the exempt share
    assert p4.d_pay(0) == pytest.approx(0.70 * 15.20, abs=5e-9)
    assert p4.d_pay(0) == pytest.approx(10.64, abs=5e-9)
    assert p4.d_ben(0) == pytest.approx(0.30 * 20.20 + 0.70 * 15.20, abs=5e-9)
    assert p4.d_ben(0) == pytest.approx(16.70, abs=5e-9)
    assert p4.d_ben(0) > p4.d_pay(0)
    # The exempt days are outside the ledger, so it advances on d_pay alone.
    assert p4.agg_days_dis(1) == pytest.approx(
        p4.inc_rate_mth(0) * 0.92 * p4.d_pay(0), rel=1e-12)


def test_lump_sum_rider_off_and_attached(medical):
    """入院一時金特約: JPY 100,000 per hospitalization against a 通算50回 count ledger.

    The market's answer to falling stay lengths — as the mean stay falls a per-day
    benefit shrinks and a per-admission benefit does not.  Off on the anchor cell,
    attached on model points 3 and 7.  Point 3 pays 231,914.26 over the lifetime and its
    count ledger reaches 24.91, well inside the 通算50回 limit.
    """
    a, p3 = medical.Projection[1], medical.Projection[3]
    assert a.lump_rider() is False
    assert all(a.lump_claims_pp(t) == 0.0 for t in range(0, a.proj_len(), 29))
    assert (a.result_cf()["claims_lump"] == 0.0).all()
    assert all(a.lump_count(t) == 0.0 for t in range(0, a.proj_len(), 29))

    assert p3.lump_rider() is True
    assert p3.lump_amount == 100000.0 and p3.lump_max_count == 50.0
    assert p3.result_cf()["claims_lump"].sum() == pytest.approx(231914.26, abs=YEN)
    assert p3.lump_count(p3.proj_len()) == pytest.approx(24.91, abs=0.005)
    assert p3.lump_count(p3.proj_len()) < p3.lump_max_count
    assert p3.claims(0, "LUMP") == pytest.approx(
        100000.0 * p3.inc_rate_mth(0) * p3.pols_if(0), rel=1e-14)
    assert p3.check_lump_ledger() is True


def test_the_advanced_medicine_ledger_counts_the_reimbursement_only(jp_medical_anchor):
    """The JPY 20,000,000 lifetime cap counts 技術料, not the cash top-up.

    ``V(t+1) = V(t) + f_adv pay(t)`` while the claim is ``f_adv [pay + min(10% pay,
    500,000)]``.  A model that also charged the top-up to the cap would exhaust the rider
    10% early.  The cap is the one genuinely market-wide parameter in this product
    [S1] [S3] [S5] [S6] [S7] [S9]; on the expectation it is never approached, which is a
    fact about the deterministic grid and not a reason to drop it.
    """
    a = jp_medical_anchor
    assert a.adv_cap == 20000000.0
    assert a.adv_pay_pp(0) == 150000.0
    assert a.adv_claim_pp(0) == pytest.approx(
        a.adv_freq_mth() * (150000.0 + 15000.0), rel=1e-14)
    assert a.adv_paid(1) - a.adv_paid(0) == pytest.approx(
        a.adv_freq_mth() * 150000.0, rel=1e-14)
    assert a.adv_paid(1) == pytest.approx(5.00, abs=YEN)
    assert a.adv_paid(a.proj_len()) < a.adv_cap
    assert a.check_adv_ledger() is True


def test_the_advanced_medicine_rider_can_be_absent(medical):
    """Model point 6 carries no 先進医療特約: the claim limb and the ledger are zero."""
    p6 = medical.Projection[6]
    assert p6.adv_rider() is False
    assert p6.adv_freq_mth() == 0.0
    assert (p6.result_cf()["claims_advanced"] == 0.0).all()
    assert p6.adv_paid(p6.proj_len()) == 0.0
    assert p6.check_adv_ledger() is True


# ---------------------------------------------------------------------------
# The structural product facts


def test_the_horizon_is_the_mortality_table_not_a_contract_term(medical):
    """Whole-of-life cover ends where the table does, and nothing happens at the end.

    ``proj_len = 12 x (omega_age - x + 1)``, with the terminal age read off
    ``mort_table.csv`` — 116 male, 118 female [REG-R18] [REG-R20] — so replacing the
    table replaces the horizon with it.  There is no 満期保険金 and no maturity benefit:
    on the 終身 chassis the only thing that happens at the horizon is nothing.
    """
    a, p8, p9 = (medical.Projection[1], medical.Projection[8], medical.Projection[9])
    assert a.omega_age() == 116 and a.proj_len() == 12 * (116 - 40 + 1) == 924
    assert p8.omega_age() == 118 and p8.proj_len() == 12 * (118 - 80 + 1) == 468
    assert p9.proj_len() == 12 * (116 - 20 + 1) == 1164
    assert len(a.result_cf()) == a.proj_len()
    # Nothing is paid at the horizon beyond the ordinary monthly benefit limbs.
    last = a.proj_len() - 1
    assert a.claims(last, "LAPSE") == 0.0
    assert a.pols_maturity(last) == 0.0        # everybody has already died
    # ``pols_maturity`` counts cover ending at the scheduled end of the contract; a
    # payment for it would be ``claims(t, "MATURITY")``, and this product has none.
    assert "claims_maturity" not in set(medical.Projection.cells)
    assert "claims_maturity" not in set(a.result_cf().columns)


def test_the_teiki_flag_expires_at_its_final_renewal(medical):
    """定期 cover runs to the last ten-year renewal completing by age 80 [std].

    Issue age 35 therefore expires at 75, and ``pols_maturity`` — the count whose cover
    ends at the scheduled end of the contract — carries the survivors out at the horizon
    so the roll-forward closes.  Nothing is paid for it: there is no ``claims_maturity``
    limb.  On the 終身 chassis ``expiry_age()`` is meaningless and raises rather than
    returning a number nobody should use.
    """
    p6 = medical.Projection[6]
    assert p6.chassis() == "teiki"
    assert p6.expiry_age() == 75
    assert p6.proj_len() == 12 * (75 - 35) == 480
    assert p6.age(p6.proj_len() - 1) == 74
    last = p6.proj_len() - 1
    assert all(p6.pols_maturity(t) == 0.0 for t in range(0, last, 19))
    assert p6.pols_maturity(last) > 0.0
    assert p6.claims(last) == pytest.approx(
        p6.claims(last, "HOSP") + p6.claims(last, "SURGERY"), rel=1e-12)
    assert p6.check_pols_roll_fwd() is True
    with pytest.raises(FormulaError):
        medical.Projection[1].expiry_age()


def test_the_short_pay_point_is_the_only_one_with_a_surrender_value(medical):
    """65歳払済 is the single route by which this chassis ever acquires a 解約返戻金.

    Zero at every duration under 終身払; after a completed 短期払 it is 10 x 入院給付金日額
    [S1] [S6].  Model point 4 issues at 45, so the premium stops at t = 240 and the value
    appears from the same month — and that is also where ``claims(t, "LAPSE")`` becomes
    non-zero for the only time anywhere in the library's medical model.
    """
    p4 = medical.Projection[4]
    assert p4.prem_period_type() == "to_65"
    assert p4.prem_end_month() == 12 * (65 - 45) == 240
    assert p4.premiums(239) > 0.0 and p4.premiums(240) == 0.0
    assert p4.cv_pp(239) == 0.0
    assert p4.cv_pp(240) == 10.0 * p4.daily_amount() == 50000.0
    assert p4.claims(239, "LAPSE") == 0.0
    assert p4.claims(240, "LAPSE") == pytest.approx(
        p4.pols_lapse(240) * 50000.0, rel=1e-14)
    assert p4.result_cf()["claims_lapse"].sum() > 0.0


def test_the_sex_factors_cross_the_incidence_ordering_between_30_and_40(medical):
    """Female incidence above male below 35 and below it from 35 on, per the [std] factors.

    Both published premium scales show the crossover [S3] [S8], and it is a morbidity
    feature rather than a pricing artefact, so it belongs on the incidence basis and not
    on the loadings.  Whether it reproduces the *premium* crossover depends on the
    mortality and expense loads too and is not claimed here.
    """
    table = medical.Data.incidence_table()
    assert table.loc[30, "inc_factor_f"] == 1.45
    assert table.loc[40, "inc_factor_f"] == 0.80
    assert (table["inc_factor_m"] == 1.00).all()
    f30, f40 = medical.Projection[2], medical.Projection[5]
    m40 = medical.Projection[1]
    assert f30.sex() == "F" and f30.issue_age() == 30
    assert f40.sex() == "F" and f40.issue_age() == 40

    def male_rate(band):
        row = table.loc[band]
        return row["juryoritsu_per_100k"] / 100000.0 * 365.0 / row["alos_days"]

    assert f30.inc_rate(0) == pytest.approx(1.45 * male_rate(30), rel=1e-12)
    assert f30.inc_rate(0) > male_rate(30)                    # female heavier below 35
    assert f40.inc_rate(0) == pytest.approx(0.80 * male_rate(40), rel=1e-12)
    assert f40.inc_rate(0) < male_rate(40)                    # and lighter from 35
    assert m40.inc_rate(0) == pytest.approx(male_rate(40), rel=1e-12)
    assert f40.inc_rate(0) < m40.inc_rate(0)


def test_benefit_driven_termination_is_a_decrement_a_death_product_lacks(medical):
    """Cover ceases when both 通算 limbs are exhausted [S9] — hence a third decrement.

    That is why the aggregate limit is a tracked state variable rather than a cap applied
    at the end of the projection, and why the roll-forward carries ``pols_term`` at all.

    On the shipped expectation it never fires, and the magnitudes are why: expected paid
    days run 0.709 a year at age 40 and 15.16 at 90 and over, the 疾病 limb takes 92% of
    them, and the ledger therefore stands at 541 of the 1,095 days at the horizon while
    the 災害 limb — the one that governs termination — stands at 47.
    """
    names = set(medical.Projection.cells)
    for cells in ("term_rate", "pols_term", "agg_days_dis", "agg_days_acc",
                  "room_dis", "room_acc"):
        assert cells in names
    for point_id in medical.Data.model_point_table().index:
        proj = medical.Projection[point_id]
        assert all(proj.term_rate(t) == 0.0 for t in range(0, proj.proj_len(), 37))
        assert all(proj.pols_term(t) == 0.0 for t in range(0, proj.proj_len(), 37))
    a = medical.Projection[1]
    assert a.term_rate(0) == 0.0
    assert a.room_dis(0) == a.limit_agg() and a.room_acc(0) == a.limit_agg()
    horizon = a.proj_len()
    assert a.inc_rate(0) * a.d_pay(0) == pytest.approx(0.709, abs=0.0005)
    assert a.inc_rate(12 * 50) * a.d_pay(12 * 50) == pytest.approx(15.16, abs=0.005)
    assert a.agg_days_dis(horizon) == pytest.approx(541.36, abs=0.05)
    assert a.agg_days_acc(horizon) == pytest.approx(47.1, abs=0.05)
    assert a.agg_days_dis(horizon) < a.limit_agg()


def test_result_cf_shape(jp_medical_anchor):
    """The published statement, column by column, indexed by the policy month."""
    df = jp_medical_anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(924))
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_hosp", "claims_surgery", "claims_advanced",
        "claims_lump", "claims_lapse", "expenses", "claim_expenses", "commissions",
        "net_cf",
    ]
    assert df.loc[0, "net_cf"] == pytest.approx(-56412.95, abs=YEN)


def test_result_cf_rows_sum_to_net_cf(medical):
    """The cash flow columns are a decomposition of net_cf, not a selection from it."""
    for point_id in medical.Data.model_point_table().index:
        df = medical.Projection[point_id].result_cf()
        outgo = df[["claims_hosp", "claims_surgery", "claims_advanced", "claims_lump",
                    "claims_lapse", "expenses", "claim_expenses",
                    "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9)


def test_net_cf_carries_the_notes_own_sign(medical):
    """The notes print the stream income-positive, which is the library-wide convention.

    So there is no outgo-positive ``liability_cf`` companion here, unlike the whole life
    and payout annuity models whose notes print the other sign.
    """
    assert "liability_cf" not in medical.Projection.cells
    a = medical.Projection[1]
    assert a.net_cf(0) < 0.0 and a.net_cf(1) > 0.0
    assert a.net_cf(1) == pytest.approx(
        a.premiums(1) - a.claims(1) - a.expenses(1) - a.claim_expenses(1)
        - a.commissions(1), abs=1e-9)


def test_invalid_enum_values_raise(medical):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    a = medical.Projection[1]
    with pytest.raises(FormulaError):
        a.pols_if_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        a.claims(0, "SURRENDER")


def test_inputs_live_beside_the_model():
    """The five input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
                "incidence_table.csv", "los_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_the_shipped_tables_mark_their_own_provenance():
    """Every assumption row says where it came from, and none is UTF-8-BOM encoded.

    The mortality file is the one that matters most: 第三分野標準生命表2018 is public and
    free but may not be redistributed [REG-R21], so the shipped table is a [std]
    construction anchored to the male q40 the notes quote, and marking the rows is what
    stops it being mistaken for the real table.
    """
    for name in ("mort_table.csv", "lapse_table.csv", "incidence_table.csv",
                 "los_table.csv"):
        path = MODEL_DIR.parent / name
        assert not path.read_bytes().startswith(b"\xef\xbb\xbf"), name
        table = pd.read_csv(path)
        assert table["provenance"].notna().all(), name
        assert table["provenance"].str.len().min() > 0, name

    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col=["sex", "age"])
    assert mort.loc[("M", 40), "mort_rate"] == pytest.approx(Q40_TABLE, rel=1e-12)
    assert mort.loc[("M", 116), "mort_rate"] == 1.0
    assert mort.loc[("F", 118), "mort_rate"] == 1.0
    assert mort["provenance"].str.contains(r"\[std\]").all()

    los = pd.read_csv(MODEL_DIR.parent / "los_table.csv")
    for band, mean in ((0, 7.6), (15, 10.5), (35, 20.2), (65, 35.5)):
        rows = los[los["band_start"] == band]
        assert (rows["prob"] * rows["stay_days"]).sum() == pytest.approx(mean, abs=5e-9)
        assert rows["prob"].sum() == pytest.approx(1.0, abs=1e-12)


def test_model_docstring_describes_the_current_structure(medical):
    """Specifics a reader relies on, asserted so they cannot go stale silently."""
    doc = medical.doc
    assert "mechanics demonstration" in doc
    assert "external" in doc
    assert "once per model" in doc
    assert "no death benefit" in doc
    assert "third-sector chassis" in doc


def test_space_docstrings_carry_their_reference_material(medical):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = medical.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "agg_days_dis", "agg_days_acc",
                  "d_pay", "d_ben", "term_rate", "adv_paid", "waived"):
        assert cells in proj, cells
    data = medical.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "incidence_table", "los_table"):
        assert cells in data, cells


def test_cells_names_follow_basicterm_s(medical):
    """Names shared with lifelib's basiclife/BasicTerm_S must not drift apart."""
    shared = {
        "model_point", "issue_age", "sex", "proj_len", "age", "pols_if",
        "pols_if_init", "pols_death", "pols_lapse", "mort_rate", "lapse_rate",
        "premiums", "claims", "expenses", "claim_expenses", "expense_acq",
        "expense_maint", "inflation_rate", "commissions", "net_cf", "result_cf",
    }
    names = set(medical.Projection.cells) | set(medical.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a production user
    does with a company 危険発生率: the basis drops in as a same-schema CSV with no
    formula change.
    """
    model = _sandbox(tmp_path, "Medical_JP_S_swap")
    try:
        base = model.Projection[1].claims(0, "HOSP")
        doubled = model.Data.incidence_table().copy()
        doubled["juryoritsu_per_100k"] = doubled["juryoritsu_per_100k"] * 2
        alt = "incidence_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt)
        model.Data.incidence_table_file = alt
        model.Data.clear_all()
        model.Projection.clear_all()
        assert model.Projection[1].claims(0, "HOSP") == pytest.approx(
            2 * base, rel=1e-12)
    finally:
        model.close()


def test_round_trip_reproduces_the_worked_example(tmp_path):
    """read -> write -> re-read reproduces the goldens and the Projection docstring."""
    model = mx.read_model(MODEL_DIR, name="Medical_JP_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Medical_JP_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[8], abs=YEN)
        assert "Notes symbol" in reread.Projection.doc
        assert anchor.check_agg_days() is True
    finally:
        reread.close()
