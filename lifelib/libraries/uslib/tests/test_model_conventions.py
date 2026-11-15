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

``Term_US_S`` also asserts several of these for itself, in more specific form (it names
its five input files and its own docstring phrases). That overlap is deliberate: the
checks here are the general contract, the ones there are that model's particulars.

This module also holds the library's **only** sweep of a model over its whole model point
table. Each product module used to run a second one on its own instance of the same model,
and a model point's first evaluation is by far the most expensive thing in this suite —
modelx caches per instance, so the second sweep pays full price to assert what the first
one just asserted. ``test_every_model_point_projects`` below is therefore where the
``check_*`` cells are called and where the few product assertions that did not generalise
live, in :data:`EXTRA_POINT_ASSERTIONS`.

The module serves two families (USLIB-SEC-PLAN.md D10): the ``_S`` models, and the
``_SEC`` models derived from them, which run in force at ``t = 0`` and then compile.  Every
section but the last holds for both, and what differs between them is read from the
registry rather than assumed: the name suffix, the ``Projection`` parameter, the files
beside the model.  No test indexes ``Projection`` by hand.  The keys come from
:func:`us_registry.point_keys` and the ItemSpaces from :func:`us_registry.projection`, so a
model indexed by position (``idx``) is enumerated as correctly as one indexed by label.

The last section holds the conventions of the SEC family alone — the frame on the valuation
clock, the count timings, new business, the in-force columns, the twin identity with S,
and the registry's own consistency — parametrized over the SEC models registered.  Phase 1
registers them one product at a time, Term first.
"""
import math
import re
from collections import Counter

import modelx as mx
import pytest

from us_registry import (
    INPUT_FILES, MODELS, is_sec, meta, model_path, point_keys, projection)

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

# The letters an SEC model adds after its grid letter: E, it runs in force at t = 0, as
# basiclife/BasicTerm_SE does; C, it compiles, as basiclife/BasicTerm_SC does.  The family
# decides them and the stage does not (USLIB-SEC-PLAN.md D2): a model is _SEC from its first
# commit, while it is still at stage "E", so its name never changes when the stage does.
SEC_LETTERS = "EC"


def _flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    These docstrings are hard-wrapped prose. Searching the raw text for a sentence
    fragment finds it or not depending on where the wrap fell, which makes the assertions
    below test the line breaks rather than the content.
    """
    return re.sub(r"\s+", " ", doc)


def _points(model):
    """Each model point as ``(key, label)``, in table order.

    The key is what :func:`us_registry.point_keys` gives, and selects the ItemSpace; the
    label is the table's ``point_id``, which is what a message names and what
    :data:`CHECK_EXEMPTIONS` is keyed by.  On a ``point_id`` model the two coincide.  On an
    ``idx`` model the key is the label's position, and keying by label is what keeps an
    exemption, or a message, meaning the same point when Phase 2 changes the parameter.
    """
    return list(zip(point_keys(model), model.Data.model_point_table().index))


@pytest.fixture(scope="module", params=ALL)
def name(request):
    """Each registered model name in turn."""
    return request.param


@pytest.fixture(scope="module")
def read_log(name):
    """The path of every CSV pandas reads while this model is alive.

    ``model`` requests this fixture, and that dependency is the whole trick: it forces the
    counting window open *before* ``mx.read_model``, so the window spans the model's entire
    life and catches every read its formulas trigger, the sweep's included. A counter
    installed after the model has been warmed instead sees nothing, and
    ``test_inputs_are_read_once_not_once_per_model_point`` below then passes vacuously.

    With the window over the sweep the module already runs, the read-once check no longer
    needs an instance of its own: it used to build a second ``<name>_reads`` model and
    re-project every model point purely to count reads, which was the single most expensive
    line in all three suites.

    ``name`` is requested so the window is per model rather than per module.
    """
    import pandas as pd

    reads = []
    original = pd.read_csv

    def counting(*args, **kwargs):
        reads.append(str(args[0]).replace("\\", "/"))
        return original(*args, **kwargs)

    pd.read_csv = counting
    try:
        yield reads
    finally:
        pd.read_csv = original


@pytest.fixture(scope="module")
def model(name, read_log):
    """The model itself, read under a distinct instance name and closed afterwards.

    Read inside ``read_log``'s counting window, so that the reads it provokes are counted.
    """
    m = mx.read_model(model_path(name), name=name + "_conv")
    yield m
    m.close()


# ---------------------------------------------------------------------------
# Layout — the model folder holds formulas, the parent holds data


def test_the_model_name_matches_its_folder(name, model):
    """The registry name, the folder on disk and the model's own ``_name`` agree.

    The name is the product's market short name, a country tag and a grid tag —
    ``MYGA_US_S``, ``Term_US_S`` — rather than anything derivable from the folder slug,
    because ``registered-index-linked-annuity`` spelled out is unusable and the industry
    already calls it a RILA. So the pairing lives in :data:`conftest.MODELS` and is
    asserted here instead of being recomputed.
    """
    assert model_path(name).name == name
    assert model.name.removesuffix("_conv") == name


def test_the_name_carries_the_right_grid_suffix(name):
    """``_A`` for an annual step, ``_S`` for a monthly one, per conftest's metadata.

    The letters follow lifelib: ``annuallife/TradLife_A`` is annual-step, while
    ``basiclife/BasicTerm_S`` and ``savings/CashValue_SE`` are monthly. Every model here is
    a scalar single-model-point projection, which is the other thing lifelib's ``S``
    denotes.

    An SEC model, registered with a ``"twin"``, carries :data:`SEC_LETTERS` after the grid
    letter, so ``_SEC`` on a monthly grid; an S model must not. The suffix is the family's
    and not the stage's, so it is asserted from :func:`us_registry.is_sec` and never from
    ``"stage"``.
    """
    grid = meta(name)["grid"]
    suffix = GRID_SUFFIX[grid] + (SEC_LETTERS if is_sec(name) else "")
    family = "an SEC" if is_sec(name) else "an S"
    assert name.endswith(suffix), (
        f"{name} is {family} model on a {grid} step, so its name ends {suffix}")


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


