# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.CI_UK_S.Projection` as ``data``. :mod:`~.CI_UK_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/critical_illness/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``CI_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
ci_rate_file            ci_rate_table()             ci_rate_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
======================  ==========================  ==============================

``ci_rate_table.csv`` holds **pivot ages only** — 40, 45, 50, 55, 60, 65 — because that
is the form the technical notes give the basis in, together with the rule that
intermediate ages are interpolated log-linearly. The interpolation therefore lives in
``Projection.pivot_interp`` rather than being baked into a pre-expanded file, and
swapping in a licensed AC04 or "16" Series basis means replacing a 24-row table, not a
generated one.
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


def ci_rate_table():
    """The CI diagnosis and mortality pivot rates, from *ci_rate_table.csv*.

    Annual rates at the pivot ages 40, 45, 50, 55, 60 and 65 by sex and smoker status.
    ``i_ci`` is the first-diagnosis rate for a listed condition including total and
    permanent disability; ``q_d`` is best-estimate mortality.  Both are **[std]**
    proxies - the CMI accelerated-CI tables are subscriber-restricted - and the file's
    ``provenance`` column says which cells came from the notes and which from a
    sex/smoker factor.

    Sorted on read: ``Projection.pivot_interp`` slices the frame by (sex, smoker), and
    pandas warns about indexing past the lexsort depth of an unsorted MultiIndex.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / ci_rate_file,                                  # noqa: F821
        index_col=["sex", "smoker", "age"]).sort_index()


def lapse_table():
    """The lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

ci_rate_file = "ci_rate_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")