# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. registered index-linked annuities (RILA).

:mod:`~.RILA_US_S` is the executable counterpart of
``products/registered_index_linked_annuity/technical-notes.md`` in the
lifelib-products library. It projects gross liability cash flows for a single-contract
model point of a single-premium buffered index-linked deferred annuity: one purchase
payment allocated to one index-linked option, a 10% buffer, Cap / Step / Edge crediting
over a 1, 3 or 6 year point-to-point term, a 7-7-6-5-4-3-0 withdrawal charge above a 10%
free amount, a return-of-premium GMDB, no explicit asset-based charge, and — the
mechanic that defines the product — an **Actuarial Guideline LIV Interim Value** at which
every mid-term transaction settles.

That interim value is why this model carries an option pricer. AG 54 makes the value of a
hypothetical replicating portfolio of European options plus a fixed income proxy the
contractual value for every mid-term withdrawal, surrender, death benefit, annuitization
and transfer [R2], and the source prospectuses implement exactly that with Black-Scholes
[S2][S6]. No other product in this library has a contractual value that cannot be computed
without a derivatives pricer. The three components the notes separate — the crediting
engine, the interim-value engine and the market-data provider — are separate here too:
:func:`~.RILA_US_S.Projection.credit_rate_term` credits,
:func:`~.RILA_US_S.Projection.iv_factor` prices, and
:mod:`~.RILA_US_S.Data` supplies the market state.

This model is built on the **deferred annuity base chassis**,
:mod:`.MYGA_US_S`, and shares its cells names for every concept the two have
in common — ``av_pp``, ``av_pp_at``, ``free_wd_allow``, ``surr_charge_rate``,
``surr_value_pp``, ``pols_if_at``, ``claim_pp``, ``check_av_roll_fwd``. Where the RILA
notes restate a recursion with product-specific parameters, this model follows the RILA
notes, not the chassis: there is **no market value adjustment on the contract**, no Model
#805 minimum guaranteed surrender value (AG 54 displaces Model #805 outright [R2]
[REG-R42][REG-R44]), and the account value is a derivative price rather than a book value.

**Spaces.** The model contains two:

:mod:`~.RILA_US_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.RILA_US_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single
    :mod:`~.RILA_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps. ``t`` counts **policy months**, and following the
notes ``t`` denotes **month ends**, with ``t = 0`` the Issue Date. Complete contract years
are ``duration(t) = t // 12`` — the notes' ``cy(t) = floor(t/12)`` — so an anniversary
month ``t = 12, 24, ...`` already counts as a completed year, and ``policy_year(t) =
duration(t) + 1``. Note the contrast with :mod:`.Term_US_A`, where ``t`` counts **years**,
and the smaller contrast with :mod:`.MYGA_US_S`, whose beginning-of-month
transaction convention makes its ``duration(t)`` ``ceil(t/12) - 1``: on a month-end
convention the anniversary belongs to the year that just closed. That month-end reading is
right for what is read *at* the instant ``t`` — the withdrawal charge a transaction
settling there bears, the free-withdrawal base snapshotted there, and the surrender
behaviour keyed to that charge — but wrong for a rate applied *across* month ``t``, so the
attained age behind ``q_m(t)`` and the expense inflation step are keyed on the interval
reading ``duration_bom(t) = ceil(t/12) - 1`` instead: all twelve months of contract year 1,
month 12 included, are charged at ``q_x`` and at the issue expense level. The two readings
differ only in anniversary months. The contractual interim
value is a *daily* quantity [S2][S4][S6]; the model evaluates it at each month end
**[std]**, which resolves every contractual boundary because terms are whole years, the
withdrawal-charge schedule runs by complete contract years and the free-withdrawal limit
resets annually [S1][S2].

``proj_len()`` is ``12 * policy_term()`` months, and ``policy_term()`` is the Maturity
Date rule: the later of the anniversary after the oldest owner's age 90 and ten years
[S2] — 360 months on the anchor cell. The survivors there are force-annuitized through
:func:`~.RILA_US_S.Projection.pols_maturity`.

