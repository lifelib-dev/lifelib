# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.IncomeTerm_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 4            # or switch the default

``t`` counts **policy months**, 1-based: ``t = 1`` is the first policy month and
``t = proj_len()`` the last projected one. ``proj_len()`` is **not** the policy term.
It is ``term_m() + guar_m() - 1``, because a claim arising in the last months of cover
carries its guaranteed instalments past the expiry date — see *The run-off tail* below.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/income_guarantee/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``IncomeTerm_JP_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.IncomeTerm_JP_S.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
rate_class_file         data.rate_class_table()         rate_class_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_mth`` for the monthly form of an annual rate, ``*_pp`` for per-policy
amounts, ``claims(t, kind)`` with an uppercase ``kind`` string,
``pols_if_at(t, timing)`` for the within-month in-force reads. The technical notes use
compact actuarial symbols instead. The mapping is:

===================  =====================  =================================
Notes symbol         Cells                  Meaning
===================  =====================  =================================
t                    (the cells argument)   Policy month, 1-based
x                    issue_age()            契約年齢, 満年齢 at issue
x + floor((t-1)/12)  age(t)                 Attained age in month t
y(t)                 policy_year(t)         Policy year of month t
(none)               sex(), rate_class()    Rating factors
N                    term_m()               保険期間 in months
G                    guar_m()               最低支払保証期間 in months
T = N + G - 1        proj_len()             Projection horizon, months
A                    annuity_mth()          年金月額, JPY per month
P_m                  premium_mth_pp()       Monthly office premium
P_due(t)             prem_due_pp(t)         Premium falling due at t
(none)               model_point()          The selected model point
n_pay(m)             pay_count(m)           Instalments a claim at m makes
ends_at(m)           pay_end(m)             Month of that stream's last
(table)              mort_rate_base(t)      死亡保険用 table rate at age(t)
(class factor)       class_factor()         Rate class multiplier
q(t)                 mort_rate(t)           Annual death-and-高度障害 rate
q_m(t)               mort_rate_mth(t)       Monthly equivalent
w(t)                 lapse_rate(t)          Annual ordinary lapse rate
w_m(t)               lapse_rate_mth(t)      Monthly equivalent
lambda               sel_lapse_lambda       Selective-lapsation loading
l_ref                sel_lapse_ref          Selective-lapsation threshold
(none)               sel_lapse_factor(t)    Mortality loading on persisters
l(t)                 pols_if(t)             In force at the start of t
l(t)(1-q_m), l(t+1)  pols_if_at(t, timing)  BEF_DECR / BEF_LAPSE / AFT_DECR
D(t)                 pols_death(t)          Expected new claims in month t
(none)               pols_lapse(t)          Lapses at the end of month t
(none)               pols_maturity(t)       Survivors at expiry, paid nil
(none)               pols_reinst(t)         復活 reinstatements
(none)               pols_payer(t)          Policies actually paying premium
(none)               pols_commute(t)        Claims settled by 一括受取
(none)               pols_living_needs(t)   リビング・ニーズ accelerations
(none)               annuities_open(t)      Streams opened in month t
(none)               annuities_ended(t)     Streams making their last pay
R(t)                 annuities_if(t)        Streams in payment during t
(none)               annuities_cum(t)       Instalments due to date
i_c                  commute_rate           Commutation rate p.a.
v                    commute_disc()         (1 + i_c) ** (-1/12)
L(n)                 commute_pp(t)          Lump sum for one claim at t
(cap)                ln_cap                 リビング・ニーズ cap, JPY
(none)               ln_benefit_pp(t)       リビング・ニーズ payout per claim
(none)               wop_waived_frac(t)     Fraction with premiums waived
P_m l(t)             premiums(t)            Premium income
A R(t)               claims(t, kind)        Benefit outgo by kind
ec D(t)              claim_expenses(t)      Claim expense outgo
ea R(t)              annuity_expenses(t)    Annuity administration outgo
E0, e_m(t)           expenses(t)            Acquisition + maintenance
(none)               inflation_factor(t)    Expense inflation factor
c0, c_r              commissions(t)         Commission outgo
CF(t)                net_cf(t)              Net cash flow, income positive
===================  =====================  =================================

The References carrying the notes' scalar assumptions are ``mort_be_factor`` (the
chassis's 0.80 best-estimate factor), ``expense_acq`` (``E0``), ``expense_maint``
(``e_m`` before inflation), ``expense_claim`` (``ec``), ``expense_annuity`` (``ea``),
``inflation_rate``, ``comm_init_rate`` (``c0``) and ``comm_renewal_rate`` (``c_r``).

Four names needed care.

``claims_annuity`` names a **death** benefit here. The instalments are paid on the death
of the insured, or on the contractual 高度障害 state carried inside the same decrement as
its accelerated equivalent; the name records the benefit's *form*, not its trigger, and
the same column carries a *living* benefit in ``LTC_JP_S`` and ``Annuity_JP_A``. So the
contingency is stated in :func:`claims` and in :func:`result_cf` rather than inferred.
**There is no ``claims_death`` column**, and that absence is a product fact: this
contract pays no lump sum on death at any duration — a claim *opens* an annuity stream
instead of settling one — so the whole death benefit is ``claims_annuity``, and a
zero-valued ``claims_death`` would misdescribe the contract rather than document it.

``R(t)`` is spelled :func:`annuities_if` rather than ``pols_annuity`` because it is
**not a population of policies**. It is a count of instalments falling due in month
``t``, per policy issued. ``pols_if`` and ``annuities_if`` are disjoint quantities that
must never be summed: on the anchor cell ``annuities_if(420) = 0.016780`` while
``pols_if(420) = 0.145023``, and adding them produces a number with no meaning.

``pols_maturity`` has no symbol in the notes. The notes give the roll-forward as
``l(t+1) = l(t)(1-q_m)(1-w_m)`` for ``t < N`` and, separately, set ``l(t) = 0`` for
``t > N``. Those do not reconcile in month ``N``: its survivors neither die nor lapse,
their cover simply runs out. :func:`pols_maturity` names them, zero in every month but
``N``, so that

    pols_if(t) + pols_reinst(t+1) - pols_if(t+1)
        = pols_death(t) + pols_lapse(t) + pols_maturity(t)

holds for every ``t``; :func:`check_pols_roll_fwd` asserts it. It is *not* a maturity
**benefit**: nothing is payable on survival, on this product at any duration.

``claims_lapse`` is a column of zeros by product design. The composite is 無解約返戻金型
— there is no 解約返戻金 at any duration, so a lapse moves :func:`pols_if` and pays
nothing. The zero is published rather than dropped because a non-zero lapse row
imported from a cash-value chassis is one of the notes' listed pitfalls, and a column
of zeros states the product fact where a missing column would only hide it. For the
same reason there is no ``cv_pp`` and no 自動振替貸付 anywhere in this model: with no cash
value there is no collateral to lend against, and one carrier states the absence in
terms.

