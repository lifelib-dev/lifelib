# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The three input CSVs are read here, **once per model**, and referenced from
:mod:`~.WOL_UK_S.Projection` as ``data``. :mod:`~.WOL_UK_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/whole_of_life/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WOL_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
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

Both the mortality and the lapse table are keyed by the **cell** as well as by the usual
rating factors, because the two cells of this product do not share a basis and must not
be given each other's. The underwritten cell restores select experience through full
underwriting and takes an assured-lives shape; the guaranteed-acceptance cell cannot be
better than the population and self-selects worse, so it takes a population shape with an
anti-selection loading. The FCA's price differential between the two designs — £71.73
against £8.10 per £1,000 of cover — is the scale of the error a basis mix-up produces.
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
    """The annual mortality rates, read from *mort_table.csv*.

    Keyed by basis (``population`` or ``assured``), sex, smoker status and age last
    birthday, and capped at 1.  Both bases are **[std]** proxies: the ``population``
    rates are shaped like the ONS national life tables and anchored so that the O50
    cell's loaded rate is the notes' walk-through basis exactly, and the ``assured``
    rates are shaped like the "00" Series permanent assurance tables.  Neither is a
    published table, and the file's ``provenance`` column says which cells are anchors
    and which come from a sex or smoker factor.  Sorted on read, because
    ``Projection.mort_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["basis", "sex", "smoker", "age"]).sort_index()


def lapse_table():
    """The annual lapse rates by cell and policy year, from *lapse_table.csv*.

    The two cells carry different tables: the guaranteed-acceptance one lapses faster
    early, on affordability attrition.  Both are **[std]** drafting constructions - no
    public UK whole of life lapse study was retrieved - and on a product with no
    surrender value they are the single largest lever on the liability.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col=["cell", "policy_year"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

pd = ("Module", "pandas")