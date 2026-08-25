# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Endowment_JP_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's 養老保険 anchor cell
    >>> Projection[2].result_cf()          # its 学資保険 cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy years**, 1-based: ``t = 1`` is the first policy year and
``t = proj_len() = policy_term()`` the last. There is nothing after it. Every state
closes at ``t = n``: ``pols_if(n + 1) = pols_if_pay(n + 1) = pols_wv(n + 1) = 0``, and
the closing cash flow is a **certain** payment of the sum assured to the survivors rather
than a decrement.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/endowment/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through modelx's
IOSpec machinery.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Endowment_JP_A.Data`, reached here through the ``data`` Reference:

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
with an uppercase ``kind`` string, ``pols_if_pay_at(t, timing)`` for the within-year
in-force reads. The technical notes use compact actuarial symbols instead. The mapping
is:

=========================  ===============================  ===============================
Notes symbol               Cells                            Meaning
=========================  ===============================  ===============================
cell                       cell()                           endowment or education
(none)                     model_point()                    The model point as a Series
x                          issue_age()                      契約年齢 of the 被保険者
y                          ph_issue_age()                   契約年齢 of the 契約者
x + t - 1                  age(t)                           Attained age of the 被保険者
y + t - 1                  age_ph(t)                        Attained age of the 契約者
n                          policy_term()                    保険期間 in years
m                          prem_term()                      保険料払込期間 in years
t = 1..n                   proj_len()                       Last policy year, = n
S                          sum_assured()                    基準保険金額
P                          premium_pp()                     Level annual premium
P x min(t, m)              prem_cum_pp(t)                   Cumulative premiums due to t
(table)                    mort_rate_at_age(sx, z)          Raw table rate, sex and age
q(t)                       mort_rate(t)                     被保険者 decrement in year t
q_p(t)                     mort_rate_ph(t)                  契約者 decrement, zero past m
mort_be_factor             mort_be_factor()                 被保険者 mortality multiplier
wv_load                    wv_load()                        契約者 mortality multiplier
wv_frac                    wv_frac()                        Fraction of 契約者 deaths waived
wv_lapse_mult              wv_lapse_mult()                  Surrender multiplier when waived
(table)                    lapse_rate_base(t)               Table surrender rate
(dynamic form)             dyn_lapse_factor(t)              Value-to-premium multiplier
w(t)                       lapse_rate(t)                    Surrender rate applied in year t
u(t)                       default_rate(t)                  Premium-default rate (APL)
g(t)                       benefit_pct(t)                   Staged 学資金 as a fraction of S
G(t)                       benefit_pct_cum(t)               Cumulative staged fraction
(schedule)                 benefit_schedule()               The whole grid as a dict
k p z                      surv_prob(z, k)                  Table survival probability
A(z, k)                    endow_epv(z, k, i)               Endowment assurance EPV of 1
a-due(z, k)                annuity_due(z, k, i)             Annuity-due of 1
EPV(t)                     edu_epv(t, i)                    Survival-benefit EPV, 学資 cell
pi, pi_g                   prem_net_level_pp()              Net level premium on i_cv
(solved rate)              implied_rate()                   Rate at which net = gross
W(t)                       pol_val_pp(t)                    保険料積立金 after any staged benefit
Wb(t)                      pol_val_pre_pp(t)                The same value before it
(EPV limb)                 pol_val_db_pp(t)                 Death benefit inside the EPV
SC(t)                      surr_charge_pp(t)                Acquisition deduction
V(t)                       surr_val_pp(t)                   Ordinary surrender value
CV(t)                      cv_pp(t)                         Payable 解約返戻金
(reserve)                  reserve_pp(t)                    平準純保険料式 reserve on i_std
DB(t)                      death_ben_pp(t)                  Death benefit for a death in t
L(t)                       loan_pp(t)                       Loan and APL principal plus interest
(advance)                  apl_advance_pp(t)                APL advance made in year t
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
R(t)                       pols_surv(t)                     In force at the anniversary
Sr(t)                      pols_lapse(t)                    Expected surrenders in year t
R(n)                       pols_maturity(t)                 Survivors who mature, at t = n
P x l_p(t)                 premiums(t)                      Premium income
DB(t) x D(t) etc.          claims(t, kind)                  Benefit outgo by kind
ec x D(t)                  claim_expenses(t)                Claim expense outgo
e(t)                       maint_expenses(t)                Maintenance expense
E0                         acq_expenses(t)                  Acquisition expense
E0 + e(t)                  expenses(t)                      Acquisition plus maintenance
c0, c_r                    commissions(t)                   Commission outgo
CF(t)                      net_cf(t)                        Net cash flow, income positive
rho                        henreiritsu()                    返戻率, the contractual ratio
=========================  ===============================  ===============================

Five names needed care.

The notes' ``W(t)`` and ``Wb(t)`` differ only on the education cell, where a staged
benefit falls due at ``t``: ``Wb`` is the value **before** that payment and ``W`` the
value after it, which is the sourced fact that each 祝金 reduces the surrender value.
:func:`pol_val_pre_pp` and :func:`pol_val_pp` keep them apart because the two feed
different things — the death benefit and the refused-waiver termination read ``Wb``, the
surrender value reads ``W`` — and a model that pays the staged benefit *beside* the value
rather than out of it inflates every later surrender.

``CV`` and ``V`` are the same series on this product. There is no 低解約返戻金型
(*tei-kaiyaku-henreikin-gata*, suppressed-surrender-value) form of either cell in any
retrieved document, so there is no ``k`` multiplier, no step at 払込満了 and no surrender
spike; :func:`surr_val_pp` and :func:`cv_pp` are both published anyway, so that the
absence of the multiplier is stated rather than left to inference.

``mort_rate`` is the projection decrement and carries :func:`mort_be_factor`; the cash-value
construction reads :func:`mort_rate_at_age` directly, unadjusted. The policy value is a
contractual quantity on the pricing basis, so a best-estimate adjustment to the
projection must not move it — and that is testable, because model point 4 carries
``mort_be_factor = 1.25`` and its policy value is identical to model point 2's.

:func:`pols_maturity` has no symbol of its own in the notes, which write the closing
payment as ``S x R(n)``. It is named so that the in-force roll-forward closes in the
final year, where the survivors neither die nor surrender: they mature.
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

The waiver runs on the **契約者's** mortality at ``y + t - 1``; every benefit runs on the
**被保険者's** at ``x + t - 1``. Reading one table at one age for both is the most likely
implementation error on the education cell — and on the endowment cell the two ages
coincide, so it would not show there.

``q_p(t) = 0`` for ``t > m`` is a modelling ruling, not an approximation. Every waiver
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
``t = n`` and there is no staged schedule at all.

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

:func:`henreiritsu` returns ``(S x sum of g(t) + S) / (P x m)``: contractual amounts on
one policy that survives, pays every premium, takes every benefit in cash and receives no
dividend. It is not probability-weighted, not discounted, not net of tax and not net of
expenses, so it is **not** the ratio the cash-flow statement produces. It is undefined on
a policy that surrenders and unbounded on a waived one, which is why it reads the
contractual premium term ``P x m`` and never the projected premium income. Computed from
a monthly premium on an annual grid it sits below the carrier's own published figure.
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
    年単位の契約応当日 rather than on the birthday, so the attained age in policy year
    ``t`` is ``x + t - 1`` exactly.  The shipped table is built on a nearest-birthday
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
    over ``t = 1 .. m`` only.
    """
    if cell() != "education":
        raise ValueError("the endowment cell has no 契約者 life")
    return int(model_point()["ph_issue_age"])


def sum_assured():
    """S: 基準保険金額, the amount every benefit is scaled from.

    On the endowment cell it is a sum assured in the ordinary sense: the death benefit,
    and the 満期保険金 paid on survival to ``t = n``, are both exactly ``S``.  On the
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


def proj_len():
    """The last projected policy year: the 保険期間, exactly.

    There is no tail and no terminal age.  Everything closes at ``t = n``, and the
    closing cash flow is a certain payment of ``S`` to the survivors rather than a
    decrement.  Importing a whole life chassis's terminal age would project a contract
    that has already matured.
    """
    return policy_term()


def age(t):
    """x + t - 1: the attained age of the 被保険者 in policy year t."""
    return issue_age() + t - 1


def age_ph(t):
    """y + t - 1: the attained age of the 契約者 in policy year t.

    Defined on the education cell only, and read only for ``t <= m``: after 払込満了 there
    is no premium to waive and the second decrement is dropped entirely.
    """
    return ph_issue_age() + t - 1


def prem_cum_pp(t):
    """P x min(t, m): cumulative premiums **due** to and including policy year t.

    Deemed-paid, not cash-paid.  On a waived policy this keeps growing although the
    policy pays nothing, because the contract provides that each future premium is
    treated as having been paid on its 契約応当日 — which is what makes the education
    cell's return-of-premiums death benefit behave the same in both states.
    """
    return premium_pp() * min(t, prem_term())


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
    """q(t): the 被保険者 mortality decrement applied in policy year t.

    The table rate at ``x + t - 1`` times :func:`mort_be_factor`, capped at 1.  It runs on
    **both** states: a waived policy is still insured.
    """
    return min(1.0, mort_rate_at_age(sex(), age(t)) * mort_be_factor())


def mort_rate_ph(t):
    """q_p(t): the 契約者 decrement driving the waiver in policy year t.

    The table rate at ``y + t - 1`` times :func:`wv_load`, and **zero for ``t > m``** —
    every waiver trigger is conditional on the event falling during 保険料払込期間, so after
    払込満了 there is nothing for the provision to do and the composite treats the contract
    as continuing through the 契約者's death by succession.  Zero throughout on the
    endowment cell, which has no second life.
    """
    if not waiver() or t > prem_term():
        return 0.0
    return min(1.0, mort_rate_at_age(ph_sex(), age_ph(t)) * wv_load())


def lapse_rate_base(t):
    """The table voluntary surrender rate in policy year t **[std]**.

    4 / 3 / 2 percent, the last row applying to every later policy year.  The shape is
    inherited from the savings chassis so that the products stay comparable.  No carrier
    publishes a lapse or surrender curve by duration for either cell — the single largest
    assumption gap on this product — and the only public benchmark, an industry
    解約・失効率 of 5.6% defined on **sum assured** across all product types, is used as a
    sanity ceiling and nothing more.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(t, int(tbl.index.max())), "lapse_rate"])


def dyn_lapse_factor(t):
    """The dynamic surrender multiplier in policy year t **[std]**; 1 in the base run.

    ``min(3, max(1, 1 + beta max(0, CV(t) / cumprem(t) - 1)))`` with ``beta = 2``.  On
    this product it never leaves 1 even when switched on, because the surrender value is
    below cumulative premiums at every duration on both cells — peaking at 92.0% at
    maturity on the endowment anchor cell.  A thirty-year 養老保険 at a 1.00% 予定利率 gives
    its owner no point at which surrendering beats persisting on value grounds alone,
    and that is the finding the module exists to produce.
    """
    if not dyn_lapse():
        return 1.0
    base = prem_cum_pp(t)
    if base <= 0.0:
        return 1.0
    return min(dyn_lapse_cap, max(                                   # noqa: F821
        1.0, 1.0 + dyn_lapse_beta * max(0.0, cv_pp(t) / base - 1.0)))  # noqa: F821


def lapse_rate(t):
    """w(t): the annual voluntary surrender rate applied at the end of policy year t.

    The table rate times the dynamic multiplier, and **zero in the final policy year**
    **[std]**.  That zero is not a rounding of a small number: a surrender at the end of
    the final year and the maturity payment fall on the same anniversary at the same
    amount, so running both double-counts the terminal payment and running the surrender
    instead of the maturity misclassifies most of the outgo into the wrong column.  An
    owner one year from a guaranteed ``S`` does not take ``CV(n) = S`` early.
    """
    if t >= proj_len():
        return 0.0
    return min(1.0, lapse_rate_base(t) * dyn_lapse_factor(t))


def default_rate(t):
    """u(t): the premium-default rate feeding the APL module; zero in the base run.

    The table rate times :func:`apl_default_mult`, and zero once premiums have ceased.  A
    default is **not** a lapse: the advance is applied to the premium and the policy stays
    in force, which is exactly the Japanese mechanic that has no analogue in the U.S. or
    UK reference sets.  It therefore moves :func:`premiums` and :func:`loan_pp` and leaves
    the in-force recursion alone.  The waived state never defaults, because there is no
    premium there to miss.
    """
    if not apl_elected() or t > prem_term():
        return 0.0
    tbl = data.lapse_table()                                         # noqa: F821
    rate = float(tbl.loc[min(t, int(tbl.index.max())), "default_rate"])
    return min(1.0, rate * apl_default_mult())


# --- the staged benefit schedule


def benefit_schedule():
    """The whole staged 学資金 grid for this model point, as ``{policy year: fraction}``.

    Read from ``benefit_schedule_table.csv`` by :func:`schedule_id`.  An empty dict on
    the endowment cell, whose ``schedule_id`` is ``none``: the survival benefit there is
    a single payment at ``t = n`` and there is no staged schedule at all.  The maturity
    benefit is never a row here — it is always present on both cells and is held
    separately, so that a schedule with no rows still matures.
    """
    sid = schedule_id()
    tbl = data.benefit_schedule_table()                              # noqa: F821
    if sid not in tbl.index:
        return {}
    sub = tbl.loc[[sid]]
    return {int(a): float(b)
            for a, b in zip(sub["t"], sub["benefit_pct"])}


def benefit_pct(t):
    """g(t): the staged 学資金 due at anniversary t, as a fraction of S.

    Zero in every year the schedule does not name, and zero throughout on the endowment
    cell.  It is a fraction of ``S``, never of a premium: on the education cell the two
    are within a factor of two of each other, so the distinction is not idle.
    """
    return benefit_schedule().get(t, 0.0)


def benefit_pct_cum(t):
    """G(t): the cumulative staged fraction paid to and including anniversary t."""
    return sum(v for k, v in benefit_schedule().items() if k <= t)


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


def edu_epv(t, i):
    """EPV(t): the education cell's survival-benefit EPV at rate ``i``, per policy in force.

    ``S x [ sum over s > t of g(s) v^(s-t) (s-t)p + v^(n-t) (n-t)p ]``.  The ``s > t``
    is what makes :func:`pol_val_pp` the value **after** the staged benefit due at ``t``,
    which is the sourced fact that each 祝金 reduces the surrender value.

    Excluding the death benefit from the EPV is the **[std]** step, and it is one
    carrier's own wording read literally: its 死亡払戻金 *is* the 責任準備金相当額, so on that
    design the decrement is exactly value-neutral, and the composite's max-form death
    benefit dominates it.
    """
    v = 1.0 / (1.0 + i)
    z = issue_age() + t
    n = policy_term()
    total = sum(g * (v ** (s - t)) * surv_prob(z, s - t)
                for s, g in benefit_schedule().items() if s > t)
    return sum_assured() * (total + (v ** (n - t)) * surv_prob(z, n - t))


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


def pol_val_at(t, i):
    """W(t) at rate ``i``: the policy value at anniversary t, after any staged benefit.

    ``S x A(x + t, n - t) - pi x a-due(x + t, m - t)`` on the endowment cell and
    ``EPV(t) - pi_g x a-due(x + t, m - t)`` on the education cell.  At ``t = n`` there is
    no future benefit beyond maturity and no future premium, so it is ``S`` exactly on
    **both** cells, by construction — the identity :func:`check_pol_val_terminal`
    asserts, and the one thing a whole life chassis can never check.
    """
    n, m = policy_term(), prem_term()
    ann = annuity_due(issue_age() + t, max(m - t, 0), i)
    if cell() == "endowment":
        return (sum_assured() * endow_epv(issue_age() + t, n - t, i)
                - prem_net_level_at(i) * ann)
    return edu_epv(t, i) - prem_net_level_at(i) * ann


def pol_val_pp(t):
    """W(t): 保険料積立金, the policy value at anniversary t on the cash-value basis.

    **After** any staged benefit due at ``t``, which is why the surrender value falls by
    exactly the amount of each 祝金 rather than beside it.  Identical in the paying and the
    waived states: the value is computed as if the premiums had been paid, so a model
    that keeps two value series is modelling a contract nobody wrote.
    """
    return pol_val_at(t, i_cv)                                       # noqa: F821


def pol_val_pre_pp(t):
    """Wb(t) = W(t) + S g(t): the policy value at anniversary t **before** the staged benefit.

    The limb the education cell's death benefit and the refused-waiver termination are
    valued on, and equal to :func:`pol_val_pp` in every year no staged benefit falls due
    and throughout on the endowment cell.
    """
    return pol_val_pp(t) + sum_assured() * benefit_pct(t)


def pol_val_db_pp(t):
    """The death benefit **inside** the cash-value basis: S on 養老, zero on 学資.

    Not a cash flow.  It exists so that :func:`check_pol_val_roll_fwd` can state one
    recursion covering both cells, and it names the structural difference between the two
    constructions: an endowment assurance carries the death benefit inside its EPV, while
    the education cell's death payment releases the value instead of adding to it.
    """
    return sum_assured() if cell() == "endowment" else 0.0


def reserve_pp(t):
    """The 平準純保険料式 policy reserve at anniversary t, on the reference rate ``i_std``.

    A reference quantity and **never a cash flow**.  The statutory 標準責任準備金 is set by
    告示 on the 標準利率 and the standard table, with 危険準備金 and 価格変動準備金 outside it
    altogether; this library projects gross cash flows and cites the valuation layers
    rather than reproducing them.  The current numeric 標準利率 could not be established
    from any retrieved official document, so ``i_std`` defaults to ``i_cv`` **[std]**,
    which makes ``reserve_pp(t) - surr_val_pp(t) = surr_charge_pp(t)`` exactly testable —
    see :func:`check_surr_charge`.
    """
    return pol_val_at(t, i_std)                                      # noqa: F821


def surr_charge_pp(t):
    """SC(t) = alpha P (m - t) / m: the acquisition deduction inside the surrender value.

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
    return alpha * premium_pp() * max(0, m - t) / m                  # noqa: F821


def surr_val_pp(t):
    """V(t) = max(0, W(t) - SC(t)): the ordinary surrender value at anniversary t."""
    return max(0.0, pol_val_pp(t) - surr_charge_pp(t))


def cv_pp(t):
    """CV(t): the payable 解約返戻金 at anniversary t.

    Equal to :func:`surr_val_pp` on this product, with **no 低解約返戻金型 multiplier**.  No
    retrieved document offers a suppressed-surrender-value form of either cell, so there
    is no ``k``, no step at 払込満了 and no surrender spike; importing a whole life chassis's
    cliff would model a product that does not exist here.  Both cells are published
    anyway so that the absence is stated rather than inferred.
    """
    return surr_val_pp(t)


def death_ben_pp(t):
    """DB(t): the death benefit for a death of the 被保険者 in policy year t.

    On the endowment cell ``S`` net of loans, level for the term and equal to the
    maturity benefit.  On the education cell
    ``max(P x min(t, m) - S G(t - 1) - L(t), Wb(t))`` — a **return of premiums** floored
    at the policy value, where the premium limb is deemed-paid and the staged benefits
    already received are deducted.

    **Both limbs must be evaluated.**  On the composite's basis the value limb dominates
    at every duration on the education anchor cell, so the ``max`` never switches — but
    that is a property of that cell's negative loading and not of the contract, and a
    point with a positive loading binds the other way.  Hard-coding either limb passes on
    one cell and fails on the next.
    """
    if cell() == "endowment":
        return sum_assured() - loan_pp(t)
    refund = (prem_cum_pp(t) - sum_assured() * benefit_pct_cum(t - 1) - loan_pp(t))
    return max(refund, pol_val_pre_pp(t))


# --- the loan and the automatic premium loan


def apl_advance_pp(t):
    """The 自動振替貸付 advance made at the start of policy year t; zero in the base run.

    ``P u(t)``, capped at the surrender value still free of loan.  The advance is applied
    to the premium, so the premium is not collected in cash and appears only as growth in
    :func:`loan_pp`.  The exhaustion test and the clawback belong to the whole life
    chassis, where they are exercised in both positions; the cap here is what keeps the
    loan from exceeding the value that secures it.
    """
    if t > prem_term():
        return 0.0
    return min(premium_pp() * default_rate(t),
               max(0.0, cv_pp(t) - loan_pp(t)))


def loan_pp(t):
    """L(t): 契約者貸付 and APL principal with interest, at the **start** of policy year t.

    ``pol_loan_util x CV(1)`` drawn at outset **[std]**, then
    ``L(t + 1) = (L(t) + advance(t)) (1 + i_loan)``.  Identically zero in the base run,
    where nothing is drawn and nothing is defaulted.  It produces no cash flow of its own:
    it nets off the death benefit and the surrender benefit, which is why every benefit in
    the base run is gross.
    """
    if t <= 1:
        return pol_loan_util() * cv_pp(1)
    return (loan_pp(t - 1) + apl_advance_pp(t - 1)) * (1.0 + i_loan)  # noqa: F821


# --- in force


def pols_if(t):
    """l(t): the **total** in-force probability at the start of policy year t.

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
    """l_p(t): the in-force probability in the **premium-paying** state at year t's start.

    ``l_p(1) = 1``, then ``l_p(t + 1) = l_p_after(t) (1 - w(t))`` where ``l_p_after`` is
    net of both mortality decrements.  This is the weight on the premium and the renewal
    commission of the same ``result_cf()`` row, and the strict subset of :func:`pols_if`
    that is still paying.  Zero outside ``1 .. proj_len()``: the contract has not
    started, or it has matured.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return 1.0
    return pols_if_pay_at(t - 1, "AFT_DECR")


def pols_wv(t):
    """h(t): the in-force probability in the **waived** state at the start of year t.

    ``h(1) = 0``, and identically zero on the endowment cell, which has no waiver.  A
    waived policy pays no premium and earns the distributor no renewal commission, but it
    still costs the insurer administration and it still receives every benefit — which is
    why the maintenance expense runs on both states and the renewal commission on one.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return 0.0
    return pols_wv_at(t - 1, "AFT_DECR")


def pols_if_pay_at(t, timing):
    """The premium-paying in-force probability at a point inside policy year t.

    ``"BEF_DECR"``
        l_p(t), the start of the year, before any decrement; the same number as
        :func:`pols_if_pay` and the weight on that year's premium.

    ``"BEF_LAPSE"``
        ``l_p(t) (1 - q(t)) (1 - q_p(t))`` — after **both** mortality decrements, which is
        the population surrenders are taken from.  The processing order is 被保険者 death,
        then 契約者 decrement, then the staged benefit, then maturity, then surrender.

    ``"AFT_DECR"``
        l_p(t + 1), the end-of-year state, and zero from ``proj_len()`` on because
        everything closes at the end of the term.
    """
    if timing == "BEF_DECR":
        return pols_if_pay(t)
    if timing == "BEF_LAPSE":
        return pols_if_pay(t) * (1.0 - mort_rate(t)) * (1.0 - mort_rate_ph(t))
    if timing == "AFT_DECR":
        if t < 1 or t >= proj_len():
            return 0.0
        return pols_if_pay_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing: " + str(timing))


def pols_wv_at(t, timing):
    """The waived-state in-force probability at a point inside policy year t.

    ``"BEF_DECR"``
        h(t), the start of the year.

    ``"BEF_LAPSE"``
        ``h(t) (1 - q(t)) + wv_frac x Dp(t)`` — the survivors of the insured's mortality
        plus this year's transitions in.  Only the qualifying fraction arrives; the rest
        terminates the contract instead.

    ``"AFT_DECR"``
        h(t + 1), after a surrender rate of ``wv_lapse_mult x w(t)``, and zero from
        ``proj_len()`` on.
    """
    if timing == "BEF_DECR":
        return pols_wv(t)
    if timing == "BEF_LAPSE":
        return pols_wv(t) * (1.0 - mort_rate(t)) + pols_waived(t)
    if timing == "AFT_DECR":
        if t < 1 or t >= proj_len():
            return 0.0
        return pols_wv_at(t, "BEF_LAPSE") * (
            1.0 - min(1.0, wv_lapse_mult() * lapse_rate(t)))
    raise ValueError("invalid timing: " + str(timing))


def pols_if_at(t, timing):
    """The **total** in-force probability at a point inside policy year t.

    ``pols_if_pay_at(t, timing) + pols_wv_at(t, timing)`` — the library-wide within-year
    read, on the whole surviving block rather than on one state.  The two states are read
    separately by :func:`pols_if_pay_at` and :func:`pols_wv_at`, because only the
    premium-paying one carries the premium and the renewal commission.

    ``"BEF_DECR"``
        l(t), the start of the year, before any decrement; the same number as
        :func:`pols_if` and the weight on that ``result_cf()`` row.

    ``"BEF_LAPSE"``
        the anniversary population after **both** mortality decrements and before
        surrender — the same number as :func:`pols_surv`, which is what the staged
        benefit and the maturity benefit are paid to.

    ``"AFT_DECR"``
        l(t + 1), the end-of-year state, and zero from ``proj_len()`` on because
        everything closes at the end of the term.

    An invalid ``timing`` raises ``ValueError`` from the two state cells rather than
    returning a number.
    """
    return pols_if_pay_at(t, timing) + pols_wv_at(t, timing)


def pols_death(t):
    """D(t) = l(t) q(t): expected 被保険者 deaths in policy year t.

    On the **total** in force, paying and waived together: a waived policy is still
    insured, and the 高度障害 trigger is inside the table rate rather than beside it.
    """
    return pols_if(t) * mort_rate(t)


def pols_ph_decr(t):
    """Dp(t) = l_p(t) (1 - q(t)) q_p(t): expected 契約者 decrements in policy year t.

    On the **premium-paying state only**, and zero for ``t > m``: a policy already waived
    has no premium left to waive, and after 払込満了 the provision has nothing to act on.
    """
    return pols_if_pay(t) * (1.0 - mort_rate(t)) * mort_rate_ph(t)


def pols_waived(t):
    """wv_frac x Dp(t): transitions into the waived state at the end of policy year t.

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
    """R(t): the expected in force at the anniversary, after mortality, before surrender.

    ``l_p_after(t) + h_after(t)``.  This is what the staged benefit and the maturity benefit
    are paid to, in **both** states.
    """
    return pols_if_pay_at(t, "BEF_LAPSE") + pols_wv_at(t, "BEF_LAPSE")


def pols_lapse(t):
    """Sr(t): expected surrenders at the end of policy year t.

    ``l_p_after(t) w(t) + h_after(t) wv_lapse_mult w(t)``, taken from the survivors of both
    mortality decrements and valued on the surrender value **net of the staged benefit
    just paid**.  Zero in the final policy year, where :func:`lapse_rate` is zero.
    """
    return (pols_if_pay_at(t, "BEF_LAPSE")
            + pols_wv_at(t, "BEF_LAPSE") * wv_lapse_mult()) * lapse_rate(t)


def pols_maturity(t):
    """R(n) at ``t = n`` and zero in every other year: the survivors who mature.

    The maturity benefit is **certain, not a decrement**: at ``t = n`` the survivors are
    paid ``S`` with probability 1.  Modelling maturity as a rate, or letting the
    projection run past ``t = n``, is wrong in both directions.  It is named separately so
    that the in-force roll-forward closes in the final year, where the survivors neither
    die nor surrender.
    """
    if t != proj_len():
        return 0.0
    return pols_surv(t)


# --- cash flows


def premiums(t):
    """Premium income at the start of policy year t, an inflow.

    ``P l_p(t)`` for ``t <= m``, less anything advanced under the automatic premium loan,
    which is not collected in cash.  Carried on :func:`pols_if_pay` alone and never on
    :func:`pols_if`: the waived state is in force and pays nothing.
    """
    if t > prem_term():
        return 0.0
    return (premium_pp() - apl_advance_pp(t)) * pols_if_pay(t)


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``max(0, DB(t)) D(t)``, at the end of the policy year of death, on both states.

    ``"STAGED"``
        ``S g(t) R(t)``, the staged 学資金 due at this anniversary, paid on survival to
        everything in force in **both** states.  It is not a decrement and it terminates
        nothing.  Zero throughout on the endowment cell.

    ``"MATURITY"``
        ``S R(n)`` at ``t = n`` and zero elsewhere — a certain payment, not a rate.

    ``"LAPSE"``
        ``max(0, CV(t) - L(t)) Sr(t)``, valued net of the staged benefit just paid.

    ``"PH_DEATH"``
        ``Wb(t) (1 - wv_frac) Dp(t)``: the policy value paid to the 契約者's heirs where a
        waiver carve-out terminates the contract.  Identically **zero** in the base run,
        and published as a column of zeros because the zero is the product fact.
    """
    if kind is None:
        return sum(claims(t, k) for k in
                   ("DEATH", "STAGED", "MATURITY", "LAPSE", "PH_DEATH"))
    if kind == "DEATH":
        return max(0.0, death_ben_pp(t)) * pols_death(t)
    if kind == "STAGED":
        return sum_assured() * benefit_pct(t) * pols_surv(t)
    if kind == "MATURITY":
        return sum_assured() * pols_maturity(t)
    if kind == "LAPSE":
        return max(0.0, cv_pp(t) - loan_pp(t)) * pols_lapse(t)
    if kind == "PH_DEATH":
        return pol_val_pre_pp(t) * pols_ph_term(t)
    raise ValueError("invalid kind: " + str(kind))


def claim_expenses(t):
    """ec D(t): the claim handling expense on the year's death claims **[std]**.

    A flat amount per death claim, uninflated, and a cells and a ``result_cf()`` column
    of its own.  :func:`expenses` carries acquisition and maintenance only and
    :func:`net_cf` deducts this line explicitly beside it, so that ``expenses`` means one
    thing across the library — a per-policy servicing cost, never a per-claim one — and
    the technical notes' worked example prints the two as two columns.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def maint_expenses(t):
    """e(t): the inflating maintenance expense in policy year t **[std]**.

    Per policy per year to ``t = n``, inflating from issue, and carried on **both**
    states: a waived policy costs the insurer administration although it pays the
    distributor nothing.  There is no separate maturity or staged-benefit expense; both
    are folded in here.
    """
    return (expense_maint * (1.0 + inflation_rate) ** (t - 1)        # noqa: F821
            * pols_if(t))


def acq_expenses(t):
    """E0: the acquisition expense per policy at issue **[std]**; zero after policy year 1.

    No carrier publishes an expense basis at all — 予定事業費率 is named in the
    保険契約者保護機構 boilerplate and never quantified — so this and every other expense level
    is inherited unchanged from the savings chassis so that the products stay comparable.
    """
    return expense_acq * pols_if_pay(t) if t == 1 else 0.0               # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in policy year t: the **policy** expenses only.

    Maintenance, and at ``t = 1`` the acquisition expense as well.  The claim handling
    expense is **not** in here: it is a per-claim cost rather than a per-policy one, it
    lives in :func:`claim_expenses`, :func:`net_cf` deducts it explicitly, and it is
    published as its own ``claim_expenses`` column.  Folding it in here is how two models
    come to publish an ``expenses`` column that cannot be compared.
    """
    return acq_expenses(t) + maint_expenses(t)


def commissions(t):
    """Commission outgo in policy year t **[std]**.

    The initial commission at issue, then renewal commission on the premium in years
    2 .. m — on the **premium-paying state only**.  That the renewal commission runs on
    one state while the maintenance expense runs on both is not a detail: a waived policy
    costs the insurer administration and pays the distributor nothing.
    """
    init = comm_init_rate * premium_pp() * pols_if_pay(t) if t == 1 else 0.0  # noqa: F821
    renew = (comm_renewal_rate * premium_pp() * pols_if_pay(t)           # noqa: F821
             if 2 <= t <= prem_term() else 0.0)
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy year t, **income positive**.

    Premiums less death claims, the refused-waiver termination, the staged benefit, the
    maturity benefit, surrender benefits, the claim handling expense, maintenance and
    acquisition expense and commission.  The claim expense is deducted explicitly rather
    than through :func:`expenses`, which carries acquisition and maintenance only.  This
    is the technical notes' own sign, which is also the library-wide convention, so there
    is no outgo-positive ``liability_cf`` companion to publish.

    The shape to expect is a deep new business strain in year 1, then thin positive
    margins, then **one very large negative year at maturity**: on the endowment anchor
    cell the maturity payment is the largest single item in the stream and it is one year
    wide.  Unlike a behavioural cliff it is a certain payment; the only uncertainty in it
    is how many policies reach it, which is why every surrender assumption on this product
    is really a maturity assumption.

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

    ``(S x sum of g(t) + S) / (P x m)``.  Contractual amounts on one policy that
    survives, pays every premium, takes every benefit in cash and receives no dividend —
    **not** a rate of return, not probability-weighted, not discounted and not net of
    expenses, so it is not the ratio the cash-flow statement produces.  It is undefined
    on a policy that surrenders and unbounded on a waived one, which is why it reads the
    contractual premium term and never the projected premium income.  It also moves with
    payment frequency and volume band, so a ratio computed from a 月払 premium on an annual
    grid is a lower bound on a carrier's own published figure.
    """
    total = sum_assured() * (sum(benefit_schedule().values()) + 1.0)
    return total / (premium_pp() * prem_term())


# --- roll-forward and cash flow statement checks


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``l(t) - l(t + 1) - D(t) - (1 - wv_frac) Dp(t) - Sr(t) - R(n)|t=n``, on the total
    in force ``l = l_p + h``.
    Summed over ``t`` it is the technical notes' own identity, that every policy leaves by
    exactly one route and the term is finite:
    ``sum D + sum (1 - wv_frac) Dp + sum Sr + R(n) = 1``.  The maturity term is non-zero
    only in the final year, where the survivors neither die nor surrender: without it the
    last year appears to lose lives with no cause.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_ph_term(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    The library-wide form of a roll-forward check: no argument, one bool over all t.
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the year that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pol_val_roll_fwd_resid(t):
    """The policy-value recursion residual at anniversary t; zero everywhere.

    ``(W(t-1) + pi 1{t <= m}) (1 + i_cv) - q_tab(t) DB_val(t) - (1 - q_tab(t)) Wb(t)``,
    with ``W(0) = 0``, ``q_tab`` the **unadjusted** table rate and ``DB_val`` the death
    benefit inside the EPV — ``S`` on the endowment cell and zero on the education cell,
    where the death payment releases the value instead of adding to it.

    One recursion covers both constructions, which is the point of publishing
    :func:`pol_val_db_pp`.  It also pins the timing: the premium is credited at the start
    of the year, interest for the whole year, the death benefit and the staged benefit at
    the end.
    """
    prev = pol_val_pp(t - 1) if t > 1 else 0.0
    prem = prem_net_level_pp() if t <= prem_term() else 0.0
    q = mort_rate_at_age(sex(), age(t))
    return ((prev + prem) * (1.0 + i_cv)                             # noqa: F821
            - q * pol_val_db_pp(t) - (1.0 - q) * pol_val_pre_pp(t))


def check_pol_val_roll_fwd():
    """True when the policy-value recursion closes at every anniversary.

    No argument, one bool over all t; :func:`check_pol_val_roll_fwd_resid` gives the
    signed residual of the year that failed.  The tolerance scales with the sum assured,
    since the residual accumulates rounding on an amount of that size.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_pol_val_terminal_resid(t):
    """``W(n) - S`` in the final policy year, zero in every other; zero everywhere.

    The identity that makes an endowment a real test of a savings model: the policy value
    must converge on its own maturity benefit, exactly, on **both** cells.  A whole life
    reserve that drifts can hide for decades; an endowment reserve that does not converge
    is wrong on the first run.
    """
    if t != proj_len():
        return 0.0
    return pol_val_pp(t) - sum_assured()


def check_pol_val_terminal():
    """True when the policy value converges on the sum assured at ``t = n``.

    No argument, one bool over all t; :func:`check_pol_val_terminal_resid` gives the
    signed residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_pol_val_terminal_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_surr_charge_resid(t):
    """``reserve_pp(t) - CV(t) - SC(t)`` at anniversary t; zero everywhere.

    The gap between the reference reserve and the payable surrender value is the
    acquisition deduction and nothing else, which is exactly testable because ``i_std``
    defaults to ``i_cv``.  Where the deduction would exhaust the value the surrender value
    floors at zero and the identity is not asserted, which is the one branch this residual
    reports as zero by construction rather than by arithmetic.
    """
    if pol_val_pp(t) < surr_charge_pp(t):
        return 0.0
    return reserve_pp(t) - cv_pp(t) - surr_charge_pp(t)


def check_surr_charge():
    """True when the reserve, the surrender value and the deduction reconcile in every year.

    No argument, one bool over all t; :func:`check_surr_charge_resid` gives the signed
    residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_surr_charge_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_staged_value_resid(t):
    """``Wb(t) - W(t) - S g(t)`` at anniversary t; zero everywhere.

    Each staged benefit reduces the surrender value **by its own amount**: the payment
    comes out of the value rather than beside it, which is the sourced constraint that
    each 祝金 reduces the 解約返戻金.  A model that pays the benefit beside the value inflates
    every later surrender, and this residual is where that shows.
    """
    return (pol_val_pre_pp(t) - pol_val_pp(t)
            - sum_assured() * benefit_pct(t))


def check_staged_value():
    """True when the staged benefit comes out of the policy value in every year.

    No argument, one bool over all t; :func:`check_staged_value_resid` gives the signed
    residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_staged_value_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_net_cf_resid(t):
    """The cash flow statement residual in policy year t; zero everywhere.

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
    """True when the published columns reconcile to ``net_cf`` in every projected year.

    No argument, one bool over all t; :func:`check_net_cf_resid` gives the signed
    residual.
    """
    tol = val_tol * max(1.0, sum_assured())                        # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


# --- result tables


def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the **total** start-of-year in force and the weight on that row's
    benefits; ``pols_if_pay`` is the premium-paying subset of it and the weight on that
    row's premium; ``pols_wv`` is the waived state, identically zero on the endowment
    cell.  The three satisfy ``pols_if = pols_if_pay + pols_wv`` row by row.  ``expenses``
    is acquisition plus maintenance and ``claim_expenses`` is a column of its own.
    ``net_cf`` carries the technical notes' own income-positive sign.
    ``claims_ph_death`` is a column of zeros in the base run by product design and is
    published rather than dropped; see the Space docstring.
    """
    ts = list(range(1, proj_len() + 1))
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
    """Result table of in-force probabilities and decrement rates, indexed by policy year t."""
    ts = list(range(1, proj_len() + 1))
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
            "mort_rate_ph": [mort_rate_ph(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the per-policy value construction, indexed by policy year t.

    The policy value before and after the staged benefit, the acquisition deduction, the
    payable surrender value, the reference reserve, the death benefit and the loan
    balance.  None of these is a cash flow on its own; they are what the cash flow columns
    are built from.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pol_val_pre_pp": [pol_val_pre_pp(t) for t in ts],
            "pol_val_pp": [pol_val_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "reserve_pp": [reserve_pp(t) for t in ts],
            "death_ben_pp": [death_ben_pp(t) for t in ts],
            "prem_cum_pp": [prem_cum_pp(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
            "benefit_pct": [benefit_pct(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
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
