# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of :mod:`~.VA_US_SEC`.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.VA_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is:
``Projection[0]`` is an ItemSpace projecting the table's first row, model point 1, the
worked example's anchor cell issued at the valuation date, and :func:`point_id` is its
label::

    >>> Projection[0].result_cf()          # one row per month from the valuation date
    >>> Projection[0].point_id()           # 1, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, and an int set on a float Reference reads as a float
(``products/variable_annuity/model-sec.md``).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.VA_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``, on the chassis
:mod:`.MYGA_US_SEC` and :mod:`.FIA_US_SEC` compiled first. A formula of :mod:`~.VA_US_S`
is rewritten where it depends on where the projection starts, where it must answer for a
month outside cover, where it read a scenario or a contractual event at the wrong clock,
where it compared a model point's text or a timing, a kind or a phase as text, where its
recursion ran two cells a month, or where it reads a table or text the compiled model
holds as numbers; every other is :mod:`~.VA_US_S`'s own.
``products/variable_annuity/model-sec.md`` lists the rewritten cells with the reason for
each.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/variable_annuity/``, read at run time rather than stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``VA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers and the filename References live on the sibling :mod:`~.VA_US_SEC.Data`
Space, reached here through the ``data`` Reference, so each file is read once per model
rather than once per model point. Five assumption tables are the files
:mod:`~.VA_US_S` reads, read in place; the model point table and the two scenarios are
this model's own, generated from :mod:`~.VA_US_S` and its inputs. The projection reads
each table as ``Data`` holds it in arrays, built from the table checked, its keys read by
value, and through cells of its own:

=========================  ================================  ==========================
Reference (on Data)        Arrays the projection reads       File
=========================  ================================  ==========================
model_point_file           data.premium() and the vectors    model_point_table_sec.csv
mort_table_file            data.mort_table_array()           mort_table.csv
fund_file                  data.fund_sub_ids(),              fund_table.csv
                           data.alloc_array(),
                           data.fund_expense_array()
return_scenario_file       data.return_array()               return_scenario_sec.csv
rate_scenario_file         data.vix_sq_array(),              rate_scenario_sec.csv
                           data.cmt10_array()
gawa_pct_file              data.gawa_pct_array()             gawa_pct_table.csv
cdsc_file                  data.surr_charge_rate_array()     cdsc_table.csv
transaction_file           data.prem_amount_array(),         transaction_table.csv
                           data.wd_amount_array()
=========================  ================================  ==========================

The model point's attributes are each one element of a ``Data`` vector, read by an
accessor of the column's name, ``premium_single`` reading ``data.premium()[idx]``;
:func:`model_point`, the whole row, is for a reader. :func:`mort_rate_base_at`,
:func:`subaccount_id` with :func:`alloc` and :func:`fund_expense_rate`,
:func:`inv_return_mth`, :func:`scenario_rate`, :func:`gawa_pct_at_age`,
:func:`surr_charge_rate_at`, and :func:`prem_scheduled_pm` with :func:`wd_scheduled_pm` are
the tables' readers, in that order, and :func:`sa_pp_init` reads the subaccount values the
model point table carries, through ``Data.sa_pp_init_array``. Each is keyed by an age, a
position or an id of a subaccount, a month, a count of years or a policy month, and
called by a monthly cell in cover only. The mortality, the fund set, the two scenarios,
the grid, the withdrawal charge schedule and the programme are read at the row ``Data``
numbers the point's ``sex``, ``fund_set``, ``scenario_id``, ``glwb_option``,
``cdsc_schedule`` or ``txn_id`` by, :func:`mort_schedule`, :func:`fund_set_number`,
:func:`return_scenario_number` and :func:`rate_scenario_number`,
:func:`gawa_grid_number`, :func:`cdsc_number` and :func:`txn_number` (``Data``'s
docstring, *The vectors*).

A subaccount is named by its id throughout, as :mod:`~.VA_US_S` names it,
``sa_pp(t, i)`` with ``i`` 1 or 2 as shipped: a point's fund set picks its own ids, which
the returns and the opening columns key alike. The ids run from 1 to
``subaccount_id_max``, 9, the subaccount axis of every compiled cache, and a sum over the
subaccounts loops over the positions of the point's set, ``0 .. subaccount_count() - 1``,
taking each id from :func:`subaccount_id`, in the file's order, the order
:mod:`~.VA_US_S` sums in.

.. rubric:: Projection basis

