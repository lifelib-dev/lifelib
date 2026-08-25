# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.FXWholeLife_JP_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the month beginning at issue and
``t = proj_len() - 1`` the last projected month. The step is the 月単位の契約応当日, not the
calendar month end. There is no maturity date and no 満期保険金: the horizon is the
terminal age of the mortality table, ``proj_len() = 12 (omega - x + 1)`` months, and at
``t = proj_len() - 1`` the table's rate is 1, so the projection ends with nobody left
and no tail states.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/fx_whole_life/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``FXWholeLife_JP_S`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.FXWholeLife_JP_S.Data`, reached here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
charge_table_file       data.charge_table()             charge_table.csv
fx_path_file            data.fx_path_table()            fx_path_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for annual rates with ``*_rate_mth`` for their monthly
equivalents, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase
``kind`` string, ``av_pp_at(t, timing)`` and ``pols_if_at(t, timing)`` for the
within-month reads. The technical notes use compact actuarial symbols instead. The
mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
(model point row)          model_point()                   The selected model point
(shape)                    shape()                         LEVEL or SINGLE
x                          issue_age()                     契約年齢, 満年齢 at 契約日
x + floor(t/12)            age(t)                          Attained age in month t
(none)                     sex()                           M or F
omega                      omega_age()                     Terminal age of the table
T = 12(omega - x + 1)      proj_len()                      Projected months
n                          prem_months_eff()               保険料払込期間 in months
SA                         sum_assured()                   基本保険金額
P                          prem_due_pp(t)                  Premium due at the start of t
(single premium)           single_premium()                一時払保険料
i0                         guar_floor()                    最低保証積立利率 / 予定利率
ic                         credit_rate()                   Declared 積立利率
j                          credit_rate_mth()               (1 + ic)^(1/12) - 1
(none)                     guar_floor_mth()                (1 + i0)^(1/12) - 1
q(t)                       mort_rate(t)                    Annual decrement, incl. 高度障害
q_m(t)                     mort_rate_mth(t)                Monthly decrement
(charge basis)             coi_rate(t)                     Unadjusted table rate
(charge basis)             coi_rate_mth(t)                 Monthly charge rate
w(t)                       lapse_rate(t)                   Annual surrender rate
w_m(t)                     lapse_rate_mth(t)               Monthly surrender rate
(dynamic module)           lapse_dyn_factor(t)             FX-driven surrender multiplier
l(t)                       pols_if(t)                      In force at the start of t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
(none)                     pols_payer(t)                   In force and paying premium
(APL cohort)               pols_if_apl(t)                  Carried by the 自動振替貸付
(APL balance)              loan_pp(t)                      Average advance per APL policy
D(t)                       pols_death(t)                   Expected death / 高度障害 claims
S(t)                       pols_lapse(t)                   Expected surrenders
(target hit)               pols_target(t)                  Policies reaching the 目標値
phi(t)                     prem_charge_rate(t)             契約初期費用 rate on the premium
mu                         maint_rate()                    維持費率 p.a. of the 積立金
C_init(t)                  charge_init(t)                  契約初期費用 taken in month t
C_maint(t)                 charge_maint(t)                 維持費 taken in month t
C_coi(t)                   charge_coi(t)                   保障部分 charge on the 危険保険金額
P - C_init                 prem_to_av_pp(t)                Premium credited to the 積立金
AV(t)                      av_pp(t)                        積立金 at the start of month t
AVg(t) and after           av_pp_at(t, timing)             AFT_PREM / AFT_CHARGE / AFT_INT
AV0(t)                     av0_pp(t)                       The same fund at i0
(prospective AV0)          av0_pro_pp(t)                   The 予定利率 prospective fund
特別積立金                   special_reserve_pp(t)           Ten- and twenty-year top-up
IDB(t)                     idb_pp(t)                       増加死亡保険金額
DB(t)                      benefit_pp(t)                   Death benefit per policy
sc(t)                      surr_charge_rate(t)             解約控除率
rem(t)                     mva_rem(t)                      Years left in 積立利率適用期間
Delta(t)                   mva_delta(t)                    Rate move since the rate was set
mva(t)                     mva_rate(t)                     市場価格調整率, can be negative
kl(t)                      low_cv_rate(t)                  低解約返戻金割合
CV(t)                      cv_pp(t)                        解約返戻金
e(t)                       fx_rate(t)                      Reference TTM, yen per US$1
s                          fx_spread()                     為替手数料 spread, each way
g                          target_g()                      目標値, a multiple of yen paid
(target test)              target_hit(t)                   Yen-converted CV has reached it
(target test)              target_month()                  The month it is first reached
P l_p(t)                   premiums(t)                     Premium income
DB D, CV S                 claims(t, kind)                 DEATH and LAPSE outgo
(conversion)               conversions(t)                  Value leaving on a target hit
ec D(t)                    claim_expenses(t)               Claim expense, its own column
E0, e_m(t)                 expenses(t)                     Acquisition + maintenance
c0, c_r                    commissions(t)                  Commission outgo
CF(t)                      net_cf(t)                       Net cash flow, income positive
CF_JPY(t)                  net_cf_jpy(t)                   The three-rate yen translation
s (premiums + benefits)    fx_spread_jpy(t)                Spread income, published apart
=========================  ==============================  ==========================

.. rubric:: The policy currency is the model currency

Every state variable, every assumption and every cash-flow column above is in **US
dollars**. Yen enters only through :func:`fx_rate` and :func:`fx_spread`, and the
exchange rate is a model point column, never a literal in a formula: an exchange rate
buried in a recursion is an economic assumption disguised as a product feature and
cannot be varied by the point that owns it.

The yen ledger is **three translations, not one**. Premiums cross at ``e + s`` under the
円入金特約, benefits at ``e - s`` under the 円支払特約, and expenses and commission at the
plain ``e``, because they are the insurer's own costs and never cross the policyholder
boundary. So

    net_cf_jpy(t) != net_cf(t) x fx_rate(t)

identically, and the difference is the insurer's spread income. :func:`fx_spread_jpy`
publishes it as its own column rather than letting it hide inside a translated net
figure: on the anchor cell it is ¥125.17 in month 0 and ¥39,266 over the whole run.
:func:`check_fx_ledger` asserts the identity
``net_cf_jpy = net_cf x fx_rate + fx_spread_jpy`` in every month.

.. rubric:: The account-value charges are not cash flows

:func:`charge_init`, :func:`charge_maint` and :func:`charge_coi` are internal transfers
from the 積立金 to the insurer. They move :func:`av_pp` and appear **nowhere** in
:func:`net_cf`; the insurer's outgo is the expense and commission stream instead.
Booking a charge as revenue alongside the premium that funded it double-counts the
premium. :func:`check_net_cf` rebuilds :func:`net_cf` from the published columns alone
and would catch it.

The order inside the month is fixed, because it changes the answer at the third decimal
and the published surrender-value run is reproduced to the dollar: premium in, then
:func:`charge_init`, then :func:`charge_maint`, then :func:`charge_coi` on the net
amount at risk measured *after* the maintenance charge, then interest at
``(1 + ic)^(1/12)`` — the geometric twelfth root **[std]**, not ``ic/12``.

.. rubric:: Two mechanics that vanish at the guaranteed floor

The base run credits at ``ic = i0``, the contract's own 予定利率, which is the guaranteed
column of the only published surrender-value run and the only crediting figure for this
shape that is a contract term. Under the **[std]** definition of :func:`av0_pp` — the
account value the *same* recursion produces with ``ic`` replaced by ``i0`` and the
benchmark benefit held at ``SA`` — the fund and its benchmark coincide identically, so
:func:`idb_pp` is zero for every ``t`` and :func:`special_reserve_pp` with it. The
published guaranteed column shows 特別積立金 of (0) at both 10 and 20 years, so that is
what a correct implementation must produce: **a non-zero uplift or top-up on the
guaranteed run is a bug, not a refinement.**

The alternative reading of ``AV0`` — the prospective fund at ``i0`` needed to carry
``SA`` with no future premiums on the same charge basis — is implemented as
:func:`av0_pro_pp` and selected by ``idb_basis = "prospective"`` on the model point. It
does not give an identically zero uplift: on the anchor cell it gives ``AV - AV0`` of
-US$22,044.31 at ten years, **+US$36.52** at 払込満了, +US$296.03 at fifty years and
+US$30,762.05 at the terminal month. The near-zero crossing at 払込満了 is a strong
independent check on the back-solved charge stack — actuarial equivalence predicts a
contract that is almost exactly self-funding at the floor — but a definition that
manufactures a positive uplift on the guaranteed run contradicts the one document that
shows the guaranteed run, so it is the switch and not the base.

.. rubric:: The surrender layer, and what is not a charge