.. rubric:: The in-payment ledger, and the rule it obeys

The ledger is the whole model. A claim in month ``m`` opens a stream of
``pay_count(m) = max(N - m + 1, G)`` monthly instalments whose last falls in month
``pay_end(m) = max(N, m + G - 1)``, and :func:`annuities_if` counts the streams paying
in month ``t``::

    annuities_if(t) = annuities_if(t-1) - annuities_ended(t) + annuities_open(t)

New claims enter in the **same** month, because the first instalment falls at the end
of the month of the insured event.

**The ledger is never decremented.** Not by the insured's mortality — the insured is
dead, and that is what opened the stream. Not by the recipient's mortality: on the
composite the instalments carry no survival condition, so the stream is an
annuity-certain, confirmed from the contract side by a published factor table that
depends on the payment period and not on the annuitant's age or sex. Not by lapse: a
policy in claim cannot lapse and premiums have ceased. Applying the surviving-policy
factor ``(1 - q_m)(1 - w_m)`` to the ledger — the natural thing to do if it is mistaken
for a population of policies — cuts annuity outgo on the anchor cell from ¥443,313.69
to ¥245,605.66, an understatement of 44.6%, and it is the largest single error
available in this model. :func:`check_annuity_ledger` rebuilds the ledger directly from
the claim vector, with no reference to the recursion, and :func:`check_annuity_total`
checks the instalments due to date against ``sum of D(s) x pay_count(s)``.

.. rubric:: The run-off tail

Every stream opened in months ``1 ... N - G + 1`` pays its last instalment in month
``N`` *exactly*, whenever it opened, because the expiry date is fixed at issue. It
follows that ``annuities_if(N)`` equals the sum of every claim the contract has ever
made — the ledger peaks at exactly month ``N`` — and that the only streams surviving
into month ``N + 1`` are those opened in the last ``G - 1`` months of cover. From
``N + 1`` on, ``annuities_ended(t) = annuities_open(t - G)`` and the ledger runs down
one month's claims at a time.

In months ``N + 1 ... T`` there is no premium, no maintenance expense, no commission
and no new claim, because ``pols_if(t) = 0`` there: only the annuity instalments and
the annuity administration expense remain. That is why ``expense_annuity`` is charged
against the ledger rather than against ``pols_if`` — it is the one expense that
survives the end of the policy term, and an implementation that attaches every expense
to the in-force population charges nothing at all in those months.

**最低支払保証期間 is a term extension, not a benefit floor.** Both readings pay the same
``max(N - m + 1, G)`` instalments, so an undiscounted *total* cannot tell them apart;
they differ in *when*. A floor implementation compresses the guaranteed instalments
inside the term and produces zero cash flow after month ``N``. This model pays them
after expiry, on the same monthly timetable: on the anchor cell ¥2,645.21 of claim
outgo — 0.5967% of the total — falls in months 421 to 443.

.. rubric:: Modules that are off in the base run

Five of the notes' optional constructions are implemented and switched off, so that
the base run reproduces the worked example while the machinery stays visible and
testable:

- **一括受取 (full commutation)**, ``commutation`` on the model point, false on the
  anchor. The claim is settled at the claim date by :func:`commute_pp`, the present
  value of the ``pay_count(m)`` instalments at ``commute_rate`` **[std]**, and the
  ledger is then **not opened at all** for that claim — a full commutation
  extinguishes the contract, so a model that pays the lump sum *and* opens the stream
  doubles the benefit. Partial commutation is out of scope **[std scope]**: it is
  barred once the first instalment has been paid, limited to once during the term at
  two carriers, and refused where the residual 年金月額 falls below ¥50,000, which makes
  it an election on a claim already open rather than a cash-flow shape. Model point 4
  runs it on.
- **リビング・ニーズ特約**, ``living_needs`` on the model point, false on the anchor. A
  **[std]** proportion ``ln_take_up`` of the month's claims is settled instead as an
  acceleration, at the 年金現価 of the designated 年金月額 less six months' interest and
  premium equivalent, capped at ``ln_cap`` = ¥30,000,000 and barred in the final year.
  It is carved *out* of the death decrement rather than added to it, because the
  insured is by definition within six months of death; the ``<= 6``-month timing shift
  is ignored on this grid **[std]**. The product-specific consequence is that because
  the amount is the present value of an income stream, the **cap binds from month 1**
  and stops binding only once the unpaid stream falls below it — the opposite pattern
  to a level sum assured. Model point 5 runs it on.
- **保険料払込免除**, ``wop`` on the model point, false on the anchor. A two-state
  incidence/recovery chain **[std]** on the premium-paying population, on the
  accident-plus-180-days-plus-別表4 test. 別表4 is a materially lower bar than the 別表3
  高度障害 schedule, so the incidence is **not** the 高度障害 incidence and deliberately does
  not reuse :func:`mort_rate`. Model point 7 runs it on.
- **復活 (reinstatement)**, ``reinstatement`` on the model point, false on the anchor. A
  **[std]** proportion ``reinst_rate`` of each month's lapses returns to in force
  ``reinst_lag_m`` months later — a single-lag approximation of the three-year window
  ``reinst_window_m`` **[std]** — paying its arrears with interest. The rate class
  carries over unchanged on reinstatement, which matters here because the class is a
  mortality parameter. Model point 8 runs it on.
- **Selective lapsation**, ``q_eff(t) = q(t) [1 + lambda max(0, 1 - l(t)/l_ref)]``, with
  ``sel_lapse_lambda = 0``. The mechanism is weaker than on the protection chassis
  because there is no periodic no-underwriting renewal to select against, but it is not
  absent: the rate class is fixed at issue and cannot be changed even if BMI, blood
  pressure or smoking status changes, so a life whose health deteriorates keeps a
  preferred rate while a life whose health improves cannot get one and may re-shop.

Two of the notes' constructions are **not** implemented and are named so the absence is
not read as an oversight. The **recipient-mortality variant** — one carrier alone
conditions second-and-later instalments on the recipient being alive — would need a
post-event mortality basis on a life the contract never underwrote, and the 年金開始後用
table stays on the 2007 vintage; it is out of scope **[std]**. And there is **no 更新**
on this chassis: no retrieved document offers renewal, one states the absence in terms,
and the term is 歳満了 only, so importing the protection chassis's renewal repricing and
its decline decrement would invent a decision, a premium ladder and a decrement the
contract does not have.

.. rubric:: Sign convention

The notes' ``CF(t)`` is already **income positive** — they write ``+ = inflow`` — which
is the library-wide sign of :func:`net_cf`, so there is no outgo-positive
``liability_cf`` companion to publish: one stream, one sign, one name.

