# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Term_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` is the **0-based** projection index and its unit is the **policy month**: ``t = 0``
is the first projected month and ``t = proj_len() - 1`` the last, so ``proj_len()`` is the
**number** of projected months and the frame is ``range(proj_len())``. The contractual
policy year is the 1-based label ``policy_year(t) = 1 + t // 12``, derived and never
indexed by, and ``duration(t) = t // 12`` is the count of completed policy years that every
contractual schedule in the product is quoted against. There is nothing after the last
month — no 満期保険金 (maturity benefit), no 解約返戻金 (*kaiyaku-henreikin*, surrender
value), no run-off and no tail state of any kind [S1][S8][S10][S14].

Where the horizon ends is a product question rather than a convention. A 歳満了
(*sai manryō*) contract ends at its stated age and never renews [S1], so
``proj_len() = 12 policy_term()``. A 年満了 (*nen manryō*) 更新型 contract renews
automatically at the end of every 保険期間 until it reaches the **renewal ceiling of
attained age 80** [S1][S2][S8], so ``proj_len() = 12 (renew_ceiling() - age_at_entry())``
and a ten-year term issued at 30 is projected for 600 months across five priced terms.
``contract_boundary = current_term`` truncates instead at the end of the term in force
at the valuation date.

.. rubric:: The monthly grid, and what it changes

Everything the composite guarantees is still quoted in years — the 保険期間, the renewal
ceiling, the lapse curve, the mortality table — so the monthly step does not make the
contract finer; it makes the *projection of it* finer, and four things move as a result.

**Rates convert, one-off proportions do not.** The mortality and lapse decrements are
annual rates and are taken to the month on the effective convention
``r_m = 1 - (1 - r)^(1/12)``, which is :func:`mort_rate_mth` and :func:`lapse_rate_mth`;
twelve of them compound back to the annual rate exactly. The renewal decline is **not** a
rate per unit time — it is the proportion of survivors who walk away when a 保険期間 ends —
so :func:`decline_rate` is applied unconverted in the single month the term expires.
Converting it would spread one decision over twelve months; annualizing the other two
would apply a year of decrement to a month of exposure.

**The premium is now paid when the contract says it is.** ``premium_mode`` was inert on
the annual grid, which annualized every mode into one start-of-year payment; here
:func:`prem_mode_months` and :func:`prem_due_pp` pay 月払 monthly, 半年払 every sixth month
and 年払 every twelfth. The rate cards this product is priced off are quoted monthly [S2],
so the monthly grid is also the grid the premium is *stated* on.

**One [std] approximation is retired rather than restated.** The annual model collected a
whole year of premium in advance from lives that might exit in month two, and offset that
against claims booked at the end of the year; the notes declared the pair matched and
warned against correcting either alone. Neither approximation survives here, so neither
offset is needed, and the undiscounted totals move accordingly — the anchor cell collects
¥457,507.04 of premium against the annual grid's ¥470,348.54, because it stops collecting
from lives that have already gone.

**The strain is where it actually falls.** Acquisition expense and initial commission are
one month's outgo against one month's premium, so ``t = 0`` is a far deeper hole than the
annual grid's first row and every later month is shallower. The total is the same money;
the shape is the one a cash flow statement is for.

What does **not** move is the survivorship at the anniversaries, and that is worth knowing
because it is the check that the conversion was done right. The effective convention makes
``(1 - q_m)^12 = (1 - q)`` and ``(1 - w_m)^12 = (1 - w)`` exactly, and the renewal decline
falls in the month a policy year ends either way, so ``pols_if(12 j)`` here equals the
annual model's ``pols_if(j)`` to floating-point: ``l(120) = 0.466683`` and
``l(600) = 0.026042``, the same two numbers the annual grid published. Every difference in
the cash flows is therefore a **timing** difference and never a difference in the decrement
basis — which is what makes the two runs comparable at all.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/term_life/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Term_JP_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Term_JP_S.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
prem_rate_file          data.prem_rate_table()          prem_rate_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind``
string, ``pols_if_at(t, timing)`` for the within-month in-force reads, and the annual /
``*_mth`` pair for a rate that is quoted per annum and applied per month. The technical
notes use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ============================
Notes symbol               Cells                           Meaning
=========================  ==============================  ============================
(row label)                model_point()                   The selected model point row
t                          (the index of result_cf)        Policy month, 0-based
floor(t/12)                duration(t)                     Completed policy years
y(t) = 1 + floor(t/12)     policy_year(t)                  Contractual policy year
x                          age_at_entry()                  契約年齢, 満年齢
x + floor(t/12)            age(t)                          Attained age in month t
(none)                     sex()                           Rating factor, M or F
(none)                     term_type()                     nen (renewable) or sai
n                          policy_term()                   保険期間, in years
12n                        term_months()                   保険期間, in months
w_r                        renew_ceiling()                 Attained age renewal stops
N                          horizon_ceiling()               Years from entry to w_r
t = 0..12N-1               proj_len()                      Number of projected months
(none)                     contract_boundary()             ceiling or current_term
k                          term_index(t)                   Term index, 1 in the first
x_k                        term_start_age(k)               Attained age at term k start
m_k                        term_len(k)                     Length of term k, truncated
SA                         sum_assured()                   保険金額, level
f                          policy_fee_m()                  Flat monthly element, 248
r(sex, x, m)               prem_rate_m(t)                  Rate per 5,000,000 of cover
qbar(x, m)                 mort_table_mean(x, m)           Mean table rate over m years
P_m(k)                     premium_mth_pp(t)               Monthly premium, whole yen
P_a(k)                     prem_pp(t)                      Annualized premium
(mode)                     prem_mode_months()              1, 6 or 12
(none)                     prem_due_pp(t)                  Premium falling due in month t
(table)                    mort_rate_at_age(x)             Table rate at an age
(table)                    mort_rate_base(t)               Table rate in month t, annual
(margin removal)           mort_be_factor                  Best-estimate factor, 0.80
lambda                     sel_lapse_lambda                Selective-lapsation loading
l_ref                      sel_lapse_ref                   Selective-lapsation reference
(none)                     sel_lapse_factor(t)             Mortality loading on stayers
q(t)                       mort_rate(t)                    Death and 高度障害, annual
q_m(t)                     mort_rate_mth(t)                The same, per month
w(t)                       lapse_rate(t)                   Ordinary lapse rate, annual
w_m(t)                     lapse_rate_mth(t)               The same, per month
d(t)                       decline_rate(t)                 Renewal decline, not a rate
d_0                        decline_base                    Flat decline rate, 15%
beta, d_max                decline_beta, decline_max       Decline elasticity module
l(t)                       pols_if(t)                      In force at start of month t
(within-month)             pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / ...
D(t)                       pols_death(t)                   Expected claims in month t
(none)                     pols_lapse(t)                   Ordinary lapses
(none)                     pols_decline(t)                 Renewal declines
lap(t)                     pols_lapse_pool(t)              Reinstatable population
rho                        reinstate_rate                  Reinstatement rate, annual
rho_m                      reinstate_rate_mth()            The same, per month
W                          reinstate_window                3 years [S1]
12W                        reinstate_window_m()            36 months
(none)                     pols_reinstate(t)               Reinstatements into l(t+1)
(none)                     pols_lapse_expire(t)            Pool leavers, window expired
(none)                     wop_waived_frac(t)              Fraction with premiums waived
inc_m, rec_m               wop_inc_rate_mth(), ...         Waiver chain, per month
(none)                     pols_payer(t)                   Policies paying premium
A                          ln_amount()                     Accelerated amount
i_ln                       ln_interest_rate                Six-month discount rate
a(t)                       ln_share(t)                     Acceleration take-up
(payout formula)           ln_payout_pp(t)                 A - interest - premiums
P x l                      premiums(t)                     Premium income
SA x D(t)                  claims(t, kind)                 Benefit outgo by kind
ec                         expense_claim                   Claim expense per claim
ec x D(t)                  claim_expenses(t)               Claim expense outgo
E0                         expense_acq                     Acquisition expense, 15,000
e_m(t)                     expenses(t)                     Acquisition + maintenance
c0                         comm_init_pp()                  Initial commission per policy
c_r                        comm_renewal_rate               Renewal commission rate, 5%
(footnote 4)               comm_new_term(t)                Commission at a 更新
(none)                     commissions(t)                  Commission outgo
CF(t)                      net_cf(t)                       Net cash flow, income positive
=========================  ==============================  ============================

Five names needed care.

The notes write ``q(t)`` for the decrement and ``qbar(x, m)`` for a mean of **table**
rates used by the premium scale. Those are different quantities on different bases — one
is best-estimate and one is not — so they get different names: :func:`mort_rate` is the
decrement, and :func:`mort_table_mean` averages :func:`mort_rate_at_age`, which reads the
table unadjusted. Feeding the best-estimate rate into the premium extension would move a
premium scale by an assumption that has nothing to do with pricing.

``P_m(k)`` and ``P_a(k)`` are indexed by the *term* in the notes and by the policy month
here. :func:`premium_mth_pp` and :func:`prem_pp` take ``t`` and resolve the term through
:func:`term_index`, which is what keeps every cash flow line indexed the same way. The
premium is nonetheless level within a 保険期間, and :func:`check_prem_level` asserts it.