``CV = AV (1 - mva - sc) kl``, and all three factors can be active at once on the
SINGLE shape. Paying a surrender on :func:`av_pp` instead of :func:`cv_pp` overstates
every early exit by up to 7% plus the adjustment.

:func:`surr_charge_rate` **is** a charge: one-sided, never adding value, 7.0% in policy
year 1 falling 0.7 points per completed policy year to zero at ten, constant within the
year, and applied to the **積立金**. Three different bases are in use across the market —
the account value, the 責任準備金 and the 基本保険金額 — and a rate quoted against one means
nothing against another.

:func:`mva_rate` is **not** a charge. It is symmetric, it can be negative, and a fall in
rates **increases** the surrender value; implementing it floored at zero models a
different product. It is zero on the whole LEVEL shape, zero on an 積立利率計算基準日 and zero
inside a one-year 積立利率適用期間 — a discontinuity a monthly model has to place on the
right month. The reconstruction

    mva(t) = 1 - (1 + (Delta(t) + A) / (1 + r0)) ^ (-d rem(t))

is a **[std]** fit to the published 15-year rate table. Two structural facts drop out of
the fit rather than being imposed: the zero column sits at ``Delta = -0.1%``, which is
what ``A`` is, so a contract surrendered with no rate move at all still carries a small
positive adjustment; and the effective duration is ``d rem``, 0.70 of the remaining
term rather than the remaining term itself.

:func:`low_cv_rate` is a **cliff**: 0.70 while four or more premium-paying years remain,
stepping to 0.775, 0.85 and 0.925 at three, two and one, and to 1.00 at 払込満了, on whole
remaining years rounded **up**. Interpolating across the boundary is wrong.

.. rubric:: mort_be_factor moves the decrement and never the charge

``mort_be_factor`` is an experience assumption and multiplies :func:`mort_rate` only.
:func:`coi_rate` reads the same table **unadjusted**, because the cost-of-insurance
basis is a pricing element the insurer sets in its 算出方法書. Wiring one lever to both is
the easiest way to make this model self-consistent and wrong: raising
``mort_be_factor`` would then raise claims *and* raise the charge that funds them, and
the account value would
absorb the sensitivity instead of the cash flow showing it. Model point 7 runs
``mort_be_factor = 1.20`` and the two rates part company there.

.. rubric:: Modules that are off in the base run

Seven of the notes' optional constructions are implemented and switched off on the anchor
cell, so that the base run reproduces the worked example while the machinery stays
visible and testable:

- **The prospective uplift basis**, ``idb_basis = "prospective"``, described above; the
  base is ``"fund"``. Model point 7.
- **The uplift ratchet**, ``idb_ratchet``, which holds :func:`idb_pp` at its running
  maximum. It is *on* in the base run and makes no difference there, because the uplift
  is identically zero; it is sourced to the ご契約のしおり and not to the extracted 約款 text,
  so it is carried as a switch and turned off on model point 7.
- **The 低解約返戻金特則**, ``low_cv``, the four-step suppression ramp with its cliff at
  払込満了. Model points 2 and 6.
- **The 自動振替貸付**, ``apl_on``. A policy does not lapse while its surrender value can
  advance the premium, so ``apl_nonpay_share`` of the surrender decrement is
  **redirected** into :func:`pols_if_apl` rather than lost while the fund can carry it;
  the advance accumulates at ``apl_int_rate`` in :func:`loan_pp` and is repaid out of
  whatever the policy is eventually paid. Applying a lapse rate to unpaid premiums
  without first running that test models a decrement the contract does not have. The
  split of the surrender decrement into voluntary and non-payment parts is **[std]** —
  no source separates them — and the cohort's loan is carried as an average rather than
  as a full triangle, which is exact in aggregate. The module is **structurally absent**
  on the SINGLE shape: there is no premium to advance, so the two shapes have different
  decrement *sets*, not merely different rates. Model point 6.
- **Dynamic surrender on the FX rate**, ``dyn_lapse``. The economically natural driver
  on this product is the currency rather than the crediting rate: a policyholder in yen
  profit surrenders, one in yen loss holds on. SINGLE only. Model point 4.
- **An FX path**, ``fx_path``, reading ``fx_path_table.csv`` by policy year instead of
  holding the model point's ``fx_ttm`` flat. Model point 7.
- **The target-value rider**, ``target_on`` with ``target_action``, which converts or
  surrenders the contract at :func:`target_month`. ``target_action`` has **no default**
  where the rider is elected, and the rubric below says why a deterministic run cannot
  choose one. Model points 3 (convert) and 4 (surrender).

.. rubric:: The target-value rider is priced at intrinsic only

:func:`target_month` is the first month at or after the contractual one-year dead zone
at which the **yen-converted surrender value** reaches the 目標額. Two things about that
test are easy to get wrong and both are contractual. It runs on :func:`cv_pp`, after FX
and after the MVA, not on :func:`av_pp`: on the base SINGLE cell testing the account
value converts at month 39 against month 52, thirteen months early, and the error grows
with any rate move. And the one-year dead zone is real — a target reached inside the
first year does not trigger, and a model that converts at month 6 has invented a
contract term.

``target_action`` has **no default**, because the contract and the evidence disagree and
neither is the modeller's to assume silently. The 約款 converts the contract to a yen
whole life; the observed population surrenders on the hit and buys the same product
again, paying the front-loaded commission twice. Under ``"surrender"`` the value leaves
through :func:`claims` ``(t, "LAPSE")``; under ``"convert"`` it leaves through
:func:`conversions`, and the yen contract it becomes is out of scope — this model's
ledger is denominated in dollars and the converted liability is not. That scope boundary
is **[std]** and is why the two elections differ in where the money is booked rather
than in how much of it there is.

What a deterministic run cannot do is value the *option*. On one path the rider either
converts at one determinate month or never converts, so its time value is zero by
construction. A scenario set is the only instrument that can price it and this library
does not ship one.

.. rubric:: Sign convention

The notes' ``CF(t)`` is already **income positive** — premiums less claims, surrender
benefits, expenses and commission — which is the library-wide sign of :func:`net_cf`, so
there is no outgo-positive ``liability_cf`` companion to publish: one stream, one sign,
one name.
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


def shape():
    """The contract shape: ``LEVEL`` (平準払 積立利率変動型) or ``SINGLE`` (一時払 積立利率更改型).

    The two shapes share the whole account-value recursion and differ in the premium
    stream, the rate-reset cycle, the presence of the 市場価格調整 and the relation of the
    death benefit to the fund.  A third market shape, a level *yen* premium converted
    to US dollars each month, is a different cash-flow object and is out of scope; a
    model point naming it is rejected here.
    """
    v = model_point()["shape"]
    if v not in ("LEVEL", "SINGLE"):
        raise ValueError("invalid shape: " + str(v))
    return v


