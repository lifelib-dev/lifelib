# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.UL_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.UL_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is: ``Projection[5]``
is an ItemSpace projecting the table's sixth row, model point 6, ``UL_US_S``'s in-force
point restated six months on, in force 126 months at the valuation date with its loan,
and :func:`point_id` is its label::

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
(``products/universal_life/model-sec.md``, *What it refuses*).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.UL_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.UL_US_S` is rewritten where it depends on where the projection starts, where it
must answer for a month outside cover, or where it reads a table at a policy year or an
attained age; every other is :mod:`~.UL_US_S`'s own.
``products/universal_life/model-sec.md`` lists the rewritten cells with the reason for
each. Making it compile changed how each cell reads its inputs and spells its codes, and
no number: every model point attribute a projection cell uses is read as a number from a
``Data`` vector, every table as an array indexed by integers, every timing and kind is an
int code (*Codes*, below), :mod:`~.UL_US_S`'s ``coi_rate_scale``, a Series, is a schedule
number, :func:`coi_schedule`, and :mod:`~.UL_US_S`'s ``claims(t, kind=None)`` is two
cells and their total.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/universal_life/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``UL_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

The readers live in the unparameterized :mod:`~.UL_US_SEC.Data` Space, reached
here through the ``data`` Reference, so each file is read once per model rather than
once per model point. The seven assumption tables are the files :mod:`~.UL_US_S` reads,
read in place; the model point table is this model's own:

======================  ================================  ==========================
Reference (on Data)     Cells                             File
======================  ================================  ==========================
model_point_file        data.model_point_table()          model_point_table_sec.csv
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
later, at most ten years later. It is the notes' ``d(t)``, and everything contractual
reads it: the surrender charge run-off, the COI, per-unit and premium persistency scales
by policy year, the corridor factor and the mortality rate by attained age, the first
withdrawal year, and the GPT and 7-pay limits. The policy year is the 1-based contractual
label ``policy_year(t) = duration(t) + 1`` and the attained age (ANB) is
``age(t) = age_at_entry() + duration(t)``, both derived and never indexed by. Point 3,
``UL_US_S``'s in-force cell, is in policy year 11 at attained age 45 at ``t = 0``, and
point 9, to be issued 25 months after the valuation date, is issued at ``t = 25``.

``UL_US_S`` already counts its months from the start of its own projection rather than
from issue, and opens its in-force point 3 there with its account value and its loan.
What the valuation clock adds is that ``t = 0`` is one instant for every point, that a
point may be issued after it, and that a point in force brings in what its past has left
it: the face its withdrawals have left, the year's free allowance it has used, the
premiums it has paid and its MEC latch, four more opening values than ``UL_US_S`` reads.

The economic inputs read the valuation clock: the declared rates,
:func:`crediting_rate_ann` and :func:`comp_rate_ann`, flat as shipped, and expense
inflation, ``inflation_factor(t) = (1 + inflation_rate)^(t // 12)``, ``UL_US_S``'s step
by year moved onto ``t``, so that the maintenance expense is in valuation-date dollars for
every point alike. Acquisition is charged per policy issued, in the issue month, and is
not inflated, as in ``basiclife.BasicTerm_SE``.

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.UL_US_S` computes: every cell the two share agrees at every argument
:mod:`~.UL_US_S` evaluates in its sweep, but for three whose meaning changed,
``pols_if_init``, now the count already in force at the valuation date, ``model_point``,
a row of another table, and ``result_pols``, which gains the month's new business, and
``coi_rate_scale``, which this model replaces with :func:`coi_schedule`. S's ``claims(t,
kind)`` is :func:`claims_death` and :func:`claims_lapse` here, and its total,
``claims(t, None)``, is :func:`claims`. That
is how :mod:`~.UL_US_S`'s goldens on its new-business points carry over, the worked
example among them, and ``tests/test_model_conventions.py`` asserts it cell by cell. On
point 3 the projection is :mod:`~.UL_US_S`'s, month for month, its expenses apart, which
are in valuation-date dollars.

The **value** state variables are closing balances at the end of month ``t``:
``av_pp(t)``, ``loan_bal_pp(t)`` and ``cum_prem_pp(t)``. ``sum_assured_at(t)`` is not a
closing balance: it is the face amount in force **during** month ``t``, after that
month's BOM withdrawal reduction -- the face that ``db_pp(t)``, ``net_amt_at_risk(t)``
and ``units(t)`` are measured on. ``wd_used_year(t)`` is the free allowance used in the
policy year before month ``t``'s withdrawal, and ``is_mec(t)`` the 7-pay latch after
month ``t``'s test. The opening values -- the notes' ``AV(t-1)``, ``L(t-1)``,
``CumPrem(t-1)`` -- are ``av_pp_at(t, BEF_PREM)``, ``loan_bal_pp_bom(t)`` and
``cum_prem_pp(t - 1)``, and at :func:`t_entry`, the first month on the books, each chain
opens from the model point's opening state instead, so that nothing is ever asked for a
month before the valuation date or before issue. For a point in force the opening state
is six columns of its row, per policy, as the policy stands at the start of month 0,
before any month-0 event: the account value and the loan, ``UL_US_S``'s own columns
(:func:`av_pp_init`, :func:`loan_bal_init`); the face in force
(:func:`sum_assured_init`); the free withdrawal allowance already used in the policy year
under way (:func:`wd_used_year_init`); the premiums less withdrawals paid to date
(:func:`cum_prem_init`); and the MEC latch (:func:`is_mec_init`). ``UL_US_S`` takes the
last four as they stand at issue, the face at issue and nothing used, paid or failed, on
its in-force point too. For a point issued at or after the valuation date every one of
them is 0, and the issue values come from the formulas: :func:`sum_assured` for the face,
0 for the rest.

Every chain is one cell a month. ``av_pp_at(t, BEF_PREM)`` forms the previous month's
close itself, from its own value at ``t - 1`` and month ``t - 1``'s net premium,
withdrawal, fee, deduction and interest, the same sum in the same order as
``av_pp(t - 1)``, rather than calling for it, where ``UL_US_S``'s account value chain ran
through five cells a month; :func:`loan_bal_pp_bom` does the same for the loan, where
``UL_US_S``'s ran through two, and the ``BEF_NB`` timing of :func:`pols_if_at` for the
count, one cell a month as ``UL_US_S``'s :func:`pols_if` already was. The face, the year's
withdrawal usage and the cumulative premium call themselves at ``t - 1`` before anything
else, and the MEC latch does once its in-year test has run. A compiled model runs these
chains on the C stack.

Within each month the notes' monthiversary order is followed exactly:

1. amortize the surrender charge (:func:`surr_charge_rate`);
2. gross premium and its load, net premium to the account value
   (:func:`premium_pp`, :func:`prem_to_av_pp`);
3. withdrawal and withdrawal fee, and under Option A the face reduction they force
   (:func:`wd_pp`, :func:`wd_fee_pp`, :func:`sum_assured_at`) -- after which the
   account value is the notes' ``AV'(t)``, :func:`av_pp_at(t, BEF_FEE)<av_pp_at>`;
4. death benefit and the GPT corridor test (:func:`db_pp`);
5. net amount at risk, the death benefit discounted one month at the **guaranteed**
   rate less the account value measured **before** the deduction
   (:func:`net_amt_at_risk`);
6. the monthly deduction (:func:`mth_deduction_pp`);
7. the shortfall test (:func:`is_shortfall`);
8. end of month: one month's interest on the post-deduction balance
   (:func:`inv_income_pp`) and loan interest accrual (:func:`loan_bal_pp`);
9. end of month: decrements, death before lapse (:func:`pols_death`,
   :func:`pols_lapse`).

