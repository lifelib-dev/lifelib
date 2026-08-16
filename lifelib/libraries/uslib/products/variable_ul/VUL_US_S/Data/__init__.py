# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The ten input CSVs are read here, **once per model**, and referenced from
:mod:`~.VUL_US_S.Projection` as ``data``. :mod:`~.VUL_US_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/variable_ul/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas -- no ``_data/``, no IOSpec, no embedded values --
so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VUL_US_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

======================  ============================  ==============================
Reference               Cells                         File
======================  ============================  ==============================
model_point_file        model_point_table()           model_point_table.csv
subaccount_file         subaccount_table()            subaccount_table.csv
scenario_file           scenario_table()              scenario_table.csv
coi_rates_file          coi_rates()                   coi_rates.csv
corridor_file           corridor_factors()            corridor_factors.csv
mort_table_file         mort_table()                  mort_table.csv
class_factor_file       class_factor_table()          class_factor_table.csv
lapse_table_file        lapse_table()                 lapse_table.csv
prem_persistency_file   prem_persistency_table()      prem_persistency.csv
surr_charge_file        surr_charge_table()           surr_charge_table.csv
======================  ============================  ==============================

Two of these carry the assumptions the technical notes rank first among this product's
sensitivities, and both are standardizations.

``scenario_table.csv`` is the **separate-account return scenario**: monthly *gross*
subaccount returns keyed by ``scenario_id``, ``subaccount_id`` and policy month ``t``,
with the last month of a scenario repeating for the rest of the projection. Fund
expenses and the M&E charge are applied on top of these in
:func:`~.VUL_US_S.Projection.inv_return_mth`, so the table holds gross returns only.
A stochastic set is a data change -- more ``scenario_id`` values -- not a formula
change. The shipped scenarios are deterministic: ``WE`` is the worked example's month
(+1.00% equity, -0.50% bond) followed by a level 6% a year gross path, and ``LEVEL6``
is that level path throughout.

``coi_rates.csv`` carries the **guaranteed maximum** monthly rate per $1,000 of net
amount at risk; the current scale is that times
``Projection.coi_curr_factor``, or the model point's ``coi_rate_override``. The notes
require the 2017 CSO ultimate ANB table for the guaranteed maximum and the 2015 VBT for
best-estimate mortality; both are licensed and may not be reproduced here, so
``coi_rates.csv`` and ``mort_table.csv`` ship small illustrative **[std]** tables
instead -- the COI scale anchored on the one disclosed guaranteed point in the notes
(male 45 standard non-tobacco, policy year 1 = $0.22 [S4]) and the mortality table well
below it, because the notes insist the COI *charge* basis and the death *decrement*
basis must never be conflated. To swap in a licensed basis, replace either file with a
same-schema one, or point ``mort_table_file`` at a different name, then clear the
cache. No formula changes.
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


def subaccount_table():
    """The separate-account subaccount lineup, read from *subaccount_table.csv*.

    One row per subaccount, giving its name and its annual fund operating expense
    ratio.  The two-subaccount lineup is a **[std]** collapse of the observed menus.
    """
    return pd.read_csv(input_dir() / subaccount_file, index_col="subaccount_id")  # noqa: F821


def scenario_table():
    """Monthly gross subaccount returns, read from *scenario_table.csv*.

    Keyed by ``scenario_id``, ``subaccount_id`` and policy month ``t``.  Returns are
    **gross**: fund expenses and the M&E charge are applied on top of them in the
    projection, so a table row is the fund's own return before any charge.  The index
    is sorted on read so partial slices of the three-level key are lexsorted.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / scenario_file,                                 # noqa: F821
        index_col=["scenario_id", "subaccount_id", "t"]).sort_index()


def coi_rates():
    """Guaranteed maximum monthly COI rates, read from *coi_rates.csv*.

    Per $1,000 of net amount at risk, keyed by issue-age cell and policy year.  An
    illustrative **[std]** stand-in for the licensed 2017 CSO ultimate ANB table.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / coi_rates_file,                                # noqa: F821
        index_col=["sex", "rate_class", "age_at_entry", "policy_year"])


def corridor_factors():
    """The GPT corridor factor table by attained age, read from *corridor_factors.csv*."""
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


def prem_persistency_table():
    """Premium persistency (paid/planned) by policy year, read from *prem_persistency.csv*."""
    return pd.read_csv(input_dir() / prem_persistency_file, index_col="policy_year")  # noqa: F821


def surr_charge_table():
    """The surrender charge schedules, read from *surr_charge_table.csv*.

    One row per ``surr_charge_id``, giving the initial charge per $1,000 of initial
    face and the number of policy years over which it runs off linearly.
    """
    return pd.read_csv(input_dir() / surr_charge_file, index_col="surr_charge_id")  # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

subaccount_file = "subaccount_table.csv"

scenario_file = "scenario_table.csv"

coi_rates_file = "coi_rates.csv"

corridor_file = "corridor_factors.csv"

mort_table_file = "mort_table.csv"

class_factor_file = "class_factor_table.csv"

lapse_table_file = "lapse_table.csv"

prem_persistency_file = "prem_persistency.csv"

surr_charge_file = "surr_charge_table.csv"

pd = ("Module", "pandas")