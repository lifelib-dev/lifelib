"""Golden and structural tests for WP_UK_A.

The golden values are the worked example in
products/with_profits/technical-notes.md ("Worked example"), which projects a
unitised with-profits bond in force at duration 5 — asset share GBP 30,000, face value
GBP 27,602.02, smoothed payout GBP 29,500, unit price 1.104081 on 25,000 units, AMC 1%,
guarantee charge 0.10%, q(60) = 0.5%, death uplift 1.01, smoothing cap 10% — through
policy year 6 on **two scenarios**: a fund return of +7% and one of -15%.  They are
hard-coded here rather than pickled so that a reviewer can compare them against the
notes by eye.

Tolerances follow the precision the notes display: money to the penny.

Beyond the worked example this module asserts the product facts the notes call out,
because each is a way an implementation can look right and be wrong:

* the asset share is a **state variable**, not a cash flow, and its step order —
  charges, then the shareholder transfer, then the mortality charge on the balance
  *after* the transfer — is contractual discipline;
* a declared bonus **hardens** into the guarantee permanently, at a cost to the payout
  of exactly a ninth of what it hardens;
* the smoothing cap is applied **before** the corridor;
* a final bonus and a market value reduction are **never** simultaneous, and the MVR is
  bounded by the excess of the unit value over the underlying asset value; and
* the guarantee-date surrender spike is gated on the guarantee actually being in the
  money, because otherwise it invents anti-selection where there is none.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from uk_registry import MODELS, LIB

PENNY = 0.01          # the notes display money to 2 d.p. and truncate, not round

MODEL_DIR = LIB / MODELS["WP_UK_A"][0]

T = 6                 # the policy year the worked example projects

# The notes' two-scenario table, keyed by the fixture that carries the scenario.
# fund return, AS after return, AS after charges, b(6), Q(6), FV(6),
# CB, ST, AS after ST, MC, AS(6), S_cap, S(6), FB, MVR, MVR bound
WORKED_EXAMPLE = {
    "up": dict(
        fund_return=0.07, aft_return=32100.00, aft_charge=31746.90,
        bonus=0.02, unit_price=1.126162, guar_benefit=28154.06,
        cost_of_bonus=552.04, transfer=61.34, aft_st=31685.56, mort_charge=0.00,
        asset_share=31685.56, capped=31685.56, smoothed=31685.56,
        final_bonus=3531.50, mvr=0.00, mvr_bound=0.00,
        pay_guarantee=31685.56, pay_surrender=31685.56, pay_death=32002.42,
        cost_guarantee=0.00, cost_surrender=0.00,
    ),
    "down": dict(
        fund_return=-0.15, aft_return=25500.00, aft_charge=25219.50,
        bonus=0.01, unit_price=1.115122, guar_benefit=27878.04,
        cost_of_bonus=276.02, transfer=30.67, aft_st=25188.83, mort_charge=14.84,
        asset_share=25173.99, capped=26550.00, smoothed=26550.00,
        final_bonus=0.00, mvr=1328.04, mvr_bound=2704.05,
        pay_guarantee=27878.04, pay_surrender=26550.00, pay_death=28156.82,
        cost_guarantee=2704.05, cost_surrender=1376.01,
    ),
}

# State carried into policy year 6, from the model point.
AS_5 = 30000.00
S_5 = 29500.00
FV_5 = 27602.02

CWP_MATURITY = 29018.91      # G(25) = 20,000 x 1.015^25, the notes' endowment check


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_asset_share_steps(with_profits, key):
    """The recursion one step at a time, both scenarios, to the displayed precision."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.fund_return() == pytest.approx(e["fund_return"])
    assert p.asset_share(T - 1) == pytest.approx(AS_5, abs=PENNY)
    assert p.asset_share_at(T, "BEF_RETURN") == pytest.approx(AS_5, abs=PENNY)
    assert p.asset_share_at(T, "AFT_RETURN") == pytest.approx(e["aft_return"], abs=PENNY)
    assert p.asset_share_at(T, "AFT_CHARGE") == pytest.approx(e["aft_charge"], abs=PENNY)
    assert p.asset_share_at(T, "AFT_ST") == pytest.approx(e["aft_st"], abs=PENNY)
    assert p.asset_share_at(T, "AFT_MC") == pytest.approx(e["asset_share"], abs=PENNY)
    assert p.asset_share(T) == pytest.approx(e["asset_share"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_bonus_and_unit_price(with_profits, key):
    """b(6), Q(6) = Q(5)(1 + b) and FV(6) = U Q(6) on 25,000 units."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.bonus_rate(T) == pytest.approx(e["bonus"])
    assert p.unit_price(T - 1) == pytest.approx(1.104081)
    assert p.unit_price(T) == pytest.approx(e["unit_price"], abs=1e-6)
    assert p.units(T) == pytest.approx(25000.0)
    assert p.guar_benefit_pp(T - 1) == pytest.approx(FV_5, abs=PENNY)
    assert p.guar_benefit_pp(T) == pytest.approx(e["guar_benefit"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_bonus_cost_and_shareholder_transfer(with_profits, key):
    """CB = b FV(5) on the unitised chassis, and ST = CB/9 — the 90:10 split."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.cost_of_bonus_pp(T) == pytest.approx(e["cost_of_bonus"], abs=PENNY)
    assert p.cost_of_bonus_pp(T) == pytest.approx(
        p.bonus_rate(T) * p.guar_benefit_pp(T - 1), abs=PENNY)
    assert p.shareholder_transfer_pp(T) == pytest.approx(e["transfer"], abs=PENNY)
    assert p.shareholder_transfer_pp(T) == pytest.approx(p.cost_of_bonus_pp(T) / 9.0)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_mortality_charge(with_profits, key):
    """MC = q x max(0, 1.01 FV(6) - AS after ST); nil in A, 14.84 in B."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.mort_rate(T) == pytest.approx(0.005, abs=5e-9)
    assert p.death_guar_pp(T) == pytest.approx(1.01 * p.guar_benefit_pp(T), abs=PENNY)
    assert p.mort_charge_pp(T) == pytest.approx(e["mort_charge"], abs=PENNY)


@pytest.mark.parametrize("key", sorted(WORKED_EXAMPLE))
def test_worked_example_smoothing(with_profits, key):
    """The cap, then the corridor.  In B the cap floor binds at exactly -10%."""
    p = with_profits.Projection[1 if key == "up" else 2]
    e = WORKED_EXAMPLE[key]
    assert p.smoothed_payout(T - 1) == pytest.approx(S_5, abs=PENNY)
    assert p.smoothed_payout_capped(T) == pytest.approx(e["capped"], abs=PENNY)
    assert p.smoothed_payout(T) == pytest.approx(e["smoothed"], abs=PENNY)


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

    The asset share falls 16.1% while the surrender payout falls exactly 10.0% — the
    smoothing cap absorbing the rest — and both scenarios land inside the corridor.
    """
    p = uk_wp_down
    assert p.asset_share(T) / AS_5 == pytest.approx(0.8391, abs=5e-5)
    assert p.claim_pp(T, "SURRENDER") / S_5 == pytest.approx(0.90, abs=5e-7)
    assert p.claim_pp(T, "SURRENDER") / p.asset_share(T) == pytest.approx(
        1.055, abs=5e-4)
    assert p.mvr_pp(T) < max(0.0, p.guar_benefit_pp(T) - p.asset_share(T))


def test_worked_example_the_up_scenario_pays_the_asset_share(uk_wp_up):
    """Neither the cap nor the corridor binds in A, so the payout is the asset share."""
    p = uk_wp_up
    assert p.smoothed_payout(T) == pytest.approx(p.asset_share(T))
    assert p.claim_pp(T, "SURRENDER") / p.asset_share(T) == pytest.approx(1.0)


def test_the_endowment_maturity_check_line(with_profits):
    """G(25) = 20,000 x 1.015^25 = 29,018.91, and the guarantee bites by 115."""
    p = with_profits.Projection[5]
    assert p.chassis() == "CWP_endowment"
    assert p.proj_len() == 25
    assert p.guar_benefit_pp(25) == pytest.approx(CWP_MATURITY, abs=PENNY)
    assert p.claim_pp(25, "MATURITY") == pytest.approx(CWP_MATURITY, abs=PENNY)
    # The asset share falls short of the guarantee, so the estate meets the difference.
    assert p.asset_share(25) < CWP_MATURITY
    assert p.smoothing_cost_pp(25, "MATURITY") == pytest.approx(115.07, abs=0.02)


# ---------------------------------------------------------------------------
# The asset share is a state variable, not a cash flow


def test_the_asset_share_recursion_closes(with_profits):
    """Rebuilt in one expression, the recursion reproduces the model in every year."""
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
    q, dbg = p.mort_rate(T), p.death_guar_pp(T)
    assert p.mort_charge_pp(T) == pytest.approx(
        q * max(0.0, dbg - p.asset_share_at(T, "AFT_ST")), abs=1e-9)
    wrong = q * max(0.0, dbg - p.asset_share_at(T, "AFT_CHARGE"))
    assert wrong < p.mort_charge_pp(T) - 0.10       # 14.69 against 14.84


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
    """Sixty years at -15% exhausts it; the payout target may not go negative.

    A negative asset share would invert the corridor, whose bounds are 0.80 AS and
    1.20 AS.  What a nil asset share means is that the guarantee is being met entirely
    by the estate.
    """
    p = uk_wp_down
    assert p.asset_share(p.proj_len()) == 0.0
    assert p.check_fund_nonneg() is True
    assert p.smoothed_payout(p.proj_len()) == 0.0
    assert p.guar_benefit_pp(p.proj_len()) > 0.0    # the guarantee is still there


# ---------------------------------------------------------------------------
# The bonus hardens, and that is what makes guarantees expensive


def test_the_unit_price_never_falls(with_profits):
    """b(t) >= 0 is a contractual floor, so a declaration is irreversible."""
    for point_id in (1, 2, 3, 4):
        p = with_profits.Projection[point_id]
        for t in range(p.proj_start(), p.proj_len() + 1):
            assert p.bonus_rate(t) >= 0.0
            assert p.unit_price(t) >= p.unit_price(t - 1)


def test_a_declaration_hardens_the_payout_at_a_cost_of_a_ninth(uk_wp_up):
    """The declaration converts final bonus into guarantee without moving the payout.

    FV rises by the full cost of bonus, 552.04, and the target payout falls by 61.34 -
    the shareholder transfer, one ninth of what was hardened.  Everything else in the
    payout is unchanged, which is why hardening is the expensive part of the product
    rather than the distribution itself.
    """
    p = uk_wp_up
    hardened = p.guar_benefit_pp(T) - p.guar_benefit_pp(T - 1)
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
    assert [p.bonus_rate(t) for t in range(6, 10)] == [0.02] * 4

    with_profits.Projection.bonus_rule_on = True
    with_profits.Projection.clear_all()
    try:
        p = with_profits.Projection[1]
        assert p.bonus_rate(6) == pytest.approx(0.02)     # the snapshot, held
        assert p.bonus_rate(7) == pytest.approx(0.03)     # +1%, capped
        assert p.bonus_rate(8) == pytest.approx(0.04)     # +1%, capped
        assert p.bonus_supportable(9) > p.bonus_rate(8)
        assert p.bonus_rate(9) == pytest.approx(
            0.04 + 0.5 * (p.bonus_supportable(9) - 0.04))  # inside the cap now
    finally:
        with_profits.Projection.bonus_rule_on = False
        with_profits.Projection.clear_all()
    assert with_profits.Projection[1].bonus_rate(7) == pytest.approx(0.02)


def test_the_declared_bonus_is_floored_at_zero_and_stays_there(with_profits):
    """A declaration can be nil but never negative, however bad the supportable rate."""
    with_profits.Projection.bonus_rule_on = True
    with_profits.Projection.clear_all()
    try:
        p = with_profits.Projection[2]
        assert p.bonus_supportable(7) < -0.10             # deeply unsupportable
        assert p.bonus_rate(6) == pytest.approx(0.01)
        assert [p.bonus_rate(t) for t in range(7, 13)] == [0.0] * 6
        assert all(p.unit_price(t) == pytest.approx(p.unit_price(t - 1))
                   for t in range(8, 13))
    finally:
        with_profits.Projection.bonus_rule_on = False
        with_profits.Projection.clear_all()


def test_the_endowment_bonus_cost_is_discounted_and_the_bond_one_is_not(with_profits):
    """A reversionary addition is not payable until maturity, so it is discounted."""
    cwp = with_profits.Projection[5]
    delta = cwp.guar_benefit_pp(1) - cwp.guar_benefit_pp(0)
    assert delta == pytest.approx(20000.0 * 0.015, abs=PENNY)
    assert cwp.cost_of_bonus_pp(1) == pytest.approx(delta / 1.04 ** 24, abs=PENNY)
    assert cwp.cost_of_bonus_pp(1) < delta

    uwp = with_profits.Projection[1]
    assert uwp.cost_of_bonus_pp(T) == pytest.approx(
        uwp.guar_benefit_pp(T) - uwp.guar_benefit_pp(T - 1), abs=PENNY)


# ---------------------------------------------------------------------------
# Smoothing: the cap, then the corridor


def test_the_cap_is_skipped_when_there_is_no_previous_payout(with_profits):
    """A new-business cell has no prior payout, so the cap would clamp it to nil."""
    p = with_profits.Projection[5]
    assert p.proj_start() == 1
    assert p.smoothed_payout(0) == 0.0
    assert p.smoothed_payout_capped(1) == pytest.approx(p.asset_share(1))
    assert p.smoothed_payout(1) == pytest.approx(p.asset_share(1))


def test_the_cap_is_applied_before_the_corridor(tmp_path):
    """Order matters: corridor-then-cap collapses to the cap alone.

    In the notes' scenarios the corridor never binds after the cap, so both orders
    agree there.  Deepen the shock past a quarter and they diverge — the cap floor
    holds the payout at 26,550 and the corridor then pulls it down to 1.20 of the asset
    share.  Applying the corridor first would leave 26,550 standing, because an asset
    share is always inside its own corridor.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="WP_UK_A_order")
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
            assert p.smoothed_payout_capped(T) == pytest.approx(0.90 * S_5, abs=PENNY)
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
        for t in range(p.proj_start(), p.proj_len() + 1):
            assert min(p.final_bonus_pp(t), p.mvr_pp(t)) == pytest.approx(0.0, abs=1e-9)


def test_the_mvr_stays_inside_its_contractual_bound(with_profits):
    """It may not exceed the excess of the unit value over the underlying asset value."""
    for point_id in with_profits.Data.model_point_table().index:
        assert with_profits.Projection[point_id].check_mvr_bound() is True


def test_the_mvr_is_not_applied_on_a_guarantee_date(uk_wp_down):
    """The scale is still positive - it is the *application* the contract waives."""
    p = uk_wp_down
    assert p.guarantee_years() == (10,)
    assert p.is_guarantee_date(10) is True
    assert p.mvr_pp(10) > 0.0
    assert p.mvr_applied_pp(10) == 0.0
    assert p.claim_pp(10, "SURRENDER") == pytest.approx(p.claim_pp(10, "GUARANTEE"))


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
    reduction in policy year 1 of a 25-year endowment.
    """
    p = with_profits.Projection[5]
    assert p.guar_benefit_pp(1) > p.smoothed_payout(1) + 19000.0
    assert p.mvr_pp(1) == 0.0
    assert p.mvr_applied_pp(1) == 0.0
    assert p.claim_pp(1, "SURRENDER") == pytest.approx(p.smoothed_payout(1))
    assert all(p.mvr_pp(t) == 0.0 for t in range(1, 26))


def test_the_endowment_surrender_value_is_capped_at_the_prospective_value(with_profits):
    """It targets the smoothed payout, never more than the policy is worth at maturity."""
    p = with_profits.Projection[6]
    for t in range(p.proj_start(), p.proj_len() + 1):
        prospective = p.guar_benefit_pp(t) + p.final_bonus_pp(t)
        assert p.claim_pp(t, "SURRENDER") <= prospective + 1e-9
        assert p.claim_pp(t, "SURRENDER") == pytest.approx(
            min(p.smoothed_payout(t), prospective))


# ---------------------------------------------------------------------------
# Behaviour, where the anti-selection lives


def test_the_mvr_deterrent_suppresses_exit(uk_wp_down, uk_wp_up):
    """0.6 while an MVR would be applied; inert where none would be."""
    assert uk_wp_down.mvr_applied_pp(T) > 0.0
    assert uk_wp_down.mvr_deterrent(T) == 0.6
    assert uk_wp_down.surr_rate(T) == pytest.approx(0.05 * 0.6)

    assert uk_wp_up.mvr_applied_pp(T) == 0.0
    assert uk_wp_up.mvr_deterrent(T) == 1.0
    assert uk_wp_up.surr_rate(T) == pytest.approx(0.05)


def test_the_guarantee_spike_is_gated_on_the_guarantee_being_in_the_money(
        uk_wp_down, uk_wp_up):
    """The gate is the point.

    MVR-free encashment is worth exercising precisely when the guaranteed benefit
    exceeds the asset share and worth nothing otherwise, so an ungated spike would
    invent anti-selection on a policy with no incentive to exit.
    """
    for p in (uk_wp_down, uk_wp_up):
        assert p.is_guarantee_date(10) is True

    assert uk_wp_down.guar_benefit_pp(10) > uk_wp_down.asset_share(10)
    assert uk_wp_down.guarantee_spike(10) == 2.5
    assert uk_wp_down.surr_rate(10) == pytest.approx(0.05 * 2.5)

    assert uk_wp_up.guar_benefit_pp(10) < uk_wp_up.asset_share(10)
    assert uk_wp_up.guarantee_spike(10) == 1.0
    assert uk_wp_up.surr_rate(10) == pytest.approx(0.05)


def test_the_guarantee_imminent_suppression(uk_wp_up):
    """0.8 in the year before a guarantee date: policyholders wait for the window."""
    p = uk_wp_up
    assert p.guarantee_imminent(9) == 0.8
    assert p.surr_rate(9) == pytest.approx(0.05 * 0.8)
    assert p.guarantee_imminent(8) == 1.0
    assert p.guarantee_imminent(10) == 1.0


def test_the_surrender_rate_is_capped_at_one(with_profits):
    """Three multipliers stacked cannot take a rate above certainty."""
    for point_id in with_profits.Data.model_point_table().index:
        p = with_profits.Projection[point_id]
        for t in range(p.proj_start(), p.proj_len() + 1):
            assert 0.0 <= p.surr_rate(t) <= 1.0


def test_deaths_come_before_surrenders(uk_wp_up):
    """The processing order: surrenders are taken from the survivors of mortality."""
    p = uk_wp_up
    assert p.pols_if_at(T, "BEF_SURR") == pytest.approx(
        p.pols_if(T) * (1.0 - p.mort_rate(T)))
    assert p.pols_surr(T) == pytest.approx(
        p.pols_if_at(T, "BEF_SURR") * p.surr_rate(T))
    assert p.pols_death(T) == pytest.approx(p.pols_if(T) * p.mort_rate(T))


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
    assert p.wd_pp(T) == pytest.approx(0.05 * 25000.0)
    pv = p.policy_value_pp(T - 1)
    assert pv == pytest.approx(S_5, abs=PENNY)          # FV(5) + FB(5)
    assert p.wd_as_pp(T) == pytest.approx(AS_5 * p.wd_pp(T) / pv, abs=PENNY)
    assert p.wd_as_pp(T) > p.wd_pp(T)                   # AS above the policy value


def test_the_withdrawal_is_capped_at_the_unit_fund(with_profits):
    """A level election against a fund being run down eventually asks for too much."""
    p = with_profits.Projection[4]
    assert p.wd_pp(20) == pytest.approx(1250.0)         # the election, in full
    assert p.guar_benefit_pp(33) < 1250.0               # not enough left
    assert p.wd_pp(34) == pytest.approx(p.guar_benefit_pp(33), abs=PENNY)
    assert p.units(34) == pytest.approx(0.0, abs=1e-9)
    assert p.check_fund_nonneg() is True


def test_the_fund_exhausts_the_projection_and_forces_an_encashment(with_profits):
    """The last unit is cancelled in year 34, so the projection ends in year 33."""
    p = with_profits.Projection[4]
    assert p.fund_exhaust_year() == 34
    assert p.proj_len() == 33
    assert p.is_forced_encashment() is True
    # A real contractual ending, so the survivors are paid — residual final bonus and all.
    assert p.pols_maturity(33) > 0.0
    assert p.claim_pp(33, "MATURITY") == pytest.approx(
        p.guar_benefit_pp(33) + p.final_bonus_pp(33))
    assert p.claims(33, "MATURITY") > 0.0


def test_a_limiting_age_ending_pays_nothing(uk_wp_up):
    """That ending is a modelling truncation; paying there would invent a claim."""
    p = uk_wp_up
    assert p.fund_exhaust_year() == 0
    assert p.proj_len() == 120 - 55
    assert p.is_forced_encashment() is False
    assert p.claim_pp(p.proj_len(), "MATURITY") == 0.0
    assert p.claims(p.proj_len(), "MATURITY") == 0.0


# ---------------------------------------------------------------------------
# Charges and the shareholder transfer


def test_the_guarantee_charge_stops_at_its_lifetime_cap(with_profits):
    """0.10% a year, ceasing once cumulative deductions reach 2% of the asset share.

    The cap is measured against the **current** asset share, as the notes specify, not
    against a level struck once at first breach.  On a fund that keeps growing the
    threshold grows with it, so the charge stops the year the cumulative overtakes it
    and resumes the year after.  That is the rule as written; a cap frozen at first
    breach would be a different rule and a materially different charge.
    """
    p = with_profits.Projection[3]
    assert with_profits.Projection.guar_charge_rate_base == 0.001
    assert with_profits.Projection.guar_charge_cap == 0.02
    assert p.guar_charge_rate(39) == pytest.approx(0.001)
    assert p.guar_charge_cum_pp(38) < 0.02 * p.asset_share(38)
    assert p.guar_charge_rate(40) == 0.0                    # the first breach
    assert p.guar_charge_cum_pp(39) >= 0.02 * p.asset_share(39)
    assert p.guar_charge_pp(40) == 0.0
    assert p.guar_charge_cum_pp(40) == pytest.approx(p.guar_charge_cum_pp(39))
    # The threshold is 2% of the *current* asset share, which keeps growing, so it
    # overtakes the frozen cumulative again and the charge resumes.
    assert p.guar_charge_rate(41) == pytest.approx(0.001)
    assert p.guar_charge_cum_pp(40) < 0.02 * p.asset_share(40)


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
    """GBP 30 a policy a year at 3%, on the in-force count."""
    p = uk_wp_up
    assert p.inflation_factor(T) == pytest.approx(1.03 ** (T - 1))
    assert p.expenses(T) == pytest.approx(30.0 * 1.03 ** (T - 1) * p.pols_if(T))


# ---------------------------------------------------------------------------
# Chassis and scope


def test_the_smoothed_fund_chassis_is_out_of_scope(tmp_path):
    """Its limits are daily and quarterly; an annual grid smooths them away.

    The model rejects it by name rather than running it on the wrong grid.
    """
    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="WP_UK_A_sf")
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
    """The cash flow table, indexed by policy year."""
    df = uk_wp_up.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(uk_wp_up.proj_start(),
                                        uk_wp_up.proj_len() + 1))
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
    assert p.smoothing_account(p.proj_start() - 1) == 0.0
    for t in range(p.proj_start(), p.proj_start() + 5):
        assert p.smoothing_account(t) == pytest.approx(
            p.smoothing_account(t - 1) + p.smoothing_cost(t))
    assert p.smoothing_account(p.proj_start() + 4) > 0.0     # guarantees are biting


