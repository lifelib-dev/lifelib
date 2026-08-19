"""Golden and structural tests for ULB_UK_S.

The golden values are the worked example in
products/unit_linked_bond/technical-notes.md ("Worked example"), which projects the
anchor cell: male 65, GBP 100,000 in 100 segments, AMC 1.00%, further costs 0.10%, tax
provision 20%, death uplift 1.001, a 5% gross fund return and GBP 416.67 a month of
withdrawals.  They are hard-coded here rather than pickled so that a reviewer can compare
them against the notes by eye.

Tolerances follow the precision the notes display: money to the penny.

Beyond the worked example this module asserts the product facts the notes call out as
modelling pitfalls, because each is a way an implementation can look right and be wrong:

* the AMC is levied on the post-growth, pre-cancellation fund;
* the tax provision, the further costs and adviser charges are **pass-throughs**, not
  margin;
* the death strain is the uplift over the unit fund, not the death benefit;
* and the 5% tax allowance is policyholder machinery that generates no insurer cash flow.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from uk_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9, a house decision per D8).  Those
    caches are not part of the model and must not make a round-trip comparison fail for
    anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


PENNY = 0.005         # money displayed to 2 d.p.

MODEL_DIR = LIB / MODELS["ULB_UK_S"][0]

# t: (UF(t-1), gross return, tax provision, AMC, further costs, withdrawal, UF(t))
WORKED_EXAMPLE = {
    1:  (100000.00, 407.41, 81.48, 83.60, 8.36, 416.67, 99817.30),
    2:  (99817.30,  406.67, 81.33, 83.45, 8.35, 416.67, 99634.17),
    3:  (99634.17,  405.92, 81.18, 83.30, 8.33, 416.67, 99450.61),
    12: (97966.60,  399.13, 79.83, 81.90, 8.19, 416.67, 97779.14),
}

# The notes' year-1 totals row.
YEAR_1 = {
    "growth": 4839.44,
    "tax": 967.89,
    "amc": 993.10,
    "further_costs": 99.31,
    "withdrawals": 5000.00,
    "uf_end": 97779.14,
}

# The notes' derived monthly rates.
G_M = 0.0040741
C_M = 0.0008333
F_M = 0.0000833
Q_M = 0.000837


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(uk_bond_anchor, t):
    """Every cell of the notes' unit fund table, to the displayed precision."""
    uf_start, growth, tax, amc, fc, wd, uf_end = WORKED_EXAMPLE[t]
    p = uk_bond_anchor
    assert p.av_pp(t) == pytest.approx(uf_start, abs=PENNY)
    assert p.fund_growth_pp(t) == pytest.approx(growth, abs=PENNY)
    assert p.tax_provision_pp(t) == pytest.approx(tax, abs=PENNY)
    assert p.amc_pp(t) == pytest.approx(amc, abs=PENNY)
    assert p.further_costs_pp(t) == pytest.approx(fc, abs=PENNY)
    assert p.wd_pp(t) == pytest.approx(wd, abs=PENNY)
    assert p.av_pp_at(t, "AFT_WD") == pytest.approx(uf_end, abs=PENNY)


def test_worked_example_month_one_trace(uk_bond_anchor):
    """G$ 407.41, TX 81.48, UF_g 100,325.93, AMC 83.60, FC 8.36, UF' 100,233.96."""
    p = uk_bond_anchor
    assert p.fund_return_mth() == pytest.approx(G_M, abs=5e-8)
    assert p.amc_rate_mth() == pytest.approx(C_M, abs=5e-8)
    assert p.further_costs_rate_mth() == pytest.approx(F_M, abs=5e-8)
    assert p.av_pp_at(1, "AFT_GROWTH") == pytest.approx(100325.93, abs=PENNY)
    assert p.av_pp_at(1, "AFT_CHARGE") == pytest.approx(100233.96, abs=PENNY)
    # The notes' trace subtracts the withdrawal as the rounded 416.67; the model carries
    # 5,000/12 at full precision, so the two agree at the pence the table displays.
    assert p.wd_pp(1) == pytest.approx(5000.0 / 12, rel=1e-14)
    assert p.av_pp_at(1, "AFT_WD") == pytest.approx(99817.30, abs=PENNY)


