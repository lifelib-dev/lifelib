"""Golden and product-specific tests for WholeLife_US_A.

The golden values are the worked example in products/whole_life/technical-notes.md
("Worked example"), a single-year walk-through of the core recursion: RefWL-Par, male
Standard NT, issue age 45, face 100,000, gross premium 1,800, paid-up-additions
dividend option, no rider, no loan, policy year 10 (attained age 55 at the anniversary).
They are hard-coded here rather than pickled so that a reviewer can compare them against
the notes by eye.

Model point 1 carries that walk-through as an *in-force* point - duration_inforce = 9,
puaf_inforce = 4,100 - because the example stipulates a prior paid-up-additions balance,
which is a projected state variable and cannot otherwise be pinned without fitting the
shipped tables to the answer.

Tolerances follow the precision the notes display: money to the cent, probabilities to
their displayed decimals.
"""
import itertools

import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/whole_life/WholeLife_US_A"

CENT = 0.005          # money displayed to 2 d.p.
PROB = 5e-6           # probabilities displayed to 5 d.p.
INFORCE = 5e-7

_counter = itertools.count()

I_GUAR = 0.04
D_GUAR = I_GUAR / (1 + I_GUAR)


def _annuity_due(mort, sex, y, n, i=I_GUAR):
    """ae_{y:n|} on a shipped mortality table at interest i."""
    v, total, kpx = 1 / (1 + i), 0.0, 1.0
    for k in range(n):
        total += v ** k * kpx
        kpx *= 1 - float(mort.loc[(sex, y + k), "mort_rate"])
    return total


def _endow_nsp(mort, sex, y, i=I_GUAR):
    """A_{y:(100-y)|} on a shipped mortality table at interest i: the notes' NSP_y."""
    v, a = 1 / (1 + i), 1.0
    for age in range(99, y - 1, -1):
        q = float(mort.loc[(sex, age), "mort_rate"])
        a = v * (q + (1 - q) * a)
    return a

# ---------------------------------------------------------------------------
# The notes' worked example: step -> (label, value as the notes print it)

WORKED_EXAMPLE = {
    1:  ("CV_9      guaranteed CV, BOY (table)",           9500.00),
    2:  ("CV_10     guaranteed CV, EOY (table)",          11200.00),
    3:  ("NP_g      net level premium, NF basis",          1300.00),
    4:  ("q^g_54    guarantee mortality, age 54",             0.00320),
    5:  ("q^sc_54   scale mortality = 0.70 * q^g_54",         0.00224),
    6:  ("D^int     (0.06-0.04) * (9,500 + 1,300)",         216.00),
    7:  ("D^mort    (0.00320-0.00224) * (100,000-11,200)",   85.25),
    8:  ("D^exp     expense margin e^m_10",                   25.00),
    9:  ("D_10      216.00 + 85.25 + 25.00",                326.25),
    10: ("NSP_55    net single premium, age 55 (table)",       0.42),
    11: ("dPUAF     326.25 / 0.42",                         776.79),
    12: ("PUAF_10   4,100.00 + 776.79",                    4876.79),
    13: ("PUACV_10  4,876.79 * 0.42",                      2048.25),
    14: ("DB_11     F + PUAF_10",                        104876.79),
    15: ("CSV_10    CV_10 + PUACV_10",                    13248.25),
}


def _worked_example_values(a):
    """The model's answer to each numbered step of the notes' table."""
    return {
        1: a.cv_pp(9),
        2: a.cv_pp(10),
        3: a.np_guar(),
        4: a.mort_rate_guar(10),
        5: a.mort_rate_scale(10),
        6: a.div_int(10),
        7: a.div_mort(10),
        8: a.div_exp(10),
        9: a.div_base(10),
        10: a.nsp(55),
        11: a.pua_face_purch(10),
        12: a.pua_face(10),
        13: a.pua_cv(10),
        14: a.claim_pp(11, "DEATH"),
        15: a.claim_pp(10, "LAPSE"),
    }


# ---------------------------------------------------------------------------
# Fixtures

@pytest.fixture(scope="module")
def whole_life():
    """The WholeLife_US_A model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(whole_life):
    """Model point 1 - the worked-example anchor cell, in force at duration 9."""
    return whole_life.Projection[1]


@pytest.fixture(scope="module")
def newbiz(whole_life):
    """Model point 2 - the same policy issued as new business, the full 55 years."""
    return whole_life.Projection[2]


@pytest.fixture
def fresh():
    """Factory for a throwaway model instance whose References may be changed."""
    opened = []

    def _make(**refs):
        model = mx.read_model(MODEL_PATH, name="WholeLife_US_A_%d" % next(_counter))
        for name, value in refs.items():
            setattr(model.Projection, name, value)
        opened.append(model)
        return model

    yield _make
    for model in opened:
        model.close()


# ---------------------------------------------------------------------------
# The worked example

@pytest.mark.parametrize("step", sorted(WORKED_EXAMPLE))
def test_worked_example_step(anchor, step):
    """Every numbered step of the notes' 15-row table, to the displayed precision."""
    label, want = WORKED_EXAMPLE[step]
    got = _worked_example_values(anchor)[step]
    tol = PROB if want < 1.0 else CENT
    assert got == pytest.approx(want, abs=tol), "step %d: %s" % (step, label)


def test_the_anchor_is_the_in_force_point_the_notes_describe(anchor):
    """The worked example's stipulated opening state is model point 1's input."""
    assert anchor.age_at_entry() == 45
    assert anchor.sex() == "M"
    assert anchor.risk_class() == "STD_NT"
    assert anchor.sum_assured() == 100000.0
    assert anchor.premium_pp(10) == 1800.0
    assert anchor.dividend_option() == "PUA"
    assert anchor.duration_inforce() == 9
    assert anchor.pua_face(9) == 4100.0          # the notes' "prior 4,100.00"
    assert anchor.loan_bal(9) == 0.0
    assert anchor.proj_start() == 10             # policy year 10 is the first projected
    assert anchor.proj_len() == 55               # maturity at attained age 100


