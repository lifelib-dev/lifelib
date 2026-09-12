"""Golden and structural tests for UC_FR_S.

The golden values are the worked example in
products/assurance_vie_uc/technical-notes.md ("Worked example"), which projects the
anchor cell: male 65, a single premium of 100,000 EUR with a 1.00% `frais sur versement`,
70% to one composite `unites de compte` support and 30% to the `fonds en euros`, a UC
management charge of 0.88% a year, a `garantie plancher` on the `simple` basis levied from
the euro support at the Spirica tariff of 196 EUR per 10,000 EUR of `capital sous risque`,
an arbitrage of 10,000 EUR at ``t = 2``, a partial surrender of 5,000 EUR at ``t = 5``, and
the `stress_yr1` path that rises 1% a month for six months and falls 5% a month for six.
They are hard-coded here rather than pickled so that a reviewer can compare them against
the notes by eye.

The time index is **0-based**: ``t = 0`` is the issue month, the frame is
``t = 0 ... proj_len() - 1``, and the balances at issue are not a row of it - they are the
``*_init`` cells, reached inside month 0 through ``units_open``, ``unit_price_open``,
``av_euro_open_pp`` and ``av_pp_at(t, "OPENING")``.

Tolerances follow the precision the notes display: money to the centime, unit counts and
liquidation values to the fourth decimal - `au dix millieme`, which is the precision the
contract itself guarantees.

Beyond the worked example this module asserts every product fact the notes list as a
modeling pitfall, because each is a way an implementation of *this* product can look right
and be wrong: the plancher is charged on the `capital sous risque` and never on the
account value; the net amount at risk is floored at zero and capped on the risk rather
than on the benefit; an arbitrage never moves the floor, and a `cliquet` floor is reduced
proportionally where a `simple` one is reduced nominally; the management charge is taken
on the opening unit count at ``c/12``; under ``euro_first`` the rider never touches a
single unit; the `prelevements sociaux` fall on the UC leg only at `denouement` and only
on a gain; the social levy, the fund-level costs and the euro credited interest are all
outside ``net_cf``, which is the UC leg plus the rider and not the contract's margin; and
the cover stops at the cessation age rather than extrapolating a tariff that stops at 74.

One assertion here is about the frame rather than the product: ``pols_if(t)`` is the
**start**-of-month count and therefore the weight on its own ``result_cf`` row, with the
notes' end-of-month ``l(t + 1)`` reachable as ``pols_if_at(t, "AFT_DECR")``.  This model
was first written with the **end**-of-month count published under the ``pols_if`` name,
which is silent - the column is the right series one month stale - so it is asserted
rather than assumed.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from fr_registry import LIB, MODELS


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENTIME = 0.005       # money displayed to 2 d.p.
DIXMILL = 0.00005     # unit counts and liquidation values displayed to 4 d.p.

MODEL_DIR = LIB / MODELS["UC_FR_S"][0]

INPUT_CSVS = {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
              "plancher_rate_table.csv", "uc_scenario_table.csv"}

# t: (unit_price, units, av_uc_pp, av_euro_pp, av_pp_at(t,"BEF_DECR"),
#     plancher_amount, nar, mgmt_fee_uc_pp, plancher_charge_pp)
WORKED_EXAMPLE = {
    0:  (101.0000, 692.4918, 69941.67, 29761.18, 99702.85, 99000.00, 0.00, 51.33, 0.00),
    1:  (102.0100, 691.9840, 70589.29, 29822.48, 100411.77, 99000.00, 0.00, 51.80, 0.00),
    2:  (103.0301, 788.0502, 81192.89, 19883.91, 101076.80, 99000.00, 0.00, 52.28, 0.00),
    3:  (104.0604, 787.4723, 81944.69, 19924.87, 101869.55, 99000.00, 0.00, 60.14, 0.00),
    4:  (105.1010, 786.8949, 82703.44, 19965.91, 102669.35, 99000.00, 0.00, 60.69, 0.00),
    5:  (106.1520, 748.3227, 79435.96, 19040.29, 98476.25, 94000.00, 0.00, 61.26, 0.00),
    6:  (100.8444, 747.7739, 75408.83, 19079.51, 94488.34, 94000.00, 0.00, 55.34, 0.00),
    7:  (95.8022, 747.2256, 71585.85, 19113.43, 90699.28, 94000.00, 3295.34, 52.53, 5.38),
    8:  (91.0121, 746.6776, 67956.69, 19141.54, 87098.23, 94000.00, 6890.52, 49.87, 11.25),
    9:  (86.4615, 746.1300, 64511.51, 19164.14, 83675.65, 94000.00, 10307.52, 47.34,
         16.84),
    10: (82.1384, 745.5829, 61240.99, 19181.47, 80422.46, 94000.00, 13555.40, 44.94,
         22.14),
    11: (78.0315, 745.0361, 58136.28, 19193.80, 77330.08, 94000.00, 16642.74, 42.66,
         27.18),
}

# The notes' year-1 per-policy totals row, and the insurer-side extraction beside it.
YEAR_1_PER_POLICY = {"mgmt_fee_uc_pp": 630.20, "plancher_charge_pp": 82.80}

YEAR_1_EXTRACTION = {"prem_charge": 1000.00, "mgmt_fee_uc": 621.33,
                     "arbitrage_fee": 49.73, "plancher_charge": 80.67,
                     "plancher_strain": -49.67, "expenses": -439.41,
                     "net_cf": 1262.66}

YEAR_1_GROSS = {"claims_death": 1158.20, "claims_lapse": 1852.58,
                "withdrawals": 4933.21}

# point_id -> (plancher_amount(11), nar(11), av_pp_at(11,"BEF_LEVY"), year-1 charge)
BASIS_VARIANTS = {
    1: (94000.00, 16642.74, 77357.26, 82.80),      # simple
    3: (97378.25, 20041.15, 77337.10, 108.39),     # indexee, 3.50% p.a.
    4: (94216.29, 16860.46, 77355.83, 84.57),      # cliquet, 12-month ratchet
    5: (98476.25, 21155.09, 77321.17, 126.04),     # cliquet, 1-month ratchet
}

# The notes' derived monthly factors.
C_M = 0.000733333
EURO_FACTOR_M = 1.002059836
PI_65 = 0.0196
Q_M = 0.001005543
W_M = 0.001682143


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_uc_anchor, t):
    """Every cell of the notes' worked-example table, to the displayed precision."""
    price, units, av_uc, av_eur, av, floor, k, fee, charge = WORKED_EXAMPLE[t]
    p = fr_uc_anchor
    assert p.unit_price(t) == pytest.approx(price, abs=DIXMILL)
    assert p.units(t) == pytest.approx(units, abs=DIXMILL)
    assert p.av_uc_pp(t) == pytest.approx(av_uc, abs=CENTIME)
    assert p.av_euro_pp(t) == pytest.approx(av_eur, abs=CENTIME)
    assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(av, abs=CENTIME)
    assert p.plancher_amount(t) == pytest.approx(floor, abs=CENTIME)
    assert p.nar(t) == pytest.approx(k, abs=CENTIME)
    assert p.mgmt_fee_uc_pp(t) == pytest.approx(fee, abs=CENTIME)
    assert p.plancher_charge_pp(t) == pytest.approx(charge, abs=CENTIME)