def sex():
    """The sex (M / F) of the insured; the two are rated separately [S2]."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex: " + str(v))
    return v


def issue_age():
    """x: the 契約年齢 at 契約日, 満年齢 with the fractional year discarded.

    The age increments on the 年単位の契約応当日, so the attained age in month ``t`` is
    ``x + floor(t/12)`` exactly.  生保標準生命表2018（死亡保険用）is built on a 保険年齢
    (nearest-birthday) basis and is read here at the 満年齢 attained age with no
    adjustment **[std]**, as the savings chassis does.
    """
    return int(model_point()["issue_age"])


def currency():
    """The operating currency; USD on every shipped model point.

    Only USD and AUD are inside the 標準責任準備金 regime and the published run-off tables
    the composite is built on are USD tables, so the reference implementation writes
    USD and rejects anything else by name rather than silently pricing it.
    """
    v = model_point()["currency"]
    if v != "USD":
        raise ValueError("only USD is in scope: " + str(v))
    return v


def sum_assured():
    """SA: the 基本保険金額 in US dollars.

    On the SINGLE shape it equals the 一時払保険料 at issue and never binds, because that
    shape's death benefit is ``max(積立金, 解約返戻金)`` with no sum assured above the fund.
    """
    return float(model_point()["sum_assured"])


def premium_mth_pp():
    """P: the level monthly premium in US dollars on the LEVEL shape.

    Guaranteed for the whole of 保険料払込期間 with no unilateral repricing right, which is
    what puts every future premium inside the contract boundary.  US$239.60 on the
    anchor cell is **sourced**, not constructed: it is the published premium for
    exactly that cell, and the same booklet publishes 225.00 for the 低解約返戻金特則 form.
    Zero on the SINGLE shape.
    """
    return float(model_point()["premium_mth"])


def single_premium():
    """The 一時払保険料 in US dollars on the SINGLE shape; zero on the LEVEL shape."""
    return float(model_point()["single_premium"])


def prem_months():
    """The 保険料払込期間 in months as the model point states it.

    ``0`` denotes 終身払, for which no 払込満了 exists; :func:`prem_months_eff` resolves it
    against the projection horizon.  ``240`` on the anchor cell is 60歳払込満了.
    """
    return int(model_point()["prem_months"])


def credit_rate():
    """ic: the declared 積立利率, annual effective.

    Held flat over the projection **[std]**.  On the LEVEL shape the base run holds it
    at the guaranteed floor, which is the guaranteed column of the published
    illustration and the only crediting figure for that shape that is a contract term;
    the declared-rate history is not machine-fetchable.  On the SINGLE shape it is a
    rate actually declared in the market and fixed for the whole 積立利率適用期間.
    """
    return float(model_point()["credit_rate"])


def guar_floor():
    """i0: the 最低保証積立利率, fixed at issue, which the declared rate can never breach.

    3.00% on the LEVEL shape, where it equals the contract's own 予定利率 and therefore
    also defines the 増加死亡保険金額 benchmark; 0.01% on the SINGLE shape, which is a floor
    in name only because that shape resets its rate every 積立利率適用期間.
    """
    return float(model_point()["guar_floor"])


def rate_period_y():
    """The 積立利率適用期間 in whole years; zero on the LEVEL shape, 15 on the SINGLE shape.

    Fifteen years is taken because it is the only period for which a complete 市場価格調整
    rate table is published, and the reconstruction in :func:`mva_rate` is anchored on
    that table.
    """
    return int(model_point()["rate_period_y"])


def mva_delta(t):
    """Delta(t): the move in the applicable 基準利率 since the contract's rate was set.

    A deterministic model point input, held flat, because this library projects
    contractual cash flows and not a rate view.  It is **not** a neutral zero: the
    published table's zero column sits at ``Delta = -0.1%``, so a flat path still
    charges a small positive adjustment.  Model point 4 runs it at -1.0%, where the
    adjustment turns negative and *raises* the surrender value.
    """
    return float(model_point()["mva_delta"])


def low_cv():
    """Whether the 低解約返戻金特則 is elected; off on the anchor cell.

    The suppression is a cliff released at 払込満了, so it is meaningless on a 終身払
    contract, which has no 払込満了 — a model point combining the two is rejected here
    rather than given an arbitrary release date.
    """
    v = bool(model_point()["low_cv"])
    if v and shape() == "LEVEL" and prem_months() == 0:
        raise ValueError("低解約返戻金特則 has no 払込満了 to release at on a 終身払 contract")
    return v


def idb_ratchet():
    """Whether the 増加死亡保険金額 is held at its running maximum.

    The ratchet appears in the ご契約のしおり but not in the extracted 約款第46条 text, so it
    is **[unverified]** and carried as a switch.  It is on in the base run and makes no
    difference there, because the uplift is identically zero at the floor.
    """
    return bool(model_point()["idb_ratchet"])


def idb_basis():
    """Which definition of the uplift benchmark ``AV0`` applies.

    ``"fund"`` **[std]**
        the account value the *same* recursion produces with ``ic`` replaced by ``i0``
        and the benchmark benefit held at ``SA``: :func:`av0_pp`.  Under it the uplift
        is identically zero on the guaranteed run, which is what the published
        guaranteed column requires.

    ``"prospective"``
        the fund needed at ``t`` to carry ``SA`` to the end of the table with no future
        premiums, on the same charge basis: :func:`av0_pro_pp`.  See the Space
        docstring for why this is the switch and not the base.
    """
    v = model_point()["idb_basis"]
    if v not in ("fund", "prospective"):
        raise ValueError("invalid idb_basis: " + str(v))
    return v


def target_on():
    """Whether the target-value conversion rider is elected; SINGLE shape only.

    The rider converts the contract to a yen whole life when the yen-converted
    surrender value reaches the 目標額.  It exists only on the single-premium shape in
    the retrieved set, so a LEVEL model point electing it is rejected by name.

    The rider has no settled name: the two carriers whose documents were retrieved call
    theirs 円建終身移行特約 and 目標値到達時終身保険移行特約, and the name
    目標到達時円建終身保険移行特約 that the wider market uses is **[unverified]** — the carrier
    whose documents carry it could not be fetched at all.  The *mechanic* is verified;
    only the name is not.
    """
    v = bool(model_point()["target_on"])
    if v and shape() != "SINGLE":
        raise ValueError("the target-value rider is a SINGLE-shape option")
    return v


def target_g():
    """g: the 目標値, a multiple of the yen the policyholder actually paid.

    110% **[std]**, the only value inside all three published menus and a target a
    two-and-a-half-year average holding period can actually reach.  The target is
    measured against the yen-converted premium, so a weaker yen alone can trigger it.
    """
    return float(model_point()["target_g"])


def target_action():
    """What happens on a target hit: ``"convert"``, ``"surrender"`` or ``"none"``.

    There is no default.  The 約款 converts the contract to a yen whole life; at every
    focus-monitored distributor most ターゲット型 policies are instead **surrendered** on
    the hit and the same product immediately re-sold to the same customer.  The
    contract and the evidence disagree and the choice is the user's.
    """
    v = model_point()["target_action"]
    if v not in ("convert", "surrender", "none"):
        raise ValueError("invalid target_action: " + str(v))
    if target_on() and v == "none":
        raise ValueError("target_action must be chosen where the rider is elected")
    return v


def dyn_lapse():
    """Whether the FX-driven dynamic surrender module is on; off in the base run.

    SINGLE shape only, because the yen profit it keys on is measured against a single
    premium actually paid at a known rate.
    """
    v = bool(model_point()["dyn_lapse"])
    if v and shape() != "SINGLE":
        raise ValueError("dynamic surrender is specified on the SINGLE shape only")
    return v


def apl_on():
    """Whether the 自動振替貸付 module is on; off in the base run.

    **Structurally absent on the SINGLE shape**: there is no premium to advance, so
    that shape's decrement set is smaller, not merely differently rated.  A SINGLE
    model point carrying a premium-default decrement is modelling a contract that does
    not exist, and is rejected here.
    """
    v = bool(model_point()["apl_on"])
    if v and shape() == "SINGLE":
        raise ValueError("the APL is structurally absent on the SINGLE shape")
    return v


def yen_in():
    """Whether the 円入金特約 is attached, so premiums are paid in yen at ``e + s``."""
    return bool(model_point()["yen_in"])


def yen_out():
    """Whether the 円支払特約 is attached, so benefits are paid in yen at ``e - s``."""
    return bool(model_point()["yen_out"])


def fx_ttm():
    """The reference TTM in yen per US$1, held flat unless ``fx_path`` is set.

    ¥159.43 is the published reference level and the base run holds it flat **[std]**:
    this library models contractual cash flows, not an FX view, and a projected
    currency path would be an economic assumption dressed as a product feature.
    """
    return float(model_point()["fx_ttm"])


def fx_spread():
    """s: the 為替手数料 spread in yen per US$1, charged on **each** crossing.

    ¥0.50 each way, the modal and the widest published value.  At the reference TTM
    that is 0.3136% one leg and **0.6292% on a round trip** — which is why every
    carrier warns that a loss can arise with no exchange-rate movement at all.  Zero
    where neither yen rider is attached.
    """
    return float(model_point()["fx_spread"])


def fx_path():
    """Whether :func:`fx_rate` reads the path table instead of holding ``fx_ttm`` flat."""
    return bool(model_point()["fx_path"])


def mort_be_factor():
    """The experience adjustment to the mortality **decrement**; 1.00 in the base run.

    The shipped table is a *valuation* table with an explicit margin, so any
    best-estimate basis is a **[std]** adjustment of it.  This lever moves
    :func:`mort_rate` and must never move :func:`coi_rate`; see the Space docstring.
    """
    return float(model_point()["mort_adj"])


def omega_age():
    """The terminal age of the shipped table for this life: the first age at which q = 1.

    109 male and 113 female on 生保標準生命表2018（死亡保険用）.  It is read off the table
    rather than hard-coded, so replacing the table moves the horizon with it.
    """
    tbl = data.mort_table().xs(sex(), level="sex")                   # noqa: F821
    return int(tbl.index[tbl["mort_rate"] >= 1.0].min())


def proj_len():
    """T: the projection length in months, ``12 (omega - x + 1)``.

    840 on the anchor cell.  ``t`` runs ``0 ... proj_len() - 1``; there is no maturity
    date and no 満期保険金, so the horizon is the table's terminal age and nothing else.
    Truncating at 払込満了, or at age 100, is a direct understatement: 85% of expected
    death claims on the anchor cell arrive after 払込満了.
    """
    return 12 * (omega_age() - issue_age() + 1)


def prem_months_eff():
    """n: the 保険料払込期間 in months as the projection uses it.

    One month on the SINGLE shape; the whole horizon where ``prem_months`` is 0, which
    denotes 終身払; otherwise the model point's own value.
    """
    if shape() == "SINGLE":
        return 1
    n = prem_months()
    return proj_len() if n == 0 else n


def policy_year(t):
    """The policy year containing month t, 1-based: ``floor(t/12) + 1``."""
    return t // 12 + 1


def age(t):
    """The attained age in policy month t: ``x + floor(t/12)``, exactly."""
    return issue_age() + t // 12


def coi_rate(t):
    """The table mortality rate at the attained age, **unadjusted**.

    This is the cost-of-insurance basis: 生保標準生命表2018（死亡保険用）with no further
    loading, on the ground that it is already a valuation table carrying an explicit
    margin.  It is a pricing element the insurer sets in its 算出方法書, so ``mort_be_factor``
    does not touch it.  Includes 高度障害, which the published death rate already carries.
    """
    return float(data.mort_table().loc[(sex(), age(t)), "mort_rate"])  # noqa: F821


def coi_rate_mth(t):
    """The monthly cost-of-insurance rate, ``1 - (1 - q)^(1/12)``."""
    return 1.0 - (1.0 - coi_rate(t)) ** (1.0 / 12.0)


def mort_rate(t):
    """q(t): the annual mortality decrement in month t, including 高度障害.

    The table rate times ``mort_be_factor``, capped at 1.  One decrement covering both
    benefits: 高度障害 pays the same amount and extinguishes the contract, and the
    published table's death rate already includes it, so adding a second decrement
    would double-count the benefit.
    """
    return min(1.0, coi_rate(t) * mort_be_factor())


def mort_rate_mth(t):
    """q_m(t): the monthly decrement, ``1 - (1 - q)^(1/12)``.

    ``0.0000983866`` at the anchor cell's first attained age, where ``q40 = 0.00118``.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """The table annual surrender rate for this shape in month t, before any module.

    Two curves.  The SINGLE curve, 28 / 23 / 18 / 14 / 8%, is calibrated so the
    cumulative four-year exit is 60.90%, against a published reading that about 60% of
    外貨建一時払保険 are surrendered within four years; the LEVEL curve, 8 / 7 / 6 / 5 / 5 /
    4 / 3%, rests on no public evidence at all and is a **[std]** judgement.  Policy
    years beyond the table take its last row.
    """
    tbl = data.lapse_table().xs(shape(), level="shape")              # noqa: F821
    y = min(policy_year(t), int(tbl.index.max()))
    return float(tbl.loc[y, "lapse_rate"])


def lapse_dyn_factor(t):
    """The FX-driven dynamic surrender multiplier **[std]**; 1 unless ``dyn_lapse``.

    ``min(2.5, max(0.5, 1 + beta (CV(t)(e(t) - s) / P_jpy0 - 1)))`` with ``beta = 2.0``.
    A policyholder in yen profit surrenders and one in yen loss holds on, which is the
    economically natural driver on this product — the currency, not the crediting rate.
    Under the base run's flat FX path the multiplier moves only with the account value,
    which is precisely the limitation the notes name.
    """
    if not dyn_lapse():
        return 1.0
    ratio = cv_pp(t) * (fx_rate(t) - fx_spread()) / premium_jpy0()
    return min(dyn_lapse_cap,                                        # noqa: F821
               max(dyn_lapse_floor,                                  # noqa: F821
                   1.0 + dyn_lapse_beta * (ratio - 1.0)))            # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** surrender rate applied in month t, capped at 1.

    The table rate times the dynamic multiplier.  A surrender pays :func:`cv_pp`, never
    :func:`av_pp`.
    """
    return min(1.0, lapse_rate_base(t) * lapse_dyn_factor(t))