``prem_pp`` is the annualized premium and is **not** the premium cash flow on this grid.
:func:`prem_due_pp` is: it is what the payment mode makes fall in month ``t``, and on a
年払 point it is zero in eleven months out of twelve. ``prem_pp`` survives because the
repricing rule, the commission scale and the renewal ladder are all quoted per annum, and
because a cells that meant "premium" in two senses would be worse than two cells.

``d(t)`` is spelled :func:`decline_rate`, not any variant of ``lapse``. It is a
different event at a different time from a different population — see below — and the
name is the first line of defence against the two being merged.

``lap(t)`` is spelled :func:`pols_lapse_pool` because it is a **stock**, the lapsed
lives still inside the three-year 復活 window, whereas :func:`pols_lapse` is the
month's **flow** into it.

.. rubric:: 更新 reprices; it does not re-issue

This is the structural difference from this repository's UK term model and the notes'
second-listed pitfall. At a renewal boundary the premium is recomputed on attained age
and on the scale then in force [S1][S4][S8][S12], and **nothing else resets**:

- ``pols_if`` is continuous across the boundary. There is no reset to 1.
- No acquisition expense and, in the base run, no commission is paid at a renewal
  (``comm_new_term_rate`` is 0). A 更新 is not new business: no new 保険証券 is issued
  and no 告知 is taken [S1][S4].
- The suicide and contestability clocks run from the original 責任開始日 and **do not**
  restart on 更新 [S1][S4][S7][S8]. Only 復活 restarts them [S1]. Neither clock is
  monetized in the base run, so neither is a cells; both are stated here because
  treating each renewed term as a fresh policy gets persistency, the strain pattern and
  both clocks wrong at once.

Truncation at the ceiling shortens the **term**, not the horizon: a renewal that would
carry the policy past attained age 80 renews as an 80歳満了 term instead [S1][S2][S8],
so an issue age of 35 has a final term of five years and the projection still ends
exactly at 80. That is :func:`term_len`, and model point 4 exercises it. Three other
market rules exist — shorten to expiry age 90, shorten or lengthen to a 指定年齢,
auto-convert to another product [S4][S7][S12] — and importing one changes the horizon.

.. rubric:: Renewal decline is not lapse

:func:`decline_rate` is non-zero **only** in a boundary month, and the exits it produces
are taken **after** mortality and after ordinary lapse — the notes' processing order,
steps 3, 4 and 5. On the anchor cell that month is ``t = 119``, the last month of the
first 保険期間, and there the decline removes 15% of the survivors against a month of
ordinary lapse of about 0.43% and a month of mortality of about 0.007%: better than
**97%** of that month's exits. The annual grid could only say 74%, because it compared one
renewal decision with a whole year of lapse. Folding the decline into :func:`lapse_rate`
makes the boundary invisible and mis-times most of the cohort's departure.

That is also the clearest thing the finer grid buys on this product. A renewal is an event
at a date, and on the monthly grid it is projected as one.

Two behaviours roll into the one rate, and a production model should separate them: the
policyholder who gives notice to decline, and the policyholder whose **first renewed
premium goes unpaid through grace**, in which case the renewal is treated as never
having happened and the contract terminates at the original expiry [S1][S7]. Only the
first is a decision. Both leave at the boundary, which is why one rate can carry them —
and why neither may appear in force at ``t + 1`` collecting the renewed premium. The
monthly grid makes the *second* of the two representable for the first time — grace is
about a month long [S1][S8], so a model that wanted to separate them now has a period
short enough to put the unpaid-premium exit in — but separating them would need a
take-up assumption the sources do not give, so the composite keeps one rate.

.. rubric:: One decrement, one benefit

生保標準生命表2018（死亡保険用）**includes 高度障害** (*kōdo shōgai*, severe disability)
inside its death rate [REG-R20], and the contract pays one sum assured and terminates on
whichever of the two events comes first [S1][S8]. :func:`mort_rate` is therefore the
combined death-and-高度障害 decrement, and there is no disability incidence anywhere in
this model. Adding one on top of the table double-counts the benefit — the notes'
first-listed pitfall.

The same reasoning governs the リビング・ニーズ特約 module below: an acceleration is a
*re-timing and re-pricing* of the death benefit, not a second claim, so
:func:`ln_share` splits the existing decrement rather than adding to it.

.. rubric:: Lapse pays nothing, and there is no 自動振替貸付

There is no 解約返戻金 at any duration on this composite
[S1][S4][S6][S8][S9][S10][S13][S14], so an ordinary lapse is a pure decrement: it moves
:func:`pols_if` and pays nothing. ``claims(t, "LAPSE")`` exists and returns zero, and
``result_cf()`` carries the zero column, because the notes list a non-zero lapse row as
a pitfall imported from models with cash surrender values — and because one carrier in
eight *does* write this design with a surrender value [S12], so the zero is asserted
from the composite's sources rather than assumed from the product class.

There is no 自動振替貸付 (*jidō furikae kashitsuke*, automatic premium loan), stated in
terms by one carrier [S7], and no collateral for a 契約者貸付 either — the second an
inference from the missing surrender value rather than a citation, since that carrier
points its policyholders at the 契約貸付制度 instead [S7] and the document appearing to rule
the policy loan out could not be extracted [S11]. Importing the APL mechanic
that ``WholeLife_JP_S`` carries would create a no-lapse cushion this contract does not
have. Grace, then 失効, then 復活-or-not is the whole persistency machinery here.

.. rubric:: The premium chassis, and where it stops being sourced

Japanese carriers publish rate cards, so the structure decomposes exactly [S2]::

    P_m(k) = f + r(sex, x_k, m_k) * SA / 5,000,000
    x_k    = x + (k - 1) * n
    m_k    = min(n, w_r - x_k)
    P_a(k) = 12 * P_m(k)

with ``f = 248`` per month and ``P_m`` rounded to the whole yen, which is the granularity
rate cards are published at [S2][S9][S10]. On this grid ``P_m`` is the cash flow and
``P_a`` the pricing quantity; the payment mode decides how many months' worth of ``P_m``
fall in a given month, through :func:`prem_due_pp`. Four cells are sourced — male ages 30, 40 and 50
and female age 30, all at a ten-year term. **Ages 60 and 70 are published by no
carrier**, and the anchor cell reaches both, so :func:`prem_rate_m` extends the scale off
the ``is_anchor`` row of the matching sex **[std]**::

    r(sex, x, m) = r_anchor * mort_table_mean(x, m) / mort_table_mean(x_a, m_a)

The extension back-casts to ¥958.9 at age 30 against the published ¥974 (-1.5%) and to
¥1,806.4 at age 40 against ¥1,823 (-0.9%), and gives ¥8,976 at 60 and ¥23,881 at 70.
Published cells are always used where they exist; the extension fills the gaps. That the
back-cast is close is reassuring about the *form* and says nothing about the *level* an
insurer will charge in 2056 — the notes rate it the third-largest lever on this cell.

The ¥248 is a **premium** component, not an expense recovery [S2]. It enters the model
only through :func:`premium_mth_pp`; crediting it against maintenance expense counts it
twice.

.. rubric:: Modules that are off in the base run

Eight of the notes' optional constructions are implemented and switched off, so that the
base run reproduces the worked example while the machinery stays visible and testable.
Three of them are model point columns, five are References:

- **リビング・ニーズ特約** (``living_needs``), a discounted acceleration of the death
  benefit. Off on the anchor cell; on for model points 6 and 9.
- **保険料の払込の免除** (``wop``), the premium waiver on an accident-caused 別表4 state.
  Off on the anchor cell; on for model point 7. 別表4 is a materially lower bar than the
  別表3 test for 高度障害 — loss of one eye, deafness in both ears, loss of one limb at
  the wrist or ankle [S1] — so the waiver incidence is **not** the 高度障害 incidence and
  :func:`wop_waived_frac` does not reuse :func:`mort_rate`.
- **復活** (``reinstatement``), the lapsed-but-reinstatable population and its three-year
  window [S1]. Off on the anchor cell; on for model point 8.
- **Contract boundary** (``contract_boundary``), ``current_term`` truncating at the end
  of the 保険期間 in force at the valuation date. ``ceiling`` on the anchor cell;
  ``current_term`` on model point 5. The two differ by more than a rounding — +¥47,254.64
  against -¥16,071.24 on the same cell — and the ESR standard-model treatment of a
  no-underwriting auto-renewal that would settle which is right is [unverified] here
  [REG-R16], so the model does not rule.
- **Selective lapsation**, ``q_eff = q (1 + lambda max(0, 1 - l(t)/l_ref))``, with
  ``sel_lapse_lambda = 0``. Stronger here than on a UK term policy: renewal takes **no
  告知** [S1][S4][S8][S12], so a life that has become uninsurable elsewhere renews while
  a healthy life re-shops, and the decision recurs four times on the anchor cell.
- **Renewal-decline elasticity**,
  ``d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta)``, with ``decline_beta = 0`` giving the
  flat 15%. The premium jump the elasticity would respond to accelerates: 1.87, then
  2.16, 2.28 and 2.66.