Read the undiscounted total honestly. On the anchor cell it is negative, and the reason
is not a bug: the premium is a published *preferred non-smoker* rate while the
assumption basis is a **[std]** adjustment of a *valuation* table carrying a 2-sigma
margin, and the pricing basis that would reconcile them is not public. More
importantly, on this product an undiscounted total is close to meaningless — the
benefit is paid over up to 35 years *after* a claim that itself arises over 35 years,
so the claim leg discounts far harder than the premium leg. Discounting is out of scope
for this library, and a reader who takes the undiscounted total as the liability has
mis-read this product more badly than any other in ``jplib``.
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


def sex():
    """The sex of the insured, ``M`` or ``F``; a rating factor and a table key."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the 契約年齢 (issue age), 満年齢 with the fraction truncated.

    Age last birthday at the 契約日, worked in one carrier's booklet as 35歳7カ月 giving a
    契約年齢 of 35.  Envelope 20-70 on the composite.  Note the basis mismatch this
    creates and does not resolve: 生保標準生命表2018（死亡保険用）is built on a 保険年齢 (age nearest
    birthday) basis, so reading it at 満年齢 reads it half a year early and understates
    mortality.  The bias is stated rather than corrected in the base run; the optional
    ``sqrt(q_x q_{x+1})`` shift belongs to the protection chassis and moves ``q`` **up**.
    """
    v = int(model_point()["issue_age"])
    if not 20 <= v <= 70:
        raise ValueError("issue_age outside the composite envelope 20-70")
    return v


def expiry_age():
    """The attained age at which cover ends, 45-90 on the composite.

    The term is **歳満了 only** — stated to an attained age.  No retrieved document
    offers 年満了 or 更新, so a model point supplying an n-year term would be describing a
    product the composite does not have, and :func:`term_m` is derived from this rather
    than read.
    """
    v = int(model_point()["expiry_age"])
    if not 45 <= v <= 90:
        raise ValueError("expiry_age outside the composite envelope 45-90")
    if v <= issue_age():
        raise ValueError("expiry_age must exceed issue_age")
    return v


def term_m():
    """N: the 保険期間 in months, ``12 x (expiry_age - issue_age)``.

    Derived, not an input.  The 保険料払込期間 equals the 保険期間 always on this composite, so
    there is no 払込満了 step and no separate premium-paying term to carry.
    """
    return 12 * (expiry_age() - issue_age())


def guar_m():
    """G: the 最低支払保証期間 in months, from the composite menu {24, 60}.

    Elected at issue and not changeable.  It is quoted in years and binds in months,
    which is one of the reasons this product cannot be run on an annual grid.
    """
    v = int(model_point()["guar_m"])
    if v not in (24, 60):
        raise ValueError("guar_m outside the composite menu {24, 60}")
    return v


def annuity_mth():
    """A: the 年金月額, JPY per month; ¥50,000 minimum in ¥10,000 steps."""
    v = float(model_point()["annuity_mth"])
    if v < 50000.0 or round(v) % 10000 != 0:
        raise ValueError("annuity_mth below the ¥50,000 floor or off the ¥10,000 step")
    return v


def rate_class():
    """The preferred-risk rate class code, a key into ``rate_class_table.csv``.

    Four classes on the composite — ``nonsmoker_preferred`` (非喫煙者優良体),
    ``nonsmoker_standard`` (非喫煙者標準体), ``smoker_preferred`` (喫煙者優良体) and
    ``smoker_standard`` (喫煙者標準体).  Qualification is published and *measured* rather
    than declared: BMI 18.0 to under 27.0, 最大血圧 under 140 and 最小血圧 under 90 mmHg, no
    tobacco in the past year verified by a コチニン (cotinine) test.  The class is fixed
    at issue and cannot be changed later, which is what gives the selective-lapsation
    module its mechanism.
    """
    v = model_point()["rate_class"]
    if v not in data.rate_class_table().index:                       # noqa: F821
        raise ValueError("unknown rate_class " + str(v))
    return v


def class_factor():
    """The rate class mortality multiplier **[std]**, read from ``rate_class_table.csv``.

    0.70 / 0.90 / 1.05 / 1.35 across the four classes.  **No carrier publishes a class
    differential for this product**, so this is the least evidenced and the largest
    lever in the file: annuity outgo on the anchor cell runs ¥443,313.69 at 0.70 and
    ¥846,803.38 at 1.35, a factor of 1.9 across the composite's own four classes, on a
    premium quoted for the cheapest of them.  The four are given an internal structure
    rather than four free numbers — see :func:`check_class_factor_norm`.
    """
    return float(data.rate_class_table().loc[                        # noqa: F821
        rate_class(), "class_factor"])


def premium_mth_pp():
    """P_m: the level monthly office premium per policy, JPY.

    Level and guaranteed for the whole 保険期間, with no review mechanic and no 更新, so
    the insurer has no unilateral repricing right and the contract boundary is the full
    term.  On the anchor cell ¥2,565 is a *published* rate — the 65歳満了 / 保証2年 /
    非喫煙優良体型 / 年金月額¥150,000 monthly rate for a male aged 30 — and on several other
    model points the rate is likewise published.  Where no published cell exists the
    value is **[std]**; ``model.md`` says which is which.
    """
    return float(model_point()["premium_monthly"])


def premium_mode():
    """The premium frequency: ``monthly``, ``semiannual`` or ``annual``.

    All three are contractual.  The composite defaults to 月払, which is the frequency
    the only published rate grid is quoted in.  The mode changes the *timing* only:
    :func:`prem_due_pp` collects ``12 / f`` months of premium at the start of each
    payment period.  No 前納 or frequency discount is applied, because the discount is
    insurer-set and unpublished **[std scope]**.
    """
    v = model_point()["premium_mode"]
    if v not in ("monthly", "semiannual", "annual"):
        raise ValueError("invalid premium_mode")
    return v


def prem_mode_months():
    """The number of months in one premium payment period: 1, 6 or 12."""
    return {"monthly": 1, "semiannual": 6, "annual": 12}[premium_mode()]


def commutation():
    """Whether claims are settled by a full 一括受取 lump sum; false in the base run."""
    return bool(model_point()["commutation"])


def living_needs():
    """Whether the リビング・ニーズ特約 acceleration module is on; false in the base run.

    The rider is attached automatically and free at three carriers, so its *presence*
    is a product fact; what is switched off in the base run is the **[std]**
    acceleration incidence, which no retrieved document gives.
    """
    return bool(model_point()["living_needs"])


def wop():
    """Whether the 保険料払込免除 waiver module is on; false in the base run.

    The waiver is in the 主契約, not a rider, so it carries no extra premium: premiums
    are waived where the insured, from an 不慮の事故 on or after the 責任開始期, comes within
    180 days to a 別表4 身体障害の状態.  Disease-based waiver is a rider only and is out of
    scope.
    """
    return bool(model_point()["wop"])


