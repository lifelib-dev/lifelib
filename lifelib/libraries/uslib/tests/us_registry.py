"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis, which is not uniform across the
library — some products run on an annual grid and some on a monthly one — and records
that none of them discount.  That last entry is a property of the library, not an
omission: every ``technical-notes.md`` specifies *gross liability cash flows* and leaves
discounting and reserves to a separate layer that consumes them.

**Why this is not in `conftest.py`.**  Two libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting both in one run puts two files called
``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest import
LIB`` in *either* suite silently resolves to the other library — a green run against the
wrong models, or the ``FileNotFoundError`` that revealed it.  The registry therefore lives
under a library-unique module name and ``conftest.py`` re-exports it for its fixtures.
"""
import pathlib

LIB = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "age_basis": "ANB", "discounted": False}
MONTHLY = {"grid": "monthly", "age_basis": "ANB", "discounted": False}

# name -> (path relative to the library root, metadata)
#
# The name is <market short name>_<country>_<grid>: the name the product is actually known
# by (MYGA, RILA, SPIA, ULSG — the same short names the taxonomy tables in the library's
# README use), then US, then _A for an annual step or _S for a monthly one.  The grid
# letters follow lifelib, where annuallife/TradLife_A is the annual-step model and
# basiclife/BasicTerm_S and savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "registered_index_linked_annuity"
# spelled out is unusable and the industry says RILA — so it lives here, and
# test_model_conventions.py asserts name, folder and the model's own _name all agree.
MODELS = {
    # Life
    "Term_US_A": ("products/term_life/Term_US_A", ANNUAL),
    "WholeLife_US_A": ("products/whole_life/WholeLife_US_A", ANNUAL),
    "UL_US_S": ("products/universal_life/UL_US_S", MONTHLY),
    "IUL_US_S": ("products/indexed_ul/IUL_US_S", MONTHLY),
    "VUL_US_S": ("products/variable_ul/VUL_US_S", MONTHLY),
    "ULSG_US_S": ("products/guaranteed_ul/ULSG_US_S", MONTHLY),
    # Annuity — deferred
    "MYGA_US_S": ("products/fixed_deferred_annuity/MYGA_US_S", MONTHLY),
    "FIA_US_S": ("products/fixed_indexed_annuity/FIA_US_S", MONTHLY),
    "VA_US_S": ("products/variable_annuity/VA_US_S", MONTHLY),
    "RILA_US_S": (
        "products/registered_index_linked_annuity/RILA_US_S", MONTHLY),
    # Annuity — payout
    "SPIA_US_S": ("products/immediate_annuity/SPIA_US_S", MONTHLY),
    "DIA_US_S": ("products/deferred_income_annuity/DIA_US_S", MONTHLY),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# ``test_model_conventions.py`` asserts this set, not merely that whatever was read was
# read once.  Counting only the files that happen to be read makes the check self-
# fulfilling: a file that stops being read drops out of the counter, and the read-once
# assertion passes over less coverage rather than failing.  Registering the set is what
# turns "each file is read once per model" into a statement about *which* files.
#
# The set is what the **base run** reads, which is not always every CSV in the directory.
# ``VUL_US_S`` ships ``prem_persistency.csv`` and does not read it: ``prem_persistency(t)``
# short-circuits to 1.0 while ``dyn_behavior_on`` is off, which is the default, so only a
# test that switches the behaviour module on reaches the table.  Two files are reached
# late rather than not at all — ``SPIA_US_S`` first reads its mortality table and
# improvement scale at model point 7, where ``mort_basis`` stops being ``"scenario"`` —
# which is why the sweep has to run to the end of the table before this is asserted.
INPUT_FILES = {
    "DIA_US_S": {
        "improvement_scale.csv", "model_point_table.csv", "mort_table.csv",
        "payout_factor_table.csv", "premium_schedule.csv", "rop_factor_table.csv"},
    "FIA_US_S": {
        "model_point_table.csv", "mort_table.csv", "payout_rate_table.csv",
        "rate_scenario.csv", "rollup_table.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "IUL_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "surr_charge_table.csv"},
    "MYGA_US_S": {
        "model_point_table.csv", "mort_table.csv", "mva_factor_table.csv",
        "rate_scenario.csv", "surr_charge_age_cap.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "RILA_US_S": {
        "guar_min_rate_table.csv", "lapse_table.csv", "market_scenario.csv",
        "model_point_table.csv", "mort_table.csv", "surr_charge_table.csv",
        "withdrawal_table.csv"},
    "SPIA_US_S": {
        "improvement_scale.csv", "model_point_table.csv", "mort_table.csv",
        "surr_charge_table.csv"},
    "Term_US_A": {
        "class_factor_table.csv", "model_point_table.csv", "mort_table.csv",
        "premium_rates.csv", "shock_lapse_table.csv"},
    "ULSG_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "rop_table.csv", "surr_charge_table.csv"},
    "UL_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "prem_persistency.csv", "surr_charge_table.csv"},
    "VA_US_S": {
        "cdsc_table.csv", "fund_table.csv", "gawa_pct_table.csv",
        "model_point_table.csv", "mort_table.csv", "rate_scenario.csv",
        "return_scenario.csv", "transaction_table.csv"},
    "VUL_US_S": {
        "class_factor_table.csv", "coi_rates.csv", "corridor_factors.csv",
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "scenario_table.csv", "subaccount_table.csv", "surr_charge_table.csv"},
    "WholeLife_US_A": {
        "cv_table.csv", "model_point_table.csv", "mort_table.csv",
        "np_guar_table.csv", "nsp_table.csv", "premium_rates.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