- **Age-basis shift**, ``q_x -> sqrt(q_x q_(x+1))``, with ``mort_age_shift = False``.
  契約年齢 is 満年齢 (*man-nenrei*, age last birthday) [S1] while 標準生命表2018 is built
  for 保険年齢 (*hoken-nenrei*, age nearest birthday) [REG-R20], so reading the table at
  満年齢 reads it half a year early and **understates** mortality. The base run accepts
  and states that bias; the shift module must move ``q`` **up**, not down — about 0.7% at
  age 30 and 4.2% at age 40.
- **Commission at 更新**, ``comm_new_term_rate = 0``. Set it to reproduce a scale paying
  first-year rates on each renewed term, which would change the sign of the cash flow at
  ``t = 120, 240, 360`` and ``480``. No document in the source set discloses a commission
  scale at all, so the zero is a choice and not a fact.

.. rubric:: Sign convention and premium timing

The notes' ``CF(t)`` is already **income positive** — they write ``+ = inflow`` — which
is the library-wide sign of :func:`net_cf`, so there is no outgo-positive
``liability_cf`` companion to publish: one stream, one sign, one name.

Premiums fall at the **start of the month** on the payment mode the contract carries, and
claims at the **end of the month** in which they arise. There is no half-year correction to
make and none to double-count: the annual grid needed one because it collected a whole
year of premium from lives that could exit in month two and booked their claims twelve
months late, and this grid does neither. The residual timing convention is within a single
month and is worth about a fortnight of interest on one month's cash flow, which this
model does not discount in any case.

.. rubric:: What is not modelled, and why

