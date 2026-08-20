# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Term_UK_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy years**, 1-based: ``t = 1`` is the first policy year and
``t = proj_len() = policy_term()`` the last. There is nothing after it — cover ceases
at the end of the term with no maturity value, no renewal and no conversion.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/term_assurance/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_UK_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Term_UK_A.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
select_factor_file      data.select_factor_table()      select_factor_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind``
string, ``pols_if_at(t, timing)`` for the within-year in-force reads. The technical
notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
shape                      shape()                         level / decreasing / fib
x                          age_at_entry(life)              Issue age (ANB), life 1 or 2
x + t - 1                  age(t, life)                    Attained age in policy year t
(none)                     sex(life), smoker(life)         Rating factors of each life
n                          policy_term()                   Term in years
N = 12n                    term_mths()                     Term in months
t = 1..n                   proj_len()                      Last policy year
(none)                     proj_start()                    First projected policy year
(none)                     duration_inforce()              Years already elapsed at t = 0
(none)                     duration(t)                     Completed years since entry
SA0                        sum_assured()                   Initial sum assured
I                          fib_income()                    FIB income per month
j                          sched_rate()                    Decreasing schedule rate p.a.
j_m                        sched_rate_mth()                (1+j)^(1/12) - 1
B(k)                       benefit_sched(k)                Decreasing benefit at month k
DB(t)                      benefit_pp(t)                   Death/TI benefit per policy
idx(t)                     idx_factor(t)                   Cover indexation factor
idx_p(t)                   idx_prem_factor(t)              Premium indexation factor
(RPI scenario)             rpi_rate                        Flat RPI assumption, 3%
P_m                        premium_mth_pp()                Monthly premium
P_a x idx_p(t)             premium_pp(t)                   Annualized premium in year t
(table)                    mort_rate_base(t, life)         Table rate before adjustment
(select)                   select_factor(t)                Select-duration factor
(proxy scaling)            mort_scale                      "00" to "16" Series factor
(none)                     mort_rate_life(t, life)         Per-life rate, all factors
q(t), q_joint              mort_rate(t)                    Policy decrement, incl. TI
(none)                     mort_basis()                    applied or select run
lambda                     sel_lapse_lambda                Selective-lapsation loading
w_ref                      sel_lapse_ref                   Selective-lapsation threshold
w_cum(t)                   lapse_cum(t)                    Cumulative lapse proportion
(none)                     sel_lapse_factor(t)             Mortality loading on persisters
(table)                    lapse_rate_base(t)              Table lapse rate
M_reb(t)                   rebroke_factor(t)               Rebroking multiplier
w(t)                       lapse_rate(t)                   Lapse rate applied in year t
l(t)                       pols_if(t)                      In force at the start of year t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
D(t)                       pols_death(t)                   Expected death/TI claims
(none)                     pols_lapse(t)                   Lapses at the end of year t
(none)                     pols_maturity(t)                Expiries at the end of the term
(none)                     pols_payer(t)                   Policies actually paying premium
inc(t)                     wop_inc_rate                    WOP incidence rate
(recovery)                 wop_rec_rate                    WOP recovery rate
(none)                     wop_waived_frac(t)              Fraction with premiums waived
FIBcum(t)                  fib_cum(t)                      FIB streams already in payment
a(m)                       annuity_certain_factor(m)       m-month annuity-certain factor
r_c                        fib_commute_disc_rate           FIB commutation rate, 3%
CV(k)                      fib_commute_pp(t)               Commuted value of one stream
(take-up)                  fib_commute_rate()              Proportion of FIB claims commuted
P_a x idx_p x l            premiums(t)                     Premium income
DB(t) x D(t), Claims_fib   claims(t, kind)                 Benefit outgo by kind
ec x D(t)                  claim_expenses(t)               Claim expense outgo
E0, e(t)                   expenses(t)                     Acquisition + maintenance
(none)                     inflation_factor(t)             Expense inflation factor
c0                         comm_init_pp()                  Initial commission per policy
c_r                        comm_renewal_rate               Renewal commission rate
(clawback)                 comm_clawback(t)                Commission recovered on lapse
c0, c_r x premiums         commissions(t)                  Commission outgo, net
CF(t)                      net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ==========================

Four names needed care.

The notes use ``q(t)`` both for the per-life table rate and for the decrement actually
applied to the policy, which on a joint first-death policy is
``1 - (1-q_1)(1-q_2)``. :func:`mort_rate_life` is the per-life rate and
:func:`mort_rate` the policy decrement, so the joint combination has somewhere to live
and the single-life case collapses to the same number.

``w(t)`` is the lapse rate and ``w_cum(t)`` the cumulative lapse proportion that drives
the selective-lapsation loading on *mortality*. Spelling them ``lapse_rate`` and
``lapse_cum`` keeps the second from reading as a running total of the first, which it
is not: it is a proportion of the original cohort, and the loading it feeds moves
claims, not lapses.