The month's processing order follows the notes' step list exactly. **Market state** (the
index level, the Market Value Rate, the implied volatility and the dividend yield are
refreshed from the scenario); **term-end crediting** (at a Term End Date the completed
term's index performance ``R`` is turned into a crediting rate ``g`` and the Investment
Amount rolls to ``IA(1 + g)``); **renewal and transfer** (the 80 / 15 / 5 roll split, and
the option is re-struck at the prevailing index level, the new declared cap and a fresh
option budget ``beta``); **interim values** (fixed income proxy, derivative asset proxy,
trading costs); **accounts** (the Fixed and Holding Accounts accrue, the Account Value is
set, and on a Contract Anniversary the free-withdrawal base is snapshotted); **contract
holder transactions** (the withdrawal is allocated, charged, and reduces the Investment
Amount **proportionally** and the return-of-premium base proportionally); and finally
**decrements** at the end of the month — death at ``q_m(t)``, then surrender at ``w_m(t)``
on survivors **[std order]**, plus the discrete term-end surrender fraction ``phi`` if
``t`` is a Term End Date.

``t = 0`` is the Issue Date. The single premium and the acquisition expense fall there,
as they do in the notes' cash flow ledger, and ``inv_amt_pp(0)``, ``rop_pp(0)`` and
``pols_if(0)`` are the initial branches of the recursions, so ``result_cf()`` starts at
``t = 0`` rather than ``t = 1``.

In-force counts follow the library-wide convention: ``pols_if(t)`` is the number in force
at the **start** of month ``t`` and is the weight applied to that same month's cash flows,
so ``pols_if(1) = pols_if_init()`` as in :mod:`.Term_US_A` and the ``pols_if`` column of
``result_cf()`` reconciles against the row it sits on rather than the next one. The notes'
own **end**-of-month ``l(t)`` is not lost: it is ``pols_if_at(t, "AFT_DECR")``, the last
point of the decrement chain. Surrender rates follow the ``mort_rate`` / ``mort_rate_mth``
pair - ``lapse_rate(t)`` is the notes' annual ``w_annual(y,t)`` and ``lapse_rate_mth(t)``
its monthly ``w_m(t)``, which is what the decrement chain reads.

**Undiscounted.** Like every model in this library, this one projects *gross liability
cash flows* only; reserves and discounting are a separate layer, and the notes' Valuation
and reserve pointers section cites AG 54, VM-21 and C-3 Phase II rather than reproducing
them. The discounting that lives *inside* the benefit formula — the fixed income asset
proxy's ``((1 + r_0) / (1 + r(t)))^tau`` market value adjustment factor, and the
Black-Scholes discount factors — is contractual and stays.

**What is sourced and what is not.** Contractual: the 10% buffer, the 1/3/6 year term
menu, the guaranteed minimum Cap / Step / Edge rates of 2% / 6% / 8% by term, the 1%
minimum on the Fixed and Holding Accounts, the 7-7-6-5-4-3-0 withdrawal charge and its
non-gross-up, the zero free amount in contract year 1 and 10% of the prior anniversary's
Account Value thereafter, the return-of-premium death benefit for issue ages 80 and
under, the Maturity Date rule, the Transfer Period during which the interim value equals
the Investment Amount, and the interim value algebra itself with its straight-line
option-budget amortization and CMT discount [S1][S2][S4][S5][S6][R2].

Everything else is a standardization. The declared Cap / Step / Edge rates of 100% / 8% /
6% and the 3.00% Fixed Account rate are a snapshot — **no current rate sheet was
retrievable**, both insurer rate pages returning HTTP 403. The market data that the
contractual formula consumes is a flat scalar surface: a 4.00% risk-free rate, a 2.00%
dividend yield and a 20.00% implied volatility. The 0.10% trading cost factor matches only
the order of magnitude implied by [R6], and the two free parameters of the alternative
interim-value family (b) are **[std]** on the same footing: the investment-grade discount
spread ``iv_credit_spread`` = 1.00%, which no source quantifies ([S4] says only that the
rate is above swap rates), and the Cap Calculation Factor's expense rate
``iv_expense_rate`` = 0.10%, which [S4] gives only as a dollar illustration. All
behaviour is **[std]** — the base surrender
shape, the 3.0 charge-expiry shock multiplier, the interim-value moneyness suppression
``M_iv``, the term-end concentration ``phi``, the 80 / 15 / 5 roll split, the 2% partial
withdrawal rule, the 100% mortality A/E, the $60 per contract per year maintenance
expense and the 6% + $200 acquisition expense — and the shipped mortality table is an
illustrative curve, *not* the prescribed 2012 IAM Basic table with Scale G2.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the assumption tables and the market data with company data before drawing any conclusion
from the output.

