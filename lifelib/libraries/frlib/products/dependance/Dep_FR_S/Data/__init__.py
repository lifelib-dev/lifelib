# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.Dep_FR_S.Projection` as ``data``. :mod:`~.Dep_FR_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/dependance/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Dep_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

========================  ============================  ==============================
Reference                 Cells                         File
========================  ============================  ==============================
model_point_file          model_point_table()           model_point_table.csv
mort_table_file           mort_table()                  mort_table.csv
prevalence_file           prevalence_table()            prevalence_table.csv
severity_share_file       severity_share_table()        severity_share_table.csv
lapse_table_file          lapse_table()                 lapse_table.csv
cause_mix_file            cause_mix_table()             cause_mix_table.csv
reduction_file            reduction_table()             reduction_table.csv
revision_file             revision_table()              revision_table.csv
========================  ============================  ==============================

**Why the decrement basis is four files and not one.** Nothing in this product's
assumption set comes from a single publication, and the four files are four different
kinds of claim. ``mort_table.csv`` is a **[std]** Gompertz proxy shaped like a French
population table; ``prevalence_table.csv`` holds the three parameters of a **[std]**
logistic fitted to two *sourced* DREES APA prevalence rates per sex;
``severity_share_table.csv`` holds the **[std]** haircuts that turn public APA take-up
on the AGGIR grid into insured prevalence on the contract's own trigger grid, which is
the step no retrieved document supports at all; and ``cause_mix_table.csv`` holds the
**[std]** weights of the three *carence* causes. Keeping them apart keeps their
provenances apart: every one of these files carries a ``provenance`` column, and the
words in it say which of the four kinds each row is.

No table in this library is a copy of a homologated French mortality table. TH 00-02 /
TF 00-02 and TGH05 / TGF05 are cited by name and arrêté in ``technical-notes.md`` and
are not reproduced here.
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
    """The healthy-life mortality rates by sex and age, from *mort_table.csv*.

    Annual rates for a life in the **autonomous** state.  A **[std]** proxy: a
    two-parameter Gompertz force ``mu(x) = B c^x`` with ``B = 5.2321459244e-06`` and
    ``c = 1.11704543``, fitted to the two **[std]** anchors ``mort_rate(60) = 0.00400``
    and ``mort_rate(90) = 0.10500``, shaped like a French female population table with
    no sourced value behind either anchor.  The male rows are the same force times
    **1.60 [std]**, a sex multiple introduced here because ``technical-notes.md``
    specifies a female basis only.  Rates for the two dependent states are this rate
    raised to a power in ``Projection.mort_rate_partial`` and
    ``Projection.mort_rate_total``, not a separate table: no impaired-life table for
    either French dependence state exists in any retrieved source.

    The ``provenance`` column says so on every row.  This is **not** a copy of
    TH 00-02 / TF 00-02 or of TGH05 / TGF05, which are cited by name and arrêté in the
    technical notes and are not reproduced by this library.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"]).sort_index()


def prevalence_table():
    """The APA-prevalence logistic parameters by sex, from *prevalence_table.csv*.

    ``prev_ceil``, ``prev_beta`` and ``prev_x_mid`` of
    ``prev(x) = prev_ceil / (1 + exp(-beta (x - x_mid)))``.  The two slope parameters
    are pinned to **sourced** DREES rates at end 2023 — 20% of women and 13% of men aged
    80 to 89, read at the band midpoint 84.5, and 54% of women and 40% of men from age
    90, read at 93 — while ``prev_ceil = 0.90`` is **[std]** and unidentified by the
    fit.  The ceiling governs the tail, which is where the claims are.

    What this table measures is **receipt of the *allocation personnalisée
    d'autonomie***: a prevalence, not an incidence, and a public classification on the
    AGGIR grid rather than the insurer's.  Both conversions are explicit steps
    elsewhere — :func:`severity_share_table` for the first and
    ``Projection.inc_rate_partial`` for the second.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / prevalence_file,                               # noqa: F821
        index_col=["sex", "param"]).sort_index()


def severity_share_table():
    """The public-to-insured severity shares, from *severity_share_table.csv*.

    ``share_partial`` and ``share_total`` are the fractions of APA prevalence the model
    reads as insured *dépendance partielle* and *dépendance totale*, keyed by the
    contract's ``trigger_grid``.  All three rows are **[std]**.  The ``avq5`` row is
    bounded by two indirect anchors — the sourced GIR 1-2 share of APA beneficiaries,
    34.9%, and the market's ratio of *rentes* in payment to lives covered, about 0.44 —
    and the ``avq6`` and ``aggir`` rows are flat factors on it that **no retrieved
    document supports at all**.  The ``provenance`` column says which is which.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / severity_share_file,                           # noqa: F821
        index_col="trigger_grid")


def lapse_table():
    """The annual lapse rates by policy year, read from *lapse_table.csv*.

    Applied to the autonomous ledger alone: a recognised life is exonerated and a
    reduced membership is paid up, so neither can lapse for non-payment, and with no
    surrender value there is nothing to surrender for.  The last row is the terminal
    rate — ``Projection.lapse_rate_base`` caps the policy year at the largest year in
    the table, so a lifetime projection does not run off the end of it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_table_file, index_col="policy_year")     # noqa: F821


def cause_mix_table():
    """The **[std]** cause mix weighting the three *carences*, from *cause_mix_table.csv*.

    accident 10% / illness other than neurological or psychiatric 55% / neurological or
    psychiatric 35%.  The three-way *structure* is close to universal across the
    retrieved contracts; the **weights** are what a projection needs and no retrieved
    document states any.  ``Projection.carence_factor`` reads the shares against the
    model point's own three *carence* lengths, so a contract with a different menu
    changes the model point and not this file.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cause_mix_file, index_col="cause")             # noqa: F821


def reduction_table():
    """The *barème de maintien des garanties*, read from *reduction_table.csv*.

    ``coefficient`` is the share of the guaranteed *rente totale* a paid-up membership
    keeps, by completed years of premiums.  The **only published French LTC reduction
    scale** retrieved, the CNP Banque de France annexe 2 in force 1 January 2012, whose
    own qualifying period is five years; the reference composite applies it from the
    eight-year qualifying period of the other retrieved contracts **[std]**, so 25% is
    the coefficient at first qualification and the rows at 5, 6 and 7 years are
    unreachable on the base cell.  The last row applies to 30 years and over.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / reduction_file, index_col="years_paid")        # noqa: F821


def revision_table():
    """The scheduled tariff-revision path, read from *revision_table.csv*.

    An annual rate by policy year, applied to the premium **on top of** the
    *revalorisation des garanties*.  A real tariff revision is a management action, not
    a projected assumption: the column exists so that the contractual capability is
    present and testable, and the shipped path — nil for five years, then 1.5% a year —
    is arbitrary inside the 0-10% band the only retrieved cap allows.  The last row is
    the terminal rate.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / revision_file, index_col="policy_year")        # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

prevalence_file = "prevalence_table.csv"

severity_share_file = "severity_share_table.csv"

lapse_table_file = "lapse_table.csv"

cause_mix_file = "cause_mix_table.csv"

reduction_file = "reduction_table.csv"

revision_file = "revision_table.csv"

pd = ("Module", "pandas")
