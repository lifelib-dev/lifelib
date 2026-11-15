# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

r"""The by-contract projection of :mod:`~.RILA_US_SEC`.

``RILA_US_S`` run from a valuation date. The Space is parameterized by ``idx``, the
position of a model point in the table and in every :mod:`~.RILA_US_SEC.Data` vector, as
``basiclife.BasicTerm_SC`` is: ``Projection[0]`` is an ItemSpace projecting the table's
first row, model point 1, the anchor cell issued at the valuation date, where every
number is ``RILA_US_S``'s, and :func:`point_id` is its label::

    >>> Projection[0].result_iv()          # the worked example's own table
    >>> Projection[0].result_cf()
    >>> Projection[15].result_cf()         # point 16, the anchor cell in force 71 months
    >>> Projection[0].point_id()           # 1, the row's point_id
    >>> Projection.idx = 1                 # or switch the default, before computing

Compiled, no cache is ever cleared: set ``idx``, like every Reference, on a model just
imported, before anything is computed, or project through ``Projection[i]``. modelx
recomputes what a Reference reaches when it is set; a compiled ItemSpace takes the
References when it is made and keeps every value it has computed until it is deleted,
and the base ``Projection`` and ``Data`` keep theirs for good. And it holds each Reference
as a C variable of its shipped value's type: a float set on an int Reference truncates
toward zero, and an int set on a float Reference reads as a float
(``products/registered_index_linked_annuity/model-sec.md``, *What it refuses*).

Any ``idx`` makes an ItemSpace, and none is refused here. ``Projection[-1]`` reads every
vector at its last element, as numpy and a compiled memoryview both do, so it is the
table's last point, under that point's own :func:`point_id`; an ``idx`` past the last
row raises ``IndexError`` at its first read of a vector, which modelx reports inside its
``FormulaError``.

This is :mod:`~.RILA_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``, and then made to compile, as
``basiclife.BasicTerm_SC`` is made from ``basiclife.BasicTerm_S``, on the deferred
chassis :mod:`.MYGA_US_SEC` compiled first and the index crediting of
:mod:`.FIA_US_SEC`. A formula of :mod:`~.RILA_US_S` is rewritten where it depends on where
the projection starts, where it must answer for a month outside cover, where it compared
a timing, a kind or a switch as text, where it priced at a float argument, or where it
reads a table or text the compiled model holds as numbers; every other is
:mod:`~.RILA_US_S`'s own. ``products/registered_index_linked_annuity/model-sec.md`` lists
the rewritten cells with the reason for each.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/registered_index_linked_annuity/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an input
can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RILA_US_SEC`` folder without its parent's CSVs produces a model that
reads and then fails on first evaluation.

The readers and the filename References live on the sibling
:mod:`~.RILA_US_SEC.Data` Space, reached here through the ``data``
Reference, so each file is read once per model rather than once per model point. Five of
the files are ``RILA_US_S``'s, read in place; the model point table and the market
scenarios are this model's own:

=========================  ==================================  ==========================
Reference (on Data)        Cells                               File
=========================  ==================================  ==========================
model_point_file           data.model_point_table()            model_point_table_sec.csv
mort_table_file            data.mort_table()                   mort_table.csv
market_scenario_file       data.market_scenario()              market_scenario_sec.csv
surr_charge_file           data.surr_charge_table()            surr_charge_table.csv
guar_min_rate_file         data.guar_min_rate_table()          guar_min_rate_table.csv
lapse_file                 data.lapse_table()                  lapse_table.csv
withdrawal_file            data.withdrawal_table()             withdrawal_table.csv
=========================  ==================================  ==========================

``market_scenario`` is the input class peculiar to this product: the *contractual* formula
consumes market data, so the index level, the Market Value Rate, the risk-free rate, the
dividend yield and the implied volatility are inputs on the same footing as the
withdrawal-charge schedule, not a valuation overlay. It runs on the valuation clock
(below), and each model point restated in force or issued after the valuation date reads
its own copy of its scenario, re-based to its month.

.. rubric:: Projection basis

``t`` counts **months from the valuation date** and is **0-based**: ``t = 0`` is the
valuation month, the same month for every model point however old the contract, month
``t`` runs from time ``t`` to time ``t + 1``, and the frame is ``t = 0 … proj_len() - 1``,
so ``len(result_cf()) == proj_len()``, with ``proj_len() = maturity_mth() -
duration_mth_init()``. The **policy clock** is :func:`duration_mth`,
``duration_mth_init() + t``, the policy months elapsed at the start of month ``t``, which is
``RILA_US_S``'s ``t``: on a contract issued at the valuation date the two clocks coincide,
and every number is ``RILA_US_S``'s. Following the notes, every within-month quantity is
evaluated at the month **end**, time ``t + 1``: the market state, the interim value, the
Account Value and the benefits on row ``t`` are the values there, while ``pols_if(t)`` is
the count entering the month at time ``t``. The Issue Date opens the contract's first
month, the one with ``duration_mth(t) == 0``, so the purchase payment, the acquisition
expense and the opening state of a contract issued at or after the valuation date fall
inside that row rather than in a row of their own.

**Two clocks.** The market runs on the **valuation** clock, which every point of a block
shares: the index level, the Market Value Rate and the option-pricing market month ``t``
is valued at are the scenario's at time ``t + 1`` (:func:`market_state`), and expense
inflation steps every twelve months from the valuation date (:func:`inflation_factor`).
Everything contractual runs on the **policy** clock: the terms and their Term Start and
End Dates (:func:`term_elapsed_mth`), the Contract Anniversaries and the free-withdrawal
base snapshotted at them, the withdrawal charge and the surrender behaviour keyed to it,
the attained age, the withdrawal programme (:func:`wd_amount_pm`) and the Maturity Date
(:func:`maturity_mth`). Each test of a month against a contractual date reads
``duration_mth(t)``, and a policy month that names a month to read, a Term Start Date or
an anniversary, is turned into a month from the valuation date once, by subtracting
``duration_mth_init()``, in the one cell that reads it.

**A month-end valuation has two readings of "the contract year", and the model carries
both.** ``duration(t) = duration_mth(t) // 12`` is the *interval* reading and lifelib's
0-based duration: the complete contract years elapsed at the **start** of month ``t``,
i.e. the contract year the whole month lies inside. It is the right one for a rate that
applies across the month — the attained age behind ``q_m(t)`` (:func:`age`).
``duration_eom(t) = (duration_mth(t) + 1) // 12`` is the *instant* reading, the notes'
``cy`` at the month end: how many complete contract years have elapsed at time ``t + 1``,
where the month's transactions and decrements settle. It is the right one for the
withdrawal charge a transaction bears (:func:`surr_charge_rate`), the free-withdrawal base
snapshotted at an anniversary (:func:`free_wd_base`), and the surrender behaviour keyed to
that charge (:func:`policy_year`, :func:`lapse_rate_sc_mult`, :func:`lapse_rate_base`),
which must see the charge expire in the same month the contract does. The two differ
**only in the month that closes on an anniversary**: at policy month 11 ``duration`` is 0
but ``duration_eom`` is 1, so that month bears the age-``x`` mortality rate while a
surrender settling at its end is already on the year-2 side of the charge schedule. The
expense inflation step is the one annual step on the valuation clock instead,
``1.025^(t // 12)``, so that every point of a block carries its expenses in
valuation-date dollars.

:mod:`.MYGA_US_S` needs only one reading, because its beginning-of-month transaction
convention makes the two coincide: there the anniversary month belongs to the year that is
opening, here the anniversary closes the month that has just run, and the two products'
``policy_year`` readings differ in exactly that one month a year. Each convention is the
right one for its own timing basis.

Within month ``t`` the notes' processing order is: refresh the **market state**; apply
**term-end crediting** if ``t`` is a Term End Date; apply the **renewal / transfer** roll
split and re-strike the option; compute **interim values**; accrue the **accounts** and
set the Account Value, snapshotting the free-withdrawal base on a Contract Anniversary;
take **contract-holder transactions**; and apply **decrements** at the end of the month —
death at ``q_m(t)``, then surrender at ``w_m(t)`` on survivors **[std order]**, plus the
discrete term-end surrender fraction ``phi`` at a Term End Date.

Two conventions carry that order through the cells. Every quantity of the option bucket is
**homogeneous of degree one in the Investment Amount** — the notes require it, and the
model imposes it by holding the per-unit ratio :func:`iv_ratio` and multiplying, so a
withdrawal reduces the interim value by exactly the cash removed. And each month's
valuation refers to the option **in force during that month**, which at a Term End Date is
the *expiring* one: :func:`tau` is 0 there, not ``T``, so the replicating portfolio
collapses to intrinsic value and reproduces the crediting rate exactly.

.. rubric:: In force at the valuation date

A model point is a contract issued at the valuation date (``duration_mth_init() == 0``),
one already in force there (the months since issue), or one to be issued ``k`` months
later (``-k``), up to ``Data.future_horizon_mth`` months on. Every recursion opens at
:func:`t_entry`, the first month on the books, and none reads a month before it. A
contract issued at or after the valuation date opens as ``RILA_US_S`` opens at issue: the
purchase payment allocated wholly to the option, the general accounts empty, no free
withdrawal amount, its contracts entering as :func:`pols_new_biz` in the issue month. A
contract in force opens from the model point's opening state, what ``RILA_US_S`` carries
into the valuation month, per contract, before any month-0 event: the Investment Amount,
which is also the crediting basis, the Fixed and Holding Accounts, the Account Value, the
Free Withdrawal Amount still unused and the return-of-premium base
(:func:`inv_amt_pp_init`, :func:`fixed_acct_pp_init`, :func:`holding_acct_pp_init`,
:func:`av_pp_init`, :func:`free_wd_remain_init`, :func:`rop_pp_init`), and the Account
Value at the Contract Anniversary on or before the valuation date, the base of the
contract year's Free Withdrawal Amount (:func:`av_pp_prev_anniv_init`); its count in
force is :func:`pols_if_init`.

The **term under way** is fixed at its Term Start Date. Where that date precedes the
valuation month, its index level, its Market Value Rate and its option-pricing market are
the model point's (:func:`index_at_term_start_init` and the four beside it), and so is the
cap re-solved there at a renewal under ``nge_reset`` (:func:`cap_rate_init`): facts frozen
at a past date, which a change to the market or to a Reference at the valuation date must
not move, and which no scenario re-based to the valuation date holds. A term that starts
at or after the valuation month reads its start from the scenario, as ``RILA_US_S`` does,
and re-solves its cap there. Terms align with issue, every ``12 x term_years`` policy
months, so the Term Start Date follows from the policy clock and takes no column.
``RILA_US_S`` does not implement the Performance Lock, and this model, ``RILA_US_S`` run in
force, adds none: a contract carries no lock flag and no locked value.

The Account Value may be of **either sign**. It is the interim value plus the two
accounts, and the interim value can be negative even when the index has risen [S2], so
``Data`` accepts any finite opening Account Value and refuses instead a contract in force
that holds nothing, no investment amount and no account balance.

.. rubric:: Naming

Cell names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``, and
this library's deferred annuity chassis :mod:`.MYGA_US_S`, wherever those have
an analogue — ``pols_*`` for policy counts, ``av_*`` for account values, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-contract amounts, ``*_at(t, timing)``
for a quantity read at a point inside the month, ``*_init`` for a contract's opening state
at the valuation date (``basiclife.BasicTerm_SE``'s ``pols_if_init``), ``*_pm(m)`` for a
schedule read by policy month and ``*_py(y)`` by contract year. The technical notes use
compact actuarial symbols instead. The mapping is:

===========================  ================================  =============================
Notes symbol                 Cells                             Meaning
===========================  ================================  =============================
(valuation clock)            t, the cells argument             Month from the valuation
                                                               date, 0-based; time t opens
                                                               month t
t                            duration_mth(t)                   Policy months elapsed at the
                                                               start of month t
(none)                       duration_mth_init()               Policy months at the
                                                               valuation date; -k if issued
                                                               k months on
(none)                       t_entry()                         First month on the books
(the point's label)          point_id()                        point_id of row idx
(none)                       is_active(t)                      Whether month t is in cover
cy(t) = floor(t/12)          duration(t)                       Complete years during month t
cy_end(t) = floor((t+1)/12)  duration_eom(t)                   Complete years at t's month
                                                               end
cy_end(t) + 1                policy_year(t)                    Contract year in force there
x                            age_at_entry                      Issue age (ANB)
x + cy(t)                    age(t)                            Attained age (ANB) during t
(Maturity Date)              policy_term                       Years from issue to maturity
(Maturity Date)              maturity_mth()                    Policy month cover ends at
(none)                       proj_len                          Months projected from the
                                                               valuation date
P                            premium_pp                        Single purchase payment
T                            term_years                        Index-linked term in years
(Term Start Date)            term_start_month(t)               First month of that term, a
                                                               policy month
(none)                       term_elapsed_mth(t)               Months elapsed in that term
(Term End Date)              is_term_end(t)                    True when t ends a term
tau_k(t)                     tau(t)                            Years remaining in the term
(the market path)            market_state(t, name)             The scenario at time t from
                                                               the valuation date
(the scenario's row)         scenario_number()                 Its row in Data's arrays
I(t)                         index_level(t)                    Index level
I_s                          index_at_term_start(t)            Index level at the Term Start
I_s, before t = 0            index_at_term_start_init          I_s of a term begun before
                                                               the valuation month
R_k(t)                       index_perf(t)                     I(t)/I_s - 1
r(t)                         mvr(t)                            Market Value Rate (CMT)
r_0                          mvr_at_term_start(t)              Market Value Rate at term
                                                               start
r_0, before t = 0            mvr_at_term_start_init            r_0 of a term begun before
                                                               the valuation month
(r, q, sigma)                risk_free(t), div_yield(t),       Option-pricing market state
                             impl_vol(t)
(r, q, sigma) at term start  risk_free_at_term_start(t),       Option-pricing market on the
                             div_yield_at_term_start(t),       Term Start Date
                             impl_vol_at_term_start(t)
(the same, before t = 0)     risk_free_at_term_start_init,     Their values for a term begun
                             div_yield_at_term_start_init,     before the valuation month
                             impl_vol_at_term_start_init
N(.)                         norm_cdf(x)                       Standard normal c.d.f.
d1, d2                       bs_d1(...), bs_d2(...)            Black-Scholes arguments
C(I,K,tau)                   bs_call(...)                      European call
P(I,K,tau)                   bs_put(...)                       European put
BC(I,K,tau)                  bs_binary_call(...)               Cash-or-nothing binary call
b                            buffer                            Buffer
c, s, e (model point)        declared_cap, declared_step,      Rates declared on the model
                             declared_edge                     point
c                            cap_rate(t)                       Cap Rate in force, floored
c, before t = 0              cap_rate_init                     Cap re-solved at a renewal
                                                               before the valuation month
s                            step_rate(t)                      Step Rate in force, floored
e                            edge_rate(t)                      Edge Rate in force, floored
PR                           participation                     Participation Rate
f                            floor_rate                        Floor (optional module)
(crediting type)             is_cap_crediting(),               crediting_type decoded
                             is_step_crediting(),
                             is_edge_crediting(),
                             is_floor_crediting()
(interim value family)       is_iv_portfolio(),                iv_family decoded
                             is_iv_notional(),
                             is_iv_delta(),
                             is_iv_legacy()
(amortization rule)          is_straight_line(),               amort_rule decoded
                             is_updated_expiry()
guar_min_cap(T)              guar_min_rate(kind)               Contractual minimum by term
(one option leg)             opt_component(t, leg, ...)        Signed per-unit leg value
(one leg, by basis)          opt_component_at(t, leg, basis)   The same, keyed by a basis
                                                               code, priced inline
(the leg count)              opt_leg_count()                   Legs of the replicating set
(one leg's code)             opt_leg(i)                        Code of leg i, in S's order
(Pi, by basis)               opt_portfolio_at(t, basis)        Pi on a basis code
(sum of \|legs\|, by basis)  opt_portfolio_abs_at(t, basis)    Trading-cost base on a basis
Pi(I, tau)                   opt_portfolio(t, spot, tau, mkt)  Per-unit portfolio value
(sum of \|legs\|)            opt_portfolio_abs(...)            Trading-cost assessment base
beta                         opt_budget(t)                     Initial option budget
y_e, spread                  earned_rate, nge_spread           Earned rate; target margin
                                                               [std]
beta_target(T)               opt_budget_target()               NGE cap-solve target
(the cap solve)              declared_cap_solved(t)            Cap solving Pi = beta_target
(the same, once a term)      cap_solved_at_start(t)            Its bisection, keyed by start
g                            credit_rate_term(t)               Term-end crediting rate
AccruedCapRate               credit_rate_accrued(t)            Pre-AG 54 time-prorated rate
(g by rule)                  credit_rate_by(t, rule)           Either rate, keyed by a rule
                                                               code
B_k(t)                       budget_amort_pp(t)                Amortized initial budget
F_k(t)                       fixed_proxy_pp(t)                 Fixed Income Asset Proxy
D_k(t)                       deriv_proxy_pp(t)                 Derivative Asset Proxy
TC_k(t)                      trading_cost_pp(t)                Trading cost provision
kappa                        trading_cost_rate                 Trading cost factor
[(1+r_0)/(1+r(t))]^tau       mva_factor(t)                     Interim-value rate adjustment
CCF_k(t)                     cap_calc_factor(t)                Cap Calculation Factor,
                                                               family (b)
E_0                          iv_expense_rate                   CCF expense rate [std],
                                                               family (b)
rate(t), family (b)          risk_free(t) + iv_credit_spread   Investment-grade discount
                                                               rate
DailyAdjustment(t)           fixed_proxy_factor(t),            Family (c), the delta form
                             deriv_proxy_factor(t)
V_k(t)                       interim_value_pp_at(t, timing)    Interim Value
V_k(t)/IA_k(t)               iv_ratio(t)                       Interim Value per unit of
                                                               base
(the decomposition base)     iv_notional_pp(t, timing)         Notional a component sits on
IA_k(t)                      inv_amt_pp(t)                     Investment Amount
IA_k(t) inside the month     inv_amt_pp_at(t, timing)          BEF_CREDIT, BEF_ROLL,
                                                               BEF_WD, AFT_WD
IA_k, before t = 0           inv_amt_pp_init                   Investment Amount entering
                                                               month 0
FA(t)                        fixed_acct_pp(t)                  Fixed Account value
HA(t)                        holding_acct_pp(t)                Holding Account value
FA, HA before t = 0          fixed_acct_pp_init,               The accounts entering month 0
                             holding_acct_pp_init
i_declared                   acct_rate()                       Declared rate on FA and HA
AV(t)                        av_pp(t), av_pp_at(t, timing)     Account Value
AV, before t = 0             av_pp_init                        Account Value entering month
                                                               0
l(t) x AV(t)                 av_at(t, timing)                  In-force weighted Account
                                                               Value
ROP(t)                       rop_pp(t)                         ROP base at the end of month
                                                               t
ROP, before t = 0            rop_pp_init                       ROP base entering month 0
DB(t)                        death_ben_pp(t)                   Death benefit
CSV(t)                       surr_value_pp(t)                  Cash surrender value
AV_anniv(y)                  free_wd_base(t)                   Account Value at the
                                                               anniversary
AV_anniv(y), before t = 0    av_pp_prev_anniv_init             AV_anniv(y) of the year under
                                                               way, its anniversary before
                                                               the valuation month
0.10 x AV_anniv(y)           free_wd_allow(t)                  Free Withdrawal Amount
FW(t)                        free_wd_avail(t)                  Allowance before the
                                                               withdrawal
FW(t) after the withdrawal   free_wd_remain(t)                 Allowance a surrender can
                                                               shelter
FW, before t = 0             free_wd_remain_init               Allowance unused entering
                                                               month 0
FW_used(y)                   free_wd_avail/free_wd_remain      Consumed amount, as its
                                                               complement
G_total                      wd_pp(t)                          Gross amount removed
G_k                          wd_alloc_pp(t, bucket)            Amount taken from one bucket
(scheduled part of G)        wd_scheduled_pp(t)                Programme's withdrawal in
                                                               month t
(the programme)              wd_amount_pm(m)                   Its withdrawal at policy
                                                               month end m
(the programme's row)        wd_schedule_number()              Its row in Data's array
(behavioural part of G)      wd_behavioral_pp(t)               The anniversary rule's
                                                               withdrawal
(free part of G)             wd_free_pp(t)                     Portion inside the free
                                                               amount
chargeable                   wd_excess_pp(t)                   Amount exposed to the charge
wc(cy)                       surr_charge_rate(t)               Withdrawal charge rate
wc(cy), by year              surr_charge_rate_at(cy)           Its rate in contract year cy
WC(t)                        wd_charge_pp(t)                   Withdrawal charge
net proceeds                 wd_payment_pp(t)                  Cash paid on the withdrawal
chargeable on a surrender    surr_excess_pp(t)                 AV(t) less the free amount
wc x chargeable              surr_charge_pp(t)                 Charge on a full surrender
q_m(t)                       mort_rate_mth(t)                  Monthly mortality rate
(annual q_x)                 mort_rate(t)                      Annual mortality rate
(q_x by age)                 mort_rate_base_at(a)              Table rate at attained age a
(the sex's row)              mort_schedule()                   Its row in Data's array
w_base(y)                    lapse_rate_base(t)                Un-shocked annual surrender
                                                               rate
w_base(y), by year           lapse_rate_base_py(y)             Its rate in contract year y
M_sc(y)                      lapse_rate_sc_mult(t),            Charge-expiry shock
                             lapse_shock_mult                  multiplier and its **[std]**
                                                               size, 3.0
(the shock year)             lapse_shock_year()                First charge-free contract
                                                               year
M_iv(t)                      lapse_iv_mult(t)                  Moneyness suppression
w_annual(y,t)                lapse_rate(t)                     Total annual surrender rate
w_m(t)                       lapse_rate_mth(t)                 Monthly surrender rate
phi                          term_end_lapse_rate(t)            Term-end surrender
                                                               concentration
l(t)                         pols_if(t)                        In force at the start of
                                                               month t
(none)                       policy_count                      Contracts the point stands
                                                               for
l at the valuation date      pols_if_init                      In force at the valuation
                                                               date
(new business)               pols_new_biz(t)                   Contracts issued in month t
l(t+1)                       pols_if_at(t, timing)             BEF_NB, BEF_DECR, BEF_LAPSE,
                                                               BEF_TERM_SURR, AFT_DECR
l(t) q_m                     pols_death(t)                     Deaths
l(t)(1-q_m) w_m + phi        pols_lapse(t)                     Full surrenders
(the phi part)               pols_lapse_term(t)                Term-end concentrated
                                                               surrenders
(none)                       pols_maturity(t)                  Forced annuitizations at
                                                               maturity
P in the issue month         premiums(t)                       Premium income
(premium credited)           prem_to_av_pp(t), prem_to_av(t)   Premium credited to the base
G_total - WC(t)              withdrawals(t)                    Withdrawal payments
(ledger benefit lines)       claims(t, kind)                   Benefit outgo by kind
(per contract)               claim_pp(t, kind)                 Benefit per contract by kind
(from the Account Value)     claims_from_av(t, kind)           Account Value released
(above the Account Value)    claims_over_av(t, kind)           Benefit paid above the AV
(investment return)          inv_income_pp(t), inv_income(t)   Return credited to the AV
(acquisition; maintenance)   expenses(t)                       0.06 P + 200; 60/12 x
                                                               1.025^(t//12)
1.025^(t//12)                inflation_factor(t)               Expense inflation, valuation
                                                               clock
premium tax                  premium_taxes(t)                  Premium tax, 0% [std]
NetCF(t)                     net_cf(t)                         Net cash flow
===========================  ================================  =============================

.. rubric:: Names that needed care

The notes reuse single letters across three different vocabularies — contract mechanics,
Black-Scholes and the deferred annuity chassis — and the collisions are real.

``T`` is the term length in **years** while ``t`` is a **month**, so it becomes
:func:`term_years`; ``tau`` is likewise in years and stays :func:`tau`. ``P`` is both the
single purchase payment and the Black-Scholes put: :func:`premium_pp` against
:func:`bs_put`. ``C`` is the Black-Scholes call, the [S2] fixed-leg symbol for the Market
Value Rate at term start, *and* the surrender charge on the chassis: :func:`bs_call`,
:func:`mvr_at_term_start` and :func:`surr_charge_pp`. ``B`` is the amortized option budget
here and the buffer is ``b``: :func:`budget_amort_pp` against :func:`buffer`. ``R`` is
index performance and ``r`` is the Market Value Rate: :func:`index_perf` against
:func:`mvr`. ``e`` is the Edge Rate, not Euler's number: :func:`edge_rate`.

One collision is worth stating in prose because getting it wrong would be a modelling
error rather than a naming one. On the deferred annuity chassis ``M(t)`` is a **contract**
market value adjustment applied to the surrender benefit. **This product has no such
thing** — the only MVA-like term in the prospectus is the ``[(1+C)/(1+D)]^E`` factor
*inside* the interim value [S2], which is why it is named :func:`mva_factor` (a factor, in
the interim value) and there is no ``mva_pp``, no ``mva_rate`` and no ``mva_cap_rule``
anywhere in this model. The notes' ``M_sc`` and ``M_iv`` are lapse multipliers and are
named :func:`lapse_rate_sc_mult` and :func:`lapse_iv_mult` so they cannot be read as
adjustments either. Nor is there an ``mgsv_pp``: AG 54 displaces Model #805 outright when
it is satisfied [R2][REG-R42][REG-R44], and the nonforfeiture value *is* the interim
value.

.. rubric:: Timing arguments

Investment Amount, ``inv_amt_pp_at(t, timing)``:

``BEF_CREDIT``
    the notional entering month ``t``, which is what the month's valuation applies to. In
    a contract's issue month it is the purchase payment allocated to the option — the
    opening state the Issue Date leaves behind — and in the valuation month of a contract
    in force it is :func:`inv_amt_pp_init`.
``BEF_ROLL``
    after term-end crediting, ``IA(1 + g)`` at a Term End Date and unchanged otherwise.
    This is the worked example's **Investment Amount** column.
``BEF_WD``
    after the renewal / transfer roll split, so ``roll_share(OPTION)`` of
    ``BEF_ROLL`` at a Term End Date and unchanged otherwise.
``AFT_WD``
    after the proportional withdrawal reduction. Equal to :func:`inv_amt_pp`.

Interim Value, ``interim_value_pp_at(t, timing)``, takes the same three of those points —
``BEF_ROLL``, ``BEF_WD``, ``AFT_WD`` — and is in each case the Investment Amount at
that point multiplied by :func:`iv_ratio`. ``BEF_ROLL`` is the worked example's
**Interim value** column.

The currency decomposition of that value — :func:`fixed_proxy_pp`,
:func:`opt_component_pp`, :func:`deriv_proxy_pp`, :func:`trading_cost_pp` and
:func:`budget_amort_pp` — takes two of them, ``BEF_ROLL`` and ``AFT_WD``, through
:func:`iv_notional_pp`; ``RILA_US_S``'s default, ``"BEF_ROLL"``, is no default here, every
caller passing its timing. That pair is what the worked example's rows
B1 and B2 are: the same month, the same market state, the decomposition before and after
an $8,000 withdrawal, every component scaled by one factor.

Account Value, ``av_pp_at(t, timing)``, following ``CashValue_SE``'s ``av_pp_at``:

``BEF_WD``
    ``AV(t)`` as the notes' step 5 leaves it — after crediting, the roll split, the
    interim value and the account accruals, before any transaction. This is the value the
    free-withdrawal base is snapshotted from and the base the withdrawal is allocated
    across.
``AFT_WD``
    after the transaction; equal to :func:`av_pp`, and the value every decrement benefit
    is measured on.

Policy counts, ``pols_if_at(t, timing)``, following ``CashValue_SE``'s ``pols_if_at`` and
``basiclife.BasicTerm_SE``'s ``BEF_NB``:

``BEF_NB``
    the count carried in from month ``t - 1``, before month ``t``'s new business:
    :func:`pols_if_init` at :func:`t_entry`, and the survivors of month ``t - 1`` after it.
``BEF_DECR``
    ``l(t)``, in force at the **start** of month ``t``: ``BEF_NB`` plus the month's new
    business, :func:`pols_new_biz`; equal to :func:`pols_if`.
``BEF_LAPSE``
    after deaths, ``l(t)(1 - q_m(t))``.
``BEF_TERM_SURR``
    after the background monthly surrender, ``l(t)(1 - q_m)(1 - w_m)``.
``AFT_DECR``
    after the discrete term-end surrender fraction ``phi``. This is the count at the month
    **end**, the notes' ``l(t+1)``: :func:`pols_if` carries the start-of-month count, so
    the end-of-month one lives here and nowhere else.

Benefit ``kind`` arguments are ``DEATH``, ``LAPSE`` and ``MATURITY``, and ``ALL`` for the
total of :func:`claims` and :func:`claims_over_av`. Withdrawal allocation ``bucket``
arguments are ``OPTION``, ``FIXED`` and ``HOLDING``. Option ``leg`` arguments are
``ATM_CALL``, ``OTM_CALL``, ``OTM_PUT``, ``ATM_PUT``, ``FLOOR_PUT``, ``STEP_BINARY`` and
``EDGE_BINARY``. Market-state ``mkt`` arguments are ``CURRENT`` and ``TERM_START``, and a
pricing ``basis`` is one of those or ``UPDATED_EXPIRY``. Any other value of any of these
raises ``ValueError``. Each is an int code (*Codes*, below).

There is no ``"ANNUITIZATION"`` kind. The notes give no elective annuitization take-up
for this product; the only annuitization modelled is the **forced** one at the Maturity
Date, which is ``MATURITY``.

.. rubric:: pols_maturity and the Maturity Date

Unlike the deferred annuity chassis, this product's horizon is contractual rather than
chosen: the Maturity Date is the later of the anniversary after the oldest owner's 90th
birthday and ten years from issue [S2], so ``policy_term()`` is
``max(90 - age_at_entry(), 10)`` years and :func:`maturity_mth` is twelve times that, the
policy month cover ends at — 360 on the anchor cell, whose last covered policy month is
359. :func:`proj_len` counts from the valuation date to there,
``maturity_mth() - duration_mth_init()``: 360 months on the anchor cell issued at the
valuation date, the last of them ``t = 359``, and 289 on the anchor in force 71 months.
The Maturity Date is that month's end, where the contract force-annuitizes at the Account
Value, and :func:`pols_maturity` carries the survivors out, so that the roll-forward::

    pols_if(t) - pols_if_at(t + 1, BEF_NB)
        = pols_death(t) + pols_lapse(t) + pols_maturity(t)

closes for every ``t``, including the last — ``pols_if(t)`` opening month ``t`` and
``pols_if_at(t+1, BEF_NB)`` the count carried into the next, which past the Maturity
Date is zero; the next month's new business is no part of month ``t``'s movement. The name
follows ``BasicTerm_S.pols_maturity`` and the construction follows :mod:`.Term_US_S` and
:mod:`.MYGA_US_S`. The payout stream bought at that date is not derived here: it is the
immediate-annuity chassis, restricted to the two forms this contract offers [S2].

.. rubric:: Codes

What :mod:`~.RILA_US_S` spells as text, a timing, a kind, a bucket, a leg, a market, a
scenario column or a pricing rule, is here an int Reference named as the text it
replaces, the column names upper-cased, so that every cell takes and returns C numbers. A
call site reads as it did, less the quotes: ``pols_if_at(t, BEF_DECR)``,
``av_pp_at(t, BEF_WD)``, ``claims(t, DEATH)``, ``market_state(t + 1, RISK_FREE)``.

===============  =====  =============================================================
Reference        Value  Meaning
===============  =====  =============================================================
BEF_NB           0      :func:`pols_if_at`: the count carried in from month t - 1
BEF_DECR         1      :func:`pols_if_at`: that count plus month t's new business
BEF_LAPSE        2      :func:`pols_if_at`: after deaths
BEF_TERM_SURR    3      :func:`pols_if_at`: after the background surrender
AFT_DECR         4      :func:`pols_if_at`: after the term-end fraction, the notes' l(t+1)
BEF_CREDIT       5      :func:`inv_amt_pp_at`: the notional entering month t
BEF_ROLL         6      the Investment Amount, interim value and decomposition cells:
                        after term-end crediting, before the roll split
BEF_WD           7      the value cells: after the roll split, before the withdrawal
AFT_WD           8      the value cells: after the withdrawal
DEATH            0      the claim cells: the death claim
LAPSE            1      the claim cells: the surrender claim
MATURITY         2      the claim cells: the annuitization at the Maturity Date
ALL              3      :func:`claims`, :func:`claims_over_av`: the three kinds' total
CAP              4      :func:`guar_min_rate`: the guaranteed minimum Cap Rate
STEP             5      :func:`guar_min_rate`: the guaranteed minimum Step Rate
EDGE             6      :func:`guar_min_rate`: the guaranteed minimum Edge Rate
OPTION           0      the bucket cells: the index-linked option
FIXED            1      the bucket cells: the Fixed Account
HOLDING          2      the bucket cells: the Holding Account
ATM_CALL         0      the leg cells: the at-the-money call
OTM_CALL         1      the leg cells: the call struck at the cap
OTM_PUT          2      the leg cells: the put struck at the buffer
ATM_PUT          3      the leg cells: the at-the-money put
FLOOR_PUT        4      the leg cells: the put struck at the floor
STEP_BINARY      5      the leg cells: the at-the-money binary call
EDGE_BINARY      6      the leg cells: the binary call struck at the buffer
CURRENT          0      :func:`opt_component`'s ``mkt``, and a basis of
                        :func:`opt_component_at`: the current market, tau(t)
TERM_START       1      the same: the term-start market, at the term T
UPDATED_EXPIRY   2      a basis alone: the term-start market at tau(t)
INDEX_LEVEL      0      :func:`market_state`: the ``index_level`` column
MVR              1      :func:`market_state`: the ``mvr`` column
RISK_FREE        2      :func:`market_state`: the ``risk_free`` column
DIV_YIELD        3      :func:`market_state`: the ``div_yield`` column
IMPL_VOL         4      :func:`market_state`: the ``impl_vol`` column
TERM_END         0      :func:`credit_rate_by`: the term-end rule, accrual 1
PRORATED         1      :func:`credit_rate_by`: the pre-AG 54 rule, accrual 1 - tau/T
===============  =====  =============================================================

The timings are numbered as one family, ``BEF_NB`` 0 and ``BEF_DECR`` 1, as in every SEC
model, then the count's others, then the value cells', each in the order of its instants,
so that a timing of the count passed to a value cell, ``av_pp_at(t, BEF_NB)``, is refused
as any timing the cell does not take is, ``ValueError("invalid timing")``, in both
engines, rather than read as one of its own. The kinds are numbered in ``result_cf``'s
order, the order :mod:`~.RILA_US_S` adds them in its total, then ``ALL``, its
``kind=None``, and the guaranteed minimum's three rate kinds after it, so that a claim
kind passed to :func:`guar_min_rate`, or a rate kind to a claim cell, is refused,
``ValueError("invalid kind")``. The buckets and the legs are numbered in
:mod:`~.RILA_US_S`'s order; the market of :func:`opt_component`, ``mkt``, and the basis of
:func:`opt_component_at` share ``CURRENT`` and ``TERM_START``, which :mod:`~.RILA_US_S`
spells alike. A code a cell takes indexes that cell's cache, a C array of nine codes a
month for each cell that takes a ``t`` and a code, and of seven legs by nine bases or
timings for :func:`opt_component_at` and :func:`opt_component_pp`, since every 2-D cache
of the model has one inner width and every 3-D one one inner shape (``spec_sec.py``): a
code a cell does not take but below 9, or a leg below 7, is refused inside the cache.
Codes are References, not cells, so the symbol map does not list them. Every other
Reference is named in lower case, ``issue_age_min`` and ``issue_age_max`` among them, the
issue ages 0 to 111 the compiled model's caches are sized from (:func:`proj_len`).

.. rubric:: Reporting cells

:func:`model_point`, the label accessors :func:`policy_id`, :func:`sex`,
:func:`crediting_type`, :func:`iv_family`, :func:`amort_rule`, :func:`scenario_id` and
:func:`wd_schedule_id`, the reports :func:`result_cf`, :func:`result_pols`,
:func:`result_av` and :func:`result_iv`, and the checks :func:`check_av_roll_fwd`,
:func:`check_pols_roll_fwd` and :func:`check_term_end_identity` are written for a reader
and for the comparison with :mod:`~.RILA_US_S`, which has every one of them: a table row,
text, DataFrames and three verdicts. No other cell calls them: each reads the number
``Data`` decoded from the same column instead, the decodes' flags and the rows the keys
select. So the row, the text and the frames stay Python when the model compiles. A label
accessor returns its column as read, text or not: ``Data`` accepts, and the model
projects, a point whose ``policy_id`` is blank or a number, which no cell reads, whose
``crediting_type``, ``iv_family`` or ``amort_rule`` is, which its decodes answer False to,
or whose ``scenario_id`` or ``wd_schedule_id`` is a number, where its table's keys are
numbers, and the compiled accessor returns what modelx returns, NaN or an int; ``sex`` is
always ``M`` or ``F``, which the mortality table's check holds. Every other cell returns
a C ``bint``, ``long long`` or ``double``, and so do the three checks, which may stay
Python but compile to a ``bint``, their verdict, as their per-month residuals,
``*_resid``, compile to a ``double``.

.. rubric:: Engine cells

Eleven cells of float parameters compile with C signatures and dict caches, their bodies
Python, ``math`` included: :func:`norm_cdf`, :func:`bs_d1`, :func:`bs_d2`,
:func:`bs_call`, :func:`bs_put`, :func:`bs_binary_call`, :func:`opt_component`,
:func:`opt_portfolio`, :func:`opt_portfolio_abs`, :func:`credit_rate_at` and
:func:`opt_budget_at_cap`, :mod:`~.RILA_US_S`'s own with its strings coded, kept for its
tests, which call :func:`opt_component`, :func:`opt_portfolio`, :func:`credit_rate_at`
and :func:`bs_binary_call` directly, for T1, which compares the keys
:mod:`~.RILA_US_S` caches, some 5,000 a point, and for a reader. No projection cell calls
them, and a cell keyed by a float compiles with a Python dict for a cache, so the registry
admits them by name. The projection prices through their int-keyed forms instead, each
written inline once: :func:`opt_component_at`, a leg on one of three bases, which
:func:`opt_portfolio_at` and :func:`opt_portfolio_abs_at` sum; :func:`credit_rate_by`, the
crediting rate under one of two rules; and :func:`cap_solved_at_start`, the cap solve,
once a term. A module test holds each to its engine cell bit for bit on every committed
point and month, and on two points under ``nge_reset`` that solve a one-year cap fifty
times on a market that steps each year. :mod:`~.RILA_US_S`'s ``opt_legs()``, a tuple of
leg names, which no C type holds, is dropped for :func:`opt_leg_count` and
:func:`opt_leg`, and T1 exempts it.

The two pricing cells, :func:`opt_component_at` and :func:`cap_solved_at_start`, call
``math.log``, ``math.exp``, ``math.sqrt`` and ``math.erf``, Python's own functions, which
the registry admits in those two cells alone by their dotted names (``"python_calls"``),
each wrapped in ``float(...)`` so that every local stays a C double. So a compiled price
is modelx's on every platform, and a ``math`` raise, ``exp``'s ``OverflowError`` among
them, is Python's own in both engines. C's own functions, measured on a prototype under
MSVC, were equal bit for bit and faster, and are not taken
(``products/registered_index_linked_annuity/model-sec.md``, *The compiled model*). Every
other cell calls no ``math``: the uncapped cap's ``+inf`` comes from
``Data.cap_uncapped()`` and ``math.isinf`` from :func:`is_uncapped`; and
:func:`opt_budget_target`, :func:`mva_factor`, :func:`fixed_leg_yield`,
:func:`fixed_proxy_factor` and :func:`inflation_factor` call ``math.log`` only inside the
bound check before a power (*Powers*, below), which the registry admits in each.

.. rubric:: Powers

A ``**`` of two floats is Python's in modelx, which raises where it has no float to give,
and C's ``pow`` compiled, which raises nowhere: a base of 0 under a negative power gives
``inf`` there, a negative base under a fractional power NaN, and a result past the
largest float ``inf``, where Python raises ``ZeroDivisionError``, returns a complex
number, and raises ``OverflowError``. So every power whose base inputs ``Data`` accepts,
or a moved Reference, can take there is guarded before it is taken, the same in both
engines, refusing nothing :mod:`~.RILA_US_S` projects:

* a base of 0 under a negative power raises Python's own ``ZeroDivisionError``, its own
  message, in :func:`opt_budget_target`, :func:`fixed_leg_yield` and
  :func:`fixed_proxy_factor`;
* a base below 0 under a power that is not a whole number, where :mod:`~.RILA_US_S`'s
  ``**`` returns a complex number, which no cell can carry on with, raises ``ValueError``
  naming the point and what took the base there: in :func:`fixed_leg_yield` on a term
  longer than a year, in :func:`fixed_proxy_factor` where the months left in the term are
  not a multiple of 12, in :func:`fixed_acct_pp_at`, :func:`fixed_acct_pp`,
  :func:`holding_acct_pp_at` and :func:`holding_acct_pp`, the accounts' twelfth root, and
  in :func:`lapse_rate_mth`. Under a whole-number power, a negative base computes as
  :mod:`~.RILA_US_S` does, and so does ``-0.0``, and any base under a power of 0 is 1;
* a power past the largest float, which Python's ``**`` refuses with a message of the
  platform's, raises ``OverflowError`` with a message of this model's, naming the point,
  before it is taken: where ``y log|x|`` exceeds ``709.7827128933845``, which is
  ``log`` of the largest float, ``709.782712893384``, and a margin of ``5e-13`` above the
  error of the product, in :func:`opt_budget_target`, :func:`fixed_leg_yield`,
  :func:`mva_factor`, :func:`fixed_proxy_factor` and :func:`inflation_factor`, and where
  a square's base exceeds ``1.3407807929942596e154``, the largest float whose square is a
  float, in :func:`opt_component_at`, :func:`cap_solved_at_start`, :func:`lapse_iv_mult`
  and the engine's :func:`bs_d1`. A base or a power that is not finite, which Python's
  ``**`` answers without a raise, is not checked. The square's bound is exact; the
  logarithm's falls within ``1e-12`` relative of Python's own overflow, and a power
  inside that sliver, which no input reaches but by construction, is refused in both:
  modelx raises Python's ``OverflowError``, with the platform's message, and the
  compiled model raises this model's, after the power, its result past the largest
  float.

Each refuses only where :mod:`~.RILA_US_S` itself raises or returns a complex number, and
``model-sec.md`` records each beside :mod:`~.RILA_US_S`'s own outcome.
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

    Row ``idx`` of the table, as ``Data.model_point_table`` checked it: ``RILA_US_S``'s
    columns, ``pols_if_init`` renamed ``policy_count``, then ``duration_mth`` and the
    thirteen columns of the opening state, and the generator's ``row_kind``,
    ``source_policy_id`` and ``source_mth``, which no formula reads. A reporting cell (the
    Space docstring's *Reporting cells*), for a reader who wants every column at once: no
    projection cell reads it, each accessor reading its own ``Data`` vector instead.
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
    """The issue age (ANB) of the selected model point, from ``Data.age_at_entry``.

    An age of ``2**53`` or more in size, which an int64 cannot be trusted to hold, is
    refused here, naming the point (``Data.age_at_entry_ok``); ``Data`` accepts one only
    where the mortality table rates it.
    """
    if data.age_at_entry_ok()[idx] == 0:                             # noqa: F821
        raise ValueError(f"point_id {point_id()}: age_at_entry must be below 2**53 in "
                         f"size; it is not")
    return int(data.age_at_entry()[idx])                             # noqa: F821


def sex():
    """The sex of the selected model point, M or F.

    A label for reporting, which no projection cell calls: :func:`mort_rate_base_at` reads
    the sex's rates by :func:`mort_schedule`. Text always: the mortality table's check
    admits no sex but ``M`` and ``F``, and ``Data`` no point of a sex it does not rate,
    and the label refuses any other value itself, ``ValueError`` naming the point, so
    that it returns text or raises in either engine.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError(f"point_id {point_id()}: sex must be M or F")
    return v