``E0`` and ``e(t)`` are the acquisition and maintenance expenses; both are inside
:func:`expenses`, which is the library-wide name, with the claim expense ``ec x D(t)``
kept out of it under :func:`claim_expenses` because the notes' worked-example table
prints the two as separate columns.

``pols_maturity`` has no symbol in the notes at all. The notes give the roll-forward as
``l(t+1) = l(t)(1-q)(1-w)`` and, separately, terminate everything at ``t = n``. Those
do not reconcile in the final policy year: its survivors neither die nor lapse — their
cover simply runs out — so without a term for that the roll-forward appears to lose
lives with no cause. :func:`pols_maturity` names it, zero in every year but the last,
so that

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)

holds for every ``t``; :func:`check_pols_roll_fwd` asserts it. It is bookkeeping
determined by the notes' own rules, not an added assumption, and the name follows
``BasicTerm_S.pols_maturity``. Note that it is *not* a maturity **benefit**: the amount
paid is nil.

.. rubric:: No tail states

This is the structural difference from ``Term_US_A``, and the notes list importing a
U.S.-style post-level-term tail as a modelling pitfall. A UK term policy expires at
``t = n``: there is no jump to ART rates, no post-level-term shock lapse, no mortality
deterioration factor and no conversion option, so none of those cells exist here. What
does exist and has no U.S. analogue is the family income benefit ledger below.

.. rubric:: Terminal illness is not an extra benefit

Terminal illness is a 100% **acceleration** of the death benefit under a two-limb
12-month definition, not an additional cover: one decrement, one payment. Adding a
separate terminal-illness decrement double-counts claims, which is the notes'
first-listed pitfall, and the CMI "16" Series assured lives tables already include
terminal illness. So ``mort_rate`` is the combined death-and-terminal-illness rate and
there is no ``ti_rate`` anywhere in the model. The acceleration shifts payment earlier
by less than twelve months, which the annual grid cannot see in any case.

.. rubric:: The family income benefit ledger

A death in month ``k`` on the ``fib`` shape triggers ``N - k`` monthly instalments of
``I``, in arrears, ending at month ``N``. The instalments are an **annuity-certain**:
once the claim is admitted they run to the end of the term regardless of any life, so
the in-payment stream is decremented by neither mortality nor lapse. Only *new* claims
carry ``l(t)``. Omitting the ledger — paying only the instalments falling in the year
of death — understates the liability by up to ``n - 1`` years of income, and the notes
list it as a pitfall.

:func:`fib_cum` is that ledger: the expected number of streams already in payment at
the start of year ``t``, ``sum of D(s) for s < t``. With deaths at mid-year on the
annual grid **[std]**, a death in year ``t`` produces six instalments in year ``t`` and
twelve in each later year, so

    claims(t, "FIB") = I x [6 D(t) + 12 FIBcum(t)]

and the whole stream for a death in year ``s`` totals ``6 + 12(n - s)`` instalments,
which is exactly ``N - k`` at ``k = 12(s-1) + 6``. :func:`check_fib_ledger` rebuilds
the year's instalment count from the death vector, with no reference to the recursion,
and asserts the two agree in every projected year.

The optional commutation module replaces a proportion :func:`fib_commute_rate` of the
streams with a lump sum, the present value of the remaining instalments at the
**[std]** snapshot rate ``r_c = 3%``. Contractually the insurer reduces the sum of the
remaining instalments "fairly and reasonably" and no insurer publishes the basis, so
the rate is a standardization; base take-up is zero and model point 4 exercises the
other extreme.

.. rubric:: Two mortality bases: applied and select

UK assured-lives tables are **select** tables — TMNL16/TFNL16 have a 5-year select
period, AM92 a 2-year one — so the mortality interface has to accept a rate that
depends on duration since entry as well as attained age. But the notes' worked example
is quoted as three applied rates, ``q(1) = 0.00055, q(2) = 0.00060, q(3) = 0.00065``,
described as illustrative values in the shape of a non-smoker temporary assurance table
and explicitly *not* taken from any CMI table. Three numbers rising at 9% a year are
not consistent with a graduated select structure, where the wearing-off of selection
alone moves the rate faster than that. Forcing them onto one would mean either a
back-solved ultimate curve that is nearly flat at ages 35-37 or shipped cells that
deviate from the notes. Both are shipped instead, and which applies is a model point
column:

``mort_basis = "applied"`` **[std]**
    ``mort_table.csv`` is read as the rate actually applied: no select factor, no
    proxy scaling. Model points 1-6 and 8; point 1 is the anchor cell and reproduces
    the worked example to the penny.

``mort_basis = "select"``
    the same table is read as an **ultimate** basis and multiplied by
    :func:`select_factor` and by ``mort_scale``, the notes' **[std]** 75% proxy
    for improvement from the public "00" Series era to the 16-Series era. Model point
    7. This is the shape a production run takes once licensed tables are dropped in —
    replacing the two CSVs changes the basis with no formula change.

