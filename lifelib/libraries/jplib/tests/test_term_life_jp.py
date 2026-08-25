"""Golden and structural tests for Term_JP_A.

The golden values are the worked example in
products/term_life/technical-notes.md ("Worked example"), which projects the anchor cell
M30 / 年満了 10年 更新型 / renewal ceiling attained age 80 / JPY 10,000,000 of cover /
JPY 974 a month.  They are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the yen's second decimal,
in-force to six decimals, and the year-10 exit split to the eight decimals the notes
print it at.

Beyond the worked example this module asserts every product fact the notes list under
"Known modeling pitfalls", because each of them is a way an implementation can look right
and be wrong.  One test per pitfall, named after it:

* 高度障害 is inside the mortality table, so it is not a second decrement;
* 更新 reprices the contract; it does not re-issue it;
* truncation at the renewal ceiling shortens the **term**, not the horizon;
* a 歳満了 contract never renews;
* a lapse pays nothing — there is no 解約返戻金 at any duration;
* and with no surrender value there is no 自動振替貸付 to carry the policy;
* the JPY 248 monthly element is premium, not an expense recovery;
* the renewal decline is not lapse — different year, different population, different size;
* a failed first renewed premium is an expiry, not a mid-term lapse;
* the リビング・ニーズ特約 cap is per insured and is *exactly reached*, never binding;
* the mortality table is read at 満年齢 and the optional shift must move q **up**;
* and the contract boundary is part of the answer, not a footnote to it.

The structural facts the product turns on are asserted alongside them: the horizon is the
renewal ceiling rather than the term, the premium is a function of the term index rather
than of the policy year, and there are no tail states of any kind.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from jp_registry import LIB, MODELS

YEN = 0.005           # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.
EXITS = 5e-9          # the year-10 exit split, displayed to 8 d.p.

MODEL_DIR = LIB / MODELS["Term_JP_A"][0]

# The notes' worked example, anchor cell (point_id = 1).
# t: (l(t), P_a, premiums, claims, claim expense, maint + acq, commission, CF(t))
WORKED_EXAMPLE = {
    1:  (1.000000, 11688,  11688.00, 5440.00, 16.32, 19000.00, 5844.00, -18612.32),
    2:  (0.909505, 11688,  10630.29, 5020.47, 15.06,  3674.40,  531.51,  +1388.85),
    3:  (0.845373, 11688,   9880.72, 4734.09, 14.20,  3449.46,  494.04,  +1188.93),
    10: (0.578436, 11688,   6760.76, 4997.69, 14.99,  2530.51,  338.04,  -1120.47),
    11: (0.466683, 21876,  10209.17, 4405.49, 13.22,  2062.04,  510.46,  +3217.97),
}

# The notes' table rates for the anchor cell's first term, attained ages 30 .. 40.  Ages
# 30-35 and 40 are read from 生保標準生命表2018（死亡保険用）and quoted [REG-R18] [R4];
# ages 36-39 are the [std] log-linear interpolation between the 35 and 40 anchors.
WORKED_EXAMPLE_QTAB = {
    30: 0.00068, 31: 0.00069, 32: 0.00070, 33: 0.00072, 34: 0.00074, 35: 0.00077,
    36: 0.00084, 37: 0.00091, 38: 0.00099, 39: 0.00108, 40: 0.00118,
}

# The sourced anchors of the canonical jplib proxy, over the attained ages this product
# ships (20 .. 80).  They are the union of the rates read from the published table across
# the library's research passes [REG-R18] — more ages than this product's own pass read
# [R4] — and the model reproduces every one of them exactly; every other row of
# mort_table.csv is log-linear in ln q between its two neighbouring anchors.
SOURCED_ANCHORS = {
    ("M", 20): 0.00059, ("M", 22): 0.00066, ("M", 25): 0.00067, ("M", 30): 0.00068,
    ("M", 31): 0.00069, ("M", 32): 0.00070, ("M", 33): 0.00072, ("M", 34): 0.00074,
    ("M", 35): 0.00077, ("M", 40): 0.00118, ("M", 45): 0.00177, ("M", 50): 0.00285,
    ("M", 55): 0.00422, ("M", 60): 0.00653, ("M", 65): 0.01015, ("M", 70): 0.01544,
    ("M", 75): 0.02637, ("M", 80): 0.05006,
    ("F", 20): 0.00025, ("F", 22): 0.00027, ("F", 25): 0.00029, ("F", 30): 0.00037,
    ("F", 35): 0.00059, ("F", 40): 0.00088, ("F", 45): 0.00122, ("F", 50): 0.00197,
    ("F", 55): 0.00270, ("F", 60): 0.00363, ("F", 65): 0.00484, ("F", 70): 0.00730,
    ("F", 75): 0.01289, ("F", 80): 0.02414,
}

# The renewal ladder: (t of the 更新, attained age at the renewed term's start, P_m, P_a,
# the premium jump the notes print to 2 d.p., l(t+1) after the decline).
RENEWAL_LADDER = [
    (10, 40,  1823,  21876, 1.87, 0.466683),
    (20, 50,  3933,  47196, 2.16, 0.234147),
    (30, 60,  8976, 107712, 2.28, 0.115211),
    (40, 70, 23881, 286572, 2.66, 0.054121),
]

# The three exits of year 10, in the notes' processing order.
YEAR_10_EXITS = (0.00049977, 0.02889681, 0.08235591)

# Undiscounted totals over the fifty years, and the current-term answer.
TOTAL_PREMIUMS = 470348.54
TOTAL_CLAIMS = 309768.95
TOTAL_NET_CF = 50400.25
CURRENT_TERM_NET_CF = -15878.74

# The renewal-decline sensitivity the notes tabulate: a factor of four across a range no
# document narrows.
DECLINE_SENSITIVITY = {0.00: 92123.94, 0.15: 50400.25, 0.30: 22587.91}


def _reread(suffix):
    """A private copy of the model, for tests that move a Reference."""
    return mx.read_model(MODEL_DIR, name="Term_JP_A_" + suffix)


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(jp_term_anchor, t):
    """Every cell of the notes' five-row table, to the precision the notes display."""
    pols, prem_a, prem, clm, clm_exp, exp, comm, net = WORKED_EXAMPLE[t]
    a = jp_term_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.prem_pp(t) == prem_a
    assert a.premiums(t) == pytest.approx(prem, abs=YEN)
    assert a.claims(t, "DEATH") == pytest.approx(clm, abs=YEN)
    assert a.claim_expenses(t) == pytest.approx(clm_exp, abs=YEN)
    assert a.expenses(t) == pytest.approx(exp, abs=YEN)
    assert a.commissions(t) == pytest.approx(comm, abs=YEN)
    assert a.net_cf(t) == pytest.approx(net, abs=YEN)


def test_worked_example_mortality_vector(jp_term_anchor):
    """The table rates over the first term, and q(t) = 0.80 x q_x^tab on top of them.

    The 0.80 is the model's largest single lever [std]; the table rates it multiplies are
    a [std] proxy anchored on rates quoted from the published table [REG-R18] [R4].
    """
    a = jp_term_anchor
    for t in range(1, 12):
        q_tab = WORKED_EXAMPLE_QTAB[a.age(t)]
        assert a.mort_rate_at_age(a.age(t)) == pytest.approx(q_tab, rel=1e-12)
        assert a.mort_rate(t) == pytest.approx(0.80 * q_tab, rel=1e-12)
    assert a.mort_rate(1) == pytest.approx(0.000544, rel=1e-12)
    assert a.mort_rate(11) == pytest.approx(0.000944, rel=1e-12)
    # The canonical table anchors ages 31-34 as well, so the first term is anchored
    # everywhere except 36-39.
    for x in (30, 31, 32, 33, 34, 35, 40):
        assert a.mort_rate_at_age(x) == SOURCED_ANCHORS[("M", x)]


