# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The seven input CSVs are read here, **once per model**, and referenced from
:mod:`~.KLV_DE_S.Projection` as ``data``. :mod:`~.KLV_DE_S.Projection` is parameterized by
``point_id``, so each ``Projection[N]`` is a separate ItemSpace with its own cells cache;
if the readers lived there, every model point would re-read every file. Holding them in an
unparameterized Space reads each file once no matter how many policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/kapitallebensversicherung/``, rather than data stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``KLV_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

========================  ============================  ==========================
Reference                 Cells                         File
========================  ============================  ==========================
model_point_file          model_point_table()           model_point_table.csv
mort_table_file           mort_table()                  mort_table.csv
lapse_file                lapse_table()                 lapse_table.csv
surplus_rate_file         surplus_rate_table()          surplus_rate_table.csv
cost_file                 cost_table()                  cost_table.csv
freq_loading_file         freq_loading_table()          freq_loading_table.csv
deckrv_file               deckrv_table()                deckrv_table.csv
========================  ============================  ==========================

Every file but ``model_point_table.csv`` carries a final **``provenance``** column, one tag
per row — this library's second ruling, and machine-checked. The model point table is the
single exemption, because a model point is a configuration rather than an assumption.

.. rubric:: The mortality table is a [std] proxy, and this is its anchor

``mort_table.csv`` is **not** a fitted or an industry table. It is a Makeham-form proxy,
sex-specific over ages 0 to 120::

    mort_rate_1st(M, x) = 0.00022 + B * 1.10 ** x
    mort_rate_1st(F, x) = 0.00016 + B * 1.10 ** (x - 3)

with the single free constant ``B`` fixed by one **anchor**:

    **mort_rate_1st(M, 37) = 0.001200 exactly**

which is the first-order death rate at the worked example's entry age. That anchor is why
the notes' twenty-five-year table reproduces to the cent, and it is the one number a
replacement table must reproduce for the worked example to survive unchanged. Rates are
capped at 1.0 at the top of the age range, which no shipped model point reaches.

The table this proxy stands in for is **DAV 2008 T**, the market-standard first-order
basis for German death-benefit business, derived over 2006–2008 from German insurers' own
policy data, the cleansed insured data covering 60 % of the German market in the
*Kapitallebensversicherung* segment. **It is the property of the Deutsche
Aktuarvereinigung, is not public and is not redistributed here**; it is cited by name.
A replacement must preserve four things beyond the anchor: an **insured-lives** level,
materially lighter than the national population table at the working ages; **sex-specific**
base tables, which are the raw material even though a German tariff written since
21 December 2012 may not price on sex; **no projected improvement**, because for a death
cover improvement favours the insurer; and an explicit *Sicherheitszuschlag* directed
*upward* on the death leg. The proxy carries **no selection factors**, which DAV 2008 T is
understood to have, so a book of newly underwritten lives shows more early deaths here than
a real one — stated rather than corrected by a second unsourced factor.

The best-estimate basis is this same table scaled: ``mort_rate(t) = mort_rate_base(t) *
mort_be_factor`` with ``mort_be_factor = 0.75``, so the first-order table carries a 33 %
safety loading. That wedge is the *Sicherheitszuschlag*, and its systematic release **is**
the *Risikoüberschuss*. The model does not compute the *Risikoüberschuss*, and the two
bases must not be crossed: ``mort_rate_base`` prices and reserves, ``mort_rate`` projects.

.. rubric:: The other six tables

``lapse_table.csv`` carries two duration-keyed rates that are easily confused.
``lapse_rate`` is the **surrender decrement** — the only voluntary exit modelled — and
``storno_rate`` is the **Stornoabzug**, the percentage deduction from the guaranteed value
on a surrender. Both are **[std]**: the only German lapse data are market aggregates that
are neither endowment-specific nor by duration, and the headline one counts conversions to
*beitragsfrei* alongside surrenders, so calibrating a surrender decrement to it
double-counts. The shape — suppressed approaching policy year 12 and spiking at it — is
what the twelve-year income-tax threshold supports; the levels are not sourced. Its key
column ``policy_year`` is the **contractual, 1-based** label and is left that way: the
projection's own index ``t`` is 0-based, and ``Projection.policy_year(t) = t + 1`` maps
between them.

``surplus_rate_table.csv`` carries three declared-rate paths keyed by ``scenario_id`` and
the same 1-based ``policy_year``. ``base`` is one carrier's 2026 *laufende Verzinsung* for its classic endowment
book, held level for the whole projection — a modelling choice, not a forecast; ``low`` and
``nil`` exist so that the sensitivity is exercisable rather than argued, ``nil`` resting on
the sourced statement that the surplus may be zero euros.

