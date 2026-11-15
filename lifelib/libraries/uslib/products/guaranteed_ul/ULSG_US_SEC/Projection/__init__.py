# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.ULSG_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.ULSG_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is:
``Projection[4]`` is an ItemSpace projecting the table's fifth row, model point 5,
``ULSG_US_S``'s worked-example cell restated 81 months on, in force 381 months at the
valuation date and one month into its grace, and :func:`point_id` is its label::

    >>> Projection[0].result_av()          # point 1, the worked example, at t = 0..4
    >>> Projection[4].result_guar()        # the grace running out at the valuation date
    >>> Projection[4].point_id()           # 5, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, and an int set on a float Reference reads as a float
(``products/guaranteed_ul/model-sec.md``, *What it refuses*).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.ULSG_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.ULSG_US_S` is rewritten where it depends on the month its frame opens at, where it
must answer for a month outside cover, or where it reads a table at a policy year, an
attained age or an anniversary; every other is :mod:`~.ULSG_US_S`'s own, but for the
funding-premium solve, which is not in this model (see the model docstring).
``products/guaranteed_ul/model-sec.md`` lists the rewritten cells with the reason for
each. Making it compile changed how each cell reads its inputs and spells its codes, and
no number: every model point attribute a projection cell uses is read as a number from a
``Data`` vector, every table as an array indexed by integers, every timing, kind and
status is an int code (*Codes*, below), :mod:`~.ULSG_US_S`'s ``coi_rate_scale``, a
Series, is a schedule number, :func:`coi_schedule`, and :mod:`~.ULSG_US_S`'s
``claims(t, kind=None)`` is three cells and their total, written as Python's compensated
``sum`` (:func:`claims`). The one call into Python a compiled cell keeps is ``round``,
in :func:`coi_rate` and :func:`sg_coi_rate`, on a point that pins its precision.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/guaranteed_ul/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``ULSG_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers live in the unparameterized :mod:`~.ULSG_US_SEC.Data` Space, reached here
through the ``data`` Reference, so each file is read once per model rather than once
per model point. The seven assumption tables are the files :mod:`~.ULSG_US_S` reads,
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
surr_charge_file        data.surr_charge_table()          surr_charge_table.csv
rop_file                data.rop_table()                  rop_table.csv
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
later, at most ten years later. Everything contractual reads it: the premium months and
the ten-pay years, the single premium and acquisition in the issue month, the first-year
acquisition load, the withdrawals from the second policy year, the surrender charge's
month, the return-of-premium windows at the 20th and 25th policy anniversaries, the COI
scale, the mortality rate and the corridor factor at the attained age, the base lapse
rate by policy year, and the end of premiums and charges at attained age 121. The policy
year is the 1-based contractual label ``policy_year(t) = duration(t) + 1`` and the
attained age (ANB) is ``age(t) = age_at_entry() + duration(t)``, both derived and never
indexed by. Point 1, ``ULSG_US_S``'s worked-example cell, is in policy year 26 at
attained age 85 at ``t = 0``, and point 9, to be issued 25 months after the valuation
date, is issued at ``t = 25``.

``ULSG_US_S`` already counts its months from the start of its own projection rather than
from issue, and opens its in-force point 1 there with its account value, its shadow
account, its loan and its premiums to date. What the valuation clock adds is that
``t = 0`` is one instant for every point, that a point may be issued after it, and that a
point in force brings in what its past has left it: the months it has already spent in
its grace, one more opening value than ``ULSG_US_S`` reads.

The economic inputs read the valuation clock. The declared credited rate,
:func:`crediting_rate_ann`, is read at ``t``, and is flat as shipped. Expense inflation is
``inflation_factor(t) = (1 + inflation_rate)^(t // 12)``, ``ULSG_US_S``'s step by policy
year moved onto ``t``, so that the maintenance expense is in valuation-date dollars for
every point alike; it is 2.5% a year as shipped. Mortality improvement runs from the
valuation date, as ``ULSG_US_S``'s runs from the start of its own projection: a year of it
accrues on each anniversary of the valuation date, ``t = 12, 24, ...``, for at most 20
years, in the same months for every point of a block, each year's at the rate graded at
the attained age a year before; and a point written after the valuation date takes the
improvement of the years before its issue (:func:`mort_improve_factor`). Acquisition is
charged per policy issued, from the issue month, and is not inflated, as in
``basiclife.BasicTerm_SE``. The model point's two pins, ``prem_persistency_override`` and
``coi_rate_dp``, are rules of the point, which hold in every month.

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.ULSG_US_S` computes: every cell the two share agrees at every argument
:mod:`~.ULSG_US_S` evaluates in its sweep, but for three whose meaning changed,
``pols_if_init``, now the count already in force at the valuation date, ``model_point``,
a row of another table, and ``result_pols``, which gains the month's new business.
``tests/test_model_conventions.py`` asserts it cell by cell. On point 1,
:mod:`~.ULSG_US_S`'s in-force point, the projection is :mod:`~.ULSG_US_S`'s too, month for
month, from ``t = 0``: it opens with :mod:`~.ULSG_US_S`'s own opening balances, and its
one new column, the months in grace, holds what :mod:`~.ULSG_US_S` assumes there, none.
Only the expenses differ, and the cells that sum them: ``ULSG_US_S`` inflates the
maintenance expense from the policy's issue, 25 years before, and this model from the
valuation date. That is how the worked example's five months, which
:mod:`~.ULSG_US_S`'s tests assert at ``t = 0..4`` on point 1, carry over: every premium,
charge, interest credit, account value, shadow account and status of them.

The **value** state variables are closing balances at the end of month ``t``:
``av_pp(t)``, ``sg_pp(t)`` and ``loan_bal_pp(t)``, and ``cum_prem_pp(t)``, the premiums
paid after the premium of month ``t``. The opening value is the ``BEF_PREM`` timing of
:func:`av_pp_at` and :func:`sg_pp_at` and the ``BEF_INT`` timing of
:func:`loan_bal_pp_at`, which is the previous month's closing balance, and at
:func:`t_entry`, the first month on the books, the model point's opening state instead, so
that nothing is ever asked for a month before the valuation date or before issue. For a
point in force the opening state is five columns of its row, per policy, as the policy
stands at the start of month 0, before any month-0 event: the account value, the shadow
account, the loan and the premiums paid to date, ``ULSG_US_S``'s own columns
(:func:`av_pp_init`, :func:`sg_pp_init`, :func:`loan_bal_init`, :func:`cum_prem_init`), and
the months already spent in the grace period (:func:`grace_mth_init`), which
``ULSG_US_S`` reads as 0 at the start of its frame. For a point issued at or after the
valuation date every one of them is 0, and the issue values come from the formulas, 0
for all five, as in ``ULSG_US_S``. The notes' ``av_init``, ``sg_init``, ``loan_init`` and
``cumprem_init`` are these opening values, and ``l_0`` is the count the point opens with
(see *Counts*, below).

Every chain is one cell a month. Each opening timing forms the previous month's close
itself, from its own value at ``t - 1`` and month ``t - 1``'s premium, withdrawal,
charges, cost of insurance and interest, the same operations in the same order as the
closing cell ``ULSG_US_S`` calls for, rather than calling for it: the account value's,
where ``ULSG_US_S``'s chain ran through six cells a month, the shadow account's, through
six, and the loan's, through two. The premiums to date, the grace counter with its lapse
latch, and the count call themselves at ``t - 1``, one cell a month, as ``ULSG_US_S``'s
do; the mortality improvement factor calls itself a year back, one cell a year. A
compiled model runs these chains on the C stack.

Within each month the notes' monthiversary order is followed exactly. The ten steps below
are numbered apart from the notes' twelve: the notes' step 6, the insufficiency test, is
the seventh here.

1. status check -- a policy whose 61-day grace has expired lapses at BOM with no value
   (:func:`is_lapsed`, :func:`grace_mth`);
2. premium, its two loads and the cumulative premium (:func:`premium_pp`,
   :func:`prem_to_av_pp`, :func:`prem_to_sg_pp`, :func:`cum_prem_pp`);
3. expense charges on both accounts and the withdrawal and its fee
   (:func:`maint_fee_pp`, :func:`sg_maint_fee_pp`, :func:`wd_pp`, :func:`wd_fee_pp`)
   -- after which the account value is the notes' ``AV'(t)``,
   :func:`av_pp_at(t, BEF_COI)<av_pp_at>`, and the shadow value its ``SG'(t)``;
4. death benefit and the GPT corridor test (:func:`db_pp`);
5. the net amount at risk on both accounts, each the death benefit discounted one
   month at *that account's* credited rate less *that account's* balance floored at
   zero (:func:`net_amt_at_risk`, :func:`sg_net_amt_at_risk`);
6. cost of insurance on both accounts (:func:`coi_pp`, :func:`sg_coi_pp`);
7. the insufficiency test: if the account value cannot carry the deduction, the
   shortfall is either **forgone by the insurer** while the guarantee stands
   (:func:`mth_deduction_forgone_pp`, :func:`is_guar_supported`) or opens the grace
   period (:func:`is_shortfall`, :func:`grace_mth`);
8. end of month: interest on the post-deduction balance of each account
   (:func:`inv_income_pp`, :func:`sg_inv_income_pp`) and loan interest accrual
   (:func:`loan_bal_pp`);
9. the in-force test ``SG - L > 0`` (:func:`is_guar_active`, :func:`sg_net_pp`) and
   the catch-up requirement it implies (:func:`catch_up_prem_pp`);
10. end of month: decrements, death first, then surrender, then return-of-premium
    exercise (:func:`pols_death`, :func:`pols_lapse`, :func:`pols_rop`).

