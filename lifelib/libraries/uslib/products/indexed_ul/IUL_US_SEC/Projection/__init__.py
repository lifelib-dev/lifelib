# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy monthly projection of the :mod:`~.IUL_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.IUL_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is: ``Projection[6]``
is an ItemSpace projecting the table's seventh row, model point 7, ``IUL_US_S``'s
monthly-premium point restated 65 months on, in force at the valuation date with all
twelve index segments live, and :func:`point_id` is its label::

    >>> Projection[0].result_av()          # the account value roll-forward
    >>> Projection[6].result_seg()         # the segment ladder, carried in
    >>> Projection[6].point_id()           # 7, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, an int set on a float Reference reads as a float, and text set on a code,
``basis`` or ``seg_credit_base_conv``, is refused with ``TypeError`` at assignment, where
modelx's cell refuses it as it reads it (``products/indexed_ul/model-sec.md``).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.IUL_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.IUL_US_S` is rewritten where it depends on the month its frame opens at, where it
must answer for a month outside cover, where it reads the index path, or where it reads a
table at a policy year or an attained age; every other is :mod:`~.IUL_US_S`'s own.
``products/indexed_ul/model-sec.md`` lists the rewritten cells with the reason for each.
Making it compile changed how each cell reads its inputs and spells its codes, and no
number: every model point attribute a projection cell uses is read as a number from a
``Data`` vector, every table as an array indexed by integers, the segment ladder among
them, every timing and kind is an int code, and so are the basis and the credit base's
convention (*Codes*, below). :mod:`~.IUL_US_S`'s ``coi_rate_scale``, a Series, is a
schedule number, :func:`coi_schedule`; its ``claims(t, kind=None)`` is two cells and
their total, :func:`claims_death`, :func:`claims_lapse` and :func:`claims`; its six
segment cells keyed by a segment's creation month, ``seg_bal_pp(t, m)`` and its
neighbours, are keyed by the segment's slot, its months since creation,
``seg_bal_pp(t, k)`` (*The segment ladder*, below); and its crediting engine, five cells
of float arguments, is inlined into cells keyed by the month, :func:`seg_return`,
:func:`seg_credit_rate` and :func:`index_credit_pp`, the five kept for its worked example
and called by no projection cell (*Reporting cells*, below).

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/indexed_ul/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas -- no ``_data/``, no
IOSpec, no embedded values -- so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IUL_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers live in the unparameterized :mod:`~.IUL_US_SEC.Data` Space, reached here
through the ``data`` Reference, so each file is read once per model rather than once
per model point. The six assumption tables are the files :mod:`~.IUL_US_S` reads, read
in place; the model point table and the segment ladder are this model's own:

======================  ================================  ==========================
Reference (on Data)     Cells                             File
======================  ================================  ==========================
model_point_file        data.model_point_table()          model_point_table_sec.csv
inforce_segments_file   data.inforce_segments()           inforce_segments_sec.csv
coi_rates_file          data.coi_rates()                  coi_rates.csv
corridor_file           data.corridor_factors()           corridor_factors.csv
mort_table_file         data.mort_table()                 mort_table.csv
class_factor_file       data.class_factor_table()         class_factor_table.csv
lapse_table_file        data.lapse_table()                lapse_table.csv
surr_charge_file        data.surr_charge_table()          surr_charge_table.csv
======================  ================================  ==========================

The index path is **not** a file. The base deterministic run generates
:func:`index_level` from a level annual return, and a historical or simulated path is
substituted by overriding that one cell, before the model computes anything: a formula
override, which only modelx can make; compiled, the path is changed by editing the
formula and rebuilding.

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however old the policy, month ``t`` runs from the monthiversary at time ``t`` to
the next, and the frame is ``t = 0, 1, ..., proj_len() - 1``, where :func:`proj_len`
counts the months from the valuation date to the end of the projection. Row ``t`` is the
same month for every point, so the frames of a block line up and sum row by row.

``duration_mth(t)`` counts **policy months**, the notes' own month index from issue:
``duration_mth(t) = duration_mth_init() + t``, where :func:`duration_mth_init` is read
from the model point -- positive for a policy in force at the valuation date, in any month
of its policy year, 0 for one issued at it, ``-k`` for one issued ``k`` months later, at
most ten years later. Everything contractual reads it: the anniversary premium
(``duration_mth(t) % 12 == 0``), the first policy years of the withdrawal and the loan,
the maturity of a segment twelve policy months after its creation, the surrender charge's
month, the no-lapse period and its expiry shock, the GPT and 7-pay years, the COI scale
and the lapse table by policy year, the mortality rate and the corridor factor at the
attained age, the policy-year steps of the per-unit charge and of the collateral's
credited rate, the cessation of premiums and charges at ``charges_cease_age`` and the end
of the projection at ``maturity_age``. The policy year is the 1-based contractual label
``policy_year(t) = duration(t) + 1`` and the attained age (ANB) is
``age(t) = age_at_entry() + duration(t)``, both derived and never indexed by. Point 7,
``IUL_US_S``'s point 4 restated 65 months on, is in policy year 6 at attained age 50 at
``t = 0``, and point 12, to be issued 25 months after the valuation date, is issued at
``t = 25``.

``IUL_US_S`` already counts its months from the start of its own projection rather than
from issue, but ships no point in force, and its in-force entry loses what a policy's past
has left it: it opens the fixed account at the account value less the loan, the loan
collateral at the loan, the face at issue, both premium accumulators at 0, and no index
segment before its first month. What the valuation clock adds is that ``t = 0`` is one
instant for every point, that a point may be issued after it, and that a point in force
brings in its whole state: the fixed account and the collateral apart from the loan, the
face in force, the premiums paid to date and the no-lapse accumulator, whether it has
failed the 7-pay test, and its live index segments.