def test_worked_example_year_one_totals(uk_bond_anchor):
    """The notes' totals row, and the reconciliation that closes it."""
    p = uk_bond_anchor
    months = range(1, 13)
    growth = sum(p.fund_growth_pp(t) for t in months)
    tax = sum(p.tax_provision_pp(t) for t in months)
    amc = sum(p.amc_pp(t) for t in months)
    fc = sum(p.further_costs_pp(t) for t in months)
    wd = sum(p.wd_pp(t) for t in months)
    assert growth == pytest.approx(YEAR_1["growth"], abs=PENNY)
    assert tax == pytest.approx(YEAR_1["tax"], abs=PENNY)
    assert amc == pytest.approx(YEAR_1["amc"], abs=PENNY)
    assert fc == pytest.approx(YEAR_1["further_costs"], abs=PENNY)
    assert wd == pytest.approx(YEAR_1["withdrawals"], abs=PENNY)
    # 100,000 + 4,839.44 - 967.89 - 993.10 - 99.31 - 5,000.00 = 97,779.14
    assert 100000.0 + growth - tax - amc - fc - wd == pytest.approx(
        YEAR_1["uf_end"], abs=PENNY)
    assert p.av_pp_at(12, "AFT_WD") == pytest.approx(YEAR_1["uf_end"], abs=PENNY)


def test_worked_example_per_segment(uk_bond_anchor):
    """The bond is 100 identical segments, so a segment is worth 977.79 after a year."""
    p = uk_bond_anchor
    assert p.n_segments() == 100
    assert p.av_per_segment_pp(1) == pytest.approx(1000.00, abs=PENNY)
    assert p.av_per_segment_pp(13) == pytest.approx(977.79, abs=PENNY)


def test_worked_example_insurer_side(uk_bond_anchor):
    """AMC +993.10, maintenance -60.00, expected death strain -0.99, per policy.

    The notes take survivorship as approximately 1 over the first year, so their figures
    are per policy; the model weights properly, which is why the aggregate columns are a
    shade lower.
    """
    p = uk_bond_anchor
    months = range(1, 13)
    assert sum(p.amc_pp(t) for t in months) == pytest.approx(993.10, abs=PENNY)
    # Maintenance is GBP 60 in year 1, and the GBP 300 acquisition charge falls at issue.
    assert p.expenses(1) - 300.0 * p.pols_if(1) == pytest.approx(5.00, abs=PENNY)
    assert sum(p.expenses(t) for t in months) - 300.0 == pytest.approx(
        60.0 * sum(p.pols_if(t) for t in months) / 12, abs=0.02)
    # The expected death strain over year 1: about GBP 1 per GBP 100k at q = 1%.
    strain = sum(p.death_strain(t) for t in months)
    assert strain == pytest.approx(0.99, abs=0.02)
    assert p.mort_rate(1) == pytest.approx(0.01, rel=1e-12)
    assert p.mort_rate_mth(1) == pytest.approx(Q_M, abs=5e-7)


def test_worked_example_death_benefit_at_month_twelve(uk_bond_anchor):
    """Per actual death the benefit is 1.001 x 97,779.14 = 97,876.92; the strain 97.78."""
    p = uk_bond_anchor
    uf = p.av_pp_at(12, "AFT_WD")
    assert 1.001 * uf == pytest.approx(97876.92, abs=PENNY)
    assert p.death_strain_pp(12) == pytest.approx(97.78, abs=PENNY)
    assert p.claims(12, "DEATH") == pytest.approx(
        97876.92 * p.pols_death(12), abs=PENNY)


def test_worked_example_allowance_check(uk_bond_anchor):
    """Year-1 withdrawals of 5,000 exactly equal the allowable element: no excess."""
    p = uk_bond_anchor
    assert p.wd_cum_pp(12) == pytest.approx(5000.00, abs=PENNY)
    assert p.allowance_cum_pp(12) == pytest.approx(5000.00, abs=PENNY)
    assert p.excess_gain_pp(12) == pytest.approx(0.0, abs=PENNY)
    # And the 7.5% product cap - 7,500 on the premium - is nowhere near breached.
    assert p.wd_cap_pp(1) == pytest.approx(0.075 * 100233.96, abs=PENNY)
    assert 12 * p.wd_pp(1) < p.wd_cap_pp(1)


