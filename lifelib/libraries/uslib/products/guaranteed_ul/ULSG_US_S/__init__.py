# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for U.S. guaranteed universal life (ULSG).

:mod:`~.ULSG_US_S` is the executable counterpart of
``products/guaranteed_ul/technical-notes.md`` in the lifelib-products library. It
projects gross liability cash flows for a single-life, flexible-premium universal life
policy with a **single shadow-account secondary guarantee** (AG 38 8E Policy Design #1
[R1]; VM-01 shadow-account definition [R2]): level death benefit only, a notional
guarantee account with its own load, charges and credited rate, an in-force test
``SG - L > 0`` that keeps the contract alive after the real account value is exhausted,
a built-in return-of-premium endorsement at anniversaries 20 and 25 [S1], a 15-year
surrender charge, and no maturity date -- charges and premiums cease at attained age
121 and coverage continues [S7].

The product is built on the universal life chassis. Its technical notes say so
explicitly, and this model follows :mod:`.UL_US_S` in structure, naming and
processing order, deviating only where the guaranteed-UL notes restate a recursion with
their own parameters. The two documented deviations are that the account value for the
net amount at risk is measured **after the expense charges and before the cost of
insurance** (the UL chassis measures it before the entire monthly deduction), and that
the guaranteed-UL notes' ``CSV_t`` already nets policy debt, which is the chassis'
``ncsv_pp``.

**Spaces.** The model contains two:

:mod:`~.ULSG_US_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.ULSG_US_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.ULSG_US_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps on policy monthiversaries. ``t`` counts **policy
months** from the start of the projection, 1-based: ``t = 1`` is the issue month of a
new-business model point and the first projected month of an in-force cell, which sits
``duration_mth_init()`` completed policy months after issue. The technical notes index
the same months by their absolute policy month number, starting at
``duration_months + 1``; the worked example's months 301-305 are therefore ``t = 1``
to ``t = 5`` here, with ``duration_mth(t) = 300 + t - 1``. State variables the notes
define at ``t = 0`` -- ``AV_0``, ``SG_0``, ``L_0``, ``CumPrem_0``, ``l_0 = 1``,
``g_0 = 0`` -- are the ``t == 0`` branch of the corresponding recursion.

``proj_len() = 12 * (121 - age_at_entry()) - duration_mth_init()``, the notes' maximum
projection length: the projection runs to attained age 121, where charges and premiums
cease. Coverage continues past that point in the contract [S7]; the illustrative
mortality table reaches 1.0 at attained age 120, so nothing survives the horizon and
``pols_maturity(t)`` is identically zero -- guaranteed UL has no maturity date.

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
payment instead. The README says so, and a test pins it.

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
enough to project, or that belong to a different layer, all named here and in the
README so their absence is not mistaken for an oversight:

* The **cumulative-premium-test** guarantee design (AG 38 8E Design #2). The notes
  document it as a swap of ``SG_t`` for the pair (``CumPrem^net``, ``ReqPrem``), but
  give no required-premium schedule, so there is nothing to project.
* **Catch-up premium payment.** The catch-up requirement ``C_t`` is a complete formula
  and is implemented as the diagnostic
  :func:`~.ULSG_US_S.Projection.catch_up_prem_pp`; the notes state expressly that
  catch-up behaviour is not modelled in the base run, so no catch-up premium is ever
  paid and no guarantee is ever restored.
* **Grace cure.** The required cure payment is implemented as
  :func:`~.ULSG_US_S.Projection.cure_premium_pp`, but the notes give no cure
  probability, so a policy that enters grace always lapses when the 61 days expire.
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

The **funding-premium solve** *is* implemented, because the notes give the complete
algorithm: :func:`~.ULSG_US_S.Projection.no_lapse_premium` bisects
:func:`~.ULSG_US_S.Projection.guar_min_sg` over the level annual premium with
decrements off, on the notes' own domain. It is a side calculation; nothing in the
projection depends on it.

**Model points.** ``model_point_table.csv`` carries four points, all on the anchor cell
male 60 ANB / NT Standard / $500,000, because the illustrative COI table covers that
cell alone. Point 1 is the technical notes' worked-example model point: an in-force
cell at 300 completed policy months with an account value of $2,400, a shadow account
of $118,000 and a level $10,800 annual premium. Point 2 is the same policy from issue,
which is the base behavioural run and the cell whose solved no-lapse premium the tests
check. Point 3 funds the same lifetime guarantee with a single premium, exercising the
single-pay lapse multiplier. Point 4 elects a guarantee to age 90 and underfunds it, so
the shadow account runs out, the catch-up requirement becomes positive, the grace
period opens and the policy lapses for insufficiency -- the one path the other three
never take. A model point on any other issue age, sex or class requires
``coi_rates.csv`` to be extended first; a test asserts every model point in the table
actually projects.

**Verification.** Model point 1 is the anchor of the worked example in the technical
notes, and ``tests/test_guaranteed_ul_us.py`` asserts every cell of all five of its
rows -- premium, net premium to each account, the monthly deductions on each account,
the interest credited to each, both closing balances, the forgone deduction and the
status -- together with the notes' NAAR constants, the exhaustion of the account value
in month 304 and the guarantee carrying the contract from month 305.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/guaranteed_ul/ULSG_US_S")
    >>> model.Projection[1].result_av()
"""

from modelx.serialize.jsonvalues import *

_name = "ULSG_US_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]