def lapse_rate_mth(t):
    """w_m(t): the monthly surrender rate, ``1 - (1 - w)^(1/12)``.

    ``0.0069243826`` in the anchor cell's first policy year, where ``w = 8%``.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def credit_rate_mth():
    """j: the monthly crediting factor, ``(1 + ic)^(1/12) - 1``.

    The geometric twelfth root **[std]**, not ``ic/12``.  The convention has to be
    stated because the published surrender-value run is reproduced to the dollar and a
    nominal-over-12 implementation misses the fit.  ``1 + j = 1.0024662698`` at 3.00%.
    """
    return (1.0 + credit_rate()) ** (1.0 / 12.0) - 1.0


def guar_floor_mth():
    """The same monthly factor on the 予定利率 basis, ``(1 + i0)^(1/12) - 1``."""
    return (1.0 + guar_floor()) ** (1.0 / 12.0) - 1.0


def charge_param(item):
    """One row of *charge_table.csv* for this shape, by item name.

    The whole shape-dependent parameter set lives in the CSV with a ``provenance``
    column on every row: the back-solved 契約初期費用 and 維持費率, the 解約控除 scale, the
    低解約返戻金割合 ramp, the three constants of the 市場価格調整 reconstruction and the two
    特別積立金 rates.
    """
    return float(data.charge_table().loc[(shape(), item), "value"])  # noqa: F821


def prem_charge_rate(t):
    """phi(t): the 契約初期費用 rate deducted from the premium received in month t.

    Two rates on the LEVEL shape — 38% over policy months 0 to 23 and 12% thereafter —
    **back-solved** from the published guaranteed surrender-value run, because every
    carrier in the source set refuses to quantify the charge and the rates live in an
    unpublished 基礎書類.  One front-end rate on the SINGLE shape, 4.50% of the single
    premium at issue, which *is* published.
    """
    if t < int(charge_param("prem_charge_early_months")):
        return charge_param("prem_charge_early")
    return charge_param("prem_charge_late")


def maint_rate():
    """mu: the 維持費率 per annum of the 積立金, deducted monthly.

    0.50% p.a. on the LEVEL shape, back-solved with the two premium charges.  **Zero on
    the SINGLE shape**: that shape's in-force costs sit inside the declared 積立利率, and
    reproducing its published surrender values requires the fund to grow at the
    declared rate exactly.
    """
    return charge_param("maint_rate")


def coi_charged():
    """Whether a 保障部分 charge is deducted from the fund; true on the LEVEL shape only.

    On the SINGLE shape the death benefit never exceeds the fund by design and the
    保障 cost is taken inside the crediting-rate calculation, so nothing is deducted from
    the 積立金 — which is why a negative 市場価格調整 can raise the death benefit above the
    account value without creating a charge.
    """
    return charge_param("coi_charged") > 0.0


def prem_due_pp(t):
    """P(t): the premium due per policy at the **start** of month t, in US dollars.

    Level and guaranteed over months ``0 ... n - 1`` on the LEVEL shape; a single
    collection at ``t = 0`` on the SINGLE shape.
    """
    if t >= prem_months_eff():
        return 0.0
    return single_premium() if shape() == "SINGLE" else premium_mth_pp()


def charge_init(t):
    """C_init(t): the 契約初期費用 taken out of month t's premium.

    ``phi(t) P(t)``.  Not a cash flow — an internal transfer from the premium to the
    insurer, taken before anything reaches the 積立金.
    """
    return prem_charge_rate(t) * prem_due_pp(t)


def prem_to_av_pp(t):
    """The part of month t's premium that reaches the 積立金: ``P(t) - C_init(t)``.

    US$148.5520 in every month of the anchor cell's first two policy years.
    """
    return prem_due_pp(t) - charge_init(t)


def charge_maint(t):
    """C_maint(t): the 維持費 taken in month t, ``(mu / 12) x AVg(t)``.

    Charged on the fund **after** the premium and the 契約初期費用 and **before** the
    cost of insurance, which is what fixes the order of the recursion.  Not a cash flow.
    """
    return (maint_rate() / 12.0) * av_pp_at(t, "AFT_PREM")


def charge_coi(t):
    """C_coi(t): the 保障部分 charge in month t, on the 危険保険金額.

    ``q_m(t) x max(0, DB(t) - (AVg(t) - C_maint(t)))`` — the monthly table rate applied
    to the net amount at risk measured *after* the maintenance charge.  The floor at
    zero is structural, not cosmetic: on the anchor cell the account value overtakes the
    sum assured at month 709 and the charge stops, and the death benefit must **not** be
    silently floored at the fund in exchange.  Not a cash flow.

    The charge is also capped at what the fund actually holds, so the 積立金 can never
    run negative: it is an account, not a debt.  Where the cap binds — as it does on the
    低解約返戻金特則 model point at the far end of the projection, whose lower premium the
    back-solved charge stack does not make self-funding — the contract's guaranteed 終身
    cover at a guaranteed level premium is being carried by the insurer rather than by
    the fund, and the surrender value is nil. Without the cap the shortfall compounds
    into the net amount at risk and the projection diverges.
    """
    if not coi_charged():
        return 0.0
    fund = av_pp_at(t, "AFT_CHARGE_MAINT")
    raw = coi_rate_mth(t) * max(0.0, benefit_pp(t) - fund)
    return min(raw, max(0.0, fund))


def av_pp_at(t, timing):
    """The 積立金 per policy at a point inside month t, in US dollars.

    ``"BEF_PREM"``
        ``AV(t)``, the start of the month before that month's premium; the
        same number as :func:`av_pp`.

    ``"AFT_PREM"``
        ``AVg(t) = AV(t) + P(t) - C_init(t)``, after the premium and the
        契約初期費用.

    ``"AFT_CHARGE_MAINT"``
        after the 維持費 as well; this is the fund the net amount at risk is
        measured against.

    ``"AFT_CHARGE"``
        after all three charges, the fund interest is credited to.

    ``"AFT_INT"``
        ``AV(t+1)``, the end-of-month state including any 特別積立金.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t)
    if timing == "AFT_CHARGE_MAINT":
        return av_pp_at(t, "AFT_PREM") - charge_maint(t)
    if timing == "AFT_CHARGE":
        return av_pp_at(t, "AFT_CHARGE_MAINT") - charge_coi(t)
    if timing == "AFT_INT":
        return av_pp(t + 1)
    raise ValueError("invalid timing: " + str(timing))


