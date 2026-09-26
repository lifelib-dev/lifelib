# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Input data shared by every by-policy projection.

The eight input CSVs are read here, **once per model**, and referenced from
:mod:`~.Index_DE_S.Projection` as ``data``. :mod:`~.Index_DE_S.Projection` is
parameterized by ``point_id``, so each ``Projection[N]`` is a separate ItemSpace with
its own cells cache; if the readers lived there, every model point would re-read every
file. Holding them in an unparameterized Space reads each file once no matter how many
policies are projected.

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/indexpolice/``, rather than data stored inside the model. The model folder
therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded values — so
a diff of the model shows logic changes only. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Index_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

:func:`input_dir` resolves the directory from ``_model.path.parent`` at run time, so the
model works wherever the repository is checked out. Each table has a filename Reference
and a reader Cells:

=====================  ==========================  ==========================
Reference              Cells                       File
=====================  ==========================  ==========================
model_point_file       model_point_table()         model_point_table.csv
index_return_file      index_return_table()        index_return_table.csv
index_param_file       index_param_table()         index_param_table.csv
surplus_rate_file      surplus_rate_table()        surplus_rate_table.csv
election_file          election_table()            election_table.csv
mort_file              mort_table()                mort_table.csv
lapse_file             lapse_table()               lapse_table.csv
freq_load_file         freq_load_table()           freq_load_table.csv
=====================  ==========================  ==========================

.. rubric:: Every table but the model point table is a [std] construction

Nothing about an *Indexpolice* — no Cap level, no *Partizipationsquote*, no declared
surplus rate, no charge, no lapse rate — was established for any German carrier: direct
HTTP egress was blocked in the build environment and the session's search budget was
exhausted before this product was researched. Every assumption file therefore carries a
per-row ``provenance`` tag that says so in the library's own vocabulary, and the tags are
overwhelmingly ``[std]``. That is the honest form of the evidence, not a placeholder for
better data that was withheld.

``mort_table.csv`` is a **[std] Gompertz-form proxy**, ``qx(M, x) = 0.001200 x
1.095^(x - 40)`` over ages 20-100 with ``qx(F, x) = 0.65 x qx(M, x)``. The market bases
are **DAV 2008 T** for death cover and **DAV 2004 R**, a *Generationentafel* in attained
age *and* calendar year, for every annuity promise: they are the property of the Deutsche
Aktuarvereinigung, are not public, and are cited by name in this library rather than
redistributed. **The anchor a substitute table must preserve is ``qx(M, 40) = 0.001200``
exactly**, so the technical notes' worked example still closes; the female ratio and the
0.095 log-slope may move freely. Two properties of the real bases the proxy deliberately
does not have, and a user replacing it should know which: it is a **period** table, not a
generational one, so it understates a long-deferred annuitisation; and it carries no
selection effect. Neither matters much *here*, because mortality in this model is a
**timing** assumption and not an amount assumption — the death benefit is the account
value with a floor, not a sum at risk — but both matter greatly to the *Rentenfaktor*
that the terminal capital buys, which is why the *Rentenfaktor* is a **[std]** input
rather than a computed one.

``index_return_table.csv`` is the file the whole product turns on: one row per
``(index_id, t)`` and twelve monthly returns ``m01 ... m12``, as decimals. Three paths
ship, and each is reproducible from its own provenance tag rather than taken on trust:

* ``eqidx_vol17`` — a broad equity **price index**, from
  ``numpy.random.default_rng(20260829).normal(0.0060, 0.0500, size=(40, 12))`` rounded to
  four decimal places (0.60 % a month at an annualised 17.3 %). **Rows ``t = 8`` and
  ``t = 9`` — policy years 9 and 10 on the 0-based index — are overwritten** with the
  research file's constructed Example A and Example B, so that the two *Indexjahre* the
  mechanic turns on are *reproduced by the model* rather than restated in prose. The
  anchors a substitute path must preserve are those two rows: ``t = 8`` must sum, capped
  at 3 %, to **+8.90 %**, and ``t = 9`` must sum to **-2.60 %** while its compounded raw
  return is **+6.4402 %**.
* ``houseidx_vol5`` — the volatility-targeted house multi-asset index, from
  ``numpy.random.default_rng(20260830).normal(0.0025, 0.0144, size=(40, 12))`` rounded to
  four decimal places, carrying a 6 % Cap and a 100 % *Partizipationsquote* in
  ``index_param_table.csv`` because a low-volatility underlying is cheap to buy options on.
* ``zero_path`` — every monthly return exactly zero. Not a scenario but an **instrument**:
  it isolates the guaranteed accumulation, makes every *Indexjahr* credit exactly 0.00 EUR,
  and lets the *Beitragsgarantie* floor be tested where it actually binds.

``index_param_table.csv`` carries the monthly Cap and the *Partizipationsquote* per
``(index_id, t)``, so that a path can be repriced year by year without a formula change.
**The Cap and the declared surplus rate in ``surplus_rate_table.csv`` are not independent
parameters** — the Cap is the level at which the option strip costs the budget — and the
shipped pair (3.00 %, 2.50 %) is not mutually consistent at this volatility. The
projection reports the diagnostic ``index_budget_ratio()`` for exactly that reason.