def test_model_docstring_describes_the_current_structure(with_profits):
    """Two Spaces, and the docstring names both."""
    doc = with_profits.doc
    assert "Data" in doc and "Projection" in doc
    assert "asset share is a state variable" in doc
    assert set(with_profits.spaces) == {"Data", "Projection"}


def test_space_docstrings_carry_their_reference_material(with_profits):
    """The symbol mapping and the input table live where a reader will meet them."""
    proj = with_profits.Projection.doc
    assert "Notes symbol" in proj
    assert "asset_share_at(t, timing)" in proj
    assert "model_point_table.csv" in with_profits.Data.doc


def test_the_discretionary_scale_is_references_not_a_rate_table(with_profits):
    """None of it is published, so it sits where a reader trips over it."""
    refs = set(with_profits.Projection.refs)
    for name in ("amc_rate", "guar_charge_rate_base", "guar_charge_cap", "smooth_cap",
                 "corridor_lo", "corridor_hi", "guar_fill_target", "bonus_speed",
                 "bonus_change_cap", "mvr_deterrent_factor", "guarantee_spike_factor",
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

    model = mx.read_model(MODEL_DIR, name="WP_UK_A_swap")
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

    model = mx.read_model(MODEL_DIR, name="WP_UK_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="WP_UK_A_rt")
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
