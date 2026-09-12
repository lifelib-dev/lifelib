# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Endowment_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's 養老保険 anchor cell
    >>> Projection[2].result_cf()          # its 学資保険 cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months and is 0-based**: ``t = 0`` is the first policy month and
``t = proj_len() - 1 = 12 policy_term() - 1`` the last, so ``proj_len()`` is the *number*
of projected months and the frame is ``range(proj_len())``. The contractual policy year is
the 1-based label ``policy_year(t) = 1 + t // 12``, and ``duration(t) = t // 12`` is the
count of completed policy years.

A **second index** runs beside it, and it is still in years. ``k`` counts
**anniversaries**, ``k = 0`` at issue, so month ``t`` opens inside the policy year running
from anniversary ``duration(t)`` to ``duration(t) + 1``. The per-policy value construction
is indexed by ``k`` and not by ``t`` — :func:`pol_val_pp`, :func:`pol_val_pre_pp`,
:func:`surr_charge_pp`, :func:`surr_val_pp`, :func:`cv_pp`, :func:`reserve_pp`,
:func:`benefit_pct`, :func:`benefit_pct_cum`, :func:`prem_cum_pp`, :func:`loan_pp` and
:func:`edu_epv` — because it is a value *at a point in time* rather than a flow *during a
period*: ``SC(0)`` is the acquisition deduction at issue and ``W(n) = S`` is the maturity
value. **None of its numbers moved when ``t`` became a month**, and ``result_val()`` is
indexed by ``k`` rather than by ``t`` so that the two frames cannot be confused.

A benefit falling **between** anniversaries reads the interpolating companions instead —
:func:`pol_val_at_m`, :func:`pol_val_pre_at_m`, :func:`surr_charge_at_m`, :func:`cv_at_m`
and :func:`prem_cum_pp_m` — each of which reproduces its annual original at every
anniversary.

There is nothing after the term. Every state closes at the end of the last month
``t = 12n - 1``, whose closing instant is the anniversary ``n``:
``pols_if(12n) = pols_if_pay(12n) = pols_wv(12n) = 0``, and the closing cash flow is a
**certain** payment of the sum assured to the survivors rather than a decrement.

.. rubric:: The monthly grid: what moved and what did not

The contract is quoted in years and valued at anniversaries, so the monthly step is finer
than the guarantees rather than finer than the product.

**Annual, because the contract is.** The value construction — :func:`endow_epv`,
:func:`annuity_due`, :func:`edu_epv`, :func:`prem_net_level_pp`, :func:`pol_val_pp`,
:func:`reserve_pp` — is built from annual actuarial functions, and
:func:`check_pol_val_roll_fwd` and :func:`check_pol_val_terminal` roll and close it at
anniversaries. The **staged 学資金 grid** is a list of anniversaries by construction. The
**loan balances** compound once a year, because the rate is a 年利 capitalised at the
契約応当日. And a **premium default** is the failure to pay one premium on one date, so
:func:`default_rate` is applied once per premium and never spread.

**Monthly, because the experience is.** Both mortality decrements — the 被保険者's and the
契約者's — and voluntary surrender are rates per unit time and are taken to the month on
the effective convention ``r_m = 1 - (1 - r)^(1/12)``, so twelve of them compound back to
the annual rate exactly. Maintenance expense is a twelfth a month, inflating once a policy
year. The **premium**, being 年払, now falls in one month out of twelve. And every payment
that is a payment **on a date** — each staged 学資金, the maturity benefit — now falls in
the single month whose end is that date, instead of being attributed to a year.