def av_pp_bef_sr(t):
    """AV(t) before any 特別積立金 top-up is added; zero at issue.

    Split out from :func:`av_pp` so that the top-up has a base to be computed against
    without the recursion feeding on itself.
    """
    if t <= 0:
        return 0.0
    return av_pp_at(t - 1, "AFT_CHARGE") * (1.0 + credit_rate_mth())


def special_reserve_pp(t):
    """特別積立金: the top-up added to the 積立金 after 10 and after 20 years in force.

    Computed from ten-year investment performance and never paid to a contract
    terminating earlier.  The **[std]** reconstruction is a share of the fund's excess
    over its 予定利率 benchmark, ``0.24`` at ten years and ``0.16`` at twenty, fitted to
    the four published amounts — 147 and 527 on the 3.50% column, 302 and 1,120 on the
    4.00% column — with a worst deviation of 3.0%.

    On the guaranteed run it is **identically zero**, because the fund and its benchmark
    coincide there, and the published 3.00% column shows (0) at both durations.  A
    non-zero top-up on the base run is a bug.
    """
    if t == 120:
        rate = charge_param("special_reserve_rate_10")
    elif t == 240:
        rate = charge_param("special_reserve_rate_20")
    else:
        return 0.0
    if rate == 0.0:
        return 0.0
    return rate * max(0.0, av_pp_bef_sr(t) - av0_pp(t))


def av_pp(t):
    """AV(t): the 積立金 at the **start** of month t, before that month's premium.

    The one-line recursion, in the order the notes fix::

        AVg(t)  = AV(t) + P(t) - C_init(t)
        AV(t+1) = (AVg(t) - C_maint(t) - C_coi(t)) x (1 + j)

    plus the 特別積立金 at ten and twenty years.  ``AV(1) = 139.0080451`` on the anchor
    cell.  This is a per-policy quantity: it carries no survivorship, and the weight on
    the cash flows it drives is :func:`pols_if`.
    """
    return av_pp_bef_sr(t) + special_reserve_pp(t)


def av0_pp(t):
    """AV0(t): the same fund on the 予定利率 basis — the uplift's **[std]** benchmark.

    The 約款 does not define ``AV0`` numerically, because it rests on the insurer's
    unpublished 予定死亡率 and 予定事業費率.  The definition taken here is the account value
    the *same* recursion produces with ``ic`` replaced by ``i0`` and the benchmark
    benefit held at ``SA`` with no uplift of its own.  It follows that whenever
    ``ic = i0`` the two funds coincide exactly and :func:`idb_pp` is identically zero —
    which is what the published guaranteed column requires.
    """
    if t <= 0:
        return 0.0
    prev = av0_pp(t - 1)
    gross = prev + prem_to_av_pp(t - 1)
    maint = (maint_rate() / 12.0) * gross
    coi = 0.0
    if coi_charged():
        fund = gross - maint
        coi = min(coi_rate_mth(t - 1) * max(0.0, sum_assured() - fund),
                  max(0.0, fund))
    return (gross - maint - coi) * (1.0 + guar_floor_mth())


def av0_pro_pp(t):
    """The prospective 予定利率 fund: what is needed at t to carry SA with no premiums.

    The same charge mechanic run backwards with the premium switched off, terminating
    at ``AV0(T) = SA`` because death is certain in the last month::

        AV0(t) = (AV0(t+1) / (1 + j0) + q_m(t) SA) / ((1 - mu/12)(1 + q_m(t)))

    Selected by ``idb_basis = "prospective"``.  It gives ``AV - AV0`` of -22,044.31 at
    ten years, +36.52 at 払込満了, +296.03 at fifty years and +30,762.05 at the terminal
    month on the anchor cell.  The near-zero crossing at 払込満了 is a strong independent
    check on the back-solved charge stack.
    """
    if t >= proj_len():
        return sum_assured()
    qm = coi_rate_mth(t) if coi_charged() else 0.0
    g = 1.0 - maint_rate() / 12.0
    return ((av0_pro_pp(t + 1) / (1.0 + guar_floor_mth()) + qm * sum_assured())
            / (g * (1.0 + qm)))


def idb_pp(t):
    """IDB(t): the 増加死亡保険金額, the ratcheting death-benefit uplift.

    ``max(IDB(t-1), AV(t) - AV0(t))`` floored at zero, recomputed at each 月単位の契約応当日,
    with the ``max`` against the previous month being the ratchet.  It exists only on
    the main contract of the LEVEL shape: the SINGLE shape has no sum assured above the
    fund for an uplift to sit on top of.

    **Identically zero on the guaranteed run**, by construction of :func:`av0_pp`.
    """
    if shape() != "LEVEL" or t <= 0:
        return 0.0
    bench = av0_pro_pp(t) if idb_basis() == "prospective" else av0_pp(t)
    raw = max(0.0, av_pp(t) - bench)
    if not idb_ratchet():
        return raw
    return max(idb_pp(t - 1), raw)


def benefit_pp(t):
    """DB(t): the death and 高度障害 benefit per policy in month t, in US dollars.

    ``SA + IDB(t)`` on the LEVEL shape.  ``max(AV(t), CV(t))`` on the SINGLE shape,
    where there is no sum assured above the fund at all — and the ``max`` binds: where
    the 市場価格調整 is strongly negative the surrender value exceeds the account value and
    the death benefit follows the higher.
    """
    if shape() == "SINGLE":
        return max(av_pp(t), cv_pp(t))
    return sum_assured() + idb_pp(t)


