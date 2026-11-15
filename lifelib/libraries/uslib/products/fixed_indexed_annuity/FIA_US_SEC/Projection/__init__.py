# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of :mod:`~.FIA_US_SEC`.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.FIA_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is:
``Projection[0]`` is an ItemSpace projecting the table's first row, model point 1, the
worked example's anchor cell in force at anniversary 7, and :func:`point_id` is its
label::

    >>> Projection[0].result_cf()          # one row per month from the valuation date
    >>> Projection[0].result_cf_annual()   # the same, summed into contract years
    >>> Projection[0].point_id()           # 1, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, and an int set on a float Reference reads as a float
(``products/fixed_indexed_annuity/model-sec.md``, *What it refuses*).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.FIA_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``, on the chassis
:mod:`.MYGA_US_SEC` compiled first. A formula of :mod:`~.FIA_US_S` is rewritten where it
depends on where the projection starts, where it must answer for a month outside cover,
where it passed a policy month as ``t``, where it compared a phase or a switch as text, or
where it reads a table or text the compiled model holds as numbers; every other is
:mod:`~.FIA_US_S`'s own.
``products/fixed_indexed_annuity/model-sec.md`` lists the rewritten cells with the
reason for each.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/fixed_indexed_annuity/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FIA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers and the filename References live on the sibling :mod:`~.FIA_US_SEC.Data`
Space, reached here through the ``data`` Reference, so each file is read once per model
rather than once per model point. Five assumption tables are the files
:mod:`~.FIA_US_S` reads, read in place; the model point table and the rate scenarios are
this model's own, generated from :mod:`~.FIA_US_S` and its inputs. The projection reads
each table as ``Data`` holds it in arrays, built from the table checked, its keys read by
value, and through one cell of its own:

=========================  ================================  ==========================
Reference (on Data)        Arrays the projection reads       File
=========================  ================================  ==========================
model_point_file           data.premium() and the vectors    model_point_table_sec.csv
mort_table_file            data.mort_table_array()           mort_table.csv
surr_charge_file           data.surr_charge_rate_array(),    surr_charge_table.csv
                           data.vest_rate_array()
rollup_file                data.rollup_rate_array()          rollup_table.csv
payout_rate_file           data.payout_rate_array()          payout_rate_table.csv
rate_scenario_file         data.index_level_array(),         rate_scenario_sec.csv
                           data.mva_ref_yield_array()
withdrawal_file            data.wd_amount_array()            withdrawal_table.csv
=========================  ================================  ==========================

The model point's attributes are each one element of a ``Data`` vector, read by an
accessor of the column's name, ``premium_pp`` reading ``data.premium()[idx]``;
:func:`model_point`, the whole row, is for a reader. :func:`mort_rate_base_at`,
:func:`surr_charge_rate_py` with :func:`vest_rate_py`, :func:`rollup_rate_py`,
:func:`payout_rate_at`, :func:`scenario_value` and :func:`wd_scheduled_at` are the
tables' readers, in that order, each keyed by an age, a contract year, a count of years
or an anniversary rather than by the month, and called by a monthly cell in cover only.
The mortality, the rollup schedule, the scenario and the withdrawal programme are read at
the row ``Data`` numbers the point's ``sex``, ``rollup_id``, ``scenario_id`` or
``wd_schedule_id`` by, :func:`mort_schedule`, :func:`rollup_number`,
:func:`scenario_number` or :func:`wd_schedule_number` (``Data``'s docstring, *The
vectors*).

.. rubric:: Projection basis

