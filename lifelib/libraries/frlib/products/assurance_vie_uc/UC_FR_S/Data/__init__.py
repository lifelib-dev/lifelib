# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.UC_FR_S.Projection` as ``data``. :mod:`~.UC_FR_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells cache;
if the readers lived there, every model point would re-read every file. Holding them in
an unparameterized Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/assurance_vie_uc/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``UC_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
lapse_table_file           lapse_table()                   lapse_table.csv
plancher_rate_table_file   plancher_rate_table()           plancher_rate_table.csv
uc_scenario_table_file     uc_scenario_table()             uc_scenario_table.csv
=========================  ==============================  ==========================

Note what is **not** an input file. The charge rates — the premium charge, the UC
management charge, the arbitrage fee, the euro credited rate — and every attribute of the
`garantie plancher` except its tariff are **model point columns** rather than rate
tables, because they are per-policy contractual and discretionary parameters rather than
experience assumptions. Art. A. 132-8 requires charge *maxima* to be disclosed, not
levels to be capped, and the retrieved contracts span 0.475% to 1.50% on the same charge
line, so a single shipped rate card would assert a market fact that does not exist.

The plancher tariff is the exception and is a table, because it is the one price on this
product that an insurer publishes: `plancher_rate_table.csv` is Spirica's own schedule,
an annual premium per 10,000 € of `capital sous risque` by attained age, ages 12 to 74.
It stops at 74 because the cover stops at 75; a model that extrapolated it would silently
invent a price, which is why :func:`~.UC_FR_S.Projection.plancher_rate` raises rather
than extends.
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
    """The base annual mortality rates by sex and age, from *mort_table.csv*.

    A **[std]** proxy shaped like the INSEE national series, the only freely
    redistributable French mortality data.  Art. A. 335-1 permits only a table
    homologated by ministerial arrete - by sex, on INSEE data for a non-annuity contract
    - or an undertaking's own experience table certified by an independent actuary, so
    TH 00-02 / TF 00-02 are cited by name and article in the documents and are **not
    shipped**.

    The table is anchored so that ``Projection.mort_be_factor`` times the male rate at
    age 65 reproduces the technical notes' placeholder ``q = 1.20% p.a.`` exactly.  That
    placeholder is *not* the mortality implied by the plancher tariff: 196 EUR a year per
    10,000 EUR of capital sous risque at age 65 is 1.96% of the net amount at risk, and
    no insurer publishes the split between mortality, expense loading and margin, so the
    tariff cannot be decomposed.  The model carries the tariff as a **price** and the
    mortality as an **assumption**, and the difference between them is the rider's
    expected margin.  Sorted on read, because ``Projection.mort_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


def lapse_table():
    """The base annual total-surrender rates by policy year, from *lapse_table.csv*.

    2% in year 1, 4% in years 2 to 4, 6% in years 5 to 7, **12% in year 8** and 6%
    thereafter.  A **[std]** construction: no public French persistency study was
    retrieved, and no insurer document gives a lapse table.

    The year-8 spike is the one shape that is not arbitrary.  Art. 125-0 A CGI makes the
    eighth anniversary the point at which the withholding rate falls to 7.5% and the
    4,600 EUR / 9,200 EUR annual abattement opens, and eight years is the recommended
    holding period printed in both retrieved key-information documents.  A model with no
    duration-8 spike has ignored the single strongest driver of French surrender timing.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")      # noqa: F821


def plancher_rate_table():
    """The garantie plancher tariff by attained age, from *plancher_rate_table.csv*.

    An annual premium per 10,000 EUR of `capital sous risque`, ages 12 to 74: Spirica's
    published schedule, the only tariff retrieved together with an explicit premium
    formula, ``Pr = K x (PA / 10 000) x 1/52``.  It is a **price**, not a decrement, and
    it is the only sourced quantitative table this model ships.

    The table stops at 74 because the cover stops at the 75th birthday.
    ``Projection.plancher_rate`` returns zero once the cover has ceased and raises if an
    attained age inside the cover falls outside the table, rather than extrapolating:
    extending the cessation age past 75 needs a tariff the sources do not contain.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / plancher_rate_table_file, index_col="age")      # noqa: F821


def uc_scenario_table():
    """The UC liquidation-value scenarios, from *uc_scenario_table.csv*.

    Each row is a **segment** of one scenario: a monthly return applying from
    ``from_month`` to ``to_month`` inclusive.  Both bounds are written in the projection's
    own **0-based** policy months, so the first segment of every scenario opens at
    ``from_month = 0`` and ``Projection.uc_return_mth`` compares them against ``t``
    directly.  Three scenarios ship, all **[std]**:
    ``stress_yr1``, the worked example's path of +1.00% a month for six months then
    -5.00% a month for six; ``base_490``, a deterministic 4.90% a year, the five-year
    average performance of UC supports net of fund charges; and ``bear_5pct``, a
    sustained -5.00% a year that holds the plancher in the money.

    The path is **exogenous** and the base run is deterministic, which understates the
    plancher cost: ``E[max(0, F - AV)]`` exceeds ``max(0, F - E[AV])``, so a stochastic
    or scenario-set run is not an enhancement here but the only way to price the rider.
    Fund-level recurring costs, an ``encours``-weighted 1.60% a year, are inside these
    returns and accrue to the fund manager rather than to the insurer.  Sorted on read,
    because ``Projection.uc_return_mth`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / uc_scenario_table_file,                         # noqa: F821
        index_col="scenario_id").sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

plancher_rate_table_file = "plancher_rate_table.csv"

uc_scenario_table_file = "uc_scenario_table.csv"

pd = ("Module", "pandas")
