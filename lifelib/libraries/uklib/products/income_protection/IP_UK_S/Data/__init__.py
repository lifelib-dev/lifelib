# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.IP_UK_S.Projection` as ``data``. :mod:`~.IP_UK_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/income_protection/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IP_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
inception_file          inception_table()           inception_table.csv
termination_file        termination_table()         termination_table.csv
mort_table_file         mort_table()                mort_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
======================  ==========================  ==============================

The two experience bases are separate files because they are separate CMI publications
and are parameterized differently. Inception rates are keyed by **sex, occupation class,
deferred period and age**, exactly as the IP11 Series names its tables; termination
rates are keyed by **claim duration** alone here, which is a deliberate simplification —
IP11 terminations are two-dimensional in age and duration, with claimant mortality
duration-dependent to five years and age-only beyond, and a licensee should restore the
age dimension by adding it as an index level. Nothing in the projection assumes the
termination basis is one-dimensional except the lookup itself.
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


def inception_table():
    """The claim inception rates, read from *inception_table.csv*.

    Annual rates per life in state H, keyed by sex, occupation class, deferred period
    and pivot age - the IP11 Series parameterization.  A **[std]** proxy: the IP11
    values are restricted to CMI Authorised Users, and the file's ``provenance`` column
    marks which cells are the notes' own pivots and which come from a factor.  Sorted
    on read, because ``Projection.inception_rate`` slices it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / inception_file,                                # noqa: F821
        index_col=["sex", "occ_class", "deferred_weeks", "age"]).sort_index()


def termination_table():
    """The claim termination rates, read from *termination_table.csv*.

    Annual recovery and in-claim mortality rates by claim duration year.  IP11 splits
    terminations into recovery and death exactly this way, but is two-dimensional in
    age and duration; the age dimension is suppressed here **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / termination_file,                              # noqa: F821
        index_col="claim_duration_year")


def mort_table():
    """The active-life mortality rates by sex and age, from *mort_table.csv*.

    A **[std]** proxy shaped like the ONS UK national life tables, which are the only
    freely redistributable UK mortality source; population mortality is heavier than
    insured experience, and active-life mortality is a minor decrement in income
    protection anyway, so the shipped rates are a placeholder to be replaced with
    portfolio experience.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


def lapse_table():
    """The lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

inception_file = "inception_table.csv"

termination_file = "termination_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")