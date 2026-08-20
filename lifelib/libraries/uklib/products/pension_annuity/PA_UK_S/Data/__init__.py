# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The two input CSVs are read here, **once per model**, and referenced from
:mod:`~.PA_UK_S.Projection` as ``data``. :mod:`~.PA_UK_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many contracts are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/pension_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``PA_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
======================  ==========================  ==============================

There are only two files because this product has almost nothing to parameterize: no
lapse table, no charge scale, no bonus rates, no surrender-value schedule. Everything
else is either a contractual rule in the formulas or a single Reference on
``Projection``.

Substituting a licensed basis means replacing ``mort_table.csv`` with a same-schema
file — the SAPS S3/S4 pensioner tables or the PMA16/PFA16 insured-annuitant family,
both restricted to CMI Authorised Users — and setting ``Projection.annuitant_adj`` to 1
so the population-proxy adjustment stops being applied on top of an annuitant table.
No formula changes.
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
    """The base annual mortality rates by sex and age, from *mort_table.csv*.

    A **[std]** proxy shaped like the ONS UK national life tables, which are period
    tables of *population* mortality and the only freely redistributable UK source.  It
    is **not** an annuitant table: the proper bases are the SAPS S3/S4 pensioner tables
    and the PMA16/PFA16 insured-annuitant family, both restricted to CMI Authorised
    Users.  ``Projection.annuitant_adj`` carries the population-to-annuitant adjustment
    that stands in for the difference, and it is a shape-level placeholder rather than a
    calibration.  Sorted on read, because ``Projection.mort_rate_base`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

pd = ("Module", "pandas")