``cost_table.csv`` deliberately carries the **first-order tariff loadings and the
second-order expense assumptions on the same row**, because the difference between them
*is* the *Kostenüberschuss*. ``deckrv_table.csv`` carries both DeckRV ceilings — § 2's
*Höchstrechnungszins* and § 4's *Höchstzillmersatz* — keyed by ``issue_year``, both being
cohort facts that travel with the contract for its whole term. ``freq_loading_table.csv``
carries the *Ratenzahlungszuschlag*, which applies only where the sub-annual premium is an
instalment of an annual *Versicherungsperiode* (``unecht``) and not where the period is
genuinely sub-annual (``echt``).
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

    Fourteen single-policy configurations indexed by ``point_id``.  The only input file
    without a ``provenance`` column: a model point is a *configuration* — one policy's own
    terms — rather than an assumption, and that exemption is the only one in the library.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def mort_table():
    """The first-order annual death rates by sex and attained age, from *mort_table.csv*.

    A **[std]** Makeham-form proxy standing in for DAV 2008 T, which is not public and is
    not redistributed here.  See the Space docstring for the anchor that fixes it and for
    what a replacement must preserve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_table_file,                               # noqa: F821
        index_col=["sex", "age"])


def lapse_table():
    """The surrender rate and the *Stornoabzug* by policy year, from *lapse_table.csv*.

    ``lapse_rate`` is the decrement; ``storno_rate`` is the deduction the surrender value
    suffers.  Both **[std]**, and they are different quantities — see the Space docstring.
    The ``policy_year`` key is the **contractual, 1-based** label, read through
    ``Projection.policy_year(t) = t + 1`` rather than by the 0-based ``t`` directly.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="policy_year")           # noqa: F821


def surplus_rate_table():
    """The declared surplus rates by scenario and policy year, from *surplus_rate_table.csv*.

    ``decl_rate`` is the *laufende Verzinsung* — the **total** declared rate, from which
    the interest surplus is *derived* by subtracting the guarantee, never added on top of
    it.  ``term_rate`` is the *Schlussüberschussanteilsatz* and ``ans_rate`` the
    *Ansammlungszinssatz*.  Three scenarios ship: ``base``, ``low`` and ``nil``.  The
    ``policy_year`` key is the **contractual, 1-based** label, read through
    ``Projection.policy_year(t) = t + 1``.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surplus_rate_file,                             # noqa: F821
        index_col=["scenario_id", "policy_year"])


def cost_table():
    """The tariff loadings and the expense basis by ``cost_id``, from *cost_table.csv*.

    First order and second order on the same row — ``alpha_rate``, ``beta_rate`` and
    ``gamma_rate`` are what the tariff charges, ``acq_expense``, ``maint_expense``,
    ``expense_infl``, ``claim_expense``, ``comm_init_rate`` and ``comm_renew_rate`` are
    what the insurer expects to spend — because the difference between them **is** the
    *Kostenüberschuss*.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / cost_file, index_col="cost_id")                # noqa: F821


def freq_loading_table():
    """The *Ratenzahlungszuschlag* by payment frequency, from *freq_loading_table.csv*.

    ``instalments`` is the number of payments a year and ``prem_freq_load`` the multiplier
    on the annual *Bruttobeitrag*.  The loading applies only to an **unechte**
    unterjährige Zahlweise — an instalment of an annual *Versicherungsperiode* — and is
    inert where the sub-annual period is genuine.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / freq_loading_file, index_col="prem_freq")      # noqa: F821


def deckrv_table():
    """The two DeckRV cohort ceilings by issue year, from *deckrv_table.csv*.

    ``hoechstrechnungszins`` is § 2's maximum technical interest rate for new business and
    ``hoechstzillmersatz`` is § 4's maximum *Zillmersatz* as a fraction of the
    *Beitragssumme*.  Both are fixed at conclusion and **stay with the contract for its
    whole term**, which is why the German in-force book is a stack of cohorts and why they
    are keyed by ``issue_year`` rather than by projection year.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / deckrv_file, index_col="issue_year")           # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

mort_table_file = "mort_table.csv"

lapse_file = "lapse_table.csv"

surplus_rate_file = "surplus_rate_table.csv"

cost_file = "cost_table.csv"

freq_loading_file = "freq_loading_table.csv"

deckrv_file = "deckrv_table.csv"

pd = ("Module", "pandas")