def surr_charge_rate(t):
    """sc(t): the 解約控除率 applying to a surrender at month t.

    7.0% in policy year 1 falling 0.7 percentage points per completed policy year to
    zero at ten years, constant within the year, applied to the **積立金**.  It is a
    charge: one-sided and never adding value.
    """
    if t >= int(charge_param("surr_charge_months")):
        return 0.0
    return max(0.0, charge_param("surr_charge_start")
               - charge_param("surr_charge_step") * (t // 12))


def mva_rem(t):
    """rem(t): the years remaining in the current 積立利率適用期間; zero on the LEVEL shape.

    Each period restarts at its 積立利率計算基準日 **[std]**, so ``rem`` saws from the full
    period down to zero and back.  ``rem(36) = 12`` on the worked example's cell.
    """
    if shape() != "SINGLE" or rate_period_y() <= 0:
        return 0.0
    return rate_period_y() - (t % (12 * rate_period_y())) / 12.0


def mva_rate(t):
    """mva(t): the 市場価格調整率 at month t; **not** a charge, and it can be negative.

    ``1 - (1 + (Delta(t) + A) / (1 + r0)) ^ (-d rem(t))``, the **[std]** reconstruction
    of the published 15-year rate table.  Zero on the whole LEVEL shape, zero on an
    積立利率計算基準日 and zero inside a one-year 積立利率適用期間 — a discontinuity a monthly model
    must place on the right month.

    A rise in market rates since the contract's own rate was set reduces the surrender
    value and a fall **increases** it.  Implementing this as a deduction floored at zero
    models a different product.
    """
    if shape() != "SINGLE" or rate_period_y() <= 1:
        return 0.0
    if t % (12 * rate_period_y()) == 0:
        return 0.0
    a = charge_param("mva_spread")
    r0 = charge_param("mva_base_rate")
    d = charge_param("mva_damping")
    return 1.0 - (1.0 + (mva_delta(t) + a) / (1.0 + r0)) ** (-d * mva_rem(t))


def low_cv_rate(t):
    """kl(t): the 低解約返戻金割合 at month t; 1.00 unless the 特則 is in force.

    0.70 while four or more premium-paying years remain, stepping to 0.775, 0.85 and
    0.925 at three, two and one, and to 1.00 from 払込満了 — with the remaining count
    rounded **up** to whole years.  The step is a cliff and interpolating across it is
    wrong: on the published run the 特則 form pays US$27,706 at duration 15 against
    US$53,029 at duration 20.
    """
    if not low_cv():
        return 1.0
    left = prem_months_eff() - t
    if left <= 0:
        return 1.0
    years = -(-left // 12)
    if years >= 4:
        return charge_param("low_cv_ge4")
    return charge_param("low_cv_%d" % years)


def cv_pp(t):
    """CV(t): the payable 解約返戻金 per policy at month t, in US dollars.

    ``AV(t) (1 - mva(t) - sc(t)) kl(t)``.  All three factors can be active at once on
    the SINGLE shape.  ``CV(1) = 129.2774820`` on the anchor cell, where the 積立金 is
    139.0080451 and the 解約控除率 7.0%.  Paying a surrender on :func:`av_pp` instead
    overstates every early exit by up to 7% plus the adjustment.
    """
    return av_pp(t) * (1.0 - mva_rate(t) - surr_charge_rate(t)) * low_cv_rate(t)


def fx_rate(t):
    """e(t): the reference TTM in month t, yen per US$1.

    The model point's own ``fx_ttm``, held flat, unless ``fx_path`` is set — in which
    case the path table is read by policy year, its last row carried forward.  The rate
    is never a literal inside a formula.
    """
    if not fx_path():
        return fx_ttm()
    tbl = data.fx_path_table()                                       # noqa: F821
    return float(tbl.loc[min(policy_year(t), int(tbl.index.max())), "fx_ttm"])


def premium_jpy0():
    """P_jpy0: the yen the policyholder actually paid for the contract.

    The single premium converted at the 入金用為替レート on day one, ``e(0) + s``:
    ¥15,993,000 on the worked example's SINGLE cell.  It is the base of both the 目標額
    and the dynamic-surrender multiplier, which is why a weaker yen alone can trigger a
    conversion.
    """
    return single_premium() * (fx_rate(0) + (fx_spread() if yen_in() else 0.0))


def target_amount_jpy():
    """The 目標額 in yen: ``g`` times the yen premium paid.

    ¥17,592,300 on the worked example's cell, from a 目標値 of 110%.
    """
    return target_g() * premium_jpy0()


def target_hit(t):
    """Whether the yen-converted 解約返戻金 has reached the 目標額 at month t.

    The test is on :func:`cv_pp`, **after** FX and after the 市場価格調整 — not on the
    account value — and it does not apply inside the contractual one-year dead zone.
    """
    if not target_on() or t < target_dead_zone_mths:                 # noqa: F821
        return False
    out = fx_rate(t) - (fx_spread() if yen_out() else 0.0)
    return cv_pp(t) * out >= target_amount_jpy()


def target_month():
    """The first month at which the 目標値 is reached, or ``proj_len() + 1`` if never.

    Month 52 on the worked example's cell — four years four months — where the 積立金 is
    116,626.82, the 市場価格調整率 0.007219, the 解約控除率 4.2% and the 解約返戻金 110,886.51,
    worth ¥17,623,193 against a 目標額 of ¥17,592,300.
    """
    if not target_on():
        return proj_len() + 1
    for t in range(target_dead_zone_mths, proj_len() + 1):           # noqa: F821
        if target_hit(t):
            return t
    return proj_len() + 1


def apl_intercept(t):
    """Whether the 自動振替貸付 can carry the premium falling due in month t.

    True while the module is on, a premium is due, and the policy's net surrender value
    — the 解約返戻金 less the advance already outstanding — covers it.  While it is true
    the non-payment share of the surrender decrement does not lapse: it is redirected
    into :func:`pols_if_apl`.  A policy does not lapse while the account value can carry
    the premium, and applying a lapse rate to unpaid premiums without running this test
    models a decrement the contract does not have.
    """
    if not apl_on() or t >= prem_months_eff():
        return False
    return cv_pp(t) - loan_pp(t) >= prem_due_pp(t)


def pols_apl_new(t):
    """The policies whose premium the 自動振替貸付 advances at the end of month t.

    The non-payment share of the surrenders the paying cohort would otherwise have
    made.  The split of the surrender decrement into a voluntary part and a
    premium-non-payment part is **[std]**: no retrieved source separates them.
    """
    if not apl_intercept(t):
        return 0.0
    return (pols_payer(t) * (1.0 - mort_rate_mth(t)) * lapse_rate_mth(t)
            * apl_nonpay_share)                                      # noqa: F821


def pols_payer(t):
    """The policies in force at the start of month t that are paying their own premium.

    ``pols_if_init()`` at ``t = 0``, then ``(1 - q_m)(1 - w_m)`` — the same recursion
    the whole cohort follows, with the intercepted non-payers moving out of it into
    :func:`pols_if_apl` rather than lapsing.  Zero from :func:`target_month` on, where
    the contract has left the dollar ledger.
    """
    if t < 0:
        return 0.0
    if t == 0:
        return pols_if_init                                          # noqa: F821
    if t >= proj_len() or t >= target_month():
        return 0.0
    return (pols_payer(t - 1) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1)))


def pols_if_apl(t):
    """The policies in force at the start of month t carried by the 自動振替貸付.

    Zero everywhere unless ``apl_on``.  The cohort accumulates the intercepted
    non-payers, is decremented by mortality and by the *voluntary* part of the surrender
    rate only, and runs off through the ordinary decrement once the fund can no longer
    carry the premium.
    """
    if t <= 0 or not apl_on():
        return 0.0
    if t >= proj_len() or t >= target_month():
        return 0.0
    surv = (pols_if_apl(t - 1) * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1)
               * (1.0 - apl_nonpay_share)))                          # noqa: F821
    return surv + pols_apl_new(t - 1)


def loan_total(t):
    """The aggregate 自動振替貸付 advance outstanding at the start of month t.

    Advanced premiums accumulated at ``apl_int_rate`` and decremented with the cohort
    that owes them; policies entering the cohort bring no balance with them.  Carried in
    aggregate rather than as a full entry-year triangle, which is exact for the total
    and makes :func:`loan_pp` the cohort average **[std]**.

    ``apl_int_rate`` is **2.75% p.a.**, the savings chassis's own **[std]** level, taken
    unchanged because this product changes nothing about the 自動振替貸付 except whether the
    shape has one at all.  The contractual ceiling the chassis cites is 年8%.
    """
    if t <= 0 or not apl_on():
        return 0.0
    if t >= proj_len() or t >= target_month():
        return 0.0
    advanced = loan_total(t - 1) + prem_due_pp(t - 1) * pols_if_apl(t - 1)
    rate = (1.0 + apl_int_rate) ** (1.0 / 12.0)                      # noqa: F821
    return (advanced * rate * (1.0 - mort_rate_mth(t - 1))
            * (1.0 - lapse_rate_mth(t - 1)
               * (1.0 - apl_nonpay_share)))                          # noqa: F821


def loan_pp(t):
    """The average 自動振替貸付 advance per policy in the APL cohort at month t.

    Repaid out of whatever the policy is eventually paid: a death benefit or a surrender
    value net of it, floored at zero.  Zero everywhere unless ``apl_on``.
    """
    n = pols_if_apl(t)
    return loan_total(t) / n if n > 0.0 else 0.0


def pols_if(t):
    """l(t): the policies in force at the **start** of policy month t.

    ``pols_payer(t) + pols_if_apl(t)``, and the weight on every cash flow of the same
    ``result_cf()`` row.  ``pols_if(0) = 1`` on a single-policy model point;
    ``pols_if(proj_len()) = 0``, because the table's terminal rate is 1 and every policy
    leaves by death, by surrender or through the target conversion.
    """
    return pols_payer(t) + pols_if_apl(t)