def test_the_issue_balances_and_the_derived_monthly_factors(fr_uc_anchor):
    """The notes' `init` row, and every factor the notes print - including a nil risk.

    The balances at issue are **not** a row of the 0-based frame: ``t = 0`` is the first
    projected month.  They are the ``*_init`` cells, and month 0 reads them through its own
    opening cells.  That the net amount at risk at issue is zero *exactly* is the point of
    the net-premium floor basis: the rider starts at the money, which is an assertable
    invariant rather than an accident of the premium charge.
    """
    p = fr_uc_anchor
    assert p.prem_to_av_pp() == pytest.approx(99000.00, abs=CENTIME)
    assert p.units_init() == pytest.approx(693.0000, abs=DIXMILL)
    assert p.unit_price_init() == pytest.approx(100.0000, abs=DIXMILL)
    assert p.units_init() * p.unit_price_init() == pytest.approx(69300.00, abs=CENTIME)
    assert p.av_euro_init_pp() == pytest.approx(29700.00, abs=CENTIME)
    assert p.cum_prem_net_init() == pytest.approx(99000.00, abs=CENTIME)
    assert p.uc_cost_basis_init() == pytest.approx(69300.00, abs=CENTIME)
    # The floor at issue equals the account value at issue, so the risk is nil exactly.
    assert p.cum_prem_net_init() - p.prem_to_av_pp() == 0.0
    # Month 0 opens on them, through the opening cells rather than through a t = -1.
    assert p.units_open(0) == pytest.approx(p.units_init(), rel=1e-14)
    assert p.unit_price_open(0) == pytest.approx(p.unit_price_init(), rel=1e-14)
    assert p.av_euro_open_pp(0) == pytest.approx(p.av_euro_init_pp(), rel=1e-14)
    assert p.av_pp_at(0, "OPENING") == pytest.approx(99000.00, abs=CENTIME)
    # The in-force count is read the other way round: pols_if(t) is the count at the
    # START of month t, so the frame opens on pols_if(0).
    assert p.pols_if(0) == p.pols_if_init() == 1.0
    assert p.mgmt_fee_rate_uc_mth() == pytest.approx(C_M, abs=5e-9)
    assert p.euro_credit_factor_mth() == pytest.approx(EURO_FACTOR_M, abs=5e-10)
    assert p.plancher_rate(0) == pytest.approx(PI_65, rel=1e-14)
    assert p.mort_rate_mth(0) == pytest.approx(Q_M, abs=5e-10)
    assert p.lapse_rate_mth(0) == pytest.approx(W_M, abs=5e-10)
    # The euro leg accrues geometrically: 29,700.00 x 1.025^(2/12) = 29,822.48.
    assert p.av_euro_pp(1) == pytest.approx(29700.0 * 1.025 ** (2 / 12), abs=CENTIME)


def test_worked_example_year_one_per_policy_totals(fr_uc_anchor):
    """630.20 of management charge and 82.80 of plancher premium, per policy.

    The notes' totals row is the full-precision column sum rounded once; adding the
    printed cells instead gives 630.18 and 82.79.
    """
    p = fr_uc_anchor
    months = range(12)
    assert sum(p.mgmt_fee_uc_pp(t) for t in months) == pytest.approx(
        YEAR_1_PER_POLICY["mgmt_fee_uc_pp"], abs=CENTIME)
    assert sum(p.plancher_charge_pp(t) for t in months) == pytest.approx(
        YEAR_1_PER_POLICY["plancher_charge_pp"], abs=CENTIME)
    assert sum(round(p.mgmt_fee_uc_pp(t), 2) for t in months) == pytest.approx(
        630.18, abs=CENTIME)
    assert sum(round(p.plancher_charge_pp(t), 2) for t in months) == pytest.approx(
        82.79, abs=CENTIME)


def test_worked_example_insurer_side_extraction(fr_uc_anchor):
    """The notes' year-1 non-unit result of +1,262.66, line by line.

    Every line is weighted at the notes' ``l(t)``, the start-of-month count
    ``pols_if(t)`` the row publishes - and which is why the management charge is 621.33
    here against the per-policy table's 630.20.
    """
    p = fr_uc_anchor
    df = p.result_cf()
    for col in ("prem_charge", "mgmt_fee_uc", "arbitrage_fee", "plancher_charge",
                "net_cf"):
        assert df[col].sum() == pytest.approx(YEAR_1_EXTRACTION[col], abs=CENTIME)
    assert -df["plancher_strain"].sum() == pytest.approx(
        YEAR_1_EXTRACTION["plancher_strain"], abs=CENTIME)
    assert -df["expenses"].sum() == pytest.approx(
        YEAR_1_EXTRACTION["expenses"], abs=CENTIME)
    # 400 of acquisition at issue, then a level 40 a year.
    assert p.expenses(0) - 400.0 == pytest.approx(40.0 / 12, abs=CENTIME)
    assert sum(p.expenses(t) for t in range(12)) - 400.0 == pytest.approx(
        39.41, abs=CENTIME)
    # Both issue items are booked in the FIRST projected month, t = 0: the issue instant
    # is not a row of its own, and pols_if(0) = 1 weights them.
    assert p.prem_charge(0) == pytest.approx(1000.00, abs=CENTIME)
    assert p.expenses(0) == pytest.approx(403.33, abs=CENTIME)
    assert p.net_cf(0) == pytest.approx(647.99, abs=CENTIME)


def test_worked_example_gross_flows_are_not_insurer_cash_flow(fr_uc_anchor):
    """claims_death 1,158.20, claims_lapse 1,852.58, withdrawals 4,933.21 - none of them.

    All three are funded from the policyholder's own account, so they are published and
    excluded, and ``check_benefit_funding`` asserts that they net exactly.
    """
    p = fr_uc_anchor
    df = p.result_cf()
    for col, expected in YEAR_1_GROSS.items():
        assert df[col].sum() == pytest.approx(expected, abs=CENTIME)
    assert p.check_benefit_funding() is True
    assert df["av_releases"].sum() + df["plancher_strain"].sum() == pytest.approx(
        df["claims_death"].sum() + df["claims_lapse"].sum(), abs=CENTIME)