def test_worked_example_year_one_trace(jp_term_anchor):
    """The notes' year-one trace, line by line.

    l(1) = 1; D(1) = 0.000544; claims = 10,000,000 x D(1); claim expense = 30,000 x D(1);
    expenses = E0 + e(1) = 15,000 + 4,000; commission = c0 = 0.50 x 11,688.  The strain
    the protection shape starts from is 20,844 of outgo against 11,688 of premium.
    """
    a = jp_term_anchor
    assert a.pols_if(1) == 1.0
    assert a.pols_death(1) == pytest.approx(0.000544, rel=1e-12)
    assert a.premiums(1) == 11688.00
    assert a.claims(1, "DEATH") == pytest.approx(10000000.0 * 0.000544, rel=1e-12)
    assert a.claim_expenses(1) == pytest.approx(30000.0 * 0.000544, rel=1e-12)
    assert a.expenses(1) == pytest.approx(15000.0 + 4000.0, abs=YEN)
    assert a.comm_init_pp() == pytest.approx(0.50 * 11688.0, abs=YEN)
    assert a.net_cf(1) == pytest.approx(
        11688.00 - 5440.00 - 16.32 - 19000.00 - 5844.00, abs=1e-9)


def test_worked_example_inforce_updates(jp_term_anchor):
    """The notes' roll-forward steps, including the boundary year's three of them.

    l(2) = 1 x (1 - 0.000544) x (1 - 0.09); l(3) = l(2) x (1 - 0.000552) x (1 - 0.07);
    and in year 10, mortality then ordinary lapse then the renewal decline, in that order
    and no other: 0.57793622, then 0.54903941, then 0.46668350.
    """
    a = jp_term_anchor
    assert a.lapse_rate(1) == 0.09
    assert a.pols_if(2) == pytest.approx(1.0 * (1 - 0.000544) * (1 - 0.09), rel=1e-14)
    assert a.lapse_rate(2) == 0.07
    assert a.pols_if(3) == pytest.approx(
        a.pols_if(2) * (1 - 0.000552) * (1 - 0.07), rel=1e-14)

    assert a.lapse_rate(10) == 0.05 and a.decline_rate(10) == 0.15
    assert a.pols_if_at(10, "BEF_LAPSE") == pytest.approx(0.57793622, abs=EXITS)
    assert a.pols_if_at(10, "BEF_DECLINE") == pytest.approx(0.54903941, abs=EXITS)
    assert a.pols_if_at(10, "AFT_DECR") == pytest.approx(0.46668350, abs=EXITS)
    assert a.pols_if(11) == pytest.approx(0.466683, abs=INFORCE)


def test_worked_example_year_eleven_premium_rises_though_the_cohort_shrinks(
        jp_term_anchor):
    """Year 11 collects more premium than year 10 on 19% fewer policies.

    The repricing takes effect at the start of year 11 and not before, so year 10 is
    still on the old premium; the new one has multiplied by 1.87.  That crossing is the
    signature of a 更新型 contract and no UK or U.S. term model in this repository has it.
    """
    a = jp_term_anchor
    assert a.prem_pp(10) == 11688.0 and a.prem_pp(11) == 21876.0
    assert a.pols_if(11) < 0.81 * a.pols_if(10)
    assert a.premiums(11) > a.premiums(10)
    assert a.premiums(11) == pytest.approx(10209.17, abs=YEN)


def test_worked_example_totals(jp_term_anchor):
    """Undiscounted fifty-year totals: premiums, claims and net cash flow."""
    df = jp_term_anchor.result_cf()
    assert df["premiums"].sum() == pytest.approx(TOTAL_PREMIUMS, abs=YEN)
    assert (df["claims_death"].sum() + df["claims_living_needs"].sum()
            == pytest.approx(TOTAL_CLAIMS, abs=YEN))
    assert df["net_cf"].sum() == pytest.approx(TOTAL_NET_CF, abs=YEN)


def test_the_renewal_ladder(jp_term_anchor):
    """The notes' five-numbers-per-renewal table, including the [std] ages 60 and 70.

    Ages 30, 40 and 50 are published rate card cells [S2]; 60 and 70 are published by no
    carrier and come from the [std] extension off the age-50 anchor.  The ladder is the
    product: a renewable term at attained-age rates converges on term-cost pricing, which
    is why carriers stop renewing at 80.
    """
    a = jp_term_anchor
    assert a.premium_mth_pp(1) == 974 and a.prem_pp(1) == 11688
    for t, entry_age, p_m, p_a, jump, pols_next in RENEWAL_LADDER:
        assert a.term_start_age(a.term_index(t + 1)) == entry_age
        assert a.premium_mth_pp(t + 1) == p_m
        assert a.prem_pp(t + 1) == p_a
        assert round(a.prem_pp(t + 1) / a.prem_pp(t), 2) == jump
        assert a.pols_if(t + 1) == pytest.approx(pols_next, abs=INFORCE)
    assert a.pols_if(51) == pytest.approx(0.026042, abs=INFORCE)


def test_the_shape_is_strain_then_thin_margins_then_a_pre_renewal_dip(jp_term_anchor):
    """The protection shape, asserted rather than described.

    A deep first-year strain, thin positive margins through the middle of each term, a
    negative year immediately before each renewal as the level premium falls behind the
    rising mortality cost, and a jump back into surplus the year after.
    """
    a = jp_term_anchor
    assert a.net_cf(1) < -18000.0
    assert all(a.net_cf(t) > 0.0 for t in (2, 3, 4))
    for t, *_ in RENEWAL_LADDER:
        assert a.net_cf(t) < 0.0, f"year {t} is a pre-renewal year and should be negative"
        assert a.net_cf(t + 1) > 0.0, f"year {t + 1} is the first repriced year"


# ---------------------------------------------------------------------------
# Pitfall: 高度障害 is not a second decrement


def test_pitfall_kodo_shogai_is_not_a_second_decrement(term_life):
    """One decrement carrying one benefit: there is no disability incidence at all.

    生保標準生命表2018（死亡保険用）includes 高度障害 inside its death rate [REG-R20] and
    the contract pays one sum assured and terminates on whichever event comes first
    [S1] [S8], so a separate incidence on top double-counts claims.

    Names alone are not coverage, because a second decrement can be added under any name
    and given its own benefit kind and its own column without disturbing any ledger.  The
    arithmetic guard is the product fact itself: **total** benefit outgo in a year can
    never exceed one sum assured on that year's decrement, on any model point, in any
    year, whichever kinds exist.
    """
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("disability_rate", "disab_rate", "kodo_rate", "kodo_shogai_rate",
                   "ci_rate", "ti_rate", "morbidity_rate"):
        assert absent not in names, f"{absent} would double-count the benefit"
    assert not [n for n in names if "disab" in n or "morbid" in n]
    doc = term_life.Projection.doc
    assert "One decrement, one benefit" in doc

    a = term_life.Projection[1]
    for t in (1, 11, 41):
        assert a.claims(t, "DEATH") == pytest.approx(
            a.sum_assured() * a.pols_death(t), rel=1e-14)

    # One sum assured per decrement, everywhere.  A second incidence layered on top would
    # break this at the first year it fires, whatever it is called.
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        cap = p.sum_assured()
        df = p.result_cf()
        for t in range(1, p.proj_len() + 1):
            paid = p.claims(t)
            assert paid <= cap * p.pols_death(t) + 1e-9, (
                f"point {point_id}, t={t}: benefit outgo exceeds one sum assured "
                f"on the year's decrement")
            # and the statement's benefit columns are that same total, not a subset
            assert (df.loc[t, "claims_death"] + df.loc[t, "claims_living_needs"]
                    + df.loc[t, "claims_lapse"]) == pytest.approx(paid, abs=1e-9)