def pols_if_at(t, timing):
    """The policies in force at a point inside month t.

    ``"BEF_DECR"``
        l(t), the start of the month before any decrement; the same number
        as :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before surrenders — the processing order is **death
        before surrender** **[std order]**, so this is the population
        surrenders are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing: " + str(timing))


def pols_death(t):
    """D(t) = l(t) q_m(t): expected death and 高度障害 claims at the end of month t."""
    if t >= proj_len():
        return 0.0
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """S(t): expected surrenders at the end of month t, on the survivors of mortality.

    The paying cohort surrenders at the full monthly rate, less whatever the 自動振替貸付
    intercepts; the APL cohort surrenders at the voluntary part only.  Does **not**
    include the policies leaving through a target conversion, which are
    :func:`pols_target`.
    """
    if t >= proj_len():
        return 0.0
    w = lapse_rate_mth(t)
    keep = apl_nonpay_share if apl_intercept(t) else 0.0             # noqa: F821
    payer = pols_payer(t) * (1.0 - mort_rate_mth(t)) * w * (1.0 - keep)
    apl = (pols_if_apl(t) * (1.0 - mort_rate_mth(t)) * w
           * (1.0 - apl_nonpay_share))                               # noqa: F821
    return payer + apl


def pols_target(t):
    """The policies leaving the dollar ledger at the end of month t on a target hit.

    Non-zero in exactly one month, ``target_month() - 1``, where every survivor of that
    month's decrements either converts to a yen whole life or surrenders — the election
    the model point makes.  Zero everywhere on every model point without the rider.
    """
    if not target_on() or t != target_month() - 1 or t >= proj_len():
        return 0.0
    return pols_if(t) - pols_death(t) - pols_lapse(t)


def premiums(t):
    """Premium income at the start of month t, an inflow, in US dollars.

    Carried on :func:`pols_payer`, not on :func:`pols_if`: a policy whose premium the
    自動振替貸付 is advancing pays the insurer nothing, though the premium still reaches
    the 積立金.  ``239.60`` in month 0 and ``237.9175077`` in month 1 on the anchor cell.
    """
    if t >= proj_len():
        return 0.0
    return prem_due_pp(t) * pols_payer(t)


def claims(t, kind=None):
    """Benefit outgo at the end of month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        ``DB(t) D(t)``, the death and 高度障害 benefit.  The APL cohort's
        payment is net of the advance outstanding, floored at zero.

    ``"LAPSE"``
        ``CV(t+1) S(t)``, the surrender benefit — valued on the surrender
        value **after** that month's interest, and net of any APL advance.
        Where the target election is ``"surrender"`` the policies leaving on
        the hit are paid here as well.
    """
    if kind is None:
        return claims(t, "DEATH") + claims(t, "LAPSE")
    if t >= proj_len():
        return 0.0
    qm = mort_rate_mth(t)
    if kind == "DEATH":
        gross = benefit_pp(t) * pols_payer(t) * qm
        net = max(0.0, benefit_pp(t) - loan_pp(t)) * pols_if_apl(t) * qm
        return gross + net
    if kind == "LAPSE":
        w = lapse_rate_mth(t)
        keep = apl_nonpay_share if apl_intercept(t) else 0.0         # noqa: F821
        payer = pols_payer(t) * (1.0 - qm) * w * (1.0 - keep)
        apl = (pols_if_apl(t) * (1.0 - qm) * w
               * (1.0 - apl_nonpay_share))                           # noqa: F821
        out = cv_pp(t + 1) * payer + max(0.0, cv_pp(t + 1) - loan_pp(t)) * apl
        if target_action() == "surrender":
            out = out + cv_pp(t + 1) * pols_target(t)
        return out
    raise ValueError("invalid kind: " + str(kind))


def conversions(t):
    """The 解約返戻金 leaving the dollar ledger on a 目標値 conversion at the end of month t.

    Zero unless the target election is ``"convert"``.  The contract becomes a yen whole
    life whose death benefit and surrender value are fixed in yen and on which neither
    the exchange rate nor the 市場価格調整 acts again; **that contract is out of scope**, so
    the dollar model books its value out at the conversion date and stops.  The scope
    boundary is **[std]** and is why the two target elections differ in where the money
    is booked rather than in how much of it there is.
    """
    if target_action() != "convert" or t >= proj_len():
        return 0.0
    return cv_pp(t + 1) * pols_target(t)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + pi)^floor(t/12)`` **[std]**.

    1.0 through the first twelve months, then 1% a year on the anniversary.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def claim_expenses(t):
    """ec D(t): the claim handling expense on the month's death claims **[std]**.

    US$150 per claim, uninflated.  Kept **out** of :func:`expenses`, deducted on its own
    line in :func:`net_cf` and published as its own ``result_cf()`` column: it is driven
    by the death decrement, not by the in-force count, so folding it into the
    acquisition-and-maintenance column hides which lever moves it.
    """
    return expense_claim * pols_death(t)                             # noqa: F821


def expenses(t):
    """Acquisition and maintenance expense in month t **[std]**, in US dollars.

    Acquisition expense of US$300 per policy at issue, then US$60 a year per policy
    inflating at 1%, accrued monthly and payable **for life** — this is a whole-life
    contract with no maturity date, so the maintenance stream runs to the terminal age.
    The claim expense is **not** in here: it is :func:`claim_expenses`, its own column.
    ``305.0000000`` in month 0 on the anchor cell.

    No carrier publishes an expense basis, so every level here is a standardization.
    Expenses are the insurer's own costs, incurred in yen, held in dollars at the
    model's convenience and translated at the plain TTM: they do not cross the
    policyholder boundary and so never meet the 為替手数料 spread.
    """
    if t >= proj_len():
        return 0.0
    acq = expense_acq * pols_if(t) if t == 0 else 0.0                # noqa: F821
    maint = (expense_maint / 12.0) * inflation_factor(t) * pols_if(t)  # noqa: F821
    return acq + maint


def commissions(t):
    """Commission outgo in month t **[std]**, in US dollars.

    LEVEL: 90% of the annualized premium at issue, then 3% of premium income from month
    12 to 払込満了.  SINGLE: 5.5% of the single premium at issue and a 継続手数料 of 0.75%
    p.a. of the account value for seven years — the shape the published schedules and
    the FSA's L-shaped 5.5% / 0.1% reading of the sector both describe.  Only the
    upfront *pattern* is evidenced; the levels are standardizations.
    """
    if t >= proj_len():
        return 0.0
    if shape() == "SINGLE":
        init = (comm_init_single_rate * single_premium()             # noqa: F821
                * pols_if(t) if t == 0 else 0.0)
        trail = 0.0
        if t < 12 * comm_trail_years:                                # noqa: F821
            trail = (comm_trail_rate / 12.0) * av_pp(t) * pols_if(t)  # noqa: F821
        return init + trail
    init = (comm_init_rate * 12.0 * premium_mth_pp()                 # noqa: F821
            * pols_if(t) if t == 0 else 0.0)
    renew = 0.0
    if comm_renewal_start <= t < prem_months_eff():                  # noqa: F821
        renew = comm_renewal_rate * premiums(t)                      # noqa: F821
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy month t, **income positive**, in US dollars.

    Premiums less death and 高度障害 claims, surrender benefits, any target conversion,
    claim expense, acquisition and maintenance expense and commission.  The notes' own
    sign, which is also the library-wide one, so there is no outgo-positive
    ``liability_cf`` companion to publish.

    The three account-value charges are **not** in it: they are internal transfers from
    the 積立金, and booking one as revenue alongside the premium that funded it
    double-counts the premium.

    The shape to expect is a deep new business strain in month 0 — upfront commission
    and acquisition expense against a single monthly premium — then thin positive
    margins that thin further as the surrender benefit grows, and a long negative tail
    after 払込満了 where claims and maintenance run on with no premium behind them.
    """
    return (premiums(t) - claims(t) - conversions(t) - claim_expenses(t)
            - expenses(t) - commissions(t))


def benefits_usd(t):
    """The total policyholder payment in month t: claims plus any target conversion.

    The quantity that crosses the currency boundary outbound, at ``e - s``.
    """
    return claims(t) + conversions(t)


def premiums_jpy(t):
    """Premium income in month t translated at the 入金用為替レート, ``e(t) + s``.

    ¥38,319.23 in month 0 on the anchor cell.  Where the 円入金特約 is not attached the
    policyholder pays in US dollars and the plain TTM applies.
    """
    return premiums(t) * (fx_rate(t) + (fx_spread() if yen_in() else 0.0))


def benefits_jpy(t):
    """Benefit outgo in month t translated at the 支払用為替レート, ``e(t) - s``.

    ¥1,705.91 in month 0 on the anchor cell.
    """
    return benefits_usd(t) * (fx_rate(t) - (fx_spread() if yen_out() else 0.0))


def expenses_jpy(t):
    """Expense and commission outgo in month t translated at the plain TTM.

    All three lines — the claim expense, the acquisition and maintenance expense and the
    commission.  The insurer's own costs never cross the policyholder boundary, so they
    never meet the spread.
    """
    return (claim_expenses(t) + expenses(t) + commissions(t)) * fx_rate(t)


