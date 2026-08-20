# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.ULB_UK_S.Projection` as ``data``. :mod:`~.ULB_UK_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/unit_linked_bond/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ULB_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
surr_table_file         surr_table()                surr_table.csv
======================  ==========================  ==============================

Note what is **not** an input file. The charge rates — the annual management charge, the
fund-borne further costs, the tax provision rate, the death-benefit uplift — are model
point columns rather than a rate table, because they are per-policy contractual and
discretionary parameters rather than experience assumptions, and because per-fund charge
rate cards are not published anyway. The fund return is a single Reference on
``Projection``, because the base run is deterministic.
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

    A **[std]** proxy shaped like the ONS UK national life tables, the only fully
    redistributable UK mortality source; the CMI's current assured-lives tables are
    restricted to Authorised Users.  ``Projection.mort_be_factor`` carries the crude
    allowance for population mortality being heavier than insured-lives experience.

    Mortality is nearly irrelevant on this product - the net amount at risk is a tenth
    of a percent of the unit fund - unless the guaranteed minimum death benefit rider is
    enabled, which is why a proxy of this quality is tolerable here and would not be
    elsewhere.  Sorted on read, because ``Projection.mort_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


def surr_table():
    """The base annual full-surrender rates by policy year, from *surr_table.csv*.

    Low early, rising as the advised five-to-ten-year holding period completes, then
    settling at a high ultimate level.  A **[std]** drafting construction: no public UK
    bond persistency study was fetched.  On a product whose every margin line is
    proportional to the unit fund *and* to persistency, this is the first assumption to
    sensitivity-test.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_table_file, index_col="policy_year")      # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

surr_table_file = "surr_table.csv"

pd = ("Module", "pandas")