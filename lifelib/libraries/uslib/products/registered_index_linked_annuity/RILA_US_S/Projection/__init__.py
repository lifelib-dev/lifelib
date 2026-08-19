# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-contract projection of :mod:`~.RILA_US_S`.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_iv()          # the worked example's own table
    >>> Projection[1].result_cf()
    >>> Projection.point_id = 2            # or switch the default

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/registered_index_linked_annuity/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an input
can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RILA_US_S`` folder without its parent's CSVs produces a model that
reads and then fails on first evaluation.

The readers and the filename References live on the sibling
:mod:`~.RILA_US_S.Data` Space, reached here through the ``data``
Reference, so each file is read once per model rather than once per model point:

=========================  ==================================  ==========================
Reference (on Data)        Cells                               File
=========================  ==================================  ==========================
model_point_file           data.model_point_table()            model_point_table.csv
mort_table_file            data.mort_table()                   mort_table.csv
market_scenario_file       data.market_scenario()              market_scenario.csv
surr_charge_file           data.surr_charge_table()            surr_charge_table.csv
guar_min_rate_file         data.guar_min_rate_table()          guar_min_rate_table.csv
lapse_file                 data.lapse_table()                  lapse_table.csv
withdrawal_file            data.withdrawal_table()             withdrawal_table.csv
=========================  ==================================  ==========================

``market_scenario`` is the input class peculiar to this product: the *contractual* formula
consumes market data, so the index level, the Market Value Rate, the risk-free rate, the
dividend yield and the implied volatility are inputs on the same footing as the
withdrawal-charge schedule, not a valuation overlay.

.. rubric:: Projection basis

``t`` counts **policy months** and, following the notes, denotes **month ends**, with
``t = 0`` the Issue Date. Complete contract years are ``duration(t) = t // 12`` — the
notes' ``cy(t) = floor(t/12)`` — so the anniversary month itself already counts as a
completed year, and ``policy_year(t) = duration(t) + 1``. This differs by one step from
:mod:`.MYGA_US_S`, whose beginning-of-month transaction convention puts the
anniversary month in the year that is opening rather than the one that has just closed;
each convention is the right one for its own timing basis, and the divergence is visible
only in the anniversary month.

**A month-end index has two readings of "the contract year", and the model carries
both.** ``duration(t) = t // 12`` is the *instant* reading: how many complete contract
years have elapsed **at** the month end ``t``. It is the right one for anything read at
that instant — the withdrawal charge a transaction settling at ``t`` bears
(:func:`surr_charge_rate`), the free-withdrawal base snapshotted there
(:func:`free_wd_base`), and the surrender behaviour keyed to that charge
(:func:`lapse_rate_sc_mult`, :func:`lapse_rate_base`), which must see the charge expire in
the same month the contract does. ``duration_bom(t) = ceil(t/12) - 1`` is the *interval*
reading: the complete contract years at the **start** of month ``t``, i.e. the contract
year the interval ``(t-1, t]`` lies inside. It is the right one for a rate that applies
across the whole of month ``t`` — the attained age behind ``q_m(t)`` (:func:`age`) and the
expense inflation step ``1.025^(y-1)`` (:func:`inflation_factor`). The two differ **only
in anniversary months**: ``duration(12) = 1`` but ``duration_bom(12) = 0``, so month 12
bears the age-``x`` mortality rate and the year-1 expense level while a surrender in it
already settles on the year-2 side of the charge schedule.

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

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``, and
this library's deferred annuity chassis :mod:`.MYGA_US_S`, wherever those have
an analogue — ``pols_*`` for policy counts, ``av_*`` for account values, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-contract amounts, ``*_at(t, timing)``
for a quantity read at a point inside the month. The technical notes use compact
actuarial symbols instead. The mapping is:

============================  ================================  ==============================
Notes symbol                  Cells                             Meaning
============================  ================================  ==============================
t                             duration_mth(t)                   Elapsed policy months
cy(t) = floor(t/12)           duration(t)                       Complete contract years at t
cy(t) + 1                     policy_year(t)                    Contract year in force at t
ceil(t/12) - 1                duration_bom(t)                   Complete years during month t
x                             age_at_entry                      Issue age (ANB)
x + ceil(t/12) - 1            age(t)                            Attained age (ANB) during t
(Maturity Date)               policy_term                       Years from issue to maturity
(none)                        proj_len                          Last projection month
P                             premium_pp                        Single purchase payment
T                             term_years                        Index-linked term in years
(Term Start Date)             term_start_month(t)               Month the option in force began
(none)                        term_elapsed_mth(t)               Months elapsed in that term
(Term End Date)               is_term_end(t)                    True when t ends a term
tau_k(t)                      tau(t)                            Years remaining in the term
I(t)                          index_level(t)                    Index level
I_s                           index_at_term_start(t)            Index level at the Term Start
R_k(t)                        index_perf(t)                     I(t)/I_s - 1
r(t)                          mvr(t)                            Market Value Rate (CMT)
r_0                           mvr_at_term_start(t)              Market Value Rate at term start
(r, q, sigma)                 risk_free(t), div_yield(t),       Option-pricing market state
                              impl_vol(t)
N(.)                          norm_cdf(x)                       Standard normal c.d.f.
d1, d2                        bs_d1(...), bs_d2(...)            Black-Scholes arguments
C(I,K,tau)                    bs_call(...)                      European call
P(I,K,tau)                    bs_put(...)                       European put
BC(I,K,tau)                   bs_binary_call(...)               Cash-or-nothing binary call
b                             buffer                            Buffer
c, s, e (model point)         declared_cap, declared_step,      Rates declared on the model point
                              declared_edge
c                             cap_rate(t)                       Cap Rate in force, floored
s                             step_rate(t)                      Step Rate in force, floored
e                             edge_rate(t)                      Edge Rate in force, floored
PR                            participation                     Participation Rate
f                             floor_rate                        Floor (optional module)
guar_min_cap(T)               guar_min_rate(kind)               Contractual minimum by term
(one option leg)              opt_component(t, leg, ...)        Signed per-unit leg value
(the leg set)                 opt_legs()                        Legs of the replicating set
Pi(I, tau)                    opt_portfolio(t, spot, tau, mkt)  Per-unit portfolio value
(sum of \|legs\|)               opt_portfolio_abs(...)            Trading-cost assessment base
beta                          opt_budget(t)                     Initial option budget
y_e, spread                   earned_rate, nge_spread           Earned rate; target margin [std]
beta_target(T)                opt_budget_target()               NGE cap-solve target
(the cap solve)               declared_cap_solved(t)            Cap solving Pi = beta_target
g                             credit_rate_term(t)               Term-end crediting rate
AccruedCapRate                credit_rate_accrued(t)            Pre-AG 54 time-prorated rate
B_k(t)                        budget_amort_pp(t)                Amortized initial budget
F_k(t)                        fixed_proxy_pp(t)                 Fixed Income Asset Proxy
D_k(t)                        deriv_proxy_pp(t)                 Derivative Asset Proxy
TC_k(t)                       trading_cost_pp(t)                Trading cost provision
kappa                         trading_cost_rate                 Trading cost factor
[(1+r_0)/(1+r(t))]^tau        mva_factor(t)                     Interim-value rate adjustment
CCF_k(t)                      cap_calc_factor(t)                Cap Calculation Factor, family (b)
E_0                           iv_expense_rate                   CCF expense rate [std], family (b)
rate(t), family (b)           risk_free(t) + iv_credit_spread   Investment-grade discount rate
DailyAdjustment(t)            fixed_proxy_factor(t),            Family (c), the delta form
                              deriv_proxy_factor(t)
V_k(t)                        interim_value_pp_at(t, timing)    Interim Value
V_k(t)/IA_k(t)                iv_ratio(t)                       Interim Value per unit of base
(the decomposition base)      iv_notional_pp(t, timing)         Notional a component sits on
IA_k(t)                       inv_amt_pp(t)                     Investment Amount
IA_k(t) inside the month      inv_amt_pp_at(t, timing)          BEF_CREDIT/BEF_ROLL/BEF_WD/AFT_WD
FA(t)                         fixed_acct_pp(t)                  Fixed Account value
HA(t)                         holding_acct_pp(t)                Holding Account value
i_declared                    acct_rate()                       Declared rate on FA and HA
AV(t)                         av_pp(t), av_pp_at(t, timing)     Account Value
l(t) x AV(t)                  av_at(t, timing)                  In-force weighted Account Value
ROP(t)                        rop_pp(t)                         Return-of-premium GMDB base
DB(t)                         death_ben_pp(t)                   Death benefit
CSV(t)                        surr_value_pp(t)                  Cash surrender value
AV_anniv(y)                   free_wd_base(t)                   Account Value at the anniversary
0.10 x AV_anniv(y)            free_wd_allow(t)                  Free Withdrawal Amount
FW(t)                         free_wd_avail(t)                  Allowance before the withdrawal
FW(t) after the withdrawal    free_wd_remain(t)                 Allowance a surrender can shelter
FW_used(y)                    free_wd_avail/free_wd_remain      Consumed amount, as its complement
G_total                       wd_pp(t)                          Gross amount removed
G_k                           wd_alloc_pp(t, bucket)            Amount taken from one bucket
(free part of G)              wd_free_pp(t)                     Portion inside the free amount
chargeable                    wd_excess_pp(t)                   Amount exposed to the charge
wc(cy)                        surr_charge_rate(t)               Withdrawal charge rate
WC(t)                         wd_charge_pp(t)                   Withdrawal charge
net proceeds                  wd_payment_pp(t)                  Cash paid on the withdrawal
chargeable on a surrender     surr_excess_pp(t)                 AV(t) less the free amount
wc x chargeable               surr_charge_pp(t)                 Charge on a full surrender
q_m(t)                        mort_rate_mth(t)                  Monthly mortality rate
(annual q_x)                  mort_rate(t)                      Annual mortality rate
w_base(y)                     lapse_rate_base(t)                Un-shocked annual surrender rate
M_sc(y)                       lapse_rate_sc_mult(t),            Charge-expiry shock multiplier
                              lapse_shock_mult                  and its **[std]** size, 3.0
