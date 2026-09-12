"""Golden and product tests for RILA_US_S.

The golden values are the worked example in
products/registered_index_linked_annuity/technical-notes.md ("Worked example"), which
prices the anchor cell M60 / $100,000 single premium / one 6-year option / S&P 500 price
return / 10% buffer / Cap crediting at a declared 100% cap, on flat market inputs of
r = 4.00%, q = 2.00%, sigma = 20.00% and an index normalized to I_s = 100.  They are
hard-coded here rather than pickled so that a reviewer can compare them against the notes
by eye.

The notes' table has six rows and fourteen columns and every cell of it is asserted
below, together with the trace beneath the table: the option budget, the fixed leg's
opening value and equivalent accretion yield, the cost of the 100 bp rate rise, the
counterfactual interim values without it, and the proportional-withdrawal arithmetic.

Rows 0, A1 and A2 run on model point 1 (Scenario A, index 100 -> 120 -> 140); rows B1,
B2 and B3 on model point 2 (Scenario B, index 100 -> 80 -> 75, with the illustrative
$8,000 withdrawal at the term midpoint).

``t`` is the 0-based month index: month ``t`` runs from time ``t`` to time ``t + 1`` and is
valued at its **end**, so a contract instant sits on the row of the month it closes.  The
notes' year column is contract time, and the model row is one less than the month end it
names: the 3-year point is time 36, the end of month 35, and the 6-year Term End Date is
time 72, the end of month 71.  Row 0 of the notes' table is the Term Start Date itself, the
*opening* of month 0, which is an instant and not a projected month; it is asserted by
``test_worked_example_row_0_at_the_term_start_instant``.

The notes' "Known modeling pitfalls" section is a test list in disguise; there is one
test per entry below.
"""
import math
import re

import modelx as mx
import pytest

from us_registry import LIB

MODEL_PATH = LIB / "products/registered_index_linked_annuity/RILA_US_S"

# Half a cent, plus a hair, for money the notes display to 2 d.p.
CENT = 0.006

# The notes compute row B3 from the cent-rounded row B2: they print
# "90,566.38 x 0.85 = 76,981.42" where full precision gives 76,981.4260.  This tolerance
# covers that and nothing larger.
ROUNDED = 0.01

RATE = 5e-7             # rates the notes display to six decimals


# ---------------------------------------------------------------------------
# Worked example, "Worked example" table.
# label: (point_id, t, timing, index, R, fixed proxy, ATM call, -OTM call, -OTM put,
#         deriv proxy, trading cost, interim value, investment amount)
#
# The Interim value column is printed as "-" in rows 0, A2 and B3 because the interim
# value is undefined at term start and term end [R6]; the parenthesised Strategy Value
# there is what the model returns, and that is what is asserted.
WORKED_EXAMPLE = {
    "A1": (1, 35, "BEF_ROLL", 120.0,  0.20,  92280.78, 29145.94, -2182.94,  -2726.33,
           24236.66, 34.06, 116483.39, 100000.00),
    "B1": (2, 35, "BEF_ROLL",  80.0, -0.20,  92280.78,  5778.47,   -85.24, -13151.88,
           -7458.66, 19.02,  84803.11, 100000.00),
    "B2": (2, 35, "AFT_WD",    80.0, -0.20,  83575.37,  5233.35,   -77.20, -11911.19,
           -6755.04, 17.22,  76803.11,  90566.38),
    "A2": (1, 71, "BEF_ROLL", 140.0,  0.40, 100000.00, 40000.00,     0.00,      0.00,
           40000.00,  0.00, 140000.00, 140000.00),
    "B3": (2, 71, "BEF_ROLL",  75.0, -0.25,  90566.38,     0.00,     0.00, -13584.96,
           -13584.96, 0.00,  76981.42,  76981.42),
}

# The notes' row 0: the Term Start Date, tau = T.  Not a projected month - it is the
# opening instant of month 0 - so the model reproduces it by pricing the replicating
# portfolio at tau = T under the term-start market state.
TERM_START = {
    "index": 100.0,
    "notional": 100000.00,
    "fixed_proxy": 89936.81,
    "ATM_CALL": 21567.95,
    "OTM_CALL": -3344.55,
    "OTM_PUT": -8160.20,
    "deriv_proxy": 10063.19,
    "trading_cost": 33.07,
    "strategy_value": 100000.00,
}

# Trace beneath the table.
BETA = 0.100632                 # Pi(100, 6) = 0.215679 - 0.033445 - 0.081602
OPT_BUDGET = 10063.19           # beta x 100,000
FIXED_LEG_OPEN = 89936.81       # 100,000 (1 - beta)
FIXED_LEG_YIELD = 0.017834      # equivalent geometric accretion yield
NGE_SPREAD = 0.0222             # 4.00% - 1.7834%
BUDGET_AT_MIDTERM = 5031.60     # B = beta x 100,000 x 3/6
FIXED_LEG_UNADJUSTED = 94968.40  # IA - B
MVA_COST = 2687.62              # the cost of the 100 bp rise
IV_A1_NO_RATE_MOVE = 119171.01
IV_B1_NO_RATE_MOVE = 87490.73
WD_RATIO = 0.094336             # 8,000 / 84,803.11
IA_REDUCTION = 9433.62          # notional lost
IA_REDUCTION_EXCESS = 1433.62   # notional lost less cash received

# The notes' second labelled verification, in "Withdrawal charge, free amount, and
# allocation": the [S2] prospectus example.  Model point 15 reproduces it end to end.
S2_CHARGE = {
    "premium": 100000.00,
    "account_value": 80000.00,      # at the start of contract year 6
    "free_amount": 8000.00,         # 10% of the Account Value at the anniversary
    "chargeable": 72000.00,
    "charge_rate": 0.03,            # wc(5)
    "charge": 2160.00,
    "cash_value": 77840.00,
}

README = (LIB / "products/registered_index_linked_annuity/model.md").read_text(
    encoding="utf-8")


def _flat(text):
    """Collapse whitespace, so a phrase split across a hard-wrapped line still matches."""
    return re.sub(r"\s+", " ", text)


@pytest.fixture(scope="module")
def rila():
    """The RILA_US_S model, closed after the module finishes."""
    model = mx.read_model(MODEL_PATH)
    yield model
    model.close()


@pytest.fixture(scope="module")
def anchor(rila):
    """Model point 1 - the worked example's anchor cell on Scenario A."""
    return rila.Projection[1]


@pytest.fixture(scope="module")
def scenario_b(rila):
    """Model point 2 - the same anchor cell on Scenario B, with the $8,000 withdrawal."""
    return rila.Projection[2]


def _point(rila, point_id):
    return rila.Projection[point_id]


# ---------------------------------------------------------------------------
# The worked example, every row and every column

@pytest.mark.parametrize("label", sorted(WORKED_EXAMPLE))
def test_worked_example_row(rila, label):
    """Every cell of the five projected rows of the notes' fourteen-column table; row 0 is
    the term-start instant and is asserted separately."""
    (pid, t, timing, index, perf, fixed, atm, otmc, otmp,
     deriv, tcost, value, notional) = WORKED_EXAMPLE[label]
    p = _point(rila, pid)

    assert p.index_level(t) == pytest.approx(index, abs=1e-9)
    assert p.index_perf(t) == pytest.approx(perf, abs=RATE)
    assert p.fixed_proxy_pp(t, timing) == pytest.approx(fixed, abs=CENT)
    assert p.opt_component_pp(t, "ATM_CALL", timing) == pytest.approx(atm, abs=CENT)
    assert p.opt_component_pp(t, "OTM_CALL", timing) == pytest.approx(otmc, abs=CENT)
    assert p.opt_component_pp(t, "OTM_PUT", timing) == pytest.approx(otmp, abs=CENT)
    assert p.deriv_proxy_pp(t, timing) == pytest.approx(deriv, abs=CENT)
    assert p.trading_cost_pp(t, timing) == pytest.approx(tcost, abs=CENT)
    assert p.interim_value_pp_at(t, timing) == pytest.approx(value, abs=ROUNDED)
    assert p.inv_amt_pp_at(t, timing) == pytest.approx(notional, abs=ROUNDED)


