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


def model_path(name):
    """Absolute path to a model folder, from its entry in :data:`MODELS`."""
    return LIB / MODELS[name][0]
