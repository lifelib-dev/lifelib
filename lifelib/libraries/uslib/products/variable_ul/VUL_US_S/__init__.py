# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. variable universal life.

:mod:`~.VUL_US_S` is the executable counterpart of
``products/variable_ul/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-life, flexible-premium variable
universal life policy: account value allocated between two separate-account
subaccounts and a general-account fixed option, a front-end premium load, a monthly
deduction of cost-of-insurance, per-policy and per-$1,000 charges, an asset-based
mortality-and-expense (M&E) risk charge collected inside the unit values, Guideline
Premium Test death benefit options A and B, a fourteen-year surrender charge, spread
policy loans through a general-account loan account, and no maturity date -- premiums
and monthly deductions cease at attained age 121 while the asset charges continue.

The product is built on the universal-life chassis of
``products/universal_life/technical-notes.md``, and :mod:`~.VUL_US_S` follows
:mod:`.UL_US_S` name for name wherever the two products share a concept. Where
the two models differ, the difference is the variable-UL notes' own instruction rather
than an implementation choice. Every one of those differences is listed below, and the
model README tabulates the same set against the chassis:

* **No one-month discount in the net amount at risk.** The VUL prospectuses define the
  NAAR as death benefit less account value with no discount [S2], so
  ``net_amt_at_risk(t) = max(0, db_pp(t) - av_pp_at(t, "BEF_FEE"))``. The fixed-UL
  chassis divides the death benefit by ``1 + i_gm`` first; this model does not, and
  carries no ``naar_factor``. For the same reason there is no ``wd_free_pp``: the
  fixed-UL specimen carves out a free withdrawal amount and cuts the face by the
  excess, where the variable-UL notes cut the face proportionately with no free amount.
* **The investment return is a separate-account unit-value factor, not a declared
  credited rate.** Each subaccount grows by ``(1 + r) (1 - e_i/12) (1 - m/12)`` on
  exogenous gross returns ``r``; only the fixed option earns a declared rate.
* **The account value is a vector.** Subaccounts, the fixed option and the loan
  account are tracked separately because their growth rules differ, and the monthly
  deduction is allocated across the *unloaned* accounts pro rata.
* **Charges are quoted on the initial face amount.** The per-$1,000 monthly charge and
  the surrender charge both scale with ``F_0``, so :func:`~.VUL_US_S.Projection.units`
  takes no ``t``.
* **The surrender charge steps by policy year, not by month.**
  ``sc_init x (runoff + 1 - y) / runoff`` is level within a policy year, where the
  chassis amortizes its charge every month; the worked example pins the step at
  ``18.00 x 12/14`` through the whole of policy year 3.
* **The maintenance expense does not inflate.** The variable-UL notes give a flat $75
  per policy per year, so ``inflation_rate = 0.0`` where the chassis inflates at 2.5%.
* **The surrender-charge lapse shock is a one-month spike, not a shock year**, its
  magnitude an input (``lapse_shock_mult``, shipped at 1.0, off), and there is no 35%
  cap on the total lapse rate -- the notes set none, and the dynamic multiplier is
  already bounded at 2.0.
* **Guideline premium and 7-pay/MEC compliance are not tracked.** The chassis carries
  them as flags; the variable-UL notes state they are not enforced in the baseline and
  that premiums are assumed within limits, so there is no ``gpt_ok`` or ``is_mec``.

**Spaces.** The model contains two:

:mod:`~.VUL_US_S.Data`
    Reads the ten input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.VUL_US_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.VUL_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps on policy monthiversaries. Policy month ``t`` runs
1, 2, ..., ``proj_len()``, where ``t = 1`` is the **issue month** of a new-business
model point and ``proj_len() = 12 * (omega_age - age_at_entry() + 1) -
duration_mth_init()``, so the projection ends with the policy year in which the insured
attains ``omega_age`` (121), the last age of the mortality table, where the annual rate
is 1.0. For an in-force model point ``duration_mth_init()`` is the number of completed
policy months already elapsed at ``t = 1``. The contract has no maturity date
[S1][S2][S4]; ``pols_maturity(t)`` is therefore identically zero and the projection is
truncated by mortality, not by the contract. The notes' state variables at ``t = 0`` --
``SA_i(0)``, ``FA(0)``, ``LA(0)``, ``D(0)``, ``F(0)``, ``l(0) = 1`` -- are the ``t == 0``
branch of the corresponding recursion.