def test_worked_example_tau_column(anchor):
    """The notes' year column: the 3-year point closes month 35, the term end month 71."""
    assert anchor.term_start_month(0) == 0          # the term opens with month 0
    assert anchor.tau(35) == 3.0
    assert anchor.tau(71) == 0.0
    assert anchor.is_term_end(71) is True
    assert anchor.is_term_end(35) is False
    # tau = T belongs to the opening instant of month 0, which is not a projected month:
    # by the end of month 0 one month of the term has already run.
    assert anchor.tau(0) == pytest.approx((12 * 6 - 1) / 12.0, rel=1e-15)


def test_option_budget_and_fixed_leg(anchor):
    """beta = 10.0632%, so the budget is $10,063.19 and the fixed leg opens at $89,936.81."""
    assert anchor.opt_budget(0) == pytest.approx(BETA, abs=5e-7)
    assert anchor.opt_budget(0) * anchor.premium_pp() == pytest.approx(
        OPT_BUDGET, abs=CENT)
    assert anchor.premium_pp() * (1 - anchor.opt_budget(0)) == pytest.approx(
        FIXED_LEG_OPEN, abs=CENT)


def test_option_budget_decomposes_as_the_notes_print_it(anchor):
    """Pi(100, 6) = 0.215679 - 0.033445 - 0.081602 = 0.100632."""
    legs = {leg: anchor.opt_component(0, leg, 100.0, 6.0, "TERM_START")
            for leg in anchor.opt_legs()}
    assert legs["ATM_CALL"] == pytest.approx(0.215679, abs=5e-7)
    assert legs["OTM_CALL"] == pytest.approx(-0.033445, abs=5e-7)
    assert legs["OTM_PUT"] == pytest.approx(-0.081602, abs=5e-7)
    assert sum(legs.values()) == pytest.approx(BETA, abs=5e-7)


def test_fixed_leg_yield_and_the_implied_nge_spread(anchor):
    """The fixed leg accretes at 1.7834%, a 2.22% spread against the 4.00% market rate.

    That spread is the [std] input to the NGE cap-solve rule, read back out of the
    snapshot cap - which is why the model computes it rather than only storing it.
    """
    assert anchor.fixed_leg_yield(0) == pytest.approx(FIXED_LEG_YIELD, abs=5e-6)
    assert anchor.nge_spread_implied(0) == pytest.approx(NGE_SPREAD, abs=5e-5)


def test_worked_example_row_0_at_the_term_start_instant(anchor):
    """The notes' row 0, and with it AG 54's Index Strategy Base requirement.

    ``tau = T`` is the **opening** of month 0, not a projected month: by the end of month 0
    a month of the term has run.  The same instant recurs at every renewal Term Start Date
    and never had a row either, so the model reproduces it the way it always computed the
    option budget - pricing the replicating portfolio at ``tau = T`` under the term-start
    market state.  ``F + D = 100,000.00`` exactly there, and the interim value is
    *undefined* [R6]: the contractual value is the Strategy Value, the Investment Amount.
    """
    ia = anchor.inv_amt_basis_pp(0)                 # the notional entering month 0
    i_s = anchor.index_at_term_start(0)
    term = float(anchor.term_years())
    assert ia == TERM_START["notional"]
    assert i_s == TERM_START["index"]

    for leg in anchor.opt_legs():
        value = ia * anchor.opt_component(0, leg, i_s, term, "TERM_START")
        assert value == pytest.approx(TERM_START[leg], abs=CENT)

    deriv = ia * anchor.opt_budget(0)               # D = beta x IA at tau = T
    fixed = ia * (1.0 - anchor.opt_budget(0))       # B = beta x IA and the MVA factor is 1
    assert deriv == pytest.approx(TERM_START["deriv_proxy"], abs=CENT)
    assert fixed == pytest.approx(TERM_START["fixed_proxy"], abs=CENT)
    assert fixed + deriv == pytest.approx(TERM_START["strategy_value"], abs=1e-9)

    tcost = ia * anchor.trading_cost_rate * anchor.opt_portfolio_abs(
        0, i_s, term, "TERM_START")
    assert tcost == pytest.approx(TERM_START["trading_cost"], abs=CENT)


def test_midterm_amortization_and_the_mva_factor(anchor, scenario_b):
    """B = 5,031.60, the unadjusted fixed leg is 94,968.40, and the rise costs 2,687.62.

    Note a display slip in the notes: they print the factor as 0.971690, but every dollar
    figure derived from it requires (1.04/1.05)^3 = 0.9716998.  The model reproduces the
    dollars, and this test pins the factor that actually produces them.
    """
    assert anchor.budget_amort_pp(35) == pytest.approx(BUDGET_AT_MIDTERM, abs=CENT)
    unadjusted = anchor.inv_amt_basis_pp(35) - anchor.budget_amort_pp(35)
    assert unadjusted == pytest.approx(FIXED_LEG_UNADJUSTED, abs=CENT)
    assert anchor.mva_factor(35) == pytest.approx((1.04 / 1.05) ** 3, rel=1e-12)
    assert anchor.mva_factor(35) == pytest.approx(0.9716998, abs=5e-8)
    assert unadjusted - anchor.fixed_proxy_pp(35) == pytest.approx(MVA_COST, abs=CENT)
    # The same fixed leg serves both scenarios: it does not depend on the index.
    assert scenario_b.fixed_proxy_pp(35) == pytest.approx(
        anchor.fixed_proxy_pp(35), abs=1e-9)


def test_interim_values_without_the_rate_move(anchor, scenario_b):
    """Without the 100 bp rise the interim values would be 119,171.01 and 87,490.73."""
    for p, expected in ((anchor, IV_A1_NO_RATE_MOVE), (scenario_b, IV_B1_NO_RATE_MOVE)):
        no_move = (p.inv_amt_basis_pp(35) - p.budget_amort_pp(35)
                   + p.deriv_proxy_pp(35) - p.trading_cost_pp(35))
        assert no_move == pytest.approx(expected, abs=CENT)


def test_the_short_put_subtracts_even_when_the_index_is_up(anchor):
    """Row A1: the index is up 20% and the short out-of-the-money put still costs 2,726.33.

    The prospectus warns that "the out-of-the-money put will almost always reduce the
    Interim Value, even when the current Index Value ... is higher than the Index Value on
    the Term Start Date" [S2].
    """
    assert anchor.index_perf(35) > 0.0
    assert anchor.opt_component_pp(35, "OTM_PUT") == pytest.approx(-2726.33, abs=CENT)


def test_the_proportional_withdrawal_rule(scenario_b):
    """Row B2: $8,000 of cash costs $9,433.62 of notional, an excess of $1,433.62.

    ``IA(t+) = IA(t-) (1 - G/V(t-))`` with ratio 8,000 / 84,803.11 = 9.4336%.  The excess
    is exactly ``G (IA/V - 1)``, and it is positive whenever the interim value is below
    the notional - the asymmetry the prospectus states directly [S2].
    """
    v_before = scenario_b.interim_value_pp_at(35, "BEF_WD")
    ia_before = scenario_b.inv_amt_pp_at(35, "BEF_WD")
    wd = scenario_b.wd_pp(35)
    assert wd == 8000.00
    assert v_before == pytest.approx(84803.11, abs=CENT)
    ratio = wd / v_before
    assert ratio == pytest.approx(WD_RATIO, abs=5e-7)

    ia_after = scenario_b.inv_amt_pp(35)
    assert ia_before - ia_after == pytest.approx(IA_REDUCTION, abs=CENT)
    assert ia_before - ia_after - wd == pytest.approx(IA_REDUCTION_EXCESS, abs=CENT)
    assert ia_before - ia_after - wd == pytest.approx(
        wd * (ia_before / v_before - 1.0), rel=1e-12)


