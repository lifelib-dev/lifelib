# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. variable universal life.

:mod:`~.VUL_US_SEC` projects the policy :mod:`~.VUL_US_S` projects -- a single-life,
flexible-premium variable universal life policy: account value allocated between two
separate-account subaccounts and a general-account fixed option, a front-end premium
load, a monthly deduction of cost-of-insurance, per-policy and per-$1,000 charges, an
asset-based mortality-and-expense (M&E) risk charge collected inside the unit values,
Guideline Premium Test death benefit options A and B, a fourteen-year surrender charge,
spread policy loans through a general-account loan account, and no maturity date,
premiums and monthly deductions ceasing at attained age 121 while the asset charges
continue -- from a **valuation date** rather than from the start of a projection of its
own. A model point may be a policy already in force at that date, in any month of its
policy year, one issued at it, or one to be issued in the ten years after it, as in
lifelib's ``basiclife/BasicTerm_SE``, which extends ``basiclife/BasicTerm_S`` the same
way. Its formulas are the executable counterpart of
``products/variable_ul/technical-notes.md``, and ``products/variable_ul/model-sec.md``
explains what running in force changes.

The product is built on the universal-life chassis of
``products/universal_life/technical-notes.md``, and :mod:`~.VUL_US_S` follows
:mod:`.UL_US_S` name for name wherever the two products share a concept, as this model
follows ``UL_US_SEC``, the chassis's in-force model, wherever running in force needs the
same thing. Where the two products differ, the difference is the variable-UL notes' own
instruction rather than an implementation choice, and :mod:`~.VUL_US_S`'s docstring lists
every one of them: no one-month discount in the net amount at risk, a separate-account
unit-value return rather than a declared credited rate, an account value that is a vector
of subaccounts, a fixed option and a loan account, charges quoted on the initial face, a
surrender charge that steps by policy year, a maintenance expense that does not inflate, a
one-month lapse spike at the surrender charge's cliff, and no guideline premium or 7-pay
tracking.

**Spaces.** The model contains two:

:mod:`~.VUL_US_SEC.Data`
    Reads the nine assumption CSVs it shares with :mod:`~.VUL_US_S` and its own model
    point table, and holds their filename References. It checks the model point table as
    it reads it, the keys and the values of every table read at a policy year or an
    attained age, the class factors, the surrender-charge schedules, the subaccount lineup
    and the return scenario. It takes no parameters, so each file is read **once per
    model**. It hands the projection what the files hold as numpy vectors and arrays of
    numbers, one element per model point, per subaccount, per key, per schedule or per
    scenario.

:mod:`~.VUL_US_SEC.Projection`
    The by-policy projection, parameterized by ``idx``, the position of a model point in
    the ``Data`` vectors, as ``basiclife.BasicTerm_SC`` is: ``Projection[0]`` is an
    ItemSpace projecting the table's first row, model point 1, and its ``point_id()`` is
    that label. It reaches the inputs through its ``data`` Reference, which resolves to
    the single :mod:`~.VUL_US_SEC.Data` Space.

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
number from a ``Data`` vector at ``idx``, a subaccount's at its position in the lineup,
and every table, the return scenario among them, as an array indexed by integers; a
timing or a kind is an int code; and every cell but the reports, ``model_point`` and seven
label accessors returns a C ``bint``, ``long long`` or ``double``, cached as a single
value or in a C array sized from the contract. modelx reads and runs the same formulas,
and computes the same numbers. ``products/variable_ul/model-sec.md`` says how to compile
and run it, and what the compiled model does not do as modelx does: it clears no cache
when a Reference is set, so every Reference is set on a model just imported.

**Projection basis.** Monthly steps on policy monthiversaries, on two clocks. ``t``
counts months from the valuation date, 0-based, as ``basiclife/BasicTerm_SE`` counts
them: ``t = 0`` is the valuation month for every model point, however old the policy, and
the frame runs ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len() = omega_mth() - duration_mth_init()`` counts the months from the valuation
date to the end of the projection. That ends with the policy year in which the insured
attains ``omega_age`` (121), the last age of the mortality table, where the annual rate is
1.0: ``omega_mth()`` is the first policy month at attained age 122. ``duration_mth(t)``
counts the months the policy has been in force, ``duration_mth_init() + t`` from the model
point's ``duration_mth`` at ``t = 0``, and the contract runs on it:
``policy_year(t) = duration(t) + 1`` is the 1-based contractual label,
``duration(t) = duration_mth(t) // 12``, derived and never indexed by. The policy is on
the books from :func:`~.VUL_US_SEC.Projection.t_entry`, the valuation month for a point
in force or issued at it and the issue month for one issued later, and every recursion
opens there. The contract has no maturity date [S1][S2][S4];
``pols_maturity(t)`` is therefore identically zero and the projection is truncated by
mortality, not by the contract, so where lives survive the last month the count and the
account value they carry into ``t = proj_len()`` are kept, and the roll-forwards close on
them. The separate-account return scenario, the declared fixed rate and expense
inflation run on ``t``: the scenario is a path of the economy from the valuation date,
and the rate and inflation are flat as shipped. Acquisition is charged per policy issued,
in the issue month, and is not inflated, as in ``basiclife/BasicTerm_SE``. On a point
issued at ``t = 0`` the two clocks coincide, and the model computes what :mod:`~.VUL_US_S`
computes.

