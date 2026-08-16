# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. indexed universal life.

:mod:`~.IUL_US_S` is the executable counterpart of
``products/indexed_ul/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-life, flexible-premium indexed
universal life policy: the universal life chassis -- monthiversary processing, a
monthly deduction of per-policy, per-unit and cost-of-insurance charges, Guideline
Premium Test death benefit options A and B, a ten-year surrender charge run-off --
with the current-assumption crediting engine replaced by one AG 49-A Benchmark Index
Account: a fixed (holding) account credited at 4.50% [S2] and a ladder of monthly
1-year S&P 500 point-to-point segments credited at ``max(0%, min(10%, 100% x r))``
[S2][S3][R1].

The indexed crediting engine is the only thing that differs from the chassis. The
technical notes say so explicitly and defer the shared mechanics to
``products/universal_life/technical-notes.md``; this model therefore uses the same
cells names as :mod:`~.UL_US_S` for every shared concept, and adds names only
for the fixed account, the segment ladder and the crediting formula.

**Spaces.** The model contains two:

:mod:`~.IUL_US_S.Data`
    Reads the seven input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.IUL_US_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.IUL_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps. Policy month ``t`` runs 1, 2, ..., ``proj_len()``,
where ``t = 1`` is the **issue month** of a new-business model point and
``proj_len() = 12 * (maturity_age - age_at_entry()) - duration_mth_init()``, so the
projection ends as the insured attains 121, the notes' [unverified] maturity inference
(spec F5). For an in-force model point ``duration_mth_init()`` is the number of
completed policy months already elapsed at ``t = 1``. State variables the notes define
at their own ``t = 0`` -- ``FA(0) = 0``, ``S(0) = 0``, ``L(0) = 0``, ``l(0) = 1`` --
are the ``t == 0`` branch of the corresponding recursion.

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
segment matures at step 2 of month ``m + 12``, *before* that month's deduction, so it
carries eleven in-segment deductions rather than twelve -- see the README, which is
where the worked example's stipulated twelve is reconciled.

**What is sourced and what is not.** The contractual elements come from the composite
product spec: the 10.00% current cap and 2.00% guaranteed cap, 100% participation and
0% floor of the Benchmark Index Account [S2][R1]; the 4.50% current and 1.00%
guaranteed fixed-account rates [S2]; the 1-year S&P 500 point-to-point method and the
12-month, up-to-12-concurrent segment ladder [S2][S3][S4]; the $10 monthly policy fee
[S3][S5]; the $25 withdrawal fee and the fixed-account-first sourcing rule [S3] (the
$500 withdrawal minimum and the $500 cash surrender value floor of the same source are
sourced but **not** enforced -- see "Not implemented"); the 61-day grace period and the cumulative-MNLP no-lapse test with its
$20.80 per $1,000 band-1 rate [S3][S4]; the 10-year surrender charge period [S1][S5][S7];
the IRC 7702(d) corridor factors [R4]; the standard-loan design [S3][S5][S7]. Everything
else is a standardization introduced for the reference implementation: the 5% current
and 8% guaranteed premium loads, the $0.30 per $1,000 per-unit charge, the 65%
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

The notes are emphatic that the 6.40% figure is a *carrier-published 25-year lookback*
[S2] and that AG 49-A bounds what may be **illustrated**, not what will be **credited**
[R1][R6]: because the cap truncates the right tail while the floor only offsets the
left, a deterministic run at the illustrated rate overstates credits against a
stochastic mean at matched expected index growth. Treat ``index_return_ann`` as a
disclosure-anchored placeholder, not a best estimate.

**Not implemented.** Modules the technical notes describe but do not specify completely
enough to project, all named here and in the README so their absence is not mistaken
for an oversight:

* Stochastic index scenarios. The notes give the lognormal parameters (mu = 6.0%,
  sigma = 16% **[std]** placeholders) but a path-by-path simulation is a driver around
  this model, not a cells inside it; the base run is the deterministic one the notes
  prescribe. :func:`~.IUL_US_S.Projection.index_level` is the single point of
  substitution.
* Cap re-declaration from an option budget. The notes give the economics
  (``HB ~ [C(I_0) - C(I_0(1+c))] / I_0``, ``HB ~ NIER - target spread``) but no option
  pricing model, no NIER path and no target spread, so the cap is held level as the
  notes prescribe for the base run.
