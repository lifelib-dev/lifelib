"""House-style conventions every reference model in this library must satisfy.

Each model has its own test module asserting its product behaviour — the technical
notes' worked example, its recursions, its roll-forward identities. This module asserts
the things that are the *same* for all of them, parametrized over
:data:`conftest.MODELS`, so that the house style is enforced once rather than
re-litigated per model. A model registered in ``MODELS`` either conforms or fails here.

What the house style is, and why, is written up in
``products/temporaire_deces/model.md``:

* inputs are **external** CSVs beside ``run.py`` — the ``annuallife/TradLife_A`` layout,
  not ``basiclife/BasicTerm_S``'s embedded IOSpec — so the model folder holds nothing but
  formulas and a diff shows logic changes only;
* the CSV readers live in an unparameterized ``Data`` Space, so each file is read once
  per model rather than once per model point;
* every Space and every cells carries a docstring, and the ``Projection`` docstring
  carries the mapping from the technical notes' actuarial symbols to the cells names.

``TD_FR_S`` also asserts several of these for itself, in more specific form (it names its
own input files, its own docstring phrases). That overlap is deliberate: the checks here
are the general contract, the ones there are that model's particulars.

This module also holds the library's **only** sweep of a model over its whole model point
table. A model point's first evaluation is by far the most expensive thing in this suite —
modelx caches per instance, so a second sweep on a second instance pays full price to
assert what the first one just asserted. ``test_every_model_point_projects`` below is
therefore also where the ``check_*`` cells are called, on every model point rather than on
the first alone, and where the few product assertions that did not generalise live, in
:data:`EXTRA_POINT_ASSERTIONS`.

**On the time index and ``proj_len()``.** The time index ``t`` is 0-based: ``t = 0`` is
the first period of a policy projected from issue (the issue year on an annual grid, the
issue month on a monthly one), period ``t`` runs from time ``t`` to time ``t + 1``, and
the attained age is ``age_at_entry + t`` on an annual grid
(``age_at_entry + duration(t)``, ``duration(t) = t // 12``, on a monthly one).
``proj_len()`` is the number of periods from ``t = 0``, i.e. the exclusive end of the
frame: ``result_cf()`` covers ``t = t_first, ..., proj_len() - 1``, where ``t_first`` is
0 for a point projected from issue and the elapsed periods for an in-force point. This
is lifelib's own convention (``basiclife/BasicTerm_S``, ``savings/CashValue_SE``:
``for t in range(proj_len())``). A contractual policy year is the 1-based label
``t + 1`` (``duration(t) + 1`` on a monthly grid) and is derived, never indexed by. The
same convention holds in every sister library, and the sweep below asserts it for every
model point of every model in the registry.
"""
import math
import re
from collections import Counter

import modelx as mx
import pytest

from fr_registry import INPUT_FILES, MODELS, model_path

def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is now routine: the autodoc API pages read the cells docstrings by importing
    ``Projection`` and ``Data`` (USLIB-MERGE-PLAN.md D9, a house decision per D8).  Those caches are not part of the
    model and must not make a round-trip comparison fail for anyone who has built the docs.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


ALL = sorted(MODELS)

