# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.VUL_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.VUL_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is: ``Projection[5]``
is an ItemSpace projecting the table's sixth row, model point 6, ``VUL_US_S``'s in-force
point restated six months on, in force 126 months at the valuation date with its fixed
option and its loan, and :func:`point_id` is its label::

    >>> Projection[5].result_cf()          # one row per month from the valuation date
    >>> Projection[5].result_av()          # the account value roll-forward behind it
    >>> Projection[5].point_id()           # 6, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, and an int set on a float Reference reads as a float
(``products/variable_ul/model-sec.md``, *What it refuses*).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.VUL_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.VUL_US_S` is rewritten where it depends on where the projection starts, where it
must answer for a month outside cover, or where it reads a table at a policy year or an
attained age; every other is :mod:`~.VUL_US_S`'s own.
``products/variable_ul/model-sec.md`` lists the rewritten cells with the reason for
each. Making it compile changed how each cell reads its inputs and spells its codes, and
no number: every model point attribute a projection cell uses is read as a number from a
``Data`` vector, every table as an array indexed by integers, the return scenario among
them, every timing and kind is an int code (*Codes*, below), and a subaccount is its
position in the lineup, from 0, where :mod:`~.VUL_US_S` names it by its id.
:mod:`~.VUL_US_S`'s ``subaccount_ids``, a list, is a count, :func:`subaccount_count`; its
``coi_rate_scale``, a Series, is a schedule number, :func:`coi_schedule`; its
``claims(t, kind=None)`` is two cells and their total, :func:`claims_death`,
:func:`claims_lapse` and :func:`claims`; and its ``me_charge_pp(t, i=None)`` is a cell
of a subaccount, :func:`me_charge_sa_pp`, and their total, :func:`me_charge_pp`. Its eight
sums of a generator over the lineup are loops from 0.0, the same floats on the shipped
lineup of two.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/variable_ul/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VUL_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers live in the unparameterized :mod:`~.VUL_US_SEC.Data` Space, reached here
through the ``data`` Reference, so each file is read once per model rather than once
per model point. The nine assumption tables are the files :mod:`~.VUL_US_S` reads, read
in place; the model point table is this model's own:

======================  ================================  ==========================
Reference (on Data)     Cells                             File
======================  ================================  ==========================
model_point_file        data.model_point_table()          model_point_table_sec.csv
subaccount_file         data.subaccount_table()           subaccount_table.csv
scenario_file           data.scenario_table()             scenario_table.csv
coi_rates_file          data.coi_rates()                  coi_rates.csv
corridor_file           data.corridor_factors()           corridor_factors.csv
mort_table_file         data.mort_table()                 mort_table.csv
class_factor_file       data.class_factor_table()         class_factor_table.csv
lapse_table_file        data.lapse_table()                lapse_table.csv
prem_persistency_file   data.prem_persistency_table()     prem_persistency.csv
surr_charge_file        data.surr_charge_table()          surr_charge_table.csv
======================  ================================  ==========================

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however old the policy, month ``t`` runs from the monthiversary at time ``t`` to
the next, and the frame is ``t = 0, 1, ..., proj_len() - 1``, where :func:`proj_len`
counts the months from the valuation date to the end of the projection. Row ``t`` is the
same month for every point, so the frames of a block line up and sum row by row.

``duration_mth(t)`` counts **policy months**, the months the policy has been in force at
time ``t``: ``duration_mth(t) = duration_mth_init() + t``, where :func:`duration_mth_init`
is read from the model point -- positive for a policy in force at the valuation date, in
any month of its policy year, 0 for one issued at it, ``-k`` for one issued ``k`` months
later, at most ten years later. Everything contractual reads it: the surrender charge and
the loan tier by policy year and the lapse spike at the surrender charge's cliff, the COI
scale, the base lapse rate and the premium persistency scale by policy year, the corridor
factor and the mortality rate at the attained age, the end of premiums, withdrawals and
monthly deductions at attained age 121, and the single premium and acquisition in the
issue month. The policy year is the 1-based contractual label
``policy_year(t) = duration(t) + 1`` and the attained age (ANB) is
``age(t) = age_at_entry() + duration(t)``, both derived and never indexed by. Point 4,
``VUL_US_S``'s in-force cell, is in policy year 11 at attained age 55 at ``t = 0``, and
point 9, to be issued 25 months after the valuation date, is issued at ``t = 25``.

``VUL_US_S`` already counts its months from the start of its own projection rather than
from issue, and opens its in-force points 1, 2 and 4 there with their subaccounts, their
fixed option and their loan. What the valuation clock adds is that ``t = 0`` is one
instant for every point, that a point may be issued after it, and that a point in force
brings in what its past has left it: the loan account, which grows at the rate credited
to it while the debt grows at the rate charged, so that the two part once interest
accrues, and the face its withdrawals have left, two more opening values than
``VUL_US_S`` reads.

The economic inputs read the valuation clock. The separate-account return scenario,
:func:`gross_return_mth`, is a path of the economy from the valuation date, month ``t``
the same month for every point, however old the policy; ``VUL_US_S`` keys it by its own
projection month already. The declared fixed rate, :func:`crediting_rate_ann`, is flat
as shipped. Expense inflation is ``inflation_factor(t) = (1 + inflation_rate)^(t // 12)``,
``VUL_US_S``'s step by policy year moved onto ``t``, so that the maintenance expense is
in valuation-date dollars for every point alike; it is 0 as shipped. Acquisition is
charged per policy issued, in the issue month, and is not inflated, as in
``basiclife.BasicTerm_SE``. The two first-month pins, ``corridor_override_m1`` and
``coi_rate_override_m1``, apply in the valuation month, ``t = 0``: the month the worked
example describes, on point 1, which is in force there. The pricing path behind the
funding ratio is a projection made at issue, keyed by the policy month from issue; it
reads no state and nothing on the valuation clock (see :func:`funding_ratio`).

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.VUL_US_S` computes: every cell the two share agrees at every argument
:mod:`~.VUL_US_S` evaluates in its sweep, but for three whose meaning changed,
``pols_if_init``, now the count already in force at the valuation date, ``model_point``,
a row of another table, and ``result_pols``, which gains the month's new business.
``tests/test_model_conventions.py`` asserts it cell by cell. On points 1, 2 and 4,
:mod:`~.VUL_US_S`'s in-force points, the projection is :mod:`~.VUL_US_S`'s too, month for
month, from ``t = 0``: each opens with :mod:`~.VUL_US_S`'s own opening balances, and its
two new columns hold what :mod:`~.VUL_US_S` assumes there, the loan account equal to the
debt and the face at issue. That is how the worked example's month, which
:mod:`~.VUL_US_S`'s tests assert at ``t = 0`` on point 1, carries over.

The **value** state variables are closing balances at the end of month ``t``:
``sa_pp(t, i)``, ``fa_pp(t)``, ``la_pp(t)``, ``loan_bal_pp(t)`` and ``av_pp(t)``.
``sum_assured_at(t)`` is not a closing balance: it is the face amount in force **during**
month ``t``, after that month's BOM withdrawal reduction. The opening value is the
``BEF_PREM`` timing of the matching ``*_at`` cells -- ``sa_pp_at(t, i, BEF_PREM)``,
``fa_pp_at(t, BEF_PREM)``, ``la_pp_at(t, BEF_PREM)``, ``loan_bal_pp_at(t,
BEF_PREM)``, ``av_pp_at(t, BEF_PREM)`` -- which is the previous month's closing
balance, and at :func:`t_entry`, the first month on the books, the model point's opening
state instead, so that nothing is ever asked for a month before the valuation date or
before issue. For a point in force the opening state is six columns of its row, per
policy, as the policy stands at the start of month 0, before any month-0 event: each
subaccount and the fixed option, ``VUL_US_S``'s own columns (:func:`sa_pp_init`,
:func:`fa_pp_init`); the loan account (:func:`la_pp_init`); the debt, ``VUL_US_S``'s own
(:func:`loan_bal_init`); and the face in force (:func:`sum_assured_init`). ``VUL_US_S``
takes the loan account equal to the debt there, and the face at issue, on its in-force
points too. For a point issued at or after the valuation date every one of them is 0,
and the issue values come from the formulas: :func:`sum_assured` for the face, 0 for the
rest. The notes' ``SA_i(0)``, ``FA(0)``, ``LA(0)``, ``D(0)`` and ``F(0)`` are these
opening values, and ``l_0`` is the count the point opens with (see *Counts*, below).

Every chain is one cell a month. Each opening timing forms the previous month's close
itself, from its own value at ``t - 1`` and month ``t - 1``'s premium, withdrawal,
deduction and growth, the same products in the same order as the closing cell
``VUL_US_S`` calls for, rather than calling for it: a subaccount's, where
``VUL_US_S``'s chain ran through six cells a month, the fixed option's, through five, and
the loan account's and the debt's, through two. The subaccounts and the fixed option
share each month's withdrawal and deduction pro rata, so the first of them called runs
the others alongside it, a month at a time. The face calls itself at ``t - 1`` before
anything else, and the count, the ``BEF_NB`` timing of :func:`pols_if_at`, forms the
previous month's survivors itself, one cell a month as ``VUL_US_S``'s :func:`pols_if`
already was. A compiled model runs these chains on the C stack.

Within each month the notes' monthiversary order is followed exactly:

1. advance the policy year, the attained age and the year-dependent parameters -- the
   loan tier (:func:`loan_rate_ann`), the surrender charge (:func:`surr_charge_rate`)
   and the corridor factor (:func:`corridor_factor`);
2. gross premium and its load, the net premium allocated by :func:`alloc` and
   :func:`alloc_fixed` (:func:`premium_pp`, :func:`prem_to_av_pp`);
3. withdrawal and the $25 fee, taken pro rata from the unloaned accounts, and under
   Option A the proportionate face reduction they force (:func:`wd_pp`,
   :func:`wd_fee_pp`, :func:`face_reduction_pp`, :func:`sum_assured_at`) -- after which
   the account value is :func:`av_pp_at(t, BEF_FEE)<av_pp_at>`, the notes'
   post-premium value;
4. loan activity -- not modeled; the opening debt and collateral roll forward;
5. death benefit and the GPT corridor test (:func:`db_pp`), then the net amount at
   risk (:func:`net_amt_at_risk`), **with no one-month discount**;
6. the monthly deduction (:func:`mth_deduction_pp`), allocated across the unloaned
   accounts pro rata (:func:`mth_deduction_sa_pp`, :func:`mth_deduction_fa_pp`);
7. growth over the month: the separate-account unit-value factor
   (:func:`inv_return_mth`), fixed-option interest (:func:`fixed_return_mth`), loan
   account interest (:func:`loan_cr_rate_mth`) and debt accrual
   (:func:`loan_rate_mth`);
8. end of month: the death benefit and net amount at risk recomputed on end-of-month
   balances (:func:`db_pp_eom`, :func:`net_amt_at_risk_eom`), then the decrements,
   death before lapse (:func:`pols_death`, :func:`pols_lapse`);
9. the default test (:func:`is_default`) -- a diagnostic; see the model docstring.

