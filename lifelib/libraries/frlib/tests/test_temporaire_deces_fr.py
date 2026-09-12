"""Golden and structural tests for TD_FR_S.

The golden values are the worked example in
products/temporaire_deces/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: a revisable-cotisation *assurance temporaire
décès* on a male aged 58 on the *différence de millésime* basis, 150 000 EUR of constant
capital, death cover to attained age 75 and PTIA cover to 65, annual cotisation, standard
rates, no waiting period and no accidental option.  Model point 1 is that cell.

The time index ``t`` counts **policy months**, 0-based: ``t = 0`` is the first policy
month and the frame is ``t = 0 ... proj_len() - 1`` with
``proj_len() = 12 x (75 - 58) = 204`` the *number* of projected months, whose last index
is 203.  The contractual policy year is the derived 1-based label
``policy_year(t) = duration(t) + 1`` with ``duration(t) = t // 12``, which is what the two
policy-year-keyed CSVs are read at.

The notes' worked example is therefore two tables, and so are the goldens here:
``MONTHS_YEAR_1`` is the twelve months of policy year 1 (``t = 0 ... 11``), and
``WORKED_EXAMPLE`` is the same frame summed into policy years 1-17 through
``result_cf_annual()`` -- which is the seventeen-row table the annual-step model this
replaced published, and still the **entire** projection rather than a slice of one, so
every row of it is asserted here.

They are hard-coded rather than pickled so that a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent,
``pols_if`` to six decimals, and the totals at full precision -- 10 094,20 EUR of death
claims that way against 10 094,19 EUR if the seventeen rounded cells are added.

Beyond the worked example this module asserts the fourteen product facts the notes list
as modeling pitfalls -- the ways an implementation of *this* product looks right and is
wrong: the cotisation is **revisable** and moves every year; PTIA is an **acceleration**
and never a second payment; PTIA cover stops **before** death cover, at a hard age gate;
``q_d`` and ``q_p`` are **dependent** rates and therefore additive; there is **no
surrender value**, by statute, at any duration; the age basis is the *différence de
millésime*; the tariff grid is a lookup whose +38 % step at age 60 must survive; the
suicide factor touches death claims in the first year and nothing else; the premium-cessation rule
is applied once; nothing exists at or beyond ``t = proj_len``; the two premium forms do **not**
collect the same projected total; a *surprime* scales the cotisation and never the
capital; the fractionation loading and the *frais d'échéance* are charges of different
kinds; and the accidental option is a share and not an uplift.

It also asserts the conversion itself, decision by decision: that twelve monthly rates
compound back to exactly the annual ones on the **combined** insured decrement, that the
in-force at every anniversary is what the annual recursion gives, that
``result_cf_annual()`` is the monthly frame regrouped and not a second projection, and
that each annual **contract term** -- the repricing, the suicide year, the commission
year, the expense inflation step, the final year's zero lapse, the *constante*
equivalence, the selective-lapsation and premium-shock modules -- lands on the policy year
and not inside it.
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


def boy(year):
    """The **first** month of 1-based contractual policy year ``year``: ``12 * (year - 1)``.

    Policy years are 1-based here because that is the label the contract, the two
    policy-year-keyed CSVs and ``result_cf_annual()``'s index all use; ``duration`` is the
    0-based companion and is ``year - 1``.
    """
    return 12 * (year - 1)


def anniv(year):
    """The **last** month of 1-based policy year ``year``: ``12 * year - 1``.

    The anniversary that closes the year; the next month, ``12 * year``, opens the next
    one and is where every annual contract term steps.
    """
    return 12 * year - 1


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

N_YEARS = 17                  # the anchor cell's cover, in policy years
PROJ_LEN = 12 * N_YEARS       # 204 months

MODEL_DIR = LIB / MODELS["TD_FR_S"][0]

# The notes' first table: the twelve months of policy year 1 on the anchor cell.
# t: (pols_if, premiums, claims_death, claims_ptia, expenses, commissions, net_cf).
# The whole annual cotisation falls in month 0 and nothing else does, which is what an
# annual-mode policy looks like on a monthly grid; model point 4 is the contrast.
MONTHS_YEAR_1 = {
    0:  (1.000000, 1575.00, 49.11, 10.02, 882.14, 630.00,  633.73),
    1:  (0.989007,    0.00, 48.57,  9.91,   2.12,   0.00,  -60.60),
    2:  (0.978135,    0.00, 48.03,  9.80,   2.10,   0.00,  -59.93),
    3:  (0.967383,    0.00, 47.51,  9.70,   2.07,   0.00,  -59.28),
    4:  (0.956748,    0.00, 46.98,  9.59,   2.05,   0.00,  -58.62),
    5:  (0.946231,    0.00, 46.47,  9.48,   2.03,   0.00,  -57.98),
    6:  (0.935829,    0.00, 45.96,  9.38,   2.01,   0.00,  -57.34),
    7:  (0.925542,    0.00, 45.45,  9.28,   1.98,   0.00,  -56.71),
    8:  (0.915367,    0.00, 44.95,  9.17,   1.96,   0.00,  -56.09),
    9:  (0.905305,    0.00, 44.46,  9.07,   1.94,   0.00,  -55.47),
    10: (0.895353,    0.00, 43.97,  8.97,   1.92,   0.00,  -54.86),
    11: (0.885510,    0.00, 43.49,  8.87,   1.90,   0.00,  -54.26),
}

# The notes' second table: the same frame summed into policy years 1-17.  `pols_if` is
# the count entering the year, l(12(y-1)), which is what the annual-step model carried on
# the same row -- and the reason that column, `premiums` and the tariff columns are
# unchanged from the annual goldens while claims and expenses are not.
# policy_year: (attained age, r(x), pols_if, premiums, claims_death, claims_ptia,
#               expenses, net_cf)
WORKED_EXAMPLE = {
    1:  (58, 0.0105, 1.000000, 1575.00, 554.94, 113.25, 904.22,    2.58),
    2:  (59, 0.0113, 0.875776, 1484.44, 546.03, 109.21,  96.12,  733.09),
    3:  (60, 0.0156, 0.784075, 1834.73, 538.15, 107.63, 111.97, 1076.98),
    4:  (61, 0.0168, 0.717235, 1807.43, 541.82, 108.36, 109.47, 1047.77),
    5:  (62, 0.0181, 0.670010, 1819.08, 551.70, 110.34, 109.19, 1047.84),
    6:  (63, 0.0197, 0.625542, 1848.48, 561.45, 112.29, 109.83, 1064.91),
    7:  (64, 0.0214, 0.583667, 1873.57, 571.01, 114.20, 110.28, 1078.07),
    8:  (65, 0.0233, 0.544230, 1902.08, 580.35,   0.00, 110.83, 1210.91),
    9:  (66, 0.0255, 0.507836, 1942.47, 590.28,   0.00, 112.12, 1240.07),
    10: (67, 0.0278, 0.473561, 1974.75, 599.98,   0.00, 113.04, 1261.73),
    11: (68, 0.0288, 0.441280, 1906.33, 609.40,   0.00, 108.94, 1187.98),
    12: (69, 0.0314, 0.410875, 1935.22, 618.48,   0.00, 109.74, 1207.00),
    13: (70, 0.0343, 0.382236, 1966.60, 627.16,   0.00, 110.68, 1228.76),
    14: (71, 0.0374, 0.355260, 1993.01, 635.36,   0.00, 111.39, 1246.25),
    15: (72, 0.0409, 0.329849, 2023.62, 643.01,   0.00, 112.34, 1268.27),
    16: (73, 0.0446, 0.305913, 2046.56, 650.03,   0.00, 112.92, 1283.61),
    17: (74, 0.0486, 0.283369, 2065.76, 675.04,   0.00, 113.62, 1277.10),
}

# The notes' Total row, summed at full precision and then rounded.  `premiums` is the
# annual grid's own figure to the cent; the other four moved with the finer grid.
TOTALS = {"premiums": 31999.13, "claims_death": 10094.20, "claims_ptia": 775.29,
          "expenses": 2666.69, "net_cf": 18462.95}

# What the annual-step model this replaced produced, quoted as the comparison.
ANNUAL_GRID_TOTALS = {"premiums": 31999.13, "claims_death": 10396.90,
                      "claims_ptia": 804.25, "expenses": 2676.38, "net_cf": 18121.59}

# The level-premium variant -- the same cell with premium_form = constante and
# level_premium = 0, so P_lev is derived by equivalence.  Model point 2, summed into
# policy years.  policy_year: (prem_pp, premiums, claims_death, claims_ptia, expenses,
# net_cf).
LEVEL_VARIANT = {
    1:  (3914.39, 3914.39, 554.94, 113.25, 1839.98, 1406.22),
    2:  (3914.39, 3428.13, 546.03, 109.21,  193.30, 2579.59),
    3:  (3914.39, 3069.17, 538.15, 107.63,  173.69, 2249.70),
    8:  (3914.39, 2130.33, 580.35,   0.00,  122.24, 1427.74),
    17: (3914.39, 1109.22, 675.04,   0.00,   65.79,  368.39),
}

LEVEL_TOTALS = {"premiums": 36367.46, "claims_death": 10094.20, "claims_ptia": 775.29,
                "expenses": 3703.89, "net_cf": 21794.07}


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(MONTHS_YEAR_1))
def test_worked_example_month_row(fr_td_anchor, t):
    """Every cell of the notes' month-level table, the twelve months of policy year 1.

    This is where the monthly grid is visible: the annual cotisation and the acquisition
    cost fall in month 0 and nothing else does, and the eleven months after it carry only
    claims and a twelfth of the maintenance charge.
    """
    pols_if, prem, cd, cp, exp, comm, net = MONTHS_YEAR_1[t]
    p = fr_td_anchor
    assert p.duration(t) == 0 and p.policy_year(t) == 1
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "PTIA") == pytest.approx(cp, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.commissions(t) == pytest.approx(comm, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.claims(t, "LAPSE") == 0.0


def test_the_month_zero_decrement_is_the_check_on_the_rate_conversion(fr_td_anchor):
    """The notes' own arithmetic on the first month, spelled out.

    ``q_d(0) = 0,00400`` and ``q_p(0) = 0,00080`` give a combined annual insured decrement
    of 0,00480, so ``1 - (1 - 0,0048)^(1/12) = 0,00040088``, split 0,00033407 / 0,00006681
    in the exact ratio 0,20; ``w(0) = 12 %`` gives ``1 - (1 - 0,12)^(1/12) = 0,01059624``;
    so ``l(1) = (1 - 0,00040088)(1 - 0,01059624) = 0,989007``, and twelve such months land
    on ``l(12) = 0,875776`` -- the annual model's ``l(1)``, exactly.
    """
    p = fr_td_anchor
    assert p.mort_rate(0) == pytest.approx(0.00400, rel=1e-12)
    assert p.ptia_rate(0) == pytest.approx(0.00080, rel=1e-12)
    assert p.decr_rate(0) == pytest.approx(0.00480, rel=1e-12)
    assert p.decr_rate_mth(0) == pytest.approx(0.00040088, abs=5e-9)
    assert p.mort_rate_mth(0) == pytest.approx(0.00033407, abs=5e-9)
    assert p.ptia_rate_mth(0) == pytest.approx(0.00006681, abs=5e-9)
    assert p.ptia_rate_mth(0) == pytest.approx(0.20 * p.mort_rate_mth(0), rel=1e-15)
    assert p.lapse_rate_mth(0) == pytest.approx(0.01059624, abs=5e-9)
    assert p.pols_if(1) == pytest.approx(
        (1 - p.decr_rate_mth(0)) * (1 - p.lapse_rate_mth(0)), rel=1e-15)
    assert p.pols_if(1) == pytest.approx(0.989007, abs=SIX_DP)
    assert p.pols_if(12) == pytest.approx(0.875776, abs=SIX_DP)


@pytest.mark.parametrize("year", sorted(WORKED_EXAMPLE))
def test_worked_example_policy_year(fr_td_anchor, year):
    """Every cell of the notes' seventeen-row table, read off ``result_cf_annual()``."""
    age, rate, pols_if, prem, cd, cp, exp, net = WORKED_EXAMPLE[year]
    p = fr_td_anchor
    row = p.result_cf_annual().loc[year]
    t0 = boy(year)
    assert p.age(t0) == age
    assert p.prem_rate(t0) == pytest.approx(rate, rel=1e-12)
    assert row["pols_if"] == pytest.approx(pols_if, abs=SIX_DP)
    assert p.pols_if(t0) == pytest.approx(pols_if, abs=SIX_DP)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_ptia"] == pytest.approx(cp, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)
    assert row["claims_lapse"] == 0.0