# The vocabulary every product in the library shares — épargne or retraite or prévoyance,
# account-value or not. It is deliberately small. Names that are shared only within a
# family — av_pp_at and check_av_roll_fwd across the épargne products, the multi-state
# ledgers across ADE_FR_S and Dep_FR_S, pols_lapse wherever there is a lapse decrement —
# are asserted in the family's own test modules, because their *absence* elsewhere is a
# product fact rather than a defect: a temporaire décès is fonds perdu and has no account
# value at all, and a rente viagère has no premium income and no lapse decrement, the
# capital having been aliéné at conversion.
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
    line in every one of the country libraries' suites.

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

    The name is the product's short name, a country tag and a grid tag — ``ADE_FR_S``,
    ``Euro_FR_S`` — rather than anything derivable from the folder slug, because
    ``assurance_emprunteur`` spelled out is unusable in a model name. Where the French
    market has a settled short form the model takes it (UC, PER, ADE, EC); where it has
    none the short name is chosen rather than found. Either way the pairing lives in
    :data:`fr_registry.MODELS` and is asserted here instead of being recomputed.
    """
    assert model_path(name).name == name
    assert model.name.removesuffix("_conv") == name


def test_the_name_carries_the_right_grid_suffix(name):
    """``_A`` for an annual step, ``_S`` for a monthly one, per conftest's metadata.

    The letters follow lifelib: ``annuallife/TradLife_A`` is annual-step, while
    ``basiclife/BasicTerm_S`` and ``savings/CashValue_SE`` are monthly. All the models
    here are scalar single-model-point projections, which is the other thing lifelib's
    ``S`` denotes.
    """
    grid = MODELS[name][1]["grid"]
    assert name.endswith(GRID_SUFFIX[grid]), f"{name} is a {grid}-step model"


def test_the_name_carries_the_country_tag(name):
    """Every model in this library is France and says so, ahead of the grid tag."""
    assert "_FR_" in name, f"{name} does not carry the _FR country tag"


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
# The register is shared across the country libraries, and the reasons record where each
# collision was found — so some of them name a US, UK or Japanese model. That is
# provenance, not a stale reference: the name lost there, and it stays lost here.
#
# frlib added none of its own. It did not need to: two of the inherited entries fired
# against the nine models as they were first written — EC_FR_S had reintroduced
# premium_net_pp and Rente_FR_S mort_rate_table — which is the register earning its keep
# rather than merely recording history. Neither of the names the register offered fitted
# EC_FR_S's quantity, a versement net of the entry charge and a real cash flow rather than
# a pricing one, so it is spelled prem_after_charge_pp; the rule the register enforces is
# that the retired spelling stays retired, not that a replacement must already exist.
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
    # Settled by the jplib cross-model review. Every one of these was a real collision
    # found across the nine models, not a matter of taste: one concept under two names, or
    # one name over two concepts.
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
        "collected after the dividend offset; where the quantity is neither, as in "
        "EC_FR_S, name it for what the charge did to it — prem_after_charge_pp"
    ),
    "premium_net_at": "prem_net_level_at",
    "prem_pp_mth": "premium_mth_pp (monthly), with premium_pp for the annual amount",
    "prem_period_m": "prem_mode_months (it is a payment frequency, not a paying term)",
    "check_pols_if": "check_pols_roll_fwd, the name eleven uslib and uklib models already use",
    "check_lives_if": "check_lives_roll_fwd, matching SPIA_US_S / DIA_US_S / PA_UK_S",
    "pols_init": "pols_if_init",
    "sel_lapse_lam": "sel_lapse_lambda",
    "value_tol": "val_tol",
    "loan_bal": "loan_pp, the 契約者貸付 balance on the savings chassis",
    "pols_expiry": (
        "pols_maturity — the count whose cover ends at the scheduled end of the contract, "
        "whether or not anything is paid for it; any payment is claims(t, 'MATURITY'). "
        "BasicTerm_S and Term_UK_S both use it that way"
    ),
    "check_cf_ledger": "check_net_cf, the spelling five of the nine already used",
    "check_cf_ledger_resid": "check_net_cf_resid",
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

    Three models briefly used ``lapse_rate`` for the *monthly* rate while still spelling
    the monthly mortality rate ``mort_rate_mth``, so one model had two conventions in it.
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


# ``check_*`` takes no argument and returns a bool, as in CashValue_SE, with the per-``t``
# residual under ``<name>_resid(t)``. That contract is asserted inside the sweep under
# *Behaviour* below rather than in a test of its own: run separately it was the first test
# to touch the shared instance, and so paid a model point's cold projection to assert one
# bool. *Which* checks each model must publish is a product fact and stays in the product
# module, because generic discovery cannot notice a check that has disappeared.


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
    survives verbatim as ``liability_cf`` and
    ``net_cf`` is its negative - so ``result_cf()["net_cf"]`` can be compared and summed
    across the library without checking which product it came from.
    """
    proj = model.Projection[list(model.Data.model_point_table().index)[0]]
    if "liability_cf" not in model.Projection.cells:
        pytest.skip("no notes-orientation companion cells")
    df = proj.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)