Cash flows are **undiscounted**. Premiums, expenses and percent-of-premium expenses
fall at BOM and are weighted by ``pols_if(t)``; death claims by
``pols_if(t) * mort_rate_mth(t)``; surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, BEF_DECR)``, the
count carried in from ``t - 1`` (``BEF_NB``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, and before issue
(:func:`is_active`) every count, and so every cash flow, is zero, and so is every value
state. ``VUL_US_S`` already names three timings, in a cell that returns ``pols_if(t)``
for each and that nothing calls. ``BEF_DECR`` keeps that meaning, and so does
``BEF_MAT``, the count before any maturity, since nothing matures: the name keeps its S
model's meaning, as in the family's other models, and ``basiclife.BasicTerm_SE``'s
start-of-month ``BEF_MAT`` is not adopted. ``BEF_NB`` is the one timing this model
gives a new meaning, ``basiclife.BasicTerm_SE``'s, and it differs from ``VUL_US_S``'s only
in the issue month, where it counts the issued policies as new business, not yet in.
Inside the month the decrements are :mod:`~.VUL_US_S`'s, death before lapse.

.. rubric:: The end of the projection

The frame ends at :func:`omega_mth`, the first policy month at attained age 122, where the
mortality table has ended, and not at an event of the contract, which never matures. With
the shipped table -- an annual rate of 1.0 from attained age 119 -- and a class factor and
an A/E of 1 or more, every life has died by the end of the first month at attained age
119. With a preferred class, an A/E below 1, or a table that stays below 1, lives survive
the last month, and the roll-forwards read them: :func:`check_av_roll_fwd` and
:func:`av_change` read the opening account value in force of month ``t + 1``, which in
the last month is ``t = proj_len()``. So the two opening values they read there, the
count (the ``BEF_NB`` timing of :func:`pols_if_at`, and through it :func:`pols_if`) and
the account value (``av_pp_at(t, BEF_PREM)``), are defined for
``0 <= duration_mth(t) <= omega_mth()``: on the books, and in the month after the frame,
where they are the survivors of the last month and the account value they carry. Both
equal :mod:`~.VUL_US_S`'s values there exactly. Every other cell is zero or false there,
as before issue: each account inside the month and its opening value, the debt, every
charge, premium, withdrawal, decrement rate, decrement, claim and flow, and the expenses,
whose maintenance would otherwise fall on the carried count; only the two clocks, the
inputs read on the valuation clock, the loan account's level credited rate and the
neutral 1.0 of the two lapse multipliers and the funding ratio hold values there. A loan
account carried into the month would earn a month's credit past the end of the frame.
And nothing reads past ``t = proj_len()``: :func:`av_change` and the three checks'
residual cells, which read ``t + 1``, are zero outside cover before they read it.

.. rubric:: Two views of the same run

The notes require two reports and warn that confusing them is "a common specification
error". :func:`result_cf` is the **gross (policyholder) view**: the insurer's liability
outflow on death is the *full death benefit less policy debt*, and the account value
seized is the *funding* of part of it. :func:`result_net` is the **net-of-account
(general-account strain) view**, derived arithmetically from the same run: the margins
collected (premium loads, monthly deductions, M&E, loan spread, surrender charges) less
the net mortality cost :func:`claims_net`, which is the net amount at risk. Projecting
``DB - AV`` as the claim understates gross benefit outgo; projecting the full death
benefit *and* separately expensing the net amount at risk double counts.
:func:`check_net_view` pins the two views to each other.

.. rubric:: Naming

Cell names follow :mod:`.UL_US_S` -- the universal-life chassis this product is
built on -- and through it lifelib's ``basiclife.BasicTerm_S`` and
``savings.CashValue_SE``: ``pols_*`` for policy counts, ``av_*`` for account values,
plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``timing`` and ``kind`` arguments. Names are added only where variable UL has a
concept fixed universal life does not: the subaccount vector, the fixed option, the
loan account, the M&E charge, the return scenario, the funding ratio and the pricing
path.

What running in force adds is named as ``basiclife.BasicTerm_SE`` names it:
``duration_mth`` read from the model point, ``policy_count``, ``pols_new_biz``,
``pols_if_at`` with its ``BEF_NB`` timing, ``is_active`` and ``result_pols``.
``t_entry``, the first month on the books, is the SEC models' own, and ``omega_mth`` is
named for ``omega_age``, where the projection ends, since the contract has no end of its
own; both are ``UL_US_SEC``'s, the chassis's in-force model. A column of the opening state
is the cell it opens with ``_init`` added, in ``VUL_US_S``'s spelling of the stem:
``sa_pp_init``, ``fa_pp_init`` and ``loan_bal_init`` are ``VUL_US_S``'s own,
``la_pp_init`` opens :func:`la_pp_at` as they open theirs, and ``sum_assured_init`` is
``UL_US_SEC``'s name for the face in force. A table read at a policy year has one reader
keyed by the year, ``<cell>_py(y)``, or ``VUL_US_S``'s ``coi_rate_guar_at(y)``, kept, and
a table read at an attained age one keyed by the age, ``<cell>_at(a)``; the monthly cell
keeps ``VUL_US_S``'s name and calls it inside cover. The surrender-charge schedule, keyed
by its ID, has one reader for each of its two columns, :func:`surr_charge_rate_max` and
:func:`surr_charge_runoff_years`, and the return scenario a reader of its extent,
:func:`scenario_last_mth`; the COI scale, keyed by sex, class and issue age, is numbered,
:func:`coi_schedule`, and so is the return scenario, keyed by its ID,
:func:`scenario_index`. A check's residual in month t is ``<check>_resid(t)``. A text
column a monthly cell branches on is read through bool decodes, one for each value it
branches on, named for the value: :func:`is_db_option_a` and :func:`is_db_option_b`,
:func:`is_gpt`, and :func:`is_level_premium` and :func:`is_single_premium`. No projection
cell reads text: ``Data`` decodes each column into its flags, and joins the class factor,
the COI scale, the surrender-charge schedule and the return scenario to the points by
their text keys, so ``VUL_US_S``'s label accessors are kept for reporting alone
(*Reporting cells*, below). Each first-month pin is read once a point, a value and
whether the point gives one: :func:`corridor_override_m1` and
:func:`has_corridor_override_m1`, :func:`coi_rate_override_m1` and
:func:`has_coi_rate_override_m1`. Each of ``VUL_US_S``'s two claim kinds is a cell,
``claims_<kind>(t)``, and :func:`claims` their total, as in the family's other compiled
models; and a subaccount's share of an amount is ``<amount>_sa_pp(t, i)``, as
:func:`wd_sa_pp` and :func:`mth_deduction_sa_pp` already were, so the M&E charge of one
subaccount is :func:`me_charge_sa_pp` and :func:`me_charge_pp` their total.

The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Months from the valuation date
(policy year)              policy_year(t)                  Policy year, 1-based label
(months since issue)       duration_mth(t)                 Completed policy months at
                                                           month t
(completed years)          duration(t)                     Completed policy years
(issue age)                age_at_entry                    Issue age (ANB)
x_t                        age(t)                          Attained age (ANB)
(none)                     proj_len                        Months from the valuation date
                                                           to the end of the projection
(table's last age)         omega_age                       Last age of the table, 121
(projection end)           omega_mth                       Policy month the projection
                                                           ends at, attained age 122
(none)                     t_entry                         First month on the books
(none)                     is_active(t)                    Whether month t is in cover
(months at valuation)      duration_mth_init               Completed policy months at the
                                                           valuation date; -k if issued k
                                                           months later
(none)                     policy_count                    Policies the model point
                                                           stands for
(none)                     point_id                        The model point's label
F_0                        sum_assured                     Initial face amount
F_t                        sum_assured_at(t)               Face after reductions
F(0)                       sum_assured_init                Face in force entering month 0
(F_0 / 1000)               units                           Initial face in $1,000s
(death benefit option)     db_option                       Death benefit option, A or B
(Option A)                 is_db_option_a                  Whether db_option is A
(Option B)                 is_db_option_b                  Whether db_option is B
(qualification test)       qual_test                       7702 test elected; GPT only
(GPT elected)              is_gpt                          Whether qual_test is GPT
(premium pattern)          premium_type                    LEVEL or SINGLE
(LEVEL pattern)            is_level_premium                Whether premium_type is LEVEL
(SINGLE pattern)           is_single_premium               Whether it is SINGLE
i (subaccount index)       (the ``i`` argument)            Position in the lineup, from 0
(lineup size)              subaccount_count                The lineup's size
alpha_i                    alloc(i)                        Allocation to subaccount i
alpha_F                    alloc_fixed                     Allocation to fixed option
e_i                        fund_expense_ann(i)             Fund expense ratio (annual)
m                          me_rate_ann                     M&E rate (annual)
r_{i,t}                    gross_return_mth(t, i)          Gross subaccount return
(last scenario month)      scenario_last_mth(i)            The scenario's last month
(scenario's number)        scenario_index                  The point's row of the returns
(net unit-value return)    inv_return_mth(t, i)            (1+r)(1-e/12)(1-m/12) - 1
i_fix                      crediting_rate_ann(t)           Declared fixed rate
(monthly fixed rate)       fixed_return_mth(t)             (1+i_fix)^(1/12) - 1
(fixed floor)              guar_rate_ann                   1.0% fixed-option floor
i_L                        loan_rate_ann(t)                Loan rate charged
i_C                        loan_cr_rate_ann(t)             Loan rate credited
P_t                        premium_pp(t)                   Premium paid per policy
(planned)                  premium_pp_ann                  Planned annual premium
rho_t                      prem_persistency(t)             Premium persistency
rho^base_t                 prem_persistency_base(t)        Base persistency factor
(rho^base by year)         prem_persistency_py(y)          The same, keyed by policy year
gamma                      load_prem_rate                  Premium load rate
(net premium)              prem_to_av_pp(t)                Net premium to the accounts
W(t)                       wd_pp(t)                        Partial withdrawal
(planned W)                wd_pp_mth                       The wd_pp column, a month's W
(withdrawal fee)           wd_fee_pp(t)                    $25 withdrawal fee
(face cut)                 face_reduction_pp(t)            Option A face reduction
SA_{i,t+1}                 sa_pp(t, i)                     Subaccount value, EOM
SA_{i,t}                   sa_pp_at(t, i, BEF_PREM)        Subaccount, start of month
SA_i(0)                    sa_pp_init(i)                   Subaccount entering month 0
SA'_{i,t}                  sa_pp_at(t, i, BEF_INV)         Subaccount post-deduction
FA_{t+1}                   fa_pp(t)                        Fixed-option value, EOM
FA_t                       fa_pp_at(t, BEF_PREM)           Fixed option, start of month
FA(0)                      fa_pp_init                      Fixed option entering month 0
LA_{t+1}                   la_pp(t)                        Loan-account collateral, EOM
LA_t                       la_pp_at(t, BEF_PREM)           Collateral, start of month
LA(0)                      la_pp_init                      Collateral entering month 0
D_{t+1}                    loan_bal_pp(t)                  Outstanding policy debt, EOM
D_t                        loan_bal_pp_at(t, BEF_PREM)     Policy debt, start of month
D(0)                       loan_bal_init                   Debt entering month 0
AV_{t+1}                   av_pp(t)                        Total account value, EOM
AV_t                       av_pp_at(t, BEF_PREM)           Account value, start of month
AV(0)                      av_pp_init                      Account value entering month 0
(post-premium AV)          av_pp_at(t, BEF_FEE)            The notes' step-5 balance
(unloaned AV)              unloaned_av_pp_at(t, timing)    Deduction allocation base
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
e_pol                      expense_pol_mth                 $10.00 per-policy charge
e_face                     expense_unit_mth                $0.20 per $1,000 of F_0
rc(t)                      rider_charge_pp(t)              Rider charges (0)
(e_pol + e_face U + rc)    maint_fee_pp(t)                 Non-COI monthly charges
MD_t                       mth_deduction_pp(t)             Monthly deduction
(MD share)                 mth_deduction_sa_pp(t, i)       Pro-rata share, subaccount i
(MD share)                 mth_deduction_fa_pp(t)          Pro-rata share, fixed option
c_t                        coi_rate(t)                     Current monthly COI rate
(c by year)                coi_rate_at(y)                  The rule, keyed by policy year
(first-month COI pin)      coi_rate_override_m1            Pinned c in the valuation
                                                           month, blank if none
(COI pin given)            has_coi_rate_override_m1        Whether the point pins c
(2017 CSO max)             coi_rate_guar(t)                Guaranteed maximum COI rate
(max by year)              coi_rate_guar_at(y)             The same, keyed by policy year
(last year of the scale)   coi_rate_last_year              The scale's last policy year
(COI scale's number)       coi_schedule                    The point's row of the scale
(83.34 cap)                coi_rate_cap                    Monthly COI rate cap
COI_t                      coi_pp(t)                       Cost of insurance charge
kappa_t                    corridor_factor(t)              GPT corridor factor
(kappa by age)             corridor_factor_at(a)           The same, keyed by age
(first-month kappa pin)    corridor_override_m1            Pinned kappa in the valuation
                                                           month, blank if none
(kappa pin given)          has_corridor_override_m1        Whether the point pins kappa
(corridor minimum)         db_corridor_pp(t)               kappa_t x AV
DB_t                       db_pp(t)                        Death benefit, BOM
DB_t^EOM                   db_pp_eom(t)                    Death benefit, EOM
NAAR_t                     net_amt_at_risk(t)              Net amount at risk, BOM
NAAR_t^EOM                 net_amt_at_risk_eom(t)          Net amount at risk, EOM
(M&E collected)            me_charge_pp(t)                 M&E taken in unit values
(M&E by subaccount)        me_charge_sa_pp(t, i)           The same, in subaccount i
(interest credited)        inv_income_pp(t)                Total credit to the accounts
SC_t                       surr_charge_pp(t)               Surrender charge scheduled
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
(initial SC per $1,000)    surr_charge_rate_max            The schedule's charge before
                                                           any run-off
(run-off period)           surr_charge_runoff_years        The schedule's run-off, years
(schedule applies)         has_surr_charge                 Whether a schedule applies
(AV - SC)                  csv_pp(t)                       Cash value before debt
CSV_t                      ncsv_pp(t)                      AV - SC - D, the notes' CSV
(SC collected)             surr_charge(t)                  sc_income
(default test)             is_default(t)                   CSV_t <= 0
(deduction shortfall)      is_shortfall(t)                 Unloaned AV cannot pay MD_t
(none)                     first_default_month()           First month in default
(none)                     first_shortfall_month()         First month short of MD_t
phi_t                      funding_ratio(t)                AV_t / AV*_t
AV*_t                      av_pricing_pp(m)                At-issue pricing path
(pricing fixed rate)       pricing_fixed_return_mth        The fixed option's rate on
                                                           the pricing path
lambda_t                   lapse_rate_dyn_mult(t)          Dynamic lapse multiplier
(SC cliff spike)           lapse_rate_sc_mult(t)           Surrender-charge cliff spike
q^d,annual                 mort_rate(t)                    Annual mortality rate, capped
(base q by age)            mort_rate_base_at(a)            The base table's rate
q^d_t                      mort_rate_mth(t)                Monthly mortality rate
q^w,annual                 lapse_rate(t)                   Total annual lapse rate
q^w_t                      lapse_rate_mth(t)               Monthly lapse rate
q^w,base                   lapse_rate_base(t)              Base annual lapse rate
(q^w,base by year)         lapse_rate_base_py(y)           The same, keyed by policy year
l_t                        pols_if(t)                      In force at start of month t
(l at valuation)           pols_if_init                    In force at the valuation date
(none)                     pols_if_at(t, BEF_NB)           Carried in from month t - 1
(none)                     pols_if_at(t, BEF_DECR)         After new business: l_t
(none)                     pols_if_at(t, BEF_MAT)          Before maturity: l_t
(none)                     pols_new_biz(t)                 Policies issued in month t
(deaths)                   pols_death(t)                   Deaths in month t
(lapses)                   pols_lapse(t)                   Lapses in month t
(none)                     pols_maturity(t)                Maturities: always zero
prem_gross                 premiums(t)                     Premium income
load_income                premium_loads(t)                Premium loads collected
md_income                  mth_deduction(t)                Monthly deductions collected
me_income                  me_charge(t)                    M&E collected
loan_spread                loan_spread(t)                  (i_L - i_C) accrual on D_t
claim_gross                claims_death(t)                 Death claims, DB - debt
claim_net                  claims_net(t)                   Net GA strain, NAAR^EOM
surr_outgo                 claims_lapse(t)                 Surrender payments
(claim outgo)              claims(t)                       Death and surrender claims
(withdrawals)              withdrawals(t)                  Withdrawal payments
sc_income                  surr_charge(t)                  Surrender charges collected
expense                    expenses(t), premium_taxes(t)   Insurer expenses
sa_transfer                sa_transfer(t)                  Separate -> general account
av_eop                     av_at(t, EOM)                   Account value in force, EOM
(net GA cash flow)         net_cf_ga(t)                    Net-of-account view
NetCF(t)                   net_cf(t)                       Gross liability cash flow
(none)                     check_av_roll_fwd_resid(t)      AV roll-forward residual
(none)                     check_margin_resid(t)           Margin identity residual
(none)                     check_net_view_resid(t)         Net view identity residual
(none)                     result_pols()                   Counts and decrement rates
=========================  ==============================  ==========================

Eight names needed care.

``l_t`` in the notes is the in-force probability at the **start** of month ``t`` and
``l_{t+1} = l_t (1 - q^d_t)(1 - q^w_t)`` is its roll-forward; ``pols_if(t)`` follows
``BasicTerm_S`` and is the number in force at the start of month ``t``, after the month's
new business, so the two coincide: ``pols_if(t) = l_t``. On a point issued at ``t = 0``,
``pols_if(0)`` is the issued count, the notes' ``l_0``, while ``pols_if_init()`` is 0,
the count already in force at the valuation date; on a point in force the two are one
count. The notes' roll-forward is the ``pols_if_at(t + 1, BEF_NB)`` step. Every BOM
cash flow is weighted by ``pols_if(t)``.

The notes' ``AV_{t+1}`` is an **end-of-month** balance, not the next month's opening
event: ``av_pp(t)`` is the notes' ``AV_{t+1}`` and ``av_pp_at(t, BEF_PREM)`` is the
notes' ``AV_t``. The same shift applies to ``D_{t+1}``, which is ``loan_bal_pp(t)``,
and to ``LA_{t+1}``, which is ``la_pp(t)``. This is why the notes write the death claim
as ``DB_t^EOM - D_{t+1}``: both are end-of-month quantities of month ``t``.

The notes use ``m`` for the M&E rate and also index the pricing path by policy month.
``me_rate_ann`` names the rate; the pricing-path cells take an argument ``m`` counting
policy months **from issue**, 0-based, which is ``duration_mth(t)`` in month ``t`` -- not
``t`` itself, which counts from the valuation date for every point, issued or not.
``av_pricing_pp(m)`` is the pricing path's closing balance of month ``m`` and
``av_pricing_pp_at(m, BEF_PREM)`` its opening balance, zero at ``m = 0``. A cell of the
pricing path is never asked for a policy month before issue: :func:`funding_ratio`, the
path's one reader in the projection, answers 1.0 outside cover before it computes one.

The notes call ``AV_t - SC_t - D_t`` the cash surrender value ``CSV_t``. The chassis
name for that quantity, net of policy debt, is ``ncsv_pp``; ``csv_pp`` is the
intermediate ``AV_t - SC_t`` before debt. Both are kept so the chassis reads across,
and the symbol table above records which is which.

``coi_rate`` is quoted per $1,000 of net amount at risk **per month** and
``expense_unit_mth`` per $1,000 of face per month, so both are divided by 1,000 -- or
multiplied by :func:`units` -- before they meet a currency amount. :func:`coi_rate` is
therefore not comparable with ``CashValue_SE.coi_rate``, which is a rate per unit of
account value.

:func:`units` takes **no** ``t``. Both the $0.20 monthly charge and the surrender
charge are quoted on ``F_0``, the *initial* face [S2], where the fixed-UL chassis
charges its per-unit fee on the current face and so writes ``units(t)``. Using the
current face here would silently reduce both charges after an Option A withdrawal. The
face in force at the valuation date, :func:`sum_assured_init`, opens the face the death
benefit is measured on, and nothing else.

:func:`maint_fee_pp` is the non-COI part of the *monthly deduction* -- a charge against
the account value, and therefore insurer income. :func:`expenses` is something
different: the insurer's own **[std]** maintenance outgo of $75 per policy per year.
The two must not be confused. Note also that the variable-UL notes specify a flat $75 a
year where the fixed-UL chassis inflates it at 2.5%, so ``inflation_rate`` is **0.0**
here; the cell is kept so the two models read alike.

A partial withdrawal is **not a claim**: it is a payment the owner elects, not an event
that terminates coverage, so it is :func:`withdrawals` in its own ``withdrawals`` column
and neither :func:`claims_death` nor :func:`claims_lapse`, nor their total
:func:`claims`, counts it.  The per-policy amount is still reached through
:func:`claim_pp(t, WITHDRAWAL)<claim_pp>`, which is where the rule that the $25 fee is
not part of the payment is written down, and :func:`withdrawals` weights it by
:func:`pols_if` -- a withdrawal is taken at the monthiversary by policies still in force,
where a death claim is weighted by :func:`pols_death` and a surrender by
:func:`pols_lapse`.

.. rubric:: Codes

What :mod:`~.VUL_US_S` spells as text, a timing or a kind, is here an int Reference named
as the text it replaces, so that every cell takes and returns C numbers. A call site
reads as it did, less the quotes: ``pols_if_at(t, BEF_DECR)``, ``sa_pp_at(t, i,
BEF_FEE)``, ``claim_pp(t, DEATH)``.

=============  =====  ===============================================================
Reference      Value  Meaning
=============  =====  ===============================================================
BEF_NB         0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR       1      :func:`pols_if_at`: that count plus month t's new business
BEF_MAT        2      :func:`pols_if_at`: before any maturity, the BEF_DECR count
BEF_PREM       3      the accounts, the debt and the pricing path: the value carried in
BEF_WD         4      the accounts and :func:`av_at`: after the net premium
BEF_FEE        5      the accounts and the pricing path: after the withdrawal and its fee
BEF_INV        6      the accounts and the pricing path: after the monthly deduction
BEF_ME         7      the accounts and :func:`av_at`: after the gross return and the fund
                      expense, before the M&E charge
EOM            8      :func:`av_at`: after growth, before decrements
DEATH          0      :func:`claim_pp`, :func:`claims_from_av`: the death claim
LAPSE          1      :func:`claim_pp`, :func:`claims_from_av`: the surrender claim
MATURITY       2      :func:`claims_from_av`: none, the contract never matures
WITHDRAWAL     3      :func:`claim_pp`: the withdrawal, which is no claim
=============  =====  ===============================================================

The accounts are :func:`sa_pp_at`, :func:`fa_pp_at`, :func:`la_pp_at`,
:func:`loan_bal_pp_at`, :func:`av_pp_at`, :func:`unloaned_av_pp_at` and :func:`av_at`;
:func:`fa_pp_at` reads ``BEF_ME`` as ``BEF_INV``, since the fixed option bears no M&E
charge, and :func:`la_pp_at` and :func:`loan_bal_pp_at`, which move only at the end of
the month, read every one of the accounts' timings as ``BEF_PREM``. The pricing path,
:func:`sa_pricing_pp_at`, :func:`fa_pricing_pp_at` and :func:`av_pricing_pp_at`, takes
``BEF_PREM``, ``BEF_FEE`` and ``BEF_INV`` alone, as it has no withdrawal and no M&E
step of its own.

The model has two families of timing, the count's and the account value's, passed to
different cells, and they are numbered as one: ``BEF_NB`` 0 and ``BEF_DECR`` 1, as in
every SEC model, then the count's third, ``BEF_MAT``, then the account value's in the
order of their instants within the month, ``EOM`` last, as ``UL_US_SEC`` numbers them
with ``BEF_ME``, the one instant variable UL adds, in its place. So no two timings share
a code, and a code of one family passed to the other's cell, ``av_pp_at(t, BEF_NB)``, is
refused as any timing the cell does not take is, ``ValueError("invalid timing")``, in
both engines, rather than read as a timing of the cell's own. Kinds are numbered in the
order the month settles them, ``UL_US_SEC``'s three, and ``WITHDRAWAL``, which only
:func:`claim_pp` takes, after them. A cell compares its code with ``==`` alone, never by
order or by membership of a tuple, so that a text passed where a code is taken meets the
cell's own refusal in modelx too. A code a cell takes indexes that cell's cache, a C array
of nine codes a month for each cell that takes one, since every 2-D cache of the model has
one width, nine, and every 3-D cache one inner shape, nine by nine (``spec_sec.py``), so
codes are numbered densely from 0. They are References, not cells, so the symbol map does
not list them. Every other Reference is named in lower case, ``issue_age_min``,
``issue_age_max``, ``subaccount_max`` and ``omega_age`` among them, the contract's bounds,
which :func:`proj_len` refuses a point past, and three of which the compiled model's
caches are sized from.

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`sex`, :func:`rate_class`,
:func:`db_option`, :func:`qual_test`, :func:`premium_type`, :func:`surr_charge_id` and
:func:`scenario_id`, the reports :func:`result_cf`, :func:`result_pols`,
:func:`result_av` and :func:`result_net`, and the checks :func:`check_av_roll_fwd`,
:func:`check_margin` and :func:`check_net_view` are written for a reader and for the
comparison with :mod:`~.VUL_US_S`, which has every one of them: a table row, text,
DataFrames and three verdicts. No other cell calls them: each reads the number ``Data``
decoded from the same column instead, the decodes' flags, the schedules, the scenarios and
the joins the keys select. So the row, the text and the frames stay Python when the model
compiles. A label accessor returns its column as read, text or not: a blank
``surr_charge_id`` on a point without a charge reads as NaN, and a column of numbers as
ints, and the compiled accessor returns the same. Every other cell returns a C ``bint``,
``long long`` or ``double``, and so do the three checks, which may stay Python but compile
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
    """The selected model point, its row of *model_point_table_sec.csv*, as a Series.

    Row ``idx`` of the table, for a reader who wants every column at once: a reporting
    cell (the Space docstring's *Reporting cells*), which no projection cell reads.  Each
    reads its own ``Data`` vector instead.
    """
    return data.model_point_table().iloc[idx]                        # noqa: F821


def point_id():
    """The label of the selected model point, its ``point_id``, from ``Data.point_id``.

    ``Projection`` is indexed by position, ``idx``, as ``basiclife.BasicTerm_SC`` is; the
    label is what a reader finds in the table, so every refusal names it.
    """
    return int(data.point_id()[idx])                                 # noqa: F821


def age_at_entry():
    """The issue age (ANB) of the selected model point, from ``Data.age_at_entry``.

    The age at issue, whatever the policy's duration at the valuation date; the attained
    age in month t is :func:`age`.  ``Data`` holds it to a whole number, 0 or more, and
    :func:`proj_len` to the ages the contract issues.
    """
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point.

    A reporting cell (the Space docstring): ``Data`` joins the COI scale by it, through
    :func:`coi_schedule`, and no projection cell reads it here.
    """
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point (one of six).

    A reporting cell (the Space docstring): ``Data`` joins the class factor and the COI
    scale by it, :func:`class_factor` and :func:`coi_schedule`, and no projection cell
    reads it here.
    """
    return model_point()["rate_class"]


def sum_assured():
    """F_0: the initial face amount of the selected model point, the face at issue.

    Both the $0.20 per $1,000 monthly charge and the surrender charge are quoted on
    this, the *initial* face, not on :func:`sum_assured_at`, and it is the face a point
    not yet in force is issued with.  The face in force at the valuation date is
    :func:`sum_assured_init`, and the face in force in month t is :func:`sum_assured_at`.
    From ``Data.sum_assured``.
    """
    return float(data.sum_assured()[idx])                            # noqa: F821


def db_option():
    """The death benefit option: ``"A"`` (level) or ``"B"`` (face plus account value).

    Option C (return of premium) is observed at one insurer only and is out of scope
    in the product spec.  A reporting cell (the Space docstring): ``Data`` decodes the
    column into :func:`is_db_option_a` and :func:`is_db_option_b`, and no projection
    cell reads it here.
    """
    return model_point()["db_option"]


def is_db_option_a():
    """Whether the death benefit is Option A, the level face, from ``Data.is_db_option_a``.

    ``Data`` decodes the ``db_option`` column, 1 where it is ``"A"``, so that no monthly
    cell branches on text; :func:`db_pp`, :func:`db_pp_eom`, :func:`db_pricing_pp` and
    :func:`face_reduction_pp` read this instead.
    """
    return bool(data.is_db_option_a()[idx])                          # noqa: F821


def is_db_option_b():
    """Whether the death benefit is Option B, the face plus the account value.

    From ``Data.is_db_option_b``, 1 where ``db_option`` is ``"B"``, read by :func:`db_pp`,
    :func:`db_pp_eom` and :func:`db_pricing_pp`, each of which raises on a point that is
    neither A nor B, as ``VUL_US_S``'s do.
    """
    return bool(data.is_db_option_b()[idx])                          # noqa: F821


def qual_test():
    """The IRC 7702 qualification test elected at issue; only ``"GPT"`` is modeled.

    CVAT is a documented variation, out of scope in the baseline, so
    :func:`corridor_factor` raises on anything else rather than silently applying GPT
    corridor factors.  A reporting cell (the Space docstring): ``Data`` decodes the
    column into :func:`is_gpt`, and no projection cell reads it here.
    """
    return model_point()["qual_test"]


def is_gpt():
    """Whether the point elected the Guideline Premium Test, from ``Data.is_gpt``.

    1 where ``qual_test`` is ``"GPT"``, read by :func:`corridor_factor`, which raises on
    any other test, as ``VUL_US_S``'s does: CVAT is a documented variation, out of scope
    in the baseline.
    """
    return bool(data.is_gpt()[idx])                                  # noqa: F821


def premium_type():
    """The premium pattern: ``"LEVEL"`` or ``"SINGLE"`` **[std]**.

    The notes do not enforce guideline premium or 7-pay limits in the baseline --
    premiums are assumed within limits -- so there is no cap on either pattern and no
    ``TARGET`` pattern.  A reporting cell (the Space docstring): ``Data`` decodes the
    column into :func:`is_level_premium` and :func:`is_single_premium`, and no
    projection cell reads it here.
    """
    return model_point()["premium_type"]


def is_level_premium():
    """Whether the premium pattern is LEVEL, from ``Data.is_level_premium``.

    One of the two decodes of the ``premium_type`` column that :func:`premium_pp` and
    :func:`prem_pricing_pp` branch on, so that no monthly cell compares text; each raises
    on a point that is neither, as ``VUL_US_S``'s does.
    """
    return bool(data.is_level_premium()[idx])                        # noqa: F821


def is_single_premium():
    """Whether the premium pattern is SINGLE, from ``Data.is_single_premium``.

    A decode of the ``premium_type`` column, read by :func:`premium_pp` and
    :func:`prem_pricing_pp`.
    """
    return bool(data.is_single_premium()[idx])                       # noqa: F821


def premium_pp_ann():
    """The planned annualized premium per policy; flexible in amount and timing [S1].

    From ``Data.premium_pp_ann``.
    """
    return float(data.premium_pp_ann()[idx])                         # noqa: F821


def load_prem_rate():
    """gamma: the current premium load rate, 4.0% flat **[std]** (guaranteed max 6.0% [S2]).

    The load is a non-guaranteed element under ASOP 2 [R11], which is why it sits in
    the model point table rather than in a Reference.  From ``Data.load_prem_rate``, which
    refuses a load outside 0 to 1.
    """
    return float(data.load_prem_rate()[idx])                         # noqa: F821


def subaccount_count():
    """The number of subaccounts in the separate-account lineup, *subaccount_table.csv*.

    Two subaccounts -- equity and bond -- a **[std]** collapse of the observed menus.
    Each is named by its position in the table, ``i``, from 0, the argument every cell of
    a subaccount takes, so the lineup is ``range(subaccount_count())``: ``VUL_US_S``'s
    ``subaccount_ids``, a list of the ids, which no compiled cell returns.  Extending the
    lineup means adding a row there *and* the matching ``sa_pp_init_<id>`` and
    ``alloc_<id>`` columns to the model point table, which ``Data`` checks;
    :func:`proj_len` refuses a lineup of more than ``subaccount_max`` subaccounts, the most
    the compiled model's caches hold.  From ``Data.subaccount_count``, which checks the
    lineup.
    """
    return int(data.subaccount_count())                              # noqa: F821


def alloc(i):
    """alpha_i: the share of each net premium allocated to subaccount i.

    The point's ``alloc_<id>`` column for the subaccount at position ``i`` of the lineup,
    from ``Data.alloc``.  A position outside the lineup is refused, naming the point, as
    each cell that reads a subaccount's input refuses it, so that no read falls past the
    lineup.
    """
    if not 0 <= i < subaccount_count():
        raise ValueError(f"point_id {point_id()}: no subaccount at position {i} of the "
                         f"lineup of {subaccount_count()}")
    return float(data.alloc()[idx, i])                               # noqa: F821


def alloc_fixed():
    """alpha_F: the share of each net premium allocated to the fixed option.

    From ``Data.alloc_fixed``.
    """
    return float(data.alloc_fixed()[idx])                            # noqa: F821


def fund_expense_ann(i):
    """e_i: the annual fund operating expense ratio of subaccount i **[std]**.

    0.75% equity and 0.55% bond, chosen inside the observed lineup ranges
    (0.29%-1.18% [S1], 0.55%-2.88% gross [S2], 0.46%-2.54% [S3], 0.08%-1.93% [S4]).
    Borne through the unit value, so it reduces the policyholder's return and is *not*
    insurer income.  From ``Data.fund_expense_ann`` at the subaccount's position, once
    ``Data`` has checked the lineup, which refuses a ratio that is blank, text, infinite
    or below 0.  A position outside the lineup is refused, as :func:`alloc` refuses it.
    """
    if not 0 <= i < subaccount_count():
        raise ValueError(f"point_id {point_id()}: no subaccount at position {i} of the "
                         f"lineup of {subaccount_count()}")
    return float(data.fund_expense_ann()[i])                         # noqa: F821


def sa_pp_init(i):
    """SA_i(0): the value of subaccount i per policy entering month 0.

    The ``sa_pp_init_<id>`` column, ``VUL_US_S``'s own, for the subaccount at position
    ``i`` of the lineup, from ``Data.sa_pp_init``: the balance at the close of policy
    month ``duration_mth_init() - 1``, before any month-0 event, which is what
    ``VUL_US_S`` carries into the month as ``sa_pp_at(d, i, BEF_PREM)`` at
    ``d = duration_mth_init()``.  It is the opening balance of :func:`sa_pp_at` at
    :func:`t_entry`, read off the policy's own subaccount, never the premium allocation
    times the account value: a subaccount's share drifts from its allocation as the
    returns differ.  Zero for a point not yet in force.  A position outside the lineup
    is refused, as :func:`alloc` refuses it.
    """
    if not 0 <= i < subaccount_count():
        raise ValueError(f"point_id {point_id()}: no subaccount at position {i} of the "
                         f"lineup of {subaccount_count()}")
    return float(data.sa_pp_init()[idx, i])                          # noqa: F821


def fa_pp_init():
    """FA(0): the fixed-option value per policy entering month 0.

    The ``fa_pp_init`` column, ``VUL_US_S``'s own, the fixed option's balance at the close
    of policy month ``duration_mth_init() - 1``; the opening balance of :func:`fa_pp_at`
    at :func:`t_entry`.  Zero for a point not yet in force.  From ``Data.fa_pp_init``.
    """
    return float(data.fa_pp_init()[idx])                             # noqa: F821


def loan_bal_init():
    """D(0): the outstanding policy debt per policy entering month 0.

    The ``loan_bal_init`` column, ``VUL_US_S``'s own: the debt at the close of policy
    month ``duration_mth_init() - 1``, interest accrued to then included, before any
    month-0 event; the opening balance of :func:`loan_bal_pp_at` at :func:`t_entry`.
    Zero for a point not yet in force.  ``VUL_US_S`` also opens its loan account from it,
    taking the collateral equal to the debt at the outset **[std]**; here the loan account
    opens from a column of its own, :func:`la_pp_init`, since the two part once interest
    accrues.  From ``Data.loan_bal_init``.
    """
    return float(data.loan_bal_init()[idx])                          # noqa: F821


def la_pp_init():
    """LA(0): the loan-account collateral per policy entering month 0.

    The ``la_pp_init`` column: the loan account at the close of policy month
    ``duration_mth_init() - 1``, before any month-0 event, which is what ``VUL_US_S``
    carries into the month as ``la_pp_at(d, BEF_PREM)``.  It is the opening balance of
    :func:`la_pp_at` at :func:`t_entry`, and part of the account value, as the debt is
    not.  A loan moves value out of the investment options into the loan account [S3], so
    the two coincide on the loan's first day, and ``VUL_US_S`` takes them equal at the
    start of its frame **[std]**; after that the collateral grows at the rate credited,
    :func:`loan_cr_rate_mth`, and the debt at the rate charged, :func:`loan_rate_mth`, so
    they part: ``VUL_US_S``'s point 4, six months on, holds 8,039.90 of collateral against
    a debt of 8,041.89.  ``Data`` refuses a loan account without a loan, or a loan without
    one.  Zero for a point not yet in force.  From ``Data.la_pp_init``.
    """
    return float(data.la_pp_init()[idx])                             # noqa: F821


def sum_assured_init():
    """F(0): the face amount in force per policy entering month 0.

    The ``sum_assured_init`` column: the face in force at the close of policy month
    ``duration_mth_init() - 1``, after every Option A withdrawal cut to date, which is the
    face ``VUL_US_S`` carries into the month as ``sum_assured_at(d - 1)``.  It is the base
    of :func:`sum_assured_at` at :func:`t_entry`, so month 0's own withdrawal cut, death
    benefit and net amount at risk are measured from it.  The face at issue,
    :func:`sum_assured`, stays the base of :func:`units` and so of the $0.20 charge and
    the surrender charge, and ``Data`` refuses a value above it, since face increases are
    not modelled, or of 0 in force.  Zero for a point not yet in force, which is issued at
    :func:`sum_assured`.  ``VUL_US_S`` opens its in-force points at the face at issue.
    From ``Data.sum_assured_init``.
    """
    return float(data.sum_assured_init()[idx])                       # noqa: F821


def wd_pp_mth():
    """The planned partial withdrawal per policy, in each month withdrawals are allowed.

    The model point's ``wd_pp`` column, a monthly amount, **0 in every shipped model
    point**: the notes make withdrawals explicitly none in the baseline, so the behaviour
    is left to the data **[std]**.  Read once a point here, from ``Data.wd_pp``, so that
    :func:`wd_pp`, a monthly cell on the account value's chain, reads no table in its own
    formula.
    """
    return float(data.wd_pp()[idx])                                  # noqa: F821


def av_pp_init():
    """AV(0): the total account value per policy entering month 0.

    ``sum(SA_i(0)) + FA(0) + LA(0)`` -- the loan account is part of the account value
    [S1][S2][S3][S4], the debt is not.  The loan account is :func:`la_pp_init`, the
    collateral entering month 0, where ``VUL_US_S`` takes the debt, ``loan_bal_init()``, in
    its place.  It is the opening balance of ``av_pp_at(t, BEF_PREM)`` at
    :func:`t_entry`.  The subaccounts are summed in a loop over the lineup's positions,
    from 0.0, which for the shipped lineup of two is ``VUL_US_S``'s ``sum()`` float for
    float; with three or more, Python's ``sum()``, compensated since 3.12, can differ from
    it in the last bit.
    """
    av = 0.0
    for i in range(subaccount_count()):
        av = av + sa_pp_init(i)
    return av + fa_pp_init() + la_pp_init()


def policy_count():
    """The number of policies the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the policies in force then, before any
    month-0 event; any other point counts the policies it issues.  Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second.  Every per-policy value -- the
    accounts, the debt, the face, the opening state -- is the same whatever the count, and
    every cash flow is a per-policy amount weighted by it.  From ``Data.policy_count``.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """Policies in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose policies
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``.  So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count.  ``VUL_US_S``'s cell of the name is the notes'
    ``l_0``, the count at the start of its frame, which on new business is the issued
    count.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 24 for points 1 and 2 and 120 for point 4,
    ``VUL_US_S``'s in-force cells, 126 for point 6, point 4 six months on, 0 for a policy
    issued at the valuation date, and -25 for point 9, to be issued 25 months after it,
    which ``Data`` admits up to ``future_horizon_mth`` months ahead.  This is the notes'
    ``duration_inforce``, an elapsed count and therefore already 0-based, and
    ``VUL_US_S``'s cell and column of the same name, which count from the first month of
    its own projection; here that month is the valuation date for every point, and the
    count may be negative.  It is the one fact the policy clock takes from the model
    point, from ``Data.duration_mth``.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point.

    False models the low-load / no-load archetype [S3], a documented variation.  From
    ``Data.has_surr_charge``, 1 where the column reads True.
    """
    return bool(data.has_surr_charge()[idx])                         # noqa: F821


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*.

    A reporting cell (the Space docstring): ``Data`` joins the schedule by it, into
    :func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`, and no projection
    cell reads it here.  A point without a charge is never refused for it, so it may be
    blank, read as NaN, or a number, as the column reads, and is returned as read.
    """
    return model_point()["surr_charge_id"]


def surr_charge_rate_max():
    """The schedule's charge per $1,000 of initial face, before any of it runs off.

    The ``sc_per_1000_init`` column of this point's row of *surr_charge_table.csv*,
    $18.00 on the shipped ``VUL14`` schedule; :func:`surr_charge_rate` steps it down by
    policy year from here.  ``Data.surr_charge_rate_max`` joins it to the points by
    ``surr_charge_id``, once the table and the join are checked, so that no projection
    cell reads the table: a blank charge would come out of :func:`surr_charge_rate`'s
    ``max`` as no charge at all, and ``Data`` refuses one.  :func:`surr_charge_rate`
    reads it only where :func:`has_surr_charge` is true, but a point without a charge
    reads its schedule too, as at stage ``E``, where the table holds its id; where it
    does not, ``Data.has_surr_charge_schedule`` is 0, and this raises ``KeyError``, naming
    the point, where stage ``E``'s ``.loc`` raised it.
    """
    rate = float(data.surr_charge_rate_max()[idx])                   # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise KeyError(f"point_id {point_id()}: surr_charge_table.csv has no schedule "
                       f"for its surr_charge_id")
    return rate


def surr_charge_runoff_years():
    """The number of policy years over which the schedule's charge runs off.

    The ``runoff_years`` column of this point's row of *surr_charge_table.csv*, 14 on the
    shipped ``VUL14`` schedule, read as a float, as ``UL_US_SEC`` reads its own; ``Data``
    holds it to a whole number of years, 1 or more, and below ``2**53`` in size on a
    point with a charge.  :func:`surr_charge_rate` divides :func:`surr_charge_rate_max`
    by it, and :func:`lapse_shock_month` counts policy years on its ``int()``, as
    ``VUL_US_S`` does: the compiled ``int()`` converts it through a Python int to a C
    ``long long``, exact below ``2**63``.  Joined by ``Data.surr_charge_runoff_years`` as
    :func:`surr_charge_rate_max` is.  Read by those two only where :func:`has_surr_charge`
    is true; on a point without a charge it reads the schedule where the table holds its
    id, as at stage ``E``, and raises ``KeyError``, naming the point, where it does not,
    as :func:`surr_charge_rate_max` does.
    """
    years = float(data.surr_charge_runoff_years()[idx])              # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise KeyError(f"point_id {point_id()}: surr_charge_table.csv has no schedule "
                       f"for its surr_charge_id")
    return years


def scenario_id():
    """The return scenario ID, a row label of *scenario_table.csv*.

    The separate-account return path is the dominant assumption for this product, so
    it is a model point attribute rather than a Reference: different cells can be run
    on different paths in one model.  A reporting cell (the Space docstring): ``Data``
    numbers the scenarios and gives each point its own, :func:`scenario_index`, and no
    projection cell reads it here.  A numeric scenario id, written so in both files,
    joins as text does, and is returned as read.
    """
    return model_point()["scenario_id"]


def scenario_index():
    """The number of this point's return scenario, its row of ``Data.gross_return_array``.

    ``Data.scenario_index`` at this point: ``Data`` numbers the scenarios of
    *scenario_table.csv* from 1 in the order of their ``scenario_id``, and gives each
    point the number of its own, refusing, as the table is first read, a point whose
    scenario the table lacks or holds no row for a subaccount of the lineup.
    ``VUL_US_S`` joins the table on the point's ``scenario_id`` text in every month,
    which this replaces, since no compiled cell reads text.
    """
    return int(data.scenario_index()[idx])                           # noqa: F821


def corridor_override_m1():
    """The model point's first-month corridor factor pin, a number, or NaN where blank.

    The ``corridor_override_m1`` column, from ``Data.corridor_override_m1``, read once a
    point, so that :func:`corridor_factor`, a monthly cell, reads no model point column
    in its own formula.  Read only where :func:`has_corridor_override_m1` is true;
    ``Data`` holds the column to blank or a number, zero or more, and to blank on a point
    issued after the valuation date.  Blank, it is NaN, as at stage ``E``: the flag, not
    this value, decides, so no NaN reaches a formula.
    """
    return float(data.corridor_override_m1()[idx])                   # noqa: F821


def has_corridor_override_m1():
    """Whether the model point pins its corridor factor in the valuation month.

    True where the ``corridor_override_m1`` column holds a number, False where it is
    blank: ``Data.has_corridor_override_m1``, the column decoded once for every point,
    so that :func:`corridor_factor` tests a flag rather than a missing value.  Model
    point 1 pins it, at the worked example's 2.15; every other shipped point leaves it
    blank.
    """
    return bool(data.has_corridor_override_m1()[idx])                # noqa: F821


def coi_rate_override_m1():
    """The model point's first-month current COI rate pin, a number, or NaN where blank.

    The ``coi_rate_override_m1`` column, from ``Data.coi_rate_override_m1``, read once a
    point, so that :func:`coi_rate`, a monthly cell, reads no model point column in its
    own formula.  Read only where :func:`has_coi_rate_override_m1` is true; ``Data``
    holds the column as it holds :func:`corridor_override_m1`'s, NaN where blank.
    """
    return float(data.coi_rate_override_m1()[idx])                   # noqa: F821


def has_coi_rate_override_m1():
    """Whether the model point pins its current COI rate in the valuation month.

    True where the ``coi_rate_override_m1`` column holds a number, False where it is
    blank, from ``Data.has_coi_rate_override_m1``, as :func:`has_corridor_override_m1` is
    read.  Model point 1 pins it, at the $0.04 disclosed for its cell [S4]; every other
    shipped point leaves it blank.
    """
    return bool(data.has_coi_rate_override_m1()[idx])                # noqa: F821


def duration_mth(t):
    """Completed policy months at the beginning of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together.  A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame.  It is 0 in the issue month, ``t = 0`` for
    a point issued at the valuation date, and negative before issue.  It is the policy
    month **from issue**, 0-based, of month ``t``.  The pricing-path cells index policy
    months from issue on the same clock, so ``m = duration_mth(t)``; see
    :func:`funding_ratio`.
    """
    return duration_mth_init() + t


def duration(t):
    """Completed policy years at the beginning of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year, as ``duration`` is in lifelib, and negative before
    issue.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """The policy year containing month t: ``duration(t) + 1``.

    A contractual, 1-based label -- policy year 1 is the twelve months from issue --
    used only to look up schedules the contract states by policy year: the surrender
    charge, the loan tier, the COI scale, the lapse and persistency tables.  It is
    never the frame index.  It is 0 or less before issue, where no table is read by it:
    each reader is called inside cover only (:func:`is_active`).
    """
    return duration(t) + 1


def age(t):
    """x_t: the attained age (ANB) in month t, ``age_at_entry() + duration(t)``.

    Age advances on the policy anniversary, not on the birthday, which is the ANB
    convention the whole model is built on **[std]**.  Before issue it is below the issue
    age, where no table is read at it.
    """
    return age_at_entry() + duration(t)


def omega_mth():
    """The policy month at which the projection ends, the first at attained age 122.

    ``12 * (omega_age - age_at_entry() + 1)``: 924 at issue age 45.  The mortality table
    ends at ``omega_age`` (121), where the annual rate is 1.0, so the last month of the
    frame, ``omega_mth() - 1``, is the last at attained age 121.  It is ``VUL_US_S``'s
    frame from issue, counted on the policy clock; :func:`proj_len` counts from the
    valuation date instead.  The contract has no maturity date [S1][S2][S4], so the cell
    is named for ``omega_age``, the end of the table, and not for an event of the policy:
    where lives survive the last month, the count and the account value they carry into
    this month are kept (see :func:`pols_if_at`).
    """
    return 12 * (omega_age - age_at_entry() + 1)                     # noqa: F821


def proj_len():
    """The number of months from the valuation date to the end of the projection.

    ``omega_mth() - duration_mth_init()``: 924 for a policy issued at age 45 at the
    valuation date, 900 for points 1 and 2, in force 24 months, 804 for point 4, in force
    120 months, and 949 for point 9, issued 25 months after the valuation date.  The frame
    is ``t = 0, 1, ..., proj_len() - 1``; ``proj_len()`` is its exclusive end, the row
    count of :func:`result_cf`, and ``proj_len() - 1`` is the frame's last month, the
    last at attained age 121.  The contract has no maturity date [S1][S2][S4], so the
    projection is truncated by mortality **[std]**, not by the policy.  Ending at 121
    rather than 120 is deliberate: it is the age at which premiums and monthly deductions
    cease while the asset charges continue, and the notes list missing that regime switch
    among the modeling pitfalls.

    Four kinds of point have no frame the contract issues, and each raises here, naming
    the point, rather than projecting what the contract does not hold, in this order:

    * one issued above ``omega_age``, 121, which would never be in cover: ``VUL_US_S``
      projects it as months in which nothing happens.  Checked first, so that a point to
      be issued there is refused as never in cover, whenever it is to be issued and
      whatever ``issue_age_max`` is set to, as ``UL_US_SEC`` refuses it;
    * one at or past the end of the projection at the valuation date, which an in-force
      extract should not carry;
    * one issued below ``issue_age_min``, 0, or above ``issue_age_max``, 85, the issue ages
      ``product-spec.md`` admits.  ``VUL_US_S`` projects any age its tables serve, but the
      compiled model's caches are sized from the youngest (``spec_sec.py``), so a younger
      point, whose frame and policy years run longer, would read past them; the oldest
      sizes nothing, and is the contract's;
    * one whose lineup holds more than ``subaccount_max``, 9, subaccounts, the most the
      compiled model's caches hold for a subaccount's position.
    """
    if omega_mth() <= 0:
        raise ValueError(
            f"point_id {point_id()}: age_at_entry {age_at_entry()} is above omega_age, "
            f"{omega_age}: a policy issued there would never be in cover")  # noqa: F821
    n = omega_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past the end of the projection, policy month {omega_mth()}, "
            f"attained age {omega_age + 1}")                              # noqa: F821
    if age_at_entry() < issue_age_min:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is below "
                         f"issue_age_min, {issue_age_min}")           # noqa: F821
    if age_at_entry() > issue_age_max:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is above "
                         f"issue_age_max, {issue_age_max}")           # noqa: F821
    if subaccount_count() > subaccount_max:                          # noqa: F821
        raise ValueError(f"point_id {point_id()}: the subaccount lineup holds "
                         f"{subaccount_count()} subaccounts, above subaccount_max, "
                         f"{subaccount_max}")                         # noqa: F821
    return n


def t_entry():
    """The first month the policy is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later.  It is the base of every recursion: the count, each subaccount,
    the fixed option, the loan account, the debt and the face all open there, from the
    model point's opening state on a point in force and from the issue values on any
    other.  No cell in cover reads a month before it.  The pricing path is not a
    recursion of the projection's: it runs from issue, keyed by the policy month, and
    reads no state (see :func:`funding_ratio`).
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and inside the projection.

    ``0 <= duration_mth(t) < omega_mth()``, false before issue and from
    ``t = proj_len()`` on.  Outside cover every count, charge, premium, withdrawal,
    decrement rate, decrement, claim and flow is zero and every flag false, no table is
    read at a policy year or an attained age the policy does not have, the pricing path is
    not asked for a policy month before issue, and nothing reads a month past
    ``proj_len()``; the clocks, the inputs read on the valuation clock and the loan
    account's credited rate keep their values, and the two lapse multipliers and the
    funding ratio their neutral 1.0.  The two exceptions are the opening values of the
    month after the frame, the count and the account value carried into
    ``t = proj_len()``, which the roll-forwards read (see :func:`pols_if_at` and
    :func:`av_pp_at`).
    """
    return 0 <= duration_mth(t) < omega_mth()


def units():
    """U: the **initial** face amount in $1,000 units, ``sum_assured() / 1000``.

    Takes no ``t``.  The $0.20 monthly charge is quoted per $1,000 of ``F_0`` [S2] and
    the surrender charge per $1,000 of initial face **[std]**, so neither follows
    :func:`sum_assured_at`.  The fixed-UL chassis charges its per-unit fee on the
    *current* face and therefore writes ``units(t)``; copying that here would silently
    shrink both charges after an Option A withdrawal.
    """
    return sum_assured() / 1000


def scenario_last_mth(i):
    """The last month of this point's return scenario for subaccount i: its extent.

    ``Data.scenario_last_mths`` at this point's :func:`scenario_index` and the
    subaccount's position ``i``, which ``Data`` reads from the table's key columns once it
    has checked the keys and the returns, and which it has refused, at its first read, a
    point whose scenario lacks a subaccount of the lineup for.  1 for the shipped ``WE``
    scenario, whose month 1 starts the level path, and 0 for ``LEVEL6``.  A position
    outside the lineup is refused, as :func:`alloc` refuses it.
    """
    if not 0 <= i < subaccount_count():
        raise ValueError(f"point_id {point_id()}: no subaccount at position {i} of the "
                         f"lineup of {subaccount_count()}")
    return int(data.scenario_last_mths()[scenario_index(), i])       # noqa: F821


def gross_return_mth(t, i):
    """r_{i,t}: the **gross** monthly return of subaccount i, a scenario input.

    Read from *scenario_table.csv* for this model point's scenario, whose ``t`` column
    counts months from the **valuation date**, 0-based, exactly as here: a scenario is a
    path of the economy from that date, the same month for every point, however old the
    policy, and a point in force reads the path from its own month 0 on.  It is
    ``Data.gross_return_array`` at the point's :func:`scenario_index`, the subaccount's
    position ``i`` and the month.  Months beyond the end of a scenario take its last row,
    :func:`scenario_last_mth`, which is asked for first, so that a projection meets the
    check of the table's keys and returns; a two-row scenario is a level path with one
    distinguished opening month -- which is exactly the shipped ``WE`` scenario, whose
    ``t = 0`` is the worked example's month (+1.00% equity, -0.50% bond).  A scenario
    whose months start after month 0, as a path re-based to a policy issued later does,
    holds no return before them, and a read there is refused, naming the point, the
    subaccount and the month, where ``VUL_US_S``'s ``.loc`` raised ``KeyError``, so that
    the padding before the cell's first month is never read.  ``Data`` holds a path to
    ``Data.return_horizon_mth``, 1,585, the last month any frame the contract allows
    reads, and gives a path that runs past it that month as its last.  So a month past the
    horizon, which no frame reads, is refused, naming the point, the scenario by its
    number, :func:`scenario_index`, the subaccount and the month, where ``VUL_US_S`` reads
    the path's own month, or its last; the scenario's id is a label, which no projection
    cell reads, even to refuse (R17), and the point's row of the table names it.  And so
    is any month of a cell whose path starts past the horizon, which ``Data`` holds
    nothing of, its last month falling below its first: no read reaches the padding after
    a cell's last month either.

    Gross means before the fund expense ratio and before the M&E charge; both are
    applied in :func:`inv_return_mth`.  A stochastic set is more rows in this table,
    not a formula change.  An economic input, so it takes no guard: outside cover no
    formula reads it.
    """
    last = scenario_last_mth(i)
    first = data.scenario_first_mths()[scenario_index(), i]          # noqa: F821
    if t < first:
        raise ValueError(f"point_id {point_id()}: scenario_table.csv has no return for "
                         f"subaccount_id {int(data.subaccounts()[i])} at t {t}")  # noqa
    if t > data.return_horizon_mth or last < first:                  # noqa: F821
        raise ValueError(f"point_id {point_id()}: scenario_table.csv is read to "
                         f"return_horizon_mth, {data.return_horizon_mth}, so its "  # noqa
                         f"scenario {scenario_index()}, in the order of the ids, has no "
                         f"return for subaccount_id {int(data.subaccounts()[i])} "  # noqa
                         f"at t {t}")
    return float(data.gross_return_array()[scenario_index(), i, min(t, last)])  # noqa


def inv_return_mth(t, i):
    """The net monthly unit-value return of subaccount i.

    ``(1 + r_{i,t}) (1 - e_i/12) (1 - m/12) - 1``.  In the contract the fund expenses
    and (at one insurer [S1]) the M&E charge accrue daily inside the unit value; the
    monthly product form is a **[std]** approximation, and insurers that deduct M&E
    monthly [S2][S3][S4] are captured by the same factor.

    The M&E charge is applied **here and only here**.  Applying it again as a monthly
    deduction would double count it across insurer conventions -- the notes list that
    among the modeling pitfalls, and this model picks the unit-value factor.
    """
    return ((1 + gross_return_mth(t, i))
            * (1 - fund_expense_ann(i) / 12)
            * (1 - me_rate_ann / 12) - 1)                            # noqa: F821


def crediting_rate_ann(t):
    """i_fix: the declared annual effective rate on the fixed option, 1.0% **[std]**.

    Floored at the contractual guaranteed minimum ``guar_rate_ann`` of 1.0% [S1].
    Declared rates are non-guaranteed and are not published, so the baseline holds the
    declared rate at the floor; in practice it would move with general-account yields.

    An economic input, so it is read on the **valuation** clock: ``t`` counts months from
    the valuation date, and a declared-rate scenario would be indexed by it, one path for
    every point of a block, however old the policy.  The shipped rate is flat, so the
    clock shows in no number.  The pricing path does not read it: it is a projection
    made at issue, and credits :func:`pricing_fixed_return_mth`.
    """
    return max(guar_rate_ann, crediting_rate_curr)                   # noqa: F821


def fixed_return_mth(t):
    """The monthly fixed-option rate, ``(1 + i_fix)^(1/12) - 1``.

    The contract credits daily [S1]; monthly compounding is the model's discretization
    **[std]** -- do not also compound daily.
    """
    return (1 + crediting_rate_ann(t)) ** (1 / 12) - 1


def loan_rate_ann(t):
    """i_L: the annual effective rate charged on policy debt [S1].

    2.0% in policy years 1-9 (the standard loan), 1.05% from policy year 10, which opens
    at the 9th anniversary (the preferred loan), as the technical notes give it.  Against
    the 1.0% credited to the loan account this is a net spread of 1.0% falling to 0.05%.  A
    contractual scale by policy year, so it is zero outside cover, before the policy year
    is compared.
    """
    if not is_active(t):
        return 0.0
    if policy_year(t) < loan_pref_year:                              # noqa: F821
        return loan_rate_ann_std                                     # noqa: F821
    return loan_rate_ann_pref                                        # noqa: F821


def loan_rate_mth(t):
    """The monthly charged loan rate, ``(1 + i_L)^(1/12) - 1``.

    Contractually the interest is due each anniversary and capitalized if unpaid [S1];
    monthly compounding is the model's discretization **[std]**.
    """
    return (1 + loan_rate_ann(t)) ** (1 / 12) - 1


def loan_cr_rate_ann(t):
    """i_C: the annual effective rate credited to the loan account, 1.0% [S1].

    Loaned value earns this, not fund returns -- the notes list ignoring that among
    the modeling pitfalls.
    """
    return loan_cr_rate_ann_lvl                                      # noqa: F821


def loan_cr_rate_mth(t):
    """The monthly loan-account credited rate, ``(1 + i_C)^(1/12) - 1`` **[std]**."""
    return (1 + loan_cr_rate_ann(t)) ** (1 / 12) - 1


def pricing_return_mth():
    """The monthly gross subaccount return on the notes' at-issue pricing path.

    ``(1 + 6%)^(1/12) - 1`` **[std]**: the level gross return the notes specify for
    ``AV*``, the denominator of the funding ratio.  Independent of the projection's own
    return scenario, which is the point -- the funding ratio compares the realized path
    against a fixed pricing path.
    """
    return (1 + pricing_return_ann) ** (1 / 12) - 1                  # noqa: F821


def pricing_fixed_return_mth():
    """The monthly fixed-option rate on the notes' at-issue pricing path.

    ``(1 + max(guar_rate_ann, crediting_rate_curr))^(1/12) - 1``: the declared rate's
    level, the rate :func:`crediting_rate_ann` declares as shipped, made one rate for
    every policy month of the path.  ``VUL_US_S`` credits the path at
    ``fixed_return_mth(m)``, the projection's rate read at a policy month ``m`` as though
    it were a month of the projection; the shipped rate is flat, so the two are the same
    float.  But ``t`` here counts months from the valuation date, so a declared-rate path
    read at ``m`` would credit a point's pricing path with the rate declared ``m`` months
    after the valuation date, a different rate for each point.  The pricing path is a
    projection made at issue, which no later declaration moves, so it takes the level.
    """
    return (1 + max(guar_rate_ann, crediting_rate_curr)) ** (1 / 12) - 1  # noqa: F821


def age_pricing(m):
    """The attained age (ANB) in policy month m of the pricing path.

    ``age_at_entry() + m // 12``.  ``m`` counts policy months from issue, 0-based:
    ``m = 0`` is the issue month.
    """
    return age_at_entry() + m // 12


def policy_year_pricing(m):
    """The policy year containing policy month m of the pricing path, ``m // 12 + 1``."""
    return m // 12 + 1


def prem_pricing_pp(m):
    """The premium paid in policy month m on the pricing path: the *planned* premium.

    The pricing path is funded at ``rho = 1`` by construction -- it is the benchmark
    the realized funding level is measured against -- so premium persistency does not
    enter it.  A single premium falls in the issue month ``m = 0``.  Zero from attained
    age 121.  The pattern is read through its decodes, :func:`is_single_premium` and
    :func:`is_level_premium`, not as text.
    """
    if age_pricing(m) >= charges_cease_age:                          # noqa: F821
        return 0.0
    if is_single_premium():
        return premium_pp_ann() if m == 0 else 0.0
    elif is_level_premium():
        return premium_pp_ann() / 12
    else:
        raise ValueError("invalid premium type")


def sa_pricing_pp_at(m, i, timing):
    """Pricing-path subaccount value at an intra-month point of policy month m.

    ``BEF_PREM`` the closing balance of month ``m - 1``, or zero in the issue month
    ``m = 0`` -- the path starts at issue with no account value, whatever the model
    point's own opening balances are; ``BEF_FEE`` after the net premium;
    ``BEF_INV`` after this subaccount's pro-rata share of the monthly deduction.
    There are no withdrawals and no loans on the pricing path, so the ``BEF_WD``
    point of :func:`sa_pp_at` has no counterpart.

    ``BEF_PREM`` forms the previous month's close itself -- month ``m - 1``'s opening
    balance, net premium, share of the deduction and growth, the products
    :func:`sa_pricing_pp` takes, in the order it takes them -- rather than calling for
    it, so the chain of calls back to issue is one cell a month, where ``VUL_US_S``'s ran
    through four.  The path is deterministic and reads no state, so it stays based at
    issue, ``m = 0``, on a point in force too: a cold call at policy month ``m`` runs
    ``m`` cells deep.  It is read only inside cover (see :func:`funding_ratio`).
    """
    if timing == BEF_PREM:
        if m == 0:
            return 0.0
        bef = (sa_pricing_pp_at(m - 1, i, BEF_PREM)
               + alloc(i) * (1 - load_prem_rate()) * prem_pricing_pp(m - 1))
        den = av_pricing_pp_at(m - 1, BEF_FEE)
        share = bef / den if den > 0 else alloc(i)
        bef = bef - mth_deduction_pricing_pp(m - 1) * share
        return (bef * (1 + pricing_return_mth())
                * (1 - fund_expense_ann(i) / 12)
                * (1 - me_rate_ann / 12))                            # noqa: F821
    elif timing == BEF_FEE:
        return (sa_pricing_pp_at(m, i, BEF_PREM)
                + alloc(i) * (1 - load_prem_rate()) * prem_pricing_pp(m))
    elif timing == BEF_INV:
        den = av_pricing_pp_at(m, BEF_FEE)
        bef = sa_pricing_pp_at(m, i, BEF_FEE)
        share = bef / den if den > 0 else alloc(i)
        return bef - mth_deduction_pricing_pp(m) * share
    else:
        raise ValueError("invalid timing")


def sa_pricing_pp(m, i):
    """SA*_i: the pricing-path value of subaccount i at the end of policy month m.

    The post-deduction balance times the unit-value factor; the opening balance, zero
    at ``m = 0``, is ``sa_pricing_pp_at(m, i, BEF_PREM)``.  Growth uses the level
    pricing return rather than the projection's scenario, with the same fund expense
    and M&E factors.
    """
    return (sa_pricing_pp_at(m, i, BEF_INV)
            * (1 + pricing_return_mth())
            * (1 - fund_expense_ann(i) / 12)
            * (1 - me_rate_ann / 12))                                # noqa: F821


def fa_pricing_pp_at(m, timing):
    """Pricing-path fixed-option value at an intra-month point of policy month m.

    ``BEF_PREM`` is the closing balance of month ``m - 1``, zero at ``m = 0``, formed
    here from month ``m - 1``'s values as :func:`fa_pricing_pp` forms it, rather than
    called for, so that the chain back to issue is one cell a month, as
    :func:`sa_pricing_pp_at`'s is.
    """
    if timing == BEF_PREM:
        if m == 0:
            return 0.0
        bef = (fa_pricing_pp_at(m - 1, BEF_PREM)
               + alloc_fixed() * (1 - load_prem_rate()) * prem_pricing_pp(m - 1))
        den = av_pricing_pp_at(m - 1, BEF_FEE)
        share = bef / den if den > 0 else alloc_fixed()
        bef = bef - mth_deduction_pricing_pp(m - 1) * share
        return bef * (1 + pricing_fixed_return_mth())
    elif timing == BEF_FEE:
        return (fa_pricing_pp_at(m, BEF_PREM)
                + alloc_fixed() * (1 - load_prem_rate()) * prem_pricing_pp(m))
    elif timing == BEF_INV:
        den = av_pricing_pp_at(m, BEF_FEE)
        bef = fa_pricing_pp_at(m, BEF_FEE)
        share = bef / den if den > 0 else alloc_fixed()
        return bef - mth_deduction_pricing_pp(m) * share
    else:
        raise ValueError("invalid timing")


def fa_pricing_pp(m):
    """FA*: the pricing-path fixed-option value at the end of policy month m.

    The post-deduction balance credited one month at :func:`pricing_fixed_return_mth`,
    the pricing path's own rate, which no declaration after issue moves.
    """
    return fa_pricing_pp_at(m, BEF_INV) * (1 + pricing_fixed_return_mth())


def av_pricing_pp_at(m, timing):
    """Pricing-path total account value at an intra-month point of policy month m.

    The subaccounts' values at the ``timing``, summed in a loop over the lineup's
    positions from 0.0, then the fixed option's: ``VUL_US_S``'s ``sum()`` of a generator,
    float for float on the shipped lineup of two, which no compiled cell can run.
    """
    av = 0.0
    for i in range(subaccount_count()):
        av = av + sa_pricing_pp_at(m, i, timing)
    return av + fa_pricing_pp_at(m, timing)


def av_pricing_pp(m):
    """AV*: the pricing path's account value at the **end** of policy month m.

    "The account value projected at issue under the pricing path (level 6% gross
    subaccount return, current charges, planned premiums)" **[std]**.  Its close of policy
    month ``m``, the opening balance of month ``m + 1``, ``av_pricing_pp_at(m + 1,
    BEF_PREM)``, is the denominator of :func:`funding_ratio` in that month, and it is a
    genuine second recursion: no decrements, no loans, no withdrawals, ``rho = 1``,
    starting from zero at issue -- ``av_pricing_pp_at(0, BEF_PREM) == 0``.  ``m`` counts
    policy months from issue, 0-based, so this is the notes' ``AV*_{m+1}``.  The
    subaccounts are summed in a loop over the lineup's positions from 0.0, as
    :func:`av_pricing_pp_at` sums its own.
    """
    av = 0.0
    for i in range(subaccount_count()):
        av = av + sa_pricing_pp(m, i)
    return av + fa_pricing_pp(m)


def db_pricing_pp(m):
    """The pricing-path death benefit in policy month m, after the corridor test.

    Uses :func:`corridor_factor_at` at the pricing path's own attained age rather than
    :func:`corridor_factor`, whose first-month pin belongs to the projection and not to
    this benchmark.  The option is read through its decodes, :func:`is_db_option_a` and
    :func:`is_db_option_b`, not as text.
    """
    av = av_pricing_pp_at(m, BEF_FEE)
    if is_db_option_a():
        opt = sum_assured()
    elif is_db_option_b():
        opt = sum_assured() + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor_at(age_pricing(m)) * av)


def naar_pricing_pp(m):
    """The pricing-path net amount at risk, ``max(0, DB* - AV*')``, undiscounted [S2]."""
    return max(0.0, db_pricing_pp(m) - av_pricing_pp_at(m, BEF_FEE))


def mth_deduction_pricing_pp(m):
    """The pricing-path monthly deduction: current charges, as the notes specify.

    ``e_pol + e_face x U + c x NAAR*/1000``, zero from attained age 121.  The current
    COI scale comes from :func:`coi_rate_at`, the rule, never from a model point's
    first-month pin: the pricing path is a seventy-year benchmark and a single
    disclosed rate is not a scale.
    """
    if age_pricing(m) >= charges_cease_age:                          # noqa: F821
        return 0.0
    return (expense_pol_mth + expense_unit_mth * units()             # noqa: F821
            + coi_rate_at(policy_year_pricing(m)) / 1000 * naar_pricing_pp(m))


def funding_ratio(t):
    """phi_t: the funding ratio ``AV_t / AV*_t`` **[std]**.

    Both sides are measured at the **start** of month t, before the premium, so the
    dynamic multipliers that consume it cannot depend on the premium they help
    determine: ``av_pp_at(t, BEF_PREM)`` against the pricing path's opening balance
    of the same policy month from issue, ``av_pricing_pp_at(duration_mth(t),
    BEF_PREM)``.  ``phi_t < 1`` is a performance or funding shortfall.

    Returns 1.0 -- no dynamic effect -- when the behavior module is off, and also when
    the pricing path's opening balance is at or below 0: in the issue month of a point,
    ``duration_mth(t) == 0``, where it has accumulated nothing yet, and in any month its
    deductions have run it down to 0 or below.  And 1.0 outside cover, before the policy
    month is computed: before issue ``duration_mth(t)`` is negative, and the path, based
    at issue, would recurse without end from a month before it.  The path is a projection
    made at issue, on the policy clock, deterministic, and reads no state, so a point in
    force reads it from issue, one cell a month, and needs no opening value for it: its
    first month on the books reads the path cold, back to issue, however the months after
    it are evaluated.
    """
    if not dyn_behavior_on:                                          # noqa: F821
        return 1.0
    if not is_active(t):
        return 1.0
    star = av_pricing_pp_at(duration_mth(t), BEF_PREM)
    if star <= 0:
        return 1.0
    return av_pp_at(t, BEF_PREM) / star


def prem_persistency_base(t):
    """rho^base_t: the base fraction of the planned premium paid in the policy year of t.

    1.00 in year 1 grading to 0.85 in year 5 and 0.80 thereafter, read from
    *prem_persistency.csv* at the policy year of month t by :func:`prem_persistency_py`.
    The levels come from the UL premium persistency study [REG-R21] applied to VUL by
    analogy -- no VUL-specific study was retrieved, which the notes flag.  Zero outside
    cover, before the table is read: before issue the valuation clock reaches policy
    years 0 and below.
    """
    return prem_persistency_py(policy_year(t)) if is_active(t) else 0.0


def prem_persistency_py(y):
    """rho^base in policy year y, from *prem_persistency.csv*: the table's one reader.

    ``Data.prem_persistency_array()`` at the year, the table padded from year 0, so that
    the year is the index.  Policy years beyond the table take its last row, the last year
    ``data.prem_persistency_last_year()`` gives, which it reads from the table's key
    column once it has checked the keys and the factors, before any factor is read.  A
    year below 1, before the table's first row, where ``VUL_US_S``'s ``.loc`` raised
    ``KeyError``, is refused, naming the point and the year, so that the padding is never
    read.  Keyed by the contractual policy year, so the table is read once a policy year
    rather than once a month; :func:`prem_persistency_base` calls it inside cover only.
    """
    last = data.prem_persistency_last_year()                         # noqa: F821
    if y < 1:
        raise ValueError(f"point_id {point_id()}: prem_persistency.csv has no factor for "
                         f"policy year {y}")
    return float(data.prem_persistency_array()[min(y, last)])        # noqa: F821


def prem_persistency(t):
    """rho_t: the fraction of the planned premium actually paid **[std]**.

    ``rho^base_t x min(1.3, max(0.7, phi_t^-0.25))``: a funding shortfall induces
    catch-up funding by retained policyholders, strong performance induces premium
    holidays -- the signature flexible-premium behavior the UL studies measure
    [REG-R21].

    **1.0 when the behavior module is off**, which is the default.  The base
    deterministic run therefore pays the planned premium in full, which is what the
    notes' worked example does ("planned premium $500/month paid"); switching
    ``dyn_behavior_on`` on brings in both the base persistency scale and the funding
    adjustment.  ``Term_US_S`` switches conversion off for the same reason.  Zero outside
    cover, before either, where no premium is paid.
    """
    if not is_active(t):
        return 0.0
    if not dyn_behavior_on:                                          # noqa: F821
        return 1.0
    phi = funding_ratio(t)
    if phi <= 0:
        adj = prem_pers_cap                                          # noqa: F821
    else:
        adj = min(prem_pers_cap,                                     # noqa: F821
                  max(prem_pers_floor, phi ** (-prem_pers_delta)))   # noqa: F821
    return prem_persistency_base(t) * adj


def premium_pp(t):
    """P_t: the gross premium per policy paid at the monthiversary of month t.

    ``LEVEL``
        The planned annual premium / 12, times :func:`prem_persistency`.
    ``SINGLE``
        One premium in the issue month, ``duration_mth(t) == 0``: ``t = 0`` for a point
        issued at the valuation date, ``t = k`` for one issued ``k`` months later, and
        never for a point already in force.

    Zero from attained age 121, when premiums are no longer accepted [S1][S2][S4], and
    zero outside cover.  Guideline premium and 7-pay limits are not enforced in the
    baseline; premiums are assumed within limits **[std]**.  The pattern is read through
    its decodes, :func:`is_single_premium` and :func:`is_level_premium`, not as text.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    if is_single_premium():
        return premium_pp_ann() if duration_mth(t) == 0 else 0.0
    elif is_level_premium():
        return premium_pp_ann() / 12 * prem_persistency(t)
    else:
        raise ValueError("invalid premium type")


def prem_to_av_pp(t):
    """The net premium credited to the accounts, ``P_t x (1 - gamma)``.

    Split by :func:`alloc` and :func:`alloc_fixed`.  The net premium is a pass-through
    into the policyholder's accounts; the load is insurer revenue.
    """
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_av(t):
    """Net premium credited to the accounts, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """prem_gross: premium income at BOM of month t, weighted by the in force.

    The **full** premium, not the load: the net premium is a pass-through into the
    accounts and shows up again as an account release when a claim is paid.
    """
    return premium_pp(t) * pols_if(t)


def premium_loads(t):
    """load_income: the premium load the insurer keeps, ``gamma x P_t x l_t``."""
    return load_prem_rate() * premium_pp(t) * pols_if(t)


def wd_pp(t):
    """W(t): the partial withdrawal per policy at the monthiversary of month t.

    The constant monthly figure :func:`wd_pp_mth`, the model point's ``wd_pp`` column,
    from the valuation date on, **0 in every shipped model point**: the notes make
    withdrawals explicitly none in the baseline, so the mechanics are implemented and the
    behavior is left to the data **[std]**.  Not taken from attained age 121, and zero
    outside cover, before either, so that nothing is withdrawn at ``t = proj_len()``
    whatever ``omega_age`` and ``charges_cease_age`` are set to.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return wd_pp_mth()


def wd_fee_pp(t):
    """The $25 withdrawal fee, charged only in a month with a withdrawal [S1].

    Retained by the insurer, so it is account-value outgo but not a liability cash
    flow; it appears in :func:`margin_expense`, not in :func:`claims`.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def wd_sa_pp(t, i):
    """The part of the withdrawal and its fee taken from subaccount i.

    Pro rata over the **unloaned** accounts, on balances measured after the premium
    **[std]**; the loan account is collateral and is not available.  The denominator is
    guarded exactly as :func:`mth_deduction_sa_pp` guards it, and for the same reason.
    """
    den = unloaned_av_pp_at(t, BEF_WD)
    share = sa_pp_at(t, i, BEF_WD) / den if den > 0 else alloc(i)
    return (wd_pp(t) + wd_fee_pp(t)) * share


def wd_fa_pp(t):
    """The part of the withdrawal and its fee taken from the fixed option."""
    den = unloaned_av_pp_at(t, BEF_WD)
    share = fa_pp_at(t, BEF_WD) / den if den > 0 else alloc_fixed()
    return (wd_pp(t) + wd_fee_pp(t)) * share


def face_reduction_pp(t):
    """The face reduction a withdrawal forces under Option A [S1][S2].

    **Proportionate**: the face is cut in the same proportion as the withdrawal bears
    to the account value, ``F x W / AV``.  Note the contrast with the fixed-UL chassis,
    which instead cuts the face by the excess of the withdrawal over a free amount --
    the variable-UL notes say proportionate, and that is what is implemented here.
    Under Option B the withdrawal reduces the account value only, and this is zero.

    ``F`` is the face entering the month: the previous month's :func:`sum_assured_at`,
    and in the first month on the books, :func:`t_entry`, the face in force at the
    valuation date, :func:`sum_assured_init`, on a point in force, and the face at issue,
    :func:`sum_assured`, on any other.  The option is read through its decode,
    :func:`is_db_option_a`.
    """
    if not is_db_option_a() or wd_pp(t) <= 0:
        return 0.0
    av = av_pp_at(t, BEF_WD)
    if av <= 0:
        return 0.0
    if t > t_entry():
        face = sum_assured_at(t - 1)
    elif duration_mth_init() > 0:
        face = sum_assured_init()
    else:
        face = sum_assured()
    return face * wd_pp(t) / av


def sum_assured_at(t):
    """F_t: the face in force from the monthiversary of month t, after any reduction.

    The face the death benefit of month ``t`` is measured on, at BOM and at EOM alike,
    since the only movement is the Option A withdrawal reduction taken at the
    monthiversary.  The face entering the first month on the books, :func:`t_entry`, is
    the face in force at the valuation date, :func:`sum_assured_init`, on a point in
    force, and the face at issue, :func:`sum_assured`, on any other; the face entering a
    later month is the previous month's, this cell at ``t - 1``, which it calls before
    anything else, so the chain back to :func:`t_entry` is one cell a month.  Face
    increases, elective decreases and option changes are not modeled.  Zero outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        prev = sum_assured_at(t - 1)
    elif duration_mth_init() > 0:
        prev = sum_assured_init()
    else:
        prev = sum_assured()
    return max(0.0, prev - face_reduction_pp(t))


def unloaned_av_pp_at(t, timing):
    """The unloaned account value: subaccounts plus the fixed option, excluding LA.

    This is the base the withdrawal and the monthly deduction are allocated over
    **[std]** -- the loan account is collateral for the debt and is not drawn on.
    ``timing`` takes the :func:`sa_pp_at` values.  The subaccounts are summed in a loop
    over the lineup's positions from 0.0, as :func:`av_pricing_pp_at` sums its own.
    """
    av = 0.0
    for i in range(subaccount_count()):
        av = av + sa_pp_at(t, i, timing)
    return av + fa_pp_at(t, timing)


def corridor_factor_at(a):
    """kappa: the GPT corridor factor at attained age a [S2][R3], the table's one reader.

    250% to age 40, 215% at 45, 185% at 50, 150% at 55, 130% at 60, then **grading
    linearly to 100% at attained age 95** and level at 100% from there on.  The quoted
    quinquennial factors are sourced; every age between them is **linear interpolation
    [std]**, carried in ``corridor_factors.csv`` to six decimals.

    The notes write the tail as "to 100% at 90-95", which does not say which end of
    that range reaches 100%; the product spec's footnote 11 does -- *"The reference
    model linearly interpolates between the quoted ages and grades to 100% at 95"* --
    so the last quoted age (130% at 60) is joined to 100% at 95, not to 100% at 90.
    The two readings differ over attained ages 61-94: at age 90 this table gives
    ``kappa = 1.042857`` where grading to 90 would give 1.00, and a corridor of exactly
    1.00 would collapse the net amount at risk to zero on an Option A policy funded
    above its face.

    ``Data.corridor_factor_array()`` at the age, the table padded from age 0, so that the
    age is the index.  Ages outside the table take its first or last row: the first and
    last ages ``data.corridor_age_first()`` and ``data.corridor_age_last()`` give, which
    they read from the table's key column once the keys and the factors are checked,
    before any factor is read, the last first, since it runs the checks.  So the padding
    is never read, and no age below 0 is either: ``Data`` refuses a table whose first age
    is negative.  Interpolating is what keeps the death benefit continuous: stepping
    between quinquennial factors would make it jump on every fifth anniversary, which the
    notes list among the modeling pitfalls.  Keyed by the attained age, so the table is
    read once an age rather than once a month; :func:`corridor_factor` calls it inside
    cover only, and the pricing path from the issue age on.
    """
    last = data.corridor_age_last()                                  # noqa: F821
    a = min(max(a, data.corridor_age_first()), last)                 # noqa: F821
    return float(data.corridor_factor_array()[a])                    # noqa: F821


def corridor_factor(t):
    """kappa_t: the corridor factor in month t, at the **attained** age.

    Only the Guideline Premium Test is modeled; CVAT is a documented variation, so any
    other ``qual_test`` raises rather than being treated as GPT, in whatever month, since
    it is a fault of the point; the test is read through its decode, :func:`is_gpt`.  Zero
    outside cover, before the table is read.

    A model point may pin the factor **in the valuation month**, ``t = 0``, through the
    ``corridor_override_m1`` column (:func:`has_corridor_override_m1`,
    :func:`corridor_override_m1`).  Model point 1 does, at 2.15, because the notes'
    worked example sits in policy year 3 -- attained age 47, where the rule gives
    2.03 -- but quotes ``kappa(45) = 215%``, the **issue**-age factor.  The pin
    reproduces the worked example's corridor product exactly.  Point 1 is in force at the
    valuation date, and its ``t = 0``, the valuation month, is the one month the worked
    example describes, which is what the ``_m1`` in the column name, "the first month",
    means here, as it means the first month of ``VUL_US_S``'s own frame.

    The pin is deliberately confined to that one month.  It is a *lookup* that the notes
    performed at the wrong age, not a parameter of the contract; holding an issue-age
    corridor factor across the seventy-seven years this projection runs would misstate
    every later month and is no reading of the notes at all.  Model point 2 is the same
    cell with the pin blank, so the rule applies from the first month too, and a test
    holds the gap open in both directions.  ``Data`` refuses a pin on a point issued after
    the valuation date, where ``t = 0`` precedes issue and the pin would never apply, and
    the generator leaves it blank on every point it restates in force at a later month.
    """
    if not is_gpt():
        raise ValueError("invalid qual_test")
    if not is_active(t):
        return 0.0
    if t == 0 and has_corridor_override_m1():
        return corridor_override_m1()
    return corridor_factor_at(age(t))


def db_corridor_pp(t):
    """The corridor minimum death benefit, ``kappa_t x AV'(t)``.

    Named because the worked example displays it: at the anchor cell it is
    ``2.15 x 50,480 = 108,532.00``, which loses to the $500,000 face.  The corridor
    binds only on heavily funded, older cells.
    """
    return corridor_factor(t) * av_pp_at(t, BEF_FEE)


def db_pp(t):
    """DB_t: the death benefit per policy at the monthiversary, after the corridor test.

    Option A ``max(F_t, kappa_t x AV'(t))``; Option B ``max(F_t + AV'(t),
    kappa_t x AV'(t))``, where ``AV'(t)`` is the account value after premium and
    withdrawal and **before** the monthly deduction [S2][R3].  Measuring the account
    value at that point is what removes the circularity: under Option B the death
    benefit depends on the account value and the net amount at risk depends on the
    death benefit, but with this ordering neither depends on the deduction.  The option
    is read through its decodes, :func:`is_db_option_a` and :func:`is_db_option_b`, not
    as text.  Zero outside cover, before the corridor table is read.
    """
    if not is_active(t):
        return 0.0
    av = av_pp_at(t, BEF_FEE)
    if is_db_option_a():
        opt = sum_assured_at(t)
    elif is_db_option_b():
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, db_corridor_pp(t))


def net_amt_at_risk(t):
    """NAAR_t: ``max(0, DB_t - AV'(t))`` [S2]; floor **[std]**.

    **No one-month discount.**  This is the single sourced deviation from the
    fixed-UL chassis, which divides the death benefit by ``1 + i_gm`` first: the VUL
    prospectuses define the net amount at risk as death benefit less account value
    outright [S2], so there is no ``naar_factor`` in this model.  Carrying the chassis
    recursion across unexamined would understate the net amount at risk, and with it
    the cost of insurance, by about one month's guaranteed interest on the death
    benefit every month.

    The floor at zero is a standardization: the corridor keeps ``DB >= AV`` in normal
    operation, and forgetting the floor is on the notes' pitfall list.
    """
    return max(0.0, db_pp(t) - av_pp_at(t, BEF_FEE))


def coi_schedule():
    """The number of this point's guaranteed COI scale, its row of ``Data.coi_rate_array``.

    ``Data.coi_schedule`` at this point: ``Data`` numbers each issue-age cell of
    *coi_rates.csv*, its ``sex``, ``rate_class`` and ``age_at_entry``, from 1 in the order
    of those keys, and gives each point the number of its own, or 0 where the table has no
    scale for it.  ``VUL_US_S`` slices the scale, a Series, by the same three keys in
    ``coi_rate_scale``, which this replaces, since no compiled cell returns a Series.  A
    point without a scale is projected as ``VUL_US_S`` projects it while no COI rate is
    read, and refused by :func:`coi_rate_last_year` once one is.
    """
    return int(data.coi_schedule()[idx])                             # noqa: F821


def coi_rate_last_year():
    """The last policy year of this point's guaranteed COI scale: its extent.

    ``Data.coi_rate_last_years`` at this point's :func:`coi_schedule`, the last year of
    its scale, which ``Data`` reads from the table's key columns once it has checked the
    keys and the rates.  77 on the shipped anchor cell, whose scale runs to attained age
    121.  A point the table has no scale for, schedule 0, has a last year of 0, and is
    refused here, naming it, where ``VUL_US_S``'s slice raised ``KeyError``: when its first
    COI rate is read, and not before, since a point valued, or issued, at or past
    ``charges_cease_age`` never reads one, and ``VUL_US_S`` projects it.  The element is
    compared, and ``int`` of it returned, rather than held in a local first: in a
    formula that also builds a message, such a local would compile as a Python object.
    """
    if data.coi_rate_last_years()[coi_schedule()] < 1:               # noqa: F821
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no scale for the "
                         f"point's sex, rate_class and age_at_entry")
    return int(data.coi_rate_last_years()[coi_schedule()])           # noqa: F821


def coi_rate_guar_at(y):
    """The guaranteed maximum monthly COI rate per $1,000 NAAR in policy year y.

    An illustrative **[std]** stand-in for the licensed 2017 CSO sex-distinct
    smoker/nonsmoker ultimate ANB table the notes require [S2][S4][R12], anchored on
    the one disclosed guaranteed point -- male 45 standard non-tobacco, policy year 1
    = $0.22 [S4].  Capped at ``coi_rate_cap`` ($83.34, observed $83.33-$83.34 across
    filings), the monthly rate that fully consumes the net amount at risk near attained
    age 120 [S1][S2][S3][S4].  ``Data.coi_rate_array()`` at the point's
    :func:`coi_schedule` and the year, each schedule padded from year 0, so that the year
    is the column.  Policy years beyond the table take its last row,
    :func:`coi_rate_last_year`, which is asked for first, so that a projection meets the
    check of the table's keys, and the refusal of a point without a scale, before any
    rate is read.  A year below 1, where ``VUL_US_S``'s slice raised ``KeyError``, is
    refused, naming the point and the year, so that the padding is never read.  The
    scale's one reader, keyed by the contractual policy year; :func:`coi_rate_guar` calls
    it inside cover only, and the pricing path from issue.
    """
    last = coi_rate_last_year()
    if y < 1:
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no rate for policy "
                         f"year {y}")
    return min(float(data.coi_rate_array()[coi_schedule(), min(y, last)]),  # noqa: F821
               coi_rate_cap)                                         # noqa: F821


def coi_rate_guar(t):
    """The guaranteed maximum monthly COI rate in month t.

    Read at the policy year of month t by :func:`coi_rate_guar_at`; zero outside cover,
    before the scale is read.
    """
    return coi_rate_guar_at(policy_year(t)) if is_active(t) else 0.0


def coi_rate_at(y):
    """c: the current monthly COI rate per $1,000 NAAR in policy year y **[std]**.

    ``coi_curr_factor`` (50%) of the guaranteed maximum -- the notes' stated default
    placeholder for the current scale -- bounded above by the guaranteed maximum and by
    the $83.34 cap [S2][S4][R12].  Current COI tables are not publicly disclosed; only
    minima, maxima and representative points appear in prospectuses, so this factor is
    a pure modeling assumption and the notes rank it the second most important
    assumption in the model.

    Note the units: per $1,000 of net amount at risk per **month**, so it is divided by
    1,000 in :func:`coi_pp`.  It is not comparable with ``CashValue_SE.coi_rate``,
    which is a rate per unit of account value.
    """
    rate = coi_curr_factor * coi_rate_guar_at(y)                     # noqa: F821
    return min(rate, coi_rate_guar_at(y), coi_rate_cap)              # noqa: F821


def coi_rate(t):
    """c_t: the current monthly COI rate in month t.

    A model point may pin the rate **in the valuation month**, ``t = 0``, through the
    ``coi_rate_override_m1`` column (:func:`has_coi_rate_override_m1`,
    :func:`coi_rate_override_m1`).  Model point 1 does, at 0.04: that is the year-1
    current rate disclosed for this cell [S4], which the notes' worked example applies
    in policy year 3, and it is 18% of the year-1 guaranteed $0.22 rather than the 50%
    the placeholder assumes.  The notes acknowledge the gap themselves -- "disclosed
    year-1 current/guaranteed ratios are much lower (select effect)" -- so the
    placeholder is conservative early and the select-to-ultimate shape matters.

    As with :func:`corridor_factor`, the pin is confined to that one month, the one the
    worked example describes: a single disclosed point is not a scale, and holding $0.04
    flat for seventy-seven years would leave a policy paying almost nothing for its
    insurance at age 100.  Model point 2 is the same cell with the pin blank and takes
    the placeholder from the first month, and a test holds the gap open in both
    directions.  Zero outside cover, before either.  A COI rate is a charge per $1,000 of
    net amount at risk, not a decrement, and is never capped at 1: the current rate
    passes 1 from attained age 72 on the shipped scale, as it should.
    """
    if not is_active(t):
        return 0.0
    if t == 0 and has_coi_rate_override_m1():
        return min(coi_rate_override_m1(), coi_rate_guar(t), coi_rate_cap)  # noqa: F821
    return coi_rate_at(policy_year(t))


def coi_pp(t):
    """COI_t: the cost of insurance charge per policy, ``c_t / 1000 x NAAR_t``.

    Zero from attained age 121, when monthly deductions cease [S1][S2][S4], and zero
    outside cover.

    The rate here is the **current COI scale** -- insurer revenue, a non-guaranteed
    element under ASOP 2 [R11].  It is not the death decrement: that is
    :func:`mort_rate`, best-estimate experience.  The notes are emphatic that the two
    must never be conflated, and they are deliberately different tables here.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def coi(t):
    """Cost of insurance charges deducted from account values, for the policies in force."""
    return coi_pp(t) * pols_if(t)


def rider_charge_pp(t):
    """rc(t): rider charges, 0 in the baseline **[std]**.

    The no-lapse guarantee and overloan protection riders are documented variations
    that the notes exclude from the baseline; this term is carried in the monthly
    deduction so a rider module can be added without changing the recursion.
    """
    return 0.0


def maint_fee_pp(t):
    """The non-COI part of the monthly deduction per policy.

    ``e_pol + e_face x U + rc(t)``: the $10.00 per-policy administrative charge
    [S2][S4] and the $0.20 per $1,000 of **initial** face charge [S2], both level in
    all years, plus rider charges.  Zero from attained age 121, when deductions cease
    [S1][S2][S4], and zero outside cover.

    The name follows ``CashValue_SE.maint_fee``: this is a *charge* against the account
    value and therefore insurer income.  It is not :func:`expenses`, which is the
    insurer's own outgo.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return (expense_pol_mth + expense_unit_mth * units()             # noqa: F821
            + rider_charge_pp(t))


def maint_fee(t):
    """Non-COI monthly charges deducted from account values, for the policies in force."""
    return maint_fee_pp(t) * pols_if(t)


def mth_deduction_pp(t):
    """MD_t: the monthly deduction per policy, taken at the monthiversary.

    ``COI_t + e_pol + e_face x F_0/1000``, i.e. :func:`maint_fee_pp` plus
    :func:`coi_pp`.  The M&E charge is **not** part of it -- that is collected inside
    the unit values by :func:`inv_return_mth`, and taking it in both places is on the
    notes' pitfall list.
    """
    return maint_fee_pp(t) + coi_pp(t)


def mth_deduction(t):
    """md_income: monthly deductions collected, for the policies in force."""
    return mth_deduction_pp(t) * pols_if(t)


def mth_deduction_sa_pp(t, i):
    """The monthly deduction's pro-rata share taken from subaccount i **[std]**.

    ``MD_t x SA_i / sum(unloaned)``, on balances measured after the premium and the
    withdrawal.  The loan account is excluded because it is collateral.

    The denominator is guarded -- the notes list an unguarded one among the modeling
    pitfalls -- and the guard falls back to the **premium allocation** shares
    ``alpha_i`` **[std]**.  That keeps the full deduction applied, so the account value
    roll-forward stays exact, and it matters only once the unloaned balance has run to
    zero or below, which is well past the month :func:`is_shortfall` first fires.  The
    notes would have defaulted the policy there; the grace cascade is not implemented,
    so the arithmetic simply continues, as it does on the fixed-UL chassis.  Whatever
    fallback is chosen, the shares sum to one, which is what the identity needs.
    """
    den = unloaned_av_pp_at(t, BEF_FEE)
    share = sa_pp_at(t, i, BEF_FEE) / den if den > 0 else alloc(i)
    return mth_deduction_pp(t) * share


def mth_deduction_fa_pp(t):
    """The monthly deduction's pro-rata share taken from the fixed option **[std]**."""
    den = unloaned_av_pp_at(t, BEF_FEE)
    share = fa_pp_at(t, BEF_FEE) / den if den > 0 else alloc_fixed()
    return mth_deduction_pp(t) * share


def sa_pp_at(t, i, timing):
    """Subaccount i's value per policy at an intra-month point of month t.

    The events change the balance in this order, and ``timing`` names the point just
    before each of them:

    ``BEF_PREM``
        Before the premium: the closing balance of the previous month, or the model
        point's opening balance ``sa_pp_init(i)`` -- the notes' ``SA_i(0)`` -- in the
        first month on the books, :func:`t_entry`: the subaccount's value at the
        valuation date on a point in force, 0 at issue.  The previous month's close is
        formed here, from this timing's own value at ``t - 1`` and month ``t - 1``'s net
        premium share, withdrawal share, deduction share and unit-value growth, the same
        products in the same order as ``sa_pp(t - 1, i)``, rather than called for, so
        the chain of calls back to :func:`t_entry` is one cell a month, where
        ``VUL_US_S``'s ran through six.  Zero outside cover.

    ``BEF_WD``
        After this subaccount's share ``alpha_i`` of the net premium.

    ``BEF_FEE``
        After the withdrawal and its fee, before the monthly deduction.  Summed across
        the accounts this is the notes' post-premium value ``AV'``, the balance the
        death benefit, corridor test and net amount at risk are all measured against.

    ``BEF_INV``
        After the monthly deduction, before growth.  Growth applies to this
        post-deduction balance; reversing the two overstates the account value by about
        one month's return on the deduction every month.

    ``BEF_ME``
        After the gross return and the fund expense, before the M&E charge.  This is
        the balance the M&E charge is taken from, so it is what :func:`me_charge_sa_pp`
        measures.  Zero outside cover, before the return scenario is read.

    The end-of-month balance is :func:`sa_pp`.  Every timing is zero outside cover,
    ``t = proj_len()`` included.
    """
    if timing == BEF_PREM:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return sa_pp_init(i)
        bef = sa_pp_at(t - 1, i, BEF_PREM) + alloc(i) * prem_to_av_pp(t - 1)
        bef = bef - wd_sa_pp(t - 1, i)
        bef = bef - mth_deduction_sa_pp(t - 1, i)
        bef = bef * (1 + gross_return_mth(t - 1, i)) * (1 - fund_expense_ann(i) / 12)
        return bef * (1 - me_rate_ann / 12)                          # noqa: F821
    elif timing == BEF_WD:
        return sa_pp_at(t, i, BEF_PREM) + alloc(i) * prem_to_av_pp(t)
    elif timing == BEF_FEE:
        return sa_pp_at(t, i, BEF_WD) - wd_sa_pp(t, i)
    elif timing == BEF_INV:
        return sa_pp_at(t, i, BEF_FEE) - mth_deduction_sa_pp(t, i)
    elif timing == BEF_ME:
        if not is_active(t):
            return 0.0
        return (sa_pp_at(t, i, BEF_INV) * (1 + gross_return_mth(t, i))
                * (1 - fund_expense_ann(i) / 12))
    else:
        raise ValueError("invalid timing")


def sa_pp(t, i):
    """SA_{i,t+1} in the notes: subaccount i's value per policy at the **end** of month t.

    The post-deduction balance times the unit-value factor ``(1 + r)(1 - e_i/12)(1 -
    m/12)``, which is ``1 + inv_return_mth(t, i)``; the opening balance ``SA_i(0) =
    sa_pp_init(i)`` is ``sa_pp_at(t_entry(), i, BEF_PREM)``, not a row of this cell.
    Separate-account assets: the policyholder bears the investment experience and the
    insurer's general account does not.  Zero outside cover, through its timings.
    """
    return sa_pp_at(t, i, BEF_ME) * (1 - me_rate_ann / 12)         # noqa: F821


def fa_pp_at(t, timing):
    """The fixed-option value per policy at an intra-month point of month t.

    ``timing`` takes the same values as :func:`sa_pp_at` except ``BEF_ME``: the
    fixed option is a general-account balance and bears neither fund expenses nor the
    M&E charge.  ``BEF_PREM`` is the closing balance of the previous month, or the
    opening balance ``fa_pp_init()`` -- the notes' ``FA(0)`` -- in the first month on the
    books, :func:`t_entry`.  The previous month's close is formed here, from this
    timing's own value at ``t - 1`` and month ``t - 1``'s net premium share, withdrawal
    share, deduction share and interest, as ``fa_pp(t - 1)`` forms it, rather than called
    for, so the chain back to :func:`t_entry` is one cell a month, where ``VUL_US_S``'s
    ran through five.  Zero outside cover.
    """
    if timing == BEF_PREM:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return fa_pp_init()
        bef = fa_pp_at(t - 1, BEF_PREM) + alloc_fixed() * prem_to_av_pp(t - 1)
        bef = bef - wd_fa_pp(t - 1)
        bef = bef - mth_deduction_fa_pp(t - 1)
        return bef * (1 + fixed_return_mth(t - 1))
    elif timing == BEF_WD:
        return fa_pp_at(t, BEF_PREM) + alloc_fixed() * prem_to_av_pp(t)
    elif timing == BEF_FEE:
        return fa_pp_at(t, BEF_WD) - wd_fa_pp(t)
    elif timing == BEF_INV or timing == BEF_ME:                       # noqa: F821
        return fa_pp_at(t, BEF_FEE) - mth_deduction_fa_pp(t)
    else:
        raise ValueError("invalid timing")


def fa_pp(t):
    """FA_{t+1} in the notes: the fixed-option value per policy at the **end** of month t.

    ``FA'(t) x (1 + i_fix)^(1/12)`` at the declared rate, floored at the contractual
    1.0% [S1]; the opening balance ``FA(0) = fa_pp_init()`` is ``fa_pp_at(t_entry(),
    BEF_PREM)``.  A general-account liability, unlike the subaccounts.  The declared
    rate is month t's own, on the valuation clock (:func:`crediting_rate_ann`).
    """
    return fa_pp_at(t, BEF_INV) * (1 + fixed_return_mth(t))


def la_pp_at(t, timing):
    """The loan-account collateral per policy at an intra-month point of month t.

    The loan account does not move intra-month -- new loans and repayments are not
    modeled, and it accrues only at end of month -- so every :func:`sa_pp_at`
    ``timing`` returns the **opening** balance: the closing balance of the previous
    month, or :func:`la_pp_init` in the first month on the books, :func:`t_entry`, the
    notes' ``LA(0)``.  ``VUL_US_S`` takes ``loan_bal_init()`` there **[std]** -- a loan
    moves value out of the investment options into a general-account loan account, so
    collateral and debt coincide on the loan's first day -- and a point in force here
    brings the collateral its loan has earned since.  The previous month's close is
    formed here, the timing's value at ``t - 1`` grown one month at the credited loan
    rate, as ``la_pp(t - 1)`` forms it, so the chain back to :func:`t_entry` is one cell
    a month, where ``VUL_US_S``'s ran through two.  Zero outside cover,
    ``t = proj_len()`` included, so that the account carried there earns no month's
    credit past the frame's end.
    """
    if (timing == BEF_PREM or timing == BEF_WD or timing == BEF_FEE   # noqa: F821
            or timing == BEF_INV or timing == BEF_ME):                # noqa: F821
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return la_pp_init()
        return la_pp_at(t - 1, BEF_PREM) * (1 + loan_cr_rate_mth(t - 1))
    else:
        raise ValueError("invalid timing")


def la_pp(t):
    """LA_{t+1} in the notes: the loan-account collateral per policy at the end of month t.

    The opening collateral ``la_pp_at(t, BEF_PREM)`` grown one month at the credited
    loan rate ``i_C`` [S3], **not** fund returns, which is why it is held apart from the
    subaccounts and excluded from the pro-rata deduction base.  It is part of the
    account value; the debt is not.

    New loans and repayments are not modeled -- the notes give no utilization pattern
    -- so this only rolls the model point's opening collateral forward.  Zero outside
    cover, through its opening value.
    """
    return la_pp_at(t, BEF_PREM) * (1 + loan_cr_rate_mth(t))


def loan_bal_pp_at(t, timing):
    """The outstanding policy debt per policy at an intra-month point of month t.

    Debt accrues only at end of month, so every :func:`sa_pp_at` ``timing`` returns
    the **opening** debt: the closing balance of the previous month, or
    :func:`loan_bal_init` in the first month on the books, :func:`t_entry`, the notes'
    ``D(0)``.  The previous month's close is formed here, the timing's value at ``t - 1``
    times one month of the charged rate, as ``loan_bal_pp(t - 1)`` forms it, so the chain
    back to :func:`t_entry` is one cell a month, where ``VUL_US_S``'s ran through two.
    Zero outside cover: nothing reads the debt at ``t = proj_len()``, where it would
    turn the death claim on a death benefit of 0 negative.
    """
    if (timing == BEF_PREM or timing == BEF_WD or timing == BEF_FEE   # noqa: F821
            or timing == BEF_INV or timing == BEF_ME):                # noqa: F821
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return loan_bal_init()
        return loan_bal_pp_at(t - 1, BEF_PREM) * (1 + loan_rate_mth(t - 1))
    else:
        raise ValueError("invalid timing")


def loan_bal_pp(t):
    """D_{t+1} in the notes: the outstanding policy debt per policy at the end of month t.

    The opening debt ``loan_bal_pp_at(t, BEF_PREM)`` times ``(1 + i_L)^(1/12)``, the
    charged rate, monthly **[std]** where the contract charges interest annually in
    arrears and capitalizes it if unpaid [S1].  Debt reduces both the death benefit and
    the surrender value; it grows faster than the collateral in :func:`la_pp`, and the
    difference is the insurer's :func:`loan_spread`.

    Note the notes' indexing: their ``D_{t+1}`` is this end-of-month balance of month
    ``t``, which is why the death claim is ``DB_t^EOM - D_{t+1}``.  Zero outside cover,
    through its opening value.
    """
    return loan_bal_pp_at(t, BEF_PREM) * (1 + loan_rate_mth(t))


def loan_spread(t):
    """loan_spread: the insurer's margin on policy debt, for the policies in force.

    ``l_t x D_t x [(1 + i_L)^(1/12) - (1 + i_C)^(1/12)]`` -- one month of the charged
    rate less one month of the credited rate on the opening debt
    ``loan_bal_pp_at(t, BEF_PREM)``.  1.0% a year in policy years 1-9 and 0.05% from
    the 10th [S1].
    """
    return (loan_bal_pp_at(t, BEF_PREM)
            * (loan_rate_mth(t) - loan_cr_rate_mth(t)) * pols_if(t))


def av_pp_at(t, timing):
    """AV per policy at an intra-month point of month t.

    ``sum(SA_i) + FA + LA``.  ``BEF_PREM`` is the notes' ``AV_t``, the balance at
    the start of the month: the closing balance ``av_pp(t - 1)`` of the previous
    month, or :func:`av_pp_init` in the first month on the books, :func:`t_entry` --
    the account value at the valuation date on a point in force, 0 at issue.  It is not a
    chain of its own: its parts are, and it sums their closes.  It is also defined in the
    month after the frame, ``t = proj_len()``, where it is the account value the survivors
    of the last month carry, which the roll-forward reads; zero before issue.  The loan
    account does not move intra-month -- it accrues only at end of month -- so it enters
    at its opening balance :func:`la_pp_at` whatever the ``timing``, which takes the
    :func:`sa_pp_at` values.  The other timings are zero outside cover, ``t = proj_len()``
    included, through their parts.  An unknown ``timing`` raises from :func:`sa_pp_at`.
    """
    if timing == BEF_PREM:
        if not 0 <= duration_mth(t) <= omega_mth():
            return 0.0
        if t == t_entry():
            return av_pp_init()
        return av_pp(t - 1)
    return unloaned_av_pp_at(t, timing) + la_pp_at(t, timing)


def av_pp(t):
    """AV_{t+1} in the notes: the total account value per policy at the **end** of month t.

    ``sum(SA_i) + FA + LA`` [S1][S2][S3][S4].  The opening value ``AV(0) =
    av_pp_init()`` is ``av_pp_at(t_entry(), BEF_PREM)``, and each component starts at
    its own opening balance.  The subaccounts are summed in a loop over the lineup's
    positions from 0.0, as :func:`av_pricing_pp_at` sums its own.  Zero outside cover,
    through its parts.
    """
    av = 0.0
    for i in range(subaccount_count()):
        av = av + sa_pp(t, i)
    return av + fa_pp(t) + la_pp(t)


def av_at(t, timing):
    """Account value in force at an intra-month point of month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``EOM`` for the closing balance before
    decrements -- the notes' ``av_eop`` reconciliation column.  At ``t = proj_len()``,
    ``av_at(t, BEF_PREM)`` is the account value the survivors of the last month carry,
    which :func:`check_av_roll_fwd` reads.
    """
    if timing == EOM:
        return av_pp(t) * pols_if(t)
    return av_pp_at(t, timing) * pols_if(t)


def av_change(t):
    """Change in the account value in force over month t.

    ``av_at(t + 1, BEF_PREM) - av_at(t, BEF_PREM)``, following ``CashValue_SE``.
    Zero outside cover, before ``t + 1`` is read, so that nothing reads a month past
    ``t = proj_len()``; there the change would otherwise be minus the account value the
    survivors of the last month carry.
    """
    if not is_active(t):
        return 0.0
    return av_at(t + 1, BEF_PREM) - av_at(t, BEF_PREM)


def me_charge_pp(t):
    """me_income per policy: the M&E risk charge collected inside the unit values.

    The total over the lineup of :func:`me_charge_sa_pp`, each subaccount's charge,
    summed in a loop over the lineup's positions from 0.0.  ``VUL_US_S``'s
    ``me_charge_pp(t, i=None)`` is both a subaccount's charge and, with ``i`` left
    ``None``, this total, a generator summed by Python's ``sum``, which compiles to
    neither a C parameter nor a C loop; here the subaccount's charge is a cell of its own,
    and this is the total.  Python's ``sum`` of floats is compensated, but of two it is
    their sum, rounded once, which is what this computes, and its ``0.0`` start keeps
    ``sum``'s, which turns two negative zeros to ``0.0``.  So on the shipped lineup of two
    the total is ``VUL_US_S``'s float in every month.  0.45% a year current [S1], under a
    0.60% guaranteed ceiling **[std]**.

    This is insurer revenue taken from separate-account assets, and it is the only
    charge in this model that is *not* an explicit deduction -- which is why it has to
    be reported separately for the net-of-account view to reconcile.  It continues
    after attained age 121, when the monthly deduction stops [S1][S2][S4].
    """
    me = 0.0
    for i in range(subaccount_count()):
        me = me + me_charge_sa_pp(t, i)
    return me


def me_charge_sa_pp(t, i):
    """The M&E risk charge per policy collected inside subaccount i's unit value.

    ``SA_i (after the gross return and the fund expense) x m / 12``: the balance
    ``sa_pp_at(t, i, BEF_ME)`` times a month of ``me_rate_ann``.  ``VUL_US_S``'s
    ``me_charge_pp(t, i)`` with ``i`` given; :func:`me_charge_pp` is the total, and the
    per-subaccount shares of the family's other amounts are ``*_sa_pp``, as
    :func:`wd_sa_pp` and :func:`mth_deduction_sa_pp` are.
    """
    return sa_pp_at(t, i, BEF_ME) * me_rate_ann / 12                 # noqa: F821


def me_charge(t):
    """me_income: the M&E risk charge collected, for the policies in force."""
    return me_charge_pp(t) * pols_if(t)


def inv_income_pp(t):
    """The total investment credit to the accounts per policy over month t.

    The subaccount growth **net** of fund expenses and the M&E charge, plus the
    fixed-option interest, plus the loan-account interest.  Because it is net, the
    insurer's M&E revenue is *not* in it: :func:`me_charge_pp` reports that separately
    and :func:`check_net_view` puts the two back together.  The subaccounts' growth is
    summed in a loop over the lineup's positions from 0.0, as :func:`av_pp` sums their
    values.  Zero outside cover, through its parts.
    """
    inc = 0.0
    for i in range(subaccount_count()):
        inc = inc + (sa_pp(t, i) - sa_pp_at(t, i, BEF_INV))
    return (inc + fa_pp(t) - fa_pp_at(t, BEF_INV)
            + la_pp(t) - la_pp_at(t, BEF_PREM))


def inv_income(t):
    """Investment credit to the accounts, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month of it.
    """
    return inv_income_pp(t) * pols_if(t)


def db_pp_eom(t):
    """DB_t^EOM: the death benefit recomputed on end-of-month balances **[std]**.

    The notes weight the death claim by ``l_t q^d_t`` at end of month and recompute the
    option and corridor formula on the end-of-month account value, so a death in month
    ``t`` is paid on ``DB_t^EOM``, not on the monthiversary figure that priced the
    month's cost of insurance.  The option is read through its decodes,
    :func:`is_db_option_a` and :func:`is_db_option_b`.  Zero outside cover, before the
    corridor table is read.
    """
    if not is_active(t):
        return 0.0
    av = av_pp(t)
    if is_db_option_a():
        opt = sum_assured_at(t)
    elif is_db_option_b():
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor(t) * av)


def net_amt_at_risk_eom(t):
    """NAAR_t^EOM: ``max(0, DB_t^EOM - AV_t)``, the net general-account strain.

    This, not the death benefit, is what the insurer's own funds have to find when a
    policy dies: the account value is seized to fund the rest.  It is the notes'
    ``claim_net`` before survivorship weighting -- and it is emphatically **not** the
    claim cash flow; see :func:`claims`.
    """
    return max(0.0, db_pp_eom(t) - av_pp(t))


def surr_charge_rate(t):
    """SC per $1,000 of initial face in the policy year of month t **[std]**.

    ``sc_init x (runoff_years + 1 - y) / runoff_years``, floored at zero: $18.00 per
    $1,000 in policy year 1, declining **by policy year** to zero at the end of policy
    year 14.  In policy year 3 that is ``18.00 x 12/14 = 15.428571``, the factor the
    worked example quotes.  ``sc_init`` and ``runoff_years`` are the schedule's,
    :func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`.  ``VUL_US_S``
    divides by the ``int()`` of the run-off; ``Data`` holds it to a whole number of years
    below ``2**53``, where the float is that int exactly, so the float gives the same
    quotient bit for bit, and compiles to C, where an ``int()`` held in a local would
    compile as a Python object.

    Note the contrast with the fixed-UL chassis, whose surrender charge amortizes every
    *month*.  The variable-UL notes step it by policy year, and the worked example pins
    the step: carrying the chassis's monthly run-off across would give
    ``18 x (1 - 25/168)`` here instead.  Zero outside cover, before the policy year is
    read.
    """
    if not is_active(t) or not has_surr_charge():
        return 0.0
    init = surr_charge_rate_max()
    yrs = surr_charge_runoff_years()
    return max(0.0, init * (yrs + 1 - policy_year(t)) / yrs)


def surr_charge_pp(t):
    """SC_t: the surrender charge scheduled per policy in month t.

    Quoted on the **initial** face amount [S1][S2].  This is the schedule; the amount
    actually collected is :func:`surr_charge`, which is capped by the account value.
    """
    return surr_charge_rate(t) * units()


def csv_pp(t):
    """``AV_{t+1} - SC_t``: the end-of-month cash value before debt, floored at zero.

    The chassis name for this intermediate.  The floor is a standardization **[std]** --
    a negative cash value would be a payment *from* the policyholder -- and it binds in
    the early policy years, where the scheduled surrender charge exceeds the account
    value, so the charge actually collected is the whole account value.  The notes'
    own ``CSV_t^EOM`` is net of debt: that is :func:`ncsv_pp`.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """CSV_t^EOM: the cash surrender value at the end of month t, floored at zero [S1].

    ``AV_{t+1} - SC_t - D_{t+1}`` in the notes' subscripts -- the end-of-month
    balances of month ``t``, which is why the surrender charge, a within-month
    schedule, keeps the plain ``t``.  What a surrendering policyholder is paid, and
    the notes' surrender outgo.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """sc_income: surrender charges collected from the policies lapsing in month t.

    ``(AV_{t+1} - csv_pp(t)) x pols_lapse(t)``, so it is capped by the account value where
    the :func:`csv_pp` floor binds.  Insurer income, and part of
    :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def is_default(t):
    """The notes' default test on end-of-month balances, ``AV_{t+1} - SC_t - D_{t+1} <= 0``.

    The notes' ``CSV_t^EOM`` [S1] -- :func:`ncsv_pp` before its zero floor -- at or below
    zero: the contractual trigger for grace, and the same test as the excess-debt
    default (debt at or above fund less surrender charge) [S1].  It is a
    **diagnostic only**:
    the notes lapse a defaulted policy "at the next monthiversary if not cured" without
    defining the cure test, the in-grace deduction accrual or the death benefit during
    grace, so the grace cascade is not implemented and no policy is terminated for
    insufficiency here.

    Read literally the test is true from **issue** on any front-loaded design: in
    policy year 1 the scheduled $18 per $1,000 surrender charge is far larger than the
    account value a first premium buys, so ``AV - SC`` is negative on a perfectly
    healthy new policy.  That is what model point 3 shows.  The test is reported as the
    notes write it, and :func:`is_shortfall` is the companion diagnostic that answers
    the question the default rule is really asking.  False outside cover.
    """
    if not is_active(t):
        return False
    return av_pp(t) - surr_charge_pp(t) - loan_bal_pp(t) <= 0


def is_shortfall(t):
    """The deduction-shortfall test: the unloaned accounts cannot pay ``MD_t``.

    ``unloaned_av_pp_at(t, BEF_FEE) < mth_deduction_pp(t)``.  The fixed-UL chassis
    makes this its grace trigger, and it is the point at which the account genuinely
    stops being able to carry the contract, as opposed to the notes' literal
    surrender-charge test in :func:`is_default`.  A diagnostic; nothing terminates.
    """
    return unloaned_av_pp_at(t, BEF_FEE) < mth_deduction_pp(t)


def first_default_month():
    """The first month ``t`` from the valuation date in which :func:`is_default` is true.

    -1 if never; -1 lies outside the frame, so "never" cannot be mistaken for a month.
    On a front-loaded point issued at or after the valuation date this is its issue
    month, :func:`t_entry`; see :func:`is_default`.  The month is on the valuation clock:
    on a point ``VUL_US_S`` restates in force at its month ``d``, it is the first month at
    or after ``d`` in which ``VUL_US_S`` finds the test true, less ``d``, which is 0 where
    the test already holds at ``d``.
    """
    for t in range(proj_len()):
        if is_default(t):
            return t
    return -1


def first_shortfall_month():
    """The first month ``t`` from the valuation date in which :func:`is_shortfall` is true.

    -1 if never; -1 lies outside the frame, so "never" cannot be mistaken for a month.
    The month past which the projection is arithmetic rather than a description of a
    live contract: the notes' default rule would have terminated the policy at the
    following monthiversary, and that cascade is not implemented.  A level-premium cell
    whose cost of insurance eventually outruns its premium reaches this point at some
    late duration; run it to see where.  The month is on the valuation clock, as
    :func:`first_default_month`'s is: point 7, ``VUL_US_S``'s point 3 restated in the
    month its shortfall begins, is in shortfall from ``t = 0``.
    """
    for t in range(proj_len()):
        if is_shortfall(t):
            return t
    return -1


def class_factor():
    """The underwriting-class multiplier on the base mortality table **[std]**.

    The ``factor`` *class_factor_table.csv* gives this point's ``rate_class``, from
    ``Data.class_factor``, which joins it to the points once it has checked the table's
    classes and factors, so that a blank factor never reaches :func:`mort_rate` as a
    missing value, and refuses, as the table is first read, a point whose class the table
    lacks, where ``VUL_US_S`` failed that point at its first read.
    """
    return float(data.class_factor()[idx])                           # noqa: F821


def mort_rate(t):
    """q^d,annual: the annual best-estimate mortality rate in month t, capped at 1.

    Base table times :func:`class_factor` times the A/E factor, 100% in the base run
    **[std]** with no mortality improvement.  The shipped table is a small illustrative
    one **[std]**, *not* the 2015 VBT calibrated to ILEC experience the notes recommend
    [REG-R18][REG-R19] -- that family is licensed and may not be reproduced here.  Ages
    beyond the table take its last row, where the rate is 1.0.  The base rate is read at
    the attained age of month t by :func:`mort_rate_base_at`.

    This is the **death decrement**, best-estimate experience.  It is not
    :func:`coi_rate`, the current COI scale, which is a revenue item.  Conflating them
    is the first entry on the notes' list of modeling pitfalls, and the two tables
    shipped here are deliberately different.

    The product is capped at 1, written ``min(q, 1.0)``, as ``VUL_US_S`` writes it: a
    class factor above 1 -- 1.50 and 1.75 for the two tobacco classes -- carries the
    oldest ages' rates past 1, where the monthly rate ``1 - (1 - q)^(1/12)`` has no real
    value; at the shipped A/E a StdTob point's product first passes 1 at attained age 113
    and a PTob point's at 114.  With the bound second a missing input, a NaN, stays NaN,
    where ``min(1.0, q)`` would read it as 1, certain death with every flow finite;
    ``Data`` refuses a blank base rate or class factor as it reads the tables, before any
    rate is read, and a base rate outside 0 to 1 or a class factor below 0.  No shipped
    point's product passes 1.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    q = mort_rate_base_at(age(t)) * class_factor() * mort_ae_factor  # noqa: F821
    return min(q, 1.0)


def mort_rate_base_at(a):
    """The base table's annual mortality rate at attained age a: the table's one reader.

    From *mort_table.csv*, before the class factor and the A/E factor:
    ``Data.mort_table_array()`` at the age, the table padded from age 0, so that the age
    is the index.  Ages outside the table take its nearest row, which above it is the
    rate of 1.0 at age 121 and below it, at issue ages under 18, the rate at 18: the
    first and last ages ``data.mort_age_first()`` and ``data.mort_age_last()`` give,
    which they read from the table's key column once the keys and the rates are checked,
    before any rate is read, the last first, as :func:`corridor_factor_at` asks, and which
    keep the read off the padding.  Keyed by the attained age, so the table is read once
    an age rather than once a month; :func:`mort_rate` calls it inside cover only.
    """
    last = data.mort_age_last()                                      # noqa: F821
    a = min(max(a, data.mort_age_first()), last)                     # noqa: F821
    return float(data.mort_table_array()[a])                         # noqa: F821


def mort_rate_mth(t):
    """q^d_t: the monthly mortality rate, ``1 - (1 - q^d,annual)^(1/12)`` **[std]**."""
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """q^w,base: the base annual lapse rate by policy year **[std]**.

    6% in year 1, 5% in year 2, 4% in years 3-10, 3% thereafter, read from
    *lapse_table.csv* at the policy year of month t by :func:`lapse_rate_base_py`.  The
    levels come from the LIMRA/SOA UL persistency and lapse studies [REG-R20][REG-R21]
    applied to VUL **by analogy** -- VUL is not broken out separately in them, which the
    notes flag -- and the detailed tables are behind a paid package, so the numbers are a
    standardization.  Zero outside cover, before the table is read.
    """
    return lapse_rate_base_py(policy_year(t)) if is_active(t) else 0.0


def lapse_rate_base_py(y):
    """q^w,base in policy year y, from *lapse_table.csv*: the table's one reader.

    ``Data.lapse_rate_array()`` at the year, read as :func:`prem_persistency_py` reads its
    own table: policy years beyond the table take its last row, the last year
    ``data.lapse_last_year()`` gives once it has checked the keys and the rates, and a
    year below 1 is refused, naming the point and the year.  Keyed by the contractual
    policy year, so the table is read once a policy year rather than once a month;
    :func:`lapse_rate_base` calls it inside cover only.
    """
    last = data.lapse_last_year()                                    # noqa: F821
    if y < 1:
        raise ValueError(f"point_id {point_id()}: lapse_table.csv has no rate for policy "
                         f"year {y}")
    return float(data.lapse_rate_array()[min(y, last)])              # noqa: F821


def lapse_shock_month():
    """The policy month of the surrender-charge cliff, counted from issue, 0-based.

    ``12 x runoff_years``: the first month in which the surrender charge is zero -- the
    first month of policy year ``runoff_years + 1`` -- which for the shipped
    fourteen-year schedule is policy month 168 from issue, i.e. ``duration_mth(t) ==
    168``.  Derived from the schedule's :func:`surr_charge_runoff_years`, whose ``int()``
    it takes as ``VUL_US_S`` does, rather than hard-coded, so a different schedule moves
    the cliff with it.  -1 when the model point carries no surrender charge, which no
    policy month in cover can equal.
    """
    if not has_surr_charge():
        return -1
    return 12 * int(surr_charge_runoff_years())


def lapse_rate_sc_mult(t):
    """The surrender-charge cliff spike multiplier **[std]**.

    Applied in the policy month :func:`lapse_shock_month` gives, and only there -- the
    notes make it a *one-month* spike "in the month after SC_t reaches zero", not a whole
    shock year as on the fixed-UL chassis.  The notes call the spike optional and its
    magnitude an input, so ``lapse_shock_mult`` ships at 1.0, i.e. off; set it to 2.0 to
    switch it on.  1.0 outside cover, before the policy month is compared: a run-off of
    ``n`` years puts the spike at policy month ``12 n``, which can be the month after the
    frame.
    """
    if not is_active(t):
        return 1.0
    if not has_surr_charge():
        return 1.0
    if duration_mth(t) == lapse_shock_month():
        return lapse_shock_mult                                      # noqa: F821
    return 1.0


def lapse_rate_dyn_mult(t):
    """lambda_t: the dynamic lapse multiplier **[std]**.

    ``min(2.0, max(0.5, 1 + beta (1 - phi_t)))`` with ``beta = 0.5``: a performance
    shortfall raises the premium needed to sustain coverage and pushes marginal
    policyholders to lapse, while overfunded policies are stickier.  The bounds stop
    extreme extrapolation.  No public VUL dynamic-behavior study was retrieved, so the
    form is standardized with the notes' rationale.

    **1.0 when the behavior module is off**, which is the default -- see
    :func:`prem_persistency`.
    """
    if not dyn_behavior_on:                                          # noqa: F821
        return 1.0
    raw = 1 + lapse_dyn_beta * (1 - funding_ratio(t))                # noqa: F821
    return min(lapse_dyn_cap, max(lapse_dyn_floor, raw))             # noqa: F821


def lapse_rate(t):
    """q^w,annual: the total annual lapse rate **[std]**.

    ``q^w,base x cliff spike x lambda_t``.  The notes set no cap on the product, unlike
    the fixed-UL chassis's 35% **[std]** cap, and none is imposed: the dynamic
    multiplier is already bounded at 2.0.  ``Data`` holds each base rate to 0 to 1, and
    the spike and the multiplier's bound are References, ``lapse_shock_mult`` and
    ``lapse_dyn_cap``.  With both at 0 or more, the annual lapse rate is at most
    ``max(1, lapse_shock_mult)`` x (``lapse_dyn_cap`` with the behavior module on, 1 with
    it off) x the largest base rate, since the spike is 1 outside its month and the
    multiplier 1 with the module off.  It stays at most 1 while that product is at most 1:
    0.06 as shipped, 0.12 with the module on, 0.36 under the tests' splice.  Past 1 the
    monthly rate, ``1 - (1 - q)^(1/12)``, has no real value: the count turns complex, here
    as in ``VUL_US_S``, and the three checks raise, as ``VUL_US_S``'s do.
    """
    return lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_rate_dyn_mult(t)


def lapse_rate_mth(t):
    """q^w_t: the monthly lapse rate, ``1 - (1 - q^w,annual)^(1/12)`` **[std]**."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """l_t: the number of policies in force at the beginning of month t, row t's weight.

    ``pols_if_at(t, BEF_DECR)``, the notes' ``l_t``: the count carried in from month
    t - 1 plus month t's new business, before month t's decrements.  Decrements are
    end-of-month events, so the number in force is constant through the month and every
    BOM cash flow is weighted by it.  On a point issued at ``t = 0`` it is exactly
    ``VUL_US_S``'s ``pols_if``, the notes' ``l_{t+1} = l_t (1 - q^d_t)(1 - q^w_t)``
    rolled forward from the issued count.  A point in force at the valuation date opens
    with :func:`pols_if_init`, and one issued at or after it with its issued count in the
    issue month.  Zero before issue.  At ``t = proj_len()``, the month after the frame, it
    is the survivors of the last month, which the roll-forwards read.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity.
    """
    return pols_if_at(t, BEF_DECR)


def pols_if_at(t, timing):
    """Number of policies in force at a point of month t, by ``timing``.

    The three timings ``VUL_US_S``'s cell names:

    ``BEF_NB``
        The count carried in from month t - 1, before month t's new business: the
        survivors of month t - 1's deaths and lapses, out of month t - 1's
        ``BEF_DECR`` count.  In the first month on the books, :func:`t_entry`, it is
        :func:`pols_if_init`, the count in force at the valuation date (0 for a point
        issued at or after it), and the recursion reads no earlier month.  It is also
        defined in the month after the frame, ``t = proj_len()``, where it is the
        survivors of the last month: the projection ends where the mortality table ends,
        not where the contract does, so they are kept rather than matured.  Zero before
        issue.
    ``BEF_DECR``
        ``l_t``: ``BEF_NB`` plus :func:`pols_new_biz`, before any decrement; the same
        number as :func:`pols_if`, and the weight on that month's cash flows.
    ``BEF_MAT``
        Before any maturity: ``VUL_US_S``'s meaning, the ``BEF_DECR`` count, which its
        cell gives for this timing.  The contract has no maturity date, so nothing
        matures and no event of the month separates the two.  ``basiclife.BasicTerm_SE``'s
        ``BEF_MAT``, the count at the start of the month before its new business, is
        not adopted, as it is not in ``UL_US_SEC``: the name keeps its S model's meaning.

    ``BEF_NB`` forms the count left at the end of month t - 1 itself -- month t - 1's
    ``BEF_NB`` count plus its :func:`pols_new_biz`, less its deaths and lapses, the
    products :func:`pols_death` and :func:`pols_lapse` take, in the order they take
    them -- rather than calling for it.  So the chain of calls back to :func:`t_entry`
    is one cell a month, as ``VUL_US_S``'s :func:`pols_if` chain was: a compiled model
    runs that chain on the C stack.  ``VUL_US_S``'s cell returns :func:`pols_if` for
    every timing, which in the issue month counts the issued policies under all three;
    here ``BEF_NB`` alone counts them as new business, not yet in.  Any other timing
    raises.
    """
    if timing == BEF_NB:
        if not 0 <= duration_mth(t) <= omega_mth():
            return 0.0
        if t == t_entry():
            return pols_if_init()
        prev = pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1)
        q = mort_rate_mth(t - 1)
        return prev - prev * q - prev * (1 - q) * lapse_rate_mth(t - 1)
    elif timing == BEF_DECR:
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)
    elif timing == BEF_MAT:
        return pols_if_at(t, BEF_DECR)
    else:
        raise ValueError("invalid timing")


def pols_new_biz(t):
    """Number of policies issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point
    issued at the valuation date, ``t = k`` for one issued ``k`` months later.  A point
    already in force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_death(t):
    """Number of deaths at the end of month t, ``l_t x q^d_t``.

    Zero outside cover, before any rate is read.
    """
    return pols_if(t) * mort_rate_mth(t) if is_active(t) else 0.0


def pols_lapse(t):
    """Number of surrenders at the end of month t.

    ``l_t x (1 - q^d_t) x q^w_t``: death is applied before lapse **[std order]**,
    matching the notes' ``l_{t+1} = l_t (1 - q^d_t)(1 - q^w_t)``.  Zero outside cover,
    before any rate is read.
    """
    if not is_active(t):
        return 0.0
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    Variable universal life has no maturity date -- at attained age 121 premiums and
    monthly deductions cease, the asset charges continue, and coverage runs to death or
    surrender [S1][S2][S4].  The cell is kept so the in-force roll-forward identity
    has the same shape as in the term and annuity models of this library, where it is
    not zero.  The survivors of the frame's last month do not mature either: the
    projection stops there because the mortality table does, and they are carried into
    ``t = proj_len()`` (:func:`pols_if_at`).
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``DEATH``
        ``DB_t^EOM - D_t``: the **full death benefit** less outstanding policy debt
        [S1][S3].  Not ``DB - AV``.  The notes carry an explicit warning here: the
        insurer's liability outflow is the whole death benefit, and seizing the account
        value is the *funding* of part of it.  ``DB - AV`` is the net
        general-account strain, reported separately as :func:`claims_net`.

    ``LAPSE``
        ``ncsv_pp(t)``, the cash surrender value net of debt and the surrender charge.

    ``WITHDRAWAL``
        ``W(t)``.  The $25 fee is retained by the insurer and is not part of the
        payment.  A withdrawal is a payment on the owner's election rather than a
        claim, so it is *not* a claim cell's kind, of :func:`claims_death`,
        :func:`claims_lapse` or their total, :func:`claims`; this branch is the
        per-policy amount :func:`withdrawals` weights by :func:`pols_if`.

    Any other code raises, ``MATURITY`` among them, which only :func:`claims_from_av`
    takes, and so does a text, in modelx, since the codes are compared with ``==``.
    """
    if kind == DEATH:
        return db_pp_eom(t) - loan_bal_pp(t)
    elif kind == LAPSE:
        return ncsv_pp(t)
    elif kind == WITHDRAWAL:
        return wd_pp(t)
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim funded by releasing the account value, by ``kind``.

    Death and surrender both release the end-of-month account value ``AV_t``, because
    decrements follow the investment credit.  ``MATURITY`` is zero: the contract has
    no maturity date.
    """
    if kind == DEATH:
        return av_pp(t) * pols_death(t)
    elif kind == LAPSE:
        return av_pp(t) * pols_lapse(t)
    elif kind == MATURITY:
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    """Death claims in excess of the account value released.

    ``(claim_pp(t, DEATH) - AV_t) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin.  It differs from :func:`claims_net` by the
    debt extinguished on death, which the account release also covers.
    """
    return (claim_pp(t, DEATH) - av_pp(t)) * pols_death(t)


def claims(t):
    """Claim outgo in month t: death and surrender claims together -- the **gross view**.

    :func:`claims_death` and :func:`claims_lapse`, summed left to right from ``0.0``, the
    total :func:`net_cf` subtracts.  ``VUL_US_S``'s ``claims(t, kind=None)`` is both the
    kinds and their total, a generator summed by Python's ``sum``, which compiles to
    neither a C parameter nor a C loop; here the kinds are two cells, the ``result_cf``
    columns, and this is their total.  Python's ``sum`` of floats is compensated, but of
    two it is their sum, rounded once, which is what this computes, and its ``0.0``
    start keeps ``sum``'s, which turns two negative zeros to ``0.0``.  So the total is
    ``VUL_US_S``'s float in every month.  Death claims are weighted by
    :func:`pols_death` and surrenders by :func:`pols_lapse`, both end-of-month events.

    Partial withdrawals are **not** here, neither as a kind nor in the total: a
    withdrawal is a payment on the owner's election rather than an event that terminates
    coverage, and it is reported by :func:`withdrawals` in its own column, while
    ``WITHDRAWAL`` remains a valid ``kind`` of :func:`claim_pp`, which carries the
    per-policy amount.

    :func:`claims_death` is the notes' ``claim_gross``.  Projecting the net amount at
    risk there instead understates gross benefit outgo and breaks reconciliation with
    statutory exhibits; projecting the full death benefit there *and* separately
    expensing the net amount at risk double counts.  The general-account view is
    derived from the same run in :func:`result_net`.
    """
    return 0.0 + claims_death(t) + claims_lapse(t)


def claims_death(t):
    """claim_gross: death claims in month t, :func:`pols_death` at ``claim_pp(t, DEATH)``.

    The full death benefit less the debt, per policy, weighted by the deaths, an
    end-of-month event: ``VUL_US_S``'s ``claims(t, "DEATH")``, the ``claims_death``
    column of :func:`result_cf`, and the ``claim_gross`` column of :func:`result_net`.
    """
    return claim_pp(t, DEATH) * pols_death(t)                        # noqa: F821


def claims_lapse(t):
    """surr_outgo: surrender claims at the end of month t.

    :func:`pols_lapse` at the net cash surrender value per policy, ``claim_pp(t, LAPSE)``:
    ``VUL_US_S``'s ``claims(t, "LAPSE")``, the ``claims_lapse`` column of
    :func:`result_cf`, and the ``surr_outgo`` column of :func:`result_net`.
    """
    return claim_pp(t, LAPSE) * pols_lapse(t)                        # noqa: F821


def claims_net(t):
    """claim_net: the net general-account cost of the deaths in month t.

    ``l_t x q^d_t x NAAR_t^EOM`` -- the death benefit less the account value seized to
    fund it.  A **derived report**, not a cash flow: it belongs to the net-of-account
    view in :func:`result_net`, never to :func:`result_cf`.
    """
    return net_amt_at_risk_eom(t) * pols_death(t)


def withdrawals(t):
    """Partial withdrawal payments in month t, for the policies in force.

    ``claim_pp(t, WITHDRAWAL) x l_t`` -- the withdrawal is taken at the monthiversary
    by policies still in force, so it is weighted by :func:`pols_if` and not by a
    decrement.  Zero in every shipped model point, which is the notes' baseline.

    A payment on the owner's election, not a claim: it terminates nothing and it is
    reported in its own ``withdrawals`` column of :func:`result_cf`, outside
    :func:`claims_death`, :func:`claims_lapse` and their total, :func:`claims`.  The $25
    fee is retained by the insurer and is :func:`wd_fees`, not part of this payment.
    """
    return claim_pp(t, WITHDRAWAL) * pols_if(t)


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force.

    Account-value outgo but not a liability cash flow, so this appears in
    :func:`margin_expense` and not in :func:`claims`.
    """
    return wd_fee_pp(t) * pols_if(t)


def sa_transfer(t):
    """sa_transfer: separate-account value released to the general account (memo).

    On death the subaccount values move separate account to general account; on
    surrender the separate account liquidates to fund the cash surrender value.  The
    fixed option and the loan account release internally and are not part of this.  A
    memo column for reconciliation, not a liability cash flow.  The subaccounts are
    summed in a loop over the lineup's positions from 0.0, as :func:`av_pp` sums them.
    """
    sa = 0.0
    for i in range(subaccount_count()):
        sa = sa + sa_pp(t, i)
    return sa * (pols_death(t) + pols_lapse(t))


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(t // 12)``.

    ``inflation_rate`` is **0.0** here: the variable-UL notes specify a flat $75 per
    policy per year maintenance expense **[std]** with no inflation, where the fixed-UL
    chassis inflates its own at 2.5%.  The cell is kept so the two models read alike
    and so an inflation assumption can be switched on with one Reference.  Switched on,
    expenses inflate by year, on the **valuation** clock: the years are counted from the
    valuation date, ``t // 12``, so the expense is in valuation-date dollars whatever the
    policy's age, and every point of a block steps alike, on the valuation anniversaries.
    ``VUL_US_S`` steps on the policy year, ``(1 + inflation_rate)^(policy_year - 1)``; on
    a point issued at ``t = 0`` the two are the same.  Acquisition is not inflated (see
    :func:`expenses`).
    """
    return (1 + inflation_rate) ** (t // 12)                         # noqa: F821


def expenses(t):
    """The insurer's own expenses in month t **[std]**.

    ``(acq + expense_maint / 12 x inflation) x pols_if(t)``, ``VUL_US_S``'s formula in
    its order: the maintenance expense of $75 a year, inflating on the valuation clock
    (:func:`inflation_factor`, flat as shipped), and ``expense_acq`` in the issue month,
    ``duration_mth(t) == 0``, not inflated, both on the policies in force at the start of
    the month.  In the issue month those are the policies issued, :func:`pols_new_biz`,
    since a point issued at or after the valuation date opens with none, so acquisition
    is charged per policy issued, as in ``basiclife.BasicTerm_SE``, and a point in force
    at the valuation date never bears it, because it was issued before.  On a point
    issued at ``t = 0`` this is ``VUL_US_S``'s charge bit for bit.  The notes specify no
    acquisition expense for this product -- the premium load and the surrender charge
    are the contractual acquisition-cost recovery, which is income, not outgo -- so
    ``expense_acq`` is zero and the term is carried only so a user can switch it on.

    Zero outside cover, where the count carried into ``t = proj_len()`` would otherwise
    bear a maintenance expense.  Not to be confused with :func:`maint_fee`, which is the
    charge *against the account value*.  Internal expense assumptions are not public, so
    both figures are placeholders.
    """
    if not is_active(t):
        return 0.0
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    return (acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """The percent-of-premium collection expense, 2% of premium **[std]**.

    The chassis name; for this product the notes call it a premium collection expense
    rather than a premium tax, but it is the same percent-of-premium line.
    """
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``premium loads + withdrawal fees + maint_fee + surrender charges - expenses
    - premium taxes``.  Follows ``CashValue_SE.margin_expense``.  The M&E charge is
    *not* in it -- it is an asset-based charge on separate-account assets, reported by
    :func:`me_charge` and reconciled in :func:`check_net_view`.
    """
    return (premium_loads(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`.

    The gap between the cost of insurance *charged* on the current COI scale and the
    cost of the deaths that actually occur on best-estimate mortality -- the two bases
    the notes insist must never be conflated, meeting here and only here.
    """
    return coi(t) - claims_over_av(t)


def net_cf(t):
    """NetCF(t): net liability cash flow in month t, **undiscounted**.

    ``premiums - claims (death and surrender) - withdrawals - expenses - premium
    taxes``: the **gross (policyholder) view**, which the notes make the reference
    model's primary projection.  Withdrawals are a separate term because they are not
    claims -- :func:`claims` no longer carries them -- and dropping them here would
    lose an outgo the account value has already released.  Like the rest of this
    library the model
    projects gross liability cash flows: there is no discounting and no change in
    account value in this figure, because reserves are a separate layer that consumes
    these flows.  Investment credit on the account value is the policyholder's, not an
    insurer cash flow, so it does not appear either -- see :func:`check_margin` and
    :func:`check_net_view` for how it reconciles.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - premium_taxes(t))


def net_cf_ga(t):
    """The net-of-account (general-account strain) view of month t.

    ``load_income + md_income + me_income + loan_spread + sc_income - claim_net
    - expense``, the notes' reconciliation identity.  A **derived report** from the
    same run as :func:`net_cf`, not a second projection: :func:`check_net_view` shows
    the gross view reproduces it once the account pass-throughs are added back.
    """
    return (premium_loads(t) + mth_deduction(t) + me_charge(t)
            + loan_spread(t) + surr_charge(t)
            - claims_net(t) - expenses(t) - premium_taxes(t))


def check_av_roll_fwd():
    """Check the account value roll-forward.

    Returns ``True`` when, for every month of the frame, the opening account value in
    force of month ``t + 1`` equals::

        av_at(t, BEF_PREM)
            + prem_to_av(t)
            - withdrawals(t)
            - wd_fees(t)
            - mth_deduction(t)
            + inv_income(t)
            - claims_from_av(t, DEATH)
            - claims_from_av(t, LAPSE)

    to within ``1e-9``, relative to the larger of the two and 1, which is what
    ``VUL_US_S``'s ``math.isclose`` tests with both its tolerances at ``1e-9``.  This
    pins the notes' processing order: that the deduction comes out before growth, that
    growth applies to the post-deduction balance, that the M&E charge is inside the
    investment credit rather than a second deduction, and that the decrements come after
    the credit.  Each month's residual is :func:`check_av_roll_fwd_resid`, so a failure
    can be found by month; a residual that is not a number fails, and one that is not real
    raises, as ``VUL_US_S``'s check does.  In the last month
    the opening value of ``t + 1`` is the account value the survivors carry into
    ``t = proj_len()``.
    """
    for t in range(proj_len()):
        if not abs(check_av_roll_fwd_resid(t)) <= 1e-9:
            return False
    return True


def check_av_roll_fwd_resid(t):
    """The account value roll-forward's relative residual in month t; zero everywhere.

    The opening account value in force of month ``t + 1`` less the roll-forward of month
    t that :func:`check_av_roll_fwd` sets out, over the larger of the two in magnitude and
    1: one number a month, whose magnitude is within ``1e-9`` exactly where
    ``math.isclose`` with both tolerances at ``1e-9`` holds.  Returned as a ``float``, so
    that a value that is not real raises here, as ``VUL_US_S``'s ``math.isclose`` raises on
    it: a monthly rate built from an annual one past 1, ``1 - (1 - q)^(1/12)``, is complex,
    and so is every count after it, and a complex residual's magnitude would pass.  Zero
    outside cover, before ``t + 1`` is read, so that nothing reads a month past
    ``t = proj_len()``.
    """
    if not is_active(t):
        return 0.0
    av = (av_at(t, BEF_PREM)
          + prem_to_av(t)
          - withdrawals(t)
          - wd_fees(t)
          - mth_deduction(t)
          + inv_income(t)
          - claims_from_av(t, DEATH)
          - claims_from_av(t, LAPSE))
    nxt = av_at(t + 1, BEF_PREM)
    return float((nxt - av) / max(abs(nxt), abs(av), 1.0))


def check_margin():
    """Check the net cash flow against the expense and mortality margins.

    Returns ``True`` when, for every month of the frame::

        net_cf(t) == margin_expense(t) + margin_mortality(t)
                     + av_change(t) - inv_income(t)
                     + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)

    to within ``1e-9``, relative to the larger side and 1, as for
    :func:`check_av_roll_fwd`; each month's residual is :func:`check_margin_resid`, and a
    residual that is not a number fails.  The last three terms are what separates a
    *gross liability cash flow* model from ``CashValue_SE``, whose ``net_cf`` already nets
    the change in account value and the investment credit; the loan term is the debt a
    surrender recovers out of the cash value, which is the whole loan while the cash value
    covers it and the cash value once the loan exceeds it, where :func:`ncsv_pp` pays
    nothing.  ``VUL_US_S``'s identity takes the whole loan in every month, so it is off by
    ``(csv_pp(t) - loan_bal_pp(t)) x pols_lapse(t)`` once the loan exceeds the cash value,
    and its check fails on a projection that is right; on every shipped model point the
    cash value covers the loan, and the two checks agree.
    """
    for t in range(proj_len()):
        if not abs(check_margin_resid(t)) <= 1e-9:
            return False
    return True


def check_margin_resid(t):
    """The margin identity's relative residual in month t; zero everywhere.

    ``net_cf(t)`` less the margins, the change in account value, the investment credit
    and the loan a surrender recovers, that :func:`check_margin` sets out, over the larger
    of the two sides in magnitude and 1, as :func:`check_av_roll_fwd_resid` measures its
    own, and a ``float``, as it is.  Zero outside cover, before :func:`av_change` would read
    ``t + 1``.
    """
    if not is_active(t):
        return 0.0
    rhs = (margin_expense(t) + margin_mortality(t)
           + av_change(t) - inv_income(t)
           + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t))
    lhs = net_cf(t)
    return float((lhs - rhs) / max(abs(lhs), abs(rhs), 1.0))


def check_net_view():
    """Check the gross view against the net-of-account view.

    Returns ``True`` when, for every month of the frame::

        net_cf(t) == net_cf_ga(t)
                     + av_change(t) - inv_income(t) + wd_fees(t)
                     - me_charge(t) - loan_spread(t)
                     + loan_bal_pp(t) * pols_death(t)
                     + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)

    to within ``1e-9``, relative to the larger side and 1, as for
    :func:`check_av_roll_fwd`; each month's residual is :func:`check_net_view_resid`, and
    a residual that is not a number fails.  This is the notes' "the gross view must
    reproduce it after adding back the account pass-throughs".  Reading the correction
    terms: ``av_change - inv_income`` is the net premium in and the account releases out;
    ``- me_charge`` and ``- loan_spread`` remove the two margins the gross view never sees
    because they are collected inside the accounts; the debt terms are the policy debt
    extinguished against the account value, the whole debt on a death, whose claim is the
    death benefit less the debt with no floor, and on a surrender the debt the cash value
    recovers, as in :func:`check_margin`.  ``VUL_US_S`` adds back the whole debt on a
    surrender too, and its check fails once the loan exceeds the cash value.
    """
    for t in range(proj_len()):
        if not abs(check_net_view_resid(t)) <= 1e-9:
            return False
    return True


def check_net_view_resid(t):
    """The net view identity's relative residual in month t; zero everywhere.

    ``net_cf(t)`` less the net-of-account view and the pass-throughs that
    :func:`check_net_view` sets out, over the larger of the two sides in magnitude and 1,
    as :func:`check_av_roll_fwd_resid` measures its own, and a ``float``, as it is.  Zero
    outside cover, before :func:`av_change` would read ``t + 1``.
    """
    if not is_active(t):
        return 0.0
    rhs = (net_cf_ga(t)
           + av_change(t) - inv_income(t) + wd_fees(t)
           - me_charge(t) - loan_spread(t)
           + loan_bal_pp(t) * pols_death(t)
           + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t))
    lhs = net_cf(t)
    return float((lhs - rhs) / max(abs(lhs), abs(rhs), 1.0))


def result_cf():
    """Result table of the gross-view cash flows, indexed by month ``t``.

    One row per month ``t = 0, ..., proj_len() - 1`` from the valuation date, the same
    month for every model point, so the frames of a block line up and sum row by row,
    and a point issued after the valuation date has zeros until its issue month;
    ``len(result_cf()) == proj_len()``.  The columns are ``VUL_US_S``'s, each claim
    column a cell of its name, :func:`claims_death` and :func:`claims_lapse`.  The
    surrender column is ``claims_lapse``, matching the ``LAPSE`` kind that produces it,
    and partial withdrawals sit in their own ``withdrawals`` column rather than among the
    claims.  The cash flow columns net to ``net_cf`` under the library's income-positive
    sign; ``pols_if`` is a policy count, not a cash flow.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims_death(t) for t in ts],
            "claims_lapse": [claims_lapse(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, a DataFrame indexed by ``t``.

    One row per month ``t = 0 .. proj_len() - 1``, as in :func:`result_cf`.  First the
    counts :func:`result_cf` weights its rows by, and how they move, as
    ``basiclife.BasicTerm_SE``'s ``result_pols`` sets them out: ``pols_if``, the count of
    month t; ``pols_new_biz``, the part of it issued in month t; then month t's deaths and
    lapses, death first, and its maturities, which are always zero.  Row by row,
    ``pols_if`` at ``t + 1`` is ``pols_if`` less the three outflows of month t, plus the
    new business of month ``t + 1``.  Then ``VUL_US_S``'s two monthly decrement rates,
    which are 0 outside cover, where the model reads no rate.
    """
    ts = list(range(proj_len()))
    rows = []
    for t in ts:
        active = is_active(t)
        rows.append((pols_if(t), pols_new_biz(t), pols_death(t), pols_lapse(t),
                     pols_maturity(t),
                     mort_rate_mth(t) if active else 0.0,
                     lapse_rate_mth(t) if active else 0.0))
    return pd.DataFrame(                                             # noqa: F821
        rows,
        columns=["pols_if", "pols_new_biz", "pols_death", "pols_lapse",
                 "pols_maturity", "mort_rate_mth", "lapse_rate_mth"],
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the per-policy account value roll-forward.

    The columns follow the worked example in the technical notes: the two subaccount
    balances at the start of the month, the net premium, the post-premium account
    value, the death benefit and net amount at risk it is measured against, the cost of
    insurance and the monthly deduction, the post-deduction balance, the two
    end-of-month subaccount balances and the total, then the M&E collected, the
    surrender charge, the cash surrender value and the end-of-month death benefit and
    net amount at risk.  The index runs ``t = 0 .. proj_len() - 1``, as in
    :func:`result_cf`; on point 1 row ``t = 0`` is the worked example's month, and on a
    point issued later the rows before issue are zeros.
    """
    ts = list(range(proj_len()))
    n = subaccount_count()
    out = {}
    for i in range(n):
        out["sa{}_bef_prem".format(int(data.subaccounts()[i]))] = [  # noqa: F821
            sa_pp_at(t, i, BEF_PREM) for t in ts]                    # noqa: F821
    out["fa_bef_prem"] = [fa_pp_at(t, BEF_PREM) for t in ts]
    out["prem_to_av_pp"] = [prem_to_av_pp(t) for t in ts]
    out["av_pp_bef_fee"] = [av_pp_at(t, BEF_FEE) for t in ts]
    out["db_pp"] = [db_pp(t) for t in ts]
    out["net_amt_at_risk"] = [net_amt_at_risk(t) for t in ts]
    out["coi_pp"] = [coi_pp(t) for t in ts]
    out["mth_deduction_pp"] = [mth_deduction_pp(t) for t in ts]
    out["av_pp_bef_inv"] = [av_pp_at(t, BEF_INV) for t in ts]
    for i in range(n):
        out["sa{}_pp".format(int(data.subaccounts()[i]))] = [        # noqa: F821
            sa_pp(t, i) for t in ts]
    out["fa_pp"] = [fa_pp(t) for t in ts]
    out["av_pp"] = [av_pp(t) for t in ts]
    out["me_charge_pp"] = [me_charge_pp(t) for t in ts]
    out["surr_charge_pp"] = [surr_charge_pp(t) for t in ts]
    out["ncsv_pp"] = [ncsv_pp(t) for t in ts]
    out["loan_bal_pp"] = [loan_bal_pp(t) for t in ts]
    out["db_pp_eom"] = [db_pp_eom(t) for t in ts]
    out["net_amt_at_risk_eom"] = [net_amt_at_risk_eom(t) for t in ts]
    return pd.DataFrame(out, index=pd.Index(ts, name="t"))           # noqa: F821


def result_net():
    """Result table of the net-of-account (general-account strain) view.

    The notes' derived report: the margins the insurer collects, the net mortality
    cost, and the memo columns for reconciliation.  Column names are the notes' own.
    The index runs ``t = 0 .. proj_len() - 1``, as in :func:`result_cf`.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "prem_gross": [premiums(t) for t in ts],
            "load_income": [premium_loads(t) for t in ts],
            "md_income": [mth_deduction(t) for t in ts],
            "me_income": [me_charge(t) for t in ts],
            "loan_spread": [loan_spread(t) for t in ts],
            "claim_gross": [claims_death(t) for t in ts],
            "claim_net": [claims_net(t) for t in ts],
            "surr_outgo": [claims_lapse(t) for t in ts],
            "sc_income": [surr_charge(t) for t in ts],
            "expense": [expenses(t) + premium_taxes(t) for t in ts],
            "sa_transfer": [sa_transfer(t) for t in ts],
            "av_eop": [av_at(t, EOM) for t in ts],
            "naar": [net_amt_at_risk_eom(t) for t in ts],
            "pols_if": [pols_if(t) for t in ts],
            "net_cf_ga": [net_cf_ga(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

BEF_NB = 0

BEF_DECR = 1

BEF_MAT = 2

BEF_PREM = 3

BEF_WD = 4

BEF_FEE = 5

BEF_INV = 6

BEF_ME = 7

EOM = 8

DEATH = 0

LAPSE = 1

MATURITY = 2

WITHDRAWAL = 3

issue_age_min = 0

issue_age_max = 85

subaccount_max = 9

omega_age = 121

charges_cease_age = 121

expense_pol_mth = 10.0

expense_unit_mth = 0.2

me_rate_ann = 0.0045

coi_curr_factor = 0.5

coi_rate_cap = 83.34

guar_rate_ann = 0.01

crediting_rate_curr = 0.01

loan_rate_ann_std = 0.02

loan_rate_ann_pref = 0.0105

loan_cr_rate_ann_lvl = 0.01

loan_pref_year = 10

wd_fee = 25.0

mort_ae_factor = 1.0

lapse_shock_mult = 1.0

dyn_behavior_on = False

pricing_return_ann = 0.06

lapse_dyn_beta = 0.5

lapse_dyn_floor = 0.5

lapse_dyn_cap = 2.0

prem_pers_delta = 0.25

prem_pers_floor = 0.7

prem_pers_cap = 1.3

expense_acq = 0.0

expense_maint = 75.0

inflation_rate = 0.0

premium_tax_rate = 0.02

pd = ("Module", "pandas")