def test_worked_example_terminal_quantities(fr_uc_anchor):
    """uc_cost_basis 75,420.62, l(12) 0.968240, av_at(11,"BEF_DECR") 74,874.07.

    The notes' ``l(12)`` - twelve months of decrements - is ``pols_if_at(11, "AFT_DECR")``,
    the count once the twelfth month's decrements have gone, and not ``pols_if(11)``, which
    is the start-of-month exposure the twelfth ``result_cf`` row is weighted at.
    """
    p = fr_uc_anchor
    assert p.uc_cost_basis(11) == pytest.approx(75420.62, abs=CENTIME)
    assert p.pols_if_at(11, "AFT_DECR") == pytest.approx(0.968240, abs=5e-7)
    assert p.av_at(11, "BEF_DECR") == pytest.approx(74874.07, abs=CENTIME)
    assert p.av_uc_at(11) + p.av_euro_at(11) == pytest.approx(
        p.av_at(11, "BEF_DECR"), rel=1e-14)


def test_worked_example_partial_surrender_settlement(fr_uc_anchor):
    """``t = 5``: 103,476.25 split 0.80665095 UC, 4,033.25 / 966.75, 37.9951 units.

    And the gain component of 203.87 the 17.2% `prelevements sociaux` of 35.07 are
    withheld on.  The cost basis falls pro rata and the floor base nominally: two
    different rules on the same event.
    """
    p = fr_uc_anchor
    assert p.av_uc_bef_wd_pp(5) == pytest.approx(83469.22, abs=CENTIME)
    assert p.av_euro_bef_wd_pp(5) == pytest.approx(20007.04, abs=CENTIME)
    assert p.av_pp_at(5, "BEF_WD") == pytest.approx(103476.25, abs=CENTIME)
    assert p.av_uc_bef_wd_pp(5) / p.av_pp_at(5, "BEF_WD") == pytest.approx(
        0.80665095, abs=5e-9)
    assert p.wd_amount_pp(5) == pytest.approx(5000.00, abs=CENTIME)
    assert p.wd_uc_pp(5) == pytest.approx(4033.25, abs=CENTIME)
    assert p.wd_eur_pp(5) == pytest.approx(966.75, abs=CENTIME)
    assert p.wd_units(5) == pytest.approx(37.9951, abs=DIXMILL)
    assert p.wd_uc_gain_pp(5) == pytest.approx(203.87, abs=CENTIME)
    assert p.social_levy_wd_pp(5) == pytest.approx(35.07, abs=CENTIME)
    assert p.uc_cost_basis(4) == pytest.approx(79250.00, abs=CENTIME)
    assert p.uc_cost_basis(5) == pytest.approx(75420.62, abs=CENTIME)
    assert p.cum_prem_net(4) == pytest.approx(99000.00, abs=CENTIME)
    assert p.cum_prem_net(5) == pytest.approx(94000.00, abs=CENTIME)


def test_worked_example_death_in_the_twelfth_month(fr_uc_anchor):
    """At ``t = 11`` the benefit is 77,330.08 + 16,642.74 = 93,972.82; the insurer funds K.

    It is the floor less that month's own premium, because the levy is in arrears against
    a `capital sous risque` observed before it - the [std] discretization of a design that
    observes weekly and levies monthly.
    """
    p = fr_uc_anchor
    benefit = p.av_pp_at(11, "BEF_DECR") + p.nar(11)
    assert benefit == pytest.approx(93972.82, abs=CENTIME)
    assert p.claims(11, "DEATH") == pytest.approx(benefit * p.pols_death(11), rel=1e-14)
    assert p.plancher_strain(11) == pytest.approx(
        p.nar(11) * p.pols_death(11), rel=1e-14)
    assert benefit == pytest.approx(
        p.plancher_amount(11) - p.plancher_charge_pp(11), abs=CENTIME)
    assert p.av_pp_at(11, "BEF_LEVY") + p.nar(11) == pytest.approx(
        p.plancher_amount(11), abs=CENTIME)


def test_the_unit_count_checks_the_notes_print(fr_uc_anchor):
    """693 (1-c_m)^3 = 691.4765, + 9,950/103.0301 = 96.5737 bought, = 788.0502.

    And from ``t = 5`` the count reaches ``t = 11`` without the rider touching a unit.
    """
    p = fr_uc_anchor
    assert p.units_init() * (1 - C_M) ** 2 == pytest.approx(691.9840, abs=DIXMILL)
    assert p.units_bef_wd(2) - p.arb_units(2) == pytest.approx(691.4765, abs=DIXMILL)
    assert p.arb_units(2) == pytest.approx(9950.0 / 103.0301, abs=DIXMILL)
    assert p.units(2) == pytest.approx(788.0502, abs=DIXMILL)
    assert p.units_bef_wd(5) == pytest.approx(786.3178, abs=DIXMILL)
    assert p.units(5) == pytest.approx(786.3178 - 37.9951, abs=1e-3)
    assert p.units(5) * (1 - C_M) ** 6 == pytest.approx(745.0361, abs=DIXMILL)


def test_the_net_amount_at_risk_closes_on_itself_in_arrears(fr_uc_anchor):
    """The ninth row, ``t = 8``: the base is 87,098.23 + 11.25, and 94,000 less it 6,890.52."""
    p = fr_uc_anchor
    assert p.av_pp_at(8, "BEF_LEVY") == pytest.approx(
        p.av_pp_at(8, "BEF_DECR") + p.plancher_charge_pp(8), rel=1e-14)
    assert p.av_pp_at(8, "BEF_LEVY") == pytest.approx(87109.48, abs=CENTIME)
    assert p.nar(8) == pytest.approx(94000.00 - 87109.48, abs=CENTIME)
    assert p.plancher_charge_pp(8) == pytest.approx(p.nar(8) * PI_65 / 12, rel=1e-14)


def test_the_decrement_conversion_is_geometric(fr_uc_anchor):
    """[(1-q_m)(1-w_m)]^12 = (1-0.012)(1-0.020) = 0.968240 exactly.

    The only sensible test that the monthly rates were derived geometrically rather than
    by dividing by twelve.
    """
    p = fr_uc_anchor
    assert p.mort_rate(0) == pytest.approx(0.012, rel=1e-12)
    assert p.lapse_rate(0) == pytest.approx(0.020, rel=1e-12)
    assert p.pols_if_at(11, "AFT_DECR") == pytest.approx(0.988 * 0.98, rel=1e-12)
    assert p.check_pols_roll_fwd() is True


