# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.ADE_FR_S.Projection` as ``data``. :mod:`~.ADE_FR_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/assurance_emprunteur/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ADE_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ==============================  ==========================
Reference                 Cells                           File
========================  ==============================  ==========================
model_point_file          model_point_table()             model_point_table.csv
mort_table_file           mort_table()                    mort_table.csv
itt_inception_file        itt_inception_table()           itt_inception_table.csv
itt_termination_file      itt_termination_table()         itt_termination_table.csv
franchise_file            franchise_table()               franchise_table.csv
lapse_table_file          lapse_table()                   lapse_table.csv
crd_rate_file             crd_rate_table()                crd_rate_table.csv
========================  ==============================  ==========================

**There is no loan schedule file, and that is deliberate.** The *échéancier* is
deterministic given the capital, the rate and the term, so ``Projection.crd`` computes
it and ``Projection.check_crd`` asserts it closes. A pasted amortisation table is the
notes' first-listed pitfall: it cannot be checked against the roll-forward, and the whole
product hangs off the *capital restant dû*.

The decrement files are separate because they are separate objects with different
parameterizations, exactly as a real basis would publish them. Mortality and ITT
inception are keyed by **sex and pivot age** and interpolated; ITT terminations are keyed
by **claim duration year** and split three ways — recovery, transition to IPT, death in
claim — because ITT has three competing exits and a real disability basis publishes them
apart. The *franchise* factor is its own one-column file because it is a property of the
deferred period rather than of the life, and the CRD premium scale is its own file
because it is a tariff and not a decrement.

Every shipped rate table carries a ``provenance`` column saying in words that it is a
**[std]** proxy. No French decrement, incidence or termination table for this product was
retrieved: insurer rate cards are proprietary, and TH 00-02 / TF 00-02 are cited by name
but are not redistributable. A licensee replaces the files and changes no formula.
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
    """The model point table, read from *model_point_table.csv*.

    Twelve single-life cells.  Point 1 is the notes' worked example configuration; the
    others carry the two premium bases, the two indemnity bases, the two IPT benefit
    bases, a *quotité* below 1, the *franchise* menu, a cell whose ITT/IPT cover ends
    long before its loan, and one claim in payment in each of the two disabled states.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """Healthy-life annual mortality by sex and pivot age, from *mort_table.csv*.

    A **[std]** proxy.  The homologated French tables for a non-annuity contract are
    TH 00-02 / TF 00-02 with the annexed *décalage d'âge*, cited by name in the notes but
    not redistributable, so the shipped values are shaped from INSEE population data —
    the only freely redistributable French series.  Population mortality is heavier than
    medically-selected insured experience, so the proxy overstates death cost for a
    standard-risk book and understates it for a book written without medical selection.
    The female rows are 0.60 x male, a pick; one sampled insurer is unisex instead.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


def itt_inception_table():
    """ITT claim-payment inception rates, read from *itt_inception_table.csv*.

    Annual rates per life in ``healthy``, by sex and pivot age.  Shaped as a **claim
    payment** inception rate — the quantity a real disability basis publishes per
    deferred period — so a sickness spell that recovers inside the *franchise* never
    leaves ``healthy`` and no separate "sick, not yet in payment" state is needed.  The
    shipped rates are the *franchise* 90 days column; :func:`franchise_table` scales them
    to the other four.  Every value is **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / itt_inception_file,                            # noqa: F821
        index_col=["sex", "age"]).sort_index()


def itt_termination_table():
    """The three ITT exit rates by claim duration year, from *itt_termination_table.csv*.

    Annual recovery, transition-to-IPT and death-in-claim rates.  Three columns rather
    than one because ITT has three competing exits and they move in opposite directions
    with duration: recovery falls 0.55 to 0.15 across the three duration years while the
    IPT transition rises 0.02 to 0.12.  Short claims mostly recover and long claims mostly
    consolidate, which is the qualitative structure of any disability termination basis
    and the reason the in-claim population needs a duration dimension at all.  The values
    are **[std]** proxies with no French anchor.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / itt_termination_file,                          # noqa: F821
        index_col="claim_duration_year")


def franchise_table():
    """The *franchise* multipliers on the inception rate, from *franchise_table.csv*.

    Keyed by ``franchise_days`` over the sourced 30 / 60 / 90 / 120 / 180 menu.  A longer
    deferred period admits fewer spells to payment, so the factor falls 1.60 to 0.65 with
    1.00 at the 90-day pick the inception table is written on.  The menu is sourced; the
    factors are **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / franchise_file, index_col="franchise_days")    # noqa: F821


def lapse_table():
    """*Résiliation* rates by policy year, read from *lapse_table.csv*.

    The loi Lemoine substitution decrement, and the behavioural heart of the product:
    4 % in year 1, 12 % in years 2 and 3, 10 %, then a 7 % ultimate.  Materially higher
    than a classic protection lapse because the cover does not stop, it moves — the
    borrower may cancel *à tout moment* and the insurer must remind them annually.  The
    shape is a reading of the statutory mechanics rather than of data: the published
    French series are counts of substitution *requests*, not portfolio lapse rates, so
    the whole table is **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def crd_rate_table():
    """The CRD-basis premium scale by attained age, from *crd_rate_table.csv*.

    Annual rates applied to the *capital restant dû* at each policy anniversary, used
    only when ``premium_basis = capital_restant_du``.  A tariff, not a decrement, and
    **[std]**: it is calibrated so its present value over the worked-example cell matches
    the level 0.84 % *capital initial* scale to about 0.11 %.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / crd_rate_file, index_col="age")                # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

itt_inception_file = "itt_inception_table.csv"

itt_termination_file = "itt_termination_table.csv"

franchise_file = "franchise_table.csv"

lapse_table_file = "lapse_table.csv"

crd_rate_file = "crd_rate_table.csv"

pd = ("Module", "pandas")
