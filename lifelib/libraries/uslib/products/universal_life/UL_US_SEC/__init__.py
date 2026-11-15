# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. current-assumption universal life.

:mod:`~.UL_US_SEC` projects the policy :mod:`~.UL_US_S` projects -- a single-life,
flexible-premium adjustable (universal) life policy on the current-assumption chassis: a
declared credited rate above a contractual minimum, a monthly deduction of per-policy,
per-unit and cost-of-insurance charges, Guideline Premium Test death benefit options A
and B, a nine-year surrender charge run-off, and no maturity date, charges and premiums
ceasing at attained age 121 and coverage continuing for life -- from a **valuation
date** rather than from the start of a projection of its own. A model point may be a
policy already in force at that date, in any month of its policy year, one issued at it,
or one to be issued in the ten years after it, as in lifelib's ``basiclife/BasicTerm_SE``,
which extends ``basiclife/BasicTerm_S`` the same way. Its formulas are the executable
counterpart of ``products/universal_life/technical-notes.md``, and
``products/universal_life/model-sec.md`` explains what running in force changes.

**Spaces.** The model contains two:

:mod:`~.UL_US_SEC.Data`
    Reads the seven assumption CSVs it shares with :mod:`~.UL_US_S` and its own model
    point table, and holds their filename References. It checks the model point table as
    it reads it, the keys and the rates of every table read at a policy year or an
    attained age, the class factors and the surrender-charge schedules. It takes no
    parameters, so each file is read **once per model**. It hands the projection what the
    files hold as numpy vectors and arrays of numbers, one element per model point, per
    key or per schedule.

:mod:`~.UL_US_SEC.Projection`
    The by-policy projection, parameterized by ``idx``, the position of a model point in
    the ``Data`` vectors, as ``basiclife.BasicTerm_SC`` is: ``Projection[0]`` is an
    ItemSpace projecting the table's first row, model point 1, and its ``point_id()`` is
    that label. It reaches the inputs through its ``data`` Reference, which resolves to
    the single :mod:`~.UL_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Compiled.** The model compiles under modelx-cython into C-typed code, as
``basiclife/BasicTerm_SC`` does, from the two inputs beside it: ``sample_sec.py``, the run
that types each cell, and ``spec_sec.py``, the length of each cell's cache.
``Projection``'s cells read every model point attribute a projection cell uses as a C
number from a ``Data`` vector at ``idx``, and every table as an array indexed by integers;
a timing or a kind is an int code; and every cell but the reports, ``model_point`` and six
label accessors returns a C ``bint``, ``long long`` or ``double``, cached as a single
value or in a C array sized from the contract. modelx reads and runs the same formulas,
and computes the same numbers. ``products/universal_life/model-sec.md`` says how to
compile and run it, and what the compiled model does not do as modelx does: it clears no
cache when a Reference is set, so every Reference is set on a model just imported.

**Projection basis.** Monthly steps on two clocks. ``t`` counts months from the
valuation date, 0-based, as ``basiclife/BasicTerm_SE`` counts them: ``t = 0`` is the
valuation month for every model point, however old the policy, and the frame runs
``t = 0, 1, ..., proj_len() - 1``, where ``proj_len() = omega_mth() - duration_mth_init()``
counts the months from the valuation date to the end of the projection. That ends with
the policy year in which the insured attains ``omega_age`` (120), the last age of the
mortality table, where the annual rate is 1.0: ``omega_mth()`` is the first policy month
at attained age 121. ``duration_mth(t)`` counts the months the policy has been in force,
``duration_mth_init() + t`` from the model point's ``duration_mth`` at ``t = 0``, and the
contract runs on it: ``policy_year(t) = duration(t) + 1`` is the 1-based contractual
label, ``duration(t) = duration_mth(t) // 12``, derived and never indexed by. The
contract itself has no maturity date [S2][S3]; ``pols_maturity(t)`` is therefore
identically zero and the projection is truncated by mortality, not by the contract, so
where lives survive the last month the count and the account value they carry into
``t = proj_len()`` are kept, and the roll-forwards close on them. Expense inflation and the
two declared rates run on ``t``: the rates flat as shipped, and inflation stepping on the
valuation anniversaries, so the maintenance expense is in valuation-date dollars;
acquisition is charged per policy issued, in the issue month, and is not inflated, as in
``basiclife/BasicTerm_SE``. On a point issued at ``t = 0`` the
two clocks coincide, and the model computes what :mod:`~.UL_US_S` computes.

Within each month the notes' monthiversary order is followed exactly: at the beginning
of the month (BOM), surrender-charge amortization, gross premium and its load,
withdrawal and withdrawal fee, death benefit and corridor test, net amount at risk,
monthly deduction, shortfall test; at the end of the month (EOM), one month's interest
on the post-deduction balance, loan interest accrual, then the decrements -- death
before lapse. Premiums, expenses and premium taxes therefore fall at BOM and are
weighted by ``pols_if(t)``; death claims are weighted by
``pols_if(t) * mort_rate_mth(t)`` and surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``. ``net_cf(t)`` is
income-positive -- premiums less claims, withdrawals, expenses and premium taxes --
and ``result_cf()`` publishes the flows in the columns ``premiums``, ``claims_death``,
``claims_lapse``, ``withdrawals``, ``expenses`` and ``premium_taxes``. A partial
withdrawal is a payment on the owner's election, not a claim, so it is
``withdrawals(t)`` and not a claim of either kind, ``claims_death(t)`` or
``claims_lapse(t)``, nor of their total, ``claims(t)``.

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
  :func:`~.UL_US_SEC.Projection.is_shortfall` and
  :func:`~.UL_US_SEC.Projection.cure_premium_pp`, but the notes leave the
  in-grace account value treatment (deductions accrue "due and unpaid") and the cash
  flow of a cure payment undetermined, so no policy is terminated for insufficiency
  and no in-grace state is carried -- the notes' ``grace_flag(t)`` has no cells.
  **This absence bites on a shipped model point.** Point 2 enters shortfall in policy
  year 57 and stays there for the last 356 of its 1,032 months, and point 7, the same
  policy restated in force at that month, is in shortfall throughout: deductions keep
  being taken from an account value that is already empty, which ends about $1.84m
  overdrawn. Cash flows past the trigger month of a model point in shortfall are not
  meaningful. What the model does *not* do is let that negative balance reach the
  death benefit: :func:`~.UL_US_SEC.Projection.av_pp_db_basis` floors it at zero
  **[std]**, so an Option B death benefit is never below the face amount and no death
  claim is ever negative. Nor does it take such a balance in as opening state: no
  policy in force holds one, so the model point table refuses a negative account value.
* Reinstatement -- a contractual provision only, out of scope in the notes.
* NGE revision. The notes' rule ``i_cr(t) = max(i_guar, earned_rate(t) - spread)``
  needs an earned-rate input the notes do not supply; the base run holds the snapshot
  scale level, which is what the notes prescribe.
* New policy loans and loan repayments. Loan *interest accrual* on an opening balance
  is implemented (the notes give the formula); no loan utilization pattern is given,
  so ``loan_bal_pp(t)`` only rolls forward the model point's opening balance.
* Face increases and decreases, option changes, and the surrender-charge layering
  that goes with them. Withdrawal-driven face reduction under Option A *is*
  implemented, and a point in force carries the face its withdrawals have left.
* Riders. ``rider_charge_pp(t)`` is the notes' placeholder term, zero in the base
  model.
* MEC status has no cash flow consequence for the insurer, so
  :func:`~.UL_US_SEC.Projection.is_mec` flags and does not project. The flag does
  **latch**, though: 7702A status is permanent once the 7-pay test fails, so once true
  it stays true for the rest of the projection, and a point in force carries the latch
  in from before the valuation date.
* Withdrawal *utilization*. The mechanics are complete -- the fee, the notes' annual
  free-amount rule with its ``wd_used_year`` state, and the Option A face reduction --
  but the notes give no utilization pattern, so every shipped model point withdraws
  nothing.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.UL_US_S` and
