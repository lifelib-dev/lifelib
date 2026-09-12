# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The five input CSVs are read here, **once per model**, and referenced from
:mod:`~.PER_FR_S.Projection` as ``data``. :mod:`~.PER_FR_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/per_assurance/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``PER_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        model_point_table()             model_point_table.csv
allocation_grid_file    allocation_grid()               allocation_grid.csv
mort_table_file         mort_table()                    mort_table.csv
exit_table_file         exit_table()                    exit_table.csv
annuity_factor_file     annuity_factor_table()          annuity_factor.csv
======================  ==============================  ==========================

Four of the five carry a compound key, because every one of them is a *ladder* rather
than a single number. ``allocation_grid`` is indexed by
(``allocation_profile``, ``years_to_horizon``) so the four qualified profiles of the
de-risking arrêté sit in one file and an insurer ladder finer than the four regulatory
bands substitutes without touching a formula; ``mort_table`` by (``sex``, ``age``);
``exit_table`` by (``compartment``, ``duration``), because compartment 3 is closed to the
main-residence early-release case and therefore does not carry the same decrement as
compartments 1 and 2; and ``annuity_factor_table`` by (``sex``, ``age``).

**The glide path being a file is the point of the file list.** It is the product's
dominant financial lever — moving the *équilibré* grid to the *prudent* one replaces most
of a 5.00% UC return with a 3.38% euro return over the anchor cell's twelve years — and
the regulatory grid is a *minimum* that insurers may sit above and restate unilaterally.
A published grid is a snapshot, so it belongs in a table a reader can edit and diff, not
in a chain of ``if`` statements.

**What is not in a file, and why.** The charge levels — the entry loading, the two
management charges, the arbitrage rate, the *frais d'arrérages* — are ``Projection``
References rather than table columns. The *encadré* requires maxima to be disclosed and
caps nothing, so a charge level is never a contractual constant, and the sampled range is
wide: entry loadings from 0% to 4.80%, euro management charges from 0.50% to 2.30%. Every
adopted level is a standardization, and putting them where a reader trips over them is
better than filing them in a table that looks like data.

To swap in a licensed basis — TH 00-02 / TF 00-02 for the death benefit during
accumulation, or the generational TGH05 / TGF05 for the annuity conversion, neither of
which is redistributed here — replace ``mort_table.csv`` or ``annuity_factor.csv`` with a
same-schema file, or point ``mort_table_file`` / ``annuity_factor_file`` at a different
name, then clear the cache. No formula changes.
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


def allocation_grid():
    """The *gestion pilotée par horizon* glide path, from *allocation_grid.csv*.

    Indexed by (``allocation_profile``, ``years_to_horizon``), with an ``euro_share``
    and a ``uc_share`` column.  The four qualified profiles of the de-risking arrêté are
    shipped at their regulatory minimum — the *équilibré* ladder is 0 / 20 / 50 / 70% in
    the low-risk bucket as the horizon closes — because in this market the regulatory
    grid is not a floor insurers beat; it is the product.  ``dynamique`` and ``offensif``
    are shipped **identical**, which is what the arrêté says rather than an oversight.

    The band edges are a **[std]** convention: the tighter minimum applies at a boundary,
    so ``k = 10`` reads 20% and not 0%.  Sorted on read, because
    ``Projection.alloc_euro`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / allocation_grid_file,                          # noqa: F821
        index_col=["allocation_profile", "years_to_horizon"]).sort_index()


def mort_table():
    """The base annual mortality rates by sex and age, from *mort_table.csv*.

    A **[std]** proxy shaped on French population mortality, which through INSEE is the
    only freely redistributable French mortality data.  The homologated tables that
    actually govern the death benefit during accumulation — TH 00-02 and TF 00-02, and
    the *décalage d'âge* age shifts annexed with them — are cited and **not shipped**.

    The *level* is anchored, not measured: the whole table is scaled by one constant so
    that ``Projection.mort_be_factor`` times ``q(M, 52)`` reproduces the technical notes'
    flat 0.00500 placeholder exactly, which is what makes the worked example close on
    either mortality basis.  That places the table above French population mortality,
    because the placeholder is above it.  Sorted on read, because
    ``Projection.mort_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"]).sort_index()


def exit_table():
    """The two accumulation-phase exit decrements, from *exit_table.csv*.

    Indexed by (``compartment``, ``duration``), with an ``early_release_rate`` and a
    ``transfer_out_rate`` column.  The ``duration`` key is the plan's own *ancienneté*
    year and is **1-based**: its first row is the plan's first year, so
    ``Projection.early_release_rate`` keys it with ``plan_year(t)`` — the 1-based label —
    and not with the 0-based ``duration(t)``.

    **Neither is a lapse rate** and the file deliberately does not use the word: the plan
    carries no surrender right, and these are a *déblocage anticipé* on one of the seven
    statutory cases and a transfer of acquired rights to another PER.

    Both are **[std]**.  The one citable anchor is an aggregate — early releases and
    transfers together were €1 651 m against €63.0 bn of accumulation-phase provisions in
    2024, i.e. 2.62% — which the shipped split of 1.60% / 1.00% reproduces to 2.60%.  Two
    caveats travel with it: it is an *amount* ratio adopted as a *policy* decrement rate,
    and it is contaminated by a book growing 18.7% a year, so it is not a steady-state
    rate.

    The compartment key earns its place.  Compartment 3 is excluded from the
    main-residence limb of L. 224-4, which is the only discretionary case of the seven,
    so it carries a lower early-release rate; the transfer rate does not vary by
    compartment, because a transfer moves the rights without changing them.  Sorted on
    read, because ``Projection.early_release_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / exit_table_file,                               # noqa: F821
        index_col=["compartment", "duration"]).sort_index()


def annuity_factor_table():
    """The annuity conversion factors by sex and age, from *annuity_factor.csv*.

    A **[std]** placeholder ladder anchored at 22.0000 for a male aged 64 — annual in
    arrears, no reversion — which is the figure the technical notes' worked example uses.
    No sampled insurer publishes an annuity rate card: the contracts say only "la table
    de mortalité en vigueur" and "le taux d'intérêt technique en vigueur", and the
    homologated generational TGH05 / TGF05 are cited and not shipped.

    At the 0% technical rate a PER tariff is capped at, the factor is an **undiscounted
    expected-instalment count** rather than a discounted annuity factor — so this file
    holds a number of payments, and applying any discount to it would be a second,
    unauthorised technical rate.  Sorted on read, because
    ``Projection.annuity_factor`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / annuity_factor_file,                           # noqa: F821
        index_col=["sex", "age"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

allocation_grid_file = "allocation_grid.csv"

mort_table_file = "mort_table.csv"

exit_table_file = "exit_table.csv"

annuity_factor_file = "annuity_factor.csv"

pd = ("Module", "pandas")