def mort_schedule():
    """The row of ``Data.mort_rate_array`` the point reads, by its ``sex``.

    The sexes are numbered from 1 in their sorted order, ``F`` 1 and ``M`` 2 as
    shipped, and read by :func:`mort_rate_base_at` and :func:`proj_len`'s
    mortality check, where ``RILA_US_S`` joins on the point's text.
    """
    return int(data.mort_schedule()[idx])                            # noqa: F821


def premium_pp():
    """P: the single purchase payment per contract; no subsequent payments [S1][S2]."""
    return float(data.premium()[idx])                                # noqa: F821


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the contracts in force then, before any
    month-0 event; any other point counts the contracts it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Every per-contract value — the
    Investment Amount, the interim value, the accounts, the allowance, the opening state
    — is the same whatever the count, and every cash flow is a per-contract amount
    weighted by it.
    """
    return float(data.policy_count()[idx])                           # noqa: F821


def pols_if_init():
    """l at the valuation date: the contracts in force then, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose contracts
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count. ``RILA_US_S``'s cell of the name is the notes'
    ``l(0)``, the count at issue; in both models the count at a month's end is
    ``pols_if_at(t, AFT_DECR)``.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The contract's age in months at ``t = 0``: 71 for the anchor cell valued in the last
    month of its first term, 0 for a contract issued at the valuation date, and -13 for
    one to be issued 13 months after it, which ``Data`` admits up to
    ``future_horizon_mth`` months ahead. It is read as ``basiclife.BasicTerm_SE`` reads it,
    as a whole number whatever the column's type, and is the one fact the policy clock
    takes from the model point, from ``Data.duration_mth``; a value of ``2**53`` or more in
    size, which an int64 cannot be trusted to hold, is refused here, naming the point.
    """
    if data.duration_mth_ok()[idx] == 0:                             # noqa: F821
        raise ValueError(f"point_id {point_id()}: duration_mth must be below 2**53 in "
                         f"size; it is not")
    return int(data.duration_mth()[idx])                             # noqa: F821


def term_years():
    """T: the index-linked term in years, from the 1 / 3 / 6 menu [S1][S2].

    Read from ``Data.term_years``, an int64 vector. A term of ``2**53`` or more in size,
    which ``Data`` accepts where *guar_min_rate_table.csv* floors it and an int64 cannot
    be trusted to hold, is refused here, naming the point: ``RILA_US_S`` projects it on
    Python's exact ints, where the compiled term clock, ``12 x term_years`` in C, would
    wrap (``Data.term_years_ok``).
    """
    if data.term_years_ok()[idx] == 0:                               # noqa: F821
        raise ValueError(f"point_id {point_id()}: term_years must be below 2**53 in size; "
                         f"it is not")
    return int(data.term_years()[idx])                               # noqa: F821


def buffer():
    """b: the buffer, guaranteed for the life of each term [S1][S2].

    The buffer absorbs the first ``b`` of index loss and passes the excess through; 10% is
    the one level present in every retrieved insurer's menu [S1]-[S6].
    """
    return float(data.buffer()[idx])                                 # noqa: F821


def crediting_type():
    """``CAP``, ``STEP``, ``EDGE`` or ``FLOOR``.

    The chassis offers Cap, Step and Edge crediting [S2]; ``FLOOR`` is the optional module
    that only one insurer in the sample offers and that needs a **four**-option
    replicating portfolio rather than three [S5].
    """
    return model_point()["crediting_type"]


def declared_cap():
    """c: the declared Cap Rate for the initial term, or blank for an uncapped option.

    100% at 6 years, 55% at 3 and 12% at 1 **[std]** — no current rate sheet was
    retrievable, both insurer rate pages returning HTTP 403. A blank means the option is
    uncapped, in which case the out-of-the-money call is valued at zero [S2].
    """
    return float(data.declared_cap()[idx])                           # noqa: F821


def declared_step():
    """s: the declared Step Rate, 8% **[std]**; observed illustrative 8% [S1]."""
    return float(data.declared_step()[idx])                          # noqa: F821


def declared_edge():
    """e: the declared Edge Rate, 6% **[std]**.

    No Edge value appears in any retrieved document; 6% is set below the 8% Step because
    the Edge design pays down to -b rather than to 0 and so buys a lower rate.
    """
    return float(data.declared_edge()[idx])                          # noqa: F821


def participation():
    """PR: the Participation Rate, 100% [S4].

    At ``PR = 1`` the notes' BUFFER + CAP + PR portfolio collapses **exactly** to the
    BUFFER + CAP one, so a single branch serves both; see :func:`opt_component`.
    """
    return float(data.participation()[idx])                          # noqa: F821


def floor_rate():
    """f: the floor for the ``FLOOR`` crediting module, a positive fraction [S5]."""
    return float(data.floor_rate()[idx])                             # noqa: F821


def iv_family():
    """The interim value algebra: ``portfolio``, ``notional``, ``delta`` or ``legacy``.

    ``portfolio`` **[std]** is family (a), the AG 54-literal Hypothetical Portfolio form
    [S2][R2] and the baseline. ``notional`` is family (b), the full Segment Investment
    discounted at a current investment-grade rate plus an always-positive Cap Calculation
    Factor [S4][S6]. ``delta`` is family (c), a delta applied to the notional with **no
    interest-rate adjustment term at all** [S5]. ``legacy`` is the pre-AG 54 time-prorated
    design [S1], which uses no option pricing; it predates AG 54's July 1, 2024 effective
    date [R2] and is carried as a tractable regression contrast, not as a live design.
    """
    return model_point()["iv_family"]


def amort_rule():
    """``straight_line`` **[std]** [S2] or ``updated_expiry`` [S3].

    How the initial option budget is amortized: ``beta x IA x tau/T`` straight-line to
    term end, or the initial-market-conditions portfolio value re-read at the **updated
    time to expiry**. One insurer needs both, split by state [S3], so this is a
    configuration flag rather than a modelling opinion.
    """
    return model_point()["amort_rule"]


def nge_reset():
    """Whether the declared cap is re-solved at each renewal Term Start Date **[std]**.

    False holds the snapshot scale level, which is the notes' base projection. True
    applies the ASOP No. 2 determination rule in :func:`declared_cap_solved`, floored at
    the contractual guaranteed minimum [S2][R5][REG-R26].
    """
    return bool(data.nge_reset()[idx])                               # noqa: F821


def wd_rate_ann():
    """The behavioural partial-withdrawal rate, 2% of Account Value a year **[std]**.

    Zero in contract year 1 because the free amount is zero there [S1][S2]; thereafter
    taken at each Contract Anniversary and capped at the Free Withdrawal Amount, so the
    base run incurs no withdrawal charge. It is a model point column rather than a
    Reference because the notes' worked example and the notes' behavioural rule are
    mutually inconsistent - see the product's ``model.md``, *The worked example and the
    base withdrawal rule contradict each other*.
    """
    return float(data.wd_rate_ann()[idx])                            # noqa: F821


def scenario_id():
    """The market scenario the model point runs on, a key into *market_scenario_sec.csv*.

    A label for reporting, as read, which no projection cell calls: :func:`market_state`
    reads the scenario by :func:`scenario_number`, the number ``Data`` joins it to. A
    point issued at the valuation date runs on ``RILA_US_S``'s scenario under its own
    id; one restated in force at policy month ``d`` runs on its own copy re-based to that
    month, ``up-M71``, and one issued ``k`` months on on its copy moved ``k`` months
    later, ``up-F13``, which holds no level before the issue month.
    """
    return model_point()["scenario_id"]


def wd_schedule_id():
    """The scheduled withdrawal programme, a key into *withdrawal_table.csv*.

    A label for reporting, as read, which no projection cell calls: :func:`wd_amount_pm`
    reads the programme by :func:`wd_schedule_number`.
    """
    return model_point()["wd_schedule_id"]


def wd_schedule_number():
    """The row of ``Data.wd_amount_array`` the point reads, by its ``wd_schedule_id``.

    Numbered from 1 in the sorted order of the ids, as :func:`scenario_number`
    is, and read by :func:`wd_amount_pm`, the programme's one reader.
    """
    return int(data.wd_schedule_number()[idx])                       # noqa: F821


def scenario_number():
    """The row of ``Data``'s scenario arrays the point reads, by its ``scenario_id``.

    Numbered from 1 in the sorted order of the ids (``Data.scenario_number``), so
    that :func:`market_state` reads the scenario by number where ``RILA_US_S``
    joins on the point's text. :func:`scenario_id`, the label, is a reporting
    cell no projection cell calls.
    """
    return int(data.scenario_number()[idx])                          # noqa: F821


def is_cap_crediting():
    """Whether the option credits by the Cap Rate method, ``crediting_type`` ``CAP``.

    One of the four decodes of ``crediting_type``, each a bool ``Data`` decodes from the
    text element by element, as ``RILA_US_S`` compares it, read where ``RILA_US_S``
    compares the text, so that no projection cell compares the model point's text or
    calls :func:`crediting_type`: :func:`opt_leg_count`, :func:`opt_leg`,
    :func:`opt_component_at`, :func:`credit_rate_by` and the engine cells. A value none of
    the four decodes knows is refused there, with ``RILA_US_S``'s message, where the
    projection meets it.
    """
    return bool(data.is_cap_crediting()[idx])                        # noqa: F821


def is_step_crediting():
    """Whether the option credits by the Step Rate method, ``crediting_type`` ``STEP``."""
    return bool(data.is_step_crediting()[idx])                       # noqa: F821


def is_edge_crediting():
    """Whether the option credits by the Edge Rate method, ``crediting_type`` ``EDGE``."""
    return bool(data.is_edge_crediting()[idx])                       # noqa: F821


def is_floor_crediting():
    """Whether the option credits by the Floor module, ``crediting_type`` ``FLOOR``."""
    return bool(data.is_floor_crediting()[idx])                      # noqa: F821


def is_iv_portfolio():
    """Whether the interim value is family (a), ``iv_family`` ``portfolio`` [S2][R2].

    One of the four decodes of ``iv_family``, a bool ``Data`` decodes from the text, read
    where ``RILA_US_S`` compares the text: :func:`fixed_proxy_factor`,
    :func:`deriv_proxy_factor`, :func:`trading_cost_factor`, :func:`cap_calc_factor` and
    :func:`iv_factor`. A value none of the four knows is refused in
    :func:`fixed_proxy_factor`, with ``RILA_US_S``'s message.
    """
    return bool(data.is_iv_portfolio()[idx])                         # noqa: F821


def is_iv_notional():
    """Whether the interim value is family (b), ``iv_family`` ``notional`` [S4][S6]."""
    return bool(data.is_iv_notional()[idx])                          # noqa: F821


def is_iv_delta():
    """Whether the interim value is family (c), ``iv_family`` ``delta`` [S5]."""
    return bool(data.is_iv_delta()[idx])                             # noqa: F821


def is_iv_legacy():
    """Whether the interim value is the pre-AG 54 design, ``iv_family`` ``legacy`` [S1]."""
    return bool(data.is_iv_legacy()[idx])                            # noqa: F821


def is_straight_line():
    """Whether the option budget amortizes straight-line, ``amort_rule`` ``straight_line``.

    One of the two decodes of ``amort_rule``, a bool ``Data`` decodes from the text, read
    where ``RILA_US_S`` compares the text, in :func:`budget_amort_factor`, which refuses a
    value neither knows with ``RILA_US_S``'s message.
    """
    return bool(data.is_straight_line()[idx])                        # noqa: F821


def is_updated_expiry():
    """Whether the budget is re-read at the updated expiry, ``updated_expiry`` [S3]."""
    return bool(data.is_updated_expiry()[idx])                       # noqa: F821


def inv_amt_pp_init():
    """IA_k entering month 0: the Investment Amount per contract at the valuation date.

    What ``RILA_US_S`` carries into the valuation month: the notional the month's
    crediting and interim value apply to, after every term-end credit, roll split and
    proportional withdrawal reduction before it. It is also the crediting basis, so no
    second basis column is needed. Read at :func:`t_entry` on a contract in force, by
    :func:`inv_amt_basis_pp` and :func:`inv_amt_pp`; 0 on a point issued at or after the
    valuation date, which opens with its purchase payment in its issue month.
    """
    return float(data.inv_amt_pp_init()[idx])                        # noqa: F821


def fixed_acct_pp_init():
    """FA entering month 0: the Fixed Account value per contract at the valuation date.

    Read at :func:`t_entry` on a contract in force, by :func:`fixed_acct_pp_at` and
    :func:`fixed_acct_pp`; 0 before the first Term End Date, since only a term end
    transfers to the account, and on a point not yet in force.
    """
    return float(data.fixed_acct_pp_init()[idx])                     # noqa: F821


def holding_acct_pp_init():
    """HA entering month 0: the Holding Account value per contract at the valuation date.

    Read at :func:`t_entry` on a contract in force, by :func:`holding_acct_pp_at` and
    :func:`holding_acct_pp`; 0 before the first Term End Date and on a point not yet in
    force, as :func:`fixed_acct_pp_init` is.
    """
    return float(data.holding_acct_pp_init()[idx])                   # noqa: F821


def av_pp_init():
    """AV entering month 0: the Account Value per contract at the valuation date.

    The close of the month before the valuation month, after its withdrawal: the opening
    from which :func:`inv_income_pp` measures month 0's investment return and
    :func:`av_change` the block's movement. Of either sign: the interim value can be
    negative under the contract [S2]. 0 on a point not yet in force.
    """
    return float(data.av_pp_init()[idx])                             # noqa: F821


def av_pp_prev_anniv_init():
    """AV_anniv(y) of the contract year under way: its base at the valuation date.

    The Account Value **before** withdrawals at the Contract Anniversary on or before the
    valuation date, ``av_pp_at(12 cy - 1, BEF_WD)`` in ``RILA_US_S``, which
    :func:`free_wd_base` reads where that anniversary month precedes :func:`t_entry`: the
    Free Withdrawal Amount of the year under way is ``free_wd_rate`` times it. The
    purchase payment in the first contract year, which opened at issue; 0 on a point not
    yet in force. Where the anniversary month is in the frame, the valuation month being
    the last of its contract year, the projection reads the frame instead.
    """
    return float(data.av_pp_prev_anniv_init()[idx])                  # noqa: F821


def free_wd_remain_init():
    """FW entering month 0: the Free Withdrawal Amount still unused in the contract year.

    ``RILA_US_S``'s ``free_wd_remain`` of the month before the valuation month, which
    :func:`free_wd_avail` carries from :func:`t_entry` until the next anniversary resets
    it. An allowance's remainder, not an accumulator, so it takes no ``_ytd``. 0 in the
    first contract year, which has no free amount, and on a point not yet in force;
    :func:`proj_len` holds it to the year's allowance.
    """
    return float(data.free_wd_remain_init()[idx])                    # noqa: F821


def rop_pp_init():
    """ROP entering month 0: the return-of-premium death benefit base at the valuation date.

    The purchase payment reduced proportionally by every withdrawal before the valuation
    month, read at :func:`t_entry` on a contract in force by :func:`rop_pp`; at most the
    purchase payment, and 0 on a point not yet in force.
    """
    return float(data.rop_pp_init()[idx])                            # noqa: F821


def index_at_term_start_init():
    """I_s of a term begun before the valuation month: its Term Start Date index level.

    A fact frozen at a past date, which no scenario re-based to the valuation date holds,
    so :func:`index_at_term_start` reads it from the model point wherever the term in
    force began before :func:`t_entry`. Given exactly there, and blank on every other
    point, where the term in force starts at or after the valuation month and its index
    is the scenario's; ``Data`` holds it above 0, since :func:`index_perf` divides by it.
    A blank column reads as NaN here, and no cell reads it.
    """
    return float(data.index_at_term_start_init()[idx])               # noqa: F821


def mvr_at_term_start_init():
    """r_0 of a term begun before the valuation month: its Term Start Date MVR.

    Read by :func:`mvr_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above -1.
    """
    return float(data.mvr_at_term_start_init()[idx])                 # noqa: F821


def risk_free_at_term_start_init():
    """The risk-free rate on the Term Start Date of a term begun before ``t = 0``.

    One of the three option-pricing inputs fixed at the term's start, read by
    :func:`risk_free_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above -1. The budget, the amortized budget and the
    cap solve price under it.
    """
    return float(data.risk_free_at_term_start_init()[idx])           # noqa: F821


def div_yield_at_term_start_init():
    """The dividend yield on the Term Start Date of a term begun before ``t = 0``.

    Read by :func:`div_yield_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above -1.
    """
    return float(data.div_yield_at_term_start_init()[idx])           # noqa: F821


def impl_vol_at_term_start_init():
    """The implied volatility on the Term Start Date of a term begun before ``t = 0``.

    Read by :func:`impl_vol_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above 0.
    """
    return float(data.impl_vol_at_term_start_init()[idx])            # noqa: F821


def cap_rate_init():
    """c of a term begun at a renewal under ``nge_reset`` before the valuation month.

    The cap :func:`declared_cap_solved` re-solved at that renewal's Term Start Date and
    :func:`cap_rate` floored at the guaranteed minimum: a contractual fact fixed then,
    from the market and the References of that date, which a sensitivity run that changes
    ``earned_rate``, ``nge_spread`` or the market at the valuation date must not move.
    :func:`cap_rate` reads it for the rest of that term. Given exactly on a capped Cap
    Rate option under ``nge_reset`` whose term in force began at a renewal before the
    valuation month, and blank everywhere else: off ``nge_reset``, and in the initial
    term, the cap is the model point's declared cap, and a renewal at or after the
    valuation month re-solves from the scenario. ``Data`` holds it at or above the term's
    guaranteed minimum cap.
    """
    return float(data.cap_rate_init()[idx])                          # noqa: F821


def is_uncapped():
    """True when the model point leaves ``declared_cap`` blank [S2].

    ``Data.is_uncapped``, 1 where the column is blank, decoded once in ``Data`` where
    ``RILA_US_S`` asks ``pd.isna`` of the model point (R8). It is also where
    ``RILA_US_S``'s ``math.isinf(cap)`` is asked in the cells that compile:
    :func:`cap_rate` returns ``+inf`` exactly for an uncapped option, ``Data`` holding
    every declared cap, re-solved cap and floor finite.
    """
    return bool(data.is_uncapped()[idx])                             # noqa: F821


def policy_term():
    """Years from issue to the Maturity Date [S2].

    The later of the anniversary after the oldest owner's 90th birthday and ten years from
    issue, read on the ANB attained age **[std]**: 30 years at issue age 60, 10 at 80 or
    above.
    """
    return max(maturity_age - age_at_entry(), maturity_min_years)    # noqa: F821


def maturity_mth():
    """The policy month at which cover ends: ``12 * policy_term()``.

    The Maturity Date closes policy month ``maturity_mth() - 1``, so this is the
    ``duration_mth`` of the first month not covered: 360 at issue age 60, 120 at 80 or
    above. It is ``RILA_US_S``'s frame length, counted from issue on the policy clock;
    :func:`proj_len` counts from the valuation date instead.
    """
    return 12 * policy_term()


def proj_len():
    """The number of months from the valuation date to the Maturity Date.

    ``maturity_mth() - duration_mth_init()``: 360 for the anchor cell issued at ``t = 0``,
    289 for it in force 71 months, 1 for the notional family in its last covered month,
    and 373 for the anchor issued 13 months after the valuation date. The frame is
    ``t = 0, 1, ..., proj_len() - 1``; ``proj_len()`` is its exclusive end and the row
    count of :func:`result_cf`, and ``proj_len() - 1`` is the last covered month, the one
    ending on the Maturity Date.

    The checks run first, in turn, each raising ``ValueError`` naming the point, so that
    both engines refuse a point with one message before any frame is read. First the
    contract the compiled model's caches are sized from (``spec_sec.py``), through two
    References, the issue ages ``RILA_US_S`` projects:

    * an issue age below ``issue_age_min``, 0, which ``Data`` refuses too, is refused;
    * an issue age above ``issue_age_max``, 111, is refused: the oldest issue age
      ``RILA_US_S`` projects on the shipped tables, whose last age, 120, its ten-year
      minimum cover reaches from 111. ``RILA_US_S`` raises on 112. The product's own issue
      ages, 0 to 85, bound nothing ``RILA_US_S`` refuses, so the caches hold 86 to 111
      too.

    Then three rules of the product, which need ``Projection`` References or the
    mortality table that ``Data`` does not join on the cover:

    * a point at or past its Maturity Date at the valuation date has no frame, and is
      refused rather than projecting nothing: an in-force extract should not carry it;
    * the mortality table rates the point's sex to the age its last covered year is
      entered at, ``age_at_entry() + policy_term() - 1``, and the compiled model holds
      that age, ``Data.mort_age_held()``, ``Data.read_last_age``: ``RILA_US_S`` raises
      pandas' ``KeyError`` where it first reads a missing age, so a table short of the
      cover is refused here instead, naming the last age the table rates; a table past
      ``read_last_age`` rates more than the caches hold, and only a moved
      ``issue_age_max`` reaches it;
    * from the second contract year, ``duration_mth_init()`` 12 or more, the Free
      Withdrawal Amount still unused, :func:`free_wd_remain_init`, is at most the year's,
      ``free_wd_rate`` times :func:`av_pp_prev_anniv_init`, to a cent, the year's
      withdrawals only ever reducing it. The rule holds where that base is 0 or more, and
      is not applied below 0: on a negative base ``RILA_US_S``'s allowance is negative,
      and a behavioural rate above ``free_wd_rate`` then takes a withdrawal more negative
      still, which leaves a positive remainder that no allowance bounds. That is a state
      ``RILA_US_S`` reaches, on a negative interim value [S2], so it is accepted.
    """
    if age_at_entry() < issue_age_min:                               # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: age_at_entry {age_at_entry()} is below "
            f"issue_age_min, {issue_age_min}")                       # noqa: F821
    if age_at_entry() > issue_age_max:                               # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: age_at_entry {age_at_entry()} is above "
            f"issue_age_max, {issue_age_max}, the oldest issue age the compiled model "
            f"holds")
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id()}: duration_mth {duration_mth_init()} is at or past the "
            f"maturity date, policy month {maturity_mth()}; the contract has matured")
    s = mort_schedule()
    last = age_at_entry() + policy_term() - 1
    if last > data.mort_age_lasts()[s]:                              # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: the mortality table rates its sex to age "
            f"{data.mort_age_lasts()[s]}, short of age {last}, at which its last "  # noqa
            f"covered year is entered")
    if last > data.mort_age_held():                                  # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: its last covered year is entered at age {last}, "
            f"past read_last_age, {data.mort_age_held()}, the oldest age the compiled "
            f"model holds")
    if duration_mth_init() >= 12 and av_pp_prev_anniv_init() >= 0.0:
        allowance = free_wd_rate * av_pp_prev_anniv_init()           # noqa: F821
        if free_wd_remain_init() > allowance + 0.01:
            raise ValueError(
                f"point_id {point_id()}: free_wd_remain_init {free_wd_remain_init()} is "
                f"more than the contract year's free withdrawal amount, free_wd_rate x "
                f"av_pp_prev_anniv_init, {allowance:.2f}")
    return n


def duration_mth(t):
    """Policy months elapsed at the **start** of month t: the policy clock.

    ``duration_mth_init() + t``, a closed form: 71 at ``t = 0`` for the anchor cell in
    force 71 months, 0 at ``t = 0`` for a contract issued at the valuation date, and 0 at
    ``t = 13`` for one issued 13 months later, negative before that. It is
    ``RILA_US_S``'s ``t``, and every contractual date is read on it: the terms, the
    anniversaries, the withdrawal charge, the attained age, the withdrawal programme and
    the Maturity Date. Defined in every month, before issue too.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later. It is the base of every recursion: :func:`pols_if_at` opens there
    from :func:`pols_if_init`, the Investment Amount, the two accounts, the
    return-of-premium base and the free-withdrawal carry from the model point's opening
    state, and the Account Value's movement from :func:`av_pp_init`. No cell in cover
    reads a month before it, and a term or an anniversary that falls before it is read
    from the opening state.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and not yet past the Maturity Date.

    ``0 <= duration_mth(t) < maturity_mth()``. False before issue and from the month after
    the one ending on the Maturity Date. Outside cover every count is zero, and so every
    cash flow; so is every value, rate and interim-value factor, but for the two surrender
    multipliers, which are 1.0, their neutral value; every flag is false, no market path
    is read, and no table is read at a contract year or an attained age the contract does
    not have.
    """
    return 0 <= duration_mth(t) < maturity_mth()


def duration(t):
    """cy(t): complete contract years elapsed at the start of month t, on the policy clock.

    lifelib's 0-based duration, ``duration_mth(t) // 12``: it is ``0`` through the whole
    of contract year 1, policy months 0 to 11, and steps to 1 at policy month 12. It is
    the *interval* reading of the contract year - the year the whole of month ``t`` lies
    inside - and so is the right one for a rate applied across the month: the attained age
    behind ``q_m(t)`` (:func:`age`). For a transaction settling at the month **end**, one
    instant later, use :func:`duration_eom`; the two differ only in the month that closes
    on an anniversary. Before issue it is negative, which is why no cell calls it outside
    cover. Expense inflation runs on the valuation clock instead (:func:`inflation_factor`).
    """
    return duration_mth(t) // 12


def duration_eom(t):
    """Complete contract years at the month **end** that closes month t.

    ``(duration_mth(t) + 1) // 12``, the *instant* reading, and the notes' own ``cy`` at
    that instant. Month ``t`` ends at time ``t + 1``, so the month ending on the first
    anniversary is policy month 11 and ``duration_eom`` is 1 there where :func:`duration`
    is 0. Anything settled at that instant takes this reading - the withdrawal charge a
    transaction bears (:func:`surr_charge_rate`), the free-withdrawal base snapshotted at
    the anniversary (:func:`free_wd_base`), and the surrender behaviour keyed to that
    charge (:func:`policy_year`, :func:`lapse_rate_sc_mult`), which must see the charge
    expire in the same month the contract does. No cell calls it outside cover.
    """
    return (duration_mth(t) + 1) // 12


def policy_year(t):
    """The contract year in force at the month end that closes month t, ``cy_end + 1``.

    A contractual, 1-based label on the policy clock, and the key the surrender table is
    read on. It takes the **month-end** reading ``duration_eom(t) + 1``, not the interval
    reading ``duration(t) + 1``, because the charge-expiry shock must land in the same
    month the charge a surrender settling there bears goes to zero, which is
    :func:`surr_charge_rate` on that same reading. So at policy month 11 it is 2: a
    surrender at the first anniversary already settles on the year-2 side of the
    schedule, while the mortality rate charged **over** that month is still contract year
    1's. Before issue it is 0 or below, so every call is guarded by :func:`is_active`.
    """
    return duration_eom(t) + 1


def age(t):
    """The attained age (ANB) during month t, ``x + duration(t)``, on the policy clock.

    Keyed on :func:`duration`, not :func:`duration_eom`: ``q_m(t) = 1 - (1 - q_x)^(1/12)``
    is an exposure rate for the whole of month ``t``, so all twelve months of contract
    year 1 - policy month 11, which ends on the anniversary, included - are charged at
    ``q_x`` and the attained age steps at the anniversary rather than one month before
    it. At the Maturity Date the attained age is therefore ``age(proj_len() - 1) + 1``, the
    age the contract's own rule names. Before issue it is below the issue age, so every
    call is guarded by :func:`is_active`.
    """
    return age_at_entry() + duration(t)


def is_anniv(t):
    """True when month t **ends** on a Contract Anniversary, on the policy clock.

    ``(duration_mth(t) + 1) % 12 == 0``. Month ``t`` ends at time ``t + 1``, so the first
    anniversary closes policy month 11.
    The Issue Date is not flagged: it opens policy month 0 rather than ending a month, and
    nothing the model does at an anniversary - the free-withdrawal reset, the behavioural
    withdrawal - happens there. False outside cover, where a month before issue can end on
    a multiple of 12 policy months short of it.
    """
    if not is_active(t):
        return False
    return (duration_mth(t) + 1) % 12 == 0


def term_elapsed_mth(t):
    """Months elapsed in the term of the option **in force during** month t.

    Counted at the month end on the policy clock, ``duration_mth(t) % (12T) + 1``: ``1``
    in the first month of a term and ``12T`` in the month that ends on a Term End Date -
    the expiring option, not the renewed one. Terms align with issue, so the term clock
    follows from the policy clock alone. Reading the boundary month as belonging to the
    term that is closing is what makes the term-end identity work: the replicating
    portfolio at ``tau = 0`` collapses to intrinsic value and reproduces ``g`` exactly.
    Defined in every month, but it means nothing outside cover, where no cell calls it.
    """
    return (duration_mth(t) % (12 * term_years())) + 1


def term_start_month(t):
    """The first month of the term in force during month t, as a **policy** month.

    Equivalently the Term Start Date itself as a time in policy months, since policy month
    ``m`` opens at time ``m``: ``0`` for the initial term, ``12T`` for the first renewal.
    It stays a policy month on either clock: the readers of the term-start market,
    :func:`index_at_term_start`, :func:`mvr_at_term_start` and the three option-pricing
    ones, turn it into a month from the valuation date once each, and read the opening
    state where it precedes the valuation month; :func:`cap_rate` compares it with 0 to
    find a renewal. Defined in every month, but no cell calls it outside cover.
    """
    return duration_mth(t) + 1 - term_elapsed_mth(t)


def tau(t):
    """tau_k(t): years remaining in the option's term at the end of month t.

    ``(12T - elapsed) / 12``. The notes define it as days remaining / 365 [S2]; on a
    monthly grid that is exact twelfths. ``tau(t) = 0`` at every Term End Date, and the
    term opens at ``tau = T`` - an instant, the opening of the term's first month, not a
    projected month. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return (12 * term_years() - term_elapsed_mth(t)) / 12.0


