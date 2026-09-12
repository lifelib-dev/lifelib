# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.Obseques_FR_S.Projection` as ``data``. :mod:`~.Obseques_FR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/obseques/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Obseques_FR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
mort_table_file         mort_table()                    mort_table.csv
select_table_file       select_table()                  select_table.csv
lapse_table_file        lapse_table()                   lapse_table.csv
surr_scale_file         surr_scale_table()              surr_scale_table.csv
single_prem_file        single_prem_table()             single_prem_table.csv
======================  ==============================  ==========================

Two of those tables are the reason this product needs six files where the UK sibling
needs three. The **surrender-value scale** is an input rather than a formula: the
contract makes the surrender value the *provision mathematique*, a production model
computes that prospectively on the tariff basis, and **no French insurer publishes its
tariff basis** — the whole retrieved set contains one technical rate with a table and one
rate alone. What every insurer does publish, since 1 July 2025, is a standardised table
of surrender values by duration for a 5000 EUR capital, so the model reads that scale and
interpolates it. The **single-premium scale** is the second: it prices the *prime unique*
form and, serving twice, turns a mathematical provision into a *valeur de reduction* when
a policy is made paid-up.

Every rate in these files is **[std]**, and each file carries a ``provenance`` column
saying which rows are transcribed anchors and which are constructions. The mortality
proxy is the case that matters most: TH 00-02 and TF 00-02 are the homologated regulatory
tables for this product, they are cited by name and never redistributed here, and the
shipped rates are an INSEE-shaped Gompertz proxy anchored at ``q(M, 50) = 0.0040`` so
that the anchor cell reproduces the technical notes' own placeholder rate exactly.
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

    Twelve single-policy points.  **Point 1 is the worked-example cell** RefOBS-VIA;
    points 2 and 3 are the other two premium forms; the rest are the documented
    variations - the premium-linked revalorisation, *reduction* at 50 %, the doubled
    accidental benefit with a surrender penalty, a second insurer's *viagere* rate card,
    an entry-70 cell, a 25-year temporary, a cessation age of 80, simple revalorisation
    and monthly instalments.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The annual base mortality rates, read from *mort_table.csv*.

    Keyed by sex and attained age 18-112 on the *difference de millesime* basis, and
    capped at 1.  A **[std]** proxy, not a published table: TH 00-02 and TF 00-02 are the
    homologated regulatory tables here and are cited by name and never redistributed, so
    the shipped rates are an INSEE-shaped Gompertz series anchored at
    ``q(M, 50) = 0.0040`` with 9 % p.a. age progression - which is the technical notes'
    walk-through basis exactly - and the female rates are a flat 0.60 factor on it.  The
    ``provenance`` column says which row is the anchor and which are constructions.
    Sorted on read, because ``Projection.mort_rate_base`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"]).sort_index()


def select_table():
    """The select uplift on base mortality by policy year, from *select_table.csv*.

    The anti-selection excess of a guaranteed-issue book, and it is **not flat in
    duration**: acceptance is guaranteed, no medical questionnaire and no examination, so
    the pool cannot be better than the population and self-selects worse, and the excess
    sits at short durations and decays as the anti-selected cohort dies out.  The
    first-year factor is the largest even though a first-year illness death costs only a
    refund - the deaths still happen, they merely cost less, and moving the excess to
    year 2 would double-count the protection the waiting period already gives.  Policy
    years beyond the table take its last row.  **[std]** throughout: the magnitude has no
    public calibration of any kind.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / select_table_file,                             # noqa: F821
        index_col="policy_year").sort_index()


def lapse_table():
    """The annual premium-stop rates by policy year, from *lapse_table.csv*.

    Declining with duration, on the reasoning that a small-premium *prevoyance* contract
    bought for one purpose is stopped early or not at all, reinforced by a surrender value
    worth far less than the premiums paid for decades.  Policy years beyond the table take
    its last row.  A **[std]** drafting construction: no public French source gives any
    lapse, surrender or paid-up rate for this product, and on a contract whose surrender
    value is a real cash flow this rate moves the liability in both directions at once.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col="policy_year").sort_index()


def surr_scale_table():
    """The surrender-value scales, read from *surr_scale_table.csv*.

    Keyed by scale name and **elapsed months from issue** - 0 at issue, 60 at five years -
    in EUR per 5000 EUR of guaranteed capital.  That key is a duration, not the
    projection's 0-based month index: it does not move with the frame, and
    ``Projection.surr_scale_pp`` reads it at ``duration_mth(t) + 1``, the months elapsed by
    the end of month ``t``, when a surrender resolves.
    Each scale is transcribed from one insurer's *tableau d'exemples normalises* - the
    standardised comparison table every French funeral insurer has published since
    1 July 2025 - so premium, revalorisation rate and surrender scale within a scale come
    from the same document and are mutually consistent.  Feeding one insurer's premium
    into another's scale produces plausible-looking and wrong margins: the lifetime
    premium for the same capital and age spans roughly 2:1 across the retrieved set.

    The published anchors are quinquennial; ``Projection.surr_scale_pp`` interpolates
    linearly in elapsed months between them **[std]** and holds the scale flat beyond the
    last one.  The month-0 anchor is 0 on every periodic-premium scale and a linear
    back-extrapolation of the first two published anchors on the single-premium scale
    **[std]**, since a *prime unique* contract surrendered at once returns a provision
    rather than nothing.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surr_scale_file,                               # noqa: F821
        index_col=["scale", "month"]).sort_index()


def single_prem_table():
    """u(x): the single premium per 1 EUR of whole-life capital, from *single_prem_table.csv*.

    Keyed by attained age.  Anchored on the published *prime unique* rate card - 0.854808
    at 50, 0.909720 at 60 and 0.963912 at 70, from 4274.04 / 4548.60 / 4819.56 EUR per
    5000 EUR of capital - then interpolated between the anchors and extrapolated outside
    them **[std]**, clipped to [0.30, 1.00].  It serves twice: it is the tariff behind the
    *prime unique* premium form, and it is what turns a mathematical provision into a
    *valeur de reduction* when a policy stops paying and is made paid-up.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / single_prem_file,                              # noqa: F821
        index_col="age").sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

select_table_file = "select_table.csv"

lapse_table_file = "lapse_table.csv"

surr_scale_file = "surr_scale_table.csv"

single_prem_file = "single_prem_table.csv"

pd = ("Module", "pandas")
