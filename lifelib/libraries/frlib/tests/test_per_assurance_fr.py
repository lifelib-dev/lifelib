"""Golden and structural tests for PER_FR_S.

The golden values are the worked example in
``products/per_assurance/technical-notes.md`` ("Worked example"): a male aged 52 with a
declared horizon of 64, two completed years since his first *versement*, compartment 1 on
the *équilibré horizon retraite* glide path, opening EUR 16,600 entirely in *unités de
compte* against a EUR 16,000 *garantie plancher* base, paying EUR 3,000 at the start of
each of the twelve plan years, and settling 70% as capital and 30% as a *rente viagère*
that turns out to be small enough to commute.  Model point 1 is that cell.  The numbers
are hard-coded here rather than pickled so that a reviewer can compare them against the
notes by eye.

Tolerances follow the precision the notes display: money to the cent, the in-force
probability to six decimals, shares to the basis point.

``t`` is **0-based** throughout and counts **plan months**: ``t = 0`` is the first
projected month, the anchor cell's frame is ``t = 0 … 143``, and ``proj_len() = 12 x
proj_years()`` is the number of projected months rather than the last index.  Plan year
``y`` is months ``12y … 12y + 11``; the module reads a worked-example row at its
**rebalancing month** ``bom(y) = 12y``, where the *versement*, the glide-path share and the
switch are determined, and at its **anniversary month** ``anniv(y) = 12y + 11``, where the
management charge and that year's closing balances are.  ``result_state_annual()`` is that
pairing published as a frame, and ``result_cf_annual()`` sums the monthly cash flows into
the same plan years.  The plan's own 1-based *ancienneté* year is ``plan_year(t)``, which
on an in-force cell is ahead of the projected plan year by ``duration_ifo``.

The conversion from the annual grid is asserted rather than assumed: the notes' twelve
worked-example rows carry the **same numbers they carried on the annual grid**, because
every one of them is an anniversary or rebalancing quantity and the monthly rates and
credit factors compound back to the annual ones exactly.  What moved — the claims, the
expenses and the split between the three decrements — has its own tests, named for the
reason it moved.

One naming point runs through the module.  The notes index the in force at the **end** of
the plan year and call it ``l(t)``; the library publishes the exposure at the **start** of
the period under the shared name ``pols_if``, because that is the weight the period's own
cash flows carry.  Both are here: ``pols_if(t)`` is the notes' ``l⁻(t)`` — 1 at ``t = 0``
and ``l(t - 1)`` afterwards — ``pols_if_at(t, "AFT_DECR")`` is ``l(t)``, and
``result_state()`` prints the latter as ``pols_if_eoy``.
The last column of ``WORKED_EXAMPLE`` below is the notes' ``l(t)``.

Beyond the worked example this module asserts each of the twelve "Known modeling
pitfalls" the notes list, because each is a way an implementation of *this* product can
look right and be wrong, and every test below is named for the failure it catches: the
monthly rates not compounding back to the annual ones; the management charge being spread
across the year, which leaves the account value alone and moves the *garantie plancher*
base; the regulatory euro-share minimum being tested between rebalancing dates, where it
is negative by construction; the
glide-path boundary belonging to the **tighter** band; a *versement* allocated at the
target mix and therefore not a switch; the arbitrage charge coming off the **source**
support, which on a de-risking switch is what keeps the euro share at or above the
regulatory minimum; that minimum binding at the **rebalancing date** rather than
continuously; the *garantie plancher* being a floor at *versements* net of loading and
net of charges and never at gross premiums; neither exit being a lapse, and an early
release paying the **whole** account value; the transfer indemnity window running from
the first *versement*; the three decrements not double-counting; the annuity conversion
factor being **undiscounted**, because a PER tariff is capped at a 0% technical rate;
commutation happening at the conversion basis against a **monthly** EUR 110 threshold;
per-policy and aggregate quantities not being multiplied together twice; and the
projection stopping at the declared horizon with tax outside it entirely.
"""
import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from fr_registry import LIB, MODELS


CENT = 0.005          # money displayed to 2 d.p.
POLS = 5e-7           # the in-force probability displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["PER_FR_S"][0]
PRODUCT_DIR = MODEL_DIR.parent

PROJ_LEN = 144        # the anchor cell's frame: 12 plan years of 12 months


def bom(year):
    """The **first** month of 0-based projected plan year ``year``: ``12 * year``.

    The rebalancing month: where the *versement* arrives, the glide path is re-read and
    the switch and its arbitrage charge are taken.  All five of those columns are nil in
    the other eleven months of the year.
    """
    return 12 * year


def anniv(year):
    """The month that **closes** 0-based projected plan year ``year``: ``12 * year + 11``.

    The anniversary month: where the management charge is levied on the post-crediting
    balance and, at ``year = proj_years() - 1``, where the plan is liquidated.  The
    closing balances, the *garantie plancher* base and the notes' ``l(t)`` are read here.
    """
    return 12 * year + 11


# plan year y (0-based): (k, a, arb, av_euro_pp, av_uc_pp, av_pp, l(y))
# The notes' worked-example table, read straight off the page, and UNCHANGED by the move
# to a monthly grid: every figure in it is an anniversary or rebalancing quantity.  k, a
# and arb are read at bom(y); the three balances and l at anniv(y).  V_net is 2,925.00 in
# every row and is asserted separately.  The last column is the notes' l(t), the in force
# at the END of the plan year, which the model publishes as
# pols_if_at(anniv(y), "AFT_DECR").
WORKED_EXAMPLE = {
    0:  (12, 0.00,     0.00,     0.00, 20357.74, 20357.74, 0.969289),
    1:  (11, 0.00,     0.00,     0.00, 24275.75, 24275.75, 0.939522),
    2:  (10, 0.20,    14.57,  5584.66, 22673.50, 28258.16, 0.910668),
    3:  (9,  0.20,     0.20,  6402.30, 26010.29, 32412.59, 0.882701),
    4:  (8,  0.20,     0.24,  7255.25, 29475.54, 36730.79, 0.855592),
    5:  (7,  0.20,     0.27,  8141.84, 33077.41, 41219.24, 0.829316),
    6:  (6,  0.20,     0.31,  9063.37, 36821.28, 45884.65, 0.803847),
    7:  (5,  0.50,    41.64, 25053.10, 25402.28, 50455.38, 0.779161),
    8:  (4,  0.50,     0.52, 27399.17, 27827.98, 55227.15, 0.755232),
    9:  (3,  0.50,     0.64, 29848.43, 30315.50, 60163.93, 0.732038),
    10: (2,  0.70,    36.80, 45335.35, 19695.53, 65030.89, 0.709557),
    11: (1,  0.70,     0.56, 48832.72, 21255.68, 70088.40, 0.687766),
}

# The notes' settlement table, per policy except where the label says otherwise.
SETTLEMENT = {
    "av_pp": 70088.40,
    "capital_leg_pp": 49061.88,
    "annuity_cap_pp": 21026.52,
    "rente_gross_pp": 955.75,
    "rente_net_pp": 941.41,
    "rente_net_mth": 78.45,
    "commuted_pp": 20711.12,
    "death_floor_pp": 47267.36,
}


def model_files(folder):
    """The model's own file names, ignoring interpreter caches."""
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def alt_model_point_file(model, rows, name):
    """Write a one-row model point table beside the model and point the model at it.

    The only way to assert that an invalid model point *raises* is to build one, and the
    shipped table cannot hold one — every row in it has to project.  The caller is
    responsible for deleting the file.
    """
    path = model.Data.input_dir() / name
    pd.DataFrame(rows).to_csv(path, index=False)
    model.Data.model_point_file = name
    model.Data.clear_all()
    model.Projection.clear_all()
    return path


def anchor_row(**overrides):
    """The anchor model point as a dict, with the named columns replaced."""
    table = pd.read_csv(PRODUCT_DIR / "model_point_table.csv")
    row = table[table["point_id"] == 1].iloc[0].to_dict()
    row.update(overrides)
    return row


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("y", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_per_anchor, y):
    """Every cell of the notes' table, to the precision the notes display.

    The rebalancing columns at ``bom(y)``, the balances and the in force at ``anniv(y)``.
    Not one of these figures moved when the grid became monthly.
    """
    k, a, arb, euro, uc, av, l_y = WORKED_EXAMPLE[y]
    p = fr_per_anchor
    assert p.years_to_horizon(bom(y)) == k
    assert p.alloc_euro(bom(y)) == pytest.approx(a, abs=1e-4)
    assert p.prem_to_av_pp(bom(y)) == pytest.approx(2925.00, abs=CENT)
    assert p.arbitrage_charge_pp(bom(y)) == pytest.approx(arb, abs=CENT)
    assert p.av_euro_pp(anniv(y)) == pytest.approx(euro, abs=CENT)
    assert p.av_uc_pp(anniv(y)) == pytest.approx(uc, abs=CENT)
    assert p.av_pp(anniv(y)) == pytest.approx(av, abs=CENT)
    assert p.pols_if_at(anniv(y), "AFT_DECR") == pytest.approx(l_y, abs=POLS)
    # result_state_annual() is exactly that pairing, published as the notes' table.
    row = p.result_state_annual().loc[y]
    assert row["years_to_horizon"] == k
    assert row["alloc_euro"] == pytest.approx(a, abs=1e-4)
    assert row["arbitrage_charge_pp"] == pytest.approx(arb, abs=CENT)
    assert row["av_pp"] == pytest.approx(av, abs=CENT)
    assert row["death_floor_pp"] == pytest.approx(p.death_floor_pp(anniv(y)), abs=CENT)
    assert row["pols_if_eoy"] == pytest.approx(l_y, abs=POLS)
    # The five rebalancing columns are nil in the other eleven months of the year.
    for t in range(bom(y) + 1, anniv(y) + 1):
        assert p.prem_to_av_pp(t) == 0.0, t
        assert p.switch_pp(t) == 0.0, t
        assert p.arbitrage_charge_pp(t) == 0.0, t