def test_homogeneity_the_interim_value_falls_by_exactly_the_cash(scenario_b):
    """Every component scales by one factor, so V falls by exactly the $8,000 withdrawn.

    This is the notes' "losing homogeneity" pitfall.  If ``B_k(t)`` were frozen at the
    term-start notional rather than scaled with the current ``IA_k(t)``, the contract
    would silently gain or lose value on every withdrawal.
    """
    v_before = scenario_b.interim_value_pp_at(35, "BEF_WD")
    v_after = scenario_b.interim_value_pp_at(35, "AFT_WD")
    assert v_before - v_after == pytest.approx(8000.00, rel=1e-12)

    scale = scenario_b.inv_amt_pp(35) / scenario_b.inv_amt_pp_at(35, "BEF_WD")
    for leg in scenario_b.opt_legs():
        assert scenario_b.opt_component_pp(35, leg, "AFT_WD") == pytest.approx(
            scenario_b.opt_component_pp(35, leg, "BEF_ROLL") * scale, rel=1e-12)
    for cells in ("fixed_proxy_pp", "deriv_proxy_pp", "trading_cost_pp",
                  "budget_amort_pp"):
        before = getattr(scenario_b, cells)(35, "BEF_ROLL")
        after = getattr(scenario_b, cells)(35, "AFT_WD")
        assert after == pytest.approx(before * scale, rel=1e-12)


def test_the_withdrawal_bite_persists_to_term_end(scenario_b):
    """Row B3: 90,566.38 x 0.85 = 76,981.42 - the proportional reduction does not heal."""
    assert scenario_b.credit_rate_term(71) == pytest.approx(-0.15, abs=RATE)
    assert scenario_b.inv_amt_pp_at(71, "BEF_ROLL") == pytest.approx(
        76981.42, abs=ROUNDED)


def test_rop_falls_in_the_same_proportion_as_the_account_value(scenario_b):
    """The return-of-premium base is reduced proportionally on withdrawal [S1][S2]."""
    av_before = scenario_b.av_pp_at(35, "BEF_WD")
    ratio = 1.0 - scenario_b.wd_pp(35) / av_before
    assert scenario_b.rop_pp(35) == pytest.approx(
        scenario_b.rop_pp(34) * ratio, rel=1e-12)
    assert scenario_b.rop_pp(35) == pytest.approx(90566.38, abs=CENT)
    # And the guarantee is in the money exactly here: AV is depressed, ROP is not.
    assert scenario_b.death_ben_pp(35) == pytest.approx(scenario_b.rop_pp(35), rel=1e-12)
    assert scenario_b.death_ben_pp(35) > scenario_b.av_pp(35)


# ---------------------------------------------------------------------------
# The notes' verification identity, for every crediting type

@pytest.mark.parametrize("point_id", [1, 2, 4, 5, 6, 11, 12])
def test_term_end_identity_holds_for_every_crediting_type(rila, point_id):
    """At tau = 0 every replicating portfolio collapses to ``g``, so V = IA(1 + g).

    The notes ask for this as a unit test explicitly, and name the ways it can break: a
    wrong strike set, a wrong notional convention, a flipped buffer sign, or a trading
    cost provision left switched on at term end.
    """
    p = _point(rila, point_id)
    ends = [t for t in range(p.proj_len()) if p.is_term_end(t)]
    assert ends
    for t in ends:
        assert p.check_term_end_identity_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.trading_cost_pp(t) == 0.0
        assert p.iv_ratio(t) == 1.0
    # the same check with no argument, which is how the library calls it
    assert p.check_term_end_identity() is True


def test_the_term_end_identity_is_the_crediting_formula(rila):
    """Pi at tau = 0 equals ``g`` for Cap, Step, Edge and Floor alike."""
    for point_id in (1, 4, 5, 6, 12):
        p = _point(rila, point_id)
        t = next(t for t in range(p.proj_len()) if p.is_term_end(t))
        pi = p.opt_portfolio(t, p.index_level(t), 0.0, "CURRENT")
        assert pi == pytest.approx(p.credit_rate_term(t), abs=1e-12)


# ---------------------------------------------------------------------------
# Crediting formulas

def test_cap_applies_to_the_whole_term_return(anchor):
    """"We do not apply the Cap ... annually on a 3-year or 6-year Term Index Option" [S5]."""
    assert anchor.index_perf(71) == pytest.approx(0.40, abs=RATE)
    assert anchor.cap_rate(71) == 1.00
    assert anchor.credit_rate_term(71) == pytest.approx(0.40, abs=RATE)
    # not an annualized 40% applied six times, and not (1.40)^(1/6) - 1 compounded
    assert anchor.credit_rate_term(71) != pytest.approx(1.40 ** (1 / 6) - 1, abs=1e-3)


def test_the_buffer_branch_can_never_credit_a_gain(scenario_b):
    """"The Performance Rate can never be greater than zero if Index Performance is
    negative" [S1]: g = min(0, R + b), so -25% under a 10% buffer credits -15%."""
    assert scenario_b.index_perf(71) == pytest.approx(-0.25, abs=RATE)
    assert scenario_b.credit_rate_term(71) == pytest.approx(-0.15, abs=RATE)
    assert scenario_b.credit_rate_at(71, 1.0) <= 0.0


def test_step_and_edge_discontinuities_are_not_smoothed(rila):
    """A Step design pays the full step at R = 0.00% and zero just below [S2][S4].

    The binary option is what makes the interim value track that; smoothing it breaks the
    term-end identity.
    """
    step = _point(rila, 4)
    t = next(t for t in range(step.proj_len()) if step.is_term_end(t))
    assert step.index_perf(t) == pytest.approx(0.0, abs=1e-12)
    assert step.credit_rate_term(t) == pytest.approx(0.08, abs=RATE)   # full step at R = 0
    # the binary itself, at expiry
    assert step.bs_binary_call(100.0, 100.0, 0.0, 0.04, 0.02, 0.20) == 1.0
    assert step.bs_binary_call(99.99, 100.0, 0.0, 0.04, 0.02, 0.20) == 0.0

    edge = _point(rila, 5)
    # The Edge design triggers at -b rather than 0, and pays R + b below it.
    assert edge.credit_rate_at(11, 1.0) == pytest.approx(0.06, abs=RATE)   # R = 0
    t_down = 35                                                            # R = -20%
    assert edge.index_perf(t_down) == pytest.approx(-0.20, abs=RATE)
    assert edge.credit_rate_term(t_down) == pytest.approx(-0.10, abs=RATE)


def test_floor_needs_four_options_not_three(rila):
    """The floor design buys back an out-of-the-money put so the short exposure stops [S5]."""
    p = _point(rila, 6)
    assert p.opt_legs() == ("ATM_CALL", "OTM_CALL", "ATM_PUT", "FLOOR_PUT")
    assert p.credit_rate_term(35) == pytest.approx(-0.10, abs=RATE)   # R = -20%, f = 10%
    # the bought-back put is the only positive-signed put in the set
    assert p.opt_component(35, "FLOOR_PUT", 80.0, 0.5, "CURRENT") > 0.0
    assert p.opt_component(35, "ATM_PUT", 80.0, 0.5, "CURRENT") < 0.0