Both are standardizations. The shipped table is a **[std]** construction throughout:
the M/N cells at ages 35-37 are the notes' illustrative vector, and every other cell is
a 9% p.a. geometric extension in age with a 2.2 smoker and a 0.70 female factor, each
row tagged in the file's ``provenance`` column. It is not a published table and no
conclusion about UK mortality should be drawn from it.

.. rubric:: Modules that are off in the base run

Four of the notes' optional constructions are implemented and switched off, so that the
base run reproduces the worked example while the machinery stays visible and testable:

- **Selective lapsation**, ``q_eff = q (1 + lambda max(0, w_cum - w_ref))``, with
  ``lambda = 0``. Healthier lives lapse, so persisters are progressively impaired; the
  notes rate it the third-largest lever on a long-term block.
- **Rebroking**, ``M_reb = min(2, max(1, P_inforce / P_market))`` on the lapse rate,
  with ``premium_market_ratio`` at 1. Guaranteed premiums rule out premium-shock
  lapse, so falling market rates for the attained age are the economic driver instead.
  The Reference is a flat scalar, so the multiplier is level in ``t``; a market premium
  path would be another input table.
- **Commission clawback** on lapse inside the clawback window, linear in months in
  force, with ``clawback_mths`` at 0. Set it to 48 for the notes' four-year rule.
- **Waiver of premium**, a two-state incidence/recovery chain on the premium-paying
  population, with ``wop`` false on every model point but 7. Both its incidence basis
  and its extra premium are **[std]** placeholders: no public UK incidence basis for
  the work-tasks definitions exists in the sources. The 26-week deferred period is
  read on the annual grid as incidence in year ``t`` producing waiver from year
  ``t + 1`` **[std]**, and mortality and lapse are assumed independent of the waiver
  state **[std]**, which is what lets the waived population be carried as a fraction
  rather than as a separate decrement.

.. rubric:: Sign convention and the annual-grid bias

The notes' ``CF(t)`` is already **income positive** — "+ = inflow" — which is the
library-wide sign of :func:`net_cf`, so unlike the whole life and payout annuity models
there is no ``liability_cf`` companion to publish: one stream, one sign, one name.

Two annual-grid approximations are wired in and are, per the notes, offsetting: the
decreasing shape's death benefit is the **mid-year** balance ``B(12(t-1) + 6)``, and
premiums are annual in advance with no allowance for premiums ceasing at a mid-year
death or lapse, which slightly overstates premium income. The notes are explicit that
these are a matched pair and that applying a further half-year premium adjustment on
top of the mid-year claim timing would double-count the correction. The monthly grid is
the arbiter of both and is not implemented; ``premium_mode`` is inert.

.. rubric:: Lapse pays nothing

There is no surrender value and no paid-up value at any duration, so a lapse is a pure
decrement: it moves ``pols_if`` and pays nothing. ``claims(t, "LAPSE")`` exists and
returns zero, and ``result_cf()`` carries the zero column, because the notes list a
non-zero lapse row as a pitfall imported from US models with cash surrender values —
a column of zeros states the product fact where a missing column would only hide it.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def shape():
    """The benefit shape: ``level``, ``decreasing`` or ``fib`` [S1][S2][S6][S8]."""
    v = model_point()["shape"]
    if v not in ("level", "decreasing", "fib"):
        raise ValueError("invalid shape")
    return v


def is_joint():
    """True when the policy covers two lives on a first-death basis.

    The policy pays once and ends; separation and replacement options create *new*
    policies and are out of scope **[std scope]**.
    """
    return bool(model_point()["joint_first_death"])


def age_at_entry(life=1):
    """x: the issue age (ANB) of the first (``life = 1``) or second life.

    Age nearest birthday at entry, plus a curtate policy year **[std]**: the fetched
    product documents state no age basis, and the UK assured lives tables are select
    tables indexed that way.
    """
    if life == 1:
        return int(model_point()["age_at_entry"])
    if life == 2 and is_joint():
        return int(model_point()["joint_age"])
    raise ValueError("invalid life")


def sex(life=1):
    """The sex (M / F) of the first or second life."""
    if life == 1:
        return model_point()["sex"]
    if life == 2 and is_joint():
        return model_point()["joint_sex"]
    raise ValueError("invalid life")


def smoker(life=1):
    """The smoker status (N / S) of the first or second life."""
    if life == 1:
        return model_point()["smoker"]
    if life == 2 and is_joint():
        return model_point()["joint_smoker"]
    raise ValueError("invalid life")


def policy_term():
    """n: the term in years; 1-50 level, 5-50 decreasing, 5-40 FIB [S1][S6][S8]."""
    return int(model_point()["policy_term"])


def sum_assured():
    """SA0: the initial sum assured of the level and decreasing shapes [S1][S6]."""
    return float(model_point()["sum_assured"])