def test_pols_if_is_the_weight_on_its_own_row(assurance_vie_uc):
    """``pols_if(t)`` is the START-of-month count, and the weight on row t's flows.

    The library's settled ruling, and the one thing about this frame a reader relies on
    without checking: divide any cash flow on row ``t`` by that row's ``pols_if`` and the
    per-policy amount comes back.  This model shipped the other way round once - the
    **end**-of-month count published under the ``pols_if`` name while the flows beside it
    were weighted at the start-of-month one - which is silent, because nothing raises and
    nothing goes NaN; the exposure column is simply the right series one month stale.

    The end-of-month count survives under ``pols_if_at(t, "AFT_DECR")``, which is the
    ``CashValue_SE`` timing form, equals ``pols_if(t + 1)`` wherever the projection runs
    on, and is what ``av_at`` weights the account-value stock by.
    """
    for point_id in assurance_vie_uc.Data.model_point_table().index:
        p = assurance_vie_uc.Projection[point_id]
        df = p.result_cf()
        assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12)
        for t in (0, 5, min(11, p.proj_len() - 1)):
            assert df.loc[t, "pols_if"] == pytest.approx(p.pols_if(t), rel=1e-14)
            # Every flow on the row divides back to its own per-policy amount.
            assert df.loc[t, "mgmt_fee_uc"] == pytest.approx(
                p.pols_if(t) * p.mgmt_fee_uc_pp(t), rel=1e-14)
            assert df.loc[t, "plancher_charge"] == pytest.approx(
                p.pols_if(t) * p.plancher_charge_pp(t), rel=1e-14)
            assert df.loc[t, "withdrawals"] == pytest.approx(
                p.pols_if(t) * p.wd_amount_pp(t), rel=1e-14)
            # The three timings, and the end-of-month count under its own name.
            assert p.pols_if_at(t, "BEF_DECR") == pytest.approx(p.pols_if(t), rel=1e-14)
            assert (p.pols_if_at(t, "BEF_DECR") >= p.pols_if_at(t, "BEF_LAPSE")
                    >= p.pols_if_at(t, "AFT_DECR"))
            if t + 1 < p.proj_len():
                assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(
                    p.pols_if(t + 1), rel=1e-14)
        assert p.av_at(0, "BEF_DECR") == pytest.approx(
            p.av_pp_at(0, "BEF_DECR") * p.pols_if_at(0, "AFT_DECR"), rel=1e-14)
        assert p.check_pols_roll_fwd() is True


@pytest.mark.parametrize("point_id", sorted(BASIS_VARIANTS))
def test_the_plancher_basis_variants(assurance_vie_uc, point_id):
    """simple / indexee / cliquet on the same path, and the unit count in all four.

    ``av_uc_pp(11)`` is 58,136.28 in every one of them, because with the premium levied
    from the euro support the rider never touches the unit count.
    """
    floor, k, av_levy, charge = BASIS_VARIANTS[point_id]
    p = assurance_vie_uc.Projection[point_id]
    assert p.plancher_amount(11) == pytest.approx(floor, abs=CENTIME)
    assert p.nar(11) == pytest.approx(k, abs=CENTIME)
    assert p.av_pp_at(11, "BEF_LEVY") == pytest.approx(av_levy, abs=CENTIME)
    assert sum(p.plancher_charge_pp(t) for t in range(12)) == pytest.approx(
        charge, abs=CENTIME)
    assert p.av_uc_pp(11) == pytest.approx(58136.28, abs=CENTIME)
    assert p.units(11) == pytest.approx(745.036125, abs=1e-6)


# ---------------------------------------------------------------------------
# The garantie plancher: the ways it goes wrong


def test_the_charge_base_is_the_risk_and_not_the_account_value(fr_uc_anchor):
    """27.18 against 126.35 at ``t = 11`` - a factor of 4.6, and the first listed pitfall.

    Out of the money the charge is **exactly** zero, not a small number: the first seven
    months of the anchor cell, ``t = 0 .. 6``.
    """
    p = fr_uc_anchor
    assert p.plancher_charge_pp(11) == pytest.approx(27.18, abs=CENTIME)
    assert p.av_pp_at(11, "BEF_LEVY") * p.plancher_rate_mth(11) == pytest.approx(
        126.35, abs=CENTIME)
    for t in range(7):
        assert p.nar(t) == 0.0
        assert p.plancher_charge_pp(t) == 0.0
        assert p.plancher_charge(t) == 0.0


def test_a_path_that_never_crosses_the_floor_pays_no_plancher_premium(assurance_vie_uc):
    """Model point 11 rises for thirty years: sum(plancher_charge) is exactly zero."""
    p = assurance_vie_uc.Projection[11]
    assert p.plancher_flag() is True
    df = p.result_cf()
    assert df["plancher_charge"].sum() == 0.0
    assert df["plancher_strain"].sum() == 0.0
    assert all(p.av_pp_at(t, "BEF_LEVY") >= p.plancher_amount(t)
               for t in range(p.proj_len()))


def test_the_net_amount_at_risk_is_floored_at_zero(assurance_vie_uc):
    """max(0, F - AV), not F - AV: without the floor the rider pays a rebate.

    On a rising path the unfloored expression is negative every month, which would make
    the premium a credit and the death strain a profit on the policyholder's own units.
    """
    p = assurance_vie_uc.Projection[11]
    assert all(p.plancher_amount(t) - p.av_pp_at(t, "BEF_LEVY") < 0.0
               for t in (11, 119, 299))
    assert all(p.nar(t) == 0.0 for t in (11, 119, 299))
    for point_id in assurance_vie_uc.Data.model_point_table().index:
        assert assurance_vie_uc.Projection[point_id].check_nar_bounds() is True


def test_the_cap_applies_to_the_risk_and_not_to_the_benefit(assurance_vie_uc):
    """Model point 10 runs the cap: K is 300,000 and the benefit is AV + 300,000.

    Capping the death benefit at 300,000 instead would be a different and much cruder
    contract - the beneficiary would receive less than the account value.
    """
    p = assurance_vie_uc.Projection[10]
    assert p.plancher_cap() == 300000.0
    assert p.nar(59) == 300000.0
    assert p.plancher_amount(59) - p.av_pp_at(59, "BEF_LEVY") > 300000.0
    benefit = p.av_pp_at(59, "BEF_DECR") + p.nar(59)
    assert benefit == pytest.approx(p.av_pp_at(59, "BEF_DECR") + 300000.0, rel=1e-14)
    assert p.plancher_charge_pp(59) == pytest.approx(
        300000.0 * p.plancher_rate_mth(59), rel=1e-14)


