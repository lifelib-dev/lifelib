# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.ULSG_US_S.Projection` as ``data``. :mod:`~.ULSG_US_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/guaranteed_ul/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded
values -- so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ULSG_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

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
rop_file                rop_table()                 rop_table.csv
======================  ==========================  ==============================

``coi_rates.csv`` carries the **guaranteed maximum annual** rate per $1,000, by
attained age; ``Projection.coi_rate_guar`` divides it by twelve, which is the notes'
simple-twelfth conversion and one of their named pitfalls. The current scale is that
rate times ``Projection.coi_curr_factor`` (65%) and the shadow scale times
``Projection.coi_sg_factor`` (55%), because no carrier publishes either **[std]**.

Both mortality tables are small illustrative ones **[std]**, *not* published tables:
the notes forbid hard-coding the licensed 2017 CSO and 2015 VBT families, so
``coi_rates.csv`` ships a Perks curve fitted to the two figures the notes state -- the
8.615 per $1,000 per month guaranteed maximum at attained age 85, and a solved level
lifetime no-lapse premium near $10,800 for the anchor cell -- and ``mort_table.csv``
ships the same curve at 72% of the guaranteed basis. To swap in a licensed basis,
replace a file with a same-schema one, or point its filename Reference at a different
name, then clear the cache. No formula changes.
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
    """Guaranteed maximum **annual** COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by sex, rate class and **attained** age.
    The monthly rate is the annual rate divided by twelve **[std]** structure; [R3]
    requires the guaranteed maxima to be stated in the policy, and [REG-R17] names the
    2017 CSO family the notes point at.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*."""
    return pd.read_csv(input_dir() / corridor_file, index_col="age")  # noqa: F821


def mort_table():
    """The best-estimate annual mortality table by attained age, read from *mort_table.csv*."""
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


def rop_table():
    """The return-of-premium exercise windows, read from *rop_table.csv*.

    One row per policy anniversary carrying a window: the refund ratio applied to
    cumulative premiums [S1] and the **[std]** exercise rate.
    """
    return pd.read_csv(input_dir() / rop_file, index_col="anniversary")  # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

surr_charge_file = "surr_charge_table.csv"

rop_file = "rop_table.csv"

pd = ("Module", "pandas")