def test_pua_block_dividend_matches_the_notes_parenthetical(fresh):
    """The notes' aside: D^PUA_10 = 0.02*PUACV_9 + 0.00096*(PUAF_9 - PUACV_9).

    0.02 is i_d - i_g and 0.00096 is q^g_54 - q^sc_54, both taken straight from the
    steps above, so this pins the PUA-block formula against the notes' own arithmetic.
    """
    a = fresh(pua_div_on=True).Projection[1]
    expected = 0.02 * a.pua_cv(9) + 0.00096 * (a.pua_face(9) - a.pua_cv(9))
    assert a.div_pua(10) == pytest.approx(expected, rel=1e-12)
    assert a.div_pua(10) == pytest.approx(35.331623, abs=1e-6)
    assert a.div_credited(10) == pytest.approx(326.25 + 35.331623, abs=1e-5)


def test_pua_block_dividend_is_off_in_the_shipped_base_run(anchor, newbiz, fresh):
    """pua_div_on ships False so the worked example reproduces; it is a switch, not a claim.

    The notes' table computes steps 11-15 from the base-block dividend alone and says
    so.  Turning the PUA-block dividend on is the product-faithful setting and moves the
    numbers materially, which is exactly why the switch is explicit rather than implied.
    """
    assert anchor.pua_div_on is False
    assert anchor.div_pua(10) == 0.0
    assert anchor.div_credited(10) == pytest.approx(326.25, abs=CENT)

    on = fresh(pua_div_on=True)
    assert on.Projection[1].pua_face(10) > anchor.pua_face(10)
    # paid-up additions compound on their own dividends: the notes' first sensitivity
    assert on.Projection[2].pua_face(55) > 1.5 * newbiz.pua_face(55)


def test_the_dividend_is_rounded_to_the_cent_and_it_matters(anchor, fresh):
    """Documented divergence: the notes carry the *displayed* dividend into step 11.

    216.00 + 85.25 + 25.00 = 326.25 is the notes' own arithmetic, but the exact
    mortality margin is 85.248, so the unrounded dividend is 326.248.  326.25/0.42
    displays as 776.79 and 326.248/0.42 displays as 776.78 - the exact value sits just
    below the rounding boundary.  Dividends are declared in whole cents, so the shipped
    model rounds; the test pins both readings so neither can be lost.
    """
    assert anchor.div_round_digits == 2
    assert anchor.div_mort(10) == pytest.approx(85.248, abs=1e-9)
    assert anchor.div_base(10) == 326.25                      # exactly, after rounding
    assert anchor.pua_face_purch(10) == pytest.approx(326.25 / 0.42, rel=1e-12)
    assert round(anchor.pua_face_purch(10), 2) == 776.79      # the notes' printed value

    unrounded = fresh(div_round_digits=None).Projection[1]
    assert unrounded.div_base(10) == pytest.approx(326.248, abs=1e-9)
    assert round(unrounded.pua_face_purch(10), 2) == 776.78   # one displayed cent apart
    assert unrounded.pua_face_purch(10) != pytest.approx(
        anchor.pua_face_purch(10), abs=1e-4)


# ---------------------------------------------------------------------------
# Roll-forwards

def test_inforce_rollforward_closes(newbiz, anchor):
    """pols_if(t) - pols_if(t+1) = deaths + surrenders + maturities, every year.

    `pols_if(t)` is the *start*-of-year count, so the year's decrements carry it to the
    start of the next year.  `pols_maturity` is non-zero only in the final policy year,
    where the survivors neither die nor surrender: the modelled contract ends at
    attained age 100.  Without it in the identity the last year appears to lose lives
    with no cause.
    """
    for proj in (newbiz, anchor):
        assert proj.check_pols_roll_fwd() is True
        for t in range(proj.proj_start(), proj.proj_len() + 1):
            out = proj.pols_death(t) + proj.pols_lapse(t) + proj.pols_maturity(t)
            assert proj.pols_if(t) - proj.pols_if(t + 1) == pytest.approx(out, abs=1e-12)
            assert proj.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_pols_if_is_the_start_of_year_count_the_row_is_weighted_by(newbiz, anchor):
    """pols_if(t) is l_{t-1}, and it reconciles with the cash flows on its own row.

    The library-wide convention: `pols_if(t)` is the number in force at the *start* of
    period t and is the weight applied to that same `result_cf()` row.  The notes'
    end-of-year `l_t` is `pols_if_at(t, "AFT_DECR")`, one year on.
    """
    for proj in (newbiz, anchor):
        T = proj.proj_len()
        assert proj.pols_if(proj.proj_start()) == proj.pols_if_init()
        for t in range(proj.proj_start(), T + 1):
            assert proj.pols_if(t) == proj.pols_if_at(t, "BEF_DECR")
            assert proj.pols_if_at(t, "AFT_DECR") == pytest.approx(
                proj.pols_if(t + 1), abs=1e-15)
            # the printed in-force column reconciles with the row it sits on
            if proj.premium_net_pp(t):
                assert proj.premiums(t) / proj.premium_net_pp(t) == pytest.approx(
                    proj.pols_if(t), rel=1e-12)
            assert proj.pols_death(t) == pytest.approx(
                proj.pols_if(t) * proj.mort_rate(t), rel=1e-12)
        assert proj.pols_if_at(T, "AFT_DECR") == 0.0      # everything left matures at T
        assert proj.pols_if(T + 1) == 0.0

    df = newbiz.result_cf()
    assert df.loc[1, "pols_if"] == newbiz.pols_if_init()
    assert df.loc[1, "premiums"] == pytest.approx(
        newbiz.premium_net_pp(1) * df.loc[1, "pols_if"], rel=1e-12)