減額 (a reduction in sum assured) changes ``SA`` and ``P_a`` together, which is a model
point re-parameterization rather than a decrement **[std scope]** [S1][S8]. クーリング・
オフ is out of scope: the projection begins with cover in force and the eight-day
statutory population already out [REG-R36][S1]. The 復活 arrears, payable at 年6%
compound [S1], are not monetized: they settle premiums for years in which this projection
collected none, so recognizing them would need a missed-premium ledger the notes do not
specify **[std scope]**. And a **partial** acceleration under リビング・ニーズ特約 leaves
a reduced contract in force at a reduced premium [S1][S7] — a second transition, not one
benefit with two amounts — so :func:`ln_amount` raises rather than approximating it. It
cannot arise inside the composite's ¥1,000,000-¥30,000,000 envelope, where the
¥30,000,000 per-insured cap is *exactly reached* at the ceiling and never reduces a
single-contract payment: :func:`ln_cap_binds` tests that with a **strict** inequality.
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
    """The sex (M / F) of the insured, a rating factor of the premium scale [S2]."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_at_entry():
    """x: the 契約年齢 (issue age), 満年齢 with fractions discarded [S1].

    Age *last* birthday, not age nearest birthday.  生保標準生命表2018（死亡保険用）is
    built for a 保険年齢 basis [REG-R20], so reading it here reads it half a year early
    and understates mortality; ``mort_age_shift`` is the optional correction and the
    Space docstring states the direction.  The composite's envelope is 20-65 [S1][S2].
    """
    return int(model_point()["issue_age"])


def term_type():
    """``nen`` for a 年満了 更新型 contract, ``sai`` for a 歳満了 one [S1][S4][S7].

    The single most consequential model point attribute.  A 年満了 contract renews
    automatically at attained-age rates to the ceiling; a 歳満了 contract has one term,
    one premium and no repricing [S1], and applying the renewal machinery to it invents
    cover the contract does not have.
    """
    v = model_point()["term_type"]
    if v not in ("nen", "sai"):
        raise ValueError("invalid term_type: expected nen or sai")
    return v


def policy_term():
    """n: the 保険期間 in years — the *priced* term, not the projection horizon.

    Read from ``term_y`` on a 年満了 point and implied by ``expiry_age`` on a 歳満了 one
    [S1][S4].  On a 更新型 contract the horizon is :func:`horizon_ceiling`, which is
    longer, because the contract renews.
    """
    if term_type() == "nen":
        return int(model_point()["term_y"])
    return int(model_point()["expiry_age"]) - age_at_entry()


def renew_ceiling():
    """w_r: the attained age at which renewal stops, 80 on the composite [S1][S2][S8].

    Observed ceilings run 75 to 99 and 80 is the mode; behaviour *at* the ceiling varies
    more than the ceiling does, and the composite truncates into an 80歳満了 term rather
    than shortening to another expiry age or converting to another product [S4][S7][S12].
    """
    return int(model_point()["renew_ceiling"])


def sum_assured():
    """SA: the 保険金額, level for the whole term and unchanged through 更新.

    Paid on death **or** on a 別表3 高度障害 state, whichever becomes payable first;
    either terminates the contract and the other is then not paid [S1][S4][S8][S9][S12].
    The composite's envelope is ¥1,000,000-¥30,000,000 in ¥1,000,000 units [S2][S9][S13].
    """
    return float(model_point()["sum_assured"])


def premium_mode():
    """Monthly, semiannual or annual premium payment [S1].

    **Live on this grid.**  The annual-step predecessor annualized every mode into one
    start-of-year payment and carried this column inert; the monthly grid pays the premium
    when the contract says it falls, through :func:`prem_mode_months` and
    :func:`prem_due_pp`.  Model points 3 and 9 are 年払 and model point 7 半年払, so the
    difference is exercised by the shipped table rather than merely available.
    """
    return model_point()["premium_mode"]


def contract_boundary():
    """``ceiling`` or ``current_term``: how far the liability is projected.

    A Japanese 年満了 contract guarantees its premium only **within** the current
    保険期間; at each 更新 the insurer recomputes it on attained age and the scale then in
    force [S1][S4][S8][S12].  That is a unilateral repricing right exercisable every ten
    years — but a *scale-level* right, not an individual one, because renewal takes no
    告知 and no fresh underwriting, so the insurer cannot reprice a life for its own
    deterioration.  The ESR coefficients that would settle where the boundary falls were
    not retrieved [REG-R16], so the model does not rule: it projects to the ceiling in
    the base run **[std]** and carries the truncation as a switch.  Naming the convention
    is part of reporting the number.
    """
    v = model_point()["contract_boundary"]
    if v not in ("ceiling", "current_term"):
        raise ValueError("invalid contract_boundary")
    return v


def living_needs():
    """Whether the リビング・ニーズ特約 acceleration module is on; false in the base run."""
    return bool(model_point()["living_needs"])


def wop():
    """Whether the 保険料の払込の免除 module is on; false in the base run [S1][S8]."""
    return bool(model_point()["wop"])


def reinstatement():
    """Whether the 復活 module is on; false in the base run [S1].

    Off by default because ``reinstate_rate = 0.10`` is an **arbitrary placeholder** with a
    material persistency effect: no carrier in the source set publishes a reinstatement
    rate, no industry statistic in the set gives one, and no observed range can be quoted.
    A round tenth was chosen for the same reason as ``ln_take_up`` — so that no reader
    reads it as an estimate — and the only defence of it is that the module is off in the
    base run, leaving the worked example and every published figure independent of it.
    What *is* published, and is therefore not [std], is the window — three years, against
    arrears at 年6% compound [S1], on evidence of health [S8] — which is why
    ``reinstate_window`` is sourced while the rate beside it is not.
    """
    return bool(model_point()["reinstatement"])


def horizon_ceiling():
    """N: policy years from entry to the renewal ceiling.

    ``renew_ceiling() - age_at_entry()`` on a 年満了 point, because the contract renews
    until it gets there [S1][S2][S8]; the term itself on a 歳満了 point, which never
    renews [S1].
    """
    if term_type() == "nen":
        return renew_ceiling() - age_at_entry()
    return policy_term()


def proj_len():
    """The **number** of projected policy **months**: ``12 N``, or the current term's.

    The frame is ``range(proj_len())``, so ``t`` runs ``0 .. proj_len() - 1`` and
    ``len(result_cf()) == proj_len()``.  ``contract_boundary = current_term`` truncates at
    the end of the 保険期間 in force at the valuation date, which for a policy projected
    from issue is ``policy_term()`` years.  On a 歳満了 point the two coincide.

    Twelve rows to the policy year, so the anchor cell's fifty-year horizon is 600 rows
    and its boundary months are ``t = 119, 239, 359, 479`` — the last month of each
    保険期間 — rather than the annual grid's ``t = 9, 19, 29, 39``.
    """
    if contract_boundary() == "current_term":
        return 12 * min(horizon_ceiling(), policy_term())
    return 12 * horizon_ceiling()


def duration(t):
    """The number of **completed** policy years at the start of policy month t, ``t // 12``.

    The bridge between the monthly projection index and every contractual schedule in the
    product, all of which are quoted in years: the 保険期間 ``n``, the renewal ceiling, the
    ``policy_year`` column of ``lapse_table.csv`` and the attained age the mortality table
    is read at.  Months ``t = 0 .. 11`` are all duration 0, the first policy year.
    """
    return t // 12


def policy_year(t):
    """y(t): the contractual policy year containing month t, ``1 + t // 12``.

    The **1-based** label beside the 0-based month index — ``t = 0 .. 11`` is policy
    year 1 — and the key into ``lapse_table.csv``, whose ``policy_year`` column is 1-based
    for the same reason.  It is **derived, never indexed by**: every cells of this model
    is indexed by the 0-based month ``t``.
    """
    return 1 + duration(t)


def age(t):
    """x + floor(t / 12): the attained age (満年齢) at the start of policy month t.

    ``t`` is 0-based, so the 契約年齢 holds for the twelve months ``t = 0 .. 11`` and the
    contractual policy year is ``policy_year(t)``.  The table this feeds is graduated by
    整数年齢, so the age steps once a policy anniversary and not once a month.
    """
    return age_at_entry() + duration(t)


def term_index(t):
    """k: the term index — 1 in the original 保険期間, 2 after the first 更新, and so on.

    ``1 + floor(duration(t) / n)`` on a 年満了 point; always 1 on a 歳満了 one, which
    never renews [S1].  ``k`` is a contractual, **1-based** label and does not shift with
    the projection index.  The premium is a function of ``k`` and not of ``t``, which is
    the state variable a Japanese term model needs and a UK one does not.

    Going through :func:`duration` rather than through ``t`` is what keeps the term index
    a *contractual* quantity on the monthly grid: a 保険期間 is ``n`` years, so the index
    turns over at ``t = 12 n``, not at ``t = n``.
    """
    if term_type() != "nen":
        return 1
    return 1 + duration(t) // policy_term()


def term_months():
    """12 n: the length of a full 保険期間 in policy months.

    The renewal period on the projection grid.  A 保険期間 *ends* in the month
    ``t`` where ``(t + 1) % term_months() == 0`` — ``t = 119`` on the anchor cell — and
    that is the only month :func:`decline_rate` can be non-zero in.
    """
    return 12 * policy_term()


def term_start_age(k):
    """x_k: the attained age at which term k starts, ``x + (k - 1) n``."""
    if term_type() != "nen":
        return age_at_entry()
    return age_at_entry() + (k - 1) * policy_term()


def term_len(k):
    """m_k: the length of term k in years, ``min(n, w_r - x_k)``.

    Truncation at the ceiling shortens the **term**, not the horizon: a renewal that
    would carry the policy past attained age 80 renews as an 80歳満了 term instead
    [S1][S2][S8].  An issue age of 35 on a ten-year term therefore has a final term of
    five years and still ends exactly at 80.  The truncated term is priced over its own
    shorter length, which is why this feeds :func:`prem_rate_m`.
    """
    if term_type() != "nen":
        return policy_term()
    return min(policy_term(), renew_ceiling() - term_start_age(k))


def omega_age():
    """The highest attained age the shipped mortality table carries for this sex.

    Used only to keep the optional age-basis shift from reading past the end of the
    table; no shipped model point comes near it.
    """
    return int(data.mort_table().loc[sex()].index.max())             # noqa: F821


def mort_rate_at_age(x):
    """The **table** mortality rate at attained age x, unadjusted.

    A **[std]** proxy for 生保標準生命表2018（死亡保険用）, anchored on the rates the
    technical notes quote and attribute [REG-R18][R4]; see :mod:`~.Term_JP_S.Data`.  This
    is the valuation-table rate with its own margin still in it, and it includes 高度障害
    [REG-R20].  It is read directly by the premium scale and only through
    :func:`mort_rate_base` by the decrement.
    """
    return float(data.mort_table().loc[(sex(), int(x)), "mort_rate"])  # noqa: F821


def mort_table_mean(x, m):
    """qbar(x, m): the mean **table** rate over ages x .. x + m - 1.

    The shape parameter of the **[std]** premium extension.  Deliberately built on the
    table rate rather than on :func:`mort_rate`: a premium scale is not a best-estimate
    quantity, and feeding the best-estimate factor in would move a published rate card by
    an assumption that has nothing to do with pricing.
    """
    return sum(mort_rate_at_age(a) for a in range(int(x), int(x) + int(m))) / float(m)


def mort_rate_base(t):
    """The table rate at the attained age of policy month t, before the margin removal.

    An **annual** rate, read at ``age(t)`` and therefore level across the twelve months of
    a policy year; :func:`mort_rate_mth` turns it into the monthly decrement.

    Optionally shifted to ``sqrt(q_x q_(x+1))`` **[std]** when ``mort_age_shift`` is set,
    the correction for reading a 保険年齢 table [REG-R20] at 満年齢 [S1].  The shift raises
    the rate — about 0.7% at age 30 and 4.2% at age 40 — because the unshifted read is half
    a year early and understates.  Off in the base run.  The monthly grid does **not**
    dispose of it: the age still steps once a policy anniversary, so the half-year bias is
    the same one the annual grid carries, and interpolating ``q`` across the year would be
    a different and undocumented adjustment rather than this one.
    """
    q = mort_rate_at_age(age(t))
    if not mort_age_shift:                                           # noqa: F821
        return q
    return (q * mort_rate_at_age(min(age(t) + 1, omega_age()))) ** 0.5


def sel_lapse_factor(t):
    """The selective-lapsation loading on mortality in policy month t **[std]**.

    ``1 + lambda max(0, 1 - l(t)/l_ref)``.  Lapsers and decliners are healthier than
    stayers, so a block that has shed a large proportion of its lives carries impaired
    mortality on the remainder.  The mechanism is stronger here than on a UK term policy
    and one-directional: renewal takes **no 告知** [S1][S4][S8][S12], so a life that has
    become uninsurable elsewhere renews while a healthy life re-shops — and the decision
    recurs at every boundary.  Off in the base run (``sel_lapse_lambda = 0``), where it
    returns 1 in every month.  ``sel_lapse_ref = 1.0`` **[std]** is the cohort at issue, so
    the loading is driven by the proportion of the *original* block that has left.
    """
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, 1.0 - pols_if(t) / sel_lapse_ref)                       # noqa: F821


def mort_rate(t):
    """q(t): the **annual** best-estimate death-and-高度障害 rate in policy month t.

    ``mort_be_factor`` times the table rate, then the selective-lapsation loading, capped
    at 1.  This is the annual rate the table is stated on; :func:`mort_rate_mth` is the
    decrement actually applied to the month.  The pair follows the library's convention —
    ``mort_rate`` annual, ``mort_rate_mth`` monthly — so that a rate quoted in the notes
    can be compared with the cells that carries it without a conversion in between.

    **One** decrement carrying **one** sum assured: 生保標準生命表2018（死亡保険用）
    includes 高度障害 inside its death rate [REG-R20] and the contract pays once and
    terminates on whichever event comes first [S1][S8], so projecting the table rate for
    death and adding a 高度障害 incidence on top double-counts the benefit.

    ``mort_be_factor = 0.80`` **[std]** is this model's largest single lever and its least
    evidenced number.  The table's 作成概要 sizes its margin to hold the exceedance
    probability near 2σ, **capped at 130% of the unadjusted rate** [REG-R20], and removing
    a margin at its cap implies ``1/1.3 = 0.769``; against that the table already carries
    a forward improvement allowance and its base experience is 2008, 2009 and 2011.  0.80
    is a round central choice between the two.  No observed range can be given: no
    Japanese insurer publishes protection experience by duration.
    """
    return min(1.0, mort_be_factor * mort_rate_base(t)               # noqa: F821
               * sel_lapse_factor(t))


def mort_rate_mth(t):
    """q_m(t): the monthly death-and-高度障害 decrement, ``1 - (1 - q(t))^(1/12)`` **[std]**.

    The **effective** convention, not a nominal ``q / 12``: twelve months of it compound
    back to exactly the annual rate, which is what makes the monthly projection comparable
    with the annual one rather than merely finer.  At the anchor cell's attained age 30 it
    is about 4.534e-05 against an annual 0.000544, and a nominal ``q / 12`` would be
    4.533e-05 — the difference is small here and is not small at attained age 75, where
    the same choice moves the month's claims by 2%.

    This is the cells the roll-forward and the claim line use; :func:`mort_rate` above is
    the annual rate it is built from and is what the assumption tables and the notes quote.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate(t):
    """w(t): the **annual** ordinary lapse rate of the policy year containing month t **[std]**.

    9 / 7 / 6 / 5.5 / 5 percent, from ``lapse_table.csv``, which is keyed by the
    **contractual, 1-based** policy year and so is read at :func:`policy_year`; policy years
    beyond the table take its last row.  The **level** is anchored to the LIAJ's FY2024 whole-market
    解約・失効率 of 5.6% of opening in-force sum insured [REG-R31] — the simple mean over
    the first ten years is 5.75% and the in-force-weighted mean 5.94%, both a little above
    it, which is the expected direction for an early-duration protection curve against a
    figure dominated by long-duration in-force.  The **shape** is a convention with no
    Japanese published evidence behind it.

    A lapse pays nothing: there is no 解約返戻金 at any duration [S1][S4][S8].
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())), "lapse_rate"])


def lapse_rate_mth(t):
    """w_m(t): the monthly ordinary lapse rate, ``1 - (1 - w(t))^(1/12)`` **[std]**.

    The same effective convention as :func:`mort_rate_mth`, and it matters more here
    because the rates are two orders of magnitude larger: the anchor cell's first policy
    year is 9% a year, which is 0.783% a month effective against 0.750% nominal, a 4.4%
    difference in the month's exits.  Spreading an annual lapse rate over twelve months by
    division would shed 9.0% of the cohort over months that compound to 9.4%.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def decline_rate(t):
    """d(t): the renewal-decline rate — non-zero **only** in a boundary month **[std]**.

    A proportion of survivors leave at each 更新 rather than accept the repriced
    contract.  This decrement has no analogue in this repository's UK or U.S. term models
    and it is large: on the anchor cell the monthly premium moves from ¥974 to ¥1,823 at
    the first renewal, a factor of 1.87 [S2].  Against that, renewal is the **default** —
    it happens unless notice is given, and the notice period is two weeks [S1][S8], the
    shortest of the three observed and the design that maximizes renewal by inertia.  No
    carrier publishes a take-up or decline rate, so ``decline_base = 15%`` at every
    boundary.

    **It is not annualized and never converted to a monthly rate.**  It is a one-off
    proportion of the survivors of a single month — the month the 保険期間 ends — and not
    a rate per unit time, so the ``1 - (1 - r)^(1/12)`` treatment :func:`mort_rate_mth` and
    :func:`lapse_rate_mth` get would be a category error here.  It is the one decrement in
    this model the monthly grid leaves exactly as the annual grid had it, and that is the
    gain the finer grid buys: on the annual grid the decline was mixed into a year that
    also carried twelve months of ordinary lapse, and here it stands alone in its month.

    Non-zero where a 保険期間 *ends*, which on the 0-based monthly frame is
    ``(t + 1) mod 12n = 0`` — ``t = 119, 239, 359, 479`` on the anchor cell.  Zero on a
    歳満了 point, which never renews [S1], and zero in the final projected month
    ``t = proj_len() - 1``, where the cover ends at the ceiling rather than renewing.  The
    optional elasticity ``d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta)`` responds to the
    premium jump, which itself accelerates — 1.87, then 2.16, 2.28 and 2.66 across the
    anchor cell's four renewals; ``decline_beta = 0`` in the base run gives the flat rate.
    ``decline_max = 0.50`` **[std]** caps it: at ``beta = 1`` the largest jump reaches only
    40%, so the cap binds at no boundary, while at ``beta = 2`` it binds at every one.
    """
    if term_type() != "nen":
        return 0.0
    if (t + 1) % term_months() != 0 or t >= proj_len() - 1:
        return 0.0
    jump = prem_pp(t + 1) / prem_pp(t)
    return min(decline_max, decline_base * jump ** decline_beta)     # noqa: F821