def test_an_arbitrage_never_moves_the_floor(fr_uc_anchor):
    """The 10,000 switch at ``t = 2`` leaves plancher_amount at 99,000.00.

    ``check_floor_base`` rebuilds the floor base from the withdrawal series by a second
    accumulation, so a model that let the switch move it shows a 10,000 residual.
    """
    p = fr_uc_anchor
    assert p.arb_amount_pp(2) == pytest.approx(10000.00, abs=CENTIME)
    assert p.arb_fee_pp(2) == pytest.approx(50.00, abs=CENTIME)
    assert p.plancher_amount(2) == pytest.approx(99000.00, abs=CENTIME)
    assert p.check_floor_base() is True
    # But both legs moved, and the fee left the contract.
    assert p.av_euro_bef_wd_pp(2) == pytest.approx(
        p.av_euro_aft_credit_pp(2) - 10000.00, rel=1e-14)
    assert p.arb_units(2) * p.unit_price(2) == pytest.approx(9950.00, abs=CENTIME)


def test_the_cliquet_floor_is_reduced_proportionally_not_nominally(assurance_vie_uc):
    """94,216.29 against 94,000.00 at ``t = 11``: a ratchet is a value level.

    The proportional adjustment is the only reason ``cliquet`` differs from ``simple`` in
    a year whose ratchet date locks in nothing; a one-month ratchet locks in the pre-fall
    high instead.  The twelve-month ratchet fires at the **end** of ``t = 11``, which is
    twelve months from issue.
    """
    p1 = assurance_vie_uc.Projection[1]
    p4 = assurance_vie_uc.Projection[4]
    assert p4.plancher_basis() == "cliquet" and p4.plancher_ratchet_months() == 12
    assert p4.plancher_ratchet(11) == pytest.approx(94216.29, abs=CENTIME)
    assert p4.plancher_ratchet(11) == pytest.approx(
        99000.0 * (1 - 5000.0 / p4.av_pp_at(5, "BEF_WD")), abs=CENTIME)
    assert p1.plancher_amount(11) == pytest.approx(94000.00, abs=CENTIME)
    assert p4.plancher_amount(11) > p1.plancher_amount(11)
    p5 = assurance_vie_uc.Projection[5]
    assert p5.plancher_ratchet_months() == 1
    assert p5.plancher_amount(11) == pytest.approx(
        p5.av_pp_at(5, "BEF_LEVY"), abs=CENTIME)


def test_the_indexee_floor_indexes_and_then_deducts_the_nominal_withdrawal(
        assurance_vie_uc):
    """97,378.25 at ``t = 11`` on a 3.50% a year indexation, and it bites two months early."""
    p = assurance_vie_uc.Projection[3]
    assert p.plancher_basis() == "indexee" and p.plancher_index_rate() == 0.035
    r = 1.035 ** (1 / 12)
    assert p.plancher_amount(5) == pytest.approx(99000.0 * r ** 6 - 5000.0, abs=CENTIME)
    assert p.plancher_amount(11) == pytest.approx(
        (99000.0 * r ** 6 - 5000.0) * r ** 6, abs=CENTIME)
    assert p.nar(6) > 0.0 and assurance_vie_uc.Projection[1].nar(6) == 0.0


def test_the_levy_source_decides_whether_the_rider_touches_the_units(assurance_vie_uc):
    """745.036125 under euro_first, 744.044774 under uc_units.

    If the two agree, the levy is not being applied at all.
    """
    p1 = assurance_vie_uc.Projection[1]
    p6 = assurance_vie_uc.Projection[6]
    assert p1.plancher_levy_source() == "euro_first"
    assert p6.plancher_levy_source() == "uc_units"
    assert p1.units(11) == pytest.approx(745.036125, abs=1e-6)
    assert p6.units(11) == pytest.approx(744.044774, abs=1e-6)
    for t in range(7, 12):
        assert p1.plancher_levy_units(t) == 0.0
        assert p1.plancher_levy_eur_pp(t) == pytest.approx(
            p1.plancher_charge_pp(t), rel=1e-14)
        assert p6.plancher_levy_units(t) > 0.0
        assert p6.plancher_levy_eur_pp(t) == 0.0


def test_the_levy_falls_on_the_units_when_the_euro_leg_cannot_pay(assurance_vie_uc):
    """Model point 10 is 100% UC, so ``euro_first`` has nothing to take and cancels units.

    That is the mechanism by which the euro leg's credited rate reaches the UC leg, and it
    is what makes the unit count path-dependent when it happens.
    """
    p = assurance_vie_uc.Projection[10]
    assert p.plancher_levy_source() == "euro_first" and p.euro_alloc() == 0.0
    assert p.av_euro_pp(59) == 0.0 and p.plancher_levy_eur_pp(59) == 0.0
    assert p.plancher_levy_uc_pp(59) == pytest.approx(
        p.plancher_charge_pp(59), rel=1e-14)
    assert p.units(59) < p.units_init() * (1 - p.mgmt_fee_rate_uc_mth()) ** 60
    assert p.check_unit_roll_fwd() is True


def test_the_cover_stops_at_the_cessation_age(assurance_vie_uc):
    """Model point 9 is issued at 73: the rider is on for two years and off from age 75."""
    p = assurance_vie_uc.Projection[9]
    assert p.issue_age() == 73 and p.plancher_end_age() == 75
    assert p.age(23) == 74 and p.age(24) == 75
    assert p.plancher_rate(23) > 0.0 and p.plancher_rate(24) == 0.0
    assert p.nar(23) > 0.0 and p.nar(24) == 0.0
    assert p.plancher_charge_pp(24) == 0.0 and p.plancher_strain(24) == 0.0
    # But the floor would be firmly in the money if the cover had not ceased.
    assert p.plancher_amount(24) > p.av_pp_at(24, "BEF_LEVY")
    assert all(p.nar(t) == 0.0 for t in range(24, p.proj_len()))


