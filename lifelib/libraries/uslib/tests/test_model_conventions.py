"""House-style conventions every reference model in this library must satisfy.

Each model has its own test module asserting its product behaviour — the technical
notes' worked example, its recursions, its roll-forward identities. This module asserts
the things that are the *same* for all of them, parametrized over
:data:`conftest.MODELS`, so that the house style is enforced once rather than
re-litigated per model. A model registered in ``MODELS`` either conforms or fails here.

What the house style is, and why, is written up in ``products/term_life/model.md``:

* inputs are **external** CSVs beside ``run.py`` — the ``annuallife/TradLife_A`` layout,
  not ``basiclife/BasicTerm_S``'s embedded IOSpec — so the model folder holds nothing but
  formulas and a diff shows logic changes only;
* the CSV readers live in an unparameterized ``Data`` Space, so each file is read once
  per model rather than once per model point;
* every Space and every cells carries a docstring, and the ``Projection`` docstring
  carries the mapping from the technical notes' actuarial symbols to the cells names.

``Term_US_A`` also asserts several of these for itself, in more specific form (it names
its five input files, its exact read count, its own docstring phrases). That overlap is
deliberate: the checks here are the general contract, the ones there are that model's
particulars.
"""
import re

import modelx as mx
import pytest

from us_registry import MODELS, model_path

def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9).  Those caches are not part of the
    model and must not make a round-trip comparison fail for anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


ALL = sorted(MODELS)

# The vocabulary every product in the library shares, life or annuity, account-value or
# not. It is deliberately small. Names that are shared only within a family — av_pp_at
# and check_av_roll_fwd across the account-value products, lives_if across the payout
# annuities, pols_lapse wherever there is a lapse decrement — are asserted in the family's
# own test modules, because their *absence* elsewhere is a product fact rather than a
# defect: a SPIA has no premium income after outset and no lapse decrement at all.
SHARED_CELLS = {
    "model_point", "proj_len", "age", "pols_if",
    "mort_rate", "claims", "expenses", "net_cf", "result_cf",
}


# The grid suffix each model must carry, from the metadata registered in conftest.MODELS.
# lifelib's own libraries use these letters the same way: annuallife/TradLife_A is the
# annual-step model, basiclife/BasicTerm_S and savings/CashValue_SE the monthly ones.
GRID_SUFFIX = {"annual": "_A", "monthly": "_S"}