**Not implemented.** Named here so the gaps cannot be mistaken for oversights.
*Performance Lock*: the notes give the election rule and the dollar-for-dollar withdrawal
consequence but not the rate at which a locked bucket accrues to term end, so the module
is incomplete and is left out rather than guessed. *Tiered participation rate*: the notes
give its replicating portfolio but no crediting formula ``g``. *Dual-direction and
absolute-return designs, annual-lock segments, rainbow segments and resetting locks*:
listed as out of scope by the product spec, with no formula. *RMD-driven withdrawals*:
named as a behavioural input, with no amount formula. *Multi-option contracts*: the notes
define a model point as one contract holding one option and describe the multi-option
case as a vector sharing one contract-level decrement and guarantee base; this model
carries the single-option case, and the pro-rata-to-interim-value allocation rule is
implemented over the option, the Fixed Account and the Holding Account rather than over
several options.
*The payout phase*: the Maturity Date benefit is emitted as an outgo at the Account Value;
converting it to a payment stream is the immediate-annuity chassis. *Stochastic
scenarios*: the index path, the CMT curve, the volatility and the dividend yield are read
from a deterministic scenario table, and the Academy's regression grid [R6] would be run
by supplying more scenarios, not by changing formulas. *A volatility surface*: the notes
call the flat-surface approximation the single largest simplification in the model, and it
is one this implementation makes. *check_margin()*: on this chassis the cap *is* the fee —
no charge is deducted from index-linked value — so there is no charge-versus-cost
decomposition to check; :func:`~.RILA_US_S.Projection.check_av_roll_fwd`
and :func:`~.RILA_US_S.Projection.check_pols_roll_fwd` are implemented
and both close to floating point. Each ``check_*`` takes **no argument and returns a
bool** over every projected month, as ``CashValue_SE`` does, with the signed per-month
residual available as ``check_*_resid(t)`` for a debugging session.

**Model points.** ``model_point_table.csv`` carries fifteen contracts. Points 1 and 2 are
the worked example's anchor cell — male 60, $100,000 single premium, one 6-year option,
10% buffer, Cap crediting at a declared 100% cap — run on the notes' Scenario A and
Scenario B respectively, point 2 carrying the illustrative $8,000 withdrawal at the term
midpoint. Point 3 is the same contract with the notes' base *behavioural* withdrawal rule
switched on, which is the second reading of a place where the notes contradict themselves
(see the README). Points 4 to 14 exercise every branch the notes specify: Step, Edge and
Floor crediting; interim value families (b) and (c) and the pre-AG 54 time-prorated
engine; the updated-time-to-expiry amortization convention; a participation rate above
100% on a 20% buffer; an uncapped Cap option; the NGE cap-solve; a withdrawal above the
free amount, so the withdrawal charge and its non-gross-up are live; and, at issue age 81,
the death benefit band in which the return-of-premium guarantee does not apply. Point 15
is the notes' *second* labelled verification: it runs the pre-AG 54 engine on a scenario
whose index level makes the accrued crediting rate exactly -20% at month 60, which puts an
Account Value of exactly $80,000 at the start of contract year 6 and so reproduces the
[S2] withdrawal-charge example — $8,000 free, $72,000 chargeable, a 3% charge of $2,160
and a $77,840 cash surrender value — end to end rather than by re-deriving it. A test
asserts every point projects to completion.

**Verification.** ``tests/test_registered_index_linked_annuity_us.py`` asserts every row
and every column of the notes' worked example table — all six rows and all thirteen
columns, money to the cent — together with the trace beneath it: the option budget
``beta = 10.0632%``, the fixed leg opening at $89,936.81, its 1.7834% equivalent accretion
yield and the 2.22% implied spread, the $2,687.62 cost of the 100 bp rate rise, the
counterfactual interim values without the rate move, the $1,433.62 excess of notional lost
over cash withdrawn, and the term-end identity ``V = IA(1 + g)`` for every crediting type.
The [S2] withdrawal-charge example is asserted on model point 15 — $80,000 of Account
Value at the start of contract year 6 giving a $2,160 charge and a $77,840 cash surrender
value — and the pre-AG 54 engine reproduces the $52,500 of the [S1] worked example. There
is one test per entry in the notes' "Known modeling pitfalls" list, and three more that
hold the documentation to the model: the two readings of the contract year, the timing
literals the ``Projection`` docstring prints, and the **[std]** marks on the invented
interim-value parameters.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model(
    ...     "products/registered_index_linked_annuity/RILA_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "RILA_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

