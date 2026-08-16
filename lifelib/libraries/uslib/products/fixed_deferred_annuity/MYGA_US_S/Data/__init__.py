# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.MYGA_US_S.Projection` as ``data``.
:mod:`~.MYGA_US_S.Projection` is parameterized by ``point_id``, so each
``Projection[N]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/fixed_deferred_annuity/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``MYGA_US_S`` folder without its parent's CSVs produces a model that reads
and then fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
surr_charge_file           surr_charge_table()             surr_charge_table.csv
surr_charge_age_cap_file   surr_charge_age_cap_table()     surr_charge_age_cap.csv
rate_scenario_file         rate_scenario()                 rate_scenario.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
mva_factor_file            mva_factor_table()              mva_factor_table.csv
=========================  ==============================  ==========================

Three of these carry a compound key. ``surr_charge_table`` is indexed by
``(schedule, contract_year)`` so the initial 9/8/7/6/5 schedule [S10] and the renewal
5/4/3/2/1 schedule [S2] sit in one file; ``rate_scenario`` by ``(scenario_id, t)`` and
``withdrawal_table`` by ``(wd_schedule_id, t)``, both read as step functions of ``t`` so
a scenario or a withdrawal programme is a handful of rows rather than one row per month.

To swap in a licensed mortality basis — the 2012 IAM Basic table with Projection Scale G2
and the VM-22 Table 6.7 factors that the notes prescribe and that may not be redistributed
here — replace ``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at
a different name, then clear the cache. No formula changes.
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


def surr_charge_table():
    """Surrender charge rates by schedule and contract year, from *surr_charge_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file,                              # noqa: F821
        index_col=["schedule", "contract_year"])


def surr_charge_age_cap_table():
    """The attained-age cap on the renewal surrender charge, from *surr_charge_age_cap.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_age_cap_file, index_col="age")     # noqa: F821


def rate_scenario():
    """The exogenous rate scenarios, read from *rate_scenario.csv*.

    Indexed by ``(scenario_id, t)`` and read as a step function of ``t``: each row states
    the MVA reference yield and the market competitor rate that hold from that month
    until the next row of the same scenario.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "t"])


def withdrawal_table():
    """Scheduled gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, t)``; a month with no row takes no withdrawal.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "t"])


def mva_factor_table():
    """The declared-differential MVA duration factors, from *mva_factor_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mva_factor_file, index_col="years_remaining")  # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

surr_charge_file = "surr_charge_table.csv"

surr_charge_age_cap_file = "surr_charge_age_cap.csv"

rate_scenario_file = "rate_scenario.csv"

withdrawal_file = "withdrawal_table.csv"

mva_factor_file = "mva_factor_table.csv"

pd = ("Module", "pandas")