* The grace and lapse-for-insufficiency cascade. The trigger and the no-lapse test are
  complete and are implemented as the diagnostics
  :func:`~.IUL_US_S.Projection.is_shortfall`,
  :func:`~.IUL_US_S.Projection.nlg_test_ok` and
  :func:`~.IUL_US_S.Projection.nlg_in_effect`, and the notes' lapse suppression while
  the no-lapse guarantee is in effect *is* implemented in
  :func:`~.IUL_US_S.Projection.lapse_rate`; but the notes leave the in-grace account
  value treatment and the cash flow of a cure payment undetermined, so no policy is
  terminated for insufficiency and no in-grace state is carried.

  **This has a consequence worth stating plainly.** A policy whose account value is
  exhausted goes on being charged. The monthly deduction is taken in full, the fixed
  account carries whatever the segments cannot, and the account value turns negative;
  and because ``NAAR_t = max(0, DB_t x v_g - AV'_t)`` rises one for one as ``AV'_t``
  falls, the cost of insurance then compounds on itself and the account value runs
  away. Model point 5 is the only shipped point that gets there:
  :func:`~.IUL_US_S.Projection.av_pp` first turns negative at policy month **605**
  (policy year 51) and reaches roughly -1.3e10 at the horizon, so ``result_av()`` --
  ``av_pp``, ``net_amt_at_risk``, ``coi_pp``, ``mth_deduction_pp`` -- **is not a
  meaningful number for model point 5 from month 605 onward**. The cash flow columns of
  ``result_cf()`` stay finite and bounded: the death benefit is the Option A face amount
  -- reduced dollar for dollar by the withdrawals to $70,000 by the horizon, and never
  lifted by the corridor, which is multiplying a *negative* account value -- and both
  the death claim ``max(0, DB - L)`` and the surrender payment floor at zero. It is the
  account value roll-forward that is meaningless, not the cash flows.
  ``test_point_5_account_value_runs_away_after_month_605`` pins the boundary so it
  cannot move unnoticed.

* The two $500 withdrawal limits. The product spec carries both -- "minimum withdrawal
  $500; CSV may not fall below $500" [S3] -- and neither is enforced here. The
  withdrawal is whatever the model point's ``wd_pp`` column says, and model point 5
  deliberately takes $200 a month, below the sourced minimum, because a compliant $500 a
  month against a $6,000 annual premium empties the policy before the loan module it is
  there to exercise ever starts; :func:`~.IUL_US_S.Projection.ncsv_pp` floors at zero
  rather than at $500. Both are limits on what a policyholder may *request*, and the
  notes give no behaviour for a refused request, so the mechanics are implemented and
  the limits are left to the data.
* The funding-stop state (1%/yr **[std]**) of the premium persistency section. It is a
  *second* account value path, and the notes do not say how to blend it with the first;
  the 98% compounding persistency factor is implemented, the second state is not.
* The guaranteed floor accumulation test (Securian's 2% cumulative average, Transamerica's
  in-segment 0.75%). Explicitly a variation, not the baseline: the 0% annual floor needs
  no shadow account.
* Charge-funded high-cap accounts, multi-index and multi-year segments, participating
  (indexed) loans, the Overloan Protection Rider, face increases and decreases, option
  changes, reinstatement, and riders -- all excluded from the baseline by the product
  spec.
* MEC status has no cash flow consequence for the insurer, so
  :func:`~.IUL_US_S.Projection.is_mec` flags and does not project.

**Model points.** ``model_point_table.csv`` carries five points, all on the notes' own
anchor configuration M45 / Non-Tobacco / $250,000 / Option A / GPT, because the shipped
COI scale covers that cell alone. Point 1 is the baseline, at the $10,000 planned annual
premium. Point 2 switches to death benefit Option B, which makes the corridor and the
growing net amount at risk live. Point 3 sets the indexed allocation to 0%, so the
whole balance stays in the fixed account and no segment is ever created -- the control
run against which the segment ladder is read. Point 4 pays **monthly** rather than
annually, and is the only point that builds the notes' full twelve-concurrent-segment
ladder: under the annual baseline nothing reaches the fixed account in months 2-12, so
nothing is swept, the ladder degenerates to one segment a year, and the notes' first
pitfall would otherwise go untested. Point 5 is underfunded at $6,000 a year and takes a
$200 monthly withdrawal from policy year 2 and a $6,000 annual standard loan from policy
year 21, which exercises the fixed-account-first-then-pro-rata sourcing, the loan
collateral account, the no-lapse test and the overloan exposure -- and which, because no
policy is terminated for insufficiency here, runs its *account value* away negative in
late duration; the "Not implemented" note on the grace cascade above says from exactly
when, and the README says it again. A model point on any other issue age, sex or class
requires ``coi_rates.csv`` to be extended first; a test asserts every model point in the
table actually projects.

**Verification.** ``tests/test_indexed_ul_us.py`` asserts every row and column of the
notes' worked example -- both index scenarios, and both of the variant credit bases the
notes price alongside them (the Transamerica half-weighted base at 1,191.00 and the
guaranteed-cap-only credit at 236.40) -- to the cent, together with the in-force and
account-value roll-forwards, the segment ladder invariants, and one test per entry in
the notes' "Known modeling pitfalls" list that can be asserted. The ladder invariants
include the 0% floor stated as a **bound**: on every model point, no segment balance and
no index credit may be negative. The two disclosed gaps above -- model point 5's account
value past month 605, and the unenforced $500 withdrawal limits -- are pinned open by
tests of their own, so neither can be closed or widened silently.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/indexed_ul/IUL_US_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "IUL_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