def test_the_tariff_is_not_extrapolated_past_the_table(assurance_vie_uc):
    """Push the cessation age past 74 and the model raises rather than inventing a rate."""
    model = mx.read_model(MODEL_DIR, name="UC_FR_S_tariff")
    try:
        table = model.Data.model_point_table()
        table.loc[9, "plancher_end_age"] = 85
        alt = "model_point_table_late.csv"
        table.to_csv(model.Data.input_dir() / alt)
        try:
            model.Data.model_point_file = alt
            model.Data.clear_all()
            model.Projection.clear_all()
            p = model.Projection[9]
            assert p.plancher_rate(23) > 0.0        # age 74, the last published age
            with pytest.raises(FormulaError):
                p.plancher_rate(24)                 # age 75, off the end of the table
        finally:
            (model.Data.input_dir() / alt).unlink(missing_ok=True)
    finally:
        model.close()


def test_the_gross_premium_floor_starts_in_the_money(assurance_vie_uc):
    """Model point 8: the floor is the gross premium, so the risk at issue is the charge."""
    p8 = assurance_vie_uc.Projection[8]
    p1 = assurance_vie_uc.Projection[1]
    assert p8.plancher_gross_basis() is True
    assert p8.cum_prem_net_init() == pytest.approx(100000.00, abs=CENTIME)
    assert p8.cum_prem_net_init() - p8.prem_to_av_pp() == pytest.approx(
        1000.00, abs=CENTIME)
    assert p1.cum_prem_net_init() - p1.prem_to_av_pp() == 0.0
    assert p8.plancher_amount(11) == pytest.approx(
        p1.plancher_amount(11) + 1000.00, abs=CENTIME)
    assert p8.nar(11) > p1.nar(11)


def test_the_rider_is_an_election_not_a_premium(assurance_vie_uc):
    """Model point 7 would be 25,280 in the money and pays nothing: it never elected.

    And the charge is a deduction from an existing account, never a premium: it appears in
    ``plancher_charge`` and never in ``prem_charge``, which is non-zero only at issue.
    """
    p7 = assurance_vie_uc.Projection[7]
    assert p7.plancher_flag() is False
    assert p7.plancher_amount(359) - p7.av_pp_at(359, "BEF_LEVY") > 25000.0
    assert all(p7.nar(t) == 0.0 for t in (0, 119, 239, 359))
    assert p7.result_cf()["plancher_charge"].sum() == 0.0
    df = assurance_vie_uc.Projection[1].result_cf()
    assert df["prem_charge"].iloc[0] == pytest.approx(1000.00, abs=CENTIME)
    assert df["prem_charge"].iloc[1:].sum() == 0.0
    assert df["plancher_charge"].sum() > 0.0


# ---------------------------------------------------------------------------
# The charge mechanics


def test_the_management_fee_is_taken_on_the_opening_unit_count(fr_uc_anchor):
    """52.28 at ``t = 2``, not 59.54: the two differ by the arbitrage's units.

    Immaterial in one month, systematic over decades, and a common source of a persistent
    reconciliation break against an administration system.
    """
    p = fr_uc_anchor
    assert p.fee_units(2) == pytest.approx(
        p.units_open(2) * p.mgmt_fee_rate_uc_mth(), rel=1e-14)
    assert p.units_open(2) == pytest.approx(p.units(1), rel=1e-14)
    assert p.mgmt_fee_uc_pp(2) == pytest.approx(52.28, abs=CENTIME)
    on_closing = p.units(2) * p.mgmt_fee_rate_uc_mth() * p.unit_price(2)
    assert on_closing == pytest.approx(59.54, abs=CENTIME)
    assert p.mgmt_fee_uc_pp(2) != pytest.approx(on_closing, rel=1e-6)


def test_the_monthly_charge_rate_is_c_over_twelve(fr_uc_anchor):
    """c/12, not 1 - (1-c)^(1/12): the insurers compound the periodic rate.

    0.25% a quarter gives an annual factor of (1 - 0.0025)^4 = 0.99003744 and not
    1 - 1.00%, and Suravenir's published table prints 100 x (1 - 0.60%) = 99.4000 after a
    year where a monthly 1/12 levy gives 99.4016.
    """
    p = fr_uc_anchor
    assert p.mgmt_fee_rate_uc_mth() == pytest.approx(0.0088 / 12, rel=1e-15)
    assert p.mgmt_fee_rate_uc_mth() != pytest.approx(
        1 - (1 - 0.0088) ** (1 / 12), rel=1e-6)
    assert (1 - 0.0025) ** 4 == pytest.approx(0.99003744, abs=5e-9)
    assert 100 * (1 - 0.006 / 12) ** 12 == pytest.approx(99.4016, abs=5e-5)


def test_the_recursion_reproduces_the_insurers_published_unit_tables(fr_uc_anchor):
    """Bourso Vie's statutory eight-year table, digit for digit, from the same recursion.

    Independent evidence that the unit count is a deterministic ``(1 - c_p)^n`` sequence,
    which is the whole content of art. A. 132-5 for a model.
    """
    n = 100.0
    for expected in (99.2521, 98.5098, 97.7731, 97.0418, 96.3161, 95.5957, 94.8808,
                     94.1711):
        n *= (1 - 0.001875) ** 4
        assert n == pytest.approx(expected, abs=DIXMILL)
    h = 100.0
    for expected in (99.0037, 98.0174):
        h *= (1 - 0.0025) ** 4
        assert h == pytest.approx(expected, abs=DIXMILL)
    p = fr_uc_anchor
    assert p.units(11) == pytest.approx(p.units(5) * (1 - C_M) ** 6, abs=DIXMILL)


def test_the_account_value_and_the_unit_count_roll_forward(assurance_vie_uc):
    """AV(t) = AV opening + UC return + euro interest - charges - withdrawal - premium.

    Built from the opening unit count and the opening euro balance, so it is an identity
    the recursion has to satisfy rather than a restatement of it.  In the first month the
    opening balance is the premium net of the `frais sur versement`, which is what
    ``av_pp_at(0, "OPENING")`` returns.
    """
    for point_id in assurance_vie_uc.Data.model_point_table().index:
        p = assurance_vie_uc.Projection[point_id]
        assert p.check_av_roll_fwd() is True
        assert p.check_unit_roll_fwd() is True
    p = assurance_vie_uc.Projection[1]
    assert p.av_pp_at(0, "OPENING") == pytest.approx(p.prem_to_av_pp(), rel=1e-14)
    for t in (0, 2, 5, 11):
        assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(
            p.av_pp_at(t, "OPENING") + p.uc_growth_pp(t) + p.euro_interest_pp(t)
            - p.mgmt_fee_uc_pp(t) - p.arb_fee_pp(t) - p.wd_amount_pp(t)
            - p.plancher_charge_pp(t), abs=1e-7)
        if t > 0:
            assert p.av_pp_at(t, "OPENING") == pytest.approx(p.av_pp(t - 1), rel=1e-14)
    # And each month's closing euro balance opens the next month.
    for t in (0, 5, 10):
        assert p.av_euro_aft_credit_pp(t + 1) == pytest.approx(
            p.av_euro_pp(t) * p.euro_credit_factor_mth(), rel=1e-14)