def test_the_worked_example_settlement(fr_per_anchor):
    """The notes' second table: capital leg, conversion, commutation test, lump sum."""
    p = fr_per_anchor
    s = p.result_settlement()
    for label, value in SETTLEMENT.items():
        assert s[label] == pytest.approx(value, abs=CENT), label
    assert p.annuity_share() == 0.30
    assert p.annuity_factor() == 22.0
    assert p.is_commuted() is True
    last = p.proj_len() - 1
    assert last == anniv(11) == 143
    assert p.claim_pp(last, "MATURITY") == pytest.approx(69773.00, abs=CENT)
    assert p.claims(last, "MATURITY") == pytest.approx(47987.47, abs=CENT)
    # The whole maturity claim is the account value less the arrerage charge on the
    # converted part, and nothing else: there is no exit charge on a PER.
    assert p.claim_pp(last, "MATURITY") == pytest.approx(
        p.av_pp(last) - 0.015 * p.annuity_cap_pp(), abs=CENT)
    # The settlement is not spread: it falls whole in the horizon-anniversary month.
    assert p.claims(last - 1, "MATURITY") == 0.0
    assert p.pols_maturity(last - 1) == 0.0


def test_the_aggregate_benefits_over_the_twelve_years(fr_per_anchor):
    """claims_death 2,106.52, claims_early_release 6,772.42, claims_transfer 4,211.07.

    These are the three figures the monthly grid **moved**, and they are recomputed
    goldens rather than the annual model's.  The annual grid produced 2,160.30, 6,878.40
    and 4,225.92; every one of them falls, and each for two reasons that this test states
    so the direction is not mistaken for an error.  A mid-year exit is now settled on the
    balance it actually holds in the month of exit, which is below the year-end balance
    the annual grid paid it on; and the *split* between the three decrements moves as the
    ordered chain is walked twelve times with small steps instead of once with large ones,
    which takes deaths and releases down and transfers up.  The two effects partly cancel
    on the transfer line, which is why it moves least.
    """
    df = fr_per_anchor.result_cf()
    assert df["claims_death"].sum() == pytest.approx(2106.52, abs=CENT)
    assert df["claims_early_release"].sum() == pytest.approx(6772.42, abs=CENT)
    assert df["claims_transfer"].sum() == pytest.approx(4211.07, abs=CENT)
    # Each is below the annual grid's figure, and by how much.
    assert df["claims_death"].sum() < 2160.30
    assert df["claims_early_release"].sum() < 6878.40
    assert df["claims_transfer"].sum() < 4225.92
    # The maturity claim is a horizon event and did not move at all.
    assert df["claims_maturity"].sum() == pytest.approx(47987.47, abs=CENT)