Monthly steps on two clocks. ``t`` counts months from the **valuation date**, 0-based,
the clock ``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every
model point, however old the contract, month ``t`` runs from time ``t`` to time
``t + 1``, and the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len` counts
the months from the valuation date to the end of cover,
``maturity_mth() - duration_mth_init()``. Row ``t`` is the same month for every point,
so the frames of a block line up and sum row by row. :mod:`~.VA_US_S` counts ``t`` the
same way, from the first month it projects, and enters its in-force point 2 at ``t = 0``
26 months after issue; but it opens every recursion and keys its issue events at
``t == 0``. Here the frame has an edge at each end: a policy issued at or after the
valuation date pays its single premium, and bears its acquisition expense, in its issue
month, :func:`t_entry`, the month with ``duration_mth(t) = 0``, where every recursion
opens; a policy in force at the valuation date opens at ``t = 0`` on the state its model
point carries; and cover ends with the last month before attained age ``omega_age``.

The *policy* month is ``duration_mth(t) = duration_mth_init() + t``, the number of policy
months already **elapsed** at the start of month ``t``: 0 in a contract's issue month,
``duration_mth_init()`` at ``t = 0`` on a contract in force at the valuation date — the
worked example's carried state is one, in force with 26 elapsed months — and negative
before issue on a contract issued later. The ordinal policy month — the notes' "the
27th policy month" — is ``duration_mth(t) + 1``. Every calendar test (Contract
Anniversary, Contract Quarterly Anniversary, contract year, attained age) is written on
``duration_mth(t)``, never on ``t``.

``policy_year(t) = duration_mth(t) // 12 + 1`` is the contract year ``y``, a 1-based
contractual label, and ``contract_quarter(t) = duration_mth(t) // 3 + 1`` the contract
quarter ``k``. Contract Anniversaries fall at the **end** of the months where
``duration_mth + 1 ≡ 0 (mod 12)`` and Contract Quarterly Anniversaries at the end of
those where ``duration_mth + 1 ≡ 0 (mod 3)`` **[std]**; on a cell issued at the valuation
date that is ``t = 11, 23, 35, …`` and ``t = 2, 5, 8, …``. The attained age is
``a(t) = x + y − 1``, equivalently ``x + duration(t)`` with
``duration(t) = duration_mth(t) // 12``. Two months of the frame name the edges of a
contract year on the valuation clock: ``anniv_mth(t)``, the month at whose end the
anniversary closing the contract year of month ``t`` falls, and ``year_open_mth(t)``, the
month at whose end the year opened, which precedes the valuation date for the year under
way at ``t = 0`` on a contract valued in force mid-year.

The scenario inputs read the valuation clock. The gross fund returns, the VIX-squared
averages and the CMT rate are a market path in calendar time, shared by every point of a
block, so the ``t`` of *return_scenario_sec.csv* and *rate_scenario_sec.csv* is a
valuation month, and :func:`inv_return_mth` and :func:`scenario_rate` read them at ``t``
itself; each row of the model point table reads its own copy of :mod:`~.VA_US_S`'s path,
re-based to its months in force (``Data.return_scenario``). Expense inflation counts the
years from the valuation date, ``t // 12``, so maintenance expense is in valuation-date
dollars for every point alike (:func:`inflation_factor`). The transaction programmes, the
GAWA% grid, the withdrawal charge scale and the mortality stay on the policy clock, read
at the policy month, the attained age or the contract years completed. On a point issued
at ``t = 0`` the two clocks coincide, and the model computes what :mod:`~.VA_US_S`
computes.

Within a month the technical notes' processing order is followed exactly. At the
beginning of the month (BOM): if the contract is already depleted, run the
post-depletion routine and skip everything else; otherwise take the premium, which buys
units at the prior unit value per ``alloc[i]`` and raises ``GWB``, ``BB``, ``NP``,
``RP``, ``RB``, ``GAWA`` and ``ADJ``; then take the withdrawal, which fixes the GAWA% if
it is the first one, splits into excess and non-excess portions, computes the withdrawal
charge, cancels units pro rata and updates ``GWB``, ``GAWA`` and ``BB``. Then unit values
grow over the month. At the end of the month (EOM): the two rider fees are assessed at a
Contract Quarterly Anniversary and the annual contract fee at a Contract Anniversary,
both by pro-rata unit cancellation; then, at a Contract Anniversary only, the seven
guarantee events in the notes' order — GMDB withdrawal adjustment, GMDB roll-up, GLWB
bonus, step-up, GWB Adjustment Date test, the non-For-Life ``GAWA = GWB`` floor, and the
$10,000,000 cap; then the depletion test; then decrements, **death first, then
surrender** **[std]**.

Outside cover, before issue and from :func:`proj_len` on, every count, cash flow, balance
and rate is 0.0 and every flag ``False``; the four factors that multiply a base or a rate,
:func:`gmdb_wd_factor`, :func:`gmdb_factor_acc`, :func:`lapse_dyn_mult` and
:func:`lapse_wd_factor`, are 1.0, no change; :func:`bonus_end` is 0; and the phase is
``PRE_ISSUE`` before issue and ``EXPIRED`` from the end of cover. The clocks,
:func:`duration_mth` among them, and :func:`inflation_factor` keep their values.
:func:`is_active` is the test, made before any table or rate is read. One read reaches
ahead of the month:
:func:`lapse_wd_factor` asks whether the contract year of month ``t`` takes a withdrawal,
and reads it once, at :func:`anniv_mth`, up to 11 months later and inside the frame,
since the answer is a property of the contract year that depends on no count and on
nothing after that anniversary.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only. Reserves and discounting are a separate layer: the notes' *Valuation
and reserve pointers* section cites VM-21's CTE70 stochastic reserve, C-3 Phase II's
CTE(98), VM-22/VM-V §1 for the post-depletion stream and IRC §807, rather than
reproducing any of them.

.. rubric:: Naming

Cell names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue, and :mod:`.MYGA_US_S` — the deferred
annuity chassis of this library — wherever the two products share a concept:
``pols_*`` for policy counts, ``av_*`` for account values, plural nouns for cash flows,
``*_rate`` for rates, ``*_pp`` for per-contract amounts, ``*_at(t, timing)`` for a
quantity read at a point inside the month. What running in force adds is named as
``basiclife.BasicTerm_SE`` names it: ``duration_mth`` read from the model point,
``policy_count``, ``pols_new_biz``, ``pols_if_at`` with its ``BEF_NB`` timing,
``is_active`` and ``result_pols``; ``t_entry`` and ``maturity_mth`` are
:mod:`.MYGA_US_SEC`'s, and ``anniv_mth`` and ``year_open_mth`` :mod:`.FIA_US_SEC`'s. A
column of the opening state is the cell it opens with ``_init`` added, ``gwb_pp_init``
for :func:`gwb_pp`; a value of the contract year to date adds ``_ytd_init``, and a
balance at the anniversary that opened the year under way ``_prev_anniv_init``. A reader
keyed by an age, a year count or a policy month is ``<cell>_at`` or ``<cell>_pm``. The
``is_*`` cells read the model point's four switch columns as ``Data`` decodes them into
flags, so that no monthly cell compares a column's text and none calls a label accessor
(``stepup_basis``, ``gmdb_option``, ``scenario_id``, ...), which is left to reporting; a
``*_number`` cell, and :func:`mort_schedule`, is the row ``Data`` numbers a text key by.
No cell compares text: :mod:`~.VA_US_S`'s timings, kinds, rate columns and phases are int
codes (*Codes*, below). The technical notes use compact actuarial symbols
instead. The notes' month index is this model's ``duration_mth(t)``, so the notes' ``t``
in the left-hand column is ``duration_mth(t)`` throughout. The mapping is:

============================  ==============================  ==============================
Notes symbol                  Cells                           Meaning
============================  ==============================  ==============================
t (0-based)                   duration_mth(t)                 Policy months elapsed at the
                                                              start of month t
(valuation month)             (the projection index)          Months from the valuation
                                                              date, 0-based
(months at t = 0)             duration_mth_init()             Policy months elapsed at the
                                                              valuation date; -k if issued k
                                                              months later
(first month on books)        t_entry()                       max(0, -duration_mth_init())
(in cover)                    is_active(t)                    Whether t is inside cover
y = t//12 + 1                 policy_year(t)                  Contract year containing month
                                                              t (1-based)
y - 1                         duration(t)                     Completed contract years
k = t//3 + 1                  contract_quarter(t)             Contract quarter containing
                                                              month t (1-based)
(the anniversary month)       anniv_mth(t)                    Month closing t's contract
                                                              year, valuation clock
(year-opening month)          year_open_mth(t)                Month whose close opened it,
                                                              valuation clock
(policy month to t)           t_of_month(m)                   Valuation month of policy
                                                              month m
(the row's label)             point_id()                      The point_id of the point at
                                                              idx
x, issue_age                  age_at_entry                    Issue age (ANB)
a(t) = x + y - 1              age(t)                          Attained age during month t
(a at the anniversary)        age_at_anniv(t)                 Attained age just after the
                                                              anniversary
(none)                        policy_term                     Years from issue to omega_age
(cover from issue)            maturity_mth()                  Policy month cover ends: 12 x
                                                              policy_term
(none)                        proj_len                        Months from the valuation date
                                                              to the end of cover
(contracts)                   policy_count                    Contracts the model point
                                                              stands for
av_initial                    av_pp_init()                    AV entering month 0, the sum
                                                              of the SA_i; 0 on new business
(SA_i at entry)               sa_pp_init(i)                   SA_i entering month 0, the
                                                              sa_pp_init_<i> column
gwb_initial                   gwb_pp_init()                   GWB entering month 0
bb_initial                    bb_pp_init()                    Bonus Base entering month 0
rb_initial                    rb_pp_init()                    GMDB Benefit Base entering
                                                              month 0
(GAWA at entry)               gawa_pp_init()                  GAWA entering month 0
(GAWA% at entry)              gawa_pct_init()                 GAWA% locked by the valuation
                                                              date
(withdrawn at entry)          has_wd_init()                   Whether a withdrawal was taken
                                                              before month 0
(NP at entry)                 np_pp_init()                    Cumulative Net Premiums
                                                              entering month 0
(RP at entry)                 rp_pp_init()                    Remaining Premium entering
                                                              month 0
(ADJ at entry)                adj_pp_init()                   GWB Adjustment entering month
                                                              0
(bonus end at entry)          bonus_end_init()                Contract year the Bonus Period
                                                              ends, entering month 0
SumW_y at entry               sum_wd_pp_ytd_init()            Withdrawals in the contract
                                                              year before month 0
(allowance used at entry)     free_wd_used_cum_pp_ytd_init()  Free allowance used in that
                                                              year before month 0
(accrued d-f-d at entry)      gmdb_dfd_acc_pp_ytd_init()      GMDB d-f-d accrued in that
                                                              year before month 0
(accrued factor at entry)     gmdb_factor_acc_ytd_init()      GMDB pro-rata factor accrued
                                                              in that year before month 0
(withdrawal year at entry)    wd_this_year_init()             Whether that year took a
                                                              withdrawal before month 0
RB at the prior anniversary   rb_pp_prev_anniv_init()         RB at the anniversary opening
                                                              the year under way
(quarterly AVs at entry)      stepup_base_pp_ytd_init()       Highest AV at that year's
                                                              quarterly anniversaries before
                                                              month 0
(prior quarter's phi_G)       phi_glwb_init()                 vix rule: the last quarter's
                                                              rate before month 0
glwb_stepup_basis             stepup_basis()                  annual_CV or
                                                              highest_quarterly_CV
(annual step-up)              is_stepup_annual()              The basis is annual_CV
(quarterly step-up)           is_stepup_highest_quarterly()   The basis is
                                                              highest_quarterly_CV
(roll-up GMDB)                is_gmdb_rollup()                gmdb_option is rollup
(ratchet GMDB)                is_gmdb_ratchet()               gmdb_option is ratchet
(return-of-premium GMDB)      is_gmdb_basic()                 gmdb_option is basic
(no fee reset)                is_fee_reset_none()             fee_reset_rule is none
(five-yearly fee reset)       is_fee_reset_quinquennial()     fee_reset_rule is quinquennial
(VIX fee reset)               is_fee_reset_vix()              fee_reset_rule is vix
(fixed roll-up)               is_rollup_fixed()               rollup_rule is fixed
(CMT-linked roll-up)          is_rollup_cmt_linked()          rollup_rule is cmt_linked
i                             sub_ids                         Subaccount ids, a list (an
                                                              engine cell)
(the point's fund set)        fund_set_number()               Data's number for fund_set
(subaccounts held)            subaccount_count()              Subaccounts the fund set holds
(the j-th subaccount)         subaccount_id(j)                Its id, in file order
alloc[i]                      alloc(i)                        Allocation of net premium to
                                                              subaccount i
e_i                           fund_expense_rate(i)            Annual fund expense ratio
r_i(t)                        inv_return_mth(t, i)            Gross monthly fund return
                                                              (scenario input)
(the point's returns)         return_scenario_number()        Data's number for its
                                                              scenario_id, the returns
(the point's rates)           rate_scenario_number()          The same, the rate scenarios
(the rate scenario)           scenario_rate(t, name)          Level of column name in force
                                                              at month t
(VIX-squared average)         vix_sq(k)                       Quarterly average of daily
                                                              VIX^2, quarter k
(CMT10)                       cmt10(t)                        10-year CMT rate at month t
m                             asset_charge_me                 M&E asset charge
alpha                         asset_charge_admin              Administrative asset charge
(the growth factor)           unit_growth(t, i)               (1+r_i)(1-e_i/12)(1-(m+a)/12)
V_i(t)                        (inside unit_growth)            Unit value; see the note below
U_i(t)                        (implicit)                      Units; see the note below
SA_i(t)                       sa_pp(t, i)                     Subaccount value at end of
                                                              month t
SA_i at a point in the month  sa_pp_at(t, i, timing)          BEF_PREM, BEF_WD, BEF_INV,
                                                              BEF_FEE or EOM
AV(t)                         av_pp(t)                        Contract value at end of month
                                                              t
AV at a point in the month    av_pp_at(t, timing)             Same timings, summed over
                                                              subaccounts
l x AV(t)                     av_at(t, timing)                In-force weighted contract
                                                              value
w_i(t)                        sa_weight(t, i)                 Value weight, the pro-rata
                                                              deduction key
(gross fund return)           gross_inv_income_pp(t)          Return before any charge
(fund's own expense)          fund_expense_pp(t)              Paid to the funds, not insurer
                                                              revenue
(M&E + admin)                 asset_charge_pp(t)              Collected inside the unit
                                                              value
(net of both)                 inv_income_pp(t)                Change in AV from investment
                                                              over month t
P(t)                          premium_pp(t)                   Gross premium at BOM of month
                                                              t
(single premium)              premium_single()                The purchase payment, in the
                                                              issue month
(scheduled premium)           prem_scheduled_pp(t)            Premium from
                                                              transaction_table.csv
(premium at policy month)     prem_scheduled_pm(m)            The programme's premium at
                                                              policy month m
(the point's programme)       txn_number()                    Data's number for txn_id
P(t)(1 - tau)                 prem_to_av_pp(t)                Net premium buying units
tau                           premium_tax_rate                Premium tax rate
W(t)                          wd_pp(t)                        Gross withdrawal, inclusive of
                                                              charges
(W before the AV cap)         wd_pp_due(t)                    Withdrawal requested before
                                                              capping at AV
(scheduled part of W)         wd_scheduled_pp(t)              Withdrawal from
                                                              transaction_table.csv
(W at policy month)           wd_scheduled_pm(m)              The programme's withdrawal at
                                                              policy month m
(utilization part of W)       wd_glwb_pp(t)                   wd_intensity x L(t) once
                                                              activated
(GLWB withdrawal month)       is_wd_month(t)                  The utilization withdrawal
                                                              falls in month t
(a withdrawal in t)           is_wd_taken(t)                  Any withdrawal is taken in
                                                              month t
(withdrawn by t)              has_wd_by(t)                    A withdrawal taken at or
                                                              before month t
(the first withdrawal)        is_first_wd(t)                  Month t takes the first
                                                              withdrawal
(withdrawal year)             is_wd_year(t)                   The contract year of t takes a
                                                              withdrawal
L(t)                          wd_limit_pp(t)                  Annual withdrawal limit
                                                              max(GAWA, RMD)
SumW_y                        sum_wd_pp(t)                    Withdrawals to date in the
                                                              contract year
E(t)                          wd_excess_pp(t)                 Excess portion of W(t)
N(t)                          wd_nonexcess_pp(t)              Non-excess portion of W(t)
CV_pre                        cv_pre_excess_pp(t)             AV after N has been deducted
(1 - E/CV_pre)                excess_factor(t)                The pro-rata factor for the
                                                              excess
(charge-free amount)          free_wd_allow(t)                max(earnings, 10% of RP)
(unused allowance)            free_wd_avail(t)                Allowance left in the contract
                                                              year
(allowance consumed)          wd_free_pp(t)                   Allowance used by month t's
                                                              withdrawal
(allowance used to date)      free_wd_used_cum_pp(t)          Allowance used in the contract
                                                              year so far
(exempt part of W)            wd_exempt_pp(t)                 Portion of W bearing no charge
(chargeable part of W)        wd_chargeable_pp(t)             Portion of W bearing the CDSC
c(t)                          wd_charge_pp(t)                 CDSC on the withdrawal
W(t) - c(t)                   wd_payment_pp(t)                Cash paid on the withdrawal
CDSC scale                    surr_charge_rate(t)             CDSC % by completed years
                                                              since receipt
(CDSC by year count)          surr_charge_rate_at(k)          The schedule's rate at k
                                                              completed years
(the point's scale)           cdsc_number()                   Data's number for
                                                              cdsc_schedule
(surrender free amount)       surr_free_pp(t)                 Charge-free amount left for a
                                                              full surrender
(surrender chargeable base)   surr_chargeable_pp(t)           Remaining Premium withdrawn on
                                                              surrender
(CDSC on surrender)           surr_charge_pp(t)               Charge on a full surrender
AV(t) - CDSC                  surr_benefit_pp(t)              Surrender proceeds
RP(t)                         rp_pp(t)                        Remaining Premium, the CDSC
                                                              basis
(premium portion withdrawn)   rp_reduction_pp(t)              Reduction of RP by a
                                                              withdrawal
NP(t)                         np_pp(t)                        Cumulative Net Premiums
GWB(t)                        gwb_pp(t)                       Guaranteed Withdrawal Balance
GWB at a point in the month   gwb_pp_at(t, timing)            BEF_PREM / BEF_WD / BEF_ANNIV
(GWB after the bonus)         gwb_pp_aft_bonus(t)             Anniversary sub-step 3
(GWB after the step-up)       gwb_pp_aft_stepup(t)            Anniversary sub-step 4
b x BB                        bonus_pp(t)                     GLWB bonus credited at the
                                                              anniversary
BB(t)                         bb_pp(t)                        Bonus Base
BB before the anniversary     bb_pp_bef_anniv(t)              Bonus Base the bonus is
                                                              computed on
bonus_end(t)                  bonus_end(t)                    Contract year the Bonus Period
                                                              ends
(the step-up basis)           stepup_base_pp(t)               Annual or highest quarterly CV
(step-up occurred)            is_stepup(t)                    True at a step-up anniversary
GAWA(t)                       gawa_pp(t)                      Guaranteed Annual Withdrawal
                                                              Amount
GAWA in the month             gawa_pp_at(t, timing)           BEF_PREM / BEF_WD / BEF_ANNIV
g(a)                          gawa_pct_at_age(a)              GAWA% at attained age a
(the point's grid)            gawa_grid_number()              Data's number for glwb_option
gawa_pct_fixed                gawa_pct_fixed(t)               GAWA% locked at the first
                                                              withdrawal
ADJ(t)                        adj_pp(t)                       GWB Adjustment amount
ADJ before the anniversary    adj_pp_bef_anniv(t)             ADJ carried into the
                                                              anniversary events
s                             gwb_adj_pct                     GWB Adjustment percentage,
                                                              105%
(the Adjustment year)         gwb_adj_year()                  Contract year of the
                                                              Adjustment Date
(the Adjustment Date)         is_gwb_adj_date(t)              Later of anniv on/after 70 and
                                                              the 12th
RB(t)                         rb_pp(t)                        GMDB Benefit Base
RB in the month               rb_pp_at(t, timing)             BEF_PREM / BEF_WD / BEF_ANNIV
(RB opening the year)         rb_prior_anniv_pp(t)            RB at the anniversary
                                                              preceding t
rho                           rollup_rate(t)                  GMDB roll-up percentage in
                                                              force
(the year's d-f-d allowance)  gmdb_allow_pp(t)                rho x RB at the prior
                                                              anniversary
(d-f-d part of a withdrawal)  gmdb_wd_dfd_pp(t)               Dollar-for-dollar portion
(excess part)                 gmdb_wd_excess_pp(t)            Portion above the allowance
(its pro-rata factor)         gmdb_wd_factor(t)               Proportional factor of the
                                                              excess
(accrued d-f-d)               gmdb_dfd_acc_pp(t)              Accrued to the end of the
                                                              contract year
(accrued pro-rata factor)     gmdb_factor_acc(t)              Accrued to the end of the
                                                              contract year
DB(t)                         db_pp(t)                        Gross death benefit: max(AV,
                                                              NP, RB)
max(NP, RB)                   gmdb_guarantee_pp(t)            The floor under DB; ``basic``
                                                              elects RB alone
GuaranteeClaim                gmdb_claim_pp(t)                Net general-account strain on
                                                              death
phi_G                         phi_glwb(t)                     GLWB charge rate in force
(phi_G on the vix rule)       phi_glwb_vix(k)                 VIX-formula rate in contract
                                                              quarter k
phi_D                         phi_gmdb(t)                     GMDB charge rate in force
Fee_G                         fee_glwb_pp(t)                  Quarterly GLWB fee, on the GWB
Fee_D                         fee_gmdb_pp(t)                  Quarterly GMDB fee, on the RB
f_c                           maint_fee_pp(t)                 Annual contract fee, $35
                                                              waived at $50k
(total unit cancellation)     charge_pp(t)                    Fee_G + Fee_D + f_c actually
                                                              collected
(fee reset formula)           fee_rate_vix_raw(phi0, vix2)    The VIX-squared fee formula
                                                              [S4][S6]
(fee reset clipping)          fee_rate_vix_clip(prior, raw)   Band and corridor clipping
                                                              [S4]
forlife_flag                  forlife_flag()                  For Life Guarantee in effect
depleted_flag(t)              depleted_flag(t)                AV has reached zero with the
                                                              GLWB alive
(depleted entering t)         depleted_open(t)                Depleted entering month t
(post-depletion payment)      glwb_payment_pp(t)              Insurer-funded GAWA payment
phase(t)                      phase(t)                        PRE_ISSUE, ACCUM, DEPLETED or
                                                              EXPIRED
M_G(t)                        moneyness_glwb(t)               GWB / AV
M_D(t)                        moneyness_gmdb(t)               max(NP, RB) / AV
lambda(M)                     lapse_itm_mult(ratio)           The VM-21 7.B.1 multiplier
lambda*(t)                    lapse_dyn_mult(t)               min of the two, per VM-21
                                                              6.C.6
kappa(t)                      lapse_wd_factor(t)              0.60 in a withdrawal year
q^w_base(y)                   lapse_rate_base(t)              VM-21 Table 6.3 under-50%-ITM
                                                              column
q^w_annual(t)                 lapse_rate(t)                   Annual total surrender rate
q^w(t)                        lapse_rate_mth(t)               Monthly total surrender rate
q^d(t)                        mort_rate_mth(t)                Monthly mortality rate
(annual q_x)                  mort_rate(t)                    Annual mortality at the
                                                              attained age
(the table's q_x)             mort_rate_base_at(x)            Table rate at attained age x
                                                              and the sex
(the point's sex)             mort_schedule()                 Data's number for sex
l(t-1)                        pols_if(t)                      Count at the START of month t
l(t)                          pols_if_at(t, AFT_DECR)         In-force at the end of month t
l(-1)                         pols_if_init                    In force at the valuation
                                                              date; 0 on new business
l(t-1), ...                   pols_if_at(t, timing)           BEF_NB, BEF_DECR, BEF_LAPSE,
                                                              AFT_DECR
(new business)                pols_new_biz(t)                 policy_count in the issue
                                                              month
l(t-1) q^d                    pols_death(t)                   Deaths
l(t-1)(1-q^d) q^w             pols_lapse(t)                   Full surrenders
(none)                        pols_maturity(t)                Survivors at the end of cover
Premium income                premiums(t)                     Premium cash flow
Charge income - M&E/admin     asset_charges(t)                Asset charge cash flow
Charge income - rider fees    fees_glwb(t), fees_gmdb(t)      Rider fee cash flow
Charge income - contract fee  maint_fees(t)                   Contract fee cash flow
Charge income - CDSC          wd_charges(t)                   CDSC on withdrawals (memo; see
                                                              below)
Withdrawal proceeds           withdrawals(t)                  W(t) - c(t), weighted
Post-depletion GLWB payments  glwb_payments(t)                GAWA paid after depletion
Death benefit (gross)         claims(t, DEATH)                DB(t) x deaths
Death benefit (net strain)    gmdb_claims(t)                  GuaranteeClaim x deaths (memo)
Surrender proceeds            claims(t, LAPSE)                surr_benefit_pp(t) x
                                                              surrenders
(horizon benefit)             claims(t, MATURITY)             Survivors in the last covered
                                                              month
Maintenance expense           expenses(t)                     VM-21 6.C.2 prescribed expense
(expense inflation)           inflation_factor(t)             1.025^(years from 2015 to the
                                                              valuation date plus projection
                                                              years completed)
(acquisition)                 commissions(t)                  0 in the base run [std]
(none)                        net_cf(t)                       The notes' ledger, summed
(none)                        net_cf_ga(t)                    General-account view (memo)
============================  ==============================  ==============================

Model point attributes the notes and the model name identically — ``sex``,
``designated_lives``, ``tax_status``, ``premium_tax_rate``, ``glwb_option``,
``gmdb_option``, ``cdsc_schedule`` and the ``rate_sheet_date`` Reference — are not
repeated in the table above; ``issue_date`` is not carried at all, the model working in
policy months throughout.

Nine names needed care.

``pols_if(t)`` is the count in force at the **start** of month ``t`` — the notes'
``l(t-1)`` — and is the weight applied to that same row's cash flows, so
``premiums(t) / premium_pp(t)`` is exactly ``pols_if(t)`` and the printed in-force column
reconciles with the row it sits on. That is the library-wide convention, set by
:mod:`.Term_US_S` and by ``savings.CashValue_SE``. The notes' own end-of-month ``l(t)``
has not gone anywhere: it is ``pols_if_at(t, AFT_DECR)``, and the roll-forward
is written across it.

``lapse_rate(t)`` is the **annual** total surrender rate and :func:`lapse_rate_mth` the
monthly one, matching the ``mort_rate`` / ``mort_rate_mth`` pair. Both spellings of the
notes' ``q^w`` are present and the suffix is the only thing that tells them apart, so
read the suffix.

``wd_free_pp(t)`` is the portion of a withdrawal covered by the **free-withdrawal
allowance**, which is what the same name means on the deferred annuity chassis
(:mod:`.MYGA_US_S`, ``min(W, FW)``). On this product a second exemption
stacks on top of it — no CDSC applies to cumulative withdrawals within ``L`` [S1] — and
the union of the two is :func:`wd_exempt_pp`, the portion of ``W(t)`` bearing no charge
at all. The two differ by exactly :func:`wd_nonexcess_pp`, and it is
:func:`wd_exempt_pp`, not :func:`wd_free_pp`, that complements
:func:`wd_chargeable_pp`. The year-to-date cumulative is
:func:`free_wd_used_cum_pp`, named for what it is rather than sharing the ``wd_*`` stem.

``E(t)`` is the **guarantee** excess here — the portion of a withdrawal above the GLWB
annual limit — and :func:`wd_excess_pp` carries that meaning. In
:mod:`.MYGA_US_S` the same cell name means the portion of a withdrawal above
the free allowance, i.e. the *charge* base. On this product those are two different
quantities and both exist: the charge base is :func:`wd_chargeable_pp`. Reading
``wd_excess_pp`` across the two models without checking is the single easiest mistake to
make in this library.

``E(t)`` in :mod:`.Term_US_S` is expenses, which here is :func:`expenses` as usual. ``M``
is the in-the-moneyness ratio here and the market value adjustment in
:mod:`.MYGA_US_S`; a VA separate account has no MVA at all, so there is no
collision in the model, only in the reader's memory. ``c(t)`` is the CDSC here and the
Model #805 contract charge in :mod:`.MYGA_US_S`; it becomes
:func:`wd_charge_pp`. ``g`` is the GAWA% here and the monthly nonforfeiture factor there;
it becomes :func:`gawa_pct_at_age`. And ``b`` is the GLWB bonus percentage here and the
MVA distribution yield there.

Two cells the chassis has that this model deliberately does **not**: ``mgsv_pp`` and
``surr_value_pp``. NAIC Model #805 expressly excludes variable annuities and reaches a VA
only through its *fixed* account under Model #250 §7.B [REG-R42][REG-R43], and this
contract has no fixed account because electing the Roll-up GMDB removes the Fixed Account
Options [S1]. There is therefore no minimum guaranteed surrender value and no pre-floor
surrender value to distinguish: :func:`surr_benefit_pp` is simply ``AV(t)`` less the
CDSC. Carrying the chassis' floor across would be the error the chassis file itself warns
against.

.. rubric:: The unit ledger

The notes write the account value as ``AV = Σ_i U_i V_i`` and require charges assessed
*per unit of value* (fund expense, M&E, administrative asset charge) to live **inside**
``V_i``, while charges assessed *per contract or on a benefit base* (the annual contract
fee, the two rider fees) are collected by **cancelling units**, leaving ``V_i``
untouched: ``ΔU_i = C · w_i(t) / V_i(t)``, so ``ΔAV = C``.

.. rubric:: State carried into the frame

Every state variable in this model is a **closing balance of month t**: ``av_pp(t)``,
``sa_pp(t, i)``, ``gwb_pp(t)``, ``bb_pp(t)``, ``rb_pp(t)``, ``gawa_pp(t)``, ``np_pp(t)``,
``rp_pp(t)`` and ``adj_pp(t)`` are all values at the **end** of month ``t``. Their
*opening* value is therefore ``S(t - 1)``, and in the first month a contract is on the
books, :func:`t_entry`, it is the model point's ``S_init()`` instead, its column of the
opening state: every recursion reads its previous month first,
``S(t - 1) if t > t_entry() else S_init()``, then the month's own steps, as
:mod:`.MYGA_US_SEC` and :mod:`.FIA_US_SEC` write it. That single convention replaces an
entry-instant row: the premium, the guarantee-base initialization and the acquisition
expense are all beginning-of-month flows of the issue month, where the opening state is
0, and the issue values come by :mod:`~.VA_US_S`'s own rules there. **No carried-in state
is read before the first month on the books**, and no cell in cover reads a month before
:func:`t_entry`.

A contract in force at the valuation date carries twenty columns of opening state, per
contract, as it stands at the start of month 0, before any month-0 event, each exactly
what :mod:`~.VA_US_S` carries into that month: the two subaccount values, which
:mod:`~.VA_US_S` would split from the account value by the target allocation, wrong once
the funds drift apart; the GWB, the Bonus Base, the GAWA, the GMDB Benefit Base, the
cumulative Net Premiums, the Remaining Premium and the GWB Adjustment; the locked GAWA%,
the end of the Bonus Period and whether a withdrawal has been taken. Four quantities of
the contract year restart at its start — the withdrawals to date, the free allowance
they used, the GMDB's dollar-for-dollar reduction and its proportional factor — and the
year under way at the valuation date opened before it on a contract valued mid-year, so
each opens at ``t = 0`` on its ``_ytd_init`` column, as does whether that year has taken
a withdrawal, :func:`wd_this_year_init`. The Benefit Base at the anniversary that opened
the year is read three ways (:func:`rb_prior_anniv_pp`): from the frame where that
anniversary is on the books, from :func:`rb_pp_prev_anniv_init` where it precedes the
valuation date, and by the issue rule in a contract's first year. The highest quarterly
account value of the year before the valuation month and the VIX-formula rate of the last
quarter to end before it are columns too, :func:`stepup_base_pp_ytd_init` and
:func:`phi_glwb_init`. The depleted status takes none: a contract in force enters month 0
depleted exactly where its opening account value is at or below
``av_depletion_threshold``, and new business never does (:func:`depleted_open`).

The model carries the *product* ``SA_i = U_i V_i`` rather than the two factors, because
with no transfers between subaccounts the two are never needed apart, and every quantity
the notes print is a subaccount **value**. The distinction the ledger exists to enforce
survives intact: a per-unit charge multiplies ``sa_pp`` through :func:`unit_growth`,
while a unit cancellation multiplies it by ``(1 − C / AV)`` — which is exactly pro-rata
deduction, and which therefore leaves every ``w_i`` unchanged.

That property is necessary for the notes' 60/40 anchor cell to still sit at exactly
60/40 twenty-six months later, but it is **not sufficient**, and it would be a bad
lesson to take away on its own: unequal growth moves the weights whatever the charges
do. What closes the gap is the illustrative ``base`` path, reverse-engineered so that
the two subaccounts grow at the same rate *net of fund expense* (see the ``provenance``
column of *return_scenario.csv*) — with equal net growth and pro-rata cancellation the
weights cannot move at all. The worked-example month itself is the counter-example:
``r_1`` = +1.20% against ``r_2`` = −0.30% takes ``w_1`` from 0.600000 at the beginning of
that month to :func:`sa_weight` = 0.603519 by the time the fees are read at its end. On
the cell issued at the valuation date the month is ``t = 26`` — the 27th policy month —
and on the carried state in force at 26 months it is ``t = 0``.

.. rubric:: Timing arguments

Account and subaccount values, following ``CashValue_SE``'s ``av_pp_at``:

``BEF_PREM``
    ``AV(t-1)``, at the start of month ``t`` before the premium — the opening balance,
    and in the first month on the books, :func:`t_entry`, the model point's opening
    state, :func:`sa_pp_init` and :func:`av_pp_init`, which are 0 on new business.
``BEF_WD``
    after the premium has bought units, before the withdrawal.
``BEF_INV``
    ``AV'(t)``, after the withdrawal, before unit value growth.
``BEF_FEE``
    after growth, before the rider fees and the contract fee. This is the point at which
    the notes read the pro-rata key ``w_i``.
``EOM``
    ``AV(t)``, after every charge. Equal to :func:`av_pp`.

Guarantee bases (``gwb_pp_at``, ``gawa_pp_at``, ``rb_pp_at``) take ``BEF_PREM``,
``BEF_WD`` and ``BEF_ANNIV``; their end-of-month value, after the anniversary
guarantee events, is the plain cells (:func:`gwb_pp`, :func:`gawa_pp`, :func:`rb_pp`).
``BEF_PREM`` opens on the model point's ``_init`` column at :func:`t_entry`.

Policy counts, following ``CashValue_SE``'s ``pols_if_at`` and
``basiclife.BasicTerm_SE``:

``BEF_NB``
    the count carried in from month ``t - 1``, before month ``t``'s new business:
    :func:`pols_if_init` at :func:`t_entry`, the contracts in force at the valuation
    date, 0 on new business.
``BEF_DECR``
    ``l(t-1)``, in force at the start of month ``t``: ``BEF_NB`` plus that month's
    :func:`pols_new_biz`. Equal to ``pols_if(t)``.
``BEF_LAPSE``
    after deaths, ``l(t-1)(1 - q^d(t))``.
``AFT_DECR``
    after surrenders, ``l(t)`` — the notes' end-of-month count, and equal to
    ``pols_if_at(t + 1, BEF_NB)`` except in the last covered month, where the survivors
    leave as :func:`pols_maturity` instead.

Benefit ``kind`` arguments are ``DEATH``, ``LAPSE`` and ``MATURITY``, and ``ALL``, the
three kinds' total, for :func:`claims` and :func:`claims_over_av`. Any other value of any
of these raises ``ValueError``. Each is an int code (*Codes*, below).

.. rubric:: pols_maturity and the projection horizon

The technical notes state no projection horizon, and this contract does not supply one:
once the account value is exhausted the For Life Guarantee is a **pure life-contingent
annuity at GAWA**, which the notes rank sixth in their sensitivity list precisely because
the mortality basis then becomes the whole story. The model therefore runs to attained
age ``omega_age`` = 120 **[std]**, the terminal age of the mortality table: cover ends at
policy month :func:`maturity_mth` ``= 12 * policy_term()``, which is
``proj_len() = maturity_mth() - duration_mth_init()`` months from the valuation date, and
``pols_maturity(t)`` carries the survivors out in the last covered month,
``duration_mth(t) = maturity_mth() - 1``, which is ``t = proj_len() - 1`` — zero
everywhere else — so that::

    pols_if(t) - pols_if_at(t + 1, BEF_NB) = pols_death(t) + pols_lapse(t)
                                               + pols_maturity(t)

holds for every ``t``, including the last, where the block would otherwise appear to lose
lives with no cause. The identity is written on start-of-month counts because that is
what :func:`pols_if` carries: the next month opens on what is left, before its own new
business, and in the last covered month ``pols_if_at(proj_len(), BEF_NB)`` is zero,
every survivor of that month having left as :func:`pols_maturity`. The name follows
``BasicTerm_S.pols_maturity`` and the construction follows :mod:`.Term_US_S` and
:mod:`.MYGA_US_S`. It is bookkeeping determined by the horizon, not an added
assumption.

The contract's own Latest Income Date — the Contract Anniversary at owner age 95 [S2] —
is **not** implemented as a forced annuitization; see the model docstring's list of what
is not implemented.

.. rubric:: Codes

What :mod:`~.VA_US_S` spells as text, a timing, a kind, a rate scenario's column or a
phase, is here an int Reference named as the text it replaces, so that every cell takes
and returns C numbers. A call site reads as it did, less the quotes:
``pols_if_at(t, BEF_DECR)``, ``av_pp_at(t, BEF_WD)``, ``claims(t, DEATH)``.

===============  =====  =============================================================
Reference        Value  Meaning
===============  =====  =============================================================
BEF_NB           0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR         1      :func:`pols_if_at`: that count plus month t's new business
BEF_LAPSE        2      :func:`pols_if_at`: after deaths
AFT_DECR         3      :func:`pols_if_at`: after surrenders, the notes' l(t)
BEF_PREM         4      the account value and the bases: the opening balance
BEF_WD           5      the account value and the bases: after the premium
BEF_INV          6      the account value: after the withdrawal, before the growth
BEF_FEE          7      the account value: after the growth, before the charges
EOM              8      the account value: closing the month
BEF_ANNIV        9      the bases: after the withdrawal, before the anniversary
DEATH            0      the claim cells: the death claim
LAPSE            1      the claim cells: the surrender claim
MATURITY         2      the claim cells: the survivors at the horizon
ALL              3      :func:`claims`, :func:`claims_over_av`: the three kinds' total
VIX_SQ           0      :func:`scenario_rate`: the ``vix_sq`` column
CMT10            1      :func:`scenario_rate`: the ``cmt10`` column
PRE_ISSUE        0      :func:`phase`: before issue
ACCUM            1      :func:`phase`: in cover, the account value not run out
DEPLETED         2      :func:`phase`: in cover, the account value run out
EXPIRED          3      :func:`phase`: from the end of cover
===============  =====  =============================================================

The model has three families of timing, the count's, the account value's and the bases',
passed to different cells, and they are numbered as one: ``BEF_NB`` 0 and ``BEF_DECR`` 1,
as in every SEC model, then the count's others, then the account value's, then the
bases' own one, each family in the order of its instants. The bases share ``BEF_PREM``
and ``BEF_WD`` with the account value, where :mod:`~.VA_US_S` spells them alike, so each
is one Reference. So a code of one family passed to another's cell,
``av_pp_at(t, BEF_NB)``, is refused as any timing the cell does not take is,
``ValueError("invalid timing")``, in both engines, rather than read as a timing of the
cell's own. Kinds are numbered in ``result_cf``'s order, which is the order
:mod:`~.VA_US_S` adds them in its total, and ``ALL``, its ``kind=None``, after them;
:func:`claims` and :func:`claims_over_av` answer ``ALL`` with :mod:`~.VA_US_S`'s chain of
``+``, so that the total is :mod:`~.VA_US_S`'s bit for bit, and the other claim cells
refuse it, ``ValueError("invalid kind")``. The columns are :mod:`~.VA_US_S`'s names
upper-cased. A code a cell takes indexes that cell's cache, a C array of ten codes a
month, since every 2-D cache of the model has one width, the timings' count, which is the
subaccount axis's too (``spec_sec.py``), so codes are numbered densely from 0, and a code
a cell does not take but below 10 is refused inside the cache; a code from 10 raises
``IndexError``, compiled alone. Codes are References, not cells, so the symbol map does
not list them. Every other Reference is named in lower case, the contract's bounds among
them: ``issue_age_min``, ``issue_age_max``, ``glwb_issue_age_max`` and
``gmdb_issue_age_max``, the product's issue ages, 35, 85, 80 and 79, and
``subaccount_id_max``, 9, the largest subaccount id a fund set may hold, which
:func:`proj_len` checks, the first and the last of which, with ``omega_age``, the compiled
model's caches are sized from.

.. rubric:: Reporting cells

:func:`model_point`, the thirteen label accessors :func:`policy_id`, :func:`sex`,
:func:`designated_lives`, :func:`tax_status`, :func:`fund_set`, :func:`glwb_option`,
:func:`stepup_basis`, :func:`gmdb_option`, :func:`cdsc_schedule`, :func:`fee_reset_rule`,
:func:`rollup_rule`, :func:`scenario_id` and :func:`txn_id`, the reports
:func:`result_cf`, :func:`result_pols`, :func:`result_av` and :func:`result_bases`, and the
checks :func:`check_av_roll_fwd`, :func:`check_pols_roll_fwd` and
:func:`check_charge_split` are written for a reader and for the comparison with
:mod:`~.VA_US_S`, which has every one of them: a table row, text, DataFrames and three
verdicts. No other cell calls them: each reads the number ``Data`` decoded from the same
column instead, the decodes' flags and the rows the keys select. So the row, the text and
the frames stay Python when the model compiles. A label accessor returns its column as
read, text or not: ``Data`` accepts, and the model projects, a point whose ``policy_id``,
``designated_lives`` or ``tax_status`` is blank or a number, which no cell reads, whose
``glwb_stepup_basis``, ``gmdb_option``, ``fee_reset_rule`` or ``rollup_rule`` is blank,
which its decodes answer False to, or whose ``sex``, ``fund_set``, ``glwb_option``,
``cdsc_schedule``, ``scenario_id`` or ``txn_id`` is a number, where its table's keys are
numbers, and the compiled accessor returns what modelx returns, NaN or an int. Every
other cell returns a C ``bint``, ``long long`` or ``double``, and so do the three checks,
which may stay Python but compile to a ``bint``, their verdict, as their per-month
residuals, ``*_resid``, compile to a ``double``.

Four cells compile with C signatures and dict caches, or stay Python, the engine cells
:func:`lapse_itm_mult`, :func:`fee_rate_vix_raw` and :func:`fee_rate_vix_clip`, keyed by
floats, and :func:`sub_ids`, a list: :mod:`~.VA_US_S`'s own, kept for its tests, for T1,
which compares them at the arguments :mod:`~.VA_US_S`'s tests use, and for a reader. No
projection cell calls them, and a cell keyed by a float compiles with a Python dict for a
cache, so the registry admits them by name. The projection writes the three float
engines inline in the cells that call them, :func:`lapse_dyn_mult` and
:func:`phi_glwb_vix`, in :mod:`~.VA_US_S`'s order of evaluation, and loops over the
subaccounts by position itself.
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
    """x: the issue age (ANB) of the selected model point."""
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the Designated Life, M or F.

    A label for reporting: the projection reads the mortality at :func:`mort_schedule`.
    """
    return model_point()["sex"]


def mort_schedule():
    """The number ``Data`` gives the point's ``sex``, by which its mortality is read.

    The row of ``Data.mort_table_array``. The join on the text key, made once in ``Data``
    (R7), where ``VA_US_S``'s reader selects its rows by the key itself:
    :func:`mort_rate_base_at` reads the table at this number, so no projection cell
    compares the key or calls the label accessor.
    """
    return int(data.mort_schedule()[idx])                            # noqa: F821


def designated_lives():
    """``single`` or ``joint``.

    Reported only: the joint-life election of the modeled GLWB is out of scope in the
    product spec, so the GAWA% grid and the For Life test are the single-life ones
    **[std]**.
    """
    return model_point()["designated_lives"]


def tax_status():
    """``NQ`` or ``Q``.

    Reported only. The base run is non-qualified **[std]**, which keeps the RMD term of
    ``L = max(GAWA, RMD)`` disclosed but inactive; no RMD module is implemented.
    """
    return model_point()["tax_status"]


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the contracts in force then, before any
    month-0 event; any other point counts the contracts it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Every per-contract value — the
    subaccount values, the guarantee bases, the GAWA, the opening state — is the same
    whatever the count, and every cash flow is a per-contract amount weighted by it.
    ``VA_US_S``'s ``pols_if_init`` column, renamed, as ``basiclife.BasicTerm_SE`` names it.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """l(-1): contracts in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose contracts
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count. ``VA_US_S``'s cell of the name is the count at its
    entry, 1 for a single-contract model point, whether entered at issue or in force.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def premium_tax_rate():
    """tau: premium tax deducted from the purchase payment, 0% **[std]**, 0-3.5% [S2].

    Set to zero so that GWB at issue equals gross premium and the worked example is
    checkable; premium tax is contractually deducted from the amounts that initialize the
    guarantee bases [S1].
    """
    return float(data.premium_tax_rate()[idx])                       # noqa: F821


def premium_single():
    """The single purchase payment, paid at the beginning of the issue month.

    The month with ``duration_mth(t) = 0``, which is :func:`t_entry` on a contract issued
    at or after the valuation date; :func:`premium_pp` takes it there. A contract in force
    at the valuation date paid it before the frame, and its opening state carries what it
    bought.
    """
    return float(data.premium()[idx])                                # noqa: F821


def fund_set():
    """The key into *fund_table.csv* naming this contract's subaccount allocation.

    A label for reporting: the projection reads the set at :func:`fund_set_number`.
    """
    return model_point()["fund_set"]


def fund_set_number():
    """The number ``Data`` gives the point's ``fund_set``, by which its funds are read.

    The row of ``Data``'s fund arrays, ``fund_sub_ids``, ``fund_held``, ``alloc_array``
    and ``fund_expense_array``, the join on the text key made once in ``Data`` (R7).
    """
    return int(data.fund_set_number()[idx])                          # noqa: F821


def subaccount_count():
    """The number of subaccounts the point's fund set holds."""
    return int(data.fund_sub_count()[fund_set_number()])             # noqa: F821


def subaccount_id(j):
    """The id of the subaccount at position ``j`` of the point's fund set, in file order.

    ``j`` runs from 0 to ``subaccount_count() - 1``, in the order ``VA_US_S``'s
    ``sub_ids`` returns the ids and its sums run in, so that a loop over the positions,
    taking each id from here, sums the subaccounts as ``VA_US_S`` does. A position outside
    the set raises ``ValueError``, naming the point, and so does any position of a set
    holding an id past ``Data.read_last_sub_id``, which ``Data`` does not hold and
    :func:`proj_len` refuses first.
    """
    f = fund_set_number()
    if data.fund_sub_id_last()[f] > data.read_last_sub_id:           # noqa: F821
        raise ValueError(f"point_id {point_id()}: the fund set holds subaccount "
                         f"{data.fund_sub_id_last()[f]}, past Data.read_last_sub_id, "
                         f"{data.read_last_sub_id}")                 # noqa: F821
    if j < 0 or j >= subaccount_count():
        raise ValueError(f"point_id {point_id()}: the fund set holds no subaccount at "
                         f"position {j}")
    return int(data.fund_sub_ids()[f, j])                            # noqa: F821


def sub_ids():
    """The subaccount ids of the model point's allocation set, in file order, as a list.

    Two subaccounts **[std]** — the minimum that exercises pro-rata charge allocation and
    unit accounting. Real contracts offer far more; one carrier's build-your-own menu
    lists 76 options across 12 asset classes [S4].

    ``VA_US_S``'s cell, kept for a reader and for the comparison with ``VA_US_S``: a list,
    which no C type holds, so it is an engine cell (the Space docstring's *Reporting
    cells*), built by an explicit loop over :func:`subaccount_id`, and no other cell calls
    it. Every sum over the subaccounts loops over the positions itself.
    """
    ids = []
    for j in range(subaccount_count()):
        ids.append(subaccount_id(j))
    return ids


def alloc(i):
    """alloc[i]: the share of net premium allocated to subaccount i, no rebalancing.

    ``Data.alloc_array`` at the point's :func:`fund_set_number` and the subaccount id
    ``i``. An id outside 1 to ``Data.read_last_sub_id``, or one the set does not hold,
    raises ``ValueError``, naming the point, where ``VA_US_S``'s lookup raised
    ``KeyError``.
    """
    f = fund_set_number()
    if i < 1 or i > data.read_last_sub_id or data.fund_held()[f, i] == 0:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: the fund set holds no subaccount {i}")
    return float(data.alloc_array()[f, i])                           # noqa: F821


def fund_expense_rate(i):
    """e_i: the annual fund expense ratio of subaccount i, paid to the fund [S2].

    ``Data.fund_expense_array`` at the point's :func:`fund_set_number` and ``i``, refused
    as :func:`alloc` refuses.
    """
    f = fund_set_number()
    if i < 1 or i > data.read_last_sub_id or data.fund_held()[f, i] == 0:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: the fund set holds no subaccount {i}")
    return float(data.fund_expense_array()[f, i])                    # noqa: F821


def glwb_option():
    """The GLWB election, and the key into the GAWA% grid; ``s3_single`` [S3].

    A label for reporting: the projection reads the grid at :func:`gawa_grid_number`.
    """
    return model_point()["glwb_option"]


def gawa_grid_number():
    """The number ``Data`` gives the point's ``glwb_option``, the row of its GAWA% grid.

    The row of ``Data.gawa_pct_array``, the join made once in ``Data`` (R7), which
    :func:`gawa_pct_at_age` reads.
    """
    return int(data.gawa_grid_number()[idx])                         # noqa: F821


def stepup_basis():
    """``annual_CV`` or ``highest_quarterly_CV`` [S1][S3].

    ``annual_CV`` is the representative election: the step-up test uses the Contract
    Value at the anniversary. ``highest_quarterly_CV`` uses the highest contract value
    over the four most recent Contract Quarterly Anniversaries; the source also adjusts
    each of those for subsequent premiums and withdrawals under the same
    dollar-for-dollar / proportional rule, which is **not implemented** — see the model
    docstring.

    A label accessor, called by no projection cell: :func:`is_stepup_annual` and
    :func:`is_stepup_highest_quarterly` decode the model point's ``glwb_stepup_basis``
    column, and :func:`stepup_base_pp` branches on them.
    """
    return model_point()["glwb_stepup_basis"]


def is_stepup_annual():
    """Whether the step-up basis is ``annual_CV``, the column decoded once a point.

    ``Data.is_stepup_annual``, ``glwb_stepup_basis`` compared with ``"annual_CV"`` as
    ``VA_US_S`` compares it, element by element, read at the point. Read by
    :func:`stepup_base_pp` where ``VA_US_S`` compares :func:`stepup_basis` with the text.
    """
    return bool(data.is_stepup_annual()[idx])                        # noqa: F821


def is_stepup_highest_quarterly():
    """Whether the step-up basis is ``highest_quarterly_CV``, the column decoded.

    ``Data.is_stepup_highest_quarterly``, ``glwb_stepup_basis`` compared with
    ``"highest_quarterly_CV"`` as ``VA_US_S`` compares it, element by element, read at the
    point. Read by :func:`stepup_base_pp`; a basis that is neither of the two raises
    ``VA_US_S``'s message there.
    """
    return bool(data.is_stepup_highest_quarterly()[idx])             # noqa: F821


def gmdb_option():
    """``rollup``, ``ratchet`` or ``basic``.

    ``rollup`` is the representative election: ``RB(t) = RB(t-1)(1 + rho)`` at each
    anniversary to the age cutoff, with a dollar-for-dollar withdrawal allowance applied
    at Contract Year end [S1][S3]. ``ratchet`` is the annual ratchet ``max(RB, AV)`` at each
    anniversary with proportional withdrawal treatment [S1][S4][S7]. ``basic`` is the
    included no-charge proportional return of premium [S1][S2]; on that election the base
    *is* the return of premium, so :func:`np_pp` is not floored under it as well — see
    :func:`gmdb_guarantee_pp`. The notes' fourth form, ``combination``, is **not
    implemented** — see the model docstring.

    A label accessor, called by no projection cell: :func:`is_gmdb_rollup`,
    :func:`is_gmdb_ratchet` and :func:`is_gmdb_basic` decode the model point's
    ``gmdb_option`` column, and the cells that branch on the election read them.
    """
    return model_point()["gmdb_option"]


def is_gmdb_rollup():
    """Whether the GMDB election is ``rollup``, the column decoded once a point.

    ``Data.is_gmdb_rollup``, ``gmdb_option`` compared with ``"rollup"`` as ``VA_US_S``
    compares it, element by element, read at the point. Read by :func:`rb_pp`,
    :func:`rb_pp_at`, :func:`gmdb_wd_dfd_pp` and :func:`gmdb_wd_excess_pp`, where
    ``VA_US_S`` compares :func:`gmdb_option` with the text.
    """
    return bool(data.is_gmdb_rollup()[idx])                          # noqa: F821


def is_gmdb_ratchet():
    """Whether the GMDB election is ``ratchet``, the annual ratchet, the column decoded.

    ``Data.is_gmdb_ratchet``, ``gmdb_option`` compared with ``"ratchet"`` as ``VA_US_S``
    compares it, element by element, read at the point. Read by :func:`rb_pp`.
    """
    return bool(data.is_gmdb_ratchet()[idx])                         # noqa: F821


def is_gmdb_basic():
    """Whether the GMDB election is ``basic``, the return of premium, the column decoded.

    ``Data.is_gmdb_basic``, ``gmdb_option`` compared with ``"basic"`` as ``VA_US_S``
    compares it, element by element, read at the point. Read by :func:`rb_pp`,
    :func:`gmdb_guarantee_pp` and :func:`phi_gmdb`; an election that is none of the three
    raises ``VA_US_S``'s message in :func:`rb_pp`.
    """
    return bool(data.is_gmdb_basic()[idx])                           # noqa: F821


def cdsc_schedule():
    """The key into *cdsc_table.csv* naming this contract's withdrawal charge scale.

    A label for reporting: the projection reads the scale at :func:`cdsc_number`.
    """
    return model_point()["cdsc_schedule"]


def cdsc_number():
    """The number ``Data`` gives the point's ``cdsc_schedule``, the row of its scale.

    The row of ``Data.surr_charge_rate_array``, the join made once in ``Data`` (R7),
    which :func:`surr_charge_rate_at` reads.
    """
    return int(data.cdsc_number()[idx])                              # noqa: F821


def fee_reset_rule():
    """``none``, ``quinquennial`` or ``vix``.

    ``none`` is the base run **[std]**: the insurer does not increase the rider charge
    and the owner does not opt out. ``quinquennial`` applies the maximum single increase
    of +0.25% at each fifth Contract Anniversary up to the guaranteed maximum [S1].
    ``vix`` applies a second carrier's non-discretionary VIX-squared formula [S4][S6].

    A label accessor, called by no projection cell: :func:`is_fee_reset_none`,
    :func:`is_fee_reset_quinquennial` and :func:`is_fee_reset_vix` decode the model
    point's ``fee_reset_rule`` column, and :func:`phi_glwb` branches on them.
    """
    return model_point()["fee_reset_rule"]


def is_fee_reset_none():
    """Whether the GLWB fee reset rule is ``none``, the column decoded once a point.

    ``Data.is_fee_reset_none``, ``fee_reset_rule`` compared with ``"none"`` as ``VA_US_S``
    compares it, element by element, read at the point. Read by :func:`phi_glwb`, where
    ``VA_US_S`` compares :func:`fee_reset_rule` with the text.
    """
    return bool(data.is_fee_reset_none()[idx])                       # noqa: F821


def is_fee_reset_quinquennial():
    """Whether the GLWB fee reset rule is ``quinquennial``, the column decoded.

    ``Data.is_fee_reset_quinquennial``, ``fee_reset_rule`` compared with ``"quinquennial"``
    as ``VA_US_S`` compares it, element by element, read at the point. Read by
    :func:`phi_glwb`.
    """
    return bool(data.is_fee_reset_quinquennial()[idx])               # noqa: F821


def is_fee_reset_vix():
    """Whether the GLWB fee reset rule is ``vix``, the column decoded once a point.

    ``Data.is_fee_reset_vix``, ``fee_reset_rule`` compared with ``"vix"`` as ``VA_US_S``
    compares it, element by element, read at the point. Read by :func:`phi_glwb`; a rule
    that is none of the three raises ``VA_US_S``'s message there.
    """
    return bool(data.is_fee_reset_vix()[idx])                        # noqa: F821


def rollup_rule():
    """``fixed`` or ``cmt_linked``.

    ``fixed`` is the base run **[std]**: 6.00% at election ages up to 69 and 5.00% from
    70 [S3]. ``cmt_linked`` is a third carrier's formula rate, a 20-day average 10-year
    CMT plus 1.00% (1.50% before the first withdrawal), rounded to 0.10%, floored at 4%
    and capped at 8% [S7].

    A label accessor, called by no projection cell: :func:`is_rollup_fixed` and
    :func:`is_rollup_cmt_linked` decode the model point's ``rollup_rule`` column, and
    :func:`rollup_rate` branches on them.
    """
    return model_point()["rollup_rule"]


def is_rollup_fixed():
    """Whether the GMDB roll-up rule is ``fixed``, the column decoded once a point.

    ``Data.is_rollup_fixed``, ``rollup_rule`` compared with ``"fixed"`` as ``VA_US_S``
    compares it, element by element, read at the point. Read by :func:`rollup_rate`, where
    ``VA_US_S`` compares :func:`rollup_rule` with the text.
    """
    return bool(data.is_rollup_fixed()[idx])                         # noqa: F821


def is_rollup_cmt_linked():
    """Whether the GMDB roll-up rule is ``cmt_linked``, the column decoded once a point.

    ``Data.is_rollup_cmt_linked``, ``rollup_rule`` compared with ``"cmt_linked"`` as
    ``VA_US_S`` compares it, element by element, read at the point. Read by
    :func:`rollup_rate`; a rule that is neither of the two raises ``VA_US_S``'s message
    there.
    """
    return bool(data.is_rollup_cmt_linked()[idx])                    # noqa: F821


def wd_start_age():
    """The attained age at which GLWB withdrawals begin; 70 in the base run **[std]**.

    Zero means the contract never withdraws. The base-run value rests on the finding that
    activation clusters at the RMD age [REG-R64 **[unverified]**][REG-R57][REG-R58]. The
    prescribed alternative is VM-21's Withdrawal Delay Cohort Method, which is **not
    implemented**.
    """
    return int(data.wd_start_age()[idx])                             # noqa: F821


def wd_intensity():
    """The fraction of the annual limit withdrawn once activated; 100% **[std]**.

    100% matches VM-21 §6.C.3's Guarantee Actuarial Present Value construction [R1]. The
    prescribed partial-withdrawal assumption is 90% for lifetime GMWBs and 70% for
    non-lifetime ones [R1].
    """
    return float(data.wd_intensity()[idx])                           # noqa: F821


def scenario_id():
    """The scenario the model point runs on, a key into the two scenario tables.

    The row's own copy of a ``VA_US_S`` scenario, on the valuation clock: ``VA_US_S``'s id
    for a contract issued at the valuation date, and ``{id}-M{m}`` or ``{id}-F{k}`` for
    one in force at policy month ``m`` or issued ``k`` months later
    (``Data.return_scenario``). A label accessor, called by no projection cell:
    :func:`inv_return_mth` and :func:`scenario_rate` read the scenarios at
    :func:`return_scenario_number` and :func:`rate_scenario_number`.
    """
    return model_point()["scenario_id"]


def return_scenario_number():
    """The number ``Data`` gives the point's ``scenario_id`` in the return scenarios.

    The row of ``Data.return_array``, the join made once in ``Data`` (R7), which
    :func:`inv_return_mth` reads.
    """
    return int(data.return_scenario_number()[idx])                   # noqa: F821


def rate_scenario_number():
    """The number ``Data`` gives the point's ``scenario_id`` in the rate scenarios.

    The row of ``Data.vix_sq_array`` and ``Data.cmt10_array``, which
    :func:`scenario_rate` reads; 0 where the rate scenarios lack the id, which ``Data``
    accepts on a point no level is read for and :func:`scenario_rate` refuses.
    """
    return int(data.rate_scenario_number()[idx])                     # noqa: F821


def txn_id():
    """The scheduled transaction programme, a key into *transaction_table.csv*.

    A label for reporting: the projection reads the programme at :func:`txn_number`.
    """
    return model_point()["txn_id"]


def txn_number():
    """The number ``Data`` gives the point's ``txn_id``, the row of its programme.

    The row of ``Data.prem_amount_array`` and ``Data.wd_amount_array``, the join made once
    in ``Data`` (R7), which :func:`prem_scheduled_pm` and :func:`wd_scheduled_pm` read.
    """
    return int(data.txn_number()[idx])                               # noqa: F821


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The contract's age in months at ``t = 0``: 26 for the worked example's carried state,
    in force at the beginning of its 27th policy month, 0 for a contract issued at the
    valuation date, and -15 for one to be issued 15 months after it, which ``Data`` admits
    up to ``future_horizon_mth`` months ahead. It is read as ``basiclife.BasicTerm_SE``
    reads it, as a whole number whatever the column's type, and is the one fact the policy
    clock takes from the model point. ``VA_US_S``'s ``duration_mth_init`` column, renamed;
    ``VA_US_S`` can take it as 0 or as a month in force, never as a month to come.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def is_inforce():
    """True when the model point is in force at the valuation date, not issued at or after.

    ``duration_mth_init() > 0``: a contract issued at the valuation date, or after it,
    is not, and opens with no state at all. Read where :mod:`~.VA_US_S` reads it, to choose
    the Bonus Period's end opening the frame.
    """
    return duration_mth_init() > 0


def av_pp_init():
    """AV entering month 0, per contract: the sum of the subaccount values carried in.

    ``sum_i sa_pp_init(i)`` over the set's subaccounts, an explicit loop over the
    positions taking each id from :func:`subaccount_id`, so 0 on a contract
    issued at or after the valuation date. ``VA_US_S`` carries one account value,
    ``av_init``, and splits it across the subaccounts by the target allocation **[std]**,
    which holds for its in-force point, exactly at its 60/40 target, and fails wherever
    the funds have grown apart since issue: the subaccount values are therefore the
    opening state here, and the account value their sum. Read by :func:`av_change` for the
    block's opening value and by :func:`depleted_open`, which reads a contract in force
    whose sum is at or below ``av_depletion_threshold`` as depleted from month 0.
    """
    total = 0.0
    for j in range(subaccount_count()):
        total = total + sa_pp_init(subaccount_id(j))
    return total


def sa_pp_init(i):
    """SA_i entering month 0, per contract: the model point's ``sa_pp_init_<i>`` column.

    The value of subaccount ``i`` at the start of month 0, before any month-0 event, read
    from ``Data.sa_pp_init_array`` at the point's position and the subaccount id; 0 on a
    contract issued at or after the valuation date, whose premium buys its units in the
    issue month, and 0 for an id the point's set does not hold. :func:`sa_pp_at` and
    :func:`sa_pp` open on it at :func:`t_entry`, where ``VA_US_S`` opens on
    ``alloc(i) x av_pp_init()``. An id outside 1 to ``Data.read_last_sub_id`` raises
    ``ValueError``, naming the point.
    """
    if i < 1 or i > data.read_last_sub_id:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: subaccount ids run from 1 to "
                         f"{data.read_last_sub_id}, Data.read_last_sub_id; there is no "
                         f"subaccount {i}")
    return float(data.sa_pp_init_array()[idx, i])                    # noqa: F821


def gwb_pp_init():
    """GWB entering month 0, the ``gwb_pp_init`` column.

    0 on a contract issued at or after the valuation date, where the premium creates it
    in the issue month [S1]; ``VA_US_S``'s ``gwb_init`` column, renamed.
    """
    return float(data.gwb_pp_init()[idx])                            # noqa: F821


def gawa_pp_init():
    """GAWA entering month 0, the ``gawa_pp_init`` column.

    0 until the first withdrawal fixes it [S1], or depletion; ``VA_US_S``'s ``gawa_init``
    column, renamed. On a contract depleted at the valuation date it is the amount the
    GLWB pays at each contract year's start, read by :func:`glwb_payment_pp` at ``t = 0``.
    """
    return float(data.gawa_pp_init()[idx])                           # noqa: F821


def gawa_pct_init():
    """The GAWA% locked by the valuation date; 0 when none has been locked.

    The percentage is locked at the first withdrawal, or at depletion where the account
    value runs out first [S1], so a contract that depleted without withdrawing carries a
    percentage above 0 here with :func:`has_wd_init` False. The column of the name, as in
    ``VA_US_S``, which infers its withdrawal status from it.
    """
    return float(data.gawa_pct_init()[idx])                          # noqa: F821


def has_wd_init():
    """Whether a withdrawal was taken before the valuation date, the ``has_wd_init`` column.

    ``VA_US_S`` infers it from :func:`gawa_pct_init`, which is non-zero once the GAWA% has
    been locked. That holds until a contract's account value runs out before its first
    withdrawal: the GAWA% locks at depletion too, and ``VA_US_S``'s own frame then keeps
    ``has_wd_by`` False. Once the account is exhausted no cash flow reads the status, but
    the GWB Adjustment does, to its date, voided by a withdrawal and not by a depletion, so
    the status is a column of its own here. ``Data`` reads it by value and ties it to the
    GWB Adjustment, to the year's withdrawal flag and to the GAWA%.
    """
    return bool(data.has_wd_init()[idx])                             # noqa: F821


def bb_pp_init():
    """Bonus Base entering month 0, the ``bb_pp_init`` column; it initializes at GWB [S1].

    ``VA_US_S``'s ``bb_init`` column, renamed; 0 on new business.
    """
    return float(data.bb_pp_init()[idx])                             # noqa: F821


def rb_pp_init():
    """GMDB Benefit Base entering month 0, the ``rb_pp_init`` column.

    ``VA_US_S``'s ``rb_init`` column, renamed; 0 on new business.
    """
    return float(data.rb_pp_init()[idx])                             # noqa: F821


def np_pp_init():
    """Cumulative Net Premiums entering month 0, the ``np_pp_init`` column.

    ``VA_US_S``'s ``np_init`` column, renamed; 0 on new business.
    """
    return float(data.np_pp_init()[idx])                             # noqa: F821


def rp_pp_init():
    """Remaining Premium entering month 0, the ``rp_pp_init`` column; the CDSC basis [S2].

    ``VA_US_S``'s ``rp_init`` column, renamed; 0 on new business.
    """
    return float(data.rp_pp_init()[idx])                             # noqa: F821


def adj_pp_init():
    """GWB Adjustment entering month 0, the ``adj_pp_init`` column.

    105% of net premium at endorsement [S3], credited in the issue month, so 0 on a
    contract issued at or after the valuation date; 0 too once any withdrawal has voided it
    or its date has passed. ``VA_US_S``'s ``adj_init`` column, renamed.
    """
    return float(data.adj_pp_init()[idx])                            # noqa: F821


def bonus_end_init():
    """The contract year the Bonus Period ends, carried into the frame.

    1 or more on a contract in force at the valuation date, which ``Data`` requires, and 0
    on one issued at or after it, whose Bonus Period opens at ``bonus_period_years`` = 10
    [S1] in its issue month (:func:`bonus_end`).
    """
    return int(data.bonus_end_init()[idx])                           # noqa: F821


def sum_wd_pp_ytd_init():
    """SumW_y entering month 0: the withdrawals of the contract year to date, per contract.

    The gross withdrawals taken in the contract year under way at the valuation date, in
    its months before month 0; 0 at a year's start, where :func:`sum_wd_pp` restarts, and
    on new business. :func:`sum_wd_pp` opens on it at ``t = 0`` where that year opened
    before the valuation date; ``VA_US_S`` restarts the sum at ``t = 0`` as though every
    valuation were a year's start.
    """
    return float(data.sum_wd_pp_ytd_init()[idx])                     # noqa: F821


def free_wd_used_cum_pp_ytd_init():
    """The free allowance used in the contract year to date, entering month 0.

    The opening of :func:`free_wd_used_cum_pp`, read by it and by :func:`free_wd_avail`
    at ``t = 0`` where the year under way opened before the valuation date; 0 at a year's
    start and on new business. Part of :func:`sum_wd_pp_ytd_init`, and it may exceed the
    allowance month 0 allows, which is recomputed every month from the earnings and the
    Remaining Premium.
    """
    return float(data.free_wd_used_cum_pp_ytd_init()[idx])           # noqa: F821


def gmdb_dfd_acc_pp_ytd_init():
    """The GMDB dollar-for-dollar reduction accrued in the contract year to date.

    Entering month 0, the opening of :func:`gmdb_dfd_acc_pp`, read by it and by
    :func:`gmdb_wd_dfd_pp` at ``t = 0`` where the year under way opened before the
    valuation date; 0 at a year's start, off the ``rollup`` election and on new business.
    Part of :func:`sum_wd_pp_ytd_init`.
    """
    return float(data.gmdb_dfd_acc_pp_ytd_init()[idx])               # noqa: F821


def gmdb_factor_acc_ytd_init():
    """The GMDB proportional factor accrued in the contract year to date, entering month 0.

    The opening of :func:`gmdb_factor_acc` at ``t = 0`` where the year under way opened
    before the valuation date: the product of the year's withdrawal factors so far, 1 at a
    year's start and below 1 only after an excess withdrawal in the year. 0 on new
    business, which has no opening state and opens the factor at 1 in its issue month, a
    year's start.
    """
    return float(data.gmdb_factor_acc_ytd_init()[idx])               # noqa: F821


def wd_this_year_init():
    """Whether the contract year under way took a withdrawal before the valuation month.

    The ``wd_this_year_init`` column. :func:`is_wd_year` answers True for that year from
    it, the months before ``t = 0`` being off the books, and scans the months on the books
    for the rest; ``VA_US_S``'s scan starts at ``t = 0``. False at a year's start and on
    new business.
    """
    return bool(data.wd_this_year_init()[idx])                       # noqa: F821


def rb_pp_prev_anniv_init():
    """RB at the anniversary that opened the contract year under way at the valuation date.

    The GMDB Benefit Base at the close of month ``year_open_mth(0)``, before the valuation
    date, the base of the year's dollar-for-dollar allowance, which
    :func:`rb_prior_anniv_pp` reads where that anniversary precedes the books. In the
    first policy year it is the issue value, the premium credited at issue, and at a year's
    start it equals :func:`rb_pp_init`, the two being one instant; ``Data`` checks both.
    ``VA_US_S`` reads ``rb_pp_at(0, BEF_WD)`` there instead, wrong wherever a premium was
    credited after the anniversary and before the valuation month. 0 on new business.
    """
    return float(data.rb_pp_prev_anniv_init()[idx])                  # noqa: F821


def stepup_base_pp_ytd_init():
    """The highest account value at the year's quarterly anniversaries before month 0.

    The largest of the account values at the ends of the contract year's quarterly
    anniversary months that closed before the valuation month, 0 where none has, on any
    step-up basis, as the generator writes it; only :func:`stepup_base_pp` reads it, on the
    ``highest_quarterly_CV`` basis alone, taking it into the step-up base at the
    anniversary closing the year under way, and at no other. ``VA_US_S`` leaves out every
    quarter before ``t = 0``. 0 before the year's first quarterly anniversary and on new
    business; on the highest-quarterly basis above ``av_depletion_threshold`` from it on a
    contract not depleted, which :func:`proj_len` checks.
    """
    return float(data.stepup_base_pp_ytd_init()[idx])                # noqa: F821


def phi_glwb_init():
    """The VIX-formula GLWB charge rate of the last contract quarter before month 0.

    On the ``vix`` fee rule, the rate of the quarter before the one under way at the
    valuation date, the clip's prior for that quarter's rate, which :func:`phi_glwb_vix`
    reads; ``VA_US_S`` recurses the rate from the first quarter instead, through VIX
    fixings before the frame. 0 in the first contract quarter, off the rule and on new
    business.
    """
    return float(data.phi_glwb_init()[idx])                          # noqa: F821


def policy_term():
    """Contract term in years: entry age to ``omega_age`` **[std]**."""
    return omega_age - age_at_entry()                                 # noqa: F821


def maturity_mth():
    """The policy month at which cover ends: ``12 * policy_term()``.

    The first policy month past cover, at attained age ``omega_age`` = 120 **[std]**, so
    the last covered month is ``maturity_mth() - 1``, 719 at issue age 60. It is
    ``VA_US_S``'s frame from issue on the policy clock; :func:`proj_len` counts from the
    valuation date instead.
    """
    return 12 * policy_term()


def proj_len():
    """The number of months from the valuation date to the end of cover.

    ``maturity_mth() - duration_mth_init()``: 720 for a contract issued at ``t = 0`` at
    issue age 60, 694 for the worked example's carried state in force at 26 months, 1 for
    a contract valued in its last policy month, and 735 for one to be issued 15 months
    after the valuation date. The frame is ``t = 0, 1, ..., proj_len() - 1``, so
    ``proj_len()`` is the **exclusive** end of the projection and
    ``len(result_cf()) == proj_len()``. ``VA_US_S`` computes the same number,
    ``12 * policy_term() - duration_mth_init()``, on every point it can project.

    First the contract's bounds, each a Reference, set before the model computes
    anything, and each refusal naming the point, its value and the Reference that would
    admit it, in this order: an issue age below ``issue_age_min``, 35, the GLWB's youngest
    (product-spec.md, *Eligible ages*), from which the compiled model's caches are sized
    (``spec_sec.py``), so that lowering it needs the spec recomputed and the model
    rebuilt; above ``issue_age_max``, 85, the base contract's oldest; above
    ``glwb_issue_age_max``, 80, the GLWB's oldest, which every point carries; above
    ``gmdb_issue_age_max``, 79, the add-on GMDB's oldest, on the two elected forms,
    ``rollup`` and ``ratchet``, the ``basic`` form, included at no charge, having none;
    and a fund set holding a subaccount id above ``subaccount_id_max``, 9, the subaccount
    axis of every compiled cache, which needs ``Data.read_last_sub_id`` raised with it,
    the spec recomputed and the model rebuilt. Each sizes nothing else. ``VA_US_S``
    projects a point past each bound, given the tables to read it with, so each is a
    refusal ``VA_US_S`` lacks.

    Then a point at or past the end of cover at the valuation date has no frame, and
    raises here, naming the point, rather than projecting nothing: an in-force extract
    should not carry it. So does a point issued at or past ``omega_age``, whose cover from
    issue is empty, which the ages refuse first unless ``issue_age_max`` is raised past
    it.

    And so, on a contract in force, does an opening state that no contract can be in by a
    rule needing a Reference of this Space, which ``Data`` cannot read, each refusal naming
    the point, in this order:

    * depleted, its account value carried in, :func:`av_pp_init`, at or below
      ``av_depletion_threshold``, that account value is 0 to within 1e-8: a contract that
      opens depleted has its account released in month 0 with no flow, so
      :func:`check_av_roll_fwd`, at ``check_tol_av`` a contract, would miss by any more;
      ``VA_US_S``'s depletions close on roundings of the order of 1e-14;
    * not depleted, its account value carried in, :func:`av_pp_init`, above
      ``av_depletion_threshold``, a contract that has not withdrawn has no GAWA% locked:
      the percentage locks at the first withdrawal or at depletion, and before either the
      GAWA is 0 too, which ``Data`` ties to it;
    * depleted without a withdrawal, it has one above 0, the grid's at the age it ran out
      at, unless its grid gave 0% at an attained age it reached before the valuation
      month, ``Data.gawa_pct_zero_by_point()`` at the point, read here and nowhere else;
    * on the ``highest_quarterly_CV`` basis, not depleted and three months or more into
      its contract year, its step-up history, :func:`stepup_base_pp_ytd_init`, is above
      the threshold: depletion is absorbing, so every quarter end of the year before the
      valuation month closed above it;
    * on the ``vix`` fee rule, in its second contract quarter, ``duration_mth`` 3 to 5,
      the VIX prior, :func:`phi_glwb_init`, is the first quarter's rate,
      ``phi_glwb_curr``; and from the third the prior is at most ``vix_corridor_hi`` and,
      where ``phi_glwb_curr`` is at or above ``vix_corridor_lo`` and the corridor runs
      upward, at least ``vix_corridor_lo``, since :func:`fee_rate_vix_clip` holds every
      rate after the first at most at the corridor's top, and, from a first rate at or
      above its foot, at least at the foot.

    The other refusals of the opening state are ``Data``'s, as the table is read.
    """
    x = age_at_entry()
    if x < issue_age_min:                                            # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {x} is below issue_age_min, "
                         f"{issue_age_min}; lower issue_age_min, and rebuild a compiled "
                         f"model, whose caches it sizes, to project it")
    if x > issue_age_max:                                            # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {x} is above issue_age_max, "
                         f"{issue_age_max}; raise issue_age_max to project it")  # noqa
    if x > glwb_issue_age_max:                                       # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {x} is above "
                         f"glwb_issue_age_max, {glwb_issue_age_max}, the GLWB's oldest; "
                         f"raise glwb_issue_age_max to project it")
    if (is_gmdb_rollup() or is_gmdb_ratchet()) and x > gmdb_issue_age_max:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {x} is above "
                         f"gmdb_issue_age_max, {gmdb_issue_age_max}, the add-on GMDB's "
                         f"oldest; raise gmdb_issue_age_max to project it")
    top = data.fund_sub_id_last()[fund_set_number()]                 # noqa: F821
    if top > subaccount_id_max:                                      # noqa: F821
        raise ValueError(f"point_id {point_id()}: its fund set holds subaccount {top}, "
                         f"above subaccount_id_max, {subaccount_id_max}; raise "  # noqa
                         f"subaccount_id_max and Data.read_last_sub_id, and rebuild a "
                         f"compiled model, whose caches it sizes, to project it")
    if maturity_mth() <= 0:
        raise ValueError(
            f"point_id {point_id()}: age_at_entry {age_at_entry()} is at or past "
            f"omega_age {omega_age}: the contract has no cover")             # noqa: F821
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past the end of cover, policy month {maturity_mth()}")
    d = duration_mth_init()
    if d <= 0:
        return n
    threshold = av_depletion_threshold                               # noqa: F821
    if av_pp_init() <= threshold and not abs(av_pp_init()) <= 1e-8:
        raise ValueError(
            f"point_id {point_id()}: av_pp_init must be 0, to within 1e-8, on a "
            f"policy depleted at the valuation date, its account value at or below "
            f"av_depletion_threshold {threshold}: depletion releases the account in month "
            f"0 with no flow; it is {av_pp_init()}")
    if not has_wd_init() and not av_pp_init() <= threshold and gawa_pct_init() > 0.0:
        raise ValueError(
            f"point_id {point_id()}: gawa_pct_init must be 0 on a policy "
            f"that has not withdrawn and is not depleted, its account value above "
            f"av_depletion_threshold {threshold}: the GAWA% locks at the first "
            f"withdrawal or at depletion; it is {gawa_pct_init()}")
    if (not has_wd_init() and av_pp_init() <= threshold and gawa_pct_init() == 0.0
            and data.gawa_pct_zero_by_point()[idx] == 0):              # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: gawa_pct_init must be more than 0 on a "
            f"depleted policy that has not withdrawn: depletion locks the GAWA% of the "
            f"attained age it falls at, which the point's grid gives as more than 0 at "
            f"every attained age the policy reached before the valuation month")
    if (is_stepup_highest_quarterly() and d % 12 >= 3 and not av_pp_init() <= threshold
            and not stepup_base_pp_ytd_init() > threshold):
        raise ValueError(
            f"point_id {point_id()}: stepup_base_pp_ytd_init must be above "
            f"av_depletion_threshold {threshold} on a policy not depleted, duration_mth "
            f"% 12 3 or more: every quarter end of the year before the valuation month "
            f"closed above it; it is {stepup_base_pp_ytd_init()}")
    curr = phi_glwb_curr                                             # noqa: F821
    lo = vix_corridor_lo                                             # noqa: F821
    hi = vix_corridor_hi                                             # noqa: F821
    if is_fee_reset_vix() and 3 <= d < 6 and phi_glwb_init() != curr:
        raise ValueError(
            f"point_id {point_id()}: phi_glwb_init must be phi_glwb_curr, "
            f"{curr}, in the second contract quarter, duration_mth 3 to 5: the prior is "
            f"the first quarter's rate; it is {phi_glwb_init()}")
    if is_fee_reset_vix() and d >= 6 and not (
            phi_glwb_init() <= hi
            and (phi_glwb_init() >= lo or not (curr >= lo and lo <= hi))):
        raise ValueError(
            f"point_id {point_id()}: phi_glwb_init must be at most "
            f"vix_corridor_hi, {hi}, and at least vix_corridor_lo, {lo}, where "
            f"phi_glwb_curr is, from the third contract quarter, duration_mth 6 or more: "
            f"the clip holds every rate after the first there; it is {phi_glwb_init()}")
    return n


def duration_mth(t):
    """Policy months already **elapsed** at the start of month t.

    ``duration_mth_init() + t``, 0-based like ``t`` itself: ``duration_mth(t) = 0`` is the
    first policy month, the issue month. The ordinal policy month — the notes' "the 27th
    policy month" — is ``duration_mth(t) + 1``. Negative before issue on a contract issued
    after the valuation date.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later. It is the base of every recursion: :func:`pols_if_at` opens there
    from :func:`pols_if_init`; the subaccount values, the guarantee bases, the statuses
    and the year to date from the model point's opening state, which is 0 on new business;
    and the year's quarterly history, its opening Benefit Base and the VIX fee's prior read
    the frame only where it is at or after this month. No cell in cover reads a month
    before it.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month ``t`` is inside cover: issued, and not past the last covered month.

    ``0 <= duration_mth(t) < maturity_mth()``. False before issue and from :func:`proj_len`
    on. Outside cover every count is zero, and so every cash flow; so is every balance,
    every charge and every rate, every flag is ``False``, and no table is read at a policy
    month, a contract year or an attained age the contract does not have.
    """
    return 0 <= duration_mth(t) < maturity_mth()


def policy_year(t):
    """y(t): the contract year containing month t, **1-based**: 1 in the first year."""
    return duration_mth(t) // 12 + 1


def duration(t):
    """Completed contract years at month t, ``policy_year(t) - 1``; 0 in the first year."""
    return duration_mth(t) // 12


def age(t):
    """a(t) = x + y - 1: the attained age (ANB) during month t."""
    return age_at_entry() + duration(t)


def age_at_anniv(t):
    """The attained age just after the Contract Anniversary at the end of month t.

    ``x + y``, one more than :func:`age`, and the age the GMDB growth cutoff and the
    Bonus Period restart cutoff are stated against [S1].
    """
    return age_at_entry() + policy_year(t)


def contract_quarter(t):
    """k(t): the contract quarter containing month t, **1-based**: 1 in months 0 to 2."""
    return duration_mth(t) // 3 + 1


def is_anniv(t):
    """True at the end of a Contract Anniversary month.

    The anniversary falls at the **end** of month t, when ``duration_mth(t) + 1`` elapsed
    policy months is a whole number of years. False outside cover, tested first, where
    ``VA_US_S`` tests ``t`` against its frame.
    """
    return is_active(t) and (duration_mth(t) + 1) % 12 == 0


def is_quarterly_anniv(t):
    """True at a Contract Quarterly Anniversary, at the end of month t **[std]**.

    False outside cover, tested first, where ``VA_US_S`` tests ``t`` against its frame.
    """
    return is_active(t) and (duration_mth(t) + 1) % 3 == 0


def is_year_start(t):
    """True in the first month of a contract year, where SumW_y resets [S1].

    False outside cover, tested first, where ``VA_US_S`` tests ``t >= 0``.
    """
    return is_active(t) and duration_mth(t) % 12 == 0


def anniv_mth(t):
    """The month that **closes** the contract year of month ``t``, on the valuation clock.

    ``t + 11 - duration_mth(t) % 12``: the month of the frame whose policy month is the
    year's last, at whose end the anniversary falls; ``t`` itself where :func:`is_anniv`
    is true. It lies at most 11 months after ``t``, inside the frame, since cover ends at
    the close of a contract year. :func:`lapse_wd_factor` reads the withdrawal year there,
    the one read in the model that reaches past ``t + 1``.
    """
    return t + 11 - duration_mth(t) % 12


def year_open_mth(t):
    """The month whose **closing** value opens the contract year of month ``t``.

    ``t - 1 - duration_mth(t) % 12``, on the valuation clock: the anniversary month that
    precedes the year, ``t - 1`` in a year's first month. Before ``t = 0`` for the year
    under way at the valuation date on a contract valued in force mid-year, and before the
    issue month in a contract's first year, so :func:`rb_prior_anniv_pp` and
    :func:`stepup_base_pp` read the frame at it only where it is at or after
    :func:`t_entry`.
    """
    return t - 1 - duration_mth(t) % 12


def t_of_month(m):
    """The projection index t of the policy month with m months elapsed.

    ``m`` is 0-based, like :func:`duration_mth`: ``t_of_month(0)`` is the first policy
    month, the issue month. It is negative for a policy month before the valuation date,
    and no cell reads a month it gives before :func:`t_entry`: :func:`is_wd_year` takes the
    year's first month as the lower bound of its scan, clipped at :func:`t_entry`, and
    :func:`vix_sq` is read only for quarters on the books.
    """
    return m - duration_mth_init()


def phase(t):
    """The phase at month t, a code: PRE_ISSUE, ACCUM, DEPLETED or EXPIRED.

    ``PRE_ISSUE`` before issue and ``EXPIRED`` from the end of cover, outside cover; in
    cover ``DEPLETED`` once the account value has run out with the GLWB alive and
    ``ACCUM`` before. ``VA_US_S``'s labels, each an int Reference here (R10, the Space
    docstring's *Codes*), and a leaf: no cell, report or check reads it, the projection's
    state being :func:`depleted_flag`.
    """
    if not is_active(t):
        return PRE_ISSUE if t < t_entry() else EXPIRED                # noqa: F821
    return DEPLETED if depleted_flag(t) else ACCUM                   # noqa: F821


def inv_return_mth(t, i):
    """r_i(t): the gross monthly fund return of subaccount i, a scenario input.

    Read from *return_scenario_sec.csv* as a step function of ``t``, the **valuation**
    month, so a flat path is one row per subaccount: the return is the last row of the
    point's scenario at or before ``t`` for subaccount ``i``. A market path runs in
    calendar time, shared by every point of a block, so each row of the model point table
    reads its own copy of ``VA_US_S``'s path, re-based to its months in force
    (``Data.return_scenario``), and the copy of a contract issued at the valuation date is
    ``VA_US_S``'s own, its policy month being ``t``. VM-21 requires each variable
    subaccount to be mapped to a crafted proxy fund, normally a linear combination of
    recognized market indices [R1]; the model takes the return series as an input rather
    than hard-coding one.

    ``Data`` holds the scenarios step-filled by valuation month, ``Data.return_array``, at
    the row :func:`return_scenario_number` gives the point's ``scenario_id``, the column
    of subaccount id ``i`` and the month, to ``Data.read_last_mth``, 1,141, the last a
    read reaches; a month past it, which no projection reads, raises, naming the point,
    and so does an id outside 1 to ``Data.read_last_sub_id``. ``VA_US_S`` reads a month
    before the scenario's first row at its issue month, ``max(duration_mth(t), 0)``. Here
    a month with no row at or before it raises, naming the point
    (``Data.return_first_mths``): ``Data`` refuses a point whose scenario sets no return
    for a subaccount of its fund set by its first month on the books, and no cell reads
    the return outside cover, so the raise is the guard behind that refusal.
    """
    if i < 1 or i > data.read_last_sub_id:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: subaccount ids are held from 1 to "
                         f"{data.read_last_sub_id}, Data.read_last_sub_id; there is no "
                         f"subaccount {i}")
    s = return_scenario_number()
    if t < data.return_first_mths()[s, i]:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: the return scenario sets no return "
                         f"for subaccount {i} by month {t}")
    if t > data.read_last_mth:                                       # noqa: F821
        raise ValueError(f"point_id {point_id()}: the return scenarios are held to month "
                         f"{data.read_last_mth}, Data.read_last_mth, and no projection "
                         f"reads month {t}")
    return float(data.return_array()[s, i, t])                       # noqa: F821


def scenario_rate(t, name):
    """Step-function lookup of column ``name`` in the model point's rate scenario.

    Each row of *rate_scenario_sec.csv* states the level that holds from its own
    **valuation** month — the file's 0-based ``t`` column — until the next row of the same
    scenario, so a flat path is one row, keyed ``t = 0`` for a contract on the books at the
    valuation date. Each row of the model point table reads its own copy of ``VA_US_S``'s
    path, re-based to its months in force, as :func:`inv_return_mth` reads the returns.

    ``Data`` holds the scenarios step-filled by valuation month, ``Data.vix_sq_array`` and
    ``Data.cmt10_array``, at the row :func:`rate_scenario_number` gives the point's
    ``scenario_id``, to ``Data.read_last_mth``; a month past it, which no projection
    reads, raises, naming the point. A month with no row at or before it raises, naming
    the point (``Data.rate_first_mths``): ``Data`` refuses a point on the ``vix`` fee or
    the ``cmt_linked`` roll-up whose scenario sets no level by its first month on the
    books, and only those read it. ``name`` is the column's code, ``VIX_SQ`` or ``CMT10``,
    ``VA_US_S``'s ``"vix_sq"`` and ``"cmt10"`` upper-cased; any other raises
    ``ValueError("invalid name")``.
    """
    s = rate_scenario_number()
    if t < data.rate_first_mths()[s]:                                # noqa: F821
        raise ValueError(f"point_id {point_id()}: the rate scenario sets no level by "
                         f"month {t}")
    if t > data.read_last_mth:                                       # noqa: F821
        raise ValueError(f"point_id {point_id()}: the rate scenarios are held to month "
                         f"{data.read_last_mth}, Data.read_last_mth, and no projection "
                         f"reads month {t}")
    if name == VIX_SQ:                                               # noqa: F821
        return float(data.vix_sq_array()[s, t])                      # noqa: F821
    elif name == CMT10:                                              # noqa: F821
        return float(data.cmt10_array()[s, t])                       # noqa: F821
    raise ValueError("invalid name")


def vix_sq(k):
    """The quarterly average of daily VIX-squared for contract quarter k [S4][S6].

    Read at the last month of the quarter, which is the month with ``3k - 1`` elapsed
    policy months. Used only by the ``vix`` fee reset rule.
    """
    return scenario_rate(t_of_month(3 * k - 1), VIX_SQ)              # noqa: F821


def cmt10(t):
    """The 20-day average 10-year Constant Maturity Treasury rate at month t [S7].

    Used only by the ``cmt_linked`` roll-up rule.
    """
    return scenario_rate(t, CMT10)                                   # noqa: F821


def unit_growth(t, i):
    """The monthly unit value factor of subaccount i.

    ``(1 + r_i(t)) x (1 - e_i/12) x (1 - (m + alpha)/12)`` — a monthly discretization of
    a daily accrual **[std]** [S2]. The fund's own expense and the base contract asset
    charge live **inside** the unit value; charges assessed per contract or on a benefit
    base do not, and are collected by cancelling units instead. Do not additionally
    compound daily: pick one discretization and document it, because reconciling to an
    admin system requires knowing which was used.
    """
    return ((1.0 + inv_return_mth(t, i))
            * (1.0 - fund_expense_rate(i) / 12.0)
            * (1.0 - (asset_charge_me + asset_charge_admin) / 12.0))  # noqa: F821


def sa_pp_at(t, i, timing):
    """SA_i at month t read at the point given by ``timing``; see the Space docstring.

    A withdrawal and a unit cancellation both scale the subaccount by
    ``(1 - amount / AV)`` — pro-rata deduction — so neither moves the value weights.

    ``BEF_PREM`` is the opening balance of month t: the model point's
    :func:`sa_pp_init` in the first month on the books, :func:`t_entry`, and
    ``sa_pp(t - 1, i)`` after it. ``EOM`` is :func:`sa_pp` itself, which carries the
    month's steps one cell a month. 0.0 outside cover and once the contract is depleted
    entering the month, :func:`depleted_open`.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    sa = sa_pp(t - 1, i) if t > t_entry() else sa_pp_init(i)
    if timing == BEF_PREM:
        return sa
    sa = sa + alloc(i) * prem_to_av_pp(t)
    if timing == BEF_WD:
        return sa
    base = av_pp_at(t, BEF_WD)
    sa = sa * (1.0 - wd_pp(t) / base) if base > 0.0 else 0.0
    if timing == BEF_INV:
        return sa
    sa = sa * unit_growth(t, i)
    if timing == BEF_FEE:
        return sa
    if timing == EOM:
        return sa_pp(t, i)
    raise ValueError("invalid timing")


def sa_pp(t, i):
    """SA_i(t): the value of subaccount i per contract at the end of month t.

    The chain of the subaccount, one cell a month: the opening balance,
    ``sa_pp(t - 1, i)``, or :func:`sa_pp_init` at :func:`t_entry`, read first, then the
    month's steps in the notes' order — the premium bought at ``alloc(i)``, the withdrawal
    and the charges cancelling units pro rata, the growth in between — each as
    :func:`sa_pp_at` computes it. ``VA_US_S`` reads ``sa_pp_at(t, i, EOM)``, which reads
    ``sa_pp(t - 1, i)``, two cells a month. 0.0 outside cover and once the contract is
    depleted entering the month.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    sa = sa_pp(t - 1, i) if t > t_entry() else sa_pp_init(i)
    sa = sa + alloc(i) * prem_to_av_pp(t)
    base = av_pp_at(t, BEF_WD)
    sa = sa * (1.0 - wd_pp(t) / base) if base > 0.0 else 0.0
    sa = sa * unit_growth(t, i)
    base = av_pp_at(t, BEF_FEE)
    return sa * (1.0 - charge_pp(t) / base) if base > 0.0 else 0.0


def av_pp_at(t, timing):
    """AV at month t read at the point given by ``timing``: the sum over subaccounts.

    An explicit loop over the positions of the point's set, each id from
    :func:`subaccount_id`, where ``VA_US_S`` sums a generator over ``sub_ids``: the same
    sum, in the same order.
    """
    total = 0.0
    for j in range(subaccount_count()):
        total = total + sa_pp_at(t, subaccount_id(j), timing)
    return total


def av_pp(t):
    """AV(t): the contract value per contract at the end of month t.

    The sum of :func:`sa_pp` over the set's subaccounts, an explicit loop over the
    positions, as :func:`av_pp_at` sums, which is
    ``av_pp_at(t, EOM)``; 0.0 outside cover.
    """
    total = 0.0
    for j in range(subaccount_count()):
        total = total + sa_pp(t, subaccount_id(j))
    return total


def sa_weight(t, i):
    """w_i(t): the value weight of subaccount i, the pro-rata deduction key [S2].

    Read at ``BEF_FEE``, where the notes read it: after the month's growth and before the
    charges that cancel units.
    """
    base = av_pp_at(t, BEF_FEE)
    return sa_pp_at(t, i, BEF_FEE) / base if base > 0.0 else 0.0


def gross_inv_income_pp(t):
    """The gross fund return over month t, before any charge.

    An explicit loop over the positions, as :func:`av_pp_at` sums; 0.0 outside
    cover and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    total = 0.0
    for j in range(subaccount_count()):
        i = subaccount_id(j)
        total = total + sa_pp_at(t, i, BEF_INV) * inv_return_mth(t, i)
    return total


def fund_expense_pp(t):
    """The funds' own expense collected inside the unit value.

    ``Σ_i SA_i(1 + r_i) e_i/12``. **Not insurer revenue** — it is paid to the underlying
    funds — so it never enters :func:`charge_income` or :func:`net_cf`. An explicit loop
    over the positions; 0.0 outside cover and once the contract is depleted entering the
    month.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    total = 0.0
    for j in range(subaccount_count()):
        i = subaccount_id(j)
        total = total + (sa_pp_at(t, i, BEF_INV) * (1.0 + inv_return_mth(t, i))
                         * fund_expense_rate(i) / 12.0)
    return total


def asset_charge_pp(t):
    """The M&E and administrative asset charge collected inside the unit value.

    ``Σ_i SA_i^{pre-charge}(t) (m + alpha)/12`` where the pre-charge value is net of the
    fund's own expense, which is deducted first inside :func:`unit_growth`. This is
    insurer charge income. An explicit loop over the positions; 0.0 outside cover and
    once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    rate = (asset_charge_me + asset_charge_admin) / 12.0             # noqa: F821
    total = 0.0
    for j in range(subaccount_count()):
        i = subaccount_id(j)
        total = total + (sa_pp_at(t, i, BEF_INV) * (1.0 + inv_return_mth(t, i))
                         * (1.0 - fund_expense_rate(i) / 12.0) * rate)
    return total


def inv_income_pp(t):
    """The change in AV over month t from investment, net of both per-unit charges.

    ``AV(BEF_FEE) - AV(BEF_INV)``, and identically
    ``gross_inv_income_pp - fund_expense_pp - asset_charge_pp``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return av_pp_at(t, BEF_FEE) - av_pp_at(t, BEF_INV)


def prem_scheduled_pm(m):
    """The gross premium the point's programme schedules at policy month ``m``, else 0.

    ``Data.prem_amount_array`` at the row :func:`txn_number` gives the point's ``txn_id``
    and policy month ``m``, 0.0 at a month the programme has no row for, as
    ``VA_US_S``'s exact-key lookup answers it: a month with no row takes nothing. **The
    key is the elapsed policy month**, on the policy clock, as *transaction_table.csv*
    states it. The table's one reader of the premium; :func:`prem_scheduled_pp` calls it
    in cover only. A month below 0 is no row, 0.0, before the array is read; one past
    ``Data.read_last_mth``, which no projection reads, raises, naming the point.
    """
    if m < 0:
        return 0.0
    if m > data.read_last_mth:                                       # noqa: F821
        raise ValueError(f"point_id {point_id()}: the programmes are held to policy month "
                         f"{data.read_last_mth}, Data.read_last_mth, and no projection "
                         f"reads policy month {m}")
    return float(data.prem_amount_array()[txn_number(), m])          # noqa: F821


def prem_scheduled_pp(t):
    """The gross premium scheduled for month t in *transaction_table.csv*, else zero.

    The file's ``t`` column is the **elapsed** policy month, so the key is
    ``duration_mth(t)``, read through :func:`prem_scheduled_pm`; the
    programme stays on the policy clock. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return prem_scheduled_pm(duration_mth(t))


def premium_pp(t):
    """P(t): the gross premium paid at BOM of month t.

    The model point's single purchase payment falls at the beginning of the issue month,
    the one with ``duration_mth(t) = 0``, together with anything scheduled for that month
    in *transaction_table.csv*. The chassis is flexible-premium [S1][S2] and premium
    receipt is retained as an active term in every guarantee-base recursion, so a
    subsequent payment is a data change rather than a formula change. ``VA_US_S`` takes
    the single premium at ``t == 0``, which is the issue month of its new business; a
    contract in force at the valuation date paid it before the frame. 0.0 outside cover
    and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    single = premium_single() if duration_mth(t) == 0 else 0.0
    return single + prem_scheduled_pp(t)


def prem_to_av_pp(t):
    """P(t)(1 - tau): the net premium that buys units and raises the guarantee bases.

    The per-contract counterpart of :func:`prem_to_av`, and the name every
    account-value model in this library uses for the premium credited to the account
    value. Not to be confused with ``WholeLife_US_S.premium_net_pp``, which is a *gross*
    premium net of the dividend offset — a different concept entirely.
    """
    return premium_pp(t) * (1.0 - premium_tax_rate())


def wd_scheduled_pm(m):
    """The gross withdrawal the point's programme schedules at policy month ``m``, else 0.

    ``Data.wd_amount_array`` at the row :func:`txn_number` gives the point's ``txn_id``
    and policy month ``m``, as :func:`prem_scheduled_pm` reads the premium: the elapsed
    policy month, on the policy clock. The table's one reader of the withdrawal;
    :func:`wd_scheduled_pp` calls it in cover only.
    """
    if m < 0:
        return 0.0
    if m > data.read_last_mth:                                       # noqa: F821
        raise ValueError(f"point_id {point_id()}: the programmes are held to policy month "
                         f"{data.read_last_mth}, Data.read_last_mth, and no projection "
                         f"reads policy month {m}")
    return float(data.wd_amount_array()[txn_number(), m])            # noqa: F821


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *transaction_table.csv*, else zero.

    Keyed on the **elapsed** policy month ``duration_mth(t)``, as
    :func:`prem_scheduled_pp` is, through :func:`wd_scheduled_pm`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_scheduled_pm(duration_mth(t))


def is_wd_month(t):
    """True when the GLWB utilization withdrawal falls in month t.

    Base run **[std]**: the contract activates in the first month of the contract year in
    which the attained age reaches :func:`wd_start_age`, and withdraws in the first month
    of every contract year thereafter. ``wd_start_age = 0`` never withdraws. False outside
    cover and once the contract is depleted entering the month.
    """
    if not is_active(t) or wd_start_age() <= 0:
        return False
    if depleted_open(t) or not is_year_start(t):
        return False
    return age(t) >= wd_start_age()


def is_wd_taken(t):
    """True when any withdrawal is taken in month t, before its amount is known.

    Stated as a predicate rather than ``wd_pp(t) > 0`` so that the first-withdrawal test
    can run *before* the GAWA% is fixed, which is what the amount itself depends on.
    False outside cover and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t):
        return False
    return wd_scheduled_pp(t) > 0.0 or is_wd_month(t)


def has_wd_by(t):
    """True when a withdrawal has been taken at or before month t.

    The value carried into month t is :func:`has_wd_init` in the first month on the
    books, :func:`t_entry`, the model point's own status, and ``has_wd_by(t - 1)`` after
    it. False outside cover.
    """
    if not is_active(t):
        return False
    prior = has_wd_by(t - 1) if t > t_entry() else has_wd_init()
    return prior or is_wd_taken(t)


def is_first_wd(t):
    """True in the month of the contract's first withdrawal.

    The notes are explicit that this test must run **before** the annual limit ``L`` is
    formed: a first withdrawal tested against ``GAWA = 0`` would score entirely as excess
    and wreck both benefit bases [S1]. The status carried in is read as :func:`has_wd_by`
    reads it, from :func:`has_wd_init` at :func:`t_entry`.
    """
    return is_wd_taken(t) and not (has_wd_by(t - 1) if t > t_entry() else has_wd_init())


def is_wd_year(t):
    """True when any withdrawal falls in the contract year containing month t.

    Drives the VM-21 withdrawal-year surrender factor ``kappa`` [R1] and the rule that
    *any* withdrawal in a Contract Year kills that year's bonus [S1].

    The year's months on the books are scanned by an explicit loop, from its first month,
    or :func:`t_entry` if later, to its last inside the frame; where the year opened before
    the valuation date, its months before ``t = 0`` are the model point's
    :func:`wd_this_year_init`, which answers True for the year by itself. ``VA_US_S``
    scans from ``t = 0``, as though no year had begun before its frame. It is read at a
    year's last month only, by :func:`bonus_pp` at the anniversary and by
    :func:`lapse_wd_factor` at :func:`anniv_mth`, so the scan reaches no month after its
    own. Called at another month of the year, as C4's full sweep calls every cell at
    every month, it answers the same and scans the year's months after it, inside the
    frame: a read past ``t + 1`` that no cell of the model makes. False outside cover.
    """
    if not is_active(t):
        return False
    first = t_of_month(12 * (policy_year(t) - 1))
    if first < t_entry() and wd_this_year_init():
        return True
    for u in range(max(t_entry(), first), min(first + 12, proj_len())):
        if is_wd_taken(u):
            return True
    return False


def gawa_pct_at_age(a):
    """g(a): the GAWA% for attained age a, from *gawa_pct_table.csv* [S3].

    The band starting at the largest ``age_from`` at or below ``a``, ``Data.gawa_pct_array``
    at the row :func:`gawa_grid_number` gives the point's ``glwb_option`` and the age;
    0.0 below the grid's first band, ``VA_US_S``'s value there, and at a negative age,
    before the array is read. Called in cover only, at :func:`age`. The array holds ages
    to ``Data.read_last_age``, 120; an older age reads the rate there where the grid's
    last band starts at or below it, since every age from that band on reads its rate, and
    raises, naming the point, where the last band starts past it, which no projection
    reads.
    """
    g = gawa_grid_number()
    if a < 0:
        return 0.0
    if a > data.read_last_age:                                       # noqa: F821
        if data.gawa_last_band()[g] > data.read_last_age:            # noqa: F821
            raise ValueError(f"point_id {point_id()}: the GAWA% grids are held to age "
                             f"{data.read_last_age}, Data.read_last_age, and no "  # noqa
                             f"projection reads age {a}")
        a = data.read_last_age                                       # noqa: F821
    return float(data.gawa_pct_array()[g, a])                        # noqa: F821


def wd_limit_pp(t):
    """L(t) = max(GAWA, RMD): the annual withdrawal limit governing month t [S1].

    At the first withdrawal the GAWA is fixed on the **pre-withdrawal** GWB, so the limit
    is formed from that. The RMD term is disclosed but inactive: the base run is
    non-qualified and no RMD module is implemented. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_first_wd(t):
        return gawa_pct_at_age(age(t)) * gwb_pp_at(t, BEF_WD)
    return gawa_pp_at(t, BEF_WD)


def wd_glwb_pp(t):
    """The GLWB utilization withdrawal: ``wd_intensity x L(t)`` once activated **[std]**."""
    return wd_intensity() * wd_limit_pp(t) if is_wd_month(t) else 0.0


def wd_pp_due(t):
    """The gross withdrawal requested at BOM of month t, before capping at AV.

    Scheduled withdrawals **add to** the utilization withdrawal, which is how a model
    point exercises the excess algebra without disturbing the base run. 0.0 outside cover
    and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t):
        return 0.0
    return wd_scheduled_pp(t) + wd_glwb_pp(t)


def wd_pp(t):
    """W(t): the gross amount removed from the contract value at BOM of month t.

    Measured **inclusive of withdrawal charges, MVAs, advisory fees and every other
    charge** for all guarantee calculations [S1]; using net proceeds would understate the
    benefit-base reduction. Capped at the available contract value **[std]**.

    Each operand of the ``min`` that calls a cell is a local, assigned in ``VA_US_S``'s
    order of evaluation, left to right, since a compiled ``min`` or ``max`` evaluates its
    arguments right to left: so a point that reaches two refusals raises ``VA_US_S``'s first
    in both engines.
    """
    due = wd_pp_due(t)
    held = av_pp_at(t, BEF_WD)
    return min(due, held)


def sum_wd_pp(t):
    """SumW_y: cumulative withdrawals in the current contract year, including W(t) [S1].

    Restarts at 0 in a contract year's first month. Where the year under way at the
    valuation date opened before it, the sum carried into ``t = 0`` is the model point's
    :func:`sum_wd_pp_ytd_init`; ``VA_US_S`` restarts the sum at ``t == 0`` as though a
    year began there. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_year_start(t):
        prev = 0.0
    elif t > t_entry():
        prev = sum_wd_pp(t - 1)
    else:
        prev = sum_wd_pp_ytd_init()
    return prev + wd_pp(t)


def wd_excess_pp(t):
    """E(t) = min(W, SumW_y - L) if SumW_y > L else 0: the excess withdrawal [S1].

    This is the **guarantee** excess, not the charge base — see the Space docstring's
    note on the divergence from :mod:`.MYGA_US_S`.
    """
    if wd_pp(t) <= 0.0:
        return 0.0
    over = sum_wd_pp(t) - wd_limit_pp(t)
    return min(wd_pp(t), over) if over > 0.0 else 0.0


def wd_nonexcess_pp(t):
    """N(t) = W(t) - E(t): the guaranteed portion of the withdrawal [S1]."""
    return wd_pp(t) - wd_excess_pp(t)


def cv_pre_excess_pp(t):
    """CV_pre: the contract value after the non-excess portion has been deducted [S1].

    The order is decisive: the non-excess portion reduces the base dollar-for-dollar
    **first**, and the proportional factor for the excess is computed against the
    contract value *after* that reduction. Reversing it changes both GWB and GAWA.
    """
    return av_pp_at(t, BEF_WD) - wd_nonexcess_pp(t)


def excess_factor(t):
    """``1 - E(t)/CV_pre``: the pro-rata factor applied to GWB, GAWA and BB [S1]."""
    base = cv_pre_excess_pp(t)
    if base <= 0.0:
        return 0.0
    return max(0.0, 1.0 - wd_excess_pp(t) / base)


def free_wd_allow(t):
    """The charge-free amount at month t: earnings first, then 10% of Remaining Premium.

    The notes state it as ``max(0, AV - RP)`` plus ``max(0, 0.10 RP - earnings)``, which
    is ``max(earnings, 0.10 x RP)`` [S1]. Aged-out premium is free too, which the CDSC
    scale delivers by reaching 0.0% at seven completed years [S2]. The Remaining Premium
    carried into the month is :func:`rp_pp_init` at :func:`t_entry`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    rp = (rp_pp(t - 1) if t > t_entry() else rp_pp_init()) + premium_pp(t)
    earnings = max(0.0, av_pp_at(t, BEF_WD) - rp)
    return max(earnings, free_wd_rate * rp)                          # noqa: F821


def free_wd_avail(t):
    """The free-withdrawal allowance still unused in the contract year at BOM of month t.

    The allowance used before the month is 0 in a contract year's first month,
    ``free_wd_used_cum_pp(t - 1)`` after it, and at ``t = 0``, where the year under way
    opened before the valuation date, the model point's
    :func:`free_wd_used_cum_pp_ytd_init`; ``VA_US_S`` takes 0 at ``t == 0``. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if is_year_start(t):
        used = 0.0
    elif t > t_entry():
        used = free_wd_used_cum_pp(t - 1)
    else:
        used = free_wd_used_cum_pp_ytd_init()
    return max(0.0, free_wd_allow(t) - used)


def wd_free_pp(t):
    """The free-allowance portion of month t's withdrawal: ``min(FW, E(t))``.

    The chassis name for the same thing — :mod:`.MYGA_US_S` has
    ``min(W, FW)`` — differing only in that here the allowance is applied to the
    *guarantee excess* rather than to the whole withdrawal, because the non-excess
    portion is already exempt from the CDSC under the within-``L`` rule [S1]. The
    portion of ``W(t)`` bearing no charge *at all* is therefore the wider
    :func:`wd_exempt_pp`, not this cell.

    Each operand of the ``min`` that calls a cell is a local, assigned in ``VA_US_S``'s
    order of evaluation, left to right, since a compiled ``min`` or ``max`` evaluates its
    arguments right to left: so a point that reaches two refusals raises ``VA_US_S``'s first
    in both engines.
    """
    avail = free_wd_avail(t)
    excess = wd_excess_pp(t)
    return min(avail, excess)


def free_wd_used_cum_pp(t):
    """The free allowance consumed so far in the contract year, including month t.

    The year-to-date cumulative of :func:`wd_free_pp`, reset at each contract year
    start; it is what :func:`free_wd_avail` and :func:`surr_free_pp` net off. Where the
    year under way at the valuation date opened before it, the cumulative carried into
    ``t = 0`` is the model point's :func:`free_wd_used_cum_pp_ytd_init`. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if is_year_start(t):
        prev = 0.0
    elif t > t_entry():
        prev = free_wd_used_cum_pp(t - 1)
    else:
        prev = free_wd_used_cum_pp_ytd_init()
    return prev + wd_free_pp(t)


def wd_exempt_pp(t):
    """The portion of W(t) bearing no withdrawal charge at all.

    Two exemptions stack: **no CDSC applies to cumulative withdrawals within L** [S1],
    which covers the non-excess portion outright, and the free-withdrawal allowance
    covers part of what is left. So this is identically
    ``wd_nonexcess_pp(t) + wd_free_pp(t)``, and it — not :func:`wd_free_pp` — is what
    complements :func:`wd_chargeable_pp`.

    Each operand of the ``min`` that calls a cell is a local, assigned in ``VA_US_S``'s
    order of evaluation, left to right, since a compiled ``min`` or ``max`` evaluates its
    arguments right to left: so a point that reaches two refusals raises ``VA_US_S``'s first
    in both engines.
    """
    w = wd_pp(t)
    cap = wd_nonexcess_pp(t) + free_wd_avail(t)
    return min(w, cap)


def wd_chargeable_pp(t):
    """The portion of W(t) exposed to the CDSC: ``max(0, E(t) - free allowance)``."""
    return wd_pp(t) - wd_exempt_pp(t)


def surr_charge_rate_at(k):
    """The withdrawal charge rate of the point's schedule at ``k`` completed years.

    ``Data.surr_charge_rate_array`` at the row :func:`cdsc_number` gives the point's
    ``cdsc_schedule`` and ``min(k, last)``, where ``last`` is the schedule's last year,
    ``Data.cdsc_last_years``: the last row holds for every later year, as ``VA_US_S`` caps
    the year at the table's largest. The table's one reader; :func:`surr_charge_rate`
    calls it in cover only, at :func:`duration`. A count below 0 raises ``ValueError``,
    naming the point, where ``VA_US_S``'s lookup raised ``KeyError``; so does a year past
    the 95 the array holds, ``Data.read_last_mth // 12``, which no projection reads.
    """
    c = cdsc_number()
    if k < 0:
        raise ValueError(f"point_id {point_id()}: the withdrawal charge scale gives no "
                         f"rate at {k} completed years")
    last = data.cdsc_last_years()[c]                                 # noqa: F821
    y = min(k, last)
    if y > data.read_last_mth // 12:                                 # noqa: F821
        raise ValueError(f"point_id {point_id()}: the withdrawal charge scales are held to "
                         f"{data.read_last_mth // 12} completed years, and no projection "
                         f"reads {y}")
    return float(data.surr_charge_rate_array()[c, y])                # noqa: F821


def surr_charge_rate(t):
    """The CDSC rate at month t, read off the **contract duration** [S2].

    The scale runs 8.5% down to 0.0% at seven completed years and is read from
    *cdsc_table.csv*, keyed by :func:`duration`, through :func:`surr_charge_rate_at`.

    The notes key it on *completed years since receipt of the premium being withdrawn*
    [S2], which coincides with the contract duration only while the contract is single
    premium. It is **not implemented** by premium tranche: :func:`rp_pp` carries Remaining
    Premium as one undifferentiated pool, so a subsequent premium does not restart its
    own charge clock — model point 4 pays a second premium in its 73rd policy month, with
    72 elapsed, and is read at that contract's 6-completed-year band rather than at the
    new tranche's 8.5%. Named in the model docstring's and the README's *not implemented*
    lists and pinned by a test; splitting the pool needs a withdrawal-ordering rule across
    tranches that no retrieved source states. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return surr_charge_rate_at(duration(t))


def wd_charge_pp(t):
    """c(t): the withdrawal charge on month t's withdrawal [S2]."""
    return surr_charge_rate(t) * wd_chargeable_pp(t)


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``W(t) - c(t)``."""
    return wd_pp(t) - wd_charge_pp(t)


def surr_free_pp(t):
    """The charge-free amount left for a full surrender at the end of month t."""
    rp = rp_pp(t)
    earnings = max(0.0, av_pp(t) - rp)
    allow = max(earnings, free_wd_rate * rp)                         # noqa: F821
    return max(0.0, allow - free_wd_used_cum_pp(t))


def surr_chargeable_pp(t):
    """The Remaining Premium withdrawn on a full surrender, net of the free amount [S2].

    Each operand of the outer ``min`` that calls a cell is a local, assigned in
    ``VA_US_S``'s order of evaluation, left to right, since a compiled ``min`` or ``max``
    evaluates its arguments right to left: so a point that reaches two refusals raises
    ``VA_US_S``'s first in both engines.
    """
    rp = rp_pp(t)
    over = max(0.0, av_pp(t) - surr_free_pp(t))
    return min(rp, over)


def surr_charge_pp(t):
    """The CDSC on a full surrender at the end of month t."""
    return surr_charge_rate(t) * surr_chargeable_pp(t)


def surr_benefit_pp(t):
    """Surrender proceeds: ``AV(t)`` less the CDSC.

    There is **no nonforfeiture floor** under this value. NAIC Model #805 expressly
    excludes variable annuities and reaches a VA only through its fixed account under
    Model #250 §7.B [REG-R42][REG-R43], and electing the Roll-up GMDB removes the Fixed
    Account Options [S1]. Contrast :mod:`.MYGA_US_S`, where
    ``max(SV, MGSV)`` is the whole point.
    """
    return av_pp(t) - surr_charge_pp(t)


def phi_glwb(t):
    """phi_G: the annual GLWB rider charge rate in force in month t.

    1.25% of the GWB currently [S3], guaranteed maximum 3.00% **[std]** within an
    observed 1.20%-3.00% band by option and vintage [S1]. ``fee_reset_rule`` selects the
    reset mechanism; the base run does not increase the charge and the owner does not opt
    out **[std]**, because opting out forfeits bonus, step-up and GWB Adjustment and
    blocks future premium [S1], so a rational opt-out is a joint decision rather than an
    independent lapse-style rate. The rule is read through its decodes,
    :func:`is_fee_reset_none`, :func:`is_fee_reset_quinquennial` and
    :func:`is_fee_reset_vix`, in ``VA_US_S``'s order. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_fee_reset_none():
        return phi_glwb_curr                                         # noqa: F821
    elif is_fee_reset_quinquennial():
        steps = duration(t) // fee_reset_years                       # noqa: F821
        return min(phi_glwb_max,                                     # noqa: F821
                   phi_glwb_curr + fee_increase_max * steps)         # noqa: F821
    elif is_fee_reset_vix():
        return phi_glwb_vix(contract_quarter(t))
    else:
        raise ValueError("invalid fee_reset_rule")


def fee_rate_vix_raw(phi_0, vix_sq_avg):
    """The unclipped VIX-squared fee formula [S4][S6].

    ``phi_0 + 0.05% x [ QuarterlyAverage(daily VIX^2) / 33 - 10 ]``. The disclosed
    examples are an initial 1.45% with a quarterly average of 204.42 giving 1.26%, and
    602.30 giving an unclipped 1.86%.

    ``VA_US_S``'s cell, an engine cell (the Space docstring's *Reporting cells*), called by
    no other: :func:`phi_glwb_vix` writes it inline.
    """
    return phi_0 + vix_fee_coef * (vix_sq_avg / vix_divisor - vix_offset)  # noqa: F821


def fee_rate_vix_clip(prior, raw):
    """Clip a VIX-formula rate to the movement band and the absolute corridor [S4].

    The band is +/-0.40% annualized against the prior quarter's rate (advisory class) and
    the corridor is [0.60%, 2.50%]. The second disclosed example clips to 1.82% against a
    prior rate of 1.42%.

    ``VA_US_S``'s cell, an engine cell, called by no other: :func:`phi_glwb_vix` writes it
    inline.
    """
    lo = max(vix_corridor_lo, prior - vix_band)                      # noqa: F821
    hi = min(vix_corridor_hi, prior + vix_band)                      # noqa: F821
    return min(hi, max(lo, raw))


def phi_glwb_vix(k):
    """The VIX-formula GLWB charge rate in contract quarter k [S4][S6].

    ``phi_glwb_curr`` in the first quarter; after it, the formula's rate for the quarter's
    VIX-squared average, clipped against the prior quarter's rate. The prior is
    ``phi_glwb_vix(k - 1)``, one cell a quarter, except in the quarter under way at the
    first month on the books, where it is the model point's :func:`phi_glwb_init`: the
    quarters before it are off the books, and ``VA_US_S`` recurses through them from the
    first. That quarter is ``max(duration_mth_init(), 0) // 3 + 1``, a key the model point
    fixes, which is ``contract_quarter(t_entry())`` read without a clock (R2). No quarter
    before it is read.

    ``VA_US_S``'s :func:`fee_rate_vix_raw` and :func:`fee_rate_vix_clip`, written inline
    (R14), in the order ``VA_US_S``'s call evaluates them: the prior, then the quarter's
    VIX-squared average, then the raw rate, then the clip, each ``min`` and ``max`` with
    its operands as :func:`fee_rate_vix_clip` writes them. A ``vix_divisor`` of 0 raises
    Python's ``ZeroDivisionError("float division by zero")`` after the average is read,
    where ``VA_US_S``'s division raises it, since a compiled division by 0 raises with
    another message.
    """
    if k <= 1:
        return phi_glwb_curr                                         # noqa: F821
    if k == max(duration_mth_init(), 0) // 3 + 1:
        prior = phi_glwb_init()
    else:
        prior = phi_glwb_vix(k - 1)
    avg = vix_sq(k)
    if vix_divisor == 0.0:                                           # noqa: F821
        raise ZeroDivisionError("float division by zero")
    raw = phi_glwb_curr + vix_fee_coef * (avg / vix_divisor - vix_offset)  # noqa: F821
    lo = max(vix_corridor_lo, prior - vix_band)                      # noqa: F821
    hi = min(vix_corridor_hi, prior + vix_band)                      # noqa: F821
    return min(hi, max(lo, raw))


def phi_gmdb(t):
    """phi_D: the annual GMDB rider charge rate in force in month t.

    0.90% of the GMDB Benefit Base currently, guaranteed maximum 1.80% [S2][S3]. The
    ``basic`` death benefit is included at no charge [S1][S2], so the rate is zero there,
    read through :func:`is_gmdb_basic`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return 0.0 if is_gmdb_basic() else phi_gmdb_curr                 # noqa: F821


def rollup_pct():
    """rho at election: 6.00% at age 69 or younger, 5.00% from 70 [S3]."""
    if age_at_entry() >= rollup_age_split:                           # noqa: F821
        return rollup_pct_old                                        # noqa: F821
    return rollup_pct_young                                          # noqa: F821


def rollup_rate(t):
    """rho(t): the GMDB roll-up percentage credited at the anniversary ending month t.

    ``fixed`` is the base run [S3]. ``cmt_linked`` is a third carrier's formula rate:
    the 10-year CMT plus 1.00%, or 1.50% before the first withdrawal, rounded to 0.10%,
    floored at 4% and capped at 8% [S7]. The rule is read through its decodes,
    :func:`is_rollup_fixed` and :func:`is_rollup_cmt_linked`. 0.0 outside cover.

    ``VA_US_S`` rounds with ``math.floor(raw / step + 0.5) * step``. Here the floor is the
    float floor division by 1.0, ``v // 1.0``, which is ``math.floor(v)`` as a float for
    every finite ``v`` in both engines, exactly, so no number moves and no module is read;
    ``VA_US_S``'s three refusals are written out in its order, a ``cmt_round_step`` of 0,
    ``ZeroDivisionError("float division by zero")``, then a ``v`` that is NaN,
    ``ValueError("cannot convert float NaN to integer")``, or infinite,
    ``OverflowError("cannot convert float infinity to integer")``, each with Python's
    message.
    """
    if not is_active(t):
        return 0.0
    if is_rollup_fixed():
        return rollup_pct()
    elif is_rollup_cmt_linked():
        spread = cmt_spread if has_wd_by(t) else cmt_spread_predraw  # noqa: F821
        raw = cmt10(t) + spread
        step = cmt_round_step                                        # noqa: F821
        if step == 0.0:
            raise ZeroDivisionError("float division by zero")
        v = raw / step + 0.5
        if v != v:
            raise ValueError("cannot convert float NaN to integer")
        if v - v != 0.0:
            raise OverflowError("cannot convert float infinity to integer")
        rounded = (v // 1.0) * step
        return max(cmt_floor, min(cmt_cap, rounded))                 # noqa: F821
    else:
        raise ValueError("invalid rollup_rule")


def fee_glwb_pp_due(t):
    """Fee_G = (phi_G/4) x GWB at a Contract Quarterly Anniversary [S1][S3].

    The base is the **benefit base, not the account value** — putting the rider fee on
    account value is the most common and most consequential error on this product. The
    fee therefore rises as markets fall, until the account reaches zero, at which point
    it stops [S4]. 0.0 outside cover and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t) or not is_quarterly_anniv(t):
        return 0.0
    return (phi_glwb(t) / 4.0) * gwb_pp_at(t, BEF_ANNIV)


def fee_gmdb_pp_due(t):
    """Fee_D = (phi_D/4) x RB at a Contract Quarterly Anniversary [S2][S3].

    The charge base is the GMDB Benefit Base; the quarterly frequency aligns it with the
    GLWB fee **[std]**, the research file recording quarterly for the GMWB family only.
    0.0 outside cover and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t) or not is_quarterly_anniv(t):
        return 0.0
    return (phi_gmdb(t) / 4.0) * rb_pp_at(t, BEF_ANNIV)


def maint_fee_pp_due(t):
    """f_c: the $35 annual contract fee, waived at a contract value of $50,000 or more.

    Assessed at the Contract Anniversary and deducted proportionally across investment
    divisions [S2]. The waiver is tested on the contract value after the rider fees
    **[std]**, the notes placing the contract fee after them in the processing order.
    0.0 outside cover and once the contract is depleted entering the month.
    """
    if not is_active(t) or depleted_open(t) or not is_anniv(t):
        return 0.0
    after_riders = (av_pp_at(t, BEF_FEE)
                    - fee_glwb_pp_due(t) - fee_gmdb_pp_due(t))
    return 0.0 if after_riders >= maint_fee_waiver_av else maint_fee  # noqa: F821


def charge_pp_due(t):
    """The total unit cancellation due at EOM before capping at the contract value."""
    return fee_glwb_pp_due(t) + fee_gmdb_pp_due(t) + maint_fee_pp_due(t)


def charge_scale(t):
    """The fraction of the charges due that the contract value can actually pay **[std]**.

    Charges are collected only up to the available contract value; the shortfall is not
    carried forward. This binds in at most one month per contract, the one in which the
    account is exhausted, and it is what makes :func:`check_av_roll_fwd` close there.
    """
    due = charge_pp_due(t)
    if due <= 0.0:
        return 0.0
    return min(1.0, av_pp_at(t, BEF_FEE) / due)


def fee_glwb_pp(t):
    """The GLWB rider fee actually collected in month t."""
    return fee_glwb_pp_due(t) * charge_scale(t)


def fee_gmdb_pp(t):
    """The GMDB rider fee actually collected in month t."""
    return fee_gmdb_pp_due(t) * charge_scale(t)


def maint_fee_pp(t):
    """The annual contract fee actually collected in month t."""
    return maint_fee_pp_due(t) * charge_scale(t)


def charge_pp(t):
    """The total unit cancellation at EOM of month t: the two rider fees and f_c."""
    return charge_pp_due(t) * charge_scale(t)


def charge_income_pp(t):
    """Insurer charge income per contract in month t.

    The asset charge collected inside the unit value plus the charges collected by unit
    cancellation. The funds' own expense is **not** included — it is paid to the funds.
    """
    return asset_charge_pp(t) + charge_pp(t)


def gwb_pp_at(t, timing):
    """GWB at month t read at ``BEF_PREM``, ``BEF_WD`` or ``BEF_ANNIV`` [S1].

    ``BEF_PREM`` is the opening balance of month t: the model point's
    :func:`gwb_pp_init` in the first month on the books, :func:`t_entry`, and
    ``gwb_pp(t - 1)`` afterwards. Once the contract is depleted entering the month every
    timing is that opening balance. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    g = gwb_pp(t - 1) if t > t_entry() else gwb_pp_init()
    if depleted_open(t):
        return g
    if timing == BEF_PREM:
        return g
    g = min(gwb_cap, g + prem_to_av_pp(t))                           # noqa: F821
    if timing == BEF_WD:
        return g
    if wd_pp(t) > 0.0:
        if sum_wd_pp(t) <= wd_limit_pp(t):
            g = max(g - wd_pp(t), 0.0)
        else:
            g = max((g - wd_nonexcess_pp(t)) * excess_factor(t), 0.0)
    if timing == BEF_ANNIV:
        return g
    raise ValueError("invalid timing")


def bb_pp_bef_anniv(t):
    """The Bonus Base carried into the anniversary events of month t [S1].

    Increased by net premium, set to ``min(GWB_after, BB_before)`` on an excess
    withdrawal, and otherwise unaffected by withdrawals. Applying the bonus does not
    change it. The base carried into the month is :func:`bb_pp_init` at :func:`t_entry`.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = bb_pp(t - 1) if t > t_entry() else bb_pp_init()
    if depleted_open(t):
        return prev
    b = min(gwb_cap, prev + prem_to_av_pp(t))                        # noqa: F821
    if wd_pp(t) > 0.0 and sum_wd_pp(t) > wd_limit_pp(t):
        b = min(gwb_pp_at(t, BEF_ANNIV), b)
    return b


def bonus_pp(t):
    """The GLWB bonus credited at the Contract Anniversary ending month t.

    ``b x BB`` if **no withdrawal was taken in the contract year** and the year is within
    the Bonus Period [S1]. *Any* withdrawal kills the whole year's bonus, including an
    automatic withdrawal or an RMD; pro-rating it for a partial year is wrong. The Bonus
    Period's end carried into the first month on the books is the model point's
    :func:`bonus_end_init` on a contract in force at the valuation date, and
    ``bonus_period_years`` on one issued at or after it.
    """
    if not is_anniv(t) or depleted_open(t):
        return 0.0
    if t > t_entry():
        prev_end = bonus_end(t - 1)
    else:
        prev_end = bonus_end_init() if is_inforce() else bonus_period_years  # noqa: F821
    if policy_year(t) > prev_end or is_wd_year(t):
        return 0.0
    return bonus_pct * bb_pp_bef_anniv(t)                            # noqa: F821


def gwb_pp_aft_bonus(t):
    """GWB after anniversary sub-step 3, the GLWB bonus."""
    return gwb_pp_at(t, BEF_ANNIV) + bonus_pp(t)


def stepup_base_pp(t):
    """The contract value the step-up test is made against [S1][S3].

    ``annual_CV``: the Contract Value at the anniversary. ``highest_quarterly_CV``: the
    highest contract value over the four most recent Contract Quarterly Anniversaries,
    the anniversary month itself and the three quarter ends before it.

    On the highest-quarterly basis the quarter ends on the books, at or after
    :func:`t_entry`, are read from the frame by an explicit loop, and at the anniversary
    closing the contract year under way at the valuation date — the one whose year opened
    before :func:`t_entry`, ``year_open_mth(t) < t_entry()`` — the quarter ends before the
    valuation month are the model point's :func:`stepup_base_pp_ytd_init`, their largest
    account value. ``VA_US_S`` leaves out every quarter end before ``t = 0``. The basis is
    read through its decodes, :func:`is_stepup_annual` and
    :func:`is_stepup_highest_quarterly`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_stepup_annual():
        return av_pp(t)
    elif is_stepup_highest_quarterly():
        best = av_pp(t)
        for j in range(1, 4):
            u = t - 3 * j
            if u >= t_entry():
                best = max(best, av_pp(u))
        if duration_mth_init() > 0 and year_open_mth(t) < t_entry():
            best = max(best, stepup_base_pp_ytd_init())
        return best
    else:
        raise ValueError("invalid stepup_basis")


def is_stepup(t):
    """True when the anniversary step-up fires: the contract value exceeds the GWB [S1]."""
    return is_anniv(t) and stepup_base_pp(t) > gwb_pp_aft_bonus(t)


def gwb_pp_aft_stepup(t):
    """GWB after anniversary sub-step 4, the step-up.

    The **[std]** order — bonus first, then step-up — gives
    ``max(GWB_old + bonus, AV)``; the reverse gives ``max(GWB_old, AV) + bonus``, which
    is strictly more generous. The research file does not settle the interaction, and the
    choice made here follows the one design in the set that states it explicitly [S8].
    Treat the alternative as a first-order sensitivity, not a rounding issue.

    Each operand of the ``max`` that calls a cell is a local, assigned in ``VA_US_S``'s
    order of evaluation, left to right, since a compiled ``min`` or ``max`` evaluates its
    arguments right to left: so a point that reaches two refusals raises ``VA_US_S``'s first
    in both engines.
    """
    if not is_anniv(t):
        return gwb_pp_aft_bonus(t)
    g = gwb_pp_aft_bonus(t)
    cv = stepup_base_pp(t)
    return max(g, cv)


def gwb_adj_year():
    """The contract year of the GWB Adjustment Date [S1].

    The later of the anniversary on or after the Designated Life's 70th birthday and the
    12th Contract Anniversary.
    """
    return max(gwb_adj_min_year, gwb_adj_age - age_at_entry())       # noqa: F821


def is_gwb_adj_date(t):
    """True at the Contract Anniversary that is the GWB Adjustment Date."""
    return is_anniv(t) and policy_year(t) == gwb_adj_year()


def adj_pp_bef_anniv(t):
    """ADJ carried into the anniversary events of month t [S1][S3].

    Initialized at 105% of net premium at endorsement, increased by ``s x P(1-tau)`` for
    premiums before the first anniversary after endorsement and by ``P(1-tau)`` for later
    ones, and **voided without value** by any earlier partial withdrawal.

    "Before the first anniversary after endorsement" is the first twelve policy months,
    ``duration_mth(t) < 12``. The Adjustment carried into the first month on the books is
    the model point's :func:`adj_pp_init`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if has_wd_by(t):
        return 0.0
    rate = gwb_adj_pct if duration_mth(t) < 12 else 1.0              # noqa: F821
    prev = adj_pp(t - 1) if t > t_entry() else adj_pp_init()
    return prev + rate * prem_to_av_pp(t)


def adj_pp(t):
    """ADJ(t): the GWB Adjustment amount at the end of month t; 0 once it terminates.

    The chain of the Adjustment, one cell a month: the Adjustment carried in,
    ``adj_pp(t - 1)`` or :func:`adj_pp_init` at :func:`t_entry`, read first, then
    :func:`adj_pp_bef_anniv`'s steps inline, where ``VA_US_S`` reads that cell, which reads
    ``adj_pp(t - 1)``, two cells a month. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_gwb_adj_date(t) or policy_year(t) > gwb_adj_year():
        return 0.0
    prev = adj_pp(t - 1) if t > t_entry() else adj_pp_init()
    if has_wd_by(t):
        return 0.0
    rate = gwb_adj_pct if duration_mth(t) < 12 else 1.0              # noqa: F821
    return prev + rate * prem_to_av_pp(t)


def gwb_pp(t):
    """GWB(t): the Guaranteed Withdrawal Balance at the end of month t [S1].

    Anniversary sub-steps 5 to 7 finish here: the GWB Adjustment Date test, which raises
    the GWB to the Adjustment only if no withdrawal has ever been taken, and the
    $10,000,000 cap. In the depleted state the balance is run down by each payment when
    the For Life Guarantee is not in effect, and is left alone when it is. The balance
    carried in, ``gwb_pp(t - 1)`` or :func:`gwb_pp_init` at :func:`t_entry`, is read
    first, so a cold call walks the chain one cell a month. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = gwb_pp(t - 1) if t > t_entry() else gwb_pp_init()
    if depleted_open(t):
        return prev if forlife_flag() else max(0.0, prev - glwb_payment_pp(t))
    g = gwb_pp_aft_stepup(t)
    if is_gwb_adj_date(t) and not has_wd_by(t):
        g = max(g, adj_pp_bef_anniv(t))
    return min(gwb_cap, g)                                           # noqa: F821


def bb_pp(t):
    """BB(t): the Bonus Base at the end of month t [S1].

    A step-up sets it to ``max(GWB_after_step-up, BB_before)``; the bonus itself never
    changes it. The base carried in, ``bb_pp(t - 1)`` or :func:`bb_pp_init` at
    :func:`t_entry`, is read first. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = bb_pp(t - 1) if t > t_entry() else bb_pp_init()
    if depleted_open(t):
        return prev
    b = bb_pp_bef_anniv(t)
    if is_stepup(t):
        b = max(gwb_pp_aft_stepup(t), b)
    return min(gwb_cap, b)                                           # noqa: F821


def bonus_end(t):
    """The contract year in which the Bonus Period ends [S1].

    Ten Contract Years from the endorsement effective date, **restarting** on each
    Bonus-Base-increasing step-up occurring on or before the anniversary following the
    Designated Life's 80th birthday. A hard-coded 10-year window from issue materially
    understates the guarantee in rising markets. The end carried into the first month on
    the books is :func:`bonus_end_init` on a contract in force at the valuation date and
    ``bonus_period_years`` on one issued at or after it. The int 0 outside cover.
    """
    if not is_active(t):
        return 0
    if t > t_entry():
        prev = bonus_end(t - 1)
    else:
        prev = bonus_end_init() if is_inforce() else bonus_period_years  # noqa: F821
    if (is_stepup(t) and age_at_anniv(t) <= bonus_restart_age        # noqa: F821
            and gwb_pp_aft_stepup(t) > bb_pp_bef_anniv(t)):
        return policy_year(t) + bonus_period_years                   # noqa: F821
    return prev


def gawa_pct_fixed(t):
    """The GAWA% locked at the first withdrawal; 0 until then [S1].

    If the contract value reaches zero with the percentage not yet fixed, it is fixed at
    the percentage for the attained age at that moment [S1]. The percentage carried into
    the first month on the books is the model point's :func:`gawa_pct_init`. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    prev = gawa_pct_fixed(t - 1) if t > t_entry() else gawa_pct_init()
    if prev > 0.0:
        return prev
    if is_first_wd(t) or depleted_flag(t):
        return gawa_pct_at_age(age(t))
    return 0.0


def gawa_pp_at(t, timing):
    """GAWA at month t read at ``BEF_PREM``, ``BEF_WD`` or ``BEF_ANNIV`` [S1].

    ``BEF_PREM`` is the opening balance of month t: the model point's
    :func:`gawa_pp_init` in the first month on the books, :func:`t_entry`, and
    ``gawa_pp(t - 1)`` after it; the withdrawal status and the GAWA% carried in are read
    the same way, from :func:`has_wd_init` and :func:`gawa_pct_init` there. 0.0 outside
    cover.

    Each operand of the excess's ``min`` that calls a cell is a local, assigned in
    ``VA_US_S``'s order of evaluation, left to right, since a compiled ``min`` or ``max``
    evaluates its arguments right to left: so a point that reaches two refusals raises
    ``VA_US_S``'s first in both engines.
    """
    if not is_active(t):
        return 0.0
    g = gawa_pp(t - 1) if t > t_entry() else gawa_pp_init()
    if depleted_open(t):
        return g
    if timing == BEF_PREM:
        return g
    had_wd = has_wd_by(t - 1) if t > t_entry() else has_wd_init()
    if had_wd and prem_to_av_pp(t) > 0.0:
        pct = gawa_pct_fixed(t - 1) if t > t_entry() else gawa_pct_init()
        g = g + pct * prem_to_av_pp(t)
    if timing == BEF_WD:
        return g
    if is_first_wd(t):
        g = gawa_pct_at_age(age(t)) * gwb_pp_at(t, BEF_WD)
    if wd_pp(t) > 0.0 and sum_wd_pp(t) > wd_limit_pp(t):
        scaled = g * excess_factor(t)
        cap = gwb_pp_at(t, BEF_ANNIV)
        g = min(scaled, cap)
    if timing == BEF_ANNIV:
        return g
    raise ValueError("invalid timing")


def gawa_pp(t):
    """GAWA(t): the Guaranteed Annual Withdrawal Amount at the end of month t [S1].

    After the first withdrawal, both the bonus and the step-up raise it to
    ``max(g x GWB, GAWA)``. If the For Life Guarantee is not in effect and ``GWB < GAWA``
    at a Contract Year end, GAWA is set equal to GWB. The amount carried in,
    ``gawa_pp(t - 1)`` or :func:`gawa_pp_init` at :func:`t_entry`, is read first. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = gawa_pp(t - 1) if t > t_entry() else gawa_pp_init()
    if depleted_open(t):
        return prev
    g = gawa_pp_at(t, BEF_ANNIV)
    if is_anniv(t):
        pct = gawa_pct_fixed(t)
        if has_wd_by(t) and pct > 0.0:
            if bonus_pp(t) > 0.0:
                g = max(pct * gwb_pp_aft_bonus(t), g)
            if is_stepup(t):
                g = max(pct * gwb_pp_aft_stepup(t), g)
        if not forlife_flag() and gwb_pp(t) < g:
            g = gwb_pp(t)
    if g <= 0.0 and depleted_flag(t) and gawa_pct_fixed(t) > 0.0:
        g = gawa_pct_fixed(t) * gwb_pp(t)
    return g


def np_pp(t):
    """NP(t): cumulative Net Premiums, a floor under the death benefit [S1].

    Updated by premium only, as the notes' state table has it: it is never reduced for a
    withdrawal. Under the ``rollup`` and ``ratchet`` elections it is therefore an unreduced
    floor beneath ``DB``. Under ``gmdb_option = "basic"`` the elected form is itself the
    proportional return of premium — carried on :func:`rb_pp`, which *does* fall with a
    withdrawal — and this cell is not layered over it, or the election would have no
    effect at all. See :func:`gmdb_guarantee_pp`. The amount carried into the first month
    on the books is the model point's :func:`np_pp_init`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = np_pp(t - 1) if t > t_entry() else np_pp_init()
    if depleted_open(t):
        return prev
    return prev + prem_to_av_pp(t)


def rp_reduction_pp(t):
    """The premium portion of month t's withdrawal, earnings coming out first **[std]**.

    The sources state that Remaining Premium falls by "withdrawals of premium including
    withdrawal charges" [S2] and that earnings come out free first [S1], but give no
    algebra; this is the reading that makes the two consistent. The Remaining Premium
    carried into the month is :func:`rp_pp_init` at :func:`t_entry`. 0.0 outside cover.
    """
    if not is_active(t) or wd_pp(t) <= 0.0:
        return 0.0
    rp = (rp_pp(t - 1) if t > t_entry() else rp_pp_init()) + premium_pp(t)
    earnings = max(0.0, av_pp_at(t, BEF_WD) - rp)
    return min(rp, max(0.0, wd_pp(t) - earnings))


def rp_pp(t):
    """RP(t): Remaining Premium, the basis the CDSC is charged on [S2].

    The amount carried in, ``rp_pp(t - 1)`` or :func:`rp_pp_init` at :func:`t_entry`, is
    read first. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = rp_pp(t - 1) if t > t_entry() else rp_pp_init()
    if depleted_open(t):
        return prev
    return max(0.0, prev + premium_pp(t) - rp_reduction_pp(t))


def rb_prior_anniv_pp(t):
    """RB at the Contract Anniversary preceding month t, the d-f-d allowance base [S1].

    That anniversary is the **end** of the month with ``12(y - 1) - 1`` elapsed policy
    months, ``year_open_mth(t)`` on the valuation clock, and the base is read
    three ways. From the frame, :func:`rb_pp` there, where that month is on the books, at
    or after :func:`t_entry`. On a contract in force at the valuation date whose year
    under way opened before it, from the model point's :func:`rb_pp_prev_anniv_init`. And
    in the first contract year of a contract issued at or after the valuation date, by
    ``VA_US_S``'s issue rule: the Benefit Base after the premium taken at the beginning of
    the issue month, ``rb_pp_at(t_entry(), BEF_WD)``. ``VA_US_S`` reads that last value
    wherever the anniversary precedes its frame, which is wrong on a contract in force
    once a premium has been credited after the anniversary and before the valuation
    month. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    u = year_open_mth(t)
    if u >= t_entry():
        return rb_pp(u)
    if duration_mth_init() > 0:
        return rb_pp_prev_anniv_init()
    return rb_pp_at(t_entry(), BEF_WD)


def gmdb_allow_pp(t):
    """The contract year's dollar-for-dollar GMDB withdrawal allowance [S1].

    ``rho x RB`` at the previous anniversary. Withdrawals inside it reduce the Benefit
    Base dollar for dollar; anything above it reduces it proportionally.
    """
    return rollup_rate(t) * rb_prior_anniv_pp(t)


def gmdb_wd_dfd_pp(t):
    """The dollar-for-dollar portion of month t's withdrawal against the allowance [S1].

    The allowance already used in the year is 0 in its first month,
    ``gmdb_dfd_acc_pp(t - 1)`` after it, and at ``t = 0``, where the year under way opened
    before the valuation date, the model point's :func:`gmdb_dfd_acc_pp_ytd_init`;
    ``VA_US_S`` takes 0 at ``t == 0``. Only the ``rollup`` election,
    :func:`is_gmdb_rollup`, reduces dollar for dollar. 0.0 outside cover.

    Each operand of the outer ``min`` that calls a cell is a local, assigned in
    ``VA_US_S``'s order of evaluation, left to right, since a compiled ``min`` or ``max``
    evaluates its arguments right to left: so a point that reaches two refusals raises
    ``VA_US_S``'s first in both engines.
    """
    if not is_active(t) or wd_pp(t) <= 0.0 or not is_gmdb_rollup():
        return 0.0
    if is_year_start(t):
        used = 0.0
    elif t > t_entry():
        used = gmdb_dfd_acc_pp(t - 1)
    else:
        used = gmdb_dfd_acc_pp_ytd_init()
    w = wd_pp(t)
    left = max(0.0, gmdb_allow_pp(t) - used)
    return min(w, left)


def gmdb_wd_excess_pp(t):
    """The portion of month t's withdrawal above the GMDB d-f-d allowance [S1].

    On the ``rollup`` election, :func:`is_gmdb_rollup`; 0.0 on the others and outside
    cover.
    """
    if not is_active(t) or not is_gmdb_rollup():
        return 0.0
    return wd_pp(t) - gmdb_wd_dfd_pp(t)


def gmdb_wd_factor(t):
    """The proportional factor month t's excess GMDB withdrawal accrues **[std]**.

    The notes say the adjustment above the allowance is "proportional to the contract
    value reduction from the excess" but leave the base unstated. The model measures it
    the same way the GLWB does: against the contract value after the dollar-for-dollar
    portion has been deducted.
    """
    if gmdb_wd_excess_pp(t) <= 0.0:
        return 1.0
    base = av_pp_at(t, BEF_WD) - gmdb_wd_dfd_pp(t)
    if base <= 0.0:
        return 0.0
    return max(0.0, 1.0 - gmdb_wd_excess_pp(t) / base)


def gmdb_dfd_acc_pp(t):
    """The dollar-for-dollar reduction accrued so far in the contract year [S1].

    **GMDB withdrawal adjustments are applied at Contract Year end**, not at the
    withdrawal; applying them immediately changes the base the roll-up compounds on.
    Restarts at 0 in a contract year's first month; where the year under way at the
    valuation date opened before it, the accrual carried into ``t = 0`` is the model
    point's :func:`gmdb_dfd_acc_pp_ytd_init`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_year_start(t):
        prev = 0.0
    elif t > t_entry():
        prev = gmdb_dfd_acc_pp(t - 1)
    else:
        prev = gmdb_dfd_acc_pp_ytd_init()
    return prev + gmdb_wd_dfd_pp(t)


def gmdb_factor_acc(t):
    """The proportional factor accrued so far in the contract year **[std]**.

    Restarts at 1 in a contract year's first month; where the year under way at the
    valuation date opened before it, the factor carried into ``t = 0`` is the model
    point's :func:`gmdb_factor_acc_ytd_init`. 1.0 outside cover, no change.
    """
    if not is_active(t):
        return 1.0
    if is_year_start(t):
        prev = 1.0
    elif t > t_entry():
        prev = gmdb_factor_acc(t - 1)
    else:
        prev = gmdb_factor_acc_ytd_init()
    return prev * gmdb_wd_factor(t)


def rb_pp_at(t, timing):
    """RB at month t read at ``BEF_PREM``, ``BEF_WD`` or ``BEF_ANNIV``.

    The ``rollup`` form accrues its withdrawal adjustment and applies it at the Contract
    Year end; the ``ratchet`` and ``basic`` forms reduce the base proportionally at the
    withdrawal itself [S1]. ``BEF_PREM`` is the opening balance, the model point's
    :func:`rb_pp_init` at :func:`t_entry` and ``rb_pp(t - 1)`` after it. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    r = rb_pp(t - 1) if t > t_entry() else rb_pp_init()
    if depleted_open(t):
        return r
    if timing == BEF_PREM:
        return r
    r = r + prem_to_av_pp(t)
    if timing == BEF_WD:
        return r
    if wd_pp(t) > 0.0 and not is_gmdb_rollup():
        base = av_pp_at(t, BEF_WD)
        r = r * max(0.0, 1.0 - wd_pp(t) / base) if base > 0.0 else 0.0
    if timing == BEF_ANNIV:
        return r
    raise ValueError("invalid timing")


def rb_pp(t):
    """RB(t): the GMDB Benefit Base at the end of month t.

    Growth cutoffs are **age-based, not duration-based**: roll-up and ratchet growth stop
    at the Contract Anniversary preceding the oldest Covered Life's 81st birthday [S1],
    so an issue-age-60 cell gets 20 roll-up credits and an issue-age-75 cell gets 5. The
    base carried in, ``rb_pp(t - 1)`` or :func:`rb_pp_init` at :func:`t_entry`, is read
    first, and the election through its decodes, :func:`is_gmdb_rollup`,
    :func:`is_gmdb_ratchet` and :func:`is_gmdb_basic`, in ``VA_US_S``'s order. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    prev = rb_pp(t - 1) if t > t_entry() else rb_pp_init()
    if depleted_open(t):
        return prev
    r = rb_pp_at(t, BEF_ANNIV)
    if not is_anniv(t):
        return r
    if is_gmdb_rollup():
        r = max(0.0, (r - gmdb_dfd_acc_pp(t)) * gmdb_factor_acc(t))
        if age_at_anniv(t) <= gmdb_growth_cutoff_age:                # noqa: F821
            r = r * (1.0 + rollup_rate(t))
    elif is_gmdb_ratchet():
        if age_at_anniv(t) <= gmdb_growth_cutoff_age:                # noqa: F821
            r = max(r, av_pp(t))
    elif is_gmdb_basic():
        pass
    else:
        raise ValueError("invalid gmdb_option")
    return r


def gmdb_guarantee_pp(t):
    """The guarantee actually floored under the death benefit [S1].

    ``max(NP(t), RB(t))`` under the ``rollup`` and ``ratchet`` elections, exactly as the
    notes' ``DB = max(AV, NP, RB)`` reads: there ``NP`` is the *included* return of
    premium and ``RB`` the separately elected base, and the two are different guarantees.

    Under ``basic`` they are the **same** guarantee — the elected form *is* the return of
    premium — and the notes' two tables then contradict each other. The GMDB form table
    reduces it ``G <- G x (1 - W/AV_pre)``, "proportional, **not** dollar-for-dollar",
    while the state table updates ``NP`` by premium alone. Layering the unreduced ``NP``
    over the reduced base would make the emphasized rule unreachable and the election a
    dead switch, so on that election the elected form governs alone **[std]**. The
    README section *The basic GMDB election and the unreduced NP floor* sets out the
    conflict and the choice; :func:`np_pp` still carries cumulative net premiums, and a
    test pins the difference on model point 9. The election is read through
    :func:`is_gmdb_basic`.

    Each operand of the ``max`` that calls a cell is a local, assigned in ``VA_US_S``'s
    order of evaluation, left to right, since a compiled ``min`` or ``max`` evaluates its
    arguments right to left: so a point that reaches two refusals raises ``VA_US_S``'s first
    in both engines.
    """
    if is_gmdb_basic():
        return rb_pp(t)
    net = np_pp(t)
    rb = rb_pp(t)
    return max(net, rb)


def db_pp(t):
    """DB(t) = max(AV(t), NP(t), RB(t)): the **gross** death benefit outflow [S1].

    Zero once the contract value has reached zero with the GLWB in force: all other
    endorsements terminate without value and **no death benefit is payable on subsequent
    death** [S1].

    Each operand of the ``max`` that calls a cell is a local, assigned in ``VA_US_S``'s
    order of evaluation, left to right, since a compiled ``min`` or ``max`` evaluates its
    arguments right to left: so a point that reaches two refusals raises ``VA_US_S``'s first
    in both engines.
    """
    if depleted_flag(t):
        return 0.0
    av = av_pp(t)
    floor = gmdb_guarantee_pp(t)
    return max(av, floor)


def gmdb_claim_pp(t):
    """``max(0, max(NP, RB) - AV)``: the **net general-account strain** on death [S1].

    Project ``DB(t)`` as the outflow and derive this as the strain — never the reverse,
    never both. Projecting only the guarantee excess understates gross benefit outgo and
    breaks reconciliation with statutory exhibits; projecting both double counts.
    """
    if depleted_flag(t):
        return 0.0
    return max(0.0, gmdb_guarantee_pp(t) - av_pp(t))


def forlife_flag():
    """Whether the For Life Guarantee is in effect from issue [S1].

    True when the Designated Life is 59 1/2 or older. On an age-nearest-birthday basis an
    ANB of 60 is exactly an actual age of 59 1/2 or more, so the test is
    ``age_at_entry() >= 60`` with no approximation **[std]**.
    """
    return age_at_entry() >= forlife_age                             # noqa: F821


def depleted_open(t):
    """Whether the contract enters month t depleted: the status at the start of the month.

    ``depleted_flag(t - 1)`` after the first month on the books, and in it, at
    :func:`t_entry`, derived from the opening state: a contract in force at the valuation
    date enters month 0 depleted exactly where its account value carried in,
    :func:`av_pp_init`, is at or below ``av_depletion_threshold``, and new business never
    does. The status is exact so: :func:`depleted_flag` is absorbing, and from the month
    after it is set every subaccount is held at 0, so at each month end the flag is set
    exactly where the account value is at or below the threshold. ``VA_US_S`` reads
    ``depleted_flag(t - 1)`` wherever this is read, below ``t = 0`` in its first month.
    False outside cover.
    """
    if not is_active(t):
        return False
    if t > t_entry():
        return depleted_flag(t - 1)
    return duration_mth_init() > 0 and av_pp_init() <= av_depletion_threshold  # noqa


def depleted_flag(t):
    """True once the contract value has reached zero with the GLWB in force [S1].

    Absorbing: once set it never clears. The threshold is half a cent **[std]** — the
    charge cap in :func:`charge_scale` and the withdrawal cap in :func:`wd_pp` both drive
    the account to zero, or to a rounding of either sign about it, of the order of 1e-14,
    so the threshold only guards floating point. In the first month on the books the
    status carried in is :func:`depleted_open`, read from the opening account value, the
    threshold's test, which reads such a rounding as depleted. False outside cover.
    """
    if not is_active(t):
        return False
    if t > t_entry():
        if depleted_flag(t - 1):
            return True
    elif depleted_open(t):
        return True
    return av_pp(t) <= av_depletion_threshold                        # noqa: F821


def glwb_payment_pp(t):
    """The insurer-funded GLWB payment in month t once the contract is depleted [S1].

    With the For Life Guarantee in effect, GAWA is paid for the life of the Designated
    Life. Without it, payments continue until the earlier of death and GWB depletion, the
    final one truncated to the remaining GWB. The notes place the routine at BOM and the
    payment "at each Contract Anniversary"; the model pays it at the BOM of the first
    month of each contract year **[std]**, the instant just after the anniversary, which
    keeps it on the same clock as the pre-depletion withdrawals.

    The GAWA and the GWB paid on are those carried into the month: ``gawa_pp(t - 1)`` and
    ``gwb_pp(t - 1)``, and at :func:`t_entry` the model point's :func:`gawa_pp_init` and
    :func:`gwb_pp_init`, which is where a contract in force and depleted at the valuation
    date, valued at a contract year's start, takes its first payment. ``VA_US_S`` reads
    ``t - 1`` there, below its frame. 0.0 outside cover.
    """
    if not is_active(t) or not depleted_open(t):
        return 0.0
    if not is_year_start(t):
        return 0.0
    amount = gawa_pp(t - 1) if t > t_entry() else gawa_pp_init()
    if forlife_flag():
        return amount
    return min(amount, gwb_pp(t - 1) if t > t_entry() else gwb_pp_init())


def mort_rate_base_at(x):
    """The table's annual mortality rate at attained age ``x`` and the model point's sex.

    ``Data.mort_table_array`` at the row :func:`mort_schedule` gives the point's ``sex``
    and the column of age ``min(x, top)``, where ``top`` is the table's last age,
    :func:`~.VA_US_SEC.Data.mort_last_age`, as ``VA_US_S`` caps the age at the table's
    largest. The table's one reader, keyed by the age; :func:`mort_rate` calls it in cover
    only, at :func:`age`. ``Data`` refuses a point whose sex the table lacks, or whose
    attained age in its first month on the books it gives no rate at. An age outside the
    sex's rates, which no projection reads, raises ``ValueError`` naming the point, where
    ``VA_US_S``'s lookup raised ``KeyError``; so does one outside the ages the array holds,
    from the table's first, or 0 if that is lower, to ``Data.read_last_age``, 120.
    """
    top = data.mort_last_age()                                       # noqa: F821
    b = min(x, top)
    s = mort_schedule()
    if b < data.mort_age_firsts()[s] or b > data.mort_age_lasts()[s]:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: the mortality table gives no rate at "
                         f"attained age {b}")
    base = data.mort_age_base()                                      # noqa: F821
    if b < base or b > data.read_last_age:                           # noqa: F821
        raise ValueError(f"point_id {point_id()}: the mortality table is held from age "
                         f"{base} to {data.read_last_age}, Data.read_last_age, and no "
                         f"projection reads age {b}")
    return float(data.mort_table_array()[s, b - base])               # noqa: F821


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, from *mort_table.csv*.

    The shipped table is an illustrative annuitant curve **[std]**, *not* a published
    basis. The prescribed basis is the 2012 IAM **Basic** Table improved to December 31,
    2017 on Projection Scale G2, generational, with no further improvement in the
    projection [R1][REG-R59]; it may not be redistributed here, so swap it in by
    repointing ``Data.mort_table_file`` before the model computes anything. **Do not use
    CSO or VBT life tables** — annuitant mortality is a different and generally lighter
    basis [REG-R59].

    The rate is the table's, read at :func:`mort_rate_base_at`, with no factor applied, as
    in ``VA_US_S``, so no rate past 1 can arise and none is capped; ``Data`` refuses a rate
    outside 0 to 1, a blank or text one among them. 0.0 outside cover, before the table is
    read.
    """
    if not is_active(t):
        return 0.0
    return mort_rate_base_at(age(t))


def mort_rate_mth(t):
    """q^d(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """q^w_base(y): VM-21 Table 6.3's "under 50% ITM" column **[std]** [R1].

    4.0% p.a. during the surrender-charge period (contract years 1 to 7 here [S2]),
    25.0% in the first year after it, 15.0% thereafter. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    year = policy_year(t)
    if year <= surr_charge_years:                                    # noqa: F821
        return lapse_rate_sc                                         # noqa: F821
    elif year == surr_charge_years + 1:                              # noqa: F821
        return lapse_rate_shock                                      # noqa: F821
    return lapse_rate_ult                                            # noqa: F821


def moneyness_glwb(t):
    """M_G(t) = GWB(t) / AV(t): the living-benefit in-the-moneyness ratio [R1]."""
    return gwb_pp(t) / av_pp(t) if av_pp(t) > 0.0 else 0.0


def moneyness_gmdb(t):
    """M_D(t) = max(NP(t), RB(t)) / AV(t): the death-benefit moneyness ratio [R1].

    Measured on the guarantee actually floored under ``DB``, not on ``RB`` alone.
    """
    return gmdb_guarantee_pp(t) / av_pp(t) if av_pp(t) > 0.0 else 0.0


def lapse_itm_mult(ratio):
    """lambda(M): the VM-21 §7.B.1 Alternative Methodology multiplier [R1].

    ``min[U, max(L, 1 - Mult (M - D))]`` with U = 1.00, L = 0.50, Mult = 1.25, D = 1.10 —
    the only closed-form dynamic lapse formula the Valuation Manual publishes for VAs.
    Note that it floors suppression at 50% while Table 6.3's own ITM grading implies an
    84% suppression; compose one or the other, never both.

    ``VA_US_S``'s cell, an engine cell, called by no other: :func:`lapse_dyn_mult` writes it
    inline. Its parameter is ``ratio``, ``VA_US_S``'s ``m``, since ``spec_sec.py`` sizes a
    cache by ``m``, a policy month, and a parameter it sizes would compile to C.
    """
    raw = 1.0 - lapse_itm_mult_coef * (ratio - lapse_itm_threshold)  # noqa: F821
    return min(lapse_itm_upper, max(lapse_itm_lower, raw))           # noqa: F821


def lapse_dyn_mult(t):
    """lambda*(t) = min(lambda(M_G), lambda(M_D)) [R1].

    The contract carries both a VAGLB and a GMDB, and VM-21 §6.C.6 directs that such
    contracts use the **lower** of the two ITM-based rates. 1.0 outside cover, no
    adjustment; ``VA_US_S`` reads the multiplier there of an empty account's moneyness.

    ``VA_US_S``'s :func:`lapse_itm_mult` of each moneyness, written inline (R14), its
    operands in ``VA_US_S``'s order: the GLWB's moneyness and its multiplier first, as
    ``VA_US_S``'s call evaluates its first argument first, then the GMDB's, each clamp
    ``min(lapse_itm_upper, max(lapse_itm_lower, raw))`` as :func:`lapse_itm_mult` writes
    it, so that a NaN meets the bound it meets there. So no compiled cell calls the engine
    cell, keyed by a float.
    """
    if not is_active(t):
        return 1.0
    m_g = moneyness_glwb(t)
    raw_g = 1.0 - lapse_itm_mult_coef * (m_g - lapse_itm_threshold)  # noqa: F821
    lam_g = min(lapse_itm_upper, max(lapse_itm_lower, raw_g))        # noqa: F821
    m_d = moneyness_gmdb(t)
    raw_d = 1.0 - lapse_itm_mult_coef * (m_d - lapse_itm_threshold)  # noqa: F821
    lam_d = min(lapse_itm_upper, max(lapse_itm_lower, raw_d))        # noqa: F821
    return min(lam_g, lam_d)


def lapse_wd_factor(t):
    """kappa(t): 0.60 in any contract year with a projected withdrawal, else 1.00 [R1].

    Whether the contract year takes a withdrawal is a property of the year, so it is read
    once, at the month closing the year, ``is_wd_year(anniv_mth(t))``, up to 11 months
    after ``t`` and inside the frame: the same value as ``VA_US_S``'s ``is_wd_year(t)``,
    which scans the whole year from ``t`` on, a read the model admits only at the
    anniversary. The year's answer there rests on no count, no decrement and no later
    month. 1.0 outside cover, no adjustment.
    """
    if not is_active(t):
        return 1.0
    return lapse_wd_year_factor if is_wd_year(anniv_mth(t)) else 1.0  # noqa: F821


def lapse_rate(t):
    """q^w_annual(t) = min[1, base x lambda* x kappa] **[std] composition** [R1].

    The **annual** total surrender rate; :func:`lapse_rate_mth` is the monthly one, the
    pair matching :func:`mort_rate` / :func:`mort_rate_mth`. Zero whenever the contract
    value is zero: the prescribed surrender assumption for a GMWB contract at ``AV = 0``
    is 0% [R1]. This is the single most important behavioural assumption on the product,
    because it determines how many deeply in-the-money contracts persist to become
    claims. The bound of 1 is ``VA_US_S``'s, written first as there, and binds only where
    a base rate is set above 1, the two multipliers being at most 1. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if av_pp(t) <= 0.0:
        return 0.0
    return min(1.0, lapse_rate_base(t) * lapse_dyn_mult(t) * lapse_wd_factor(t))


def lapse_rate_mth(t):
    """q^w(t): the monthly surrender rate, ``1 - (1 - q^w_annual)^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """The in-force count at the **start** of projection month t, after its new business.

    ``pols_if_at(t, BEF_DECR)``: the notes' ``l(t-1)``, and the weight applied to month
    ``t``'s cash flows, so that the ``pols_if`` column of :func:`result_cf` reconciles with
    the row it sits on: ``premiums(t) / premium_pp(t)`` is exactly ``pols_if(t)``. This is
    the library-wide convention, set by :mod:`.Term_US_S` and by ``savings.CashValue_SE``.
    In the issue month it is the count issued, :func:`pols_new_biz`, and on a contract in
    force at the valuation date it opens month 0 at :func:`pols_if_init`.

    The notes' own end-of-month ``l(t)`` is ``pols_if_at(t, AFT_DECR)``. The
    two coincide — ``pols_if_at(t + 1, BEF_NB) == pols_if_at(t, AFT_DECR)`` —
    everywhere but the last covered month, where the survivors leave as
    :func:`pols_maturity` and nothing is in force at the start of the month after it.
    """
    return pols_if_at(t, BEF_DECR)


def pols_if_at(t, timing):
    """In-force at month t read at ``BEF_NB``, ``BEF_DECR``, ``BEF_LAPSE`` or ``AFT_DECR``.

    ``BEF_NB`` is the count carried in from month ``t - 1``, before month ``t``'s new
    business, the chain of the count, one cell a month: :func:`pols_if_init` at
    :func:`t_entry`, and ``(BEF_NB(t-1) + pols_new_biz(t-1)) x (1 - q^d) x (1 - q^w)``
    after it, as ``basiclife.BasicTerm_SE`` rolls it. ``BEF_DECR`` adds the month's new
    business and is ``pols_if(t)``. Then the order is the notes'
    ``l(t) = l(t-1)(1 - q^d(t))(1 - q^w(t))`` — **death first, then surrender**
    **[std]** — and ``AFT_DECR`` is the notes' ``l(t)``, the end-of-month count.
    ``VA_US_S`` rolls ``pols_if(t)`` through ``pols_if_at(t - 1, AFT_DECR)``, two cells a
    month. 0.0 outside cover at every timing.
    """
    if timing == BEF_NB:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1))
                * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1)))
    elif timing == BEF_DECR:
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)
    elif timing == BEF_LAPSE or timing == AFT_DECR:
        if not is_active(t):
            return 0.0
        pols = pols_if_at(t, BEF_DECR) * (1.0 - mort_rate_mth(t))
        if timing == BEF_LAPSE:
            return pols
        return pols * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_new_biz(t):
    """New business in month t: ``policy_count()`` in the issue month, else 0.

    The month with ``duration_mth(t) == 0``, which is :func:`t_entry` on a contract issued
    at or after the valuation date; a contract in force at it has no new business, its
    count entering as :func:`pols_if_init` instead. As ``basiclife.BasicTerm_SE`` takes
    it, the issued count joins ``BEF_NB`` to make ``BEF_DECR``, before the month's
    decrements.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_death(t):
    """Deaths in month t, on the contracts in force at the start of it.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Full surrenders in month t, on the survivors of mortality; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_LAPSE) * lapse_rate_mth(t)


def pols_maturity(t):
    """Survivors carried out at the end of cover; zero in every other month.

    Not a decrement — the projection runs out — but needed for the in-force roll-forward
    to close; see the Space docstring. The month is the last covered one,
    ``duration_mth(t) == maturity_mth() - 1``, a test on the policy clock, where
    ``VA_US_S`` tests ``t == proj_len() - 1``.
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
    """The benefit paid per contract in month t by ``kind``.

    ``DEATH`` is the gross death benefit :func:`db_pp`. ``LAPSE`` is the surrender
    proceeds :func:`surr_benefit_pp`. ``MATURITY`` is the surrender value of the
    survivors at the projection horizon.
    """
    if kind == DEATH:
        return db_pp(t)
    elif kind == LAPSE:
        return surr_benefit_pp(t)
    elif kind == MATURITY:
        return surr_benefit_pp(t)
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The contract value released per contract by a claim of ``kind``.

    Always ``AV(t)``: the separate account gives up the account value, and whatever the
    guarantee adds on top is general-account money, reported as :func:`claims_over_av`.
    The kind is tested by a chain of ``==``, where ``VA_US_S`` tests it in a tuple.
    """
    if kind == DEATH or kind == LAPSE or kind == MATURITY:
        return av_pp(t)
    raise ValueError("invalid kind")


def premiums(t):
    """Premium income in month t, weighted by the contracts in force at the start of it.

    In the issue month ``pols_if(t)`` is the count issued, :func:`pols_new_biz`, so the
    purchase payment on that row needs no special case; a later scheduled premium falls
    on every contract still in force. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return premium_pp(t) * pols_if(t)


def prem_to_av(t):
    """Net premium credited to the block's contract value in month t; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return prem_to_av_pp(t) * pols_if(t)


def asset_charges(t):
    """Charge income from the M&E and administrative asset charge, in-force weighted.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return asset_charge_pp(t) * pols_if(t)


def fees_glwb(t):
    """Charge income from the GLWB rider fee, in-force weighted; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return fee_glwb_pp(t) * pols_if(t)


def fees_gmdb(t):
    """Charge income from the GMDB rider fee, in-force weighted; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return fee_gmdb_pp(t) * pols_if(t)


def maint_fees(t):
    """Charge income from the annual contract fee, in-force weighted; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return maint_fee_pp(t) * pols_if(t)


def wd_charges(t):
    """The CDSC collected on withdrawals, in-force weighted — a **memo line**.

    The notes' ledger lists the withdrawal charge twice: once as charge income ``c(t)``
    and once as a deduction inside withdrawal proceeds ``W(t) - c(t)``. Counting both
    double-counts it. :func:`withdrawals` carries the net proceeds into :func:`net_cf`
    and this line reports the charge separately. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_charge_pp(t) * pols_if(t)


def charge_income(t):
    """Total insurer charge income in month t, excluding the double-counted CDSC."""
    return asset_charges(t) + fees_glwb(t) + fees_gmdb(t) + maint_fees(t)


def withdrawals(t):
    """Withdrawal proceeds ``W(t) - c(t)``, weighted by ``pols_if(t)``.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_payment_pp(t) * pols_if(t)


def glwb_payments(t):
    """Insurer-funded post-depletion GLWB payments, weighted by ``pols_if(t)``.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return glwb_payment_pp(t) * pols_if(t)


def claims(t, kind):
    """Benefit outgo in month t, for one ``kind`` or, with ``ALL``, all three.

    ``ALL`` is ``VA_US_S``'s ``kind=None``, its total ``VA_US_S``'s chain of ``+`` in its
    order, so that the total is ``VA_US_S``'s bit for bit (the Space docstring's
    *Codes*).
    """
    if kind == ALL:                                                  # noqa: F821
        return (claims(t, DEATH) + claims(t, LAPSE)
                + claims(t, MATURITY))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The contract value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind):
    """Benefit paid less the contract value released, ``claims - claims_from_av``.

    On death this is exactly the GMDB guarantee claim — the general-account strain. On a
    surrender it is negative by the withdrawal charge, which the separate account keeps.
    A reconciliation quantity, never a ledger line of its own. ``ALL``, ``VA_US_S``'s
    ``kind=None``, is the three kinds' total, ``VA_US_S``'s chain of ``+``.
    """
    if kind == ALL:                                                  # noqa: F821
        return (claims_over_av(t, DEATH) + claims_over_av(t, LAPSE)
                + claims_over_av(t, MATURITY))
    return claims(t, kind) - claims_from_av(t, kind)


def gmdb_claims(t):
    """The net general-account strain on death, ``GuaranteeClaim x deaths`` — a memo.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return gmdb_claim_pp(t) * pols_death(t)


def commissions(t):
    """Acquisition commission; **0 in the base run [std]**, the notes not modelling it."""
    return comm_rate_acq * premiums(t)                               # noqa: F821


def premium_taxes(t):
    """Premium tax deducted from the purchase payment, 0% **[std]** [S2]."""
    return premium_tax_rate() * premiums(t)


def inflation_factor(t):
    """The VM-21 §6.C.2 expense inflation factor for the projection year containing t.

    ``1.025^(valuation year - 2015 + t // 12)`` [R1]: the years from the expense base year
    to the valuation date, then the whole years of the projection, so that every point's
    maintenance expense in month ``t`` is in the same valuation-date dollars, however old
    the contract. ``VA_US_S`` counts the contract's own years instead, ``duration(t)``,
    which is ``t // 12`` on a contract issued at the valuation date and mixes the two
    clocks on any other.

    The exponent is an int, so a base below 0 gives a real power in both engines. Where
    Python's float power raises, the cell raises Python's message, which a compiled
    ``pow`` would not: a base of 0 to a negative power, ``inflation_rate`` -1 and a
    valuation year before the base year, ``ZeroDivisionError``; and a power past the
    largest float from a finite base, ``OverflowError``.  That last is Python's own float
    power, called where the compiled ``pow`` gives an infinity, so that its message is the
    platform's, ``Numerical result out of range`` on Linux and ``Result too large`` on
    Windows, as Python's is; modelx never reaches it, its own power raising first.
    """
    base = 1.0 + inflation_rate                                      # noqa: F821
    n = valuation_year - expense_base_year + t // 12                 # noqa: F821
    if base == 0.0 and n < 0:
        raise ZeroDivisionError("0.0 cannot be raised to a negative power")
    factor = base ** n
    if factor - factor != 0.0 and base - base == 0.0:
        raise float.__pow__(base, n)
    return factor


def expenses(t):
    """VM-21 §6.C.2 prescribed maintenance expense [R1].

    ``[100 x 1.025^(valuation year - 2015)]/12`` per contract per month, inflating 2.5%
    a year, **plus 7 basis points of projected account value** for a company-administered
    block. Acquisition expense is not modelled in the base run **[std]**; when it is, it
    falls at the beginning of the issue month, the one with ``duration_mth(t) = 0``,
    alongside the purchase payment, per contract issued. ``VA_US_S`` charges it at
    ``t == 0``, which on its point in force at the valuation date is not the issue month.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    acq = expense_acq if duration_mth(t) == 0 else 0.0               # noqa: F821
    per_contract = (expense_maint / 12.0) * inflation_factor(t)      # noqa: F821
    per_av = (expense_av_rate / 12.0) * av_pp(t)                     # noqa: F821
    return (acq + per_contract + per_av) * pols_if(t)


def net_cf(t):
    """The technical notes' cash flow ledger, summed with the notes' own signs.

    Premium income and every charge income line are positive; the gross death benefit,
    surrender and horizon proceeds, withdrawal proceeds, post-depletion GLWB payments and
    maintenance expense are negative. Note what this **is not**: because a VA's separate
    account is legally segregated, this line mixes separate-account movements (premium
    in, benefits out) with transfers into the general account (the charges), and it omits
    investment return entirely, so it does not reconcile to the account value.
    :func:`net_cf_ga` is the insurer's own view; :func:`check_av_roll_fwd` is the
    account-value identity.
    """
    return (premiums(t) + charge_income(t)
            - withdrawals(t) - glwb_payments(t) - claims(t, ALL)
            - expenses(t) - commissions(t) - premium_taxes(t))


def net_cf_ga(t):
    """The general-account view: charge income less guarantee strain and expenses.

    The notes require both the gross death benefit and the net general-account strain and
    say they are not interchangeable. This line assembles the net one: charge income,
    less the GMDB guarantee claim, less insurer-funded post-depletion GLWB payments, less
    expenses, commissions and premium tax. It is the memo, not the ledger.
    """
    return (charge_income(t) - gmdb_claims(t) - glwb_payments(t)
            - expenses(t) - commissions(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted contract value at month t; see :func:`av_pp_at`.

    Every timing inside the month is weighted by the contracts in force at the start of
    it, ``pols_if(t)``. ``EOM`` is weighted by ``pols_if_at(t + 1, BEF_NB)``
    — the count still in force once the month's decrements have gone, before the next
    month's new business — which is zero in the last covered month, where the survivors
    leave as :func:`pols_maturity` and their contract value is released through
    :func:`claims_from_av`.

    The contract value carried into the frame, ``av_pp_init() x pols_if_init()``, is not
    a row of this cell: it is the opening value :func:`av_change` uses in the first
    month on the books, which is what makes :func:`check_av_roll_fwd_resid` close there.
    0.0 outside cover, before ``t + 1`` is read.
    """
    if not is_active(t):
        return 0.0
    if timing == EOM:
        return av_pp(t) * pols_if_at(t + 1, BEF_NB)
    return av_pp_at(t, timing) * pols_if(t)


def inv_income(t):
    """Investment income credited to the block's contract value in month t.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return inv_income_pp(t) * pols_if(t)


def wd_from_av(t):
    """The contract value released by month t's withdrawals, gross of the charge.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_pp(t) * pols_if(t)


def charges_from_av(t):
    """The contract value cancelled by month t's per-contract and benefit-base charges.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return charge_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's contract value over month t.

    The opening value is the carried-in ``av_pp_init() x pols_if_init()`` in the first
    month on the books, :func:`t_entry` — 0 on new business, whose purchase payment is the
    month's net premium in — and ``av_at(t - 1, EOM)`` after it. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = (av_at(t - 1, EOM) if t > t_entry()
               else av_pp_init() * pols_if_init())
    return av_at(t, EOM) - opening


def check_av_roll_fwd_resid(t):
    """Contract value roll-forward residual; zero to floating point in every covered month.

    ``AV(t) - AV(t-1) = net premium in - withdrawals out + investment income net of the
    per-unit charges - the charges collected by unit cancellation - the contract value
    released by each claim kind``. The cash *paid* on a death may exceed the contract
    value released; that excess is :func:`claims_over_av` and is not part of this
    identity. In the first month on the books ``AV(t-1)`` is the carried-in
    ``av_pp_init()``, so a purchase payment appears on that row as net premium in.

    The signed residual, for a debugging session that wants to know *where* the identity
    fails; :func:`check_av_roll_fwd` is the library-wide boolean over all ``t``. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - charges_from_av(t)
                - claims_from_av(t, DEATH) - claims_from_av(t, LAPSE)
                - claims_from_av(t, MATURITY))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the contract value roll-forward closes at **every** projected month.

    No argument and a ``bool`` return, following ``savings.CashValue_SE`` and the
    library-wide convention, so one test can call the same check across every model.
    The per-month signed residual is :func:`check_av_roll_fwd_resid`, and this is
    ``abs(resid) < check_tol_av x max(policy_count(), 1)`` over
    ``t = 0 .. proj_len() - 1``: the tolerance scales with the count, since the residual
    is rounding on that many contracts. On a point counting one contract it is
    ``VA_US_S``'s 1e-6 of a currency unit on a contract value of order 1e5. A loop that
    stops at the first month out of bounds; a residual that is not a number fails, as it
    fails ``VA_US_S``'s strict bound, since no comparison with NaN is true.
    """
    tol = check_tol_av * max(policy_count(), 1.0)                    # noqa: F821
    for t in range(proj_len()):
        if not abs(check_av_roll_fwd_resid(t)) < tol:
            return False
    return True


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual; zero to floating point in every covered month.

    ``pols_if(t) - pols_if_at(t + 1, BEF_NB) = deaths + surrenders + horizon
    survivors``, written on the start-of-month counts :func:`pols_if` carries: the next
    month opens on what is left, before its own new business. In the last covered month
    the next month's count is zero and :func:`pols_maturity` absorbs the survivors. 0.0
    outside cover, before ``t + 1`` is read; ``VA_US_S`` guards only below ``t = 0``.
    """
    if not is_active(t):
        return 0.0
    return (pols_if(t) - pols_if_at(t + 1, BEF_NB) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes at **every** projected month.

    No argument and a ``bool`` return; :func:`check_pols_roll_fwd_resid` is the signed
    per-month residual. In-force is a probability of order 1 per contract, so the
    tolerance is ``check_tol_pols``, 1e-12, times ``max(policy_count(), 1)``. A loop that
    fails a residual that is not a number, as :func:`check_av_roll_fwd` does.
    """
    tol = check_tol_pols * max(policy_count(), 1.0)                  # noqa: F821
    for t in range(proj_len()):
        if not abs(check_pols_roll_fwd_resid(t)) < tol:
            return False
    return True


def check_charge_split_resid(t):
    """Residual of the investment identity; zero to floating point in every covered month.

    ``gross fund return = fund expense + asset charge + the change in AV from
    investment``. It is the guard against the charge-base confusion the notes call the
    most consequential error on this product: M&E and admin are on **account value**, the
    rider fees on **benefit bases**, the contract fee **per contract** and the CDSC on
    **Remaining Premium** — four bases in one stack. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return (gross_inv_income_pp(t) - fund_expense_pp(t)
            - asset_charge_pp(t) - inv_income_pp(t))


def check_charge_split():
    """True when the investment identity closes at **every** projected month.

    No argument and a ``bool`` return; :func:`check_charge_split_resid` is the signed
    per-month residual, measured per contract, so the tolerance, ``check_tol_charge``,
    1e-8, does not scale with the count. A loop that fails a residual that is not a
    number, as :func:`check_av_roll_fwd` does.
    """
    for t in range(proj_len()):
        if not abs(check_charge_split_resid(t)) < check_tol_charge:  # noqa: F821
            return False
    return True


def result_cf():
    """Result table of cashflows, indexed by valuation month ``t = 0 .. proj_len() - 1``.

    Row ``t = 0`` is the valuation month, the same month for every model point, so the
    frames of a block sum row by row. A contract issued at or after the valuation date
    carries its purchase payment at the beginning of its issue month, :func:`t_entry`,
    and zeros before it; every row carries its month's own growth, charges and
    decrements. The ``pols_if`` column is the count in force at the **start** of each
    month and is the weight carried by every cash flow on that row, so the two reconcile.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "asset_charges": [asset_charges(t) for t in ts],
            "fees_glwb": [fees_glwb(t) for t in ts],
            "fees_gmdb": [fees_gmdb(t) for t in ts],
            "maint_fees": [maint_fees(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "glwb_payments": [glwb_payments(t) for t in ts],
            "claims_death": [claims(t, DEATH) for t in ts],
            "claims_lapse": [claims(t, LAPSE) for t in ts],
            "claims_maturity": [claims(t, MATURITY) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed by valuation month t.

    ``pols_if`` opens the month, after its new business, which ``pols_new_biz`` shows
    beside it, the count issued in the issue month; the three decrement columns take
    contracts out of it, and ``pols_if_aft_decr`` — the notes' ``l(t)`` — closes it. Rows
    therefore read across: ``pols_if - pols_death - pols_lapse - pols_maturity`` is the
    next row's ``pols_if``, less that row's new business.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, AFT_DECR) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract subaccount and contract values, indexed by t.

    One ``sa_pp_<i>`` column per subaccount, then the worked example's own columns: the
    contract value before the charges, the three charges, and the end-of-month value.
    """
    ts = list(range(proj_len()))
    cols = {}
    for j in range(subaccount_count()):
        i = subaccount_id(j)
        cols["sa_pp_%s" % i] = [sa_pp(t, i) for t in ts]
    cols["av_pp_bef_fee"] = [av_pp_at(t, BEF_FEE) for t in ts]
    cols["fee_glwb_pp"] = [fee_glwb_pp(t) for t in ts]
    cols["fee_gmdb_pp"] = [fee_gmdb_pp(t) for t in ts]
    cols["maint_fee_pp"] = [maint_fee_pp(t) for t in ts]
    cols["asset_charge_pp"] = [asset_charge_pp(t) for t in ts]
    cols["fund_expense_pp"] = [fund_expense_pp(t) for t in ts]
    cols["av_pp"] = [av_pp(t) for t in ts]
    cols["surr_benefit_pp"] = [surr_benefit_pp(t) for t in ts]
    return pd.DataFrame(cols, index=pd.Index(ts, name="t"))          # noqa: F821


def result_bases():
    """Result table of the guarantee bases and moneyness ratios, indexed by t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "gwb_pp": [gwb_pp(t) for t in ts],
            "gawa_pp": [gawa_pp(t) for t in ts],
            "bb_pp": [bb_pp(t) for t in ts],
            "rb_pp": [rb_pp(t) for t in ts],
            "np_pp": [np_pp(t) for t in ts],
            "rp_pp": [rp_pp(t) for t in ts],
            "adj_pp": [adj_pp(t) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "gmdb_claim_pp": [gmdb_claim_pp(t) for t in ts],
            "moneyness_glwb": [moneyness_glwb(t) for t in ts],
            "moneyness_gmdb": [moneyness_gmdb(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

issue_age_min = 35

issue_age_max = 85

glwb_issue_age_max = 80

gmdb_issue_age_max = 79

subaccount_id_max = 9

omega_age = 120

rate_sheet_date = "2026-04-27"

asset_charge_me = 0.01

asset_charge_admin = 0.003

phi_glwb_curr = 0.0125

phi_glwb_max = 0.03

phi_gmdb_curr = 0.009

phi_gmdb_max = 0.018

fee_increase_max = 0.0025

fee_reset_years = 5

maint_fee = 35.0

maint_fee_waiver_av = 50000.0

free_wd_rate = 0.1

surr_charge_years = 7

bonus_pct = 0.06

bonus_period_years = 10

bonus_restart_age = 81

gwb_cap = 10000000.0

gwb_adj_pct = 1.05

gwb_adj_age = 70

gwb_adj_min_year = 12

rollup_pct_young = 0.06

rollup_pct_old = 0.05

rollup_age_split = 70

gmdb_growth_cutoff_age = 80

forlife_age = 60

av_depletion_threshold = 0.005

lapse_rate_sc = 0.04

lapse_rate_shock = 0.25

lapse_rate_ult = 0.15

lapse_itm_upper = 1.0

lapse_itm_lower = 0.5

lapse_itm_mult_coef = 1.25

lapse_itm_threshold = 1.1

lapse_wd_year_factor = 0.6

vix_fee_coef = 0.0005

vix_divisor = 33.0

vix_offset = 10.0

vix_band = 0.004

vix_corridor_lo = 0.006

vix_corridor_hi = 0.025

cmt_spread = 0.01

cmt_spread_predraw = 0.015

cmt_round_step = 0.001

cmt_floor = 0.04

cmt_cap = 0.08

expense_maint = 100.0

expense_base_year = 2015

valuation_year = 2026

expense_av_rate = 0.0007

inflation_rate = 0.025

expense_acq = 0.0

comm_rate_acq = 0.0

check_tol_av = 1e-06

check_tol_pols = 1e-12

check_tol_charge = 1e-08

BEF_NB = 0

BEF_DECR = 1

BEF_LAPSE = 2

AFT_DECR = 3

BEF_PREM = 4

BEF_WD = 5

BEF_INV = 6

BEF_FEE = 7

EOM = 8

BEF_ANNIV = 9

DEATH = 0

LAPSE = 1

MATURITY = 2

ALL = 3

VIX_SQ = 0

CMT10 = 1

PRE_ISSUE = 0

ACCUM = 1

DEPLETED = 2

EXPIRED = 3

math = ("Module", "math")

pd = ("Module", "pandas")
