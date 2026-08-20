# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.CI_UK_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 2            # or switch the default

``t`` counts **policy months**, 1-based: ``t = 1`` is the first projected month and
``t = proj_len() = 12 x term`` the last. The notes index the in-force probability
``l(t)`` at the **end** of month ``t`` with ``l(0) = 1``; the library indexes
:func:`pols_if` at the **start** of the month, so ``pols_if(t)`` is the notes' ``l(t-1)``
and the notes' ``l(t)`` is :func:`pols_if_at` ``(t, "AFT_DECR")``. That is deliberate:
``pols_if(t)`` is then the weight on the same ``result_cf()`` row's cash flows, which is
the convention every model in this library shares.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/critical_illness/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``CI_UK_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.CI_UK_S.Data`,
reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
ci_rate_file            data.ci_rate_table()            ci_rate_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for annual rates and ``*_rate_mth`` for monthly ones, ``*_pp``
for per-policy amounts, ``claims(t, kind)`` and ``benefit_pp(t, kind)`` with an
uppercase ``kind`` string, ``pols_if_at(t, timing)`` for the within-month in-force
reads. The technical notes use compact actuarial symbols instead. The mapping is:

===================  ===============================  ================================
Notes symbol         Cells                            Meaning
===================  ===============================  ================================
contract_type        contract_type()                  accelerated or standalone
issue_age            age_at_entry(life)               Issue age (ANB), life 1 or 2
a                    age(t, life)                     Attained age (ANB) in month t
y = ceil(t/12)       policy_year(t)                   Policy year containing month t
(none)               duration(t)                      Completed policy years, y - 1
(none)               duration_mth(t)                  Months elapsed at end of month t
n                    policy_term()                    Term in years
12n                  proj_len()                       Last projected month
SA                   sum_assured()                    Sum assured at outset
SA(t)                benefit_pp(t, "MAIN")            Sum assured in month t, indexed
B_AP                 benefit_pp(t, "AP")              Additional-payment benefit
B_ch                 benefit_pp(t, "CHILD")           Children's-cover benefit
P                    premium_mth_pp()                 Monthly premium at outset
P(t)                 premium_pp(t)                    Monthly premium in month t
(pivot table)        pivot_interp(x, sex, smoker, c)  Log-linear pivot lookup
i_ci(a)              ci_rate_base(t, life)            Table CI diagnosis rate
(1 + tau)^(y-1)      ci_trend_factor(t)               CI trend factor
eta                  sel_lapse_ci_loading             Anti-selection loading on i_ci
(none)               ci_sel_factor(t)                 Anti-selection factor applied
i_ci x trend x sel   ci_rate(t, life)                 CI diagnosis rate applied
q_d(a)               mort_rate(t, life)               Best-estimate mortality rate
k                    overlap_k                        Death/CI overlap factor, 0.10
(per life)           claim_rate_life(t, life)         q_d(1-k) + i_ci, one life
q_claim(a)           claim_rate(t)                    Combined claim decrement
q_pay(a)             claim_rate_paid(t)               The part that pays a benefit
delta                survival_slip                    Standalone slippage, 0.03
q_m(t)               claim_rate_mth(t)                Monthly combined decrement
q_pay_m(t)           claim_rate_paid_mth(t)           Monthly paying decrement
q_exit_m(t)          claim_rate_exit_mth(t)           Monthly non-paying decrement
a(x)                 ap_rate(t)                       Additional-payment frequency
a_m(t)               ap_rate_mth(t)                   The same, monthly
lambda_ch            child_freq                       Children's claim frequency p.a.
lambda_m             child_rate_mth()                 The same, monthly
w(y)                 lapse_rate(t)                    Annual lapse rate in month t
(table)              lapse_rate_base(t)               Table lapse rate before shock
w_shock              lapse_rate(t) at a review        Post-review shock lapse
w_m(t)               lapse_rate_mth(t)                Monthly lapse rate
rho_review           review_prem_shock                Premium change at a review
(none)               reviews_passed(t)                Reviews already applied
(none)               review_shock_active(t)           In the post-review window
l(t-1)               pols_if(t)                       In force at the start of month t
l(t)                 pols_if_at(t, "AFT_DECR")        In force at the end of month t
(none)               pols_if_at(t, timing)            BEF_DECR / BEF_LAPSE / AFT_DECR
(none)               pols_claim(t)                    Main-benefit claims in month t
(none)               pols_lapse(t)                    Lapses at the end of month t
(none)               pols_maturity(t)                 Expiries at the end of the term
idx(t)               idx_factor(t)                    Cover indexation factor
idx_p(t)             idx_prem_factor(t)               Premium indexation factor
P x l                premiums(t)                      Premium income
SA x q_m x l         claims(t, "MAIN")                Main-benefit outgo
B_AP x a_m x l       claims(t, "AP")                  Additional-payment outgo
B_ch x lambda_m x l  claims(t, "CHILD")               Children's-cover outgo
0                    claims(t, "LAPSE")               Surrender outgo; always zero
E_cl x q_m x l       claim_expenses(t)                Claim handling expense
E0, E_m(y)           expenses(t)                      Initial + maintenance expense
(none)               inflation_factor(t)              Expense inflation factor
CF(t)                net_cf(t)                        Net cash flow, income positive
===================  ===============================  ================================

Three names needed care.

The notes write ``a(x)`` for the additional-payment frequency and ``a`` for the attained
age in the same table. :func:`ap_rate` and :func:`age` separate them; nothing in the
model is called ``a``.

``q_d`` is the best-estimate mortality rate and is spelled :func:`mort_rate`, the
library-wide name, even though on this product mortality never acts as a decrement on
its own: it enters only through :func:`claim_rate`, net of the overlap. Keeping the
name makes the input visible where a reader looks for it.

``SA`` is a constant in the notes and a function of ``t`` here, because the indexation
option moves it. ``benefit_pp(t, "MAIN")`` is that quantity; :func:`sum_assured` is the
outset value the model point carries. The additional-payment and children's benefits
are derived from the *indexed* sum assured **[std]** — the notes state their caps
against ``SA`` without saying which ``SA``, and applying the cap to a frozen outset
value would make the benefit shrink in real terms while the main benefit did not.

.. rubric:: The combined decrement, and why the rates cannot be added

The insured event is *death or first CI diagnosis, whichever comes first*. Adding
``q_d`` and ``i_ci`` double-counts lives that are both diagnosed and die in the same
period: once the CI claim has been paid the subsequent death of that life is not a
second claim, and a death inside the survival period converts the CI claim into a death
claim of the same amount rather than adding one. So

    q_claim(a) = i_ci(a)(1 + tau)^(y-1) + q_d(a)(1 - k)          **[std]**

where ``k`` is the proportion of deaths preceded by a claimable diagnosis. ``k = 0.10``
flat is a standardization: the cause-of-claim splits that would calibrate it live in
CMI working papers whose datasets are subscriber-restricted. ``k = 0`` maximally
double-counts and ``k = 0.25`` may understate, so the notes rate it the third-largest
lever on the liability and it is a Reference rather than a literal.

On the **accelerated** contract nothing further is needed: however the overlap
resolves, ``SA`` is paid once. The 14-day survival period is cash-flow-neutral there
and is not modelled, which is the notes' second pitfall — applying the survival-period
slippage ``delta`` to the accelerated main benefit is wrong, because a death inside the
period still pays ``SA`` as a death claim.

On the **standalone** contract death pays nothing, and the decrement splits::

    q_pay(a)  = i_ci(a)(1 + tau)^(y-1) (1 - delta)
    q_exit(a) = q_d(a)(1 - k) + i_ci(a)(1 + tau)^(y-1) delta

with the same total, so the in-force run-off is identical and only the *paid* part
generates outgo. Note where ``k`` goes: onto the non-paying death exit, never onto the
paid decrement. Applying it to ``q_pay`` instead is the mirror-image pitfall and
understates claims.

One divergence from the notes' literal text. The notes convert annual rates to monthly
with ``1 - (1 - q)^(1/12)`` and prescribe ``q_pay_m`` for the standalone main benefit,
but converting ``q_pay`` and ``q_exit`` independently leaves their sum slightly below
the ``q_m`` the same notes use for the in-force run-off — the two conventions are
inconsistent at second order. :func:`claim_rate_paid_mth` follows the notes literally
and :func:`claim_rate_exit_mth` is defined as the **residual** ``q_m - q_pay_m``, so the
split is exact by construction and the run-off is the notes'.
:func:`check_claim_split` bounds the artefact: it asserts the residual really is the
independently converted ``q_exit`` to within ``claim_split_tol``, which on the
shipped points it is by four decimal places or better.

.. rubric:: The non-terminating benefits

The additional-payment and children's-cover benefits are the notes' third and fourth
pitfalls, and they are one mistake in two directions. Both are **non-depleting** —
they do not reduce the sum assured — and **non-terminating** — they do not decrement
the in-force. Only the main benefit ends the policy. Modelling them as accelerations
of the sum assured is a different product; terminating the policy on one is the same
error with the opposite sign.

They are carried as frequency loadings on the in-force, ``a_m`` and ``lambda_m``, and
appear in the roll-forward nowhere at all: :func:`pols_if_at` never sees them. Note the
monthly conversion is ``rate / 12`` and not ``1 - (1 - rate)^(1/12)``, which is correct
and deliberate: these are claim *frequencies* — expected events per year, repeatable —
not probabilities of a terminating event, so there is no survival transform to apply.

The treatment deliberately ignores the contractual claim-count caps — one per
additional-payment condition, two children's claims, and the per-child cross-policy
limit — because at the **[std]** frequencies shipped here the probability of reaching a
cap is second order. Respecting them exactly would need claim-count state variables.

.. rubric:: The rate basis is interpolated, not tabulated

``ci_rate_table.csv`` holds six pivot ages and the notes' rule is to interpolate
log-linearly between them, so :func:`pivot_interp` does exactly that: geometric in the
rate, linear in age. Outside the pivot range it continues the nearest end segment's
gradient, which is the same expression with the exponent out of [0, 1] — an
extrapolation, and flagged as one, because a 25-year policy issued at 40 stays inside
the pivots but a longer or younger one does not.

Both rate sets are **[std]** placeholders shaped like the tables the notes name — AC04
and the "16" Series for diagnosis, a scaled population table for mortality — and must
not be presented as CMI or ONS values. The sex and smoker cells are the male
non-smoker pivots times flat factors, which is cruder still: real accelerated-CI
experience is not a flat female factor, since breast cancer makes female incidence
exceed male at the younger ages. The file's ``provenance`` column marks which cells came
from the notes and which from a factor.

.. rubric:: The reviewable variant

``premium_guarantee = reviewable`` turns on a 5-yearly review from the fifth
anniversary. Premiums are constant between reviews and multiplied by
``1 + rho_review`` at each one; the snapshot is ``rho_review = 0``, so the variant runs
identically to the guaranteed one until the Reference is moved. Two behavioural
responses hang off the same switch, both **[std]**:

- a **review shock lapse** in the twelve months after a review that raises premiums by
  more than 5%, ``min(0.30, w(y) + 2.0 max(0, rho - 0.05))``; and
- **selective lapsation** from the first such shock onward, loading the diagnosis rate
  by ``1 + eta`` on the lives that remain, because the healthier ones leave first.

The economics are the point of the variant rather than the cash flows: guaranteed
premiums mean morbidity deterioration and definition drift fall entirely on the
insurer, and the reviewable design transfers that to policyholders at the cost of these
two responses.

.. rubric:: What this product does not have

No account value, no asset share, no surrender or paid-up value, no bonus, no market
value reduction, and no commission line — the notes fold acquisition cost into the £200
initial expense rather than carrying commission separately as the term assurance
chassis does. There is likewise no interest-sensitive dynamic lapse: with no cash value
and no credited rate there is nothing to arbitrage, so the machinery the accumulation
products in this library carry is deliberately absent. ``claims(t, "LAPSE")`` exists and
returns zero so that the absence of a surrender value is stated rather than inferred.

.. rubric:: Sign convention

The notes' ``Net CF`` is income positive, which is the library-wide sign of
:func:`net_cf`, so there is no outgo-positive ``liability_cf`` companion here. One
caveat for a reader checking the worked example by eye: the notes' **Net CF column
excludes the initial expense** — at month 1 it shows 31.88, with the £200 initial
expense noted separately as taking the month to -168.12. :func:`net_cf` is the total,
so ``net_cf(1)`` is -168.12 and the notes' column is ``net_cf(1) + 200``.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def contract_type():
    """``accelerated`` (death or CI, whichever first) or ``standalone`` (CI only).

    On the standalone variant death pays nothing and simply terminates the policy
    [S4][S11]; a premium-refund-on-death feature exists in some designs and is excluded
    **[std]**.
    """
    v = model_point()["contract_type"]
    if v not in ("accelerated", "standalone"):
        raise ValueError("invalid contract_type")
    return v


def life_basis():
    """``single`` or ``joint_first_event``.

    The joint variant is a two-life survivorship product the notes place outside the
    base model **[std scope]**.  It is not combined with the standalone contract: the
    notes write the standalone decrement split for one life only, and there is no
    published basis for splitting a joint first-event decrement into paying and
    non-paying parts, so the combination raises rather than inventing one.
    """
    v = model_point()["life_basis"]
    if v not in ("single", "joint_first_event"):
        raise ValueError("invalid life_basis")
    if v == "joint_first_event" and contract_type() == "standalone":
        raise ValueError("standalone joint first event is out of scope")
    return v


def is_joint():
    """True when the policy covers two lives on a first-event basis."""
    return life_basis() == "joint_first_event"


def age_at_entry(life=1):
    """The issue age (ANB) of the first (``life = 1``) or second life.

    Age nearest birthday, attained age advancing on policy anniversaries **[std]**.
    Any consistent basis works, but it must be the same one for the diagnosis rates,
    the mortality rates and the attained-age indexing - a mismatch there is one of the
    notes' listed pitfalls.
    """
    if life == 1:
        return int(model_point()["age_at_entry"])
    if life == 2 and is_joint():
        return int(model_point()["joint_age"])
    raise ValueError("invalid life")


def sex(life=1):
    """The sex (M / F) of the first or second life."""
    if life == 1:
        return model_point()["sex"]
    if life == 2 and is_joint():
        return model_point()["joint_sex"]
    raise ValueError("invalid life")


def smoker(life=1):
    """The smoker status (NS / S) of the first or second life."""
    if life == 1:
        return model_point()["smoker"]
    if life == 2 and is_joint():
        return model_point()["joint_smoker"]
    raise ValueError("invalid life")


def sum_assured():
    """SA: the sum assured at outset **[std]**, £100,000 on the anchor cell.

    :func:`benefit_pp` ``(t, "MAIN")`` is the amount actually at risk in month t, which
    differs from this once the indexation option is elected.
    """
    return float(model_point()["sum_assured"])


def policy_term():
    """n: the term in years, 5-50 [S2][S5]; the policy also ends by the 75th birthday."""
    return int(model_point()["policy_term"])


def cover_basis():
    """The cover shape.  Level only: decreasing and FIB shapes are out of scope here.

    Both exist on the term assurance chassis this product sits on and are implemented
    in ``Term_UK_A``; these notes scope them out **[std scope]**.
    """
    v = model_point()["cover_basis"]
    if v != "level":
        raise ValueError("invalid cover_basis")
    return v


def premium_guarantee():
    """``guaranteed`` [S1] or ``reviewable``, which turns on the 5-yearly review cycle."""
    v = model_point()["premium_guarantee"]
    if v not in ("guaranteed", "reviewable"):
        raise ValueError("invalid premium_guarantee")
    return v


def premium_mth_pp():
    """P: the monthly premium per policy at outset **[std]**, £55.00 on the anchor cell.

    A placeholder, not a market rate: no UK insurer publishes CI rate cards, so any
    reference premium is constructed.  Profitability conclusions drawn from the worked
    example are meaningless.
    """
    return float(model_point()["premium_mth"])


def premium_mode():
    """Monthly or annual premium payment.

    Inert: the grid is monthly and the notes carry the premium as a monthly amount
    either way.  Carried because the model point attribute table names it.
    """
    return model_point()["premium_mode"]


def children_cover():
    """Whether children's cover is active; automatic on the composite product [S1]."""
    return bool(model_point()["children_cover"])


def indexation():
    """Whether the increasing-cover option is elected; false in the base run **[std]**.

    Declining an increase three years running removes the option [S1][S4]; the base
    model assumes full take-up while the option is active, so that rule is never
    reached and is not implemented.
    """
    return bool(model_point()["indexation"])


def pols_if_init():
    """Initial number of policies in force; 1.0 on a single-policy model point."""
    return float(model_point()["pols_if_init"])


def proj_len():
    """Projection length in months: ``12 x term``.

    The policy expires at the end of the term with no maturity and no surrender value
    [S1][S4][S5], so there is nothing after it.
    """
    return 12 * policy_term()


def duration(t):
    """Completed policy years at the start of month t: ``(t - 1) // 12``."""
    return (t - 1) // 12


def duration_mth(t):
    """Months elapsed from issue at the end of month t; equal to t.

    ``t`` is 1-based, so the identity is trivial - the cells exists so the monthly
    models in this library share one vocabulary.
    """
    return t


def policy_year(t):
    """y = ceil(t/12): the policy year containing month t; 1 for t = 1..12."""
    return duration(t) + 1


def age(t, life=1):
    """a: the attained age (ANB) of ``life`` in the policy year containing month t."""
    return age_at_entry(life) + duration(t)


def pivot_interp(x, sex_, smoker_, column):
    """Log-linear interpolation of ``column`` at age x from the pivot table.

    Geometric in the rate and linear in age::

        r(x) = r0 (r1/r0)^((x - x0)/(x1 - x0))

    which is the notes' "interpolate log-linearly between pivot ages" **[std]** written
    without a logarithm.  Outside the pivot range the nearest end segment's gradient is
    continued - the same expression with the exponent outside [0, 1] - which is an
    **extrapolation** and should be read as one: the shipped pivots run 40 to 65, so a
    policy issued young or running long leaves the tabulated region.
    """
    sub = data.ci_rate_table().loc[(sex_, smoker_)]                  # noqa: F821
    ages = sorted(int(a) for a in sub.index)
    if x <= ages[0]:
        lo, hi = ages[0], ages[1]
    elif x >= ages[-1]:
        lo, hi = ages[-2], ages[-1]
    else:
        lo = max(a for a in ages if a <= x)
        hi = min(a for a in ages if a > x)
    r_lo = float(sub.loc[lo, column])
    r_hi = float(sub.loc[hi, column])
    return r_lo * (r_hi / r_lo) ** ((x - lo) / (hi - lo))


def ci_rate_base(t, life=1):
    """i_ci(a): the table CI diagnosis rate for ``life`` in the year containing month t.

    First diagnosis of a listed condition, total and permanent disability included.  A
    **[std]** proxy shaped like an insured-lives accelerated-CI diagnosis-rate table -
    the AC04 and "16" Series values are subscriber-restricted - and not to be presented
    as a CMI rate.
    """
    return pivot_interp(age(t, life), sex(life), smoker(life), "i_ci")


def mort_rate(t, life=1):
    """q_d(a): the best-estimate annual mortality rate for ``life`` **[std]**.

    Never a decrement on its own: on this product mortality enters only through
    :func:`claim_rate`, net of the overlap factor.  A **[std]** proxy shaped like a
    scaled population table, not an ONS value.
    """
    return pivot_interp(age(t, life), sex(life), smoker(life), "q_d")


def ci_trend_factor(t):
    """(1 + tau)^(y-1): the CI trend factor in the year containing month t **[std]**.

    Zero trend in the base run.  It is the notes' *first*-listed sensitivity anyway:
    diagnosis rates move with medical practice, and the covered event itself moves when
    the ABI revises its model definitions - the 2021/22 review broadened Alzheimer's to
    all dementia, tightened cancer staging and excluded myocardial injury from heart
    attack.  Those are **step** changes that no trend parameter anticipates, so the
    basis must be re-mapped at each definition generation rather than trended through
    one.
    """
    return (1.0 + ci_trend) ** (policy_year(t) - 1)                  # noqa: F821


def ci_sel_factor(t):
    """1 + eta once a review shock has occurred; 1 otherwise **[std]**.

    Healthier lives lapse first when premiums rise, so the lives remaining after a
    review shock carry loaded diagnosis rates.  Reachable only on the reviewable
    variant, and only once a review has actually raised premiums past the shock
    threshold; ``sel_lapse_ci_loading`` is 0.10 in the notes and the magnitude is a
    placeholder.
    """
    if premium_guarantee() != "reviewable":
        return 1.0
    if reviews_passed(t) < 1:
        return 1.0
    if review_prem_shock <= review_lapse_threshold:                  # noqa: F821
        return 1.0
    return 1.0 + sel_lapse_ci_loading                                # noqa: F821


def ci_rate(t, life=1):
    """The CI diagnosis rate applied to ``life`` in month t: table x trend x selection."""
    return ci_rate_base(t, life) * ci_trend_factor(t) * ci_sel_factor(t)


def claim_rate_life(t, life=1):
    """The combined annual claim decrement for one life: ``i_ci + q_d (1 - k)``.

    The overlap term is what stops the two rates being added.  See the Space docstring
    for why, and for the bounds on ``k``.
    """
    return ci_rate(t, life) + mort_rate(t, life) * (1.0 - overlap_k)  # noqa: F821


def claim_rate(t):
    """q_claim(a): the combined annual claim decrement applied to the policy.

    One life's rate on a single-life policy; on a joint first-event policy the joint
    decrement ``1 - (1 - q_1)(1 - q_2)`` **[std]** on one policy, which pays once and
    ends.  Capped at 1.
    """
    q1 = claim_rate_life(t, 1)
    if not is_joint():
        return min(1.0, q1)
    q2 = claim_rate_life(t, 2)
    return min(1.0, 1.0 - (1.0 - q1) * (1.0 - q2))


def claim_rate_paid(t):
    """q_pay(a): the part of the claim decrement that pays the main benefit.

    The whole of it on the **accelerated** contract, where death and CI both pay ``SA``
    and the 14-day survival period is cash-flow-neutral.  On the **standalone**
    contract only diagnoses that survive the period pay, ``i_ci(1 - delta)``; deaths pay
    nothing and neither do diagnoses followed by death inside the period.  The overlap
    factor ``k`` belongs to the non-paying exit and never appears here - applying it to
    the paid decrement understates claims, which is the mirror image of the
    double-counting pitfall.
    """
    if contract_type() == "accelerated":
        return claim_rate(t)
    return ci_rate(t, 1) * (1.0 - survival_slip)                     # noqa: F821


def claim_rate_mth(t):
    """q_m(t) = 1 - (1 - q_claim)^(1/12): the monthly combined decrement **[std]**.

    This is what runs the in-force off, on both contract types: the standalone variant
    terminates on death as well, it simply pays nothing for it.
    """
    return 1.0 - (1.0 - claim_rate(t)) ** (1.0 / 12.0)


def claim_rate_paid_mth(t):
    """q_pay_m(t) = 1 - (1 - q_pay)^(1/12): the monthly paying decrement.

    Equal to :func:`claim_rate_mth` on the accelerated contract, where every claim pays.
    """
    return 1.0 - (1.0 - claim_rate_paid(t)) ** (1.0 / 12.0)


def claim_rate_exit_mth(t):
    """q_exit_m(t): the monthly decrement that terminates the policy without paying.

    Defined as the **residual** ``q_m - q_pay_m`` rather than by converting ``q_exit``
    independently, so that the paying and non-paying parts sum exactly to the decrement
    that runs the in-force off.  Converting both annual parts independently would leave
    their sum slightly below ``q_m``: the notes' additive annual split and their
    ``1 - (1 - q)^(1/12)`` conversion are inconsistent at second order.
    :func:`check_claim_split` bounds the difference rather than hiding it.  Zero on the
    accelerated contract.
    """
    return claim_rate_mth(t) - claim_rate_paid_mth(t)


def ap_rate(t):
    """a(x) = 0.15 i_ci(a): the annual additional-payment claim frequency **[std]**.

    A **frequency**, not a probability: additional-payment conditions are payable more
    than once across the schedule, subject to one claim per condition, and they never
    terminate the policy.
    """
    return ap_freq_factor * ci_rate(t, 1)                            # noqa: F821


def ap_rate_mth(t):
    """a_m(t) = a(x)/12: the monthly additional-payment frequency **[std]**.

    Divided by twelve rather than transformed by ``1 - (1 - a)^(1/12)``, because a
    frequency of repeatable events has no survival transform to apply.  The notes use
    the same approximation and say so.
    """
    return ap_rate(t) / 12.0


def child_rate_mth():
    """lambda_m = lambda_ch/12: the monthly children's-cover claim frequency **[std]**.

    Flat in age and duration, and zero if children's cover is not active.  Like the
    additional-payment frequency it is per-year events divided by twelve, not a
    probability conversion.
    """
    if not children_cover():
        return 0.0
    return child_freq / 12.0                                         # noqa: F821


def reviews_passed(t):
    """The number of premium reviews already applied at month t.

    Reviews fall every ``review_period_mths`` from the fifth anniversary [S3][S4], so
    the first bites in month 61.  Always zero on guaranteed-premium business, where the
    premium cannot be changed at all.
    """
    if premium_guarantee() != "reviewable":
        return 0
    return (t - 1) // review_period_mths                             # noqa: F821


def review_shock_active(t):
    """Whether month t falls in the twelve months after a premium-raising review.

    The window a review shock lapse applies in.  A review that raises premiums by less
    than the threshold produces no shock at all.
    """
    if reviews_passed(t) < 1:
        return False
    if review_prem_shock <= review_lapse_threshold:                  # noqa: F821
        return False
    return (t - 1) % review_period_mths < 12                         # noqa: F821


def idx_increase():
    """The cover increase offered at each anniversary under the indexation option.

    ``min(max(RPI, 0), 10%)`` [S1][S4] on a flat 3% RPI scenario **[std]**.
    """
    return min(max(rpi_rate, 0.0), idx_cover_cap)                    # noqa: F821


def idx_factor(t):
    """idx(t): the cumulative **cover** indexation factor in month t.

    Steps on policy anniversaries, so it is ``(1 + increase)^(y - 1)``; 1 throughout if
    the option is not elected.
    """
    if not indexation():
        return 1.0
    return (1.0 + idx_increase()) ** (policy_year(t) - 1)


def idx_prem_factor(t):
    """idx_p(t): the cumulative **premium** indexation factor in month t.

    The premium rises by ``min(1.5 x increase, 15%)`` for a cover increase of
    ``increase`` [S1][S4] - the same x1.5 factor the term assurance chassis carries.
    """
    if not indexation():
        return 1.0
    step = min(idx_prem_mult * idx_increase(), idx_prem_cap)         # noqa: F821
    return (1.0 + step) ** (policy_year(t) - 1)


def premium_pp(t):
    """P(t): the monthly premium per policy in month t.

    The outset premium, indexed if the option is elected, and multiplied by
    ``1 + rho_review`` once per review already passed.  On guaranteed-premium business
    - the base run - it is level for the whole term, which is what puts every month of
    premium inside the Solvency UK contract boundary.
    """
    p = premium_mth_pp() * idx_prem_factor(t)
    return p * (1.0 + review_prem_shock) ** reviews_passed(t)        # noqa: F821


def premiums(t):
    """Premium income at the beginning of month t, an inflow.

    Carried on the survivors at the start of the month, :func:`pols_if`.
    """
    return premium_pp(t) * pols_if(t)


def lapse_rate_base(t):
    """The table annual lapse rate in month t **[std]**, before any review shock.

    10 / 8 / 6 / 6 / 6 / 4 percent by policy year.  Protection lapse is duration-skewed
    - buyer's remorse, remortgaging, distribution churn - and levels off later; UK CI
    lapse studies are proprietary, so the levels are calibrations to be replaced with
    the user's own experience.  Policy years beyond the table take its last row.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    y = policy_year(t)
    return float(tbl.loc[min(y, int(tbl.index.max())), "lapse_rate"])


def lapse_rate(t):
    """w(y): the **annual** lapse rate applying in month t, review shock included.

    ``min(0.30, w(y) + 2.0 max(0, rho_review - 0.05))`` in the twelve months after a
    review that raises premiums by more than 5% **[std]**, and the table rate otherwise.
    Review-driven shocks are the dominant behavioural risk on reviewable business,
    where one insurer's review changes are subject to no stated limit at all; the slope
    and the cap are placeholders.

    There is no interest-sensitive dynamic lapse anywhere in this model.  With no cash
    value and no credited rate there is nothing to arbitrage, so the machinery the
    accumulation products in this library carry is deliberately absent.
    """
    w = lapse_rate_base(t)
    if not review_shock_active(t):
        return w
    shock = w + review_lapse_slope * max(                            # noqa: F821
        0.0, review_prem_shock - review_lapse_threshold)             # noqa: F821
    return min(review_lapse_cap, shock)                              # noqa: F821


def lapse_rate_mth(t):
    """w_m(t) = 1 - (1 - w(y))^(1/12): the monthly lapse rate **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """The number of policies in force at the **start** of policy month t.

    The notes' ``l(t-1)``, and the weight on every cash flow of the same
    ``result_cf()`` row.  ``pols_if_init()`` in month 1, then the notes' recursion
    ``l(t) = l(t-1)(1 - q_m)(1 - w_m)``.  Zero once the term has run out.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after main-benefit claims, before lapses - the notes' processing
        order is **claim before lapse** **[std order]**, so this is the
        population lapses are taken from.

    ``"AFT_DECR"``
        the notes' ``l(t)``, the end-of-month state, and zero from the last
        month on because the cover expires there.

    The additional-payment and children's-cover claims appear at none of these points.
    They are non-terminating: only the main benefit ends the policy.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - claim_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 1 or t >= proj_len():
            return 0.0
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_claim(t):
    """Main-benefit claims in month t: death, terminal illness or CI diagnosis.

    The whole combined decrement, including the standalone contract's non-paying
    deaths - they terminate the policy just the same.  What is *paid* on them is
    :func:`claims` ``(t, "MAIN")``.
    """
    return pols_if(t) * claim_rate_mth(t)


def pols_lapse(t):
    """Lapses at the end of month t, taken from the non-claiming survivors.

    Pays nothing: there is no surrender or paid-up value [S1][S4][S5].  The 60-day
    grace period is not modelled separately - the lapse rates are assumed already to
    reflect grace-period cures **[std]**.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """Policies whose cover expires at the end of the term; zero in every other month.

    Not a decrement and not a benefit - the contract runs out, with no maturity value -
    but needed for the in-force roll-forward to close; see :func:`check_pols_roll_fwd`.
    """
    if t != proj_len():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))


def benefit_pp(t, kind):
    """The benefit amount per policy in month t, by kind.

    ``"MAIN"``
        SA(t), the sum assured, indexed if the option is elected.

    ``"AP"``
        the additional-payment benefit ``min(25% of SA(t), £25,000)``
        [S1][S4][S11] - £25,000 at the anchor cell, and **non-depleting**: it
        does not reduce the main benefit.

    ``"CHILD"``
        children's cover ``min(50% of SA(t), £25,000)`` [S1], also
        non-depleting, and zero if the cover is not active.  The £4,000 child
        funeral benefit is excluded as de minimis **[std]**.

    Both caps are struck against the **indexed** sum assured **[std]**: the notes state
    them against ``SA`` without saying which, and holding them to a frozen outset value
    would let the ancillary benefits shrink in real terms while the main one did not.
    In practice the cash cap binds at the anchor cell either way.
    """
    if kind == "MAIN":
        return sum_assured() * idx_factor(t)
    if kind == "AP":
        return min(ap_share * benefit_pp(t, "MAIN"), ap_cap)         # noqa: F821
    if kind == "CHILD":
        if not children_cover():
            return 0.0
        return min(child_share * benefit_pp(t, "MAIN"), child_cap)   # noqa: F821
    raise ValueError("invalid kind")


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"MAIN"``
        ``SA(t) x q_pay_m(t) x l``, the terminating benefit.  On the
        accelerated contract every claim pays; on the standalone one only
        diagnoses surviving the 14-day period do.

    ``"AP"``
        ``B_AP x a_m(t) x l``, non-terminating and non-depleting.

    ``"CHILD"``
        ``B_ch x lambda_m x l``, likewise.

    ``"LAPSE"``
        zero, always.  There is no surrender or paid-up value [S1][S4][S5];
        the kind exists so that the zero is stated rather than inferred.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("MAIN", "AP", "CHILD", "LAPSE"))
    if kind == "MAIN":
        return benefit_pp(t, "MAIN") * claim_rate_paid_mth(t) * pols_if(t)
    if kind == "AP":
        return benefit_pp(t, "AP") * ap_rate_mth(t) * pols_if(t)
    if kind == "CHILD":
        return benefit_pp(t, "CHILD") * child_rate_mth() * pols_if(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def claim_expenses(t):
    """E_cl x q_m(t) x l: the claim handling expense in month t **[std]**.

    £250 per main claim, uninflated, carried on the **whole** combined decrement rather
    than on the paying part: a notified death on a standalone contract costs the
    insurer to assess even though it pays nothing.  That is the notes' own formula.
    Kept out of :func:`expenses` because the notes' worked example prints the two as
    separate columns.
    """
    return expense_claim * claim_rate_mth(t) * pols_if(t)            # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y - 1)`` **[std]**.

    Steps on policy anniversaries, not monthly, which is how the notes write it.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """E0 and E_m(y): the initial and maintenance expense in month t **[std]**.

    £200 per policy at issue, then £30 per policy per year - a twelfth of it each month
    - inflating at 3%, both at the beginning of the month.  There is **no commission
    line** on this product: the notes fold acquisition cost into the initial expense
    rather than carrying commission separately as the term assurance chassis does.
    """
    acq = expense_acq * pols_if(t) if t == 1 else 0.0                # noqa: F821
    return acq + expense_maint / 12.0 * inflation_factor(t) * pols_if(t)  # noqa: F821


def net_cf(t):
    """CF(t): the net cash flow of month t, **income positive**.

    Premiums less main, additional-payment and children's claims, claim expense and
    expenses.  The notes' own sign, and the library-wide one, so there is no
    outgo-positive ``liability_cf`` companion.

    One caveat for a reader checking the worked example by eye: the notes' *Net CF*
    column **excludes the initial expense**, showing 31.88 at month 1 and noting the
    £200 separately as taking the month to -168.12.  This cells is the total, so
    ``net_cf(1)`` is -168.12 and the notes' column is ``net_cf(1) + 200``.
    """
    return premiums(t) - claims(t) - claim_expenses(t) - expenses(t)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - main claims - lapses - expiries``.  The
    additional-payment and children's-cover claims are absent by design: they are
    non-terminating, and their appearance here would be the notes' fourth pitfall.
    Expiries are non-zero only in the last month, where the survivors neither claim nor
    lapse - their cover runs out.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_claim(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives
    the signed residual of the month that failed.  The tolerance scales with
    ``pols_if_init()``, since the residual accumulates rounding on that many policies.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(pols_if_init(), 1.0)
               for t in range(1, proj_len() + 1))


def check_claim_split_resid(t):
    """How far the residual exit rate is from an independently converted ``q_exit``.

    :func:`claim_rate_exit_mth` is defined as ``q_m - q_pay_m`` so that the split is
    exact; the notes' own construction would instead convert the annual ``q_exit``
    directly.  The two differ because the notes add the annual parts but convert them
    geometrically, which cannot both hold.  This residual is that inconsistency, made
    visible: it is zero on the accelerated contract and of order 1e-5 on the standalone
    one at the shipped rates, growing with the level of the rates.
    """
    if contract_type() == "accelerated":
        return 0.0
    q_exit = (mort_rate(t, 1) * (1.0 - overlap_k)                    # noqa: F821
              + ci_rate(t, 1) * survival_slip)                       # noqa: F821
    return claim_rate_exit_mth(t) - (1.0 - (1.0 - q_exit) ** (1.0 / 12.0))


def check_claim_split():
    """True when the paying/non-paying split stays inside ``claim_split_tol``.

    No argument, one bool over all t, the library-wide shape of a ``check_*`` cells.
    Unlike a roll-forward check this one is not an identity that must hold exactly - it
    bounds a known second-order artefact of the notes' two conventions - so its
    tolerance is a Reference rather than a machine epsilon, and moving that Reference is
    how a user states how much of the artefact they will accept.
    """
    return all(abs(check_claim_split_resid(t)) <= claim_split_tol    # noqa: F821
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cashflows, indexed by policy month t.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash
    flow on the same row.  ``net_cf`` carries the notes' own income-positive sign and
    **includes** the initial expense, unlike the notes' own Net CF column.
    ``claims_lapse`` is a column of zeros by product design - there is no surrender
    value - and is published rather than dropped.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_main": [claims(t, "MAIN") for t in ts],
            "claims_ap": [claims(t, "AP") for t in ts],
            "claims_child": [claims(t, "CHILD") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy month t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_claim": [pols_claim(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
            "ci_rate": [ci_rate(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "claim_rate": [claim_rate(t) for t in ts],
            "claim_rate_mth": [claim_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

overlap_k = 0.1

survival_slip = 0.03

ci_trend = 0.0

ap_freq_factor = 0.15

ap_share = 0.25

ap_cap = 25000.0

child_freq = 0.0004

child_share = 0.5

child_cap = 25000.0

expense_acq = 200.0

expense_maint = 30.0

expense_claim = 250.0

inflation_rate = 0.03

rpi_rate = 0.03

idx_cover_cap = 0.1

idx_prem_mult = 1.5

idx_prem_cap = 0.15

review_period_mths = 60

review_prem_shock = 0.0

review_lapse_slope = 2.0

review_lapse_threshold = 0.05

review_lapse_cap = 0.3

sel_lapse_ci_loading = 0.1

claim_split_tol = 0.0001

pd = ("Module", "pandas")