# ---------------------------------------------------------------------------
# Pitfall: 更新 reprices; it does not re-issue


def test_pitfall_koshin_reprices_it_does_not_reissue(jp_term_anchor):
    """No reset of l(t), no acquisition expense and no commission at a renewal.

    A 更新 is not new business — no new 保険証券 is issued and no 告知 is taken
    [S1] [S4] — so treating each renewed term as a fresh policy would get persistency,
    the strain pattern and both contract clocks wrong at once.
    """
    a = jp_term_anchor
    for t, *_ in RENEWAL_LADDER:
        assert a.pols_if(t + 1) == pytest.approx(
            a.pols_if_at(t, "AFT_DECR"), rel=1e-15)     # continuous across the boundary
        assert a.pols_if(t + 1) < 0.5                    # never a reset to 1
        # Maintenance only: no E0 in a renewal year, and inflation runs from issue.
        assert a.expenses(t + 1) == pytest.approx(
            4000.0 * 1.01 ** t * a.pols_if(t + 1), rel=1e-12)
        # Renewal commission only: no acquisition commission on a renewed term.
        assert a.commissions(t + 1) == pytest.approx(
            0.05 * a.premiums(t + 1), rel=1e-12)
        assert a.comm_new_term(t + 1) == 0.0
    assert a.expenses(1) - 4000.0 == pytest.approx(15000.0, abs=YEN)


def test_the_premium_is_level_within_a_term_and_moves_only_at_a_koshin(term_life):
    """check_prem_level: P_a is a function of the term index, not of the policy year.

    A residual here means the rate lookup is keyed on attained age rather than on the
    term's own entry age, which makes the premium drift year by year instead of stepping.
    """
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        assert p.check_prem_level() is True
        for t in range(1, p.proj_len() + 1):
            assert p.check_prem_level_resid(t) == pytest.approx(0.0, abs=1e-12)

    a = term_life.Projection[1]
    for t in range(2, 11):
        assert a.prem_pp(t) == a.prem_pp(1)
    assert a.prem_pp(11) != a.prem_pp(10)


# ---------------------------------------------------------------------------
# Pitfall: truncation at the ceiling shortens the term, not the horizon


def test_pitfall_truncation_shortens_the_term_not_the_horizon(term_life):
    """Model point 4: issue age 35, four full terms then a five-year final term to 80.

    A renewal that would carry the policy past attained age 80 renews as an 80歳満了 term
    instead [S1] [S2] [S8].  The horizon still ends exactly at the ceiling; it is the
    term that shortens, and the shortened term is priced over its own length.

    The shipped table stops at attained age 80 because nothing reaches past it, so the
    ten-year window at 75 the truncation avoids does not exist to be read; the shortening
    is asserted on the monotonicity of qbar in the window instead.
    """
    p = term_life.Projection[4]
    assert p.age_at_entry() == 35 and p.renew_ceiling() == 80
    assert p.proj_len() == 45 == 80 - 35
    assert p.age(p.proj_len()) + 1 == 80
    assert [p.term_len(k) for k in range(1, 6)] == [10, 10, 10, 10, 5]
    assert p.term_start_age(5) == 75
    assert p.term_index(41) == 5 and p.term_index(45) == 5
    # The final term is priced over its own five years, not over ten: term_len feeds the
    # rate lookup, so the shortened term carries a cheaper mean than a ten-year one would.
    assert p.mort_table_mean(70, 5) < p.mort_table_mean(70, 10)
    anchor = term_life.Data.prem_anchor_table().loc["M"]
    assert p.prem_rate_m(41) == pytest.approx(
        float(anchor["rate_per_5m"]) * p.mort_table_mean(75, 5)
        / p.mort_table_mean(50, 10), rel=1e-12)
    assert p.decline_rate(40) == 0.15                    # the last renewal
    assert p.decline_rate(45) == 0.0                     # the cover ends; it does not renew


# ---------------------------------------------------------------------------
# Pitfall: 歳満了 never renews


def test_pitfall_sai_manryo_never_renews(term_life):
    """A 歳満了 point has one term, one premium and no repricing [S1].

    Applying the renewal machinery to it invents cover the contract does not have, so the
    term index stays at 1, the decline rate is zero throughout and the horizon is the term.
    """
    for point_id in (3, 6, 9):
        p = term_life.Projection[point_id]
        assert p.term_type() == "sai"
        assert p.proj_len() == p.policy_term() == p.horizon_ceiling()
        assert all(p.term_index(t) == 1 for t in range(1, p.proj_len() + 1))
        assert all(p.decline_rate(t) == 0.0 for t in range(1, p.proj_len() + 1))
        assert all(p.pols_decline(t) == 0.0 for t in range(1, p.proj_len() + 1))
        assert all(p.prem_pp(t) == p.prem_pp(1) for t in range(1, p.proj_len() + 1))

    p3 = term_life.Projection[3]
    assert p3.age_at_entry() == 40 and p3.policy_term() == 25   # expiry age 65
    assert p3.age(p3.proj_len()) + 1 == 65


# ---------------------------------------------------------------------------
# Pitfall: lapse pays nothing


def test_pitfall_lapse_pays_nothing(term_life):
    """claims_lapse is identically zero on every model point, and is published anyway.

    There is no 解約返戻金 and no paid-up value at any duration on this composite
    [S1] [S4] [S6] [S8] [S9] [S10] [S13] [S14], so an ordinary lapse moves pols_if and
    pays nothing.  One of the eight carriers whose position is documented *does* write this
    design with a surrender value [S12], so the zero is asserted from the composite's
    sources rather than assumed from the product class — which is why the column is shipped rather than dropped.
    """
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        df = p.result_cf()
        assert "claims_lapse" in df.columns
        assert (df["claims_lapse"] == 0.0).all()
        assert all(p.claims(t, "LAPSE") == 0.0 for t in range(1, p.proj_len() + 1))
        assert any(p.pols_lapse(t) > 0.0 for t in range(1, p.proj_len() + 1))


def test_pitfall_there_is_no_automatic_premium_loan_on_this_chassis(term_life):
    """The 自動振替貸付 absence is sourced [S7]; the 契約者貸付 absence is an inference.

    No 解約返戻金 means no collateral for either loan, and one carrier states the APL
    absence in terms [S7] — but that same carrier points its policyholders at the
    契約貸付制度 instead, so the policy loan is ruled out structurally rather than by a
    citation.  Importing the APL mechanic that the savings chassis carries would create a
    no-lapse cushion this contract does not have.  Grace, then 失効, then 復活-or-not is the
    whole persistency machinery here, and the absence of a cash value is a product fact
    rather than a gap.
    """
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("cv_pp", "av_pp", "av_pp_at", "apl", "apl_rate", "policy_loan",
                   "loan_bal", "prem_to_av_pp", "cv_rate"):
        assert absent not in names, f"{absent} belongs to a chassis with a cash value"
    assert not [n for n in names if "loan" in n or n.startswith("cv_")]


# ---------------------------------------------------------------------------
# Pitfall: the JPY 248 policy fee is premium, not expense