Within each month the notes' monthiversary order is followed exactly. At the beginning
of the month (BOM): advance the policy year and its age-dependent parameters; premium
and its load, with the net premium allocated by ``alloc(i)`` and ``alloc_fixed()``;
withdrawal and the $25 withdrawal fee, and under Option A the proportionate face
reduction they force; the death benefit and the GPT corridor test on the post-premium
account value; the net amount at risk; the monthly deduction, allocated across the
unloaned accounts pro rata. Over the month: separate-account growth through the
unit-value factor, fixed-option interest, loan-account interest and debt accrual. At
the end of the month (EOM): the death benefit and net amount at risk are recomputed on
end-of-month balances, then the decrements -- **death before lapse**.

Premiums, expenses, percent-of-premium expenses and withdrawal payments therefore fall
at BOM and are weighted by ``pols_if(t)``; death claims by
``pols_if(t) * mort_rate_mth(t)`` and surrender payments by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)``.
Cash flows are **undiscounted**: this library projects gross liability cash flows and
leaves reserving and discounting to a separate layer.

A partial withdrawal is a payment on the owner's election, not a claim, so it is
:func:`~.VUL_US_S.Projection.withdrawals` in its own ``withdrawals`` column of
``result_cf()``; :func:`~.VUL_US_S.Projection.claims` covers deaths and surrenders
only, and its surrender column is ``claims_lapse``, named for the ``"LAPSE"`` kind that
produces it.

