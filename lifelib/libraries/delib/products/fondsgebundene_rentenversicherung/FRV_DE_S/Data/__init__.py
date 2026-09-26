# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.FRV_DE_S.Projection` as ``data``. :mod:`~.FRV_DE_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/fondsgebundene_rentenversicherung/``, rather than data stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FRV_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ============================  ==========================
Reference                 Cells                         File
========================  ============================  ==========================
model_point_file          model_point_table()           model_point_table.csv
mort_file                 mort_table()                  mort_table.csv
lapse_file                lapse_table()                 lapse_table.csv
charge_file               charge_table()                charge_table.csv
fund_scenario_file        fund_scenario_table()         fund_scenario_table.csv
rentenfaktor_file         rentenfaktor_table()          rentenfaktor_table.csv
========================  ============================  ==========================

**Every file but ``model_point_table.csv`` carries a ``provenance`` column**, one tag per
row, and the library's conventions suite asserts it. That is this library's second
ruling: the citation discipline reaches the data files rather than stopping at the prose.
The model point table is the single exemption, because a model point is a *configuration*
— one policy's own terms — and not an assumption.

.. rubric:: The two shipped decrement proxies, and what a replacement must preserve

Nothing in this product's source corpus was retrieved, and **no charge level, lapse rate
or *Rentenfaktor* was established at any carrier**. Three of the five assumption files
are therefore standardizations end to end, and two of them stand in for tables this
library may not ship.

``mort_table.csv`` is a **[std] Gompertz-form proxy** of the *first-order* DAV 2008 T
death table::

    qx_tariff(x) = 0.00080 x 1.10^(x - 37),        ages 18 to 100

**anchored so that ``qx_tariff(37) = 0.00080`` exactly.** That single value is what the
notes' worked example rests on — it produces ``mort_rate_tariff_mth(0) = 0.00080/12`` and,
through ``mort_be_factor = 0.75``, ``mort_rate(0) = 0.00060`` — so a substitute table must
reproduce it at the anchor cell's entry age if the example is to close. What else a
replacement must preserve is the *direction* of the two bases: DAV 2008 T is a **death**
table with a first-order margin **above** best estimate, which is the opposite direction
from an annuity table, and the 10 % per year of age is an **insured-lives** gradient — a
proxy built on population mortality overstates claims at the working ages this product
lives at. DAV 2008 T is the property of the Deutsche Aktuarvereinigung, is not public and
is cited by name here rather than redistributed.

``rentenfaktor_table.csv`` is **[std] and derived, not observed**. At a *Rechnungszins*
of 0 % — the only conversion-basis statement with any corroboration anywhere in the delib
corpus, and that at one remove and for a *classic* tariff — a monthly annuity of ``R`` per
10 000 € for an expected ``T`` years has present value ``12 T R``, so::

    T_eff(x) = 100/3 - 0.75 (x - 67)            ages 60 to 75
    rentenfaktor_guar(x) = 10000 / (12 T_eff(x)) = 10000 / (400 - 9 (x - 67))

which is **exactly 25.00 at age 67**, 22.47 at 62 and 26.81 at 70. Read the other way,
25.00 prices the guarantee as though the insurer holds the capital for 33⅓ years and
earns nothing on it — the *Sicherheitsabschlag* made concrete. The ``std_2026`` row sets
the current factor equal to the guaranteed one, so the ``max(guaranteed, current)`` rule
is exercised without injecting an unsourced uplift; ``rich_current`` sets it 12 % higher
so that the ``max()`` visibly bites on one model point. The underlying table, DAV 2004 R,
is generational and is likewise cited and not shipped: a replacement must preserve a
**generational annuitant basis with a first-order margin**, which is a margin in the
*opposite* direction from the death table above.