# ---------------------------------------------------------------------------
# The charge ordering


def test_the_amc_is_levied_on_the_post_growth_pre_cancellation_fund(uk_bond_anchor):
    """Not UF(t-1), and not the post-withdrawal fund - a listed pitfall.

    The charge accrues daily through the unit price, so it sits on UF_g.  The three
    wrong bases differ by about half a month's growth or withdrawal, which is small
    monthly and systematic over decades.
    """
    p = uk_bond_anchor
    for t in (1, 60, 200):
        uf_g = p.av_pp_at(t, "AFT_GROWTH")
        assert p.amc_pp(t) == pytest.approx(p.amc_rate_mth() * uf_g, rel=1e-14)
        assert p.amc_pp(t) != pytest.approx(p.amc_rate_mth() * p.av_pp(t), rel=1e-9)
        assert p.amc_pp(t) != pytest.approx(
            p.amc_rate_mth() * p.av_pp_at(t, "AFT_WD"), rel=1e-9)
    # The four timing points are strictly ordered while the fund is being drawn down.
    t = 60
    assert (p.av_pp_at(t, "AFT_GROWTH") > p.av_pp_at(t, "AFT_CHARGE")
            > p.av_pp_at(t, "AFT_WD"))


def test_the_unit_fund_rollforward_closes(unit_linked_bond):
    """UF(t) = UF(t-1)(1 + g_m(1-t_pf))(1 - c_m - f_m) - W - AC - GC."""
    for point_id in unit_linked_bond.Data.model_point_table().index:
        assert unit_linked_bond.Projection[point_id].check_av_roll_fwd() is True
    p = unit_linked_bond.Projection[1]
    for t in (1, 12, 100):
        assert p.av_pp_at(t, "AFT_WD") == pytest.approx(
            p.av_pp(t) * (1 + p.fund_return_mth() * (1 - 0.20))
            * (1 - p.amc_rate_mth() - p.further_costs_rate_mth()) - p.wd_pp(t),
            abs=1e-8)
    # And the end-of-month fund is the next month's opening fund.
    for t in (1, 12, 100):
        assert p.av_pp_at(t, "AFT_WD") == pytest.approx(p.av_pp(t + 1), rel=1e-14)


def test_the_timing_strings_validate(uk_bond_anchor):
    with pytest.raises(FormulaError):
        uk_bond_anchor.av_pp_at(1, "AFT_NOTHING")
    with pytest.raises(FormulaError):
        uk_bond_anchor.pols_if_at(1, "BEF_NOTHING")


# ---------------------------------------------------------------------------
# Pass-throughs are not margin


def test_the_pass_throughs_stay_out_of_net_cf(uk_bond_anchor):
    """net_cf is AMC + rider charge - expenses - death strain, and nothing else.

    Counting the tax provision or the further costs as margin is the notes'
    second-listed pitfall, and it would overstate the year-one result by more than the
    AMC itself.
    """
    p = uk_bond_anchor
    for t in (1, 12, 100):
        assert p.net_cf(t) == pytest.approx(
            p.amc_charges(t) + p.gmdb_charges(t) - p.expenses(t) - p.death_strain(t),
            rel=1e-12)
    # The pass-throughs are published so that their exclusion is visible.
    df = p.result_cf()
    assert df["tax_provisions"].sum() > 0.0
    assert df["further_costs"].sum() > 0.0


def test_the_size_of_the_pass_throughs_against_the_amc(uk_bond_anchor):
    """Tax provision about 97% of the AMC in year 1, further costs about 10%.

    That is the measure of how badly counting them as margin would mislead.
    """
    p = uk_bond_anchor
    months = range(1, 13)
    amc = sum(p.amc_pp(t) for t in months)
    tax = sum(p.tax_provision_pp(t) for t in months)
    fc = sum(p.further_costs_pp(t) for t in months)
    assert tax / amc == pytest.approx(0.97, abs=0.01)
    assert fc / amc == pytest.approx(0.10, abs=0.01)