Cash flows are **undiscounted**. Premiums and expenses fall at BOM and are weighted by
``pols_if(t)``; death claims by ``pols_if(t) * mort_rate_mth(t)``; surrender payments
by ``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``; refunds by the same
survivors times ``rop_rate(t)``. Loads, charges, interest credits and **every
shadow-account entry** are internal transfers, not cash flows: the shadow account is
notional and never payable [S2][S3], so it has per-policy cells only and no in-force
weighted counterparts.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, BEF_DECR)``, the
count carried in from ``t - 1`` (``BEF_NB``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, and before issue
(:func:`is_active`) every count, and so every cash flow, is zero, and so is every value
state. ``ULSG_US_S`` already names three timings, in a cell that returns ``pols_if(t)``
for each and that nothing calls. ``BEF_DECR`` keeps that meaning, and so does
``BEF_MAT``, the count before any maturity, since nothing matures: the name keeps its
S model's meaning, as in the family's other models, and ``basiclife.BasicTerm_SE``'s
start-of-month ``BEF_MAT`` is not adopted. ``BEF_NB`` is the one timing this model
gives a new meaning, ``basiclife.BasicTerm_SE``'s, and it differs from ``ULSG_US_S``'s
only in the issue month, where it counts the issued policies as new business, not yet
in. Inside the month the decrements are :mod:`~.ULSG_US_S`'s, in its order: death, then
surrender, then return-of-premium exercise, then, in the month before a grace expires,
every policy left, which ends the count at 0 from the next month.

.. rubric:: The end of the projection

The frame ends at :func:`charges_cease_mth`, the policy month at attained age 121,
where premiums and charges cease, and not at an event of the contract, whose cover
continues [S7]. Lives can survive the last month wherever improvement has taken the
mortality rate at attained age 120 below the table's 1.0. Improvement accrues over the
first 20 years from the valuation date, at the shipped 1% a year to attained age 85,
graded to 0 at 95, so on the committed points the rate at 120 is 0.817907 of the table's
on the four issued at or after the valuation date, at age 60, whose 20 years all fall
below 85, and nearer the table's on those in force there, whose 20 years start at an
older age: 0.899924 on point 6, valued at attained age 80, 0.946302 on points 1 and 7, at
85, and 0.990035 on point 5, at 91. Point 8, valued in its last month, at 120, dies at the
table's 1.0, with no improvement yet, and carries no survivor. The roll-forwards read the
survivors: :func:`check_av_roll_fwd` and :func:`av_change` read the opening account value
in force of month ``t + 1``, which in the last month is ``t = proj_len()``, and
:func:`pols_lapse_grace` reads the lapse latch of month ``t + 1``. So the three opening
values they read there, the count (the ``BEF_NB`` timing of :func:`pols_if_at`, and
through it :func:`pols_if`), the account value (``av_pp_at(t, BEF_PREM)``) and the latch
(:func:`is_lapsed`), are defined for ``0 <= duration_mth(t) <= charges_cease_mth()``: on
the books, and in the month after the frame, where they are the survivors of the last
month, the account value they carry and the latch the last month leaves. Each equals
:mod:`~.ULSG_US_S`'s value there exactly.
Every other cell is zero or false there, as before issue: each account inside the month,
the shadow account and its opening value, the loan, every charge, premium, withdrawal,
decrement rate, decrement, claim and flow, the grace counter and the expenses, whose
maintenance would otherwise fall on the carried count; only the two clocks, the inputs
read on the valuation clock and the neutral 1.0 of the dynamic lapse multiplier hold
values there, and :func:`status` returns ``CEASED``. And nothing reads past
``t = proj_len()``: :func:`av_change`, :func:`pols_lapse_grace` and the residual cells of
the three checks, which read ``t + 1`` or are read beside cells that do, are zero
outside cover before they read it.

.. rubric:: Naming

Cell names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and this library's own
:mod:`.UL_US_S` -- the chassis this product is built on -- everywhere else.
Names introduced in ``ULSG_US_S`` are the ones guaranteed UL genuinely adds: the shadow
account (``sg_*``), the guarantee tests, the grace counter, the forgone deduction and the
return-of-premium endorsement.

What running in force adds is named as ``basiclife.BasicTerm_SE`` names it:
``duration_mth`` read from the model point, ``policy_count``, ``pols_new_biz``,
``pols_if_at`` with its ``BEF_NB`` timing, ``is_active`` and ``result_pols``.
``t_entry``, the first month on the books, is the SEC models' own, and
``charges_cease_mth`` is named for ``charges_cease_age``, where the projection ends. A
column of the opening state is the cell it opens with ``_init`` added: ``av_pp_init``,
``sg_pp_init``, ``loan_bal_init`` and ``cum_prem_init`` are ``ULSG_US_S``'s own, and
``grace_mth_init`` opens :func:`grace_mth` as they open theirs. A table read at an
attained age has one reader keyed by the age, ``<cell>_at(a)``, a table read at a policy
year one keyed by the year, ``<cell>_py(y)``, and the return-of-premium table, read at a
policy anniversary, readers keyed by the anniversary, ``<cell>_anniv(y)``; the monthly
cell keeps ``ULSG_US_S``'s name and calls its reader inside cover. The surrender-charge
schedule, keyed by its ID, has one reader for each of its two columns,
:func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`, and the COI scale,
keyed by sex and class, is numbered, :func:`coi_schedule`, with its first and last ages,
:func:`coi_rate_first_age` and :func:`coi_rate_last_age`. A check's residual in month t
is ``<check>_resid(t)``. The premium pattern a monthly cell branches on is read through
bool decodes, one for each value, named for the value: :func:`is_level_premium`,
:func:`is_single_premium` and :func:`is_ten_pay_premium`; :func:`premium_freq` is the mode
as a number, as ``ULSG_US_S``'s is. No projection cell reads text: ``Data`` decodes each
column into its flags or its number, and joins the class factor, the COI scale and the
surrender-charge schedule to the points by their text keys, so ``ULSG_US_S``'s label
accessors, ``sex``, ``rate_class``, ``premium_type``, ``premium_mode`` and
``surr_charge_id``, are kept for reporting alone (*Reporting cells*, below). The premium
persistency pin is read once a point, a value and whether the point gives one:
:func:`prem_persistency_override` and :func:`has_prem_persistency_override`. Each of
``ULSG_US_S``'s claim kinds that pays is a cell, ``claims_<kind>(t)``, and :func:`claims`
their total, as in the family's other compiled models.

The technical notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Months from the valuation
                                                           date, 0-based
(months at valuation)      duration_mth_init               Completed policy months at the
                                                           valuation date; -k if issued k
                                                           months later
duration_months + t        duration_mth(t)                 Completed policy months at
                                                           month t
y                          policy_year(t)                  Policy year, 1-based
(y - 1)                    duration(t)                     Completed policy years
issue_age                  age_at_entry                    Issue age (ANB)
x_t                        age(t)                          Attained age (ANB)
sex                        sex                             Sex, M or F
risk_class                 rate_class                      Underwriting class [S4]
proj_len                   proj_len                        Months from the valuation date
                                                           to the end of the projection
(projection end)           charges_cease_mth               Policy month the projection
                                                           ends at, attained age 121
(none)                     point_id                        The point's label
(none)                     t_entry                         First month on the books
(none)                     is_active(t)                    Whether month t is in cover
(none)                     policy_count                    Policies the model point
                                                           stands for
face_amount, F             sum_assured                     Initial face amount
(none)                     sum_assured_at(t)               Face amount in month t
(units)                    units(t)                        Face in $1,000 units
guarantee_age              guarantee_age                   Elected guarantee age
premium_pattern            premium_type                    LEVEL / SINGLE / TEN_PAY
(LEVEL pattern)            is_level_premium                Whether premium_type is LEVEL
(SINGLE pattern)           is_single_premium               Whether it is SINGLE
(TEN_PAY pattern)          is_ten_pay_premium              Whether it is TEN_PAY
annual_premium             premium_pp_ann                  Scheduled premium
premium_mode               premium_mode, premium_freq      Payment mode, per year
(premium month)            is_premium_mth(t)               A premium falls due
phi_t                      prem_persistency(t)             Premium persistency
(persistency pin)          prem_persistency_override       The point's phi, NaN where
                                                           blank
(pin given)                has_prem_persistency_override   Whether the point pins phi
P_t                        premium_pp(t)                   Premium received at BOM
pi                         load_prem_rate                  Base premium load, 25%
pi^g                       load_prem_rate_sg               Shadow premium load, 8%
(1-pi) P_t                 prem_to_av_pp(t)                Net premium to the AV
(1-pi^g) P_t               prem_to_sg_pp(t)                Net premium to the shadow
CumPrem_t                  cum_prem_pp(t)                  Cumulative premiums
cumprem_init               cum_prem_init                   Premiums paid entering
                                                           month 0
W_t                        wd_pp(t)                        Withdrawal
(planned W)                wd_pp_mth                       The wd_pp column, a month's W
(25 fee)                   wd_fee_pp(t)                    Withdrawal fee
e_pol                      expense_pol_mth                 Per-policy charge
e_u                        expense_unit_mth                Base per-unit charge
e_u^g                      expense_unit_mth_sg             Shadow per-unit charge
rc(t)                      rider_charge_pp(t)              Rider charges (0)
(e_pol + e_u F/1000 + rc)  maint_fee_pp(t)                 Base non-COI charges
(e_u^g F/1000)             sg_maint_fee_pp(t)              Shadow non-COI charges
DB_t                       db_pp(t)                        Death benefit
kappa(x)                   corridor_factor(t)              GPT corridor factor
(kappa by age)             corridor_factor_at(a)           The same, keyed by age
NAAR_t                     net_amt_at_risk(t)              Base net amount at risk
NAAR_t^g                   sg_net_amt_at_risk(t)           Shadow net amount at risk
(NAAR factors)             naar_factor, sg_naar_factor     1 + j_g, 1 + j^g
(guaranteed max scale)     coi_schedule                    The number of the point's
                                                           annual COI scale
(scale's first age)        coi_rate_first_age              The scale's first attained age
(scale's last age)         coi_rate_last_age               The scale's last attained age
(annual max by age)        coi_rate_guar_at(a)             The scale's rate at age a
m_t^max                    coi_rate_guar(t)                Guaranteed max monthly COI
m_t                        coi_rate(t)                     Current monthly COI rate
m_t^g                      sg_coi_rate(t)                  Shadow monthly COI rate
(scale precision)          coi_rate_dp                     Quoting precision per $1,000
COI_t                      coi_pp(t)                       Base cost of insurance
COI_t^g                    sg_coi_pp(t)                    Shadow cost of insurance
MD_t                       mth_deduction_pp(t)             Base monthly deduction
(shadow MD)                sg_deduction_pp(t)              Shadow monthly deduction
D_t                        mth_deduction_forgone_pp(t)     Deduction forgone
(deduction taken)          mth_deduction_taken_pp(t)       Deduction actually taken
AV_{t-1}                   av_pp_at(t, BEF_PREM)           Opening AV, entering month t
(after premium)            av_pp_at(t, BEF_WD)             Before the withdrawal
(after withdrawal)         av_pp_at(t, BEF_FEE)            Before the expense charges
AV_t'                      av_pp_at(t, BEF_COI)            After the expense charges
AV_t''                     av_pp_at(t, BEF_INV)            After COI, floored at zero
AV_t                       av_pp(t)                        Account value, EOM
av_init                    av_pp_init                      Account value entering
                                                           month 0
(aggregate AV)             av_at(t, timing)                Account value in force
(none)                     av_change(t)                    Change in account value
SG_{t-1}                   sg_pp_at(t, BEF_PREM)           Opening SG, entering month t
SG_t'                      sg_pp_at(t, BEF_COI)            Shadow after the charges
SG_t''                     sg_pp_at(t, BEF_INV)            Shadow after COI, no floor
SG_t                       sg_pp(t)                        Shadow value, EOM
sg_init                    sg_pp_init                      Shadow account entering
                                                           month 0
SG_t - L_t                 sg_net_pp(t)                    The in-force test quantity
(in-force test)            is_guar_active(t)               SG_t - L_t > 0
(step 6 test)              is_guar_supported(t)            SG_t'' - L_{t-1} > 0
C_t                        catch_up_prem_pp(t)             Catch-up premium required
j_c                        inv_return_mth(t)               Monthly credited rate
j_g                        guar_rate_mth()                 Monthly guaranteed rate
j^g                        sg_rate_mth()                   Monthly shadow rate
(interest)                 inv_income_pp(t)                Interest credited to the AV
(shadow interest)          sg_inv_income_pp(t)             Interest credited to SG
L_{t-1}                    loan_bal_pp_at(t, BEF_INT)      Opening loan, entering month t
L_t                        loan_bal_pp(t)                  Loan balance, EOM
loan_init                  loan_bal_init                   Loan entering month 0
SC_t                       surr_charge_pp(t)               Surrender charge scheduled
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
(initial SC per $1,000)    surr_charge_rate_max            The schedule's charge before
                                                           any run-off
(run-off period)           surr_charge_runoff_years        The schedule's run-off, years
(AV - SC)                  csv_pp(t)                       Cash surrender value
CSV_t                      ncsv_pp(t)                      Net cash surrender value
(SC retained)              surr_charge(t)                  Surrender charge collected
g_t                        grace_mth(t)                    Months in grace
(grace at valuation)       grace_mth_init                  Months in grace entering
                                                           month 0
(grace trigger)            is_shortfall(t)                 The deduction attempt fails
(cure payment)             cure_premium_pp(t)              Payment curing the grace
(lapse for insufficiency)  is_lapsed(t)                    Terminated in grace
(Status column)            status(t)                       The notes' status, a code;
                                                           its label in result_av
rop_elected                rop_elected                     Endorsement elected [S1]
rho                        rop_ratio(t)                    ROP refund ratio
w^ROP                      rop_rate(t)                     ROP exercise rate
(ROP window)               rop_anniversary(t)              20, 25 or 0
(window anniversary)       is_rop_anniv(y)                 Whether a window follows
                                                           anniversary y
(rho by anniversary)       rop_ratio_anniv(y)              rho at anniversary y
(w^ROP by anniversary)     rop_rate_anniv(y)               w^ROP at anniversary y
q_t^d                      mort_rate_mth(t)                Monthly mortality rate
(annual q)                 mort_rate(t)                    Annual mortality rate, capped
(base q by age)            mort_rate_base_at(a)            The base table's rate
(improvement)              mort_improve_rate(t)            Annual improvement rate
(improvement factor)       mort_improve_factor(t)          Cumulative improvement
b(d)                       lapse_rate_base(t)              Base annual lapse rate
(b by year)                lapse_rate_base_py(y)           The same, keyed by policy year
G                          lapse_rate_guar_mult()          Lifetime-guarantee factor
Phi                        lapse_rate_pattern_mult()       Premium-pattern factor
Psi_t                      lapse_rate_dyn_mult(t)          Funding-status factor
(annual w)                 lapse_rate(t)                   Total annual lapse rate
w_t                        lapse_rate_mth(t)               Monthly lapse rate
l_t                        pols_if(t)                      In force at BOM of month t
(l at valuation)           pols_if_init                    In force at the valuation date
(none)                     pols_if_at(t, BEF_NB)           Carried in from month t - 1
(none)                     pols_if_at(t, BEF_DECR)         After new business: l_t
(none)                     pols_if_at(t, BEF_MAT)          Before maturity: l_t
(none)                     pols_new_biz(t)                 Policies issued in month t
(deaths)                   pols_death(t)                   Deaths in month t
(surrenders)               pols_lapse(t)                   Surrenders in month t
(ROP exercises)            pols_rop(t)                     Refund exercises
(grace lapse)              pols_lapse_grace(t)             Terminations in grace
(none)                     pols_maturity(t)                Maturities: always zero
(premium income)           premiums(t)                     Premium income
(claims CF)                claims(t)                       Death, surrender and refund
                                                           claims
(death CF)                 claims_death(t)                 Death claims
(surrender CF)             claims_lapse(t)                 Surrender payments
(ROP CF)                   claims_refund(t)                Refund payments
(withdrawal CF)            withdrawals(t)                  Withdrawal payments
(expenses)                 expenses(t)                     Insurer expenses
(none)                     premium_taxes(t)                Percent-of-premium: zero
NetCF                      net_cf(t)                       Net liability cash flow
(none)                     check_av_roll_fwd_resid(t)      AV roll-forward residual
(none)                     check_sg_roll_fwd_resid(t)      Shadow roll-forward residual
(none)                     check_margin_resid(t)           Margin identity residual
(none)                     result_pols()                   Counts and decrement rates
=========================  ==============================  ==========================

Ten names needed care.

The notes' ``risk_class`` is this model's ``rate_class`` -- the name ``Term_US_S`` and
:mod:`.UL_US_S` both use for the underwriting class, and the one the model point
table column carries, so the notes' word appears nowhere in the model. It is the only
model point attribute renamed on cross-model grounds rather than for a reason internal
to this product.

``l_t`` in these notes is the in-force probability at the **beginning** of month ``t``
-- the notes weight every cash flow of month ``t`` by ``l_t`` and roll forward with
``l_{t+1} = l_t (1 - q^d)(1 - w)(1 - w^ROP)`` -- so it maps straight onto
``pols_if(t)`` with no offset, which follows ``BasicTerm_S`` and is the number in force at
the start of month ``t``, after the month's new business. On a point issued at ``t = 0``,
``pols_if(0)`` is the issued count, the notes' ``l_0``, while ``pols_if_init()`` is 0, the
count already in force at the valuation date; on a point in force the two are one count.
The notes' roll-forward is the ``pols_if_at(t + 1, BEF_NB)`` step.

``grace_mth_init`` is the one opening value ``ULSG_US_S`` does not read. Its grace
counter reads the month before its frame as 0, which is right for a policy issued there
and for the notes' worked example, which is not in grace, and wrong for a policy restated
in its grace: read so, the restated policy would lapse a month late. It is an int, a
count of whole months, as ``ULSG_US_S``'s counter is.

The account value measured for the net amount at risk is ``AV'(t)``, which in these
notes is the balance **after the expense charges and before the cost of insurance** --
``av_pp_at(t, BEF_COI)``. The universal life chassis measures it before the entire
monthly deduction, ``av_pp_at(t, BEF_FEE)``. The guaranteed-UL notes flag the
difference as a deliberate deviation; it is immaterial at the modelled charge levels
but it is real, and ``BEF_COI`` exists so that the two models can be reconciled
without reading the formulas.

The notes' ``CSV_t = max(AV_t - SC_t - L_t, 0)`` already nets policy debt, so it is
this model's :func:`ncsv_pp`, not its :func:`csv_pp`. :func:`csv_pp` is the chassis'
``AV - SC`` floored at zero, and keeping both means the surrender-charge and the
indebtedness offsets can be read separately.

``D_t`` is the monthly deduction the insurer **forgoes** because the account value is
exhausted while the guarantee stands. It is not a receivable and must never accrue
against future premiums or account value recoveries -- treating it as one understates
the guarantee cost, which the notes list among the pitfalls.
:func:`mth_deduction_forgone_pp` therefore feeds nothing but the diagnostics, and
:func:`mth_deduction_taken_pp` -- what actually left the account -- is what the
account value roll-forward and the margins use.

The guarantee is tested twice at slightly different points, and the notes use the same
words for both. :func:`is_guar_supported` is the step-6 test ``SG''_t - L_{t-1} > 0``,
which decides whether a failed deduction is forgone or opens the grace period;
:func:`is_guar_active` is the step-9 in-force test ``SG_t - L_t > 0``, measured after
the shadow interest credit and the loan accrual. Running the second before the
deduction attempt -- the notes' "order of tests" pitfall -- shifts claim timing at
exactly the durations where the net amount at risk is the whole death benefit.

``maint_fee_pp`` is the notes' non-COI monthly *charge* against the account value and
is therefore insurer income, following ``CashValue_SE.maint_fee``. :func:`expenses` is
something different -- the insurer's own **[std]** acquisition, maintenance and claim
expense, a cash flow. The two must not be confused: ``maint_fee`` is income,
``expenses`` is outgo.

A partial withdrawal is **not a claim**. It is a payment the owner elects to take out
of a policy that stays in force, not an event that terminates one, so it is
:func:`withdrawals` and a ``withdrawals`` column of :func:`result_cf`, and no
``claims_<kind>`` cell carries it, where ``ULSG_US_S``'s ``claims(t, "WITHDRAWAL")``
raises ``ValueError("invalid kind")``. :func:`claim_pp` keeps its ``WITHDRAWAL`` branch,
because the per-policy amount is what :func:`withdrawals` weights, and
:func:`claims_from_av` keeps its own, because a withdrawal does release account value;
only the *claim* total, :func:`claims`, excludes it, and must not double-count it.

:func:`coi_rate_dp` is the one place where the notes' worked example and the notes'
own rule disagree by more than rounding; see its docstring and
``products/guaranteed_ul/model.md``. It is a pin of the point, as
``prem_persistency_override`` is, and holds in every month.

.. rubric:: Codes

What :mod:`~.ULSG_US_S` spells as text, a timing, a kind or a status, is here an int
Reference named as the text it replaces, so that every cell takes and returns C numbers.
A call site reads as it did, less the quotes: ``pols_if_at(t, BEF_DECR)``,
``av_pp_at(t, BEF_COI)``, ``loan_bal_pp_at(t, BEF_INT)``, ``claim_pp(t, DEATH)``.

==================  =====  ==========================================================
Reference           Value  Meaning
==================  =====  ==========================================================
BEF_NB              0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR            1      :func:`pols_if_at`: that count plus month t's new business
BEF_MAT             2      :func:`pols_if_at`: before any maturity, the BEF_DECR count
BEF_PREM            3      :func:`av_pp_at`, :func:`sg_pp_at`, :func:`av_at`: the
                           balance carried in
BEF_WD              4      the same three: after the net premium
BEF_FEE             5      the same three: after the withdrawal (and, on the account,
                           its fee)
BEF_COI             6      the same three: after the expense charges
BEF_INV             7      the same three: after the cost of insurance
EOM                 8      :func:`av_at`: after the interest credit, before decrements
BEF_INT             9      :func:`loan_bal_pp_at`: the loan carried in, before the
                           month's interest
DEATH               0      :func:`claim_pp`, :func:`claims_from_av`: the death claim
LAPSE               1      the same two: the surrender claim
REFUND              2      the same two: the return-of-premium refund
GRACE               3      the same two: a termination in grace, which pays nothing;
                           and the status :func:`status` gives a month in grace
WITHDRAWAL          4      the same two: the withdrawal, which is not a claim
MATURITY            5      :func:`claims_from_av`: none, the contract never matures
PRE_ISSUE           0      :func:`status`: before issue
IN_FORCE            1      :func:`status`: ``ULSG_US_S``'s ``"IN FORCE"``
IN_FORCE_GUARANTEE  2      :func:`status`: ``ULSG_US_S``'s ``"IN FORCE - GUARANTEE"``
LAPSED              4      :func:`status`: lapsed in grace
CEASED              5      :func:`status`: past the end of the projection
==================  =====  ==========================================================

The model has three families of timing, the count's, the two accounts' and the loan's,
passed to different cells, and they are numbered as one: ``BEF_NB`` 0 and ``BEF_DECR``
1, as in every SEC model, then the count's third, ``BEF_MAT``, then the accounts' in the
order of their instants within the month, ``EOM`` last, then the loan's one,
``BEF_INT``, the balance before the month's interest, which ``ULSG_US_S`` keys apart
from any instant of the accounts' month. So no two timings share a code, and a code of
one family passed to another's cell, ``av_pp_at(t, BEF_NB)`` or
``loan_bal_pp_at(t, BEF_PREM)``, is refused as any timing the cell does not take is,
``ValueError("invalid timing")``, in both engines, rather than read as a timing of the
cell's own. Kinds are numbered in ``ULSG_US_S``'s order of the month's decrements, the
grace lapse fourth, then the two that are not decrements. Statuses are numbered in the
order of a policy's life, so that grace is fourth there too: ``ULSG_US_S`` spells the
kind and the status alike, ``"GRACE"``, and one Reference, ``GRACE``, 3, serves both.
Two of ``ULSG_US_S``'s statuses are not names, ``"IN FORCE"`` and
``"IN FORCE - GUARANTEE"``; their codes join the words with underscores, the hyphen
dropped, and :func:`result_av` writes ``ULSG_US_S``'s labels back in its ``status``
column. A code a cell takes indexes that cell's cache, a C array of ten codes a month for
each of the seven cells that take one, since every 2-D cache of the model has one width
(``spec_sec.py``), so codes are numbered densely from 0. They are References, not cells,
so the symbol map does not list them. Every other Reference is named in lower case,
``issue_age_min`` and ``charges_cease_age`` among them, two of the contract's bounds that
the compiled model's caches are sized from (:func:`proj_len`).

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`sex`, :func:`rate_class`,
:func:`premium_type`, :func:`premium_mode` and :func:`surr_charge_id`, the reports
:func:`result_cf`, :func:`result_pols`, :func:`result_av` and :func:`result_guar`, and the
checks :func:`check_av_roll_fwd`, :func:`check_sg_roll_fwd` and :func:`check_margin` are
written for a reader and for the comparison with :mod:`~.ULSG_US_S`, which has every one
of them: a table row, text, DataFrames and three verdicts. No other cell calls them: each
reads the number ``Data`` decoded from the same column instead, the decodes' flags, the
schedules and the joins the keys select. So the row, the text and the frames stay Python
when the model compiles. A label accessor returns its column as read, text or not: a
blank ``surr_charge_id`` on a point without a charge reads as NaN, and a column of
numbers as ints, and the compiled accessor returns the same. Every other cell returns a C
``bint``, ``long long`` or ``double``, and so do the three checks, which may stay Python
but compile to a ``bint``, their verdict, as their per-month residuals, ``*_resid``,
compile to a ``double``.
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
    """The issue age (ANB) of the selected model point.

    Read from ``Data.age_at_entry``, at the point's position, ``idx``.
    """
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point.

    A reporting cell (the Space docstring): ``Data`` joins the COI scale by it, through
    :func:`coi_schedule`, and no projection cell reads it here.
    """
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point (four NT, two tobacco) [S4].

    A reporting cell (the Space docstring): ``Data`` joins the class factor and the COI
    scale by it, through :func:`class_factor` and :func:`coi_schedule`, and no projection
    cell reads it here.
    """
    return model_point()["rate_class"]


def sum_assured():
    """F: the initial face amount of the selected model point [S4][S6].

    Read from ``Data.sum_assured``, at the point's position, ``idx``.
    """
    return float(data.sum_assured()[idx])                            # noqa: F821


def guarantee_age():
    """The elected secondary-guarantee age, any attained age from 90 to 121 [S1][S2][S9].

    121 is the lifetime election, which is what the anchor cell carries and what
    switches :func:`lapse_rate_guar_mult` to the 0.55 multiplier [R7].

    Read from ``Data.guarantee_age``, at the point's position, ``idx``.
    """
    return int(data.guarantee_age()[idx])                            # noqa: F821


def premium_type():
    """The premium pattern: ``"LEVEL"``, ``"SINGLE"`` or ``"TEN_PAY"`` **[std]**.

    A first-class model point attribute because funding pattern drives both the
    guarantee trajectory and observed lapse behaviour [R8].

    A reporting cell (the Space docstring): ``Data`` decodes it into the three flags
    :func:`is_level_premium`, :func:`is_single_premium` and :func:`is_ten_pay_premium`, and
    no projection cell reads it here.
    """
    return model_point()["premium_type"]


def is_level_premium():
    """Whether the premium pattern is LEVEL: ``premium_type`` is ``"LEVEL"``.

    One of the three flags ``Data`` decodes from the model point's ``premium_type``
    column, ``Data.is_level_premium`` at the point, which :func:`is_premium_mth`,
    :func:`prem_persistency`, :func:`premium_pp` and :func:`lapse_rate_pattern_mult`
    branch on, so that no projection cell compares text; each of those cells raises on a
    point that is none of the three, as ``ULSG_US_S``'s do.  ``Data`` compares the text
    exactly, as ``ULSG_US_S`` does, so ``"level"`` is no pattern.  The label accessor
    :func:`premium_type` is kept as it is, for reporting, and no projection cell calls it.
    """
    return bool(data.is_level_premium()[idx])                        # noqa: F821


def is_single_premium():
    """Whether the premium pattern is SINGLE: ``premium_type`` is ``"SINGLE"``.

    ``Data.is_single_premium`` at the point, decoded as :func:`is_level_premium` is, and
    read by :func:`is_premium_mth`, :func:`premium_pp` and :func:`lapse_rate_pattern_mult`.
    """
    return bool(data.is_single_premium()[idx])                       # noqa: F821


def is_ten_pay_premium():
    """Whether the premium pattern is TEN_PAY: ``premium_type`` is ``"TEN_PAY"``.

    ``Data.is_ten_pay_premium`` at the point, decoded as :func:`is_level_premium` is, and
    read by :func:`is_premium_mth` and :func:`lapse_rate_pattern_mult`.
    """
    return bool(data.is_ten_pay_premium()[idx])                      # noqa: F821


def premium_mode():
    """The premium mode: ``"A"``, ``"S"``, ``"Q"`` or ``"M"`` (EFT only) [S2].

    A reporting cell (the Space docstring): ``Data`` decodes it into the payments a year
    :func:`premium_freq` returns, and no projection cell reads it here.
    """
    return model_point()["premium_mode"]


def premium_pp_ann():
    """The scheduled annual premium per policy, or the single premium for ``"SINGLE"``.

    An input fixed at issue, read from the model point, as ``basiclife.BasicTerm_SE``
    reads its premium from a table: a policy in force at the valuation date pays the
    premium it was issued on, whatever its shadow account stands at now.  For the anchor
    cell this is the notes' solved level no-lapse premium ``P* = 10,800`` **[std]**.  The
    solve itself is ``ULSG_US_S``'s, a side calculation its projection never reads, and it
    is not in this model (see the model docstring).

    Read from ``Data.premium_pp_ann``, at the point's position, ``idx``.
    """
    return float(data.premium_pp_ann()[idx])                         # noqa: F821


def load_prem_rate():
    """pi: the base premium expense charge, 25% of every premium, all years [S3][S7].

    Contractual here, unlike the universal life chassis where the load is a
    non-guaranteed element; it sits in the model point table for the same reason it
    does there, so that the table alone describes the policy.

    Read from ``Data.load_prem_rate``, at the point's position, ``idx``.
    """
    return float(data.load_prem_rate()[idx])                         # noqa: F821


def av_pp_init():
    """av_init: the base account value per policy entering month 0, 0 before issue.

    The ``av_pp_init`` column, ``ULSG_US_S``'s own: the balance at the close of policy
    month ``duration_mth_init() - 1``, before any month-0 event, which is what
    ``ULSG_US_S`` carries into the month as ``av_pp_at(d, BEF_PREM)`` at
    ``d = duration_mth_init()``.  It is the opening balance of :func:`av_pp_at` at
    :func:`t_entry`; ``av_pp(0)`` is the balance at the **end** of ``t = 0``.  ``Data``
    holds it to 0 or more: no policy in force holds a negative account value, and the one
    way ``ULSG_US_S`` carries it below 0, a loan on an exhausted account, is restated no
    later than the last month it is still 0 or more (see :func:`inv_income_pp`).  Zero for
    a point not yet in force.

    Read from ``Data.av_pp_init``, at the point's position, ``idx``.
    """
    return float(data.av_pp_init()[idx])                             # noqa: F821


def sg_pp_init():
    """sg_init: the shadow account value per policy entering month 0, 0 before issue.

    The ``sg_pp_init`` column, ``ULSG_US_S``'s own: the shadow balance at the close of
    policy month ``duration_mth_init() - 1``, before any month-0 event, which is what
    ``ULSG_US_S`` carries into the month as ``sg_pp_at(d, BEF_PREM)``; the opening
    balance of :func:`sg_pp_at` at :func:`t_entry`.  The shadow account is state, carried in
    its own column like the account value, not a path a model could recompute from issue.
    Not floored anywhere in the projection, and ``Data`` takes it of either sign: a
    negative shadow balance measures the catch-up shortfall, and flooring it destroys
    :func:`catch_up_prem_pp`.  Point 5, the worked-example cell restated in its grace,
    opens at -1,365.21.  Zero for a point not yet in force.

    Read from ``Data.sg_pp_init``, at the point's position, ``idx``.
    """
    return float(data.sg_pp_init()[idx])                             # noqa: F821


def loan_bal_init():
    """loan_init: the policy loan per policy entering month 0, 0 in every shipped point.

    The ``loan_bal_init`` column, ``ULSG_US_S``'s own: the loan at the close of policy
    month ``duration_mth_init() - 1``, interest accrued to then included, before any
    month-0 event, which is what ``ULSG_US_S`` carries into the month as
    ``loan_bal_pp_at(d, BEF_INT)``; the opening balance of :func:`loan_bal_pp_at` at
    :func:`t_entry`.  ``Data`` holds it to 0 or more.  Zero for a point not yet in force.

    Read from ``Data.loan_bal_init``, at the point's position, ``idx``.
    """
    return float(data.loan_bal_init()[idx])                          # noqa: F821


def cum_prem_init():
    """cumprem_init: the premiums already paid per policy entering month 0.

    The ``cum_prem_init`` column, ``ULSG_US_S``'s own.  The notes make this a model point
    attribute because it drives the return-of-premium refund [S1] and the 7-pay test
    [R5].  For the anchor cell it is the 25 annual premiums of $10,800 implied by the
    in-force snapshot **[std]**.  It is the balance *before* the premium of month 0, the
    close of policy month ``duration_mth_init() - 1``, ``ULSG_US_S``'s ``cum_prem_pp(d -
    1)``: ``cum_prem_pp(t_entry()) = cum_prem_init() + premium_pp(t_entry())``.  Premiums
    only, withdrawals not netted, so ``Data`` holds it to 0 or more.  It moves no number
    until a return-of-premium window, where it is the refund's base: on point 1 the 25th
    window falls at ``t = 0``, and the refund there is the 40%-of-face cap, 200,000.00,
    where an opening of 0 would refund 10,800.00.  Zero for a point not yet in force.

    Read from ``Data.cum_prem_init``, at the point's position, ``idx``.
    """
    return float(data.cum_prem_init()[idx])                          # noqa: F821


def grace_mth_init():
    """g at the valuation date: the months already spent in grace entering month 0.

    The ``grace_mth_init`` column, an int: the grace counter at the close of policy month
    ``duration_mth_init() - 1``, ``ULSG_US_S``'s ``grace_mth(d - 1)``, which
    :func:`grace_mth` reads as ``g_{t-1}`` in the first month on the books,
    :func:`t_entry`, where ``ULSG_US_S`` reads 0.  0 for a policy not in grace, and for one
    not yet in force.  A policy in its grace carries the months it has spent there, so
    that its grace expires on time: point 5, the worked-example cell restated at policy
    month 381 in its grace, carries 1, advances it to 2 in month 0 and lapses at
    ``t = 1``, where read as 0 it would lapse a month late.  A counter carried in resets in
    the first month whose deduction no longer fails, as when a scheduled premium falls due
    and carries it, as it would have in ``ULSG_US_S``.  ``Data`` holds it to a whole number,
    0 or more, and :func:`proj_len` refuses one at or past ``grace_months``: that grace
    expired before the valuation date, and the policy lapsed then, with no value.

    Read from ``Data.grace_mth_init``, at the point's position, ``idx``.
    """
    return int(data.grace_mth_init()[idx])                           # noqa: F821


def policy_count():
    """The number of policies the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the policies in force then, before any
    month-0 event; any other point counts the policies it issues.  Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second.  Every per-policy value -- the
    two accounts, the loan, the premiums to date, the grace counter -- is the same whatever
    the count, and every cash flow is a per-policy amount weighted by it.

    Read from ``Data.policy_count``, at the point's position, ``idx``.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """l_0 at the valuation date: the policies in force there, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose policies
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``.  So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count.  ``ULSG_US_S``'s cell of the name is the notes'
    ``l_0``, the count at the start of its frame, which on new business is the issued
    count.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 300 for point 1, the notes' worked-example
    cell, whose policy months 301-305 are ``t = 0`` to ``t = 4``; 381 for point 5, the
    same cell restated 81 months on; 0 for a policy issued at the valuation date; and -25
    for point 9, to be issued 25 months after it, which ``Data`` admits up to
    ``future_horizon_mth`` months ahead.  This is the notes' ``duration_months``, an
    elapsed count and therefore already 0-based, and ``ULSG_US_S``'s cell and column of the
    same name, which count from the first month of its own projection; here that month is
    the valuation date for every point, and the count may be negative.  It is the one fact
    the policy clock takes from the model point.

    Read from ``Data.duration_mth``, at the point's position, ``idx``.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point.

    ``Data.has_surr_charge`` at the point: 1 where the column reads True, in any case,
    which ``Data`` holds to True or False.
    """
    return bool(data.has_surr_charge()[idx])                         # noqa: F821


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*.

    A reporting cell (the Space docstring): ``Data`` joins the schedule by it, through
    :func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`, and no projection
    cell reads it here.  Returned as read: a blank id on a point without a charge is NaN,
    and a column of numbers reads as ints.
    """
    return model_point()["surr_charge_id"]


def surr_charge_rate_max():
    """The schedule's charge per $1,000 of initial face, before any of it runs off.

    ``Data.surr_charge_rate_max`` at the point: the ``sc_per_1000_init`` column of the
    point's row of *surr_charge_table.csv*, $18.00 on the shipped ``GUL15`` schedule;
    :func:`surr_charge_rate` runs it off from here.  ``Data`` joins the schedule to the
    points by ``surr_charge_id`` once it has checked the table, so that no projection cell
    reads the table or the id, and refuses the table, naming every point, where a point
    that :func:`has_surr_charge` names an id the table lacks, which ``ULSG_US_S``'s ``.loc``
    met in every month of its cover.  :func:`surr_charge_rate` reads it only where
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
    """The number of years over which the schedule's charge runs off, linearly.

    ``Data.surr_charge_runoff_years`` at the point: the ``runoff_years`` column of the
    point's row of *surr_charge_table.csv*, 15 on the shipped ``GUL15`` schedule, read as
    a float, as ``ULSG_US_S`` reads it, and joined, checked and refused as
    :func:`surr_charge_rate_max` is; ``Data`` holds it to a whole number of years, 1 or
    more, so that the division in :func:`surr_charge_rate` never meets 0.
    """
    years = float(data.surr_charge_runoff_years()[idx])              # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise KeyError(f"point_id {point_id()}: surr_charge_table.csv has no schedule "
                       f"for its surr_charge_id")
    return years