**One convention is new and one carve-out shrinks.** The new convention is the linear
interpolation of the policy value between anniversaries **[std]**, which is what a
surrender or a death between two of them is settled on; it interpolates from the value
*after* the staged benefit at one anniversary to the value *before* the one at the next,
which is the curve the contract actually traces. The carve-out is :func:`lapse_rate`'s
suppression of surrender in the final period: the annual grid had to suppress it for the
whole last policy year to keep the maturity payment from being double-counted, and here
only the final **month** is suppressed.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/endowment/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Endowment_JP_S.Data`, reached here through the ``data`` Reference:

========================  ====================================  ==========================
Reference                 Cells                                 File
========================  ====================================  ==========================
model_point_file          data.model_point_table()              model_point_table.csv
mort_table_file           data.mort_table()                     mort_table.csv
lapse_table_file          data.lapse_table()                    lapse_table.csv
benefit_schedule_file     data.benefit_schedule_table()         benefit_schedule_table.csv
========================  ====================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string, ``pols_if_pay_at(t, timing)`` for the within-month
in-force reads, and the annual / ``*_mth`` pair for a rate quoted per annum and applied
per month. The technical notes use compact actuarial symbols instead. ``t`` in the mapping
below is the 0-based **month** index, ``u`` an elapsed month and ``k`` the anniversary:

=========================  ===============================  ===============================
Notes symbol               Cells                            Meaning
=========================  ===============================  ===============================
cell                       cell()                           endowment or education
(none)                     model_point()                    The model point as a Series
x                          issue_age()                      契約年齢 of the 被保険者
y                          ph_issue_age()                   契約年齢 of the 契約者
x + floor(t/12)            age(t)                           Attained age of the 被保険者
y + floor(t/12)            age_ph(t)                        Attained age of the 契約者
floor(t/12)                duration(t)                      Completed policy years
y(t)                       policy_year(t)                   Contractual policy year
n                          policy_term(), proj_years()      保険期間 in years, the span of k
m                          prem_term()                      保険料払込期間 in years
12m                        prem_period_months()                  払込満了, in policy months
t = 0..12n-1               proj_len()                       Number of policy months, = 12n
S                          sum_assured()                    基準保険金額
P                          premium_pp()                     Level annual premium
P x min(k, m)              prem_cum_pp(k)                   Cumulative premiums by anniv. k
(same, by month)           prem_cum_pp_m(u)                 Cumulative premiums by month u
(table)                    mort_rate_at_age(sx, z)          Raw table rate, sex and age
q(t)                       mort_rate(t)                     被保険者 rate, annual
q_m(t)                     mort_rate_mth(t)                 The same, per month
q_p(t)                     mort_rate_ph(t)                  契約者 rate, annual; 0 from 12m
q_p,m(t)                   mort_rate_ph_mth(t)              The same, per month
mort_be_factor             mort_be_factor()                 被保険者 mortality multiplier
wv_load                    wv_load()                        契約者 mortality multiplier
wv_frac                    wv_frac()                        Fraction of 契約者 deaths waived
wv_lapse_mult              wv_lapse_mult()                  Surrender multiplier when waived
(table)                    lapse_rate_base(t)               Table surrender rate
(dynamic form)             dyn_lapse_factor(t)              Value-to-premium multiplier
w(t)                       lapse_rate(t)                    Surrender rate, annual
w_m(t)                     lapse_rate_mth(t)                The same, per month
u(t)                       default_rate(t)                  Premium-default rate (APL)
g(k)                       benefit_pct(k)                   Staged 学資金 at anniversary k
G(k)                       benefit_pct_cum(k)               Cumulative staged fraction to k
(schedule)                 benefit_schedule()               The whole grid as a dict
k p z                      surv_prob(z, k)                  Table survival probability
A(z, k)                    endow_epv(z, k, i)               Endowment assurance EPV of 1
a-due(z, k)                annuity_due(z, k, i)             Annuity-due of 1
EPV(k)                     edu_epv(k, i)                    Survival-benefit EPV, 学資 cell
pi, pi_g                   prem_net_level_pp()              Net level premium on i_cv
(solved rate)              implied_rate()                   Rate at which net = gross
W(k)                       pol_val_pp(k)                    保険料積立金 after any staged benefit
W at month u               pol_val_at_m(u)                  The same, interpolated [std]
Wb(k)                      pol_val_pre_pp(k)                The same value before it
Wb at month u              pol_val_pre_at_m(u)              The same, interpolated [std]
(EPV limb)                 pol_val_db_pp(k)                 Death benefit inside the EPV
SC(k)                      surr_charge_pp(k)                Acquisition deduction
SC at month u              surr_charge_at_m(u)              The same, at elapsed month u
V(k)                       surr_val_pp(k)                   Ordinary surrender value
CV(k)                      cv_pp(k)                         Payable 解約返戻金
CV at month u              cv_at_m(u)                       The same, at elapsed month u
(reserve)                  reserve_pp(k)                    平準純保険料式 reserve on i_std
DB(t)                      death_ben_pp(t)                  Death benefit for a death in t
L(k)                       loan_pp(k)                       Loan and APL principal plus interest
(advance)                  apl_advance_pp(t)                APL advance made in month t
l(t)                       pols_if(t)                       In force, total
l_p(t)                     pols_if_pay(t)                   In force, premium-paying state
h(t)                       pols_wv(t)                       In force, waived state
l_p_after(t)               pols_if_pay_at(t, timing)        BEF_DECR / BEF_LAPSE / AFT_DECR
h_after(t)                 pols_wv_at(t, timing)            BEF_DECR / BEF_LAPSE / AFT_DECR
l_after(t)                 pols_if_at(t, timing)            BEF_DECR / BEF_LAPSE / AFT_DECR
D(t)                       pols_death(t)                    Expected 被保険者 deaths
Dp(t)                      pols_ph_decr(t)                  Expected 契約者 decrements
wv_frac x Dp(t)            pols_waived(t)                   Transitions into the waived state
(1 - wv_frac) x Dp(t)      pols_ph_term(t)                  Terminations, waiver refused
R(t)                       pols_surv(t)                     In force at the end of month t
Sr(t)                      pols_lapse(t)                    Expected surrenders in month t
R                          pols_maturity(t)                 Survivors who mature, final month
P x l_p(t)                 premiums(t)                      Premium income, once a year
DB(t) x D(t) etc.          claims(t, kind)                  Benefit outgo by kind
ec x D(t)                  claim_expenses(t)                Claim expense outgo
e_m(t)                     maint_expenses(t)                Maintenance expense, per month
(none)                     inflation_factor(t)              Expense inflation factor
E0                         acq_expenses(t)                  Acquisition expense
E0 + e(t)                  expenses(t)                      Acquisition plus maintenance
c0, c_r                    commissions(t)                   Commission outgo
CF(t)                      net_cf(t)                        Net cash flow, income positive
rho                        henreiritsu()                    返戻率, the contractual ratio
=========================  ===============================  ===============================

Six names needed care.

The notes' ``W(k)`` and ``Wb(k)`` differ only on the education cell, where a staged
benefit falls due at anniversary ``k``: ``Wb`` is the value **before** that payment and
``W`` the value after it, which is the sourced fact that each 祝金 reduces the surrender
value.
:func:`pol_val_pre_pp` and :func:`pol_val_pp` keep them apart because the two feed
different things — the death benefit and the refused-waiver termination read ``Wb``, the
surrender value reads ``W`` — and a model that pays the staged benefit *beside* the value
rather than out of it inflates every later surrender.

``CV`` and ``V`` are the same series on this product. There is no 低解約返戻金型
(*tei-kaiyaku-henreikin-gata*, suppressed-surrender-value) form of either cell in any
retrieved document, so there is no suppression multiplier, no step at 払込満了 and no surrender
spike; :func:`surr_val_pp` and :func:`cv_pp` are both published anyway, so that the
absence of the multiplier is stated rather than left to inference.

Every ``*_at_m`` cells is the **monthly reading of an annual contractual quantity**, and
the suffix is the warning: ``cv_pp(k)`` is the 解約返戻金 the contract defines at an
anniversary, and ``cv_at_m(u)`` is what this model pays someone who surrenders between
two. They agree at every anniversary by construction.

``mort_rate`` is the projection decrement and carries :func:`mort_be_factor`; the cash-value
construction reads :func:`mort_rate_at_age` directly, unadjusted. The policy value is a
contractual quantity on the pricing basis, so a best-estimate adjustment to the
projection must not move it — and that is testable, because model point 4 carries
``mort_be_factor = 1.25`` and its policy value is identical to model point 2's.

:func:`pols_maturity` has no symbol of its own in the notes, which write the closing
payment as ``S x R``. It is named so that the in-force roll-forward closes in the
final month ``t = 12n - 1``, where the survivors neither die nor surrender: they mature.
:func:`check_pols_roll_fwd` asserts the closure, and summing the residual over ``t``
gives the notes' own identity, that every policy leaves by exactly one route.

:func:`pols_if` is the **total** in force, ``l(t) = l_p(t) + h(t)``, and it is the weight
on that ``result_cf()`` row — the library-wide meaning, and what the death, staged and
maturity benefits and the maintenance expense all run on. The premium-paying subset is
:func:`pols_if_pay`, and only the premium and the renewal commission read it. The two
coincide on the endowment cell, which has no waiver, so a model that published only the
paying state would look correct there and understate the education cell's benefits by the
whole of its waived cohort. All three are published as columns, so the identity
``pols_if = pols_if_pay + pols_wv`` can be read off the statement.

.. rubric:: Two lives, two decrements, one policy

The waiver runs on the **契約者's** mortality at ``y + duration(t)``; every benefit runs on
the **被保険者's** at ``x + duration(t)``. Reading one table at one age for both is the most
likely implementation error on the education cell — and on the endowment cell the two ages
coincide, so it would not show there. Both decrements are converted to the month the same
way, because both are rates on lives.

``q_p(t) = 0`` from the month ``12m`` on is a modelling ruling, not an approximation. Every waiver
trigger in the retrieved 約款 is conditional on the event falling *during* 保険料払込期間, and
the termination-without-waiver path is the failure mode of that same provision. After
払込満了 there is no premium to waive, so the composite treats the contract as continuing
through the 契約者's death by succession and drops the second decrement entirely. On the
education anchor cell that covers five years of a twenty-two-year term — the years in
which most of the receipts fall — and carrying the decrement through them would
terminate policies the contract does not terminate.

The waiver itself produces **no outgo line at all**. What it produces is the absence of
premium income, which is why omitting it would leave every claim column unchanged, and
why booking a "waiver benefit" double-counts. Premiums on a waived policy are
**deemed paid**: :func:`prem_cum_pp` keeps growing on a policy that pays nothing, because
the contract provides that each future premium is treated as paid on its 契約応当日, and
the same wording is why :func:`cv_pp` is identical in both states rather than two series.

.. rubric:: The staged schedule is data

:func:`benefit_schedule` reads the whole grid from a table keyed by ``schedule_id``, and
:func:`benefit_pct` is a lookup into it. Model point 3 runs the degenerate ``J`` variant
— one payment of 100%, then maturity — without touching a formula, which is the sharpest
test that the grid really is data. ``schedule_id = "none"`` on the endowment cell is a
product fact and not a missing value: the survival benefit there is a single payment at
anniversary ``n`` and there is no staged schedule at all.

The staged benefit is **not a claim and not a decrement**. It is paid on survival at a
fixed anniversary to a policy still in force, in **both** states, and it terminates
nothing. Weighting it by a decrement rate, or paying it only from the premium-paying
state, understates it.

.. rubric:: Modules that are off in the base run

Five of the notes' optional constructions are implemented and switched off, so that the
base run reproduces the worked example while the machinery stays visible and testable:

- **The automatic premium loan** 自動振替貸付, a premium not paid in cash but advanced
  against the surrender value. ``default_rate(t)`` is the table rate times
  :func:`apl_default_mult`, which is 0 on every model point but 8, so the base run has
  ``default_rate`` identically zero and ``loan_pp`` identically zero with it. An APL is
  emphatically **not** a lapse: a policy does not lapse while the cash value can carry
  the premium. The advance is capped at the value available, and the exhaustion test and
  the clawback belong to the whole life chassis, where they are exercised in both
  positions.
- **The policy loan** 契約者貸付, drawn at outset as :func:`pol_loan_util` of the first
  year's surrender value and rolling up at ``i_loan``. Zero on every model point but 9.
  Both loans net off the death benefit and the surrender benefit and neither produces a
  cash flow of its own.
- **The refused waiver.** When the three-year suicide carve-out, the successor's
  intentional act or war bites, the contract does not merely lose the waiver — it
  **terminates**, paying the policy value to the 契約者's heirs. ``wv_frac = 1`` in the
  base run, so :func:`claims` ``(t, "PH_DEATH")`` is identically zero and the
  ``claims_ph_death`` column is a column of zeros. That zero is a product fact worth
  publishing, in the same way ``claims(t, "LAPSE")`` is on the UK term chassis, and model
  point 4 makes it non-zero.
- **Dynamic surrender** on the value-to-premium ratio,
  ``w_dyn = w x min(3, max(1, 1 + beta (CV / cumprem - 1)))`` with ``beta = 2``, elected
  by the ``dyn_lapse`` column and true only on model point 6. On this product it is
  **inert wherever it is switched on**, and that is the finding rather than a defect: the
  surrender value never reaches cumulative premiums on either cell, so an owner is never
  given a value reason to surrender. Model point 6 exists to show the module wired and
  inert rather than absent.
- **The mortality margins**, :func:`mort_be_factor` on the insured and :func:`wv_load` on the
  policyholder, both 1.00 in the base run. They are two inputs and not one because the
  margin points in opposite directions on the two lives: on the 契約者 the waiver is a
  cost, so an overstated rate is prudent, while on an insured child whose death benefit
  is approximately the reserve the contract already holds the same margin is nearly
  neutral. ``mort_be_factor = 1.00`` also means the base run is a **valuation-table run, not a
  best estimate**, taken so that every number in the worked example can be checked
  against a document anyone can download.

Three constructions are named and deliberately **not** implemented. ``dividend_type`` is
validated and the value ``five_year`` is rejected by name: the ５年ごと利差配当 variant needs
a 配当基準 no carrier publishes, and the notes' cash flow equation carries no dividend
term. 復活 (reinstatement) is not modelled either, and it costs more here than on a
protection product, because two carriers pay a 学資金 whose payment date fell while the
policy was lapsed once the policy is reinstated — so treating every exit as terminal
understates later-duration in force, premium income, staged benefits and the maturity
benefit together. 減額 (a reduction of the sum assured) is the third, and it belongs to the
savings chassis rather than to this product: there is no reduction year and no
partial-surrender cash flow, so ``sum_assured()`` is one number for the whole term. It is
not free here — on the education cell a reduction re-scales the whole staged grid, every
payment of which is a percentage of 基準保険金額 — which is why the absence is stated rather
than left to inference.

.. rubric:: Sign convention

The notes' ``CF(t)`` is already **income positive** — premiums less every outgo — which
is the library-wide sign of :func:`net_cf`, so there is no ``liability_cf`` companion to
publish here: one stream, one sign, one name.

.. rubric:: 返戻率 is a contractual ratio, not a model output

:func:`henreiritsu` returns ``(S x sum of g(k) + S) / (P x m)``: contractual amounts on
one policy that survives, pays every premium, takes every benefit in cash and receives no
dividend. It is not probability-weighted, not discounted, not net of tax and not net of
expenses, so it is **not** the ratio the cash-flow statement produces. It is undefined on
a policy that surrenders and unbounded on a waived one, which is why it reads the
contractual premium term ``P x m`` and never the projected premium income. Computed from
a 月払 premium it sits below the carrier's own published figure.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

# --- the model point


def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The policy identifier of the model point, e.g. ``EN-JP-0001``."""
    return str(model_point()["policy_id"])


def cell():
    """Which cell of the composite this model point is: endowment or education.

    ``endowment`` is 養老保険, a finite term whose 満期保険金 equals the death benefit;
    ``education`` is 学資保険, whose benefits are a staged 学資金 schedule plus a maturity
    payment, whose death payment is a return of premiums, and which carries the waiver.
    """
    v = str(model_point()["cell"])
    if v not in ("endowment", "education"):
        raise ValueError("invalid cell: " + v)
    return v


def sex():
    """The sex (M / F) of the 被保険者 (*hihokensha*), the insured life."""
    return str(model_point()["sex"])


def issue_age():
    """x: the 契約年齢 of the 被保険者, on a 満年齢 (attained age) basis.

    The fractional year is discarded at 契約日 and the age increments on each
    年単位の契約応当日 rather than on the birthday, so the attained age in period
    ``t`` is ``x + t`` exactly.  The shipped table is built on a nearest-birthday
    basis and is read here at the attained age with no adjustment **[std]**; the
    resulting understatement of up to half a year of age is named in the technical notes
    rather than hidden.
    """
    return int(model_point()["issue_age"])


def ph_sex():
    """The sex (M / F) of the 契約者 (*keiyakusha*), the policyholder.

    Only the education cell has a second life.  Reading it on the endowment cell is an
    error, not a missing value: there is no waiver there and nothing for a second life to
    do.
    """
    if cell() != "education":
        raise ValueError("the endowment cell has no 契約者 life")
    return str(model_point()["ph_sex"])


def ph_issue_age():
    """y: the 契約年齢 of the 契約者, on the same 満年齢 basis as :func:`issue_age`.

    The second life of the education cell, whose decrement drives the waiver and runs
    over ``t = 0 .. m - 1`` only — the premium-paying periods.
    """
    if cell() != "education":
        raise ValueError("the endowment cell has no 契約者 life")
    return int(model_point()["ph_issue_age"])


def sum_assured():
    """S: 基準保険金額, the amount every benefit is scaled from.

    On the endowment cell it is a sum assured in the ordinary sense: the death benefit,
    and the 満期保険金 paid on survival to anniversary ``n``, are both exactly ``S``.  On the
    education cell it is a **benefit-scaling unit and not a sum assured** — total
    premiums run to nearly twice it — which is why the acquisition deduction is re-based
    on one annual premium rather than on ``S``.
    """
    return float(model_point()["sum_assured"])


def policy_term():
    """n: the 保険期間 in years.  The projection is exactly this long."""
    return int(model_point()["policy_term"])


def prem_term():
    """m: the 保険料払込期間 in years, ``m <= n``.

    Premiums are level and guaranteed for years 1 .. m and there is none thereafter.  No
    retrieved 約款 carries a unilateral repricing right, so every year of premium and
    every year of benefit sits inside any defensible contract boundary.
    """
    m = int(model_point()["prem_term"])
    if m > policy_term():
        raise ValueError("prem_term exceeds policy_term")
    return m


def premium_pp():
    """P: the level annual premium per policy, payable in advance in years 1 .. m.

    On the two anchor cells this is 12 times a monthly premium published for exactly that
    cell **[std]**.  No carrier publishes an annual-mode scale, so the modal discount a
    real 年払 rate would carry is not applied and both annual premiums are slightly
    **overstated** — which matters more here than on a protection product, because the
    return ratio the product is sold on moves with it.  On the other model points the
    premium is the net premium grossed at the anchor cell's implied loading **[std]**.
    """
    return float(model_point()["premium_annual"])


def schedule_id():
    """The key into ``benefit_schedule_table.csv``; ``none`` on the endowment cell.

    ``none`` is a product fact and not a missing value.  The type, once elected, cannot
    be changed after issue, so this is a model point attribute and never a projected
    decision.
    """
    return str(model_point()["schedule_id"])


def waiver():
    """Whether 保険料払込免除 is written on the 契約者; false on the endowment cell.

    The trigger is the 契約者's death, 高度障害, or 身体障害 from a listed accident within 180
    days, during 保険料払込期間.  The first two are inside the table rate already; the third
    is not, and :func:`wv_load` is the multiplier that would add it.
    """
    v = bool(model_point()["waiver"])
    if v and cell() != "education":
        raise ValueError("the waiver is written on the education cell only")
    return v


def apl_elected():
    """Whether 自動振替貸付 (automatic premium loan) is elected; on by default.

    Election alone advances nothing: the module also needs a non-zero premium-default
    rate, which :func:`apl_default_mult` supplies and which is zero in the base run.  Two
    of the six carriers in the source set do not offer the APL at all, so the off
    position is a product variant and not merely a switch.
    """
    return bool(model_point()["apl_elected"])


def apl_default_mult():
    """The multiplier on the table premium-default rate **[std]**; 0 in the base run.

    The switch that turns the automatic premium loan module on.  Zero on every shipped
    model point but 8, which runs the table rates in full.
    """
    return float(model_point()["apl_default_mult"])


def pol_loan_util():
    """The fraction of the first year's 解約返戻金 drawn as a 契約者貸付 **[std]**.

    Zero in the base run.  Model point 9 draws half.  The loan is taken at outset and
    rolls up at ``i_loan``; it produces no cash flow of its own and nets off the death
    benefit and the surrender benefit instead.
    """
    return float(model_point()["pol_loan_util"])


def dividend_type():
    """The dividend design; ``none`` on the composite, which is 無配当.

    ``five_year`` — the ５年ごと利差配当 variant two carriers write — is **rejected by name**.
    It needs a 配当基準 that sits in the filed but unpublished 算出方法書, no retrieved
    document quantifies it, and the notes' cash flow equation carries no dividend term.
    A model point asking for it fails here rather than silently projecting a 無配当
    contract under a 有配当 label, which would present a non-guaranteed element as certain.
    :func:`net_cf` evaluates this, so the rejection reaches the projection rather than
    waiting for a caller who might never ask.
    """
    v = str(model_point()["dividend_type"])
    if v == "five_year":
        raise ValueError(
            "dividend_type 'five_year' is out of scope: the ５年ごと利差配当 variant needs "
            "a 配当基準 no retrieved source publishes")
    if v != "none":
        raise ValueError("invalid dividend_type: " + v)
    return v


def dyn_lapse():
    """Whether the dynamic surrender module is switched on; false in the base run.

    True on model point 6 only, where it is **inert** — the surrender value never reaches
    cumulative premiums on either cell, so the multiplier never leaves 1.  That the
    module is inert is the finding, not a defect.
    """
    return bool(model_point()["dyn_lapse"])


def mort_be_factor():
    """The multiplier on the 被保険者's table mortality **[std]**; 1.00 in the base run.

    1.00 makes the base run a **valuation-table run, not a best estimate**: the shipped
    rates trace a table carrying a safety margin sized to roughly a 2-sigma level, and a
    best-estimate basis is an adjustment of it.  It moves the projection decrement and
    **not** the policy value, which is a contractual quantity on the pricing basis.
    """
    return float(model_point()["mort_adj"])


def wv_load():
    """The multiplier on the 契約者's table mortality **[std]**; 1.00 in the base run.

    The one place on this product where a separate disability decrement is right.  The
    table already carries 高度障害, so the waiver's death and 高度障害 triggers are inside
    ``q`` and adding a decrement for them would double-count.  Its **third** trigger,
    身体障害 from a listed accident within 180 days, is genuinely additional, and holding
    ``wv_load`` at 1.00 therefore *understates* the waiver — the exact opposite of the
    ruling on 高度障害, and confusing the two is a pitfall.
    """
    return float(model_point()["wv_load"])


def wv_frac():
    """The fraction of 契約者 decrements that qualify for the waiver **[std]**; 1.00 in base.

    The complement is not "no waiver" but **termination**: the three-year suicide
    carve-out, the 後継保険契約者's intentional act and war each end the contract against the
    責任準備金 paid to the 契約者's legal heirs.  That is what
    :func:`claims` ``(t, "PH_DEATH")`` pays, and it is identically zero while this is 1.
    """
    return float(model_point()["wv_frac"])


def wv_lapse_mult():
    """The surrender-rate multiplier applied to the waived state **[std]**; 1.00 in base.

    Almost certainly too high: a waived policy receives every benefit for no further
    premium and has a strictly dominant reason to persist.  It is named so that it can be
    moved, and model point 5 halves it.
    """
    return float(model_point()["wv_lapse_mult"])


# --- structure


def proj_years():
    """n: the 保険期間 in years — the span of the **anniversary** index ``k``.

    ``k`` runs ``0 .. proj_years()`` and stays in years on this grid, because every
    contractual value in the product is defined at an anniversary: the 保険料積立金, the
    解約返戻金, the 解約控除, the staged 学資金 grid and the 満期保険金 all fall on a
    年単位の契約応当日 and are quoted by policy year.
    """
    return policy_term()


def proj_len():
    """The **number** of projected policy **months**: ``12 n``, the 保険期間 exactly.

    The exclusive end of the 0-based frame, so ``result_cf()`` covers
    ``t = 0 .. proj_len() - 1`` and ``len(result_cf()) == proj_len()``.  Twelve rows to
    the policy year, so the endowment anchor cell's thirty-year term is 360 rows.

    There is no tail and no terminal age.  Everything closes at the end of the last
    **month** ``t = 12n - 1``, whose closing instant is the anniversary ``n``, and the
    closing cash flow is a certain payment of ``S`` to the survivors rather than a
    decrement.  Importing a whole life chassis's terminal age would project a contract
    that has already matured.
    """
    return 12 * policy_term()


def duration(t):
    """The number of **completed** policy years at the start of policy month t, ``t // 12``.

    The bridge from the monthly projection index to the annual anniversary index ``k``:
    month ``t`` opens inside the policy year running from anniversary ``duration(t)`` to
    ``duration(t) + 1``.
    """
    return t // 12


def policy_year(t):
    """y(t) = 1 + t // 12: the contractual policy year of month t, a 1-based label.

    The key into ``lapse_table.csv``, whose ``policy_year`` column is 1-based, and the
    label the 保険料払込期間 and the staged grid are quoted against.  **Derived, never
    indexed by**: every cells here is indexed by the 0-based month ``t`` or by the
    anniversary ``k``.
    """
    return 1 + duration(t)


def age(t):
    """x + floor(t / 12): the attained age of the 被保険者 in policy month t.

    The 契約年齢 holds for the twelve months of policy year 1; the table is graduated by
    整数年齢 and the rating age steps on the 契約応当日.
    """
    return issue_age() + duration(t)


def age_ph(t):
    """y + floor(t / 12): the attained age of the 契約者 in policy month t.

    Defined on the education cell only, and read only while premiums are still due: after
    払込満了 there is no premium to waive and the second decrement is dropped entirely.
    """
    return ph_issue_age() + duration(t)


def prem_period_months():
    """12 m: the 保険料払込期間 in policy months — the month 払込満了 falls at.

    Premiums fall at the anniversary months ``0, 12, …, 12(m - 1)`` and none falls at
    ``12 m`` or after, so this is the exclusive end of the premium-paying months and the
    anniversary the 解約控除 has graded to zero at.
    """
    return 12 * prem_term()


def prem_cum_pp(k):
    """P x min(k, m): cumulative premiums **due** over the first k policy years.

    An anniversary quantity, ``k = 0`` at issue: ``prem_cum_pp(0) = 0`` and
    ``prem_cum_pp(k)`` counts the k premiums falling due at times ``0 .. k - 1``, so the
    death benefit of period ``t``, payable at anniversary ``t + 1``, reads it at
    ``t + 1``.

    Deemed-paid, not cash-paid.  On a waived policy this keeps growing although the
    policy pays nothing, because the contract provides that each future premium is
    treated as having been paid on its 契約応当日 — which is what makes the education
    cell's return-of-premiums death benefit behave the same in both states.
    """
    return premium_pp() * min(k, prem_term())


def prem_cum_pp_m(u):
    """Cumulative premiums **due** by elapsed month u.

    The premium is annual and falls at the anniversary months ``0, 12, 24, …``, so the
    count due by elapsed month ``u`` is ``ceil(u / 12)`` capped at ``m`` — a **step**
    function of ``u``, not a smooth accrual, because that is what paying once a year is.
    It agrees with :func:`prem_cum_pp` at every anniversary, and it is what the education
    cell's return-of-premiums death benefit reads for a death between two.
    """
    return premium_pp() * min(-(-u // 12), prem_term())


# --- decrement rates


def mort_rate_at_age(sx, z):
    """The raw table mortality rate for sex ``sx`` at attained age ``z``.

    A **[std]** construction anchored to 生保標準生命表2018（死亡保険用）and never a copy of
    it; the rate **includes 高度障害**, so the endowment cell's 重度障害 benefit is not a
    separate decrement.  Read unadjusted by the cash-value construction, which is a
    contractual quantity on the pricing basis; :func:`mort_rate` and :func:`mort_rate_ph`
    apply the projection's own multipliers on top.
    """
    return float(data.mort_table().loc[(sx, z), "mort_rate"])        # noqa: F821


def mort_rate(t):
    """q(t): the **annual** 被保険者 mortality rate in policy month t.

    The table rate at ``x + floor(t/12)`` times :func:`mort_be_factor`, capped at 1.  It
    runs on **both** states: a waived policy is still insured.  This is the annual rate the
    table is stated on; :func:`mort_rate_mth` is the decrement applied to the month.
    """
    return min(1.0, mort_rate_at_age(sex(), age(t)) * mort_be_factor())


def mort_rate_mth(t):
    """q_m(t): the monthly 被保険者 decrement, ``1 - (1 - q(t))^(1/12)`` **[std]**.

    The **effective** convention, not a nominal ``q / 12``, so twelve months compound back
    to the annual rate exactly and survivorship at the anniversaries is what the
    annual-grid model produced.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_rate_ph(t):
    """q_p(t): the **annual** 契約者 decrement driving the waiver in policy month t.

    The table rate at ``y + floor(t/12)`` times :func:`wv_load`, and **zero from the month
    ``12 m`` on** — every waiver trigger is conditional on the event falling during
    保険料払込期間, so after 払込満了 there is nothing for the provision to do and the composite
    treats the contract as continuing through the 契約者's death by succession.  Zero
    throughout on the endowment cell, which has no second life.
    """
    if not waiver() or t >= prem_period_months():
        return 0.0
    return min(1.0, mort_rate_at_age(ph_sex(), age_ph(t)) * wv_load())


def mort_rate_ph_mth(t):
    """q_p,m(t): the monthly 契約者 decrement, ``1 - (1 - q_p(t))^(1/12)`` **[std]**.

    The waiver decrement converts on the same effective convention as the insured's.  It
    is a real second decrement on a second life and not a rider charge, so it gets the
    same treatment and not a twelfth.
    """
    return 1.0 - (1.0 - mort_rate_ph(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table voluntary surrender rate in period t **[std]**.

    The table is keyed by the **contractual policy year** ``policy_year(t)``, a 1-based
    label, so the first twelve months read the year-1 row.  The rates are **annual** and
    are not restated per month.  4 / 3 / 2 percent, the last row applying to every
    later policy year.  The shape is
    inherited from the savings chassis so that the products stay comparable.  No carrier
    publishes a lapse or surrender curve by duration for either cell — the single largest
    assumption gap on this product — and the only public benchmark, an industry
    解約・失効率 of 5.6% defined on **sum assured** across all product types, is used as a
    sanity ceiling and nothing more.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())), "lapse_rate"])


def dyn_lapse_factor(t):
    """The dynamic surrender multiplier in period t **[std]**; 1 in the base run.

    ``min(3, max(1, 1 + beta max(0, CV / cumprem - 1)))`` with ``beta = 2``, both read at
    the **end of month t**, where the surrender is paid.  On
    this product it never leaves 1 even when switched on, because the surrender value is
    below cumulative premiums at every duration on both cells — peaking at 92.0% at
    maturity on the endowment anchor cell.  A thirty-year 養老保険 at a 1.00% 予定利率 gives
    its owner no point at which surrendering beats persisting on value grounds alone,
    and that is the finding the module exists to produce.
    """
    if not dyn_lapse():
        return 1.0
    base = prem_cum_pp_m(t + 1)
    if base <= 0.0:
        return 1.0
    return min(dyn_lapse_cap, max(                                   # noqa: F821
        1.0, 1.0 + dyn_lapse_beta * max(0.0, cv_at_m(t + 1) / base - 1.0)))  # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** voluntary surrender rate of the policy year containing month t.

    The table rate times the dynamic multiplier, and **zero in the final month**,
    ``t = proj_len() - 1`` **[std]**.  That zero is not a rounding of a small number: a
    surrender at the end of the final month and the maturity payment fall on the same
    anniversary at the same amount, so running both double-counts the terminal payment
    and running the surrender instead of the maturity misclassifies most of the outgo
    into the wrong column.

    **The monthly grid shrinks that carve-out from a year to a month**, and the difference
    is real rather than cosmetic: the annual grid had to suppress surrender for the whole
    of the last policy year, twelve months in which an owner could in fact still
    surrender, and here only the month whose end *is* the maturity date is suppressed.
    """
    if t >= proj_len() - 1:
        return 0.0
    return min(1.0, lapse_rate_base(t) * dyn_lapse_factor(t))


def lapse_rate_mth(t):
    """w_m(t): the monthly voluntary surrender rate, ``1 - (1 - w(t))^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def default_rate(t):
    """u(t): the premium-default rate feeding the APL module; zero in the base run.

    The table rate — keyed, like :func:`lapse_rate_base`, by the contractual policy year —
    times :func:`apl_default_mult`, and zero once premiums have ceased.

    **Non-zero only in a premium due month.**  A default is the failure to pay one
    particular premium on one particular date, not a hazard running through a year, so the
    annual rate is applied once at each anniversary the premium falls due and is never
    converted to a monthly equivalent.  A default is also **not** a lapse: the advance is
    applied to the premium and the policy stays in force, which is exactly the Japanese
    mechanic that has no analogue in the U.S. or UK reference sets.  It therefore moves
    :func:`premiums` and :func:`loan_pp` and leaves the in-force recursion alone.  The
    waived state never defaults, because there is no premium there to miss.
    """
    if not apl_elected() or t % 12 != 0 or t >= prem_period_months():
        return 0.0
    tbl = data.lapse_table()                                         # noqa: F821
    rate = float(tbl.loc[min(policy_year(t), int(tbl.index.max())), "default_rate"])
    return min(1.0, rate * apl_default_mult())


# --- the staged benefit schedule


def benefit_schedule():
    """The whole staged 学資金 grid for this model point, as ``{anniversary: fraction}``.

    Read from ``benefit_schedule_table.csv`` by :func:`schedule_id`.  The file's key
    column is ``k``, the **anniversary** the payment falls on with ``k = 0`` at issue —
    3 / 6 / 12 / 15 / 18 / 20 on the S型 grid — and not the projection's period index
    ``t``: the payment due at anniversary ``k`` falls at the end of period ``k - 1``.
    An empty dict on the endowment cell, whose ``schedule_id`` is ``none``: the survival
    benefit there is a single payment at anniversary ``n`` and there is no staged
    schedule at all.  The maturity benefit is never a row here — it is always present on
    both cells and is held separately, so that a schedule with no rows still matures.
    """
    sid = schedule_id()
    tbl = data.benefit_schedule_table()                              # noqa: F821
    if sid not in tbl.index:
        return {}
    sub = tbl.loc[[sid]]
    return {int(a): float(b)
            for a, b in zip(sub["k"], sub["benefit_pct"])}


def benefit_pct(k):
    """g(k): the staged 学資金 due at anniversary k, as a fraction of S.

    Anniversary-indexed, ``k = 0`` at issue, so the staged claim of period ``t`` reads
    ``benefit_pct(t + 1)``.  Zero at every anniversary the schedule does not name, and
    zero throughout on the endowment cell.  It is a fraction of ``S``, never of a
    premium: on the education cell the two are within a factor of two of each other, so
    the distinction is not idle.
    """
    return benefit_schedule().get(k, 0.0)


def benefit_pct_cum(k):
    """G(k): the cumulative staged fraction paid to and including anniversary k."""
    return sum(v for s, v in benefit_schedule().items() if s <= k)


# --- the cash-value construction


def surv_prob(z, k):
    """k p z: the probability that a life of the insured's sex survives k years from age z.

    On the **unadjusted** table, because this is the cash-value basis: the policy value is
    a contractual quantity computed on the pricing basis, so :func:`mort_be_factor` must not
    move it.
    """
    if k <= 0:
        return 1.0
    return surv_prob(z, k - 1) * (1.0 - mort_rate_at_age(sex(), z + k - 1))


def endow_epv(z, k, i):
    """A(z, k): the EPV at rate ``i`` of a k-year endowment assurance of 1 issued at age z.

    1 at the end of the year of death within k years, or 1 on survival to k.  ``k = 0``
    returns 1, which is what makes ``W(n) = S`` exact on the endowment cell.
    """
    if k <= 0:
        return 1.0
    v = 1.0 / (1.0 + i)
    total = 0.0
    for j in range(k):
        total += (v ** (j + 1)) * surv_prob(z, j) * mort_rate_at_age(sex(), z + j)
    return total + (v ** k) * surv_prob(z, k)


def annuity_due(z, k, i):
    """a-due(z, k): the EPV at rate ``i`` of a k-year annuity-due of 1 issued at age z.

    In years of premium, so ``S x A / a-due`` is yen per year.  ``k = 0`` returns 0.
    """
    v = 1.0 / (1.0 + i)
    return sum((v ** j) * surv_prob(z, j) for j in range(k))


def edu_epv(k, i):
    """EPV(k): the education cell's survival-benefit EPV at anniversary k, at rate ``i``.

    Per policy in force, ``k = 0`` at issue.
    ``S x [ sum over s > k of g(s) v^(s-k) (s-k)p + v^(n-k) (n-k)p ]``.  The ``s > k``
    is what makes :func:`pol_val_pp` the value **after** the staged benefit due at ``k``,
    which is the sourced fact that each 祝金 reduces the surrender value.

    Excluding the death benefit from the EPV is the **[std]** step, and it is one
    carrier's own wording read literally: its 死亡払戻金 *is* the 責任準備金相当額, so on that
    design the decrement is exactly value-neutral, and the composite's max-form death
    benefit dominates it.
    """
    v = 1.0 / (1.0 + i)
    z = issue_age() + k
    n = policy_term()
    total = sum(g * (v ** (s - k)) * surv_prob(z, s - k)
                for s, g in benefit_schedule().items() if s > k)
    return sum_assured() * (total + (v ** (n - k)) * surv_prob(z, n - k))


def prem_net_level_at(i):
    """The net level premium at rate ``i``: pi on the endowment cell, pi_g on the other.

    ``S x A(x, n) / a-due(x, m)`` where the death benefit is inside the EPV, and
    ``EPV(0) / a-due(x, m)`` where it is not.  A derived quantity, never an input: the
    gross premium is sourced and the loading is what falls out.
    """
    if cell() == "endowment":
        return (sum_assured() * endow_epv(issue_age(), policy_term(), i)
                / annuity_due(issue_age(), prem_term(), i))
    return edu_epv(0, i) / annuity_due(issue_age(), prem_term(), i)


def prem_net_level_pp():
    """pi: the net level premium on the cash-value basis rate ``i_cv``.

    The seam of the composite shows here and is meant to.  On the endowment anchor cell
    the net premium is well below the sourced gross premium, an implied loading of about
    19.5% that is plausible for a thirty-year endowment and coherent because the premium
    and the rate come from the same carrier and the same release.  On the education anchor
    cell the same calculation gives a net premium **above** the gross one — a negative
    loading that no real product carries — because that premium is a different carrier's
    and that carrier does not publish its 予定利率.  It is visible, it is derived, and
    :func:`implied_rate` restates it as a rate.
    """
    return prem_net_level_at(i_cv)                                      # noqa: F821


def implied_rate():
    """The rate at which the net level premium equals the sourced gross premium.

    The loading of :func:`prem_net_level_pp` restated as a rate, solved by bisection on
    :func:`prem_net_level_at`, which is monotone decreasing in the rate.  Below ``i_cv``
    wherever the loading is positive and above it wherever the loading is negative, so
    the sign of the gap between this and ``i_cv`` is the sign of the loading.  A derived
    diagnostic, never an input.
    """
    lo, hi = -0.20, 0.50
    target = premium_pp()
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if prem_net_level_at(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def pol_val_at(k, i):
    """W(k) at rate ``i``: the policy value at anniversary k, after any staged benefit.

    ``k = 0`` at issue, where it is zero by the definition of the net level premium.
    ``S x A(x + k, n - k) - pi x a-due(x + k, m - k)`` on the endowment cell and
    ``EPV(k) - pi_g x a-due(x + k, m - k)`` on the education cell.  At ``k = n`` there is
    no future benefit beyond maturity and no future premium, so it is ``S`` exactly on
    **both** cells, by construction — the identity :func:`check_pol_val_terminal`
    asserts, and the one thing a whole life chassis can never check.
    """
    n, m = policy_term(), prem_term()
    ann = annuity_due(issue_age() + k, max(m - k, 0), i)
    if cell() == "endowment":
        return (sum_assured() * endow_epv(issue_age() + k, n - k, i)
                - prem_net_level_at(i) * ann)
    return edu_epv(k, i) - prem_net_level_at(i) * ann


def pol_val_pp(k):
    """W(k): 保険料積立金, the policy value at anniversary k on the cash-value basis.

    ``k = 0`` at issue; the closing value of period ``t`` is ``pol_val_pp(t + 1)``.
    **After** any staged benefit due at ``k``, which is why the surrender value falls by
    exactly the amount of each 祝金 rather than beside it.  Identical in the paying and the
    waived states: the value is computed as if the premiums had been paid, so a model
    that keeps two value series is modelling a contract nobody wrote.
    """
    return pol_val_at(k, i_cv)                                       # noqa: F821


def pol_val_pre_pp(k):
    """Wb(k) = W(k) + S g(k): the policy value at anniversary k **before** the staged benefit.

    The limb the education cell's death benefit and the refused-waiver termination are
    valued on, and equal to :func:`pol_val_pp` at every anniversary no staged benefit
    falls due and throughout on the endowment cell.
    """
    return pol_val_pp(k) + sum_assured() * benefit_pct(k)


def pol_val_db_pp(k):
    """The death benefit **inside** the cash-value basis: S on 養老, zero on 学資.

    Not a cash flow.  It exists so that :func:`check_pol_val_roll_fwd` can state one
    recursion covering both cells, and it names the structural difference between the two
    constructions: an endowment assurance carries the death benefit inside its EPV, while
    the education cell's death payment releases the value instead of adding to it.
    """
    return sum_assured() if cell() == "endowment" else 0.0


def reserve_pp(k):
    """The 平準純保険料式 policy reserve at anniversary k, on the reference rate ``i_std``.

    A reference quantity and **never a cash flow**.  The statutory 標準責任準備金 is set by
    告示 on the 標準利率 and the standard table, with 危険準備金 and 価格変動準備金 outside it
    altogether; this library projects gross cash flows and cites the valuation layers
    rather than reproducing them.  The current numeric 標準利率 could not be established
    from any retrieved official document, so ``i_std`` defaults to ``i_cv`` **[std]**,
    which makes ``reserve_pp(k) - surr_val_pp(k) = surr_charge_pp(k)`` exactly testable —
    see :func:`check_surr_charge`.
    """
    return pol_val_at(k, i_std)                                      # noqa: F821


def surr_charge_pp(k):
    """SC(k) = alpha P (m - k) / m: the acquisition deduction inside the surrender value.

    Anniversary-indexed, ``k = 0`` at issue, where the deduction is at its full
    ``alpha P``; it grades linearly to zero at 払込満了, ``k = m``.

    Re-based on **one annual premium** rather than on the sum assured **[std]**, because
    基準保険金額 is a benefit-scaling unit and not a sum assured on the education cell.  With
    ``alpha = 0.25`` the deduction at issue is within 0.6% of the level the whole life
    chassis calibrated against a real published surrender-value run, so the only piece of
    genuine Japanese surrender-value calibration in this library is carried across rather
    than discarded.

    No carrier publishes a surrender-value formula or a numeric surrender-value table for
    either cell, so ``alpha`` is calibrated by inheritance rather than fitted, and it
    carries the whole surrender-benefit stream.  It satisfies the three sourced
    quantitative constraints — below cumulative premiums at every duration, capped at the
    death benefit, reduced by each 祝金 — and not the fourth, adjectival one, that the
    early durations return very little.  It is the named lever and a listed model risk.
    """
    m = prem_term()
    return alpha * premium_pp() * max(0, m - k) / m                  # noqa: F821


def surr_val_pp(k):
    """V(k) = max(0, W(k) - SC(k)): the ordinary surrender value at anniversary k."""
    return max(0.0, pol_val_pp(k) - surr_charge_pp(k))


def cv_pp(k):
    """CV(k): the payable 解約返戻金 at anniversary k.

    Equal to :func:`surr_val_pp` on this product, with **no 低解約返戻金型 multiplier**.  No
    retrieved document offers a suppressed-surrender-value form of either cell, so there
    is no suppression multiplier, no step at 払込満了 and no surrender spike; importing a
    whole life chassis's
    cliff would model a product that does not exist here.  Both cells are published
    anyway so that the absence is stated rather than inferred.
    """
    return surr_val_pp(k)


def pol_val_pre_at_m(u):
    """Wb at **elapsed month u**: the policy value before any staged benefit due there.

    ``Wb(k)`` at every anniversary — ``u = 12 k`` reproduces :func:`pol_val_pre_pp`
    exactly — and **linear in the elapsed months** between two anniversaries **[std]**::

        Wb(u) = (1 - f) W(k) + f Wb(k + 1),   k = u // 12,  f = (u mod 12) / 12

    Note which two values it interpolates between: the value **after** the staged benefit
    at ``k`` and the value **before** the one at ``k + 1``.  That is the curve the contract
    actually traces — the 保険料積立金 accumulates through the year and each 祝金 takes a
    step out of it at the anniversary it falls on — and interpolating ``W(k)`` to
    ``W(k + 1)`` instead would spread each staged payment backwards over the twelve months
    before it was due.

    The within-year rule is a **[std]**: the 算出方法書 that would state it is a 基礎書類
    filed with the 金融庁 and is not published, so linear interpolation in elapsed months is
    the market's ordinary convention for a value quoted by policy year and the least
    assuming choice available.  The anniversary values are untouched, so nothing that was
    calibrated moves.
    """
    k, r = u // 12, u % 12
    if r == 0:
        return pol_val_pre_pp(k)
    f = r / 12.0
    return (1.0 - f) * pol_val_pp(k) + f * pol_val_pre_pp(k + 1)


def pol_val_at_m(u):
    """W at elapsed month u: the policy value **after** any staged benefit due there.

    Equal to :func:`pol_val_pre_at_m` everywhere except at an anniversary a 祝金 falls on,
    where it is that value less ``S g(k)`` — the same relation the two annual cells have.
    """
    k, r = u // 12, u % 12
    if r == 0:
        return pol_val_pp(k)
    return pol_val_pre_at_m(u)


def surr_charge_at_m(u):
    """SC at elapsed month u: ``alpha P (12m - u) / 12m``, floored at zero.

    The monthly reading of :func:`surr_charge_pp`, which grades linearly to zero at
    払込満了; linear in the anniversary means linear in the month, so this is the same
    schedule read finely rather than a second one.
    """
    mm = prem_period_months()
    return alpha * premium_pp() * max(0, mm - u) / mm                # noqa: F821


def cv_at_m(u):
    """CV at elapsed month u: the payable 解約返戻金 between anniversaries.

    ``max(0, W(u) - SC(u))``.  This is what a surrender in month ``t`` is paid, read at
    ``u = t + 1`` because the surrender falls at the end of the month.  There is **no
    低解約返戻金型 multiplier** on this product, so unlike ``WholeLife_JP_S`` there is no
    step for the finer grid to re-time — the value is continuous and the interpolation is
    the whole of the monthly refinement.
    """
    return max(0.0, pol_val_at_m(u) - surr_charge_at_m(u))


def death_ben_pp(t):
    """DB(t): the death benefit for a death of the 被保険者 in policy month t.

    Payable at the **end of the month**, which is where the value family is read.  On the
    endowment cell ``S`` net of loans, level for the term and equal to the maturity
    benefit.  On the education cell
    ``max(cumprem(t+1) - S G(duration(t)) - L, Wb(t+1))`` — a **return of premiums**
    floored at the policy value, where the premium limb is deemed-paid and counts the
    premiums actually fallen due by that month, and the staged benefits already received,
    those falling at anniversaries up to and including ``duration(t)``, are deducted.

    **Both limbs must be evaluated, and on the monthly grid they both bind.**  On the
    annual grid the value limb dominated at every duration of the education cell and the
    ``max`` never switched; read month by month it switches 85 times in 264.  The premium
    limb steps up by a whole 年払 premium in each anniversary month and the value accretes
    through the year to overtake it, so the refund limb binds early in each policy year
    and the value limb late in it — eleven months of the first policy year, then fewer
    each year until the value pulls clear for good in policy year 13.  A model that
    hard-codes either limb is right eleven months a year at best.
    """
    if cell() == "endowment":
        return sum_assured() - loan_pp(duration(t))
    refund = (prem_cum_pp_m(t + 1)
              - sum_assured() * benefit_pct_cum(duration(t))
              - loan_pp(duration(t)))
    return max(refund, pol_val_pre_at_m(t + 1))


# --- the loan and the automatic premium loan


def apl_advance_pp(t):
    """The 自動振替貸付 advance made at the start of policy month t; zero in the base run.

    ``P u(t)``, capped at the surrender value still free of loan.  Non-zero only in a
    premium due month, because :func:`default_rate` is and because there is nothing to
    advance in the other eleven.  The advance is applied to the premium, so the premium is
    not collected in cash and appears only as growth in :func:`loan_pp`.  The exhaustion
    test and the clawback belong to the whole life chassis, where they are exercised in
    both positions; the cap here is what keeps the loan from exceeding the value that
    secures it.
    """
    if t >= prem_period_months() or t % 12 != 0:
        return 0.0
    k = duration(t)
    return min(premium_pp() * default_rate(t),
               max(0.0, cv_pp(k + 1) - loan_pp(k)))


def loan_pp(k):
    """L(k): 契約者貸付 and APL principal with interest, at anniversary k.

    ``pol_loan_util x CV(1)`` drawn at outset **[std]** — the first anniversary's
    surrender value — then ``L(k + 1) = (L(k) + advance(k)) (1 + i_loan)``.  Identically
    zero in the base run, where nothing is drawn and nothing is defaulted.  It produces no
    cash flow of its own: it nets off the death benefit and the surrender benefit, which
    is why every benefit in the base run is gross.

    **It stays an annual quantity on the monthly grid, and that is the contract's own
    convention.**  The loan rate is a 年利 capitalised at the 年単位の契約応当日, so the
    balance genuinely does not move between anniversaries; a benefit falling in month
    ``t`` is settled net of ``loan_pp(duration(t))``, the balance actually outstanding.
    """
    if k <= 0:
        return pol_loan_util() * cv_pp(1)
    return (loan_pp(k - 1) + apl_advance_pp(12 * (k - 1))) * (1.0 + i_loan)  # noqa: F821


# --- in force


def pols_if(t):
    """l(t): the **total** in-force probability at the start of policy month t.

    ``l(t) = l_p(t) + h(t)``: the premium-paying state plus the waived state, which is
    the whole surviving block.  This is the library-wide meaning of ``pols_if`` and the
    weight on that ``result_cf()`` row — the death benefit, the staged benefit, the
    maturity benefit and the maintenance expense all run on it, because a waived policy
    is still in force and still insured.  What it is **not** is the weight on the
    premium: that is :func:`pols_if_pay`, which excludes the waived cohort.

    Identical to :func:`pols_if_pay` on the endowment cell, which has no waiver and
    therefore no second state.
    """
    return pols_if_pay(t) + pols_wv(t)


def pols_if_pay(t):
    """l_p(t): the in-force probability in the **premium-paying** state at month t's start.

    ``l_p(0) = 1``, then ``l_p(t + 1) = l_p_after(t) (1 - w(t))`` where ``l_p_after`` is
    net of both mortality decrements.  This is the weight on the premium and the renewal
    commission of the same ``result_cf()`` row, and the strict subset of :func:`pols_if`
    that is still paying.  Zero outside ``0 .. proj_len() - 1``: the contract has not
    started, or it has matured.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return 1.0
    return pols_if_pay_at(t - 1, "AFT_DECR")


def pols_wv(t):
    """h(t): the in-force probability in the **waived** state at the start of month t.

    ``h(0) = 0``, and identically zero on the endowment cell, which has no waiver.  A
    waived policy pays no premium and earns the distributor no renewal commission, but it
    still costs the insurer administration and it still receives every benefit — which is
    why the maintenance expense runs on both states and the renewal commission on one.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t == 0:
        return 0.0
    return pols_wv_at(t - 1, "AFT_DECR")


def pols_if_pay_at(t, timing):
    """The premium-paying in-force probability at a point inside policy month t.

    ``"BEF_DECR"``
        l_p(t), the start of the month, before any decrement; the same number as
        :func:`pols_if_pay` and the weight on that month's premium.

    ``"BEF_LAPSE"``
        ``l_p(t) (1 - q_m(t)) (1 - q_p,m(t))`` — after **both** monthly mortality
        decrements, which is the population surrenders are taken from.  The processing
        order is 被保険者 death, then 契約者 decrement, then the staged benefit, then
        maturity, then surrender.

    ``"AFT_DECR"``
        l_p(t + 1), the end-of-month state, and zero from ``proj_len() - 1`` on because
        everything closes at the end of the term.
    """
    if timing == "BEF_DECR":
        return pols_if_pay(t)
    if timing == "BEF_LAPSE":
        return (pols_if_pay(t) * (1.0 - mort_rate_mth(t))
                * (1.0 - mort_rate_ph_mth(t)))
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len() - 1:
            return 0.0
        return pols_if_pay_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing: " + str(timing))


def pols_wv_at(t, timing):
    """The waived-state in-force probability at a point inside policy month t.

    ``"BEF_DECR"``
        h(t), the start of the month.

    ``"BEF_LAPSE"``
        ``h(t) (1 - q_m(t)) + wv_frac x Dp(t)`` — the survivors of the insured's
        mortality plus this month's transitions in.  Only the qualifying fraction
        arrives; the rest terminates the contract instead.

    ``"AFT_DECR"``
        h(t + 1), after a monthly surrender rate of ``wv_lapse_mult x w_m(t)``, and zero
        from ``proj_len() - 1`` on.  The multiplier is applied to the **monthly** rate, so
        a waived policy that surrenders at half the ordinary pace does so at half the pace
        every month rather than at half an annual rate spread unevenly.
    """
    if timing == "BEF_DECR":
        return pols_wv(t)
    if timing == "BEF_LAPSE":
        return pols_wv(t) * (1.0 - mort_rate_mth(t)) + pols_waived(t)
    if timing == "AFT_DECR":
        if t < 0 or t >= proj_len() - 1:
            return 0.0
        return pols_wv_at(t, "BEF_LAPSE") * (
            1.0 - min(1.0, wv_lapse_mult() * lapse_rate_mth(t)))
    raise ValueError("invalid timing: " + str(timing))


def pols_if_at(t, timing):
    """The **total** in-force probability at a point inside policy month t.

    ``pols_if_pay_at(t, timing) + pols_wv_at(t, timing)`` — the library-wide within-month
    read, on the whole surviving block rather than on one state.  The two states are read
    separately by :func:`pols_if_pay_at` and :func:`pols_wv_at`, because only the
    premium-paying one carries the premium and the renewal commission.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that ``result_cf()`` row.

    ``"BEF_LAPSE"``
        the anniversary population after **both** mortality decrements and before
        surrender — the same number as :func:`pols_surv`, which is what the staged
        benefit and the maturity benefit are paid to.

    ``"AFT_DECR"``
        l(t + 1), the end-of-month state, and zero from ``proj_len() - 1`` on because
        everything closes at the end of the term.

    An invalid ``timing`` raises ``ValueError`` from the two state cells rather than
    returning a number.
    """
    return pols_if_pay_at(t, timing) + pols_wv_at(t, timing)


def pols_death(t):
    """D(t) = l(t) q_m(t): expected 被保険者 deaths in policy month t.

    On the **total** in force, paying and waived together: a waived policy is still
    insured, and the 高度障害 trigger is inside the table rate rather than beside it.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_ph_decr(t):
    """Dp(t) = l_p(t) (1 - q_m(t)) q_p,m(t): expected 契約者 decrements in month t.

    On the **premium-paying state only**, and zero from the month ``12 m`` on: a policy
    already waived has no premium left to waive, and after 払込満了 the provision has nothing
    to act on.
    """
    return pols_if_pay(t) * (1.0 - mort_rate_mth(t)) * mort_rate_ph_mth(t)


def pols_waived(t):
    """wv_frac x Dp(t): transitions into the waived state at the end of period t.

    A **state transition, not a benefit**.  It produces no outgo line at all; what it
    produces is the absence of premium income.
    """
    return wv_frac() * pols_ph_decr(t)


def pols_ph_term(t):
    """(1 - wv_frac) x Dp(t): contracts terminated because the waiver was refused.

    Zero in the base run.  Where a carve-out bites the contract does not merely lose the
    waiver, it **ends**, against the 責任準備金 paid to the 契約者's legal heirs — which is
    what :func:`claims` ``(t, "PH_DEATH")`` pays.
    """
    return (1.0 - wv_frac()) * pols_ph_decr(t)


def pols_surv(t):
    """R(t): the expected in force at the end of month t, after mortality, before surrender.

    ``l_p_after(t) + h_after(t)``.  This is what the staged benefit and the maturity benefit
    are paid to, in **both** states.
    """
    return pols_if_pay_at(t, "BEF_LAPSE") + pols_wv_at(t, "BEF_LAPSE")


def pols_lapse(t):
    """Sr(t): expected surrenders at the end of policy month t.

    ``l_p_after(t) w_m(t) + h_after(t) wv_lapse_mult w_m(t)``, taken from the survivors of
    both monthly mortality decrements and valued on the surrender value **net of any staged
    benefit just paid**.  Zero in the final month ``t = 12n - 1``, where :func:`lapse_rate`
    is zero.
    """
    return (pols_if_pay_at(t, "BEF_LAPSE")
            + pols_wv_at(t, "BEF_LAPSE") * wv_lapse_mult()) * lapse_rate_mth(t)


def pols_maturity(t):
    """R in the final month and zero elsewhere: the survivors who mature.

    The maturity benefit is **certain, not a decrement**: at the end of the month
    ``t = proj_len() - 1``, whose closing instant is the anniversary ``n``, the survivors
    are paid ``S`` with probability 1.  Modelling maturity as a rate, or letting the
    projection run past the last month, is wrong in both directions.  It is named
    separately so that the in-force roll-forward closes in the final month, where the
    survivors neither die nor surrender.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_surv(t)


# --- cash flows


def premiums(t):
    """Premium income at the start of policy month t, an inflow.

    **The premium is annual (年払), so it falls in one month out of twelve** — the
    anniversary months ``t = 0, 12, …, 12(m - 1)`` — and is zero in the other eleven.
    That is the most visible change the monthly grid makes to this statement: one large
    inflow a year against maintenance expense every month, which is what a 年払 contract
    is and what the annual grid could not show.

    ``P l_p(t)`` at those months, less anything advanced under the automatic premium loan,
    which is not collected in cash.  Carried on :func:`pols_if_pay` alone and never on
    :func:`pols_if`: the waived state is in force and pays nothing.
    """
    if t % 12 != 0 or t >= prem_period_months():
        return 0.0
    return (premium_pp() - apl_advance_pp(t)) * pols_if_pay(t)


def claims(t, kind=None):
    """Benefit outgo in policy month t, by kind; the total when kind is omitted.

    Every limb falls at the **end of the month**, which is where the value family is read.

    ``"DEATH"``
        ``max(0, DB(t)) D(t)``, at the end of the month of death, on both states.

    ``"STAGED"``
        ``S g(k) R(t)`` in the month whose end **is** the anniversary ``k`` the 学資金
        falls on — the month ``t = 12k - 1`` — and zero in the other eleven.  A staged
        payment is a payment on a date, so it belongs to one month.  It is paid on
        survival to everything in force in **both** states; it is not a decrement and it
        terminates nothing.  Zero throughout on the endowment cell.

    ``"MATURITY"``
        ``S R`` in the final month and zero elsewhere — a certain payment, not a rate.

    ``"LAPSE"``
        ``max(0, CV(t + 1) - L) Sr(t)``, on the interpolated value at the end of the
        month and net of any staged benefit just paid.

    ``"PH_DEATH"``
        ``Wb(t + 1) (1 - wv_frac) Dp(t)``: the policy value paid to the 契約者's heirs
        where a waiver carve-out terminates the contract.  Identically **zero** in the
        base run, and published as a column of zeros because the zero is the product fact.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("DEATH", "STAGED", "MATURITY", "LAPSE", "PH_DEATH"))
    if kind == "DEATH":
        return max(0.0, death_ben_pp(t)) * pols_death(t)
    if kind == "STAGED":
        if (t + 1) % 12 != 0:
            return 0.0
        return sum_assured() * benefit_pct((t + 1) // 12) * pols_surv(t)
    if kind == "MATURITY":
        return sum_assured() * pols_maturity(t)
    if kind == "LAPSE":
        return max(0.0, cv_at_m(t + 1) - loan_pp(duration(t))) * pols_lapse(t)
    if kind == "PH_DEATH":
        return pol_val_pre_at_m(t + 1) * pols_ph_term(t)
    raise ValueError("invalid kind: " + str(kind))


def claim_expenses(t):
    """ec D(t): the claim handling expense on the month's death claims **[std]**.

    A flat amount per death claim, uninflated, and a cells and a ``result_cf()`` column
    of its own.  :func:`expenses` carries acquisition and maintenance only and
    :func:`net_cf` deducts this line explicitly beside it, so that ``expenses`` means one
    thing across the library — a per-policy servicing cost, never a per-claim one — and
    the technical notes' worked example prints the two as two columns.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^(y(t) - 1)`` **[std]**.

    **Annual steps inside the monthly grid**: maintenance inflates once a policy year, at
    the anniversary, and not once a month.  The assumption is an annual observation and
    compounding it monthly would assert a within-year expense profile no source supports.
    """
    return (1.0 + inflation_rate) ** (policy_year(t) - 1)            # noqa: F821


def maint_expenses(t):
    """e_m(t): the inflating maintenance expense in policy month t **[std]**.

    A twelfth of the annual per-policy amount each month to the end of the term,
    inflating once a policy year, and carried on **both** states: a waived policy costs
    the insurer administration although it pays the distributor nothing.  There is no
    separate maturity or staged-benefit expense; both are folded in here.
    """
    return expense_maint / 12.0 * inflation_factor(t) * pols_if(t)   # noqa: F821


def acq_expenses(t):
    """E0: the acquisition expense per policy at issue **[std]**; zero after period 0.

    No carrier publishes an expense basis at all — 予定事業費率 is named in the
    保険契約者保護機構 boilerplate and never quantified — so this and every other expense level
    is inherited unchanged from the savings chassis so that the products stay comparable.
    """
    return expense_acq * pols_if_pay(t) if t == 0 else 0.0               # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in period t: the **policy** expenses only.

    Maintenance, and at ``t = 0`` the acquisition expense as well.  The claim handling
    expense is **not** in here: it is a per-claim cost rather than a per-policy one, it
    lives in :func:`claim_expenses`, :func:`net_cf` deducts it explicitly, and it is
    published as its own ``claim_expenses`` column.  Folding it in here is how two models
    come to publish an ``expenses`` column that cannot be compared.
    """
    return acq_expenses(t) + maint_expenses(t)


def commissions(t):
    """Commission outgo in policy month t **[std]**.

    The initial commission at issue, ``t = 0``, then renewal commission on the premium in
    policy years 2 .. m — the anniversary months ``t = 12, 24, …`` — on the
    **premium-paying state only**.  It follows the premium it is a percentage of, so it
    falls in the month the premium does and is zero in the eleven between.  That the
    renewal commission runs on one state while the maintenance expense runs on both is not
    a detail: a waived policy costs the insurer administration and pays the distributor
    nothing.
    """
    init = comm_init_rate * premium_pp() * pols_if_pay(t) if t == 0 else 0.0  # noqa: F821
    renew = (comm_renewal_rate * premium_pp() * pols_if_pay(t)           # noqa: F821
             if t % 12 == 0 and 12 <= t < prem_period_months() else 0.0)
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**.

    Premiums less death claims, the refused-waiver termination, the staged benefit, the
    maturity benefit, surrender benefits, the claim handling expense, maintenance and
    acquisition expense and commission.  The claim expense is deducted explicitly rather
    than through :func:`expenses`, which carries acquisition and maintenance only.  This
    is the technical notes' own sign, which is also the library-wide convention, so there
    is no outgo-positive ``liability_cf`` companion to publish.

    The shape to expect is a deep new business strain in the first month, then a sawtooth
    of one premium a year against expense and claims every month, then **one very large
    negative month at maturity**: on the endowment anchor cell the maturity payment is the
    largest single item in the stream and on this grid it is one month wide rather than
    one year.  Unlike a behavioural cliff it is a certain payment; the only uncertainty in
    it is how many policies reach it, which is why every surrender assumption on this
    product is really a maturity assumption.  The staged 学資金 of the education cell has
    the same shape in miniature — six single months, on the six anniversaries the grid
    names.

    The equation carries **no dividend term**, so it is valid only on a 無配当 design.
    :func:`dividend_type` is therefore evaluated here rather than left to a caller who
    might never ask: a model point electing the ５年ごと利差配当 variant fails on its first
    cash flow instead of being projected silently under a 有配当 label.
    """
    dividend_type()
    return (premiums(t) - claims(t) - claim_expenses(t)
            - expenses(t) - commissions(t))


def henreiritsu():
    """rho: the 返戻率, the contractual return ratio the product is sold on.

    ``(S x sum of g(k) + S) / (P x m)``.  Contractual amounts on one policy that
    survives, pays every premium, takes every benefit in cash and receives no dividend —
    **not** a rate of return, not probability-weighted, not discounted and not net of
    expenses, so it is not the ratio the cash-flow statement produces.  It is undefined
    on a policy that surrenders and unbounded on a waived one, which is why it reads the
    contractual premium term and never the projected premium income.  It also moves with
    payment frequency and volume band, so a ratio computed from a 月払 premium is a lower
    bound on a carrier's own published figure.
    """
    total = sum_assured() * (sum(benefit_schedule().values()) + 1.0)
    return total / (premium_pp() * prem_term())


# --- roll-forward and cash flow statement checks


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy month t; zero everywhere.

    ``l(t) - l(t + 1) - D(t) - (1 - wv_frac) Dp(t) - Sr(t) - R|final``, on the total
    in force ``l = l_p + h``.
    Summed over ``t`` it is the technical notes' own identity, that every policy leaves by
    exactly one route and the term is finite:
    ``sum D + sum (1 - wv_frac) Dp + sum Sr + R(n-1) = 1``.  The maturity term is non-zero
    only in the final month, where the survivors neither die nor surrender: without it
    the last row appears to lose lives with no cause.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_ph_term(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t.
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def check_pol_val_roll_fwd_resid(k):
    """The policy-value recursion residual over the policy year opening at anniversary k.

    ``(W(k) + pi 1{k < m}) (1 + i_cv) - q_tab(k) DB_val - (1 - q_tab(k)) Wb(k + 1)``:
    the value rolls from one anniversary to the next, with ``W(0) = 0``, ``q_tab`` the
    **unadjusted** table rate at ``x + k`` and ``DB_val`` the death benefit inside the EPV
    — ``S`` on the endowment cell and zero on the education cell, where the death payment
    releases the value instead of adding to it.

    **Annual, and it must stay annual.**  The policy value is built from annual actuarial
    functions on an annual basis and is defined at anniversaries; rolling it monthly would
    be checking :func:`pol_val_at_m`'s interpolation convention rather than the
    construction underneath it.

    One recursion covers both constructions, which is the point of publishing
    :func:`pol_val_db_pp`.  It also pins the timing: the premium is credited at the start
    of the policy year, interest for the whole year, the death benefit and the staged
    benefit at the end.
    """
    prev = pol_val_pp(k)
    prem = prem_net_level_pp() if k < prem_term() else 0.0
    q = mort_rate_at_age(sex(), issue_age() + k)
    return ((prev + prem) * (1.0 + i_cv)                             # noqa: F821
            - q * pol_val_db_pp(k) - (1.0 - q) * pol_val_pre_pp(k + 1))


def check_pol_val_roll_fwd():
    """True when the policy-value recursion closes over every projected policy year.

    No argument, one bool over all k; :func:`check_pol_val_roll_fwd_resid` gives the
    signed residual of the year that failed.  The tolerance scales with the sum assured,
    since the residual accumulates rounding on an amount of that size.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(k)) <= tol
               for k in range(proj_years()))


def check_pol_val_terminal_resid(k):
    """``W(n) - S`` at the final anniversary, zero at every other; zero everywhere.

    The residual is ``pol_val_pp(n) - sum_assured()`` at ``k = proj_years()``.
    The identity that makes an endowment a real test of a savings model: the policy value
    must converge on its own maturity benefit, exactly, on **both** cells.  A whole life
    reserve that drifts can hide for decades; an endowment reserve that does not converge
    is wrong on the first run.
    """
    if k != proj_years():
        return 0.0
    return pol_val_pp(k) - sum_assured()


def check_pol_val_terminal():
    """True when the policy value converges on the sum assured at anniversary ``n``.

    No argument, one bool over all k; :func:`check_pol_val_terminal_resid` gives the
    signed residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_pol_val_terminal_resid(k)) <= tol
               for k in range(proj_years() + 1))


def check_surr_charge_resid(k):
    """``reserve_pp - CV - SC`` at anniversary k; zero everywhere.

    The gap between the reference reserve and the payable surrender value is the
    acquisition deduction and nothing else, which is exactly testable because ``i_std``
    defaults to ``i_cv``.  Where the deduction would exhaust the value the surrender value
    floors at zero and the identity is not asserted, which is the one branch this residual
    reports as zero by construction rather than by arithmetic.
    """
    if pol_val_pp(k) < surr_charge_pp(k):
        return 0.0
    return reserve_pp(k) - cv_pp(k) - surr_charge_pp(k)


def check_surr_charge():
    """True when the reserve, the surrender value and the deduction reconcile everywhere.

    No argument, one bool over all anniversaries; :func:`check_surr_charge_resid` gives
    the signed residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_surr_charge_resid(k)) <= tol
               for k in range(proj_years() + 1))


def check_staged_value_resid(k):
    """``Wb(k) - W(k) - S g(k)`` at anniversary k; zero everywhere.

    Each staged benefit reduces the surrender value **by its own amount**: the payment
    comes out of the value rather than beside it, which is the sourced constraint that
    each 祝金 reduces the 解約返戻金.  A model that pays the benefit beside the value inflates
    every later surrender, and this residual is where that shows.
    """
    return (pol_val_pre_pp(k) - pol_val_pp(k)
            - sum_assured() * benefit_pct(k))


def check_staged_value():
    """True when the staged benefit comes out of the policy value at every anniversary.

    No argument, one bool over all anniversaries; :func:`check_staged_value_resid` gives
    the signed residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_staged_value_resid(k)) <= tol
               for k in range(proj_years() + 1))


def check_net_cf_resid(t):
    """The cash flow statement residual in policy month t; zero everywhere.

    :func:`net_cf` less an independent rebuild from the columns ``result_cf()``
    publishes, kind by kind.  A benefit that reached ``net_cf`` without reaching a column,
    or a column counted twice, shows up here and nowhere else.
    """
    built = (premiums(t)
             - claims(t, "DEATH") - claims(t, "STAGED") - claims(t, "MATURITY")
             - claims(t, "LAPSE") - claims(t, "PH_DEATH")
             - claim_expenses(t) - expenses(t) - commissions(t))
    return net_cf(t) - built


def check_net_cf():
    """True when the published columns reconcile to ``net_cf`` in every projected month.

    No argument, one bool over all t; :func:`check_net_cf_resid` gives the signed
    residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(proj_len()))


# --- result tables


def result_cf():
    """Result table of cash flows, indexed by the 0-based policy **month** t.

    ``t = 0`` is the first policy month and ``t = proj_len() - 1`` the last, so there are
    ``proj_len()`` rows, twelve to the policy year;
    ``df.groupby(df.index // 12).sum()`` reads it back as the annual statement.
    ``pols_if`` is the **total** start-of-month in force and the weight on that row's
    benefits; ``pols_if_pay`` is the premium-paying subset of it and the weight on that
    row's premium; ``pols_wv`` is the waived state, identically zero on the endowment
    cell.  The three satisfy ``pols_if = pols_if_pay + pols_wv`` row by row.  ``expenses``
    is acquisition plus maintenance and ``claim_expenses`` is a column of its own.
    ``net_cf`` carries the technical notes' own income-positive sign.
    ``claims_ph_death`` is a column of zeros in the base run by product design and is
    published rather than dropped; see the Space docstring.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_wv": [pols_wv(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_staged": [claims(t, "STAGED") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_ph_death": [claims(t, "PH_DEATH") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """In-force probabilities and decrement rates, indexed by the 0-based policy month t.

    Both the annual rates and the monthly decrements are published: the ``*_rate`` columns
    are the annual rates the assumption tables are stated on and the notes quote, and the
    ``*_mth`` columns the rates actually applied to the month.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_wv": [pols_wv(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_ph_decr": [pols_ph_decr(t) for t in ts],
            "pols_waived": [pols_waived(t) for t in ts],
            "pols_ph_term": [pols_ph_term(t) for t in ts],
            "pols_surv": [pols_surv(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "mort_rate_ph": [mort_rate_ph(t) for t in ts],
            "mort_rate_ph_mth": [mort_rate_ph_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """The per-policy value construction, indexed by the **anniversary** k.

    The policy value before and after the staged benefit, the acquisition deduction, the
    payable surrender value, the reference reserve, the cumulative premiums, the loan
    balance and the staged fraction.  None of these is a cash flow on its own; they are
    what the cash flow columns are built from.

    **Indexed by the anniversary, not by the month**, because that is what these
    quantities are: the contractual value construction is annual, defined at the
    年単位の契約応当日, and it did not move when the cash flow statement went monthly.  The
    frame is ``k = 0 … proj_years()``, issue and maturity included.  The value a surrender
    or a death **between** anniversaries is settled on is :func:`cv_at_m` and
    :func:`pol_val_pre_at_m`, which interpolate these columns.
    """
    ks = list(range(proj_years() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pol_val_pre_pp": [pol_val_pre_pp(k) for k in ks],
            "pol_val_pp": [pol_val_pp(k) for k in ks],
            "surr_charge_pp": [surr_charge_pp(k) for k in ks],
            "cv_pp": [cv_pp(k) for k in ks],
            "reserve_pp": [reserve_pp(k) for k in ks],
            "prem_cum_pp": [prem_cum_pp(k) for k in ks],
            "loan_pp": [loan_pp(k) for k in ks],
            "benefit_pct": [benefit_pct(k) for k in ks],
        },
        index=pd.Index(ks, name="k"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

i_cv = 0.01

i_std = 0.01

i_loan = 0.024

alpha = 0.25

dyn_lapse_beta = 2.0

dyn_lapse_cap = 3.0

expense_acq = 50000.0

expense_maint = 8000.0

expense_claim = 20000.0

inflation_rate = 0.01

comm_init_rate = 0.90

comm_renewal_rate = 0.03

roll_fwd_tol = 1e-10

val_tol = 1e-9

pd = ("Module", "pandas")
