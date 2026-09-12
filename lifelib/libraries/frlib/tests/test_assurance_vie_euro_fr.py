"""Golden and structural tests for Euro_FR_S.

The golden values are the worked example in
products/assurance_vie_euro/technical-notes.md ("Worked example"): an in-force
euro-support cell with EUR 100,000 of `epargne acquise` at duration 5, male aged 60,
EUR 2,400 a year of `versements` and EUR 3,000 a year of `rachats partiels` from ``y = 5``,
a 0.60% management charge, a nil TMG, a 2.30% target `taux servi`, a 17.2% social levy, and
an opening PPB of EUR 4,000 in eight equal vintages falling due at ``y = 0`` to ``y = 7``.
Model point 1 is that cell.  They are hard-coded here rather than pickled so that a reviewer
can compare them against the notes by eye, to the precision the notes display: money to the
cent, rates to the fourth decimal of a percentage.

``t`` is **0-based** throughout and counts policy **months**: ``t = 0`` is the first
projected month and the frame is ``t = 0 ... proj_len() - 1`` with ``proj_len() = 480``.
The model carries a financial-year layer underneath it, indexed by the projection year
``y = t // 12``, and the golden dictionaries below are keyed by ``y`` wherever every
quantity in them is a financial-year quantity - which is the whole of Tables 1 and 2 and
the year-5 trace, and the reason those figures are unchanged by the change of grid.  The
cash-flow extract is not: it is read off ``result_cf_annual()``, the monthly frame summed
into its projection years, and its flow columns moved.  ``opens(y)`` and ``anniv(y)``
below turn a projection year into its first and last month.

Beyond the worked example this module asserts the product facts the notes list as modelling
pitfalls, one test each and each named for the failure it catches, because every one of
them is a way an implementation can look right and be wrong - and, since the conversion to
a monthly grid, one test for each timing decision the grid forced the model to take a view
on.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import LIB, MODELS


def model_files(folder):
    """The model's own file names, ignoring ``__pycache__``.

    Those caches appear as soon as anything imports the model - which building the
    autodoc API pages does - and are not part of it.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def opens(y):
    """The **first** month of projection year ``y``: ``12 * y``.

    The month the annual layer reads its opening balance at, and the row
    ``result_cf_annual()`` takes its ``pols_if`` from.
    """
    return 12 * y


def anniv(y):
    """The **last** month of projection year ``y``: ``12 * y + 11``.

    The 31 December of year ``y``, where the whole of the revalorisation, the social levy
    and the management charge lands - ``is_anniv(t)`` is true here and nowhere else.
    """
    return 12 * y + 11


CENT = 0.01           # money, to the precision the notes display
RATE = 1e-6           # rates, displayed as a percentage to four decimals

PROJ_LEN = 480        # 12 * proj_years, the number of projected policy months
PROJ_YEARS = 40

MODEL_DIR = LIB / MODELS["Euro_FR_S"][0]

CHECKS = ("check_av_roll_fwd", "check_ppb_roll_fwd", "check_ppb_clock",
          "check_pols_roll_fwd", "check_pb_allocation", "check_cliquet",
          "check_guar_floor", "check_decrements_compound")

# Table 1 -- the taux servi and the PPB.  A financial-year statement, so every figure is
# the one the annual-step model produced and only the key's name changed, t -> y.
# y: (r_fin, pm_avg_pp, 0.85 x fin_acct_pp, policyholder technical share, pb_min_pp,
#     ts_stat, PPB release less dotation, ppb_pp(y+1), ts_net)
TABLE_1 = {
    0: (0.0330, 101200.00, 2950.86, 121.00, 3071.86, 0.024354, 362.94, 3637.06, 0.027941),
    1: (0.0325, 105941.25, 3027.10, 132.49, 3159.59, 0.023824, 412.70, 3224.36, 0.027720),
    2: (0.0320, 110772.80, 3100.72, 144.21, 3244.93, 0.023294, 467.48, 2756.88, 0.027514),
    3: (0.0310, 115696.36, 3121.24, 156.14, 3277.39, 0.022327, 500.00, 2256.88, 0.026649),
    4: (0.0295, 120649.25, 3081.87, 168.15, 3250.02, 0.020938, 500.00, 1756.88, 0.025082),
    5: (0.0280, 124054.88, 2994.32, 176.28, 3170.60, 0.019558, 500.00, 1256.88, 0.023589),
    6: (0.0265, 125877.84, 2863.71, 180.45, 3044.16, 0.018183, 606.30, 650.58, 0.023000),
    7: (0.0255, 127675.06, 2781.46, 184.55, 2966.01, 0.017231, 650.58, 0.00, 0.022327),
    8: (0.0245, 129435.30, 2695.49, 188.55, 2884.04, 0.016282, 0.00, 0.00, 0.016282),
    9: (0.0240, 130580.26, 2663.84, 191.01, 2854.85, 0.015863, 0.00, 0.00, 0.015863),
    10: (0.0235, 131695.35, 2630.61, 193.39, 2824.00, 0.015443, 0.00, 0.00, 0.015443),
    11: (0.0230, 132779.35, 2595.84, 195.68, 2791.51, 0.015024, 0.00, 0.00, 0.015024),
}

# Table 2 -- the epargne acquise roll-forward, also a financial-year statement.  av_pp is
# read at the year's first and last-plus-one month, av_pp(12y) and av_pp(12(y+1)).
# y: (av_pp(12y), prem_to_av_pp, withdrawals_pp, int_credited_pp, soc_levy_pp,
#     av_pp(12(y+1)))
TABLE_2 = {
    0: (100000.00, 2400.00, 0.00, 2827.60, 486.35, 104741.25),
    1: (104741.25, 2400.00, 0.00, 2936.65, 505.10, 109572.80),
    2: (109572.80, 2400.00, 0.00, 3047.77, 524.22, 114496.36),
    3: (114496.36, 2400.00, 0.00, 3083.21, 530.31, 119449.25),
    4: (119449.25, 2400.00, 0.00, 3026.13, 520.49, 124354.88),
    5: (124354.88, 2400.00, 3000.00, 2926.27, 503.32, 126177.84),
    6: (126177.84, 2400.00, 3000.00, 2895.19, 497.97, 127975.06),
    7: (127975.06, 2400.00, 3000.00, 2850.54, 490.29, 129735.30),
    8: (129735.30, 2400.00, 3000.00, 2107.43, 362.48, 130880.26),
    9: (130880.26, 2400.00, 3000.00, 2071.36, 356.27, 131995.35),
    10: (131995.35, 2400.00, 3000.00, 2033.83, 349.82, 133079.35),
    11: (133079.35, 2400.00, 3000.00, 1994.84, 343.11, 134131.08),
}

# The notes' month-level table: the twelve months of projection year 5, where the two
# layers meet.  The level versement and rachat net to -EUR 50 a month and the whole of
# the year's revalorisation and levy arrives in the last month, t = 71.
# t: (av_pp(t), prem_to_av_mth_pp, withdrawals_mth_pp, int_credited_mth_pp,
#     soc_levy_mth_pp, av_pp(t+1))
MONTHS = {
    60: (124354.8847, 200.00, 250.00, 0.0000, 0.0000, 124304.8847),
    61: (124304.8847, 200.00, 250.00, 0.0000, 0.0000, 124254.8847),
    62: (124254.8847, 200.00, 250.00, 0.0000, 0.0000, 124204.8847),
    63: (124204.8847, 200.00, 250.00, 0.0000, 0.0000, 124154.8847),
    64: (124154.8847, 200.00, 250.00, 0.0000, 0.0000, 124104.8847),
    65: (124104.8847, 200.00, 250.00, 0.0000, 0.0000, 124054.8847),
    66: (124054.8847, 200.00, 250.00, 0.0000, 0.0000, 124004.8847),
    67: (124004.8847, 200.00, 250.00, 0.0000, 0.0000, 123954.8847),
    68: (123954.8847, 200.00, 250.00, 0.0000, 0.0000, 123904.8847),
    69: (123904.8847, 200.00, 250.00, 0.0000, 0.0000, 123854.8847),
    70: (123854.8847, 200.00, 250.00, 0.0000, 0.0000, 123804.8847),
    71: (123804.8847, 200.00, 250.00, 2926.2730, 503.3190, 126177.8387),
}