def policy_fee_m():
    """f: the flat monthly element inside the premium, ¥248 [S2].

    A **premium** component, not an expense recovery.  It enters the model only through
    :func:`premium_mth_pp`; crediting it against :func:`expenses` counts it twice.  Read from the
    ``is_anchor`` row of the matching sex, which is where the decomposition of the
    published rate card is recorded.
    """
    return float(data.prem_anchor_table().loc[sex(), "policy_fee_m"])  # noqa: F821


def prem_rate_m(t):
    """r(sex, x_k, m_k): the marginal monthly rate per ¥5,000,000 of cover in month t.

    The published cell where one exists [S2] — male ages 30, 40 and 50 and female age 30,
    all at a ten-year term — and otherwise the **[std]** extension off the ``is_anchor``
    row of the matching sex::

        r(sex, x, m) = r_anchor * qbar(x, m) / qbar(x_a, m_a)

    Ages 60 and 70 are published by no carrier and the anchor cell reaches both, so the
    extension is unavoidable rather than optional.  It back-casts to ¥958.9 at age 30
    against the published ¥974 (-1.5%) and to ¥1,806.4 at age 40 against ¥1,823 (-0.9%),
    which is reassuring about the form of the scale and says nothing about the level an
    insurer will charge decades out.
    """
    k = term_index(t)
    x_k, m_k = term_start_age(k), term_len(k)
    tbl = data.prem_rate_table()                                     # noqa: F821
    key = (sex(), int(x_k), int(m_k))
    if key in tbl.index:
        return float(tbl.loc[key, "rate_per_5m"])
    anchor = data.prem_anchor_table().loc[sex()]                     # noqa: F821
    return (float(anchor["rate_per_5m"])
            * mort_table_mean(x_k, m_k)
            / mort_table_mean(int(anchor["issue_age"]), int(anchor["term_y"])))


def premium_mth_pp(t):
    """P_m: the monthly premium per policy in policy month t, in whole yen.

    ``f + r(sex, x_k, m_k) SA / 5,000,000``, rounded half up to the yen, which is the
    granularity published rate cards are quoted at [S2][S9][S10].  Level within the
    保険期間 and recomputed at each 更新 on attained age [S1][S4][S8][S12]; it is **not**
    guaranteed beyond the current term, which is what makes ``contract_boundary`` a
    question rather than a detail.

    On the anchor cell this reproduces the published ¥974 exactly: ``248 + 2 x 363``.
    It is the **rate card's own quantity**, and on the monthly grid it is also the cash
    flow: the annual grid had to annualize it to get a row, and this one does not.
    """
    return float(int(policy_fee_m()
                     + prem_rate_m(t) * sum_assured() / 5000000.0 + 0.5))


def prem_mode_months():
    """The number of months between premium payments: 1, 6 or 12 [S1].

    月払 pays every month, 半年払 every sixth and 年払 every twelfth, the first instalment
    of each falling at ``t = 0``.  **The mode is live on this grid and was inert on the
    annual one**, which annualized every mode into one start-of-year payment: the monthly
    grid is the first place in this model where a 年払 policy and a 月払 policy have
    different cash flows, and the difference is a timing difference of up to eleven months
    on every premium the contract collects.

    What does *not* change with the mode is the **amount** per year.  Mode discounts and
    前納 (advance payment) discounts are insurer-set and unpublished [S1][S7][S9][S14], so a
    年払 policy pays ``12 P_m`` once rather than a discounted annual premium **[std]**.
    """
    mode = premium_mode()
    if mode == "monthly":
        return 1
    if mode == "semiannual":
        return 6
    if mode == "annual":
        return 12
    raise ValueError("invalid premium_mode")


def prem_due_pp(t):
    """The premium falling due per paying policy at the start of policy month t.

    ``P_m`` every month on 月払; ``prem_mode_months()`` months' premium at the start of
    each payment period and nothing in between on 半年払 and 年払, the first falling at
    ``t = 0``.  Zero outside the projection.

    The payment clock runs from **issue**, not from the start of the current 保険期間, so a
    年払 policy renewing at ``t = 120`` pays its renewed premium in that same month because
    ``120 % 12 == 0``; that is true of every 保険期間 here because the terms are a whole
    number of years.  Where a truncated final term is not — it cannot be on this composite,
    since the ceiling is reached in whole years — the clock would still be the issue clock.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    p = prem_mode_months()
    return premium_mth_pp(t) * p if t % p == 0 else 0.0


def prem_pp(t):
    """P_a: the annualized gross premium per policy in policy month t, ``12 P_m``.

    **Not a cash flow on this grid** — :func:`prem_due_pp` is — but the pricing quantity the
    contract is repriced on and the base the commission scale is quoted against, so it is
    kept and published in ``result_pols()``.  On the anchor cell ``P_a = 12 x 974 = 11,688``.

    The annualization is **[std]** in the same sense as before: mode discounts are
    insurer-set and unpublished [S1][S7][S9][S14], so twelve months of premium is what a
    year of cover costs whatever the mode.
    """
    return 12.0 * premium_mth_pp(t)


def pols_if_init():
    """l(0) = 1: the model point is one policy, projected on an expected basis.

    Survivorship multiplies the per-policy cash flows; no aggregation logic is specified
    in the technical notes and none is implemented.
    """
    return 1.0


def pols_if(t):
    """l(t): the in-force probability at the **start** of policy month t.

    ``pols_if_init()`` at ``t = 0``, then the notes' roll-forward
    ``l(t+1) = l(t)(1 - q_m)(1 - w_m)(1 - d)`` plus any 復活 reinstatements.  This is the
    weight on every cash flow of the same ``result_cf()`` row.

    Note which rates appear in it: the two *rates per unit time* are the **monthly**
    :func:`mort_rate_mth` and :func:`lapse_rate_mth`, while the renewal decline is the
    one-off proportion :func:`decline_rate` and enters unconverted, in the single month the
    保険期間 ends.

    It is **continuous across a renewal boundary**: a 更新 reprices the contract, it does
    not re-issue it [S1][S4], so there is no reset to 1 and no new cohort.  Defined one
    month beyond the last projected month, at ``t = proj_len()``, where it is the survivors
    whose cover expires at the ceiling — on the anchor cell ``l(600)``, the fraction of the
    cohort still in force after fifty years and four repricings.  That is not a tail
    state: nothing is paid and nothing runs off, the cover simply ends [S1][S8][S10][S14].
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR") + pols_reinstate(t - 1)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy month t.

    The notes' processing order is death, then ordinary lapse, then the renewal decline —
    steps 3, 4 and 5 — and each timing reads the population the next decrement is taken
    from:

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number
        as :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before ordinary lapse.

    ``"BEF_DECLINE"``
        after ordinary lapse, before the renewal decline.  Equal to
        ``"AFT_DECR"`` in every month that is not a renewal boundary, which
        on a 更新型 point is 599 months out of 600.

    ``"AFT_DECR"``
        after all three decrements — the end-of-month state, before any 復活
        reinstatement is added back by :func:`pols_if`.

    Zero outside ``0 .. proj_len() - 1``: the cover has not started or has ended.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "BEF_DECLINE":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_DECLINE") * (1.0 - decline_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t) = l(t) q_m(t): expected death and 高度障害 claims in policy month t.

    One decrement covering both, because the table includes 高度障害 [REG-R20] and the
    contract pays once and terminates on either event [S1][S8].  The **monthly** rate: a
    month's claims are a twelfth of a year's cover, not a year's.
    """
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_lapse(t):
    """Ordinary lapses at the end of policy month t, from the survivors of mortality.

    Pays nothing — there is no 解約返戻金 at any duration [S1][S4][S8] — so this moves
    :func:`pols_if` and nothing else.  With the 復活 module on, these lives flow into
    :func:`pols_lapse_pool` rather than leaving for good.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_decline(t):
    """Renewal declines at the end of a boundary month, after ordinary lapse.

    Zero in every month that is not the last month of a 保険期間, and zero on a 歳満了
    point.  In the one month it applies it dwarfs the other two exits, which are a single
    month's worth apiece — that contrast is invisible on an annual grid, where the decline
    is compared with a whole year of lapse.  Nothing is paid.
    """
    return pols_if_at(t, "BEF_DECLINE") * decline_rate(t)