(the shock year)              lapse_shock_year()                First charge-free contract year
M_iv(t)                       lapse_iv_mult(t)                  Moneyness suppression
w_annual(y,t)                 lapse_rate(t)                     Total annual surrender rate
w_m(t)                        lapse_rate_mth(t)                 Monthly surrender rate
phi                           term_end_lapse_rate(t)            Term-end surrender concentration
l(t-1)                        pols_if(t)                        In-force at the start of month t
l(0)                          pols_if_init                      In-force at issue
l(t)                          pols_if_at(t, timing)             BEF_DECR/BEF_LAPSE/BEF_TERM_SURR/AFT_DECR
l(t-1) q_m                    pols_death(t)                     Deaths
l(t-1)(1-q_m) w_m + phi       pols_lapse(t)                     Full surrenders
(the phi part)                pols_lapse_term(t)                Term-end concentrated surrenders
(none)                        pols_maturity(t)                  Forced annuitizations at maturity
P at t = 0                    premiums(t)                       Premium income
(premium credited)            prem_to_av_pp(t), prem_to_av(t)   Premium credited to the base
G_total - WC(t)               withdrawals(t)                    Withdrawal payments
(ledger benefit lines)        claims(t, kind)                   Benefit outgo by kind
                              claim_pp(t, kind)                 Benefit per contract by kind
                              claims_from_av(t, kind)           Account Value released
                              claims_over_av(t, kind)           Benefit paid above the AV
(investment return)           inv_income_pp(t), inv_income(t)   Return credited to the AV
(acquisition; maintenance)    expenses(t)                       0.06 P + 200; 60/12 x 1.025^(y-1)
1.025^(y-1)                   inflation_factor(t)               Maintenance expense inflation
premium tax                   premium_taxes(t)                  Premium tax, 0% [std]
NetCF(t)                      net_cf(t)                         Net cash flow
============================  ================================  ==============================

.. rubric:: Names that needed care

The notes reuse single letters across three different vocabularies — contract mechanics,
Black-Scholes and the deferred annuity chassis — and the collisions are real.

``T`` is the term length in **years** while ``t`` is the policy **month**, so it becomes
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

``"BEF_CREDIT"``
    ``IA_k(t-1)``, the notional the month-``t`` valuation applies to. At ``t = 0`` it is
    the premium allocated to the option.
``"BEF_ROLL"``
    after term-end crediting, ``IA(1 + g)`` at a Term End Date and unchanged otherwise.
    This is the worked example's **Investment Amount** column.
``"BEF_WD"``
    after the renewal / transfer roll split, so ``roll_index_share`` of ``"BEF_ROLL"`` at
    a Term End Date and unchanged otherwise.
``"AFT_WD"``
    after the proportional withdrawal reduction. Equal to :func:`inv_amt_pp`.

Interim Value, ``interim_value_pp_at(t, timing)``, takes the same three of those points —
``"BEF_ROLL"``, ``"BEF_WD"``, ``"AFT_WD"`` — and is in each case the Investment Amount at
that point multiplied by :func:`iv_ratio`. ``"BEF_ROLL"`` is the worked example's
**Interim value** column.

The currency decomposition of that value — :func:`fixed_proxy_pp`,
:func:`opt_component_pp`, :func:`deriv_proxy_pp`, :func:`trading_cost_pp` and
:func:`budget_amort_pp` — takes two of them, ``"BEF_ROLL"`` (the default) and
``"AFT_WD"``, through :func:`iv_notional_pp`. That pair is what the worked example's rows
B1 and B2 are: the same month, the same market state, the decomposition before and after
an $8,000 withdrawal, every component scaled by one factor.

Account Value, ``av_pp_at(t, timing)``, following ``CashValue_SE``'s ``av_pp_at``:

``"BEF_WD"``
    ``AV(t)`` as the notes' step 5 leaves it — after crediting, the roll split, the
    interim value and the account accruals, before any transaction. This is the value the
    free-withdrawal base is snapshotted from and the base the withdrawal is allocated
    across.
``"AFT_WD"``
    after the transaction; equal to :func:`av_pp`, and the value every decrement benefit
    is measured on.

Policy counts, ``pols_if_at(t, timing)``, following ``CashValue_SE``'s ``pols_if_at``:

``"BEF_DECR"``
    ``l(t-1)``, in force at the **start** of month ``t``; equal to :func:`pols_if`.
``"BEF_LAPSE"``
    after deaths, ``l(t-1)(1 - q_m(t))``.
``"BEF_TERM_SURR"``
    after the background monthly surrender, ``l(t-1)(1 - q_m)(1 - w_m)``.
``"AFT_DECR"``
    after the discrete term-end surrender fraction ``phi``. This is the notes' own
    **end**-of-month ``l(t)``: :func:`pols_if` carries the start-of-month count, so the
    notes' quantity lives here and nowhere else.

Benefit ``kind`` arguments are ``"DEATH"``, ``"LAPSE"`` and ``"MATURITY"``. Withdrawal
allocation ``bucket`` arguments are ``"OPTION"``, ``"FIXED"`` and ``"HOLDING"``. Option
``leg`` arguments are ``"ATM_CALL"``, ``"OTM_CALL"``, ``"OTM_PUT"``, ``"ATM_PUT"``,
``"FLOOR_PUT"``, ``"STEP_BINARY"`` and ``"EDGE_BINARY"``. Market-state ``mkt`` arguments
are ``"CURRENT"`` and ``"TERM_START"``. Any other value of any of these raises
``ValueError``.

There is no ``"ANNUITIZATION"`` kind. The notes give no elective annuitization take-up
for this product; the only annuitization modelled is the **forced** one at the Maturity
Date, which is ``"MATURITY"``.

.. rubric:: pols_maturity and the Maturity Date

Unlike the deferred annuity chassis, this product's horizon is contractual rather than
chosen: the Maturity Date is the later of the anniversary after the oldest owner's 90th
birthday and ten years from issue [S2], so ``policy_term()`` is
``max(90 - age_at_entry(), 10)`` years and ``proj_len()`` is twelve times that — 360
months on the anchor cell. At that month the contract force-annuitizes at the Account
Value, and :func:`pols_maturity` carries the survivors out so that

    pols_if(t) - pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)

closes for every ``t``, including the last — ``pols_if(t)`` opening month ``t`` and
``pols_if(t+1)`` opening the next, which at the Maturity Date is zero. The name follows
``BasicTerm_S.pols_maturity``
and the construction follows :mod:`.Term_US_A` and :mod:`.MYGA_US_S`. The
payout stream bought at that date is not derived here: it is the immediate-annuity
chassis, restricted to the two forms this contract offers [S2].
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The contract identifier of the selected model point."""
    return model_point()["policy_id"]


def age_at_entry():
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point, M or F."""
    return model_point()["sex"]


def premium_pp():
    """P: the single purchase payment per contract; no subsequent payments [S1][S2]."""
    return float(model_point()["premium"])


def pols_if_init():
    """l(0): in-force probability at issue, 1 for a single-contract model point."""
    return float(model_point()["pols_if_init"])


def term_years():
    """T: the index-linked term in years, from the 1 / 3 / 6 menu [S1][S2]."""
    return int(model_point()["term_years"])


def buffer():
    """b: the buffer, guaranteed for the life of each term [S1][S2].

    The buffer absorbs the first ``b`` of index loss and passes the excess through; 10% is
    the one level present in every retrieved insurer's menu [S1]-[S6].
    """
    return float(model_point()["buffer"])


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
    return float(model_point()["declared_cap"])


def declared_step():
    """s: the declared Step Rate, 8% **[std]**; observed illustrative 8% [S1]."""
    return float(model_point()["declared_step"])


def declared_edge():
    """e: the declared Edge Rate, 6% **[std]**.

    No Edge value appears in any retrieved document; 6% is set below the 8% Step because
    the Edge design pays down to -b rather than to 0 and so buys a lower rate.
    """
    return float(model_point()["declared_edge"])


def participation():
    """PR: the Participation Rate, 100% [S4].

    At ``PR = 1`` the notes' BUFFER + CAP + PR portfolio collapses **exactly** to the
    BUFFER + CAP one, so a single branch serves both; see :func:`opt_component`.
    """
    return float(model_point()["participation"])


def floor_rate():
    """f: the floor for the ``FLOOR`` crediting module, a positive fraction [S5]."""
    return float(model_point()["floor_rate"])


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
    return bool(model_point()["nge_reset"])


def wd_rate_ann():
    """The behavioural partial-withdrawal rate, 2% of Account Value a year **[std]**.

    Zero in contract year 1 because the free amount is zero there [S1][S2]; thereafter
    taken at each Contract Anniversary and capped at the Free Withdrawal Amount, so the
    base run incurs no withdrawal charge. It is a model point column rather than a
    Reference because the notes' worked example and the notes' behavioural rule are
    mutually inconsistent - see the README.
    """
    return float(model_point()["wd_rate_ann"])