def is_term_end(t):
    """True when month t ends on a Term End Date, i.e. ``tau(t) == 0``.

    False outside cover.
    """
    if not is_active(t):
        return False
    return term_elapsed_mth(t) == 12 * term_years()


def market_state(t, name):
    """The model point's market scenario at time ``t``: field ``name``, a code.

    ``t`` is a **time** in months from the **valuation date**, ``t = 0`` at the valuation
    date, not the month index: the market state month ``t`` is valued at is
    ``market_state(t + 1, ...)``, and a term that starts at or after the valuation month
    reads the state locked on its Term Start Date at that date's time. Each row of
    *market_scenario_sec.csv* is keyed by that same ``month_end`` and states the market
    state that holds from it until the next row of the same scenario, so a flat path is
    one row. The index path is therefore piecewise constant between the scenario's own
    anchor months; that is a property of the deterministic scenario, not of the model.

    ``name`` is a code, ``INDEX_LEVEL``, ``MVR``, ``RISK_FREE``, ``DIV_YIELD`` or
    ``IMPL_VOL``, each named as the scenario's column upper-cased, and any other is
    refused, ``ValueError("invalid name")``. ``Data`` holds each column step-filled by
    valuation month, ``[scenario, t]`` (``Data.index_level_array`` and the four beside
    it), and the point reads row :func:`scenario_number`, where ``RILA_US_S`` takes the
    ``max`` of a list of the months at or before ``t`` on every call.

    On the valuation clock, which every point of a block shares. ``RILA_US_S`` keys the
    same lookup by policy month from issue, the valuation clock of a contract issued at
    the valuation date, and names its parameter ``k``; it is ``t`` here, a month on the
    valuation clock. A copy re-based to a later issue month holds no level before it, so
    a read there is refused, naming the point and the month, where ``RILA_US_S``'s
    ``max()`` of an empty list raised; so is a read past ``Data.scenario_last_mth()``,
    ``Data.read_last_mth``, the last month the arrays hold. No cell reads either in cover.
    """
    s = scenario_number()
    if t < data.scenario_first_mths()[s] or t > data.scenario_last_mth():  # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: its market scenario holds no level at month {t}")
    if name == INDEX_LEVEL:                                          # noqa: F821
        return float(data.index_level_array()[s, t])                 # noqa: F821
    elif name == MVR:                                                # noqa: F821
        return float(data.mvr_array()[s, t])                         # noqa: F821
    elif name == RISK_FREE:                                          # noqa: F821
        return float(data.risk_free_array()[s, t])                   # noqa: F821
    elif name == DIV_YIELD:                                          # noqa: F821
        return float(data.div_yield_array()[s, t])                   # noqa: F821
    elif name == IMPL_VOL:                                           # noqa: F821
        return float(data.impl_vol_array()[s, t])                    # noqa: F821
    else:
        raise ValueError("invalid name")