Cash flows are **undiscounted**. Premiums, expenses and premium taxes fall at BOM and
are weighted by ``pols_if(t)``; death claims by ``pols_if(t) * mort_rate_mth(t)``;
surrender payments by ``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``.
Partial withdrawals also fall at BOM and are weighted by ``pols_if(t)``, but they are
:func:`withdrawals`, a cash flow line of their own rather than a ``kind`` of
:func:`claim_pp`.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, BEF_DECR)``, the
count carried in from ``t - 1`` (``BEF_NB``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, and before issue
(:func:`is_active`) every count, and so every cash flow, is zero, and so is every value
state. ``UL_US_S`` already names three timings, in a cell that returns ``pols_if(t)`` for
each and that nothing calls. ``BEF_DECR`` keeps that meaning, and so does ``BEF_MAT``,
the count before any maturity, since nothing matures: the name keeps its S model's
meaning, as in the family's other models, and ``basiclife.BasicTerm_SE``'s start-of-month
``BEF_MAT`` is not adopted. ``BEF_NB`` is the one timing this model gives a new
meaning, ``basiclife.BasicTerm_SE``'s, and it differs from ``UL_US_S``'s only in the issue
month, where it counts the issued policies as new business, not yet in. Inside the month
the decrements are :mod:`~.UL_US_S`'s, death before lapse.

.. rubric:: The end of the projection

The frame ends at :func:`omega_mth`, where the mortality table ends, and not at an event
of the contract, which never matures. With the shipped table -- an annual rate of 1.0 at
ages 119 and 120 -- and a class factor and an A/E of 1 or more, every life has died by
the end of the first month at attained age 119. With a preferred class, an A/E below 1,
or a table that stays below 1, lives survive the last month, and the roll-forwards read
them: :func:`check_av_roll_fwd` and :func:`av_change` read the opening account value in
force of month ``t + 1``, which in the last month is ``t = proj_len()``. So the two
opening values they read there, the count (the ``BEF_NB`` timing of
:func:`pols_if_at`, and through it :func:`pols_if`) and the account value
(``av_pp_at(t, BEF_PREM)``), are defined for ``0 <= duration_mth(t) <= omega_mth()``:
on the books, and in the month after the frame, where they are the survivors of the last
month and the account value they carry. Both equal :mod:`~.UL_US_S`'s values there
exactly. Every other cell is zero or false there, as before issue: the account value
inside the month, the loan, every charge, premium, withdrawal, decrement rate, decrement,
claim and flow, and the expenses, whose maintenance would otherwise fall on the carried
count; only the two clocks, the inputs read on the valuation clock and the lapse shock's
neutral 1.0 hold values there.
And nothing reads past ``t = proj_len()``: :func:`av_change` and the two checks' residual
cells, which read ``t + 1``, are zero outside cover before they read it.

.. rubric:: Naming

Cell names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue -- ``pols_*`` for policy counts, ``av_*`` for
account values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for
per-policy amounts, ``timing`` and ``kind`` arguments. What running in force adds
is named as ``basiclife.BasicTerm_SE`` names it: ``duration_mth`` read from the model
point, ``policy_count``, ``pols_new_biz``, ``pols_if_at`` with its ``BEF_NB`` timing,
``is_active`` and ``result_pols``. ``t_entry``, the first month on the books, is the SEC
models' own, and ``omega_mth`` this model's, named for ``omega_age``, where the
projection ends, since the contract has no end of its own. A column of the opening state
is the cell it opens with ``_init`` added, in ``UL_US_S``'s spelling of the stem:
``av_pp_init`` and ``loan_bal_init`` are ``UL_US_S``'s own, ``sum_assured_init``,
``wd_used_year_init`` and ``is_mec_init`` are new, and ``cum_prem_init`` is
``ULSG_US_S``'s name for the same column. ``wd_used_year`` already says it restarts each
policy year, so its column takes no ``_ytd``. A table read at a policy year has one
reader keyed by the year, ``<cell>_py(y)``, and a table read at an attained age one keyed
by the age, ``<cell>_at(a)``; the monthly cell keeps ``UL_US_S``'s name and calls it
inside cover. The surrender-charge schedule, keyed by its ID, has one reader for each of
its two columns, :func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`, and
the COI scale, keyed by sex, class and issue age, is numbered, :func:`coi_schedule`. A
check's residual in month t is ``<check>_resid(t)``. A text column a monthly cell
branches on is read through bool decodes, one for each value it branches on, named for
the value:
:func:`is_db_option_a` and :func:`is_db_option_b`, :func:`is_gpt`, and
:func:`is_level_premium`, :func:`is_single_premium` and :func:`is_target_premium`. No
projection cell reads text: ``Data`` decodes each column into its flags, and joins the
class factor, the COI scale and the surrender-charge schedule to the points by their text
keys, so ``UL_US_S``'s label accessors are kept for reporting alone (*Reporting cells*,
below). Each of ``UL_US_S``'s claim kinds is a cell, ``claims_<kind>(t)``, and
:func:`claims` their total, as in the family's other compiled models.

The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Months from the valuation date
d(t)                       duration_mth(t)                 Completed policy months at
                                                           month t, the notes' month index
y                          policy_year(t)                  Policy year, d(t) // 12 + 1
(y - 1)                    duration(t)                     Completed policy years
(none)                     point_id                        The row's label, at idx
x / issue_age              age_at_entry                    Issue age (ANB)
x + y - 1                  age(t)                          Attained age (ANB)
proj_len                   proj_len                        Months from the valuation date
                                                           to the end of the projection
(table's last age)         omega_age                       Last age of the table, 120
(projection end)           omega_mth                       Policy month the projection
                                                           ends at, attained age 121
(none)                     t_entry                         First month on the books
(none)                     is_active(t)                    Whether month t is in cover
sex                        sex                             Sex, M or F
risk_class                 rate_class                      Underwriting class, one of six
F / face_amount            sum_assured                     Initial total face amount
F(t)                       sum_assured_at(t)               Total face after reductions
(opening F)                sum_assured_init                Face in force entering month 0
U                          units(t)                        Face in $1,000 units
db_option                  db_option                       Death benefit option, A or B
(Option A)                 is_db_option_a                  Whether db_option is A
(Option B)                 is_db_option_b                  Whether db_option is B
qual_test                  qual_test                       7702 test elected; GPT only
(GPT elected)              is_gpt                          Whether qual_test is GPT
premium_pattern            premium_type                    LEVEL / SINGLE / TARGET
(LEVEL pattern)            is_level_premium                Whether premium_type is LEVEL
(SINGLE pattern)           is_single_premium               Whether it is SINGLE
(TARGET pattern)           is_target_premium               Whether it is TARGET
premium_mode               (not modelled)                  Monthly premiums only **[std]**
planned_premium_annual     premium_pp_ann                  Planned annual premium
av_initial                 av_pp_init                      Account value entering month 0
loan_balance_initial       loan_bal_init                   Loan balance entering month 0
policy_month_offset        duration_mth_init               Completed policy months at the
                                                           valuation date; -k if issued k
                                                           months later
(none)                     policy_count                    Policies the model point
                                                           stands for
sc_layer_table             surr_charge_id                  Surrender charge schedule ID
(schedule applies)         has_surr_charge                 Whether a schedule applies
(initial SC per $1,000)    surr_charge_rate_max            The schedule's charge before
                                                           any run-off
(run-off period)           surr_charge_runoff_years        The schedule's run-off, years
guideline_single_premium   gsp                             GSP in the GPT limit
guideline_level_premium    glp                             GLP in the GPT limit
seven_pay_premium          seven_pay_prem                  7-pay premium, an input
GP(t)                      premium_pp(t)                   Gross premium per policy
pp(y)                      prem_persistency(t)             Paid/planned factor
(pp by year)               prem_persistency_py(y)          The same, keyed by policy year
pl                         load_prem_rate                  Current premium load rate
NP(t)                      prem_to_av_pp(t)                Net premium to account value
W(t)                       wd_pp(t)                        Partial withdrawal
(planned W)                wd_pp_mth                       The wd_pp column, a month's W
wf                         wd_fee_pp(t)                    Withdrawal fee ($25)
(free amount)              wd_free_pp(t)                   Free allowance still available
wd_used_year               wd_used_year(t)                 Free allowance used this year
(opening usage)            wd_used_year_init               The usage entering month 0
(face cut)                 face_reduction_pp(t)            Option A face reduction
AV(t)                      av_pp(t)                        Account value, end of month
AV(t-1)                    av_pp_at(t, BEF_PREM)           Account value, start of month
(after premium)            av_pp_at(t, BEF_WD)             Before the withdrawal
AV'(t)                     av_pp_at(t, BEF_FEE)            After premium and withdrawal
(AV'(t) floored at 0)      av_pp_db_basis(t)               The AV' that DB and NAAR use
AV'(t) - MD(t)             av_pp_at(t, BEF_INV)            After the monthly deduction
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
e_pol                      expense_pol_mth                 Per-policy charge
e_unit(y)                  expense_unit_mth_1/_2           Per-unit charge
rc(t)                      rider_charge_pp(t)              Rider charges (0)
(e_pol + e_unit U + rc)    maint_fee_pp(t)                 Non-COI monthly charges
MD(t)                      mth_deduction_pp(t)             Monthly deduction
(the point's scale)        coi_schedule                    Its row of the COI table
q_coi_guar(s)              coi_rate_guar(t)                Guaranteed maximum COI rate
(q_coi_guar by year)       coi_rate_guar_py(y)             The same, keyed by policy year
(last year of the scale)   coi_rate_last_year              The scale's last policy year
q_coi(s)                   coi_rate(t)                     Current COI rate
(COI charge)               coi_pp(t)                       Cost of insurance charge
NAAR(t)                    net_amt_at_risk(t)              Net amount at risk
DB(t)                      db_pp(t)                        Death benefit after corridor
cf(a)                      corridor_factor(t)              GPT corridor factor
(cf by age)                corridor_factor_at(a)           The same, keyed by age
(NAAR factor)              naar_factor                     1 + i_gm
i_guar                     guar_rate_ann                   Guaranteed annual rate
i_cr                       crediting_rate_ann(t)           Current credited annual rate
i_m                        inv_return_mth(t)               Monthly credited rate
i_gm                       guar_rate_mth                   Monthly guaranteed rate
(interest credited)        inv_income_pp(t)                Interest credited to AV
earned_rate(t)             (not modelled)                  NGE revision input, no source
L(t)                       loan_bal_pp(t)                  Loan balance, end of month
L(t-1)                     loan_bal_pp_bom(t)              Loan balance, start of month
r_L                        loan_rate_ann                   Charged loan rate
SC(t)                      surr_charge_pp(t)               Surrender charge
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
CSV(t)                     csv_pp(t)                       Cash surrender value
NCSV(t)                    ncsv_pp(t)                      Net cash surrender value
(SC retained)              surr_charge(t)                  Surrender charge collected
CumPrem(t)                 cum_prem_pp(t)                  Cumulative premiums
(opening CumPrem)          cum_prem_init                   Premiums less withdrawals
                                                           before the valuation date
(GPT limit)                gpt_limit(t)                    max(GSP, GLP x years)
(GPT test)                 gpt_ok(t)                       GPT compliance flag
(7-pay limit)              seven_pay_limit(t)              7-pay cumulative limit
(MEC flag)                 is_mec(t)                       7-pay failure flag, latched
(opening MEC flag)         is_mec_init                     The latch entering month 0
(grace trigger)            is_shortfall(t)                 AV' - L < MD
grace_flag(t)              (not modelled)                  In-grace state; see below
(cure payment)             cure_premium_pp(t)              3 x MD plus load
q_m(t)                     mort_rate_mth(t)                Monthly mortality rate
(annual q)                 mort_rate(t)                    Annual mortality rate, capped
(base q by age)            mort_rate_base_at(a)            The base table's rate
w_base(y)                  lapse_rate_base(t)              Base annual lapse rate
(w_base by year)           lapse_rate_base_py(y)           The same, keyed by policy year
M_sc                       lapse_rate_sc_mult(t)           SC-expiry lapse shock
(shock year)               lapse_shock_year                Policy year of the shock
M_rate(t)                  lapse_rate_dyn_mult(t)          Dynamic lapse multiplier
r_comp(t)                  comp_rate_ann(t)                Competitor new-money rate
w_annual(y,t)              lapse_rate(t)                   Total annual lapse rate
w_m(t)                     lapse_rate_mth(t)               Monthly lapse rate
l(t)                       pols_if(t)                      In force at start of month t
l(0)                       pols_if_init                    In force at the valuation date
(none)                     pols_if_at(t, BEF_NB)           Carried in from month t - 1
(none)                     pols_if_at(t, BEF_DECR)         After new business: l(t)
(none)                     pols_if_at(t, BEF_MAT)          Before maturity: l(t)
(none)                     pols_new_biz(t)                 Policies issued in month t
(deaths)                   pols_death(t)                   Deaths in month t
(lapses)                   pols_lapse(t)                   Lapses in month t
(none)                     pols_maturity(t)                Maturities: always zero
(premium income)           premiums(t)                     Premium income
(death claims)             claims_death(t)                 Death claims
(surrender outgo)          claims_lapse(t)                 Surrender payments
(claims)                   claims(t)                       Death and surrender claims
(withdrawal outgo)         withdrawals(t)                  Withdrawal payments
(maintenance)              expenses(t)                     Maintenance expenses
(percent of premium)       premium_taxes(t)                Premium tax / %-of-premium
NetCF(t)                   net_cf(t)                       Net liability cash flow
(none)                     check_av_roll_fwd_resid(t)      AV roll-forward residual
(none)                     check_margin_resid(t)           Margin identity residual
(none)                     result_pols()                   Counts and decrement rates
=========================  ==============================  ==========================

The table covers every symbol the notes define: the Model point attributes table, the
State variables table and the notation list, in that order, followed by the cash flow
rows; the cells running in force adds sit beside the symbols they open, key or count.
Three symbols have **no cells at all**, and are carried in the table as ``(not
modelled)`` so that the absence is recorded rather than silent: ``grace_flag(t)``, the
one of the notes' ten state variables with no counterpart here, because the grace
cascade is a diagnostic and no in-grace state is held (:func:`is_shortfall`);
``premium_mode``, because every premium in this model is monthly **[std]**; and
``earned_rate(t)``, the input the notes' optional NGE revision rule would need
(:func:`crediting_rate_ann`).

Eight names needed care.

The notes' ``risk_class`` is :func:`rate_class` here, and the model point table column
is ``rate_class`` too. The name is taken from ``Term_US_S``/``BasicTerm_S``, which
this library follows ahead of the notes wherever the two collide; ``rate_class`` also
avoids reading as Python's ``class``. The six classes themselves are the product
spec's, unchanged.

``l(t)`` in the notes is the in-force probability at the **start** of month ``t``, before
that month's decrements, with ``l(0) = 1``; ``pols_if(t)`` is the same quantity under
``BasicTerm_S``'s name, after the month's new business, so ``pols_if(t) = l(t)``. On a
point issued at ``t = 0``, ``pols_if(0)`` is the issued count, the notes' ``l(0)``, while
``pols_if_init()`` is 0, the count already in force at the valuation date; on a point in
force the two are one count. The notes' recursion ``l(t+1) = l(t)(1 - q_m(t))(1 - w_m(t))``
is the ``pols_if_at(t + 1, BEF_NB)`` step. Every BOM cash flow is weighted by
``pols_if(t)``, which is the notes' own ``l(t)`` weighting; take care not to read ``l(t)``
as an end-of-month count, which would weight every flow by the survivors of the month's
own decrements.

The notes write the monthly deduction as ``MD(t)`` and split it into a per-policy
charge, a per-unit charge, rider charges and the COI charge. ``CashValue_SE`` calls the
non-COI part of an account-value deduction ``maint_fee``; that name is kept here for
:func:`maint_fee_pp`, and :func:`mth_deduction_pp` is the notes' ``MD(t)`` in full.
:func:`expenses` is something different -- the insurer's own **[std]** maintenance
expense of $75 per policy per year, a cash flow, not a charge against the account
value. The two must not be confused: ``maint_fee`` is income, ``expenses`` is outgo.

The surrender-charge run-off ``SC(t) = max(0, (9.00 - (d(t) + 1)/12) x U)`` counts the
**current** month: one twelfth of a year's amortization is already earned in the issue
month, so the charge is $8.916667 per $1,000 in the issue month, not $9.00. The month
count in :func:`surr_charge_rate` is therefore ``duration_mth(t) + 1``, not
``duration_mth(t)``; using the completed months alone shifts the whole run-off by a
month.

``q_coi`` is quoted per $1,000 of net amount at risk **per month** and ``e_unit`` per
$1,000 of face per month, so both are divided by 1,000 -- or multiplied by
:func:`units` -- before they meet a currency amount. :func:`coi_rate` is therefore not
comparable with ``CashValue_SE.coi_rate``, which is a rate per unit of account value.

``surr_charge_pp(t)`` is the surrender charge *scheduled* at month ``t``;
``surr_charge(t)`` is the amount actually *collected* from lapsing policies, which is
capped by the account value because :func:`csv_pp` is floored at zero. In the first
policy years the schedule exceeds the account value and the two differ by a lot.

The notes' cash flow table lists "Withdrawal outgo" beside "Death claims" and
"Surrender outgo", but a partial withdrawal is a payment made on the **owner's
election**, not on a contingency, so it is not a claim here: it is :func:`withdrawals`,
its own cash flow line and its own ``result_cf()`` column, and no ``kind`` of
:func:`claim_pp` is a withdrawal. The consequence to hold on to is that
:func:`claims`, the total, is the death and surrender total *only*, so :func:`net_cf`
subtracts :func:`withdrawals` as a separate term. The per-policy amount
stays :func:`wd_pp`, which is the notes' ``W(t)``.

Finally, the notes write ``AV'(t)`` for one quantity and use it for two: the balance
the monthly deduction comes out of, and the balance the death benefit and the net
amount at risk are measured against. The two coincide until a policy in permanent
shortfall drives the account value negative -- which this model does not prevent,
because it does not terminate such a policy (:func:`is_shortfall`).
:func:`av_pp_at(t, BEF_FEE)<av_pp_at>` is the first and stays signed;
:func:`av_pp_db_basis` is the second and is floored at zero **[std]**, so an Option B
death benefit can never fall below the face amount.

.. rubric:: Codes

What :mod:`~.UL_US_S` spells as text, a timing or a kind, is here an int Reference named
as the text it replaces, so that every cell takes and returns C numbers. A call site
reads as it did, less the quotes: ``pols_if_at(t, BEF_DECR)``, ``av_pp_at(t, BEF_FEE)``,
``claim_pp(t, DEATH)``.

=============  =====  ===============================================================
Reference      Value  Meaning
=============  =====  ===============================================================
BEF_NB         0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR       1      :func:`pols_if_at`: that count plus month t's new business
BEF_MAT        2      :func:`pols_if_at`: before any maturity, the BEF_DECR count
BEF_PREM       3      :func:`av_pp_at`, :func:`av_at`: the account value carried in
BEF_WD         4      :func:`av_pp_at`, :func:`av_at`: after the net premium
BEF_FEE        5      :func:`av_pp_at`, :func:`av_at`: after the withdrawal and its fee
BEF_INV        6      :func:`av_pp_at`, :func:`av_at`: after the monthly deduction
EOM            7      :func:`av_at`: after the interest credit, before decrements
DEATH          0      :func:`claim_pp`, :func:`claims_from_av`: the death claim
LAPSE          1      :func:`claim_pp`, :func:`claims_from_av`: the surrender claim
MATURITY       2      :func:`claims_from_av`: none, the contract never matures
=============  =====  ===============================================================

The model has two families of timing, the count's and the account value's, passed to
different cells, and they are numbered as one: ``BEF_NB`` 0 and ``BEF_DECR`` 1, as in
every SEC model, then the count's third, ``BEF_MAT``, then the account value's in the
order of their instants within the month, ``EOM`` last. So no two timings share a code,
and a code of one family passed to the other's cell, ``av_pp_at(t, BEF_NB)``, is refused
as any timing the cell does not take is, ``ValueError("invalid timing")``, in both
engines, rather than read as a timing of the cell's own. Kinds are numbered in the
order the month settles them. A code a cell takes indexes that cell's cache, a C array
of eight codes a month for each of the five cells that take one, since every 2-D cache
of the model has one width (``spec_sec.py``), so codes are numbered densely from 0.
They are References, not cells, so the symbol map does not list them. Every other
Reference is named in lower case, ``issue_age_min`` and ``omega_age`` among them, two of
the contract's bounds that the compiled model's caches are sized from (:func:`proj_len`).

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`sex`, :func:`rate_class`,
:func:`db_option`, :func:`qual_test`, :func:`premium_type` and :func:`surr_charge_id`,
the reports :func:`result_cf`, :func:`result_pols` and :func:`result_av`, and the checks
:func:`check_av_roll_fwd` and :func:`check_margin` are written for a reader and for the
comparison with :mod:`~.UL_US_S`, which has every one of them: a table row, text,
DataFrames and two verdicts. No other cell calls them: each reads the number ``Data``
decoded from the same column instead, the decodes' flags, the schedules and the joins
the keys select. So the row, the text and the frames stay Python when the model
compiles. A label accessor returns its column as read, text or not: a blank
``surr_charge_id`` on a point without a charge reads as NaN, and a column of numbers as
ints, and the compiled accessor returns the same. Every other cell returns a C ``bint``,
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
    age in month t is :func:`age`.  ``Data`` reads it as ``UL_US_S`` reads it, ``int`` of
    the number, so a fractional age truncates toward zero.
    """
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point, M or F.

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
    """The initial total face amount F of the selected model point, the face at issue.

    The face the surrender charge is quoted on, whatever later withdrawals cut it to
    [S3], and the face a point not yet in force is issued with.  The face in force at the
    valuation date is :func:`sum_assured_init`, and the face in force in month t is
    :func:`sum_assured_at`.  From ``Data.sum_assured``.
    """
    return float(data.sum_assured()[idx])                            # noqa: F821


def db_option():
    """The death benefit option: ``"A"`` (level) or ``"B"`` (face plus account value).

    Option C (return of premium) is out of scope in the product spec.  A reporting cell
    (the Space docstring): ``Data`` decodes the column into :func:`is_db_option_a` and
    :func:`is_db_option_b`, and no projection cell reads it here.
    """
    return model_point()["db_option"]


def is_db_option_a():
    """Whether the death benefit is Option A, the level face, from ``Data.is_db_option_a``.

    ``Data`` decodes the ``db_option`` column, 1 where it is ``"A"``, so that no monthly
    cell branches on text; :func:`db_pp` and :func:`face_reduction_pp` read this instead.
    """
    return bool(data.is_db_option_a()[idx])                          # noqa: F821


def is_db_option_b():
    """Whether the death benefit is Option B, the face plus the account value.

    From ``Data.is_db_option_b``, 1 where ``db_option`` is ``"B"``, read by :func:`db_pp`,
    which raises on a point that is neither A nor B, as ``UL_US_S``'s does.
    """
    return bool(data.is_db_option_b()[idx])                          # noqa: F821


def qual_test():
    """The IRC 7702 qualification test elected at issue; only ``"GPT"`` is modeled.

    CVAT is out of scope in the product spec, so :func:`corridor_factor` raises on
    anything else rather than silently applying GPT corridor factors.  A reporting cell
    (the Space docstring): ``Data`` decodes the column into :func:`is_gpt`, and no
    projection cell reads it here.
    """
    return model_point()["qual_test"]


def is_gpt():
    """Whether the point elected the Guideline Premium Test, from ``Data.is_gpt``.

    1 where ``qual_test`` is ``"GPT"``, read by :func:`corridor_factor`, which raises on
    any other test, as ``UL_US_S``'s does: CVAT is out of scope in the product spec.
    """
    return bool(data.is_gpt()[idx])                                  # noqa: F821


def premium_type():
    """The premium pattern: ``"LEVEL"``, ``"SINGLE"`` or ``"TARGET"`` **[std]**.

    A reporting cell (the Space docstring): ``Data`` decodes the column into
    :func:`is_level_premium`, :func:`is_single_premium` and :func:`is_target_premium`, and
    no projection cell reads it here.
    """
    return model_point()["premium_type"]


def is_level_premium():
    """Whether the premium pattern is LEVEL, from ``Data.is_level_premium``.

    One of the three decodes of the ``premium_type`` column that :func:`premium_pp`
    branches on, so that no monthly cell compares text; :func:`premium_pp` raises on a
    point that is none of the three, as ``UL_US_S``'s does.
    """
    return bool(data.is_level_premium()[idx])                        # noqa: F821


def is_single_premium():
    """Whether the premium pattern is SINGLE, from ``Data.is_single_premium``.

    A decode of the ``premium_type`` column, read by :func:`premium_pp`.
    """
    return bool(data.is_single_premium()[idx])                       # noqa: F821


def is_target_premium():
    """Whether the premium pattern is TARGET, from ``Data.is_target_premium``.

    A decode of the ``premium_type`` column, read by :func:`premium_pp`.
    """
    return bool(data.is_target_premium()[idx])                       # noqa: F821


def premium_pp_ann():
    """The planned annual premium per policy; a billing target only [S3].

    From ``Data.premium_pp_ann``.
    """
    return float(data.premium_pp_ann()[idx])                         # noqa: F821


def wd_pp_mth():
    """The planned partial withdrawal per policy, in each month withdrawals are allowed.

    The model point's ``wd_pp`` column, ``Data.wd_pp``, a monthly amount, **0 in every
    shipped model point**: the notes give no withdrawal utilization pattern, so the
    behaviour is left to the data **[std]**.  Read once a point here, so that
    :func:`wd_pp`, a monthly cell on the account value's chain, reads no table in its own
    formula.
    """
    return float(data.wd_pp()[idx])                                  # noqa: F821


def load_prem_rate():
    """The current premium load rate, 6% **[std]** (guaranteed maximum 9%) [S1].

    The load is itself a non-guaranteed element in the source design, which is why it
    sits in the model point table rather than in a Reference.  From
    ``Data.load_prem_rate``, which refuses a load outside 0 to 1.
    """
    return float(data.load_prem_rate()[idx])                         # noqa: F821


def av_pp_init():
    """AV entering month 0: the account value per policy at the valuation date.

    The ``av_pp_init`` column, ``UL_US_S``'s own and the notes' ``av_initial``: the
    balance at the close of policy month ``duration_mth_init() - 1``, before any month-0
    event, which is what ``UL_US_S`` carries into the month as ``av_pp_at(d, BEF_PREM)``
    at ``d = duration_mth_init()``.  It is the opening balance of the account value chain
    at :func:`t_entry`, ``av_pp_at(0, BEF_PREM)``.  Zero for a point not yet in force,
    which is issued with no account value.  ``Data`` refuses a negative one: an account
    value below zero is an artifact of the grace cascade the model does not implement,
    which no policy in force can hold.  From ``Data.av_pp_init``.
    """
    return float(data.av_pp_init()[idx])                             # noqa: F821


def loan_bal_init():
    """L entering month 0: the policy loan balance per policy at the valuation date.

    The ``loan_bal_init`` column, ``UL_US_S``'s own and the notes'
    ``loan_balance_initial``: the debt outstanding at the close of policy month
    ``duration_mth_init() - 1``, interest accrued to then included, before any month-0
    event.  It is the opening balance of :func:`loan_bal_pp_bom` at :func:`t_entry`, the
    loaned portion that month 0's interest credit, shortfall test and death claim read.
    Zero for a point not yet in force.  From ``Data.loan_bal_init``.
    """
    return float(data.loan_bal_init()[idx])                          # noqa: F821


def sum_assured_init():
    """F entering month 0: the total face amount in force at the valuation date.

    The ``sum_assured_init`` column: the face in force at the close of policy month
    ``duration_mth_init() - 1``, after every Option A withdrawal cut to date, which is the
    face ``UL_US_S`` carries into the month as ``sum_assured_at(d - 1)``.  It is the base
    of :func:`sum_assured_at` at :func:`t_entry`, so month 0's own withdrawal cut, death
    benefit, net amount at risk and per-unit charge are measured from it.  The face at
    issue, :func:`sum_assured`, stays the surrender-charge base, and ``Data`` refuses a
    value above it, since face increases are not modelled.  Zero for a point not yet in
    force, which is issued at :func:`sum_assured`.  ``UL_US_S`` opens its in-force point
    at the face at issue.  From ``Data.sum_assured_init``.
    """
    return float(data.sum_assured_init()[idx])                       # noqa: F821


def wd_used_year_init():
    """The free withdrawal allowance already used in the policy year under way, per policy.

    The ``wd_used_year_init`` column: the free part of every withdrawal taken since the
    anniversary on or before the valuation date, through policy month
    ``duration_mth_init() - 1``, which is what ``UL_US_S`` carries into the month as
    ``wd_used_year(d)``.  :func:`wd_used_year` opens from it at :func:`t_entry`, so month
    0's free amount is what is left of the year's 10%.  The cell's name already says it
    restarts each policy year, so the column takes no ``_ytd``: on a point valued on an
    anniversary the year has just begun, the usage is 0, and ``Data`` refuses any other
    value there.  Zero for a point not yet in force.  ``UL_US_S`` opens its in-force
    point with the year's allowance unused.  From ``Data.wd_used_year_init``.
    """
    return float(data.wd_used_year_init()[idx])                      # noqa: F821


def cum_prem_init():
    """CumPrem entering month 0: premiums less withdrawals per policy before the valuation.

    The ``cum_prem_init`` column: every gross premium :func:`premium_pp` collected from
    issue through policy month ``duration_mth_init() - 1``, less every withdrawal
    :func:`wd_pp` paid, which is what ``UL_US_S`` carries into the month as
    ``cum_prem_pp(d - 1)``.  :func:`cum_prem_pp` opens from it at :func:`t_entry`, so the
    GPT test, the 7-pay test and the TARGET premium cap of month 0 all count the premiums
    paid before the valuation date.  ``ULSG_US_S`` gives the same column this name.  From
    ``Data.cum_prem_init``.

    It may be negative.  The notes' "less a portion of withdrawals" is taken as the whole
    withdrawal **[std]**, so this is a tax measure, not a balance, and withdrawals can
    exceed the premiums paid; ``Data`` holds the account value, the loan, the face and the
    usage to zero or more, and this to a number.  Zero for a point not yet in force.
    ``UL_US_S`` opens its in-force point with none paid.
    """
    return float(data.cum_prem_init()[idx])                          # noqa: F821


def is_mec_init():
    """The MEC latch entering month 0: whether the 7-pay test failed before it.

    The ``is_mec_init`` column, an int code: 1 for a policy that failed the 7-pay test in
    some month before the valuation date, and so is a modified endowment contract for
    good, 0 otherwise.  It is what ``UL_US_S`` carries into the month as ``is_mec(d - 1)``.
    :func:`is_mec` latches on it at :func:`t_entry`, so a policy that failed in its first
    seven years stays a MEC after them, where the in-year test no longer applies.
    ``Data`` refuses a 0 where ``cum_prem_init`` already exceeds the 7-pay limit of the
    month before the valuation date, inside the first seven policy years.  From
    ``Data.is_mec_init``, an int64 vector, so 1.0 reads as 1, and True.  Zero for a point
    not yet in force.  ``UL_US_S`` opens its in-force point with the latch off.
    """
    return bool(data.is_mec_init()[idx])                             # noqa: F821


def policy_count():
    """The number of policies the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the policies in force then, before any
    month-0 event; any other point counts the policies it issues.  Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second.  Every per-policy value -- the
    account value, the loan, the face, the opening state -- is the same whatever the
    count, and every cash flow is a per-policy amount weighted by it.  From
    ``Data.policy_count``.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """Policies in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose policies
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``.  So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count.  ``UL_US_S``'s cells of the name is the notes'
    ``l(0)``, the count at the start of its frame, which on new business is the issued
    count.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 120 for point 3, ``UL_US_S``'s in-force cell,
    126 for point 6, the same policy six months on, 0 for a policy issued at the valuation
    date, and -25 for point 9, to be issued 25 months after it, which ``Data`` admits up to
    ``future_horizon_mth`` months ahead.  This is the notes' ``policy_month_offset``, an
    elapsed count, already 0-based, and ``UL_US_S``'s cells and column of the same name,
    which count from the first projected month; here that month is the valuation date for
    every point, and the count may be negative.  It is the one fact the policy clock takes
    from the model point, from ``Data.duration_mth``.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point.

    From ``Data.has_surr_charge``, 1 where the column reads True.
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
    $9.00 on the shipped ``UL9`` schedule; :func:`surr_charge_rate` amortizes it linearly
    from here.  ``Data.surr_charge_rate_max`` joins it to the points by
    ``surr_charge_id``, once the table and the join are checked, so that no projection
    cell reads the table.  :func:`surr_charge_rate` reads it only where
    :func:`has_surr_charge` is true, but a point without a charge reads its schedule too,
    as at stage ``E``, where the table holds its id; where it does not,
    ``Data.has_surr_charge_schedule`` is 0, and this raises ``KeyError``, naming the point,
    where stage ``E``'s ``.loc`` raised it.
    """
    rate = float(data.surr_charge_rate_max()[idx])                   # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise KeyError(f"point_id {point_id()}: surr_charge_table.csv has no schedule "
                       f"for its surr_charge_id")
    return rate


def surr_charge_runoff_years():
    """The number of policy years over which the schedule's charge runs off.

    The ``runoff_years`` column of this point's row of *surr_charge_table.csv*, 9 on the
    shipped ``UL9`` schedule, read as a float: :func:`surr_charge_rate` amortizes
    :func:`surr_charge_rate_max` over it, and :func:`lapse_shock_year` is the year after
    it.  Joined by ``Data.surr_charge_runoff_years`` as :func:`surr_charge_rate_max` is,
    which refuses on a point with a charge a run-off of 0, which ``surr_charge_rate``
    would divide by, or one of ``2**53`` years or more in size, the bound every number
    read as an int is held to: the compiled ``int()`` in :func:`lapse_shock_year`
    converts it through a Python int to a C ``long long``, exact below ``2**63`` and
    raising ``OverflowError`` past it.  Read by those two only where
    :func:`has_surr_charge` is true; on a point without a charge it reads the schedule
    where the table holds its id, as at stage ``E``, and raises ``KeyError``, naming the
    point, where it does not, as :func:`surr_charge_rate_max` does.
    """
    years = float(data.surr_charge_runoff_years()[idx])              # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise KeyError(f"point_id {point_id()}: surr_charge_table.csv has no schedule "
                       f"for its surr_charge_id")
    return years


def gsp():
    """The guideline single premium (GPT compliance input) [S3], from ``Data.gsp``."""
    return float(data.gsp()[idx])                                    # noqa: F821


def glp():
    """The guideline level premium (GPT compliance input) [S3], from ``Data.glp``."""
    return float(data.glp()[idx])                                    # noqa: F821


def seven_pay_prem():
    """The 7-pay premium (IRC 7702A compliance input) [S3], from ``Data.seven_pay_prem``."""
    return float(data.seven_pay_prem()[idx])                         # noqa: F821


def duration_mth(t):
    """d(t): completed policy months at the beginning of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together.  A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame.  It is 0 in the issue month, ``t = 0`` for
    a point issued at the valuation date, and negative before issue.  This is the elapsed
    count in lifelib's sense (``CashValue_SE.duration_mth``) and the notes' month index;
    the surrender charge run-off counts the current month as well,
    ``duration_mth(t) + 1`` -- see :func:`surr_charge_rate`.
    """
    return duration_mth_init() + t


def duration(t):
    """Completed policy years at the beginning of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year, and negative before issue.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y: the policy year containing month t, the 1-based contractual label.

    ``duration(t) + 1``: derived from ``t``, and the key every policy-year table
    (*coi_rates.csv*, *lapse_table.csv*, *prem_persistency.csv*) is read with.  It is 0 or
    less before issue, where no table is read by it: each reader is called inside cover
    only (:func:`is_active`).
    """
    return duration(t) + 1


def age(t):
    """The attained age (ANB) in month t: ``age_at_entry() + duration(t)``.

    This is the notes' ``x + y - 1``.  Age changes on the policy anniversary, not on
    the birthday, which is the ANB convention the whole model is built on **[std]**.
    Before issue it is below the issue age, where no table is read at it.
    """
    return age_at_entry() + duration(t)


def omega_mth():
    """The policy month at which the projection ends, the first at attained age 121.

    ``12 * (omega_age - age_at_entry() + 1)``: 1,032 at issue age 35.  The mortality table
    ends at ``omega_age`` (120), where the annual rate is 1.0, so the last projected
    month, ``omega_mth() - 1``, is the last at attained age 120.  It is ``UL_US_S``'s frame
    length, counted from issue on the policy clock; :func:`proj_len` counts from the
    valuation date instead.  The contract has no maturity date [S2][S3], so the cell is
    named for ``omega_age``, the end of the table, and not for an event of the policy:
    where lives survive the last month, the count and the account value they carry into
    this month are kept (see :func:`pols_if_at`).
    """
    return 12 * (omega_age - age_at_entry() + 1)                     # noqa: F821


def proj_len():
    """The number of months from the valuation date to the end of the projection.

    ``omega_mth() - duration_mth_init()``: 1,032 for a policy issued at age 35 at the
    valuation date, 912 for point 3, in force 120 months, and 1,057 for point 9, issued 25
    months after the valuation date.  The frame is ``t = 0, 1, ..., proj_len() - 1``;
    ``proj_len()`` is its exclusive end, the row count of :func:`result_cf`, and
    ``proj_len() - 1`` is the last projected month, the last at attained age 120.  The
    contract has no maturity date [S2][S3]; the projection is truncated by mortality, not
    by the policy.

    Three kinds of point have no frame the contract issues, and each raises here, naming
    the point, rather than projecting what the contract does not hold, in this order:

    * one issued above ``omega_age``, 120, which would never be in cover: ``UL_US_S``
      projects it as months in which nothing happens.  Checked first, so that a point to
      be issued there is refused whenever it is to be issued;
    * one at or past the end of the projection at the valuation date, which an in-force
      extract should not carry;
    * one issued below ``issue_age_min``, 18, the youngest issue age ``product-spec.md``
      admits.  ``UL_US_S`` projects any age its tables serve, but the compiled model's
      caches are sized from the contract (``spec_sec.py``), so a younger point, whose
      frame and policy years run longer, would read past them.  A fractional issue age is
      read as ``UL_US_S`` reads it, truncated, so 17.5 is 17 and refused.
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
    return n


def t_entry():
    """The first month the policy is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later.  It is the base of every recursion: the count, the account value,
    the loan, the face, the year's withdrawal usage, the cumulative premium and the MEC
    latch all open there, from the model point's opening state on a point in force and
    from the issue values on any other.  No cell in cover reads a month before it.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and inside the projection.

    ``0 <= duration_mth(t) < omega_mth()``, false before issue and from
    ``t = proj_len()`` on.  Outside cover every count, charge, premium, withdrawal,
    decrement rate, decrement, claim and flow is zero and every flag false, no table is
    read at a policy year or an attained age the policy does not have, and nothing reads a
    month past ``proj_len()``; the clocks and the inputs read on the valuation clock keep
    their values, and the lapse shock's multiplier its neutral 1.0.  The two exceptions
    are the opening values of the month after the frame, the count and the account value
    carried into ``t = proj_len()``, which the roll-forwards read (see :func:`pols_if_at`
    and :func:`av_pp_at`).
    """
    return 0 <= duration_mth(t) < omega_mth()


def crediting_rate_ann(t):
    """i_cr: the current declared annual effective credited rate, 4.00% **[std]**.

    A non-guaranteed element under ASOP 2 [R8].  The base deterministic run holds the
    snapshot scale level, as the notes prescribe.  The notes' optional revision rule
    ``i_cr(t) = max(i_guar, earned_rate(t) - spread)`` needs an earned-rate input the
    notes do not supply and is not implemented.

    An economic input, so it is read on the **valuation** clock: ``t`` counts months from
    the valuation date, and a declared-rate scenario would be indexed by it, one path for
    every point of a block, however old the policy.  The shipped rate is flat, so the
    clock shows in no number.
    """
    return crediting_rate_curr                                       # noqa: F821


def inv_return_mth(t):
    """i_m: the monthly credited rate, ``(1 + i_cr)^(1/12) - 1``.

    0.0032737 at the **[std]** 4.00% current rate.  The contract credits daily on a
    365-day year [S3]; monthly compounding is the model's discretization **[std]** --
    do not also compound daily.
    """
    return (1 + crediting_rate_ann(t)) ** (1 / 12) - 1


def guar_rate_mth():
    """i_gm: the monthly guaranteed rate, ``(1 + i_guar)^(1/12) - 1`` = 0.0016516."""
    return (1 + guar_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def naar_factor():
    """The specimen's NAAR factor, ``1 + i_gm`` = 1.0016516 **[std]** at 2% [S3].

    The death benefit is discounted one month at the **guaranteed** rate, never the
    credited rate; the specimen prints 1.0024663 = 1.03^(1/12) at its own 3%
    guarantee [S3].
    """
    return 1 + guar_rate_mth()


def loan_rate_mth():
    """The monthly charged loan rate, ``(1 + r_L)^(1/12) - 1`` at r_L = 2.75%.

    The contract accrues daily and capitalizes annually [S3]; monthly compounding is
    the model's discretization **[std]**.
    """
    return (1 + loan_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def prem_persistency(t):
    """pp(y): the fraction of the planned premium actually paid in policy year y **[std]**.

    100% in year 1, declining 2 percentage points a year to a 70% floor from year 16,
    read from *prem_persistency.csv* at the policy year of month t by
    :func:`prem_persistency_py`.  The shape is informed qualitatively by the SOA/LIMRA UL
    study [R7]; the levels are a standardization.  Zero outside cover, before the table is
    read: before issue the valuation clock reaches policy years 0 and below.
    """
    return prem_persistency_py(policy_year(t)) if is_active(t) else 0.0


def prem_persistency_py(y):
    """pp(y) in policy year y, from *prem_persistency.csv*: the table's one reader.

    ``Data.prem_persistency_array()`` at the year, the table padded from year 0, so that
    the year is the index.  Policy years beyond the table take its last row, the last year
    ``data.prem_persistency_last_year()`` gives, which it reads from the table's key
    column once it has checked the keys and the factors, before any factor is read.  A
    year below 1, before the table's first row, where ``UL_US_S``'s ``.loc`` raised
    ``KeyError``, is refused, naming the point and the year, so that the padding is never
    read.  Keyed by the contractual policy year, so the table is read once a policy year
    rather than once a month; :func:`prem_persistency` calls it inside cover only.
    """
    last = data.prem_persistency_last_year()                         # noqa: F821
    if y < 1:
        raise ValueError(f"point_id {point_id()}: prem_persistency.csv has no factor for "
                         f"policy year {y}")
    return float(data.prem_persistency_array()[min(y, last)])        # noqa: F821


def premium_pp(t):
    """GP(t): the gross premium per policy received at BOM of month t.

    ``LEVEL``
        Planned annual premium / 12, times :func:`prem_persistency`.
    ``SINGLE``
        One premium in the issue month, capped at the guideline single premium.
    ``TARGET``
        As ``LEVEL`` but capped so cumulative premium stays inside the GPT limit
        **[std]**; the cap looks at the cumulative premium *before* this month's,
        ``cum_prem_pp(t - 1)``, so there is no circularity.  In the first month on the
        books, :func:`t_entry`, that is :func:`cum_prem_init`, the premiums paid before
        the valuation date, 0 at issue: a TARGET point in force near its limit collects
        only what the limit still has room for.

    Zero from attained age 121, when premiums are no longer accepted [S2][S3], and zero
    outside cover.  The pattern is read through its decodes, :func:`is_single_premium`,
    :func:`is_level_premium` and :func:`is_target_premium`, not as text.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    if is_single_premium():
        return min(premium_pp_ann(), gsp()) if duration_mth(t) == 0 else 0.0
    elif is_level_premium():
        return premium_pp_ann() / 12 * prem_persistency(t)
    elif is_target_premium():
        level = premium_pp_ann() / 12 * prem_persistency(t)
        paid = cum_prem_pp(t - 1) if t > t_entry() else cum_prem_init()
        return min(level, max(0.0, gpt_limit(t) - paid))
    else:
        raise ValueError("invalid premium type")


def prem_to_av_pp(t):
    """NP(t): the net premium credited to the account value, ``GP(t) x (1 - pl)``."""
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_av(t):
    """Net premium credited to account value, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """Premium income at BOM of month t, weighted by the in force at BOM."""
    return premium_pp(t) * pols_if(t)


def wd_pp(t):
    """W(t): the partial withdrawal per policy at BOM of month t.

    Withdrawals are allowed from the first policy anniversary and stop at attained age
    121 [S3].  The amount is the constant monthly figure :func:`wd_pp_mth`, the model
    point's ``wd_pp`` column, from the valuation date on, **0 in every shipped model
    point**: the notes give no withdrawal utilization pattern, so the mechanics are
    implemented and the behaviour is left to the data **[std]**.  Zero outside cover,
    before either contractual test, so that nothing is withdrawn at ``t = proj_len()``
    whatever ``omega_age`` and ``charges_cease_age`` are set to.
    """
    if not is_active(t):
        return 0.0
    if duration_mth(t) < 12 * wd_first_year:                         # noqa: F821
        return 0.0
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return wd_pp_mth()


def wd_used_year(t):
    """The free-withdrawal allowance already consumed in the current policy year.

    The notes' ``wd_used_year`` state variable, "free-withdrawal usage in current
    policy year, updated on withdrawal": reset to zero on each policy anniversary and
    increased month by month by the free part of each withdrawal taken since,
    ``min(W(t-1), wd_free_pp(t-1))``.  It is a value entering month t, before month t's
    own withdrawal.

    This is what makes the notes' allowance an **annual** one.  Without it the 10% is
    granted afresh every month, and a policyholder withdrawing 10% of the account value
    every month takes twelve full annual allowances in a policy year and never triggers
    the Option A face reduction of :func:`face_reduction_pp`.

    In the first month on the books, :func:`t_entry`, it is :func:`wd_used_year_init`,
    the usage of the policy year under way at the valuation date.  The anniversary reset
    comes first, so in an anniversary month, the issue month included, it is 0 whatever
    the model point says, and ``Data`` refuses a non-zero usage on a point valued on an
    anniversary.  Zero outside cover.
    """
    if not is_active(t) or duration_mth(t) % 12 == 0:
        return 0.0
    if t == t_entry():
        return wd_used_year_init()
    return wd_used_year(t - 1) + min(wd_pp(t - 1), wd_free_pp(t - 1))


def wd_free_pp(t):
    """The free partial withdrawal allowance still available in month t **[std]**.

    ``max(0, 10% of AV - wd_used_year(t))``: the allowance is 10% of the account value
    measured after the premium and before the withdrawal, less the part of it already
    taken earlier in the same policy year, and it resets on each policy anniversary --
    the notes' "free-amount rule (10% of AV per policy year)" with its ``wd_used_year``
    state (:func:`wd_used_year`).  In the first withdrawal month of a policy year
    nothing is used yet and this is the full 10%.

    The specimen's carve-out is the lesser of $10,000 and 10% of net cash surrender
    value, on the first withdrawal of each of the first 15 policy years [S3]; the
    composite simplifies to 10% of the account value, with no dollar cap and no
    15-year limit **[std]**.
    """
    allowance = wd_free_rate * av_pp_at(t, BEF_WD)                   # noqa: F821
    return max(0.0, allowance - wd_used_year(t))


def wd_fee_pp(t):
    """wf: the $25 withdrawal fee, charged only in a month with a withdrawal [S2][S3].

    The fee is retained by the insurer, so it is account-value outgo but not a
    liability cash flow; it appears in :func:`margin_expense`, not in :func:`claims`.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def face_reduction_pp(t):
    """The total face reduction forced by a withdrawal under Option A [S3].

    Under Option A a withdrawal beyond the free amount would otherwise increase the
    net amount at risk, so the face is cut by the excess.  The free amount is whatever
    is left of the policy year's allowance (:func:`wd_free_pp`), not a fresh 10% each
    month.  Under Option B the withdrawal reduces the account value only, and this is
    zero.  The option is read through its decode, :func:`is_db_option_a`.
    """
    if not is_db_option_a() or wd_pp(t) <= 0:
        return 0.0
    return max(0.0, wd_pp(t) - wd_free_pp(t))


def sum_assured_at(t):
    """F(t): the total face amount in force in month t, after any reductions.

    The face entering the first month on the books, :func:`t_entry`, is the face in force
    at the valuation date, :func:`sum_assured_init`, on a point in force, and the face at
    issue, :func:`sum_assured`, on any other; the face in month ``t`` is the previous
    month's less the reduction forced by this month's withdrawal, so ``F(t)`` already
    reflects a reduction taken at BOM of month ``t``, the first month's included.  Face
    increases, elective decreases and option changes are not modeled, so the only
    movement is the Option A withdrawal reduction.  Zero outside cover.
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


def units(t):
    """U: the total face amount in $1,000 units, ``sum_assured_at(t) / 1000``.

    The per-unit charge is quoted per $1,000 of face per month, so it is multiplied by
    this.  The surrender charge is quoted per $1,000 of **initial** face, because face
    decreases do not reduce it [S3]; see :func:`surr_charge_pp`.
    """
    return sum_assured_at(t) / 1000


def corridor_factor(t):
    """cf(a): the GPT corridor factor at the attained age of month t [S3][R2].

    250% to age 40, grading to 101% above age 93, read by :func:`corridor_factor_at`.
    Only the Guideline Premium Test is modeled; CVAT is out of scope in the product spec,
    so any other ``qual_test`` raises rather than being treated as GPT, in whatever month,
    since it is a fault of the point; the test is read through its decode, :func:`is_gpt`.
    Zero outside cover, before the table is read.
    """
    if not is_gpt():
        raise ValueError("invalid qual_test")
    return corridor_factor_at(age(t)) if is_active(t) else 0.0


def corridor_factor_at(a):
    """cf at attained age a, from *corridor_factors.csv*: the table's one reader.

    ``Data.corridor_factor_array()`` at the age, the table padded from age 0, so that the
    age is the index.  Ages outside the table take its nearest row, which above it is
    101%: the first and last ages ``data.corridor_age_first()`` and
    ``data.corridor_age_last()`` give, which they read from the table's key column once
    the keys and the factors are checked, before any factor is read.  So the padding is
    never read, and no age below 0 is either: ``Data`` refuses a table whose first age is
    negative.  The last is asked for first, since it runs the checks and the first is
    counted back from it, which keeps the call one level shallower.  Keyed by the attained
    age, so the table is read once an age rather than once a month;
    :func:`corridor_factor` calls it inside cover only.
    """
    last = data.corridor_age_last()                                  # noqa: F821
    a = min(max(a, data.corridor_age_first()), last)                 # noqa: F821
    return float(data.corridor_factor_array()[a])                    # noqa: F821


def av_pp_db_basis(t):
    """AV'(t) floored at zero: the balance the death benefit is measured against.

    The notes' step 4 sets the Option B death benefit to ``F + AV'(t)`` and step 5
    measures the net amount at risk against the same ``AV'(t)``, both on the premise
    that ``AV'`` is a real account balance.  It stops being one as soon as a policy in
    permanent shortfall keeps being projected: the grace and lapse-for-insufficiency
    cascade is not implemented (see :func:`is_shortfall`), so nothing terminates such a
    policy and its account value runs deeply negative.  Fed to ``F + AV'`` unfloored
    that gives an Option B death benefit **below the face amount**, and in the end a
    negative one -- a death claim paid *by* the beneficiary, which no universal life
    contract can produce.

    Flooring the balance at zero here is **[std]**, and is the same floor
    :func:`csv_pp` already carries for the same reason: a negative account balance is
    an artifact of the missing termination, not a contract state.  It holds the Option
    B death benefit at or above the face amount, and it stops the net amount at risk
    from growing with the shortfall and charging COI on a fund that is not there.

    Wherever ``AV'(t) >= 0`` -- every month of model points 1 and 3, and the first 677
    of point 2's 1,032 months -- this is exactly ``av_pp_at(t, BEF_FEE)`` and changes
    nothing, so the worked example is untouched.
    """
    return max(0.0, av_pp_at(t, BEF_FEE))


def db_pp(t):
    """DB(t): the death benefit per policy after the corridor test [S1][S3].

    ``max(option_db, cf(a) x AV'(t))`` where ``option_db`` is the face amount under
    Option A and face plus account value under Option B, and ``AV'(t)`` is the account
    value after premium and withdrawal and **before** the monthly deduction.  Taking
    the account value at that point is what removes the circularity the notes warn
    about: under Option B the death benefit depends on the account value and the net
    amount at risk depends on the death benefit, but with this BOM ordering neither
    depends on the deduction.

    The ``AV'(t)`` used here is :func:`av_pp_db_basis`, floored at zero **[std]**, so
    the death benefit is never less than the face amount; see that cells for why the
    floor is needed at all.  The option is read through its decodes,
    :func:`is_db_option_a` and :func:`is_db_option_b`, not as text.  Zero outside cover,
    before the corridor table is read.
    """
    if not is_active(t):
        return 0.0
    av = av_pp_db_basis(t)
    if is_db_option_a():
        opt = sum_assured_at(t)
    elif is_db_option_b():
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor(t) * av)


def net_amt_at_risk(t):
    """NAAR(t): ``DB(t) / (1 + i_gm) - AV'(t)``, floored at zero [S3].

    Two conventions here are the specimen's, not conveniences: the death benefit is
    discounted one month at the **guaranteed** rate (:func:`naar_factor`), and the
    account value is measured **before** the monthly deduction.  Using the credited
    rate in the discount, or the post-deduction account value, makes the COI charge
    implicit and requires iteration, and produces small systematic COI errors.

    The ``AV'(t)`` subtracted is :func:`av_pp_db_basis`, the same floored balance the
    death benefit is measured on, so the two sides of the subtraction stay consistent.
    """
    return max(0.0, db_pp(t) / naar_factor() - av_pp_db_basis(t))


def coi_schedule():
    """The number of this point's guaranteed COI scale, its row of ``Data.coi_rate_array``.

    ``Data.coi_schedule`` at this point: ``Data`` numbers each issue-age cell of
    *coi_rates.csv*, its ``sex``, ``rate_class`` and ``age_at_entry``, from 1 in the order
    of those keys, and gives each point the number of its own, or 0 where the table has no
    scale for it.  ``UL_US_S`` slices the scale, a Series, by the same three keys in
    ``coi_rate_scale``, which this replaces, since no compiled cell returns a Series.  A
    point without a scale is projected as ``UL_US_S`` projects it while no COI rate is
    read, and refused by :func:`coi_rate_last_year` once one is.
    """
    return int(data.coi_schedule()[idx])                             # noqa: F821


def coi_rate_guar(t):
    """q_coi_guar(s): the guaranteed maximum monthly COI rate per $1,000 NAAR [S3].

    A 2001 CSO-era specimen table, log-linearly interpolated between the printed
    anchor years **[std]**; it grades to 1000/12 at attained ages 112-120 and to zero
    from attained age 121.  Read at the policy year of month t by
    :func:`coi_rate_guar_py`; zero outside cover, before the scale is read.
    """
    return coi_rate_guar_py(policy_year(t)) if is_active(t) else 0.0


def coi_rate_guar_py(y):
    """q_coi_guar in policy year y, from this point's scale: the scale's one reader.

    ``Data.coi_rate_array()`` at the point's :func:`coi_schedule` and the year, each
    schedule padded from year 0, so that the year is the column.  Policy years beyond the
    scale take its last row, :func:`coi_rate_last_year`, which is asked for first, so that
    a projection meets the check of the table's keys, and the refusal of a point without
    a scale, before any rate is read.  A year below 1, where ``UL_US_S``'s slice raised
    ``KeyError``, is refused, naming the point and the year, so that the padding is never
    read.  Keyed by the contractual policy year; :func:`coi_rate_guar` calls it inside
    cover only.
    """
    last = coi_rate_last_year()
    if y < 1:
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no rate for policy "
                         f"year {y}")
    return float(data.coi_rate_array()[coi_schedule(), min(y, last)])  # noqa: F821


def coi_rate_last_year():
    """The last policy year of this point's guaranteed COI scale: its extent.

    ``Data.coi_rate_last_years`` at this point, the last year of its scale, which ``Data``
    reads from the table's key columns once it has checked the keys and the rates.  87 on
    the shipped anchor cell, whose scale runs to attained age 121.  A point the table
    has no scale for, schedule 0, has a last year of 0, and is refused here, naming it,
    where ``UL_US_S``'s slice raised ``KeyError``: when its first COI rate is read, and
    not before, since a point valued, or issued, at or past ``charges_cease_age`` never
    reads one, and ``UL_US_S`` projects it.  The element is compared, and ``int`` of it
    returned, rather than held in a local first, which a formula that also builds a
    message would keep a Python object compiled.
    """
    if data.coi_rate_last_years()[idx] < 1:                          # noqa: F821
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no scale for the "
                         f"point's sex, rate_class and age_at_entry")
    return int(data.coi_rate_last_years()[idx])                      # noqa: F821


def coi_rate(t):
    """q_coi(s): the current monthly COI rate, ``coi_curr_factor`` x guaranteed **[std]**.

    60% of the guaranteed maximum at every duration.  Current COI scales are not
    published -- only guaranteed maxima appear in the specimen [S3] -- so this factor
    is a pure modeling assumption and one of the two assumptions to sensitivity-test
    first.

    Note the units: this is per $1,000 of net amount at risk per **month**, so it is
    divided by 1,000 in :func:`coi_pp`.  It is not comparable with
    ``CashValue_SE.coi_rate``, which is a rate per unit of account value.
    """
    return coi_curr_factor * coi_rate_guar(t)                        # noqa: F821


def coi_pp(t):
    """The cost of insurance charge per policy, ``q_coi(y) / 1000 x NAAR(t)`` [S3].

    Zero from attained age 121, when monthly deductions cease [S2][S3], and zero outside
    cover.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def coi(t):
    """Cost of insurance charges deducted from account values, for the policies in force."""
    return coi_pp(t) * pols_if(t)


def rider_charge_pp(t):
    """rc(t): rider charges, 0 in the base model **[std]**.

    The notes carry this term in the monthly deduction so that rider modules can be
    added without changing the recursion [S3].
    """
    return 0.0


def maint_fee_pp(t):
    """The non-COI part of the monthly deduction per policy [S3].

    ``e_pol + e_unit(y) x U + rc(t)``: the $7.50 per-policy administrative charge, the
    per-unit coverage charge of $0.26 per $1,000 of face per month in policy years
    1-10 and $0.156 thereafter, and rider charges.  Zero from attained age 121, when
    charges cease [S2][S3], and zero outside cover.

    The name follows ``CashValue_SE.maint_fee``: this is a *charge* against the
    account value and therefore insurer income.  It is not :func:`expenses`, which is
    the insurer's own outgo.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    if policy_year(t) <= expense_unit_step_year:                     # noqa: F821
        e_unit = expense_unit_mth_1                                  # noqa: F821
    else:
        e_unit = expense_unit_mth_2                                  # noqa: F821
    return expense_pol_mth + e_unit * units(t) + rider_charge_pp(t)  # noqa: F821


def maint_fee(t):
    """Non-COI monthly charges deducted from account values, for the policies in force."""
    return maint_fee_pp(t) * pols_if(t)


def mth_deduction_pp(t):
    """MD(t): the monthly deduction per policy, taken at BOM [S3].

    ``e_pol + e_unit(y) x U + rc(t) + q_coi(y) / 1000 x NAAR(t)``, i.e.
    :func:`maint_fee_pp` plus :func:`coi_pp`.  The deduction at the start of month t
    pays for month t's coverage: the specimen says the deduction provides coverage for
    the following policy month, which with BOM indexing is the month it is taken in.
    """
    return maint_fee_pp(t) + coi_pp(t)


def mth_deduction(t):
    """Monthly deductions taken from account values, for the policies in force."""
    return mth_deduction_pp(t) * pols_if(t)


def av_pp_at(t, timing):
    """Account value per policy at an intra-month point of month t.

    The BOM events change the balance in this order, and ``timing`` names the point
    just before each of them:

    ``BEF_PREM``
        Before the premium: the closing balance of the previous month, ``AV(t-1)``, or
        the model point's opening balance :func:`av_pp_init` in the first month on the
        books, :func:`t_entry` -- the account value at the valuation date on a point in
        force, 0 at issue.  This is where the opening state enters the recursion, as in
        ``CashValue_SE``; :func:`av_pp` itself has no base case.  The previous month's
        close is formed here, from this timing's own value at ``t - 1`` and month
        ``t - 1``'s net premium, withdrawal, fee, deduction and interest, the same sum in
        the same order as ``av_pp(t - 1)``, rather than called for, so the chain of calls
        back to :func:`t_entry` is one cell a month, where ``UL_US_S``'s ran through
        five.  It is also defined in the month after the frame, ``t = proj_len()``,
        where it is the account value the survivors of the last month carry, which the
        roll-forward reads; zero before issue.

    ``BEF_WD``
        After the net premium, before the withdrawal.

    ``BEF_FEE``
        After the withdrawal and its fee, before the monthly deduction.  This is the
        notes' ``AV'(t)``, and the balance the death benefit, corridor test and net
        amount at risk are all measured against.

    ``BEF_INV``
        After the monthly deduction, before interest.  Interest is credited on this
        post-deduction balance; reversing the two overstates the account value by
        about one month's interest on the deduction every month.

    The end-of-month balance ``AV(t)`` is :func:`av_pp`.  The three timings after
    ``BEF_PREM`` are zero outside cover, ``t = proj_len()`` included.
    """
    if timing == BEF_PREM:
        if not 0 <= duration_mth(t) <= omega_mth():
            return 0.0
        if t == t_entry():
            return av_pp_init()
        av = (av_pp_at(t - 1, BEF_PREM) + prem_to_av_pp(t - 1) - wd_pp(t - 1)
              - wd_fee_pp(t - 1) - mth_deduction_pp(t - 1))
        loaned = loan_bal_pp_bom(t - 1)
        return av + ((av - loaned) * inv_return_mth(t - 1) + loaned * guar_rate_mth())
    elif timing == BEF_WD:
        if not is_active(t):
            return 0.0
        return av_pp_at(t, BEF_PREM) + prem_to_av_pp(t)
    elif timing == BEF_FEE:
        return av_pp_at(t, BEF_WD) - wd_pp(t) - wd_fee_pp(t)
    elif timing == BEF_INV:
        return av_pp_at(t, BEF_FEE) - mth_deduction_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_income_pp(t):
    """Interest credited to the account value per policy at EOM of month t.

    The unloaned part of the post-deduction balance earns the current monthly rate and
    the loaned part earns the guaranteed monthly rate [S2][S3]::

        (AV'(t) - MD(t) - L(t-1)) x i_m + L(t-1) x i_gm

    which is the notes' step 8 rearranged.  The loaned portion is taken as the opening
    loan balance :func:`loan_bal_pp_bom` exactly, as the notes write it, without capping
    it at the account value.
    """
    loaned = loan_bal_pp_bom(t)
    unloaned = av_pp_at(t, BEF_INV) - loaned
    return unloaned * inv_return_mth(t) + loaned * guar_rate_mth()


def av_pp(t):
    """AV(t): the account value per policy at the end of month t.

    The post-deduction balance plus one month's interest, for every month of the frame
    including the first on the books: the opening balance ``av_pp_init()`` enters through
    ``av_pp_at(t, BEF_PREM)``, not through a base case here.  With no loans and no
    withdrawals this collapses to the notes' core recursion
    ``AV(t) = [AV(t-1) + NP(t) - MD(t)] x (1 + i_m)``, which in the issue month of a point
    projected from issue reproduces the contractual policy-date rule that the account
    value equals the net premium less the first monthly deduction [S3].  Zero outside
    cover, through its timings.
    """
    return av_pp_at(t, BEF_INV) + inv_income_pp(t)


def loan_bal_pp_bom(t):
    """L(t-1): the policy loan balance per policy at the beginning of month t.

    The previous month's closing balance, or the model point's opening balance
    :func:`loan_bal_init` in the first month on the books, :func:`t_entry` -- the debt
    at the valuation date on a point in force, 0 at issue.  This is the loaned portion
    the interest credit, the shortfall test and the death claim all read; it plays for
    the loan the part ``av_pp_at(t, BEF_PREM)`` plays for the account value, and like
    it forms the previous month's close itself, its own value at ``t - 1`` times
    ``(1 + r_L)^(1/12)``, the product :func:`loan_bal_pp` takes, rather than calling for
    it.  So the chain back to :func:`t_entry` is one cell a month, where ``UL_US_S``'s
    ran through two.  Zero outside cover: nothing reads the loan at ``t = proj_len()``,
    where it would turn the death claim on a death benefit of 0 negative.
    """
    if not is_active(t):
        return 0.0
    if t == t_entry():
        return loan_bal_init()
    return loan_bal_pp_bom(t - 1) * (1 + loan_rate_mth())


def loan_bal_pp(t):
    """L(t): the policy loan balance per policy at the end of month t.

    ``L(t-1) x (1 + r_L)^(1/12)`` on the opening balance :func:`loan_bal_pp_bom`, for
    every month on the books, the first included.  Interest accrues daily and is
    capitalized annually under the contract [S3]; monthly compounding is the model's
    discretization **[std]**.  New loans and repayments are not modeled -- the notes
    give no utilization pattern -- so this only rolls the model point's opening
    balance forward.  Zero outside cover.
    """
    return loan_bal_pp_bom(t) * (1 + loan_rate_mth())


def av_at(t, timing):
    """Account value in force at an intra-month point of month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``EOM`` for the closing balance before
    decrements.  At ``t = proj_len()``, ``av_at(t, BEF_PREM)`` is the account value the
    survivors of the last month carry, which :func:`check_av_roll_fwd` reads.
    """
    if timing == EOM:
        return av_pp(t) * pols_if(t)
    return av_pp_at(t, timing) * pols_if(t)


def inv_income(t):
    """Interest credited to account values, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month's interest.
    """
    return inv_income_pp(t) * pols_if(t)


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


def surr_charge_rate(t):
    """SC per $1,000 of initial face in month t **[std amount; mechanics [S3]]**.

    ``max(0, sc_init - (sc_init / runoff_years) x m / 12)`` where ``m`` is the number
    of months amortized **including the current one**, ``duration_mth(t) + 1``, and
    ``sc_init`` and ``runoff_years`` are the schedule's, :func:`surr_charge_rate_max`
    and :func:`surr_charge_runoff_years`.  With the shipped schedule of $9.00 per $1,000
    running off over 9 years this is the notes' ``max(0, 9.00 - (d(t) + 1)/12)``:
    $8.916667 in the issue month, $8.00 in the last month of policy year 1, and zero from
    policy month 107, the last month of policy year 9, onward.  Using
    ``duration_mth(t)`` alone would shift the entire run-off by a month.  Zero outside
    cover.
    """
    if not is_active(t) or not has_surr_charge():
        return 0.0
    init = surr_charge_rate_max()
    yrs = surr_charge_runoff_years()
    m = duration_mth(t) + 1
    return max(0.0, init - (init / yrs) * (m / 12))


def surr_charge_pp(t):
    """SC(t): the surrender charge scheduled per policy in month t.

    Quoted on the **initial** face amount, because face decreases do not reduce the
    surrender charge [S3].  This is the schedule, not the amount collected: see
    :func:`surr_charge`.
    """
    return surr_charge_rate(t) * sum_assured() / 1000


def csv_pp(t):
    """CSV(t): the cash surrender value per policy, ``AV(t) - SC(t)``, floored at zero.

    The floor is **[std]**: the notes write ``CSV = AV - SC`` without one, but a
    negative cash surrender value would be a payment *from* the policyholder.  In the
    early policy years the scheduled surrender charge exceeds the account value and
    the floor binds, so the charge actually collected is the whole account value.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """NCSV(t): the net cash surrender value, ``CSV(t) - L(t)``, floored at zero.

    This is what a surrendering policyholder is paid, and the notes' surrender outgo.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """Surrender charge actually collected from the policies lapsing in month t.

    ``(AV(t) - CSV(t)) x pols_lapse(t)``, so it is capped by the account value where
    the :func:`csv_pp` floor binds.  Insurer income, and part of
    :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def is_shortfall(t):
    """The grace trigger: ``AV'(t) - L(t-1) < MD(t)`` on a monthiversary [S2][S3].

    A diagnostic.  The full grace and lapse-for-insufficiency cascade is **not
    implemented**: the notes leave the in-grace account value treatment (deductions
    accrue as due and unpaid) and the cash flow of a cure payment undetermined, so no
    policy is terminated for insufficiency here.

    It is not inert.  Of the three model points that are ``UL_US_S``'s own, its twins:

    * point 1, the worked-example anchor, is never in shortfall in any of its 1,032
      months -- ``$150`` a month comfortably covers the ``$39.54`` issue-month
      deduction, and the account value grows from there;
    * point 3, the in-force cell, is never in shortfall in any of its 912 months;
    * point 2, the Option B cell, **is** in shortfall from ``t = 676`` (policy year 57,
      attained age 91) to the end of the projection, 356 months.  Level $150 premiums
      stop covering a COI charge on a ~$100,000 net amount at risk at those ages.

    Point 7 is point 2 restated in force at that month, so it is in shortfall from
    ``t = 0`` for the whole of its frame.  Because nothing terminates either, their
    deductions keep coming out of an account value that is already empty, and point 2
    ends the projection about $1.84m overdrawn.  That is an artifact of the missing
    cascade, and it is why the death benefit is measured on the floored
    :func:`av_pp_db_basis` rather than on a signed ``AV'``.  Treat cash flows for a model
    point in shortfall as **not meaningful** past the trigger month; the README says so
    too.  False outside cover, where every term is zero.
    """
    return av_pp_at(t, BEF_FEE) - loan_bal_pp_bom(t) < mth_deduction_pp(t)


def cure_premium_pp(t):
    """The payment required to cure a grace: ``3 x MD(t)`` grossed up for the load [S3].

    The specimen requires at least three times the monthly deduction due plus the
    premium load, so the gross payment is ``3 x MD / (1 - pl)``.  A diagnostic; see
    :func:`is_shortfall`.

    ``Data`` admits a load of 1, which ``UL_US_S`` projects in full, since no report
    reads this cell, and at which this one divides by zero.  ``UL_US_S`` raises Python's
    ``ZeroDivisionError: float division by zero`` there, and the compiled division's
    check would raise the same error with another message, so the divisor is checked
    first and ``UL_US_S``'s own error raised, the same in both engines.
    """
    if 1 - load_prem_rate() == 0:
        raise ZeroDivisionError("float division by zero")
    return 3 * mth_deduction_pp(t) / (1 - load_prem_rate())


def cum_prem_pp(t):
    """CumPrem(t): cumulative premiums less withdrawals through month t.

    The running total for the GPT and 7-pay tests, including month ``t``'s own premium
    and withdrawal.  It opens in the first month on the books, :func:`t_entry`, from
    :func:`cum_prem_init`, the premiums less withdrawals paid before the valuation date
    on a point in force and 0 at issue, so the GPT and 7-pay flags of a point in force
    count every premium since issue.  ``UL_US_S`` restarts it at 0 on its in-force
    point, the notes giving no opening cumulative-premium attribute **[std]**.  The
    notes' "less a portion of withdrawals" is taken as the whole withdrawal **[std]**.
    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = cum_prem_pp(t - 1) if t > t_entry() else cum_prem_init()
    return prev + premium_pp(t) - wd_pp(t)


def gpt_limit(t):
    """The guideline premium limit, ``max(GSP, GLP x policy years elapsed)`` [S3][R2].

    Zero outside cover, where the policy year is not the policy's.
    """
    if not is_active(t):
        return 0.0
    return max(gsp(), glp() * policy_year(t))


def gpt_ok(t):
    """Whether cumulative premium is still inside the guideline premium limit.

    A compliance side-calculation with no cash flow of its own: a refused premium
    simply never enters the model [S3][R2][R3].  False outside cover.
    """
    if not is_active(t):
        return False
    return cum_prem_pp(t) <= gpt_limit(t)


def seven_pay_limit(t):
    """The 7-pay limit, ``seven_pay_prem x min(7, policy years elapsed)`` [R3][REG-R14].

    Zero outside cover, where the policy year is not the policy's.
    """
    if not is_active(t):
        return 0.0
    return seven_pay_prem() * min(7, policy_year(t))


def is_mec(t):
    """Whether the 7-pay test has failed by month t -- once true, true for good.

    ``CumPrem(t) > 7-pay limit`` in any of the first seven policy years, **latched**:
    the flag stays set for the rest of the projection.  The latch is not decoration.
    Under IRC 7702A the contract *is* a modified endowment contract once the 7-pay test
    fails, permanently and for every later year [R3][REG-R14]; and the in-year test
    itself stops applying in policy year 8, so an unlatched flag would quietly switch
    itself off exactly when the failure becomes permanent.  The notes ask the base
    model to "flag (does not project) 7-pay failures", which a flag that turns itself
    off does not do.

    The in-year test comes first in every month, the first on the books included, so a
    policy that fails it in the valuation month is a MEC from then on.  Only then does
    the latch look back: to month ``t - 1``, or, in the first month on the books,
    :func:`t_entry`, to :func:`is_mec_init`, so a policy that failed the test before the
    valuation date stays a MEC, even in a year where the in-year test no longer applies.
    False outside cover.

    A flag, not a cash flow: MEC status changes policyholder taxation, not insurer
    liability cash flows, and modeling it as a charge or refund would distort premium
    income [S3][R2][R3].
    """
    if not is_active(t):
        return False
    if policy_year(t) <= 7 and cum_prem_pp(t) > seven_pay_limit(t):
        return True
    return is_mec(t - 1) if t > t_entry() else is_mec_init()


def class_factor():
    """The underwriting-class multiplier on the base mortality table **[std]**.

    The ``factor`` of this point's ``rate_class`` in *class_factor_table.csv*, joined to
    the points by ``Data.class_factor`` once ``data.class_count()`` has checked the
    table's classes and factors: a blank factor would otherwise reach :func:`mort_rate` as
    a missing value.  A point whose class the table lacks, which ``UL_US_S`` fails on in
    every projection, is refused by ``Data`` at the join's first read, naming every such
    point.
    """
    return float(data.class_factor()[idx])                           # noqa: F821


def mort_rate(t):
    """The annual best-estimate mortality rate in month t, capped at 1.

    Base table times :func:`class_factor` times the A/E factor, which is 100% in the
    base run **[std]** with no mortality improvement.  The shipped table is a small
    illustrative one **[std]**, *not* the 2015 VBT the notes recommend -- that family
    is licensed and may not be reproduced here.  Ages beyond the table take its last
    row, where the rate is 1.0.  The base rate is read at the attained age of month t by
    :func:`mort_rate_base_at`.

    The product is capped at 1.0, as ``UL_US_S``'s and ``ULSG_US_S``'s are.  A class factor
    above 1 -- 1.50 and 1.75 for the two tobacco classes -- carries the oldest ages' rates
    past 1, where the monthly rate ``1 - (1 - q)^(1/12)`` has no real value; at the shipped
    A/E a StdTob point's product first passes 1 at attained age 113.  Where the product is
    at most 1, which is every rate ``UL_US_S``'s own points reach, the cap changes nothing.
    It is written ``min(q, 1.0)``, as ``UL_US_S`` writes it, the same float as
    ``min(1.0, q)`` wherever ``q`` is a number: Python's ``min``, and the compiled cell,
    keep their first argument unless a later one is smaller, so ``min(1.0, q)`` would turn
    a blank base rate or class factor, which ``UL_US_S`` reads as a missing value, into
    1.0, certain death with every flow finite, where ``min(q, 1.0)`` keeps it missing.
    ``Data`` refuses both as it reads the tables (``data.mort_age_last()``,
    ``data.class_count()``), before any rate is read.  Zero outside cover.
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
    rate of 1.0 at age 120: the first and last ages ``data.mort_age_first()`` and
    ``data.mort_age_last()`` give, which they read from the table's key column once the
    keys and the rates are checked, before any rate is read, the last first, as
    :func:`corridor_factor_at` asks, and which keep the read off the padding.  Keyed by
    the attained age, so the table is read once an age rather than once a month;
    :func:`mort_rate` calls it inside cover only.
    """
    last = data.mort_age_last()                                      # noqa: F821
    a = min(max(a, data.mort_age_first()), last)                     # noqa: F821
    return float(data.mort_table_array()[a])                         # noqa: F821


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate, ``1 - (1 - q)^(1/12)``."""
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """w_base(y): the base annual lapse rate by policy year **[std]**.

    6% in year 1, 5% in year 2, 4% in years 3-10, 3% thereafter, read from
    *lapse_table.csv* at the policy year of month t by :func:`lapse_rate_base_py`.  The
    shape is informed qualitatively by the SOA/LIMRA UL persistency studies
    [R7][REG-R20], whose detailed tables are behind a paid package, so the levels are a
    standardization.  Zero outside cover, before the table is read.
    """
    return lapse_rate_base_py(policy_year(t)) if is_active(t) else 0.0


def lapse_rate_base_py(y):
    """w_base in policy year y, from *lapse_table.csv*: the table's one reader.

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


def lapse_shock_year():
    """The policy year of the surrender-charge-expiry lapse shock.

    The first policy year with no surrender charge in any month, i.e. the run-off length
    plus one; because the run-off counts the current month the charge already reaches
    zero in policy month 107, the last month of policy year 9.  Derived from the
    schedule's :func:`surr_charge_runoff_years` rather than hard-coded, so a different
    schedule moves the shock with it.  Zero when the model point carries no surrender
    charge, which no policy year in cover can equal.  The valuation clock reaches policy
    year 0 in the twelve months before issue, which is why :func:`lapse_rate_sc_mult`
    asks :func:`is_active` first.
    """
    if not has_surr_charge():
        return 0
    return int(surr_charge_runoff_years()) + 1


def lapse_rate_sc_mult(t):
    """M_sc: the surrender-charge-expiry lapse shock multiplier, 2.0 **[std]**.

    Applied in the policy year :func:`lapse_shock_year` gives, and only there.  The
    surrender charge suppresses
    surrender while it is positive and its expiry is a known industry shock point;
    product-specific studies are proprietary, so the size is a shape assumption.  1.0
    outside cover, before the policy year is compared: in the twelve months before issue
    the valuation clock reaches policy year 0, the shock year :func:`lapse_shock_year`
    gives a point with no surrender charge.
    """
    if not is_active(t):
        return 1.0
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def comp_rate_ann(t):
    """r_comp(t): the competitor / market new-money rate driving dynamic lapse **[std]**.

    The base deterministic run sets it equal to the current credited rate, exactly as
    the notes prescribe, so :func:`lapse_rate_dyn_mult` is 1.  An economic input, read on
    the **valuation** clock, as :func:`crediting_rate_ann` is.  To switch
    interest-sensitive lapse on, override this cell's formula before the model computes
    anything; that is a formula override, which only modelx can make.
    """
    return crediting_rate_ann(t)


def lapse_rate_dyn_mult(t):
    """M_rate(t): the interest-sensitive lapse multiplier **[std]**.

    ``min(3.0, 1 + 5 x max(0, r_comp(t) - i_cr(t) - 0.01))``: no effect until the
    competitor rate exceeds the credited rate by more than 100 basis points.  Equal to
    1 throughout the base run.
    """
    excess = max(0.0, comp_rate_ann(t) - crediting_rate_ann(t)
                 - lapse_dyn_threshold)                              # noqa: F821
    return min(lapse_dyn_cap, 1 + lapse_dyn_slope * excess)          # noqa: F821


def lapse_rate(t):
    """w_annual(y, t): the total annual lapse rate **[std]**.

    ``min(0.35, w_base(y) x M_sc(y) x M_rate(t))`` -- the base rate, the
    surrender-charge-expiry shock and the dynamic multiplier, capped **[std]**.
    """
    rate = lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_rate_dyn_mult(t)
    return min(lapse_rate_cap, rate)                                 # noqa: F821


def lapse_rate_mth(t):
    """w_m(t): the monthly lapse rate, ``1 - (1 - w_annual)^(1/12)``."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """Number of policies in force at the beginning of month t, the weight of row t.

    ``pols_if_at(t, BEF_DECR)``, the notes' ``l(t)``: the count carried in from month
    t - 1 plus month t's new business, before month t's decrements.  Decrements are
    end-of-month events, so the number in force is constant through the month and every
    BOM cash flow is weighted by it.  On a point issued at ``t = 0`` it is exactly
    ``UL_US_S``'s ``pols_if``.  A point in force at the valuation date opens with
    :func:`pols_if_init`, and one issued at or after it with its issued count in the
    issue month.  Zero before issue.  At ``t = proj_len()``, the month after the frame,
    it is the survivors of the last month, which the roll-forwards read.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity.
    """
    return pols_if_at(t, BEF_DECR)


def pols_if_at(t, timing):
    """Number of policies in force at a point of month t, by ``timing``.

    The three timings ``UL_US_S``'s cell names:

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
        ``l(t)``: ``BEF_NB`` plus :func:`pols_new_biz`, before any decrement; the same
        number as :func:`pols_if`, and the weight on that month's cash flows.
    ``BEF_MAT``
        Before any maturity: ``UL_US_S``'s meaning, the ``BEF_DECR`` count, which its
        cell gives for this timing.  The contract has no maturity date, so nothing
        matures and no event of the month separates the two.  ``basiclife.BasicTerm_SE``'s
        ``BEF_MAT``, the count at the start of the month before its new business, is
        not adopted, as it is not in ``Term_US_SEC`` and ``WholeLife_US_SEC``: the name
        keeps its S model's meaning.

    ``BEF_NB`` forms the count left at the end of month t - 1 itself -- month t - 1's
    ``BEF_NB`` count plus its :func:`pols_new_biz`, less its deaths and lapses, the
    products :func:`pols_death` and :func:`pols_lapse` take, in the order they take
    them -- rather than calling for it.  So the chain of calls back to :func:`t_entry`
    is one cell a month, as ``UL_US_S``'s :func:`pols_if` chain was: a compiled model runs
    that chain on the C stack.  ``UL_US_S``'s cell returns :func:`pols_if` for every
    timing, which in the issue month counts the issued policies under all three; here
    ``BEF_NB`` alone counts them as new business, not yet in.  Any other timing raises.
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
    """Number of deaths at the end of month t, ``pols_if(t) x q_m(t)``.

    Zero outside cover, before any rate is read.
    """
    return pols_if(t) * mort_rate_mth(t) if is_active(t) else 0.0


def pols_lapse(t):
    """Number of lapses at the end of month t.

    ``pols_if(t) x (1 - q_m(t)) x w_m(t)``: death is applied before lapse **[std
    order]**, matching the notes' ``l(t+1) = l(t)(1 - q_m(t))(1 - w_m(t))``.  Zero
    outside cover, before any rate is read.
    """
    if not is_active(t):
        return 0.0
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    Universal life has no maturity date -- at attained age 121 charges cease, premiums
    stop and coverage continues for life [S2][S3].  The cells is kept so the in-force
    roll-forward identity has the same shape as in the term and annuity models of this
    library, where it is not zero.  The survivors of the last projected month do not
    mature either: the projection stops there because the mortality table does, and they
    are carried into ``t = proj_len()`` (:func:`pols_if_at`).
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``DEATH``
        ``DB(t) - L(t-1)``: the death benefit less the policy debt at the start of the
        month, :func:`loan_bal_pp_bom` [S3].  Due and unpaid deductions during grace
        would also be subtracted, but the grace cascade is not implemented.

    ``LAPSE``
        ``NCSV(t)``, the net cash surrender value.

    A partial withdrawal is **not** a claim -- it is a payment on the owner's election
    rather than on a contingency -- so no ``kind`` here is a withdrawal.  Its
    per-policy amount is :func:`wd_pp` and its cash flow is :func:`withdrawals`; the
    $25 fee is retained by the insurer and is not part of the payment.
    """
    if kind == DEATH:
        return db_pp(t) - loan_bal_pp_bom(t)
    elif kind == LAPSE:
        return ncsv_pp(t)
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim paid out of the account value, by ``kind``.

    Death and lapse both release the end-of-month account value ``AV(t)``, because
    decrements follow the interest credit.  ``MATURITY`` is zero: the contract has
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

    ``(claim_pp(t, DEATH) - AV(t)) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin.
    """
    return (claim_pp(t, DEATH) - av_pp(t)) * pols_death(t)


def claims(t):
    """Claim outgo in month t: death and surrender claims together.

    :func:`claims_death` and :func:`claims_lapse`, summed left to right from ``0.0``, the
    total :func:`net_cf` subtracts.  ``UL_US_S``'s ``claims(t, kind=None)`` is both the
    kinds and their total, a generator summed by Python's ``sum``, which compiles to
    neither a C parameter nor a C loop; here the kinds are two cells, the ``result_cf``
    columns, and this is their total.  Python's ``sum`` of floats is compensated, but of
    two it is their sum, rounded once, which is what this computes, and its ``0.0``
    start keeps ``sum``'s, which turns two negative zeros to ``0.0``.  So the total is
    ``UL_US_S``'s float in every month.

    Partial withdrawals are **not** here, neither as a kind nor in the total: a
    withdrawal is a payment on the owner's election rather than a claim, and is
    :func:`withdrawals`.  So ``claims(t)`` is the death and surrender total only, and
    :func:`net_cf` subtracts the withdrawal row separately.
    """
    return 0.0 + claims_death(t) + claims_lapse(t)


def claims_death(t):
    """Death claims in month t: :func:`pols_death` at the death benefit per policy,
    ``claim_pp(t, DEATH)``, an end-of-month event.  The ``claims_death`` column of
    :func:`result_cf`."""
    return claim_pp(t, DEATH) * pols_death(t)                        # noqa: F821


def claims_lapse(t):
    """Surrender claims at the end of month t: :func:`pols_lapse` at the net cash
    surrender value per policy, ``claim_pp(t, LAPSE)``.  The ``claims_lapse`` column of
    :func:`result_cf`."""
    return claim_pp(t, LAPSE) * pols_lapse(t)                        # noqa: F821


def withdrawals(t):
    """Partial withdrawal payments at BOM of month t.

    ``W(t) x pols_if(t)``: a withdrawal is taken at the beginning of the month by the
    policies still in force, so it is weighted by :func:`pols_if` and not by a
    decrement.

    It is a cash flow line of its own -- the ``withdrawals`` column of
    :func:`result_cf` -- and not a ``kind`` of :func:`claim_pp`, because a withdrawal is
    a payment the owner elects rather than a claim on a contingency.  The $25
    withdrawal fee is retained by the insurer and is not part of the payment; see
    :func:`wd_fees`.

    Zero in every shipped model point: the mechanics are implemented and the
    utilization is left to the data **[std]**, as :func:`wd_pp` explains.
    """
    return wd_pp(t) * pols_if(t)


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force.

    Account-value outgo but not a liability cash flow, so this appears in
    :func:`margin_expense` and not in :func:`claims`.
    """
    return wd_fee_pp(t) * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(t // 12)`` **[std]**.

    Expenses inflate by year, not by month, which is how the notes write the $75 per
    policy per year maintenance expense, and on the **valuation** clock: the years are
    counted from the valuation date, ``t // 12``, so the expense is in valuation-date
    dollars whatever the policy's age, and every point of a block steps alike, on the
    valuation anniversaries.  ``UL_US_S`` steps on the policy year,
    ``(1 + inflation_rate)^(y - 1)``; on a point issued at ``t = 0`` the two are the same,
    and on point 3, in force 120 months, this model's expense is ``UL_US_S``'s divided by
    ``1.025^10``.  Acquisition is not inflated (see :func:`expenses`).
    """
    return (1 + inflation_rate) ** (t // 12)                         # noqa: F821


def expenses(t):
    """The insurer's own expenses in month t **[std]**.

    ``(acq + expense_maint / 12 x inflation) x pols_if(t)``, ``UL_US_S``'s formula in its
    order: the maintenance expense inflating at 2.5% a year, on the valuation clock, and
    ``expense_acq`` in the issue month, ``duration_mth(t) == 0``, not inflated, both on
    the policies in force at the start of the month.  In the issue month those are the
    policies issued, :func:`pols_new_biz`, since a point issued at or after the valuation
    date opens with none, so acquisition is charged per policy issued, as in
    ``basiclife.BasicTerm_SE``, and a point in force at the valuation date never bears it,
    because it was issued before.  On a point issued at ``t = 0`` this is ``UL_US_S``'s
    charge bit for bit.  The notes specify no acquisition expense for this product -- the
    higher per-unit charge in policy years 1-10 is the contractual acquisition-cost
    recovery, which is income, not outgo -- so ``expense_acq`` is zero and the term is
    carried only so products built on this chassis can switch it on.

    Zero outside cover, where the count carried into ``t = proj_len()`` would otherwise
    bear a maintenance expense.  Not to be confused with :func:`maint_fee`, which is the
    charge *against the account value*.
    """
    if not is_active(t):
        return 0.0
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    return (acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """Premium tax and other percent-of-premium expense, 2.5% of premium **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``load x GP + withdrawal fees + maint_fee + surrender charges - expenses
    - premium taxes``.  Follows ``CashValue_SE.margin_expense``; see
    :func:`check_margin` for the identity it takes part in.
    """
    return (load_prem_rate() * premium_pp(t) * pols_if(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`."""
    return coi(t) - claims_over_av(t)


def net_cf(t):
    """Net liability cash flow in month t, **undiscounted**.

    ``premiums - death claims - surrender payments - withdrawals - expenses
    - premium taxes``, **income-positive** as in every model of this library.
    :func:`claims` carries the death and surrender rows only, so the withdrawal row is
    subtracted as its own term.  Like the rest of this library the model projects
    *gross liability cash flows*: there is no discounting and no change in account
    value in this figure, because reserves are a separate layer that consumes these
    flows.  Investment income on the account value is a credit to the policyholder,
    not an insurer cash flow, so it does not appear either -- see :func:`check_margin`
    for how it reconciles.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - premium_taxes(t))