def rop_elected():
    """Whether the return-of-premium endorsement applies [S1].

    Built into the representative contract, so it is on for every point but the one
    that switches it off to isolate the guarantee mechanics.  ``Data.rop_elected`` at the
    point: 1 where the column reads True, in any case, which ``Data`` holds to True or
    False.
    """
    return bool(data.rop_elected()[idx])                             # noqa: F821


def prem_persistency_override():
    """The model point's premium persistency pin, a number, or NaN where blank.

    ``Data.prem_persistency_override`` at the point, so that :func:`prem_persistency`, a
    monthly cell, reads no model point column in its own formula.  Read only where
    :func:`has_prem_persistency_override` is true, which decides, never the value; ``Data``
    holds the column to blank or a number from 0 to 1, a probability, and keeps a blank as
    NaN, as ``ULSG_US_S`` reads it.  Point 1, the worked example, pins it at
    1.00, and so does point 5, the same policy restated 81 months on; every other shipped
    point leaves it blank.  A rule of the point, not state: it holds in every month, so a
    point restated in force or written later keeps its S point's value.
    """
    return float(data.prem_persistency_override()[idx])              # noqa: F821


def has_prem_persistency_override():
    """Whether the model point pins its premium persistency.

    ``Data.has_prem_persistency_override`` at the point: 1 where the
    ``prem_persistency_override`` column holds a number, 0 where it is blank, a flag
    decoded once for the table, so that :func:`prem_persistency` tests a flag rather than
    a missing value.
    """
    return bool(data.has_prem_persistency_override()[idx])           # noqa: F821


def coi_rate_dp():
    """Decimal places the declared COI scales are quoted to per $1,000; -1 = exact.

    **The one place where the notes' rule and the notes' worked example disagree by
    more than rounding.**  The rule is that the current scale is 65% and the shadow
    scale 55% of the guaranteed maximum, which at the worked example's
    ``m^max = 8.615`` gives 5.59975 and 4.73825.  The worked example is computed with
    5.60 and 4.74 -- the same figures rounded to the cent per $1,000, which is how the
    notes quote them -- and the difference is about $0.12 a month of base deduction and
    $0.65 of shadow deduction, an order of magnitude more than the cent-level rounding
    that explains the rest of that table.

    Rather than pick one, the model ships both.  A model point that leaves this column
    blank takes the rule at full precision; the worked-example anchor sets it to 2 and
    holds both declared scales to the cent per $1,000, which is a perfectly ordinary
    way for an admin system to carry a rate table and reproduces the notes' table.

    ``Data.coi_rate_dp`` at the point: the column, which ``Data`` holds to blank or a whole
    number, 0 or more, below ``2**53``, with -1 where it is blank, ``ULSG_US_S``'s own
    "exact".  :func:`coi_rate` and :func:`sg_coi_rate` round only where it is 0 or more.
    """
    return int(data.coi_rate_dp()[idx])                              # noqa: F821


def duration_mth(t):
    """Completed policy months at the beginning of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together.  A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame.  It is 0 in the issue month, ``t = 0`` for a
    point issued at the valuation date, 300 in the first month of the notes' worked
    example, and negative before issue.  Note the contrast with the contractual policy
    month *number*, which counts the current month as well and is ``duration_mth(t) + 1``;
    see :func:`surr_charge_rate`.
    """
    return duration_mth_init() + t


def duration(t):
    """Completed policy years at the beginning of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year, and negative before issue.  The ten-pay years and
    the return-of-premium anniversaries count it.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y: the policy year containing month t, ``duration(t) + 1``, 1-based.

    A contractual label -- policy year 1 is the twelve months from issue -- used to look
    up the base lapse rate and to charge the first-year acquisition load, and never the
    frame index.  It is 0 or less before issue, where no table is read by it: each reader
    is called inside cover only (:func:`is_active`).
    """
    return duration(t) + 1


def age(t):
    """x_t: the attained age (ANB) in month t, ``age_at_entry() + duration(t)``.

    Age advances on the policy anniversary, not on the birthday, which is the ANB
    convention the whole model is built on **[std]**.  Mixing an ALB basis into the
    COI or mortality lookups shifts both by up to half a year of mortality, which the
    notes list among the pitfalls.  Before issue it is the age the cohort to be issued has
    reached, below the issue age: no table is read at it there, but
    :func:`mort_improve_rate` grades the improvement of the years before issue at it (see
    :func:`mort_improve_factor`).
    """
    return age_at_entry() + duration(t)


def charges_cease_mth():
    """The policy month at which the projection ends, the first at attained age 121.

    ``12 * (charges_cease_age - age_at_entry())``: 732 at issue age 60.  Premiums and all
    charges cease at attained age 121 [S7], so the last month of the frame,
    ``charges_cease_mth() - 1``, is the last at attained age 120.  It is ``ULSG_US_S``'s
    frame from issue, counted on the policy clock; :func:`proj_len` counts from the
    valuation date instead.  The contract has no maturity date and its cover continues
    past attained age 121 [S7], so where lives survive the last month, the count, the
    account value and the lapse latch they carry into this month are kept (see
    :func:`pols_if_at`).  The cell is named for the Reference ``charges_cease_age`` that
    ends the frame, as ``ULSG_US_S``'s frame ends there: no value of it puts the cessation
    inside the frame, since the frame ends where the charges do.
    """
    return 12 * (charges_cease_age - age_at_entry())


def proj_len():
    """The number of months from the valuation date to the end of the projection.

    ``charges_cease_mth() - duration_mth_init()``: 732 for a policy issued at age 60 at
    the valuation date, 432 for point 1, in force 300 months, and 757 for point 9, issued
    25 months after the valuation date.  The frame is ``t = 0, 1, ..., proj_len() - 1``;
    ``proj_len()`` is its exclusive end, the row count of every result table, and
    ``proj_len() - 1`` is the frame's last month, the last at attained age 120: the
    notes' maximum projection length, to attained age 121, where premiums and all charges
    cease.  Coverage continues past that point under the contract [S7], and lives can
    survive it wherever improvement has taken the mortality rate at attained age 120 below
    the table's 1.0, as it has on every committed point but point 8, valued in its last
    month, where it has not yet begun (see the Space's docstring), so the count, the account
    value and the lapse latch the survivors carry into ``t = proj_len()`` are kept (see
    :func:`charges_cease_mth`).

    Four kinds of point have no frame the contract issues, and raise here, naming the
    point, rather than projecting, each checked in this order:

    * one to be issued at or past attained age 121, which would never be in cover,
      ``charges_cease_mth() <= 0``, so that a point issued past it is refused by this rule
      whenever it is to be issued;
    * one at or past the end of the projection at the valuation date;
    * one whose grace expired before the valuation date, ``grace_mth_init() >=
      grace_months``, which lapsed then, with no value;
    * one issued below ``issue_age_min``, 18, the youngest issue age ``product-spec.md``
      admits.  ``ULSG_US_S`` projects any age its tables serve, and the shipped COI scale
      none below 45, but the compiled model's caches are sized from the contract
      (``spec_sec.py``), so a younger point, whose frame, policy years and attained ages
      run longer, would read past them.  Checked last, so that a point that breaks an
      earlier rule too keeps that rule's message.

    An in-force extract should carry none of them.  These are rules of the product, read
    from this Space's References, where ``Data`` checks the table.  ``charges_cease_age``
    and ``issue_age_min`` are two of the three bounds the compiled caches are sized from,
    with ``Data.future_horizon_mth``.
    """
    if charges_cease_mth() <= 0:
        raise ValueError(
            f"point_id {point_id()}: age_at_entry {age_at_entry()} "
            f"is at or past charges_cease_age, {charges_cease_age}: "    # noqa: F821
            f"a policy issued there would never be in cover")
    n = charges_cease_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past the end of the projection, policy month "
            f"{charges_cease_mth()}, attained age {charges_cease_age}")    # noqa: F821
    if grace_mth_init() >= grace_months:                              # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: grace_mth_init {grace_mth_init()} "
            f"is at or past grace_months, {grace_months}: the grace "    # noqa: F821
            f"expired before the valuation date, so the policy lapsed then, with "
            f"no value")
    if age_at_entry() < issue_age_min:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is below "
                         f"issue_age_min, {issue_age_min}")           # noqa: F821
    return n


