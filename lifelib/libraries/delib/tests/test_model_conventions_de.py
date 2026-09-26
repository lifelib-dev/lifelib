"""House-style conventions every reference model in this library must satisfy.

Each model has its own test module asserting its product behaviour — the technical
notes' worked example, its recursions, its roll-forward identities. This module asserts
the things that are the *same* for all of them, parametrized over
:data:`de_registry.MODELS`, so that the house style is enforced once rather than
re-litigated per model. A model registered in ``MODELS`` either conforms or fails here.

What the house style is, and why, is written up in
``products/risikolebensversicherung/model.md``:

* inputs are **external** CSVs beside ``run.py`` — the ``annuallife/TradLife_A`` layout,
  not ``basiclife/BasicTerm_S``'s embedded IOSpec — so the model folder holds nothing but
  formulas and a diff shows logic changes only;
* the CSV readers live in an unparameterized ``Data`` Space, so each file is read once
  per model rather than once per model point;
* every Space and every cells carries a docstring, and the ``Projection`` docstring
  carries the mapping from the technical notes' actuarial symbols to the cells names.

This module also holds the library's **only** sweep of a model over its whole model point
table. A model point's first evaluation is by far the most expensive thing in this suite —
modelx caches per instance, so a second sweep on a second instance pays full price to
assert what the first one just asserted. :func:`test_every_model_point_projects` below is
therefore also where the ``check_*`` cells are called, on every model point rather than on
the first alone, and where the few product assertions that did not generalise live, in
:data:`EXTRA_POINT_ASSERTIONS`.

**On the time index and ``proj_len()``.** The convention is the same in every library of
this repository, and it is asserted here for every model point. The time index ``t`` is
0-based: ``t = 0`` is the first period of a policy projected from issue (the issue year
on an annual grid, the issue month on a monthly one), period ``t`` runs from time ``t``
to time ``t + 1``, and the attained age is ``age_at_entry + t`` on an annual grid
(``age_at_entry + duration(t)``, ``duration(t) = t // 12``, on a monthly one).
``proj_len()`` is the number of periods from ``t = 0``, i.e. the exclusive end of the
frame: ``result_cf()`` covers ``t = t_first, ..., proj_len() - 1``, where ``t_first`` is
0 for a point projected from issue and the elapsed periods for an in-force point. This
is lifelib's own convention (``basiclife/BasicTerm_S``, ``savings/CashValue_SE``:
``for t in range(proj_len())``). A contractual policy year is the 1-based label
``t + 1`` (``duration(t) + 1`` on a monthly grid) and is derived, never indexed by.

.. rubric:: The two rulings this library added

Every library in this repository settles a convention of its own and asserts it rather
than merely describing it. delib settled two, and both are here:

**``check_net_cf()`` is mandatory.** Every model must publish the identity that
reconstructs ``net_cf(t)`` from its cash flow statement's own published parts, and its
per-``t`` residual at ``check_net_cf_resid(t)``. frlib carried this name on five of its
nine models by convention; here it is a requirement, so that no model's headline number is
reconciled only in prose. What the identity *is* differs by product — a term cover's is
premiums less claims less expenses, a unit-linked contract's has to cross the unit /
non-unit boundary — which is why the check is per model and only its existence is
asserted here. See :func:`test_every_model_publishes_check_net_cf`.

**Every assumption CSV carries a ``provenance`` column.** The library's hard rule is that
every quantitative parameter is either source-tagged or marked ``[std]``. In the prose
that rule is enforced by review; in the input files it was, until here, enforced by habit.
:func:`test_every_assumption_csv_carries_provenance` makes it a property of the library.
``model_point_table.csv`` is the single exemption, because a model point is a
*configuration* rather than an assumption: its columns are the policy's own terms, and
tagging them row by row would tag the same fact once per policy. That exemption is the
only one.

.. rubric:: This module was checked against a library it does not govern

Before any delib model existed, this suite was run against two frlib models —
``TD_FR_S`` and ``Euro_FR_S`` — through a throwaway registry pointing at them. The result
was **50 passed, 2 skipped, 4 failed**, and all four failures were the intended
differences: the ``_DE_`` country tag, twice, and ``check_net_cf``, twice. Everything else
passed unchanged.

That is worth recording for two reasons. It shows the general contract here is the same
contract the sister libraries already meet, so a delib model that satisfies it is
conforming rather than merely self-consistent. And it shows the second ruling asks for
something already achievable: ``test_every_assumption_csv_carries_provenance`` passed on
both frlib models, because frlib's input files already carry the column by convention.
delib promotes that convention to a contract; it does not invent a new burden.
"""
import csv
import math
import re
from collections import Counter

