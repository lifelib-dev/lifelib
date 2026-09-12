"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions_uk.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis — every model in this library runs on a
monthly grid, the frequency these products are written in — and records that none of them
discount.  :data:`ANNUAL` is kept alongside :data:`MONTHLY` because the grid is a property
of the model rather than of the library, and a later annual-step model would register with
it.  ``discounted: False`` is a property of the library, not an omission: every
``technical-notes.md`` specifies *gross liability cash flows* and leaves discounting and
reserves to a separate layer that consumes them.

**Why this is not in `conftest.py`.**  Two libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting both in one run puts two files called
``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest import
LIB`` in *either* suite silently resolves to the other library — a green run against the
wrong models, or the ``FileNotFoundError`` that revealed it.  The registry therefore lives
under a library-unique module name and ``conftest.py`` re-exports it for its fixtures.
"""
import pathlib

LIB = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "discounted": False}
MONTHLY = {"grid": "monthly", "discounted": False}

# The age basis is a property of the product, not of the grid: most of the library rates
# on age nearest birthday, but whole of life prices on "age last birthday" for both cells,
# the unit-linked bond's mortality charge is quoted ALB, and the pension annuity's
# generational table is entered ALB.  It is recorded per model rather than folded into the
# grid constants, where a single value would be false for three of the seven.
ANB, ALB = "ANB", "ALB"

# name -> (path relative to the library root, metadata)
#
# The name is <market short name>_<country>_<grid>: the name the product is actually known
# by (CI, IP, WOL, ULB, WP, PA — the same short names the taxonomy table in the library's
# index uses), then UK, then _A for an annual step or _S for a monthly one.  The grid
# letters follow lifelib, where annuallife/TradLife_A is the annual-step model and
# basiclife/BasicTerm_S and savings/CashValue_SE are the monthly ones.  Every model here
# carries _S: the whole library is on a monthly grid.
#
# This pairing is not derivable from the folder slug — "unit_linked_bond" spelled out is
# unusable in a model name — so it lives here, and test_model_conventions_uk.py asserts
# name, folder and the model's own _name all agree.
MODELS = {
    # Protection
    "Term_UK_S": ("products/term_assurance/Term_UK_S", {**MONTHLY, "age_basis": ANB}),
    "CI_UK_S": ("products/critical_illness/CI_UK_S", {**MONTHLY, "age_basis": ANB}),
    "IP_UK_S": ("products/income_protection/IP_UK_S", {**MONTHLY, "age_basis": ANB}),
    "WOL_UK_S": ("products/whole_of_life/WOL_UK_S", {**MONTHLY, "age_basis": ALB}),
    # Savings
    "ULB_UK_S": ("products/unit_linked_bond/ULB_UK_S", {**MONTHLY, "age_basis": ALB}),
    "WP_UK_S": ("products/with_profits/WP_UK_S", {**MONTHLY, "age_basis": ANB}),
    # Annuity
    "PA_UK_S": ("products/pension_annuity/PA_UK_S", {**MONTHLY, "age_basis": ALB}),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# Each product module used to assert its own model's read *count* — ``PA_UK_S`` expects 2,
# ``IP_UK_S`` 5 — inside a copy of the read-once check that built its own instance and
# re-projected every model point to get it.  The counts are kept here as sets instead, and
# ``test_model_conventions_uk.py`` asserts them once against the sweep it already runs.
#
# The set, and not merely "whatever was read was read once", is the assertion: counting only
# the files that happen to be read makes the check self-fulfilling, since a file that stops
# being read drops out of the counter and the check then passes over less coverage rather
# than failing.
INPUT_FILES = {
    "CI_UK_S": {"ci_rate_table.csv", "lapse_table.csv", "model_point_table.csv"},
    "IP_UK_S": {
        "inception_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv", "termination_table.csv"},
    "PA_UK_S": {"model_point_table.csv", "mort_table.csv"},
    "Term_UK_S": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "select_factor_table.csv"},
    "ULB_UK_S": {"model_point_table.csv", "mort_table.csv", "surr_table.csv"},
    "WOL_UK_S": {"lapse_table.csv", "model_point_table.csv", "mort_table.csv"},
    "WP_UK_S": {"lapse_table.csv", "model_point_table.csv", "mort_table.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
