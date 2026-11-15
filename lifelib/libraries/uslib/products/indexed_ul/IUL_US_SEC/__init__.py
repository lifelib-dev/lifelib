# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. indexed universal life.

:mod:`~.IUL_US_SEC` projects the policy :mod:`~.IUL_US_S` projects -- a single-life,
flexible-premium indexed universal life policy: the universal life chassis --
monthiversary processing, a monthly deduction of per-policy, per-unit and
cost-of-insurance charges, Guideline Premium Test death benefit options A and B, a
ten-year surrender charge run-off -- with the current-assumption crediting engine replaced
by one AG 49-A Benchmark Index Account: a fixed (holding) account credited at 4.50% [S2]
and a ladder of monthly 1-year S&P 500 point-to-point segments credited at
``max(0%, min(10%, 100% x r))`` [S2][S3][R1] -- from a **valuation date** rather than
from the start of a projection of its own. A model point may be a policy already in force
at that date, in any month of its policy year and with up to twelve index segments live,
one issued at it, or one to be issued in the ten years after it, as in lifelib's
``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S`` the same way. Its
formulas are the executable counterpart of ``products/indexed_ul/technical-notes.md``, and
``products/indexed_ul/model-sec.md`` explains what running in force changes.

The indexed crediting engine is the only thing that differs from the chassis. The
technical notes say so explicitly and defer the shared mechanics to
``products/universal_life/technical-notes.md``; :mod:`~.IUL_US_S` therefore uses the same
cells names as :mod:`~.UL_US_S` for every shared concept, and adds names only for the
fixed account, the segment ladder and the crediting formula. This model follows
``UL_US_SEC``, the chassis's in-force model, wherever running in force needs the same
thing.

**Spaces.** The model contains two:

:mod:`~.IUL_US_SEC.Data`
    Reads the six assumption CSVs it shares with :mod:`~.IUL_US_S`, its own model point
    table and its own segment ladder, and holds their filename References. It checks the
    model point table and the ladder as it reads them, and the keys and the values of
    every table the projection reads at an attained age or a policy year, the class
    factors and the surrender charge schedules. It takes no parameters, so each file is
    read **once per model**.

