# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.DIA_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.DIA_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is: ``Projection[18]``
is an ItemSpace projecting the table's nineteenth row, model point 19, the worked-example
anchor cell in force 241 months at the valuation date, one month into its income phase,
and :func:`point_id` is its label::

    >>> Projection[18].result_cf()         # one row per month from the valuation date
    >>> Projection[18].result_pols()       # the counts and survival behind it
    >>> Projection[18].point_id()          # 19, the row's point_id
    >>> Projection[0].result_annual()      # the worked example, issued at t = 0
    >>> Projection.idx = 7                 # or switch the default, before it computes

Switch the default, or set any Reference, before the model computes anything. Compiled, no
cache is ever cleared: set ``idx``, like every Reference, on a model just imported, before
anything is computed, or project through ``Projection[i]``. modelx recomputes what a
Reference reaches when it is set; a compiled ItemSpace takes the References when it is
made and keeps every value it has computed until it is deleted, and the base
``Projection`` and ``Data`` keep theirs for good. And it holds each Reference as a C
variable of its shipped value's type: a float set on an int Reference, ``pricing_iters``
or a code, truncates toward zero, and an int set on a float Reference reads as a float
(``products/deferred_income_annuity/model-sec.md``).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.DIA_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.DIA_US_S` is rewritten where it depends on where the projection starts, where it
must answer for a month outside the frame, where it passed a policy month as ``t``, where
it priced a premium off the projection's survival, or where it branched on text; every
other is :mod:`~.DIA_US_S`'s own. ``products/deferred_income_annuity/model-sec.md`` lists
the rewritten cells with the reason for each. Making it compile changed how each cell
reads its inputs and spells its codes, and no number: every model point attribute a
projection cell uses is read as a number from a ``Data`` vector, each text column it
branches on as ``Data``'s decoded flags, the two age tables as arrays by sex and age, the
two factor tables as row vectors and the premium schedule as a table by policy month,
every timing, kind, phase and pricing basis as an int code (*Codes*, below), and
:mod:`~.DIA_US_S`'s ``claims(t, kind=None)`` and ``claims_ann(y, kind=None)``, whose
``None`` is the total of the two kinds, take the code ``ALL`` for it.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/deferred_income_annuity/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can
be edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``DIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.DIA_US_SEC.Data`. The four assumption tables are the files :mod:`~.DIA_US_S`
reads, read in place; the model point table and the premium schedule are this model's
own:

