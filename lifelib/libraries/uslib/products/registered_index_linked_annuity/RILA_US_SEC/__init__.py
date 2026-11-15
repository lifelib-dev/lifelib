# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. registered index-linked annuities.

:mod:`~.RILA_US_SEC` projects the contracts :mod:`~.RILA_US_S` projects — a
single-premium buffered index-linked deferred annuity: one purchase payment allocated to
one index-linked option, a 10% buffer, Cap / Step / Edge crediting over a 1, 3 or 6 year
point-to-point term, a 7-7-6-5-4-3-0 withdrawal charge above a 10% free amount, a
return-of-premium GMDB, no explicit asset-based charge, and an **Actuarial Guideline LIV
Interim Value** at which every mid-term transaction settles — from a **valuation date**
rather than from issue. A model point may be a contract already in force at that date, in
any month of any term, one issued at that date, or one issued in the ten years after it,
as in lifelib's ``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S`` the
same way. Its formulas are the executable counterpart of
``products/registered_index_linked_annuity/technical-notes.md``, and
``products/registered_index_linked_annuity/model-sec.md`` explains what running in force
changes. On a contract issued at the valuation date it is :mod:`~.RILA_US_S`, number for
number.

That interim value is why this model carries an option pricer. AG 54 makes the value of a
hypothetical replicating portfolio of European options plus a fixed income proxy the
contractual value for every mid-term withdrawal, surrender, death benefit, annuitization
and transfer [R2], and the source prospectuses implement exactly that with Black-Scholes
[S2][S6]. No other product in this library has a contractual value that cannot be computed
without a derivatives pricer. The three components the notes separate — the crediting
engine, the interim-value engine and the market-data provider — are separate here too:
:func:`~.RILA_US_SEC.Projection.credit_rate_term` credits,
:func:`~.RILA_US_SEC.Projection.iv_factor` prices, and
:mod:`~.RILA_US_SEC.Data` supplies the market state.

This model is built on the **deferred annuity base chassis**, :mod:`.MYGA_US_S`, as
:mod:`~.RILA_US_S` is, and shares its cells names for every concept the two have in
common — ``av_pp``, ``av_pp_at``, ``free_wd_allow``, ``surr_charge_rate``,
``surr_value_pp``, ``pols_if_at``, ``claim_pp``, ``check_av_roll_fwd``. Where the RILA
notes restate a recursion with product-specific parameters, this model follows the RILA
notes, not the chassis: there is **no market value adjustment on the contract**, no Model
#805 minimum guaranteed surrender value (AG 54 displaces Model #805 outright [R2]
[REG-R42][REG-R44]), and the account value is a derivative price rather than a book value.

**Spaces.** The model contains two:

:mod:`~.RILA_US_SEC.Data`
    Reads the five assumption CSVs it shares with :mod:`~.RILA_US_S`, its own model point
    table and its own market scenarios, and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.RILA_US_SEC.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.RILA_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every model point. In ``Data`` they are evaluated once,
however many contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the valuation
date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the valuation month
for every model point, however long the contract has been in force, and the frame runs
``t = 0, 1, ..., proj_len() - 1``, where ``proj_len()`` counts the months from the
valuation date to the Maturity Date. ``duration_mth(t)`` counts the policy months elapsed
from issue, ``duration_mth_init() + t`` from the model point's ``duration_mth`` at
``t = 0``, and the contract runs on it: the terms and their Term Start and End Dates, the
Contract Anniversaries, the withdrawal charge schedule, the attained age, the withdrawal
programme and the Maturity Date. The market runs on ``t``, the valuation clock every point
of a block shares, and so does expense inflation, so the maintenance charge is in
valuation-date dollars. Following the notes, every within-month quantity is evaluated at
the month **end**, time ``t + 1``, while ``pols_if(t)`` is the count entering the month at
time ``t``; the month-end convention is forced here by the term structure, whose crediting
dates are contract-month boundaries.

**In force at the valuation date.** A contract in force opens from its opening state on
the model point, what :mod:`~.RILA_US_S` carries into the valuation month: the Investment
Amount, the Fixed and Holding Accounts, the Account Value, the Account Value at the
anniversary on or before the valuation date, the Free Withdrawal Amount still unused and
the return-of-premium base, and, where the term under way began before the valuation
month, the index level, the Market Value Rate and the option-pricing market of its Term
Start Date, with the cap re-solved there at a renewal under ``nge_reset``. A term that
starts at or after the valuation month reads its start from the market scenario, which
for each point restated in force or issued later is a copy of its scenario re-based to
its month. A contract issued at or after the valuation date opens as at issue, its
purchase payment, acquisition expense and count falling in its issue month.