def test_pitfall_the_policy_fee_is_premium_not_expense(jp_term_anchor):
    """P_a reconstructs as 12 x (248 + 2 x 363) and the fee is never credited to expense.

    The flat monthly element sits inside the published premium [S2]; crediting it against
    maintenance expense counts it twice.  Year 1's expense is exactly E0 + e(1), with no
    fee offset in it.
    """
    a = jp_term_anchor
    assert a.policy_fee_m() == 248.0
    assert a.prem_rate_m(1) == 363.0
    assert a.premium_mth_pp(1) == 248 + 2 * 363 == 974
    assert a.prem_pp(1) == 12 * (248 + 2 * 363) == 11688
    assert a.expenses(1) == pytest.approx(19000.0, abs=1e-9)
    assert a.expenses(2) == pytest.approx(4000.0 * 1.01 * a.pols_if(2), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall: renewal decline is not lapse


def test_pitfall_renewal_decline_is_not_lapse(jp_term_anchor):
    """A different event, in a different year, from a different population.

    It applies only in boundary years, only after mortality and after ordinary lapse, and
    it dominates them: 0.08235591 of the 0.11175249 lives leaving in year 10, 74% of that
    year's exits.  Folding it into w(t) makes the boundary invisible.
    """
    a = jp_term_anchor
    deaths, lapses, declines = YEAR_10_EXITS
    assert a.pols_death(10) == pytest.approx(deaths, abs=EXITS)
    assert a.pols_lapse(10) == pytest.approx(lapses, abs=EXITS)
    assert a.pols_decline(10) == pytest.approx(declines, abs=EXITS)
    total = deaths + lapses + declines
    assert a.pols_if(10) - a.pols_if(11) == pytest.approx(total, abs=EXITS)
    assert declines / total > 0.73

    # Non-boundary years carry no decline at all, and the lapse rate does not absorb it.
    assert all(a.decline_rate(t) == 0.0
               for t in range(1, a.proj_len() + 1) if t % 10 or t == a.proj_len())
    assert a.lapse_rate(10) == a.lapse_rate(9) == 0.05
    # Taken after lapse, from the survivors of it.
    assert a.pols_decline(10) == pytest.approx(
        a.pols_if_at(10, "BEF_DECLINE") * 0.15, rel=1e-14)
    assert a.pols_lapse(10) == pytest.approx(
        a.pols_if_at(10, "BEF_LAPSE") * a.lapse_rate(10), rel=1e-14)


def test_pitfall_a_failed_first_renewal_premium_is_an_expiry_not_a_lapse(jp_term_anchor):
    """The decliners leave at the boundary and never collect the renewed premium.

    Where the first premium of the renewed contract goes unpaid through grace, the renewal
    is treated as never having happened and the contract terminates at the *original*
    expiry [S1] [S7].  Those lives must not appear in force in year t + 1, and must not be
    counted as a mid-term lapse of a term that never began.
    """
    a = jp_term_anchor
    assert a.pols_if(11) == pytest.approx(
        a.pols_if_at(10, "BEF_DECLINE") * (1 - 0.15), rel=1e-14)
    assert a.premiums(11) == pytest.approx(
        a.prem_pp(11) * a.pols_if(11), rel=1e-14)
    # The year-11 lapse is taken from the year-11 in-force at the year-11 rate; the
    # decliners are already gone and are not re-counted there.
    assert a.pols_lapse(11) == pytest.approx(
        a.pols_if_at(11, "BEF_LAPSE") * a.lapse_rate(11), rel=1e-14)
    assert a.pols_lapse(11) < a.pols_decline(10)
    # And no decline is taken in the final projected year: the cover ends at the ceiling
    # rather than renewing, so there is no renewal to decline.
    assert a.decline_rate(a.proj_len()) == 0.0
    assert a.pols_decline(a.proj_len()) == 0.0


# ---------------------------------------------------------------------------
# Pitfall: the living-needs cap is per insured and never binds here


def test_pitfall_the_living_needs_cap_is_per_insured_and_never_binds(term_life):
    """ln_cap_binds() is a strict inequality and is False at SA = 30,000,000.

    The JPY 30,000,000 cap is per **insured**, aggregated across all of that insurer's
    contracts [S1] [S7] [S8] [S12] — not per contract — so inside the composite's
    envelope it is *exactly reached* at the ceiling and never reduces a single-contract
    payment.  A model reporting the cap biting at the ceiling has a strict-versus-weak
    inequality error; one applying it per contract has misread the clause.
    """
    p9 = term_life.Projection[9]
    assert p9.sum_assured() == 30000000.0 == p9.ln_cap
    assert p9.ln_cap_binds() is False
    assert p9.ln_amount() == 30000000.0
    for point_id in term_life.Data.model_point_table().index:
        assert term_life.Projection[point_id].ln_cap_binds() is False


def test_a_partial_acceleration_is_rejected_by_name_not_approximated():
    """Above the cap the rider leaves a reduced contract in force at a reduced premium.

    That is a second transition, not one benefit with two amounts [S1] [S7], and it
    cannot arise inside the composite's envelope — so ln_amount() raises rather than
    approximating a mechanic the notes do not specify.
    """
    model = _reread("cap")
    try:
        model.Projection.ln_cap = 2000000.0        # below model point 6's 3,000,000
        model.Projection.clear_all()
        p = model.Projection[6]
        assert p.ln_cap_binds() is True
        with pytest.raises(FormulaError):
            p.ln_amount()
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: read the table at the right age


def test_pitfall_the_table_is_read_at_man_nenrei_and_the_shift_moves_q_up(
        jp_term_anchor):
    """契約年齢 is 満年齢 [S1]; 標準生命表2018 is built for 保険年齢 [REG-R20].

    Reading it at 満年齢 reads it half a year early and **understates** mortality.  The
    base run accepts and states that bias; the optional shift must therefore raise q — by
    about 0.7% at age 30 and 4.2% at age 40 — and a shift module that lowered it would
    have the sign wrong.
    """
    a = jp_term_anchor
    assert a.age_at_entry() == 30 and a.age(1) == 30 and a.age(11) == 40
    assert a.mort_age_shift is False
    for t in (1, 6, 11):
        assert a.mort_rate_base(t) == a.mort_rate_at_age(a.age(t))

    model = _reread("shift")
    try:
        base = {t: model.Projection[1].mort_rate_base(t) for t in range(1, 51)}
        model.Projection.mort_age_shift = True
        model.Projection.clear_all()
        p = model.Projection[1]
        for t in range(1, 50):
            assert p.mort_rate_base(t) > base[t], f"the shift lowered q at t={t}"
        assert p.mort_rate_base(1) / base[1] == pytest.approx(1.0073, abs=5e-4)
        assert p.mort_rate_base(11) / base[11] == pytest.approx(1.0415, abs=5e-4)
        assert p.mort_rate_base(1) == pytest.approx(
            (0.00068 * 0.00069) ** 0.5, rel=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: naming the boundary is part of reporting the number


def test_pitfall_naming_the_contract_boundary_is_part_of_the_answer(term_life):
    """The same cell gives +50,400.25 to the ceiling and -15,878.74 over the current term.

    A Japanese 年満了 contract guarantees its premium only within the current 保険期間, so
    where the boundary falls is a question and not a detail.  The ESR treatment that would
    settle it is [unverified] here [REG-R16], so the model carries both and rules on
    neither; the two do not even share a sign.
    """
    p1, p5 = term_life.Projection[1], term_life.Projection[5]
    assert p1.contract_boundary() == "ceiling" and p1.proj_len() == 50
    assert p5.contract_boundary() == "current_term" and p5.proj_len() == 10
    assert p5.policy_term() == 10 and p5.horizon_ceiling() == 50
    assert p1.result_cf()["net_cf"].sum() == pytest.approx(TOTAL_NET_CF, abs=YEN)
    assert p5.result_cf()["net_cf"].sum() == pytest.approx(
        CURRENT_TERM_NET_CF, abs=YEN)
    assert p1.result_cf()["net_cf"].sum() * p5.result_cf()["net_cf"].sum() < 0.0
    # Truncation changes only where the projection stops: the first ten years agree.
    for t in range(1, 11):
        assert p5.net_cf(t) == pytest.approx(p1.net_cf(t), rel=1e-12)


# ---------------------------------------------------------------------------
# Structural product facts


def test_the_horizon_is_the_renewal_ceiling_not_the_term(jp_term_anchor):
    """proj_len() = w_r - x on a 更新型 point: fifty years across five priced terms.

    This is the structural difference from the UK and U.S. term models in this repository
    rather than a parameter difference — a UK term assurance simply expires at the end of
    its term.
    """
    a = jp_term_anchor
    assert a.term_type() == "nen"
    assert a.policy_term() == 10
    assert a.renew_ceiling() == 80
    assert a.horizon_ceiling() == 50 == a.proj_len()
    assert a.age(a.proj_len()) + 1 == 80
    assert len(a.result_cf()) == 50
    assert {a.term_index(t) for t in range(1, 51)} == {1, 2, 3, 4, 5}


def test_there_are_no_tail_states_of_any_kind(term_life):
    """Cover ends at the ceiling with survivors still in force, and nothing is paid.

    No 満期保険金, no 解約返戻金, no paid-up value and no run-off [S1] [S8] [S10] [S14].
    l(51) is 2.5% of the cohort whose cover simply ends; it is not a maturity population
    and there is no benefit kind that fires on it.
    """
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("claims_maturity", "pols_maturity", "maturity_benefit", "surr_charge"):
        assert absent not in names, f"{absent} is a tail state this product does not have"

    a = term_life.Projection[1]
    n = a.proj_len()
    assert a.pols_if(n) > 0.0
    assert a.pols_if(n + 1) == pytest.approx(0.026042, abs=INFORCE)
    assert a.pols_if(n + 2) == 0.0
    assert a.pols_if_at(n + 1, "BEF_DECR") == 0.0
    assert a.claims(n) == pytest.approx(a.claims(n, "DEATH"), rel=1e-12)
    with pytest.raises(FormulaError):
        a.claims(1, "MATURITY")
    with pytest.raises(FormulaError):
        a.pols_if_at(1, "BEF_NOTHING")


def test_the_premium_scale_uses_published_cells_where_they_exist(term_life):
    """Male 30/40/50 and female 30 are rate card cells [S2]; 60 and 70 are the extension.

    The extension is unavoidable rather than optional — no carrier publishes above age 50
    and the anchor cell reaches 70 — and it is anchored so that the published cells are
    always used where they exist.
    """
    a = term_life.Projection[1]
    assert (a.prem_rate_m(1), a.prem_rate_m(11), a.prem_rate_m(21)) == (
        363.0, 787.5, 1842.5)
    anchor = term_life.Data.prem_anchor_table()
    assert int(anchor.loc["M", "issue_age"]) == 50
    assert int(anchor.loc["F", "issue_age"]) == 30
    # The extension: r = r_anchor x qbar(x, m) / qbar(x_a, m_a), on table rates.
    for t in (31, 41):
        x_k = a.term_start_age(a.term_index(t))
        assert a.prem_rate_m(t) == pytest.approx(
            1842.5 * a.mort_table_mean(x_k, 10) / a.mort_table_mean(50, 10), rel=1e-12)
    assert a.premium_mth_pp(31) == 8976 and a.premium_mth_pp(41) == 23881
    # Back-cast quality, stated in the notes so the size of the approximation is visible:
    # applied where a published cell already exists, the extension gives 958.9 a month at
    # age 30 against the published 974 (-1.5%) and 1,806.4 at age 40 against 1,823 (-0.9%).
    def extended_p_m(x):
        return 248.0 + 2.0 * 1842.5 * a.mort_table_mean(x, 10) / a.mort_table_mean(50, 10)

    assert extended_p_m(30) == pytest.approx(958.9, abs=0.05)
    assert extended_p_m(40) == pytest.approx(1806.4, abs=0.05)
    assert extended_p_m(30) / 974.0 - 1 == pytest.approx(-0.0155, abs=5e-4)
    assert extended_p_m(40) / 1823.0 - 1 == pytest.approx(-0.0091, abs=5e-4)


def test_the_premium_scale_is_built_on_table_rates_not_best_estimate_ones(term_life):
    """qbar averages the unadjusted table rate; the 0.80 never reaches a rate card.

    A premium scale is not a best-estimate quantity, so feeding the best-estimate factor
    into the extension would move a published scale by an assumption that has nothing to
    do with pricing.
    """
    a = term_life.Projection[1]
    assert a.mort_table_mean(30, 10) == pytest.approx(
        sum(WORKED_EXAMPLE_QTAB[x] for x in range(30, 40)) / 10.0, rel=1e-12)
    assert a.mort_rate(1) == pytest.approx(0.80 * a.mort_rate_at_age(30), rel=1e-14)
    assert a.mort_table_mean(30, 1) == a.mort_rate_at_age(30)     # not 0.8 x it


def test_the_female_cell_is_priced_off_the_only_published_female_anchor(term_life):
    """Model point 2 is the anchor cell female: 509 = 248 + 261 at 5,000,000 [S2].

    Sex is a rating factor of the published scale, and the female age-30 ten-year cell is
    the only published female cell in the source set — so it is that sex's anchor.
    """
    p = term_life.Projection[2]
    assert p.sex() == "F" and p.age_at_entry() == 30
    assert p.prem_rate_m(1) == 261.0
    assert p.premium_mth_pp(1) == 248 + 2 * 261 == 770
    assert p.premium_mth_pp(1) < term_life.Projection[1].premium_mth_pp(1)


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Every row says whether it is a quoted anchor or the [std] interpolation.

    生保標準生命表2018 is freely readable [REG-R18] [R3] [R4] but its publisher prohibits
    reproduction and transmission without written consent [REG-R21], so the library ships
    the canonical proxy anchored on the rates read from it.  Marking the rows is what
    stops the proxy being mistaken for the table.
    """
    import pandas as pd

    table = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert table["provenance"].notna().all()
    anchors = table[table["provenance"].str.contains(" - ANCHOR row:", regex=False)]
    assert len(anchors) == len(SOURCED_ANCHORS)
    got = {(r.sex, int(r.age)): float(r.mort_rate) for r in anchors.itertuples()}
    assert got == SOURCED_ANCHORS
    assert (table["provenance"].str.contains(r"\[std\]")).all()
    # One canonical construction, so every row names it and points at the same entries.
    assert (table["provenance"].str.contains("canonical jplib", regex=False)).all()
    assert (table["provenance"].str.contains("[REG-R18]", regex=False)).all()
    assert (table["provenance"].str.contains("[REG-R21]", regex=False)).all()
    # Restricted to the ages the model can reach: issue age 20 to the renewal ceiling.
    assert (table["age"].min(), table["age"].max()) == (20, 80)


# ---------------------------------------------------------------------------
# Roll-forward identities and the check_* cells


def test_every_check_closes_on_every_model_point(term_life):
    """The five ledgers, on all nine points, with their per-t residuals at zero.

    check_* takes no argument and returns a bool over all t, which is the library-wide
    form; the signed residual of the year that failed lives at check_*_resid(t).
    """
    checks = ["check_pols_roll_fwd", "check_lapse_pool", "check_pols_payer",
              "check_prem_level", "check_net_cf"]
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        for name in checks:
            value = getattr(p, name)()
            assert value is True, f"point {point_id}: {name}() is False"
            resid = getattr(p, name + "_resid")
            for t in range(1, p.proj_len() + 1):
                assert resid(t) == pytest.approx(0.0, abs=1e-8), \
                    f"point {point_id}: {name}_resid({t})"


def test_the_check_tolerances_are_named_references(term_life):
    """No bare literal tolerance: roll_fwd_tol for the ledgers, cash_tol for the statement.

    The two are different quantities and must not collapse into one. roll_fwd_tol closes
    identities between cells evaluated in a single expression, where the residual is a
    unit or two in the last place of a count near 1.0. cash_tol closes check_net_cf, which
    re-reads yen amounts of order 1e5 back out of the result_cf() DataFrame; the round trip
    through column construction leaves float64 rounding roll_fwd_tol would reject. So
    cash_tol must be wider -- and still far below one yen, the smallest error a reader
    adding up the printed statement could observe.
    """
    refs = term_life.Projection.refs
    assert "roll_fwd_tol" in refs and "cash_tol" in refs
    cash_tol, roll_fwd_tol = refs["cash_tol"], refs["roll_fwd_tol"]
    assert cash_tol > roll_fwd_tol
    assert cash_tol < 1.0

    # The wider tolerance is not slack the check hides behind: the residual it actually
    # sees is orders of magnitude below it on every point.
    worst = 0.0
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        worst = max(worst, max(abs(p.check_net_cf_resid(t))
                               for t in range(1, p.proj_len() + 1)))
    assert worst < cash_tol / 100.0


def test_the_four_placeholder_scalars_are_inert_in_the_base_run(term_life):
    """ln_take_up, ln_interest_rate, wop_inc_rate and reinstate_rate move no base figure.

    These four carry no evidence of any kind -- no retrieved document gives an acceleration
    take-up, a rider discount rate, a 別表4 accident-disability incidence or a reinstatement
    rate -- so the documents label them arbitrary placeholders whose only defence is that
    the module each one drives is off in the base run. That defence is the assertion here:
    perturb all four and the anchor cell must not move by one yen.
    """
    a = term_life.Projection[1]
    before = a.net_cf(1), a.net_cf(11), sum(a.net_cf(t)
                                            for t in range(1, a.proj_len() + 1))
    saved = {name: term_life.Projection.refs[name]
             for name in ("ln_take_up", "ln_interest_rate",
                          "wop_inc_rate", "reinstate_rate")}
    try:
        for name, value in saved.items():
            setattr(term_life.Projection, name, value * 3.0 + 0.5)
        a = term_life.Projection[1]
        assert a.living_needs() is False and a.wop() is False
        assert a.reinstatement() is False
        after = a.net_cf(1), a.net_cf(11), sum(a.net_cf(t)
                                               for t in range(1, a.proj_len() + 1))
        assert after == pytest.approx(before, abs=1e-9)
    finally:
        for name, value in saved.items():
            setattr(term_life.Projection, name, value)


def test_the_inforce_rollforward_is_the_notes_identity(term_life):
    """l(t) - l(t+1) = deaths + lapses + declines - reinstatements, in every year.

    The 復活 inflow is carried as its own term so that the same residual closes in both
    positions of the module switch.
    """
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        for t in range(1, p.proj_len() + 1):
            out = (p.pols_death(t) + p.pols_lapse(t) + p.pols_decline(t)
                   - p.pols_reinstate(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12)


def test_the_decrements_are_taken_in_the_notes_processing_order(term_life):
    """Death, then ordinary lapse, then the renewal decline — steps 3, 4 and 5.

    Each timing reads the population the next decrement is taken from, which is what makes
    the decline a decrement on the survivors of lapse rather than a competing one.
    """
    a = term_life.Projection[1]
    for t in (1, 5, 10, 20, 41):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) * (1 - a.mort_rate(t)), rel=1e-14)
        assert a.pols_if_at(t, "BEF_DECLINE") == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * (1 - a.lapse_rate(t)), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(
            a.pols_if_at(t, "BEF_DECLINE") * (1 - a.decline_rate(t)), rel=1e-14)
    for t in (1, 5, 41):
        assert a.pols_if_at(t, "BEF_DECLINE") == a.pols_if_at(t, "AFT_DECR")


def test_inforce_is_a_decreasing_probability(term_life):
    """One policy, projected on an expected basis, and nothing creates lives.

    With the 復活 module on the pool feeds lives back in, so this is asserted on the
    points where it is off; reinstatement's own effect is asserted with the module.
    """
    for point_id in term_life.Data.model_point_table().index:
        p = term_life.Projection[point_id]
        if p.reinstatement():
            continue
        for t in range(1, p.proj_len() + 2):
            assert 0.0 <= p.pols_if(t) <= 1.0
            assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15


def test_the_published_statement_adds_up(term_life):
    """The result_cf columns are a decomposition of net_cf, not a selection from it.

    check_net_cf is the guard against a benefit kind that exists in claims() but was never
    given a column, which would leave the statement silently short of outgo.
    """
    for point_id in term_life.Data.model_point_table().index:
        df = term_life.Projection[point_id].result_cf()
        outgo = df[["claims_death", "claims_living_needs", "claims_lapse",
                    "claim_expenses", "expenses", "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Modules that are off in the base run, in both positions


def test_living_needs_is_off_on_the_anchor_cell(jp_term_anchor):
    """No acceleration, no share of the decrement and a zero benefit column."""
    a = jp_term_anchor
    assert a.living_needs() is False
    assert a.ln_amount() == 0.0
    assert all(a.ln_share(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.claims(t, "LIVING_NEEDS") == 0.0 for t in range(1, a.proj_len() + 1))
    assert (a.result_cf()["claims_living_needs"] == 0.0).all()


def test_living_needs_splits_the_decrement_and_does_not_add_to_it(term_life):
    """The acceleration is a re-timing and re-pricing of the death benefit, not a claim.

    a(t) is a **share** of the existing death-and-高度障害 decrement, the same ruling the
    notes make for 高度障害 itself.  Because the payout is discounted, switching the rider
    on lowers total outgo; it must leave the decrement itself untouched.
    """
    p = term_life.Projection[6]
    assert p.living_needs() is True
    assert p.ln_share(1) == 0.10
    for t in range(1, p.proj_len() + 1):
        assert p.claims(t, "DEATH") == pytest.approx(
            p.sum_assured() * (1 - p.ln_share(t)) * p.pols_death(t), rel=1e-14)
        assert p.claims(t, "LIVING_NEEDS") == pytest.approx(
            p.ln_payout_pp(t) * p.ln_share(t) * p.pols_death(t), rel=1e-14)
        assert p.claims(t) <= p.sum_assured() * p.pols_death(t) + 1e-9

    model = _reread("lnoff")
    try:
        model.Projection.ln_take_up = 0.0
        model.Projection.clear_all()
        off = model.Projection[6]
        n = p.proj_len()
        assert all(off.pols_death(t) == pytest.approx(p.pols_death(t), abs=1e-15)
                   for t in range(1, n + 1))
        assert sum(p.claims(t) for t in range(1, n + 1)) < sum(
            off.claims(t) for t in range(1, n + 1))
    finally:
        model.close()


def test_living_needs_is_discounted_and_net_of_six_months_premium(term_life):
    """payout = A - A i/2 - six months' premiums on A [S1] [S7] [S8] [S12].

    The discount is the economic reason the rider can be offered without a premium, and it
    is the difference from UK terminal illness cover, which pays the face amount.  The
    trigger is a six-month prognosis, not the UK's twelve.
    """
    p = term_life.Projection[6]
    assert p.ln_interest_rate == 0.02
    assert p.ln_payout_pp(1) == pytest.approx(
        3000000.0 * 0.99 - 6 * p.premium_mth_pp(1), abs=1e-6)
    assert p.ln_payout_pp(1) < p.sum_assured()


def test_living_needs_is_barred_within_a_year_of_a_non_renewable_expiry(term_life):
    """The bar bites in the final projected year, and only there.

    On a 更新型 cell every earlier expiry is followed by a renewal, so the rider stays
    available; on a 歳満了 cell the final year is a genuine non-renewable expiry.
    """
    for point_id in (6, 9):
        p = term_life.Projection[point_id]
        n = p.proj_len()
        assert p.ln_available(n) is False and p.ln_share(n) == 0.0
        assert p.claims(n, "LIVING_NEEDS") == 0.0
        assert p.ln_available(n - 1) is True and p.ln_share(n - 1) == 0.10


def test_waiver_of_premium_is_off_and_works_when_switched_on(term_life):
    """A two-state chain on the premium-paying population; zero unless the module is on.

    The trigger is an accident producing a 別表4 state within 180 days [S1] [S8] [S12]
    [S14] — a materially lower bar than the 別表3 test for 高度障害 — so the incidence is
    its own [std] parameter and does not reuse mort_rate.
    """
    a = term_life.Projection[1]
    assert a.wop() is False
    assert all(a.wop_waived_frac(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.pols_payer(t) == a.pols_if(t) for t in range(1, a.proj_len() + 1))
    assert all(a.pols_waived(t) == 0.0 for t in range(1, a.proj_len() + 1))

    p = term_life.Projection[7]
    assert p.wop() is True
    assert p.wop_waived_frac(1) == 0.0                     # the chain starts empty
    assert p.wop_waived_frac(2) == pytest.approx(0.0008, rel=1e-12)
    assert p.wop_waived_frac(3) > p.wop_waived_frac(2)     # and accumulates
    assert p.wop_rec_rate == 0.0                           # 別表4 states are permanent
    assert p.pols_payer(5) < p.pols_if(5)
    assert p.premiums(5) == pytest.approx(p.prem_pp(5) * p.pols_payer(5), rel=1e-14)
    # Cover continues while the premium is waived: the waived lives stay in force.
    assert p.check_pols_payer() is True
    assert p.pols_death(5) == pytest.approx(p.pols_if(5) * p.mort_rate(5), rel=1e-14)
    # The incidence is not the mortality rate.
    assert p.wop_inc_rate != pytest.approx(p.mort_rate(2), rel=1e-3)


def test_reinstatement_is_off_and_works_when_switched_on(term_life):
    """The 復活 pool: one inflow, two outflows, tracked by vintage over a 3-year window.

    Off in the base run because any reinstatement rate is an invention with a material
    persistency effect [S1].  The pool is tracked either way, so the ledger closes in both
    positions of the switch.
    """
    a = term_life.Projection[1]
    assert a.reinstatement() is False
    assert a.reinstate_rate_eff() == 0.0
    assert all(a.pols_reinstate(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert a.pols_lapse_pool(4) > 0.0                      # the stock is tracked anyway
    assert a.check_lapse_pool() is True

    p = term_life.Projection[8]
    assert p.reinstatement() is True
    assert p.reinstate_rate_eff() == 0.10
    assert p.reinstate_window == 3
    assert p.pols_lapse_pool(1) == 0.0
    assert p.pols_reinstate(2) == pytest.approx(0.10 * p.pols_lapse_pool(2), rel=1e-14)
    assert p.pols_if(3) > p.pols_if_at(2, "AFT_DECR")      # lives come back in
    # By vintage, not one blanket balance: the pool at t is the last three years' lapses
    # net of the reinstatements taken out of each along the way.
    for t in range(2, p.proj_len() + 1):
        rebuilt = sum(p.pols_lapse(s) * 0.9 ** (t - 1 - s)
                      for s in range(max(1, t - 3), t))
        assert p.pols_lapse_pool(t) == pytest.approx(rebuilt, abs=1e-14)
    # And the window really closes: the vintage that lapsed three years ago leaves.
    assert p.pols_lapse_expire(4) == pytest.approx(
        p.pols_lapse(1) * 0.9 ** 3, rel=1e-12)
    assert p.pols_lapse_expire(3) == 0.0
    assert p.check_lapse_pool() is True


def test_declines_never_enter_the_reinstatement_pool(term_life):
    """A declined renewal is an expiry, not a 失効, so there is nothing to reinstate.

    Only ordinary lapses flow into the pool; folding the boundary exits in would
    reinstate lives whose contract ended rather than lapsed.
    """
    p = term_life.Projection[8]
    boundary = 10
    assert p.pols_decline(boundary) > 0.0
    assert p.pols_lapse_pool(boundary + 1) == pytest.approx(
        sum(p.pols_lapse(s) * 0.9 ** (boundary - s)
            for s in range(boundary - 2, boundary + 1)), abs=1e-14)


def test_selective_lapsation_is_off_and_works_when_switched_on(term_life):
    """q_eff = q (1 + lambda max(0, 1 - l(t)/l_ref)); lambda = 0 in the base run.

    The mechanism is stronger here than on a UK term policy and one-directional: renewal
    takes no 告知 [S1] [S4] [S8] [S12], so a life that has become uninsurable elsewhere
    renews while a healthy life re-shops — and the decision recurs at every boundary.
    """
    a = term_life.Projection[1]
    assert a.sel_lapse_lambda == 0.0
    assert all(a.sel_lapse_factor(t) == 1.0 for t in range(1, a.proj_len() + 1))

    model = _reread("sel")
    try:
        base_late = model.Projection[1].mort_rate(20)
        model.Projection.sel_lapse_lambda = 0.25
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.sel_lapse_factor(1) == 1.0                # nothing has left yet
        assert p.sel_lapse_factor(20) > 1.0                # the block has shed lives
        assert p.mort_rate(20) > base_late
        assert p.mort_rate(20) == pytest.approx(
            0.80 * p.mort_rate_base(20) * p.sel_lapse_factor(20), rel=1e-12)
        assert p.check_pols_roll_fwd() is True
    finally:
        model.close()


def test_the_renewal_decline_elasticity_is_off_and_works_when_switched_on(term_life):
    """d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta); beta = 0 gives the flat 15%.

    The premium jump the elasticity responds to accelerates — 1.87, 2.16, 2.28, 2.66 —
    so a non-zero beta makes the later boundaries shed more than the earlier ones, and the
    cap is what stops it running away.
    """
    a = term_life.Projection[1]
    assert a.decline_beta == 0.0 and a.decline_base == 0.15
    assert all(a.decline_rate(t) == 0.15 for t, *_ in RENEWAL_LADDER)

    model = _reread("beta")
    try:
        model.Projection.decline_beta = 1.0
        model.Projection.clear_all()
        p = model.Projection[1]
        rates = [p.decline_rate(t) for t, *_ in RENEWAL_LADDER]
        assert rates == sorted(rates)                      # rising with the jump
        assert rates[0] == pytest.approx(0.15 * 21876 / 11688, rel=1e-12)
        assert rates[-1] == pytest.approx(0.15 * 286572 / 107712, rel=1e-12)
        assert p.result_cf()["net_cf"].sum() < TOTAL_NET_CF
        model.Projection.decline_beta = 2.0                # above the cap everywhere
        model.Projection.clear_all()
        p = model.Projection[1]
        assert all(p.decline_rate(t) == 0.50 for t, *_ in RENEWAL_LADDER)
    finally:
        model.close()


@pytest.mark.parametrize("d", sorted(DECLINE_SENSITIVITY))
def test_the_decline_sensitivity_the_notes_tabulate(d):
    """Net cash flow at d = 0%, 15% and 30%: a factor of four across an unnarrowed range.

    The renewal decline is the largest structural lever on this product and has no uklib
    analogue, so the three points are asserted rather than described.
    """
    model = _reread("d%d" % round(d * 100))
    try:
        model.Projection.decline_base = d
        model.Projection.clear_all()
        assert model.Projection[1].result_cf()["net_cf"].sum() == pytest.approx(
            DECLINE_SENSITIVITY[d], abs=YEN)
    finally:
        model.close()


def test_commission_at_koshin_is_off_and_changes_the_sign_when_switched_on(term_life):
    """A 更新 is not new business, so the base run pays no commission on a renewed term.

    That is a choice and not a fact — no document in the source set discloses a commission
    scale at all — and a scale paying first-year rates on each renewed term changes the
    **sign** of the cash flow in years 11, 21, 31 and 41.
    """
    a = term_life.Projection[1]
    assert a.comm_new_term_rate == 0.0
    assert all(a.comm_new_term(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.net_cf(t + 1) > 0.0 for t, *_ in RENEWAL_LADDER)

    model = _reread("comm")
    try:
        model.Projection.comm_new_term_rate = 0.50
        model.Projection.clear_all()
        p = model.Projection[1]
        for t, *_ in RENEWAL_LADDER:
            assert p.comm_new_term(t + 1) == pytest.approx(
                0.50 * p.prem_pp(t + 1) * p.pols_if(t + 1), rel=1e-12)
            assert p.net_cf(t + 1) < 0.0, f"year {t + 1} should flip negative"
        assert p.comm_new_term(1) == 0.0                   # not the first term
        assert p.comm_new_term(12) == 0.0                  # only the term's first year
        assert p.check_net_cf() is True
    finally:
        model.close()


def test_the_contract_boundary_switch_only_truncates(term_life):
    """current_term stops the projection; it does not change any year that survives it."""
    p1, p5 = term_life.Projection[1], term_life.Projection[5]
    df1, df5 = p1.result_cf(), p5.result_cf()
    assert list(df5.index) == list(range(1, 11))
    assert (df5 - df1.loc[1:10]).abs().max().max() == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(jp_term_anchor):
    """The published statement's columns, in order, with pols_if first."""
    df = jp_term_anchor.result_cf()
    assert list(df.index) == list(range(1, 51))
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_living_needs", "claims_lapse",
        "claim_expenses", "expenses", "commissions", "net_cf",
    ]
    assert df.loc[1, "net_cf"] == pytest.approx(-18612.32, abs=YEN)


