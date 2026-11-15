# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of the :mod:`~.MYGA_US_SEC` model.

The Space is parameterized by ``idx``, the position of a model point in the table and in
every :mod:`~.MYGA_US_SEC.Data` vector, as ``basiclife.BasicTerm_SC`` is:
``Projection[7]`` is an ItemSpace projecting the table's eighth row, model point 8, the
anchor cell in force 12 months at the valuation date, on its first contract
anniversary, and :func:`point_id` is its label::

    >>> Projection[7].result_cf()          # one row per month from the valuation date
    >>> Projection[7].result_av()          # its account value and Model #805 floor
    >>> Projection[7].point_id()           # 8, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before it computes

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, and an int set on a float Reference reads as a float
(``products/fixed_deferred_annuity/model-sec.md``, *What it refuses*).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.MYGA_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``. A formula of
:mod:`~.MYGA_US_S` is rewritten where it depends on where the projection starts, where it
must answer for a month outside cover, where it passed a policy month as ``t``, or where
it reads a table or text the compiled model holds as numbers; every other is
:mod:`~.MYGA_US_S`'s own. ``products/fixed_deferred_annuity/model-sec.md`` lists the
rewritten cells with the reason for each.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/fixed_deferred_annuity/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``MYGA_US_SEC`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

The readers and the filename References live on the sibling :mod:`~.MYGA_US_SEC.Data`
Space, reached here through the ``data`` Reference, so each file is read once per model
rather than once per model point. The six assumption tables are the files
:mod:`~.MYGA_US_S` reads, read in place; the model point table is this model's own. The
projection reads each table as ``Data`` holds it in arrays, built from the table checked,
its keys read by value, and through one cell of its own:

=========================  ================================  ==========================
Reference (on Data)        Arrays the projection reads       File
=========================  ================================  ==========================
model_point_file           data.premium() and the vectors    model_point_table_sec.csv
mort_table_file            data.mort_table_array()           mort_table.csv
surr_charge_file           data.surr_charge_array()          surr_charge_table.csv
surr_charge_age_cap_file   data.surr_charge_age_cap_array()  surr_charge_age_cap.csv
rate_scenario_file         data.market_rate_array(),         rate_scenario.csv
                           data.mva_ref_yield_array()
withdrawal_file            data.wd_amount_array()            withdrawal_table.csv
mva_factor_file            data.mva_factor_array()           mva_factor_table.csv
=========================  ================================  ==========================

The model point's attributes are each one element of a ``Data`` vector, read by an
accessor of the column's name, ``premium_pp`` reading ``data.premium()[idx]``;
:func:`model_point`, the whole row, is for a reader. :func:`mort_rate_at`,
:func:`surr_charge_rate`, :func:`surr_charge_age_cap_at`, :func:`scenario_rate`,
:func:`wd_scheduled_pp` and :func:`mva_duration_factor` are the tables' readers, in that
order. The age cap and the mortality are read through cells keyed by the attained age,
the duration factors at the whole years of the MVA term, and the surrender charge, the
scenario and the withdrawals at the month; the mortality, the scenario and the
withdrawals at the row ``Data`` numbers the point's ``sex``, ``scenario_id`` or
``wd_schedule_id`` by, and the surrender charge at the schedule code
:func:`surr_charge_id` returns (``Data``'s docstring, *The vectors*).

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however old the contract, month ``t`` runs from time ``t`` to time ``t + 1``, and
the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len` counts the months from
the valuation date to the deemed maturity at attained age 100. Row ``t`` is the same
month for every point, so the frames of a block line up and sum row by row.

``duration_mth(t)`` counts **policy months**, the months the contract has been in force
at time ``t``: ``duration_mth(t) = duration_mth_init() + t``, where
:func:`duration_mth_init` is read from the model point — positive for a contract in
force at the valuation date, in any month of its contract year, 0 for one issued at it,
``-k`` for one issued ``k`` months later, at most ten years later. It is the technical
notes' month index, and everything contractual reads it. The contract year is
``policy_year(t) = duration(t) + 1`` with ``duration(t) = duration_mth(t) // 12``, so the
anniversaries fall at the **start** of the months whose ``duration_mth(t)`` is a
multiple of 12, and the attained age is ``age(t) = age_at_entry() + duration(t)``. On
that clock run the guarantee periods, the initial term and each renewal of ``n`` years;
the 30-day window in the first month of each renewal period; the redeclaration months;
the surrender charge schedules, their clock and the attained-age cap; the MVA term; the
base lapse years and the dynamic-lapse exponent; the free-withdrawal year and its reset;
and the scheduled withdrawals, whose ``t`` in *withdrawal_table.csv* is a policy month.
Every renewal period is ``n`` years, as the product has it, so the position in the
guarantee period, the surrender-charge clock and the window are derived from
``duration_mth(t)`` alone. The anchor cell in force 12 months is in contract year 2 at
attained age 61 at ``t = 0``, where its $4,000 withdrawal of policy month 12 falls.