def test_an_uncapped_option_values_the_otm_call_at_zero(rila, anchor):
    """"the value of the out-of-the-money call will be zero if a Cap Rate Shield Option is
    uncapped" [S2]."""
    p = _point(rila, 12)
    assert p.is_uncapped() is True
    assert math.isinf(p.cap_rate(0))
    assert p.opt_component(35, "OTM_CALL", 120.0, 3.0, "CURRENT") == 0.0
    # at expiry the uncapped design credits the whole index return; the capped one stops
    assert p.opt_portfolio(35, 300.0, 0.0, "CURRENT") == pytest.approx(2.00, abs=1e-12)
    assert anchor.opt_portfolio(35, 300.0, 0.0, "CURRENT") == pytest.approx(
        1.00, abs=1e-12)
    # the buffer branch is unaffected by the absence of a cap
    assert p.credit_rate_term(71) == pytest.approx(-0.15, abs=RATE)


def test_participation_above_100_percent_restrikes_the_short_call(rila):
    """Cap + PR: ``PR [C(I,I_s) - C(I,I_s(1+c/PR))] - P(I,I_s(1-b))``, all over I_s [S4]."""
    p = _point(rila, 11)
    assert p.participation() == 1.10
    assert p.buffer() == 0.20
    assert p.cap_rate(0) == 0.60
    # the short call strike is I_s(1 + c/PR), not I_s(1 + c)
    i_s, tau_ = p.index_at_term_start(35), p.tau(35)
    expected = -1.10 * p.bs_call(
        p.index_level(35), i_s * (1 + 0.60 / 1.10), tau_,
        p.risk_free(35), p.div_yield(35), p.impl_vol(35)) / i_s
    assert p.opt_component(35, "OTM_CALL", p.index_level(35), tau_,
                           "CURRENT") == pytest.approx(expected, rel=1e-12)


def test_participation_of_one_recovers_the_plain_cap_portfolio(anchor):
    """At PR = 1 the notes' two Cap rows are the same portfolio, so one branch serves both."""
    assert anchor.participation() == 1.0
    i_s, tau_ = 100.0, 3.0
    plain = (anchor.bs_call(120.0, i_s, tau_, 0.04, 0.02, 0.20)
             - anchor.bs_call(120.0, i_s * 2.0, tau_, 0.04, 0.02, 0.20)
             - anchor.bs_put(120.0, i_s * 0.9, tau_, 0.04, 0.02, 0.20)) / i_s
    assert anchor.opt_portfolio(35, 120.0, 3.0, "CURRENT") == pytest.approx(
        plain, rel=1e-12)


# ---------------------------------------------------------------------------
# Interim value families and the amortization switch

def test_the_pre_ag54_engine_reproduces_its_own_worked_example(rila):
    """[S1]: $50,000, Shield 10, a 10% Cap, index 500 -> 600 at day 183 -> $52,500.

    The accrued cap is 10% x 183/365 = 5%, so the Performance Rate is 5%.  On a monthly
    grid the sixth month end of twelve is exactly half the term - the end of month 5 - so
    the model reproduces the source figure to the cent.  This is the era-mixing contrast:
    the pre-AG 54 design uses no option pricing at all and both engines are live in
    in-force blocks.
    """
    p = _point(rila, 9)
    assert p.iv_family() == "legacy"
    assert p.premium_pp() == 50000.0
    assert p.index_at_term_start(0) == 500.0
    assert p.index_level(5) == 600.0
    assert p.index_perf(5) == pytest.approx(0.20, abs=RATE)
    assert p.credit_rate_accrued(5) == pytest.approx(0.05, abs=RATE)
    assert p.interim_value_pp_at(5, "BEF_ROLL") == pytest.approx(52500.00, abs=CENT)
    # and it carries no derivative proxy or trading cost at all
    assert p.deriv_proxy_pp(5) == 0.0
    assert p.trading_cost_pp(5) == 0.0


def test_family_c_is_family_a_with_the_mva_factor_set_to_one(rila):
    """The notes' non-obvious equivalence: (a) and (c) differ only in the fixed leg's mark.

    Expanding (c) gives ``V = IA[1 + Pi(I(t), tau) - beta tau/T]``, which is family (a)
    with the interest-rate adjustment factor set to 1 - and family (c) carries no trading
    cost either [S5].
    """
    delta = _point(rila, 8)
    assert delta.iv_family() == "delta"
    assert delta.trading_cost_factor(35) == 0.0
    expected = (1.0 - delta.budget_amort_factor(35)) + delta.deriv_proxy_factor(35)
    assert delta.iv_factor(35) == pytest.approx(expected, rel=1e-12)
    # the same model point priced under family (a) would carry the MVA factor instead
    assert delta.fixed_proxy_factor(35) == pytest.approx(
        (1.0 - delta.budget_amort_factor(35)), rel=1e-12)
    assert delta.mva_factor(35) != pytest.approx(1.0, abs=1e-6)


def test_family_b_discounts_the_full_notional_and_rebates_expenses(rila):
    """Equitable discounts the **whole** Segment Investment and adds the always-positive
    Cap Calculation Factor, which declines linearly to zero at term end [S4][S6]."""
    p = _point(rila, 7)
    assert p.iv_family() == "notional"
    assert p.fixed_proxy_factor(35) == pytest.approx(
        (1 + p.risk_free(35) + p.iv_credit_spread) ** (-p.tau(35)), rel=1e-12)
    assert p.cap_calc_factor(35) > 0.0
    assert p.cap_calc_factor(35) == pytest.approx(
        p.iv_expense_rate * p.tau(35) / p.term_years(), rel=1e-12)
    assert p.cap_calc_factor(71) == 0.0
    assert p.trading_cost_factor(35) == 0.0


def test_the_amortization_switch_changes_the_middle_and_not_the_ends(rila):
    """Straight-line [S2] against updated time to expiry [S3] - one insurer needs both."""
    straight, updated = _point(rila, 1), _point(rila, 10)
    assert straight.amort_rule() == "straight_line"
    assert updated.amort_rule() == "updated_expiry"
    # identical at both boundaries: at the term-start instant both reduce to beta, and at
    # term end both are zero. The term-start instant is not a row after the merge, so the
    # updated-expiry rule is evaluated there directly, at tau = T.
    i_s, term = updated.index_at_term_start(0), float(updated.term_years())
    assert updated.opt_portfolio(0, i_s, term, "TERM_START") == pytest.approx(
        straight.opt_budget(0), rel=1e-12)
    assert straight.budget_amort_factor(71) == updated.budget_amort_factor(71) == 0.0
    # and different in between
    assert straight.budget_amort_factor(35) != pytest.approx(
        updated.budget_amort_factor(35), rel=1e-6)


def test_the_nge_cap_solve_hits_its_target(rila):
    """At a renewal Term Start Date the declared cap solves ``Pi(c) = beta_target(T)``."""
    p = _point(rila, 13)
    assert p.nge_reset() is True
    assert p.cap_rate(0) == 1.00                       # the issue cap is contractual
    solved = p.cap_rate(72)                            # the first renewal term
    assert 0.0 < solved < 1.00
    assert p.opt_budget(72) == pytest.approx(p.opt_budget_target(), abs=1e-9)
    assert solved >= p.guar_min_rate("CAP")
    # the base run holds the snapshot instead
    assert _point(rila, 1).cap_rate(72) == 1.00


# ---------------------------------------------------------------------------
# Contract mechanics: charges, free amount, transfer period, roll

