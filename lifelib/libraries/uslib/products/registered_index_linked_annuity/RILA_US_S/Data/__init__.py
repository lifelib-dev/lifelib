# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-contract projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.RILA_US_S.Projection` as ``data``.
:mod:`~.RILA_US_S.Projection` is parameterized by ``point_id``, so
each ``Projection[N]`` is a separate ItemSpace with its own cells cache; if the readers
lived there, every model point would re-read every file. Holding them in an
unparameterized Space reads each file once no matter how many contracts are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/registered_index_linked_annuity/``, rather than data stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RILA_US_S`` folder without its parent's CSVs produces a model that
reads and then fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
market_scenario_file       market_scenario()               market_scenario.csv
surr_charge_file           surr_charge_table()             surr_charge_table.csv
guar_min_rate_file         guar_min_rate_table()           guar_min_rate_table.csv
lapse_file                 lapse_table()                   lapse_table.csv
withdrawal_file            withdrawal_table()              withdrawal_table.csv
=========================  ==============================  ==========================

``market_scenario`` is the file peculiar to this product. A RILA's *contractual* formula
consumes market data — an index level, a Constant Maturity Treasury yield at the term's
maturity, an implied volatility and a dividend yield — so the market state is an input
class of its own alongside the contractual, declared and behavioural classes, not a
valuation overlay. It is indexed by ``(scenario_id, t)`` and read as a step function of
``t``: each row states the market state that holds from that month until the next row of
the same scenario, so the notes' Scenario A is three rows.

``withdrawal_table`` is indexed by ``(wd_schedule_id, t)`` and a month with no row takes
no scheduled withdrawal; ``surr_charge_table`` is indexed by complete contract years
``cy = 0 .. 6``; ``guar_min_rate_table`` by ``term_years``, the contractual floors on the
declared Cap, Step and Edge rates at 1, 3 and 6 years [S1][S2]; and ``lapse_table`` by
contract year, read as a step function so the notes' three-row reference shape stays
three rows.

To swap in the prescribed mortality basis — the 2012 IAM **Basic** table (VM-M §2.C) with
generational Projection Scale G2 [REG-R59], which may not be redistributed here — replace
``mort_table.csv`` with a same-schema file, or point ``mort_table_file`` at a different
name, then clear the cache. No formula changes. The same is true of the market data: a
production implementation supplies a volatility *surface* rather than the flat scalar
shipped here, and that is a change to ``market_scenario.csv`` plus a strike-and-maturity
lookup, not to the crediting or interim-value formulas.
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


def market_scenario():
    """The exogenous market-data scenarios, read from *market_scenario.csv*.

    Indexed by ``(scenario_id, t)`` and read as a step function of ``t``: each row states
    the index level, the Market Value Rate, the risk-free rate, the dividend yield and
    the implied volatility that hold from that month until the next row of the same
    scenario.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / market_scenario_file,                          # noqa: F821
        index_col=["scenario_id", "t"])


def surr_charge_table():
    """The withdrawal charge schedule by complete contract year, from *surr_charge_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_charge_file, index_col="contract_year")   # noqa: F821


def guar_min_rate_table():
    """The guaranteed minimum Cap, Step and Edge rates by term, from *guar_min_rate_table.csv*."""
    return pd.read_csv(                                              # noqa: F821
        input_dir() / guar_min_rate_file, index_col="term_years")    # noqa: F821


def lapse_table():
    """The un-shocked base annual surrender rate by contract year, from *lapse_table.csv*.

    The charge-expiry shock is not in this file: its size is the ``lapse_shock_mult``
    Reference on ``Projection`` and the year it lands in is derived from
    *surr_charge_table.csv*, so the two cannot drift apart.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="contract_year")         # noqa: F821


def withdrawal_table():
    """Scheduled gross withdrawals, read from *withdrawal_table.csv*.

    Indexed by ``(wd_schedule_id, t)``; a month with no row takes no withdrawal.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / withdrawal_file,                               # noqa: F821
        index_col=["wd_schedule_id", "t"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

market_scenario_file = "market_scenario.csv"

surr_charge_file = "surr_charge_table.csv"

guar_min_rate_file = "guar_min_rate_table.csv"

lapse_file = "lapse_table.csv"

withdrawal_file = "withdrawal_table.csv"

pd = ("Module", "pandas")