def test_adviser_charges_are_a_pass_through(unit_linked_bond):
    """Model point 3 adds a 0.5% ongoing adviser charge: it reduces the fund, not margin.

    Post-RDR adviser charges are facilitated pass-throughs by unit cancellation.  They
    consume the policyholder's tax allowance and add nothing to the insurer's result.
    """
    p1, p3 = unit_linked_bond.Projection[1], unit_linked_bond.Projection[3]
    assert p3.oac_rate() == 0.005
    assert p3.adviser_charge_pp(1) == pytest.approx(
        0.005 / 12 * p3.av_pp_at(1, "AFT_CHARGE"), rel=1e-14)
    # It draws the fund down faster, so the fund is exhausted sooner.
    assert p3.av_pp(60) < p1.av_pp(60)
    assert p3.proj_len() < p1.proj_len()
    # And it consumes the tax allowance alongside the withdrawal.
    assert p3.wd_cum_pp(12) > p1.wd_cum_pp(12)
    # But it appears in no income line: net_cf is still AMC less expenses and strain.
    assert p3.net_cf(12) == pytest.approx(
        p3.amc_charges(12) - p3.expenses(12) - p3.death_strain(12), rel=1e-12)


# ---------------------------------------------------------------------------
# The death strain


def test_benefits_are_funded_by_cancelling_units(unit_linked_bond):
    """claims - unit_releases - death_strain = 0, on every model point.

    A model that funded benefits twice - once from the fund and once from the insurer -
    would show it here.
    """
    for point_id in unit_linked_bond.Data.model_point_table().index:
        assert unit_linked_bond.Projection[point_id].check_unit_funding() is True
    p = unit_linked_bond.Projection[1]
    for t in (1, 60, 200):
        assert p.claims(t) - p.unit_releases(t) == pytest.approx(
            p.death_strain(t), abs=1e-9)
        # A surrender is funded entirely from the fund: no strain at all.
        assert p.claims(t, "SURRENDER") == pytest.approx(
            p.av_pp_at(t, "AFT_WD") * p.pols_surr(t), rel=1e-14)


def test_the_death_strain_is_the_uplift(uk_bond_anchor):
    """(u - 1) x UF: a tenth of a percent of the fund, and nothing else in the base run."""
    p = uk_bond_anchor
    assert p.gmdb_flag() is False
    for t in (1, 60, 200):
        assert p.death_strain_pp(t) == pytest.approx(
            0.001 * p.av_pp_at(t, "AFT_WD"), rel=1e-12)


def test_the_uplift_is_a_parameter_never_a_literal(unit_linked_bond):
    """100.1% against 101% is a tenfold difference in death strain - a listed pitfall."""
    p1, p5 = unit_linked_bond.Projection[1], unit_linked_bond.Projection[5]
    assert p1.db_uplift() == 1.001
    assert p5.db_uplift() == 1.010
    for t in (12, 100):
        assert p5.death_strain_pp(t) / p1.death_strain_pp(t) == pytest.approx(
            10.0, rel=1e-9)
    # And it costs the insurer measurably more over the projection.
    assert (p5.result_cf()["net_cf"].sum() < p1.result_cf()["net_cf"].sum())


def test_mortality_barely_matters_without_the_rider(uk_bond_anchor):
    """The net amount at risk is 0.1% of the fund, so the death strain is a rounding line.

    Behaviour, not mortality, dominates this product's value.
    """
    p = uk_bond_anchor
    df = p.result_cf()
    assert df["death_strain"].sum() < 0.02 * df["amc_charges"].sum()


# ---------------------------------------------------------------------------
# The GMDB rider


