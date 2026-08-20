# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.FIA_US_S.Projection` as ``data``.
:mod:`~.FIA_US_S.Projection` is parameterized by ``point_id``, so each
``Projection[N]`` is a separate ItemSpace with its own cells cache; if the readers lived
there, every model point would re-read every file. Holding them in an unparameterized
Space reads each file once no matter how many contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/fixed_indexed_annuity/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FIA_US_S`` folder without its parent's CSVs produces a model that reads
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
rollup_file                rollup_table()                  rollup_table.csv
payout_rate_file           payout_rate_table()             payout_rate_table.csv
rate_scenario_file         rate_scenario()                 rate_scenario.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
=========================  ==============================  ==========================

Three of these are read as **step functions**, so a schedule is a handful of rows rather
than one row per contract year. ``rollup_table`` is indexed by
``(rollup_id, contract_year)`` and each row states the guaranteed simple rollup rate that
holds from its own contract year until the next row of the same schedule, which turns the
blended 5.00%/2.00%/0% [S2] and the flat 3.00%/0% [S9] designs into three rows and two.
``rate_scenario`` is indexed by ``(scenario_id, t)`` and carries the index level ``I(t)``
and the MVA reference yield ``i_t``; the projection differences consecutive levels into
``R(t) = I(t)/I(t-1) - 1``, so holding a level flat is how a scenario says "no index
credit this year". ``withdrawal_table`` is indexed by ``(wd_schedule_id, t)`` and is
*not* a step function — an anniversary with no row simply takes no ad hoc withdrawal.

``surr_charge_table`` carries **two** contract-year vectors in one file, the surrender
charge percentage and the bonus vesting percentage, because [S5] supplies them as a
single schedule pair and both are read at the same key. ``payout_rate_table`` is banded
rather than keyed: each row gives an inclusive attained-age band and the single-life and
joint-life percentages, the joint column being the single column less 0.50% [S1][S3].

To swap in the prescribed annuitant mortality — the 2012 IAM/IAR family with Projection
Scale G2 [REG-R59][REG-R60], which may not be redistributed here — replace
``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a different
name, then clear the cache. No formula changes. The shipped table is the same
illustrative Makeham annuitant curve as ``products/fixed_deferred_annuity``, so the two
annuity models sit on one mortality basis.
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
    """Surrender charge and bonus vesting percentages by contract year [S5].

    Read from *surr_charge_table.csv*.  One file because [S5] states the two vectors as
    a single contract-year schedule pair, read at the same key.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="contract_year")   # noqa: F821


def rollup_table():
    """The guaranteed simple rollup schedules, read from *rollup_table.csv*.

    Indexed by ``(rollup_id, contract_year)`` and read as a step function of the contract
    year: each row states the rate that holds from its own year until the next row of the
    same schedule.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rollup_file,                                   # noqa: F821
        index_col=["rollup_id", "contract_year"])


def payout_rate_table():
    """The lifetime withdrawal percentage bands, read from *payout_rate_table.csv*.

    Banded rather than keyed: each row gives an inclusive attained-age band with the
    single-life and joint-life percentages [S3].
    """
    return pd.read_csv(input_dir() / payout_rate_file)               # noqa: F821


def rate_scenario():
    """The exogenous scenarios, read from *rate_scenario.csv*.

    Indexed by ``(scenario_id, t)`` and read as a step function of ``t``: each row states
    the index level and the MVA reference yield that hold from that anniversary until the
    next row of the same scenario.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rate_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "t"])


def withdrawal_table():
    """Scheduled ad hoc gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, t)``; an anniversary with no row takes no ad hoc
    withdrawal.  Lifetime withdrawals are *not* scheduled here — they are generated by
    the rider from ``utilization_intensity`` and the locked payout percentage.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "t"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

surr_charge_file = "surr_charge_table.csv"

rollup_file = "rollup_table.csv"

payout_rate_file = "payout_rate_table.csv"

rate_scenario_file = "rate_scenario.csv"

withdrawal_file = "withdrawal_table.csv"

pd = ("Module", "pandas")