:mod:`~.IUL_US_SEC.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.IUL_US_SEC.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps on policy monthiversaries, on two clocks. ``t``
counts months from the valuation date, 0-based, as ``basiclife/BasicTerm_SE`` counts
them: ``t = 0`` is the valuation month for every model point, however old the policy, and
the frame runs ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len() = maturity_mth() - duration_mth_init()`` counts the months from the
valuation date to the end of the projection. That ends as the insured attains 121
(``maturity_age``), the notes' [unverified] maturity inference (spec F5):
``maturity_mth()`` is the first policy month at that age. ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t`` from the model point's
``duration_mth`` at ``t = 0``, and the contract runs on it: the anniversary premium, the
segment maturities, the surrender charge, the no-lapse period, the tax tests and the
tables, with ``policy_year(t) = duration(t) + 1`` the 1-based contractual label,
``duration(t) = duration_mth(t) // 12``, derived and never indexed by. The policy is on
the books from :func:`~.IUL_US_SEC.Projection.t_entry`, the valuation month for a point in
force or issued at it and the issue month for one issued later, and every recursion opens
there. The contract is described as continuing in force at 121 with no further charges,
so the horizon truncates the run rather than terminating the policy: the count and the
account value the survivors of the last month carry into ``t = proj_len()`` are kept, and
the roll-forwards close on them; ``pols_maturity(t)`` is identically zero. The index path
and expense inflation run on ``t``: the index grows at its level return from
``index_level_init`` at the valuation date, one path for every point, and inflation,
which ships at 0, steps on the valuation date's anniversaries. Acquisition is charged per
policy issued, from the issue month, and is not inflated, as in
``basiclife/BasicTerm_SE``. On a point issued at ``t = 0`` the two clocks coincide, and
the model computes what :mod:`~.IUL_US_S` computes.

A point in force opens with its state at the valuation date, per policy, as it stands at
the start of month 0, which :mod:`~.IUL_US_S`, opening an in-force point with
everything outside the loan in its fixed account, cannot restate: the account value and
the loan, ``IUL_US_S``'s own columns, ``av_pp_init`` and ``loan_bal_init``; the fixed
account and the loan collateral apart from the loan, ``fa_pp_init`` and ``lca_pp_init``;
the face in force, ``sum_assured_init``; the premiums less withdrawals paid to date,
``cum_prem_init``, the base of the guideline premium and 7-pay tests, and the same less
loans, ``cum_prem_net_init``, the no-lapse guarantee's accumulator, each of which
``IUL_US_S`` opens at 0; the MEC latch, ``is_mec_init``; and its live index segments,
up to twelve, each with its balance, the deductions and draws charged to it since its
creation, the index level at its creation and the cap declared then, one row a segment of
a companion table, ``inforce_segments_sec.csv``, keyed by ``point_id`` and ``slot``. A
point not yet in force carries none of it.

Within each month the notes' monthiversary order is followed exactly. At the beginning
of the month (BOM): the anniversary premium and its load; the maturity of any segment
created twelve months earlier, whose index credit is added and whose value rolls into
the fixed account; withdrawals and new loan collateral, sourced fixed-account-first
then pro rata across live segments; the death benefit and corridor test; the net amount
at risk; the monthly deduction, sourced the same way; and the sweep of the remaining
fixed-account balance into a new segment. At the end of the month (EOM): one month's
interest on the fixed account and on the loan collateral account -- **segments earn no
interim interest**, which is what the 0% floor design buys [S2] -- loan interest
accrual, then the decrements, death before lapse.

Cash flows are **undiscounted**. Premiums, expenses and premium taxes fall at BOM and
are weighted by ``pols_if(t)``, the count in force at the **start** of month ``t``;
death claims by ``pols_if(t) * mort_rate_mth(t)``; surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``; and partial withdrawals by
``pols_if(t)`` again, because a withdrawal is taken at BOM on the owner's election and
is not a decrement. ``result_cf()`` publishes the withdrawal payment in a
``withdrawals`` column of its own rather than as a claim leg, and the surrender leg as
``claims_lapse``, matching the ``"LAPSE"`` kind that produces it; the cash flow columns
are income-positive and sum to ``net_cf``.

Two orderings are load-bearing and are pinned by ``check_av_roll_fwd()``. Interest is
credited on the *post-deduction* fixed-account balance, as on the chassis. And a
segment matures at step 2 of policy month ``m + 12``, *before* that month's deduction, so
it carries eleven in-segment deductions rather than twelve -- see
``products/indexed_ul/model.md``, which is where the worked example's stipulated twelve is
reconciled.

**What is sourced and what is not.** The contractual elements come from the composite
product spec: the 10.00% current cap and 2.00% guaranteed cap, 100% participation and
0% floor of the Benchmark Index Account [S2][R1]; the 4.50% current and 1.00%
guaranteed fixed-account rates [S2]; the 1-year S&P 500 point-to-point method and the
12-month, up-to-12-concurrent segment ladder [S2][S3][S4]; the $10 monthly policy fee
[S3][S5]; the $25 withdrawal fee and the fixed-account-first sourcing rule for loans [S3]
(the $500 withdrawal minimum and the $500 cash surrender value floor of the same source
are sourced but **not** enforced -- see "Not implemented"); the 61-day grace period [S3]
and the cumulative-MNLP no-lapse test [S3] [S4] with its $20.80 per $1,000 band-1 rate
[S3]; the 10-year surrender charge period [S1][S5][S7]; the IRC 7702(d) corridor factors
[R4]; the standard-loan design [S3][S5][S7]. Everything else is a standardization
introduced for the reference implementation: applying the fixed-account-first rule to
withdrawals and the monthly deduction, which the source takes pro rata across accounts
[S3]; reading the source's band-1 base annual minimum premium rate as the MNLP rate; the
5% current and 8% guaranteed premium loads, the $0.30 per $1,000 per-unit charge, the 65%
current-to-guaranteed COI factor and the whole COI scale (2017 CSO is licensed and may
not be reproduced [REG-R17]), the $25 per $1,000 surrender charge scale, the
best-estimate mortality table, the rate-class factors, the 6%/4% base lapse vector with
its year-11 surrender-charge-expiry spike, the dynamic-lapse formula, the 98% premium
persistency, the 3.00%/2.00%/3.00% loan rates, the guideline and 7-pay placeholders,
the $75 per policy per year maintenance expense and $150 acquisition expense, the 2.0%
premium tax, and -- the assumption that matters most -- the 6.40% level index return of
the base deterministic run. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

The notes are emphatic that the 6.40% figure is a *carrier-published 1988-2023 lookback*
[S2], not AG 49-A's 25-year averaging window, and that AG 49-A bounds what may be
**illustrated**, not what will be **credited** [R1][R6]: because the cap truncates the
right tail while the floor only offsets the left, a deterministic run at the illustrated
rate overstates credits against a stochastic mean at matched expected index growth. Treat
``index_return_ann`` as a disclosure-anchored placeholder, not a best estimate.

**Not implemented.** Modules the technical notes describe but do not specify completely
enough to project, all named here and in ``products/indexed_ul/model.md`` so their
absence is not mistaken for an oversight:

* Stochastic index scenarios. The notes give the lognormal parameters (mu = 6.0%,
  sigma = 16% **[std]** placeholders) but a path-by-path simulation is a driver around
  this model, not a cell inside it; the base run is the deterministic one the notes
  prescribe. :func:`~.IUL_US_SEC.Projection.index_level` is the single point of
  substitution.
* Cap re-declaration from an option budget. The notes give the economics
  (``HB ~ [C(I_0) - C(I_0(1+c))] / I_0``, ``HB ~ NIER - target spread``) but no option
  pricing model, no NIER path and no target spread, so the cap is held level as the
  notes prescribe for the base run. A segment carries the cap declared at its creation,
  so a re-declared cap would reach new segments only.
* The grace and lapse-for-insufficiency cascade. The trigger and the no-lapse test are
  complete and are implemented as the diagnostics
  :func:`~.IUL_US_SEC.Projection.is_shortfall`,
  :func:`~.IUL_US_SEC.Projection.nlg_test_ok` and
  :func:`~.IUL_US_SEC.Projection.nlg_in_effect`, and the notes' lapse suppression while
  the no-lapse guarantee is in effect *is* implemented in
  :func:`~.IUL_US_SEC.Projection.lapse_rate`; but the notes leave the in-grace account
  value treatment and the cash flow of a cure payment undetermined, so no policy is
  terminated for insufficiency and no in-grace state is carried.

  **This has a consequence worth stating plainly.** A policy whose account value is
  exhausted goes on being charged. The monthly deduction is taken in full, the fixed
  account carries whatever the segments cannot, and the account value turns negative;
  and because ``NAAR_t = max(0, DB_t x v_g - AV'_t)`` rises one for one as ``AV'_t``
  falls, the cost of insurance then compounds on itself and the account value runs
  away. ``IUL_US_S``'s point 5, twin 5 here, is the only shipped point that gets there:
  its fixed account first closes a month below zero at policy month 383 and its account
  value at policy month **604**, so ``result_av()`` -- ``av_pp``, ``net_amt_at_risk``,
  ``coi_pp``, ``mth_deduction_pp`` -- **is not a meaningful number for that policy from
  month 604 onward**. The cash flow columns of ``result_cf()`` stay finite and bounded:
  the death benefit is the Option A face amount and both the death claim
  ``max(0, DB - L)`` and the surrender payment floor at zero. It is the account value
  roll-forward that is meaningless, not the cash flows. Because ``IUL_US_S`` carries such
  a state by design, this model accepts it in force: a point may be restated past either
  month, its fixed account and account value below zero, as points 9 and 10 are.

* The two $500 withdrawal limits. The product spec carries both -- "minimum withdrawal
  $500; CSV may not fall below $500" [S3] -- and neither is enforced here. The
  withdrawal is whatever the model point's ``wd_pp`` column says, and model point 5
  deliberately takes $200 a month, below the sourced minimum, because a compliant $500 a
  month against a $6,000 annual premium empties the policy before the loan module it is
  there to exercise ever starts; :func:`~.IUL_US_SEC.Projection.ncsv_pp` floors at zero
  rather than at $500. Both are limits on what a policyholder may *request*, and the
  notes give no behaviour for a refused request, so the mechanics are implemented and
  the limits are left to the data. A withdrawal above 0 and below its own $25 fee, which
  would debit the account less than the fee charged, is refused by
  :func:`~.IUL_US_SEC.Projection.proj_len`.
* The funding-stop state (1%/yr **[std]**) of the premium persistency section. It is a
  *second* account value path, and the notes do not say how to blend it with the first;
  the 98% compounding persistency factor is implemented, the second state is not.
* The guaranteed floor accumulation test (one carrier's 2% cumulative average [S7],
  another's in-segment 0.75% [S3]). Explicitly a variation, not the baseline: the 0%
  annual floor needs no shadow account.
* Charge-funded high-cap accounts, multi-index and multi-year segments, participating
  (indexed) loans, the Overloan Protection Rider, face increases and decreases, option
  changes, reinstatement, and riders -- all excluded from the baseline by the product
  spec.
* MEC status has no cash flow consequence for the insurer, so
  :func:`~.IUL_US_SEC.Projection.is_mec` flags and does not project. It latches, as
  ``UL_US_S``'s does, where ``IUL_US_S``'s does not.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.IUL_US_S` and