# The decrement and cash-flow extract, read off result_cf_annual().  lapse_rate and
# pols_if are the annual-grid figures unchanged, because the monthly rates compound back
# to the annual ones; the flow columns are NOT, and the annual grid's figures are given
# beside them because the gap is what the finer grid is for:
#   premiums     2400.00 / 2184.19 / 1771.44 / 1473.06   ->  the fourth column below
#   withdrawals     0.00 /    0.00 / 2214.30 / 1841.32
#   claims_death  628.45 /  743.00 /  862.56 /  968.78
#   claims_lapse 4164.51 / 8276.62 / 4613.46 / 4989.75
#   expenses      378.20 /  375.34 /  339.56 /  294.65
#   liability_cf 2771.16 / 7210.78 / 6258.43 / 6621.44
# y: (lapse_rate(12y), pols_if(12y), premiums, withdrawals, claims_death, claims_lapse,
#     expenses, liability_cf)
DECREMENTS = {
    0: (0.040000, 1.000000, 2349.24, 0.00, 597.66, 4046.14, 370.20, 2664.76),
    2: (0.080000, 0.910080, 2096.12, 0.00, 693.89, 8054.76, 360.21, 7012.73),
    5: (0.050000, 0.738099, 1723.18, 2153.97, 829.63, 4561.82, 330.31, 6152.55),
    8: (0.062873, 0.613775, 1422.28, 1777.85, 931.07, 4967.10, 284.49, 6538.23),
}


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("y", sorted(TABLE_1))
def test_the_worked_example_row(fr_euro_anchor, y):
    """Every cell of the notes' Tables 1 and 2 for projection year y, to the displayed
    precision.

    Table 2's recursion is then restated on the notes' own printed numbers, so that a row
    which reproduces the model still has to reproduce the next row's opening balance.

    Both tables are financial-year statements and every golden in them is the number the
    annual-step model carried: the monthly grid leaves anniversary quantities exactly
    where the annual grid put them.  What the grid changed is the *index* each is read at
    - ``av_pp(5)`` is now ``av_pp(60)`` and ``av_pp(6)`` is ``av_pp(72)`` - and that no
    interest arrives before 31 December, which the last assertion states directly.
    """
    r_fin, pm, fin85, ph_tech, pb_min, ts_stat, ppb_flow, ppb_next, ts_net = TABLE_1[y]
    p = fr_euro_anchor
    assert p.r_fin(y) == pytest.approx(r_fin, abs=RATE)
    assert p.pm_avg_pp(y) == pytest.approx(pm, abs=CENT)
    assert 0.85 * p.fin_acct_pp(y) == pytest.approx(fin85, abs=CENT)
    assert p.tech_acct_pp(y) - p.insurer_tech_share_pp(y) == pytest.approx(
        ph_tech, abs=CENT)
    assert p.pb_min_pp(y) == pytest.approx(pb_min, abs=CENT)
    assert p.ts_stat(y) == pytest.approx(ts_stat, abs=RATE)
    assert p.ppb_release_pp(y) - p.ppb_dotation_pp(y) == pytest.approx(
        ppb_flow, abs=CENT)
    assert p.ppb_pp(y + 1) == pytest.approx(ppb_next, abs=CENT)
    assert p.ts_net(y) == pytest.approx(ts_net, abs=RATE)

    av, prem, wd, interest, levy, av_next = TABLE_2[y]
    assert p.av_pp(opens(y)) == pytest.approx(av, abs=CENT)
    assert p.prem_to_av_pp(y) == pytest.approx(prem, abs=CENT)
    assert p.withdrawals_pp(y) == pytest.approx(wd, abs=CENT)
    assert p.int_credited_pp(y) == pytest.approx(interest, abs=CENT)
    assert p.soc_levy_pp(y) == pytest.approx(levy, abs=CENT)
    assert p.av_pp(opens(y + 1)) == pytest.approx(av_next, abs=CENT)
    assert p.av_pp(opens(y + 1)) == pytest.approx(
        av + prem - wd + interest - levy, abs=2 * CENT)
    # Nothing but the instalments has moved by the opening of 31 December: the account
    # entering the last month of the year is the opening balance plus eleven twelfths of
    # the year's net movement, with no interest in it at all.
    assert p.av_pp(anniv(y)) == pytest.approx(
        av + (11.0 / 12.0) * (prem - wd), abs=2 * CENT)


@pytest.mark.parametrize("t", sorted(MONTHS))
def test_the_worked_example_month_of_year_five(fr_euro_anchor, t):
    """The notes' month-level table: the twelve months of projection year 5.

    This is the one place a reader sees the two layers meet.  Eleven months move the
    account by the level instalments alone, EUR 200 in and EUR 250 out; the twelfth
    carries the whole of ``int_credited_pp(5)`` and ``soc_levy_pp(5)``.
    """
    av, prem, wd, interest, levy, av_next = MONTHS[t]
    p = fr_euro_anchor
    assert p.av_pp(t) == pytest.approx(av, abs=CENT)
    assert p.prem_to_av_mth_pp(t) == pytest.approx(prem, abs=CENT)
    assert p.withdrawals_mth_pp(t) == pytest.approx(wd, abs=CENT)
    assert p.int_credited_mth_pp(t) == pytest.approx(interest, abs=CENT)
    assert p.soc_levy_mth_pp(t) == pytest.approx(levy, abs=CENT)
    assert p.av_pp(t + 1) == pytest.approx(av_next, abs=CENT)
    assert p.is_anniv(t) is (t == 71)
    # The mid-month-weighted base is literally the balance at the middle of the year on a
    # level schedule: the opening of month 66, the seventh of the twelve.
    assert p.pm_avg_pp(5) == pytest.approx(p.av_pp(66), abs=1e-9)


