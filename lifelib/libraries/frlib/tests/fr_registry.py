"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions_fr.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis — every model in this library now runs
on a monthly grid — and records that none of them discount.  That last entry is a property of the library, not an
omission: every ``technical-notes.md`` specifies *gross liability cash flows* and leaves
discounting and reserves to a separate layer that consumes them.

**Why this is not in `conftest.py`.**  Four libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting them in one run puts several files
called ``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest
import LIB`` in *any* of the suites silently resolves to another library — a green run
against the wrong models, or the ``FileNotFoundError`` that revealed it.  The registry
therefore lives under a library-unique module name and ``conftest.py`` re-exports it for
its fixtures.

**Why the short names are what they are.**  Everywhere else in this library the French
name leads, because it is what the product is called.  A model name cannot follow: it is
a Python identifier and the name of a directory on disk, and *assurance vie en unités de
compte* has no spelling that survives that.  Where the French market itself uses a short
form the model takes it — ``UC``, ``PER``, ``ADE`` — and where it does not, the name is a
short descriptor.  The pairing to the French product is written down in the library index
rather than inferred.

Two of them are worth naming explicitly.  ``ADE_FR_S`` is *assurance des emprunteurs*,
mortgage borrower's protection: a death, PTIA, ITT and IPT cover written against an
amortising loan, and the largest individual protection market in France.  It is not term
assurance in ``TD_FR_S``'s sense, where the sum assured is a level or freely chosen
capital rather than the loan balance.  And ``EC_FR_S`` is *eurocroissance*, the hybrid
support whose capital guarantee bites only at a stated term — not a second euro fund.
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

# name -> (path relative to the library root, metadata)
#
# The name is <short name>_<country>_<grid>: the short form the French market itself uses
# where there is one — UC, PER, ADE, EC — and a short descriptor where there is not, then
# FR, then _A for an annual step or _S for a monthly one.  The grid letters follow lifelib,
# where annuallife/TradLife_A is the annual-step model and basiclife/BasicTerm_S and
# savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "assurance_emprunteur" spelled out
# is unusable in a model name — so it lives here, and test_model_conventions_fr.py asserts
# that the name, the folder and the model's own _name all agree.
MODELS = {
    # Épargne (savings)
    "Euro_FR_S": ("products/assurance_vie_euro/Euro_FR_S", MONTHLY),
    "UC_FR_S": ("products/assurance_vie_uc/UC_FR_S", MONTHLY),
    "EC_FR_S": ("products/eurocroissance/EC_FR_S", MONTHLY),
    # Retraite (retirement)
    "PER_FR_S": ("products/per_assurance/PER_FR_S", MONTHLY),
    "Rente_FR_S": ("products/rente_viagere/Rente_FR_S", MONTHLY),
    # Prévoyance (protection)
    "TD_FR_S": ("products/temporaire_deces/TD_FR_S", MONTHLY),
    "ADE_FR_S": ("products/assurance_emprunteur/ADE_FR_S", MONTHLY),
    "Obseques_FR_S": ("products/obseques/Obseques_FR_S", MONTHLY),
    "Dep_FR_S": ("products/dependance/Dep_FR_S", MONTHLY),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# ``test_model_conventions_fr.py`` asserts this set, not merely that whatever was read was
# read once.  Counting only the files that happen to be read makes the check self-
# fulfilling: a file that stops being read drops out of the counter, and the read-once
# assertion then passes over less coverage rather than failing.  Registering the set is
# what turns "each file is read once per model" into a statement about *which* files.
INPUT_FILES = {
    "ADE_FR_S": {
        "crd_rate_table.csv", "franchise_table.csv", "itt_inception_table.csv",
        "itt_termination_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv"},
    "Dep_FR_S": {
        "cause_mix_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv", "prevalence_table.csv", "reduction_table.csv",
        "revision_table.csv", "severity_share_table.csv"},
    "EC_FR_S": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "scenario_table.csv", "tec_curve.csv"},
    "Euro_FR_S": {
        "fin_rate_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv"},
    "Obseques_FR_S": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "select_table.csv", "single_prem_table.csv", "surr_scale_table.csv"},
    "PER_FR_S": {
        "allocation_grid.csv", "annuity_factor.csv", "exit_table.csv",
        "model_point_table.csv", "mort_table.csv"},
    "Rente_FR_S": {
        "model_point_table.csv", "mort_table.csv", "reversion_coeff_table.csv"},
    "TD_FR_S": {
        "benefit_schedule.csv", "freq_loading_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "premium_rate_table.csv"},
    "UC_FR_S": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "plancher_rate_table.csv", "uc_scenario_table.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