def test_the_guarantee_erodes_with_withdrawals(unit_linked_bond):
    """G = premium - withdrawals - adviser charges, so it runs out before the fund does.

    On the anchor withdrawal pattern the guarantee reaches zero at month 240 - which is
    why the rider never bites on the base assumptions, and why model point 4's cash flows
    are all but identical to point 1's.
    """
    p = unit_linked_bond.Projection[4]
    assert p.gmdb_flag() is True
    assert p.gmdb_guarantee_pp(1) == pytest.approx(100000.0, abs=PENNY)
    assert p.gmdb_guarantee_pp(120) == pytest.approx(
        100000.0 - 119 * 416.6667, abs=0.02)
    assert p.gmdb_guarantee_pp(241) == 0.0
    # Out of the money throughout, so the charge is zero and the strain is the uplift.
    assert all(p.gmdb_charge_pp(t) == 0.0 for t in (1, 60, 120, 200))
    assert p.death_strain_pp(60) == pytest.approx(
        0.001 * p.av_pp_at(60, "AFT_WD"), rel=1e-12)


def test_the_guarantee_bites_when_the_fund_falls(unit_linked_bond):
    """Drive the fund return negative and the rider moves into the money.

    The base assumptions never exercise it, so the machinery is demonstrated here rather
    than left unverified.  The real charge scale is unpublished, so the cost-of-insurance
    form used has the right shape and no authority.
    """
    model = mx.read_model(MODEL_DIR, name="ULB_UK_S_gmdb")
    try:
        model.Projection.fund_return = -0.06
        model.Projection.clear_all()
        p = model.Projection[4]
        assert p.gmdb_guarantee_pp(60) > p.db_uplift() * p.av_pp_at(60, "AFT_CHARGE")
        assert p.gmdb_charge_pp(60) > 0.0
        assert p.death_strain_pp(60) > 0.001 * p.av_pp_at(60, "AFT_WD")
        assert p.gmdb_charges(60) > 0.0          # the charge is insurer income
        assert p.check_unit_funding() is True
        # The death benefit is the guarantee where it exceeds the uplifted fund.
        assert p.claims(60, "DEATH") == pytest.approx(
            p.gmdb_guarantee_pp(60) * p.pols_death(60), rel=1e-12)
    finally:
        model.close()


def test_the_guarantee_is_measured_before_the_months_cancellations(unit_linked_bond):
    """At wd_cum_pp(t - 1), which is the only reading that resolves.

    The rider charge is itself a cancellation alongside the withdrawal, so a guarantee
    net of the same month's withdrawal would make the charge depend on a withdrawal that
    depends on the charge.
    """
    p = unit_linked_bond.Projection[4]
    for t in (2, 60, 120):
        assert p.gmdb_guarantee_pp(t) == pytest.approx(
            max(0.0, p.premium() - p.wd_cum_pp(t - 1)), abs=1e-9)


# ---------------------------------------------------------------------------
# Withdrawals, the caps, and the fund running out


def test_the_withdrawal_patterns(unit_linked_bond):
    """none, allowance_5pct and custom."""
    p1 = unit_linked_bond.Projection[1]
    assert p1.wd_pattern() == "allowance_5pct" and p1.wd_rate() == 0.05
    assert p1.wd_pp(1) == pytest.approx(0.05 * 100000 / 12, rel=1e-14)

    p2 = unit_linked_bond.Projection[2]
    assert p2.wd_pattern() == "none" and p2.wd_rate() == 0.0
    assert all(p2.wd_pp(t) == 0.0 for t in (1, 60, 400))

    p6 = unit_linked_bond.Projection[6]
    assert p6.wd_pattern() == "custom" and p6.wd_rate() == 0.03
    assert p6.wd_pp(1) == pytest.approx(0.03 * 250000 / 12, rel=1e-14)


def test_the_product_cap_is_the_seven_and_a_half_percent_one(uk_bond_anchor):
    """max(7.5% of the fund, 7.5% of the premium) over a rolling twelve months.

    Not the 5% tax allowance - that never caps what can be withdrawn.
    """
    p = uk_bond_anchor
    assert p.wd_cap_pp(1) == pytest.approx(
        0.075 * max(p.av_pp_at(1, "AFT_CHARGE"), 100000.0), abs=PENNY)
    # The cap floors on the premium once the fund has fallen below it.
    late = 300
    assert p.av_pp_at(late, "AFT_CHARGE") < 100000.0
    assert p.wd_cap_pp(late) == pytest.approx(0.075 * 100000.0, abs=PENNY)
    # The anchor's 5% pattern sits comfortably inside it.
    assert 12 * p.wd_pp(1) < p.wd_cap_pp(1)