def scenario_id():
    """The market scenario the model point runs on, a key into *market_scenario.csv*."""
    return model_point()["scenario_id"]


def wd_schedule_id():
    """The scheduled withdrawal programme, a key into *withdrawal_table.csv*."""
    return model_point()["wd_schedule_id"]


def is_uncapped():
    """True when the model point leaves ``declared_cap`` blank [S2]."""
    return bool(pd.isna(model_point()["declared_cap"]))              # noqa: F821


def policy_term():
    """Years from issue to the Maturity Date [S2].

    The later of the anniversary after the oldest owner's 90th birthday and ten years from
    issue, read on the ANB attained age **[std]**: 30 years at issue age 60, 10 at 80 or
    above.
    """
    return max(maturity_age - age_at_entry(), maturity_min_years)    # noqa: F821


def proj_len():
    """Projection length in policy months, ``12 * policy_term()``."""
    return 12 * policy_term()


def duration_mth(t):
    """Policy months elapsed at the end of month t. The projection index itself."""
    return t


def duration(t):
    """cy(t) = floor(t / 12): complete contract years since issue, **at** month end t.

    The notes' own definition, and a **month-end** reading: the anniversary month ``t =
    12`` already counts as one completed contract year, which is what makes the withdrawal
    charge step and the free-withdrawal reset fall on the anniversary itself. Use this for
    anything read at the instant ``t`` - the charge a transaction settling there bears,
    the free-withdrawal base snapshotted there. For a rate that applies across the whole
    of month ``t``, use :func:`duration_bom` instead; the two differ only in anniversary
    months.
    """
    return max(0, t // 12)


def policy_year(t):
    """The contract year in force at month end t, ``duration(t) + 1``.

    The month-end reading, so ``policy_year(12) = 2``. The surrender assumptions read it
    - :func:`lapse_rate_base` and :func:`lapse_rate_sc_mult` - because the charge-expiry
    shock must land in the same month the charge a surrender bears goes to zero, which is
    :func:`surr_charge_rate` on the same reading.
    """
    return duration(t) + 1


def duration_bom(t):
    """Complete contract years at the **start** of month t, ``ceil(t/12) - 1``.

    The *interval* reading of the contract year: the year the whole of month ``t`` lies
    inside, so months 1 to 12 are contract year 1 and ``duration_bom(12) = 0`` where
    ``duration(12) = 1``. Rates that apply across a month rather than at its end are keyed
    on this - the attained age behind ``q_m(t)`` (:func:`age`) and the expense inflation
    step (:func:`inflation_factor`) - because a monthly rate charged over ``(t-1, t]``
    belongs to the contract year that interval sits in. This is the reading
    :mod:`.MYGA_US_S` uses for its own ``duration(t)``.
    """
    return max(0, (t + 11) // 12 - 1)


def age(t):
    """The attained age (ANB) during month t, ``x + ceil(t/12) - 1``.

    Keyed on :func:`duration_bom`, not :func:`duration`: ``q_m(t) = 1 - (1 - q_x)^(1/12)``
    is an exposure rate for the whole of month ``t``, so all twelve months of contract
    year 1 - month 12 included - are charged at ``q_x`` and the attained age steps at the
    anniversary rather than one month before it. At the Maturity Date the attained age is
    therefore ``age(proj_len()) + 1``, the age the contract's own rule names.
    """
    return age_at_entry() + duration_bom(t)


def is_anniv(t):
    """True at a Contract Anniversary, including the Issue Date itself."""
    return t % 12 == 0


def term_elapsed_mth(t):
    """Months elapsed in the term of the option **in force during** month t.

    ``0`` at issue and ``12T`` at a Term End Date - the expiring option, not the renewed
    one. Reading the boundary month as belonging to the term that is closing is what makes
    the term-end identity work: the replicating portfolio at ``tau = 0`` collapses to
    intrinsic value and reproduces ``g`` exactly.
    """
    if t <= 0:
        return 0
    return ((t - 1) % (12 * term_years())) + 1


def term_start_month(t):
    """The month at which the term in force during month t began."""
    return t - term_elapsed_mth(t)


def tau(t):
    """tau_k(t): years remaining in the option's term, ``(12T - elapsed) / 12``.

    The notes define it as days remaining / 365 [S2]; on a monthly grid that is exact
    twelfths. ``tau(0) = T`` and ``tau(t) = 0`` at every Term End Date.
    """
    return (12 * term_years() - term_elapsed_mth(t)) / 12.0


def is_term_end(t):
    """True when month t is a Term End Date, i.e. ``tau(t) == 0`` with ``t > 0``."""
    return t > 0 and term_elapsed_mth(t) == 12 * term_years()


def market_state(t, name):
    """Step-function lookup of column ``name`` in the model point's market scenario.

    Each row of *market_scenario.csv* states the market state that holds from its own
    month until the next row of the same scenario, so a flat path is one row. The index
    path is therefore piecewise constant between the scenario's own anchor months; that is
    a property of the deterministic scenario, not of the model.
    """
    sub = data.market_scenario().loc[scenario_id()]                  # noqa: F821
    months = [i for i in sub.index if i <= max(t, 0)]
    return float(sub.loc[max(months), name])


def index_level(t):
    """I(t): the index level at month t, price return [S1][S2].

    All representative indices are **price return**, which is why the dividend yield is a
    live pricing input: omitting it overprices every call in the portfolio.
    """
    return market_state(t, "index_level")


def index_at_term_start(t):
    """I_s: the index level at the Term Start Date of the term in force during month t."""
    return index_level(term_start_month(t))


def mvr(t):
    """r(t): the Market Value Rate at month t, annual effective [S2].

    The Constant Maturity Treasury yield at the term's maturity, linearly interpolated
    between adjacent CMT maturities [S2]; the model takes it as an exogenous scalar series
    **[std]** rather than carrying a curve.
    """
    return market_state(t, "mvr")


def mvr_at_term_start(t):
    """r_0: the Market Value Rate on the Term Start Date [S2]."""
    return mvr(term_start_month(t))


def risk_free(t):
    """The risk-free rate at month t, annual effective, 4.00% **[std]**."""
    return market_state(t, "risk_free")


def div_yield(t):
    """q: the dividend yield at month t, annual effective, 2.00% **[std]**.

    A live pricing input because every representative index is price return [S1][S2].
    """
    return market_state(t, "div_yield")


def impl_vol(t):
    """sigma: the implied volatility at month t, 20.00% flat **[std]**.

    A flat surface is the largest single simplification in this model. AG 54 requires
    assumptions "consistent with the observable market prices of derivative assets over
    the Index Strategy Term, whenever possible" [R2], and a production implementation must
    supply a surface interpolated in both maturity and moneyness [S4]; that is a change to
    *market_scenario.csv* plus a lookup, not to any formula here.
    """
    return market_state(t, "impl_vol")


def index_perf(t):
    """R_k(t): index performance to date, ``I(t) / I_s - 1``.

    At a Term End Date this is the crediting input; the cap applies to the **whole-term**
    return, never annually on a 3 or 6 year term [S5].
    """
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
    """
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    return ((math.log(spot / strike) + (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_)  # noqa: F821
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
    compresses the spread, which is why the table is a genuine tail exposure.
    """
    row = data.guar_min_rate_table().loc[term_years()]                # noqa: F821
    if kind == "CAP":
        return float(row["guar_min_cap"])
    elif kind == "STEP":
        return float(row["guar_min_step"])
    elif kind == "EDGE":
        return float(row["guar_min_edge"])
    else:
        raise ValueError("invalid kind")


def opt_budget_target():
    """beta_target(T) = ``1 - (1 + y_e - spread)^(-T)``: the NGE cap-solve target **[std]**.

    ``y_e`` is the projected earned rate on supporting assets and ``spread`` the target
    margin, **[std]** 2.22% - the level implied by the snapshot 6-year cap, which opens
    its fixed leg at an equivalent accretion yield of 1.7834% against a 4.00% market rate.
    """
    return 1.0 - (1.0 + earned_rate - nge_spread) ** (-term_years())  # noqa: F821


def opt_budget_at_cap(t, cap):
    """The per-unit replicating portfolio value at term start for a trial Cap Rate.

    The cap-solve needs the portfolio as a function of ``c`` while :func:`cap_rate` is
    what the rest of the model reads, so this cells recomputes the BUFFER + CAP + PR
    portfolio directly rather than calling :func:`opt_portfolio`, which would close a
    cycle. It is monotonically increasing in ``cap``.
    """
    i_s = index_at_term_start(t)
    m = term_start_month(t)
    tau_ = float(term_years())
    pr = participation()
    rate, divy, vol = risk_free(m), div_yield(m), impl_vol(m)
    atm = pr * bs_call(i_s, i_s, tau_, rate, divy, vol) / i_s
    otm = pr * bs_call(i_s, i_s * (1.0 + cap / pr), tau_, rate, divy, vol) / i_s
    otp = bs_put(i_s, i_s * (1.0 - buffer()), tau_, rate, divy, vol) / i_s
    return atm - otm - otp


def declared_cap_solved(t):
    """The Cap Rate solving ``Pi(c; b, T, sigma, r, q) = beta_target(T)`` **[std]**.

    The ASOP No. 2 determination rule the notes state for redetermining the declared cap
    at each Term Start Date [R5]. Solved by bisection because the portfolio value is
    monotone in ``c`` and no root finder may be imported; ``nge_solve_iter`` bisections of
    ``[0, nge_cap_search_max]`` reach machine precision on a rate. The result is floored
    at the contractual minimum by :func:`cap_rate`, not here.
    """
    target = opt_budget_target()
    lo, hi = 0.0, nge_cap_search_max                                 # noqa: F821
    for _ in range(nge_solve_iter):                                  # noqa: F821
        mid = 0.5 * (lo + hi)
        if opt_budget_at_cap(t, mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def cap_rate(t):
    """c: the Cap Rate in force for the term containing month t, floored at the minimum.

    The snapshot declared cap on the initial term; on a renewal term either the same
    snapshot (the notes' base projection holds the scale level) or, with ``nge_reset``,
    the solved cap - in both cases floored at the guaranteed minimum [S2]. Returns
    ``math.inf`` for an uncapped option, which makes ``min(PR R, c)`` the uncapped payoff
    and switches the out-of-the-money call off in :func:`opt_component` [S2].
    """
    if is_uncapped():
        return math.inf                                              # noqa: F821
    if nge_reset() and term_start_month(t) > 0:
        return max(guar_min_rate("CAP"), declared_cap_solved(t))
    return max(guar_min_rate("CAP"), declared_cap())


def step_rate(t):
    """s: the Step Rate in force, floored at the 2% contractual minimum [S2]."""
    return max(guar_min_rate("STEP"), declared_step())


def edge_rate(t):
    """e: the Edge Rate in force, floored at the 2% contractual minimum [S2]."""
    return max(guar_min_rate("EDGE"), declared_edge())


def opt_legs():
    """The legs of the replicating portfolio for the model point's crediting type.

    Cap: at-the-money call, out-of-the-money call, out-of-the-money put [S2][S3][S5][S6].
    Step: step-scaled at-the-money binary call, out-of-the-money put [S2][S5]. Edge: the
    binary call is struck at ``I_s(1 - b)`` and is therefore **in the money**, because it
    pays when the index ratio is at or above ``1 - b`` [S2][S5]. Floor needs **four**
    options, not three - buy the at-the-money call spread, sell an at-the-money put, and
    buy back an out-of-the-money put struck at the floor so the short put exposure stops
    there [S5].
    """
    kind = crediting_type()
    if kind == "CAP":
        return ("ATM_CALL", "OTM_CALL", "OTM_PUT")
    elif kind == "STEP":
        return ("STEP_BINARY", "OTM_PUT")
    elif kind == "EDGE":
        return ("EDGE_BINARY", "OTM_PUT")
    elif kind == "FLOOR":
        return ("ATM_CALL", "OTM_CALL", "ATM_PUT", "FLOOR_PUT")
    else:
        raise ValueError("invalid crediting_type")


def opt_component(t, leg, spot, tau_, mkt):
    """The **signed** value of one replicating-portfolio leg, per unit of notional.

    Each option's notional is the Investment Amount [S4], and every strike is set from the
    Term Start Date index level ``I_s``, so dividing by ``I_s`` makes each leg
    dimensionless and the portfolio a fraction of notional. ``mkt`` selects the market
    state: ``"CURRENT"`` prices at month ``t``, ``"TERM_START"`` prices under the initial
    market conditions of the term in force, which is what the option budget and the
    ``updated_expiry`` amortization need.

    The participation rate multiplies the call spread and re-strikes the short call at
    ``I_s(1 + c/PR)`` [S4]; at ``PR = 1`` that is exactly the plain Cap portfolio, so one
    branch serves both of the notes' first two rows. An uncapped option values the
    out-of-the-money call at zero [S2].
    """
    if mkt == "CURRENT":
        m = t
    elif mkt == "TERM_START":
        m = term_start_month(t)
    else:
        raise ValueError("invalid mkt")
    rate, divy, vol = risk_free(m), div_yield(m), impl_vol(m)
    i_s = index_at_term_start(t)
    pr = participation() if crediting_type() == "CAP" else 1.0
    if leg == "ATM_CALL":
        return pr * bs_call(spot, i_s, tau_, rate, divy, vol) / i_s
    elif leg == "OTM_CALL":
        cap = cap_rate(t)
        if math.isinf(cap):                                          # noqa: F821
            return 0.0
        strike = i_s * (1.0 + cap / pr)
        return -pr * bs_call(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == "OTM_PUT":
        strike = i_s * (1.0 - buffer())
        return -bs_put(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == "ATM_PUT":
        return -bs_put(spot, i_s, tau_, rate, divy, vol) / i_s
    elif leg == "FLOOR_PUT":
        strike = i_s * (1.0 - floor_rate())
        return bs_put(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == "STEP_BINARY":
        return step_rate(t) * bs_binary_call(spot, i_s, tau_, rate, divy, vol)
    elif leg == "EDGE_BINARY":
        strike = i_s * (1.0 - buffer())
        return edge_rate(t) * bs_binary_call(spot, strike, tau_, rate, divy, vol)
    else:
        raise ValueError("invalid leg")


def opt_portfolio(t, spot, tau_, mkt):
    """Pi(I, tau): the per-unit market value of the replicating option portfolio.

    The sum of the signed legs. **Verification identity**: at ``tau = 0`` this collapses
    to the crediting rate ``g`` for every crediting type - for the Cap design
    ``max(R,0) - max(R-c,0) - max(-b-R,0) = g``. If the interim value at term end does not
    reproduce ``IA(1 + g)`` exactly, the strike set or the notional convention is wrong;
    :func:`check_term_end_identity` tests it.
    """
    return sum(opt_component(t, leg, spot, tau_, mkt) for leg in opt_legs())


def opt_portfolio_abs(t, spot, tau_, mkt):
    """The sum of the **absolute** leg values: the trading cost assessment base **[std]**.

    A wider base than the Academy's net derivative value [R6], deliberately, because no
    prospectus quantifies the trading cost provision; the base must be stated whenever the
    factor is recalibrated.
    """
    return sum(abs(opt_component(t, leg, spot, tau_, mkt)) for leg in opt_legs())


def opt_budget(t):
    """beta: the initial option budget per unit of notional, ``Pi(I_s, T)``.

    Struck at each Term Start Date under the market conditions of that date. On the anchor
    cell ``beta = 10.0632%``, so the option budget is $10,063.19 of a $100,000 Investment
    Amount and the fixed leg opens at $89,936.81.
    """
    return opt_portfolio(t, index_at_term_start(t), float(term_years()), "TERM_START")


def fixed_leg_yield(t):
    """The equivalent geometric accretion yield on the fixed leg, ``(1-beta)^(-1/T) - 1``.

    1.7834% on the anchor cell: the rate at which $89,936.81 accretes to $100,000 over six
    years. The gap to the 4.00% market rate is :func:`nge_spread_implied`.
    """
    return (1.0 - opt_budget(t)) ** (-1.0 / term_years()) - 1.0


def nge_spread_implied(t):
    """The spread implied by the declared cap: ``earned rate - fixed leg yield``.

    2.22% on the anchor cell, and that is the **[std]** ``nge_spread`` input to the
    cap-solve rule - the model's own snapshot, read back out of the snapshot cap.
    """
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
    rules are applied to the accrued rates.
    """
    kind = crediting_type()
    perf = index_perf(t)
    buff = buffer() * accrual
    if kind == "CAP":
        cap = cap_rate(t)
        cap = cap if math.isinf(cap) else cap * accrual              # noqa: F821
        return min(participation() * perf, cap) if perf >= 0.0 else min(0.0, perf + buff)
    elif kind == "STEP":
        return step_rate(t) * accrual if perf >= 0.0 else min(0.0, perf + buff)
    elif kind == "EDGE":
        edge = edge_rate(t) * accrual
        return edge if perf >= -buff else perf + buff
    elif kind == "FLOOR":
        cap = cap_rate(t)
        cap = cap if math.isinf(cap) else cap * accrual              # noqa: F821
        return min(max(perf, -floor_rate() * accrual), cap)
    else:
        raise ValueError("invalid crediting_type")


def credit_rate_term(t):
    """g at a Term End Date, zero in every other month.

    Applied as ``IA_k(term end) = IA_k(term start, adjusted for withdrawals) x (1 + g)``
    [S1][S2].
    """
    return credit_rate_at(t, 1.0) if is_term_end(t) else 0.0


def credit_rate_accrued(t):
    """The pre-AG 54 time-prorated crediting rate at month t [S1].

    ``credit_rate_at(t, elapsed / total)``. The source worked example - $50,000, a 10%
    buffer, a 10% Cap on a one-year term, index 500 to 600 at day 183 - gives an accrued
    cap of 5%, a 5% Performance Rate and an interim value of $52,500; on a monthly grid
    month 6 of 12 is exactly half the term, so the model reproduces it to the cent.
    """
    return credit_rate_at(t, 1.0 - tau(t) / term_years())


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
    every withdrawal.
    """
    if tau(t) <= 0.0:
        return 0.0
    rule = amort_rule()
    if rule == "straight_line":
        return opt_budget(t) * tau(t) / term_years()
    elif rule == "updated_expiry":
        return opt_portfolio(t, index_at_term_start(t), tau(t), "TERM_START")
    else:
        raise ValueError("invalid amort_rule")


def mva_factor(t):
    """``[(1 + r_0) / (1 + r(t))]^tau``: the interim value's interest-rate adjustment [S2].

    The only market-value-adjustment-like term in the contract, and it lives **inside**
    the interim value rather than on the surrender benefit - this product has no contract
    MVA. At the worked-example parameters a 100 bp rise costs $2,687.62 of interim value
    at the term midpoint, two orders of magnitude more than the entire trading-cost
    provision. Family (c) has no such term at all [S5], so the choice of interim-value
    family is itself a rate-sensitivity assumption.
    """
    return ((1.0 + mvr_at_term_start(t)) / (1.0 + mvr(t))) ** tau(t)


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
    """
    family = iv_family()
    if family == "portfolio":
        return (1.0 - budget_amort_factor(t)) * mva_factor(t)
    elif family == "notional":
        return (1.0 + risk_free(t) + iv_credit_spread) ** (-tau(t))  # noqa: F821
    elif family == "delta":
        return 1.0 - budget_amort_factor(t)
    elif family == "legacy":
        return 0.0
    else:
        raise ValueError("invalid iv_family")


def deriv_proxy_factor(t):
    """D_k(t) / IA_k(t): the Derivative Asset Proxy, ``Pi(I(t), tau(t))``.

    Valued at the current market state. The pre-AG 54 ``legacy`` engine has no derivative
    proxy at all - it uses no option pricing.
    """
    if iv_family() == "legacy":
        return 0.0
    return opt_portfolio(t, index_level(t), tau(t), "CURRENT")


def trading_cost_factor(t):
    """TC_k(t) / IA_k(t): the trading cost provision, ``kappa x sum |leg values|``.

    Strictly interior to the term: ``kappa_effective = kappa x 1{tau > 0}`` **[std]**.
    There are no options left to exit at term end, the Academy example likewise shows no
    trading cost there [R6], and leaving the provision switched on at ``tau = 0`` breaks
    the term-end verification identity by ``kappa x IA x |g|``. Only family (a) carries
    it; family (b) has an always-positive expense rebate instead [S4] and family (c)
    states none [S5].
    """
    if iv_family() != "portfolio" or tau(t) <= 0.0:
        return 0.0
    return trading_cost_rate * opt_portfolio_abs(                    # noqa: F821
        t, index_level(t), tau(t), "CURRENT")


def cap_calc_factor(t):
    """CCF_k(t) / IA_k(t): the Cap Calculation Factor of family (b) [S4].

    ``E_0 x tau/T`` - "a return of estimated expenses for the portion of the Segment
    Duration that has not elapsed", always positive and declining to zero at term end;
    the source works it as $10 of estimated expenses on a one-year segment giving $6 with
    219 days remaining. ``E_0`` is expressed here as a rate of notional,
    ``iv_expense_rate`` = **[std]** 0.10%, because no source quantifies it - the same
    standing as family (b)'s other free parameter, ``iv_credit_spread``.
    """
    if iv_family() != "notional":
        return 0.0
    return iv_expense_rate * tau(t) / term_years()                   # noqa: F821


def iv_factor(t):
    """V_k(t) / IA_k(t-1): the interim value per unit of the pre-crediting notional.

    ``F + D - TC + CCF`` for the three AG 54-era families, and ``1 + g_accrued`` for the
    pre-AG 54 one. Two boundaries fall out of the algebra rather than being imposed: at
    ``tau = T`` the fixed and derivative legs sum to exactly 1, which is AG 54's
    requirement that the Index Strategy Base equal the Strategy Value at term start [R2];
    at ``tau = 0`` they sum to ``1 + g``, which is the term-end Strategy Value.

    At ``t = 0`` this returns 1 rather than ``1 - kappa x sum|legs|``. The interim value is
    **undefined** at term start and term end - those points are Strategy Values, not
    Interim Values [R6] - and the contract sets the value equal to the Investment Amount
    for the Transfer Period [S2]. :func:`trading_cost_pp` still reports the $33.07 the
    worked example's opening row shows.
    """
    if t <= 0:
        return 1.0
    if iv_family() == "legacy":
        return 1.0 + credit_rate_accrued(t)
    return (fixed_proxy_factor(t) + deriv_proxy_factor(t)
            - trading_cost_factor(t) + cap_calc_factor(t))


def iv_ratio(t):
    """V_k(t) / IA_k(t): the interim value per unit of the **current** notional.

    1 at a Term End Date, where the Investment Amount has just been credited and the
    interim value equals it for the Transfer Period [S2], and 1 at issue; the interim
    value factor otherwise. Multiplying by this is how homogeneity is carried through the
    model: the same ratio serves before and after a withdrawal, so the interim value falls
    by exactly the cash removed.
    """
    return 1.0 if (t <= 0 or is_term_end(t)) else iv_factor(t)


def inv_amt_basis_pp(t):
    """IA_k(t-1): the notional the month-t valuation applies to, per contract.

    The whole purchase payment at issue - the anchor cell allocates 100% to one 6-year
    option - and the prior month's Investment Amount thereafter.
    """
    return premium_pp() if t <= 0 else inv_amt_pp(t - 1)


def iv_notional_pp(t, timing):
    """The notional an interim-value decomposition column is measured on.

    ``"BEF_ROLL"`` is ``IA_k(t-1)``, the notional in force during month ``t`` before the
    roll split - the notes' rows 0, A1, B1, A2 and B3. ``"AFT_WD"`` is the notional after
    the proportional withdrawal reduction - the notes' row B2, in which **every** component
    of the interim value scales by the same factor, which is exactly why the interim value
    then falls by precisely the cash withdrawn.
    """
    if timing == "BEF_ROLL":
        return inv_amt_basis_pp(t)
    elif timing == "AFT_WD":
        return inv_amt_pp(t)
    else:
        raise ValueError("invalid timing")


def opt_component_pp(t, leg, timing="BEF_ROLL"):
    """The currency value of one replicating-portfolio leg, per contract.

    The notional at ``timing`` times the per-unit leg value at the current market state.
    These are the worked example's ATM call, OTM call and OTM put columns.
    """
    return iv_notional_pp(t, timing) * opt_component(
        t, leg, index_level(t), tau(t), "CURRENT")


def fixed_proxy_pp(t, timing="BEF_ROLL"):
    """F_k(t): the Fixed Income Asset Proxy in currency, per contract."""
    return iv_notional_pp(t, timing) * fixed_proxy_factor(t)


def budget_amort_pp(t, timing="BEF_ROLL"):
    """B_k(t): the amortized initial option budget in currency, per contract."""
    return iv_notional_pp(t, timing) * budget_amort_factor(t)


def deriv_proxy_pp(t, timing="BEF_ROLL"):
    """D_k(t): the Derivative Asset Proxy in currency, per contract."""
    return iv_notional_pp(t, timing) * deriv_proxy_factor(t)


def trading_cost_pp(t, timing="BEF_ROLL"):
    """TC_k(t): the trading cost provision in currency, per contract."""
    return iv_notional_pp(t, timing) * trading_cost_factor(t)


def inv_amt_pp_at(t, timing):
    """IA_k: the Investment Amount per contract, read at a point inside month t.

    ``"BEF_CREDIT"`` is ``IA(t-1)``; ``"BEF_ROLL"`` applies term-end crediting;
    ``"BEF_WD"`` applies the renewal / transfer roll split; ``"AFT_WD"`` applies the
    proportional withdrawal reduction. Outside a Term End Date the first three coincide.
    """
    if timing == "BEF_CREDIT":
        return inv_amt_basis_pp(t)
    elif timing == "BEF_ROLL":
        return inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t))
    elif timing == "BEF_WD":
        rolled = inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t))
        return rolled * roll_share("OPTION") if is_term_end(t) else rolled
    elif timing == "AFT_WD":
        return inv_amt_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_amt_pp(t):
    """IA_k(t): the Investment Amount (AG 54 Index Strategy Base) at end of month t.

    Term-end crediting, then the roll split, then **the universal proportional rule**:

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
    """
    if t <= 0:
        return premium_pp()
    base = inv_amt_pp_at(t, "BEF_WD")
    value = interim_value_pp_at(t, "BEF_WD")
    if value <= 0.0:
        return base
    return base * (1.0 - wd_alloc_pp(t, "OPTION") / value)


def interim_value_pp_at(t, timing):
    """V_k: the Interim Value per contract, read at a point inside month t.

    ``"BEF_ROLL"`` is the worked example's Interim value column - the value of the option
    in force during month ``t``, after any term-end crediting and before the roll split.
    ``"BEF_WD"`` and ``"AFT_WD"`` are that value carried through the roll split and the
    withdrawal, each as the Investment Amount at that point times :func:`iv_ratio`.

    Every mid-term transaction settles here: withdrawal, surrender, death benefit,
    annuitization, transfer and any fee deduction [S1][S2][S4][S6]. It can be **negative
    even when the index is up** [S2]; flooring it at zero, or at the notional, is not
    implementing the contract.
    """
    if timing == "BEF_ROLL":
        return inv_amt_basis_pp(t) * iv_factor(t)
    elif timing == "BEF_WD":
        return inv_amt_pp_at(t, "BEF_WD") * iv_ratio(t)
    elif timing == "AFT_WD":
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
    if bucket == "OPTION":
        return roll_renew_same + roll_transfer_other                 # noqa: F821
    elif bucket == "FIXED":
        return roll_transfer_fixed                                   # noqa: F821
    elif bucket == "HOLDING":
        return roll_transfer_holding                                 # noqa: F821
    else:
        raise ValueError("invalid bucket")


def roll_to_acct_pp(t, bucket):
    """The amount transferred out of the option into a general-account bucket at term end."""
    if not is_term_end(t):
        return 0.0
    return inv_amt_pp_at(t, "BEF_ROLL") * roll_share(bucket)


def acct_rate():
    """The declared Fixed and Holding Account rate, floored at the 1% minimum [S1][S2].

    3.00% **[std]** - only the contractual minimum is public.
    """
    return max(declared_acct_rate, guar_min_acct_rate)               # noqa: F821


def fixed_acct_pp_at(t, timing):
    """FA: the Fixed Account value per contract, read at a point inside month t.

    ``FA(t) = FA(t-1) x (1 + max(i_declared, 0.01))^(1/12)`` [S1][S2], plus any amount
    transferred in at a Term End Date, less its pro-rata share of the withdrawal. The
    transfer accrues for the month in which it arrives **[std]**.
    """
    if t < 1:
        return 0.0
    if timing == "BEF_WD":
        opening = fixed_acct_pp(t - 1) + roll_to_acct_pp(t, "FIXED")
        return opening * (1.0 + acct_rate()) ** (1.0 / 12.0)
    elif timing == "AFT_WD":
        return fixed_acct_pp(t)
    else:
        raise ValueError("invalid timing")


def fixed_acct_pp(t):
    """FA(t): the Fixed Account value per contract at the end of month t."""
    if t < 1:
        return 0.0
    return fixed_acct_pp_at(t, "BEF_WD") - wd_alloc_pp(t, "FIXED")


def holding_acct_pp_at(t, timing):
    """HA: the Holding Account value per contract, read at a point inside month t.

    Same accrual and the same 1% guaranteed minimum as the Fixed Account [S1][S2]. It
    holds maturing amounts to the next Contract Anniversary when the option and the Fixed
    Account are both unavailable [S2]; ``roll_transfer_holding`` is 0 on the base run, so
    the bucket stays empty and is carried for completeness of ``AV = sum V_k + FA + HA``.
    """
    if t < 1:
        return 0.0
    if timing == "BEF_WD":
        opening = holding_acct_pp(t - 1) + roll_to_acct_pp(t, "HOLDING")
        return opening * (1.0 + acct_rate()) ** (1.0 / 12.0)
    elif timing == "AFT_WD":
        return holding_acct_pp(t)
    else:
        raise ValueError("invalid timing")


def holding_acct_pp(t):
    """HA(t): the Holding Account value per contract at the end of month t."""
    if t < 1:
        return 0.0
    return holding_acct_pp_at(t, "BEF_WD") - wd_alloc_pp(t, "HOLDING")


def av_pp_at(t, timing):
    """AV: the Account Value per contract, ``sum_k V_k(t) + FA(t) + HA(t)``.

    ``"BEF_WD"`` is the notes' step 5 value - after crediting, the roll split, the interim
    value and the account accruals, before any transaction. It is the base the withdrawal
    is allocated across, the base the free-withdrawal allowance is snapshotted from, and
    the base the return-of-premium reduction ratio uses. ``"AFT_WD"`` is
    :func:`av_pp`, the value every decrement benefit is measured on.

    Between term start and term end this contract has **no account value in the ordinary
    sense**: ``AV`` is a derivative price, depressed exactly when the option leg is out of
    the money - which is when the return-of-premium guarantee bites.
    """
    if t < 1:
        return premium_pp() if t == 0 else 0.0
    if timing == "BEF_WD":
        return (interim_value_pp_at(t, "BEF_WD")
                + fixed_acct_pp_at(t, "BEF_WD")
                + holding_acct_pp_at(t, "BEF_WD"))
    elif timing == "AFT_WD":
        return av_pp(t)
    else:
        raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the Account Value per contract at the end of month t."""
    if t <= 0:
        return premium_pp()
    return (interim_value_pp_at(t, "AFT_WD")
            + fixed_acct_pp(t) + holding_acct_pp(t))


def inv_income_pp(t):
    """The investment return credited to one contract's Account Value in month t.

    ``AV`` before the transaction less the prior month end. On this product it is not
    "interest credited": it is the month's movement in a derivative price plus the Fixed
    and Holding Accounts' accrual, and at a Term End Date it also carries the index credit.
    """
    if t < 1:
        return 0.0
    return av_pp_at(t, "BEF_WD") - av_pp(t - 1)


def free_wd_base(t):
    """AV_anniv(y): the Account Value at the most recent Contract Anniversary [S1][S2].

    Read **before** that month's transaction, which is the notes' step 5 - the snapshot is
    taken when the anniversary is reached and the withdrawal follows at step 6 - so an
    anniversary withdrawal is measured against a base that already includes that month's
    crediting.
    """
    return av_pp_at(12 * duration(t), "BEF_WD")


def free_wd_allow(t):
    """The Free Withdrawal Amount for the contract year containing month t [S1][S2].

    Zero in contract year 1; thereafter 10% of the Account Value at the prior Contract
    Anniversary, non-cumulative - nothing carries across an anniversary.
    """
    if duration(t) < 1:
        return 0.0
    return free_wd_rate * free_wd_base(t)                            # noqa: F821


def free_wd_avail(t):
    """FW(t): the unused free withdrawal allowance at month t, before that month's G.

    Reset to the whole allowance at each Contract Anniversary and carried forward within
    the contract year, reduced by amounts already withdrawn in it [S1][S2].
    """
    if t < 1:
        return 0.0
    if is_anniv(t):
        return free_wd_allow(t)
    return free_wd_remain(t - 1)


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *withdrawal_table.csv*, else zero."""
    if t < 1:
        return 0.0
    table = data.withdrawal_table()                                  # noqa: F821
    key = (wd_schedule_id(), t)
    return float(table.loc[key, "wd_amount"]) if key in table.index else 0.0


def wd_behavioral_pp(t):
    """The behavioural partial withdrawal at month t **[std]**.

    0% in contract year 1, the free amount being zero there [S1][S2]; thereafter
    ``wd_rate_ann`` of the Account Value taken at each Contract Anniversary and capped at
    the Free Withdrawal Amount, so the base run incurs no withdrawal charge. RMD-driven
    withdrawals for qualified cells are named in the notes as a behavioural input but no
    amount formula is given, so no RMD module is implemented.
    """
    if t < 1 or not is_anniv(t) or duration(t) < 1:
        return 0.0
    return min(wd_rate_ann() * av_pp_at(t, "BEF_WD"), free_wd_allow(t))


def wd_pp(t):
    """G_total: the gross amount removed from the contract at month t, per contract.

    The scheduled programme plus the behavioural rule. Gross by construction: the
    withdrawal charge is deducted **from** the amount withdrawn and is not grossed up on
    this chassis [S1][S2], in contrast to [S4]. Capped at the Account Value **[std]** so a
    request larger than the contract cannot drive it negative; the contractual treatment
    of a request that would leave less than the $2,000 minimum - it becomes a full
    withdrawal [S1][S2] - is not implemented.
    """
    if t < 1:
        return 0.0
    total = wd_scheduled_pp(t) + wd_behavioral_pp(t)
    return min(total, max(0.0, av_pp_at(t, "BEF_WD")))


def wd_free_pp(t):
    """The portion of G_total inside the Free Withdrawal Amount, free of charge [S1][S2]."""
    return min(wd_pp(t), free_wd_avail(t))


def free_wd_remain(t):
    """The unused free withdrawal allowance after month t's withdrawal.

    This, not :func:`free_wd_avail`, is the allowance a full surrender at the end of month
    t can still shelter.
    """
    return free_wd_avail(t) - wd_free_pp(t)


def wd_excess_pp(t):
    """chargeable: ``max(0, G_total - FW(t))``, the amount exposed to the charge [S1][S2]."""
    return max(0.0, wd_pp(t) - free_wd_avail(t))


def surr_charge_rate(t):
    """wc(cy): the withdrawal charge rate at month t, by **complete** contract years.

    7, 7, 6, 5, 4, 3, 0 per cent [S1][S2], zero once the schedule runs out. Contract year
    7 - the first with a zero charge - is also the first year following a 6-year Term End
    Date on this chassis, which is why the charge-expiry shock lapse is applied there.
    """
    table = data.surr_charge_table()                                 # noqa: F821
    key = duration(t)
    if key not in table.index:
        return 0.0
    return float(table.loc[key, "surr_charge_rate"])


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
    if bucket == "OPTION":
        return max(0.0, interim_value_pp_at(t, "BEF_WD"))
    elif bucket == "FIXED":
        return max(0.0, fixed_acct_pp_at(t, "BEF_WD"))
    elif bucket == "HOLDING":
        return max(0.0, holding_acct_pp_at(t, "BEF_WD"))
    else:
        raise ValueError("invalid bucket")


def wd_alloc_pp(t, bucket):
    """G_k: the part of G_total taken from one bucket, pro rata to value **[std]**.

    The notes prescribe allocation across open options **pro rata to interim value**,
    the prospectuses not prescribing an allocation for an unspecified withdrawal; with a
    Fixed and a Holding Account present the model extends the same rule to all three
    buckets. On a single-option model point with empty general accounts the whole
    withdrawal falls on the option.
    """
    if t < 1 or wd_pp(t) <= 0.0:
        return 0.0
    total = sum(wd_bucket_value_pp(t, b) for b in ("OPTION", "FIXED", "HOLDING"))
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
    """ROP(t): the return-of-premium GMDB base, reduced **proportionally** [S1][S2].

    ``ROP(t+) = ROP(t-) x (1 - G_total / AV(t-))``, the ratio taken on the **gross** amount
    removed from the contract - including any withdrawal charge [S1] - and on the Account
    Value before the transaction.
    """
    if t <= 0:
        return premium_pp()
    base = av_pp_at(t, "BEF_WD")
    if base <= 0.0 or wd_pp(t) <= 0.0:
        return rop_pp(t - 1)
    return rop_pp(t - 1) * (1.0 - wd_pp(t) / base)


def death_ben_pp(t):
    """DB(t): ``max(AV(t), ROP(t))`` for issue ages 80 and under, ``AV(t)`` for 81+ [S2].

    The guarantee sits on top of a value that is itself a derivative price, so it is most
    in the money exactly when interim values are depressed: the guarantee and the account
    are not independent, and a deterministic run understates its cost.
    """
    if age_at_entry() <= db_rop_max_issue_age:                       # noqa: F821
        return max(av_pp(t), rop_pp(t))
    return av_pp(t)


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, times the A/E factor.

    The shipped table is an illustrative annuitant curve **[std]**, *not* a published
    basis. The notes prescribe the 2012 IAM **Basic** table (VM-M section 2.C) with
    generational Projection Scale G2 [REG-R59], which may not be redistributed here; swap
    it in by repointing ``Data.mort_table_file``. Do **not** run best-estimate mortality
    off the 2012 IAM *Period* table: it carries the valuation margin built in at
    construction, so a 100% A/E against it sets deferral-phase mortality roughly 10% below
    the unloaded basis [REG-R60]. ``mort_ae_factor`` is 100% **[std]** - a placeholder,
    not a measurement, because public deferred-period annuitant mortality is thin
    [REG-R65] and the payout chassis's 108.4% is annuitant-select and deliberately not
    imported.
    """
    rate = float(data.mort_table().loc[(age(t), sex()), "mort_rate"])   # noqa: F821
    return rate * mort_ae_factor                                     # noqa: F821


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """w_base(y): the un-shocked annual surrender rate for the contract year **[std]**.

    2.0% through contract year 7 and 6.0% thereafter, read as a step function of the
    contract year. A shape placeholder: the VA/RILA behaviour study [REG-R64] reports
    aggregate counts only and its detailed tables sit behind a paid data package. The
    shock enters separately as :func:`lapse_rate_sc_mult`, so the two are multiplicative
    and neither is baked into the other.
    """
    table = data.lapse_table()                                       # noqa: F821
    years = [i for i in table.index if i <= policy_year(t)]
    return float(table.loc[max(years), "lapse_rate_base"])


def lapse_shock_year():
    """The contract year the withdrawal-charge-expiry surrender shock falls in.

    The first contract year with a zero withdrawal charge, derived from
    *surr_charge_table.csv* rather than hard-coded, so a different schedule moves the
    shock with it - the construction :mod:`.UL_US_S` uses. On the 7-7-6-5-4-3-0
    schedule that is contract year 7, which on this 6-year chassis is also the first year
    following a Term End Date [S1][S2].
    """
    table = data.surr_charge_table()                                 # noqa: F821
    free = [cy for cy in table.index
            if float(table.loc[cy, "surr_charge_rate"]) <= 0.0]
    return (min(free) if free else max(table.index) + 1) + 1


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
    term structure offsets it, so the **[std]** shock is set well below that anchor.
    """
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def lapse_iv_mult(t):
    """M_iv(t): interim-value moneyness suppression, the RILA-specific effect **[std]**.

    ``min(1.0, max(0.25, V_k(t) / IA_k(t)))^2``, so a bucket at ``V/IA = 0.85`` carries a
    0.72 multiplier and one at or above par carries 1.0. Surrendering mid-term
    crystallizes the interim value, which is punitive when the option leg is out of the
    money [S1][S2], and a rational holder defers. It is exactly 1 at a Term End Date,
    where the interim value equals the Investment Amount, which is what makes the
    term-end concentration :func:`term_end_lapse_rate` the whole story there.
    """
    return min(1.0, max(iv_moneyness_floor, iv_ratio(t))) ** 2       # noqa: F821


def lapse_rate(t):
    """w_annual(y,t): the **annual** surrender rate, ``min(0.50, w_base x M_sc x M_iv)``.

    The 50% ceiling is a **[std] cap**. ``lapse_rate`` is annual and
    :func:`lapse_rate_mth` is monthly, matching the ``mort_rate`` / ``mort_rate_mth``
    pair; the decrement chain reads the monthly one.
    """
    return min(lapse_rate_max,                                       # noqa: F821
               lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_iv_mult(t))


def lapse_rate_mth(t):
    """w_m(t): the monthly background surrender rate, ``1 - (1 - w_annual)^(1/12)``."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


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

        l(t) = l(t-1) (1 - q_m(t)) (1 - w_m(t)) (1 - phi(t))

    ``"BEF_DECR"`` is ``l(t-1)``, the start-of-month count, and is :func:`pols_if` itself.
    ``"AFT_DECR"`` is the notes' own **end**-of-month ``l(t)``, which lives here because
    ``pols_if`` carries the start-of-month count library-wide.
    """
    if t < 1:
        return pols_if_init()
    pols = pols_if(t)
    if timing == "BEF_DECR":
        return pols
    pols = pols * (1.0 - mort_rate_mth(t))
    if timing == "BEF_LAPSE":
        return pols
    pols = pols * (1.0 - lapse_rate_mth(t))
    if timing == "BEF_TERM_SURR":
        return pols
    pols = pols * (1.0 - term_end_lapse_rate(t))
    if timing == "AFT_DECR":
        return pols
    raise ValueError("invalid timing")


def pols_if(t):
    """l(t-1): the in-force probability at the **start** of policy month t.

    The library-wide convention, following :mod:`.Term_US_A` and ``CashValue_SE``:
    ``pols_if(t)`` counts the contracts entering period ``t`` and is the weight applied
    to that same period's cash flows, so the ``pols_if`` column of :func:`result_cf`
    reconciles against the row it sits on - ``premiums(t) / premium_pp()``,
    ``withdrawals(t) / wd_payment_pp(t)`` and ``expenses(t)`` over the per-contract
    maintenance charge all return it. ``pols_if(1)`` is therefore ``pols_if_init()``.

    The notes' own end-of-month ``l(t)`` is ``pols_if_at(t, "AFT_DECR")``; it is *not*
    this cells. Zero past the Maturity Date, where the survivors have been
    force-annuitized out through :func:`pols_maturity`.
    """
    if t <= 1:
        return pols_if_init()
    if t > proj_len():
        return 0.0
    return pols_if_at(t - 1, "AFT_DECR")


def pols_death(t):
    """Deaths in month t, weighted ``l(t-1) q_m(t)``."""
    return 0.0 if t < 1 else pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_lapse_term(t):
    """The discrete term-end concentrated surrenders, non-zero only at a Term End Date."""
    return 0.0 if t < 1 else pols_if_at(t, "BEF_TERM_SURR") * term_end_lapse_rate(t)


def pols_lapse(t):
    """Full surrenders in month t: the background rate on survivors, plus ``phi``.

    Weighted ``l(t-1)(1 - q_m(t)) w_m(t)`` **[std timing]** for the background part. Both
    parts settle at the same cash surrender value, so they are one benefit line; the
    term-end part is broken out as :func:`pols_lapse_term` for diagnosis.
    """
    if t < 1:
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t) + pols_lapse_term(t)


def pols_maturity(t):
    """Forced annuitizations at the Maturity Date, non-zero only at ``proj_len()``.

    Not a decrement - the contract reaches its Maturity Date and must annuitize [S2] - but
    needed for the in-force roll-forward to close; see the Space docstring.
    """
    return pols_if_at(t, "AFT_DECR") if t == proj_len() else 0.0


def pols_decr(t, kind):
    """The number of contracts leaving in month t by benefit ``kind``."""
    if kind == "DEATH":
        return pols_death(t)
    elif kind == "LAPSE":
        return pols_lapse(t)
    elif kind == "MATURITY":
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def claim_pp(t, kind):
    """The benefit paid per contract in month t by ``kind``.

    ``"DEATH"`` is :func:`death_ben_pp`, ``max(AV, ROP)`` in the return-of-premium band
    [S2]. ``"LAPSE"`` is the cash surrender value :func:`surr_value_pp`. ``"MATURITY"`` is
    the Account Value, force-annuitized at the Maturity Date [S2]; converting it to a
    payment stream is the immediate-annuity chassis, restricted to the two forms this
    contract offers - and note that this contract offers **no refund forms**, so that
    branch of the chassis is unused.
    """
    if kind == "DEATH":
        return death_ben_pp(t)
    elif kind == "LAPSE":
        return surr_value_pp(t)
    elif kind == "MATURITY":
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
    if kind in ("DEATH", "LAPSE", "MATURITY"):
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single purchase payment at t = 0 [S1][S2].

    Weighted by :func:`pols_if`, the count entering month t, so
    ``premiums(0) / premium_pp() == pols_if(0)``.
    """
    return premium_pp() * pols_if(t) if t == 0 else 0.0


def prem_to_av_pp(t):
    """Premium credited to the Investment Amount per contract; the whole payment at t = 0.

    There is no front-end load and no explicit asset-based charge on this chassis: the cap
    *is* the fee, and the margin appears as the spread between the earned rate and the
    option budget implied by the declared cap [S3][S4][S6].
    """
    return premium_pp() if t == 0 else 0.0


def prem_to_av(t):
    """Premium credited to the block's Account Value."""
    return prem_to_av_pp(t) * pols_if(t) if t == 0 else 0.0


def withdrawals(t):
    """Withdrawal payments in month t: ``(G_total - WC(t))`` weighted by :func:`pols_if`.

    The weight is the count entering month t - transactions are taken before the month's
    decrements - so ``withdrawals(t) / wd_payment_pp(t) == pols_if(t)``. The withdrawal
    charge is retained by the insurer, so it is not a cash flow of its own: it is the
    difference between the gross amount removed from the contract and the cash paid out.
    """
    return 0.0 if t < 1 else wd_payment_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, for one ``kind`` or, with ``kind=None``, all three."""
    if kind is None:
        return (claims(t, "DEATH") + claims(t, "LAPSE") + claims(t, "MATURITY"))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The Account Value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind=None):
    """Benefit paid less the Account Value released, ``claims - claims_from_av``.

    Signed. Negative on a surrender inside the charge period, where the contract pays out
    less than the Account Value it releases; positive on a death claim where the
    return-of-premium guarantee bites. A reconciliation quantity, not a cash flow of its
    own.
    """
    if kind is None:
        return (claims_over_av(t, "DEATH") + claims_over_av(t, "LAPSE")
                + claims_over_av(t, "MATURITY"))
    return claims(t, kind) - claims_from_av(t, kind)


def inflation_factor(t):
    """``1.025^(y-1)``: the expense inflation factor for the contract year month t is in.

    Keyed on :func:`duration_bom`, so ``y = ceil(t/12)`` and the step falls on the month
    *after* an anniversary: the maintenance expense is incurred over month ``t``, and all
    twelve months of contract year 1 - month 12 included - are charged at the issue level.
    """
    return (1.0 + inflation_rate) ** duration_bom(t)                 # noqa: F821


def expenses(t):
    """Insurer expenses: acquisition at issue and inflating maintenance monthly **[std]**.

    ``0.06 x premium + 200`` at ``t = 0`` and ``60/12 x 1.025^(y-1)`` per contract per
    month thereafter, weighted by :func:`pols_if` - the count entering the month, since
    the expense is incurred over it - with ``y = ceil(t/12)`` the contract year the month
    lies inside (:func:`inflation_factor`). The notes' ledger carries no separate
    commission line - distribution cost sits inside the acquisition expense - so this
    model has no ``commissions`` cells.
    """
    if t == 0:
        return (expense_acq_rate * premium_pp()                      # noqa: F821
                + expense_acq_fixed) * pols_if(t)                    # noqa: F821
    if t < 0 or t > proj_len():
        return 0.0
    return (expense_maint / 12.0) * inflation_factor(t) * pols_if(t)  # noqa: F821


def premium_taxes(t):
    """Premium tax on the purchase payment, 0% **[std]** [S2].

    State-specific and not quantified in any retrieved document; the parameter is exposed
    rather than removed.
    """
    return premium_tax_rate * premiums(t)                            # noqa: F821


def net_cf(t):
    """Net cash flow in policy month t.

    Term-end index credits, the movement of the interim value, the withdrawal charge and
    the roll split between the option and the general accounts are **internal accounting
    entries**: they drive the Investment Amount, the Account Value and the benefit
    *amount*, but are never ledger lines. The option budget is not a liability cash flow
    at all - it is an asset-side flow, and the liability model sees it only through the
    declared cap. Only amounts paid to or received from the contract holder, and the
    insurer's own expenses, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t)
            - expenses(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted Account Value at month t; ``timing`` as in :func:`av_pp_at`.

    ``"BEF_WD"`` carries :func:`pols_if`, the count entering month ``t``. ``"AFT_WD"``
    carries the count *leaving* it, which under the start-of-period convention is
    ``pols_if(t + 1)`` - zero at the Maturity Date, where :func:`pols_maturity` has
    force-annuitized the survivors out and the block's Account Value is released in full.
    """
    if t < 1:
        return av_pp(t) * pols_if(t) if t == 0 else 0.0
    if timing == "BEF_WD":
        return av_pp_at(t, "BEF_WD") * pols_if(t)
    elif timing == "AFT_WD":
        return av_pp(t) * pols_if(t + 1)
    else:
        raise ValueError("invalid timing")


def inv_income(t):
    """The investment return credited to the whole block in month t."""
    return 0.0 if t < 1 else inv_income_pp(t) * pols_if(t)


def wd_from_av(t):
    """The Account Value released by month t's withdrawals, gross of the charge."""
    return 0.0 if t < 1 else wd_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's Account Value over month t."""
    return av_at(t, "AFT_WD") - av_at(t - 1, "AFT_WD")


def roll_fwd_tol():
    """The absolute tolerance the ``check_*`` booleans hold a currency residual to.

    One part in a billion of the purchase payment. The roll-forward identities are
    differences of Account Values of that size, and the option pricer's own rounding sits
    well inside it; a genuine wiring error is orders of magnitude larger.
    """
    return 1e-9 * max(1.0, premium_pp())


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual; zero to floating point for every t >= 1.

    ``AV(t) - AV(t-1) = premium in - withdrawals out + investment return - the Account
    Value released by each of the three claim kinds``. The *cash* paid can differ from the
    Account Value released - by the withdrawal charge retained on a surrender and by the
    return-of-premium excess on a death claim - and that difference is
    :func:`claims_over_av`, not part of this identity. ``t = 0`` is the premium deposit
    itself and is excluded.

    The signed per-month residual, which is what a failing :func:`check_av_roll_fwd` needs
    for diagnosis; the boolean is implemented in terms of it.
    """
    if t < 1:
        return 0.0
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - claims_from_av(t, "DEATH") - claims_from_av(t, "LAPSE")
                - claims_from_av(t, "MATURITY"))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the account value roll-forward closes in **every** projected month.

    No argument and a bool, following ``CashValue_SE.check_av_roll_fwd`` and the rest of
    this library, so one test can call the same check across every model;
    :func:`check_av_roll_fwd_resid` gives the signed residual of a month that fails.
    """
    return all(abs(check_av_roll_fwd_resid(t)) <= roll_fwd_tol()
               for t in range(1, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual; zero to floating point for every t >= 1.

    ``pols_if(t) - pols_if(t+1) = deaths + surrenders + forced annuitizations at the
    Maturity Date``. Both counts are start-of-month, so the month's movements sit between
    the month that is opening and the one that follows it.
    """
    if t < 1:
        return 0.0
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in **every** projected month.

    No argument and a bool; :func:`check_pols_roll_fwd_resid` gives the signed residual.
    The counts are probabilities of order 1, so the tolerance is absolute rather than the
    currency-scaled :func:`roll_fwd_tol`.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-12
               for t in range(1, proj_len() + 1))


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
    return (interim_value_pp_at(t, "BEF_ROLL")
            - inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t)))


def check_term_end_identity():
    """True when ``V_k = IA_k(1 + g)`` holds at **every** Term End Date.

    No argument and a bool, like the two roll-forward checks;
    :func:`check_term_end_identity_resid` gives the signed residual of a term end that
    fails. This is the check the notes ask for by name.
    """
    return all(abs(check_term_end_identity_resid(t)) <= roll_fwd_tol()
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by policy month t from 0 to ``proj_len()``.

    ``t = 0`` carries the purchase payment and the acquisition expense, exactly as the
    notes' cash flow ledger indexes them. The surrender column is ``claims_lapse``,
    matching the ``"LAPSE"`` ``kind`` that produces it, and partial withdrawals sit in
    their own ``withdrawals`` column rather than among the claims - a withdrawal is a
    payment on the owner's election, not a claim. The cash flow columns sum to ``net_cf``
    under the income-positive sign convention: ``premiums`` less every other flow.

    ``pols_if`` is the count in force at the **start** of each month, so it is the weight
    the cash flows on that same row carry - the column and the row reconcile.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed by policy month t.

    ``pols_if`` opens the month, the four movement columns are what leaves it, and
    ``pols_if_aft_decr`` is the notes' end-of-month ``l(t)`` - after death, surrender and
    the term-end concentration, but before the Maturity Date annuitization that
    ``pols_maturity`` carries out.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_lapse_term": [pols_lapse_term(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract values, indexed by policy month t.

    The Investment Amount and Interim Value either side of the month's transaction, the
    Account Value, the general accounts, the return-of-premium base and the surrender and
    death benefits.
    """
    ts = list(range(0, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "inv_amt_pp": [inv_amt_pp(t) for t in ts],
            "interim_value_pp": [interim_value_pp_at(t, "AFT_WD") for t in ts],
            "fixed_acct_pp": [fixed_acct_pp(t) for t in ts],
            "holding_acct_pp": [holding_acct_pp(t) for t in ts],
            "av_pp_bef_wd": [av_pp_at(t, "BEF_WD") for t in ts],
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
    line up with the notes.
    """
    ts = list(range(0, proj_len() + 1))
    out = {
        "index_level": [index_level(t) for t in ts],
        "index_perf": [index_perf(t) for t in ts],
        "tau": [tau(t) for t in ts],
        "fixed_proxy_pp": [fixed_proxy_pp(t) for t in ts],
    }
    for leg in opt_legs():
        out[leg.lower()] = [opt_component_pp(t, leg) for t in ts]
    out["deriv_proxy_pp"] = [deriv_proxy_pp(t) for t in ts]
    out["trading_cost_pp"] = [trading_cost_pp(t) for t in ts]
    out["interim_value_pp"] = [interim_value_pp_at(t, "BEF_ROLL") for t in ts]
    out["inv_amt_pp"] = [inv_amt_pp_at(t, "BEF_ROLL") for t in ts]
    return pd.DataFrame(out, index=pd.Index(ts, name="t"))           # noqa: F821


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

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

math = ("Module", "math")

pd = ("Module", "pandas")