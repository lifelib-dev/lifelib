# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The four input CSVs are read here, **once per model**, and referenced from
:mod:`~.Euro_FR_S.Projection` as ``data``. :mod:`~.Euro_FR_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/assurance_vie_euro/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Euro_FR_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        model_point_table()         model_point_table.csv
mort_table_file         mort_table()                mort_table.csv
lapse_table_file        lapse_table()               lapse_table.csv
fin_rate_file           fin_rate_table()            fin_rate_table.csv
======================  ==========================  ==============================

Note what is **not** in a file. The crediting rule that actually drives this product —
the target `taux servi`, the dotation and release policy, the FIFO release order, the
expense loadings, the dynamic-surrender coefficients — lives in model point columns and
``Projection`` References rather than in a rate table, and that is not an oversight.
**None of it is published.** Only the outer bounds of the discretion are public: at
least 85% of the `compte financier` and the art. A132-11 technical share must reach
policyholders, and the PPB must be released within eight years. Between those bounds no
insurer publishes its own rule, so every value is a standardization, and putting them
where a reader trips over them is better than filing them in a table that looks like
data.

The three rate tables each carry a ``provenance`` column that says in words what the
numbers are. That column is never read by a formula; it is there so that a file lifted
out of this directory still says what it is.
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

    Eleven model points.  Point 1 is the notes' worked example; the rest exercise the
    variants the notes discuss - the `garantie brute` floor, an aggressive target rate,
    a paid-up contract, a nil PPB, a young vintage profile, the low and high financial
    scenarios, a small new-business cell with an entry charge, a drawdown cell and a
    grouped cell carrying 250 policies.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The base annual mortality rates by sex and age, from *mort_table.csv*.

    A **[std]** proxy shaped like French population mortality.  The statutory tables -
    TH00-02/TF00-02 and TGH05/TGF05, annexed to the arrêté du 1er août 2006 - are cited
    in the documents but **not redistributed here**, and the Institut des actuaires'
    certified experience tables are not public either, so no permitted insured basis can
    be reproduced.  INSEE population data is the only freely redistributable French
    mortality source, and this is a Makeham curve fitted to its shape.
    ``Projection.mort_be_factor`` carries the allowance for population mortality being
    heavier than insured experience; the table is anchored so that the two together give
    the notes' placeholder ``q = 0.0060`` at male age 60 exactly.  Sorted on read,
    because ``Projection.mort_rate`` indexes into it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col=["sex", "age"]).sort_index()


def lapse_table():
    """The base annual surrender rates by completed policy duration, from *lapse_table.csv*.

    4% at durations 1-7, **8% at duration 8**, 5% at durations 9 and beyond.  The
    duration-8 step is the tax threshold rather than a behavioural guess: the reduced
    7.5% rate and the EUR 4 600 / EUR 9 200 annual allowance both switch on at eight
    years, and a French savings projection with no surrender step there has ignored the
    single strongest driver of French partial-surrender timing.  The **levels** are
    **[std]** - the ACPR publishes aggregate surrender flows with no split by duration,
    age or vintage - and the dynamic term layered on them in ``Projection.lapse_rate``
    matters more than the levels do.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file,                              # noqa: F821
        index_col="policy_duration").sort_index()


def fin_rate_table():
    """The financial scenario paths, from *fin_rate_table.csv*.

    Three scenarios by projection year: the fund's `taux de rendement de l'actif`
    ``r_fin`` and the market reference rate ``ref_rate`` the dynamic surrender term keys
    off.  The key column is ``y``, the model's own **projection year**, 0-based: ``y = 0``
    is the first projected year and the file runs 0 to 39.  It is named ``y`` and not
    ``t`` because ``t`` is a policy **month** everywhere else in this model - the table is
    an annual path and ``Projection.r_fin`` reads it at ``proj_year(t) = t // 12``.
    The base path runs 3.30% down to 2.30% over twelve years and stays there,
    anchored to the ACPR's observed asset return - 2.8% in 2025, 2.5% in 2024, half of
    undertakings between 2.4% and 3.3% - and to the reinvestment picture behind it.
    ``ref_rate`` is 2.20% throughout, the 2025 average Livret A rate.  These are
    **[std]** scenarios, not forecasts.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / fin_rate_file,                                 # noqa: F821
        index_col=["scenario_id", "y"]).sort_index()


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_table_file = "lapse_table.csv"

fin_rate_file = "fin_rate_table.csv"

pd = ("Module", "pandas")
