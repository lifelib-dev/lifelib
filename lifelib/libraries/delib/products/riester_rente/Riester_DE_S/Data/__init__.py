# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.Riester_DE_S.Projection` as ``data``. :mod:`~.Riester_DE_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its
own cells cache; if the readers lived there, every model point would re-read every file.
Holding them in an unparameterized Space reads each file once no matter how many policies
are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/riester_rente/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Riester_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=========================  ==============================  ==========================
Reference                  Cells                           File
=========================  ==============================  ==========================
model_point_file           model_point_table()             model_point_table.csv
mort_accum_file            mort_table_accum()              mort_table_accum.csv
annuity_mort_file          annuity_mort_table()            annuity_mort_table.csv
lapse_file                 lapse_table()                   lapse_table.csv
zulage_file                zulage_schedule()               zulage_schedule.csv
income_file                income_schedule()               income_schedule.csv
surplus_file               surplus_scenario()              surplus_scenario.csv
freq_loading_file          freq_loading()                  freq_loading.csv
=========================  ==============================  ==========================

**Every file but ``model_point_table.csv`` carries a per-row ``provenance`` column**,
which is delib's second ruling: a model point is a *configuration*, every other row is an
*assumption* and says on the row where its number came from. The tags are the same
vocabulary the prose uses — ``[S#]``, ``[R#]``, ``[REG-R#]``, ``[std]`` with a rationale.

.. rubric:: The two decrement tables are [std] proxies, and what a replacement must preserve

The German first-order tables are the property of the **Deutsche Aktuarvereinigung**, are
not public, and are **not redistributed here**. They are cited by name and stood in for.

``mort_table_accum.csv`` stands in for **DAV 2008 T**, the death-risk table. It is a
Gompertz proxy, ``qx = 0.001500 x 1.10^(age - 50)`` over ages 16 to 109 with ``qx = 1`` at
110, and it carries **no improvement projection at all**, because on a death cover
improvement runs in the insurer's favour and a first-order death basis does not anticipate
it. The projection applies ``mort_be_factor = 0.80`` on top, which is the direction of
prudence for a death table: a first-order death basis assumes mortality *higher* than
expected, so the best estimate sits **below** it. **The anchor a substitute must preserve
is the rate at age 50, ``qx = 0.001500``**, so the notes' worked example still closes;
the slope is a placeholder and nothing in the corpus fixes it.

``annuity_mort_table.csv`` stands in for **DAV 2004 R**, the annuitant table, and the one
structural property that is *not* optional is that it is **two-dimensional**: a
generational basis in age and calendar year,
``q(x, tau) = qx_base(x) x (1 - improvement(x))^(tau - annuity_base_year)`` with
``annuity_base_year = 2027``. A period-table proxy understates a twenty-year-deferred
annuitisation by a margin that dwarfs every other assumption in the model, so a
replacement may change the level and the improvement scale but must keep both arguments.
The shipped base is ``qx_base = 0.006000 x 1.115^(age - 65)`` over ages 55 to 109, capped
at 0.95, with ``qx_base = 1`` at 110; the improvement is 1,8 % a year to age 65, tapering
by 0,045 pp per year of age to a floor of 0,2 %. It is applied at
``annuity_mort_be_factor = 1.15`` in the projection — the opposite direction, because a
first-order *annuity* table assumes mortality *lower* than expected — and at 1.00 inside
:func:`~.Riester_DE_S.Projection.ann_factor`, which is the first-order basis the market's
*Rentenfaktor* is struck on. **The anchor a substitute must preserve is the first-order
annuity factor at age 67 in calendar 2044, ``ann_factor() = 20.87222879``**, which is what
puts ``rentenfaktor_curr()`` at 27,947822 — below the anchor's guaranteed 29,00 — so that
the **guaranteed** *Rentenfaktor* binds on the worked example and the notes' conversion
table reproduces exactly.

The remaining six files are assumption or configuration tables rather than proxies for a
named instrument; each row says so in its own ``provenance`` cell.
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

    Indexed by ``point_id``, one row per policy, twenty-six columns.  This is the one
    input file with **no** ``provenance`` column, and the only exemption in the library: a
    model point is a *configuration* — one policy's own terms — rather than an assumption,
    so a per-row tag would repeat the same provenance once per policy while saying nothing
    about any assumption.  Where a column is an assumption in disguise (``rechnungszins``,
    the opening balances) the technical notes carry the tag.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table_accum():
    """Accumulation-phase death rates by attained age, from *mort_table_accum.csv*.

    A **[std]** proxy for **DAV 2008 T**, which is proprietary and is not redistributed
    here; see the Space docstring for the anchor a replacement must preserve.  Ages 16 to
    110, no improvement dimension: a first-order death basis does not anticipate mortality
    improvement, because on a death cover improvement favours the insurer.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_accum_file, index_col="age")              # noqa: F821


def annuity_mort_table():
    """Annuitant base rates and improvement scale by attained age.

    Read from *annuity_mort_table.csv*, ages 55 to 110.  A **[std]** *generational* proxy
    for **DAV 2004 R**: ``qx_base`` is the rate in the base calendar year and
    ``improvement`` the annual rate of decline, so the applied rate depends on **both**
    attained age and calendar year.  That two-dimensional structure is the property a
    replacement may not drop.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / annuity_mort_file, index_col="age")            # noqa: F821