def reinstatement():
    """Whether the 復活 module is on; false in the base run.

    復活 is available for three years from lapse, on fresh underwriting and arrears with
    interest.  Japanese policies really do come back, which is a genuine difference from
    the UK composite in ``uklib``, where a lapsed policy terminates finally.
    """
    return bool(model_point()["reinstatement"])


def pols_if_init():
    """l(1) = 1: the model point is a single policy on an expected basis.

    Every cash flow below is therefore *per policy issued*, probability-weighted, which
    is the sense the ESR 現在推計 (*genzai suikei*, current estimate) requires.
    """
    return 1.0


def proj_len():
    """T: the projection horizon in months, ``term_m() + guar_m() - 1``.

    **Not the policy term.**  Where the insured event falls so late that fewer than
    ``G`` months remain, the annuity payment period is extended past the expiry date
    until the guarantee has run, so the last instalment any claim can make falls in
    month ``N + G - 1``.  On the anchor cell that is 443 against a term of 420.
    Terminating the projection at ``t = N`` drops ¥2,645.21 of contractual claim outgo,
    0.5967% of the total, all of it in months 421-443 — the most natural error to make
    on this product and the least visible, because every remaining number still looks
    reasonable.
    """
    return term_m() + guar_m() - 1


def policy_year(t):
    """y(t): the policy year containing month t, ``1 + floor((t - 1) / 12)``."""
    return 1 + (t - 1) // 12


def age(t):
    """The attained age of the insured at the start of policy month t.

    ``x + floor((t - 1) / 12)`` on the 満年齢 basis of :func:`issue_age`.  Beyond
    ``term_m()`` the value is nominal: cover has expired, ``pols_if(t)`` is zero and no
    rate is read at it.
    """
    return issue_age() + (t - 1) // 12


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi) ** (y(t) - 1)`` **[std]**.

    Annual steps within the monthly grid, so maintenance expense inflates once a policy
    year rather than once a month.  1.0% p.a.; no Japanese public source supports any
    expense level or inflation rate in this model.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def mort_rate_base(t):
    """The 死亡保険用 table rate at the attained age of month t, before adjustment.

    Read from ``mort_table.csv``, which is a **[std]** construction anchored on the
    individual 生保標準生命表2018（死亡保険用）rates the technical notes quote and attribute —
    *not* a copy of the published table, whose publisher prohibits redistribution.  The
    rate **includes 高度障害**, which is why 高度障害 is not a second decrement here: adding a
    separate 高度障害 incidence on top of the table double-counts the benefit, and the two
    annuities are contractually mutually exclusive in any case.
    """
    return float(data.mort_table().loc[                              # noqa: F821
        (sex(), age(t)), "mort_rate"])


def sel_lapse_factor(t):
    """The selective-lapsation loading on mortality in month t **[std]**.

    ``1 + lambda max(0, 1 - l(t) / l_ref)``.  Off in the base run
    (``sel_lapse_lambda = 0``), where it returns 1 in every month.  The mechanism is
    weaker here than on the protection chassis, which has a periodic no-underwriting
    renewal to select against, but it is not absent: the rate class is fixed at issue
    and cannot be changed, so a life whose health deteriorates keeps a preferred rate
    while a life whose health improves cannot get one and may re-shop.
    """
    if sel_lapse_lambda == 0.0:                                      # noqa: F821
        return 1.0
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, 1.0 - pols_if(t) / sel_lapse_ref)                       # noqa: F821


def mort_rate(t):
    """q(t): the **annual** best-estimate death-and-高度障害 rate in policy month t.

    ``0.80 x class_factor x q_x^tab``, times the selective-lapsation loading.  The 0.80
    is the protection chassis's **[std]** best-estimate factor: 標準生命表2018 is a
    *valuation* table carrying a margin sized to about a 2-sigma exceedance probability
    and capped at 130% of the unadjusted rate, plus a forward improvement allowance, so
    a best-estimate basis is an adjustment of it whatever else is done.  Three separate
    departures from the statutory basis therefore sit between this projection and a
    責任準備金, and no reserve is computed anywhere in this library.

    Zero beyond ``term_m()``: cover has expired and there is nothing left to decrement.
    """
    if t < 1 or t > term_m():
        return 0.0
    return min(1.0, mort_be_factor * class_factor()                  # noqa: F821
               * mort_rate_base(t) * sel_lapse_factor(t))


def mort_rate_mth(t):
    """q_m(t): the monthly death-and-高度障害 rate, ``1 - (1 - q(t)) ** (1/12)`` **[std]**.

    The effective convention, not a nominal ``q / 12``.  On the anchor cell at attained
    age 30 this is about 3.17e-05, which is why the claim and ledger populations are
    carried to nine decimals: six would leave them with two significant figures --
    0.000032 against 0.000031738873, a 0.8% distortion of the first policy year's
    claims.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate(t):
    """w(t): the **annual** ordinary lapse rate in policy month t **[std]**.

    Read from ``lapse_table.csv`` by policy year — 9 / 7 / 6 / 5.5 / 5 percent, the last
    row applying to policy year 5 and beyond.  Zero beyond ``term_m()``.

    A lapse pays nothing: there is no 解約返戻金 at any duration on the composite, so this
    moves :func:`pols_if` and nothing else.  Note that the *sign* of the lapse
    sensitivity here is the opposite of the protection chassis's: on this assumption set
    expected claims exceed premiums, so lapse relieves the liability — undiscounted net
    cash flow is -¥269,617.32 at zero lapse against -¥103,051.56 on this table.
    """
    if t < 1 or t > term_m():
        return 0.0
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())), "lapse_rate"])


def lapse_rate_mth(t):
    """w_m(t): the monthly lapse rate, ``1 - (1 - w(t)) ** (1/12)`` **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def pols_if(t):
    """l(t): the policies in force at the **start** of policy month t.

    ``pols_if_init()`` at ``t = 1``, then the notes' recursion
    ``l(t+1) = l(t)(1 - q_m(t))(1 - w_m(t))`` for ``t < N``, plus any 復活
    reinstatements.  This is the weight on the premium, maintenance and commission
    lines of the same ``result_cf()`` row — and on *nothing else*: the annuity
    instalments carry :func:`annuities_if` instead.

    **Zero for every ``t > term_m()``.**  Cover ends at the expiry date with nothing
    payable on survival, and the months after it belong entirely to the run-off of
    claims that arose inside the term.
    """
    if t < 1 or t > term_m():
        return 0.0
    if t == 1:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR") + pols_reinst(t)


