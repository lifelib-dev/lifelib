# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.WP_UK_A.Projection` as ``data``. :mod:`~.WP_UK_A.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/with_profits/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WP_UK_A`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
======================  ==========================  ==============================

Note how little is in a file. The discretionary scale that actually drives this product
— the bonus rates, the smoothing cap, the target corridor, the guarantee-fill target,
the charge levels — lives in model point columns and ``Projection`` References rather
than in a rate table, and that is not an oversight: **none of it is published**. Firms'
principles and practices documents describe the discretion and withhold the numbers, so
every one of those values is a standardization, and putting them where a reader trips
over them is better than filing them in a table that looks like data.
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

    A **[std]** proxy shaped like the ONS national life tables, which are the only
    freely redistributable UK mortality source; CMI tables issued after March 2013 are
    restricted to Authorised Users, so no current insured rate can be reproduced here.
    ``Projection.mort_be_factor`` carries the allowance for population mortality being
    heavier than insured experience.  Sorted on read, because ``Projection.mort_rate``
    indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


def lapse_table():
    """The base annual surrender rates by chassis and policy year, from *lapse_table.csv*.

    Flat on the bond chassis and duration-declining on the endowment.  Both are **[std]**
    drafting constructions - no public UK with-profits lapse experience was retrieved -
    and the dynamic multipliers layered on them in ``Projection.surr_rate`` matter more
    than the levels do, because anti-selective exit when guarantees are in the money is
    the dominant behavioural risk on this product.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col=["chassis", "policy_year"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")