def net_cf_jpy(t):
    """The yen ledger of month t: **three translations, not one**.

    ``premiums_jpy - benefits_jpy - expenses_jpy``.  ¥-424,569.01 in month 0 on the
    anchor cell, against ``net_cf(0) x 159.43 = ¥-424,694.18`` — the two figures are
    both correct and mean different things, and a model that publishes only the second
    has silently given the spread away.
    """
    return premiums_jpy(t) - benefits_jpy(t) - expenses_jpy(t)


def fx_spread_jpy(t):
    """The insurer's 為替手数料 spread income in month t, published as its own column.

    ``s x (premiums + benefits)`` over the legs that actually convert.  ¥125.17 in month
    0 on the anchor cell and ¥39,266 over the whole run — exactly the gap between
    :func:`net_cf_jpy` and ``net_cf(t) e(t)``, month by month and so in total.  Summing
    ``net_cf`` first and translating once at ``e(0)`` reproduces that gap only where the
    rate is flat; where ``fx_path`` is on it does not.
    """
    legs = 0.0
    if yen_in():
        legs = legs + premiums(t)
    if yen_out():
        legs = legs + benefits_usd(t)
    return fx_spread() * legs


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``l(t) - l(t+1) - D(t) - S(t) - target(t)``.  The table terminates, so every policy
    leaves by one of the decrements and the residual has nowhere to hide.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_target(t))


def check_pols_roll_fwd():
    """True when every policy leaves by a named decrement and none is lost.

    The per-month roll-forward closes, ``pols_if(proj_len())`` is zero, and the whole-run
    decrements sum to the cohort: on the anchor cell ``sum D = 0.211608544`` and
    ``sum S = 0.788391456``, which is 1.000000000 exactly.  Surrenders take 78.8% of the
    cohort out against mortality's 21.2%, so this is a lapse-driven liability wearing a
    mortality product's clothes.
    """
    tol = roll_fwd_tol * max(pols_if_init, 1.0)                      # noqa: F821
    if abs(pols_if(proj_len())) > tol:
        return False
    total = sum(pols_death(t) + pols_lapse(t) + pols_target(t)
                for t in range(proj_len()))
    if abs(total - pols_if_init) > tol:                              # noqa: F821
        return False
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_av_roll_fwd_resid(t):
    """The account-value roll-forward residual in month t; zero everywhere.

    ``AV(t+1) - [(AV(t) + P - C_init - C_maint - C_coi)(1 + j) + 特別積立金(t+1)]``,
    rebuilt from the charge cells rather than from the recursion that produced it.
    """
    built = (av_pp_at(t, "AFT_PREM") - charge_maint(t) - charge_coi(t)) \
        * (1.0 + credit_rate_mth()) + special_reserve_pp(t + 1)
    return av_pp(t + 1) - built


def check_av_roll_fwd():
    """True when the 積立金 recursion closes in every projected month.

    The identity the whole product hangs on: premium in, three charges out, interest
    credited, in that order.  :func:`check_av_roll_fwd_resid` gives the signed residual
    of the month that failed.
    """
    tol = roll_fwd_tol * max(1.0, sum_assured())                     # noqa: F821
    return all(abs(check_av_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_cv_ledger_resid(t):
    """The surrender-benefit ledger residual in month t; zero everywhere.

    :func:`claims` ``(t, "LAPSE")`` less an independent rebuild of it from
    ``CV(t+1)``, the decrement split and the APL advance — with no reference to the
    cells that produced the claim.  A model paying surrenders on :func:`av_pp`, or
    valuing them before that month's interest, or forgetting the 低解約返戻金 suppression,
    would show up here.
    """
    if t >= proj_len():
        return 0.0
    cv = cv_pp(t + 1)
    apl_exit = (pols_if_apl(t) * (1.0 - mort_rate_mth(t)) * lapse_rate_mth(t)
                * (1.0 - apl_nonpay_share))                          # noqa: F821
    built = cv * pols_lapse(t) - min(loan_pp(t), cv) * apl_exit
    if target_action() == "surrender":
        built = built + cv * pols_target(t)
    return claims(t, "LAPSE") - built


def check_cv_ledger():
    """True when the surrender benefit equals ``CV(t+1)`` times the exits in every month.

    The surrender value is read **after** that month's interest and after the 市場価格調整,
    the 解約控除 and the 低解約返戻金 suppression, which is what ``CV(t+1)`` means; the
    rebuild is independent of the cells that produce the claim.
    """
    tol = roll_fwd_tol * max(1.0, sum_assured())                     # noqa: F821
    return all(abs(check_cv_ledger_resid(t)) <= tol
               for t in range(proj_len()))


def check_net_cf_resid(t):
    """The cash-flow ledger residual in month t; zero everywhere.

    :func:`net_cf` less the sum of the columns ``result_cf()`` publishes.  It is what
    would catch an account-value charge leaking into the cash flow: ``C_init``,
    ``C_maint`` and ``C_coi`` are internal transfers and appear in no column, so booking
    one as revenue alongside the premium that funded it would break this identity.
    """
    gross = (prem_to_av_pp(t) + charge_init(t)) * pols_payer(t)
    built = (gross - claims(t, "DEATH") - claims(t, "LAPSE")
             - conversions(t) - claim_expenses(t) - expenses(t)
             - commissions(t))
    return net_cf(t) - built


def check_net_cf():
    """True when the published columns add to :func:`net_cf` in every projected month."""
    tol = roll_fwd_tol * max(1.0, sum_assured())                     # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol for t in range(proj_len()))


def check_fx_ledger_resid(t):
    """The yen-ledger residual in month t; zero everywhere.

    ``net_cf_jpy(t) - [net_cf(t) e(t) + fx_spread_jpy(t)]``.  The identity states the
    whole currency layer: premiums translate at ``e + s``, benefits at ``e - s`` and the
    insurer's own costs at ``e``, so the yen net is the translated dollar net **plus**
    the spread income.  A model that translates the net figure at one rate fails here.
    """
    return net_cf_jpy(t) - (net_cf(t) * fx_rate(t) + fx_spread_jpy(t))


def check_fx_ledger():
    """True when the three-rate yen translation closes in every projected month."""
    tol = roll_fwd_tol * max(1.0, sum_assured() * fx_rate(0))        # noqa: F821
    return all(abs(check_fx_ledger_resid(t)) <= tol
               for t in range(proj_len()))


def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash
    flow on the same row.  ``net_cf`` carries the notes' own income-positive sign.
    ``net_cf_jpy`` and ``fx_spread_jpy`` are the translation block: the yen net is *not*
    the dollar net times anything, and the spread income is published rather than hidden
    inside it.  ``av_pp`` and ``cv_pp`` are the state columns and are stated at the
    **end** of the month, ``AV(t+1)`` and ``CV(t+1)``, which is where the surrender
    benefit on the same row is valued.  ``conversions`` is a column of zeros on every
    model point without the target rider.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "conversions": [conversions(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "net_cf_jpy": [net_cf_jpy(t) for t in ts],
            "fx_spread_jpy": [fx_spread_jpy(t) for t in ts],
            "av_pp": [av_pp(t + 1) for t in ts],
            "cv_pp": [cv_pp(t + 1) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy month t."""
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_payer": [pols_payer(t) for t in ts],
            "pols_if_apl": [pols_if_apl(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_target": [pols_target(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of the account-value and surrender layers, indexed by month t.

    The per-policy state, carrying no survivorship: the fund, its 予定利率 benchmark and
    the uplift measured against it, the three charges, and the three factors that stand
    between the 積立金 and the 解約返戻金.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "av_pp": [av_pp(t) for t in ts],
            "av0_pp": [av0_pp(t) for t in ts],
            "idb_pp": [idb_pp(t) for t in ts],
            "benefit_pp": [benefit_pp(t) for t in ts],
            "charge_init": [charge_init(t) for t in ts],
            "charge_maint": [charge_maint(t) for t in ts],
            "charge_coi": [charge_coi(t) for t in ts],
            "mva_rate": [mva_rate(t) for t in ts],
            "surr_charge_rate": [surr_charge_rate(t) for t in ts],
            "low_cv_rate": [low_cv_rate(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

pols_if_init = 1.0

roll_fwd_tol = 1e-9

target_dead_zone_mths = 12

dyn_lapse_beta = 2.0

dyn_lapse_floor = 0.5

dyn_lapse_cap = 2.5

apl_nonpay_share = 0.30

apl_int_rate = 0.0275

expense_acq = 300.0

expense_maint = 60.0

expense_claim = 150.0

inflation_rate = 0.01

comm_init_rate = 0.90

comm_renewal_rate = 0.03

comm_renewal_start = 12

comm_init_single_rate = 0.055

comm_trail_rate = 0.0075

comm_trail_years = 7

pd = ("Module", "pandas")
