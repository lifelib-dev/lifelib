"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions_de.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis — every model in this library now runs
on a monthly grid — and records that none of them discount.  That last entry is a property
of the library, not an omission:
every ``technical-notes.md`` specifies *gross liability cash flows* and leaves discounting,
the ``Deckungsrückstellung`` and Solvency II technical provisions to a separate layer that
consumes them.

**Why this is not in `conftest.py`.**  Five libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting them in one run puts several files
called ``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest
import LIB`` in *any* of the suites silently resolves to another library — a green run
against the wrong models, or the ``FileNotFoundError`` that revealed it in frlib.  The
registry therefore lives under a library-unique module name and ``conftest.py`` re-exports
it for its fixtures.

**Why the short names are what they are.**  Everywhere else in this library the German
name leads, because it is what the product is called.  A model name cannot follow: it is a
Python identifier and the name of a directory on disk, and *fondsgebundene
Rentenversicherung* has no spelling that survives that.  Where the German market itself
uses a short form the model takes it — ``KLV``, ``RLV``, ``BU`` — and where it does not,
the name is a short descriptor.  The pairing to the German product is written down in the
library index rather than inferred.

Four of them are worth naming explicitly.  ``RV_DE_S`` is the *klassische aufgeschobene
private Rentenversicherung*, the deferred annuity written on the general account with a
guaranteed *Rentenfaktor*; it is not the payout contract, which is ``Sofort_DE_S``.
``Index_DE_S`` is the *indexgebundene Rentenversicherung* — the German "Indexpolice", whose
capital sits in the *Sicherungsvermögen* and whose upside is an annual index participation
bought out of the *Überschuss* — and not a unit-linked contract, which is ``FRV_DE_S``.
``Basis_DE_S`` is the *Basisrente* of Schicht 1 (Rürup), whose defining facts are what it
may **not** do: no surrender, no capital option, no assignment.  And ``Riester_DE_S`` is
the Schicht 2 contract, whose defining facts are a state *Zulage* that is a cash flow and a
statutory 100 % *Beitragsgarantie* that is a constraint on the projection rather than a
parameter of it.
"""
import pathlib

LIB = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "age_basis": "ALB", "discounted": False}
MONTHLY = {"grid": "monthly", "age_basis": "ALB", "discounted": False}

# ``ANNUAL`` has no members below, and that is **not** the same as saying the library has no
# use for it.  The metadata is a statement about a model rather than about the library: a
# model added or converted to an annual step registers ``ANNUAL`` here, and
# ``test_the_name_carries_the_right_grid_suffix`` then requires its name to end ``_A``.  The
# row and the name move together, which is the point of asserting the suffix from the
# metadata rather than from the folder.
#
# The row is checked against the **frame** as well as against the name.  A suffix is
# spelling, and six of these models spent a while carrying ``_S`` in the registry while
# still stepping a year at a time; ``test_a_monthly_registry_entry_means_a_monthly_frame``
# reads the grid off the attained age instead, which steps once every twelve periods on a
# monthly frame and every period on an annual one.  Mis-registering a model is therefore a
# failure rather than a rename.

# name -> (path relative to the library root, metadata)
#
# The name is <short name>_<country>_<grid>: the short form the German market itself uses
# where there is one — KLV, RLV, BU — and a short descriptor where there is not, then DE,
# then _A for an annual step or _S for a monthly one.  The grid letters follow lifelib,
# where annuallife/TradLife_A is the annual-step model and basiclife/BasicTerm_S and
# savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "fondsgebundene_rentenversicherung"
# spelled out is unusable in a model name — so it lives here, and
# test_model_conventions_de.py asserts that the name, the folder and the model's own _name
# all agree.
MODELS = {
    # Kapitalbildende Lebensversicherung und private Rentenversicherung (Schicht 3)
    "KLV_DE_S": ("products/kapitallebensversicherung/KLV_DE_S", MONTHLY),
    "RV_DE_S": ("products/klassische_rentenversicherung/RV_DE_S", MONTHLY),
    "FRV_DE_S": ("products/fondsgebundene_rentenversicherung/FRV_DE_S", MONTHLY),
    "Index_DE_S": ("products/indexpolice/Index_DE_S", MONTHLY),
    # Geförderte Altersvorsorge (Schicht 1 und Schicht 2)
    "Basis_DE_S": ("products/basisrente/Basis_DE_S", MONTHLY),
    "Riester_DE_S": ("products/riester_rente/Riester_DE_S", MONTHLY),
    # Rentenbezug
    "Sofort_DE_S": ("products/sofortrente/Sofort_DE_S", MONTHLY),
    # Biometrie
    "RLV_DE_S": ("products/risikolebensversicherung/RLV_DE_S", MONTHLY),
    "BU_DE_S": ("products/berufsunfaehigkeit/BU_DE_S", MONTHLY),
    "Pflege_DE_S": ("products/pflegerentenversicherung/Pflege_DE_S", MONTHLY),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# ``test_model_conventions_de.py`` asserts this set, not merely that whatever was read was
# read once.  Counting only the files that happen to be read makes the check self-
# fulfilling: a file that stops being read drops out of the counter, and the read-once
# assertion then passes over less coverage rather than failing.  Registering the set is
# what turns "each file is read once per model" into a statement about *which* files.
#
# This table is generated from a real sweep rather than transcribed by hand — see
# ``tools/`` in the repository root — but it is committed, because a generated-at-run-time
# expectation would assert nothing at all.
INPUT_FILES = {
    "BU_DE_S": {
        "claim_duration_table.csv", "freq_loading_table.csv", "inception_table.csv",
        "lapse_table.csv", "model_point_table.csv", "mortality_table.csv",
        "occupation_table.csv"},
    "Basis_DE_S": {
        "behaviour_table.csv", "charge_table.csv", "model_point_table.csv",
        "mort_table.csv", "option_table.csv", "rentenfaktor_table.csv",
        "surplus_table.csv"},
    "FRV_DE_S": {
        "charge_table.csv", "fund_scenario_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv"},
    "Index_DE_S": {
        "election_table.csv", "freq_load_table.csv", "index_param_table.csv",
        "index_return_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv", "surplus_rate_table.csv"},
    "KLV_DE_S": {
        "cost_table.csv", "deckrv_table.csv", "freq_loading_table.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "surplus_rate_table.csv"},
    "Pflege_DE_S": {
        "basis_table.csv", "benefit_scale_table.csv", "care_table.csv",
        "expense_table.csv", "incidence_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "surrender_table.csv"},
    "RLV_DE_S": {
        "benefit_schedule.csv", "freq_loading_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "nvg_schedule.csv"},
    "RV_DE_S": {
        "charge_table.csv", "decl_rate_table.csv", "freq_load_table.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv", "param_table.csv",
        "rentenfaktor_table.csv"},
    "Riester_DE_S": {
        "annuity_mort_table.csv", "freq_loading.csv", "income_schedule.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table_accum.csv",
        "surplus_scenario.csv", "zulage_schedule.csv"},
    "Sofort_DE_S": {
        "hoechstrechnungszins_table.csv", "improvement_table.csv",
        "model_point_table.csv", "mort_table.csv", "surplus_scale_table.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
