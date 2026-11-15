# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.SPIA_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.SPIA_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is: ``Projection[15]``
is an ItemSpace projecting the table's sixteenth row, model point 16, the worked-example
anchor cell in payment 14 months at the valuation date, its joint annuitant already dead,
and :func:`point_id` is its label::

    >>> Projection[15].result_cf()         # one row per month from the valuation date
    >>> Projection[15].result_pols()       # the counts and survival behind it
    >>> Projection[15].point_id()          # 16, the row's point_id
    >>> Projection.idx = 7                 # or switch the default, before it computes

Switch the default, or set any Reference, before the model computes anything. Compiled, no
cache is ever cleared: set ``idx``, like every Reference, on a model just imported, before
anything is computed, or project through ``Projection[i]``. modelx recomputes what a
Reference reaches when it is set; a compiled ItemSpace takes the References when it is
made and keeps every value it has computed until it is deleted, and the base
``Projection`` and ``Data`` keep theirs for good. And it holds each Reference as a C
variable of its shipped value's type: a float set on an int Reference truncates toward
zero, an int set on a float Reference reads as a float, and text cannot be set on
``commute_disc_convention``, an int code, at all, where modelx takes it and
:func:`is_disc_compound` refuses it (``products/immediate_annuity/model-sec.md``).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.SPIA_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.SPIA_US_S` is rewritten where it depends on where the projection starts, where it
must answer for a month outside the frame, where it passed a policy month as ``t``, or
where it branched on text; every other is :mod:`~.SPIA_US_S`'s own.
``products/immediate_annuity/model-sec.md`` lists the rewritten cells with the reason for
each. Making it compile changed how each cell reads its inputs and spells its codes, and
no number: every model point attribute a projection cell uses is read as a number from a
``Data`` vector, each text column it branches on as ``Data``'s decoded flags, the two age
tables as arrays by sex and age, every timing and kind and the commutation discount
convention as an int code (*Codes*, below), and :mod:`~.SPIA_US_S`'s
``claims(t, kind=None)``, whose one kind is its total, is :func:`claims` of ``t`` alone.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/immediate_annuity/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``SPIA_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.SPIA_US_SEC.Data`. The three assumption tables are the files :mod:`~.SPIA_US_S`
reads, read in place; the model point table is this model's own:

