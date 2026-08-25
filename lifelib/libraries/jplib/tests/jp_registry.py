"""The model registry, and the locator that resolves it against this library.

Models are located relative to **this library directory**, so the suite runs from a clean
clone with no installation step, and keeps running from a copy made by
``lifelib.create()`` — where it tests *that copy's* models, which is the whole point of
shipping the tests inside the library.

That is why the path here is relative and not :data:`lifelib._dirs.TEMPLATES`: the
canonical locator resolves to the *installed* library, so a copy would silently test
lifelib's pristine models instead of the user's edited ones, and pass while proving
nothing.

:data:`MODELS` is the registry ``test_model_conventions_jp.py`` is parametrized over, so
registering a model here subjects it to the whole house style: it then either conforms or
fails.  The metadata records the projection basis, which is not uniform across the
library — some products run on an annual grid and some on a monthly one — and records
that none of them discount.  That last entry is a property of the library, not an
omission: every ``technical-notes.md`` specifies *gross liability cash flows* and leaves
discounting and reserves to a separate layer that consumes them.

**Why this is not in `conftest.py`.**  Three libraries now ship in-library suites, and
``conftest.py`` is a name pytest fixes.  Collecting them in one run puts several files
called ``conftest`` on ``sys.path``, one wins ``sys.modules``, and every ``from conftest
import LIB`` in *any* of the suites silently resolves to another library — a green run
against the wrong models, or the ``FileNotFoundError`` that revealed it.  The registry
therefore lives under a library-unique module name and ``conftest.py`` re-exports it for
its fixtures.

**Why the short names are English.**  Everywhere else in this library the Japanese name
leads, because it is what the product is called.  A model name cannot follow: it is a
Python identifier and the name of a directory on disk.  Japanese products also have no
settled Latin abbreviation the way a RILA or a SPIA does, so there is nothing to borrow —
uslib and uklib take the market's own short name, and here there is none to take.  The
names below are therefore short English descriptors, and the pairing to the Japanese
product is written down in the library index rather than inferred.

Two of them are worth naming explicitly.  ``IncomeTerm_JP_S`` is 収入保障保険, whose
benefit is a **death** benefit paid as a monthly income to the end of the term — the UK
family income benefit shape, sold in Japan as a product in its own right.  It is not
income protection in uklib's sense, where ``IP_UK_S`` insures disability.  And ``LTC_JP_S``
is 介護保険, private nursing-care cover written on top of the public 公的介護保険 scheme,
not that scheme itself.
"""
import pathlib

LIB = pathlib.Path(__file__).resolve().parents[1]

ANNUAL = {"grid": "annual", "discounted": False}
MONTHLY = {"grid": "monthly", "discounted": False}

# The age basis is NOT uniform here, and it is not ``ANB`` — the value uslib and uklib
# carry.  Japan uses two age conventions and this library uses both, because the products
# do: 満年齢 (*man nenrei*, age last birthday) is what most 契約年齢 tables and model points
# are stated on, while 保険年齢 (*hoken nenrei*, insurance age, nearest birthday) is what
# 個人年金保険 quotes and, more importantly, what 標準生命表2018 itself is graduated on.
#
# That mismatch is a modelled quantity rather than a footnote: a model whose points are
# 満年齢 reading a 保険年齢 table understates the rate, and the models that care carry an
# explicit shift for it.  Recording the basis per model is what keeps the two apart.
MAN = {"age_basis": "満年齢"}       # age last birthday
HOKEN = {"age_basis": "保険年齢"}   # insurance age, nearest birthday

# name -> (path relative to the library root, metadata)
#
# The name is <short name>_<country>_<grid>: a short English descriptor of the product,
# then JP, then _A for an annual step or _S for a monthly one.  The grid letters follow
# lifelib, where annuallife/TradLife_A is the annual-step model and basiclife/BasicTerm_S
# and savings/CashValue_SE are the monthly ones.
#
# This pairing is not derivable from the folder slug — "individual_annuity" spelled out is
# unusable in a model name — so it lives here, and test_model_conventions_jp.py asserts
# that the name, the folder and the model's own _name all agree.
MODELS = {
    # Protection
    "Term_JP_A": ("products/term_life/Term_JP_A", ANNUAL | MAN),
    "IncomeTerm_JP_S": ("products/income_guarantee/IncomeTerm_JP_S", MONTHLY | MAN),
    # Savings
    "WholeLife_JP_A": ("products/whole_life/WholeLife_JP_A", ANNUAL | MAN),
    "Endowment_JP_A": ("products/endowment/Endowment_JP_A", ANNUAL | MAN),
    "FXWholeLife_JP_S": ("products/fx_whole_life/FXWholeLife_JP_S", MONTHLY | MAN),
    # Third sector (第三分野)
    "Medical_JP_S": ("products/medical/Medical_JP_S", MONTHLY | MAN),
    "Cancer_JP_S": ("products/cancer/Cancer_JP_S", MONTHLY | MAN),
    "LTC_JP_S": ("products/nursing_care/LTC_JP_S", MONTHLY | MAN),
    # Annuity — the one product quoted on 保険年齢 rather than 満年齢
    "Annuity_JP_A": ("products/individual_annuity/Annuity_JP_A", ANNUAL | HOKEN),
}


# name -> the exact set of input files a full sweep of the shipped model point table reads.
#
# ``test_model_conventions_jp.py`` asserts this set, not merely that whatever was read was
# read once.  Counting only the files that happen to be read makes the check self-
# fulfilling: a file that stops being read drops out of the counter, and the read-once
# assertion then passes over less coverage rather than failing.  Registering the set is
# what turns "each file is read once per model" into a statement about *which* files.
#
# It also fixes how far the sweep has to run.  Eight of the nine models read every file
# they need on the very first model point, but ``FXWholeLife_JP_S`` does not:
# ``fx_path_table.csv`` is first read at model point 7 of 8, because the 為替 path only
# differs from the flat TTM there.  A check over a truncated table would drop it silently.
INPUT_FILES = {
    "Annuity_JP_A": {
        "commute_factor_table.csv", "expense_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_anchor_table.csv", "mort_table.csv",
        "pricing_table.csv"},
    "Cancer_JP_S": {
        "hosp_stay_table.csv", "incidence_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv", "sex_factor_table.csv",
        "survival_table.csv"},
    "Endowment_JP_A": {
        "benefit_schedule_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv"},
    "FXWholeLife_JP_S": {
        "charge_table.csv", "fx_path_table.csv", "lapse_table.csv",
        "model_point_table.csv", "mort_table.csv"},
    "IncomeTerm_JP_S": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "rate_class_table.csv"},
    "LTC_JP_S": {
        "grade_share_table.csv", "lapse_table.csv", "model_point_table.csv",
        "mort_table.csv", "prevalence_table.csv"},
    "Medical_JP_S": {
        "incidence_table.csv", "lapse_table.csv", "los_table.csv",
        "model_point_table.csv", "mort_table.csv"},
    "Term_JP_A": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv",
        "prem_rate_table.csv"},
    "WholeLife_JP_A": {
        "lapse_table.csv", "model_point_table.csv", "mort_table.csv"},
}


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