# What an SEC model needs beside it on top of what its twin does: its own runner, notes and
# model point table (USLIB-SEC-PLAN.md D8, D9). They share the S model's directory, under
# names that cannot collide with the S files. At stage "EC" it needs mx2cy's two inputs
# too, the sample run that types its cells and the spec that sizes their caches (§6.1).
SEC_COMPANION_FILES = ("run_sec.py", "model-sec.md", "model_point_table_sec.csv")
EC_COMPANION_FILES = ("sample_sec.py", "spec_sec.py")


def test_the_model_ships_with_its_inputs_and_a_runner(name):
    """Every model directory carries its CSVs, a run.py and a model.md beside the model.

    An SEC model lives in its twin's directory, so it has those already, and needs
    :data:`SEC_COMPANION_FILES` beside them as well, and :data:`EC_COMPANION_FILES` from
    stage ``"EC"`` on.
    """
    parent = model_path(name).parent
    csvs = {p.name for p in parent.iterdir() if p.suffix == ".csv"}
    assert "model_point_table.csv" in csvs, f"{name}: no model point table"
    assert (parent / "run.py").is_file()
    assert (parent / "model.md").is_file()
    if is_sec(name):
        needed = SEC_COMPANION_FILES + (
            EC_COMPANION_FILES if meta(name).get("stage") == "EC" else ())
        missing = [f for f in needed if not (parent / f).is_file()]
        assert not missing, f"{name}: no {', '.join(missing)} beside the model"


def test_input_dir_resolves_to_the_parent(name, model):
    """``input_dir()`` is derived from where the model was read, not hard-coded.

    This is what lets the model work from any checkout location.
    """
    assert model.Data.input_dir() == model_path(name).parent


def _filenames(model):
    """The filename References of a model's ``Data``: every one whose value is a str."""
    return {value for value in model.Data.refs.values() if isinstance(value, str)}


def _siblings(name):
    """The other registered models whose folders sit in ``name``'s product directory."""
    parent = model_path(name).parent
    return [n for n in ALL if n != name and model_path(n).parent == parent]


def test_every_csv_beside_the_model_is_actually_read(name, model):
    """No orphan input files: each CSV in the directory backs a filename Reference.

    A CSV nobody reads is either dead weight or a wiring bug, and both look identical
    from the outside.

    "Nobody" is every registered model in the directory, not this one alone. An SEC model
    shares its twin's directory and reads its own ``model_point_table_sec.csv`` beside the
    S table, so each of the two models leaves a CSV the other never opens, and neither is
    an orphan. The siblings are read only for their References — none is evaluated, so the
    read-once count below sees nothing of them — and closed straight away.
    """
    parent = model_path(name).parent
    on_disk = {p.name for p in parent.iterdir() if p.suffix == ".csv"}
    referenced = _filenames(model)
    for sibling in _siblings(name):
        other = mx.read_model(model_path(sibling), name=sibling + "_sibling")
        try:
            referenced |= _filenames(other)
        finally:
            other.close()
    assert on_disk <= referenced, (
        f"{name}: CSVs no model in {parent.name}/ references "
        f"{sorted(on_disk - referenced)}")


# ---------------------------------------------------------------------------
# The Data / Projection split


def test_the_model_has_exactly_data_and_projection(model):
    assert set(model.spaces) == {"Data", "Projection"}


def test_projection_is_parameterized_as_registered(name, model):
    """``Projection`` takes the parameter the registry names, ``point_id`` by default.

    That is every S model, and every SEC model at stage ``"E"``; a compiled SEC model takes
    ``idx``, the position of the point in the ``Data`` vectors, as
    ``basiclife/BasicTerm_SC`` does. :func:`us_registry.point_keys` decides between labels
    and positions from the model itself, so this is what holds the registry to the model,
    and the other way round.
    """
    expected = meta(name).get("param", "point_id")
    assert model.Projection.parameters == (expected,), (
        f"{name}: Projection takes {model.Projection.parameters}, registered {expected!r}")


def test_projection_shares_one_data_space(model):
    """``data`` resolves to the single Data Space from every ItemSpace."""
    keys = point_keys(model)
    assert projection(model, keys[0]).data is model.Data
    if len(keys) > 1:
        assert projection(model, keys[0]).data is projection(model, keys[1]).data


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


# The read-once property this arrangement buys is asserted under *Behaviour* below, after
# the sweep whose reads it counts.


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
    "prem_net_pp": "prem_to_av_pp (prem_net_pp collided with WholeLife_US_S.premium_net_pp)",
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
    proj = projection(model, point_keys(model)[0])
    for t in (0, 12, 24):
        if t < proj.proj_len():
            ann, mth = proj.lapse_rate(t), proj.lapse_rate_mth(t)
            if ann > 0:
                assert mth < ann, f"t={t}: monthly {mth} not below annual {ann}"


# ``check_*`` takes no argument and returns a bool, as in CashValue_SE, with the per-``t``
# residual under ``<name>_resid(t)``. That contract is asserted inside the sweep under
# *Behaviour* below rather than in a test of its own: run separately it was the first test
# to touch the shared instance, and so paid a model point's cold projection to assert one
# bool.


def test_result_cf_column_conventions(model):
    """One column vocabulary across the library, so two models can be read side by side."""
    proj = projection(model, point_keys(model)[0])
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
    proj = projection(model, point_keys(model)[0])
    if "liability_cf" not in model.Projection.cells:
        pytest.skip("no notes-orientation companion cells")
    df = proj.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Behaviour