def _flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    These docstrings are hard-wrapped prose. Searching the raw text for a sentence
    fragment finds it or not depending on where the wrap fell, which makes the assertions
    below test the line breaks rather than the content.
    """
    return re.sub(r"\s+", " ", doc)


@pytest.fixture(scope="module", params=ALL)
def name(request):
    """Each registered model name in turn."""
    return request.param


@pytest.fixture(scope="module")
def model(name):
    """The model itself, read under a distinct instance name and closed afterwards."""
    m = mx.read_model(model_path(name), name=name + "_conv")
    yield m
    m.close()


# ---------------------------------------------------------------------------
# Layout — the model folder holds formulas, the parent holds data


def test_the_model_name_matches_its_folder(name, model):
    """The registry name, the folder on disk and the model's own ``_name`` agree.

    The name is the product's market short name, a country tag and a grid tag —
    ``MYGA_US_S``, ``Term_US_A`` — rather than anything derivable from the folder slug,
    because ``registered-index-linked-annuity`` spelled out is unusable and the industry
    already calls it a RILA. So the pairing lives in :data:`conftest.MODELS` and is
    asserted here instead of being recomputed.
    """
    assert model_path(name).name == name
    assert model.name.removesuffix("_conv") == name


def test_the_name_carries_the_right_grid_suffix(name):
    """``_A`` for an annual step, ``_S`` for a monthly one, per conftest's metadata.

    The letters follow lifelib: ``annuallife/TradLife_A`` is annual-step, while
    ``basiclife/BasicTerm_S`` and ``savings/CashValue_SE`` are monthly. All twelve models
    here are scalar single-model-point projections, which is the other thing lifelib's
    ``S`` denotes.
    """
    grid = MODELS[name][1]["grid"]
    assert name.endswith(GRID_SUFFIX[grid]), f"{name} is a {grid}-step model"


def test_the_name_carries_the_country_tag(name):
    """Every model in this section is U.S. and says so, ahead of the grid tag."""
    assert "_US_" in name, f"{name} does not carry the _US country tag"


def test_model_folder_holds_formulas_only(name):
    """Inputs are external: the model folder carries no data of any kind.

    No IOSpec (``_data/``), no embedded CSVs, no pickles — only the serialized formulas.
    This is the ``annuallife/TradLife_A`` layout, as opposed to ``basiclife/BasicTerm_S``,
    which stores its inputs inside the model.
    """
    folder = model_path(name)
    assert not (folder / "_data").exists()
    for pattern in ("*.pickle", "*.csv", "*.xlsx", "*.xls"):
        assert not list(folder.rglob(pattern)), f"{name}: data inside the model folder"
    assert {p.name for p in folder.iterdir() if p.is_file()} == {
        "__init__.py", "_system.json"}


def test_the_model_ships_with_its_inputs_and_a_runner(name):
    """Every model directory carries its CSVs, a run.py and a model.md beside the model."""
    parent = model_path(name).parent
    csvs = {p.name for p in parent.iterdir() if p.suffix == ".csv"}
    assert "model_point_table.csv" in csvs, f"{name}: no model point table"
    assert (parent / "run.py").is_file()
    assert (parent / "model.md").is_file()


def test_input_dir_resolves_to_the_parent(name, model):
    """``input_dir()`` is derived from where the model was read, not hard-coded.

    This is what lets the model work from any checkout location.
    """
    assert model.Data.input_dir() == model_path(name).parent


def test_every_csv_beside_the_model_is_actually_read(name, model):
    """No orphan input files: each CSV in the directory backs a filename Reference.

    A CSV nobody reads is either dead weight or a wiring bug, and both look identical
    from the outside.
    """
    parent = model_path(name).parent
    on_disk = {p.name for p in parent.iterdir() if p.suffix == ".csv"}
    referenced = {
        model.Data.refs[r] for r in model.Data.refs if isinstance(model.Data.refs[r], str)
    }
    assert on_disk <= referenced, f"{name}: unreferenced CSVs {sorted(on_disk - referenced)}"


# ---------------------------------------------------------------------------
# The Data / Projection split


def test_the_model_has_exactly_data_and_projection(model):
    assert set(model.spaces) == {"Data", "Projection"}


def test_projection_is_parameterized_by_point_id(model):
    assert model.Projection.parameters == ("point_id",)


def test_projection_shares_one_data_space(model):
    """``data`` resolves to the single Data Space from every ItemSpace."""
    ids = list(model.Data.model_point_table().index)
    assert model.Projection[ids[0]].data is model.Data
    if len(ids) > 1:
        assert model.Projection[ids[0]].data is model.Projection[ids[1]].data


def test_readers_and_filenames_belong_to_data_alone(model):
    """The CSV readers and their filename References live in Data, not Projection.

    Projection is parameterized, so a reader placed there would be re-evaluated for every
    model point. Keeping them in Data is what makes the read-once property below hold.
    """
    assert "input_dir" in model.Data.cells
    files = {r for r in model.Data.refs if r.endswith("_file")}
    assert files, f"{model.name}: Data holds no filename References"
    assert not (files & set(model.Projection.refs))
    assert "input_dir" not in model.Projection.cells


def test_inputs_are_read_once_not_once_per_model_point(name):
    """N model points must not cause N reads of each input file.

    Projection is parameterized by ``point_id``, so every ``Projection[N]`` is a separate
    ItemSpace with its own cells cache. Readers placed there would re-read every file for
    every policy; in ``Data`` they are evaluated once per model.
    """
    from collections import Counter

    import pandas as pd

    model = mx.read_model(model_path(name), name=name + "_reads")
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
    assert counts, f"{name}: no input file was read at all"
    assert all(n == 1 for n in counts.values()), counts


# ---------------------------------------------------------------------------
# Documentation


def test_every_space_is_documented(model):
    """Each Space carries a docstring, and the model docstring names every one of them.

    This is the guard against the docstrings describing a structure the model no longer
    has: adding or removing a Space without saying so in the model docstring fails here.
    """
    assert model.doc
    for space in model.spaces:
        assert model.spaces[space].doc, f"{model.name}.{space} has no docstring"
        assert space in model.doc, f"{model.name} docstring does not name Space {space}"


def test_every_cells_is_documented(model):
    """No undocumented cells anywhere in the library."""
    undocumented = [
        f"{space}.{cells}"
        for space in model.spaces
        for cells in model.spaces[space].cells
        if not model.spaces[space].cells[cells].doc
    ]
    assert not undocumented, f"{model.name}: undocumented cells {undocumented}"


def test_the_model_docstring_carries_the_house_disclaimers(model):
    """Claims a reader relies on, asserted so they cannot go stale silently."""
    doc = _flat(model.doc)
    assert "mechanics demonstration" in doc, "missing the not-a-pricing-result warning"
    assert "external" in doc, "does not say the inputs are external files"
    assert "once per model" in doc, "does not say why the Data Space exists"


def test_the_projection_docstring_carries_the_symbol_map(model):
    """Projection holds the technical notes' symbol-to-cells mapping table.

    The notes use compact actuarial symbols; the cells use lifelib names. For a reader
    holding the notes next to the model that mapping is the most useful thing in the
    file, so its absence is a defect rather than a matter of taste.
    """
    doc = _flat(model.Projection.doc)
    assert "Notes symbol" in doc
    for cells in ("proj_len", "model_point"):
        assert cells in doc, f"{cells} missing from the Projection symbol map"


def test_the_data_docstring_explains_the_input_arrangement(model):
    doc = _flat(model.Data.doc)
    assert "TradLife_A" in doc, "does not name the layout it follows"
    for cells in ("input_dir", "model_point_table"):
        assert cells in doc


# ---------------------------------------------------------------------------
# Naming


def test_the_shared_cells_names_are_present(model):
    """The vocabulary common to every product must not drift apart between models."""
    names = set(model.Projection.cells) | set(model.Projection.refs)
    assert SHARED_CELLS <= names, f"{model.name} missing: {sorted(SHARED_CELLS - names)}"


def test_cells_names_are_lower_snake_case(model):
    """lifelib names are lower snake case; a CamelCase cells is a naming slip."""
    bad = [
        f"{space}.{cells}"
        for space in model.spaces
        for cells in model.spaces[space].cells
        if not re.fullmatch(r"[a-z][a-z0-9_]*", cells)
    ]
    assert not bad, bad


# Names a cross-model review retired because they gave one concept two spellings, or one
# spelling two concepts. Each maps to the name that won and why it won. Reintroducing one
# is how the library drifts back apart, so it fails here.
RETIRED_NAMES = {
    "lapse_rate_ann": "lapse_rate (annual), with lapse_rate_mth for the monthly rate",
    "free_wd_used_pp": "wd_free_pp, the fixed-deferred-annuity chassis name",
    "free_wd_taken_pp": "wd_free_pp",
    "prem_net_pp": "prem_to_av_pp (prem_net_pp collided with WholeLife_US_A.premium_net_pp)",
    "mort_a_e_factor": "mort_ae_factor",
    "ae_factor": "mort_ae_factor",
    "omega": "omega_age",
    "check_tol": "roll_fwd_tol (it is a tolerance, not a check)",
}

RETIRED_COLUMNS = {
    "claims_surr": "claims_lapse, matching the kind argument that produces it",
    "claims_wd": "withdrawals - a withdrawal is an owner election, not a claim",
}


def test_no_retired_names(model):
    """Names the cross-model review settled against must not come back."""
    present = (set(model.Projection.cells) | set(model.Projection.refs)) & set(RETIRED_NAMES)
    assert not present, {n: f"use {RETIRED_NAMES[n]}" for n in present}


def test_lapse_rate_is_the_annual_rate(name, model):
    """``lapse_rate`` is annual and ``lapse_rate_mth`` monthly, as for mort_rate.

    Three models briefly used ``lapse_rate`` for the *monthly* rate while still spelling
    the monthly mortality rate ``mort_rate_mth``, so one model had two conventions in it.
    """
    cells = set(model.Projection.cells)
    if "lapse_rate_mth" not in cells:
        pytest.skip(f"{name} has no monthly lapse rate")
    assert "lapse_rate" in cells, "lapse_rate_mth exists without an annual lapse_rate"
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    for t in (1, 13, 25):
        if t <= proj.proj_len():
            ann, mth = proj.lapse_rate(t), proj.lapse_rate_mth(t)
            if ann > 0:
                assert mth < ann, f"t={t}: monthly {mth} not below annual {ann}"


def test_check_cells_are_no_argument_booleans(model):
    """``check_*`` takes no argument and returns a bool, as in CashValue_SE.

    A per-``t`` residual is genuinely useful when a check fails, but it lives under
    ``<name>_resid(t)`` so that one test can call the same no-arg check across the library.
    """
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    checks = [c for c in model.Projection.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    for c in checks:
        value = getattr(proj, c)()
        assert isinstance(value, bool), f"{c}() returned {type(value).__name__}, not bool"
        assert value is True, f"{c}() is False - a roll-forward identity does not close"


def test_result_cf_column_conventions(model):
    """One column vocabulary across the library, so two models can be read side by side."""
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    columns = list(proj.result_cf().columns)
    for col in columns:
        assert re.fullmatch(r"[a-z][a-z0-9_]*", col), f"{col} is not lower_snake_case"
        assert col not in RETIRED_COLUMNS, f"{col}: use {RETIRED_COLUMNS.get(col)}"
    assert columns[0] == "pols_if", f"{columns[0]!r} precedes pols_if"
    assert "net_cf" in columns


def test_net_cf_is_income_positive(model):
    """``net_cf`` carries one sign across all twelve models: income less outgo.

    Where a product's technical notes print the stream outgo-positive (whole life, and
    both payout annuities), that orientation survives verbatim as ``liability_cf`` and
    ``net_cf`` is its negative - so ``result_cf()["net_cf"]`` can be compared and summed
    across the library without checking which product it came from.
    """
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    if "liability_cf" not in model.Projection.cells:
        pytest.skip("no notes-orientation companion cells")
    df = proj.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Behaviour


def test_every_model_point_projects(model):
    """No model point may sit in the table that the input tables cannot serve.

    A model point the shipped rate tables cannot price raises deep inside a lookup, so
    without this the table quietly documents a capability the model does not have.
    """
    for point_id in model.Data.model_point_table().index:
        df = model.Projection[point_id].result_cf()
        assert len(df) > 0, f"{model.name}: model point {point_id} projects nothing"
        assert df.index.name == "t", f"{model.name}: result_cf is not indexed by t"
        assert df.notna().all().all(), f"{model.name}: NaN in point {point_id} cash flows"


def test_round_trip_is_stable(name, tmp_path):
    """read -> write -> re-read reproduces the same file set and the same numbers.

    Inputs are external, so they must travel with the model: the CSVs are copied to the
    new parent directory before re-reading. Without that the re-read model loads and then
    fails on first evaluation — which is exactly the trade-off this layout makes, and the
    reason it is worth asserting in both directions.
    """
    import shutil

    src = model_path(name)
    model = mx.read_model(src, name=name + "_rt_src")
    try:
        point_id = list(model.Data.model_point_table().index)[0]
        before = model.Projection[point_id].result_cf()
        before_doc = model.Projection.doc
        dest = tmp_path / src.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in src.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name=name + "_rt")
    try:
        after = reread.Projection[point_id].result_cf()
        assert list(after.columns) == list(before.columns)
        assert (after - before).abs().max().max() == pytest.approx(0.0, abs=1e-9)
        assert reread.Projection.doc == before_doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(src)