========================  ==================================  ==========================
Reference                 Cells                               File
========================  ==================================  ==========================
model_point_file          data.model_point_table()            model_point_table_sec.csv
mort_table_file           data.mort_table()                   mort_table.csv
improvement_scale_file    data.improvement_scale()            improvement_scale.csv
surr_charge_file          data.surr_charge_table()            surr_charge_table.csv
========================  ==================================  ==========================

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however long the contract has been in payment, month ``t`` runs from time ``t``
to time ``t + 1``, and the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len`
counts the months from the valuation date to the stop rule. Row ``t`` is the same month
for every point, so the frames of a block line up and sum row by row. Three cells are
indexed by a **time point** on this clock rather than by a month: ``lives_if(t, life)``
and ``lives_if_last(t)``, survival *at* time ``t``, and ``check_lives_roll_fwd_resid(t)``.
Time ``t`` is the start of month ``t``, so month ``t`` opens at time ``t`` and closes at
time ``t + 1``, which is why the death density of month ``t`` is ``l(t) - l(t + 1)`` and
the arrears survival point is ``t + 1``, as in :mod:`~.SPIA_US_S`.

``duration_mth(t)`` counts **policy months**, the months elapsed from the annuity date at
the start of month ``t``: ``duration_mth(t) = duration_mth_init() + t``, where
:func:`duration_mth_init` is read from the model point — positive for a contract already
in payment at the valuation date, 0 for one whose annuity date is the valuation date,
``-k`` for one commencing ``k`` months later, at most ten years later. It is the technical
notes' month index, and everything contractual reads it: the completed policy years
``duration(t) = duration_mth(t) // 12``, the contractual 1-based label
``policy_year(t) = duration(t) + 1``, the attained ages ``age(t, life)``, and through them
the payment months, the COLA anniversaries, the certain period, the commutation months
and the surrender-charge scale. A cell keyed directly by this clock takes ``k``, never
``t``: :func:`is_payment_pm` and :func:`annuity_pp_sched_pm` are keyed by the policy month
``k``, and :func:`cum_annuity_pp` by the time point ``k`` months after the annuity date,
so that its ``G(13)`` reads as the notes write it. The anchor cell in payment 14 months,
point 16, is in policy year 2 at ``t = 0``, its joint annuitant dead since the end of
policy month 13, and it reaches its next COLA anniversary, policy month 24, at
``t = 10``.

The **stop rule** ends every frame where it ends :mod:`~.SPIA_US_S`'s: :func:`stop_mth` is
:mod:`~.SPIA_US_S`'s frame length from the annuity date, the age stop on the youngest
covered life or the end of the certain period if that is later, and :func:`is_active` is
``0 <= duration_mth(t) < stop_mth()``. A contract's own end, its last death or its last
certain instalment, is a probability or a floor reaching zero inside the frame, which runs
on with zeros, as :mod:`~.SPIA_US_S`'s does.

Two inputs, and their clocks. Expense inflation reads the **valuation** clock,
``inflation_factor(t) = (1 + inflation_rate) ** (t // 12)``, :mod:`~.SPIA_US_S`'s annual
steps moved onto ``t``, so that the maintenance charge is in valuation-date dollars for
every point alike. Mortality improvement stays on the **policy** clock, because it is
already calendar-dated: its exponent is ``calendar_year(t) - mort_table_year``, and
``calendar_year(t) = annuity_year() + duration(t)`` is the calendar year the contract
reaches whatever the valuation date, so a contract in payment reads the improvement of its
own calendar years and nothing is re-based. The commutation discount rate is level and
reads neither clock. It moves with the 10-year CMT's change since the annuity date, on one
path every point shares: for a contract on the books at the valuation date, the change to
that date, which a contract in payment carries in its opening state, plus
``cmt10_shift``, a change made at the valuation date; for a contract commencing later,
bought after that change, none.

On a point whose annuity date is the valuation date the two clocks coincide and this model
computes what :mod:`~.SPIA_US_S` computes: every cell the two share agrees at every
argument :mod:`~.SPIA_US_S` evaluates in its sweep, but for three whose meaning changed,
``pols_if_init``, now the count already in payment at the valuation date, ``model_point``,
a row of another table, and ``result_pols``, which gains the month's new business. That is
how the worked example carries over, and ``tests/test_model_conventions.py`` asserts it
cell by cell.

.. rubric:: Counts

The count on the books is the number of contracts the point stands for,
:func:`policy_count`, from the annuity date to the stop rule. Mortality decrements each
life's survival, :func:`lives_if`, never the count: the two lives are independent, so their
two probabilities are the whole survival state, and every cash flow is the count times a
per-contract amount weighted by survival, as :mod:`~.SPIA_US_S` weights every flow by its
constant ``pols_if_init``. So ``pols_if_at(t, BEF_NB)`` is :func:`pols_if_init`, the count
already in payment, at :func:`t_entry`, the first month on the books, the whole count after
it, and 0 outside the frame; and ``pols_if_at(t, BEF_DECR)`` adds :func:`pols_new_biz`,
the annuities commencing in month ``t``. The ``BEF_DECR`` count weights every cash flow
of row ``t``. A contract in payment at the valuation date opens with its ``policy_count``;
one commencing at or after it opens with none, and takes its ``policy_count`` as new
business in the month of its annuity date, ``duration_mth(t) = 0``. New business brings no
premium and no acquisition cost: the single premium is a pricing input, as in
:mod:`~.SPIA_US_S`.

:func:`pols_if` keeps :mod:`~.SPIA_US_S`'s definition, the notes' obligation measure
``IF(t)``, on that count: ``pols_if_at(t, BEF_DECR) * max(C(t), l_alive(t+1))``, the
contracts with a payment obligation still open at the end of month ``t``, which carries
the maintenance expense. It is a closing measure, not the count before decrements: on the
anchor cell's twin, point 8, ``pols_if(0)`` is 0.99999986 against a count of 1.0, as in
:mod:`~.SPIA_US_S`, and the registry marks the model ``closing_pols_if`` for that reason.
There is no lapse decrement, and no ``pols_lapse``.

.. rubric:: The opening state

A contract in payment at the valuation date carries three things its count and its policy
clock do not say. Each is read from its model point as it stands at the start of month
0, before any month-0 event:

``lives_if_init_1``, ``lives_if_init_2``
    each covered life's probability of being alive at the valuation date,
    :func:`lives_if_init`. On a real record it is 1 or 0, and a joint contract may carry
    one life already dead; on a point restated from :mod:`~.SPIA_US_S` at its month
    ``d`` it is :mod:`~.SPIA_US_S`'s ``lives_if(d, life)``, a probability. The lives are
    independent, as in :mod:`~.SPIA_US_S`, so the two per-life probabilities are the
    whole survival state. Life 2 is 0 on a single-life contract.
``commute_frac_cum_init``
    the cumulative commutation fraction applying in month 0, before any month-0
    withdrawal, :func:`commute_frac_cum_init`: path-dependent, because it records the
    withdrawals the owner has taken.
``cmt10_shift_init``
    the 10-year CMT at the valuation date less the 10-year CMT at the annuity date,
    :func:`cmt10_shift_init`: the part of the change since purchase, which moves the
    commutation discount rate one for one, that the contract has already seen. The CMT's
    path began before ``t = 0``, so its value at the start of the contract's term is
    opening state, as for any point-to-point quantity on a market path; it is a fact of
    the market, the same for two contracts with one annuity date.

At the annuity date each covered life is 1, the fraction 0 and the CMT's change 0, so a
point commencing at or after the valuation date carries those values. Nothing else carries
a path. The certain
months left follow from ``duration_mth``, because :func:`certain_floor` compares the
policy month with the certain period, which is static. The payments to date, ``G``, are a
deterministic schedule: :func:`cum_annuity_pp` stays on the policy clock and sums them from
the annuity date, with one loop at the valuation date's policy month, so that the refund
of an old cash refund does not recurse as deep as the contract is old.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for contract counts, plural nouns
for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claim_pp(t, kind)`` with an uppercase ``kind`` code, ``result_cf()`` for the cash flow
table. What running in force adds is named as ``basiclife.BasicTerm_SE`` names it:
``duration_mth`` read from the model point, ``policy_count``, ``pols_new_biz``,
``pols_if_at`` with its ``BEF_NB`` and ``BEF_DECR`` timings, ``is_active`` and
``result_pols``; and what compiling adds as ``basiclife.BasicTerm_SC`` names it,
``point_id``, the label of the point at ``idx``. ``duration_mth_init``, the policy months
completed at the valuation date, takes ``UL_US_S``'s name, and each opening-state column
is ``<cell>_init``, the cell it opens with ``_init`` added, read per life by
``lives_if_init(life)``. ``t_entry`` and
``stop_mth`` are the SEC family's own. A cell keyed by policy month carries ``_pm``,
beside the ``_py`` that ``Term_US_SEC`` gives a policy-year key, and a table reader keyed
by attained age carries ``_at``, beside the ``_schedule`` that gives it the table's row
for a life's sex. The ``is_*`` decodes turn the model point's text columns into the flags
the projection branches on, each reading ``Data``'s decoded flag and refusing a value
:mod:`~.SPIA_US_S`'s label accessor refuses, with its message, so that no projection cell
compares text and none calls a label accessor (``form``, ``sex``, ...), which is left to
reporting. The technical notes use compact actuarial symbols instead. The mapping is:

========================  =================================  ===============================
Notes symbol              Cells                              Meaning
========================  =================================  ===============================
t                         (the cells argument)               Month from the valuation date,
                                                             0-based; time t opens month t
k                         (the cells argument)               Policy month, or the time point
                                                             opening it, from the annuity
                                                             date
(month index)             duration_mth(t)                    Months from the annuity date at
                                                             the start of month t
(none)                    duration_mth_init()                Months in payment at the
                                                             valuation date; -k if the
                                                             annuity commences k months on
y(t) = duration(t) + 1    policy_year(t)                     Policy year containing month t
(none)                    duration(t)                        Completed policy years at
                                                             month t
(none)                    t_entry()                          First month on the books
(stopping rule)           stop_mth()                         Policy month the frame stops at
(none)                    is_active(t)                       Whether month t is in the frame
m                         payment_freq()                     Payments per year
timing                    payment_timing()                   arrears (default) or advance
(none)                    is_arrears()                       timing decoded: arrears or not
T                         is_payment_mth(t)                  Month t is a payment date
(T by policy month)       is_payment_pm(k)                   Policy month k is a payment
                                                             date
(payment point)           payment_surv_mth(t)                Time survival is measured at
P                         premium_pp()                       Single premium
tau                       premium_tax_rate()                 State premium tax rate
P_net                     premium_net_pp()                   P(1 - tau), the amount
                                                             annuitized
B(y)                      annual_income(y)                   Unreduced annualized income
B(1)                      annual_income_first()              Income in policy year 1
inst(t)                   annuity_pp(t)                      Instalment per contract payable
(inst, untrimmed)         annuity_pp_sched(t)                Scheduled instalment before
                                                             trim
(inst by policy month)    annuity_pp_sched_pm(k)             The same, in policy month k
g                         cola_rate()                        Fixed compound COLA rate
delta                     survivor_pct()                     Survivor percentage
trig                      reduction_trigger()                either / primary
(none)                    is_trigger_either()                trig decoded: either or not
form                      form()                             Payout form, one of five
(none)                    is_period_certain()                form decoded: an elected
                                                             certain period
(none)                    is_certain_only()                  form decoded: certain_only
(none)                    is_cash_refund()                   form decoded: cash_refund
(none)                    is_installment_refund()            form decoded: installment
                                                             refund
n                         certain_mths()                     Elected certain months
n_R                       certain_mths_refund()              Derived installment-refund
                                                             months
n_eff                     certain_mths_eff()                 Effective certain months by
                                                             form
joint                     is_joint()                         Contract covers two lives
x1, x2                    age_at_entry(life)                 Issue ages (ANB), life = 1 or 2
(none)                    age(t, life)                       Attained age (ANB)
(none)                    sex(life)                          Sex of each covered life
(none)                    mort_schedule(life)                Each life's row of the
                                                             mortality table
(none)                    improvement_schedule(life)         Each life's row of the
                                                             improvement scale
l_i(t)                    lives_if(t, life)                  Survival probability to time t
l_i(t_entry)              lives_if_init(life)                Survival at the valuation
                                                             date, or at the annuity date
                                                             if later
d_i(t)                    lives_death(t, life)               Death density of month t
l_last(t)                 lives_if_last(t)                   At least one covered life alive
d_last(t), d_term(t)      lives_death_last(t)                Last-death density of month t
L(t)                      payment_factor_life(t)             Life-contingent payment factor
C(t)                      certain_floor(t)                   Certain floor
                                                             1{duration_mth(t) < n_eff}
Phi(t)                    payment_factor(t)                  max(C(t), L(t))
G(k)                      cum_annuity_pp(k)                  Instalments scheduled before
                                                             time k from the annuity date
IF(t)                     pols_if(t)                         Obligation open at end of
                                                             month t
(none)                    policy_count()                     Contracts the point stands for
(none)                    point_id()                         The point's label in the table
(none)                    pols_if_init()                     Contracts in payment at the
                                                             valuation date
(none)                    pols_if_at(t, timing)              Contracts on the books at time
                                                             t, BEF_NB or BEF_DECR
(none)                    pols_new_biz(t)                    Annuities commencing in month t
(none)                    annuity_year()                     Calendar year of the annuity
                                                             date
(none)                    calendar_year(t)                   Calendar year containing
                                                             month t
q_x (table)               mort_rate_base(t, life)            Base-table annual mortality
                                                             rate
(q_x by age)              mort_rate_base_at(x, life)         The same, at attained age x
G2_x                      improvement_rate(t, life)          Generational improvement rate
(G2_x by age)             improvement_rate_at(x, life)       The same, at attained age x
AE                        mort_ae_factor                     A/E factor, 1.084 **[std]**
theta                     rating_factor()                    Substandard multiplier
q_rated(x, cal)           mort_rate(t, life)                 Annual rate after AE and theta
q_m(t)                    mort_rate_mth(t, life)             Monthly rate 1-(1-q)^(1/12)
(none)                    mort_basis()                       table or scenario run **[std]**
(none)                    is_scenario()                      mort_basis decoded: scenario
(none)                    death_mth(life)                    Scenario policy month of death
                                                             **[std]**
omega                     omega_age                          Limiting age, 120
(stopping rule)           horizon_mths()                     Policy months before the age
                                                             stop rule
(none)                    proj_len()                         Months from the valuation date
                                                             to the stop rule
(inst after commutation)  annuity_pp_paid(t)                 inst(t)*(1 - theta_cum*C)
E[ANN(t)]                 annuity_payments(t)                Expected annuity outgo
E[CR(t)]                  claims(t)                          Cash-refund lump sum
(per contract)            claim_pp(t, kind)                  Refund amount per contract
E[COMM(t)]                commutations(t)                    Commutation paid to the owner
E[EXP(t)]                 expenses(t)                        Maintenance expense
CF(t)                     liability_cf(t)                    Total gross liability outgo
(none)                    net_cf(t)                          -liability_cf(t), insurer sign
commutation_enabled       commutation_enabled()              Contract has the withdrawal
                                                             right
(same name)               issue_state_excludes_withdrawal()  Oregon bars the withdrawal
qualified                 qualified()                        Qualified money; inert here
(none)                    commute_elig(t)                    Withdrawal allowed in month t
CV(t)                     commuted_value(t)                  Commuted value of certain tail
j(t)                      commute_disc_rate(t)               Commutation discount rate
j0                        commute_disc_rate_base             Base commutation rate, 4.00%
(none)                    is_disc_compound()                 commute_disc_convention
                                                             decoded: compound or not
CMT10(t) - CMT10(0)       cmt10_shift_init() + cmt10_shift   10-yr CMT change since issue:
                                                             to the valuation date, then
                                                             at it; none for an annuity
                                                             commencing later
sc(y)                     surr_charge_rate(y)                Surrender charge rate
sc(y) x W                 surr_charge(t)                     Surrender charge retained
W                         commute_amount(t)                  Gross withdrawal requested
theta_cum(t)              commute_frac_cum(t)                Cumulative commutation
                                                             fraction
theta_cum(t_entry)        commute_frac_cum_init()            The same at the valuation
                                                             date, or at the annuity date
                                                             if later
u(y)                      commute_util_rate(y)               Commutation utilization
                                                             **[std]**
c_e                       expense_maint                      Maintenance expense p.a.
pi                        inflation_rate                     Expense inflation
(1+pi)^(t//12)            inflation_factor(t)                Expense inflation factor, on
                                                             the valuation clock
========================  =================================  ===============================

Every attribute of the notes' *Model point attributes* table has a row above, and so do
the model's own additions, which the notes give no symbol but which drive the
generational basis, the verification anchor, the commutation eligibility test and the
in-force projection: ``annuity_year``, ``calendar_year``, ``mort_basis``, ``death_mth``,
``commute_elig``, the counts and the clock. Only the outputs and diagnostics are left out
— :func:`result_cf`, :func:`result_pols`, :func:`check_lives_roll_fwd` /
:func:`check_lives_roll_fwd_resid` and :func:`check_payment_factor` /
:func:`check_payment_factor_resid` — because they are not quantities the notes define.
Most model point attributes keep the notes' own name; ``issue_state_excludes_withdrawal``
is one of them and is entered as ``(same name)`` only because it is too wide for the first
column.

Six names in that table needed care.

``l`` and ``L`` differ in the notes only by case — survival probability versus the
life-contingent payment factor — so they become ``lives_if`` and
``payment_factor_life``. Likewise ``G(k)``, cumulative instalments, collides with
``G2_x``, the improvement scale: ``cum_annuity_pp`` and ``improvement_rate``. And
``theta`` is used twice, once as the substandard mortality multiplier and once as
``theta_cum``, the cumulative commutation fraction: ``rating_factor`` and
``commute_frac_cum``.

``t`` and ``k`` both count months, on the two clocks: ``t`` from the valuation date and
``k`` from the annuity date, and ``k = duration_mth(t)`` is the same instant. Survival,
which the projection carries forward from the valuation date, is indexed by ``t``, and so
is every monthly cell; the schedule, which the contract fixes from the annuity date,
is indexed by ``k``, and so are the payments to date that sum it. :mod:`~.SPIA_US_S`
names the time point of its ``lives_if`` ``k`` as well, on its one clock; here that cell
is on the valuation clock and its argument is ``t``.

``d_term(t)`` is not a separate quantity. The notes define it as ``d_1`` on a
single-life contract and ``d_last`` on a joint one; because :func:`lives_if_last`
returns ``l_1`` when the contract is single-life, ``lives_death_last`` *is* ``d_term``
in both cases and no second cells is needed.

``CF(t)`` needs one sentence of warning. The notes define
``CF(t) = E[ANN] + E[CR] + E[COMM] + E[EXP]``, an outgo-positive total, and that is
:func:`liability_cf`. But the **CF column of the worked-example table is the annuity
instalment alone** — at ``t = 0`` it shows 500.00, not the 505.00 that the definition
gives once the $5.00 monthly maintenance expense is added. The worked example is
therefore asserted against :func:`annuity_payments`, and :func:`net_cf` carries the
house sign convention of ``Term_US_S`` (income less outgo, so ``-liability_cf``). Both
signs are published as columns of :func:`result_cf`, the notes' outgo-positive total
under ``liability_cf`` and the library-wide income-positive one under ``net_cf``.

The two self-checks follow the library convention: :func:`check_lives_roll_fwd` and
:func:`check_payment_factor` take **no argument and return a bool** covering every
projected month, so one test can call the same no-arg check across every model in the
library. The signed per-month residual — the more useful object once a check fails —
stays available as :func:`check_lives_roll_fwd_resid` and
:func:`check_payment_factor_resid`, and each boolean is implemented in terms of its own
residual.

.. rubric:: Two mortality bases: table and scenario

The notes' worked example is not a probability-weighted run. It is a **scenario**: "the
joint (secondary) annuitant dies during month 14" — the fourteenth month from the annuity
date, policy month 13 on the 0-based grid — "the primary survives throughout",
evaluated at ``l_1 = 1``, ``l_2 = 0``. The notes' *Model points* section, by contrast,
projects "on an expected (probability-weighted) basis". Both readings are shipped, and
which one applies is a model point column:

``mort_basis = "table"``
    ``lives_if`` runs the notes' generational recursion off the shipped mortality and
    improvement tables, forward from the opening state. Model points 7, 8, 9, 12 and 15,
    and of the points restated in payment or commencing later, 20, 21 and 22; point 8 is
    the anchor cell on this basis and is the run to read for a realistic cash flow shape.

``mort_basis = "scenario"`` **[std]**
    ``lives_if(t, life)`` is the deterministic step function
    ``1{duration_mth(t) <= death_mth(life)}`` on the policy clock: the life is alive at
    every time point up to the start of its month of death, and dead from the end of that
    month on, with a blank ``death_mth`` meaning the life survives the whole projection.
    Model points 1-6, 10, 11, 13 and 14, which reproduce the worked example and its
    traces exactly, and 16 to 19, restated from them in payment.

The scenario switch is a **[std]** modelling device, not a product feature; it exists
because the notes' verification anchor is a scenario and retuning assumptions to force a
probability-weighted run onto it would be dishonest.

.. rubric:: The certain period is a floor, not a second stream

``payment_factor(t) = max(certain_floor(t), payment_factor_life(t))`` is the single most
important line in the model and the notes' first listed pitfall. During the certain
period the full, *unreduced* instalment is payable regardless of survival; an additive
construction would pay ``1 + L`` and silently double the guarantee. The ``max`` also
reproduces, with no extra logic, one carrier's rule that a survivor reduction inside a
certain period is deferred to the end of that period [S5] — see model point 5, where the
reduction to ``delta`` begins at policy month 120 and not at the death in policy month 13,
and point 18, the same contract in payment 120 months, where it begins at ``t = 0``.

.. rubric:: ``certain_only``, where the notes' expense formula outlives the contract

The notes carry the maintenance expense on ``IF(t) = max(C(t), l_alive(t+1))`` and, in the
same table, describe it as paid *"while any payment obligation remains"*. The two agree
on the four life-contingent forms. They do not agree on ``certain_only``, where the notes
also set ``L(t) = 0``: the last instalment falls in policy month ``n_eff - 1`` and nothing
is owed afterwards, but ``l_alive`` is a survival probability, not a payment factor, and
stays positive for the annuitant's whole remaining lifetime. Read literally the formula
keeps billing a contract that ended years earlier. :func:`pols_if` follows the prose and
drops the life-contingent leg on ``certain_only`` — the one form with no life contingency
in it — so ``IF(t) = C(t)`` there and ``max(C(t), l_alive(t+1))`` on every other form.
Model point 15 exercises it; no other form and no other model point moves.

.. rubric:: Survival-measurement and refund-balance timing

Two timing conventions move the liability by one payment period each and are wired to
the same switch, ``timing``:

- an **arrears** instalment falling at the end of month ``t`` requires survival to time
  ``t + 1``; an **advance** instalment falls at the *start* of month ``t``, which is time
  ``t``, so survival is measured one full month earlier whatever the frequency. That is
  :func:`payment_surv_mth`, which returns a **time point**, not a month. The notes write
  the advance point as ``t + 1 - 12/m``, one full payment period earlier than the arrears
  point ``t + 1`` — but that measures from the **arrears** month of the same instalment,
  which falls one payment period later than the advance month. :func:`is_payment_pm`
  indexes an advance instalment by the policy month it falls *in* (``0, 3, 6, …`` at
  ``m = 4``), so the start of month ``t`` is the reading that holds at every frequency;
  the two agree at ``m = 12``, the only frequency the notes spell out.
- the cash-refund balance nets instalments *already paid*: ``G(m)`` on arrears, where
  ``m = duration_mth(t)`` — with ``G`` indexed by a time point on the policy clock,
  everything paid before month ``t`` opened — but ``G(m + 1)`` in an advance payment
  month, because an instalment paid at the start of the month of death has been paid.
  That is :func:`claim_pp`.

Deaths are decremented at end of month, so a survivor reduction takes effect **from the
instalment due at the end of the month of death** — which is why the worked example's
trigger split bites at policy month 13, the month of the death, and not at 14.

.. rubric:: Codes

What :mod:`~.SPIA_US_S` spells as text, a timing, a kind or the commutation discount
convention, is here an int Reference named as the text it replaces, so that every cell
takes and returns C numbers. A call site reads as it did, less the quotes:
``pols_if_at(t, BEF_DECR)``, ``claim_pp(t, REFUND)``.

=============  =====  ===============================================================
Reference      Value  Meaning
=============  =====  ===============================================================
BEF_NB         0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR       1      :func:`pols_if_at`: that count plus month t's new business
REFUND         0      :func:`claim_pp`: the cash refund, the one kind
COMPOUND       0      ``commute_disc_convention``: compound discounting, the default
SIMPLE         1      ``commute_disc_convention``: simple discounting, per [S7]
=============  =====  ===============================================================

The timings are numbered by instant, ``BEF_NB`` 0 and ``BEF_DECR`` 1, as in every SEC
model, and a code a cell takes indexes that cell's cache, a C array three codes wide for
each of the two cells that take one, since every 2-D cache of the model has the width
of the lives' (``spec_sec.py``), so codes are numbered densely from 0. ``COMPOUND`` and
``SIMPLE`` are the values ``commute_disc_convention`` holds, ``COMPOUND`` as shipped,
where :mod:`~.SPIA_US_S` holds ``"compound"`` or ``"simple"``; :func:`is_disc_compound`
refuses any other. They are References, not cells, so the symbol map does not list them.
Every other Reference is named in lower case, ``issue_age_min`` and ``omega_age``
among them, the contract's bounds that :func:`proj_len` checks and that the compiled
model's caches are sized from, with ``Data.future_horizon_mth``.

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`form`, :func:`reduction_trigger`,
:func:`payment_timing`, :func:`mort_basis` and :func:`sex`, the reports :func:`result_cf`
and :func:`result_pols`, and the checks :func:`check_lives_roll_fwd` and
:func:`check_payment_factor` are written for a reader and for the comparison with
:mod:`~.SPIA_US_S`, which has every one of them: a table row, text, DataFrames and two
verdicts. No other cell calls them: each reads the number ``Data`` decoded from the same
column instead, the decodes' flags and the schedules the sexes select. So the row, the
text and the frames stay Python when the model compiles. Each label returns its point's
column: ``form``, ``reduction_trigger`` and ``mort_basis`` the column of their own name,
``payment_timing`` the ``timing`` column and ``sex(life)`` the ``primary_sex`` or
``joint_sex`` column by life, as the registry declares them. The first four validate
their column, as :mod:`~.SPIA_US_S`'s do, so each returns text or raises; ``sex`` returns
its column as read, text or not, a blank second life on a single-life contract as NaN,
and the compiled accessor returns the same. Every other cell returns a C ``bint``,
``long long`` or ``double``, and so do the two checks, which may stay Python but compile
to a ``bint``, their verdict, as their per-month residuals, ``*_resid``, compile to a
``double``.
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


def premium_pp():
    """P: the single premium of the selected model point.

    A pricing input at the annuity date, not a projected cash flow: the projection carries
    no premium income, for a contract commencing after the valuation date as for one
    already in payment.  It enters the projection only through the refund forms, where the
    guarantee is measured against it.

    Read from ``Data.premium``.  A premium that is not a number is refused here, naming
    the point, as ``SPIA_US_S``'s ``float()`` refuses it; so is a blank or infinite one on
    a cash or installment refund, whose refund balance ``max(0, P - G)`` and refund period
    ``G(k) >= P`` would read it as a number (``Data``'s ``premium_ok``).  On the other forms
    a blank is NaN, as in ``SPIA_US_S``.
    """
    if data.premium_ok()[idx] == 0:                                  # noqa: F821
        raise ValueError(f"point_id {point_id()}: premium must be a number, and a finite "
                         f"one on a cash or installment refund, which reads it; it is "
                         f"not")
    return float(data.premium()[idx])                                # noqa: F821


def premium_tax_rate():
    """tau: the state premium tax rate deducted before income is determined **[std]**.

    Zero in the base run; no source quantifies a rate [S6][S7][S11].  Read from
    ``Data.premium_tax_rate``; text is refused here, naming the point, and a blank is NaN,
    as in ``SPIA_US_S``.
    """
    if data.premium_tax_rate_ok()[idx] == 0:                         # noqa: F821
        raise ValueError(f"point_id {point_id()}: premium_tax_rate must be a number or "
                         f"blank; it is not")
    return float(data.premium_tax_rate()[idx])                       # noqa: F821


def premium_net_pp():
    """P_net = P(1 - tau), the amount annuitized [S6][S7][S11].

    Reported for completeness.  Because ``B(1)`` is exogenous - no insurer publishes
    payout factors, so the model does not derive income from premium - nothing in the
    projection consumes it.
    """
    return premium_pp() * (1.0 - premium_tax_rate())


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in payment at the valuation date counts the contracts in payment then, before
    any month-0 event; any other point counts the annuities it commences.  Either way the
    count enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the month the annuity commences for the second.  It is
    ``SPIA_US_S``'s ``pols_if_init`` column, renamed, and like it a constant on the books:
    mortality decrements each life's survival, :func:`lives_if`, never the count.  Read
    from ``Data.policy_count``.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """Contracts in payment at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in payment at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one commencing at or after it, whose
    contracts enter through :func:`pols_new_biz` in the month the annuity commences
    instead, as in ``basiclife.BasicTerm_SE``.  So on a point commencing at ``t = 0`` this
    is 0, where ``SPIA_US_S``'s is the count itself; on either model the count that weights
    row 0 is the same, here ``pols_if_at(0, BEF_DECR)``.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def form():
    """The payout form: one of the five forms of [S1][S2][S4][S5].

    life_only, life_certain, cash_refund, installment_refund, certain_only.  A label
    accessor, which no projection cell calls: it returns the ``form`` column, compared
    exactly, or raises.
    """
    v = model_point()["form"]
    if v not in ("life_only", "life_certain", "cash_refund",
                 "installment_refund", "certain_only"):
        raise ValueError("invalid form")
    return v


def is_period_certain():
    """Whether the form has an elected certain period: life_certain or certain_only.

    One of four decodes of the model point's ``form`` column, as are the three below it,
    so that no projection cell compares text or calls :func:`form`, the label accessor,
    which is left to reporting.  Each reads ``Data``'s flag for its value, and
    ``Data.has_form``, which says whether the column holds one of the five values
    :func:`form` accepts, compared as :func:`form` compares them, so an invalid form raises
    ``ValueError("invalid form")`` wherever the projection first meets it.
    """
    if data.has_form()[idx] == 0:                                    # noqa: F821
        raise ValueError("invalid form")
    return bool(data.is_period_certain()[idx])                       # noqa: F821


def is_certain_only():
    """Whether the form is certain_only: an annuity certain, with no life contingency.

    A decode of the ``form`` column, validated as :func:`form` validates it.
    """
    if data.has_form()[idx] == 0:                                    # noqa: F821
        raise ValueError("invalid form")
    return bool(data.is_certain_only()[idx])                         # noqa: F821


def is_cash_refund():
    """Whether the form is cash_refund: a lump sum of ``P - G`` on the terminating death.

    A decode of the ``form`` column, validated as :func:`form` validates it.
    """
    if data.has_form()[idx] == 0:                                    # noqa: F821
        raise ValueError("invalid form")
    return bool(data.is_cash_refund()[idx])                          # noqa: F821


def is_installment_refund():
    """Whether the form is installment_refund: a certain period derived from ``P``.

    A decode of the ``form`` column, validated as :func:`form` validates it.
    """
    if data.has_form()[idx] == 0:                                    # noqa: F821
        raise ValueError("invalid form")
    return bool(data.is_installment_refund()[idx])                   # noqa: F821


def is_joint():
    """True when the contract covers two annuitants: ``bool()`` of the ``joint`` column,
    from ``Data.is_joint``."""
    return bool(data.is_joint()[idx])                                # noqa: F821


def age_at_entry(life):
    """x_i: issue age (ANB) of the primary (life = 1) or joint (life = 2) annuitant.

    Age nearest birthday **[std]**: one carrier defines contract age as ANB [S1] and the
    2012 IAM/IAR family is tabulated ANB [R2][R9].  The age at the annuity date, which
    ``SPIA_US_S`` collapses onto the issue date, and not at the valuation date:
    ``age(0, life)`` is the attained age then.

    Read from ``Data.primary_age`` and ``Data.joint_age``, ``int()`` of the column, so a
    fraction truncates as in ``SPIA_US_S``.  An age ``int()`` cannot read, text or a blank,
    or one of ``2**53`` or more in size, is refused here, naming the point: a single-life
    contract's blank ``joint_age``, which no projection reads, only by a direct call.
    :func:`proj_len` refuses an issue age the contract does not cover.
    """
    if life == 1:
        if data.primary_age_ok()[idx] == 0:                          # noqa: F821
            raise ValueError(f"point_id {point_id()}: primary_age must be a number int() "
                             f"reads, below 2**53 in size; it is not")
        return int(data.primary_age()[idx])                          # noqa: F821
    if life == 2:
        if data.joint_age_ok()[idx] == 0:                            # noqa: F821
            raise ValueError(f"point_id {point_id()}: joint_age must be a number int() "
                             f"reads, below 2**53 in size; it is not")
        return int(data.joint_age()[idx])                            # noqa: F821
    raise ValueError("invalid life")


def sex(life):
    """Sex (M / F) of the primary (life = 1) or joint (life = 2) annuitant.

    A label accessor, which no projection cell calls: it returns the ``primary_sex`` or
    ``joint_sex`` column as read, a single-life contract's blank second life as NaN.  The
    two age readers join on the sex through :func:`mort_schedule` and
    :func:`improvement_schedule` instead.
    """
    if life == 1:
        return model_point()["primary_sex"]
    if life == 2:
        return model_point()["joint_sex"]
    raise ValueError("invalid life")


def survivor_pct():
    """delta: the survivor percentage, in {0.50, 2/3, 0.75, 1.00} [S1][S2][S5][S6][S7].

    Read from ``Data.survivor_pct``.  Text is refused here, naming the point, and so is a
    blank or infinite percentage on a joint contract with a life contingency, the one
    reader, whose payment factor's ``max(C, L)`` would read it as a number
    (``Data``'s ``survivor_pct_ok``).
    """
    if data.survivor_pct_ok()[idx] == 0:                             # noqa: F821
        raise ValueError(f"point_id {point_id()}: survivor_pct must be a number, and a "
                         f"finite one on a joint contract with a life contingency, which "
                         f"reads it; it is not")
    return float(data.survivor_pct()[idx])                           # noqa: F821


def reduction_trigger():
    """trig: whether the reduction is triggered by *either* death or the *primary*'s.

    A switch, not a parameter: the two conventions coincide on the primary's death and
    differ only on the secondary's [S1][S2][S3][S7].  A label accessor, which no
    projection cell calls.
    """
    v = model_point()["reduction_trigger"]
    if v not in ("either", "primary"):
        raise ValueError("invalid reduction_trigger")
    return v


def is_trigger_either():
    """Whether either death triggers the survivor reduction, not the primary's alone.

    A decode of the model point's ``reduction_trigger`` column, ``Data.is_trigger_either``,
    validated by ``Data.has_reduction_trigger`` as :func:`reduction_trigger` validates it,
    so that :func:`payment_factor_life` branches on a flag and no projection cell calls the
    label accessor, which is left to reporting.
    """
    if data.has_reduction_trigger()[idx] == 0:                       # noqa: F821
        raise ValueError("invalid reduction_trigger")
    return bool(data.is_trigger_either()[idx])                       # noqa: F821


def certain_mths():
    """n: the elected certain period in months, 0 or 60-360 [S1][S2][S4][S5].

    Read from ``Data.certain_months``, ``int()`` of the column; one ``int()`` cannot read,
    or of ``2**53`` or more in size, is refused here, naming the point.  Only a form with
    an elected certain period reads it, so a blank elsewhere is refused only by a direct
    call.  :func:`proj_len` refuses a period longer than the caches hold.
    """
    if data.certain_months_ok()[idx] == 0:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: certain_months must be a number int() "
                         f"reads, below 2**53 in size; it is not")
    return int(data.certain_months()[idx])                           # noqa: F821


def payment_freq():
    """m: payments per year, in {12, 4, 2, 1} [S1][S2].

    Read from ``Data.frequency``, ``int()`` of the column, so 12.5 is monthly, as in
    ``SPIA_US_S``; one ``int()`` cannot read, or of ``2**53`` or more in size, is refused,
    naming the point, and any other number raises ``SPIA_US_S``'s
    ``ValueError("invalid frequency")``.  The element is compared, never held in a local,
    so the compiled cell keeps no Python object.
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

    No product document states the convention; VM-V's prescribed weight-table cash flow
    model assumes payments at the end of each period, so arrears is the default [R1].  A
    label accessor, which no projection cell calls: it returns the ``timing`` column,
    compared exactly, or raises.
    """
    v = model_point()["timing"]
    if v not in ("arrears", "advance"):
        raise ValueError("invalid timing")
    return v


def is_arrears():
    """Whether instalments fall in arrears, at the end of the month, rather than in advance.

    A decode of the model point's ``timing`` column, ``Data.is_arrears``, validated by
    ``Data.has_timing`` as :func:`payment_timing` validates it, so that the payment
    months, the survival point, the refund balance and the refund-period search branch on
    a flag and no projection cell calls the label accessor, which is left to reporting.
    """
    if data.has_timing()[idx] == 0:                                  # noqa: F821
        raise ValueError("invalid timing")
    return bool(data.is_arrears()[idx])                              # noqa: F821


def cola_rate():
    """g: the fixed compound COLA rate, in {0, .01, .02, .03, .04} [S1][S5].

    Read from ``Data.cola_rate``.  A rate that is not a finite number is refused here,
    naming the point: it compounds every instalment past the first year, which the
    refunds, the refund period and the withdrawal's floor read through a ``max``, a
    ``min`` or a search.
    """
    if data.cola_rate_ok()[idx] == 0:                                # noqa: F821
        raise ValueError(f"point_id {point_id()}: cola_rate must be a finite number; it "
                         f"is not")
    return float(data.cola_rate()[idx])                              # noqa: F821


def annual_income_first():
    """B(1): the annualized income in the first policy year, the ``annual_income`` column.

    Fixed at the annuity date and exogenous, as in ``SPIA_US_S``: no insurer publishes
    payout factors, so the model does not derive it from the premium.  The one cell that
    reads the column, ``Data.annual_income``, so that :func:`annual_income`, a recursion,
    reads no vector in its own formula.  An income that is not a finite number is refused
    here, naming the point, for the reason :func:`cola_rate` gives.
    """
    if data.annual_income_ok()[idx] == 0:                            # noqa: F821
        raise ValueError(f"point_id {point_id()}: annual_income must be a finite number; "
                         f"it is not")
    return float(data.annual_income()[idx])                          # noqa: F821


def commutation_enabled():
    """Whether the contract carries the certain-portion commutation right [S1]: ``bool()``
    of the column, from ``Data.commutation_enabled``."""
    return bool(data.commutation_enabled()[idx])                     # noqa: F821


def issue_state_excludes_withdrawal():
    """True where the issue state bars the withdrawal feature (Oregon) [S1][S2]: ``bool()``
    of the column, from ``Data.issue_state_excludes_withdrawal``."""
    return bool(data.issue_state_excludes_withdrawal()[idx])         # noqa: F821


def qualified():
    """True for qualified money.  Informational: the RMD overlay is not implemented.

    ``bool()`` of the column, from ``Data.qualified``; no flow reads it.
    """
    return bool(data.qualified()[idx])                               # noqa: F821


def rating_factor():
    """theta: the substandard mortality multiplier **[std]**; 1.0 in the base run.

    ``q_rated = min(1, theta * q_be)``, the reference model's carrier for anti-selection
    at outset and for rated ages [S8][R1][REG-R41].  Read from ``Data.rating_factor``.
    Text is refused here, naming the point, and so is a blank or infinite factor on the
    table basis, the one reader, whose survival the payment factor's ``max(C, L)`` would
    read as a number (``Data``'s ``rating_factor_ok``).
    """
    if data.rating_factor_ok()[idx] == 0:                            # noqa: F821
        raise ValueError(f"point_id {point_id()}: rating_factor must be a number, and a "
                         f"finite one on the table basis, which reads it; it is not")
    return float(data.rating_factor()[idx])                          # noqa: F821


def annuity_year():
    """The calendar year of the annuity date **[std]**; the generational anchor.

    The improvement exponent is ``calendar_year(t) - mort_table_year``, so this is what
    makes the mortality basis generational rather than period.  For a contract in payment
    at the valuation date it is the year the annuity commenced, before that date; for one
    commencing after it, the year it will commence.  The model carries no calendar
    valuation date: each point's calendar years follow from its own annuity year, which is
    why improvement needs nothing re-based on the valuation clock (see
    :func:`calendar_year`).  A real block carries each contract's actual annuity year.
    The shipped points are test cases, restated from ``SPIA_US_S``'s at different months
    with ``SPIA_US_S``'s 2026 kept, so they stand at different calendar dates at their
    common ``t = 0``.  Read from ``Data.annuity_year``, ``int()`` of the column; one
    ``int()`` cannot read, or of ``2**53`` or more in size, is refused here, naming the
    point.  Only the table basis reads it, so a blank on the scenario basis is refused only
    by a direct call.
    """
    if data.annuity_year_ok()[idx] == 0:                             # noqa: F821
        raise ValueError(f"point_id {point_id()}: annuity_year must be a number int() "
                         f"reads, below 2**53 in size; it is not")
    return int(data.annuity_year()[idx])                             # noqa: F821


def mort_basis():
    """Whether the run is probability-weighted (*table*) or deterministic (*scenario*).

    *table* runs the notes' generational recursion off the shipped tables; *scenario*
    **[std]** replaces it with the step function ``1{duration_mth(t) <= death_mth(life)}``
    on the policy clock - alive at every time point up to the start of the month of death,
    dead from its end - so the notes' worked example, which is a scenario and not an
    expectation, reproduces exactly.  See the Space docstring.  A label accessor, which
    no projection cell calls.
    """
    v = model_point()["mort_basis"]
    if v not in ("table", "scenario"):
        raise ValueError("invalid mort_basis")
    return v


def is_scenario():
    """Whether the run is the deterministic scenario, not the probability-weighted table.

    A decode of the model point's ``mort_basis`` column, ``Data.is_scenario``, validated by
    ``Data.has_mort_basis`` as :func:`mort_basis` validates it, so that :func:`lives_if`
    and its check branch on a flag and no projection cell calls the label accessor, which
    is left to reporting.
    """
    if data.has_mort_basis()[idx] == 0:                              # noqa: F821
        raise ValueError("invalid mort_basis")
    return bool(data.is_scenario()[idx])                             # noqa: F821


def death_mth(life):
    """The scenario month of death of ``life``, a **policy month**; -1 if it survives.

    Read only on the scenario basis, :func:`is_scenario`.  A blank cell in the model point
    table means the life never dies in the scenario and is returned as -1, because month 0
    is a projectable month of death like any other.  The month counts from the annuity date,
    on the clock :func:`duration_mth` counts, whatever the valuation date: a death "during
    policy month m" is decremented at the end of that month, so ``lives_if(t, life)`` is 1
    while ``duration_mth(t) <= m`` and 0 from the next time point on.  The model point
    table's ``death_mth_1`` / ``death_mth_2`` are month indices on this 0-based grid: the
    notes' "dies during month 14" is ``death_mth = 13``, which falls at ``t = 13`` on a
    point commencing at the valuation date and before it, at ``t = -1``, on point 16, in
    payment 14 months.  Read from ``Data.death_mth_1`` and ``Data.death_mth_2``, which hold
    the blank as -1 already; a month of ``2**53`` or more in size is refused here, naming
    the point.  Any other life raises, where stage ``E`` read the joint annuitant's column
    for any life but 1.
    """
    if life == 1:
        if data.death_mth_1_ok()[idx] == 0:                          # noqa: F821
            raise ValueError(f"point_id {point_id()}: death_mth_1 must be blank or below "
                             f"2**53 months in size; it is not")
        return int(data.death_mth_1()[idx])                          # noqa: F821
    if life == 2:
        if data.death_mth_2_ok()[idx] == 0:                          # noqa: F821
            raise ValueError(f"point_id {point_id()}: death_mth_2 must be blank or below "
                             f"2**53 months in size; it is not")
        return int(data.death_mth_2()[idx])                          # noqa: F821
    raise ValueError("invalid life")


def duration_mth_init():
    """Months from the annuity date to the valuation date, the ``duration_mth`` column.

    The contract's age in months at ``t = 0``: 14 for an annuity that commenced 14 months
    before the valuation date, 0 for one commencing at it, and -13 for one to commence 13
    months after it, which ``Data`` admits up to ``future_horizon_mth`` months ahead.  It is
    read as ``basiclife.BasicTerm_SE`` reads it, by value, and is the one fact the policy
    clock takes from the model point, from ``Data.duration_mth``; a value ``int()`` cannot
    read, or of ``2**53`` or more in size, is refused here, naming the point.
    """
    if data.duration_mth_ok()[idx] == 0:                             # noqa: F821
        raise ValueError(f"point_id {point_id()}: duration_mth must be a number int() "
                         f"reads, below 2**53 in size; it is not")
    return int(data.duration_mth()[idx])                             # noqa: F821


def lives_if_init(life):
    """l_i at the valuation date: the probability that ``life`` is alive then.

    The ``lives_if_init_1`` (primary, life = 1) or ``lives_if_init_2`` (joint annuitant,
    life = 2) column, as the contract stands at the start of month 0, before any month-0
    death: the opening value of :func:`lives_if` at :func:`t_entry`.  On a real record it
    is 1 or 0, so a joint contract may carry one life already dead; on a point restated
    from ``SPIA_US_S`` at its month ``d`` it is ``SPIA_US_S``'s ``lives_if(d, life)``, a
    probability.  The lives are independent, as in ``SPIA_US_S``, so the two per-life
    probabilities are the whole survival state.  A contract not yet in payment carries its
    values at the annuity date, 1 for each covered life, and ``lives_if_init_2`` is 0 on a
    single-life contract; ``Data`` checks both, and on the scenario basis that each status
    is its death month's.  Read from ``Data.lives_if_init_1`` and ``Data.lives_if_init_2``.
    """
    if life == 1:
        return float(data.lives_if_init_1()[idx])                    # noqa: F821
    if life == 2:
        return float(data.lives_if_init_2()[idx])                    # noqa: F821
    raise ValueError("invalid life")


def commute_frac_cum_init():
    """theta_cum at the valuation date: the commutation fraction applying in month 0.

    The ``commute_frac_cum_init`` column: the cumulative fraction of the certain
    instalments commuted before the valuation date, as it applies to month 0's instalment,
    before any month-0 withdrawal, and the opening value of :func:`commute_frac_cum` at
    :func:`t_entry`.  Path-dependent, because it records the withdrawals actually taken,
    so the contract's terms cannot re-derive it.  0 at the annuity date, and so on every
    point not yet in payment; ``Data`` refuses a fraction where none could have been
    taken, a necessary condition only.  Read from ``Data.commute_frac_cum_init``.
    """
    return float(data.commute_frac_cum_init()[idx])                  # noqa: F821


def cmt10_shift_init():
    """The 10-year CMT's change from the annuity date to the valuation date.

    The ``cmt10_shift_init`` column, a decimal, 0.005 for a rise of 50 basis points: the
    10-year CMT at the valuation date less the 10-year CMT at the contract's annuity date,
    the part of the change since purchase that a contract in payment has already seen.
    The commutation discount rate moves one for one with the change since the annuity
    date (:func:`commute_disc_rate`), and that change began before ``t = 0``, so its value
    there is opening state, as the CMT's value at the start of a term would be on a market
    path.  A fact of the market, not of the contract's own history: two contracts with one
    annuity date carry one value.  0 at the annuity date, and so on every point not yet in
    payment, as ``Data`` checks.  The change made at the valuation date is
    ``cmt10_shift``, which a contract commencing later, bought after it, has not seen
    (:func:`commute_disc_rate`).  Read from ``Data.cmt10_shift_init``, a float vector, in
    the same order as at stage ``E``.
    """
    return float(data.cmt10_shift_init()[idx])                       # noqa: F821


def duration_mth(t):
    """Months elapsed from the annuity date at the start of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from the annuity date, and the two move together.  A closed
    form, where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame.  Negative before the annuity date.
    Everything contractual reads this clock: the policy year, the attained ages, the
    payment months, the COLA anniversaries, the certain period and the commutation months.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a contract in payment at the valuation date or commencing at it, ``k`` for one
    commencing ``k`` months later.  It is the base of every recursion on the valuation
    clock: :func:`lives_if` and :func:`commute_frac_cum` open there, from the opening
    state, and read no month before it, and :func:`pols_if_at` counts the contracts from
    there.
    """
    return max(0, -duration_mth_init())


def stop_mth():
    """The policy month at which the projection stops: the stop rule, on the policy clock.

    ``max(horizon_mths(), certain_mths_eff())``, ``SPIA_US_S``'s frame length counted from
    the annuity date: the notes' age stop on the youngest covered life, or the end of the
    effective certain period if that is later.  The last projected month is policy month
    ``stop_mth() - 1``; :func:`proj_len` counts the months to the stop from the valuation
    date instead.  696 on the anchor cell's 65/62 pair.
    """
    return max(horizon_mths(), certain_mths_eff())


def is_active(t):
    """Whether month t is inside the frame: commenced, and not yet at the stop rule.

    ``0 <= duration_mth(t) < stop_mth()``.  False before the annuity date and from the
    stop rule on.  Outside it every count is zero, and so every cash flow; no cell reads
    a rate, a policy year or an attained age there that the contract does not have.  A
    contract's own end inside the frame - its last death, or its last certain instalment
    - is a probability or a floor reaching zero, not the end of the frame, which runs on
    with zeros as ``SPIA_US_S``'s does.
    """
    return 0 <= duration_mth(t) < stop_mth()


def duration(t):
    """Completed policy years at the start of month t: ``duration_mth(t) // 12``.

    0 throughout the first policy year from the annuity date, and negative before it.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y(t) = duration(t) + 1: the policy year containing month t, on the policy clock.

    The policy year is the contract's own 1-based label, ``duration_mth(t) // 12 + 1``, and
    is *derived* from the policy clock, never used to index the frame: 1 for policy months
    0..11, whatever ``t`` they fall at.  It is 0 or less before the annuity date, where no
    cell reads a schedule by it.
    """
    return duration(t) + 1


def calendar_year(t):
    """The calendar year of the policy year containing month t, on the policy clock.

    ``annuity_year() + duration(t)``: calendar-dated from the annuity year, so a contract
    in payment at the valuation date reads its own calendar years whatever that date, and
    nothing in the improvement it dates is re-based onto the valuation clock.  On a point
    restated from ``SPIA_US_S`` at its month ``d``, month ``t`` here is ``SPIA_US_S``'s
    month ``d + t``, and so the same calendar year.
    """
    return annuity_year() + duration(t)


def age(t, life):
    """The attained age (ANB) of ``life`` in the policy year containing month t.

    ``age_at_entry(life) + duration(t)``, on the policy clock: the age changes on each
    anniversary of the annuity date, whatever the valuation date.
    """
    return age_at_entry(life) + duration(t)


def horizon_mths():
    """Policy months from the annuity date before some covered life passes the limit age.

    ``12*(omega_age - min x_i)``: the notes stop once ``(m + 1)/12 + x_i > omega`` for
    every covered life, ``m`` the policy month, and stopping on the primary's age alone
    would truncate a younger joint annuitant's tail.  Counted from the annuity date, so
    the last month it admits is policy month ``horizon_mths() - 1``, in which the youngest
    life is still ``omega_age - 1`` - see :func:`proj_len`.  The younger of the two ages is
    found by one comparison, with no list.
    """
    youngest = age_at_entry(1)
    if is_joint() and age_at_entry(2) < youngest:
        youngest = age_at_entry(2)
    return 12 * (omega_age - youngest)                               # noqa: F821


def proj_len():
    """The number of months from the valuation date to the stop rule.

    ``stop_mth() - duration_mth_init()``: 696 for the anchor cell commencing at ``t = 0``,
    682 for it in payment 14 months (point 16), 1 in its last month (point 21), and 709 for
    it commencing 13 months after the valuation date (point 22).  The exclusive end of the
    frame: :func:`result_cf` runs over ``range(proj_len())``, so the last projected month
    is ``proj_len() - 1``, which is policy month ``stop_mth() - 1`` on every point.

    :func:`horizon_mths` implements the notes' age stop rule literally - stop once
    ``(m + 1)/12 + x_i > omega`` for every covered life, ``m`` the policy month - and
    :func:`stop_mth` takes it, or the certain period if longer, from the annuity date.
    Under the ANB age convention the youngest life's attained age in the last month is
    ``omega_age - 1``: the projection stops **one month before** any life attains
    ``omega_age``.  The notes' other stop test, ``IF(t) < 1e-6``, is therefore **not**
    subsumed - point 21, the anchor cell on the table basis in payment 695 months, carries
    ``pols_if(0) = 3.41e-06``, ``SPIA_US_S``'s ``pols_if(695)``.  The age rule is the one
    implemented, because it keeps the frame independent of the projection it bounds.

    Two kinds of point have no frame, and raise here, naming the point, rather than
    projecting nothing: an in-force extract should not carry either.  A point at or past
    the stop rule.  And a contract that owes nothing after the valuation date: in payment,
    its certain period over, ``duration_mth`` at or past ``certain_mths_eff()``, and no
    life-contingent payment left, because the form is certain_only or every covered life
    has died.  Such a contract's last payment, or its refund, was made before the
    valuation date; this is ``Term_US_SEC``'s point past its cover, for a product whose
    cover can end with a death.  The rule needs the certain period, which an installment
    refund derives from the schedule, so it is checked here rather than in ``Data``, and
    each message says, by form, why nothing is owed.

    Before either, the contract the compiled model's caches are sized for
    (``spec_sec.py``), each bound a lower-case Reference, each refusal naming the point:
    an issue age of a covered life below ``issue_age_min``, 0, on every form, since a
    frame runs to the age stop on its youngest life, the primary's and the joint
    annuitant's each asked; and an elected certain period longer than ``12 * (omega_age -
    issue_age_min)``, 1,440 months, which would carry the stop rule past the age stop at
    ``issue_age_min``.  They come first, because :func:`stop_mth` reads the installment
    refund's search, which reads :func:`cum_annuity_pp` up to :func:`horizon_mths`, past
    the cache on a point issued younger.  ``SPIA_US_S`` projects every age from 0, on the
    scenario basis, and on the table basis with a table starting below 40, and so does
    this model, a lifetime form below the 18 product-spec issues at among them: a
    negative issue age and a certain period above 1,440 months are outside every contract,
    and refused as Term's issue ages are, a departure from ``SPIA_US_S``, which projects
    them.  ``omega_age``
    above 120, and ``Data.future_horizon_mth`` above 120, are not refused: each needs the
    caches resized and the model rebuilt, and a report past them is a bare ``IndexError``
    in the compiled model alone, where modelx projects.  So is a monthly cell called
    directly on a point ``proj_len`` refuses, which reads :func:`stop_mth` through
    :func:`is_active` without asking here.
    """
    if age_at_entry(1) < issue_age_min:                              # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry(1)} is below "
                         f"issue_age_min, {issue_age_min}")          # noqa: F821
    if is_joint() and age_at_entry(2) < issue_age_min:               # noqa: F821
        raise ValueError(f"point_id {point_id()}: joint issue age {age_at_entry(2)} "
                         f"is below issue_age_min, {issue_age_min}")  # noqa: F821
    if (is_period_certain()
            and certain_mths() > 12 * (omega_age - issue_age_min)):  # noqa: F821
        raise ValueError(f"point_id {point_id()}: certain_months {certain_mths()} is above "
                         f"12 * (omega_age - issue_age_min), "
                         f"{12 * (omega_age - issue_age_min)}, the longest "  # noqa: F821
                         f"certain period the caches are sized for")
    n = stop_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past the end of the projection, policy month {stop_mth()}")
    d = duration_mth_init()
    n_eff = certain_mths_eff()
    if d > 0 and d >= n_eff:
        if is_certain_only():
            raise ValueError(
                f"point_id {point_id()}: duration_mth {d}: no payment is "
                f"owed after the valuation date: a certain_only contract pays nothing "
                f"after its certain period, which ended at policy month {n_eff}")
        dead = not (lives_if_init(1) > 0.0 or (is_joint() and lives_if_init(2) > 0.0))
        if dead and n_eff > 0:
            raise ValueError(
                f"point_id {point_id()}: duration_mth {d}: no payment is "
                f"owed after the valuation date: every covered life has died, and the "
                f"certain period ended at policy month {n_eff}")
        if dead:
            raise ValueError(
                f"point_id {point_id()}: duration_mth {d}: no payment is "
                f"owed after the valuation date: every covered life has died, and the "
                f"form has no certain period")
    return n


def is_payment_pm(k):
    """Whether policy month k is a payment month: the payment schedule, on the policy clock.

    ``k`` counts months from the annuity date.  Arrears: the n-th instalment falls at the
    end of policy month ``12n/m - 1``, so ``k = 2, 5, 8, ...`` at m = 4.  Advance: it falls
    one full payment period earlier, at the start of policy month ``12(n-1)/m``, so
    ``k = 0, 3, 6, ...``.  At m = 12 every month is a payment month on either convention.
    The one definition of the payment months: :func:`is_payment_mth` asks it at the policy
    month of month t, and :func:`annuity_pp_sched_pm` at any policy month, so that the
    payments to date and the commuted value read the schedule without passing a policy
    month as ``t``.
    """
    step = 12 // payment_freq()
    if is_arrears():
        return (k + 1) % step == 0
    return k % step == 0


def is_payment_mth(t):
    """Whether month t is a payment date: ``is_payment_pm(duration_mth(t))``, in the frame.

    The schedule is the contract's, on the policy clock (:func:`is_payment_pm`): a contract
    in payment 14 months that pays quarterly in arrears pays in policy months 14, 17, ...,
    so at ``t = 0, 3, ...``.  False outside the frame.
    """
    return is_active(t) and is_payment_pm(duration_mth(t))


def payment_surv_mth(t):
    """The **time point** at which survival is measured for the instalment of month t.

    A time point on the valuation clock, where :func:`lives_if` is indexed.  Arrears: time
    ``t + 1``, the end of month t.  Advance: time ``t``, the start of month t, because an
    advance instalment falls at the start of the month whatever the frequency; for the
    first instalment of a contract commencing at the valuation date that is time 0, where
    ``lives_if`` is 1.  Using end-of-period survival for advance payments understates the
    liability by about one period's mortality per payment.

    The notes put the advance point at ``t + 1 - 12/m``, "one full payment period
    earlier" than the arrears point ``t + 1``.  That measures from the **arrears** month
    of the same instalment, which falls one payment period *after* the advance month;
    :func:`is_payment_pm` indexes an advance instalment by the policy month it falls in, so
    the two readings coincide only at m = 12.  At m = 4 the second instalment falls at the
    start of policy month 3 and requires survival to that time point - not to the one two
    months earlier, ``t + 1 - 12/m``, which would pay it to a life the projection has
    already recorded as dead.
    """
    if is_arrears():
        return t + 1
    return t


def annual_income(y):
    """B(y): the unreduced annualized income in policy year y.

    ``B(y) = B(y-1)(1 + g)`` on each anniversary of the annuity date [S1][S4], compound
    and irrevocable.  Escalation applies to the **unreduced** level and continues after a
    survivor reduction, because the contract reduces payments to delta of the *current*
    income payment [S2].  One carrier instead starts the first increase one year after the
    first income payment [S5]; that one-period difference is a **[std]** convention choice
    not taken here.  ``B(1)`` is exogenous - no insurer publishes payout factors, so the
    model does not derive it from the premium - and :func:`annual_income_first` reads it.

    Keyed by policy year, on the policy clock, and a deterministic schedule, so it needs no
    opening state.  Its recursion is based where the valuation date falls: for the policy
    year containing it, ``max(duration_mth_init(), 0) // 12 + 1``, the policy year of
    :func:`t_entry`, one loop compounds ``B(1)`` year by year, the same products in the
    same order as the recursion, so ``B`` is ``SPIA_US_S``'s to the last bit, and a
    contract valued late in life reads its income without recursing back to the annuity
    date.  Later years recurse back to that one, and earlier years back to ``B(1)``, as in
    ``SPIA_US_S``.  The base year is read from the model point, not from the clock, so
    reading it reads no month.
    """
    if y <= 1:
        return annual_income_first()
    if y == max(duration_mth_init(), 0) // 12 + 1:
        b = annual_income_first()
        for _ in range(y - 1):
            b *= 1.0 + cola_rate()
        return b
    return annual_income(y - 1) * (1.0 + cola_rate())


def annuity_pp_sched_pm(k):
    """The scheduled unreduced instalment per contract in policy month k, before any trim.

    ``inst = B(y)/m`` in a payment month and 0 elsewhere, ``y = k // 12 + 1`` the policy
    year containing policy month ``k``.  Keyed by policy month, on the policy clock, so
    that :func:`cum_annuity_pp`, :func:`commuted_value` and :func:`commute_amount` read the
    schedule at policy months before and after month t without passing a policy month as
    ``t``; :func:`annuity_pp_sched` is this at the policy month of month t.
    """
    if not is_payment_pm(k):
        return 0.0
    return annual_income(k // 12 + 1) / payment_freq()


def annuity_pp_sched(t):
    """The scheduled unreduced instalment per contract in month t, before any trim.

    ``inst(t) = B(y(t))/m`` on payment dates and 0 elsewhere:
    ``annuity_pp_sched_pm(duration_mth(t))`` inside the frame, and 0 outside it.
    """
    return annuity_pp_sched_pm(duration_mth(t)) if is_active(t) else 0.0


def cum_annuity_pp(k):
    """G(k): cumulative scheduled instalments per contract paid **by time k**.

    Indexed by a **time point** on the **policy** clock, not by a month: ``k`` months
    after the annuity date, ``k = 0`` the annuity date itself and ``G(0) = 0``; ``G(k)``
    sums the instalments of policy months ``0 ... k - 1``, so the instalment of policy
    month ``m`` - whether it falls at the month's start or at its end - enters
    ``G(m + 1)``.  That index does not move with the valuation date, which is why the
    notes' ``G(13) = 12 x 500.00 + 515.00`` reads unchanged here, on the cash refund in
    payment 13 months (point 17) as on its twin.

    A **deterministic** as-if-alive schedule: instalments payable while any covered life
    is alive follow the deterministic escalation path, so the refund balance needs no
    path simulation, and the payments to date need no opening state: they are summed from
    the annuity date.  On a joint contract with a survivor reduction the cash refund is
    offered only at delta = 100% [S5], so the unreduced schedule is the paid schedule.

    The recursion ``G(k) = G(k-1) + inst(k-1)`` is ``SPIA_US_S``'s, but it is based where
    the valuation date falls: at the policy month of :func:`t_entry`,
    ``max(duration_mth_init(), 0)``, read from the model point rather than the clock, one
    loop sums the instalments scheduled before it, the
    same additions in the same order as the recursion, so ``G`` is ``SPIA_US_S``'s to the
    last bit.  The refunds read ``G`` from there on and recurse back to it; the
    installment-refund search reads it upward from the first payment point and recurses
    back no further than the key it read before.  Recursing from the annuity date instead,
    the first refund of a cash refund long in payment would recurse as deep as the
    contract is old.
    """
    if k <= 0:
        return 0.0
    if k == max(duration_mth_init(), 0):
        total = 0.0
        for j in range(k):
            total += annuity_pp_sched_pm(j)
        return total
    return cum_annuity_pp(k - 1) + annuity_pp_sched_pm(k - 1)


def certain_mths_refund():
    """n_R: the certain period derived by an installment refund [S1][S4][S5][S6].

    ``n_R = min{k : G(k) >= P}`` over the payment points - payments continue until
    cumulative payments equal the premium.  A **count of months** from the annuity date,
    like ``n``, not a month index: the last certain month is policy month ``n_R - 1``.  The
    search therefore runs on the time axis of :func:`cum_annuity_pp`, the policy clock,
    where ``G(k)`` is the amount paid by time k, and its result does not depend on the
    valuation date.

    Under a level path this closes to ``(12/m) * ceil(m*P/B(1))``, which is
    the published rule "guaranteed payment period = premium paid / annualized income
    benefit amount" rounded up to a payment date [S5]; the anchor check is
    ``P/B(1) = 100,000/6,000 = 16.667 years = 200 months``.  Searched rather than closed
    so a COLA path (which the anchor carrier does not offer with this form [S1]) still
    resolves.
    Capped at :func:`horizon_mths` if the premium is never recovered.
    """
    step = 12 // payment_freq()
    last = horizon_mths()
    k = step if is_arrears() else 1
    while k <= last:
        if cum_annuity_pp(k) >= premium_pp():
            return k
        k += step
    return last


def certain_mths_eff():
    """n_eff: the effective certain period in months from the annuity date, by form.

    ``n`` for life_certain and certain_only [S1][S2][S4][S5]; ``n_R`` for
    installment_refund [S1][S5]; 0 for life_only and cash_refund [S1][S2].  A count of
    months on the policy clock: the certain period covers policy months
    ``0 ... n_eff - 1``, so a contract in payment ``d`` months has ``n_eff - d`` certain
    months left, and none once ``d >= n_eff``.
    """
    if is_period_certain():
        return certain_mths()
    if is_installment_refund():
        return certain_mths_refund()
    return 0


def annuity_pp(t):
    """inst(t): the instalment per contract actually payable in month t.

    Equal to :func:`annuity_pp_sched` except on installment_refund, where the notes trim
    the final instalment to ``P - G(n_R - 12/m)`` **[std]** so cumulative payments land
    exactly on the premium.  That final instalment falls in policy month ``n_R - 1``,
    ``n_R`` being a count of months, and ``G`` is indexed by a policy time point, so both
    indices read exactly as the notes write them, and the trim falls at whichever ``t``
    policy month ``n_R - 1`` does.  The trim is a no-op whenever ``P`` is an exact
    multiple of the instalment, which is the shipped anchor's case.  Where the first
    instalment already repays the premium, ``n_R - 12/m`` is before the annuity date, and
    ``G`` is read at 0, its value there.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    if not is_installment_refund():
        return annuity_pp_sched(t)
    n_r = certain_mths_refund()
    if duration_mth(t) != n_r - 1:
        return annuity_pp_sched(t)
    step = 12 // payment_freq()
    return max(0.0, premium_pp() - cum_annuity_pp(max(0, n_r - step)))


def mort_rate_base_at(x, life):
    """The base-table annual mortality rate at attained age ``x``, for ``life``'s sex.

    The one cell that reads ``mort_table.csv``, keyed by age and life, so that the monthly
    cells call it rather than join the table themselves.  The sex is the join key:
    :func:`mort_schedule` gives ``life``'s row of ``Data.mort_table_array``, and the age is
    its column, and the label accessor itself is left to reporting.  Called only below the
    limiting age: :func:`mort_rate_base` returns 1 at and above it without calling here.
    The age is checked against the row's first and last ages, ``Data.mort_age_first`` and
    ``Data.mort_age_last``, before the array is read, so an age the table lacks, below
    its first age, 40 as shipped, or any age on a sex the table lacks, whose row 0 holds
    none, is refused, naming the point, the age and the life, where ``SPIA_US_S``'s
    ``.loc`` raised ``KeyError``, and the padding is never read.
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
    """The base-table annual mortality rate for ``life`` in the policy year containing t.

    The shipped table is an illustrative **[std]** annuitant table, *not* the 2012 IAM
    Basic table the notes prescribe: licensed tables may not be embedded, and the Basic
    table is in any case not printed in any source this library holds.  Rates at and
    above the limiting age are 1, and the table is read below it, at the attained age
    :func:`age` gives, through :func:`mort_rate_base_at`.  Zero outside the frame, where
    the contract has no attained age to look up.
    """
    if not is_active(t):
        return 0.0
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 1.0
    return mort_rate_base_at(x, life)


def improvement_rate(t, life):
    """G2_x: the generational improvement rate for ``life`` in the year containing t.

    The shipped scale is an illustrative **[std]** stand-in for Projection Scale G2.
    Scaling this table is the notes' first-listed sensitivity - Scale G2 is fixed and
    dated, and 2020-2024 experience says it has over-projected [R9].  Zero at and above
    the limiting age, and outside the frame; read below it through
    :func:`improvement_rate_at`.
    """
    if not is_active(t):
        return 0.0
    x = age(t, life)
    if x >= omega_age:                                               # noqa: F821
        return 0.0
    return improvement_rate_at(x, life)


def mort_rate(t, life):
    """q_rated: the annual mortality rate applied to ``life`` in the year containing t.

    The notes' construction, in order::

        q_base(x, 2012+k) = q_x(table) * (1 - G2_x)^k
        q_be              = min(1, AE * q_base),      AE = 1.084 [std]
        q_rated           = min(1, theta * q_be),     theta = 1 in base

    ``k = calendar_year(t) - mort_table_year``, so the basis is **generational**: each
    attained age in each future calendar year uses its own improved rate.  The calendar
    year is the contract's own, dated from its annuity year on the policy clock
    (:func:`calendar_year`), so a contract in payment at the valuation date reads the
    improvement of the calendar years it reaches, and nothing is re-based.  The A/E factor
    belongs on the *projected* basis, matching the study's measurement convention - on
    the unprojected table the study's own answer is 99.6% [R9], and applying 1.084 there
    misstates the mortality level by about 8%.  An improvement rate of exactly 1 at a
    calendar year before ``mort_table_year`` raises ``0.0`` to a negative power, which
    modelx refuses with ``ZeroDivisionError`` and the compiled model, whose power is C's,
    reads as an infinity; no shipped rate is 1.  The two caps keep ``q_rated`` at most 1,
    so :func:`mort_rate_mth` stays real at any rating, and the code writes each with its
    float bound second, ``min(q, 1.0)``, as ``SPIA_US_S`` does, so that a missing input,
    a NaN, stays NaN, where ``min(1.0, q)`` would read it as 1.  Zero outside the frame,
    before the calendar year is read.
    """
    if not is_active(t):
        return 0.0
    k = calendar_year(t) - mort_table_year                           # noqa: F821
    q_base = mort_rate_base(t, life) * (1.0 - improvement_rate(t, life)) ** k
    q_be = min(mort_ae_factor * q_base, 1.0)                         # noqa: F821
    return min(rating_factor() * q_be, 1.0)


def mort_rate_mth(t, life):
    """q_m(t) = 1 - (1 - q_rated)^(1/12): the monthly mortality rate **[std]**."""
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def lives_if(t, life):
    """l_i(t): the probability that ``life`` is alive **at time t**.

    Indexed by a **time point** on the valuation clock, not by a month: time ``t`` is the
    start of month ``t``, so month t opens at time ``t`` and closes at time ``t + 1``, and
    time 0 is the valuation date.  The argument is named ``t``, as the valuation clock's;
    ``SPIA_US_S`` names its own ``k``, the same reading on its one clock.

    At :func:`t_entry`, the first time point on the books, it is the opening state,
    :func:`lives_if_init`: the life's status at the valuation date for a contract in
    payment, and 1, its value at the annuity date, for one commencing at or after it.
    Before that it is 0: the contract is not yet on the books.  After it, on the *table*
    basis, ``l_i(t) = l_i(t-1)(1 - q_m(t-1))``: the rate of month ``t - 1``, the month that
    has just closed, deaths being decremented at end of month.  On the *scenario* basis
    **[std]** the survival path is the step function ``1{duration_mth(t) <= death_mth}``
    on the policy clock, with ``death_mth = -1`` meaning the life survives the whole
    projection - which is what the notes' worked example specifies; ``Data`` holds the
    opening status to the same step, so the two agree at :func:`t_entry`.  A joint
    annuitant dying in policy month 13 reads ``lives_if(14, 2) = 0`` on a point commencing
    at the valuation date, as in the notes, and ``lives_if(0, 2) = 0`` on point 16, in
    payment 14 months.
    Returns 0 for life = 2 on a single-life contract.
    """
    if life == 2 and not is_joint():
        return 0.0
    if t < t_entry():
        return 0.0
    if t == t_entry():
        return lives_if_init(life)
    if is_scenario():
        d = death_mth(life)
        return 0.0 if (d >= 0 and duration_mth(t) > d) else 1.0
    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t - 1, life))


def lives_death(t, life):
    """d_i(t) = l_i(t) - l_i(t+1): the death density of ``life`` in month t.

    Month t runs from time t to time t + 1, and :func:`lives_if` is indexed by time, so
    the deaths *of month t* are the forward difference - which is how the notes write it
    too.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    return lives_if(t, life) - lives_if(t + 1, life)


def lives_if_last(t):
    """l_last(t): the probability that at least one covered life is alive at time t.

    ``l_1 + l_2 - l_1*l_2`` on a joint contract, under **joint-life independence
    [std]** - the SOA/LIMRA payout study is explicit that its data cannot inform the
    assumption, since it gives no recognition to a living secondary annuitant [R9].
    On a single-life contract this is ``l_1``, which is why no separate ``l_alive`` cells
    is needed.  Indexed by a time point on the valuation clock, like :func:`lives_if`,
    and 0 before the contract is on the books.
    """
    l1 = lives_if(t, 1)
    if not is_joint():
        return l1
    l2 = lives_if(t, 2)
    return l1 + l2 - l1 * l2


def lives_death_last(t):
    """d_last(t) = l_last(t) - l_last(t+1): the last-death density in month t.

    This is also the notes' ``d_term(t)``, the death that terminates the income stream:
    ``d_1`` on a single-life contract and ``d_last`` on a joint one, which
    :func:`lives_if_last` already collapses into one expression.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    return lives_if_last(t) - lives_if_last(t + 1)


def certain_floor(t):
    """C(t) = 1{duration_mth(t) < n_eff}: the annuity-certain floor indicator.

    ``n_eff`` is a **count** of certain months from the annuity date, so the certain
    period covers policy months ``0 ... n_eff - 1``: a 10-year certain period is
    ``duration_mth(t) < 120``, and the floor is gone from policy month 120, which is
    ``t = 0`` on point 18, in payment 120 months.  The certain months left at the
    valuation date are therefore no opening state: they follow from ``duration_mth``.
    Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    return 1.0 if duration_mth(t) < certain_mths_eff() else 0.0


def payment_factor_life(t):
    """L(t): the life-contingent payment factor for the instalment falling in month t.

    Survival is measured at the time point :func:`payment_surv_mth` returns - ``t + 1`` on
    arrears, ``t`` on advance - not at ``t``.  By form and trigger::

        single life:           L = l_1
        joint, trig = either:  L = l_1*l_2 + delta*(l_1 + l_2 - 2*l_1*l_2)
        joint, trig = primary: L = l_1 + delta*(1 - l_1)*l_2
        certain_only:          L = 0

    The *either* form pays the full instalment while **both** are alive and delta while
    **exactly one** is - the second bracket is P(at least one alive) - P(both alive)
    [S2][S3].  The *primary* form pays in full while the primary lives whatever the joint
    annuitant's status, and delta only when the primary is dead and the joint annuitant
    alive [S2][S3][S5].  The two coincide on the primary's death and differ only on the
    secondary's, which is why the trigger is a switch and not a footnote.  On a joint
    contract in payment with one life already dead, as point 16 is, the factor is delta
    or 1 from ``t = 0``, by trigger.  Zero outside the frame.
    """
    if not is_active(t) or is_certain_only():
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


def payment_factor(t):
    """Phi(t) = max(C(t), L(t)): the master payment factor.

    The ``max`` makes the certain period an annuity-**certain floor** rather than an
    additional stream: during the certain period the full unreduced instalment is paid
    regardless of survival, and the ``max`` prevents paying ``1 + L``.  An additive
    construction silently doubles the guarantee - the notes' first-listed pitfall.
    Because the floor pays the *unreduced* instalment, it also reproduces one carrier's
    rule that a survivor reduction inside a certain period is deferred to the end of that
    period, with no extra flag [S5].
    """
    return max(certain_floor(t), payment_factor_life(t))


def pols_if(t):
    """IF(t): contracts with a payment obligation still open in month t.

    ``pols_if_at(t, BEF_DECR) * max(C(t), l_alive(t+1))`` **[std]** - the in-force
    measure the notes use to carry the maintenance expense, which runs while *any* payment
    obligation remains, whether that obligation is life-contingent or certain, on the
    contracts on the books.  The life-contingent leg is measured at the **end** of month t
    (time ``t + 1``), matching the notes' own end-of-month decrement, so this is a closing
    measure of the period rather than an opening count.  Unlike the library's usual
    ``pols_if``, therefore, it is not ``pols_if_at(t, BEF_DECR)``, the count that weights
    row t, and the registry marks the model ``closing_pols_if`` for that reason: on the
    anchor cell's twin, point 8, ``pols_if(0)`` is 0.99999986 against a count of 1.0, as in
    ``SPIA_US_S``, and on point 21, the same cell in its last month, 3.41e-06.

    One divergence from the notes' literal formula, on ``certain_only`` only.  That form
    has ``L(t) = 0``, so the last instalment falls in policy month ``n_eff - 1`` and
    nothing is owed after it; but ``l_alive`` is a survival probability rather than a
    payment factor and stays positive for the annuitant's remaining lifetime, so the
    unqualified ``max`` would keep accruing the maintenance expense on a contract that has
    ended - contradicting the same table's "while any payment obligation remains".  The
    life-contingent leg is therefore dropped on ``certain_only``, the one form with no
    life contingency in it, and ``IF(t) = C(t)`` there.  Every other form is unaffected.
    See model point 15.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    alive = 0.0 if is_certain_only() else lives_if_last(t + 1)
    return pols_if_at(t, BEF_DECR) * max(certain_floor(t), alive)    # noqa: F821


def pols_if_at(t, timing):
    """Contracts on the books at time t, at the instant ``timing`` names.

    ``BEF_NB``
        The contracts carried in from month t - 1, before month t's annuities commence:
        at :func:`t_entry`, the first month on the books, :func:`pols_if_init`, the count
        in payment at the valuation date (0 for a point commencing at or after it), and
        the whole ``policy_count()`` after it.  Zero outside the frame, so the contracts
        leave the books at the stop rule, at the end of the last projected month.
    ``BEF_DECR``
        ``BEF_NB`` plus :func:`pols_new_biz`: the count that weights every cash flow
        of month t.

    These are ``basiclife.BasicTerm_SE``'s names, int codes (the Space docstring's
    *Codes*), compared by ``==`` alone, and any other timing raises, a string among them in
    modelx.  The count
    is not decremented: mortality decrements each life's survival, :func:`lives_if`, and
    every cash flow is this count times a per-contract amount weighted by survival, as
    ``SPIA_US_S`` weights its flows by the constant ``pols_if_init``.  A count weighted by
    survival could not carry the two lives' independent probabilities.  So ``BEF_NB`` is
    a closed form, the same float that the recursion ``BEF_NB(t-1) + pols_new_biz(t-1)``
    gives, with no chain of calls back to :func:`t_entry`.  :func:`pols_if` is not
    ``BEF_DECR``: it is the notes' closing obligation measure on this count.
    """
    if timing == BEF_NB:                                             # noqa: F821
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return policy_count()
    elif timing == BEF_DECR:                                         # noqa: F821
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)               # noqa: F821
    else:
        raise ValueError("invalid timing")


def pols_new_biz(t):
    """Annuities commencing in month t: ``policy_count()`` in the month of the annuity date.

    The month with ``duration_mth(t) == 0``: ``t = 0`` for a point whose annuity date is
    the valuation date, ``t = k`` for one commencing ``k`` months later.  A contract already
    in payment at the valuation date has none.  New business in
    ``basiclife.BasicTerm_SE``'s sense, a contract entering the books, with no premium:
    the single premium is a pricing input, as in ``SPIA_US_S``.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def commute_util_rate(y):
    """u(y): the deterministic commutation utilization in contract year y **[std]**.

    Zero in the base run, so the payment engine is exercised in isolation: no public data
    on SPIA commutation take-up exists.  The notes' rate-driven alternative
    ``u(y, t) = min(u_max, u_base(y) * max(0, 1 + kappa*[CMT10(0) - CMT10(t)]))`` is not
    implemented - it is a pure shape assumption calibrated to nothing.  Both
    constructions are best-estimate objects and are **barred from a CARVM run**:
    commutation is an elective benefit under AG 33, whose incidence rates must be
    maximised over rather than assumed [REG-R151].
    """
    return 0.0 if y < 2 else commute_util_base                       # noqa: F821


def commute_elig(t):
    """Whether a commutation may be taken in month t [S1].

    All of: the contract carries the right; the issue state is not Oregon; the form has a
    certain period; the contract year is 2 or later; and this is the first month of that
    contract year, which enforces "one withdrawal per contract year".

    On the policy clock: the certain period covers policy months ``0 ... n_eff - 1`` and
    the first month of contract year y is policy month ``12(y - 1)``, so year 2 opens at
    policy month 12, and on point 20, in payment 24 months, year 3 opens at ``t = 0``.
    False outside the frame.
    """
    if not is_active(t):
        return False
    if not commutation_enabled():
        return False
    if issue_state_excludes_withdrawal():
        return False
    n_eff = certain_mths_eff()
    if n_eff <= 0 or duration_mth(t) >= n_eff:
        return False
    if policy_year(t) < 2:
        return False
    return duration_mth(t) % 12 == 0


def commute_disc_rate(t):
    """j(t): the commutation discount rate **[std] [unverified]**.

    ``j(t) = j0 + [CMT10(t) - CMT10(0)]`` with ``j0 = 4.00%``, ``0`` the annuity date: the
    10-year CMT's change since purchase.  **No fixed SPIA issuer publishes a commutation
    discount formula**: one carrier gives only the cap [S1], a second only "an
    interest-rate adjustment will apply" [S2], a third only the 10-year CMT as the driver
    [S5]; the 4% comes from a fourth's *variable* contract [S7].

    Every contract of a block reads the change on one path of the CMT, which every point
    shares, as it shares every economic input, each contract from its own annuity date.
    A contract on the books at the valuation date, in payment or commencing then,
    ``t_entry() == 0``, has seen :func:`cmt10_shift_init` by that date, from its model
    point, and sees ``cmt10_shift``, the change made at the valuation date, from month 0
    on, as ``SPIA_US_S``'s contract sees its ``cmt10_shift`` from its annuity date: its rate
    is ``j0 + cmt10_shift_init() + cmt10_shift``, added in that order.  A contract
    commencing ``t_entry()`` months later is bought after that change and has seen none of
    it, its column being 0, so its rate is ``j0``.  One Reference could not hold the change
    since each contract's own annuity date: contracts in payment bought at different dates
    have seen different changes.  ``cmt10_shift`` is a flat scalar, a path that steps once,
    at the valuation date, so the rate is level and reads neither clock.  A CMT path would
    be another input table, read on the valuation clock, each contract taking the change on
    it from the later of its annuity date and the valuation date, the instant its column is
    measured to.  Any run with commutation enabled inherits an unsupported assumption; flag
    it in output.
    """
    shift = cmt10_shift if t_entry() == 0 else 0.0                   # noqa: F821
    return commute_disc_rate_base + cmt10_shift_init() + shift       # noqa: F821


def is_disc_compound():
    """Whether the commuted value discounts at compound interest: the Reference decoded.

    ``commute_disc_convention`` is ``COMPOUND`` (the default **[std]**) or ``SIMPLE`` (per
    [S7]), the int codes of ``SPIA_US_S``'s ``"compound"`` and ``"simple"``; any other value
    raises, text among them in modelx, which a compiled model cannot hold.  A decode, so
    that :func:`commuted_value` branches on a flag rather than on a Reference.  It raises
    for an invalid convention whenever a certain month remains to discount, where
    ``SPIA_US_S`` raises at the first instalment it discounts.
    """
    if commute_disc_convention == COMPOUND:                          # noqa: F821
        return True
    if commute_disc_convention == SIMPLE:                            # noqa: F821
        return False
    raise ValueError("invalid commute_disc_convention")


def commuted_value(t):
    """CV(t): the commuted value of the remaining certain instalments [S1].

    ``CV(t) = sum over policy months s in T, m < s < n_eff of inst(s) * (1 - theta_cum(t))
    * v(m, s)``, ``m = duration_mth(t)`` - the instalments of the policy months still to
    come inside the certain period, which ends with policy month ``n_eff - 1`` - with, per
    the ``commute_disc_convention`` Reference (:func:`is_disc_compound`)::

        compound (default [std]):      v = (1 + j)^(-(s-m)/12)
        simple   (per [S7]):           v = max(0, 1 - j*(s-m)/12)

    Only the certain tail is discounted; the life-contingent payments after the certain
    period are untouched by a commutation [S1][S2][S5].  A rate ``j`` below -100%, a
    change in the CMT of more than about -104%, raises a negative number to a fractional
    power under the compound convention, which modelx returns as a complex number and the
    compiled model, whose power is C's, as NaN; no rate reaches it.  The instalments are
    read from the schedule by policy month, :func:`annuity_pp_sched_pm`, in one loop, so
    that no month of the frame ahead of t is read.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    n_eff = certain_mths_eff()
    m = duration_mth(t)
    if m + 1 >= n_eff:
        return 0.0
    j = commute_disc_rate(t)
    compound = is_disc_compound()
    total = 0.0
    for k in range(m + 1, n_eff):
        inst = annuity_pp_sched_pm(k)
        if inst == 0.0:
            continue
        yrs = (k - m) / 12.0
        if compound:
            v = (1.0 + j) ** (-yrs)
        else:
            v = max(0.0, 1.0 - j * yrs)
        total += inst * v
    return total * (1.0 - commute_frac_cum(t))


def commute_amount(t):
    """W: the gross withdrawal taken in month t [S1]; zero in the base run.

    ``W = u(y) * CV(t)``, then constrained by the published limits: at least $5,000, at
    most ``CV(t)``, and leaving every remaining guaranteed payment at or above $100.  The
    residual floor is applied as a **cap** on W rather than a rejection, so a large
    requested utilization degrades to the largest admissible withdrawal; if that is below
    the $5,000 minimum, nothing is withdrawn.  The smallest remaining certain instalment,
    which the floor binds on, is found by one loop over the policy months still to come,
    on the schedule :func:`annuity_pp_sched_pm`.
    """
    if not commute_elig(t):
        return 0.0
    cv = commuted_value(t)
    if cv <= 0.0:
        return 0.0
    th = commute_frac_cum(t)
    n_eff = certain_mths_eff()
    smallest = 0.0
    for k in range(duration_mth(t) + 1, n_eff):
        inst = annuity_pp_sched_pm(k)
        if inst > 0.0 and (smallest == 0.0 or inst < smallest):
            smallest = inst
    if smallest == 0.0:
        return 0.0
    th_max = 1.0 - commute_min_payment / smallest                    # noqa: F821
    if th_max <= th:
        return 0.0
    w_max = cv * (th_max - th) / (1.0 - th)
    w = min(commute_util_rate(policy_year(t)) * cv, cv, w_max)
    return w if w >= commute_min_amount else 0.0                     # noqa: F821


def commute_frac_cum(t):
    """theta_cum(t): the cumulative commutation fraction applying in month t.

    Measured *before* any withdrawal taken in month t, because the notes' processing
    order records the instalment (step 3) before the commutation (step 5)::

        theta_cum(t+) = theta_cum(t) + (1 - theta_cum(t)) * W / CV(t)

    This is one carrier's pro-rata rule: future income payments through the end of the
    guaranteed period are reduced by the withdrawal percentage elected, with full payments
    resuming for life at the end of that period [S5][S2].  It applies to certain-period
    instalments **only** - applying it to the life-contingent tail contradicts every
    retrieved contract [S1][S2][S5], which is why :func:`annuity_payments` multiplies it
    by ``C(t)``.

    At :func:`t_entry`, the first month on the books, it is the opening state,
    :func:`commute_frac_cum_init`: the fraction commuted before the valuation date, which
    reduces month 0's instalment, for a contract in payment, and 0 for one commencing at or
    after it.  A withdrawal taken in month t first reduces the instalment of month
    ``t + 1``.  Zero outside the frame.
    """
    if not is_active(t):
        return 0.0
    if t == t_entry():
        return commute_frac_cum_init()
    prev = commute_frac_cum(t - 1)
    cv = commuted_value(t - 1)
    w = commute_amount(t - 1)
    if cv <= 0.0 or w <= 0.0:
        return prev
    return prev + (1.0 - prev) * w / cv


def surr_charge_rate(y):
    """sc(y): the surrender charge on a commutation in contract year y [S1].

    8% in year 2 grading to 1% in year 9 and 0% from year 10 - the only published SPIA
    surrender-charge schedule found.  Contract years below and above the table's range
    take its first and last rows; year 1 is barred from withdrawing at all, so its rate
    is never reached through :func:`commute_amount`.  The years, the first and last among
    them, and the rates are read from the scale ``Data`` has checked: the year is clamped
    to ``Data.surr_charge_year_first`` and ``Data.surr_charge_year_last``, and the rate
    read from ``Data.surr_charge_rate_array`` at it, where ``SPIA_US_S`` takes the first
    and last years from the raw table.
    """
    lo = data.surr_charge_year_first()                               # noqa: F821
    hi = data.surr_charge_year_last()                                # noqa: F821
    return float(data.surr_charge_rate_array()[min(max(y, lo), hi)])  # noqa: F821


def surr_charge(t):
    """The surrender charge retained by the insurer on a commutation in month t [S1].

    On the contracts on the books, at the contract year's rate; zero outside the frame,
    before the contract year is read.
    """
    if not is_active(t):
        return 0.0
    return (pols_if_at(t, BEF_DECR) * commute_amount(t)              # noqa: F821
            * surr_charge_rate(policy_year(t)))


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(t // 12)`` **[std]**.

    On the **valuation** clock: ``SPIA_US_S``'s annual steps, ``(1 + pi)^(y(t) - 1)``,
    moved onto ``t``, so that the maintenance charge it inflates is in valuation-date
    dollars, whatever the contract's age, and every point of a block inflates alike,
    stepping on each anniversary of the valuation date.  On a point commencing at
    ``t = 0`` the two are the same.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def annuity_pp_paid(t):
    """The instalment per contract after any prior commutation, before survival weighting.

    ``inst(t) * (1 - theta_cum(t)*C(t))``: a commutation reduces certain-period
    instalments only.
    """
    return annuity_pp(t) * (1.0 - commute_frac_cum(t) * certain_floor(t))


def annuity_payments(t):
    """E[ANN(t)]: expected annuity outgo in month t.

    ``inst(t) * Phi(t) * (1 - theta_cum(t)*C(t))``, on the contracts on the books,
    ``pols_if_at(t, BEF_DECR)``.  This is the column the notes' worked-example table
    labels "CF": at t = 0 on point 1 it is 500.00, the instalment alone, with the
    maintenance expense carried separately in :func:`liability_cf`.
    """
    return pols_if_at(t, BEF_DECR) * annuity_pp_paid(t) * payment_factor(t)  # noqa


def claim_pp(t, kind):
    """The claim amount per contract in month t, by ``kind``.

    ``REFUND`` - the cash refund lump sum ``max(0, P - G)``, zero on any form other
    than cash_refund [S1][S3][S5].  Because :func:`cum_annuity_pp` is indexed by a time
    point on the policy clock, the balance is measured at ``G(m)``,
    ``m = duration_mth(t)``, on arrears - everything paid before month t opened, which is
    the notes' "instalments already paid" for a mid-month death; in an **advance** payment
    month the instalment paid at the *start* of the death month has been paid, so
    ``G(m + 1)`` is used or the lump sum is overstated by one instalment.  On the cash
    refund in payment 13 months, point 17, that is 100,000 - G(13) = 93,485.00 at
    ``t = 0``.  Zero outside the frame; any other kind raises, a string among them in
    modelx.
    """
    if kind != REFUND:                                               # noqa: F821
        raise ValueError("invalid kind")
    if not is_active(t) or not is_cash_refund():
        return 0.0
    k = duration_mth(t)
    if not is_arrears() and is_payment_mth(t):
        k += 1
    return max(0.0, premium_pp() - cum_annuity_pp(k))


def claims(t):
    """E[CR(t)]: expected claim outgo in month t, the cash refund.

    The only kind on this product is ``REFUND``, so this is its formula and the total
    alike: ``SPIA_US_S``'s ``claims(t, kind=None)`` returns ``claims(t, "REFUND")``, whose
    value this is, the same product in the same order, with no ``0.0 +`` that would turn
    a ``-0.0`` into ``0.0``.  It is weighted by :func:`lives_death_last`, the notes'
    ``d_term`` - the death that terminates the income stream, which is the primary's on a
    single-life contract and the last death on a joint one (a cash refund on a joint
    contract is offered only at delta = 100% [S5]) - on the contracts on the books,
    ``pols_if_at(t, BEF_DECR)``.  The twin identity reaches ``SPIA_US_S``'s two keys,
    ``(t, None)`` and ``(t, "REFUND")``, through the spec's ``twin_arg_map``.
    """
    return pols_if_at(t, BEF_DECR) * lives_death_last(t) * claim_pp(t, REFUND)  # noqa


def commutations(t):
    """E[COMM(t)]: the commutation payment made to the owner in month t [S1].

    ``W * (1 - sc(y))`` - the withdrawal net of its surrender charge, on the contracts on
    the books.  Zero in the base run, where utilization is zero, and outside the frame,
    before the contract year is read.
    """
    if not is_active(t):
        return 0.0
    return (pols_if_at(t, BEF_DECR) * commute_amount(t)              # noqa: F821
            * (1.0 - surr_charge_rate(policy_year(t))))


def expenses(t):
    """E[EXP(t)]: maintenance expense in month t **[std]**.

    ``(c_e / 12) * (1 + pi)^(t // 12) * IF(t)``: $60 per contract p.a. inflating at 2.5% on
    the valuation clock (:func:`inflation_factor`), paid monthly while any payment
    obligation remains.  No insurer publishes expense assumptions; the "zero fees"
    statement [S1] refers to charges to the policyholder, not to the insurer's cost.
    Acquisition cost is out of scope - the premium is single and the cost is priced in -
    so an annuity commencing after the valuation date brings none either.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def liability_cf(t):
    """CF(t): total gross liability outgo in month t, the notes' cash flow definition.

    ``E[ANN] + E[CR] + E[COMM] + E[EXP]``.  **Outgo positive**, the notes' own sign, and
    the sum of the cash flow columns of :func:`result_cf`.  There is no premium income
    in the projection - the single premium at the annuity date is a pricing input - and
    no surrender outgo, because the contract has no cash value at any time [S1][S4][S5].
    Note that the worked-example table's "CF" column is :func:`annuity_payments`, not this.

    Both signs are published, here and in :func:`net_cf`, so that the notes' stream
    survives verbatim under the name the notes give it while the library-wide
    income-positive convention is available under the name every other model uses.
    """
    return annuity_payments(t) + claims(t) + commutations(t) + expenses(t)


def net_cf(t):
    """Net cash flow to the insurer in month t: income less outgo, so ``-liability_cf``.

    **Income positive**, the sign convention of ``Term_US_S.net_cf``, kept even though
    this product has no projected income so that every model's ``net_cf`` can be compared
    or summed across the library.  :func:`liability_cf` carries the opposite, outgo-positive
    sign of the technical notes; both are published as columns of :func:`result_cf` rather
    than one being made to stand for the other.
    """
    return -liability_cf(t)


def check_lives_roll_fwd_resid(t):
    """Residual between :func:`lives_if` and an independently rebuilt survival path.

    Indexed by a **time point** on the valuation clock, like :func:`lives_if` itself:
    time 0 is the valuation date and the residual is checked over ``t = 0 ...
    proj_len()``, the opening and closing time of every projected month.  It is zero
    before the contract is on the books, where both sides are 0.

    Deliberately **not** the telescoping identity ``l_i(t) - d_i(t) - l_i(t+1)``:
    :func:`lives_death` is *defined* as that difference, so the identity is identically
    zero whatever :func:`lives_if` returns and constrains nothing.  Each life's survival
    is rebuilt here from the opening state and the assumptions instead, with no reference
    to the recursion - on the *table* basis as :func:`lives_if_init` times the running
    product ``prod_{s = t_entry() ... t-1} (1 - q_m(s, i))`` over the months that have
    closed since the contract came on the books, which a misindexed or mis-based recursion
    breaks - and the residual is the sum of the per-life differences.

    On the *scenario* basis ``lives_if`` is closed form, so there is no recursion to
    close and that leg only restates the step function; the substantive check is the
    table one.  On a joint contract the last-survivor identity
    ``l_last(t) - [l_1 + l_2 - l_1*l_2]`` is added.  That term *is* zero by construction,
    like :func:`check_payment_factor_resid`, and exists to catch a future redefinition of
    :func:`lives_if_last` that broke the independence construction.
    """
    res = 0.0
    entry = t_entry()
    for i in range(1, 3):
        if i == 2 and not is_joint():
            continue
        if t < entry:
            built = 0.0
        elif is_scenario():
            d = death_mth(i)
            built = 0.0 if (d >= 0 and duration_mth(t) > d) else 1.0
        else:
            built = lives_if_init(i)
            for s in range(entry, t):
                built *= 1.0 - mort_rate_mth(s, i)
        res += built - lives_if(t, i)
    if is_joint():
        l1 = lives_if(t, 1)
        l2 = lives_if(t, 2)
        res += lives_if_last(t) - (l1 + l2 - l1 * l2)
    return res


def check_lives_roll_fwd():
    """Whether the survival recursion closes at **every** projected time point.

    Takes no argument and returns a ``bool``, the library-wide shape of a ``check_*``
    cells, so one test can call the same check across every model.  It is
    ``all(abs(check_lives_roll_fwd_resid(t)) < 1e-10)`` over the time points
    ``t = 0 ... proj_len()``, the valuation date through the closing time of the last
    projected month; before the contract is on the books both sides are 0.  The signed
    residual of a failing time point is the more useful object when it does fail, and
    stays available as :func:`check_lives_roll_fwd_resid`.

    The tolerance is absolute, not relative: the residual is a difference of survival
    probabilities that is zero when the model is right, and ``math.isclose(x, 0.0)``
    is False for every nonzero ``x`` at the default relative tolerance.
    """
    return all(abs(check_lives_roll_fwd_resid(k)) < 1e-10
               for k in range(proj_len() + 1))


def check_payment_factor_resid(t):
    """``Phi(t) - max(C(t), L(t))``: the certain-period double-count guard.

    Zero by construction.  It is asserted anyway because an additive floor - ``C + L``
    instead of ``max(C, L)`` - is the notes' first-listed pitfall and would show up here
    as ``min(C, L)``.
    """
    return payment_factor(t) - max(certain_floor(t), payment_factor_life(t))


def check_payment_factor():
    """Whether the master payment factor is the certain floor at **every** projected month.

    No argument, returns a ``bool``, implemented as
    ``all(abs(check_payment_factor_resid(t)) < 1e-10)`` over ``t = 0 ... proj_len() - 1``.
    See :func:`check_payment_factor_resid` for what the residual catches and why a
    quantity that is zero by construction is checked at all.
    """
    return all(abs(check_payment_factor_resid(t)) < 1e-10
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, one row per month ``t = 0 ... proj_len() - 1``.

    Row 0 is the valuation month for every model point, so the frames of a block line up
    and sum row by row; a point commencing after the valuation date has zeros until the
    month its annuity commences.  The columns are ``SPIA_US_S``'s.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims": [claims(t) for t in ts],
            "commutations": [commutations(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of the counts, survival probabilities and payment factors, by month t.

    One row per projected month, ``t = 0 ... proj_len() - 1``: ``pols_if``, the closing
    obligation measure, and ``pols_new_biz``, the annuities commencing in the month, as
    ``basiclife.BasicTerm_SE``'s ``result_pols`` sets its counts out first; then
    ``SPIA_US_S``'s other columns in ``SPIA_US_S``'s order.  The survival columns are the
    **end-of-month** values, i.e. :func:`lives_if` read at time ``t + 1``, so each row
    reports the state the month closes in - which is the state the arrears instalment of
    that month is paid on, and the one the maintenance expense is carried on - and every
    column is 0 in the months before a point's annuity commences.  The count on the books
    that weights the cash flows is not a column: it is the table's ``policy_count``, from
    the annuity date to the stop rule.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "lives_if_1": [lives_if(t + 1, 1) if is_active(t) else 0.0 for t in ts],
            "lives_if_2": [lives_if(t + 1, 2) if is_active(t) else 0.0 for t in ts],
            "lives_if_last": [lives_if_last(t + 1) if is_active(t) else 0.0
                              for t in ts],
            "lives_death_last": [lives_death_last(t) for t in ts],
            "certain_floor": [certain_floor(t) for t in ts],
            "payment_factor_life": [payment_factor_life(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

BEF_NB = 0

BEF_DECR = 1

REFUND = 0

COMPOUND = 0

SIMPLE = 1

issue_age_min = 0

omega_age = 120

mort_table_year = 2012

mort_ae_factor = 1.084

expense_maint = 60.0

inflation_rate = 0.025

commute_util_base = 0.0

commute_disc_rate_base = 0.04

cmt10_shift = 0.0

commute_disc_convention = 0

commute_min_amount = 5000.0

commute_min_payment = 100.0

pd = ("Module", "pandas")