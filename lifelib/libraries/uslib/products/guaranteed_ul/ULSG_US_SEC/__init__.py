# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""In-force reference liability cash flow model for U.S. guaranteed universal life (ULSG).

:mod:`~.ULSG_US_SEC` projects the policy :mod:`~.ULSG_US_S` projects -- a single-life,
flexible-premium universal life policy with a **single shadow-account secondary
guarantee** (AG 38 8E Policy Design #1 [R1]; VM-01 shadow-account definition [R2]): level
death benefit only, a notional guarantee account with its own load, charges and credited
rate, an in-force test ``SG - L > 0`` that keeps the contract alive after the real account
value is exhausted, a built-in return-of-premium endorsement at anniversaries 20 and 25
[S1], a 15-year surrender charge, and no maturity date, charges and premiums ceasing at
attained age 121 while coverage continues [S7] -- from a **valuation date** rather than
from the start of a projection of its own. A model point may be a policy already in force
at that date, in any month of its policy year and in its grace, one issued at it, or one
to be issued in the ten years after it, as in lifelib's ``basiclife/BasicTerm_SE``, which
extends ``basiclife/BasicTerm_S`` the same way. Its formulas are the executable
counterpart of ``products/guaranteed_ul/technical-notes.md``, and
``products/guaranteed_ul/model-sec.md`` explains what running in force changes.

The product is built on the universal life chassis. Its technical notes say so
explicitly, and :mod:`~.ULSG_US_S` follows :mod:`.UL_US_S` in structure, naming and
processing order, as this model follows ``UL_US_SEC``, the chassis's in-force model,
wherever running in force needs the same thing. Where the two products differ, the
guaranteed-UL notes restate a recursion with their own parameters, and two deviations
are documented: the account value for the net amount at risk is measured **after the
expense charges and before the cost of insurance** (the UL chassis measures it before the
entire monthly deduction), and the guaranteed-UL notes' ``CSV_t`` already nets policy
debt, which is the chassis' ``ncsv_pp``.

**Spaces.** The model contains two:

:mod:`~.ULSG_US_SEC.Data`
    Reads the seven assumption CSVs it shares with :mod:`~.ULSG_US_S` and its own model
    point table, and holds their filename References. It checks the model point table as
    it reads it, and the keys and the values of every table the projection reads at an
    attained age, a policy year or an anniversary, the class factors and the surrender
    charge schedules. It takes no parameters, so each file is read **once per model**.

:mod:`~.ULSG_US_SEC.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.ULSG_US_SEC.Data` Space.

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
``proj_len() = charges_cease_mth() - duration_mth_init()`` counts the months from the
valuation date to the end of the projection. That ends at attained age 121, where charges
and premiums cease, the notes' maximum projection length: ``charges_cease_mth()`` is the
first policy month at that age. ``duration_mth(t)`` counts the months the policy has been
in force, ``duration_mth_init() + t`` from the model point's ``duration_mth`` at
``t = 0``, and the contract runs on it: ``policy_year(t) = duration(t) + 1`` is the
1-based contractual label, ``duration(t) = duration_mth(t) // 12``, derived and never
indexed by. The policy is on the books from :func:`~.ULSG_US_SEC.Projection.t_entry`, the
valuation month for a point in force or issued at it and the issue month for one issued
later, and every recursion opens there. Coverage continues past attained age 121 under
the contract [S7], and lives can survive the last month wherever mortality improvement has
taken the rate at attained age 120 below the table's 1.0, so the count, the account value
and the lapse latch they carry into ``t = proj_len()`` are kept, and the roll-forwards
close on them; ``pols_maturity(t)`` is identically zero -- guaranteed UL has no maturity
date. The declared credited rate, expense inflation and mortality improvement run on
``t``: the rate is flat as shipped, inflation steps on the valuation date's anniversaries,
and improvement runs from the valuation date for every point of a block, as
:mod:`~.ULSG_US_S`'s runs from the start of its own projection. Acquisition is charged per
policy issued, from the issue month, and is not inflated, as in
``basiclife/BasicTerm_SE``. On a point issued at ``t = 0`` the two clocks coincide, and
the model computes what :mod:`~.ULSG_US_S` computes.

A point in force opens with its state at the valuation date, per policy, as it stands at
the start of month 0: the account value (floored), the shadow account (never floored),
the loan and the premiums paid to date, ``ULSG_US_S``'s own columns, ``av_pp_init``,
``sg_pp_init``, ``loan_bal_init`` and ``cum_prem_init``; and the months it has already
spent in its grace, ``grace_mth_init``, which ``ULSG_US_S`` reads as 0 at the start of its
frame. A policy whose grace has expired has lapsed, and is not in force: the model point
table carries none, and ``Projection.proj_len`` refuses one. The two pins of the model
point, ``prem_persistency_override`` and ``coi_rate_dp``, hold in every month.

Within each month the notes' monthiversary order is followed exactly. At the beginning
of the month (BOM): the status check, premium and its two loads (one to the account
value, one to the shadow account), withdrawal and its fee, the expense charges, the
death benefit and corridor test, the net amount at risk on **both** accounts, the cost
of insurance on both, and the insufficiency test that decides between a forgone
deduction and the grace period. At the end of the month (EOM): interest on both
accounts and loan interest accrual, the in-force test, then the decrements -- death,
then surrender, then return-of-premium exercise. Premiums and expenses therefore fall
at BOM and are weighted by ``pols_if(t)``; death claims by
``pols_if(t) * mort_rate_mth(t)``, surrenders by
``pols_if(t) * (1 - mort_rate_mth(t)) * lapse_rate_mth(t)`` and refunds by the same
survivors times ``rop_rate(t)``.

Cash flows are **undiscounted**. Loads, charges, interest credits and every
shadow-account entry are internal transfers, not external cash flows: they drive the
account value, the surrender value and the in-force test only.

**One documented deviation from the notes [std].** The notes floor the account value at
zero *only while the guarantee is active*: their step 6 sets ``AV''_t = 0`` in the
guarantee branch and gives the grace branch no account-value recursion at all. This
model applies the floor unconditionally -- in the grace months and after a lapse as
well -- because a negative balance would break the account-value roll-forward, which
closes on the deduction actually taken and nothing is taken from an exhausted account.
No cash flow moves: a policy in grace surrenders for nothing by construction, and
``pols_if(t)`` is zero once it has lapsed. What it does mean is that the per-policy
account-value and forgone-deduction cells keep running after the policy has gone, and
that ``mth_deduction_forgone(t)`` is the guarantee's running cost only while
``is_guar_supported(t)`` holds -- in grace the same figure is the notes' required grace
payment instead. ``products/guaranteed_ul/model.md`` says so, and a test pins it.

**What is sourced and what is not.** The contractual elements come from the product
specification's composite of retrieved carrier documents: the 25% premium load and the
$5.50 monthly per-policy charge [S3][S7], the 2.0% guaranteed credited rate
[S3][S5][S7], the 5.0%/3.0% loan rates [S4], the 61-day grace period [S7], the
return-of-premium percentages, anniversaries and 40%-of-face cap [S1], the in-force
test on the shadow account net of indebtedness [S4][S2][S9], and the cessation of
charges at attained age 121 [S7]. **Every shadow-account parameter is a
standardization** -- no carrier publishes them and no specimen policy form was
retrieved -- as are the $0.20 and $0.05 per-unit charges, the 65% current-to-guaranteed
COI factor, the 3.5% current credited rate, the 15-year $18 per $1,000 surrender
charge, the mortality and lapse tables, the mortality improvement scale, the dynamic
lapse formulas, the return-of-premium exercise rates, the premium persistency
probability and every expense. The illustrative guaranteed maximum COI curve shipped
in ``coi_rates.csv`` is **not** the 2017 CSO table, which is licensed and may not be
reproduced here; it is a Perks curve fitted to the two figures the technical notes
state -- 8.615 per $1,000 per month at attained age 85, and a solved level lifetime
no-lapse premium near $10,800 for the anchor cell. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables with
company data before drawing any conclusion from the output.

**Not implemented.** Modules the technical notes describe but do not specify completely
enough to project, or that belong to a different layer, all named here and in
``products/guaranteed_ul/model.md`` so their absence is not mistaken for an oversight:

* The **cumulative-premium-test** guarantee design (AG 38 8E Design #2). The notes
  document it as a swap of ``SG_t`` for the pair (``CumPrem^net``, ``ReqPrem``), but
  give no required-premium schedule, so there is nothing to project.
* **Catch-up premium payment.** The catch-up requirement ``C_t`` is a complete formula
  and is implemented as the diagnostic
  :func:`~.ULSG_US_SEC.Projection.catch_up_prem_pp`; the notes state expressly that
  catch-up behaviour is not modelled in the base run, so no catch-up premium is ever
  paid and no guarantee is ever restored.
* **Grace cure.** The required cure payment is implemented as
  :func:`~.ULSG_US_SEC.Projection.cure_premium_pp`, but the notes give no cure
  probability, so no policy pays it. A grace ends without a lapse only where the
  month's deduction stops failing on its own, as when a scheduled premium falls due and
  carries it; otherwise a policy that enters grace lapses when the 61 days expire.
* **New policy loans, repayments and withdrawal utilisation.** The mechanics are
  implemented -- loan interest accrual, the loaned/unloaned interest split, the
  dollar-for-dollar shadow reduction, the $25 fee -- but the notes set utilisation to
  zero in the base model point and give no pattern, so ``loan_bal_pp(t)`` only rolls an
  opening balance forward and ``wd_pp`` comes from the model point table.
* **7702 / 7702A testing.** Guideline premium limits and MEC status are flagged by the
  notes as out of model; they cap or classify premiums and generate no insurer cash
  flow, and no guideline premium inputs are given for this product.
* **Terminal illness acceleration**, treated as cash-flow-neutral by the notes;
  **selective-lapse mortality adjustment**, which the notes exclude expressly; and
  **non-guaranteed-element re-rating**, which is out of scope.
* **Reserves.** Like the rest of this library the model stops at gross liability cash
  flows; VM-20 ULSG, AG 38 and A-830 consume them and are cited, not reproduced.

**The funding-premium solve is not in this model.** :mod:`~.ULSG_US_S` implements the
notes' complete algorithm, a bisection over the level annual premium of a replay of the
shadow recursion with decrements off, as a side calculation that nothing in its
projection reads, and its tests check it. It is an issue-time calculation: the premium a
policy was issued on, which a point in force carries from issue as an input, as
``basiclife/BasicTerm_SE`` reads its premium from a table. So this model reads the
premium from the model point's ``premium_pp_ann`` and leaves the solve to
:mod:`~.ULSG_US_S`, whose four cells it does not copy. Kept unchanged here, the solve
would answer a question no point valued later asks: it replays the shadow account from
the frame's first month rather than from the policy's issue, so on a point in force it
solves from the valuation date, and on a point written later, whose months before issue
enter its minimum at zero, it finds no premium at all. And its cells take the premium as
a float argument, which a compiled model could cache only in a Python dictionary. To
solve a policy's premium from a later state, give :mod:`~.ULSG_US_S` a point carrying
that state, as its in-force point 1 does: it solves from that point's own start.

**Model points.** ``model_point_table_sec.csv`` is generated from :mod:`~.ULSG_US_S` and
its model point table, and the tests regenerate it and compare, so no row is typed by
hand. Every point is on the anchor cell male 60 ANB / NT Standard / $500,000, because the
illustrative COI table covers that cell alone. Points 1 to 4 are the twins of
:mod:`~.ULSG_US_S`'s four points: point 1, the technical notes' worked-example point, in
force 300 months at the valuation date with an account value of $2,400, a shadow account
of $118,000, $270,000 of premiums paid and a level $10,800 annual premium, whose
``t = 0`` is the worked example's first month, policy month 301, and its 25th
anniversary, where the return-of-premium window opens; point 2, the same policy issued at
the valuation date, the base behavioural run; point 3, which funds the same lifetime
guarantee with a single premium; and point 4, which elects a guarantee to age 90 and
underfunds it. Three of the four lapse for insufficiency, each two months after its grace
opens: point 1 at policy month 382, its grace opening at 380, point 2 at 504 and point 4
at 236, as in :mod:`~.ULSG_US_S`; point 3 never does. Points 5 to 8 are S points restated
in force at an S month, each opened with the state :mod:`~.ULSG_US_S` carries into that
month: point 1 at policy month 381, a month into its grace, its shadow account below
zero, which lapses at ``t = 1``; point 2 on its 20th anniversary, at 240, where its first
return-of-premium window falls at ``t = 0``; point 2 at 305, mid-year, its account value
exhausted and the guarantee carrying it, where its policy anniversaries and the valuation
date's part; and point 3 in its last month, 731, a frame of one month. Point 9 is point
2 to be issued 25 months after the valuation date. Points 6, 7 and 9 lapse with S point
2, at its policy month 504, which is ``t = 264``, ``199`` and ``529`` of theirs; points 3
and 8 never lapse. A model point on any other issue age, sex or class requires
``coi_rates.csv`` to be extended first; a test asserts every model point in the table
actually projects.

**Verification.** On points 2, 3 and 4, the twins issued at the valuation date, every
cell this model shares with :mod:`~.ULSG_US_S` agrees with it at every argument the S
model evaluates in its sweep, ``pols_if_init``, ``model_point`` and ``result_pols``
excepted. On point 1, :mod:`~.ULSG_US_S`'s in-force point, which both models open at the
valuation date, every cell agrees from ``t = 0`` on with expense inflation set to 0 in
both, and as shipped every cell but the inflation factor, the expenses, the expense
margin, the net cash flow and the report that holds them. So the goldens
``tests/test_guaranteed_ul_us.py`` asserts on point 1 hold here too, with no number
restated: every cell of all five of the worked example's rows -- premium, net premium to
each account, the monthly deductions on each account, the interest credited to each, both
closing balances, the forgone deduction and the status -- together with the notes' NAAR
constants, the exhaustion of the account value in policy month 304 (``t = 3``) and the
guarantee carrying the contract from policy month 305 (``t = 4``).
``tests/test_guaranteed_ul_us_sec.py`` splices: an S point restated in force at month
``d``, opened with S's own state there, continues the S projection from ``d`` on, cell by
cell. A point issued ``k`` months late is the S projection ``k`` months on, and the
committed table is what S generates.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/guaranteed_ul/ULSG_US_SEC")
    >>> model.Projection[1].result_av()
    >>> model.Projection[5].result_guar()
"""

from modelx.serialize.jsonvalues import *

_name = "ULSG_US_SEC"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