def test_the_timing_strings_and_claim_kinds_validate(fr_uc_anchor):
    with pytest.raises(FormulaError):
        fr_uc_anchor.av_pp_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        fr_uc_anchor.pols_if_at(0, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        fr_uc_anchor.claims(0, "MATURITY")


# ---------------------------------------------------------------------------
# Prelevements sociaux and the other pass-throughs


def test_the_uc_social_levy_falls_at_denouement_and_only_on_a_gain(fr_uc_anchor):
    """The UC leg is 17,284.34 under water at ``t = 11``, so the levy on a death is zero.

    Accruing it year by year is the euro rule, not the UC one: a model that did would
    understate the account value throughout and shrink the base the management charge is
    levied on - and the account value here carries no levy deduction at all.
    """
    p = fr_uc_anchor
    assert p.social_levy_rate == 0.172
    assert p.av_uc_pp(11) - p.uc_cost_basis(11) == pytest.approx(-17284.34, abs=CENTIME)
    assert p.social_levy_decr_pp(11) == 0.0
    assert all(p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-7)
               for t in (0, 5, 11))
    assert p.social_levy_wd_pp(5) == pytest.approx(35.07, abs=CENTIME)
    assert all(p.social_levy_wd_pp(t) == 0.0 for t in (0, 4, 6, 11))


def test_the_pass_throughs_stay_out_of_net_cf(fr_uc_anchor):
    """net_cf is the four income lines less expenses and the death strain, and nothing else.

    The social levy is withheld and remitted; the 1.60% fund-level recurring costs sit
    inside the liquidation value and would put 1,136.76 against a true net_cf of 1,262.66;
    and the euro credited interest is a policyholder credit whose margin is Euro_FR_S's.
    """
    p = fr_uc_anchor
    for t in (0, 5, 11):
        assert p.net_cf(t) == pytest.approx(
            p.prem_charge(t) + p.mgmt_fee_uc(t) + p.arbitrage_fee(t)
            + p.plancher_charge(t) - p.expenses(t) - p.plancher_strain(t), rel=1e-12)
    df = p.result_cf()
    assert df["social_levy_uc"].sum() > 0.0        # published, and excluded
    # Weighted at the same start-of-month exposure as every line inside net_cf, so that
    # the two figures are on one basis; the unweighted per-policy sum is 1,152.86 and is
    # not comparable with a survivorship-weighted net_cf.
    fund_costs = sum(p.pols_if(t) * p.av_uc_pp(t) * 0.016 / 12 for t in range(12))
    assert fund_costs == pytest.approx(1136.76, abs=CENTIME)
    assert sum(p.av_uc_pp(t) * 0.016 / 12 for t in range(12)) == pytest.approx(
        1152.86, abs=CENTIME)
    assert fund_costs > df["net_cf"].sum() * 0.85
    assert sum(p.euro_interest_pp(t) for t in range(12)) > 500.0
    assert df["net_cf"].sum() == pytest.approx(1262.66, abs=CENTIME)
    assert "Euro_FR_S" in p.net_cf.doc


# ---------------------------------------------------------------------------
# Behaviour


def test_the_worked_example_runs_the_base_surrender_table_alone(fr_uc_anchor):
    """lapse_dynamic is `none` on the anchor, which is what the notes' 2.00% a year means.

    The performance multiplier would be 1 through the first twelve months anyway - it
    reads a completed trailing year - but the moneyness multiplier would halve surrender
    from ``t = 7``, and the notes' decrement check would then not close.
    """
    p = fr_uc_anchor
    assert p.lapse_dynamic() == "none"
    assert all(p.lapse_rate(t) == pytest.approx(0.02, rel=1e-12) for t in range(12))
    assert all(p.perf_factor(t) == 1.0 for t in range(12))
    assert p.return_12m(11) == pytest.approx(p.uc_return_ref, rel=1e-14)


def test_the_moneyness_multiplier_halves_surrender_while_the_floor_bites(
        assurance_vie_uc):
    """Model point 9 elects the dynamics: 0.02 x 0.5 in year 1, 0.04 x 1.198 x 0.5 in
    year 2, and the full 0.04 x 1.198 once the cover has ceased and the guarantee is gone.
    """
    p = assurance_vie_uc.Projection[9]
    assert p.lapse_dynamic() == "full"
    assert p.nar(11) > 0.0 and p.plancher_factor(11) == 0.5
    assert p.lapse_rate(11) == pytest.approx(0.02 * 0.5, rel=1e-12)
    assert p.perf_factor(12) == pytest.approx(1 + 2 * (0.049 + 0.05), rel=1e-9)
    assert p.lapse_rate(23) == pytest.approx(0.04 * p.perf_factor(23) * 0.5, rel=1e-12)
    assert p.nar(24) == 0.0 and p.plancher_factor(24) == 1.0
    assert p.lapse_rate(24) == pytest.approx(0.04 * p.perf_factor(24), rel=1e-12)
    assert p.lapse_rate(24) > p.lapse_rate(23)


def test_the_duration_eight_spike_and_the_rate_conventions(assurance_vie_uc):
    """12% in policy year 8 against 6% either side, and lapse_rate_mth below lapse_rate.

    A model with no duration-8 spike has ignored the strongest driver of French surrender
    timing there is: art. 125-0 A CGI made behavioural.
    """
    p = assurance_vie_uc.Projection[2]
    assert p.policy_year(0) == 1 and p.policy_year(89) == 8
    assert p.lapse_rate_base(0) == pytest.approx(0.02, rel=1e-12)
    assert p.lapse_rate_base(12) == pytest.approx(0.04, rel=1e-12)
    assert p.lapse_rate_base(59) == pytest.approx(0.06, rel=1e-12)
    assert p.lapse_rate_base(89) == pytest.approx(0.12, rel=1e-12)
    assert p.lapse_rate_base(99) == pytest.approx(0.06, rel=1e-12)
    for point_id in assurance_vie_uc.Data.model_point_table().index:
        q = assurance_vie_uc.Projection[point_id]
        for t in (0, 12, 24):
            if t < q.proj_len() and q.lapse_rate(t) > 0:
                assert q.lapse_rate_mth(t) < q.lapse_rate(t)
                assert q.mort_rate_mth(t) < q.mort_rate(t)