def index_level(t):
    """I(t): the index level month t is valued at - its month end - price return [S1][S2].

    ``market_state(t + 1, INDEX_LEVEL)``, on the valuation clock. All representative
    indices are **price return**, which is why the dividend yield is a live pricing input:
    omitting it overprices every call in the portfolio. No cell calls it outside cover:
    before issue a future point's scenario holds no level.
    """
    return market_state(t + 1, INDEX_LEVEL)


def index_at_term_start(t):
    """I_s: the index level at the Term Start Date of the term in force during month t.

    The Term Start Date is the policy month :func:`term_start_month`, which is month
    ``term_start_month(t) - duration_mth_init()`` from the valuation date. Where that is
    :func:`t_entry` or later the term starts in the frame, and its index is the scenario's
    there, as in ``RILA_US_S``; where it is earlier the term began before the valuation
    month, and its index is the model point's :func:`index_at_term_start_init`, a level no
    scenario re-based to the valuation date holds. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return index_at_term_start_init()
    return market_state(k, INDEX_LEVEL)


def mvr(t):
    """r(t): the Market Value Rate at month t's month end, annual effective [S2].

    The Constant Maturity Treasury yield at the term's maturity, linearly interpolated
    between adjacent CMT maturities [S2]; the model takes it as an exogenous scalar series
    **[std]** rather than carrying a curve. ``market_state(t + 1, MVR)``, on the
    valuation clock; no cell calls it outside cover.
    """
    return market_state(t + 1, MVR)


def mvr_at_term_start(t):
    """r_0: the Market Value Rate on the Term Start Date [S2].

    Read as :func:`index_at_term_start` reads the index: the scenario's at the Term Start
    Date where that date is in the frame, the model point's
    :func:`mvr_at_term_start_init` where it precedes the valuation month. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return mvr_at_term_start_init()
    return market_state(k, MVR)


def risk_free_at_term_start(t):
    """The risk-free rate on the Term Start Date of the term in force during month t.

    The option budget, the ``updated_expiry`` amortization and the cap solve price under
    the market of the Term Start Date, which ``RILA_US_S`` reads from its scenario at
    :func:`term_start_month` in place, in :func:`opt_component` and
    :func:`opt_budget_at_cap`. Here it is read as :func:`index_at_term_start` reads the
    index: the scenario's at that date where it is in the frame, the model point's
    :func:`risk_free_at_term_start_init` where it precedes the valuation month. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return risk_free_at_term_start_init()
    return market_state(k, RISK_FREE)


def div_yield_at_term_start(t):
    """The dividend yield on the Term Start Date of the term in force during month t.

    Read as :func:`risk_free_at_term_start` reads the rate, from
    :func:`div_yield_at_term_start_init` where the term began before the valuation month.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return div_yield_at_term_start_init()
    return market_state(k, DIV_YIELD)


def impl_vol_at_term_start(t):
    """The implied volatility on the Term Start Date of the term in force during month t.

    Read as :func:`risk_free_at_term_start` reads the rate, from
    :func:`impl_vol_at_term_start_init` where the term began before the valuation month.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return impl_vol_at_term_start_init()
    return market_state(k, IMPL_VOL)


def risk_free(t):
    """The risk-free rate at month t's month end, annual effective, 4.00% **[std]**.

    ``market_state(t + 1, RISK_FREE)``, on the valuation clock; no cell calls it outside
    cover.
    """
    return market_state(t + 1, RISK_FREE)


def div_yield(t):
    """q: the dividend yield at month t's month end, annual effective, 2.00% **[std]**.

    A live pricing input because every representative index is price return [S1][S2].
    ``market_state(t + 1, DIV_YIELD)``, on the valuation clock; no cell calls it outside
    cover.
    """
    return market_state(t + 1, DIV_YIELD)


def impl_vol(t):
    """sigma: the implied volatility at month t's month end, 20.00% flat **[std]**.

    A flat surface is the largest single simplification in this model. AG 54 requires
    assumptions "consistent with the observable market prices of derivative assets over
    the Index Strategy Term, whenever possible" [R2], and a production implementation must
    supply a surface interpolated in both maturity and moneyness [S4]; that is a change to
    *market_scenario_sec.csv* plus a lookup, not to any formula here.
    ``market_state(t + 1, IMPL_VOL)``, on the valuation clock; no cell calls it outside
    cover.
    """
    return market_state(t + 1, IMPL_VOL)


def index_perf(t):
    """R_k(t): index performance to date, ``I(t) / I_s - 1``.

    At a Term End Date this is the crediting input; the cap applies to the **whole-term**
    return, never annually on a 3 or 6 year term [S5]. ``I_s`` is the model point's for a
    term begun before the valuation month (:func:`index_at_term_start`), held above 0 by
    ``Data``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return index_level(t) / index_at_term_start(t) - 1.0


def norm_cdf(x):
    """N(x): the standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))                # noqa: F821


def bs_d1(spot, strike, tau_, rate, divy, vol):
    """Black-Scholes d1.

    ``[ln(I/K) + (r_cc - q_cc + sigma^2/2) tau] / (sigma sqrt(tau))``. ``rate`` and
    ``divy`` are **annual effective** and are converted to continuous compounding here, so
    the 4.00% and 2.00% market inputs enter as ``ln 1.04 = 3.9221%`` and
    ``ln 1.02 = 1.9803%`` exactly as the notes state.

    An engine cell, ``RILA_US_S``'s formula: :func:`opt_component_at` and
    :func:`cap_solved_at_start` price inline what the projection reads. A volatility whose
    square is past the largest float, above about ``1.34e154``, is refused before it is
    squared, ``OverflowError`` naming the point, where Python's ``**`` raises its own
    and the compiled power would return ``inf``.
    """
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    moneyness = math.log(spot / strike)                              # noqa: F821
    if 1.3407807929942596e154 < abs(vol) <= 1.7976931348623157e308:
        raise OverflowError(
            f"point_id {point_id()}: bs_d1, the volatility {vol!r} squared, is past the "
            f"largest float")
    return ((moneyness + (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_)
            / (vol * math.sqrt(tau_)))                               # noqa: F821


def bs_d2(spot, strike, tau_, rate, divy, vol):
    """Black-Scholes d2, ``d1 - sigma sqrt(tau)``."""
    return (bs_d1(spot, strike, tau_, rate, divy, vol)
            - vol * math.sqrt(tau_))                                 # noqa: F821


def bs_call(spot, strike, tau_, rate, divy, vol):
    """C(I, K, tau): the European call, ``I e^(-q tau) N(d1) - K e^(-r tau) N(d2)``.

    At ``tau = 0`` it returns the intrinsic value ``max(I - K, 0)``, which is what makes
    the replicating portfolio collapse to the crediting rate at term end.
    """
    if tau_ <= 0.0:
        return max(spot - strike, 0.0)
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    d_1 = bs_d1(spot, strike, tau_, rate, divy, vol)
    d_2 = bs_d2(spot, strike, tau_, rate, divy, vol)
    return (spot * math.exp(-divy_cc * tau_) * norm_cdf(d_1)         # noqa: F821
            - strike * math.exp(-rate_cc * tau_) * norm_cdf(d_2))    # noqa: F821


def bs_put(spot, strike, tau_, rate, divy, vol):
    """P(I, K, tau): the European put, ``K e^(-r tau) N(-d2) - I e^(-q tau) N(-d1)``.

    At ``tau = 0`` it returns the intrinsic value ``max(K - I, 0)``.
    """
    if tau_ <= 0.0:
        return max(strike - spot, 0.0)
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    d_1 = bs_d1(spot, strike, tau_, rate, divy, vol)
    d_2 = bs_d2(spot, strike, tau_, rate, divy, vol)
    return (strike * math.exp(-rate_cc * tau_) * norm_cdf(-d_2)      # noqa: F821
            - spot * math.exp(-divy_cc * tau_) * norm_cdf(-d_1))     # noqa: F821


def bs_binary_call(spot, strike, tau_, rate, divy, vol):
    """BC(I, K, tau): the cash-or-nothing binary call paying 1, ``e^(-r tau) N(d2)``.

    At ``tau = 0`` it pays 1 when ``I >= K`` and 0 below. That discontinuity is
    contractual, not an artifact: a Step design pays the full step at ``R = 0.00%`` and
    zero at ``R = -0.01%`` [S4], and the binary option is what makes the interim value
    track it. Do not smooth it.
    """
    if tau_ <= 0.0:
        return 1.0 if spot >= strike else 0.0
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    return (math.exp(-rate_cc * tau_)                                # noqa: F821
            * norm_cdf(bs_d2(spot, strike, tau_, rate, divy, vol)))


def guar_min_rate(kind):
    """The contractual minimum declared rate for the model point's term [S1][S2].

    2% / 6% / 8% for the Cap at 1 / 3 / 6 years and 2% for the Step and the Edge. These
    are **guaranteed elements** in ASOP No. 2 terms, so every renewal-rate assumption is
    floored here [R5][REG-R26]; the floor mechanically raises the option budget and
    compresses the spread, which is why the table is a genuine tail exposure. ``kind`` is
    a code, ``CAP``, ``STEP`` or ``EDGE``, numbered after the claim kinds so that a claim
    kind passed here is refused as any other code is, ``ValueError("invalid kind")``.
    ``Data`` joins each point's term with the table by value once, after its count's
    checks, into three vectors, ``Data.guar_min_cap`` and the two beside it, and refuses a
    point whose term the table lacks.
    """
    if kind == CAP:                                                  # noqa: F821
        return float(data.guar_min_cap()[idx])                       # noqa: F821
    elif kind == STEP:                                               # noqa: F821
        return float(data.guar_min_step()[idx])                      # noqa: F821
    elif kind == EDGE:                                               # noqa: F821
        return float(data.guar_min_edge()[idx])                      # noqa: F821
    else:
        raise ValueError("invalid kind")


def opt_budget_target():
    """beta_target(T) = ``1 - (1 + y_e - spread)^(-T)``: the NGE cap-solve target **[std]**.

    ``y_e`` is the projected earned rate on supporting assets and ``spread`` the target
    margin, **[std]** 2.22% - the level implied by the snapshot 6-year cap, which opens
    its fixed leg at an equivalent accretion yield of 1.7834% against a 4.00% market rate.

    The power's exponent is a whole number, so any base but 0 is real. A base of 0,
    ``earned_rate - nge_spread`` at -1, raises Python's own ``ZeroDivisionError`` in both
    engines, and a power past the largest float, which a base near 0 and a long term
    reach, is refused, ``OverflowError`` naming the point (the Space docstring's
    *Powers*): compiled, the power is C's, which raises neither.
    """
    b = 1.0 + earned_rate - nge_spread                               # noqa: F821
    e = -term_years()
    if b == 0.0:
        raise ZeroDivisionError("0.0 cannot be raised to a negative power")
    if (e != 0.0 and b != 0.0 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308
            and not (0.01 < abs(b) < 100.0 and abs(e) < 150.0)
            and e * float(math.log(abs(b))) > 709.7827128933845):    # noqa: F821
        raise OverflowError(
            f"point_id {point_id()}: opt_budget_target(): {b!r} ** {e!r} is past "
            f"the largest float")
    p = b ** e
    if (abs(p) > 1.7976931348623157e308 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308):
        raise OverflowError(
            f"point_id {point_id()}: opt_budget_target(): {b!r} ** {e!r} is past "
            f"the largest float")
    return 1.0 - p


def opt_budget_at_cap(t, cap):
    """The per-unit replicating portfolio value at term start for a trial Cap Rate.

    The cap-solve needs the portfolio as a function of ``c`` while :func:`cap_rate` is
    what the rest of the model reads, so this cell recomputes the BUFFER + CAP + PR
    portfolio directly rather than calling :func:`opt_portfolio`, which would close a
    cycle. It is monotonically increasing in ``cap``. The market is the Term Start
    Date's, through :func:`risk_free_at_term_start`, :func:`div_yield_at_term_start` and
    :func:`impl_vol_at_term_start`, where ``RILA_US_S`` reads its scenario at
    :func:`term_start_month` in place. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    i_s = index_at_term_start(t)
    tau_ = float(term_years())
    pr = participation()
    rate = risk_free_at_term_start(t)
    divy = div_yield_at_term_start(t)
    vol = impl_vol_at_term_start(t)
    atm = pr * bs_call(i_s, i_s, tau_, rate, divy, vol) / i_s
    otm = pr * bs_call(i_s, i_s * (1.0 + cap / pr), tau_, rate, divy, vol) / i_s
    otp = bs_put(i_s, i_s * (1.0 - buffer()), tau_, rate, divy, vol) / i_s
    return atm - otm - otp


