"""Golden and structural tests for Term_US_S.

The golden values are the worked example in products/term_life/technical-notes.md
("Worked example"), which projects the specimen anchor cell M35 / StdNT / $100,000 /
10-year plan / annual mode on a **monthly** grid.  They are hard-coded here rather than
pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the cent, in-force to six
decimals.

The time index is 0-based and counts policy months: ``t = 0`` is the issue month, the
frame is ``t = 0 .. proj_len() - 1`` with ``proj_len() = 12 * (95 - x)``, and the notes'
two tables are the twelve months of policy year 1 (``t = 0 .. 11``) and the policy-year
aggregation of years 1-12.  The contractual policy year is
``policy_year(t) = duration(t) + 1``, ``duration(t) = t // 12``.
"""
import modelx as mx
import pytest

from us_registry import MODELS, LIB

def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9).  Those caches are not part of the
    model and must not make a round-trip comparison fail for anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-7        # in-force displayed to 6 d.p.

N = 10                # the anchor cell's level period, in years
SHOCK_MTH = 12 * N - 1        # the month the shock lapse falls in, t = 119
PROJ_LEN = 12 * (95 - 35)     # 720 months for issue age 35

# The notes' first table: the twelve months of policy year 1, t = 0 .. 11.
#   t: (pols_if, premiums, claims, commissions, expenses, premium_taxes, net_cf,
#       pols_if next)
MONTHS = {
     0: (1.000000,   140.00,   6.67, 112.00,  302.50, 2.80,   -283.97, 0.994791),
     1: (0.994791,     0.00,   6.63,   0.00,    2.49, 0.00,     -9.13, 0.989608),
     2: (0.989608,     0.00,   6.60,   0.00,    2.48, 0.00,     -9.08, 0.984453),
     3: (0.984453,     0.00,   6.57,   0.00,    2.47, 0.00,     -9.04, 0.979325),
     4: (0.979325,     0.00,   6.53,   0.00,    2.46, 0.00,     -9.00, 0.974223),
     5: (0.974223,     0.00,   6.50,   0.00,    2.46, 0.00,     -8.95, 0.969148),
     6: (0.969148,     0.00,   6.46,   0.00,    2.45, 0.00,     -8.91, 0.964099),
     7: (0.964099,     0.00,   6.43,   0.00,    2.44, 0.00,     -8.87, 0.959077),
     8: (0.959077,     0.00,   6.40,   0.00,    2.43, 0.00,     -8.83, 0.954081),
     9: (0.954081,     0.00,   6.36,   0.00,    2.42, 0.00,     -8.78, 0.949111),
    10: (0.949111,     0.00,   6.33,   0.00,    2.41, 0.00,     -8.74, 0.944167),
    11: (0.944167,     0.00,   6.30,   0.00,    2.40, 0.00,     -8.70, 0.939248),
}

# The notes' second table: the same frame summed into policy years 1-12.  `pols_if` is
# the count entering the year, l(12(k-1)), which is what the annual-step model carried on
# the same row -- and the reason those figures are unchanged from the annual goldens.
#   policy_year: (pols_if, premiums, claims, commissions, expenses, premium_taxes, net_cf)
YEARS = {
     1: (1.000000,   140.00,   77.78,  112.00,   329.42,  2.80,   -381.99),
     2: (0.939248,   131.49,   77.99,    6.57,    28.32,  2.63,     15.98),
     3: (0.891527,   124.81,   78.76,    6.24,    27.55,  2.50,      9.77),
     4: (0.855096,   119.71,   79.73,    5.99,    26.95,  2.39,      4.65),
     5: (0.820112,   114.82,   80.50,    5.74,    26.36,  2.30,     -0.08),
     6: (0.786520,   110.11,   84.92,    5.51,    25.79,  2.20,     -8.30),
     7: (0.754229,   105.59,   88.84,    5.28,    25.22,  2.11,    -15.86),
     8: (0.723191,   101.25,   92.28,    5.06,    24.67,  2.02,    -22.79),
     9: (0.693361,    97.07,   97.74,    4.85,    23.89,  1.94,    -31.36),
    10: (0.650814,    91.11,  104.13,    4.56,    23.53,  1.82,    -42.92),
    11: (0.129955,    99.29,   69.90,    1.99,     4.08,  1.99,     21.33),
    12: (0.090395,    75.03,   56.28,    1.50,     3.15,  1.50,     12.59),
}