def test_the_two_readings_of_the_contract_year(anchor):
    """A month-end valuation reads the contract year two ways, and each cells takes its own.

    ``duration(t) = t // 12`` is lifelib's 0-based duration: the complete contract years at
    the **start** of month t, hence the year the whole month lies inside.  A rate applied
    **across** the month - the mortality rate ``q_m(t) = 1 - (1 - q_x)^(1/12)``, the
    maintenance expense incurred over it - belongs to that year.
    ``duration_eom(t) = (t + 1) // 12`` is the notes' ``cy`` at the month **end**, where
    the month's transactions settle: it is what the withdrawal charge is keyed on, and what
    the charge-expiry lapse shock follows so the two move in the same month.  Keying the
    attained age on ``duration_eom`` would charge month 11 - which is inside contract year
    1 - at ``q_(x+1)``, leaving only eleven months at the issue age.
    """
    assert anchor.age_at_entry() == 60
    assert [anchor.duration(t) for t in (0, 1, 10, 11, 12, 23, 24)] == [
        0, 0, 0, 0, 1, 1, 2]
    assert anchor.duration_eom(11) == 1 and anchor.duration(11) == 0

    # twelve months at each attained age, the step falling after the anniversary
    assert (anchor.age(10), anchor.age(11), anchor.age(12)) == (60, 60, 61)
    assert len([t for t in range(anchor.proj_len()) if anchor.age(t) == 60]) == 12
    assert anchor.mort_rate(11) == anchor.mort_rate(0)
    assert anchor.mort_rate(12) > anchor.mort_rate(11)

    # and the expense step goes with it: 60/12 x 1.025^(y-1), y = duration(t) + 1
    assert anchor.inflation_factor(11) == 1.0
    assert anchor.inflation_factor(12) == pytest.approx(1.025, rel=1e-12)
    assert anchor.expenses(11) == pytest.approx(
        (60 / 12) * anchor.pols_if(11), rel=1e-12)

    # the contractual boundaries keep the month-end reading, as the notes define them
    assert anchor.surr_charge_rate(23) == 0.06         # cy_end(23) = 2, not 1
    assert anchor.surr_charge_rate(59) == 0.03         # wc(5), the [S2] example's rate
    # the anniversary at time 12 closes month 11, so that is where the base is snapshotted
    assert anchor.free_wd_base(11) == pytest.approx(
        anchor.av_pp_at(11, "BEF_WD"), rel=1e-12)
    assert anchor.policy_year(71) == 7 and anchor.lapse_rate_sc_mult(71) == 3.0


def test_the_withdrawal_charge_schedule(anchor):
    """7, 7, 6, 5, 4, 3, 0 per cent by **complete** contract years [S1][S2]."""
    expected = [0.07, 0.07, 0.06, 0.05, 0.04, 0.03, 0.00]
    for cy, rate in enumerate(expected):
        assert anchor.surr_charge_rate(12 * cy) == pytest.approx(rate, abs=1e-12)
        assert anchor.duration_eom(12 * cy) == cy
    assert anchor.surr_charge_rate(12 * 8) == 0.0      # runs out, stays out


def test_the_free_withdrawal_amount(scenario_b):
    """Zero in contract year 1; thereafter 10% of the Account Value at the prior
    anniversary, non-cumulative [S1][S2]."""
    assert scenario_b.free_wd_allow(0) == 0.0
    assert scenario_b.free_wd_allow(5) == 0.0          # still contract year 1
    assert scenario_b.free_wd_avail(35) == pytest.approx(
        0.10 * scenario_b.av_pp_at(35, "BEF_WD"), rel=1e-12)
    # the notes' worked $8,000 sits inside it, so no charge is incurred
    assert scenario_b.wd_pp(35) == 8000.0
    assert scenario_b.free_wd_avail(35) > 8000.0
    assert scenario_b.wd_charge_pp(35) == 0.0
    assert scenario_b.wd_payment_pp(35) == 8000.0
    # and nothing carries across the next anniversary
    assert scenario_b.free_wd_remain(35) == pytest.approx(
        scenario_b.free_wd_avail(35) - 8000.0, rel=1e-12)
    assert scenario_b.free_wd_avail(47) == pytest.approx(
        scenario_b.free_wd_allow(47), rel=1e-12)


def test_the_charge_is_not_grossed_up(rila):
    """The charge is deducted from the amount withdrawn, not added to it [S1][S2].

    Model point 14 takes $20,000 at the second anniversary - time 24, which is the end of
    month 23 - well above the free amount, so the charge is live; contrast [S4], where "any
    amount deducted to pay withdrawal charges is also subject to that same withdrawal
    charge percentage".
    """
    p = _point(rila, 14)
    t = 23
    assert p.wd_pp(t) == 20000.0
    assert p.wd_excess_pp(t) > 0.0
    assert p.wd_excess_pp(t) == pytest.approx(
        p.wd_pp(t) - p.free_wd_avail(t), rel=1e-12)
    assert p.surr_charge_rate(t) == 0.06                 # complete contract year 2
    assert p.wd_charge_pp(t) == pytest.approx(
        p.surr_charge_rate(t) * p.wd_excess_pp(t), rel=1e-12)
    assert p.wd_payment_pp(t) == pytest.approx(
        p.wd_pp(t) - p.wd_charge_pp(t), rel=1e-12)
    # the gross amount leaves the contract; only the net is a cash flow
    assert p.wd_payment_pp(t) < p.wd_pp(t)
    assert p.rop_pp(t) == pytest.approx(
        p.rop_pp(t - 1) * (1 - p.wd_pp(t) / p.av_pp_at(t, "BEF_WD")), rel=1e-12)


def test_the_surrender_value_composition(anchor):
    """CSV(t) = AV(t) - wc(cy) max(0, AV(t) - FW(t)) [S1][S2].

    A wiring check only - it re-expands the composition from the same cells, so it holds
    by construction.  The numbers themselves are pinned by
    :func:`test_the_prospectus_withdrawal_charge_example` below.
    """
    for t in (0, 12, 35, 59, 71, 99):
        expected = anchor.av_pp(t) - anchor.surr_charge_rate(t) * max(
            0.0, anchor.av_pp(t) - anchor.free_wd_remain(t))
        assert anchor.surr_value_pp(t) == pytest.approx(expected, rel=1e-12)
    # after the charge schedule runs out the surrender value is the account value
    assert anchor.surr_value_pp(71) == pytest.approx(anchor.av_pp(71), rel=1e-12)


def test_the_prospectus_withdrawal_charge_example(rila):
    """[S2]: an $80,000 Account Value at the start of contract year 6 pays $77,840.

    The notes' second explicitly labelled verification, beside the interim-value table:
    "$100,000 payment, $80,000 Account Value at the start of contract year 6, full
    withdrawal -> FW = $8,000, chargeable $72,000, wc(5) = 3%, charge $2,160, cash value
    $77,840."

    Model point 15 exists to put that Account Value on the table.  It runs the pre-AG 54
    engine on a scenario whose index level makes the accrued crediting rate exactly -20%
    at time 60, so ``av_pp(59)`` is $80,000 to a rounding error of 3e-6 and every figure
    of the example - the free amount as 10% of the anniversary Account Value, the
    chargeable balance, ``wc(5)``, the charge and the cash surrender value - comes out of
    the model's own cells rather than being re-derived from them.
    """
    p = _point(rila, 15)
    t = 59                          # closes at the fifth anniversary, opening contract year 6
    assert p.premium_pp() == S2_CHARGE["premium"]
    assert p.duration_eom(t) == 5 and p.policy_year(t) == 6
    assert p.av_pp(t) == pytest.approx(S2_CHARGE["account_value"], abs=CENT)
    assert p.free_wd_allow(t) == pytest.approx(S2_CHARGE["free_amount"], abs=CENT)
    assert p.free_wd_remain(t) == pytest.approx(S2_CHARGE["free_amount"], abs=CENT)
    assert p.surr_excess_pp(t) == pytest.approx(S2_CHARGE["chargeable"], abs=CENT)
    assert p.surr_charge_rate(t) == S2_CHARGE["charge_rate"]
    assert p.surr_charge_pp(t) == pytest.approx(S2_CHARGE["charge"], abs=CENT)
    assert p.surr_value_pp(t) == pytest.approx(S2_CHARGE["cash_value"], abs=CENT)
    # and that is what a surrender in that month actually pays: the charge is retained,
    # not grossed up, so the benefit is the Account Value less exactly the charge
    assert p.claim_pp(t, "LAPSE") == pytest.approx(S2_CHARGE["cash_value"], abs=CENT)
    assert p.av_pp(t) - p.claim_pp(t, "LAPSE") == pytest.approx(
        S2_CHARGE["charge"], abs=CENT)


