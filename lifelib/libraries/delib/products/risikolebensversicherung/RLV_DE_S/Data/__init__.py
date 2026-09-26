# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The six input CSVs are read here, **once per model**, and referenced from
:mod:`~.RLV_DE_S.Projection` as ``data``. :mod:`~.RLV_DE_S.Projection` is parameterized
by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells
cache; if the readers lived there, every model point would re-read every file. Holding
them in an unparameterized Space reads each file once no matter how many policies are
projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/risikolebensversicherung/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RLV_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ============================  ==========================
Reference                 Cells                         File
========================  ============================  ==========================
model_point_file          model_point_table()           model_point_table.csv
mort_table_file           mort_table()                  mort_table.csv
benefit_schedule_file     benefit_schedule()            benefit_schedule.csv
nvg_schedule_file         nvg_schedule()                nvg_schedule.csv
lapse_file                lapse_table()                 lapse_table.csv
freq_loading_file         freq_loading_table()          freq_loading_table.csv
========================  ============================  ==========================

**Every file but the model point table carries a per-row ``provenance`` column.** That is
this library's second ruling and it is machine-checked in
``tests/test_model_conventions_de.py``: a number in a shipped input file says where it
came from, in the same ``[S#]`` / ``[R#]`` / ``[REG-R#]`` / ``[std]`` vocabulary the
documents use. ``model_point_table.csv`` is the single exemption, because a model point is
a *configuration* — one policy's own terms — rather than an assumption.

.. rubric:: The mortality table is a proxy, and here is its anchor

``mort_table.csv`` is a **[std] Gompertz-form proxy**, not a fitted or supervised table::

    mort_rate(sex, smoker, x) = base(sex) x smoker_mult(smoker) x 1.095^(x - 30)

    base(M) = 0.00040      base(F) = 0.00020
    smoker_mult(N) = 1.00  smoker_mult(R) = 2.20        ages 18 to 80

The German first-order basis for a term product is **DAV 2008 T**, with its
**DAV 2008 T NR** and **DAV 2008 T R** smoker variants — derived by the DAV
*Arbeitsgruppe Biometrische Rechnungsgrundlagen* from German insurers' own policy data
over 2006 to 2008, adopted 4 December 2008 and restated as a *Fachgrundsatz* dated
29 November 2022, and expressly suitable for premium calculation but **not** for policies
written without a *Gesundheitsprüfung*. **Those tables are the property of the Deutsche
Aktuarvereinigung, are not public, and are not redistributed here.** They are cited by
name; the shipped proxy stands in for them.

**What a replacement must preserve, so that the notes' worked example still closes:**

1. **The 50/50 unisex non-smoker blend is** ``0.00030 x 1.095^(x - 30)``. That is the
   [std] best-estimate scale the research file constructed and froze, and it is what the
   tariff — which may not rate on sex — is actually built on. A replacement table whose
   male and female non-smoker rates average to this at every age reproduces every premium
   in the model unchanged.
2. **The female-to-male ratio is 0.50 at every age**, the order of magnitude reported for
   insured lives at the ages this product is sold [unverified]. It is what decides the
   size of the unisex cross-subsidy between model points 1 and 2, and it moves no premium.
3. **The smoker multiplier is 2.20**, the mid-point of the two-to-three range reported for
   insured-lives smoker mortality at working ages [unverified]. It reproduces a *premium*
   ratio near 2.0 between model points 1 and 3 once the sum-related and per-policy expense
   elements, which do not scale with mortality, are added back.

The 9,5 % per year of age is the slope of the research file's own construction; it is a
fitted-in-spirit gradient with **no German source**, and on model point 14's forty-year
run it is the single most exposed number in the model. **A population table is the wrong
starting point for a replacement**: a Destatis series without a selection adjustment
overstates claims by a wide margin at the issue ages 25–45 this product is sold at.
Dropping a licensed or company table in place of this one changes the basis with no
formula change.

.. rubric:: The other four assumption files

The three schedule files are keyed on ``policy_year``, the **contractual 1-based label**,
and their values are left as they are: ``Projection`` reads them at ``t + 1``, ``t`` being
the model's 0-based period index.

``benefit_schedule.csv`` carries the three German *Versicherungssumme* shapes as factors
on the initial sum: ``konstant`` (1.0 at every year, the majority form, shipped for forty
years), ``linear_fallend`` (``(21 - policy_year)/20``, i.e. ``f(t) = (20 - t)/20``,
shipped for the twenty-year term model
point 4 is written on) and ``annuitaet_fallend_3pct`` (the outstanding balance of a
thirty-year annuity loan at 3,00 % nominal, shipped for model point 5's thirty-year term).
The falling schedules are **term-specific by construction**: an amortisation shape is
agreed at issue for a stated term, so a schedule id is written for the term it belongs to
rather than truncated from a longer one. A model that hard-codes a constant sum insured
cannot represent two of the three shapes the German market sells, which is why the
schedule is a first-class input.

``nvg_schedule.csv`` carries the cumulative *Nachversicherungsgarantie* multiplier
``sum_uplift``: ``keine`` is 1.0 throughout and is the base run, and
``nvg_zwei_erhoehungen`` steps to 1.2 at policy year 6 (``t = 5``) and 1.4 at policy
year 12 (``t = 11``). **No
event list, cap, exercise window or age limit was established from any document**, so the
take-up is exogenous — a schedule, not a modelled decision. What the model does with it is
not exogenous: each increment carries **its own** three-year § 161 window, so
``suicide_factor`` is a weighted average across tranches in the years after an increase.

``lapse_table.csv`` is 6 % in policy year 1, 4 % in years 2 and 3 and 3 % thereafter, all
**[std]**, argued from three structural features rather than from data: nothing is
forfeited by lapsing, exit is frictionless in time because the *Versicherungsperiode*
follows the *Zahlweise*, and the need that motivated the purchase amortises. The GDV
whole-market *Stornoquote* is a book average dominated by long-dated savings contracts and
is deliberately **not** used. The table's own row for the final policy year still reads
3 %; the model zeroes it, because a lapse and an expiry at the end of the last period
``t = n - 1`` are the same event paying the same nothing.

``freq_loading_table.csv`` carries the *Ratenzahlungszuschlag* — 1.000 annual, 1.02
half-yearly, 1.03 quarterly, 1.05 monthly — a German market convention with no carrier
attribution, and the instalment count that goes with it. Whether carriers strike the
loading on the *Bruttobeitrag* or the *Zahlbeitrag* was not established; this model loads
the billed amount, so the *Brutto* = *Zahl* + *Verrechnung* identity holds at every
frequency.
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

    The one input file with no ``provenance`` column, and the only one exempt from the
    rule: a model point is a *configuration* — one policy's issue age, sum insured,
    *Zahlweise* and schedule ids — rather than an assumption about the world.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The second-order annual death rates, from *mort_table.csv*.

    Indexed by ``table_id``, ``sex``, ``smoker`` and attained ``age``.  A **[std]**
    Gompertz proxy standing in for DAV 2008 T, which is proprietary and is cited by name
    rather than shipped; see the Space docstring for the three anchors a replacement must
    preserve.  The table is *second order* — a best estimate for medically selected lives.
    The first-order tariff rate is built from it in ``Projection.mort_rate_tar`` by taking
    the unisex blend and applying the *Sicherheitszuschlag*, so there is exactly one
    unsourced mortality level in the model rather than two stacked on each other.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["table_id", "sex", "smoker", "age"])


def benefit_schedule():
    """The *Versicherungssumme* factors by schedule id and **1-based** policy year.

    Read from *benefit_schedule.csv*.  ``konstant``, ``linear_fallend`` and
    ``annuitaet_fallend_3pct`` are the three German shapes; the two falling ones are
    written for the term of the model point that uses them, an amortisation schedule being
    agreed at issue for a stated term.  ``policy_year`` is the contractual label and runs
    from 1; ``Projection.benefit_factor`` reads it at ``t + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / benefit_schedule_file,                         # noqa: F821
        index_col=["schedule_id", "policy_year"])


def nvg_schedule():
    """The cumulative *Nachversicherungsgarantie* multiplier by schedule id and **1-based** policy year.

    Read from *nvg_schedule.csv*.  ``keine`` is 1.0 throughout — the base run — and
    ``nvg_zwei_erhoehungen`` steps twice.  Take-up is **exogenous**: no event list, cap,
    window or age limit was established from any document, so an increase is supplied as a
    schedule rather than modelled as a decision.  ``policy_year`` is the contractual label
    and runs from 1; ``Projection.sum_uplift`` reads it at ``t + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / nvg_schedule_file,                             # noqa: F821
        index_col=["nvg_id", "policy_year"])


def lapse_table():
    """The annual lapse rates by **1-based** policy year, read from *lapse_table.csv*.

    Entirely **[std]**: no *Risikoversicherung*-specific German rate exists in the source
    corpus, and the whole-market *Stornoquote* is deliberately not used.  The final policy
    year's row is a live 3 % and is overridden to zero by ``Projection.lapse_rate``, which
    is where the convention belongs — the zero is a property of the last policy year, not
    of the table.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="policy_year")           # noqa: F821


def freq_loading_table():
    """The *Ratenzahlungszuschlag* and instalment count by *Zahlweise*.

    Read from *freq_loading_table.csv*: the multiplier ``prem_freq_load`` applied to the
    billed amount, and ``instalments``, the number of payments a year, which is carried
    for reporting and enters no cash flow on an annual grid.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / freq_loading_file, index_col="prem_freq")      # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

benefit_schedule_file = "benefit_schedule.csv"

nvg_schedule_file = "nvg_schedule.csv"

lapse_file = "lapse_table.csv"

freq_loading_file = "freq_loading_table.csv"

pd = ("Module", "pandas")