========================  ==================================  =========================
Reference                 Cells                               File
========================  ==================================  =========================
model_point_file          data.model_point_table()            model_point_table_sec.csv
premium_schedule_file     data.premium_schedule_table()       premium_schedule_sec.csv
mort_table_file           data.mort_table()                   mort_table.csv
improvement_scale_file    data.improvement_scale()            improvement_scale.csv
payout_factor_file        data.payout_factor_table()          payout_factor_table.csv
rop_factor_file           data.rop_factor_table()             rop_factor_table.csv
========================  ==================================  =========================

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however long the contract has been in force, month ``t`` runs from time ``t`` to
time ``t + 1``, and the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len`
counts the months from the valuation date to the stop rule. Row ``t`` is the same month
for every point, so the frames of a block line up and sum row by row. Survival is indexed
by a **time point** on this clock rather than by a month: ``lives_if(t, life)`` and
``lives_if_last(t)`` are survival *at* time ``t``, the start of month ``t``, so month
``t`` opens at time ``t`` and closes at time ``t + 1``, the deaths of month ``t`` are
``l(t) - l(t + 1)``, and the arrears survival point is ``t + 1``, as in
:mod:`~.DIA_US_S`.

``duration_mth(t)`` counts **policy months**, the months elapsed from issue at the start
of month ``t``: ``duration_mth(t) = duration_mth_init() + t``, where
:func:`duration_mth_init` is read from the model point — positive for a contract already
in force at the valuation date, 0 for one issued at it, ``-k`` for one to be issued ``k``
months later, at most ten years later. It is the technical notes' month index, and
everything contractual reads it: the completed policy years
``duration(t) = duration_mth(t) // 12``, the contractual 1-based label
``policy_year(t) = duration(t) + 1``, the attained ages ``age(t, life)``, the premium
months, the income start month ``T``, the three option months, the payment months, the
COLA anniversaries and the certain period. ``T``, the premium months and the option months
stay policy months and are compared with ``duration_mth(t)``: converted to ``t`` they
would collide with the ``-1`` that the option accessors return for "never", and turn
negative on a contract past them. A cell keyed directly by this clock takes ``k``, a
policy month or the time point that opens it, or ``y``, a policy year, never ``t``: the
pricing cells and the payout schedule are keyed by ``k``, and the annual mortality rate by
``y``. The months from the income start month, the payout phase's own count, are this
clock less ``T``. No cell is keyed by them: :func:`is_payment_pm`, :func:`cola_factor_pm`,
:func:`certain_floor_pm` and :func:`annuity_pp_sched_pm` take a policy month ``k`` and
form ``k - T`` inside, so that the contract's schedules, its premiums and its options share
one key. The anchor cell in force 241 months, point 19, is in policy year 21 at ``t = 0``,
a month after its income start month ``T = 240``, and point 18, the payment-acceleration
contract in force 59 months, pays its second premium at policy month 60, ``t = 1``.

The **stop rule** ends every frame where it ends :mod:`~.DIA_US_S`'s: :func:`stop_mth` is
:mod:`~.DIA_US_S`'s frame length from issue, the month the youngest covered life attains
the limiting age or the end of the guarantee period if that is later, and :func:`is_active`
is ``0 <= duration_mth(t) < stop_mth()``. A contract's own end inside the frame, its last
death or the end of its guarantee, is a probability or a floor reaching zero, and the
frame runs on with zeros, as :mod:`~.DIA_US_S`'s does.

Three inputs, and their clocks. Expense inflation reads the **valuation** clock,
``inflation_factor(t) = (1 + inflation_rate) ** (t // 12)``, :mod:`~.DIA_US_S`'s annual
steps moved onto ``t``, so that the maintenance charge is in valuation-date dollars for
every point alike. Mortality improvement stays on the **policy** clock, because it is
already calendar-dated: its exponent is the calendar year less ``mort_table_year``, and the
calendar year ``issue_year() + duration(t)`` is the one the contract reaches whatever the
valuation date, so a contract in force reads the improvement of its own calendar years and
nothing is re-based. The commutation discount rate moves with the reference rate's change
since issue, on one path every point shares: for a contract on the books at the valuation
date, the change to that date, which a contract in force carries in its opening state,
plus ``ref_rate_shift``, a change made at the valuation date; for a contract issued later,
after that change, none.

On a point issued at the valuation date the two clocks coincide and this model computes
what :mod:`~.DIA_US_S` computes: every cell the two share agrees at every argument
:mod:`~.DIA_US_S` evaluates in its sweep, but for three whose meaning changed,
``pols_if_init``, now the count already in force at the valuation date, ``model_point``, a
row of another table, and ``result_pols``, which gains the month's new business. That is
how the worked example carries over, and ``tests/test_model_conventions.py`` asserts it
cell by cell.

.. rubric:: Counts

The count on the books is the number of contracts the point stands for,
:func:`policy_count`, from issue to the stop rule. Mortality decrements each life's
survival, :func:`lives_if`, never the count: the two lives are independent, so their two
probabilities are the whole survival state, and every cash flow is the count times a
per-contract amount weighted by survival, as :mod:`~.DIA_US_S` weights every flow by its
constant ``pols_if_init``. So ``pols_if_at(t, BEF_NB)`` is :func:`pols_if_init`, the
count already in force, at :func:`t_entry`, the first month on the books, the whole count
after it, and 0 outside the frame; and ``pols_if_at(t, BEF_DECR)`` adds
:func:`pols_new_biz`, the contracts issued in month ``t``. The ``BEF_DECR`` count weights
every cash flow of row ``t``. A contract in force at the valuation date opens with its
``policy_count``; one issued at or after it opens with none, and takes its
``policy_count`` as new business in its issue month, ``duration_mth(t) = 0``. New business
brings its premium schedule and no acquisition cost, as in :mod:`~.DIA_US_S`, which has
none.

:func:`pols_if` keeps :mod:`~.DIA_US_S`'s definition on that count: the contracts on the
books weighted by the probability that a covered life is alive at the start of month
``t``, ``pols_if_at(t, BEF_DECR) * lives_if_last(t)``, which carries the maintenance
expense. It is not the count before decrements, which mortality never moves: on point 20,
the period-certain point in force 300 months, ``pols_if(0)`` is 0.5577 against a count of
1.0, as ``DIA_US_S``'s ``pols_if(300)`` is, and the registry marks the model
``survival_pols_if`` for that reason. There is no lapse decrement, and no ``pols_lapse``.

.. rubric:: The opening state

A contract in force at the valuation date carries eight things its count and its policy
clock do not say. Each is read from its model point as it stands at the start of month
0, before any month-0 event:

``lives_if_init_1``, ``lives_if_init_2``
    each covered life's probability of being alive at the valuation date,
    :func:`lives_if_init`. On a real record it is 1 or 0, and a joint contract may carry
    one life already dead; on a point restated from :mod:`~.DIA_US_S` at its month ``d``
    it is :mod:`~.DIA_US_S`'s ``lives_if(d, life)``, a probability. The lives are
    independent, as in :mod:`~.DIA_US_S`, so the two per-life probabilities are the whole
    survival state. Life 2 is 0 on a single-life contract.
``cum_premium_pp_init``, ``annual_income_init``
    ``CP`` and ``B`` entering month 0: the premiums paid before the valuation date and the
    guaranteed annual income their slices bought, a start-date adjustment already
    exercised included, :func:`cum_premium_pp_init` and :func:`annual_income_init`.
    ``CP`` is the base of the death benefit and of the refund, and ``B`` of the income;
    the premiums still due are in the premium schedule, so the two columns and the
    schedule hold all of the premium history the projection reads.
``guarantee_mths_pricing_init``
    on a cash or installment refund in force, ``n_g`` as the pricing kernel takes it,
    :func:`guarantee_mths_pricing_init`: a fixed point over the **whole** premium schedule,
    the slices bought included, which prices every slice still to be bought and a
    start-date adjustment still to come. The schedule holds only the premiums still due,
    and the iteration depends on the path, so neither the schedule nor ``CP`` and ``B``
    can recover it.
``surv_to_payout_init``
    on a contract past its income start month, the cohort that reached the income phase,
    ``l_last(T)``, :func:`surv_to_payout_init`, which weights every guaranteed
    instalment. It is **not** the probability that a life is alive: in a certain period
    the contract stays open after the last death, its guarantee running on to a
    beneficiary, so on point 20, in force 300 months, it is 0.715 while
    ``lives_if_last(0)`` is 0.5577. On a real record in payout it is 1.
``commute_weight_init``
    on a contract that commuted before the valuation month, the cohort that commuted,
    ``l_last(t_c)``, :func:`commute_weight_init`, whose guaranteed instalments the
    commutation extinguished; the rest of the cohort that reached the income phase keeps
    its guarantee. On a real record of a commuted contract it is 1.
``ref_rate_shift_init``
    the reference rate at the valuation date less the reference rate at issue,
    :func:`ref_rate_shift_init`: the part of the change since issue, which moves the
    commutation discount rate, that the contract has already seen. A fact of the market,
    the same for two contracts issued together.

At issue each covered life is 1, the premiums paid, the income bought and the change 0,
and the three other columns blank, so a point issued at or after the valuation date
carries those values. Each of the two frozen weights is blank where its instant, the income
start month or the commutation month, is at or after the valuation month: the projection
derives it there from the lives, :mod:`~.DIA_US_S`'s own ``l_last`` at that month.
Nothing else carries a path. The acceleration factor is read only in the exercise month,
and a contract valued after its exercise paid the lump sum before the valuation date,
its blackout months paying nothing. The commuted fraction follows from the policy clock:
the commutation is one exercise named on the model point, and there is no withdrawal. The
certain months left follow from ``duration_mth``. And the instalments scheduled to date,
``G``, are a deterministic schedule fixed by the income at the income start month
(below).

.. rubric:: Pricing on the policy clock

:mod:`~.DIA_US_S` uses one survival curve for two jobs: **pricing** each premium's paid-up
slice at its own date, and **projecting**. On the valuation clock they part. The
projection's survival, :func:`lives_if`, opens at the valuation date from the opening
state. Pricing stays anchored at issue and at the premium dates, deterministic from the
contract's terms: :func:`lives_if_pm`, survival from issue to a policy time point ``k``,
is one explicit loop from issue over the monthly rates, :mod:`~.DIA_US_S`'s recursion
unrolled, the same products in the same order, so every purchase rate, every pricing
factor and every guarantee period is :mod:`~.DIA_US_S`'s to the last bit. The monthly rate
comes from one place, :func:`mort_rate_py`, the annual rate of a policy year, which the
projection's :func:`mort_rate` reads at the policy year of month ``t``, so the two curves
use one rate, as :mod:`~.DIA_US_S`'s one curve did. So pricing shares the valuation's
mortality basis, its A/E and its improvement, as :mod:`~.DIA_US_S`'s does: a mortality
sensitivity moves the purchase rate of every premium still due, and every twin's and
future row's guarantee period and income, while a contract in force keeps the guarantee
period it was priced with, ``guarantee_mths_pricing_init``. Every pricing cell is keyed
by the premium's or the exercise's policy month ``k``, :mod:`~.DIA_US_S`'s ``t`` renamed:
:func:`income_start_mth_at`, :func:`deferral_yrs`, :func:`surv_to_income_start`,
:func:`rop_factor_calc`, :func:`rop_factor`, :func:`annuity_factor_def` and
:func:`purchase_rate`. Pricing never reads the projection, so a cold ``net_cf(0)`` runs a
handful of cells deep where :mod:`~.DIA_US_S`'s recurses through survival to the payout
date.

The payout phase reads the income ahead of ``t``: the installment refund's search for its
certain period, the refund balance, the commuted value and the accelerated instalments.
On the valuation clock the income ``B`` and the cumulative premium ``CP`` are recursions,
and reading them far ahead would open a chain as long as the deferral. So the payout
schedule is fixed at the income start month, from :func:`annual_income_payout`,
``B(T)``, and :func:`cum_premium_payout`, ``CP(T)``, each one loop over the policy months
from the valuation date's to ``T``, in :mod:`~.DIA_US_S`'s order. The schedule rests on
``B`` being level from ``T`` on, which the product guarantees and ``Data`` checks: no
premium falls at or after ``T``, and a start-date adjustment is exercised before its new
start month. :func:`annuity_pp_sched_pm` is the instalment of policy month ``k`` on that
schedule, and :func:`cum_annuity_pp` sums it, ``G``, keyed by policy month and based at
the valuation date's, so that the refund of a cash refund long in payout reads ``G`` from
there forward, recursing back to that key and no further.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and — for everything in the income phase — they
follow :mod:`.SPIA_US_S` **exactly**, because the payout phase of a DIA *is* a single
premium immediate annuity. What running in force adds is named as
``basiclife.BasicTerm_SE`` names it: ``duration_mth`` read from the model point,
``policy_count``, ``pols_new_biz``, ``pols_if_at`` with its ``BEF_NB`` and
``BEF_DECR`` timings, codes here, ``is_active`` and ``result_pols``.
``duration_mth_init``, the policy months completed at the valuation date, takes
``UL_US_S``'s name, and each opening-state column is ``<cell>_init``, the cell it opens
with ``_init`` added, read per life by ``lives_if_init(life)``. ``t_entry`` and
``stop_mth`` are the SEC family's own. A cell keyed by policy month carries ``_pm``, as in
``SPIA_US_SEC``, beside the ``_py`` that ``Term_US_SEC`` gives a policy-year key, a table
reader keyed by attained age carries ``_at``, and a quantity fixed at the income start
month carries ``_payout``. The ``is_*``
decodes turn the model point's text columns into the flags the projection branches on,
each reading and validating its column as :mod:`~.DIA_US_S`'s label accessor does, so that
no other projection cell compares text and none calls a label accessor (``sex``,
``income_form``, ...), which is left to reporting. The technical notes use compact
actuarial symbols instead. The mapping is:

========================  ==================================  ==============================
Notes symbol              Cells                               Meaning
========================  ==================================  ==============================
t                         (the cells argument)                Month from the valuation date,
                                                              0-based; time t opens month t
k                         (the cells argument)                Policy month, or the time
                                                              point opening it, from issue
y                         (the cells argument)                Policy year, 1-based
(month index)             duration_mth(t)                     Months from issue at the start
                                                              of month t
(none)                    duration_mth_init()                 Months in force at the
                                                              valuation date; -k if issued k
                                                              months on
y = duration + 1          policy_year(t)                      Policy year containing t
(none)                    duration(t)                         Completed policy years
(issue year)              issue_year()                        Calendar year of issue
(calendar year)           calendar_year(t)                    Calendar year of the policy
                                                              year containing t
(none)                    t_entry()                           First month on the books
(stopping rule)           stop_mth()                          Policy month the frame stops
(none)                    is_active(t)                        Whether month t is in frame
(none)                    point_id()                          The point's label, idx's row
x, x_2                    age_at_entry(life)                  Issue ages (ANB), life 1 or 2
x(t)                      age(t, life)                        Attained age (ANB)
(none)                    sex(life)                           Sex of each covered life
(none)                    is_joint()                          Two covered lives
market_type               market_type()                       NQ / TradIRA / RothIRA / QLAC
(none)                    is_qlac()                           market_type decoded: QLAC
f                         income_form()                       LO / LO_ROP / CR / IR / PC
(f, payout part)          payout_form()                       The payout stream f implies
(none)                    is_life_only()                      f decoded: LO or LO_ROP
(none)                    is_cash_refund()                    f decoded: CR
(none)                    is_installment_refund()             f decoded: IR
(none)                    is_period_certain()                 f decoded: PC
db_form                   db_form()                           ROP or NONE in deferral
(none)                    is_rop()                            db_form decoded: ROP
n                         certain_period()                    Elected certain period, years
T                         income_start_mth()                  Income start month in force
(T at issue)              income_start_mth_init()             Income start month at issue
(T for a premium at k)    income_start_mth_at(k)              Start month a premium at k is
                                                              priced to
m                         payment_freq()                      Payments per year
pay_timing                payment_timing()                    arrears / advance
(none)                    is_arrears()                        timing decoded: arrears
c                         cola_rate()                         Fixed compound COLA rate
(1+c)^floor((t-T)/12)     cola_factor(t)                      COLA escalation factor
(the same, at k)          cola_factor_pm(k)                   The same, in policy month k
delta / survivor_pct      survivor_pct()                      Survivor percentage
reduction_trigger         reduction_trigger()                 either / primary
(none)                    is_trigger_either()                 trigger decoded: either
P_k                       premium_pp(t)                       Premium paid in month t
(P_k by policy month)     premium_pm(k)                       Premium paid in policy month k
(the schedule)            premium_by_mth()                    {month: premium} still due
CP(t)                     cum_premium_pp(t)                   Cumulative premiums during t,
                                                              eq (7)
CP(t_entry)               cum_premium_pp_init()               Premiums paid before the
                                                              valuation date
CP(T)                     cum_premium_payout()                Cumulative premiums at the
                                                              income start, the refund base
B(t)                      annual_income(t)                    Guaranteed annual income
                                                              during t, eq (8)
B(t_entry)                annual_income_init()                Income bought before the
                                                              valuation date
B(T)                      annual_income_payout()              Income at the income start
l(t)                      lives_if(t, life)                   Survival to time t, projected
l(t_entry)                lives_if_init(life)                 Survival at the valuation
                                                              date, or at issue if later
l(k) (pricing)            lives_if_pm(k, life)                Survival from issue to policy
                                                              time point k
l_last(k) (pricing)       lives_if_last_pm(k)                 At least one life alive, from
                                                              issue to k
q(t)                      mort_rate_mth(t, life)              Monthly death probability
(q by policy year)        mort_rate_mth_py(y, life)           The same, in policy year y
(annual q)                mort_rate(t, life)                  Annual rate after improvement
(annual q by year)        mort_rate_py(y, life)               The same, in policy year y
q_x (table)               mort_rate_base(t, life)             Base-table annual rate
(q_x by age)              mort_rate_base_at(x, life)          The same, at attained age x
(the table's sex)         mort_schedule(life)                 The life's row of the table
2012 (in q_x^(2012+n))    mort_table_year                     Base year of the shipped table
G2_x                      improvement_rate(t, life)           Generational improvement rate
(G2_x by age)             improvement_rate_at(x, life)        The same, at attained age x
(the scale's sex)         improvement_schedule(life)          The life's row of the scale
(none)                    mort_basis()                        anchor / generational
(none)                    is_generational()                   mort_basis decoded
(A/E)                     mort_ae_factor                      A/E factor, 1.00 **[std]**
omega                     omega_age                           Limiting age, 120
(stopping rule)           horizon_mths()                      Months from issue to the age
                                                              stop rule
(none)                    proj_len()                          Months from the valuation date
                                                              to the stop rule
(d_i)                     lives_death(t, life)                Deaths during month t
l_last(t)                 lives_if_last(t)                    At least one life alive
d_last(t)                 lives_death_last(t)                 Last-death density
(none)                    policy_count()                      Contracts the point stands for
(none)                    pols_if_init()                      Contracts in force at the
                                                              valuation date
(none)                    pols_if_at(t, timing)               Contracts on the books at time
                                                              t, BEF_NB or BEF_DECR
(none)                    pols_new_biz(t)                     Contracts issued in month t
(in force)                pols_if(t)                          Contracts on the books times
                                                              l_last(t)
i_p, v                    pricing_rate                        Pricing interest rate, 4.75%
v^d                       pricing_disc_factor(yrs)            Pricing discount factor
L                         expense_load                        Expense and profit load, 6.0%
d_k = (T - t_k)/12        deferral_yrs(k)                     Deferral of a premium at k
_d p_x                    surv_to_income_start(k)             Survival over the deferral
a^(m)_y(f; i)             annuity_factor(...)                 Payout APV, eq (2) generalized
(the same, by basis)      annuity_factor_at(k, basis)         The same from policy month k,
                                                              on a basis's arguments
(same, at T)              payout_factor()                     Payout factor in force
(same, computed)          payout_factor_calc()                Payout factor by eq (2)
(none)                    factor_basis()                      table / formula
(none)                    is_formula_basis()                  factor_basis decoded
A_rop(x, d; i)            rop_factor(k)                       ROP factor in force, eq (3)
(d in whole years)        rop_deferral_yrs(k)                 d_k rounded half to even, the
                                                              ROP table's key
(same, computed)          rop_factor_calc(k)                  ROP factor, mid-band rule
a_def(x, d, f; i)         annuity_factor_def(k)               Deferred APV, eq (1)
pr(x, d, f)               purchase_rate(k)                    Purchase rate, eq (4)
(none)                    purchase_rate_dp()                  Its decimal places, -1 for all
n_g (pricing)             guarantee_mths_pricing()            n_g in the kernel, eq (5)
(n_g as priced)           guarantee_mths_pricing_init()       The same, carried in force
("three iterations")      pricing_iters                       Fixed points taken on eq (5)
n_g (realized)            guarantee_yrs()                     CP(T)/B(T), eq (5)
n_R                       certain_mths_refund()               Derived refund period, months
n_eff                     certain_mths_eff()                  Effective certain months
C(t)                      certain_floor(t)                    Certain-floor indicator
(C by policy month)       certain_floor_pm(k)                 The same, in policy month k
L(t), L_pay(t)            payment_factor_life(t)              Life-contingent payment factor
l_last(T)                 surv_to_payout()                    Cohort reaching the income
                                                              phase
(l_last(T) in force)      surv_to_payout_init()               The same, carried in force
Phi(t)                    payment_factor(t)                   max(C(t) * l_last(T), L(t))
inst(t)                   annuity_pp_sched(t)                 Scheduled instalment
(inst by policy month)    annuity_pp_sched_pm(k)              The same, in policy month k
(inst as payable)         annuity_pp(t)                       Instalment after a blackout
(inst after commutation)  annuity_pp_paid(t)                  inst * (1 - theta_cum * C)
G(k)                      cum_annuity_pp(k)                   Cumulative instalments through
                                                              policy month k
RG(t)                     refund_balance(t)                   Refund balance at the start of
                                                              t
phase(t)                  phase(t)                            PRE_ISSUE / DEFERRAL /
                                                              PAYOUT / TERMINATED
(t >= T)                  is_payout(t)                        In the income phase
T (payment dates)         is_payment_mth(t)                   Month t is a payment date
(by policy month)         is_payment_pm(k)                    Policy month k is a payment
                                                              date
(payment point)           payment_surv_mth(t)                 Time survival is measured at
Baa(t_e)                  baa_yield                           Moody's Baa yield at t_e
s_adj                     adjust_spread                       Repricing spread, 100 bp
i_e                       repricing_rate()                    Start-date repricing rate,
                                                              eq (10)
B'/B                      adjust_income_factor()              Repricing factor, eq (11)
t_e                       adjust_mth()                        Start-date exercise month
T'                        adjust_start_mth()                  New income start month
t_a                       accel_mth()                         Acceleration exercise month
n_a                       accel_months                        Payments accelerated, 6
Cost(t_a)                 accel_cost()                        Acceleration cost, eq (12)
accel_blackout(t)         accel_blackout(t)                   Payments suspended
(Phi, frozen at t_a)      accel_payment_factor(t)             Weight on an accelerated
                                                              payment
t_c                       commute_mth()                       Commutation exercise month
(commuted share)          commute_frac()                      Fraction commuted at t_c
r_ref(t) - r_ref(0)       ref_rate_shift_init()               Reference-rate change from
                                                              issue to the valuation date
(the change at t = 0)     ref_rate_shift                      Reference-rate change made at
                                                              the valuation date; none for a
                                                              policy issued later
i_c(t)                    commute_disc_rate(t)                Commutation rate, eq (13)
m_c                       commute_margin                      Commutation margin, 50 bp
CV(t)                     commuted_value(t)                   Commuted value, eq (14)
theta_cum(t)              commute_frac_cum(t)                 Cumulative commuted fraction
(l_last(t_c))             commute_weight(t)                   Cohort a commutation
                                                              extinguishes
(l_last(t_c) in force)    commute_weight_init()               The same, carried in force
E[COMM(t)]                commutations(t)                     Commutation paid to the owner
Limit(year)               qlac_premium_limit                  QLAC premium limit, $210,000
qlac_room(t)              qlac_room(t)                        Remaining QLAC premium room
(none)                    other_qlac_premium()                Premiums to any other QLAC
(age 85 outside date)     qlac_max_start_age                  Latest QLAC income start age
(QLAC conditions)         qlac_flags()                        QLAC compliance failures
(premium income)          premiums(t)                         l(t) * premium paid at t
(deferral DB)             claims(t, DEATH)                    Return of CP(t) on death
(refund benefit)          claims(t, REFUND)                   Cash-refund lump sum
(per contract)            claim_pp(t, kind)                   Claim amount per contract
E[income]                 annuity_payments(t)                 Expected income outgo
e, g                      expense_maint, inflation_rate       Maintenance expense and
                                                              escalation
(1+g)^(t//12)             inflation_factor(t)                 Expense inflation factor, on
                                                              the valuation clock
E[EXP(t)]                 expenses(t)                         Maintenance expense
(total outgo)             liability_outgo(t)                  Gross liability outgo
(none)                    liability_cf(t)                     Net stream, outgo positive
(none)                    net_cf(t)                           Premiums less outgo
========================  ==================================  ==============================

Every input of the notes has a row above, and so do the model's own additions, which the
notes give no symbol but which drive the in-force projection: the counts, the clocks, the
opening state and the decodes. Only the outputs and diagnostics are left out —
:func:`model_point`, :func:`premium_schedule`, the annual display cells
:func:`lives_if_ann`, :func:`claims_ann` and :func:`annuity_payments_ann`, the reports
:func:`result_cf`, :func:`result_pols` and :func:`result_annual`, and the ``check_*``
cells — because they are not quantities the notes define.

Seven names in that table needed care.

``l`` and ``L`` differ in the notes only by case — the survival probability versus the
life-contingent payment factor — so they become ``lives_if`` and
``payment_factor_life``, exactly as in :mod:`.SPIA_US_S`. ``L`` is *also* the
expense and profit load in equation (4); that one is the Reference ``expense_load``.

``l`` is also two curves here, where the notes have one: the projection's
:func:`lives_if`, on the valuation clock from the opening state, and the pricing kernel's
:func:`lives_if_pm`, on the policy clock from issue. On a point issued at the valuation
date they are the same numbers at every time point.

``B`` is the guaranteed **annual** income and ``B(t)/m`` is one instalment; the notes
never name the instalment, so it takes the chassis name ``annuity_pp_sched``. Note that
``annual_income(t)`` is indexed by **month**, not by policy year as in
:mod:`.SPIA_US_S`, because a DIA's income level changes when a *premium* is paid
and premiums fall on months.

``n_g`` is three different quantities in the notes and they must not be conflated.
:func:`guarantee_mths_pricing` is the guarantee period fed into the pricing kernel by
equation (5) — a fixed point, since ``n_g = CP(T)/B`` and ``B`` depends on ``n_g``.
:func:`guarantee_yrs` is the realized value once ``B`` is known, the 3.3891 years the
worked example quotes. And :func:`certain_mths_eff` — the *projection's* certain floor —
is **zero on a cash-refund contract**, because a cash refund is a lump sum at death, not
a stream of guaranteed payments. Equation (5) is a pricing approximation for both refund
forms; only installment refund actually pays a certain stream.

``theta`` appears **nowhere** in the DIA notes.  ``theta_cum``, the cumulative commuted
fraction, is inherited from the immediate-annuity notes that these notes incorporate by
reference for the whole income phase; the DIA notes write equations (13) and (14) with
no symbol for the fraction at all.  The cells keeps the chassis name,
:func:`commute_frac_cum`, so that the two models read alike.

Two cohort weights carry no notes symbol because the notes have no need of one: a SPIA
is already in payment and its whole model point reaches the income phase together.
:func:`surv_to_payout` is ``l_last(T)``, the cohort that ever reaches the income phase
and therefore the only cohort a guarantee period can pay; :func:`commute_weight` is
``l_last(t_c)``, the sub-cohort still alive to exercise a commutation and therefore the
only cohort whose guarantee a commutation can extinguish.  They are the same idea
applied at two dates, and getting either of them wrong moves the guaranteed leg without
moving anything else. A contract valued after either date carries it in its opening
state, because the lives at the valuation date can no longer say it.

``CP(T)`` is the DIA-specific change to the payout chassis and the notes' own listed
pitfall: **the refund base is cumulative premiums, not the initial premium.** Where
``SPIA_US_S`` writes ``premium_pp()``, this model writes :func:`cum_premium_payout`.

The self-checks follow the library-wide ``check_*`` convention, which is
``CashValue_SE.check_av_roll_fwd()``'s: each check takes **no argument and returns a
bool** covering every projected ``t``, so one test can call the same name across every
model in the library, and each carries a companion ``check_*_resid(t)`` returning the
signed float residual at a single ``t`` for the debugging session that follows a failure.
The bool is defined in terms of the residual, never the other way round.
:func:`check_lives_roll_fwd`, :func:`check_income_roll_fwd`,
:func:`check_payment_factor` and :func:`check_commutation_value` are the four here; there
is no ``check_av_roll_fwd``, because there is no account value to roll forward.

.. rubric:: The state variables do not share one timing

Month ``t`` spans time ``t`` to time ``t + 1``, and the state cells sit at three different
instants inside it.

- ``l(t)`` and ``RG(t)`` are **start-of-month** values. ``lives_if(t, life)`` is survival
  to the start of month ``t``; :func:`refund_balance` is measured before the arrears
  instalment due at the end of the month, ``CP(T) - G(m - 1)`` at policy month ``m``,
  which is why a death in month ``T`` refunds the full ``CP(T)``. (On *advance* timing the
  instalment paid at the start of the month has been paid, so that one is netted:
  ``CP(T) - G(m)``.)
- ``CP(t)`` and ``B(t)`` are the values **during** month ``t`` — after the premium
  received at its start, which is exactly what makes the deferral death benefit
  ``CP(t) * l(t) * q(t)`` right and what lets a slice bought at the start of ``t`` be
  guaranteed from that moment. Entering month 0 they are the opening state, the values
  :mod:`~.DIA_US_S` holds during the month before the valuation month.
- ``G(k)`` is a **closing** balance: cumulative scheduled instalments through the *end*
  of policy month ``k``. ``G`` and ``RG`` are therefore exactly one month apart by
  construction, not by accident.

None of them is a recursion seed living before the frame: each opens at :func:`t_entry`,
from the opening state in force and from its value at issue otherwise, and nothing in this
model is indexed at a time point before it on the valuation clock.

.. rubric:: Two pricing bases: tabulated and computed

The notes' worked example is priced off illustrative factors it states outright —
``a^(12)_80(cash refund, female; 4.75%) = 8.60``, ``A_rop(60, 20) = 0.157900``,
``A_rop(65, 15) = 0.180200`` — declaring them "mutually consistent illustrative values,
**not** table lookups". Both readings are shipped, and which one applies is a model point
column:

``factor_basis = "table"``
    :func:`payout_factor` and :func:`rop_factor` read the shipped factor tables, and
    :func:`annuity_factor_def` is the notes' equation (1) literally,
    ``v^d * _d p_x * a^(m)``. Model points 1, 2 and 4, and the points restated from point
    1, 19 and 25. This is the basis that reproduces the worked example. It is single-life
    only: equation (1) factorizes the deferral survival out of the payout APV, which a
    joint status does not permit, and ``Data`` refuses a joint contract on it.

``factor_basis = "formula"``
    :func:`payout_factor_calc` computes equation (2) and :func:`rop_factor_calc` the
    notes' mid-band approximation of equation (3), both off the shipped mortality table,
    and :func:`annuity_factor_def` values the whole deferred stream in one pass so joint
    forms work. Model points 3, 5 to 18, 20 to 24 and 26.

The shipped mortality table is **[std]**, built so that the two bases agree where the
notes say they should: its rates over ages 60-84 are band-constant values reproducing
the notes' five-year survival anchors exactly, and the geometric continuation past age
85 is calibrated so that equation (2) at the income start age returns 8.600 — the notes'
own illustrative payout factor. Where they then *disagree* is ``A_rop(60, 20)``; see
below.

.. rubric:: The A_rop(60, 20) divergence is shipped, not resolved

The notes say ``A_rop`` was "computed from the same survival anchors with a mid-band
death-timing approximation". Run that recipe and the twenty-year factor comes out at
**0.161605**, not the **0.157900** the notes print, while the fifteen-year factor comes
out at **0.180241** against a printed **0.180200** — agreement to four decimal places.
One of the two is arithmetically consistent with the stated recipe and the other is not.
Rather than choose, the model ships both: model point 1 takes the printed factors from
``rop_factor_table.csv`` and reproduces the worked example, model point 3 is otherwise
identical and computes them. A test of :mod:`~.DIA_US_S`'s pins the gap open, and the twin
identity carries it here.

.. rubric:: The purchase-rate rounding is a [std] convention, and it is worth 3.6 cents

The worked example computes ``B_1 = 100,000 x 0.321765 = $32,176.50`` from a purchase
rate printed to six decimals. At full precision ``pr_1 = 0.3217647`` and the same
premium buys ``$32,176.47``; over both slices the difference is 3.6 cents on a
``$44,259.65`` income. The model point column ``purchase_rate_dp`` carries the
convention — 6 on point 1, blank (full precision) on point 2 — so the worked example
reproduces to the cent without the rounding being hidden.

.. rubric:: The certain period is a floor, not a second stream

``payment_factor(t) = max(certain_floor(t) * l_last(T), payment_factor_life(t))`` is
inherited from the payout chassis and is the notes' first-listed payout pitfall. During
the certain period the full, *unreduced* instalment is payable regardless of survival; an
additive construction would pay ``1 + L`` and silently double the guarantee. The ``max``
also reproduces, with no extra logic, the rule that a survivor reduction falling inside a
guarantee period is deferred to the end of that period.

.. rubric:: There is no lapse decrement, and adding one is a defect

"Lapse and surrender: exactly zero, at all durations. Not conservatism — there is no
surrender benefit to elect [R9][R13]. A nonzero lapse assumption in a DIA model is a
defect, not a margin." There is no ``lapse_rate``, no ``pols_lapse``, no surrender cash
flow row and no account value roll-forward in this model, and none should be added:
the liability is a schedule of income slices keyed on (premium, purchase date, income
start date, income option), not a balance.

.. rubric:: Codes

What :mod:`~.DIA_US_S` spells as text, a timing, a kind or a phase, is here an int
Reference named as the text it replaces, so that every cell takes and returns C numbers;
and so is the basis :func:`annuity_factor_at` prices on, which :mod:`~.DIA_US_S` passes as
float arguments to ``annuity_factor``. A call site reads as it did, less the quotes:
``pols_if_at(t, BEF_DECR)``, ``claims(t, DEATH)``.

=============  =====  ===============================================================
Reference      Value  Meaning
=============  =====  ===============================================================
BEF_NB         0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR       1      :func:`pols_if_at`: that count plus month t's new business
DEATH          0      :func:`claim_pp`, :func:`claims`, :func:`claims_ann`: the deferral
                      death benefit
REFUND         1      the same: the cash refund
ALL            2      :func:`claims` and :func:`claims_ann`: the two kinds' total,
                      :mod:`~.DIA_US_S`'s ``kind=None``
PRE_ISSUE      0      :func:`phase`: before a point issued after the valuation date
DEFERRAL       1      :func:`phase`: before the income start month
PAYOUT         2      :func:`phase`: from the income start month
TERMINATED     3      :func:`phase`: from the stop rule on
PURCHASE       0      :func:`annuity_factor_at`: a premium's purchase, at ``i_p``, from
                      the income start month it is priced to
ADJUST_OLD     1      :func:`annuity_factor_at`: a start-date adjustment, at ``i_e``,
                      from the old income start month
ADJUST_NEW     2      the same, from the new income start month
=============  =====  ===============================================================

Each family is numbered densely from 0, since a code a cell takes indexes that cell's
cache, a C array three codes wide, the width of every 2-D cache of the model, the lives'
(``spec_sec.py``). A code inside the cache that names nothing raises as
:mod:`~.DIA_US_S` raises on text it does not know: ``claim_pp(t, ALL)`` raises
``ValueError("invalid kind")``, as :mod:`~.DIA_US_S`'s ``claim_pp(t, None)`` does.
:mod:`~.DIA_US_S`'s total is the sum of its two kinds' cells, ``claims(t, "DEATH") +
claims(t, "REFUND")``, so ``claims(t, ALL)`` keeps it as written, and keeps its float,
the sign of a zero included. They are References, not cells, so the symbol map does not
list them. Every other Reference is named in lower case, ``issue_age_min`` and
``omega_age`` among them, the contract's bounds that :func:`stop_mth` checks and that the
compiled model's caches are sized from, with ``Data.future_horizon_mth``.

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`market_type`, :func:`income_form`,
:func:`payout_form`, :func:`db_form`, :func:`payment_timing`, :func:`mort_basis`,
:func:`factor_basis`, :func:`reduction_trigger` and :func:`sex`, the reports
:func:`result_cf`, :func:`result_pols` and :func:`result_annual`, and the four checks are
written for a reader and for the comparison with :mod:`~.DIA_US_S`, which has every one
of them: a table row, text, DataFrames and verdicts. No other cell calls them: each reads
the number ``Data`` decoded from the same column instead, the decodes' flags and the
schedules the sexes select. So the row, the text and the frames stay Python when the
model compiles. Each label returns its point's column: the column of its own name, but
``payment_timing`` the ``timing`` column, ``sex(life)`` the ``sex`` or ``joint_sex``
column by life, and ``payout_form`` the ``income_form`` column with ``LO_ROP`` read as
``LO``, as the registry declares them. Each validates its column, as
:mod:`~.DIA_US_S`'s does, and so returns text or raises, but ``sex``, which returns its
column as read, a blank second life on a single-life contract as NaN, and the compiled
accessor returns the same. The checks may stay Python but compile to a ``bint``, their
verdict, as their per-month residuals, ``*_resid``, compile to a ``double``.

And five cells of :mod:`~.DIA_US_S`'s are kept for a reader and for the comparison, and
called by no other cell but each other, the registry's ``"engine"`` cells: the pricing
kernel's two of float parameters, :func:`annuity_factor` and :func:`pricing_disc_factor`,
which compile with C signatures and dict caches, their bodies Python, the projection
holding their arithmetic in :func:`annuity_factor_at` and inline; and
:func:`premium_schedule`, :func:`premium_by_mth` and :func:`qlac_flags`, which take no
parameter and return a DataFrame, a dict and a list, the projection reading the premiums
from ``Data``'s premium table instead and nothing reading the flags. Every other cell
returns a C ``bint``, ``long long`` or ``double``.
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
    cell (the Space docstring's *Reporting cells*), which only the label accessors read.
    Every projection cell reads its own ``Data`` vector instead.
    """
    return data.model_point_table().iloc[idx]                        # noqa: F821


def point_id():
    """The label of the selected model point, its ``point_id``, from ``Data.point_id``.

    ``Projection`` is indexed by position, ``idx``, as ``basiclife.BasicTerm_SC`` is; the
    label is what a reader finds in the table, so every refusal names it.
    """
    return int(data.point_id()[idx])                                 # noqa: F821


def age_at_entry(life):
    """x: issue age (ANB) of the primary (life = 1) or joint (life = 2) annuitant.

    Age nearest birthday **[std]**: the archetype guide states contract issue age on an
    ANB basis [S2], prescribed VM-22 payout mortality is ANB [R9], and the 2012 IAM
    Basic and Period tables were developed ANB [R15][REG-R59].  The age at issue, not at
    the valuation date: ``age(0, life)`` is the attained age then.

    Read from ``Data.issue_age`` and ``Data.joint_age``, ``int()`` of the column.  An age
    ``int()`` cannot read, text or a blank, or one of ``2**53`` or more in size, is
    refused here, naming the point: a single-life contract's blank ``joint_age``, which no
    projection reads, only by a direct call.  :func:`stop_mth` refuses an issue age the
    contract does not cover.
    """
    if life == 1:
        if data.issue_age_ok()[idx] == 0:                            # noqa: F821
            raise ValueError(f"point_id {point_id()}: issue_age must be a number int() "
                             f"reads, below 2**53 in size; it is not")
        return int(data.issue_age()[idx])                            # noqa: F821
    if life == 2:
        if data.joint_age_ok()[idx] == 0:                            # noqa: F821
            raise ValueError(f"point_id {point_id()}: joint_age must be a number int() "
                             f"reads, below 2**53 in size; it is not")
        return int(data.joint_age()[idx])                            # noqa: F821
    raise ValueError("invalid life")


def sex(life):
    """Sex (M / F) of the primary (life = 1) or joint (life = 2) annuitant.

    A label accessor, which no projection cell calls: it returns the ``sex`` or
    ``joint_sex`` column as read, a single-life contract's blank second life as NaN.  The
    age readers and the factor tables join on the sex through ``Data``'s schedules
    instead.
    """
    if life == 1:
        return model_point()["sex"]
    if life == 2:
        return model_point()["joint_sex"]
    raise ValueError("invalid life")


def is_joint():
    """True when the contract covers two annuitants [S2][S4].

    The ``joint`` column as ``Data`` checked it, a flag, from ``Data.is_joint``:
    ``DIA_US_S``'s ``bool()`` of the raw value reads any text, ``"no"`` and a blank among
    them, as ``True``.
    """
    return bool(data.is_joint()[idx])                                # noqa: F821


def survivor_pct():
    """delta: the survivor percentage, in {0.50, 2/3, 0.75, 1.00} [S1][S2][S4].

    Read from ``Data.survivor_pct``, a probability on every point, as ``Data`` checks.
    """
    return float(data.survivor_pct()[idx])                           # noqa: F821


def reduction_trigger():
    """trig: whether the reduction is triggered by *either* death or the *primary*'s.

    A switch, not a parameter: the two conventions coincide on the primary's death and
    differ only on the secondary's [S1][S2][S4].  A label accessor, which no projection
    cell calls.
    """
    v = model_point()["reduction_trigger"]
    if v not in ("either", "primary"):
        raise ValueError("invalid reduction_trigger")
    return v


def is_trigger_either():
    """Whether either death triggers the survivor reduction, not the primary's alone.

    A decode of the model point's ``reduction_trigger`` column, ``Data.is_trigger_either``,
    validated by ``Data.has_reduction_trigger`` as :func:`reduction_trigger` validates it,
    so that :func:`payment_factor_life` and the pricing kernel branch on a flag and no
    projection cell calls the label accessor, which is left to reporting.
    """
    if data.has_reduction_trigger()[idx] == 0:                       # noqa: F821
        raise ValueError("invalid reduction_trigger")
    return bool(data.is_trigger_either()[idx])                       # noqa: F821


def market_type():
    """The tax wrapper: NQ, TradIRA, RothIRA or QLAC [S2][S4].

    A label accessor, which no projection cell calls.
    """
    v = model_point()["market_type"]
    if v not in ("NQ", "TradIRA", "RothIRA", "QLAC"):
        raise ValueError("invalid market_type")
    return v


def is_qlac():
    """True when the contract is intended to be a QLAC [R1 (q)(1)(vi)].

    A decode of the model point's ``market_type`` column, ``Data.is_qlac``, validated by
    ``Data.has_market_type`` as :func:`market_type` validates it, so that
    :func:`qlac_flags` branches on a flag and calls no label accessor.
    """
    if data.has_market_type()[idx] == 0:                             # noqa: F821
        raise ValueError("invalid market_type")
    return bool(data.is_qlac()[idx])                                 # noqa: F821


def income_form():
    """f: the income option elected at issue and immutable thereafter [S1][S2][S4].

    ``LO`` life only; ``LO_ROP`` life only with a 100% return-of-purchase-payments death
    benefit in deferral, the unbundled extended-case variant [S4]; ``CR`` life with cash
    refund; ``IR`` life with installment refund; ``PC`` life with period certain.  A label
    accessor, which no projection cell calls.
    """
    v = model_point()["income_form"]
    if v not in ("LO", "LO_ROP", "CR", "IR", "PC"):
        raise ValueError("invalid income_form")
    return v


def payout_form():
    """The payout stream the elected form implies: LO, CR, IR or PC.

    ``LO_ROP`` collapses to ``LO`` here because its return of premium is a *deferral*
    death benefit carried by :func:`db_form`; after the income start date it is a pure
    life annuity [S4].  The unbundling of the death benefit from the payout form is the
    product spec's chosen parameterization, so that the two mortality exposures move
    independently.  A label accessor, which no projection cell calls: the ``income_form``
    column's value with ``LO_ROP`` read as ``LO``, as the registry declares it.
    """
    f = income_form()
    return "LO" if f in ("LO", "LO_ROP") else f


def is_life_only():
    """Whether the payout stream is life only: ``income_form`` LO or LO_ROP.

    One of four decodes of the model point's ``income_form`` column, as are the three below
    it, so that no projection cell compares text or calls :func:`income_form` or
    :func:`payout_form`, the label accessors, which are left to reporting.  Each reads
    ``Data``'s flag for its value, and ``Data.has_income_form``, which says whether the
    column holds one of the five values :func:`income_form` accepts, compared as it
    compares them, so an invalid form raises ``ValueError("invalid income_form")``
    wherever the projection first meets it.  ``LO_ROP`` is life only in payout, as
    :func:`payout_form` collapses it.
    """
    if data.has_income_form()[idx] == 0:                             # noqa: F821
        raise ValueError("invalid income_form")
    return bool(data.is_life_only()[idx])                            # noqa: F821


def is_cash_refund():
    """Whether the form is cash refund, CR: a lump sum of ``CP(T) - G`` on the last death.

    A decode of the ``income_form`` column, validated as :func:`income_form` validates it.
    """
    if data.has_income_form()[idx] == 0:                             # noqa: F821
        raise ValueError("invalid income_form")
    return bool(data.is_cash_refund()[idx])                             # noqa: F821


def is_installment_refund():
    """Whether the form is installment refund, IR: a certain period derived from ``CP(T)``.

    A decode of the ``income_form`` column, validated as :func:`income_form` validates it.
    """
    if data.has_income_form()[idx] == 0:                             # noqa: F821
        raise ValueError("invalid income_form")
    return bool(data.is_installment_refund()[idx])                      # noqa: F821


def is_period_certain():
    """Whether the form is life with period certain, PC: an elected certain period.

    A decode of the ``income_form`` column, validated as :func:`income_form` validates it.
    """
    if data.has_income_form()[idx] == 0:                             # noqa: F821
        raise ValueError("invalid income_form")
    return bool(data.is_period_certain()[idx])                          # noqa: F821


def db_form():
    """The deferral-phase death benefit: ``ROP`` or ``NONE``.

    100% of cumulative premiums, no interest, lump sum, on every option except Life Only
    and Joint Life Only [S1][S2][S3][S4][R13 SS3.I(1)(a)].  This is the product's central
    pricing fork: setting it to ``NONE`` removes ``A_rop`` from the numerator of equation
    (4) and buys strictly more income for the same premium.  A label accessor, which no
    projection cell calls.
    """
    v = model_point()["db_form"]
    if v not in ("ROP", "NONE"):
        raise ValueError("invalid db_form")
    return v


def is_rop():
    """Whether the contract carries the return-of-premium death benefit in deferral.

    A decode of the model point's ``db_form`` column, ``Data.is_rop``, validated by
    ``Data.has_db_form`` as :func:`db_form` validates it, so that the ROP factor and the
    death claim branch on a flag and no projection cell calls the label accessor.
    """
    if data.has_db_form()[idx] == 0:                                 # noqa: F821
        raise ValueError("invalid db_form")
    return bool(data.is_rop()[idx])                                  # noqa: F821


def certain_period():
    """n: the elected certain period in years, 10-30 on PC forms [S2]; 0 otherwise.

    Read from ``Data.certain_period``, ``int()`` of the column; one ``int()`` cannot read,
    or of ``2**53`` or more in size, is refused here, naming the point.  Only a period
    certain reads it.  :func:`stop_mth` refuses a period ending later than the caches hold.
    """
    if data.certain_period_ok()[idx] == 0:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: certain_period must be a number int() "
                         f"reads, below 2**53 in size; it is not")
    return int(data.certain_period()[idx])                           # noqa: F821


def payment_freq():
    """m: payments per year, in {12, 4, 2, 1}; fixed at issue [S1][S2].

    Read from ``Data.frequency``, ``int()`` of the column, as ``Data`` checked it a whole
    number; one of ``2**53`` or more in size is refused, naming the point, and any other
    number raises ``DIA_US_S``'s ``ValueError("invalid frequency")``.  The element is
    compared, never held in a local, so the compiled cell keeps no Python object.
    """
    if data.frequency_ok()[idx] == 0:                                # noqa: F821
        raise ValueError(f"point_id {point_id()}: frequency must be a number int() reads, "
                         f"below 2**53 in size; it is not")
    if (data.frequency()[idx] == 12 or data.frequency()[idx] == 4    # noqa: F821
            or data.frequency()[idx] == 2 or data.frequency()[idx] == 1):  # noqa: F821
        return int(data.frequency()[idx])                            # noqa: F821
    raise ValueError("invalid frequency")


def payment_timing():
    """Whether instalments fall in *arrears* (the **[std]** default) or in *advance*.

    No retrieved DIA document states the convention; arrears matches
    ``products/immediate_annuity/product-spec.md`` so that one payout chassis serves
    both products.  A label accessor, which no projection cell calls: it returns the
    ``timing`` column, compared exactly, or raises.
    """
    v = model_point()["timing"]
    if v not in ("arrears", "advance"):
        raise ValueError("invalid timing")
    return v


def is_arrears():
    """Whether instalments fall in arrears, at the end of the month, rather than in advance.

    A decode of the model point's ``timing`` column, ``Data.is_arrears``, validated by
    ``Data.has_timing`` as :func:`payment_timing` validates it, so that the payment
    months, the survival point, the refund balance, the refund-period search and the
    pricing kernel branch on a flag and no projection cell calls the label accessor.
    """
    if data.has_timing()[idx] == 0:                                  # noqa: F821
        raise ValueError("invalid timing")
    return bool(data.is_arrears()[idx])                              # noqa: F821


def cola_rate():
    """c: the fixed compound annual increase, 0 or 1%-4%, elected at issue [S2][S3][S4].

    Every observed option is a fixed compound escalator applied on each anniversary of
    the income start date, **not** a CPI adjustment - the notes list treating it as
    index-linked among the product's pitfalls.  Read from ``Data.cola_rate``, a number
    zero or more on every point, as ``Data`` checks.
    """
    return float(data.cola_rate()[idx])                              # noqa: F821


def issue_year():
    """The calendar year of issue **[std]**; the anchor of the generational projection.

    The improvement exponent is ``calendar_year(t) - mort_table_year``.  The chassis
    calls its counterpart ``annuity_year`` because a SPIA's annuity date *is* its issue
    date; here the two are twenty years apart, so the generational anchor has to be
    named for the one that matters.  Read from ``Data.issue_year``, ``int()`` of the
    column; one ``int()`` cannot read, or of ``2**53`` or more in size, is refused here,
    naming the point.  Only the generational basis and the calendar year read it.
    """
    if data.issue_year_ok()[idx] == 0:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue_year must be a number int() reads, "
                         f"below 2**53 in size; it is not")
    return int(data.issue_year()[idx])                               # noqa: F821


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the contracts in force then, before any
    month-0 event; any other point counts the contracts it issues.  Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second.  It is ``DIA_US_S``'s
    ``pols_if_init`` column, renamed, and like it a constant on the books: mortality
    decrements each life's survival, :func:`lives_if`, never the count.  Read from
    ``Data.policy_count``.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """Contracts in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0`` (``duration_mth_init() >
    0``), and 0 for one issued at or after it, whose contracts enter through
    :func:`pols_new_biz` in the issue month instead, as in ``basiclife.BasicTerm_SE``.  So
    on a point issued at ``t = 0`` this is 0, where ``DIA_US_S``'s is the count itself; on
    either model the count that weights row 0 is the same, here
    ``pols_if_at(0, BEF_DECR)``.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def mort_basis():
    """Whether mortality is the notes' *anchor* curve or the *generational* projection.

    *anchor* **[std]**: the shipped table is used as a period table, which is what
    reproduces the worked example - its survival anchors are a single non-generational
    curve.  *generational*: the notes' prescribed construction
    ``q^(2012+k) = q^(2012) * (1 - G2_x)^k`` [R9][REG-R59] is applied with the shipped
    illustrative improvement scale.  Both are shipped because the notes prescribe the
    second and verify against the first.  A label accessor, which no projection cell calls.
    """
    v = model_point()["mort_basis"]
    if v not in ("anchor", "generational"):
        raise ValueError("invalid mort_basis")
    return v


def is_generational():
    """Whether mortality is the generational projection rather than the anchor curve.

    A decode of the model point's ``mort_basis`` column, ``Data.is_generational``,
    validated by ``Data.has_mort_basis`` as :func:`mort_basis` validates it, so that
    :func:`mort_rate_py` branches on a flag and no projection cell calls the label
    accessor.
    """
    if data.has_mort_basis()[idx] == 0:                              # noqa: F821
        raise ValueError("invalid mort_basis")
    return bool(data.is_generational()[idx])                         # noqa: F821


def factor_basis():
    """Whether the pricing factors are *table* lookups or *formula* computations.

    *table*: :func:`payout_factor` and :func:`rop_factor` read the notes' illustrative
    factors and :func:`annuity_factor_def` is equation (1) literally - the basis that
    reproduces the worked example, single-life only.  *formula*: both are computed from
    the shipped mortality table by equations (2) and (3).  See the Space docstring.  A
    label accessor, which no projection cell calls.
    """
    v = model_point()["factor_basis"]
    if v not in ("table", "formula"):
        raise ValueError("invalid factor_basis")
    return v


def is_formula_basis():
    """Whether the pricing factors are formula computations rather than table lookups.

    A decode of the model point's ``factor_basis`` column, ``Data.is_formula_basis``,
    validated by ``Data.has_factor_basis`` as :func:`factor_basis` validates it, so that
    :func:`payout_factor`, :func:`rop_factor` and :func:`annuity_factor_def` branch on a
    flag and no projection cell calls the label accessor.
    """
    if data.has_factor_basis()[idx] == 0:                            # noqa: F821
        raise ValueError("invalid factor_basis")
    return bool(data.is_formula_basis()[idx])                        # noqa: F821


def purchase_rate_dp():
    """Decimal places the purchase rate is rounded to, or -1 for full precision.

    **[std]**.  The worked example computes ``B`` from a six-decimal purchase rate;
    carrying full precision instead moves the anchor cell's annual income by 3.6 cents.
    Blank on the model point returns -1, meaning no rounding: modelx forbids a cells
    returning ``None``, so every "not set" on this Space is a negative sentinel.  Read
    from ``Data.purchase_rate_dp``, which holds the blank as -1 already; a value of
    ``2**53`` or more in size is refused here, naming the point.
    """
    if data.purchase_rate_dp_ok()[idx] == 0:                         # noqa: F821
        raise ValueError(f"point_id {point_id()}: purchase_rate_dp must be blank or below "
                         f"2**53 in size; it is not")
    return int(data.purchase_rate_dp()[idx])                         # noqa: F821


def other_qlac_premium():
    """Premiums paid to any other contract intended to be a QLAC [R1 (q)(2)(ii)(B)].

    The QLAC dollar limit is reduced by premiums paid to any other QLAC under any
    401(a), 403(a), 403(b), 408 or governmental 457(b) arrangement; the issuer may rely
    on the owner's written representation [R5 (h)(2)].  Read from
    ``Data.other_qlac_premium``.
    """
    return float(data.other_qlac_premium()[idx])                     # noqa: F821


def premium_schedule():
    """The selected contract's premium slices still due, ordered by payment month.

    A DIA is a flexible-premium contract - "any number of premiums during the deferral
    period" [S2][S3][S4][R13] - so the schedule is a separate long table rather than a
    fixed set of model point columns.  Its rows of ``premium_schedule_sec.csv``, which holds
    the premiums due at or after the valuation date: on a point issued at or after it the
    whole schedule, and on a point in force the premiums of policy months ``duration_mth``
    and later, those paid before being in the opening state.  Kept for a reader and for
    the comparison with ``DIA_US_S``, a DataFrame, and called by no cell but
    :func:`premium_by_mth`: the projection reads the premiums from ``Data.premium_array``,
    through :func:`premium_pm` (the Space docstring's *Reporting cells*).
    """
    tbl = data.premium_schedule_table()                              # noqa: F821
    return tbl[tbl["point_id"] == point_id()].sort_values("premium_mth")  # noqa: F821


def premium_by_mth():
    """The premium schedule still due collapsed to a ``{month: amount}`` mapping.

    Keyed by policy month, ``DIA_US_S``'s dict, kept for a reader and for the comparison
    with ``DIA_US_S``, and called by no projection cell: ``Data.premium_array`` holds the
    same sums by policy month, added in the same order, which :func:`premium_pm` reads,
    and ``Data.premium_rows`` the months with a row, which :func:`guarantee_mths_pricing`
    visits as ``DIA_US_S`` visits this dict's keys.
    """
    out = {}
    for _, r in premium_schedule().iterrows():
        k = int(r["premium_mth"])
        out[k] = out.get(k, 0.0) + float(r["premium_amt"])
    return out


def premium_pm(k):
    """P_k: the premium per contract paid at the **start** of policy month k; 0 if none.

    Keyed by policy month, on the policy clock, and the one cell that reads the premium
    schedule, so that :func:`premium_pp` reads a premium at the policy month of month t,
    and :func:`annual_income_payout` and :func:`cum_premium_payout` at every policy month
    from the valuation date's to the income start month, without passing a policy month as
    ``t``.  0 before the valuation date on a point in force, whose premiums paid are in its
    opening state.  Read from ``Data.premium_array``, the schedule summed by policy month
    as ``DIA_US_S``'s ``premium_by_mth`` sums it, and 0.0 past its last month, as
    ``DIA_US_S``'s ``dict.get`` gives it.  ``k`` is never negative: every caller reads a
    policy month from the valuation date's, or from issue, on.
    """
    if k >= data.premium_width():                                    # noqa: F821
        return 0.0
    return float(data.premium_array()[idx, k])                       # noqa: F821


def premium_pp(t):
    """P_k: the premium per contract paid at the **start** of month t; 0 if none falls.

    ``premium_pm(duration_mth(t))``, the premium of the policy month that month ``t`` falls
    in, inside the frame, and 0 outside it.
    """
    if not is_active(t):
        return 0.0
    return premium_pm(duration_mth(t))


def cum_premium_pp_init():
    """CP at the valuation date: the premiums per contract paid before it.

    The ``cum_premium_pp_init`` column, the cumulative premium entering month 0, before
    the premium, if any, received at its start: ``DIA_US_S``'s ``cum_premium_pp(d - 1)``
    on a point restated at its month ``d``.  The opening value of :func:`cum_premium_pp` at
    :func:`t_entry`, and the deferral death benefit's and the refund's base before the
    premiums still due are added.  0 at issue, and so on every point not yet in force, as
    ``Data`` checks.  Read from ``Data.cum_premium_pp_init``.
    """
    return float(data.cum_premium_pp_init()[idx])                    # noqa: F821


def cum_premium_pp(t):
    """CP(t): cumulative premiums paid per contract, equation (7).

    ``CP(t) = CP(t-1) + P_k`` at the premiums of month ``t``.  The recursion opens at
    :func:`t_entry`, the first month on the books, on the opening state,
    :func:`cum_premium_pp_init`, the premiums paid before the valuation date, which is 0
    on a point issued at or after it, so that ``CP(t_entry)`` is that plus the premium,
    if any, received at the start of the month.  The value is the one in force *during*
    month ``t`` - it already includes the premium received at the start of that month,
    which is what makes the deferral death benefit ``CP(t) * l(t) * q(t)`` right.  This is
    the deferral death benefit base; the refund base is ``CP(T)``,
    :func:`cum_premium_payout`, read from the income start month on.  **For a
    flexible-premium DIA the refund base is CP(T), not the initial premium**, which is one
    of the notes' listed pitfalls [S2][S4].  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    prev = cum_premium_pp(t - 1) if t > t_entry() else cum_premium_pp_init()
    return prev + premium_pp(t)


def cum_premium_payout():
    """CP(T): cumulative premiums per contract at the income start month, the refund base.

    ``cum_premium_pp_init()`` plus every premium still due, from the valuation date's
    policy month to the income start month ``T``, in one loop over the policy months, the
    same additions in the same order as the recursion :func:`cum_premium_pp`, so ``CP(T)``
    is ``DIA_US_S``'s ``cum_premium_pp(T)`` to the last bit.  On a contract past its
    income start month the loop is empty and ``CP(T)`` is the opening state: no premium
    falls at or after ``T``, as ``Data`` checks, so ``CP`` is level in payout.  A static
    quantity, so that the refund balance, the installment refund's search and
    :func:`guarantee_yrs` read the refund base without reading :func:`cum_premium_pp` far
    ahead of their month.
    """
    total = cum_premium_pp_init()
    for k in range(max(duration_mth_init(), 0), income_start_mth() + 1):
        total = total + premium_pm(k)
    return total


def duration_mth_init():
    """Months from issue to the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 241 for a contract issued 241 months before the
    valuation date, 0 for one issued at it, and -13 for one to be issued 13 months after
    it, which ``Data`` admits up to ``future_horizon_mth`` months ahead.  It is read as
    ``basiclife.BasicTerm_SE`` reads it, by value, and is the one fact the policy clock
    takes from the model point, from ``Data.duration_mth``; a value ``int()`` cannot read,
    or of ``2**53`` or more in size, is refused here, naming the point.
    """
    if data.duration_mth_ok()[idx] == 0:                             # noqa: F821
        raise ValueError(f"point_id {point_id()}: duration_mth must be a number int() "
                         f"reads, below 2**53 in size; it is not")
    return int(data.duration_mth()[idx])                             # noqa: F821


def duration_mth(t):
    """Months elapsed from issue at the start of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together.  A closed form, where
    ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers, without a
    call chain as long as the frame.  Negative before issue.  Everything contractual reads
    this clock: the policy year, the attained ages, the premium months, the income start
    month, the option months, the payment months, the COLA anniversaries and the certain
    period.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a contract in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later.  It is the base of every recursion on the valuation clock:
    :func:`lives_if`, :func:`cum_premium_pp` and :func:`annual_income` open there, from the
    opening state, and read no month before it, and :func:`pols_if_at` counts the contracts
    from there.
    """
    return max(0, -duration_mth_init())


def stop_mth():
    """The policy month at which the projection stops: the stop rule, on the policy clock.

    ``max(horizon_mths(), income_start_mth() + certain_mths_eff())``, ``DIA_US_S``'s frame
    length counted from issue: the month the youngest covered life attains the limiting
    age, or the end of the guarantee period if that is later.  The last projected month is
    policy month ``stop_mth() - 1``; :func:`proj_len` counts the months to the stop from
    the valuation date instead.  720 on the anchor cell, ages 60 to 119.

    Before it, the contract the compiled model's caches are sized for (``spec_sec.py``),
    each bound a lower-case Reference, each refusal naming the point: an issue age of a
    covered life below ``issue_age_min``, 0, on every form, the primary's and, on a joint
    contract, the joint annuitant's each asked, since a frame runs to the age stop on its
    youngest life; an income start month, at issue or in force after a start-date
    adjustment, past ``12 * (omega_age - issue_age_min)``, 1,440, the latest policy month
    the caches hold, both asked, since the premiums before an adjustment are priced to the
    old month; and a certain period ending past that month.  Each is checked here, before
    the stop rule, which reads the installment refund's search over :func:`cum_annuity_pp`
    up to :func:`horizon_mths`, and here rather than in :func:`proj_len`, so that every
    cell of a refused point that reads the frame, through :func:`is_active`, refuses it as
    :func:`proj_len` does, in both engines.  ``DIA_US_S`` projects every form at issue age
    0, on tables starting below 20, and so does this model, the product-spec's 22 bounding
    nothing; a negative issue age is outside every contract, and refused as Term's issue
    ages are, a departure from ``DIA_US_S``, which projects it.  ``DIA_US_S`` projects an
    income start month, or a certain period's end, past 1,440 too, and those are refused
    as what the caches cannot hold, as ``SPIA_US_SEC`` refuses a certain period of more
    than 1,440 months: recorded departures.  The product-spec's income start months, 13 to
    360, and certain periods, 10 to 30 years, bound nothing.  The installment refund
    rounds its derived period up to a whole instalment, so the stop rule ends at policy
    month 1,441 at most.
    """
    cap = 12 * (omega_age - issue_age_min)                           # noqa: F821
    if age_at_entry(1) < issue_age_min:                              # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry(1)} is below "
                         f"issue_age_min, {issue_age_min}")          # noqa: F821
    if is_joint() and age_at_entry(2) < issue_age_min:               # noqa: F821
        raise ValueError(f"point_id {point_id()}: joint issue age {age_at_entry(2)} is "
                         f"below issue_age_min, {issue_age_min}")    # noqa: F821
    if income_start_mth_init() > cap:
        raise ValueError(f"point_id {point_id()}: income_start_mth "
                         f"{income_start_mth_init()} is past 12 * (omega_age - "
                         f"issue_age_min), {cap}, the latest policy month the caches are "
                         f"sized for")
    if income_start_mth() > cap:
        raise ValueError(f"point_id {point_id()}: adjust_start_mth {income_start_mth()} "
                         f"is past 12 * (omega_age - issue_age_min), {cap}, the latest "
                         f"policy month the caches are sized for")
    if is_period_certain() and income_start_mth() + 12 * certain_period() > cap:
        raise ValueError(f"point_id {point_id()}: the certain period of "
                         f"{certain_period()} years from policy month "
                         f"{income_start_mth()} ends past 12 * (omega_age - "
                         f"issue_age_min), {cap}, the latest policy month the caches are "
                         f"sized for")
    return max(horizon_mths(), income_start_mth() + certain_mths_eff())


def is_active(t):
    """Whether month t is inside the frame: issued, and not yet at the stop rule.

    ``0 <= duration_mth(t) < stop_mth()``.  False before issue and from the stop rule on.
    Outside it every count is zero, and so every cash flow; no cell reads a rate, a policy
    year or an attained age there that the contract does not have.  A contract's own end
    inside the frame - its last death, or the end of its guarantee - is a probability or a
    floor reaching zero, not the end of the frame, which runs on with zeros as
    ``DIA_US_S``'s does.
    """
    return 0 <= duration_mth(t) < stop_mth()


def duration(t):
    """Completed policy years at the start of month t: ``duration_mth(t) // 12``.

    0 throughout the first policy year from issue, and negative before issue.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y = duration(t) + 1: the policy year containing month t, on the policy clock.

    The policy year is the contract's own 1-based label, ``duration_mth(t) // 12 + 1``, and
    is *derived* from the policy clock, never used to index the frame: 1 for policy months
    0..11, whatever ``t`` they fall at.  It is 0 or less before issue, where no cell reads
    a rate by it.  Used where the notes speak in policy years: the mortality rate, and the
    annual display grid.
    """
    return duration(t) + 1


def calendar_year(t):
    """The calendar year of the policy year containing month t, on the policy clock.

    ``issue_year() + duration(t)``: calendar-dated from the issue year, so a contract in
    force at the valuation date reads its own calendar years whatever that date, and
    nothing in the improvement it dates is re-based onto the valuation clock.  On a point
    restated from ``DIA_US_S`` at its month ``d``, month ``t`` here is ``DIA_US_S``'s month
    ``d + t``, and so the same calendar year.  :func:`mort_rate_py` computes the same year
    for a policy year.
    """
    return issue_year() + duration(t)


def age(t, life):
    """x(t) = x + duration(t): the attained age (ANB) of ``life`` in month t.

    On the policy clock: the age changes on each anniversary of issue, whatever the
    valuation date.
    """
    return age_at_entry(life) + duration(t)


def horizon_mths():
    """Months from issue to the limiting age of the *youngest* covered life.

    ``t/12 + x_i > omega_age`` for every covered life is the payout chassis' stop rule;
    stopping on the primary's age alone would truncate a younger joint annuitant's tail.
    Counted from issue, on the policy clock; :func:`stop_mth` and :func:`proj_len` take it.
    The younger of the two ages is found by one comparison, with no list, reading the
    cells ``DIA_US_S``'s ``min`` reads, in its order.
    """
    youngest = age_at_entry(1)
    if is_joint() and age_at_entry(2) < youngest:
        youngest = age_at_entry(2)
    return 12 * (omega_age - youngest)                               # noqa: F821


def proj_len():
    """The number of months from the valuation date to the stop rule.

    ``stop_mth() - duration_mth_init()``: 720 for the anchor cell issued at ``t = 0``, 479
    for it in force 241 months (point 19), 1 in its last month (point 25), and 733 for the
    joint point issued 13 months after the valuation date (point 26).  The exclusive end of
    the frame: :func:`result_cf` runs over ``range(proj_len())``, so the last projected
    month is ``proj_len() - 1``, which is policy month ``stop_mth() - 1`` on every point.

    The projection stops when it reaches the mortality horizon - the month the youngest
    covered life attains the limiting age, ``horizon_mths()`` - or the end of the
    guarantee period if that is later.  Both are age- or contract-driven rather than
    derived from the projection they bound, so the frame never depends on the survival
    path.

    Two kinds of point have no frame, and raise here, naming the point, rather than
    projecting nothing: an in-force extract should not carry either.  A point at or past
    the stop rule.  And a contract that owes nothing after the valuation date: in force,
    with every covered life dead at the valuation date, valued at or before its income
    start month, whose every death fell in the deferral and whose death benefit, if any,
    was paid before the valuation date; or valued after it, with its certain period over
    or no certain period at all, the refund, if any, having been paid at the last death.
    This is ``Term_US_SEC``'s point past its cover, for a product whose cover can end with
    a death.  The rule needs the certain period, which an installment refund derives from
    the payout schedule, so it is checked here rather than in ``Data``, and each message
    says why nothing is owed.  A contract in its certain period with every life dead pays
    the beneficiary, and projects.

    And one combination of the two payout options raises here, naming the point, because
    neither model prices it: an acceleration on the books, at or after the valuation date,
    whose lump sum pulls forward instalments of a guarantee that a commutation before it
    has reduced.  The lump sum pays each instalment it pulls forward at the payment
    factor, unreduced, as ``DIA_US_S``'s does, so the cohort that commuted would be paid
    those instalments again.  The guarantee's end needs the certain period, so this too is
    checked here.  ``Data`` refuses the two options within six months of each other, the
    product's interlock; an acceleration that pulls forward only the life-contingent
    instalments after the guarantee projects, and so does one paid before the valuation
    date, whose blackout months pay nothing.

    Before any of these, :func:`stop_mth` refuses a point outside the contract the
    compiled model's caches are sized for, naming it.  ``omega_age`` above 120,
    ``issue_age_min`` below 0, ``accel_months`` above 6 and ``Data.future_horizon_mth``
    above 120 are not refused: each needs the caches resized and the model rebuilt, and a
    report past them is a bare ``IndexError`` in the compiled model alone, where modelx
    projects.
    """
    d = duration_mth_init()
    n = stop_mth() - d
    if n <= 0:
        raise ValueError(f"point_id {point_id()}: duration_mth {d} is at or past the end "
                         f"of the projection, policy month {stop_mth()}")
    if d > 0:
        dead = not (lives_if_init(1) > 0.0 or (is_joint() and lives_if_init(2) > 0.0))
        start = income_start_mth()
        end = start + certain_mths_eff()
        if dead and d <= start:
            raise ValueError(f"point_id {point_id()}: duration_mth {d}: no payment is "
                             f"owed after the valuation date: every covered life has died "
                             f"before the income start month, {start}")
        if dead and d >= end and end > start:
            raise ValueError(f"point_id {point_id()}: duration_mth {d}: no payment is "
                             f"owed after the valuation date: every covered life has died, "
                             f"and the certain period ended at policy month {end}")
        if dead and d >= end:
            raise ValueError(f"point_id {point_id()}: duration_mth {d}: no payment is "
                             f"owed after the valuation date: every covered life has died, "
                             f"and the form has no certain period")
    a = accel_mth()
    c = commute_mth()
    if 0 <= c <= a and d <= a and commute_frac() > 0.0:
        end = income_start_mth() + certain_mths_eff()
        if a + 1 < end:
            raise ValueError(f"point_id {point_id()}: accel_mth {a} pulls forward "
                             f"guaranteed instalments that the commutation at policy "
                             f"month {c} reduced, the guarantee running to policy month "
                             f"{end - 1}: the lump sum would pay the cohort that commuted "
                             f"its instalments again")
    return n


def income_start_mth_init():
    """T at issue: the income start month elected at issue, ``13 <= T <= 360`` [S2][S4].

    ``T`` is a **policy month**, so the income start date is the **start** of policy month
    ``T``, exactly ``T/12`` years after issue, whatever the valuation date.  Under arrears
    the first instalment falls one payment period later - at ``m = 12``, at the end of
    policy month ``T``.  Read as ``Data`` checked it, a whole number of months, from
    ``Data.income_start_mth``, and compared with ``duration_mth(t)``, never with ``t``; a
    month of ``2**53`` or more in size is refused here, naming the point, and
    :func:`stop_mth` refuses one later than the caches hold.
    """
    if data.income_start_mth_ok()[idx] == 0:                         # noqa: F821
        raise ValueError(f"point_id {point_id()}: income_start_mth must be a number int() "
                         f"reads, below 2**53 in size; it is not")
    return int(data.income_start_mth()[idx])                         # noqa: F821


def adjust_mth():
    """t_e: the policy month a start-date adjustment is exercised; -1 if it never is.

    One-time, deferral only, excluded on Life Only and Joint Life Only [S1][S3][S4].
    The **incidence** of the exercise - the notes' 1.5% p.a. take-up with its 60/40
    direction split, rate multipliers and health-selection overlay - is a cohort-
    splitting behavioural construction and is **not implemented**; the exercise is
    named deterministically on the model point instead, and is off by default.  Read as
    ``Data`` checked it, blank or a whole number of months, and compared with
    ``duration_mth(t)``; a contract valued after it carries its repricing in
    ``annual_income_init``.
    Read from ``Data.adjust_mth``, which holds the blank as -1; a month of
    ``2**53`` or more in size is refused here, naming the point.
    """
    if data.adjust_mth_ok()[idx] == 0:                          # noqa: F821
        raise ValueError(f"point_id {point_id()}: adjust_mth must be blank or below "
                         f"2**53 months in size; it is not")
    return int(data.adjust_mth()[idx])                               # noqa: F821


def adjust_start_mth():
    """T': the new income start month after an adjustment, a policy month; -1 if none.

    ``|T' - T| <= 60`` months, ``T'`` at least 13 months after the last premium, and
    inside the maximum deferral and the maximum income start age [S1][S2][S3][S4].
    ``Data`` checks that it is given exactly where :func:`adjust_mth` is, and that it
    follows the exercise.
    Read from ``Data.adjust_start_mth``, which holds the blank as -1; a month of
    ``2**53`` or more in size is refused here, naming the point.
    """
    if data.adjust_start_mth_ok()[idx] == 0:                    # noqa: F821
        raise ValueError(f"point_id {point_id()}: adjust_start_mth must be blank or below "
                         f"2**53 months in size; it is not")
    return int(data.adjust_start_mth()[idx])                         # noqa: F821


def income_start_mth():
    """T in force: the adjusted start month if one is exercised, else the elected one."""
    return income_start_mth_init() if adjust_mth() < 0 else adjust_start_mth()


def income_start_mth_at(k):
    """The income start month a premium paid in policy month k is priced to.

    A premium bought before the adjustment was priced to the original date; one bought
    after it is priced to the new date [R13 SS3.B(1)(b)].  Keyed by the premium's policy
    month, ``DIA_US_S``'s ``t`` renamed: pricing stays on the policy clock.
    """
    a = adjust_mth()
    if a < 0 or k < a:
        return income_start_mth_init()
    return adjust_start_mth()


def repricing_rate():
    """i_e = Baa(t_e) - s_adj: the rate a start-date adjustment is repriced at, eq (10).

    The disclosed recipe keys on Moody's Seasoned Baa Corporate Bond Yield at the
    request date less a contractual interest-rate-change adjustment [S1][S2]; the
    adjustment is named but never quantified in any retrieved source, so the 100 bp
    spread is **[std]**.  The base run sets ``baa_yield`` so that ``i_e = i_p`` - no rate
    movement since issue - because the notes supply no Baa value **[std]**.  A flat level,
    so it reads the same on either clock.
    """
    return baa_yield - adjust_spread                                 # noqa: F821


def accel_mth():
    """t_a: the policy month payment acceleration is exercised; -1 if it never is.

    Payout phase, attained age 59 1/2 or over, nonqualified, monthly frequency
    [S1][S2][S3][S4].  The notes' 2% p.a. take-up among eligible contracts is a
    cohort-splitting construction and is **not implemented**; the exercise is named
    deterministically on the model point and is off by default.  Read as ``Data``
    checked it, blank or a whole number of months at or after the income start month, and
    compared with ``duration_mth(t)``.
    Read from ``Data.accel_mth``, which holds the blank as -1; a month of
    ``2**53`` or more in size is refused here, naming the point.
    """
    if data.accel_mth_ok()[idx] == 0:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: accel_mth must be blank or below "
                         f"2**53 months in size; it is not")
    return int(data.accel_mth()[idx])                                # noqa: F821


def commute_mth():
    """t_c: the policy month a commutation is exercised; -1 if never (extended case only).

    Offered by one of the four composite sources [S4][S5] and prohibited on a QLAC after
    the required beginning date [R1 (q)(1)(iv)].  The notes' 1.5% p.a. take-up is not
    implemented, for the same reason as the other two options.  Read as ``Data`` checked
    it, blank or a whole number of months at or after the income start month, and compared
    with ``duration_mth(t)``.
    Read from ``Data.commute_mth``, which holds the blank as -1; a month of
    ``2**53`` or more in size is refused here, naming the point.
    """
    if data.commute_mth_ok()[idx] == 0:                         # noqa: F821
        raise ValueError(f"point_id {point_id()}: commute_mth must be blank or below "
                         f"2**53 months in size; it is not")
    return int(data.commute_mth()[idx])                              # noqa: F821


def commute_frac():
    """The fraction of the remaining guaranteed payments commuted; up to 100% [S4][R13].

    Read from ``Data.commute_frac``, which holds a blank as 0.0, none.
    """
    return float(data.commute_frac()[idx])                           # noqa: F821


def mort_rate_base_at(x, life):
    """The base-table annual mortality rate at attained age ``x``, for ``life``'s sex.

    The one cell that reads ``mort_table.csv``, keyed by age and life, so that the rate
    cells call it rather than join the table themselves.  The sex is the join key:
    :func:`mort_schedule` gives ``life``'s row of ``Data.mort_table_array``, and the age is
    its column, and the label accessor itself is left to reporting.  Called only below the
    limiting age: :func:`mort_rate_py` and :func:`mort_rate_base` return 1 at and above it
    without calling here.  The schedule asks ``Data.mort_table_count`` first, through
    ``Data.mort_sexes``, which checks the table's keys and rates, so that a projection
    meets the checks before it reads a rate: a blank rate would otherwise reach the cap on
    mortality as a missing value.  The age is checked against the row's first and last
    ages, ``Data.mort_age_first`` and ``Data.mort_age_last``, before the array is read, so
    an age the table lacks, below its first age, 20 as shipped, or any age on a sex the
    table lacks, whose row 0 holds none, is refused, naming the point, the age and the
    life, where ``DIA_US_S``'s ``.loc`` raised ``KeyError``, and the padding is never read.
    """
    s = mort_schedule(life)
    if x < data.mort_age_first()[s] or x > data.mort_age_last()[s]:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: mort_table.csv has no mort_rate at "
                         f"attained age {x} for the sex of life {life}")
    return float(data.mort_table_array()[s, x])                      # noqa: F821


def improvement_rate_at(x, life):
    """The generational improvement rate at attained age ``x``, for ``life``'s sex.

    The one cell that reads ``improvement_scale.csv``, keyed by age and life and joined on
    the sex as :func:`mort_rate_base_at` joins the mortality table, through
    :func:`improvement_schedule`, the scale's own numbering of its sexes, and checked and
    refused as it is.  Called only below the limiting age.
    """
    s = improvement_schedule(life)
    if (x < data.improvement_age_first()[s]                          # noqa: F821
            or x > data.improvement_age_last()[s]):                  # noqa: F821
        raise ValueError(f"point_id {point_id()}: improvement_scale.csv has no "
                         f"improvement_rate at attained age {x} for the sex of life "
                         f"{life}")
    return float(data.improvement_array()[s, x])                     # noqa: F821


def mort_schedule(life):
    """The number of ``life``'s sex in the mortality table: its row of
    ``Data.mort_table_array``.

    ``Data.mort_schedule_1`` for the primary (life = 1) and ``Data.mort_schedule_2`` for
    the joint annuitant (life = 2), 0 where the table lacks the sex, which
    :func:`mort_rate_base_at` refuses; any other life raises.  A cell of its own, so that
    the reader indexes the table by a cell's value, never by a ``Data`` array's.
    """
    if life == 1:
        return int(data.mort_schedule_1()[idx])                      # noqa: F821
    if life == 2:
        return int(data.mort_schedule_2()[idx])                      # noqa: F821
    raise ValueError("invalid life")


def improvement_schedule(life):
    """The number of ``life``'s sex in the improvement scale: its row of
    ``Data.improvement_array``.

    As :func:`mort_schedule`, on the scale's own numbering of its sexes, which need not be
    the mortality table's.
    """
    if life == 1:
        return int(data.improvement_schedule_1()[idx])               # noqa: F821
    if life == 2:
        return int(data.improvement_schedule_2()[idx])               # noqa: F821
    raise ValueError("invalid life")


def mort_rate_base(t, life):
    """The base-table annual mortality rate for ``life`` in the year containing month t.

    The shipped table is an illustrative **[std]** annuitant table, *not* the 2012 IAM
    Basic table the notes prescribe: licensed tables may not be embedded, and the Basic
    table is in any case printed in no source this library holds - A-821 prints the
    loaded Period Table only [REG-R153].  Its rates over ages 60-84 are band-constant
    values that reproduce the notes' five-year survival anchors exactly.  Rates at and
    above the limiting age are 1, and the table is read below it, at the attained age
    :func:`age` gives, through :func:`mort_rate_base_at`.  Zero outside the frame, where
    the contract has no attained age to look up.  The rate the projection applies is built
    by :func:`mort_rate_py`, which reads the same table at the same age.
    """
    if not is_active(t):
        return 0.0
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return mort_rate_base_at(x, life)


def improvement_rate(t, life):
    """G2_x: the generational improvement rate for ``life`` in the year containing t.

    The shipped scale is an illustrative **[std]** stand-in for Projection Scale G2 and
    is read only on the generational basis.  Scaling it is the notes' first listed
    sensitivity: Scale G2 is fixed and dated, and the 2020-2024 payout experience study
    says it has over-projected improvement [R15][REG-R61].  Zero at and above the limiting
    age, and outside the frame; read below it through :func:`improvement_rate_at`.
    """
    if not is_active(t):
        return 0.0
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 0.0
    return improvement_rate_at(x, life)


def mort_rate_py(y, life):
    """The annual mortality rate of ``life`` in policy year y: the one place it is built.

    On the *generational* basis the notes' construction
    ``q_x^(2012+k) = q_x^(2012) * (1 - G2_x)^k`` [R9][REG-R59], with ``k`` the calendar year
    of policy year ``y``, ``issue_year() + y - 1``, less ``mort_table_year``, so each
    attained age in each future calendar year uses its own improved rate.  On the *anchor*
    basis the table is used unprojected, which is what the worked example's survival curve
    is.  The attained age is ``age_at_entry(life) + y - 1``, the rate 1 and the
    improvement 0 at and above the limiting age, and the tables are read below it through
    :func:`mort_rate_base_at` and :func:`improvement_rate_at`.  ``mort_ae_factor`` is the
    experience A/E overlay, **[std]** at 1.00 - the notes set the deferral-phase A/E at
    1.00 and give no number for the payout phase, the 2020-2024 study being cited without a
    factor [R15][REG-R61].

    Keyed by policy year, so that the projection's :func:`mort_rate`, at the policy year of
    month t, and the pricing kernel's :func:`mort_rate_mth_py`, at any policy year from
    issue, read one rate.  The rate is capped at 1 as ``DIA_US_S`` caps it, the bound
    second, ``min(mort_ae_factor * q, 1.0)``, so that a missing input, a NaN, stays NaN,
    where ``min(1.0, q)`` would read it as 1, certain death with every flow finite.
    """
    x = age_at_entry(life) + y - 1
    q = 1.0 if x >= omega_age else mort_rate_base_at(x, life)        # noqa: F821
    if is_generational():
        k = issue_year() + y - 1 - mort_table_year                   # noqa: F821
        imp = 0.0 if x >= omega_age else improvement_rate_at(x, life)  # noqa: F821
        q = q * (1.0 - imp) ** k
    return min(mort_ae_factor * q, 1.0)                              # noqa: F821


def mort_rate_mth_py(y, life):
    """The monthly death probability in policy year y: ``1 - (1 - q_annual)^(1/12)``.

    :func:`mort_rate_py` turned monthly, as :func:`mort_rate_mth` turns :func:`mort_rate`,
    so the two give one float in the same policy year.  The pricing kernel's rate, keyed
    by policy year, which :func:`lives_if_pm` and :func:`annuity_factor` read at the
    policy year of each month from issue.
    """
    return 1.0 - (1.0 - mort_rate_py(y, life)) ** (1.0 / 12.0)


def mort_rate(t, life):
    """The annual mortality rate applied to ``life`` in the year containing month t.

    :func:`mort_rate_py` at the policy year of month ``t``, on the policy clock, so the
    projection's survival and the pricing kernel's read one rate: on the generational
    basis, improved to the calendar year the contract reaches, and capped at 1.  Zero
    outside the frame, before any rate is read.
    """
    if not is_active(t):
        return 0.0
    return mort_rate_py(policy_year(t), life)


def mort_rate_mth(t, life):
    """q(t) = 1 - (1 - q_annual)^(1/12): the probability of death during month t **[std]**.

    Month ``t`` on the valuation clock, the projection's rate; 0 outside the frame.
    """
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def lives_if_init(life):
    """l_i at the valuation date: the probability that ``life`` is alive then.

    The ``lives_if_init_1`` (primary, life = 1) or ``lives_if_init_2`` (joint annuitant,
    life = 2) column, as the contract stands at the start of month 0, before any month-0
    death: the opening value of :func:`lives_if` at :func:`t_entry`.  On a real record it
    is 1 or 0, so a joint contract may carry one life already dead; on a point restated
    from ``DIA_US_S`` at its month ``d`` it is ``DIA_US_S``'s ``lives_if(d, life)``, a
    probability.  The lives are independent, as in ``DIA_US_S``, so the two per-life
    probabilities are the whole survival state.  A contract not yet in force carries its
    values at issue, 1 for each covered life, and ``lives_if_init_2`` is 0 on a
    single-life contract; ``Data`` checks both.  Read from ``Data.lives_if_init_1`` and
    ``Data.lives_if_init_2``.
    """
    if life == 1:
        return float(data.lives_if_init_1()[idx])                    # noqa: F821
    if life == 2:
        return float(data.lives_if_init_2()[idx])                    # noqa: F821
    raise ValueError("invalid life")


def lives_if(t, life):
    """l(t): the probability that ``life`` is alive **at time t**, as projected.

    Indexed by a **time point** on the valuation clock, not by a period: time ``t`` is the
    start of month ``t``, so month t opens at time ``t`` and closes at time ``t + 1``, and
    time 0 is the valuation date.  :mod:`.SPIA_US_S` writes the same cells with the
    argument named ``k``; here it is the valuation clock's ``t``.

    At :func:`t_entry`, the first time point on the books, it is the opening state,
    :func:`lives_if_init`: the life's status at the valuation date for a contract in force,
    and 1, its value at issue, for one issued at or after it.  Before that it is 0: the
    contract is not yet on the books.  After it ``l(t) = l(t-1) * (1 - q(t-1))``, equation
    (9) - the only decrement in the product, at the rate of month ``t - 1``, the month that
    has just closed.  There is no lapse and no annuitization decrement: VM-22's
    standard-projection lapse section is "not applicable" to contracts with no account
    value or surrender benefit, and annuitization is prescribed at 0% [R9].

    The projection's survival only: the pricing kernel prices each premium on its own
    survival curve from issue, :func:`lives_if_pm`.  Returns 0 for ``life = 2`` on a
    single-life contract.
    """
    if life == 2 and not is_joint():
        return 0.0
    if t < t_entry():
        return 0.0
    if t == t_entry():
        return lives_if_init(life)
    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t - 1, life))


def lives_if_pm(k, life):
    """The pricing survival: the probability that ``life`` survives from issue to time k.

    Indexed by a **time point** on the policy clock, ``k`` months after issue, ``l(0) =
    1``.  One explicit loop from issue over the monthly rates of each policy year,
    :func:`mort_rate_mth_py`: ``DIA_US_S``'s ``lives_if`` recursion unrolled, the same
    products in the same order, so it is ``DIA_US_S``'s ``lives_if(k, life)`` to the last
    bit.  The pricing kernel reads it at the premium months, the income start months, the
    five-year bands of the ROP factor and the exercise months, and :func:`annuity_factor`
    carries the product on from there to the horizon, so pricing is anchored at issue and
    at the premium dates, deterministic from the contract's terms and the mortality basis
    the model is read with, whatever the valuation date, and never reads the projection or
    its opening state.  Returns 0 for ``life = 2`` on a single-life contract.
    """
    if life == 2 and not is_joint():
        return 0.0
    surv = 1.0
    for j in range(k):
        surv = surv * (1.0 - mort_rate_mth_py(j // 12 + 1, life))
    return surv


def lives_if_last_pm(k):
    """l_last on the pricing curve: the probability that a covered life survives to time k.

    ``l_1 + l_2 - l_1*l_2`` on :func:`lives_if_pm`, under joint-life independence, and
    ``l_1`` on a single-life contract: ``DIA_US_S``'s ``lives_if_last(k)`` from issue,
    which the ROP factor's exposure reads.
    """
    l1 = lives_if_pm(k, 1)
    if not is_joint():
        return l1
    l2 = lives_if_pm(k, 2)
    return l1 + l2 - l1 * l2


def lives_death(t, life):
    """d(t) = l(t) - l(t+1): the deaths of ``life`` **during** month t.

    Note the index.  Month ``t`` spans time ``t`` to time ``t + 1``, so the density is a
    forward difference: the deaths of month ``t`` are taken at its end, between the
    survival at its start and the survival at the start of ``t + 1``.  Zero outside the
    frame.
    """
    if not is_active(t):
        return 0.0
    return lives_if(t, life) - lives_if(t + 1, life)


def lives_if_last(t):
    """l_last(t): the probability at least one covered life is alive at time t.

    ``l_1 + l_2 - l_1*l_2`` on a joint contract, under **joint-life independence
    [std]**; ``l_1`` on a single-life contract, which is why no separate ``l_alive``
    cells is needed.  Indexed by a time point on the valuation clock, like
    :func:`lives_if`, and 0 before the contract is on the books.
    """
    l1 = lives_if(t, 1)
    if not is_joint():
        return l1
    l2 = lives_if(t, 2)
    return l1 + l2 - l1 * l2


def lives_death_last(t):
    """d_last(t) = l_last(t) - l_last(t+1): the last-death density in month t.

    Also the death that terminates the income stream and triggers the refund, and - on
    a joint contract, where the first death leaves the contract running on the option
    chosen at issue [S2] - the death that triggers the deferral death benefit.  Zero
    outside the frame.
    """
    if not is_active(t):
        return 0.0
    return lives_if_last(t) - lives_if_last(t + 1)


def pols_if(t):
    """Contracts in force at the start of month t: the count on the books times l_last(t).

    The contracts on the books weighted by the probability that a covered life is alive
    at the start of month ``t``, ``DIA_US_S``'s ``pols_if_init * l_last(t)`` on the count
    on the books.  The notes weight the maintenance expense by ``l(t)`` alone.  The payout
    chassis instead uses ``max(C(t), l_alive(t))``, so that a certain-period obligation
    running on after the last death still carries expense; the two notes files differ here
    and this model follows its own.  They coincide on every form without a certain floor,
    the anchor cell included.

    It is not the count that weights row ``t``, ``pols_if_at(t, BEF_DECR)``, which
    mortality never moves: on point 20, the period-certain point in force 300 months,
    ``pols_if(0)`` is 0.5577 against a count of 1.0.  The registry marks the model
    ``survival_pols_if`` for that reason.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_DECR) * lives_if_last(t)


def pols_if_at(t, timing):
    """Contracts on the books at time t, at the instant ``timing`` names.

    ``BEF_NB``
        The contracts carried in from month t - 1, before month t's new business: at
        :func:`t_entry`, the first month on the books, :func:`pols_if_init`, the count in
        force at the valuation date (0 for a point issued at or after it), and the whole
        ``policy_count()`` after it.  Zero outside the frame, so the contracts leave the
        books at the stop rule, at the end of the last projected month.
    ``BEF_DECR``
        ``BEF_NB`` plus :func:`pols_new_biz`: the count that weights every cash flow
        of month t.

    These are ``basiclife.BasicTerm_SE``'s names, int codes here (the Space docstring's
    *Codes*), and any other timing raises.  The count
    is not decremented: mortality decrements each life's survival, :func:`lives_if`, and
    every cash flow is this count times a per-contract amount weighted by survival, as
    ``DIA_US_S`` weights its flows by the constant ``pols_if_init``.  A count weighted by
    survival could not carry the two lives' independent probabilities.  So ``BEF_NB`` is
    a closed form, the same float that the recursion ``BEF_NB(t-1) + pols_new_biz(t-1)``
    gives, with no chain of calls back to :func:`t_entry`.  :func:`pols_if` is not
    ``BEF_DECR``: it is this count weighted by survival.
    """
    if timing == BEF_NB:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return policy_count()
    elif timing == BEF_DECR:
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)
    else:
        raise ValueError("invalid timing")


def pols_new_biz(t):
    """Contracts issued in month t: ``policy_count()`` in the issue month.

    The month with ``duration_mth(t) == 0``: ``t = 0`` for a point issued at the valuation
    date, ``t = k`` for one issued ``k`` months later.  A contract already in force at the
    valuation date has none.  New business in ``basiclife.BasicTerm_SE``'s sense, a
    contract entering the books, which brings its premium schedule and no acquisition
    cost: ``DIA_US_S`` carries none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pricing_disc_factor(yrs):
    """v^yrs on the pricing interest rate i_p **[std]**.

    Contractual, not a valuation discount: this is the kernel that turns a premium into
    guaranteed income.  No DIA source discloses a pricing rate - the Compact relieves
    the insurer of disclosing the deferral-period basis altogether [R13 SS1.B(1)(a)] -
    so 4.75% is a modeling assumption, readable as a long-duration general-account
    portfolio yield net of default costs.  An engine cell of float parameter, kept as
    ``DIA_US_S``'s for its tests and the twin identity, which no other cell calls: its
    three callers in ``DIA_US_S``, :func:`rop_factor_calc`, :func:`annuity_factor_def` and
    :func:`accel_cost`, write ``(1.0 + pricing_rate) ** (-yrs)`` inline, the same
    operation on the same float.
    """
    return (1.0 + pricing_rate) ** (-yrs)                            # noqa: F821


def deferral_yrs(k):
    """d_k = (T - k)/12: the remaining deferral in years of a premium in policy month k.

    Keyed by the premium's policy month, ``DIA_US_S``'s ``t`` renamed.
    """
    return (income_start_mth_at(k) - k) / 12.0


def surv_to_income_start(k):
    """_d p_x(k): the primary life's survival from policy month k to the income start month.

    A ratio on the pricing survival curve anchored at issue, :func:`lives_if_pm`, which is
    how the notes derive ``_15p_65 = _20p_60 / _5p_60 = 0.715000/0.975000 = 0.733333``.
    Keyed by the premium's policy month, ``DIA_US_S``'s ``t`` renamed.
    """
    base = lives_if_pm(k, 1)
    if base <= 0.0:
        return 0.0
    return lives_if_pm(income_start_mth_at(k), 1) / base


def annuity_factor(start_mth, guar_mths, int_rate, from_mth):
    """The APV at policy month ``from_mth`` of $1 per annum of income from ``start_mth``.

    Equation (2) generalized.  The k-th instalment is certain while ``k * 12/m`` does not
    exceed ``guar_mths`` and life-contingent after that, the payment factor being the
    same ``max(C, L)`` the projection uses, with the survival probabilities taken
    **conditional on being alive at** ``from_mth``::

        a = sum over k of (1/m) * v^((s_k - from_mth)/12) * max(C_k, L_k)

    Called with ``from_mth = start_mth`` it is ``a^(m)_y(f; i)``, the payout factor at
    the income start age; called with ``from_mth = k``, a premium's month, it is
    ``a_def(x(k), d, f; i)`` directly, which is what makes the joint forms work.  Equation
    (15)'s expansion ``a_def^(both) + s * sum_i a_def^(only i)`` is algebraically this sum
    with the *either* trigger, so no separate joint kernel is needed.  The convertible
    variant, equation (16), is **not implemented**; the base is non-convertible **[std]**.

    The certain instalments are weighted by the probability that the income phase is
    reached at all - see :func:`surv_to_payout`.  Without that weight the deferred
    factor would treat a guarantee period as payable to an annuitant who died in the
    deferral, and equation (1)'s ``v^d * _d p_x * a^(m)`` would not be recovered.

    Every month is a **policy month**, and every survival probability is the pricing
    curve's, :func:`lives_if_pm`, from issue: ``DIA_US_S``'s own sum, read at the same
    months.  The survival at each payment point is carried forward month by month from
    ``lives_if_pm(start_mth)``, in one pass, at the rates of :func:`mort_rate_mth_py`,
    the same products in the same order as ``DIA_US_S``'s recursion, so the factor is
    ``DIA_US_S``'s to the last bit, with no recursion through the projection.

    **The sum is bounded by** ``horizon_mths()``, **not by the frame.**  ``horizon_mths()``
    is the policy month the youngest covered life attains ``omega_age``, which is **one
    past** the last projected month on a contract issued at the valuation date - on the
    anchor cell the frame ends at policy month 719 and the last instalment admitted here
    falls at month 720.  That is deliberate: this is a pricing kernel and must be bounded
    by the mortality horizon, which is age-driven, rather than by ``proj_len()``, which the
    pricing feeds.  Do not "tidy" ``last`` to the frame's end; it would move golden
    values.  A pricing engine with a float rate and guarantee, kept as ``DIA_US_S``'s cell
    for its tests and the twin identity, which no other cell calls:
    :func:`annuity_factor_at` holds its body for the three argument sets
    ``DIA_US_S``'s callers pass with the final guarantee period, and
    :func:`guarantee_mths_pricing` the same body inline, where the period changes each
    iteration.
    """
    v = 1.0 / (1.0 + int_rate)
    m = payment_freq()
    step = 12 // m
    adv = not is_arrears()
    l1f = lives_if_pm(from_mth, 1)
    if l1f <= 0.0:
        return 0.0
    jt = is_joint()
    l2f = lives_if_pm(from_mth, 2) if jt else 1.0
    dlt = survivor_pct()
    either = is_trigger_either()
    q1 = lives_if_pm(start_mth, 1) / l1f
    if jt and l2f > 0.0:
        q2 = lives_if_pm(start_mth, 2) / l2f
        p_start = q1 + q2 - q1 * q2
    else:
        p_start = q1
    last = horizon_mths()
    l1 = lives_if_pm(start_mth, 1)
    l2 = lives_if_pm(start_mth, 2) if jt else 0.0
    j = start_mth
    total = 0.0
    k = 1
    while True:
        off = (k - 1) * step if adv else k * step
        s = start_mth + off
        if s > last:
            break
        while j < s:
            y = j // 12 + 1
            l1 = l1 * (1.0 - mort_rate_mth_py(y, 1))
            if jt:
                l2 = l2 * (1.0 - mort_rate_mth_py(y, 2))
            j += 1
        cert = p_start if k * step <= guar_mths else 0.0
        p1 = l1 / l1f
        if jt and l2f > 0.0:
            p2 = l2 / l2f
            if either:
                lf = p1 * p2 + dlt * (p1 + p2 - 2.0 * p1 * p2)
            else:
                lf = p1 + dlt * (1.0 - p1) * p2
        else:
            lf = p1
        total += (1.0 / m) * v ** ((s - from_mth) / 12.0) * max(cert, lf)
        k += 1
    return total


def annuity_factor_at(k, basis):
    """:func:`annuity_factor` from policy month ``k``, on the arguments ``basis`` names.

    ``DIA_US_S`` calls :func:`annuity_factor` with the final guarantee period
    :func:`guarantee_mths_pricing` on three sets of arguments, and this is the factor on
    each, keyed by the month it is valued from and an int code for the rest (the Space
    docstring's *Codes*):

    ``PURCHASE``
        a premium's: from the income start month it is priced to,
        :func:`income_start_mth_at`, at the pricing rate ``i_p``, valued at its month ``k``,
        :func:`annuity_factor_def`'s call; and :func:`payout_factor_calc`'s at ``k = T``,
        where :func:`income_start_mth_at` is ``T`` on every point ``Data`` admits, an
        adjustment preceding the old month and the new one following it.
    ``ADJUST_OLD``, ``ADJUST_NEW``
        a start-date adjustment's two factors, at the repricing rate ``i_e``, valued at the
        exercise month ``k``, from the old income start month and from the new one,
        :func:`adjust_income_factor`'s calls.

    Any other code raises.  The arguments are read in ``DIA_US_S``'s order, and the body is
    :func:`annuity_factor`'s, the same operations on the same floats in the same order, so
    the factor is ``DIA_US_S``'s to the last bit: a cell keyed by C integers, where
    :func:`annuity_factor` takes a float rate and a float guarantee period, which compile
    with a Python dict for a cache (R14).
    """
    if basis == PURCHASE:                                            # noqa: F821
        start = income_start_mth_at(k)
        guar = guarantee_mths_pricing()
        rate = pricing_rate                                          # noqa: F821
    elif basis == ADJUST_OLD:                                        # noqa: F821
        rate = repricing_rate()
        guar = guarantee_mths_pricing()
        start = income_start_mth_init()
    elif basis == ADJUST_NEW:                                        # noqa: F821
        rate = repricing_rate()
        guar = guarantee_mths_pricing()
        start = adjust_start_mth()
    else:
        raise ValueError("invalid basis")
    v = 1.0 / (1.0 + rate)
    m = payment_freq()
    step = 12 // m
    adv = not is_arrears()
    l1f = lives_if_pm(k, 1)
    if l1f <= 0.0:
        return 0.0
    jt = is_joint()
    l2f = lives_if_pm(k, 2) if jt else 1.0
    dlt = survivor_pct()
    either = is_trigger_either()
    q1 = lives_if_pm(start, 1) / l1f
    if jt and l2f > 0.0:
        q2 = lives_if_pm(start, 2) / l2f
        p_start = q1 + q2 - q1 * q2
    else:
        p_start = q1
    horizon = horizon_mths()
    l1 = lives_if_pm(start, 1)
    l2 = lives_if_pm(start, 2) if jt else 0.0
    j = start
    total = 0.0
    pay = 1
    while True:
        off = (pay - 1) * step if adv else pay * step
        s = start + off
        if s > horizon:
            break
        while j < s:
            y = j // 12 + 1
            l1 = l1 * (1.0 - mort_rate_mth_py(y, 1))
            if jt:
                l2 = l2 * (1.0 - mort_rate_mth_py(y, 2))
            j += 1
        cert = p_start if pay * step <= guar else 0.0
        p1 = l1 / l1f
        if jt and l2f > 0.0:
            p2 = l2 / l2f
            if either:
                lf = p1 * p2 + dlt * (p1 + p2 - 2.0 * p1 * p2)
            else:
                lf = p1 + dlt * (1.0 - p1) * p2
        else:
            lf = p1
        total += (1.0 / m) * v ** ((s - k) / 12.0) * max(cert, lf)
        pay += 1
    return total


def guarantee_mths_pricing_init():
    """n_g as the kernel prices with it, carried in force: the column of that name.

    On a cash or installment refund in force at the valuation date, ``DIA_US_S``'s
    ``guarantee_mths_pricing()``, the guarantee period in months with which every slice of
    the contract is priced: a fixed point over the **whole** premium schedule, the slices
    already bought included.  The premium schedule holds only the premiums still due, and
    the fixed point depends on the path of its iterations, so neither the schedule nor the
    premiums paid and the income bought can recover it: it is opening state, a quantity
    fixed at issue and not re-derivable from static data.  It prices a premium still due
    and a start-date adjustment still to come, and :func:`payout_factor_calc` reports it.
    ``Data`` requires it on every refund form in force, a rule a contract record meets
    without the schedule, though on one with nothing left to price, in payout say, only
    :func:`payout_factor_calc` reads it; it is blank, and unread, on every other point.
    Read from ``Data.guarantee_mths_pricing_init``.
    """
    return float(data.guarantee_mths_pricing_init()[idx])            # noqa: F821


def guarantee_mths_pricing():
    """n_g in months as fed into the pricing kernel, equation (5).

    ``n_g = CP(T) / B`` puts ``B`` on both sides, and the notes' listed pitfall is
    "failing to iterate leaves a systematic bias in the derived guarantee period and
    hence in the income".  Resolved here by fixed-point iteration from a life-only
    start, the notes' own prescription ("three iterations from a life-only start are
    ample") - ``pricing_iters`` carries the count.  The equation (5) approximation is
    used for **both** refund forms **[std]**; the exact cash-refund factor of equation
    (6) is not implemented.

    The elected period on a period-certain form and 0 on a life-only form, as in
    ``DIA_US_S``.  On a refund form the fixed point runs over the premium schedule, which
    on a point issued at or after the valuation date is the whole schedule, so it is
    ``DIA_US_S``'s to the last bit; on a contract in force the schedule holds only the
    premiums still due, and the value is the opening state,
    :func:`guarantee_mths_pricing_init`.

    ``DIA_US_S`` sums and iterates its ``premium_by_mth()`` dict; here the premium months
    are those of the point's row of ``Data.premium_rows`` with a row, in ascending order,
    the dict's keys in its order, a month with a premium of 0.0 among them, whose ROP
    factor is read as ``DIA_US_S`` reads it, and each premium is :func:`premium_pm`, the
    dict's value.  ``CP`` is Python's ``sum`` of the premiums written out, the compensated
    sum CPython 3.12 and later take of floats, so that it is ``DIA_US_S``'s float to the
    last bit where a running sum is not.  And each iteration's annuity factor is
    :func:`annuity_factor`'s body at the iteration's guarantee period, inline, since the
    period changes each iteration: where the premium's life 1 has died by its month, the
    factor is 0, as :func:`annuity_factor` returns, and the premium is skipped, as
    ``DIA_US_S`` skips it, the loops going on.
    """
    if is_period_certain():
        return float(12 * certain_period())
    if is_life_only():
        return 0.0
    if duration_mth_init() > 0:
        return guarantee_mths_pricing_init()
    prem_last = data.premium_last()[idx]                             # noqa: F821
    cp = 0.0
    comp = 0.0
    for tk in range(prem_last + 1):
        if data.premium_rows()[idx, tk] > 0:                         # noqa: F821
            x = premium_pm(tk)
            added = cp + x
            if abs(cp) >= abs(x):
                comp = comp + ((cp - added) + x)
            else:
                comp = comp + ((x - added) + cp)
            cp = added
    if comp != 0.0 and abs(comp) <= 1.7976931348623157e308:
        cp = cp + comp
    n = 0.0
    for _ in range(pricing_iters):                                   # noqa: F821
        inc = 0.0
        for tk in range(prem_last + 1):
            if data.premium_rows()[idx, tk] == 0:                    # noqa: F821
                continue
            pk = premium_pm(tk)
            start = income_start_mth_at(tk)
            v = 1.0 / (1.0 + pricing_rate)                           # noqa: F821
            m = payment_freq()
            step = 12 // m
            adv = not is_arrears()
            a = 0.0
            l1f = lives_if_pm(tk, 1)
            if not l1f <= 0.0:
                jt = is_joint()
                l2f = lives_if_pm(tk, 2) if jt else 1.0
                dlt = survivor_pct()
                either = is_trigger_either()
                q1 = lives_if_pm(start, 1) / l1f
                if jt and l2f > 0.0:
                    q2 = lives_if_pm(start, 2) / l2f
                    p_start = q1 + q2 - q1 * q2
                else:
                    p_start = q1
                horizon = horizon_mths()
                l1 = lives_if_pm(start, 1)
                l2 = lives_if_pm(start, 2) if jt else 0.0
                j = start
                pay = 1
                while True:
                    off = (pay - 1) * step if adv else pay * step
                    s = start + off
                    if s > horizon:
                        break
                    while j < s:
                        y = j // 12 + 1
                        l1 = l1 * (1.0 - mort_rate_mth_py(y, 1))
                        if jt:
                            l2 = l2 * (1.0 - mort_rate_mth_py(y, 2))
                        j += 1
                    cert = p_start if pay * step <= n else 0.0
                    p1 = l1 / l1f
                    if jt and l2f > 0.0:
                        p2 = l2 / l2f
                        if either:
                            lf = p1 * p2 + dlt * (p1 + p2 - 2.0 * p1 * p2)
                        else:
                            lf = p1 + dlt * (1.0 - p1) * p2
                    else:
                        lf = p1
                    a += (1.0 / m) * v ** ((s - tk) / 12.0) * max(cert, lf)
                    pay += 1
            if a > 0.0:
                inc += pk * ((1.0 - expense_load) - rop_factor(tk)) / a  # noqa: F821
        if inc <= 0.0:
            return 0.0
        n = 12.0 * cp / inc
    return n


def payout_factor_calc():
    """a^(m) at the income start age computed from the shipped table, equation (2).

    ``DIA_US_S``'s ``annuity_factor(T, guarantee_mths_pricing(), pricing_rate, T)``, which
    is :func:`annuity_factor_at` at ``T`` on its ``PURCHASE`` basis.
    """
    return annuity_factor_at(income_start_mth(), PURCHASE)          # noqa: F821


def payout_factor():
    """a^(m)_{x+d}(f; i_p): the payout annuity factor in force.

    On the *table* basis the notes' illustrative value - 8.60 for the anchor cell's
    ``a^(12)_80(cash refund, female; 4.75%)`` - read from *payout_factor_table.csv*
    **[std]**; on the *formula* basis :func:`payout_factor_calc`.  No insurer publishes
    payout factors for this product and the Compact does not require the basis to be
    disclosed at all [R13 SS1.B(1)(a)].  The table's key is the primary life's age at the
    income start month, ``age_at_entry(1) + T // 12`` on the policy clock, its sex, read
    from the model point's ``sex`` column as the join key, and the payout stream, from the
    form decodes, as :func:`payout_form` names it.  The join asks
    ``data.payout_factor_count()`` first, which checks the table's keys and factors, so that
    a projection meets the checks before it reads a factor.

    The table is ``Data``'s row vectors, the sex numbered by the table's own sexes,
    ``Data.payout_schedule``, and the form as ``Data.payout_form_code`` numbers it, LO 1,
    CR 2, IR 3 and PC 4; the join scans the rows for the key, the first match its only
    one, since the count cell refuses a key on two rows.  A key no row holds, a sex the
    table lacks among them, is refused, naming the point and the key, where
    ``DIA_US_S``'s ``.loc`` raised ``KeyError``.
    """
    if is_formula_basis():
        return payout_factor_calc()
    if is_life_only():
        form = 1
    elif is_cash_refund():
        form = 2
    elif is_installment_refund():
        form = 3
    else:
        form = 4
    x = age_at_entry(1) + income_start_mth() // 12
    rows = data.payout_factor_count()                                # noqa: F821
    for i in range(rows):
        if (data.payout_income_start_age()[i] == x                   # noqa: F821
                and data.payout_sex()[i] == data.payout_schedule()[idx]  # noqa: F821
                and data.payout_form_code()[i] == form):             # noqa: F821
            return float(data.payout_factor_value()[i])              # noqa: F821
    raise ValueError(f"point_id {point_id()}: payout_factor_table.csv has no payout_factor "
                     f"at income_start_age {x} for the point's sex and payout form")


def rop_factor_calc(k):
    """A_rop for a premium paid in policy month k, by the notes' mid-band approximation.

    Equation (3) is a monthly sum; the notes state their illustrative factors were
    "computed from the same survival anchors with a mid-band death-timing
    approximation", which is what this implements: deaths in each five-year band of the
    deferral, discounted from the midpoint of the band.  Zero when the contract carries
    no deferral death benefit, which is the ``1{db_form = ROP}`` indicator of (4).

    **The exposure is the last-death curve** ``l_last``, not the primary life's.
    Equation (3) is written on a single life ``x`` and the notes never restate it for a
    joint contract, but the benefit this factor has to pay for is the one
    :func:`claims` projects, and on a joint contract that attaches to the **last** death
    - "if one annuitant dies in deferral the contract continues on the option chosen at
    issue" [S2], so the return of premium falls due only when the contract ends.
    Pricing the primary life's death density instead would charge for an exposure 2.5
    times the one projected (0.161605 against 0.064105 on the joint model point) and
    understate the income the premium buys by about 12.5% - the notes' own listed
    pitfall that the deferral death benefit's cost "belongs in the purchase rate (4)
    *and* in the projected cash flows", read as requiring the *same* benefit in both.
    On a single-life contract ``l_last`` **is** the primary curve, so this changes
    nothing on the worked example.  On the pricing curve, :func:`lives_if_last_pm`, from
    issue; keyed by the premium's policy month, ``DIA_US_S``'s ``t`` renamed.  Each band is
    discounted as :func:`pricing_disc_factor` discounts, written inline.
    """
    if not is_rop():
        return 0.0
    end = income_start_mth_at(k)
    base = lives_if_last_pm(k)
    if base <= 0.0:
        return 0.0
    total = 0.0
    lo = k
    while lo < end:
        hi = min(lo + 60, end)
        s0 = lives_if_last_pm(lo) / base
        s1 = lives_if_last_pm(hi) / base
        mid = ((lo - k) + (hi - k)) / 24.0
        total += (s0 - s1) * (1.0 + pricing_rate) ** (-mid)          # noqa: F821
        lo = hi
    return total


def rop_factor(k):
    """A_rop(x(k), d; i_p): the return-of-premium factor of a premium in policy month k.

    On the *table* basis the notes' illustrative values from *rop_factor_table.csv*
    **[std]**; on the *formula* basis :func:`rop_factor_calc`.  The two disagree on the
    twenty-year slice - 0.157900 printed against 0.161605 computed - while agreeing to
    four decimals on the fifteen-year slice; both readings are shipped and a test pins
    the gap open.  See the Space docstring.  The table's key is the primary life's age
    at the premium, ``age_at_entry(1) + k // 12`` on the policy clock, its sex, read from
    the model point's ``sex`` column as the join key, and the deferral in whole years,
    :func:`rop_deferral_yrs`.  The join asks ``data.rop_factor_count()`` first, which
    checks the table's keys and factors, so that a projection meets the checks before it
    reads a factor.  It scans ``Data``'s row vectors as :func:`payout_factor` scans its
    table's, the sex numbered by the table's own sexes, ``Data.rop_schedule``, and a key no
    row holds is refused, naming the point and the key, where ``DIA_US_S``'s ``.loc``
    raised ``KeyError``.
    """
    if not is_rop():
        return 0.0
    if is_formula_basis():
        return rop_factor_calc(k)
    x = age_at_entry(1) + k // 12
    n = rop_deferral_yrs(k)
    rows = data.rop_factor_count()                                   # noqa: F821
    for i in range(rows):
        if (data.rop_issue_age()[i] == x                             # noqa: F821
                and data.rop_sex()[i] == data.rop_schedule()[idx]    # noqa: F821
                and data.rop_deferral_years()[i] == n):              # noqa: F821
            return float(data.rop_factor_value()[i])                 # noqa: F821
    raise ValueError(f"point_id {point_id()}: rop_factor_table.csv has no rop_factor at "
                     f"issue_age {x}, deferral_years {n} for the point's sex")


def rop_deferral_yrs(k):
    """The deferral of a premium in policy month k in whole years: the ROP table's key.

    ``DIA_US_S``'s ``int(round(deferral_yrs(k)))``, ``(T - k) / 12`` rounded half to even,
    computed on the integers: the months ``n = T - k`` are ``12q + r``, and the rounding
    is ``q`` below a half year, ``r < 6``, ``q + 1`` above it, and at a half year exactly,
    ``r = 6``, the even of the two.  Away from a half year the float ``n / 12.0`` is at
    least a month from it, so its rounding error cannot cross it, and at a half year it is
    ``q + 0.5`` exactly: so this is ``round``'s whole number at every ``k``, without a
    Python call in a compiled cell (R16).  ``//`` floors on a negative ``n`` as Python's
    does, compiled too.  Keyed by the premium's policy month.
    """
    n = income_start_mth_at(k) - k
    q = n // 12
    r = n - 12 * q
    if r < 6 or (r == 6 and q % 2 == 0):
        return q
    return q + 1


def annuity_factor_def(k):
    """a_def(x(k), d, f; i_p): the APV at policy month k of $1 p.a. from T, equation (1).

    On the *table* basis, equation (1) literally, ``v^d * _d p_x * a^(m)``.  That
    factorization is single-life only - a joint status does not separate into a deferral
    survival times a payout APV - so a joint model point must use the *formula* basis,
    where the whole deferred stream is valued in one pass by :func:`annuity_factor`, and
    ``Data`` refuses a joint point on the table basis, naming it.  Keyed by the premium's
    policy month, ``DIA_US_S``'s ``t`` renamed.  The discount is written as
    :func:`pricing_disc_factor` writes it, and each factor of the product is read in
    ``DIA_US_S``'s order before the product is taken, in its order; the formula basis is
    :func:`annuity_factor_at` on its ``PURCHASE`` basis.
    """
    if not is_formula_basis():
        if is_joint():
            raise ValueError("factor_basis 'table' is single-life only")
        disc = (1.0 + pricing_rate) ** (-deferral_yrs(k))            # noqa: F821
        surv = surv_to_income_start(k)
        return disc * surv * payout_factor()
    return annuity_factor_at(k, PURCHASE)                            # noqa: F821


def purchase_rate(k):
    """pr(x(k), d, f): annual income bought per $1 of premium in policy month k, eq (4).

    ``pr = [ (1 - L) - 1{ROP} * A_rop ] / a_def`` - the equivalence principle applied
    **per premium**, which is the core of the product: income is additive across slices,
    each priced at the annuitant's attained age and the remaining deferral **at its own
    payment date** [R13 SS3.B(1)(b)][S3].  Nothing accumulates and there is no balance to
    roll forward.  The whole kernel is **[std]**: no purchase-rate table was obtained
    and none is published.  ``purchase_rate_dp`` rounds the result, 6 on the worked
    example's model point; see the Space docstring.  Keyed by the premium's policy month,
    ``DIA_US_S``'s ``t`` renamed, so a premium still due at the valuation date is priced
    as ``DIA_US_S`` prices it.  The rounding stays, a call of Python's ``round`` in a
    compiled cell, which the registry's ``"python_calls"`` admits here alone: the rate is
    built from ``Projection``'s References, the pricing rate and the expense load, which
    ``Data`` cannot read, so it cannot be rounded there (R16).
    """
    a = annuity_factor_def(k)
    if a <= 0.0:
        return 0.0
    pr = ((1.0 - expense_load) - rop_factor(k)) / a                  # noqa: F821
    dp = purchase_rate_dp()
    return pr if dp < 0 else round(pr, dp)


def adjust_income_factor():
    """B'/B on a start-date adjustment, equation (11).

    Actuarial equivalence at the exercise month **[std]**::

        B' = B(t_e) * a_def(x(t_e), (T - t_e)/12, f; i_e)
                    / a_def(x(t_e), (T' - t_e)/12, f; i_e)

    ``a_def`` decreases in the deferral, so deferring the date raises the payment and
    advancing it lowers it, matching the extended case's statement [S4][S5].  Two
    refinements the disclosed recipe does not mention are **flagged rather than
    modeled**, as the notes require: the return-of-premium exposure changes with the
    deferral length, and ``CP`` is unchanged so the derived guarantee period shifts.
    Priced at the exercise's policy month on the pricing curve, so it is ``DIA_US_S``'s
    factor; a contract valued after the exercise carries the repriced income in
    ``annual_income_init``, and nothing reads the factor there.  The two factors are
    :func:`annuity_factor_at` at the exercise month on its ``ADJUST_OLD`` and
    ``ADJUST_NEW`` bases, ``DIA_US_S``'s two calls of :func:`annuity_factor`.
    """
    a = adjust_mth()
    if a < 0:
        return 1.0
    old = annuity_factor_at(a, ADJUST_OLD)                           # noqa: F821
    new = annuity_factor_at(a, ADJUST_NEW)                           # noqa: F821
    if new <= 0.0:
        return 1.0
    return old / new


def annual_income_init():
    """B at the valuation date: the guaranteed annual income per contract bought before it.

    The ``annual_income_init`` column, the income entering month 0, before COLA and before
    the slice, if any, bought at its start: ``DIA_US_S``'s ``annual_income(d - 1)`` on a
    point restated at its month ``d``, a start-date adjustment exercised before ``d``
    included.  The opening value of :func:`annual_income` at :func:`t_entry`; on a
    contract past its income start month it is the income ``B(T)``, level in payout.  0 at
    issue, and so on every point not yet in force, as ``Data`` checks.  Read from
    ``Data.annual_income_init``.
    """
    return float(data.annual_income_init()[idx])                     # noqa: F821


def annual_income(t):
    """B(t): the guaranteed annual income purchased to date, before COLA, equation (8).

    ``B(t) = B(t-1) + sum of P_k * pr(x(t_k), (T - t_k)/12, f)`` at the premiums of month
    ``t``, plus the repricing factor of equation (11) in the month a start-date adjustment
    is exercised.  The recursion opens at :func:`t_entry`, on the opening state,
    :func:`annual_income_init`, the income bought before the valuation date, which is 0 on
    a point issued at or after it.  ``B(t)`` is the income in force *during* month ``t``,
    including a slice bought at its start.  Income is **additive across slices** and each
    slice is fully guaranteed from the moment its premium is paid [R13 SS3.H(1)].  The
    exercise month and the purchase rate are read at the policy month of month ``t``.  Zero
    outside the frame.
    """
    if not is_active(t):
        return 0.0
    b = annual_income(t - 1) if t > t_entry() else annual_income_init()
    if duration_mth(t) == adjust_mth():
        b = b * adjust_income_factor()
    p = premium_pp(t)
    if p:
        b = b + p * purchase_rate(duration_mth(t))
    return b


def annual_income_payout():
    """B(T): the guaranteed annual income per contract at the income start month.

    ``annual_income_init()``, then one loop over the policy months from the valuation
    date's to the income start month ``T``, applying the repricing factor at the exercise
    month and adding each premium's slice at its purchase rate, the same operations in the
    same order as the recursion :func:`annual_income`, so ``B(T)`` is ``DIA_US_S``'s
    ``annual_income(T)`` to the last bit.  On a contract past its income start month the
    loop is empty and ``B(T)`` is the opening state.  The income is level from ``T`` on: no
    premium falls at or after it and a start-date adjustment precedes its new start month,
    as ``Data`` checks.  So this is the income of every instalment of the payout schedule,
    :func:`annuity_pp_sched_pm`, which the refund, the commuted value and the accelerated
    payments read at policy months ahead of ``t`` without reading :func:`annual_income`
    there.
    """
    b = annual_income_init()
    a = adjust_mth()
    for k in range(max(duration_mth_init(), 0), income_start_mth() + 1):
        if k == a:
            b = b * adjust_income_factor()
        p = premium_pm(k)
        if p:
            b = b + p * purchase_rate(k)
    return b


def guarantee_yrs():
    """n_g realized: the derived guarantee period in years, equation (5).

    ``CP(T) / B(T)`` on the refund forms - 150,000/44,259.65 = 3.3891 years on the
    anchor cell, so its cash-refund guarantee is exhausted during the fourth payment
    year, at attained age about 83.4.  The elected period on a PC form, zero on a life
    only form.  Distinct from :func:`guarantee_mths_pricing`, which is the fixed point
    the *kernel* uses before ``B`` is known.  Read from the payout schedule's two static
    quantities, :func:`cum_premium_payout` and :func:`annual_income_payout`.
    """
    if is_period_certain():
        return float(certain_period())
    if is_life_only():
        return 0.0
    b = annual_income_payout()
    return 0.0 if b <= 0.0 else cum_premium_payout() / b


def is_payout(t):
    """Whether month t is in the income phase, ``duration_mth(t) >= T``, inside the frame.

    Deaths in months before ``T`` are deferral-phase deaths attracting the return of
    premium; deaths from ``T`` on are payout-phase deaths attracting the form's refund
    benefit.  ``T`` is a policy month, compared with the policy clock.  False outside the
    frame.
    """
    return is_active(t) and duration_mth(t) >= income_start_mth()


def phase(t):
    """PRE_ISSUE, DEFERRAL, PAYOUT or TERMINATED in month t.

    PRE_ISSUE before a point issued after the valuation date is issued; TERMINATED from the
    stop rule on, ``t = proj_len()``, the first month past the frame.  Each an int code (the
    Space docstring's *Codes*), where ``DIA_US_S`` returns text.
    """
    if duration_mth(t) < 0:
        return PRE_ISSUE                                             # noqa: F821
    if not is_active(t):
        return TERMINATED                                            # noqa: F821
    return PAYOUT if is_payout(t) else DEFERRAL                      # noqa: F821


def is_payment_pm(k):
    """Whether an instalment falls in policy month k: the payment schedule, by policy month.

    Arrears: the n-th instalment falls at the **end** of policy month ``T + n*(12/m) - 1``,
    so the first lands at the end of month ``T`` when ``m = 12`` - one payment period after
    the income start date, which is why policy year 21 of the anchor cell carries the
    first twelve payments.  Advance: the n-th falls at the **start** of policy month
    ``T + (n-1)*(12/m)``, one full payment period earlier.  False before ``T``.  Keyed by
    policy month and counted from ``T`` inside, so that :func:`is_payment_mth` asks it at
    the policy month of month t and :func:`annuity_pp_sched_pm` at any policy month.
    """
    off = k - income_start_mth()
    if off < 0:
        return False
    step = 12 // payment_freq()
    if is_arrears():
        return (off + 1) % step == 0
    return off % step == 0


def is_payment_mth(t):
    """Whether an instalment falls in month t: ``is_payment_pm(duration_mth(t))``.

    The schedule is the contract's, on the policy clock (:func:`is_payment_pm`).  False
    outside the frame.
    """
    return is_active(t) and is_payment_pm(duration_mth(t))


def payment_surv_mth(t):
    """The **time point** at which survival is measured for the instalment falling in t.

    Arrears: the end of month t, time ``t + 1``.  Advance: the start of month t, time
    ``t``.  A time point on the valuation clock, where :func:`lives_if` is indexed.  Using
    end-of-period survival for advance payments understates the liability by about one
    period's mortality per payment.
    """
    return t + 1 if is_arrears() else t


def cola_factor_pm(k):
    """(1+c)^floor((k-T)/12): the COLA escalation applying in policy month k.

    Fixed compound, on each anniversary of the income start date, elected at issue and
    irrevocable [S2][S3][S4].  One in the deferral and in the first payout year.  Keyed by
    policy month and counted from ``T`` inside, the one COLA formula, which
    :func:`annuity_pp_sched_pm`, :func:`accel_cost` and :func:`annuity_payments_ann` read
    at policy months, and :func:`cola_factor` at the policy month of month t.
    """
    d = k - income_start_mth()
    if d < 0:
        return 1.0
    return (1.0 + cola_rate()) ** (d // 12)


def cola_factor(t):
    """(1+c)^floor((t-T)/12): the COLA escalation applying in month t.

    ``cola_factor_pm(duration_mth(t))``, on the policy clock: one in the deferral and in
    the first payout year, whatever the valuation date.  One outside the frame, a factor
    that moves nothing.
    """
    if not is_active(t):
        return 1.0
    return cola_factor_pm(duration_mth(t))


def annuity_pp_sched_pm(k):
    """inst(k) = B(T)/m * (1+c)^floor((k-T)/12): the scheduled instalment in policy month k.

    Zero outside payment months.  Scheduled, not paid: an acceleration blackout or a
    commutation may suppress it.  The payout schedule, fixed at the income start month
    by :func:`annual_income_payout`, on which ``B`` is level, so it is ``DIA_US_S``'s
    ``annual_income(k) / m * cola_factor(k)`` at every payment month.  Keyed by policy
    month, on the policy clock, so that :func:`cum_annuity_pp`, :func:`commuted_value` and
    the acceleration's lump sum read the schedule at policy months after month t without
    passing a policy month as ``t``; :func:`annuity_pp_sched` is this at the policy month
    of month t.
    """
    if not is_payment_pm(k):
        return 0.0
    return annual_income_payout() / payment_freq() * cola_factor_pm(k)


def annuity_pp_sched(t):
    """inst(t) = B/m * (1+c)^floor((t-T)/12): the scheduled instalment per contract.

    ``annuity_pp_sched_pm(duration_mth(t))`` inside the frame, and 0 outside it.  Zero
    outside payment months.  Scheduled, not paid: an acceleration blackout or a
    commutation may suppress it.
    """
    if not is_active(t):
        return 0.0
    return annuity_pp_sched_pm(duration_mth(t))


def cum_annuity_pp(k):
    """G(k): cumulative scheduled instalments per contract to the end of policy month k.

    A **deterministic** as-if-alive schedule - instalments payable while any covered
    life is alive follow the deterministic escalation path - so the refund balance needs
    no path simulation, and no opening state.  A **closing** balance, one month ahead of
    the start-of-month :func:`refund_balance` that consumes it.  Keyed by policy month,
    ``DIA_US_S``'s ``t`` renamed, so ``G(k)`` reads as the notes write it on a contract in
    force as on new business; 0 before the income start month.

    The recursion ``G(k) = G(k-1) + inst(k)`` is ``DIA_US_S``'s, but it is based where the
    valuation date falls: at the policy month before the valuation month, or before issue
    on a contract issued later, ``max(duration_mth_init(), 0) - 1``, a key fixed by the
    model point that reads no clock, one loop sums the instalments from the income start
    month to it, the same additions in the same order as the recursion, so ``G`` is
    ``DIA_US_S``'s to the last bit.  The refund reads ``G`` from there on and recurses back
    to it, and the installment refund's search reads it upward from the first payment
    point, recursing back no further than the key it read before.  Recursing from the
    income start month instead, the first refund of a cash refund long in payout would
    recurse as deep as it has been paying.
    """
    start = income_start_mth()
    if k < start:
        return 0.0
    if k == max(duration_mth_init(), 0) - 1:
        total = 0.0
        for j in range(start, k + 1):
            total += annuity_pp_sched_pm(j)
        return total
    prev = cum_annuity_pp(k - 1) if k > start else 0.0
    return prev + annuity_pp_sched_pm(k)


def certain_mths_refund():
    """n_R: the certain period an installment refund derives, in months.

    Payments "continue in the same amount and frequency until they equal the purchase
    payments" [S2], so ``n_R`` is the offset of the first payment month at which
    cumulative instalments reach ``CP(T)``.  Searched rather than closed so that a COLA
    path still resolves, and bounded by the mortality horizon so that it never depends
    on :func:`proj_len`, which depends on it - and that bound is ``horizon_mths()``,
    **one month past the last projected month of a contract issued at the valuation
    date**, for the same reason as in :func:`annuity_factor`.  **[std]**: the month grid
    rounds the guarantee **up** to a whole instalment rather than trimming the last one,
    which is what the notes' "exactly a certain-and-life annuity with n_g = CP(T)/B"
    framing implies; the payout chassis trims instead.  A count of months from ``T``; the
    search runs over policy months on the payout schedule, :func:`cum_annuity_pp`, against
    the refund base :func:`cum_premium_payout`, so its result does not depend on the
    valuation date.
    """
    t0 = income_start_mth()
    cp = cum_premium_payout()
    step = 12 // payment_freq()
    k = t0 + step - 1 if is_arrears() else t0
    last = horizon_mths()
    while k <= last:
        if cum_annuity_pp(k) >= cp:
            return k - t0 + 1
        k += step
    return max(0, last - t0)


def certain_mths_eff():
    """n_eff: the effective certain period in months, by payout form.

    ``12 * n`` on a period certain form; ``n_R`` on installment refund; **zero on cash
    refund and life only**.  A cash refund is a lump-sum shortfall paid at death, not a
    stream of guaranteed payments - equation (5) treats it as certain-and-life for
    *pricing* only, and carrying that into the projection would pay the guarantee twice.
    A count of months from ``T``: the guarantee covers policy months ``T ... T + n_eff -
    1``, so a contract in force ``d`` months has the months to ``T + n_eff`` left, and none
    once ``d >= T + n_eff``.
    """
    if is_period_certain():
        return 12 * certain_period()
    if is_installment_refund():
        return certain_mths_refund()
    return 0


def certain_floor_pm(k):
    """C(k) = 1{the instalment in policy month k falls inside the guarantee period}.

    ``0 <= k - T < n_eff``: keyed by policy month and counted from ``T`` inside, so that
    :func:`certain_floor` asks it at the policy month of month t and the acceleration's
    lump sum at the policy months of the instalments it pulls forward.
    """
    d = k - income_start_mth()
    return 1.0 if 0 <= d < certain_mths_eff() else 0.0


def certain_floor(t):
    """C(t) = 1{the instalment in month t falls inside the guarantee period}.

    ``certain_floor_pm(duration_mth(t))`` inside the frame, and 0 outside it.  The certain
    months left at the valuation date are therefore no opening state: they follow from
    ``duration_mth``.
    """
    if not is_active(t):
        return 0.0
    return certain_floor_pm(duration_mth(t))


def payment_factor_life(t):
    """L(t): the life-contingent payment factor for the instalment falling in month t.

    Survival is measured at :func:`payment_surv_mth`, not at t.  By form and trigger::

        single life:           L = l_1
        joint, trig = either:  L = l_1*l_2 + delta*(l_1 + l_2 - 2*l_1*l_2)
        joint, trig = primary: L = l_1 + delta*(1 - l_1)*l_2

    The *either* form pays the full instalment while **both** are alive and delta while
    **exactly one** is; the *primary* form pays in full while the primary lives whatever
    the joint annuitant's status.  The two coincide on the primary's death and differ
    only on the secondary's, which is why the trigger is a switch and not a footnote.
    On a joint contract in force with one life already dead, as point 23 is, the factor is
    delta times the survivor's survival from ``t = 0``.  Zero before the income start date,
    and outside the frame.
    """
    if not is_payout(t):
        return 0.0
    s = payment_surv_mth(t)
    l1 = lives_if(s, 1)
    if not is_joint():
        return l1
    l2 = lives_if(s, 2)
    d = survivor_pct()
    if is_trigger_either():
        return l1 * l2 + d * (l1 + l2 - 2.0 * l1 * l2)
    return l1 + d * (1.0 - l1) * l2


def surv_to_payout_init():
    """l_last(T) carried in force: the cohort that reached the income phase.

    The ``surv_to_payout_init`` column, on a contract whose income start month precedes
    the valuation month: ``DIA_US_S``'s ``surv_to_payout()``, the probability, from issue,
    that a covered life was alive at the income start month.  The lives at the valuation
    date cannot say it: in a certain period the contract stays open after the last death,
    its guarantee running on to a beneficiary, so the cohort the guarantee pays exceeds the
    survivors, 0.715 against 0.5577 on point 20, in force 300 months.  On a real record in
    payout it is 1.  Read only where the certain floor is positive, so on a period certain
    or an installment refund; ``Data`` requires it on every contract past its income start
    month, a rule a contract record meets without the certain period, though on a cash
    refund or a life-only form nothing reads it.  Blank elsewhere.  Read from
    ``Data.surv_to_payout_init``.
    """
    return float(data.surv_to_payout_init()[idx])                    # noqa: F821


def surv_to_payout():
    """l_last(T): the probability that the income phase is ever reached.

    **The one place the payout chassis cannot be carried across unexamined.**  A SPIA
    is already in payment, so ``SPIA_US_S`` weights its certain floor by
    nothing: ``C(t)`` is a bare indicator.  A DIA's guarantee period only begins if the
    contract reaches the income start date - an annuitant who dies in the deferral
    receives the return-of-premium benefit and no instalment is ever paid - so on an
    expected basis the certain instalments carry this factor.  Without it a period
    certain or installment refund contract would pay its guarantee with probability
    one and overstate the liability by the whole deferral mortality.  The DIA notes
    inherit ``L_pay`` and its "certain inside a guarantee period" wording from the
    immediate-annuity notes without adjusting for the deferral; this is that
    adjustment, and it is the same weight equation (1) applies through ``_d p_x``.

    A frozen weight: on a contract valued after its income start month, the opening state,
    :func:`surv_to_payout_init`; otherwise ``lives_if_last`` at the income start month on
    the valuation clock, ``T - duration_mth_init()``, which on a contract valued at its
    income start month is time 0.  Read only where the certain floor is positive, from the
    income start month on, so never ahead of the month that reads it.
    """
    if duration_mth_init() > income_start_mth():
        return surv_to_payout_init()
    return lives_if_last(income_start_mth() - duration_mth_init())


def payment_factor(t):
    """Phi(t) = max(C(t) * l_last(T), L(t)): the master payment factor.

    The ``max`` makes the certain period an annuity-**certain floor** rather than an
    additional stream: during the guarantee the full unreduced instalment is payable
    regardless of survival *after the income start date*, and the ``max`` prevents
    paying ``1 + L``.  An additive construction silently doubles the guarantee - the
    payout chassis' first-listed pitfall - and, because the floor pays the *unreduced*
    instalment, it also reproduces with no extra flag the rule that a survivor reduction
    inside a guarantee period is deferred to the end of that period [S1][S3].  The
    ``l_last(T)`` weight on the floor is the DIA's own; see :func:`surv_to_payout`, which
    is read only where the floor is positive: elsewhere the floor is 0, as
    ``DIA_US_S``'s ``0 * l_last(T)`` is.
    """
    c = certain_floor(t)
    floor = c * surv_to_payout() if c > 0.0 else 0.0
    return max(floor, payment_factor_life(t))


def refund_balance(t):
    """RG(t) = max(0, CP(T) - income scheduled through the end of policy month m-1).

    ``m = duration_mth(t)``.  The ``m - 1`` is the arrears convention: an instalment due at
    the end of the death month has not been paid, so a death between ``T`` and ``T + 1/m``
    yields a cash refund of the **full** ``CP(T)``.  On advance timing an instalment paid
    at the *start* of the death month **has** been paid, so the balance is measured at
    ``m`` there or the lump sum is overstated by one instalment.  ``CP(T)`` is
    :func:`cum_premium_payout` and ``G`` the payout schedule's :func:`cum_annuity_pp`, by
    policy month.  Zero before the income start month and outside the frame.
    """
    m = duration_mth(t)
    if not is_active(t) or m < income_start_mth():
        return 0.0
    adv = not is_arrears() and is_payment_mth(t)
    return max(0.0, cum_premium_payout() - cum_annuity_pp(m if adv else m - 1))


def accel_blackout(t):
    """Whether payments are suspended in month t by a payment acceleration.

    Six monthly payments are made in one sum at ``t_a`` and no payment is made for the
    following five months [S1][S4].  The feature is expressly "not a liquidity feature"
    [S2] - a timing shift, not a withdrawal - and modelling it as a withdrawal is one of
    the notes' listed pitfalls.  ``t_a < duration_mth(t) <= t_a + 5``, on the policy
    clock; False outside the frame.
    """
    a = accel_mth()
    if a < 0 or not is_active(t):
        return False
    return a < duration_mth(t) <= a + accel_months - 1               # noqa: F821


def accel_cost():
    """Cost(t_a): the economic cost of a payment acceleration, equation (12).

    ``(B/m) * sum over j = 1..n_a-1 of [ 1 - v^(j/m) * _{j/m} p_x(t_a) ]``.  Accelerated
    payments are made **unconditionally**, so the insurer forgoes the survivorship and
    interest discount on payments 2 through ``n_a``.  Small but real, and the reason the
    feature is capped in uses and gated at age 59 1/2 - the gate itself being driven by
    the IRC SS72(q) 10% additional tax [R8][REG-R55].  Reported, not added to the cash
    flows: the cost is already implicit in paying them early.  Only the **mortality**
    element of it surfaces in the projected cash flows, because they are undiscounted -
    on the anchor configuration 435.11 per exercising contract here against 153.52 of
    extra lifetime income outgo, the difference being the interest term ``v^(j/m)`` that
    an undiscounted projection has nowhere to put.  Priced at the exercise's policy month
    on the pricing curve, :func:`lives_if_pm`, with the instalment of the payout schedule,
    so it is ``DIA_US_S``'s cost whatever the valuation date.  Each instalment is
    discounted as :func:`pricing_disc_factor` discounts, written inline.

    ``Data`` bounds the exercise month from below alone, and the pricing survival's cache
    ends at policy month 1,446 (``spec_sec.py``).  Past the age stop, ``12 * (omega_age -
    age_at_entry(1))``, with ``mort_ae_factor`` 1 or more, the rate is 1 from the limiting
    age on, so ``DIA_US_S``'s survival in every later month is the one float it reaches a
    month after the stop, 0 on a finite curve, and its cost 0: the survival is read there,
    and the cost is ``DIA_US_S``'s, compiled as in modelx, however late the exercise, which
    the projection never reaches (M24).  Below an A/E of 1 the rate past the limiting age
    is the A/E, the survival positive, and it is read at the exercise month as
    ``DIA_US_S`` reads it: past the cache, from an exercise at policy month 1,442, that
    read raises ``IndexError`` in the compiled model alone, where modelx reads on as
    ``DIA_US_S`` does (``model-sec.md``, *What it refuses*).
    """
    a = accel_mth()
    if a < 0:
        return 0.0
    stop = max(12 * (omega_age - age_at_entry(1)), 0)                # noqa: F821
    if a > stop and mort_ae_factor >= 1.0:                           # noqa: F821
        base = lives_if_pm(stop + 1, 1)
    else:
        base = lives_if_pm(a, 1)
    if base <= 0.0:
        return 0.0
    inst = annual_income_payout() / payment_freq() * cola_factor_pm(a)
    total = 0.0
    for j in range(1, accel_months):                                 # noqa: F821
        sp = lives_if_pm(a + j, 1) / base
        total += 1.0 - (1.0 + pricing_rate) ** (-(j / 12.0)) * sp    # noqa: F821
    return inst * total


def accel_payment_factor(t):
    """Phi for an instalment scheduled in month t but paid in the acceleration lump sum.

    The six instalments are paid **in one sum** at ``t_a`` [S1][S4], so the five that are
    pulled forward are paid **unconditionally**: their survivorship is frozen at the date
    the lump sum falls - ``payment_factor_life`` in the exercise month, the same weight the
    first instalment of the block carries - instead of being measured at their own
    scheduled dates.  That frozen weight *is* the mortality element equation (12)
    prices; the interest element of (12) does not appear in an undiscounted projection.

    A **guaranteed** instalment is untouched.  Its weight is already
    ``C(t) * l_last(T)``, independent of survival after the income start date, so
    accelerating it forgoes no survivorship - which is why the ``max`` is taken against
    the certain floor exactly as :func:`payment_factor` does, and why equation (12)'s
    cost is zero inside a guarantee period and strictly positive outside it.

    ``DIA_US_S``'s weight in a blackout month whose exercise is on the books, the
    exercise month at or after the valuation date, and 0 in every other month: with no
    acceleration, outside the blackout, and where the lump sum was paid before the
    valuation date, from which on nothing reads the factor.  :func:`annuity_payments`
    computes the same weight in the exercise month itself, reading the payout schedule by
    policy month, so this cell is ``DIA_US_S``'s, for its readers and for the twin
    identity, and no projection cell calls it.
    """
    a = accel_mth()
    if not accel_blackout(t) or a < duration_mth_init():
        return 0.0
    c = certain_floor(t)
    floor = c * surv_to_payout() if c > 0.0 else 0.0
    return max(floor, payment_factor_life(a - duration_mth_init()))


def commute_frac_cum(t):
    """theta_cum(t): the cumulative commuted fraction applying in month t.

    Zero before the exercise month and ``commute_frac`` from it, the exercise falling at
    the **start** of the month and so reaching that month's own instalment - the notes'
    processing order puts option exercises ahead of the income payment.  It multiplies
    ``C(t)`` in :func:`annuity_pp_paid`, so it reaches guaranteed instalments only: if
    the annuitant is alive when the would-be guarantee period ends, income **resumes
    until death**, the life-contingent tail not being commuted [S4].  Applying it to
    that tail contradicts every retrieved contract.  The commutation is one exercise
    named on the model point, so the fraction follows from the policy clock,
    ``duration_mth(t) >= t_c``, and needs no opening state.  Zero outside the frame.
    """
    c = commute_mth()
    if c < 0 or not is_active(t) or duration_mth(t) < c:
        return 0.0
    return commute_frac()


def commute_weight_init():
    """l_last(t_c) carried in force: the cohort that commuted.

    The ``commute_weight_init`` column, on a contract whose commutation month precedes the
    valuation month: ``DIA_US_S``'s ``lives_if_last(t_c)``, the probability, from issue,
    that a covered life was alive to exercise the commutation, and so the cohort whose
    guaranteed instalments it extinguished.  The lives at the valuation date cannot say
    it: the contracts whose annuitant died between ``T`` and ``t_c`` keep their guarantee,
    running to the beneficiary, so the residual guaranteed stream is
    ``l_last(T) - l_last(t_c)``.  On a real record of a commuted contract it is 1.  Given
    exactly where the commutation precedes the valuation month, as ``Data`` requires, and
    blank elsewhere.  Read from ``Data.commute_weight_init``.
    """
    return float(data.commute_weight_init()[idx])                    # noqa: F821


def commute_weight(t):
    """l_last(t_c): the expected size of the cohort a commutation extinguishes in month t.

    **The one weight the payout chassis has no need for, and the mirror image of**
    :func:`surv_to_payout`.  A commutation is exercised by an owner who is *alive* at
    ``t_c`` [S4], so it can only extinguish the guaranteed instalments of the
    ``l_last(t_c)`` sub-cohort.  The rest of the cohort that reached the income phase -
    ``l_last(T) - l_last(t_c)``, contracts whose annuitant died between ``T`` and ``t_c``
    - keeps its guarantee running to the beneficiary and is unaffected.  On the shipped
    commutation model point those two weights are ``0.715000`` and ``0.680338``, and
    ``l_last(t_c)`` is the one this model applies: applying the
    commutation to all of the first would cancel 4.85% more guaranteed liability than
    the commuted value pays for.

    Zero outside a guarantee period, before the exercise month, and on a contract that
    never commutes.  Bounded above by :func:`payment_factor` because ``t_c >= T``, which
    ``Data`` checks, so the surviving expected instalment is never negative.  A frozen
    weight: on a contract that commuted before the valuation month, the opening state,
    :func:`commute_weight_init`; otherwise ``lives_if_last`` at the commutation month on
    the valuation clock, ``t_c - duration_mth_init()``, read from that month on.
    """
    c = commute_mth()
    if c < 0 or duration_mth(t) < c or certain_floor(t) == 0.0:
        return 0.0
    if c < duration_mth_init():
        return commute_weight_init()
    return lives_if_last(c - duration_mth_init())


def ref_rate_shift_init():
    """The reference rate's change from issue to the valuation date.

    The ``ref_rate_shift_init`` column, a decimal, 0.005 for a rise of 50 basis points, of
    either sign: the reference rate at the valuation date less the reference rate at the
    contract's issue, the part of the change since issue that a contract in force has
    already seen.  The commutation discount rate moves with the change since issue, floored
    at 0 (:func:`commute_disc_rate`), and that change began before ``t = 0``, so its value
    there is opening state, as a rate's value at the start of a term would be on a market
    path.  A fact of the market, not of the contract's own history: two contracts issued
    together carry one value.  0 at issue, and so on every point not yet in force, as
    ``Data`` checks.  The change made at the valuation date is ``ref_rate_shift``, which a
    contract issued later has not seen (:func:`commute_disc_rate`).  Read from
    ``Data.ref_rate_shift_init``.
    """
    return float(data.ref_rate_shift_init()[idx])                    # noqa: F821


def commute_disc_rate(t):
    """i_c(t) = i_p + max(0, r_ref(t) - r_ref(0)) + m_c: the commutation rate, eq (13).

    One-sided by construction - it rises with rates and does not fall - implementing the
    Compact's stated intent that the adjustment "reduce interest risk in the event of
    rising interest rate after issue" and its required disclosure that "the higher the
    interest rate the lower the commuted value" [R13 SS3.F(7)].  **The actual contractual
    formula is not published anywhere** [S4][S5], so this is **[std]** and
    **[unverified]**.

    Every contract of a block reads the change since its own issue on one path of the
    reference rate, which every point shares, as it shares every economic input.  A
    contract on the books at the valuation date, in force or issued then,
    ``t_entry() == 0``, has seen :func:`ref_rate_shift_init` by that date, from its model
    point, and sees ``ref_rate_shift``, the change made at the valuation date, from month
    0 on, as ``DIA_US_S``'s contract sees its ``ref_rate_shift`` from issue; a contract
    issued ``t_entry()`` months later is bought after that change and has seen none of
    it, its column being 0.  The floor applies to the whole change since issue, the two
    parts added first, ``i_p + max(0, ref_rate_shift_init() + shift) + m_c`` in that
    order, so a fall before the valuation date offsets a rise at it, and on a point issued
    at the valuation date the rate is ``DIA_US_S``'s ``i_p + max(0, ref_rate_shift) + m_c``
    to the last bit.  One Reference could not hold the change since each contract's own
    issue: contracts issued at different dates have seen different changes.
    ``ref_rate_shift`` is a flat scalar, a path that steps once, at the valuation date, so
    the rate is level and reads neither clock; a reference-rate path would be another input
    table, read on the valuation clock.
    """
    shift = ref_rate_shift if t_entry() == 0 else 0.0                # noqa: F821
    return (pricing_rate + max(0.0, ref_rate_shift_init() + shift)   # noqa: F821
            + commute_margin)                                        # noqa: F821


def commuted_value(t):
    """CV(t): the commuted value of the remaining guaranteed payments, equation (14).

    ``sum over j in J_g(t) of (B/m) * (1 + i_c(t))^(-(j - m)/12)``, where ``J_g`` is the
    set of remaining **guaranteed** payment months and ``m = duration_mth(t)``.  Zero on a
    form with no guaranteed stream: a cash refund is a lump sum at death, not a schedule
    of payments, so there is nothing to commute.  Non-zero only in the exercise month.
    The guaranteed instalments are read from the payout schedule by policy month,
    :func:`annuity_pp_sched_pm`, in one loop, so that no month of the frame ahead of t is
    read.  Zero outside the frame.
    """
    c = commute_mth()
    if c < 0 or not is_active(t) or duration_mth(t) != c:
        return 0.0
    n_eff = certain_mths_eff()
    if n_eff <= 0:
        return 0.0
    m = duration_mth(t)
    start = income_start_mth()
    i = commute_disc_rate(t)
    total = 0.0
    for k in range(max(m, start), start + n_eff):
        inst = annuity_pp_sched_pm(k)
        if inst:
            total += inst * (1.0 + i) ** (-(k - m) / 12.0)
    return total * commute_frac()


def commutations(t):
    """E[COMM(t)]: the commutation payment made to the owner in month t.

    ``CV(t) * l_last(t)``: the commuted value is paid to the cohort alive to exercise,
    which is the **same** ``l_last(t_c)`` weight :func:`commute_weight` removes from the
    guaranteed instalments, on the contracts on the books.  The two must agree, and
    :func:`check_commutation_value` asserts that they do - discounted at ``i_c``, the
    value paid out equals the value suppressed.  Zero in the base run - commutation exists
    only in the extended case [S4][S5] - and prohibited on a QLAC after the required
    beginning date other than a rescission period not exceeding 90 days
    [R1 (q)(1)(iv)][R2 SS202(a)(4)].  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_DECR) * lives_if_last(t) * commuted_value(t)


def annuity_pp(t):
    """The instalment per contract payable in month t, before commutation and survival.

    Equal to :func:`annuity_pp_sched` except during an acceleration blackout, where the
    payment has already been made in one sum at the exercise month.
    """
    if accel_blackout(t):
        return 0.0
    return annuity_pp_sched(t)


def annuity_pp_paid(t):
    """inst(t) * (1 - theta_cum(t) * C(t)): the instalment a **commuting** contract gets.

    A commutation reduces guaranteed instalments only; the life-contingent payments
    after the guarantee period are untouched, which is what makes the tail resume.  Per
    contract, and only for a contract that actually commuted - which is a sub-cohort,
    not the whole model point, so :func:`annuity_payments` applies it through
    :func:`commute_weight` rather than to the expected instalment as a whole.
    """
    return annuity_pp(t) * (1.0 - commute_frac_cum(t) * certain_floor(t))


def annuity_payments(t):
    """E[income] in month t: the instalment weighted over the cohorts entitled to it.

    Two cohort splits sit on top of the chassis' ``inst(t) * Phi(t)``, and both are
    weights rather than per-contract adjustments::

        E[income](t) = pols * [ inst(t) * (Phi(t) - w_c(t))          not commuted
                              + inst_paid(t) * w_c(t) ]              commuted

    ``pols`` is the count on the books, ``pols_if_at(t, BEF_DECR)``.  ``w_c(t)`` is
    :func:`commute_weight`, the ``l_last(t_c)`` sub-cohort that was alive to exercise the
    commutation; ``inst_paid`` is that sub-cohort's reduced instalment.  Multiplying
    ``inst_paid`` by the whole of ``Phi`` instead - the obvious reading of the chassis
    formula - would cancel the guarantee of contracts whose annuitant died between ``T``
    and ``t_c`` and could not have commuted.

    In the exercise month of a payment acceleration the following ``n_a - 1``
    instalments are added at the survivorship frozen at the lump sum's own date, the
    exercise month's ``payment_factor_life``, floored by the certain floor of each
    instalment's own month as :func:`accel_payment_factor` floors it - they are paid
    whether or not the annuitant survives to their scheduled dates, which is precisely the
    mortality element equation (12) measures - and the months they would have fallen in
    pay nothing.  The instalments and their floors are read from the payout schedule by
    policy month, so the lump sum reads no month of the frame ahead of the exercise.  The
    lump sum weighs no commutation: after one, it would pay the cohort that commuted its
    pulled-forward guaranteed instalments unreduced, as ``DIA_US_S``'s does, so
    :func:`proj_len` refuses an acceleration whose lump sum pulls forward instalments of a
    commuted guarantee.
    """
    w = commute_weight(t)
    pols = pols_if_at(t, BEF_DECR)
    total = pols * (annuity_pp(t) * (payment_factor(t) - w) + annuity_pp_paid(t) * w)
    a = accel_mth()
    if a >= 0 and is_active(t) and duration_mth(t) == a:
        life = payment_factor_life(t)
        for j in range(1, accel_months):                             # noqa: F821
            c = certain_floor_pm(a + j)
            floor = c * surv_to_payout() if c > 0.0 else 0.0
            total += pols * annuity_pp_sched_pm(a + j) * max(floor, life)
    return total


def claim_pp(t, kind):
    """The claim amount per contract in month t, by ``kind``.

    ``DEATH`` - the deferral death benefit, 100% of cumulative premiums paid without
    interest as a lump sum at the end of the month of death
    [S1][S2][S3][S4][R13 SS3.I(1)(a)], zero once the income phase starts and zero on a
    no-death-benefit form.  ``REFUND`` - the cash-refund shortfall
    :func:`refund_balance`, zero on any form other than cash refund, because installment
    refund and period certain deliver their guarantee as continued payments through the
    certain floor rather than as a lump sum.  Zero outside the frame; any other kind
    raises, ``ALL``, the total, among them, as ``DIA_US_S``'s ``claim_pp(t, None)`` does.
    """
    if kind == DEATH:
        if not is_active(t) or is_payout(t) or not is_rop():
            return 0.0
        return cum_premium_pp(t)
    if kind == REFUND:
        if not is_payout(t) or not is_cash_refund():
            return 0.0
        return refund_balance(t)
    raise ValueError("invalid kind")


def claims(t, kind):
    """Expected claim outgo in month t, by ``kind``; ``ALL`` totals the two kinds.

    Weighted by :func:`lives_death_last`, the death that ends the contract: on a joint
    contract the first death leaves the contract running on the option chosen at issue
    [S2], so both the deferral death benefit and the refund attach to the last death, on
    the contracts on the books, ``pols_if_at(t, BEF_DECR)``.  The two kinds are mutually
    exclusive by construction - ``DEATH`` is zero from the income start month and
    ``REFUND`` is zero before it.

    ``ALL`` is ``DIA_US_S``'s ``kind=None``, its total, written as ``DIA_US_S`` writes it,
    the sum of the two kinds' cells, so that it is ``DIA_US_S``'s float, the sign of a zero
    included, where a sum from ``0.0`` would turn a negative zero positive.
    """
    if kind == ALL:                                                  # noqa: F821
        return claims(t, DEATH) + claims(t, REFUND)                  # noqa: F821
    return pols_if_at(t, BEF_DECR) * lives_death_last(t) * claim_pp(t, kind)


def premiums(t):
    """Premium income in month t: ``l(t) * sum of P_k at t``, received at the start.

    Deterministic schedule with no attrition **[std]**: DIA subsequent premiums are
    wholly discretionary and no source publishes a distribution of them.  Dump-in risk
    differs structurally from a fixed deferred annuity's - each premium is priced at
    *then-current* rates, so there is no rate guarantee to select against unless the
    contract guarantees paid-up rates for future premiums [R13 SS1.B(1)(h)], which is off
    in the base **[std]**.  On the contracts on the books, ``pols_if_at(t, BEF_DECR)``,
    so a point issued after the valuation date brings its premiums as new business.
    """
    return pols_if_at(t, BEF_DECR) * premium_pp(t) * lives_if_last(t)


def inflation_factor(t):
    """The expense escalation factor in month t: ``(1 + g)^(t // 12)`` **[std]**.

    On the **valuation** clock: ``DIA_US_S``'s annual steps, ``(1 + g)^(y(t) - 1)``, moved
    onto ``t``, so that the maintenance charge it inflates is in valuation-date dollars,
    whatever the contract's age, and every point of a block inflates alike, stepping on
    each anniversary of the valuation date.  On a point issued at ``t = 0`` the two are the
    same.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """E[EXP(t)] = (e/12) * (1+g)^(t//12) * pols_if(t): maintenance expense in month t.

    $50 per contract per year escalated at 2.5%: VM-22 prescribes exactly that for
    individual Payout Annuity Reserving Category contracts, plus 7 basis points on a
    present-value base for contracts without an account value [R9]; adopting the
    prescribed figure as the best estimate is **[std]**, and the 7 bp element is not
    implemented because this model computes no present-value base.  The inflation runs on
    the valuation clock (:func:`inflation_factor`), and the count is the contracts on the
    books weighted by survival, :func:`pols_if`.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def liability_outgo(t):
    """Total gross liability outgo in month t, outgo positive.

    Income payments, death and refund benefits, any commutation, and maintenance
    expense.  **There is no surrender cash flow row, and none should be added** - the
    contract has no cash surrender value at any time before the income start date and
    none after [S1][S2][R13 SS3.P].
    """
    return annuity_payments(t) + claims(t, ALL) + commutations(t) + expenses(t)  # noqa


def liability_cf(t):
    """The net liability cash flow in month t, **outgo positive**: ``-net_cf(t)``.

    Across this library ``liability_cf`` is the net stream carried under the sign the
    notes that print one use, and ``net_cf`` is the same stream income-positive; the
    invariant ``net_cf(t) == -liability_cf(t)`` holds in every model that publishes both,
    and a conventions test asserts it.

    The distinction that matters here: the notes' purpose statement projects "premiums in;
    deferral death benefits, income...", so premium income belongs in the net stream.
    That makes this product differ from the :mod:`~.SPIA_US_S` payout chassis it
    otherwise follows, where the single premium is a pricing input and never a projected
    cash flow, so there gross outgo and the net stream coincide.  The gross outgo alone is
    :func:`liability_outgo`.
    """
    return liability_outgo(t) - premiums(t)


def net_cf(t):
    """Net cash flow to the insurer in month t: premium income less liability outgo.

    The sign convention of ``Term_US_S.net_cf``.  Unlike the immediate-annuity chassis
    this product **does** carry premium income in the projection, because premiums are
    flexible and fall throughout the deferral - so premium income nets here, and
    :func:`liability_cf` is this stream negated rather than the gross outgo
    :func:`liability_outgo`.
    """
    return premiums(t) - liability_outgo(t)


def qlac_room(t):
    """qlac_room(t) = Limit - CP(t) - premiums paid to any other intended QLAC.

    $200,000 as enacted, indexed with a base period of the calendar quarter beginning
    July 1 2022 and increments rounded to the next lowest multiple of $10,000;
    **$210,000 for 2026** [R1 (q)(2)(ii), (q)(4)(ii)(A)][R2 SS202(a)(2)][R3][S4].  There
    is **no percentage-of-account-balance limit**: SECURE 2.0 SS202(a)(1) directed its
    elimination and the codified text has no percentage test, so a 25% rule, a $125,000
    or $130,000 cap and an RMD age of 70 1/2 are all superseded arithmetic.
    """
    return qlac_premium_limit - cum_premium_pp(t) - other_qlac_premium()  # noqa: F821


def qlac_flags():
    """The QLAC conditions this contract fails; an empty list when it complies.

    The overlay generates **no cash flows of its own** - it caps premiums, restricts
    forms, constrains ``T``, disables features and raises compliance flags.  Loss of
    QLAC status changes the owner's RMD position, not the insurer's liability cash
    flows.  An excess premium ends QLAC status on the date paid unless returned by the
    end of the following calendar year; any other failure voids status retroactively to
    purchase [R1 (q)(4)(i)(B), (q)(4)(iii)(A)].  Empty on a contract that is not a QLAC.
    The premium limit is tested on the premiums paid by the last projected month, and the
    income start age on the policy clock, ``age_at_entry(1) + T // 12``; the market type
    and the form are read through the decodes.
    """
    if not is_qlac():
        return []
    out = []
    if qlac_room(proj_len() - 1) < 0.0:
        out.append("premium limit exceeded")
    if age_at_entry(1) + income_start_mth() // 12 > qlac_max_start_age:  # noqa: F821
        out.append("income start after the age limit")
    if cola_rate() > 0.0:
        out.append("cost-of-living adjustment on a QLAC")
    if commute_mth() >= 0:
        out.append("commutation on a QLAC")
    if accel_mth() >= 0:
        out.append("payment acceleration on a QLAC")
    if not (is_life_only() or is_cash_refund()):
        out.append("income form not permitted on a QLAC")
    return out


def check_lives_roll_fwd_resid(t):
    """Residual between :func:`lives_if` and its recursion restated, over both lives.

    Indexed by a **time point** on the valuation clock, like :func:`lives_if` itself.  For
    each covered life the survival is restated month by month from the opening state:
    0 before :func:`t_entry`, :func:`lives_if_init` at it, and ``l(t-1) * (1 - q(t-1))``
    after it; the residual is the sum of the per-life differences from :func:`lives_if`,
    plus, on a joint contract, the last-survivor identity
    ``l_last(t) - [l_1 + l_2 - l_1*l_2]``.  Zero to floating point.

    Deliberately **not** ``DIA_US_S``'s telescoping identity ``l_i(t) - d_i(t) -
    l_i(t+1)``: :func:`lives_death` is *defined* as that difference, so the identity is
    identically zero whatever :func:`lives_if` returns and constrains nothing.  Restating
    the recursion from the opening state, a misindexed or mis-based recursion fails it; it
    shares the monthly rate with :func:`lives_if`, which the twin and splice identities
    check against ``DIA_US_S``.  It reads one month back, so it costs a cell a month,
    where a running product rebuilt at every time point would hold a dependency graph
    quadratic in the frame.  The last-survivor term *is* zero by construction, like
    :func:`check_payment_factor_resid`, and exists to catch a redefinition of
    :func:`lives_if_last` that broke the independence construction.  The signed float at a
    single ``t``, for the debugging session that follows a :func:`check_lives_roll_fwd`
    failure.
    """
    res = 0.0
    entry = t_entry()
    for i in range(1, 3):
        if i == 2 and not is_joint():
            continue
        if t < entry:
            built = 0.0
        elif t == entry:
            built = lives_if_init(i)
        else:
            built = lives_if(t - 1, i) * (1.0 - mort_rate_mth(t - 1, i))
        res += built - lives_if(t, i)
    if is_joint():
        l1 = lives_if(t, 1)
        l2 = lives_if(t, 2)
        res += lives_if_last(t) - (l1 + l2 - l1 * l2)
    return res


def check_lives_roll_fwd():
    """``True`` when the in-force roll-forward closes in every projected month.

    No argument and a bool, the library-wide ``check_*`` shape taken from
    ``CashValue_SE.check_av_roll_fwd()``: one call covers ``t = 0 .. proj_len() - 1``, so
    the same name can be asserted across every model in the library.
    :func:`check_lives_roll_fwd_resid` carries the signed residual at a single ``t``, the
    survival recursion restated from the opening state.  Mortality is the only decrement
    here, so a failure means the projection's survival and its recursion, or the
    last-survivor construction and the per-life survival, have come apart.
    """
    return all(abs(check_lives_roll_fwd_resid(t)) < 1e-12
               for t in range(proj_len()))


def check_income_roll_fwd_resid(t):
    """``B(t) - B(t-1)*adj - P_k*pr`` in month t: the income roll-forward residual, eq (8).

    Zero to floating point.  Non-zero would mean income appearing from somewhere other
    than a premium slice or the one permitted repricing - and **nothing else can move
    it**: there is no credited rate, no index, no charge and no balance in this product.
    The signed float at a single ``t``; :func:`check_income_roll_fwd` is the bool.
    At :func:`t_entry` the prior income is the opening state,
    :func:`annual_income_init`, rather than a month before the books.  The exercise month
    and the purchase rate are read at the policy month of month ``t``.  Zero outside the
    frame.
    """
    if not is_active(t):
        return 0.0
    prev = annual_income(t - 1) if t > t_entry() else annual_income_init()
    if duration_mth(t) == adjust_mth():
        prev = prev * adjust_income_factor()
    bought = premium_pp(t) * purchase_rate(duration_mth(t)) if premium_pp(t) else 0.0
    return annual_income(t) - prev - bought


def check_income_roll_fwd():
    """``True`` when income moves only by a premium slice or the permitted repricing.

    No argument and a bool over every projected ``t``, the library-wide ``check_*`` shape;
    :func:`check_income_roll_fwd_resid` returns the signed residual at one ``t``.  The
    tolerance is absolute rather than relative because ``B`` is a currency amount that
    only ever steps, never accrues.
    """
    return all(abs(check_income_roll_fwd_resid(t)) < 1e-9
               for t in range(proj_len()))


def check_payment_factor_resid(t):
    """``Phi(t) - max(C(t)*l_last(T), L(t))`` in month t: the double-count residual.

    Zero by construction.  Computed anyway because an additive floor - ``C + L`` instead
    of ``max(C, L)`` - is the payout chassis' first-listed pitfall and would show up
    here as ``min(C, L)``.  :func:`check_payment_factor` is the bool over every ``t``.
    ``l_last(T)`` is read only where the certain floor is positive, as
    :func:`payment_factor` reads it.
    """
    c = certain_floor(t)
    floor = c * surv_to_payout() if c > 0.0 else 0.0
    return payment_factor(t) - max(floor, payment_factor_life(t))


def check_payment_factor():
    """``True`` when Phi is the max of the two legs, never their sum, in every month.

    No argument and a bool, the library-wide ``check_*`` shape.  The comparison is exact
    rather than tolerant: the identity is arithmetical, so any residual at all is a
    defect and not a rounding artefact.
    """
    return all(check_payment_factor_resid(t) == 0.0
               for t in range(proj_len()))


def check_commutation_value_resid(t):
    """``PV_ic(instalments suppressed) - commutations(t_c)``: the exchange residual.

    A commutation is an exchange, not a benefit: the owner gives up guaranteed
    instalments and receives their present value at ``i_c``.  On an expected basis the
    two legs must therefore carry the *same* cohort weight, and this residual is what
    catches it if they do not.

    The suppressed leg is read out of :func:`annuity_payments` itself rather than
    re-derived - what the projection would have paid, ``inst(s) * Phi(s)``, less what it
    does pay - so weighting the suppression by ``l_last(T)`` while paying the commuted
    value to ``l_last(t_c)`` shows up here as a leak equal to the difference: 6,898.37 on
    the shipped commutation model point.  The acceleration block is added back before the
    comparison so that the two options do not contaminate each other.  It is reached where
    an acceleration falls in a commuted guarantee's last month, its lump sum pulling
    forward life-contingent instalments alone: ``Data`` refuses an acceleration within six
    months of the commutation, the product's interlock [S4], and :func:`proj_len` one whose
    lump sum would pull forward instalments of the guarantee the commutation reduced, which
    :func:`annuity_payments` would pay unreduced, as ``DIA_US_S``'s does.

    **Measured at the guarantee's last month**, policy month ``T + n_eff - 1``, reading
    back to the commutation month ``t_c``: ``DIA_US_S`` takes the same sum at the exercise
    month, reading every guaranteed month still to come, which on the valuation clock is a
    read far ahead of the month that makes it.  Here every month read is at or before the
    month the residual is measured in, and the sum is the same, month by month and
    discounted at ``i_c(t_c)`` from the exercise month, so the residual equals
    ``DIA_US_S``'s at the exercise month.  Zero to floating point there, and zero in every
    other month; zero too where the commutation precedes the valuation month, the exchange
    having closed before it, and where it falls after the guarantee, with nothing to
    commute.  :func:`check_commutation_value` is the bool over every ``t``.
    """
    c = commute_mth()
    start = income_start_mth()
    end = start + certain_mths_eff()
    d = duration_mth_init()
    if (c < 0 or c < max(d, 0) or c >= end or not is_active(t)
            or duration_mth(t) != end - 1):
        return 0.0
    t_c = c - d
    a = accel_mth()
    i = commute_disc_rate(t_c)
    total = 0.0
    for s in range(t_c, t + 1):
        k = duration_mth(s)
        paid = annuity_payments(s)
        if k == a:
            life = payment_factor_life(s)
            for j in range(1, accel_months):                         # noqa: F821
                cf = certain_floor_pm(a + j)
                floor = cf * surv_to_payout() if cf > 0.0 else 0.0
                paid -= (pols_if_at(s, BEF_DECR) * annuity_pp_sched_pm(a + j)
                         * max(floor, life))
        supp = pols_if_at(s, BEF_DECR) * annuity_pp(s) * payment_factor(s) - paid
        total += supp * (1.0 + i) ** (-(k - c) / 12.0)
    return total - commutations(t_c)


def check_commutation_value():
    """``True`` when the commutation exchange closes in every projected month.

    No argument and a bool, the library-wide ``check_*`` shape;
    :func:`check_commutation_value_resid` returns the signed leak at one ``t``.
    Trivially ``True`` on a contract that never commutes, which is the base run - the
    residual is identically zero away from the month it is measured in.
    """
    return all(abs(check_commutation_value_resid(t)) < 1e-6
               for t in range(proj_len()))


def lives_if_ann(y):
    """l at the **end** of policy year y: the survival at the start of policy month 12y.

    The annual display's survival column.  Policy year ``y`` spans policy months
    ``12(y-1) .. 12y-1``, so surviving it means being alive at the start of policy month
    ``12y``, which is time ``12y - duration_mth_init()`` on the valuation clock; 0 for a
    year that ended before the contract was on the books.
    """
    t = 12 * y - duration_mth_init()
    return lives_if_last(t) if t >= t_entry() else 0.0


def claims_ann(y, kind):
    """Expected claim outgo over policy year y, by ``kind``; the notes' ``E[DB]`` at
    ``DEATH``.

    The monthly cash flows summed over the twelve months of the year, those on the books:
    on a contract in force the months of its valuation year from the valuation date on.
    Because ``CP`` is constant through a year whose premium falls at its start, this
    collapses to ``(l(y-1) - l(y)) * CP(y)`` on the annual grid - which is exactly how the
    worked example computes it.  ``ALL``, ``DIA_US_S``'s ``kind=None``, sums the months'
    totals, :func:`claims` at ``ALL``.  Each kind is a plain left-to-right sum, as at
    stage ``E``, an ulp or two from ``DIA_US_S``'s compensated ``sum`` in some years: at
    ``ALL``, in 154 of the twins' policy years at the shipped assumptions on Windows, 152
    on Linux and macOS.
    """
    d = duration_mth_init()
    entry = t_entry()
    total = 0.0
    for t in range(max(12 * (y - 1) - d, entry), max(12 * y - d, entry)):
        total += claims(t, kind)
    return total


def annuity_payments_ann(y):
    """The notes' ``E[income]``: expected income at the end of policy year y.

    An **annual-payment display approximation**, not the sum of the year's monthly
    instalments: one year's income ``B`` escalated for COLA and weighted by survival to
    the end of the year, on the count the point stands for.  The model runs monthly; this
    cells exists so that the notes' annual display table can be reproduced and asserted
    directly.  Zero in a policy year that ends before the income start month.  The income
    is the payout schedule's, ``B(T)``, level from the income start month on, and the COLA
    is read at the year's last policy month.
    """
    last = 12 * y - 1
    if last < income_start_mth():
        return 0.0
    return (policy_count() * annual_income_payout() * cola_factor_pm(last)
            * lives_if_ann(y))


def result_cf():
    """Result table of monthly cashflows, one row per month ``t = 0 ... proj_len() - 1``.

    Row 0 is the valuation month for every model point, so the frames of a block line up
    and sum row by row; a point issued after the valuation date has zeros until its issue
    month.  The columns are ``DIA_US_S``'s.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims": [claims(t, ALL) for t in ts],                  # noqa: F821
            "commutations": [commutations(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of the counts, survival probabilities and payment factors, by month t.

    One row per projected month, ``t = 0 ... proj_len() - 1``, the frame of
    :func:`result_cf`: ``pols_if``, the count on the books weighted by survival, and
    ``pols_new_biz``, the contracts issued in the month, as ``basiclife.BasicTerm_SE``'s
    ``result_pols`` sets its counts out first; then ``DIA_US_S``'s other columns in
    ``DIA_US_S``'s order, the survival read at the start of each month, as in
    ``DIA_US_S``, and every column 0 in the months before a point is issued.  The count on
    the books that weights the cash flows is not a column: it is the table's
    ``policy_count``, from issue to the stop rule.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "lives_if_1": [lives_if(t, 1) for t in ts],
            "lives_if_2": [lives_if(t, 2) for t in ts],
            "lives_if_last": [lives_if_last(t) for t in ts],
            "lives_death_last": [lives_death_last(t) for t in ts],
            "certain_floor": [certain_floor(t) for t in ts],
            "payment_factor_life": [payment_factor_life(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_annual():
    """The technical notes' annual display table, indexed by policy year.

    One row per policy year with the columns the worked example prints: the attained age
    at the start of the year, the premium received at its start, ``CP``, ``B``, the
    survival probability at the end of the year, the expected deferral death benefit
    paid during it, the expected refund, and the expected income at its end on the
    annual-payment display approximation.  The projection itself is monthly; this is the
    display grid, keyed by the policy year, ``DIA_US_S``'s key, one row per complete
    policy year to the stop rule, 60 on the anchor cell.

    A point in force at the valuation date shows the policy years from the one the
    valuation date falls in, whose row holds the months of that year from the valuation
    date on: its premium and claims are the year's on the books, and ``CP``, ``B`` and the
    survival are the year's closing values, which a year begun before the valuation date
    reaches as ``DIA_US_S`` does.  The years before it are left out, as ``Term_US_SEC``'s
    annual report leaves them out.  A point issued later starts at policy year 1.
    """
    d = duration_mth_init()
    entry = t_entry()
    ys = list(range(duration_mth(entry) // 12 + 1, stop_mth() // 12 + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "age": [age_at_entry(1) + y - 1 for y in ys],
            "premium_pp": [sum(premium_pp(t) for t in range(
                max(12 * (y - 1) - d, entry), 12 * y - d)) for y in ys],
            "cum_premium_pp": [cum_premium_pp(12 * y - 1 - d) for y in ys],
            "annual_income": [annual_income(12 * y - 1 - d) for y in ys],
            "lives_if": [lives_if_ann(y) for y in ys],
            "claims_death": [claims_ann(y, DEATH) for y in ys],      # noqa: F821
            "claims_refund": [claims_ann(y, REFUND) for y in ys],    # noqa: F821
            "annuity_payments": [annuity_payments_ann(y) for y in ys],
        },
        index=pd.Index(ys, name="policy_year"),                      # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

BEF_NB = 0

BEF_DECR = 1

DEATH = 0

REFUND = 1

ALL = 2

PRE_ISSUE = 0

DEFERRAL = 1

PAYOUT = 2

TERMINATED = 3

PURCHASE = 0

ADJUST_OLD = 1

ADJUST_NEW = 2

issue_age_min = 0

omega_age = 120

mort_table_year = 2012

mort_ae_factor = 1.0

pricing_rate = 0.0475

expense_load = 0.06

pricing_iters = 3

expense_maint = 50.0

inflation_rate = 0.025

baa_yield = 0.0575

adjust_spread = 0.01

accel_months = 6

commute_margin = 0.005

ref_rate_shift = 0.0

qlac_premium_limit = 210000.0

qlac_max_start_age = 85

pd = ("Module", "pandas")