@pytest.mark.parametrize("t", sorted(MONTHS))
def test_worked_example_month(anchor, t):
    """Every cell of the notes' first table (the months of policy year 1)."""
    pols, prem, clm, comm, exp, tax, net, pols_next = MONTHS[t]
    assert anchor.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert anchor.premiums(t) == pytest.approx(prem, abs=CENT)
    assert anchor.claims(t) == pytest.approx(clm, abs=CENT)
    assert anchor.commissions(t) == pytest.approx(comm, abs=CENT)
    assert anchor.expenses(t) == pytest.approx(exp, abs=CENT)
    assert anchor.premium_taxes(t) == pytest.approx(tax, abs=CENT)
    assert anchor.net_cf(t) == pytest.approx(net, abs=CENT)
    assert anchor.pols_if(t + 1) == pytest.approx(pols_next, abs=INFORCE)


@pytest.mark.parametrize("year", sorted(YEARS))
def test_worked_example_policy_year(anchor, year):
    """Every cell of the notes' second table, off ``result_cf_annual()``."""
    pols, prem, clm, comm, exp, tax, net = YEARS[year]
    row = anchor.result_cf_annual().loc[year]
    assert row["pols_if"] == pytest.approx(pols, abs=INFORCE)
    assert row["premiums"] == pytest.approx(prem, abs=CENT)
    assert row["claims"] == pytest.approx(clm, abs=CENT)
    assert row["commissions"] == pytest.approx(comm, abs=CENT)
    assert row["expenses"] == pytest.approx(exp, abs=CENT)
    assert row["premium_taxes"] == pytest.approx(tax, abs=CENT)
    assert row["net_cf"] == pytest.approx(net, abs=CENT)