its model point table, and the tests regenerate it and compare, so no row is typed by
hand. Every point is on the anchor configuration M35 / StdNT / $100,000, because the
specimen gives a guaranteed COI scale for that cell alone. Points 1 to 3 are the twins of
:mod:`~.UL_US_S`'s three points: point 1, the technical notes' worked-example anchor,
Option A with a $1,800 planned annual premium, issued at the valuation date; point 2,
the same on Option B, which makes the increasing net amount at risk live, and, from policy
year 57, the shortfall trigger; and point 3, the in-force cell,
120 completed policy months at the valuation date with an account value of $15,000 and
a $2,000 loan. Points 4 to 8 are S points restated in force at an S month, each opened
with the state :mod:`~.UL_US_S` carries into that month: point 1 on its first
anniversary, inside the surrender-charge period; point 1 at month 113, in the middle of
the lapse-shock year; point 3 six months on, at policy month 126, mid-year with its loan;
point 2 at month 676, the month its shortfall begins; and point 1 at month 1,008, the
first month at attained age 119, where the mortality rate reaches 1.0 and every survivor
dies. Point 9 is point 1 to be issued 25 months after the valuation date. A model point
on any other issue age, sex or class requires ``coi_rates.csv`` to be extended first; a
test asserts every model point in the table actually projects.

**Verification.** On the two twins issued at the valuation date every cell this model
shares with :mod:`~.UL_US_S` agrees with it at every argument the S model evaluates in
its sweep, ``pols_if_init``, ``model_point``, ``result_pols`` and ``coi_rate_scale``
excepted, S's ``claims(t, None)`` compared as :func:`~.Projection.claims`, so the goldens
``tests/test_universal_life_us.py`` asserts on them hold here too, with no number
restated: every cell of all three rows of the technical notes' worked example on point 1,
to the cent, and the notes' issue-month trace at full precision.
``tests/test_universal_life_us_sec.py`` splices: an S point restated in force at month
``d``, opened with S's own state there, continues the S projection from ``d`` on, cell by
cell, and so does the twin of S's in-force point 3 from S's own first month. A point
issued ``k`` months late is the S projection ``k`` months on, and the committed table is
what S generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/universal_life/UL_US_SEC")
    >>> model.Projection[5].result_cf()     # model point 6, the table's sixth row
    >>> model.Projection[5].result_av()
"""

from modelx.serialize.jsonvalues import *

_name = "UL_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