The claim cash flow is the **full death benefit less policy debt**, not the net amount
at risk. The notes carry an explicit warning about this ("a common specification
error"): projecting ``DB - AV`` as the claim understates gross benefit outgo, and
projecting the full death benefit *and* separately expensing the net amount at risk
double counts. The model projects the gross view in :func:`~.VUL_US_S.Projection.claims`
and derives the general-account view arithmetically from the same run in
:func:`~.VUL_US_S.Projection.result_net`; ``check_net_view()`` pins the two together.

**What is sourced and what is not.** The contractual elements come from the four
registered prospectuses behind the composite: the 6% guaranteed premium load ceiling
[S2], the $10.00 per-policy monthly charge [S2][S4], the $0.20 per $1,000 of initial
face monthly charge [S2], the 0.45% current M&E rate [S1], the 1.0% fixed-option floor
[S1], the 2.0%/1.0% and 1.05%/1.0% loan charged/credited rates [S1], the GPT corridor
factors at the quoted quinquennial ages [S2][R3], the net amount at risk defined
without a discount [S2], the $83.34 monthly COI cap [S1][S2][S3][S4], the disclosed
current/guaranteed COI anchor for male 45 standard non-tobacco year 1 ($0.04 / $0.22)
[S4], the default test and 61-day grace [S1][R8], and the cessation of premiums and
deductions at attained age 121 [S1][S2][S4].

Everything else is a standardization: the 4.0% current premium load, the two-subaccount
lineup and its 0.75% / 0.55% fund expense ratios, the $18.00 per $1,000 surrender charge
running off linearly over fourteen years, the linear interpolation of the corridor
factors between the quoted ages and their grading to 100% at attained age 95 rather
than at 90 (the product spec's footnote 11 resolves the notes' "100% at 90-95" that
way), the illustrative guaranteed COI scale standing in for
the licensed 2017 CSO table, the 50%-of-guaranteed current COI placeholder, the
illustrative best-estimate mortality table standing in for the licensed 2015 VBT, the
rate-class factors, the base lapse vector, the surrender-charge-cliff spike, the
dynamic lapse and premium persistency forms, the level 6% gross return scenario, and
the $75 per policy per year maintenance expense with the 2% percent-of-premium expense.
The separate-account return scenario is the dominant assumption for this product and it
is **[std]** in full. **This model is a mechanics demonstration, not a pricing or
reserving result.** Replace the assumption tables with company data before drawing any
conclusion from the output.

**Not implemented.** Modules the technical notes describe but do not specify completely
enough to project, all named here and in the README so their absence is not mistaken
for an oversight:

* The grace and default cascade. The trigger is a complete formula and is implemented
  as :func:`~.VUL_US_S.Projection.is_default`, but the notes lapse the policy "at the
  next monthiversary **if not cured**" without defining the cure test, the in-grace
  deduction accrual or the death benefit during grace, so no policy is terminated for
  insufficiency and no in-grace state is carried. Read literally the notes' test fires
  from issue on any front-loaded design, because the scheduled surrender charge exceeds
  a first premium; :func:`~.VUL_US_S.Projection.is_shortfall` and
  :func:`~.VUL_US_S.Projection.first_shortfall_month` are the companion diagnostics
  that mark where the account genuinely stops being able to carry the contract, and
  months after that are arithmetic, not a description of a live contract.
* No-lapse guarantee and overloan protection riders -- documented variations, excluded
  from the baseline by the notes themselves.
* New policy loans, repayments and the loan value limit. Loan *interest accrual* on an
  opening balance is implemented (the notes give the formula); no utilization pattern
  is given, so :func:`~.VUL_US_S.Projection.loan_bal_pp` only rolls the model point's
  opening debt forward and :func:`~.VUL_US_S.Projection.la_pp` only rolls its
  collateral forward.
* Guideline premium and 7-pay/MEC testing. The notes state these are not enforced in
  the baseline and that premiums are assumed within limits.
* Face increases and decreases, death benefit option changes and CVAT qualification.
  Withdrawal-driven proportionate face reduction under Option A *is* implemented.
* Stochastic return sets. The scenario interface is a table of monthly gross returns
  per subaccount, so a stochastic set is a data change, not a formula change; the
  shipped scenarios are deterministic.
* Riders generally. :func:`~.VUL_US_S.Projection.rider_charge_pp` is the notes'
  placeholder term, zero in the base model.

The **dynamic behavior module** -- the funding ratio, dynamic lapse and premium
persistency -- *is* implemented in full, including the notes' at-issue pricing path
``AV*``, but is switched **off** by the Reference ``dyn_behavior_on = False`` so that
the base deterministic run pays the planned premium in full and reproduces the worked
example, exactly as ``Term_US_A`` switches conversion off for the same reason.

**Model points.** ``model_point_table.csv`` carries four points, all on the anchor
configuration M45 / StdNT / $500,000, because the notes disclose a COI anchor for that
cell alone. Point 1 is the technical notes' worked-example anchor: Option A, $6,000
planned annual premium, twenty-four completed policy months, opening subaccount balances
of $30,000 and $20,000 split 60/40, no fixed balance and no debt, on the worked
example's own return scenario. Point 2 is identical except that it leaves the two
override columns blank and so takes the formula path -- see **Verification**. Point 3 is
new business under Option B, which makes the corridor and the constant net amount at
risk live and exercises the surrender charge from policy year 1. Point 4 is an in-force
cell at 120 completed policy months with a fixed-option balance and an $8,000 loan,
which exercises the fixed option, the loan account, the debt accrual, the loan spread
and the pro-rata deduction that excludes the loan account. A model point on any other
issue age, sex or class requires ``coi_rates.csv`` to be extended first; a test asserts
every model point in the table actually projects.

**Verification.** Model point 1 is the anchor cell of the worked example in the
technical notes, and ``tests/test_variable_ul_us.py`` asserts every row and column of
it -- the opening balances, the premium and its load, the 60/40 net premium split, the
death benefit and the corridor product that loses to it, the net amount at risk, the
cost of insurance, the two fixed charges, the monthly deduction and its pro-rata split,
both unit-value growth factors, both end-of-month subaccount balances, the M&E collected
in each subaccount, the insurer margin for the month, the surrender charge, the cash
surrender value and the end-of-month death benefit and net amount at risk -- to the cent
and to the six displayed decimals of the growth factors.

The worked example evaluates two age-dependent parameters at the **issue** age 45 while
sitting in **policy year 3**, where the attained age is 47: it quotes the corridor factor
as ``kappa(45) = 215%`` and the current COI rate as the disclosed year-1 anchor $0.04.
The model implements the rule -- both are attained-age lookups, per the notes' own state
variable table -- and pins the worked example's two values on model point 1 through the
``corridor_override_m1`` and ``coi_rate_override_m1`` columns. Both pins are confined to
``t == 1``, the single month the worked example describes: they are lookups the notes
performed at the wrong age, not contract parameters, and carrying an issue-age corridor
factor or one disclosed COI rate across seventy-seven years would misstate every later
month. Model point 2 is the same cell with both blank, so it takes the rule from the
first month, and a test pins the gap open in both directions. This is the pattern
``Term_US_A`` uses for its ``M(1)`` divergence; neither reading is "correct", and
neither may be closed silently.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/variable_ul/VUL_US_S")
    >>> model.Projection[1].result_av()
"""

from modelx.serialize.jsonvalues import *

_name = "VUL_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