def check_av_roll_fwd():
    """Check the account value roll-forward.

    Returns ``True`` when, for every projected month, the opening account value in
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
    ``math.isclose`` tests with both its tolerances at ``1e-9``.  This pins the notes'
    processing order, in particular that interest is credited on the *post-deduction*
    balance and that decrements come after the credit.  Each month's residual is
    :func:`check_av_roll_fwd_resid`, so a failure can be found by month, and a residual
    that is not a number fails.  In the last month the opening value of ``t + 1`` is the
    account value the survivors carry into ``t = proj_len()``.
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
    ``math.isclose`` with both tolerances at ``1e-9`` holds.  Zero outside cover, before
    ``t + 1`` is read, so that nothing reads a month past ``t = proj_len()``.  Returned
    as ``float(...)`` of the ratio, as the life chassis returns every residual: a real
    ratio is its own float, and one that is not real, as a decrement rate past 1 would
    make it in modelx, raises here rather than pass the check on its magnitude.
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

    Returns ``True`` when, for every projected month::

        net_cf(t) == margin_expense(t) + margin_mortality(t)
                     + av_change(t) - inv_income(t)
                     + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)

    to within ``1e-9``, relative to the larger side and 1, as for
    :func:`check_av_roll_fwd`; each month's residual is :func:`check_margin_resid`, and a
    residual that is not a number fails.  The last three terms are what separates a
    *gross liability cash flow* model from ``CashValue_SE``, whose ``net_cf`` already nets
    the change in account value and the investment income; the loan term is the debt a
    surrender recovers out of the cash value, which is the whole loan while the cash value
    covers it and the cash value once the loan exceeds it, where :func:`ncsv_pp` pays
    nothing.  ``UL_US_S``'s identity takes the whole loan in every month, so it is off by
    ``(CSV(t) - L(t)) x pols_lapse(t)`` once the loan exceeds the cash value, and its check
    fails on a projection that is right; on every shipped model point the cash value
    covers the loan, and the two checks agree.
    """
    for t in range(proj_len()):
        if not abs(check_margin_resid(t)) <= 1e-9:
            return False
    return True