# What each product module's own sweep asserted that the generic sweep below cannot say.
#
# Twelve product modules each ran their own ``test_every_model_point_projects`` over their
# own instance of the same model. Most of what they asserted is said generically below —
# the frame is non-empty, indexed by ``t``, runs contiguously from its first row to
# ``proj_len() - 1``, is free of NaN, and every ``check_*`` closes — and a second sweep to
# re-assert it cost a full cold projection of every model point. These four are the
# residue: a payout annuity's outgo sign, a GLWB's phase vocabulary, a DIA's income actually
# starting, a VA's two per-``t`` residuals. They are keyed by model name and called with the
# ItemSpace and the frame the sweep has already computed, so the product fact survives
# without a second sweep to carry it.
#
# The row count used to sit here too, one helper per product, because ``proj_len()`` once
# meant different things in different models. It no longer does: the time index ``t`` is
# 0-based and ``proj_len()`` is the number of periods from ``t = 0``, the exclusive end of
# the frame, in every model — so the row count is asserted generically in the sweep.


def _dia_pays_an_income(proj, df):
    """DIA_US_S: the income actually starts.

    A deferred income annuity whose ``annual_income`` is zero at ``income_start_mth`` defers
    forever, which is not a contract the shipped table should be able to describe.
    """
    assert proj.annual_income(proj.income_start_mth()) > 0.0


def _dia_sec_pays_an_income(proj, df):
    """DIA_US_SEC: the income actually starts, read on the valuation clock.

    ``DIA_US_S``'s fact, with the income start month kept a policy month (R1a): the income
    in force at ``T`` is read at ``T - duration_mth_init()`` on the valuation clock, or at
    the first month on the books on a contract already past ``T``, whose income is its
    opening state, and it is positive.  It is the payout schedule's income too,
    ``annual_income_payout()``, which the refund and the commuted value read.
    """
    t = max(proj.income_start_mth() - proj.duration_mth_init(), proj.t_entry())
    assert proj.annual_income(t) > 0.0
    assert proj.annual_income(t) == proj.annual_income_payout()


def _fia_phase_is_one_of_four(proj, df):
    """FIA_US_S: every projected month sits in one of the four GLWB phases."""
    assert proj.result_glwb()["phase"].isin(
        ["ACCUM", "INCOME", "DEPLETED", "TERMINATED"]).all()


def _fia_sec_phase_is_one_of_four(proj, df):
    """FIA_US_SEC: every month in cover sits in one of the four GLWB phases.

    The frame starts at the valuation date, so a point issued after it carries its months
    before issue, which ``result_glwb()`` labels ``PRE_ISSUE``.
    """
    phase = proj.result_glwb()["phase"]
    before = phase.index < proj.t_entry()
    assert (phase[before] == "PRE_ISSUE").all()
    assert phase[~before].isin(["ACCUM", "INCOME", "DEPLETED", "TERMINATED"]).all()


def _spia_liability_is_outgo(proj, df):
    """SPIA_US_S: gross outgo, never negative.

    A payout annuity has no income after outset, so a negative ``liability_cf`` is a sign
    error rather than a thin margin.
    """
    assert df["liability_cf"].min() >= 0.0


def _va_residuals(proj, df):
    """VA_US_S: both roll-forward residuals at four sampled months.

    The ``_resid`` cells are deliberately outside the generic ``check_*`` discovery below —
    they take a ``t`` and return a float rather than a bool — so nothing else calls them.
    The months are the first period, two anniversaries and the last month of a 25-year
    frame, each guarded so a shorter model point samples what it has.
    """
    for t in (0, 60, 120, 299):
        if t < proj.proj_len():
            assert proj.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
            assert proj.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-6)


def _va_sec_residuals(proj, df):
    """VA_US_SEC: both roll-forward residuals at four sampled months, scaled by the count.

    ``VA_US_S``'s fact on the valuation clock: the months are the first projected month,
    two anniversaries of S's anchor and the last month of a 25-year frame, each guarded so
    that a shorter frame samples what it has, and each bound is the model's own,
    ``check_tol_pols`` and ``check_tol_av`` times ``max(policy_count(), 1)``, kept strict
    as S's is, so that a residual that is not a number fails.
    """
    scale = max(proj.policy_count(), 1.0)
    for t in (0, 60, 120, 299):
        if t < proj.proj_len():
            assert abs(proj.check_pols_roll_fwd_resid(t)) < proj.check_tol_pols * scale
            assert abs(proj.check_av_roll_fwd_resid(t)) < proj.check_tol_av * scale


EXTRA_POINT_ASSERTIONS = {
    "DIA_US_S": _dia_pays_an_income,
    "DIA_US_SEC": _dia_sec_pays_an_income,
    "FIA_US_S": _fia_phase_is_one_of_four,
    "FIA_US_SEC": _fia_sec_phase_is_one_of_four,
    "SPIA_US_S": _spia_liability_is_outgo,
    "SPIA_US_SEC": _spia_liability_is_outgo,
    "VA_US_S": _va_residuals,
    "VA_US_SEC": _va_sec_residuals,
}


# (model, model point) -> the ``check_*`` cells that are documented *not* to close there.
#
# The model point is its table label, ``point_id``, and never the ItemSpace key: on an
# ``idx`` model the key is a position, and an entry keyed by it would quietly move to the
# next point down when Phase 2 changes the parameter.
#
# ``IUL_US_S.check_margin()`` is defined with a stated precondition — its docstring ends
# "the identity holds while neither ``csv_pp`` nor ``ncsv_pp`` floor binds against a policy
# loan" — and model point 5 exists to break it: its loan overruns the cash value, the
# ``ncsv_pp`` floor binds, and the identity opens up by the unrecoverable debt.
# ``test_indexed_ul_us.py`` excludes point 5 from its own ``check_margin`` parametrization
# for that reason, and pins the exposure directly in
# ``test_heavy_late_life_loans_can_overrun_the_cash_value``.
#
# The exemption is registered rather than skipped, and the sweep asserts the check is
# actually ``False`` there. An exemption nobody can see is how a check quietly stops being
# run; one that has silently started passing should be deleted, and this is what says so.
CHECK_EXEMPTIONS = {
    ("IUL_US_S", 5): {"check_margin"},
}


