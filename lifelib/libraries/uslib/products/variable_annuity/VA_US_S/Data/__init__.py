# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.VA_US_S.Projection` as ``data``. :mod:`~.VA_US_S.Projection`
is parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_annuity/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VA_US_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
fund_file                  fund_table()                    fund_table.csv
return_scenario_file       return_scenario()               return_scenario.csv
rate_scenario_file         rate_scenario()                 rate_scenario.csv
gawa_pct_file              gawa_pct_table()                gawa_pct_table.csv
cdsc_file                  cdsc_table()                    cdsc_table.csv
transaction_file           transaction_table()             transaction_table.csv
=========================  ==============================  ==========================

Five of these carry a compound key. ``fund_table`` is indexed by ``(fund_set, sub_id)``
so one row per subaccount describes an allocation set; ``return_scenario`` by
``(scenario_id, sub_id, t)`` and ``rate_scenario`` by ``(scenario_id, t)``, both read as
step functions of ``t`` so a flat path is one row per subaccount; ``gawa_pct_table`` by
``(gawa_grid, age_from)``, read as a banded lookup on the attained age; ``cdsc_table`` by
``(cdsc_schedule, completed_years)``; and ``transaction_table`` by ``(txn_id, t)``, a
month with no row taking neither premium nor withdrawal.

The mortality table shipped here is an illustrative **[std]** annuitant curve, *not* a
published basis. The prescribed basis is the 2012 IAM **Basic** Table improved to
December 31, 2017 on Projection Scale G2 [R1][REG-R59], which may not be redistributed
here; swap it in by replacing ``mort_table.csv`` with a same-schema file, or point
``mort_table_file`` at a different name, then clear the cache. No formula changes.
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

    Inputs are *external* files, not data stored inside the model, so the model folder
    is pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*."""
    return pd.read_csv(input_dir() / model_point_file, index_col="point_id")  # noqa: F821


def mort_table():
    """Annual mortality by attained age and sex, read from *mort_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["age", "sex"])     # noqa: F821


def fund_table():
    """Subaccount allocations and fund expense ratios, from *fund_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / fund_file, index_col=["fund_set", "sub_id"])   # noqa: F821


def return_scenario():
    """Gross subaccount returns, read from *return_scenario.csv*.

    Indexed by ``(scenario_id, sub_id, t)`` and read as a step function of ``t``: each
    row states the monthly gross fund return that holds from that month until the next
    row for the same scenario and subaccount.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / return_scenario_file,                          # noqa: F821
        index_col=["scenario_id", "sub_id", "t"])


def rate_scenario():
    """The exogenous market rate series, read from *rate_scenario.csv*.

    Indexed by ``(scenario_id, t)`` and read as a step function of ``t``. It carries the
    quarterly average of daily VIX-squared driving the optional non-discretionary fee
    reset [S4][S6] and the 10-year Constant Maturity Treasury rate driving the optional
    formula-linked GMDB roll-up [S7]. Neither is used by the base run.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "t"])


def gawa_pct_table():
    """The GAWA% grid by attained age band, read from *gawa_pct_table.csv*.

    Indexed by ``(gawa_grid, age_from)``; the applicable row is the highest ``age_from``
    at or below the attained age at the first withdrawal [S3].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / gawa_pct_file, index_col=["gawa_grid", "age_from"])  # noqa: F821


def cdsc_table():
    """The withdrawal charge scale, read from *cdsc_table.csv*.

    Indexed by ``(cdsc_schedule, completed_years)``, where the key is completed years
    **since receipt of the premium being withdrawn**, not the contract year [S2].
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cdsc_file,                                     # noqa: F821
        index_col=["cdsc_schedule", "completed_years"])


def transaction_table():
    """Scheduled policyholder transactions, read from *transaction_table.csv*.

    Indexed by ``(txn_id, t)`` with a gross premium and a gross withdrawal per month; a
    month with no row takes neither. Scheduled withdrawals are **added to** the
    utilization withdrawal the base run derives from the GLWB, which is how the excess
    algebra is exercised.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / transaction_file, index_col=["txn_id", "t"])   # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

fund_file = "fund_table.csv"

return_scenario_file = "return_scenario.csv"

rate_scenario_file = "rate_scenario.csv"

gawa_pct_file = "gawa_pct_table.csv"

cdsc_file = "cdsc_table.csv"

transaction_file = "transaction_table.csv"

pd = ("Module", "pandas")