def test_the_withdrawal_is_capped_at_what_the_fund_can_pay(uk_bond_anchor):
    """Which is what stops the fund going negative."""
    p = uk_bond_anchor
    last = p.proj_len()
    assert p.av_pp(last) > 0.0
    assert p.av_pp_at(last, "AFT_WD") == pytest.approx(0.0, abs=1e-9)
    assert p.wd_pp(last) <= p.av_pp_at(last, "AFT_CHARGE") + 1e-9
    assert all(p.av_pp(t) >= 0.0 for t in range(1, last + 1))


def test_the_fund_exhausts_the_projection(unit_linked_bond):
    """A 5% withdrawal against a 5% gross return is not sustainable after tax and charges.

    A bond with no units has no liability, no margin and nothing left to project.
    """
    p1, p2 = unit_linked_bond.Projection[1], unit_linked_bond.Projection[2]
    assert p1.fund_exhaust_mth() == 354
    assert p1.proj_len() == 353 < p1.horizon_mths()
    assert p1.proj_len() == p1.fund_exhaust_mth() - 1
    # The accumulation cell has no withdrawals, so it runs to the limiting age instead.
    assert p2.fund_exhaust_mth() > p2.horizon_mths()
    assert p2.proj_len() == p2.horizon_mths() == 12 * (120 - 65)
    assert p2.av_pp(p2.proj_len()) > p2.premium()      # and its fund has grown


# ---------------------------------------------------------------------------
# The tax allowance is policyholder machinery


def test_the_allowance_generates_no_insurer_cash_flow(uk_bond_anchor):
    """It is tracked because it drives behaviour, not because anyone pays anything.

    Treating it as a product feature is a listed pitfall.
    """
    p = uk_bond_anchor
    df = p.result_cf()
    assert "excess_gain" not in "".join(df.columns)
    assert "allowance" not in "".join(df.columns)
    # net_cf is unaffected by the allowance state at every t.
    for t in (12, 240, 300):
        assert p.net_cf(t) == pytest.approx(
            p.amc_charges(t) + p.gmdb_charges(t) - p.expenses(t) - p.death_strain(t),
            rel=1e-12)


def test_the_allowance_accrues_for_twenty_years_then_stops(uk_bond_anchor):
    """P x min(y, 20) x 5%, so the cumulative allowance caps at the premium."""
    p = uk_bond_anchor
    assert p.allowance_cum_pp(12) == pytest.approx(5000.0, abs=PENNY)
    assert p.allowance_cum_pp(240) == pytest.approx(100000.0, abs=PENNY)   # year 20
    assert p.allowance_cum_pp(252) == pytest.approx(100000.0, abs=PENNY)   # year 21
    assert p.allowance_cum_pp(300) == pytest.approx(100000.0, abs=PENNY)


def test_the_excess_gain_appears_once_the_allowance_is_spent(uk_bond_anchor):
    """Withdrawals past twenty years' worth of allowance generate immediate gains."""
    p = uk_bond_anchor
    assert p.excess_gain_pp(240) == pytest.approx(0.0, abs=PENNY)
    assert p.excess_gain_pp(252) > 0.0
    assert p.excess_gain_pp(300) > p.excess_gain_pp(252)


def test_the_allowance_exhaustion_step_raises_surrender(uk_bond_anchor):
    """M_allow steps to 1.5 from policy year 21, when the allowance runs out."""
    p = uk_bond_anchor
    assert p.policy_year(240) == 20 and p.policy_year(241) == 21
    assert p.allow_factor(240) == 1.0
    assert p.allow_factor(241) == 1.5
    assert p.surr_rate(241) == pytest.approx(
        min(0.35, p.surr_rate_base(241) * 1.5), rel=1e-12)


# ---------------------------------------------------------------------------
# Behaviour


