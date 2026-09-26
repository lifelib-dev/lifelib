# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.Basis_DE_S.Projection` as ``data``. :mod:`~.Basis_DE_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/basisrente/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only, and an input can be edited or swapped
without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Basis_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_table_file            mort_table()                    mort_table.csv
surplus_file               surplus_table()                 surplus_table.csv
rentenfaktor_file          rentenfaktor_table()            rentenfaktor_table.csv
charge_file                charge_table()                  charge_table.csv
behaviour_file             behaviour_table()               behaviour_table.csv
option_file                option_table()                  option_table.csv
=========================  ==============================  ==========================

**Every file but ``model_point_table.csv`` carries a final ``provenance`` column**, one
tag per row — delib's second ruling, asserted by the conventions suite. A model point is
a *configuration* rather than an assumption, which is why it is the single exemption.

.. rubric:: The mortality table is a [std] proxy, and here is its anchor

``mort_table.csv`` is **not** DAV 2004 R. **DAV 2004 R is the property of the Deutsche
Aktuarvereinigung, is not public, and is not redistributed here**; it is cited by name in
``sources.md`` and in the technical notes, and what ships instead is a shaped proxy:

    ``qx(age) = min(1.0, 0.014000 x 1.085^(age - 67))`` over ages 20 to 121,
    with ``qx(121) = 1.0`` and a flat improvement ``trend = 0.015`` at every age
    applied from ``mort_base_year = 2005``.

**The anchor a replacement must preserve is ``qx(67) = 0.014000`` exactly**, because the
notes' worked example converts at attained age 67 and every figure in the payout phase of
that example is struck off it. A replacement must also preserve three structural
properties, or the model stops being a model of this product:

* it must be **generational** — DAV 2004 R is a *Generationentafel*, with the improvement
  inside the table rather than applied on top of it, which is why ``mort_rate_at_age``
  takes a calendar year as well as an age and why ``cal_year(t)`` is carried at all;
* it must be **first order**, carrying the DAV's prudential margins, because the
  guaranteed *Rentenfaktor* is struck on that basis and the projection's own
  ``mort_be_factor`` steps down from it to a best estimate;
* it must run to a terminal age at which ``qx`` is 1.0, because ``proj_len()`` is derived
  from the last age in this file and the projection has no tail state.

The 1.085 slope and the 1.5 % flat trend are **[std]** with nothing behind them: DAV
2004 R's own trends are age-dependent, and no Basisrente-specific decrement evidence
exists anywhere in the delib corpus.

.. rubric:: What the other six files are

``surplus_table.csv`` is the insurer's discretionary path in the *Aufschubphase* and the
*Rentenphase*, keyed on the projection index ``t`` itself, **0-based** like the frame:
``decl_rate`` is the declared *laufende Verzinsung*, which in German
practice is the **total** credited rate including the *Rechnungszins* and not a spread
over it, and ``ann_bonus_rate`` is the *Überschussrente* uplift. It is a scenario, not a
forecast, and the base path is set above the 1,00 % *Höchstrechnungszins* so the
guarantee does not bind on the anchor.

``rentenfaktor_table.csv`` is the *aktueller Rentenfaktor* by conversion age and
scenario, in euro of monthly annuity per 10 000 € of capital. No *Rentenfaktor* level,
range or time series exists anywhere in the delib corpus, so both this table and the
guaranteed factors on the model points are **[std]**; the ``low`` scenario exists so that
model point 13 exercises the other branch of ``max(garantiert, aktuell)``.

``charge_table.csv`` holds one row per tariff: the four charges struck against the
policyholder's *Deckungskapital* (the *Zillmerung* rate, the premium charge β, the
reserve charge γ and the *Stückkosten*), the *Schlussüberschussanteil* rate, and the
insurer's own expense and commission scale. Two tariffs ship, differing only in
``zill_rate``: 25 ‰ of the *Beitragssumme* for business written from 1 January 2015 and
40 ‰ for the pre-LVRG in-force cohorts.

``behaviour_table.csv`` holds the two behavioural assumptions that vary by duration —
the *Beitragsfreistellung* rate and the *Zuzahlung* take-up. **Its ``dur`` index is the
policy year, ``duration(t) + 1``**, so the notes' "durations 1–5" reads off the file
directly; ``duration(t)`` itself is completed policy years and is 0 in the first year.