def test_pua_rollforward_closes(whole_life, fresh):
    """PUAF_t - PUAF_{t-1} = dividend purchases + rider purchases + offset purchases."""
    for point_id in (1, 2, 5, 7, 8, 14):
        proj = whole_life.Projection[point_id]
        assert proj.check_pua_roll_fwd() is True
        for t in range(proj.proj_start(), proj.proj_len() + 1):
            assert proj.check_pua_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)
    on = fresh(pua_div_on=True)
    assert on.Projection[2].check_pua_roll_fwd() is True


def test_the_roll_forward_checks_are_no_arg_booleans(newbiz):
    """The library-wide shape: no argument, a bool over every t, plus a *_resid(t).

    So one test can call the same check across every model, and a debugging session can
    still ask which year moved and by how much.
    """
    for check in (newbiz.check_pols_roll_fwd, newbiz.check_pua_roll_fwd):
        assert check() is True
        assert isinstance(check(), bool)
    for resid in (newbiz.check_pols_roll_fwd_resid, newbiz.check_pua_roll_fwd_resid):
        assert isinstance(resid(10), float)


def test_maturity_is_confined_to_the_final_year(newbiz):
    for t in range(newbiz.proj_start(), newbiz.proj_len()):
        assert newbiz.pols_maturity(t) == 0.0
        assert newbiz.claim_pp(t, "MATURITY") == 0.0
    T = newbiz.proj_len()
    assert newbiz.pols_maturity(T) > 0.0
    assert newbiz.pols_maturity(T) == newbiz.pols_if_at(T, "BEF_MAT")
    assert newbiz.pols_if_at(T, "AFT_DECR") == 0.0      # the notes' l_T after maturity


def test_inforce_is_a_decreasing_probability(newbiz):
    for t in range(newbiz.proj_start(), newbiz.proj_len() + 1):
        assert 0.0 <= newbiz.pols_if(t) <= 1.0
        assert newbiz.pols_if(t + 1) <= newbiz.pols_if(t) + 1e-15


# ---------------------------------------------------------------------------
# The notes' "Known modeling pitfalls", one test each

def test_pitfall_cv_table_and_nsp_endow_together(newbiz, whole_life):
    """Pitfall 1, the half that is satisfied: neither block leaks at maturity.

    NSP is exactly 1 at attained age 100 and the cash value schedule is exactly face in
    the final policy year, so PUACV reaches PUAF and CV reaches F.  The other half of
    the pitfall - one basis for all four tables - is *not* satisfied; see
    test_the_guarantee_basis_is_not_one_construction.
    """
    T = newbiz.proj_len()
    assert newbiz.age_anniv(T) == 100
    assert newbiz.nsp(100) == 1.0
    assert newbiz.cv_pp(T) == pytest.approx(newbiz.sum_assured(), abs=CENT)
    assert newbiz.pua_cv(T) == pytest.approx(newbiz.pua_face(T), rel=1e-12)
    assert newbiz.claim_pp(T, "MATURITY") == pytest.approx(
        newbiz.claim_pp(T, "LAPSE"), abs=CENT)
    tbl = whole_life.Data.nsp_table()
    assert (tbl.xs(100, level="age")["nsp"] == 1.0).all()
    cv = whole_life.Data.cv_table()["cv_per_1000"]
    cells = set(cv.index.droplevel("policy_year"))
    assert len(cells) == 12
    for pp, sx, x in cells:
        assert cv.loc[(pp, sx, x, 100 - x)] == 1000.00, (pp, sx, x)


def test_the_guarantee_basis_is_not_one_construction(anchor, whole_life):
    """Pitfall 1, the half that is NOT satisfied - a documented divergence.

    The notes say to "regenerate all guarantee-basis quantities from one 2017 CSO / 4%
    source".  The shipped tables do not: each is pinned to its own worked-example
    anchor.  That is not laziness - the worked example's own anchors are unreachable on
    any single basis, and this test carries the proof, so the claim cannot be softened
    into "one construction" again, and the size of the gap cannot quietly move.
    """
    # (1) On one basis, A_{x:n} = 1 - d*ae_{x:n}, so the notes' NNLP = F NSP_x/ae_{x:100-x}
    #     collapses to 1000 d NSP_45 / (1 - NSP_45).  Step 3 (NP_g = 13.00) then fixes NSP_45.
    nsp45 = 13.0 / (1000 * D_GUAR + 13.0)
    assert nsp45 == pytest.approx(0.252616, abs=1e-6)
    assert 1000 * D_GUAR * nsp45 / (1 - nsp45) == pytest.approx(13.00, abs=1e-9)

    # (2) NSP_y = v(NSP_{y+1} + q_y(1 - NSP_{y+1})) >= v NSP_{y+1} for any q_y >= 0,
    #     so NSP_55 <= NSP_45 * 1.04**10 whatever the mortality table.
    assert nsp45 * 1.04 ** 10 == pytest.approx(0.373933, abs=1e-6)
    assert nsp45 * 1.04 ** 10 < 0.42                  # the worked example's step 10

    # (3) Read the other way: step 10 forces NNLP >= 15.236, 17% above the notes' 13.00.
    from_step10 = 0.42 / 1.04 ** 10
    assert from_step10 == pytest.approx(0.283737, abs=1e-6)
    assert 1000 * D_GUAR * from_step10 / (1 - from_step10) == pytest.approx(15.236, abs=5e-4)

    # (4) So the shipped NSP curve is not the endowment NSP on the shipped mortality.
    mort = whole_life.Data.mort_table()
    assert _endow_nsp(mort, "M", 55) == pytest.approx(0.330820, abs=1e-6)
    assert anchor.nsp(55) == 0.42                     # +27.0% on the recomputed value
    assert _endow_nsp(mort, "M", 45) == pytest.approx(0.236184, abs=1e-6)
    assert anchor.nsp(45) == pytest.approx(0.258170, abs=1e-6)

    # (5) The size of the mismatch: the guarantee rate that reconciles the two falls
    #     from 5.99% at 45 to 0.02% at 99, and is never the 4.00% i_g the model credits
    #     excess interest against.
    def implied_rate(y):
        q = anchor.mort_rate_guar_at(y)
        return (q + (1 - q) * anchor.nsp(y + 1)) / anchor.nsp(y) - 1.0

    for y, want in ((45, 0.059857), (54, 0.048929), (80, 0.020819), (99, 0.000186)):
        assert implied_rate(y) == pytest.approx(want, abs=1e-6)
        assert abs(implied_rate(y) - anchor.int_rate_guar) > 1e-3

    # (6) And inverting the curve for q at 4% gives impossible rates.
    def implied_q(y):
        return (1.04 * anchor.nsp(y) - anchor.nsp(y + 1)) / (1 - anchor.nsp(y + 1))

    assert implied_q(45) == pytest.approx(-0.005507, abs=1e-6)   # negative
    assert implied_q(54) == pytest.approx(-0.002991, abs=1e-6)   # negative
    assert all(implied_q(y) < 0.0 for y in range(18, 58))        # negative up to age 57
    assert all(implied_q(y) > 1.0 for y in range(89, 99))        # above 1 from age 89
    assert implied_q(90) == pytest.approx(1.350388, abs=1e-6)


