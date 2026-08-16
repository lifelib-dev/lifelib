# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. current-assumption universal life.

:mod:`~.UL_US_S` is the executable counterpart of
``products/universal_life/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-life, flexible-premium adjustable
(universal) life policy on the current-assumption chassis: a declared credited rate
above a contractual minimum, a monthly deduction of per-policy, per-unit and cost-of-
insurance charges, Guideline Premium Test death benefit options A and B, a nine-year
surrender charge run-off, and no maturity date -- charges and premiums cease at
attained age 121 and coverage continues for life.

**Spaces.** The model contains two:

:mod:`~.UL_US_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.UL_US_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.UL_US_S.Data`
    Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. Policy month ``t`` runs 1, 2, ...,
``proj_len()``, where ``t = 1`` is the **issue month** of a new-business model point
and ``proj_len() = 12 * (omega_age - age_at_entry() + 1) - duration_mth_init()``, so
the projection ends with the policy year in which the insured attains ``omega_age``
(120), the last age of the mortality table, where the annual rate is 1.0. For an
in-force model point ``duration_mth_init()`` is the number of completed policy months
already elapsed at ``t = 1``. The contract itself has no maturity date [S2][S3];
``pols_maturity(t)`` is therefore identically zero and the projection is truncated by
mortality, not by the contract.

Within each month the notes' monthiversary order is followed exactly. At the beginning
of the month (BOM): surrender-charge amortization, gross premium and its load,
withdrawal and withdrawal fee, death benefit and corridor test, net amount at risk,
monthly deduction, shortfall test. At the end of the month (EOM): one month's interest
on the post-deduction balance, loan interest accrual, then the decrements -- death
before lapse. Premiums, expenses and premium taxes therefore fall at BOM and are
weighted by ``pols_if(t)``; death claims are weighted by
``pols_if(t) * mort_rate_mth(t)`` and surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``. ``net_cf(t)`` is
income-positive -- premiums less claims, withdrawals, expenses and premium taxes --
and ``result_cf()`` publishes the flows in the columns ``premiums``, ``claims_death``,
``claims_lapse``, ``withdrawals``, ``expenses`` and ``premium_taxes``. A partial
withdrawal is a payment on the owner's election, not a claim, so it is
``withdrawals(t)`` and not a ``kind`` of ``claims(t, kind)``.

Reversing the deduction/interest order overstates the account value by about one
month's interest on the deduction every month, which compounds over the eighty-plus
years this projection runs; the notes list it first among the modelling pitfalls, and
``check_av_roll_fwd()`` pins the order.

**What is sourced and what is not.** The contractual mechanics come from a specimen
policy [S3] and the composite product spec: the guaranteed maximum monthly COI scale
at the anchor cell, the $7.50 per-policy and $0.26/$0.156 per-unit charges, the
Guideline Premium Test corridor factor table, the specimen's net-amount-at-risk
convention (death benefit discounted one month at the *guaranteed* rate, account value
measured *before* the deduction), the nine-year monthly surrender-charge amortization,
the 0.75% loan spread, and the cessation of charges at attained age 121. Everything
else is a standardization introduced for the reference implementation: the 2.00%
guaranteed and 4.00% current credited rates, the 6% current premium load, the 60%
current-to-guaranteed COI factor, the $9.00 per $1,000 initial surrender charge, the
best-estimate mortality table, the rate-class factors, the base lapse vector, the
surrender-charge-expiry lapse shock, the dynamic-lapse formula, the premium
persistency scale, the $75 per policy per year maintenance expense inflating at 2.5%,
and the 2.5% percent-of-premium expense. Insurers do not publish current credited
rates or current COI scales, so the two assumptions that matter most for this product
are both **[std]**. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**Not implemented.** Modules the technical notes describe but do not specify
completely enough to project, all named here and in the README so their absence is not
mistaken for an oversight:

* The grace and lapse-for-insufficiency cascade. The trigger and the required cure
  payment are complete formulas and are implemented as the diagnostics
  :func:`~.UL_US_S.Projection.is_shortfall` and
  :func:`~.UL_US_S.Projection.cure_premium_pp`, but the notes leave the
  in-grace account value treatment (deductions accrue "due and unpaid") and the cash
  flow of a cure payment undetermined, so no policy is terminated for insufficiency
  and no in-grace state is carried -- the notes' ``grace_flag(t)`` has no cells.
  **This absence bites on a shipped model point.** Point 2 enters shortfall in policy
  year 57 and stays there for the last 356 of its 1,032 months: deductions keep being
  taken from an account value that is already empty, which ends about $1.84m
  overdrawn. Cash flows past the trigger month of a model point in shortfall are not
  meaningful. What the model does *not* do is let that negative balance reach the
  death benefit: :func:`~.UL_US_S.Projection.av_pp_db_basis` floors it at zero
  **[std]**, so an Option B death benefit is never below the face amount and no death
  claim is ever negative.
* Reinstatement -- a contractual provision only, out of scope in the notes.
* NGE revision. The notes' rule ``i_cr(t) = max(i_guar, earned_rate(t) - spread)``
  needs an earned-rate input the notes do not supply; the base run holds the snapshot
  scale level, which is what the notes prescribe.
* New policy loans and loan repayments. Loan *interest accrual* on an opening balance
  is implemented (the notes give the formula); no loan utilization pattern is given,
  so ``loan_bal_pp(t)`` only rolls forward the model point's opening balance.
* Face increases and decreases, option changes, and the surrender-charge layering
  that goes with them. Withdrawal-driven face reduction under Option A *is*
  implemented.
* Riders. ``rider_charge_pp(t)`` is the notes' placeholder term, zero in the base
  model.
* MEC status has no cash flow consequence for the insurer, so
  :func:`~.UL_US_S.Projection.is_mec` flags and does not project. The flag does
  **latch**, though: 7702A status is permanent once the 7-pay test fails, so once true
  it stays true for the rest of the projection.
* Withdrawal *utilization*. The mechanics are complete -- the fee, the notes' annual
  free-amount rule with its ``wd_used_year`` state, and the Option A face reduction --
  but the notes give no utilization pattern, so every shipped model point withdraws
  nothing.

**Model points.** ``model_point_table.csv`` carries three points, all on the anchor
configuration M35 / StdNT / $100,000, because the specimen gives a guaranteed COI
scale for that cell alone. Point 1 is the technical notes' worked-example anchor:
Option A, $1,800 planned annual premium, no opening account value and no loan. Point 2
switches the death benefit to Option B, which makes the corridor and the increasing
net amount at risk live -- and, from policy year 57, the shortfall trigger too, so it
doubles as the model point that exhibits the missing grace cascade above. Point 3 is
an in-force cell at 120 completed policy months
with an opening account value of $15,000 and a $2,000 loan, which exercises the
duration offset, the expired surrender charge and the loan roll-forward. A model point
on any other issue age, sex or class requires ``coi_rates.csv`` to be extended first; a
test asserts every model point in the table actually projects.

**Verification.** Model point 1 is the anchor cell of the worked example in the
technical notes, and ``tests/test_universal_life_us.py`` asserts every cell of all
three of its rows -- account value, net premium, death benefit, net amount at risk,
cost of insurance, monthly deduction, post-deduction balance and credited interest --
to the cent, together with the notes' month-1 trace at full precision.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/universal_life/UL_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "UL_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