The economic inputs read the valuation clock. The index path,
``index_level(t) = index_level_init x (1 + index_return_ann)^(t / 12)``, is one path for
every point, whose level at the valuation date is ``index_level_init``; ``IUL_US_S``
reads it at ``duration_mth(t)``, a path of each point's own from its issue. The cap in
force (:func:`index_cap_at`) and the fixed-account rate (:func:`fixed_rate_ann`) are read
at ``t``, and are level as shipped. Expense inflation is
``inflation_factor(t) = (1 + inflation_rate)^(t // 12)``, ``IUL_US_S``'s step by policy
year moved onto ``t``, so that the maintenance expense is in valuation-date dollars for
every point alike; it is 0 as shipped. Acquisition is charged per policy issued, in the
issue month, and is not inflated, as in ``basiclife.BasicTerm_SE``. The collateral's
credited rate and the per-unit charge step on the policy year, as terms of the contract.

A segment's credit is a ratio of two index levels, its level at maturity over its level at
creation, so moving the path onto the valuation clock moves no credit. A segment created
in the frame, at month ``t - 12``, reads ``index_level(t - 12)`` and the cap declared then,
``index_cap_at(t - 12)``; a segment created before the valuation date carries its start
level on the same path, the level ``IUL_US_S`` reads at its creation rebased so that the
path's level at the valuation date is ``index_level_init``, and the cap declared at its
creation (:func:`seg_index_start`, :func:`seg_index_cap`). What does move is the level
itself: on a point in force ``d`` months, ``index_level(t)`` is ``IUL_US_S``'s level at its
month ``t + d`` divided by ``(1 + index_return_ann)^(d / 12)``, and so is the
``index_level`` column of :func:`result_seg`.

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.IUL_US_S` computes: every cell the two share agrees at every argument
:mod:`~.IUL_US_S` evaluates in its sweep, but for four whose meaning changed:
``pols_if_init``, now the count already in force at the valuation date, ``model_point``,
a row of another table, ``result_pols``, which gains the month's new business, and
``check_margin``, whose identity this model states with the debt a surrender recovers (see
:func:`check_margin`). ``tests/test_model_conventions.py`` asserts it cell by cell.

The **value** state variables are closing balances at the end of month ``t``, the notes'
``X_{t+1}``: :func:`av_pp`, :func:`fa_pp`, :func:`lca_pp`, :func:`loan_bal_pp`,
``seg_bal_pp(t, k)``, :func:`sum_assured_at`, and the two premium accumulators,
:func:`cum_prem_pp` and :func:`cum_prem_net_pp`. The opening value of a month, the notes'
``X_t``, is the ``BEF_PREM`` timing of :func:`av_pp_at`, :func:`fa_pp_at` and
:func:`lca_pp_at`, or the previous month's value of the others, and at :func:`t_entry`,
the first month on the books, the model point's opening state instead, so that nothing is
ever asked for a month before the valuation date or before issue. For a point in force the
opening state is its row and its segments, per policy, as the policy stands at the start
of month 0, before any month-0 event: the account value and the loan, ``IUL_US_S``'s own
columns (:func:`av_pp_init`, :func:`loan_bal_init`); the fixed account and the loan
collateral (:func:`fa_pp_init`, :func:`lca_pp_init`); the face in force
(:func:`sum_assured_init`); the premiums less withdrawals paid to date and the no-lapse
accumulator, premiums less withdrawals and loans (:func:`cum_prem_init`,
:func:`cum_prem_net_init`); the MEC latch (:func:`is_mec_init`); and each live segment's
balance, deductions and draws to date, start level and cap, from the segment ladder (see
*The segment ladder*, below). At a mid-year valuation the current year's anniversary
premium and loan draw are already inside them. For a point issued at or after the
valuation date every one of them is 0, and the issue values come from the formulas, as
in ``IUL_US_S``.

Every chain is one cell a month. Each opening timing forms the previous month's close
itself, from its own value at ``t - 1`` and month ``t - 1``'s premium, credit, draws,
deduction, sweep and interest, the same operations in the same order as the closing cell
``IUL_US_S`` calls for, rather than calling for it: the account value's, where
``IUL_US_S``'s chain ran through five cells a month, the fixed account's, through six,
and the collateral's, through two. The loan, the face, the two premium accumulators, the
MEC latch, each segment's balance and running totals, and the count call themselves at
``t - 1``, one cell a month. A compiled model runs these chains on the C stack.

Within each month the notes' monthiversary order is followed exactly:

1. **Anniversary resets and premium.** The attained age and the corridor factor move
   on the policy anniversary (:func:`age`, :func:`corridor_factor`); the annual
   premium is received at BOM of the first month of each policy year and its load
   deducted (:func:`premium_pp`, :func:`prem_to_av_pp`), the net premium going to the
   fixed account.
2. **Segment maturity.** A segment created twelve months earlier matures: its index
   credit is computed (:func:`index_credit_pp`) and its whole value rolls into the
   fixed account (:func:`seg_roll_pp`), from which the sweep at step 7 re-enters it
   into a new segment under the standing instruction **[std]**.
3. **Withdrawals and new loans** are sourced fixed-account-first, then pro rata across
   live segments (:func:`draw_from_fa_pp`, :func:`draw_from_seg_pp`) -- the order one
   carrier gives for loans [S3]; for withdrawals, which that carrier takes pro rata
   across all unloaned accounts [S3], it is **[std]**; loan
   collateral moves into :func:`lca_pp`.
4. **Death benefit and corridor** on the post-premium, post-withdrawal account value
   (:func:`db_pp`).
5. **Net amount at risk**, the death benefit discounted one month at the
   **guaranteed** rate less the account value measured **before** the deduction
   (:func:`net_amt_at_risk`) -- the universal life base convention.
6. **Monthly deduction** (:func:`mth_deduction_pp`), sourced the same way as step 3
   (:func:`mth_deduction_from_fa_pp`, :func:`mth_deduction_from_seg_pp`), then the
   shortfall / no-lapse test (:func:`is_shortfall`).
7. **Sweep.** ``w_ix`` times the remaining fixed-account balance creates the new
   segment of this month (:func:`sweep_pp`, :func:`seg_new_pp`).
8. **Interest, EOM.** One month at the fixed-account rate on the post-sweep fixed
   balance and at the loan collateral rate on the collateral account
   (:func:`inv_income_pp`); **segments earn no interim interest** [S2]; loan interest
   accrues (:func:`loan_bal_pp`).
9. **Decrements, EOM**, death before lapse (:func:`pols_death`, :func:`pols_lapse`).

Cash flows are **undiscounted**. Premiums, expenses and premium taxes fall at BOM and
are weighted by :func:`pols_if`, the count in force at the **start** of month ``t``;
death claims by ``pols_if(t) * mort_rate_mth(t)``; surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``; and partial withdrawals by
``pols_if(t)`` again, because a withdrawal is taken at BOM on the owner's election and
is not a decrement.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, BEF_DECR)``, the
count carried in from ``t - 1`` (``BEF_NB``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, and before issue
(:func:`is_active`) every count, and so every cash flow, is zero, and so is every value
state. ``IUL_US_S`` already names three timings, in a cell that returns ``pols_if(t)``
for each and that nothing calls. ``BEF_DECR`` keeps that meaning, and so does
``BEF_MAT``, the count before any maturity, since nothing matures: the name keeps its
S model's meaning, as in the family's other models, and ``basiclife.BasicTerm_SE``'s
start-of-month ``BEF_MAT`` is not adopted. ``BEF_NB`` is the one timing this model
gives a new meaning, ``basiclife.BasicTerm_SE``'s, and it differs from ``IUL_US_S``'s
only in the issue month, where it counts the issued policies as new business, not yet
in. Inside the month the decrements are :mod:`~.IUL_US_S`'s, in its order: death, then
surrender. No policy is terminated for insufficiency, as in ``IUL_US_S``.

.. rubric:: The end of the projection

The frame ends at :func:`maturity_mth`, the policy month at attained age
``maturity_age``, 121, the notes' [unverified] maturity inference (spec F5), and not at an
event of the contract, which is described as continuing in force with no further charges
at 121. Premiums, withdrawals and charges stop at ``charges_cease_age``, a Reference of
its own, 121 too as shipped; set below ``maturity_age``, the projection runs on past the
cessation, the account value earning its interest and the segments their credits with
nothing deducted. The roll-forwards read the survivors of the last month:
:func:`check_av_roll_fwd` and :func:`av_change` read the opening account value in force
of month ``t + 1``, which in the last month is ``t = proj_len()``. So the two opening
values they read there, the count (the ``BEF_NB`` timing of :func:`pols_if_at`, and
through it :func:`pols_if`) and the account value (``av_pp_at(t, BEF_PREM)``), are
defined for ``0 <= duration_mth(t) <= maturity_mth()``: on the books, and in the month
after the frame, where they are the survivors of the last month and the account value they
carry. Each equals :mod:`~.IUL_US_S`'s value there exactly. Every other cell is zero or
false there, as before issue: each account inside the month and its opening value, each
segment, the loan, the face, every charge, premium, withdrawal, loan draw, credit,
decrement rate, decrement, claim and flow, and the expenses, whose maintenance would
otherwise fall on the carried count; only the two clocks, the inputs read on the valuation
clock and the neutral 1.0 of the two lapse multipliers hold values there. And nothing
reads past ``t = proj_len()``: :func:`av_change` and the residual cells of the checks,
which read ``t + 1`` or are read beside cells that do, are zero outside cover before they
read it.

.. rubric:: The segment ladder

A segment is created at every monthiversary from the sweep and matures twelve months
later, so between step 2 and step 7 of any month eleven segments are live and after the
sweep twelve are -- the "up to 12 segments" of [S4]. A segment is born in a policy month
``m``, ``duration_mth`` of the month of the sweep that created it, and in month ``t`` it
sits in **slot** ``k = duration_mth(t) - m``, its months since creation, 0 in its creation
month and 11 in the last month it is live: ``seg_bal_pp(t, k)`` is the balance at the end
of month ``t`` of the segment ``k`` months old then, and is zero outside
``0 <= k <= min(11, duration_mth(t))``. The six cells of a segment in a month,
:func:`seg_share`, :func:`seg_wd_pp`, :func:`seg_ded_pp`, :func:`seg_bal_pp`,
:func:`seg_ded_cum_pp` and :func:`seg_wd_cum_pp`, are keyed so, by ``(t, k)``, and each
reads its own value of the month before at ``(t - 1, k - 1)``, the same segment a month
younger: ``IUL_US_S`` keys them by ``(t, m)``, which a compiled cache would hold across
every creation month of the frame, where twelve slots hold the live ones. A segment's
creation balance, :func:`seg_new_pp`, is keyed by its creation month ``m``, a policy month,
as in ``IUL_US_S``: one value a segment. A parameter that holds a policy month is named
``m``, never ``t``, so that what moves with the valuation clock is ``t`` alone.

A point in force at the valuation date carries its live segments in a companion of the
model point table, ``inforce_segments_sec.csv``, one row a segment, keyed by ``point_id``
and ``slot``: the months since the segment's creation at the valuation date, 1 to 12, so
that the segment in slot ``k`` is the one born in policy month ``duration_mth_init() - k``
and the segment in slot 12 matures at ``t = 0``. The ladder's slot is the slot of month
0, so a segment carried in opens at ``t = 0`` from its own row: ``seg_bal_pp(0, k)``
from ``seg_bal_pp_init(k)``. Every month of the last
``min(12, duration_mth_init())`` holds a row, a month that swept nothing included, at
zero, since the credited rate of a month reads the start level and the cap of the segment
maturing then whether or not it holds a balance (:func:`cred_rate_ann`). Each row gives
the segment's balance entering month 0 (:func:`seg_bal_pp_init`), the deductions and the
draws -- withdrawals and loan transfers -- charged to it since its creation
(:func:`seg_ded_cum_pp_init`, :func:`seg_wd_cum_pp_init`), which with the balance are its
credit base, the index level at its creation on the valuation-clock path
(:func:`seg_index_start_init`) and the cap declared then (:func:`seg_index_cap_init`). Its
creation balance takes no column: nothing may enter or leave a segment but a deduction, a
withdrawal or a loan transfer, so it is the three summed, which is the closure
:func:`check_seg_ladder` asserts (:func:`seg_new_pp`).

Two properties of this arrangement are worth stating because the notes list both as
pitfalls.

Each segment carries **its own index start level**, so twelve segments a year mature at
twelve different point-to-point returns. Collapsing them into one annual segment
mis-times credits and distorts mid-segment surrender values [S3]; :func:`check_seg_ladder`
and model point 3 (indexed allocation 0%) exist so the difference is visible rather than
assumed.

Deductions and withdrawals are sourced from the fixed account first and then **pro rata
across live segments** on their remaining balances **[std]**. Because a pro-rata draw
leaves the proportions unchanged, one set of shares (:func:`seg_share`) serves both the
step-3 draw and the step-6 deduction. The two claims on the pool are **ordered, not
parallel**: the step-6 deduction is capped against what the step-3 draw leaves behind,
so their sum can never exceed the pool, no segment balance can go negative, and no
segment can pay a negative index credit at maturity. Capping both against the same
pre-draw pool is the easy mistake, and :func:`check_seg_ladder` asserts against it.
The credit base under the baseline convention is exactly the remaining balance --
amounts that left the segment mid-term earn no index credit [S3]. The alternative
convention the notes price, one carrier's adjusted-beginning-value with half-weighted
deductions [S3], is the ``ADJ_BEGIN`` argument of :func:`seg_credit_base`.

A segment can close a month on a rounding about zero, a balance of the order of 1e-16 of
either sign, where a draw or a deduction took exactly what it held. :func:`seg_share` and
:func:`seg_count` read such a balance by ``IUL_US_S``'s own tests of zero, and the pool
:func:`seg_bal_active_pp` and the total :func:`seg_bal_tot_pp` sum the segments in an
explicit loop that compensates as Python's ``sum()`` of floats does from Python 3.12, so
that each is ``IUL_US_S``'s sum bit for bit there. Python 3.11's ``sum()`` is a plain
fold, which can leave such a pool on the other side of zero, so the states ``IUL_US_S``
closes on a rounding about zero depend on the interpreter it runs on.

.. rubric:: Naming

Cell names follow :mod:`~.UL_US_S` -- the chassis these notes defer to -- and
through it lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``: ``pols_*``
for policy counts, ``av_*`` for account values, plural nouns for cash flows, ``*_rate``
for rates, ``*_pp`` for per-policy amounts, ``timing`` and ``kind`` arguments.
Every concept shared with the chassis carries the chassis name. The names that are new
in ``IUL_US_S`` are the ones the indexed crediting engine needs: the fixed (holding)
account, the segment ladder, the crediting formula, and the no-lapse guarantee test.

What running in force adds is named as ``basiclife.BasicTerm_SE`` names it:
``duration_mth`` read from the model point, ``policy_count``, ``pols_new_biz``,
``pols_if_at`` with its ``BEF_NB`` timing, ``is_active`` and ``result_pols``.
``t_entry``, the first month on the books, is the SEC models' own, and ``maturity_mth`` is
named for ``maturity_age``, where the projection ends. A column of the opening state is
the cell it opens with ``_init`` added: ``av_pp_init`` and ``loan_bal_init`` are
``IUL_US_S``'s own, and ``fa_pp_init``, ``lca_pp_init``, ``sum_assured_init``,
``cum_prem_init``, ``cum_prem_net_init`` and ``is_mec_init`` open :func:`fa_pp_at`,
:func:`lca_pp_at`, :func:`sum_assured_at`, :func:`cum_prem_pp`, :func:`cum_prem_net_pp`
and :func:`is_mec` as they open theirs. A column of the segment ladder is the segment
cell it opens with ``_init`` added, keyed by the slot: ``seg_bal_pp_init(k)``,
``seg_ded_cum_pp_init(k)`` and ``seg_wd_cum_pp_init(k)``; the start level and the cap,
which no cell of ``IUL_US_S`` holds per segment, are ``seg_index_start_init(k)`` and
``seg_index_cap_init(k)``, and the monthly cells that read them, for the segment maturing
in month ``t``, :func:`seg_index_start` and :func:`seg_index_cap`. A table read at an
attained age has one reader keyed by the age, ``<cell>_at(a)``, and a table read at a
policy year one keyed by the year, ``<cell>_py(y)``; the monthly cell keeps
``IUL_US_S``'s name and calls its reader inside cover. The surrender-charge schedule,
keyed by its ID, has one reader for each of its two columns, :func:`surr_charge_rate_max`
and :func:`surr_charge_runoff_years`. A check's residual in month ``t`` is
``<check>_resid(t)``. Each text column a monthly cell branches on is read through bool
decodes, one for each value, named for the value: :func:`is_db_option_a`,
:func:`is_db_option_b`, :func:`is_gpt`, :func:`is_level_premium`,
:func:`is_single_premium`, :func:`is_target_premium`, :func:`is_annual_premium` and
:func:`is_monthly_premium`. Each reads the vector ``Data`` decoded from its column, and
so does each per-point join, so no projection cell compares text or calls a label
accessor: ``IUL_US_S``'s label accessors, ``sex``, ``rate_class``, ``db_option``,
``qual_test``, ``premium_type``, ``premium_mode`` and ``surr_charge_id``, are kept as they
are, for reporting (*Reporting cells*, below). A segment's cell in a month is keyed by
its slot, ``k``, and a monthly cell of the segment maturing in month ``t`` is named for
the segment, ``seg_*(t)``: :func:`seg_return`, :func:`seg_credit_rate`,
:func:`seg_index_start` and :func:`seg_index_cap`.

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
t                          (the ``t`` argument)            Months from the valuation
                                                           date, 0-based
(months at valuation)      duration_mth_init               Completed policy months at the
                                                           valuation date; -k if issued k
                                                           months later
(notes' t, from issue)     duration_mth(t)                 Completed policy months at
                                                           month t
y                          policy_year(t)                  Policy year, 1-based,
                                                           ``duration(t) + 1``
(y - 1)                    duration(t)                     Completed policy years at BOM
(model point)              point_id()                      The point's label
(issue age)                age_at_entry                    Issue age (ANB)
Sex                        sex                             Sex, M or F
Risk class                 rate_class                      Underwriting class, spec
                                                           Table 1
DB option                  db_option                       Death benefit option, A or B
(Option A)                 is_db_option_a                  Whether db_option is A
(Option B)                 is_db_option_b                  Whether db_option is B
Tax test                   qual_test                       IRC 7702 test; only GPT
                                                           modeled
(GPT elected)              is_gpt                          Whether qual_test is GPT
Premium mode               premium_mode                    ANNUAL **[std]** or MONTHLY
(annual mode)              is_annual_premium               Whether premium_mode is ANNUAL
(monthly mode)             is_monthly_premium              Whether it is MONTHLY
x                          age(t)                          Attained age (ANB)
(none)                     proj_len                        Months from the valuation date
                                                           to the end of the projection
(projection end)           maturity_mth                    Policy month the projection
                                                           ends at, attained age 121
(none)                     t_entry                         First month on the books
(none)                     is_active(t)                    Whether month t is in cover
(none)                     policy_count                    Policies the model point
                                                           stands for
F                          sum_assured                     Initial face amount
F_0                        sum_assured_init                Face in force entering month 0
F_{t+1}                    sum_assured_at(t)               Face after reductions, end of
                                                           month t
F/1000                     units(t)                        Face in $1,000 units
P_t                        premium_pp(t)                   Gross premium per policy
(planned)                  premium_pp_ann                  Planned annual premium
(premium pattern)          premium_type                    LEVEL, SINGLE or TARGET
(LEVEL pattern)            is_level_premium                Whether premium_type is LEVEL
(SINGLE pattern)           is_single_premium               Whether it is SINGLE
(TARGET pattern)           is_target_premium               Whether it is TARGET
(persistency)              prem_persistency(t)             Paid/planned factor 0.98^(y-1)
l_prem                     load_prem_rate()                Premium load rate
NP_t                       prem_to_av_pp(t)                Net premium to the accounts
W_t                        wd_pp(t)                        Partial withdrawal, gross of
                                                           fee
(planned W)                wd_pp_mth                       The wd_pp column, a month's W
(the $25 fee)              wd_fee_pp(t)                    Withdrawal fee
B_t                        loan_new_pp(t)                  New standard loan
(planned B)                loan_new_pp_ann                 The loan_new_pp_ann column
W_t + B_t                  draw_pp(t)                      The whole step-3 draw
W^FA_t + B^FA_t            draw_from_fa_pp(t)              Step-3 draw sourced from FA
W^seg_{k,t} + B^seg_{k,t}  draw_from_seg_pp(t)             Step-3 draw sourced from
                                                           segments
(segment k's share)        seg_wd_pp(t, k)                 Segment k's part of that draw
(cumulative)               seg_wd_cum_pp(t, k)             Draws out of segment k to date
FA_{t+1}                   fa_pp(t)                        Fixed (holding) account, end
                                                           of month t
FA_t                       fa_pp_at(t, BEF_PREM)           Fixed account, start of
                                                           month t
(FA intra-month)           fa_pp_at(t, timing)             Fixed account by timing
FA_0                       fa_pp_init                      Fixed account entering month 0
S_{k,t+1}                  seg_bal_pp(t, k)                Segment in slot k, end of
                                                           month t
Sweep_t                    sweep_pp(t)                     Sweep into a new segment
S_{k,m_k}                  seg_new_pp(m)                   Segment balance at creation
(sum of segments)          seg_bal_tot_pp(t)               All live segment balances
(active pool)              seg_bal_active_pp(t)            Segments available to a draw
(pro-rata share)           seg_share(t, k)                 Segment k's share of that pool
(segment count)            seg_count(t)                    Live segments, at most 12
k                          (the ``k`` argument)            Slot, a segment's months since
                                                           creation: in month t, or at
                                                           the valuation date in the
                                                           ladder's ``_init`` cells
S_{k,0}                    seg_bal_pp_init(k)              Slot k's balance entering
                                                           month 0
(deductions to date)       seg_ded_cum_pp_init(k)          Deductions charged to slot k
(draws to date)            seg_wd_cum_pp_init(k)           Draws out of slot k
I(m_k)                     seg_index_start_init(k)         Slot k's level at creation
c_k                        seg_index_cap_init(k)           Cap declared at slot k's
                                                           creation
(start level at t)         seg_index_start(t)              Level at creation of the
                                                           segment maturing at t
(cap at t)                 seg_index_cap(t)                Cap of the segment maturing
                                                           at t
w_ix                       index_alloc_rate()              Indexed allocation share
I(t)                       index_level(t)                  Index level at monthiversary t
r_k                        index_change(i_0, i_1)          Point-to-point index change
(index path)               index_return_ann                Level annual index return
                                                           **[std]**
c                          index_cap_at(t)                 Cap in force
p                          index_par                       Participation rate
f                          index_floor                     Floor
cr_k                       index_credit_rate(r)            max(f, min(c, p x r)), engine
(the segment's cr_k)       seg_credit_rate(t)              The same, of the segment
                                                           maturing at t
(credit base)              seg_credit_base(...)            Balance the credit applies to
Credit_k                   index_credit(...)               Index credit, engine form
(matured value)            seg_matured_value(...)          Value rolling into the next
                                                           segment
(the segment's r)          seg_return(t)                   Index change of the segment
                                                           maturing at t
(credit at t)              index_credit_pp(t)              Credit added at BOM of month t
Roll^FA_t                  seg_roll_pp(t)                  Matured value rolled into FA
LCA_{t+1}                  lca_pp(t)                       Loan collateral account, end
                                                           of month t
LCA_0                      lca_pp_init                     Collateral entering month 0
Existing loan balance      loan_bal_init                   L(0), the loan entering
                                                           month 0
L_{t+1}                    loan_bal_pp(t)                  Loan plus interest, end of
                                                           month t
i_L^c                      loan_rate_ann                   Loan charged rate
i_L^e                      loan_credit_rate_ann(t)         Collateral credited rate
AV_{t+1}                   av_pp(t)                        Account value, end of month t
AV_t                       av_pp_at(t, BEF_PREM)           Account value, start of
                                                           month t
AV_0                       av_pp_init                      Account value entering month 0
(after premium)            av_pp_at(t, BEF_CREDIT)         Before the maturity credit
(after credit)             av_pp_at(t, BEF_WD)             Before the withdrawal
AV'_t                      av_pp_at(t, BEF_FEE)            After premium and withdrawal
AV'_t - MD_t               av_pp_at(t, BEF_INV)            After the monthly deduction
(aggregate AV)             av_at(t, timing)                Account value in force
(change in AV)             av_change(t)                    Change in account value
i_fix                      fixed_rate_ann(t)               Fixed-account annual rate
i_g                        guar_rate_ann                   Guaranteed annual rate
(i_fix monthly)            inv_return_mth(t)               Monthly fixed-account rate
(i_g monthly)              guar_rate_mth()                 Monthly guaranteed rate
v_g                        naar_factor()                   1 + i_gm; DB is divided by it
(interest credited)        inv_income_pp(t)                Interest on FA and LCA
e_pol                      expense_pol_mth_at(t)           Monthly policy fee
e_unit                     expense_unit_mth_at(t)          Per-unit charge per $1,000
(rider charges)            rider_charge_pp(t)              Rider charges (0)
(e_pol + e_unit + rc)      maint_fee_pp(t)                 Non-COI monthly charges
coi_t                      coi_rate(t)                     Current monthly COI rate
(guaranteed COI)           coi_rate_guar(t)                Guaranteed maximum COI rate
(guaranteed COI scale)     coi_schedule()                  The scale's number in Data
(scale's last year)        coi_rate_last_year()            The scale's last policy year
(COI by policy year)       coi_rate_guar_py(y)             The scale's rate in year y
COI_t                      coi_pp(t)                       Cost of insurance charge
NAAR_t                     net_amt_at_risk(t)              Net amount at risk
MD_t                       mth_deduction_pp(t)             Monthly deduction
MD^FA_t                    mth_deduction_from_fa_pp(t)     Deduction sourced from FA
MD^seg_{k,t}               mth_deduction_from_seg_pp(t)    Deduction sourced from
                                                           segments
(segment k's deduction)    seg_ded_pp(t, k)                Segment k's part of the
                                                           deduction
(cumulative deductions)    seg_ded_cum_pp(t, k)            Deductions charged to
                                                           segment k
DB_t                       db_pp(t)                        Death benefit after corridor
kappa_x                    corridor_factor(t)              IRC 7702(d) corridor factor
(kappa by age)             corridor_factor_at(a)           The same, keyed by age
SC_t                       surr_charge_pp(t)               Surrender charge scheduled
(SC per $1,000)            surr_charge_rate(t)             Surrender charge rate
(initial SC per $1,000)    surr_charge_rate_max()          The schedule's charge before
                                                           any run-off
(run-off period)           surr_charge_runoff_years()      The schedule's run-off, years
(AV - SC)                  csv_pp(t)                       Cash value before loan
CSV_t                      ncsv_pp(t)                      Cash surrender value, loan
                                                           netted
(SC retained)              surr_charge(t)                  Surrender charge collected
CumP_{t+1}                 cum_prem_net_pp(t)              Premiums less withdrawals and
                                                           loans, end of month t
CumP_0                     cum_prem_net_init               The same, entering month 0
(GPT/7-pay base)           cum_prem_pp(t)                  Premiums less withdrawals,
                                                           end of month t
(GPT/7-pay base at entry)  cum_prem_init                   The same, entering month 0
CumMNLP_{t+1}              cum_mnlp_pp(t)                  Cumulative no-lapse premium
                                                           through month t
(MNLP rate)                mnlp_rate()                     No-lapse premium per $1,000
                                                           p.a.
(MNLP monthly)             mnlp_pp_mth()                   Monthly no-lapse premium
(no-lapse period)          nlg_period_years()              Length of the no-lapse period
(no-lapse test)            nlg_test_ok(t)                  CumP >= CumMNLP
(NLG status)               nlg_in_effect(t)                In period and test passing
(NLG expiry shock)         nlg_expiry_shock(t)             25% shock at expiry **[std]**
(grace trigger)            is_shortfall(t)                 CSV cannot cover MD, NLG
                                                           failed
(GPT limit)                gpt_limit(t)                    max(GSP, GLP x years)
(GPT test)                 gpt_ok(t)                       GPT compliance flag
(7-pay limit)              seven_pay_limit(t)              7-pay cumulative limit
(MEC flag)                 is_mec(t)                       7-pay failure, latched
(MEC at entry)             is_mec_init                     The latch entering month 0
q^d_t                      mort_rate_mth(t)                Monthly mortality rate
(annual q)                 mort_rate(t)                    Annual mortality rate, capped
(base q by age)            mort_rate_base_at(a)            The base table's rate
(class factor)             class_factor()                  Underwriting-class multiplier
(base lapse)               lapse_rate_base(t)              Base annual lapse rate
(base lapse by year)       lapse_rate_base_py(y)           The same, keyed by policy year
(SC-expiry year)           lapse_shock_year()              Policy year of the spike
(SC-expiry spike)          lapse_rate_sc_mult(t)           Year-11 shock multiplier
r_cred,t                   cred_rate_ann(t)                Trailing credited rate
r_alt                      comp_rate_ann(t)                Competitor / market rate
(dynamic multiplier)       lapse_rate_dyn_mult(t)          Dynamic lapse multiplier
q^w_t                      lapse_rate_mth(t)               Monthly lapse rate
(annual w)                 lapse_rate(t)                   Total annual lapse rate
l_t                        pols_if(t)                      In force at BOM of month t
(l at valuation)           pols_if_init                    In force at the valuation date
(carried in)               pols_if_at(t, BEF_NB)           Carried in from month t - 1
(after new business)       pols_if_at(t, BEF_DECR)         After new business: l_t
(before maturity)          pols_if_at(t, BEF_MAT)          Before maturity: l_t
(new business)             pols_new_biz(t)                 Policies issued in month t
(deaths)                   pols_death(t)                   Deaths in month t
(lapses)                   pols_lapse(t)                   Lapses in month t
(maturities)               pols_maturity(t)                Maturities: always zero
(premium income)           premiums(t)                     Premium income
DB_t - L_t                 claims_death(t)                 Death claims
CSV_t                      claims_lapse(t)                 Surrender payments
(claims)                   claims(t)                       Death and surrender claims
W_t - fee                  withdrawals(t)                  Withdrawal payments
(inflation)                inflation_factor(t)             Expense inflation factor
E_t                        expenses(t)                     Insurer's own expenses
(premium tax)              premium_taxes(t)                Premium tax
(net loan cash flows)      net_loan_cf(t)                  Loan advances and repayments
CF_t                       net_cf(t)                       Net liability cash flow
(AV components residual)   check_av_components_resid(t)    AV less its three parts
(AV roll residual)         check_av_roll_fwd_resid(t)      AV roll-forward residual
(margin residual)          check_margin_resid(t)           Margin identity residual
(segments over the term)   check_seg_count_resid(t)        Live segments beyond 12
(the month's credit)       check_seg_credit_resid(t)       The credit, 0 or more
(least segment)            check_seg_bal_resid(t)          The least live balance
(segment closure)          check_seg_closure_resid(t)      The maturing segment's closure
(none)                     result_pols()                   Counts and decrement rates
=========================  ==============================  ==========================

Ten names needed care.

**A withdrawal is not a claim.** The notes write the withdrawal outflow as its own term
of ``CF_t``, alongside the death and surrender legs, and the library follows that: the
payment is :func:`withdrawals`, published in a ``withdrawals`` column, and
``WITHDRAWAL`` is **not** a kind :func:`claims` totals -- it would otherwise sit in the
total and be double-counted against the standalone cells.
The per-policy amount is still ``claim_pp(t, WITHDRAWAL)``, because that is
where the ``W_t - $25 fee`` rule lives and :func:`withdrawals` weights it by
:func:`pols_if`: a withdrawal is taken at BOM by policies still in force, not by a
decrement. Surrenders keep the ``LAPSE`` kind and are published as ``claims_lapse``,
so the column name matches the kind that produces it.

**The notes' month counts from issue; this model's counts from the valuation date.** The
notes' ``t`` and this model's are both 0-based and they coincide for a point issued at the
valuation date; for any other the notes' index is :func:`duration_mth`
``(t) = duration_mth_init() + t``.
Every ``mod 12`` test -- the anniversary premium, the anniversary loan -- is therefore
written against ``duration_mth(t)`` rather than ``t``, a segment's creation is a policy
month, and the surrender charge run-off uses ``duration_mth(t) + 1`` because the notes'
schedule counts the current month.

**A segment's slot is not its creation month.** ``IUL_US_S`` keys ``seg_bal_pp(t, m)``
and the segment cells beside it by ``m``, the policy month the segment was born in; this
model keys them by the slot, ``k = duration_mth(t) - m``, the months since that birth in
month ``t``, which moves with ``t``, so that ``seg_bal_pp(t, k)`` reads
``seg_bal_pp(t - 1, k - 1)``, and :func:`seg_new_pp` alone keeps the creation month. The
ladder's ``slot`` is the slot of month 0, ``duration_mth_init() - m``, which is what an
extract of a policy's live segments knows, and what one row of
``inforce_segments_sec.csv`` is keyed by.

**The notes' cash surrender value is the net one.** Their ``CSV_t`` is :func:`ncsv_pp`,
not :func:`csv_pp`: the notes define ``CSV_t = AV_t - SC_t - L_t``, with the loan already
netted. The chassis and
``CashValue_SE`` split that into :func:`csv_pp` (``AV - SC``) and :func:`ncsv_pp`
(``CSV - L``). The chassis names are kept, and the notes' symbol maps to the second.

**The withdrawal fee is inside the withdrawal, not on top of it.** These notes say
``W_t`` is "gross of $25 fee" and that the "withdrawal outflow = W_t - $25 fee". The
account is therefore debited ``W_t``, the policyholder receives ``W_t - 25`` and the
insurer keeps the fee. The universal life chassis reads its own notes the other way --
there the fee is charged *on top* of the withdrawal -- so :func:`av_pp_at` deliberately
differs from the chassis at ``BEF_FEE``. A planned withdrawal above 0 and below the fee
would debit the account less than the fee it is charged, which :func:`proj_len` refuses.

**The death claim nets the loan at the end of the month.** These notes write
``death claim outflow = DB_t - L_t``; decrements are end-of-month events, after the
loan has accrued, so :func:`claim_pp` uses :func:`loan_bal_pp` at ``t``. The chassis
uses the opening balance because its own notes write ``L(t-1)``.

**The maintenance fee is income, the expenses outgo.** As on the chassis,
:func:`maint_fee_pp` is the non-COI part of the monthly deduction -- a charge *against
the account value* -- while :func:`expenses` is the insurer's own $75 a year plus $150
at issue **[std]**. Confusing them double-counts.

**The two cumulative premium accumulators are different.** :func:`cum_prem_net_pp` is
the notes' ``CumP_t``, premiums less withdrawals **and loans**, which is what the
no-lapse test compares against ``CumMNLP_t``. :func:`cum_prem_pp` is premiums less
withdrawals only, which is the base of the guideline premium and 7-pay tests. Using one
for the other quietly changes both answers, and so does opening either at 0 on a point in
force: each opens from a column of its own, :func:`cum_prem_init` and
:func:`cum_prem_net_init`.

**The MEC flag latches here, and does not in the S model.** ``IUL_US_S``'s flag is the
in-year 7-pay test alone, which stops applying in policy year 8 and so switches the flag
off exactly when the failure becomes permanent. This model latches it, as ``UL_US_S``
does, from :func:`is_mec_init` on a point in force: under IRC 7702A a contract that fails
the test is a modified endowment contract for good [R5].

**The fixed account and the collateral are not the account value less the loan.**
``IUL_US_S`` opens an in-force point with everything in the fixed account and the
collateral equal to the loan. Both part from those after the first loan: the collateral
is credited at :func:`loan_credit_rate_ann` while the loan accrues at ``loan_rate_ann``,
and the segments hold the rest of the account value. So each opens from its own column,
:func:`fa_pp_init` and :func:`lca_pp_init`, and the segments from the ladder; ``Data``
holds the account value to the sum of the three parts.

.. rubric:: Codes

What :mod:`~.IUL_US_S` spells as text, a timing, a kind, the basis or the credit base's
convention, is here an int Reference named as the text it replaces, so that every cell
takes and returns C numbers. A call site reads as it did, less the quotes:
``pols_if_at(t, BEF_DECR)``, ``av_pp_at(t, BEF_FEE)``, ``claim_pp(t, DEATH)``,
``basis = GUARANTEED``.

=============  =====  ===============================================================
Reference      Value  Meaning
=============  =====  ===============================================================
BEF_NB         0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR       1      :func:`pols_if_at`: that count plus month t's new business
BEF_MAT        2      :func:`pols_if_at`: before any maturity, the BEF_DECR count
BEF_PREM       3      the accounts: the value carried in, before the premium
BEF_CREDIT     4      :func:`fa_pp_at`, :func:`av_pp_at`, :func:`av_at`: after the net
                      premium, before the maturing segment's credit
BEF_WD         5      :func:`fa_pp_at`, :func:`av_pp_at`, :func:`av_at`: after the
                      credit, before the withdrawal and the loan
BEF_FEE        6      :func:`fa_pp_at`, :func:`av_pp_at`, :func:`av_at`: after the
                      draws, before the monthly deduction
BEF_SWEEP      7      :func:`fa_pp_at`: after the deduction, before the sweep
BEF_INV        8      the accounts: after the deduction and the sweep, before interest
EOM            9      :func:`av_at`: after interest, before decrements
DEATH          0      :func:`claim_pp`, :func:`claims_from_av`: the death claim
LAPSE          1      :func:`claim_pp`, :func:`claims_from_av`: the surrender claim
MATURITY       2      :func:`claims_from_av`: none, the contract never matures
WITHDRAWAL     3      :func:`claim_pp`: the withdrawal, which is no claim
CURRENT        0      ``basis``: the current, non-guaranteed scales
GUARANTEED     1      ``basis``: the contractual guarantees alone
REMAINING      0      ``seg_credit_base_conv``: the credit on the remaining balance
ADJ_BEGIN      1      ``seg_credit_base_conv``: the adjusted beginning value, deductions
                      half-weighted
=============  =====  ===============================================================

The accounts are :func:`fa_pp_at`, which takes the six timings from ``BEF_PREM`` to
``BEF_INV``; :func:`av_pp_at`, which takes those but ``BEF_SWEEP``, since a sweep moves
value between the account value's parts and changes no total; :func:`lca_pp_at`, which
moves only at the loan, ``BEF_PREM`` and ``BEF_INV``; and :func:`av_at`, the account value
in force, which takes :func:`av_pp_at`'s five and ``EOM``.

The model has two families of timing, the count's and the accounts', passed to different
cells, and they are numbered as one: ``BEF_NB`` 0 and ``BEF_DECR`` 1, as in every SEC
model, then the count's third, ``BEF_MAT``, then the accounts' in the order of their
instants within the month, ``EOM`` last, as ``UL_US_SEC`` numbers its own with the two
instants an indexed account adds, ``BEF_CREDIT`` and ``BEF_SWEEP``, in their places. So no
two timings share a code, and a code of one family passed to the other's cell,
``av_pp_at(t, BEF_NB)``, is refused as any timing the cell does not take is,
``ValueError("invalid timing")``, in both engines, rather than read as a timing of the
cell's own. Kinds are numbered in the order the month settles them, as ``VUL_US_SEC``
numbers its own. ``basis`` and ``seg_credit_base_conv``, the two text References
``IUL_US_S`` switches on, are code families of their own, each holding one of its codes,
``CURRENT`` and ``REMAINING`` as shipped: a run on the guaranteed basis sets
``basis = GUARANTEED`` before anything computes, and in modelx a string set on either
meets its cell's own refusal, ``"invalid basis"`` or ``"invalid credit base"``. A cell
compares its code with ``==`` alone, never by order or by membership of a tuple, so that
a text passed where a code is taken meets the cell's own refusal in modelx too. A timing
or a kind indexes its cell's cache, a C array of twelve codes a month, since every 2-D
cache of the model has one width, the twelve slots of a segment's life
(``spec_sec.py``), so codes are numbered densely from 0. They are References, not cells,
so the symbol map does not list them. Every other Reference is named in lower case,
``issue_age_min`` and ``issue_age_max`` among them, the contract's issue ages, which
:func:`proj_len` refuses a point outside of, and the first of which the compiled model's
caches are sized from.

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`sex`, :func:`rate_class`,
:func:`db_option`, :func:`qual_test`, :func:`premium_type`, :func:`premium_mode` and
:func:`surr_charge_id`, the reports :func:`result_cf`, :func:`result_pols`,
:func:`result_av` and :func:`result_seg`, and the checks :func:`check_av_components`,
:func:`check_av_roll_fwd`, :func:`check_seg_ladder` and :func:`check_margin` are written
for a reader and for the comparison with :mod:`~.IUL_US_S`, which has every one of them: a
table row, text, DataFrames and four verdicts. No other cell calls them: each reads the
number ``Data`` decoded from the same column instead, the decodes' flags, the schedule
numbers and the joins the keys select. So the row, the text and the frames stay Python
when the model compiles. A label accessor returns its column as read, text or not: a
blank ``surr_charge_id`` on a point without a charge reads as NaN, and the compiled
accessor returns the same. Every other cell returns a C ``bint``, ``long long`` or
``double``, and so do the four checks, which may stay Python but compile to a ``bint``,
their verdict, as their per-month residuals, ``*_resid``, compile to a ``double``.

The crediting engine of ``IUL_US_S``, :func:`index_change`, :func:`index_credit_rate`,
:func:`seg_credit_base`, :func:`index_credit` and :func:`seg_matured_value`, cells of
float arguments, is kept as it is, for its worked example, which prices one segment's
credit at the current and the guaranteed cap through it, and for the comparison with
:mod:`~.IUL_US_S`, whose projection calls it. No projection cell here calls it: the credit
of the segment maturing in month ``t`` is :func:`seg_return`, :func:`seg_credit_rate` and
:func:`index_credit_pp`, cells keyed by the month, which compute what the engine computes
in its order. Compiled, the five keep a Python dict for a cache and Python objects for
their defaulted parameters, as the registry admits them (R14).
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
    :func:`proj_len` to the ages the contract issues, 0 to 85.
    """
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point.

    A reporting cell (the Space docstring): ``Data`` joins the COI scale by it, through
    ``Data.coi_schedule``, and no projection cell reads it here.  Returned as read.
    """
    return model_point()["sex"]


def rate_class():
    """The underwriting class of the selected model point (spec Table 1) [S3].

    A reporting cell (the Space docstring): ``Data`` joins the COI scale and the class
    factor by it, through ``Data.coi_schedule`` and ``Data.class_factor``, and no projection
    cell reads it here.  Returned as read.
    """
    return model_point()["rate_class"]


def sum_assured():
    """F: the initial face amount of the selected model point, the face at issue.

    The surrender charge is quoted per $1,000 of this, the *initial* face, not of
    :func:`sum_assured_at` [S3], and it is the face a point not yet in force is issued
    with.  The face in force at the valuation date is :func:`sum_assured_init`, and the
    face in force in month t is :func:`sum_assured_at`.
    """
    return float(data.sum_assured()[idx])                            # noqa: F821


def db_option():
    """The death benefit option: ``"A"`` (level) or ``"B"`` (face plus account value).

    The Graded and Return of Premium options are minority designs excluded from the
    baseline by the product spec (F3).  A reporting cell (the Space docstring): the
    projection reads :func:`is_db_option_a` and :func:`is_db_option_b`, ``Data``'s decodes
    of the column.  Returned as read.
    """
    return model_point()["db_option"]


def is_db_option_a():
    """Whether the death benefit is Option A, the level face.

    ``Data.is_db_option_a`` at the point: ``db_option`` is ``"A"``, the decode of the model
    point's column ``Data`` makes once for the table, compared exactly, as ``IUL_US_S``
    compares it, so that no monthly cell branches on text; :func:`db_pp` and
    :func:`face_reduction_pp` read this instead.  The label accessor :func:`db_option` is
    kept as it is, for reporting, and no projection cell calls it.
    """
    return bool(data.is_db_option_a()[idx])                          # noqa: F821


def is_db_option_b():
    """Whether the death benefit is Option B, the face plus the account value.

    ``Data.is_db_option_b`` at the point: ``db_option`` is ``"B"``, read by :func:`db_pp`,
    which raises on a point that is neither A nor B, as ``IUL_US_S``'s does.
    """
    return bool(data.is_db_option_b()[idx])                          # noqa: F821


def qual_test():
    """The IRC 7702 qualification test elected at issue; only ``"GPT"`` is modeled.

    GPT is the baseline (spec F4) because the Overloan Protection Rider attaches only
    to GPT non-MEC policies [S3]; CVAT is documented as a variation, so
    :func:`corridor_factor` raises on anything else rather than silently applying GPT
    corridor factors.  A reporting cell (the Space docstring): the projection reads
    :func:`is_gpt`, ``Data``'s decode of the column.  Returned as read.
    """
    return model_point()["qual_test"]


def is_gpt():
    """Whether the point elected the Guideline Premium Test: ``qual_test`` is ``"GPT"``.

    ``Data.is_gpt`` at the point, the decode of the model point's ``qual_test`` column, read
    by :func:`corridor_factor`, which raises on any other test, as ``IUL_US_S``'s does: CVAT
    is documented as a variation, out of the baseline.
    """
    return bool(data.is_gpt()[idx])                                  # noqa: F821


def premium_type():
    """The premium pattern: ``"LEVEL"``, ``"SINGLE"`` or ``"TARGET"`` **[std]**.

    A reporting cell (the Space docstring): the projection reads :func:`is_level_premium`,
    :func:`is_single_premium` and :func:`is_target_premium`, ``Data``'s decodes of the
    column.  Returned as read.
    """
    return model_point()["premium_type"]


def is_level_premium():
    """Whether the premium pattern is LEVEL: ``premium_type`` is ``"LEVEL"``.

    ``Data.is_level_premium`` at the point: one of the three decodes of the model point's
    ``premium_type`` column that :func:`premium_pp` branches on, each made once for the
    table by ``Data``, so that no monthly cell compares text; :func:`premium_pp` raises on a
    point that is none of the three, as ``IUL_US_S``'s does.  The label accessor
    :func:`premium_type` is kept as it is, for reporting, and no projection cell calls it.
    """
    return bool(data.is_level_premium()[idx])                        # noqa: F821


def is_single_premium():
    """Whether the premium pattern is SINGLE: ``premium_type`` is ``"SINGLE"``.

    ``Data.is_single_premium`` at the point, a decode of the model point's ``premium_type``
    column, read by :func:`premium_pp`.
    """
    return bool(data.is_single_premium()[idx])                       # noqa: F821


def is_target_premium():
    """Whether the premium pattern is TARGET: ``premium_type`` is ``"TARGET"``.

    ``Data.is_target_premium`` at the point, a decode of the model point's ``premium_type``
    column, read by :func:`premium_pp`, whose TARGET premium is capped inside the guideline
    premium limit.
    """
    return bool(data.is_target_premium()[idx])                       # noqa: F821


def premium_mode():
    """The premium mode: ``"ANNUAL"`` **[std]** baseline, or ``"MONTHLY"``.

    The notes fix the baseline at annual premiums paid at BOM of the first month of
    each policy year (``duration_mth(t) % 12 == 0``) **[std]**; monthly mode is carried
    so the chassis' level-pay pattern remains reachable.  A reporting cell (the Space
    docstring): the projection reads :func:`is_annual_premium` and
    :func:`is_monthly_premium`, ``Data``'s decodes of the column.  Returned as read.
    """
    return model_point()["premium_mode"]


def is_annual_premium():
    """Whether premiums are paid annually: ``premium_mode`` is ``"ANNUAL"``.

    ``Data.is_annual_premium`` at the point: one of the two decodes of the model point's
    ``premium_mode`` column that :func:`premium_pp` branches on, made once for the table by
    ``Data``, so that no monthly cell compares text; :func:`premium_pp` raises on a point
    that is neither, as ``IUL_US_S``'s does.  The label accessor :func:`premium_mode` is
    kept as it is, for reporting, and no projection cell calls it.
    """
    return bool(data.is_annual_premium()[idx])                       # noqa: F821


def is_monthly_premium():
    """Whether premiums are paid monthly: ``premium_mode`` is ``"MONTHLY"``.

    ``Data.is_monthly_premium`` at the point, a decode of the model point's ``premium_mode``
    column, read by :func:`premium_pp`.
    """
    return bool(data.is_monthly_premium()[idx])                      # noqa: F821


def premium_pp_ann():
    """The planned annual premium per policy; a billing target only, premiums flexible."""
    return float(data.premium_pp_ann()[idx])                         # noqa: F821


def index_alloc_rate():
    """w_ix: the share of the sweepable fixed-account balance moved to the indexed account.

    100% in the baseline **[std]**.  A model point at 0% never creates a segment and
    accumulates entirely at the fixed-account rate, which is the control run for the
    segment ladder.
    """
    return float(data.index_alloc_rate()[idx])                       # noqa: F821


def av_pp_init():
    """AV(0): the account value per policy entering month 0, the valuation month.

    The ``av_pp_init`` column, ``IUL_US_S``'s own: the balance at the close of policy
    month ``duration_mth_init() - 1``, before any month-0 event, which is what
    ``IUL_US_S`` carries into the month as ``av_pp_at(d, BEF_PREM)`` at
    ``d = duration_mth_init()``.  It opens the account value chain at :func:`t_entry` on a
    point issued at or after the valuation date, 0 there.  A point in force opens the chain
    from its parts instead, which ``Data`` holds this column to, so that an extract whose
    amounts are carried to the cent opens one account (see :func:`av_pp_at`).  Zero for a
    point not yet in force, which is issued with no account value.

    The account value is the fixed account, the live segments and the loan collateral,
    and each of the three opens from a value of its own -- :func:`fa_pp_init`, the
    segment ladder and :func:`lca_pp_init` -- where ``IUL_US_S`` places the whole opening
    balance less the loan in the fixed account and starts with no live segment.  ``Data``
    holds this column to their sum, to the cent.  It may be negative: ``IUL_US_S`` lapses
    no policy for insufficiency, and charges an exhausted policy on, so its point 5's
    account value closes below zero from policy month 604, and a point restated after
    that month carries that balance (see the model docstring).
    """
    return float(data.av_pp_init()[idx])                             # noqa: F821


def loan_bal_init():
    """L(0): the policy loan balance per policy entering month 0.

    The ``loan_bal_init`` column, ``IUL_US_S``'s own: the debt at the close of policy
    month ``duration_mth_init() - 1``, interest accrued to then included, before any
    month-0 event; the opening balance of :func:`loan_bal_pp` at :func:`t_entry`, and the
    loan month 0's shortfall test nets.  Zero for a point not yet in force.
    ``IUL_US_S`` also opens its loan collateral account from it, taking the collateral
    equal to the debt; here the collateral opens from a column of its own,
    :func:`lca_pp_init`, since the two part once interest accrues.
    """
    return float(data.loan_bal_init()[idx])                          # noqa: F821


def fa_pp_init():
    """FA(0): the fixed (holding) account per policy entering month 0.

    The ``fa_pp_init`` column: the fixed account at the close of policy month
    ``duration_mth_init() - 1``, before any month-0 event, which is what ``IUL_US_S``
    carries into the month as ``fa_pp_at(d, BEF_PREM)``.  It is the opening balance of
    :func:`fa_pp_at` at :func:`t_entry`.  ``IUL_US_S`` opens its in-force points with the
    account value less the loan here, everything outside the collateral in the fixed
    account and no live segment, which re-opening a policy restates wrongly: the segments
    hold most of an account value whose allocation is indexed, and the collateral is not
    the loan once interest accrues.

    It may be negative.  ``IUL_US_S`` lapses no policy for insufficiency, and its fixed
    account carries every deduction and draw the segments cannot cover, so an exhausted
    policy's fixed account runs below zero: its point 5's closes below zero from policy
    month 383.  ``Data`` holds it, with the collateral and the segments, to
    :func:`av_pp_init`.  Zero for a point not yet in force.
    """
    return float(data.fa_pp_init()[idx])                             # noqa: F821


def lca_pp_init():
    """LCA(0): the loan collateral account per policy entering month 0.

    The ``lca_pp_init`` column: the collateral at the close of policy month
    ``duration_mth_init() - 1``, before any month-0 event, which is what ``IUL_US_S``
    carries into the month as ``lca_pp_at(d, BEF_PREM)``.  It is the opening balance
    of :func:`lca_pp_at` at :func:`t_entry`, and part of the account value, as the debt
    is not.  A standard loan moves value out of the fixed account and the segments into
    the collateral, so the two coincide on the loan's first day, and ``IUL_US_S`` takes
    them equal at the start of its frame **[std]**; after that the collateral grows at the
    rate credited, :func:`loan_credit_rate_mth`, and the debt at the rate charged,
    :func:`loan_rate_mth`, so they part.  ``Data`` refuses a collateral without a loan, or
    a loan without one.  Zero for a point not yet in force.
    """
    return float(data.lca_pp_init()[idx])                            # noqa: F821


def sum_assured_init():
    """F(0): the face amount in force per policy entering month 0.

    The ``sum_assured_init`` column: the face in force at the close of policy month
    ``duration_mth_init() - 1``, after every Option A withdrawal cut to date, which is
    the face ``IUL_US_S`` carries into the month as ``sum_assured_at(d - 1)``.  It is the
    base of :func:`sum_assured_at` at :func:`t_entry`, so month 0's own withdrawal cut,
    death benefit, net amount at risk and per-unit charge are measured from it.  The face
    at issue, :func:`sum_assured`, stays the surrender charge's base, and ``Data`` refuses
    a value above it, since face increases are not modelled.  It may be 0: withdrawals
    under Option A can cut the face to nothing while the policy stays in force, as
    ``IUL_US_S`` carries it.  Zero for a point not yet in force, which is issued at
    :func:`sum_assured`.  ``IUL_US_S`` opens its in-force points at the face at issue.
    """
    return float(data.sum_assured_init()[idx])                       # noqa: F821


def cum_prem_init():
    """CumPrem(0): the premiums less withdrawals per policy before the valuation date.

    The ``cum_prem_init`` column: every gross premium :func:`premium_pp` collected from
    issue through policy month ``duration_mth_init() - 1``, less every withdrawal
    :func:`wd_pp` paid, which is what ``IUL_US_S`` carries into the month as
    ``cum_prem_pp(d - 1)``.  :func:`cum_prem_pp` opens from it at :func:`t_entry`, so the
    GPT test, the 7-pay test and the TARGET premium cap of month 0 all count the premiums
    paid before the valuation date.  ``IUL_US_S`` opens its accumulator at 0 on any point,
    the notes giving no opening accumulator **[std]**, so its flags are meaningful only
    for points projected from issue.

    It may be negative.  The statutory "less a portion of withdrawals" is taken as the
    whole withdrawal **[std]**, so this is a tax measure, not a balance, and withdrawals
    can exceed the premiums paid.  Zero for a point not yet in force.
    """
    return float(data.cum_prem_init()[idx])                          # noqa: F821


def cum_prem_net_init():
    """CumP(0): premiums less withdrawals and loans per policy before the valuation date.

    The ``cum_prem_net_init`` column, the no-lapse guarantee's accumulator: every gross
    premium collected from issue through policy month ``duration_mth_init() - 1``, less
    every withdrawal and every new loan, which is what ``IUL_US_S`` carries into the month
    as ``cum_prem_net_pp(d - 1)``.  :func:`cum_prem_net_pp` opens from it at
    :func:`t_entry`, so the no-lapse test of month 0 compares every premium since issue
    with the cumulative minimum no-lapse premium since issue, which :func:`cum_mnlp_pp`
    counts on the policy clock.  Opened at 0, as ``IUL_US_S`` opens it, a policy in force
    would fail that test at once and lose its guarantee.

    It may be negative, as loans can exceed the premiums paid net of withdrawals; ``Data``
    holds it to at most :func:`cum_prem_init`, to a cent and a half, since loans only
    lower it.
    Zero for a point not yet in force.
    """
    return float(data.cum_prem_net_init()[idx])                      # noqa: F821


def is_mec_init():
    """The MEC latch entering month 0: whether the 7-pay test failed before it.

    The ``is_mec_init`` column, an int code: 1 for a policy that failed the 7-pay test in
    some month before the valuation date, and so is a modified endowment contract for
    good, 0 otherwise.  :func:`is_mec` latches on it at :func:`t_entry`, so a policy that
    failed in its first seven years stays a MEC after them, where the in-year test no
    longer applies.  ``IUL_US_S``'s flag does not latch, so the generator reads whether
    its in-year test failed in any month before ``duration_mth_init()``.  ``Data``
    refuses a 0 where ``cum_prem_init`` already exceeds the 7-pay limit of the month
    before the valuation date, inside the first seven policy years.  Read as a bool, so
    1.0 reads as True.  Zero for a point not yet in force.
    """
    return bool(data.is_mec_init()[idx])                             # noqa: F821


def seg_bal_pp_init(k):
    """S_k(0): the balance per policy entering month 0 of the segment in ladder slot k.

    ``Data.seg_bal_pp_init`` at this point and slot ``k``, the ``seg_bal_pp_init`` column
    of ``inforce_segments_sec.csv``: ``k`` is the months since the segment's creation at
    the valuation date, and the value is the balance at the close of policy month
    ``duration_mth_init() - 1`` of the segment born in policy month
    ``duration_mth_init() - k``, which is what ``IUL_US_S`` carries into the month as
    ``seg_bal_pp(d - 1, d - k)``.  :func:`seg_bal_pp` opens each live segment from it at
    :func:`t_entry`, its slot then the ladder's, :func:`seg_bal_active_pp` sums slots 1 to
    11 into month 0's pool, and slot 12, the segment maturing at ``t = 0``, is what month
    0's maturity rolls into the fixed account (:func:`seg_roll_pp`).  ``Data`` holds it to
    ``-1e-8`` or more, the tolerance :func:`check_seg_ladder` holds a live balance to, and
    :func:`proj_len` refuses a point whose ladder does not hold exactly slots 1 to
    ``min(12, duration_mth_init())``.  Read only on a point in force, at
    ``1 <= k <= 12``.  Like the other four readers of the ladder, it asks :func:`proj_len`
    first, so that a ladder missing a slot is refused by
    name before any value of it is read, and then refuses a slot below 1 or past the point's
    last, naming the point and the slot, where stage ``E``'s ``.loc`` raised pandas'
    ``KeyError``, so that no read meets ``Data``'s padding.
    """
    proj_len()
    if k < 1 or k > data.inforce_segment_last()[idx]:                # noqa: F821
        raise ValueError(f"point_id {point_id()}: inforce_segments_sec.csv holds no "
                         f"segment in slot {k}")
    return float(data.seg_bal_pp_init()[idx, k])                     # noqa: F821


def seg_ded_cum_pp_init(k):
    """The deductions per policy charged to the segment in ladder slot k before month 0.

    ``Data.seg_ded_cum_pp_init`` at the point and slot ``k``, the ``seg_ded_cum_pp_init``
    column of ``inforce_segments_sec.csv``: every monthly deduction the segment born in
    policy month ``duration_mth_init() - k`` has borne since its creation, through the close
    of policy month ``duration_mth_init() - 1``, which is ``IUL_US_S``'s
    ``seg_ded_cum_pp(d - 1, d - k)``.  With the balance and the draws it is the segment's
    credit base: :func:`seg_ded_cum_pp` opens from it at :func:`t_entry`, and in slot 12
    :func:`index_credit_pp` reads it at ``t = 0``, where the credit base convention
    ``ADJ_BEGIN`` half-weights it.  Read only on a point in force, at ``1 <= k <= 12``,
    after :func:`proj_len`, and refused, as :func:`seg_bal_pp_init` refuses it, at a slot
    the point does not hold.
    """
    proj_len()
    if k < 1 or k > data.inforce_segment_last()[idx]:                # noqa: F821
        raise ValueError(f"point_id {point_id()}: inforce_segments_sec.csv holds no "
                         f"segment in slot {k}")
    return float(data.seg_ded_cum_pp_init()[idx, k])                 # noqa: F821


def seg_wd_cum_pp_init(k):
    """The draws per policy out of the segment in ladder slot k before month 0.

    ``Data.seg_wd_cum_pp_init`` at the point and slot ``k``, the ``seg_wd_cum_pp_init``
    column of ``inforce_segments_sec.csv``: every withdrawal and loan transfer the segment
    born in policy month ``duration_mth_init() - k`` has paid since its creation, through
    the close of policy month ``duration_mth_init() - 1``, which is ``IUL_US_S``'s
    ``seg_wd_cum_pp(d - 1, d - k)``.  :func:`seg_wd_cum_pp` opens from it at
    :func:`t_entry`, and in slot 12 :func:`index_credit_pp` reads it at ``t = 0``.  Read
    only on a point in force, at ``1 <= k <= 12``, after :func:`proj_len`, and refused, as
    :func:`seg_bal_pp_init` refuses it, at a slot the point does not hold.
    """
    proj_len()
    if k < 1 or k > data.inforce_segment_last()[idx]:                # noqa: F821
        raise ValueError(f"point_id {point_id()}: inforce_segments_sec.csv holds no "
                         f"segment in slot {k}")
    return float(data.seg_wd_cum_pp_init()[idx, k])                  # noqa: F821


def seg_index_start_init(k):
    """I(m_k): the index level at the creation of the segment in ladder slot k.

    ``Data.seg_index_start_init`` at the point and slot ``k``, the ``seg_index_start_init``
    column of ``inforce_segments_sec.csv``: the index level the segment born in policy month
    ``duration_mth_init() - k`` started from, on this model's path, the valuation clock's,
    whose level at the valuation date is ``index_level_init``: ``IUL_US_S``'s level at the
    segment's creation month times ``index_level_init`` over its level at month
    ``duration_mth_init()``.  So the segment's return at maturity, a ratio of two levels, is
    ``IUL_US_S``'s.  Read for the segment maturing in month ``t < 12`` by
    :func:`seg_index_start`, and only on a point in force, at ``1 <= k <= 12``, after
    :func:`proj_len`; ``Data`` holds it above 0, since the return divides by it, and it is
    refused, as :func:`seg_bal_pp_init` refuses it, at a slot the point does not hold.
    """
    proj_len()
    if k < 1 or k > data.inforce_segment_last()[idx]:                # noqa: F821
        raise ValueError(f"point_id {point_id()}: inforce_segments_sec.csv holds no "
                         f"segment in slot {k}")
    return float(data.seg_index_start_init()[idx, k])                # noqa: F821


def seg_index_cap_init(k):
    """c_k: the cap declared at the creation of the segment in ladder slot k.

    ``Data.seg_index_cap_init`` at the point and slot ``k``, the ``seg_index_cap_init``
    column of ``inforce_segments_sec.csv``: the cap in force when the segment born in policy
    month ``duration_mth_init() - k`` was created, which its credit at maturity is capped
    at, the cap being re-declared at every segment start [S3][S4].  ``IUL_US_S`` holds the
    cap level, so every segment carries :func:`index_cap_at`'s value; the column lets a cap
    re-declared at the valuation date apply to new segments only.  Read for the segment
    maturing in month ``t < 12`` by :func:`seg_index_cap`, and only on a point in force, at
    ``1 <= k <= 12``, after :func:`proj_len`; ``Data`` holds it to 0 or more, and it is
    refused, as :func:`seg_bal_pp_init` refuses it, at a slot the point does not hold.
    """
    proj_len()
    if k < 1 or k > data.inforce_segment_last()[idx]:                # noqa: F821
        raise ValueError(f"point_id {point_id()}: inforce_segments_sec.csv holds no "
                         f"segment in slot {k}")
    return float(data.seg_index_cap_init()[idx, k])                  # noqa: F821


def policy_count():
    """The number of policies the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the policies in force then, before any
    month-0 event; any other point counts the policies it issues.  Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second.  Every per-policy value --
    the accounts, the segments, the loan, the face, the opening state -- is the same
    whatever the count, and every cash flow is a per-policy amount weighted by it.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """Policies in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose policies
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``.  So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count.  ``IUL_US_S``'s cell of the name is the notes'
    ``l(0)``, the count at the start of its frame, which on new business is the issued
    count.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 60 for point 6 and 888 for point 11,
    ``IUL_US_S``'s point 1 on its fifth anniversary and two years before the end of its
    projection, 0 for a policy issued at the valuation date, and -25 for point 12, to be
    issued 25 months after it, which ``Data`` admits up to ``future_horizon_mth`` months
    ahead.  This is the notes' issue-date / duration offset attribute, an elapsed count
    and therefore already 0-based, and ``IUL_US_S``'s cell and column of the same name,
    which count from the first month of its own frame; here that month is the valuation
    date for every point, and the count may be negative.  It is the one fact the policy
    clock takes from the model point.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def has_surr_charge():
    """Whether a surrender charge schedule applies to this model point.

    ``Data.has_surr_charge`` at the point: its ``has_surr_charge`` column, which ``Data``
    holds to True or False in any case.
    """
    return bool(data.has_surr_charge()[idx])                         # noqa: F821


def surr_charge_id():
    """The surrender charge schedule ID, a row label of *surr_charge_table.csv*.

    A reporting cell (the Space docstring): ``Data`` joins the schedule by it, through
    ``Data.surr_charge_rate_max`` and ``Data.surr_charge_runoff_years``, and no projection
    cell reads it here.  Returned as read: a blank id on a point without a charge is NaN.
    """
    return model_point()["surr_charge_id"]


def surr_charge_rate_max():
    """The schedule's charge per $1,000 of initial face, before any of it runs off.

    ``Data.surr_charge_rate_max`` at the point: the ``sc_per_1000_init`` column of the
    point's row of *surr_charge_table.csv*, $25.00 on the shipped ``IUL10`` schedule;
    :func:`surr_charge_rate` runs it off from here.  ``Data`` joins the schedule to the
    points by ``surr_charge_id`` once it has checked the table, so that no projection cell
    reads the table or the id, and refuses the table, naming every point, where a point that
    :func:`has_surr_charge` names an id the table lacks, which ``IUL_US_S``'s ``.loc`` met
    in every month of its cover.  :func:`surr_charge_rate` reads it only where
    :func:`has_surr_charge` is true, but a point without a charge reads its schedule too, as
    at stage ``E``, where the table holds its id; where it does not,
    ``Data.has_surr_charge_schedule`` is 0, and this raises ``ValueError``, naming the
    point, where stage ``E``'s refused it.
    """
    value = float(data.surr_charge_rate_max()[idx])                  # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise ValueError(f"point_id {point_id()}: surr_charge_table.csv has no row for "
                         f"its surr_charge_id")
    return value


def surr_charge_runoff_years():
    """The number of policy years over which the schedule's charge runs off, linearly.

    ``Data.surr_charge_runoff_years`` at the point: the ``runoff_years`` column of the
    point's row of *surr_charge_table.csv*, 10 on the shipped ``IUL10`` schedule, read as a
    float, as ``IUL_US_S`` reads it, and joined, checked and refused as
    :func:`surr_charge_rate_max` is.  ``Data`` holds it to a whole number of years, 1 or
    more, so that the division in :func:`surr_charge_rate` never meets 0 and
    :func:`lapse_shock_year`'s ``int()`` of it changes nothing, and to below ``2**53`` years
    on a point with a charge, where that ``int()`` is exact.
    """
    value = float(data.surr_charge_runoff_years()[idx])              # noqa: F821
    if not data.has_surr_charge_schedule()[idx]:                     # noqa: F821
        raise ValueError(f"point_id {point_id()}: surr_charge_table.csv has no row for "
                         f"its surr_charge_id")
    return value


def wd_first_year():
    """The first policy year in which a withdrawal may be taken.

    2 in the shipped points: withdrawals are allowed after the free-look period [S3]
    and the model takes that as the first anniversary **[std]**.
    """
    return int(data.wd_first_year()[idx])                            # noqa: F821


def wd_pp_mth():
    """The planned partial withdrawal per policy, in each month withdrawals are allowed.

    The model point's ``wd_pp`` column, a monthly amount, gross of the $25 fee and **0 in
    the baseline** [std]; model point 5 takes $200 a month.  Read once a point here, so
    that :func:`wd_pp`, a monthly cell on the accounts' chains, reads no model point
    column in its own formula.  ``Data`` holds it to 0 or more, and
    :func:`proj_len` refuses one above 0 and below the fee.
    """
    return float(data.wd_pp()[idx])                                  # noqa: F821


def loan_first_year():
    """The first policy year in which the distribution-scenario loan is drawn.

    The notes' loan utilization module borrows a level amount annually from a start
    age, e.g. 65 **[std]**; 21 for issue age 45 is that age expressed as a policy year.
    """
    return int(data.loan_first_year()[idx])                          # noqa: F821


def loan_new_pp_ann():
    """The planned standard loan per policy, drawn at each anniversary loans are taken.

    The model point's ``loan_new_pp_ann`` column, **0 in the baseline** -- the notes set
    loan utilization to none -- and $6,000 a year on model point 5.  Read once a point
    here, so that :func:`loan_new_pp`, a monthly cell on the accounts' and the loan's
    chains, reads no model point column in its own formula.  ``Data`` holds it to 0 or
    more.
    """
    return float(data.loan_new_pp_ann()[idx])                        # noqa: F821


def mnlp_rate():
    """The minimum monthly no-lapse premium rate per $1,000 of face, annualized [S3].

    20.80 for M / Non-Tobacco / 45 / band 1 [S3]: the entry in one carrier's base
    annual minimum premium rate table for faces of $25,000-$99,999, which that carrier
    does not label as MNLP rates, so reading it as the annualized MNLP is **[std]**.
    The 250,000 example face falls in the same carrier's $100,000-and-up table, which
    gives 11.32 for the same cell [S3]; the band-1 rate stands in **[std]**.
    """
    return float(data.mnlp_rate()[idx])                              # noqa: F821


def gsp():
    """The guideline single premium (GPT compliance input) **[std]** placeholder.

    No retrieved source gives guideline premiums for this composite, so the shipped
    value is a plausible placeholder, not a computed IRC 7702 figure.
    """
    return float(data.gsp()[idx])                                    # noqa: F821


def glp():
    """The guideline level premium (GPT compliance input) **[std]** placeholder."""
    return float(data.glp()[idx])                                    # noqa: F821


def seven_pay_prem():
    """The 7-pay premium (IRC 7702A compliance input) **[std]** placeholder [R5]."""
    return float(data.seven_pay_prem()[idx])                         # noqa: F821


def duration_mth(t):
    """Completed policy months at the beginning of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together.  A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame.  It is the notes' own month index, 0 in the
    issue month -- ``t = 0`` for a point issued at the valuation date -- and negative
    before issue.  Anniversary events test ``duration_mth(t) % 12 == 0``, and a segment's
    creation month, the ``m`` of :func:`seg_new_pp`, is a value of it, its slot in month
    ``t``, the ``k`` of :func:`seg_bal_pp`, ``duration_mth(t) - m``.
    """
    return duration_mth_init() + t


def duration(t):
    """Completed policy years at the beginning of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year, as in lifelib, and negative before issue.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y: the policy year containing month t, the 1-based contractual label.

    ``duration(t) + 1``.  Derived, never indexed by: it is what the policy-year-keyed
    schedules -- the COI scale, the lapse table, ``wd_first_year``, ``loan_first_year``,
    the no-lapse period -- are looked up with.  It is 0 or less before issue, where no
    table is read by it: each reader is called inside cover only (:func:`is_active`).
    """
    return duration(t) + 1


def age(t):
    """The attained age (ANB) in month t: ``age_at_entry() + duration(t)``.

    Attained age increments on the policy anniversary, not on the birthday, which is
    the ANB convention the whole model is built on **[std]** (spec Table 1, F1).  It is
    the issue age throughout the first policy year, and below it before issue, where no
    table is read at it.
    """
    return age_at_entry() + duration(t)


def maturity_mth():
    """The policy month at which the projection ends, the first at attained age 121.

    ``12 * (maturity_age - age_at_entry())``: 912 at issue age 45.  The projection runs to
    attained age 121 **[std]**, the notes' [unverified] maturity inference (spec F5), so
    the last month of the frame, ``maturity_mth() - 1``, is the last at attained age 120.
    It is ``IUL_US_S``'s frame from issue, counted on the policy clock; :func:`proj_len`
    counts from the valuation date instead.  The contract is described as continuing in
    force at 121 with no further charges, so the horizon truncates the run rather than
    terminating the policy: where lives survive the last month, the count and the account
    value they carry into this month are kept (see :func:`pols_if_at`).  Premiums and
    charges cease at ``charges_cease_age``, a Reference of its own, 121 too as shipped,
    which may be set inside the frame.
    """
    return 12 * (maturity_age - age_at_entry())                      # noqa: F821


def proj_len():
    """The number of months from the valuation date to the end of the projection.

    ``maturity_mth() - duration_mth_init()``: 912 for a policy issued at age 45 at the
    valuation date, 852 for point 6, in force 60 months, and 937 for point 12, issued 25
    months after the valuation date.  The frame is ``t = 0, 1, ..., proj_len() - 1``;
    ``proj_len()`` is its exclusive end, the row count of every result table, and
    ``proj_len() - 1`` is the frame's last month, the last at attained age 120.  The
    contract is described as continuing in force at 121 with no further charges, so the
    horizon truncates the run rather than terminating the policy; :func:`pols_maturity`
    is identically zero, and the count and the account value the survivors carry into
    ``t = proj_len()`` are kept (see :func:`maturity_mth`).

    Six kinds of point raise here, naming the point, rather than projecting, each checked
    in this order: one to be issued at or past attained age 121, which would never be in
    cover, ``maturity_mth() <= 0``, so that a point issued past it is refused by this rule
    whenever it is to be issued; one at or past the end of the projection at the
    valuation date; one whose planned withdrawal is above 0 and below the withdrawal fee,
    ``wd_fee``, which the fee would exceed -- the account would be debited the withdrawal,
    less than the fee the insurer books, and the policyholder paid nothing, so that
    ``IUL_US_S``'s own account value roll-forward and margin identity fail on such a
    point; one in force whose segment ladder in ``inforce_segments_sec.csv`` does not
    hold exactly one row for each of its last ``min(seg_term_mth, duration_mth_init())``
    months, slots 1 to that, a segment a month however little it was swept; and one issued
    below ``issue_age_min``, 0, or above ``issue_age_max``, 85, the issue ages
    ``product-spec.md`` admits.  ``IUL_US_S`` projects any age its tables serve, but the
    compiled model's caches are sized from the youngest issue age (``spec_sec.py``), so a
    younger point, whose frame and policy years run longer, would read past them;
    ``Data`` refuses an age below 0 first, so at the shipped value that rule binds only
    once the Reference is raised.  The oldest sizes nothing, and is the contract's.  The
    two issue-age rules come after the four of stage ``E``, so that every message stage
    ``E`` gave a point it still gives.  An in-force extract should carry none of them.
    These are rules of the product, read from this Space's References, where ``Data``
    checks the tables.  The ladder's counts are compared as ``Data`` elements, not held in
    locals, and the file is named as shipped, so that the formula keeps no Python object
    compiled.
    """
    if maturity_mth() <= 0:
        raise ValueError(
            f"point_id {point_id()}: age_at_entry {age_at_entry()} "
            f"is at or past maturity_age, {maturity_age}: "          # noqa: F821
            f"a policy issued there would never be in cover")
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past the end of the projection, policy month "
            f"{maturity_mth()}, attained age {maturity_age}")        # noqa: F821
    if 0 < wd_pp_mth() < wd_fee:                                     # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: wd_pp {wd_pp_mth()} is above 0 and "
            f"below wd_fee, {wd_fee}: a withdrawal pays its fee out of "  # noqa: F821
            f"itself, so it must be at least the fee")
    want = min(seg_term_mth, max(duration_mth_init(), 0))            # noqa: F821
    if (data.inforce_segment_count()[idx] != want                    # noqa: F821
            or data.inforce_segment_last()[idx] != want):            # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: inforce_segments_sec.csv "
            f"holds {data.inforce_segment_count()[idx]} segments, its last in slot "
            f"{data.inforce_segment_last()[idx]}, where a policy in force "  # noqa: F821
            f"{max(duration_mth_init(), 0)} months holds one a month for its last "
            f"{want}, slots 1 to {want}")
    if age_at_entry() < issue_age_min:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is below "
                         f"issue_age_min, {issue_age_min}")          # noqa: F821
    if age_at_entry() > issue_age_max:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is above "
                         f"issue_age_max, {issue_age_max}")          # noqa: F821
    return n


def t_entry():
    """The first month the policy is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later.  It is the base of every recursion: the count, the account value,
    the fixed account, the collateral, the loan, each live segment and its running totals,
    the face, the two premium accumulators and the MEC latch all open there, from the
    model point's opening state and its segment ladder on a point in force and from the
    issue values on any other.  No cell reads a month before it: a segment created
    before the valuation date is read from the ladder, never from a month before
    ``t = 0``.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and inside the projection.

    ``0 <= duration_mth(t) < maturity_mth()``, false before issue and from
    ``t = proj_len()`` on.  Outside cover every count, balance, segment, charge, premium,
    withdrawal, loan draw, credit, decrement rate, decrement, claim and flow is zero and
    every flag false, :func:`seg_count` the int 0, and no table is read at a policy year
    or an attained age the policy does not have; the clocks and the inputs read on the
    valuation clock and the level policy fee, :func:`expense_pol_mth_at`, keep their
    values, and the two lapse multipliers their neutral 1.0.
    The two exceptions are the opening values of the month after the frame, the count and
    the account value carried into ``t = proj_len()``, which the roll-forwards read (see
    :func:`pols_if_at` and :func:`av_pp_at`).
    """
    return 0 <= duration_mth(t) < maturity_mth()


def is_guaranteed_basis():
    """Whether the run uses class (a) contractual guarantees only.

    ``basis`` is ``CURRENT`` in the base run, so the current non-guaranteed scales
    apply.  Setting it to ``GUARANTEED`` switches the fixed-account rate to 1.00%,
    the cap to 2.00%, the premium load to 8%, the policy fee to $15, the per-unit
    charge to $0.40 in all years and the COI scale to its guaranteed maximum -- the
    notes' "guaranteed-basis projections use only this class".  Key sensitivity 1 in
    the notes is exactly how far apart the two runs are.  ``basis`` holds a code, as
    ``IUL_US_S``'s holds the text it is named for (the Space docstring's *Codes*), and any
    other value is refused, ``"invalid basis"``, as there.
    """
    if basis == CURRENT:                                             # noqa: F821
        return False
    elif basis == GUARANTEED:                                        # noqa: F821
        return True
    else:
        raise ValueError("invalid basis")


def load_prem_rate():
    """l_prem: the premium load rate, 5% current **[std]** / 8% guaranteed **[std]** (F12).

    The current rate sits in the model point table because the load is itself a
    non-guaranteed element re-declarable under ASOP 2 [REG-R26]: ``Data.load_prem_rate``
    at the point.
    """
    if is_guaranteed_basis():
        return load_prem_rate_guar                                   # noqa: F821
    return float(data.load_prem_rate()[idx])                         # noqa: F821


def fixed_rate_ann(t):
    """i_fix: the fixed (holding) account annual effective rate.

    4.50% current [S2], 1.00% guaranteed [S2].  A non-guaranteed element; the base
    deterministic run holds the snapshot level, as the notes prescribe.  An economic
    input, read at month ``t`` on the **valuation** clock, the same month for every point,
    as a re-declared rate would apply; level as shipped, so it holds its value outside
    cover.
    """
    if is_guaranteed_basis():
        return guar_rate_ann                                         # noqa: F821
    return fixed_rate_curr                                           # noqa: F821


def inv_return_mth(t):
    """The monthly fixed-account rate, ``(1 + i_fix)^(1/12) - 1`` **[std]** conversion.

    0.0036748 at the 4.50% current rate [S2].  The name follows ``CashValue_SE``; only
    the fixed account and the loan collateral account earn it -- segments earn no
    interim interest at all, which is what the 0% floor design buys [S2].
    """
    return (1 + fixed_rate_ann(t)) ** (1 / 12) - 1


def guar_rate_mth():
    """i_gm: the monthly guaranteed rate, ``(1 + i_g)^(1/12) - 1`` at i_g = 1.00% [S2]."""
    return (1 + guar_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def naar_factor():
    """``1 + i_gm``; ``v_g = 1 / naar_factor()`` is the notes' one-month discount.

    The death benefit is discounted one month at the **guaranteed** rate, never the
    credited or index rate -- the universal life base convention, carried over
    unchanged.  1.0008295 at the 1.00% guarantee [S2].
    """
    return 1 + guar_rate_mth()


def loan_rate_mth():
    """The monthly charged loan rate, ``(1 + i_L^c)^(1/12) - 1``, at 3.00% **[std]** (F18).

    A Reference of the run, level in every month.
    """
    return (1 + loan_rate_ann) ** (1 / 12) - 1                       # noqa: F821


def loan_credit_rate_ann(t):
    """i_L^e: the rate credited on loan collateral, 2.00% years 1-10, 3.00% after **[std]**.

    The standardization keeps the universal carrier pattern of a ~1% net loan spread
    early grading to a 0% "wash" from year 11 [S3][S5][S7] (F18).  A term of the
    contract, so it steps on the **policy** year.  Zero outside cover, before the policy
    year is compared: before issue the valuation clock reaches policy years the policy
    does not have.
    """
    if not is_active(t):
        return 0.0
    if policy_year(t) <= loan_credit_step_year:                      # noqa: F821
        return loan_credit_rate_ann_1                                # noqa: F821
    return loan_credit_rate_ann_2                                    # noqa: F821


def loan_credit_rate_mth(t):
    """The monthly loan collateral credited rate, ``(1 + i_L^e)^(1/12) - 1``."""
    return (1 + loan_credit_rate_ann(t)) ** (1 / 12) - 1


def index_cap_at(t):
    """c: the cap in force, 10.00% current [S2] / 2.00% guaranteed [S2] (F8).

    The current cap is a **snapshot**: observed 10.00%-13.75% across carriers and print
    dates [S2][S3][S4][S5][S7], and re-declared at every segment start [S3][S4].  The
    base run holds it level; a cap re-declaration module driven by an option budget is
    described in the notes but not implemented, because the notes supply neither an
    option pricing model nor a net investment earnings rate path.

    Read at month ``t`` on the **valuation** clock, the cap declared then: a segment
    created in month ``t`` is capped at ``index_cap_at(t)`` at its maturity, twelve months
    on (:func:`seg_index_cap`), and a segment created before the valuation date at the cap
    its ladder row carries, :func:`seg_index_cap_init`.  Level as shipped, so it holds its
    value outside cover.
    """
    if is_guaranteed_basis():
        return index_cap_guar                                        # noqa: F821
    return index_cap_curr                                            # noqa: F821


def index_level(t):
    """I(t): the S&P 500 price-return index level at monthiversary t [S2][S3].

    The base deterministic run grows the index at a level ``index_return_ann`` a year
    along the **valuation** clock: ``index_level_init * (1 + index_return_ann)^(t / 12)``,
    so ``index_level_init`` is the level at the valuation date, one path for every point,
    and every segment matures at the same point-to-point return.  6.40% is the
    carrier-published 1988-2023 lookback for the 10%-cap account [S2].  ``IUL_US_S`` reads
    the path at ``duration_mth(t)``, a path of each point's own from its issue, which is
    the same path on a point issued at the valuation date.  Moving the path moves no
    credit, a ratio of two levels on one path: a segment created before the valuation date
    carries its start level on this path in its ladder row (:func:`seg_index_start`).

    **This cell is the single point of substitution.**  Override it, a formula override,
    which only modelx can make (compiled, edit the formula and rebuild), with a historical
    or simulated path, keyed by the months from the valuation date, and every segment
    created in the frame follows; the ladder's start levels are inputs, which do not follow
    an override, so an extract's ``seg_index_start_init`` must be on the overriding path:
    the notes' stochastic module (real-world lognormal, mu = 6.0%, sigma = 16% **[std]**)
    is a driver around the model, not a formula inside it.  Remember what the notes say
    about the level rate: AG 49-A bounds what may be *illustrated*, not what will be
    *credited* [R1][R6], and because the cap truncates the right tail while the floor only
    offsets the left, a deterministic run at the illustrated rate overstates credits
    against a stochastic mean at matched expected index growth.  A function of the clock
    alone, so it holds its value outside cover.
    """
    return index_level_init * (1 + index_return_ann) ** (t / 12)    # noqa: F821


def index_change(index_start, index_end):
    """r = I(m+12) / I(m) - 1: the point-to-point index change over a segment term.

    Price return, dividends excluded [S2][S3].  Takes the two index levels rather than
    a month so that the worked example's own levels -- 4,500.00 to 5,040.00 in
    scenario A, to 3,825.00 in scenario B -- can be put through the same formula the
    projection uses.  An engine cell of ``IUL_US_S``'s, kept for its worked example and for
    the comparison with it (the Space docstring's *Reporting cells*): no projection cell
    calls it, and :func:`seg_return` computes the same ratio for the segment maturing in
    month ``t``.
    """
    return index_end / index_start - 1


def index_credit_rate(index_return, cap=None):
    """cr_k = max(f, min(c, p x r)): the credited rate for one segment [S2][S3][R1].

    Floor 0%, participation 100%, cap per :func:`index_cap_at` [S2].  ``cap`` defaults to
    the cap in force at ``t = 0``, ``IUL_US_S``'s engine, kept unchanged for its worked
    example -- pass ``index_cap_guar`` for the guaranteed-basis credit; the notes price both
    on the worked example, at 10.00% and 2.00%.  An engine cell, kept for that example and
    for the comparison with ``IUL_US_S``: no projection cell calls it, and
    :func:`seg_credit_rate` computes the same rate, in the same order of bounds, for the
    segment maturing in month ``t``, at the cap declared at its creation.

    This is where the two-sided truncation lives: the cap binds on the way up, the
    floor on the way down, and the historical frequency of a 0% credit for a single
    index allocation was 12.55%-23.81% in a carrier's 2005-2017 issue-date study [S8].
    """
    c = index_cap_at(0) if cap is None else cap
    return max(index_floor, min(c, index_par * index_return))        # noqa: F821


def seg_credit_base(seg_bal_init, seg_deductions, conv=None):
    """The segment balance the index credit is applied to.

    ``REMAINING`` **[std]**, the baseline
        ``seg_bal_init - seg_deductions``: the actual balance left at maturity, so
        amounts withdrawn, borrowed or deducted mid-segment earn no index credit
        (withdrawal and loan forfeiture [S3]; extension to deductions **[std]**).

    ``ADJ_BEGIN``, the documented variation
        ``seg_bal_init - seg_deductions / 2``: one carrier's contractual adjusted
        beginning value, which subtracts withdrawals and loan transfers in full but
        **one half** of the monthly deductions taken during the segment [S3].  Pass
        ``seg_bal_init`` already net of withdrawals and loan transfers, as
        :func:`index_credit_pp` takes it.

    The notes list picking one and keeping the death benefit, cash value and credit
    formulas consistent with it among the modeling pitfalls; ``seg_credit_base_conv``
    is the Reference that records the choice, a code (the Space docstring's *Codes*),
    which ``conv`` defaults to.  An engine cell, kept for ``IUL_US_S``'s worked example and
    for the comparison with it: no projection cell calls it, and :func:`index_credit_pp`
    computes the same base inline, refusing a convention neither code names with the
    same ``"invalid credit base"``.
    """
    k = seg_credit_base_conv if conv is None else conv               # noqa: F821
    if k == REMAINING:                                               # noqa: F821
        return seg_bal_init - seg_deductions
    elif k == ADJ_BEGIN:                                             # noqa: F821
        return seg_bal_init - seg_deductions / 2
    else:
        raise ValueError("invalid credit base")


def index_credit(seg_bal_init, seg_deductions, index_return, conv=None, cap=None):
    """Credit_k = cr_k x credit base: the index credit paid at a segment's maturity.

    The engine form, taking the segment's opening balance (net of any withdrawals and loan
    transfers), the deductions charged to it over its term, and its point-to-point index
    change: :func:`index_credit_rate` times :func:`seg_credit_base`.  An engine cell, kept
    for ``IUL_US_S``'s worked example, which prices one segment's credit at both caps
    through it, and for the comparison with ``IUL_US_S``, whose projection calls it: no
    projection cell here calls it, and :func:`index_credit_pp` computes the same product,
    the rate first, then the base.
    """
    return (index_credit_rate(index_return, cap)
            * seg_credit_base(seg_bal_init, seg_deductions, conv))


def seg_matured_value(seg_bal_init, seg_deductions, index_return, conv=None, cap=None):
    """The matured segment value: remaining balance plus the index credit.

    ``S_{k,m+12} x (1 + cr_k)`` under the baseline credit base, which is the value that
    rolls into the fixed account and is swept back into a new segment under the
    standing allocation instruction **[std]** (spec F11).  An engine cell, kept for
    ``IUL_US_S``'s worked example, which alone calls it; :func:`seg_roll_pp` is the
    projection's matured value.
    """
    return (seg_bal_init - seg_deductions
            + index_credit(seg_bal_init, seg_deductions, index_return, conv, cap))


def prem_persistency(t):
    """The fraction of the planned premium actually paid in policy year y **[std]**.

    ``0.98^(y - 1)``: the notes give premium persistency in closed form rather than as
    a table, compounding at 98% a year.  Premium persistency is *the* behavior
    dimension unique to flexible-premium products; the 2015-2021 LIMRA/SOA UL study is
    the recommended public calibration base [REG-R21] and the level here is a
    placeholder.  A rule of the contract's years, so it steps on the **policy** year:
    a policy in force pays the persistency of its own year, not of the valuation date's.

    The funding-stop state the notes pair with this factor -- probability 1% a year,
    after which the policy runs charge-only -- is a **second account value path** the
    notes do not say how to blend with the first, and is not implemented.  Zero outside
    cover, before the policy year is read.
    """
    if not is_active(t):
        return 0.0
    return prem_persistency_rate ** (policy_year(t) - 1)             # noqa: F821


def premium_pp(t):
    """P_t: the gross premium per policy received at BOM of month t.

    Annual mode **[std]**: the whole planned premium falls at BOM of the first month
    of each policy year, ``duration_mth(t) % 12 == 0``, and every other month is zero.
    Monthly mode: a twelfth of the planned annual premium falls at BOM of every month,
    ``premium_pp_ann / 12`` times :func:`prem_persistency`, as on points 4, 7 and 12.

    ``LEVEL``
        The planned premium times :func:`prem_persistency`, in either mode.

    ``SINGLE``
        One premium in the issue month, capped at the guideline single premium.

    ``TARGET``
        As ``LEVEL`` but capped so cumulative premium stays inside the guideline
        premium limit **[std]**; the cap looks at the accumulator's opening value --
        ``cum_prem_pp(t - 1)``, or, in the first month on the books, :func:`t_entry`,
        :func:`cum_prem_init`, the premiums less withdrawals paid before the valuation
        date, 0 at issue -- so there is no circularity, and a TARGET point in force near
        its limit collects only what the limit still has room for.

    Zero from attained age ``charges_cease_age``, 121 as shipped, when charges cease and
    premiums are no longer accepted (spec F5), and zero outside cover.  The pattern and
    the mode are read through their decodes, :func:`is_single_premium`,
    :func:`is_level_premium`, :func:`is_target_premium`, :func:`is_annual_premium` and
    :func:`is_monthly_premium`, not as text; a value none of them knows raises, as
    ``IUL_US_S``'s does.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    if is_single_premium():
        return min(premium_pp_ann(), gsp()) if duration_mth(t) == 0 else 0.0
    if is_annual_premium():
        if duration_mth(t) % 12 != 0:
            return 0.0
        gross = premium_pp_ann() * prem_persistency(t)
    elif is_monthly_premium():
        gross = premium_pp_ann() / 12 * prem_persistency(t)
    else:
        raise ValueError("invalid premium mode")
    if is_level_premium():
        return gross
    elif is_target_premium():
        paid = cum_prem_pp(t - 1) if t > t_entry() else cum_prem_init()
        return min(gross, max(0.0, gpt_limit(t) - paid))
    else:
        raise ValueError("invalid premium type")


def prem_to_av_pp(t):
    """NP_t = P_t (1 - l_prem): the net premium, credited to the fixed account.

    The fixed account doubles as the interim / holding account: net premium sits there
    at the declared fixed rate until the next monthiversary sweep moves it into a
    segment [S1] **[std]** (spec F10).
    """
    return premium_pp(t) * (1 - load_prem_rate())


def prem_to_av(t):
    """Net premium credited to account values, for the policies in force."""
    return prem_to_av_pp(t) * pols_if(t)


def premiums(t):
    """Premium income at BOM of month t, weighted by the in force at BOM."""
    return premium_pp(t) * pols_if(t)


def wd_pp(t):
    """W_t: the partial withdrawal per policy at BOM of month t, **gross of the fee**.

    A constant monthly amount from :func:`wd_first_year`, :func:`wd_pp_mth`, the model
    point's ``wd_pp`` column, and **0 in the baseline** **[std]**: the notes give no
    withdrawal utilization pattern, so the mechanics are implemented and the behaviour is
    left to the data.  Model point 5 switches it on.

    The account is debited ``W_t``; the policyholder receives ``W_t - 25`` and the
    insurer keeps the $25 fee [S3].  This differs from the universal life chassis,
    where the fee is charged on top of the withdrawal -- these notes write the
    withdrawal outflow as ``W_t - $25 fee``, so the fee is inside ``W_t`` here.  Zero from
    attained age ``charges_cease_age``, and zero outside cover, before the policy year
    is compared: before issue the valuation clock reaches policy years the policy does not
    have.
    """
    if not is_active(t) or policy_year(t) < wd_first_year():
        return 0.0
    if age(t) >= charges_cease_age:                                  # noqa: F821
        return 0.0
    return wd_pp_mth()


def wd_fee_pp(t):
    """The $25 withdrawal fee, charged only in a month with a withdrawal [S3].

    Retained by the insurer, so it is part of :func:`margin_expense`, not of
    :func:`claims`.  It is not an extra debit to the account value: it comes out of
    ``W_t``.
    """
    return wd_fee if wd_pp(t) > 0 else 0.0                           # noqa: F821


def loan_new_pp(t):
    """B_t: a new standard loan taken at BOM of month t **[std]**.

    The notes' distribution-scenario module borrows a level amount annually from a start
    age **[std]**; here that is :func:`loan_new_pp_ann`, the model point's
    ``loan_new_pp_ann``, at each policy anniversary from the first month of policy year
    :func:`loan_first_year`.  **Zero in the baseline** -- the notes set loan utilization
    to none -- and switched on by model point 5.

    Participating (indexed) loans are a documented variation, not modeled: the baseline
    uses standard loans only **[std]** (F18), which decouples loan modeling from index
    scenarios.  Zero outside cover, before the policy year is compared.
    """
    if not is_active(t) or policy_year(t) < loan_first_year():
        return 0.0
    if duration_mth(t) % 12 != 0:
        return 0.0
    return loan_new_pp_ann()


def face_reduction_pp(t):
    """The face reduction a withdrawal forces under Option A, dollar for dollar **[std]**.

    Standard universal life practice, stated in the product spec but not explicit in
    the retrieved brochures.  Under Option B the withdrawal reduces the account value
    only and this is zero.  Never more than the face entering the month, which is the
    previous month's :func:`sum_assured_at`, or, in the first month on the books,
    :func:`t_entry`, the face in force at the valuation date, :func:`sum_assured_init`, on
    a point in force, and the face at issue, :func:`sum_assured`, on any other.  The
    option is read through its decode, :func:`is_db_option_a`.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if not is_db_option_a() or wd_pp(t) <= 0:
        return 0.0
    if t > t_entry():
        opening = sum_assured_at(t - 1)
    elif duration_mth_init() > 0:
        opening = sum_assured_init()
    else:
        opening = sum_assured()
    return min(wd_pp(t), opening)


def sum_assured_at(t):
    """F(t+1): the face amount at the end of month t, after any withdrawal-driven cuts.

    A closing balance: the opening face of month ``t`` is the previous month's, and in the
    first month on the books, :func:`t_entry`, the face in force at the valuation date,
    :func:`sum_assured_init`, on a point in force, and the face at issue,
    :func:`sum_assured`, on any other, less this month's Option A reduction.  Face
    increases, elective decreases and option changes are not modeled, so the withdrawal
    reduction is the only movement; it never takes more than the opening face, so the
    face reaches 0 at the least and stays there.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        opening = sum_assured_at(t - 1)
    elif duration_mth_init() > 0:
        opening = sum_assured_init()
    else:
        opening = sum_assured()
    return max(0.0, opening - face_reduction_pp(t))


def units(t):
    """The face amount in $1,000 units, ``sum_assured_at(t) / 1000``.

    The per-unit charge is quoted per $1,000 of face per month, so it multiplies this.
    The surrender charge is quoted per $1,000 of **initial** face, because face
    decreases do not reduce it [S3]; see :func:`surr_charge_pp`.
    """
    return sum_assured_at(t) / 1000


def corridor_factor(t):
    """kappa_x: the IRC 7702(d) corridor factor at the attained age [R4].

    250% at ages 0-40 grading to 100% at 90-95, read at the attained age of month t by
    :func:`corridor_factor_at`.  Only the Guideline Premium Test is modeled (spec F4), so
    any other ``qual_test`` raises rather than being treated as GPT, in whatever month,
    since it is a fault of the point; the test is read through its decode, :func:`is_gpt`.

    High funding drives the corridor rather than the face amount, which raises the
    death benefit, the net amount at risk and hence the cost of insurance: the notes
    list omitting this among the pitfalls, because it overstates late-duration account
    values and understates charges.  Zero outside cover, before the table is read.
    """
    if not is_gpt():
        raise ValueError("invalid qual_test")
    return corridor_factor_at(age(t)) if is_active(t) else 0.0


def corridor_factor_at(a):
    """kappa at attained age a, from *corridor_factors.csv*: the table's one reader.

    ``Data.corridor_factor_array()`` at the age, the table padded from age 0, so that the
    age is the index.  Ages outside the table take its nearest row: the first and last
    ages ``data.corridor_age_first()`` and ``data.corridor_age_last()`` give, which they
    read from the table's key column once the keys and the factors are checked, before any
    factor is read.  So the padding is never read, and no age below 0 is either: ``Data``
    refuses a table whose first age is negative.  The last is asked for first, since it
    runs the checks and the first is counted back from it.  Keyed by the attained age, so
    the table is read once an age rather than once a month; :func:`corridor_factor` calls
    it inside cover only.
    """
    last = data.corridor_age_last()                                  # noqa: F821
    a = min(max(a, data.corridor_age_first()), last)                 # noqa: F821
    return float(data.corridor_factor_array()[a])                    # noqa: F821


def db_pp(t):
    """DB_t: the death benefit per policy after the corridor test [S3][R4].

    ``max(option_db, kappa_x x AV'_t)`` where ``option_db`` is the face amount under
    Option A and face plus account value under Option B, and ``AV'_t`` is the account
    value after premium, the maturity credit and any withdrawal, and **before** the
    monthly deduction.  Measuring the account value at that point is what removes the
    circularity: under Option B the death benefit depends on the account value and the
    net amount at risk on the death benefit, but with this ordering neither depends on
    the deduction.

    During a segment the death benefit reflects the segment balance **without**
    unrealized index credit [S3]: with a 0% floor design segments simply carry no
    interim interest, so nothing extra is needed here.  ``IUL_US_S``'s formula, with no
    floor on the account value: an exhausted account's ``AV'_t`` below zero leaves the
    corridor's amount at 0 or below, and the face wins, which ``Data`` keeps so by
    refusing a corridor factor below 0.  The option is read through its decodes,
    :func:`is_db_option_a` and :func:`is_db_option_b`, not as text.  Zero outside cover,
    before the corridor table is read.
    """
    if not is_active(t):
        return 0.0
    av = av_pp_at(t, BEF_FEE)                                        # noqa: F821
    if is_db_option_a():
        opt = sum_assured_at(t)
    elif is_db_option_b():
        opt = sum_assured_at(t) + av
    else:
        raise ValueError("invalid db_option")
    return max(opt, corridor_factor(t) * av)


def net_amt_at_risk(t):
    """NAAR_t = max(0, DB_t x v_g - AV'_t), the universal life base convention.

    The death benefit is discounted one month at the **guaranteed** rate
    (:func:`naar_factor`) and the account value is measured **before** the monthly
    deduction.  Using the credited or index rate in the discount, or the
    post-deduction account value, makes the cost of insurance implicit and requires
    iteration, and produces small systematic errors.
    """
    return max(0.0, db_pp(t) / naar_factor() - av_pp_at(t, BEF_FEE)) # noqa: F821


def coi_rate_guar(t):
    """The guaranteed maximum monthly COI rate per $1,000 of net amount at risk.

    The notes set the guaranteed basis at 2017 CSO ANB smoker-distinct ultimate
    **[std]**/[REG-R17].  That table is licensed and is not reproduced here: the
    shipped scale is illustrative **[std]**, of realistic magnitude and shape, and is
    swapped by replacing *coi_rates.csv*.  Read at the policy year of month t by
    :func:`coi_rate_guar_py`, where policy years beyond the table take its last row; zero
    outside cover, before the scale is read.
    """
    return coi_rate_guar_py(policy_year(t)) if is_active(t) else 0.0


def coi_schedule():
    """The number of this point's guaranteed COI scale, its row of the COI array.

    ``Data.coi_schedule`` at the point: the schedules of *coi_rates.csv*, one for each
    ``sex``, ``rate_class`` and ``age_at_entry`` it holds, numbered from 1 in the order
    of those keys, and 0 where the table has no scale for the point's own, which
    :func:`coi_rate_last_year` refuses where a rate is read.  It stands for
    ``IUL_US_S``'s ``coi_rate_scale``, a Series sliced from the table, which no compiled
    cell can hold: :func:`coi_rate_guar_py` reads the scale at this row and the year.
    """
    return int(data.coi_schedule()[idx])                             # noqa: F821


def coi_rate_guar_py(y):
    """The guaranteed maximum monthly COI rate in policy year y, from the point's scale.

    ``Data.coi_rate_array()`` at the point's :func:`coi_schedule` and the year, each
    schedule padded from year 0, so that the year is the column.  Policy years beyond the
    scale take its last row, :func:`coi_rate_last_year`, which is asked for first, so that a
    projection meets the check of the table's keys, and the refusal of a point whose cell
    the table lacks, before any rate is read.  A year below 1, where ``IUL_US_S``'s slice
    raised ``KeyError``, is refused, naming the point and the year, so that the padding is
    never read.  The scale's one reader, keyed by the contractual policy year;
    :func:`coi_rate_guar` calls it inside cover only.
    """
    last = coi_rate_last_year()
    if y < 1:
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no rate for policy "
                         f"year {y}")
    return float(data.coi_rate_array()[coi_schedule(), min(y, last)])  # noqa: F821


def coi_rate_last_year():
    """The last policy year of this point's guaranteed COI scale: its extent.

    ``Data.coi_rate_last_years`` at this point's :func:`coi_schedule`, the last year of
    its scale, which ``Data`` reads from the table's key columns once it has checked the
    keys and the rates.  76 on the shipped anchor cell, whose scale runs to attained age
    120.  A point the table has no scale for, schedule 0, has a last year of 0, and is
    refused here, naming it and its issue age, where ``IUL_US_S`` raises pandas'
    ``KeyError``: when its first COI rate is read, and not before, since a point valued at
    or past ``charges_cease_age`` never reads one, and ``IUL_US_S`` projects it.  Stage
    ``E``'s message quoted the point's ``sex`` and ``rate_class`` too, which a projection
    formula cannot read here: each is a label, a reporting cell's.  The element is compared,
    and ``int`` of it returned, rather than held in a local first, which a formula that also
    builds a message would keep a Python object compiled.
    """
    if data.coi_rate_last_years()[coi_schedule()] < 1:               # noqa: F821
        raise ValueError(f"point_id {point_id()}: coi_rates.csv has no rates for its sex, "
                         f"rate_class and age_at_entry {age_at_entry()}")
    return int(data.coi_rate_last_years()[coi_schedule()])           # noqa: F821


def coi_rate(t):
    """coi_t: the monthly COI rate in force, per $1,000 of net amount at risk.

    ``coi_curr_factor`` (65% **[std]**) times the guaranteed maximum on the current
    basis; the guaranteed maximum itself on the guaranteed basis.  Carrier COI tables
    are not public [S3] and re-rating is governed by ASOP 2 [REG-R26], so the ratio is
    a pure modeling assumption and one of the notes' dominant sensitivities.

    Note the units: per $1,000 of net amount at risk per **month**, so it is divided by
    1,000 in :func:`coi_pp`.  It is not comparable with ``CashValue_SE.coi_rate``,
    which is a rate per unit of account value.
    """
    if is_guaranteed_basis():
        return coi_rate_guar(t)
    return coi_curr_factor * coi_rate_guar(t)                        # noqa: F821


def coi_pp(t):
    """COI_t = coi_t x NAAR_t / 1000: the cost of insurance charge per policy.

    Zero from attained age ``charges_cease_age``, when charges cease, and zero outside
    cover, before the scale is read.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return coi_rate(t) / 1000 * net_amt_at_risk(t)


def coi(t):
    """Cost of insurance charges deducted from account values, for the policies in force."""
    return coi_pp(t) * pols_if(t)


def rider_charge_pp(t):
    """Rider charges, 0 in the baseline **[std]**.

    The notes carry this term in the monthly deduction so rider modules can be added
    without changing the recursion; every rider in the product spec is out of the
    baseline.
    """
    return 0.0


def expense_pol_mth_at(t):
    """e_pol: the monthly policy fee, $10 current [S3][S5] / $15 guaranteed **[std]**.

    The notes' F13.  Level in every month, an input that holds its value outside cover,
    as the fixed-account rate and the cap do; :func:`maint_fee_pp`, its one reader, is
    zero there.
    """
    if is_guaranteed_basis():
        return expense_pol_mth_guar                                  # noqa: F821
    return expense_pol_mth                                           # noqa: F821


def expense_unit_mth_at(t):
    """e_unit: the per-unit charge per $1,000 of face per month (F14).

    $0.30 in policy years 1-10 and nothing thereafter on the current basis; $0.40 in
    **all** years on the guaranteed basis.  The structure -- charged for the first ten
    years currently, guaranteed for all years -- is sourced [S3][S5]; the dollar scales
    live in policy data pages and are not public, so the levels are **[std]**.  A term
    of the contract, so it steps on the **policy** year.  Zero outside cover, before the
    policy year is compared.
    """
    if not is_active(t):
        return 0.0
    if is_guaranteed_basis():
        return expense_unit_mth_guar                                 # noqa: F821
    if policy_year(t) <= expense_unit_step_year:                     # noqa: F821
        return expense_unit_mth_1                                    # noqa: F821
    return expense_unit_mth_2                                        # noqa: F821


def maint_fee_pp(t):
    """The non-COI part of the monthly deduction per policy.

    ``e_pol + e_unit x F/1000 + rider charges``.  The name follows
    ``CashValue_SE.maint_fee``: this is a *charge* against the account value and
    therefore insurer income.  It is not :func:`expenses`, which is the insurer's own
    outgo.  Zero from attained age ``charges_cease_age``, when charges cease, and zero
    outside cover.  The policy fee, :func:`expense_pol_mth_at`, is level, an input that
    holds its value in every month; the guard here keeps it off the months outside cover.
    """
    if not is_active(t) or age(t) >= charges_cease_age:              # noqa: F821
        return 0.0
    return (expense_pol_mth_at(t) + expense_unit_mth_at(t) * units(t)
            + rider_charge_pp(t))


def maint_fee(t):
    """Non-COI monthly charges deducted from account values, for the policies in force."""
    return maint_fee_pp(t) * pols_if(t)


def mth_deduction_pp(t):
    """MD_t = e_pol + e_unit x F/1000 x 1{yr<=10} + coi_t x NAAR_t / 1000.

    :func:`maint_fee_pp` plus :func:`coi_pp`, taken at BOM.  The deduction at the start
    of month t pays for month t's coverage.
    """
    return maint_fee_pp(t) + coi_pp(t)


def mth_deduction(t):
    """Monthly deductions taken from account values, for the policies in force."""
    return mth_deduction_pp(t) * pols_if(t)


def draw_pp(t):
    """The total amount leaving the fixed account and segments at step 3 of month t.

    The withdrawal (gross of its fee) plus the collateral for any new standard loan.
    The loan collateral does not leave the *account value* -- it moves into
    :func:`lca_pp` -- but it does leave the fixed account and the segments, and it is
    sourced by the same rule: fixed account first, then pro rata across live segments,
    the order one carrier gives for loans [S3].  Applied to the withdrawal the rule is
    **[std]**: that carrier takes withdrawals pro rata across all unloaned accounts [S3].
    """
    return wd_pp(t) + loan_new_pp(t)


def draw_from_seg_pp(t):
    """The part of the step-3 draw sourced pro rata from live segments.

    Only what the fixed account cannot cover, and never more than the live segments
    hold (see :func:`draw_pp`).  Being step 3 it has the **first** claim on the pool; the
    step-6 deduction is capped against what is left after it
    (:func:`mth_deduction_from_seg_pp`).  Amounts leaving a segment mid-term earn no
    index credit [S3], which under the baseline credit base happens automatically.
    """
    short = draw_pp(t) - max(0.0, fa_pp_at(t, BEF_WD))               # noqa: F821
    if short <= 0:
        return 0.0
    return min(short, max(0.0, seg_bal_active_pp(t)))


def draw_from_fa_pp(t):
    """The part of the step-3 draw sourced from the fixed account, taken first.

    Defined as the residual of :func:`draw_pp` so that the two sources always sum to it
    exactly; if neither the fixed account nor the segments can cover it, the fixed
    account carries the excess and goes negative rather than the draw being silently
    truncated.
    """
    return draw_pp(t) - draw_from_seg_pp(t)


def mth_deduction_from_seg_pp(t):
    """The part of the monthly deduction sourced pro rata from live segments **[std]**.

    The notes' sourcing convention: fixed account first, shortfall pro rata across
    active segments.  Never more than the segments still hold **after** the step-3
    draw, which is why the cap is ``seg_bal_active_pp(t) - draw_from_seg_pp(t)`` and
    not the pool :func:`draw_from_seg_pp` was itself capped against: the withdrawal
    and the new loan collateral come out of the same segments earlier in the same
    month, so capping both against the pre-draw pool would let the two together take
    more than the segments hold.  That drives a segment balance negative and, twelve
    months later, pays a **negative** index credit on it -- a breach of the 0% floor
    of ``cr_k = max(f, min(c, p x r))`` [S2][R1].  :func:`check_seg_ladder` asserts
    both consequences away.

    Whatever the segments cannot cover stays with :func:`mth_deduction_from_fa_pp`,
    so the fixed account carries the excess and goes negative rather than the
    deduction being silently truncated -- the notes charge ``MD_t`` in full and hand
    an uncovered deduction to the grace/lapse cascade, which is not implemented.

    Carrier practice differs -- one carrier instead half-weights in-segment
    deductions in its credit base [S3] -- and the notes list picking one and keeping
    the formulas consistent among the modeling pitfalls; see :func:`seg_credit_base`.
    """
    short = mth_deduction_pp(t) - max(0.0, fa_pp_at(t, BEF_FEE))     # noqa: F821
    if short <= 0:
        return 0.0
    return min(short, max(0.0, seg_bal_active_pp(t) - draw_from_seg_pp(t)))


def mth_deduction_from_fa_pp(t):
    """The part of the monthly deduction sourced from the fixed account, taken first.

    The residual, so the two sources always sum to :func:`mth_deduction_pp`.
    """
    return mth_deduction_pp(t) - mth_deduction_from_seg_pp(t)


def seg_bal_active_pp(t):
    """The live segment balances available to a draw at BOM of month t.

    The segments born in policy months ``duration_mth(t) - 11`` to
    ``duration_mth(t) - 1``, valued at the end of month ``t - 1``, where each sat in slot
    ``duration_mth(t) - 1 - m``.  The segment born at ``duration_mth(t) - 12`` is **not**
    in the pool: it matured at step 2 of this month and its value is already in the fixed
    account.  The segment born this month does not exist yet -- it is created by the sweep
    at step 7.  No segment is born before issue, so the pool is empty in the issue month.
    In the first month on the books, :func:`t_entry`, a segment born before the valuation
    date is valued from the segment ladder, :func:`seg_bal_pp_init`, its balance entering
    month 0.

    The balances are summed in ``IUL_US_S``'s order, by creation month, in an explicit loop
    that compensates as Python's ``sum()`` of floats does from Python 3.12, Neumaier's
    improvement of Kahan's summation, the compensation added at the end where it is a finite
    number other than zero, ``abs(c) <= 1.7976931348623157e308``, the largest double: so the
    pool is ``IUL_US_S``'s ``sum()`` bit for bit there, a segment closing on a rounding
    about zero included, which :func:`seg_share` reads by its test of zero.  Compiled, the
    loop is C on doubles, added in the order written, since nothing in the build lets the
    compiler reassociate (no ``-ffast-math``), and with no multiply and add fused into one
    rounding, which the build forbids (``-ffp-contract=off``).  Python 3.11's ``sum()`` is
    a plain fold, which can put such a pool on the other side of zero.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    s = 0.0
    c = 0.0
    for m in range(max(0, d - seg_term_mth + 1), d):                 # noqa: F821
        if t > t_entry():
            x = seg_bal_pp(t - 1, d - 1 - m)
        else:
            x = seg_bal_pp_init(duration_mth_init() - m)
        u = s + x
        if abs(s) >= abs(x):
            c = c + ((s - u) + x)
        else:
            c = c + ((x - u) + s)
        s = u
    if c != 0.0 and abs(c) <= 1.7976931348623157e308:
        s = s + c
    return s


def seg_share(t, k):
    """The pro-rata share of a draw at BOM of month t of the segment in slot k.

    Its opening balance over the live pool, :func:`seg_bal_active_pp`, and 0 where the pool
    is not above zero, ``IUL_US_S``'s own test, which a pool closing on a rounding about
    zero meets either way.  Because a pro-rata draw leaves the proportions unchanged, the
    same shares serve the step-3 draw and the step-6 deduction even though they are taken at
    different points in the month.  ``k`` is the segment's slot in month ``t``, its months
    since creation, ``duration_mth(t) - m`` for the segment born in policy month ``m``.  The
    opening balance is the segment's at the end of month ``t - 1``, where it sat in slot
    ``k - 1``, or, in the first month on the books, :func:`t_entry`, the ladder's
    :func:`seg_bal_pp_init` at slot ``k``, read only for a slot the ladder holds, ``1`` to
    ``min(seg_term_mth, duration_mth_init())``; any other slot, slot 0, the segment born in
    the month itself, or one older than the ladder, has a share of 0, as ``IUL_US_S``'s read
    of a balance outside its segment's life gives.  Slot 0 asks for no balance, so no cell
    reads a slot below 0.
    """
    pool = seg_bal_active_pp(t)
    if pool <= 0:
        return 0.0
    if k < 1:
        return 0.0
    if t > t_entry():
        prev = seg_bal_pp(t - 1, k - 1)
    elif k <= min(seg_term_mth, duration_mth_init()):                # noqa: F821
        prev = seg_bal_pp_init(k)
    else:
        prev = 0.0
    return prev / pool


def seg_wd_pp(t, k):
    """The draw of month t out of the segment in slot k: its share of the step-3 draw."""
    return draw_from_seg_pp(t) * seg_share(t, k)


def seg_ded_pp(t, k):
    """The deduction of month t out of the segment in slot k: its share of the monthly
    deduction.
    """
    return mth_deduction_from_seg_pp(t) * seg_share(t, k)


def sweep_pp(t):
    """Sweep_t = w_ix x FA balance after steps 1-6 **[std]** (spec F10).

    The monthiversary sweep, which creates this month's segment.  Carrier practice
    varies -- one carrier sweeps on the 15th [S1], another on the first day of a
    policy month [S3] -- and the baseline standardizes on the monthiversary so segment
    dates align with monthly processing.  A third carrier's charge-holdback in the
    fixed strategy [S5] is a documented variation and is not modeled.  Nothing is swept
    from a fixed account below zero.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return index_alloc_rate() * max(0.0, fa_pp_at(t, BEF_SWEEP))     # noqa: F821


def seg_new_pp(m):
    """S_{k,m_k}: the balance of the segment born in policy month m, at its creation.

    ``m`` is a **policy** month, ``duration_mth`` of the month of the sweep that created the
    segment.  Born in the frame, at or after the valuation date, the segment is that month's
    sweep, :func:`sweep_pp` at month ``m - duration_mth_init()``, as in ``IUL_US_S``.  Born
    before the valuation date, it is in ladder slot ``k = duration_mth_init() - m``, and its
    creation balance is what the ladder gives it since, its balance entering month 0 plus
    the deductions and the draws charged to it: nothing may enter or leave a segment but a
    deduction, a withdrawal or a loan transfer, which is the closure
    :func:`check_seg_ladder` asserts.  Zero for a month before issue and for a segment
    matured before the valuation date, which nothing reads.  Keyed by the creation month, as
    in ``IUL_US_S``, where the six cells of a segment in a month are keyed by its slot: one
    value a segment, which :func:`seg_bal_pp` reads in slot 0 and :func:`index_credit_pp` at
    maturity.
    """
    d0 = duration_mth_init()
    if m < 0:
        return 0.0
    if m >= d0:
        return sweep_pp(m - d0)
    k = d0 - m
    if k > seg_term_mth:                                             # noqa: F821
        return 0.0
    return seg_bal_pp_init(k) + seg_ded_cum_pp_init(k) + seg_wd_cum_pp_init(k)


def seg_bal_pp(t, k):
    """S_{k,t+1}: the balance at the end of month t of the segment in slot k.

    ``S_{k,t+1} = S_{k,t} - MD^seg - W^seg - B^seg``, with **no interim interest**: the
    0% floor design credits nothing during the segment term [S2], in contrast with
    one carrier's in-segment 0.75% [S3], which is a different guarantee and must not
    be mixed with a 0% annual floor.  A closing balance: the value at the end of
    month ``t`` is the notes' ``S_{k,t+1}``.  ``k`` is the segment's slot, its months since
    creation in month ``t``, ``duration_mth(t) - m`` for the segment born in policy month
    ``m``: 0 in its creation month, where its balance is its creation balance,
    :func:`seg_new_pp`, and 11 in the last month it is live.  Its balance a month earlier is
    the same segment's in slot ``k - 1`` at ``t - 1``.

    Zero outside slots 0 to ``min(11, duration_mth(t))``: below 0, for a segment not yet
    born, past the policy's months (no segment exists before issue) and past 11, and outside
    cover.  A segment created at ``m`` is live through the end of policy month ``m + 11``
    and matures at step 2 of policy month ``m + 12``, before that month's deduction -- so it
    bears eleven in-segment deductions.  The worked example stipulates twelve; see
    ``products/indexed_ul/model.md``.  In the first month on the books, :func:`t_entry`, a
    segment born before the valuation date opens from the ladder, :func:`seg_bal_pp_init` at
    its slot, its balance entering month 0.  ``IUL_US_S`` keys the cell by the creation
    month, ``seg_bal_pp(t, m)``; the slot is what lets a compiled cache hold twelve segments
    a month rather than every creation month of the frame.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    if k < 0 or k > d or k > seg_term_mth - 1:                       # noqa: F821
        return 0.0
    if k == 0:
        return seg_new_pp(d)
    if t > t_entry():
        prev = seg_bal_pp(t - 1, k - 1)
    else:
        prev = seg_bal_pp_init(k)
    return prev - seg_wd_pp(t, k) - seg_ded_pp(t, k)


def seg_ded_cum_pp(t, k):
    """Deductions charged to the segment in slot k, through the end of month t.

    Zero in the creation month itself, slot 0 (the segment is created after that month's
    deduction), outside the segment's life and outside cover.  Its running total a month
    earlier is the same segment's in slot ``k - 1`` at ``t - 1``.  In the first month on
    the books, :func:`t_entry`, a segment born before the valuation date opens from the
    ladder, :func:`seg_ded_cum_pp_init` at its slot, the deductions charged to it before
    month 0.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    if k < 1 or k > d or k > seg_term_mth - 1:                       # noqa: F821
        return 0.0
    if t > t_entry():
        prev = seg_ded_cum_pp(t - 1, k - 1)
    else:
        prev = seg_ded_cum_pp_init(k)
    return prev + seg_ded_pp(t, k)


def seg_wd_cum_pp(t, k):
    """Withdrawals and loan transfers out of the segment in slot k, through month t.

    Zero in the creation month itself, slot 0, outside the segment's life and outside cover.
    Its running total a month earlier is the same segment's in slot ``k - 1`` at ``t - 1``.
    In the first month on the books, :func:`t_entry`, a segment born before the valuation
    date opens from the ladder, :func:`seg_wd_cum_pp_init` at its slot, the draws out of it
    before month 0.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    if k < 1 or k > d or k > seg_term_mth - 1:                       # noqa: F821
        return 0.0
    if t > t_entry():
        prev = seg_wd_cum_pp(t - 1, k - 1)
    else:
        prev = seg_wd_cum_pp_init(k)
    return prev + seg_wd_pp(t, k)


def seg_bal_tot_pp(t):
    """The sum of every live segment balance at the end of month t.

    The segments born in policy months ``max(0, duration_mth(t) - 11)`` to
    ``duration_mth(t)``, each read at its slot, ``duration_mth(t) - m``, summed in
    ``IUL_US_S``'s order in the compensated loop :func:`seg_bal_active_pp` sums in, so that
    the total is ``IUL_US_S``'s ``sum()`` bit for bit from Python 3.12.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    s = 0.0
    c = 0.0
    for m in range(max(0, d - seg_term_mth + 1), d + 1):             # noqa: F821
        x = seg_bal_pp(t, d - m)
        u = s + x
        if abs(s) >= abs(x):
            c = c + ((s - u) + x)
        else:
            c = c + ((x - u) + s)
        s = u
    if c != 0.0 and abs(c) <= 1.7976931348623157e308:
        s = s + c
    return s


def seg_count(t):
    """The number of segments with a positive balance at the end of month t.

    At most ``seg_term_mth`` (12), the contractual maximum [S4]; zero throughout
    for a model point with ``index_alloc_rate() == 0``.  A segment counts where its
    balance, read at its slot, is above zero, ``IUL_US_S``'s own test, which a balance
    closing on a rounding about zero meets by its sign.  An int, counted in a loop, and the
    int 0 outside cover.
    """
    if not is_active(t):
        return 0
    d = duration_mth(t)
    n = 0
    for m in range(max(0, d - seg_term_mth + 1), d + 1):             # noqa: F821
        if seg_bal_pp(t, d - m) > 0:
            n = n + 1
    return n


def seg_index_start(t):
    """I(m): the index level at the creation of the segment maturing in month t.

    The segment maturing in month ``t`` was born twelve months earlier.  Born in the frame,
    at month ``t - 12``, it started from ``index_level(t - 12)``; born before the valuation
    date, in ladder slot ``12 - t``, from the start level its ladder row carries,
    :func:`seg_index_start_init`, on the same path.  ``IUL_US_S`` reads
    ``index_level(t - 12)``, a month of its own frame, since no segment it projects was
    born before its first month.  Zero where nothing matures, in a policy's first twelve
    policy months, and outside cover.
    """
    if not is_active(t) or duration_mth(t) < seg_term_mth:          # noqa: F821
        return 0.0
    if t - seg_term_mth >= t_entry():                                # noqa: F821
        return index_level(t - seg_term_mth)                         # noqa: F821
    return seg_index_start_init(seg_term_mth - t)                    # noqa: F821


def seg_index_cap(t):
    """c_m: the cap of the segment maturing in month t, the one declared at its creation.

    Born in the frame, at month ``t - 12``, the segment is capped at the cap in force then,
    ``index_cap_at(t - 12)``; born before the valuation date, in ladder slot ``12 - t``, at
    the cap its ladder row carries, :func:`seg_index_cap_init`.  The cap is re-declared at
    every segment start [S3][S4], and a segment keeps the one declared at its own.
    ``IUL_US_S`` holds the cap level and its engine reads ``index_cap_at(0)``, the cap in
    force at its own ``t = 0``, for every segment, so the two agree on every point it
    projects.  Zero where nothing matures and outside cover.
    """
    if not is_active(t) or duration_mth(t) < seg_term_mth:          # noqa: F821
        return 0.0
    if t - seg_term_mth >= t_entry():                                # noqa: F821
        return index_cap_at(t - seg_term_mth)                        # noqa: F821
    return seg_index_cap_init(seg_term_mth - t)                      # noqa: F821


def seg_return(t):
    """r_k for the segment maturing in month t: its own point-to-point index change.

    ``index_level(t) / seg_index_start(t) - 1``, the level now over the segment's start
    level, :func:`seg_index_start`: :func:`index_change` inlined, as no projection cell
    calls an engine cell (R14).  Each segment carries its own index start level, which is
    the whole point of a monthly ladder: collapsing twelve segments into one annual
    segment mis-times credits and distorts mid-segment surrender values [S3].  Zero where
    nothing matures, in a policy's first twelve policy months, and outside cover, where
    ``IUL_US_S`` leaves it to every caller to guard.
    """
    if not is_active(t) or duration_mth(t) < seg_term_mth:           # noqa: F821
        return 0.0
    return index_level(t) / seg_index_start(t) - 1


def seg_credit_rate(t):
    """cr_k for the segment maturing in month t: ``max(f, min(c, p x r))``.

    :func:`index_credit_rate` inlined for the projection (R14): the floor
    ``index_floor``, the cap declared at the segment's creation, :func:`seg_index_cap`,
    and the participation ``index_par`` on its own return, :func:`seg_return`, bounded in
    ``IUL_US_S``'s order, the cap first and then the floor, so that a return that is not a
    number credits the cap, and a cap that is not a number the floor, in both engines
    alike: ``min`` and ``max`` keep their first argument unless a later one compares past
    it, in Python as in the C two-argument form.  Cached by month, where the engine cell is
    keyed by floats.  :func:`index_credit_pp` multiplies it by the credit base, and
    :func:`cred_rate_ann` reads it as the policy's credited rate.  Zero where nothing
    matures, in a policy's first twelve policy months, and outside cover.
    """
    if not is_active(t) or duration_mth(t) < seg_term_mth:           # noqa: F821
        return 0.0
    return max(index_floor, min(seg_index_cap(t), index_par * seg_return(t)))  # noqa: F821


def index_credit_pp(t):
    """The index credit added to the account value at BOM of month t.

    The segment born in policy month ``m = duration_mth(t) - 12`` matures now: its credit is
    ``IUL_US_S``'s ``index_credit`` of its creation balance net of withdrawals and loan
    transfers, the deductions charged to it, its own point-to-point return, the credit base
    convention ``seg_credit_base_conv`` and the cap declared at its creation, inlined (R14):
    the credited rate, :func:`seg_credit_rate`, first, then the base, the remaining balance
    under ``REMAINING`` and the deductions half-weighted under ``ADJ_BEGIN``, then their
    product, ``IUL_US_S``'s order of operations, and a convention neither code names refused
    after the rate, ``"invalid credit base"``, as there.  The draws and deductions to date
    are the segment's at the end of month ``t - 1``, in slot 11; in the first month on the
    books, :func:`t_entry`, a segment born before the valuation date is ladder slot 12,
    whose draws and deductions are its ladder row's.  Zero in a policy's first twelve policy
    months, in every month for a model point that never creates a segment, and outside
    cover.
    """
    if not is_active(t):
        return 0.0
    m = duration_mth(t) - seg_term_mth                               # noqa: F821
    if m < 0:
        return 0.0
    if t > t_entry():
        wd = seg_wd_cum_pp(t - 1, seg_term_mth - 1)                  # noqa: F821
        ded = seg_ded_cum_pp(t - 1, seg_term_mth - 1)                # noqa: F821
    else:
        wd = seg_wd_cum_pp_init(seg_term_mth)                        # noqa: F821
        ded = seg_ded_cum_pp_init(seg_term_mth)                      # noqa: F821
    init = seg_new_pp(m) - wd
    rate = seg_credit_rate(t)
    if seg_credit_base_conv == REMAINING:                            # noqa: F821
        base = init - ded
    elif seg_credit_base_conv == ADJ_BEGIN:                          # noqa: F821
        base = init - ded / 2
    else:
        raise ValueError("invalid credit base")
    return rate * base


def index_credits(t):
    """Index credits added to account values, for the policies in force."""
    return index_credit_pp(t) * pols_if(t)


def seg_roll_pp(t):
    """Roll^FA_t: the matured segment value rolled into the fixed account at step 2.

    Remaining balance plus index credit.  Under the standing allocation instruction it
    is swept straight back into a new segment at step 7 **[std]** (spec F11); routing
    it through the fixed account is what makes it available to pay this month's
    deduction first, which is the notes' own sourcing rule.  The remaining balance is
    the segment's at the end of month ``t - 1``, in slot 11, or, in the first month on the
    books, :func:`t_entry`, ladder slot 12's.  Zero in a policy's first twelve policy
    months and outside cover.
    """
    if not is_active(t):
        return 0.0
    m = duration_mth(t) - seg_term_mth                               # noqa: F821
    if m < 0:
        return 0.0
    if t > t_entry():
        prev = seg_bal_pp(t - 1, seg_term_mth - 1)                   # noqa: F821
    else:
        prev = seg_bal_pp_init(seg_term_mth)                         # noqa: F821
    return prev + index_credit_pp(t)


def fa_pp_at(t, timing):
    """FA: the fixed (holding) account balance at an intra-month point of month t.

    The notes' recursion
    ``FA_{t+1} = [FA_t + NP_t - MD^FA - W^FA - B^FA - Sweep + Roll^FA] x (1+i_fix)^(1/12)``
    unrolled, with ``timing`` naming the point just before each event:

    ``BEF_PREM``
        The opening balance, the notes' ``FA_t``: the closing balance of the previous
        month, formed here from month ``t - 1``'s own opening balance and events, the
        same operations in the same order as :func:`fa_pp`, so that the chain back to the
        first month on the books is one cell a month.  In that month, :func:`t_entry`, it
        is :func:`fa_pp_init`, the fixed account the point carries into the valuation
        month, 0 at issue (``FA(0) = 0``).  ``IUL_US_S`` opens an in-force point at the
        account value less the loan here, everything outside the collateral in the
        fixed account.  Zero outside cover.

    ``BEF_CREDIT``
        After the net premium, before the maturing segment rolls in.

    ``BEF_WD``
        After the roll, before the withdrawal and any new loan collateral.

    ``BEF_FEE``
        After the draw, before the monthly deduction.

    ``BEF_SWEEP``
        After the deduction, before the sweep.  This is the balance the sweep takes
        ``w_ix`` of.

    ``BEF_INV``
        After the sweep, before interest.  Interest is credited on this balance;
        reversing the two overstates the account value by about one month's interest on
        the deduction, every month.

    The balance may run below zero: no policy is terminated for insufficiency, and the
    fixed account carries whatever the segments cannot (:func:`draw_from_fa_pp`).
    """
    if timing == BEF_PREM:                                           # noqa: F821
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return fa_pp_init()
        bef = fa_pp_at(t - 1, BEF_PREM) + prem_to_av_pp(t - 1)       # noqa: F821
        bef = bef + seg_roll_pp(t - 1)
        bef = bef - draw_from_fa_pp(t - 1)
        bef = bef - mth_deduction_from_fa_pp(t - 1)
        bef = bef - sweep_pp(t - 1)
        return bef * (1 + inv_return_mth(t - 1))
    elif timing == BEF_CREDIT:                                       # noqa: F821
        return fa_pp_at(t, BEF_PREM) + prem_to_av_pp(t)              # noqa: F821
    elif timing == BEF_WD:                                           # noqa: F821
        return fa_pp_at(t, BEF_CREDIT) + seg_roll_pp(t)              # noqa: F821
    elif timing == BEF_FEE:                                          # noqa: F821
        return fa_pp_at(t, BEF_WD) - draw_from_fa_pp(t)              # noqa: F821
    elif timing == BEF_SWEEP:                                        # noqa: F821
        return fa_pp_at(t, BEF_FEE) - mth_deduction_from_fa_pp(t)    # noqa: F821
    elif timing == BEF_INV:                                          # noqa: F821
        return fa_pp_at(t, BEF_SWEEP) - sweep_pp(t)                  # noqa: F821
    else:
        raise ValueError("invalid timing")


def fa_pp(t):
    """FA_{t+1}: the fixed (holding) account balance at the end of month t.

    A closing balance: the post-sweep balance plus one month's interest at the
    fixed-account rate.  The opening balance of the month, :func:`fa_pp_init` in the
    first month on the books, is ``fa_pp_at(t, BEF_PREM)``, which forms this cell's
    value at ``t - 1`` itself rather than calling for it.  Zero outside cover.
    """
    return fa_pp_at(t, BEF_INV) * (1 + inv_return_mth(t))            # noqa: F821


def lca_pp_at(t, timing):
    """LCA: the loan collateral account at an intra-month point of month t.

    ``BEF_PREM`` is the opening balance, the notes' ``LCA_t``: the closing balance of
    the previous month, formed here from month ``t - 1``'s own opening balance and new
    loan, the same operations in the same order as :func:`lca_pp`, so that the chain is
    one cell a month; in the first month on the books, :func:`t_entry`, it is
    :func:`lca_pp_init`, the collateral the point carries into the valuation month, 0 at
    issue.  ``IUL_US_S`` sets ``LCA(0)`` equal to ``loan_bal_init()`` **[std]**, which the
    collateral parts from once interest accrues.  ``BEF_INV`` adds the collateral for
    any new loan taken at step 3, which is the balance one month's interest is credited
    on.  Zero outside cover.
    """
    if timing == BEF_PREM:                                           # noqa: F821
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return lca_pp_init()
        return ((lca_pp_at(t - 1, BEF_PREM) + loan_new_pp(t - 1))    # noqa: F821
                * (1 + loan_credit_rate_mth(t - 1)))
    elif timing == BEF_INV:                                          # noqa: F821
        return lca_pp_at(t, BEF_PREM) + loan_new_pp(t)               # noqa: F821
    else:
        raise ValueError("invalid timing")


def lca_pp(t):
    """LCA_{t+1}: the loan collateral account at the end of month t.

    Standard loans move loaned value out of the fixed account and the segments into a
    collateral account credited at :func:`loan_credit_rate_ann` while the loan itself
    accrues at the charged rate; the collateral remains part of the account value, so a
    loan advance does not reduce ``AV`` -- it reduces the cash surrender value through
    ``- L_t``.  A closing balance; the opening value, :func:`lca_pp_init` in the first
    month on the books, is ``lca_pp_at(t, BEF_PREM)``.  Zero outside cover.
    """
    return lca_pp_at(t, BEF_INV) * (1 + loan_credit_rate_mth(t))     # noqa: F821


def loan_bal_pp(t):
    """L_{t+1}: the policy loan balance at the end of month t.

    ``L_{t+1} = (L_t + B_t) (1 + i_L^c)^(1/12)``, the notes' own recursion: new loans
    from step 3 are added to principal and the whole balance accrues at the charged
    rate.  The opening balance ``L_t`` is the previous month's, and in the first month on
    the books, :func:`t_entry`, :func:`loan_bal_init`, the loan the point carries into
    the valuation month, 0 at issue.  Repayments are not modeled -- the notes give no
    repayment pattern.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = loan_bal_init() if t == t_entry() else loan_bal_pp(t - 1)
    return (opening + loan_new_pp(t)) * (1 + loan_rate_mth())


def inv_income_pp(t):
    """Interest credited to the account value per policy at EOM of month t.

    The post-sweep fixed-account balance at the fixed-account monthly rate plus the
    loan collateral account at the collateral credited rate.  **Segments contribute
    nothing**: they earn no interim interest under a 0% floor design [S2], and their
    whole return arrives as :func:`index_credit_pp` at maturity.  Keeping the two apart
    is what stops the floor being confused with an in-segment guarantee, which the notes
    list among the pitfalls.
    """
    return (fa_pp_at(t, BEF_INV) * inv_return_mth(t)                 # noqa: F821
            + lca_pp_at(t, BEF_INV) * loan_credit_rate_mth(t))       # noqa: F821


def inv_income(t):
    """Interest credited to account values, for the policies in force.

    Decrements fall after the credit, so every policy in force at BOM earns a full
    month's interest.
    """
    return inv_income_pp(t) * pols_if(t)


def av_pp_at(t, timing):
    """AV: the account value per policy at an intra-month point of month t.

    The account value is the fixed account plus every live segment plus the loan
    collateral account; ``timing`` names the point just before each BOM event:

    ``BEF_PREM``
        Before the premium: the opening balance, the notes' ``AV_t`` -- the closing
        balance of the previous month, formed here from month ``t - 1``'s own opening
        balance and events, the same operations in the same order as :func:`av_pp`, so
        that the chain is one cell a month.  In the first month on the books,
        :func:`t_entry`, a point in force opens from its parts, :func:`fa_pp_init` plus
        :func:`lca_pp_init` plus the ladder's balances, :func:`seg_bal_pp_init`, slot by
        slot, summed in the compensated loop :func:`seg_bal_active_pp` sums in, so that
        an extract carried to the cent opens one account, its parts' sum, which
        :func:`check_av_components` then holds; any other point opens from
        :func:`av_pp_init`, 0 at issue.  It is also defined in the month after the frame,
        ``t = proj_len()``, where it is the account value the survivors of the last month
        carry, which :func:`check_av_roll_fwd` reads.  Zero before issue.

    ``BEF_CREDIT``
        After the net premium, before the maturing segment's index credit.  Zero outside
        cover, and so is every later timing.

    ``BEF_WD``
        After the index credit, before the withdrawal.  The roll of the matured segment
        into the fixed account is internal and does not change this total.

    ``BEF_FEE``
        After the withdrawal, before the monthly deduction.  This is the notes'
        ``AV'_t``, the balance the death benefit, the corridor test and the net amount
        at risk are all measured against.  A new loan does not change it: the collateral
        moves within the account value.

    ``BEF_INV``
        After the monthly deduction, before interest.

    The end-of-month balance, the notes' ``AV_{t+1}``, is :func:`av_pp`, and
    :func:`check_av_components` asserts that it still equals the sum of its three
    parts.
    """
    if timing == BEF_PREM:                                           # noqa: F821
        if not 0 <= duration_mth(t) <= maturity_mth():
            return 0.0
        if t == t_entry():
            if duration_mth_init() <= 0:
                return av_pp_init()
            s = fa_pp_init()
            c = 0.0
            for k in range(min(seg_term_mth, duration_mth_init()) + 1):  # noqa: F821
                x = lca_pp_init() if k == 0 else seg_bal_pp_init(k)
                u = s + x
                if abs(s) >= abs(x):
                    c = c + ((s - u) + x)
                else:
                    c = c + ((x - u) + s)
                s = u
            if c != 0.0 and abs(c) <= 1.7976931348623157e308:
                s = s + c
            return s
        av = (av_pp_at(t - 1, BEF_PREM) + prem_to_av_pp(t - 1)       # noqa: F821
              + index_credit_pp(t - 1) - wd_pp(t - 1) - mth_deduction_pp(t - 1))
        return av + inv_income_pp(t - 1)
    elif timing == BEF_CREDIT:                                       # noqa: F821
        if not is_active(t):
            return 0.0
        return av_pp_at(t, BEF_PREM) + prem_to_av_pp(t)              # noqa: F821
    elif timing == BEF_WD:                                           # noqa: F821
        return av_pp_at(t, BEF_CREDIT) + index_credit_pp(t)          # noqa: F821
    elif timing == BEF_FEE:                                          # noqa: F821
        return av_pp_at(t, BEF_WD) - wd_pp(t)                        # noqa: F821
    elif timing == BEF_INV:                                          # noqa: F821
        return av_pp_at(t, BEF_FEE) - mth_deduction_pp(t)            # noqa: F821
    else:
        raise ValueError("invalid timing")


def av_pp(t):
    """AV_{t+1}: the account value per policy at the end of month t.

    A closing balance: the post-deduction balance plus one month's interest.  The
    opening balance, :func:`av_pp_init` in the first month on the books, is
    ``av_pp_at(t, BEF_PREM)``, which forms this cell's value at ``t - 1`` itself.
    Interest is credited on the *post-deduction* balance, as on the universal life
    chassis; the index credit is not part of it -- that arrives at BOM when a segment
    matures.  Zero outside cover.
    """
    return av_pp_at(t, BEF_INV) + inv_income_pp(t)                   # noqa: F821


def av_at(t, timing):
    """Account value in force at an intra-month point of month t.

    :func:`av_pp_at` times the number of policies in force, which is constant through
    the month because decrements are end-of-month events.  ``timing`` takes the same
    values as :func:`av_pp_at`, plus ``EOM`` for the closing balance before
    decrements.  At ``t = proj_len()``, ``av_at(t, BEF_PREM)`` is the account value the
    survivors of the last month carry, which :func:`check_av_roll_fwd` reads.
    """
    if timing == EOM:                                                # noqa: F821
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
    return av_at(t + 1, BEF_PREM) - av_at(t, BEF_PREM)               # noqa: F821


def surr_charge_rate(t):
    """SC per $1,000 of initial face in month t **[std]** scale (F17).

    ``max(0, sc_init - (sc_init / runoff_years) x m / 12)`` where ``m`` is the notes'
    own month index ``duration_mth(t) + 1`` -- the current month counts.  With the
    shipped schedule of $25.00 per $1,000 running off over 10 years this is $24.79 in
    the issue month, declining linearly to zero in the last month of policy year 10.
    The ten-year period is sourced [S1][S5][S7]; the dollar scale is not public and is
    a placeholder of realistic magnitude.  The schedule's two values are read once a
    point by :func:`surr_charge_rate_max` and :func:`surr_charge_runoff_years`, which ask
    ``Data`` to check the table first; the floor keeps ``IUL_US_S``'s order,
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

    Quoted on the **initial** face amount, because face decreases do not reduce the
    surrender charge [S3].  This is the schedule, not the amount collected: see
    :func:`surr_charge`.
    """
    return surr_charge_rate(t) * sum_assured() / 1000


def csv_pp(t):
    """``AV_t - SC_t``, floored at zero: the cash value before the loan is netted.

    The floor is **[std]**: the notes write the cash surrender value without one, but a
    negative value would be a payment *from* the policyholder.  In the early policy
    years the scheduled surrender charge exceeds the account value and the floor binds,
    so the charge actually collected is the whole account value.

    The notes' own ``CSV_t`` -- which already nets the loan -- is :func:`ncsv_pp`.
    """
    return max(0.0, av_pp(t) - surr_charge_pp(t))


def ncsv_pp(t):
    """CSV_t = AV_t - SC_t - L_t: the cash surrender value, floored at zero.

    This is what a surrendering policyholder is paid, and the notes' surrender outflow.
    """
    return max(0.0, csv_pp(t) - loan_bal_pp(t))


def surr_charge(t):
    """Surrender charge actually collected from the policies lapsing in month t.

    ``(AV_t - csv_pp(t)) x pols_lapse(t)``, so it is capped by the account value where
    the :func:`csv_pp` floor binds.  Insurer income, and part of
    :func:`margin_expense`.
    """
    return (av_pp(t) - csv_pp(t)) * pols_lapse(t)


def cum_prem_pp(t):
    """Cumulative premiums less withdrawals: the base of the GPT and 7-pay tests.

    The value at the end of month ``t``, including month ``t``'s own premium and
    withdrawal.  It opens in the first month on the books, :func:`t_entry`, from
    :func:`cum_prem_init`, the premiums less withdrawals paid before the valuation date on
    a point in force and 0 at issue, so the GPT and 7-pay flags of a point in force count
    every premium since issue.  ``IUL_US_S`` opens it at 0 on any point, the notes giving
    no opening accumulator **[std]**.  The statutory "less a portion of withdrawals" is
    taken as the whole withdrawal **[std]**.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = cum_prem_pp(t - 1) if t > t_entry() else cum_prem_init()
    return opening + premium_pp(t) - wd_pp(t)


def cum_prem_net_pp(t):
    """CumP_{t+1}: cumulative premiums less withdrawals **and loans**, the no-lapse base.

    The notes define the no-lapse accumulator this way and the guideline premium
    accumulator differently; :func:`cum_prem_pp` is the other one.  Using one for the
    other quietly changes both answers.  The value at the end of month ``t``, opening in
    the first month on the books, :func:`t_entry`, from :func:`cum_prem_net_init`, the
    accumulator the point carries into the valuation month, 0 at issue.  ``IUL_US_S``
    opens it at 0 on any point, which on a point in force would fail the no-lapse test
    against a minimum premium counted from issue.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = cum_prem_net_pp(t - 1) if t > t_entry() else cum_prem_net_init()
    return opening + premium_pp(t) - wd_pp(t) - loan_new_pp(t)


def nlg_period_years():
    """The length of the no-lapse period in policy years, by issue age [S3] (spec F6).

    0-45: 20 years; 46-60: to attained age 65; 61+: 5 years.  Comparators differ --
    another carrier gives 20 years for issue ages 0-55, ``75 - issue age`` for 56-69,
    5 years for 70+ [S5] -- and the structure above [S3] is the one the baseline
    follows.
    """
    x = age_at_entry()
    if x <= 45:
        return 20
    elif x <= 60:
        return max(0, 65 - x)
    return 5


def mnlp_pp_mth():
    """The minimum monthly no-lapse premium per policy [S3].

    ``mnlp_rate x F / 1000 / 12``: the annual rate per $1,000 of face spread evenly
    over the year.
    """
    return mnlp_rate() * sum_assured() / 1000 / 12


def cum_mnlp_pp(t):
    """CumMNLP_{t+1}: the cumulative minimum no-lapse premium through month t.

    ``mnlp_pp_mth() x (duration_mth(t) + 1)``: a closed form on the **policy** clock,
    every month from issue counted, so a point in force needs no opening value for it.
    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return mnlp_pp_mth() * (duration_mth(t) + 1)


def nlg_test_ok(t):
    """The cumulative-premium no-lapse test: ``CumP_t >= CumMNLP_t`` [S3][S4].

    False outside cover.
    """
    if not is_active(t):
        return False
    return cum_prem_net_pp(t) >= cum_mnlp_pp(t)


def nlg_in_effect(t):
    """Whether the no-lapse guarantee is in effect: inside the period and test passing.

    While it is, the policy cannot lapse for insufficiency even with no cash surrender
    value [S3][S4], which is why :func:`lapse_rate` suppresses voluntary lapse in that
    state as well **[std]**.  The period counts policy years, from issue.  False outside
    cover, before the policy year is compared.
    """
    if not is_active(t):
        return False
    return policy_year(t) <= nlg_period_years() and nlg_test_ok(t)


def nlg_expiry_shock(t):
    """Whether the 25% no-lapse-expiry shock lapse applies in month t **[std]**.

    The notes apply a 25% shock lapse to *underfunded* policies on no-lapse expiry;
    "underfunded" is taken as a non-positive cash surrender value **[std]**, and the
    shock is confined to the first policy year after the no-lapse period ends.  False
    outside cover, before the policy year is compared.
    """
    if not is_active(t):
        return False
    return policy_year(t) == nlg_period_years() + 1 and ncsv_pp(t) <= 0


def is_shortfall(t):
    """The grace trigger: the cash surrender value cannot cover the monthly deduction.

    ``AV'_t - SC_t - L_t < MD_t`` -- with ``L_t`` the loan balance at the *start* of
    the month, the previous month's :func:`loan_bal_pp`, or, in the first month on the
    books, :func:`t_entry`, :func:`loan_bal_init` -- **and** the no-lapse test fails
    [S3][S4].  A diagnostic.  The grace and lapse-for-insufficiency cascade (61 days,
    modeled as lapse at ``t + 2`` months if unfunded **[std]**) is **not implemented**:
    the notes leave the in-grace account value treatment and the cash flow of a cure
    payment undetermined, so no policy is terminated for insufficiency here.  False
    outside cover.
    """
    if not is_active(t):
        return False
    loan_opening = loan_bal_init() if t == t_entry() else loan_bal_pp(t - 1)
    csv = av_pp_at(t, BEF_FEE) - surr_charge_pp(t) - loan_opening    # noqa: F821
    return csv < mth_deduction_pp(t) and not nlg_in_effect(t)


def gpt_limit(t):
    """The guideline premium limit, ``max(GSP, GLP x policy years elapsed)`` [R4].

    Zero outside cover, where the policy year is not the policy's.
    """
    if not is_active(t):
        return 0.0
    return max(gsp(), glp() * policy_year(t))


def gpt_ok(t):
    """Whether cumulative premium is still inside the guideline premium limit.

    A compliance side-calculation with no cash flow of its own: a refused premium
    simply never enters the model.  False outside cover.
    """
    if not is_active(t):
        return False
    return cum_prem_pp(t) <= gpt_limit(t)


def seven_pay_limit(t):
    """The 7-pay limit, ``seven_pay_prem x min(7, policy years elapsed)`` [R5].

    Zero outside cover, where the policy year is not the policy's.
    """
    if not is_active(t):
        return 0.0
    return seven_pay_prem() * min(7, policy_year(t))


def is_mec(t):
    """Whether the 7-pay test has failed by month t -- once true, true for good [R5].

    ``CumPrem(t) > 7-pay limit`` in any of the first seven policy years, **latched**:
    the flag stays set for the rest of the projection.  ``IUL_US_S``'s flag is the
    in-year test alone, which stops applying in policy year 8 and so would switch itself
    off exactly when the failure becomes permanent; under IRC 7702A a contract that fails
    the test is a modified endowment contract for good, so this model latches it, as
    ``UL_US_S`` does.

    The in-year test comes first in every month, the first on the books included, so a
    policy that fails it in the valuation month is a MEC from then on.  Only then does
    the latch look back: to month ``t - 1``, or, in the first month on the books,
    :func:`t_entry`, to :func:`is_mec_init`, so a policy that failed the test before the
    valuation date stays a MEC, even in a year where the in-year test no longer applies.
    False outside cover.

    A flag, not a cash flow: MEC status changes policyholder taxation, not insurer
    liability cash flows.
    """
    if not is_active(t):
        return False
    if policy_year(t) <= 7 and cum_prem_pp(t) > seven_pay_limit(t):
        return True
    return is_mec(t - 1) if t > t_entry() else is_mec_init()


def class_factor():
    """The underwriting-class multiplier on the base mortality table **[std]**.

    ``Data.class_factor`` at the point: the ``factor`` of the point's ``rate_class`` in
    *class_factor_table.csv*, joined once for the table after ``data.class_count()`` has
    checked its classes and factors, so that no projection cell reads the table or the
    class: a blank factor would otherwise reach :func:`mort_rate` as a missing value, which
    its cap keeps missing.  A class the table has no row for is refused by ``Data``, naming
    every such point, at the first read, where ``IUL_US_S`` raises pandas' ``KeyError`` in
    every point's first month in cover.
    """
    return float(data.class_factor()[idx])                           # noqa: F821


def mort_rate(t):
    """The annual best-estimate mortality rate in month t.

    Base table times :func:`class_factor` times the A/E factor, 100% in the base run
    **[std]** with no mortality improvement.  The notes recommend 2015 VBT
    sex/smoker-distinct ANB validated against ILEC 2012-2019 [REG-R18][REG-R19]; those
    tables are licensed, so the shipped table is a small illustrative one **[std]**.
    Ages beyond the table take its last row, where the rate is 1.0; the base rate is read
    at the attained age of month t by :func:`mort_rate_base_at`.

    The product is capped at 1, written ``min(q, 1.0)``, as ``IUL_US_S``'s is: a class
    factor above 1 carries the oldest ages' rates past 1, where the monthly rate
    ``1 - (1 - q)^(1/12)`` has no real value, and with the bound second a missing input, a
    NaN, stays NaN, where ``min(1.0, q)`` would read it as 1.  On every shipped point the
    product reaches 1.0, at attained age 119, and never passes it, so the cap changes no
    shipped number.  ``Data`` refuses a blank rate or class factor as it reads the tables
    (``data.mort_age_last()``, ``data.class_count()``), before any rate is read.  Zero
    outside cover, before the table is read.
    """
    if not is_active(t):
        return 0.0
    q = mort_rate_base_at(age(t)) * class_factor() * mort_ae_factor  # noqa: F821
    return min(q, 1.0)


def mort_rate_base_at(a):
    """The base table's annual mortality rate at attained age a: the table's one reader.

    From *mort_table.csv*, before the class factor and the A/E factor:
    ``Data.mort_table_array()`` at the age, the table padded from age 0, so that the age is
    the index.  Ages outside the table take its nearest row, which above it is the rate of
    1.0 at age 120: the first and last ages ``data.mort_age_first()`` and
    ``data.mort_age_last()`` give, which they read from the table's key column once the keys
    and the rates are checked, before any rate is read, the last first, as
    :func:`corridor_factor_at` asks, and which keep the read off the padding.  Keyed by the
    attained age, so the table is read once an age rather than once a month;
    :func:`mort_rate` calls it inside cover only.
    """
    last = data.mort_age_last()                                      # noqa: F821
    a = min(max(a, data.mort_age_first()), last)                     # noqa: F821
    return float(data.mort_table_array()[a])                         # noqa: F821


def mort_rate_mth(t):
    """q^d_t: the monthly mortality rate, ``1 - (1 - q)^(1/12)`` **[std]** conversion."""
    return 1 - (1 - mort_rate(t)) ** (1 / 12)


def lapse_rate_base(t):
    """The base annual lapse rate by policy year **[std]**.

    6% in policy years 1-10, 4% thereafter, read from *lapse_table.csv* at the policy
    year of month t by :func:`lapse_rate_base_py`, where policy years beyond the table
    take its last row.  The levels are placeholders to be calibrated to the LIMRA/SOA
    persistency studies [REG-R20][REG-R21], whose detailed tables are behind a paid
    package.  Zero outside cover, before the table is read.
    """
    return lapse_rate_base_py(policy_year(t)) if is_active(t) else 0.0


def lapse_rate_base_py(y):
    """The base annual lapse rate in policy year y, from *lapse_table.csv*: its one reader.

    ``Data.lapse_rate_array()`` at the year, the table padded from year 0, so that the year
    is the index.  Policy years beyond the table take its last row, the last year
    ``data.lapse_last_year()`` gives, which it reads from the table's key column once it
    has checked the keys and the rates, before any rate is read, and a year below 1, where
    ``IUL_US_S``'s lookup raised ``KeyError``, is refused, naming the point and the year.
    Keyed by the contractual policy year, so the table is read once a policy year rather
    than once a month; :func:`lapse_rate_base` calls it inside cover only.
    """
    last = data.lapse_last_year()                                    # noqa: F821
    if y < 1:
        raise ValueError(f"point_id {point_id()}: lapse_table.csv has no rate for policy "
                         f"year {y}")
    return float(data.lapse_rate_array()[min(y, last)])              # noqa: F821


def lapse_shock_year():
    """The policy year of the surrender-charge-expiry lapse spike.

    The first policy year with no surrender charge -- the run-off length plus one,
    which is 11 for the shipped ten-year schedule -- derived from the schedule's
    :func:`surr_charge_runoff_years` rather than hard-coded, so a different schedule moves
    the spike with it.  Zero when the model point carries no surrender charge, which no
    policy year in cover can equal.  The valuation clock reaches policy year 0 in the
    twelve months before issue, which is why :func:`lapse_rate_sc_mult` asks
    :func:`is_active` first.
    """
    if not has_surr_charge():
        return 0
    return int(surr_charge_runoff_years()) + 1


def lapse_rate_sc_mult(t):
    """The surrender-charge-expiry spike multiplier, 2.0 in policy year 11 **[std]**.

    The ten-year surrender charge period [S1][S5][S7] creates a cliff in surrender
    economics; the size of the spike is a shape assumption, and UL lapse and surrender
    experience by duration is available in [REG-R21] for calibration.  1.0 outside
    cover, before the policy year is compared: in the twelve months before issue the
    valuation clock reaches policy year 0, the shock year :func:`lapse_shock_year` gives a
    point with no surrender charge.
    """
    if not is_active(t):
        return 1.0
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def cred_rate_ann(t):
    """r_cred,t: the policy's trailing credited rate, driving dynamic lapse **[std]**.

    The credited rate of the segment that matured this month once the ladder is
    running, from policy month 12 on, :func:`seg_credit_rate`, at the cap declared at its
    creation; and the fixed-account rate before that or when nothing is allocated to the
    indexed account.  The notes say only "the policy's trailing credited rate"; this is
    the reading the model uses.  The ladder runs from the policy's own twelfth month, so
    the test is on the **policy** clock, ``duration_mth(t)``, where ``IUL_US_S``'s compares
    ``t`` itself, its frame's month, which is the same month only on a point issued at its
    frame's start.  A segment holding nothing still has a start level and a cap, so this
    reads them in every month the ladder runs.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if index_alloc_rate() <= 0 or duration_mth(t) < seg_term_mth:    # noqa: F821
        return fixed_rate_ann(t)
    return seg_credit_rate(t)


def comp_rate_ann(t):
    """r_alt: the competitor / market alternative rate **[std]**.

    The base deterministic run sets it equal to the trailing credited rate, so
    :func:`lapse_rate_dyn_mult` is exactly 1.  Override this cell, before the model
    computes anything, to switch dynamic lapse on; that is a formula override, which only
    modelx can make.  The rationale the notes give is real: caps are non-guaranteed
    elements and uncompetitive re-declarations -- caps on one product fell from 13.75% to
    12.00% between two print dates [S3][S4] -- plausibly drive excess lapse.
    """
    return cred_rate_ann(t)


def lapse_rate_dyn_mult(t):
    """The dynamic lapse multiplier **[std]**.

    ``min(2.0, max(0.5, 1 + 3.0 x (r_alt - r_cred,t)))``: a competitive credited rate
    halves lapse at the floor and an uncompetitive one doubles it at the cap.  Equal to
    1 throughout the base run.  The bounds keep ``IUL_US_S``'s order, written first.  1.0
    outside cover, the neutral multiplier.
    """
    if not is_active(t):
        return 1.0
    raw = 1 + lapse_dyn_slope * (comp_rate_ann(t) - cred_rate_ann(t))  # noqa: F821
    return min(lapse_dyn_cap, max(lapse_dyn_floor, raw))             # noqa: F821


def lapse_rate(t):
    """The total annual lapse rate **[std]**.

    Base rate times the surrender-charge-expiry spike times the dynamic multiplier,
    with two no-lapse-guarantee overrides the notes specify:

    * while the guarantee is in effect and the cash surrender value is non-positive,
      lapse is **suppressed** -- policyholders paying no-lapse-premium-level premiums
      persist;
    * in the first policy year after the no-lapse period ends, an underfunded policy
      takes a 25% shock lapse.

    ``lapse_rate_cap`` is 1.0: these notes give no cap, unlike the universal life
    chassis, so the Reference is present for symmetry and inert at its shipped value.
    The shock lapse is returned before the cap, as ``IUL_US_S`` returns it, so an
    ``nlg_shock_lapse`` past 1 is a rate past 1, whose monthly rate has no real value.
    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if nlg_in_effect(t) and ncsv_pp(t) <= 0:
        return 0.0
    if nlg_expiry_shock(t):
        return nlg_shock_lapse                                       # noqa: F821
    rate = lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_rate_dyn_mult(t)
    return min(lapse_rate_cap, rate)                                 # noqa: F821


def lapse_rate_mth(t):
    """q^w_t: the monthly lapse rate, ``1 - (1 - w)^(1/12)`` **[std]** conversion."""
    return 1 - (1 - lapse_rate(t)) ** (1 / 12)


def pols_if(t):
    """l_t: the number of policies in force at the beginning of month t, row t's weight.

    ``pols_if_at(t, BEF_DECR)``, the notes' ``l_t``: the count carried in from month
    t - 1 plus month t's new business, before month t's decrements.  Decrements are
    end-of-month events, so the number in force is constant through the month and every
    BOM cash flow is weighted by it.  On a point issued at ``t = 0`` it is exactly
    ``IUL_US_S``'s ``pols_if``.  A point in force at the valuation date opens with
    :func:`pols_if_init`, and one issued at or after it with its issued count in the
    issue month.  Zero before issue.  At ``t = proj_len()``, the month after the frame,
    it is the survivors of the last month, which the roll-forwards read.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity.
    """
    return pols_if_at(t, BEF_DECR)                                   # noqa: F821


def pols_if_at(t, timing):
    """Number of policies in force at a point of month t, by ``timing``.

    The three timings ``IUL_US_S``'s cell names:

    ``BEF_NB``
        The count carried in from month t - 1, before month t's new business: month
        t - 1's ``BEF_DECR`` count less its deaths and lapses, death applied before
        lapse, in ``IUL_US_S``'s order.  In the first month on the books,
        :func:`t_entry`, it is :func:`pols_if_init`, the count in force at the valuation
        date (0 for a point issued at or after it), and the recursion reads no earlier
        month.  It is also defined in the month after the frame, ``t = proj_len()``,
        where it is the survivors of the last month: the projection ends at an age
        horizon, not at an event of the contract, so they are kept rather than matured.
        Zero before issue.
    ``BEF_DECR``
        ``l_t``: ``BEF_NB`` plus :func:`pols_new_biz`, before any decrement; the same
        number as :func:`pols_if`, and the weight on that month's cash flows.
    ``BEF_MAT``
        Before any maturity: ``IUL_US_S``'s meaning, the ``BEF_DECR`` count, which its
        cell gives for this timing.  The contract has no maturity in the frame, so
        nothing matures and no event of the month separates the two.
        ``basiclife.BasicTerm_SE``'s ``BEF_MAT``, the count at the start of the month
        before its new business, is not adopted: the name keeps its S model's meaning.

    ``BEF_NB`` forms month t - 1's ``BEF_DECR`` count itself -- its own value at
    ``t - 1`` plus that month's :func:`pols_new_biz` -- and takes its deaths and lapses
    from the month's rates, as :func:`pols_death` and :func:`pols_lapse` do, rather than
    calling for any of them.  So the chain of calls back to :func:`t_entry` is one cell a
    month, as ``IUL_US_S``'s :func:`pols_if` chain was: a compiled model runs that chain
    on the C stack.  ``IUL_US_S``'s cell returns :func:`pols_if` for every
    timing, which in the issue month counts the issued policies under all three; here
    ``BEF_NB`` alone counts them as new business, not yet in.  Any other timing raises.
    """
    if timing == BEF_NB:                                             # noqa: F821
        if not 0 <= duration_mth(t) <= maturity_mth():
            return 0.0
        if t == t_entry():
            return pols_if_init()
        prev = pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1)       # noqa: F821
        q = mort_rate_mth(t - 1)
        return prev - prev * q - prev * (1 - q) * lapse_rate_mth(t - 1)
    elif timing == BEF_DECR:                                         # noqa: F821
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)               # noqa: F821
    elif timing == BEF_MAT:                                          # noqa: F821
        return pols_if_at(t, BEF_DECR)                               # noqa: F821
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
    """Number of deaths at the end of month t, ``pols_if(t) x q^d_t``.

    Zero outside cover, before any rate is read.
    """
    return pols_if(t) * mort_rate_mth(t) if is_active(t) else 0.0


def pols_lapse(t):
    """Number of lapses at the end of month t.

    ``pols_if(t) x (1 - q^d_t) x q^w_t``: death is applied before lapse **[std]**.  Zero
    outside cover, before any rate is read.
    """
    if not is_active(t):
        return 0.0
    return pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)


def pols_maturity(t):
    """Number of maturing policies: always zero.

    At attained age 121 the policy is described as continuing in force with no further
    charges [unverified] (spec F5), so the projection horizon truncates the run rather
    than terminating the contract.  The cell is kept so the in-force roll-forward
    identity has the same shape as in the term and annuity models of this library,
    where it is not zero.  The survivors of the frame's last month do not mature either:
    they are carried into ``t = proj_len()`` (:func:`pols_if_at`).
    """
    return 0.0


def claim_pp(t, kind):
    """The claim amount per policy by ``kind``.

    ``DEATH``
        ``DB_t - L_t``, the death benefit less policy debt.  The loan is taken at its
        end-of-month value because decrements follow the loan accrual, which is how
        these notes write it.

    ``LAPSE``
        ``CSV_t``, the cash surrender value with the surrender charge and the loan
        already netted -- :func:`ncsv_pp`.

    ``WITHDRAWAL``
        ``W_t - $25 fee``: the withdrawal is gross of the fee and the insurer keeps it.
        This kind survives here, though :func:`claims` takes no kind, because the
        per-policy rule has to live somewhere; :func:`withdrawals` is its only caller.
    """
    if kind == DEATH:                                                # noqa: F821
        return max(0.0, db_pp(t) - loan_bal_pp(t))
    elif kind == LAPSE:                                              # noqa: F821
        return ncsv_pp(t)
    elif kind == WITHDRAWAL:                                         # noqa: F821
        return max(0.0, wd_pp(t) - wd_fee_pp(t))
    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):
    """The part of a claim released out of the account value, by ``kind``.

    Death and lapse both release the end-of-month account value ``AV_t``, because
    decrements follow the interest credit.  ``MATURITY`` is zero: the contract does
    not mature within the projection.
    """
    if kind == DEATH:                                                # noqa: F821
        return av_pp(t) * pols_death(t)
    elif kind == LAPSE:                                              # noqa: F821
        return av_pp(t) * pols_lapse(t)
    elif kind == MATURITY:                                           # noqa: F821
        return 0.0
    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    """Death claims in excess of the account value released.

    ``(claim_pp(t, DEATH) - AV_t) x pols_death(t)``.  The cost of insurance charge
    net of this is the mortality margin.
    """
    return (claim_pp(t, DEATH) - av_pp(t)) * pols_death(t)           # noqa: F821


def claims(t):
    """Claim outgo in month t: death and surrender claims together.

    :func:`claims_death` and :func:`claims_lapse`, summed left to right from ``0.0``, the
    total ``IUL_US_S``'s ``claims(t)`` computes with its ``kind=None`` default, ``sum`` over
    the two kinds: a fold of two terms from ``0.0`` is that ``sum``, the sign of a zero
    included, so the total is ``IUL_US_S``'s bit for bit.  Death claims are weighted by
    :func:`pols_death` and surrenders by :func:`pols_lapse`, both end-of-month events.

    ``WITHDRAWAL`` is deliberately **not** in the total: a partial withdrawal is a payment
    on the owner's election rather than a claim, so it is the standalone cell
    :func:`withdrawals` and its own ``result_cf()`` column.  Keeping it out of the total is
    what stops it being counted twice.
    """
    return 0.0 + claims_death(t) + claims_lapse(t)


def claims_death(t):
    """Death claims in month t: :func:`claim_pp` at ``DEATH`` times :func:`pols_death`.

    ``IUL_US_S``'s ``claims(t, "DEATH")``, a cell of its own, so that each kind is a
    monthly cell with a C cache and :func:`claims` their total.  The ``claims_death``
    column of :func:`result_cf`.
    """
    return claim_pp(t, DEATH) * pols_death(t)                        # noqa: F821


def claims_lapse(t):
    """Surrender payments in month t: :func:`claim_pp` at ``LAPSE`` times
    :func:`pols_lapse`.

    ``IUL_US_S``'s ``claims(t, "LAPSE")``, a cell of its own, as :func:`claims_death` is.
    The ``claims_lapse`` column of :func:`result_cf`.
    """
    return claim_pp(t, LAPSE) * pols_lapse(t)                        # noqa: F821


def withdrawals(t):
    """Partial withdrawal payments in month t: ``(W_t - $25 fee) x l_t``.

    Weighted by :func:`pols_if`, because a withdrawal is taken at BOM by policies still
    in force -- it is not a decrement.  The per-policy amount is
    ``claim_pp(t, WITHDRAWAL)``, so the fee-inside-``W_t`` rule is stated
    once; the fee itself stays with the insurer as :func:`wd_fees`.

    A withdrawal is not a claim, and this cell is why :func:`claims`, the death and lapse
    claims, holds no withdrawal.
    """
    return claim_pp(t, WITHDRAWAL) * pols_if(t)                      # noqa: F821


def wd_fees(t):
    """Withdrawal fees retained by the insurer, for the policies in force.

    Taken out of the withdrawal, so this is the difference between what leaves the
    account value and what the policyholder receives; it appears in
    :func:`margin_expense`, not in :func:`claims`.
    """
    return wd_fee_pp(t) * pols_if(t)


def net_loan_cf(t):
    """Net loan cash flow in month t: advances out, repayments in.

    A loan advance is cash the insurer pays out while the account value is unchanged --
    the collateral moves inside it -- so it is a liability cash flow of its own.
    Repayments are not modeled: the notes give no repayment pattern.
    """
    return -loan_new_pp(t) * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor, ``(1 + inflation_rate)^(t // 12)``.

    ``inflation_rate`` is **0** in the base run: these notes give per-policy
    maintenance and per-issue expenses as flat placeholders with no inflation
    assumption, unlike the universal life chassis.  The cell is kept so the chassis'
    shape survives and an inflation assumption can be switched on with one Reference.
    Switched on, it steps by year on the **valuation** clock: the years are counted from
    the valuation date, ``t // 12``, so the expense is in valuation-date dollars whatever
    the policy's age, and every point of a block steps alike, on the valuation date's
    anniversaries.  ``IUL_US_S`` steps on the policy year,
    ``(1 + inflation_rate)^(y - 1)``; on a point issued at ``t = 0`` the two are the same.
    A function of the clock alone, so it holds its value outside cover.  Acquisition is
    not inflated (see :func:`expenses`).
    """
    return (1 + inflation_rate) ** (t // 12)                         # noqa: F821


def expenses(t):
    """E_t: the insurer's own expenses in month t **[std]**.

    ``$75`` a policy a year spread monthly, plus ``$150`` at issue.  Placeholders: the
    notes have no public source for insurer expenses and say to calibrate to company
    studies.  ``IUL_US_S``'s formula in its order, on the policies in force at the start
    of the month: in the issue month those are the policies issued, :func:`pols_new_biz`,
    since a point issued at or after the valuation date opens with none, so acquisition is
    charged per policy issued, as in ``basiclife.BasicTerm_SE``, and a point in force
    never bears it.  On a point issued at ``t = 0`` this is ``IUL_US_S``'s charge bit for
    bit.

    Not to be confused with :func:`maint_fee`, which is the charge *against the account
    value* -- income, not outgo.  Zero outside cover, where the count carried into
    ``t = proj_len()`` would otherwise bear a maintenance expense.
    """
    if not is_active(t):
        return 0.0
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    return (acq + expense_maint / 12 * inflation_factor(t)) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """Premium tax, 2.0% of premium **[std]** placeholder."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def margin_expense(t):
    """Expense margin: the charges the insurer keeps, net of its own outgo.

    ``load x P + withdrawal fees + maint_fee + surrender charges - expenses
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
    """CF_t: the net liability cash flow in month t, **undiscounted**.

    ``premiums - claims - withdrawals - expenses - premium taxes + net loan cash
    flows``, which is the notes' own sign convention (inflow positive) and the
    library-wide one.  :func:`claims` is the death and surrender legs only, so
    :func:`withdrawals` is a term of its own here rather than part of the claim total.
    Policy charges -- the premium load, the monthly deduction, the surrender charge, the
    withdrawal fee -- are internal transfers within the account value, not cash flows;
    they emerge in profit as the margins.  Index credits and fixed-account interest are
    credits to the policyholder, not insurer cash flows, so they do not appear either --
    see :func:`check_margin` for how it all reconciles.  Zero outside cover.
    """
    return (premiums(t) - claims(t) - withdrawals(t) - expenses(t)
            - premium_taxes(t) + net_loan_cf(t))


def check_av_components():
    """Check that the account value is still the sum of its three parts.

    Returns ``True`` when, for every month of the frame,
    ``av_pp(t) == fa_pp(t) + seg_bal_tot_pp(t) + lca_pp(t)`` to within ``1e-9``, relative
    to the larger side and 10, which is what ``IUL_US_S``'s ``math.isclose`` tests with
    its tolerances, ``rel_tol=1e-9`` and ``abs_tol=1e-8``.  :func:`av_pp` is built from the
    notes' aggregate recursion while the fixed account, the segment ladder and the loan
    collateral account are each built from their own; this is the test that the two
    constructions have not drifted, and it is the strongest single check on the segment
    bookkeeping.  On a point in force the three parts open from their own columns and the
    account value from their sum, so an extract carried to the cent holds it too, and
    ``Data`` holds the ``av_pp_init`` column to the same sum.  Each month's residual is
    :func:`check_av_components_resid`, so a failure can be found by month; a residual that
    is not a number fails, and one that is not real raises, as ``IUL_US_S``'s check does.
    """
    for t in range(proj_len()):
        if not abs(check_av_components_resid(t)) <= 1e-9:
            return False
    return True


def check_av_components_resid(t):
    """The account value components' relative residual in month t; zero everywhere.

    ``av_pp(t)`` less the sum of the fixed account, the live segments and the loan
    collateral at the end of month t, over the larger of the two in magnitude and 10: one
    number a month, whose magnitude is within ``1e-9`` exactly where ``math.isclose``
    with ``rel_tol=1e-9`` and ``abs_tol=1e-8`` holds, ``IUL_US_S``'s test.  Returned as a
    ``float``, so that a value that is not real raises here, as ``IUL_US_S``'s
    ``math.isclose`` raises on it.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    parts = fa_pp(t) + seg_bal_tot_pp(t) + lca_pp(t)
    av = av_pp(t)
    return float((av - parts) / max(abs(av), abs(parts), 10.0))


def check_av_roll_fwd():
    """Check the account value roll-forward.

    Returns ``True`` when, for every month of the frame, the opening account value in
    force of month ``t + 1`` equals::

        av_at(t, BEF_PREM)
            + prem_to_av(t)
            + index_credits(t)
            - withdrawals(t)
            - wd_fees(t)
            - mth_deduction(t)
            + inv_income(t)
            - claims_from_av(t, DEATH)
            - claims_from_av(t, LAPSE)

    to within ``1e-9``, relative to the larger of the two and 10, as for
    :func:`check_av_components`.  This pins the notes' processing order: the index credit
    arrives at BOM when a segment matures, interest is credited on the *post-deduction*
    balance, decrements come after both, and the withdrawal fee leaves the account value
    alongside the withdrawal itself.  Each month's residual is
    :func:`check_av_roll_fwd_resid`; a residual that is not a number fails, and one that is
    not real raises, as ``IUL_US_S``'s check does.  In the last month the opening value
    of ``t + 1`` is the account value the survivors carry into ``t = proj_len()``.
    """
    for t in range(proj_len()):
        if not abs(check_av_roll_fwd_resid(t)) <= 1e-9:
            return False
    return True


def check_av_roll_fwd_resid(t):
    """The account value roll-forward's relative residual in month t; zero everywhere.

    The opening account value in force of month ``t + 1`` less the roll-forward of month
    t that :func:`check_av_roll_fwd` sets out, over the larger of the two in magnitude and
    10, and a ``float``, as :func:`check_av_components_resid` is: a monthly rate built from
    an annual one past 1, ``1 - (1 - q)^(1/12)``, is complex, and so is every count after
    it, and a complex residual's magnitude would pass.  Zero outside cover, before ``t + 1``
    is read, so that nothing reads a month past ``t = proj_len()``.
    """
    if not is_active(t):
        return 0.0
    av = (av_at(t, BEF_PREM)                                         # noqa: F821
          + prem_to_av(t)
          + index_credits(t)
          - withdrawals(t)
          - wd_fees(t)
          - mth_deduction(t)
          + inv_income(t)
          - claims_from_av(t, DEATH)                                 # noqa: F821
          - claims_from_av(t, LAPSE))                                # noqa: F821
    nxt = av_at(t + 1, BEF_PREM)                                     # noqa: F821
    return float((nxt - av) / max(abs(nxt), abs(av), 10.0))


def check_seg_ladder():
    """Check the segment ladder bookkeeping.

    Returns ``True`` when, for every month of the frame, all four of the following hold:

    * at most ``seg_term_mth`` segments are live (:func:`check_seg_count_resid`);
    * every segment that matured accounted for its creation balance exactly,
      ``seg_new_pp(m) == seg_bal_pp(t - 1, 11) + deductions + withdrawals`` -- nothing
      may appear in or vanish from a segment except a deduction, a withdrawal or a loan
      transfer, because segments earn no interim interest
      (:func:`check_seg_closure_resid`);
    * **every live segment balance is non-negative**, to within ``1e-8``
      (:func:`check_seg_bal_resid`);
    * **every index credit is non-negative**, to within ``1e-8``
      (:func:`check_seg_credit_resid`).

    The last two are the 0% floor of ``cr_k = max(f, min(c, p x r))`` [S2][R1] stated as
    an invariant.  The accounting identity above closes even on a negative balance, and
    :func:`seg_count` counts only positive ones, so without these two an over-sourced
    draw could take a segment below zero and pay a negative credit on it at maturity
    without any check firing -- see :func:`mth_deduction_from_seg_pp`.  ``IUL_US_S``'s
    tests and tolerances, each month's read from a residual cell; a residual that is not
    a number fails each test.  A segment born before the valuation date that matures in
    month 0 closes on its creation balance by construction, since that balance is its
    ladder row summed (:func:`seg_new_pp`).
    """
    for t in range(proj_len()):
        if not check_seg_count_resid(t) <= 0:
            return False
        if not check_seg_credit_resid(t) >= -1e-8:
            return False
        if not check_seg_bal_resid(t) >= -1e-8:
            return False
        if not abs(check_seg_closure_resid(t)) <= 1e-9:
            return False
    return True


def check_seg_count_resid(t):
    """The live segments beyond ``seg_term_mth`` at the end of month t: zero or below.

    ``seg_count(t) - seg_term_mth`` as a ``float``, which :func:`check_seg_ladder` holds to
    0 or below, ``IUL_US_S``'s ``seg_count(t) <= seg_term_mth``.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return float(seg_count(t) - seg_term_mth)                        # noqa: F821


def check_seg_credit_resid(t):
    """The index credit of month t per policy, held by the ladder check to -1e-8 or more.

    :func:`index_credit_pp`, which :func:`check_seg_ladder` holds to ``-1e-8`` or more,
    ``IUL_US_S``'s tolerance.  Zero outside cover, where no segment matures.
    """
    return index_credit_pp(t)


def check_seg_bal_resid(t):
    """The least live segment balance at the end of month t, or 0 where none is below.

    The smallest of 0 and the balances of the segments born in policy months
    ``max(0, duration_mth(t) - 11)`` to ``duration_mth(t)``, each read at its slot, which
    :func:`check_seg_ladder` holds to ``-1e-8`` or more, ``IUL_US_S``'s test of each
    balance.  A balance that is not a number, once met, is kept, so that the residual is
    not a number and the check fails, as ``IUL_US_S``'s does.  Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    low = 0.0
    for m in range(max(0, d - seg_term_mth + 1), d + 1):             # noqa: F821
        b = seg_bal_pp(t, d - m)
        if low == low and not b >= low:
            low = b
    return low


def check_seg_closure_resid(t):
    """The closure's relative residual for the segment maturing in month t; zero.

    The creation balance of the segment born in policy month ``duration_mth(t) - 12``,
    :func:`seg_new_pp`, less its balance at the end of month ``t - 1``, in slot 11, plus the
    deductions and the draws charged to it, over the larger of the two in magnitude and 10,
    a ``float``, as :func:`check_av_components_resid` is: ``math.isclose`` with
    ``IUL_US_S``'s tolerances.  In the first month on the books, :func:`t_entry`, a
    segment born before the valuation date is ladder slot 12, read from its row.  Zero
    where nothing matures and outside cover.
    """
    if not is_active(t):
        return 0.0
    m = duration_mth(t) - seg_term_mth                               # noqa: F821
    if m < 0:
        return 0.0
    k = seg_term_mth - 1                                             # noqa: F821
    if t > t_entry():
        closed = (seg_bal_pp(t - 1, k) + seg_ded_cum_pp(t - 1, k)
                  + seg_wd_cum_pp(t - 1, k))
    else:
        closed = (seg_bal_pp_init(seg_term_mth) + seg_ded_cum_pp_init(seg_term_mth)
                  + seg_wd_cum_pp_init(seg_term_mth))                # noqa: F821
    new = seg_new_pp(m)
    return float((new - closed) / max(abs(new), abs(closed), 10.0))


def check_margin():
    """Check the net cash flow against the expense and mortality margins.

    Returns ``True`` when, for every month of the frame::

        net_cf(t) == margin_expense(t) + margin_mortality(t)
                     + av_change(t) - inv_income(t) - index_credits(t)
                     + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)
                     + net_loan_cf(t)

    to within ``1e-9``, relative to the larger side and 10, as for
    :func:`check_av_components`; each month's residual is :func:`check_margin_resid`, and
    a residual that is not a number fails.  The terms after the two margins are what
    separates a *gross liability cash flow* model from ``CashValue_SE``, whose ``net_cf``
    already nets the change in account value and the investment income.
    ``index_credits`` joins ``inv_income`` because the indexed account's whole return
    arrives at maturity rather than monthly; the loan terms are the debt a surrender
    recovers out of the cash value, which is the whole loan while the cash value covers it
    and the cash value once the loan exceeds it, where :func:`ncsv_pp` pays nothing, and
    the advance itself.  ``IUL_US_S``'s identity takes the whole loan in every month, which
    holds while neither the :func:`csv_pp` nor the :func:`ncsv_pp` floor binds against a
    policy loan, so its check fails on its point 5, whose loan overruns the cash value
    from policy month 383, on a projection that is right; this model states the identity
    as ``UL_US_SEC``, ``VUL_US_SEC`` and ``ULSG_US_SEC`` do, and on every point whose loan
    stays within its cash value the two agree.
    """
    for t in range(proj_len()):
        if not abs(check_margin_resid(t)) <= 1e-9:
            return False
    return True


def check_margin_resid(t):
    """The margin identity's relative residual in month t; zero everywhere.

    ``net_cf(t)`` less the two margins, the change in account value, the interest and the
    index credits, the loan a surrender recovers and the net loan cash flow, that
    :func:`check_margin` sets out, over the larger of the two sides in magnitude and 10, a
    ``float``, as :func:`check_av_components_resid` is.  Zero outside cover, before
    :func:`av_change` would read ``t + 1``.
    """
    if not is_active(t):
        return 0.0
    rhs = (margin_expense(t) + margin_mortality(t)
           + av_change(t) - inv_income(t) - index_credits(t)
           + min(loan_bal_pp(t), csv_pp(t)) * pols_lapse(t)
           + net_loan_cf(t))
    lhs = net_cf(t)
    return float((lhs - rhs) / max(abs(lhs), abs(rhs), 10.0))


def result_cf():
    """Result table of cashflows, a DataFrame indexed by month ``t``.

    One row per month ``t = 0 .. proj_len() - 1`` from the valuation date, the same month
    for every model point, so the frames of a block line up and sum row by row, and a
    point issued after the valuation date has zeros until its issue month;
    ``len(result_cf()) == proj_len()``.  The columns are ``IUL_US_S``'s.  ``pols_if`` is
    the number in force at the **start** of month ``t`` and is the weight on that same
    row's cash flows.  The cash flow columns are income-positive and sum to ``net_cf``:
    ``premiums - claims_death - claims_lapse - withdrawals - expenses - premium_taxes
    + net_loan_cf``.  The surrender column is ``claims_lapse``, matching the ``LAPSE``
    kind that produces it, and withdrawals are their own column because they are not
    claims.
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
            "net_loan_cf": [net_loan_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, a DataFrame indexed by ``t``.

    One row per month ``t = 0 .. proj_len() - 1``, as in :func:`result_cf`.  First the
    counts :func:`result_cf` weights its rows by, and how they move, as
    ``basiclife.BasicTerm_SE``'s ``result_pols`` sets them out: ``pols_if``, the count of
    month t; ``pols_new_biz``, the part of it issued in month t; then month t's deaths
    and lapses, in ``IUL_US_S``'s order, and its maturities, which are always zero.  Row
    by row, ``pols_if`` at ``t + 1`` is ``pols_if`` less the two outflows of month t,
    plus the new business of month ``t + 1``.  Then ``IUL_US_S``'s two monthly decrement
    rates, which are 0 outside cover, where the model reads no rate.
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

    The columns follow the notes' processing order: opening account value, net
    premium, the index credit of any maturing segment, the account value before the
    deduction, the death benefit, the net amount at risk, the cost of insurance, the
    monthly deduction, the post-deduction balance, the interest credited, the closing
    account value, and then the surrender and loan values.  One row per month
    ``t = 0 .. proj_len() - 1`` from the valuation date, as in :func:`result_cf`;
    ``av_pp_bef_prem`` on row ``t`` is the opening balance and ``av_pp`` the closing one.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_prem": [av_pp_at(t, BEF_PREM) for t in ts],   # noqa: F821
            "prem_to_av_pp": [prem_to_av_pp(t) for t in ts],
            "index_credit_pp": [index_credit_pp(t) for t in ts],
            "av_pp_bef_fee": [av_pp_at(t, BEF_FEE) for t in ts],     # noqa: F821
            "db_pp": [db_pp(t) for t in ts],
            "net_amt_at_risk": [net_amt_at_risk(t) for t in ts],
            "coi_pp": [coi_pp(t) for t in ts],
            "mth_deduction_pp": [mth_deduction_pp(t) for t in ts],
            "av_pp_bef_inv": [av_pp_at(t, BEF_INV) for t in ts],     # noqa: F821
            "inv_income_pp": [inv_income_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "ncsv_pp": [ncsv_pp(t) for t in ts],
            "loan_bal_pp": [loan_bal_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_seg():
    """Result table of the indexed segment ladder, a DataFrame indexed by ``t``.

    The index level, the fixed (holding) account, the sweep that creates this month's
    segment, the total and count of live segments, the credit paid by the segment
    maturing this month and the return that produced it (0 in a policy's first twelve
    policy months, when nothing can mature yet).  One row per month
    ``t = 0 .. proj_len() - 1`` from the valuation date, as in :func:`result_cf`.  The
    index level is the path on the valuation clock, :func:`index_level`, which on a point
    in force differs from ``IUL_US_S``'s by a constant factor; every other column is a
    ratio of levels or an amount, and moves with the segments, not with the path.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "index_level": [index_level(t) for t in ts],
            "fa_pp": [fa_pp(t) for t in ts],
            "sweep_pp": [sweep_pp(t) for t in ts],
            "seg_bal_tot_pp": [seg_bal_tot_pp(t) for t in ts],
            "seg_count": [seg_count(t) for t in ts],
            "index_credit_pp": [index_credit_pp(t) for t in ts],
            "seg_return": [seg_return(t) for t in ts],
            "lca_pp": [lca_pp(t) for t in ts],
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

BEF_CREDIT = 4

BEF_WD = 5

BEF_FEE = 6

BEF_SWEEP = 7

BEF_INV = 8

EOM = 9

DEATH = 0

LAPSE = 1

MATURITY = 2

WITHDRAWAL = 3

CURRENT = 0

GUARANTEED = 1

REMAINING = 0

ADJ_BEGIN = 1

issue_age_min = 0

issue_age_max = 85

basis = 0

maturity_age = 121

omega_age = 120

charges_cease_age = 121

guar_rate_ann = 0.01

fixed_rate_curr = 0.045

index_cap_curr = 0.1

index_cap_guar = 0.02

index_par = 1.0

index_floor = 0.0

index_return_ann = 0.064

index_level_init = 4500.0

seg_term_mth = 12

seg_credit_base_conv = 0

load_prem_rate_guar = 0.08

expense_pol_mth = 10.0

expense_pol_mth_guar = 15.0

expense_unit_mth_1 = 0.3

expense_unit_mth_2 = 0.0

expense_unit_mth_guar = 0.4

expense_unit_step_year = 10

coi_curr_factor = 0.65

loan_rate_ann = 0.03

loan_credit_rate_ann_1 = 0.02

loan_credit_rate_ann_2 = 0.03

loan_credit_step_year = 10

wd_fee = 25.0

prem_persistency_rate = 0.98

mort_ae_factor = 1.0

lapse_shock_mult = 2.0

lapse_dyn_slope = 3.0

lapse_dyn_cap = 2.0

lapse_dyn_floor = 0.5

lapse_rate_cap = 1.0

nlg_shock_lapse = 0.25

expense_acq = 150.0

expense_maint = 75.0

inflation_rate = 0.0

premium_tax_rate = 0.02

pd = ("Module", "pandas")