def test_the_performance_multiplier_is_off_and_bites_when_switched_on(unit_linked_bond):
    """M_perf = min(2, 1 + 2 max(0, g_ref - R_12m)); 1 when the trailing return matches.

    The shock is kept separate from the fund return so it moves the *behavioural* driver
    without disturbing the fund path, which is what makes the multiplier testable in
    isolation.
    """
    p = unit_linked_bond.Projection[1]
    assert p.return_12m(1) == pytest.approx(0.05, rel=1e-12)   # equals the reference
    assert all(p.perf_factor(t) == 1.0 for t in (1, 60, 200))

    model = mx.read_model(MODEL_DIR, name="ULB_UK_S_perf")
    try:
        model.Projection.return_shock = -0.20
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.return_12m(1) == pytest.approx(0.05 - 0.20, rel=1e-12)
        assert proj.perf_factor(1) == pytest.approx(min(2.0, 1 + 2 * 0.20), rel=1e-12)
        assert proj.surr_rate(1) > p.surr_rate(1)
        # But the fund path is untouched, which is the point of the separate Reference.
        assert proj.av_pp(60) == pytest.approx(p.av_pp(60), rel=1e-12)
    finally:
        model.close()


def test_the_surrender_rate_is_capped(unit_linked_bond):
    """min(0.35, base x M_perf x M_allow) [std cap]."""
    model = mx.read_model(MODEL_DIR, name="ULB_UK_S_cap")
    try:
        model.Projection.return_shock = -0.50     # far past the multiplier cap
        model.Projection.clear_all()
        proj = model.Projection[1]
        assert proj.perf_factor(1) == 2.0         # the multiplier caps first
        assert proj.surr_rate(300) == pytest.approx(
            min(0.35, 0.10 * 2.0 * 1.5), rel=1e-12)
    finally:
        model.close()


def test_a_surrender_costs_nothing_at_exit_but_truncates_the_margin(uk_bond_anchor):
    """The surrender value is the bid value of units, cancelled - no penalty, no strain."""
    p = uk_bond_anchor
    for t in (12, 100):
        assert p.claims(t, "SURRENDER") == pytest.approx(
            p.av_pp_at(t, "AFT_WD") * p.pols_surr(t), rel=1e-14)
        # It contributes nothing to the non-unit stream at all.
        assert p.net_cf(t) == pytest.approx(
            p.amc_charges(t) + p.gmdb_charges(t) - p.expenses(t) - p.death_strain(t),
            rel=1e-12)
    # But it removes the policy, and with it every future charge.
    assert p.pols_if(200) < p.pols_if(12)


def test_the_inforce_rollforward_closes(unit_linked_bond):
    for point_id in unit_linked_bond.Data.model_point_table().index:
        assert unit_linked_bond.Projection[point_id].check_pols_roll_fwd() is True
    p = unit_linked_bond.Projection[1]
    for t in (1, 100, p.proj_len()):
        out = p.pols_death(t) + p.pols_surr(t) + p.pols_maturity(t)
        assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-12)
    assert all(p.pols_maturity(t) == 0.0 for t in (1, 100, p.proj_len() - 1))
    assert p.pols_maturity(p.proj_len()) > 0.0


def test_deaths_come_before_surrenders(uk_bond_anchor):
    p = uk_bond_anchor
    for t in (1, 60):
        assert p.pols_if_at(t, "BEF_SURR") == pytest.approx(
            p.pols_if(t) * (1 - p.mort_rate_mth(t)), rel=1e-14)
        assert p.pols_surr(t) == pytest.approx(
            p.pols_if_at(t, "BEF_SURR") * p.surr_rate_mth(t), rel=1e-14)


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape(uk_bond_anchor):
    df = uk_bond_anchor.result_cf()
    assert list(df.index) == list(range(1, 354))
    assert list(df.columns) == [
        "pols_if", "av_pp", "amc_charges", "gmdb_charges", "further_costs",
        "tax_provisions", "withdrawals", "claims_death", "claims_surrender",
        "unit_releases", "death_strain", "expenses", "net_cf",
    ]