def lapse_table():
    """Surrender and transfer-out rates by contract duration, from *lapse_table.csv*.

    The ``duration`` key is the **contract year**, 1-based and contractual: row ``k`` is
    contract year ``k``, and the projection reaches it through
    ``duration(t) + 1 = duration_init() + t + 1`` rather than through the 0-based ``t``
    — ``duration(t)`` is itself the 0-based count of completed contract years.

    Two rates, not one.  ``lapse_rate`` is a *Kündigung*, which repays every Zulage and
    every § 10a relief and taxes the accumulated growth; ``transfer_rate`` is an
    *Anbieterwechsel* under the statutory *Wechselrecht*, which carries none of those
    consequences.  The second is set **above** the first at every duration for that
    reason, and a model of this book carrying only a lapse rate has mis-specified it.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="duration")              # noqa: F821


def zulage_schedule():
    """The Zulage entitlement drivers by schedule id and projection period ``t``.

    Read from *zulage_schedule.csv*.  The ``t`` key is the model's own **0-based** time
    index, running ``0 ... 59``, and is read directly at ``t``.  Four drivers per row: ``unmittelbar``, the indicator
    that the *Grundzulage* is drawn at all; ``n_kinder_pre2008`` and
    ``n_kinder_post2008``, the counts of children for whom *Kindergeld* is drawn at the
    185 € and the 300 € rate — a permanent **birth-cohort** split, not a transition, so a
    contract can carry both at once; and ``bonus``, the once-in-a-lifetime
    *Berufseinsteiger-Bonus*.  The schedule is exogenous because *Kindergeld* is a
    household fact the insurance contract does not observe, which is the most awkward
    feature of this product for a per-policy projection.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / zulage_file, index_col=["zulage_id", "t"])     # noqa: F821


def income_schedule():
    """Contribution-liable earnings by schedule id and projection period ``t``.

    Read from *income_schedule.csv*.  The ``t`` key is the model's own **0-based** time
    index, running ``0 ... 59``.  ``income(t)`` is the earnings of the **calendar year of
    period t**; the § 86 *Mindesteigenbeitrag* of period ``t`` is struck on the
    **previous** calendar year, so the projection reads ``income(t - 1)`` and takes
    ``income_init`` from the model point for ``t = 0``.  The ``zero`` path encodes a
    *mittelbar zulageberechtigt* spouse, who has no contribution-liable earnings of their
    own and whose *Mindesteigenbeitrag* is therefore the 60 € *Sockelbeitrag*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / income_file, index_col=["income_id", "t"])     # noqa: F821


def surplus_scenario():
    """The declared *laufende Verzinsung* by scenario id and projection period ``t``.

    Read from *surplus_scenario.csv*.  The ``t`` key is the model's own **0-based** time
    index, running ``0 ... 89``, and is read directly at ``t``.  Two paths ship: ``base`` at 2,30 % level and
    ``low`` at 0,50 % level.  The declared rate **includes** the *Rechnungszins* — adding
    the two is the German arithmetic error this model is built to make visible — so
    ``decl_rate - rechnungszins`` is the *laufende Zinsüberschussbeteiligung* and is
    what accrues in the *Überschussguthaben*.  It is the largest single lever in the model
    and the least supported: no declared rate at any carrier was established.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surplus_file, index_col=["scenario_id", "t"])  # noqa: F821


def freq_loading():
    """The *Ratenzuschlag* multiplier by payment frequency, from *freq_loading.csv*.

    A **charge** and never a credit: the saver pays ``eigenbeitrag_pp x load`` while only
    ``eigenbeitrag_pp`` reaches the *Sparbeitrag* base and the *Beitragsgarantie*, so the
    loading enlarges the premium income and nothing else.  Crediting it to the account is
    a listed modeling pitfall.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / freq_loading_file, index_col="prem_freq")      # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_accum_file = "mort_table_accum.csv"

annuity_mort_file = "annuity_mort_table.csv"

lapse_file = "lapse_table.csv"

zulage_file = "zulage_schedule.csv"

income_file = "income_schedule.csv"

surplus_file = "surplus_scenario.csv"

freq_loading_file = "freq_loading.csv"

pd = ("Module", "pandas")