def check_margin_resid(t):
    """The margin identity's relative residual in month t; zero everywhere.

    ``net_cf(t)`` less the margins, the change in account value, the investment income
    and the loan a surrender recovers, that :func:`check_margin` sets out, over the larger
    of the two sides in magnitude and 1, as :func:`check_av_roll_fwd_resid` measures its
    own.  Zero outside cover, before :func:`av_change` would read ``t + 1``.  Returned
    as ``float(...)`` of the ratio, as :func:`check_av_roll_fwd_resid` is.
    """
    if not is_active(t):
        return 0.0
    rhs = (margin_expense(t) + margin_mortality(t)
           + av_change(t) - inv_income(t)
           + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t))
    lhs = net_cf(t)
    return float((lhs - rhs) / max(abs(lhs), abs(rhs), 1.0))


def result_cf():
    """Result table of cashflows, a DataFrame indexed by month ``t``.

    One row per month ``t = 0 .. proj_len() - 1`` from the valuation date, the same month
    for every model point, so the frames of a block line up and sum row by row, and a
    point issued after the valuation date has zeros until its issue month.  The columns
    are ``UL_US_S``'s.  The two claim columns are the cells of their names,
    :func:`claims_death` and :func:`claims_lapse`, each the claim of the ``kind`` it is
    named for, and partial withdrawals sit in their own ``withdrawals`` column rather
    than among the claims.  The cash flow columns sum to
    ``net_cf`` under the income-positive sign convention: ``premiums`` less every other
    flow.
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
    new business of month ``t + 1``.  Then ``UL_US_S``'s two monthly decrement rates,
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

    The columns are the columns of the worked example in the technical notes, in the
    notes' own order: ``AV(t-1)``, ``NP``, ``AV'``, ``DB``, ``NAAR``, ``COI``, ``MD``,
    ``AV' - MD``, interest, ``AV(t)``, followed by the surrender and loan values.  The
    index runs ``t = 0 .. proj_len() - 1``, as in :func:`result_cf`; on a point issued at
    the valuation date row ``t = 0`` is the notes' issue-month row, and on a point issued
    later the rows before issue are zeros.  The ``loan_bal_pp`` column is the
    end-of-month balance ``L(t)``.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_prem": [av_pp_at(t, BEF_PREM) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "av_pp_bef_fee": [av_pp_at(t, BEF_FEE) for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "net_amt_at_risk": [net_amt_at_risk(t) for t in ts],
            "coi_pp": [coi_pp(t) for t in ts],
            "mth_deduction_pp": [mth_deduction_pp(t) for t in ts],
            "av_pp_bef_inv": [av_pp_at(t, BEF_INV) for t in ts],
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "ncsv_pp": [ncsv_pp(t) for t in ts],
            "loan_bal_pp": [loan_bal_pp(t) for t in ts],
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

EOM = 7

DEATH = 0

LAPSE = 1

MATURITY = 2

issue_age_min = 18

omega_age = 120

charges_cease_age = 121

guar_rate_ann = 0.02

crediting_rate_curr = 0.04

coi_curr_factor = 0.6

expense_pol_mth = 7.5

expense_unit_mth_1 = 0.26

expense_unit_mth_2 = 0.156

expense_unit_step_year = 10

loan_rate_ann = 0.0275

wd_fee = 25.0

wd_free_rate = 0.1

wd_first_year = 1

mort_ae_factor = 1.0

lapse_shock_mult = 2.0

lapse_dyn_slope = 5.0

lapse_dyn_threshold = 0.01

lapse_dyn_cap = 3.0

lapse_rate_cap = 0.35

expense_acq = 0.0

expense_maint = 75.0

inflation_rate = 0.025

premium_tax_rate = 0.025

pd = ("Module", "pandas")