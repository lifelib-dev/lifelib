# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Term_US_SEC` model; holds all formulas.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.Term_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is: ``Projection[3]``
is an ItemSpace projecting the table's fourth row, model point 4, the anchor cell in force
126 months at the valuation date, and :func:`point_id` is its label::

    >>> Projection[3].result_cf()          # one row per month from the valuation date
    >>> Projection[3].result_pols()        # the counts behind it
    >>> Projection[3].point_id()           # 4, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good.

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.Term_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.Term_US_S` is rewritten where it depends on where the projection starts, where it
must answer for a month outside cover, or where it read a month far ahead of its own. The
``min`` of the notes' M(1) rule and the ``max`` of the PLT grading,
:func:`plt_mort_factor_init_formula` and :func:`plt_mort_factor`, are rewritten with their
bounds second, as :func:`mort_rate` writes its cap, ``min(q, 1.0)``, in both models, so
that a NaN stays NaN; wherever its argument is a number, each is the float it would be
with its bound first. Every other formula is :mod:`~.Term_US_S`'s own, :func:`mort_rate`
among them. ``products/term_life/model-sec.md`` lists the rewritten cells with the reason
for each. Making it compile changed how each cell reads its inputs and spells its codes, and
no number: every model point attribute a projection cell uses is read as a number from a
``Data`` vector, every table as an array indexed by integers, and every timing and phase is
an int code (*Codes*, below).

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/term_life/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation. A test asserts this by round-tripping the model together
with its inputs.

:func:`~.Term_US_SEC.Data.input_dir` resolves the directory from
``_model.path.parent`` at run time, so the model works wherever the repository is
checked out. The four assumption tables are the files :mod:`~.Term_US_S` reads, read in
place; the model point table is this model's own. Each table has a filename Reference
and a reader Cells:

======================  ==========================  ==============================
Reference               Cells                       File
======================  ==========================  ==============================
model_point_file        data.model_point_table()    model_point_table_sec.csv
premium_rates_file      data.premium_rates()        premium_rates.csv
mort_table_file         data.mort_table()           mort_table.csv
class_factor_file       data.class_factor_table()   class_factor_table.csv
shock_lapse_file        data.shock_lapse_table()    shock_lapse_table.csv
======================  ==========================  ==============================

To swap in a licensed mortality basis, replace ``mort_table.csv`` with a same-schema
file, or point ``mort_table_file`` at a different name. No formula changes. Replacing
the file changes :mod:`~.Term_US_S` too, which reads the same one.

No cell here but :func:`model_point`, a reporting cell, reads the readers' DataFrames,
and the label accessors read through it. Every other reads :mod:`~.Term_US_SEC.Data`'s
vectors and arrays, one element at a time: a model point's attribute at its position,
``data.age_at_entry()[idx]``, decoded already into the number the formula needs; the
premium schedule at ``data.premium_rates_array()[premium_schedule(), y]``; the mortality
table at the attained age, ``data.mort_table_array()[age(t)]``. ``Data``'s docstring
lists them.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts — and, for the monthly grid, the
``duration_mth`` / ``duration`` / ``policy_year`` triple that ``savings.CashValue_SE``
and the UL family in this library use. What running in force adds is named as
``basiclife.BasicTerm_SE`` names it: ``duration_mth`` read from the model point,
``policy_count``, ``pols_new_biz``, ``pols_if_at`` with its ``BEF_NB`` and ``BEF_DECR``
timings, ``is_active`` and ``result_pols``. ``duration_mth_init``, the policy months
completed at the valuation date, takes ``UL_US_S``'s name; ``t_entry`` and
``expiry_mth`` are this model's own. What compiling adds is named as
``basiclife.BasicTerm_SC`` names it: ``idx``, ``point_id`` and the ``Data`` vectors under
their columns' names. A cell keyed by policy year rather than by month carries ``_py``.
The technical notes use compact actuarial symbols instead.

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however old the policy, period ``t`` runs from time ``t`` to time ``t + 1``, and
the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len` counts the months from
the valuation date to the end of cover. Row ``t`` is the same month for every point, so
the frames of a block line up and sum row by row.

``duration_mth(t)`` counts **policy months**, the months the policy has been in force at
time ``t``: ``duration_mth(t) = duration_mth_init() + t``, where
:func:`duration_mth_init` is read from the model point — positive for a policy in force
at the valuation date, 0 for one issued at it, ``-k`` for one issued ``k`` months later,
at most ten years later. It is the technical notes' month index. Everything contractual
reads it: the completed policy years ``duration(t) = duration_mth(t) // 12``, the
contractual 1-based label ``policy_year(t) = duration(t) + 1``, the attained age
``age(t) = age_at_entry() + duration(t)``, and through them the premium schedule, the
ART renewals, the shock lapse, the conversion window and the commission scale. The
anchor cell in force 126 months is in policy year 11 at attained age 45 at ``t = 0``,
and pays its next premium at ``t = 6``, its eleventh anniversary.