def pols_if_at(t, timing):
    """The policies in force at a point inside policy month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if`.

    ``"BEF_LAPSE"``
        after deaths, before lapses — the notes' processing order is **death
        before lapse** **[std order]**, so this is the population lapses are
        taken from.

    ``"AFT_DECR"``
        the end-of-month state, and zero from ``term_m()`` on, because the
        survivors of the last month of cover leave with nothing rather than
        rolling forward.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 1 or t >= term_m():
            return 0.0
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t) = l(t) q_m(t): expected new claims at the end of policy month t.

    One decrement covering death and 高度障害 together, because the table includes 高度障害
    and the two annuities are mutually exclusive.  **No lump sum is paid**: except under
    the two optional settlement modules, the claim *opens* an annuity stream and does
    not settle one.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Lapses at the end of policy month t, taken from the survivors of mortality.

    失効 follows the 猶予期間, which for 月払 runs to the last day of the month after the
    払込期月.  Pays nothing: there is no 解約返戻金 at any duration on the composite, and with
    no cash value there is no 自動振替貸付 to carry the policy through an unpaid premium
    either.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """Survivors whose cover expires at the end of month ``term_m()``; zero elsewhere.

    Not a decrement and not a benefit — the contract simply runs out, with no 満期保険金
    and no 解約返戻金 — but needed for the in-force roll-forward to close in the last month
    of cover.  On the anchor cell it is 0.144342 of the original cohort.
    """
    if t != term_m():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))


def pols_reinst(t):
    """復活 reinstatements returning to force at the start of month t; off in the base run.

    A **[std]** proportion ``reinst_rate`` of the lapses of month ``t - reinst_lag_m``
    comes back, a single-lag approximation of the three-year ``reinst_window_m``
    window.  The rate class carries over unchanged on reinstatement, which matters here
    because the class is a mortality parameter; the arrears with interest they pay are
    in :func:`premiums` through :func:`prem_arrears_pp`.
    """
    if not reinstatement() or t <= reinst_lag_m or t > term_m():     # noqa: F821
        return 0.0
    if reinst_lag_m > reinst_window_m:                               # noqa: F821
        raise ValueError("reinst_lag_m outside the 復活 window")
    return reinst_rate * pols_lapse(t - reinst_lag_m)                # noqa: F821


def wop_waived_frac(t):
    """The fraction of in-force policies with premiums waived at the start of month t.

    A two-state incidence/recovery chain **[std]**,
    ``u(t+1) = u(t)(1 - rec_m) + (1 - u(t)) inc_m``, starting from ``u = 0``.  Both
    rates are placeholders: no public Japanese incidence basis for the
    accident-plus-180-days-plus-別表4 test appears in the sources.  別表4 is a materially
    lower bar than the 別表3 高度障害 schedule, so the incidence is deliberately **not**
    :func:`mort_rate`.  Mortality and lapse are assumed independent of the waiver state
    **[std]**, which is what lets the waived population be carried as a fraction of the
    in-force rather than as its own decrement.  Zero unless the module is on.
    """
    if not wop() or t <= 1:
        return 0.0
    inc_m = 1.0 - (1.0 - wop_inc_rate) ** (1.0 / 12.0)               # noqa: F821
    rec_m = 1.0 - (1.0 - wop_rec_rate) ** (1.0 / 12.0)               # noqa: F821
    u = wop_waived_frac(t - 1)
    return u * (1.0 - rec_m) + (1.0 - u) * inc_m


def pols_payer(t):
    """The in-force policies actually paying premium in policy month t.

    ``l(t)`` less the waived fraction.  Equal to :func:`pols_if` unless the 保険料払込免除
    module is on.  Premiums also cease on the annuity event, but that needs no term
    here: a policy in claim has already left :func:`pols_if`.
    """
    return pols_if(t) * (1.0 - wop_waived_frac(t))


def pay_count(m):
    """n_pay(m) = max(N - m + 1, G): the instalments a claim in month m generates.

    One instalment per monthly payment date from the insured event to the 保険期間満了日,
    floored at the 最低支払保証期間.  The rule reproduces every published illustration in
    the source set: on ``N = 420``, 420 instalments for a claim in month 1, 240 for
    month 181 and 60 for month 361; 411 for month 10 and 178 for month 243; and on a
    5年 guarantee, 60 for a death 33 years in, where the remaining term is 24 months and
    the guarantee binds.
    """
    return max(term_m() - m + 1, guar_m())


def pay_end(m):
    """ends_at(m) = max(N, m + G - 1): the month of that stream's last instalment.

    The whole guarantee mechanic in one expression.  For ``m <= N - G + 1`` every
    stream ends at exactly ``N``, whenever it opened, because the expiry date is fixed
    at issue; only later claims run past it.
    """
    return max(term_m(), m + guar_m() - 1)


def commute_disc():
    """v = (1 + i_c) ** (-1/12): the monthly discount factor of the commutation basis."""
    return (1.0 + commute_rate) ** (-1.0 / 12.0)                     # noqa: F821


def annuity_certain_factor(n):
    """a(n) = v (1 - v^n) / (1 - v): an n-instalment annuity-certain, monthly in arrears.

    The commutation basis is **[std]** at ``commute_rate`` = 0.65% p.a. effective, and
    it is the best-evidenced [std] number in the product.  No direct writer publishes a
    discount basis, but one 特約条項 publishes the factor table itself — 年金の現価相当額 =
    基本年金額 times a tabulated rate with **no dependence on the annuitant's age or sex**
    — which fits an annual annuity-due less a small constant at about 0.61% p.a., and
    three carriers publish a worked commutation amount whose ratios cluster at 0.92190,
    0.92183 and 0.92133, the last two implying 0.66%.  The midpoint of those two
    independent anchors is 0.635%; 0.65% is that rounded to the nearest 0.05%, and it
    reproduces the two 300-instalment amounts to +0.12% and +0.18%, inside their
    published rounding.  It
    does *not* reproduce the 180-instalment amount, and no single flat rate can produce
    a near-constant ratio at both 180 and 300 instalments — a fact about the data, not a
    failure of the fit.  Observed range to test over: 0.61%-1.45%.
    """
    if n <= 0:
        return 0.0
    v = commute_disc()
    return v * (1.0 - v ** n) / (1.0 - v)


def commute_pp(t):
    """L(n): the 全部一括受取 lump sum settling one claim arising in month t.

    ``A a(n_pay(t))``.  A full commutation **extinguishes the contract**, so with the
    module on the ledger must not open at all for that claim.  On the anchor cell a
    death in month 1 commutes ¥63,000,000 of instalments to ¥56,352,381.90, a ratio of
    0.894482; at 300 remaining instalments the ratio is 0.922965, against the
    0.92133-0.92190 the three published illustrations show.
    """
    return annuity_mth() * annuity_certain_factor(pay_count(t))


def ln_benefit_pp(t):
    """The リビング・ニーズ特約 payout per accelerated claim in month t.

    The 年金現価 of the designated 年金月額 — taken as the whole of it **[std]** — less six
    months' interest and six months' premium equivalent, capped at ``ln_cap`` and
    barred in the final year before expiry.  Because the amount is the present value of
    an income stream, **the cap binds from month 1** on the anchor cell, where the full
    年金現価 at issue is ¥56,352,381.90, and stops binding only once the unpaid stream has
    run down below ¥30,000,000 — the opposite pattern to a level sum assured, where a
    cap either always binds or never does.
    """
    if t > term_m() - 12:
        return 0.0
    gross = (commute_pp(t) * (1.0 + commute_rate) ** (-ln_defer_m / 12.0)
             - ln_defer_m * premium_mth_pp())                           # noqa: F821
    return max(0.0, min(ln_cap, gross))                              # noqa: F821


def pols_living_needs(t):
    """The claims of month t settled instead as a リビング・ニーズ acceleration.

    ``ln_take_up x D(t)`` **[std]**; zero unless the module is on or where the rider is
    barred.  Carved **out** of the death decrement rather than added to it: the insured
    is by definition within six months of death, so an added decrement would
    double-count the benefit.  The ``<= 6``-month timing shift the acceleration really
    produces is ignored on this grid **[std]**.
    """
    if not living_needs() or ln_benefit_pp(t) <= 0.0:
        return 0.0
    return ln_take_up * pols_death(t)                                # noqa: F821


def pols_commute(t):
    """The claims of month t settled by a full 一括受取 lump sum; zero in the base run."""
    if not commutation():
        return 0.0
    return pols_death(t) - pols_living_needs(t)


def annuities_open(t):
    """The annuity streams opened by the claims of month t.

    ``D(t)`` less any claim settled as a lump sum instead — a full commutation or a
    リビング・ニーズ acceleration.  They enter :func:`annuities_if` in the **same** month,
    because the first instalment falls at the end of the month of the insured event:
    contractually the day before the first monthly policy anniversary falling on or
    after it, which on a monthly grid is exactly one payment in the month of the event.
    """
    return pols_death(t) - pols_commute(t) - pols_living_needs(t)


def annuities_ended(t):
    """The streams whose last instalment fell in month ``t - 1``.

    Two cases exhaust it.  At ``t = N + 1`` every stream opened in months
    ``1 ... N - G + 1`` ends at once, because each of them ran to the fixed expiry
    date whenever it opened.  Beyond that the ledger runs down one month's claims at a
    time, ``annuities_open(t - G)``.
    """
    n, g = term_m(), guar_m()
    if t == n + 1:
        return sum(annuities_open(s) for s in range(1, n - g + 2))
    if t > n + 1:
        return annuities_open(t - g)
    return 0.0


def annuities_if(t):
    """R(t): the annuity streams in payment during policy month t, per policy issued.

    ``R(t) = R(t-1) - ended(t) + opened(t)``, ``R(0) = 0``.  **Never decremented** — not
    by the insured's mortality, not by the recipient's, not by lapse.  It is a count of
    instalments falling due, *not* a population of policies, and must never be summed
    with :func:`pols_if`.

    The ledger peaks at exactly month ``N``, where it equals the sum of every claim the
    contract has ever made: 0.016779783 on the anchor cell.  An implementation that
    ends streams one month early gets that identity wrong and nothing else visibly
    changes, which is why :func:`check_annuity_ledger` rebuilds it directly.
    """
    if t < 1 or t > proj_len():
        return 0.0
    return annuities_if(t - 1) - annuities_ended(t) + annuities_open(t)


def annuities_cum(t):
    """The instalments due from month 1 to month t inclusive, per policy issued.

    The running total of :func:`annuities_if`.  Over the whole projection it reconciles
    to ``sum of D(s) x pay_count(s)`` — 2.955425 on the anchor cell, an average total
    benefit of ¥26,419,511.96 per claim — which is what :func:`check_annuity_total`
    asserts.
    """
    if t < 1:
        return 0.0
    return annuities_cum(t - 1) + annuities_if(t)


def prem_due_pp(t):
    """The office premium falling due per paying policy at the start of month t.

    ``P_m`` every month on 月払; on 半年払 and 年払, ``12 / f`` months' premium at the start
    of each payment period and nothing in between.  Zero beyond ``term_m()``: the
    保険料払込期間 equals the 保険期間, and premiums cease on the annuity event in any case —
    which needs no term here, because a policy in claim has already left
    :func:`pols_if`.
    """
    if t < 1 or t > term_m():
        return 0.0
    p = prem_mode_months()
    return premium_mth_pp() * p if (t - 1) % p == 0 else 0.0


def prem_arrears_pp():
    """The arrears with interest one reinstating policy pays **[std]**.

    ``reinst_lag_m`` months of premium accumulated at ``reinst_int_rate`` over half the
    lag.  復活 requires the arrears *with interest*; the interest rate is nowhere
    published, so it is standardized at the commutation basis for want of a better one.
    """
    return (premium_mth_pp() * reinst_lag_m                             # noqa: F821
            * (1.0 + reinst_int_rate) ** (reinst_lag_m / 24.0))      # noqa: F821


def premiums(t):
    """Premium income at the start of policy month t, an inflow.

    Carried on :func:`pols_payer` and on nothing else.  **Premiums stop on the annuity
    event; the benefit does not** — netting the two against one combined population
    would collect ¥7,535.43 of premium on the anchor cell, 1.63% of the total, from
    policies that are in claim and paying nothing.  The 復活 arrears, where that module
    is on, arrive here too.
    """
    return (prem_due_pp(t) * pols_payer(t)
            + prem_arrears_pp() * pols_reinst(t))


def claims(t, kind=None):
    """Benefit outgo at the end of month t; every kind here is paid on **death**.

    The contingency is stated rather than left to the column names, because
    ``claims_annuity`` names a benefit paid on a **living** contingency in
    ``LTC_JP_S`` and ``Annuity_JP_A``.  Here the name records the benefit's *form* — an
    annuity — and the trigger is the death of the insured, or the contractual 高度障害
    state carried inside the same decrement as its accelerated equivalent.  Nothing in
    this model is paid on survival, on disability as such, or on lapse.

    **There is no ``claims_death`` column, and the absence is a product fact.** This
    contract pays no lump sum on death at all: the claim *opens* an annuity stream
    rather than settling one, so the whole death benefit is ``claims_annuity``.  The two
    lump-sum kinds below are settlements of that same death claim under an optional
    module, not a second benefit.

    ``"ANNUITY"``
        the 遺族年金 / 高度障害年金 instalments falling due in month t,
        ``A x annuities_if(t)``, paid on the **death** of the insured (or the
        高度障害 equivalent).  This is the product's whole benefit in the base
        run, and it is the only line that continues after the policy term has
        ended.

    ``"COMMUTATION"``
        the 全部一括受取 lump sum where that module is on, ``commute_pp(t)``
        per commuting claim.  Zero in the base run.

    ``"LIVING_NEEDS"``
        the リビング・ニーズ特約 acceleration where that module is on.  Zero in the
        base run.

    ``"LAPSE"``
        zero, always.  There is no 解約返戻金 at any duration on the composite;
        the kind exists so the zero is stated rather than left to inference.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("ANNUITY", "COMMUTATION", "LIVING_NEEDS", "LAPSE"))
    if kind == "ANNUITY":
        return annuity_mth() * annuities_if(t)
    if kind == "COMMUTATION":
        return commute_pp(t) * pols_commute(t)
    if kind == "LIVING_NEEDS":
        return ln_benefit_pp(t) * pols_living_needs(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec D(t): the claim handling expense on the month's new claims **[std]**.

    ¥30,000 per claim, charged once when the claim arises however it is then settled.
    Kept out of :func:`expenses`, which is acquisition plus maintenance only, and separate
    from :func:`annuity_expenses`, which is charged per *instalment* rather than per claim.
    It is deducted explicitly in :func:`net_cf` and published as its own ``claim_expenses``
    column.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def annuity_expenses(t):
    """ea R(t): the administration expense of the instalments due in month t **[std]**.

    ¥200 per instalment paid, plus one payment for each claim settled instead by a lump
    sum.  A new item with no analogue on the protection chassis, which pays a lump sum
    and closes the file: this product pays up to 420 instalments over up to 35 years
    after the claim.  The level is a placeholder — ¥591.08 undiscounted per policy
    issued on the anchor cell against ¥443,313.69 of claims — but its *structure* is the
    point.  It is charged against the **ledger**, not against :func:`pols_if`, and it is
    the one expense that survives the end of the policy term: an implementation that
    attaches every expense to the in-force population charges nothing at all in months
    421-443, when instalments are still being paid.
    """
    return expense_annuity * (annuities_if(t)                        # noqa: F821
                              + pols_commute(t) + pols_living_needs(t))


def expenses(t):
    """E0 and e_m(t): acquisition and inflating maintenance expense in month t **[std]**.

    **Acquisition and maintenance only** — the library-wide meaning of ``expenses``.  The
    claim expense is :func:`claim_expenses` and the per-instalment annuity administration
    expense is :func:`annuity_expenses`; both are deducted separately in :func:`net_cf` and
    published as their own ``result_cf()`` columns.  The notes' worked-example *table*
    prints those two combined in a single "Claim + ann. exp" column, which is a
    presentational grouping in the notes and not a definition of ``expenses``.

    ¥15,000 per policy at issue, then ¥4,000 p.a. taken as ``4,000 / 12`` a month and
    inflating at 1.0% p.a., both at the start of the month and both on the in-force
    population.  Zero beyond ``term_m()``, where there is no in-force population left.

    Expense is heavy relative to this premium: ¥30,780 of annual premium carries ¥4,000
    of maintenance, and the five non-benefit lines total ¥120,768.70 against ¥461,030.83
    of premium on the anchor cell — 26.2%.  No Japanese public source supports any of
    these levels.
    """
    acq = expense_acq * pols_if(t) if t == 1 else 0.0                # noqa: F821
    return acq + (expense_maint / 12.0) * inflation_factor(t) * pols_if(t)  # noqa: F821


def comm_init_pp():
    """c0: the initial commission per policy issued **[std]**.

    50% of the first-year annualized premium, paid upfront at issue.  With the
    acquisition expense it is what produces the deep first-month new business strain in
    the worked example: -¥28,164.05 in month 1 against +¥2,203.68 in month 2.
    """
    return comm_init_rate * 12.0 * premium_mth_pp()                     # noqa: F821


def commissions(t):
    """Commission outgo in policy month t **[std]**.

    The initial commission at ``t = 1``, then 5% of premium income from month 13.  Both
    levels are chosen for the reference implementation; nothing about Japanese
    protection commission is published in the source set.
    """
    init = comm_init_pp() * pols_if(t) if t == 1 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 13 else 0.0      # noqa: F821
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less the annuity instalments, the annuity administration expense, the
    claim expense, maintenance and acquisition expense and commission.  The notes' own
    sign — they write ``+ = inflow`` — which is also the library-wide convention, so
    there is no outgo-positive ``liability_cf`` companion to publish.

    Note which population multiplies which term: **premiums, maintenance and commission
    carry ``pols_if``; the annuity instalments and the annuity administration expense
    carry ``annuities_if``**, and the two are disjoint.  Lapse contributes no term at
    all — it acts only through ``pols_if``, and ``claims(t, "LAPSE")`` is identically
    zero.
    """
    return (premiums(t) - claims(t) - claim_expenses(t)
            - annuity_expenses(t) - expenses(t) - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``l(t) + reinstatements(t+1) - l(t+1) - deaths - lapses - expiries``.  Expiries are
    non-zero only in month ``term_m()``, where the survivors neither die nor lapse:
    their cover runs out and they are paid nothing.  Without that term the last month
    of cover appears to lose lives with no cause.
    """
    return (pols_if(t) + pols_reinst(t + 1) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every month of cover.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call the same check across every model.
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol           # noqa: F821
               for t in range(1, term_m() + 1))


def check_annuity_ledger_resid(t):
    """The in-payment ledger residual in policy month t; zero everywhere.

    :func:`annuities_if` less an independent rebuild of the same figure — the streams
    ``s`` with ``s <= t <= pay_end(s)``, summed straight off the claim vector with no
    reference to the recursion.  A ledger decremented by mortality or lapse, or one
    whose streams end a month early, shows up here.
    """
    n, g = term_m(), guar_m()
    lo = 1 if t <= n else t - g + 1
    hi = min(t, n)
    direct = 0.0
    for s in range(max(1, lo), hi + 1):
        direct += annuities_open(s)
    return annuities_if(t) - direct


def check_annuity_ledger():
    """True when the in-payment ledger closes in every projected month.

    No argument, one bool over all t; :func:`check_annuity_ledger_resid` gives the
    signed residual of the month that failed.
    """
    return all(abs(check_annuity_ledger_resid(t)) <= roll_fwd_tol    # noqa: F821
               for t in range(1, proj_len() + 1))


def check_annuity_total_resid(t):
    """The cumulative-instalment residual at policy month t; zero everywhere.

    :func:`annuities_cum` less an independent count built from the claim vector and the
    contractual instalment schedule: each claim in month ``s`` contributes the number of
    its instalments falling at or before ``t``, ``min(t, pay_end(s)) - s + 1``.  At
    ``t = proj_len()`` this is the notes' identity
    ``sum over t of R(t) = sum over s of D(s) x n_pay(s)``.
    """
    n, g = term_m(), guar_m()
    built = 0.0
    for s in range(1, min(t, n) + 1):
        built += annuities_open(s) * (min(t, max(n, s + g - 1)) - s + 1)
    return annuities_cum(t) - built


def check_annuity_total():
    """True when the instalments due to date reconcile in every projected month."""
    return all(abs(check_annuity_total_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pay_count_resid(t):
    """The guarantee-arithmetic residual for a claim in month t; zero everywhere.

    ``pay_count(t) - (pay_end(t) - t + 1)``.  The two express the same contractual rule
    from opposite ends — how many instalments a claim makes, and when the last of them
    falls — and ``ends_at(m) = max(N, m + G - 1)`` is the whole guarantee mechanic in
    one expression.  An off-by-one in either is invisible in any total.
    """
    return float(pay_count(t) - (pay_end(t) - t + 1))


def check_pay_count():
    """True when the instalment count and the stream end date agree in every month."""
    return all(abs(check_pay_count_resid(t)) <= roll_fwd_tol         # noqa: F821
               for t in range(1, term_m() + 1))


def check_expired_cover_resid(t):
    """What the model still charges to the in-force population after expiry; zero.

    ``premiums(t) + expenses(t) + commissions(t) + pols_death(t)`` for ``t > N``, and
    zero by construction at or before ``N``.  Cover ends at the expiry date with
    nothing payable on survival, so every line carried on :func:`pols_if` must vanish
    there while the annuity instalments and their administration expense run on — the
    asymmetry this product exists to model.
    """
    if t <= term_m():
        return 0.0
    return premiums(t) + expenses(t) + commissions(t) + pols_death(t)


def check_expired_cover():
    """True when nothing is charged to the in-force population past the policy term."""
    return all(abs(check_expired_cover_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(term_m() + 1, proj_len() + 1))


def check_class_factor_norm_resid(t):
    """The rate-class normalization residual; the same at every t.

    The mix-weighted mean of the four **[std]** class factors, less 1.  生保標準生命表2018 is
    an **all-lives** basis, so a class split whose weighted mean is not 1.000 silently
    re-levels the whole table.  The illustrative mix
    ``0.25 x 0.70 + 0.35 x 0.90 + 0.10 x 1.05 + 0.30 x 1.35`` gives exactly 1.000; the
    mix is **[std]** and is used to check the normalization, not as a claim about the
    market.  The identity has no time dimension, so ``t`` is carried only for uniformity
    with the other ``check_*_resid`` cells.
    """
    tbl = data.rate_class_table()                                    # noqa: F821
    return float((tbl["class_factor"] * tbl["mix_weight"]).sum()
                 / tbl["mix_weight"].sum() - 1.0)


def check_class_factor_norm():
    """True when the mix-weighted mean of the rate class factors is 1.000."""
    return abs(check_class_factor_norm_resid(1)) <= roll_fwd_tol     # noqa: F821


def check_net_cf_resid(t):
    """The cash flow statement residual in policy month t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns re-added — premiums, less
    the four ``claims_*`` splits, the claim expense, the annuity administration expense,
    maintenance and acquisition expense and commission.  It is not a restatement of
    :func:`net_cf`: that cells subtracts the *total* :func:`claims`, while this rebuild
    sums the four columns the statement actually prints, so a benefit limb that is
    computed but never published — or one published twice — shows up here.  It is also
    what makes publishing a bare ``claims`` subtotal beside its own splits a defect
    rather than a convenience: the columns would then no longer add to ``net_cf``
    without knowing which of them to skip.
    """
    return (net_cf(t) - premiums(t)
            + claims(t, "ANNUITY") + claims(t, "COMMUTATION")
            + claims(t, "LIVING_NEEDS") + claims(t, "LAPSE")
            + claim_expenses(t) + annuity_expenses(t)
            + expenses(t) + commissions(t))


def check_net_cf():
    """True when the published cash flow statement adds to net_cf in every month.

    The library-wide name for this check, and the library-wide form: no argument, one
    bool over all t, with the signed residual of the month that failed at
    :func:`check_net_cf_resid`.
    """
    return all(abs(check_net_cf_resid(t)) <= cash_tol                # noqa: F821
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month in-force probability and the weight on the
    premium, maintenance and commission lines of the same row; ``annuities_if`` is the
    ledger and the weight on the two annuity lines.  **They are disjoint and must never
    be summed.**  ``net_cf`` carries the notes' own income-positive sign, and
    :func:`check_net_cf` re-adds the published columns to it.

    **``claims_annuity`` is a death benefit.**  The instalments are paid on the death of
    the insured, or on the contractual 高度障害 state treated as its accelerated
    equivalent — not on survival and not on disability as such.  The same column name
    carries a *living* benefit in ``LTC_JP_S`` and ``Annuity_JP_A``, so on this product
    the contingency is stated here: the name records the benefit's form, not its
    trigger.  **There is no ``claims_death`` column**, and that absence is a product
    fact rather than an omission — the contract pays no lump sum on death, so the whole
    death benefit is the annuity.  ``claims_lapse`` is likewise a column of zeros by
    product design — there is no 解約返戻金 at any duration — and is published rather than
    dropped.

    The table runs to ``proj_len()``, which is ``guar_m() - 1`` months longer than the
    policy term: the last rows carry annuity instalments and their administration
    expense alone.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "annuities_if": [annuities_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_commutation": [claims(t, "COMMUTATION") for t in ts],
            "claims_living_needs": [claims(t, "LIVING_NEEDS") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "annuity_expenses": [annuity_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of populations and decrement rates, indexed by policy month t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_reinst": [pols_reinst(t) for t in ts],
            "pols_payer": [pols_payer(t) for t in ts],
            "annuities_open": [annuities_open(t) for t in ts],
            "annuities_ended": [annuities_ended(t) for t in ts],
            "annuities_if": [annuities_if(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.8

sel_lapse_lambda = 0.0

sel_lapse_ref = 1.0

expense_acq = 15000.0

expense_maint = 4000.0

expense_claim = 30000.0

expense_annuity = 200.0

inflation_rate = 0.01

comm_init_rate = 0.5

comm_renewal_rate = 0.05

commute_rate = 0.0065

ln_take_up = 0.05

ln_cap = 30000000.0

ln_defer_m = 6

wop_inc_rate = 0.0006

wop_rec_rate = 0.1

reinst_rate = 0.15

reinst_lag_m = 6

reinst_window_m = 36

reinst_int_rate = 0.0065

roll_fwd_tol = 1e-10

cash_tol = 1e-06

pd = ("Module", "pandas")