def test_result_uf_matches_the_notes_table(uk_bond_anchor):
    """result_uf is the notes' worked-example table, column for column."""
    df = uk_bond_anchor.result_uf()
    for name in ("av_pp", "fund_growth_pp", "tax_provision_pp", "amc_pp",
                 "further_costs_pp", "wd_pp", "av_pp_end"):
        assert name in df.columns
    assert df.loc[1, "av_pp"] == pytest.approx(100000.00, abs=PENNY)
    assert df.loc[1, "av_pp_end"] == pytest.approx(99817.30, abs=PENNY)


def test_model_docstring_describes_the_current_structure(unit_linked_bond):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = unit_linked_bond.doc
    assert "unit-linked" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "non-unit" in doc
    assert "death strain" in doc


def test_space_docstrings_carry_their_reference_material(unit_linked_bond):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = unit_linked_bond.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("av_pp_at", "amc_pp", "death_strain_pp", "wd_cap_pp",
                  "allowance_cum_pp", "gmdb_guarantee_pp"):
        assert cells in proj
    data = unit_linked_bond.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "mort_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_the_account_value_vocabulary(unit_linked_bond):
    """av_pp_at and check_av_roll_fwd put this model in the library's account-value family."""
    shared = {
        "model_point", "age_at_entry", "sex", "proj_len", "age", "pols_if",
        "pols_if_at", "pols_if_init", "pols_death", "pols_maturity", "mort_rate",
        "mort_rate_mth", "premium", "claims", "expenses", "expense_acq",
        "expense_maint", "inflation_rate", "inflation_factor", "net_cf", "result_cf",
        "policy_year", "duration", "duration_mth", "av_pp", "av_pp_at",
        "check_av_roll_fwd", "withdrawals",
    }
    names = set(unit_linked_bond.Projection.cells) | set(
        unit_linked_bond.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_charge_rates_are_model_point_columns_not_a_rate_table(unit_linked_bond):
    """Per-policy contractual and discretionary parameters, not experience assumptions."""
    columns = set(unit_linked_bond.Data.model_point_table().columns)
    for col in ("amc_rate", "further_costs_rate", "tax_provision_rate", "db_uplift"):
        assert col in columns


def test_inputs_live_beside_the_model():
    """The three input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "surr_table.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir()
                        if p.suffix == ".csv"}


def test_inputs_are_read_once_not_once_per_model_point():
    """The readers live in Data, so N model points do not cause N reads."""
    from collections import Counter

    import pandas as pd

    model = mx.read_model(MODEL_DIR, name="ULB_UK_S_reads")
    reads = []
    original = pd.read_csv

    def counting(*args, **kwargs):
        reads.append(str(args[0]).replace("\\", "/").split("/")[-1])
        return original(*args, **kwargs)

    pd.read_csv = counting
    try:
        for point_id in model.Data.model_point_table().index:
            model.Projection[point_id].result_cf()
    finally:
        pd.read_csv = original
        model.close()

    counts = Counter(reads)
    assert counts and all(n == 1 for n in counts.values()), counts
    assert len(reads) == 3           # one per input file, regardless of point count


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows."""
    import pandas as pd

    src = MODEL_DIR.parent / "surr_table.csv"
    sticky = pd.read_csv(src, index_col="policy_year")
    sticky["surr_rate"] = sticky["surr_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="ULB_UK_S_swap")
    try:
        alt_name = "surr_table_sticky.csv"
        sticky.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["amc_charges"].sum()
            model.Data.surr_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Halving surrender keeps policies in force, so more AMC is collected.
            assert model.Projection[1].result_cf()["amc_charges"].sum() > base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_every_model_point_projects(unit_linked_bond):
    """No model point may sit in the table that the input tables cannot serve."""
    for point_id in unit_linked_bond.Data.model_point_table().index:
        proj = unit_linked_bond.Projection[point_id]
        df = proj.result_cf()
        assert len(df) > 0
        assert df.notna().all().all()
        assert proj.check_av_roll_fwd() is True
        assert proj.check_pols_roll_fwd() is True
        assert proj.check_unit_funding() is True


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="ULB_UK_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="ULB_UK_S_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.av_pp(t) == pytest.approx(row[0], abs=PENNY)
            assert p.av_pp_at(t, "AFT_WD") == pytest.approx(row[6], abs=PENNY)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