def test_np_guar_is_the_notes_endowment_period_net_level_premium(whole_life):
    """NNLP = 1000 NSP_x / ae_{x:(100-x)}: the endowment period, not the premium period.

    The notes annotate only the *other* nonforfeiture quantity, P_adj, with
    "(m = premium period)", so the (100 - x) subscript on NNLP is deliberate and NP_g
    does not vary with m.  The shipped table used to carry 1000 NSP_x / ae_{x:m} on the
    limited-pay rows - 30.85 instead of 13.00 for a PAY_10 male 45, which moved every
    year's interest margin by 0.02 * (3085 - 1300) = 35.70.
    """
    mort = whole_life.Data.mort_table()
    nsp_tbl = whole_life.Data.nsp_table()["nsp"]
    npg = whole_life.Data.np_guar_table()["np_guar_per_1000"]

    for sex, x in (("M", 45), ("F", 45), ("M", 65), ("F", 65)):
        want = round(1000 * float(nsp_tbl.loc[(sex, x)])
                     / _annuity_due(mort, sex, x, 100 - x), 2)
        rows = npg.xs((sex, x), level=("sex", "issue_age"))
        assert len(rows) >= 2
        assert set(rows) == {want}, (sex, x, sorted(set(rows)), want)

    assert round(1000 * float(nsp_tbl.loc[("M", 45)])
                 / _annuity_due(mort, "M", 45, 55), 2) == 13.00      # the notes' reading
    assert round(1000 * float(nsp_tbl.loc[("M", 45)])
                 / _annuity_due(mort, "M", 45, 10), 2) == 30.85      # the m reading, not used

    # every premium period on the same cell now sees the same NP_g
    for point_id in (2, 9):                     # TO_100 and PAY_10, both M45 / 100k
        assert whole_life.Projection[point_id].np_guar() == pytest.approx(1300.0, abs=CENT)
    assert whole_life.Projection[10].np_guar() == pytest.approx(1026.0, abs=CENT)   # F45


def test_cv_schedule_is_sex_distinct(whole_life):
    """The notes require sex-distinct rates throughout, the CV schedule included.

    The pay-to-100 rows used to be byte-identical for male and female, so the female
    pay-to-100 model point silently ran on the male schedule while every other premium
    period in the same table was sex-distinct.
    """
    cv = whole_life.Data.cv_table()["cv_per_1000"]
    cells = set(cv.index.droplevel("policy_year"))
    checked = 0
    for pp in ("TO_100", "PAY_10", "PAY_20", "TO_65"):
        for x in (45, 65):
            if (pp, "M", x) not in cells or (pp, "F", x) not in cells:
                continue
            checked += 1
            T = 100 - x
            for t in range(1, T):
                m, f = cv.loc[(pp, "M", x, t)], cv.loc[(pp, "F", x, t)]
                assert f < m, (pp, x, t, m, f)          # lower mortality, lower schedule
            assert cv.loc[(pp, "M", x, T)] == cv.loc[(pp, "F", x, T)] == 1000.00
    assert checked == 6

    male, female = whole_life.Projection[2], whole_life.Projection[10]
    assert (male.sex(), female.sex()) == ("M", "F")
    assert male.cv_pp(10) == pytest.approx(11200.0, abs=CENT)    # the worked example
    assert female.cv_pp(10) == pytest.approx(9800.0, abs=CENT)   # its own schedule now
    assert female.cv_pp(female.proj_len()) == pytest.approx(female.sum_assured(), abs=CENT)


def test_pitfall_dividend_floor_is_asymmetric(fresh):
    """Pitfall 2: with D_t floored at 0, adverse experience does not claw back."""
    adverse = fresh(int_rate_div=0.01, ae_scale=1.5, expense_margin=-500.0)
    p = adverse.Projection[2]
    assert p.div_int(10) < 0.0
    assert p.div_mort(10) < 0.0
    assert p.div_base(10) == 0.0                # floored, not negative
    assert p.div_credited(10) == 0.0
    assert p.pua_face(10) == 0.0