def t_entry():
    """The first month the policy is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later.  It is the base of every recursion: the count, the account value,
    the shadow account, the loan, the premiums to date and the grace counter all open
    there, from the model point's opening state on a point in force and from the issue
    values on any other.  No cell in cover reads a month before it but the mortality
    improvement factor, an input on the valuation clock, which a point written later reads
    at the years before its issue (see :func:`mort_improve_factor`).
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and inside the projection.

    ``0 <= duration_mth(t) < charges_cease_mth()``, false before issue and from
    ``t = proj_len()`` on.  Outside cover every count, balance, charge, premium,
    withdrawal, decrement rate, decrement, claim and flow is zero, every flag false and
    the grace counter and the return-of-premium anniversary 0, and no table is read at a
    policy year, an attained age or an anniversary the policy does not have; the clocks and
    the inputs read on the valuation clock keep their values, the dynamic lapse multiplier
    its neutral 1.0, and :func:`status` says why.  The three exceptions are the opening
    values of the month after the frame, the count, the account value and the lapse latch
    carried into ``t = proj_len()``, which the roll-forwards read (see :func:`pols_if_at`,
    :func:`av_pp_at` and :func:`is_lapsed`).
    """
    return 0 <= duration_mth(t) < charges_cease_mth()


def sum_assured_at(t):
    """F(t): the face amount in month t; zero outside cover.

    Level: face increases are not permitted [S2] and elective decreases, option
    changes and the face reduction some designs attach to a withdrawal are not
    modelled -- the notes' withdrawal reduces the account and shadow balances only.
    So the face in force is the face at issue in every month, and needs no opening
    column.  The cell is kept so the chassis' shape is unchanged and a design with face
    movement can specialise it.
    """
    return sum_assured() if is_active(t) else 0.0


def units(t):
    """U: the face amount in $1,000 units, ``sum_assured_at(t) / 1000``.

    Both per-unit charges are quoted per $1,000 of **initial** face per month, and the
    surrender charge per $1,000 of initial face; with a level face they coincide.
    """
    return sum_assured_at(t) / 1000


def crediting_rate_ann(t):
    """i^c: the current declared annual effective credited rate, 3.50% **[std]**.

    A non-guaranteed element declared at insurer discretion within the guaranteed
    bounds and governed by ASOP 2 [REG-R26].  The base run holds the snapshot scale
    level, as the notes prescribe; re-rating is out of scope.  An economic input, read on
    the **valuation** clock: month ``t`` of the rate is the same month for every point,
    however old the policy, as ``ULSG_US_S`` reads it at the month of its own projection.
    """
    return crediting_rate_curr


def inv_return_mth(t):
    """j_c: the monthly credited rate, ``(1 + i^c)^(1/12) - 1``, floored at j_g.

    0.0028709 at the **[std]** 3.50% current rate, matching the notes.  The floor is
    the contractual 2.0% guaranteed minimum [S3][S5][S7]; it does not bind at the
    snapshot scale.  Read at month t of the valuation clock, as the declared rate is, and
    the floor written second, as ``ULSG_US_S`` writes it, so that a rate that is not a
    number stays one.
    """
    return max((1 + crediting_rate_ann(t)) ** (1 / 12) - 1, guar_rate_mth())