def test_the_worked_example_totals_are_summed_at_full_precision(fr_td_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells."""
    df = fr_td_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    # And the rounded-cell sum really does differ, which is why this test exists.
    assert sum(round(WORKED_EXAMPLE[y][4], 2) for y in WORKED_EXAMPLE) == pytest.approx(
        10094.19, abs=CENT)


def test_the_finer_grid_moved_exactly_the_columns_it_should_have(fr_td_anchor):
    """Premium income is the annual grid's own figure; claims and expenses are not.

    The comparison the conversion rests on, stated as arithmetic rather than left to the
    prose.  An annual-mode cotisation is collected on the anniversary and weighted by the
    anniversary in-force under either grid, so it does not move at all.  Claims fall at
    the end of the month of claim on a block that has been decrementing all year, and the
    maintenance charge is borne by the in-force of each month, so both come in **below**
    an anniversary weighting -- and ``net_cf`` is the residual, up 1,9 %.
    """
    df = fr_td_anchor.result_cf()
    assert df["premiums"].sum() == pytest.approx(
        ANNUAL_GRID_TOTALS["premiums"], abs=CENT)
    for column in ("claims_death", "claims_ptia", "expenses"):
        assert df[column].sum() < ANNUAL_GRID_TOTALS[column], column
    assert df["net_cf"].sum() > ANNUAL_GRID_TOTALS["net_cf"]
    assert df["claims_death"].sum() / ANNUAL_GRID_TOTALS["claims_death"] - 1 == (
        pytest.approx(-0.029, abs=0.001))
    assert df["expenses"].sum() / ANNUAL_GRID_TOTALS["expenses"] - 1 == (
        pytest.approx(-0.0036, abs=0.0005))


def test_the_policy_year_3_row_rebuilt_from_scratch(fr_td_anchor):
    """The notes' own independent rebuild, now of policy year 3 and of its first month.

    The in-force rebuild is exact on either grid -- ``l(24) = l(12) x (1 - 0,005232) x
    0,90``, the annual factors term for term -- while the cash-flow rebuild is now a
    single *month*'s product, month 24, because a policy year's claims are the sum of
    twelve of them.
    """
    p = fr_td_anchor
    assert p.pols_if(12) == pytest.approx(0.99520 * 0.88, rel=1e-9)
    assert p.mort_rate(12) == pytest.approx(0.00400 * 1.09, rel=1e-9)
    assert p.ptia_rate(12) == pytest.approx(0.000872, rel=1e-9)
    assert p.pols_if(24) == pytest.approx(0.875776 * 0.8952912, abs=1e-8)
    assert p.mort_rate(24) == pytest.approx(0.0047524, rel=1e-9)
    assert p.ptia_rate(24) == pytest.approx(0.00095048, rel=1e-9)
    # Month 24, the first month of policy year 3: one instalment, one twelfth of the
    # maintenance charge, and a month of claims at the monthly rates.
    assert p.premiums(24) == pytest.approx(2340.00 * 0.78407455, abs=CENT)
    assert p.claims(24, "DEATH") == pytest.approx(
        150000 * 0.78407455 * p.mort_rate_mth(24), abs=CENT)
    assert p.claims(24, "PTIA") == pytest.approx(
        150000 * 0.78407455 * p.ptia_rate_mth(24), abs=CENT)
    assert p.commissions(24) == pytest.approx(0.05 * 2340.00 * 0.78407455, abs=CENT)
    assert p.claim_expenses(24) == pytest.approx(
        150 * 0.78407455 * p.decr_rate_mth(24), abs=0.0005)
    assert p.expenses(24) == pytest.approx(1.6995 + 91.7367 + 0.0560, abs=CENT)
    assert p.net_cf(24) == pytest.approx(1685.20, abs=CENT)
    # And the policy year is the sum of its twelve months, not a second projection.
    row = p.result_cf_annual().loc[3]
    assert row["net_cf"] == pytest.approx(
        sum(p.net_cf(t) for t in range(boy(3), boy(4))), rel=1e-12)


def test_the_decrements_close_four_ways(fr_td_anchor):
    """The notes' closure split: deaths, PTIA, lapses and survivors sum to exactly one.

    The last term is ``pols_if(proj_len)`` -- one past the frame's last index -- the
    expiring cohort, which exists so the identity closes and is a weight on no cash flow.
    It is **exactly the annual-step model's 0,27886852**, because it is a pure anniversary
    quantity; the three exit terms are not, because a decrementing block reaches the claim
    decrements later in the year and correspondingly more of the cohort leaves as a lapse.
    """
    p = fr_td_anchor
    n = p.proj_len()
    assert n == PROJ_LEN
    deaths = sum(p.pols_death(t) for t in range(n))
    ptia = sum(p.pols_ptia(t) for t in range(n))
    lapses = sum(p.pols_lapse(t) for t in range(n))
    assert deaths == pytest.approx(0.06737020, abs=5e-9)
    assert ptia == pytest.approx(0.00516859, abs=5e-9)
    assert lapses == pytest.approx(0.64859269, abs=5e-9)
    assert p.pols_if(n) == pytest.approx(0.27886852, abs=5e-9)
    assert deaths + ptia + lapses + p.pols_if(n) == pytest.approx(1.0, abs=1e-12)
    # The annual grid's own split, for the contrast the notes draw.
    assert deaths < 0.06939268 and ptia < 0.00536169 and lapses > 0.64637711


# ---------------------------------------------------------------------------
# The conversion itself


def test_the_monthly_rates_compound_back_to_the_annual_ones(fr_td_anchor):
    """Twelve monthly rates compound to exactly the annual rate the notes tabulate.

    This is what makes the two grids reconcile at anniversaries, so it is asserted
    directly rather than only through its consequence.  The rate that must compound back
    is the **combined** insured decrement ``q_d + q_p``, because ``q_d`` and ``q_p`` are
    dependent rates of one two-decrement table and it is their sum the annual recursion
    applies; converting each apart and adding the results misses it.  The only safe
    monotonic assertion on ``1 - (1 - q)^(1/12)`` is that it is *below* the annual rate --
    it is not ``q / 12`` and not linear in ``q``.
    """
    p = fr_td_anchor
    for t in (0, 7, 13, 100, 125, 200):
        assert 1 - (1 - p.mort_rate_mth(t) - p.ptia_rate_mth(t)) ** 12 == pytest.approx(
            p.decr_rate(t), rel=1e-12)
        assert 1 - (1 - p.lapse_rate_mth(t)) ** 12 == pytest.approx(
            p.lapse_rate(t), rel=1e-12)
        assert p.mort_rate_mth(t) < p.mort_rate(t)
        if p.lapse_rate(t) > 0.0:
            assert p.lapse_rate_mth(t) < p.lapse_rate(t)
    # The naive per-rate conversion is the one this model does not do, and the gap is
    # already material at the first anniversary.
    naive = ((1 - (1 - p.mort_rate(0)) ** (1 / 12))
             + (1 - (1 - p.ptia_rate(0)) ** (1 / 12)))
    assert (1 - naive) ** 12 == pytest.approx(0.9952029339, abs=5e-11)
    assert (1 - p.decr_rate(0)) == pytest.approx(0.9952000000, abs=5e-11)
    # The proportional split keeps the acceleration ratio exact at every month.
    for t in (0, 11, 12, 83):
        assert p.ptia_rate_mth(t) == pytest.approx(
            p.ptia_ratio * p.mort_rate_mth(t), rel=1e-15)


def test_the_annual_rates_are_properties_of_the_policy_year_not_of_the_month(
        fr_td_anchor):
    """``mort_rate``, ``ptia_rate`` and ``lapse_rate`` are flat across a policy year.

    The library convention the whole ``*_rate`` / ``*_rate_mth`` split rests on, and the
    reason ``lapse_rate_ann`` is a retired name: the unsuffixed cells keeps the annual
    meaning the technical notes give it.
    """
    p = fr_td_anchor
    for year in (1, 3, 8, 17):
        for cells in ("mort_rate", "ptia_rate", "lapse_rate", "prem_rate", "prem_pp",
                      "benefit_pp", "suicide_factor", "inflation_factor"):
            values = {getattr(p, cells)(t) for t in range(boy(year), boy(year) + 12)}
            assert len(values) == 1, (cells, year, sorted(values))


def test_in_force_at_every_anniversary_matches_the_annual_recursion(fr_td_anchor):
    """``pols_if(12k)`` is exactly what an annual step would carry, over the whole frame.

    The annual recursion is written out here from the model's own annual vectors rather
    than taken from a fixture, so this asserts the equivalence and not a memory of it.
    Because the combined insured decrement and the lapse rate each compound back to their
    annual values, twelve months collapse to ``l(t+12) = l(t)(1 - q_d - q_p)(1 - w)``.
    """
    p = fr_td_anchor
    expected = p.pols_if_init()
    for year in range(1, N_YEARS + 1):
        t = boy(year)
        assert p.pols_if(t) == pytest.approx(expected, abs=1e-12), f"policy year {year}"
        expected *= (1 - p.decr_rate(t)) * (1 - p.lapse_rate(t))
    # And the expiring cohort, one anniversary past the frame.
    assert p.pols_if(p.proj_len()) == pytest.approx(expected, abs=1e-12)


def test_result_cf_annual_is_the_monthly_frame_summed(fr_td_anchor):
    """The annual view is the frame regrouped, never a second projection."""
    p = fr_td_anchor
    df, ann = p.result_cf(), p.result_cf_annual()
    assert ann.index.name == "policy_year"
    assert list(ann.index) == list(range(1, N_YEARS + 1))
    assert list(ann.columns) == list(df.columns)
    for year in (1, 3, 8, 17):
        rows = df.loc[boy(year):anniv(year)]
        assert len(rows) == 12
        assert ann.loc[year, "pols_if"] == p.pols_if(boy(year))
        for column in df.columns:
            if column != "pols_if":
                assert ann.loc[year, column] == pytest.approx(
                    rows[column].sum(), rel=1e-12), (year, column)


def test_the_time_index_triple_reads_as_the_library_writes_it(fr_td_anchor):
    """``duration_mth`` / ``duration`` / ``policy_year``, and the age that steps yearly."""
    p = fr_td_anchor
    assert p.proj_len_y() == N_YEARS
    assert p.proj_len() == PROJ_LEN == 12 * (75 - 58)
    assert [p.duration_mth(t) for t in (0, 11, 12, 203)] == [0, 11, 12, 203]
    assert [p.duration(t) for t in (0, 11, 12, 203)] == [0, 0, 1, 16]
    assert [p.policy_year(t) for t in (0, 11, 12, 203)] == [1, 1, 2, 17]
    assert [p.age(t) for t in (0, 11, 12, 192, 203)] == [58, 58, 59, 74, 74]
    assert len(p.result_cf()) == PROJ_LEN
    assert len(p.result_cf_annual()) == N_YEARS


# ---------------------------------------------------------------------------
# The level-premium variant


@pytest.mark.parametrize("year", sorted(LEVEL_VARIANT))
def test_level_premium_variant_policy_year(temporaire_deces, year):
    """The notes' constante table: only the premium and the commission change."""
    prem_pp, prem, cd, cp, exp, net = LEVEL_VARIANT[year]
    p = temporaire_deces.Projection[2]
    row = p.result_cf_annual().loc[year]
    assert p.premium_form() == "constante"
    assert p.prem_pp(boy(year)) == pytest.approx(prem_pp, abs=CENT)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims_death"] == pytest.approx(cd, abs=CENT)
    assert row["claims_ptia"] == pytest.approx(cp, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)


def test_the_level_premium_is_reached_two_independent_ways(temporaire_deces):
    """P_lev = 60 476,2476 / 15,449728 = 3 914,3891, and also a weighted mean of the grid.

    The second route never forms the premium stream: ``P_lev / SA`` is the
    ``v^y p_tau(y)``-weighted mean of the seventeen grid rates, 2,60959276 %.

    The equivalence is an **annual** construction and stays one on the monthly grid --
    :func:`disc_factor` and :func:`pols_tariff` take a 0-based *policy year*, not a month,
    and the sums run over ``range(proj_len_y())``.  Re-striking it monthly would move
    ``P_lev`` and break the identity the notes assert, so all three figures are unchanged
    by the conversion.
    """
    p = temporaire_deces.Projection[2]
    assert p.tariff_prem_pv() == pytest.approx(60476.2476, abs=CENT)
    assert p.tariff_annuity() == pytest.approx(15.449728, abs=5e-7)
    assert p.prem_level_pp() == pytest.approx(3914.3891, abs=5e-5)
    assert p.proj_len_y() == N_YEARS
    weights = [p.disc_factor(y) * p.pols_tariff(y) for y in range(p.proj_len_y())]
    assert len(weights) == N_YEARS
    assert p.disc_factor(1) == pytest.approx(1 / 1.005, rel=1e-12)
    mean_rate = sum(w * p.prem_rate(boy(y + 1)) for y, w in enumerate(weights))
    mean_rate /= sum(weights)
    assert mean_rate == pytest.approx(0.0260959276, rel=1e-8)
    assert p.sum_assured() * mean_rate == pytest.approx(3914.3891, abs=5e-5)
    assert p.prem_level_pp() * p.tariff_annuity() == pytest.approx(60476.25, abs=CENT)
    # Model point 3 supplies 3 900,00 EUR instead, so the derivation branch is not taken.
    given = temporaire_deces.Projection[3]
    assert given.level_premium() == 3900.0
    assert all(given.prem_pp(t) == 3900.0 for t in (0, 50, 203))
    assert given.result_cf()["premiums"].sum() < p.result_cf()["premiums"].sum()


# ---------------------------------------------------------------------------
# Pitfalls 1 and 7 -- the cotisation is revisable, and the grid is not smoothed


def test_the_revisable_cotisation_moves_with_attained_age(temporaire_deces, fr_td_anchor):
    """The French default is revisable, not constante -- the notes' first pitfall.

    ``prem_pp(24)/prem_pp(12) = 1,56/1,13 = 1,380531`` -- policy year 3 against policy
    year 2 -- and over the whole cover the cotisation multiplies by
    ``r(74)/r(58) = 4,6286``, a figure that depends only on the grid and not at all on the
    capital.  It is re-read on the **anniversary only**, so there are seventeen distinct
    cotisations over 204 months and not 204.
    """
    p = fr_td_anchor
    assert p.premium_form() == "revisable"
    assert len({p.prem_pp(boy(y)) for y in range(1, N_YEARS + 1)}) == N_YEARS
    assert len({p.prem_pp(t) for t in range(p.proj_len())}) == N_YEARS
    assert p.prem_pp(24) / p.prem_pp(12) == pytest.approx(1.56 / 1.13, rel=1e-12)
    assert p.prem_pp(24) / p.prem_pp(12) == pytest.approx(1.380531, abs=5e-7)
    assert p.prem_pp(0) == pytest.approx(1575.00, abs=CENT)
    assert p.prem_pp(192) == pytest.approx(7290.00, abs=CENT)
    assert p.prem_pp(192) / p.prem_pp(0) == pytest.approx(4.86 / 1.05, rel=1e-12)
    assert p.prem_pp(192) / p.prem_pp(0) == pytest.approx(4.6286, abs=5e-5)
    # Model point 12 is the same cell at 20 000 EUR: the same ratios, 7,5x less money.
    # It is also the notes' expense sensitivity -- a year-one cotisation of 210 EUR
    # against 250 EUR of acquisition expense, so on small capitals the expense assumption
    # and not mortality decides whether the cell is viable.
    small = temporaire_deces.Projection[12]
    assert small.prem_pp(0) == pytest.approx(210.00, abs=CENT)
    assert small.prem_pp(192) / small.prem_pp(0) == pytest.approx(
        p.prem_pp(192) / p.prem_pp(0), rel=1e-12)
    assert small.result_cf_annual().loc[1, "net_cf"] < 0.0


def test_the_tariff_grid_is_a_lookup_and_keeps_its_step(temporaire_deces):
    """The +38 % step from 59 to 60 is in the published grid; a fitted curve loses it."""
    table = temporaire_deces.Data.premium_rate_table()
    r59 = float(table.loc[("maif_2019", 59), "prem_rate"])
    r60 = float(table.loc[("maif_2019", 60), "prem_rate"])
    assert r60 / r59 == pytest.approx(1.380531, abs=5e-7)
    assert float(table.loc[("maif_2019", 58), "prem_rate"]) == 0.0105
    assert float(table.loc[("maif_2019", 74), "prem_rate"]) == 0.0486
    # The flat 18-34 entry band is a feature of the card, not a gap in it.
    assert {float(table.loc[("maif_2019", a), "prem_rate"])
            for a in range(18, 35)} == {0.0015}


# ---------------------------------------------------------------------------
# Pitfalls 2, 3 and 4 -- PTIA


def test_the_capital_is_never_paid_twice(fr_td_anchor):
    """PTIA is an acceleration: total claim events cannot exceed the policy.

    And the amounts follow the events exactly but for the first-year suicide withholding:
    ``150 000 x (0,06737020 + 0,00516859) = 10 880,82`` against 10 869,49 paid, a gap of
    11,33 EUR which is precisely ``0,02 x 150 000 x`` the deaths of policy year 1.  That
    the exclusion is the *only* gap is what "acceleration, not addition" means
    arithmetically.
    """
    p = fr_td_anchor
    n = p.proj_len()
    events = sum(p.pols_death(t) + p.pols_ptia(t) for t in range(n))
    paid = sum(p.claims(t, "DEATH") + p.claims(t, "PTIA") for t in range(n))
    deaths_year_1 = sum(p.pols_death(t) for t in range(12))
    assert events <= 1.0
    assert events == pytest.approx(0.07253879, abs=5e-9)
    assert p.sum_assured() * events == pytest.approx(10880.82, abs=CENT)
    assert paid == pytest.approx(10869.49, abs=CENT)
    assert p.sum_assured() * events - paid == pytest.approx(11.33, abs=CENT)
    assert (1 - p.suicide_factor(0)) * p.sum_assured() * deaths_year_1 == (
        pytest.approx(11.33, abs=CENT))


def test_a_ptia_life_leaves_the_in_force(fr_td_anchor):
    """A life removed by the PTIA decrement must not appear in ``l(t+1)``.

    If it did, the closure residual would be positive at every t after the first PTIA
    claim while the cash flows still looked plausible.  Both roll-forwards now have to
    close **month by month**, not only at the anniversary.
    """
    p = fr_td_anchor
    assert p.check_pols_roll_fwd() is True
    assert p.check_decrement_closure() is True
    for t in (0, 1, 11, 83, 84, 203):
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_decrement_closure_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_ptia_cover_stops_before_death_cover(temporaire_deces, fr_td_anchor):
    """A hard gate on the attained age, not a taper, at both extremes of the model points.

    On the anchor cell ``age(84) = ptia_end_age = 65``, so the cover is off for the whole
    of contractual policy year 8 -- months 84 to 95 -- and every month after it: ``>=``,
    not ``>``.  Because the attained age steps on the anniversary, the gate closes on an
    anniversary too.  Model point 11 enters at exactly ``ptia_end_age`` and never
    attaches; model point 7 never switches off.
    """
    p = fr_td_anchor
    assert p.ptia_end_age() == 65 and p.cover_end_age() == 75
    assert all(p.ptia_rate(t) > 0.0 for t in range(84))
    assert all(p.ptia_rate(t) == 0.0 for t in range(84, PROJ_LEN))
    assert all(p.ptia_rate_mth(t) == 0.0 for t in range(84, PROJ_LEN))
    assert all(p.claims(t, "PTIA") == 0.0 for t in range(84, PROJ_LEN))
    assert all(p.claims(t, "DEATH") > 0.0 for t in range(84, PROJ_LEN))
    assert p.check_ptia_gate() is True

    never = temporaire_deces.Projection[11]
    assert never.issue_age() == never.ptia_end_age() == 65
    assert never.proj_len() == 120 and never.proj_len_y() == 10
    assert never.result_cf()["claims_ptia"].sum() == 0.0
    assert never.result_cf()["claims_death"].sum() > 0.0
    assert never.check_ptia_gate() is True

    always = temporaire_deces.Projection[7]
    assert always.ptia_end_age() == always.cover_end_age() == 65
    assert all(always.ptia_rate(t) > 0.0 for t in range(always.proj_len()))
    assert always.check_ptia_gate() is True


def test_the_competing_risks_are_dependent_rates_and_therefore_additive(fr_td_anchor):
    """q_d + q_p, not 1 - (1-q_d)(1-q_p): 0.00480000 against 0.00479680 at t = 0.

    Immaterial here -- 0,48 EUR of first-year claims per 150 000 EUR of capital -- and
    material at older ages.  The in-force recursion is where the convention shows, on the
    monthly rates within a month and on the annual ones across a policy year.
    """
    p = fr_td_anchor
    qd, qp = p.mort_rate(0), p.ptia_rate(0)
    assert qd + qp == pytest.approx(0.00480000, rel=1e-12)
    assert p.decr_rate(0) == pytest.approx(qd + qp, rel=1e-15)
    assert 1.0 - (1.0 - qd) * (1.0 - qp) == pytest.approx(0.00479680, rel=1e-9)
    # Within the month, on the monthly split of the combined rate.
    qdm, qpm = p.mort_rate_mth(0), p.ptia_rate_mth(0)
    assert p.pols_if_at(0, "BEF_LAPSE") == pytest.approx(1.0 - qdm - qpm, rel=1e-12)
    assert p.pols_if(1) == pytest.approx(
        (1.0 - qdm - qpm) * (1.0 - p.lapse_rate_mth(0)), rel=1e-12)
    # Across the policy year, on the annual ones -- the annual-step model's own recursion.
    assert p.pols_if(12) == pytest.approx((1.0 - qd - qp) * (1.0 - 0.12), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 5 -- there is no surrender value


def test_a_lapse_pays_nothing_at_any_duration(temporaire_deces, fr_td_anchor):
    """Art. L. 132-23 forbids both rachat and reduction, so the column is zeros.

    The absent names are asserted too: they are exactly what a reader arriving from a US
    model with cash surrender values would add, and every total would still look sane.
    """
    p = fr_td_anchor
    assert all(p.claims(t, "LAPSE") == 0.0 for t in range(p.proj_len()))
    assert (p.result_cf()["claims_lapse"] == 0.0).all()
    assert p.check_no_cash_value() is True
    assert p.pols_lapse(0) > 0.0          # the lapses are real; only the benefit is nil
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    for absent in ("av_pp_at", "av_at", "prem_to_av_pp", "cv_pp", "surr_charge_rate",
                   "surr_value_pp", "paid_up_factor", "asset_share", "mvr",
                   "claims_surr", "withdrawals", "wd_free_pp"):
        assert absent not in names, absent


# ---------------------------------------------------------------------------
# Pitfall 6 -- the age basis


def test_the_age_basis_is_the_difference_de_millesime(fr_td_anchor):
    """Calendar year less birth year, so age(t) = issue_age + duration(t) and nothing else.

    The age steps on the **policy anniversary**, at ``t = 12, 24, ...``, and not monthly;
    the finer grid does not make it finer.  A one-year shift moves ``prem_pp(0)`` from
    1 575,00 EUR (age 58) to 1 695,00 EUR (age 59) -- a 7,6 % error in year one that
    compounds through the whole projection.
    """
    p = fr_td_anchor
    assert p.issue_age() == 58
    assert [p.age(t) for t in (0, 11, 12, 192, 203)] == [58, 58, 59, 74, 74]
    assert p.prem_pp(0) == pytest.approx(1575.00, abs=CENT)
    assert p.prem_pp(11) == pytest.approx(1575.00, abs=CENT)
    assert p.prem_pp(12) == pytest.approx(1695.00, abs=CENT)
    assert 1695.00 / 1575.00 - 1 == pytest.approx(0.076, abs=0.0005)
    # issue_date is carried and drives nothing: the millesime basis needs only the age.
    assert p.issue_date() == "2026-01-01"


def test_pricing_is_unisex_while_the_model_point_still_carries_sex(temporaire_deces):
    """Art. L. 111-7 forbids sex-based premium and benefit differences.

    Model point 8 is the anchor cell as a woman: same tariff rate, same mortality rate.
    Only the payment frequency differs, which is what actually moves her cotisation -- she
    pays quarterly, so the annual charge is the same 1 644,00 EUR whichever grid it is read
    on while the *instalment* is a quarter of it.
    """
    male, female = temporaire_deces.Projection[1], temporaire_deces.Projection[8]
    assert male.sex() == "M" and female.sex() == "F"
    assert female.prem_rate(0) == male.prem_rate(0)
    assert female.mort_rate(0) == male.mort_rate(0)
    assert female.mort_rate_mth(0) == male.mort_rate_mth(0)
    assert female.benefit_pp(0) == male.benefit_pp(0)
    assert female.prem_pp(0) == pytest.approx(150000 * 0.0105 * 1.04 + 6.0, abs=CENT)
    assert female.prem_freq() == "quarterly"
    assert female.prem_inst_pp(0) == pytest.approx(female.prem_pp(0) / 4, rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 8 -- the suicide factor


def test_the_suicide_factor_touches_death_in_the_first_year_and_nothing_else(
        temporaire_deces, fr_td_anchor):
    """Art. L. 132-7 voids the death cover for suicide in the **first policy year**.

    The statute says "au cours de la première année du contrat", so the exclusion covers
    months ``t = 0 ... 11`` in full and not merely month 0 -- a monthly grid does not turn
    a statutory year into a month.  PTIA is not death, so it is never touched.  The
    art. R. 132-5 immediate-cover ceiling of 120 000 EUR belongs to principal-residence
    loan cover; importing it would cap the anchor cell's first-year death benefit, so its
    absence is visible in the numbers and not only in the cells list.
    """
    p = fr_td_anchor
    assert all(p.suicide_factor(t) == 0.98 for t in (0, 6, 11))
    assert all(p.suicide_factor(t) == 1.0 for t in (12, 13, 203))
    for t in (0, 11):
        assert p.claims(t, "DEATH") == pytest.approx(
            0.98 * p.benefit_pp(t) * p.pols_death(t), rel=1e-12)
    assert p.claims(12, "DEATH") == pytest.approx(
        p.benefit_pp(12) * p.pols_death(12), rel=1e-12)
    assert p.claims(0, "PTIA") == pytest.approx(
        p.benefit_pp(0) * p.pols_ptia(0), rel=1e-12)
    assert p.benefit_death_pp(0) == 150000.0
    assert p.claims(0, "DEATH") / p.pols_death(0) > 120000.0
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    for absent in ("immediate_cover_cap", "suicide_cover_cap", "loan_cover_cap"):
        assert absent not in names


# ---------------------------------------------------------------------------
# Pitfall 9 and the expense ledger


def test_the_premium_cessation_rule_is_applied_once(fr_td_anchor):
    """Instalments are in advance and claims at month end, so a claimant has already paid.

    Multiplying ``premiums(t)`` by ``(1 - q_dm - q_pm)`` as well applies the rule twice.
    On the monthly grid the item it would double-count is one *month's* decrement on one
    instalment, which is where the finer grid has already put the real effect: the
    instalments after the first are collected on a block that has genuinely lost lives.
    """
    p = fr_td_anchor
    for t in (0, 12, 100, 192):
        assert p.premiums(t) == pytest.approx(p.prem_inst_pp(t) * p.pols_if(t), rel=1e-12)
    twice = p.prem_inst_pp(0) * p.pols_if(0) * (
        1 - p.mort_rate_mth(0) - p.ptia_rate_mth(0))
    assert p.premiums(0) - twice == pytest.approx(1575.00 * p.decr_rate_mth(0), abs=CENT)


def test_commissions_are_inside_expenses_not_beside_them(fr_td_anchor):
    """expenses(0) = 250 + 2,08 + 0,06 + 630 = 882,14, and the last term is the commission.

    The maintenance term is one twelfth of the 25 EUR annual charge, so the twelve months
    of policy year 1 total 904,22 EUR of expense.  ``result_cf()`` publishes both columns
    because the notes' table does, so an implementation that also subtracted
    ``commissions`` from ``net_cf`` would charge it twice -- loudest in the first year,
    where the commission is 40 % of the cotisation.
    """
    p = fr_td_anchor
    assert p.commissions(0) == pytest.approx(0.40 * 1575.00, abs=CENT)
    assert p.claim_expenses(0) == pytest.approx(150 * p.decr_rate_mth(0), abs=CENT)
    assert p.expenses(0) == pytest.approx(250.0 + 25.0 / 12 + 0.06 + 630.0, abs=CENT)
    assert p.result_cf_annual().loc[1, "expenses"] == pytest.approx(904.22, abs=CENT)
    assert p.net_cf(0) == pytest.approx(
        p.premiums(0) - p.claims(0) - p.expenses(0), rel=1e-12)
    assert (p.result_cf()["commissions"] <= p.result_cf()["expenses"]).all()
    # The rate steps on the anniversary; the base is the instalment collected.
    assert p.commissions(11) == 0.0                # no instalment due, so no commission
    assert p.commissions(12) == pytest.approx(0.05 * p.premiums(12), rel=1e-12)


def test_expense_inflation_steps_at_the_anniversary_and_not_monthly(fr_td_anchor):
    """``inflation_factor(t) = 1.02^(policy_year(t) - 1)`` -- the frlib house form.

    ``Obseques_FR_S``, ``ADE_FR_S`` and ``Dep_FR_S`` all step the factor by policy year
    rather than compounding it continuously as ``Term_US_S`` does, and the notes tabulate
    the maintenance charge per policy year.  The choice is stated rather than inherited
    because a continuous factor would move the within-year expense numbers.

    What the finer grid does change is the *weight*: a twelfth of the charge is borne by
    the in-force of each month, so a decrementing block carries 254,60 EUR of maintenance
    over the cover against the annual grid's 263,96 EUR.
    """
    p = fr_td_anchor
    assert p.inflation_factor(0) == 1.0
    assert all(p.inflation_factor(t) == 1.0 for t in range(12))
    assert p.inflation_factor(12) == pytest.approx(1.02, rel=1e-12)
    assert p.inflation_factor(24) == pytest.approx(1.02 ** 2, rel=1e-12)
    assert p.inflation_factor(203) == pytest.approx(1.02 ** 16, rel=1e-12)
    maint = sum(25.0 / 12 * p.inflation_factor(t) * p.pols_if(t)
                for t in range(p.proj_len()))
    assert maint == pytest.approx(254.60, abs=CENT)
    assert maint < 263.96


# ---------------------------------------------------------------------------
# Pitfall 10 -- nothing exists past the age limit


def test_nothing_runs_past_the_age_limit(temporaire_deces, fr_td_anchor):
    """proj_len is the number of projected months, and there is no tail state after it.

    ``proj_len() = 12 x (cover_end_age - issue_age) = 204``, so the frame is
    ``t = 0 ... 203`` -- 204 rows whose last index is ``proj_len() - 1``.  No maturity
    benefit, no renewal, no conversion and no post-level-term phase -- the last of which
    ``Term_US_S`` has and importing it here would invent.

    In the final projected **policy year** a lapse and an expiry are the same event paying
    the same nothing, so ``lapse_rate`` is zero through the whole of it, months 192 to 203
    and not only month 203.  That is what makes the notes' closure split 64,859 % lapses
    and 27,887 % survivors, and it changes no cash flow.  Zeroing only the last month
    would leave eleven months of 6 % lapse inside the final year and move the expiring
    cohort away from the notes' own figure.
    """
    p = fr_td_anchor
    assert p.proj_len_y() == 75 - 58 == 17
    assert p.proj_len() == PROJ_LEN
    df = p.result_cf()
    assert list(df.index) == list(range(PROJ_LEN))
    assert df.index[-1] == p.proj_len() - 1
    assert df.index.name == "t"
    assert p.pols_if(PROJ_LEN) == pytest.approx(0.27886852, abs=5e-9)
    assert p.pols_if(PROJ_LEN + 1) == 0.0
    assert p.pols_if_at(PROJ_LEN - 1, "AFT_DECR") == pytest.approx(
        p.pols_if(PROJ_LEN), rel=1e-12)
    for t in range(boy(N_YEARS), PROJ_LEN):
        assert p.lapse_rate_base(t) == 0.06, t
        assert p.lapse_rate(t) == 0.0, t
        assert p.lapse_rate_mth(t) == 0.0, t
        assert p.pols_lapse(t) == 0.0, t
    assert p.lapse_rate(boy(N_YEARS) - 1) == pytest.approx(0.06, rel=1e-12)
    assert p.pols_lapse(boy(N_YEARS) - 1) > 0.0
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    for absent in ("claims_maturity", "pols_maturity", "maturity_benefit_pp",
                   "conv_rate", "renewal_rate", "jump_ratio", "shock_lapse_rate",
                   "lapse_rate_ann", "prem_pp_mth", "prem_period_m"):
        assert absent not in names


# ---------------------------------------------------------------------------
# Pitfalls 11, 12, 13 and 14


def test_the_two_premium_forms_do_not_collect_the_same_total(temporaire_deces):
    """36 367,46 EUR against 31 999,13 EUR -- correct, not a bug.

    The equivalence ignores lapse, so once lapses truncate the expensive late years the
    level form collects more.  The identity that holds is the discounted one, and not a
    single claim moves.  Both totals are unchanged by the conversion, because both points
    pay annually and an annual cotisation is collected on the anniversary under either
    grid; what moved is the ``net_cf`` sensitivity, from +18,4 % to +18,04 %, because the
    claims underneath both forms fell.
    """
    rev, lev = temporaire_deces.Projection[1], temporaire_deces.Projection[2]
    rdf, ldf = rev.result_cf(), lev.result_cf()
    assert rdf["premiums"].sum() == pytest.approx(31999.13, abs=CENT)
    for column, total in LEVEL_TOTALS.items():
        assert ldf[column].sum() == pytest.approx(total, abs=CENT), column
    assert (rdf["claims_death"] - ldf["claims_death"]).abs().max() < 1e-9
    assert (rdf["claims_ptia"] - ldf["claims_ptia"]).abs().max() < 1e-9
    assert (rdf["pols_if"] - ldf["pols_if"]).abs().max() < 1e-12
    # The notes' sensitivity: +13,7 % of premium and +18,04 % of net_cf.
    assert ldf["premiums"].sum() / rdf["premiums"].sum() - 1 == pytest.approx(
        0.137, abs=0.001)
    assert ldf["net_cf"].sum() / rdf["net_cf"].sum() - 1 == pytest.approx(
        0.1804, abs=0.0005)
    assert lev.prem_level_pp() * lev.tariff_annuity() == pytest.approx(
        rev.tariff_prem_pv(), rel=1e-9)


def test_a_surprime_scales_the_cotisation_and_never_the_capital(temporaire_deces):
    """Model point 5 is the anchor cell at rating_factor 1.50 on a smoker.

    Claims are invariant to it: a *surprime* buys the same capital at a higher price.
    """
    rated, std = temporaire_deces.Projection[5], temporaire_deces.Projection[1]
    assert rated.rating_factor() == 1.5 and rated.smoker() == "S"
    assert rated.prem_pp(0) == pytest.approx(1.5 * std.prem_pp(0), rel=1e-12)
    rdf, sdf = rated.result_cf(), std.result_cf()
    assert (rdf["claims_death"] - sdf["claims_death"]).abs().max() < 1e-9
    assert (rdf["claims_ptia"] - sdf["claims_ptia"]).abs().max() < 1e-9
    assert (rdf["pols_if"] - sdf["pols_if"]).abs().max() < 1e-12
    assert rated.benefit_pp(0) == std.benefit_pp(0)
    assert rdf["premiums"].sum() == pytest.approx(1.5 * sdf["premiums"].sum(), rel=1e-12)


def test_the_fractionation_loading_and_the_fee_are_charges_of_different_kinds(
        temporaire_deces):
    """A multiplier inside the cotisation, plus a fixed euro fee added once a year.

    Model point 4 is monthly: 200 000 x 0,44 % x 1,04 = 915,20 EUR of loaded cotisation
    plus 18,00 EUR of *frais d'échéance*.  Applying the fee as a further percentage, or
    loading the already-loaded cotisation with it, overstates premium income.
    """
    p = temporaire_deces.Projection[4]
    assert p.prem_freq() == "monthly"
    assert p.prem_freq_load() == 1.04 and p.prem_freq_fee() == 18.0
    assert p.prem_tariff_pp(0) == pytest.approx(200000 * 0.0044 * 1.04, abs=CENT)
    assert p.prem_pp(0) == pytest.approx(915.20 + 18.00, abs=CENT)
    # The fee is flat in t while the loaded cotisation climbs with the grid, and it is
    # charged once a year at every t -- the notes' P(t) = P_tar(t) + F.
    assert p.prem_pp(29) - p.prem_tariff_pp(29) == pytest.approx(18.0, abs=CENT)
    assert all(p.prem_pp(t) - p.prem_tariff_pp(t) == pytest.approx(18.0, abs=CENT)
               for t in range(p.proj_len()))
    # It is part of what the policyholder pays, so it reaches premium income and the
    # commission base -- while the constante equivalence is struck on P_tar alone.
    assert p.premiums(0) == pytest.approx(p.prem_inst_pp(0) * p.pols_if(0), rel=1e-12)
    assert p.commissions(12) == pytest.approx(0.05 * p.premiums(12), rel=1e-12)
    half = temporaire_deces.Projection[10]
    assert half.prem_freq() == "half_yearly"
    assert half.prem_pp(0) == pytest.approx(250000 * 0.0015 * 1.025 + 3.0, abs=CENT)
    annual = temporaire_deces.Projection[1]
    assert annual.prem_freq_load() == 1.0 and annual.prem_freq_fee() == 0.0


def test_the_modal_cotisation_is_collected_in_instalments_on_its_own_cycle(
        temporaire_deces):
    """The *fractionnement* is collected on the mode's cycle, not on the anniversary.

    The one cycle in this product the **model point** chooses rather than the contract, so
    it is the one thing the monthly grid collects other than annually.  Twelve monthly
    instalments sum to exactly the annual cotisation, fee included, which is what
    *freq_loading_table.csv* says of the monthly mode; the annual *frais d'échéance* is
    therefore charged once a year and not twelve times.

    Consequence, stated rather than hidden: the instalments after the first are collected
    on a block that has already lost lives, so the three fractionated points collect 1,6 %
    to 3,1 % less than the annual grid did.  That is the premium-cessation rule finally
    biting where an annual grid could not express it.
    """
    monthly = temporaire_deces.Projection[4]
    assert monthly.prem_instalments() == 12 and monthly.prem_cycle() == 1
    assert all(monthly.prem_due(t) for t in range(24))
    assert monthly.prem_inst_pp(0) == pytest.approx(933.20 / 12, abs=5e-5)
    assert monthly.prem_inst_pp(0) == pytest.approx(77.7667, abs=5e-5)
    assert sum(monthly.prem_inst_pp(t) for t in range(12)) == pytest.approx(
        monthly.prem_pp(0), rel=1e-12)
    assert monthly.result_cf()["premiums"].sum() == pytest.approx(29404.08, abs=CENT)
    assert monthly.result_cf()["premiums"].sum() < 30358.26      # the annual grid's total

    half = temporaire_deces.Projection[10]
    assert half.prem_instalments() == 2 and half.prem_cycle() == 6
    assert [t for t in range(12) if half.prem_due(t)] == [0, 6]
    assert half.prem_inst_pp(6) == pytest.approx(half.prem_pp(6) / 2, rel=1e-12)
    assert half.prem_inst_pp(5) == 0.0
    assert half.result_cf()["premiums"].sum() == pytest.approx(13171.49, abs=CENT)

    quarterly = temporaire_deces.Projection[8]
    assert quarterly.prem_instalments() == 4 and quarterly.prem_cycle() == 3
    assert [t for t in range(12) if quarterly.prem_due(t)] == [0, 3, 6, 9]
    assert quarterly.result_cf()["premiums"].sum() == pytest.approx(32433.73, abs=CENT)

    # An annual payer collects the whole cotisation in the first month of the policy year
    # and nothing in the other eleven -- which is why its totals do not move at all.
    annual = temporaire_deces.Projection[1]
    assert annual.prem_instalments() == 1 and annual.prem_cycle() == 12
    assert [t for t in range(24) if annual.prem_due(t)] == [0, 12]
    assert annual.prem_inst_pp(0) == pytest.approx(annual.prem_pp(0), rel=1e-12)
    assert all(annual.premiums(t) == 0.0 for t in range(1, 12))
    assert annual.result_cf()["premiums"].sum() == pytest.approx(31999.13, abs=CENT)


def test_the_accidental_option_is_a_share_and_not_an_uplift(temporaire_deces):
    """It pays an additional capital on the accidental share, not on every claim.

    Model point 6 is model point 1 with the multiplier at 2.00.  With ``acc_share = 0`` --
    no retrieved source gives an accidental share of deaths -- the two frames must be
    identical to the last bit; supply a share and the multiplier starts to matter.
    """
    opt, base = temporaire_deces.Projection[6], temporaire_deces.Projection[1]
    assert opt.accident_multiplier() == 2.0 and base.accident_multiplier() == 1.0
    assert opt.acc_share == 0.0
    assert all(opt.accident_extra_pp(t) == 0.0 for t in range(opt.proj_len()))
    assert (opt.result_cf() - base.result_cf()).abs().max().max() == 0.0

    model = mx.read_model(MODEL_DIR, name="TD_FR_S_acc")
    try:
        model.Projection.acc_share = 0.1
        model.Projection.clear_all()
        # (2.00 - 1) x 0.10 x 150 000 = 15 000 EUR of extra capital per claim.
        assert model.Projection[6].accident_extra_pp(0) == pytest.approx(15000.0)
        assert model.Projection[1].accident_extra_pp(0) == 0.0
        assert model.Projection[6].result_cf()["claims_death"].sum() > (
            base.result_cf()["claims_death"].sum())
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The delai d'attente


def test_the_waiting_period_returns_the_cotisations_and_suspends_ptia(temporaire_deces):
    """Model point 9 carries a one-year *délai d'attente* on a 40 000 EUR capital.

    ``waiting_period_y`` is a length in *contractual policy years*, so the window is
    ``duration_mth(t) < 12 x waiting_period_y()`` -- months ``t = 0 ... 11``, exactly the
    annual model's ``t = 0``.  Inside it an illness-caused death pays back what was
    **collected** -- 296,00 EUR, the single annual cotisation this annual-mode point pays
    in month 0 -- and PTIA pays nothing; from month 12 the full capital is at risk again.
    The window changes what a claim pays, never who leaves.  Only this one model point
    elects one; five of the eight carriers have none.

    Counting the window in months is what the sources actually state (12 months at one
    carrier, 3 months at another) and makes a sub-annual window expressible for the first
    time; no shipped model point uses one, so no ``waiting_period_m`` column exists.
    """
    p = temporaire_deces.Projection[9]
    assert p.waiting_period_y() == 1
    assert p.in_waiting(0) is True and p.in_waiting(11) is True
    assert p.in_waiting(12) is False
    assert p.prem_pp(0) == pytest.approx(296.00, abs=CENT)
    assert p.prem_inst_pp(0) == pytest.approx(296.00, abs=CENT)
    assert p.prem_refund_pp(0) == pytest.approx(296.00, abs=CENT)
    assert p.prem_refund_pp(11) == pytest.approx(296.00, abs=CENT)
    assert p.prem_refund_pp(12) == pytest.approx(612.00, abs=CENT)
    assert p.benefit_death_pp(11) == pytest.approx(296.00, abs=CENT)
    assert p.benefit_ptia_pp(0) == 0.0
    assert p.claims(0, "PTIA") == 0.0
    assert p.claims(0, "DEATH") == pytest.approx(
        0.98 * 296.00 * p.pols_death(0), abs=CENT)
    assert p.benefit_death_pp(12) == 40000.0
    assert p.claims(12, "PTIA") > 0.0
    assert p.pols_ptia(0) > 0.0            # a benefit is suppressed, not a decrement
    assert p.check_decrement_closure() is True
    table = temporaire_deces.Data.model_point_table()
    assert (table["waiting_period_y"] > 0).sum() == 1
    assert table.loc[1, "waiting_period_y"] == 0
    assert "waiting_period_m" not in table.columns


# ---------------------------------------------------------------------------
# Modules that are off in the base run


def test_the_behaviour_modules_are_off_and_reachable(temporaire_deces):
    """Base run values, so the worked example reproduces with the machinery still there."""
    proj = temporaire_deces.Projection
    assert proj.tariff_drift == 0.0
    assert proj.shock_lapse_beta == 0.0 and proj.shock_lapse_g0 == 0.1
    assert proj.sel_lapse_lambda == 0.0 and proj.sel_lapse_ref == 0.3
    assert proj.acc_share == 0.0
    p = temporaire_deces.Projection[1]
    assert all(p.shock_lapse_factor(t) == 1.0 for t in (0, 24, 203))
    assert all(p.sel_lapse_factor(t) == 1.0 for t in (0, 24, 203))
    assert all(p.mort_rate(t) == p.mort_rate_base(t) for t in (0, 24, 203))


def test_the_premium_shock_module_bites_where_the_grid_steps():
    """Switched on, M_shock lifts the lapse rate through policy year 3 and nowhere else.

    The grid's +38 % step at age 60 is the only renewal whose cotisation rise clears the
    10 % tolerance, which is the whole point of carrying the module on a revisable form.
    The ratio is between consecutive **renewals**, ``P(t)/P(t-12)`` -- on a monthly grid
    ``P(t)/P(t-1)`` would be 1 in eleven months of twelve and the module would never fire
    at all -- so the multiplier is one number for the whole of policy year 3, months 24 to
    35, and the elevated annual rate is then spread over those months by ``lapse_rate_mth``.
    """
    model = mx.read_model(MODEL_DIR, name="TD_FR_S_shock")
    try:
        model.Projection.shock_lapse_beta = 1.5
        model.Projection.clear_all()
        p = model.Projection[1]
        expected = 1.0 + 1.5 * (1.380531 - 1.0 - 0.10)
        for t in range(boy(3), boy(4)):
            assert p.shock_lapse_factor(t) == pytest.approx(expected, abs=1e-6), t
            assert p.lapse_rate(t) > 0.08
        assert all(p.shock_lapse_factor(t) == 1.0
                   for t in (0, 11, 12, 23, 36, 48, 108, 180))
        assert p.lapse_rate_mth(24) == pytest.approx(
            1 - (1 - p.lapse_rate(24)) ** (1 / 12), rel=1e-15)
        assert p.result_cf()["premiums"].sum() < 31999.13
    finally:
        model.close()


def test_the_selective_lapsation_module_loads_persisters():
    """q_d_eff = q_d (1 + lambda max(0, w_cum - w_ref)), off at lambda = 0.

    Cumulative lapse reaches 64,9 % over the worked configuration, so the loading is
    reached and then grows -- larger here than on a UK guaranteed-premium term policy.

    ``lapse_cum`` now moves every month, but it is read **at the anniversary**, so the
    loaded ``mort_rate`` stays one annual rate for its policy year.  Letting it drift
    month by month would break the library's ``*_rate`` / ``*_rate_mth`` split and the
    anniversary equivalence with it, so the constancy is asserted directly.
    """
    model = mx.read_model(MODEL_DIR, name="TD_FR_S_sel")
    try:
        model.Projection.sel_lapse_lambda = 0.25
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.lapse_cum(0) == 0.0 and p.sel_lapse_factor(0) == 1.0
        assert p.lapse_cum(192) > 0.30
        # Read at the anniversary: one factor and one annual rate for the whole year.
        for year in (5, 12):
            factors = {p.sel_lapse_factor(t) for t in range(boy(year), boy(year) + 12)}
            assert len(factors) == 1, (year, sorted(factors))
            assert factors.pop() == pytest.approx(
                1.0 + 0.25 * max(0.0, p.lapse_cum(boy(year)) - 0.30), rel=1e-12)
            assert len({p.mort_rate(t)
                        for t in range(boy(year), boy(year) + 12)}) == 1
        # But lapse_cum itself does move every month inside a policy year.
        assert p.lapse_cum(boy(5) + 6) > p.lapse_cum(boy(5))
        assert p.mort_rate(192) > p.mort_rate_base(192)
        assert p.check_pols_roll_fwd() is True
        assert p.check_decrement_closure() is True
    finally:
        model.close()


def test_tariff_drift_reprices_the_card_and_nothing_else():
    """A drift assumption is a premium-income assumption, not a mortality one.

    The drift compounds on ``duration(t)``, completed policy **years**, because a
    re-rating of the card is an annual act; compounding it on ``t`` would reprice the card
    twelve times a year.
    """
    model = mx.read_model(MODEL_DIR, name="TD_FR_S_drift")
    try:
        model.Projection.tariff_drift = 0.02
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.prem_rate(0) == pytest.approx(0.0105, rel=1e-12)
        assert p.prem_rate(11) == pytest.approx(0.0105, rel=1e-12)
        assert p.prem_rate(24) == pytest.approx(0.0156 * 1.02 ** 2, rel=1e-12)
        assert p.mort_rate(24) == pytest.approx(0.00400 * 1.09 ** 2, rel=1e-8)
        assert p.result_cf()["premiums"].sum() > 31999.13
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_both_signs_of_the_net_flow(fr_td_anchor):
    """The notes' eight columns plus liability_cf, the notes' own outgo orientation."""
    df = fr_td_anchor.result_cf()
    assert list(df.index) == list(range(PROJ_LEN))
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_ptia", "claims_lapse",
        "expenses", "commissions", "net_cf", "liability_cf",
    ]
    # A cash flow statement must not publish its own subtotal beside its parts.
    assert "claims" not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    outgo = df["claims_death"] + df["claims_ptia"] + df["claims_lapse"] + df["expenses"]
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    # Within policy year 1 the monthly frame shows what the annual one could not: the
    # whole cotisation against the acquisition cost in month 0, then eleven thin negative
    # months.  Read by policy year, every year is positive.
    assert df["net_cf"].iloc[0] == pytest.approx(633.73, abs=CENT)
    assert (df["net_cf"].iloc[1:12] < 0).all()
    ann = fr_td_anchor.result_cf_annual()
    assert ann.loc[1, "net_cf"] == pytest.approx(2.58, abs=CENT)
    assert (ann["net_cf"] > 0).all()


def test_invalid_enum_values_raise(fr_td_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_td_anchor.claims(0, "SURRENDER")
    with pytest.raises(FormulaError):
        fr_td_anchor.pols_if_at(0, "AFTER_LAPSE")


def test_docstrings_describe_the_current_structure(temporaire_deces):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = temporaire_deces.doc
    assert "temporaire décès" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "revisable" in doc and "constante" in doc
    assert "acceleration" in doc
    assert "ADE_FR_S" in doc and "Obseques_FR_S" in doc   # the siblings on this chassis
    assert "Monthly steps" in doc
    assert "annual" in doc.lower()               # the two-speed structure is declared
    proj = temporaire_deces.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "proj_len_y", "policy_year", "duration", "duration_mth",
                  "model_point", "prem_pp", "prem_inst_pp", "prem_cycle", "ptia_rate",
                  "mort_rate_mth", "ptia_rate_mth", "lapse_rate_mth", "decr_rate_mth",
                  "suicide_factor", "benefit_death_pp", "lapse_cum", "pols_if_at",
                  "result_cf_annual"):
        assert cells in proj, cells
    data = temporaire_deces.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "premium_rate_table",
                  "mort_table"):
        assert cells in data, cells


def test_the_docs_state_every_timing_decision_the_conversion_had_to_take(
        temporaire_deces):
    """The decisions that were not forced are written down where a reader will meet them.

    Each of these is also asserted by a named test above; this one guards the *prose*, so
    that the arithmetic and the explanation cannot drift apart.
    """
    proj = temporaire_deces.Projection.doc
    assert "policy months" in proj
    # H1 -- the two dependent rates are converted together and split.
    assert "decr_rate_mth" in proj and "split" in proj
    # H2 -- the constante equivalence stays annual.
    assert "annual" in proj and "equivalence" in proj
    # H3 -- the final year's zero lapse covers the whole year.
    assert "whole" in proj
    # H4 -- the fractionnement is collected on the mode's cycle.
    assert "instalments" in proj
    # H5/H6 -- the two behaviour modules stay annual experience statements.
    assert "anniversary" in proj
    assert "renewal" in proj
    # H7 -- expense inflation steps by policy year.
    assert "inflation_factor" in proj
    # The reconciliation claim itself.
    assert "pols_if(12k)" in proj
    for cells in ("suicide_factor", "in_waiting", "prem_inst_pp", "sel_lapse_factor",
                  "shock_lapse_factor", "lapse_rate", "disc_factor", "pols_tariff"):
        assert cells in proj, cells


def test_the_protection_chassis_vocabulary_is_present(temporaire_deces):
    """Names ADE_FR_S and Obseques_FR_S inherit must mean the same thing on all three.

    All three now run a monthly grid, so the monthly vocabulary is part of the shared set.
    """
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_death", "pols_ptia", "pols_lapse", "mort_rate", "mort_rate_base",
        "mort_rate_mth", "ptia_rate", "ptia_rate_mth", "lapse_rate", "lapse_rate_base",
        "lapse_rate_mth", "lapse_cum", "duration", "duration_mth", "policy_year",
        "prem_rate", "prem_pp", "premiums", "benefit_pp", "benefit_death_pp",
        "benefit_ptia_pp", "suicide_factor", "claims", "claim_expenses", "commissions",
        "expenses", "inflation_factor", "net_cf", "liability_cf", "result_cf",
    }
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Six CSVs beside run.py, and each says what it is -- especially what it is not.

    The mortality table is a **[std]** proxy -- TH 00-02 / TF 00-02 are cited by name,
    never shipped -- and the anchor a substitute must preserve is the rate at age 58.  The
    tariff grid is the one real French artefact and marks its own entry cap.  Every rate
    in both is an **annual** rate; the monthly grid converts them rather than re-keying
    them, so not one input file changed in the conversion.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "premium_rate_table.csv", "mort_table.csv",
                "lapse_table.csv", "freq_loading_table.csv", "benefit_schedule.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir() if p.suffix == ".csv"}

    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col="age")
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert float(mort.loc[58, "mort_rate"]) == 0.00400
    assert float(mort.loc[59, "mort_rate"]) == pytest.approx(0.00436, rel=1e-9)
    assert mort["mort_rate"].max() <= 1.0
    assert list(mort.index) == list(range(18, 75))
    assert float(mort.loc[74, "mort_rate"]) / float(mort.loc[73, "mort_rate"]) == (
        pytest.approx(1.09, rel=1e-6))

    rates = pd.read_csv(MODEL_DIR.parent / "premium_rate_table.csv")
    assert set(rates["rate_id"]) == {"maif_2019"}
    assert all("entry grid" in p for p in rates[rates["age"] <= 65]["provenance"])
    assert all("en cours de contrat" in p for p in rates[rates["age"] > 65]["provenance"])

    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    assert list(lapse["lapse_rate"]) == [0.12, 0.10, 0.08, 0.06]
    assert all("no observed range" in p for p in lapse["provenance"])

    # The instalments column shipped with the frequency table all along; the monthly grid
    # is what gave it something to drive.
    freq = pd.read_csv(MODEL_DIR.parent / "freq_loading_table.csv", index_col="prem_freq")
    assert list(freq["instalments"]) == [1, 2, 4, 12]
    assert "12 instalments" in freq.loc["monthly", "provenance"]


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a company or licensed mortality basis."""
    import pandas as pd

    lighter = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col="age")
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="TD_FR_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_death"].sum()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Lighter mortality means fewer death claims and more premium collected.
            assert model.Projection[1].result_cf()["claims_death"].sum() < base
            assert model.Projection[1].result_cf()["premiums"].sum() > 31999.13
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="TD_FR_S_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="TD_FR_S_rt")
    try:
        p = reread.Projection[1]
        ann = p.result_cf_annual()
        for year, row in WORKED_EXAMPLE.items():
            assert ann.loc[year, "premiums"] == pytest.approx(row[3], abs=CENT)
            assert ann.loc[year, "claims_death"] == pytest.approx(row[4], abs=CENT)
            assert ann.loc[year, "net_cf"] == pytest.approx(row[7], abs=CENT)
        for t, row in MONTHS_YEAR_1.items():
            assert p.net_cf(t) == pytest.approx(row[6], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_decrement_closure() is True
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