def test_the_programmed_and_progressive_patterns(assurance_vie_uc):
    """5% of the account value a year taken monthly, and a fixed monthly switch that stops
    of its own accord once the euro support is empty.
    """
    p = assurance_vie_uc.Projection[2]
    assert p.wd_pattern() == "programmed" and p.arb_pattern() == "progressive"
    assert p.wd_amount_pp(0) == pytest.approx(
        p.av_pp_at(0, "BEF_WD") * 0.05 / 12, rel=1e-14)
    assert p.arb_amount_pp(0) == pytest.approx(500.00, abs=CENTIME)
    assert p.av_euro_pp(119) == pytest.approx(0.0, abs=CENTIME)
    assert p.arb_amount_pp(119) == 0.0


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_frames_match_the_notes(fr_uc_anchor):
    """result_cf's column vocabulary, and result_av as the notes' table column for column."""
    df = fr_uc_anchor.result_cf()
    assert df.index.name == "t"
    assert list(df.index) == list(range(12))
    assert df.index[-1] == fr_uc_anchor.proj_len() - 1
    assert list(df.columns) == [
        "pols_if", "av_pp", "prem_charge", "mgmt_fee_uc", "arbitrage_fee",
        "plancher_charge", "plancher_strain", "expenses", "withdrawals",
        "claims_death", "claims_lapse", "av_releases", "social_levy_uc", "net_cf",
    ]
    # No subtotal beside its parts, and no retired column names.
    assert not ({"claims", "claims_surr", "claims_wd"} & set(df.columns))
    av = fr_uc_anchor.result_av()
    for name in ("unit_price", "units", "av_uc_pp", "av_euro_pp", "av_pp",
                 "plancher_amount", "nar", "mgmt_fee_uc_pp", "plancher_charge_pp"):
        assert name in av.columns
    assert av.loc[0, "units"] == pytest.approx(692.4918, abs=DIXMILL)
    assert av.loc[11, "av_pp"] == pytest.approx(77330.08, abs=CENTIME)


def test_every_model_point_publishes_the_same_columns(assurance_vie_uc):
    """A model point the shipped tables cannot serve is a defect, not a documented gap."""
    columns = None
    for point_id in assurance_vie_uc.Data.model_point_table().index:
        p = assurance_vie_uc.Projection[point_id]
        df = p.result_cf()
        assert len(df) == p.proj_len()
        assert df.notna().all().all()
        assert (df["pols_if"] > 0.0).all()
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns


def test_the_docstrings_describe_the_current_structure(assurance_vie_uc):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = assurance_vie_uc.doc
    for phrase in ("mechanics demonstration", "external", "once per model", "non-unit",
                   "garantie plancher", "Euro_FR_S"):
        assert phrase in doc
    proj = assurance_vie_uc.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "av_pp_at", "nar", "plancher_amount",
                  "cum_prem_net", "uc_cost_basis"):
        assert cells in proj
    data = assurance_vie_uc.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "plancher_rate_table"):
        assert cells in data


def test_cells_names_follow_the_account_value_vocabulary(assurance_vie_uc):
    """av_pp_at and check_av_roll_fwd put this model in the library's account-value family."""
    shared = {
        "model_point", "issue_age", "sex", "proj_len", "age", "pols_if", "pols_death",
        "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth", "premium",
        "claims", "expenses", "net_cf", "result_cf", "policy_year", "duration",
        "duration_mth", "av_pp", "av_pp_at", "av_at", "check_av_roll_fwd",
        "withdrawals", "prem_to_av_pp", "pols_if_at", "pols_if_init",
        "units_open", "unit_price_open", "av_euro_open_pp",
    }
    names = set(assurance_vie_uc.Projection.cells) | set(
        assurance_vie_uc.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    retired = {"lapse_rate_ann", "free_wd_used_pp", "free_wd_taken_pp", "prem_net_pp",
               "mort_a_e_factor", "ae_factor", "omega", "check_tol"}
    assert not (names & retired)


def test_inputs_are_external_and_carry_their_provenance(assurance_vie_uc):
    """The five CSVs sit beside run.py; the decrement tables say they are [std] proxies.

    Art. A. 132-8 requires charge maxima to be disclosed and not capped, and the retrieved
    contracts span 0.475% to 1.50% on the management charge alone - so the charge rates
    are model point columns and not a shipped rate card.
    """
    assert INPUT_CSVS == {p.name for p in MODEL_DIR.parent.iterdir()
                          if p.suffix == ".csv"}
    columns = set(assurance_vie_uc.Data.model_point_table().columns)
    for col in ("prem_charge_rate", "mgmt_fee_rate_uc", "arbitrage_fee_rate",
                "euro_credit_rate", "plancher_flag", "plancher_basis",
                "plancher_levy_source", "plancher_cap", "plancher_end_age"):
        assert col in columns
    mort = assurance_vie_uc.Data.mort_table()
    lapse = assurance_vie_uc.Data.lapse_table()
    tariff = assurance_vie_uc.Data.plancher_rate_table()
    assert mort["provenance"].str.startswith("[std]").all()
    assert lapse["provenance"].str.startswith("[std]").all()
    assert tariff["provenance"].str.contains(r"\[S4").all()
    # The mortality proxy is anchored on the notes' placeholder; the tariff is Spirica's.
    assert float(mort.loc[("M", 65), "mort_rate"]) == pytest.approx(0.015, rel=1e-12)
    assert assurance_vie_uc.Projection.mort_be_factor == 0.8
    assert int(tariff.index.min()) == 12 and int(tariff.index.max()) == 74
    assert float(tariff.loc[65, "premium_per_10000"]) == 196.0
    assert float(tariff.loc[74, "premium_per_10000"]) == 408.0


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows."""
    import pandas as pd

    sticky = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    sticky["lapse_rate"] = sticky["lapse_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="UC_FR_S_swap")
    try:
        alt_name = "lapse_table_sticky.csv"
        sticky.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[2].result_cf()["mgmt_fee_uc"].sum()
            model.Data.lapse_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Halving surrender keeps policies in force, so more charge is collected.
            assert model.Projection[2].result_cf()["mgmt_fee_uc"].sum() > base
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="UC_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="UC_FR_S_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.units(t) == pytest.approx(row[1], abs=DIXMILL)
            assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(row[4], abs=CENTIME)
            assert p.nar(t) == pytest.approx(row[6], abs=CENTIME)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