def test_net_cf_carries_the_notes_own_sign(term_life):
    """The notes write "+ = inflow", which is already the library-wide convention.

    So there is no outgo-positive liability_cf companion here, unlike the models whose
    notes print the other sign.
    """
    assert "liability_cf" not in term_life.Projection.cells
    assert term_life.Projection[1].net_cf(2) > 0.0         # a positive-margin year
    assert term_life.Projection[1].net_cf(1) < 0.0         # the strain year


def test_result_pols_makes_a_renewal_boundary_legible(jp_term_anchor):
    """The boundary is the row whose decline_rate is non-zero and whose premium then moves.

    The renewal machinery is only readable next to the decrements it drives, which is why
    term_index and prem_pp are printed beside them.
    """
    df = jp_term_anchor.result_pols()
    assert df.index.name == "t"
    assert list(df.columns)[0] == "pols_if"
    boundaries = [t for t in df.index if df.loc[t, "decline_rate"] > 0.0]
    assert boundaries == [10, 20, 30, 40]
    for t in boundaries:
        assert df.loc[t + 1, "prem_pp"] > df.loc[t, "prem_pp"]
        assert df.loc[t + 1, "term_index"] == df.loc[t, "term_index"] + 1


def test_model_docstring_describes_the_current_structure(term_life):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = term_life.doc
    assert "level term" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "no tail states of any kind" in doc


