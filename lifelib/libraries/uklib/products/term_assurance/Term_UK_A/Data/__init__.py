# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.Term_UK_A.Projection` as ``data``. :mod:`~.Term_UK_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/term_assurance/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_UK_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
select_factor_file      select_factor_table()       select_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
======================  ==========================  ==============================

To swap in a licensed mortality basis — the CMI "16" Series assured lives tables
TMNL16/TFNL16, which are subscriber-restricted and cannot be redistributed here —
replace ``mort_table.csv`` and ``select_factor_table.csv`` with same-schema files, or
point ``mort_table_file`` and ``select_factor_file`` at different names, then clear the
cache. No formula changes: the mortality lookup already carries the select-duration
argument the UK tables need.
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
    """The mortality rates by sex, smoker status and age, from *mort_table.csv*.

    Read as the applied best-estimate rate on the ``applied`` mortality basis and as
    the ultimate rate on the ``select`` basis; see ``Projection.mort_basis``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "smoker", "age"])


def select_factor_table():
    """The select-duration factors, read from *select_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / select_factor_file, index_col="duration")      # noqa: F821


def lapse_table():
    """The lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

select_factor_file = "select_factor_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")