import modelx as mx
import pytest

from de_registry import INPUT_FILES, MODELS, model_path


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


ALL = sorted(MODELS)

# The vocabulary every product in the library shares — Schicht 1, 2 or 3, biometric or
# savings, account-value or not. It is deliberately small. Names that are shared only
# within a family — av_pp_at and check_av_roll_fwd across the savings products, the
# multi-state ledgers across BU_DE_S and Pflege_DE_S, pols_lapse wherever there is a lapse
# decrement — are asserted in the family's own test modules, because their *absence*
# elsewhere is a product fact rather than a defect: a Risikolebensversicherung has no
# Deckungskapital to speak of and a Sofortrente has no premium income and no lapse
# decrement, the capital having been paid over at inception.
SHARED_CELLS = {
    "model_point", "proj_len", "age", "pols_if",
    "mort_rate", "claims", "expenses", "net_cf", "result_cf",
}


# The grid suffix each model must carry, from the metadata registered in de_registry.MODELS.
# lifelib's own libraries use these letters the same way: annuallife/TradLife_A is the
# annual-step model, basiclife/BasicTerm_S and savings/CashValue_SE the monthly ones.
GRID_SUFFIX = {"annual": "_A", "monthly": "_S"}

# The one input file that is a configuration rather than an assumption, and so is exempt
# from the provenance rule. See the module docstring.
PROVENANCE_EXEMPT = {"model_point_table.csv"}


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
def read_log(name):
    """The path of every CSV pandas reads while this model is alive.

    ``model`` requests this fixture, and that dependency is the whole trick: it forces the
    counting window open *before* ``mx.read_model``, so the window spans the model's entire
    life and catches every read its formulas trigger, the sweep's included. A counter
    installed after the model has been warmed instead sees nothing, and
    ``test_inputs_are_read_once_not_once_per_model_point`` below then passes vacuously.

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

    The name is the product's short name, a country tag and a grid tag — ``KLV_DE_S``,
    ``BU_DE_S`` — rather than anything derivable from the folder slug, because
    ``fondsgebundene_rentenversicherung`` spelled out is unusable in a model name. Where
    the German market has a settled short form the model takes it (KLV, RLV, BU); where it
    has none the short name is chosen rather than found. Either way the pairing lives in
    :data:`de_registry.MODELS` and is asserted here instead of being recomputed.
    """
    assert model_path(name).name == name
    assert model.name.removesuffix("_conv") == name


def test_the_name_carries_the_right_grid_suffix(name):
    """``_A`` for an annual step, ``_S`` for a monthly one, per the registry's metadata.

    The letters follow lifelib: ``annuallife/TradLife_A`` is annual-step, while
    ``basiclife/BasicTerm_S`` and ``savings/CashValue_SE`` are monthly. All the models
    here are scalar single-model-point projections, which is the other thing lifelib's
    ``S`` denotes.
    """
    grid = MODELS[name][1]["grid"]
    assert name.endswith(GRID_SUFFIX[grid]), f"{name} is a {grid}-step model"