def test_space_docstrings_carry_their_reference_material(term_life):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = term_life.Projection.doc
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    for cells in ("pols_if", "term_index", "decline_rate", "pols_lapse_pool",
                  "prem_rate_m", "ln_share", "proj_len", "model_point"):
        assert cells in proj
    data = term_life.Data.doc
    assert "TradLife_A" in data                  # the layout it follows
    for cells in ("input_dir", "mort_table", "model_point_table", "prem_rate_table"):
        assert cells in data


def test_cells_names_follow_basicterm_s(term_life):
    """Names shared with lifelib's basiclife/BasicTerm_S must not drift apart."""
    shared = {
        "model_point", "age_at_entry", "sex", "sum_assured", "policy_term",
        "proj_len", "age", "pols_if", "pols_if_init", "pols_if_at", "pols_death",
        "pols_lapse", "mort_rate", "lapse_rate", "premiums", "claims", "expenses",
        "expense_acq", "expense_maint", "inflation_rate", "inflation_factor",
        "commissions", "net_cf", "result_cf",
    }
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_inputs_live_beside_the_model():
    """The four input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
                "prem_rate_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_the_input_csvs_are_utf8_without_a_bom():
    """A BOM survives into the first column name and breaks the index lookup silently."""
    for csv in MODEL_DIR.parent.glob("*.csv"):
        head = csv.open("rb").read(3)
        assert head != b"\xef\xbb\xbf", f"{csv.name} carries a UTF-8 BOM"
        csv.read_text(encoding="utf-8")


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a user with a
    company mortality basis does: it drops in as a same-schema CSV, no formula change.
    """
    import pandas as pd

    src = MODEL_DIR.parent / "mort_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "age"])
    doubled["mort_rate"] = doubled["mort_rate"] * 2

    model = _reread("swap")
    try:
        alt_name = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].claims(1, "DEATH")
            model.Data.mort_table_file = alt_name           # repoint the Reference
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].claims(1, "DEATH") == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_model_point_table_exercises_the_product(term_life):
    """Both sexes, both term shapes, both boundaries, all three riders, both extremes.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.
    """
    table = term_life.Data.model_point_table()
    assert len(table) == 9
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["term_type"]) == {"nen", "sai"}
    assert set(table["contract_boundary"]) == {"ceiling", "current_term"}
    for module in ("living_needs", "wop", "reinstatement"):
        assert set(table[module]) == {0, 1}, f"{module} is not exercised in both positions"
    assert table["issue_age"].min() == 20 and table["issue_age"].max() == 65
    assert table["sum_assured"].min() == 1000000 and table["sum_assured"].max() == 30000000
    assert table.index[0] == 1                             # the anchor cell leads


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = _reread("rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Term_JP_A_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[7], abs=YEN)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    src_files = {p.name for p in MODEL_DIR.rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts}
    dest_files = {p.name for p in dest.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts}
    assert dest_files == src_files