``election_table.csv`` carries the *Wahlrecht* path ``w(t)``, the fraction of the year's
declared surplus directed to the index arm: ``always_index``, ``always_safe``,
``half_half`` and ``switch_at_15``. It is a **behavioural** assumption and not a
contractual one, and no election distribution for this product family is established.

``model_point_table.csv`` is the one file with no ``provenance`` column, and that
exemption is the library's only one: a model point is a *configuration* — one policy's
own terms — rather than an assumption, and tagging it row by row would repeat the same
provenance once per policy. Thirteen points ship; point 1 is the anchor cell of the
technical notes' worked example, and point 8 is an in-force cell whose first projected
*Indexjahr* is ``t = 8``, so it reproduces the research file's Examples A and B on a
50,000.00 EUR base to the euro.
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

    Thirteen single-policy model points, indexed by ``point_id``, each carrying the
    twenty-two contract attributes the projection reads.  The one input file exempt from
    the library's ``provenance`` rule, a model point being a configuration rather than an
    assumption.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / model_point_file, index_col="point_id")        # noqa: F821


def index_return_table():
    """The twelve monthly index returns of each *Indexjahr*, from *index_return_table.csv*.

    Indexed by ``(index_id, t)``, with value columns ``m01`` ... ``m12`` as decimal
    returns.  Wide rather than long because the twelve observations of an *Indexjahr*
    live **inside** one annual step: the contract's clock is annual, and this is what
    keeps ``Index_DE_S`` an ``_A`` model while the genuinely unit-linked ``FRV_DE_S`` is
    ``_S``.  All three shipped paths are **[std]**; see the Space docstring for how each
    was constructed and which rows a replacement must preserve.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / index_return_file,                             # noqa: F821
        index_col=["index_id", "t"])


def index_param_table():
    """The monthly Cap and the *Partizipationsquote* by index and year.

    Read from *index_param_table.csv*, indexed by ``(index_id, t)``: ``cap`` is the
    ceiling ``C`` applied to each month's return before the twelve are summed, ``quote``
    the fraction ``q`` of the year's compounded movement in the alternative payoff design.
    Both are per year, because the insurer redetermines them for each *Indexjahr*; the
    shipped paths hold them level only because no level for any carrier and any year was
    established.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / index_param_file,                              # noqa: F821
        index_col=["index_id", "t"])


def surplus_rate_table():
    """The declared *Überschussanteilsatz* by year, from *surplus_rate_table.csv*.

    Indexed by the model's 0-based ``t``, so its first row is ``t = 0``, the first policy
    year.  This rate **is** the option budget: for a contract in the index arm
    the same declared amount that a classic contract would receive as interest is spent on
    the option package instead.  It is exogenous here — the model consumes a declared rate
    and does not derive one from an investment result under the MindZV minimum.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / surplus_rate_file, index_col="t")              # noqa: F821


def election_table():
    """The *Wahlrecht* election paths, from *election_table.csv*.

    Indexed by ``(elect_id, t)``; ``w`` is the fraction of that year's declared surplus
    directed to the *Indexbeteiligung*, the remainder being credited as *sichere
    Verzinsung*.  ``w`` in [0, 1] rather than a binary flag, because some tariffs permit a
    partial election and all-or-nothing is then the special case.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / election_file, index_col=["elect_id", "t"])    # noqa: F821


def mort_table():
    """The annual death rates by sex and attained age, from *mort_table.csv*.

    A **[std]** Gompertz-form proxy anchored at ``qx(M, 40) = 0.001200``, not a DAV table;
    see the Space docstring for what it is, what it is not, and what a replacement must
    preserve.  Sex selects the best-estimate row only and is never a rating factor.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / mort_file, index_col=["sex", "age"])           # noqa: F821


def lapse_table():
    """The base surrender rates by year, read from *lapse_table.csv*.

    Indexed by the model's 0-based ``t``, so its first row is ``t = 0``, the first policy
    year.  These are the rates **before** the terminal-year override: in the final period
    the projection applies zero, because the end of that period is *Rentenbeginn* and the
    survivors leave as maturities rather than as surrenders.  The step at ``t = 11``
    (policy year 12) is the § 20 Abs. 1 Nr. 6 EStG tax threshold and is the shape's whole
    point; the levels are **[std]**.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / lapse_file, index_col="t")                     # noqa: F821


def freq_load_table():
    """The *Ratenzahlungszuschlag* multipliers by payment frequency.

    Read from *freq_load_table.csv*, indexed by ``prem_freq``: the surcharge for paying
    other than annually, as a multiplier on the annual-mode premium.  It multiplies the
    premium **collected** and does not enter the *Beitragssumme*, so it changes neither
    the acquisition charge nor the *Mindesttodesfallschutz* floor.
    """
    return pd.read_csv(                                              # noqa: F821
        input_dir() / freq_load_file, index_col="prem_freq")         # noqa: F821


# ---------------------------------------------------------------------------
# References

model_point_file = "model_point_table.csv"

index_return_file = "index_return_table.csv"

index_param_file = "index_param_table.csv"

surplus_rate_file = "surplus_rate_table.csv"

election_file = "election_table.csv"

mort_file = "mort_table.csv"

lapse_file = "lapse_table.csv"

freq_load_file = "freq_load_table.csv"

pd = ("Module", "pandas")