def reinstate_rate_eff():
    """rho: the 復活 reinstatement rate actually applied — zero unless the module is on.

    Keeping the effective rate in one cells is what lets :func:`pols_lapse_pool` and
    :func:`check_lapse_pool` carry the same ledger in both positions of the switch: with
    the module off the pool still tracks the lapsed-but-reinstatable population, and
    nothing is reinstated out of it.
    """
    return reinstate_rate if reinstatement() else 0.0                # noqa: F821


def reinstate_window_m():
    """W: the 復活 window in policy **months**, ``12 reinstate_window``.

    Three years [S1], which on this grid is 36 months.  The window is what
    :func:`pols_lapse_pool` tracks vintages over, and expressing it in months is what makes
    the pool age out on the anniversary of each life's own 失効 rather than at the end of
    the third *projection* year — the error the annual grid could not make and this one
    can.  ``reinstate_window`` stays a Reference in years because that is how the contract
    states it.
    """
    return 12 * reinstate_window                                     # noqa: F821


def pols_lapse_pool(t):
    """lap(t): lapsed lives still inside the three-year 復活 window at the start of month t.

    A **stock**, where :func:`pols_lapse` is the flow into it.  Tracked by vintage rather
    than as one blanket balance, because the window runs from each life's own 失効 and a
    single indicator would drop a whole cohort a month early or late::

        lap(t) = sum over s in [max(0, t - W), t - 1] of pols_lapse(s) (1 - rho_m)^(t - 1 - s)

    with ``W = reinstate_window_m() = 36`` months [S1].  The vintage index ``s`` is the same
    0-based month index as ``t``, so the sum is empty and ``lap(0) = 0``.  Renewal
    declines never enter it: a declined renewal is an expiry, not a 失効, and there is
    nothing to reinstate.

    The monthly grid carries **36 vintages** where the annual grid carried three, which is
    the point of tracking them: a life that lapses in month 5 leaves the window in month
    41, and no blanket balance indexed by projection year can say that.
    """
    rho = reinstate_rate_mth()
    return sum(pols_lapse(s) * (1.0 - rho) ** (t - 1 - s)
               for s in range(max(0, t - reinstate_window_m()), t))


def reinstate_rate_mth():
    """rho_m: the monthly reinstatement rate, ``1 - (1 - rho)^(1/12)`` **[std]**.

    ``reinstate_rate`` is quoted per annum like every other behavioural rate in this model,
    so it is converted on the same effective convention as :func:`mort_rate_mth` and
    :func:`lapse_rate_mth` rather than applied twelve times over.  Zero unless the module is
    on, which is what keeps the pool ledger closing in both positions of the switch.
    """
    return 1.0 - (1.0 - reinstate_rate_eff()) ** (1.0 / 12.0)


def pols_reinstate(t):
    """Reinstatements out of the pool into ``pols_if(t + 1)``: ``lap(t) rho_m``.

    復活 is available for three years against arrears at 年6% compound [S1], on evidence
    of health [S8].  The arrears are not monetized — see the Space docstring — so the
    module is a persistency effect only.  Reinstatement is the **only** event that
    restarts the suicide and contestability clocks [S1]; 更新 does not.  Zero in the base
    run.
    """
    return pols_lapse_pool(t) * reinstate_rate_mth()


def pols_lapse_expire(t):
    """Lives leaving the pool in month t because their three-year window has run out.

    The vintage that lapsed in month ``t - W``, net of the reinstatements taken out of it
    along the way, and zero while ``t < W``, when no vintage has aged out yet.  They are
    gone for good: after the window there is no 復活 [S1].
    """
    s = t - reinstate_window_m()
    if s < 0:
        return 0.0
    return pols_lapse(s) * (1.0 - reinstate_rate_mth()) ** reinstate_window_m()


def wop_inc_rate_mth():
    """The monthly 別表4 waiver incidence, ``1 - (1 - wop_inc_rate)^(1/12)`` **[std]**.

    ``wop_inc_rate`` is quoted per annum, so the two-state chain below — which now steps
    once a month rather than once a year — needs the monthly equivalent, on the same
    effective convention as every other rate in this model.  Zero unless the module is on.
    """
    return 1.0 - (1.0 - wop_inc_rate) ** (1.0 / 12.0)                # noqa: F821


def wop_rec_rate_mth():
    """The monthly recovery rate out of the waiver state **[std]**; zero in every run.

    ``1 - (1 - wop_rec_rate)^(1/12)``, and ``wop_rec_rate`` is zero **[std]** because a
    別表4 state is largely permanent — so this is zero too.  It exists rather than being
    inlined as a zero so that a user who sets a non-zero recovery rate gets it converted on
    the same convention as the incidence beside it instead of applied twelve times a year.
    """
    return 1.0 - (1.0 - wop_rec_rate) ** (1.0 / 12.0)                # noqa: F821


def wop_waived_frac(t):
    """The fraction of in-force policies with premiums waived at the start of month t.

    A two-state incidence chain **[std]**, ``u(t+1) = u(t)(1 - rec_m) + (1 - u(t)) inc_m``,
    stepping once a **month** and starting from ``u(0) = 0``.  The trigger is an **accident** on or after the
    責任開始時 producing a 別表4 state within 180 days [S1][S8][S12][S14].  別表4 is a
    materially lower bar than the 別表3 test for 高度障害 — loss of one eye, deafness in
    both ears, loss of one limb at the wrist or ankle [S1] — so this incidence is **not**
    the 高度障害 incidence and must not reuse :func:`mort_rate`.  It is also largely
    permanent, which is why ``wop_rec_rate`` is zero **[std]**.

    ``wop_inc_rate = 0.0008`` is an **arbitrary placeholder**: no retrieved document gives
    a 別表4 accident-disability incidence, the FSA and industry statistics in the source
    set do not publish waiver experience, and no observed range exists to quote.  It is
    not derived from :func:`mort_rate` and must not be — 別表4 is a different and much
    lower bar than the 別表3 test the mortality table's 高度障害 loading covers, so a
    number scaled off ``q`` would be a false derivation dressed as one.  The module is off
    in the base run; it is live only on model point 7, where the two-state chain and its
    effect on :func:`pols_payer` are what is being shown.

    While the waiver runs, premium income stops and cover continues [S1]; mortality and
    lapse are assumed independent of the waiver state **[std]**, which is what lets the
    waived population be carried as a fraction rather than as its own decrement.  Zero
    unless the module is on.
    """
    if not wop() or t <= 0:
        return 0.0
    u = wop_waived_frac(t - 1)
    return u * (1.0 - wop_rec_rate_mth()) + (1.0 - u) * wop_inc_rate_mth()


def pols_waived(t):
    """In-force policies whose premiums are waived in policy month t; zero in the base run."""
    return pols_if_at(t, "BEF_DECR") * wop_waived_frac(t)


def pols_payer(t):
    """In-force policies actually paying premium in policy month t.

    ``l(t)`` less the waived fraction.  Equal to :func:`pols_if` unless the
    保険料の払込の免除 module is on.
    """
    return pols_if_at(t, "BEF_DECR") - pols_waived(t)


def ln_cap_binds():
    """Whether the リビング・ニーズ特約 cap would **reduce** a single-contract payment.

    ``sum_assured() > ln_cap``, a **strict** inequality, and False on every shipped model
    point.  The ¥30,000,000 cap is per **insured**, aggregated across all of that
    insurer's contracts [S1][S7][S8][S12] — not per contract — so inside the composite's
    ¥1,000,000-¥30,000,000 envelope it is *exactly reached* at the ceiling and never
    reduces anything.  A model reporting the cap biting at ``SA = 30,000,000`` has a
    strict-versus-weak inequality error; a model applying it per contract has misread the
    clause.  Model point 9 sits exactly on the boundary and must come back False.
    """
    return bool(sum_assured() > ln_cap)                              # noqa: F821