def test_result_cf_annual_is_the_monthly_frame_summed(anchor):
    """The aggregation is the frame regrouped, not a second projection.

    ``pols_if`` is the count entering the policy year and every other column is the total
    of its twelve months, so the two tables cannot drift apart.
    """
    df, ann = anchor.result_cf(), anchor.result_cf_annual()
    assert ann.index.name == "policy_year"
    assert list(ann.index) == list(range(1, PROJ_LEN // 12 + 1))
    assert list(ann.columns) == list(df.columns)
    for year in (1, 10, 11, 60):
        rows = df.loc[12 * (year - 1):12 * year - 1]
        assert ann.loc[year, "pols_if"] == anchor.pols_if(12 * (year - 1))
        for col in df.columns:
            if col != "pols_if":
                assert ann.loc[year, col] == pytest.approx(rows[col].sum(), rel=1e-12)


def test_monthly_rates_compound_back_to_the_annual_ones(anchor):
    """q_m and w_m are the constant-force conversion of the annual rates the notes give.

    This is what makes the two grids reconcile at anniversaries, so it is asserted
    directly rather than only through its consequence.
    """
    for t in (0, 13, 100, 125, 400):
        assert 1 - (1 - anchor.mort_rate_mth(t)) ** 12 == pytest.approx(
            anchor.mort_rate(t), rel=1e-12)
        if anchor.duration(t) != N - 1:          # the shock year is not spread
            assert 1 - (1 - anchor.lapse_rate_mth(t)) ** 12 == pytest.approx(
                anchor.lapse_rate(t), rel=1e-12)
        assert anchor.mort_rate_mth(t) < anchor.mort_rate(t)


def test_in_force_at_every_anniversary_matches_the_annual_recursion(anchor):
    """l(12k) is exactly what an annual step would carry, over the whole frame.

    The annual recursion is written out here from the notes' own annual vectors rather
    than taken from a fixture, so this asserts the equivalence and not a memory of it.
    """
    expected = 1.0
    for year in range(PROJ_LEN // 12):
        t = 12 * year
        assert anchor.pols_if(t) == pytest.approx(expected, abs=1e-12), f"year {year + 1}"
        expected *= ((1 - anchor.mort_rate(t)) * (1 - anchor.conv_rate(t))
                     * (1 - anchor.lapse_rate(t)))


def test_the_shock_lapse_falls_in_one_month_and_is_not_spread(anchor):
    """The notes' single exception to the constant-force conversion.

    The final level-period policy year's annual rate *is* the shock, so eleven of its
    months carry no ordinary lapse and the twelfth carries the shock in full - the month
    immediately before the first ART premium falls due.
    """
    assert anchor.shock_lapse_rate() == 0.80
    assert anchor.lapse_rate(SHOCK_MTH) == 0.80          # the policy year's annual rate
    assert anchor.lapse_rate_mth(SHOCK_MTH) == 0.80      # in full, unspread
    for t in range(12 * (N - 1), SHOCK_MTH):
        assert anchor.lapse_rate_mth(t) == 0.0, f"ordinary lapse at t = {t}"
    assert anchor.premium_pp(SHOCK_MTH + 1) == 764.0     # the first ART premium
    assert anchor.pols_lapse(SHOCK_MTH) > 0.5 * anchor.pols_if(SHOCK_MTH)


def test_shock_lapse_collapse(anchor):
    """The notes' headline check: l(120) = l(119)(1 - q_m(119))(1 - 0.80) = 0.129955."""
    assert anchor.pols_if(SHOCK_MTH) == pytest.approx(0.649859, abs=INFORCE)
    assert (anchor.pols_if(SHOCK_MTH) * (1 - anchor.mort_rate_mth(SHOCK_MTH))
            * (1 - 0.80)) == pytest.approx(0.129955, abs=INFORCE)
    assert anchor.pols_if(SHOCK_MTH + 1) == pytest.approx(0.129955, abs=INFORCE)


def test_jump_ratio(anchor):
    """J = AP(12n)/AP(12n - 1) = 764/140, fee included in both, and mode-independent.

    Month 119 is the last month of policy year 10, carrying the last level premium;
    month 120 opens policy year 11, the first ART year.
    """
    assert anchor.premium_pp_ann(SHOCK_MTH) == 140.0
    assert anchor.premium_pp_ann(SHOCK_MTH + 1) == 764.0
    assert anchor.jump_ratio() == pytest.approx(764.0 / 140.0, rel=1e-12)


def test_premium_mode_drives_the_instalments(term_life):
    """premium_pp(t) is the instalment; premium_pp_ann(t) is the notes' AP.

    Both shipped model points are annual mode, so the premium falls in the first month of
    each policy year and nowhere else.  The modal machinery is exercised by moving the
    Reference rather than by a model point, because the specimen prices only this cell.
    """
    anchor = term_life.Projection[1]
    assert anchor.premium_mode() == "A"
    assert anchor.modal_factor() == 1.0
    assert anchor.premium_pp(0) == 140.0
    assert all(anchor.premium_pp(t) == 0.0 for t in range(1, 12))
    assert anchor.premium_pp(12) == 140.0
    assert anchor.prem_due(0) is True
    assert anchor.prem_due(1) is False
    # Three quantities stay on AP and so do not move with the mode.
    assert anchor.premium_pp_ann(5) == 140.0             # mid-year, no instalment due
    assert anchor.conv_credits(SHOCK_MTH) == 0.0         # cv is off; the base is AP
    assert anchor.expense_acq == 300.0


def test_policy_year_is_the_contractual_label(anchor):
    """policy_year(t) = duration(t) + 1 keys premium_rates.csv; t never does."""
    assert anchor.duration(0) == 0
    assert anchor.duration(11) == 0
    assert anchor.duration(12) == 1
    assert anchor.policy_year(0) == 1
    assert anchor.policy_year(SHOCK_MTH) == 10
    assert anchor.premium_pp_ann(0) == 140.0             # policy_year 1 in the CSV
    assert anchor.premium_pp_ann(PROJ_LEN - 1) == 74780.0  # policy_year 60, age 94


def test_plt_factor_formula_diverges_from_the_pinned_fixture(term_life):
    """Documented divergence: the rule gives 3.4514, the worked example pins 3.50.

    Point 1 carries plt_mort_factor_override = 3.50 so the golden table reproduces;
    point 2 is otherwise identical and leaves the override blank, taking the formula.
    Neither is "correct" - both are standardizations, and the test exists so the gap
    cannot be closed silently in either direction.
    """
    p1, p2 = term_life.Projection[1], term_life.Projection[2]
    assert p1.plt_mort_factor_init_formula() == pytest.approx(3.4514, abs=5e-5)
    assert p1.plt_mort_factor_init() == 3.50            # the pin the worked example uses
    assert p2.plt_mort_factor_init() == pytest.approx(3.4514, abs=5e-5)   # formula path
    assert p1.plt_mort_factor_init() != pytest.approx(
        p2.plt_mort_factor_init(), abs=1e-3)


def test_plt_factor_grades_to_two(anchor):
    """M(d) = max(2.0, M(1) - 0.15(d-1)); reaches the 2.00 floor at d = 11.

    d is the notes' PLT duration in policy years, d = policy_year(t) - n (d = 1 in the
    months t = 12n .. 12n + 11), not the frame index.
    """
    assert anchor.plt_mort_factor(1) == 3.50
    assert anchor.plt_mort_factor(2) == pytest.approx(3.35)
    assert anchor.plt_mort_factor(11) == pytest.approx(2.00)
    assert anchor.plt_mort_factor(12) == 2.00           # level thereafter
    assert anchor.plt_mort_factor(30) == 2.00


def test_deterioration_multiplies_the_annual_rate(anchor):
    """M(d) applies to the annual rate, before the monthly conversion.

    Converting first and multiplying after gives a different number wherever M != 1, and
    the notes' pitfall list says which order is meant.
    """
    t = SHOCK_MTH + 1                                    # first PLT month, M(1) = 3.50
    assert anchor.mort_rate(t) == pytest.approx(0.0018 * 3.50, rel=1e-12)
    assert anchor.mort_rate_mth(t) == pytest.approx(
        1 - (1 - 0.0018 * 3.50) ** (1 / 12), rel=1e-12)
    wrong = 3.50 * (1 - (1 - 0.0018) ** (1 / 12))        # convert first, multiply after
    assert anchor.mort_rate_mth(t) != pytest.approx(wrong, rel=1e-6)


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + conversions + maturities.

    `pols_maturity` is non-zero only in the final period of the frame, t = proj_len() - 1,
    where coverage ends at attained age 95.  That is not a decrement - the contract runs
    out - but without it in the identity the last month appears to lose lives with no cause.
    """
    for t in range(anchor.proj_len()):
        out = (anchor.pols_death(t) + anchor.pols_lapse(t)
               + anchor.pols_conv(t) + anchor.pols_maturity(t))
        assert anchor.pols_if(t) - anchor.pols_if(t + 1) == pytest.approx(out, abs=1e-12)


def test_maturity_is_confined_to_the_final_month(anchor):
    for t in range(anchor.proj_len() - 1):
        assert anchor.pols_maturity(t) == 0.0
    assert anchor.pols_maturity(anchor.proj_len() - 1) > 0.0


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(anchor.proj_len() + 1):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


def test_expiry_at_attained_age_95(anchor):
    """t = 719 is the last month for issue age 35; nothing survives past it.

    proj_len() counts the months projected, so the frame ends at proj_len() - 1 - the
    last month of the policy year running from attained age 94 to expiry at 95.
    """
    assert anchor.proj_len() == PROJ_LEN                 # 720 months
    assert anchor.age(0) == 35                  # age(t) = age_at_entry() + duration(t)
    assert anchor.age(11) == 35                 # still policy year 1
    assert anchor.age(12) == 36
    assert anchor.age(PROJ_LEN - 1) == 94       # the final policy year
    assert anchor.pols_if(0) == anchor.pols_if_init()
    assert anchor.pols_if(PROJ_LEN - 1) > 0.0
    assert anchor.pols_if(PROJ_LEN) == 0.0
    assert anchor.phase(PROJ_LEN - 1) == "PLT"
    assert anchor.phase(PROJ_LEN) == "EXPIRED"


def test_phase_switches_at_the_level_period_end(anchor):
    """The level period is duration 0..n-1 (policy years 1..n); PLT starts at t = 12n."""
    assert anchor.phase(0) == "LEVEL"
    assert anchor.phase(SHOCK_MTH) == "LEVEL"
    assert anchor.phase(SHOCK_MTH + 1) == "PLT"


def test_conversion_is_off_in_the_base_run(anchor):
    """The worked example sets cv = 0; the eligibility window is still modelled."""
    assert anchor.conv_rate(48) == 0.0
    assert anchor.conv_rate_mth(48) == 0.0
    assert all(anchor.conv_credits(t) == 0.0 for t in range(24))
    assert anchor.conv_elig(SHOCK_MTH) is True    # within level period, age 44 < 70
    assert anchor.conv_elig(SHOCK_MTH + 1) is False   # level period over


def test_result_cf_shape(anchor):
    """One row per month t = 0 .. proj_len() - 1; proj_len() is the row count."""
    df = anchor.result_cf()
    assert list(df.index) == list(range(anchor.proj_len()))
    assert df.index[0] == 0
    assert df.index[-1] == anchor.proj_len() - 1
    assert len(df) == anchor.proj_len()
    assert set(df.columns) == {
        "pols_if", "premiums", "claims", "commissions", "expenses",
        "premium_taxes", "conv_credits", "net_cf",
    }
    assert df.loc[0, "net_cf"] == pytest.approx(-283.97, abs=CENT)


def test_every_space_is_documented(term_life):
    """Each Space carries a docstring, and the model docstring names every one of them.

    This is the guard against the docstrings describing a structure the model no longer
    has: adding or removing a Space without saying so in the model docstring fails here.
    """
    assert term_life.doc
    for name in term_life.spaces:
        assert term_life.spaces[name].doc, f"{name} has no docstring"
        assert name in term_life.doc, f"model docstring does not mention Space {name}"


def test_model_docstring_describes_the_current_structure(term_life):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = term_life.doc
    assert "level premium term life insurance" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    # The model had one Space before Data was split out; make sure that claim is gone.
    assert "contains one Space" not in doc


def test_space_docstrings_carry_their_reference_material(term_life):
    """Projection holds the symbol mapping; Data explains the input arrangement."""
    proj = term_life.Projection.doc
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    for cells in ("pols_if", "pols_maturity", "plt_mort_factor", "premium_pp",
                  "mort_rate_mth", "lapse_rate_mth", "duration"):
        assert cells in proj
    data = term_life.Data.doc
    assert "TradLife_A" in data                  # the pattern it follows
    for cells in ("input_dir", "mort_table", "model_point_table"):
        assert cells in data


def test_cells_names_follow_basicterm_s(term_life):
    """Names shared with lifelib's basiclife/BasicTerm_S must not drift apart."""
    shared = {
        "model_point", "age_at_entry", "sex", "sum_assured", "policy_term",
        "proj_len", "age", "pols_if", "pols_if_init", "pols_death", "pols_lapse",
        "pols_maturity", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "duration", "duration_mth", "policy_year", "premiums", "claims",
        "commissions", "expenses", "expense_acq", "expense_maint",
        "inflation_rate", "inflation_factor", "net_cf", "result_cf",
    }
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_model_folder_holds_formulas_only():
    """Inputs are external: the model folder carries no data of any kind.

    No IOSpec (`_data/`), no embedded CSVs, no pickles - only the serialized
    formulas.  This is the annuallife/TradLife_A layout, as opposed to
    basiclife/BasicTerm_S, which stores its inputs inside the model.
    """
    folder = LIB / MODELS["Term_US_S"][0]
    assert not (folder / "_data").exists()
    assert not list(folder.rglob("*.pickle"))
    assert not list(folder.rglob("*.csv"))
    assert not list(folder.rglob("*.xlsx"))
    assert {p.name for p in folder.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}


def test_inputs_live_beside_the_model():
    """The five input CSVs sit in the model folder's parent directory."""
    parent = (LIB / MODELS["Term_US_S"][0]).parent
    expected = {
        "model_point_table.csv", "premium_rates.csv", "mort_table.csv",
        "class_factor_table.csv", "shock_lapse_table.csv",
    }
    assert expected <= {p.name for p in parent.iterdir() if p.is_file()}


def test_input_dir_resolves_to_the_parent(term_life):
    """input_dir() is derived from where the model was read, not hard-coded."""
    assert term_life.Data.input_dir() == (LIB / MODELS["Term_US_S"][0]).parent


def test_projection_shares_one_data_space(term_life):
    """`data` resolves to the single Data Space from every ItemSpace."""
    assert term_life.Projection[1].data is term_life.Data
    assert term_life.Projection[1].data is term_life.Projection[2].data


def test_data_holds_the_inputs_and_projection_does_not(term_life):
    """The readers and filename References belong to Data alone."""
    readers = {"input_dir", "model_point_table", "premium_rates", "mort_table",
               "class_factor_table", "shock_lapse_table"}
    files = {"model_point_file", "premium_rates_file", "mort_table_file",
             "class_factor_file", "shock_lapse_file"}
    assert readers <= set(term_life.Data.cells)
    assert files <= set(term_life.Data.refs)
    assert not (readers & set(term_life.Projection.cells))
    assert not (files & set(term_life.Projection.refs))


def test_an_input_can_be_swapped_without_touching_formulas(term_life, tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys: a licensed mortality basis
    drops in as a same-schema CSV with no formula change.

    The **annual** rate doubles exactly, because that is what the table carries; the
    month's claims do not, because ``mort_rate_mth`` is ``1 - (1 - q)^(1/12)`` and that
    is not linear in q.  Asserting both is the honest form of this check on a monthly
    grid - and it is also where a model that converted the rate at the wrong point would
    show up.
    """
    import pandas as pd

    src = (LIB / MODELS["Term_US_S"][0]).parent / "mort_table.csv"
    doubled = pd.read_csv(src, index_col="age")
    doubled["mort_rate"] = doubled["mort_rate"] * 2

    model = mx.read_model(LIB / MODELS["Term_US_S"][0], name="Term_US_S_swap")
    try:
        # Write the alternative table where this model instance will look for it.
        alt_name = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base_rate = model.Projection[1].mort_rate(0)
            base_claims = model.Projection[1].claims(0)
            model.Data.mort_table_file = alt_name      # repoint the Reference
            model.Data.clear_all()
            model.Projection.clear_all()
            proj = model.Projection[1]
            assert proj.mort_rate(0) == pytest.approx(2 * base_rate, rel=1e-12)
            assert proj.mort_rate_mth(0) == pytest.approx(
                1 - (1 - 2 * base_rate) ** (1 / 12), rel=1e-12)
            assert proj.claims(0) == pytest.approx(2 * base_claims, rel=1e-3)
            assert proj.claims(0) != pytest.approx(2 * base_claims, rel=1e-9)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    src = LIB / MODELS["Term_US_S"][0]
    model = mx.read_model(src)
    try:
        dest = tmp_path / "Term_US_S"
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model: copy the CSVs to the
    # new parent directory before re-reading.  Without this the re-read model loads
    # but fails on first evaluation - which is the trade-off this layout makes.
    for csv in src.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Term_US_S_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in MONTHS.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[6], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    written = model_files(dest)
    committed = model_files(src)
    assert written == committed