def declared_cap_solved(t):
    """The Cap Rate solving ``Pi(c; b, T, sigma, r, q) = beta_target(T)`` **[std]**.

    The ASOP No. 2 determination rule the notes state for redetermining the declared cap
    at each Term Start Date [R5]. The result is floored at the contractual minimum by
    :func:`cap_rate`, not here. A term that began at a renewal before the valuation month
    carries its solved cap on the model point instead, :func:`cap_rate_init`, and this
    cell is not read for it. 0.0 outside cover.

    ``RILA_US_S`` repeats the bisection in every month of a renewal term, on the same
    term-start market each time; here it is solved once a term, by
    :func:`cap_solved_at_start`, keyed by the term's first month on the books: its Term
    Start Date as a month from the valuation date, or :func:`t_entry` for the term under
    way there. Every month of a term reads one key, never a month after ``t`` nor before
    :func:`t_entry`, and the cap is ``RILA_US_S``'s to the last bit.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    return cap_solved_at_start(max(k, t_entry()))


def cap_solved_at_start(t):
    """The cap :func:`declared_cap_solved` solves, once a term, keyed by the term's start.

    ``RILA_US_S``'s bisection, ``nge_solve_iter`` halvings of ``[0,
    nge_cap_search_max]`` on whether :func:`opt_budget_at_cap` at the midpoint is below
    :func:`opt_budget_target`, priced on the market of the term in force at month ``t``,
    which every month of the term shares: ``t`` is the term's first month on the books,
    the key :func:`declared_cap_solved` passes. Because the portfolio value is monotone in
    ``c`` and no root finder may be imported, bisection reaches machine precision on a
    rate.

    :func:`opt_budget_at_cap`'s portfolio is written inline, the at-the-money call, the
    call struck at ``I_s(1 + c/PR)`` and the buffer's put at the term ``T``, as
    :func:`opt_component_at` writes the legs: ``RILA_US_S``'s arithmetic in its order,
    ``math`` admitted in this cell, each call wrapped in ``float(...)``. The at-the-money
    call and the put do not depend on the trial cap, so they are priced once, where
    ``RILA_US_S`` prices them each trial and its cache returns the same doubles, and so are
    the two discount factors; only the call at the cap is priced each trial. So the cap is
    ``RILA_US_S``'s to the last bit, which a module test holds, at one solve a term where
    ``RILA_US_S`` solves in every month of a renewal term. A volatility whose square is
    past the largest float is refused before it is squared, as in
    :func:`opt_component_at`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    target = opt_budget_target()
    i_s = index_at_term_start(t)
    tau_ = float(term_years())
    pr = participation()
    rate = risk_free_at_term_start(t)
    divy = div_yield_at_term_start(t)
    vol = impl_vol_at_term_start(t)
    rate_cc = float(math.log(1.0 + rate))                            # noqa: F821
    divy_cc = float(math.log(1.0 + divy))                            # noqa: F821
    if 1.3407807929942596e154 < abs(vol) <= 1.7976931348623157e308:
        raise OverflowError(
            f"point_id {point_id()}: cap_solved_at_start({t}), the volatility {vol!r} "
            f"squared, is past the largest float")
    root = float(math.sqrt(tau_))                                    # noqa: F821
    drift = (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_
    disc_q = float(math.exp(-divy_cc * tau_))                        # noqa: F821
    disc_r = float(math.exp(-rate_cc * tau_))                        # noqa: F821
    d_1 = (float(math.log(i_s / i_s)) + drift) / (vol * root)        # noqa: F821
    d_2 = d_1 - vol * root
    n_1 = 0.5 * (1.0 + float(math.erf(d_1 / 1.4142135623730951)))    # noqa: F821
    n_2 = 0.5 * (1.0 + float(math.erf(d_2 / 1.4142135623730951)))    # noqa: F821
    atm = pr * (i_s * disc_q * n_1 - i_s * disc_r * n_2) / i_s
    strike = i_s * (1.0 - buffer())
    d_1 = (float(math.log(i_s / strike)) + drift) / (vol * root)     # noqa: F821
    d_2 = d_1 - vol * root
    n_1 = 0.5 * (1.0 + float(math.erf(-d_1 / 1.4142135623730951)))   # noqa: F821
    n_2 = 0.5 * (1.0 + float(math.erf(-d_2 / 1.4142135623730951)))   # noqa: F821
    otp = (strike * disc_r * n_2 - i_s * disc_q * n_1) / i_s
    lo = 0.0
    hi = nge_cap_search_max                                          # noqa: F821
    for _ in range(nge_solve_iter):                                  # noqa: F821
        mid = 0.5 * (lo + hi)
        strike = i_s * (1.0 + mid / pr)
        d_1 = (float(math.log(i_s / strike)) + drift) / (vol * root) # noqa: F821
        d_2 = d_1 - vol * root
        n_1 = 0.5 * (1.0 + float(math.erf(d_1 / 1.4142135623730951)))  # noqa: F821
        n_2 = 0.5 * (1.0 + float(math.erf(d_2 / 1.4142135623730951)))  # noqa: F821
        otm = pr * (i_s * disc_q * n_1 - strike * disc_r * n_2) / i_s
        if atm - otm - otp < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def cap_rate(t):
    """c: the Cap Rate in force for the term containing month t, floored at the minimum.

    The snapshot declared cap on the initial term; on a renewal term either the same
    snapshot (the notes' base projection holds the scale level) or, with ``nge_reset``,
    the solved cap - in both cases floored at the guaranteed minimum [S2]. Returns
    ``+inf`` for an uncapped option, ``Data.cap_uncapped()``, where ``RILA_US_S`` returns
    ``math.inf``: it makes ``min(PR R, c)`` the uncapped payoff and switches the
    out-of-the-money call off in :func:`opt_component_at` [S2].

    A renewal under ``nge_reset`` whose Term Start Date precedes the valuation month was
    re-solved then, on the market of that date, so its cap is the model point's
    :func:`cap_rate_init` for the rest of the term; one at or after the valuation month
    re-solves from the scenario, as ``RILA_US_S`` does. The renewal is read on the policy
    clock: :func:`term_start_month` above 0. Each ``max`` takes the floor first, as
    ``RILA_US_S`` does, each operand bound to a local in that order, since compiled the
    two operands of a ``max`` are evaluated right to left. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_uncapped():
        return data.cap_uncapped()                                   # noqa: F821
    if nge_reset() and term_start_month(t) > 0:
        if term_start_month(t) - duration_mth_init() < t_entry():
            return cap_rate_init()
        floor = guar_min_rate(CAP)                                   # noqa: F821
        solved = declared_cap_solved(t)
        return max(floor, solved)
    floor = guar_min_rate(CAP)                                       # noqa: F821
    cap = declared_cap()
    return max(floor, cap)


def step_rate(t):
    """s: the Step Rate in force, floored at the 2% contractual minimum [S2].

    The floor first, as ``RILA_US_S``'s ``max`` takes it, bound to a local. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    floor = guar_min_rate(STEP)                                      # noqa: F821
    rate = declared_step()
    return max(floor, rate)


def edge_rate(t):
    """e: the Edge Rate in force, floored at the 2% contractual minimum [S2].

    The floor first, as ``RILA_US_S``'s ``max`` takes it, bound to a local. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    floor = guar_min_rate(EDGE)                                      # noqa: F821
    rate = declared_edge()
    return max(floor, rate)


def opt_leg_count():
    """The number of legs of the replicating portfolio for the crediting type.

    Cap: three, the at-the-money call, the out-of-the-money call and the out-of-the-money
    put [S2][S3][S5][S6]. Step: two, the step-scaled at-the-money binary call and the
    out-of-the-money put [S2][S5]. Edge: two, the binary call struck at ``I_s(1 - b)``,
    **in the money** because it pays when the index ratio is at or above ``1 - b``, and the
    put [S2][S5]. Floor: **four** options, not three - buy the at-the-money call spread,
    sell an at-the-money put, and buy back an out-of-the-money put struck at the floor so
    the short put exposure stops there [S5]. ``RILA_US_S``'s ``opt_legs()`` returns the
    legs as a tuple of their names, which no C type holds, so this cell counts them and
    :func:`opt_leg` names each by its code. The crediting type is read through its four
    decodes, :func:`is_cap_crediting` and the three beside it; a type none knows raises
    ``RILA_US_S``'s message.
    """
    if is_cap_crediting():
        return 3
    elif is_step_crediting():
        return 2
    elif is_edge_crediting():
        return 2
    elif is_floor_crediting():
        return 4
    else:
        raise ValueError("invalid crediting_type")


def opt_leg(i):
    """The code of leg ``i`` of the replicating portfolio, in ``RILA_US_S``'s order.

    ``RILA_US_S``'s ``opt_legs()[i]`` as its code, for ``i`` from 0 to
    :func:`opt_leg_count` less 1: Cap ``ATM_CALL``, ``OTM_CALL``, ``OTM_PUT``; Step
    ``STEP_BINARY``, ``OTM_PUT``; Edge ``EDGE_BINARY``, ``OTM_PUT``; Floor ``ATM_CALL``,
    ``OTM_CALL``, ``ATM_PUT``, ``FLOOR_PUT``. A type none of the four decodes knows raises
    ``RILA_US_S``'s message, and an ``i`` past the count ``ValueError("invalid leg
    index")``.
    """
    if is_cap_crediting():
        if i == 0:
            return ATM_CALL                                          # noqa: F821
        elif i == 1:
            return OTM_CALL                                          # noqa: F821
        elif i == 2:
            return OTM_PUT                                           # noqa: F821
    elif is_step_crediting():
        if i == 0:
            return STEP_BINARY                                       # noqa: F821
        elif i == 1:
            return OTM_PUT                                           # noqa: F821
    elif is_edge_crediting():
        if i == 0:
            return EDGE_BINARY                                       # noqa: F821
        elif i == 1:
            return OTM_PUT                                           # noqa: F821
    elif is_floor_crediting():
        if i == 0:
            return ATM_CALL                                          # noqa: F821
        elif i == 1:
            return OTM_CALL                                          # noqa: F821
        elif i == 2:
            return ATM_PUT                                           # noqa: F821
        elif i == 3:
            return FLOOR_PUT                                         # noqa: F821
    else:
        raise ValueError("invalid crediting_type")
    raise ValueError("invalid leg index")


def opt_component(t, leg, spot, tau_, mkt):
    """The **signed** value of one replicating-portfolio leg, per unit of notional.

    Each option's notional is the Investment Amount [S4], and every strike is set from the
    Term Start Date index level ``I_s``, so dividing by ``I_s`` makes each leg
    dimensionless and the portfolio a fraction of notional. ``mkt`` selects the market
    state: ``CURRENT`` prices at month ``t``'s month end, time ``t + 1`` on the valuation
    clock, and ``TERM_START`` under the initial market conditions of the term in force -
    its Term Start Date - which is what the option budget and the ``updated_expiry``
    amortization need. The Term Start Date's market is read through
    :func:`risk_free_at_term_start`, :func:`div_yield_at_term_start` and
    :func:`impl_vol_at_term_start`, from the model point where the term began before the
    valuation month.

    The participation rate multiplies the call spread and re-strikes the short call at
    ``I_s(1 + c/PR)`` [S4]; at ``PR = 1`` that is exactly the plain Cap portfolio, so one
    branch serves both of the notes' first two rows. An uncapped option values the
    out-of-the-money call at zero [S2]. 0.0 outside cover.

    An engine cell, ``RILA_US_S``'s formula with the leg and the market as codes: ``spot``
    and ``tau_`` are floats, so it keeps a Python dict for a cache, and no projection cell
    calls it. The projection reads :func:`opt_component_at`, the same price keyed by a
    basis code, which a module test holds to this cell bit for bit.
    """
    if not is_active(t):
        return 0.0
    if mkt == CURRENT:                                               # noqa: F821
        k = t + 1
        rate = market_state(k, RISK_FREE)                            # noqa: F821
        divy = market_state(k, DIV_YIELD)                            # noqa: F821
        vol = market_state(k, IMPL_VOL)                              # noqa: F821
    elif mkt == TERM_START:                                          # noqa: F821
        rate = risk_free_at_term_start(t)
        divy = div_yield_at_term_start(t)
        vol = impl_vol_at_term_start(t)
    else:
        raise ValueError("invalid mkt")
    i_s = index_at_term_start(t)
    pr = participation() if is_cap_crediting() else 1.0
    if leg == ATM_CALL:                                              # noqa: F821
        return pr * bs_call(spot, i_s, tau_, rate, divy, vol) / i_s
    elif leg == OTM_CALL:                                            # noqa: F821
        cap = cap_rate(t)
        if math.isinf(cap):                                          # noqa: F821
            return 0.0
        strike = i_s * (1.0 + cap / pr)
        return -pr * bs_call(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == OTM_PUT:                                             # noqa: F821
        strike = i_s * (1.0 - buffer())
        return -bs_put(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == ATM_PUT:                                             # noqa: F821
        return -bs_put(spot, i_s, tau_, rate, divy, vol) / i_s
    elif leg == FLOOR_PUT:                                           # noqa: F821
        strike = i_s * (1.0 - floor_rate())
        return bs_put(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == STEP_BINARY:                                         # noqa: F821
        return step_rate(t) * bs_binary_call(spot, i_s, tau_, rate, divy, vol)
    elif leg == EDGE_BINARY:                                         # noqa: F821
        strike = i_s * (1.0 - buffer())
        return edge_rate(t) * bs_binary_call(spot, strike, tau_, rate, divy, vol)
    else:
        raise ValueError("invalid leg")


def opt_component_at(t, leg, basis):
    """The **signed** value of leg ``leg`` per unit of notional, priced on a basis code.

    :func:`opt_component` at the three argument sets the projection prices at, keyed by
    ints, so that the cache is a C array: ``CURRENT``, the leg at the current market,
    ``opt_component(t, leg, index_level(t), tau(t), CURRENT)``, which
    :func:`opt_component_pp`, :func:`deriv_proxy_factor` and
    :func:`trading_cost_factor` read; ``TERM_START``, the leg at its term's start,
    ``opt_component(t, leg, index_at_term_start(t), T, TERM_START)``, the option budget's;
    and ``UPDATED_EXPIRY``, the same initial market at the remaining time,
    ``opt_component(t, leg, index_at_term_start(t), tau(t), TERM_START)``, the
    ``updated_expiry`` amortization's. Any other basis raises ``ValueError("invalid
    basis")``, and any other leg ``ValueError("invalid leg")``.

    The Black-Scholes price is written inline, ``RILA_US_S``'s :func:`bs_call`,
    :func:`bs_put` and :func:`bs_binary_call` with :func:`bs_d1`, :func:`bs_d2` and
    :func:`norm_cdf`, in their arithmetic order, from one set of locals: the intrinsic
    value at ``tau = 0``, and otherwise ``I e^(-q tau) N(d1) - K e^(-r tau) N(d2)`` for a
    call, ``K e^(-r tau) N(-d2) - I e^(-q tau) N(-d1)`` for a put and ``e^(-r tau) N(d2)``
    for a binary, ``N(x) = 0.5 (1 + erf(x / sqrt 2))``, ``sqrt 2`` written as the double
    ``math.sqrt(2.0)`` returns, which a test holds. Its ``math.log``, ``math.exp``,
    ``math.sqrt`` and ``math.erf`` are Python's, called from the compiled cell, each
    wrapped in ``float(...)`` so that every local is a C double, which the registry admits
    in this cell alone (``"python_calls"``): the compiled value is modelx's on every
    platform, and a ``math`` raise is Python's own in both engines. Then each leg's sign
    and scale, as ``RILA_US_S``'s. So the leg is ``RILA_US_S``'s to the last bit, which a
    module test holds against :func:`opt_component` on every committed point and month. A
    volatility whose square is past the largest float is refused before it is squared,
    ``OverflowError`` naming the point, where Python's ``**`` raises its own and the
    compiled power would return ``inf``. An uncapped option's out-of-the-money call is
    0.0, as ``RILA_US_S``'s ``math.isinf(cap)`` makes it, read from
    :func:`is_uncapped`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if basis == CURRENT:                                             # noqa: F821
        spot = index_level(t)
        tau_ = tau(t)
        k = t + 1
        rate = market_state(k, RISK_FREE)                            # noqa: F821
        divy = market_state(k, DIV_YIELD)                            # noqa: F821
        vol = market_state(k, IMPL_VOL)                              # noqa: F821
    elif basis == TERM_START:                                        # noqa: F821
        spot = index_at_term_start(t)
        tau_ = float(term_years())
        rate = risk_free_at_term_start(t)
        divy = div_yield_at_term_start(t)
        vol = impl_vol_at_term_start(t)
    elif basis == UPDATED_EXPIRY:                                    # noqa: F821
        spot = index_at_term_start(t)
        tau_ = tau(t)
        rate = risk_free_at_term_start(t)
        divy = div_yield_at_term_start(t)
        vol = impl_vol_at_term_start(t)
    else:
        raise ValueError("invalid basis")
    i_s = index_at_term_start(t)
    pr = participation() if is_cap_crediting() else 1.0
    if leg == ATM_CALL or leg == ATM_PUT or leg == STEP_BINARY:      # noqa: F821
        strike = i_s
    elif leg == OTM_CALL:                                            # noqa: F821
        cap = cap_rate(t)
        if is_uncapped():
            return 0.0
        strike = i_s * (1.0 + cap / pr)
    elif leg == OTM_PUT or leg == EDGE_BINARY:                       # noqa: F821
        strike = i_s * (1.0 - buffer())
    elif leg == FLOOR_PUT:                                           # noqa: F821
        strike = i_s * (1.0 - floor_rate())
    else:
        raise ValueError("invalid leg")
    if leg == ATM_CALL or leg == OTM_CALL:                           # noqa: F821
        if tau_ <= 0.0:
            price = max(spot - strike, 0.0)
        else:
            rate_cc = float(math.log(1.0 + rate))                    # noqa: F821
            divy_cc = float(math.log(1.0 + divy))                    # noqa: F821
            moneyness = float(math.log(spot / strike))               # noqa: F821
            if 1.3407807929942596e154 < abs(vol) <= 1.7976931348623157e308:
                raise OverflowError(
                    f"point_id {point_id()}: opt_component_at({t}, {leg}, {basis}), "
                    f"the volatility {vol!r} squared, is past the largest float")
            root = float(math.sqrt(tau_))                            # noqa: F821
            d_1 = ((moneyness + (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_)
                   / (vol * root))
            d_2 = d_1 - vol * root
            price = (spot * float(math.exp(-divy_cc * tau_))         # noqa: F821
                     * (0.5 * (1.0 + float(math.erf(d_1 / 1.4142135623730951))))  # noqa
                     - strike * float(math.exp(-rate_cc * tau_))     # noqa: F821
                     * (0.5 * (1.0 + float(math.erf(d_2 / 1.4142135623730951)))))  # noqa
    elif leg == STEP_BINARY or leg == EDGE_BINARY:                   # noqa: F821
        if tau_ <= 0.0:
            price = 1.0 if spot >= strike else 0.0
        else:
            rate_cc = float(math.log(1.0 + rate))                    # noqa: F821
            disc_r = float(math.exp(-rate_cc * tau_))                # noqa: F821
            divy_cc = float(math.log(1.0 + divy))                    # noqa: F821
            moneyness = float(math.log(spot / strike))               # noqa: F821
            if 1.3407807929942596e154 < abs(vol) <= 1.7976931348623157e308:
                raise OverflowError(
                    f"point_id {point_id()}: opt_component_at({t}, {leg}, {basis}), "
                    f"the volatility {vol!r} squared, is past the largest float")
            root = float(math.sqrt(tau_))                            # noqa: F821
            d_1 = ((moneyness + (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_)
                   / (vol * root))
            d_2 = d_1 - vol * root
            price = disc_r * (0.5 * (1.0 + float(math.erf(d_2 / 1.4142135623730951))))
    else:
        if tau_ <= 0.0:
            price = max(strike - spot, 0.0)
        else:
            rate_cc = float(math.log(1.0 + rate))                    # noqa: F821
            divy_cc = float(math.log(1.0 + divy))                    # noqa: F821
            moneyness = float(math.log(spot / strike))               # noqa: F821
            if 1.3407807929942596e154 < abs(vol) <= 1.7976931348623157e308:
                raise OverflowError(
                    f"point_id {point_id()}: opt_component_at({t}, {leg}, {basis}), "
                    f"the volatility {vol!r} squared, is past the largest float")
            root = float(math.sqrt(tau_))                            # noqa: F821
            d_1 = ((moneyness + (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_)
                   / (vol * root))
            d_2 = d_1 - vol * root
            price = (strike * float(math.exp(-rate_cc * tau_))       # noqa: F821
                     * (0.5 * (1.0 + float(math.erf(-d_2 / 1.4142135623730951))))  # noqa
                     - spot * float(math.exp(-divy_cc * tau_))       # noqa: F821
                     * (0.5 * (1.0 + float(math.erf(-d_1 / 1.4142135623730951)))))  # noqa
    if leg == ATM_CALL:                                              # noqa: F821
        return pr * price / i_s
    elif leg == OTM_CALL:                                            # noqa: F821
        return -pr * price / i_s
    elif leg == OTM_PUT or leg == ATM_PUT:                           # noqa: F821
        return -price / i_s
    elif leg == FLOOR_PUT:                                           # noqa: F821
        return price / i_s
    elif leg == STEP_BINARY:                                         # noqa: F821
        return step_rate(t) * price
    else:
        return edge_rate(t) * price


def opt_portfolio(t, spot, tau_, mkt):
    """Pi(I, tau): the per-unit market value of the replicating option portfolio.

    The sum of the signed legs. **Verification identity**: at ``tau = 0`` this collapses
    to the crediting rate ``g`` for every crediting type - for the Cap design
    ``max(R,0) - max(R-c,0) - max(-b-R,0) = g``. If the interim value at term end does not
    reproduce ``IA(1 + g)`` exactly, the strike set or the notional convention is wrong;
    :func:`check_term_end_identity` tests it.

    An engine cell, ``RILA_US_S``'s ``sum``, over the legs :func:`opt_leg` names in
    ``RILA_US_S``'s order, which adds the same doubles as ``RILA_US_S``'s over its
    ``opt_legs()``. The projection reads :func:`opt_portfolio_at`.
    """
    return sum(opt_component(t, opt_leg(i), spot, tau_, mkt)
               for i in range(opt_leg_count()))


def opt_portfolio_abs(t, spot, tau_, mkt):
    """The sum of the **absolute** leg values: the trading cost assessment base **[std]**.

    A wider base than the Academy's net derivative value [R6], deliberately, because no
    prospectus quantifies the trading cost provision; the base must be stated whenever the
    factor is recalibrated. An engine cell, as :func:`opt_portfolio` is; the projection
    reads :func:`opt_portfolio_abs_at`.
    """
    return sum(abs(opt_component(t, opt_leg(i), spot, tau_, mkt))
               for i in range(opt_leg_count()))


def opt_portfolio_at(t, basis):
    """Pi on a basis code: the legs of :func:`opt_component_at` summed as ``sum`` adds.

    :func:`opt_portfolio` at the projection's three argument sets, ``CURRENT``,
    ``TERM_START`` and ``UPDATED_EXPIRY`` (:func:`opt_component_at`), keyed by ints.
    ``RILA_US_S`` adds the legs with Python's ``sum``, which CPython 3.12 and later
    compensates on floats, Neumaier's way, so the loop here does the same, over the legs
    :func:`opt_leg` names in ``RILA_US_S``'s order, from ``0.0 +`` the first, adding the
    compensation once at the end where it is finite: the same double as ``RILA_US_S``'s,
    where a running sum is not. No ``sum`` and no generator, which compiled would be calls
    into Python. 0.0 outside cover, every leg being 0.0 there.
    """
    total = 0.0
    comp = 0.0
    for i in range(opt_leg_count()):
        x = opt_component_at(t, opt_leg(i), basis)
        added = total + x
        if abs(total) >= abs(x):
            comp = comp + ((total - added) + x)
        else:
            comp = comp + ((x - added) + total)
        total = added
    if comp != 0.0 and abs(comp) <= 1.7976931348623157e308:
        total = total + comp
    return total


def opt_portfolio_abs_at(t, basis):
    """The sum of the absolute legs on a basis code, as ``sum`` adds them.

    :func:`opt_portfolio_abs` at the projection's argument sets, keyed by ints: the
    absolute value of each leg of :func:`opt_component_at`, added by Neumaier's loop as
    :func:`opt_portfolio_at` adds the signed legs, and as CPython's ``sum`` adds
    ``RILA_US_S``'s generator. :func:`trading_cost_factor` reads it at ``CURRENT``.
    """
    total = 0.0
    comp = 0.0
    for i in range(opt_leg_count()):
        x = abs(opt_component_at(t, opt_leg(i), basis))
        added = total + x
        if abs(total) >= abs(x):
            comp = comp + ((total - added) + x)
        else:
            comp = comp + ((x - added) + total)
        total = added
    if comp != 0.0 and abs(comp) <= 1.7976931348623157e308:
        total = total + comp
    return total


def opt_budget(t):
    """beta: the initial option budget per unit of notional, ``Pi(I_s, T)``.

    Struck at each Term Start Date under the market conditions of that date. On the anchor
    cell ``beta = 10.0632%``, so the option budget is $10,063.19 of a $100,000 Investment
    Amount and the fixed leg opens at $89,936.81. A term that began before the valuation
    month prices it from the model point's term-start market, so the budget is the one
    struck then. ``opt_portfolio_at(t, TERM_START)``, ``RILA_US_S``'s
    ``opt_portfolio(t, index_at_term_start(t), T, TERM_START)``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return opt_portfolio_at(t, TERM_START)                           # noqa: F821


def fixed_leg_yield(t):
    """The equivalent geometric accretion yield on the fixed leg, ``(1-beta)^(-1/T) - 1``.

    1.7834% on the anchor cell: the rate at which $89,936.81 accretes to $100,000 over six
    years. The gap to the 4.00% market rate is :func:`nge_spread_implied`. 0.0 outside
    cover.

    ``Data`` accepts a declared rate and a market that price the budget at 1 or more: a
    Step declared at 3.0 on a one-year term does. ``RILA_US_S`` then takes the power of a
    base of 0 or below, and this cell answers as Python's ``**`` does where it is a real
    number and refuses where it is not, in both engines (the Space docstring's *Powers*):
    on a one-year term the exponent is -1, and any base but 0 gives ``RILA_US_S``'s float;
    a base of 0 raises Python's own ``ZeroDivisionError``; a base below 0 on a longer term,
    where ``RILA_US_S`` returns a complex number, raises ``ValueError`` naming the point;
    and a power past the largest float, ``OverflowError`` naming it.
    """
    if not is_active(t):
        return 0.0
    b = 1.0 - opt_budget(t)
    e = -1.0 / term_years()
    if b == 0.0:
        raise ZeroDivisionError("0.0 cannot be raised to a negative power")
    if b < 0.0 and term_years() != 1:
        raise ValueError(
            f"point_id {point_id()}: fixed_leg_yield({t}): 1 - opt_budget, {b!r}, is "
            f"below 0, and its power -1 / term_years is no real number")
    if (e != 0.0 and b != 0.0 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308
            and not (0.01 < abs(b) < 100.0 and abs(e) < 150.0)
            and e * float(math.log(abs(b))) > 709.7827128933845):    # noqa: F821
        raise OverflowError(
            f"point_id {point_id()}: fixed_leg_yield({t}): {b!r} ** {e!r} is past "
            f"the largest float")
    p = b ** e
    if (abs(p) > 1.7976931348623157e308 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308):
        raise OverflowError(
            f"point_id {point_id()}: fixed_leg_yield({t}): {b!r} ** {e!r} is past "
            f"the largest float")
    return p - 1.0


def nge_spread_implied(t):
    """The spread implied by the declared cap: ``earned rate - fixed leg yield``.

    2.22% on the anchor cell, and that is the **[std]** ``nge_spread`` input to the
    cap-solve rule - the model's own snapshot, read back out of the snapshot cap. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    return earned_rate - fixed_leg_yield(t)                          # noqa: F821


def credit_rate_at(t, accrual):
    """g: the crediting rate applied to R(t), with the declared rates scaled by ``accrual``.

    ``accrual = 1`` is the contractual term-end rule [S1][S2][S4][S5]::

        BUFFER + CAP    g = min(PR R, c)      if R >= 0;  g = min(0, R + b)  if R < 0
        BUFFER + STEP   g = s                 if R >= 0;  g = min(0, R + b)  if R < 0
        BUFFER + EDGE   g = e                 if R >= -b; g = R + b          if R < -b
        FLOOR  + CAP    g = min(max(R, -f), c)

    The ``min(0, .)`` in the buffer branch is load-bearing: the Performance Rate can never
    be greater than zero if the Index Performance is negative [S1]. The discontinuities -
    a Step design paying the full step at ``R = 0.00%`` and zero at ``R = -0.01%``, an
    Edge design flipping at the buffer edge - are contractual; do not smooth them [S2][S4].

    ``accrual < 1`` is the **pre-AG 54** design [S1], which uses no option pricing at all:
    the buffer, Cap and Step Rates each accrue linearly over the term and the term-end
    rules are applied to the accrued rates. The crediting type is read through its four
    decodes, and a type none knows raises ``RILA_US_S``'s message. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    perf = index_perf(t)
    buff = buffer() * accrual
    if is_cap_crediting():
        cap = cap_rate(t)
        cap = cap if math.isinf(cap) else cap * accrual              # noqa: F821
        return min(participation() * perf, cap) if perf >= 0.0 else min(0.0, perf + buff)
    elif is_step_crediting():
        return step_rate(t) * accrual if perf >= 0.0 else min(0.0, perf + buff)
    elif is_edge_crediting():
        edge = edge_rate(t) * accrual
        return edge if perf >= -buff else perf + buff
    elif is_floor_crediting():
        cap = cap_rate(t)
        cap = cap if math.isinf(cap) else cap * accrual              # noqa: F821
        return min(max(perf, -floor_rate() * accrual), cap)
    else:
        raise ValueError("invalid crediting_type")


def credit_rate_by(t, rule):
    """g by a rule code: :func:`credit_rate_at` at the two accruals the projection reads.

    ``TERM_END``, ``accrual = 1``, the contractual term-end rule :func:`credit_rate_term`
    reads, and ``PRORATED``, ``accrual = 1 - tau(t) / T``, the pre-AG 54 time-prorated rule
    :func:`credit_rate_accrued` reads; any other rule raises ``ValueError("invalid
    rule")``. :func:`credit_rate_at`'s formula, keyed by an int, so that the cache is a C
    array, with :func:`is_uncapped` where ``RILA_US_S`` asks ``math.isinf(cap)``, and the
    accrual formed before the cover test, as ``RILA_US_S`` forms its argument before the
    call. 0.0 outside cover.
    """
    if rule == TERM_END:                                             # noqa: F821
        accrual = 1.0
    elif rule == PRORATED:                                           # noqa: F821
        accrual = 1.0 - tau(t) / term_years()
    else:
        raise ValueError("invalid rule")
    if not is_active(t):
        return 0.0
    perf = index_perf(t)
    buff = buffer() * accrual
    if is_cap_crediting():
        cap = cap_rate(t)
        cap = cap if is_uncapped() else cap * accrual
        return min(participation() * perf, cap) if perf >= 0.0 else min(0.0, perf + buff)
    elif is_step_crediting():
        return step_rate(t) * accrual if perf >= 0.0 else min(0.0, perf + buff)
    elif is_edge_crediting():
        edge = edge_rate(t) * accrual
        return edge if perf >= -buff else perf + buff
    elif is_floor_crediting():
        cap = cap_rate(t)
        cap = cap if is_uncapped() else cap * accrual
        return min(max(perf, -floor_rate() * accrual), cap)
    else:
        raise ValueError("invalid crediting_type")


def credit_rate_term(t):
    """g at a Term End Date, zero in every other month.

    Applied as ``IA_k(term end) = IA_k(term start, adjusted for withdrawals) x (1 + g)``
    [S1][S2]. ``credit_rate_by(t, TERM_END)``, ``RILA_US_S``'s ``credit_rate_at(t, 1.0)``.
    """
    return credit_rate_by(t, TERM_END) if is_term_end(t) else 0.0    # noqa: F821


def credit_rate_accrued(t):
    """The pre-AG 54 time-prorated crediting rate at month t [S1].

    ``credit_rate_by(t, PRORATED)``, ``RILA_US_S``'s ``credit_rate_at(t, 1 - tau(t) /
    T)``, the elapsed share of the term, on the term clock :func:`term_elapsed_mth` reads
    from the policy clock. The source worked example - $50,000, a 10% buffer, a 10% Cap on
    a one-year term, index 500 to 600 at day 183 - gives an accrued cap of 5%, a 5%
    Performance Rate and an interim value of $52,500; on a monthly grid the sixth month
    end of twelve is exactly half the term, and that is the end of policy month 5, so the
    model reproduces it to the cent.
    """
    return credit_rate_by(t, PRORATED)                               # noqa: F821


def budget_amort_factor(t):
    """B_k(t) / IA_k(t): the amortized initial option budget, per unit of notional.

    ``straight_line`` **[std]** [S2] gives ``beta x tau/T``; ``updated_expiry`` [S3] gives
    the initial-market-conditions portfolio value re-read at the current time to expiry.
    Both are forced to zero at ``tau = 0``, which is AG 54's boundary condition and what
    makes ``V = IA(1 + g)`` exact at term end.

    **This is where homogeneity is imposed.** ``B`` is defined against the *current*
    ``IA``, so every term of the interim value scales with the notional and a withdrawal
    reduces the interim value by exactly the cash removed. Freezing ``B`` at the
    term-start notional instead would make the contract silently gain or lose value on
    every withdrawal. The rule is read through its two decodes, :func:`is_straight_line`
    and :func:`is_updated_expiry`, and a rule neither knows raises ``RILA_US_S``'s
    message. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if tau(t) <= 0.0:
        return 0.0
    if is_straight_line():
        return opt_budget(t) * tau(t) / term_years()
    elif is_updated_expiry():
        return opt_portfolio_at(t, UPDATED_EXPIRY)                   # noqa: F821
    else:
        raise ValueError("invalid amort_rule")


def mva_factor(t):
    """``[(1 + r_0) / (1 + r(t))]^tau``: the interim value's interest-rate adjustment [S2].

    The only market-value-adjustment-like term in the contract, and it lives **inside**
    the interim value rather than on the surrender benefit - this product has no contract
    MVA. At the worked-example parameters a 100 bp rise costs $2,687.62 of interim value
    at the term midpoint, two orders of magnitude more than the entire trading-cost
    provision. Family (c) has no such term at all [S5], so the choice of interim-value
    family is itself a rate-sensitivity assumption. ``r_0`` is the model point's for a term
    begun before the valuation month (:func:`mvr_at_term_start`). ``Data`` holds both
    rates above -1, so the base is above 0; a power past the largest float, which a Market
    Value Rate far apart from the term's reaches, is refused, ``OverflowError`` naming the
    point (the Space docstring's *Powers*). 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    b = (1.0 + mvr_at_term_start(t)) / (1.0 + mvr(t))
    e = tau(t)
    if (e != 0.0 and b != 0.0 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308
            and not (0.01 < abs(b) < 100.0 and abs(e) < 150.0)
            and e * float(math.log(abs(b))) > 709.7827128933845):    # noqa: F821
        raise OverflowError(
            f"point_id {point_id()}: mva_factor({t}): {b!r} ** {e!r} is past "
            f"the largest float")
    p = b ** e
    if (abs(p) > 1.7976931348623157e308 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308):
        raise OverflowError(
            f"point_id {point_id()}: mva_factor({t}): {b!r} ** {e!r} is past "
            f"the largest float")
    return p


def fixed_proxy_factor(t):
    """F_k(t) / IA_k(t): the Fixed Income Asset Proxy, per unit of notional.

    ``portfolio`` **[std]**: ``(1 - B/IA) x mva_factor`` - AG 54's hypothetical bond,
    starting at base less the derivative proxy and accreting to the base at unchanged
    yield [R2][S2]. ``notional``: the **full** notional discounted at an investment-grade
    rate, risk-free plus ``iv_credit_spread`` = **[std]** 1.00%, with no subtraction of an
    option budget [S4][S6]. No source quantifies that spread - [S4] says only that the
    rate is investment-grade, above swap rates, and therefore "will result in a lower
    value for that component" - so the 1.00% is a standardization on the same footing as
    ``iv_expense_rate``, and family (b)'s interim value moves with it. ``delta``:
    ``1 - B/IA``, the notional plus the amortization term, with no rate adjustment [S5].
    The family is read through its four decodes, :func:`is_iv_portfolio` and the three
    beside it, and a family none knows raises ``RILA_US_S``'s message. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_iv_portfolio():
        return (1.0 - budget_amort_factor(t)) * mva_factor(t)
    elif is_iv_notional():
        b = 1.0 + risk_free(t) + iv_credit_spread                    # noqa: F821
        e = -tau(t)
        if e != 0.0 and b == 0.0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        if b < 0.0 and (12 * term_years() - term_elapsed_mth(t)) % 12 != 0:
            raise ValueError(
                f"point_id {point_id()}: fixed_proxy_factor({t}): 1 + risk_free + "
                f"iv_credit_spread, {b!r}, is below 0, and its power -tau, {e!r}, is no "
                f"real number")
        if (e != 0.0 and b != 0.0 and abs(b) <= 1.7976931348623157e308
                and abs(e) <= 1.7976931348623157e308
                and not (0.01 < abs(b) < 100.0 and abs(e) < 150.0)
                and e * float(math.log(abs(b))) > 709.7827128933845):  # noqa: F821
            raise OverflowError(
                f"point_id {point_id()}: fixed_proxy_factor({t}): {b!r} ** {e!r} is past "
                f"the largest float")
        p = b ** e
        if (abs(p) > 1.7976931348623157e308 and abs(b) <= 1.7976931348623157e308
                and abs(e) <= 1.7976931348623157e308):
            raise OverflowError(
                f"point_id {point_id()}: fixed_proxy_factor({t}): {b!r} ** {e!r} is past "
                f"the largest float")
        return p
    elif is_iv_delta():
        return 1.0 - budget_amort_factor(t)
    elif is_iv_legacy():
        return 0.0
    else:
        raise ValueError("invalid iv_family")


def deriv_proxy_factor(t):
    """D_k(t) / IA_k(t): the Derivative Asset Proxy, ``Pi(I(t), tau(t))``.

    Valued at the current market state, on the valuation clock:
    ``opt_portfolio_at(t, CURRENT)``. The pre-AG 54 ``legacy`` engine has no derivative
    proxy at all - it uses no option pricing. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_iv_legacy():
        return 0.0
    return opt_portfolio_at(t, CURRENT)                              # noqa: F821


def trading_cost_factor(t):
    """TC_k(t) / IA_k(t): the trading cost provision, ``kappa x sum |leg values|``.

    Strictly interior to the term: ``kappa_effective = kappa x 1{tau > 0}`` **[std]**.
    There are no options left to exit at term end, the Academy example likewise shows no
    trading cost there [R6], and leaving the provision switched on at ``tau = 0`` breaks
    the term-end verification identity by ``kappa x IA x |g|``. Only family (a) carries
    it; family (b) has an always-positive expense rebate instead [S4] and family (c)
    states none [S5]. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if not is_iv_portfolio() or tau(t) <= 0.0:
        return 0.0
    return trading_cost_rate * opt_portfolio_abs_at(t, CURRENT)      # noqa: F821


def cap_calc_factor(t):
    """CCF_k(t) / IA_k(t): the Cap Calculation Factor of family (b) [S4].

    ``E_0 x tau/T`` - "a return of estimated expenses for the portion of the Segment
    Duration that has not elapsed", always positive and declining to zero at term end;
    the source works it as $10 of estimated expenses on a one-year segment giving $6 with
    219 days remaining. ``E_0`` is expressed here as a rate of notional,
    ``iv_expense_rate`` = **[std]** 0.10%, because no source quantifies it - the same
    standing as family (b)'s other free parameter, ``iv_credit_spread``. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if not is_iv_notional():
        return 0.0
    return iv_expense_rate * tau(t) / term_years()                   # noqa: F821


def iv_factor(t):
    """V_k(t) / IA_k: the interim value per unit of the month's **opening** notional.

    ``F + D - TC + CCF`` for the three AG 54-era families, and ``1 + g_accrued`` for the
    pre-AG 54 one. Two boundaries fall out of the algebra rather than being imposed: at
    ``tau = T`` the fixed and derivative legs sum to exactly 1, which is AG 54's
    requirement that the Index Strategy Base equal the Strategy Value at term start [R2];
    at ``tau = 0`` they sum to ``1 + g``, which is the term-end Strategy Value.

    ``tau = T`` is an instant - the opening of the term's first month - and not a
    projected month, so no row of the frame carries it; the interim value is **undefined**
    at term start and term end alike, those points being Strategy Values rather than
    Interim Values [R6]. At a Term End Date, which *is* a month end, :func:`iv_ratio`
    returns 1 for the Transfer Period [S2] rather than this factor. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_iv_legacy():
        return 1.0 + credit_rate_accrued(t)
    return (fixed_proxy_factor(t) + deriv_proxy_factor(t)
            - trading_cost_factor(t) + cap_calc_factor(t))


def iv_ratio(t):
    """V_k(t) / IA_k(t): the interim value per unit of the **current** notional.

    1 at a Term End Date, where the Investment Amount has just been credited and the
    interim value equals it for the Transfer Period [S2]; the interim value factor
    otherwise. Multiplying by this is how homogeneity is carried through the model: the
    same ratio serves before and after a withdrawal, so the interim value falls by exactly
    the cash removed.
    """
    return 1.0 if is_term_end(t) else iv_factor(t)


def inv_amt_basis_pp(t):
    """IA_k: the notional the month-t valuation applies to, per contract.

    The Investment Amount **entering** month ``t``: the prior month's Investment Amount
    after the month the contract enters the books, :func:`t_entry`. In that month it is
    the opening state: the whole purchase payment in the issue month of a contract issued
    at or after the valuation date - the anchor cell allocates 100% to one 6-year option,
    and the payment falls at the opening of that month - and the model point's
    :func:`inv_amt_pp_init` on a contract in force. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        return inv_amt_pp(t - 1)
    if duration_mth(t) == 0:
        return premium_pp()
    return inv_amt_pp_init()


def iv_notional_pp(t, timing):
    """The notional an interim-value decomposition column is measured on.

    ``BEF_ROLL`` is the opening notional, the one in force during month ``t`` before the
    roll split - the notes' rows A1, B1, A2 and B3. ``AFT_WD`` is the notional after
    the proportional withdrawal reduction - the notes' row B2, in which **every** component
    of the interim value scales by the same factor, which is exactly why the interim value
    then falls by precisely the cash withdrawn.
    """
    if timing == BEF_ROLL:
        return inv_amt_basis_pp(t)
    elif timing == AFT_WD:
        return inv_amt_pp(t)
    else:
        raise ValueError("invalid timing")


def opt_component_pp(t, leg, timing):
    """The currency value of one replicating-portfolio leg, per contract.

    The notional at ``timing``, ``BEF_ROLL`` or ``AFT_WD`` (:func:`iv_notional_pp`), times
    the per-unit leg value at the current market state, ``opt_component_at(t, leg,
    CURRENT)``. These are the worked example's ATM call, OTM call and OTM put columns.
    0.0 outside cover, where no market path is read.
    """
    if not is_active(t):
        return 0.0
    return iv_notional_pp(t, timing) * opt_component_at(t, leg, CURRENT)  # noqa: F821


def fixed_proxy_pp(t, timing):
    """F_k(t): the Fixed Income Asset Proxy in currency, per contract."""
    return iv_notional_pp(t, timing) * fixed_proxy_factor(t)


def budget_amort_pp(t, timing):
    """B_k(t): the amortized initial option budget in currency, per contract."""
    return iv_notional_pp(t, timing) * budget_amort_factor(t)


def deriv_proxy_pp(t, timing):
    """D_k(t): the Derivative Asset Proxy in currency, per contract."""
    return iv_notional_pp(t, timing) * deriv_proxy_factor(t)


def trading_cost_pp(t, timing):
    """TC_k(t): the trading cost provision in currency, per contract."""
    return iv_notional_pp(t, timing) * trading_cost_factor(t)


def inv_amt_pp_at(t, timing):
    """IA_k: the Investment Amount per contract, read at a point inside month t.

    ``BEF_CREDIT`` is the opening notional, :func:`inv_amt_basis_pp`, whose opening on
    a contract in force is the model point's; ``BEF_ROLL`` applies term-end crediting;
    ``BEF_WD`` applies the renewal / transfer roll split; ``AFT_WD`` applies the
    proportional withdrawal reduction. Outside a Term End Date the first three coincide.
    """
    if timing == BEF_CREDIT:
        return inv_amt_basis_pp(t)
    elif timing == BEF_ROLL:
        return inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t))
    elif timing == BEF_WD:
        rolled = inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t))
        return rolled * roll_share(OPTION) if is_term_end(t) else rolled
    elif timing == AFT_WD:
        return inv_amt_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_amt_pp(t):
    """IA_k(t): the Investment Amount (AG 54 Index Strategy Base) at end of month t.

    Term-end crediting, then the roll split, then **the universal proportional rule**::

        IA_k(t+) = IA_k(t-) x (1 - G_k / V_k(t-))

    Every insurer in the sample reduces the notional in proportion to the reduction in
    interim value, not dollar for dollar [S2][S3][S4][S6], and the reduction in notional
    therefore **exceeds the cash received** whenever the interim value is below the
    notional - by ``G (IA/V - 1)``, $1,433.62 on the worked example's $8,000 withdrawal.
    Modelling withdrawals as dollar-for-dollar reductions overstates the remaining
    notional in down markets and compounds through the rest of the term.

    The rule is undefined at a non-positive interim value, which this contract can produce
    [S2]; the model then leaves the notional unreduced **[std]**, the withdrawal having
    been allocated away from the option by :func:`wd_alloc_pp`.

    The opening is written inline, as :func:`inv_amt_basis_pp` gives it - the prior
    month's amount after :func:`t_entry`, the purchase payment in the issue month, the
    model point's :func:`inv_amt_pp_init` on a contract in force - so the chain of calls
    back to :func:`t_entry` is one cell a month, where ``RILA_US_S``'s runs through
    :func:`inv_amt_pp_at` and :func:`inv_amt_basis_pp`; the arithmetic, the crediting and
    the roll split are ``RILA_US_S``'s, bit for bit. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        opening = inv_amt_pp(t - 1)
    elif duration_mth(t) == 0:
        opening = premium_pp()
    else:
        opening = inv_amt_pp_init()
    rolled = opening * (1.0 + credit_rate_term(t))
    base = rolled * roll_share(OPTION) if is_term_end(t) else rolled
    value = interim_value_pp_at(t, BEF_WD)
    if value <= 0.0:
        return base
    return base * (1.0 - wd_alloc_pp(t, OPTION) / value)


def interim_value_pp_at(t, timing):
    """V_k: the Interim Value per contract, read at a point inside month t.

    ``BEF_ROLL`` is the worked example's Interim value column - the value at month
    ``t``'s month end of the option in force during it, after any term-end crediting and
    before the roll split.
    ``BEF_WD`` and ``AFT_WD`` are that value carried through the roll split and the
    withdrawal, each as the Investment Amount at that point times :func:`iv_ratio`.

    Every mid-term transaction settles here: withdrawal, surrender, death benefit,
    annuitization, transfer and any fee deduction [S1][S2][S4][S6]. It can be **negative
    even when the index is up** [S2]; flooring it at zero, or at the notional, is not
    implementing the contract.
    """
    if timing == BEF_ROLL:
        return inv_amt_basis_pp(t) * iv_factor(t)
    elif timing == BEF_WD:
        return inv_amt_pp_at(t, BEF_WD) * iv_ratio(t)
    elif timing == AFT_WD:
        return inv_amt_pp(t) * iv_ratio(t)
    else:
        raise ValueError("invalid timing")


def roll_share(bucket):
    """The Term End Date roll split **[std]**: 80 / 5 / 15 / 0.

    80% renew into the same option at the new declared rate - the contractual default
    [S1] - 5% transfer to a different index-linked option, modelled as renewal at the same
    parameters, and 15% transfer to the Fixed Account. The Holding Account share is zero
    on the base run: it receives maturing amounts only when the option **and** the Fixed
    Account are both unavailable [S2].

    On a probability-weighted single-contract model point the split is a split of *value*
    between the buckets, which is why it can be applied per contract and independently of
    the ``phi`` surrender fraction the notes place before it.
    """
    if bucket == OPTION:
        return roll_renew_same + roll_transfer_other                 # noqa: F821
    elif bucket == FIXED:
        return roll_transfer_fixed                                   # noqa: F821
    elif bucket == HOLDING:
        return roll_transfer_holding                                 # noqa: F821
    else:
        raise ValueError("invalid bucket")


def roll_to_acct_pp(t, bucket):
    """The amount transferred out of the option into a general-account bucket at term end.
    """
    if not is_term_end(t):
        return 0.0
    return inv_amt_pp_at(t, BEF_ROLL) * roll_share(bucket)


def acct_rate():
    """The declared Fixed and Holding Account rate, floored at the 1% minimum [S1][S2].

    3.00% **[std]** - only the contractual minimum is public.
    """
    return max(declared_acct_rate, guar_min_acct_rate)               # noqa: F821


def fixed_acct_pp_at(t, timing):
    """FA: the Fixed Account value per contract, read at a point inside month t.

    ``FA(t) = FA(t-1) x (1 + max(i_declared, 0.01))^(1/12)`` [S1][S2], plus any amount
    transferred in at a Term End Date, less its pro-rata share of the withdrawal. The
    transfer accrues for the month in which it arrives **[std]**. The bucket opens empty
    on a contract issued at or after the valuation date: the purchase payment is allocated
    wholly to the index-linked option, so the Fixed Account enters the issue month at zero
    and stays there until the first Term End Date. On a contract in force it opens at
    :func:`t_entry` from the model point, :func:`fixed_acct_pp_init`. 0.0 outside cover.
    """
    if timing == BEF_WD:                                             # noqa: F821
        if not is_active(t):
            return 0.0
        prior = fixed_acct_pp(t - 1) if t > t_entry() else fixed_acct_pp_init()
        opening = prior + roll_to_acct_pp(t, FIXED)                  # noqa: F821
        growth = 1.0 + acct_rate()
        if growth < 0.0:
            raise ValueError(
                f"point_id {point_id()}: fixed_acct_pp_at({t}, BEF_WD): 1 + acct_rate, "
                f"{growth!r}, is below 0, and its power 1 / 12 is no real number")
        return opening * growth ** (1.0 / 12.0)
    elif timing == AFT_WD:                                           # noqa: F821
        return fixed_acct_pp(t)
    else:
        raise ValueError("invalid timing")


def fixed_acct_pp(t):
    """FA(t): the Fixed Account value per contract at the end of month t.

    ``fixed_acct_pp_at(t, BEF_WD)`` less the account's share of the withdrawal,
    written inline from the prior month's value, so that the chain back to
    :func:`t_entry` is one cell a month; the arithmetic is ``RILA_US_S``'s. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    prior = fixed_acct_pp(t - 1) if t > t_entry() else fixed_acct_pp_init()
    opening = prior + roll_to_acct_pp(t, FIXED)                      # noqa: F821
    growth = 1.0 + acct_rate()
    if growth < 0.0:
        raise ValueError(
            f"point_id {point_id()}: fixed_acct_pp({t}): 1 + acct_rate, {growth!r}, is "
            f"below 0, and its power 1 / 12 is no real number")
    return opening * growth ** (1.0 / 12.0) - wd_alloc_pp(t, FIXED)  # noqa: F821


def holding_acct_pp_at(t, timing):
    """HA: the Holding Account value per contract, read at a point inside month t.

    Same accrual and the same 1% guaranteed minimum as the Fixed Account [S1][S2]. It
    holds maturing amounts to the next Contract Anniversary when the option and the Fixed
    Account are both unavailable [S2]; ``roll_transfer_holding`` is 0 on the base run, so
    the bucket stays empty and is carried for completeness of ``AV = sum V_k + FA + HA``.
    It opens empty for the same reason the Fixed Account does, and on a contract in force
    from the model point, :func:`holding_acct_pp_init`. 0.0 outside cover.
    """
    if timing == BEF_WD:                                             # noqa: F821
        if not is_active(t):
            return 0.0
        prior = holding_acct_pp(t - 1) if t > t_entry() else holding_acct_pp_init()
        opening = prior + roll_to_acct_pp(t, HOLDING)                # noqa: F821
        growth = 1.0 + acct_rate()
        if growth < 0.0:
            raise ValueError(
                f"point_id {point_id()}: holding_acct_pp_at({t}, BEF_WD): 1 + acct_rate, "
                f"{growth!r}, is below 0, and its power 1 / 12 is no real number")
        return opening * growth ** (1.0 / 12.0)
    elif timing == AFT_WD:                                           # noqa: F821
        return holding_acct_pp(t)
    else:
        raise ValueError("invalid timing")


def holding_acct_pp(t):
    """HA(t): the Holding Account value per contract at the end of month t.

    Written inline as :func:`fixed_acct_pp` is, one cell a month back to :func:`t_entry`.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prior = holding_acct_pp(t - 1) if t > t_entry() else holding_acct_pp_init()
    opening = prior + roll_to_acct_pp(t, HOLDING)                    # noqa: F821
    growth = 1.0 + acct_rate()
    if growth < 0.0:
        raise ValueError(
            f"point_id {point_id()}: holding_acct_pp({t}): 1 + acct_rate, {growth!r}, is "
            f"below 0, and its power 1 / 12 is no real number")
    return opening * growth ** (1.0 / 12.0) - wd_alloc_pp(t, HOLDING)  # noqa: F821


def av_pp_at(t, timing):
    """AV: the Account Value per contract, ``sum_k V_k(t) + FA(t) + HA(t)``.

    ``BEF_WD`` is the notes' step 5 value - after crediting, the roll split, the interim
    value and the account accruals, before any transaction. It is the base the withdrawal
    is allocated across, the base the free-withdrawal allowance is snapshotted from, and
    the base the return-of-premium reduction ratio uses. ``AFT_WD`` is
    :func:`av_pp`, the value every decrement benefit is measured on.

    Between term start and term end this contract has **no account value in the ordinary
    sense**: ``AV`` is a derivative price, depressed exactly when the option leg is out of
    the money - which is when the return-of-premium guarantee bites.

    There is no opening timing here. The Account Value entering a contract's issue month
    is the purchase payment itself, which :func:`inv_amt_basis_pp` carries, the
    general-account buckets opening empty; entering the valuation month on a contract in
    force it is the model point's :func:`av_pp_init`, and the buckets open from theirs.
    The ``BEF_WD`` value at an anniversary month is what :func:`free_wd_base` reads, from
    the frame where the anniversary is in it.
    """
    if timing == BEF_WD:
        return (interim_value_pp_at(t, BEF_WD)
                + fixed_acct_pp_at(t, BEF_WD)
                + holding_acct_pp_at(t, BEF_WD))
    elif timing == AFT_WD:
        return av_pp(t)
    else:
        raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the Account Value per contract at the end of month t."""
    return (interim_value_pp_at(t, AFT_WD)
            + fixed_acct_pp(t) + holding_acct_pp(t))


def inv_income_pp(t):
    """The investment return credited to one contract's Account Value in month t.

    ``AV`` before the transaction less the value entering the month - the prior month end
    after :func:`t_entry`; in that month the purchase payment itself in the issue month,
    which is where the payment falls, and the model point's :func:`av_pp_init` on a
    contract in force. On this product it is not "interest credited": it is the month's
    movement in a derivative price plus the Fixed and Holding Accounts' accrual, and at a
    Term End Date it also carries the index credit. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        opening = av_pp(t - 1)
    elif duration_mth(t) == 0:
        opening = premium_pp()
    else:
        opening = av_pp_init()
    return av_pp_at(t, BEF_WD) - opening


def free_wd_base(t):
    """AV_anniv(y): the Account Value at the most recent Contract Anniversary [S1][S2].

    Read **before** that month's transaction, which is the notes' step 5 - the snapshot is
    taken when the anniversary is reached and the withdrawal follows at step 6 - so an
    anniversary withdrawal is measured against a base that already includes that month's
    crediting. The anniversary at ``12 cy`` closes policy month ``12 cy - 1``, so the
    snapshot is that month's ``BEF_WD`` value, read at month
    ``12 cy - 1 - duration_mth_init()`` from the valuation date: from the frame where that
    month is :func:`t_entry` or later, and from the model point's
    :func:`av_pp_prev_anniv_init` where the anniversary precedes the valuation month.
    Before the first anniversary there is no snapshot and the base is the purchase
    payment; :func:`free_wd_allow` is zero there in any case. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    cy = duration_eom(t)
    if cy < 1:
        return premium_pp()
    m = 12 * cy - 1 - duration_mth_init()
    if m < t_entry():
        return av_pp_prev_anniv_init()
    return av_pp_at(m, BEF_WD)


def free_wd_allow(t):
    """The Free Withdrawal Amount for the contract year month t's month end falls in.

    Zero in contract year 1; thereafter 10% of the Account Value at the prior Contract
    Anniversary, non-cumulative - nothing carries across an anniversary. On a negative
    base it is negative, as in ``RILA_US_S``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if duration_eom(t) < 1:
        return 0.0
    return free_wd_rate * free_wd_base(t)                            # noqa: F821


def free_wd_avail(t):
    """FW(t): the unused free withdrawal allowance at month t, before that month's G.

    Reset to the whole allowance in the month that ends on a Contract Anniversary and
    carried forward within the contract year, reduced by amounts already withdrawn in it
    [S1][S2]: the month before's allowance less its free withdrawal,
    ``free_wd_avail(t - 1) - wd_free_pp(t - 1)``, which is ``RILA_US_S``'s
    ``free_wd_remain(t - 1)`` formed inline, so that the carry is one cell a month where
    ``RILA_US_S``'s runs through two. In the month the contract enters the books it is
    the model point's :func:`free_wd_remain_init`, which is 0 on a contract issued at or
    after the valuation date: its first month opens with nothing carried in. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if is_anniv(t):
        return free_wd_allow(t)
    if t > t_entry():
        return free_wd_avail(t - 1) - wd_free_pp(t - 1)
    return free_wd_remain_init()


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *withdrawal_table.csv*, else zero.

    The programme is a contractual schedule, keyed by the **policy** month end the
    withdrawal is taken at, so month ``t`` reads policy month end ``duration_mth(t) + 1``
    through :func:`wd_amount_pm`: the worked example's $8,000 at the 3-year point sits at
    month end 36 and is taken in policy month 35, whatever the valuation date. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    return wd_amount_pm(duration_mth(t) + 1)


def wd_amount_pm(m):
    """The gross withdrawal the model point's programme takes at policy month end ``m``.

    The withdrawal table's one reader, keyed by the policy month end:
    ``Data.wd_amount_array()[wd_schedule_number(), m]``, the programme's amount at ``m``,
    and 0.0 where it has no row there, as ``RILA_US_S``'s exact-key lookup answers it. A
    month below 0 or past ``Data.wd_last_mth()``, ``Data.read_last_mth``, the last the
    array holds, is refused, naming the point and the month: no programme withdraws
    before issue, and :func:`wd_scheduled_pp` calls it in cover only, at ``m`` 1 or more.
    """
    if m < 0 or m > data.wd_last_mth():                              # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: the withdrawal programme holds no month end {m}")
    return float(data.wd_amount_array()[wd_schedule_number(), m])    # noqa: F821


def wd_behavioral_pp(t):
    """The behavioural partial withdrawal at month t **[std]**.

    0% in contract year 1, the free amount being zero there [S1][S2]; thereafter
    ``wd_rate_ann`` of the Account Value taken at each Contract Anniversary and capped at
    the Free Withdrawal Amount, so the base run incurs no withdrawal charge. The
    anniversary closes policy month ``12y - 1``, and the first one that can bear a
    withdrawal is the end of policy month 11, where :func:`free_wd_allow` first turns
    positive. RMD-driven withdrawals for qualified cells are named in the notes as a
    behavioural input but no amount formula is given, so no RMD module is implemented.

    On a negative Account Value at the anniversary, which the interim value allows [S2],
    the Free Withdrawal Amount is a share of a negative base and so negative too, and
    ``min(rate x AV, allowance)`` takes the more negative of two negative amounts: a
    withdrawal below 0, which :func:`wd_pp` passes through. ``RILA_US_S`` computes the
    same, and this model, which is ``RILA_US_S`` run in force, keeps it. No shipped point's
    Account Value falls below 0.
    """
    if not is_anniv(t):
        return 0.0
    asked = wd_rate_ann() * av_pp_at(t, BEF_WD)                      # noqa: F821
    allowance = free_wd_allow(t)
    return min(asked, allowance)


def wd_pp(t):
    """G_total: the gross amount removed from the contract at month t, per contract.

    The scheduled programme plus the behavioural rule. Gross by construction: the
    withdrawal charge is deducted **from** the amount withdrawn and is not grossed up on
    this chassis [S1][S2], in contrast to [S4]. Capped at the Account Value **[std]** so a
    request larger than the contract cannot drive it negative; the contractual treatment
    of a request that would leave less than the $2,000 minimum - it becomes a full
    withdrawal [S1][S2] - is not implemented. On a negative Account Value the cap is 0,
    and a positive request takes nothing. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    total = wd_scheduled_pp(t) + wd_behavioral_pp(t)
    return min(total, max(0.0, av_pp_at(t, BEF_WD)))


def wd_free_pp(t):
    """The portion of G_total inside the Free Withdrawal Amount, free of charge [S1][S2].

    ``min(wd_pp(t), free_wd_avail(t))``, each operand bound to a local in that order, as
    ``RILA_US_S`` evaluates them: compiled, the two operands of a ``min`` are evaluated
    right to left, and the two can raise from different months.
    """
    wd = wd_pp(t)
    avail = free_wd_avail(t)
    return min(wd, avail)


def free_wd_remain(t):
    """The unused free withdrawal allowance after month t's withdrawal.

    This, not :func:`free_wd_avail`, is the allowance a full surrender at the end of month
    t can still shelter.
    """
    return free_wd_avail(t) - wd_free_pp(t)


def wd_excess_pp(t):
    """chargeable: ``max(0, G_total - FW(t))``, the amount exposed to the charge [S1][S2].
    """
    return max(0.0, wd_pp(t) - free_wd_avail(t))


def surr_charge_rate(t):
    """wc(cy): the withdrawal charge rate at month t's month end, by **complete** years.

    7, 7, 6, 5, 4, 3, 0 per cent [S1][S2], zero once the schedule runs out. Keyed on
    :func:`duration_eom`, the complete contract years at the instant the transaction
    settles, on the policy clock, through :func:`surr_charge_rate_at`. Contract year 7 -
    the first with a zero charge - is also the first year following a 6-year Term End
    Date on this chassis, which is why the charge-expiry shock lapse is applied there.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return surr_charge_rate_at(duration_eom(t))


def surr_charge_rate_at(cy):
    """The withdrawal charge rate of complete contract year ``cy``, from the table.

    The withdrawal charge table's one reader, keyed by the complete contract years at the
    month end: ``Data.surr_charge_array()[cy]`` for ``cy`` in ``0 .. n - 1``, where ``n``
    is ``Data.surr_charge_count()``, whose check holds the table's years to that run, and
    0.0 from ``n`` on, once the schedule has run out, as ``RILA_US_S`` reads a year the
    table lacks; 0.0 below 0 too, before the array is read. It asks the count first, so a
    projection meets the table's checks before it reads a rate. :func:`surr_charge_rate`
    calls it in cover only.
    """
    n = data.surr_charge_count()                                     # noqa: F821
    if cy < 0 or cy >= n:
        return 0.0
    return float(data.surr_charge_array()[cy])                       # noqa: F821


def wd_charge_pp(t):
    """WC(t): the withdrawal charge on month t's withdrawal, ``wc(cy) x chargeable``."""
    return surr_charge_rate(t) * wd_excess_pp(t)


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``G_total - WC(t)``.

    Not grossed up: the charge comes out of the amount withdrawn [S1][S2].
    """
    return wd_pp(t) - wd_charge_pp(t)


def wd_bucket_value_pp(t, bucket):
    """The value of one bucket at the allocation point, floored at zero.

    The flooring matters because the interim value can be negative [S2], and a negative
    weight in a pro-rata allocation is meaningless; a bucket at or below zero simply takes
    no share **[std]**.
    """
    if bucket == OPTION:
        return max(0.0, interim_value_pp_at(t, BEF_WD))
    elif bucket == FIXED:
        return max(0.0, fixed_acct_pp_at(t, BEF_WD))
    elif bucket == HOLDING:
        return max(0.0, holding_acct_pp_at(t, BEF_WD))
    else:
        raise ValueError("invalid bucket")


def wd_alloc_pp(t, bucket):
    """G_k: the part of G_total taken from one bucket, pro rata to value **[std]**.

    The notes prescribe allocation across open options **pro rata to interim value**,
    the prospectuses not prescribing an allocation for an unspecified withdrawal; with a
    Fixed and a Holding Account present the model extends the same rule to all three
    buckets. On a single-option model point with empty general accounts the whole
    withdrawal falls on the option.

    ``RILA_US_S`` adds the three buckets' values with Python's ``sum``, which CPython 3.12
    and later compensates on floats, Neumaier's way, so the loop here does the same over
    the codes ``OPTION``, ``FIXED`` and ``HOLDING``, 0 to 2, from ``0.0 +`` the first,
    adding the compensation once at the end where it is finite: ``RILA_US_S``'s double,
    where a running sum is not, once the Holding Account is not empty.
    """
    if wd_pp(t) <= 0.0:
        return 0.0
    total = 0.0
    comp = 0.0
    for b in range(3):
        x = wd_bucket_value_pp(t, b)
        added = total + x
        if abs(total) >= abs(x):
            comp = comp + ((total - added) + x)
        else:
            comp = comp + ((x - added) + total)
        total = added
    if comp != 0.0 and abs(comp) <= 1.7976931348623157e308:
        total = total + comp
    if total <= 0.0:
        return 0.0
    return wd_pp(t) * wd_bucket_value_pp(t, bucket) / total


def surr_excess_pp(t):
    """The part of the Account Value exposed to the charge on a full surrender [S1][S2]."""
    return max(0.0, av_pp(t) - free_wd_remain(t))


def surr_charge_pp(t):
    """The withdrawal charge on a full surrender at the end of month t."""
    return surr_charge_rate(t) * surr_excess_pp(t)


def surr_value_pp(t):
    """CSV(t): ``AV(t) - wc(cy) x max(0, AV(t) - FW(t))`` [S1][S2].

    The prospectus example reproduces here: a $100,000 payment with an $80,000 Account
    Value at the start of contract year 6 gives a free amount of $8,000, a chargeable
    $72,000, a 3% charge of $2,160 and a cash value of $77,840.
    """
    return av_pp(t) - surr_charge_pp(t)


def rop_pp(t):
    """ROP(t): the return-of-premium GMDB base at the **end** of month t, reduced
    **proportionally** [S1][S2].

    ``ROP(t+) = ROP(t-) x (1 - G_total / AV(t-))``, the ratio taken on the **gross** amount
    removed from the contract - including any withdrawal charge [S1] - and on the Account
    Value before the transaction. The base entering a contract's issue month is the
    purchase payment, which is where the guarantee starts; entering the valuation month on
    a contract in force it is the model point's :func:`rop_pp_init`. The opening is written
    inline, one cell a month back to :func:`t_entry`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        prior = rop_pp(t - 1)
    elif duration_mth(t) == 0:
        prior = premium_pp()
    else:
        prior = rop_pp_init()
    base = av_pp_at(t, BEF_WD)
    if base <= 0.0 or wd_pp(t) <= 0.0:
        return prior
    return prior * (1.0 - wd_pp(t) / base)


def death_ben_pp(t):
    """DB(t): ``max(AV(t), ROP(t))`` for issue ages 80 and under, ``AV(t)`` for 81+ [S2].

    The guarantee sits on top of a value that is itself a derivative price, so it is most
    in the money exactly when interim values are depressed: the guarantee and the account
    are not independent, and a deterministic run understates its cost.
    """
    if age_at_entry() <= db_rop_max_issue_age:                       # noqa: F821
        av = av_pp(t)
        rop = rop_pp(t)
        return max(av, rop)
    return av_pp(t)


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, times the A/E factor.

    The shipped table is an illustrative annuitant curve **[std]**, *not* a published
    basis. The notes prescribe the 2012 IAM **Basic** table (VM-M section 2.C) with
    generational Projection Scale G2 [REG-R59], which may not be redistributed here; swap
    it in by repointing ``Data.mort_table_file`` before the model computes anything. Do
    **not** run best-estimate mortality off the 2012 IAM *Period* table: it carries the
    valuation margin built in at construction, so a 100% A/E against it sets
    deferral-phase mortality roughly 10% below the unloaded basis [REG-R60].
    ``mort_ae_factor`` is 100% **[std]** - a placeholder, not a measurement, because public
    deferred-period annuitant mortality is thin [REG-R65] and the payout chassis's 108.4%
    is annuitant-select and deliberately not imported.

    The product is capped at 1, written ``min(q, 1.0)``, so that an A/E above 1 cannot
    carry a rate past certainty, and with the bound second a missing input, a NaN, stays
    NaN, where ``min(1.0, q)`` would read it as 1. No shipped point reaches the cap. The
    cap is ``RILA_US_S``'s. The table rate is read through :func:`mort_rate_base_at`, at
    the attained age on the policy clock. 0.0 outside cover, where no table is read.
    """
    if not is_active(t):
        return 0.0
    rate = mort_rate_base_at(age(t))
    return min(rate * mort_ae_factor, 1.0)                           # noqa: F821


def mort_rate_base_at(a):
    """The table's annual mortality rate at attained age ``a`` for the model point's sex.

    The mortality table's one reader, keyed by attained age, so that no per-month cell
    joins on the table: ``Data.mort_rate_array()[mort_schedule(), a]``, the point's sex's
    rate. An age outside the sex's, below its first or past its last, or past
    ``Data.mort_age_held()``, ``Data.read_last_age``, the last age the array holds, is
    refused, naming the point and the age, where ``RILA_US_S``'s ``.loc`` raised
    ``KeyError``: :func:`proj_len` refuses a point whose cover the table does not rate,
    and ``Data`` one whose first attained age it does not, so :func:`mort_rate` reads
    none. The parameter is ``a``, ``RILA_US_S``'s ``x``, so that no engine cell's
    parameter shares the name of a size ``spec_sec.py`` gives.
    """
    s = mort_schedule()
    if (a < data.mort_age_firsts()[s] or a > data.mort_age_lasts()[s]  # noqa: F821
            or a > data.mort_age_held()):                            # noqa: F821
        raise ValueError(
            f"point_id {point_id()}: the mortality table holds no rate at age {a}")
    return float(data.mort_rate_array()[s, a])                       # noqa: F821


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """w_base(y): the un-shocked annual surrender rate for the contract year **[std]**.

    2.0% through contract year 7 and 6.0% thereafter, read as a step function of the
    contract year :func:`policy_year`, on the policy clock, through
    :func:`lapse_rate_base_py`. A shape placeholder: the VA/RILA behaviour study [REG-R64]
    reports aggregate counts only and its detailed tables sit behind a paid data package.
    The shock enters separately as :func:`lapse_rate_sc_mult`, so the two are
    multiplicative and neither is baked into the other. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return lapse_rate_base_py(policy_year(t))


def lapse_rate_base_py(y):
    """The base annual surrender rate of contract year ``y``, the table's step function.

    The lapse table's one reader, keyed by contract year: the rate of the last
    ``contract_year`` at or before ``y``, found by a loop over ``Data``'s row vectors,
    ``Data.lapse_years`` and ``Data.lapse_rates``, the years compared by value as the table
    holds them, where ``RILA_US_S`` takes the ``max`` of a list. ``Data.lapse_table_count``
    holds the table's first year at 1, so every contract year has a rate; a ``y`` below
    every year, which :func:`lapse_rate_base` never passes, is refused, naming the point,
    where ``RILA_US_S``'s ``max()`` of an empty list raised. :func:`lapse_rate_base` calls
    it in cover only, at ``y`` 1 or more.
    """
    n = data.lapse_table_count()                                     # noqa: F821
    row = -1
    for i in range(n):
        if data.lapse_years()[i] <= y:                               # noqa: F821
            if row < 0 or data.lapse_years()[i] > data.lapse_years()[row]:  # noqa: F821
                row = i
    if row < 0:
        raise ValueError(
            f"point_id {point_id()}: the lapse table holds no rate at or before contract "
            f"year {y}")
    return float(data.lapse_rates()[row])                            # noqa: F821


def lapse_shock_year():
    """The contract year the withdrawal-charge-expiry surrender shock falls in.

    The first contract year with a zero withdrawal charge, derived from
    *surr_charge_table.csv* rather than hard-coded, so a different schedule moves the
    shock with it - the construction :mod:`.UL_US_S` uses. On the 7-7-6-5-4-3-0
    schedule that is contract year 7, which on this 6-year chassis is also the first year
    following a Term End Date [S1][S2]. The table's years run ``0 .. n - 1``, which
    ``Data.surr_charge_count`` checks, so an explicit loop over them reads
    ``Data.surr_charge_array`` and finds the first charge-free year where ``RILA_US_S``
    takes the ``min`` of a list; with none, it is the year after the schedule runs out,
    as there. It reads the array, not :func:`surr_charge_rate_at`, so that a table longer
    than that cell's cache never calls it past it.
    """
    n = data.surr_charge_count()                                     # noqa: F821
    for cy in range(n):
        if data.surr_charge_array()[cy] <= 0.0:                      # noqa: F821
            return cy + 1
    return n + 1


def lapse_rate_sc_mult(t):
    """M_sc(y): the charge-expiry shock multiplier, ``lapse_shock_mult`` = 3.0 **[std]**.

    Applied in :func:`lapse_shock_year` only, and 1.0 in every other contract year. The
    size is the scalar Reference ``lapse_shock_mult`` and the year is derived from the
    charge schedule, matching the universal-life chassis's Reference / Cells split.
    Contract year 7 is the first year with a zero withdrawal charge [S1][S2] **and** the
    first following a 6-year Term End Date - on this chassis the two coincide. The
    order-of-magnitude anchors from adjacent products are ~33% without a living-benefit
    rider and ~10% with one for FIA [REG-R62][REG-R63][unverified]; the representative
    RILA carries no living-benefit rider, which argues for the un-suppressed end, but the
    term structure offsets it, so the **[std]** shock is set well below that anchor. 1.0
    outside cover, its neutral value, so that no contract year the contract does not have
    is compared.
    """
    if not is_active(t):
        return 1.0
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def lapse_iv_mult(t):
    """M_iv(t): interim-value moneyness suppression, the RILA-specific effect **[std]**.

    ``min(1.0, max(0.25, V_k(t) / IA_k(t)))^2``, so a bucket at ``V/IA = 0.85`` carries a
    0.72 multiplier and one at or above par carries 1.0. Surrendering mid-term
    crystallizes the interim value, which is punitive when the option leg is out of the
    money [S1][S2], and a rational holder defers. It is exactly 1 at a Term End Date,
    where the interim value equals the Investment Amount, which is what makes the
    term-end concentration :func:`term_end_lapse_rate` the whole story there. 1.0 outside
    cover, its neutral value.
    """
    if not is_active(t):
        return 1.0
    m = min(1.0, max(iv_moneyness_floor, iv_ratio(t)))               # noqa: F821
    if 1.3407807929942596e154 < abs(m) <= 1.7976931348623157e308:
        raise OverflowError(
            f"point_id {point_id()}: lapse_iv_mult({t}), {m!r} squared, is past the "
            f"largest float")
    return m ** 2


def lapse_rate(t):
    """w_annual(y,t): the **annual** surrender rate, ``min(0.50, w_base x M_sc x M_iv)``.

    The 50% ceiling is a **[std] cap**, ``RILA_US_S``'s ``min`` with its bound first.
    ``lapse_rate`` is annual and :func:`lapse_rate_mth` is monthly, matching the
    ``mort_rate`` / ``mort_rate_mth`` pair; the decrement chain reads the monthly one.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return min(lapse_rate_max,                                       # noqa: F821
               lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_iv_mult(t))


def lapse_rate_mth(t):
    """w_m(t): the monthly background surrender rate, ``1 - (1 - w_annual)^(1/12)``.

    :func:`lapse_rate` is at most ``lapse_rate_max``, 0.5 as shipped, so the base is
    above 0. Set above 1, the Reference lets a rate past certainty through, whose base
    below 0 ``RILA_US_S`` takes the twelfth root of, a complex number: refused here,
    ``ValueError`` naming the point and the Reference, in both engines (the Space
    docstring's *Powers*).
    """
    b = 1.0 - lapse_rate(t)
    if b < 0.0:
        raise ValueError(
            f"point_id {point_id()}: lapse_rate_mth({t}): 1 - lapse_rate, {b!r}, is "
            f"below 0, lapse_rate_max being above 1, and its power 1 / 12 is no real "
            f"number")
    return 1.0 - b ** (1.0 / 12.0)


def term_end_lapse_rate(t):
    """phi: the discrete term-end surrender fraction **[std]**.

    10% when the withdrawal charge is zero and 3% otherwise, applied at each Term End Date
    **in addition** to the background monthly rate. During the Transfer Period the interim
    value equals the Investment Amount - no option adjustment [S2] - so the economic
    penalty for exiting vanishes for five days each term and surrenders concentrate there.
    A model that spreads surrenders uniformly across the term systematically over-collects
    the negative interim value adjustment.
    """
    if not is_term_end(t):
        return 0.0
    return (term_end_lapse_free if surr_charge_rate(t) <= 0.0        # noqa: F821
            else term_end_lapse_charged)                             # noqa: F821


def pols_if_at(t, timing):
    """In-force at month t read at the point given by ``timing``.

    The notes' order is death at ``q_m(t)``, then surrender at ``w_m(t)`` on survivors
    **[std order]**, plus the discrete term-end fraction ``phi``::

        l(t+1) = l(t) (1 - q_m(t)) (1 - w_m(t)) (1 - phi(t))

    The timings in processing order:

    ``BEF_NB``
        the count carried in from month t - 1, before month t's new business: the
        survivors of month t - 1's deaths and surrenders, out of month t - 1's
        ``BEF_DECR`` count. At :func:`t_entry`, the first month on the books, it is
        :func:`pols_if_init`, the count in force at the valuation date (0 for a point
        issued at or after it), and the recursion reads no earlier month. Zero outside
        cover, so the survivors of the last covered month leave as :func:`pols_maturity`.
    ``BEF_DECR``
        ``l(t)``, the start-of-month count: ``BEF_NB`` plus :func:`pols_new_biz`, before
        any decrement; :func:`pols_if` itself, and the weight on that month's cash flows.
    ``BEF_LAPSE``
        after deaths, ``l(t)(1 - q_m(t))``.
    ``BEF_TERM_SURR``
        after the background monthly surrender, ``l(t)(1 - q_m)(1 - w_m)``.
    ``AFT_DECR``
        after the discrete term-end surrender fraction ``phi``: the count at the month
        **end**, the notes' ``l(t+1)``, which in the last covered month is what
        :func:`pols_maturity` force-annuitizes out.

    ``BEF_NB`` and ``BEF_DECR`` are ``basiclife.BasicTerm_SE``'s names, and any timing
    but these five raises. ``BEF_NB`` forms the count left at the end of month t - 1
    itself - month t - 1's ``BEF_NB`` plus its :func:`pols_new_biz`, after its three
    decrements, the products ``AFT_DECR`` takes in the order it takes them - rather than
    calling for it. So the chain of calls from month t back to :func:`t_entry` is one
    cell a month, where ``RILA_US_S``'s runs through two. Every count is zero outside
    cover, before any rate is read.
    """
    if timing == BEF_NB:
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, BEF_NB) + pols_new_biz(t - 1))
                * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1))
                * (1.0 - term_end_lapse_rate(t - 1)))
    elif timing == BEF_DECR:
        return pols_if_at(t, BEF_NB) + pols_new_biz(t)
    elif timing == BEF_LAPSE or timing == BEF_TERM_SURR or timing == AFT_DECR:
        if not is_active(t):
            return 0.0
        pols = pols_if_at(t, BEF_DECR)
        pols = pols * (1.0 - mort_rate_mth(t))
        if timing == BEF_LAPSE:
            return pols
        pols = pols * (1.0 - lapse_rate_mth(t))
        if timing == BEF_TERM_SURR:
            return pols
        return pols * (1.0 - term_end_lapse_rate(t))
    raise ValueError("invalid timing")


def pols_if(t):
    """l(t): the number in force at the **start** of month t, the weight of row t.

    ``pols_if_at(t, BEF_DECR)``: the count carried in from month t - 1 plus month t's new
    business, before month t's decrements - the population that takes the month's
    withdrawal, carries its expenses and is exposed to its decrements, so it is the weight
    on every cash flow of the same :func:`result_cf` row, which reconciles against the row
    it sits on: ``premiums(t) / premium_pp()`` in the issue month, ``withdrawals(t) /
    wd_payment_pp(t)`` and ``expenses(t)`` over the per-contract maintenance charge all
    return it. On a point issued at ``t = 0`` it is exactly ``RILA_US_S``'s ``pols_if``. A
    point in force at the valuation date opens with :func:`pols_if_init`, and one issued
    at or after it with its issued count in the issue month. Zero outside cover: before
    issue, and from ``t = proj_len()`` on, because the survivors of the last covered month
    are force-annuitized out through :func:`pols_maturity`.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity. The count at the month **end**, the notes' ``l(t+1)``, is
    ``pols_if_at(t, AFT_DECR)``, which equals ``pols_if_at(t + 1, BEF_NB)`` in every
    month but the last covered one.
    """
    return pols_if_at(t, BEF_DECR)


def pols_new_biz(t):
    """Number of contracts issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point
    issued at the valuation date, ``t = k`` for one issued ``k`` months later. A point
    already in force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_death(t):
    """Deaths in month t, weighted ``l(t) q_m(t)``; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_DECR) * mort_rate_mth(t)


def pols_lapse_term(t):
    """The discrete term-end concentrated surrenders, non-zero only at a Term End Date.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_TERM_SURR) * term_end_lapse_rate(t)


def pols_lapse(t):
    """Full surrenders in month t: the background rate on survivors, plus ``phi``.

    Weighted ``l(t)(1 - q_m(t)) w_m(t)`` **[std timing]** for the background part. Both
    parts settle at the same cash surrender value, so they are one benefit line; the
    term-end part is broken out as :func:`pols_lapse_term` for diagnosis. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, BEF_LAPSE) * lapse_rate_mth(t) + pols_lapse_term(t)


def pols_maturity(t):
    """Forced annuitizations at the Maturity Date, non-zero only in the last month.

    The Maturity Date is the end of policy month ``maturity_mth() - 1``, the last month of
    the frame, ``t = proj_len() - 1``; the test is made on the policy clock. Not a
    decrement - the contract reaches its Maturity Date and must annuitize [S2] - but
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
    elif kind == MATURITY:
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def claim_pp(t, kind):
    """The benefit paid per contract in month t by ``kind``.

    ``DEATH`` is :func:`death_ben_pp`, ``max(AV, ROP)`` in the return-of-premium band
    [S2]. ``LAPSE`` is the cash surrender value :func:`surr_value_pp`. ``MATURITY`` is
    the Account Value, force-annuitized at the Maturity Date [S2]; converting it to a
    payment stream is the immediate-annuity chassis, restricted to the two forms this
    contract offers - and note that this contract offers **no refund forms**, so that
    branch of the chassis is unused.
    """
    if kind == DEATH:
        return death_ben_pp(t)
    elif kind == LAPSE:
        return surr_value_pp(t)
    elif kind == MATURITY:
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The Account Value released per contract by a claim of ``kind``.

    ``AV(t)`` for all three: decrements act at the end of the month on the post-transaction
    Account Value. It differs from :func:`claim_pp` by the withdrawal charge retained on a
    surrender and by any return-of-premium excess on a death claim; that difference is
    :func:`claims_over_av`.
    """
    if kind == DEATH or kind == LAPSE or kind == MATURITY:           # noqa: F821
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single purchase payment, at the opening of the issue month.

    The month with ``duration_mth(t) == 0`` [S1][S2], weighted by :func:`pols_new_biz`,
    the contracts issued there, so ``premiums(t) / premium_pp() == pols_if(t)`` in that
    month; none on a contract in force at the valuation date, whose payment was made
    before it.
    """
    return premium_pp() * pols_new_biz(t)


def prem_to_av_pp(t):
    """Premium credited to the Investment Amount per contract, in the issue month.

    There is no front-end load and no explicit asset-based charge on this chassis: the cap
    *is* the fee, and the margin appears as the spread between the earned rate and the
    option budget implied by the declared cap [S3][S4][S6]. The issue month is the one
    with ``duration_mth(t) == 0``.
    """
    return premium_pp() if duration_mth(t) == 0 else 0.0


def prem_to_av(t):
    """Premium credited to the block's Account Value, weighted by :func:`pols_new_biz`."""
    return prem_to_av_pp(t) * pols_new_biz(t)


def withdrawals(t):
    """Withdrawal payments in month t: ``(G_total - WC(t))`` weighted by :func:`pols_if`.

    The weight is the count entering month t - transactions are taken before the month's
    decrements - so ``withdrawals(t) / wd_payment_pp(t) == pols_if(t)``. The withdrawal
    charge is retained by the insurer, so it is not a cash flow of its own: it is the
    difference between the gross amount removed from the contract and the cash paid out.
    """
    return wd_payment_pp(t) * pols_if(t)


def claims(t, kind):
    """Benefit outgo in month t, for one ``kind`` or, with ``ALL``, all three.

    ``ALL`` is ``RILA_US_S``'s ``kind=None``: its total, the three kinds added with ``+``
    in its order, so that the sign of a zero total is ``RILA_US_S``'s too.
    """
    if kind == ALL:                                                  # noqa: F821
        return (claims(t, DEATH) + claims(t, LAPSE) + claims(t, MATURITY))  # noqa: F821
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The Account Value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind):
    """Benefit paid less the Account Value released, ``claims - claims_from_av``.

    Signed. Negative on a surrender inside the charge period, where the contract pays out
    less than the Account Value it releases; positive on a death claim where the
    return-of-premium guarantee bites. A reconciliation quantity, not a cash flow of its
    own. ``ALL`` is ``RILA_US_S``'s ``kind=None``, the three kinds added with ``+``, as
    :func:`claims` adds them.
    """
    if kind == ALL:                                                  # noqa: F821
        return (claims_over_av(t, DEATH) + claims_over_av(t, LAPSE)  # noqa: F821
                + claims_over_av(t, MATURITY))                       # noqa: F821
    return claims(t, kind) - claims_from_av(t, kind)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + inflation_rate) ** (t // 12)``.

    On the **valuation** clock: ``t`` counts months from the valuation date, so the
    maintenance charge it inflates is in valuation-date dollars, whatever the contract's
    age, and every point of a block inflates alike. ``RILA_US_S``'s annual step is kept,
    ``1.025^k`` from ``t = 12 k`` to ``12 k + 11``, but it falls every twelve months from
    the valuation date rather than on the contract's anniversaries. On a point issued at
    ``t = 0`` the two are the same; on the anchor cell in force 71 months this model's
    charge is ``RILA_US_S``'s divided by ``1.025^6``, or by ``1.025^5`` at
    ``t = 0, 12, 24, …``, where the valuation clock has stepped and the contract's
    anniversary is a month away. Defined in every month, before issue too: it is an input,
    not a state of the contract.
    """
    b = 1.0 + inflation_rate                                         # noqa: F821
    e = t // 12
    if (e != 0.0 and b != 0.0 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308
            and not (0.01 < abs(b) < 100.0 and abs(e) < 150.0)
            and e * float(math.log(abs(b))) > 709.7827128933845):    # noqa: F821
        raise OverflowError(
            f"point_id {point_id()}: inflation_factor({t}): {b!r} ** {e!r} is past "
            f"the largest float")
    p = b ** e
    if (abs(p) > 1.7976931348623157e308 and abs(b) <= 1.7976931348623157e308
            and abs(e) <= 1.7976931348623157e308):
        raise OverflowError(
            f"point_id {point_id()}: inflation_factor({t}): {b!r} ** {e!r} is past "
            f"the largest float")
    return p


def expenses(t):
    """Insurer expenses: acquisition at issue and inflating maintenance monthly **[std]**.

    ``0.06 x premium + 200`` at the opening of the issue month, ``duration_mth(t) == 0``,
    where the purchase payment falls, and ``60/12 x inflation_factor(t)`` per contract in
    every month including that one, weighted by :func:`pols_if` - the count entering the
    month, since the expense is incurred over it. The issue month therefore carries both
    lines, and the acquisition is per contract issued. The notes' ledger carries no
    separate commission line - distribution cost sits inside the acquisition expense - so
    this model has no ``commissions`` cells. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    acq = (expense_acq_rate * premium_pp()                           # noqa: F821
           + expense_acq_fixed) if duration_mth(t) == 0 else 0.0     # noqa: F821
    return (acq + (expense_maint / 12.0)                             # noqa: F821
            * inflation_factor(t)) * pols_if(t)


def premium_taxes(t):
    """Premium tax on the purchase payment, 0% **[std]** [S2].

    State-specific and not quantified in any retrieved document; the parameter is exposed
    rather than removed.
    """
    return premium_tax_rate * premiums(t)                            # noqa: F821


def net_cf(t):
    """Net cash flow in month t from the valuation date.

    Term-end index credits, the movement of the interim value, the withdrawal charge and
    the roll split between the option and the general accounts are **internal accounting
    entries**: they drive the Investment Amount, the Account Value and the benefit
    *amount*, but are never ledger lines. The option budget is not a liability cash flow
    at all - it is an asset-side flow, and the liability model sees it only through the
    declared cap. Only amounts paid to or received from the contract holder, and the
    insurer's own expenses, in valuation-date dollars, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t, ALL)            # noqa: F821
            - expenses(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted Account Value at month t; ``timing`` as in :func:`av_pp_at`.

    ``BEF_WD`` carries :func:`pols_if`, the count entering month ``t``. ``AFT_WD``
    carries the count *leaving* it, which under the start-of-period convention is
    ``pols_if_at(t + 1, BEF_NB)``, the count carried into the next month before its new
    business - zero in the last month, where :func:`pols_maturity` has force-annuitized
    the survivors out and the block's Account Value is released in full. ``AFT_WD`` is
    zero outside cover, before it reads ``t + 1``, so that at ``t = proj_len()``, the month
    after cover, nothing reads the count a month past the frame.
    """
    if timing == BEF_WD:
        return av_pp_at(t, BEF_WD) * pols_if(t)
    elif timing == AFT_WD:
        if not is_active(t):
            return 0.0
        return av_pp(t) * pols_if_at(t + 1, BEF_NB)
    else:
        raise ValueError("invalid timing")


def inv_income(t):
    """The investment return credited to the whole block in month t."""
    return inv_income_pp(t) * pols_if(t)


def wd_from_av(t):
    """The Account Value released by month t's withdrawals, gross of the charge."""
    return wd_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's Account Value over month t.

    After :func:`t_entry`, the month before's close; in that month, the block's opening
    state, ``av_pp_init() x pols_if_init()``, which is nothing on a contract issued at or
    after the valuation date: its purchase payment arrives inside the issue month, as
    :func:`prem_to_av`.
    """
    opening = av_at(t - 1, AFT_WD) if t > t_entry() else av_pp_init() * pols_if_init()
    return av_at(t, AFT_WD) - opening


def roll_fwd_tol():
    """The absolute tolerance the ``check_*`` booleans hold a currency residual to.

    One part in a billion of the purchase payment. The roll-forward identities are
    differences of Account Values of that size, and the option pricer's own rounding sits
    well inside it; a genuine wiring error is orders of magnitude larger.
    """
    return 1e-9 * max(1.0, premium_pp())


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual; zero to floating point in every month.

    ``AV(t) - AV(t-1) = premium in - withdrawals out + investment return - the Account
    Value released by each of the three claim kinds``. The *cash* paid can differ from the
    Account Value released - by the withdrawal charge retained on a surrender and by the
    return-of-premium excess on a death claim - and that difference is
    :func:`claims_over_av`, not part of this identity. The month a contract enters the
    books is included: issued then, the block opens at nothing, the purchase payment
    arrives as :func:`prem_to_av`, and the identity closes on it like any other month; in
    force at the valuation date, it opens at its opening state (:func:`av_change`).

    The signed per-month residual, which is what a failing :func:`check_av_roll_fwd` needs
    for diagnosis; the boolean is implemented in terms of it.
    """
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - claims_from_av(t, DEATH) - claims_from_av(t, LAPSE)
                - claims_from_av(t, MATURITY))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the account value roll-forward closes in **every** projected month.

    No argument and a bool, following ``CashValue_SE.check_av_roll_fwd`` and the rest of
    this library, so one test can call the same check across every model;
    :func:`check_av_roll_fwd_resid` gives the signed residual of a month that fails. The
    residual is an aggregate over the point's contracts, so the tolerance is
    :func:`roll_fwd_tol` times ``max(policy_count(), 1)``: on a point counting one
    contract it is ``RILA_US_S``'s. ``RILA_US_S``'s ``all`` is kept, so a residual that
    is not a number fails the check.
    """
    tol = roll_fwd_tol() * max(policy_count(), 1.0)
    return all(abs(check_av_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual; zero to floating point in every month.

    ``pols_if(t) - pols_if_at(t + 1, BEF_NB) = deaths + surrenders + forced
    annuitizations at the Maturity Date``: the start-of-month count opens the row, the
    exits are taken during it, and the next month opens on what is left, before its own
    new business, which is no part of month t's movement. Zero outside cover, before
    ``t + 1`` is read, so that at ``t = proj_len()``, the month after cover, nothing reads
    the count a month past the frame.
    """
    if not is_active(t):
        return 0.0
    return (pols_if(t) - pols_if_at(t + 1, BEF_NB) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in **every** projected month.

    No argument and a bool; :func:`check_pols_roll_fwd_resid` gives the signed residual.
    The counts are probabilities of order 1 per contract, so the tolerance is absolute
    rather than the currency-scaled :func:`roll_fwd_tol`, ``1e-12`` times
    ``max(policy_count(), 1)``, scaling with the count as the residual does. On a point
    counting one contract it is ``RILA_US_S``'s ``1e-12``. ``RILA_US_S``'s ``all`` is kept,
    so a residual that is not a number fails the check.
    """
    tol = 1e-12 * max(policy_count(), 1.0)
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_term_end_identity_resid(t):
    """The notes' term-end verification identity, ``V_k = IA_k(1 + g)``; zero everywhere.

    At ``tau = 0`` the replicating portfolio collapses to intrinsic value and must
    reproduce the crediting rate exactly. If this is not zero to the cent, the strike set,
    the notional convention, the buffer sign - or a trading cost provision left switched on
    at ``tau = 0`` - is wrong. Zero by construction outside a Term End Date, where the
    identity does not apply.
    """
    if not is_term_end(t):
        return 0.0
    return (interim_value_pp_at(t, BEF_ROLL)
            - inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t)))


def check_term_end_identity():
    """True when ``V_k = IA_k(1 + g)`` holds at **every** Term End Date.

    No argument and a bool, like the two roll-forward checks;
    :func:`check_term_end_identity_resid` gives the signed residual of a term end that
    fails. This is the check the notes ask for by name.
    """
    return all(abs(check_term_end_identity_resid(t)) <= roll_fwd_tol()
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, indexed by month ``t`` from the valuation date.

    The frame is ``t = 0 ... proj_len() - 1``, and row ``t`` is the same month for every
    model point, so the frames of a block sum row by row. A contract issued at or after
    the valuation date carries its purchase payment and acquisition expense in its issue
    month - they fall at its opening, which is the Issue Date - as well as that month's
    own maintenance expense and decrements, and zeros in every month before it. The
    surrender column is ``claims_lapse``, matching the ``LAPSE`` ``kind`` that produces
    it, and partial withdrawals sit in their own ``withdrawals`` column rather than among
    the claims - a withdrawal is a payment on the owner's election, not a claim. The cash
    flow columns sum to ``net_cf`` under the income-positive sign convention:
    ``premiums`` less every other flow. The columns are ``RILA_US_S``'s.

    ``pols_if`` is the count in force at the **start** of each month, so it is the weight
    the cash flows on that same row carry - the column and the row reconcile.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, DEATH) for t in ts],
            "claims_lapse": [claims(t, LAPSE) for t in ts],
            "claims_maturity": [claims(t, MATURITY) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed ``t = 0 ... proj_len() - 1``.

    ``pols_if`` opens the month, ``pols_new_biz`` is the contracts issued in it, the four
    movement columns are what leaves it, and ``pols_if_aft_decr`` is the count at the
    month end, the notes' ``l(t+1)`` - after death, surrender and the term-end
    concentration, but before the Maturity Date annuitization that ``pols_maturity``
    carries out. ``RILA_US_S``'s columns, with ``pols_new_biz`` after ``pols_if``, as
    ``basiclife.BasicTerm_SE``'s report carries it; zeros before issue.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_lapse_term": [pols_lapse_term(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, AFT_DECR) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract values, indexed ``t = 0 ... proj_len() - 1``.

    The Investment Amount and Interim Value either side of the month's transaction, the
    Account Value, the general accounts, the return-of-premium base and the surrender and
    death benefits; zeros before issue.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "inv_amt_pp": [inv_amt_pp(t) for t in ts],
            "interim_value_pp": [interim_value_pp_at(t, AFT_WD) for t in ts],
            "fixed_acct_pp": [fixed_acct_pp(t) for t in ts],
            "holding_acct_pp": [holding_acct_pp(t) for t in ts],
            "av_pp_bef_wd": [av_pp_at(t, BEF_WD) for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "rop_pp": [rop_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "surr_value_pp": [surr_value_pp(t) for t in ts],
            "death_ben_pp": [death_ben_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_iv():
    """The interim value decomposition, one row per month - the worked example's table.

    Index level, index performance, the fixed income asset proxy, one column per
    replicating-portfolio leg, the derivative asset proxy, the trading cost, the interim
    value and the Investment Amount, each measured before the roll split so the columns
    line up with the notes. Indexed ``t = 0 ... proj_len() - 1``; before issue every
    column is 0.0, the index level included, which no market path is read for there. The
    legs are :func:`opt_leg`'s, in ``RILA_US_S``'s order, each column named as
    ``RILA_US_S`` names it, its leg's name in lower case.
    """
    names = ("atm_call", "otm_call", "otm_put", "atm_put", "floor_put", "step_binary",
             "edge_binary")
    ts = list(range(proj_len()))
    out = {
        "index_level": [index_level(t) if is_active(t) else 0.0 for t in ts],
        "index_perf": [index_perf(t) for t in ts],
        "tau": [tau(t) for t in ts],
        "fixed_proxy_pp": [fixed_proxy_pp(t, BEF_ROLL) for t in ts],
    }
    for i in range(opt_leg_count()):
        leg = opt_leg(i)
        out[names[leg]] = [opt_component_pp(t, leg, BEF_ROLL) for t in ts]
    out["deriv_proxy_pp"] = [deriv_proxy_pp(t, BEF_ROLL) for t in ts]
    out["trading_cost_pp"] = [trading_cost_pp(t, BEF_ROLL) for t in ts]
    out["interim_value_pp"] = [interim_value_pp_at(t, BEF_ROLL) for t in ts]
    out["inv_amt_pp"] = [inv_amt_pp_at(t, BEF_ROLL) for t in ts]
    return pd.DataFrame(out, index=pd.Index(ts, name="t"))           # noqa: F821


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

idx = 0

issue_age_min = 0

issue_age_max = 111

maturity_age = 90

maturity_min_years = 10

free_wd_rate = 0.1

trading_cost_rate = 0.001

iv_credit_spread = 0.01

iv_expense_rate = 0.001

earned_rate = 0.04

nge_spread = 0.0222

nge_cap_search_max = 5.0

nge_solve_iter = 80

declared_acct_rate = 0.03

guar_min_acct_rate = 0.01

roll_renew_same = 0.8

roll_transfer_other = 0.05

roll_transfer_fixed = 0.15

roll_transfer_holding = 0.0

db_rop_max_issue_age = 80

mort_ae_factor = 1.0

iv_moneyness_floor = 0.25

lapse_shock_mult = 3.0

lapse_rate_max = 0.5

term_end_lapse_free = 0.1

term_end_lapse_charged = 0.03

expense_acq_rate = 0.06

expense_acq_fixed = 200.0

expense_maint = 60.0

inflation_rate = 0.025

premium_tax_rate = 0.0

BEF_NB = 0

BEF_DECR = 1

BEF_LAPSE = 2

BEF_TERM_SURR = 3

AFT_DECR = 4

BEF_CREDIT = 5

BEF_ROLL = 6

BEF_WD = 7

AFT_WD = 8

DEATH = 0

LAPSE = 1

MATURITY = 2

ALL = 3

CAP = 4

STEP = 5

EDGE = 6

OPTION = 0

FIXED = 1

HOLDING = 2

ATM_CALL = 0

OTM_CALL = 1

OTM_PUT = 2

ATM_PUT = 3

FLOOR_PUT = 4

STEP_BINARY = 5

EDGE_BINARY = 6

CURRENT = 0

TERM_START = 1

UPDATED_EXPIRY = 2

INDEX_LEVEL = 0

MVR = 1

RISK_FREE = 2

DIV_YIELD = 3

IMPL_VOL = 4

TERM_END = 0

PRORATED = 1

math = ("Module", "math")

pd = ("Module", "pandas")