def test_pitfall_first_dividend_year_is_a_parameter(newbiz, fresh):
    """Pitfall 3: year 1 vs year 2 shifts early-duration PUA compounding.

    A real cross-carrier difference, so the notes insist it stay a parameter.
    """
    assert newbiz.div_first_year == 2
    assert newbiz.div_base(1) == 0.0
    assert newbiz.div_base(2) > 0.0
    early = fresh(div_first_year=1).Projection[2]
    assert early.div_base(1) > 0.0
    assert early.pua_face(10) > newbiz.pua_face(10)


def test_pitfall_mec_is_flagged_not_policed(whole_life):
    """Pitfall 4: the model flags model points needing a 7702A test, it does not run one.

    Limited-pay designs sit near the 7-pay limit and PUA-rider payments consume 7-pay
    room, so both raise the flag; the pay-to-100 base design does not.
    """
    assert whole_life.Projection[2].mec_flag() is False    # TO_100, no rider
    assert whole_life.Projection[7].mec_flag() is True     # PUA rider premium
    assert whole_life.Projection[9].mec_flag() is True     # PAY_10
    assert len(whole_life.Projection[9].result_cf()) > 0   # flagged, still projected


def test_pitfall_truncation_at_age_100(newbiz):
    """Pitfall 5: truncation is exact for amounts but reallocates deaths to maturity."""
    T = newbiz.proj_len()
    assert T == 100 - newbiz.age_at_entry()
    assert newbiz.age_anniv(T) == 100
    assert newbiz.lapse_rate(T) == 0.0          # "0 within 1 year of maturity"
    assert newbiz.claims(T, "MATURITY") > 0.0
    assert newbiz.claims(T + 0, "LAPSE") == 0.0
    assert newbiz.pols_if_at(T, "AFT_DECR") == 0.0
    assert newbiz.pols_if(T + 1) == 0.0


# ---------------------------------------------------------------------------
# Processing order, sign convention, decrements

def test_deaths_are_valued_before_the_dividend_and_surrenders_after(anchor):
    """The notes' EOY order: deaths, then the dividend credit, then surrenders."""
    assert anchor.claim_pp(11, "DEATH") == pytest.approx(
        anchor.sum_assured() + anchor.pua_face(10), rel=1e-12)
    assert anchor.claim_pp(10, "LAPSE") == pytest.approx(
        anchor.cv_pp(10) + anchor.pua_cv(10), rel=1e-12)
    # the surrender value includes the year-10 dividend; the death benefit does not
    assert anchor.pua_face(10) > anchor.pua_face(9)


def test_liability_cf_is_the_notes_outgo_positive_stream(newbiz):
    """The notes print NetCF_t with outgo positive; liability_cf carries it verbatim."""
    t = 20
    assert newbiz.liability_cf(t) == pytest.approx(
        -newbiz.premiums(t) - newbiz.rider_premiums(t)
        + newbiz.expenses(t) + newbiz.premium_taxes(t)
        + newbiz.claims(t) + newbiz.div_cash_paid(t) + newbiz.loan_draws(t),
        rel=1e-12)
    # early durations are premium-dominated, so outgo-positive liability_cf is negative
    assert newbiz.liability_cf(2) < 0.0
    assert newbiz.liability_cf(newbiz.proj_len()) > 0.0    # the maturity payment


def test_net_cf_is_income_positive_and_is_minus_liability_cf(newbiz, anchor):
    """net_cf is income less outgo in every model in the library, this one included.

    The whole-life notes are the only ones that print the opposite sign, so the stream
    is published twice rather than one reading being dropped: `liability_cf` under the
    notes' sign, `net_cf` under the library's.  They are exact negatives.
    """
    for proj in (newbiz, anchor):
        for t in range(proj.proj_start(), proj.proj_len() + 1):
            assert proj.net_cf(t) == -proj.liability_cf(t)
        assert proj.net_cf(proj.proj_start() + 1) > 0.0   # premium-dominated: income
        assert proj.net_cf(proj.proj_len()) < 0.0         # the maturity payment: outgo

    df = newbiz.result_cf()
    assert (df["net_cf"] == -df["liability_cf"]).all()
    assert df.loc[2, "net_cf"] == pytest.approx(
        df.loc[2, "premiums"] + df.loc[2, "rider_premiums"]
        - df.loc[2, "expenses"] - df.loc[2, "premium_taxes"]
        - df.loc[2, "claims_death"] - df.loc[2, "claims_lapse"]
        - df.loc[2, "claims_maturity"] - df.loc[2, "div_cash_paid"]
        - df.loc[2, "loan_draws"], rel=1e-12)


def test_par_lapse_schedule(newbiz):
    """5.0% in year 1 grading linearly to 2.0% at year 10, level after, 0 at maturity."""
    assert newbiz.lapse_rate(1) == pytest.approx(0.05)
    assert newbiz.lapse_rate(2) == pytest.approx(0.05 - 0.03 / 9)
    assert newbiz.lapse_rate(10) == pytest.approx(0.02)
    assert newbiz.lapse_rate(30) == pytest.approx(0.02)
    assert newbiz.lapse_rate(newbiz.proj_len() - 1) == pytest.approx(0.02)
    assert newbiz.lapse_rate(newbiz.proj_len()) == 0.0


