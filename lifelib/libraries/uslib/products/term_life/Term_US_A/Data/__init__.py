# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.Term_US_A.Projection` as ``data``. :mod:`~.Term_US_A.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/term_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_US_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
premium_rates_file      premium_rates()             premium_rates.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
shock_lapse_file        shock_lapse_table()         shock_lapse_table.csv
======================  ==========================  ==============================

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No
formula changes.
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
    return pd.read_csv(input_dir() / model_point_file, index_col="point_id")  # noqa: F821


def premium_rates():
    """The guaranteed premium schedule, read from *premium_rates.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rates_file,                            # noqa: F821
        index_col=["plan", "sex", "rate_class", "band", "policy_year"])


def mort_table():
    """The base mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(input_dir() / class_factor_file, index_col="rate_class")  # noqa: F821


def shock_lapse_table():
    """The shock-lapse buckets by jump ratio, read from *shock_lapse_table.csv*."""
    return pd.read_csv(input_dir() / shock_lapse_file)               # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

premium_rates_file = "premium_rates.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

shock_lapse_file = "shock_lapse_table.csv"

pd = ("Module", "pandas")