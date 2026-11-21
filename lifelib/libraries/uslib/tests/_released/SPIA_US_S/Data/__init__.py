# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.SPIA_US_S.Projection` as ``data``. :mod:`~.SPIA_US_S.Projection`
is parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/immediate_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``SPIA_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table.csv
mort_table_file           mort_table()                    mort_table.csv
improvement_scale_file    improvement_scale()             improvement_scale.csv
surr_charge_file          surr_charge_table()             surr_charge_table.csv
========================  ==============================  ==========================

The two mortality tables are keyed by ``(age, sex)`` and the surrender-charge table by
``policy_year``. They are separate files on purpose: the technical notes require the
best-estimate basis to be the **2012 IAM Basic** table projected with **Projection Scale
G2**, two distinct objects with distinct provenance, and neither may be embedded in the
model — the shipped tables are illustrative **[std]** stand-ins. To swap in a licensed
basis, replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file``
at a different name, then clear the cache. No formula changes. The improvement scale is
swappable the same way, which is how the notes' first sensitivity — a 50% / 150% scaling
of tabulated improvement — is run.
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


def mort_table():
    """The base annuitant mortality table by age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def improvement_scale():
    """The generational improvement scale by age and sex, from *improvement_scale.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / improvement_scale_file, index_col=["age", "sex"])  # noqa: F821


def surr_charge_table():
    """The commutation surrender-charge scale by contract year, from *surr_charge_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="policy_year")     # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

improvement_scale_file = "improvement_scale.csv"

surr_charge_file = "surr_charge_table.csv"

pd = ("Module", "pandas")