Monthly steps on two clocks. ``t`` counts months from the **valuation date**, 0-based,
the clock ``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every
model point, however old the contract, month ``t`` runs from time ``t`` to time
``t + 1``, and the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len` counts
the months from the valuation date to the end of cover,
``maturity_mth() - duration_mth_init()``. Row ``t`` is the same month for every point,
so the frames of a block line up and sum row by row.

``duration_mth(t)`` counts **policy months**, the months the contract has been in force
at time ``t``: ``duration_mth(t) = duration_mth_init() + t``, where
:func:`duration_mth_init` is read from the model point — positive for a contract in
force at the valuation date, in any month of its contract year, 0 for one issued at it,
``-k`` for one issued ``k`` months later, at most ten years later. It is
:mod:`~.FIA_US_S`'s ``t``, the notes' month index, and everything contractual reads it:
``duration(t) = duration_mth(t) // 12`` is the completed contract years at the start of
month ``t``, the contractual label is ``policy_year(t) = duration(t) + 1``, and the
anniversary month, where every annual event lands, is the one with
``duration_mth(t) % 12 == 11``. The grid matches :mod:`.MYGA_US_S`, :mod:`.Term_US_S` and
the rest of the library, and it is what the product assignment table records for this
product.

Two inputs read the valuation clock instead. The **rate scenario** — the index level and
the MVA reference yield — is a path in calendar time, shared by every point of a block,
so the ``t`` of *rate_scenario_sec.csv* is a valuation month; each anniversary's level is
read at the valuation month that anniversary falls in, through :func:`scenario_value`,
and the level at the anniversary that opened the year under way, where that anniversary
precedes the valuation date, is the model point's :func:`index_level_prev_anniv_init`.
And **expense inflation**, ``inflation_factor(t) = (1 + inflation_rate) ** (t / 12)``,
keeps :mod:`~.FIA_US_S`'s formula on ``t``, so maintenance expense is in valuation-date
dollars for every point alike. The surrender charge, the vesting, the rollup schedule, the
growth window, the shock-lapse year, the MVA term, the withdrawal programme, the payout
bands and the mortality stay on the policy clock, read at the contract year, the elapsed
year count or the age. On a point issued at ``t = 0`` the two clocks coincide, and the
model computes what :mod:`~.FIA_US_S` computes.

**The monthly grid does not make the product monthly.** The technical notes make the
anniversary the single event date — "All transactions occur **at** the anniversary and are
processed as the last events of the contract year ending there" **[std]** — and that is
still true here: every contractual event is an annual event landing in the **anniversary
month**, ``is_anniv(t)``, the last month of each contract year. What the finer grid buys is
everything that is *not* a contractual event: mortality and surrender now fall in the month
they happen rather than all at the anniversary, the Model #805 floor and the fixed account
accrue month by month so a mid-year death or surrender is valued on the balance it actually
has, and maintenance expense accrues where it is incurred. Because the monthly decrement
rates compound to the annual ones and every contractual step still happens once a year,
**every state value at an anniversary is identical to the annual grid's** — account value,
benefit base, rollup base, lifetime withdrawal, Model #805 floor, phase and ``pols_if`` in
the month opening each contract year. What changes is the timing and the weighting of the
cash, which is the point.

Three vocabulary cells carry the split, and the whole model is written in terms of them:
:func:`duration` for anything keyed by contract year, :func:`is_anniv` for anything that
happens once a year, and :func:`year_open_mth` for the month whose closing value opens the
contract year — because on a monthly grid the previous *month* is no longer the previous
*year*, and reaching for ``t - 1`` where a year is meant is the mistake this conversion
exists to prevent. :func:`year_open_mth` and :func:`anniv_mth` are months of the frame,
on the valuation clock, computed from ``duration_mth(t) % 12``.

``age(t) = age_at_entry() + duration(t)`` is the attained age **opening the contract year**
of month ``t``, so mortality over that year reads ``age(t)`` itself — the library
convention of :mod:`.Term_US_S` and :mod:`.MYGA_US_S`. Age changes on the anniversary, not
on the birthday and not monthly. The transactions at the closing anniversary are one year
older, and that age is :func:`exercise_age`, ``covered_age(t) + 1``: it is what reads the
lifetime-withdrawal percentage table and what clears the contractual minimum exercise age.

**There is no issue-instant row.** The single premium, the premium bonus and the
acquisition expense are beginning-of-month flows of the issue month, the one with
``duration_mth(t) = 0``, :func:`t_entry` on a point issued at or after the valuation
date, alongside that month's own activity, and the issue values are credited there by
:mod:`~.FIA_US_S`'s rules: ``P x (1 + b)`` to the account value through
:func:`prem_to_av_pp`, its fixed share to the fixed account, and 87.5% of the premium,
the bonus excluded, to the Model #805 floor through :func:`prem_to_mgsv_pp`; the benefit
base and the rollup base open the first contract year at ``P`` under the rider. A model
point may instead be in force at the valuation date, in any month of its contract year,
on the opening state its row carries, per contract, as the contract stands at the start of
month 0, before any month-0 event: the account value, the fixed account, the benefit
base, the rollup base, the lifetime withdrawal, the Model #805 floor and the withdrawals
to date entering month 0; and, at the anniversary on or before the valuation date, the
account value and the fixed account, the phase as a code, the locked payout percentage and
the index level. Each is exactly what :mod:`~.FIA_US_S` carries into the month the point
is valued at. Every recursion opens at :func:`t_entry`: a monthly balance on its ``_init``
column, 0 on new business, and a quantity of the year — the opening account value and
fixed account, the benefit base, the rollup base, the lifetime withdrawal, the phase and
the locked percentage — is read at the anniversary that opened the year three ways: from
the frame where that anniversary is at or after :func:`t_entry`, from the model point's
``_prev_anniv_init`` or ``_init`` column where the year opened before the valuation date,
and by the issue rule in the first year of a contract issued at or after it. The rider
state opening the year has no column: it is read from the frame, or from ``glwb_elected()``
where that anniversary precedes :func:`t_entry`, a contract in force with the rider elected
having it alive (:func:`rider_in_force_open`). ``result_cf()`` has exactly ``proj_len()``
rows, ``t = 0 .. proj_len() - 1``.

The anniversary's eight processing steps are the notes' own, all eight still annual and all
eight landing in the anniversary month, and each intermediate value is reachable through a
``timing`` argument rather than being buried inside one formula:

1. index credit and fixed interest --- :func:`index_credit_pp`,
   :func:`fixed_interest_ann_pp`
2. rider charge on the **opening** benefit base --- :func:`rider_charge_pp`
3. benefit base: rollup, stack, step-up --- :func:`rollup_pp`, :func:`stack_pp`
4. lifetime and excess withdrawal --- :func:`lw_pp_at`, :func:`wd_pp`
5. charges on the excess and the proportional reduction --- :func:`wd_reduction_rate`
6. guaranteed minimum value roll --- :func:`mgsv_pp`
7. phase transition including the depletion test --- :func:`phase`
8. decrements --- :func:`pols_if_at` at ``AFT_DECR``

Steps 1--3 are skipped in ``DEPLETED``, steps 1--7 in ``TERMINATED``. Step 8 is the one
that is **not** annual: it runs every month, on :func:`mort_rate_mth` and
:func:`lapse_rate_mth`. Steps 1 and 6 keep a monthly component — the fixed account accrues
at ``(1 + i_F)^(1/12) - 1`` and the Model #805 floor at ``(1 + i_nf)^(1/12)`` — while their
annual figures, :func:`fixed_interest_ann_pp` and the anniversary deduction, stay whole.

Between anniversaries the contract is quiet: no withdrawal, no rider charge, no index
credit, no rollup and no step-up. The indexed account is therefore **flat between
anniversaries**, because the annual point-to-point segment locks only at maturity and "the
credit ... cannot be lost to later declines" [S1] is a statement about a credit that has
not yet been earned. That is the sourced rule "withdrawals are not credited with index
interest in the year they are taken" [S1] carried to mid-year deaths and surrenders
**[std]**; crediting a part year would be the *daily interim value* variant the notes
exclude.

Outside cover, before issue and from :func:`proj_len` on, every count, cash flow,
balance and rate is 0.0, every flag is ``False``, the phase is ``PRE_ISSUE`` before issue
and ``MATURED`` after cover, and :func:`lapse_moneyness_factor` is 1.0, no adjustment;
:func:`is_active` is the test, made before any table is read. One read reaches ahead of
the month: :func:`lapse_rate` reads the phase, and :func:`lapse_moneyness_factor` the
account value and the benefit base, at the anniversary closing the contract year,
:func:`anniv_mth`, up to 11 months later and inside the frame, a state that depends on
no count and on nothing after that anniversary.

.. rubric:: Naming

Cell names follow :mod:`.MYGA_US_S` — the deferred annuity chassis this
product sits on — and through it lifelib's ``basiclife.BasicTerm_S`` and
``savings.CashValue_SE``: ``pols_*`` for policy counts, ``av_*`` for account values,
plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-contract amounts,
``*_at(t, timing)`` for a quantity read at a point inside the anniversary. What running in
force adds is named as ``basiclife.BasicTerm_SE`` names it: ``duration_mth`` read from the
model point, ``policy_count``, ``pols_new_biz``, ``pols_if_at`` with its ``BEF_NB``
timing, ``is_active`` and ``result_pols``. ``duration_mth_init``, the policy months
completed at the valuation date, takes ``UL_US_S``'s name, and ``t_entry`` and
``maturity_mth`` are :mod:`.MYGA_US_SEC`'s. A column of the opening state is the cell it
opens with ``_init`` added, ``av_pp_init`` for :func:`av_pp`; a balance at the anniversary
on or before the valuation date adds ``_prev_anniv_init`` instead,
``av_pp_prev_anniv_init``. A reader keyed by a contract year is ``<cell>_py`` and one keyed
by an age or a year count ``<cell>_at``, as in :mod:`.MYGA_US_SEC`, and a cell that reads
the anniversary opening the year is ``<cell>_year_open``, as :mod:`~.FIA_US_S`'s
``av_pp_year_open``. The ``is_*`` cells decode the model point's text columns, read in
``Data``, and the three switches, int codes here, into the flags the projection branches
on, so that no cell compares text and none calls a label accessor (``credit_method``,
``glwb_basis``, ``scenario_id``, ...), which is left to reporting. :mod:`~.FIA_US_S`'s
timing, kind and scenario column strings are int codes, named as the strings (*Codes*,
below). The technical notes use compact actuarial symbols instead.
The notes' month index is this model's ``duration_mth(t)``, so the notes' ``t`` in the
left-hand column is ``duration_mth(t)`` throughout. The mapping is:

========================  ==================================  ==============================
Notes symbol              Cells                               Meaning
========================  ==================================  ==============================
t                         duration_mth(t)                     The notes' month index:
                                                              completed policy months at the
                                                              start of month t
(valuation month)         (the projection index)              Months from the valuation
                                                              date, 0-based
(elapsed years)           duration(t)                         Completed contract years at
                                                              month t
(the anniversary month)   is_anniv(t)                         Last month of a contract year
(that month's index)      anniv_mth(t)                        Month closing t's contract
                                                              year, valuation clock
(year-opening month)      year_open_mth(t)                    Month whose close opened it,
                                                              valuation clock
(contract year)           policy_year(t)                      Contract year containing t;
                                                              duration + 1
x                         age_at_entry                        Issue age (ANB)
x + duration(t)           age(t)                              Attained age opening month t's
                                                              contract year
(younger covered life)    covered_age(t)                      Younger covered age opening
                                                              that year
x + duration(t) + 1       exercise_age(t)                     Covered age at the closing
                                                              anniversary
(none)                    policy_term                         Contract years from issue to
                                                              maturity_age
(cover from issue)        maturity_mth                        Policy month cover ends; 12 x
                                                              policy_term
(none)                    proj_len                            Months from the valuation date
                                                              to the end of cover
(months at t = 0)         duration_mth_init                   Completed policy months at the
                                                              valuation date; -k if issued
                                                              k months later
(first month on books)    t_entry                             max(0, -duration_mth_init)
(in cover)                is_active(t)                        Whether month t is inside
                                                              cover
(contracts)               policy_count                        Contracts the model point
                                                              stands for
(the point's label)       point_id                            Its point_id, from Data; the
                                                              Space is keyed by idx
(the joins on text keys)  mort_schedule,                      The row Data numbers the
                          rollup_number,                      point's sex, rollup_id,
                          scenario_number,                    scenario_id and wd_schedule_id
                          wd_schedule_number                  by, in their arrays
av_initial                av_pp_init                          AV entering month 0; 0 on new
                                                              business
(F entering month 0)      av_fixed_pp_init                    Fixed account entering month 0
AV(0) at entry            av_pp_prev_anniv_init               AV at the anniversary on or
                                                              before the valuation date
F(0) at entry             av_fixed_pp_prev_anniv_init         F at that anniversary
bb_initial                benefit_base_pp_init                BB entering month 0
mgv_initial               mgsv_pp_init                        MGV entering month 0
(RB at entry)             rollup_base_pp_init                 RB entering month 0
(LW at entry)             lw_pp_init                          LW entering month 0, 0 before
                                                              exercise
(pi at entry)             payout_rate_locked_prev_anniv_init  Payout percentage locked at
                                                              that anniversary
(phase at entry)          phase_prev_anniv_init               Phase code at that anniversary
I(y) at entry             index_level_prev_anniv_init         Index level at that
                                                              anniversary
Wcum at entry             wd_cum_pp_init                      Withdrawals from issue to the
                                                              valuation date
P                         premium_pp                          Single premium
b                         bonus_rate                          Premium bonus rate (7% [S5])
b/(1+b)                   bonus_factor                        Clawback factor -- **not** b
                                                              [S10]
v(t)                      vest_rate(t)                        Vested bonus percentage [S5]
v(y)                      vest_rate_py(y)                     The same, by contract year
(allocation)              alloc_indexed / alloc_fixed         Account allocation at issue
I(y)                      index_level(y)                      Index level at **anniversary
                                                              number** y
(the level by month)      scenario_value(y, name)             Scenario level at anniversary
                                                              y's valuation month
R(t)                      index_return(t)                     I(y+1)/I(y) - 1 over month t's
                                                              year
c                         cap_rate                            Declared annual cap (5.25%
                                                              [S2])
c_min                     cap_rate_min                        Guaranteed minimum cap (0.25%
                                                              [S4])
c(t)                      cap_rate_in_force()                 Cap actually applied
f                         floor_rate                          Index credit floor (0%)
p, s, d                   par_rate, spread_rate,              Participation rate [R1];
                          trigger_rate                        spread and trigger, levels
                                                              **[std]**
(crediting method)        is_credit_cap,                      The crediting method, decoded
                          is_credit_par,
                          is_credit_par_cap,
                          is_credit_spread,
                          is_credit_trigger
cr(t)                     credit_rate(t)                      Credit rate for month t's
                                                              contract year
(cr on a return)          credit_rate_on(r, method)           The crediting engine itself
IC(t)                     index_credit_pp(t)                  Index credit, in the
                                                              anniversary month
FI(t) monthly             fixed_interest_pp(t)                Fixed account interest for
                                                              month t
FI(t) annual              fixed_interest_ann_pp(t)            The contract year's, for the
                                                              stack
i_F, i_F,min              fixed_rate, fixed_rate_min          Declared / guaranteed fixed
                                                              rate
kappa                     av_int_factor                       Share of IC reaching the AV
                                                              [S3]
(IC x kappa + FI)         inv_income_pp(t)                    Interest credited to the AV
A(t)                      av_indexed_pp(t)                    Indexed account balance
F(t)                      av_fixed_pp(t)                      Fixed account balance
AV(t)                     av_pp(t)                            Account value closing month t
AV(0), AV(1), AV(2)       av_pp_at(t, timing)                 BEF_INV / BEF_FEE / BEF_WD;
                                                              EOY is AV(t); BEF_PREM opens
                                                              the month
AV(0) of the year         av_pp_year_open(t)                  Balance opening month t's
                                                              contract year
F(0), A(0) of the year    av_fixed_pp_year_open(t),           The fixed and indexed
                          av_indexed_pp_year_open(t)          openings: the credit base and
                                                              the fixed-interest base
(premium credited)        prem_to_av_pp(t)                    P x (1 + b), in the issue
                                                              month
l(t) x AV(t)              av_at(t, timing)                    In-force weighted account
                                                              value
(AV shortfall)            av_depletion_pp(t)                  Withdrawal the AV could not
                                                              fund
phi                       rider_charge_rate                   Rider charge rate (0.95% [S9])
Phi(t)                    rider_charge_pp(t)                  Rider charge amount
BB(t)                     benefit_base_pp(t)                  GLWB benefit base, closing
BB(3), BB(4)              benefit_base_pp_at(t, timing)       BEF_ROLLUP / BEF_STEP_UP /
                                                              BEF_WD / EOY
RB(t)                     rollup_base_pp(t)                   Rollup base
RB(0) of the year         rollup_base_pp_year_open(t)         Rollup base opening the year
(RB on a withdrawal)      is_rb_pro_rata,                     rb_wd_convention, decoded
                          is_rb_dollar
g(t)                      rollup_rate(t)                      Guaranteed simple rollup rate
                                                              [S2]
g(y)                      rollup_rate_py(y)                   The same, by contract year
rollup(t)                 rollup_pp(t)                        Rollup dollar increment
m                         stack_factor                        Stacking factor (1.50
                                                              [S8][S9])
stack(t)                  stack_pp(t)                         Stacking credit
T_g                       in_growth_period(t)                 Benefit base still growing
(the step-up)             step_up_applies(t)                  Whether the ratchet is tested
(step-up mode)            is_step_up_annual,                  step_up_mode, decoded
                          is_step_up_at_exercise
LW(t)                     lw_pp(t)                            Lifetime withdrawal amount,
                                                              closing
LW before/after step 5    lw_pp_at(t, timing)                 BEF_WD / EOY
pi(a, basis)              payout_rate(a, basis)               Payout percentage by age band
                                                              [S3]
pi(a)                     payout_rate_at(a)                   The same, on the point's basis
(the basis)               is_single_basis,                    glwb_basis, decoded
                          is_joint_basis
(pi locked at exercise)   payout_rate_locked(t)               The percentage actually in
                                                              force
h(a)                      activation_rate(a)                  Activation incidence, reported
                                                              only
G(t)                      wd_pp(t)                            Gross withdrawal requested
(scheduled G)             wd_scheduled_pp(t)                  Ad hoc withdrawal at the
                                                              anniversary
(G by year count)         wd_scheduled_at(k)                  The same, by elapsed contract
                                                              year
min(G, LW)                wd_guar_pp(t)                       Guaranteed portion
E(t)                      wd_excess_pp(t)                     Excess above the guaranteed
                                                              amount
(unpayable withdrawal)    wd_unfunded_pp(t)                   Requested but neither funded
                                                              nor guaranteed, on TERMINATED
(guaranteed part paid)    wd_guar_paid_pp(t)                  min(G, LW) less its share of
                                                              it
(excess portion paid)     wd_excess_paid_pp(t)                E(t) less its share of it
FW(t)                     free_wd_allow(t)                    Free withdrawal amount
0.10 x AV(0)(t)           free_wd_base(t)                     Base of the free amount
(FW consumed)             wd_free_pp(t)                       Free-allowance portion of the
                                                              withdrawal
(FW remaining)            free_wd_remain(t)                   Free amount left for the
                                                              excess
X(t) on a withdrawal      wd_charge_base_pp(t)                Amount exposed to charge and
                                                              MVA
X(t) on a surrender       surr_charge_base_pp(t)              Same, at a full surrender
sc(t)                     surr_charge_rate(t)                 Surrender charge percentage
                                                              [S5]
sc(y)                     surr_charge_rate_py(y)              The same, by contract year
SC(t) on a withdrawal     wd_charge_pp(t)                     Surrender charge on the excess
SC(t) on a surrender      surr_charge_pp(t)                   Surrender charge on a
                                                              surrender
CB(t) on a withdrawal     wd_clawback_pp(t)                   Non-vested bonus recovery
CB(t) on a surrender      surr_clawback_pp(t)                 Same, at a full surrender
MVA(t) on a withdrawal    wd_mva_pp(t)                        Collared MVA on the excess
MVA(t) on a surrender     mva_pp(t)                           Collared MVA on a surrender
(the collar's basis)      is_collar_gross                     mva_collar_basis, decoded
                          is_collar_surrender_value
(the MVA rate)            mva_rate(t)                         [(1+i0)/(1+it)]^(n/12) - 1
                                                              [S10]
i0                        mva_ref_yield_at_issue              Reference index at issue
i_y                       mva_ref_yield(y)                    Reference index at
                                                              **anniversary number** y
n/12                      mva_term(t)                         Years left in the MVA period
(MVA applies at all)      mva_in_force(t)                     Inside the MVA period
rho(t)                    wd_reduction_rate(t)                Proportional reduction factor
Wcum(t)                   wd_cum_pp(t)                        Cumulative gross withdrawals
G - SC - CB + MVA         wd_payment_pp(t)                    Cash paid on the withdrawal
(SV before the floor)     surr_value_pp(t)                    AV - SC - CB + MVA
CSV(t)                    surr_benefit_pp(t)                  Surrender benefit paid
MGV(t)                    mgsv_pp(t)                          Model #805 guaranteed minimum
(0.875 x P)               prem_to_mgsv_pp(t)                  The floor's issue value, in
                                                              the issue month
i_nf                      mgsv_rate                           Nonforfeiture accumulation
                                                              rate
(the $50 charge)          mgsv_charge_pp(t)                   Annual contract charge, 0
                                                              **[std]**
(statutory i_nf)          mgsv_rate_statutory(...)            Model #805 4B/4C indexed rate
phase(t)                  phase(t)                            Closing phase code, ACCUM ..
                                                              TERMINATED
(phase opening a year)    phase_year_open(t)                  Phase code at the anniversary
                                                              opening t's year
(phase during the year)   phase_open(t)                       Phase steps 1-7 are processed
                                                              under
(first exercise)          is_exercise(t)                      The first lifetime withdrawal
rider_in_force(t)         rider_in_force(t)                   Rider still alive closing
                                                              month t [S9]
rider_in_force(k-1)       rider_in_force_open(t)              Rider alive opening the
                                                              contract year
depletion_cause(t)        depletion_cause(t)                  Excess / charge / negative MVA
                                                              flag
q(t)                      mort_rate(t)                        Annual mortality of month t's
                                                              contract year, capped at 1
q at age a                mort_rate_base_at(a)                The table's rate at age a
1 - (1-q)^(1/12)          mort_rate_mth(t)                    The monthly rate actually
                                                              applied
(A/E deviation)           mort_ae_factor                      Mortality A/E factor, 100%
                                                              **[std]**
w(t)                      lapse_rate(t)                       Annual surrender rate of that
                                                              year
1 - (1-w)^(1/12)          lapse_rate_mth(t)                   The monthly rate actually
                                                              applied
w_base(t)                 lapse_rate_base(t)                  Base surrender table
w_shock                   shock_lapse_rate(t)                 33% / 10% / 5% by rider state
                                                              [R8]
M_money(t)                lapse_moneyness_factor(t)           Moneyness suppression
                                                              **[std]**
l(k), opening a year      pols_if(t)                          In force opening month t,
                                                              after its new business
(closing the month)       pols_if_at(t, AFT_DECR)             In force at the end of month t
l(0)                      pols_if_init                        In force at the valuation
                                                              date; 0 for new business
(new business)            pols_new_biz(t)                     Contracts issued in month t
(the five readings)       pols_if_at(t, timing)               BEF_NB / BEF_DECR / BEF_MORT /
                                                              BEF_LAPSE / AFT_DECR
l q_m                     pols_death(t)                       Deaths in the month
l (1-q_m) w_m             pols_lapse(t)                       Full surrenders in the month
(none)                    pols_maturity(t)                    Survivors at the horizon
P on new business         premiums(t)                         Premium income, in the issue
                                                              month
(premium credited)        prem_to_av(t)                       The same, in-force weighted
min(G, LW) x l(t)         wd_guar(t)                          Guaranteed withdrawal outgo,
                                                              paid
(E - SC - CB + MVA) l(t)  wd_excess(t)                        Excess withdrawal outgo, paid
LW while DEPLETED         income_payments(t)                  Post-depletion income outgo
(all three together)      withdrawals(t)                      Total withdrawal outgo
(ledger benefit lines)    claims(t, kind)                     Benefit outgo by kind
(benefit per contract)    claim_pp(t, kind)                   Benefit per contract by kind
(AV released)             claims_from_av(t, kind)             Account value released by a
                                                              claim
(paid above AV)           claims_over_av(t, kind)             Benefit paid above the account
                                                              value
(no separate commission)  commissions(t)                      Acquisition commission, 0
                                                              **[std]**
(80/12) x 1.025^(t/12)    expenses(t)                         Monthly maintenance, valuation
                                                              clock, plus 0.06 P on issue
1.025^(t/12)              inflation_factor(t)                 Expense inflation, valuation
                                                              clock
premium tax               premium_taxes(t)                    Premium tax, 0% **[std]**
NetCF(t)                  net_cf(t)                           Net cash flow for the month
(the annual summary)      result_cf_annual()                  result_cf() summed into
                                                              contract years
(none)                    result_pols()                       The counts behind result_cf
(the model point)         model_point()                       The point's row of the table
========================  ==================================  ==============================

Six names needed care.

**pols_if(t) is the notes' l(k) in the month opening each contract year.** Across this
library ``pols_if(t)`` is the number in force at the **start** of ``t`` and is the weight
carried by that same row's cash flows — :mod:`.Term_US_S` has ``pols_if(0)`` the count
issued and ``savings.CashValue_SE`` has ``pols_if(t)`` equal to
``pols_if_at(t, "BEF_MAT")``. Here it is ``pols_if_at(t, BEF_DECR)``, the count carried
in plus the month's new business, before the month's decrements. The notes define
``l(k)`` as the in-force probability at the *end* of contract year ``k``, which is
anniversary ``k``, which is where contract year ``k + 1`` opens: on the monthly grid that
is the month with ``duration_mth(t) = 12k``, so ``pols_if`` there is ``l(k)``, and in the
issue month of a contract issued at or after the valuation date it is ``l(0)``, its
``policy_count``. Because the monthly rates compound to the annual ones this equality is
exact, not approximate.

**The one place the finer grid changes an answer rather than its resolution** is the weight
on the anniversary's own cash. A withdrawal, a rider charge or a surrender charge falls in
the anniversary month and is weighted by ``pols_if`` there — the contracts that actually
*reach* the anniversary — where the annual grid weighted it by ``l(k)``, the contracts that
entered the year. The second is an approximation the annual grid could not avoid: it pays a
full year's guaranteed withdrawal to a contract that died in month three. The
reconciliation the convention buys is unchanged, and now holds row by row on the finer
grid: the ``pols_if`` column of :func:`result_cf` is the divisor of the cash flows on its
own row — ``result_cf()["wd_guar"][t] / wd_guar_paid_pp(t)`` is ``pols_if(t)``.

**MGV is MGSV.** The Model #805 floor is called ``MGV`` in these notes, after [S10], and
``MGSV`` in ``products/fixed_deferred_annuity/``, after its own specimen. Both source
files say in terms that this is **one quantity under two labels** and must not be modeled
as two. The chassis name :func:`mgsv_pp` is used here, so the two annuity models share it.
The *recursion*, however, is **not** the chassis's: this product accretes and then deducts,
``MGV(t) = max(0, MGV(t-1) x (1 + i_nf) - G(t))``, while the chassis deducts and then
accretes, ``MGSV(t) = [MGSV(t-1) - d(t) - c(t)] x g``. The worked example pins the FIA
ordering — ``93,811.84 x 1.01 - 10,144.16 = 84,605.80`` — and the chassis notes explicitly
warn against carrying their recursions across unexamined. Same name, same concept,
different arithmetic, on purpose.

**E(t) is not the chassis's E(t).** On the chassis ``E(t)`` is the amount exposed to the
surrender charge and the MVA, and is named ``wd_excess_pp`` / ``surr_excess_pp``. Here
``E(t)`` is the notes' **excess withdrawal** — the part of a gross withdrawal above the
guaranteed lifetime amount, the quantity that permanently reduces the guarantee and, at
exhaustion, destroys it. That is the product's headline concept and it keeps the name
:func:`wd_excess_pp`. The chargeable amount, the notes' ``X(t)``, becomes
:func:`wd_charge_base_pp` on the withdrawal path and :func:`surr_charge_base_pp` on the
surrender path. Reading a chassis formula across without renaming would silently charge a
surrender charge on the wrong base.

**age(t) opens the contract year; exercise_age(t) closes it.**
``age(t) = age_at_entry() + duration(t)`` is the attained age at the anniversary that opens
month ``t``'s contract year, exactly as in :mod:`.Term_US_S` and :mod:`.MYGA_US_S`, and
:func:`mort_rate` reads it directly — the annual rate it returns is then converted for the
month by :func:`mort_rate_mth`. Every transaction, however, falls at the **closing**
anniversary, one year older, and the payout percentage depends on that age: the anchor
cell's first lifetime withdrawal, in contract year 8 from an issue age of 62, is taken at
attained age 70 and reads ``pi(70, single) = 5.20%``. :func:`exercise_age` carries that age
— ``covered_age(t) + 1`` — so the ``+ 1`` is named once rather than spelled at each use.

**M_shock is absorbed into lapse_rate_base.** The notes write
``w(t) = min(0.35, w_base(t) x M_shock(t) x M_money(t))`` but state the shock as three
*absolute* rates (33% / 10% / 5%) rather than as multipliers on the 6% ultimate. Carrying
``M_shock`` as a separate factor would require inventing a denominator, so
:func:`lapse_rate_base` returns :func:`shock_lapse_rate` in the shock year and
:func:`lapse_rate` multiplies only by :func:`lapse_moneyness_factor`. The name
``shock_lapse_rate`` follows :mod:`.Term_US_S` — but the **timing does not**, and the
contrast is worth stating. There the notes put the shock "in full at the end of the final
level-period month", a contractual date, so :mod:`.Term_US_S` drops the whole shock in that
one month. Here the notes state it as the surrender rate *of contract year 11*, a year that
carries no surrender charge in any of its months, so there is no date inside the year for
the decision to cluster on and :func:`lapse_rate_mth` spreads it like any other annual
rate. The one surrender that is not spread is the deemed full surrender at termination,
which is a contractual event and lands whole on the anniversary.

**d and c collide across the library.** ``d`` is the performance-trigger rate in these
notes, deaths in :mod:`.Term_US_S` and the floor's withdrawal deduction on the chassis;
``c`` is the declared cap here and the floor's contract charge on the chassis. The names
``trigger_rate``, :func:`pols_death`, :func:`mgsv_charge_pp` and :func:`cap_rate`
keep the four apart.

One name is reused deliberately and reads across cleanly. :func:`credit_rate` is the
chassis's declared effective annual rate ``i_cr(t)`` and here the index credit rate
``cr(t) = max(f, min(c, R(t)))``. Different formulas, but the same concept — the rate at
which interest is credited for the contract year — so the name is kept rather than split.

.. rubric:: Timing arguments

Account value, following ``CashValue_SE``'s ``av_pp_at`` and named for the processing step
each precedes:

``BEF_PREM``
    the balance carried into month ``t`` **before** the single premium: at
    :func:`t_entry`, :func:`av_pp_init`, the account value of a contract in force at the
    valuation date and zero on new business, and ``AV(t-1)`` after it. It exists so that
    the account-value roll-forward closes on the issue month too, the premium being a
    beginning-of-month flow rather than a row of its own.
``BEF_INV``
    the balance opening month ``t`` after the premium: ``BEF_PREM`` plus
    :func:`prem_to_av_pp`, which is ``P x (1 + b)`` in the issue month and zero in every
    other. In an anniversary month this is the notes' ``AV(0)`` only when the fixed
    allocation is zero; in general the notes' ``AV(0)`` of the contract year is
    :func:`av_pp_year_open`, eleven months earlier.
``BEF_FEE``
    ``AV(1)``, after the month's interest — the fixed accrual every month, plus the index
    credit in an anniversary month — and before the rider charge.
``BEF_WD``
    ``AV(2)``, after the rider charge, before the withdrawal. **Not floored at zero** —
    the 0% floor is on the index *credit*, not on the account value [S7].
``EOY``
    ``AV(t)``, after the withdrawal, floored at zero. Equal to :func:`av_pp`.

**Away from an anniversary the last three coincide**, at the opening balance plus the
month's fixed accrual, because no contractual transaction falls there.

Benefit base, named for the same steps: ``BEF_ROLLUP`` is the base opening the **contract
year**, ``BEF_STEP_UP`` is ``BB(3)`` after rollup and stack, ``BEF_WD`` is ``BB(4)``
after the annual step-up, and ``EOY`` is ``BB(t)`` after the proportional reduction. All
four steps are annual, so away from an anniversary every timing returns the opening base.
Lifetime withdrawal: ``BEF_WD`` is the amount payable at the contract year's anniversary,
``EOY`` the closing value after the same reduction; away from an anniversary both carry
the amount set at the last one, which is the income in force.

Policy counts, following the chassis and ``basiclife.BasicTerm_SE``: ``BEF_NB`` is the
count carried in from month ``t - 1``, before month ``t``'s new business, which is
:func:`pols_if_init` at :func:`t_entry`; ``BEF_DECR`` adds :func:`pols_new_biz` and
therefore equals :func:`pols_if` itself; ``BEF_MORT`` is the same (this product has no
annuitization decrement); ``BEF_LAPSE`` is after that month's deaths; and ``AFT_DECR``
is the closing count, which is also ``pols_if_at(t + 1, BEF_NB)`` in every month but
the last covered one. Both decrements are the **monthly** rates. ``BEF_NB`` is the one
timing running in force adds; ``basiclife.BasicTerm_SE``'s ``"BEF_MAT"`` is not adopted,
since the survivors leave at the end of the last covered month, as the S goldens have it.

Benefit ``kind`` arguments are ``DEATH``, ``LAPSE`` and ``MATURITY``, and ``ALL`` for the
total of :func:`claims` and :func:`claims_over_av`. Any other value of any of these raises
``ValueError``.

.. rubric:: The four phases, and why the cause of depletion matters

``ACCUM`` is deferral. ``INCOME`` starts at the first lifetime withdrawal and lasts while
an account value remains. ``DEPLETED`` is what the product is sold for: the account value
is gone, the insurer pays ``LW`` from its own funds for the rest of the covered life, no
rider charge is deducted, no index credit is computed, the surrender value and the death
benefit are zero, and **lapse is impossible**, so :func:`lapse_rate` returns zero and
``l(t+1) = l(t)(1 - q_m(t))``. ``TERMINATED`` is the same exhaustion with the guarantee
destroyed — reached when the account value is driven to zero by an excess withdrawal, a
surrender charge or a negative MVA rather than by guaranteed withdrawals and rider charges
[S1][S5][S9]. :func:`depletion_cause` carries the attribution and is evaluated *before*
the depletion test, exactly as the notes require. A model testing only ``AV <= 0`` would
either give the guarantee away after an excess withdrawal or destroy it after a legitimate
one. When the contract terminates, the survivors leave as a deemed full surrender —
:func:`lapse_rate` returns 1.0 for that contract year, and :func:`lapse_rate_mth` puts the
whole of it in the anniversary month rather than spreading it, because the contract "as
well as the rider will be considered Surrendered" [S5] on that date — so the in-force
roll-forward still closes.

The transition itself is annual and is tested only at the anniversary, which costs nothing:
the account value can reach zero only where a withdrawal or a charge is taken, and both
fall there. Between anniversaries :func:`phase` simply carries :func:`phase_open`.

Each phase is an int code, named by a Reference of the phase's name: ``ACCUM`` 1,
``INCOME`` 2, ``DEPLETED`` 3 and ``TERMINATED`` 4, so that every comparison of a phase is
a comparison of numbers. Two more codes answer outside cover: ``PRE_ISSUE`` 0 before
issue and ``MATURED`` 5 from :func:`proj_len` on, which no cell in cover reads.
:func:`result_glwb`, a report, decodes the codes back into the labels, and the model point
carries the phase at the anniversary on or before the valuation date as its code,
:func:`phase_prev_anniv_init`. ``Data`` refuses ``TERMINATED`` in force, a deemed
surrender of every contract.

**The asymmetry reaches the cash, not only the phase label.** On the exhaustion
anniversary itself the withdrawal requested exceeds what the account value can meet. In
``DEPLETED`` the insurer funds the whole shortfall, because that is the guarantee. On the
``TERMINATED`` branch it funds none of it: the balance is gone and the rider that would
have covered the rest is destroyed by the very withdrawal being paid, and [S5] treats the
contract as surrendered at that point. :func:`wd_unfunded_pp` is that unpayable part, and
:func:`wd_payment_pp`, :func:`wd_guar` and :func:`wd_excess` are all net of it. The cap is
on the *payment* only — :func:`wd_pp` still carries the amount requested, so the excess
still sets :func:`depletion_cause`, still drives ``rho`` to 1 and still takes the benefit
base to zero.

.. rubric:: pols_maturity and the projection horizon

The technical notes state no projection horizon; the ``DEPLETED`` liability is a life
annuity, so the model runs through the final month of the contract year *entered* at
attained age ``maturity_age`` = 120 **[std]**, the terminal age of the shipped mortality
table — policy month :func:`maturity_mth` ``= 12 * policy_term()``, which is
``proj_len() = maturity_mth() - duration_mth_init()`` months from the valuation date. The
survivors of the last covered month, ``duration_mth(t) = maturity_mth() - 1``, which is
``t = proj_len() - 1``, leave through :func:`pols_maturity`, zero at every other ``t``,
so that::

    pols_if(t) - pols_if_at(t + 1, BEF_NB) = pols_death(t) + pols_lapse(t)
                                               + pols_maturity(t)

holds for every ``t`` — the start-of-month count opens the row, the exits are taken
during it and the next month opens on what is left, before its own new business —
including the last, where ``pols_if_at(proj_len(), BEF_NB)`` is zero. Under the shipped
table ``q`` reaches 1.000000 at age 120, hence a monthly rate of 1.0 in the first month of
that contract year, so the projection closes itself and the term is numerically zero; it
is kept because a substituted table with no terminal age would make it bite, and because
without it the last month would appear to lose lives with no cause. The name follows
``BasicTerm_S.pols_maturity`` and the construction follows :mod:`.Term_US_S`.

.. rubric:: Codes

What :mod:`~.FIA_US_S` spells as text, a timing, a kind, a scenario column or a switch's
setting, is here an int Reference named as the text it replaces, so that every cell takes
and returns C numbers. A call site reads as it did, less the quotes:
``pols_if_at(t, BEF_DECR)``, ``av_pp_at(t, BEF_WD)``, ``claims(t, DEATH)``.

===============  =====  =============================================================
Reference        Value  Meaning
===============  =====  =============================================================
BEF_NB           0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR         1      :func:`pols_if_at`: that count plus month t's new business
BEF_MORT         2      :func:`pols_if_at`: the same instant, before the deaths
BEF_LAPSE        3      :func:`pols_if_at`: after deaths
AFT_DECR         4      :func:`pols_if_at`: after surrenders, the notes' l(t)
BEF_PREM         5      the account value cells: before the single premium
BEF_INV          6      the account value cells: after it, before the month's interest
BEF_FEE          7      the account value cells: after the interest, before the fee
BEF_WD           8      the account value, benefit base and withdrawal cells: before the
                        withdrawal
EOY              9      the same cells: closing the month
BEF_ROLLUP       10     :func:`benefit_base_pp_at`: the base opening the contract year
BEF_STEP_UP      11     :func:`benefit_base_pp_at`: after rollup and stack
DEATH            0      the claim cells: the death claim
LAPSE            1      the claim cells: the surrender claim
MATURITY         2      the claim cells: the survivors at the horizon
ALL              3      :func:`claims`, :func:`claims_over_av`: the three kinds' total
INDEX_LEVEL      0      :func:`scenario_value`: the ``index_level`` column
MVA_REF_YIELD    1      :func:`scenario_value`: the ``mva_ref_yield`` column
ANNUAL           0      ``step_up_mode``: the step-up tested every anniversary
AT_EXERCISE      1      ``step_up_mode``: at the first exercise only
PRO_RATA         0      ``rb_wd_convention``: the rollup base reduced pro rata
DOLLAR           1      ``rb_wd_convention``: reduced dollar for dollar
GROSS            0      ``mva_collar_basis``: the collar on the gross withdrawal
SURRENDER_VALUE  1      ``mva_collar_basis``: on the account value
===============  =====  =============================================================

The model has three families of timing, the count's, the account value's and the benefit
base's, passed to different cells, and they are numbered as one: ``BEF_NB`` 0 and
``BEF_DECR`` 1, as in every SEC model, then the count's others, then the account value's,
then the benefit base's own two, each family in the order of its instants. The benefit
base and the lifetime withdrawal share ``BEF_WD`` and ``EOY`` with the account value,
where :mod:`~.FIA_US_S` spells them alike, so each is one Reference. ``BEF_MORT`` keeps a
code of its own, though :func:`pols_if_at` reads it at ``BEF_DECR``'s instant, so that
each string is one code. So a code of one family passed to another's cell,
``av_pp_at(t, BEF_NB)``, is refused as any timing the cell does not take is,
``ValueError("invalid timing")``, in both engines, rather than read as a timing of the
cell's own. Kinds are numbered in ``result_cf``'s order, which is the order
:mod:`~.FIA_US_S` adds them in its total, and ``ALL``, its ``kind=None``, after them; the
claim cells but :func:`claims` and :func:`claims_over_av` refuse it, ``ValueError("invalid
kind")``, :func:`claim_pp` outside a ``DEPLETED`` month, where it answers 0.0 before it
reads the kind, as :mod:`~.FIA_US_S`'s does. A code a cell takes indexes that cell's cache,
a C array of twelve codes a month for each of the thirteen cells that take a timing or a
kind, and twelve an anniversary for :func:`scenario_value`, since every 2-D cache of the
model has one width (``spec_sec.py``), so codes are numbered densely from 0, and a code a
cell does not take but below 12 is refused inside the cache. The three switches,
``step_up_mode``, ``rb_wd_convention`` and ``mva_collar_basis``, hold a code, ``ANNUAL``,
``PRO_RATA`` and ``GROSS`` as shipped, and are read through their decodes; a text set on
one is no code, and the cell that asks raises :mod:`~.FIA_US_S`'s message, ``invalid
step_up_mode`` among them. Codes are References, not cells, so the symbol map does not
list them. Every other Reference is named in lower case, ``issue_age_min`` and
``issue_age_max`` among them, the product's issue ages, 40 and 80, the first of which,
with ``maturity_age``, the compiled model's caches are sized from (:func:`proj_len`).

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`policy_id`, :func:`sex`,
:func:`tax_status`, :func:`glwb_basis`, :func:`credit_method`, :func:`rollup_id`,
:func:`scenario_id` and :func:`wd_schedule_id`, the reports :func:`result_cf`,
:func:`result_pols`, :func:`result_av`, :func:`result_glwb` and :func:`result_cf_annual`,
and the checks :func:`check_av_roll_fwd` and :func:`check_pols_roll_fwd` are written for a
reader and for the comparison with :mod:`~.FIA_US_S`, which has every one of them: a table
row, text, DataFrames and two verdicts. No other cell calls them: each reads the number
``Data`` decoded from the same column instead, the decodes' flags and the rows the keys
select. So the row, the text and the frames stay Python when the model compiles. A label
accessor returns its column as read, text or not: ``Data`` accepts, and the model
projects, a point whose ``policy_id`` or ``tax_status`` is blank or a number, which no
cell reads, whose ``glwb_basis`` or ``credit_method`` is, which its decodes answer False
to, or whose ``sex``, ``rollup_id``, ``scenario_id`` or ``wd_schedule_id`` is a number,
where its table's keys are numbers, and the compiled accessor returns what modelx
returns, NaN or an int. Every other cell returns a C ``bint``, ``long long`` or
``double``, and so do the two checks, which may stay Python but compile to a ``bint``,
their verdict, as their per-month residuals, ``*_resid``, compile to a ``double``.

Four cells of float or text parameters compile with C signatures and dict caches, their
bodies Python, the engine cells :func:`credit_rate_on`, :func:`payout_rate`,
:func:`mgsv_rate_statutory` and :func:`mgsv_rate_is_compliant`: :mod:`~.FIA_US_S`'s own,
``math`` and its walk of the payout bands included, kept for its tests, for T1, which
compares them at the arguments :mod:`~.FIA_US_S`'s tests use, and for a reader. No
projection cell calls them, and a cell keyed by a float or a text compiles with a Python
dict for a cache, so the registry admits them by name. The three others of
:mod:`~.FIA_US_S`'s float-parameter cells, ``bonus_clawback_on``, ``mva_pp_on`` and
``wd_reduction_rate_on``, which the projection does call, are written inline in the cells
that call them: :func:`wd_clawback_pp` and :func:`surr_clawback_pp`, :func:`wd_mva_pp`
and :func:`mva_pp`, and :func:`wd_reduction_rate`.
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
    cell (the Space docstring's *Reporting cells*), which no projection cell reads. Each
    accessor reads its own ``Data`` vector instead.
    """
    return data.model_point_table().iloc[idx]                        # noqa: F821


def point_id():
    """The label of the selected model point, its ``point_id``, from ``Data.point_id``.

    ``Projection`` is indexed by position, ``idx``, as ``basiclife.BasicTerm_SC`` is; the
    label is what a reader finds in the table, so every refusal names it.
    """
    return int(data.point_id()[idx])                                 # noqa: F821


def policy_id():
    """The contract identifier of the selected model point."""
    return model_point()["policy_id"]


def age_at_entry():
    """x: the issue age (ANB) of the selected model point.

    The age at issue, not at the valuation date: ``age(0)`` is the attained age then.
    """
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point, M or F."""
    return model_point()["sex"]


def mort_schedule():
    """The number ``Data`` gives the point's ``sex``, by which its table is read.

    The row of ``Data.mort_table_array``. The join on the text key, made once in
    ``Data`` (R7), where ``FIA_US_S``'s reader selects its rows by the key itself:
    :func:`mort_rate_base_at` reads the table at this number, so no projection cell
    compares the key or calls the label accessor.
    """
    return int(data.mort_schedule()[idx])                            # noqa: F821


def tax_status():
    """Tax status of the contract, NQ or Q.

    Reported only.  The base run is non-qualified **[std]**; no RMD module is
    implemented, though the notes make the RMD age a behavioural input through
    :func:`activation_rate` and the ``rmd_age`` Reference.
    """
    return model_point()["tax_status"]


def premium_pp():
    """P: the single premium per contract."""
    return float(data.premium()[idx])                                # noqa: F821


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the contracts in force then, before any
    month-0 event; any other point counts the contracts it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Every per-contract value — the
    account value, the benefit base, the lifetime withdrawal, the floor, the opening state —
    is the same whatever the count, and every cash flow is a per-contract amount weighted by
    it. ``FIA_US_S``'s ``pols_if_init`` column, renamed, as ``basiclife.BasicTerm_SE`` names
    it.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """l(0): contracts in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose contracts
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count. ``FIA_US_S``'s cell of the name is the count at its
    entry, 1 for a single-contract model point, whether entered at issue or in force.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def bonus_rate():
    """b: the premium bonus rate, 7% of the single premium [S5]."""
    return float(data.bonus_rate()[idx])                             # noqa: F821


def alloc_indexed():
    """The share of the account value allocated to the indexed account; 100% **[std]**."""
    return float(data.alloc_indexed()[idx])                          # noqa: F821


def alloc_fixed():
    """The share allocated to the fixed account, ``1 - alloc_indexed()``."""
    return 1.0 - alloc_indexed()


def glwb_elected():
    """Whether the GLWB rider is elected at issue [S5][S9][S11]."""
    return bool(data.glwb_elected()[idx])                            # noqa: F821


def glwb_basis():
    """``single`` or ``joint``.

    The joint column of the payout table is the single column less 0.50%, read on the
    younger covered person [S1][S3].  Joint-life *survivorship* is **not implemented**:
    the notes specify the joint payout percentage but no second-life mortality basis.

    A label for reporting: the projection reads the basis through its decodes,
    :func:`is_single_basis` and :func:`is_joint_basis`, and no projection cell calls this.
    """
    return model_point()["glwb_basis"]


def is_single_basis():
    """Whether the rider is on the single-life basis, ``glwb_basis`` ``single``.

    A decode of the model point's column, made in ``Data`` (``Data.is_single_basis``), as
    each ``is_*`` cell of a column is, so that the projection branches on a flag and no
    projection cell compares the column's text or calls the label accessor,
    :func:`glwb_basis`, which is left to reporting. :func:`payout_rate_at` reads it, for the
    single-life column of the payout bands.
    """
    return bool(data.is_single_basis()[idx])                         # noqa: F821


def is_joint_basis():
    """Whether the rider is on the joint-life basis, ``glwb_basis`` ``joint``.

    The other decode of the column (:func:`is_single_basis`). :func:`covered_age` reads it,
    for the younger covered life, and :func:`payout_rate_at` for the joint column. A basis
    that is neither is read as single by :func:`covered_age` and raises in
    :func:`payout_rate_at`, as ``FIA_US_S`` answers it in its ``covered_age`` and its
    :func:`payout_rate`.
    """
    return bool(data.is_joint_basis()[idx])                          # noqa: F821


def joint_age():
    """The issue age (ANB) of the joint covered person; the annuitant's own if blank.

    Decoded in ``Data`` (``Data.joint_age``), element by element, by ``FIA_US_S``'s rule: a
    blank reads :func:`age_at_entry`.
    """
    return int(data.joint_age()[idx])                                # noqa: F821


def income_start_age():
    """The attained age at which the base run takes its first lifetime withdrawal.

    The deterministic run activates here rather than on the ``h(a)`` incidence table,
    which the notes say clusters at the RMD age but which cannot be applied to a single
    deterministic cell; see :func:`activation_rate`.
    """
    return int(data.income_start_age()[idx])                         # noqa: F821


def utilization_intensity():
    """The fraction of ``LW`` actually withdrawn once income starts.

    1.00 in the base run **[std]**; the majority of users withdraw 95%-105% of the
    maximum [R1].  **The 1.05 case is an excess withdrawal** and routes through the
    proportional reduction of step 5, which is why efficiency and excess-withdrawal
    assumptions cannot be set independently.
    """
    return float(data.utilization_intensity()[idx])                  # noqa: F821


def credit_method():
    """The crediting method: ``cap``, ``par``, ``par_cap``, ``spread`` or ``trigger``.

    All five are implemented in :func:`credit_rate`, which branches on the decodes
    :func:`is_credit_cap` to :func:`is_credit_trigger`, and in :func:`credit_rate_on`, the
    engine ``FIA_US_S`` calls, kept for its tests. This accessor is a label for reporting:
    no projection cell calls it. The notes' sixth variant, monthly sum with a monthly cap,
    is **not implemented**: it needs a monthly grid, which the notes exclude, and its floor
    convention is itself flagged as ambiguous [S4][R1].
    """
    return model_point()["credit_method"]


def is_credit_cap():
    """Whether the indexed account credits ``max(f, min(c, R))``, ``credit_method`` ``cap``.

    A decode of the model point's column, made in ``Data`` (``Data.is_credit_cap``), as each
    ``is_*`` cell of a column is, so that :func:`credit_rate` branches on flags and no
    projection cell compares the column's text or calls :func:`credit_method`, which is left
    to reporting. The composite's baseline [S2][S4][S10][R1].
    """
    return bool(data.is_credit_cap()[idx])                           # noqa: F821


def is_credit_par():
    """Whether the indexed account credits ``max(f, p x R)``, ``credit_method`` ``par``.

    A decode of the column, as :func:`is_credit_cap` is [S4][S10][R1].
    """
    return bool(data.is_credit_par()[idx])                           # noqa: F821


def is_credit_par_cap():
    """Whether the account credits ``max(f, min(c, p x R))``, ``credit_method`` ``par_cap``.

    A decode of the column, as :func:`is_credit_cap` is; [R1]'s worked case.
    """
    return bool(data.is_credit_par_cap()[idx])                       # noqa: F821


def is_credit_spread():
    """Whether the account credits ``max(f, p x R - s)``, ``credit_method`` ``spread``.

    A decode of the column, as :func:`is_credit_cap` is; the index-margin form [R1][S8].
    """
    return bool(data.is_credit_spread()[idx])                        # noqa: F821


def is_credit_trigger():
    """Whether the account credits ``d`` when ``R >= 0`` and ``f`` otherwise, ``trigger``.

    The last decode of ``credit_method``, as :func:`is_credit_cap` is: a method that is none
    of the five raises in :func:`credit_rate`, as ``FIA_US_S``'s :func:`credit_rate_on`
    raises.
    """
    return bool(data.is_credit_trigger()[idx])                       # noqa: F821


def cap_rate():
    """c: the declared annual cap, 5.25% [S2].

    A non-guaranteed element captured as of 07/01/2022, revisable under ASOP No. 2
    [R6][REG-R26].  Holding it constant for forty years is a strong implicit assumption;
    re-declaration against the option budget is **not implemented** because the notes
    give the target but no option-pricing function.
    """
    return float(data.cap_rate()[idx])                               # noqa: F821


def stack_factor():
    """m: the stacking factor on realised dollar credits, 150% [S8][S9].

    Zero gives the pure-rollup design (a); with ``rollup_rate`` zero it gives the pure
    stacking design (b), where one carrier's 250% election credits 250% to the benefit
    base [S3][S4].
    """
    return float(data.stack_factor()[idx])                           # noqa: F821


def av_int_factor():
    """kappa: the share of the index credit that reaches the account value [S3][S4].

    1.00 on the blended baseline.  0.50 is the 250% election documented at one carrier,
    which credits 250% of index interest to the benefit base but only 50% to the account
    value, deliberately starving the account value.  The stacking factor ``m`` applies to
    the **gross** index credit, not to ``kappa x IC``.
    """
    return float(data.av_int_factor()[idx])                          # noqa: F821


def rollup_id():
    """The guaranteed rollup schedule, a key into *rollup_table.csv*."""
    return model_point()["rollup_id"]


def rollup_number():
    """The number ``Data`` gives the point's ``rollup_id``, by which its table is read.

    The row of ``Data.rollup_rate_array``. The join on the text key, made once in
    ``Data`` (R7), where ``FIA_US_S``'s reader selects its rows by the key itself:
    :func:`rollup_rate_py` reads the table at this number, so no projection cell
    compares the key or calls the label accessor.
    """
    return int(data.rollup_number()[idx])                            # noqa: F821


def mva_ref_yield_at_issue():
    """i0: the MVA reference index level locked at issue, 3.00% **[std]**."""
    return float(data.mva_ref_yield_at_issue()[idx])                 # noqa: F821


def scenario_id():
    """The index and reference-yield scenario, a key into *rate_scenario_sec.csv*.

    The row's own copy of a ``FIA_US_S`` scenario on the valuation clock: ``FIA_US_S``'s id
    on a contract issued at the valuation date, ``{id}-M{d}`` on one valued in force at
    policy month ``d`` and ``{id}-F{k}`` on one issued ``k`` months after the valuation date
    (``Data.rate_scenario``). A label for reporting: :func:`scenario_value`, the scenario's
    one reader, reads the scenario at :func:`scenario_number`, the number ``Data`` joins
    the column to, and no projection cell calls this.
    """
    return model_point()["scenario_id"]


def scenario_number():
    """The number ``Data`` gives the point's ``scenario_id``, by which its table is read.

    The row of ``Data.index_level_array`` and ``Data.mva_ref_yield_array``. The join on
    the text key, made once in ``Data`` (R7), where ``FIA_US_S``'s reader selects its
    rows by the key itself: :func:`scenario_value` reads the table at this number, so no
    projection cell compares the key or calls the label accessor.
    """
    return int(data.scenario_number()[idx])                          # noqa: F821


def wd_schedule_id():
    """The ad hoc withdrawal programme, a key into *withdrawal_table.csv*."""
    return model_point()["wd_schedule_id"]


def wd_schedule_number():
    """The number ``Data`` gives the point's ``wd_schedule_id``, by which its table is read.

    The row of ``Data.wd_amount_array``. The join on the text key, made once in ``Data``
    (R7), where ``FIA_US_S``'s reader selects its rows by the key itself:
    :func:`wd_scheduled_at` reads the table at this number, so no projection cell
    compares the key or calls the label accessor.
    """
    return int(data.wd_schedule_number()[idx])                       # noqa: F821


def av_pp_init():
    """AV entering month 0: the account value of a contract in force at the valuation date.

    The model point's ``av_pp_init`` column, ``FIA_US_S``'s ``av_initial``, per contract, at
    the start of month 0, before any month-0 event; 0 on a contract issued at or after the
    valuation date, which opens with no account value. ``FIA_US_S``'s cell computes the
    issue value ``P x (1 + b)`` [S5] when its column is blank; here that rule credits the
    issue month, through :func:`prem_to_av_pp`. The bonus is credited to the **account
    value** at issue and earns index credits from day one [S5]; it does **not** enter the
    benefit base [S9] or the nonforfeiture base [S10].
    """
    return float(data.av_pp_init()[idx])                             # noqa: F821


def av_fixed_pp_init():
    """F entering month 0: the fixed account within :func:`av_pp_init`, a column of its own.

    The model point's ``av_fixed_pp_init`` column, per contract; 0 on a contract issued at
    or after the valuation date, whose fixed share of the premium and bonus,
    ``alloc_fixed() x P x (1 + b)``, is credited in the issue month. ``FIA_US_S`` derives
    the fixed account at entry as ``alloc_fixed() x AV``, the split at issue, which holds at
    issue only: the fixed account accrues its own interest month by month and takes the
    rider charge first, so after issue the two accounts drift from that split, and a
    contract re-entered in force from its own state needs the fixed account it actually
    holds.
    """
    return float(data.av_fixed_pp_init()[idx])                       # noqa: F821


def av_pp_prev_anniv_init():
    """AV(0) of the year under way: the account value at the anniversary on or before the
    valuation date.

    The model point's ``av_pp_prev_anniv_init`` column, per contract: the account value at
    the anniversary that opened the contract year under way at the valuation date, the base
    of that year's index credit, through its indexed part, and of its free withdrawal
    allowance. :func:`av_pp_year_open` reads it wherever the year under way opened before
    the first month on the books, on a contract valued in force, mid-year or on its
    anniversary. On a contract valued on an anniversary the two instants are one, and
    ``Data`` holds it equal to :func:`av_pp_init`; in the first policy year it is the issue
    value, ``P x (1 + b)``, which ``Data`` holds to a cent. 0 on a contract not yet in
    force.
    """
    return float(data.av_pp_prev_anniv_init()[idx])                  # noqa: F821


def av_fixed_pp_prev_anniv_init():
    """F(0) of the year under way: the fixed account at the anniversary on or before the
    valuation date.

    The model point's ``av_fixed_pp_prev_anniv_init`` column, per contract, read by
    :func:`av_fixed_pp_year_open` as :func:`av_pp_prev_anniv_init` is by
    :func:`av_pp_year_open`: the base of the year's annual fixed interest, which the stack
    reads, and the part of the account value outside the year's index segment. ``Data``
    holds it equal to :func:`av_fixed_pp_init` on an anniversary, to the issue value's fixed
    share in the first policy year, and, off an anniversary, the indexed account,
    ``av_pp_init - av_fixed_pp_init``, equal to its value at the anniversary, since that
    account moves only there. 0 on a contract not yet in force.
    """
    return float(data.av_fixed_pp_prev_anniv_init()[idx])            # noqa: F821


def benefit_base_pp_init():
    """BB entering month 0: the benefit base of a contract in force at the valuation date.

    The model point's ``benefit_base_pp_init`` column, ``FIA_US_S``'s ``bb_initial``, per
    contract. The base is flat between anniversaries, so it is also the base at the
    anniversary on or before the valuation date, which that year's rollup and stack build on
    and its rider charge is taken on. 0 without the rider, and 0 on a contract issued at or
    after the valuation date, whose issue base, ``P`` — the bonus stays out [S9] — opens its
    first contract year in :func:`benefit_base_pp_at`.
    """
    return float(data.benefit_base_pp_init()[idx])                   # noqa: F821


def rollup_base_pp_init():
    """RB entering month 0: the rollup base of a contract in force at the valuation date.

    The model point's ``rollup_base_pp_init`` column, ``FIA_US_S``'s ``rb_initial``, per
    contract, flat between anniversaries like the benefit base, so it is also the base the
    year's rollup is computed on. 0 without the rider, and 0 on a contract issued at or
    after the valuation date, whose issue value, ``P`` under the rider [S2][S9], opens its
    first contract year in :func:`rollup_base_pp_year_open`.
    """
    return float(data.rollup_base_pp_init()[idx])                    # noqa: F821


def mgsv_pp_init():
    """MGV entering month 0: the Model #805 floor of a contract in force.

    The model point's ``mgsv_pp_init`` column, ``FIA_US_S``'s ``mgv_initial``, per contract;
    0 on a contract issued at or after the valuation date. ``FIA_US_S``'s cell computes the
    issue value, 87.5% of the single premium **excluding the bonus** [S10][R2], when its
    column is blank; here that rule credits the issue month, through
    :func:`prem_to_mgsv_pp`. The worked example's ``93,811.84 = 87,500 x 1.01^7`` is that
    value rolled forward seven years.
    """
    return float(data.mgsv_pp_init()[idx])                           # noqa: F821


def lw_pp_init():
    """LW entering month 0: the lifetime withdrawal amount of a contract in force.

    The model point's ``lw_pp_init`` column, ``FIA_US_S``'s ``lw_initial``, per contract, 0
    before exercise. Flat between anniversaries, so it is also the amount set at the
    anniversary on or before the valuation date, the income in force, which
    :func:`lw_pp_at` carries until the next anniversary. 0 on a contract issued at or after
    the valuation date.
    """
    return float(data.lw_pp_init()[idx])                             # noqa: F821


def payout_rate_locked_prev_anniv_init():
    """The payout percentage locked at the anniversary on or before the valuation date.

    The model point's column, ``FIA_US_S``'s ``payout_rate_initial``: the percentage locked
    at the first lifetime withdrawal, 0 before it, which :func:`payout_rate_locked` carries
    where the contract year under way opened before the valuation date. ``Data`` holds it to
    0 in ``ACCUM``, and in ``INCOME`` and ``DEPLETED`` to 0 exactly where
    :func:`lw_pp_init` is 0: a contract that exercised below the first age band, or in a
    band at 0%, locked 0. 0 on a contract not yet in force.
    """
    return float(data.payout_rate_locked_prev_anniv_init()[idx])     # noqa: F821


def phase_prev_anniv_init():
    """The phase at the anniversary on or before the valuation date, as a code.

    The model point's column, ``FIA_US_S``'s ``phase_initial`` as an int: 1 ``ACCUM``, 2
    ``INCOME`` or 3 ``DEPLETED`` on a contract in force, 0 on one not yet in force.
    ``TERMINATED``, 4, is a deemed surrender of every contract, so ``Data`` refuses it in
    force. :func:`phase_year_open` reads it where the contract year under way opened before
    the valuation date: the phase that year's annual steps are processed under, unless the
    year is the exercise year. ``FIA_US_S`` reads its column as text.
    """
    return int(data.phase_prev_anniv_init()[idx])                    # noqa: F821


def index_level_prev_anniv_init():
    """I(y) of the year under way: the index level at the anniversary on or before the
    valuation date.

    The model point's column: the level at which the contract year's index segment started,
    the base of its point-to-point credit. Once that anniversary precedes the valuation date
    it is history, which the scenario, on the valuation clock, cannot give, so
    :func:`index_level` reads it for that anniversary alone, on a contract valued mid-year.
    On a contract valued on an anniversary the scenario sets the level at ``t = 0``, and
    ``Data`` holds this equal to it. 0 on a contract not yet in force.
    """
    return float(data.index_level_prev_anniv_init()[idx])            # noqa: F821


def wd_cum_pp_init():
    """Wcum entering month 0: the gross withdrawals from issue to the valuation date.

    The model point's column, per contract, which :func:`wd_cum_pp` opens on. 0 on a
    contract not yet in force, and in the first policy year, before the first anniversary's
    withdrawal. ``FIA_US_S`` counts its running total from the month it enters a contract,
    from 0.
    """
    return float(data.wd_cum_pp_init()[idx])                         # noqa: F821


def policy_term():
    """Contract term in years **[std]**: through the year entered at ``maturity_age``.

    ``maturity_age`` = 120 is the terminal age of the mortality basis, where the annual
    rate is 1.000000, so the projection closes itself rather than being truncated: the
    last contract year is the one *entered* at that age, hence the ``+ 1``.  The notes
    state no horizon, and the ``DEPLETED`` liability is a life annuity, so stopping
    earlier would silently drop the tail the product is sold for.
    """
    return maturity_age - age_at_entry() + 1                         # noqa: F821


def maturity_mth():
    """The policy month at which cover ends: ``12 * policy_term()``.

    The first policy month past the contract year entered at attained age ``maturity_age`` =
    120 **[std]**, so the last covered month is ``maturity_mth() - 1``, 707 at issue age 62.
    It is ``FIA_US_S``'s ``proj_len()``, its frame from issue on the policy clock;
    :func:`proj_len` counts from the valuation date instead.
    """
    return 12 * policy_term()


def proj_len():
    """The number of months from the valuation date to the end of cover.

    ``maturity_mth() - duration_mth_init()``: 708 for a contract issued at ``t = 0`` at
    issue age 62, 624 for the anchor in force at anniversary 7, 12 for a contract valued in
    its last policy year, at policy month 696, and 723 for one to be issued 15 months after
    the valuation date. The frame is ``t = 0, 1, ..., proj_len() - 1``; ``proj_len()`` is
    its exclusive end and the row count of :func:`result_cf`, and ``proj_len() - 1`` is the
    last covered month.

    It refuses, naming the point, in this order: a point issued below ``issue_age_min``, 40,
    the youngest issue age of the product, from which the compiled model's caches are sized
    (``spec_sec.py``); one issued above ``issue_age_max``, 80, the oldest, which sizes
    nothing but is the product's; a point whose cover from issue is empty, issued past
    ``maturity_age``, which would otherwise project a frame of zeros and never be issued,
    and which the ages refuse first unless ``issue_age_max`` is raised past it; a point at
    or past maturity at the valuation date, which has no frame and would otherwise project
    nothing: an in-force extract should not carry it; and a point whose sex's mortality
    stops below ``maturity_age``, the age the last contract year is entered at and the
    last :func:`mort_rate_base_at` reads (``Data.mort_age_lasts``), since ``Data``, which
    checks the age of the point's first month on the books, cannot read ``maturity_age``.
    Each bound is a Reference, set before the model computes anything.
    """
    if age_at_entry() < issue_age_min:
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is below "
                         f"issue_age_min, {issue_age_min}")
    if age_at_entry() > issue_age_max:
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is above "
                         f"issue_age_max, {issue_age_max}")
    if maturity_mth() <= 0:
        raise ValueError(f"point_id {point_id()}: age_at_entry {age_at_entry()} is past "
                         f"maturity_age {maturity_age}: the contract has no cover")
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(f"point_id {point_id()}: duration_mth {duration_mth_init()} "
                         f"is at or past maturity, policy month {maturity_mth()}")
    if data.mort_age_lasts()[mort_schedule()] < maturity_age:        # noqa: F821
        raise ValueError(f"point_id {point_id()}: the mortality table gives no rate at "
                         f"attained age {maturity_age}, the age the last contract year "
                         f"is entered at")
    return n


def policy_year(t):
    """The contract year month ``t`` falls in: ``duration(t) + 1``, the 1-based label.

    Derived from ``duration_mth(t)``, the policy clock, never indexed by; it is 0 or less
    before issue, where every reader is guarded by :func:`is_active`. It is the key that
    reads the surrender charge, the vesting vector and the rollup schedule, all of which the
    sources state by contract year, and it is the year whose annual decrement rates
    :func:`mort_rate` and :func:`lapse_rate` return.
    """
    return duration(t) + 1


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The contract's age in months at ``t = 0``: 84 for the anchor in force at anniversary 7,
    95 for it valued in the last month of contract year 8, 0 for a contract issued at the
    valuation date, and -15 for one to be issued 15 months after it, which ``Data`` admits
    up to ``future_horizon_mth`` months ahead. It is read as ``basiclife.BasicTerm_SE``
    reads it, as a whole number whatever the column's type, and is the one fact the policy
    clock takes from the model point. It replaces ``FIA_US_S``'s ``entry_year``, a count of
    whole years, which is why ``FIA_US_S`` can enter a contract in force on an anniversary
    only.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def duration_mth(t):
    """Completed policy months at the start of month ``t``, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together. A closed form, where
    ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers, without a
    call chain as long as the frame. Negative before issue. It is ``FIA_US_S``'s ``t``, the
    notes' month index, and everything contractual reads it, through :func:`duration`,
    :func:`policy_year`, :func:`is_anniv` and :func:`age`. ``FIA_US_S`` enters a contract in
    force by opening its frame late, at the policy month it has reached; here the frame
    opens at the valuation date and the policy clock starts where the contract stands.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued ``k``
    months later. It is the base of every recursion: :func:`pols_if_at` opens there from
    :func:`pols_if_init`; the account value, the fixed account, the Model #805 floor and the
    withdrawals to date from the model point's opening state; and the state of the year —
    the benefit base, the rollup base, the lifetime withdrawal, the phase, the locked
    percentage and the rider — reads the anniversary that opened the year from the frame
    only where that anniversary is at or after it, and from the opening state, or by the
    issue rule, where it is not. No cell in cover reads a month before it.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month ``t`` is inside cover: issued, and not past the last covered month.

    ``0 <= duration_mth(t) < maturity_mth()``. False before issue and from :func:`proj_len`
    on. Outside cover every count is zero, and so every cash flow; so is every value state
    and every contractual rate, every flag is ``False``, the phase is ``PRE_ISSUE`` or
    ``MATURED``, no count cell evaluates a rate there, and no table is read at a contract
    year or an attained age the contract does not have.
    """
    return 0 <= duration_mth(t) < maturity_mth()


def duration(t):
    """Completed contract years at the start of month ``t``, ``duration_mth(t) // 12``.

    Every contractual schedule in this product is annual, so this is what the attained
    age, the surrender charge, the vesting vector, the rollup schedule and the scenario
    tables are read at.
    """
    return duration_mth(t) // 12


def is_anniv(t):
    """True in the **last month of a contract year**, where every annual event lands.

    ``duration_mth(t) % 12 == 11``.  All eight of the notes' processing steps are
    contractually annual — the point-to-point index credit [S2][S4][S10], the rider charge
    [S9], the benefit base rollup, stack and step-up [S9], the lifetime withdrawal, the
    charges and the phase transition — so all eight happen here and nowhere else.  What
    the finer grid carries between anniversaries is the fixed-account accrual, the
    Model #805 roll, the decrements and the maintenance expense.
    """
    return duration_mth(t) % 12 == 11


def anniv_mth(t):
    """The month that **closes** the contract year of month ``t``, on the valuation clock.

    ``t + 11 - duration_mth(t) % 12``: the month of the frame whose policy month is the
    year's last, ``12 * duration(t) + 11``, which is ``FIA_US_S``'s ``anniv_mth`` and its
    ``t``; here the two clocks differ, so the month is counted from ``t``. Equal to ``t``
    itself when :func:`is_anniv` is true. It is where the annual quantities of that contract
    year are evaluated — which is what makes :func:`lapse_rate` a property of the year
    rather than of the month — and it lies at most 11 months after ``t``, inside the frame,
    since cover ends at the close of a contract year.
    """
    return t + 11 - duration_mth(t) % 12


def year_open_mth(t):
    """The month whose **closing** value opens the contract year of month ``t``.

    ``t - 1 - duration_mth(t) % 12``, on the valuation clock: the anniversary month that
    closed the previous contract year, policy month ``12 * duration(t) - 1``, which is
    ``FIA_US_S``'s ``year_open_mth``. It falls below :func:`t_entry` in the first contract
    year on the books — at ``t = -1`` or earlier on a contract valued in force, mid-year or
    on its anniversary, and before issue on new business — where the opening state stands
    in, the model point's ``_prev_anniv_init`` or ``_init`` column or the issue rule: which
    is the test every annual state cell makes.
    """
    return t - 1 - duration_mth(t) % 12


def age(t):
    """x + duration(t): the attained age (ANB) **opening** the contract year of month t.

    The library convention of :mod:`.Term_US_S` and :mod:`.MYGA_US_S`, so :func:`mort_rate`
    reads this age directly for the contract year of mortality it covers.  Age changes on
    the anniversary, not on the birthday and not monthly.  The transactions of that
    contract year fall at its *closing* anniversary and are one year older: that age is
    :func:`exercise_age`, which is what reads the lifetime withdrawal percentage table.
    """
    return age_at_entry() + duration(t)


def covered_age(t):
    """The attained age of the covered life opening the contract year of month t.

    The annuitant's own age on a single-life basis; the **younger** covered person's on a
    joint-life basis [S1][S3].  Timed like :func:`age`, at the opening anniversary; the
    payout percentage and the minimum exercise age are read at :func:`exercise_age`.

    It branches on :func:`is_joint_basis`, the decode of ``glwb_basis``.
    """
    if is_joint_basis():
        return min(age_at_entry(), joint_age()) + duration(t)
    return age(t)


def exercise_age(t):
    """``covered_age(t) + 1``: the covered age at the anniversary closing the contract year.

    All transactions occur **at** the anniversary and are processed as the last events of
    the contract year ending there **[std]**, so a lifetime withdrawal taken in the
    contract year of month ``t`` is taken one year older than the age opening it.  This is
    the age that reads the payout percentage band and that clears the contractual minimum
    exercise age of 50: the anchor cell's exercise in contract year 8, from issue age 62,
    is at attained age 70 and reads the 70-79 band.
    """
    return covered_age(t) + 1


def scenario_value(y, name):
    """The level of column ``name`` the model point's scenario sets at anniversary ``y``.

    **The argument is an anniversary number, from issue, not a month.** Callers pass
    ``duration(t)`` for the anniversary opening the contract year of month ``t`` and
    ``duration(t) + 1`` for the one closing it, as in ``FIA_US_S``. The scenario is on the
    valuation clock (``Data.rate_scenario``), so the anniversary is turned into the
    valuation month it falls in, ``m = 12 * y - duration_mth_init()``, here and nowhere
    else, and the level is the last row of the point's scenario at or before ``m``: each row
    holds from its month until the next row of the same scenario, so a flat path is one row.
    ``Data`` holds the scenarios step-filled by valuation month, ``index_level_array`` and
    ``mva_ref_yield_array``, at the row :func:`scenario_number` gives the point's
    ``scenario_id``, and ``name`` is the column's code, ``INDEX_LEVEL`` or
    ``MVA_REF_YIELD``; any other raises ``ValueError("invalid name")``.

    The arrays hold every month to ``Data.read_last_mth``, 1,093, the last a read reaches,
    the last row of a scenario holding to there; a month past it, which no projection
    reads, raises, naming the point, rather than reading a row the array does not hold.

    ``FIA_US_S`` reads an anniversary before the scenario's first row at the first row's
    level. Here a month with no row at or before it raises, naming the point
    (``Data.scenario_first_mths``): ``Data`` refuses a point whose scenario sets no level by
    its first month on the books, and no cell asks for an anniversary before that month —
    :func:`index_level` reads the one before the valuation date from the model point — so
    the raise is the guard behind that refusal.
    """
    m = 12 * y - duration_mth_init()
    s = scenario_number()
    if m < data.scenario_first_mths()[s]:                            # noqa: F821
        raise ValueError(f"point_id {point_id()}: scenario sets no level by month {m}")
    if m > data.scenario_last_mth():                                 # noqa: F821
        raise ValueError(f"point_id {point_id()}: the rate scenarios are held to month "
                         f"{data.scenario_last_mth()}, Data.read_last_mth, and no "  # noqa
                         f"projection reads month {m}")
    if name == INDEX_LEVEL:
        return float(data.index_level_array()[s, m])                 # noqa: F821
    elif name == MVA_REF_YIELD:
        return float(data.mva_ref_yield_array()[s, m])               # noqa: F821
    raise ValueError("invalid name")


def index_level(y):
    """I(y): the index level at anniversary ``y``, an anniversary number from issue.

    **Keyed by anniversary number, not by a month** — a time-point reading, so the return
    over a contract year differences this level against the next anniversary's. The S&P 500
    **price** index in the composite; dividends are excluded [S2][S6][R1].

    An anniversary at or after the first month the contract is on the books is read from the
    scenario, :func:`scenario_value`. One before it, on a contract valued mid-year, is the
    anniversary that opened the contract year under way, whose level is history the scenario
    on the valuation clock cannot give: the model point's
    :func:`index_level_prev_anniv_init`, where the year's segment started. On a contract
    valued on an anniversary the scenario sets that level at ``t = 0``, and ``Data`` holds
    the column to it.
    """
    if 12 * y - duration_mth_init() < t_entry():
        return index_level_prev_anniv_init()
    return scenario_value(y, INDEX_LEVEL)


def index_return(t):
    """R(t) = I(y+1)/I(y) - 1 with ``y = duration(t)``: the return over the contract year.

    The point-to-point segment runs from the anniversary opening the contract year of
    month ``t`` to the one closing it, where it matures.  The return is a property of the
    contract year, not of the month, and is the same for every month inside it.

    0.0 outside cover, where no contract year is the contract's.
    """
    if not is_active(t):
        return 0.0
    y = duration(t)
    prior = index_level(y)
    if prior <= 0.0:
        return 0.0
    return index_level(y + 1) / prior - 1.0


def cap_rate_in_force():
    """c(t): the annual cap actually applied.

    The declared 5.25% snapshot held level **[std]**, never below the guaranteed minimum cap
    of 0.25% [S4]. Set ``use_guaranteed_scale = True``, before the model computes anything,
    to run the contract on its guaranteed minimums instead — the notes insist the guaranteed
    and current scales are different assumption classes and "must not be mixed in the code".
    """
    if use_guaranteed_scale:                                         # noqa: F821
        return cap_rate_min                                          # noqa: F821
    return max(cap_rate_min, cap_rate())                             # noqa: F821


def fixed_rate_in_force():
    """i_F: the fixed account rate applied, 2.30% declared over a 1.00% guarantee.

    Declared [S2] and guaranteed minimum [S10]; ``use_guaranteed_scale`` switches to the
    guarantee, as for the cap.
    """
    if use_guaranteed_scale:                                         # noqa: F821
        return fixed_rate_min                                        # noqa: F821
    return max(fixed_rate_min, fixed_rate)                           # noqa: F821


def credit_rate_on(r, method):
    """cr: the credit rate for an index return ``r`` under ``method``.

    The engine the notes require, all branches floored at ``f`` = 0%:

    ``cap`` **[std]**
        ``max(f, min(c, R))`` [S2][S4][S10][R1] — the composite's baseline.
    ``par``
        ``max(f, p x R)`` [S4][S10][R1].
    ``par_cap``
        ``max(f, min(c, p x R))``, worked at [R1] as ``min(80% x 10%, 6%) = 6%`` — which
        is where ``par_rate`` = 80% comes from, and the case
        ``test_crediting_engine_reproduces_the_R1_worked_case`` asserts.
    ``spread``
        ``max(f, p x R - s)``, the spread form [R1]; one carrier names its methods
        "with Index Margin" [S8].
    ``trigger``
        ``d x 1{R >= 0}``, a declared rate credited whenever the return is non-negative
        [R1]; the floor applies when it is not.

    **The notes declare the two levels these last branches need nowhere, so both are
    [std].**  They print the *forms* — ``s`` an index margin, ``d`` a performance-trigger
    rate — and neither ``technical-notes.md`` nor ``product-spec.md`` states a value for
    either, unlike the cap (5.25% [S2]) and the participation rate (80% [R1]).  The
    shipped ``spread_rate`` = 2.00% **[std]** and ``trigger_rate`` = 4.50% **[std]** are
    illustrative levels chosen only to exercise the branch, and must not be read as
    sourced parameters of the composite.

    ``index_cost_rate`` is deducted from ``R`` **before** any cap or participation rate,
    which is where a volatility-controlled index's embedded servicing cost belongs
    [S2][S10]; it is 0 in the base run **[std]**.  The monthly-sum method is not
    implemented — see :func:`credit_method`.

    Kept as ``FIA_US_S``'s engine, for its tests and its own callers: no projection cell
    calls it. :func:`credit_rate` computes the same arithmetic inline, in the same order, on
    the decodes of ``credit_method``, so that no projection cell passes a float or a text
    argument to a cell. An engine cell (the Space docstring's *Reporting cells*): compiled,
    it keeps a Python dict for a cache and types ``method`` as ``str``, so a ``method`` that
    is not text raises ``TypeError`` there, where modelx raises ``invalid credit_method``.
    """
    net = r - index_cost_rate                                        # noqa: F821
    if method == "cap":
        raw = min(cap_rate_in_force(), net)
    elif method == "par":
        raw = par_rate * net                                         # noqa: F821
    elif method == "par_cap":
        raw = min(cap_rate_in_force(), par_rate * net)               # noqa: F821
    elif method == "spread":
        raw = par_rate * net - spread_rate                           # noqa: F821
    elif method == "trigger":
        raw = trigger_rate if net >= 0.0 else floor_rate             # noqa: F821
    else:
        raise ValueError("invalid credit_method")
    return max(floor_rate, raw)                                      # noqa: F821


def credit_rate(t):
    """cr(t): the credit rate the segment of month t's contract year matures at.

    A property of the contract year, like :func:`index_return`; it is applied once, at the
    anniversary where the segment matures. ``FIA_US_S``'s engine, :func:`credit_rate_on`,
    computed inline here, in its order, on the decodes :func:`is_credit_cap` to
    :func:`is_credit_trigger` rather than on the text of ``credit_method``: ``max(f, raw)``,
    where ``raw`` is the method's form of the return net of ``index_cost_rate``, each
    documented at :func:`credit_rate_on`. A method that is none of the five raises, as in
    ``FIA_US_S``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    net = index_return(t) - index_cost_rate                          # noqa: F821
    if is_credit_cap():
        raw = min(cap_rate_in_force(), net)
    elif is_credit_par():
        raw = par_rate * net                                         # noqa: F821
    elif is_credit_par_cap():
        raw = min(cap_rate_in_force(), par_rate * net)               # noqa: F821
    elif is_credit_spread():
        raw = par_rate * net - spread_rate                           # noqa: F821
    elif is_credit_trigger():
        raw = trigger_rate if net >= 0.0 else floor_rate             # noqa: F821
    else:
        raise ValueError("invalid credit_method")
    return max(floor_rate, raw)                                      # noqa: F821


def index_credit_pp(t):
    """IC(t) = A(0) x cr(t): the index credit on the segment maturing at month t.

    One annual segment per indexed account, created at the anniversary opening the
    contract year with the balance opening it and maturing at the anniversary closing it;
    the credit locks at maturity and cannot be lost to later declines [S1], and **it is
    not earned before then** — which is why this is zero in every month but the
    anniversary, and why the indexed balance is flat between anniversaries.  That is the
    sourced rule "withdrawals are not credited with index interest in the year they are
    taken" [S1], carried to mid-year deaths and surrenders **[std]**; crediting a part
    year would be the *daily interim value* variant the notes exclude.

    The credit base is the segment's opening balance less withdrawals from that account
    during the segment — the "Interest Credit Basis" [S6] — which collapses to the opening
    balance here because every transaction happens at an anniversary **[std]**.  Zero in
    ``DEPLETED`` and ``TERMINATED``, where steps 1-3 are skipped.

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:                 # noqa: F821
        return 0.0
    return av_indexed_pp_year_open(t) * credit_rate(t)


def fixed_interest_pp(t):
    """FI(t): interest credited to the fixed account in **month** t.

    The declared rate is an annual effective one, so the month accrues at
    ``(1 + i_F)^(1/12) - 1`` and twelve of them compound back to exactly ``i_F`` — nothing
    else touches the fixed account between anniversaries, because every contractual
    transaction falls at one.  :func:`fixed_interest_ann_pp` is the annual figure the
    benefit-base stack is computed on.

    Zero outside cover, and once the account value is exhausted, in ``DEPLETED`` and
    ``TERMINATED``. A rate in force below -1, ``fixed_rate_min`` set below -100% (with
    ``fixed_rate``, or under the guaranteed scale), raises, naming the point: its power has
    a negative base, a complex number in Python, which ``FIA_US_S`` projects or refuses at
    the next ``max``, and NaN in C. At exactly -1 the base is 0 and the account accrues
    nothing.
    """
    if not is_active(t):
        return 0.0
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:
        return 0.0
    fixed = fixed_rate_in_force()
    if 1.0 + fixed < 0.0:
        raise ValueError(f"point_id {point_id()}: the fixed rate in force, fixed_rate_min "
                         f"or fixed_rate, must be -1 or more, not {fixed}")
    rate = (1.0 + fixed) ** (1.0 / 12.0) - 1.0
    return av_fixed_pp_at(t, BEF_INV) * rate


def fixed_interest_ann_pp(t):
    """FI over the contract year closing at the anniversary in month ``t``: ``F(0) x i_F``.

    On the balance **opening** that contract year.  The twelve monthly accruals of
    :func:`fixed_interest_pp` compound to exactly this, so the annual figure is computed
    directly rather than accumulated — which is what keeps the benefit-base stack, and
    through it the whole guarantee, identical to the annual grid's.

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:                 # noqa: F821
        return 0.0
    return av_fixed_pp_year_open(t) * fixed_rate_in_force()


def inv_income_pp(t):
    """Interest credited to one contract's account value in month t.

    ``kappa x IC(t) + FI(t)``: the fixed accrual every month, and the index credit only in
    the anniversary month where the segment matures.  ``kappa`` starves the account value
    in the pure-stacking design [S3]; the benefit-base stack in :func:`stack_pp` uses the
    **gross** index credit, which is the whole point of that design.
    """
    return av_int_factor() * index_credit_pp(t) + fixed_interest_pp(t)


def rider_charge_pp(t):
    """Phi(t) = phi x BB(0): the GLWB rider charge, deducted once a year [S9].

    On the **benefit base**, not the account value, and taken **after** index credits are
    added — the notes' ordering, which is why the base in the formula is the *opening*
    base.  In the worked example the base closes at 1.59 times the account value, so
    charging on the account value would understate the deduction by a growing margin.
    Deducted from the fixed account first and then proportionately across indexed
    accounts [S9].  ``phi`` is fixed for fifteen contract years and never exceeds 1.50%
    [S9]; re-declaration after that is not implemented.  **Once the account value is
    exhausted the charge stops** — there is nothing to deduct it from and income
    continues [S9].

    The charge is annual by contract [S9], so on the monthly grid it lands whole on the
    anniversary rather than being spread over the year; the monthly deduction documented
    at one carrier is a variant this composite does not adopt **[std]**.

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    if not rider_in_force_open(t):
        return 0.0
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:                 # noqa: F821
        return 0.0
    return (min(rider_charge_rate, rider_charge_rate_max)            # noqa: F821
            * benefit_base_pp_at(t, BEF_ROLLUP))


def av_pp_at(t, timing):
    """AV per contract in **month** t, read at the point given by ``timing``.

    ``BEF_PREM`` is the balance carried into the month before the single premium:
    :func:`av_pp_init` at :func:`t_entry`, the account value of a contract in force at the
    valuation date and zero on new business, and ``AV(t-1)`` after it; ``BEF_INV`` is the
    balance opening the month after the premium, which adds :func:`prem_to_av_pp`,
    ``P x (1 + b)`` in the issue month and zero in every other; ``BEF_FEE`` is after the
    month's interest — the fixed accrual every month, plus the index credit in an
    anniversary month; ``BEF_WD`` is after the rider charge; ``EOY`` is after the
    withdrawal, the closing balance :func:`av_pp`. **In a month that is not an anniversary
    the last three coincide**, at the opening balance plus the fixed accrual, because every
    contractual transaction falls at an anniversary.

    Only ``EOY`` is floored at zero: **the 0% floor is on the index credit, not on the
    account value** [S7], so ``BEF_WD`` may legitimately sit below the opening balance or
    below zero when the rider charge exceeds the credit. Flooring it would silently remove
    the charge drag that produces depletion.

    Each timing is built from the month's opening in one formula, in ``FIA_US_S``'s order,
    so that reading any timing adds one cell to the chain beneath it; the chain itself is
    :func:`av_pp`, one cell a month. 0.0 outside cover, at every timing.
    """
    if not is_active(t):
        return 0.0
    val = av_pp(t - 1) if t > t_entry() else av_pp_init()
    if timing == BEF_PREM:
        return val
    val = val + prem_to_av_pp(t)
    if timing == BEF_INV:
        return val
    val = val + inv_income_pp(t)
    if timing == BEF_FEE:
        return val
    val = val - rider_charge_pp(t)
    if timing == BEF_WD:
        return val
    if timing == EOY:
        return av_pp(t)
    raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the account value per contract closing **month** t, after all processing.

    ``max(0, AV(t-1) + premium + interest - rider charge - withdrawal)``, the steps of
    :func:`av_pp_at` in its order, with the opening written inline — :func:`av_pp_init` at
    :func:`t_entry` and ``av_pp(t - 1)`` after it — so that the account value's chain runs
    one cell a month back to :func:`t_entry`, where ``FIA_US_S``'s runs through two, this
    cell and :func:`av_pp_at`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = (av_pp(t - 1) if t > t_entry() else av_pp_init()) + prem_to_av_pp(t)
    return max(0.0, opening + inv_income_pp(t) - rider_charge_pp(t) - wd_pp(t))


def av_pp_year_open(t):
    """AV(0): the account value **opening** the contract year containing month ``t``.

    The balance the annual index credit and the free withdrawal allowance are computed on,
    read three ways. Where the anniversary that opened the year, :func:`year_open_mth`, is
    at or after :func:`t_entry`, it is that anniversary's closing value, from the frame.
    Where it is before, on a contract in force at the valuation date, valued mid-year or on
    its anniversary, the year opened before the first month on the books, and it is the
    model point's :func:`av_pp_prev_anniv_init`. And on a
    contract issued at or after the valuation date the year is its first, and it is the
    issue value, :func:`prem_to_av_pp` of the issue month, the notes' Initialisation value.
    On an annual grid this would simply be the previous row's close; on the monthly grid the
    previous *month* is not the previous *year*, which is what this cell exists to keep
    straight. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = year_open_mth(t)
    if prev >= t_entry():
        return av_pp(prev)
    if duration_mth_init() > 0:
        return av_pp_prev_anniv_init()
    return prem_to_av_pp(t_entry())


def av_fixed_pp_year_open(t):
    """F(0): the fixed account balance opening the contract year containing month ``t``.

    Read the three ways :func:`av_pp_year_open` is: from the frame; from the model point's
    :func:`av_fixed_pp_prev_anniv_init` where the year opened before the valuation date; or,
    in the first year of a contract issued at or after it, by the issue rule, the fixed
    share of the premium and bonus, ``alloc_fixed() x P x (1 + b)``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = year_open_mth(t)
    if prev >= t_entry():
        return av_fixed_pp(prev)
    if duration_mth_init() > 0:
        return av_fixed_pp_prev_anniv_init()
    return alloc_fixed() * prem_to_av_pp(t_entry())


def av_indexed_pp_year_open(t):
    """A(0): the indexed balance opening the contract year — the segment's credit base."""
    return av_pp_year_open(t) - av_fixed_pp_year_open(t)


def av_fixed_pp_at(t, timing):
    """F per contract in month t; see :func:`av_pp_at` for ``timing``.

    The fixed account is the one balance that moves between anniversaries: it accrues at
    ``(1 + i_F)^(1/12) - 1`` every month.  The rider charge comes out of it **first** and
    only then proportionately across the indexed accounts [S9].  The notes give no
    allocation rule for withdrawals, so they are taken **pro rata** across the two accounts
    **[std]**; with the baseline 100% indexed allocation neither rule is visible.

    At :func:`t_entry` the fixed account opens on :func:`av_fixed_pp_init`, the fixed
    account in force at the valuation date, and in the issue month the premium's fixed
    share, ``alloc_fixed()`` times :func:`prem_to_av_pp`, comes on top. Each timing is built
    from the month's opening in one formula; the chain itself is :func:`av_fixed_pp`, one
    cell a month. 0.0 outside cover, at every timing.
    """
    if not is_active(t):
        return 0.0
    val = av_fixed_pp(t - 1) if t > t_entry() else av_fixed_pp_init()
    if timing == BEF_PREM:
        return val
    val = val + alloc_fixed() * prem_to_av_pp(t)
    if timing == BEF_INV:
        return val
    val = val + fixed_interest_pp(t)
    if timing == BEF_FEE:
        return val
    val = max(0.0, val - rider_charge_pp(t))
    if timing == BEF_WD:
        return val
    if timing == EOY:
        return av_fixed_pp(t)
    raise ValueError("invalid timing")


def av_fixed_pp(t):
    """F(t): the fixed account balance per contract closing month t.

    The steps of :func:`av_fixed_pp_at` in its order: the opening written inline,
    ``av_fixed_pp(t - 1)``, or :func:`av_fixed_pp_init` at :func:`t_entry`, plus the
    premium's fixed share in the issue month; the month's accrual; the rider charge, floored
    at zero; and the withdrawal's pro rata share. So the fixed account's chain runs one cell
    a month back to :func:`t_entry`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = ((av_fixed_pp(t - 1) if t > t_entry() else av_fixed_pp_init())
               + alloc_fixed() * prem_to_av_pp(t))
    val = max(0.0, opening + fixed_interest_pp(t) - rider_charge_pp(t))
    total = av_pp_at(t, BEF_WD)
    if total <= 0.0:
        return 0.0
    share = min(1.0, max(0.0, wd_pp(t) / total))
    return max(0.0, val * (1.0 - share))


def av_indexed_pp_at(t, timing):
    """A per contract in month t: ``AV - F`` at the same timing, by construction."""
    return av_pp_at(t, timing) - av_fixed_pp_at(t, timing)


def av_indexed_pp(t):
    """A(t): the indexed account balance per contract closing month t.

    Flat between anniversaries — the segment credits only at maturity — and stepped at
    each anniversary by that year's index credit net of its share of the charge and the
    withdrawal.
    """
    return av_indexed_pp_at(t, EOY)


def av_depletion_pp(t):
    """The part of month t's withdrawal the account value could not fund.

    Zero until the account value runs out, then the shortfall between the withdrawal
    requested and the balance available to meet it.  It is the term that makes the
    account value roll-forward close across the depletion anniversary, where ``AV(t)`` is
    floored at zero.

    **It is not the same thing as an amount paid.** Whether the shortfall is a payment
    depends on which exhaustion branch the anniversary closes on: in ``DEPLETED`` the
    guarantee is alive and the insurer funds it from its own funds [S1][S3][S9][R1], on
    the ``TERMINATED`` branch there is neither balance nor promise behind it and it is
    not paid at all.  :func:`wd_unfunded_pp` carries that half, and only that half is
    kept out of the ledger.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return max(0.0, wd_pp(t) - av_pp_at(t, BEF_WD))


def surr_charge_rate_py(y):
    """sc(y): the surrender charge percentage of contract year ``y`` [S5].

    9.1, 9, 8, 7, 6, 5, 4, 3, 2, 1% over the ten-year charge period and zero thereafter;
    the last row of the table holds for every later year. The reader of the schedule's
    charge column, keyed by the contractual 1-based contract year, from
    ``Data.surr_charge_rate_array``, held by year from the checked schedule to its last
    year, ``Data.surr_charge_last_year``; :func:`surr_charge_rate` calls it in cover only.
    A year below 1, which no projection reads, raises ``ValueError`` naming the point, where
    ``FIA_US_S``'s lookup raised ``KeyError``.
    """
    if y < 1:
        raise ValueError(f"point_id {point_id()}: the surrender charge table gives no "
                         f"rate at contract year {y}")
    last = data.surr_charge_last_year()                              # noqa: F821
    return float(data.surr_charge_rate_array()[min(y, last)])        # noqa: F821


def vest_rate_py(y):
    """v(y): the vested percentage of the premium bonus in contract year ``y`` [S5].

    0, 10, ..., 100% over eleven contract years; the last row holds for every later year.
    The reader of the schedule's vesting column, ``Data.vest_rate_array``, as
    :func:`surr_charge_rate_py` is of its charge; :func:`vest_rate` calls it in cover only.
    """
    if y < 1:
        raise ValueError(f"point_id {point_id()}: the surrender charge table gives no "
                         f"vesting at contract year {y}")
    last = data.surr_charge_last_year()                              # noqa: F821
    return float(data.vest_rate_array()[min(y, last)])               # noqa: F821


def surr_charge_rate(t):
    """sc(t): the surrender charge percentage of month t's contract year [S5].

    9.1, 9, 8, 7, 6, 5, 4, 3, 2, 1% over the ten-year charge period and zero thereafter; the
    last row of the table holds for every later year. The schedule is keyed by the
    contractual 1-based contract year and read at ``policy_year(t)``, through
    :func:`surr_charge_rate_py`, so the rate is the same in every month of a year. 0.0
    outside cover, before the schedule is read.
    """
    if not is_active(t):
        return 0.0
    return surr_charge_rate_py(policy_year(t))


def vest_rate(t):
    """v(t): the vested percentage of the premium bonus in month t's contract year [S5].

    0, 10, ..., 100% over eleven contract years, read at ``policy_year(t)``.  On
    **death** 100% vests immediately [S5], which is why the death benefit carries no
    clawback.

    Read from :func:`vest_rate_py`. 0.0 outside cover, before the schedule is read.
    """
    if not is_active(t):
        return 0.0
    return vest_rate_py(policy_year(t))


def rollup_rate_py(y):
    """g(y): the guaranteed simple rollup rate of contract year ``y`` [S2][S9].

    The model point's schedule read as a step function of the contract year: the rate of the
    schedule's last row at or before ``y``, or 0 before its first. The table's one reader,
    of ``Data.rollup_rate_array``, which holds each schedule step-filled by contract year,
    0.0 before its first row, at the row :func:`rollup_number` gives the point's
    ``rollup_id``; :func:`rollup_rate` calls it in cover only. A year past the array's last,
    ``Data.rollup_last_year``, which no projection reads, raises, naming the point.
    """
    if y < 1:
        return 0.0
    if y > data.rollup_last_year():                                  # noqa: F821
        raise ValueError(f"point_id {point_id()}: the rollup schedules are held to "
                         f"contract year {data.rollup_last_year()}, and no projection "
                         f"reads year {y}")
    return float(data.rollup_rate_array()[rollup_number(), y])       # noqa: F821


def rollup_rate(t):
    """g(t): the guaranteed simple rollup rate of month t's contract year [S2][S9].

    Read as a step function of the contract year ``policy_year(t)`` from the model
    point's schedule: the blended baseline is 5.00% in years 1-10, 2.00% in years 11-20 and
    zero after [S2]; another documented design is a flat 3.00% over fifteen anniversaries
    [S9].

    Read at ``policy_year(t)`` from :func:`rollup_rate_py`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return rollup_rate_py(policy_year(t))


def payout_rate(a, basis):
    """pi(a, basis): the lifetime withdrawal percentage at attained age ``a`` [S3].

    Five inclusive attained-age bands; the joint column is the single column less 0.50%
    [S1][S3].  Zero below the first band, because no lifetime withdrawal is permitted
    there; the last band holds above its upper age.

    Kept as ``FIA_US_S``'s cell, for its tests: no projection cell calls it, and it still
    walks ``payout_rate_table()`` row by row. :func:`payout_rate_locked` reads
    :func:`payout_rate_at`, the same percentages from the checked bands, on the decoded
    basis. An engine cell (the Space docstring's *Reporting cells*): compiled, it keeps a
    Python dict for a cache and types ``basis`` as ``str``, so a ``basis`` that is not text
    raises ``TypeError`` there, where modelx raises ``invalid glwb_basis``.
    """
    if basis == "single":
        column = "payout_rate_single"
    elif basis == "joint":
        column = "payout_rate_joint"
    else:
        raise ValueError("invalid glwb_basis")
    table = data.payout_rate_table()                                 # noqa: F821
    for _, row in table.iterrows():
        if int(row["age_lo"]) <= a <= int(row["age_hi"]):
            return float(row[column])
    last = table.iloc[-1]
    return float(last[column]) if a > int(last["age_hi"]) else 0.0


def payout_rate_at(a):
    """pi(a): the lifetime withdrawal percentage at attained age ``a`` on the point's basis.

    :func:`payout_rate` on ``Data.payout_rate_array``, the checked bands held one row an age
    from the first band's age [S3]: the single-life column on :func:`is_single_basis` and
    the joint-life column on :func:`is_joint_basis`, a basis that is neither raising, as
    :func:`payout_rate` raises; 0 below the first band's age, because no lifetime withdrawal
    is permitted there; and the last band's percentage above its last age. The table's one
    reader, keyed by the age; :func:`payout_rate_locked` calls it in cover only, at the
    exercise age. The array holds ages to ``Data.read_last_age``, 122, past any exercise
    age; an age past it, which no projection reads, raises, naming the point.
    """
    if is_single_basis():
        column = 0
    elif is_joint_basis():
        column = 1
    else:
        raise ValueError("invalid glwb_basis")
    first = data.payout_rate_first_age()                             # noqa: F821
    if a < first:
        return 0.0
    if a > data.payout_rate_held_age():                              # noqa: F821
        raise ValueError(f"point_id {point_id()}: the payout bands are held to age "
                         f"{data.payout_rate_held_age()}, Data.read_last_age, and no "
                         f"projection reads age {a}")
    return float(data.payout_rate_array()[a - first, column])        # noqa: F821


def payout_rate_locked(t):
    """The payout percentage in force in the contract year of month t.

    Locked at the attained age of the **first** lifetime withdrawal, :func:`exercise_age`,
    and not re-read afterwards **[std]**.  :func:`is_exercise` is a property of the
    contract year, so the lock holds for every month of the year it is set in and is then
    carried from anniversary to anniversary.  Documented alternatives: one carrier reads
    the band from the age at the most recent anniversary, letting it step up [S3]; another
    makes it depend on both issue age and the youngest covered person's age at exercise
    [S9]; a third uses sex-distinct factors [S5].

    It is carried from the anniversary that opened the year: from the frame, or, where that
    anniversary precedes the first month on the books, from the model point's
    :func:`payout_rate_locked_prev_anniv_init` on a contract in force and 0 on new business;
    in the exercise year it is :func:`payout_rate_at` the exercise age. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_exercise(t):
        return payout_rate_at(exercise_age(t))
    prev = year_open_mth(t)
    if prev >= t_entry():
        return payout_rate_locked(prev)
    if duration_mth_init() > 0:
        return payout_rate_locked_prev_anniv_init()
    return 0.0


def activation_rate(a):
    """h(a): the GLWB activation incidence at attained age ``a`` **[std]**.

    ``0`` below 60, 5% from 60 to the RMD age, 40% at it and 15% above [R1][REG-R64].
    ``rmd_age`` is a configurable Reference and **must not be hard-coded**: the statutory
    age is set by IRC 401(a)(9) as amended by SECURE 2.0 and finalized in T.D. 10001
    [REG-R57][REG-R58] and is not printed in the retrieved research material.

    **Reported only.** A single deterministic cell cannot activate a fraction of itself, so
    the base run exercises at the model point's ``income_start_age`` instead; this cell
    exists so the incidence assumption is visible and testable rather than implied.
    """
    if a < activation_age_low:                                       # noqa: F821
        return 0.0
    if a < rmd_age:                                                  # noqa: F821
        return activation_rate_early                                 # noqa: F821
    if a == rmd_age:                                                 # noqa: F821
        return activation_rate_rmd                                   # noqa: F821
    return activation_rate_late                                      # noqa: F821


def phase_year_open(t):
    """The phase **opening** the contract year of month ``t``, as a code.

    The phase at the anniversary that opened the year, read three ways, as
    :func:`av_pp_year_open` is: the closing :func:`phase` there, from the frame; the model
    point's :func:`phase_prev_anniv_init` where that anniversary precedes the valuation date
    on a contract in force; and ``ACCUM`` on a contract issued at or after it, whose first
    year opens in deferral. ``FIA_US_S`` writes this read inline in each of its readers;
    here it is a cell of its own, read by :func:`is_exercise`, :func:`phase_open` and
    :func:`in_growth_period`. ``PRE_ISSUE`` before issue and ``MATURED`` from
    :func:`proj_len` on.
    """
    if duration_mth(t) < 0:
        return PRE_ISSUE                                             # noqa: F821
    if duration_mth(t) >= maturity_mth():
        return MATURED                                               # noqa: F821
    prev = year_open_mth(t)
    if prev >= t_entry():
        return phase(prev)
    if duration_mth_init() > 0:
        return phase_prev_anniv_init()
    return ACCUM                                                     # noqa: F821


def is_exercise(t):
    """True through the contract year whose closing anniversary carries the **first** LW.

    Requires an in-force rider, the ``ACCUM`` phase opening the year and an
    :func:`exercise_age` at or above both the contractual minimum of 50 [S2][S3][S9] and
    the model point's ``income_start_age``.  It depends only on the state **opening** the
    contract year, which is what lets the phase, the benefit base and the withdrawal be
    evaluated without a circular reference — and what makes it constant across the year,
    so every month of the exercise year reads the same phase and the same locked payout
    percentage.

    The phase opening the year is :func:`phase_year_open`. False outside cover.
    """
    if not is_active(t):
        return False
    if not glwb_elected():
        return False
    if phase_year_open(t) != ACCUM:                                  # noqa: F821
        return False
    if not rider_in_force_open(t):
        return False
    return exercise_age(t) >= max(min_income_age, income_start_age())  # noqa: F821


def phase_open(t):
    """The phase the annual steps of month t's contract year are processed under.

    The phase **opening the contract year**, :func:`phase_year_open`, promoted to ``INCOME``
    when the first lifetime withdrawal falls in this year. Constant across the twelve
    months, because every one of the eight steps belongs to the year rather than to the
    month. Steps 1-3 are skipped when this is ``DEPLETED`` and steps 1-7 when it is
    ``TERMINATED``. A code, as every phase cell returns: ``PRE_ISSUE`` before issue and
    ``MATURED`` from :func:`proj_len` on, which no cell in cover reads.
    """
    if duration_mth(t) < 0:
        return PRE_ISSUE                                             # noqa: F821
    if duration_mth(t) >= maturity_mth():
        return MATURED                                               # noqa: F821
    opening = phase_year_open(t)
    if opening == ACCUM and is_exercise(t):                          # noqa: F821
        return INCOME                                                # noqa: F821
    return opening


def depletion_cause(t):
    """True when a charge, an excess withdrawal or a negative MVA touched the AV in month t.

    The attribution test of step 5, evaluated **before** the depletion test: an account
    value run to zero by an excess withdrawal, a surrender charge or a market value
    adjustment loses the guarantee entirely, while one run to zero by guaranteed
    withdrawals and rider charges keeps it [S1][S5][S9].  One carrier's confinement and
    terminal illness waivers are themselves excess withdrawals that terminate the income
    rider [S1] — a trap if waivers are added.

    False outside cover.
    """
    if not is_active(t):
        return False
    return (wd_excess_pp(t) > 0.0 or wd_charge_pp(t) > 0.0
            or wd_mva_pp(t) < 0.0)


def phase(t):
    """The phase closing month t, after step 7's transition at the anniversary.

    Step 7 is annual and the account value can only reach zero at an anniversary — nothing
    between them takes a withdrawal or a charge — so away from one this simply carries
    :func:`phase_open`, and the transition is tested at the anniversary itself.

    ``ACCUM -> INCOME`` at the first lifetime withdrawal;
    ``INCOME -> DEPLETED`` when the account value reaches zero with no
    :func:`depletion_cause`, which is where the economic value of the guarantee sits;
    ``INCOME -> TERMINATED`` when it reaches zero *with* one; and
    ``any -> TERMINATED`` when the benefit base reaches zero [S9].  An account value
    exhausted in ``ACCUM`` terminates rather than depletes **[std]**: the notes define
    the depleted state only out of ``INCOME``, and before exercise there is no ``LW`` to
    pay.

    The phase is an int code, named by the References ``ACCUM`` to ``TERMINATED``, and
    :func:`result_glwb` decodes it back to the label. ``PRE_ISSUE`` before issue and
    ``MATURED`` from :func:`proj_len` on.
    """
    if duration_mth(t) < 0:
        return PRE_ISSUE                                             # noqa: F821
    if duration_mth(t) >= maturity_mth():
        return MATURED                                               # noqa: F821
    opening = phase_open(t)
    if opening == TERMINATED:                                        # noqa: F821
        return TERMINATED                                            # noqa: F821
    if opening == DEPLETED:                                          # noqa: F821
        return DEPLETED                                              # noqa: F821
    if not is_anniv(t):
        return opening
    if glwb_elected() and benefit_base_pp(t) <= 0.0:
        return TERMINATED                                            # noqa: F821
    if av_pp(t) <= 0.0:
        if opening == INCOME and not depletion_cause(t):             # noqa: F821
            return DEPLETED                                          # noqa: F821
        return TERMINATED                                            # noqa: F821
    return opening


def rider_in_force_open(t):
    """Whether the GLWB rider is alive **opening** the contract year of month t.

    :func:`rider_in_force` at the previous anniversary where that anniversary is at or after
    :func:`t_entry`, and ``glwb_elected()`` where it is before: in the first contract year
    of a contract issued at or after the valuation date, and in the year under way on one in
    force. The model point carries no rider status, because a contract in force with the
    rider elected has the rider alive: ``Data`` refuses ``TERMINATED`` in force and a
    benefit base of 0 under the rider, the two ways the rider dies short of death. Kept as a
    cell of its own, like :func:`phase_open`, because five formulas need the opening rider
    state and none of them may reach for a closing one. False outside cover.
    """
    if not is_active(t):
        return False
    prev = year_open_mth(t)
    if prev >= t_entry():
        return rider_in_force(prev)
    return bool(glwb_elected())


def rider_in_force(t):
    """Whether the GLWB rider is still alive at the end of month t [S9].

    It terminates on the earliest of death of the covered person, the benefit base
    reduced to zero, termination of the base contract, assignment, owner cancellation on
    or after the earliest cancellation date, or a change in a covered person — with no
    refund of past charges [S9].  Death is a decrement here, and cancellation and
    assignment are not modelled, so what survives is the base-reaching-zero and
    contract-termination legs.

    False outside cover.
    """
    if not is_active(t):
        return False
    if not glwb_elected():
        return False
    if not rider_in_force_open(t):
        return False
    if phase(t) == TERMINATED:                                       # noqa: F821
        return False
    return benefit_base_pp(t) > 0.0


def in_growth_period(t):
    """T_g: whether the benefit base still rolls up and stacks in month t's contract year.

    To the earlier of the first lifetime withdrawal and contract year 20 [S1][S2].  The
    year of exercise itself is still inside the window — the worked example credits both
    the rollup and the stack in contract year 8, the year income starts — which is why the
    test is on the phase *opening* the year.

    The phase opening the year is :func:`phase_year_open`. False outside cover.
    """
    if not is_active(t):
        return False
    if not glwb_elected():
        return False
    if policy_year(t) > growth_period_max:                           # noqa: F821
        return False
    return phase_year_open(t) == ACCUM                               # noqa: F821


def is_step_up_annual():
    """Whether the step-up is tested at every anniversary, ``step_up_mode`` ``ANNUAL``.

    A decode of the Reference, an int code, ``ANNUAL`` 0 or ``AT_EXERCISE`` 1, where
    ``FIA_US_S`` holds the text ``"annual"`` or ``"at_exercise"``, so that
    :func:`step_up_applies` branches on a flag and no projection cell reads text. Set
    ``step_up_mode`` before the model computes anything. A text set on it is no code: both
    decodes answer False, and :func:`step_up_applies` raises ``FIA_US_S``'s message.
    """
    return bool(step_up_mode == ANNUAL)


def is_step_up_at_exercise():
    """Whether the step-up is tested at the first exercise only, ``step_up_mode``
    ``AT_EXERCISE``.

    The other decode of the Reference (:func:`is_step_up_annual`): a mode that is neither
    raises in :func:`step_up_applies`, as in ``FIA_US_S``.
    """
    return bool(step_up_mode == AT_EXERCISE)


def step_up_applies(t):
    """Whether the annual step-up ``BB <- max(BB, AV)`` is tested at month t.

    Annual by construction, so it is tested only at the anniversary.

    **A [std] generalisation.** No retrieved document describes an automatic annual
    ratchet during deferral; documented instead are an at-exercise step-up to the
    contract value [S5], an annual benefit amount computed on the greater of base and
    account value at exercise [S9], and a never-decreasing income amount once withdrawals
    begin [S3].  ``step_up_mode = AT_EXERCISE`` reduces the model to those designs;
    ``ANNUAL`` is the superset and the baseline.  Under the blended baseline it rarely
    binds — a dollar of credit adds $1 to the account value and $1.50 to the base — but
    *rarely is not never*: on a new issue the bonus opens contract year 1 with an account
    value of ``107,000`` against a benefit base of ``100,000``, so a first contract year
    with a zero index credit gives an account value of ``106,050`` against a base of
    ``105,000`` and the step-up binds.

    The mode is read through its decodes, :func:`is_step_up_annual` and
    :func:`is_step_up_at_exercise`, a mode that is neither raising. False outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return False
    if not glwb_elected():
        return False
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:                 # noqa: F821
        return False
    if is_step_up_annual():
        return True
    elif is_step_up_at_exercise():
        return is_exercise(t)
    else:
        raise ValueError("invalid step_up_mode")


def rollup_base_pp_year_open(t):
    """RB(0): the rollup base **opening** the contract year of month ``t``.

    Read three ways, as :func:`av_pp_year_open` is: :func:`rollup_base_pp` at the
    anniversary that opened the year, from the frame; the model point's
    :func:`rollup_base_pp_init` where that anniversary precedes the valuation date on a
    contract in force, the rollup base being flat between anniversaries; and the issue value
    on a contract issued at or after it, ``P`` under the rider and 0 without it [S2][S9].
    ``FIA_US_S`` writes this read inline in :func:`rollup_pp` and :func:`rollup_base_pp`;
    here it is a cell of its own, which both read. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = year_open_mth(t)
    if prev >= t_entry():
        return rollup_base_pp(prev)
    if duration_mth_init() > 0:
        return rollup_base_pp_init()
    return premium_pp() if glwb_elected() else 0.0


def rollup_pp(t):
    """rollup(t) = g(t) x RB(0): the guaranteed rollup increment, once a year.

    **A flat dollar increment, not simple interest on the grown base.** One carrier
    computes it on premium less withdrawals [S2] and another on the adjusted *initial*
    base [S9]; the latter's fifteen-year table confirms a constant $3,000 a year on a
    $100,000 adjusted initial base [S9].  Compounding it inflates the base and every
    downstream charge and payment.

    Computed on the rollup base opening the year, :func:`rollup_base_pp_year_open`.
    """
    if not is_anniv(t) or not in_growth_period(t):
        return 0.0
    return rollup_rate(t) * rollup_base_pp_year_open(t)


def stack_pp(t):
    """stack(t) = m x max(0, IC(t) + FI(t)): the stacking credit at the anniversary.

    On **realised dollar credits** [S8] [S9], net of any strategy fee (zero here) and
    floored at zero [S9] — one specimen's separately named stacking credit.  The gross index
    credit is used, so the pure stacking design can credit 250% to the base while
    ``kappa`` sends only 50% to the account value [S3][S4].  ``FI`` here is the **annual**
    fixed interest of the contract year, :func:`fixed_interest_ann_pp`, not the
    anniversary month's own accrual.
    """
    if not is_anniv(t) or not in_growth_period(t):
        return 0.0
    return stack_factor() * max(0.0, index_credit_pp(t) + fixed_interest_ann_pp(t))


def benefit_base_pp_at(t, timing):
    """BB per contract in month t, read at the point given by ``timing``.

    ``BEF_ROLLUP`` is the base **opening the contract year**; ``BEF_STEP_UP`` is after
    the rollup and the stack; ``BEF_WD`` is after the annual step-up and is the base the
    lifetime withdrawal is computed on; ``EOY`` is after step 5's proportional reduction.
    All four steps are annual, so away from an anniversary every timing returns the opening
    base and the benefit base is flat.

    The opening base is read three ways, as :func:`av_pp_year_open` is: the base at the
    previous anniversary, from the frame; the model point's :func:`benefit_base_pp_init`,
    flat since the anniversary on or before the valuation date, where the year opened before
    it; and the premium ``P``, the bonus kept out [S9], in the first year of a contract
    issued at or after it.

    The base is **notional**: it has no cash value, cannot be withdrawn and cannot be taken
    as a lump sum [S1][S9]. 0.0 outside cover, at every timing, and 0.0 without the rider or
    once it has died.
    """
    if not is_active(t):
        return 0.0
    if not glwb_elected() or not rider_in_force_open(t):
        return 0.0
    prev = year_open_mth(t)
    if prev >= t_entry():
        opening = benefit_base_pp(prev)
    elif duration_mth_init() > 0:
        opening = benefit_base_pp_init()
    else:
        opening = premium_pp()
    if timing == BEF_ROLLUP:
        return opening
    val = opening + rollup_pp(t) + stack_pp(t)
    if timing == BEF_STEP_UP:
        return val
    if step_up_applies(t):
        val = max(val, av_pp_at(t, BEF_WD))
    if timing == BEF_WD:
        return val
    if timing == EOY:
        return val * (1.0 - wd_reduction_rate(t))
    raise ValueError("invalid timing")


def benefit_base_pp(t):
    """BB(t): the GLWB benefit base per contract closing month t."""
    return benefit_base_pp_at(t, EOY)


def is_rb_pro_rata():
    """Whether a withdrawal reduces the rollup base pro rata, ``rb_wd_convention``
    ``PRO_RATA``.

    A decode of the Reference, an int code, ``PRO_RATA`` 0 or ``DOLLAR`` 1, where
    ``FIA_US_S`` holds ``"pro_rata"`` or ``"dollar"``, as :func:`is_step_up_annual` is, read
    by :func:`rollup_base_pp`.
    """
    return bool(rb_wd_convention == PRO_RATA)


def is_rb_dollar():
    """Whether a withdrawal reduces the rollup base dollar for dollar, ``rb_wd_convention``
    ``DOLLAR``.

    The other decode of the Reference (:func:`is_rb_pro_rata`): a convention that is
    neither raises in :func:`rollup_base_pp`, as in ``FIA_US_S``.
    """
    return bool(rb_wd_convention == DOLLAR)


def rollup_base_pp(t):
    """RB(t): the rollup base closing month t.

    Reduced in the same proportion as the benefit base under the baseline **[std]**
    convention [S9], and only at an anniversary, where the reduction happens. Set
    ``rb_wd_convention = DOLLAR``, before the model computes anything, for the alternative
    documented at another carrier, ``RB(t) = max(0, RB(0) - G(t))`` — "Premium minus
    Withdrawals" [S2].

    It opens the year on :func:`rollup_base_pp_year_open`, and reads the convention through
    its decodes, :func:`is_rb_pro_rata` and :func:`is_rb_dollar`, a convention that is
    neither raising. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = rollup_base_pp_year_open(t)
    if is_rb_pro_rata():
        return opening * (1.0 - wd_reduction_rate(t))
    elif is_rb_dollar():
        return max(0.0, opening - wd_pp(t))
    else:
        raise ValueError("invalid rb_wd_convention")


def lw_pp_at(t, timing):
    """LW per contract in month t, read at the point given by ``timing``.

    ``BEF_WD`` is the amount payable at this contract year's anniversary, after step 4's
    ratchet; ``EOY`` is the closing value, after step 5's proportional reduction.  The
    ratchet is annual, so away from an anniversary this carries the amount set at the last
    one — the income in force, which is what a mid-year reading of the rider state means.

    At exercise ``LW = pi x BB(4)``; afterwards the ratchet ``LW = max(LW(0), pi x BB(4))``
    applies so income never decreases [S3].  Unused ``LW`` does **not** carry forward [S9];
    one carrier is the exception, accumulating the shortfall without interest [S3].  In
    ``DEPLETED`` the amount is simply carried: there is no base to recompute it from.

    The amount carried from the anniversary that opened the year is :func:`lw_pp` there,
    from the frame, or, where that anniversary precedes the first month on the books, the
    model point's :func:`lw_pp_init` on a contract in force and 0 on new business. 0.0
    outside cover, at both timings; any other timing raises in cover.
    """
    if not is_active(t):
        return 0.0
    if timing != BEF_WD and timing != EOY:
        raise ValueError("invalid timing")
    prev = year_open_mth(t)
    if prev >= t_entry():
        prior = lw_pp(prev)
    elif duration_mth_init() > 0:
        prior = lw_pp_init()
    else:
        prior = 0.0
    opening = phase_open(t)
    if not is_anniv(t):
        return 0.0 if opening == TERMINATED else prior               # noqa: F821
    if opening == TERMINATED:                                        # noqa: F821
        val = 0.0
    elif opening == DEPLETED:                                        # noqa: F821
        val = prior
    elif opening == INCOME:                                          # noqa: F821
        candidate = payout_rate_locked(t) * benefit_base_pp_at(t, BEF_WD)
        val = candidate if is_exercise(t) else max(prior, candidate)
    else:
        val = 0.0
    if timing == BEF_WD:
        return val
    return val * (1.0 - wd_reduction_rate(t))


def lw_pp(t):
    """LW(t): the lifetime withdrawal amount per contract closing month t."""
    return lw_pp_at(t, EOY)


def wd_scheduled_at(k):
    """The ad hoc withdrawal the point's programme schedules at contract year count ``k``.

    ``FIA_US_S`` looks up ``(wd_schedule_id, k)``, an exact key, else zero: a contract year
    with no row takes nothing. **The key is an elapsed contract year count**, on the policy
    clock — a row keyed ``k`` is a withdrawal at the anniversary closing contract year
    ``k + 1``. The table's one reader, of ``Data.wd_amount_array``, which holds each
    programme by count, 0.0 where it has no row, at the row :func:`wd_schedule_number`
    gives the point's ``wd_schedule_id``; :func:`wd_scheduled_pp` calls it in cover only,
    in the anniversary month. A count below 0 is no row, 0.0; one past the array's last,
    ``Data.wd_last_year``, which no projection reads, raises, naming the point.
    """
    if k < 0:
        return 0.0
    if k > data.wd_last_year():                                      # noqa: F821
        raise ValueError(f"point_id {point_id()}: the withdrawal programmes are held to "
                         f"{data.wd_last_year()} contract years, and no projection reads "
                         f"{k}")
    return float(data.wd_amount_array()[wd_schedule_number(), k])    # noqa: F821


def wd_scheduled_pp(t):
    """The ad hoc gross withdrawal at the anniversary closing month t's contract year.

    Read from *withdrawal_table.csv*, which is **not** a step function: a contract year
    with no row takes nothing. **Its key column is an elapsed contract year count, not a
    month** — a row keyed ``k`` is a withdrawal at the anniversary closing contract year
    ``k + 1`` — so it is read at ``duration(t)``, through :func:`wd_scheduled_at`, on the
    policy clock. Lifetime withdrawals are generated by the rider, not scheduled here. Zero
    in every other month, and outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    return wd_scheduled_at(duration(t))


def wd_pp(t):
    """G(t): the gross withdrawal taken at the anniversary in month t.

    Zero in every other month: both the lifetime withdrawal and the ad hoc schedule are
    contractually annual, so the finer grid moves no cash between anniversaries.  In
    ``INCOME``, ``utilization_intensity() x LW`` plus any scheduled ad hoc amount; in
    ``DEPLETED``, exactly ``LW``, paid by the insurer from its own funds; in ``ACCUM``,
    only the scheduled amount.  Gross by construction: a contract promising a stated net
    check would need a gross-up solve, which is not implemented.

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    opening = phase_open(t)
    if opening == TERMINATED:                                        # noqa: F821
        return 0.0
    if opening == DEPLETED:                                          # noqa: F821
        return lw_pp_at(t, BEF_WD)
    if opening == INCOME:                                            # noqa: F821
        return utilization_intensity() * lw_pp_at(t, BEF_WD) + wd_scheduled_pp(t)
    return wd_scheduled_pp(t)


def wd_guar_pp(t):
    """min(G(t), LW(t)): the guaranteed portion of month t's withdrawal.

    A withdrawal is applied **first** against the guaranteed annual amount; that portion
    reduces the account value dollar for dollar and leaves the benefit base and the
    income amount unchanged [S9]. The two operands are read in ``FIA_US_S``'s order, each
    into a local first, so that compiled, where a two-argument ``min`` evaluates right to
    left, a point both refuse raises the first's message, as in modelx.
    """
    wd = wd_pp(t)
    lw = lw_pp_at(t, BEF_WD)
    return min(wd, lw)


def wd_excess_pp(t):
    """E(t) = max(0, G(t) - LW(t)): the **excess withdrawal** in month t.

    The quantity that permanently reduces the guarantee, and that destroys it entirely if
    it exhausts the account value [S1][S5][S9].  Note this is *not* the chassis's
    ``wd_excess_pp``, which is the amount exposed to the surrender charge; that is
    :func:`wd_charge_base_pp` here.  Before exercise ``LW`` is zero, so the whole
    withdrawal is an excess.
    """
    return max(0.0, wd_pp(t) - lw_pp_at(t, BEF_WD))


def wd_unfunded_pp(t):
    """The part of G(t) that neither the account value nor the guarantee pays.

    ``G(t) - min(G(t), max(0, AV(2)(t)))`` in a month whose closing phase is
    ``TERMINATED``; zero everywhere else.  **The two exhaustion branches are not
    symmetric, and this is where they part.**  In ``DEPLETED`` the account value is gone
    but the guarantee is alive, so the insurer pays ``LW`` from its own funds for the
    rest of the covered life [S1][S3][S9][R1] and nothing is unfunded.  On the
    ``TERMINATED`` branch the account value is driven to zero by an excess withdrawal, a
    surrender charge or a negative MVA, and "an account value run to zero by an excess
    withdrawal loses the guarantee entirely" [S1][S5][S9] — [S5] is explicit that the
    contract "as well as the rider will be considered Surrendered".  Beyond the account
    value there is then nothing to pay from: no balance and no promise.  Paying the
    requested amount in full would honour the guarantee in the very year the withdrawal
    destroys it, which is the trap the notes' attribution test exists to avoid.

    The notes write step 4 as ``AV(5)(t) = AV(2)(t) - G(t)`` with no cap because they
    write it for the funded case.  The cap here is on the **payment**, not on the
    withdrawal: :func:`wd_pp` still carries the amount requested, so the excess still
    sets :func:`depletion_cause` and still drives ``rho`` to 1 and the benefit base to
    zero.  Only :func:`wd_payment_pp` and the three ledger lines are reduced. ``G(t)`` and
    ``AV(2)(t)`` are read in ``FIA_US_S``'s order, each into a local first
    (:func:`wd_guar_pp`).

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if phase(t) != TERMINATED:
        return 0.0
    wd = wd_pp(t)
    av = av_pp_at(t, BEF_WD)
    return wd - min(wd, max(0.0, av))


def wd_guar_paid_pp(t):
    """The guaranteed portion of month t's withdrawal that is actually paid.

    ``min(G, LW)`` less whatever of :func:`wd_unfunded_pp` the excess could not absorb.
    The account value funds the withdrawal in the order the notes compose it — the first
    ``LW`` dollars are the guaranteed portion and the remainder is the excess [S9] — so
    an under-funded withdrawal leaves the **excess** unpaid first and eats into the
    guaranteed portion only after that **[std]**, the notes being silent on a withdrawal
    the account value cannot fund.  Equal to :func:`wd_guar_pp` in every month except a
    terminating anniversary.
    """
    return max(0.0, wd_guar_pp(t) - max(0.0, wd_unfunded_pp(t) - wd_excess_pp(t)))


def wd_excess_paid_pp(t):
    """The excess portion of month t's withdrawal that is actually paid.

    ``max(0, E(t) - wd_unfunded_pp(t))``: the excess is the first thing an under-funded
    withdrawal loses, being the part with no promise behind it.  Equal to
    :func:`wd_excess_pp` in every month except a terminating anniversary.
    """
    return max(0.0, wd_excess_pp(t) - wd_unfunded_pp(t))


def wd_cum_pp(t):
    """Wcum(t): cumulative gross withdrawals from issue to the end of month t.

    A running total over months, though only the anniversary months add to it. It opens at
    :func:`t_entry` on the model point's :func:`wd_cum_pp_init`, the withdrawals taken
    before the valuation date, 0 on new business; ``FIA_US_S``'s counts from the month it
    enters a contract, from 0. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prior = wd_cum_pp(t - 1) if t > t_entry() else wd_cum_pp_init()
    return prior + wd_pp(t)


def free_wd_base(t):
    """The base of the free withdrawal amount: the AV opening the contract year of month t.

    10% of the account value at the anniversary that **opens** the contract year, available
    from contract year 1 and with no carry-forward [S1][S3][S5][S6][S9][S10]; the
    combination is **[std]**.  Fixing the base at a *known* prior value is what lets the
    chargeable amount be evaluated without a fixed point, and it is what makes the
    allowance a property of the contract year rather than of the month.
    """
    return av_pp_year_open(t)


def free_wd_allow(t):
    """FW(t) = 0.10 x AV(0): the free withdrawal amount for month t's contract year."""
    return free_wd_rate * free_wd_base(t)                            # noqa: F821


def wd_free_pp(t):
    """The free-allowance portion of the anniversary's withdrawal, the part of FW it uses.

    The chassis name for this quantity (``MYGA_US_S``, ``UL_US_S``,
    ``RILA_US_S``), so the library spells the free-allowance portion
    of a withdrawal one way everywhere.  Zero away from the anniversary, where no
    withdrawal is taken and the whole allowance therefore remains against a mid-year
    surrender.

    **A [std] choice the notes flag as open.** [S9] says only that withdrawals up to the
    annual benefit amount carry no charge "even if greater than the Free Withdrawal
    Amount"; it does not say whether they *exhaust* it.  The convention here — the
    guaranteed amount consumes the free amount — is the insurer-favourable reading and is
    what the worked example uses, leaving ``12,800.00 - 10,144.16 = 2,655.84`` against
    the surrender.  The alternative leaves the whole ``FW(t)`` available against the
    excess. The free amount and the withdrawal are read in ``FIA_US_S``'s order, each into a
    local first (:func:`wd_guar_pp`).

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    if phase_open(t) == INCOME:
        allow = free_wd_allow(t)
        lw = lw_pp_at(t, BEF_WD)
        return min(allow, lw)
    allow = free_wd_allow(t)
    wd = wd_pp(t)
    return min(allow, wd)


def free_wd_remain(t):
    """The free withdrawal amount left after the contract year's guaranteed withdrawal.

    The whole allowance away from an anniversary, where no withdrawal has been taken yet —
    which is what a mid-year surrender is charged against.
    """
    return free_wd_allow(t) - wd_free_pp(t)


def wd_charge_base_pp(t):
    """X(t): the part of month t's withdrawal exposed to charge, clawback and MVA.

    ``max(0, G(t) - FW(t))`` before exercise and ``max(0, E(t) - remaining free)`` after
    it **[std]** — withdrawals up to ``LW`` carry no surrender charge, no MVA and no
    bonus clawback **even when LW exceeds the free withdrawal amount** [S9].  Zero
    once the account value is gone: post-depletion income is not a chargeable withdrawal.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:                 # noqa: F821
        return 0.0
    if opening == INCOME:                                            # noqa: F821
        return max(0.0, wd_excess_pp(t) - free_wd_remain(t))
    return max(0.0, wd_pp(t) - free_wd_allow(t))


def surr_charge_base_pp(t):
    """X(t) at a **full surrender** in month t: ``AV(t)`` less the free amount left.

    The chassis calls this ``surr_excess_pp``; renamed here only for symmetry with
    :func:`wd_charge_base_pp`, because ``E(t)`` already names a different quantity in
    these notes.  The construction is the chassis's and the source is the same [S10].

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if phase(t) == DEPLETED:                                         # noqa: F821
        return 0.0
    return max(0.0, av_pp(t) - free_wd_remain(t))


def bonus_factor():
    """b/(1+b): the factor that strips the bonus out of a bonus-inclusive account value.

    **The clawback factor is b/(1+b), not b** [S10] — the account value already contains
    the bonus, so using ``b`` over-recovers by ``(1+b)``.
    """
    return bonus_rate() / (1.0 + bonus_rate())


def mva_ref_yield(y):
    """i_y: the MVA reference index level at anniversary ``y``, from the scenario table.

    **Keyed by anniversary number**, like :func:`index_level`, so the level in force at a
    transaction closing the contract year of month ``t`` is
    ``mva_ref_yield(duration(t) + 1)``.  A declared investment-grade corporate bond yield
    index; generic here **[std]**, and named as Barclays US Credit Index in the
    linear-form products [S6][S7].
    """
    return scenario_value(y, MVA_REF_YIELD)


def mva_term(t):
    """n/12: the years remaining in the MVA period at the end of month t.

    The MVA period is the ten-year surrender charge period [S7][S10], and the notes state
    the term in **months** — which is what the monthly grid can now say exactly:
    ``surr_charge_period - (duration_mth(t) + 1)/12``, on the policy clock, a transaction in
    month ``t`` being settled at its end. At the worked example's anniversary 8 — policy
    month 95, the close of contract year 8, which is ``t = 11`` on the anchor in force at
    anniversary 7 — that is ``10 - 96/12 = 2`` years, the ``n = 24`` months the notes quote,
    so every anniversary value is the annual grid's; a surrender six months earlier now
    carries the 30 months it actually has instead of being rounded to the anniversary. The
    remaining term reaches zero at anniversary 10, so a transaction carries a live
    adjustment through contract year 9, and none at anniversary 10 itself; a surrender
    earlier in contract year 10 carries the months left.

    0.0 outside cover. ``FIA_US_S`` writes ``(t + 1)/12``, its ``t`` being the policy month.
    """
    if not is_active(t):
        return 0.0
    return max(0.0, surr_charge_period - (duration_mth(t) + 1) / 12.0)  # noqa: F821


def mva_in_force(t):
    """Whether an MVA applies to a transaction in month t.

    ``MVA = 0`` outside the MVA period and on the death benefit [S5][S6][S7][S10]; the
    second is handled where the death benefit is valued.
    """
    return mva_term(t) > 0.0


def mva_rate(t):
    """The market value adjustment rate, ``[(1+i0)/(1+it)]^(n/12) - 1`` [S10].

    Signed, and **negative when the reference yield has risen** [S10].  This is the
    ratio-of-yield-factors family, which is naturally bounded; the linear family
    ``(i0 - it) x T`` adopted by the fixed-deferred chassis [S6][S7] is unbounded and
    must be collared separately.  The FIA composite **restates** the MVA rather than
    inheriting it, which is why the chassis's ``mva_family`` switch is absent here.

    The reference yield is read at the anniversary **closing** the contract year of month
    ``t``, ``duration(t) + 1``, which is the transaction date the adjustment applies at.
    """
    if not mva_in_force(t):
        return 0.0
    return ((1.0 + mva_ref_yield_at_issue())
            / (1.0 + mva_ref_yield(duration(t) + 1))) ** mva_term(t) - 1.0


def is_collar_gross():
    """Whether the MVA collar is measured on the gross withdrawal, ``mva_collar_basis``
    ``GROSS``.

    A decode of the Reference, an int code, ``GROSS`` 0 or ``SURRENDER_VALUE`` 1, where
    ``FIA_US_S`` holds ``"gross"`` or ``"surrender_value"``, as :func:`is_step_up_annual`
    is, read by :func:`wd_mva_pp` and :func:`mva_pp`. Set ``mva_collar_basis`` before the
    model computes anything.
    """
    return bool(mva_collar_basis == GROSS)


def is_collar_surrender_value():
    """Whether the MVA collar is measured on the account value, ``mva_collar_basis``
    ``SURRENDER_VALUE``.

    The other decode of the Reference (:func:`is_collar_gross`): a basis that is neither
    raises in :func:`wd_mva_pp` and :func:`mva_pp`, as in ``FIA_US_S``'s ``mva_pp_on``.
    """
    return bool(mva_collar_basis == SURRENDER_VALUE)


def wd_charge_pp(t):
    """SC(t) on month t's withdrawal: ``sc(t) x X(t)`` [S5][S10]."""
    return surr_charge_rate(t) * wd_charge_base_pp(t)


def wd_clawback_pp(t):
    """CB(t) on month t's withdrawal [S10].

    ``(1 - v(t)) x [b/(1+b)] x X(t)`` on the chargeable amount, :func:`wd_charge_base_pp`:
    ``FIA_US_S``'s ``bonus_clawback_on``, a cell of float parameters, written inline here,
    with its arguments evaluated in its order and its expression unchanged, so that the
    value is its bit for bit and no projection cell passes a float to a cell (R14).
    """
    base = wd_charge_base_pp(t)
    vested = vest_rate(t)
    bonus = bonus_rate()
    return (1.0 - vested) * (bonus / (1.0 + bonus)) * base


def wd_mva_pp(t):
    """MVA(t) on month t's withdrawal, collared [S10].

    The raw adjustment ``mva_rate(t) x X(t)`` on the chargeable amount,
    :func:`wd_charge_base_pp`, collared to ``+/- max(0, R - SC - CB - MGV)``, where
    ``R`` is the collar's reference, the gross withdrawal, :func:`wd_pp`, under
    ``mva_collar_basis`` ``GROSS`` and the account value under ``SURRENDER_VALUE``
    (:func:`is_collar_gross`, :func:`is_collar_surrender_value`), a basis that is
    neither raising: the MVA can neither take the payment below the guaranteed minimum
    nor lift it above what the contract holds. ``FIA_US_S``'s ``mva_pp_on`` and the
    clawback inside it, cells of float parameters, written inline here, their cells
    evaluated in their order and their arithmetic in its association, so that the value
    is theirs bit for bit and no projection cell passes a float to a cell (R14).
    """
    base = wd_charge_base_pp(t)
    gross = wd_pp(t)
    raw = mva_rate(t) * base
    if is_collar_gross():
        reference = gross
    elif is_collar_surrender_value():
        reference = av_pp(t)
    else:
        raise ValueError("invalid mva_collar_basis")
    charge = surr_charge_rate(t) * base
    vested = vest_rate(t)
    bonus = bonus_rate()
    floor = mgsv_pp(t)
    limit = max(0.0, reference - charge - (1.0 - vested) * (bonus / (1.0 + bonus)) * base
                - floor)
    return max(-limit, min(limit, raw))


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``G - unfunded - SC - CB + MVA``.

    The surrender charge and the clawback are **internal transfers** within the account
    value, not fee income: the account value falls by the *gross* ``G(t)`` while the
    holder receives this.  Reporting them as income while also projecting the account
    value net of them double-counts.

    :func:`wd_unfunded_pp` is zero in every month except a terminating anniversary, where
    it strips out the part of the request the account value could not fund and the
    destroyed guarantee does not cover.  On the ``DEPLETED`` branch it stays zero and the
    whole of ``LW`` is paid, which is the guarantee.
    """
    return (wd_pp(t) - wd_unfunded_pp(t) - wd_charge_pp(t)
            - wd_clawback_pp(t) + wd_mva_pp(t))


def wd_reduction_rate(t):
    """rho(t): the proportional reduction applied to BB, LW and RB in month t.

    Pre-exercise the denominator is the gross account value after the rider charge;
    post-exercise it is that value **net of the guaranteed amount** [S9].  Zero when
    there is no excess: a withdrawal inside ``LW`` leaves the guarantee untouched, and 1
    where the denominator is 0 or less.

    ``FIA_US_S``'s ``wd_reduction_rate_on``, a cell of float parameters, written inline,
    its arguments read in its order, so that the value is its bit for bit and no projection
    cell passes a float to a cell (R14). Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = phase_open(t)
    if opening == DEPLETED or opening == TERMINATED:
        return 0.0
    av = av_pp_at(t, BEF_WD)
    if opening == INCOME:
        lw = lw_pp_at(t, BEF_WD)
    else:
        lw = 0.0
    gross = wd_pp(t)
    excess = max(0.0, gross - lw)
    if excess <= 0.0:
        return 0.0
    denom = av - lw
    if denom <= 0.0:
        return 1.0
    return min(1.0, excess / denom)


def surr_charge_pp(t):
    """SC(t) on a full surrender in month t."""
    return surr_charge_rate(t) * surr_charge_base_pp(t)


def surr_clawback_pp(t):
    """CB(t) on a full surrender closing month t [S10].

    ``(1 - v(t)) x [b/(1+b)] x X(t)`` on the chargeable amount, :func:`surr_charge_base_pp`:
    ``FIA_US_S``'s ``bonus_clawback_on``, a cell of float parameters, written inline here,
    with its arguments evaluated in its order and its expression unchanged, so that the
    value is its bit for bit and no projection cell passes a float to a cell (R14).
    """
    base = surr_charge_base_pp(t)
    vested = vest_rate(t)
    bonus = bonus_rate()
    return (1.0 - vested) * (bonus / (1.0 + bonus)) * base


def mva_pp(t):
    """MVA(t) on a full surrender closing month t, collared [S10].

    The raw adjustment ``mva_rate(t) x X(t)`` on the chargeable amount,
    :func:`surr_charge_base_pp`, collared to ``+/- max(0, R - SC - CB - MGV)``, where
    ``R`` is the collar's reference, the account value, :func:`av_pp`, under either
    ``mva_collar_basis``, ``GROSS`` or ``SURRENDER_VALUE``, the gross amount of a
    surrender being the account value (:func:`is_collar_gross`,
    :func:`is_collar_surrender_value`), a basis that is neither raising: the MVA can neither
    take the payment below the guaranteed minimum nor lift it above what the contract holds.
    ``FIA_US_S``'s ``mva_pp_on`` and the clawback inside it, cells of float parameters,
    written inline here, their cells evaluated in their order and their arithmetic in its
    association, so that the value is theirs bit for bit and no projection cell passes a
    float to a cell (R14).
    """
    base = surr_charge_base_pp(t)
    gross = av_pp(t)
    raw = mva_rate(t) * base
    if is_collar_gross():
        reference = gross
    elif is_collar_surrender_value():
        reference = av_pp(t)
    else:
        raise ValueError("invalid mva_collar_basis")
    charge = surr_charge_rate(t) * base
    vested = vest_rate(t)
    bonus = bonus_rate()
    floor = mgsv_pp(t)
    limit = max(0.0, reference - charge - (1.0 - vested) * (bonus / (1.0 + bonus)) * base
                - floor)
    return max(-limit, min(limit, raw))


def surr_value_pp(t):
    """The surrender value before the nonforfeiture floor, ``AV - SC - CB + MVA``.

    The composition order is **account value, then charge and clawback and MVA computed
    on the pre-deduction excess, then the floor** — the chassis's order, and the one
    contractual element the FIA notes inherit rather than restate.
    """
    if phase(t) == DEPLETED:                                         # noqa: F821
        return 0.0
    return (av_pp(t) - surr_charge_pp(t) - surr_clawback_pp(t) + mva_pp(t))


def surr_benefit_pp(t):
    """CSV(t) = max(AV - SC - CB + MVA, MGV): the surrender benefit paid [S1][S6][S10].

    Zero in ``DEPLETED``: there is no account value and no surrender value [S1][S9].  A
    binding floor is **not** a separate cash flow — it raises the benefit, and
    ``MGV - SV`` is a reconciliation quantity only. The two operands are read in
    ``FIA_US_S``'s order, each into a local first (:func:`wd_guar_pp`).
    """
    if phase(t) == DEPLETED:
        return 0.0
    value = surr_value_pp(t)
    floor = mgsv_pp(t)
    return max(value, floor)


def mgsv_charge_pp(t):
    """The annual contract charge deducted from the Model #805 floor, at the anniversary.

    Model #805 4.A permits $50 a year, accumulated at the nonforfeiture rate, together
    with premium tax actually paid and indebtedness [R2].  All are zero here **[std]**
    because no retrieved product declares an actual annual policy fee, which makes the
    modeled floor slightly conservative.

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    return mgsv_annual_charge                                        # noqa: F821


def prem_to_mgsv_pp(t):
    """The consideration credited to the Model #805 floor per contract, in the issue month.

    87.5% of the single premium **excluding the bonus** [S10][R2],
    ``net_consideration_ratio x P``, in the month whose ``duration_mth(t)`` is 0, and 0 in
    every other: the floor's issue value, which ``FIA_US_S``'s ``mgsv_pp_init()`` computes
    when its column is blank, credited in the issue month instead, as :func:`prem_to_av_pp`
    credits the account value's. :func:`mgsv_pp` adds it to the opening before the month's
    accrual.
    """
    if duration_mth(t) == 0:
        return net_consideration_ratio * premium_pp()                # noqa: F821
    return 0.0


def mgsv_pp(t):
    """MGV(t): the Model #805 guaranteed minimum value closing **month** t.

    The floor accretes every month at ``(1 + i_nf)^(1/12) - 1``, so twelve months compound
    to exactly the annual nonforfeiture rate and the anniversary values are the annual
    grid's; the withdrawal is deducted at the anniversary, where it is taken.  **Accrete,
    then deduct** — the worked example pins the ordering at
    ``93,811.84 x 1.01 - 10,144.16 = 84,605.80``.  The fixed-deferred chassis deducts and
    *then* accretes; the two are different arithmetic on the same concept, which is exactly
    what that file warns against carrying across.

    Accruing monthly rather than once at the anniversary is what makes the floor mean
    something for a mid-year death or surrender, which is where it most often binds. It
    opens at :func:`t_entry` on :func:`mgsv_pp_init`, the floor in force at the valuation
    date, and in the issue month the consideration :func:`prem_to_mgsv_pp`, ``0.875 x P``
    excluding the bonus [S10][R2], comes on top, both written inline, so that the floor's
    chain runs one cell a month. ``rider_charge_from_mgsv`` switches on the treatment
    documented at two carriers, one deducting the rider charge from the floor and the other
    its allocation charge [S1][S2][S3][S4]; the composite does not **[std]**.

    0.0 outside cover. A ``mgsv_rate`` below -1 raises, naming the point: its power has a
    negative base, a complex number in Python, where ``FIA_US_S`` raises ``TypeError`` at
    the floor's ``max``, and NaN in C, where that ``max`` would answer 0. At exactly -1 the
    floor accretes to 0.
    """
    if not is_active(t):
        return 0.0
    if 1.0 + mgsv_rate < 0.0:
        raise ValueError(f"point_id {point_id()}: mgsv_rate must be -1 or more, not "
                         f"{mgsv_rate}")
    opening = (mgsv_pp(t - 1) if t > t_entry() else mgsv_pp_init()) + prem_to_mgsv_pp(t)
    accrued = opening * (1.0 + mgsv_rate) ** (1.0 / 12.0)
    if not is_anniv(t):
        return max(0.0, accrued)
    charge = rider_charge_pp(t) if rider_charge_from_mgsv else 0.0
    return max(0.0, accrued - wd_pp(t) - mgsv_charge_pp(t) - charge)


def mgsv_rate_statutory(cmt5, option_cost):
    """The Model #805 4.B/4.C indexed nonforfeiture rate [R2][R3].

    ``max(0.0015, min(0.03, round(CMT5 to 1/20 of 1%) - 0.0125 - delta))`` where
    ``delta`` is the equity-index reduction of 4.C: available only when the annualized
    option cost of the **guaranteed** index features is at least 25 basis points, and
    then equal to ``min(100 bp, option cost)``, certified annually [R3].

    Two traps the notes name.  **The 4.B floor is 15 basis points, not 1%** — the
    composite's 1.00% is a **[std]** pick inside the 0.15%-3% corridor, not the statutory
    floor.  And whether the 15 bp floor survives the 4.C reduction is not stated in the
    retrieved text [unverified]; the specimen contract language, "the interest rates will
    range between 0.15% and 3%", suggests it does [S10], which is the reading
    implemented.  The statute *defines the minimum*: the contract rate must satisfy
    ``mgsv_rate >= mgsv_rate_statutory(...)``, which is what
    :func:`mgsv_rate_is_compliant` tests, not the reverse inequality.

    ``FIA_US_S``'s formula, ``math.floor`` included, kept for a user checking a contract
    rate against the statute and for the comparison with ``FIA_US_S``: an engine cell (the
    Space docstring's *Reporting cells*), which no projection cell calls. A step of 0 is
    refused before it divides, with Python's own message, ``float division by zero``, which
    compiled code would otherwise word differently.
    """
    delta = (min(mgsv_stat_delta_max, option_cost)
             if option_cost >= mgsv_stat_delta_gate else 0.0)
    step = mgsv_stat_step
    if step == 0.0:
        raise ZeroDivisionError("float division by zero")
    rounded = math.floor(cmt5 / step + 0.5) * step                   # noqa: F821
    return max(mgsv_stat_floor, min(mgsv_stat_cap, rounded - mgsv_stat_spread - delta))


def mgsv_rate_is_compliant(cmt5, option_cost):
    """True when the contract nonforfeiture rate meets the statutory minimum [R2][R3].

    An engine cell, as :func:`mgsv_rate_statutory` is, its one caller.
    """
    return mgsv_rate >= mgsv_rate_statutory(cmt5, option_cost)       # noqa: F821


def mort_rate_base_at(a):
    """The table's annual mortality rate at attained age ``a`` and the model point's sex.

    ``Data.mort_table_array`` at the row :func:`mort_schedule` gives the point's ``sex``
    and the column of age ``a``, the table's one reader, keyed by the age; :func:`mort_rate`
    calls it in cover only, at :func:`age`. ``Data`` refuses a point whose sex the table
    lacks, or whose attained age in its first month on the books it gives no rate at, and
    :func:`proj_len` one whose sex's rates stop below ``maturity_age``. An age outside the
    sex's rates, which no projection reads, raises ``ValueError`` naming the point, where
    ``FIA_US_S``'s lookup raised ``KeyError``; so does one outside the ages the array holds,
    from the table's first, or 0 if that is lower, to ``Data.read_last_age``, 122.
    """
    s = mort_schedule()
    if a < data.mort_age_firsts()[s] or a > data.mort_age_lasts()[s]:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: the mortality table gives no rate at "
                         f"attained age {a}")
    base = data.mort_age_base()                                      # noqa: F821
    if a < base or a > data.mort_age_held():                         # noqa: F821
        raise ValueError(f"point_id {point_id()}: the mortality table is held from age "
                         f"{base} to {data.mort_age_held()}, Data.read_last_age, and no "
                         f"projection reads age {a}")
    return float(data.mort_table_array()[s, a - base])               # noqa: F821


def mort_rate(t):
    """q(t): the **annual** mortality rate of the contract year containing month t.

    Read at ``age(t)``, the attained age opening that contract year — the library convention
    of :mod:`.Term_US_S` and :mod:`.MYGA_US_S`. The rate actually applied to a month is
    :func:`mort_rate_mth`; this cell stays annual so the table is read the way it is
    published and so the assumption is visible at the frequency it is set at.

    The shipped table is the same illustrative Makeham annuitant curve as
    ``products/fixed_deferred_annuity`` **[std]**, *not* a published basis. The prescribed
    basis is the 2012 IAM Basic / 2012 IAR generational family with Projection Scale G2,
    ``q_x^(2012+n) = q_x^(2012) x (1 - G2_x)^n``, rounding applied from the 2012 period rate
    each time and never by compounding an already rounded rate [REG-R59][REG-R60]; it may
    not be redistributed here, so swap it in by repointing ``Data.mort_table_file`` before
    the model computes anything. Generational projection is **not implemented** for the same
    reason. ``mort_ae_factor`` carries the A/E deviation, 100% **[std]** against the
    2020-2024 payout experience study [REG-R61]; the spelling is the library's shared one,
    so the A/E factor reads the same in every model that has one.

    The table's rate is read at :func:`mort_rate_base_at`, and capped at 1 as ``FIA_US_S``
    caps it, the bound second, ``min(q, 1.0)``, so that a NaN stays NaN rather than reading
    as certain death. ``Data`` refuses a blank rate in any case. At the shipped A/E of 100%
    the capped rate is the table's at every age, 1.0 at 120. 0.0 outside cover, before the
    table is read.
    """
    if not is_active(t):
        return 0.0
    return min(mort_ae_factor * mort_rate_base_at(age(t)), 1.0)      # noqa: F821


def mort_rate_mth(t):
    """The monthly mortality rate, ``1 - (1 - q)^(1/12)``.

    The uniform-force conversion the library uses everywhere: twelve of these compound to
    exactly the annual rate of the contract year, so the anniversary in-force numbers are
    the annual grid's and only their distribution through the year changes.  Dividing by
    twelve instead would overstate the decrement, and the error grows with the rate.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def shock_lapse_rate(t):
    """w_shock: the surrender rate in the year the surrender charge expires [R8].

    **The single most important behavioral fact in the product.** 33% without a GLWB
    rider against 10% with one in force but not activated, and 5% **[std]** once it is
    activated, extrapolated from the finding that contracts with GLWBs lapse less than
    those without and that activated GLWBs lapse least [R1][R8].  Applying a plain
    fixed-deferred shock lapse — roughly 52%-56% for fixed-rate deferred annuities
    [REG-R63, unverified] — to an FIA with an in-force rider materially understates the
    tail the product is sold for.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if not glwb_elected() or not rider_in_force_open(t):
        return shock_lapse_no_rider                                  # noqa: F821
    if phase_open(t) == ACCUM:                                       # noqa: F821
        return shock_lapse_rider_idle                                # noqa: F821
    return shock_lapse_rider_active                                  # noqa: F821


def lapse_rate_base(t):
    """w_base(t): the base annual surrender rate of month t's contract year **[std]**.

    2% in years 1-3, 3% in 4-6, 4% in 7-9, 5% in year 10, the shock in the year the
    surrender charge expires, and 6% thereafter — the shape [R1] describes: low early,
    rising through the charge period, spiking at expiry, then falling back but staying
    above pre-shock levels.  The notes' separate ``M_shock`` multiplier is absorbed here,
    because the shock is stated as an absolute rate rather than as a factor on the
    ultimate; see the Space docstring.

    Zero outside cover, where no contract year is the contract's.
    """
    if not is_active(t):
        return 0.0
    year = policy_year(t)
    if year == surr_charge_period + 1:                               # noqa: F821
        return shock_lapse_rate(t)
    if year <= 3:
        return lapse_base_early                                      # noqa: F821
    if year <= 6:
        return lapse_base_mid                                        # noqa: F821
    if year <= 9:
        return lapse_base_late                                       # noqa: F821
    if year <= surr_charge_period:                                   # noqa: F821
        return lapse_base_final                                      # noqa: F821
    return lapse_base_ult                                            # noqa: F821


def lapse_moneyness_factor(t):
    """M_money(t) = clamp(1 - 0.6 max(0, BB/AV - 1), 0.2, 1.0) **[std]**.

    Surrender is suppressed when the guarantee is in the money, because a rational
    surrender destroys a guarantee worth ``BB - AV`` in benefit-base terms.  The observed
    direction is documented [R1][R8]; the functional form is not.

    Evaluated on the state **closing the contract year**, at :func:`anniv_mth`, so the
    factor is a property of the year like the base rate it multiplies.  Reading it month
    by month would let the fixed-account accrual drift the ratio within the year and make
    the annual surrender assumption depend on where in the year it is sampled.

    :func:`anniv_mth` lies at most 11 months after ``t``, inside the frame, and the account
    value and the benefit base read there depend on no count and on nothing after that
    anniversary, so the read opens no chain past it. 1.0 outside cover, no adjustment, where
    ``FIA_US_S`` has no guard and would read a month past the frame.
    """
    if not is_active(t):
        return 1.0
    a = anniv_mth(t)
    av = av_pp(a)
    if av <= 0.0:
        return lapse_money_floor                                     # noqa: F821
    ratio = benefit_base_pp(a) / av
    return min(1.0, max(lapse_money_floor,                           # noqa: F821
                        1.0 - lapse_money_slope * max(0.0, ratio - 1.0)))  # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** surrender rate of the contract year containing month t.

    ``min(0.35, w_base(t) x M_money(t))``, and **zero in DEPLETED** — with no account
    value there is nothing to surrender, so lapse is impossible [S1][S9] and leaving the
    decrement on would silently truncate the most expensive part of the liability.  In
    the contract year the contract terminates, the survivors leave as a deemed full
    surrender [S5][S9], so this returns 1.0 there and the in-force roll-forward closes.

    Evaluated on the phase **closing** the contract year, at :func:`anniv_mth`, so it is
    one rate for the whole year; :func:`lapse_rate_mth` is what a month actually applies.

    :func:`anniv_mth` lies at most 11 months after ``t``, inside the frame; the phase read
    there depends on no count and on nothing after that anniversary. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    a = anniv_mth(t)
    if phase_open(a) == TERMINATED:                                  # noqa: F821
        return 0.0
    closing = phase(a)
    if closing == TERMINATED:                                        # noqa: F821
        return 1.0
    if closing == DEPLETED:                                          # noqa: F821
        return 0.0
    return min(lapse_rate_max,                                       # noqa: F821
               lapse_rate_base(t) * lapse_moneyness_factor(t))


def lapse_rate_mth(t):
    """The monthly surrender rate, ``1 - (1 - w)^(1/12)``.

    The same uniform-force conversion as :func:`mort_rate_mth`, so twelve months compound
    to exactly the contract year's annual rate — including the shock in the year the
    surrender charge expires, which **is** spread.  That is deliberate and is the opposite
    of :mod:`.Term_US_S`, where the notes state the shock as a rate "applied in full at
    the end of the final level-period month": here the notes state it as the surrender
    rate *of contract year 11*, a year that carries no surrender charge in any month, so
    there is no contractual date inside it for the decision to cluster on.

    The one rate that is **not** spread is the deemed full surrender at termination.  That
    is a contractual event, not a behavioral assumption: the contract "as well as the
    rider will be considered Surrendered" [S5] at the anniversary the account value is
    destroyed, so the survivors leave in that month and not before.
    """
    w = lapse_rate(t)
    if w >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - w) ** (1.0 / 12.0)


def pols_if(t):
    """The in-force count at the **start** of month t, the weight of row t.

    ``pols_if_at(t, BEF_DECR)``: the count carried in from month t - 1 plus month t's new
    business, before month t's decrements. The library convention, set by
    :mod:`.Term_US_S` and ``savings.CashValue_SE``: it is the weight carried by every cash
    flow reported on the same row of :func:`result_cf`. At an anniversary month it is the
    count that reaches the anniversary and therefore the weight the year's withdrawal and
    charges carry — on the annual grid that weight was the count entering the year, which is
    the one place the finer grid changes the answer rather than only the resolution.

    A point in force at the valuation date opens with :func:`pols_if_init`, and one issued
    at or after it with its issued count in the issue month; on a point issued at ``t = 0``
    this is exactly ``FIA_US_S``'s ``pols_if``. Death comes before surrender **[std]**. Zero
    outside cover: before issue, and from ``t = proj_len()`` on, where the survivors of the
    last covered month have left through :func:`pols_maturity`. Because the monthly rates
    compound to the annual ones, ``pols_if`` in the month opening a contract year is exactly
    the annual-grid model's count there: the notes' ``l(k)``. It is
    ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is the count
    before maturity.
    """
    return pols_if_at(t, BEF_DECR)


def pols_new_biz(t):
    """Number of contracts issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point issued
    at the valuation date, ``t = k`` for one issued ``k`` months later. A point already in
    force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_if_at(t, timing):
    """In-force in month t read at the point given by ``timing``.

    The timings in processing order:

    ``BEF_NB``
        the count carried in from month t - 1, before month t's new business: the survivors
        of month t - 1's deaths and surrenders, out of month t - 1's ``BEF_DECR`` count.
        At :func:`t_entry`, the first month on the books, it is :func:`pols_if_init`, the
        count in force at the valuation date (0 for a point issued at or after it), and the
        recursion reads no earlier month. Zero outside cover, so the survivors of the last
        covered month leave as :func:`pols_maturity`.
    ``BEF_DECR``
        ``BEF_NB`` plus :func:`pols_new_biz`, before any decrement; the same number as
        :func:`pols_if`, and the weight on that month's cash flows.
    ``BEF_MORT``
        the same count: this product has no annuitization decrement, so the chassis's two
        timings coincide.
    ``BEF_LAPSE``
        after that month's deaths.
    ``AFT_DECR``
        after its surrenders, the count at the *end* of month t, which is
        ``pols_if_at(t + 1, BEF_NB)`` in every month but the last covered one, where
        :func:`pols_maturity` takes it out.

    Both decrements are the **monthly** rates, death before surrender **[std]**.
    ``BEF_NB`` and ``BEF_DECR`` are ``basiclife.BasicTerm_SE``'s names, and any timing
    but these five raises. ``BEF_NB`` forms the count left at the end of month t - 1
    itself — month t - 1's ``BEF_NB`` plus its :func:`pols_new_biz`, after its two
    decrements, the products ``AFT_DECR`` takes in the order it takes them — rather than
    calling for it. So the chain of calls from month t back to :func:`t_entry` is one cell a
    month, where ``FIA_US_S``'s ran through two. Every count is zero outside cover, before
    any rate is read.
    """
    if timing == BEF_NB:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1))
                * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1)))
    elif timing == BEF_DECR or timing == BEF_MORT:
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)
    elif timing == BEF_LAPSE or timing == AFT_DECR:
        if not is_active(t):
            return 0.0
        pols = pols_if_at(t, BEF_DECR) * (1.0 - mort_rate_mth(t))
        if timing == BEF_LAPSE:
            return pols
        return pols * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Deaths in month t, on the monthly mortality rate.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_MORT) * mort_rate_mth(t)


def pols_lapse(t):
    """Full surrenders in month t, on the survivors of that month's mortality.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_LAPSE) * lapse_rate_mth(t)


def pols_maturity(t):
    """Survivors leaving at the projection horizon, non-zero only in the last covered month.

    That month is ``duration_mth(t) = maturity_mth() - 1``, the frame's last row,
    ``t = proj_len() - 1``. Not a decrement — the horizon runs out — but needed for the
    in-force roll-forward to close. Numerically zero under the shipped mortality table,
    whose annual rate reaches 1.000000 at age 120, hence a monthly rate of 1.0, so the
    projection closes itself; see the Space docstring.
    """
    if duration_mth(t) != maturity_mth() - 1:
        return 0.0
    return pols_if_at(t, AFT_DECR)


def pols_decr(t, kind):
    """The number of contracts leaving in month t by benefit ``kind``."""
    if kind == DEATH:
        return pols_death(t)
    elif kind == LAPSE:
        return pols_lapse(t)
    elif kind == MATURITY:
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def claim_pp(t, kind):
    """The benefit paid per contract at the end of month t by ``kind``.

    ``DEATH`` is ``max(AV(t), MGV(t))`` with 100% bonus vesting, no surrender charge
    and no MVA [S1][S2][S5][S10], and is never below the cash surrender benefit [R2 6].
    Its two operands are read in ``FIA_US_S``'s order, each into a local first
    (:func:`wd_guar_pp`).
    Note the FIA composite **restates** this rather than inheriting the chassis's full
    account value floored at the surrender benefit.  ``LAPSE`` is the surrender benefit.
    ``MATURITY`` is the account value floored at the guaranteed minimum at the horizon.
    All three are **zero in DEPLETED**: there is no account value, no surrender value and
    no death benefit, and the only exit is death [S1][S9].  Any other ``kind``, ``ALL``
    among them, raises ``ValueError("invalid kind")`` outside a ``DEPLETED`` month: the
    phase is read before the kind, as in ``FIA_US_S``, so in ``DEPLETED`` it answers 0.0.
    """
    if phase(t) == DEPLETED:
        return 0.0
    if kind == DEATH:
        av = av_pp(t)
        floor = mgsv_pp(t)
        return max(av, floor)
    elif kind == LAPSE:
        return surr_benefit_pp(t)
    elif kind == MATURITY:
        av = av_pp(t)
        floor = mgsv_pp(t)
        return max(av, floor)
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The account value released per contract by a claim of ``kind``.

    ``AV(t)`` for all three kinds; the difference from :func:`claim_pp` is
    :func:`claims_over_av`, positive when the Model #805 floor binds and negative when
    the surrender charge and a negative MVA bite. Any other ``kind``, ``ALL`` among them,
    raises ``ValueError("invalid kind")``, each kind compared by ``==``.
    """
    if kind == DEATH or kind == LAPSE or kind == MATURITY:
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single premium, at the **start** of the issue month.

    ``premium_pp() x pols_new_biz(t)``: there is no issue-instant row, so the premium is a
    beginning-of-month flow of the issue month, the one with ``duration_mth(t) = 0``, rather
    than a row of its own, and it is paid per contract issued. A point in force at the
    valuation date paid its premium before it, so this is zero throughout for it — as are
    the acquisition expense and the premium tax that key off it.
    """
    return premium_pp() * pols_new_biz(t)


def prem_to_av_pp(t):
    """Premium and bonus credited to the account value per contract, in the issue month.

    ``P x (1 + b)`` [S5] in the month whose ``duration_mth(t)`` is 0, and 0 in every other:
    the issue value ``FIA_US_S``'s ``av_pp_init()`` computes when its column is blank,
    credited in the issue month instead, where :func:`av_pp_at` adds it at ``BEF_INV``.
    Zero outside cover by its terms, no month outside cover being the issue month.
    """
    if duration_mth(t) == 0:
        return premium_pp() * (1.0 + bonus_rate())
    return 0.0


def prem_to_av(t):
    """Premium and bonus credited to the block's account value, in the issue month only.

    :func:`prem_to_av_pp` per contract issued, weighted by :func:`pols_new_biz`.
    """
    return prem_to_av_pp(t) * pols_new_biz(t)


def wd_guar(t):
    """Guaranteed withdrawal outgo in month t, weighted by ``pols_if(t)``.

    The count entering the month, which is the in-force number reported on the same row of
    :func:`result_cf`; at an anniversary that is the count which **reaches** it.
    On :func:`wd_guar_paid_pp`, not on the amount requested, so a terminating anniversary
    cannot pay a guaranteed withdrawal the account value could not fund and the destroyed
    rider no longer covers.  Zero in ``DEPLETED``, where the same payment is reported as
    :func:`income_payments` so the two lines partition the total rather than overlap.

    Zero outside cover.
    """
    if not is_active(t) or phase_open(t) == DEPLETED:                # noqa: F821
        return 0.0
    return wd_guar_paid_pp(t) * pols_if(t)


def wd_excess(t):
    """Excess withdrawal outgo in month t: ``E - unfunded - SC - CB + MVA``.

    Weighted by ``pols_if(t)``, the count entering the month, and on
    :func:`wd_excess_paid_pp`: the excess is the first part of an under-funded withdrawal to
    go unpaid.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    net = (wd_excess_paid_pp(t) - wd_charge_pp(t) - wd_clawback_pp(t) + wd_mva_pp(t))
    return net * pols_if(t)


def income_payments(t):
    """Post-depletion income outgo: ``LW`` at the anniversary while ``phase = DEPLETED``.

    **This is the guarantee.** There is no account value behind it, no rider charge is
    deducted, and it runs for the rest of the covered life [S1][S3][S9][R1].

    Annual like every other withdrawal, so it falls in the anniversary month and is
    weighted by the contracts that **reach** it.  Paying it in each of the twelve months
    would multiply the guarantee twelvefold and break the partition
    ``withdrawals = wd_guar + wd_excess + income_payments`` that :func:`result_cf`
    documents.

    Zero outside cover.
    """
    if not is_active(t) or not is_anniv(t):
        return 0.0
    if phase_open(t) != DEPLETED:                                    # noqa: F821
        return 0.0
    return lw_pp_at(t, BEF_WD) * pols_if(t)


def withdrawals(t):
    """Total withdrawal outgo in month t, ``wd_payment_pp(t) x pols_if(t)``.

    Equal to :func:`wd_guar` + :func:`wd_excess` + :func:`income_payments` in every
    month, the three lines partitioning it by the notes' ledger categories.  All
    four are published by :func:`result_cf`, so **summing every column of that frame
    double-counts the withdrawal**; the ledger identity is on the total, and the split is
    there because the notes report the three categories separately.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_payment_pp(t) * pols_if(t)


def claims(t, kind):
    """Benefit outgo in month t, for one ``kind`` or, with ``kind`` ``ALL``, all three.

    ``ALL`` is ``FIA_US_S``'s ``kind=None``: the three kinds added in its order, by its
    chain of ``+``, so that the total is its bit for bit, the sign of a zero included.
    """
    if kind == ALL:
        return claims(t, DEATH) + claims(t, LAPSE) + claims(t, MATURITY)
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The account value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind):
    """Benefit paid less the account value released, ``claims - claims_from_av``.

    Signed and a reconciliation quantity only: positive exactly when the Model #805 floor
    binds, negative when the surrender charge, the clawback and a negative MVA bite.  A
    binding floor does not add a top-up cash flow — it raises the benefit. ``ALL`` is the
    three kinds' total, as in :func:`claims`.
    """
    if kind == ALL:
        return (claims_over_av(t, DEATH) + claims_over_av(t, LAPSE)
                + claims_over_av(t, MATURITY))
    return claims(t, kind) - claims_from_av(t, kind)


def commissions(t):
    """Acquisition commission, **zero [std]**.

    The technical notes fold the whole acquisition cost into a single 6.0%-of-premium
    acquisition *expense* and give no separate commission, so ``comm_rate_acq`` is 0 and
    this line exists for shape only.  It is kept rather than dropped because every model
    in the library carries the same cash flow vocabulary.
    """
    return comm_rate_acq * premiums(t)                               # noqa: F821


def premium_taxes(t):
    """Premium tax on the single premium, 0% on the composite state basis **[std]**."""
    return premium_tax_rate * premiums(t)                            # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t, ``1.025^(t/12)``, on the valuation clock.

    ``t`` counts months from the valuation date, so the factor is 1 at the valuation date
    for every point, and maintenance expense is in valuation-date dollars, as
    ``basiclife.BasicTerm_SE`` inflates it: a contract issued later inflates from the
    valuation date, not from its issue, and one in force carries none of its years before
    it. ``FIA_US_S`` inflates from issue on its policy clock, so its in-force points,
    entered at policy month 84, carry ``1.025^7`` that this model's twins of them do not. A
    fractional power of the annual rate, so twelve months of it compound to exactly one year
    of inflation. An ``inflation_rate`` below -1 raises, naming the point: its power has a
    negative base, a complex number in Python, which ``FIA_US_S`` projects, and NaN in C.
    """
    if 1.0 + inflation_rate < 0.0:
        raise ValueError(f"point_id {point_id()}: inflation_rate must be -1 or more, not "
                         f"{inflation_rate}")
    return (1.0 + inflation_rate) ** (t / 12.0)


def expenses(t):
    """Insurer expenses: acquisition at issue and inflating maintenance monthly **[std]**.

    6.0% of the single premium in the issue month, per contract issued and uninflated, as
    ``basiclife.BasicTerm_SE`` charges acquisition, and $80 per contract per year inflating
    at 2.5% from the valuation date — **one twelfth of it a month**, weighted by the
    in-force at the start of the month. Spreading the maintenance charge is the point of the
    finer grid for this line: it is an insurer cost accruing continuously, not a contractual
    event tied to the anniversary, so it now falls where it is incurred and is weighted by
    survivors who have not yet left. ``premiums(t)`` is zero everywhere but the issue month,
    so the acquisition term simply drops out elsewhere. Both are standardizations: no
    retrieved document discloses FIA acquisition cost or per-contract maintenance.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return (expense_acq_rate * premiums(t)                           # noqa: F821
            + expense_maint / 12.0 * inflation_factor(t) * pols_if(t))  # noqa: F821


def net_cf(t):
    """Net cash flow in month t.

    The index credit, the rider charge, the surrender charge, the bonus clawback and the
    movement of the Model #805 floor are **internal accounting entries**: they drive the
    account value, the benefit base and the benefit *amount* but are never ledger lines
    of their own.  Only amounts paid to or received from the contract holder, and the
    insurer's own expenses, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t, ALL) - commissions(t) - expenses(t)
            - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted account value in month t; see :func:`av_pp_at`.

    Every timing inside the month carries ``pols_if(t)`` — the count entering it — because
    all processing happens before the decrements. ``EOY`` carries the count *leaving* the
    month, ``pols_if_at(t + 1, BEF_NB)``, the next month's count before its new business:
    zero at the horizon, where :func:`pols_maturity` has taken the survivors out.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    if timing == BEF_PREM or timing == BEF_INV or timing == BEF_FEE or timing == BEF_WD:
        return av_pp_at(t, timing) * pols_if(t)
    if timing == EOY:
        return av_pp(t) * pols_if_at(t + 1, BEF_NB)
    raise ValueError("invalid timing")


def inv_income(t):
    """Interest credited to the whole block in month t; zero outside cover."""
    if not is_active(t):
        return 0.0
    return inv_income_pp(t) * pols_if(t)


def rider_charges(t):
    """Rider charges deducted from the whole block's account value in month t.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return rider_charge_pp(t) * pols_if(t)


def wd_from_av(t):
    """The account value released by month t's withdrawals, gross of charge and MVA.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_pp(t) * pols_if(t)


def av_depletion(t):
    """The block's withdrawal outgo the account value could not fund in month t.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return av_depletion_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's account value over month t.

    Closing less **opening**, the opening being read at ``BEF_PREM`` so that the single
    premium of the issue month is a movement rather than part of the balance brought in; on
    a point in force at the valuation date the opening at ``t = 0`` is its block's account
    value entering month 0. Away from :func:`t_entry`, ``av_at(t, BEF_PREM)`` is exactly
    the previous month's closing value.
    """
    return av_at(t, EOY) - av_at(t, BEF_PREM)


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual for month t; the signed float.

    ``AV(t) - AV(0)(t) = premium in + interest credited - rider charges - withdrawals
    + the part of a withdrawal the account value could not fund - the account value
    released by each claim kind``.  The cash *paid* on a surrender may differ from the
    account value released — by the charge, the clawback, the MVA and any binding
    Model #805 floor — and that difference is :func:`claims_over_av`, deliberately not
    part of this identity.  It closes month by month on the finer grid, where the interest
    term is the month's accrual and the claim terms are that month's exits.

    The per-``t`` residual is kept because it is what a debugging session wants when
    :func:`check_av_roll_fwd` returns ``False``; the boolean is defined in terms of it.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    expected = (prem_to_av(t) + inv_income(t) - rider_charges(t) - wd_from_av(t)
                + av_depletion(t)
                - claims_from_av(t, DEATH) - claims_from_av(t, LAPSE)
                - claims_from_av(t, MATURITY))
    return av_change(t) - expected


def check_av_roll_fwd():
    """Check the account value roll-forward: ``True`` when it closes in every month.

    No argument and a bool, following ``savings.CashValue_SE`` and the rest of this library,
    so one test can call the same check across every model. The signed residual for a single
    month is :func:`check_av_roll_fwd_resid`, and this is
    ``abs(resid) <= check_tol_av x max(policy_count(), 1)`` over
    ``t = 0 .. proj_len() - 1``: the tolerance scales with the count, since the residual is
    rounding on that many contracts. On a point counting one contract it is ``FIA_US_S``'s
    absolute 1e-6, loose enough for an account value of order $100,000 accumulated over a
    century of months; it is not a modelling assumption. A residual that is not a number
    fails, as ``FIA_US_S``'s ``math.isclose`` fails it: the test is that the residual is
    within the tolerance, which no comparison with NaN is.
    """
    tol = check_tol_av * max(policy_count(), 1.0)                    # noqa: F821
    for t in range(proj_len()):
        if not abs(check_av_roll_fwd_resid(t)) <= tol:
            return False
    return True


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual for month t; the signed float.

    ``pols_if(t) - pols_if_at(t + 1, BEF_NB) = deaths + surrenders + horizon exits``: the
    start-of-month count opens the row, the exits are taken during it, and the next month
    opens on what is left, before its own new business. Zero to floating point for every
    ``t``, including the last, ``t = proj_len() - 1``, where the next month's count is zero
    and :func:`pols_maturity` carries the survivors out.

    Zero outside cover, before ``t + 1`` is read, as ``FIA_US_S`` guards it before its
    frame: so at ``t = proj_len()`` nothing reads a month past it.
    """
    if not is_active(t):
        return 0.0
    return (pols_if(t) - pols_if_at(t + 1, BEF_NB) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """Check the in-force roll-forward: ``True`` when it closes in every month.

    No argument and a bool, as for :func:`check_av_roll_fwd`; the signed residual for a
    single month is :func:`check_pols_roll_fwd_resid`. The tolerance is
    ``check_tol_pols x max(policy_count(), 1)``, 1e-12 on a point counting one contract,
    scaling with the count as the residual does. A residual that is not a number fails, as
    in :func:`check_av_roll_fwd`.
    """
    tol = check_tol_pols * max(policy_count(), 1.0)                  # noqa: F821
    for t in range(proj_len()):
        if not abs(check_pols_roll_fwd_resid(t)) <= tol:
            return False
    return True


def result_cf():
    """Result table of cashflows, one row per month ``t = 0 .. proj_len() - 1``.

    Row 0 is the valuation month for every model point, so the frames of a block line up and
    sum row by row, and a point issued after the valuation date has zeros until its issue
    month. There is **no issue-instant row**: the issue month's row carries the premium and
    the acquisition expense as beginning-of-month flows alongside that month's own activity.
    :func:`result_cf_annual` sums it into contract years.

    ``pols_if`` is the in-force count at the **start** of month ``t``, which is the weight
    every cash flow on the same row carries — dividing a row's cash flow by its per-contract
    amount returns this column exactly. Every withdrawal and benefit driven by the contract
    falls in an anniversary month, so those columns are zero in eleven rows out of twelve;
    deaths, surrenders and maintenance expense fall in every row.

    ``withdrawals`` is the library-wide column for partial withdrawal payments and is the
    total; the three columns after it — ``wd_guar``, ``wd_excess`` and ``income_payments`` —
    partition that total into the notes' own ledger categories. **They are published
    alongside it, not instead of it, so summing every column of the frame double-counts the
    withdrawal.** The columns are ``FIA_US_S``'s. ``net_cf`` is income-positive, as
    everywhere in this library.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "wd_guar": [wd_guar(t) for t in ts],
            "wd_excess": [wd_excess(t) for t in ts],
            "income_payments": [income_payments(t) for t in ts],
            "claims_death": [claims(t, DEATH) for t in ts],
            "claims_lapse": [claims(t, LAPSE) for t in ts],
            "claims_maturity": [claims(t, MATURITY) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, one row per month ``t = 0 .. proj_len() - 1``.

    ``pols_if`` opens the row and ``pols_if_aft_decr`` closes it; ``pols_new_biz``, second,
    is the month's new business, which ``pols_if`` holds. The two decrement columns are the
    **monthly** rates actually applied; the annual rates they are converted from are
    :func:`mort_rate` and :func:`lapse_rate`, constant across each contract year, and all
    four are 0 outside cover. The closing column is the next row's count before its new
    business in every month but the last, where :func:`pols_maturity` takes the survivors
    out and the projection stops. The identity ``check_pols_roll_fwd_resid`` asserts is
    therefore
    ``pols_if(t) - pols_if_at(t + 1, BEF_NB) = pols_death + pols_lapse + pols_maturity``.
    ``FIA_US_S``'s report, with ``pols_new_biz`` added.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, AFT_DECR) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the per-contract account value and surrender trace, by month.

    The first eight columns walk the worked example's account value rows, now month by
    month: ``fixed_interest_pp`` accrues in every row, ``index_credit_pp``,
    ``rider_charge_pp`` and ``wd_pp`` only in anniversary rows.  The rest are the surrender
    trace, available in **every month** rather than only at the anniversaries the notes
    tabulate — which is the reading a mid-year surrender needs.

    One row per month ``t = 0 .. proj_len() - 1``, with zeros outside cover.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_inv": [av_pp_at(t, BEF_INV) for t in ts],
            "credit_rate": [credit_rate(t) for t in ts],
            "index_credit_pp": [index_credit_pp(t) for t in ts],
            "fixed_interest_pp": [fixed_interest_pp(t) for t in ts],
            "rider_charge_pp": [rider_charge_pp(t) for t in ts],
            "av_pp_bef_wd": [av_pp_at(t, BEF_WD) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "mgsv_pp": [mgsv_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "surr_clawback_pp": [surr_clawback_pp(t) for t in ts],
            "mva_pp": [mva_pp(t) for t in ts],
            "surr_benefit_pp": [surr_benefit_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_glwb():
    """Result table of the GLWB rider state per contract, indexed by the month t.

    The benefit base is **notional** — no cash value, not withdrawable, not payable as a
    lump sum [S1][S9] — so none of these columns is a cash flow. They are the drivers of the
    rider charge, the lifetime withdrawal and, in the end, the post-depletion income. Every
    one of them is annual: the rider state is flat between anniversaries and steps at each
    one, so the rows of interest are the anniversary rows, those with
    ``duration_mth(t) % 12 == 11``.

    One row per month ``t = 0 .. proj_len() - 1``. The ``phase`` column holds the label of
    each month's phase code, ``ACCUM``, ``INCOME``, ``DEPLETED`` and ``TERMINATED`` as in
    ``FIA_US_S``, and ``PRE_ISSUE`` before issue: a report may hold text where every
    projection cell holds the code.
    """
    labels = {PRE_ISSUE: "PRE_ISSUE", ACCUM: "ACCUM", INCOME: "INCOME",  # noqa: F821
              DEPLETED: "DEPLETED", TERMINATED: "TERMINATED",        # noqa: F821
              MATURED: "MATURED"}                                    # noqa: F821
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "phase": [labels[phase(t)] for t in ts],
            "rollup_pp": [rollup_pp(t) for t in ts],
            "stack_pp": [stack_pp(t) for t in ts],
            "bb_pp_bef_step_up": [benefit_base_pp_at(t, BEF_STEP_UP) for t in ts],
            "benefit_base_pp": [benefit_base_pp(t) for t in ts],
            "rollup_base_pp": [rollup_base_pp(t) for t in ts],
            "lw_pp": [lw_pp(t) for t in ts],
            "free_wd_allow": [free_wd_allow(t) for t in ts],
            "wd_guar_pp": [wd_guar_pp(t) for t in ts],
            "wd_excess_pp": [wd_excess_pp(t) for t in ts],
            "wd_unfunded_pp": [wd_unfunded_pp(t) for t in ts],
            "wd_reduction_rate": [wd_reduction_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into contract years, indexed by ``policy_year``.

    Every cash flow column is the total of its months in cover; ``pols_if`` is the count in
    the first month of the contract year in the frame. Months outside cover are left out, so
    a point issued after the valuation date starts at policy year 1, and a point in force
    mid-year starts at the year under way, whose first row is that part of the year from the
    valuation date on. On a point issued at the valuation date it is ``FIA_US_S``'s report.

    Against the annual grid this agrees exactly on ``pols_if``, ``premiums``,
    ``commissions`` and ``premium_taxes``, the last three being the single premium and two
    rates on it. It does **not** agree on the withdrawal columns, the claims or the
    expenses, and so not on ``net_cf``: a withdrawal taken at the anniversary is now
    weighted by the contracts that **reach** it rather than by those that entered the year,
    claims fall in the month of exit, and maintenance expense accrues monthly. That gap is
    the point of the finer grid — see the Space docstring.
    """
    df = result_cf()
    df = df.loc[[t for t in df.index if is_active(t)]]
    years = pd.Index([policy_year(t) for t in df.index],             # noqa: F821
                     name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out



# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

issue_age_min = 40

issue_age_max = 80

maturity_age = 120

net_consideration_ratio = 0.875

floor_rate = 0.0

cap_rate_min = 0.0025

fixed_rate = 0.023

fixed_rate_min = 0.01

par_rate = 0.8

spread_rate = 0.02

trigger_rate = 0.045

index_cost_rate = 0.0

use_guaranteed_scale = False

rider_charge_rate = 0.0095

rider_charge_rate_max = 0.015

rider_charge_from_mgsv = False

growth_period_max = 20

step_up_mode = 0

rb_wd_convention = 0

mva_collar_basis = 0

min_income_age = 50

free_wd_rate = 0.1

surr_charge_period = 10

mgsv_rate = 0.01

mgsv_annual_charge = 0.0

mgsv_stat_step = 0.0005

mgsv_stat_spread = 0.0125

mgsv_stat_cap = 0.03

mgsv_stat_floor = 0.0015

mgsv_stat_delta_max = 0.01

mgsv_stat_delta_gate = 0.0025

mort_ae_factor = 1.0

lapse_base_early = 0.02

lapse_base_mid = 0.03

lapse_base_late = 0.04

lapse_base_final = 0.05

lapse_base_ult = 0.06

shock_lapse_no_rider = 0.33

shock_lapse_rider_idle = 0.1

shock_lapse_rider_active = 0.05

lapse_money_slope = 0.6

lapse_money_floor = 0.2

lapse_rate_max = 0.35

rmd_age = 73

activation_age_low = 60

activation_rate_early = 0.05

activation_rate_rmd = 0.4

activation_rate_late = 0.15

comm_rate_acq = 0.0

expense_acq_rate = 0.06

expense_maint = 80.0

inflation_rate = 0.025

premium_tax_rate = 0.0

check_tol_av = 1e-06

check_tol_pols = 1e-12

PRE_ISSUE = 0

ACCUM = 1

INCOME = 2

DEPLETED = 3

TERMINATED = 4

MATURED = 5

BEF_NB = 0

BEF_DECR = 1

BEF_MORT = 2

BEF_LAPSE = 3

AFT_DECR = 4

BEF_PREM = 5

BEF_INV = 6

BEF_FEE = 7

BEF_WD = 8

EOY = 9

BEF_ROLLUP = 10

BEF_STEP_UP = 11

DEATH = 0

LAPSE = 1

MATURITY = 2

ALL = 3

INDEX_LEVEL = 0

MVA_REF_YIELD = 1

ANNUAL = 0

AT_EXERCISE = 1

PRO_RATA = 0

DOLLAR = 1

GROSS = 0

SURRENDER_VALUE = 1

math = ("Module", "math")

pd = ("Module", "pandas")