def fib_income():
    """I: the family income benefit, per month, on the ``fib`` shape [S2][S6][S8]."""
    return float(model_point()["fib_income"])


def sched_rate():
    """j: the decreasing shape's schedule rate p.a. **[std]**, 6% on the shipped points.

    Contractual, not experience: the client selects it at outset and the benefit
    amortizes at it whatever happens to interest rates [S1][S6][S8].  The risk it
    carries is therefore specification error - mis-implementing the amortization or the
    monthly convention - rather than assumption error.
    """
    return float(model_point()["sched_rate"])


def indexation():
    """Whether the RPI indexation option is elected [S1][S2][S6][S7].

    Restricted to the level shape **[std scope]**: no fetched insurer offers indexed
    decreasing cover, and the notes do not combine indexation with the FIB schedule
    either.
    """
    v = bool(model_point()["indexation"])
    if v and shape() != "level":
        raise ValueError("indexation is modelled on the level shape only")
    return v


def wop():
    """Whether the waiver of premium rider is in force [S1]; false in the base run."""
    return bool(model_point()["wop"])


def premium_mth_pp():
    """P_m: the guaranteed monthly premium per policy **[std]**.

    A pure modelling value.  No UK insurer publishes premium rate tables - pricing is
    quote-driven and only the £5/month minimum is public [S5] - so any reference
    premium basis is constructed rather than observed.  It is guaranteed level for the
    full term [S2][S6][S9], which is what puts every year of premium inside the
    Solvency UK contract boundary [R3].
    """
    return float(model_point()["premium_mth"])


def premium_mode():
    """Monthly or annual premium payment.

    Inert on the annual grid, which annualizes either way: ``P_a = 12 P_m``.  It is
    carried because the notes' monthly-grid variant distinguishes them, and that
    variant is not implemented.
    """
    return model_point()["premium_mode"]


def mort_basis():
    """Whether the mortality table is read as the *applied* rate or as an *ultimate* one.

    *applied* **[std]** takes ``mort_table.csv`` as the rate actually applied, which is
    how the notes quote their illustrative worked-example vector; *select* multiplies
    it by :func:`select_factor` and by ``mort_scale``, the notes' proxy for the
    unavailable subscriber tables.  See the Space docstring for why both are shipped.
    """
    v = model_point()["mort_basis"]
    if v not in ("applied", "select"):
        raise ValueError("invalid mort_basis")
    return v


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def duration_inforce():
    """Completed policy years already elapsed when the projection starts; 0 at issue."""
    return int(model_point()["duration_inforce"])


def fib_commute_rate():
    """The proportion of FIB claims commuted to a lump sum **[std]**; 0 in the base run.

    The insurer may replace the remaining instalments with a lump sum determined
    "fairly and reasonably" [S6][S8]; no insurer publishes the basis, so both the
    take-up and the discount rate ``fib_commute_disc_rate`` are standardizations.
    """
    return float(model_point()["fib_commute_rate"])


def proj_start():
    """The first projected policy year: ``duration_inforce() + 1``.

    1 at issue, so the acquisition expense and the initial commission fall inside the
    projection; an in-force model point starts later and never sees either.
    """
    return duration_inforce() + 1


def proj_len():
    """Projection length in policy years: the term, exactly.

    Cover ceases at the end of the term with no maturity value, no renewal and no
    conversion [S1][S2][S6][S8][R8], so the horizon is ``n`` and there is nothing after
    it - the structural contrast with ``Term_US_A``, which runs on to attained age 95.
    """
    return policy_term()


def term_mths():
    """N = 12n: the term in months, the horizon of the benefit schedules."""
    return 12 * policy_term()


def duration(t):
    """Completed years since entry at the start of policy year t: ``t - 1``.

    The select duration, which is what the UK assured lives tables are indexed by
    alongside attained age.
    """
    return t - 1


def age(t, life=1):
    """The attained age (ANB) of ``life`` at the start of policy year t."""
    return age_at_entry(life) + t - 1


def select_factor(t):
    """The select-duration factor applying in policy year t **[std]**.

    A 5-year select period, the structure of TMNL16/TFNL16 [R12], with the factor
    grading from 0.55 at duration 0 to 1.00 at and beyond ``select_period``.  Read
    only on the *select* mortality basis; the *applied* basis takes the table as it
    stands.  The values are a standardization - the real tables are subscriber-only
    [R11] - and a licensed basis drops in by replacing the CSV.
    """
    d = min(duration(t), select_period)                              # noqa: F821
    return float(data.select_factor_table().loc[d, "factor"])        # noqa: F821


def mort_rate_base(t, life=1):
    """The mortality table rate for ``life`` at its attained age in policy year t.

    Includes terminal illness, which is an acceleration of the death benefit rather
    than a separate cover [S1][S6][S8]; the 16-Series tables the shipped table proxies
    are graduated on that basis [R10].
    """
    return float(data.mort_table().loc[                              # noqa: F821
        (sex(life), smoker(life), age(t, life)), "mort_rate"])


