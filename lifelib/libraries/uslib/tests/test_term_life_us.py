"""Golden and structural tests for Term_US_A.

The golden values are the worked example in products/term_life/technical-notes.md
("Worked example"), which projects the specimen anchor cell M35 / StdNT / $100,000 /
10-year plan / annual mode.  They are hard-coded here rather than pickled so that a
reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the cent, in-force to six
decimals.
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

# t: (pols_if, premiums, claims, commissions, expenses, premium_taxes, net_cf, pols_if next)
WORKED_EXAMPLE = {
    1:  (1.000000, 140.00,  80.00, 112.00, 330.00, 2.80, -384.80, 0.939248),
    2:  (0.939248, 131.49,  79.84,   6.57,  28.74, 2.63,   13.71, 0.891527),
    3:  (0.891527, 124.81,  80.24,   6.24,  27.83, 2.50,    8.01, 0.855096),
    4:  (0.855096, 119.71,  81.23,   5.99,  27.22, 2.39,    2.88, 0.820112),
    5:  (0.820112, 114.82,  82.01,   5.74,  26.63, 2.30,   -1.86, 0.786520),
    6:  (0.786520, 110.11,  86.52,   5.51,  26.05, 2.20,  -10.16, 0.754229),
    7:  (0.754229, 105.59,  90.51,   5.28,  25.48, 2.11,  -17.79, 0.723191),
    8:  (0.723191, 101.25,  94.01,   5.06,  24.92, 2.02,  -24.78, 0.693361),
    9:  (0.693361,  97.07, 100.54,   4.85,  24.37, 1.94,  -34.63, 0.650814),
    10: (0.650814,  91.11, 104.13,   4.56,  23.33, 1.82,  -42.73, 0.129955),
    11: (0.129955,  99.29,  81.87,   1.99,   4.75, 1.99,    8.69, 0.090395),
    12: (0.090395,  75.03,  60.56,   1.50,   3.37, 1.50,    8.09, 0.076321),
}


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(anchor, t):
    """Every cell of the notes' 12-row table, to the displayed precision."""
    pols, prem, clm, comm, exp, tax, net, pols_next = WORKED_EXAMPLE[t]
    assert anchor.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert anchor.premiums(t) == pytest.approx(prem, abs=CENT)
    assert anchor.claims(t) == pytest.approx(clm, abs=CENT)
    assert anchor.commissions(t) == pytest.approx(comm, abs=CENT)
    assert anchor.expenses(t) == pytest.approx(exp, abs=CENT)
    assert anchor.premium_taxes(t) == pytest.approx(tax, abs=CENT)
    assert anchor.net_cf(t) == pytest.approx(net, abs=CENT)
    assert anchor.pols_if(t + 1) == pytest.approx(pols_next, abs=INFORCE)


def test_shock_lapse_collapse(anchor):
    """The notes' headline check: l(11) = l(10)(1-0.0016)(1-0.80) = 0.129955."""
    assert anchor.pols_if(10) * (1 - 0.0016) * (1 - 0.80) == pytest.approx(
        0.129955, abs=INFORCE)
    assert anchor.pols_if(11) == pytest.approx(0.129955, abs=INFORCE)
    assert anchor.shock_lapse_rate() == 0.80
    assert anchor.lapse_rate(10) == 0.80


def test_jump_ratio(anchor):
    """J = premium_pp(11)/premium_pp(10) = 764/140, fee included in both."""
    assert anchor.premium_pp(10) == 140.0
    assert anchor.premium_pp(11) == 764.0
    assert anchor.jump_ratio() == pytest.approx(764.0 / 140.0, rel=1e-12)


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
    """M(d) = max(2.0, M(1) - 0.15(d-1)); reaches the 2.00 floor at d = 11."""
    assert anchor.plt_mort_factor(1) == 3.50
    assert anchor.plt_mort_factor(2) == pytest.approx(3.35)
    assert anchor.plt_mort_factor(11) == pytest.approx(2.00)
    assert anchor.plt_mort_factor(12) == 2.00           # level thereafter
    assert anchor.plt_mort_factor(30) == 2.00


def test_inforce_rollforward_closes(anchor):
    """pols_if(t) - pols_if(t+1) = deaths + lapses + conversions + maturities.

    `pols_maturity` is non-zero only in the final policy year, where coverage ends at
    attained age 95.  That is not a decrement - the contract runs out - but without it
    in the identity the last year appears to lose lives with no cause.
    """
    for t in range(1, anchor.proj_len() + 1):
        out = (anchor.pols_death(t) + anchor.pols_lapse(t)
               + anchor.pols_conv(t) + anchor.pols_maturity(t))
        assert anchor.pols_if(t) - anchor.pols_if(t + 1) == pytest.approx(out, abs=1e-12)


def test_maturity_is_confined_to_the_final_year(anchor):
    for t in range(1, anchor.proj_len()):
        assert anchor.pols_maturity(t) == 0.0
    assert anchor.pols_maturity(anchor.proj_len()) > 0.0


