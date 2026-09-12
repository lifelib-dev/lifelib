# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.TD_FR_S.Projection` as ``data``. :mod:`~.TD_FR_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/temporaire_deces/``, rather than data stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``TD_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so
the model works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells:

========================  ============================  ==========================
Reference                 Cells                         File
========================  ============================  ==========================
model_point_file          model_point_table()           model_point_table.csv
premium_rate_file         premium_rate_table()          premium_rate_table.csv
mort_table_file           mort_table()                  mort_table.csv
lapse_file                lapse_table()                 lapse_table.csv
freq_loading_file         freq_loading_table()          freq_loading_table.csv
benefit_schedule_file     benefit_schedule()            benefit_schedule.csv
========================  ============================  ==========================

Two of the six deserve a word about what they are and are not.

``premium_rate_table.csv`` is the one genuinely French artefact in the set: a published
*tarif de base annuel* by attained age, in per cent of the guaranteed capital, shipped
here as the decimal fraction the cotisation rule multiplies by. It is a real rate card
of a 2019–2021 vintage, and its shape — including the +38 % step from age 59 to 60
against a trend of about +8 % — is what a fitted curve would smooth away. Use it for
shape, not for level.

``mort_table.csv`` is the opposite: a **[std] Gompertz-form proxy**,
``0.00400 x 1.09^(age - 58)`` over ages 18–74, not a fitted or homologated table. The
regulatory non-annuity tables TH 00-02 and TF 00-02 are annexed to the arrêté du
20 décembre 2005 and are cited by name in this library rather than redistributed, and no
French insurer publishes a basis of its own. The 9 % per year of age slope is calibrated
on the published tariff grid — the one observable French artefact — and sits at the top
of it rather than inside a tight band: the grid rises at roughly 7–9 % per year of age
from age 35, compounding at 7,7 % over ages 42–58 and 8,98 % over the whole rated span
35 to 74. A tariff gradient is not a mortality gradient, so both the level and the slope
are placeholders. **The anchor a substitute table must preserve is the rate at age 58 =
0.00400**, so the notes' worked example still closes. INSEE's national series is the
intended base for a replacement; it is *population*, not insured, mortality, and the
INSEE page states no licence or reuse conditions — standard open-data terms are assumed
there and that assumption is [unverified], so confirm before redistributing derived CSVs.
Dropping a licensed or company table in place of this one changes the basis with no
formula change.
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


def premium_rate_table():
    """The tariff rates by rate id and attained age, from *premium_rate_table.csv*.

    An **annual** *tarif de base* by attained age, held as the decimal fraction of the
    guaranteed capital, so the published 1,05 % at age 58 is stored as ``0.0105`` and
    ``sum_assured x prem_rate`` is the annual cotisation before the *surprime* and the
    fractionation loading.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / premium_rate_file,                             # noqa: F821
        index_col=["rate_id", "age"])


def mort_table():
    """The **annual** death rates by attained age, from *mort_table.csv*.

    A **[std]** proxy, not a homologated table; see the Space docstring for what it is
    and what a replacement must preserve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file, index_col="age")               # noqa: F821


def lapse_table():
    """The lapse rates by policy year, read from *lapse_table.csv*.

    The rates are **annual** rates by policy year; ``Projection.lapse_rate_mth`` converts
    them to the month.  ``policy_year`` is the **contractual 1-based** label, 1 to 4, not
    the model's 0-based month index: ``Projection.lapse_rate_base`` reads it through
    ``Projection.policy_year(t) = t // 12 + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="policy_year")           # noqa: F821


def freq_loading_table():
    """The fractionation loadings and fees by payment frequency.

    Read from *freq_loading_table.csv*: the number of ``instalments`` per policy year,
    the multiplier ``prem_freq_load`` embedded in the cotisation TTC and the fixed annual
    *frais d'échéance* ``prem_freq_fee``, which is a euro amount and not a second
    percentage.  The last two are the only disclosed charge figures in the whole source
    corpus, and the first is what ``Projection.prem_cycle`` and
    ``Projection.prem_inst_pp`` collect them on.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / freq_loading_file, index_col="prem_freq")      # noqa: F821


def benefit_schedule():
    """The benefit factors by schedule id and policy year, from *benefit_schedule.csv*.

    One schedule ships, ``constant``, whose factor is 1.0 in every year: the capital of
    a French standalone temporaire décès does not amortize.  The table exists so that a
    decreasing shape can be dropped in without a formula change; no source in the corpus
    gives one, so none is shipped.

    ``policy_year`` is the **contractual 1-based** label, 1 to 57, not the model's 0-based
    month index: ``Projection.benefit_factor`` reads it through
    ``Projection.policy_year(t) = t // 12 + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / benefit_schedule_file,                         # noqa: F821
        index_col=["schedule_id", "policy_year"])


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

premium_rate_file = "premium_rate_table.csv"

mort_table_file = "mort_table.csv"

lapse_file = "lapse_table.csv"

freq_loading_file = "freq_loading_table.csv"

benefit_schedule_file = "benefit_schedule.csv"

pd = ("Module", "pandas")