def test_every_model_point_projects(name, model):
    """No model point may sit in the table that the input tables cannot serve.

    A model point the shipped rate tables cannot price raises deep inside a lookup, so
    without this the table quietly documents a capability the model does not have.

    This is the one place in the suite where a model is projected over its whole model point
    table, so it is also where the ``check_*`` cells are called — on every point rather than
    on the first alone — and where :data:`EXTRA_POINT_ASSERTIONS` is applied. ``notna``
    admits an infinity, so ``net_cf`` is checked for one separately; and every point must
    publish the same columns, or two rows of one model's output cannot be read together.

    Running the checks on every point rather than on the first found the one place in the
    library where a check does not close: :data:`CHECK_EXEMPTIONS` records it and why.

    The frame itself is asserted here for every point, because it is the same in every
    model. The time index ``t`` is 0-based: ``t = 0`` is the first period of a policy
    projected from issue (the issue year on an annual grid, the issue month on a monthly
    one), period ``t`` runs from time ``t`` to time ``t + 1``, and the attained age is
    ``age_at_entry + t`` on an annual grid (``age_at_entry + duration(t)``,
    ``duration(t) = t // 12``, on a monthly one). ``proj_len()`` is the number of
    periods from ``t = 0``, i.e. the exclusive end of the frame: ``result_cf()`` covers
    ``t = t_first, ..., proj_len() - 1``, where ``t_first`` is 0 for a point projected
    from issue and the elapsed periods for an in-force point (``WholeLife_US_S``'s
    ``proj_start()``). This is lifelib's own convention (``basiclife/BasicTerm_S``,
    ``savings/CashValue_SE``: ``for t in range(proj_len())``). A contractual policy year
    is the 1-based label ``t + 1`` (``duration(t) + 1`` on a monthly grid) and is
    derived, never indexed by.

    The SEC family amends that convention for itself (USLIB-SEC-PLAN.md D3). There ``t``
    counts months from the valuation date, shared by every point however old the policy,
    the months a policy has been in force are ``duration_mth(t)``, and ``t_first`` is 0 for
    every point, which the SEC section at the end of this module asserts. Everything this
    test asserts holds under both conventions, so it runs unchanged over both families.
    """
    checks = [c for c in model.Projection.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    extra = EXTRA_POINT_ASSERTIONS.get(name)
    columns = None
    for key, point_id in _points(model):
        proj = projection(model, key)
        exempt = CHECK_EXEMPTIONS.get((name, point_id), frozenset())
        df = proj.result_cf()
        assert len(df) > 0, f"{model.name}: model point {point_id} projects nothing"
        assert df.index.name == "t", f"{model.name}: result_cf is not indexed by t"
        t_first = df.index[0]
        assert t_first >= 0, f"{model.name}: point {point_id} opens at t = {t_first} < 0"
        assert list(df.index) == list(range(t_first, proj.proj_len())), (
            f"{model.name}: point {point_id} does not run contiguously from "
            f"t = {t_first} to proj_len() - 1 = {proj.proj_len() - 1}")
        assert df.index[-1] == proj.proj_len() - 1, (
            f"{model.name}: point {point_id} ends at t = {df.index[-1]}, "
            f"not proj_len() - 1 = {proj.proj_len() - 1}")
        assert df.notna().all().all(), f"{model.name}: NaN in point {point_id} cash flows"
        assert math.isfinite(df["net_cf"].sum()), (
            f"{model.name}: point {point_id} has an infinite net_cf")
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns, (
                f"{model.name}: point {point_id} publishes different columns")
        for c in checks:
            value = getattr(proj, c)()
            assert isinstance(value, bool), (
                f"{model.name} point {point_id}: {c}() returned "
                f"{type(value).__name__}, not bool")
            if c in exempt:
                assert value is False, (
                    f"{model.name} point {point_id}: {c}() now closes - the exemption in "
                    f"CHECK_EXEMPTIONS is stale and should be deleted")
                continue
            assert value is True, (
                f"{model.name} point {point_id}: {c}() is False - a roll-forward "
                f"identity does not close")
        if extra is not None:
            extra(proj, df)


def test_inputs_are_read_once_not_once_per_model_point(name, model, read_log):
    """N model points must not cause N reads of each input file.

    Projection is parameterized by ``point_id`` (by ``idx`` on a compiled SEC model), so
    every ``Projection[N]`` is a separate ItemSpace with its own cells cache. Readers placed
    there would re-read every file for every policy; in ``Data`` they are evaluated once
    per model.

    Two things make this safe to assert off the shared instance rather than off one built
    for the purpose. The sweep is repeated below, which costs nothing once
    ``test_every_model_point_projects`` has warmed this instance — and is what keeps the
    count complete when it has not, because ``-n`` can put the two tests in different
    workers. And the log is filtered to this model's own input directory, so the copies
    ``test_round_trip_is_stable`` re-reads out of ``tmp_path`` are not miscounted as second
    reads of the same file names.

    The expected file set comes from :data:`us_registry.INPUT_FILES` rather than from the
    log itself. Asserting only that whatever was read was read once is self-fulfilling: a
    file that stops being read drops out of the ``Counter`` instead of failing, and a
    shortened sweep passes with less coverage rather than louder.

    The filter is by directory, and an SEC model shares its directory with its S twin, so
    no other model may read from it while this window is open. That is why the twin
    identity reads its S model out of a copy (``twin_model``), and why
    ``test_every_csv_beside_the_model_is_actually_read`` reads its siblings without
    evaluating them. The twin identity also evaluates this model beyond the base sweep,
    and pytest 8 runs it before this test; it takes those reads back out of the log, so
    what is asserted here does not depend on the order (see the SEC section below).
    """
    for key in point_keys(model):
        projection(model, key).result_cf()

    parent = str(model_path(name).parent).replace("\\", "/")
    counts = Counter(path.rsplit("/", 1)[-1] for path in read_log
                     if path.rsplit("/", 1)[0] == parent)
    assert set(counts) == INPUT_FILES[name], (
        f"{name}: read {sorted(counts)}, registered {sorted(INPUT_FILES[name])}")
    assert all(n == 1 for n in counts.values()), counts


def test_round_trip_is_stable(name, model, tmp_path):
    """read -> write -> re-read reproduces the same file set and the same numbers.

    Inputs are external, so they must travel with the model: the CSVs are copied to the
    new parent directory before re-reading. Without that the re-read model loads and then
    fails on first evaluation — which is exactly the trade-off this layout makes, and the
    reason it is worth asserting in both directions.

    ``before`` is taken from the warm ``model`` fixture, which the sweep above has already
    projected, rather than from a third instance projected cold for the purpose. The model
    that is *written*, though, is a fresh pristine read and never the shared one:
    ``mx.write_model`` rebinds ``model.path`` to the destination, which would repoint
    ``Data.input_dir()`` at ``tmp_path`` and clear the cache of an instance every later test
    in this module shares.
    """
    import shutil

    src = model_path(name)
    key = point_keys(model)[0]
    before = projection(model, key).result_cf()
    before_doc = model.Projection.doc

    pristine = mx.read_model(src, name=name + "_rt_src")
    try:
        dest = tmp_path / src.name
        mx.write_model(pristine, str(dest), backup=False)
    finally:
        pristine.close()

    for csv in src.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name=name + "_rt")
    try:
        after = projection(reread, key).result_cf()
        assert list(after.columns) == list(before.columns)
        assert (after - before).abs().max().max() == pytest.approx(0.0, abs=1e-9)
        assert reread.Projection.doc == before_doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(src)