def test_a_monthly_registry_entry_means_a_monthly_frame(name, model):
    """The registered grid is asserted against the frame, not only against the name.

    The suffix check above is a check on spelling: it pairs ``_S`` with the metadata row
    and would pass unchanged on a model whose frame still stepped a year at a time, which
    is exactly the state six of these models were in before they were converted. So the
    grid is asserted where it is observable, on the attained age — a shared cells every
    model publishes. Age is the right probe because its period is fixed by the contract
    rather than by the model: a policy ages a year in a year on any grid, so the number of
    periods it takes to do so *is* the grid. An ``annual`` row is asserted the other way
    round for the same reason, so the registry stays a statement about the model rather
    than a label the model is free to contradict.

    The window is twelve periods from the frame's own first one rather than from issue,
    and what it asserts is that the age steps **once** inside it. An in-force point need
    not open on an anniversary — ``BU_DE_S`` re-bases one onto the valuation month, so its
    frame is a whole number of years from issue and not from ``t = 0`` — and a check
    written on ``t % 12`` or on ``proj_len() % 12`` would read that as an annual frame.
    """
    grid = MODELS[name][1]["grid"]
    for point_id in model.Data.model_point_table().index:
        proj = model.Projection[point_id]
        t0 = proj.t_start() if "t_start" in model.Projection.cells else 0
        assert proj.proj_len() - t0 > 12, (
            f"{name} point {point_id}: the frame is {proj.proj_len() - t0} periods long, "
            "too short to read a grid off")
        ages = [proj.age(t0 + i) for i in range(13)]
        steps = sum(1 for i in range(12) if ages[i + 1] != ages[i])
        if grid == "annual":
            assert steps == 12, (
                f"{name} point {point_id}: the attained age steps {steps} times in twelve "
                "periods, so the frame is not counting years")
            continue
        assert steps == 1, (
            f"{name} point {point_id}: the attained age steps {steps} times in twelve "
            "periods; on a monthly frame it steps once, at the anniversary")
        assert ages[12] == ages[0] + 1, (
            f"{name} point {point_id}: the attained age is {ages[12]} twelve periods "
            f"after {ages[0]}, so a period here is not a month")


def test_the_name_carries_the_country_tag(name):
    """Every model in this library is Germany and says so, ahead of the grid tag."""
    assert "_DE_" in name, f"{name} does not carry the _DE country tag"


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
# The citation discipline reaches the input files — delib's second ruling


def test_every_assumption_csv_carries_provenance(name):
    """Every input CSV but the model point table has a ``provenance`` column.

    The library's hard rule is that **every quantitative parameter is either source-tagged
    or marked [std]**. In the prose that is enforced by review. In the shipped data it was,
    across the four sister libraries, enforced by habit — and habit is exactly what a table
    added in a hurry escapes. Here it is a property of the library: an assumption file
    without a per-row provenance tag fails.

    The tag is the same vocabulary the documents use — ``[S3]``, ``[R7]``, ``[REG-R21]``,
    ``[std]`` with its rationale — so a reader who wants to know where a number came from
    reads it off the row rather than hunting for the paragraph that introduced the table.

    ``model_point_table.csv`` is exempt, and is the only exemption. A model point is a
    *configuration*: its columns are one policy's own terms — issue age, sum assured,
    payment frequency — and tagging them row by row would repeat the same provenance once
    per policy while saying nothing about any assumption. Where a model point column *is*
    an assumption in disguise, the technical notes say so and the notes' own parameter
    table carries the tag.

    The column must also be populated: an empty provenance is the same defect as a missing
    one, with the paperwork done.
    """
    parent = model_path(name).parent
    for path in sorted(parent.glob("*.csv")):
        if path.name in PROVENANCE_EXEMPT:
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            header = next(reader)
            assert "provenance" in header, (
                f"{name}/{path.name}: no provenance column — every assumption file in "
                "this library says where its numbers came from")
            column = header.index("provenance")
            for row_no, row in enumerate(reader, start=2):
                if not row:
                    continue
                assert len(row) > column and row[column].strip(), (
                    f"{name}/{path.name} line {row_no}: empty provenance")


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
#
# The register is shared across all five libraries, and the reasons record where each
# collision was found — so some of them name a US, UK, Japanese or French model. That is
# provenance, not a stale reference: the name lost there, and it stays lost here.
RETIRED_NAMES = {
    # Inherited from the shared register.
    "lapse_rate_ann": "lapse_rate (annual), with lapse_rate_mth for the monthly rate",
    "free_wd_used_pp": "wd_free_pp, the fixed-deferred-annuity chassis name",
    "free_wd_taken_pp": "wd_free_pp",
    "prem_net_pp": "prem_to_av_pp (prem_net_pp collided with WholeLife_US_S.premium_net_pp)",
    "mort_a_e_factor": "mort_be_factor in this library — see mort_ae_factor below",
    "ae_factor": "mort_be_factor in this library — see mort_ae_factor below",
    "omega": "omega_age",
    "check_tol": "roll_fwd_tol (it is a tolerance, not a check)",
    "mort_ae_factor": (
        "mort_be_factor — this library adjusts a *valuation* table to a best estimate, "
        "which is not an actual-to-expected ratio; mort_ae_factor stays live in uslib for "
        "that different quantity"
    ),
    "mort_adj": "mort_be_factor (attested in neither sister library)",
    "mort_rate_table": "mort_rate_at_age for a lookup keyed by age, mort_rate_base(t) for the rate in period t",
    "mort_table_rate": "mort_rate_at_age (the word order was the only difference)",
    "mort_rate_tab": "mort_rate_at_age",
    "premium_net_pp": (
        "prem_net_level_pp — a net *level* premium is a pricing quantity that never "
        "becomes a cash flow, while WholeLife_US_S.premium_net_pp is the premium actually "
        "collected after the dividend offset; where the quantity is neither, name it for "
        "what the charge did to it — prem_after_charge_pp"
    ),
    "premium_net_at": "prem_net_level_at",
    "prem_pp_mth": "premium_mth_pp (monthly), with premium_pp for the annual amount",
    "prem_period_m": "prem_mode_months (it is a payment frequency, not a paying term)",
    "check_pols_if": "check_pols_roll_fwd, the name eleven uslib and uklib models already use",
    "check_lives_if": "check_lives_roll_fwd, matching SPIA_US_S / DIA_US_S / PA_UK_S",
    "pols_init": "pols_if_init",
    "sel_lapse_lam": "sel_lapse_lambda",
    "value_tol": "val_tol",
    "loan_bal": "loan_pp, the policy-loan balance on the savings chassis",
    "pols_expiry": (
        "pols_maturity — the count whose cover ends at the scheduled end of the contract, "
        "whether or not anything is paid for it; any payment is claims(t, 'MATURITY'). "
        "BasicTerm_S and Term_UK_S both use it that way"
    ),
    "check_cf_ledger": "check_net_cf, which this library requires of every model",
    "check_cf_ledger_resid": "check_net_cf_resid",
    # Settled in delib's own cross-model naming review.
    "laufende_verz": (
        "decl_rate — the declared laufende Verzinsung is one quantity under one "
        "definition, and KLV_DE_S, RV_DE_S and Basis_DE_S already spelled it decl_rate"
    ),
}