``proj_len()`` refuses a point at or past its Maturity Date, and the Maturity Date is
:mod:`~.RILA_US_S`'s rule: the later of the anniversary after the oldest owner's age 90
and ten years [S2] — policy month 360 on the anchor cell, whose survivors are
force-annuitized through :func:`~.RILA_US_SEC.Projection.pols_maturity` at the end of
policy month 359.

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
behaviour is **[std]** — the base surrender shape, the 3.0 charge-expiry shock multiplier,
the interim-value moneyness suppression ``M_iv``, the term-end concentration ``phi``, the
80 / 15 / 5 roll split, the 2% partial withdrawal rule, the 100% mortality A/E, the $60
per contract per year maintenance expense and the 6% + $200 acquisition expense — and the
shipped mortality table is an illustrative curve, *not* the prescribed 2012 IAM Basic
table with Scale G2. The model reads :mod:`~.RILA_US_S`'s assumption tables in place,
every assumption unchanged. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables and the market data with company data
before drawing any conclusion from the output.

**Not implemented.** Named here so the gaps cannot be mistaken for oversights.
*Performance Lock*: the notes give the election rule and the dollar-for-dollar withdrawal
consequence but not the rate at which a locked bucket accrues to term end, so the module
is incomplete and is left out rather than guessed, in :mod:`~.RILA_US_S` and so here: an
in-force contract carries no lock flag and no locked value. *Tiered participation rate*:
the notes give its replicating portfolio but no crediting formula ``g``.
*Dual-direction and absolute-return designs, annual-lock segments, rainbow segments and
resetting locks*: listed as out of scope by the product spec, with no formula.
*RMD-driven withdrawals*: named as a behavioural input, with no amount formula.
*Multi-option contracts*: the notes define a model point as one contract holding one
option and describe the multi-option case as a vector sharing one contract-level
decrement and guarantee base; this model carries the single-option case, and the
pro-rata-to-interim-value allocation rule is implemented over the option, the Fixed
Account and the Holding Account rather than over several options. *The payout phase*: the
Maturity Date benefit is emitted as an outgo at the Account Value; converting it to a
payment stream is the immediate-annuity chassis. *Stochastic scenarios*: the index path,
the CMT curve, the volatility and the dividend yield are read from a deterministic
scenario table, and the Academy's regression grid [R6] would be run by supplying more
scenarios, not by changing formulas. *A volatility surface*: the notes call the
flat-surface approximation the single largest simplification in the model, and it is one
this implementation makes. *check_margin()*: on this chassis the cap *is* the fee — no
charge is deducted from index-linked value — so there is no charge-versus-cost
decomposition to check; :func:`~.RILA_US_SEC.Projection.check_av_roll_fwd` and
:func:`~.RILA_US_SEC.Projection.check_pols_roll_fwd` are implemented and both close to
floating point. Each ``check_*`` takes **no argument and returns a bool** over every
projected month, as ``CashValue_SE`` does, with the signed per-month residual available
as ``check_*_resid(t)`` for a debugging session.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.RILA_US_S`'s
table and never typed by hand: :mod:`~.RILA_US_S`'s fifteen contracts as twins, issued at
the valuation date, seven of them restated in force, in eight rows, at months chosen for
the product's events, and the anchor cell issued thirteen months after the valuation date.
Its market scenarios, ``market_scenario_sec.csv``, are :mod:`~.RILA_US_S`'s, then each
restated or later row's own copy, re-based to its month. ``model-sec.md`` lists the rows
and why each is there.

**Verification.** ``tests/test_model_conventions.py`` compares every cell of each twin
with :mod:`~.RILA_US_S`'s at every argument :mod:`~.RILA_US_S` caches, so every worked
example :mod:`~.RILA_US_S`'s own tests assert, the notes' interim-value table and the
[S2] withdrawal-charge example among them, holds here too; and
``tests/test_registered_index_linked_annuity_us_sec.py`` restates :mod:`~.RILA_US_S`'s
points in force at months across their terms and holds each to :mod:`~.RILA_US_S` from
there on, cell by cell.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model(
    ...     "products/registered_index_linked_annuity/RILA_US_SEC")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "RILA_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