def test_the_transfer_period_sets_the_value_equal_to_the_investment_amount(anchor):
    """"V = IA during it" [S1][S2] - which is why surrenders concentrate there."""
    assert anchor.iv_ratio(71) == 1.0
    assert anchor.interim_value_pp_at(71, "BEF_ROLL") == pytest.approx(
        anchor.inv_amt_pp_at(71, "BEF_ROLL"), rel=1e-12)
    assert anchor.lapse_iv_mult(71) == 1.0             # no moneyness suppression there
    assert anchor.term_end_lapse_rate(71) == 0.10      # the withdrawal charge is zero
    assert anchor.term_end_lapse_rate(35) == 0.0       # not a Term End Date


def test_the_term_end_roll_split(anchor):
    """80% renew into the same option, 5% into another, 15% to the Fixed Account **[std]**."""
    assert anchor.roll_share("OPTION") == pytest.approx(0.85, rel=1e-12)
    assert anchor.roll_share("FIXED") == pytest.approx(0.15, rel=1e-12)
    assert anchor.roll_share("HOLDING") == 0.0
    credited = anchor.inv_amt_pp_at(71, "BEF_ROLL")
    assert anchor.inv_amt_pp_at(71, "BEF_WD") == pytest.approx(
        credited * 0.85, rel=1e-12)
    assert anchor.roll_to_acct_pp(71, "FIXED") == pytest.approx(
        credited * 0.15, rel=1e-12)
    # the Fixed Account is empty until the first Term End Date and non-empty after it
    assert anchor.fixed_acct_pp(70) == 0.0
    assert anchor.fixed_acct_pp(71) > 0.0
    assert anchor.holding_acct_pp(71) == 0.0
    # and the Account Value is the sum of the three buckets
    assert anchor.av_pp(71) == pytest.approx(
        anchor.interim_value_pp_at(71, "AFT_WD") + anchor.fixed_acct_pp(71)
        + anchor.holding_acct_pp(71), rel=1e-12)


def test_the_general_accounts_accrue_at_the_declared_rate_floored_at_one_percent(anchor):
    """FA(t) = FA(t-1) (1 + max(i_declared, 0.01))^(1/12) [S1][S2]."""
    assert anchor.acct_rate() == 0.03
    assert anchor.fixed_acct_pp(72) == pytest.approx(
        (anchor.fixed_acct_pp(71)) * 1.03 ** (1 / 12), rel=1e-12)


def test_the_death_benefit_bands(rila, scenario_b):
    """max(AV, ROP) for issue ages 80 and under; AV alone for 81 and above [S2]."""
    assert scenario_b.age_at_entry() == 60
    assert scenario_b.death_ben_pp(35) == pytest.approx(
        max(scenario_b.av_pp(35), scenario_b.rop_pp(35)), rel=1e-12)

    old = _point(rila, 12)
    assert old.age_at_entry() == 81
    t = next(t for t in range(old.proj_len()) if old.rop_pp(t) > old.av_pp(t))
    assert old.death_ben_pp(t) == pytest.approx(old.av_pp(t), rel=1e-12)
    assert old.death_ben_pp(t) < old.rop_pp(t)         # the guarantee does not apply


# ---------------------------------------------------------------------------
# Behaviour

def test_the_moneyness_suppression(scenario_b):
    """M_iv(t) = min(1, max(0.25, V/IA))^2 **[std]**, so 0.85 carries 0.72."""
    assert scenario_b.lapse_iv_mult(35) == pytest.approx(
        min(1.0, max(0.25, scenario_b.iv_ratio(35))) ** 2, rel=1e-12)
    assert scenario_b.iv_ratio(35) < 1.0               # the option leg is out of the money
    assert scenario_b.lapse_iv_mult(35) < 1.0          # so surrender is suppressed
    assert scenario_b.lapse_iv_mult(35) >= 0.25 ** 2   # floored
    assert scenario_b.lapse_iv_mult(71) == 1.0         # never above par


def test_the_charge_expiry_shock_lands_in_contract_year_7(anchor):
    """M_sc(7) = 3.0 **[std]**: contract year 7 is the first with a zero withdrawal charge
    [S1][S2] and, on a 6-year chassis, the first after a Term End Date.

    The size is the scalar Reference ``lapse_shock_mult`` and the year is derived from the
    withdrawal charge schedule by ``lapse_shock_year()``, so the shock cannot drift away
    from the charge whose expiry causes it.
    """
    assert anchor.policy_year(71) == 7
    assert anchor.surr_charge_rate(71) == 0.0
    assert anchor.lapse_shock_mult == 3.0               # the Reference carries the size
    assert anchor.lapse_shock_year() == 7               # the schedule carries the year
    assert anchor.lapse_rate_sc_mult(59) == 1.0         # contract year 6
    assert anchor.lapse_rate_sc_mult(71) == 3.0
    assert anchor.lapse_rate_sc_mult(83) == 1.0         # contract year 8, the ultimate
    assert anchor.lapse_rate_base(71) == 0.02
    assert anchor.lapse_rate_base(83) == 0.06


def test_the_total_surrender_rate_is_capped_at_fifty_percent(anchor):
    """w_annual = min(0.50, w_base x M_sc x M_iv) **[std cap]**.

    ``lapse_rate`` is the **annual** rate and ``lapse_rate_mth`` the monthly one, the pair
    matching ``mort_rate`` / ``mort_rate_mth``.
    """
    for t in (0, 35, 71, 83, 199):
        assert 0.0 <= anchor.lapse_rate(t) <= 0.50
        assert anchor.lapse_rate(t) == pytest.approx(
            min(0.50, anchor.lapse_rate_base(t) * anchor.lapse_rate_sc_mult(t)
                * anchor.lapse_iv_mult(t)), rel=1e-12)
        assert anchor.lapse_rate_mth(t) == pytest.approx(
            1 - (1 - anchor.lapse_rate(t)) ** (1 / 12), rel=1e-12)
    # the monthly rate is the one the decrement chain reads
    assert anchor.pols_if_at(71, "BEF_TERM_SURR") == pytest.approx(
        anchor.pols_if_at(71, "BEF_LAPSE") * (1 - anchor.lapse_rate_mth(71)), rel=1e-12)


def test_the_worked_example_and_the_behavioural_withdrawal_rule_disagree(rila):
    """A divergence in the notes, shipped rather than resolved.

    The notes' base behavioural rule takes 2% of Account Value at every anniversary from
    contract year 2, but their worked example holds the Investment Amount at exactly
    $100,000 to the term midpoint with the illustrative $8,000 as the only withdrawal.
    Both cannot hold.  Model points 1 and 2 pin the worked example with
    ``wd_rate_ann = 0``; model point 3 is otherwise identical and runs the behavioural
    rule, so neither reading can be closed off silently.
    """
    pinned, behavioural = _point(rila, 1), _point(rila, 3)
    assert pinned.wd_rate_ann() == 0.0
    assert behavioural.wd_rate_ann() == 0.02
    assert pinned.wd_pp(11) == 0.0
    assert pinned.inv_amt_pp(34) == 100000.0
    assert behavioural.wd_pp(11) == pytest.approx(
        0.02 * behavioural.av_pp_at(11, "BEF_WD"), rel=1e-12)
    assert behavioural.wd_pp(11) > 0.0
    assert behavioural.inv_amt_pp(34) < 100000.0
    # and the behavioural rule never incurs a charge: it is capped at the free amount.
    # The anniversary at time 12y closes month 12y - 1, which is where it is taken.
    assert all(behavioural.wd_charge_pp(12 * y - 1) == 0.0 for y in range(1, 10))
    assert behavioural.wd_pp(5) == 0.0                 # nothing in contract year 1