def test_dynamic_lapse_overlay_is_off_by_default(newbiz, fresh):
    """w^dyn = w * min(1 + 2.0 * max(0, r_cmp - i_d - 0.01), 3.0), a scenario overlay."""
    assert newbiz.dyn_lapse_on is False
    on = fresh(dyn_lapse_on=True, competitor_rate=0.10).Projection[2]
    assert on.dyn_lapse_factor(5) == pytest.approx(1.0 + 2.0 * (0.10 - 0.06 - 0.01))
    assert on.lapse_rate(5) == pytest.approx(newbiz.lapse_rate(5) * 1.06)
    # the multiplier is capped at 3.0: 1 + 2*(2.00 - 0.06 - 0.01) = 4.86 -> 3.0
    capped = fresh(dyn_lapse_on=True, competitor_rate=2.00).Projection[2]
    assert capped.dyn_lapse_factor(5) == 3.0
    assert capped.lapse_rate(5) == pytest.approx(newbiz.lapse_rate(5) * 3.0)


def test_the_same_mortality_table_feeds_both_sides(newbiz):
    """The notes' consistency trap: q^e drives claims, q^sc drives the dividend margin."""
    assert newbiz.mort_rate(10) == pytest.approx(0.7 * newbiz.mort_rate_guar(10))
    assert newbiz.mort_rate_scale(10) == pytest.approx(0.7 * newbiz.mort_rate_guar(10))
    assert newbiz.div_mort(10) == pytest.approx(
        (newbiz.mort_rate_guar(10) - newbiz.mort_rate_scale(10))
        * newbiz.net_amt_at_risk(10), rel=1e-12)


# ---------------------------------------------------------------------------
# Dividend options, riders, loans

def test_dividend_options(whole_life):
    """PUA, CASH, ACCUM and REDUCE_PREM each route the same dividend somewhere else."""
    pua, cash, accum, rpd = (whole_life.Projection[i] for i in (2, 3, 4, 5))
    d = pua.div_base(10)
    assert cash.div_base(10) == pytest.approx(d, abs=CENT)      # same dividend...
    assert accum.div_base(10) == pytest.approx(d, abs=CENT)     # ...different landing

    assert pua.pua_face(10) > 0.0 and pua.div_accum(10) == 0.0
    assert cash.pua_face(10) == 0.0 and cash.div_cash(10) == pytest.approx(d, abs=CENT)
    assert cash.div_cash_paid(10) == pytest.approx(
        d * cash.pols_if_at(10, "BEF_SURR"), rel=1e-12)
    assert accum.div_accum(10) == pytest.approx(
        accum.div_accum(9) * 1.06 + accum.div_credited(10), rel=1e-12)
    assert pua.div_cash_paid(10) == 0.0                          # not a cash flow


def test_reduce_prem_offsets_and_spills_into_puas(whole_life):
    """G^net = max(G - D_{t-1}, 0), and the excess buys paid-up additions."""
    rpd = whole_life.Projection[5]
    assert rpd.premium_net_pp(3) == pytest.approx(1800.0 - rpd.div_credited(2), abs=CENT)
    assert rpd.pua_face_offset(3) == 0.0                # dividend below the premium
    offset_years = [t for t in range(2, 56) if rpd.div_credited(t - 1) > 1800.0]
    assert offset_years, "the dividend never grows past the premium"
    t = offset_years[0]
    assert rpd.premium_net_pp(t) == 0.0
    assert rpd.pua_face_offset(t) == pytest.approx(
        (rpd.div_credited(t - 1) - 1800.0) / rpd.nsp(rpd.age(t)), rel=1e-12)


def test_every_credited_dividend_is_delivered(whole_life):
    """No option may credit a dividend and then deliver nothing - the year-T leak.

    Under REDUCE_PREM the notes route D_t to the *next* year's premium, and there is no
    year T + 1.  Read literally that drops the final dividend - 2,030.14 on model point
    5, more than a full year's gross premium: it offset no premium, bought no paid-up
    additions, was not paid in cash and never reached the maturity benefit, while the
    other three options all delivered theirs.  The model treats the whole of D_T as
    REDUCE_PREM excess and buys paid-up additions with it at NSP_100 = 1.
    """
    pua, cash, accum, rpd = (whole_life.Projection[i] for i in (2, 3, 4, 5))
    T = pua.proj_len()
    ts = list(range(1, T + 1))
    credited = sum(pua.div_credited(t) for t in ts)
    assert credited > 0.0

    # PUA: every dividend becomes paid-up-additions face at that year's NSP
    assert sum(pua.pua_face_purch(t) * pua.nsp(pua.age_anniv(t))
               for t in ts) == pytest.approx(credited, rel=1e-9)

    # CASH: every dividend is paid out
    assert sum(cash.div_cash(t) for t in ts) == pytest.approx(
        sum(cash.div_credited(t) for t in ts), rel=1e-9)

    # ACCUM: the balance is the dividends rolled up at i_d, and it reaches maturity
    assert accum.div_accum(T) == pytest.approx(
        sum(accum.div_credited(t) * (1 + accum.int_rate_div) ** (T - t) for t in ts),
        rel=1e-9)
    assert accum.claim_pp(T, "MATURITY") == pytest.approx(
        accum.sum_assured() + accum.div_accum(T), rel=1e-12)

    # REDUCE_PREM: premium offsets, plus the excess, plus the final year
    delivered = sum((rpd.premium_pp(t) - rpd.premium_net_pp(t))
                    + rpd.pua_face_offset(t) * rpd.nsp(rpd.age(t)) for t in ts)
    assert delivered == pytest.approx(
        sum(rpd.div_credited(t) for t in ts) - rpd.div_credited(T), rel=1e-9)
    delivered += rpd.pua_face_purch(T) * rpd.nsp(rpd.age_anniv(T))
    assert delivered == pytest.approx(sum(rpd.div_credited(t) for t in ts), rel=1e-9)

    # the year-T dividend specifically, which used to vanish: it now reaches maturity
    assert rpd.div_credited(T) == pytest.approx(2030.14, abs=CENT)
    assert rpd.div_credited(T) > rpd.premium_pp(T)        # more than a year's premium
    assert rpd.nsp(rpd.age_anniv(T)) == 1.0
    assert rpd.pua_face_purch(T) == pytest.approx(rpd.div_credited(T), rel=1e-12)
    assert rpd.pua_face(T) == pytest.approx(                # D_{T-1} excess, then D_T
        rpd.pua_face(T - 1) + rpd.pua_face_offset(T) + rpd.div_credited(T), rel=1e-12)
    assert rpd.claim_pp(T, "MATURITY") == pytest.approx(
        rpd.sum_assured() + rpd.pua_face(T), rel=1e-12)