RETIRED_COLUMNS = {
    "claims_surr": "claims_lapse, matching the kind argument that produces it",
    "claims_wd": "withdrawals - a withdrawal is an owner election, not a claim",
    "claims_commute": "claims_commutation, matching the COMMUTATION kind that produces it",
    "claims": (
        "the claims_* split columns — a cash flow statement must not publish its own "
        "subtotal beside its parts, or the columns stop summing to net_cf without knowing "
        "which to skip. The claims(t) cells stays; only the column goes"
    ),
}


def test_no_retired_names(model):
    """Names the cross-model review settled against must not come back."""
    present = (set(model.Projection.cells) | set(model.Projection.refs)) & set(RETIRED_NAMES)
    assert not present, {n: f"use {RETIRED_NAMES[n]}" for n in present}


def test_lapse_rate_is_the_annual_rate(name, model):
    """``lapse_rate`` is annual and ``lapse_rate_mth`` monthly, as for mort_rate.

    Three frlib models briefly used ``lapse_rate`` for the *monthly* rate while still
    spelling the monthly mortality rate ``mort_rate_mth``, so one model had two conventions
    in it.
    """
    cells = set(model.Projection.cells)
    if "lapse_rate_mth" not in cells:
        pytest.skip(f"{name} has no monthly lapse rate")
    assert "lapse_rate" in cells, "lapse_rate_mth exists without an annual lapse_rate"
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    for t in (0, 12, 24):
        if t < proj.proj_len():
            ann, mth = proj.lapse_rate(t), proj.lapse_rate_mth(t)
            if ann > 0:
                assert mth < ann, f"t={t}: monthly {mth} not below annual {ann}"