Two inputs read the valuation clock instead. The **rate scenario** — the market
competitor rate ``market_rate(t)`` and the MVA reference yield ``mva_ref_yield(t)`` — is
a path in calendar time, shared by every point of a block, so its ``t`` in
*rate_scenario.csv* is a valuation month. A rate fixed in the past, the declared rate of
a renewal period or the ``i0`` locked at its start, is read from the scenario at the
valuation month it was fixed in, or from the opening state where that month is before
:func:`t_entry`. Each shipped scenario is one flat row, so no shipped number depends on
the clock it is read on. And **expense inflation**, ``inflation_factor(t) = (1 +
inflation_rate) ** (t // 12)``, keeps :mod:`~.MYGA_US_S`'s annual step but takes it every
twelve months from the valuation date, so the maintenance charge is in valuation-date
dollars for every point alike. Acquisition is charged per contract issued, in the issue
month, and is not inflated, as in ``basiclife.BasicTerm_SE``.

Within a month: the free-withdrawal counters roll, the guarantee-period boundary is
applied, the elective withdrawal is taken, the annuitization elections are taken on the
account value after it, before crediting (:func:`annuitization_pp`), and the tax basis
is updated — all at the beginning of the month (BOM) — then interest is credited, the
Model #805 floor rolls forward and decrements are applied in the order annuitization,
mortality, surrender at the end of the month (EOM) **[std]**, with the death and
surrender benefits valued on the post-crediting account value. A contract's single
premium, its acquisition commission and its premium tax are beginning-of-month flows of
its issue month, the month with ``duration_mth(t) = 0``.

Twelve monthly factors ``(1 + i_cr)^(1/12)`` reproduce the declared *effective annual*
rate exactly, so ``av_pp(11) = premium_pp() * (1 + i_cr)`` on a contract issued at
``t = 0``. Do not additionally compound daily; the discretization affects only the
placement of interest *within* a month.

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.MYGA_US_S` computes: every cell the two share agrees at every argument
:mod:`~.MYGA_US_S` evaluates in its sweep, but for five whose meaning changed —
``pols_if_init``, now the count already in force at the valuation date; ``model_point``,
a row of another table; ``av_pp_init`` and ``mgsv_pp_init``, now the account value and
the floor in force entering month 0, whose issue values are credited in the issue month
instead; and ``result_pols``, which gains the month's new business. That is how
:mod:`~.MYGA_US_S`'s goldens on its new-business points carry over, each on a cell its
sweep reaches — the worked example, both surrender traces, the roll-forwards — and
``tests/test_model_conventions.py`` asserts it cell by cell; the statutory nonforfeiture
rate, which no report reads, is compared on the restated rows of
``tests/test_fixed_deferred_annuity_us_sec.py``. On a point in force the projection is
:mod:`~.MYGA_US_S`'s from the month
the point is valued at, month for month, its expenses apart, which are in valuation-date
dollars, and ``tests/test_fixed_deferred_annuity_us_sec.py`` asserts that.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, BEF_DECR)``, the
count carried in from ``t - 1`` (``BEF_NB``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, the first month on the books, and
nothing is counted outside cover (:func:`is_active`): before issue every count, and so
every cash flow, is zero, and so is every value state. Inside the month the decrements
are :mod:`~.MYGA_US_S`'s, in the notes' order, and ``pols_if_at`` names the count
between each: ``BEF_MORT`` after the annuitization elections, ``BEF_LAPSE`` after
deaths and ``AFT_DECR`` after surrenders, the notes' end-of-month ``l(t)``.

.. rubric:: The opening state

Each **value** state variable is a closing balance at the end of month ``t``:
``av_pp(t)``, ``mgsv_pp(t)``, ``prem_accum_gmir_pp(t)``, ``interest_credited_pp(t)`` and
``tax_basis_pp(t)``. The value entering month ``t`` is the closing balance of month
``t - 1``, or, at :func:`t_entry`, the model point's opening state — written inline as
``av_pp(t - 1) if t > t_entry() else av_pp_init()`` wherever an opening balance is
read, so that nothing is ever asked for a month before the valuation date or before
issue.

For a point in force the opening state is ten columns of its row, per contract, as the
contract stands at the start of month 0, before any month-0 event, each exactly what
:mod:`~.MYGA_US_S` carries into the month the point is valued at:

* the account value, the Model #805 floor and ``P_accum@GMIR`` entering month 0
  (:func:`av_pp_init`, :func:`mgsv_pp_init`, :func:`prem_accum_gmir_pp_init`), the last
  two possibly negative;
* the interest credited from issue to the valuation date
  (:func:`interest_credited_pp_init`), which the ``min_sc_interest`` cap reads, and to
  the anniversary that opened the contract year under way
  (:func:`interest_credited_pp_prev_anniv_init`), which next year's interest-only
  allowance reads;
* the free-withdrawal allowance of the contract year under way
  (:func:`free_wd_allow_init`), read on a valuation on an anniversary, and the part of it
  unused (:func:`free_wd_remain_init`), read on any other;
* the IRC 72 investment in the contract (:func:`tax_basis_pp_init`);
* the declared rate and the MVA reference yield ``i0`` in force entering month 0
  (:func:`credit_rate_init`, :func:`mva_ref_yield_locked_init`), read wherever the
  redeclaration or the start of the guarantee period in force precedes the valuation
  date.

For a point issued at or after the valuation date every one of them is 0 but
:func:`tax_basis_pp_init`, which is then the basis at issue, as :mod:`~.MYGA_US_S` takes
it. The issue values are computed by :mod:`~.MYGA_US_S`'s rules, in the issue month: the
premium credited, ``P (1 - load)``, through :func:`prem_to_av_pp`, and 87.5% of gross
consideration to the floor through :func:`prem_to_mgsv_pp` [R1 4.A(2)].

.. rubric:: Naming

Cell names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_*`` for
account values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for
per-contract amounts, ``*_at(t, timing)`` for a quantity read at a point inside the
month. What running in force adds is named as ``basiclife.BasicTerm_SE`` names it:
``duration_mth`` read from the model point, ``policy_count``, ``pols_new_biz``,
``pols_if_at`` with its ``BEF_NB`` timing, ``is_active`` and ``result_pols``.
``duration_mth_init``, the policy months completed at the valuation date, takes
``UL_US_S``'s name. A column of the opening state is the cell it opens with ``_init``
added, ``av_pp_init`` for :func:`av_pp`, and so is ``free_wd_allow_init``, which
:func:`free_wd_allow` returns for the contract year under way; a balance at the
anniversary on or before the valuation date adds ``_prev_anniv_init`` instead,
``interest_credited_pp_prev_anniv_init``. ``t_entry`` and ``maturity_mth`` are this
model's own, and ``surr_charge_age_cap_at`` is the age-keyed reader the library spells
``_at``, as ``WholeLife_US_S``'s ``mort_rate_guar_at``, and so is ``mort_rate_at``.
``point_id`` is ``basiclife.BasicTerm_SC``'s; ``scenario_number``,
``wd_schedule_number`` and ``mort_schedule`` are the rows of ``Data``'s arrays a point
reads, and ``mva_term_years`` the whole years of ``mva_term``. The ``is_*`` cells decode
the model point's text columns into the flags the projection branches on, so that no
monthly cell compares a column's text and none calls a label accessor
(``renewal_architecture``, ``free_wd_rule``, ``mva_family``, ...), which is left to
reporting. No monthly cell compares text at all: ``MYGA_US_S``'s timing and kind strings
and the schedule :func:`surr_charge_id` names are int codes here (*Codes*, below). The
technical notes use compact actuarial symbols instead.
The notes' month index is this model's ``duration_mth(t)``, so the notes' ``t`` in the
left-hand column is ``duration_mth(t)`` throughout, but in the rows marked *valuation
clock*, where it is this model's ``t``. The mapping is:

======================  ====================================  ==============================
Notes symbol            Cells                                 Meaning
======================  ====================================  ==============================
t                       duration_mth(t)                       The notes' month index:
                                                              completed policy months at the
                                                              start of month t
y = floor(t/12) + 1     policy_year(t)                        Contract year containing month
                                                              t (1-based label)
y - 1 = floor(t/12)     duration(t)                           Completed contract years at
                                                              the start of month t
x                       age_at_entry                          Issue age (ANB)
x + floor(t/12)         age(t)                                Attained age in month t
n                       guar_period                           Guarantee period in years
(none)                  policy_term                           Years from issue to
                                                              maturity_age
12(100 - x)             maturity_mth                          Policy month at which cover
                                                              ends
(none)                  duration_mth_init                     Completed policy months at the
                                                              valuation date; -k if issued k
                                                              months later
(frame)                 proj_len                              Months from the valuation date
                                                              to maturity; the frame ends at
                                                              proj_len - 1
(none)                  t_entry                               First month on the books
(none)                  is_active(t)                          Whether month t is inside
                                                              cover
(none)                  policy_count                          Contracts the model point
                                                              stands for
(renewal_architecture)  is_rollover                           Camp A or Camp B, decoded
                        is_annual_redeclare
(free_wd_rule)          is_pct_av                             The free-withdrawal rule,
                        is_interest_only                      decoded
(mva_family)            is_linear_duration                    The MVA family, decoded
                        is_geometric
                        is_declared_differential
(mva_cap_rule)          is_cap_none                           The MVA cap rule, decoded
                        is_cap_sym_sc
                        is_cap_min_sc_interest
                        is_cap_asym_sc_snfl
                        is_cap_gmir_floor
(mgsv_wd_convention)    is_wd_gross                           The floor's deduction of a
                        is_wd_net_of_charges                  withdrawal, decoded
P                       premium_pp                            Single purchase payment
i_cr(t)                 credit_rate(t)                        Declared credited rate, eff.
                                                              annual
i_cr in force           credit_rate_init                      Declared rate in force
                                                              entering month 0
f(t) - 1                credit_rate_mth(t)                    Monthly credited rate
(declaration month)     redeclare_month(t)                    Policy month the rate in force
                                                              was declared
s_ren                   renewal_spread                        Renewal declaration spread
                                                              (Reference)
i_nf                    mgsv_rate                             GMSV accumulation rate (2.80%)
g - 1                   mgsv_rate_mth                         Monthly GMSV rate
i_stat                  mgsv_rate_statutory(cmt5)             Model #805 indexed rate
GMIR                    gmir                                  Guaranteed minimum interest
                                                              rate
MR(t)                   market_rate(t)                        Market competitor rate,
                                                              valuation clock
AV(t)                   av_pp(t)                              Account value at end of month
                                                              t (closing balance)
AV(t-1), AV'(t), AV(t)  av_pp_at(t, timing)                   BEF_WD / BEF_INV / EOM; BEF_WD
                                                              holds the premium in the issue
                                                              month
AV(-1)                  av_pp_init                            Account value entering month 0
(premium credited)      prem_to_av_pp(t)                      Premium credited to the
                                                              account value, in the issue
                                                              month
l(t) x AV(t)            av_at(t, timing)                      In-force weighted account
                                                              value
(interest credited)     inv_income_pp(t)                      Interest credited in month t
(cumulative interest)   interest_credited_pp(t)               Interest credited to date
(interest to date)      interest_credited_pp_init             Interest credited before the
                                                              valuation date
(I at anniversary)      interest_credited_pp_prev_anniv_init  Interest credited to the
                                                              anniversary opening the year
                                                              under way
MGSV(t)                 mgsv_pp(t)                            Model #805 floor at end of
                                                              month t
MGSV(-1)                mgsv_pp_init                          Model #805 floor entering
                                                              month 0
0.875 x P               prem_to_mgsv_pp(t)                    The consideration the floor
                                                              opens with, in the issue month
c(t)                    mgsv_charge_pp(t)                     Monthly slice of the contract
                                                              charge
d(t)                    mgsv_wd_deduct_pp(t)                  Withdrawal deducted from the
                                                              floor
FWB(y)                  free_wd_base(y)                       Free-withdrawal base fixed at
                                                              the start of year y
0.10 x FWB(y)           free_wd_allow(y)                      Allowance for contract year y
(year's allowance)      free_wd_allow_init                    Allowance of the contract year
                                                              under way at the valuation
                                                              date
FW(t)                   free_wd_avail(t)                      Unused allowance at BOM of
                                                              month t
(FW after W(t))         free_wd_remain(t)                     Unused allowance after the
                                                              withdrawal
(FW carried)            free_wd_remain_init                   Unused allowance carried into
                                                              month 0
W(t)                    wd_pp(t)                              Gross amount removed from the
                                                              AV
(scheduled W)           wd_scheduled_pp(t)                    Withdrawal scheduled at the
                                                              policy month of t
(free part of W)        wd_free_pp(t)                         Free portion of W(t)
E(t) on a withdrawal    wd_excess_pp(t)                       Withdrawal exposed to charge
                                                              and MVA
E(t) on a surrender     surr_excess_pp(t)                     Surrender exposed to charge
                                                              and MVA
sc(y)                   surr_charge_rate(t)                   Surrender charge rate in force
sc_clock(t)             surr_charge_year(t)                   Year within the current
                                                              schedule
(schedule key)          surr_charge_id(t)                     INITIAL / RENEWAL / NONE
(age cap)               surr_charge_age_cap(t)                Attained-age cap on the charge
                                                              in month t
(age cap by age)        surr_charge_age_cap_at(a)             The same, keyed by attained
                                                              age
C(t)                    surr_charge_pp(t)                     Charge on a full surrender
C(t) on a withdrawal    wd_charge_pp(t)                       Charge on a partial withdrawal
mu(t)                   mva_rate(t)                           MVA rate, signed
M(t)                    mva_pp(t)                             Capped MVA on a full surrender
M(t) on a withdrawal    wd_mva_pp(t)                          Capped MVA on a partial
                                                              withdrawal
T(t)                    mva_term(t)                           MVA duration in years
(whole years of T)      mva_term_years(t)                     Its whole years, an int
(period index)          gp_index(t)                           Guarantee period containing
                                                              month t
(period start)          gp_start_month(t)                     First policy month of that
                                                              period
i0                      mva_ref_yield_locked(t)               Reference yield locked at
                                                              period start
i0 in force             mva_ref_yield_locked_init             Reference yield locked for the
                                                              period in force entering month
                                                              0
it                      mva_ref_yield(t)                      Reference yield at month t,
                                                              valuation clock
Phi(t)                  mva_rate(t)                           Geometric MVA factor, inline
F_s                     mva_duration_factor(t)                Declared-differential duration
                                                              factor
(term rounded up)       mva_ref_term_years(tau)               Whole-year maturity of the
                                                              distribution yield
P_accum@GMIR            prem_accum_gmir_pp(t)                 Premium less prior withdrawals
                                                              at the GMIR
(P_accum entering)      prem_accum_gmir_pp_init               P_accum@GMIR entering month 0
s_adm                   mva_admin_spread                      Geometric MVA expense adder
                                                              (Reference)
SV(t)                   surr_value_pp(t)                      Gross surrender value before
                                                              the floor
SB(t)                   surr_benefit_pp(t)                    Surrender benefit paid
gp_end(t)               gp_end(t)                             Months left in the guarantee
                                                              period
(the 30-day window)     in_gp_window(t)                       True in the guarantee-period-
                                                              end window
basis(t)                tax_basis_pp(t)                       IRC 72 investment in the
                                                              contract
basis(-1)               tax_basis_pp_init                     Investment in the contract
                                                              entering month 0, or at issue
(taxable part of W)     taxable_wd_pp(t)                      Income-first taxable amount
l(t-1)                  pols_if(t)                            In force weighting month t:
                                                              after new business, before
                                                              decrements
(opening l)             pols_if_init                          In force at the valuation
                                                              date; 0 for new business
(none)                  pols_new_biz(t)                       Contracts issued in month t
l(t)                    pols_if_at(t, AFT_DECR)               In force at the end of month t
(intra-month l)         pols_if_at(t, timing)                 BEF_NB / BEF_DECR / BEF_MORT /
                                                              BEF_LAPSE / AFT_DECR
q(t)                    mort_rate_mth(t)                      Monthly mortality rate
(annual q_x)            mort_rate(t)                          Annual mortality at the
                                                              attained age
(q_x by age)            mort_rate_at(a)                       The same, keyed by attained
                                                              age
(label)                 point_id                              The model point's label
(table rows)            scenario_number                       Its scenario's row
                        wd_schedule_number                    Its programme's row
                        mort_schedule                         Its sex's row
w(t)                    lapse_rate_mth(t)                     Monthly total surrender rate
w_annual(t)             lapse_rate(t)                         Annual total surrender rate
Base(y)                 lapse_rate_base(t)                    Prescribed base lapse by
                                                              contract year
G                       gmir_factor                           VM-22 GMIR factor
Market(t)               lapse_dyn_market(t)                   Dynamic-lapse market term
Rate(t)                 lapse_dyn_rate(t)                     Dynamic-lapse rate term
Phi_MVA(t)              mva_lapse_factor_at(t)                MVA factor gating the dynamic
                                                              term
BF                      lapse_buffer                          Dynamic-lapse buffer factor
                                                              (Reference)
X                       lapse_dyn_exponent(t)                 Dynamic-lapse exponent
a(t)                    annuitization_rate(t)                 Monthly annuitization election
                                                              rate
l a                     pols_annuitization(t)                 Annuitization elections
l (1-a) q               pols_death(t)                         Deaths
l (1-a)(1-q) w          pols_lapse(t)                         Full surrenders
(none)                  pols_maturity(t)                      Deemed-maturity annuitizations
P on new business       premiums(t)                           Premium income, in the issue
                                                              month
(premium credited)      prem_to_av(t)                         Premium credited, in-force
                                                              weighted
W + M - C               withdrawals(t)                        Withdrawal payments
(ledger benefit lines)  claims(t, kind)                       Benefit outgo by kind
(benefit per contract)  claim_pp(t, kind)                     Benefit per contract by kind
(AV released)           claims_from_av(t, kind)               Account value released by a
                                                              claim
(paid above AV)         claims_over_av(t, kind)               Benefit paid above the account
                                                              value
0.02 x P                commissions(t)                        Acquisition commission
50/12 x 1.025^(t//12)   expenses(t)                           Maintenance expense, valuation
                                                              clock, plus acquisition on new
                                                              business
1.025^(t//12)           inflation_factor(t)                   Expense inflation, valuation
                                                              clock
premium tax             premium_taxes(t)                      Premium tax
NetCF(t)                net_cf(t)                             Net cash flow
(none)                  result_pols()                         The counts behind result_cf
======================  ====================================  ==============================

Six names needed care, and all six are collisions the notes themselves carry.

``d(t)`` in these notes is the **withdrawal deducted from the Model #805 floor** in
processing step 7, *not* deaths as in :mod:`.Term_US_S`; it becomes
:func:`mgsv_wd_deduct_pp`, leaving :func:`pols_death` unambiguous. ``c(t)`` is the monthly
slice of the annual contract charge, not conversions, and becomes :func:`mgsv_charge_pp`.
``E(t)`` names two different currency bases — the excess of a *withdrawal* over the free
allowance and the excess of the whole *account value* over it at a full surrender — which
:func:`wd_excess_pp` and :func:`surr_excess_pp` separate; the same symbol is expenses in
:mod:`.Term_US_S`, which here is :func:`expenses`. ``X`` is the dynamic-lapse exponent here
and the premium tax in :mod:`.Term_US_S`, split into :func:`lapse_dyn_exponent` and
:func:`premium_taxes`. ``T(t)`` is the MVA duration in *years* while ``t`` counts
*months*, so it becomes :func:`mva_term`. And the floor itself carries three labels in the
sources — MGSV in this library, "GMSV" in the specimen [S11], "MGV" in the fixed-indexed
annuity notes — one concept, named :func:`mgsv_pp` throughout.

Two further names carry a **library-wide** convention that differs from the notes' own
indexing, and in both cases the notes' quantity survives under a second name rather than
being dropped.

:func:`pols_if` is the count in force at the **start** of month ``t``, after the month's
new business and before its decrements, ``pols_if_at(t, BEF_DECR)``, matching
:mod:`.Term_US_S` and ``savings.CashValue_SE``, and it is the weight applied to that same
month's cash flows — :func:`withdrawals`, :func:`expenses` and the ``pols_if`` column of
:func:`result_cf` reconcile row by row. The notes' end-of-month ``l(t)`` is unchanged and
unmoved; it is read as ``pols_if_at(t, AFT_DECR)``, and ``pols_if_at(t + 1, BEF_NB)
== pols_if_at(t, AFT_DECR)`` in every month but the last covered one,
``duration_mth(t) = maturity_mth() - 1``, where :func:`pols_maturity` empties the block.

:func:`lapse_rate` is the **annual** total surrender rate and :func:`lapse_rate_mth` the
monthly one, matching the :func:`mort_rate` / :func:`mort_rate_mth` pair and the eight
other models that spell it that way. The notes write the monthly rate ``w(t)`` and the
annual rate ``w_annual(t)``, so the pairing here is the notes' own — only the suffixes
move.

Three rows of the table above are **References, not Cells**, because the notes give each
as a single assumption number rather than a function of ``t``: ``s_ren`` is
``renewal_spread``, the spread in ``i_cr^ren(t) = max(GMIR, MR(t) - s_ren)`` (0.00% on the
base run, 1.00% in the notes' scenario **[std]**); ``BF`` is ``lapse_buffer``, the 50 bp
band inside which the dynamic-lapse response is exactly zero; and ``s_adm`` is
``mva_admin_spread``, the 25 bp administrative-expense adder in the geometric MVA's
denominator [S4], which the other registered contract sets to 0 [S3]. Rebasing any of
the three is an assignment to the Reference, made before the model computes anything,
with no formula change. ``P_accum@GMIR``, by contrast, is a recursion and so a Cells:
:func:`prem_accum_gmir_pp` is the level the ``gmir_floor`` cap holds ``AV + M`` above
[S13].

Two quantities the notes list as *model point attributes* are fixed at issue by a rule the
notes also state, and are computed by that rule, in the issue month: ``av_initial`` is
``premium_pp() * (1 - load_prem_rate)`` with no front-end load [S5][S10][S16], credited
through :func:`prem_to_av_pp`, and ``mgsv_initial`` is ``net_consideration_ratio *
premium_pp()`` — 87.5% of gross consideration [R1 4.A(2)] — through
:func:`prem_to_mgsv_pp`. :func:`av_pp_init` and :func:`mgsv_pp_init`, the names
:mod:`~.MYGA_US_S` gives those issue values, are here the account value and the floor in
force entering month 0, 0 on new business. The notes' ``tax_basis_initial`` genuinely
varies with tax status, so it is a model point column, ``tax_basis_pp_init``: the basis at
issue for a contract not yet in force, the basis entering month 0 for one in force.

.. rubric:: Timing arguments

Account value, following ``CashValue_SE``'s ``av_pp_at``:

``BEF_WD``
    ``AV(t-1)``, at the start of month ``t`` before the elective withdrawal: the account
    value entering the frame, :func:`av_pp_init`, at :func:`t_entry` for a point in
    force, the previous month's closing balance after, and in the issue month the
    premium credited, :func:`prem_to_av_pp`, on top.
``BEF_INV``
    ``AV'(t)``, after the withdrawal and after annuitization elections, before crediting.
``EOM``
    ``AV(t)``, after crediting. Equal to :func:`av_pp`, the closing balance of month ``t``.

Policy counts, following ``CashValue_SE``'s ``pols_if_at`` and ``basiclife.BasicTerm_SE``'s
``BEF_NB``:

``BEF_NB``
    the count carried in from month ``t - 1``, before month ``t``'s new business:
    :func:`pols_if_init` at :func:`t_entry`, zero outside cover.
``BEF_DECR``
    ``l(t-1)``, in force at the start of month ``t``, after its new business. Equal to
    :func:`pols_if`.
``BEF_MORT``
    after annuitization elections, ``l(t-1)(1 - a(t))``.
``BEF_LAPSE``
    after deaths, ``l(t-1)(1 - a(t))(1 - q(t))``.
``AFT_DECR``
    after surrenders, ``l(t)`` — the notes' end-of-month in-force.

``BEF_NB`` is the one timing running in force adds. ``basiclife.BasicTerm_SE``'s
``"BEF_MAT"``, the count at the start of a month before its maturities, is not adopted:
this product has no timing of that name, and its contracts mature at the end of the last
covered month, as the S goldens have it.

Benefit ``kind`` arguments are ``DEATH``, ``LAPSE``, ``ANNUITIZATION`` and
``MATURITY``, and ``ALL`` for the total of :func:`claims` and :func:`claims_over_av`. Any
other value of any of these raises ``ValueError``.

.. rubric:: pols_maturity and the projection horizon

The technical notes state no projection horizon: a MYGA under the ``rollover``
architecture renews indefinitely, and the notes' own base-lapse pattern is written as a
repeating five-year cycle with no terminal date. The model runs to the contract
anniversary at attained age ``maturity_age`` = 100 **[std]** — the last attained age in
the sourced cap band on the renewal surrender charge, which the notes tabulate as 4% at
94, 3% at 95, 2% at 96, 1% at 97 and 0% at 98-100 [S1][S2]. The cap *reaches* zero at 98;
100 is where the sourced band stops, and it is past the statutory deemed maturity date of
Model #805 section 8 [R1]. That anniversary is policy month :func:`maturity_mth`. The
survivors there are annuitized out through :func:`pols_maturity`, zero in every month but
the last covered one, ``duration_mth(t) = maturity_mth() - 1``, which is
``t = proj_len() - 1``, so that::

    pols_if(t) - pols_if_at(t + 1, BEF_NB) = pols_annuitization(t) + pols_death(t)
                                               + pols_lapse(t) + pols_maturity(t)

holds for every ``t`` — the start-of-month count opens the row, the four exits are taken
during it and the next month opens on what is left, before its own new business.
Including the last covered month, where the block would otherwise appear to lose lives
with no cause. The name follows ``BasicTerm_S.pols_maturity`` and the construction follows
:mod:`.Term_US_S`.

.. rubric:: Codes

What :mod:`~.MYGA_US_S` spells as text, a timing, a kind, a scenario column or a
surrender charge schedule, is here an int Reference named as the text it replaces, so
that every cell takes and returns C numbers. A call site reads as it did, less the
quotes: ``pols_if_at(t, BEF_DECR)``, ``av_pp_at(t, BEF_WD)``, ``claims(t, DEATH)``.

==============  =====  ==============================================================
Reference       Value  Meaning
==============  =====  ==============================================================
BEF_NB          0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR        1      :func:`pols_if_at`: that count plus month t's new business
BEF_MORT        2      :func:`pols_if_at`: after the annuitization elections
BEF_LAPSE       3      :func:`pols_if_at`: after deaths
AFT_DECR        4      :func:`pols_if_at`: after surrenders, the notes' l(t)
BEF_WD          5      :func:`av_pp_at`, :func:`av_at`: before the withdrawal
BEF_INV         6      :func:`av_pp_at`, :func:`av_at`: after it, before crediting
EOM             7      :func:`av_pp_at`, :func:`av_at`: after crediting
DEATH           0      the claim cells: the death claim
LAPSE           1      the claim cells: the surrender claim
ANNUITIZATION   2      the claim cells: the annuitization election
MATURITY        3      the claim cells: the deemed maturity
ALL             4      :func:`claims`, :func:`claims_over_av`: the four kinds' total
MVA_REF_YIELD   0      :func:`scenario_rate`: the ``mva_ref_yield`` column
MARKET_RATE     1      :func:`scenario_rate`: the ``market_rate`` column
NONE            0      :func:`surr_charge_id`: no schedule in force
INITIAL         1      :func:`surr_charge_id`: the ``initial`` schedule
RENEWAL         2      :func:`surr_charge_id`: the ``renewal`` schedule
==============  =====  ==============================================================

The model has two families of timing, the count's and the account value's, passed to
different cells, and they are numbered as one: ``BEF_NB`` 0 and ``BEF_DECR`` 1, as in
every SEC model, then the count's others, then the account value's, each family in the
order of its instants within the month. So no two timings share a code, and a code of
one family passed to the other's cell, ``av_pp_at(t, BEF_NB)``, is refused as any timing
the cell does not take is, ``ValueError("invalid timing")``, in both engines, rather than
read as a timing of the cell's own. Kinds are numbered in ``result_cf``'s order, which is
the order ``MYGA_US_S`` adds them in its total, and ``ALL``, ``MYGA_US_S``'s
``kind=None``, after them; the claim cells but :func:`claims` and :func:`claims_over_av`
refuse it, ``ValueError("invalid kind")``. ``NONE``, ``INITIAL`` and ``RENEWAL`` are also
the rows of ``Data.surr_charge_array``, which holds the two schedules there. A code a
cell takes indexes that cell's cache, a C array of eight codes a month for each of the
ten cells that take one, since every 2-D cache of the model has one width
(``spec_sec.py``), so codes are numbered densely from 0, and a code a cell does not
take but below 8 is refused inside the cache. They are References, not cells, so the
symbol map does not list them. Every other Reference is named in lower case,
``issue_age_min`` and ``issue_age_max`` among them, the product's issue ages, the first
of which, with ``maturity_age``, the compiled model's caches are sized from
(:func:`proj_len`).

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`policy_id`, :func:`sex`,
:func:`tax_status`, :func:`mgsv_wd_convention`, :func:`renewal_architecture`,
:func:`free_wd_rule`, :func:`mva_family`, :func:`mva_cap_rule`, :func:`scenario_id` and
:func:`wd_schedule_id`, the reports :func:`result_cf`, :func:`result_pols` and
:func:`result_av`, and the checks :func:`check_av_roll_fwd` and
:func:`check_pols_roll_fwd` are written for a reader and for the comparison with
:mod:`~.MYGA_US_S`, which has every one of them: a table row, text, DataFrames and two
verdicts. No other cell calls them: each reads the number ``Data`` decoded from the same
column instead, the decodes' flags and the rows the keys select. So the row, the text and
the frames stay Python when the model compiles. A label accessor returns its column as
read, text or not: ``Data`` accepts, and the model projects, a point whose
``tax_status`` or ``policy_id`` is blank or a number, which no cell reads, or whose
``sex``, ``scenario_id`` or ``wd_schedule_id`` is a number, where its table's keys are
numbers, and the compiled accessor returns what modelx returns, NaN or an int. Every
other cell returns a C ``bint``, ``long long`` or ``double``, and so do the two checks,
which may stay Python but compile to a ``bint``, their verdict, as their per-month
residuals, ``*_resid``, compile to a ``double``.

Three cells of float parameters compile with C signatures and dict caches, their
bodies Python, the engine cells :func:`mgsv_rate_statutory`,
:func:`mgsv_rate_is_compliant` and :func:`mva_ref_term_years`: ``MYGA_US_S``'s own,
``math`` included, kept for a user checking a contract rate against the statute and for
the comparison with :mod:`~.MYGA_US_S`. No projection cell calls them, and a cell keyed
by a float compiles with a Python dict for a cache, so the registry admits them by name.
Compiled, :func:`mva_ref_term_years` returns a C ``long long``, so a term below
``-2**63``, outside any term, overflows there, where modelx returns Python's int. The
two others of ``MYGA_US_S``'s float-parameter cells, ``mva_pp_on`` and
``mva_factor_geometric``, which the projection does call, are written inline in the cells
that call them, :func:`mva_pp`, :func:`wd_mva_pp` and :func:`mva_rate`.
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
    reads its own ``Data`` vector instead.
    """
    return data.model_point_table().iloc[idx]                        # noqa: F821


def point_id():
    """The label of the selected model point, its ``point_id``, from ``Data.point_id``.

    ``Projection`` is indexed by position, ``idx``, as ``basiclife.BasicTerm_SC`` is; the
    label is what a reader finds in the table, so every refusal names it.
    """
    return int(data.point_id()[idx])                                 # noqa: F821


def policy_id():
    """The contract identifier of the selected model point.

    A reporting cell (the Space docstring), which no projection cell reads.
    """
    return model_point()["policy_id"]


def age_at_entry():
    """The issue age (ANB) of the selected model point.

    The age at issue, not at the valuation date: ``age(0)`` is the attained age then.
    From ``Data.age_at_entry``, which holds the column to a whole number of years below
    ``2**53`` in size.
    """
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point, M or F.

    A reporting cell (the Space docstring): ``Data`` joins the mortality table by it,
    through :func:`mort_schedule`, and no projection cell reads it here.
    """
    return model_point()["sex"]


def tax_status():
    """Tax status of the contract: NQ, IRA, Roth or inherited.

    Reported only, a reporting cell (the Space docstring). The base run is non-qualified
    **[std]**; no RMD module is implemented.
    """
    return model_point()["tax_status"]


def premium_pp():
    """P: the single purchase payment per contract."""
    return float(data.premium()[idx])                                # noqa: F821


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the contracts in force then, before any
    month-0 event; any other point counts the contracts it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Every per-contract value — the
    account value, the floor, the allowance, the basis, the opening state — is the same
    whatever the count, and every cash flow is a per-contract amount weighted by it.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """Contracts in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose contracts
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count. ``MYGA_US_S``'s cell of the name is the notes'
    ``l(t-1)`` at ``t = 0``, the count at issue; in both models their end-of-month ``l(t)``
    is ``pols_if_at(t, AFT_DECR)``.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def guar_period():
    """n: the guarantee period in years; the surrender charge and MVA periods equal it."""
    return int(data.guar_period()[idx])                              # noqa: F821


def declared_rate_initial():
    """The declared credited rate guaranteed for the initial term, 4.45% p.a. [S11]."""
    return float(data.declared_rate_initial()[idx])                  # noqa: F821


def gmir():
    """The guaranteed minimum interest rate, 0.25% p.a. [S11].

    A floor on any declared rate.
    """
    return float(data.gmir()[idx])                                   # noqa: F821


def mgsv_rate():
    """i_nf: the contract GMSV accumulation rate, 2.80% p.a. [S11].

    The Model #805 floor accretes at this rate. It must be at least the statutory indexed
    rate :func:`mgsv_rate_statutory`; crediting the floor at more is permitted and simply
    produces a higher floor [R1 4.B].
    """
    return float(data.mgsv_rate()[idx])                              # noqa: F821


def mgsv_annual_charge():
    """The annual contract charge deducted from the Model #805 floor.

    $0 representative [S11]; the statutory maximum is $50 p.a. [R1 4.A].
    """
    return float(data.mgsv_annual_charge()[idx])                     # noqa: F821


def mgsv_wd_convention():
    """How a withdrawal reduces the Model #805 floor: ``gross`` or ``net_of_charges``.

    ``gross`` [S11] deducts W(t) itself; ``net_of_charges`` [S9] deducts the cash actually
    paid, W(t) + M(t) - C(t), keeping the floor higher. Both are live in the market and
    the difference compounds at i_nf for the rest of the contract. A reporting cell (the
    Space docstring): ``Data`` decodes the column into :func:`is_wd_gross` and
    :func:`is_wd_net_of_charges`, and no projection cell reads it here.
    """
    return model_point()["mgsv_wd_convention"]


def is_wd_gross():
    """Whether the floor deducts each withdrawal gross, ``mgsv_wd_convention`` ``gross``.

    A decode of the model point's column, made by ``Data`` once for the table, as each
    ``is_*`` cell's is, so that the projection branches on a flag and no projection cell
    compares the column's text or calls the label accessor, :func:`mgsv_wd_convention`,
    which is left to reporting. ``Data.is_wd_gross`` compares the text exactly, as
    ``MYGA_US_S`` does, so ``Gross`` or `` gross`` is no flag. :func:`mgsv_wd_deduct_pp`
    reads it.
    """
    return bool(data.is_wd_gross()[idx])                             # noqa: F821


def is_wd_net_of_charges():
    """Whether the floor deducts the cash paid, ``mgsv_wd_convention`` ``net_of_charges``.

    The other decode of the column (:func:`is_wd_gross`). A value that is neither raises
    in :func:`mgsv_wd_deduct_pp`, as in ``MYGA_US_S``.
    """
    return bool(data.is_wd_net_of_charges()[idx])                    # noqa: F821


def renewal_architecture():
    """``rollover`` (Camp A) or ``annual_redeclare`` (Camp B).

    ``rollover`` starts a fresh guarantee period, surrender charge schedule and MVA period
    at each boundary [S1] (no MVA on that form) [S2] [S5] [S11], so the shock lapse
    repeats every n years.
    ``annual_redeclare`` redeclares the rate each anniversary with no further surrender
    charge and no MVA [S13], so the shock happens once. A reporting cell (the Space
    docstring), decoded by ``Data`` into :func:`is_rollover` and
    :func:`is_annual_redeclare`.
    """
    return model_point()["renewal_architecture"]


def is_rollover():
    """Whether the contract renews under ``rollover``, Camp A.

    A decode of the ``renewal_architecture`` column (:func:`is_wd_gross`), read where
    ``MYGA_US_S`` asks whether the architecture is ``rollover``: :func:`redeclare_month`
    and :func:`lapse_rate_base`.
    """
    return bool(data.is_rollover()[idx])                             # noqa: F821


def is_annual_redeclare():
    """Whether the contract renews under ``annual_redeclare``, Camp B.

    A decode of the ``renewal_architecture`` column (:func:`is_wd_gross`), read where
    ``MYGA_US_S`` asks whether the architecture is ``annual_redeclare``:
    :func:`in_gp_window`, :func:`surr_charge_id` and :func:`mva_term`. Each cell keeps the
    question ``MYGA_US_S`` asks, so a value that is neither is answered as there.
    """
    return bool(data.is_annual_redeclare()[idx])                     # noqa: F821


def free_wd_rule():
    """``pct_av`` or ``interest_only``.

    ``pct_av`` [S10] is the representative 10%-of-base allowance; ``interest_only``
    [S5][S6] is the prior contract year's credited interest. The notes' third value,
    ``greatest_of`` [S13], is **not implemented**: no formula is given for it. A reporting
    cell (the Space docstring), decoded by ``Data`` into :func:`is_pct_av` and
    :func:`is_interest_only`.
    """
    return model_point()["free_wd_rule"]


def is_pct_av():
    """Whether the free-withdrawal allowance is ``pct_av``, a percentage of the base.

    A decode of the ``free_wd_rule`` column (:func:`is_wd_gross`), read by
    :func:`free_wd_allow`.
    """
    return bool(data.is_pct_av()[idx])                               # noqa: F821


def is_interest_only():
    """Whether the free-withdrawal allowance is ``interest_only``, last year's interest.

    A decode of the ``free_wd_rule`` column (:func:`is_wd_gross`), read by
    :func:`free_wd_allow`, which raises on a rule that is neither, as ``MYGA_US_S`` does.
    """
    return bool(data.is_interest_only()[idx])                        # noqa: F821


def free_wd_rate():
    """The free-withdrawal percentage under ``pct_av``, 10% [S10]."""
    return float(data.free_wd_rate()[idx])                           # noqa: F821


def free_wd_mva_exempt():
    """Whether the free allowance is exempt from the surrender charge **and** the MVA.

    True is the retail MYGA convention **[std]** [S8][S11] and gives
    ``E(t) = AV(t) - FW(t)``. False is the registered-contract convention [S3][S4] and
    gives ``E(t) = AV(t)``, collapsing the surrender benefit to the multiplicative form
    ``max(AV(t) x (1 + mu(t) - sc(y)), MGSV(t))``. The notes apply the flag to both the
    charge and the adjustment; in the market it strictly concerns the adjustment.

    From ``Data.free_wd_mva_exempt``, an int64 vector holding ``MYGA_US_S``'s ``bool()``
    of each value, so a blank, read as NaN, and any text are True, as there.
    """
    return bool(data.free_wd_mva_exempt()[idx])                      # noqa: F821


def mva_family():
    """``linear_duration``, ``geometric`` or ``declared_differential``. All implemented.

    A reporting cell (the Space docstring), decoded by ``Data`` into
    :func:`is_linear_duration`, :func:`is_geometric` and :func:`is_declared_differential`.
    """
    return model_point()["mva_family"]


def is_linear_duration():
    """Whether the MVA is the ``linear_duration`` family.

    One of three decodes of the ``mva_family`` column (:func:`is_wd_gross`), read by
    :func:`mva_rate`, which raises on a family that is none of them, as ``MYGA_US_S``
    does.
    """
    return bool(data.is_linear_duration()[idx])                      # noqa: F821


def is_geometric():
    """Whether the MVA is the ``geometric`` family.

    A decode of the ``mva_family`` column (:func:`is_linear_duration`).
    """
    return bool(data.is_geometric()[idx])                            # noqa: F821


def is_declared_differential():
    """Whether the MVA is the ``declared_differential`` family.

    A decode of the ``mva_family`` column (:func:`is_linear_duration`).
    """
    return bool(data.is_declared_differential()[idx])                # noqa: F821


def mva_cap_rule():
    """``sym_sc``, ``min_sc_interest``, ``asym_sc_snfl``, ``gmir_floor`` or ``none``.

    The cap, not the formula family, is the largest cross-carrier divergence in the source
    set, so it is a first-class model parameter. See :func:`mva_pp`. A reporting cell (the
    Space docstring), decoded by ``Data`` into the five ``is_cap_*`` flags.
    """
    return model_point()["mva_cap_rule"]


def is_cap_none():
    """Whether the MVA is uncapped, ``mva_cap_rule`` ``none``.

    One of five decodes of the ``mva_cap_rule`` column (:func:`is_wd_gross`), read by
    :func:`mva_pp` and :func:`wd_mva_pp`, which raise on a rule that is none of them, as
    ``MYGA_US_S``'s ``mva_pp_on`` does.
    """
    return bool(data.is_cap_none()[idx])                             # noqa: F821


def is_cap_sym_sc():
    """Whether the MVA cap is ``sym_sc``, the surrender charge both ways.

    A decode of the ``mva_cap_rule`` column (:func:`is_cap_none`).
    """
    return bool(data.is_cap_sym_sc()[idx])                           # noqa: F821


def is_cap_min_sc_interest():
    """Whether the MVA cap is ``min_sc_interest``: the charge or the interest, the lesser.

    A decode of the ``mva_cap_rule`` column (:func:`is_cap_none`).
    """
    return bool(data.is_cap_min_sc_interest()[idx])                  # noqa: F821


def is_cap_asym_sc_snfl():
    """Whether the MVA cap is ``asym_sc_snfl``, the charge on the upside alone.

    A decode of the ``mva_cap_rule`` column (:func:`is_cap_none`).
    """
    return bool(data.is_cap_asym_sc_snfl()[idx])                     # noqa: F821


def is_cap_gmir_floor():
    """Whether the MVA cap is ``gmir_floor``, ``AV + M`` held at ``P_accum`` or above.

    A decode of the ``mva_cap_rule`` column (:func:`is_cap_none`).
    """
    return bool(data.is_cap_gmir_floor()[idx])                       # noqa: F821


def mva_ref_yield_at_issue():
    """i0 at issue: the MVA reference yield locked for the initial period.

    5.00% **[std]**, fixed at issue for the whole initial term.
    """
    return float(data.mva_ref_yield_at_issue()[idx])                 # noqa: F821


def premium_tax_rate():
    """Premium tax deducted from the contract, 0% **[std]** [S3][S16]."""
    return float(data.premium_tax_rate()[idx])                       # noqa: F821


def tax_basis_pp_init():
    """The IRC 72 investment in the contract at the start of month ``t_entry()`` [R6].

    The ``tax_basis_pp_init`` column, ``MYGA_US_S``'s ``tax_basis_initial`` under the
    name of the cell that reads it. For a point in force it is the basis entering month
    0, before any month-0 event: the close of policy month ``duration_mth_init() - 1``,
    what ``MYGA_US_S`` carries into that month as the ``tax_basis_pp`` of the month
    before. For a point issued at or after the valuation date it is the basis at issue,
    which varies with tax status, as ``MYGA_US_S`` takes it: the premium on every shipped
    point, all of them non-qualified. So it is the one opening-state column that is not 0
    on new business. The notes' ``basis(t)`` is the end-of-month value, so this is
    ``basis(t-1)`` at :func:`t_entry`, not ``tax_basis_pp(t_entry())``.
    """
    return float(data.tax_basis_pp_init()[idx])                      # noqa: F821


def prem_accum_gmir_pp_init():
    """P_accum@GMIR entering month 0, per contract, the ``prem_accum_gmir_pp_init`` column.

    The premium less prior withdrawals accumulated at the GMIR to the close of policy
    month ``duration_mth_init() - 1``, what ``MYGA_US_S`` carries into that month as the
    :func:`prem_accum_gmir_pp` of the month before. It opens :func:`prem_accum_gmir_pp`
    at :func:`t_entry`, and so the level the ``gmir_floor`` cap holds ``AV + M`` above in
    every month [S13]. It may be negative: withdrawals are deducted from it and nothing
    floors it, in either model. Zero for a point not yet in force, whose premium enters
    it in the issue month.
    """
    return float(data.prem_accum_gmir_pp_init()[idx])                # noqa: F821


def interest_credited_pp_init():
    """Interest credited from issue to the valuation date, per contract.

    The ``interest_credited_pp_init`` column: cumulative interest to the close of policy
    month ``duration_mth_init() - 1``, what ``MYGA_US_S`` carries into that month as the
    :func:`interest_credited_pp` of the month before. It opens
    :func:`interest_credited_pp` at :func:`t_entry`, which the ``min_sc_interest`` MVA
    cap reads in every month — the adjustment is limited to the lesser of the surrender
    charge and the interest credited to date [S8][S9] — and the interest-only allowance
    reads at each anniversary. Zero for a point not yet in force.
    """
    return float(data.interest_credited_pp_init()[idx])              # noqa: F821


def interest_credited_pp_prev_anniv_init():
    """Interest credited from issue to the anniversary opening the contract year under way.

    The ``interest_credited_pp_prev_anniv_init`` column, per contract: cumulative interest
    to the close of policy month ``12 * duration(0) - 1``, the anniversary on or before
    the valuation date. The interest-only allowance of a contract year is the interest
    credited over the year before it [S5][S6], so the allowance of the year after the one
    under way is the interest from this anniversary to the next, and
    :func:`free_wd_allow` reads it there. It is :func:`interest_credited_pp_init` on a
    point valued on an anniversary, the same instant, which ``Data`` checks, and 0 in the
    first contract year, which opened at issue with nothing credited. ``prev_anniv`` is
    the anniversary that **opened** the year. Zero for a point not yet in force.
    """
    return float(data.interest_credited_pp_prev_anniv_init()[idx])   # noqa: F821


def free_wd_allow_init():
    """The free-withdrawal allowance of the contract year under way at the valuation date.

    The ``free_wd_allow_init`` column, per contract, named for the cell that returns it:
    :func:`free_wd_allow` gives it for the contract year in force at ``t = 0``, the one
    opened by the anniversary on or before the valuation date. Under ``pct_av`` it is
    ``free_wd_rate x FWB``, the rate times the account value at that anniversary [S10];
    under ``interest_only`` it is the interest credited over the contract year before
    [S5][S6], which no single anniversary value gives, so the allowance itself is carried
    rather than the base it was fixed on.

    The projection reads it on a valuation **on an anniversary** only,
    ``duration_mth_init()`` a multiple of 12, where month 0 opens the year and
    :func:`free_wd_avail` resets to it; there ``Data`` holds it, to a cent, to
    ``free_wd_rate`` times the account value under ``pct_av``, and under
    ``interest_only`` to at most the interest credited to the anniversary, and in the
    second contract year to exactly that, the first year's. On any other valuation the
    year's remainder,
    :func:`free_wd_remain_init`, carries the year, and this column is read only by
    ``Data``'s check that the remainder does not exceed it. In the first contract year it
    is the issue allowance, ``free_wd_rate x premium`` under ``pct_av`` and 0 under
    ``interest_only``, which ``Data`` checks. Zero for a point not yet in force, which
    takes its allowance from the rule at each anniversary.
    """
    return float(data.free_wd_allow_init()[idx])                     # noqa: F821


def free_wd_remain_init():
    """The unused free-withdrawal allowance carried into month 0, per contract.

    The ``free_wd_remain_init`` column: :func:`free_wd_remain` at the close of policy
    month ``duration_mth_init() - 1``, the year's allowance less what the year's
    withdrawals have already used. :func:`free_wd_avail` opens from it at ``t = 0`` on a
    point valued off an anniversary, and what a surrender at the end of month 0 may still
    shelter is that less month 0's free withdrawal, :func:`free_wd_remain` of month 0. On
    a valuation on an anniversary month 0 opens a new contract year, the allowance resets
    to :func:`free_wd_allow_init`, and last year's remainder lapses unread, the allowance
    being non-cumulative [S4][S16]. ``Data`` refuses a remainder above the year's
    allowance off an anniversary. Zero for a point not yet in force.

    It takes no ``_ytd`` in its name, though it belongs to the contract year: it is not an
    accumulator restarting each year but the remainder of the allowance it is named for,
    :func:`free_wd_allow`, an annual quantity, which each anniversary resets to that
    year's allowance.
    """
    return float(data.free_wd_remain_init()[idx])                    # noqa: F821


def credit_rate_init():
    """i_cr in force entering month 0: the declared rate credited in the month before.

    The ``credit_rate_init`` column: :func:`credit_rate` in policy month
    ``duration_mth_init() - 1``. A declared rate is fixed when it is declared, at issue
    for the initial term [S11] and at each redeclaration after it, so for a point valued
    inside a renewal period whose redeclaration preceded the valuation date it is a fact
    of the past, which this column carries: :func:`credit_rate` returns it wherever the
    declaration in force at month ``t`` was made before :func:`t_entry`. A redeclaration
    at month 0 itself, a valuation on a renewal date, reads the scenario at ``t = 0``,
    and the column, the rate entering that month, is then unread. It equals the initial
    declared rate entering any month of the initial term, the first renewal month
    included, and is the GMIR or more after it; ``Data`` checks both. Zero for a point
    not yet in force.
    """
    return float(data.credit_rate_init()[idx])                       # noqa: F821


def mva_ref_yield_locked_init():
    """i0 in force entering month 0: the MVA reference yield locked for the period in force.

    The ``mva_ref_yield_locked_init`` column, per contract: :func:`mva_ref_yield_locked`
    in policy month ``duration_mth_init() - 1``. ``i0`` is locked at the start of each
    guarantee period — the issue value for the initial term, the prevailing reference
    yield at each renewal under ``rollover`` [S2][S11] — so for a point valued inside a
    renewal period that started before the valuation date it is a fact of the past,
    which :func:`mva_ref_yield_locked` returns wherever the period in force at month
    ``t`` started before :func:`t_entry`. A period starting at month 0 itself locks at the
    scenario's yield at ``t = 0``. It equals ``mva_ref_yield_at_issue`` entering any month
    of the initial term, which ``Data`` checks. Under ``annual_redeclare`` no MVA applies
    after the initial term, and the column is carried unread. Zero for a point not yet
    in force.
    """
    return float(data.mva_ref_yield_locked_init()[idx])              # noqa: F821


def scenario_id():
    """The rate scenario the model point runs on, a key into *rate_scenario.csv*.

    A reporting cell (the Space docstring): ``Data`` joins the scenario by it, through
    :func:`scenario_number`, and no projection cell reads it here.
    """
    return model_point()["scenario_id"]


def wd_schedule_id():
    """The withdrawal programme, a key into *withdrawal_table.csv*.

    A reporting cell (the Space docstring): ``Data`` joins the programme by it, through
    :func:`wd_schedule_number`, and no projection cell reads it here.
    """
    return model_point()["wd_schedule_id"]


def scenario_number():
    """The point's rate scenario, its row of the scenario arrays, from ``Data``.

    ``Data.scenario_number`` numbers the scenarios of *rate_scenario.csv* from 1 in the
    sorted order of their ids and gives each point the number of its ``scenario_id``,
    matched by value as ``MYGA_US_S``'s ``.loc`` matches it. ``Data`` refuses a point
    whose scenario the table lacks, so the number is 1 or more. :func:`scenario_rate`
    reads the arrays at it.
    """
    return int(data.scenario_number()[idx])                          # noqa: F821


def wd_schedule_number():
    """The point's withdrawal programme, its row of ``Data.wd_amount_array``.

    Numbered as :func:`scenario_number` numbers the scenarios, from the programmes of
    *withdrawal_table.csv*; ``Data`` refuses a programme the table lacks, so the number is
    1 or more. :func:`wd_scheduled_pp` reads the array at it.
    """
    return int(data.wd_schedule_number()[idx])                       # noqa: F821


def mort_schedule():
    """The point's sex, its row of ``Data.mort_table_array``.

    Numbered as :func:`scenario_number` numbers the scenarios, from the sexes of
    *mort_table.csv*; ``Data`` refuses a sex the table lacks, so the number is 1 or more.
    :func:`mort_rate_at` reads the array at it, and :func:`proj_len` its last age.
    """
    return int(data.mort_schedule()[idx])                            # noqa: F821


def policy_term():
    """Contract term in years: issue to the anniversary at ``maturity_age`` **[std]**."""
    return maturity_age - age_at_entry()                             # noqa: F821


def maturity_mth():
    """The policy month at which cover ends: ``12 * policy_term()``.

    The deemed maturity falls at the contract anniversary at attained age
    ``maturity_age`` = 100 **[std]**, so this is the ``duration_mth`` of the first month
    not covered, 480 at issue age 60, and the last covered month is
    ``maturity_mth() - 1``, the one ending at that anniversary. It is ``MYGA_US_S``'s
    frame length, counted from issue on the policy clock; :func:`proj_len` counts from the
    valuation date instead.
    """
    return 12 * policy_term()


def proj_len():
    """The number of months from the valuation date to the deemed maturity.

    ``maturity_mth() - duration_mth_init()``: 480 for the anchor cell issued at ``t = 0``,
    468 for it in force 12 months, 1 for the Camp B point in its last covered month, and
    495 for the anchor issued 15 months after the valuation date. The frame is ``t = 0,
    1, ..., proj_len() - 1``; ``proj_len()`` is its exclusive end and the row count of
    :func:`result_cf`, and ``proj_len() - 1`` is the last covered month, the one ending
    at the contract anniversary at ``maturity_age``.

    Four kinds of point have no frame the contract issues or the tables can project, and
    each raises here, naming the point, rather than projecting what the contract does not
    hold, in this order:

    * one issued below ``issue_age_min``, 0, the youngest issue age ``product-spec.md``
      admits. ``MYGA_US_S`` projects any age its tables rate, but the compiled model's
      caches are sized from the contract (``spec_sec.py``): a younger point, whose frame
      and contract years run longer, would read past them;
    * one issued above ``issue_age_max``, 85, the oldest issue age ``product-spec.md``
      admits. No cache is sized from it, since an older issue only shortens every frame,
      and ``MYGA_US_S`` projects such a point; it is refused as a contract the product
      does not issue, and set higher it projects as there;
    * one at or past maturity at the valuation date, which an in-force extract should not
      carry;
    * one whose sex the mortality table rates only to an attained age below
      ``maturity_age - 1``, the last covered month's, every issue age reaching that age in
      its last covered month. ``Data`` cannot check it, ``maturity_age`` being a
      Reference of this Space, so it checks the table's last age by sex,
      ``Data.mort_age_lasts``, here, where ``MYGA_US_S`` raises its ``KeyError`` at the
      first month past the table. The shipped table runs to 120.
    """
    if age_at_entry() < issue_age_min:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is below "
                         f"issue_age_min, {issue_age_min}")           # noqa: F821
    if age_at_entry() > issue_age_max:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: issue age {age_at_entry()} is above "
                         f"issue_age_max, {issue_age_max}")           # noqa: F821
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} "
            f"is at or past maturity, policy month {maturity_mth()}")
    if data.mort_age_lasts()[mort_schedule()] < maturity_age - 1:    # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: the mortality table gives no rate at attained age "
            f"{maturity_age - 1}, the last before the deemed maturity")  # noqa: F821
    return n


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The contract's age in months at ``t = 0``: 12 for the anchor cell valued on its first
    anniversary, 30 for the interest-only point valued the month after its excess
    withdrawal, 0 for a contract issued at the valuation date, and -15 for one to be
    issued 15 months after it, which ``Data`` admits up to ``future_horizon_mth`` months
    ahead. It is read as ``basiclife.BasicTerm_SE`` reads it, as a whole number whatever
    the column's type, and is the one fact the policy clock takes from the model point.
    """
    return int(data.duration_mth()[idx])                             # noqa: F821


def duration_mth(t):
    """Completed policy months at the start of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together. A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame. Negative before issue. It is the technical
    notes' month index, ``MYGA_US_S``'s ``t``, and everything contractual reads it,
    through :func:`duration`, :func:`policy_year`, :func:`age` and :func:`gp_index`.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later. It is the base of every recursion: :func:`pols_if_at` opens there
    from :func:`pols_if_init`, the five value balances from the model point's opening
    state, and the free-withdrawal carry from :func:`free_wd_remain_init`; a rate declared
    or a yield locked before it is read from the opening state too. No cell in cover
    reads a month before it.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and not yet at the deemed maturity.

    ``0 <= duration_mth(t) < maturity_mth()``. False before issue and from the month
    after the one ending at attained age 100. Outside cover every count is zero, and so
    every cash flow; so is every value state and every contractual rate, no count cell
    evaluates a rate there, and no table is read at a contract year or an attained age
    the contract does not have.
    """
    return 0 <= duration_mth(t) < maturity_mth()


def policy_year(t):
    """y(t) = duration(t) + 1: the 1-based contract year containing month t.

    A contractual label on the policy clock — the surrender charge schedule and the base
    lapse table are stated by contract year — never an index into the frame. It is 0 or
    less before issue, where nothing reads a schedule by it.
    """
    return duration(t) + 1


def duration(t):
    """Completed contract years at the start of month t, ``duration_mth(t) // 12``.

    0 throughout the first contract year, and negative before issue.
    """
    return duration_mth(t) // 12


def age(t):
    """The attained age (ANB) during month t, ``age_at_entry() + duration(t)``."""
    return age_at_entry() + duration(t)


def gp_index(t):
    """The index of the guarantee period containing month t, on the policy clock.

    ``duration_mth(t) // (12 n) + 1``: 1 for policy months ``0 .. 12n - 1``, the initial
    term, and ``k + 1`` in the ``k``-th renewal period. Every renewal period is ``n``
    years, as the product has it, so the position in the period is derived from the
    policy clock alone. It is 0 or less before issue, where nothing reads it.
    """
    return duration_mth(t) // (12 * guar_period()) + 1


def gp_start_month(t):
    """The first **policy** month of the guarantee period containing month t.

    ``12 n (gp_index(t) - 1)``: 0 for the initial term. A policy month, not a month of
    the frame: :func:`mva_ref_yield_locked` turns it into a valuation month, and reads the
    opening state where it falls before :func:`t_entry`.
    """
    return 12 * guar_period() * (gp_index(t) - 1)


def gp_end(t):
    """Months remaining in the current guarantee period at the end of month t.

    ``12 n gp_index(t) - (duration_mth(t) + 1)``: 59 in policy month 0 and 0 in policy
    month ``12n - 1``, the month that ends the period.
    """
    return 12 * guar_period() * gp_index(t) - (duration_mth(t) + 1)


def in_gp_window(t):
    """True in the 30-day guarantee-period-end window [S1][S2][S5][S6].

    The notes place the window in the month *after* a guarantee period closes, i.e. at
    ``duration_mth(t) == 0 (mod 12n)`` with ``duration_mth(t) > 0``, so for n = 5 it is
    policy months 60, 120, 180, ... — the first month of each renewal period. In the
    window the full account value is available with **no surrender charge and no MVA**,
    and it is the only month in which annuitization is elected. Under
    ``annual_redeclare`` there is exactly one window, at policy month ``12n``, the month
    after the initial term. False outside cover: no month before issue is a window.
    """
    if not is_active(t):
        return False
    n12 = 12 * guar_period()
    d = duration_mth(t)
    if d <= 0 or d % n12 != 0:
        return False
    if is_annual_redeclare():
        return d == n12
    return True


def redeclare_month(t):
    """The **policy** month at which the credited rate in force at month t was declared.

    Policy month 0 for the initial term; under ``rollover`` the first month of the
    current guarantee period, under ``annual_redeclare`` the first month of the current
    contract year. A policy month, not a month of the frame: :func:`credit_rate` turns it
    into a valuation month, and reads the opening state where it falls before
    :func:`t_entry`.
    """
    n12 = 12 * guar_period()
    if duration_mth(t) < n12:
        return 0
    if is_rollover():
        return n12 * (gp_index(t) - 1)
    return 12 * duration(t)


def scenario_rate(t, name):
    """Step-function lookup of column ``name`` in the model point's rate scenario.

    Each row of *rate_scenario.csv* states the level that holds from its own
    **valuation** month ``t`` until the next row of the same scenario, so a flat path is
    one row at ``t = 0``. The scenario is a path in calendar time, shared by every point
    of a block, so it is read at ``t`` and never on the policy clock. ``name`` is a code,
    ``MVA_REF_YIELD`` or ``MARKET_RATE`` (the Space docstring's *Codes*), for
    ``MYGA_US_S``'s column names; any other raises ``ValueError("invalid name")``.

    The table's one reader. ``Data`` fills each scenario's step function into
    ``data.mva_ref_yield_array()`` and ``data.market_rate_array()``, by scenario and
    valuation month, from the table checked, so the level at ``t`` is one element, read
    at the point's :func:`scenario_number`. Past the table's last month,
    ``data.scenario_last_mth()``, the last level holds, as the step function holds it.
    Before the scenario's first month, ``data.scenario_first_mths()``, it sets no level,
    and the read is refused, naming the point and the month, where ``MYGA_US_S``'s
    ``max()`` of no months raised. ``Data`` refuses a point whose scenario is not in the
    table, or sets no level by the first month the point is on the books, and no cell
    reads the scenario before that month, so a projection never meets the refusal.
    """
    s = scenario_number()
    if t < data.scenario_first_mths()[s]:                            # noqa: F821
        raise ValueError(f"point_id {point_id()}: the rate scenario sets no level of the "
                         f"point's scenario at t = {t}")
    m = min(t, data.scenario_last_mth())                             # noqa: F821
    if name == MVA_REF_YIELD:                                        # noqa: F821
        return float(data.mva_ref_yield_array()[s, m])               # noqa: F821
    elif name == MARKET_RATE:                                        # noqa: F821
        return float(data.market_rate_array()[s, m])                 # noqa: F821
    raise ValueError("invalid name")


def market_rate(t):
    """MR(t): the market competitor rate driving renewal declarations and dynamic lapse.

    VM-22 defines it for a 5 to 7 year guarantee period as the 7-year Treasury rate plus a
    50% A / 50% AA spread less the pricing spread [R2 6.B.5]; the model takes it as an
    exogenous input because the index is a state-filed variable **[std]**.
    """
    return scenario_rate(t, MARKET_RATE)                             # noqa: F821


def mva_ref_yield(t):
    """it: the MVA reference yield at month t, from the scenario table **[std]**.

    The source design is Barclay's US Credit Index with a state-varying formula [S8]; the
    model takes a scalar series rather than hard-coding an index.
    """
    return scenario_rate(t, MVA_REF_YIELD)                           # noqa: F821


def credit_rate(t):
    """i_cr(t): the declared credited rate in force, effective annual.

    The initial declared rate for the whole initial term, policy months ``0 .. 12n - 1``
    [S11], then the renewal rule ``max(GMIR, MR(m) - s_ren)`` **[std]** with ``m`` the
    redeclaration month, :func:`redeclare_month` turned into a valuation month. A rate
    declared before :func:`t_entry` is a fact of the past, the opening state's
    :func:`credit_rate_init`; one declared at or after it is read from the scenario at
    its month, so a valuation on a renewal date takes the new rate from the scenario at
    ``t = 0``. The base run sets ``renewal_spread = 0``, so the credited rate equals the
    competitor rate and the dynamic lapse term is exactly zero. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if duration_mth(t) < 12 * guar_period():
        return declared_rate_initial()
    m = redeclare_month(t) - duration_mth_init()
    if m < t_entry():
        return credit_rate_init()
    floor_rate = gmir()
    renewal = market_rate(m) - renewal_spread                       # noqa: F821
    return max(floor_rate, renewal)


def credit_rate_mth(t):
    """The monthly credited rate, ``(1 + i_cr(t))^(1/12) - 1``.

    Twelve of these factors reproduce the declared effective annual rate exactly, so the
    discretization moves interest only *within* a month. Do not compound daily as well.
    """
    return (1.0 + credit_rate(t)) ** (1.0 / 12.0) - 1.0


def mgsv_rate_mth():
    """The monthly GMSV accumulation rate, ``(1 + i_nf)^(1/12) - 1``."""
    return (1.0 + mgsv_rate()) ** (1.0 / 12.0) - 1.0


def mgsv_rate_statutory(cmt5):
    """The Model #805 indexed nonforfeiture rate at a 5-year CMT level [R1 4.B].

    ``max(0.0015, min(0.03, round(CMT5 to 1/20 of 1%) - 0.0125))``. Two traps the notes
    call out: the floor is **15 basis points, not the widely repeated 1%**; and the
    statute *defines* the minimum rate, it does not cap the contract rate — the contract
    must satisfy ``mgsv_rate() >= mgsv_rate_statutory(cmt5)``, which is what
    :func:`mgsv_rate_is_compliant` tests, not the reverse inequality.

    An engine cell, ``MYGA_US_S``'s formula, ``math`` included: no projection cell calls
    it, so it compiles with a C signature and a dict cache, its body Python, admitted by
    name (the Space docstring's *Reporting cells*), for a user checking a contract rate
    against the statute and for the comparison with ``MYGA_US_S``. A ``mgsv_stat_step``
    of zero raises ``ZeroDivisionError`` with Python's message, ``float division by
    zero``, tested here, as ``MYGA_US_S`` raises it, which compiled division would word
    otherwise.
    """
    step = mgsv_stat_step                                            # noqa: F821
    if step == 0.0:
        raise ZeroDivisionError("float division by zero")
    rounded = math.floor(cmt5 / step + 0.5) * step                   # noqa: F821
    return max(mgsv_stat_floor,                                      # noqa: F821
               min(mgsv_stat_cap, rounded - mgsv_stat_spread))       # noqa: F821


def mgsv_rate_is_compliant(cmt5):
    """True when the contract GMSV rate meets the statutory minimum [R1 4.B].

    At a 5-year CMT level ``cmt5``: ``mgsv_rate() >= mgsv_rate_statutory(cmt5)``. An
    engine cell, as :func:`mgsv_rate_statutory` is, which it alone calls.
    """
    return mgsv_rate() >= mgsv_rate_statutory(cmt5)


def av_pp_init():
    """AV(-1): the account value per contract entering month 0, the ``av_pp_init`` column.

    For a point in force, the closing balance of policy month ``duration_mth_init() - 1``,
    before any month-0 event: what ``MYGA_US_S`` carries into that month as the
    ``av_pp`` of the month before, and the opening balance of :func:`av_pp` and of
    ``av_pp_at(t, BEF_WD)`` at :func:`t_entry`. Zero for a point not yet in force: its
    account value opens empty and takes the premium credited in the issue month,
    :func:`prem_to_av_pp`. ``MYGA_US_S``'s cell of the name computes that issue value,
    ``P (1 - load)``; here the rule moved to the issue month, where it stays a rule.
    """
    return float(data.av_pp_init()[idx])                             # noqa: F821


def prem_to_av_pp(t):
    """Premium credited to the account value per contract, in the issue month.

    ``P x (1 - load_prem_rate)``, 100% of premium with no front-end load [S5][S10][S16],
    at BOM of the month with ``duration_mth(t) = 0``, and 0 in every other month. It is
    the notes' ``av_initial``, which ``MYGA_US_S`` computes as ``av_pp_init()``: fixed at
    issue by a rule the notes state, so computed by that rule rather than read.
    """
    if duration_mth(t) == 0:
        return premium_pp() * (1.0 - load_prem_rate)                 # noqa: F821
    return 0.0


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *withdrawal_table.csv*, else zero.

    The amount at ``(wd_schedule_id, duration_mth(t))``: the table's ``t`` is a
    **policy** month, so a withdrawal programme stays where the contract has it, however
    old the contract is at the valuation date. The anchor's $4,000 at policy month 12
    falls at ``t = 12`` on a contract issued at ``t = 0`` and at ``t = 0`` on one valued
    on its first anniversary. The table's one reader: ``Data`` holds each programme by
    policy month in ``data.wd_amount_array()``, from the table checked, with 0.0 at a
    month the programme has no row, ``MYGA_US_S``'s "a key that misses is no withdrawal",
    and this reads it at the point's :func:`wd_schedule_number`. Past the table's last
    month, ``data.wd_last_mth()``, no programme withdraws. ``Data`` refuses a programme
    the table lacks, so a month without a row is a month the programme takes nothing in,
    never a misspelt programme. 0.0 outside cover, where the policy month may be negative.
    """
    if not is_active(t):
        return 0.0
    m = duration_mth(t)
    if m > data.wd_last_mth():                                       # noqa: F821
        return 0.0
    return float(data.wd_amount_array()[wd_schedule_number(), m])    # noqa: F821


def wd_pp(t):
    """W(t): the gross amount removed from the account value at BOM of month t.

    Gross by construction: a contract promising a stated *net* check needs a gross-up
    solve, which is **not implemented** [S3]. Two sources add up here — the amount
    scheduled in *withdrawal_table.csv*, and the free-withdrawal utilization variant
    ``free_wd_util x FW(y)`` taken in the first month of each contract year, where
    ``duration_mth(t)`` is a multiple of 12. Base run utilization is 0 **[std]**, so only
    the scheduled withdrawals reach the account value: the anchor's $4,000 at policy month
    12 and point 5's $20,000 at policy month 29, on the points made from them. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    util = 0.0
    if free_wd_util and duration_mth(t) % 12 == 0:                 # noqa: F821
        util = free_wd_util * free_wd_allow(policy_year(t))          # noqa: F821
    return wd_scheduled_pp(t) + util


def av_pp(t):
    """AV(t): account value per contract at the end of month t (closing balance).

    ``AV(t) = (AV(t-1) - W(t)) x (1 + i_cr(t))^(1/12)`` [S4][S5][S16], with the premium
    credited, :func:`prem_to_av_pp`, added to the opening balance in the issue month. The
    opening balance ``AV(t-1)`` is the previous month's closing balance, or at
    :func:`t_entry` the account value entering the frame, :func:`av_pp_init`. It is
    written here inline, as ``av_pp_at(t, BEF_WD)`` writes it too, so that the chain of
    calls from month t back to :func:`t_entry` is one cell a month, where
    ``MYGA_US_S``'s ran through ``av_pp_at`` at two timings, three cells a month. No
    charges are deducted from the account value: this chassis carries no front-end load,
    no annual fee and no rider charges [S5][S10][S13][S16]. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = av_pp(t - 1) if t > t_entry() else av_pp_init()
    return (opening + prem_to_av_pp(t) - wd_pp(t)) * (1.0 + credit_rate_mth(t))


def av_pp_at(t, timing):
    """Account value per contract at month t, read at the point given by ``timing``.

    ``BEF_WD`` is ``AV(t-1)``, the opening balance — :func:`av_pp_init` at
    :func:`t_entry` and ``av_pp(t - 1)`` after, plus the premium credited in the issue
    month — written as :func:`av_pp` writes its own opening, so that :func:`av_pp` need
    not call this cell; ``BEF_INV`` is ``AV'(t) = AV(t-1) - W(t)``; ``EOM`` is
    ``AV(t)``, the closing balance. 0.0 outside cover, at every timing.
    """
    if timing == BEF_WD:
        if not is_active(t):
            return 0.0
        opening = av_pp(t - 1) if t > t_entry() else av_pp_init()
        return opening + prem_to_av_pp(t)
    elif timing == BEF_INV:
        return av_pp_at(t, BEF_WD) - wd_pp(t)
    elif timing == EOM:
        return av_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_income_pp(t):
    """Interest credited to one contract's account value at the end of month t."""
    return av_pp_at(t, BEF_INV) * credit_rate_mth(t)


def interest_credited_pp(t):
    """Cumulative interest credited to one contract from issue to the end of month t.

    Used by the ``min_sc_interest`` MVA cap, which limits the adjustment to the lesser of
    the surrender charge and the interest credited to date [S8][S9], and by the
    interest-only free-withdrawal allowance. The interest credited before the valuation
    date opens it at :func:`t_entry`, :func:`interest_credited_pp_init`; nothing has been
    credited before issue. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prior = interest_credited_pp(t - 1) if t > t_entry() else interest_credited_pp_init()
    return prior + inv_income_pp(t)


def prem_accum_gmir_pp(t):
    """Premium less prior withdrawals accumulated at the GMIR, at the end of month t.

    The reference level for the ``gmir_floor`` MVA cap, under which ``AV + M`` may not
    fall below it [S13]; the surrender charge may still breach that level. The premium
    itself enters in the issue month, as in ``MYGA_US_S``, and a point in force opens from
    :func:`prem_accum_gmir_pp_init` at :func:`t_entry`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = (prem_accum_gmir_pp(t - 1) if t > t_entry()
               else prem_accum_gmir_pp_init())
    premium = premium_pp() if duration_mth(t) == 0 else 0.0
    return (opening + premium - wd_pp(t)) * (1.0 + gmir()) ** (1.0 / 12.0)


def free_wd_base(y):
    """FWB(y): the free-withdrawal base fixed at the start of contract year y.

    Purchase payments in year 1, the account value at the most recent anniversary
    thereafter [S10] — the opening balance of policy month ``12 (y - 1)``, the first month
    of year ``y``: ``av_pp_at(t, BEF_WD)`` at the valuation month ``t`` that policy
    month falls in. Making the base a *fixed known amount* at each anniversary is what
    lets ``E(t) = AV(t) - FW(t)`` be evaluated without a fixed point. It is asked only
    for a year that opens on the books: the year under way at the valuation date takes
    its allowance from :func:`free_wd_allow_init`, and needs no base.
    """
    if y <= 1:
        return premium_pp()
    return av_pp_at(12 * (y - 1) - duration_mth_init(), BEF_WD)


def free_wd_allow(y):
    """The free-withdrawal allowance for contract year y, non-cumulative [S4][S16].

    ``pct_av``: ``free_wd_rate x FWB(y)`` [S10]. ``interest_only``: the interest credited
    over the prior contract year [S5][S6] — cumulative interest at the end of the last
    month of year ``y - 1`` less that at the end of the last month of year ``y - 2`` —
    hence zero in year 1. ``greatest_of`` [S13] is not implemented and raises.

    Asked for the contract year under way at the valuation date, a year ``y > 1`` that
    opened at or before it, the allowance is the opening state's,
    :func:`free_wd_allow_init`, under either rule. For the year after it under
    ``interest_only``, the interest at the anniversary that opened the year under way is
    the opening state's too, :func:`interest_credited_pp_prev_anniv_init`. Every later
    year is computed from the frame, its anniversaries' policy months turned into
    valuation months; no formula asks for a year that closed before the valuation date.
    """
    start = 12 * (y - 1) - duration_mth_init()    # the valuation month year y opens in
    if y > 1 and start <= t_entry():
        return free_wd_allow_init()
    if is_pct_av():
        return free_wd_rate() * free_wd_base(y)
    elif is_interest_only():
        if y <= 1:
            return 0.0
        prior = (interest_credited_pp(start - 13) if start - 13 >= t_entry()
                 else interest_credited_pp_prev_anniv_init())
        return interest_credited_pp(start - 1) - prior
    else:
        raise ValueError("invalid free_wd_rule")


def free_wd_avail(t):
    """FW(t): the unused free-withdrawal allowance at BOM of month t, before W(t).

    Reset to the whole allowance in the first month of each contract year, where
    ``duration_mth(t)`` is a multiple of 12, the issue month included; carried forward
    within the year; never carried across an anniversary [S4][S16]. The carry is the
    previous month's allowance less its free withdrawal — :func:`free_wd_remain` of month
    ``t - 1``, written out here so that the chain of calls back to the year's reset is one
    cell a month — and at :func:`t_entry` off an anniversary it is
    :func:`free_wd_remain_init`, the remainder carried into the valuation date. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    if duration_mth(t) % 12 == 0:
        return free_wd_allow(policy_year(t))
    if t > t_entry():
        return free_wd_avail(t - 1) - wd_free_pp(t - 1)
    return free_wd_remain_init()


def wd_free_pp(t):
    """The portion of W(t) covered by the free allowance, hence free of charge and MVA."""
    withdrawal = wd_pp(t)
    allowance = free_wd_avail(t)
    return min(withdrawal, allowance)


def free_wd_remain(t):
    """The unused free-withdrawal allowance after month t's withdrawal.

    This, not :func:`free_wd_avail`, is the allowance a full surrender at the end of month
    t may still shelter.
    """
    return free_wd_avail(t) - wd_free_pp(t)


def wd_excess_pp(t):
    """E(t) for a partial withdrawal: ``max(0, W(t) - FW(t))`` [S8][S9][S10].

    The whole of W(t) when ``free_wd_mva_exempt`` is False [S3][S4].
    """
    if free_wd_mva_exempt():
        return max(0.0, wd_pp(t) - free_wd_avail(t))
    return wd_pp(t)


def surr_excess_pp(t):
    """E(t) for a full surrender at the end of month t: ``AV(t) - FW(t)`` [S8][S11].

    The whole of AV(t) when ``free_wd_mva_exempt`` is False [S3][S4].
    """
    if free_wd_mva_exempt():
        return max(0.0, av_pp(t) - free_wd_remain(t))
    return av_pp(t)


def surr_charge_id(t):
    """The surrender charge schedule in force: ``INITIAL``, ``RENEWAL`` or ``NONE``.

    Under ``rollover`` a fresh renewal schedule attaches at each guarantee-period boundary
    [S1][S2][S11]; under ``annual_redeclare`` no charge applies after the initial term
    [S13]. Getting this clock wrong relocates the shock lapse by years. ``MYGA_US_S``
    returns the schedule's key in *surr_charge_table.csv*, ``initial`` or ``renewal``, or
    ``none``; here each is a code (the Space docstring's *Codes*), and ``INITIAL`` and
    ``RENEWAL`` are the rows of ``data.surr_charge_array()`` that hold the two schedules.
    ``Data`` refuses a table that lacks ``initial`` or ``renewal``.
    """
    if gp_index(t) <= 1:
        return INITIAL                                               # noqa: F821
    if is_annual_redeclare():
        return NONE                                                  # noqa: F821
    return RENEWAL                                                   # noqa: F821


def surr_charge_year(t):
    """sc_clock: the contract year within the schedule in force, 1..n.

    ``policy_year(t) - n (gp_index(t) - 1)``: 1 for policy months ``0 .. 11`` and again
    for the first twelve months of each renewal period. Resets to 1 at each renewal under
    ``rollover`` [S1][S2][S11]. The two registered contracts instead run the clock from
    the original purchase payment date so it never restarts [S3][S4]; that variant is not
    carried on this chassis.
    """
    return policy_year(t) - guar_period() * (gp_index(t) - 1)


def surr_charge_age_cap(t):
    """The attained-age cap on the surrender charge in month t [S1] [S2].

    :func:`surr_charge_age_cap_at` at the attained age, ``age(t)``: 4% at 94 down to 0%
    at 98-100, and 1.0, no cap, below the sourced age band. 0.0 outside cover, where no
    age is the contract's.
    """
    if not is_active(t):
        return 0.0
    return surr_charge_age_cap_at(age(t))


def surr_charge_age_cap_at(a):
    """The attained-age cap on the surrender charge at attained age ``a``, from its table.

    4% at 94 down to 0% at 98-100 [S1] [S2]; 1.0, no cap, below the sourced age band, and
    the last row's value above it. The one cell that reads *surr_charge_age_cap.csv*,
    keyed by age: :func:`surr_charge_age_cap` calls it at ``age(t)``, inside cover only.
    The band's first and last ages are ``data.surr_charge_age_cap_first()`` and
    ``data.surr_charge_age_cap_last()``, taken from the ages ``Data`` has checked before
    a cap is read, and the cap is one element of ``data.surr_charge_age_cap_array()``,
    the same checked table by attained age from 0, read only from the first age on, where
    it holds no padding. ``Data`` refuses a negative age, so the first is 0 or more.
    """
    lo = data.surr_charge_age_cap_first()                            # noqa: F821
    hi = data.surr_charge_age_cap_last()                             # noqa: F821
    if a < lo:
        return 1.0
    return float(data.surr_charge_age_cap_array()[min(a, hi)])       # noqa: F821


def surr_charge_rate(t):
    """sc(y): the surrender charge rate in force at month t.

    9/8/7/6/5 over the initial term [S10] and 5/4/3/2/1 over a renewal term [S2], capped
    by the attained-age scale [S1][S2], zero once a schedule runs out, and zero in the
    30-day guarantee-period-end window [S1][S2]. The schedules' one reader: ``Data``
    holds the two the projection reads in ``data.surr_charge_array()``, by schedule code
    and contract year, from the table checked, where each runs from year 1 without a
    gap, and each schedule's last year in ``data.surr_charge_last_years()``. So the rate
    is one element, at the code :func:`surr_charge_id` returns and the year of the
    schedule's clock, and a year past the schedule's last has no charge, where
    ``MYGA_US_S``'s lookup missed and returned 0.0. Neither the ``NONE`` row, the year-0
    column nor a year past a schedule's last is read, which hold padding. 0.0 outside
    cover, before any schedule is read.
    """
    if not is_active(t):
        return 0.0
    schedule = surr_charge_id(t)
    if schedule == NONE or in_gp_window(t):                          # noqa: F821
        return 0.0
    y = surr_charge_year(t)
    if y < 1 or y > data.surr_charge_last_years()[schedule]:         # noqa: F821
        return 0.0
    rate = float(data.surr_charge_array()[schedule, y])              # noqa: F821
    cap = surr_charge_age_cap(t)
    return min(rate, cap)


def mva_term(t):
    """T(t): the MVA duration in years at the end of month t [S8].

    The notes write it as (days to the end of the current contract year / 365) + whole
    years remaining in the MVA period. On a monthly grid those two terms collapse
    algebraically to ``(12 n k - (d + 1)) / 12`` with ``d = duration_mth(t)`` — the time
    from the end of month ``t`` to the end of the current MVA period, ``k = gp_index(t)``
    — and the same quantity serves as the geometric branch's ``tau``, which the notes
    define as days to maturity / 365.25. The two divisors differ in the sources; on exact
    twelfths they cannot. 0.0 outside cover, as once the MVA period has run out. The
    whole years remaining are :func:`mva_term_years`, an int, as ``MYGA_US_S``'s local
    ``whole_years_left`` is, so the sum is ``MYGA_US_S``'s.
    """
    if not is_active(t):
        return 0.0
    d = duration_mth(t)
    if is_annual_redeclare() and d >= 12 * guar_period():
        return 0.0
    months_to_year_end = 12 * policy_year(t) - (d + 1)
    return months_to_year_end / 12.0 + mva_term_years(t)


def mva_term_years(t):
    """The whole years of T(t): the MVA period's years left after the current one, an int.

    ``n k - y`` with ``k = gp_index(t)`` and ``y = policy_year(t)``, 0 or more in cover,
    where :func:`mva_term` adds the months to the end of the current contract year, at
    most 11/12. So ``int(mva_term(t))`` is this wherever :func:`mva_duration_factor`
    reads it, which reads it here instead: an ``int()`` of a float compiles to Python
    arithmetic, and this to C. 0 outside cover and once the MVA period has run out, where
    :func:`mva_term` is 0.0.
    """
    if not is_active(t):
        return 0
    if is_annual_redeclare() and duration_mth(t) >= 12 * guar_period():
        return 0
    return guar_period() * gp_index(t) - policy_year(t)


def mva_in_force(t):
    """True when an MVA applies at month t.

    ``mu(t) = 0`` unconditionally once the MVA period has expired [S8][S13][S16] and in
    the 30-day guarantee-period-end window [S2]. It is also zero on a death benefit
    [S2][S4][S8][S13][S16], on annuitization [S16], and on RMD or waiver withdrawals
    [S2][S5][S13]; the first two are handled where those benefits are valued and the
    third is not implemented. False outside cover.
    """
    if not is_active(t):
        return False
    return mva_term(t) > 0.0 and not in_gp_window(t)


def mva_ref_yield_locked(t):
    """i0: the reference yield locked at the start of the current guarantee period.

    The model point's issue value for the initial term; re-locked at the prevailing
    reference yield at each renewal under ``rollover`` [S2][S11], read at the valuation
    month the period starts in, :func:`gp_start_month` turned into ``t``. A period that
    started before :func:`t_entry` was locked at a yield of the past, the opening state's
    :func:`mva_ref_yield_locked_init`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if gp_index(t) <= 1:
        return mva_ref_yield_at_issue()
    m = gp_start_month(t) - duration_mth_init()
    return mva_ref_yield(m) if m >= t_entry() else mva_ref_yield_locked_init()


def mva_ref_term_years(tau):
    """The whole-year maturity at which the distribution yield is read [S4].

    Partial years round **up**, capped at the guarantee period: one registered contract
    reads a 3-year yield for 985/365.25 = 2.69 years remaining while the exponent keeps
    the exact day count. With a single scalar reference yield per scenario this selection
    determines nothing; it is carried so a curve-valued extension has the rule in place.

    An engine cell, ``MYGA_US_S``'s formula unchanged, ``math`` included, as
    :func:`mgsv_rate_statutory` is: no projection cell calls it. Compiled, it returns a C
    ``long long``, so a term below ``-2**63``, outside any term, overflows there, where
    modelx returns Python's int.
    """
    return min(guar_period(), int(math.ceil(tau)))                   # noqa: F821


def mva_duration_factor(t):
    """F_s: the declared-differential adjustment factor by years remaining [S14].

    A contractual table of modified durations, read on the ``Ic < 6%`` or ``Ic >= 6%``
    column and linearly interpolated between whole years, flat beyond the last row,
    ``data.mva_factor_last_year()``, taken from the years ``Data`` has checked. The
    table's one reader: ``data.mva_factor_array()`` holds it by whole year remaining, 0
    to the last, ``factor_lo`` in column 0 and ``factor_hi`` in column 1, and each factor
    is one element, at the whole years :func:`mva_term_years`, 0 or more in cover, and
    the year after, read only below the last. The years are read here, keyed by ``t``,
    rather than through a cell keyed by the year: their bound is the table's last year
    and the guarantee period, data no contract bound holds, from which no cache could be
    sized. 0.0 outside cover, before the table is read.
    """
    if not is_active(t):
        return 0.0
    column = 0 if credit_rate(t) < mva_factor_rate_split else 1    # noqa: F821
    years = mva_term(t)
    last = data.mva_factor_last_year()                               # noqa: F821
    lower = mva_term_years(t)
    if lower >= last:
        return float(data.mva_factor_array()[last, column])          # noqa: F821
    f0 = float(data.mva_factor_array()[lower, column])               # noqa: F821
    f1 = float(data.mva_factor_array()[lower + 1, column])           # noqa: F821
    return f0 + (f1 - f0) * (years - lower)


def mva_rate(t):
    """mu(t): the market value adjustment rate at month t, signed and dimensionless.

    ``linear_duration`` **[std]**: ``(i0 - it) x T(t)`` [S8][S9] — the first-order
    approximation of the geometric form, always in the contract holder's disfavour when
    rates rise. ``geometric``: ``Phi(t) - 1`` [S3][S4], where the factor
    ``Phi = ((1 + i0) / (1 + it + s_adm)) ** T(t)``, with ``s_adm`` the
    ``mva_admin_spread``, 25 bp in one registered contract [S4], covering the cost of
    liquidating fixed-income investments and structurally biasing the adjustment against
    the owner; the other registered variant sets it to zero [S3]. ``MYGA_US_S`` computes
    the factor in a cell of three float parameters, ``mva_factor_geometric``, which here
    is written inline, the same expression in the same order, since a cell keyed by
    floats compiles to a Python dict. ``declared_differential``: ``(Ic - In) x F_s`` on
    the insurer's own new-money rate [S14], with ``In`` taken as the market rate
    **[std]**.

    The geometric factor's numerator and divisor are bound to locals in ``MYGA_US_S``'s
    order, and a divisor of zero, a reference yield of ``-1 - s_adm``, raises
    ``ZeroDivisionError`` here with Python's message, ``float division by zero``, as
    ``MYGA_US_S`` raises it, which compiled division would word otherwise.
    """
    if not mva_in_force(t):
        return 0.0
    if is_linear_duration():
        return (mva_ref_yield_locked(t) - mva_ref_yield(t)) * mva_term(t)
    elif is_geometric():
        locked = 1.0 + mva_ref_yield_locked(t)
        current = 1.0 + mva_ref_yield(t) + mva_admin_spread          # noqa: F821
        if current == 0.0:
            raise ZeroDivisionError("float division by zero")
        return (locked / current) ** mva_term(t) - 1.0
    elif is_declared_differential():
        return (credit_rate(t) - market_rate(t)) * mva_duration_factor(t)
    else:
        raise ValueError("invalid mva_family")


def surr_charge_pp(t):
    """C(t): the surrender charge on a full surrender at the end of month t."""
    return surr_charge_rate(t) * surr_excess_pp(t)


def mva_pp(t):
    """M(t): the capped MVA on a full surrender at the end of month t.

    The MVA rate on the surrender's base, :func:`surr_excess_pp`, capped by one of five
    rules, all first-class parameters because the cap is the largest single
    cross-carrier divergence in the source set:

    ``sym_sc`` **[std]**
        ``clamp(M_raw, -C, +C)`` [S2].
    ``min_sc_interest``
        ``clamp(M_raw, -K, +K)`` with ``K = min(C, interest credited to date)`` [S8][S9].
    ``asym_sc_snfl``
        ``M <= +C`` with no downside cap; only ``SB >= MGSV`` binds below [S12].
    ``gmir_floor``
        ``AV + M >=`` premium less prior withdrawals accumulated at the GMIR [S13]. The
        floor is stated for a full surrender; applying it to a partial withdrawal base is
        an extension of the source.
    ``none``
        Uncapped and fully two-sided [S3][S4].

    ``MYGA_US_S`` caps an MVA on any currency base in one cell, ``mva_pp_on(t, base)``,
    which this and :func:`wd_mva_pp` call. A cell keyed by a float compiles to a Python
    dict, so here each writes the cap inline on its own base, the same expressions in
    the same order. A rule none of the five raises, as there.
    """
    base = surr_excess_pp(t)
    raw = mva_rate(t) * base
    if is_cap_none():
        return raw
    charge = surr_charge_rate(t) * base
    if is_cap_sym_sc():
        return max(-charge, min(charge, raw))
    elif is_cap_min_sc_interest():
        limit = min(charge, interest_credited_pp(t))
        return max(-limit, min(limit, raw))
    elif is_cap_asym_sc_snfl():
        return min(charge, raw)
    elif is_cap_gmir_floor():
        return max(raw, prem_accum_gmir_pp(t) - av_pp(t))
    else:
        raise ValueError("invalid mva_cap_rule")


def wd_charge_pp(t):
    """The surrender charge on month t's partial withdrawal."""
    return surr_charge_rate(t) * wd_excess_pp(t)


def wd_mva_pp(t):
    """The capped MVA on month t's partial withdrawal.

    :func:`mva_pp`'s cap, on the withdrawal's base, :func:`wd_excess_pp`, written inline
    as there.
    """
    base = wd_excess_pp(t)
    raw = mva_rate(t) * base
    if is_cap_none():
        return raw
    charge = surr_charge_rate(t) * base
    if is_cap_sym_sc():
        return max(-charge, min(charge, raw))
    elif is_cap_min_sc_interest():
        limit = min(charge, interest_credited_pp(t))
        return max(-limit, min(limit, raw))
    elif is_cap_asym_sc_snfl():
        return min(charge, raw)
    elif is_cap_gmir_floor():
        return max(raw, prem_accum_gmir_pp(t) - av_pp(t))
    else:
        raise ValueError("invalid mva_cap_rule")


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``W(t) + M(t) - C(t)``."""
    return wd_pp(t) + wd_mva_pp(t) - wd_charge_pp(t)


def surr_value_pp(t):
    """SV(t): the gross surrender value, ``AV(t) + M(t) - C(t)``, before the floor.

    The composition order is **account value, then MVA, then surrender charge, then the
    nonforfeiture floor**, and it is not interchangeable: both M and C are computed on
    E(t) *before* either is deducted [S8]. Charging first and adjusting the net figure
    understates the adjustment by ``sc x |M|``; flooring before the MVA silently removes
    the downside protection.
    """
    return av_pp(t) + mva_pp(t) - surr_charge_pp(t)


def surr_benefit_pp(t):
    """SB(t): the surrender benefit actually paid, ``max(SV(t), MGSV(t))`` [S8][S9][S12].

    A binding floor is **not** a separate cash flow: it raises SB(t), and
    ``MGSV(t) - SV(t)`` is a reconciliation quantity only.
    """
    cash = surr_value_pp(t)
    guaranteed = mgsv_pp(t)
    return max(cash, guaranteed)


def mgsv_pp_init():
    """MGSV(-1): the Model #805 floor per contract entering month 0.

    The ``mgsv_pp_init`` column: for a point in force, the floor at the close of policy
    month ``duration_mth_init() - 1``, before any month-0 event, what ``MYGA_US_S``
    carries into that month as the ``mgsv_pp`` of the month before, and the opening value
    of :func:`mgsv_pp` at :func:`t_entry`. It may be negative: every withdrawal is
    deducted from the floor and nothing floors it at zero, in either model, so heavy
    withdrawals take it below. Zero for a point not yet in force: its floor opens with
    87.5% of gross consideration in the issue month, :func:`prem_to_mgsv_pp`.
    ``MYGA_US_S``'s cell of the name computes that issue value; here the rule moved to
    the issue month, where it stays a rule.
    """
    return float(data.mgsv_pp_init()[idx])                           # noqa: F821


def prem_to_mgsv_pp(t):
    """The consideration the Model #805 floor opens with, per contract, in the issue month.

    ``net_consideration_ratio x P``, 87.5% of gross consideration [R1 4.A(2)][S11], at BOM
    of the month with ``duration_mth(t) = 0``, and 0 in every other month. It is the
    notes' ``mgsv_initial``, which ``MYGA_US_S`` computes as ``mgsv_pp_init()``: computed
    by the statutory rule rather than read, because shipping it as data would let a model
    point silently violate the statute.
    """
    if duration_mth(t) == 0:
        return net_consideration_ratio * premium_pp()                # noqa: F821
    return 0.0


def mgsv_charge_pp(t):
    """c(t): the monthly slice of the annual contract charge deducted from the floor.

    0.0 outside cover, where there is no contract to charge.
    """
    if not is_active(t):
        return 0.0
    return mgsv_annual_charge() / 12.0


def mgsv_wd_deduct_pp(t):
    """d(t): the withdrawal deducted from the Model #805 floor in month t.

    W(t) under the ``gross`` convention [S11]; the cash actually paid,
    ``W(t) + M(t) - C(t)``, under ``net_of_charges`` [S9].
    """
    if is_wd_gross():
        return wd_pp(t)
    elif is_wd_net_of_charges():
        return wd_payment_pp(t)
    else:
        raise ValueError("invalid mgsv_wd_convention")


def mgsv_pp(t):
    """MGSV(t): the Model #805 minimum guaranteed surrender value at end of month t.

    ``MGSV(t) = [MGSV(t-1) - d(t) - c(t)] x (1 + i_nf)^(1/12)`` [R1 4.A][S11], with the
    consideration the floor opens with, :func:`prem_to_mgsv_pp` = 0.875 x P, added to the
    opening value in the issue month. The opening value ``MGSV(t-1)`` is the previous
    month's closing value, or at :func:`t_entry` the floor entering the frame,
    :func:`mgsv_pp_init`. Premium tax actually paid and indebtedness are further
    permitted deductions, accumulated at the same rate, and are zero here. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    opening = mgsv_pp(t - 1) if t > t_entry() else mgsv_pp_init()
    return ((opening + prem_to_mgsv_pp(t) - mgsv_wd_deduct_pp(t) - mgsv_charge_pp(t))
            * (1.0 + mgsv_rate_mth()))


def taxable_wd_pp(t):
    """The income-first taxable portion of month t's withdrawal [R6 72(e)(3)(A)].

    Taxable to the extent the account value **gross of surrender charge** exceeds the
    basis at the start of the month, which at :func:`t_entry` is
    :func:`tax_basis_pp_init`. A reported quantity: it generates no insurer cash flow.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    opening_basis = tax_basis_pp(t - 1) if t > t_entry() else tax_basis_pp_init()
    gain = max(0.0, av_pp_at(t, BEF_WD) - opening_basis)
    return min(wd_pp(t), gain)


def tax_basis_pp(t):
    """basis(t): the IRC 72 investment in the contract at the end of month t [R6].

    Reduced only by the non-taxable remainder of a withdrawal; the opening basis of month
    :func:`t_entry` is :func:`tax_basis_pp_init`. Reported, not a cash flow. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    opening = tax_basis_pp(t - 1) if t > t_entry() else tax_basis_pp_init()
    return opening - (wd_pp(t) - taxable_wd_pp(t))


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, from *mort_table.csv*.

    The shipped table is an illustrative Makeham curve **[std]**, *not* a published
    basis. The prescribed basis is the 2012 IAM Basic table with Projection Scale G2 and
    the VM-22 Table 6.7 factors [R2 6.B.8][R9], which may not be redistributed here;
    swap it in by repointing ``Data.mort_table_file`` before the model computes anything.
    Mortality is second-order on this product: death pays the full account value with no
    charge and no MVA. 0.0 outside cover, before the table is read.

    No factor multiplies the table's rate, and ``Data`` refuses a rate outside 0 to 1, so
    none is above 1, and none is capped: the shipped rates in cover are 0.263 at most, at
    attained age 99. The rate is :func:`mort_rate_at`, the table's one reader, at the
    attained age, ``age(t)``. ``Data`` refuses a point whose sex the table lacks, or whose
    attained age in its first month on the books it gives no rate at, and :func:`proj_len`
    one whose sex it rates only below the attained age of the last covered month, where
    ``MYGA_US_S`` raises its ``KeyError`` once the projection gets there; on the shipped
    table, which runs to 120, no contract reaches one.
    """
    if not is_active(t):
        return 0.0
    return mort_rate_at(age(t))


def mort_rate_at(a):
    """The annual mortality rate at attained age ``a`` for the point's sex.

    The one cell that reads *mort_table.csv*, keyed by age, as
    :func:`surr_charge_age_cap_at` is: :func:`mort_rate` calls it at ``age(t)``, inside
    cover only. ``Data`` holds the table checked in ``data.mort_table_array()``, by sex,
    numbered as :func:`mort_schedule` numbers it, and attained age from 0, and each sex's
    first and last age in ``data.mort_age_firsts()`` and ``data.mort_age_lasts()``. An age
    outside the sex's is refused, naming the point and the age, where ``MYGA_US_S``'s
    lookup raised a ``KeyError``; inside, the rate is one element, never padding.
    ``Data`` refuses a negative age, so the first is 0 or more.
    """
    s = mort_schedule()
    if a < data.mort_age_firsts()[s] or a > data.mort_age_lasts()[s]:  # noqa: F821
        raise ValueError(f"point_id {point_id()}: the mortality table gives no rate at "
                         f"attained age {a}")
    return float(data.mort_table_array()[s, a])                      # noqa: F821


def mort_rate_mth(t):
    """q(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def gmir_factor():
    """G: the VM-22 GMIR factor stepping the base lapse rate [R2 6.B.5].

    1.25 at a GMIR of 1.0% or less, 1.00 up to 2.5%, 0.70 above. The representative 0.25%
    GMIR [S11] therefore takes the **highest** multiplier, which is the conservative end
    of the prescribed scale.
    """
    rate = gmir()
    if rate <= gmir_band_low:                                        # noqa: F821
        return gmir_factor_low                                       # noqa: F821
    elif rate <= gmir_band_high:                                     # noqa: F821
        return gmir_factor_mid                                       # noqa: F821
    else:
        return gmir_factor_high                                      # noqa: F821


def lapse_rate_base(t):
    """Base(y): the prescribed base lapse rate for the contract year containing month t.

    VM-22 Table 6.5 mapped onto the five-year architecture as a **[std] extension**
    [R2][REG-R36]. ``rollover``: 1% inside each guarantee period and 75% in the contract
    year following each expiry, repeating with period n. ``annual_redeclare``: 1% to
    expiry, 75%, then 10%, 7.5% and 3% thereafter. **The architecture switch, not the
    level, is the first-order modeling decision** — Camp A creates a repeating shock,
    Camp B a single one. 0.0 outside cover, where no contract year is the contract's.
    """
    if not is_active(t):
        return 0.0
    year = policy_year(t)
    n = guar_period()
    if is_rollover():
        if year > n and (year - 1) % n == 0:
            return lapse_base_shock                                  # noqa: F821
        return lapse_base_igp                                        # noqa: F821
    if year <= n:
        return lapse_base_igp                                        # noqa: F821
    elif year == n + 1:
        return lapse_base_shock                                      # noqa: F821
    elif year == n + 2:
        return lapse_base_post1                                      # noqa: F821
    elif year == n + 3:
        return lapse_base_post2                                      # noqa: F821
    else:
        return lapse_base_ult                                        # noqa: F821


def lapse_dyn_exponent(t):
    """X: the dynamic-lapse exponent [R2].

    2.0 during the initial surrender charge period, 2.5 at the shock and after. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    if policy_year(t) <= guar_period():
        return lapse_exp_sc                                          # noqa: F821
    return lapse_exp_post                                            # noqa: F821


def lapse_dyn_market(t):
    """Market(t): the credited-minus-competitor response of the VM-22 dynamic lapse form.

    ``-1.25 (CR - MR)^X`` when the contract is competitive, zero inside the 50 bp buffer,
    ``+1.25 (MR - BF - CR)^X`` when it is not [R2 6.B.5]. The buffer and the power make
    the sensitivity strongly convex around ``CR = MR``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    cr = credit_rate(t)
    mr = market_rate(t)
    power = lapse_dyn_exponent(t)
    if cr >= mr:
        return -lapse_slope * (cr - mr) ** power                     # noqa: F821
    elif cr >= mr - lapse_buffer:                                    # noqa: F821
        return 0.0
    else:
        return lapse_slope * (mr - lapse_buffer - cr) ** power       # noqa: F821


def lapse_dyn_rate(t):
    """Rate(t): the dynamic term gated by the surrender-charge and negative-MVA haircut.

    ``Market(t) x max(0, 1 - 5 (1 - CSV/AV))`` with ``CSV/AV = SB(t)/AV(t)`` [R2 6.B.5],
    so the dynamic response switches off entirely once the combined haircut reaches 20%.
    The ITM factor is 1 for an Accumulation contract with no guaranteed living or death
    benefit, which the guideline states explicitly. 0.0 outside cover, where the
    surrender benefit and the account value are both 0.0 and their ratio would be 0/0.

    In cover, an account value of zero, which a scheduled withdrawal of the whole account
    value reaches, raises ``ZeroDivisionError``, as ``MYGA_US_S`` does: the divisor is
    tested and the error raised here, with Python's message, ``float division by zero``,
    which compiled division would word otherwise. The two operands are read in
    ``MYGA_US_S``'s order, the surrender benefit first.
    """
    if not is_active(t):
        return 0.0
    benefit = surr_benefit_pp(t)
    account = av_pp(t)
    if account == 0.0:
        raise ZeroDivisionError("float division by zero")
    haircut = 1.0 - benefit / account
    return lapse_dyn_market(t) * max(0.0, 1.0 - lapse_itm_gate * haircut)  # noqa: F821


def mva_lapse_factor_at(t):
    """Phi_MVA(t): the factor multiplying the dynamic term while an MVA is in force.

    The VM-22 prescribed values are 0 in force and 1 expired [R2], i.e. the regulator's
    view is that an in-force MVA *completely* neutralizes disintermediation. The model
    exposes the in-force value as ``mva_lapse_factor``, defaulting to the best-estimate
    **0.35 [std]** rather than the prescribed 0; set it to 0 for the statutory run. It is
    a judgement, not a calibration — sensitivity-test it.
    """
    return mva_lapse_factor if mva_in_force(t) else 1.0              # noqa: F821


def lapse_rate(t):
    """w_annual(t): ``clamp(Base(y) G + Rate(t) Phi_MVA(t), 0.005, 0.90)`` [R2 6.B.5].

    The **annual** total surrender rate, paired with :func:`lapse_rate_mth` exactly as
    :func:`mort_rate` is paired with :func:`mort_rate_mth`.

    On the base deterministic run ``MR = CR`` and ``renewal_spread = 0``, so
    ``Market(t) = Rate(t) = 0`` and this is ``Base(y) x 1.25``: contract years 1 to 5 at
    1.25% and the shock year at 90%, the 93.75% product capped. 0.0 outside cover, where
    the clamp would otherwise give its 0.5% floor.
    """
    if not is_active(t):
        return 0.0
    rate = (lapse_rate_base(t) * gmir_factor()
            + lapse_dyn_rate(t) * mva_lapse_factor_at(t))
    return min(lapse_rate_max, max(lapse_rate_min, rate))            # noqa: F821


def lapse_rate_mth(t):
    """w(t): the monthly total surrender rate, ``1 - (1 - w_annual)^(1/12)``.

    This is the rate the monthly decrement actually applies; :func:`lapse_rate` is the
    annual rate it is derived from.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def annuitization_rate(t):
    """a(t): the monthly annuitization election rate.

    1.0% of in-force in each 30-day guarantee-period-end window after contract year 1 and
    zero elsewhere **[std]**. No public annuitization take-up study for deferred annuities
    was located; VM-22 prescribes 0% at all projection intervals for the standard
    projection [R2 6.B.6], which is a statutory simplification rather than an experience
    estimate. Set ``annuitization_rate_window = 0`` for the statutory alternative.
    """
    return annuitization_rate_window if in_gp_window(t) else 0.0     # noqa: F821


def pols_if(t):
    """l(t-1): the number in force at the **start** of month t, the weight of row t.

    ``pols_if_at(t, BEF_DECR)``: the count carried in from month t - 1 plus month t's
    new business, before month t's decrements — the population that takes the month's
    withdrawal, carries its expenses and is exposed to its decrements, so it is the
    weight on every cash flow of the same :func:`result_cf` row. On a point issued at
    ``t = 0`` it is exactly ``MYGA_US_S``'s ``pols_if``. A point in force at the
    valuation date opens with :func:`pols_if_init`, and one issued at or after it with
    its issued count in the issue month. Zero outside cover: before issue, and from
    ``t = proj_len()`` on, because the survivors of the last covered month are annuitized
    out through :func:`pols_maturity`.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity. The notes' end-of-month
    ``l(t) = l(t-1)(1 - a(t))(1 - q(t))(1 - w(t))`` is ``pols_if_at(t, AFT_DECR)``, which
    equals ``pols_if_at(t + 1, BEF_NB)`` in every month but the last covered one.
    """
    return pols_if_at(t, BEF_DECR)


def pols_new_biz(t):
    """Number of contracts issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point
    issued at the valuation date, ``t = k`` for one issued ``k`` months later. A point
    already in force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_if_at(t, timing):
    """In-force at month t read at the point given by ``timing``.

    The timings in processing order:

    ``BEF_NB``
        the count carried in from month t - 1, before month t's new business: the
        survivors of month t - 1's annuitizations, deaths and surrenders, out of month
        t - 1's ``BEF_DECR`` count. At :func:`t_entry`, the first month on the books,
        it is :func:`pols_if_init`, the count in force at the valuation date (0 for a
        point issued at or after it), and the recursion reads no earlier month. Zero
        outside cover, so the survivors of the last covered month leave as
        :func:`pols_maturity`.
    ``BEF_DECR``
        ``l(t-1)``: ``BEF_NB`` plus :func:`pols_new_biz`, before any decrement; the
        same number as :func:`pols_if`, and the weight on that month's cash flows.
    ``BEF_MORT``
        after annuitization elections, ``l(t-1)(1 - a(t))``.
    ``BEF_LAPSE``
        after deaths, ``l(t-1)(1 - a(t))(1 - q(t))``.
    ``AFT_DECR``
        after surrenders, ``l(t)`` — the notes' end-of-month in-force, which in the last
        covered month is what :func:`pols_maturity` annuitizes out.

    The order is the notes' ``l(t) = l(t-1)(1 - a)(1 - q)(1 - w)`` **[std order]**.
    ``BEF_NB`` and ``BEF_DECR`` are ``basiclife.BasicTerm_SE``'s names, and any timing
    but these five raises. ``BEF_NB`` forms the count left at the end of month t - 1
    itself — month t - 1's ``BEF_NB`` plus its :func:`pols_new_biz`, after its three
    decrements, the products ``AFT_DECR`` takes in the order it takes them — rather than
    calling for it. So the chain of calls from month t back to :func:`t_entry` is one
    cell a month, where ``MYGA_US_S``'s ran through two. Every count is zero outside
    cover, before any rate is read.
    """
    if timing == BEF_NB:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1))
                * (1.0 - annuitization_rate(t - 1)) * (1.0 - mort_rate_mth(t - 1))
                * (1.0 - lapse_rate_mth(t - 1)))
    elif timing == BEF_DECR:
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)
    elif timing == BEF_MORT or timing == BEF_LAPSE or timing == AFT_DECR:
        if not is_active(t):
            return 0.0
        pols = pols_if_at(t, BEF_DECR)
        pols = pols * (1.0 - annuitization_rate(t))
        if timing == BEF_MORT:
            return pols
        pols = pols * (1.0 - mort_rate_mth(t))
        if timing == BEF_LAPSE:
            return pols
        return pols * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_annuitization(t):
    """Annuitization elections in month t, taken at BOM before crediting.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_DECR) * annuitization_rate(t)


def pols_death(t):
    """Deaths in month t, on the in-force net of annuitization elections.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_MORT) * mort_rate_mth(t)


def pols_lapse(t):
    """Full surrenders in month t, on the survivors of annuitization and mortality.

    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_LAPSE) * lapse_rate_mth(t)


def pols_maturity(t):
    """Deemed-maturity annuitizations, non-zero only in the last covered month.

    That month is ``duration_mth(t) = maturity_mth() - 1``, the frame's last row,
    ``t = proj_len() - 1``. Not a decrement — the projection horizon runs out — but
    needed for the in-force roll-forward to close; see the Space docstring.
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
    elif kind == ANNUITIZATION:
        return pols_annuitization(t)
    elif kind == MATURITY:
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def annuitization_pp(t):
    """The amount transferred to the payout model on an annuitization election.

    The full account value ``AV'(t)`` in the 30-day window; outside it, ``AV'(t)`` less the
    surrender charge computed on ``AV'(t)``, with **no MVA** [S1][S2][S5][S16][std].

    The notes name ``SV(t)`` for the non-window case, and ``SV(t) = AV(t) + M(t) - C(t)``
    is composed on the *post*-crediting account value — but the same notes make
    annuitization an elective **BOM** transaction and set ``mu(t) = 0`` on it. The two
    cannot both hold on a monthly grid, and the model resolves it at BOM: annuitizers
    leave before the month's interest is credited, which is exactly what
    :func:`claim_from_av_pp` releases for them (``AV'(t)``, not ``AV(t)``). This cell is
    therefore the BOM analogue of ``SV(t)`` — the same composition on the account value
    the annuitant actually takes with them. Reading ``SV(t)`` literally would pay out one
    month of interest the block never credited to those contracts, and the difference
    ``(AV(t) - AV'(t)) * (1 - sc(y))`` would surface as a spurious
    :func:`claims_over_av`. The choice is inert on every shipped model point, where
    ``a(t)`` is zero outside the window; a test pins it open.

    No nonforfeiture floor is applied in either branch: ``SV(t)`` is the pre-floor value.
    Payout factors are out of scope: no retrieved product document contains an annuity
    rate table, so the accumulation model emits the transfer and hands the amount on.
    """
    account = av_pp_at(t, BEF_INV)
    if in_gp_window(t):
        return account
    excess = (max(0.0, account - free_wd_remain(t)) if free_wd_mva_exempt()
              else account)
    return account - surr_charge_rate(t) * excess


def claim_pp(t, kind):
    """The benefit paid per contract in month t by ``kind``.

    ``DEATH`` is the full account value with no charge and no MVA [S1][S2][S13],
    floored at the cash surrender benefit and hence at MGSV(t) [R1 6]; on the base run the
    floor is inert because 4.45% exceeds 2.80%, but at a renewal rate down to the GMIR it
    overtakes the account value, so it is tested at every duration **[std]**.
    ``LAPSE`` is SB(t). ``ANNUITIZATION`` is :func:`annuitization_pp`.
    ``MATURITY`` is the account value floored at MGSV at the projection horizon.
    """
    if kind == DEATH:
        account = av_pp(t)
        benefit = surr_benefit_pp(t)
        return max(account, benefit)
    elif kind == LAPSE:
        return surr_benefit_pp(t)
    elif kind == ANNUITIZATION:
        return annuitization_pp(t)
    elif kind == MATURITY:
        account = av_pp(t)
        guaranteed = mgsv_pp(t)
        return max(account, guaranteed)
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The account value released per contract by a claim of ``kind``.

    Equal to :func:`claim_pp` except where the Model #805 floor binds; the difference is
    :func:`claims_over_av`. Annuitizers leave at BOM and so release ``AV'(t)``, before the
    month's interest.
    """
    if kind == ANNUITIZATION:
        return av_pp_at(t, BEF_INV)
    elif kind == DEATH or kind == LAPSE or kind == MATURITY:
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single purchase payment, on the contracts issued in month t.

    ``premium_pp() x pols_new_biz(t)``, a beginning-of-month flow of the issue month, the
    notes' "at ``t = 0``". A point in force at the valuation date paid its premium before
    it, and has none.
    """
    return premium_pp() * pols_new_biz(t)


def prem_to_av(t):
    """Premium credited to the account value, on the contracts issued in month t."""
    return prem_to_av_pp(t) * pols_new_biz(t)


def withdrawals(t):
    """Withdrawal payments in month t: ``(W(t) + M(t) - C(t))`` weighted by ``l(t-1)``.

    The ledger separates the free part (``wd_free_pp``, never charged or adjusted) from
    the excess (``wd_excess_pp``); this line is the total cash paid. The weight is
    :func:`pols_if`, the start-of-month count printed on this same row of
    :func:`result_cf`, because the withdrawal is taken at BOM before any decrement. Zero
    outside cover.
    """
    if not is_active(t):
        return 0.0
    return wd_payment_pp(t) * pols_if(t)


def claims(t, kind):
    """Benefit outgo in month t, for one ``kind`` or, with ``ALL``, all four.

    ``ALL`` is ``MYGA_US_S``'s ``kind=None``, its total, a code here (the Space
    docstring's *Codes*), since a parameter that is sometimes ``None`` compiles to a
    Python object. The total is ``MYGA_US_S``'s expression, the four kinds added left to
    right, so it is ``MYGA_US_S``'s bit for bit, a negative zero included. ``ALL`` is the
    one code this takes that :func:`claim_pp` and :func:`pols_decr` refuse.
    """
    if kind == ALL:                                                  # noqa: F821
        return (claims(t, DEATH) + claims(t, LAPSE)
                + claims(t, ANNUITIZATION) + claims(t, MATURITY))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The account value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind):
    """Benefit paid less the account value released, ``claims - claims_from_av``.

    Signed, and normally **negative** on this chassis: a surrender pays out less than the
    account value it releases, by the surrender charge and any negative MVA. It turns
    positive exactly when the Model #805 floor binds and SB(t) exceeds AV(t). Either way
    it is a reconciliation quantity, not a cash flow of its own — a binding floor raises
    SB(t), it does not add a separate top-up line, and the charge and the MVA are
    internal accounting entries rather than ledger lines. With ``ALL``, all four, as
    :func:`claims` totals them.
    """
    if kind == ALL:                                                  # noqa: F821
        return (claims_over_av(t, DEATH) + claims_over_av(t, LAPSE)
                + claims_over_av(t, ANNUITIZATION) + claims_over_av(t, MATURITY))
    return claims(t, kind) - claims_from_av(t, kind)


def commissions(t):
    """Acquisition commission: 2.00% of premium paid at issue, in the issue month **[std]**.

    No retrieved document discloses MYGA commission; this is a pure modeling assumption.
    """
    return comm_rate_acq * premiums(t)                               # noqa: F821


def premium_taxes(t):
    """Premium tax on the purchase payment, 0% **[std]** [S3][S16]."""
    return premium_tax_rate() * premiums(t)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + inflation_rate) ** (t // 12)``.

    On the **valuation** clock: ``t`` counts months from the valuation date, so the
    maintenance charge it inflates is in valuation-date dollars, whatever the contract's
    age, and every point of a block inflates alike. ``MYGA_US_S``'s annual step is kept,
    ``1.025^k`` from ``t = 12 k`` to ``12 k + 11``, but it falls every twelve months from
    the valuation date rather than on the contract's anniversaries. On a point issued at
    ``t = 0`` the two are the same; on the anchor cell in force 12 months this model's
    charge is ``MYGA_US_S``'s divided by 1.025 in every month. Defined in every month,
    before issue too: it is an input, not a state of the contract.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """Insurer expenses: acquisition on new business and inflating maintenance **[std]**.

    ``(50 / 12) x 1.025^(t // 12)`` per contract per month on the valuation clock,
    in-force weighted, plus the acquisition expense ``expense_acq`` per contract issued,
    in the issue month, on :func:`pols_new_biz` and not inflated, as in
    ``basiclife.BasicTerm_SE``. A point in force at the valuation date never sees it,
    because it was issued before; ``MYGA_US_S`` charges it at ``t = 0`` on the contracts
    in force there, which on a point issued at ``t = 0`` is the same charge. VM-22
    prescribes $35 x 1.025^(offset) per contract for business the company does not
    administer [R2 6.B.3]; the $50 figure is a **[std]** uplift of that anchor to a
    self-administered block. ``expense_acq`` is 0 because this chassis's only acquisition
    cost is the commission. Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    acquisition = expense_acq * pols_new_biz(t)                      # noqa: F821
    maintenance = (expense_maint / 12.0) * inflation_factor(t)       # noqa: F821
    return acquisition + maintenance * pols_if(t)


def net_cf(t):
    """Net cash flow in month t.

    Interest credited, the surrender charge, the MVA and the movement of the Model #805
    floor are **internal accounting entries**, not ledger lines: they drive AV, MGSV and
    the benefit *amount* but are never cash flows of their own. Only amounts paid to or
    received from the contract holder, and the insurer's own expenses, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t, ALL)
            - commissions(t) - expenses(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted account value at month t; see :func:`av_pp_at` for ``timing``.

    Each timing carries the in-force appropriate to that point in the month: ``l(t-1)``
    before the withdrawal, ``l(t-1)(1 - a(t))`` once annuitizers have left, and at the end
    of the month the count that survives *every* exit — ``pols_if_at(t + 1, BEF_NB)``,
    the count carried into the next month before its new business, which is ``l(t)``
    except in the last covered month, where the deemed maturity empties the block. Using
    ``pols_if_at(t, AFT_DECR)`` there would leave the matured account value standing in
    the block *and* released as a claim, and :func:`check_av_roll_fwd` would not close.
    In the issue month the ``BEF_WD`` value is the premium just deposited, on the
    contracts just issued.
    """
    if timing == BEF_WD:
        return av_pp_at(t, BEF_WD) * pols_if(t)
    elif timing == BEF_INV:
        return av_pp_at(t, BEF_INV) * pols_if_at(t, BEF_MORT)
    elif timing == EOM:
        return av_pp(t) * pols_if_at(t + 1, BEF_NB)
    else:
        raise ValueError("invalid timing")


def inv_income(t):
    """Interest credited to the whole block in month t."""
    return av_at(t, BEF_INV) * credit_rate_mth(t)


def wd_from_av(t):
    """The account value released by month t's withdrawals, gross of charge and MVA."""
    return wd_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's account value over month t.

    Closing balance less the previous month's closing balance. At :func:`t_entry` the
    previous balance is the block's account value entering the frame,
    ``av_pp_init() * pols_if_init()``, which is nothing for a point not yet in force: its
    block holds nothing before the purchase payment, so in the issue month the change is
    the whole closing balance and :func:`prem_to_av` is the deposit that explains it.
    """
    opening = av_at(t - 1, EOM) if t > t_entry() else av_pp_init() * pols_if_init()
    return av_at(t, EOM) - opening


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual in month t; zero to floating point.

    ``AV(t) - AV(t-1) = premium in - withdrawals out + interest credited - the account
    value released by each of the four claim kinds``. Note that the *cash* paid on a
    surrender may exceed the account value released when the Model #805 floor binds; that
    excess is :func:`claims_over_av` and is not part of this identity. In the issue month
    the premium deposit is the ``premium in`` term; a point in force opens from its
    block's account value entering month 0 (:func:`av_change`).

    The signed residual, for a debugging session that needs to know *where* and *by how
    much* :func:`check_av_roll_fwd` failed.
    """
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - claims_from_av(t, ANNUITIZATION) - claims_from_av(t, DEATH)
                - claims_from_av(t, LAPSE) - claims_from_av(t, MATURITY))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the account value roll-forward closes in every projected month.

    Takes no argument and returns a bool, following ``CashValue_SE.check_av_roll_fwd`` and
    the library convention, so one test can call the same check across every model.
    :func:`check_av_roll_fwd_resid` carries the per-month signed residual, and this is
    ``abs(resid) <= check_tol_av x max(policy_count(), 1)`` over ``t = 0 .. proj_len() -
    1``: the tolerance scales with the count, since the residual is rounding on that many
    contracts. On a point counting one contract it is ``MYGA_US_S``'s check.
    """
    tol = check_tol_av * max(policy_count(), 1.0)                    # noqa: F821
    for t in range(proj_len()):
        if abs(check_av_roll_fwd_resid(t)) > tol:
            return False
    return True


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual in month t; zero to floating point.

    ``pols_if(t) - pols_if_at(t + 1, BEF_NB) = annuitizations + deaths + surrenders +
    deemed maturities``: the start-of-month count opens the row, the four exits are taken
    during it, and the next month opens on what is left, before its own new business,
    which is no part of month t's movement. In the notes' own indexing that is
    ``l(t-1) - l(t)``, since :func:`pols_if` is the start-of-month count.

    The signed residual; :func:`check_pols_roll_fwd` is the bool over all ``t``.
    """
    return (pols_if(t) - pols_if_at(t + 1, BEF_NB) - pols_annuitization(t)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    No argument, returns a bool over ``t = 0 .. proj_len() - 1``, matching
    :func:`check_av_roll_fwd` and the library convention. The tolerance is
    ``check_tol_pols x max(policy_count(), 1)``, scaling with the count as the residual
    does.
    """
    tol = check_tol_pols * max(policy_count(), 1.0)                  # noqa: F821
    for t in range(proj_len()):
        if abs(check_pols_roll_fwd_resid(t)) > tol:
            return False
    return True


def result_cf():
    """Result table of cashflows, one row per month ``t = 0 .. proj_len() - 1``.

    Row 0 is the valuation month for every model point, so the frames of a block line up
    and sum row by row, and a point issued after the valuation date has zeros until its
    issue month. The columns are ``MYGA_US_S``'s. The purchase payment, the acquisition
    commission and the premium tax are beginning-of-month flows of the issue month, the
    notes' "at ``t = 0``", and sit on the same row as that month's interest, decrements and
    maintenance expense.

    The ``pols_if`` column is the **start**-of-month count, which is the weight applied
    to every cash flow on that same row, so the printed in-force reconciles with the
    printed flows: ``withdrawals(t) / wd_payment_pp(t)`` and
    ``expenses(t) / ((expense_maint / 12) * inflation_factor(t))`` both return it, the
    second outside the issue month.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, DEATH) for t in ts],
            "claims_lapse": [claims(t, LAPSE) for t in ts],
            "claims_annuitization": [claims(t, ANNUITIZATION) for t in ts],
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

    The counts :func:`result_cf` weights its rows by, and how they move, as
    ``basiclife.BasicTerm_SE``'s ``result_pols`` sets them out: ``pols_if``, the count of
    month t; ``pols_new_biz``, the part of it issued in month t; then month t's
    annuitizations, deaths and surrenders in processing order, and the deemed maturities
    of the last covered month; then ``pols_if_aft_decr``, the notes' end-of-month
    ``l(t)``, as in ``MYGA_US_S``. Row by row, ``pols_if`` at ``t + 1`` is ``pols_if``
    less the four outflows of month t, plus the new business of month ``t + 1``, and
    ``pols_if_aft_decr`` is that count before the new business in every month but the
    last covered one, where the deemed maturity empties the block. Zeros before issue.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "pols_annuitization": [pols_annuitization(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, AFT_DECR) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract account value and surrender values, by month t.

    One row per month ``t = 0 .. proj_len() - 1``, zeros before a point's issue. The first
    five columns are the worked example's table — the opening balance ``AV(t-1)``,
    ``W(t)``, ``AV'(t)``, the closing balance ``AV(t)`` and ``MGSV(t)`` — and the rest are
    its surrender trace, available at every duration. The trace's ``free_wd_avail``
    column, ``MYGA_US_S``'s name, holds :func:`free_wd_remain`, the allowance left after
    the month's withdrawal, which a surrender at the end of the month may still shelter,
    not :func:`free_wd_avail`, the allowance before it.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp_bef_wd": [av_pp_at(t, BEF_WD) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp_bef_inv": [av_pp_at(t, BEF_INV) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "mgsv_pp": [mgsv_pp(t) for t in ts],
            "free_wd_avail": [free_wd_remain(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "mva_pp": [mva_pp(t) for t in ts],
            "surr_value_pp": [surr_value_pp(t) for t in ts],
            "surr_benefit_pp": [surr_benefit_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

issue_age_min = 0

issue_age_max = 85

maturity_age = 100

net_consideration_ratio = 0.875

load_prem_rate = 0.0

renewal_spread = 0.0

comm_rate_acq = 0.02

expense_acq = 0.0

expense_maint = 50.0

inflation_rate = 0.025

free_wd_util = 0.0

annuitization_rate_window = 0.01

lapse_base_igp = 0.01

lapse_base_shock = 0.75

lapse_base_post1 = 0.1

lapse_base_post2 = 0.075

lapse_base_ult = 0.03

lapse_rate_min = 0.005

lapse_rate_max = 0.9

lapse_slope = 1.25

lapse_buffer = 0.005

lapse_itm_gate = 5.0

lapse_exp_sc = 2.0

lapse_exp_post = 2.5

gmir_band_low = 0.01

gmir_band_high = 0.025

gmir_factor_low = 1.25

gmir_factor_mid = 1.0

gmir_factor_high = 0.7

mva_lapse_factor = 0.35

mva_admin_spread = 0.0025

mva_factor_rate_split = 0.06

mgsv_stat_step = 0.0005

mgsv_stat_spread = 0.0125

mgsv_stat_cap = 0.03

mgsv_stat_floor = 0.0015

check_tol_av = 1e-06

check_tol_pols = 1e-12

BEF_NB = 0

BEF_DECR = 1

BEF_MORT = 2

BEF_LAPSE = 3

AFT_DECR = 4

BEF_WD = 5

BEF_INV = 6

EOM = 7

DEATH = 0

LAPSE = 1

ANNUITIZATION = 2

MATURITY = 3

ALL = 4

MVA_REF_YIELD = 0

MARKET_RATE = 1

NONE = 0

INITIAL = 1

RENEWAL = 2

math = ("Module", "math")

pd = ("Module", "pandas")