A point in force opens with its state at the valuation date, per policy, as it stands at
the start of month 0: each subaccount and the fixed option, ``sa_pp_init_<i>`` and
``fa_pp_init``, ``VUL_US_S``'s own columns, read off the policy's own accounts and never
the premium allocation times the account value; the loan account, ``la_pp_init``, which
holds the loan's collateral and grows apart from the debt once interest accrues; the
debt, ``loan_bal_init``, ``VUL_US_S``'s own; and the face in force, ``sum_assured_init``,
after every Option A withdrawal cut to date, while the face at issue stays the base of the
per-$1,000 charge and the surrender charge. ``VUL_US_S`` takes the loan account equal to
the debt and the face at issue on its in-force points. The two first-month pins apply in
the valuation month, ``t = 0``, the month the worked example describes.

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
:func:`~.VUL_US_SEC.Projection.withdrawals` in its own ``withdrawals`` column of
``result_cf()``; :func:`~.VUL_US_SEC.Projection.claims` covers deaths and surrenders
only, :func:`~.VUL_US_SEC.Projection.claims_death` and
:func:`~.VUL_US_SEC.Projection.claims_lapse`, and its surrender column is
``claims_lapse``, named for the ``LAPSE`` kind that produces it.

The claim cash flow is the **full death benefit less policy debt**, not the net amount
at risk. The notes carry an explicit warning about this ("a common specification
error"): projecting ``DB - AV`` as the claim understates gross benefit outgo, and
projecting the full death benefit *and* separately expensing the net amount at risk
double counts. The model projects the gross view in
:func:`~.VUL_US_SEC.Projection.claims` and derives the general-account view
arithmetically from the same run in :func:`~.VUL_US_SEC.Projection.result_net`;
``check_net_view()`` pins the two together.

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
  as :func:`~.VUL_US_SEC.Projection.is_default`, but the notes lapse the policy "at the
  next monthiversary **if not cured**" without defining the cure test, the in-grace
  deduction accrual or the death benefit during grace, so no policy is terminated for
  insufficiency and no in-grace state is carried. Read literally the notes' test fires
  from issue on any front-loaded design, because the scheduled surrender charge exceeds
  a first premium; :func:`~.VUL_US_SEC.Projection.is_shortfall` and
  :func:`~.VUL_US_SEC.Projection.first_shortfall_month` are the companion diagnostics
  that mark where the account genuinely stops being able to carry the contract, and
  months after that are arithmetic, not a description of a live contract. No policy in
  force holds a negative subaccount, so the model point table refuses one, and a point in
  permanent shortfall is restated no later than the last month its subaccounts are still
  zero or more.
* No-lapse guarantee and overloan protection riders -- documented variations, excluded
  from the baseline by the notes themselves.
* New policy loans, repayments and the loan value limit. Loan *interest accrual* on an
  opening balance is implemented (the notes give the formula); no utilization pattern
  is given, so :func:`~.VUL_US_SEC.Projection.loan_bal_pp` only rolls the model point's
  opening debt forward and :func:`~.VUL_US_SEC.Projection.la_pp` only rolls its
  collateral forward.
* Guideline premium and 7-pay/MEC testing. The notes state these are not enforced in
  the baseline and that premiums are assumed within limits.
* Face increases and decreases, death benefit option changes and CVAT qualification.
  Withdrawal-driven proportionate face reduction under Option A *is* implemented, and a
  point in force carries the face its withdrawals have left.
* Stochastic return sets. The scenario interface is a table of monthly gross returns
  per subaccount, so a stochastic set is a data change, not a formula change; the
  shipped scenarios are deterministic.
* Riders generally. :func:`~.VUL_US_SEC.Projection.rider_charge_pp` is the notes'
  placeholder term, zero in the base model.

The **dynamic behavior module** -- the funding ratio, dynamic lapse and premium
persistency -- *is* implemented in full, including the notes' at-issue pricing path
``AV*``, but is switched **off** by the Reference ``dyn_behavior_on = False`` so that
the base deterministic run pays the planned premium in full and reproduces the worked
example, exactly as ``Term_US_S`` switches conversion off for the same reason. The
pricing path is a projection made at issue, deterministic and keyed by the policy month
from issue, so a point in force reads it from issue and needs no opening value for it.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.VUL_US_S` and
its model point table, and the tests regenerate it and compare, so no row is typed by
hand. Every point is on the anchor configuration M45 / StdNT / $500,000, because the
notes disclose a COI anchor for that cell alone. Points 1 to 4 are the twins of
:mod:`~.VUL_US_S`'s four points: point 1, the technical notes' worked-example anchor,
Option A, $6,000 planned annual premium, in force 24 months at the valuation date with
subaccount balances of $30,000 and $20,000 split 60/40, no fixed balance and no debt, on
the worked example's own return scenario, whose month 0 is the worked example's month;
point 2, the same with the two pins blank, so that it takes the formula path; point 3,
new business under Option B, issued at the valuation date, whose net amount at risk is the
constant face, and which exercises the surrender charge from policy year 1; and point 4,
in force 120 months with a fixed-option balance and an $8,000 loan. The corridor binds on
the Option A points alone, late in their frames: on point 1 from ``t = 375``, at attained
age 78, and on point 8 from ``t = 0``.
Points 5 to 8 are S points restated in force at an S month, each opened with the state
:mod:`~.VUL_US_S` carries into that month: point 3 on its first anniversary, inside the
surrender-charge period; point 4 six months on, at policy month 126, mid-year, its
collateral and its debt parted; point 3 at month 593, the month its shortfall begins;
and point 4 at month 768, the first month at attained age 119, where the mortality rate
reaches 1.0 and every survivor dies. Point 9 is point 3 to be issued 25 months after the
valuation date. A model point on any other issue age, sex or class requires
``coi_rates.csv`` to be extended first; a test asserts every model point in the table
actually projects.

**Verification.** On point 3, the twin issued at the valuation date, every cell this
model shares with :mod:`~.VUL_US_S` agrees with it at every argument the S model evaluates
in its sweep, ``pols_if_init``, ``model_point``, ``result_pols``, ``subaccount_ids`` and
``coi_rate_scale`` excepted, S's ``claims(t, None)`` and ``me_charge_pp(t, None)`` compared
as :func:`~.VUL_US_SEC.Projection.claims` and :func:`~.VUL_US_SEC.Projection.me_charge_pp`
and S's subaccount ids as positions in the lineup; and on
points 1, 2 and 4, :mod:`~.VUL_US_S`'s in-force points, which both models open at the
valuation date, every cell agrees from ``t = 0`` on. So the goldens
``tests/test_variable_ul_us.py`` asserts hold here too, with no number restated: every
row and column of the worked example on point 1 -- the opening balances, the premium and
its load, the 60/40 net premium split, the death benefit and the corridor product that
loses to it, the net amount at risk, the cost of insurance, the two fixed charges, the
monthly deduction and its pro-rata split, both unit-value growth factors, both
end-of-month subaccount balances, the M&E collected in each subaccount, the insurer
margin for the month, the surrender charge, the cash surrender value and the end-of-month
death benefit and net amount at risk -- to the cent, at ``t = 0``, the valuation month.
``tests/test_variable_ul_us_sec.py`` splices: an S point restated in force at month
``d``, opened with S's own state there, continues the S projection from ``d`` on, cell by
cell. A point issued ``k`` months late is the S projection ``k`` months on, and the
committed table is what S generates.

The worked example evaluates two age-dependent parameters at the **issue** age 45 while
sitting in **policy year 3**, where the attained age is 47: it quotes the corridor factor
as ``kappa(45) = 215%`` and the current COI rate as the disclosed year-1 anchor $0.04.
The model implements the rule -- both are attained-age lookups, per the notes' own state
variable table -- and pins the worked example's two values on model point 1 through the
``corridor_override_m1`` and ``coi_rate_override_m1`` columns. Both pins are confined to
``t = 0``, the valuation month and the single month the worked example describes: they
are lookups the notes performed at the wrong age, not contract parameters, and carrying
an issue-age corridor factor or one disclosed COI rate across seventy-seven years would
misstate every later month. Model point 2 is the same cell with both blank, so it takes
the rule from the first month, and a test pins the gap open in both directions. This is
the pattern ``Term_US_S`` uses for its ``M(1)`` divergence; neither reading is "correct",
and neither may be closed silently.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/variable_ul/VUL_US_SEC")
    >>> model.Projection[5].result_cf()     # model point 6, the table's sixth row
    >>> model.Projection[5].result_av()
"""

from modelx.serialize.jsonvalues import *

_name = "VUL_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