def mort_rate_life(t, life=1):
    """The mortality (incl. TI) rate applied to ``life`` in policy year t.

    The table rate, then on the *select* basis the select factor and the **[std]** 75%
    proxy scaling, then the selective-lapsation loading.  Capped at 1.
    """
    q = mort_rate_base(t, life)
    if mort_basis() == "select":
        q = q * select_factor(t) * mort_scale                        # noqa: F821
    return min(1.0, q * sel_lapse_factor(t))


def mort_rate(t):
    """q(t): the mortality (incl. TI) decrement applied to the *policy* in year t.

    The single life's rate on a single-life policy.  On a joint first-death policy it
    is the joint decrement ``1 - (1 - q_1)(1 - q_2)`` **[std]** on one policy, which
    pays once and ends [S1][S6]; modelling the two lives as separate policies would pay
    twice.
    """
    q1 = mort_rate_life(t, 1)
    if not is_joint():
        return q1
    q2 = mort_rate_life(t, 2)
    return 1.0 - (1.0 - q1) * (1.0 - q2)


def lapse_cum(t):
    """w_cum(t): the cumulative lapse proportion of the original cohort before year t.

    A proportion of ``pols_if_init()``, not a running total of :func:`lapse_rate`, and
    it drives a loading on **mortality** rather than on lapse.  Zero in the first
    projected year.
    """
    if t <= proj_start():
        return 0.0
    return lapse_cum(t - 1) + pols_lapse(t - 1) / pols_if_init()


def sel_lapse_factor(t):
    """The selective-lapsation loading on mortality in policy year t **[std]**.

    ``1 + lambda max(0, w_cum(t) - w_ref)``.  Lapsers are healthier than persisters, so
    a block that has already shed a large proportion of its lives carries impaired
    mortality on the remainder - guaranteed premiums plus healthy-life rebroking make
    this a structural feature of UK term rather than an incidental one.  Off in the base
    run (``sel_lapse_lambda = 0``), where it returns 1 in every year.
    """
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, lapse_cum(t) - sel_lapse_ref)                           # noqa: F821


def lapse_rate_base(t):
    """The table lapse rate in policy year t **[std]**, before any rebroking multiplier.

    10 / 8 / 7 / 5 / 6 / 4 percent, anchored to the FCA's 5% average in-force lapse
    rate for pure protection and to the spike pattern just after the two- and four-year
    commission clawback periods end [R9].  A full duration curve is not public and the
    levels are standardized calibrations.  Policy years beyond the table take its last
    row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "lapse_rate"])


def rebroke_factor(t):
    """M_reb(t): the rebroking multiplier on the lapse rate **[std]**; 1 in the base run.

    ``min(rebroke_cap, max(1, P_inforce / P_market))``.  Premiums are guaranteed, so
    there is no premium-shock lapse to model; the economic driver is rebroking when
    market premiums for the attained age fall below the in-force premium.
    ``premium_market_ratio`` is a flat scalar, so the multiplier is level in ``t`` -
    a market premium path would be another input table.
    """
    return min(rebroke_cap, max(1.0, premium_market_ratio))          # noqa: F821


def lapse_rate(t):
    """w(t): the annual lapse rate applied at the end of policy year t.

    The table rate times the rebroking multiplier, capped at 1.  A lapse pays nothing:
    there is no surrender or paid-up value at any duration [S1][S6][S8][R8].
    """
    return min(1.0, lapse_rate_base(t) * rebroke_factor(t))


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy year t.

    ``pols_if_init()`` in the first projected year, then the notes' recursion
    ``l(t+1) = l(t)(1 - q(t))(1 - w(t))``.  This is the weight on every cash flow of
    the same ``result_cf()`` row.  Zero outside ``proj_start() .. proj_len()``: the
    cover has not started or has expired.
    """
    if t < proj_start() or t > proj_len():
        return 0.0
    if t == proj_start():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year, before any decrement; the same number
        as :func:`pols_if` and the weight on that year's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before lapses - the notes' processing order is
        **death before lapse** **[std order]**, so this is the population
        lapses are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-year state: what is left once the year's deaths
        and lapses are taken, and zero from ``proj_len()`` on because the
        cover expires there.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "AFT_DECR":
        if t < proj_start() or t >= proj_len():
            return 0.0
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t) = l(t) q(t): expected death and terminal illness claims in policy year t.

    One decrement covering both: terminal illness accelerates the death benefit rather
    than adding to it [S1][S6][S8].
    """
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """Lapses at the end of policy year t, taken from the survivors of mortality.

    Pays nothing - there is no surrender value [S6][R8] - so this moves
    :func:`pols_if` and nothing else.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def pols_maturity(t):
    """Policies whose cover expires at the end of the term; zero in every other year.

    Not a decrement and not a benefit - the contract simply runs out, with no maturity
    value [S1][S2][S6][S8][R8] - but needed for the in-force roll-forward to close; see
    the Space docstring and :func:`check_pols_roll_fwd`.
    """
    if t != proj_len():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))