def guar_rate_mth():
    """j_g: the monthly guaranteed rate, ``(1 + i_guar)^(1/12) - 1`` = 0.0016516."""
    return (1 + guar_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def sg_rate_mth():
    """j^g: the monthly shadow credited rate, ``(1 + i^g)^(1/12) - 1`` = 0.0044717.

    5.5% annual effective **[std]**, comfortably below the AG 38 8E cap of a
    Moody's-composite-yield index plus 3% that classifies a Design #1 shadow account
    [R1], and well above the 2.0% base guarantee -- which is what makes the guarantee
    outlive the cash value.
    """
    return (1 + sg_rate_ann) ** (1 / 12) - 1                         # noqa: F821


def naar_factor():
    """The base NAAR factor, ``1 + j_g`` = 1.0016516.

    The death benefit is discounted one month at the **guaranteed** rate, never the
    credited rate.  Using the undiscounted death benefit instead changes the cost of
    insurance by about 0.17% a month at the 2% guarantee, which the notes list first
    among the pitfalls; the same convention must hold on both accounts.
    """
    return 1 + guar_rate_mth()


def sg_naar_factor():
    """The shadow NAAR factor, ``1 + j^g`` = 1.0044717 **[std]**.

    The shadow account discounts the death benefit at *its own* credited rate, which
    is what the notes' step 4 writes, so the two accounts see different net amounts at
    risk even before their balances diverge.
    """
    return 1 + sg_rate_mth()


def loan_rate_mth():
    """The monthly charged loan rate, ``(1 + r_L)^(1/12) - 1`` at r_L = 5.0% [S4].

    Charged in arrears [S3] [S7] and guaranteed [S4]; monthly accrual is the model's
    discretization **[std]**.
    """
    return (1 + loan_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def loan_cr_rate_mth():
    """The monthly rate credited on the loaned account value, 3.0% annual [S4].

    Guaranteed, and 200 basis points below the charged rate -- the contractual loan
    spread.
    """
    return (1 + loan_cr_rate_ann) ** (1 / 12) - 1                    # noqa: F821


def premium_freq():
    """Scheduled premium payments per policy year, from the ``premium_mode`` column [S2].

    Annual 1, semi-annual 2, quarterly 4, monthly (EFT only) 12.  Non-annual modes
    carry modal factors in the source design; no carrier publishes them, so the
    scheduled annual premium is divided evenly **[std]** and every shipped model point
    is annual.  ``Data.premium_freq`` at the point: ``Data`` decodes the mode's text
    there, element by element, comparing it exactly as ``ULSG_US_S`` does, so that no
    projection cell compares text; the label accessor :func:`premium_mode` is kept as it
    is, for reporting, and no projection cell calls it.  A mode it does not know, ``"a"``
    or a blank among them, ``Data`` decodes to 0, which raises here, ``ULSG_US_S``'s
    message, where the mode is read: so a SINGLE point, which never asks its mode,
    projects whatever its mode, as in ``ULSG_US_S``.  The element is compared, and
    ``int`` of it returned, rather than held in a local first, which a formula that also
    raises would keep a Python object compiled.
    """
    if data.premium_freq()[idx] == 0:                                # noqa: F821
        raise ValueError("invalid premium mode")
    return int(data.premium_freq()[idx])                             # noqa: F821


def is_premium_mth(t):
    """Whether a scheduled premium falls due at BOM of month t; False outside cover.

    ``"LEVEL"``
        every ``12 / premium_freq()`` months from issue;
    ``"SINGLE"``
        the issue month only;
    ``"TEN_PAY"``
        as ``"LEVEL"``, for the first ``ten_pay_years`` policy years **[std]**.

    Each is read on the policy clock, ``duration_mth(t)`` and ``duration(t)``, so a point
    valued mid-year pays on its own anniversaries.  The pattern is read through its
    decodes, :func:`is_level_premium`, :func:`is_single_premium` and
    :func:`is_ten_pay_premium`, and a pattern none of them knows raises, as in
    ``ULSG_US_S``.
    """
    if not is_active(t):
        return False
    if is_single_premium():
        return duration_mth(t) == 0
    elif is_ten_pay_premium():
        if duration(t) >= ten_pay_years:                             # noqa: F821
            return False
    elif not is_level_premium():
        raise ValueError("invalid premium type")
    return duration_mth(t) % (12 // premium_freq()) == 0


def prem_persistency(t):
    """phi_t: the probability the scheduled premium is actually paid **[std]**.

    98% a year for a level payer, 100% for single-pay and ten-pay, which is what the
    notes prescribe; a missed premium is never made up, so it permanently lowers the
    shadow trajectory, and catch-up behaviour is not modelled in the base run.

    The model point may override it, and the worked-example anchor overrides it to
    1.00.  That is not a tuning: the notes' worked example is a contract-mechanics
    view with the behavioural assumptions suppressed, and premium persistency is a
    class (c) behavioural assumption.  The notes are also not self-consistent about
    where phi belongs -- their cash flow list writes premium income as
    ``l_t phi_t P_t`` while their step 2 credits ``(1 - pi) P_t`` to the account, which
    would hand the account value more than the insurer received.  This model applies
    phi once, to the premium actually received, so the account value, the shadow
    account, the cumulative premium and the premium income all move together.

    The override is read once a point, a value and whether the point gives one,
    :func:`prem_persistency_override` and :func:`has_prem_persistency_override`, and the
    pattern through :func:`is_level_premium`.  It holds in every month, as in
    ``ULSG_US_S``.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if has_prem_persistency_override():
        return prem_persistency_override()
    return prem_persistency_ann if is_level_premium() else 1.0


def premium_pp(t):
    """P_t: the premium received per policy at BOM of month t.

    The scheduled premium in a premium month times :func:`prem_persistency`, zero
    otherwise, and zero from attained age 121 when premiums are no longer accepted
    [S7]: the frame ends there, so that branch is ``ULSG_US_S``'s and never taken in cover.
    Premiums are flexible in amount and timing after the first [S3] [S4]; the model
    projects the scheduled pattern, which is what the guarantee was solved on.  Zero
    outside cover.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    if not is_premium_mth(t):
        return 0.0
    if is_single_premium():
        return premium_pp_ann() * prem_persistency(t)
    return premium_pp_ann() / premium_freq() * prem_persistency(t)


def prem_to_av_pp(t):
    """The net premium credited to the base account value, ``(1 - pi) P_t`` [S3][S7]."""
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_sg_pp(t):
    """The net premium credited to the shadow account, ``(1 - pi^g) P_t`` **[std]**.

    The shadow load of 8% sits near the 7% market-wide load allowance AG 38 8B uses
    [R1] and far below the 25% base load, which is the whole point: the shadow account
    must credit premiums more generously than the real one for the guarantee to
    outlast the cash value.
    """
    return premium_pp(t) * (1 - load_prem_rate_sg)                   # noqa: F821


def prem_to_av(t):
    """Net premium credited to base account values, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """Premium income at BOM of month t, weighted by the in force at BOM."""
    return premium_pp(t) * pols_if(t)


def cum_prem_pp(t):
    """CumPrem_t: cumulative premiums paid per policy, after the premium of month t.

    ``CumPrem_{t-1} + P_t``, exactly as the notes write it, with ``CumPrem_{t-1}`` the
    model point's :func:`cum_prem_init` in the first month on the books, :func:`t_entry`:
    the premiums paid before the valuation date on a point in force, 0 at issue.  It calls
    itself at ``t - 1`` first, one cell a month.  Withdrawals do **not** reduce it here --
    that is the cumulative-premium-test variation's ``CumPrem^net``, not this one -- and it
    drives the return-of-premium refund [S1].  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = cum_prem_pp(t - 1) if t > t_entry() else cum_prem_init()
    return prev + premium_pp(t)


def wd_pp_mth():
    """The planned partial withdrawal per policy, in each month withdrawals are allowed.

    The model point's ``wd_pp`` column, a monthly amount, **0 in every shipped model
    point**: the notes set utilisation to zero in the base model and give no pattern, so
    the behaviour is left to the data **[std]**.  Read once a point here, so that
    :func:`wd_pp`, a monthly cell on the two accounts' chains, reads no model point column
    in its own formula.  ``Data`` holds it to 0 or more.

    Read from ``Data.wd_pp``, at the point's position, ``idx``.
    """
    return float(data.wd_pp()[idx])                                  # noqa: F821


def wd_pp(t):
    """W_t: the partial withdrawal per policy at BOM of month t.

    Available after policy year 1 [S3] [S4] [S7] and not from attained age 121
    **[std]**, where the frame ends.  The amount is the constant monthly figure in the
    model point's ``wd_pp`` column, :func:`wd_pp_mth`, **0 in every shipped model
    point**: the notes set utilisation to zero in the base model and give no pattern, so
    the mechanics are implemented and the behaviour is left to the data **[std]**.  A
    withdrawal reduces the account value by the amount plus the fee and the shadow account
    dollar-for-dollar, with no fee **[std]** (one observed design subtracts partial
    surrenders and their fees from its guarantee measure [S4]).  It is paid whatever the
    account can fund, as in ``ULSG_US_S``.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if duration_mth(t) < 12 * wd_first_year:                         # noqa: F821
        return 0.0
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return wd_pp_mth()


def wd_fee_pp(t):
    """The $25 withdrawal fee, charged only in a month with a withdrawal [S2][S3][S4][S7].

    Retained by the insurer, so it is account-value outgo but not a liability cash
    flow; it appears in :func:`margin_expense`, not in :func:`claims`.  It is charged
    against the base account only, never the shadow account.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force."""
    return wd_fee_pp(t) * pols_if(t)


def corridor_factor_at(a):
    """kappa: the GPT corridor factor at attained age a [R4][REG-R13], the table's reader.

    The IRC 7702(d)(2) applicable percentages, every row of them: 250% to attained age
    40, then decreasing by a ratable portion for each full year through the statute's
    breakpoints -- 215% at 45, 185% at 50, 150% at 55, 130% at 60, 120% at 65, 115% at
    70, 105% from 75 to 90 -- and 100% from attained age 95 on, which is the statute's
    last row.  ``Data.corridor_factor_array()`` at the age, the table padded from age 0,
    so that the age is the index.  Ages outside the table take its first or last row: the
    first and last ages ``data.corridor_age_first()`` and ``data.corridor_age_last()``
    give, which they read from the table's key column once the keys and the factors are
    checked, before any factor is read, the last first, since it runs the checks; so the
    padding below the first age is never read.  ``Data`` holds each factor to 0 or more,
    the statute's being 100% or more, and each age to 0 or more.  Keyed by the attained
    age, so the table is read once an age rather than once a month;
    :func:`corridor_factor` calls it inside cover only.
    """
    last = data.corridor_age_last()                                  # noqa: F821
    a = min(max(a, data.corridor_age_first()), last)                 # noqa: F821
    return float(data.corridor_factor_array()[a])                    # noqa: F821


def corridor_factor(t):
    """kappa(x_t): the GPT corridor factor at the attained age in month t [R4][REG-R13].

    Read at the attained age of month t by :func:`corridor_factor_at`; zero outside
    cover, before the table is read.  Because guaranteed UL account values are
    deliberately thin the corridor never binds in any shipped model point -- but it is the
    reason the death benefit is a ``max`` rather than the face amount.
    """
    return corridor_factor_at(age(t)) if is_active(t) else 0.0


def db_pp(t):
    """DB_t: the death benefit per policy, ``max(F, kappa(x_t) max(AV'_t, 0))`` [S2][S4].

    Level death benefit option only, the guarantee-focused segment's design [S2][S4].
    ``AV'_t`` is the account value after the premium, the withdrawal and the expense
    charges and **before** the cost of insurance, and it is floored at zero so that the
    corridor amount is never negative.  While every corridor factor is 0 or more and the
    face above 0, as ``Data`` holds them, that floor changes no death benefit: where
    ``AV'_t`` is below 0 the corridor's amount would be 0 or less without it, and the face
    wins either way.  Zero outside cover, before the corridor table is read.
    """
    if not is_active(t):
        return 0.0
    return max(sum_assured_at(t),
               corridor_factor(t) * max(av_pp_at(t, BEF_COI), 0.0))


def net_amt_at_risk(t):
    """NAAR_t: ``max(DB_t / (1 + j_g) - max(AV'_t, 0), 0)`` [S3].

    Two conventions here are the product's, not conveniences: the death benefit is
    discounted one month at the **guaranteed** rate (:func:`naar_factor`), and the
    account value is measured after the expense charges and before the cost of
    insurance.  The account input is floored at zero so that a deficit -- the
    guarantee-support regime, where the account is exhausted and the insurer is
    funding the deduction -- never inflates the net amount at risk above the
    discounted death benefit.  In that regime the cost of insurance is charged on
    essentially the whole face amount, which is what dominates late-duration
    guaranteed UL cash flows.
    """
    return max(0.0, db_pp(t) / naar_factor() - max(av_pp_at(t, BEF_COI), 0.0))


def sg_net_amt_at_risk(t):
    """NAAR_t^g: the shadow NAAR, ``max(DB_t / (1 + j^g) - max(SG'_t, 0), 0)``.

    The same construction as :func:`net_amt_at_risk` on the shadow parameter set
    **[std]**, discounting at the shadow credited rate and flooring the shadow balance
    at zero so that catch-up territory -- a negative shadow account -- does not inflate
    the shadow cost of insurance.  Zero outside cover, where the death benefit is.
    """
    return max(0.0, db_pp(t) / sg_naar_factor()
               - max(sg_pp_at(t, BEF_COI), 0.0))


def coi_schedule():
    """The number of this point's guaranteed COI scale, its row of ``Data.coi_rate_array``.

    ``Data.coi_schedule`` at this point: ``Data`` numbers each cell of *coi_rates.csv*,
    its ``sex`` and ``rate_class``, from 1 in the order of those keys, and gives each
    point the number of its own.  ``ULSG_US_S`` slices the scale, a Series, by the same
    two keys in ``coi_rate_scale``, which this replaces, since no compiled cell returns a
    Series.  Every point reads its scale in its first month in cover, so ``Data`` refuses
    the table at its first read, naming every point whose cell the scale lacks, where
    ``ULSG_US_S``'s slice raised ``KeyError`` as the point projected.
    """
    return int(data.coi_schedule()[idx])                             # noqa: F821


def coi_rate_last_age():
    """The last attained age of this point's guaranteed COI scale: its extent.

    ``Data.coi_rate_last_ages()`` at this point's :func:`coi_schedule`: a per-schedule
    extent, which ``Data`` reads from the table's key columns once it has checked the keys
    and the rates.  121 on the shipped anchor cell.
    """
    return int(data.coi_rate_last_ages()[coi_schedule()])            # noqa: F821


def coi_rate_first_age():
    """The first attained age of this point's guaranteed COI scale.

    ``Data.coi_rate_first_ages()`` at this point's :func:`coi_schedule`, read from the
    table's key columns as :func:`coi_rate_last_age` is: 45 on the shipped anchor cell.
    :func:`coi_rate_guar_at` refuses an age below it, where ``ULSG_US_S``'s scale has no
    row.
    """
    return int(data.coi_rate_first_ages()[coi_schedule()])           # noqa: F821


def coi_rate_guar_at(a):
    """The guaranteed maximum **annual** COI rate per $1,000 of NAAR at attained age a.

    The scale's one reader, keyed by the attained age: an illustrative **[std]** scale,
    not the 2017 CSO table [REG-R17].  ``Data.coi_rate_array()`` at the point's
    :func:`coi_schedule` and the age, each schedule padded from age 0, so that the age is
    the column.  Ages beyond the scale take its last row, :func:`coi_rate_last_age`, which
    is asked for first, so that a projection meets the check of the table first.  An age
    below the scale's first, :func:`coi_rate_first_age`, where ``ULSG_US_S``'s slice
    raised ``KeyError``, is refused, naming the point and the age, so that the padding is
    never read; :func:`proj_len` refuses an issue age below 18, and the shipped scale
    starts at 45, so a point issued younger than its scale is refused here, in its first
    month in cover.  :func:`coi_rate_guar` calls it inside cover only, and turns it
    monthly.
    """
    last = coi_rate_last_age()
    if a < coi_rate_first_age():
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no rate for the "
                         f"point's sex and rate_class at attained age {a}")
    return float(data.coi_rate_array()[coi_schedule(), min(a, last)])  # noqa: F821


def coi_rate_guar(t):
    """m_t^max: the guaranteed maximum **monthly** COI rate per $1,000 of NAAR.

    The annual rate from *coi_rates.csv*, :func:`coi_rate_guar_at` at the attained age of
    month t, divided by twelve -- the notes' simple-twelfth conversion, fixed **[std]**.
    It differs materially from ``1 - (1 - q)^(1/12)`` at ages 85 and over, where q exceeds
    0.10, and the notes are explicit that the two must not be mixed.  Model 585 requires
    the guaranteed maxima to be stated in the policy [R3]; carriers do not publish them, so
    the shipped scale is illustrative **[std]**, not the 2017 CSO table [REG-R17].  Zero
    outside cover, before the scale is read.
    """
    return coi_rate_guar_at(age(t)) / 12 if is_active(t) else 0.0


def coi_rate(t):
    """m_t: the current monthly COI rate, 65% of the guaranteed maximum **[std]**.

    Current COI scales are not published by any carrier, so the factor is a pure
    modelling assumption and one of the first things to sensitivity-test.  The scale
    is held to :func:`coi_rate_dp` decimals per $1,000, which reconciles the notes'
    worked example with the notes' own factor rule -- see :func:`coi_rate_dp`.

    The rounding is Python's ``round``, kept where ``ULSG_US_S`` has it: the rate is built
    from a Reference of this Space, ``coi_curr_factor``, which ``Data`` cannot read, so
    it cannot be rounded there ahead of the projection.  So this is the one call into
    Python a compiled cell makes, admitted in this cell and :func:`sg_coi_rate` alone
    (the registry's ``"python_calls"``), and made only on a point that pins the precision,
    where ``coi_rate_dp() >= 0``; it rounds the same double in both engines.
    """
    r = coi_curr_factor * coi_rate_guar(t)                           # noqa: F821
    dp = coi_rate_dp()
    return r if dp < 0 else round(r, dp)


def sg_coi_rate(t):
    """m_t^g: the shadow monthly COI rate, 55% of the guaranteed maximum **[std]**.

    Kept below the current base rate of 65% so the shadow account depletes more slowly
    than the real one and the guarantee keeps the policy in force after the account
    value is exhausted, which is the defining behaviour of the product [S2] [S7].
    Rounded like :func:`coi_rate`, by Python's ``round``, admitted here as there.
    """
    r = coi_sg_factor * coi_rate_guar(t)                             # noqa: F821
    dp = coi_rate_dp()
    return r if dp < 0 else round(r, dp)


def coi_pp(t):
    """COI_t: the base cost of insurance charge, ``m_t NAAR_t / 1000``.

    Zero from attained age 121, when all charges cease [S3][S7] -- the frame ends there,
    so that branch is ``ULSG_US_S``'s and never taken in cover -- and zero outside cover.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def sg_coi_pp(t):
    """COI_t^g: the shadow cost of insurance charge, ``m_t^g NAAR_t^g / 1000`` **[std]**.

    Notional: it never leaves the insurer and is not a cash flow.  Zero from attained
    age 121, when the shadow charges cease with the base ones **[std]**, which the frame
    ends at, and zero outside cover.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return sg_coi_rate(t) / 1000 * sg_net_amt_at_risk(t)


def rider_charge_pp(t):
    """Rider charges deducted monthly, 0 in the base model **[std]**.

    Rider charges are one of the sourced monthly charge categories [S2] [S4] [S9],
    but neither rider in scope carries one: the terminal illness accelerated benefit
    takes no premium [S9], and the return-of-premium endorsement is built into the
    representative contract rather than charged for [S1].  The term is carried, as it is
    on the universal life chassis, so that a rider module can be added without changing
    the recursion.
    """
    return 0.0


def maint_fee_pp(t):
    """The non-COI part of the base monthly deduction, ``e_pol + e_u U + rc`` [S3][S7].

    The $5.50 per-policy administrative charge [S3][S7], the $0.20 per $1,000 of initial
    face per month coverage charge **[std]** and rider charges.  Zero from attained age
    121, when charges cease [S3][S7], which the frame ends at, and zero outside cover.

    The name follows ``CashValue_SE.maint_fee``: this is a *charge* against the account
    value and therefore insurer income.  It is not :func:`expenses`, which is the
    insurer's own outgo.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return (expense_pol_mth + expense_unit_mth * units(t)            # noqa: F821
            + rider_charge_pp(t))


def sg_maint_fee_pp(t):
    """The non-COI part of the shadow monthly deduction, ``e_u^g U`` **[std]**.

    $0.05 per $1,000 of initial face per month and **no per-policy charge** -- the
    simplest representative choice, since no carrier publishes shadow parameters and
    AG 38 8E only describes shadow accounts as carrying expense charges [R1].  Zero from
    attained age 121, which the frame ends at, and zero outside cover.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return expense_unit_mth_sg * units(t)


def mth_deduction_pp(t):
    """MD_t: the full base monthly deduction scheduled at BOM, ``maint_fee + COI``.

    This is what the worked example's "Base deductions" column shows.  What actually
    leaves the account is :func:`mth_deduction_taken_pp`; the remainder is
    :func:`mth_deduction_forgone_pp`.
    """
    return maint_fee_pp(t) + coi_pp(t)


def sg_deduction_pp(t):
    """The full shadow monthly deduction, ``sg_maint_fee_pp + sg_coi_pp`` **[std]**.

    The worked example's "Shdw deductions" column.  The shadow account is never
    floored, so it is always taken in full -- there is no shadow analogue of the
    forgone deduction.
    """
    return sg_maint_fee_pp(t) + sg_coi_pp(t)


def maint_fee_taken_pp(t):
    """The part of :func:`maint_fee_pp` the account value could actually carry.

    The expense charges are deducted before the cost of insurance, so they are met
    first out of the balance standing after the premium and the withdrawal.
    """
    return min(maint_fee_pp(t), max(av_pp_at(t, BEF_FEE), 0.0))


def coi_taken_pp(t):
    """The part of :func:`coi_pp` the account value could actually carry.

    The cost of insurance is deducted last, so it absorbs the shortfall first: this is
    the term that goes unpaid in the guarantee-support regime.
    """
    return min(coi_pp(t), max(av_pp_at(t, BEF_COI), 0.0))


def mth_deduction_taken_pp(t):
    """The monthly deduction actually taken from the account value in month t."""
    return maint_fee_taken_pp(t) + coi_taken_pp(t)


def mth_deduction_forgone_pp(t):
    """D_t: the monthly deduction forgone because the account value is exhausted.

    ``MD_t - (what the account could carry)``, which equals the notes' ``-AV''_t``
    whenever the balance before the charges is non-negative.  While the guarantee
    stands (:func:`is_guar_supported`) the insurer simply funds it and coverage
    continues with the account value at zero; when the guarantee has failed the same
    shortfall opens the grace period instead.

    **It is not a receivable.**  It must never accrue against future premiums or
    account value recoveries -- the notes list that among the pitfalls, because
    treating it as one understates the guarantee cost.  Nothing in the projection
    reads this cell except the diagnostics and :func:`cure_premium_pp`.

    It reports the shortfall whenever there is one, which includes the grace months and
    the months after a lapse -- where the notes' ``D_t`` is not defined at all, the
    shortfall being their *required grace payment* instead, and where the zero floor
    above it is this model's own **[std]** extension (:func:`av_pp_at`).  Read it beside
    :func:`is_guar_supported`, not on its own.
    """
    return mth_deduction_pp(t) - mth_deduction_taken_pp(t)


def maint_fee(t):
    """Non-COI monthly charges actually deducted from account values, in force."""
    return maint_fee_taken_pp(t) * pols_if(t)


def coi(t):
    """Cost of insurance charges actually deducted from account values, in force."""
    return coi_taken_pp(t) * pols_if(t)


def mth_deduction(t):
    """Monthly deductions actually taken from account values, in force."""
    return mth_deduction_taken_pp(t) * pols_if(t)


def mth_deduction_forgone(t):
    """Monthly deductions forgone because the account value is exhausted, in force.

    While :func:`is_guar_supported` holds this is the running cost of the "negative
    account economics" regime the notes describe: the insurer is paying for coverage on
    a policy whose account value is zero.  In the grace months it is not -- there the
    shortfall is the notes' *required grace payment* on a policy about to terminate --
    so :func:`result_guar` prints it beside ``is_guar_active``.  After the lapse
    ``pols_if(t)`` is zero and so is this, whatever the per-policy cells say.
    """
    return mth_deduction_forgone_pp(t) * pols_if(t)


def av_pp_at(t, timing):
    """Base account value per policy at an intra-month point of month t.

    The BOM events change the balance in this order, and ``timing`` names the point
    just before each of them:

    ``BEF_PREM``
        Before the premium: the closing balance of the previous month, ``AV_{t-1}``,
        or the model point's opening balance :func:`av_pp_init` in the first month on
        the books, :func:`t_entry` -- the account value at the valuation date on a point
        in force, 0 at issue.  The previous month's close is formed here, its own value at
        ``t - 1`` through month ``t - 1``'s premium, withdrawal and fee, expense charges,
        cost of insurance, zero floor and interest, the same operations in the same order
        as ``ULSG_US_S``'s ``av_pp(t - 1)`` takes them, so the chain back to
        :func:`t_entry` is one cell a month, where ``ULSG_US_S``'s ran through six.  It is
        also defined in the month after the frame, ``t = proj_len()``, where it is the
        account value the survivors of the last month carry, which the roll-forward
        reads; zero before issue.

    ``BEF_WD``
        After the net premium, before the withdrawal.

    ``BEF_FEE``
        After the withdrawal and its fee, before the expense charges.

    ``BEF_COI``
        After the expense charges, before the cost of insurance.  **This is the notes'**
        ``AV'(t)``, and the balance the death benefit, the corridor test and the net
        amount at risk are all measured against.  The universal life chassis measures
        them one step earlier, at ``BEF_FEE``; the guaranteed-UL notes flag the
        difference as a deliberate deviation.

    ``BEF_INV``
        After the cost of insurance and **after the zero floor**, before interest.
        Interest is credited on this post-deduction balance; reversing the two
        overstates the account value by about one month's interest on the deduction
        every month.  The floor is what the guarantee buys: the account value stops at
        zero and the shortfall becomes :func:`mth_deduction_forgone_pp` rather than a
        negative balance.  It keeps ``ULSG_US_S``'s order, ``max(0.0, ...)``, the bound
        first.

        **Documented deviation [std].**  The notes floor the account value at zero
        *only while the guarantee is active* -- their step 6 sets ``AV''_t = 0`` in the
        guarantee branch and gives the grace branch no account-value recursion at all.
        This model applies the floor unconditionally, in the grace months and after a
        lapse as well.  A negative balance would break the account-value roll-forward,
        which closes on the deduction actually *taken*, and nothing is taken from an
        exhausted account.  No cash flow moves either way -- a policy in grace
        surrenders for nothing by construction and ``pols_if(t)`` is zero once it has
        lapsed -- but the per-policy account-value cells do keep running after the
        lapse, where they describe no policy.  See :func:`mth_deduction_forgone` and
        the section "The forgone deduction is the product" of
        ``products/guaranteed_ul/model.md``.

    The timings after ``BEF_PREM`` are zero outside cover, ``t = proj_len()`` included.
    The end-of-month balance ``AV_t`` is :func:`av_pp`.
    """
    if timing == BEF_PREM:
        if not 0 <= duration_mth(t) <= charges_cease_mth():
            return 0.0
        if t == t_entry():
            return av_pp_init()
        av = av_pp_at(t - 1, BEF_PREM) + prem_to_av_pp(t - 1)
        av = av - wd_pp(t - 1) - wd_fee_pp(t - 1)
        av = av - maint_fee_pp(t - 1)
        av = max(0.0, av - coi_pp(t - 1))
        loaned = loan_bal_pp_at(t - 1, BEF_INT)
        return av + ((av - loaned) * inv_return_mth(t - 1)
                     + loaned * loan_cr_rate_mth())
    elif timing == BEF_WD:
        if not is_active(t):
            return 0.0
        return av_pp_at(t, BEF_PREM) + prem_to_av_pp(t)
    elif timing == BEF_FEE:
        return av_pp_at(t, BEF_WD) - wd_pp(t) - wd_fee_pp(t)
    elif timing == BEF_COI:
        return av_pp_at(t, BEF_FEE) - maint_fee_pp(t)
    elif timing == BEF_INV:
        return max(0.0, av_pp_at(t, BEF_COI) - coi_pp(t))
    else:
        raise ValueError("invalid timing")


def inv_income_pp(t):
    """Interest credited to the base account value at EOM of month t.

    The unloaned part of the post-deduction balance earns the current monthly rate and
    the loaned part the guaranteed loaned rate of 3.0% [S4]::

        (AV''_t - L_{t-1}) x j_c + L_{t-1} x loan_cr_rate_mth()

    where ``L_{t-1}`` is the opening loan balance ``loan_bal_pp_at(t, BEF_INT)``.
    With the account value exhausted and no loan the credit is zero, which is why the
    worked example shows no interest from policy month 304 (``t = 3`` on the anchor).
    With a loan on an exhausted account the unloaned part is below zero, and at the
    shipped rates, the loaned rate below the current one, so is the credit: the account
    value closes the month below zero, as in ``ULSG_US_S``, which is why ``Data`` asks a
    point in force to be restated no later than the last month its account value is still
    zero or more.  Zero outside cover.
    """
    loaned = loan_bal_pp_at(t, BEF_INT)
    unloaned = av_pp_at(t, BEF_INV) - loaned
    return unloaned * inv_return_mth(t) + loaned * loan_cr_rate_mth()


def av_pp(t):
    """AV_t: the base account value per policy at the end of month t.

    The floored post-deduction balance plus one month's interest, for every ``t`` of
    the frame including the first month on the books; the opening balance
    :func:`av_pp_init` enters through ``av_pp_at(t_entry(), BEF_PREM)``, not through a
    seed row here.  An exhausted account never goes negative and the shortfall is recorded
    as :func:`mth_deduction_forgone_pp` instead, but for the loan's interest split (see
    :func:`inv_income_pp`).

    Floored at zero *throughout* -- in grace and after a lapse as well as under a live
    guarantee.  The notes floor it "only while the guarantee is active"; applying the
    floor unconditionally is a **[std]** deviation that moves no cash flow but does
    leave this cell running after the policy has gone.  :func:`av_pp_at` sets out why.
    Zero outside cover.
    """
    return av_pp_at(t, BEF_INV) + inv_income_pp(t)


def av_at(t, timing):
    """Base account value in force at an intra-month point of month t.

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
    """Interest credited to base account values, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month's interest.
    """
    return inv_income_pp(t) * pols_if(t)


def av_change(t):
    """Change in the base account value in force over month t.

    ``av_at(t + 1, BEF_PREM) - av_at(t, BEF_PREM)``, following ``CashValue_SE``.
    Zero outside cover, before ``t + 1`` is read, so that nothing reads a month past
    ``t = proj_len()``; there the change would otherwise be minus the account value the
    survivors of the last month carry.
    """
    if not is_active(t):
        return 0.0
    return av_at(t + 1, BEF_PREM) - av_at(t, BEF_PREM)


def loan_bal_pp_at(t, timing):
    """Policy loan balance per policy at an intra-month point of month t.

    ``BEF_INT``
        Before the month's loan interest accrual: the opening balance ``L_{t-1}``,
        which is the closing balance of the previous month, or the model point's
        :func:`loan_bal_init` in the first month on the books, :func:`t_entry`.  The
        previous month's close is formed here, the timing's value at ``t - 1`` times one
        month of the charged rate, as ``loan_bal_pp(t - 1)`` forms it, so the chain back
        to :func:`t_entry` is one cell a month, where ``ULSG_US_S``'s ran through two.
        With no new loans or repayments modelled the balance is constant from BOM until
        the EOM accrual, so this is the loan outstanding throughout month ``t`` -- the
        loaned part of the account value in :func:`inv_income_pp` and the debt netted in
        the step-6 test :func:`is_guar_supported`.  Zero outside cover.

    The end-of-month balance ``L_t`` is :func:`loan_bal_pp`.
    """
    if timing == BEF_INT:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return loan_bal_init()
        return loan_bal_pp_at(t - 1, BEF_INT) * (1 + loan_rate_mth())
    else:
        raise ValueError("invalid timing")


def loan_bal_pp(t):
    """L_t: the policy loan balance per policy at the end of month t.

    ``L_{t-1} x (1 + r_L)^(1/12)`` at the guaranteed 5.0% [S4] charged in arrears
    [S3] [S7], accrued monthly **[std]**, with ``L_{t-1}`` the opening balance
    ``loan_bal_pp_at(t, BEF_INT)`` -- :func:`loan_bal_init` in the first month on the
    books.  New loans and repayments are not modelled -- the notes give no utilisation
    pattern -- so this only rolls the model point's opening balance forward.
    Indebtedness is deducted from the guarantee in-force test (:func:`sg_net_pp`), from
    death proceeds and from the surrender value; the shadow account itself is not reduced
    by it [S4].  Zero outside cover.
    """
    return loan_bal_pp_at(t, BEF_INT) * (1 + loan_rate_mth())


def sg_pp_at(t, timing):
    """Shadow account value per policy at an intra-month point of month t.

    The same timings as :func:`av_pp_at`, on the shadow parameter set:

    ``BEF_PREM``
        The closing shadow balance of the previous month, ``SG_{t-1}``, or the model
        point's opening balance :func:`sg_pp_init` in the first month on the books,
        :func:`t_entry`.  The previous month's close is formed here, its own value at
        ``t - 1`` through month ``t - 1``'s shadow premium, withdrawal, charges, cost of
        insurance and interest, in ``ULSG_US_S``'s order, so the chain back to
        :func:`t_entry` is one cell a month, where ``ULSG_US_S``'s ran through six.  Zero
        outside cover: no cell reads the shadow account in the month after the frame.

    ``BEF_WD``
        After the shadow net premium ``(1 - pi^g) P_t``, before the withdrawal.

    ``BEF_FEE``
        After the withdrawal, which reduces the shadow account dollar-for-dollar and
        carries **no fee** **[std]**, before the per-unit charge (one observed design
        subtracts partial surrenders and their fees from its guarantee measure [S4]).

    ``BEF_COI``
        After the shadow per-unit charge, before the shadow cost of insurance.  **This
        is the notes'** ``SG'(t)``.

    ``BEF_INV``
        After the shadow cost of insurance, before interest.  This is the notes'
        ``SG''(t)`` and it is **not floored**: a negative shadow balance is the
        catch-up shortfall, and flooring it destroys :func:`catch_up_prem_pp` and
        misprices restoration.
    """
    if timing == BEF_PREM:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return sg_pp_init()
        sg = sg_pp_at(t - 1, BEF_PREM) + prem_to_sg_pp(t - 1)
        sg = sg - wd_pp(t - 1)
        sg = sg - sg_maint_fee_pp(t - 1)
        sg = sg - sg_coi_pp(t - 1)
        return sg + sg * sg_rate_mth()
    elif timing == BEF_WD:
        if not is_active(t):
            return 0.0
        return sg_pp_at(t, BEF_PREM) + prem_to_sg_pp(t)
    elif timing == BEF_FEE:
        return sg_pp_at(t, BEF_WD) - wd_pp(t)
    elif timing == BEF_COI:
        return sg_pp_at(t, BEF_FEE) - sg_maint_fee_pp(t)
    elif timing == BEF_INV:
        return sg_pp_at(t, BEF_COI) - sg_coi_pp(t)
    else:
        raise ValueError("invalid timing")


def sg_inv_income_pp(t):
    """Interest credited to the shadow account at EOM, ``SG''_t x j^g`` **[std]**.

    Credited on the post-deduction shadow balance with no floor and no loaned/unloaned
    split: the shadow account is notional and carries no loan of its own.
    """
    return sg_pp_at(t, BEF_INV) * sg_rate_mth()


def sg_pp(t):
    """SG_t: the shadow account value per policy at the end of month t.

    ``SG''_t x (1 + j^g)`` for every ``t`` of the frame including the first month on the
    books; the opening balance :func:`sg_pp_init` enters through
    ``sg_pp_at(t_entry(), BEF_PREM)``.  Notional throughout: it exists only to run the
    in-force test and is never payable [S2][S3].  Zero outside cover.
    """
    return sg_pp_at(t, BEF_INV) + sg_inv_income_pp(t)


def sg_net_pp(t):
    """SG_t - L_t: the shadow account net of indebtedness, the in-force test quantity.

    Indebtedness is deducted from the guarantee measure rather than from the shadow
    account itself [S4].  The observed shadow-account design; the harshest observed
    alternative voids the guarantee outright on any loan [S5].
    """
    return sg_pp(t) - loan_bal_pp(t)


def is_guar_active(t):
    """The step-9 in-force test: ``SG_t - L_t > 0`` [S4][S2][S9].

    Measured at EOM, after the shadow interest credit and the loan accrual.  While it
    holds the policy cannot lapse however exhausted the real account value is; when it
    fails, an exhausted account opens the grace period.  Strictly greater than zero, as
    the notes require: a ``>= 0`` target on a monthly grid can leave the guarantee
    failing on the final monthiversary.
    """
    return sg_net_pp(t) > 0


def is_guar_supported(t):
    """The step-6 test: ``SG''_t - L_{t-1} > 0``, measured before the interest credits.

    This is the one that decides what happens to a failed deduction -- forgone by the
    insurer, or grace.  It is deliberately a different measurement point from
    :func:`is_guar_active`, and it is evaluated **after** the full monthly deduction
    attempt: testing before the deduction lets a policy lapse a month early or late and
    shifts claim timing at exactly the durations where the net amount at risk is the
    whole death benefit.  ``L_{t-1}`` is the opening loan balance
    ``loan_bal_pp_at(t, BEF_INT)``.
    """
    return sg_pp_at(t, BEF_INV) - loan_bal_pp_at(t, BEF_INT) > 0


def catch_up_prem_pp(t):
    """C_t: the premium restoring the guarantee, ``max(0, -(SG_t - L_t)) / (1 - pi^g)``.

    The negative net shadow balance grossed up for the shadow premium load **[std]**;
    paying it brings ``SG - L`` back to zero and the guarantee with it [S7][R1 ex. 7].
    A diagnostic only: the notes state expressly that catch-up behaviour is not
    modelled in the base run, so no policy ever pays it.  This is why the shadow
    account must never be floored at zero, and why a point in force carries its shadow
    account as it stands, below zero included (:func:`sg_pp_init`).
    """
    return max(0.0, -sg_net_pp(t)) / (1 - load_prem_rate_sg)


def surr_charge_rate(t):
    """SC per $1,000 of initial face in month t **[std]**.

    ``max(0, sc_init - (sc_init / runoff_years) x m / 12)`` where ``m`` is the notes'
    own month index ``duration_mth(t) + 1`` -- the current month counts.  With the
    shipped 15-year schedule at $18 per $1,000 this is the spec's
    ``18 x max(0, (180 - m) / 180)``: $17.90 in the issue month, zero from the last
    month of policy year 15.  Reading the notes' month index as ``duration_mth(t)``
    would shift the entire run-off by a month.  The schedule's two values are read once
    a point by :func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`, which
    ask ``Data`` to check the table first; the floor keeps ``ULSG_US_S``'s order,
    ``max(0.0, ...)``, the bound first.  Zero outside cover, and where the point carries
    no schedule.
    """
    if not is_active(t) or not has_surr_charge():
        return 0.0
    init = surr_charge_rate_max()
    yrs = surr_charge_runoff_years()
    m = duration_mth(t) + 1
    return max(0.0, init - (init / yrs) * (m / 12))


def surr_charge_pp(t):
    """SC_t: the surrender charge scheduled per policy in month t.

    Quoted on the **initial** face amount.  This is the schedule, not the amount
    collected: see :func:`surr_charge`.
    """
    return surr_charge_rate(t) * sum_assured() / 1000


def csv_pp(t):
    """The cash surrender value per policy, ``AV_t - SC_t``, floored at zero.

    The floor is **[std]**: a negative cash surrender value would be a payment *from*
    the policyholder.  On this product it binds for years -- guaranteed UL account
    values are deliberately thin and the 15-year surrender charge starts at $9,000 on
    a $500,000 face.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """CSV_t in the notes: the net cash surrender value, ``max(AV_t - SC_t - L_t, 0)``.

    What a surrendering policyholder is paid, and the notes' surrender outgo.  The
    notes' symbol ``CSV_t`` already nets indebtedness, so it is this cell and not
    :func:`csv_pp`; the chassis keeps the two apart so the surrender-charge and the
    debt offsets can be read separately.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """Surrender charge actually collected from the policies surrendering in month t.

    ``(AV_t - CSV_t) x pols_lapse(t)``, so it is capped by the account value where the
    :func:`csv_pp` floor binds -- which on this product is most of the first fifteen
    years.  Insurer income, and part of :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def is_shortfall(t):
    """Whether the monthly deduction attempt failed: ``AV'_t - COI_t < 0``.

    The notes' step 6 condition, evaluated **after** the full deduction attempt.  On
    its own it says nothing about lapse: while :func:`is_guar_supported` holds the
    shortfall is forgone by the insurer and coverage continues; only when the guarantee
    has failed as well does it open the grace period.
    """
    return av_pp_at(t, BEF_COI) - coi_pp(t) < 0


def cure_premium_pp(t):
    """The payment that would cure a grace: the deduction shortfall, grossed up.

    ``D_t / (1 - pi)`` **[std]** -- the notes define the required grace payment as the
    amount curing the deduction shortfall, and a premium reaches the account value net
    of the load.  A diagnostic: the notes give no cure probability, so no policy pays it.
    A grace ends without a lapse only where the month's deduction stops failing on its own,
    as when a scheduled premium falls due and carries it (:func:`grace_mth`); otherwise a
    policy that enters grace lapses when the 61 days expire.

    ``Data`` admits a load of 1, where ``ULSG_US_S`` divides by zero in every month; the
    division is guarded, and raises Python's ``ZeroDivisionError("float division by
    zero")`` in both engines, where a compiled division would raise its own, shorter
    message.
    """
    if 1 - load_prem_rate() == 0:
        raise ZeroDivisionError("float division by zero")
    return mth_deduction_forgone_pp(t) / (1 - load_prem_rate())


def grace_mth(t):
    """g_t: months elapsed in the grace period, 0 when not in grace [S7].

    The counter advances only when the deduction attempt failed **and** the guarantee
    is not supporting the policy; a failed deduction under an active guarantee is
    forgone and never opens a grace.  A month whose deduction does not fail -- a
    scheduled premium falling due may carry it -- resets the counter to 0, so a grace
    can be cured that way, and the policy lapses only once ``grace_months`` failing months
    run together (:func:`is_lapsed`).  The count carried into the first month on the
    books, :func:`t_entry`, is the model point's :func:`grace_mth_init`, the months
    already spent in grace at the valuation date, where ``ULSG_US_S`` reads 0, as it does
    at issue.  It reads its own value at ``t - 1`` through :func:`is_lapsed`, which reads
    it first, so the counter and its latch are one chain of one cell a month.  An int in
    every branch, as in ``ULSG_US_S``; 0 outside cover.
    """
    if not is_active(t):
        return 0
    if is_lapsed(t):
        return 0
    if not is_shortfall(t) or is_guar_supported(t):
        return 0
    return (grace_mth(t - 1) if t > t_entry() else grace_mth_init()) + 1


def is_lapsed(t):
    """Whether the policy has terminated for insufficiency at or before BOM of month t.

    The 61-day grace period [S7] is taken as ``grace_months`` = 2 policy months
    **[std]**; when it expires without the required payment the policy lapses at BOM
    with no value -- the cash surrender value is zero in grace by construction.  Lapse
    for insufficiency requires all three of the notes' conditions: the deduction
    attempt failed, ``SG - L <= 0``, and the grace expired uncured.  A latch: once true it
    stays true.

    False in the first month on the books, :func:`t_entry`, where ``ULSG_US_S``'s is false
    at its own ``t = 0``: a point in force carries a grace counter below ``grace_months``,
    which :func:`proj_len` checks, so it is in force there, and the in-force interface
    carries no latch, since a policy that has lapsed is not in force.  Defined in the
    month after the frame too, ``t = proj_len()``, where it is the latch the last month
    leaves, which :func:`pols_lapse_grace` reads at ``t + 1`` and the count carried there
    reads at its own month.  False before issue.
    """
    if not 0 <= duration_mth(t) <= charges_cease_mth():
        return False
    if t == t_entry():
        return False
    return is_lapsed(t - 1) or grace_mth(t - 1) >= grace_months


def status(t):
    """The worked example's Status column as a code, and why a month is outside cover.

    ``IN_FORCE``
        the account value is carrying the policy, ``ULSG_US_S``'s ``"IN FORCE"``;
    ``IN_FORCE_GUARANTEE``
        the account value is exhausted and the guarantee is carrying it -- the notes'
        "in force - guarantee", ``ULSG_US_S``'s ``"IN FORCE - GUARANTEE"``;
    ``GRACE``
        the deduction failed with no guarantee behind it;
    ``LAPSED``
        the grace expired uncured;
    ``PRE_ISSUE``
        the month precedes the issue of a point written after the valuation date;
    ``CEASED``
        the month after the frame, ``t = proj_len()``, and any later, where premiums
        and charges have ceased.

    The last two are this model's, codes of the months outside cover, which
    ``ULSG_US_S``'s frame never holds.  ``ULSG_US_S`` returns text; here each status is
    an int Reference, numbered in the order of a policy's life (the Space docstring's
    *Codes*), and :func:`result_av` writes ``ULSG_US_S``'s label for it in its ``status``
    column, so the report reads as ``ULSG_US_S``'s.  ``GRACE`` is the one code a status
    shares with a claim kind, as ``ULSG_US_S`` spells the two alike.
    """
    if duration_mth(t) < 0:
        return PRE_ISSUE                                             # noqa: F821
    if duration_mth(t) >= charges_cease_mth():
        return CEASED                                                # noqa: F821
    if is_lapsed(t):
        return LAPSED                                                # noqa: F821
    if grace_mth(t) > 0:
        return GRACE                                                 # noqa: F821
    if av_pp(t) <= 0:
        return IN_FORCE_GUARANTEE                                    # noqa: F821
    return IN_FORCE                                                  # noqa: F821


def rop_anniversary(t):
    """The return-of-premium anniversary whose window contains month t, or 0 [S1].

    The endorsement is exercisable during the 60 days following policy anniversaries
    20 and 25 [S1] (60-day window mechanics [S3] [S4]).  On a monthly grid the window
    is taken as the anniversary month itself **[std]**, so the exercise rate is applied
    once rather than spread over two monthiversaries.  The anniversary is read on the
    policy clock, ``duration_mth(t) % 12`` and ``duration(t)``, so a point valued mid-year
    meets its windows in the months its own anniversaries fall in, not on the valuation
    date's; whether one carries a window is :func:`is_rop_anniv`'s to say.  An int, 0
    outside cover and where the point does not elect the endorsement.
    """
    if not is_active(t) or not rop_elected():
        return 0
    if duration_mth(t) % 12 != 0:
        return 0
    y = duration(t)
    return y if is_rop_anniv(y) else 0


def rop_ratio(t):
    """rho: the fraction of cumulative premiums refunded in the window, 50% or 100% [S1].

    Read at the window's anniversary by :func:`rop_ratio_anniv`; 0.0 in any other month.
    """
    a = rop_anniversary(t)
    if a == 0:
        return 0.0
    return rop_ratio_anniv(a)


def rop_rate(t):
    """w^ROP: the fraction of eligible in-force exercising in the window **[std]**.

    5% at the year-20 window and 10% at the year-25 window.  No public exercise study
    exists; the rationale for keeping them modest is that the 100% refund dominates
    the cash surrender value on a thin-account product, but exercising forfeits a
    now-cheap guarantee.  Mis-setting them distorts years 20-26 of the cash flows.  Read
    at the window's anniversary by :func:`rop_rate_anniv`; 0.0 in any other month.
    """
    a = rop_anniversary(t)
    if a == 0:
        return 0.0
    return rop_rate_anniv(a)


def is_rop_anniv(y):
    """Whether a return-of-premium window follows policy anniversary y [S1].

    The anniversary is the completed policy years at it, ``duration(t)`` in its month,
    and *rop_table.csv* lists the anniversaries that carry a window, 20 and 25 as shipped,
    so this is ``ULSG_US_S``'s membership of the table's key column, read from
    ``Data.rop_anniv_flags()``, 1 at each anniversary of the table and 0 elsewhere, from
    0 to the last, ``data.rop_last_anniv()``, so that the anniversary is the index.  It
    asks for the last first, which checks the table's anniversaries and values, so that a
    projection meets the check before it reads the table: a key written ``20.0`` is
    anniversary 20, and one that is blank, text, not whole or below 1 is refused by name.
    An anniversary past the last, or below 0, is in no window, as in ``ULSG_US_S``, and is
    answered before the flags are read, so that no read falls outside them.
    """
    last = data.rop_last_anniv()                                     # noqa: F821
    if y < 0 or y > last:
        return False
    return bool(data.rop_anniv_flags()[y])                           # noqa: F821


def rop_ratio_anniv(y):
    """rho at policy anniversary y: the ``refund_ratio`` column of *rop_table.csv* [S1].

    ``Data.rop_ratio_array()`` at the anniversary, padded with NaN between the table's
    anniversaries.  Read only at an anniversary :func:`is_rop_anniv` finds in the table,
    which it asks first; any other, where ``ULSG_US_S``'s ``.loc`` raised ``KeyError``, is
    refused, naming the point and the anniversary, so that the padding is never read.
    """
    if not is_rop_anniv(y):
        raise ValueError(f"point_id {point_id()}: rop_table.csv has no anniversary {y}")
    return float(data.rop_ratio_array()[y])                          # noqa: F821


def rop_rate_anniv(y):
    """w^ROP at policy anniversary y: the ``exercise_rate`` column of *rop_table.csv*.

    ``Data.rop_rate_array()`` at the anniversary, read and refused as
    :func:`rop_ratio_anniv` reads and refuses its own.
    """
    if not is_rop_anniv(y):
        raise ValueError(f"point_id {point_id()}: rop_table.csv has no anniversary {y}")
    return float(data.rop_rate_array()[y])                           # noqa: F821


def class_factor():
    """The underwriting-class multiplier on the best-estimate mortality table **[std]**.

    ``Data.class_factor`` at the point: the ``factor`` of the point's ``rate_class`` in
    *class_factor_table.csv*, joined to the points once ``data.class_count()`` has checked
    the table's classes and factors, so that a blank factor never reaches :func:`mort_rate`
    as a missing value, which its cap would keep missing.  Every point reads its class
    factor in its first month in cover, so ``Data`` refuses the table at its first read,
    naming every point whose class the table lacks, where ``ULSG_US_S``'s ``.loc`` raised
    ``KeyError`` as the point projected.
    """
    return float(data.class_factor()[idx])                           # noqa: F821


def mort_improve_rate(t):
    """The annual mortality improvement rate at the attained age in month t **[std]**.

    1.0% a year to attained age 85, grading linearly to 0% at attained age 95 and zero
    thereafter.  Improvement compounds, so at the late attained ages where the net
    amount at risk is the whole death benefit it is one of the two assumptions that
    move the claims most.  A function of the clock and the References alone, which reads
    no table: it holds its value outside cover, and before a point's issue it grades the
    improvement of those years at the age the cohort has reached then (:func:`age`).
    """
    a = age(t)
    if a <= mort_improve_full_age:                                   # noqa: F821
        return mort_improve_rate_init                                # noqa: F821
    if a >= mort_improve_end_age:                                    # noqa: F821
        return 0.0
    return mort_improve_rate_init * (                                # noqa: F821
        (mort_improve_end_age - a)                                   # noqa: F821
        / (mort_improve_end_age - mort_improve_full_age))


def mort_improve_factor(t):
    """The cumulative mortality improvement factor in month t **[std]**.

    1.0 in the first year from the valuation date (``t = 0 .. 11``), then one further year
    of improvement on each anniversary of the valuation date (``t = 12, 24, ...``), for at
    most ``mort_improve_max_years`` = 20 years as the notes prescribe: in month ``t`` it is
    the product, over the ``t // 12`` years before it, of one minus
    :func:`mort_improve_rate` at the months ``t - 12``, ``t - 24``, ..., each graded at the
    attained age of its month, and past 20 years the factor of month 240.  An input on the
    **valuation** clock, as ``ULSG_US_S``'s runs from the start of its own projection, which
    is the valuation date of its in-force point 1: every point of a block gains its years
    of improvement in the same months, whatever its own anniversaries.  Between them the
    factor moves only where a graded rate it reads moves, at attained ages 85 to 95, on the
    policy's own anniversaries: on point 7, valued mid-year at attained age 85, it moves at
    ``t = 12, 19, 24, 31, 36, ...``.  A point written ``k`` months after the valuation date
    takes the improvement of the years before its issue too, each graded at the age its
    cohort reached in that year: one written 25 months on starts at the factor of
    ``t = 24``.  So this is the one chain that reads months before :func:`t_entry`, each a
    year apart, a function of the clock and the References that reads no balance of the
    books; it is one cell a year, at most ``mort_improve_max_years + 2`` cells deep, 22,
    from ``t = 252`` on: that month's factor, then those of months 240, 228, ..., 12 and 0.
    """
    k = t // 12
    if k <= 0:
        return 1.0
    if k > mort_improve_max_years:                                   # noqa: F821
        return mort_improve_factor(12 * mort_improve_max_years)      # noqa: F821
    return mort_improve_factor(t - 12) * (1 - mort_improve_rate(t - 12))


def mort_rate(t):
    """The annual best-estimate mortality rate in month t, capped at 1.

    Base table x :func:`class_factor` x the A/E factor, which is 100% in the base run
    **[std]**, x :func:`mort_improve_factor`, capped at 1.0.  The shipped table is a
    small illustrative one **[std]**, *not* the 2015 VBT the notes recommend -- that
    family is licensed and may not be reproduced here.  The base rate is read at the
    attained age of month t by :func:`mort_rate_base_at`, which takes ages beyond the table
    at its last row, where the rate is 1.0; the cap is what keeps a class factor above 1
    from pushing the terminal rate past certainty.  It puts its bound second, as
    ``ULSG_US_S`` does, so that a missing input, a NaN, stays NaN, where ``min(1.0, q)``
    would read it as 1; ``Data`` refuses a blank base rate or class factor as it reads the
    tables, before any rate is read.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return min(mort_rate_base_at(age(t)) * class_factor()
               * mort_ae_factor * mort_improve_factor(t), 1.0)


def mort_rate_base_at(a):
    """The base table's annual mortality rate at attained age a: the table's one reader.

    From *mort_table.csv*, before the class factor, the A/E factor and the improvement:
    ``Data.mort_table_array()`` at the age, the table padded from age 0.  Ages outside the
    table take its nearest row, which below it is the rate at age 45 and above it the rate
    of 1.0 at age 120: the first and last ages ``data.mort_age_first()`` and
    ``data.mort_age_last()`` give, which they read from the table's key column once the
    keys and the rates are checked, before any rate is read, the last first, as
    :func:`corridor_factor_at` asks; so the padding is never read.  Keyed by the attained
    age, so the table is read once an age rather than once a month; :func:`mort_rate`
    calls it inside cover only.
    """
    last = data.mort_age_last()                                      # noqa: F821
    a = min(max(a, data.mort_age_first()), last)                     # noqa: F821
    return float(data.mort_table_array()[a])                         # noqa: F821


def mort_rate_mth(t):
    """q_t^d: the monthly best-estimate mortality rate, ``1 - (1 - q)^(1/12)``.

    Note that the **experience** decrement uses the compound conversion while the
    contractual COI rate uses the simple twelfth (:func:`coi_rate_guar`).  The notes
    prescribe exactly that split; the two must not be interchanged.
    """
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """b(d): the base annual lapse rate by policy year **[std]**.

    4.0%, 3.0%, 2.5%, then 2.0% in years 4-5, 1.5% in 6-10, 1.0% in 11-20 and 0.75%
    thereafter, read from *lapse_table.csv* at the policy year of month t by
    :func:`lapse_rate_base_py`.  The shape is anchored to the public highlights of the
    SOA/LIMRA UL persistency and lapse studies [R7][REG-R20][REG-R21], whose detailed
    tables sit in a paid data package, so the levels are a standardization.  Zero outside
    cover, before the table is read.
    """
    return lapse_rate_base_py(policy_year(t)) if is_active(t) else 0.0


def lapse_rate_base_py(y):
    """b in policy year y, from *lapse_table.csv*: the table's one reader.

    ``Data.lapse_rate_array()`` at the year, the table padded from year 0, so that the
    year is the index.  Policy years beyond the table take its last row, the last year
    ``data.lapse_last_year()`` gives, 21 as shipped, which it reads from the table's key
    column once it has checked the keys and the rates, before any rate is read.  A year
    below 1, where ``ULSG_US_S``'s ``.loc`` raised ``KeyError``, is refused, naming the
    point and the year, so that the padding is never read.  Keyed by the contractual
    policy year, so the table is read once a policy year rather than once a month;
    :func:`lapse_rate_base` calls it inside cover only.
    """
    last = data.lapse_last_year()                                    # noqa: F821
    if y < 1:
        raise ValueError(f"point_id {point_id()}: lapse_table.csv has no rate for policy "
                         f"year {y}")
    return float(data.lapse_rate_array()[min(y, last)])              # noqa: F821


def lapse_rate_guar_mult():
    """G: the guarantee-duration lapse multiplier, 0.55 for a lifetime election.

    Lifetime secondary-guarantee lapse rates run 45% below non-lifetime rates on both
    count and amount bases in the 2015-2021 industry experience [R7]; the level is
    derived from that finding and the flat duration shape is **[std]**.  This is the
    first-order assumption for a lapse-supported product: every lapse of a funded
    guarantee releases the insurer from a deeply in-the-money claim.
    """
    if guarantee_age() >= lifetime_guarantee_age:                    # noqa: F821
        return lapse_guar_mult                                       # noqa: F821
    return 1.0


def lapse_rate_pattern_mult():
    """Phi: the premium-pattern lapse multiplier **[std]**.

    Single-pay 0.6, ten-pay 0.8, level 1.0, in the direction [R8] reports -- higher
    lapses for level-pay, lower for single-pay.  The pattern is read through its decodes,
    :func:`is_single_premium`, :func:`is_ten_pay_premium` and :func:`is_level_premium`,
    and a pattern none of them knows raises, as in ``ULSG_US_S``.
    """
    if is_single_premium():
        return lapse_pattern_mult_single                             # noqa: F821
    elif is_ten_pay_premium():
        return lapse_pattern_mult_ten_pay                            # noqa: F821
    elif is_level_premium():
        return 1.0
    else:
        raise ValueError("invalid premium type")


def lapse_rate_dyn_mult(t):
    """Psi_t: the funding-status dynamic lapse factor **[std]**.

    ``1.0``
        guarantee active and the account value still positive;
    ``0.6``
        guarantee active and the account value exhausted -- the policy is deep in
        the money to the policyholder, the regime [R8]'s tail scenarios keep 40%
        of policies in after 31 years;
    ``2.0``
        the guarantee has terminated and the policy is surviving on its account
        value alone -- a shock.  Where the account value has gone too the policy
        is already in grace and about to lapse, so the rate is academic there.

    Dynamic lapse is used by 63% of surveyed ULSG writers, and lapse and tail
    investment returns are rated the most critical ULSG assumptions [R8]; the formula
    itself is a standardization.  The neutral 1.0 outside cover, before the shadow
    account or the account value is read.
    """
    if not is_active(t):
        return 1.0
    if not is_guar_active(t):
        return lapse_dyn_mult_guar_failed                            # noqa: F821
    if av_pp(t) > 0:
        return 1.0
    return lapse_dyn_mult_guar_only


def lapse_rate(t):
    """The total annual lapse rate, ``min(0.5, max(0.003, b(d) G Phi Psi_t))`` **[std]**.

    The 0.3% annual floor is applied after the dynamic factor, as the notes write it,
    and the 50% cap wraps the result; the two cannot conflict.  Both keep
    ``ULSG_US_S``'s order, each bound written first; a lapse rate's bound is not the cap
    on mortality.  ``Data`` holds each base rate to 0 to 1, so the rate stays a rate
    while ``lapse_rate_cap`` is at most 1.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    rate = (lapse_rate_base(t) * lapse_rate_guar_mult()
            * lapse_rate_pattern_mult() * lapse_rate_dyn_mult(t))
    return min(lapse_rate_cap, max(lapse_rate_floor, rate))


def lapse_rate_mth(t):
    """w_t: the monthly lapse rate, ``1 - (1 - w_annual)^(1/12)``."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """l_t: the number of policies in force at the beginning of month t, row t's weight.

    ``pols_if_at(t, BEF_DECR)``, the notes' ``l_t``: the count carried in from month
    t - 1 plus month t's new business, before month t's decrements.  Decrements are
    end-of-month events, so the number in force is constant through the month and every
    BOM cash flow is weighted by it.  On a point issued at ``t = 0`` it is exactly
    ``ULSG_US_S``'s ``pols_if``.  A point in force at the valuation date opens with
    :func:`pols_if_init`, and one issued at or after it with its issued count in the
    issue month.  Zero before issue, and zero once the policy has lapsed for
    insufficiency (:func:`is_lapsed`).  At ``t = proj_len()``, the month after the frame,
    it is the survivors of the last month, which the roll-forwards read.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity.
    """
    return pols_if_at(t, BEF_DECR)


def pols_if_at(t, timing):
    """Number of policies in force at a point of month t, by ``timing``.

    The three timings ``ULSG_US_S``'s cell names:

    ``BEF_NB``
        The count carried in from month t - 1, before month t's new business: month
        t - 1's ``BEF_DECR`` count less its four decrements, the deaths, surrenders and
        refund exercises and the policies its grace's expiry terminates, in
        ``ULSG_US_S``'s order, or 0 where the policy has lapsed for insufficiency by
        month t, which ``ULSG_US_S`` tests first.  In the first month on the books,
        :func:`t_entry`, it is :func:`pols_if_init`, the count in force at the valuation
        date (0 for a point issued at or after it), and the recursion reads no earlier
        month.  It is also defined in the month after the frame, ``t = proj_len()``, where
        it is the survivors of the last month: the projection ends where charges cease,
        not where the cover does, so they are kept rather than matured.  Zero before
        issue.
    ``BEF_DECR``
        ``l_t``: ``BEF_NB`` plus :func:`pols_new_biz`, before any decrement; the same
        number as :func:`pols_if`, and the weight on that month's cash flows.
    ``BEF_MAT``
        Before any maturity: ``ULSG_US_S``'s meaning, the ``BEF_DECR`` count, which its
        cell gives for this timing.  The contract has no maturity date, so nothing
        matures and no event of the month separates the two.  ``basiclife.BasicTerm_SE``'s
        ``BEF_MAT``, the count at the start of the month before its new business, is
        not adopted: the name keeps its S model's meaning.

    ``BEF_NB`` forms month t - 1's ``BEF_DECR`` count itself -- its own value at
    ``t - 1`` plus that month's :func:`pols_new_biz` -- rather than calling for it, and
    the decrement cells it then calls read that count, cached.  So the chain of calls
    back to :func:`t_entry` is one cell a month, as ``ULSG_US_S``'s :func:`pols_if` chain
    was: a compiled model runs that chain on the C stack.  ``ULSG_US_S``'s cell returns
    :func:`pols_if` for every timing, which in the issue month counts the issued policies
    under all three; here ``BEF_NB`` alone counts them as new business, not yet in.  Any
    other timing raises.
    """
    if timing == BEF_NB:
        if not 0 <= duration_mth(t) <= charges_cease_mth():
            return 0.0
        if t == t_entry():
            return pols_if_init()
        if is_lapsed(t):
            return 0.0
        prev = pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1)
        return (prev - pols_death(t - 1) - pols_lapse(t - 1) - pols_rop(t - 1)
                - pols_lapse_grace(t - 1))
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
    """Number of deaths at the end of month t, ``l_t x q_t^d``.

    Zero outside cover, before any rate is read.
    """
    return pols_if(t) * mort_rate_mth(t) if is_active(t) else 0.0


def pols_lapse(t):
    """Number of surrenders at the end of month t.

    ``l_t (1 - q_t^d) w_t``: death is applied before lapse, which is the notes'
    ordering.  Zero outside cover, before any rate is read.
    """
    if not is_active(t):
        return 0.0
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_rop(t):
    """Number of return-of-premium exercises at the end of month t.

    ``l_t (1 - q_t^d)(1 - w_t) w_t^ROP``, matching the notes'
    ``l_{t+1} = l_t (1 - q^d)(1 - w)(1 - w^ROP)``.  Exercise is a full surrender
    [S1][S3], so an exercising policy leaves with the refund and nothing else.  Zero
    outside cover, before any rate is read.
    """
    if not is_active(t):
        return 0.0
    return (pols_if(t) * (1 - mort_rate_mth(t))
            * (1 - lapse_rate_mth(t)) * rop_rate(t))


def pols_lapse_grace(t):
    """Number of policies terminating for insufficiency at the end of month t.

    Non-zero only in the month before the grace period expires, when every remaining
    policy is out.  This is not a rate-based decrement: it is the contractual
    termination of a policy whose account value failed and whose guarantee had already
    gone, and it is needed for the in-force roll-forward to close.  The policies leave
    with no value, so it generates no claim -- the cash surrender value is zero in
    grace by construction.  It reads the latch of month ``t + 1``, the one month ahead
    any cell reads; zero outside cover, before it reads it, so that nothing reads past
    ``t = proj_len()``, where the latch of the last month's close is defined.
    """
    if not is_active(t):
        return 0.0
    if is_lapsed(t) or not is_lapsed(t + 1):
        return 0.0
    return pols_if(t) - pols_death(t) - pols_lapse(t) - pols_rop(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    Guaranteed UL has no maturity date -- at attained age 121 premiums and charges
    cease and coverage continues [S7].  The cell is kept so the in-force roll-forward
    identity has the same shape as in the term and annuity models of this library,
    where it is not zero.  The survivors of the frame's last month do not mature either:
    the projection stops there because the charges do, and they are carried into
    ``t = proj_len()`` (:func:`pols_if_at`).
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``DEATH``
        ``DB_t - L_t``: the death benefit less outstanding indebtedness, standard UL
        treatment **[std]**.

    ``LAPSE``
        :func:`ncsv_pp`, the notes' ``CSV_t = max(AV_t - SC_t - L_t, 0)``.

    ``REFUND``
        ``min(rho CumPrem_t, 0.40 F) - L_t``, floored at zero [S1]: the
        return-of-premium refund, capped at 40% of the face amount and net of debt.
        On the anchor cell the cap binds -- 25 years of $10,800 premiums is $270,000
        against a $200,000 cap -- which is exactly why the cap exists.

    ``WITHDRAWAL``
        ``W_t``.  The $25 fee is retained by the insurer and is not part of the
        payment.  A withdrawal is not a claim -- the aggregate cash flow is
        :func:`withdrawals`, and no ``claims_<kind>`` cell carries it -- but the
        per-policy amount keeps its branch here because :func:`withdrawals` weights it.

    ``GRACE``
        Zero: a policy terminating in grace terminates without value [S7].
    """
    if kind == DEATH:
        return db_pp(t) - loan_bal_pp(t)
    elif kind == LAPSE:
        return ncsv_pp(t)
    elif kind == REFUND:
        return max(0.0, min(rop_ratio(t) * cum_prem_pp(t),
                            rop_cap_rate * sum_assured_at(t))        # noqa: F821
                   - loan_bal_pp(t))
    elif kind == WITHDRAWAL:
        return wd_pp(t)
    elif kind == GRACE:
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim released from the account value, by ``kind``.

    Death, surrender and refund all release the end-of-month account value ``AV_t``,
    because decrements follow the interest credit; so does a policy terminating in
    grace, though its account value is zero by construction.  ``MATURITY`` is zero:
    the contract has no maturity date.

    ``WITHDRAWAL`` keeps its branch even though a withdrawal is not a claim: it is
    taken at BOM out of the account values of the policies still in force, and it is
    the same figure as :func:`withdrawals`.
    """
    if kind == DEATH:
        return av_pp(t) * pols_death(t)
    elif kind == LAPSE:
        return av_pp(t) * pols_lapse(t)
    elif kind == REFUND:
        return av_pp(t) * pols_rop(t)
    elif kind == GRACE:
        return av_pp(t) * pols_lapse_grace(t)
    elif kind == WITHDRAWAL:
        return withdrawals(t)
    elif kind == MATURITY:
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    """Death claims in excess of the account value released.

    ``(claim_pp(t, DEATH) - AV_t) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin -- and in the guarantee-support regime, where
    the account value is zero and the charge is forgone, it is the whole face amount
    with no charge behind it.
    """
    return (claim_pp(t, DEATH) - av_pp(t)) * pols_death(t)


def claims(t):
    """Claim outgo in month t: death, surrender and refund claims together.

    :func:`claims_death`, :func:`claims_lapse` and :func:`claims_refund`, the total
    :func:`net_cf` subtracts.  ``ULSG_US_S``'s ``claims(t, kind=None)`` is both the kinds
    and their total, a generator over its four kinds summed by Python's ``sum``, which
    compiles to neither a C parameter nor a C loop; here the three kinds that pay are
    cells, the ``result_cf`` columns, and this is their total.  ``ULSG_US_S``'s fourth,
    ``GRACE``, is 0.0 in every month, a policy terminating in grace terminating without
    value, and has no cell.

    The total is Python's ``sum`` of floats, written out.  ``sum`` is compensated, since
    Python 3.12: it carries the rounding error of each addition, Neumaier's way, and adds
    it back once at the end, where it is finite and not 0.  On a return-of-premium
    anniversary all three kinds pay in one month, deaths, surrenders and refunds, and
    there a sum written left to right, ``0.0 + d + l + r``, differs from ``ULSG_US_S``'s
    in the last bit in some months of the committed points; with at most two kinds
    non-zero the two agree, the error of a single addition never being carried.  So each
    addition is written as ``sum`` makes it, in explicit statements, with no tuple and no
    loop, which would not compile to C; ``0.0 +`` the first kind is ``sum``'s start, the
    int 0, which turns negative zeros to ``0.0``.  The ``GRACE`` term is left out: adding
    0.0 to a running total that is never ``-0.0`` changes neither the total nor the
    carried error.  The final test, ``abs(c) <= 1.7976931348623157e308``, the largest
    double, is ``sum``'s test that the carried error is finite, false for an infinity or a
    NaN, without a subtraction a compiler might fold.  So the total is ``ULSG_US_S``'s
    float in every month, and each step is one IEEE operation in both engines.

    Partial withdrawals are **not** here, neither as a kind nor in the total: a
    withdrawal is a payment on the owner's election rather than a claim, and is
    :func:`withdrawals`.  So ``claims(t)`` is the death, surrender and refund total only,
    and :func:`net_cf` subtracts the withdrawal row separately.
    """
    f = 0.0 + claims_death(t)
    c = 0.0
    x = claims_lapse(t)
    s = f + x
    if abs(f) >= abs(x):
        c = c + ((f - s) + x)
    else:
        c = c + ((x - s) + f)
    f = s
    x = claims_refund(t)
    s = f + x
    if abs(f) >= abs(x):
        c = c + ((f - s) + x)
    else:
        c = c + ((x - s) + f)
    f = s
    if c != 0.0 and abs(c) <= 1.7976931348623157e308:
        f = f + c
    return f


def claims_death(t):
    """Death claims in month t: :func:`pols_death` at the death benefit less the loan per
    policy, ``claim_pp(t, DEATH)``, an end-of-month event.  ``ULSG_US_S``'s ``claims(t,
    "DEATH")``, and the ``claims_death`` column of :func:`result_cf`."""
    return claim_pp(t, DEATH) * pols_death(t)                        # noqa: F821


def claims_lapse(t):
    """Surrender claims at the end of month t: :func:`pols_lapse` at the net cash
    surrender value per policy, ``claim_pp(t, LAPSE)``.  ``ULSG_US_S``'s ``claims(t,
    "LAPSE")``, and the ``claims_lapse`` column of :func:`result_cf`."""
    return claim_pp(t, LAPSE) * pols_lapse(t)                        # noqa: F821


def claims_refund(t):
    """Return-of-premium refunds at the end of month t: :func:`pols_rop` at the refund per
    policy, ``claim_pp(t, REFUND)``.  ``ULSG_US_S``'s ``claims(t, "REFUND")``, and the
    ``claims_rop`` column of :func:`result_cf`."""
    return claim_pp(t, REFUND) * pols_rop(t)                         # noqa: F821


def withdrawals(t):
    """Partial withdrawal payments in month t, for the policies in force.

    ``W_t x l_t``.  Withdrawals are taken at BOM by policies still in force, so the
    weight is :func:`pols_if` and not a decrement.  A withdrawal is a payment on the
    owner's election, not a claim, which is why it is a cell and a ``result_cf()``
    column of its own rather than a claim kind, and no part of :func:`claims`.  The $25
    fee is retained by the insurer and is :func:`wd_fees`, not part of this payment.

    Zero in every shipped model point: the notes set withdrawal utilisation to zero in
    the base model and give no pattern, so the mechanics are implemented and the
    behaviour is left to the data **[std]**.
    """
    return claim_pp(t, WITHDRAWAL) * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(t // 12)`` **[std]**.

    Expenses inflate by year, not by month, which is how the notes write the $75 per
    policy per year maintenance expense, and on the **valuation** clock: the years are
    counted from the valuation date, ``t // 12``, so the expense is in valuation-date
    dollars whatever the policy's age, and every point of a block steps alike, on the
    valuation date's anniversaries.  ``ULSG_US_S`` steps on the policy year,
    ``(1 + inflation_rate)^(y - 1)``; on a point issued at ``t = 0`` the two are the same,
    and on point 1, in policy year 26 at the valuation date, this model's maintenance is
    ``ULSG_US_S``'s divided by ``1.025^25``.  A function of the clock alone, so it holds
    its value outside cover.  Acquisition is not inflated (see :func:`expenses`).
    """
    return (1 + inflation_rate) ** (t // 12)


def expenses(t):
    """The insurer's own expenses in month t **[std]**.

    Acquisition in policy year 1 -- $300 a policy in the issue month plus 90% of every
    first-year premium, which is the notes' combined commission and issue allowance --
    maintenance of $75 a policy a year inflating at 2.5% on the valuation clock
    (:func:`inflation_factor`), spread evenly over the months, and $300 of claim expense
    per death.  ``ULSG_US_S``'s formula in its order, on the policies in force at the
    start of the month: in the issue month those are the policies issued,
    :func:`pols_new_biz`, since a point issued at or after the valuation date opens with
    none, so acquisition is charged per policy issued, as in ``basiclife.BasicTerm_SE``,
    and a point in force past its first policy year never bears it.  On a point issued at
    ``t = 0`` this is ``ULSG_US_S``'s charge bit for bit.

    Zero outside cover, where the count carried into ``t = proj_len()`` would otherwise
    bear a maintenance expense.  Not to be confused with :func:`maint_fee`, which is the
    *charge against the account value*.
    """
    if not is_active(t):
        return 0.0
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    if policy_year(t) == 1:
        acq = acq + expense_acq_prem_rate * premium_pp(t)            # noqa: F821
    return ((acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821
            + expense_claim * pols_death(t))


def premium_taxes(t):
    """Percent-of-premium expense, **zero** on this product.

    The universal life chassis carries a 2.5% premium tax; the guaranteed-UL notes'
    expense list has no percent-of-premium item at all -- the commission sits inside
    the acquisition expense instead -- so the rate is zero and the cell is kept only
    so ``result_cf()`` has the chassis' shape.  Adding a tax here would be an
    unsourced assumption.
    """
    return premium_tax_rate * premiums(t)


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``pi x GP + withdrawal fees + the deduction's non-COI part actually taken
    + surrender charges collected + the account value left behind by a policy
    terminating in grace - expenses - premium taxes``.  The last of those is zero by
    construction, because the account value is exhausted before a grace can begin; it
    is carried so :func:`check_margin` closes without a special case.
    """
    return (load_prem_rate() * premiums(t)
            + wd_fees(t)
            + maint_fee(t)
            + surr_charge(t)
            + claims_from_av(t, GRACE)
            - expenses(t)
            - premium_taxes(t))


def margin_mortality(t):
    """Mortality margin: :func:`coi` net of :func:`claims_over_av`.

    Deeply negative once the account value is exhausted: the cost of insurance is
    forgone while the death benefit is still the whole face amount.  That is the
    "negative account economics" regime the notes describe, and it is what dominates
    late-duration guaranteed UL liability cash flows.
    """
    return coi(t) - claims_over_av(t)


def margin_rop(t):
    """Return-of-premium margin: the account value released less the refund paid.

    ``(AV_t - claim_pp(t, REFUND)) x pols_rop(t)``.  Large and negative on a
    thin-account product, which is the point of the endorsement: it is an option
    against the insurer whose cost depends on cumulative premiums against the reserve
    released.
    """
    return (av_pp(t) - claim_pp(t, REFUND)) * pols_rop(t)


def net_cf(t):
    """Net liability cash flow in month t, **undiscounted**.

    ``premiums - death claims - surrender payments - refunds - withdrawal payments
    - expenses - premium taxes``.  Income-positive, as in every model of this library.
    Withdrawals are subtracted here as :func:`withdrawals` rather than through
    :func:`claims`, which no longer carries them.

    Like the rest of this library the model projects *gross liability cash flows*:
    there is no discounting and no change in account value in this figure, because
    reserves are a separate layer that consumes these flows.  Loads, charges, interest
    credits and every shadow-account entry are internal transfers and do not appear --
    see :func:`check_margin` for how they reconcile.  Zero outside cover.
    """
    return (premiums(t) - claims(t) - withdrawals(t)
            - expenses(t) - premium_taxes(t))


def check_av_roll_fwd():
    """Check the base account value roll-forward.

    Returns ``True`` when, for every month of the frame, the opening account value in
    force of month ``t + 1`` equals::

        av_at(t, BEF_PREM)
            + prem_to_av(t)
            - withdrawals(t) - wd_fees(t)
            - mth_deduction(t)
            + inv_income(t)
            - claims_from_av(t, DEATH) - claims_from_av(t, LAPSE)
            - claims_from_av(t, REFUND) - claims_from_av(t, GRACE)

    to within ``1e-9``, relative to the larger of the two and 1, which is what
    ``ULSG_US_S``'s ``math.isclose`` tests with both its tolerances at ``1e-9``.  This
    pins the notes' processing order: that interest is credited on the
    *post-deduction* balance, that decrements come after the credit, and that what
    leaves the account is the deduction actually taken and not the deduction
    scheduled.  Each month's residual is :func:`check_av_roll_fwd_resid`, so a failure
    can be found by month; a residual that is not a number fails, and one that is not
    real raises, as ``ULSG_US_S``'s check does.  In the last month the opening value of
    ``t + 1`` is the account value the survivors carry into ``t = proj_len()``.
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
    that a value that is not real raises here, as ``ULSG_US_S``'s ``math.isclose`` raises
    on it: a monthly rate built from an annual one past 1, ``1 - (1 - q)^(1/12)``, is
    complex, and so is every count after it, and a complex residual's magnitude would
    pass.  Zero outside cover, before ``t + 1`` is read, so that nothing reads a month
    past ``t = proj_len()``.
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
          - claims_from_av(t, LAPSE)
          - claims_from_av(t, REFUND)
          - claims_from_av(t, GRACE))
    nxt = av_at(t + 1, BEF_PREM)
    return float((nxt - av) / max(abs(nxt), abs(av), 1.0))


def check_sg_roll_fwd():
    """Check the shadow account roll-forward, per policy.

    Returns ``True`` when, for every month of the frame::

        sg_pp(t) == sg_pp_at(t, BEF_PREM) + prem_to_sg_pp(t) - wd_pp(t)
                    - sg_deduction_pp(t) + sg_inv_income_pp(t)

    to within ``1e-9``, relative to the larger side and 1, as for
    :func:`check_av_roll_fwd`, where the opening balance is the previous month's close, or
    ``sg_pp_init()`` in the first month on the books.  The shadow account is notional and
    carries no decrements, so this is a per-policy identity with no in-force weighting.
    It is the check that the shadow account is never floored: if a zero floor crept in,
    this would fail the moment the balance went negative.  Each month's residual is
    :func:`check_sg_roll_fwd_resid`, and a residual that is not a number fails.
    """
    for t in range(proj_len()):
        if not abs(check_sg_roll_fwd_resid(t)) <= 1e-9:
            return False
    return True


def check_sg_roll_fwd_resid(t):
    """The shadow account roll-forward's relative residual in month t; zero everywhere.

    The closing shadow balance :func:`sg_pp` less the roll-forward of month t that
    :func:`check_sg_roll_fwd` sets out, over the larger of the two in magnitude and 1, as
    :func:`check_av_roll_fwd_resid` measures its own, and a ``float``, as it is.  It reads
    no month but its own.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    sg = (sg_pp_at(t, BEF_PREM) + prem_to_sg_pp(t) - wd_pp(t)
          - sg_deduction_pp(t) + sg_inv_income_pp(t))
    end = sg_pp(t)
    return float((end - sg) / max(abs(end), abs(sg), 1.0))


def check_margin():
    """Check the net cash flow against the expense, mortality and refund margins.

    Returns ``True`` when, for every month of the frame::

        net_cf(t) == margin_expense(t) + margin_mortality(t) + margin_rop(t)
                     + av_change(t) - inv_income(t)
                     + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)

    to within ``1e-9``, relative to the larger side and 1, as for
    :func:`check_av_roll_fwd`; each month's residual is :func:`check_margin_resid`, and a
    residual that is not a number fails.  The last three terms are what separates a
    *gross liability cash flow* model from ``CashValue_SE``, whose ``net_cf`` already nets
    the change in account value and the investment income; the loan term is the debt a
    surrender recovers out of the cash value, which is the whole loan while the cash value
    covers it and the cash value once the loan exceeds it, where :func:`ncsv_pp` pays
    nothing.  ``ULSG_US_S``'s identity takes the whole loan in every month, so it is off
    by ``(csv_pp(t) - loan_bal_pp(t)) x pols_lapse(t)`` once the loan exceeds the cash
    value, and its check fails on a projection that is right; on every shipped model point
    no loan is outstanding, and the two checks agree.
    """
    for t in range(proj_len()):
        if not abs(check_margin_resid(t)) <= 1e-9:
            return False
    return True


def check_margin_resid(t):
    """The margin identity's relative residual in month t; zero everywhere.

    ``net_cf(t)`` less the three margins, the change in account value, the investment
    income and the loan a surrender recovers, that :func:`check_margin` sets out, over the
    larger of the two sides in magnitude and 1, as :func:`check_av_roll_fwd_resid` measures
    its own, and a ``float``, as it is.  Zero outside cover, before :func:`av_change`
    would read ``t + 1``.
    """
    if not is_active(t):
        return 0.0
    rhs = (margin_expense(t) + margin_mortality(t) + margin_rop(t)
           + av_change(t) - inv_income(t)
           + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t))
    lhs = net_cf(t)
    return float((lhs - rhs) / max(abs(lhs), abs(rhs), 1.0))


def result_cf():
    """Result table of cashflows, a DataFrame indexed by month ``t``.

    One row per month ``t = 0 .. proj_len() - 1`` from the valuation date, the same month
    for every model point, so the frames of a block line up and sum row by row, and a
    point issued after the valuation date has zeros until its issue month;
    ``len(result_cf()) == proj_len()``.  The columns are ``ULSG_US_S``'s.  ``pols_if`` is
    the in-force weight applied to that same row's cash flows -- the number in force at
    the **start** of the month -- and the remaining columns are income-positive under
    ``net_cf``: ``premiums - claims_death - claims_lapse - claims_rop - withdrawals -
    expenses - premium_taxes``.  The three claim columns are the cells
    :func:`claims_death`, :func:`claims_lapse` and :func:`claims_refund`, ``ULSG_US_S``'s
    kinds ``DEATH``, ``LAPSE`` and ``REFUND``; the surrender column is ``claims_lapse``,
    matching the ``LAPSE`` kind that produces it, and withdrawals are their own column
    rather than a claim.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims_death(t) for t in ts],
            "claims_lapse": [claims_lapse(t) for t in ts],
            "claims_rop": [claims_refund(t) for t in ts],
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
    month t; ``pols_new_biz``, the part of it issued in month t; then month t's deaths,
    surrenders, refund exercises and terminations in grace, in ``ULSG_US_S``'s order, and
    its maturities, which are always zero.  Row by row, ``pols_if`` at ``t + 1`` is
    ``pols_if`` less the four outflows of month t, plus the new business of month
    ``t + 1``, or 0 once the policy has lapsed.  Then ``ULSG_US_S``'s two monthly
    decrement rates, which are 0 outside cover, where the model reads no rate.
    """
    ts = list(range(proj_len()))
    rows = []
    for t in ts:
        active = is_active(t)
        rows.append((pols_if(t), pols_new_biz(t), pols_death(t), pols_lapse(t),
                     pols_rop(t), pols_lapse_grace(t), pols_maturity(t),
                     mort_rate_mth(t) if active else 0.0,
                     lapse_rate_mth(t) if active else 0.0))
    return pd.DataFrame(                                             # noqa: F821
        rows,
        columns=["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_rop",
                 "pols_lapse_grace", "pols_maturity", "mort_rate_mth",
                 "lapse_rate_mth"],
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the two account values, per policy.

    The columns are the columns of the worked example in the technical notes, in the
    notes' own order -- premium, net premium to each account, the deductions on each,
    the interest credited to each, the two closing balances -- followed by the forgone
    deduction, which the notes write inline in the deductions cell, and the status.  The
    status column holds ``ULSG_US_S``'s label of each month's :func:`status` code, the
    text ``ULSG_US_S``'s cell returns, ``"IN FORCE"`` for ``IN_FORCE`` and
    ``"IN FORCE - GUARANTEE"`` for ``IN_FORCE_GUARANTEE`` among them, so that the table
    reads as ``ULSG_US_S``'s: the labels are written here, a reporting cell, and nowhere
    else.
    """
    labels = ("PRE_ISSUE", "IN FORCE", "IN FORCE - GUARANTEE", "GRACE", "LAPSED",
              "CEASED")
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "premium_pp": [premium_pp(t) for t in ts],
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "mth_deduction_pp": [mth_deduction_pp(t) for t in ts],
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "prem_to_sg_pp": [prem_to_sg_pp(t) for t in ts],
            "sg_deduction_pp": [sg_deduction_pp(t) for t in ts],
            "sg_inv_income_pp": [sg_inv_income_pp(t) for t in ts],
            "sg_pp": [sg_pp(t) for t in ts],
            "forgone_pp": [mth_deduction_forgone_pp(t) for t in ts],
            "status": [labels[status(t)] for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_guar():
    """Result table of the guarantee diagnostics, a DataFrame indexed by month ``t``.

    The net amount at risk and cost of insurance on each account, the deduction the
    insurer forgoes across the policies in force -- the running cost of the guarantee --
    the shadow account net of debt, whether the guarantee is active, the catch-up
    premium that would restore it and the grace counter.  One row per month
    ``t = 0 .. proj_len() - 1`` from the valuation date, as in :func:`result_cf`, zeros and
    ``False`` before the issue of a point written later.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "net_amt_at_risk": [net_amt_at_risk(t) for t in ts],
            "coi_pp": [coi_pp(t) for t in ts],
            "mth_deduction_forgone": [mth_deduction_forgone(t) for t in ts],
            "sg_net_amt_at_risk": [sg_net_amt_at_risk(t) for t in ts],
            "sg_coi_pp": [sg_coi_pp(t) for t in ts],
            "sg_net_pp": [sg_net_pp(t) for t in ts],
            "is_guar_active": [is_guar_active(t) for t in ts],
            "catch_up_prem_pp": [catch_up_prem_pp(t) for t in ts],
            "grace_mth": [grace_mth(t) for t in ts],
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

BEF_COI = 6

BEF_INV = 7

EOM = 8

BEF_INT = 9

DEATH = 0

LAPSE = 1

REFUND = 2

GRACE = 3

WITHDRAWAL = 4

MATURITY = 5

PRE_ISSUE = 0

IN_FORCE = 1

IN_FORCE_GUARANTEE = 2

LAPSED = 4

CEASED = 5

issue_age_min = 18

charges_cease_age = 121

lifetime_guarantee_age = 121

guar_rate_ann = 0.02

crediting_rate_curr = 0.035

sg_rate_ann = 0.055

coi_curr_factor = 0.65

coi_sg_factor = 0.55

load_prem_rate_sg = 0.08

expense_pol_mth = 5.5

expense_unit_mth = 0.2

expense_unit_mth_sg = 0.05

loan_rate_ann = 0.05

loan_cr_rate_ann = 0.03

wd_fee = 25.0

wd_first_year = 1

ten_pay_years = 10

prem_persistency_ann = 0.98

grace_months = 2

rop_cap_rate = 0.4

mort_ae_factor = 1.0

mort_improve_rate_init = 0.01

mort_improve_full_age = 85

mort_improve_end_age = 95

mort_improve_max_years = 20

lapse_guar_mult = 0.55

lapse_pattern_mult_single = 0.6

lapse_pattern_mult_ten_pay = 0.8

lapse_dyn_mult_guar_only = 0.6

lapse_dyn_mult_guar_failed = 2.0

lapse_rate_floor = 0.003

lapse_rate_cap = 0.5

expense_acq = 300.0

expense_acq_prem_rate = 0.9

expense_maint = 75.0

expense_claim = 300.0

inflation_rate = 0.025

premium_tax_rate = 0.0

pd = ("Module", "pandas")