One input reads the valuation clock instead: expense inflation,
``inflation_factor(t) = (1 + inflation_rate) ** (t / 12)``, so that the maintenance
charge is in valuation-date dollars for every point alike. Acquisition is a flat
``expense_acq`` per policy issued, charged in the issue month and not inflated, as in
``basiclife.BasicTerm_SE``.

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.Term_US_S` computes, but for one difference by design: acquisition is charged
per policy issued, where :mod:`~.Term_US_S` charges it once per model point, whatever
the count. The two agree on :mod:`~.Term_US_S`'s own model points, which count one
policy each: there every cell the two share agrees at every argument
:mod:`~.Term_US_S` evaluates in its sweep, but for two whose meaning changed,
``pols_if_init``, now the count already in force at the valuation date, and
``model_point``, a row of another table. That is how the S worked example carries over,
and ``tests/test_model_conventions.py`` asserts it cell by cell.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, BEF_DECR)``, the
count carried in from ``t - 1`` (``BEF_NB``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, the first month on the books, and
nothing is counted outside cover (:func:`is_active`): before issue every count, and so
every cash flow, is zero.

.. rubric:: Codes

What :mod:`~.Term_US_S` spells as text, a timing or a phase, is here an int Reference
named as the text it replaces, so that every cell takes and returns C numbers. A call
site reads as it did, less the quotes: ``pols_if_at(t, BEF_DECR)``.

=============  =====  ===========================================================
Reference      Value  Meaning
=============  =====  ===========================================================
BEF_NB         0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR       1      :func:`pols_if_at`: that count plus month t's new business
PRE_ISSUE      0      :func:`phase`: before issue
LEVEL          1      :func:`phase`: in the level period
PLT            2      :func:`phase`: after the level period, before expiry
EXPIRED        3      :func:`phase`: from the month cover has ended
=============  =====  ===========================================================

A code a cell takes indexes that cell's cache, a C array of two timings a month for
``pols_if_at``, so codes are numbered densely from 0. Timings are numbered in the order of
their instants within the month, ``BEF_NB`` before ``BEF_DECR``, as in every SEC model,
and phases in their natural order. They are References, not cells, so the symbol map
below does not list them.

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`sex`, :func:`rate_class`, :func:`plan`
and :func:`premium_mode`, and the reports :func:`result_cf`, :func:`result_cf_annual` and
:func:`result_pols` return Python values, a table row, text and DataFrames, for a reader
and for the comparison with :mod:`~.Term_US_S`, which has every one of them but
:func:`result_pols`. No cell but these calls them: every other reads the number ``Data``
decoded from the same column instead, the plan's level period, the mode's cycle, the
class's factor, the schedule the four keys select. So they stay Python when the model
compiles, and every other cell returns a C ``bint``, ``long long`` or ``double``.

.. rubric:: Symbols

The two-speed structure is the library's convention, asserted by
``tests/test_model_conventions.py``: ``mort_rate(t)`` and ``lapse_rate(t)`` are the
**annual** rates of the policy year containing month ``t`` — the vectors the technical
notes tabulate — and ``mort_rate_mth(t)`` and ``lapse_rate_mth(t)`` are the monthly
rates actually applied, ``1 - (1 - q)^(1/12)``. The notes' month index is this model's
``duration_mth(t)``. The mapping is:

=================  ==============================  =========================================
Notes symbol       Cells                           Meaning
=================  ==============================  =========================================
x                  age_at_entry                    Issue age (ANB)
x + dur            age(t)                          Attained age in month t
n                  policy_term                     Level period in years
F                  sum_assured                     Face amount
(none)             point_id                        The model point's label in the table
(none)             policy_count                    Policies the model point stands for
(none)             duration_mth_init               Completed policy months at the valuation
                                                   date; -k if issued k months later
t                  duration_mth(t)                 The notes' month index: completed policy
                                                   months at month t
dur(t)             duration(t)                     Completed policy years at month t
dur(t) + 1         policy_year(t)                  Policy year, the 1-based contractual
                                                   label
12(95 - x)         expiry_mth                      Policy month at which cover ends
(frame)            proj_len                        Months from the valuation date to the
                                                   end of cover; frame ends at proj_len - 1
(none)             t_entry                         First month on the books
(none)             is_active(t)                    Whether month t is inside cover
l(t)               pols_if(t)                      In-force weighting month t: after new
                                                   business, before decrements
(none)             pols_if_at(t, timing)           In-force at time t, BEF_NB or BEF_DECR
(l(0))             pols_if_init                    In-force at the valuation date
(none)             pols_new_biz(t)                 Policies issued in month t
d(t)               pols_death(t)                   Deaths in month t
s(t)               pols_surv(t)                    Survivors to end of month t
x(t)               pols_lapse(t)                   Lapses at end of month t
c(t)               pols_conv(t)                    Conversions at end of month t
(none)             pols_maturity(t)                Expiries at attained age 95
q(t)               mort_rate(t)                    Annual mortality, all factors applied,
                                                   capped at 1
q_m(t)             mort_rate_mth(t)                The monthly rate actually applied
(q_base)           mort_rate_base(t)               Base table rate before factors
w(t)               lapse_rate(t)                   Annual lapse rate, incl. the shock
w_m(t)             lapse_rate_mth(t)               The monthly rate actually applied
w(n-1)             shock_lapse_rate                Shock lapse, in full at policy month
                                                   12n - 1
cv(t)              conv_rate(t)                    Annual conversion rate
cv_m(t)            conv_rate_mth(t)                The monthly rate actually applied
conv_elig(t)       conv_elig(t)                    Conversion eligibility
(window)           conv_elig_py(y)                 Whether policy year y is in the window
M(d)               plt_mort_factor(d)              PLT mortality deterioration,
                                                   d = policy_year - n
M(1)               plt_mort_factor_init            M(1) actually used
(M(1) rule)        plt_mort_factor_init_formula    The notes' formula for M(1)
J                  jump_ratio                      AP of policy year n + 1 over year n,
                                                   fee included
AP(t)              premium_pp_ann(t)               Guaranteed annualized premium, policy
                                                   year of t
(AP by year)       premium_pp_ann_py(y)            The same, for policy year y
(schedule)         premium_schedule                The point's guaranteed premium schedule
(modal)            premium_pp(t)                   Premium per policy actually due in
                                                   month t
(modal factor)     modal_factor                    Modal factor of the premium mode
(modal cycle)      prem_cycle                      Months between instalments
(due month)        prem_due(t)                     Whether a modal premium falls due in
                                                   month t
G(t)               premiums(t)                     Premium income
K(t)               commissions(t)                  Commission
k(t)               comm_rate(t)                    Commission rate
X(t)               premium_taxes(t)                Premium tax
E(t)               expenses(t)                     Acquisition + maintenance
1.02^(t/12)        inflation_factor(t)             Expense inflation, valuation clock
DC(t)              claims(t)                       Death claims
CV(t)              conv_credits(t)                 Conversion credit outflow
NetCF(t)           net_cf(t)                       Net cash flow
phase(t)           phase(t)                        PRE_ISSUE / LEVEL / PLT / EXPIRED, as
                                                   codes
(none)             result_cf_annual()              result_cf() summed into policy years
(none)             result_pols()                   The counts, one row per month
=================  ==============================  =========================================

Three notes on the mapping. The notes write deaths as ``d(t)`` while also using ``d``
as the post-level-term duration index in ``M(d)``; the ``pols_death`` / ``plt_mort_factor``
split removes that collision. The notes' ``x(t)`` (lapses) and ``X(t)`` (premium tax)
differ only by case, which ``pols_lapse`` and ``premium_taxes`` separate. And
``pols_maturity`` has no symbol in the notes at all — see below.

.. rubric:: The shock lapse is not spread

Every ordinary decrement is converted to a monthly rate at ``1 - (1 - q)^(1/12)``, so
twelve months of it compound back to exactly the annual rate the notes tabulate. The
shock lapse is the one exception the notes make explicitly: it is **not** spread, but
applied in full at the end of the final level-period month, the month whose
``duration_mth(t)`` is ``12n - 1``, immediately before the first ART premium falls due
at ``12n``. Its policy year's annual rate ``w(n-1)`` *is* the shock, so
:func:`lapse_rate_mth` returns zero in the other eleven months of that year and the
shock itself in the last one.

That is what makes the two grids reconcile: because the ordinary monthly rates
compound to the annual ones and the shock falls at a year boundary, the in-force
**at every policy anniversary** is identical to the annual-step model's, to
floating-point. The cash flows are not identical and are not meant to be: claims now
fall at the end of the month of death rather than the end of the policy year,
maintenance expense accrues monthly, and a modal premium is collected when it is
contractually due. Those timing differences are the reason for the monthly grid.
:func:`result_cf_annual` sums the frame into policy years so the two can be laid side
by side.

.. rubric:: Premium mode

``premium_pp(t)`` is the premium **actually collected in month t**: the model point's
``premium_mode`` picks the modal factor (:func:`modal_factor`) and the payment months
(:func:`prem_cycle`) — annual in month 0 of each policy year, semi-annual every sixth
month, quarterly every third, monthly every month — and the annualized guaranteed
premium ``AP(t)`` the notes tabulate is :func:`premium_pp_ann`. Modal loading is
inside the factor (twelve monthly payments come to 0.99996 of the annual premium, two
semi-annual instalments to 1.04 of it) exactly as the specimen prints it [S6]. The
jump ratio and the conversion credit are both on ``AP``, which is what keeps them
mode-independent; commission is a *rate* keyed by policy year applied to the premium
actually collected, so a modal payer earns it in instalments too.

.. rubric:: pols_maturity

The notes give the roll-forward as ``l(t+1) = l(t)(1-q_m)(1-cv_m)(1-w_m)`` and,
separately, the rule ``l(t) = 0 for x + duration(t) >= 95``. Those do not reconcile in
the last covered month, ``duration_mth(t) = expiry_mth() - 1``: its survivors neither
die, lapse nor convert — their coverage simply runs out. Without a term for that, the
roll-forward appears to lose lives with no cause. ``pols_maturity(t)`` names it, zero
in every month but that one, so that::

    pols_if(t) - pols_if_at(t + 1, BEF_NB)
        = pols_death(t) + pols_lapse(t) + pols_conv(t) + pols_maturity(t)

holds for every ``t`` in the frame, and ``pols_if(t + 1)`` adds ``pols_new_biz(t + 1)``
to the count on the left. It is bookkeeping determined by the notes' own rules, not an
added assumption. The name follows ``BasicTerm_S.pols_maturity``.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda idx: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point, its row of ``model_point_table_sec.csv``, as a Series.

    Row ``idx`` of the table, for a reader who wants every column at once: a reporting
    cell (the Space docstring), which no projection cell reads. Each reads its own
    ``Data`` vector instead.
    """
    return data.model_point_table().iloc[idx]                              # noqa: F821


def point_id():
    """The label of the selected model point, its ``point_id``, from ``Data.point_id``.

    ``Projection`` is indexed by position, ``idx``, as ``basiclife.BasicTerm_SC`` is; the
    label is what a reader finds in the table, so every refusal names it.
    """
    return int(data.point_id()[idx])                                       # noqa: F821


def age_at_entry():
    """The issue age (ANB) of the selected model point, from ``Data.age_at_entry``.

    The age at issue, not at the valuation date: ``age(0)`` is the attained age then.
    """
    return int(data.age_at_entry()[idx])                                   # noqa: F821


def sex():
    """The sex of the selected model point, as the table spells it.

    A reporting cell (the Space docstring): ``Data.premium_schedule`` joins the premium
    schedule by the column, and no projection cell reads it here.
    """
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point, as the table spells it.

    A reporting cell: ``Data.class_factor`` and ``Data.premium_schedule`` join the class
    factor and the premium schedule by the column, and no projection cell reads it here.
    """
    return model_point()["rate_class"]


def plan():
    """The plan code of the selected model point (T10 / T20 / T30).

    A reporting cell: ``Data.policy_term`` decodes the level period from the column, and
    no projection cell reads it here.
    """
    return model_point()["plan"]


def sum_assured():
    """The face amount of the selected model point, from ``Data.sum_assured``."""
    return float(data.sum_assured()[idx])                                  # noqa: F821


def policy_count():
    """The number of policies the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the policies in force then, before any
    month-0 event; any other point counts the policies it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Read from
    ``Data.policy_count``.
    """
    return float(data.policy_count()[idx])                                 # noqa: F821


def pols_if_init():
    """Policies in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose policies
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def premium_mode():
    """The premium mode of the selected model point: A, SA, Q or M [S6].

    A reporting cell: ``Data.prem_cycle`` decodes the months between instalments from the
    column, and :func:`modal_factor` selects the factor by them.
    """
    return model_point()["premium_mode"]


def band():
    """Face-amount band 1-4, from ``Data.band``: boundaries at $250,000 / $500,000 /
    $1,000,000 [S5], the four-band choice **[std]**; the anchor cell is band 1.

    ``Data`` joins the premium schedule by the band, so no projection cell reads this; it
    is kept for a reader, and for the comparison with ``Term_US_S``, which has it.
    """
    return int(data.band()[idx])                                           # noqa: F821


def policy_term():
    """The level premium period in years, from ``Data.policy_term``: ``T10`` is 10.

    ``Data`` decodes it from the plan code, as ``Term_US_S`` reads it, ``int(plan[1:])``.
    """
    return int(data.policy_term()[idx])                                    # noqa: F821


def expiry_mth():
    """The policy month at which cover ends: ``12 * (expiry_age - age_at_entry())``.

    Coverage expires at attained age 95, so this is the ``duration_mth`` of the first
    month not covered, and the last covered month is ``expiry_mth() - 1``. It is
    ``Term_US_S``'s frame length, counted from issue on the policy clock;
    :func:`proj_len` counts from the valuation date instead.
    """
    return 12 * (expiry_age - age_at_entry())                       # noqa: F821


def proj_len():
    """The number of months from the valuation date to the end of cover.

    ``expiry_mth() - duration_mth_init()``: 720 for the anchor cell issued at ``t = 0``,
    594 for it in force 126 months, and 723 for it issued 3 months after the valuation
    date. The frame is ``t = 0, 1, ..., proj_len() - 1``; ``proj_len()`` is its exclusive
    end and the row count of :func:`result_cf`.

    Three kinds of point raise here, naming the point, rather than project nothing or a
    frame the contract does not have:

    * one whose cover ended at or before the valuation date, which an in-force extract
      should not carry;
    * one whose plan's level period is below ``policy_term_min``, 10 years, the shortest
      plan's (``product-spec.md``), such as ``T5`` or ``T0``;
    * one issued below ``issue_age_min``, 18, the youngest issue age of every plan.

    ``Data`` reads the last two as ``Term_US_S`` reads its columns. They are refused here
    because ``spec_sec.py`` sizes the compiled model's caches from the contract, cover from
    18 to ``expiry_age``, 95, the PLT years after the shortest level period, and the
    shipped future horizon, and on such a point the compiled model would run past them,
    where modelx reads on. Every report reads this cell first, so modelx and the compiled
    model refuse such a point alike. The three References are the contract the caches
    hold: lowering ``issue_age_min`` or ``policy_term_min``, or raising ``expiry_age``,
    needs the spec's sizes raised and the model rebuilt, as a longer
    ``Data.future_horizon_mth`` does.
    """
    n = expiry_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past the end of cover, policy month {expiry_mth()}")
    if policy_term() < policy_term_min:                              # noqa: F821
        raise ValueError(f"point_id {point_id()}: the plan's level period, "
                         f"{policy_term()} years, is below policy_term_min, "
                         f"{policy_term_min}")                       # noqa: F821
    if age_at_entry() < issue_age_min:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is below "
                         f"issue_age_min, {issue_age_min}")          # noqa: F821
    return n


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 126 for a policy issued 126 months before the
    valuation date, 0 for one issued at it, and -3 for one to be issued 3 months after
    it, which ``Data`` admits up to ``future_horizon_mth`` months ahead. It is read as
    ``basiclife.BasicTerm_SE`` reads it, and is the one fact the policy clock takes from
    the model point, its element of ``Data.duration_mth``.
    """
    return int(data.duration_mth()[idx])                                   # noqa: F821


def duration_mth(t):
    """Completed policy months at the start of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together. A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame. Negative before issue. Everything
    contractual reads this clock, through :func:`duration`, :func:`policy_year` and
    :func:`age`.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the policy is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later. It is the base of the count recursion: :func:`pols_if_at` opens
    there, from :func:`pols_if_init`, and reads no month before it.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and not yet expired.

    ``0 <= duration_mth(t) < expiry_mth()``. False before issue and from the month cover
    has ended. Outside cover every count is zero, and so every cash flow; no count cell
    evaluates a rate there, and no table is read at a policy year or an attained age the
    policy does not have.
    """
    return 0 <= duration_mth(t) < expiry_mth()


def duration(t):
    """Completed policy years at the start of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year, and negative before issue. Every contractual
    schedule in this product is annual, so this is what the attained age and the premium
    schedule are read at.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """The contractual policy year containing month t, ``duration(t) + 1``.

    A 1-based label on the policy clock, never indexed by: the guaranteed premium
    schedule in ``premium_rates.csv`` is keyed by it, and so are the annual decrement
    vectors. It is 0 or less before issue, where nothing reads a table by it.
    """
    return duration(t) + 1


def age(t):
    """The attained age (ANB) in month t: ``age_at_entry() + duration(t)``.

    Age changes on the policy anniversary rather than on the birthday, which is the
    ANB convention the whole model is built on **[std]**.
    """
    return age_at_entry() + duration(t)


def modal_factor():
    """The model point's modal factor: the fraction of AP collected per instalment [S6].

    Annual 1.0, semi-annual 0.52, quarterly 0.27, monthly 0.08333 — the specimen's own
    scale, so the modal loading is inside the factor. Each is its own Reference, so a
    carrier's own scale drops in without a formula change. The factor is selected by
    :func:`prem_cycle`, which is one to one with the mode, 12, 6, 3 and 1 months for A,
    SA, Q and M; ``Data.prem_cycle`` refuses any other mode, naming the point, so the
    last branch is the monthly factor.
    """
    c = prem_cycle()
    if c == 12:
        return modal_factor_a                                        # noqa: F821
    elif c == 6:
        return modal_factor_sa                                       # noqa: F821
    elif c == 3:
        return modal_factor_q                                        # noqa: F821
    else:
        return modal_factor_m                                        # noqa: F821


def prem_cycle():
    """Months between premium instalments: A 12, SA 6, Q 3, M 1, from ``Data.prem_cycle``.

    Arithmetic of the mode rather than an assumption, so ``Data`` decodes it from the
    mode rather than a Reference holding it.
    """
    return int(data.prem_cycle()[idx])                                     # noqa: F821


def prem_due(t):
    """Whether a modal premium falls due at the beginning of month t.

    Payments start at issue and repeat on the mode's own cycle on the policy clock,
    ``duration_mth(t) % prem_cycle() == 0``: annual in month 0 of each policy year,
    semi-annual every sixth month, quarterly every third, monthly every month. None falls
    due outside cover. A point in force mid-year pays its next instalment on that cycle,
    so the anchor cell in force 126 months pays nothing until ``t = 6``.
    """
    return is_active(t) and duration_mth(t) % prem_cycle() == 0


def premium_pp_ann(t):
    """AP(t): the guaranteed **annualized** gross premium per policy, fee included.

    The notes' ``AP`` for the policy year containing month t,
    ``premium_pp_ann_py(policy_year(t))``, and zero outside cover, where the policy has
    no policy year to look up. It is the base for the conversion credit, which should not
    move with the premium mode; :func:`premium_pp` is what is actually collected in
    month t, and it is that instalment — not ``AP`` — that :func:`commissions` and
    :func:`premium_taxes` are charged on.
    """
    return premium_pp_ann_py(policy_year(t)) if is_active(t) else 0.0


def premium_schedule():
    """The selected model point's guaranteed premium schedule, from
    ``Data.premium_schedule``: its row of ``Data.premium_rates_array``.

    ``Data`` joins it by the point's plan, sex, rate class and band, the key
    ``Term_US_S`` looks the premium up by. It is 0 where *premium_rates.csv* has no
    schedule for that key, a schedule whose extent holds no policy year.
    """
    return int(data.premium_schedule()[idx])                               # noqa: F821


def premium_pp_ann_py(y):
    """AP of policy year y, read from the point's schedule of ``premium_rates.csv``.

    The schedule is keyed by the contractual, 1-based policy year, so this is the cell
    that reads it, for any year the contract has: :func:`premium_pp_ann` at
    ``policy_year(t)``, and :func:`jump_ratio` at policy years ``n`` and ``n + 1``,
    which need not fall in the frame: the point in force 126 months is in year ``n + 1``
    at the valuation date, with year ``n`` behind it.

    It is the one cell that reads ``Data.premium_rates_array``, at
    ``[premium_schedule(), y]``, and it checks the year against both ends of the
    schedule first, ``Data.premium_first_year`` and ``Data.premium_last_year``. A year
    outside them raises ``ValueError``, naming the point and the year, where
    ``Term_US_S``'s lookup raised ``KeyError``, rather than reading the array's padding.
    """
    s = premium_schedule()
    if y < data.premium_first_year()[s] or y > data.premium_last_year()[s]:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: premium_rates.csv has no premium for "
                         f"policy year {y}")
    return float(data.premium_rates_array()[s, y])                        # noqa: F821


def premium_pp(t):
    """The premium per policy actually due at the beginning of month t.

    ``modal_factor() * AP(t)`` in a payment month, zero otherwise.
    """
    return modal_factor() * premium_pp_ann(t) if prem_due(t) else 0.0


def jump_ratio():
    """Initial premium jump ratio, fee included: the first ART annualized premium over the
    last level one, ``premium_pp_ann_py(n + 1) / premium_pp_ann_py(n)``.

    Policy years n + 1 and n, read by policy year. ``Term_US_S`` reads them at months
    ``12n`` and ``12n - 1``, which are those years only on a policy issued at ``t = 0``.
    """
    n = policy_term()
    return premium_pp_ann_py(n + 1) / premium_pp_ann_py(n)


def plt_mort_factor_init_formula():
    """The notes' rule for M(1): min(8.0, 1 + 0.55*(J-1)) **[std]**.

    Returns 3.4514 for the anchor cell, where the worked example uses 3.50. Not used
    unless the model point leaves plt_mort_factor_override blank. Written with the bound
    second, ``min(1.0 + 0.55 * (J - 1.0), 8.0)``, as :func:`mort_rate` writes its cap, so
    that a NaN jump ratio gives NaN rather than 8.0; wherever ``J`` is a number it is the
    notes' value.
    """
    return min(1.0 + 0.55 * (jump_ratio() - 1.0), 8.0)


def plt_mort_factor_init():
    """M(1) actually used: the model point's override if given, else the formula.

    ``Data.has_plt_mort_factor_override`` says whether the point gives one, and
    ``Data.plt_mort_factor_override`` holds it. A blank is the flag's 0, beside a 0.0,
    so no NaN reaches this formula and none is tested for here.
    """
    if data.has_plt_mort_factor_override()[idx]:                           # noqa: F821
        return float(data.plt_mort_factor_override()[idx])                 # noqa: F821
    return plt_mort_factor_init_formula()


def plt_mort_factor(d):
    """Post-level-term mortality deterioration at PLT duration d; grades to 2.00 **[std]**.

    ``d`` is the notes' PLT duration in **years**, ``d = policy_year(t) - n``: ``d = 1``
    in the first post-level-term policy year (``duration_mth(t) = 12n .. 12n + 11``). It
    is neither the frame index ``t`` nor a policy month.

    The floor is written second, ``max(M(1) - 0.15 * (d - 1), 2.0)``, as
    :func:`mort_rate` writes its cap, so that a NaN M(1) gives NaN rather than 2.0;
    wherever M(1) is a number it is the notes' value.
    """
    return max(plt_mort_factor_init() - 0.15 * (d - 1), 2.0) if d >= 1 else 1.0


def class_factor():
    """Underwriting-class multiplier on the base mortality table **[std]**.

    From ``Data.class_factor``, which joins the point's class to
    *class_factor_table.csv*.
    """
    return float(data.class_factor()[idx])                                 # noqa: F821


def mort_rate_base(t):
    """Base-table **annual** mortality rate at the attained age in month t, ``age(t)``.

    Zero outside cover, where ``age(t)`` is not an age the policy reaches in force.
    Inside it, this is the one cell that reads ``Data.mort_table_array``, which is
    indexed by the age itself. An age outside the table's, ``Data.mort_age_first`` to
    ``Data.mort_age_last``, raises ``ValueError``, naming the point and the age, where
    ``Term_US_S``'s lookup raised ``KeyError``, rather than reading the array's padding.
    """
    if not is_active(t):
        return 0.0
    a = age(t)
    if a < data.mort_age_first() or a > data.mort_age_last():              # noqa: F821
        raise ValueError(f"point_id {point_id()}: mort_table.csv has no rate at attained "
                         f"age {a}")
    return float(data.mort_table_array()[a])                               # noqa: F821


def mort_rate(t):
    """The **annual** mortality rate of the policy year containing month t, at most 1.

    Base x class factor x PLT deterioration, capped at 1, as ``Term_US_S`` caps it,
    ``min(q, 1.0)``: the product first, the float bound second. ``min`` keeps its first
    argument unless a later one compares smaller, in Python and in the compiled cell
    alike, and no comparison with NaN holds, so ``min(1.0, q)`` would be 1.0 where ``q``
    is NaN, a blank input read as certain death, silently. ``min(q, 1.0)`` is NaN there,
    and wherever ``q`` is a number it is the float ``min(1.0, q)`` is, 1.0 included.
    ``Data`` refuses a blank, text or infinite value wherever the product reads one, so
    that none reaches it. The PLT duration is ``d = policy_year(t) - n``, so the
    multiplier applies from ``duration_mth(t) = 12n`` (``d = 1``) on. :func:`mort_rate_mth`
    is the rate actually applied in the month.

    Past 1 the monthly rate, ``1 - (1 - q)^(1/12)``, has no real value. At 1 it is 1, and
    every policy in force at the start of the month dies in it. On the shipped mortality
    and class tables the product passes 1 only after the level period. At the issue ages
    ``product-spec.md`` admits, it first does so, at the lowest M(1), in the tobacco class
    on the twenty-year plan issued at 65, its oldest tobacco issue age: at attained age
    94, once M(1) passes 5.9152, which the notes' rule gives at a jump ratio past 9.9367.
    There a non-tobacco class needs an M(1) above 8, the most the rule gives, so an
    override. The model does not refuse an older issue age. Where the first PLT year falls
    at attained age 94, as on the ten-year plan issued at 84, the product passes 1 there
    once M(1) passes 4.5652 in the tobacco class and 7.9891 in the standard non-tobacco
    class, the least M(1) that does so on any point the model projects.
    """
    d = policy_year(t) - policy_term()
    return min(mort_rate_base(t) * class_factor()
               * (plt_mort_factor(d) if d >= 1 else 1.0), 1.0)


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate applied in month t **[std]**.

    ``1 - (1 - q)^(1/12)`` on the policy year's annual rate, so twelve months of it
    compound back to exactly that rate — the notes' own conversion.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def shock_lapse_rate():
    """Shock lapse at the end of the level period, by jump-ratio bucket **[std]**.

    The rate of the first bucket of *shock_lapse_table.csv*, in the table's order, whose
    range ``jump_lo < J <= jump_hi`` holds the jump ratio, and the last bucket's where
    none does, as ``Term_US_S`` reads the table: a loop over ``Data``'s three bucket
    vectors, which runs once for a point.
    """
    j = jump_ratio()
    n = data.shock_lapse_buckets()                                         # noqa: F821
    for i in range(n):
        if data.shock_lapse_jump_lo()[i] < j <= data.shock_lapse_jump_hi()[i]:  # noqa: F821
            return float(data.shock_lapse_bucket_rate()[i])                # noqa: F821
    return float(data.shock_lapse_bucket_rate()[n - 1])                    # noqa: F821


def lapse_rate(t):
    """The **annual** lapse rate of the policy year containing month t **[std]**.

    The notes' ``w`` vector, keyed by ``duration(t)``. Level period
    (``duration = 0 .. n-1``): 6% in policy year 1, 5% in year 2, 4% in years 3..n-2,
    6% anticipatory in year n-1, and the shock in year n. Post-level term: 30%, 15%,
    then 10% by PLT duration ``d = policy_year(t) - n``.

    :func:`lapse_rate_mth` is the rate actually applied in the month, and it treats the
    shock year specially — see there.
    """
    n = policy_term()
    y = duration(t)
    if y < n - 1:
        if y == 0:
            return 0.06
        if y == 1:
            return 0.05
        if y == n - 2:
            return 0.06
        return 0.04
    if y == n - 1:
        return shock_lapse_rate()
    d = policy_year(t) - n
    return 0.30 if d == 1 else 0.15 if d == 2 else 0.10


def lapse_rate_mth(t):
    """w_m(t): the lapse rate applied at the end of month t **[std]**.

    ``1 - (1 - w)^(1/12)`` on the policy year's annual rate in every month except those
    of the final level-period year. The notes are explicit that the shock is **not**
    spread: that year's annual rate *is* the shock, so it falls in full at the end of
    the final level-period month, the month with ``duration_mth(t) = 12n - 1`` —
    immediately before the first ART premium is due at ``12n`` — and the other eleven
    months of the year carry no ordinary lapse at all.
    """
    n = policy_term()
    if duration(t) == n - 1:
        return shock_lapse_rate() if duration_mth(t) == 12 * n - 1 else 0.0
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def conv_elig(t):
    """True while convertible: inside cover, within the level period, attained age below 70.

    ``conv_elig_py(policy_year(t))`` for a month inside cover, False outside it.
    """
    return is_active(t) and conv_elig_py(policy_year(t))


def conv_elig_py(y):
    """Whether policy year y lies in the conversion window.

    Within the level period, ``y <= n``, and at an attained age below 70,
    ``age_at_entry() + y - 1 < 70``: the window ends at
    ``min(end of level period, attained age 70)``. Keyed by policy year, so that
    :func:`conv_rate` can ask about the year after month t's without reading a month of
    the frame twelve months ahead.
    """
    return y <= policy_term() and age_at_entry() + y - 1 < 70


def conv_rate(t):
    """The **annual** conversion rate of the policy year containing month t **[std]**.

    Zero outside the eligibility window; ``conv_rate_final`` in the last eligible
    policy year, the one whose successor is outside the window, and ``conv_rate_base``
    before it. Both ship at 0, as the worked example requires.
    """
    if not conv_elig(t):
        return 0.0
    final = not conv_elig_py(policy_year(t) + 1)
    return conv_rate_final if final else conv_rate_base             # noqa: F821


def conv_rate_mth(t):
    """cv_m(t): the monthly conversion rate applied at the end of month t **[std]**.

    ``1 - (1 - cv)^(1/12)`` on the policy year's annual rate, the same conversion the
    other voluntary decrement takes.
    """
    return 1.0 - (1.0 - conv_rate(t)) ** (1.0 / 12.0)


def phase(t):
    """The phase of month t, as a code: PRE_ISSUE, LEVEL (``duration < n``), PLT (to
    expiry) or EXPIRED, the int References of the Space docstring's *Codes*.

    On the policy clock: ``PRE_ISSUE`` while ``duration_mth(t) < 0``, the months before a
    future point is issued, and ``EXPIRED`` from ``duration_mth(t) = expiry_mth()`` on,
    which is ``t = proj_len()``.
    """
    if duration_mth(t) < 0:
        return PRE_ISSUE                                             # noqa: F821
    if duration_mth(t) >= expiry_mth():
        return EXPIRED                                               # noqa: F821
    return LEVEL if duration(t) < policy_term() else PLT             # noqa: F821


def pols_if(t):
    """Number of policies in force at time t, the count that weights row t.

    ``pols_if_at(t, BEF_DECR)``: the count carried in from month t - 1, plus month t's
    new business, before month t's decrements. On a point issued at ``t = 0`` that is
    exactly ``Term_US_S``'s ``pols_if``, the count at the start of the month. It is
    ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is the
    count before maturity. Zero outside cover: before issue, and from ``t = proj_len()``
    on, when coverage has expired at attained age 95.
    """
    return pols_if_at(t, BEF_DECR)                                   # noqa: F821


def pols_if_at(t, timing):
    """Number of policies in force at time t, at the instant ``timing`` names.

    ``BEF_NB``
        The count carried in from month t - 1, before month t's new business: the
        survivors of month t - 1's deaths, conversions and lapses, out of month t - 1's
        ``BEF_DECR`` count. At :func:`t_entry`, the first month on the books, it is
        :func:`pols_if_init`, the count in force at the valuation date (0 for a point
        issued at or after it), and the recursion reads no earlier month. Zero outside
        cover, so the survivors of the last covered month leave as :func:`pols_maturity`.
    ``BEF_DECR``
        ``BEF_NB`` plus :func:`pols_new_biz`: the count that weights month t, which
        :func:`pols_if` returns.

    These are ``basiclife.BasicTerm_SE``'s names, as int References, 0 and 1 (the Space
    docstring's *Codes*). Its ``"BEF_MAT"`` is not adopted: here the policies expire at
    the end of the last covered month, as ``Term_US_S`` has it, and any timing but these
    two raises.

    ``BEF_NB`` forms month t - 1's ``BEF_DECR`` count itself, as ``BEF_NB`` plus
    :func:`pols_new_biz` at t - 1, the same sum in the same order, rather than calling for
    it. So the chain of calls from month t back to :func:`t_entry` is one cell a month,
    as deep as ``Term_US_S``'s ``pols_if`` chain and no deeper: a compiled model runs
    that chain on the C stack.
    """
    if timing == BEF_NB:                                             # noqa: F821
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1))       # noqa: F821
                * (1 - mort_rate_mth(t - 1)) * (1 - conv_rate_mth(t - 1))
                * (1 - lapse_rate_mth(t - 1)))
    elif timing == BEF_DECR:                                         # noqa: F821
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)                 # noqa: F821
    else:
        raise ValueError("invalid timing")


def pols_new_biz(t):
    """Number of policies issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point
    issued at the valuation date, ``t = k`` for one issued ``k`` months later. A point
    already in force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_death(t):
    """Number of deaths occurring in month t; zero outside cover."""
    return pols_if(t) * mort_rate_mth(t) if is_active(t) else 0.0


def pols_surv(t):
    """Number of policies surviving to the end of month t, before voluntary decrements.

    Zero outside cover.
    """
    return pols_if(t) * (1 - mort_rate_mth(t)) if is_active(t) else 0.0


def pols_conv(t):
    """Number of conversions at the end of month t; zero outside cover."""
    return pols_surv(t) * conv_rate_mth(t) if is_active(t) else 0.0


def pols_lapse(t):
    """Number of lapses at the end of month t, including the shock in the month with
    ``duration_mth(t) = 12n - 1``; zero outside cover."""
    if not is_active(t):
        return 0.0
    return pols_surv(t) * (1 - conv_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of policies whose coverage ends at attained age 95.

    Non-zero only in the last covered month, ``duration_mth(t) = expiry_mth() - 1``,
    which is the frame's last row, ``t = proj_len() - 1``. Not a decrement - the contract
    runs out - but needed for the in-force roll-forward to close; see the Space
    docstring.
    """
    if duration_mth(t) != expiry_mth() - 1:
        return 0.0
    return (pols_if(t) * (1 - mort_rate_mth(t))
            * (1 - conv_rate_mth(t)) * (1 - lapse_rate_mth(t)))


def comm_rate(t):
    """Commission rate **[std]**: 80% in policy year 1 (``duration(t) == 0``), 5% to the
    end of the level period, 2% after. It is a rate on the premium collected, so a
    modal payer pays it in instalments too.

    Zero outside cover, where the month has no policy year: before issue ``duration(t)``
    is negative, which the scale would otherwise read as a level-period year.
    """
    if not is_active(t):
        return 0.0
    y = duration(t)
    return 0.80 if y == 0 else (0.05 if y < policy_term() else 0.02)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + inflation_rate) ** (t / 12)``.

    On the **valuation** clock: ``t`` counts months from the valuation date, so the
    maintenance charge it inflates is in valuation-date dollars, whatever the policy's
    age, and every point of a block inflates alike. ``Term_US_S`` inflates from issue; on
    a point issued at ``t = 0`` the two are the same. Acquisition is not inflated (see
    :func:`expenses`). Compounded on the monthly grid rather than stepped at
    anniversaries: on an annual model the factor can only move once a year, and the
    monthly refinement is one of the things the finer grid buys.
    """
    return (1 + inflation_rate) ** (t / 12)                          # noqa: F821


def premiums(t):
    """Premium income in month t, at the beginning of the month."""
    return premium_pp(t) * pols_if(t)


def commissions(t):
    """Commission in month t **[std]**."""
    return comm_rate(t) * premiums(t)


def premium_taxes(t):
    """Premium tax in month t **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def expenses(t):
    """Acquisition on new business and inflating maintenance expenses in month t **[std]**.

    Acquisition is ``expense_acq`` per policy issued, ``expense_acq * pols_new_biz(t)``:
    in the issue month, never for a point already in force at the valuation date, and
    not inflated, as in ``basiclife.BasicTerm_SE``, so a policy written after the
    valuation date costs ``expense_acq`` in the dollars of its issue month.
    ``Term_US_S`` charges it once, at ``t = 0``, whatever the count. One twelfth of the
    annual maintenance charge accrues each month, inflated on the valuation clock, so a
    policy that runs a full year carries the same charge as it did on the annual grid —
    but it is now borne by the in-force of each month rather than of the anniversary,
    which is what makes a decrementing block cost less.
    """
    return (expense_acq * pols_new_biz(t)                           # noqa: F821
            + expense_maint / 12 * inflation_factor(t) * pols_if(t))  # noqa: F821


def claims(t):
    """Death claims incurred in month t, paid at the end of the month.

    Face amount only: the notes' simplification (i) — the pro-rata unearned-premium
    refund and the due-unpaid-premium deduction on death [S6] are not modelled. On the
    monthly grid the item is bounded by one modal premium, so it is immaterial by
    construction for a monthly payer and at most one annual premium on the deceased
    cohort for an annual one.
    """
    return sum_assured() * pols_death(t)


def conv_credits(t):
    """Conversion credit outflow: one **annualized** premium per conversion, after the
    first policy year (``duration(t) >= 1``). The credit is contractual and stated on
    the annual premium [S6], so it does not move with the premium mode."""
    return premium_pp_ann(t) * pols_conv(t) if duration(t) >= 1 else 0.0


def net_cf(t):
    """Net cash flow in month t."""
    return (premiums(t) - commissions(t) - premium_taxes(t)
            - expenses(t) - claims(t) - conv_credits(t))


def result_cf():
    """Result table of cashflows, one row per month ``t = 0 .. proj_len() - 1``.

    Row 0 is the valuation month for every model point, so the frames of a block line up
    and sum row by row. A point issued after the valuation date has zeros until its issue
    month. The columns are ``Term_US_S``'s.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims": [claims(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "conv_credits": [conv_credits(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by ``policy_year``.

    Every cash flow column is the total of the year's months in the frame, and
    ``pols_if`` is the count in its first month in the frame. The months before issue
    belong to no policy year and are left out. On a point issued at ``t = 0`` every year
    is whole, ``pols_if`` is the count entering it, and the table is ``Term_US_S``'s. A
    point in force at the valuation date may open part-way through a policy year, as the
    point in force 126 months does; its first row then holds the rest of that year only,
    and its ``pols_if`` is the count at the valuation date. On an anniversary, as at 12
    months, the first row is a whole year.

    On the shipped annual-mode points, in every policy year the frame holds whole, the two
    grids agree exactly on five columns —
    ``pols_if``, ``premiums``, ``commissions``, ``premium_taxes`` and ``conv_credits`` —
    because an annual premium is collected on the anniversary and weighted by the
    anniversary in force under either grid, and the other three are rates on it. They do
    **not** agree on ``claims`` or ``expenses``, which now fall where they happen rather
    than at the anniversary, and so not on ``net_cf``. That gap is the point of the finer
    grid — see the Space docstring.
    """
    df = result_cf()
    df = df.loc[[t for t in df.index if is_active(t)]]
    years = pd.Index([policy_year(t) for t in df.index], name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_pols():
    """The policy counts, one row per month ``t = 0 .. proj_len() - 1``.

    The counts :func:`result_cf` weights its rows by, and how they move, as
    ``basiclife.BasicTerm_SE``'s ``result_pols`` sets them out: ``pols_if``, the count
    of month t; ``pols_new_biz``, the part of it issued in month t; then month t's
    deaths, conversions and lapses in processing order, and the expiries of the last
    covered month. Row by row, ``pols_if`` at ``t + 1`` is ``pols_if`` less the four
    outflows of month t, plus the new business of month ``t + 1``.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_conv": [pols_conv(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

BEF_NB = 0

BEF_DECR = 1

PRE_ISSUE = 0

LEVEL = 1

PLT = 2

EXPIRED = 3

expiry_age = 95

issue_age_min = 18

policy_term_min = 10

modal_factor_a = 1.0

modal_factor_sa = 0.52

modal_factor_q = 0.27

modal_factor_m = 0.08333

premium_tax_rate = 0.02

expense_acq = 300.0

expense_maint = 30.0

inflation_rate = 0.02

conv_rate_base = 0.0

conv_rate_final = 0.0

pd = ("Module", "pandas")