def wop_waived_frac(t):
    """The fraction of in-force policies with premiums waived at the start of year t.

    A two-state incidence/recovery chain **[std]**,
    ``u(t+1) = u(t)(1 - rec) + (1 - u(t)) inc``, starting from ``u = 0``.  Both rates
    are placeholders: no public UK incidence basis for the waiver work-tasks
    definitions appears in the fetched sources.  Incidence in year ``t`` produces
    waiver from year ``t + 1``, which is the annual grid's reading of the 26-week
    deferred period [S1] **[std]**, and mortality and lapse are assumed independent of
    the waiver state **[std]** - which is what lets the waived population be carried as
    a fraction of the in-force rather than as its own decrement.  Zero unless the rider
    is in force.
    """
    if not wop() or t <= proj_start():
        return 0.0
    u = wop_waived_frac(t - 1)
    return u * (1.0 - wop_rec_rate) + (1.0 - u) * wop_inc_rate       # noqa: F821


def pols_payer(t):
    """The number of in-force policies actually paying premium in policy year t.

    ``l(t)`` less the waived fraction.  Equal to :func:`pols_if` unless the waiver of
    premium rider is in force.
    """
    return pols_if(t) * (1.0 - wop_waived_frac(t))


def idx_increase():
    """The cover increase offered at each anniversary under the indexation option.

    ``min(max(RPI, 0), 10%)`` [S1][S2][S6][S7], times ``idx_accept_rate``.  The
    notes' base run is deterministic and always accepts, which is what the shipped
    ``idx_accept_rate = 1`` means; their 80% take-up **[std]** would be a mixture of
    paths, and scaling the increase instead is a deterministic approximation to it.

    One consequence worth stating: with acceptance certain, the rule removing the option
    after three consecutive declines [S1][S6] (two at one insurer [S8]) is never
    reached, so it is not implemented.
    """
    return min(max(rpi_rate, 0.0), idx_cover_cap) * idx_accept_rate  # noqa: F821


def idx_factor(t):
    """idx(t): the cumulative **cover** indexation factor at the start of policy year t.

    1 in the first projected year and whenever the option is not elected.
    """
    if not indexation() or t <= proj_start():
        return 1.0
    return idx_factor(t - 1) * (1.0 + idx_increase())


def idx_prem_factor(t):
    """idx_p(t): the cumulative **premium** indexation factor at the start of year t.

    The premium rises by ``min(1.5 x increase, 15%)`` for a cover increase of
    ``increase`` [S1][S2][S6].  The 1.5 multiplier is what makes an accepted increase
    premium-margin-accretive if mortality is proportional to cover - and what reverses
    the sign of that conclusion if acceptance is selective, impaired lives accepting
    while healthy ones decline **[std]** concern.  No public take-up data exists.
    """
    if not indexation() or t <= proj_start():
        return 1.0
    return idx_prem_factor(t - 1) * (
        1.0 + min(idx_prem_mult * idx_increase(), idx_prem_cap))     # noqa: F821


def premium_pp(t):
    """P_a idx_p(t): the annualized gross premium per policy in policy year t.

    ``12 P_m``, indexed if the option is elected, and loaded by
    ``wop_prem_loading`` where the waiver rider is in force - a **[std]**
    placeholder, since the rider's extra premium is not published either.
    """
    p = 12.0 * premium_mth_pp() * idx_prem_factor(t)
    return p * (1.0 + wop_prem_loading) if wop() else p              # noqa: F821


def premiums(t):
    """Premium income at the start of policy year t, an inflow.

    Carried on :func:`pols_payer`, never on the FIB ledger: premiums stop at death
    while family income benefit instalments continue.  Annual in advance with no
    allowance for premiums ceasing at a mid-year death or lapse, which slightly
    overstates income - the known bias of this convention **[std]**, offset by the
    mid-year benefit timing of the decreasing shape.
    """
    return premium_pp(t) * pols_payer(t)


def sched_rate_mth():
    """j_m = (1+j)^(1/12) - 1: the decreasing schedule's monthly rate **[std]**.

    The effective convention, not a nominal ``j/12``.  The two give slightly different
    schedules, so the convention has to be stated; ``benefit_sched(60) = £134,588`` on
    the anchor cell is the notes' validation anchor for an implementation.
    """
    return (1.0 + sched_rate()) ** (1.0 / 12.0) - 1.0


