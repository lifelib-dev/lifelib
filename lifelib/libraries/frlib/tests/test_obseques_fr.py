"""Golden and structural tests for Obseques_FR_S.

The golden values are the worked example in products/obseques/technical-notes.md
("Worked example"), which projects the RefOBS-VIA anchor cell: a male entering at 50 on
the *difference de millesime* basis, a guaranteed capital of 5000 EUR, *primes viageres*
of 336.03 EUR a year payable annually in advance **for life** with no cessation age, a
guaranteed revalorisation of 1.00 % p.a. compound on the capital with the premium left
alone, a twelve-month *delai de carence* whose illness leg pays the premiums collected and
whose accident leg pays the full capital, no accidental multiplier, no surrender penalty
and no *reduction*.  Model point 1 is that cell.  They are hard-coded here rather than
pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the cent, in-force to five
decimals.  The notes' table **omits expenses** "for clarity", so it is asserted against
``premiums(t)``, ``claims(t, "DEATH")`` and ``claims(t, "LAPSE")`` rather than against
``net_cf``.

``t`` is the model's **0-based** policy month: ``t = 0`` is the first projected month, the
frame is ``t = 0 ... proj_len() - 1``, and the contractual policy year is the 1-based label
``policy_year(t) = t // 12 + 1``.  Every literal month here is that index, so the
*carence* boundary is ``t = 11`` / ``t = 12`` and the two crossovers are at ``t = 168`` and
``t = 204``.  The golden **values** are the notes' own, unchanged.

Beyond the worked example this module asserts the twelve product facts the notes list as
modelling pitfalls, because each is a way an implementation can look right and be wrong -
paying the capital inside the *carence*, dropping the accident leg, accruing the refund
base monthly, revalorising too early, confusing the two crossovers, letting lifetime
premiums stop, reversing the revalorisation coupling, treating lapse as free, treating
*reduction* as termination, applying a premium-stop decrement where no premium is due,
paying zero on an excluded death, and flattening the anti-selection loading.  Each test is
named for the failure it catches.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-6        # in-force displayed to 5 d.p.

MODEL_DIR = LIB / MODELS["Obseques_FR_S"][0]

# t (0-based policy month): (policy year, capital_pp, cum_prem_pp, db_illness,
#     surr_value_pp, pols_if(t) = the notes' l(t), E[premium], E[death outgo],
#     E[surrender outgo])
WORKED_EXAMPLE = {
    0:   (1,  5000.00,   336.03,   336.03,   13.07, 1.00000, 336.03, 0.38, 0.07),
    5:   (1,  5000.00,   336.03,   336.03,   78.40, 0.97129,   0.00, 0.37, 0.39),
    11:  (1,  5000.00,   336.03,   336.03,  156.80, 0.93793,   0.00, 0.36, 0.76),
    12:  (2,  5050.00,   672.06,  5050.00,  169.87, 0.93248, 313.34, 2.79, 0.68),
    23:  (2,  5050.00,   672.06,  5050.00,  313.60, 0.88387,   0.00, 2.64, 1.18),
    59:  (5,  5203.02,  1680.15,  5203.02,  784.01, 0.77719,   0.00, 2.39, 1.81),
    119: (10, 5468.43,  3360.30,  5468.43, 1574.90, 0.65347,   0.00, 3.25, 2.17),
    168: (15, 5747.37,  5040.45,  5747.37, 2205.42, 0.55752, 187.34, 4.50, 2.59),
    179: (15, 5747.37,  5040.45,  5747.37, 2346.97, 0.53639,   0.00, 4.33, 2.65),
    204: (18, 5921.52,  6048.54,  5921.52, 2682.12, 0.48896, 164.30, 5.27, 2.76),
    239: (20, 6040.54,  6720.60,  6040.54, 3151.33, 0.42361,   0.00, 5.55, 2.81),
    299: (25, 6348.67,  8400.75,  6348.67, 3980.74, 0.31507,   0.00, 6.72, 2.63),
    359: (30, 6672.52, 10080.90,  6672.52, 4828.57, 0.21337,   0.00, 7.43, 2.16),
    479: (40, 7370.61, 13441.20,  7370.61, 6429.96, 0.05748,   0.00, 5.46, 0.77),
    539: (45, 7746.59, 15121.35,  7746.59, 7135.11, 0.01799,   0.00, 2.88, 0.26),
}

# The notes' derived monthly factors and the undiscounted totals over t = 0..755.
Q_M_1 = 0.00066912         # 1 - (1 - 0.008000)^(1/12)
W_M_1 = 0.00514301         # 1 - (1 - 0.06)^(1/12)
TOTAL_PREMIUMS = 6184.01
TOTAL_DEATH = 2941.20
TOTAL_LAPSE = 1005.89
TOTAL_NET_BEFORE_EXPENSES = 2236.92


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_obseques_anchor, t):
    """Every cell of the notes' fifteen-row table, to the displayed precision.

    The accidental benefit is asserted here too: it equals ``capital_pp`` at every
    duration, which is why the notes do not print a ``db_accident`` column at all.
    """
    year, capital, cum, db_ill, surr, pols, prem, death, lapse = WORKED_EXAMPLE[t]
    p = fr_obseques_anchor
    assert p.policy_year(t) == year
    assert p.capital_pp(t) == pytest.approx(capital, abs=CENT)
    assert p.cum_prem_pp(t) == pytest.approx(cum, abs=CENT)
    assert p.benefit_pp(t, "ILL") == pytest.approx(db_ill, abs=CENT)
    assert p.benefit_pp(t, "ACC") == pytest.approx(capital, abs=CENT)
    assert p.surr_value_pp(t) == pytest.approx(surr, abs=CENT)
    assert p.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(death, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(lapse, abs=CENT)


def test_the_undiscounted_totals_over_the_full_horizon(fr_obseques_anchor):
    """premiums 6184.01, death 2941.20, surrender 1005.89, net +2236.92 before expenses."""
    p = fr_obseques_anchor
    assert p.proj_len() == 756 == 12 * (112 - 50 + 1)
    df = p.result_cf()
    assert df["premiums"].sum() == pytest.approx(TOTAL_PREMIUMS, abs=CENT)
    assert df["claims_death"].sum() == pytest.approx(TOTAL_DEATH, abs=CENT)
    assert df["claims_lapse"].sum() == pytest.approx(TOTAL_LAPSE, abs=CENT)
    assert (df["premiums"] - df["claims_death"] - df["claims_lapse"]).sum() == (
        pytest.approx(TOTAL_NET_BEFORE_EXPENSES, abs=CENT))
    # The notes' totals are before expenses; result_cf carries them, so net_cf is lower.
    assert df["expenses"].sum() > 0.0
    assert df["net_cf"].sum() < TOTAL_NET_BEFORE_EXPENSES


def test_the_first_month_trace_on_the_shipped_basis(fr_obseques_anchor):
    """E[death] = 1.0 x 0.00066912 x (0.95 x 336.03 + 0.05 x 5000) = 0.380884 at t = 0.

    The notes' placeholder basis, ``q(y) = q_base(x) x 1.25 x s(y)`` with
    ``q_base(x) = 0.0040 x 1.09^(x-50)``, and the shipped **[std]** proxy are the same
    object, so the worked example reproduces without any special-casing.
    """
    p = fr_obseques_anchor
    assert p.mort_antiselect_load == 1.25
    assert p.mort_rate_base(50) == pytest.approx(0.0040, rel=1e-12)
    assert p.mort_rate(0) == pytest.approx(0.008000, rel=1e-12)      # 0.0040 x 1.25 x 1.60
    assert p.mort_rate(12) == pytest.approx(0.0070850, rel=1e-9)     # age 51, s = 1.30
    assert p.mort_rate(168) == pytest.approx(0.0167086, abs=5e-8)    # age 64, s = 1.00
    for x in (55, 65, 80):
        assert p.mort_rate_base(x) == pytest.approx(0.0040 * 1.09 ** (x - 50), rel=1e-9)
    assert p.mort_rate_mth(0) == pytest.approx(Q_M_1, abs=5e-9)
    assert p.lapse_rate(0) == 0.06
    assert p.lapse_rate_mth(0) == pytest.approx(W_M_1, abs=5e-9)
    assert p.benefit_pp(0, "DEATH") == pytest.approx(569.2285, abs=CENT)
    assert p.claims(0, "DEATH") == pytest.approx(0.380884, abs=5e-7)


def test_survivorship_compounds_back_to_the_annual_rates(fr_obseques_anchor):
    """l(12) = 0.992 x 0.94 = 0.93248, and l(24) = l(12) x 0.9929150 x 0.95.

    The notes' own check, and the one that catches a misindexed recursion: the monthly
    decrements must compound back to the annual ones exactly.
    """
    p = fr_obseques_anchor
    assert p.pols_if(12) == pytest.approx(0.992 * 0.94, rel=1e-12)
    assert p.pols_if(12) == pytest.approx(0.93248, abs=INFORCE)
    assert p.pols_if(24) == pytest.approx(0.93248 * (1 - 0.0070850) * 0.95, rel=1e-9)
    assert p.pols_if(24) == pytest.approx(0.87957971, abs=1e-8)
    assert p.pols_if(23) == pytest.approx(0.88387, abs=INFORCE)   # one month earlier
    assert p.check_surv_annual() is True


def test_the_capital_and_the_surrender_value_at_month_204_two_ways(fr_obseques_anchor):
    """5000 x 1.01^17 = 5747.37 x 1.01^3 = 5921.52, and V interpolates to 2682.12.

    ``t = 204`` is the 205th policy month, the row the notes print against the elapsed
    month 205 that the surrender scale is keyed by.
    """
    p = fr_obseques_anchor
    assert p.capital_pp(204) == pytest.approx(5000.0 * 1.01 ** 17, rel=1e-12)
    assert p.capital_pp(204) == pytest.approx(p.capital_pp(168) * 1.01 ** 3, rel=1e-12)
    assert p.capital_pp(204) == pytest.approx(5921.52, abs=CENT)
    assert p.surr_value_pp(204) == pytest.approx(
        2346.97 + (3151.33 - 2346.97) * 25 / 60, abs=CENT)
    # The published anchors are reproduced exactly at their own elapsed months - the
    # anchor at 60 elapsed months is reached at the end of policy month t = 59 - and the
    # scale is held flat beyond the last of them.
    for month, value in ((60, 784.01), (120, 1574.90), (240, 3151.33), (540, 7135.11)):
        assert p.surr_scale_pp(month - 1) == pytest.approx(value, abs=CENT)
    assert p.surr_scale_pp(599) == pytest.approx(7135.11, abs=CENT)


# ---------------------------------------------------------------------------
# The delai de carence


def test_paying_the_capital_inside_the_carence(fr_obseques_anchor):
    """The single worst error available on this product, and it is 8.8x wrong.

    The illness leg inside the waiting period pays ``cum_prem_pp``, not ``capital_pp``.
    Paying the capital takes the first month's expected death outgo from 0.380884 to
    3.345618 and policy year 1 from 4.4274 to 38.8893.
    """
    p = fr_obseques_anchor
    for t in range(12):
        assert p.benefit_pp(t, "ILL") == pytest.approx(p.cum_prem_pp(t), abs=CENT)
        assert p.benefit_pp(t, "ILL") == pytest.approx(336.03, abs=CENT)
        assert p.benefit_pp(t, "ILL") < p.capital_pp(t)
    wrong = p.mort_rate_mth(0) * p.capital_pp(0)
    assert wrong == pytest.approx(3.345618, abs=5e-7)
    assert p.claims(0, "DEATH") == pytest.approx(0.380884, abs=5e-7)
    assert wrong / p.claims(0, "DEATH") == pytest.approx(8.78, abs=0.005)
    year_one = sum(p.claims(t, "DEATH") for t in range(12))
    year_one_wrong = sum(p.pols_if(t) * p.mort_rate_mth(t) * p.capital_pp(t)
                         for t in range(12))
    assert year_one == pytest.approx(4.4274, abs=5e-5)
    assert year_one_wrong == pytest.approx(38.8893, abs=5e-5)


def test_dropping_the_accident_leg_inside_the_carence(fr_obseques_anchor):
    """The mirror-image error: accidental death pays the full capital from day one.

    Treating the whole waiting period as a refund understates the first month by 41 % and
    policy year 1 by the same shape.
    """
    p = fr_obseques_anchor
    assert p.acc_share == 0.05
    for t in range(12):
        assert p.benefit_pp(t, "ACC") == pytest.approx(p.capital_pp(t), abs=CENT)
    refund_only = p.mort_rate_mth(0) * p.cum_prem_pp(0)
    assert refund_only == pytest.approx(0.224846, abs=5e-7)
    assert refund_only / p.claims(0, "DEATH") == pytest.approx(0.59, abs=0.005)
    year_one_wrong = sum(p.pols_if(t) * p.mort_rate_mth(t) * p.benefit_pp(t, "ILL")
                         for t in range(12))
    assert year_one_wrong == pytest.approx(2.6136, abs=5e-5)
    # Nearly half the year-one benefit is the small accidental tail paying the capital.
    assert 0.05 * 5000.0 / p.benefit_pp(0, "DEATH") > 0.43


def test_accruing_the_refund_base_monthly_when_the_premium_is_annual(fr_obseques_anchor):
    """The refund base is a step, constant at 336.03 through months t = 0 to 11.

    Accruing it as ``annual_premium x (t + 1) / 12`` gives 28.00 in the first month and
    understates policy-year-1 death outgo by 26 %.
    """
    p = fr_obseques_anchor
    assert p.prem_freq() == 1
    assert p.cum_prem_pp(0) == pytest.approx(336.03, abs=CENT)
    assert p.cum_prem_pp(11) == pytest.approx(336.03, abs=CENT)
    assert p.cum_prem_pp(12) == pytest.approx(672.06, abs=CENT)
    assert [t for t in range(25) if p.prem_due_pp(t) > 0.0] == [0, 12, 24]
    accrued = sum(p.pols_if(t) * p.mort_rate_mth(t)
                  * (0.95 * 336.03 * (t + 1) / 12 + 0.05 * 5000.0) for t in range(12))
    assert 336.03 / 12 == pytest.approx(28.00, abs=CENT)
    assert accrued == pytest.approx(3.2750, abs=5e-5)
    assert accrued / sum(p.claims(t, "DEATH") for t in range(12)) == pytest.approx(
        0.74, abs=0.005)


def test_the_carence_boundary_is_a_step_not_a_curve(fr_obseques_anchor):
    """A factor of 7.8080 between t = 11 and t = 12, decomposing into three moves.

    In-force 0.994191, monthly mortality 0.885251 as the select uplift drops from 1.60 to
    1.30 while the base rate rises 9 %, and benefit 8.871657 as the blend steps from
    569.2285 to the full uprated capital.  It is the signature discontinuity of the product
    and the reason the grid must be monthly.  The twelve waiting-period months are
    ``t = 0 .. 11``, so the boundary falls at ``t = 12``.
    """
    p = fr_obseques_anchor
    assert p.in_carence(11) is True and p.in_carence(12) is False
    assert p.claims(12, "DEATH") / p.claims(11, "DEATH") == pytest.approx(
        7.8080, abs=5e-5)
    assert p.pols_if(12) / p.pols_if(11) == pytest.approx(0.994191, abs=5e-7)
    assert p.mort_rate_mth(12) / p.mort_rate_mth(11) == pytest.approx(0.885251, abs=5e-7)
    assert p.benefit_pp(12, "DEATH") / p.benefit_pp(11, "DEATH") == pytest.approx(
        8.871657, abs=5e-7)
    assert p.benefit_pp(11, "DEATH") == pytest.approx(
        0.95 * 336.03 + 0.05 * 5000.0, abs=CENT)
    assert p.benefit_pp(12, "DEATH") == pytest.approx(5050.00, abs=CENT)
    # And it is the largest single month-on-month step in the whole death-outgo series.
    outgo = [p.claims(t, "DEATH") for t in range(p.proj_len())]
    steps = [outgo[i] - outgo[i - 1] for i in range(1, len(outgo))]
    assert max(steps) == pytest.approx(outgo[12] - outgo[11], rel=1e-12)


def test_the_accidental_multiplier_applies_past_the_carence_only(obseques):
    """Model point 6 doubles the accidental benefit, capped at 20000 EUR.

    Inside the waiting period the accidental benefit is already the full capital, so
    doubling it there - or applying the multiplier to all deaths - overstates outgo.
    """
    p1, p6 = obseques.Projection[1], obseques.Projection[6]
    assert p6.accident_mult() == 2.0
    assert all(p6.benefit_pp(t, "ACC") == 5000.0 for t in range(12))
    assert p6.benefit_pp(12, "ACC") == pytest.approx(10100.00, abs=CENT)
    assert p6.benefit_pp(12, "ACC") <= p6.accident_cap
    assert p6.claims(12, "DEATH") > p1.claims(12, "DEATH")
    # It moves only the accidental share: 5 % of the capital on top of the blend.
    assert p6.benefit_pp(12, "DEATH") == pytest.approx(5050.0 * 1.05, abs=CENT)
    # And the refund basis is a model point column too - gross, net of the assistance
    # premium, net of instalment charges: three insurers, three bases.  The netting is
    # not a rounding difference.
    p12 = obseques.Projection[12]
    assert p1.carence_refund_basis() == "gross"
    assert p1.refund_pp(0) == pytest.approx(336.03, abs=CENT)
    assert p6.carence_refund_basis() == "net_assistance"
    assert p6.refund_pp(0) == pytest.approx(336.03 - 12.0, abs=CENT)
    assert p12.carence_refund_basis() == "net_instalment"
    assert p12.prem_freq() == 12 and p12.cum_prem_pp(0) == pytest.approx(343.42 / 12)
    assert p12.refund_pp(0) == pytest.approx(343.42 / 12 / 1.022, abs=CENT)
    # Stripping the loading recovers the unloaded annual premium almost exactly.
    assert p12.refund_pp(0) == pytest.approx(336.03 / 12, abs=0.01)


# ---------------------------------------------------------------------------
# The capital is a state variable


def test_revalorising_too_early_or_revalorising_the_wrong_thing(fr_obseques_anchor):
    """PB accrues only to contracts in force at least a year, so year 1 is flat.

    Uprating at issue would make ``capital_pp(0)`` 5050.00 and overstate the year-1
    accidental leg.  And the illness benefit inside the waiting period is a refund of
    premiums, not a capital: it must not carry ``reval_rate``.
    """
    p = fr_obseques_anchor
    assert p.reval_rate() == 0.01
    assert all(p.capital_pp(t) == pytest.approx(5000.00, abs=CENT) for t in range(12))
    assert p.capital_pp(12) == pytest.approx(5050.00, abs=CENT)
    assert p.check_capital_reval() is True
    assert p.benefit_pp(11, "ILL") == p.benefit_pp(0, "ILL")
    assert p.carence_refund_rate() == 0.0
    assert p.refund_pp(11) == pytest.approx(p.cum_prem_pp(11), abs=CENT)


def test_the_simple_revalorisation_variant(obseques):
    """Model point 11 reads "1 % du capital souscrit" as a simple uplift.

    Which reading the wording intends is [unverified]; compound is the reference and this
    is the variation.  They agree in policy year 2 and diverge thereafter.
    """
    p1, p11 = obseques.Projection[1], obseques.Projection[11]
    assert p11.reval_simple() is True
    assert p11.capital_pp(12) == pytest.approx(5050.00, abs=CENT)
    assert p11.capital_pp(180) == pytest.approx(5000.0 * (1 + 0.01 * 15), abs=CENT)
    assert p1.capital_pp(180) == pytest.approx(5000.0 * 1.01 ** 15, abs=CENT)
    assert p1.capital_pp(180) > p11.capital_pp(180)
    assert p11.check_capital_reval() is True


def test_getting_the_revalorisation_coupling_backwards(obseques):
    """Model point 4 is the anchor with the one insurer's premium coupling switched on.

    Five of seven insurers leave the premium alone; one raises the remaining premiums in
    the same proportion.  One flag, read from the model point and never hard-coded.
    """
    p1, p4 = obseques.Projection[1], obseques.Projection[4]
    assert p1.reval_prem_linked() is False and p4.reval_prem_linked() is True
    assert p1.prem_ann(12) == 336.03
    assert p4.prem_ann(12) == pytest.approx(336.03 * 1.01, abs=CENT)
    assert p4.prem_ann(24) == pytest.approx(336.03 * 1.01 ** 2, abs=CENT)
    assert p4.result_cf()["premiums"].sum() > p1.result_cf()["premiums"].sum()
    # The capital is identical on both, so the whole difference is premium income - and
    # indexed premiums reach the capital sooner.
    assert p4.capital_pp(204) == pytest.approx(p1.capital_pp(204), rel=1e-12)
    assert p4.crossover_mth("ISSUE") < p1.crossover_mth("ISSUE")
    assert "reval_prem_linked" in obseques.Data.model_point_table().columns


# ---------------------------------------------------------------------------
# The overrun


def test_measuring_the_overrun_against_the_wrong_capital(fr_obseques_anchor):
    """Two crossovers, three years apart: t = 168 at issue, t = 204 revalorised.

    The overrun-aware lapse module that would raise the rate past the tipping point is a
    pure stress dial and is off in the base run, so the table rate applies on both sides.
    """
    p = fr_obseques_anchor
    assert p.crossover_mth("ISSUE") == 168 and p.policy_year(168) == 15
    assert p.cum_prem_pp(156) < p.capital_0()
    assert p.cum_prem_pp(168) == pytest.approx(5040.45, abs=CENT)
    assert p.cum_prem_pp(168) > p.capital_0()
    assert p.crossover_mth("CURRENT") == 204 and p.policy_year(204) == 18
    assert p.cum_prem_pp(192) < p.capital_pp(192)
    assert p.cum_prem_pp(204) > p.capital_pp(204)
    assert (204 - 168) / 12 == 3.0
    assert p.lapse_overrun_beta == 0.0
    assert p.lapse_rate(167) == p.lapse_rate_base(167) == 0.025
    assert p.lapse_rate(168) == p.lapse_rate_base(168)
    with pytest.raises(FormulaError):
        p.crossover_mth("ORIGINAL")


def test_the_standardised_tables_date_their_columns_a_year_later(obseques):
    """Model point 7 reproduces the notes' subsidiary table, and its age convention.

    The published cumulative-premium columns are dated by the age at the **end** of the
    year, so their "age 65" column is this model's attained age 64 during policy year 15.
    Both conventions are defensible; silently mixing them moves the published crossover by
    up to four years.
    """
    p = obseques.Projection[7]
    assert p.annual_premium() == 164.52
    for label_age, t in ((65, 168), (75, 288), (85, 408), (95, 528)):
        assert p.age(t) == label_age - 1
        assert p.cum_prem_pp(t) == pytest.approx(164.52 * (t // 12 + 1), abs=CENT)
    assert p.cum_prem_pp(168) == pytest.approx(2467.80, abs=CENT)
    assert p.cum_prem_pp(528) == pytest.approx(7403.40, abs=CENT)
    # 164.52 x 31 = 5100.12 first exceeds the capital in policy year 31, at age 80.
    assert p.crossover_mth("ISSUE") == 360
    assert p.policy_year(360) == 31 and p.age(360) == 80
    assert p.cum_prem_pp(360) == pytest.approx(5100.12, abs=CENT)


def test_letting_lifetime_premiums_stop_by_accident(obseques):
    """A cessation age defaulted to anything non-zero removes the overrun entirely.

    Model point 10 is the documented "jusqu'a vos 80 ans" form; the anchor has no
    cessation age at all and is still collecting premiums at attained age 100.  The other
    two premium forms stop of their own accord - a *prime unique* never crosses the
    capital and a *temporaire* may, but it stops - which is the whole argument about this
    product in three rows.
    """
    via, tmp, uni, to80 = (obseques.Projection[1], obseques.Projection[2],
                           obseques.Projection[3], obseques.Projection[10])
    # -1, not 0, is the "never crosses" sentinel: t = 0 is a real month on this frame.
    assert uni.premium_form() == "single" and uni.crossover_mth("ISSUE") == -1
    assert uni.cum_prem_pp(uni.proj_len() - 1) == pytest.approx(4274.04, abs=CENT)
    assert uni.cum_prem_pp(uni.proj_len() - 1) < uni.capital_0()
    assert tmp.premium_form() == "temporary" and tmp.prem_term_y() == 10
    assert tmp.crossover_mth("ISSUE") == 84                # the eighth instalment
    assert tmp.cum_prem_pp(tmp.proj_len() - 1) == pytest.approx(651.26 * 10, abs=CENT)
    assert tmp.prem_due_pp(120) == 0.0
    assert via.prem_cease_age() == 0
    assert via.prem_due_pp(600) == pytest.approx(336.03, abs=CENT)
    assert via.in_paying_period(via.proj_len() - 1) is True
    assert to80.prem_cease_age() == 80
    assert to80.age(348) == 79 and to80.prem_due_pp(348) == pytest.approx(336.03, abs=CENT)
    assert to80.age(360) == 80 and to80.prem_due_pp(360) == 0.0
    assert to80.cum_prem_pp(to80.proj_len() - 1) == pytest.approx(336.03 * 30, abs=CENT)
    assert to80.result_cf()["premiums"].sum() < via.result_cf()["premiums"].sum()


# ---------------------------------------------------------------------------
# Lapse pays money, and reduction is not termination


def test_treating_lapse_as_free(fr_obseques_anchor):
    """*Rachat* pays the *provision mathematique*, so claims_lapse is non-zero from t = 0.

    This is where the UK sibling's model is actively misleading.  Setting it to zero moves
    the anchor cell's undiscounted net stream from 2236.92 to 3242.81 - a 45 %
    overstatement.
    """
    p = fr_obseques_anchor
    df = p.result_cf()
    assert p.claims(0, "LAPSE") > 0.0
    # Every month up to the last, where mortality is forced to 1 and nobody survives to
    # surrender.
    assert (df.loc[df.index <= 743, "claims_lapse"] > 0.0).all()
    assert df.loc[744, "claims_lapse"] == 0.0
    assert df["claims_lapse"].sum() == pytest.approx(TOTAL_LAPSE, abs=CENT)
    without = TOTAL_NET_BEFORE_EXPENSES + TOTAL_LAPSE
    assert without == pytest.approx(3242.81, abs=CENT)
    assert without / TOTAL_NET_BEFORE_EXPENSES - 1 == pytest.approx(0.45, abs=0.005)
    for t in (0, 59, 204, 479):
        assert p.claims(t, "LAPSE") == pytest.approx(
            p.pols_lapse(t) * p.surr_value_pp(t), rel=1e-14)


def test_removing_the_lapse_decrement_raises_the_liability():
    """The opposite sign to the UK sibling, and the reason lapse is not a one-way lever.

    The premiums a lapser stops paying are worth more than the reserve handed back, so
    zero lapse *raises* the undiscounted net stream from 2236.92 to 3165.11.
    """
    model = mx.read_model(MODEL_DIR, name="Obseques_FR_S_nolapse")
    try:
        table = model.Data.lapse_table().copy()
        table["lapse_rate"] = 0.0
        alt = "lapse_table_zero.csv"
        table.to_csv(model.Data.input_dir() / alt)
        try:
            model.Data.lapse_table_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            df = model.Projection[1].result_cf()
            assert df["claims_lapse"].sum() == 0.0
            net = (df["premiums"] - df["claims_death"] - df["claims_lapse"]).sum()
            assert net == pytest.approx(3165.11, abs=CENT)
            assert net > TOTAL_NET_BEFORE_EXPENSES
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_treating_reduction_as_termination(obseques):
    """Model point 5 routes half of every premium-stop to a paid-up contract.

    Non-payment produces a paid-up contract, not an exit, wherever the surrender value is
    sufficient; routing every premium-stop to the exit removes a death liability the
    contract still owes.  The paid-up population must appear in the death outgo and must
    pay ``reduced_capital_pp``, not ``capital_pp``.  Carrying the aggregate capital
    alongside the count is what removes the need for a per-conversion cohort dimension.
    """
    p1, p5 = obseques.Projection[1], obseques.Projection[5]
    assert p1.reduction_share() == 0.0 and p5.reduction_share() == 0.5
    assert (p1.result_cf()["pols_paid_up"] == 0.0).all()
    assert (p1.result_cf()["claims_death_paid_up"] == 0.0).all()
    assert p5.pols_paid_up(199) > 0.0
    assert p5.result_cf()["claims_death_paid_up"].sum() > 0.0
    # Half the premium-stops convert and half surrender, so surrender outgo halves.
    assert p5.pols_convert(59) == pytest.approx(0.5 * p5.pols_exit(59), rel=1e-12)
    assert p5.result_cf()["claims_lapse"].sum() == pytest.approx(
        0.5 * TOTAL_LAPSE, rel=0.02)
    # The paid-up capital is the provision turned into cover at the attained age, far
    # below the guaranteed capital the contract would otherwise pay.
    assert p5.reduced_capital_pp(59) == pytest.approx(
        p5.surr_value_pp(59) / p5.single_prem_rate(54), rel=1e-12)
    assert p5.reduced_capital_pp(59) < 0.25 * p5.capital_pp(59)
    # Both strands roll forward on the same survival factor.
    for t in (99, 299):
        assert p5.pols_paid_up(t + 1) == pytest.approx(
            p5.pols_paid_up(t) * (1 - p5.mort_rate_mth(t)) + p5.pols_convert(t),
            rel=1e-12)
        assert p5.capital_paid_up(t + 1) == pytest.approx(
            p5.capital_paid_up(t) * (1 - p5.mort_rate_mth(t))
            + p5.pols_convert(t) * p5.benefit_pp(t, "PAID_UP"), rel=1e-12)
        assert p5.claims(t, "DEATH_PAID_UP") == pytest.approx(
            p5.capital_paid_up(t) * p5.mort_rate_mth(t), rel=1e-14)
    # Paid-up policies pay no premium.
    assert p5.premiums(299) == pytest.approx(
        p5.prem_due_pp(299) * p5.pols_if(299), rel=1e-14)


def test_applying_a_premium_stop_decrement_where_no_premium_is_due(obseques):
    """After cessation, in a *prime unique* cell and in the paid-up state there is none.

    A decrement there silently destroys liability.
    """
    uni, tmp, to80 = (obseques.Projection[3], obseques.Projection[2],
                      obseques.Projection[10])
    assert all(uni.lapse_rate_mth(t) == 0.0 for t in (0, 12, 119, 599))
    assert (uni.result_cf()["claims_lapse"] == 0.0).all()
    assert tmp.lapse_rate(119) == 0.025 and tmp.lapse_rate(120) == 0.0
    assert tmp.lapse_rate_mth(120) == 0.0 and tmp.pols_lapse(120) == 0.0
    assert to80.lapse_rate(359) == 0.025 and to80.lapse_rate(360) == 0.0
    for point_id in obseques.Data.model_point_table().index:
        assert obseques.Projection[point_id].check_lapse_gate() is True


def test_paying_zero_on_an_excluded_death(obseques):
    """An excluded death pays the *valeur de rachat*, not nothing.

    Suicide in year 1, war, nuclear and murder by a beneficiary do not extinguish the
    contract, so an exclusion modelled as a zero benefit understates outgo by exactly
    ``surr_value_pp`` per excluded death.  The model carries no zero-benefit exclusion
    machinery, and the amount such a death is owed is published from the first projected
    month on every model point.
    """
    names = set(obseques.Projection.cells) | set(obseques.Projection.refs)
    assert not [n for n in names if "exclu" in n or n.startswith("suicide")]
    for point_id in obseques.Data.model_point_table().index:
        p = obseques.Projection[point_id]
        assert p.surr_value_pp(0) > 0.0 and p.surr_value_pp(239) > 0.0


def test_using_the_wrong_age_basis_or_flattening_the_loading(fr_obseques_anchor):
    """*Difference de millesime*, stepping at the anniversary, and a duration-shaped uplift.

    Age last birthday shifts the whole mortality lookup by up to a year at entry.  And the
    anti-selection excess belongs at durations 1-3 and is largest in year 1 even though a
    year-1 illness death costs only a refund; a flat loading understates the year-2 step.
    """
    p = fr_obseques_anchor
    assert p.issue_month() == 1 and p.age_at_entry() == 50
    assert p.age(0) == 50 and p.age(11) == 50 and p.age(12) == 51
    assert p.age(p.proj_len() - 1) == 112
    assert (p.select_uplift(0), p.select_uplift(12), p.select_uplift(24)) == (
        1.60, 1.30, 1.15)
    assert p.select_uplift(36) == 1.00 and p.select_uplift(599) == 1.00


# ---------------------------------------------------------------------------
# Roll-forward, truncation and what the product does not have


def test_every_roll_forward_closes(obseques):
    """On every model point, not only on the anchor."""
    for point_id in obseques.Data.model_point_table().index:
        p = obseques.Projection[point_id]
        assert p.check_pols_roll_fwd() is True, point_id
        assert p.check_surv_annual() is True, point_id
        assert p.check_capital_reval() is True, point_id
        assert p.check_truncation() is True, point_id
    p = obseques.Projection[5]                        # the strand-splitting one
    for t in (49, 199, 399):
        out = p.pols_death(t) + p.pols_death_paid_up(t) + p.pols_lapse(t)
        assert p.pols_all(t) - p.pols_all(t + 1) == pytest.approx(out, abs=1e-12)
    assert p.pols_convert(199) > 0.0                  # conversions move between strands


def test_the_projection_is_exhausted_at_the_limiting_age(obseques):
    """Mortality is forced to 1 at omega_age, so nothing falls off the end.

    ``proj_len`` is measured from the entry age, so the entry-70 cell has a shorter
    horizon and the same property.
    """
    p = obseques.Projection[1]
    last = p.proj_len() - 1                           # the last projected month
    assert p.omega_age == 112
    assert p.mort_rate(last) == 1.0 and p.mort_rate_mth(last) == 1.0
    assert p.pols_all(last + 1) == pytest.approx(0.0, abs=1e-12)
    assert p.pols_if(last + 2) == 0.0
    assert all(p.mort_rate(t) <= 1.0 for t in range(0, p.proj_len(), 12))
    p8 = obseques.Projection[8]
    assert p8.age_at_entry() == 70 and p8.sex() == "F"
    assert p8.proj_len() == 516 == 12 * (112 - 70 + 1)
    assert p8.age(p8.proj_len() - 1) == 112 and p8.check_truncation() is True
    # The female rates are a flat factor on the male proxy.
    assert p8.mort_rate_base(70) == pytest.approx(0.60 * 0.0040 * 1.09 ** 20, rel=1e-9)


def test_there_is_no_maturity_and_no_account_value(obseques):
    """The contract ends only on death, on *rachat* or on lapse - a cited product fact."""
    names = set(obseques.Projection.cells) | set(obseques.Projection.refs)
    for absent in ("av_pp_at", "av_at", "prem_to_av_pp", "cv_pp", "asset_share", "mvr",
                   "claims_maturity", "pols_maturity", "withdrawals", "wd_free_pp"):
        assert absent not in names
    p = obseques.Projection[1]
    for kind in ("MATURITY", "REFUND"):
        with pytest.raises(FormulaError):
            p.claims(0, kind)
    with pytest.raises(FormulaError):
        p.benefit_pp(0, "SURRENDER")
    with pytest.raises(FormulaError):
        p.pols_if_at(0, "BEF_NOTHING")


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_both_signs_of_the_net_flow(fr_obseques_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign."""
    p = fr_obseques_anchor
    df = p.result_cf()
    assert list(df.index) == list(range(756)) and df.index.name == "t"
    assert df.index[0] == 0 and df.index[-1] == p.proj_len() - 1
    assert list(df.columns) == [
        "pols_if", "pols_paid_up", "premiums", "claims_death", "claims_death_paid_up",
        "claims_lapse", "expenses", "liability_cf", "net_cf",
    ]
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-12)
    outgo = df[["claims_death", "claims_death_paid_up", "claims_lapse",
                "expenses"]].sum(axis=1)
    assert (outgo - df["premiums"] - df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    # The notes' table omits expenses, so net_cf equals no column of it.
    assert p.expenses(0) == pytest.approx(150.0 + 24.0 / 12, abs=CENT)
    assert p.expenses(12) == pytest.approx(24.0 / 12 * 1.018 * p.pols_all(12), rel=1e-12)
    assert p.net_cf(0) == pytest.approx(
        p.premiums(0) - p.claims(0) - p.expenses(0), rel=1e-14)


def test_docstrings_describe_the_current_structure(obseques):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = obseques.doc
    for phrase in ("contrat obseques", "mechanics demonstration", "external",
                   "once per model", "carence", "WOL_UK_S"):
        assert phrase in doc
    proj = obseques.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "pols_if", "pols_paid_up", "capital_pp",
                  "cum_prem_pp", "surr_value_pp", "crossover_mth", "benefit_pp"):
        assert cells in proj
    data = obseques.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "surr_scale_table",
                  "single_prem_table"):
        assert cells in data
    # And the names shared with lifelib and with the rest of this library must not drift.
    shared = {
        "model_point", "age_at_entry", "sex", "proj_len", "age", "pols_if",
        "pols_if_at", "pols_if_init", "pols_death", "pols_lapse", "mort_rate",
        "mort_rate_mth", "lapse_rate", "lapse_rate_mth", "premiums", "claims",
        "benefit_pp", "expenses", "inflation_rate", "inflation_factor", "liability_cf",
        "net_cf", "result_cf", "policy_year", "duration", "duration_mth", "omega_age",
    }
    names = set(obseques.Projection.cells) | set(obseques.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    assert "claims" not in obseques.Projection[1].result_cf().columns


def test_the_shipped_inputs_mark_their_own_provenance():
    """Six external CSVs, each saying which rows are transcribed and which are [std].

    TH 00-02 and TF 00-02 are the homologated regulatory tables for this product; they are
    cited by name and never redistributed, so what ships is an INSEE-shaped Gompertz proxy
    anchored on the notes' own placeholder rate.  And a premium and a surrender scale from
    different insurers produce a wrong margin quietly - the lifetime premium for the same
    capital spans 2.0:1 across the retrieved set at entry age 50, 1.7:1 at 60 and 1.5:1 at
    70 - so the pairing is checked as a data-integrity question rather than left as a
    nicety.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "mort_table.csv", "select_table.csv",
                "lapse_table.csv", "surr_scale_table.csv", "single_prem_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}

    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert mort["provenance"].notna().all()
    assert set(mort["sex"]) == {"M", "F"} and mort["mort_rate"].max() <= 1.0
    anchor = mort[mort["provenance"].str.contains("anchor")]
    assert list(anchor["sex"]) == ["M"] and list(anchor["age"]) == [50]
    assert anchor["mort_rate"].iloc[0] * 1.25 * 1.60 == pytest.approx(0.008, rel=1e-12)

    for name in ("select_table.csv", "lapse_table.csv"):
        table = pd.read_csv(MODEL_DIR.parent / name)
        assert table["provenance"].str.startswith("[std]").all()

    surr = pd.read_csv(MODEL_DIR.parent / "surr_scale_table.csv")
    axa = surr[(surr["scale"] == "axa_50_viager") & (surr["month"] > 0)]
    assert axa["provenance"].str.startswith("[S14]").all()
    assert axa[axa["month"] == 60]["surr_value"].iloc[0] == pytest.approx(784.01)

    single = pd.read_csv(MODEL_DIR.parent / "single_prem_table.csv")
    anchors = single[single["provenance"].str.startswith("[S5]")]
    assert list(anchors["age"]) == [50, 60, 70]
    assert list(anchors["single_prem_rate"]) == pytest.approx(
        [4274.04 / 5000, 4548.60 / 5000, 4819.56 / 5000], rel=1e-12)

    points = pd.read_csv(MODEL_DIR.parent / "model_point_table.csv")
    assert set(points["surr_scale"]) <= set(surr["scale"])
    assert len(points) >= 8 and points["policy_id"].is_unique
    assert set(points["premium_form"]) == {"single", "temporary", "lifetime"}


# The nine quinquennial anchors each standardised table publishes, transcribed from
# _research/obseques.md section 11 exactly as printed, at 60 .. 540 months.
PUBLISHED_SURR_ANCHORS = {
    "axa_50_viager": [784.01, 1574.90, 2346.97, 3151.33, 3980.74,
                      4828.57, 5659.93, 6429.96, 7135.11],
    "axa_50_temp10": [2701.65, 5767.93, 6003.11, 6256.67, 6530.11,
                      6824.80, 7142.86, 7485.99, 7854.08],
    "cnp_50_viager": [650.15, 1275.19, 1876.68, 2460.79, 3004.02,
                      3484.41, 3876.12, 4176.77, 4399.53],
    "cnp_50_unique": [4162.06, 4282.64, 4398.69, 4511.38, 4616.18,
                      4708.86, 4784.43, 4842.43, 4885.41],
    "sogecap_70_viager": [1148.0, 2067.0, 2808.0, 3369.0, 3775.0,
                          4129.0, 4473.0, 5000.0, 5000.0],
    "mutex_50_temp25": [981.0, 1958.0, 2933.0, 3938.0, 5074.0,
                        5057.0, 5043.0, 5033.0, 5026.0],
}


def test_every_published_surrender_anchor_is_shipped_not_interpolated(obseques):
    """Each grid carries all nine published anchors, not a sample of them.

    An omitted anchor does not round the scale, it replaces a published number with a
    straight line between its neighbours.  The Mutex *temporaire* 25 ans grid is the case
    that shows why: it **peaks** at 5074 EUR at 25 years and then declines, because the
    0.40 % p.a. charge on the guaranteed capital keeps running after the last premium.
    Dropping the 300-month anchor puts the model at 4497.50 there - 11 % low - and turns a
    peak-then-decline shape into a monotone rise.
    """
    import pandas as pd

    surr = pd.read_csv(MODEL_DIR.parent / "surr_scale_table.csv")
    months = [60 * k for k in range(1, 10)]
    assert set(surr["scale"]) == set(PUBLISHED_SURR_ANCHORS)

    for scale, values in PUBLISHED_SURR_ANCHORS.items():
        grid = surr[surr["scale"] == scale].set_index("month")["surr_value"]
        assert list(grid.index) == [0] + months, scale
        assert list(grid.loc[months]) == pytest.approx(values, abs=CENT), scale

    peak = PUBLISHED_SURR_ANCHORS["mutex_50_temp25"]
    assert peak[4] == max(peak) and peak[5] < peak[4] < 2 * peak[3]
    dropped = (peak[3] + peak[5]) / 2                     # the 300-month interpolant
    assert dropped == pytest.approx(4497.50, abs=CENT)
    assert dropped < 0.90 * peak[4]

    # And the shipped model reads the anchors, at their own elapsed months, on every
    # scale.  The CSV's ``month`` key is a duration from issue and does not move with the
    # 0-based frame; the anchor at ``month`` elapsed months is reached at the end of
    # policy month ``month - 1``.
    points = pd.read_csv(MODEL_DIR.parent / "model_point_table.csv")
    for point_id, scale in zip(points["point_id"], points["surr_scale"]):
        proj = obseques.Projection[int(point_id)]
        for month, value in zip(months, PUBLISHED_SURR_ANCHORS[scale]):
            if month <= proj.proj_len():
                assert proj.surr_scale_pp(month - 1) == pytest.approx(
                    value, abs=CENT), (scale, month)


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a homologated table and own experience."""
    import pandas as pd

    lighter = pd.read_csv(MODEL_DIR.parent / "mort_table.csv",
                          index_col=["sex", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="Obseques_FR_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].claims(12, "DEATH")
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].mort_rate(0) == pytest.approx(0.004, rel=1e-12)
            assert model.Projection[1].claims(12, "DEATH") < base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Obseques_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Obseques_FR_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[5], abs=INFORCE)
            assert anchor.claims(t, "DEATH") == pytest.approx(row[7], abs=CENT)
            assert anchor.claims(t, "LAPSE") == pytest.approx(row[8], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
