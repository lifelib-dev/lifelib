# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.IUL_US_S.Projection` as ``data``. :mod:`~.IUL_US_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/indexed_ul/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values --
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IUL_US_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
coi_rates_file          coi_rates()                 coi_rates.csv
corridor_file           corridor_factors()          corridor_factors.csv
mort_table_file         mort_table()                mort_table.csv
class_factor_file       class_factor_table()        class_factor_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
surr_charge_file        surr_charge_table()         surr_charge_table.csv
======================  ==========================  ==============================

Two of these are stand-ins for licensed material and are marked **[std]** row by row in
their own ``provenance`` columns. ``coi_rates.csv`` carries the *guaranteed maximum*
monthly rate per $1,000 of net amount at risk; the notes set that basis at 2017 CSO ANB
ultimate [REG-R17], which may not be reproduced here, and the current scale is the
guaranteed scale times ``Projection.coi_curr_factor`` (65% **[std]**) because carrier
COI tables are not public. ``mort_table.csv`` is a small illustrative best-estimate
table **[std]**, not the 2015 VBT the notes recommend [REG-R18]; it is the same
illustrative table shipped with ``UL_US_S``, so the chassis and this model share
a basis.

There is deliberately **no premium persistency table**. The universal life chassis reads
one, because its notes give a 16-row schedule; these notes instead give a closed form --
``expected premium_y = planned x 0.98^(y-1)`` -- which is implemented as
:func:`~.IUL_US_S.Projection.prem_persistency` with the rate in a Reference. Nor is
there an index scenario file: the base deterministic run generates
:func:`~.IUL_US_S.Projection.index_level` from a level annual return, and a stochastic
or historical path is substituted by overriding that one cells.

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name, then clear the cache. No formula
changes.
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


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*.

    The IRC 7702(d)(2) applicable percentages [R4]: 250% to attained age 40, grading to
    100% at 90-95.
    """
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by age, read from *mort_table.csv*."""
    return pd.read_csv(input_dir() / mort_table_file, index_col="age")  # noqa: F821


def class_factor_table():
    """The underwriting-class factors, read from *class_factor_table.csv*."""
    return pd.read_csv(input_dir() / class_factor_file, index_col="rate_class")  # noqa: F821


def lapse_table():
    """The base annual lapse rates by policy year, read from *lapse_table.csv*."""
    return pd.read_csv(input_dir() / lapse_table_file, index_col="policy_year")  # noqa: F821


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of years over which it runs off linearly.
    """
    return pd.read_csv(input_dir() / surr_charge_file, index_col="surr_charge_id")  # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

surr_charge_file = "surr_charge_table.csv"

pd = ("Module", "pandas")