its model point table, and so is ``inforce_segments_sec.csv``, and the tests regenerate
both and compare, so no row is typed by hand. Every point is on the notes' own anchor
configuration M45 / Non-Tobacco / $250,000 / Option A or B / GPT, because the shipped COI
scale covers that cell alone. Points 1 to 5 are the twins of :mod:`~.IUL_US_S`'s five
points, each issued at the valuation date: point 1, the baseline at a $10,000 planned
annual premium; point 2 on death benefit Option B; point 3 with no indexed allocation,
the control run against which the ladder is read; point 4 paying monthly, the only one
that builds the full twelve-segment ladder; and point 5, underfunded, with a $200 monthly
withdrawal from policy year 2 and a $6,000 annual loan from policy year 21. Points 6 to 11
are S points restated in force at an S month, each opened with the state
:mod:`~.IUL_US_S` carries into that month and its live segments: point 1 on its fifth
anniversary, at policy month 60; point 4 mid-year at 65, all twelve segments live; point
5 at 6, mid-way through its first year, its ladder six months deep; point 5 at 384, its
fixed account below zero and its loan above its cash value; point 5 at 605, its account
value below zero too; and point 1 at 888, two years before the end of its projection.
Point 12 is point 4 to be issued 25 months after the valuation date. A model point on any
other issue age, sex or class requires ``coi_rates.csv`` to be extended first; a test
asserts every model point in the table actually projects.

**Verification.** On points 1 to 5, the twins issued at the valuation date, every cell
this model shares with :mod:`~.IUL_US_S` agrees with it at every argument the S model
evaluates in its sweep, ``pols_if_init``, ``model_point``, ``result_pols`` and
``check_margin`` excepted. So the goldens ``tests/test_indexed_ul_us.py`` asserts on the
five points hold here too, with no number restated -- every account value, segment and
cash flow -- and the worked example's credits come from the same engine cells, unchanged.
``tests/test_indexed_ul_us_sec.py`` splices: an S point restated in force at month ``d``,
opened with S's own state and segments there, continues the S projection from ``d`` on,
cell by cell. A point issued ``k`` months late is the S projection ``k`` months on, and the
committed files are what S generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/indexed_ul/IUL_US_SEC")
    >>> model.Projection[1].result_cf()
    >>> model.Projection[7].result_seg()
"""

from modelx.serialize.jsonvalues import *

_name = "IUL_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