# ===========================================================================
# The SEC family — in force at t = 0, then compiled (USLIB-SEC-PLAN.md)
#
# Everything above holds for every registered model. What follows holds for the SEC models
# alone (D10): what a model must meet once it takes points already in force at the
# valuation date, on the valuation clock, which no S model can. Each test is parametrized
# over SEC_MODELS, the models registered with a "twin".
#
# They reach their model through the same module-scoped ``name`` and ``model`` fixtures as
# the tests above, by parametrizing ``name`` indirectly at module scope; a fixture of their
# own would pay for a second cold sweep of every SEC point. Where pytest runs them depends
# on its version, and requirements.txt admits any from 8 (both orders were checked on a
# stand-in library). pytest 9.2 groups module-scoped parameters by value, so each test runs
# after its model's generic tests, on the instance their sweep has warmed. Every earlier
# release groups them by position in their parameter list, and an SEC model's position in
# SEC_MODELS is lower than its position in ALL, so there the section runs before its
# model's generic tests and pays the cold sweep itself, on an instance that is read again
# for those tests unless they follow at once. Each test gets the right model either way,
# because pytest compares the parameter itself before it reuses a fixture. Only the
# read-once window can tell the two orders apart, and only through T1, which evaluates the
# model beyond the base sweep; T1 takes those reads back out of the log (see there).
#
# Phase 1 registers the SEC models one product at a time, Term_US_SEC first, and each meets
# this section from the commit that registers it. The conventions of stage "EC" alone —
# the typing guard, no pandas in Projection, the compiled model against modelx — are
# Phase 2's and are not here: most need a compiled build, and they are
# test_compiled_conventions.py's, which shares the session's build through
# conftest.sec_build.

SEC_MODELS = sorted(n for n in MODELS if is_sec(n))

sec_family = pytest.mark.parametrize("name", SEC_MODELS, indirect=True, scope="module")

# The columns every SEC model point table adds to the S columns it carries over (D5, D6,
# D8): BasicTerm_SE's count and policy clock, then where the generator took the row from.
# And the three kinds of row a generated table holds: the twin of an S row, an S point
# restated in force at a month d, and new business issued after the valuation date.
SEC_COLUMNS = ("policy_count", "duration_mth", "row_kind", "source_policy_id", "source_mth")
ROW_KINDS = {"twin", "derived", "future"}

# The one SEC model whose ``pols_if`` is a closing count (D5). Its registry flag,
# ``closing_pols_if``, is what makes test_pols_if_is_the_count_before_decrements skip, so
# the registry test at the end confines the flag to it: set on any other model, it would
# switch that convention off without a word.
CLOSING_POLS_IF = frozenset({"SPIA_US_SEC"})

# The one SEC model whose ``pols_if`` is the count on the books weighted by survival (D5),
# ``pols_if_at(t, "BEF_DECR") * lives_if_last(t)``. Its registry flag, ``survival_pols_if``,
# makes test_pols_if_is_the_count_before_decrements skip it as ``closing_pols_if`` skips
# SPIA, and the registry test at the end confines this flag to it in the same way.
SURVIVAL_POLS_IF = frozenset({"DIA_US_SEC"})


