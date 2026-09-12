# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.Rente_FR_S.Projection` as ``data``. :mod:`~.Rente_FR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected — which matters more here than in the sibling payout models,
because a generational mortality table is two orders of magnitude larger than a period
one.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/rente_viagere/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Rente_FR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ============================
Reference                  Cells                           File
=========================  ==============================  ============================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
reversion_coeff_file       reversion_coeff_table()         reversion_coeff_table.csv
=========================  ==============================  ============================

There are three files rather than the sibling models' two because the *réversion*
coefficient is the one option-cost table any retrieved French source publishes, and a
published table belongs in a file rather than in a formula. There is no lapse table, no
charge scale, no bonus rate table and no surrender-value schedule, because the product
has none of those things: everything else is either a contractual rule in the formulas or
a single Reference on ``Projection``.

Substituting a licensed basis means replacing ``mort_table.csv`` with a same-schema file
— the TGH05/TGF05 generation tables homologated by the arrêté du 1er août 2006, which are
annexed to the Code des assurances and are not redistributed here — keyed on exactly the
same ``(sex, birth_year, age)``. **No formula changes**, and in particular no improvement
scale to switch off: the shipped proxy has the same generational *shape* as the
regulatory tables, so the model's indexing is exercised honestly even though the rates
are not the regulatory ones.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def input_dir():
    """The directory holding the input CSVs: the model folder's parent.

    Inputs are *external* files, not data stored inside the model, so the model
    folder is pure formulas.  The path is resolved at run time from where the model
    was read, following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The annual mortality rates by sex, *millésime* and age, from *mort_table.csv*.

    A **[std]** proxy with the *shape* of a French generation table: a rate is keyed on
    ``(sex, birth_year, age)`` and on nothing else, so the mortality trend lives inside
    the table and the projection needs no improvement scale.  It is **not** TGH05/TGF05,
    which the arrêté du 1er août 2006 homologates and the Code des assurances annexes,
    and which this library does not redistribute.  The rates are shaped on French
    population mortality and anchored so that the tariff annuity factor at the worked
    configuration's age and *millésime* reproduces the technical notes' placeholder
    *taux de rente* exactly; see ``Projection.taux_rente_tariff``.  Sorted on read,
    because ``Projection.mort_rate_at_age`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,
        index_col=["sex", "birth_year", "age"]).sort_index()


def reversion_coeff_table():
    """The published *réversion* coefficients, from *reversion_coeff_table.csv*.

    The only option-cost table any retrieved French source publishes.  It is keyed on the
    *taux de réversion* and on the difference in *millésime* between the reversionary and
    the annuitant — a positive difference meaning the reversionary is the younger life —
    given as an inclusive band ``(gen_diff_lo, gen_diff_hi)``.  The three published
    columns are 60%, 80% and 100%; a *taux de réversion* off that grid has no retrieved
    coefficient, and ``Projection.reversion_coeff`` raises rather than guessing one.
    Read without an index because the lookup is a band test, not a key lookup.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / reversion_coeff_file)                          # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

reversion_coeff_file = "reversion_coeff_table.csv"

pd = ("Module", "pandas")