``charge_table.csv``, ``lapse_table.csv`` and ``fund_scenario_table.csv`` are
standardizations of the same kind, each row carrying its own rationale in the
``provenance`` column. The one anchor in the charge stack is the *Höchstzillmersatz* of
25 ‰ of the *Beitragssumme*, and ``std_gross`` takes the cap rather than a guessed
interior point.
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
    """The model point table, read from *model_point_table.csv*.

    Thirteen policies indexed by ``point_id``; model point 1 is the worked example's
    anchor cell.  This is the library's one **provenance-exempt** input, because a model
    point is a configuration rather than an assumption.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The first-order annual death rates by attained age, from *mort_table.csv*.

    A **[std]** proxy of DAV 2008 T, not the table itself; see the Space docstring for
    what it is, what it is anchored on and what a replacement must preserve.  It is the
    basis of the *Risikobeitrag* the tariff charges — **not** of the projection's own
    decrement, which is this table scaled by ``mort_be_factor``, and **not** of the
    *Rentenfaktor*, which rests on an annuity table.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_file, index_col="age")                    # noqa: F821


def lapse_table():
    """The annual lapse rates by policy year, read from *lapse_table.csv*.

    The ``policy_year`` key is the **contractual 1-based label**, not the model's ``t``:
    ``Projection.lapse_rate_base(t)`` maps through ``policy_year(t) = t // 12 + 1``, so the
    file's values did not move when the frame became 0-based.

    **[std]** throughout: no German unit-linked *Stornoquote* was established anywhere.
    The front-loading in years 1 to 5 is a structural inference from the exit terms — the
    acquisition charge is being taken and the value is furthest below the premiums paid —
    and the dip in years 11 and 12 anticipates the twelve-year tax threshold, whose step
    up is applied in :mod:`~.FRV_DE_S.Projection` rather than stored here, because it
    depends on the attained age as well as the duration.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="policy_year")           # noqa: F821


def charge_table():
    """The charge scales by ``charge_id``, read from *charge_table.csv*.

    One row per tariff: the acquisition rate on the *Beitragssumme* and the months it is
    spread over, the premium-based and fund-based administration rates, the monthly
    *Stückkosten*, the *Zuzahlungskosten* rate and the *Stornoabzug* rate.  Four rows
    ship — ``std_gross``, ``std_netto``, ``std_high``, ``std_low`` — and the difference
    between the first two is the acquisition load, the parameter this library most needs
    and cannot source.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / charge_file, index_col="charge_id")            # noqa: F821


def fund_scenario_table():
    """The gross fund return and TER by scenario and policy year, from *fund_scenario_table.csv*.

    Four **[std]** deterministic paths — ``base``, ``etf``, ``zero``, ``stress``.  The
    ``policy_year`` half of the key is the contractual 1-based label, reached through
    ``policy_year(t) = t // 12 + 1``, so it is unaffected by the 0-based frame.  The
    **TER is a return item, never a policy charge**: it is borne inside the *Anteilspreis*
    and never appears in the ledger, so the projection nets it off the gross return.
    Charging it explicitly double-counts; ignoring it overstates the policyholder's return.
    Nothing here is a PRIIPs performance scenario and nothing here may be compared with
    one — those are derived from an underlying's own return history, not chosen.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / fund_scenario_file,                            # noqa: F821
        index_col=["scenario_id", "policy_year"])


def rentenfaktor_table():
    """The guaranteed and current *Rentenfaktoren* by factor id and age at *Rentenbeginn*.

    Read from *rentenfaktor_table.csv*: euro of monthly annuity per 10 000 € of
    *Fondsguthaben*.  **[std]** and derived rather than observed — see the Space
    docstring for the derivation and for what the underlying DAV 2004 R basis requires of
    a replacement.  The table is indexed by the **age at *Rentenbeginn***, not by the
    attained age in the last projected month, which is one lower.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rentenfaktor_file,                             # noqa: F821
        index_col=["factor_id", "annuity_age"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_file = "mort_table.csv"

lapse_file = "lapse_table.csv"

charge_file = "charge_table.csv"

fund_scenario_file = "fund_scenario_table.csv"

rentenfaktor_file = "rentenfaktor_table.csv"

pd = ("Module", "pandas")