def test_pua_rider_carries_a_ten_percent_load(whole_life):
    """A_t (1 - 0.10) / NSP_{x+t-1}: rider payments are loaded, dividends are not."""
    rider = whole_life.Projection[7]
    assert rider.rider_premium_pp(1) == 1000.0
    assert rider.pua_face_rider(1) == pytest.approx(
        1000.0 * 0.9 / rider.nsp(45), rel=1e-12)
    assert rider.rider_premiums(1) == pytest.approx(1000.0 * rider.pols_if(1), rel=1e-12)
    assert whole_life.Projection[2].pua_face_rider(1) == 0.0


def test_term_blend_caps_the_term_layer_and_crosses_over(whole_life):
    """The notes give no shortfall rule; the layer is capped at what the dividend buys."""
    blend = whole_life.Projection[8]
    assert blend.is_blended() is True
    for t in range(1, blend.proj_len() + 1):
        assert blend.oyt_cost(t) <= blend.div_credited(t) + 1e-9
        assert blend.div_to_pua(t) >= 0.0
        # the death benefit is base + additions + whatever term is actually funded
        assert blend.claim_pp(t, "DEATH") == pytest.approx(
            blend.sum_assured() + blend.pua_face(t - 1) + blend.oyt_face(t), rel=1e-12)
    crossover = [t for t in range(2, blend.proj_len() + 1) if blend.oyt_face(t) == 0.0]
    assert crossover, "the blend never crosses over"
    t = crossover[0]
    assert blend.pua_face(t - 1) >= blend.term_blend_target() - blend.sum_assured()
    assert whole_life.Projection[2].oyt_face(10) == 0.0          # rider off


def _cap_binding_years(p):
    """The policy years in which the one-year-term cap bites: OYT_t below the raw gap."""
    out = []
    for t in range(1, p.proj_len() + 1):
        gap = max(p.term_blend_target() - p.sum_assured() - p.pua_face(t - 1), 0.0)
        if gap > 0.0 and p.oyt_face(t) < gap - 1e-9:
            out.append(t)
    return out


def test_term_blend_cap_binds_only_where_the_dividend_falls_short(whole_life):
    """Whether the cap binds is a property of the funding, not of the design.

    Model point 8 funds the 2x target with a 5,000 rider premium: the cap binds only in
    policy year 1, where div_first_year = 2 means there is no dividend at all, and the
    gap closes at year 8.  Model point 14 is the same target with no rider premium: the
    cap binds in years 1-3 and again in every year from 30 on, and the block never
    crosses over.  Point 14 exists so the shortfall branch is exercised too.
    """
    funded, unfunded = whole_life.Projection[8], whole_life.Projection[14]

    assert float(funded.model_point()["pua_rider_premium"]) == 5000.0
    assert _cap_binding_years(funded) == [1]
    assert funded.div_credited(1) == 0.0 and funded.oyt_face(1) == 0.0
    assert funded.oyt_face(7) > 0.0 and funded.oyt_face(8) == 0.0       # crossover

    assert unfunded.is_blended() is True
    assert float(unfunded.model_point()["pua_rider_premium"]) == 0.0
    T = unfunded.proj_len()
    binding = _cap_binding_years(unfunded)
    assert binding[:3] == [1, 2, 3]
    assert set(range(30, T + 1)) <= set(binding)
    assert len(binding) == 29
    assert all(unfunded.oyt_face(t) > 0.0 for t in range(2, T + 1))     # never crosses over

    # where the cap binds, the whole dividend goes to the term layer and none to PUAs
    t = 45
    q = unfunded.ae_scale * unfunded.mort_rate_guar_at(unfunded.age_anniv(t))
    assert unfunded.oyt_face(t) == pytest.approx(
        unfunded.div_credited(t) * (1 + unfunded.int_rate_guar) / q, rel=1e-12)
    assert unfunded.oyt_cost(t) == pytest.approx(unfunded.div_credited(t), rel=1e-12)
    assert unfunded.div_to_pua(t) == pytest.approx(0.0, abs=1e-9)
    assert unfunded.claim_pp(t, "DEATH") == pytest.approx(
        unfunded.sum_assured() + unfunded.pua_face(t - 1) + unfunded.oyt_face(t), rel=1e-12)


def test_direct_recognition_is_zero_only_because_i_L_equals_i_d(whole_life, fresh):
    """The notes flag the snapshot coincidence; a scale change breaks it."""
    loaned, plain = whole_life.Projection[6], whole_life.Projection[2]
    assert loaned.loan_bal(10) == pytest.approx(0.2 * loaned.cv_pp(10), rel=1e-12)
    assert loaned.div_int(10) == pytest.approx(plain.div_int(10), rel=1e-12)

    moved = fresh(int_rate_loan=0.10)
    a, b = moved.Projection[6], moved.Projection[2]
    assert a.div_int(10) > b.div_int(10)
    assert a.div_int(10) == pytest.approx(
        0.02 * (a.cv_pp(9) + a.np_guar() - a.loan_bal(9)) + 0.06 * a.loan_bal(9),
        rel=1e-12)