def test_the_maintenance_expense_scale(fr_per_anchor):
    """E(t) = (30/12) x 1.018^(t/12): E(0) = 2.50, E(143) = 3.0922, total 401.14.

    Recomputed goldens, and the two halves of the change have **opposite signs**, which
    is why both are asserted.  Per policy the twelve-year total rises from the annual
    grid's 397.87 to 401.14 (+0.82%), because the inflation factor now compounds every
    month instead of stepping once a year and the average of a year's twelve factors sits
    above the one at its start.  In aggregate it *falls*, from 334.87 to 332.82 (-0.61%),
    because the charge is now borne by the in force of each month rather than of the
    plan-year start - which is what makes a decrementing block cost less.
    """
    p = fr_per_anchor
    per_policy = [p.expenses(t) / p.pols_if(t) for t in range(PROJ_LEN)]
    assert per_policy[0] == pytest.approx(2.50, abs=CENT)
    assert per_policy[143] == pytest.approx(3.0922, abs=1e-4)
    assert sum(per_policy) == pytest.approx(401.14, abs=CENT)
    assert sum(per_policy) > 397.87                     # the annual grid's per-policy sum
    aggregate = p.result_cf()["expenses"].sum()
    assert aggregate == pytest.approx(332.82, abs=CENT)
    assert aggregate < 334.87                           # the annual grid's aggregate
    # The factor is exact at the month that opens a plan year: 1.018^(12y/12) = 1.018^y.
    for y in (0, 5, 11):
        assert p.inflation_factor(bom(y)) == pytest.approx(1.018 ** y, rel=1e-14)
    # The weight on the row is the in force at the START of the month, not the end - and
    # that is exactly the pols_if the same row of result_cf publishes.
    assert p.expenses(143) == pytest.approx(
        30.0 / 12 * 1.018 ** (143 / 12) * p.pols_if(143), rel=1e-12)
    assert p.pols_if(12) == pytest.approx(p.pols_if_at(11, "AFT_DECR"), rel=1e-14)
    assert p.expenses(143) == pytest.approx(
        30.0 / 12 * 1.018 ** (143 / 12) * p.result_cf().loc[143, "pols_if"], rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 1 - the glide-path band edge


def test_the_band_boundary_belongs_to_the_tighter_band(fr_per_anchor):
    """k = 10 reads 20%, k = 5 reads 50%, k = 2 reads 70% - not the looser band.

    The looser reading understates the euro share for a full year at each of three
    transitions, which on the anchor cell is three years of a 5.00% UC return where the
    grid asks for a 3.38% euro one.
    """
    p = fr_per_anchor
    edges = {11: 0.00, 10: 0.20, 6: 0.20, 5: 0.50, 3: 0.50, 2: 0.70, 1: 0.70}
    for k, share in edges.items():
        t = bom(p.proj_years() - k)          # the rebalancing month k years out
        assert p.years_to_horizon(t) == k
        assert p.alloc_euro(t) == pytest.approx(share, abs=1e-9), k
        # The band is a property of the plan year, not of the month: every month of the
        # year reads the same row.
        for u in range(t, t + 12):
            assert p.years_to_horizon(u) == k, u
            assert p.alloc_euro(u) == pytest.approx(share, abs=1e-9), u


def test_the_four_profiles_are_read_from_the_file(per_assurance):
    """The grid is an input table: four ladders, and dynamique equals offensif."""
    grid = per_assurance.Data.allocation_grid()
    expected = {
        "prudent":   (0.30, 0.60, 0.80, 0.90),
        "equilibre": (0.00, 0.20, 0.50, 0.70),
        "dynamique": (0.00, 0.00, 0.30, 0.50),
        "offensif":  (0.00, 0.00, 0.30, 0.50),
    }
    for profile, (far, mid, near, close) in expected.items():
        for k, share in ((20, far), (10, mid), (5, near), (2, close)):
            assert grid.loc[(profile, k), "euro_share"] == pytest.approx(
                share, abs=1e-9), (profile, k)
    # The two shares close in every row, which is what check_glide_path_closes asserts
    # on the years a projection actually reads.
    assert (grid["euro_share"] + grid["uc_share"]).sub(1.0).abs().max() < 1e-12


def test_a_prudent_cell_holds_euro_from_the_first_year(per_assurance):
    """Moving the grid is the product's dominant lever, and it needs no code change."""
    p = per_assurance.Projection[3]
    assert p.allocation_profile() == "prudent"
    assert p.years_to_horizon(0) == 19
    assert p.alloc_euro(0) == pytest.approx(0.30, abs=1e-9)
    assert p.av_euro_pp(0) > 0.0
    # The anchor cell, on the equilibre grid at 12 years out, holds none at all.
    assert per_assurance.Projection[1].alloc_euro(0) == 0.0
    assert per_assurance.Projection[1].av_euro_pp(0) == 0.0


# ---------------------------------------------------------------------------
# Pitfalls 2, 3 and 4 - the rebalancing and the arbitrage charge


def test_a_versement_is_not_a_switch(fr_per_anchor):
    """No arbitrage charge in a year that opens on target, though 3,000 was paid.

    New money is allocated at the target mix directly.  Charging it as though it were a
    switch would take 0.30% of every contribution for the life of the plan.
    """
    p = fr_per_anchor
    for y in (0, 1):
        assert p.premium_pp(bom(y)) == 3000.00
        assert p.switch_pp(bom(y)) == 0.0
        assert p.arbitrage_charge_pp(bom(y)) == 0.0
    # And the versement still reaches the account in full, net of the entry loading only.
    # The closing balance of the first plan year is the anniversary month, not month 0:
    # month 0 carries one month's growth and no charge.
    assert p.av_pp(anniv(0)) == pytest.approx(
        (16600.0 + 2925.0) * 1.05 * 0.993, abs=CENT)
    assert p.av_pp(0) == pytest.approx(
        (16600.0 + 2925.0) * (1.05 ** (1 / 12)), abs=CENT)


def test_the_arbitrage_charge_comes_off_the_source_support(fr_per_anchor):
    """Month 84, the eighth plan year: the UC bucket pays 41.64 and euro gets it all.

    The same three figures the annual grid produced at its ``t = 7``, read at the
    rebalancing month that opens the same plan year.
    """
    p = fr_per_anchor
    t = bom(7)
    assert t == 84
    assert p.switch_pp(t) == pytest.approx(13878.95, abs=CENT)
    assert p.arbitrage_charge_pp(t) == pytest.approx(41.64, abs=CENT)
    # The euro destination gets the whole switch plus its share of the versement.
    assert p.av_euro_pp_at(t, "BOM") == pytest.approx(24404.82, abs=CENT)
    assert p.av_euro_pp_at(t, "BOM") == pytest.approx(
        p.av_euro_pp_at(t, "BEF_REBAL") + p.switch_pp(t) + 0.50 * 2925.0, abs=CENT)
    assert p.av_euro_pp_at(t, "BEF_REBAL") == pytest.approx(
        p.av_euro_pp(anniv(6)), rel=1e-14)
    # The UC source pays for it.
    assert p.av_uc_pp_at(t, "BOM") == pytest.approx(
        p.av_uc_pp_at(t, "BEF_REBAL") - p.switch_pp(t)
        - p.arbitrage_charge_pp(t) + 0.50 * 2925.0, abs=CENT)


def test_the_post_rebalancing_euro_share_meets_the_minimum(fr_per_anchor):
    """50.04% against a 50% target at the t = 7 crossing, and never under all year.

    Taking the charge from the destination instead puts the share below the regulatory
    minimum by (1 - a) x arb at every band crossing.
    """
    p = fr_per_anchor
    t = bom(7)
    share = p.av_euro_pp_at(t, "BOM") / p.av_pp_at(t, "BOM")
    assert share == pytest.approx(0.500427, abs=1e-6)
    assert share >= p.alloc_euro(t)
    assert p.check_euro_share_min() is True
    # The check measures the REBALANCING months only, and that restriction is the point:
    # between dates the mix drifts and the residual is negative by construction.
    for u in range(0, p.proj_len(), 12):
        assert p.euro_share_min_bound(u) == 0.0, u
        assert p.check_euro_share_min_resid(u) >= -1e-8, u
    drifted = [u for u in range(p.proj_len())
               if p.check_euro_share_min_resid(u) < -1e-8]
    assert drifted, "the restriction to rebalancing months must be tested, not assumed"
    assert all(u % 12 != 0 for u in drifted)


def test_a_reverse_switch_is_the_one_case_the_convention_cannot_cover(per_assurance):
    """Model point 2 arrives at 40% euro against a 20% minimum and sells euro down.

    The euro support is then the *source*, so charging the source takes the charge out of
    the very balance the minimum is measured on and leaves it (1 - a) x arb below the
    line.  The notes ask both for a symmetric formula and for a share at or above the
    minimum, and in this direction the two cannot both hold; the model implements the
    formula and states the bound.
    """
    p = per_assurance.Projection[2]
    assert p.switch_pp(0) == pytest.approx(-4000.00, abs=CENT)
    assert p.arbitrage_charge_pp(0) == pytest.approx(12.00, abs=CENT)
    assert p.check_euro_share_min_resid(0) == pytest.approx(-9.60, abs=CENT)
    assert p.euro_share_min_bound(0) == pytest.approx(-9.60, abs=CENT)
    assert p.check_euro_share_min() is True
    # It happens once and only at the arrival, because the euro support then grows more
    # slowly than the UC bucket and falls back below the minimum on its own.
    assert all(p.switch_pp(t) >= 0.0 for t in range(12, p.proj_len(), 12))
    # And there is no switch at all outside the rebalancing months.
    assert all(p.switch_pp(t) == 0.0
               for t in range(p.proj_len()) if t % 12 != 0)


def test_the_minimum_binds_at_the_rebalancing_date_not_continuously(fr_per_anchor):
    """70.0006% at month 132, 69.67% at month 143 - eleven months of drift between.

    On the annual grid these two numbers were an instant apart and the distinction was
    almost vacuous.  On the monthly grid there are eleven months between them in which the
    euro share falls monotonically below the target, so the restriction of
    ``check_euro_share_min`` to rebalancing months is load-bearing rather than cosmetic.
    """
    p = fr_per_anchor
    assert p.alloc_euro(bom(11)) == pytest.approx(0.70, abs=1e-9)
    opening = p.av_euro_pp_at(bom(11), "BOM") / p.av_pp_at(bom(11), "BOM")
    closing = p.av_euro_pp(anniv(11)) / p.av_pp(anniv(11))
    assert bom(11) == 132 and anniv(11) == 143
    assert opening == pytest.approx(0.700006, abs=1e-6)
    assert closing == pytest.approx(0.696730, abs=1e-6)
    assert closing < 0.70
    # The drift is monotone across the eleven months in between, and every one of them
    # sits below the target - which is why none of them is a compliance statement.
    shares = [p.av_euro_pp(t) / p.av_pp(t) for t in range(bom(11), anniv(11) + 1)]
    assert all(b < a for a, b in zip(shares, shares[1:]))
    assert all(s < 0.70 for s in shares)
    # Re-imposing the target every month would invent a rebalancing frequency the
    # contract does not have, so nothing in the model reads the intra-year share.


# ---------------------------------------------------------------------------
# Pitfall 5 - the garantie plancher


def test_the_floor_is_not_a_floor_at_gross_premiums(fr_per_anchor):
    """A(t) - g(t) = [A-(0) - g-(0)] + cumulative gross investment return, exactly.

    A base accumulated at gross V rather than V_net, or one that forgets the arbitrage
    charge, or one charged something other than what the account was charged, breaks this
    in the first year in which it is wrong.
    """
    p = fr_per_anchor
    # The opening state is the BEF_REBAL timing of the first row, not a row of its own.
    assert p.death_floor_pp_at(0, "BEF_REBAL") == 16000.00
    assert p.av_pp_at(0, "BEF_REBAL") == 16600.00
    gap = p.av_pp(anniv(11)) - p.death_floor_pp(anniv(11))
    assert gap == pytest.approx(22821.04, abs=CENT)
    credited = sum(p.inv_income_pp(t) for t in range(PROJ_LEN))
    assert credited == pytest.approx(22221.04, abs=CENT)
    assert gap == pytest.approx(600.00 + credited, abs=CENT)
    assert p.check_floor_identity() is True
    # The first plan year alone: the base grows by V_net less the charge, not by gross V,
    # and the charge falls in the anniversary month and nowhere else.
    assert p.mgmt_charge_pp(0) == 0.0
    assert p.death_floor_pp(0) == pytest.approx(16000.0 + 2925.0, abs=CENT)
    charge = p.mgmt_charge_pp(anniv(0))
    assert charge == pytest.approx(143.51, abs=CENT)
    assert p.death_floor_pp(anniv(0)) == pytest.approx(
        16000.0 + 2925.0 - charge, abs=CENT)
    assert p.death_floor_pp(anniv(0)) < 16000.0 + 3000.0
    # The base is FLAT through the eleven months between those two events.
    for t in range(0, anniv(0)):
        assert p.death_floor_pp(t) == pytest.approx(18925.00, abs=CENT), t
        assert p.mgmt_charge_pp(t) == 0.0, t


def test_the_floor_bites_only_where_investment_return_is_negative(per_assurance):
    """Model point 10 is the anchor cell with a 19,000 opening base rather than 16,000.

    It opens 2,400 above the account value - a plan whose accumulated investment return
    to date is negative - so the floor bites until cumulative return overtakes it, and
    then stops.
    """
    p = per_assurance.Projection[10]
    assert p.death_floor_init() == 19000.00
    assert p.death_benefit_pp(0) == pytest.approx(p.death_floor_pp(0), abs=CENT)
    assert p.death_benefit_pp(0) > p.av_pp(0)
    # The monthly grid locates the crossing to the MONTH: the base is flat inside a plan
    # year while the account value grows every month, so the floor stops biting two
    # months into the third plan year rather than at its start.
    assert p.death_benefit_pp(24) == pytest.approx(p.death_floor_pp(24), abs=CENT)
    assert p.death_benefit_pp(26) == pytest.approx(p.av_pp(26), abs=CENT)
    assert p.death_floor_pp(26) < p.av_pp(26)
    floored = [t for t in range(p.proj_len())
               if p.death_benefit_pp(t) > p.av_pp(t) + 1e-9]
    assert floored == list(range(26))
    # It costs more than the anchor cell, and only through the death benefit.
    base = per_assurance.Projection[1].result_cf()
    assert (p.result_cf()["claims_death"].sum()
            > base["claims_death"].sum())


def test_the_cover_ceases_at_seventy_and_is_capped_across_contracts(per_assurance):
    """Model point 9 retires at 70, so the cover switches off in its final plan year."""
    assert per_assurance.Projection.floor_cease_age == 70
    assert per_assurance.Projection.death_floor_cap == 762245.0
    p = per_assurance.Projection[9]
    # age(t) is the age the PLAN YEAR opens at and steps at the anniversary, so the year
    # closes at age(t) + 1 and the cover is off for the whole plan year that ends on the
    # 70th birthday.  The rule stays on the plan year: the notes' age basis is an integer
    # attained age incremented once a year, and a month-exact rule would need a
    # sub-annual age this product does not have.
    assert p.proj_len() == 48
    assert [p.age(bom(y)) for y in range(4)] == [66, 67, 68, 69]
    assert [p.age(t) for t in (0, 12, 24, 36)] == [66, 67, 68, 69]
    assert [p.floor_in_force(t) for t in (0, 12, 24, 36)] == [
        True, True, True, False]
    # The age, and so the cover, is constant through the twelve months of a plan year.
    assert all(p.age(t) == 69 for t in range(36, 48))
    assert all(p.floor_in_force(t) is False for t in range(36, 48))
    assert p.death_benefit_pp(36) == p.av_pp(36)
    # And a cell that never carried the cover is never floored at all.
    off = per_assurance.Projection[11]
    assert off.death_floor_flag() is False
    for t in range(off.proj_len()):
        assert off.floor_in_force(t) is False
        assert off.death_benefit_pp(t) == off.av_pp(t)


# ---------------------------------------------------------------------------
# Pitfalls 6 and 7 - the two exits, neither of which is a lapse


def test_there_is_no_lapse_machinery_anywhere(per_assurance):
    """A cited product fact: the plan is blocked and carries no surrender right.

    Naming either exit a lapse attaches a surrender formula - a charge, a market value
    adjustment, a surrender value - to an event that has none of them.
    """
    names = set(per_assurance.Projection.cells) | set(per_assurance.Projection.refs)
    for absent in ("lapse_rate", "lapse_rate_ann", "lapse_rate_mth", "pols_lapse",
                   "surr_rate", "surr_charge_rate", "surr_value_pp", "cv_pp",
                   "mvr_pp", "dyn_lapse_factor", "withdrawals", "wd_pp"):
        assert absent not in names, absent
    # And the two exits are named for what they are, on both speeds of the grid.
    for present in ("early_release_rate", "early_release_rate_mth",
                    "transfer_out_rate", "transfer_out_rate_mth",
                    "mort_rate", "mort_rate_mth"):
        assert present in names, present
    columns = per_assurance.Projection[1].result_cf().columns
    for absent in ("claims_lapse", "claims_surr", "claims_wd", "withdrawals"):
        assert absent not in columns, absent


def test_an_early_release_pays_the_whole_account_value(fr_per_anchor):
    """No charge, no reduction: the seven statutory cases carry neither.

    A transfer out of the same cell in the same year pays 1% less, which is the whole
    difference between the two exits and the reason they are two decrements.
    """
    p = fr_per_anchor
    for t in (0, 60, 143):
        assert p.claim_pp(t, "EARLY_RELEASE") == p.av_pp(t)
        assert p.claims(t, "EARLY_RELEASE") == pytest.approx(
            p.pols_release(t) * p.av_pp(t), rel=1e-14)
    assert p.claim_pp(0, "TRANSFER") == pytest.approx(0.99 * p.av_pp(0), rel=1e-14)
    assert p.early_release_rate(0) == 0.016
    assert p.transfer_out_rate(0) == 0.010


def test_the_transfer_indemnity_window_runs_from_the_first_versement(fr_per_anchor):
    """duration_ifo = 2, so the window covers t = 0 and t = 1 and nothing after.

    Measuring it from the projection start instead would charge the indemnity for five
    projected years on a plan that is already three years old.
    """
    p = fr_per_anchor
    assert p.duration_ifo() == 2
    # duration(t) is the 0-based elapsed count the plan year opens with; plan_year(t) is
    # the 1-based label the ancienneté schedules are written in.  Both step at the
    # anniversary, not monthly.
    assert [p.duration(t) for t in (0, 12, 24)] == [2, 3, 4]
    assert [p.plan_year(t) for t in (0, 12, 24)] == [3, 4, 5]
    assert [p.duration(t) for t in (0, 11)] == [2, 2]
    # The plan-year test is EXACTLY a month test on the monthly grid, not an
    # approximation of one, because duration_ifo is a whole number of years: the window
    # runs to 12 x (transfer_indemnity_years - 1) = 48 months from the first versement,
    # which on this cell is months 0 to 23 and nothing after.  Identical on either grid.
    window = 12 * (5 - 1)                        # transfer_indemnity_years - 1, in years
    for t in range(p.proj_len()):
        assert (p.plan_year(t) < 5) == (12 * p.duration_ifo() + t < window), t
    assert window == 48
    for t in (0, 11, 12, 23):
        assert p.transfer_indemnity_rate(t) == 0.01
        assert p.claims(t, "TRANSFER") / (p.pols_transfer(t) * p.av_pp(t)) == (
            pytest.approx(0.99, rel=1e-12))
    for t in (24, 84, 143):
        assert p.transfer_indemnity_rate(t) == 0.0
        assert p.claims(t, "TRANSFER") / (p.pols_transfer(t) * p.av_pp(t)) == (
            pytest.approx(1.00, rel=1e-12))


def test_a_new_plan_carries_the_indemnity_for_four_projected_years(per_assurance):
    """Model point 3 opens at duration 0, so its window closes at month 48."""
    p = per_assurance.Projection[3]
    assert p.duration_ifo() == 0
    assert [p.transfer_indemnity_rate(bom(y)) for y in range(6)] == [
        0.01, 0.01, 0.01, 0.01, 0.0, 0.0]
    # To the month: the last covered month is 47 and the first uncovered one is 48.
    assert [p.transfer_indemnity_rate(t) for t in (0, 36, 47, 48, 60)] == [
        0.01, 0.01, 0.01, 0.0, 0.0]


def test_compartment_three_carries_a_reduced_release_rate(per_assurance):
    """The main-residence case is the only discretionary limb, and c3 is excluded."""
    c1 = per_assurance.Projection[1]
    c3 = per_assurance.Projection[2]
    assert c3.compartment() == "c3"
    assert c3.early_release_rate(0) < c1.early_release_rate(0)
    # The transfer rate does not vary by compartment: a transfer moves the rights
    # without changing them.
    assert c3.transfer_out_rate(0) == c1.transfer_out_rate(0)


# ---------------------------------------------------------------------------
# Pitfall 8 - double-counting the exits


def test_the_three_decrements_do_not_double_count(per_assurance):
    """d_death + d_release + d_transfer + l(t) = l⁻(t), exactly, in every year.

    Applying two decrements to the same start-of-year in force instead of in sequence
    removes more of the book than exists, and every downstream number stays plausible.
    """
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        assert p.check_pols_roll_fwd() is True, point_id
        for t in range(p.proj_len()):
            assert abs(p.check_pols_roll_fwd_resid(t)) < 1e-12, (point_id, t)


def test_the_decrement_order_is_death_then_release_then_transfer(fr_per_anchor):
    """An ordered dependent-decrement convention at the MONTHLY rates, step by step."""
    p = fr_per_anchor
    q = p.mort_rate_mth(0)
    we = p.early_release_rate_mth(0)
    wr = p.transfer_out_rate_mth(0)
    assert p.pols_if_at(0, "BEF_DECR") == 1.0
    assert p.pols_if_at(0, "BEF_RELEASE") == pytest.approx(1 - q, rel=1e-14)
    assert p.pols_if_at(0, "BEF_TRANSFER") == pytest.approx(
        (1 - q) * (1 - we), rel=1e-14)
    assert p.pols_if_at(0, "AFT_DECR") == pytest.approx(
        (1 - q) * (1 - we) * (1 - wr), rel=1e-14)
    assert p.pols_release(0) == pytest.approx((1 - q) * we, rel=1e-14)
    assert p.pols_transfer(0) == pytest.approx((1 - q) * (1 - we) * wr, rel=1e-14)


def test_the_monthly_rates_compound_back_to_the_annual_ones(fr_per_anchor):
    """q_m, w_e,m and w_r,m are the constant-force conversion of the annual rates.

    This is what makes the two grids reconcile at every anniversary, so it is asserted
    directly rather than only through its consequence.  Note the shape of the assertion:
    ``1 - (1 - q_m)^12 == q``, **not** ``12 q_m == q``.  The conversion is geometric and
    has no such linearity - on the anchor cell ``12 q_m = 0.0050115`` against a stated
    ``q = 0.00500``, so dividing by twelve would overstate the plan year's mortality by
    0.23%.  The only safe monotonic statement is ``q_m < q``.
    """
    p = fr_per_anchor
    for t in (0, 5, 13, 84, 143):
        for ann, mth in ((p.mort_rate, p.mort_rate_mth),
                         (p.early_release_rate, p.early_release_rate_mth),
                         (p.transfer_out_rate, p.transfer_out_rate_mth)):
            assert 1 - (1 - mth(t)) ** 12 == pytest.approx(ann(t), rel=1e-12), t
            assert mth(t) < ann(t)
            assert 12 * mth(t) != pytest.approx(ann(t), rel=1e-9)
    # The two credited returns take the same treatment in interest form.
    assert (1 + p.return_euro_mth()) ** 12 == pytest.approx(1.0338, rel=1e-14)
    assert (1 + p.return_uc_mth()) ** 12 == pytest.approx(1.05, rel=1e-14)
    assert p.return_euro_mth() == pytest.approx(0.00277395, abs=1e-8)
    assert p.return_uc_mth() == pytest.approx(0.00407412, abs=1e-8)
    # The annual rate is a property of the plan year, not of the month.
    assert len({p.mort_rate(t) for t in range(bom(7), anniv(7) + 1)}) == 1
    assert len({p.early_release_rate(t) for t in range(bom(7), anniv(7) + 1)}) == 1


def test_the_monthly_grid_moves_the_decrement_split_and_not_the_total(fr_per_anchor):
    """The in force at every anniversary is the annual model's; the split is not.

    Walking the ordered chain twelve times with small steps dilutes the later decrements
    less than walking it once with large ones, so deaths and releases fall and transfers
    rise while the total decrement of the plan year is unchanged.  That looks like an
    error and is not, so it is asserted as arithmetic: the annual recursion is written out
    here from the model's own annual vectors rather than taken from a fixture.
    """
    p = fr_per_anchor
    expected = p.pols_if_init()
    for y in range(p.proj_years()):
        assert p.pols_if(bom(y)) == pytest.approx(expected, abs=1e-12), y
        t = bom(y)
        expected *= ((1 - p.mort_rate(t)) * (1 - p.early_release_rate(t))
                     * (1 - p.transfer_out_rate(t)))
    # The split over the anchor cell's first plan year: deaths and releases below the
    # annual grid's, transfers above, and the three still summing to the same total.
    months = range(bom(0), anniv(0) + 1)
    deaths = sum(p.pols_death(t) for t in months)
    releases = sum(p.pols_release(t) for t in months)
    transfers = sum(p.pols_transfer(t) for t in months)
    assert deaths == pytest.approx(0.00494056, abs=1e-8)          # annual: 0.00500000
    assert releases == pytest.approx(0.01588375, abs=1e-8)        # annual: 0.01592000
    assert transfers == pytest.approx(0.00988649, abs=1e-8)       # annual: 0.00979080
    assert deaths < 0.005                       # the annual grid's q x l(0)
    assert releases < 0.01592                   # the annual grid's (1 - q) w_e
    assert transfers > 0.0097908                # the annual grid's (1 - q)(1 - w_e) w_r
    total = deaths + releases + transfers
    annual_total = 1.0 - ((1 - p.mort_rate(0)) * (1 - p.early_release_rate(0))
                          * (1 - p.transfer_out_rate(0)))
    assert total == pytest.approx(annual_total, rel=1e-13)


def test_the_account_value_roll_forward_closes(per_assurance):
    """A(t) = A-(t) + V_net - arb + return credited - charge levied.

    A conservation statement: the switch does not appear in it, because it moves money
    between the supports rather than across the plan's boundary.
    """
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        assert p.check_av_roll_fwd() is True, point_id


# ---------------------------------------------------------------------------
# Pitfalls 9 and 10 - the annuity conversion and its commutation


def test_the_conversion_factor_is_undiscounted(fr_per_anchor):
    """A PER tariff may not use a technical rate above 0%, so a_x counts instalments.

    Nothing in the model discounts it: rente_gross is a plain division, and multiplying
    the instalment back by the factor returns the converted capital exactly.  A 2% rate
    would shorten the factor from 22.0000 to 17.658 - a fall of 19.7% - and so inflate the
    annuity, which is annuity_cap divided by the factor, by 22 / 17.658 - 1 = 24.6%.  The
    two percentages are different numbers and quoting the first as the second is the slip
    this assertion pins down.
    """
    p = fr_per_anchor
    assert p.annuity_factor() == 22.0
    assert p.rente_gross_pp() * p.annuity_factor() == pytest.approx(
        p.annuity_cap_pp(), rel=1e-14)
    discounted = sum(1.02 ** -k for k in range(1, 23))
    assert discounted == pytest.approx(17.658, abs=0.001)
    # The factor falls by about a fifth ...
    assert 1.0 - discounted / p.annuity_factor() == pytest.approx(0.197, abs=0.001)
    # ... and the annuity therefore rises by about a quarter, which is not the same
    # number.  Both documents must quote the second one.
    assert p.annuity_cap_pp() / discounted / p.rente_gross_pp() == pytest.approx(
        1.246, abs=0.001)


def test_commutation_returns_the_capital_less_the_arrerage_charge(fr_per_anchor):
    """commuted = rente_net x a_x = annuity_cap x (1 - c_arr), to the cent.

    Commuting at a book value instead manufactures a gain out of nothing.
    """
    p = fr_per_anchor
    assert p.commuted_pp() == pytest.approx(
        p.rente_net_pp() * p.annuity_factor(), rel=1e-14)
    assert p.commuted_pp() == pytest.approx(
        p.annuity_cap_pp() * 0.985, rel=1e-14)
    assert p.commuted_pp() == pytest.approx(20711.12, abs=CENT)
    assert p.check_commutation_identity() is True


def test_the_commutation_threshold_is_monthly(per_assurance):
    """EUR 110 a month, scaled by the months in the payment period - so 1,320 a year.

    Testing an annual instalment against 110 would commute almost nothing, and testing a
    monthly one against 1,320 would commute almost everything.
    """
    assert per_assurance.Projection.commute_threshold_mth == 110.0
    assert per_assurance.Projection.payment_mths == 12
    p = per_assurance.Projection[1]
    assert p.rente_net_pp() == pytest.approx(941.41, abs=CENT)
    assert p.result_settlement()["rente_net_mth"] == pytest.approx(78.45, abs=CENT)
    # The annual instalment is well above 110 and the monthly one well below it, so the
    # two readings of the threshold give opposite answers on the same cell.
    assert 78.45 <= 110.0 < 941.41
    assert p.is_commuted() is True


def test_the_commutation_cliff(per_assurance):
    """Model point 6 is the anchor cell at a 50% annuity share, above the threshold.

    The cliff sits at 42.06% of the settlement balance; below it the annuity reverses at
    settlement into a lump sum, above it a rente is paid and the capital is handed to
    Rente_FR_S.
    """
    p1, p6 = per_assurance.Projection[1], per_assurance.Projection[6]
    assert p6.av_pp(143) == pytest.approx(p1.av_pp(143), rel=1e-14)
    assert p6.annuity_share() == 0.50
    assert p6.rente_net_pp() == pytest.approx(1569.02, abs=CENT)
    assert p6.result_settlement()["rente_net_mth"] == pytest.approx(130.75, abs=CENT)
    assert p6.is_commuted() is False
    assert p6.commuted_pp() == 0.0
    assert p6.annuity_conversion_pp() == pytest.approx(p6.annuity_cap_pp(), rel=1e-14)
    # The cliff itself: 110 x 12 / (1 - c_arr) x a_x / A(T-1).
    cliff = 110.0 * 12 / 0.985 * 22.0 / p1.av_pp(143)
    assert cliff == pytest.approx(0.4206, abs=1e-4)


def test_the_two_annuity_legs_are_mutually_exclusive(per_assurance):
    """Commuted money leaves as claims_maturity; a rente leaves as annuity_conversion."""
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        assert min(p.commuted_pp(), p.annuity_conversion_pp()) == 0.0, point_id
        df = p.result_cf()
        t_last = p.proj_len() - 1
        assert df["annuity_conversion"].sum() == pytest.approx(
            df.loc[t_last, "annuity_conversion"], rel=1e-14)


def test_a_capital_only_exit_has_no_annuity_at_all(per_assurance):
    """Model point 7 elects capital in one payment: theta = 0 and nothing to commute."""
    p = per_assurance.Projection[7]
    assert p.exit_form() == "capital_single"
    assert p.annuity_share() == 0.0
    assert p.annuity_cap_pp() == 0.0
    assert p.is_commuted() is False
    assert p.annuity_conversion_pp() == 0.0
    t_last = p.proj_len() - 1
    assert p.claim_pp(t_last, "MATURITY") == pytest.approx(
        p.av_pp(t_last), rel=1e-14)


def test_staged_capital_publishes_its_instalment_and_settles_at_the_horizon(
        per_assurance):
    """A documented simplification: the fractionne option changes when, not how much."""
    p = per_assurance.Projection[8]
    assert p.exit_form() == "capital_staged"
    assert p.capital_instalments() == 5
    assert p.capital_instalment_pp() == pytest.approx(
        p.capital_leg_pp() / 5, rel=1e-14)
    assert p.proj_years() == p.retirement_age() - p.age_init()
    assert p.proj_len() == 12 * (p.retirement_age() - p.age_init())
    t_last = p.proj_len() - 1
    assert p.claims(t_last, "MATURITY") == pytest.approx(
        p.capital_leg_pp() * p.pols_maturity(t_last), rel=1e-12)


def test_a_compartment_three_cell_must_elect_the_annuity(per_assurance):
    """Those rights may be delivered no other way, so the model refuses the alternative."""
    p = per_assurance.Projection[2]
    assert p.compartment() == "c3"
    assert p.exit_form() == "annuity"
    assert p.annuity_share() == 1.0
    assert p.capital_leg_pp() == 0.0


# ---------------------------------------------------------------------------
# Pitfall 11 - per policy against aggregate


def test_the_account_value_column_is_per_policy_and_the_claims_are_not(fr_per_anchor):
    """Multiplying a claims column by pols_if again squares the survival factor."""
    p = fr_per_anchor
    df = p.result_cf()
    assert df.loc[143, "av_pp"] == pytest.approx(70088.40, abs=CENT)
    assert df.loc[143, "av_pp"] > df.loc[143, "claims_maturity"]
    # av_at is the weighted quantity where one is wanted, and it is not in result_cf.
    # At EOM the weight is the END-of-month count, which is pols_if_at(t, "AFT_DECR").
    assert p.av_at(143, "EOM") == pytest.approx(
        p.av_pp(143) * p.pols_if_at(143, "AFT_DECR"), rel=1e-14)
    assert p.av_at(143, "BOM") == pytest.approx(
        p.av_pp_at(143, "BOM") * p.pols_if(143), rel=1e-14)
    assert "av_at" not in df.columns
    # Every claims column is already a decrement times a per-policy amount.
    assert df.loc[65, "claims_death"] == pytest.approx(
        p.pols_death(65) * p.death_benefit_pp(65), rel=1e-14)


# ---------------------------------------------------------------------------
# Pitfall 12 - the horizon, and tax


def test_the_projection_stops_at_the_declared_horizon(per_assurance):
    """No versement after settlement, k never negative, one maturity year."""
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        n = p.proj_len()
        assert n == 12 * (p.retirement_age() - p.age_init()), point_id
        # n rows, labelled 0 .. n - 1: proj_len() is a count of MONTHS, not the last
        # index, and result_cf() carries one row per month.
        assert list(p.result_cf().index) == list(range(n)), point_id
        assert len(p.result_cf_annual()) == p.proj_years(), point_id
        # The last versement falls in the month that opens the last plan year, not in
        # the last month - and none falls in between.
        assert p.premium_pp(n - 12) > 0.0 or p.premium_init() == 0.0
        assert p.premium_pp(1) == 0.0
        assert p.premium_pp(n - 1) == 0.0 or p.proj_years() == 0
        assert p.premium_pp(n) == 0.0
        assert p.years_to_horizon(n) == 0
        assert p.check_horizon() is True, point_id


def test_the_deduction_election_is_carried_and_inert(per_assurance):
    """It changes what the holder keeps, never what the insurer pays.

    The anchor cell with the election flipped produces the identical cash flow table, to
    the last floating-point bit.  Tax appears in no recursion in this model: the
    deductibility of the *versements* moves the exit taxation between the pension regime
    and the *rente viagère à titre onéreux* fractions, and the insurer pays the same euro
    amount either way.
    """
    base = per_assurance.Projection[1].result_cf()
    assert per_assurance.Projection[1].deduction_elected() is True
    assert set(per_assurance.Data.model_point_table()["deduction_elected"]) == {
        True, False}

    model = mx.read_model(MODEL_DIR, name="PER_FR_S_ded")
    try:
        path = alt_model_point_file(
            model, [anchor_row(deduction_elected=False)],
            "model_point_table_ded.csv")
        try:
            p = model.Projection[1]
            assert p.deduction_elected() is False
            flipped = p.result_cf()
        finally:
            path.unlink(missing_ok=True)
    finally:
        model.close()

    assert (flipped - base).abs().max().max() == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------------------
# Model points the shipped tables must refuse


def test_a_c3_cell_electing_capital_raises():
    """The compartment rule is enforced, not assumed - and the table cannot hold the row."""
    model = mx.read_model(MODEL_DIR, name="PER_FR_S_c3")
    try:
        path = alt_model_point_file(
            model, [anchor_row(compartment="c3", exit_form="mixed")],
            "model_point_table_c3.csv")
        try:
            with pytest.raises(FormulaError):
                model.Projection[1].exit_form()
        finally:
            path.unlink(missing_ok=True)
    finally:
        model.close()


def test_an_annuity_share_contradicting_the_exit_form_raises():
    """capital_single with a 30% annuity share is two statements, not one."""
    model = mx.read_model(MODEL_DIR, name="PER_FR_S_share")
    try:
        path = alt_model_point_file(
            model, [anchor_row(exit_form="capital_single", annuity_share=0.30)],
            "model_point_table_share.csv")
        try:
            with pytest.raises(FormulaError):
                model.Projection[1].annuity_share()
        finally:
            path.unlink(missing_ok=True)
    finally:
        model.close()


def test_invalid_enum_values_raise(fr_per_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_per_anchor.claim_pp(0, "SURRENDER")
    with pytest.raises(FormulaError):
        fr_per_anchor.claims(0, "LAPSE")
    with pytest.raises(FormulaError):
        fr_per_anchor.av_pp_at(0, "MID")
    with pytest.raises(FormulaError):
        fr_per_anchor.pols_if_at(0, "AFT_SURR")
    with pytest.raises(FormulaError):
        fr_per_anchor.death_floor_pp_at(0, "MID")
    # The year strings were retired with the annual grid: an "EOY" returned for month
    # five of a plan year would be a label that lies, so it raises instead.
    with pytest.raises(FormulaError):
        fr_per_anchor.av_pp_at(0, "BOY")
    with pytest.raises(FormulaError):
        fr_per_anchor.av_pp_at(0, "EOY")
    with pytest.raises(FormulaError):
        fr_per_anchor.death_floor_pp_at(0, "EOY")
    with pytest.raises(FormulaError):
        fr_per_anchor.av_at(0, "EOY")


# ---------------------------------------------------------------------------
# Mortality


def test_the_two_mortality_bases_agree_in_the_anchor_cell_first_year(per_assurance):
    """The table's level is anchored so that mort_be_factor x q(M, 52) is 0.00500."""
    flat = per_assurance.Projection[1]
    assert flat.mort_basis() == "flat"
    assert flat.mort_rate(0) == 0.005
    assert all(flat.mort_rate(t) == 0.005 for t in range(144))
    table = per_assurance.Data.mort_table()
    anchored = float(table.loc[("M", 52), "mort_rate"]) * (
        per_assurance.Projection.mort_be_factor)
    assert anchored == pytest.approx(0.00500, rel=1e-12)
    # A table cell reads the age at the START of the plan year.
    tabled = per_assurance.Projection[3]
    assert tabled.mort_basis() == "table"
    assert tabled.mort_rate(0) == pytest.approx(
        float(table.loc[("M", tabled.age_init()), "mort_rate"]) * 0.85, rel=1e-12)
    # It steps at the anniversary and not monthly: constant through a plan year, higher
    # in the next one.
    assert tabled.mort_rate(1) == tabled.mort_rate(0)
    assert tabled.mort_rate(11) == tabled.mort_rate(0)
    assert tabled.mort_rate(12) > tabled.mort_rate(0)
    assert tabled.age(11) == tabled.age_init()
    assert tabled.age(12) == tabled.age_init() + 1


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """A population-shaped proxy with an anchored level, and the file says so."""
    table = pd.read_csv(PRODUCT_DIR / "mort_table.csv")
    assert len(set(table["provenance"])) == 1
    note = table["provenance"].iloc[0]
    assert note.startswith("[std]")
    assert "INSEE" in note
    assert table["mort_rate"].max() <= 1.0
    assert set(table["sex"]) == {"M", "F"}
    # Female mortality is lighter than male at every age in the table.
    wide = table.pivot(index="age", columns="sex", values="mort_rate")
    assert (wide["F"] <= wide["M"]).all()


def test_the_exit_table_marks_its_own_provenance_and_avoids_the_word_lapse():
    """The decrements are [std] and the file names them for what they are."""
    table = pd.read_csv(PRODUCT_DIR / "exit_table.csv")
    assert list(table.columns) == [
        "compartment", "duration", "early_release_rate", "transfer_out_rate",
        "provenance"]
    assert all(n.startswith("[std]") for n in set(table["provenance"]))
    assert "lapse" not in " ".join(table.columns).lower()
    # The duration key is the plan's own 1-based anciennete year, which is why the model
    # reads it with plan_year(t) and not with the 0-based duration(t).
    assert table["duration"].min() == 1
    assert set(table["compartment"]) == {"c1", "c2", "c3"}
    c1 = table[table["compartment"] == "c1"]
    c3 = table[table["compartment"] == "c3"]
    assert c1["early_release_rate"].max() == 0.016
    assert c3["early_release_rate"].max() < 0.016
    assert set(table["transfer_out_rate"]) == {0.01}


def test_the_annuity_factor_table_marks_itself_a_placeholder():
    """TGH05 / TGF05 are cited and not shipped, and the file says so."""
    table = pd.read_csv(PRODUCT_DIR / "annuity_factor.csv")
    assert all("[std]" in n and "TGH05" in n for n in set(table["provenance"]))
    male64 = table[(table["sex"] == "M") & (table["age"] == 64)]
    assert male64["annuity_factor"].iloc[0] == pytest.approx(22.0, rel=1e-12)
    assert (table["annuity_factor"] > 0).all()
    # The factor falls with age on both sexes: fewer instalments remain.
    for sex in ("M", "F"):
        column = table[table["sex"] == sex].sort_values("age")["annuity_factor"]
        assert column.is_monotonic_decreasing


# ---------------------------------------------------------------------------
# Structure, sign convention and inputs


COLUMNS = [
    "pols_if", "av_pp", "premiums", "claims_death", "claims_early_release",
    "claims_transfer", "claims_maturity", "annuity_conversion", "expenses",
    "liability_cf", "net_cf",
]


def test_result_cf_shape(fr_per_anchor):
    df = fr_per_anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(PROJ_LEN))
    assert len(df) == fr_per_anchor.proj_len()
    assert list(df.columns) == COLUMNS


def test_result_cf_annual_is_the_monthly_frame_regrouped(fr_per_anchor):
    """The plan-year view is the same frame, not a second projection.

    Cash flow columns sum; ``pols_if`` is the count ENTERING the plan year, which is what
    the annual-step model carried on the same row; ``av_pp`` is the balance CLOSING it,
    which is what ``av_pp(t)`` meant on the annual grid.  Summing a state variable over
    twelve months would be meaningless, so neither of those two takes a sum.
    """
    p = fr_per_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert ann.index.name == "t_year"
    assert list(ann.index) == list(range(12))
    assert list(ann.columns) == COLUMNS
    for y in (0, 5, 7, 11):
        rows = df.loc[bom(y):anniv(y)]
        assert len(rows) == 12
        assert ann.loc[y, "pols_if"] == pytest.approx(p.pols_if(bom(y)), rel=1e-14)
        assert ann.loc[y, "av_pp"] == pytest.approx(p.av_pp(anniv(y)), rel=1e-14)
        for col in COLUMNS:
            if col not in ("pols_if", "av_pp"):
                assert ann.loc[y, col] == pytest.approx(
                    rows[col].sum(), rel=1e-12), (y, col)


def test_result_state_annual_is_the_notes_table(fr_per_anchor):
    """Its two halves are read at the two months that determine them."""
    p = fr_per_anchor
    ann = p.result_state_annual()
    assert ann.index.name == "t_year"
    assert list(ann.index) == list(range(12))
    assert list(ann.columns) == list(p.result_state().columns)
    for y in (0, 7, 11):
        assert ann.loc[y, "switch_pp"] == pytest.approx(p.switch_pp(bom(y)), rel=1e-14)
        assert ann.loc[y, "prem_to_av_pp"] == pytest.approx(
            p.prem_to_av_pp(bom(y)), rel=1e-14)
        assert ann.loc[y, "av_euro_pp"] == pytest.approx(
            p.av_euro_pp(anniv(y)), rel=1e-14)
        assert ann.loc[y, "av_uc_pp"] == pytest.approx(
            p.av_uc_pp(anniv(y)), rel=1e-14)


# The notes' month-by-month table: the twelve months of the anchor cell's first plan
# year, per policy.  It is the table that makes the conversion legible - the versement
# arrives once, in month 0; the management charge falls once, in month 11, and is the
# same 143.51 the annual grid levied; and the garantie plancher base is flat in between.
# t: (prem_to_av_pp, inv_income_pp, mgmt_charge_pp, av_pp, death_floor_pp, pols_if)
FIRST_YEAR_MONTHS = {
    0:  (2925.00, 79.55,   0.00, 19604.55, 18925.00, 1.000000),
    1:  (   0.00, 79.87,   0.00, 19684.42, 18925.00, 0.997404),
    5:  (   0.00, 81.18,   0.00, 20007.17, 18925.00, 0.987087),
    10: (   0.00, 82.85,   0.00, 20418.06, 18925.00, 0.974341),
    11: (   0.00, 83.19, 143.51, 20357.74, 18781.49, 0.971812),
}


@pytest.mark.parametrize("t", sorted(FIRST_YEAR_MONTHS))
def test_worked_example_month(fr_per_anchor, t):
    """The notes' month-level table for the first plan year, to the cent."""
    prem, income, charge, av, floor, pols = FIRST_YEAR_MONTHS[t]
    p = fr_per_anchor
    assert p.prem_to_av_pp(t) == pytest.approx(prem, abs=CENT)
    assert p.inv_income_pp(t) == pytest.approx(income, abs=CENT)
    assert p.mgmt_charge_pp(t) == pytest.approx(charge, abs=CENT)
    assert p.av_pp(t) == pytest.approx(av, abs=CENT)
    assert p.death_floor_pp(t) == pytest.approx(floor, abs=CENT)
    assert p.pols_if(t) == pytest.approx(pols, abs=POLS)


def test_the_management_charge_is_not_spread(fr_per_anchor):
    """It falls whole in the anniversary month, and that is what keeps the floor exact.

    The load-bearing timing decision of this conversion.  The account value would survive
    a monthly levy - the two monthly factors still compound back - but the *garantie
    plancher* base accumulates a SUM of charges rather than a product of factors, and
    twelve monthly charges do not add to the annual one.  Measured on this model, levying
    it at 1 - (1 - c)^(1/12) each month moves the base at the anniversary by up to 71.95
    EUR on the anchor cell and 531.57 EUR on model point 12, which would change the
    47,267.36 the notes print.
    """
    p = fr_per_anchor
    for y in range(p.proj_years()):
        assert p.mgmt_charge_pp(anniv(y)) > 0.0, y
        assert p.is_anniv(anniv(y)) is True
        for t in range(bom(y), anniv(y)):
            assert p.mgmt_charge_pp(t) == 0.0, t
            assert p.is_anniv(t) is False
    # It is the same number, on the same balance, the annual grid levied.
    assert p.mgmt_charge_pp(anniv(0)) == pytest.approx(143.50875, rel=1e-12)
    assert p.mgmt_charge_pp(anniv(11)) == pytest.approx(494.07733045, rel=1e-10)
    assert p.mgmt_charge_pp(anniv(0)) == pytest.approx(
        p.av_euro_pp_at(anniv(0), "BEF_CHARGE") * 0.007
        + p.av_uc_pp_at(anniv(0), "BEF_CHARGE") * 0.007, rel=1e-14)
    # The price of the decision, stated: a mid-year exit is valued GROSS of the plan
    # year's charge, which in the last plan year is 0.387% above the anniversary value.
    assert p.av_pp(142) / p.av_pp(143) - 1 == pytest.approx(0.00387, abs=1e-5)
    # The credit, by contrast, IS spread - every month, geometrically - so a mid-year exit
    # is not paid on a balance carrying no return since the last anniversary.  The two
    # halves of that pair are the conversion's load-bearing decisions and they go opposite
    # ways on purpose.
    for t in range(0, 24):
        assert p.inv_income_pp(t) > 0.0, t
    assert sum(p.inv_income_pp(t) for t in range(bom(0), anniv(0) + 1)) == (
        pytest.approx(976.25, abs=CENT))            # the annual grid's year-0 credit


def test_the_versement_and_the_rebalancing_land_on_the_plan_year_start(fr_per_anchor):
    """Two annual events at one end of the plan year, one at the other.

    ``is_plan_boy`` and ``is_anniv`` are different months, which is why both exist.
    """
    p = fr_per_anchor
    for y in range(p.proj_years()):
        assert p.is_plan_boy(bom(y)) is True
        assert p.is_anniv(bom(y)) is False
        assert p.premium_pp(bom(y)) == 3000.00
        for t in range(bom(y) + 1, anniv(y) + 1):
            assert p.is_plan_boy(t) is False
            assert p.premium_pp(t) == 0.0, t
            assert p.premiums(t) == 0.0, t
    assert p.duration_mth(37) == 37
    assert p.is_plan_boy(0) is True and p.is_anniv(11) is True


def test_both_signs_of_the_net_flow_are_published(fr_per_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign."""
    df = fr_per_anchor.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    outgo = df[["claims_death", "claims_early_release", "claims_transfer",
                "claims_maturity", "annuity_conversion", "expenses"]].sum(axis=1)
    assert (outgo - df["premiums"] - df["liability_cf"]).abs().max() == (
        pytest.approx(0.0, abs=1e-9))
    # A contributing plan is cash-positive in every PLAN YEAR but the settlement one -
    # a claim that lives on the plan-year roll-up, because on the monthly frame only the
    # twelve versement months are cash-positive.
    ann = fr_per_anchor.result_cf_annual()
    assert (ann.loc[0:10, "net_cf"] > 0).all()
    assert ann.loc[11, "net_cf"] < 0
    assert int((df["net_cf"] > 0).sum()) == 12
    assert all(df.loc[t, "net_cf"] > 0 for t in range(0, PROJ_LEN, 12))


def test_pols_if_is_the_start_of_period_count(per_assurance):
    """pols_if(t) is the count row t OPENS with, and the weight that row's flows carry.

    The library's settled convention, asserted here because breaking it is silent.  This
    model was first written with the notes' end-of-year l(t) published under the name
    ``pols_if``: every cash flow on the row was still weighted correctly, but the exposure
    column beside them was the right series shifted one period, so a reader dividing a
    flow by that row's ``pols_if`` recovered a one-period-stale per-policy amount and
    nothing raised.  The end-of-year quantity now lives at ``pols_if_at(t, "AFT_DECR")``
    and in ``result_state()`` as ``pols_if_eoy``.

    The checkable consequence is the first row: no decrement has been applied when a
    period opens, so ``result_cf()`` must open at ``pols_if_init()`` exactly, on every
    model point.
    """
    for point_id in per_assurance.Data.model_point_table().index:
        p = per_assurance.Projection[point_id]
        df = p.result_cf()
        assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12), (
            point_id)
        for t in range(p.proj_len()):
            assert df.loc[t, "pols_if"] == pytest.approx(p.pols_if(t), rel=1e-14)
            # ... and one period behind the notes' l(t).
            assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(
                p.pols_if(t + 1), rel=1e-14), (point_id, t)

    p = per_assurance.Projection[1]
    assert p.pols_if(0) == 1.0
    assert p.pols_if_at(0, "BEF_DECR") == 1.0
    # The notes' l(0) is the count the first PLAN YEAR ends with, month 11.
    assert p.pols_if_at(anniv(0), "AFT_DECR") == pytest.approx(0.969289, abs=POLS)
    assert p.pols_if(12) == pytest.approx(0.969289, abs=POLS)
    # The flows on a row are weighted by that row's own pols_if, and the versement falls
    # only in the month that opens a plan year.
    assert p.premiums(12) == pytest.approx(3000.0 * p.pols_if(12), rel=1e-14)
    assert p.premiums(1) == 0.0
    assert p.result_state().loc[0, "pols_if_eoy"] == pytest.approx(
        p.result_cf().loc[1, "pols_if"], rel=1e-14)
    assert p.result_state_annual().loc[0, "pols_if_eoy"] == pytest.approx(
        p.result_cf_annual().loc[1, "pols_if"], rel=1e-14)
    # The horizon settlement is the one flow taken at the END-of-year count, because the
    # survivors settle after the final year's own decrements.
    t_last = p.proj_len() - 1
    assert p.pols_maturity(t_last) == pytest.approx(
        p.pols_if_at(t_last, "AFT_DECR"), rel=1e-14)
    assert p.pols_maturity(t_last) < p.result_cf().loc[t_last, "pols_if"]


def test_inputs_live_beside_the_model():
    """Five external CSVs, and the glide path is one of them."""
    expected = {"model_point_table.csv", "allocation_grid.csv", "mort_table.csv",
                "exit_table.csv", "annuity_factor.csv"}
    assert expected == {p.name for p in PRODUCT_DIR.iterdir() if p.suffix == ".csv"}
    assert model_files(MODEL_DIR) == {"__init__.py", "_system.json"}


def test_the_glide_path_can_be_swapped_without_touching_formulas():
    """This is what a user does with an insurer's own twenty-band ladder."""
    src = PRODUCT_DIR / "allocation_grid.csv"
    grid = pd.read_csv(src, index_col=["allocation_profile", "years_to_horizon"])
    # A ladder that de-risks harder: 10 points more euro everywhere, capped at 1.
    harder = grid.copy()
    harder["euro_share"] = (harder["euro_share"] + 0.10).clip(upper=1.0)
    harder["uc_share"] = 1.0 - harder["euro_share"]

    model = mx.read_model(MODEL_DIR, name="PER_FR_S_grid")
    try:
        alt = "allocation_grid_hard.csv"
        harder.to_csv(model.Data.input_dir() / alt)
        try:
            base = model.Projection[1].av_pp(143)
            model.Data.allocation_grid_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            # More euro support means less of the 5.00% UC return, so a smaller balance.
            assert model.Projection[1].av_pp(143) < base
            assert model.Projection[1].check_euro_share_min() is True
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_model_docstring_describes_the_current_structure(per_assurance):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = per_assurance.doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                      # inputs are not stored in the model
    assert "once per model" in doc                # why Data exists
    assert "Rente_FR_S" in doc                    # where the annuity goes
    assert "lapse_rate" in doc                    # and why there is not one
    for space in ("Data", "Projection"):
        assert space in doc
    # The grid is declared in prose, and the annual claim it replaced is gone.
    assert "Monthly steps" in doc
    assert "plan months" in doc
    assert "Annual steps" not in doc
    assert "plan years** from the valuation date" not in doc


def test_the_grid_is_monthly_and_every_contract_event_is_annual(per_assurance,
                                                                fr_per_anchor):
    """The registry row, the name and the model's own arithmetic all say monthly."""
    assert MODELS["PER_FR_S"][1]["grid"] == "monthly"
    p = fr_per_anchor
    assert p.proj_years() == 12
    assert p.proj_len() == 144
    assert len(p.result_cf()) == 144
    assert len(p.result_cf_annual()) == 12
    assert len(p.result_state_annual()) == 12
    assert p.duration_mth(84) == 84
    assert p.duration(0) == 2 and p.duration(11) == 2 and p.duration(12) == 3
    assert p.plan_year(84) == 10
    assert p.years_to_horizon(84) == 5
    assert p.is_plan_boy(84) is True and p.is_anniv(84) is False
    assert p.is_anniv(95) is True and p.is_plan_boy(95) is False
    assert p.age(11) == 52 and p.age(12) == 53 and p.age(143) == 63


def test_space_docstrings_carry_their_reference_material(per_assurance):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = per_assurance.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "alloc_euro", "switch_pp",
                  "death_floor_pp", "early_release_rate", "transfer_out_rate",
                  "annuity_factor", "is_commuted", "plan_year"):
        assert cells in proj, cells
    # The monthly vocabulary is documented alongside the notes' own symbols, and the
    # timing decisions the conversion had to make are stated rather than implied.
    for cells in ("proj_years", "duration_mth", "is_plan_boy", "is_anniv",
                  "mort_rate_mth", "early_release_rate_mth", "transfer_out_rate_mth",
                  "return_euro_mth", "return_uc_mth", "result_cf_annual",
                  "result_state_annual"):
        assert cells in proj, cells
    assert "plan months" in proj
    assert "Anniversary equivalence" in proj
    assert "BEF_CHARGE" in proj
    data = per_assurance.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "allocation_grid", "exit_table"):
        assert cells in data, cells


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="PER_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in PRODUCT_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="PER_FR_S_rt")
    try:
        p = reread.Projection[1]
        for y, row in WORKED_EXAMPLE.items():
            assert p.av_pp(anniv(y)) == pytest.approx(row[5], abs=CENT)
            assert p.pols_if_at(anniv(y), "AFT_DECR") == pytest.approx(
                row[6], abs=POLS)
        assert p.commuted_pp() == pytest.approx(20711.12, abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