def test_every_model_publishes_check_net_cf(name, model):
    """delib's first ruling: the cash flow statement reconciles, and says so in code.

    ``check_net_cf()`` reconstructs ``net_cf(t)`` from the statement's own published parts
    and returns a single bool over all ``t``; ``check_net_cf_resid(t)`` is the per-period
    residual. Requiring it of every model is what stops the headline number of a cash flow
    model from being the one quantity nothing checks.

    The *identity* is per product and is not asserted here — a Risikolebensversicherung
    reconciles premiums less claims less expenses, while a fondsgebundene
    Rentenversicherung has to cross the unit / non-unit boundary to do it, and a
    Sofortrente has no premium term at all. Each model's ``model.md`` states its identity
    in one line, and its own test module asserts that the identity is the right one. What
    generalises, and so lives here, is that the cells exists, takes no argument, returns a
    ``bool`` and has a residual companion. That it returns **True** on every model point is
    asserted in the sweep below, with the other ``check_*`` cells.
    """
    cells = model.Projection.cells
    assert "check_net_cf" in cells, (
        f"{name} does not publish check_net_cf() — every model in this library must "
        "reconcile its own cash flow statement in code, not only in prose")
    assert "check_net_cf_resid" in cells, (
        f"{name} publishes check_net_cf() with no per-t residual companion")
    assert cells["check_net_cf"].parameters == ()


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
    """``net_cf`` carries one sign across every model in the library: income less outgo.

    Where a product's technical notes print the stream outgo-positive, that orientation
    survives verbatim as ``liability_cf`` and ``net_cf`` is its negative — so
    ``result_cf()["net_cf"]`` can be compared and summed across the library without
    checking which product it came from.
    """
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    if "liability_cf" not in model.Projection.cells:
        pytest.skip("no notes-orientation companion cells")
    df = proj.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


def test_pols_if_is_the_start_of_period_count(name, model):
    """``pols_if(t)`` is the exposure at the **start** of period t, not the end of it.

    This is the first row of uslib's shared vocabulary table, which the library index
    names as the settled ruling across all five libraries: ``pols_if(t)`` is the count at
    the start of period ``t`` and is the weight on that same ``result_cf()`` row's cash
    flows, with end-of-period state reachable through ``pols_if_at(t, timing)``.

    It is asserted here because breaking it is **silent**. Three of frlib's nine models
    were first written with the notes' own end-of-period ``l(t)`` published under this
    name, so the exposure column was the correct series shifted one period while every
    cash flow beside it was weighted correctly. Nothing raised, nothing went NaN, and a
    reader dividing a cash flow by that row's ``pols_if`` to recover a per-policy amount
    got a one-period-stale answer.

    The checkable consequence is the first row. No decrement has been applied when a period
    opens, so the opening exposure is ``pols_if_init()`` exactly — at ``t = 0`` for a
    model point projected from issue, and on an in-force model point that opens partway
    through the term at whatever ``t`` the frame starts (the elapsed periods).

    A model whose ``pols_if`` is not a policy count at all — the payout products, where it
    is the probability that a payment obligation remains — is exempt **by docstring**, so
    that a model cannot acquire the exemption by being added to a list.
    """
    proj_cells = model.Projection.cells
    if "pols_if_init" not in proj_cells:
        pytest.skip(f"{name} has no pols_if_init to compare against")
    doc = _flat(proj_cells["pols_if"].doc or "")
    if "payment obligation remains" in doc:
        pytest.skip(f"{name}: pols_if is the obligation probability, not a policy count")
    for point_id in model.Data.model_point_table().index:
        p = model.Projection[point_id]
        df = p.result_cf()
        assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12), (
            f"{model.name} point {point_id}: result_cf opens at "
            f"pols_if = {df['pols_if'].iloc[0]}, not pols_if_init() = {p.pols_if_init()} - "
            "an end-of-period count published under a start-of-period name")


# ---------------------------------------------------------------------------
# Behaviour


# What a product sweep asserts that the generic sweep below cannot say.
#
# Most of what a product module would assert over its own model point table is said
# generically below — the frame spans the projection, is indexed by ``t``, ends at
# ``proj_len() - 1``, is free of NaN, publishes one column vocabulary, keeps ``pols_if``
# non-negative, and every ``check_*`` closes — and a second sweep to re-assert it costs a
# full cold projection of every model point, which is the most expensive thing in this
# suite. These are the residue: assertions that are true of one model and meaningless for
# the rest. They are keyed by model name and called with the ItemSpace and the frame the
# sweep has already computed.
EXTRA_POINT_ASSERTIONS = {}