def test_the_loan_reduces_every_benefit(whole_life):
    """DB, CSV and MAT are all net of the loan; the advance is a separate cash flow."""
    loaned, plain = whole_life.Projection[6], whole_life.Projection[2]
    T = loaned.proj_len()
    for kind, t in (("DEATH", 10), ("LAPSE", 10), ("MATURITY", T)):
        assert loaned.claim_pp(t, kind) < plain.claim_pp(t, kind)
    assert loaned.claim_pp(T, "MATURITY") == pytest.approx(
        plain.claim_pp(T, "MATURITY") - loaned.loan_bal(T), abs=CENT)
    assert loaned.loan_draw(1) == pytest.approx(loaned.loan_bal(1), rel=1e-12)
    assert loaned.loan_draw(10) == pytest.approx(
        loaned.loan_bal(10) - loaned.loan_bal(9) * 1.06, rel=1e-12)
    assert plain.loan_draws(10) == 0.0


# ---------------------------------------------------------------------------
# The RefWL-FE variant

def test_fe_premium_comes_from_the_sourced_rate_table(whole_life):
    """G = (F/1000) * rate(x, sex, class) + 36 on the [S7] California rates."""
    level_m, graded_m, level_f = (whole_life.Projection[i] for i in (11, 12, 13))
    assert level_m.premium_pp(1) == pytest.approx(15 * 59.05 + 36, abs=CENT)   # 921.75
    assert graded_m.premium_pp(1) == pytest.approx(15 * 103.00 + 36, abs=CENT)
    assert level_f.premium_pp(1) == pytest.approx(15 * 42.48 + 36, abs=CENT)
    assert level_m.is_par() is False
    assert level_m.div_base(5) == 0.0 and level_m.pua_face(5) == 0.0


def test_fe_graded_death_benefit(whole_life):
    """Years 1-2: 110% of premiums paid on natural death, full face on accidental."""
    g = whole_life.Projection[12]
    G, F = g.premium_pp(1), g.sum_assured()
    assert g.prem_cum(1) == pytest.approx(G) and g.prem_cum(2) == pytest.approx(2 * G)
    for t in (1, 2):
        assert g.claim_pp(t, "DEATH") == pytest.approx(
            0.97 * 1.10 * t * G + 0.03 * F, abs=CENT)
        assert g.claim_pp(t, "DEATH") < F
    assert g.claim_pp(3, "DEATH") == pytest.approx(F, abs=CENT)
    assert whole_life.Projection[11].claim_pp(1, "DEATH") == pytest.approx(F, abs=CENT)


def test_fe_lapse_schedule_and_maturity(whole_life):
    """12% year 1, 10% year 2, grading linearly to 6% by year 5; MAT = F - L_T."""
    fe = whole_life.Projection[11]
    assert fe.lapse_rate(1) == pytest.approx(0.12)
    assert fe.lapse_rate(2) == pytest.approx(0.10)
    assert fe.lapse_rate(3) == pytest.approx(0.10 - 0.04 / 3)
    assert fe.lapse_rate(4) == pytest.approx(0.10 - 0.08 / 3)
    assert fe.lapse_rate(5) == pytest.approx(0.06)
    assert fe.lapse_rate(20) == pytest.approx(0.06)
    T = fe.proj_len()
    assert T == 35
    assert fe.claim_pp(T, "MATURITY") == pytest.approx(fe.sum_assured(), abs=CENT)


# ---------------------------------------------------------------------------
# Structure

def test_result_cf_shape(anchor, newbiz):
    df = anchor.result_cf()
    assert list(df.index) == list(range(10, 56))
    assert df.index.name == "t"
    assert set(df.columns) == {
        "pols_if", "premiums", "rider_premiums", "expenses", "premium_taxes",
        "claims_death", "claims_lapse", "claims_maturity", "div_cash_paid",
        "loan_draws", "net_cf", "liability_cf",
    }
    assert df.loc[10, "premiums"] == pytest.approx(1800.0, abs=CENT)
    assert list(newbiz.result_cf().index) == list(range(1, 56))
    assert list(newbiz.result_pols().index) == list(range(1, 56))
    assert list(newbiz.result_cv().index) == list(range(1, 56))
    assert set(newbiz.result_cv().columns) == {
        "cv_pp", "div_base", "div_pua", "pua_face", "pua_cv", "div_accum",
        "loan_bal", "db_pp", "surr_value_pp",
    }


def test_timing_and_kind_reject_unknown_values(newbiz):
    for timing in ("BEF_DECR", "BEF_SURR", "BEF_MAT", "AFT_DECR"):
        assert newbiz.pols_if_at(10, timing) >= 0.0
    with pytest.raises(Exception, match="invalid timing"):
        newbiz.pols_if_at(10, "BEF_LUNCH")
    with pytest.raises(Exception, match="invalid kind"):
        newbiz.claim_pp(10, "SURRENDER")
    with pytest.raises(Exception, match="invalid kind"):
        newbiz.claims(10, "SURRENDER")


def test_cells_names_follow_lifelib(whole_life):
    """Names shared with basiclife/BasicTerm_S and savings/CashValue_SE must not drift."""
    shared = {
        "model_point", "age_at_entry", "sex", "sum_assured", "policy_term",
        "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init", "pols_death",
        "pols_lapse", "pols_maturity", "mort_rate", "lapse_rate", "premium_pp",
        "premiums", "claims", "claim_pp", "expenses", "expense_acq", "expense_maint",
        "inflation_rate", "inflation_factor", "premium_taxes", "net_amt_at_risk",
        "net_cf", "liability_cf", "result_cf", "result_pols",
        "check_pols_roll_fwd", "check_pua_roll_fwd",
    }
    names = set(whole_life.Projection.cells) | set(whole_life.Projection.refs)
    assert shared <= names, "missing: %s" % sorted(shared - names)