def benefit_sched(k):
    """B(k): the decreasing shape's benefit after k months [S1][S6][S8].

    ``SA0 [(1+j_m)^N - (1+j_m)^k] / [(1+j_m)^N - 1]``, a mortgage-style amortization
    from ``B(0) = SA0`` to ``B(N) = 0``.  A zero schedule rate degenerates to straight
    line, which the closed form cannot express.
    """
    n_m = term_mths()
    jm = sched_rate_mth()
    if jm == 0.0:
        return sum_assured() * (n_m - k) / n_m
    return sum_assured() * (
        (1.0 + jm) ** n_m - (1.0 + jm) ** k) / ((1.0 + jm) ** n_m - 1.0)


def annuity_certain_factor(m):
    """a(m): the m-month annuity-certain factor at the FIB commutation rate **[std]**.

    ``[1 - (1+r_c)^(-m/12)] / [(1+r_c)^(1/12) - 1]``, instalments in arrears.  Used
    only by the commutation module.
    """
    if m <= 0:
        return 0.0
    j = fib_commute_disc_rate                                        # noqa: F821
    if j == 0.0:
        return float(m)
    return (1.0 - (1.0 + j) ** (-m / 12.0)) / ((1.0 + j) ** (1.0 / 12.0) - 1.0)


def fib_commute_pp(t):
    """CV: the commuted value of one FIB stream arising from a death in year t **[std]**.

    ``I a(N - k)`` at the mid-year death month ``k = 12(t-1) + 6``, so it falls to zero
    as the term runs out.  Zero on the level and decreasing shapes.
    """
    if shape() != "fib":
        return 0.0
    return fib_income() * annuity_certain_factor(term_mths() - (12 * (t - 1) + 6))


def benefit_pp(t):
    """DB(t): the death and terminal illness benefit per policy in policy year t.

    Level: ``SA0 idx(t)``.  Decreasing: the **mid-year** balance ``B(12(t-1) + 6)``
    **[std]**, the annual grid's reading of a schedule that steps down monthly.  FIB:
    the commuted value of the instalment stream, which is what a commuted claim pays;
    an uncommuted FIB claim has no lump sum at all and goes through
    ``claims(t, "FIB")`` instead.
    """
    s = shape()
    if s == "level":
        return sum_assured() * idx_factor(t)
    if s == "decreasing":
        return benefit_sched(12 * (t - 1) + 6)
    return fib_commute_pp(t)