def _base_sweep(model):
    """``result_cf()`` and every ``check_*`` on every point: what INPUT_FILES records.

    ``tools/gen_input_files.py`` records :data:`us_registry.INPUT_FILES` from exactly this
    sweep, and ``test_every_model_point_projects`` performs it, with its assertions in
    between. On an instance that sweep has already warmed it evaluates nothing.
    """
    checks = [c for c in model.Projection.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    for key in point_keys(model):
        proj = projection(model, key)
        proj.result_cf()
        for c in checks:
            getattr(proj, c)()


def _timing(model, label):
    """The argument that selects timing ``label``: at stage ``"E"``, the string itself.

    Phase 2 turns the timing strings into int References of the same names (R9:
    ``pols_if_at(t, BEF_DECR)``, with ``BEF_NB = 0`` and ``BEF_DECR = 1`` in every SEC
    model), and this passes whichever the model defines, so the conventions below read the
    same at both stages.
    """
    value = model.Projection.refs.get(label)
    return value if isinstance(value, int) else label


@sec_family
def test_every_sec_frame_starts_at_the_valuation_date(name, model):
    """Row 0 of every SEC frame is the valuation month, however old the policy (D3).

    The generic sweep admits any first row ``t_first >= 0``, because an S model on the
    policy clock opens an in-force frame late: ``WholeLife_US_S`` at 108. An SEC model may
    not. Every frame starts at ``t = 0``, so the frames of a block line up row by row and
    sum into one, and a point issued after the valuation date carries zero rows up to its
    issue month instead of starting late.
    """
    late = {}
    for key, point_id in _points(model):
        first = projection(model, key).result_cf().index[0]
        if first != 0:
            late[point_id] = first
    assert not late, f"{name}: frames that open after t = 0, by point: {late}"


@sec_family
def test_pols_if_is_the_count_before_decrements(name, model):
    """``pols_if(t)`` is ``pols_if_at(t, "BEF_DECR")``, at every ``t`` of every frame (D5).

    The library settled ``pols_if(t)`` as the count that weights row ``t``, and this is the
    definition under which an SEC model's ``pols_if`` equals its S twin's on every
    new-business point: the count after the month's new business, before its decrements.
    BasicTerm_SE's own ``pols_if``, its ``BEF_MAT`` count, is not adopted.

    ``SPIA_US_SEC`` is registered ``closing_pols_if`` and is skipped. Its ``pols_if`` counts
    the contracts with an obligation still open at the end of the month, which differs from
    the opening count even in S. The flag would skip this test on any model it was set on,
    so ``test_the_sec_entry_agrees_with_its_twin_and_its_stage`` fails any other model that
    carries it (:data:`CLOSING_POLS_IF`).

    ``DIA_US_SEC`` is registered ``survival_pols_if`` and is skipped too. Its ``pols_if`` is
    the count on the books weighted by the probability that a covered life is alive at the
    start of the month, as ``DIA_US_S`` weights its constant count, and its own module
    asserts that definition; the registry test confines the flag to it in the same way
    (:data:`SURVIVAL_POLS_IF`).
    """
    if meta(name).get("closing_pols_if"):
        pytest.skip(f"{name}: pols_if is a closing count (USLIB-SEC-PLAN.md D5)")
    if meta(name).get("survival_pols_if"):
        pytest.skip(f"{name}: pols_if is the count on the books weighted by survival, "
                    f"pols_if_at(t, BEF_DECR) * lives_if_last(t) (USLIB-SEC-PLAN.md D5)")
    bef_decr = _timing(model, "BEF_DECR")
    bad = []
    for key, point_id in _points(model):
        proj = projection(model, key)
        for t in range(proj.proj_len()):
            pols_if, before = proj.pols_if(t), proj.pols_if_at(t, bef_decr)
            if pols_if != before:
                bad.append((point_id, t, pols_if, before))
    assert not bad, (
        f"{name}: pols_if(t) != pols_if_at(t, BEF_DECR) in {len(bad)} months; "
        f"(point, t, pols_if, BEF_DECR) first: {bad[:5]}")


@sec_family
def test_new_business_joins_the_count_before_decrements(name, model):
    """At every ``t``, ``BEF_DECR`` is ``BEF_NB`` plus that month's ``pols_new_biz`` (D5).

    ``pols_if_at(t, "BEF_NB")`` is the count carried in from ``t - 1`` (``pols_if_init()``
    at ``t = 0``), and the month's new business joins it before the month's decrements.
    There is no exception: ``closing_pols_if`` exempts SPIA from what its ``pols_if``
    means, not from how its timings add up.
    """
    bef_nb, bef_decr = _timing(model, "BEF_NB"), _timing(model, "BEF_DECR")
    bad = []
    for key, point_id in _points(model):
        proj = projection(model, key)
        for t in range(proj.proj_len()):
            before = proj.pols_if_at(t, bef_decr)
            carried, new = proj.pols_if_at(t, bef_nb), proj.pols_new_biz(t)
            if before != carried + new:
                bad.append((point_id, t, before, carried, new))
    assert not bad, (
        f"{name}: BEF_DECR != BEF_NB + pols_new_biz in {len(bad)} months; "
        f"(point, t, BEF_DECR, BEF_NB, pols_new_biz) first: {bad[:5]}")


@sec_family
def test_new_business_enters_once_at_its_policy_count(name, model):
    """Over the frame ``pols_new_biz`` sums to ``policy_count`` if issued in it, else to 0.

    ``duration_mth`` is the policy's age in months at ``t = 0`` (D4): positive in force, 0
    for a policy issued at ``t = 0``, ``-k`` for one issued ``k`` months later. A point
    enters the books once. Issued at or after the valuation date, its whole count is new
    business in its issue month; already in force, it is on the books from the start, as
    ``pols_if_init()``, and has no new business at all. Both are read from the SEC table.
    """
    table = model.Data.model_point_table()
    bad = []
    for key, point_id in _points(model):
        proj = projection(model, key)
        total = sum(proj.pols_new_biz(t) for t in range(proj.proj_len()))
        duration = table.at[point_id, "duration_mth"]
        expected = table.at[point_id, "policy_count"] if duration <= 0 else 0.0
        if not math.isclose(total, expected, rel_tol=1e-12, abs_tol=1e-12):
            bad.append((point_id, duration, total, expected))
    assert not bad, (
        f"{name}: new business over the frame is not the issued count; "
        f"(point, duration_mth, sum of pols_new_biz, expected): {bad}")


@sec_family
def test_nothing_happens_before_issue(name, model):
    """Before issue every ``result_cf`` column is zero, and no row anywhere is NaN (D4).

    A point issued ``k`` months after the valuation date still opens its frame at
    ``t = 0``, and rows ``0 .. k-1`` are the months before the policy exists. Every state
    variable is zero there, so every cash flow is, and they must be zeros rather than NaN:
    a block sums its points row by row, and one NaN would blank that row for all of them.
    """
    table = model.Data.model_point_table()
    bad = {}
    for key, point_id in _points(model):
        df = projection(model, key).result_cf()
        issue = -table.at[point_id, "duration_mth"]
        before = df[df.index < issue]
        live = [c for c in df.columns if not (before[c] == 0).all()]
        nan = [c for c in df.columns if df[c].isna().any()]
        if live or nan:
            bad[point_id] = {"nonzero before issue": live, "NaN": nan}
    assert not bad, f"{name}: by point, the columns at fault: {bad}"


@sec_family
def test_the_sec_table_carries_the_in_force_columns(name, model):
    """The SEC table has the in-force interface and every row's provenance (D5, D8).

    ``policy_count`` and ``duration_mth`` are BasicTerm_SE's two columns. ``row_kind``,
    ``source_policy_id`` and ``source_mth`` record where the generator took the row from:
    the ``"twin"`` of an S row, an S point restated in force at a month ``d``
    (``"derived"``), or new business issued after the valuation date (``"future"``). SEC
    month ``t`` corresponds to month ``t + source_mth`` of the source policy in S.
    """
    table = model.Data.model_point_table()
    missing = [c for c in SEC_COLUMNS if c not in table.columns]
    assert not missing, f"{name}: the model point table has no {missing}"
    unknown = sorted({str(k) for k in table["row_kind"] if k not in ROW_KINDS})
    assert not unknown, f"{name}: row_kind {unknown} is none of {sorted(ROW_KINDS)}"


@pytest.fixture(scope="module")
def twin_model(name, tmp_path_factory):
    """The S twin of SEC model ``name``, read out of a copy of their product directory.

    Out of a copy, because the twin reads the same CSVs from the same directory as the SEC
    model, and ``read_log`` attributes a read to a model by its directory alone. Read in
    place, the twin's reads would count against the SEC model, whose read-once assertion
    would then see ``model_point_table.csv``, which the SEC model never opens, and every
    shared table twice. Read out of ``tmp_path`` they are not counted at all, as
    ``test_round_trip_is_stable``'s are not. The copy holds the same formulas and the same
    CSVs, so it projects the same numbers; only its ``input_dir()`` differs.
    """
    import shutil

    twin = meta(name)["twin"]
    src = model_path(twin)
    dest = tmp_path_factory.mktemp(twin)
    shutil.copytree(src, dest / src.name, ignore=shutil.ignore_patterns("__pycache__"))
    for csv in src.parent.glob("*.csv"):
        shutil.copy(csv, dest / csv.name)
    m = mx.read_model(dest / src.name, name=twin + "_twin")
    yield m
    m.close()


# The cells T1 compares at an absolute floor, by SEC model, each with its reason.  Every
# other cell is held to 1e-9 relative with no absolute floor (§5.2, T1, precised at M13):
# twin_mismatches' default floor of 1e-9 passes any error in a count below 1e-9, and the
# twins of UL, VUL, ULSG, FIA and VA hold counts in force down to 1e-13.
#
# DIA_US_SEC measures the commutation exchange's residual in the guarantee's last month,
# where DIA_US_S measures it at the exercise month (DIA_US_SEC's docstring): on point 15
# the one value, -2.9e-11, a rounding about zero, sits at month 359 in SEC and at month 252
# in S, so each model's 0.0 meets the other's rounding.  It keeps the residual's own floor.
#
# RILA_US_SEC adds an option portfolio's legs by Neumaier's loop, as Python's `sum` does
# from 3.12, where RILA_US_S calls `sum`; on Python 3.11 `sum` adds left to right, so the
# account value differs in its last bits and the roll-forward residual, a rounding about
# zero near 1e-11, differs by up to 1.2e-11 (Tests run 30's 3.11 legs).  It keeps the
# residual's own floor.
TWIN_FLOORS = {
    "DIA_US_SEC": {"check_commutation_value_resid": 1e-9},
    "RILA_US_SEC": {"check_av_roll_fwd_resid": 1e-9},
}


@sec_family
def test_new_business_twins_agree_with_s_cell_by_cell(name, model, twin_model, read_log):
    """T1, the twin identity: on new business the SEC model is its S model (§5.2).

    For every SEC row that is the ``"twin"`` of an S row and issued at ``t = 0``, where the
    two clocks coincide, every cell of the S model must agree with the SEC model's at every
    argument tuple the S cell cached inside its frame in the S model's own sweep, and an S
    cell the SEC model lacks fails. The cells whose meaning SEC changes by design are
    exempt: ``sec_support.TWIN_EXEMPT_DEFAULT``, and the product's own in
    ``sec_support.SEC_SPECS``, where a cell SEC drops is named too. Through this, every S
    worked example, its intermediate cells included, becomes an SEC assertion with no golden
    restated. At stage ``"EC"`` the SEC model spells S's timings and phases as int
    References named as S's strings (R9, R10), and ``sec_support.codes`` maps the one onto
    the other, in S's arguments and in S's values; an argument SEC takes otherwise, a
    total's code for S's ``None`` or a slot for S's month, goes through the spec's
    ``twin_arg_map`` first (R12, R15).

    The identity presumes what every S table in the library holds: each S point counts one
    policy. An SEC model charges per policy issued what its S model may charge once per
    model point, as Term's acquisition (USLIB-SEC-PLAN.md §7.1), and on a point counting
    any other number the two then differ by design, in cells no exemption can drop without
    dropping most of what is compared. A product whose S model does so says it in its
    ``SecSpec`` comment, and its module asserts the count.

    The twin of an S row already in force, on the policy clock (WholeLife, FIA) or the
    projection clock (UL's point 3), is not compared here. Its SEC frame starts at the
    valuation date, so it is a splice case, which the product module asserts (T2).

    Every cell is compared to 1e-9 relative with no absolute floor, so that an error in a
    count below 1e-9, which late in a long frame is most of what is in force, fails: but
    for :data:`TWIN_FLOORS`, the cells a product names with its floor and its reason.

    At least one pair must be compared. Every S table has new-business points, so an empty
    comparison means the twins have gone missing, and a check that compares nothing is how
    coverage disappears without a failure.

    The comparison evaluates the SEC model beyond its base sweep: at every argument tuple S
    cached, and ``sec_support.sweep`` reaches those through every ``result_*`` cells, not
    ``result_cf()`` alone. It does so inside ``read_log``'s window, whose reads
    ``test_inputs_are_read_once_not_once_per_model_point`` holds to
    :data:`us_registry.INPUT_FILES`, the base sweep's set, and it runs after that test or
    before it depending on the pytest version (see the section comment). A cell only T1
    reaches that reads an input would then fail the read-once test under one pytest and
    pass it under the other, which was shown on a stand-in. So this runs the base sweep
    first, which on a warm instance evaluates nothing, and then takes whatever the
    comparison read back out of the log, and the read-once test sees the same reads in
    either order.
    """
    from sec_support import SEC_SPECS, TWIN_EXEMPT_DEFAULT, codes, sweep, twin_mismatches

    twin = meta(name)["twin"]
    spec = SEC_SPECS.get(name)
    exempt = TWIN_EXEMPT_DEFAULT | (spec.exempt if spec is not None else frozenset())
    arg_map = spec.twin_arg_map if spec is not None else None
    floors = TWIN_FLOORS.get(name, {})
    _base_sweep(model)
    mark = len(read_log)
    try:
        sec_table = model.Data.model_point_table()
        s_table = twin_model.Data.model_point_table()
        s_keys = {point_id: key for key, point_id in _points(twin_model)}
        pairs = [
            (point_id, s_keys[point_id], key)
            for key, point_id in _points(model)
            if sec_table.at[point_id, "row_kind"] == "twin"
            and sec_table.at[point_id, "duration_mth"] == 0
            and point_id in s_keys
            and s_table.at[point_id, "policy_id"] == sec_table.at[point_id, "policy_id"]
        ]
        mismatches = []
        for point_id, s_key, sec_key in pairs:
            s_proj = projection(twin_model, s_key)
            sweep(s_proj)
            sec_proj = projection(model, sec_key)
            found = twin_mismatches(s_proj, sec_proj, exempt=exempt | set(floors),
                                    arg_map=arg_map, codes=codes(sec_proj), atol=0.0)
            for cell, floor in floors.items():
                others = set(s_proj.cells) - {cell}
                found += twin_mismatches(s_proj, sec_proj, exempt=others, arg_map=arg_map,
                                         codes=codes(sec_proj), atol=floor)
            mismatches += [f"point {point_id}: {m}" for m in found]
    finally:
        del read_log[mark:]
    assert pairs, f"{name}: no SEC row is the new-business twin of a {twin} row"
    assert not mismatches, (
        f"{name} differs from {twin} in {len(mismatches)} places, first:\n  "
        + "\n  ".join(mismatches[:20]))


@sec_family
def test_the_sec_entry_agrees_with_its_twin_and_its_stage(name):
    """The registry entry is consistent with itself and with its twin (D1, D2, D10).

    The twin is a registered S model in the same product directory, whose input tables the
    SEC model reads rather than copies (D1), and the SEC model carries its name with
    :data:`SEC_LETTERS` after the grid letter. The stage is ``"E"`` or ``"EC"``, and the
    parameter follows it: ``point_id`` through Phase 1, and ``idx`` once Phase 2 has made
    the model compilable (R4). And ``closing_pols_if``, which switches the ``pols_if``
    convention off, is SPIA's alone (D5, :data:`CLOSING_POLS_IF`), as ``survival_pols_if``,
    which switches it off too, is DIA's (:data:`SURVIVAL_POLS_IF`).
    """
    entry = meta(name)
    if entry.get("closing_pols_if"):
        assert name in CLOSING_POLS_IF, (
            f"{name} is registered closing_pols_if, which skips "
            f"test_pols_if_is_the_count_before_decrements; D5 grants that to "
            f"{', '.join(sorted(CLOSING_POLS_IF))} alone")
    if entry.get("survival_pols_if"):
        assert name in SURVIVAL_POLS_IF, (
            f"{name} is registered survival_pols_if, which skips "
            f"test_pols_if_is_the_count_before_decrements; D5 grants that to "
            f"{', '.join(sorted(SURVIVAL_POLS_IF))} alone")
    twin = entry["twin"]
    assert twin in MODELS and not is_sec(twin), (
        f"{name}: its twin {twin!r} is not a registered S model")
    assert model_path(twin).parent == model_path(name).parent, (
        f"{name} is not in {twin}'s product directory, {model_path(twin).parent.name}/")
    assert name == twin + SEC_LETTERS, f"{name} is not named after its twin, {twin}"
    stage = entry.get("stage")
    assert stage in ("E", "EC"), f"{name}: stage {stage!r} is neither 'E' nor 'EC'"
    param = entry.get("param", "point_id")
    expected = {"E": "point_id", "EC": "idx"}[stage]
    assert param == expected, (
        f"{name}: param {param!r} at stage {stage!r}, which takes {expected!r}")