# ---------------------------------------------------------------------------
# Roll-forwards, shape, and every model point

def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + surrenders + forced annuitizations."""
    for t in range(anchor.proj_len()):
        assert anchor.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-14)
    assert anchor.check_pols_roll_fwd() is True
    n = anchor.proj_len()
    assert anchor.pols_if(n - 1) > 0.0                 # the maturity month is populated
    assert anchor.pols_if(n) == 0.0                    # and empty past the Maturity Date
    assert anchor.pols_maturity(n - 1) > 0.0
    assert all(anchor.pols_maturity(t) == 0.0 for t in range(n - 1))


def test_pols_if_is_the_start_of_period_count_and_weights_its_own_row(anchor):
    """The library-wide convention: ``pols_if(t)`` opens month t and weights its cash flows.

    ``pols_if(0) == pols_if_init()``, exactly as in ``Term_US_S``, and the count at the
    month end survives as ``pols_if_at(t, "AFT_DECR")``.  The reconciliation this buys is
    that the ``pols_if`` column of ``result_cf()`` divides the cash flows on the same row:
    before the ruling the printed in-force was the end-of-month count while the row was
    weighted by the opening one.
    """
    assert anchor.pols_if(0) == anchor.pols_if_init()
    assert anchor.pols_if_at(0, "BEF_DECR") == anchor.pols_if(0)
    # month 0 is excluded from the expense identity only because it also carries the
    # acquisition charge, which is not a per-month maintenance amount
    for t in (1, 11, 35, 71, 199):
        # the end-of-month count is one step ahead of the start-of-month one
        assert anchor.pols_if_at(t, "AFT_DECR") == pytest.approx(
            anchor.pols_if(t + 1), rel=1e-15)
        # and the row's own cash flows divide by the row's own in-force
        assert anchor.expenses(t) / (
            (60 / 12) * anchor.inflation_factor(t)) == pytest.approx(
            anchor.pols_if(t), rel=1e-12)
    assert anchor.premiums(0) / anchor.premium_pp() == pytest.approx(
        anchor.pols_if(0), rel=1e-15)
    df = anchor.result_cf()
    for t in (1, 23, 119):
        assert df.loc[t, "expenses"] / (
            (60 / 12) * anchor.inflation_factor(t)) == pytest.approx(
            df.loc[t, "pols_if"], rel=1e-12)


def test_the_withdrawal_payment_divides_by_the_same_in_force(scenario_b):
    """``withdrawals(t) / wd_payment_pp(t) == pols_if(t)`` - the ruling's own identity."""
    t = 35
    assert scenario_b.wd_payment_pp(t) > 0.0
    assert scenario_b.withdrawals(t) / scenario_b.wd_payment_pp(t) == pytest.approx(
        scenario_b.pols_if(t), rel=1e-15)


def test_account_value_rollforward_closes(anchor, scenario_b):
    """AV(t) - AV(t-1) = premium - withdrawals + investment return - AV released."""
    for p in (anchor, scenario_b):
        for t in range(p.proj_len()):
            assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)
        assert p.check_av_roll_fwd() is True


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(anchor.proj_len()):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