def fib_cum(t):
    """FIBcum(t): the expected FIB streams already in payment at the start of year t.

    ``sum of D(s) for s < t``.  **Not decremented** by mortality or lapse: once a claim
    is admitted the instalments are an annuity-certain to the end of the term whatever
    happens to any life [S6][S8].  Only *new* claims carry ``l(t)``.
    """
    if t <= proj_start():
        return 0.0
    return fib_cum(t - 1) + pols_death(t - 1)


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the lump sum paid at the end of the year of death: ``DB(t) D(t)`` on
        the level and decreasing shapes, and on the ``fib`` shape only the
        commuted proportion of the streams.

    ``"FIB"``
        the family income benefit instalments falling in year t,
        ``I [6 D(t) + 12 FIBcum(t)]`` net of the commuted proportion - six
        instalments in the year of a mid-year death, twelve in each later
        year.  Zero on the other two shapes.

    ``"LAPSE"``
        zero, always.  There is no surrender or paid-up value at any duration
        [S1][S6][S8][R8]; the kind exists so that the zero is stated rather
        than left to inference.  See the Space docstring.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "FIB", "LAPSE"))
    if kind == "DEATH":
        if shape() == "fib":
            return fib_commute_rate() * benefit_pp(t) * pols_death(t)
        return benefit_pp(t) * pols_death(t)
    if kind == "FIB":
        if shape() != "fib":
            return 0.0
        return ((1.0 - fib_commute_rate()) * fib_income()
                * (6.0 * pols_death(t) + 12.0 * fib_cum(t)))
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec D(t): the claim handling expense on the year's death and TI claims **[std]**.

    £250 per claim, uninflated.  Kept out of :func:`expenses` because the notes' worked
    example prints the two as separate columns.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^(t-1)`` **[std]**."""
    return (1.0 + inflation_rate) ** (t - 1)                         # noqa: F821


def expenses(t):
    """E0 and e(t): acquisition and inflating maintenance expense in year t **[std]**.

    £150 per policy at issue, then £30 per policy per year inflating at 3%, both at the
    start of the year.  An in-force model point starts after policy year 1 and never
    sees the acquisition charge.  Premiums as low as £5/month against a £30 maintenance
    expense make this assumption solvency-relevant on small-sum-assured blocks, which is
    why the notes rate expense inflation a first-order lever despite its size.
    """
    acq = expense_acq * pols_if(t) if t == 1 else 0.0                # noqa: F821
    return acq + expense_maint * inflation_factor(t) * pols_if(t)    # noqa: F821


def comm_init_pp():
    """c0: initial commission per policy issued **[std]**.

    150% of the annualized premium, paid upfront at issue.  Roughly 96% of protection
    commission is paid upfront [R9], which with the acquisition expense is what
    produces the deep year-one new business strain in the worked example.
    """
    return comm_init_rate * premium_pp(1)                            # noqa: F821


def comm_clawback(t):
    """Initial commission recovered on lapses inside the clawback window **[std]**.

    ``c0 (clawback_mths - 12t)/clawback_mths`` per lapsed policy, linear in months in
    force.  Off in the base run (``clawback_mths`` is 0); set it to 48 for the
    notes' four-year rule.  Clawback periods of two to four years are evidenced [R9];
    the linear formula is a standardization.  Inside the window it reverses the sign of
    the early-lapse sensitivity, which is the point of carrying it.
    """
    if clawback_mths <= 0:                                           # noqa: F821
        return 0.0
    mths = 12 * t
    if mths >= clawback_mths:                                        # noqa: F821
        return 0.0
    return (comm_init_pp() * (clawback_mths - mths)                  # noqa: F821
            / clawback_mths * pols_lapse(t))                         # noqa: F821


def commissions(t):
    """Commission outgo in policy year t **[std]**, net of any clawback recovered.

    The initial commission in policy year 1, then 2.5% of premium income from policy
    year 2.  Both are levels chosen for the reference implementation; only the upfront
    *pattern* is evidenced [R9].
    """
    init = comm_init_pp() * pols_if(t) if t == 1 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 2 else 0.0       # noqa: F821
    return init + renew - comm_clawback(t)


def net_cf(t):
    """CF(t): the net cash flow of policy year t, **income positive**.

    Premiums less death and terminal illness claims, claim expense, maintenance and
    acquisition expense and commission.  The notes' own sign - they write ``+ = inflow``
    - which is also the library-wide convention, so unlike the whole life and payout
    annuity models there is no outgo-positive ``liability_cf`` companion to publish.

    The shape to expect on guaranteed term is a deep new business strain in year 1,
    upfront commission and acquisition expense against a single year's premium, then
    thin positive margins: the level premium prefunds rising mortality cost, so early
    lapses forfeit margin to the insurer and late ones relieve it.
    """
    return (premiums(t) - claims(t) - claim_expenses(t)
            - expenses(t) - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - deaths - lapses - expiries``.  Expiries are non-zero
    only in the final policy year, where the survivors neither die nor lapse: their
    cover runs out.  Without that term the last year appears to lose lives with no
    cause.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives
    the signed residual of the year that failed.  The tolerance scales with
    ``pols_if_init()``, since the residual accumulates rounding on that many policies.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_start(), proj_len() + 1))


def check_fib_ledger_resid(t):
    """The family income benefit ledger residual in policy year t; zero everywhere.

    :func:`claims` ``(t, "FIB")`` less an independent rebuild of the same figure: six
    instalments for a death in year t and twelve for every death in an earlier year,
    summed straight off the death vector with no reference to the :func:`fib_cum`
    recursion.  A ledger that was decremented by mortality or lapse - the notes'
    pitfall - or one that paid only the year-of-death instalments would show up here.
    Zero by definition on the level and decreasing shapes, which have no ledger.
    """
    if shape() != "fib":
        return 0.0
    built = 6.0 * pols_death(t) + 12.0 * sum(
        pols_death(s) for s in range(proj_start(), t))
    return claims(t, "FIB") - (1.0 - fib_commute_rate()) * fib_income() * built


def check_fib_ledger():
    """True when the family income benefit ledger closes in every projected year.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells;
    :func:`check_fib_ledger_resid` gives the signed residual of the year that failed.
    """
    return all(abs(check_fib_ledger_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(proj_start(), proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by policy year t.

    ``pols_if`` is the start-of-year count, which is the weight applied to every cash
    flow on the same row.  ``net_cf`` carries the notes' own income-positive sign.
    ``claims_lapse`` is a column of zeros by product design - there is no surrender
    value - and is published rather than dropped; see the Space docstring.
    """
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_fib": [claims(t, "FIB") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy year t."""
    ts = list(range(proj_start(), proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_payer": [pols_payer(t) for t in ts],
            "fib_cum": [fib_cum(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

select_period = 5

mort_scale = 0.75

sel_lapse_lambda = 0.0

sel_lapse_ref = 0.2

premium_market_ratio = 1.0

rebroke_cap = 2.0

rpi_rate = 0.03

idx_cover_cap = 0.1

idx_prem_mult = 1.5

idx_prem_cap = 0.15

idx_accept_rate = 1.0

expense_acq = 150.0

expense_maint = 30.0

expense_claim = 250.0

inflation_rate = 0.03

comm_init_rate = 1.5

comm_renewal_rate = 0.025

clawback_mths = 0

fib_commute_disc_rate = 0.03

wop_inc_rate = 0.004

wop_rec_rate = 0.35

wop_prem_loading = 0.05

pd = ("Module", "pandas")