def ln_amount():
    """A: the accelerated amount under リビング・ニーズ特約, ``min(SA, cap)``.

    Zero unless the module is on.  A **full** acceleration extinguishes the contract
    retroactively to the claim date, which is what this model implements; a **partial**
    one leaves a reduced contract in force at a reduced premium [S1][S7], which is a
    second transition and a model point re-parameterization rather than one benefit with
    two amounts.  It cannot arise inside the composite's envelope, so rather than
    approximate it :func:`ln_amount` rejects it by name.
    """
    if not living_needs():
        return 0.0
    if ln_cap_binds():
        raise ValueError(
            "partial acceleration is out of scope: sum_assured exceeds ln_cap, "
            "which leaves a reduced contract in force at a reduced premium")
    return sum_assured()


def ln_available(t):
    """Whether an acceleration can be claimed in policy month t.

    The rider is barred within **one year** of a non-renewable expiry [S1][S7][S8], which on
    this grid is the last twelve months of the projection, ``t >= proj_len() - 12`` — and
    only those, since every earlier expiry on a 更新型 point is followed by a renewal.  On a
    更新型 cell the bar therefore bites only in the ceiling term.

    The monthly grid states this bar as the contract states it.  The annual grid could only
    approximate a one-year bar by barring the whole final projected year, which is the same
    length by coincidence of the grid rather than by reading the clause; here the twelve
    barred months are the twelve months the contract names.
    """
    return living_needs() and t < proj_len() - 12


def ln_share(t):
    """a(t): the share of the month's decrement arriving as an acceleration **[std]**.

    Modelled as a split of the existing death-and-高度障害 decrement rather than as an
    additional incidence, which is the same ruling the notes make for 高度障害: an
    acceleration is a re-timing and re-pricing of the death benefit, not a second claim,
    and a separate incidence on top would double-count it.  The trigger is a **six**-month
    prognosis, not the twelve months of UK terminal illness cover [S1][S7].

    ``ln_take_up = 0.10`` is an **arbitrary placeholder**, and the honest defence of it is
    not a rationale but the switch: no retrieved document gives an acceleration take-up
    for any Japanese carrier, no observed range can be quoted, and nothing in the sources
    bounds it.  A round tenth was chosen because it is visibly round — a number no reader
    can mistake for an estimate.  The module is off in the base run, so the worked example
    and every figure this model publishes are independent of it; it is live only on model
    points 6 and 9, where what is being demonstrated is the *mechanics* of splitting the
    decrement and never the level of the split.
    """
    return ln_take_up if ln_available(t) else 0.0                    # noqa: F821


def ln_payout_pp(t):
    """The リビング・ニーズ特約 payment per accelerated claim in policy month t.

    ``A - A i_ln / 2 - six months' premiums on A`` [S1][S7][S8][S12]: the amount is
    **discounted**, unlike a UK terminal illness payment, which is the economic reason
    the rider can be offered without a separate premium.  The premium element is
    pro-rated by ``A / SA`` **[std]**, which is exact on the full acceleration this model
    implements.

    ``ln_interest_rate = 0.02`` is an **arbitrary placeholder** in the same sense.  The
    contract fixes the rate only by reference — the insurer's rate current at the claim
    [S1][S7] — and no retrieved document states a level or a range for it.  What can be
    said positively is the size of its effect and nothing more: the rate enters halved,
    so 2% removes exactly 1% of ``A`` and the whole parameter moves the payment by 0.5%
    for every percentage point.  The module is off in the base run, which is the only
    defence the number has.
    """
    a = ln_amount()
    if a <= 0.0:
        return 0.0
    return (a * (1.0 - ln_interest_rate * 0.5)                       # noqa: F821
            - 6.0 * premium_mth_pp(t) * a / sum_assured())


def premiums(t):
    """Premium income at the start of policy month t, an inflow.

    :func:`prem_due_pp` — the instalment the mode makes fall in this month — on the
    policies actually paying, :func:`pols_payer`, which is :func:`pols_if` unless the
    waiver module is on.

    **The grid retires a [std] the annual model had to carry.**  On an annual step the
    whole year's premium was collected in advance from lives that might exit in month two,
    and the notes offset that overstatement against an end-of-year claim timing that
    understated by about the same amount, declaring the pair matched and warning against a
    further half-year adjustment.  Here a policy that lapses in month two pays two months
    of premium and its claim falls in the month it arises, so neither approximation is
    made and neither needs an offset.  What remains is a within-month timing convention
    only: premium at the start of the month, claims at the end of it.
    """
    return prem_due_pp(t) * pols_payer(t)


def claims(t, kind=None):
    """Benefit outgo at the end of policy month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the sum assured on the month's death and 高度障害 claims,
        ``SA (1 - a(t)) D(t)``.  One decrement, one benefit: either event
        terminates the contract and the other is then not paid [S1][S8].

    ``"LIVING_NEEDS"``
        the discounted リビング・ニーズ特約 acceleration on the share ``a(t)``
        of the same decrement.  Zero in the base run.  It is a split of the
        death benefit, never an addition to it.

    ``"LAPSE"``
        zero, always.  There is no 解約返戻金 and no paid-up value at any
        duration [S1][S4][S6][S8][S9][S10][S13][S14]; the kind exists so that
        the zero is stated rather than left to inference.  One carrier in
        eight writes this design *with* a surrender value [S12], so the zero
        is a fact about the composite and not about the product class.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LIVING_NEEDS", "LAPSE"))
    if kind == "DEATH":
        return sum_assured() * (1.0 - ln_share(t)) * pols_death(t)
    if kind == "LIVING_NEEDS":
        return ln_payout_pp(t) * ln_share(t) * pols_death(t)
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def claim_expenses(t):
    """ec D(t): the claim handling expense on the month's claims **[std]**.

    ¥30,000 per claim, uninflated, on the whole decrement whether the benefit is paid as
    a death claim or accelerated.  Kept out of :func:`expenses` because the notes' worked
    example prints the two as separate columns.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in policy month t **[std]**, ``(1 + pi)^(y(t) - 1)``, pi = 1%.

    **Annual steps inside the monthly grid**: maintenance expense inflates once a policy
    year, at the anniversary, rather than once a month.  That is the library's convention
    (``IncomeTerm_JP_S`` does the same) and it is deliberate — a 1.0% p.a. assumption is an
    annual observation, and compounding it monthly would assert a within-year expense
    profile no source supports.  Policy year 1 therefore carries a factor of 1.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def expenses(t):
    """E0 and e_m(t): acquisition and inflating maintenance expense in month t **[std]**.

    ¥15,000 per policy at issue — the acquisition charge falls in the first row of the
    frame, ``t = 0`` — then ¥4,000 per policy per year taken as ``4,000 / 12`` a month and
    inflating at 1.0% a year, both at the start of the month.  No Japanese public source
    supplies either level.

    **No acquisition expense is charged at a 更新.** A renewal is not new business — no
    new 保険証券 is issued and no 告知 is taken [S1][S4] — so the ``t = 0`` charge is the
    only one, however many times the contract renews.  ¥4,000 a year against ¥11,688 of
    annualized premium is a third of the first term's load, which is why the notes rate the
    **[std]** 1.0% inflation rate a poor assumption to leave unexamined.
    """
    acq = expense_acq * pols_if_at(t, "BEF_DECR") if t == 0 else 0.0  # noqa: F821
    return acq + (expense_maint / 12.0 * inflation_factor(t)         # noqa: F821
                  * pols_if_at(t, "BEF_DECR"))


def comm_init_pp():
    """c0: initial commission per policy issued **[std]**, 50% of the first year's P_a.

    Paid upfront at issue.  With the acquisition expense it is ¥20,844 of outgo in the
    **first month** of the anchor cell against one month's ¥974 of premium on the same
    row, which is the deep new business strain the protection shape starts from — and it is
    deeper here than on the annual grid, where a whole year's ¥11,688 sat on the same row
    to meet it.  The strain is the same money either way; the monthly grid shows when it is
    actually unfunded.  No document in the source set discloses a Japanese commission scale,
    so both this and ``comm_renewal_rate`` are levels chosen for the reference implementation.
    """
    return comm_init_rate * prem_pp(0)                               # noqa: F821


def comm_new_term(t):
    """Commission paid at a 更新 **[std]**; zero in the base run.

    A renewal is not new business [S1][S4], so the base run pays no acquisition
    commission on a renewed term.  That is a choice and not a fact: no document in the set
    discloses a commission scale at all, and a scale paying first-year rates on each
    renewed term would change the **sign** of the cash flow at ``t = 120, 240, 360`` and
    ``480``.  Set ``comm_new_term_rate`` to switch it on; it then falls in the first
    **month** of each term after the first, which on the 0-based monthly frame is
    ``t = (k - 1) 12n``, and it is charged on the annualized premium ``P_a`` because that is
    the base a commission scale is quoted against.
    """
    if comm_new_term_rate <= 0.0 or term_index(t) <= 1:              # noqa: F821
        return 0.0
    if t != (term_index(t) - 1) * term_months():
        return 0.0
    return comm_new_term_rate * prem_pp(t) * pols_if_at(              # noqa: F821
        t, "BEF_DECR")