@pytest.mark.parametrize("y", sorted(DECREMENTS))
def test_the_decrement_and_cash_flow_extract(fr_euro_anchor, y):
    """The notes' decrement extract, including the duration-8 surrender step at y = 2.

    The decrement columns are read at the year's first month and are the annual-grid
    figures unchanged.  The flow columns are read off ``result_cf_annual()`` - the
    monthly frame summed into its projection years - and are not: instalments are now
    collected from a block that decrements every month, expenses accrue on the in force
    of each month, and claims fall at the end of the month of exit.
    """
    lapse, pols, prem, wd, death, lapse_cl, exp, liab = DECREMENTS[y]
    p = fr_euro_anchor
    assert p.lapse_rate(opens(y)) == pytest.approx(lapse, abs=RATE)
    assert p.pols_if(opens(y)) == pytest.approx(pols, abs=1e-6)
    row = p.result_cf_annual().loc[y]
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["withdrawals"] == pytest.approx(wd, abs=CENT)
    assert row["claims_death"] == pytest.approx(death, abs=CENT)
    assert row["claims_lapse"] == pytest.approx(lapse_cl, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["liability_cf"] == pytest.approx(liab, abs=CENT)
    assert row["net_cf"] == pytest.approx(-liab, abs=CENT)
    assert row["pols_if"] == pytest.approx(pols, abs=1e-6)


def test_the_trace_at_year_five_at_full_precision(fr_euro_anchor):
    """``y = 5`` is the year in which every lever is active at once.

    The discretionary release the target wants is EUR 426.99, the vintage falling due is
    EUR 500.00, and the forced release wins - so the rate lands *above* target.  Every
    number here is a financial-year quantity and is the annual-step model's, to the last
    bit; ``av_pp(6)`` on that grid is ``av_pp(72)`` on this one.
    """
    p = fr_euro_anchor
    assert p.pm_avg_pp(5) == pytest.approx(124054.884701, abs=1e-6)
    assert p.fee_pp(5) == pytest.approx(744.329308, abs=1e-6)
    assert p.expenses_pp(5) == pytest.approx(460.046913, abs=1e-6)
    assert p.fin_acct_pp(5) == pytest.approx(3522.729293, abs=1e-6)
    assert 0.85 * p.fin_acct_pp(5) == pytest.approx(2994.319899, abs=1e-6)
    assert p.tech_acct_pp(5) == pytest.approx(284.282396, abs=1e-6)
    assert p.insurer_tech_share_pp(5) == pytest.approx(108.000000, abs=1e-6)
    assert p.pb_acct_pp(5) == pytest.approx(3170.602295, abs=1e-6)
    assert p.pb_min_pp(5) == pytest.approx(p.pb_acct_pp(5), abs=1e-9)
    assert p.ts_stat(5) == pytest.approx(0.01955806, abs=1e-8)
    assert p.pb_target_pp(5) == pytest.approx(3597.591656, abs=1e-6)
    assert p.ppb_discr_rel_pp(5) == pytest.approx(426.989361, abs=1e-6)
    assert p.ppb_forced_pp(5) == pytest.approx(500.000000, abs=1e-6)
    assert p.ppb_release_pp(5) == pytest.approx(500.000000, abs=1e-6)
    assert p.pb_credited_pp(5) == pytest.approx(3670.602295, abs=1e-6)
    assert p.ts_net(5) == pytest.approx(0.02358853, abs=1e-8)
    assert p.int_credited_pp(5) == pytest.approx(2926.272987, abs=1e-6)
    assert p.soc_levy_pp(5) == pytest.approx(503.318954, abs=1e-6)
    assert p.av_pp(opens(6)) == pytest.approx(126177.838734, abs=1e-6)
    # And the same rate from a different direction: 0.85 x financial + technical share
    # - the charge + the PPB flow, all over the base.  ``y = 8`` has the PPB exhausted.
    for y, expected in ((5, 0.02358853), (8, 0.01628173)):
        base = p.pm_avg_pp(y)
        built = (0.85 * p.fin_acct_pp(y) / base
                 + (p.tech_acct_pp(y) - p.insurer_tech_share_pp(y)) / base
                 - p.fee_rate()
                 + (p.ppb_release_pp(y) - p.ppb_dotation_pp(y)) / base)
        assert built == pytest.approx(expected, abs=1e-8)
        assert built == pytest.approx(p.ts_net(y), abs=1e-12)


def test_the_twelve_year_identities_close(fr_euro_anchor):
    """Interest EUR 31,800.82 and levies EUR 5,469.74, reaching EUR 134,131.08.

    The same total the other way: PB credited gross of the charge is EUR 40,538.97 less
    `frais de gestion` of EUR 8,738.15.  All of that is unchanged by the grid.  The
    fund-level identity is not, and is restated at a **month**: month 0 pays
    100,000 + 200.00 - 0.00 + 0.00 - 0.00 - 50.24 - 340.11 = 99,809.65, which is
    ``pols_if(1) x av_pp(1)``.  It closes in each of the 480 months, not just twelve
    times in twelve years.
    """
    p = fr_euro_anchor
    interest = sum(p.int_credited_pp(y) for y in range(12))
    levies = sum(p.soc_levy_pp(y) for y in range(12))
    credited = sum(p.pb_credited_pp(y) for y in range(12))
    fees = sum(p.fee_pp(y) for y in range(12))
    assert interest == pytest.approx(31800.82, abs=CENT)
    assert levies == pytest.approx(5469.74, abs=CENT)
    assert levies / interest == pytest.approx(0.172000, abs=1e-9)
    assert credited == pytest.approx(40538.97, abs=CENT)
    assert fees == pytest.approx(8738.15, abs=CENT)
    assert credited - fees == pytest.approx(interest, abs=1e-9)
    assert 100000.00 + 28800.00 - 21000.00 + interest - levies == pytest.approx(
        134131.08, abs=CENT)
    assert p.av_pp(opens(12)) == pytest.approx(134131.08, abs=CENT)
    assert p.pols_if(opens(1)) == pytest.approx(0.954240, abs=1e-6)
    # The month-0 roll-forward, term for term, at fund level.
    assert p.av(0) == pytest.approx(100000.00, abs=CENT)
    assert p.premiums(0) == pytest.approx(200.00, abs=CENT)
    assert p.claims(0, "DEATH") == pytest.approx(50.24, abs=CENT)
    assert p.claims(0, "LAPSE") == pytest.approx(340.11, abs=CENT)
    assert p.av(1) == pytest.approx(99809.65, abs=CENT)
    assert p.pols_if(1) * p.av_pp(1) == pytest.approx(99809.65, abs=CENT)
    assert p.check_av_roll_fwd() is True


def test_the_guarantee_floor_never_binds_on_this_path(fr_euro_anchor):
    """G = 100,000 + 28,800 - 21,000 - 8,738.15 = 99,061.85 against 139,600.82.

    Read at month 144, the twelfth anniversary, where the annual grid read it at year 12.
    Compared to the account **before** cumulative social levies, because the published
    minimum surrender-value tables are stated before social and tax levies.  The floor now
    steps down once a year, at the anniversary, and the check runs at every month.
    """
    p = fr_euro_anchor
    assert p.guarantee_form() == "net"
    assert p.guar_floor_pp(opens(12)) == pytest.approx(99061.85, abs=CENT)
    assert p.av_pp(opens(12)) + p.soc_levy_cum_pp(opens(12)) == pytest.approx(
        139600.82, abs=CENT)
    assert p.check_guar_floor() is True
    assert all(p.check_guar_floor_resid(t) == 0.0 for t in range(opens(12)))
    # The charge term steps once a year and nowhere else: the floor is flat through the
    # eleven months that follow an anniversary but for the instalments.
    for t in range(opens(3), anniv(3)):
        step = (p.guar_floor_pp(t + 1) - p.guar_floor_pp(t)
                - p.prem_to_av_mth_pp(t) + p.withdrawals_mth_pp(t))
        assert step == pytest.approx(0.0, abs=1e-9), t
    assert p.guar_floor_pp(anniv(3) + 1) - p.guar_floor_pp(anniv(3)) == pytest.approx(
        p.prem_to_av_mth_pp(anniv(3)) - p.withdrawals_mth_pp(anniv(3)) - p.fee_pp(3),
        abs=1e-9)


# ---------------------------------------------------------------------------
# Pitfalls 1 and 2: the charge and the crediting base


def test_the_management_charge_is_not_deducted_twice(fr_euro_anchor):
    """`ts_net` is already net of the charge; `av x (1 + ts_net) x (1 - c)` takes it twice."""
    p = fr_euro_anchor
    for y in (0, 5, 8, 11):
        t = anniv(y)
        assert p.pb_credited_pp(y) - p.fee_pp(y) == pytest.approx(
            p.int_credited_pp(y), abs=1e-9)
        assert p.av_pp_at(t, "AFT_INT") == pytest.approx(
            p.av_pp_at(t, "AFT_WD") + p.int_credited_pp(y), abs=1e-9)
        # What the double deduction would cost: 0.60% of the closing balance, every year.
        doubled = p.av_pp_at(t, "AFT_INT") * (1.0 - p.fee_rate())
        assert p.av_pp_at(t, "AFT_INT") - doubled == pytest.approx(
            p.fee_rate() * p.av_pp_at(t, "AFT_INT"), rel=1e-12)
        assert p.av_pp_at(t, "AFT_INT") - doubled > 600.0


def test_the_management_charge_lands_whole_at_the_anniversary(fr_euro_anchor):
    """The `frais de gestion` is levied at 31 December value date, not a twelfth a month.

    Its "pro rata temporis" is about the **base** - which :func:`pm_avg_pp` already
    carries - and not about the date, and it is never a cash flow: it is a credit to the
    `compte technique` and lives inside ``ts_net``.  The one place it is visible on the
    monthly grid is the `garantie nette` floor, which steps down once a year.  So there
    is no ``fee`` column and no monthly fee cells, and ``AFT_INT`` equals ``AFT_WD`` in
    the eleven months that carry no crediting.
    """
    p = fr_euro_anchor
    assert "fee" not in p.result_cf().columns
    assert "fee_mth_pp" not in p.cells
    for t in range(opens(4), anniv(4)):
        assert p.av_pp_at(t, "AFT_INT") == p.av_pp_at(t, "AFT_WD"), t
    assert p.av_pp_at(anniv(4), "AFT_INT") > p.av_pp_at(anniv(4), "AFT_WD")
    assert p.fee_pp(4) == pytest.approx(p.fee_rate() * p.pm_avg_pp(4), abs=1e-12)


def test_the_crediting_base_is_pro_rata_temporis(assurance_vie_euro, fr_euro_anchor):
    """B(y) = AV(12y) + 0.5 P(y) - 0.5 W(y), not the closing balance.

    On the monthly grid the 0.5 is **derived** rather than asserted: the year's amounts
    arrive in twelve equal instalments and each is weighted by ``prem_wt_mth(k)``, the
    fraction of the year still to run from the middle of month ``k``, and the twelve
    weighted twelfths sum to exactly one half.  The two neighbouring conventions do not -
    beginning-of-month gives 0.541667 and end-of-month 0.458333 - and either would move
    the anchor cell's first-year base by EUR 100.

    The base and the closing balance differ by exactly ``0.5 ts_net(y) (P(y) - W(y))`` -
    a full year's interest on a December payment - and coincide where nothing moves,
    which is the paid-up cell.
    """
    p = fr_euro_anchor
    assert sum(p.prem_wt_mth(k) for k in range(12)) == pytest.approx(6.0, abs=1e-12)
    assert sum(p.prem_wt_mth(k) / 12.0 for k in range(12)) == pytest.approx(
        0.5, abs=1e-12)
    assert sum((12 - k) / 12.0 / 12.0 for k in range(12)) == pytest.approx(
        0.541667, abs=1e-6)
    assert sum((11 - k) / 12.0 / 12.0 for k in range(12)) == pytest.approx(
        0.458333, abs=1e-6)
    for y in (0, 5, 11):
        assert p.pm_avg_pp(y) == pytest.approx(
            p.av_pp(opens(y)) + 0.5 * (p.prem_to_av_pp(y) - p.withdrawals_pp(y)),
            abs=1e-9)
        closing = p.av_pp(opens(y)) + p.prem_to_av_pp(y) - p.withdrawals_pp(y)
        assert closing - p.pm_avg_pp(y) == pytest.approx(
            0.5 * (p.prem_to_av_pp(y) - p.withdrawals_pp(y)), abs=1e-9)
        assert p.ts_net(y) * closing - p.int_credited_pp(y) == pytest.approx(
            0.5 * p.ts_net(y) * (p.prem_to_av_pp(y) - p.withdrawals_pp(y)), abs=1e-9)
    # EUR 100.00 on the base, EUR 2.79 on the year's interest, at y = 0.
    bom_base = p.av_pp(0) + sum((12 - k) / 12.0 * p.prem_to_av_mth_pp(k)
                                for k in range(12))
    assert bom_base - p.pm_avg_pp(0) == pytest.approx(100.00, abs=CENT)
    assert p.ts_net(0) * (bom_base - p.pm_avg_pp(0)) == pytest.approx(2.79, abs=CENT)
    paid_up = assurance_vie_euro.Projection[4]
    assert paid_up.prem_gross_pp(2) == 0.0 and paid_up.withdrawals_pp(2) == 0.0
    assert paid_up.pm_avg_pp(2) == pytest.approx(paid_up.av_pp(opens(2)), rel=1e-15)


def test_the_versement_and_the_rachat_are_collected_in_twelve_instalments(
        assurance_vie_euro, fr_euro_anchor):
    """Both are `programmes` and both carry a **monthly** contractual minimum.

    EUR 50 a month for a `versement libre programme` and EUR 150 a month for a `rachat
    partiel programme`, so a monthly grid that left them as annual lumps would be
    modelling a different contract.  Each month takes one twelfth, and the year's twelve
    instalments add back to the year's amount exactly - while the *fund-level* totals do
    not, because the instalments are paid by a block that decrements every month.
    """
    p = fr_euro_anchor
    for y in (0, 5, 20):
        months = range(opens(y), opens(y + 1))
        assert sum(p.prem_to_av_mth_pp(t) for t in months) == pytest.approx(
            p.prem_to_av_pp(y), abs=1e-9)
        assert sum(p.withdrawals_mth_pp(t) for t in months) == pytest.approx(
            p.withdrawals_pp(y), abs=1e-9)
        for t in months:
            assert p.prem_to_av_mth_pp(t) == pytest.approx(
                p.prem_to_av_pp(y) / 12.0, abs=1e-12)
            assert p.withdrawals_mth_pp(t) == pytest.approx(
                p.withdrawals_pp(y) / 12.0, abs=1e-12)
    assert p.prem_to_av_mth_pp(0) == pytest.approx(200.00, abs=CENT)   # >= EUR 50
    assert p.withdrawals_mth_pp(60) == pytest.approx(250.00, abs=CENT)  # >= EUR 150
    # The fund-level year totals fall, which is the whole point of collecting monthly.
    ann = p.result_cf_annual()
    assert ann.loc[0, "premiums"] < p.prem_to_av_pp(0) * p.pols_if(0)
    assert ann.loc[0, "premiums"] == pytest.approx(2349.24, abs=CENT)
    # A paid-up cell collects nothing in any month.
    paid_up = assurance_vie_euro.Projection[4]
    assert all(paid_up.prem_to_av_mth_pp(t) == 0.0 for t in range(24, 36))


def test_the_withdrawal_cap_is_struck_once_a_year_on_the_year_open_balance(
        assurance_vie_euro, fr_euro_anchor):
    """The cap is a physical constraint, and it is applied to the **year's** election.

    Capping each month against that month's balance would be more literal and would feed
    the balance back into the crediting base inside the year, for no benefit: the cap
    binds on no shipped model point on either grid.  So ``withdrawals_pp(y)`` is struck
    once, on ``av_pp(12y) + prem_to_av_pp(y)``, and the month takes a twelfth of the
    result.
    """
    p = fr_euro_anchor
    for y in (5, 10, 30):
        assert p.withdrawals_pp(y) == pytest.approx(
            min(p.wd_prog_pp(),
                max(0.0, p.av_pp(opens(y)) + p.prem_to_av_pp(y))), abs=1e-12)
    for point_id in assurance_vie_euro.Data.model_point_table().index:
        q = assurance_vie_euro.Projection[point_id]
        for y in range(PROJ_YEARS):
            if y >= q.wd_start_year():
                assert q.withdrawals_pp(y) == pytest.approx(
                    q.wd_prog_pp(), abs=1e-9), (point_id, y)


# ---------------------------------------------------------------------------
# Pitfalls 3 and 4: the statutory split


def test_the_eighty_five_percent_attaches_to_the_financial_account(fr_euro_anchor):
    """Not "90% of the financial account and 85% of the technical result".

    The popular form gives EUR 3,319.09 at ``y = 0`` against the correct EUR 3,071.86.
    """
    p = fr_euro_anchor
    for y in (0, 5, 11):
        ph_tech = p.tech_acct_pp(y) - p.insurer_tech_share_pp(y)
        assert p.pb_acct_pp(y) - ph_tech == pytest.approx(
            0.85 * p.fin_acct_pp(y), abs=1e-9)
    assert 0.90 * p.fin_acct_pp(0) + 0.85 * p.tech_acct_pp(0) == pytest.approx(
        3319.09, abs=CENT)
    assert p.pb_acct_pp(0) == pytest.approx(3071.86, abs=CENT)


def test_the_four_and_a_half_percent_of_premiums_limb_binds(
        assurance_vie_euro, fr_euro_anchor):
    """EUR 108.00 against EUR 28.43 for the 10% limb at ``y = 5``; nil on a paid-up cell.

    Two cells identical but for their premium stream credit different rates, which is the
    article working as written.  The limb is struck on the **annual** `versement`, which
    is why ``prem_gross_pp`` stays an annual amount on a monthly grid.
    """
    p = fr_euro_anchor
    assert p.insurer_tech_share_pp(5) == pytest.approx(108.00, abs=CENT)
    assert 0.10 * p.tech_acct_pp(5) == pytest.approx(28.43, abs=CENT)
    assert p.insurer_tech_share_pp(5) == pytest.approx(
        0.045 * p.prem_gross_pp(5), abs=1e-9)
    assert p.prem_gross_pp(5) == pytest.approx(
        12.0 * p.prem_to_av_mth_pp(opens(5)), abs=1e-9)   # nil entry charge here
    paid_up = assurance_vie_euro.Projection[4]
    assert paid_up.prem_gross_pp(2) == 0.0
    assert paid_up.insurer_tech_share_pp(2) == pytest.approx(
        0.10 * paid_up.tech_acct_pp(2), abs=1e-12)
    assert paid_up.ts_stat(0) > p.ts_stat(0)


# ---------------------------------------------------------------------------
# Pitfalls 5, 6 and 7: the PPB


def test_the_ppb_is_inside_the_financial_base_and_does_not_accrete(fr_euro_anchor):
    """Struck on ``pm_avg_pp + ppb_pp``; omitting it costs EUR 41.81 at ``y = 5``.

    The mirror error is accreting the vintages, which pays the PPB's own return twice.
    """
    p = fr_euro_anchor
    assert p.fin_acct_pp(5) == pytest.approx(
        p.r_fin(5) * (p.pm_avg_pp(5) + p.ppb_pp(5)), abs=1e-9)
    assert 0.85 * p.r_fin(5) * p.ppb_pp(5) == pytest.approx(41.81, abs=CENT)
    for y in range(11):
        for v in range(p.ppb_vintage_first(), y):
            assert p.ppb_vintage_pp(y + 1, v) == pytest.approx(
                p.ppb_vintage_pp(y, v) - p.ppb_vintage_release_pp(y, v), abs=1e-9)


def test_the_ppb_is_released_fifo_oldest_vintage_first(fr_euro_anchor):
    """The release of EUR 606.30 at ``y = 6`` clears the last EUR 500 vintage first.

    It then takes EUR 106.30 from the vintage carried in year -1, leaving EUR 393.70 to be
    forced out at ``y = 7`` - which the ``y = 7`` discretionary need of EUR 650.58 more
    than covers, so the PPB reaches zero exactly at the clock's last date.
    """
    p = fr_euro_anchor
    assert p.ppb_release_pp(6) == pytest.approx(606.30, abs=CENT)
    assert p.ppb_vintage_release_pp(6, -2) == pytest.approx(500.00, abs=CENT)
    assert p.ppb_vintage_release_pp(6, -1) == pytest.approx(106.30, abs=CENT)
    assert p.ppb_vintage_release_pp(6, 0) == 0.0
    assert p.ppb_vintage_pp(7, -2) == pytest.approx(0.0, abs=1e-9)
    assert p.ppb_vintage_pp(7, -1) == pytest.approx(393.70, abs=CENT)
    assert p.ppb_forced_pp(7) == pytest.approx(393.70, abs=CENT)
    assert p.ppb_release_pp(7) == pytest.approx(650.58, abs=CENT)
    assert p.ppb_pp(8) == pytest.approx(0.0, abs=CENT)


def test_the_vintage_ledger_table_in_model_md(fr_euro_anchor):
    """model.md's PPB ledger table, every cell of it.

    The table has an uncapped-want column and a capped-discretionary column because the
    two separate twice and for different reasons - a negative want at ``y = 0`` to
    ``y = 2``, which is what a dotation year is, and a binding balance from ``y = 7`` - and
    a release column because neither want column is the release wherever the clock outranks
    the target.  Nothing else in this module asserts the ``y = 8`` onward row, which is how
    a figure the model does not produce once stood in it.
    """
    p = fr_euro_anchor
    # y: (forced, want uncapped, discretionary, released)
    ledger = {
        0: (500.00, -137.06, 0.00, 500.00),
        1: (500.00, -87.30, 0.00, 500.00),
        2: (500.00, -32.52, 0.00, 500.00),
        3: (500.00, 77.81, 77.81, 500.00),
        4: (500.00, 248.81, 248.81, 500.00),
        5: (500.00, 426.99, 426.99, 500.00),
        6: (500.00, 606.30, 606.30, 606.30),
        7: (393.70, 736.57, 650.58, 650.58),
        8: (0.00, 869.58, 0.00, 0.00),
        9: (0.00, 931.98, 0.00, 0.00),
        10: (0.00, 995.17, 0.00, 0.00),
        11: (0.00, 1059.09, 0.00, 0.00),
    }
    for y, (forced, want, discr, released) in ledger.items():
        assert p.ppb_forced_pp(y) == pytest.approx(forced, abs=CENT), y
        assert p.pb_target_pp(y) - p.pb_min_pp(y) == pytest.approx(want, abs=CENT), y
        assert p.ppb_discr_rel_pp(y) == pytest.approx(discr, abs=CENT), y
        assert p.ppb_release_pp(y) == pytest.approx(released, abs=CENT), y
    # The want column is the dotation's mirror image while it is negative.
    for y in (0, 1, 2):
        assert p.ppb_dotation_pp(y) == pytest.approx(
            p.pb_min_pp(y) - p.pb_target_pp(y), abs=1e-9)
    # From ``y = 8`` the balance is nil, so the want rises and nothing is released.
    assert p.ppb_pp(8) == pytest.approx(0.0, abs=CENT)


def test_no_ppb_vintage_outlives_its_eight_year_clock(assurance_vie_euro):
    """Nothing survives the year after its deadline, and the ledger ties to the balance.

    A LIFO release satisfies the aggregate recursion exactly and breaches the clock
    invisibly, which is why the per-vintage ledger exists at all.  The sweep is over the
    forty financial **years**, not the 480 months: art. A132-16 counts financial years, so
    the ledger is a year-indexed statement and iterating months would cost twelve times as
    much for the same answer.
    """
    for point_id in assurance_vie_euro.Data.model_point_table().index:
        p = assurance_vie_euro.Projection[point_id]
        assert p.check_ppb_clock() is True, point_id
        assert p.check_ppb_roll_fwd() is True, point_id
        for y in range(p.proj_len() // 12):
            assert p.ppb_pp(y) >= -1e-9
            assert p.ppb_ledger_pp(y) == pytest.approx(p.ppb_pp(y), abs=1e-8)
            for v in range(p.ppb_vintage_first(), y - 8):
                assert p.ppb_vintage_pp(y, v) == pytest.approx(0.0, abs=1e-8)


def test_the_clock_reaches_dotation_vintages_and_a_young_profile_defers_it(
        assurance_vie_euro):
    """Point 8 credits a dotation every year and each comes back out at v + 8.

    Point 6 carries the same EUR 4,000 in four vintages rather than eight, due at ``y = 4``
    to ``y = 7``, so nothing is forced out before ``y = 4`` - which is why the vintage split
    is a **[std]** worth naming.
    """
    high = assurance_vie_euro.Projection[8]
    assert high.scenario_id() == "high"
    assert all(high.ppb_dotation_pp(y) > 0.0 for y in range(12))
    for y in range(8, 14):
        assert high.ppb_forced_pp(y) == pytest.approx(
            high.ppb_dotation_pp(y - 8), abs=CENT)
    assert high.ppb_pp(40) > 0.0     # a growing PPB, and still no vintage overdue
    young = assurance_vie_euro.Projection[6]
    assert young.ppb_vintages_init() == 4 and young.ppb_vintage_first() == -4
    assert young.ppb_vintage_pp(0, -4) == pytest.approx(1000.00, abs=CENT)
    assert all(young.ppb_forced_pp(y) == 0.0 for y in range(4))
    assert young.ppb_forced_pp(4) > 0.0
    assert young.ts_net(0) == pytest.approx(young.ts_target(), abs=1e-12)


def test_the_statutory_minimum_is_allocated_in_full_not_credited_in_full(
        assurance_vie_euro, fr_euro_anchor):
    """A dotation year credits *less* than ts_stat, and that is legal.

    The balance goes to the PPB, not to the insurer, so the invariant is an allocation
    identity rather than a rate inequality.  Model point 5 opens with no PPB and credits
    below the statutory floor rate at ``y = 0``; the anchor cell never does, only because
    its forced release always exceeds its dotation.
    """
    p = fr_euro_anchor
    assert p.check_pb_allocation() is True
    for y in (0, 5, 8):
        assert p.check_pb_allocation_resid(y) == pytest.approx(0.0, abs=1e-7)
        assert p.int_credited_pp(y) + p.fee_pp(y) + p.ppb_dotation_pp(y) == pytest.approx(
            p.pb_min_pp(y) + p.ppb_release_pp(y) + p.insurer_topup_pp(y), abs=1e-7)
    no_ppb = assurance_vie_euro.Projection[5]
    assert no_ppb.ppb_pp(0) == 0.0 and no_ppb.ppb_dotation_pp(0) > 0.0
    assert no_ppb.ts_net(0) < no_ppb.ts_stat(0)
    assert no_ppb.ts_net(0) == pytest.approx(no_ppb.ts_target(), abs=1e-12)
    assert no_ppb.check_pb_allocation() is True


# ---------------------------------------------------------------------------
# Pitfalls 8 and 9: the prelevements sociaux


def test_the_social_levy_is_annual_not_deferred_to_surrender(fr_euro_anchor):
    """17.2% every year on euro-denominated rights, inside the account and outside net_cf.

    Deferring it to `denouement` is right for the UC compartment and wrong here, and it
    overstates the account and every benefit measured on it.  On the monthly grid the
    annual timing is a **visible** property rather than an implicit one: art. L136-7 II
    charges the products "lors de leur inscription au bon ou contrat", the inscription is
    the 31 December crediting, and so ``soc_levy_mth_pp`` is nil in eleven months of
    twelve and positive in the twelfth.
    """
    p = fr_euro_anchor
    for y in range(12):
        assert p.soc_levy_pp(y) > 0.0
        assert p.soc_levy_pp(y) == pytest.approx(
            p.soc_levy_rate() * max(p.int_credited_pp(y), 0.0), abs=1e-12)
        for t in range(opens(y), anniv(y)):
            assert p.soc_levy_mth_pp(t) == 0.0, t
            assert p.int_credited_mth_pp(t) == 0.0, t
        assert p.soc_levy_mth_pp(anniv(y)) > 0.0
        assert p.soc_levy_mth_pp(anniv(y)) == pytest.approx(
            p.soc_levy_pp(y), abs=1e-12)
        assert p.int_credited_mth_pp(anniv(y)) == pytest.approx(
            p.int_credited_pp(y), abs=1e-12)
    total_levy = sum(p.soc_levy_pp(y) for y in range(12))
    total_int = sum(p.int_credited_pp(y) for y in range(12))
    assert total_levy == pytest.approx(0.172 * total_int, abs=1e-9)
    assert p.av_pp(opens(1)) == pytest.approx(
        p.av_pp_at(anniv(0), "AFT_INT") - p.soc_levy_mth_pp(anniv(0)), abs=1e-12)
    df = p.result_cf()
    outgo = df[["claims_death", "claims_lapse", "withdrawals", "expenses"]].sum(axis=1)
    assert (outgo - df["premiums"] - df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    assert df["soc_levy"].sum() > 0.0
    assert (df["soc_levy"] == 0.0).sum() == PROJ_LEN - PROJ_YEARS


def test_the_social_levy_base_is_the_years_interest_not_the_account(fr_euro_anchor):
    """17.2% of EUR 100,000 is EUR 17,200; of ``y = 0``'s EUR 2,827.60 it is EUR 486.35."""
    p = fr_euro_anchor
    assert 0.172 * p.av_pp(0) == pytest.approx(17200.00, abs=CENT)
    assert p.soc_levy_pp(0) == pytest.approx(486.35, abs=CENT)
    assert p.int_credited_pp(0) == pytest.approx(2827.60, abs=CENT)
    assert p.soc_levy_cum_pp(0) == 0.0
    assert p.soc_levy_cum_pp(opens(12)) == pytest.approx(5469.74, abs=CENT)


# ---------------------------------------------------------------------------
# Pitfalls 10, 11 and 12: the cliquet, the death benefit and mid-year exits


def test_the_cliquet_ratchets_credited_pb_not_the_account_balance(
        assurance_vie_euro, fr_euro_anchor):
    """Credited PB is definitively acquired; the balance is not.

    Model point 10, a drawdown cell, falls every year from ``y = 3`` - and, on the monthly
    grid, every *month* from then on - while its ratchet holds throughout.  Testing the
    cliquet as "``av_pp`` never falls" is the pitfall.
    """
    p = fr_euro_anchor
    assert p.check_cliquet() is True and p.pb_cum_pp(0) == 0.0
    for y in range(12):
        assert p.int_credited_pp(y) >= 0.0
        assert p.ts_net(y) >= p.tmg_rate()
        assert p.pb_cum_pp(opens(y + 1)) == pytest.approx(
            p.pb_cum_pp(opens(y)) + p.pb_credited_pp(y), abs=1e-9)
        # The ledger steps once a year, in the month after the 31 December that credited.
        for t in range(opens(y) + 1, anniv(y) + 1):
            assert p.pb_cum_pp(t) == pytest.approx(p.pb_cum_pp(opens(y)), abs=1e-9), t
    drawdown = assurance_vie_euro.Projection[10]
    assert drawdown.av_pp(opens(4)) < drawdown.av_pp(opens(3))
    assert all(drawdown.av_pp(t + 1) < drawdown.av_pp(t)
               for t in range(opens(4), opens(5) - 1))
    assert drawdown.check_cliquet() is True
    assert drawdown.pb_cum_pp(opens(19)) > drawdown.pb_cum_pp(opens(9))


def test_the_death_benefit_is_the_account_value_with_no_uplift(fr_euro_anchor):
    """DB = CV = av_pp(t+1), no uplift and no surrender penalty; and no maturity kind.

    The identity holds in **every** month, anniversary or not, which is what makes the
    claim the balance its own month closes on.
    """
    p = fr_euro_anchor
    for t in (0, 11, 64, anniv(5), 143, 359):
        assert p.db_pp(t) == pytest.approx(p.av_pp(t + 1), rel=1e-15)
        assert p.cv_pp(t) == pytest.approx(p.av_pp(t + 1), rel=1e-15)
        assert p.claim_pp(t, "DEATH") == pytest.approx(p.claim_pp(t, "LAPSE"), rel=1e-15)
    with pytest.raises(FormulaError):
        p.claim_pp(0, "MATURITY")
    assert "claims_maturity" not in p.result_cf().columns


def test_mid_year_exits_take_no_in_year_revalorisation(fr_euro_anchor):
    """The contractual rule, which the monthly grid makes implementable.

    A `denouement` in a non-anniversary month is paid the `epargne acquise` with the
    year's revalorisation accrued only at the announced floor rate `pro rata temporis` -
    which at ``tmg_rate() = 0``, the value every shipped model point carries, is nil.  So
    the claim is exactly ``av_pp_at(t, "AFT_WD")``, the balance after that month's
    instalments and nothing else.

    In the anniversary month the whole year's `taux servi` net of the levy is there, as it
    was on the annual grid.  The annual-step model this replaced gave *every* exit that
    full year's credit, because the exit and the crediting were the same instant; the
    notes listed it as a pitfall, a sensitivity and an out-of-scope item, and the finer
    grid retires all three.
    """
    p = fr_euro_anchor
    assert p.tmg_rate() == 0.0
    for t in (0, 5, 64, 70, 130, 300):
        assert p.is_anniv(t) is False
        assert p.claim_pp(t, "LAPSE") == pytest.approx(
            p.av_pp_at(t, "AFT_WD"), rel=1e-15)
        assert p.claim_pp(t, "DEATH") == pytest.approx(
            p.av_pp_at(t, "AFT_WD"), rel=1e-15)
    for y in (0, 5, 11):
        t = anniv(y)
        assert p.claim_pp(t, "LAPSE") - p.av_pp_at(t, "AFT_WD") == pytest.approx(
            p.int_credited_pp(y) - p.soc_levy_pp(y), abs=1e-9)
        assert p.claim_pp(t, "LAPSE") > p.av_pp_at(t, "AFT_WD")
    # Deaths then surrenders, on the monthly rates, at the end of every month.
    assert p.pols_if_at(65, "AFT_DECR") == pytest.approx(
        p.pols_if(65) * (1 - p.mort_rate_mth(65)) * (1 - p.lapse_rate_mth(65)),
        abs=1e-12)


# ---------------------------------------------------------------------------
# The monthly grid itself


def test_monthly_rates_compound_back_to_the_annual_ones(assurance_vie_euro,
                                                        fr_euro_anchor):
    """q_m and w_m are the constant-force conversion of the annual rates the notes give.

    This is what makes the two grids reconcile at anniversaries, so it is asserted
    directly rather than only through its consequence.  There is no linearity to assert:
    ``1 - (1 - q)^(1/12)`` is not ``q / 12``, and the only safe monotonic statement is
    that the monthly rate is the smaller.
    """
    p = fr_euro_anchor
    for t in (0, 13, 100, 125, 400):
        assert 1 - (1 - p.mort_rate_mth(t)) ** 12 == pytest.approx(
            p.mort_rate(t), rel=1e-12)
        assert 1 - (1 - p.lapse_rate_mth(t)) ** 12 == pytest.approx(
            p.lapse_rate(t), rel=1e-12)
        assert p.mort_rate_mth(t) < p.mort_rate(t)
        assert p.lapse_rate_mth(t) < p.lapse_rate(t)
    # The annual rates are properties of the policy year and do not move inside it.
    for y in (2, 7, 19):
        assert len({p.mort_rate(t) for t in range(opens(y), opens(y + 1))}) == 1
        assert len({p.lapse_rate(t) for t in range(opens(y), opens(y + 1))}) == 1
    for point_id in assurance_vie_euro.Data.model_point_table().index:
        assert assurance_vie_euro.Projection[point_id].check_decrements_compound() is True


def test_in_force_at_every_anniversary_matches_the_annual_recursion(assurance_vie_euro):
    """pols_if(12k) is exactly what an annual step would carry, over the whole frame.

    The annual recursion is written out here from the model's own annual vectors rather
    than taken from a fixture, so this asserts the equivalence and not a memory of it.
    It is the single most important consequence of the conversion, and it holds on every
    shipped model point.
    """
    for point_id in assurance_vie_euro.Data.model_point_table().index:
        p = assurance_vie_euro.Projection[point_id]
        expected = p.pols_if_init()
        for y in range(PROJ_YEARS):
            t = opens(y)
            assert p.pols_if(t) == pytest.approx(expected, rel=1e-12), (point_id, y)
            expected *= (1 - p.mort_rate(t)) * (1 - p.lapse_rate(t))


def test_the_annual_layer_is_keyed_by_the_projection_year(fr_euro_anchor):
    """A financial-year statement takes ``y``; a month takes ``t``; a rate takes ``t``.

    The mixed convention is deliberate.  Art. A132-11 builds one participation account per
    financial year and art. A132-16 counts financial years, so restating that machinery at
    480 months would carry two clocks in one signature and multiply the per-vintage FIFO
    ledger's cost by twelve for no new information.  The decrement rates keep the month
    argument and return the year's rate, which is the library-wide convention.
    """
    import inspect

    p = fr_euro_anchor
    by_year = ("r_fin", "ref_rate", "prem_gross_pp", "prem_to_av_pp", "withdrawals_pp",
               "pm_avg_pp", "fee_pp", "inflation_factor", "expenses_pp", "fin_acct_pp",
               "tech_acct_pp", "insurer_tech_share_pp", "pb_acct_pp", "pb_min_pp",
               "ts_stat", "pb_target_pp", "ppb_pp", "ppb_ledger_pp", "ppb_dotation_pp",
               "ppb_discr_rel_pp", "ppb_forced_pp", "ppb_release_pp", "pb_credited_pp",
               "ts_raw", "ts_net", "insurer_topup_pp", "int_credited_pp", "soc_levy_pp")
    by_month = ("av_pp", "guar_floor_pp", "soc_levy_cum_pp", "pb_cum_pp", "pols_if",
                "pols_death", "pols_lapse", "db_pp", "cv_pp", "premiums", "withdrawals",
                "expenses", "int_credited", "soc_levy", "liability_cf", "net_cf",
                "prem_to_av_mth_pp", "withdrawals_mth_pp", "expenses_mth_pp",
                "int_credited_mth_pp", "soc_levy_mth_pp", "proj_year", "duration",
                "duration_mth", "is_anniv", "age", "policy_year",
                "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
                "lapse_rate_base", "lapse_dyn_add")

    def params(name):
        return list(inspect.signature(p.cells[name].formula.func).parameters)

    for name in by_year:
        assert params(name) == ["y"], name
    for name in by_month:
        assert params(name) == ["t"], name
    assert params("ppb_vintage_pp") == ["y", "v"]
    assert params("ppb_vintage_release_pp") == ["y", "v"]
    # result_pb() stays a financial-year statement: proj_years rows, indexed by y.
    pb = p.result_pb()
    assert pb.index.name == "y"
    assert list(pb.index) == list(range(PROJ_YEARS))
    assert pb.loc[0, "av_pp"] == pytest.approx(p.av_pp(0), rel=1e-15)
    assert pb.loc[5, "av_pp"] == pytest.approx(p.av_pp(opens(5)), rel=1e-15)
    assert pb.loc[5, "guar_floor_pp"] == pytest.approx(
        p.guar_floor_pp(opens(5)), rel=1e-15)
    assert pb.loc[0, "ppb_pp"] == pytest.approx(p.ppb_pp(1), rel=1e-15)


def test_result_cf_annual_is_the_monthly_frame_regrouped(fr_euro_anchor):
    """Every flow column is the sum of its twelve months; pols_if is the year's opening.

    Not a second projection - the frame regrouped, which is what lets the annual-step
    model this replaced be laid beside it.
    """
    p = fr_euro_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert ann.index.name == "y"
    assert list(ann.index) == list(range(PROJ_YEARS))
    assert list(ann.columns) == list(df.columns)
    for y in (0, 5, 11, 39):
        rows = df.loc[opens(y):anniv(y)]
        assert len(rows) == 12
        assert ann.loc[y, "pols_if"] == p.pols_if(opens(y))
        for col in df.columns:
            if col != "pols_if":
                assert ann.loc[y, col] == pytest.approx(rows[col].sum(), rel=1e-12), col
    # The state column is the one the two grids still agree on; the flows are not.
    assert ann["premiums"].sum() == pytest.approx(30060.87, abs=CENT)
    assert ann["expenses"].sum() == pytest.approx(5886.79, abs=CENT)
    assert ann["liability_cf"].sum() == pytest.approx(130122.44, abs=CENT)


def test_the_expense_accrues_monthly_and_inflates_annually(fr_euro_anchor):
    """One twelfth a month, on the in force of that month; the factor steps on the year.

    The **amount** entering the `compte technique` stays the year's total, so the `taux
    servi` does not move; what changes is who bears it.  The inflation factor steps at the
    anniversary rather than continuously, which is this library's house rule and what
    keeps ``expenses_pp(y)`` equal to the annual-step model's.
    """
    p = fr_euro_anchor
    for y in (0, 3, 20):
        assert p.inflation_factor(y) == pytest.approx(1.015 ** y, rel=1e-12)
        months = range(opens(y), opens(y + 1))
        for t in months:
            assert p.expenses_mth_pp(t) == pytest.approx(
                p.expenses_pp(y) / 12.0, abs=1e-12)
        assert sum(p.expenses_mth_pp(t) for t in months) == pytest.approx(
            p.expenses_pp(y), abs=1e-9)
        # The technical account sees the year, not the month.
        assert p.tech_acct_pp(y) == pytest.approx(
            p.fee_pp(y) - p.expenses_pp(y), abs=1e-12)
    # A decrementing block carries less than the annual grid charged it.
    ann = p.result_cf_annual()
    assert ann.loc[0, "expenses"] < p.expenses_pp(0) * p.pols_if(0)
    assert ann.loc[0, "expenses"] == pytest.approx(370.20, abs=CENT)


# ---------------------------------------------------------------------------
# Behaviour


def test_the_duration_eight_surrender_step_is_the_tax_threshold(fr_euro_anchor):
    """Keyed to the **contract's** eighth anniversary, not to the eighth projected month.

    The anchor cell is five years in, so policy year 8 is the twelve months t = 24 to 35.
    A model reading the lapse table at ``t`` rather than at ``t // 12`` would put the step
    in the third *month*, which is the likeliest indexing error this grid can make; the
    width of the step is what catches it.
    """
    p = fr_euro_anchor
    assert p.duration_init() == 5
    assert [p.policy_year(t) for t in (0, 24, 60)] == [6, 8, 11]
    assert [p.duration(t) for t in (0, 11, 12, 24)] == [5, 5, 6, 7]
    assert [p.age(t) for t in (0, 11, 12, 23)] == [60, 60, 61, 61]
    assert p.lapse_rate_base(24) == pytest.approx(0.08, abs=1e-12)
    assert p.lapse_rate_base(12) == pytest.approx(0.04, abs=1e-12)
    assert p.lapse_rate_base(36) == pytest.approx(0.05, abs=1e-12)
    # Twelve months wide, and landing on the year.
    for t in range(24, 36):
        assert p.lapse_rate_base(t) == pytest.approx(0.08, abs=1e-12), t
    assert p.lapse_rate_base(23) != pytest.approx(0.08, abs=1e-12)
    assert p.lapse_rate_base(36) != pytest.approx(0.08, abs=1e-12)
    assert p.ref_rate(0) == pytest.approx(0.0220, abs=1e-12)


def test_the_dynamic_surrender_term_is_one_sided(assurance_vie_euro, fr_euro_anchor):
    """Additive in the gap, and nil while the `taux servi` beats the reference rate.

    The gap is read once a year, at ``proj_year(t)``, so the addition is one number for
    the whole policy year and only ``lapse_rate_mth`` moves inside it.
    """
    p = fr_euro_anchor
    for y in range(8):
        assert p.ts_net(y) > p.ref_rate(y)
        assert p.lapse_dyn_add(opens(y)) == 0.0
        assert p.lapse_rate(opens(y)) == pytest.approx(
            p.lapse_rate_base(opens(y)), abs=1e-12)
    assert p.lapse_dyn_add(opens(8)) == pytest.approx(
        4.0 * (p.ref_rate(8) - p.ts_net(8) - 0.0025), abs=1e-12)
    assert p.lapse_rate(opens(8)) == pytest.approx(0.062873, abs=RATE)
    assert len({p.lapse_dyn_add(t) for t in range(opens(8), opens(9))}) == 1
    # A 0.73% taux servi against a 2.20% Livret A adds 4.88 points to a 5% base rate.
    low = assurance_vie_euro.Projection[7]
    assert low.scenario_id() == "low" and low.ts_net(19) < low.ref_rate(19)
    assert low.lapse_dyn_add(opens(19)) == pytest.approx(0.048755, abs=RATE)
    assert low.lapse_rate(opens(19)) == pytest.approx(0.098755, abs=RATE)


def test_the_dynamic_surrender_cap_binds_when_the_gap_is_wide():
    """The cap has no public calibration and never binds on the shipped scenarios.

    Raising the coefficient on a throwaway instance is the only way to see it, and seeing
    it is the point: a mass-lapse run here is a pre-management-action number in any case.
    """
    model = mx.read_model(MODEL_DIR, name="Euro_FR_S_cap")
    try:
        assert model.Projection.lapse_cap == 0.3
        model.Projection.lapse_dyn_a = 60.0
        model.Projection.clear_all()
        p = model.Projection[7]
        assert p.lapse_dyn_add(opens(19)) > 0.3
        assert p.lapse_rate(opens(19)) == pytest.approx(0.3, abs=1e-12)
        assert p.lapse_rate_mth(opens(19)) == pytest.approx(
            1 - 0.7 ** (1 / 12), abs=1e-12)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The variants the shipped model points carry


def test_the_shipped_variants_behave_as_their_columns_say(assurance_vie_euro):
    """Points 2, 3, 9 and 11 against the anchor cell.

    The `garantie brute` (2) leaves the account path untouched and lifts only the floor, by
    the cumulative charge.  A 2.90% target (3) drains the PPB by ``y = 6`` and then credits
    the statutory floor rate.  The small new-business cell (9) carries a 0.50% entry charge and
    a 0.80% management charge, and the fixed part of its expense loading dominates its
    `compte technique`.  The grouped cell (11) scales every flow by 250 and no state at all.
    """
    anchor = assurance_vie_euro.Projection[1]

    gross = assurance_vie_euro.Projection[2]
    assert gross.guarantee_form() == "gross" and anchor.guarantee_form() == "net"
    assert gross.av_pp(opens(12)) == pytest.approx(anchor.av_pp(opens(12)), rel=1e-15)
    assert gross.guar_floor_pp(opens(12)) == pytest.approx(
        anchor.guar_floor_pp(opens(12)) + 8738.15, abs=CENT)
    assert gross.guar_floor_pp(opens(12)) == pytest.approx(107800.00, abs=CENT)

    eager = assurance_vie_euro.Projection[3]
    assert eager.ts_target() == pytest.approx(0.0290, abs=1e-12)
    assert eager.ppb_pp(4) < anchor.ppb_pp(4)
    assert eager.ppb_pp(6) == pytest.approx(0.0, abs=CENT)
    assert eager.ts_net(9) == pytest.approx(eager.ts_stat(9), abs=1e-12)

    small = assurance_vie_euro.Projection[9]
    assert small.prem_charge_rate() == pytest.approx(0.005, abs=1e-12)
    assert small.prem_to_av_pp(0) == pytest.approx(1200.0 * 0.995, abs=1e-9)
    assert small.prem_to_av_mth_pp(0) == pytest.approx(1200.0 * 0.995 / 12, abs=1e-9)
    assert small.duration_init() == 0 and small.age(0) == 45
    assert small.lapse_rate_base(opens(7)) == pytest.approx(0.08, abs=1e-12)
    assert small.ts_stat(0) < anchor.ts_stat(0)

    grouped = assurance_vie_euro.Projection[11]
    assert grouped.pols_if_init() == 250.0
    for y in (0, 8, 19):
        assert grouped.av_pp(opens(y)) == pytest.approx(anchor.av_pp(opens(y)), rel=1e-15)
        assert grouped.ts_net(y) == pytest.approx(anchor.ts_net(y), rel=1e-15)
    for t in (0, 100, 237):
        assert grouped.net_cf(t) == pytest.approx(250.0 * anchor.net_cf(t), rel=1e-9)


def test_no_model_point_elects_an_avance_or_carries_a_positive_tmg(assurance_vie_euro):
    """Both are unpublished in the source set, so both are validated rather than guessed.

    At ``tmg_rate() = 0`` the two things the notes call the TMG coincide: the art. A132-12
    subtraction of interest already credited, which belongs to a `taux technique` fixed at
    subscription, and the floor on the year's total revalorisation.  Above zero they are
    different quantities and a cell would have to choose, so none is shipped - and on a
    monthly grid a positive TMG would also have to be accrued inside the year and squared
    up at 31 December, which no shipped cells does.
    """
    table = assurance_vie_euro.Data.model_point_table()
    assert (table["avance_on"] == 0).all() and (table["tmg_rate"] == 0.0).all()
    assert assurance_vie_euro.Projection[1].avance_on() is False
    for point_id in table.index:
        p = assurance_vie_euro.Projection[point_id]
        assert p.pb_min_pp(2) == pytest.approx(max(0.0, p.pb_acct_pp(2)), abs=1e-12)
        assert all(p.insurer_topup_pp(y) == 0.0 for y in (0, 9, 29))
        assert all(p.ts_net(y) == p.ts_raw(y) for y in (0, 9, 29))


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_both_signs_of_the_net_flow(fr_euro_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign.

    The frame is 480 **months** and opens at the valuation date: this model carries
    elapsed policy time in ``duration_init`` and never in the index, so ``t_first`` is 0
    on every model point.  ``int_credited`` and ``soc_levy`` are published beside the flows
    and in neither: a state movement and a policyholder tax.  No subtotal is published
    beside its parts, and the enum accessors validate rather than propagating a typo into
    a lookup.
    """
    df = fr_euro_anchor.result_cf()
    assert fr_euro_anchor.proj_len() == PROJ_LEN == 12 * PROJ_YEARS
    assert list(df.index) == list(range(fr_euro_anchor.proj_len()))
    assert list(df.index) == list(range(480)) and df.index.name == "t"
    assert fr_euro_anchor.pols_if(0) == fr_euro_anchor.pols_if_init()
    assert list(df.columns) == [
        "pols_if", "premiums", "withdrawals", "claims_death", "claims_lapse",
        "expenses", "int_credited", "soc_levy", "liability_cf", "net_cf",
    ]
    for absent in ("claims", "claims_surr", "claims_wd", "claims_maturity"):
        assert absent not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    with pytest.raises(FormulaError):
        fr_euro_anchor.av_pp_at(0, "AFT_LEVY")
    with pytest.raises(FormulaError):
        fr_euro_anchor.pols_if_at(0, "AFT_SURR")


def test_every_model_point_projects_and_every_check_holds(assurance_vie_euro):
    """The whole shipped table, and all eight invariants on each of its eleven rows."""
    ids = list(assurance_vie_euro.Data.model_point_table().index)
    assert len(ids) == 11
    columns = None
    for point_id in ids:
        p = assurance_vie_euro.Projection[point_id]
        df = p.result_cf()
        assert len(df) == 480 == p.proj_len() and df.notna().all().all(), point_id
        assert list(df.index) == list(range(480)), point_id
        assert len(p.result_cf_annual()) == 40, point_id
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns, point_id
        for name in CHECKS:
            value = getattr(p, name)()
            assert isinstance(value, bool), (point_id, name)
            assert value is True, (point_id, name)


def test_docstrings_carry_their_reference_material(assurance_vie_euro):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = assurance_vie_euro.doc
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "eight-year clock", "effet cliquet", "Prélèvements sociaux",
                   "Monthly steps", "policy **months**", "1 − (1 − r)^(1/12)"):
        assert phrase in doc
    assert "Annual steps" not in doc
    proj = assurance_vie_euro.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "av_pp_at", "ppb_vintage_pp",
                  "pm_avg_pp", "ts_net", "insurer_topup_pp", "lapse_dyn_add",
                  "proj_year", "duration", "duration_mth", "is_anniv",
                  "mort_rate_mth", "lapse_rate_mth", "prem_wt_mth",
                  "prem_to_av_mth_pp", "withdrawals_mth_pp", "expenses_mth_pp",
                  "int_credited_mth_pp", "soc_levy_mth_pp", "result_cf_annual"):
        assert cells in proj
    # The grid, the two clocks and the three decisions the grid forced, all in the Space
    # docstring rather than only in the notes.
    for phrase in ("policy months", "1 - (1 - r)^(1/12)",
                   "financial-year account", "no in-year revalorisation",
                   "(11.5 - k) / 12", "Afer reading"):
        assert phrase in proj
    data = assurance_vie_euro.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "fin_rate_table"):
        assert cells in data


def test_the_inputs_live_beside_the_model_and_mark_their_own_provenance():
    """Four external CSVs, none inside the model folder, each saying what it is.

    The statutory tables annexed to the arrêté du 1er août 2006 are cited in the documents
    and not redistributed here, so the shipped mortality table is INSEE-shaped and anchored
    so that ``mort_be_factor`` reproduces the notes' ``q = 0.0060`` at male age 60.
    """
    import pandas as pd

    assert {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
            "fin_rate_table.csv"} == {p.name for p in MODEL_DIR.parent.iterdir()
                                      if p.suffix == ".csv"}
    assert not list(MODEL_DIR.rglob("*.csv"))
    assert {p.name for p in MODEL_DIR.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}
    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert set(mort["provenance"]) == {"[std] INSEE-shaped French population proxy"}
    assert mort["mort_rate"].max() <= 1.0
    q60 = mort[(mort["sex"] == "M") & (mort["age"] == 60)]["mort_rate"].iloc[0]
    assert q60 == pytest.approx(0.0075, rel=1e-12)
    assert 0.80 * q60 == pytest.approx(0.0060, rel=1e-12)
    assert mort[(mort["sex"] == "F") & (mort["age"] == 120)]["mort_rate"].iloc[0] == 1.0
    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv")
    assert all(v.startswith("[std]") for v in lapse["provenance"])
    assert lapse[lapse["policy_duration"] == 8]["lapse_rate_base"].iloc[0] == 0.08
    fin = pd.read_csv(MODEL_DIR.parent / "fin_rate_table.csv")
    assert all(v.startswith("[std]") for v in fin["provenance"])
    assert set(fin["scenario_id"]) == {"base", "low", "high"}
    assert (fin["ref_rate"] == 0.0220).all()
    # The key is `y`, the model's own 0-based projection YEAR, and not `t`, which on this
    # model is a policy month: the scenario path is annual and is read at proj_year(t).
    assert "t" not in fin.columns
    for scenario in ("base", "low", "high"):
        assert list(fin[fin["scenario_id"] == scenario]["y"]) == list(range(40))


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a permitted TGH05/TGF05 basis."""
    import pandas as pd

    lighter = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col=["sex", "age"])
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5
    model = mx.read_model(MODEL_DIR, name="Euro_FR_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_death"].sum()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Lighter mortality means fewer deaths and later releases of the account.
            assert model.Projection[1].result_cf()["claims_death"].sum() < base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="Euro_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Euro_FR_S_rt")
    try:
        p = reread.Projection[1]
        for y, row in TABLE_2.items():
            assert p.av_pp(opens(y)) == pytest.approx(row[0], abs=CENT)
            assert p.int_credited_pp(y) == pytest.approx(row[3], abs=CENT)
            assert p.soc_levy_pp(y) == pytest.approx(row[4], abs=CENT)
        assert p.ppb_pp(8) == pytest.approx(0.0, abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
