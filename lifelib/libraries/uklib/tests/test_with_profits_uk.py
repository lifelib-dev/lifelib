"""Golden and structural tests for WP_UK_S.

The golden values are the worked example in
products/with_profits/technical-notes.md ("Worked example"), which projects a
unitised with-profits bond in force at duration 5 — asset share GBP 30,000, face value
GBP 27,602.02, smoothed payout GBP 29,500, unit price 1.104081 on 25,000 units, AMC 1%
p.a., guarantee charge 0.10% p.a., q(60) = 0.5% p.a., death uplift 1.01, smoothing cap
10% year on year — through one policy year on **two scenarios**: a fund return of +7%
p.a. and one of -15% p.a.  They are hard-coded here rather than pickled so that a
reviewer can compare them against the notes by eye.

``t`` is 0-based and counts policy **months**, as everywhere in the library: the cell is
in force at duration 5, so its frame opens at ``t = proj_start() = 60`` and the policy
year the worked example projects is ``t = 60 … 71``, the sixth.  The state it carries in
is the *opening* value of month 60 — ``asset_share_at(60, "BEF_PREM")``,
``smoothed_payout_open(60)``, ``guar_benefit_open(60)`` — not a row of its own.  The
declaration falls at the end of ``t = 71``, so the closing golden values are that
month's.

Tolerances follow the precision the notes display: money to the penny.

Beyond the worked example this module asserts the product facts the notes call out,
because each is a way an implementation can look right and be wrong:

* the grid is monthly but the **declaration is annual** — the guarantee moves in
  declaration months and nowhere else, and compounding the annual bonus rate monthly
  gives a model whose roll-forwards all close and whose guarantee is an order of
  magnitude too large a decade later;
* the asset share is a **state variable**, not a cash flow, and its step order —
  charges, then the shareholder transfer, then the mortality charge on the balance
  *after* the transfer — is contractual discipline;
* a declared bonus **hardens** into the guarantee permanently, at a cost to the payout
  of exactly a ninth of what it hardens;
* the smoothing cap is applied **before** the corridor, and its monthly bounds are the
  twelfth roots of the notes' year-on-year band;
* a final bonus and a market value reduction are **never** simultaneous, and the MVR is
  bounded by the excess of the unit value over the underlying asset value;
* the MVR-free window is the guarantee-date **month**, not its policy year; and
* the guarantee-date encashment is gated on the guarantee actually being in the money,
  because otherwise it invents anti-selection where there is none.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from uk_registry import MODELS, LIB

PENNY = 0.01          # the notes display money to 2 d.p. and truncate, not round

MODEL_DIR = LIB / MODELS["WP_UK_S"][0]

T0 = 60               # the first month of the policy year the worked example projects
T = 71                # its last month, and the declaration month
GUAR_MTH = 119        # the 10th anniversary: the guarantee-date month, 12 x 10 - 1

# The notes' two-scenario table, keyed by the fixture that carries the scenario.  The
# aggregate rows are sums over the twelve months t = 60 .. 71; everything else is the
# closing month t = 71.
WORKED_EXAMPLE = {
    "up": dict(
        fund_return=0.07, fund_return_mth=0.00565415,
        amc_year=311.10, guar_charge_year=30.98, mort_charge_year=0.00,
        aft_charge=31747.19,
        bonus=0.02, unit_price=1.126163, guar_benefit=28154.07,
        cost_of_bonus=552.04, transfer=61.34, aft_st=31685.86, mort_charge=0.00,
        asset_share=31685.86, capped=31685.86, smoothed=31685.86,
        final_bonus=3531.79, mvr=0.00, mvr_bound=0.00,
        pay_guarantee=31685.86, pay_surrender=31685.86, pay_death=32002.72,
        cost_guarantee=0.00, cost_surrender=0.00,
    ),
    "down": dict(
        fund_return=-0.15, fund_return_mth=-0.01345195,
        amc_year=274.93, guar_charge_year=27.38, mort_charge_year=4.60,
        aft_charge=25216.50,
        bonus=0.01, unit_price=1.115122, guar_benefit=27878.05,
        cost_of_bonus=276.02, transfer=30.67, aft_st=25185.83, mort_charge=1.24,
        asset_share=25184.59, capped=26846.96, smoothed=26846.96,
        final_bonus=0.00, mvr=1031.08, mvr_bound=2693.46,
        pay_guarantee=27878.05, pay_surrender=26846.96, pay_death=28156.83,
        cost_guarantee=2693.46, cost_surrender=1662.37,
    ),
}

# State carried into t = T0, from the model point: the opening balances of that month,
# the values at the end of the fifth policy year.
AS_OPEN = 30000.00
S_OPEN = 29500.00
FV_OPEN = 27602.02

CWP_MATURITY = 29018.91      # 20,000 x 1.015^25, the notes' endowment check


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_monthly_rates(with_profits, key):
    """The annual assumptions, converted, and compounding back to themselves.

    Every rate the notes quote is annual, and twelve months of its effective monthly
    equivalent must rebuild it exactly.  That identity is what keeps the change of grid
    from moving the basis.
    """
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.fund_return() == pytest.approx(e["fund_return"])
    assert p.fund_return_mth() == pytest.approx(e["fund_return_mth"], abs=5e-9)
    assert (1 + p.fund_return_mth()) ** 12 == pytest.approx(
        1 + p.fund_return(), rel=1e-14)
    assert (1 - p.amc_rate_mth()) ** 12 == pytest.approx(1 - 0.01, rel=1e-14)
    assert (1 - p.guar_charge_rate_mth(T0)) ** 12 == pytest.approx(
        1 - 0.001, rel=1e-14)
    assert (1 - p.mort_rate_mth(T0)) ** 12 == pytest.approx(
        1 - p.mort_rate(T0), rel=1e-14)
    assert (1 - p.surr_rate_mth(T0)) ** 12 == pytest.approx(
        1 - p.surr_rate(T0), rel=1e-14)
    assert p.smooth_cap_dn_mth() ** 12 == pytest.approx(0.90, rel=1e-14)
    assert p.smooth_cap_up_mth() ** 12 == pytest.approx(1.10, rel=1e-14)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_asset_share_steps(with_profits, key):
    """The recursion one step at a time, both scenarios, to the displayed precision.

    The opening balances belong to month 60 and the closing steps to month 71; the three
    charge rows are the twelve-month totals the notes print.
    """
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    months = range(T0, T + 1)
    assert p.asset_share_at(T0, "BEF_PREM") == pytest.approx(AS_OPEN, abs=PENNY)
    assert p.asset_share_at(T0, "BEF_RETURN") == pytest.approx(AS_OPEN, abs=PENNY)
    amc = sum(p.asset_share_at(t, "AFT_RETURN") * p.amc_rate_mth() for t in months)
    assert amc == pytest.approx(e["amc_year"], abs=PENNY)
    assert sum(p.guar_charge_pp(t) for t in months) == pytest.approx(
        e["guar_charge_year"], abs=PENNY)
    assert sum(p.mort_charge_pp(t) for t in months) == pytest.approx(
        e["mort_charge_year"], abs=PENNY)
    assert p.asset_share_at(T, "AFT_CHARGE") == pytest.approx(e["aft_charge"], abs=PENNY)
    assert p.asset_share_at(T, "AFT_ST") == pytest.approx(e["aft_st"], abs=PENNY)
    assert p.asset_share_at(T, "AFT_MC") == pytest.approx(e["asset_share"], abs=PENNY)
    assert p.asset_share(T) == pytest.approx(e["asset_share"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_bonus_and_unit_price(with_profits, key):
    """b, Q(71) = Q(70)(1 + b) and FV(71) = U Q(71) on 25,000 units.

    The price is flat through the eleven months before the declaration and steps in the
    twelfth, which is the whole of what "an annual declaration on a monthly grid" means.
    """
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.bonus_rate(T) == pytest.approx(e["bonus"])
    assert p.bonus_rate(T0) == pytest.approx(e["bonus"])   # one rate for the year
    assert p.unit_price_init() == pytest.approx(1.104081)
    assert all(p.unit_price(t) == pytest.approx(1.104081, abs=1e-9)
               for t in range(T0, T))                      # flat for eleven months
    assert p.unit_price(T) == pytest.approx(e["unit_price"], abs=1e-6)
    assert p.units(T) == pytest.approx(25000.0)
    assert p.guar_benefit_open(T) == pytest.approx(FV_OPEN, abs=PENNY)
    assert p.guar_benefit_pp(T) == pytest.approx(e["guar_benefit"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_bonus_cost_and_shareholder_transfer(with_profits, key):
    """CB = b FV(70) on the unitised chassis, and ST = CB/9 — the 90:10 split.

    Both arise in the declaration month and are nil in the other eleven, because a cost
    arises only where a declaration does.
    """
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.cost_of_bonus_pp(T) == pytest.approx(e["cost_of_bonus"], abs=PENNY)
    assert p.cost_of_bonus_pp(T) == pytest.approx(
        p.bonus_rate(T) * p.guar_benefit_open(T), abs=PENNY)
    assert p.shareholder_transfer_pp(T) == pytest.approx(e["transfer"], abs=PENNY)
    assert p.shareholder_transfer_pp(T) == pytest.approx(p.cost_of_bonus_pp(T) / 9.0)
    assert all(p.cost_of_bonus_pp(t) == 0.0 for t in range(T0, T))
    assert all(p.shareholder_transfer_pp(t) == 0.0 for t in range(T0, T))


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_mortality_charge(with_profits, key):
    """MC = q_m x max(0, 1.01 FV - AS after ST) — monthly, so it is taken every month."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.mort_rate(T) == pytest.approx(0.005, abs=5e-9)
    assert p.mort_rate_mth(T) == pytest.approx(1 - 0.995 ** (1 / 12), abs=5e-9)
    assert p.death_guar_pp(T) == pytest.approx(1.01 * p.guar_benefit_pp(T), abs=PENNY)
    assert p.mort_charge_pp(T) == pytest.approx(e["mort_charge"], abs=PENNY)
    assert sum(p.mort_charge_pp(t) for t in range(T0, T + 1)) == pytest.approx(
        e["mort_charge_year"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_smoothing(with_profits, key):
    """The cap, then the corridor, every month.

    The cap bounds are the twelfth roots of the notes' year-on-year band, so twelve
    capped months move the payout by exactly the band.
    """
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.smoothed_payout_open(T0) == pytest.approx(S_OPEN, abs=PENNY)
    assert p.smoothed_payout_capped(T) == pytest.approx(e["capped"], abs=PENNY)
    assert p.smoothed_payout(T) == pytest.approx(e["smoothed"], abs=PENNY)
    # the payout exists in every month of the year, not only its last
    for t in range(T0, T + 1):
        lo = p.smooth_cap_dn_mth() * p.smoothed_payout_open(t)
        hi = p.smooth_cap_up_mth() * p.smoothed_payout_open(t)
        assert lo - 1e-9 <= p.smoothed_payout_capped(t) <= hi + 1e-9


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_final_bonus_and_mvr(with_profits, key):
    """FB = max(0, S - FV), MVR = min(max(0, FV - S), max(0, FV - AS))."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.final_bonus_pp(T) == pytest.approx(e["final_bonus"], abs=PENNY)
    assert p.mvr_pp(T) == pytest.approx(e["mvr"], abs=PENNY)
    bound = max(0.0, p.guar_benefit_pp(T) - p.asset_share(T))
    assert bound == pytest.approx(e["mvr_bound"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_payouts(with_profits, key):
    """All three payout bases: guarantee-date, surrender and death."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.claim_pp(T, "GUARANTEE") == pytest.approx(e["pay_guarantee"], abs=PENNY)
    assert p.claim_pp(T, "SURRENDER") == pytest.approx(e["pay_surrender"], abs=PENNY)
    assert p.claim_pp(T, "DEATH") == pytest.approx(e["pay_death"], abs=PENNY)
    assert p.claim_pp(T, "DEATH") == pytest.approx(
        1.01 * p.claim_pp(T, "GUARANTEE"), abs=PENNY)
    assert p.claim_pp(T, "MATURITY") == 0.0          # the bond is whole of life


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_smoothing_costs(with_profits, key):
    """Payout less asset share, the excess the estate absorbs on an exit."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.smoothing_cost_pp(T, "GUARANTEE") == pytest.approx(
        e["cost_guarantee"], abs=PENNY)
    assert p.smoothing_cost_pp(T, "SURRENDER") == pytest.approx(
        e["cost_surrender"], abs=PENNY)


def test_worked_example_the_down_scenario_is_the_one_to_read(uk_wp_down):
    """The notes' own checks on scenario B, and they are the point of the example.

    The asset share falls 16.1% over the policy year while the surrender payout falls
    9.0% — the smoothing cap absorbing the rest — and both scenarios land inside the
    corridor.  The cap binds in eleven of the twelve months; not the twelfth, because the
    asset share was still above the floor after one month, which is why the year's fall
    lands a little short of the 10.0% an annual step would report.
    """
    p = uk_wp_down
    assert p.asset_share(T) / AS_OPEN == pytest.approx(0.8395, abs=5e-5)
    assert p.claim_pp(T, "SURRENDER") / S_OPEN == pytest.approx(0.9101, abs=5e-5)
    assert p.claim_pp(T, "SURRENDER") / p.asset_share(T) == pytest.approx(
        1.066, abs=5e-4)
    assert p.mvr_pp(T) < max(0.0, p.guar_benefit_pp(T) - p.asset_share(T))
    capped = [p.smoothed_payout_capped(t) != p.asset_share(t) for t in range(T0, T + 1)]
    assert capped.count(True) == 11 and capped[0] is False


def test_worked_example_the_up_scenario_pays_the_asset_share(uk_wp_up):
    """Neither the cap nor the corridor binds by the year's end in A."""
    p = uk_wp_up
    assert p.smoothed_payout(T) == pytest.approx(p.asset_share(T))
    assert p.claim_pp(T, "SURRENDER") / p.asset_share(T) == pytest.approx(1.0)
    # The payout opens below the asset share, so the cap's *ceiling* holds it back for
    # the first few months - smoothing works in both directions.
    assert p.smoothed_payout(T0) < p.asset_share(T0)


def test_the_endowment_maturity_check_line(with_profits):
    """G = 20,000 x 1.015^25 = 29,018.91 at t = 299, and the guarantee bites.

    Twenty-five declarations, one at the end of each policy year — **not** three
    hundred, which is what a monthly grid produces if it compounds the annual rate every
    month.  The maturity value lands on the last projected month ``proj_len() - 1``.
    """
    p = with_profits.Projection[5]
    assert p.chassis() == "CWP_endowment"
    assert p.proj_start() == 0                    # new business
    assert p.proj_len() == 300                    # 25 policy years, t = 0 .. 299
    n = p.proj_len() - 1
    assert p.guar_benefit_pp(n) == pytest.approx(CWP_MATURITY, abs=PENNY)
    assert p.claim_pp(n, "MATURITY") == pytest.approx(CWP_MATURITY, abs=PENNY)
    # exactly 25 steps in the guarantee over 300 months
    steps = [t for t in range(p.proj_len())
             if abs(p.guar_benefit_pp(t) - p.guar_benefit_open(t)) > 1e-9]
    assert len(steps) == 25
    assert steps == [12 * y + 11 for y in range(25)]
    # The asset share falls short of the guarantee, so the estate meets the difference.
    assert p.asset_share(n) < CWP_MATURITY
    assert p.smoothing_cost_pp(n, "MATURITY") == pytest.approx(678.91, abs=0.02)


def test_the_declaration_is_annual_on_every_model_point(with_profits):
    """The grid is monthly and the discretion cycle is not.

    This is the failure mode the conversion has to be proof against: compounding the
    annual bonus rate twelve times a year leaves every roll-forward closing and the
    guarantee an order of magnitude too large a decade later.
    """
    for point_id in with_profits.Data.model_point_table().index:
        p = with_profits.Projection[point_id]
        assert p.check_declaration_is_annual() is True
        assert all(p.is_declaration_month(t) == ((t + 1) % 12 == 0)
                   for t in range(p.proj_start(), p.proj_start() + 26))
        assert all(p.declaration_month(t) == 12 * (t // 12) + 11
                   for t in range(p.proj_start(), p.proj_start() + 26))


# ---------------------------------------------------------------------------
# The asset share is a state variable, not a cash flow


def test_the_asset_share_recursion_closes(with_profits):
    """Rebuilt in one expression, the recursion reproduces the model in every month."""
    for point_id in with_profits.Data.model_point_table().index:
        assert with_profits.Projection[point_id].check_asset_share_roll_fwd() is True


def test_the_asset_share_is_published_beside_the_flows_and_not_in_them(uk_wp_up):
    """It is a shadow accumulation: visible in the result table, absent from net_cf."""
    p = uk_wp_up
    df = p.result_cf()
    assert "asset_share" in df.columns
    for t in df.index[:5]:
        assert df.at[t, "asset_share"] == pytest.approx(p.asset_share(t))
        assert p.net_cf(t) == pytest.approx(
            p.premiums(t) - p.claims(t) - p.withdrawals(t)
            - p.expenses(t) - p.shareholder_transfers(t))


def test_the_step_order_is_charges_then_transfer_then_mortality_charge(uk_wp_down):
    """The sum at risk is measured on the balance **after** the shareholder transfer.

    Measuring it on the pre-transfer balance instead would understate the charge - the
    balance is larger, so the sum at risk is smaller - which is a difference that never
    announces itself.
    """
    p = uk_wp_down
    q, dbg = p.mort_rate_mth(T), p.death_guar_pp(T)
    assert p.mort_charge_pp(T) == pytest.approx(
        q * max(0.0, dbg - p.asset_share_at(T, "AFT_ST")), abs=1e-9)
    wrong = q * max(0.0, dbg - p.asset_share_at(T, "AFT_CHARGE"))
    assert wrong < p.mort_charge_pp(T) - 0.01


def test_there_is_no_account_value_in_this_model(with_profits):
    """A product statement, not an omission: neither balance is a policyholder fund."""
    names = set(with_profits.Projection.cells) | set(with_profits.Projection.refs)
    assert not [n for n in names if n.startswith("av_pp")]
    assert "asset_share" in names and "guar_benefit_pp" in names


def test_the_timing_strings_validate(uk_wp_up):
    """A typo in a timing must fail rather than silently return the wrong step."""
    with pytest.raises(FormulaError):
        uk_wp_up.asset_share_at(T, "AFTER_RETURN")
    with pytest.raises(FormulaError):
        uk_wp_up.pols_if_at(T, "AFTER_DECR")


def test_the_asset_share_is_floored_at_zero(uk_wp_down):
    """Sixty-five years at -15% exhausts it; the payout target may not go negative.

    A negative asset share would invert the corridor, whose bounds are 0.80 AS and
    1.20 AS.  What a nil asset share means is that the guarantee is being met entirely
    by the estate.
    """
    p = uk_wp_down
    last = p.proj_len() - 1                         # the last projected month
    assert p.asset_share(last) == 0.0
    assert p.check_fund_nonneg() is True
    assert p.smoothed_payout(last) == 0.0
    assert p.guar_benefit_pp(last) > 0.0            # the guarantee is still there


# ---------------------------------------------------------------------------
# The bonus hardens, and that is what makes guarantees expensive


def test_the_unit_price_never_falls(with_profits):
    """b(t) >= 0 is a contractual floor, so a declaration is irreversible."""
    for point_id in (1, 2, 3, 4):
        p = with_profits.Projection[point_id]
        for t in range(p.proj_start(), p.proj_len()):
            assert p.bonus_rate(t) >= 0.0
            opening = (p.unit_price_init() if t == p.proj_start()
                       else p.unit_price(t - 1))
            assert p.unit_price(t) >= opening


def test_a_declaration_hardens_the_payout_at_a_cost_of_a_ninth(uk_wp_up):
    """The declaration converts final bonus into guarantee without moving the payout.

    FV rises by the full cost of bonus, 552.04, and the target payout falls by 61.34 -
    the shareholder transfer, one ninth of what was hardened.  Everything else in the
    payout is unchanged, which is why hardening is the expensive part of the product
    rather than the distribution itself.  It happens once a year, in month 71 of this
    cell's frame.
    """
    p = uk_wp_up
    hardened = p.guar_benefit_pp(T) - p.guar_benefit_open(T)
    assert hardened == pytest.approx(p.cost_of_bonus_pp(T), abs=PENNY)
    assert hardened == pytest.approx(552.04, abs=PENNY)
    # The mortality charge is nil in this scenario, so the transfer is the only cost.
    assert p.mort_charge_pp(T) == 0.0
    cost = p.asset_share_at(T, "AFT_CHARGE") - p.asset_share(T)
    assert cost == pytest.approx(p.shareholder_transfer_pp(T), abs=1e-9)
    assert cost == pytest.approx(hardened / 9.0, abs=1e-9)
    # And the payout is still the guarantee plus the final bonus, exactly.
    assert p.guar_benefit_pp(T) + p.final_bonus_pp(T) == pytest.approx(
        p.smoothed_payout(T), abs=1e-9)


def test_the_bonus_rule_is_off_and_bites_when_switched_on(with_profits):
    """The base run holds the snapshot rate; the revision module is a switch away.

    With the rule on, the +-1% gradual-change discipline binds for two years before the
    supportable rate is reached.
    """
    p = with_profits.Projection[1]
    assert with_profits.Projection.bonus_rule_on is False
    assert [p.bonus_rate(t) for t in (71, 83, 95, 107)] == [0.02] * 4

    with_profits.Projection.bonus_rule_on = True
    with_profits.Projection.clear_all()
    try:
        p = with_profits.Projection[1]
        # The rule fires once a policy year, at its declaration month, so the rate is
        # level across the twelve months that read it.
        assert p.bonus_rate(71) == pytest.approx(0.02)    # the snapshot, held
        assert all(p.bonus_rate(t) == pytest.approx(0.02) for t in range(60, 72))
        assert p.bonus_rate(83) == pytest.approx(0.03)    # +1%, capped
        assert all(p.bonus_rate(t) == pytest.approx(0.03) for t in range(72, 84))
        assert p.bonus_rate(95) == pytest.approx(0.04)    # +1%, capped
        assert p.bonus_supportable(107) > p.bonus_rate(95)
        assert p.bonus_rate(107) == pytest.approx(
            0.04 + 0.5 * (p.bonus_supportable(107) - 0.04))  # inside the cap now
    finally:
        with_profits.Projection.bonus_rule_on = False
        with_profits.Projection.clear_all()
    assert with_profits.Projection[1].bonus_rate(83) == pytest.approx(0.02)


def test_the_declared_bonus_is_floored_at_zero_and_stays_there(with_profits):
    """A declaration can be nil but never negative, however bad the supportable rate."""
    with_profits.Projection.bonus_rule_on = True
    with_profits.Projection.clear_all()
    try:
        p = with_profits.Projection[2]
        assert p.bonus_supportable(83) < -0.10            # deeply unsupportable
        assert p.bonus_rate(71) == pytest.approx(0.01)
        assert [p.bonus_rate(t) for t in (83, 95, 107, 119, 131)] == [0.0] * 5
        assert all(p.unit_price(t) == pytest.approx(p.unit_price(t - 1))
                   for t in range(84, 144))
    finally:
        with_profits.Projection.bonus_rule_on = False
        with_profits.Projection.clear_all()


def test_the_endowment_bonus_cost_is_discounted_and_the_bond_one_is_not(with_profits):
    """A reversionary addition is not payable until maturity, so it is discounted."""
    cwp = with_profits.Projection[5]
    delta = cwp.guar_benefit_pp(11) - cwp.guar_benefit_open(11)
    assert delta == pytest.approx(20000.0 * 0.015, abs=PENNY)
    # 24 years still to run at the end of the first policy year, month t = 11.
    assert cwp.cost_of_bonus_pp(11) == pytest.approx(delta / 1.04 ** 24, abs=PENNY)
    assert cwp.cost_of_bonus_pp(11) < delta
    assert cwp.cost_of_bonus_pp(10) == 0.0       # not a declaration month

    uwp = with_profits.Projection[1]
    assert uwp.cost_of_bonus_pp(T) == pytest.approx(
        uwp.guar_benefit_pp(T) - uwp.guar_benefit_open(T), abs=PENNY)


# ---------------------------------------------------------------------------
# Smoothing: the cap, then the corridor


def test_the_cap_is_skipped_when_there_is_no_previous_payout(with_profits):
    """A new-business cell has no prior payout in its first month, so the cap is off."""
    p = with_profits.Projection[5]
    assert p.proj_start() == 0
    assert p.smoothed_payout_open(0) == 0.0
    assert p.smoothed_payout_capped(0) == pytest.approx(p.asset_share(0))
    assert p.smoothed_payout(0) == pytest.approx(p.asset_share(0))


def test_the_cap_is_applied_before_the_corridor(tmp_path):
    """Order matters: corridor-then-cap collapses to the cap alone.

    In the notes' scenarios the corridor never binds after the cap, so both orders
    agree there.  Deepen the shock past a quarter and they diverge — the cap floor
    holds the payout well above the asset share and the corridor then pulls it down to
    1.20 of it.  Applying the corridor first would leave the capped figure standing,
    because an asset share is always inside its own corridor.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="WP_UK_S_order")
    try:
        table = pd.read_csv(MODEL_DIR.parent / "model_point_table.csv",
                            index_col="point_id")
        table.loc[2, "fund_return"] = -0.40
        alt = "model_point_table_crash.csv"
        table.to_csv(model.Data.input_dir() / alt)
        try:
            model.Data.model_point_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[2]
            # The cap floor binds in every month of the year once the shock is this
            # deep, so the capped figure is the opening payout run down twelve times.
            assert p.smoothed_payout_capped(T) == pytest.approx(
                p.smooth_cap_dn_mth() * p.smoothed_payout_open(T), abs=PENNY)
            assert p.smoothed_payout(T) == pytest.approx(1.20 * p.asset_share(T),
                                                         abs=PENNY)
            assert p.smoothed_payout(T) < p.smoothed_payout_capped(T)
            assert p.check_payout_corridor() is True
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_payout_stays_inside_the_corridor_on_every_model_point(with_profits):
    """80-120% of the asset share, deterministically at model-point level."""
    for point_id in with_profits.Data.model_point_table().index:
        assert with_profits.Projection[point_id].check_payout_corridor() is True


# ---------------------------------------------------------------------------
# Final bonus and MVR


def test_final_bonus_and_mvr_are_never_simultaneous(with_profits):
    """FB > 0 needs S > FV and MVR > 0 needs S < FV, so both is a contradiction."""
    for point_id in with_profits.Data.model_point_table().index:
        p = with_profits.Projection[point_id]
        assert p.check_fb_mvr_exclusive() is True
        for t in range(p.proj_start(), p.proj_len()):
            assert min(p.final_bonus_pp(t), p.mvr_pp(t)) == pytest.approx(0.0, abs=1e-9)


def test_the_mvr_stays_inside_its_contractual_bound(with_profits):
    """It may not exceed the excess of the unit value over the underlying asset value."""
    for point_id in with_profits.Data.model_point_table().index:
        assert with_profits.Projection[point_id].check_mvr_bound() is True


def test_the_mvr_is_not_applied_in_the_guarantee_date_month(uk_wp_down):
    """The scale is still positive - it is the *application* the contract waives.

    And it is the month, not the policy year: an exit in any of the other eleven months
    of the guarantee year bears the reduction like any other, which is the distinction
    the monthly grid can draw and an annual one cannot.
    """
    p = uk_wp_down
    # The guarantee date is the 10th anniversary, which ends month t = 119.
    assert p.guarantee_years() == (10,)
    assert p.policy_year(GUAR_MTH) == 10
    assert p.is_declaration_month(GUAR_MTH) is True
    assert p.is_guarantee_date(GUAR_MTH) is True
    assert p.mvr_pp(GUAR_MTH) > 0.0
    assert p.mvr_applied_pp(GUAR_MTH) == 0.0
    assert p.claim_pp(GUAR_MTH, "SURRENDER") == pytest.approx(
        p.claim_pp(GUAR_MTH, "GUARANTEE"))
    # the eleven months before it are inside the same policy year and are not the date
    for t in range(GUAR_MTH - 11, GUAR_MTH):
        assert p.policy_year(t) == 10
        assert p.is_guarantee_date(t) is False
        assert p.mvr_applied_pp(t) == pytest.approx(p.mvr_pp(t))
        assert p.claim_pp(t, "SURRENDER") < p.claim_pp(t, "GUARANTEE")


def test_the_mvr_is_not_applied_on_death(uk_wp_down):
    """A death payout is the uplifted full value on either chassis."""
    p = uk_wp_down
    assert p.mvr_applied_pp(T) > 0.0
    assert p.claim_pp(T, "DEATH") == pytest.approx(
        1.01 * (p.guar_benefit_pp(T) + p.final_bonus_pp(T)), abs=PENNY)
    assert p.claim_pp(T, "DEATH") > p.claim_pp(T, "SURRENDER")


def test_the_mvr_is_unitised_only(with_profits):
    """A conventional endowment has no units to reduce.

    The same arithmetic would collapse the surrender payout onto the asset share - the
    right answer for the wrong reason - while reporting a five-figure market value
    reduction in the first policy year, t = 0, of a 25-year endowment.
    """
    p = with_profits.Projection[5]
    assert p.guar_benefit_pp(0) > p.smoothed_payout(0) + 19000.0
    assert p.mvr_pp(0) == 0.0
    assert p.mvr_applied_pp(0) == 0.0
    assert p.claim_pp(0, "SURRENDER") == pytest.approx(p.smoothed_payout(0))
    assert all(p.mvr_pp(t) == 0.0 for t in range(p.proj_len()))


def test_the_endowment_surrender_value_is_capped_at_the_prospective_value(with_profits):
    """It targets the smoothed payout, never more than the policy is worth at maturity."""
    p = with_profits.Projection[6]
    for t in range(p.proj_start(), p.proj_len()):
        prospective = p.guar_benefit_pp(t) + p.final_bonus_pp(t)
        assert p.claim_pp(t, "SURRENDER") <= prospective + 1e-9
        assert p.claim_pp(t, "SURRENDER") == pytest.approx(
            min(p.smoothed_payout(t), prospective))


# ---------------------------------------------------------------------------
# Behaviour, where the anti-selection lives


def test_the_mvr_deterrent_suppresses_exit(uk_wp_down, uk_wp_up):
    """0.6 on the annual rate while an MVR would be applied; inert where none would be."""
    assert uk_wp_down.mvr_applied_pp(T) > 0.0
    assert uk_wp_down.mvr_deterrent(T) == 0.6
    assert uk_wp_down.surr_rate(T) == pytest.approx(0.05 * 0.6)

    assert uk_wp_up.mvr_applied_pp(T) == 0.0
    assert uk_wp_up.mvr_deterrent(T) == 1.0
    assert uk_wp_up.surr_rate(T) == pytest.approx(0.05)


def test_the_guarantee_encashment_is_dated_and_gated(uk_wp_down, uk_wp_up):
    """It falls in the guarantee-date month, and only when the guarantee is in the money.

    Two things are being asserted, and the second is the point.  The exercise is a
    **dated** one-off rather than a year-long elevation of the surrender rate, because
    the MVR-free window is open for one month; and it is **gated**, because MVR-free
    encashment is worth exercising precisely when the guaranteed benefit exceeds the
    asset share and worth nothing otherwise.  An ungated exercise would invent
    anti-selection on a policy with no incentive to leave.
    """
    for p in (uk_wp_down, uk_wp_up):
        assert p.is_guarantee_date(GUAR_MTH) is True   # the 10th anniversary

    d = uk_wp_down
    assert d.guar_benefit_pp(GUAR_MTH) > d.asset_share(GUAR_MTH)
    assert d.guarantee_exercise(GUAR_MTH) == pytest.approx(0.075)
    ordinary = 1 - (1 - d.surr_rate(GUAR_MTH)) ** (1 / 12)
    assert d.surr_rate_mth(GUAR_MTH) == pytest.approx(
        1 - (1 - ordinary) * (1 - 0.075))
    # and it really is one month: its neighbours carry the ordinary rate only
    assert d.guarantee_exercise(GUAR_MTH - 1) == 0.0
    assert d.guarantee_exercise(GUAR_MTH + 1) == 0.0
    assert d.surr_rate_mth(GUAR_MTH) > 10 * d.surr_rate_mth(GUAR_MTH - 1)

    u = uk_wp_up
    assert u.guar_benefit_pp(GUAR_MTH) < u.asset_share(GUAR_MTH)
    assert u.guarantee_exercise(GUAR_MTH) == 0.0
    assert u.surr_rate_mth(GUAR_MTH) == pytest.approx(
        1 - (1 - u.surr_rate(GUAR_MTH)) ** (1 / 12))


def test_the_guarantee_imminent_suppression(uk_wp_up):
    """0.8 in the twelve months before a guarantee date: policyholders wait for it."""
    p = uk_wp_up
    assert p.guarantee_imminent(GUAR_MTH - 12) == 0.8
    assert p.guarantee_imminent(GUAR_MTH - 1) == 0.8
    assert p.surr_rate(GUAR_MTH - 1) == pytest.approx(0.05 * 0.8)
    assert p.guarantee_imminent(GUAR_MTH - 13) == 1.0
    assert p.guarantee_imminent(GUAR_MTH) == 1.0       # the date itself is not "before"
    assert p.guarantee_imminent(GUAR_MTH + 1) == 1.0


def test_the_surrender_rate_is_capped_at_one(with_profits):
    """The overlays stacked cannot take a rate above certainty, annual or monthly."""
    for point_id in with_profits.Data.model_point_table().index:
        p = with_profits.Projection[point_id]
        for t in range(p.proj_start(), p.proj_len()):
            assert 0.0 <= p.surr_rate(t) <= 1.0
            assert 0.0 <= p.surr_rate_mth(t) <= 1.0


def test_deaths_come_before_surrenders(uk_wp_up):
    """The processing order: surrenders are taken from the survivors of mortality."""
    p = uk_wp_up
    assert p.pols_if_at(T, "BEF_SURR") == pytest.approx(
        p.pols_if(T) * (1.0 - p.mort_rate_mth(T)))
    assert p.pols_surr(T) == pytest.approx(
        p.pols_if_at(T, "BEF_SURR") * p.surr_rate_mth(T))
    assert p.pols_death(T) == pytest.approx(p.pols_if(T) * p.mort_rate_mth(T))


def test_the_inforce_rollforward_closes(with_profits):
    """Every policy that leaves is counted once, on every model point."""
    for point_id in with_profits.Data.model_point_table().index:
        assert with_profits.Projection[point_id].check_pols_roll_fwd() is True


# ---------------------------------------------------------------------------
# Withdrawals and fund exhaustion


def test_the_withdrawal_reduces_the_asset_share_pro_rata_to_the_policy_value(
        with_profits):
    """The same *proportion* of the asset share as of what the policy is worth."""
    p = with_profits.Projection[4]
    assert p.wd_rate() == 0.05
    # the annual election, taken a twelfth at a time
    assert p.wd_pp(T0) == pytest.approx(0.05 * 25000.0 / 12)
    pv = p.policy_value_open(T0)
    assert pv == pytest.approx(S_OPEN, abs=PENNY)       # the opening FV + FB
    assert p.wd_as_pp(T0) == pytest.approx(AS_OPEN * p.wd_pp(T0) / pv, abs=PENNY)
    assert p.wd_as_pp(T0) > p.wd_pp(T0)                 # AS above the policy value


def test_the_withdrawal_is_capped_at_the_unit_fund(with_profits):
    """A level election against a fund being run down eventually asks for too much."""
    p = with_profits.Projection[4]
    monthly = 0.05 * 25000.0 / 12
    assert p.wd_pp(240) == pytest.approx(monthly)       # the election, in full
    assert p.guar_benefit_open(403) < monthly           # not enough left
    assert p.wd_pp(403) == pytest.approx(p.guar_benefit_open(403), abs=PENNY)
    assert p.units(403) == pytest.approx(0.0, abs=1e-9)
    assert p.check_fund_nonneg() is True


def test_the_fund_exhausts_the_projection_and_forces_an_encashment(with_profits):
    """The last unit is cancelled at t = 403, so the projection ends at t = 402."""
    p = with_profits.Projection[4]
    assert p.fund_exhaust_mth() == 403
    assert p.proj_len() == 403                  # t = 60 .. 402
    assert p.policy_year(402) == 34             # in its thirty-fourth policy year
    assert p.is_forced_encashment() is True
    # A real contractual ending, so the survivors are paid — residual final bonus and all.
    last = p.proj_len() - 1
    assert p.pols_maturity(last) > 0.0
    assert p.claim_pp(last, "MATURITY") == pytest.approx(
        p.guar_benefit_pp(last) + p.final_bonus_pp(last))
    assert p.claims(last, "MATURITY") > 0.0


def test_a_limiting_age_ending_pays_nothing(uk_wp_up):
    """That ending is a modelling truncation; paying there would invent a claim."""
    p = uk_wp_up
    assert p.fund_exhaust_mth() == 0
    assert p.proj_len() == 12 * (120 - 55)
    assert p.is_forced_encashment() is False
    last = p.proj_len() - 1
    assert p.age(last) == 119                   # the last year before the limiting age
    assert p.claim_pp(last, "MATURITY") == 0.0
    assert p.claims(last, "MATURITY") == 0.0


# ---------------------------------------------------------------------------
# Charges and the shareholder transfer


def test_the_guarantee_charge_stops_at_its_lifetime_cap(with_profits):
    """0.10% a year, ceasing once cumulative deductions reach 2% of the asset share.

    The cap is measured against the **current** asset share, as the notes specify, not
    against a level struck once at first breach.  On a fund that keeps growing the
    threshold grows with it, so the charge stops the period the cumulative overtakes it
    and resumes the period after.  That is the rule as written; a cap frozen at first
    breach would be a different rule and a materially different charge.
    """
    p = with_profits.Projection[3]
    assert with_profits.Projection.guar_charge_rate_base == 0.001
    assert with_profits.Projection.guar_charge_cap == 0.02
    # The cap is tested every month on this grid, so the charge stops the month the
    # cumulative overtakes the threshold rather than at the following anniversary.
    assert p.guar_charge_rate(486) == pytest.approx(0.001)
    assert p.guar_charge_cum_pp(485) < 0.02 * p.asset_share(485)
    assert p.guar_charge_rate(487) == 0.0                   # the first breach
    assert p.guar_charge_cum_pp(486) >= 0.02 * p.asset_share(486)
    assert p.guar_charge_pp(487) == 0.0
    assert p.guar_charge_cum_pp(487) == pytest.approx(p.guar_charge_cum_pp(486))
    # The threshold is 2% of the *current* asset share, which keeps growing, so it
    # overtakes the frozen cumulative again and the charge resumes.
    assert p.guar_charge_rate(488) == pytest.approx(0.001)
    assert p.guar_charge_cum_pp(487) < 0.02 * p.asset_share(487)
    # The monthly rate is the annual one converted, not a twelfth of it.
    assert (1 - p.guar_charge_rate_mth(486)) ** 12 == pytest.approx(
        1 - 0.001, rel=1e-14)


def test_the_shareholder_transfer_is_reported_and_never_netted(uk_wp_up):
    """A tenth of each distribution leaves the fund, on its own line."""
    p = uk_wp_up
    df = p.result_cf()
    assert "shareholder_transfers" in df.columns
    t = df.index[0]
    on_declaration = p.shareholder_transfer_pp(t) * p.pols_if(t)
    exits = p.pols_death(t) + p.pols_surr(t) + p.pols_maturity(t)
    assert p.shareholder_transfers(t) == pytest.approx(
        on_declaration + p.final_bonus_pp(t) * exits / 9.0)
    assert p.shareholder_transfers(t) > 0.0


def test_expenses_inflate(uk_wp_up):
    """GBP 30 a policy a year at 3% — a twelfth a month, stepping on the anniversary."""
    p = uk_wp_up
    assert p.inflation_factor(0) == pytest.approx(1.0)   # one in the first policy year
    assert p.inflation_factor(11) == pytest.approx(1.0)  # level through the year
    assert p.inflation_factor(12) == pytest.approx(1.03)
    assert p.inflation_factor(T) == pytest.approx(1.03 ** 5)   # the sixth policy year
    assert p.expenses(T) == pytest.approx(
        30.0 / 12 * 1.03 ** 5 * p.pols_if(T))
    # the policy year's expense is the annual assumption, inflated once
    assert sum(p.expenses(t) / p.pols_if(t) for t in range(T0, T + 1)) == pytest.approx(
        30.0 * 1.03 ** 5, abs=PENNY)


# ---------------------------------------------------------------------------
# Chassis and scope


def test_the_smoothed_fund_chassis_is_out_of_scope(tmp_path):
    """Its limits are daily and quarterly; a monthly grid still smooths them away.

    Moving from an annual grid to a monthly one narrows the gap without closing it - a
    5% daily limit needs a daily step - so the exclusion stands rather than being quietly
    relaxed.  The model rejects the chassis by name rather than running it on the wrong
    grid.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="WP_UK_S_sf")
    try:
        table = pd.read_csv(MODEL_DIR.parent / "model_point_table.csv",
                            index_col="point_id")
        table.loc[1, "chassis"] = "SF_prufund"
        alt = "model_point_table_sf.csv"
        table.to_csv(model.Data.input_dir() / alt)
        try:
            model.Data.model_point_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            with pytest.raises(FormulaError):
                model.Projection[1].chassis()
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_tax_basis_validates(uk_wp_up, with_profits):
    """life_net or pension_gross; the return is supplied on the basis that applies."""
    assert uk_wp_up.tax_basis() == "life_net"
    assert with_profits.Projection[6].tax_basis() == "pension_gross"


def test_the_claim_kinds_validate(uk_wp_up):
    """A typo in a kind must fail rather than fall through to a default."""
    with pytest.raises(FormulaError):
        uk_wp_up.claim_pp(T, "LAPSE")
    with pytest.raises(FormulaError):
        uk_wp_up.claims(T, "LAPSE")


def test_claims_total_the_three_paid_kinds(with_profits):
    """A guarantee-date exit *is* a surrender, so GUARANTEE is not a separate outgo."""
    for point_id in (1, 2, 5):
        p = with_profits.Projection[point_id]
        for t in range(p.proj_start(), p.proj_start() + 5):
            assert p.claims(t) == pytest.approx(
                p.claims(t, "DEATH") + p.claims(t, "SURRENDER")
                + p.claims(t, "MATURITY"))


# ---------------------------------------------------------------------------
# Structure


def test_result_cf_shape(uk_wp_up):
    """The cash flow table, indexed by the 0-based month t.

    The frame opens at the elapsed months and ends at ``proj_len() - 1``, so its
    length is ``proj_len() - proj_start()``.
    """
    df = uk_wp_up.result_cf()
    assert df.index.name == "t"
    assert df.index[0] == 12 * uk_wp_up.duration_inforce() == 60
    assert df.index[-1] == uk_wp_up.proj_len() - 1
    assert list(df.index) == list(range(uk_wp_up.proj_start(),
                                        uk_wp_up.proj_len()))
    assert len(df) == uk_wp_up.proj_len() - uk_wp_up.proj_start()
    assert list(df.columns) == [
        "pols_if", "asset_share", "premiums", "claims_death", "claims_surrender",
        "claims_maturity", "withdrawals", "expenses", "shareholder_transfers",
        "smoothing_cost", "net_cf"]
    assert df.notna().all().all()


def test_result_payout_shape(uk_wp_down):
    """The payout table, and it reproduces the worked example row for row."""
    df = uk_wp_down.result_payout()
    assert df.index.name == "t"
    e = WORKED_EXAMPLE["down"]
    assert df.at[T, "asset_share"] == pytest.approx(e["asset_share"], abs=PENNY)
    assert df.at[T, "guar_benefit_pp"] == pytest.approx(e["guar_benefit"], abs=PENNY)
    assert df.at[T, "smoothed_payout"] == pytest.approx(e["smoothed"], abs=PENNY)
    assert df.at[T, "mvr_pp"] == pytest.approx(e["mvr"], abs=PENNY)
    assert df.at[T, "claim_surrender"] == pytest.approx(e["pay_surrender"], abs=PENNY)
    assert df.notna().all().all()


def test_the_smoothing_account_accumulates_without_recycling(uk_wp_down):
    """The estate's running cost, tracked and not fed back into credited returns."""
    p = uk_wp_down
    t0 = p.proj_start()
    # The balance opens at zero in the first projected month, not in a row below it.
    assert p.smoothing_account(t0) == pytest.approx(p.smoothing_cost(t0))
    for t in range(t0 + 1, t0 + 5):
        assert p.smoothing_account(t) == pytest.approx(
            p.smoothing_account(t - 1) + p.smoothing_cost(t))
    assert p.smoothing_account(t0 + 4) > 0.0                 # guarantees are biting


def test_model_docstring_describes_the_current_structure(with_profits):
    """Two Spaces, and the docstring names both."""
    doc = with_profits.doc
    assert "Data" in doc and "Projection" in doc
    assert "asset share is a state variable" in doc
    assert "Monthly steps" in doc                  # the projection basis, not annual
    assert "declaration stays annual" in doc       # and why it is not monthly with it
    assert set(with_profits.spaces) == {"Data", "Projection"}


def test_space_docstrings_carry_their_reference_material(with_profits):
    """The symbol mapping and the input table live where a reader will meet them."""
    proj = with_profits.Projection.doc
    assert "Notes symbol" in proj
    assert "asset_share_at(t, timing)" in proj
    for cells in ("is_declaration_month(t)", "fund_return_mth()", "surr_rate_mth(t)",
                  "guarantee_exercise(t)"):
        assert cells in proj
    assert "model_point_table.csv" in with_profits.Data.doc


def test_the_discretionary_scale_is_references_not_a_rate_table(with_profits):
    """None of it is published, so it sits where a reader trips over it."""
    refs = set(with_profits.Projection.refs)
    for name in ("amc_rate", "guar_charge_rate_base", "guar_charge_cap", "smooth_cap",
                 "corridor_lo", "corridor_hi", "guar_fill_target", "bonus_speed",
                 "bonus_change_cap", "mvr_deterrent_factor", "guarantee_exercise_rate",
                 "death_benefit_factor", "surr_disc_rate"):
        assert name in refs, name
    columns = set(with_profits.Data.model_point_table().columns)
    for name in ("bonus_rate", "fund_return", "guarantee_dates", "wd_rate", "tax_basis"):
        assert name in columns, name


def test_inputs_live_beside_the_model():
    """The three input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows."""
    import pandas as pd

    src = MODEL_DIR.parent / "lapse_table.csv"
    sticky = pd.read_csv(src, index_col=["chassis", "policy_year"])
    sticky["lapse_rate"] = sticky["lapse_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="WP_UK_S_swap")
    try:
        alt = "lapse_table_sticky.csv"
        sticky.to_csv(model.Data.input_dir() / alt)
        try:
            base = model.Projection[1].result_cf()["shareholder_transfers"].sum()
            model.Data.lapse_table_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            # Halving surrender keeps policies in force, so more bonus is declared on
            # them and more is transferred to shareholders.
            assert model.Projection[1].result_cf()[
                "shareholder_transfers"].sum() > base
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="WP_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="WP_UK_S_rt")
    try:
        for key, point_id in (("up", 1), ("down", 2)):
            p = reread.Projection[point_id]
            e = WORKED_EXAMPLE[key]
            assert p.asset_share(T) == pytest.approx(e["asset_share"], abs=PENNY)
            assert p.smoothed_payout(T) == pytest.approx(e["smoothed"], abs=PENNY)
            assert p.claim_pp(T, "SURRENDER") == pytest.approx(
                e["pay_surrender"], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()