def commissions(t):
    """Commission outgo in policy month t **[std]**.

    The initial commission at ``t = 0``, then 5% of premium income from ``t = 12`` — the
    first month of policy year **2**, not the second month of policy year 1 — plus any
    commission at a 更新 (off in the base run).  The threshold is stated in months for the
    same reason the lapse table is read through :func:`policy_year`: the scale is quoted by
    policy year, and ``t >= 1`` on this grid would start renewal commission eleven months
    into the first-year commission's own period.

    No clawback on early lapse is modelled: the notes record that no Japanese clawback
    evidence exists in the source set, so a clawback rule would be an invention rather than
    a standardization of something observed.
    """
    init = comm_init_pp() * pols_if_at(t, "BEF_DECR") if t == 0 else 0.0
    renew = comm_renewal_rate * premiums(t) if t >= 12 else 0.0      # noqa: F821
    return init + renew + comm_new_term(t)


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less claims, claim expense, maintenance and acquisition expense and
    commission.  The notes' own sign — they write ``+ = inflow`` — which is also the
    library-wide convention, so there is no outgo-positive ``liability_cf`` companion to
    publish.

    Lapse and the renewal decline contribute no term: they act only through
    :func:`pols_if`.  The shape to expect is the protection shape seen a month at a time: a
    single very deep month at ``t = 0`` carrying the whole acquisition cost against one
    month's premium, thin positive months through the middle of each term, months turning
    **negative** as each 保険期間 runs out and the level premium falls behind the rising
    mortality cost, and a jump back into surplus in the first month of the repriced term.
    On a 年払 point the sawtooth is larger again, because eleven months in twelve carry no
    premium at all.
    """
    return (premiums(t) - claims(t) - claim_expenses(t)
            - expenses(t) - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``l(t) - l(t+1) - D(t) - lapses - declines + reinstatements``, the notes' identity
    with the 復活 module's inflow carried as its own term so that the same residual closes
    in both positions of the switch.  Non-zero would mean the decrements and the
    roll-forward have drifted apart — most easily by applying the renewal decline to the
    wrong population, since it is taken after mortality **and** after ordinary lapse.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_decline(t) + pols_reinstate(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the signed
    residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol           # noqa: F821
               for t in range(proj_len()))


def check_lapse_pool_resid(t):
    """The 復活 pool roll-forward residual in policy month t; zero everywhere.

    ``lap(t) - lap(t+1) - reinstatements - window expiries + lapses``.  The pool is a
    stock with one inflow (:func:`pols_lapse`) and two outflows (:func:`pols_reinstate`
    and :func:`pols_lapse_expire`), and the vintage bookkeeping of the 36-month window is
    exactly where an implementation drops or double-counts a cohort — twelve times more so
    on this grid than on the annual one, which had three vintages to keep straight.  Closes
    with the module off as well as on, since the pool is tracked either way.
    """
    return (pols_lapse_pool(t) - pols_lapse_pool(t + 1)
            - pols_reinstate(t) - pols_lapse_expire(t) + pols_lapse(t))


def check_lapse_pool():
    """True when the 復活 pool ledger closes in every projected policy month."""
    return all(abs(check_lapse_pool_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_pols_payer_resid(t):
    """The premium-paying population residual in policy month t; zero everywhere.

    ``l(t) - payers - waived``.  The waiver module carries the waived lives as a fraction
    of the in-force rather than as a separate decrement, which is only legitimate while
    the two partition ``l(t)`` exactly.
    """
    return pols_if_at(t, "BEF_DECR") - pols_payer(t) - pols_waived(t)


def check_pols_payer():
    """True when payers and waived lives partition the in-force in every projected month."""
    return all(abs(check_pols_payer_resid(t)) <= roll_fwd_tol        # noqa: F821
               for t in range(proj_len()))


def check_prem_level_resid(t):
    """The premium-level residual in policy month t; zero everywhere.

    ``P_a(t) - P_a(t-1)`` inside a 保険期間, and zero by definition in the first month of
    a term.  The premium is level within the term and changes **only** at a 更新
    [S1][S4][S8][S12]; a residual here means the premium is drifting with the policy year,
    which is what happens if the rate lookup is keyed on attained age rather than on the
    term's entry age.  On the monthly grid that failure mode is the more likely of the two,
    because ``age(t)`` now steps eleven times inside a term where the premium does not move
    at all — so this check is doing more work here than it did on the annual grid.
    """
    if t <= 0 or term_index(t) != term_index(t - 1):
        return 0.0
    return prem_pp(t) - prem_pp(t - 1)


def check_prem_level():
    """True when the premium is level within every 保険期間 of the projection.

    Note that it checks ``prem_pp``, the annualized pricing quantity, and not
    :func:`prem_due_pp`: on a 半年払 or 年払 point the amount *falling due* is zero in most
    months by design, and a level-premium check over that series would be asserting the
    payment mode rather than the repricing rule.
    """
    return all(abs(check_prem_level_resid(t)) <= roll_fwd_tol      # noqa: F821
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The published cash flow statement's ledger residual in policy month t; zero.

    :func:`net_cf` less the sum of the **columns of** ``result_cf()``, so a reader adding
    up the printed statement gets the printed total.  It is the check that catches a
    benefit kind that exists in :func:`claims` but was never given a column — which would
    leave the statement silently short of outgo it is charging.
    """
    row = result_cf().loc[t]
    return float(row["net_cf"] - (
        row["premiums"] - row["claims_death"] - row["claims_living_needs"]
        - row["claims_lapse"] - row["claim_expenses"] - row["expenses"]
        - row["commissions"]))


def check_net_cf():
    """True when the published cash flow statement adds up in every projected month.

    Tested against ``cash_tol``, not the ``roll_fwd_tol`` the four decrement checks use.
    The wider tolerance is a property of what is compared: the other checks close an
    identity between cells evaluated in one expression, where the residual is exact to a
    unit or two in the last place of a count near 1.0, while this one re-reads yen
    amounts of order 1e5 back out of the ``result_cf()`` DataFrame, so the round trip
    through column construction leaves float64 rounding of order 1e-11 in absolute yen.
    ``cash_tol = 1e-8`` is well above that noise and far below one yen, which is the
    smallest error a reader adding up the printed statement could observe.
    """
    return all(abs(check_net_cf_resid(t)) <= cash_tol                # noqa: F821
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, indexed by the 0-based policy **month** ``t``.

    The frame runs ``t = 0 .. proj_len() - 1``, so it has ``proj_len()`` rows — 600 on the
    anchor cell, twelve to the policy year.  ``pols_if`` is the start-of-month count, which
    is the weight applied to every cash flow on the same row.  ``net_cf`` carries the notes'
    own income-positive sign.  ``claims_lapse`` is a column of zeros by product design —
    there is no 解約返戻金 — and is published rather than dropped; see the Space docstring.

    To read it by policy year, group by ``duration``: ``df.groupby(df.index // 12).sum()``
    reproduces the annual statement, with the one difference that matters — premium and
    claims are now weighted by the population of each month rather than of each year.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_living_needs": [claims(t, "LIVING_NEEDS") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts, decrement rates and the premium, indexed by month t.

    The renewal machinery is only legible next to the decrements it drives, so
    ``term_index`` and ``prem_pp`` are printed here with ``decline_rate``: a boundary month
    is the row where the decline rate is non-zero and the premium changes on the next row.

    Both the annual rates and the monthly decrements are published, because a reader
    holding the notes needs the first and a reader checking the roll-forward needs the
    second: ``mort_rate`` and ``lapse_rate`` are the annual rates the assumption tables are
    stated on, ``mort_rate_mth`` and ``lapse_rate_mth`` the rates actually applied to the
    month.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_decline": [pols_decline(t) for t in ts],
            "pols_reinstate": [pols_reinstate(t) for t in ts],
            "pols_lapse_pool": [pols_lapse_pool(t) for t in ts],
            "pols_payer": [pols_payer(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "decline_rate": [decline_rate(t) for t in ts],
            "term_index": [term_index(t) for t in ts],
            "prem_pp": [prem_pp(t) for t in ts],
            "prem_due_pp": [prem_due_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.8

mort_age_shift = False

sel_lapse_lambda = 0.0

sel_lapse_ref = 1.0

decline_base = 0.15

decline_beta = 0.0

decline_max = 0.5

expense_acq = 15000.0

expense_maint = 4000.0

expense_claim = 30000.0

inflation_rate = 0.01

comm_init_rate = 0.5

comm_renewal_rate = 0.05

comm_new_term_rate = 0.0

ln_cap = 30000000.0

ln_interest_rate = 0.02

ln_take_up = 0.1

wop_inc_rate = 0.0008

wop_rec_rate = 0.0

reinstate_rate = 0.1

reinstate_window = 3

roll_fwd_tol = 1e-12

cash_tol = 1e-8

pd = ("Module", "pandas")