def test_pols_if_is_the_start_of_period_count(name, model):
    """``pols_if(t)`` is the exposure at the **start** of period t, not the end of it.

    This is the in-force row of uslib's shared vocabulary table, which the library index
    names as the settled ruling across the country libraries: ``pols_if(t)`` is the count at
    the start of period ``t`` and is the weight on that same ``result_cf()`` row's cash
    flows, with end-of-period state reachable through ``pols_if_at(t, timing)``.

    It is asserted here because breaking it is **silent**. Three of the nine models were
    first written with the notes' own end-of-period ``l(t)`` published under this name, so
    the exposure column was the correct series shifted one period while every cash flow
    beside it was weighted correctly. Nothing raised, nothing went NaN, and a reader
    dividing a cash flow by that row's ``pols_if`` to recover a per-policy amount got a
    one-period-stale answer. The rest of this module could not catch it: it asserts only
    that the column exists, comes first and stays non-negative.

    The checkable consequence is the first row. No decrement has been applied when a period
    opens, so the opening exposure is ``pols_if_init()`` exactly: at ``t = 0`` for a model
    point projected from issue, and on an in-force model point that opens partway through
    the term at ``t_first``, the elapsed periods, wherever the frame starts. The time index
    is 0-based in every model of the library, so there is no per-model reading of "the
    first row" to consult; ``t = 0`` is the first projected period, never an issue-instant
    state (the issue instant is not a row — its flows are the beginning-of-period flows of
    period 0, and the state after them is period 0's opening timing).

    **What this cannot catch, stated rather than glossed.** A model that published an
    outset state as its first row rather than a projected period would open at
    ``pols_if_init()`` under *either* reading, so the check would pass on a model that has
    the defect; ``EC_FR_S`` was once exactly that case and had to be found by reading the
    docstrings instead, and it is the sweep's frame assertions — ``t = 0`` is period 0 and
    ``pols_if(0)`` is its opening count — together with each model's docstrings that rule
    it out now. A test that identified the exposure weighting itself would need to know
    which cells carries the weight, which is a product fact. So this asserts the part that
    generalises, and the docstrings carry the rest.

    ``Rente_FR_S`` is exempt and says so in its own docstring: there ``pols_if`` is the
    notes' ``IF(t)``, the probability that *any* payment obligation remains, which is a
    different quantity carrying the same name for the same reason ``PA_UK_S`` does — it is
    what the rest of the library calls the expense weight. The exemption is by docstring
    rather than by model name so that a model cannot acquire it by being added to a list.
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
#
# This table stays inside frlib because its entries are product facts of French models,
# not because the frame is read differently elsewhere: the 0-based time index and the
# exclusive ``proj_len()`` are the same in every library.


def _ade_cover_may_end_before_the_loan(proj, df):
    """ADE_FR_S: the guarantees have their own age limits, so cover can end first.

    A cover that ends before the loan does is a real feature of assurance emprunteur and
    the reason the age limits are per guarantee rather than per contract. It is asserted
    here rather than in the product module because it is a statement about the *frame* —
    the projection must still run to the end of the loan after the last guarantee has
    lapsed, publishing zeros, rather than stopping short. With months ``0, 1, ...``, the
    last month of a loan of ``n`` months is ``t = n - 1``.
    """
    assert (df["pols_if"] >= 0.0).all()
    assert df.index[-1] == proj.loan_term_months() - 1, (
        "the projection must run to the end of the loan, not to the last cover")


def _euro_opens_on_the_whole_policy(proj, df):
    """Euro_FR_S: the frame opens with the whole policy in force."""
    assert (df["pols_if"] >= 0.0).all()
    assert df["pols_if"].iloc[0] == pytest.approx(proj.pols_if_init())


EXTRA_POINT_ASSERTIONS = {
    "ADE_FR_S": _ade_cover_may_end_before_the_loan,
    "Euro_FR_S": _euro_opens_on_the_whole_policy,
}


def test_every_model_point_projects(name, model):
    """No model point may sit in the table that the input tables cannot serve.

    A model point the shipped rate tables cannot price raises deep inside a lookup, so
    without this the table quietly documents a capability the model does not have.

    This is the one place in the suite where a model is projected over its whole model point
    table, so it is also where the ``check_*`` cells are called — on every model point rather
    than on the first alone — and where :data:`EXTRA_POINT_ASSERTIONS` is applied. ``notna``
    admits an infinity, so ``net_cf`` is checked for one separately; and every point must
    publish the same columns, or two rows of one model's output cannot be read together.

    The frame rule asserted for every point is the library-wide one: the time index ``t``
    is 0-based, ``proj_len()`` is the number of periods from ``t = 0`` — the exclusive end
    of the frame, lifelib's ``for t in range(proj_len())`` — so ``result_cf()`` covers
    ``t = t_first, ..., proj_len() - 1`` and its last index is ``proj_len() - 1``. Where the
    frame *starts* is not pinned to 0, because it is not fixed per model: ``t_first`` is 0
    for a point projected from issue and the elapsed periods for an in-force point —
    ``EC_FR_S``'s in-force model points open partway through the term, at the duration the
    policy has already run. The frame is checked for **contiguity** from ``t_first`` to the
    exclusive end, which is the property that actually matters — a gap in ``t`` means a
    period was dropped, and neither end of the frame would reveal it.
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
            f"{model.name}: point {point_id} is not the contiguous frame "
            f"t = {df.index[0]}, ..., proj_len() - 1 = {proj.proj_len() - 1}")
        assert df.index[-1] == proj.proj_len() - 1, (
            f"{model.name}: point {point_id} ends at t = {df.index[-1]} for a projection "
            f"of {proj.proj_len()} periods (the last index is proj_len() - 1)")
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

    Two things make this safe to assert off the shared instance rather than off one built
    for the purpose. The sweep is repeated below, which costs nothing once
    ``test_every_model_point_projects`` has warmed this instance — and is what keeps the
    count complete when it has not, because ``-n`` can put the two tests in different
    workers. And the log is filtered to this model's own input directory, so the copies
    ``test_round_trip_is_stable`` re-reads out of ``tmp_path`` are not miscounted as second
    reads of the same file names.

    The expected file set comes from :data:`fr_registry.INPUT_FILES` rather than from the
    log itself. Asserting only that whatever was read was read once is self-fulfilling: a
    file that stops being read drops out of the ``Counter`` instead of failing, and a
    shortened sweep passes with less coverage rather than louder. Registering the set is
    what turns "each file is read once per model" into a statement about *which* files, and
    it is what catches a table that only some model points reach — a scenario path, a
    revision index — dropping out of the sweep unnoticed.
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

    ``before`` is taken from the warm ``model`` fixture, which the sweep above has already
    projected, rather than from a third instance projected cold for the purpose. The model
    that is *written*, though, is a fresh pristine read and never the shared one:
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