def test_every_model_point_projects(name, model):
    """No model point may sit in the table that the input tables cannot serve.

    A model point the shipped rate tables cannot price raises deep inside a lookup, so
    without this the table quietly documents a capability the model does not have.

    This is the one place in the suite where a model is projected over its whole model point
    table, so it is also where the ``check_*`` cells are called — on every model point rather
    than on the first alone — and where :data:`EXTRA_POINT_ASSERTIONS` is applied. ``notna``
    admits an infinity, so ``net_cf`` is checked for one separately; and every point must
    publish the same columns, or two rows of one model's output cannot be read together.

    The frame rule is asserted for every point. The time index ``t`` is 0-based — ``t = 0``
    is the first period of a policy projected from issue — and ``proj_len()`` is the number
    of periods from ``t = 0``, the **exclusive** end of the frame: ``result_cf()`` covers
    ``t = t_first, ..., proj_len() - 1``, so ``index[-1] == proj_len() - 1`` and
    ``list(index) == list(range(t_first, proj_len()))``. This is lifelib's own
    ``for t in range(proj_len())``. What must *not* be asserted is where the frame *starts*,
    which is a product fact and is not even fixed per model — ``t_first`` is 0 for a point
    projected from issue and the elapsed periods for an in-force one. The frame is checked
    for **contiguity** instead, which is the property that actually matters: a gap in ``t``
    means a period was dropped, and no reading of ``proj_len()`` alone would catch it.
    """
    checks = [c for c in model.Projection.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    extra = EXTRA_POINT_ASSERTIONS.get(name)
    columns = None
    for point_id in model.Data.model_point_table().index:
        proj = model.Projection[point_id]
        df = proj.result_cf()
        assert len(df) > 0, f"{model.name}: model point {point_id} projects nothing"
        assert df.index.name == "t", f"{model.name}: result_cf is not indexed by t"
        assert df.index[0] >= 0, (
            f"{model.name}: point {point_id} starts at t = {df.index[0]}")
        assert list(df.index) == list(range(df.index[0], proj.proj_len())), (
            f"{model.name}: point {point_id} has a gap in t, or does not end at "
            f"proj_len() - 1 = {proj.proj_len() - 1}")
        assert df.index[-1] == proj.proj_len() - 1, (
            f"{model.name}: point {point_id} ends at t = {df.index[-1]} for a projection "
            f"of {proj.proj_len()} periods (the frame is t_first .. proj_len() - 1)")
        assert df.notna().all().all(), f"{model.name}: NaN in point {point_id} cash flows"
        assert math.isfinite(df["net_cf"].sum()), (
            f"{model.name}: point {point_id} has an infinite net_cf")
        assert (df["pols_if"] >= -1e-15).all(), (
            f"{model.name}: negative pols_if in point {point_id}")
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
            assert value is True, (
                f"{model.name} point {point_id}: {c}() is False - a roll-forward "
                f"identity does not close")
        if extra is not None:
            extra(proj, df)


def test_inputs_are_read_once_not_once_per_model_point(name, model, read_log):
    """N model points must not cause N reads of each input file.

    Projection is parameterized by ``point_id``, so every ``Projection[N]`` is a separate
    ItemSpace with its own cells cache. Readers placed there would re-read every file for
    every policy; in ``Data`` they are evaluated once per model.

    The expected file set comes from :data:`de_registry.INPUT_FILES` rather than from the
    log itself. Asserting only that whatever was read was read once is self-fulfilling: a
    file that stops being read drops out of the ``Counter`` instead of failing, and a
    shortened sweep passes with less coverage rather than louder. Registering the set is
    what turns "each file is read once per model" into a statement about *which* files, and
    it is what catches a table that only some model points reach — a scenario path, an
    index cap history — dropping out of the sweep unnoticed.
    """
    for point_id in model.Data.model_point_table().index:
        model.Projection[point_id].result_cf()

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

    The model that is *written* is a fresh pristine read and never the shared one:
    ``mx.write_model`` rebinds ``model.path`` to the destination, which would repoint
    ``Data.input_dir()`` at ``tmp_path`` and clear the cache of an instance every later test
    in this module shares.
    """
    import shutil

    src = model_path(name)
    point_id = list(model.Data.model_point_table().index)[0]
    before = model.Projection[point_id].result_cf()
    before_doc = model.Projection.doc

    pristine = mx.read_model(src, name=name + "_rt_src")
    try:
        dest = tmp_path / src.name
        mx.write_model(pristine, str(dest), backup=False)
    finally:
        pristine.close()

    for csv_path in src.parent.glob("*.csv"):
        shutil.copy(csv_path, tmp_path / csv_path.name)

    reread = mx.read_model(dest, name=name + "_rt")
    try:
        after = reread.Projection[point_id].result_cf()
        assert list(after.columns) == list(before.columns)
        assert (after - before).abs().max().max() == pytest.approx(0.0, abs=1e-9)
        assert reread.Projection.doc == before_doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(src)