``option_table.csv`` holds one multiplicative factor per contractual option:
``prem_mode`` is the *Ratenzahlungszuschlag* applied to the *laufender Beitrag* alone,
and ``guarantee_period`` and ``survivor`` are reductions in the *Rentenfaktor*, because a
German tariff pays for those covers out of the annuity rather than by scaling the death
benefit.

``model_point_table.csv`` is the thirteen policies, indexed by ``point_id``, which is
:mod:`~.Basis_DE_S.Projection`'s only parameter.
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

    Inputs are *external* files, not data stored inside the model, so the model folder is
    pure formulas.  The path is resolved at run time from where the model was read,
    following ``annuallife.TradLife_A``.
    """
    return _model.path.parent                                        # noqa: F821


def model_point_table():
    """The model point table, read from *model_point_table.csv*.

    Indexed by ``point_id``.  The single input file exempt from delib's provenance rule:
    a model point is a configuration — one policy's own terms — rather than an
    assumption.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The first-order annual death rates and improvement trends by age.

    Read from *mort_table.csv*, indexed by ``age``: ``qx`` is the rate at the base
    calendar year ``mort_base_year`` and ``trend`` the annual improvement that makes the
    basis generational.  A **[std]** proxy anchored at ``qx(67) = 0.014000``, not DAV
    2004 R; see the Space docstring for what a replacement must preserve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col="age")              # noqa: F821


def surplus_table():
    """The declared surplus path by scenario and projection year.

    Read from *surplus_table.csv*, indexed by ``scenario_id`` and the **0-based**
    projection year ``t``, whose first row is ``t = 0``: ``decl_rate`` is
    the declared *laufende Verzinsung* in the *Aufschubphase* — the **total** credited
    rate including the *Rechnungszins*, not a spread over it — and ``ann_bonus_rate`` the
    *Überschussrente* uplift in the *Rentenphase*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surplus_file,                                  # noqa: F821
        index_col=["scenario_id", "t"])


def rentenfaktor_table():
    """The *aktueller Rentenfaktor* by scenario and conversion age.

    Read from *rentenfaktor_table.csv*, indexed by ``rf_scenario_id`` and ``age``:
    ``rf_curr`` is euro of monthly annuity per 10 000 € of capital at *Rentenbeginn*.
    Entirely **[std]** — no *Rentenfaktor* level, range or time series exists anywhere in
    the delib corpus.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / rentenfaktor_file,                             # noqa: F821
        index_col=["rf_scenario_id", "age"])


def charge_table():
    """The charge, expense and commission scale by tariff, from *charge_table.csv*.

    Indexed by ``tariff_id``.  The first four columns are deductions from the
    policyholder's *Deckungskapital* and are therefore insurer **income**; the last five
    are the insurer's own **outgo**.  Booking a charge as both is the fourth listed
    modeling pitfall, and keeping the two groups in one file is what makes the split
    visible.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / charge_file, index_col="tariff_id")            # noqa: F821


def behaviour_table():
    """The duration-varying behavioural assumptions, from *behaviour_table.csv*.

    Indexed by ``beh_table_id`` and ``dur``, where **``dur`` is the policy year**,
    ``duration(t) + 1``.  ``bf_rate`` is the *Beitragsfreistellung* rate — the product's
    only behavioural exit, and not a lapse — and ``zuz_take_up`` the utilisation rate of
    the *Zuzahlung*, which is paid out of a profit not known until the year end and is
    therefore behavioural rather than contractual.  Both are **[std]** with no calibration
    evidence of any kind.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / behaviour_file,                                # noqa: F821
        index_col=["beh_table_id", "dur"])


def option_table():
    """One multiplicative factor per contractual option, from *option_table.csv*.

    Indexed by ``option_id`` and ``option_key``.  ``prem_mode`` gives the
    *Ratenzahlungszuschlag*, which multiplies the *laufender Beitrag* and nothing else;
    ``guarantee_period`` and ``survivor`` give the reduction in the *Rentenfaktor* that
    pays for a *Rentengarantiezeit* and a *Hinterbliebenenrente*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / option_file,                                   # noqa: F821
        index_col=["option_id", "option_key"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

surplus_file = "surplus_table.csv"

rentenfaktor_file = "rentenfaktor_table.csv"

charge_file = "charge_table.csv"

behaviour_file = "behaviour_table.csv"

option_file = "option_table.csv"

pd = ("Module", "pandas")