def test_the_maturity_date_rule(rila):
    """The later of the anniversary after age 90 and ten years from issue [S2]."""
    assert _point(rila, 1).policy_term() == 30        # issue age 60
    assert _point(rila, 1).proj_len() == 360
    assert _point(rila, 4).policy_term() == 15        # issue age 75
    assert _point(rila, 7).policy_term() == 10        # issue age 80: the ten-year floor
    assert _point(rila, 12).policy_term() == 10       # issue age 81: still ten years
    p = _point(rila, 1)
    # The last projected month is t = proj_len() - 1, the twelfth month of contract year
    # 30.  The owner is 89 ANB throughout it and attains 90 at its end, which is the
    # Maturity Date itself: age(t) is the age *during* month t, not at its end.
    last = p.proj_len() - 1
    assert p.age(last) == 89
    assert p.age(last - 12) == 88
    assert p.age_at_entry() + p.policy_term() == 90
    assert p.claim_pp(last, "MATURITY") == pytest.approx(p.av_pp(last), rel=1e-12)


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(anchor.proj_len()))
    assert df.index.name == "t"
    assert set(df.columns) == {
        "pols_if", "premiums", "withdrawals", "claims_death", "claims_lapse",
        "claims_maturity", "expenses", "premium_taxes", "net_cf",
    }
    # The Issue Date opens month 0 rather than standing as a row of its own, so row 0
    # carries the premium and the acquisition expense *plus* its own maintenance expense
    # and decrements.
    assert df.loc[0, "premiums"] == 100000.0
    assert df.loc[0, "expenses"] == pytest.approx(
        0.06 * 100000 + 200 + 60 / 12, abs=CENT)
    assert df.loc[0, "net_cf"] == pytest.approx(
        100000.0 - df.loc[0, "expenses"] - df.loc[0, "claims_death"]
        - df.loc[0, "claims_lapse"], abs=CENT)
    assert df.loc[0, "net_cf"] == pytest.approx(93592.53, abs=CENT)

    # the cash flow columns sum to net_cf under the income-positive sign convention:
    # premiums less every other flow.  pols_if is the in-force weight, not a cash flow.
    outgo = [c for c in df.columns if c not in ("pols_if", "premiums", "net_cf")]
    rebuilt = df["premiums"] - df[outgo].sum(axis=1)
    assert (rebuilt - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


def test_result_tables_have_the_worked_examples_columns(anchor):
    """result_iv() is the notes' own table, one row per month."""
    iv = anchor.result_iv()
    for column in ("index_level", "index_perf", "tau", "fixed_proxy_pp", "atm_call",
                   "otm_call", "otm_put", "deriv_proxy_pp", "trading_cost_pp",
                   "interim_value_pp", "inv_amt_pp"):
        assert column in iv.columns
    assert iv.loc[35, "interim_value_pp"] == pytest.approx(116483.39, abs=ROUNDED)
    pols = anchor.result_pols()
    assert set(pols.columns) == {
        "pols_if", "pols_death", "pols_lapse", "pols_lapse_term",
        "pols_maturity", "pols_if_aft_decr"}
    # pols_if opens the month, pols_if_aft_decr closes it before the maturity annuitization
    assert pols.loc[11, "pols_if_aft_decr"] == pytest.approx(
        pols.loc[12, "pols_if"], rel=1e-15)
    assert "surr_value_pp" in anchor.result_av().columns


def test_price_return_not_total_return(anchor):
    """All representative indices are price return, so the dividend yield is live [S1][S2].

    Omitting it overprices every call and inflates interim values throughout.
    """
    assert anchor.div_yield(0) == 0.02
    with_div = anchor.bs_call(100.0, 100.0, 6.0, 0.04, 0.02, 0.20)
    without = anchor.bs_call(100.0, 100.0, 6.0, 0.04, 0.00, 0.20)
    assert without > with_div
    assert anchor.opt_budget(0) < (
        without - anchor.bs_call(100.0, 200.0, 6.0, 0.04, 0.00, 0.20)
        - anchor.bs_put(100.0, 90.0, 6.0, 0.04, 0.00, 0.20)) / 100.0


def test_the_discount_rate_reference_is_the_cmt_series(anchor):
    """The Market Value Rate is the CMT at the term's maturity [S2], read at two dates."""
    assert anchor.mvr(0) == 0.04                     # month 0's month end, time 1
    assert anchor.mvr(35) == 0.05                    # the 3-year point, time 36
    assert anchor.mvr_at_term_start(35) == 0.04      # locked on the Term Start Date
    assert anchor.mvr_at_term_start(72) == anchor.mvr(71)   # re-locked at renewal
    assert anchor.mva_factor(0) == 1.0               # the rate has not moved yet


def test_the_trading_cost_is_a_free_parameter_on_a_stated_base(anchor):
    """kappa x IA x sum of |per-unit option values| **[std]**, zero at term end."""
    assert anchor.trading_cost_rate == 0.001
    gross = sum(abs(anchor.opt_component(
        0, leg, anchor.index_level(0), anchor.tau(0), "CURRENT"))
        for leg in anchor.opt_legs())
    assert anchor.trading_cost_pp(0) == pytest.approx(
        0.001 * 100000.0 * gross, rel=1e-12)
    # the $33.07 the notes' opening row shows is the term-start instant, pinned by
    # test_worked_example_row_0_at_the_term_start_instant
    assert anchor.trading_cost_factor(71) == 0.0


def test_the_interim_value_is_not_floored(scenario_b):
    """"Flooring the interim value at zero, or at the notional, is not implementing the
    contract" [S2]."""
    assert scenario_b.interim_value_pp_at(35, "BEF_ROLL") < scenario_b.inv_amt_pp_at(
        35, "BEF_ROLL")
    assert scenario_b.deriv_proxy_pp(35) < 0.0        # the derivative proxy is negative
    assert scenario_b.iv_ratio(35) < 1.0
    # and the Account Value follows it down rather than being held at the notional
    assert scenario_b.av_pp(35) < scenario_b.premium_pp()


# ---------------------------------------------------------------------------
# The documentation a reader holds the notes against


def _symbol_table(rila):
    """The Projection docstring's notes-symbol -> cells table as ``{symbol: cells}``.

    A reStructuredText simple table: the ``===`` border above the header fixes the column
    widths, and a row whose first column is blank continues the row above it.
    """
    lines = rila.Projection.doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    border = lines[head - 1]
    assert set(border) == {"=", " "}, "the symbol table has no border above its header"
    starts, pos = [], 0
    for width in [len(part) for part in border.split("  ")]:
        starts.append(pos)
        pos += width + 2
    rows = []
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        symbol = line[starts[0]:starts[1]].strip()
        cells = line[starts[1]:starts[2]].strip()
        if symbol:
            rows.append([symbol, cells])
        elif cells and rows:
            rows[-1][1] += " " + cells
    return dict(rows)


def test_the_symbol_table_maps_every_notes_symbol_the_model_implements(rila):
    """The mapping table is the deliverable; a symbol the model implements must appear.

    These rows were all missing at one point: a reader holding the notes beside the model
    could find no cells for the free-amount state variable, the NGE cap-solve inputs, the
    Cap Calculation Factor's expense rate and its discount spread, the declared account
    rate, the pre-AG 54 accrued rate, family (c)'s DailyAdjustment, or the declared rates
    the model point carries as distinct from the floored rates in force.
    """
    table = _symbol_table(rila)
    required = [
        ("FW_used(y)", "free_wd_remain"),
        ("y_e, spread", "earned_rate"),
        ("y_e, spread", "nge_spread"),
        ("E_0", "iv_expense_rate"),
        ("rate(t), family (b)", "iv_credit_spread"),
        ("i_declared", "acct_rate"),
        ("AccruedCapRate", "credit_rate_accrued"),
        ("DailyAdjustment(t)", "fixed_proxy_factor"),
        ("DailyAdjustment(t)", "deriv_proxy_factor"),
        ("c, s, e (model point)", "declared_cap"),
        ("c, s, e (model point)", "declared_step"),
        ("c, s, e (model point)", "declared_edge"),
        ("1.025^(y-1)", "inflation_factor"),
        ("cy_end(t) = floor((t+1)/12)", "duration_eom"),
    ]
    for symbol, cells in required:
        assert symbol in table, f"the symbol table has no row for {symbol}"
        assert cells in table[symbol], f"{symbol} does not map to {cells}"

    # and every name the table promises must actually be there to be found
    names = set(rila.Projection.cells) | set(rila.Projection.refs)
    for symbol, cells in table.items():
        for ident in re.findall(r"[A-Za-z_]\w*", re.sub(r"\([^)]*\)", "", cells)):
            assert ident in names, f"{symbol} maps to {ident}, which does not exist"


def test_the_documented_timing_arguments_are_the_ones_the_cells_accept(rila, anchor):
    """The symbol table, the timing rubric and the code must name the same literals.

    The table row for ``pols_if_at`` once read ``BEF_TERM`` where the code and the rubric
    below it read ``BEF_TERM_SURR``, so a reader copying the literal out of the table got
    a ``ValueError``.
    """
    doc = rila.Projection.doc
    for cells, arg_of in (("pols_if_at", anchor.pols_if_at),
                          ("inv_amt_pp_at", anchor.inv_amt_pp_at)):
        row = next(line for line in doc.splitlines()
                   if f"{cells}(t, timing)" in line)
        timings = row.split()[-1].split("/")
        assert len(timings) == 4
        for timing in timings:
            assert f'``"{timing}"``' in doc, f"{timing} is not in the timing rubric"
            arg_of(24, timing)                      # must not raise
    assert "BEF_TERM_SURR" in doc and "BEF_TERM/" not in doc


def test_the_family_b_free_parameters_are_disclosed_as_std(rila):
    """``iv_credit_spread`` and ``iv_expense_rate`` are invented numbers, and say so.

    No source quantifies either: [S4] says only that family (b) discounts at an
    investment-grade rate above swap rates, and gives the Cap Calculation Factor as a
    dollar illustration.  Both move the family (b) interim value, so neither may travel
    unmarked - BUILD_SPEC's rule that every number not from a source carries **[std]**.
    """
    p = _point(rila, 7)
    assert p.iv_family() == "notional"
    assert p.iv_credit_spread == 0.01
    assert p.iv_expense_rate == 0.001
    assert p.fixed_proxy_factor(35) < 1.0              # the spread is live in the factor
    assert p.cap_calc_factor(35) > 0.0

    spread_doc = _flat(rila.Projection.cells["fixed_proxy_factor"].doc)
    assert "iv_credit_spread" in spread_doc and "**[std]**" in spread_doc
    expense_doc = _flat(rila.Projection.cells["cap_calc_factor"].doc)
    assert "iv_expense_rate" in expense_doc and "**[std]**" in expense_doc

    model_doc = _flat(rila.doc)
    section = _flat(README.split("## Standardizations used")[1].split("\n## ")[0])
    for name in ("iv_credit_spread", "iv_expense_rate"):
        assert name in model_doc, f"{name} is not in the model docstring's sourced list"
        assert name in section, f"{name} is not in the README's standardizations list"


def test_invalid_arguments_raise(anchor):
    """Every string-argument cells rejects an unknown value, as CashValue_SE does."""
    for call in (lambda: anchor.inv_amt_pp_at(1, "NOPE"),
                 lambda: anchor.interim_value_pp_at(1, "NOPE"),
                 lambda: anchor.av_pp_at(1, "NOPE"),
                 lambda: anchor.pols_if_at(1, "NOPE"),
                 lambda: anchor.claim_pp(1, "NOPE"),
                 lambda: anchor.pols_decr(1, "NOPE"),
                 lambda: anchor.roll_share("NOPE"),
                 lambda: anchor.guar_min_rate("NOPE"),
                 lambda: anchor.iv_notional_pp(1, "NOPE"),
                 lambda: anchor.opt_component(1, "NOPE", 100.0, 1.0, "CURRENT"),
                 lambda: anchor.opt_component(1, "ATM_CALL", 100.0, 1.0, "NOPE"),
                 lambda: anchor.wd_bucket_value_pp(1, "NOPE")):
        with pytest.raises(Exception):
            call()
