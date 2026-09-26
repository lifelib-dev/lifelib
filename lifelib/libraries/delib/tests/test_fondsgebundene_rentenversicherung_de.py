"""Golden and structural tests for FRV_DE_S.

The golden values are the worked example in
products/fondsgebundene_rentenversicherung/technical-notes.md ("Worked example"), which is
a **configuration** rather than a scenario: a *fondsgebundene Rentenversicherung* -- the
German unit-linked deferred private annuity, Schicht 3, single life, one fund, no
*Beitragsgarantie* -- sold to a man aged 37 last birthday, new business so
``duration_init_m = 0`` and ``proj_start() = 0``, with a level recurring *Beitrag* of
200,00 EUR a month for 30 years and *Rentenbeginn* at 67, so ``proj_len() = 360`` months
and the frame is ``t = 0 ... 359``.  ``t`` is the **0-based** policy month counted from
inception, ``t = 0`` being the inception month, and ``proj_len()`` is the month **count**
-- the frame's exclusive end.  The
*Beitragssumme* is 200.00 x 12 x 30 = 72 000,00 EUR, the acquisition charge is 2.50 % of it
-- the *Höchstzillmersatz* -- spread over sixty monthly instalments of 30,00 EUR, so the
*Anlagebeitrag* is 162,00 EUR while the instalment runs and 192,00 EUR from ``t = 60``.  The
death benefit is the *Beitragsrückgewähr* ``max(Fondsguthaben, Summe der gezahlten
Beiträge)``; the charge scale is ``std_gross`` (beta 4.00 % of each *Beitrag*, gamma
0.30 % p.a. of the fund taken as 0.30 %/12 a month, *Stückkosten* 3,00 EUR a month, no
*Stornoabzug*); the fund is ``base``, 5.00 % p.a. gross less a 0.45 % TER, so 0,371482 % a
month; the factors are ``std_2026``, guaranteed and current both 25.00 at age 67.  No
*Zuzahlung*, no *Teilentnahme*, no *Beitragsdynamik*, no *Ablaufmanagement*, no behaviour
module.

360 months is too long to assert row by row, so this module asserts the seventeen the notes
print -- the first six, ``t = 11`` and ``23``, the acquisition cliff at 58 to 60, 119, 239,
the tax-threshold step at 299 to 300 and the last two -- together with **every column total at
full precision**, where a slice of rows cannot hide an error.  Goldens are hard-coded
rather than pickled so a reviewer can compare them with the notes by eye, and tolerances
follow the precision the notes display: money to the cent, ``pols_if`` to six decimals.

Beyond the worked example: the notes' three independent rebuilds (``t = 0`` from the tariff
alone, ``t = 60`` at the cliff, the reduction in yield read as a savings account); the four
closure identities it prints; the *Einmalbeitrag* variant and the four-tariff
reduction-in-yield comparison; the seven ``check_*()`` identities and their residuals,
``check_net_cf()`` among them -- delib's first ruling; **one test per numbered modeling
pitfall in the technical notes**, eighteen of them, each named for the pitfall it guards;
and the product's own invariants.  There is deliberately **no sweep of the whole model
point table**: the conventions suite owns the single sweep, because a model point's first
evaluation is the most expensive thing in the run.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if and unit counts displayed to 6 d.p.
EIGHT_DP = 5e-9       # decrement rates displayed to 8 d.p.

MODEL_DIR = LIB / MODELS["FRV_DE_S"][0]
INPUT_DIR = MODEL_DIR.parent

CSV_FILES = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
             "charge_table.csv", "fund_scenario_table.csv", "rentenfaktor_table.csv"}

CHECKS = ("check_net_cf", "check_prem_split", "check_units_roll_fwd", "check_av_roll_fwd",
          "check_benefit_funding", "check_pols_roll_fwd", "check_acq_charge")


def _names(model):
    """Every cells and reference name published by ``Projection``."""
    return set(model.Projection.cells) | set(model.Projection.refs)


# Panel A -- the non-unit ledger; stornoabzug and withdrawals are 0.00 throughout, so the
# notes omit them.  t: (pols_if, premiums, prem_to_av, charge_acq, charge_admin_prem,
# charge_admin_fund, charge_policy_fee, charge_risk, expenses, commissions, net_cf)
PANEL_A = {
    0:   (1.000000, 200.00, 162.00, 30.00, 8.00, 0.04, 3.00, 0.00,  204.26, 1803.00, -1966.22),
    1:   (0.994807, 198.96, 161.16, 29.84, 7.96, 0.08, 2.98, 0.01,    4.25,    2.98,    33.64),
    2:   (0.989641, 197.93, 160.32, 29.69, 7.92, 0.12, 2.97, 0.01,    4.23,    2.97,    33.49),
    3:   (0.984502, 196.90, 159.49, 29.54, 7.88, 0.16, 2.95, 0.01,    4.22,    2.95,    33.35),
    4:   (0.979390, 195.88, 158.66, 29.38, 7.84, 0.20, 2.94, 0.01,    4.20,    2.94,    33.21),
    5:   (0.974304, 194.86, 157.84, 29.23, 7.79, 0.24, 2.92, 0.02,    4.19,    2.92,    33.08),
    11:  (0.944340, 188.87, 152.98, 28.33, 7.55, 0.46, 2.83, 0.03,    4.10,    2.83,    32.26),
    23:  (0.887098, 177.42, 143.71, 26.61, 7.10, 0.88, 2.66, 0.05,    3.92,    2.66,    30.69),
    58:  (0.738908, 147.78, 119.70, 22.17, 5.91, 1.93, 2.22, 0.10,    3.45,    2.22,    26.58),
    59:  (0.735054, 147.01, 119.08, 22.05, 5.88, 1.95, 2.21, 0.10,    3.44,    2.21,    26.47),
    60:  (0.731221, 146.24, 140.39,  0.00, 5.85, 1.98, 2.19, 0.11,    3.33,    2.19,     4.53),
    119: (0.625891, 125.18, 120.17,  0.00, 5.01, 4.02, 1.88, 0.00,    3.14,    1.88,     5.89),
    239: (0.459656,  91.93,  88.25,  0.00, 3.68, 7.71, 1.38, 0.00,    2.81,    1.38,     8.58),
    299: (0.385184,  77.04,  73.96,  0.00, 3.08, 9.16, 1.16, 0.00,    2.60,    1.16,     9.64),
    300: (0.384018,  76.80,  73.73,  0.00, 3.07, 9.19, 1.15, 0.00,    2.68,    1.15,     9.58),
    358: (0.304251,  60.85,  58.42,  0.00, 2.43, 9.82, 0.91, 0.00,    2.27,    0.91,     9.98),
    359: (0.303239,  60.65,  58.22,  0.00, 2.43, 9.84, 0.91, 0.00,   32.53,    0.91,   -20.27),
}

# The notes' Total row, summed at full precision and then rounded.
PANEL_A_TOTALS = {
    "pols_if": 202.931416, "premiums": 40586.28, "prem_to_av": 37413.08,
    "charge_acq": 1549.75, "charge_admin_prem": 1623.45, "charge_admin_fund": 2033.18,
    "charge_policy_fee": 608.79, "charge_risk": 5.85, "expenses": 1319.97,
    "commissions": 2408.79, "net_cf": 2087.87,
}

# Panel B -- the benefits, and what funds them.  Only death_strain crosses the unit /
# non-unit boundary.
# t: (claims_death, claims_lapse, claims_maturity, av_releases, death_strain, liability_cf)
PANEL_B = {
    0:   ( 0.01,   0.82,     0.00,     0.83, 0.0020, 1966.22),
    1:   ( 0.02,   1.64,     0.00,     1.65, 0.0040,  -33.64),
    5:   ( 0.06,   4.84,     0.00,     4.89, 0.0114,  -33.08),
    11:  ( 0.11,   9.48,     0.00,     9.57, 0.0212,  -32.26),
    23:  ( 0.23,  18.18,     0.00,    18.38, 0.0398,  -30.69),
    59:  ( 0.65,  40.13,     0.00,    40.70, 0.0745,  -26.47),
    60:  ( 0.72,  20.10,     0.00,    20.73, 0.0799,   -4.53),
    119: ( 1.90,  40.75,     0.00,    42.64, 0.0000,   -5.89),
    239: ( 9.43,  78.11,     0.00,    87.54, 0.0000,   -8.58),
    300: (19.90, 237.76,     0.00,   257.66, 0.0000,   -9.58),
    358: (31.15,  99.47,     0.00,   130.61, 0.0000,   -9.98),
    359: (31.19,   0.00, 39298.91, 39330.11, 0.0000,   20.27),
}

PANEL_B_TOTALS = {
    "claims_death": 3047.80, "claims_lapse": 22522.64, "claims_maturity": 39298.91,
    "av_releases": 64864.97, "death_strain": 4.39, "liability_cf": -2087.87,
}

# Panel C -- the Fondsguthaben, per policy; balances have no total.  t: (unit_price,
# units_pp, av_pp, bef_charge, aft_charge, bef_decr, cum_prem_pp, nar_pp, lapse_rate_mth,
# mort_rate_mth)
PANEL_C = {
    0:   (100.371482, 0.000000, 0.00, 162.60, 159.56, 159.56, 200.00, 40.44, 0.00514301, 5e-05),
    1:   (100.744344, 1.589679, 159.56, 322.75, 319.67, 319.67, 400.00, 80.33, 0.00514301, 5e-05),
    5:   (102.249694, 7.885561, 803.31, 968.90, 965.66, 965.64, 1200.00, 234.34, 0.00514301, 5e-05),
    59:  (124.916609, 83.728674, 10420.39, 10621.70, 10616.05, 10615.91, 12000.00, 1383.95, 0.00514301, 0.00007321),
    60:  (125.380652, 84.984001, 10615.91, 10848.06, 10842.35, 10842.20, 12200.00, 1357.65, 0.00253505, 0.00008053),
    93:  (141.700579, 131.144920, 18514.53, 18776.02, 18768.33, 18768.33, 18800.00, 31.67, 0.00253505, 0.00009744),
    94:  (142.226971, 132.450597, 18768.33, 19030.76, 19023.00, 19023.00, 19000.00, 0.00, 0.00253505, 0.00009744),
    239: (243.489783, 274.678167, 66633.79, 67074.04, 67054.27, 67054.27, 48000.00, 0.00, 0.00253505, 0.00030580),
    358: (378.539129, 340.534729, 128428.63, 129098.43, 129063.16, 129063.16, 71800.00, 0.00, 0.00253505, 0.00079315),
    359: (379.945333, 340.950641, 129063.16, 129735.32, 129699.88, 129699.88, 72000.00, 0.00, 0.0, 0.00079315),
}

# The Einmalbeitrag variant, model point 2: 50 000,00 EUR at 50, proj_len() = 204 months so
# the frame is t = 0 .. 203, a `fund`
# death benefit so charge_risk is 0.00 everywhere.  t: (pols_if, premiums, prem_to_av,
# charge_acq, charge_admin_prem, charge_admin_fund, charge_policy_fee, expenses,
# commissions, net_cf, av)
SINGLE_PREMIUM = {
    0:   (1.000000, 50000.00, 46750.00, 1250.00, 2000.00, 11.73, 3.00,  204.28, 2000.00, 1060.45, 46908.94),
    1:   (0.994685,     0.00,     0.00,    0.00,    0.00, 11.71, 2.98,    4.27,    0.00,   10.43, 47068.42),
    2:   (0.989399,     0.00,     0.00,    0.00,    0.00, 11.69, 2.97,    4.25,    0.00,   10.40, 47228.46),
    11:  (0.943067,     0.00,     0.00,    0.00,    0.00, 11.48, 2.83,    4.11,    0.00,   10.20, 48694.00),
    59:  (0.728611,     0.00,     0.00,    0.00,    0.00, 10.45, 2.19,    3.43,    0.00,    9.20, 57329.28),
    119: (0.611558,     0.00,     0.00,    0.00,    0.00, 10.76, 1.83,    3.09,    0.00,    9.50, 70347.78),
    203: (0.457239,     0.00,     0.00,    0.00,    0.00, 10.72, 1.37,   48.30,    0.00,  -36.21, 93766.43),
}

SINGLE_PREMIUM_TOTALS = {
    "pols_if": 136.171795, "premiums": 50000.00, "prem_to_av": 46750.00,
    "charge_acq": 1250.00, "charge_admin_prem": 2000.00, "charge_admin_fund": 2206.15,
    "charge_policy_fee": 408.52, "expenses": 911.63, "commissions": 2000.00,
    "net_cf": 2953.04,
}

# The reduction in yield across the four shipped charge scales.  The cells differ in premium
# and term as well as in tariff, so this is not a controlled experiment: what it shows is
# that the charge scale moves the measure by a factor of five.
# point_id: (charge_id, scenario_id, reduction_in_yield, av_maturity_pp)
RIY_BY_TARIFF = {
    11: ("std_netto", "etf",  0.004484, 255658.29),
    13: ("std_low",   "base", 0.007799, 158606.04),
    1:  ("std_gross", "base", 0.013407, 129699.88),
    5:  ("std_high",  "base", 0.024073, 229128.42),
}

# The closure identities the notes print below the table.
DECREMENTS = {"deaths": 0.04377181, "lapses": 0.65322937, "maturity": 0.30299882}
RISK_RESULT = {"charge_risk": 5.849973, "death_strain": 4.387480, "result": 1.462493}
BENEFIT_FUNDING = 64869.355293


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(PANEL_A))
def test_worked_example_panel_a_row(de_frv_anchor, t):
    """Every printed row of the notes' non-unit ledger, to the displayed precision."""
    (pols_if, prem, to_av, acq, admin_prem, admin_fund, fee, risk,
     exp, comm, net) = PANEL_A[t]
    p = de_frv_anchor
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.prem_to_av(t) == pytest.approx(to_av, abs=CENT)
    assert p.charge_acq(t) == pytest.approx(acq, abs=CENT)
    assert p.charge_admin_prem(t) == pytest.approx(admin_prem, abs=CENT)
    assert p.charge_admin_fund(t) == pytest.approx(admin_fund, abs=CENT)
    assert p.charge_policy_fee(t) == pytest.approx(fee, abs=CENT)
    assert p.charge_risk(t) == pytest.approx(risk, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.stornoabzug(t) == 0.0 and p.withdrawals(t) == 0.0


@pytest.mark.parametrize("t", sorted(PANEL_B))
def test_worked_example_panel_b_row(de_frv_anchor, t):
    """The benefits and what funds them.  ``death_strain`` is carried to four decimals
    rather than to the cent, because for most of the projection it is a hundredth of a cent
    a month and rounds to zero."""
    cd, cl, cm, releases, strain, liab = PANEL_B[t]
    p = de_frv_anchor
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "MATURITY") == pytest.approx(cm, abs=CENT)
    assert p.av_releases(t) == pytest.approx(releases, abs=CENT)
    assert p.death_strain(t) == pytest.approx(strain, abs=5e-5)
    assert p.liability_cf(t) == pytest.approx(liab, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(-p.net_cf(t), rel=1e-12)


@pytest.mark.parametrize("t", sorted(PANEL_C))
def test_worked_example_panel_c_row(de_frv_anchor, t):
    """The per-policy unit side: the price, the units and the four within-month balances.
    ``AFT_WD`` equals ``AFT_CHARGE`` throughout, there being no *Teilentnahme* here, and
    the notes omit the column for that reason; it is asserted so it stays a product fact."""
    (price, units, av, bef_charge, aft_charge, bef_decr, cum_prem, nar,
     lapse_mth, mort_mth) = PANEL_C[t]
    p = de_frv_anchor
    assert p.unit_price(t) == pytest.approx(price, abs=SIX_DP)
    assert p.units_pp(t) == pytest.approx(units, abs=SIX_DP)
    assert p.av_pp(t) == pytest.approx(av, abs=CENT)
    assert p.av_pp_at(t, "BEF_CHARGE") == pytest.approx(bef_charge, abs=CENT)
    assert p.av_pp_at(t, "AFT_CHARGE") == pytest.approx(aft_charge, abs=CENT)
    assert p.av_pp_at(t, "AFT_WD") == pytest.approx(aft_charge, abs=CENT)
    assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(bef_decr, abs=CENT)
    assert p.cum_prem_pp(t) == pytest.approx(cum_prem, abs=CENT)
    assert p.db_floor_pp(t) == pytest.approx(cum_prem, abs=CENT)   # Beitragsrückgewähr
    assert p.nar_pp(t) == pytest.approx(nar, abs=CENT)
    assert p.lapse_rate_mth(t) == pytest.approx(lapse_mth, abs=EIGHT_DP)
    assert p.mort_rate_mth(t) == pytest.approx(mort_mth, abs=EIGHT_DP)
    assert p.av_at(t, "BEF_DECR") == pytest.approx(
        p.av_pp_at(t, "BEF_DECR") * p.pols_if(t), rel=1e-12)   # the in-force fund


def test_the_totals_are_summed_at_full_precision(de_frv_anchor):
    """Every column total, summed at full precision and then rounded -- not cell by cell.

    Rounding the 360 cells first changes fourteen of the eighteen totals by one to twelve
    cents; ``death_strain`` rounds to zero in almost every month and loses six of 4,39.
    """
    p = de_frv_anchor
    df = p.result_cf()
    for column, total in PANEL_A_TOTALS.items():
        tol = SIX_DP * len(df) if column == "pols_if" else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    for column, total in PANEL_B_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert df["stornoabzug"].sum() == 0.0 and df["withdrawals"].sum() == 0.0
    assert sum(round(p.death_strain(t), 2) for t in df.index) == pytest.approx(
        4.33, abs=CENT)     # the rounded-cell sum, against 4.39 at full precision


def test_the_inception_month_rebuilt_from_the_tariff_alone(de_frv_anchor):
    """The notes' first independent check: ``t = 0`` from the parameters, not the recursion.

    Nine decimals are carried because six do not close the chain -- the *Gammakosten* at
    0.040650 would leave 159.561151 instead of 159.561150.
    """
    p = de_frv_anchor
    assert p.beitragssumme() == pytest.approx(200.0 * 12 * 30, rel=1e-12) == 72000.0
    assert p.charge_acq_total() == pytest.approx(0.025 * 72000.0, rel=1e-12) == 1800.0
    assert p.acq_instalments() == 60
    assert p.charge_acq_pp(0) == pytest.approx(1800.0 / 60, rel=1e-12) == 30.0
    assert p.charge_admin_prem_pp(0) == pytest.approx(0.04 * 200.0, rel=1e-12) == 8.0
    assert p.prem_to_av_pp(0) == pytest.approx(200.0 - 30.0 - 8.0, rel=1e-12) == 162.0
    i = p.fund_return_net_mth(0)
    assert i == pytest.approx(1.0455 ** (1.0 / 12.0) - 1.0, rel=1e-14)
    assert i == pytest.approx(0.0037148195588312, abs=5e-16)
    assert p.unit_price(0) == pytest.approx(100.0 * (1.0 + i), rel=1e-14)
    assert p.av_pp_at(0, "BEF_CHARGE") == pytest.approx(162.601800769, abs=5e-9)
    assert p.charge_admin_fund_pp(0) == pytest.approx(0.040650450, abs=5e-9)
    assert p.charge_policy_fee_pp(0) == 3.0 and p.db_floor_pp(0) == 200.0
    assert p.av_pp_at(0, "AFT_CHARGE") == pytest.approx(159.561150318, abs=5e-9)
    assert p.nar_pp(0) == pytest.approx(40.438849682, abs=5e-9)
    assert p.charge_risk_pp(0) == pytest.approx(0.00080 / 12 * 40.438849682, abs=5e-10)
    assert p.av_pp_at(0, "BEF_DECR") == pytest.approx(159.558454395, abs=5e-9)
    assert p.units_pp(1) == pytest.approx(159.558454395 / p.unit_price(0), abs=5e-9)


def test_month_sixty_is_the_cliff_and_the_risk_charge_at_a_second_age(de_frv_anchor):
    """The notes' second rebuild: the acquisition instalment stops and the age steps.

    The same row carries a second step -- ``claims_lapse`` halves from 40.13 to 20.10,
    because ``t = 60`` opens policy year 6 and the annual lapse rate drops from 6 % to 3 %.
    """
    p = de_frv_anchor
    assert p.charge_acq_pp(59) == 30.0 and p.charge_acq_pp(60) == 0.0
    assert p.prem_to_av_pp(59) == pytest.approx(162.0, rel=1e-12)
    assert p.prem_to_av_pp(60) == pytest.approx(192.0, rel=1e-12)
    assert p.av_pp_at(60, "BEF_CHARGE") == pytest.approx(
        (10615.913263 + 192.0) * (1.0 + p.fund_return_net_mth(60)), abs=5e-6)
    assert p.av_pp_at(60, "BEF_CHARGE") == pytest.approx(10848.062710117, abs=5e-6)
    assert p.charge_admin_fund_pp(60) == pytest.approx(2.712015678, abs=5e-8)
    assert p.av_pp_at(60, "AFT_CHARGE") == pytest.approx(10842.350694440, abs=5e-6)
    assert p.policy_year(60) == 6 and p.age(60) == 42
    assert p.mort_rate_tariff_mth(60) == pytest.approx(0.000107367333, abs=5e-13)
    assert p.cum_prem_pp(60) == pytest.approx(12200.0, rel=1e-12)
    assert p.nar_pp(60) == pytest.approx(1357.649305560, abs=5e-6)
    assert p.charge_risk_pp(60) == pytest.approx(0.145767186, abs=5e-9)
    assert p.charge_risk(60) == pytest.approx(0.10658796, abs=5e-8)
    assert p.lapse_rate(59) == pytest.approx(0.06, rel=1e-12)
    assert p.lapse_rate(60) == pytest.approx(0.03, rel=1e-12)
    assert p.claims(59, "LAPSE") == pytest.approx(40.13, abs=CENT)
    assert p.claims(60, "LAPSE") == pytest.approx(20.10, abs=CENT)


def test_the_reduction_in_yield_read_as_a_savings_account(de_frv_anchor):
    """The notes' third rebuild: 200,00 a month at the model's own IRR reaches the fund.

    At the scenario's **gross** 5.00 % the same premiums reach 163 739,57; the 34 039,69
    between is what the charge stack and the fund's TER cost over thirty years.
    """
    p = de_frv_anchor
    irr = p.irr_ann()
    assert irr == pytest.approx(0.036592629, abs=5e-9)
    monthly = (1.0 + irr) ** (1.0 / 12.0) - 1.0
    balance = sum(200.0 * (1.0 + monthly) ** (360 - t) for t in range(360))
    assert balance == pytest.approx(129699.8842, abs=CENT)
    assert p.av_maturity_pp() == pytest.approx(129699.8842, abs=CENT)
    gross = 1.05 ** (1.0 / 12.0) - 1.0
    gross_balance = sum(200.0 * (1.0 + gross) ** (360 - t) for t in range(360))
    assert gross_balance == pytest.approx(163739.57, abs=1.0)
    assert gross_balance - balance == pytest.approx(34039.69, abs=1.0)
    assert p.gross_return_ref() == pytest.approx(0.05, abs=1e-12)  # a level path
    assert p.reduction_in_yield() == pytest.approx(0.05 - irr, rel=1e-12)
    assert p.reduction_in_yield() == pytest.approx(0.013407, abs=5e-7)


def test_the_four_identities_that_close(de_frv_anchor):
    """The closure lines the notes print below the table, each exact.

    The acquisition line is worth reading twice: the ledger closes on 1 800,00 -- the
    *Höchstzillmersatz* -- while the ``charge_acq`` **column** totals 1 549,75, because it
    is weighted by ``pols_if``: the insurer's cost problem in one number.
    """
    p = de_frv_anchor
    n = p.proj_len()
    df = p.result_cf()
    deaths = sum(p.pols_death(t) for t in range(n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    assert deaths == pytest.approx(DECREMENTS["deaths"], abs=5e-9)
    assert lapses == pytest.approx(DECREMENTS["lapses"], abs=5e-9)
    assert p.pols_maturity(n - 1) == pytest.approx(DECREMENTS["maturity"], abs=5e-9)
    assert deaths + lapses + p.pols_maturity(n - 1) == pytest.approx(1.0, abs=1e-12)
    assert p.pols_if(n) == 0.0   # one past the frame's last index
    charge_risk, strain = df["charge_risk"].sum(), df["death_strain"].sum()
    assert charge_risk == pytest.approx(RISK_RESULT["charge_risk"], abs=5e-7)
    assert strain == pytest.approx(RISK_RESULT["death_strain"], abs=5e-7)
    assert charge_risk - strain == pytest.approx(RISK_RESULT["result"], abs=5e-7)
    assert charge_risk - strain == pytest.approx(0.25 * charge_risk, rel=1e-12)
    assert p.cum_charge_acq_pp(n - 1) == pytest.approx(60 * 30.0, abs=1e-9) == 1800.0
    assert p.cum_charge_acq_pp(n - 1) == pytest.approx(
        p.alpha_rate() * p.beitragssumme(), rel=1e-12)
    assert df["charge_acq"].sum() == pytest.approx(1549.75, abs=CENT)
    benefits = sum(df[c].sum() for c in
                   ("claims_death", "claims_lapse", "claims_maturity"))
    assert benefits == pytest.approx(BENEFIT_FUNDING, abs=5e-6)
    assert df["av_releases"].sum() + strain == pytest.approx(BENEFIT_FUNDING, abs=5e-6)
    charges = sum(df[c].sum() for c in ("charge_acq", "charge_admin_prem",
                                        "charge_admin_fund", "charge_policy_fee",
                                        "charge_risk", "stornoabzug"))
    assert charges == pytest.approx(5821.018511, abs=5e-6)
    assert df["expenses"].sum() == pytest.approx(1319.970596, abs=5e-6)
    assert df["commissions"].sum() == pytest.approx(2408.794247, abs=5e-6)
    assert (charges - df["expenses"].sum() - df["commissions"].sum()
            - strain) == pytest.approx(2087.866187, abs=5e-6)


def test_the_annuity_the_contract_exists_for(de_frv_anchor):
    """The Fondsguthaben at Rentenbeginn, the factor it is read at, and the annuity."""
    p = de_frv_anchor
    n = p.proj_len()
    assert p.av_maturity_pp() == pytest.approx(129699.88, abs=CENT)
    assert p.av_maturity_pp() == pytest.approx(p.av_pp_at(n - 1, "BEF_DECR"), rel=1e-15)
    assert p.annuity_age() == 67
    assert p.rentenfaktor_guar() == p.rentenfaktor_curr() == p.rentenfaktor_applied() == 25.0
    assert p.annuity_mth_pp() == pytest.approx(129699.88 / 10000.0 * 25.0, abs=CENT)
    assert p.claims(n - 1, "MATURITY") == pytest.approx(
        p.pols_maturity(n - 1) * p.av_maturity_pp(), rel=1e-12)


# ---------------------------------------------------------------------------
# The variants the notes tabulate


@pytest.mark.parametrize("t", sorted(SINGLE_PREMIUM))
def test_the_einmalbeitrag_variant_row(fondsgebundene_rentenversicherung, t):
    """Model point 2: the charges are taken once at the front and the sign reverses -- the
    inception month ``t = 0`` carries a ``net_cf`` of **+1 060,45** where the anchor's is
    -1 966,22, the 3 250,00 withheld at inception more than covering the 2 204,28 of
    acquisition cost."""
    (pols_if, prem, to_av, acq, admin_prem, admin_fund, fee, exp, comm, net,
     av) = SINGLE_PREMIUM[t]
    p = fondsgebundene_rentenversicherung.Projection[2]
    assert p.prem_form() == "einmal" and p.charge_risk(t) == 0.0
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.prem_to_av(t) == pytest.approx(to_av, abs=CENT)
    assert p.charge_acq(t) == pytest.approx(acq, abs=CENT)
    assert p.charge_admin_prem(t) == pytest.approx(admin_prem, abs=CENT)
    assert p.charge_admin_fund(t) == pytest.approx(admin_fund, abs=CENT)
    assert p.charge_policy_fee(t) == pytest.approx(fee, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(av, abs=CENT)


def test_the_einmalbeitrag_totals_and_conversion(fondsgebundene_rentenversicherung):
    """The acquisition charge is the *Zuzahlungskosten*, levied once on receipt: a single
    premium has no *Beitragssumme* to zillmer and no five-year spread to obey."""
    p = fondsgebundene_rentenversicherung.Projection[2]
    df = p.result_cf()
    assert p.proj_len() == 12 * (67 - 50) == 204
    assert p.acq_window_months() == 0 and p.acq_instalments() == 1   # once, on receipt
    assert p.charge_acq_total() == pytest.approx(
        p.zuzahlung_charge_rate() * 50000.0, rel=1e-12) == 1250.0
    for column, total in SINGLE_PREMIUM_TOTALS.items():
        tol = SIX_DP * len(df) if column == "pols_if" else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert p.av_maturity_pp() == pytest.approx(93766.43, abs=CENT)
    assert p.annuity_mth_pp() == pytest.approx(234.42, abs=CENT)
    assert p.reduction_in_yield() == pytest.approx(0.012320, abs=5e-7)
    assert all(getattr(p, c)() is True for c in CHECKS)


@pytest.mark.parametrize("point_id", sorted(RIY_BY_TARIFF))
def test_the_reduction_in_yield_across_the_four_charge_scales(
        fondsgebundene_rentenversicherung, point_id):
    """The charge scale moves the measure by a factor of five across the argued range.

    The gap between model point 11's *Nettotarif* and the anchor's commission tariff **is**
    the acquisition load.  ``comm_acq_rate`` is a flat scalar, so on the two low-load
    tariffs the assumed commission exceeds the tariff's own charge and those cells carry a
    projected loss -- the flat assumption showing, not a product fact.
    """
    charge_id, scenario_id, riy, av = RIY_BY_TARIFF[point_id]
    p = fondsgebundene_rentenversicherung.Projection[point_id]
    assert p.charge_id() == charge_id and p.scenario_id() == scenario_id
    assert p.reduction_in_yield() == pytest.approx(riy, abs=5e-7)
    assert p.av_maturity_pp() == pytest.approx(av, abs=CENT)
    assert p.gross_return_ref() == pytest.approx(0.05, abs=1e-9)
    assert p.expense_acq_pp(0) == 200.0
    assert p.comm_acq_pp(0) == pytest.approx(0.025 * p.beitragssumme(), rel=1e-12)
    if charge_id == "std_netto":
        assert p.alpha_rate() == 0.0 and p.charge_acq_total() == 0.0
        assert p.result_cf()["charge_acq"].sum() == 0.0
        assert p.result_cf()["net_cf"].sum() < 0.0
        assert p.reduction_in_yield() < RIY_BY_TARIFF[1][2]

# ---------------------------------------------------------------------------
# One test per numbered modeling pitfall in the technical notes


def test_pitfall_1_the_fund_charge_cancels_units_and_survives_the_premium(
        fondsgebundene_rentenversicherung):
    """A model netting gamma off the *Beitrag* is right until the premium stops.  Model
    point 7 goes *beitragsfrei* at ``t = 120`` on a zero-return fund: from there
    ``premiums`` is zero, ``charge_admin_fund`` is not, and the fund decays."""
    p = fondsgebundene_rentenversicherung.Projection[7]
    assert p.pup_month() == 120 and p.scenario_id() == "zero"
    assert p.premiums(119) > 0.0
    for t in (120, 121, 199, 239, 323):
        assert p.premiums(t) == 0.0
        assert p.charge_admin_prem(t) == 0.0      # stops with the premium
        assert p.charge_acq(t) == 0.0
        assert p.charge_admin_fund(t) > 0.0       # continues by unit cancellation
        assert p.charge_policy_fee(t) > 0.0 and p.charge_risk(t) > 0.0
    assert p.av_pp_at(121, "BEF_DECR") < p.av_pp_at(120, "BEF_DECR")
    assert p.av_pp_at(323, "BEF_DECR") < p.av_pp_at(120, "BEF_DECR")
    assert p.charge_admin_fund_pp(199) == pytest.approx(
        p.gamma_rate_mth() * p.av_pp_at(199, "BEF_CHARGE"), rel=1e-12)
    assert p.gamma_rate_mth() == pytest.approx(0.0030 / 12.0, rel=1e-15) == 0.00025


def test_pitfall_2_the_ter_lives_in_the_unit_price_and_in_no_charge_column(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """unit_price(t)/unit_price_open(t) = (1 + gross - ter)^(1/12), exactly.  Charging the
    TER explicitly double-counts the fund's costs and ignoring it overstates the return;
    the model nets it off the assumed return, so it is in no ``charge_*`` cells."""
    p = de_frv_anchor
    assert p.fund_return_gross_ann(0) == 0.05 and p.fund_ter_ann(0) == 0.0045
    assert p.fund_return_net_ann(0) == pytest.approx(0.0455, rel=1e-12)
    for t in (0, 1, 60, 179, 359):
        step = (1.0 + p.fund_return_gross_ann(t) - p.fund_ter_ann(t)) ** (1.0 / 12.0)
        assert p.unit_price(t) / p.unit_price_open(t) == pytest.approx(step, rel=1e-14)
    assert [c for c in p.result_cf().columns if c.startswith("charge_")] == [
        "charge_acq", "charge_admin_prem", "charge_admin_fund", "charge_policy_fee",
        "charge_risk"]
    for absent in ("charge_ter", "charge_fund_cost", "ter_charge_pp", "fund_cost_pp"):
        assert absent not in _names(fondsgebundene_rentenversicherung), absent
    etf = fondsgebundene_rentenversicherung.Projection[11]   # same gross, a cheaper fund
    assert etf.fund_ter_ann(0) == 0.0015
    assert etf.fund_return_net_mth(0) > p.fund_return_net_mth(0)


def test_pitfall_3_the_two_mortality_bases_live_in_two_files(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """No cells reads both mort_table.csv and rentenfaktor_table.csv.

    The death charge is priced on a death table (DAV 2008 T) and the conversion guarantee
    on an annuity table (DAV 2004 R); using one for both misprices one of them.
    """
    proj = fondsgebundene_rentenversicherung.Projection
    readers = {nm: {f for f in ("data.mort_table(", "data.rentenfaktor_table(")
                    if f in (proj.cells[nm].formula.source or "")}
               for nm in proj.cells}
    assert readers["mort_rate_tariff_at_age"] == {"data.mort_table("}
    assert readers["rentenfaktor_guar"] == {"data.rentenfaktor_table("}
    assert readers["rentenfaktor_curr"] == {"data.rentenfaktor_table("}
    assert [nm for nm, hits in readers.items() if len(hits) == 2] == []
    p = de_frv_anchor
    assert p.charge_risk_pp(0) == pytest.approx(
        p.mort_rate_tariff_mth(0) * p.nar_pp(0), rel=1e-12)
    assert p.mort_rate_tariff_at_age(37) == 0.00080 and p.rentenfaktor_guar() == 25.0
    assert p.mort_rate_tariff_at_age(47) == pytest.approx(0.00080 * 1.10 ** 10, rel=1e-9)


def test_pitfall_4_the_risk_result_is_exactly_a_quarter_of_the_risk_charge(de_frv_anchor):
    """Sum charge_risk - sum death_strain = (1 - mort_be_factor) x sum charge_risk.

    The tariff prices first order, the projection decrements second order, and the wedge is
    the *Risikoergebnis*.  Decrementing on the tariff basis would print zero here.
    """
    p = de_frv_anchor
    df = p.result_cf()
    charge, strain = df["charge_risk"].sum(), df["death_strain"].sum()
    assert charge > 0.0 and strain > 0.0 and charge - strain > 0.0
    assert charge - strain == pytest.approx(0.25 * charge, rel=1e-12)
    assert p.mort_rate(0) == pytest.approx(0.75 * p.mort_rate_tariff(0), rel=1e-15)
    assert p.mort_rate(0) == pytest.approx(0.00060, abs=5e-9)
    assert p.mort_rate_tariff(0) == pytest.approx(0.00080, abs=5e-9)
    for t in (0, 29, 60):
        assert p.death_strain(t) == pytest.approx(
            p.pols_death(t) * p.nar_pp(t), rel=1e-12)
        assert p.charge_risk(t) - p.death_strain(t) == pytest.approx(
            0.25 * p.charge_risk(t), rel=1e-9)


def test_pitfall_5_the_two_monthly_conversions_stay_different(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """q/12 for the charge and the decrement; 1 - (1-w)^(1/12) for the lapse rate.

    At q = 0.00080 the splits differ by 0.04 %, which would land entirely in the risk
    result.  The tax-threshold step needs **both** limbs of the 12/62 rule: the anchor
    passes duration 12 at age 48, so its step falls in policy year 26, not at ``t = 144``.
    """
    p = de_frv_anchor
    for t in (0, 60, 299, 359):
        assert p.mort_rate_mth(t) == pytest.approx(p.mort_rate(t) / 12.0, rel=1e-15)
        assert p.mort_rate_tariff_mth(t) == pytest.approx(
            p.mort_rate_tariff(t) / 12.0, rel=1e-15)
    geometric = 1.0 - (1.0 - 0.00080) ** (1.0 / 12.0)
    assert 0.00080 / 12.0 == pytest.approx(0.00006667, abs=5e-9)
    assert geometric == pytest.approx(0.00006669, abs=5e-9)
    assert geometric / (0.00080 / 12.0) - 1.0 == pytest.approx(0.0004, abs=5e-5)
    for t in (0, 60, 300):
        assert p.lapse_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - p.lapse_rate(t)) ** (1.0 / 12.0), rel=1e-14)
        assert p.lapse_rate_mth(t) < p.lapse_rate(t)
    assert p.lapse_rate_mth(0) == pytest.approx(0.00514301, abs=EIGHT_DP)
    assert (1.0 + p.fund_return_net_mth(0)) ** 12 - 1.0 == pytest.approx(
        p.fund_return_net_ann(0), rel=1e-14)
    assert p.gamma_rate_mth() * 12.0 == pytest.approx(p.gamma_rate_ann(), rel=1e-15)
    assert max(13, 62 - p.entry_age() + 1) == 26 == p.policy_year(300)
    assert p.age(300) == 62
    assert p.lapse_tax_step(299) == 1.0 and p.lapse_tax_step(312) == 1.0
    assert all(p.lapse_tax_step(t) == 2.5 for t in (300, 305, 311))
    assert p.lapse_rate(300) == pytest.approx(0.075, rel=1e-12)
    assert p.lapse_rate_mth(300) == pytest.approx(0.00647574, abs=EIGHT_DP)
    assert p.lapse_rate(144) == pytest.approx(0.03, rel=1e-12)   # duration 13, age 49
    short = fondsgebundene_rentenversicherung.Projection[12]   # its step year never comes
    assert short.entry_age() == 55 and short.proj_len() == 144
    assert all(short.lapse_tax_step(t) == 1.0 for t in range(144))


def test_pitfall_6_the_net_amount_at_risk_is_floored_at_zero(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """max(D - F, 0), not D - F.  Without the floor the death strain turns negative.

    On the *Beitragsrückgewähr* shape the amount at risk vanishes once the fund overtakes
    the premiums paid -- ``t = 94`` on the anchor -- and the unfloored difference is large
    and negative thereafter.  A `pct_fund` floor grows with the fund; `fund` has none.
    """
    p = de_frv_anchor
    n = p.proj_len()
    assert all(p.nar_pp(t) >= 0.0 and p.death_strain(t) >= 0.0 for t in range(n))
    assert p.nar_pp(93) > 0.0 and p.nar_pp(94) == 0.0
    assert p.av_pp_at(93, "AFT_WD") < p.cum_prem_pp(93)
    assert p.av_pp_at(94, "AFT_WD") > p.cum_prem_pp(94)
    assert p.db_floor_pp(239) - p.av_pp_at(239, "AFT_WD") < -18000.0
    assert p.charge_risk_pp(239) == 0.0
    for point_id in (2, 13):
        q = fondsgebundene_rentenversicherung.Projection[point_id]
        assert q.db_form() == "fund"     # no floor, so no Risikobeitrag at all
        assert q.result_cf()["charge_risk"].sum() == 0.0
        assert all(q.nar_pp(t) == 0.0
                   for t in (0, q.proj_len() // 2, q.proj_len() - 1))
    pct = fondsgebundene_rentenversicherung.Projection[12]
    assert pct.db_form() == "pct_fund" and pct.db_pct() == 1.1
    for t in (0, 23, 143):
        assert pct.nar_pp(t) == pytest.approx(0.1 * pct.av_pp_at(t, "AFT_WD"), rel=1e-9)
    assert pct.result_cf()["charge_risk"].sum() > 0.0


def test_pitfall_7_the_acquisition_instalment_stops_at_its_window(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """The instalment is zero past the window, and the count follows the frequency.

    60 monthly, 20 quarterly, 10 half-yearly, 5 annual, 24 on model point 12.  Two
    exceptions follow from the charge's definition and are stated rather than asserted
    away: ``charge_acq(120)`` is non-zero on point 9, where the *Zuzahlung* pays 500,00 of
    *Zuzahlungskosten*; and the per-policy total equals ``alpha_rate x beitragssumme()``
    on eleven points but not on point 6, whose frame opens past the window, nor on 9.
    """
    assert de_frv_anchor.acq_window_months() == 60
    assert all(de_frv_anchor.charge_acq_pp(t) == 30.0 for t in (0, 29, 58, 59))
    assert all(de_frv_anchor.charge_acq_pp(t) == 0.0 for t in (60, 61, 119, 359))
    for point_id, (mode, count, instalment) in {
            1: (1, 60, 30.0), 3: (3, 20, 111.0), 4: (6, 10, 132.0), 5: (12, 5, 630.0)
    }.items():
        q = fondsgebundene_rentenversicherung.Projection[point_id]
        assert q.prem_mode_months() == mode and q.acq_window_months() == 60
        assert q.acq_instalments() == count
        assert q.charge_acq_pp(0) == pytest.approx(instalment, abs=CENT)
        assert q.charge_acq_total() == pytest.approx(count * instalment, abs=CENT)
        assert q.check_acq_charge() is True
    short = fondsgebundene_rentenversicherung.Projection[12]
    assert short.prem_term_y() == 2
    assert short.acq_window_months() == 24 and short.acq_instalments() == 24
    assert short.charge_acq_total() == pytest.approx(0.025 * 12000.0, rel=1e-12) == 300.0
    assert short.charge_acq_pp(23) == 12.5 and short.charge_acq_pp(24) == 0.0
    assert short.cum_charge_acq_pp(143) == pytest.approx(300.0, abs=1e-9)
    topup = fondsgebundene_rentenversicherung.Projection[9]
    assert topup.charge_acq_pp(120) == pytest.approx(500.0, rel=1e-12)
    assert topup.charge_acq_pp(121) == 0.0
    assert sum(topup.charge_acq_pp(t) for t in range(topup.proj_len())) == (
        pytest.approx(3380.0, abs=1e-9))
    assert topup.alpha_rate() * topup.beitragssumme() == pytest.approx(2880.0, rel=1e-12)
    assert topup.check_acq_charge() is True


def test_pitfall_8_an_in_force_cell_carries_no_acquisition_charge_or_commission(
        fondsgebundene_rentenversicherung):
    """Model point 6 opens at t = 96: the charge and the commission are both behind it.

    ``duration_init_m`` is an elapsed count and is already 0-based, so it **is** the first
    projected index.  That is the whole difference between an in-force cell and a
    new-business one here, and why ``t`` counts policy months from inception: one rule
    serves both.
    """
    p = fondsgebundene_rentenversicherung.Projection[6]
    assert p.duration_init_m() == 96 and p.proj_start() == 96
    assert p.result_cf().index[0] == 96
    assert p.acq_window_months() == 60          # the window is real, and already closed
    assert p.charge_acq_total() == pytest.approx(0.025 * 111000.0, rel=1e-12) == 2775.0
    assert p.result_cf()["charge_acq"].sum() == 0.0 == p.cum_charge_acq_pp(
        p.proj_len() - 1)
    assert p.expense_acq_pp(96) == 0.0 and p.comm_acq_pp(96) == 0.0
    assert p.expenses(96) < 20.0
    assert p.expenses(96) == pytest.approx(
        p.expense_maint_pp(96) * p.pols_if(96)
        + 150.0 * p.pols_death(96) + 50.0 * p.pols_lapse(96), rel=1e-12)
    assert p.commissions(96) == pytest.approx(
        0.015 * p.prem_pp(96) * p.pols_if(96), rel=1e-12)
    # It opens with a live fund, a real Beitragsrückgewähr base and a live risk charge.
    assert p.av_pp(96) == pytest.approx(190.0 * 118.4, rel=1e-12) == 22496.0
    assert p.cum_prem_init() == 24000.0 and p.cum_prem_pp(95) == 24000.0
    assert p.nar_pp(96) > 0.0 and p.charge_risk(96) > 0.0
    assert all(getattr(p, c)() is True for c in CHECKS)


def test_pitfall_9_the_beitragssumme_is_the_premiums_payable_at_the_initial_level(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """S is invariant to lapse, to Beitragsfreistellung and to the Beitragsdynamik: letting
    it follow the premiums actually paid would make the acquisition charge a function of
    the lapse assumption -- wrong, and circular."""
    p = de_frv_anchor
    assert p.beitragssumme() == pytest.approx(
        p.prem_pp_base() * (12.0 / p.prem_mode_months()) * p.prem_term_y(), rel=1e-12)
    assert p.beitragssumme() == 72000.0
    assert p.result_cf()["premiums"].sum() < 0.6 * p.beitragssumme()
    pup = fondsgebundene_rentenversicherung.Projection[7]   # beitragsfrei from t = 120
    assert pup.beitragssumme() == pytest.approx(250.0 * 12 * 27, rel=1e-12) == 81000.0
    assert pup.cum_charge_acq_pp(pup.proj_len() - 1) == pytest.approx(2025.0, abs=1e-9)
    dyn = fondsgebundene_rentenversicherung.Projection[10]
    assert dyn.dynamik_rate() == 0.03
    assert dyn.prem_pp(0) == 150.0 and dyn.prem_pp(11) == 150.0
    assert dyn.prem_pp(12) == pytest.approx(150.0 * 1.03, rel=1e-12)
    assert dyn.prem_pp(24) == pytest.approx(150.0 * 1.03 ** 2, rel=1e-12)
    assert dyn.beitragssumme() == pytest.approx(150.0 * 12 * 39, rel=1e-12) == 70200.0
    topup = fondsgebundene_rentenversicherung.Projection[9]   # nor does a Zuzahlung
    assert topup.beitragssumme() == pytest.approx(300.0 * 12 * 32, rel=1e-12) == 115200.0


def test_pitfall_10_beitragsfreistellung_is_a_change_of_state_and_not_an_exit(
        fondsgebundene_rentenversicherung):
    """pols_if is continuous across t = 120 while premiums step to zero.

    One is an exit paying the *Rückkaufswert*, the other a change of state paying nothing.
    It is a model point election, not a cohort decrement: one point carries it, and no
    paid-up rate exists anywhere in the model.
    """
    p = fondsgebundene_rentenversicherung.Projection[7]
    assert p.premiums(119) > 0.0 and p.premiums(120) == 0.0
    ordinary = 1.0 / ((1.0 - p.mort_rate_mth(119)) * (1.0 - p.lapse_rate_mth(119)))
    assert p.pols_if(119) / p.pols_if(120) == pytest.approx(ordinary, rel=1e-12)
    assert p.claims(120, "LAPSE") == pytest.approx(
        p.pols_lapse(120) * p.av_pp_at(120, "BEF_DECR"), rel=1e-12)
    assert p.pols_lapse(120) > 0.0 and p.pols_maturity(120) == 0.0
    table = fondsgebundene_rentenversicherung.Data.model_point_table()
    assert (table["pup_month"] > 0).sum() == 1 and table.loc[1, "pup_month"] == 0
    for absent in ("pup_rate", "pols_pup", "paid_up_rate", "pols_paidup"):
        assert absent not in _names(fondsgebundene_rentenversicherung), absent


def test_pitfall_11_the_surrender_value_is_the_fund_and_nothing_else(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """claims_lapse = pols_lapse x av_pp_at(t, "BEF_DECR") exactly, wherever sigma = 0.

    § 169 VVG sends the contract to the *Zeitwert*, which on a pure unit-linked policy is
    the fund: no discounting, no mortality basis, no *Mindestrückkaufswert*.
    """
    p = de_frv_anchor
    n = p.proj_len()
    assert p.stornoabzug_rate() == 0.0
    for t in (0, 11, 60, 239, 358):
        assert p.claims(t, "LAPSE") == pytest.approx(
            p.pols_lapse(t) * p.av_pp_at(t, "BEF_DECR"), rel=1e-12)
    assert p.av_pp_at(0, "BEF_DECR") > 0.0 and p.claims(0, "LAPSE") > 0.0  # positive at once
    names = _names(fondsgebundene_rentenversicherung)
    for absent in ("disc_factor", "tech_rate", "rechnungszins", "deckungskapital",
                   "min_surr_value_pp", "zillmer_rate", "surr_value_pp",
                   "paid_up_factor", "asset_share", "mvr"):
        assert absent not in names, absent
    # In the last month a surrender and an annuitisation are the same event.
    assert p.lapse_rate_base(n - 1) > 0.0 and p.lapse_rate_mth(n - 1) == 0.0
    assert p.pols_lapse(n - 1) == 0.0 and p.claims(n - 1, "LAPSE") == 0.0


def test_pitfall_12_the_stornoabzug_is_a_flat_rate_on_the_fund(
        fondsgebundene_rentenversicherung):
    """sigma x pols_lapse x av, and never a function of the unrecovered charge.

    § 169 VVG makes a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten*
    ineffective.  The deduction rises with the fund while the unrecovered charge falls to
    zero, so it cannot be a function of it.
    """
    p = fondsgebundene_rentenversicherung.Projection[5]
    assert p.charge_id() == "std_high" and p.stornoabzug_rate() == 0.02
    for t in (0, 12, 59, 239):
        assert p.stornoabzug(t) == pytest.approx(
            0.02 * p.pols_lapse(t) * p.av_pp_at(t, "BEF_DECR"), rel=1e-12)
        assert p.claims(t, "LAPSE") == pytest.approx(
            p.pols_lapse(t) * p.av_pp_at(t, "BEF_DECR") * 0.98, rel=1e-12)
    assert p.charge_acq_total() - p.cum_charge_acq_pp(12) > 0.0
    assert p.charge_acq_total() - p.cum_charge_acq_pp(239) == 0.0
    assert p.stornoabzug_pp(239) > p.stornoabzug_pp(12)
    assert p.result_cf()["stornoabzug"].sum() == pytest.approx(853.00, abs=CENT)
    assert p.check_benefit_funding() is True and p.check_net_cf() is True
    charges = fondsgebundene_rentenversicherung.Data.charge_table()
    assert (charges["stornoabzug_rate"] > 0).sum() == 1   # only std_high carries one


def test_pitfall_13_the_fund_is_not_booked_as_an_insurer_outgo(de_frv_anchor):
    """net_cf is the non-unit stream; the fund is the policyholder's money passing through.

    Booking the whole *Fondsguthaben* as an outgo overstates the liability by the entire
    fund -- 64 865 EUR against a true insurer cost of 4,39 EUR on this cell.
    """
    p = de_frv_anchor
    df = p.result_cf()
    assert p.check_net_cf() is True and p.check_benefit_funding() is True
    for t in (0, 60, 239, 359):
        rebuilt = (p.charge_acq(t) + p.charge_admin_prem(t) + p.charge_admin_fund(t)
                   + p.charge_policy_fee(t) + p.charge_risk(t) + p.stornoabzug(t)
                   - p.expenses(t) - p.commissions(t) - p.death_strain(t))
        assert p.net_cf(t) == pytest.approx(rebuilt, rel=1e-12, abs=1e-9)
        funded = (p.claims(t, "DEATH") + p.claims(t, "LAPSE") + p.claims(t, "MATURITY")
                  + p.withdrawals(t) + p.stornoabzug(t))
        assert funded == pytest.approx(p.av_releases(t) + p.death_strain(t), abs=1e-8)
    assert df.loc[359, "claims_maturity"] == pytest.approx(39298.91, abs=CENT)
    assert df.loc[359, "net_cf"] == pytest.approx(-20.27, abs=CENT)


def test_pitfall_14_the_rentenfaktor_is_read_at_the_annuity_age(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """age(proj_len() - 1) is annuity_age - 1: the annuity begins at that month's end.

    The off-by-one would fetch 24.449878 at 66 instead of 25.00 at 67 and understate the
    pension by 2.2 %.
    """
    p = de_frv_anchor
    n = p.proj_len()
    assert n == 12 * (67 - 37) == 360
    assert p.age(n - 1) == 66 == p.annuity_age() - 1 and p.policy_year(n - 1) == 30
    assert p.rentenfaktor_guar() == 25.0
    table = fondsgebundene_rentenversicherung.Data.rentenfaktor_table()
    off_by_one = float(table.loc[("std_2026", 66), "rentenfaktor_guar"])
    assert off_by_one == pytest.approx(24.449878, abs=5e-7)
    wrong = p.av_maturity_pp() / 10000.0 * off_by_one
    assert wrong == pytest.approx(317.11, abs=CENT)
    assert 1.0 - wrong / p.annuity_mth_pp() == pytest.approx(0.022, abs=0.0005)
    # The derivation the [std] table carries: 10 000 / (12 T_eff), T_eff(67) = 100/3.
    assert 10000.0 / (12.0 * (100.0 / 3.0)) == pytest.approx(25.0, rel=1e-12)
    assert float(table.loc[("std_2026", 62), "rentenfaktor_guar"]) == pytest.approx(
        10000.0 / (400.0 - 9.0 * (62 - 67)), abs=5e-7)


def test_pitfall_15_the_applied_factor_is_the_higher_of_guaranteed_and_current(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """max(guaranteed, current): a guarantee with upside, not a ceiling.

    On ``std_2026`` the two are equal, so the max() is exercised without an unsourced
    uplift; model point 13 carries ``rich_current``, 12 % higher, where it bites -- and a
    model applying only the guaranteed factor would understate that pension by 12 %.
    """
    p = de_frv_anchor
    assert p.rentenfaktor_guar() == p.rentenfaktor_curr() == 25.0
    assert p.rentenfaktor_applied() == pytest.approx(
        max(p.rentenfaktor_guar(), p.rentenfaktor_curr()), rel=1e-15)
    rich = fondsgebundene_rentenversicherung.Projection[13]
    assert rich.rentenfaktor_id() == "rich_current" and rich.annuity_age() == 70
    assert rich.rentenfaktor_guar() == pytest.approx(26.809651, abs=5e-7)
    assert rich.rentenfaktor_curr() == pytest.approx(30.026809, abs=5e-7)
    assert rich.rentenfaktor_applied() == rich.rentenfaktor_curr()
    assert rich.annuity_mth_pp() == pytest.approx(476.24, abs=CENT)
    guaranteed_only = rich.av_maturity_pp() / 10000.0 * rich.rentenfaktor_guar()
    assert rich.annuity_mth_pp() / guaranteed_only == pytest.approx(1.12, abs=5e-8)
    assert rich.kapitalwahl() is True   # a reporting split that moves no cash flow
    assert rich.claims(rich.proj_len() - 1, "MATURITY") == pytest.approx(
        rich.pols_maturity(rich.proj_len() - 1) * rich.av_maturity_pp(), rel=1e-12)


def test_pitfall_16_the_stated_instalment_is_not_loaded_again(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """premiums(t) = prem_pp x pols_if(t) in a premium month, and 0.00 in between.

    ``prem_pp_base`` already contains any *Ratenzahlungszuschlag*, so loading it again
    charges the fractionation twice.  There is no frequency-loading cells here.
    """
    p = de_frv_anchor
    for t in (0, 11, 60, 359):
        assert p.premiums(t) == pytest.approx(p.prem_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.prem_pp(t) == pytest.approx(p.prem_pp_base(), rel=1e-12)
    for point_id, (mode, amount) in {3: (3, 600.0), 4: (6, 1200.0),
                                     5: (12, 3000.0)}.items():
        q = fondsgebundene_rentenversicherung.Projection[point_id]
        assert q.prem_pp(0) == pytest.approx(amount, abs=CENT)
        assert q.premiums(0) == pytest.approx(amount * q.pols_if(0), rel=1e-12)
        for offset in range(1, mode):
            assert q.prem_pp(offset) == 0.0 and q.premiums(offset) == 0.0
            assert q.charge_admin_prem(offset) == 0.0
            assert q.charge_acq(offset) == 0.0
        assert q.prem_pp(mode) == pytest.approx(amount, abs=CENT)
    for absent in ("prem_freq_load", "prem_freq_fee", "freq_loading_table",
                   "ratenzahlungszuschlag", "prem_tariff_pp"):
        assert absent not in _names(fondsgebundene_rentenversicherung), absent


def test_pitfall_17_the_death_benefit_floor_is_the_premiums_paid_not_invested(
        de_frv_anchor):
    """cum_prem_pp(59) = 12 000,00 against 9 720,00 actually put into units: reading the
    floor off the invested amount understates the death benefit by 19 % over the whole
    acquisition window, exactly where the amount at risk is largest."""
    p = de_frv_anchor
    assert p.cum_prem_pp(59) == pytest.approx(60 * 200.0, rel=1e-12) == 12000.0
    invested = sum(p.prem_to_av_pp(t) for t in range(60))
    assert invested == pytest.approx(60 * 162.0, rel=1e-12) == 9720.0
    assert 1.0 - invested / p.cum_prem_pp(59) == pytest.approx(0.19, abs=0.0005)
    assert p.db_form() == "prem_return" and p.cum_prem_init() == 0.0
    assert p.db_floor_pp(59) == pytest.approx(p.cum_prem_pp(59), rel=1e-15)
    for t in (60, 239, 359):    # the recursion step; t = 0 is the seeded first month
        assert p.cum_prem_pp(t) == pytest.approx(
            p.cum_prem_pp(t - 1) + p.prem_pp(t) + p.topup_pp(t), rel=1e-12)
    assert p.cum_prem_pp(0) == pytest.approx(
        p.cum_prem_init() + p.prem_pp(0) + p.topup_pp(0), rel=1e-12)
    for t in (0, 59, 93, 239):
        assert p.db_pp(t) == pytest.approx(
            p.av_pp_at(t, "BEF_DECR") + p.nar_pp(t), rel=1e-12)
        assert p.claims(t, "DEATH") == pytest.approx(
            p.pols_death(t) * p.db_pp(t), rel=1e-12)


def test_pitfall_18_no_balance_goes_negative_and_no_floor_is_triggered(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """Every within-month balance is non-negative and no shipped cell hits a floor.

    The ``min(.., remaining)`` guards are **[std]** safeguards, not tariff terms.  Model
    point 7 is the hardest case: a decaying paid-up fund on a zero-return path under a
    fixed *garantierte Mindesttodesfallleistung*, where the amount at risk grows.
    """
    timings = ("BEF_CHARGE", "AFT_CHARGE", "AFT_WD", "BEF_DECR")
    p = de_frv_anchor
    for t in range(0, p.proj_len(), 17):
        assert all(p.av_pp_at(t, tau) >= 0.0 for tau in timings), t
    hard = fondsgebundene_rentenversicherung.Projection[7]
    assert hard.db_form() == "sum_assured" and hard.sum_assured() == 40000.0
    for t in range(hard.proj_start(), hard.proj_len(), 11):
        assert all(hard.av_pp_at(t, tau) >= 0.0 for tau in timings), t
        assert hard.charge_policy_fee_pp(t) == pytest.approx(3.0, rel=1e-12)
        assert hard.charge_risk_pp(t) == pytest.approx(
            hard.mort_rate_tariff_mth(t) * hard.nar_pp(t), rel=1e-12)
    assert hard.nar_pp(323) > hard.nar_pp(120) and hard.av_maturity_pp() > 0.0
    assert hard.charge_risk_pp(323) > hard.charge_risk_pp(120)


# ---------------------------------------------------------------------------
# The published identities and the product's own invariants


def test_check_net_cf_is_delib_ruling_one_and_crosses_the_unit_boundary(de_frv_anchor):
    """All seven checks are bools over all t, their residuals zero at every month sampled.

    ``check_net_cf_resid`` rebuilds the premium-side charges as ``premiums - prem_to_av``,
    a different route from the one ``net_cf`` uses -- which makes it a check rather than a
    restatement: it closes the *Beitragsverrechnung* and the ledger against each other.
    """
    p = de_frv_anchor
    for name in CHECKS:
        assert getattr(p, name)() is True, name
        resid = getattr(p, name + "_resid")
        for t in (0, 1, 59, 60, 119, 239, 300, 358, 359):
            assert abs(resid(t)) < 1e-8, (name, t)
    for t in (0, 1, 60, 239, 359):
        withheld = p.premiums(t) - p.prem_to_av(t)
        assert withheld == pytest.approx(
            p.charge_acq(t) + p.charge_admin_prem(t), abs=1e-9)
        rebuilt = (withheld + p.charge_admin_fund(t) + p.charge_policy_fee(t)
                   + p.charge_risk(t) + p.stornoabzug(t)
                   - p.expenses(t) - p.commissions(t) - p.death_strain(t))
        assert p.check_net_cf_resid(t) == pytest.approx(p.net_cf(t) - rebuilt, abs=1e-12)
        assert abs(p.check_net_cf_resid(t)) < 1e-9
    assert p.check_net_cf() is True and p.check_prem_split() is True


def test_the_unit_and_account_identities_are_not_redundant(de_frv_anchor):
    """One has no price term and the other carries it; an implementation can pass either.

    The unit identity catches a charge taken in euro without the units being cancelled;
    the account identity catches the return applied at the wrong point in the order.
    """
    p = de_frv_anchor
    for t in (0, 1, 60, 239, 358):
        assert p.units_pp(t + 1) == pytest.approx(
            p.units_pp(t) + p.units_bought_pp(t) - p.units_cancelled_pp(t), abs=1e-9)
        assert p.units_cancelled_pp(t) == pytest.approx(
            (p.charge_admin_fund_pp(t) + p.charge_policy_fee_pp(t)
             + p.withdrawals_pp(t) + p.charge_risk_pp(t)) / p.unit_price(t), rel=1e-12)
        rolled = ((p.av_pp(t) + p.prem_to_av_pp(t)) * (1.0 + p.fund_return_net_mth(t))
                  - p.charge_admin_fund_pp(t) - p.charge_policy_fee_pp(t)
                  - p.withdrawals_pp(t) - p.charge_risk_pp(t))
        assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(rolled, abs=1e-8)
    assert p.check_units_roll_fwd() is True and p.check_av_roll_fwd() is True
    assert p.units_bought_pp(0) == pytest.approx(1.62, rel=1e-12)  # premium in advance
    # The opening price is its own cells: on a 0-based frame there is no t = -1 to read.
    assert p.unit_price_open(0) == p.unit_price_init() == 100.0
    assert p.unit_price_open(1) == p.unit_price(0)


def test_the_frame_closes_and_publishes_both_signs_of_the_net_flow(de_frv_anchor):
    """The in-force roll-forward, the eighteen columns in the notes' order, both signs.

    Everyone who starts a month dies, surrenders, matures or is still there at the start of
    the next, and ``result_fund()`` publishes the *Standmitteilung* state vector beside it.
    """
    p = de_frv_anchor
    n = p.proj_len()
    for t in (0, 60, 239, 358, 359):
        assert p.pols_if(t) == pytest.approx(
            p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t) + p.pols_if(t + 1),
            abs=1e-12)
    assert p.check_pols_roll_fwd() is True
    assert p.pols_if(0) == p.pols_if_init() == 1.0
    assert p.pols_if_at(0, "AFT_DEATH") == pytest.approx(
        p.pols_if(0) * (1.0 - p.mort_rate_mth(0)), rel=1e-15)
    assert p.pols_if_at(0, "AFT_DECR") == pytest.approx(p.pols_if(1), rel=1e-15)
    assert p.pols_if_at(n - 1, "AFT_DECR") == pytest.approx(
        p.pols_maturity(n - 1), rel=1e-15)
    assert p.pols_if(n) == 0.0

    df = p.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "prem_to_av", "charge_acq", "charge_admin_prem",
        "charge_admin_fund", "charge_policy_fee", "charge_risk", "stornoabzug",
        "withdrawals", "claims_death", "claims_lapse", "claims_maturity",
        "av_releases", "death_strain", "expenses", "commissions", "net_cf",
        "liability_cf"]
    assert list(df.index) == list(range(360)) and df.index[-1] == n - 1
    assert "claims" not in df.columns          # no subtotal beside its own parts
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-12)
    assert df["net_cf"].iloc[0] == pytest.approx(-1966.22, abs=CENT)  # new-business strain
    assert (df["net_cf"].iloc[1:120] > 0).all()
    fund = p.result_fund()
    assert list(fund.columns) == [
        "unit_price", "units_pp", "av_pp", "av_pp_bef_charge", "av_pp_aft_charge",
        "av_pp_aft_wd", "av_pp_bef_decr", "cum_prem_pp", "db_floor_pp", "nar_pp",
        "mort_rate_mth", "mort_rate_tariff_mth", "lapse_rate_mth"]
    assert (fund["mort_rate_tariff_mth"] > fund["mort_rate_mth"]).all()
    assert fund["unit_price"].is_monotonic_increasing
    # The enum accessors validate rather than propagating a typo into a lookup.
    for bad in (lambda: p.claims(0, "SURRENDER"), lambda: p.av_pp_at(0, "AFTER_CHARGE"),
                lambda: p.pols_if_at(0, "AFTER_DECR")):
        with pytest.raises(FormulaError):
            bad()


def test_the_modules_off_in_the_base_run_are_reachable(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """Base-run values, so the worked example reproduces with the machinery still there.

    Model point 8 switches on the *Ablaufmanagement* glide: a linear ramp of the **gross**
    return to 1.50 % p.a. over the last sixty months, the TER untouched.
    """
    proj = fondsgebundene_rentenversicherung.Projection
    assert proj.lapse_dyn_beta == 0.0 and proj.lapse_cap == 0.4
    assert proj.mort_be_factor == 0.75
    assert proj.mmkt_return_ann == 0.015 and proj.glide_months == 60
    p = de_frv_anchor
    assert all(p.lapse_dyn_add(t) == 0.0 for t in (0, 60, 239, 359))
    assert all(p.lapse_rate(t) == pytest.approx(
        p.lapse_rate_base(t) * p.lapse_tax_step(t), rel=1e-12) for t in (0, 60, 300))
    assert p.ablauf_flag() is False
    assert all(p.fund_return_gross_ann(t) == 0.05 for t in (0, 299, 359))
    for absent in ("surplus_rate", "bonus_rate", "ueberschuss_pp", "schlussueberschuss",
                   "rfb_rate", "surplus_units_pp"):
        assert absent not in _names(fondsgebundene_rentenversicherung), absent
    glide = proj[8]
    assert glide.ablauf_flag() is True and glide.proj_len() == 240
    assert glide.fund_return_gross_ann(179) == 0.05        # 60 months remaining
    assert glide.fund_return_gross_ann(180) == pytest.approx(
        0.05 - (0.05 - 0.015) / 60.0, rel=1e-9)
    assert glide.fund_return_gross_ann(209) == pytest.approx(0.0325, abs=5e-7)
    assert glide.fund_return_gross_ann(239) == pytest.approx(0.015, rel=1e-12)
    assert glide.fund_ter_ann(239) == pytest.approx(glide.fund_ter_ann(0), rel=1e-15)
    assert all(getattr(glide, c)() is True for c in CHECKS)
    assert proj.model.Data.model_point_table()["ablauf_flag"].sum() == 1


def test_the_zuzahlung_buys_units_and_the_teilentnahme_cancels_them(
        fondsgebundene_rentenversicherung):
    """A Zuzahlung raises the Beitragsrückgewähr base; a Teilentnahme is an owner election,
    published as ``withdrawals`` and never as a claim, settled by cancelling units at the
    closing *Anteilspreis* after the fund charges."""
    p = fondsgebundene_rentenversicherung.Projection[9]
    assert p.topup_month() == 120 and p.wd_month() == 240
    assert p.topup_pp(120) == 20000.0 and p.topup_pp(121) == 0.0
    assert p.prem_to_av_pp(120) == pytest.approx(
        p.prem_pp(120) + 20000.0 - 500.0 - 0.04 * p.prem_pp(120), rel=1e-12)
    assert p.cum_prem_pp(120) - p.cum_prem_pp(119) == pytest.approx(
        p.prem_pp(120) + 20000.0, rel=1e-12)
    assert p.av_pp_at(120, "BEF_DECR") > p.av_pp_at(119, "BEF_DECR") + 19000.0
    assert p.withdrawals_pp(240) == 15000.0 and p.withdrawals_pp(241) == 0.0
    assert p.av_pp_at(240, "AFT_WD") == pytest.approx(
        p.av_pp_at(240, "AFT_CHARGE") - 15000.0, rel=1e-12)
    assert "claims_wd" not in p.result_cf().columns
    assert p.result_cf()["withdrawals"].sum() == pytest.approx(
        15000.0 * p.pols_if(240), rel=1e-12)
    assert all(getattr(p, c)() is True for c in CHECKS)


def test_the_dynamic_lapse_module_bites_where_the_fund_is_under_water():
    """Switched on, the addition raises the lapse rate while the fund is under water.

    Off in the base run: no German calibration for a coefficient exists in this corpus.  It
    bites hardest on model point 12 and switches itself off once the fund overtakes.
    """
    model = mx.read_model(MODEL_DIR, name="FRV_DE_S_dynlapse")
    try:
        model.Projection.lapse_dyn_beta = 0.15
        model.Projection.clear_all()
        p = model.Projection[12]
        assert p.av_pp(12) < p.cum_prem_pp(12)
        assert p.lapse_dyn_add(12) == pytest.approx(
            0.15 * (1.0 - p.av_pp(12) / p.cum_prem_pp(12)), rel=1e-12)
        assert p.lapse_rate_base(12) < p.lapse_rate(12) <= model.Projection.lapse_cap
        assert p.check_pols_roll_fwd() is True and p.check_net_cf() is True
        last = p.proj_len() - 1
        assert p.av_pp(last) > p.cum_prem_pp(last)
        assert p.lapse_dyn_add(last) == 0.0
    finally:
        model.close()


def test_the_two_derived_tables_are_anchored_where_the_notes_need_them(
        fondsgebundene_rentenversicherung):
    """The mortality proxy at q(37) = 0.00080 and the factor derivation at age 67.

    The conventions suite owns the ``provenance`` rule; product-specific is the anchor a
    substitute must reproduce for the worked example to close, and that DAV 2008 T and
    DAV 2004 R are cited by name and never shipped.
    """
    import pandas as pd

    assert CSV_FILES == {q.name for q in INPUT_DIR.iterdir() if q.suffix == ".csv"}
    mort = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col="age")
    assert list(mort.index) == list(range(18, 101))
    assert float(mort.loc[37, "qx_tariff"]) == 0.00080
    assert float(mort.loc[38, "qx_tariff"]) / float(mort.loc[37, "qx_tariff"]) == (
        pytest.approx(1.10, rel=1e-9))
    assert mort["qx_tariff"].max() <= 1.0
    assert all(v.startswith("[std]") and "DAV 2008 T" in v for v in mort["provenance"])
    factors = pd.read_csv(INPUT_DIR / "rentenfaktor_table.csv")
    assert set(factors["factor_id"]) == {"std_2026", "rich_current"}
    assert all("derived not observed" in v or "guaranteed factor as std_2026" in v
               for v in factors["provenance"])
    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="charge_id")
    assert "Hoechstzillmersatz" in charges.loc["std_gross", "provenance"]
    lapse = pd.read_csv(INPUT_DIR / "lapse_table.csv", index_col="policy_year")
    assert [float(lapse.loc[y, "lapse_rate"]) for y in (1, 6, 11, 13)] == [
        0.06, 0.03, 0.02, 0.03]
    assert all("Stornoquote" in v for v in lapse["provenance"])   # none established
    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert len(points) == 13 and points.loc[1, "policy_id"] == "DE-FRV-0001"
    assert "provenance" not in points.columns      # a model point is a configuration
    # The chassis vocabulary this model shares with frlib's UC_FR_S, and its symbol map.
    shared = {"units_pp", "units_bought_pp", "units_cancelled_pp", "unit_price", "av_pp",
              "av_pp_at", "av_at", "prem_to_av_pp", "prem_to_av", "nar_pp", "db_pp",
              "withdrawals", "av_releases", "death_strain"}
    assert shared <= _names(fondsgebundene_rentenversicherung)