def test_inforce_is_a_decreasing_probability(anchor):
    for t in range(1, anchor.proj_len() + 2):
        assert 0.0 <= anchor.pols_if(t) <= 1.0
        assert anchor.pols_if(t + 1) <= anchor.pols_if(t) + 1e-15


def test_expiry_at_attained_age_95(anchor):
    """Policy year 60 is the last for issue age 35; nothing survives past it."""
    assert anchor.proj_len() == 60
    assert anchor.age(60) == 94                 # age at the start of the final year
    assert anchor.pols_if(60) > 0.0
    assert anchor.pols_if(61) == 0.0
    assert anchor.phase(61) == "EXPIRED"


def test_phase_switches_at_the_level_period_end(anchor):
    assert anchor.phase(10) == "LEVEL"
    assert anchor.phase(11) == "PLT"


def test_conversion_is_off_in_the_base_run(anchor):
    """The worked example sets cv = 0; the eligibility window is still modelled."""
    assert anchor.conv_rate(5) == 0.0
    assert all(anchor.conv_credits(t) == 0.0 for t in range(1, 13))
    assert anchor.conv_elig(10) is True          # within level period, age 44 < 70
    assert anchor.conv_elig(11) is False         # level period over


def test_result_cf_shape(anchor):
    df = anchor.result_cf()
    assert list(df.index) == list(range(1, anchor.proj_len() + 1))
    assert set(df.columns) == {
        "pols_if", "premiums", "claims", "commissions", "expenses",
        "premium_taxes", "conv_credits", "net_cf",
    }
    assert df.loc[1, "net_cf"] == pytest.approx(-384.80, abs=CENT)


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
    for cells in ("pols_if", "pols_maturity", "plt_mort_factor", "premium_pp"):
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
        "pols_maturity", "mort_rate", "lapse_rate", "premiums", "claims",
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
    folder = LIB / MODELS["Term_US_A"][0]
    assert not (folder / "_data").exists()
    assert not list(folder.rglob("*.pickle"))
    assert not list(folder.rglob("*.csv"))
    assert not list(folder.rglob("*.xlsx"))
    assert {p.name for p in folder.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}


def test_inputs_live_beside_the_model():
    """The five input CSVs sit in the model folder's parent directory."""
    parent = (LIB / MODELS["Term_US_A"][0]).parent
    expected = {
        "model_point_table.csv", "premium_rates.csv", "mort_table.csv",
        "class_factor_table.csv", "shock_lapse_table.csv",
    }
    assert expected <= {p.name for p in parent.iterdir() if p.is_file()}


def test_input_dir_resolves_to_the_parent(term_life):
    """input_dir() is derived from where the model was read, not hard-coded."""
    assert term_life.Data.input_dir() == (LIB / MODELS["Term_US_A"][0]).parent


def test_inputs_are_read_once_not_once_per_model_point(term_life):
    """The readers live in Data, so N model points do not cause N reads.

    Projection is parameterized by point_id, so every Projection[N] is a separate
    ItemSpace with its own cells cache.  Readers placed there would re-read every file
    for every policy; in Data they are evaluated once per model.
    """
    import pandas as pd
    from collections import Counter

    model = mx.read_model(LIB / MODELS["Term_US_A"][0], name="Term_US_A_reads")
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
    assert len(reads) == 5           # one per input file, regardless of point count


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


def test_every_model_point_projects(term_life):
    """No model point may sit in the table that the input tables cannot serve.

    Model point 3 (T20 / F / PNT) was removed for exactly this reason: the specimen
    gives a guaranteed premium scale for the anchor configuration only, so that point
    raised a KeyError on the premium lookup.
    """
    for point_id in term_life.Data.model_point_table().index:
        df = term_life.Projection[point_id].result_cf()
        assert len(df) > 0


def test_an_input_can_be_swapped_without_touching_formulas(term_life, tmp_path):
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys: a licensed mortality basis
    drops in as a same-schema CSV with no formula change.
    """
    import pandas as pd

    src = (LIB / MODELS["Term_US_A"][0]).parent / "mort_table.csv"
    doubled = pd.read_csv(src, index_col="age")
    doubled["mort_rate"] = doubled["mort_rate"] * 2

    model = mx.read_model(LIB / MODELS["Term_US_A"][0], name="Term_US_A_swap")
    try:
        # Write the alternative table where this model instance will look for it.
        alt_name = "mort_table_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].claims(1)
            model.Data.mort_table_file = alt_name      # repoint the Reference
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].claims(1) == pytest.approx(2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    src = LIB / MODELS["Term_US_A"][0]
    model = mx.read_model(src)
    try:
        dest = tmp_path / "Term_US_A"
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model: copy the CSVs to the
    # new parent directory before re-reading.  Without this the re-read model loads
    # but fails on first evaluation - which is the trade-off this layout makes.
    for csv in src.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="Term_US_A_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.net_cf(t) == pytest.approx(row[6], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    written = model_files(dest)
    committed = model_files(src)
    assert written == committed
