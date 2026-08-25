# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Annuity_JP_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 4            # or switch the default

``t`` counts **completed policy years since issue**, 0-based, matching the technical
notes and ``product-spec.md``. Premiums fall at ``t = 0 .. m - 1``; the 保険料積立金
accumulates over ``t = 0 .. n`` where ``n = m + d``; the annuity is paid at
``t = n .. n + k - 1``; and :func:`proj_len` is ``n + k`` on the 確定年金 form. ``pols_if(t)``
is the in-force count at the **start** of year ``t`` and is the weight on that same
``result_cf()`` row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/individual_annuity/``, read at run time rather than stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Annuity_JP_A`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Annuity_JP_A.Data`, reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
mort_anchor_file        data.mort_anchor_table()            mort_anchor_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
pricing_table_file      data.pricing_table()                pricing_table.csv
expense_table_file      data.expense_table()                expense_table.csv
commute_factor_file     data.commute_factor_table()         commute_factor_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib wherever it has an analogue — ``pols_*`` for policy counts,
plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claims(t, kind)`` with an uppercase ``kind`` string, ``pols_if_at(t, timing)`` and
``av_pp_at(t, timing)`` for the within-year reads. The technical notes use compact
actuarial symbols instead. The mapping is:

=================  ==========================  =======================================
Notes symbol       Cells                       Meaning
=================  ==========================  =======================================
(model point row)  model_point()               The selected model point
x                  issue_age()                 契約年齢 (保険年齢) at issue
x + t              age(t)                      Attained age in year t
(none)             sex()                       Rating factor, M or F
m                  premium_term_y()            保険料払込期間 in years
d                  defer_gap_y()               据置期間 in years
n = m + d          annuitisation_t()           Policy year of the 年金支払開始日
(none)             annuity_start_age()         保険年齢 at the 年金支払開始日
k                  payout_term_y()             確定年金 payment period in years
g                  guar_term_y()               Guarantee period, life form only
t = 0..proj_len-1  proj_len()                  Projection horizon in years
P                  premium_pp()                Level office annual premium
rho                db_ratio()                  Death benefit / cumulative premiums
i_d                int_rate_defer()            予定利率, deferral
i_p                int_rate_payout()           予定利率, payout
beta               expense_loading()           予定事業費率 on premium
theta              annuitisation_charge()      年金支払開始時費用 on the 年金原資
NP(t)              prem_to_av_pp(t)            Net premium credited to the fund
q'(x+t)            mort_rate_pricing(t)        予定死亡率, fund recursion only
q(t)               mort_rate(t)                Best-estimate rate applied in year t
(table)            mort_rate_base(t)           Table rate before the [std] factor
q(x) by age        mort_rate_at_age(table, x)  Table lookup keyed by attained age
(0.85 / 1.10)      mort_be_factor(t)           Best-estimate factor, by phase
w(t)               lapse_rate(t)               解約・失効 rate applied in year t
(table)            lapse_rate_base(t)          Table lapse rate, before dynamics
M(t)               lapse_dyn_factor(t)         Dynamic-lapse multiplier
V(t)               av_pp(t)                    保険料積立金 at the start of year t
(within year)      av_pp_at(t, timing)         BEF_PREM / AFT_PREM / AFT_INT
SC(t)              surr_charge_pp(t)           解約控除 at time t
DB(t)              db_pp(t)                    死亡給付金 for a death in year t-1
(net of loans)     db_pp_net(t)                死亡給付金 less any loan balance
CV(t)              cv_pp(t)                    解約返戻金 at time t
(net of loans)     cv_pp_net(t)                解約返戻金 less any loan balance
F = V(n)           annuity_fund_pp()           年金原資
adue(k, i_p)       annuity_due_factor()        Annuity-due factor, certain form
adue_life(g, i_p)  annuity_due_life_factor()   Guaranteed-plus-life factor
B                  annuity_amount_pp()         基本年金額, struck once at t = n
B x 1{n<=t<n+k}    annuity_pp(t)               Instalment payable at the start of t
(factor table)     commute_factor(j)           年金の一括払 factor, j instalments left
(lump sum)         commute_value_pp()          Commuted value per contract
(dividend)         div_credit_pp(t)            契約者配当 declared in year t
(dividend)         div_acc_pp(t)               Accumulated 契約者配当 at time t
l(t)               pols_if(t)                  Contracts with an obligation open
l(t)(1-q), l(t+1)  pols_if_at(t, timing)       BEF_DECR / BEF_LAPSE / AFT_DECR
L(t)               lives_if(t)                 Probability the annuitant is alive
D(t)               pols_death(t)               Expected deaths in year t
W(t)               pols_lapse(t)               Expected lapses at the end of year t
(none)             pols_commute(t)             Contracts electing 年金の一括払
(none)             pols_maturity(t)            Contracts whose last instalment is paid
(APL)              apl_bal(t)                  自動振替貸付 balance per policy
(APL)              apl_engaged(t)              Whether the APL is carrying the premium
(loan)             loan_pp(t)                  契約者貸付 balance per policy
P x l(t)           premiums(t)                 Premium income
DB, CV, B, lump    claims(t, kind)             Benefit outgo by kind
ec x D(t)          claim_expenses(t)           Claim expense, its own column
E0, e(t)           expenses(t)                 Acquisition + maintenance
(none)             inflation_factor(t)         Expense inflation factor
c0, c_r            commissions(t)              Commission outgo
(loan advance)     policy_loans(t)             契約者貸付 advanced, an outflow
CF(t)              net_cf(t)                   Net cash flow, income positive
=================  ==========================  =======================================

Three names needed care.

``av_pp`` and ``cv_pp`` are **not** the same quantity and the difference is the product.
``av_pp`` is the 保険料積立金, which grows past cumulative premiums on the survivorship
release; ``cv_pp`` is the 解約返戻金, which is capped at the 死亡給付金 and therefore at
cumulative premiums. Clipping ``av_pp`` instead of ``cv_pp`` destroys the 年金原資, because
it is the un-clipped excess of the fund over the death benefit that buys the annuity. The
library's naming ruling puts the surrender quantity under ``cv_pp``, and this model keeps
both.

``pols_if`` and ``lives_if`` are two different in-force measures, following ``SPIA_US_S``.
``pols_if`` counts contracts with an obligation open; ``lives_if`` counts annuitants
alive. In the deferral phase they separate because lapse removes a contract without
removing a life. In the payout phase they separate for the opposite reason: on a 確定年金
the instalments are unconditional, so ``pols_if`` is flat through the certain period while
``lives_if`` runs down on the payout table. Collapsing the two is the single most likely
way to build this product wrongly.

``mort_rate_pricing`` is the 予定死亡率 used **only** inside the fund recursion, at 100% of
the death-cover table. ``mort_rate`` is the best-estimate decrement applied to the
in-force. They are different numbers in every year, because ``av_pp`` is a contractual
quantity and not an experience projection — and where actual mortality runs lighter than
``q'`` the insurer credits more survivorship than it earns and takes a 死差損, so the
mortality sensitivity is signed the opposite way round from a death-cover product.

.. rubric:: Two mortality tables, with the margin running opposite ways

The deferral phase reads 生保標準生命表2018（死亡保険用）and the payout phase
生保標準生命表2007（年金開始後用）— expressly not updated in 2018 — and :func:`mort_table_name`
switches between them at ``t = n``. Both are **valuation** tables, so neither is a
best-estimate basis, and the adjustment to them reverses sign at the same date: the
death-cover table carries a prudential margin against **death**, so a best-estimate basis
is 0.85 of it; the payout table carries a prudential margin against **longevity**, so a
best-estimate basis is 1.10 of it. :func:`mort_be_factor` is the one place that sign
lives. A model applying one factor to both tables has one of the two wrong.

Neither table is shipped. Both are [std] constructions anchored to quoted spot rates:
死亡保険用 is the canonical library-wide file, graduated log-linearly in ``ln q`` between its
sourced anchors, and 年金開始後用 is a Makeham law fitted to three of them. See the
:mod:`~.Annuity_JP_A.Data` docstring, and :func:`check_mort_graduation`, which asserts that
the shipped rates are still the ones the graduation produces.

.. rubric:: Modules that are off in the base run

Six of the notes' optional constructions are implemented and switched off at the anchor
cell, so that the base run reproduces the worked example while the machinery stays
visible and testable. Each is a model point column, so a non-anchor point exercises it:

- **保証期間付終身年金**, ``payout_form = "life_guar"``: instalments unconditional for ``g``
  years and life-contingent after, priced on :func:`annuity_due_life_factor` at 100% of
  the payout table, with :func:`proj_len` running to that table's terminal age. Held at
  the issue basis **[std]** — the election is really priced on the 基礎率 in force at the
  年金支払開始日, which no model can know, and that is why base-run take-up is zero. Model
  points 4 and 9, the second being the anchor cell with nothing changed but the payout
  form: the life form with ``g = 10`` gives ``B`` = ¥281,300 against ¥638,100 on the
  certain form out of the same 年金原資, because the annuity-due factor is 22.032668 against
  9.714338.
- **年金の一括払**, ``commute_rate``: the published factor table verbatim over 1-14
  remaining instalments and an implied 0.40% p.a. outside it **[std]**. Model point 5.
  Base take-up is zero for an arithmetic reason: at ``t = n`` the factor for ten remaining
  instalments returns about 1.10% **more** than the gross 年金原資, because the factors come
  from one carrier and the payout 予定利率 from another and the composite does not reconcile
  them. Switching it on switches on a composite artefact, not a product feature.
- **自動振替貸付**, ``apl_on``: while the 解約返戻金 can carry the outstanding balance plus one
  more premium, the lapse decrement is suppressed and the insurer lends the premium at the
  contractual cap of 8% p.a.; the balance compounds and is deducted from the 死亡給付金 and
  from the 年金原資. It is **not** a no-lapse rule — the moment principal and interest
  outgrow the surrender value the contract lapses. Model point 7, where it engages at
  ``t = 2``, carries the contract for six years and then terminates it at ``t = 8``. One
  carrier's product has no such facility at all.
- **契約者貸付**, ``loan_on``: a loan of half the 解約返戻金 drawn at policy year 20 **[std]**,
  compounding at 2.40% p.a. and capped at the 解約返戻金, deducted from the 死亡給付金 and from
  the 年金原資. Model point 8.
- **契約者配当**, ``div_rate``: zero declared in the base run, machinery retained. A declared
  rate credits :func:`div_credit_pp` on the fund each year, accumulates it at the 配当積立利率
  and applies it at ``t = n`` as a single premium **increasing the 基本年金額**. Under the
  税制適格特約 it may never be paid in cash before annuitisation. Model point 8.
- **Dynamic lapse**, ``rate_new``: ``M(t) = min(2, max(1, 1 + phi max(0, i_new - i_d)))``
  with ``phi = 20`` **[std]**. Premiums and the 予定利率 are fixed at issue, so there is no
  premium-shock lapse on this chassis; the driver runs the other way, a rise in
  new-business 予定利率 making an in-force contract relatively unattractive. Model point 8.

減額, 払済 and 復活 are **not** implemented **[std scope]**. On an annual grid a premium
unpaid at ``t`` terminates the contract at ``t``: there is no partial-year 払込猶予期間 state
and no reinstatement re-entry, so this model's ``lapse_rate`` is a net-of-復活 rate by
construction and a user substituting a gross experience rate will over-decrement.

.. rubric:: Sign convention

The notes' ``CF(t)`` is already **income positive**, which is the library-wide sign of
:func:`net_cf`, so there is no ``liability_cf`` companion to publish here — that absence
is a fact about which orientation the notes chose, not an omission. A reader comparing the
payout years with ``SPIA_US_S``, whose notes print outgo-positive, must flip the sign:
this model's payout rows are large negatives.

.. rubric:: The absences are product facts

There is no premium income after 払込満了 and none at all once the annuity is in payment;
there is no lapse decrement and no surrender value from ``t = n - 1``, because surrender
is unavailable from the 年金支払開始日; and there is no maturity benefit, because the contract
does not mature — it annuitises. Each of those is stated in a formula rather than left to
inference.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
# --- Model point attributes ------------------------------------------------

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The annuitant's sex, ``M`` or ``F``; a rating factor on both mortality tables."""
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def issue_age():
    """x: the 契約年齢 at issue, on 保険年齢 (age nearest birthday) [REG-R20].

    The basis 標準生命表2018 is built for.  A model ageing its points on 満年齢 must say so
    and say what it does about the half-year difference; this one does not.
    """
    return int(model_point()["issue_age"])


def premium_term_y():
    """m: the 保険料払込期間 in years; at least ten under the 税制適格特約 [R10]."""
    return int(model_point()["premium_term_y"])


def defer_gap_y():
    """d: the 据置期間 in years, between 払込満了 and the 年金支払開始日 [S6].

    Zero is a valid model point and a different product; 払込満了 and 年金支払開始日 are
    different dates and collapsing them moves the 年金原資 by several per cent.
    """
    return int(model_point()["defer_gap_y"])


def annuity_start_age():
    """The 保険年齢 at the 年金支払開始日; at least 60 under the 税制適格特約 [R10].

    Derived rather than free: it must equal ``x + m + d``, and the model rejects a model
    point where it does not, because two spellings of one date is how a projection
    silently annuitises on the wrong year.
    """
    v = int(model_point()["annuity_start_age"])
    if v != issue_age() + premium_term_y() + defer_gap_y():
        raise ValueError("annuity_start_age is not issue_age + m + d")
    return v


def premium_pp():
    """P: the level office annual premium, guaranteed for the whole 保険料払込期間.

    There is no review right [S2] [S4] [S5] [S6], so the insurer has no unilateral
    repricing lever and all ``m`` premiums are inside the contract boundary.
    """
    return float(model_point()["premium_pp"])


def payout_form():
    """The annuity form: ``certain`` (確定年金) or ``life_guar`` (保証期間付終身年金).

    The base form is 確定年金 chosen at issue, whose 基本年金額 is struck once at ``t = n``
    from the issue basis [S2] [S3].  The life form is an election priced on the 基礎率 in
    force at the 年金支払開始日 [S2] [S9]; holding it at the issue basis is a **[std]**
    assumption and the reason base-run take-up is zero.
    """
    v = model_point()["payout_form"]
    if v not in ("certain", "life_guar"):
        raise ValueError("invalid payout_form")
    return v


def payout_term_y():
    """k: the 確定年金 payment period in years; 10 or 15 under the 税制適格特約 [R10] [R16]."""
    return int(model_point()["payout_term_y"])


def guar_term_y():
    """g: the guarantee period of the 保証期間付終身年金 form, in years [S4] [R16]."""
    return int(model_point()["guar_term_y"])


def db_ratio():
    """rho: the 死亡給付金 as a multiple of cumulative premiums paid.

    1.00 on the composite and 0.70 on both retrieved tontine designs [S3] [S10].  It sits
    on the model point rather than in a code branch because a tontine is the same chassis
    with a different death-benefit ratio under the same surrender ceiling.
    """
    return float(model_point()["db_ratio"])


def tax_rider():
    """Whether the 税制適格特約 is attached [S1] [R10].

    It constrains the contract rather than the cash flows — ten years of premiums, a
    start age of 60 or more, a payment period of ten years or more, no cash refund of a
    減額 — so it validates the model point and then does nothing else here.
    """
    v = bool(model_point()["tax_rider"])
    if v and (premium_term_y() < 10 or annuity_start_age() < 60
              or (payout_form() == "certain" and payout_term_y() < 10)
              or (payout_form() == "life_guar" and guar_term_y() < 10)):
        raise ValueError("model point does not satisfy the 税制適格特約 conditions")
    return v


def apl_on():
    """Whether the 自動振替貸付 module is switched on; false in the base run [S4] [REG-R14]."""
    return bool(model_point()["apl_on"])


def loan_on():
    """Whether the 契約者貸付 module is switched on; false in the base run [S4] [S11]."""
    return bool(model_point()["loan_on"])


def commute_rate():
    """The proportion electing 年金の一括払 at the 年金支払開始日 **[std]**; 0 in the base run.

    Commutation is available from the 年金支払開始日 to the last 年金支払日 [S2] [S4]; the model
    offers the election at ``t = n`` only **[std]**, which is where the published factor
    table is richest and where the arithmetic against the 年金原資 is checkable.
    """
    return float(model_point()["commute_rate"])


def div_rate():
    """The declared 契約者配当 rate on the fund **[std]**; zero in the base run [S4] [S11].

    Zero declared is a choice, not a product fact: the machinery is contractual, and under
    the 税制適格特約 the accumulated dividend may never be withdrawn before annuitisation and
    must be applied as a single premium increasing the 基本年金額 [S1] [S2] [R10].
    """
    return float(model_point()["div_rate"])


def rate_new():
    """i_new: the new-business 予定利率 the dynamic-lapse module compares against [S8].

    Flat over the projection on the shipped points.  Equal to :func:`int_rate_defer` in
    the base run, which makes :func:`lapse_dyn_factor` exactly 1.
    """
    return float(model_point()["rate_new"])


# --- Derived model point quantities ----------------------------------------

def annuitisation_t():
    """n = m + d: the policy year of the 年金支払開始日.

    The join between the two contracts this product really is.  Everything switches here:
    the mortality table, the sign of the best-estimate factor, the availability of
    surrender, and the direction of the cash flow.

    Read off :func:`annuity_start_age` rather than summed from ``m`` and ``d`` directly,
    which is the same number — that cells raises unless the model point's 年金支払開始日 equals
    ``x + m + d`` — but puts the consistency check on the path every projection takes.
    Reached only through :func:`tax_rider`, it would validate the base form's model points
    never, and two spellings of one date is how a projection silently annuitises on the
    wrong year.
    """
    return annuity_start_age() - issue_age()


def proj_len():
    """The projection horizon in policy years; ``result_cf()`` runs ``t = 0 .. proj_len - 1``.

    ``n + k`` on the 確定年金 form: there are no tail states, because the 確定年金 pays exactly
    ``k`` instalments and the contract ends [S2] [S4].  On the 保証期間付終身年金 form the
    horizon is instead the terminal age of the 年金開始後用 table — 122 for a male and 126 for
    a female [R3] [REG-R19] — because a life annuity has no other natural end.
    """
    if payout_form() == "certain":
        return annuitisation_t() + payout_term_y()
    return omega_age("annuity_payout_2007") - issue_age() + 1


def age(t):
    """The attained 保険年齢 at the start of policy year t: ``x + t``."""
    return issue_age() + t


# --- Assumption basis ------------------------------------------------------

def pricing_basis(item):
    """One row of the pricing and module basis table, as a float.

    A single lookup helper so that every basis item is read the same way and every one of
    them carries a ``provenance`` tag in the CSV rather than sitting as an untagged
    constant in a formula.
    """
    return float(data.pricing_table().loc[item, "value"])            # noqa: F821


def expense_basis(item):
    """One row of the best-estimate cash expense and commission table, as a float."""
    return float(data.expense_table().loc[item, "value"])            # noqa: F821


def int_rate_defer():
    """i_d: the deferral-phase 予定利率, 1.00% p.a., fixed at issue [S8]."""
    return pricing_basis("int_rate_defer")


def int_rate_payout():
    """i_p: the payout-phase 予定利率, 0.65% p.a., set separately from i_d [S5].

    Since ``i_p < i_d``, each yen of 年金原資 buys **less** annuity than a single-rate model
    would say.  Using the deferral rate to buy the annuity overstates the 基本年金額 by about
    1.55% at ``k = 10``.
    """
    return pricing_basis("int_rate_payout")


def expense_loading():
    """beta: the 予定事業費率 on each office premium, 6.5% **[std]**.

    One loading, not a three-way 新契約費 / 維持費 / 集金費 split: no retrieved document
    discloses one, the 算出方法書 is a 基礎書類 filed with the FSA and not published [REG-R2],
    and inventing a split no source can confirm is worth less than one round number
    calibrated against a published specimen [S6].
    """
    return pricing_basis("expense_loading")


def annuitisation_charge():
    """theta: the 年金支払開始時費用, 1.0% of the 年金原資, charged once **[std, new here]**."""
    return pricing_basis("annuitisation_charge")


def mort_table_name(t):
    """Which mortality table applies in policy year t.

    ``death_cover_2018`` in the deferral phase and ``annuity_payout_2007`` from ``t = n``.
    For contracts concluded from 2018-04-01 the standard valuation basis is
    生保標準生命表2018（死亡保険用）for death cover and 生保標準生命表2007（年金開始後用）for annuities in
    payment [REG-R10] [REG-R11] [R4].  An annuity computed off the death-cover table is
    wrong by construction and wrong in the expensive direction.
    """
    return "death_cover_2018" if t < annuitisation_t() else "annuity_payout_2007"


def mort_be_factor(t):
    """The best-estimate adjustment to the valuation table in policy year t.

    0.85 in the deferral phase and 1.10 from ``t = n`` **[std, new here]**.  Both tables
    are valuation bases carrying a prudential margin, and the margin runs opposite ways:
    against death before annuitisation, against **longevity** after it.  0.85 sits inside
    the range the death-cover margin implies, from 1/1.30 where the 130% cap binds to 1.00
    where no margin does [REG-R20]; the 作成概要 for the 2007 table was not retrieved, so the
    size of 1.10 is [unverified] and only its direction is structural.
    """
    if t < annuitisation_t():
        return pricing_basis("mort_be_factor_defer")
    return pricing_basis("mort_be_factor_payout")


def omega_age(table):
    """The terminal age of a shipped mortality table: 109 / 113 and 122 / 126.

    Read from ``data.mort_anchor_table()``, where it is a published fact about the real
    table rather than a property of the construction [REG-R18] [R3] [REG-R19].  ``q`` is
    truncated to 1 there.
    """
    return int(data.mort_anchor_table().loc[                         # noqa: F821
        (table, sex()), "omega_age"].iloc[0])


def mort_rate_at_age(table, x):
    """The shipped [std] rate of ``table`` at attained age ``x``, truncated to 1 at omega.

    The single point at which the model touches its mortality input, so a licensed table
    drops in by replacing ``mort_table.csv`` with a same-schema file.
    """
    if x >= omega_age(table):
        return 1.0
    return float(data.mort_table().loc[(table, sex(), x), "mort_rate"])  # noqa: F821


def mort_rate_base(t):
    """The table rate applying in policy year t, before the best-estimate factor."""
    return mort_rate_at_age(mort_table_name(t), age(t))


def mort_rate_pricing(t):
    """q'(x+t): the 予定死亡率, 100% of the 死亡保険用 table, used **only** in the fund.

    ``av_pp`` is a contractual quantity and not an experience projection, so its
    survivorship release is credited at the pricing rate whatever the best-estimate basis
    says.  Where actual mortality runs lighter than ``q'``, the insurer credits more
    survivorship than it earns and takes a 死差損.
    """
    return mort_rate_at_age("death_cover_2018", age(t))


def mort_rate(t):
    """q(t): the best-estimate mortality rate applied to the in-force in policy year t.

    The table rate of the phase times :func:`mort_be_factor`, capped at 1.  Two tables, two
    factors, and the factors point opposite ways; see the Space docstring.
    """
    return min(1.0, mort_be_factor(t) * mort_rate_base(t))


def lapse_rate_base(t):
    """The [std] table 解約・失効 rate in policy year t, before any dynamic multiplier.

    6.0 / 5.0 / 4.5 / 4.0 percent over the first ten policy years, 3.0% for the rest of
    the 保険料払込期間, 1.0% through the 据置期間 — no premium is due there, so the commonest
    lapse trigger is absent — and **zero from t = n - 1**, because that year ends on the
    年金支払開始日 where surrender is no longer available [S2] [S4].  The only public
    calibration point is a market-wide 3.4% for FY2024 whose denominator is 契約高, not
    policy count [R15] [REG-R31]; the duration shape is a standardization.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    if t >= annuitisation_t() - 1:
        return float(tbl.loc[("pre_annuitisation", 0), "lapse_rate"])
    if t >= premium_term_y():
        return float(tbl.loc[("defer_gap", 0), "lapse_rate"])
    seg = tbl.loc["premium_paying"]
    return float(seg.loc[max(y for y in seg.index if y <= t), "lapse_rate"])


def lapse_dyn_factor(t):
    """M(t): the dynamic-lapse multiplier **[std]**; 1 in the base run.

    ``min(cap, max(1, 1 + phi max(0, i_new(t) - i_d)))`` with ``phi`` = 20 and a cap of 2.
    Premiums and the 予定利率 are both fixed at issue, so there is no premium-shock lapse and
    no rate-driven surrender on this chassis.  The economic driver runs the other way: when
    new-business 予定利率 rise above the rate at issue — as they did in 2025, for the first
    time in about forty years [S8] — an in-force contract becomes relatively unattractive
    and lapse should rise.
    """
    excess = max(0.0, rate_new() - int_rate_defer())
    return min(pricing_basis("lapse_dyn_cap"),
               max(1.0, 1.0 + pricing_basis("lapse_dyn_phi") * excess))


def lapse_rate(t):
    """w(t): the annual 解約・失効 rate applied at the end of policy year t.

    The table rate times the dynamic multiplier, capped at 1 — except where the 自動振替貸付
    module is carrying the contract, which suppresses the decrement entirely, and except in
    the year that module can no longer carry it, where the whole in-force lapses [S4]
    [REG-R14].  Zero from ``t = n - 1`` in every case.
    """
    if apl_on() and t < premium_term_y():
        if apl_bal(t) > cv_pp(t):
            return 1.0
        if apl_engaged(t):
            return 0.0
    return min(1.0, lapse_rate_base(t) * lapse_dyn_factor(t))


# --- The 保険料積立金 recursion ------------------------------------------------

def prem_to_av_pp(t):
    """NP(t): the office premium net of the 予定事業費率, credited to the fund.

    ``P (1 - beta)`` while ``t < m`` and zero after.  Credited whether or not the premium
    arrives in cash: under the 自動振替貸付 module the insurer lends it, so the fund is fed
    and the loan balance grows instead.
    """
    return premium_pp() * (1.0 - expense_loading()) if t < premium_term_y() else 0.0


def av_pp(t):
    """V(t): the 保険料積立金 per policy at the start of year t, before that year's premium.

    A net-level-premium accumulation carrying a **survivorship release**::

        V(0)   = 0
        V(t+1) = [ (V(t) + NP(t)) (1 + i_d) - q'(x+t) DB(t+1) ] / (1 - q'(x+t))

    The division by ``(1 - q')`` is the release: the premiums of those who die go to the
    survivors net of the death benefit paid.  Because ``DB`` is capped at cumulative
    premiums while ``V`` is not, that release turns **positive from the duration at which V
    first exceeds DB**, and that excess is precisely the survival benefit a
    生存保障重視型 design buys.  Lapse does not appear: the surrender release is the 解約控除,
    which accrues to the insurer and not to the surviving fund.  Zero after annuitisation,
    where the fund has been converted into the annuity and the liability is the instalment
    stream instead.
    """
    if t <= 0 or t > annuitisation_t():
        return 0.0
    q = mort_rate_pricing(t - 1)
    return (av_pp_at(t - 1, "AFT_INT") - q * db_pp(t)) / (1.0 - q)


def av_pp_at(t, timing):
    """The 保険料積立金 per policy at a point inside policy year t.

    ``"BEF_PREM"``
        V(t), the start of the year before the premium is credited; the same
        number as :func:`av_pp`.

    ``"AFT_PREM"``
        after the year's net premium is credited, before interest.

    ``"AFT_INT"``
        after the 予定利率 is credited, before the survivorship release and the
        death benefit are settled.
    """
    if timing == "BEF_PREM":
        return av_pp(t)
    if timing == "AFT_PREM":
        return av_pp(t) + prem_to_av_pp(t)
    if timing == "AFT_INT":
        return av_pp_at(t, "AFT_PREM") * (1.0 + int_rate_defer())
    raise ValueError("invalid timing")


# --- Deferral-phase benefit amounts ----------------------------------------

def db_pp(t):
    """DB(t): the 死亡給付金 payable for a death in year t - 1, paid at t.

    ``rho P min(t, m)`` — the annual-grid form of the contractual 月払保険料 x 経過月数 [S2]
    [S4], which 所令211①ロ requires to increase with duration or with cumulative premiums
    [R10].  It **stops growing at 払込満了**, because no further premium is paid: a model
    that keeps accruing it to ``n`` overstates deferral-phase claims by ``d`` years' worth
    of premium.
    """
    return db_ratio() * premium_pp() * min(t, premium_term_y())


def db_pp_net(t):
    """The 死亡給付金 actually paid: :func:`db_pp` less any loan principal and interest.

    Unpaid premiums, 契約者貸付 and 自動振替貸付 balances are deducted from the benefit [S2]
    [S4].  Equal to :func:`db_pp` in the base run, where both loan modules are off.
    """
    return max(0.0, db_pp(t) - loan_pp(t) - apl_bal(t))


def surr_charge_pp(t):
    """SC(t): the 解約控除 at time t **[std]**.

    One annual premium running off linearly over ten policy years.  Both 約款 state the
    shape and not the parameters — 「ご契約後短期間で解約されたときには、解約返還金がない場合があります」 [S2] and
    「まったくないか、あってもごくわずか」 [S4] — and the formula sits in the unpublished 算出方法書
    [REG-R2].  The base amount of one annual premium is what makes the sourced invariant
    hold: the first-year 解約返戻金 is nil-or-negligible against a full year's premium.
    """
    yrs = pricing_basis("surr_charge_years")
    base = premium_pp() * pricing_basis("surr_charge_prems")
    return base * max(0.0, (yrs - t) / yrs)


def cv_pp(t):
    """CV(t): the 解約返戻金 per policy at time t.

    ``min(max(0, V(t) - SC(t)), DB(t))`` before annuitisation and **zero from t = n**,
    because surrender is not available from the 年金支払開始日 [S2] [S4] [R16].  The upper cap
    is the sourced ceiling 「解約返還金は…死亡給付金の額を限度とします」 [S2], and it is what the other
    carrier means by 「一定期間経過後は死亡給付金と同額になります」 [S4]: beyond the crossover the surrender
    value and the death benefit are literally the same number.

    That cap also reverses the sign of the late-duration lapse sensitivity.  From the
    crossover a surrender returns exactly what was paid in and no interest, while the fund
    behind it is worth more, so late-duration lapse is **profitable** to the insurer and a
    prudent reserving basis loads it down, not up.
    """
    if t >= annuitisation_t():
        return 0.0
    return min(max(0.0, av_pp(t) - surr_charge_pp(t)), db_pp(t))


def cv_pp_net(t):
    """The 解約返戻金 actually paid on surrender: :func:`cv_pp` less any loan balance.

    Equal to :func:`cv_pp` in the base run, where both loan modules are off.
    """
    return max(0.0, cv_pp(t) - loan_pp(t) - apl_bal(t))


# --- The loan modules ------------------------------------------------------

def apl_engaged(t):
    """Whether the 自動振替貸付 is carrying the premium in policy year t; false in the base run.

    True while the module is on, a premium is still due, the 解約返戻金 is at least one
    premium, and the outstanding balance has not yet outgrown the 解約返戻金 [S4].  That last
    condition is the whole point: 自動振替貸付 is a policyholder election, not a no-lapse rule
    [REG-R14], and one carrier's product does not offer it at all [S2].
    """
    if not apl_on() or t >= premium_term_y():
        return False
    return cv_pp(t) >= premium_pp() and apl_bal(t) <= cv_pp(t)


def apl_bal(t):
    """The 自動振替貸付 principal and interest per policy at time t; zero in the base run.

    Each premium the module lends is added to the balance and the whole compounds at the
    contractual cap of 8% p.a. [S4], adopted at the cap **[std]**.  8% against a surrender
    value that is itself capped at cumulative premiums is why the facility carries a
    contract for a few years and not for a term: the moment principal and interest outgrow
    the 解約返戻金 the contract lapses [S4], which is what :func:`lapse_rate` does with it.
    """
    if not apl_on() or t <= 0:
        return 0.0
    prev = apl_bal(t - 1)
    if apl_engaged(t - 1):
        prev = prev + premium_pp()
    if prev <= 0.0:
        return 0.0
    return prev * (1.0 + pricing_basis("apl_rate"))


def loan_pp(t):
    """The 契約者貸付 principal and interest per policy at time t; zero in the base run.

    A loan of half the 解約返戻金 drawn at policy year 20 **[std]**, compounding at 2.40%
    p.a. on the current issue cohort [S11] [S8] and capped at the 解約返戻金 [S4] [REG-R14].
    Deducted from the 死亡給付金 and from the 年金原資, so it does not touch :func:`av_pp`: the
    fund is a contractual accumulation and the loan is a separate account against it.
    """
    if not loan_on() or t < pricing_basis("loan_draw_year"):
        return 0.0
    if t == pricing_basis("loan_draw_year"):
        return pricing_basis("loan_draw_frac") * cv_pp(t)
    cap = cv_pp(t) if t < annuitisation_t() else av_pp(annuitisation_t())
    return min(loan_pp(t - 1) * (1.0 + pricing_basis("loan_rate")), cap)


def policy_loans(t):
    """The 契約者貸付 advanced in policy year t, an outflow; zero in the base run.

    Only the drawdown is a cash flow.  The balance is recovered by deduction from the
    死亡給付金, the 解約返戻金 or the 年金原資, which is where :func:`db_pp_net`,
    :func:`cv_pp_net` and :func:`annuity_fund_pp` take it.
    """
    if not loan_on() or t != pricing_basis("loan_draw_year"):
        return 0.0
    return loan_pp(t) * pols_if(t)


# --- 契約者配当 ---------------------------------------------------------------

def div_credit_pp(t):
    """The 契約者配当 declared in policy year t per policy **[std]**; zero in the base run.

    ``div_rate`` on the fund at the start of the year.  The composite is a
    5年ごと利差配当 design [S4]; declaring annually on the fund is a **[std]** simplification of
    it, and the declared rate rather than the frequency is what moves the answer.
    """
    if t <= 0 or t > annuitisation_t():
        return 0.0
    return div_rate() * av_pp(t)


def div_acc_pp(t):
    """The accumulated 契約者配当 per policy at time t; zero in the base run.

    Accumulated at the 配当積立利率 of 0.60% p.a. [S11].  Under the 税制適格特約 it cannot be
    withdrawn before annuitisation and must be applied as a single premium increasing the
    基本年金額, never paid in cash [S1] [S2] [R10] — so it appears in
    :func:`annuity_amount_pp` and nowhere in the cash flow before ``t = n``.
    """
    if t <= 0:
        return 0.0
    return ((div_acc_pp(t - 1) + div_credit_pp(t - 1))
            * (1.0 + pricing_basis("div_int_rate")))


# --- The annuitisation transition ------------------------------------------

def annuity_fund_pp():
    """F = V(n): the 年金原資, the fund out of which the annuity is bought.

    Struck once, at ``t = n``, net of any outstanding loan balance [S2] [S4].  One carrier
    pins the definition down by publishing both 一括受取率 (``F / Pm``) and 年金受取率
    (``kB / Pm``) at one model point [S6], which is what makes the loading calibration
    checkable rather than merely plausible.
    """
    n = annuitisation_t()
    return max(0.0, av_pp(n) - loan_pp(n) - apl_bal(n))


def annuity_due_factor():
    """adue(k, i_p): the k-year annuity-due factor at the payout 予定利率.

    ``(1 - (1 + i)^-k) / i x (1 + i)``.  The rate is ``i_p`` = 0.65%, **not** the deferral
    rate: the payout phase is priced on its own 予定利率, published separately and left
    unchanged when that carrier's deferral rates moved [S5].
    """
    i = int_rate_payout()
    k = payout_term_y()
    if i == 0.0:
        return float(k)
    return (1.0 - (1.0 + i) ** (-k)) / i * (1.0 + i)


def annuity_due_life_factor():
    """adue_life(g, i_p): the guaranteed-plus-life annuity-due factor at annuitisation.

    ``sum over j >= 0 of max(1{j < g}, jp_(x+n)) / (1 + i_p)**j`` on the 年金開始後用 table at
    **100%** — a pricing basis, not the best-estimate factor.  At the anchor cell's fund
    and ``g = 10`` this is about 22.03 against 9.71 on the certain form, which is why the
    same 年金原資 buys ¥281,300 a year as a life annuity and ¥638,100 a year as a ten-year
    certain one.  That ratio is the product fact the module exists to show.
    """
    i = int_rate_payout()
    g = guar_term_y()
    a0 = annuity_start_age()
    om = omega_age("annuity_payout_2007")
    total = 0.0
    surv = 1.0
    j = 0
    while a0 + j <= om:
        total += max(1.0 if j < g else 0.0, surv) / (1.0 + i) ** j
        surv = surv * (1.0 - mort_rate_at_age("annuity_payout_2007", a0 + j))
        j = j + 1
    return total


def annuity_amount_pp():
    """B: the 基本年金額, the annual instalment, struck once at t = n and never recomputed.

    ``floor( (F (1 - theta) + accumulated dividend) / adue / 100 ) x 100``.  The rounding
    down to the nearest ¥100 is contractual rather than a display convention **[std, new
    here]** — Japanese specimens are published at that granularity [S3] [S5] [S6] [S10] —
    so it happens inside the model.
    """
    step = pricing_basis("annuity_round_to")
    factor = (annuity_due_factor() if payout_form() == "certain"
              else annuity_due_life_factor())
    gross = (annuity_fund_pp() * (1.0 - annuitisation_charge())
             + div_acc_pp(annuitisation_t()))
    return float(int(gross / factor / step)) * step


def annuity_pp(t):
    """B x 1{in payment}: the annuity instalment per contract payable at the start of t.

    Paid in advance, once a year, from the 年金支払開始日.  On the 確定年金 form there are
    exactly ``k`` of them and then the contract ends; on the 保証期間付終身年金 form the
    instalment is the same amount for as long as the contract is in force, and it is
    :func:`pols_if` rather than the amount that carries the life contingency.
    """
    n = annuitisation_t()
    if t < n:
        return 0.0
    if payout_form() == "certain" and t >= n + payout_term_y():
        return 0.0
    return annuity_amount_pp()


def commute_factor(j):
    """The 年金の一括払 factor for j remaining instalments [S2]; **[std]** outside 1-14.

    The published table verbatim where it reaches, and an annuity-due at the 0.40% p.a. it
    implies outside it.  That rate is **not** the model's payout 予定利率 of 0.65%, and the
    composite does not reconcile the two: the factors come from one carrier [S2] and the
    payout rate from another [S5].  A production model must re-derive the factors on its
    own payout basis.
    """
    if j <= 0:
        return 0.0
    tbl = data.commute_factor_table()                                # noqa: F821
    if j <= int(tbl.index.max()):
        return float(tbl.loc[j, "factor"])
    i = pricing_basis("commute_int_rate")
    return (1.0 - (1.0 + i) ** (-j)) / i * (1.0 + i)


def commute_value_pp():
    """The lump sum per contract electing 年金の一括払 at the 年金支払開始日 [S2] [S4].

    ``B`` times the factor for the whole certain or guaranteed period.  At the anchor
    cell's numbers this returns about 1.10% **more** than the gross 年金原資, which is why
    base-run take-up is zero: switching commutation on switches on a composite artefact
    rather than a product feature.
    """
    j = (payout_term_y() if payout_form() == "certain" else guar_term_y())
    return annuity_amount_pp() * commute_factor(j)


# --- In-force and decrements -----------------------------------------------

def pols_if(t):
    """l(t): contracts with an obligation open at the **start** of policy year t.

    1.0 at ``t = 0``.  Through the deferral phase the notes' recursion
    ``l(t+1) = l(t)(1 - q(t))(1 - w(t))``.  From ``t = n`` the rules change with the payout
    form: on the 確定年金 the instalments are unconditional, so ``l`` is **flat** through the
    certain period and drops to zero once the last one is paid; on the 保証期間付終身年金 it is
    flat through the guarantee period and then runs off on the best-estimate payout basis.

    This is the weight on every cash flow of the same ``result_cf()`` row.  Do not
    decrement it by mortality during a certain or guaranteed period: deaths there pay the
    PV of the unpaid instalments, or the recipient elects continuation, and the base run
    assumes continuation at 100% **[std]** so that the stream is unchanged [S2] [R16].
    """
    n = annuitisation_t()
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return 1.0
    if t <= n:
        return pols_if_at(t - 1, "AFT_DECR")
    base = pols_if(n) - pols_commute(n)
    if payout_form() == "certain":
        return base if t < n + payout_term_y() else 0.0
    guaranteed = 1.0 if t - n < guar_term_y() else 0.0
    return base * max(guaranteed, lives_if(t) / lives_if(n))


def pols_if_at(t, timing):
    """The number of contracts in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year before any decrement; the same number as
        :func:`pols_if` and the weight on that year's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before lapses — the notes' processing order is **death
        before lapse** **[std order]**, so this is the population lapses are
        taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-year state.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_DECR":
        if t < annuitisation_t():
            return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def lives_if(t):
    """L(t): the probability the annuitant is alive at the start of policy year t.

    ``L(t+1) = L(t)(1 - q(t))`` **throughout**, on whichever table the phase reads.  It is
    carried separately from :func:`pols_if` because the two measure different things: in
    the deferral phase lapse removes a contract without removing a life, and in the payout
    phase the 確定年金 obligation survives the annuitant.  At the anchor cell ``lives_if``
    falls from 0.91268274 to 0.77848987 over the ten payout years without moving a single
    yen of projected cash flow, which is the clearest statement of why the two are not one
    cells.
    """
    if t <= 0:
        return 1.0
    return lives_if(t - 1) * (1.0 - mort_rate(t - 1))


def pols_death(t):
    """D(t): expected deaths in policy year t, taken at the **end** of the year.

    ``l(t) q(t)`` in the deferral phase.  **Zero** inside a certain or guaranteed period,
    where the obligation does not depend on survival; on the 保証期間付終身年金 form after the
    guarantee it is the run-off of :func:`pols_if` itself.
    """
    n = annuitisation_t()
    if t < n:
        return pols_if(t) * mort_rate(t)
    if payout_form() == "certain":
        return 0.0
    if t - n < guar_term_y() - 1:
        return 0.0
    return max(0.0, pols_if(t) - pols_if(t + 1))


def pols_lapse(t):
    """W(t): expected lapses at the end of policy year t, from the survivors of mortality.

    ``l(t)(1 - q(t)) w(t)``, and zero from ``t = n - 1``: that year ends on the 年金支払開始日,
    where surrender is no longer available [S2] [S4].  A lapse applied there would remove
    contracts at ``t = n``, where ``cv_pp`` is zero — in-force would disappear with no
    payment and the annuity outgo would be understated.
    """
    if t >= annuitisation_t():
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def pols_commute(t):
    """Contracts electing 年金の一括払 at the 年金支払開始日; zero in the base run.

    A decrement at ``t = n`` only **[std]**: the elector takes the lump sum in place of the
    instalments and the contract terminates [S2] [S4].
    """
    if t != annuitisation_t():
        return 0.0
    return pols_if(t) * commute_rate()


def pols_maturity(t):
    """The count whose cover ends at the scheduled end of the contract, paid for or not.

    The library-wide meaning of the name, as in ``BasicTerm_S`` and ``Term_UK_A``: the
    contracts reaching the scheduled end, whether or not anything is paid for reaching it.
    Here that end is the last 確定年金 instalment, so this is non-zero only at
    ``t = n + k - 1``, and zero on the 保証期間付終身年金 form, which has no fixed end.

    **There is no** ``claims(t, "MATURITY")`` **on this product**, and the absence is a
    product fact rather than a gap: the 確定年金 pays exactly ``k`` instalments and then the
    contract simply ends [S2] [S4], so the money attaching to this year is the ordinary
    instalment in ``claims(t, "ANNUITY")`` and nothing further falls due.  The count is
    still needed for the in-force roll-forward to close, because the survivors of that year
    neither die nor lapse; see :func:`check_pols_roll_fwd`.
    """
    if payout_form() != "certain":
        return 0.0
    if t != annuitisation_t() + payout_term_y() - 1:
        return 0.0
    return pols_if(t) - pols_commute(t)


# --- Cash flows ------------------------------------------------------------

def premiums(t):
    """P l(t): premium income at the start of policy year t, an inflow.

    Level and guaranteed for the whole 保険料払込期間, and **nothing** after 払込満了 — the
    据置期間 and the payout phase carry no premium at all.  Zero as well once the 自動振替貸付
    module has started carrying the contract, because there the insurer lends the premium
    rather than receiving it, and a policyholder who has stopped paying does not resume in
    the year the facility fails.
    """
    if t >= premium_term_y():
        return 0.0
    if apl_on() and (apl_engaged(t) or apl_bal(t) > 0.0):
        return 0.0
    return premium_pp() * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"ANNUITY"`` — published as ``claims_annuity`` — is a **living** benefit here: it is
    paid on the annuitant *surviving* to a payment date, never on death.  The same column
    name carries a **death** benefit in ``IncomeTerm_JP_S``, where the survivor income runs
    to the end of the term after the life assured dies, and a living benefit again in
    ``LTC_JP_S``.  The name is the benefit's *form* — a stream rather than a lump sum — so
    the contingency has to be read off the product, and this is where it is stated.

    ``"ANNUITY"``
        the instalments paid in advance at the start of year t, to every contract with an
        obligation open that has not commuted.  Past the guarantee period of the
        保証期間付終身年金 form the instalment is payable only while the annuitant is alive;
        over the 確定年金's certain period it is unconditional, which is prepaid
        survival-contingent cover and still not a benefit death can trigger.

    ``"DEATH"``
        the 死亡給付金 for deaths at the end of the year, ``DB(t+1) D(t)``, net of
        any loan balance.  Zero inside a certain or guaranteed period.

    ``"LAPSE"``
        surrender payments at the end of the year, ``CV(t+1) W(t)``, net of any
        loan balance.  Zero from ``t = n - 1``.

    ``"COMMUTATION"``
        the 年金の一括払 lump sums at the 年金支払開始日; zero in the base run.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("ANNUITY", "DEATH", "LAPSE", "COMMUTATION"))
    if kind == "ANNUITY":
        return annuity_pp(t) * (pols_if(t) - pols_commute(t))
    if kind == "DEATH":
        return db_pp_net(t + 1) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp_net(t + 1) * pols_lapse(t)
    if kind == "COMMUTATION":
        return commute_value_pp() * pols_commute(t)
    raise ValueError("invalid kind")


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^t`` **[std]**, pi = 1%."""
    return (1.0 + expense_basis("inflation_rate")) ** t


def claim_expenses(t):
    """ec D(t): the claim handling expense on the year's death claims **[std]**.

    ¥5,000 per death claim and none on surrender.  A cells of its own, a ``claim_expenses``
    column of its own in :func:`result_cf`, and a term of its own in :func:`net_cf` — the
    library-wide meaning: :func:`expenses` is acquisition and maintenance, and the expense
    that scales with claims rather than with in-force is never folded into it.
    """
    return expense_basis("expense_claim") * pols_death(t)


def expenses(t):
    """E0 and e(t): acquisition and maintenance expense in year t **[std]**.

    ¥30,000 per policy at ``t = 0``, then ¥4,000 per policy per year in the deferral phase
    and ¥2,000 once the annuity is in payment, both inflating at 1% p.a.  **Acquisition and
    maintenance only**: the claim handling expense is :func:`claim_expenses`, deducted
    explicitly in :func:`net_cf` and published as its own ``claim_expenses`` column, which
    is the library-wide meaning of the two names.  These are best-estimate **cash** expenses
    and are entirely separate from the 予定事業費率, which is a pricing loading living inside
    :func:`av_pp`.  Charging the loading against the cash flow, or projecting these into the
    fund, double-counts expense in one direction and destroys the calibration in the other.
    """
    acq = expense_basis("expense_acq") * pols_if(t) if t == 0 else 0.0
    maint = (expense_basis("expense_maint_defer") if t < annuitisation_t()
             else expense_basis("expense_maint_payout"))
    return acq + maint * inflation_factor(t) * pols_if(t)


def commissions(t):
    """Commission outgo in policy year t **[std]**.

    40% of the annual premium at ``t = 0``, then 2% of premium income for
    ``t = 1 .. m - 1``, and nothing after 払込満了.  Against a ¥180,000 annual premium this
    is a small acquisition cost, which is why the year-0 net cash flow of this product is a
    large **positive** — the mirror image of UK term assurance, where 150% of an annualized
    premium in upfront commission produces a deep new business strain.
    """
    init = (expense_basis("comm_init_rate") * premium_pp() * pols_if(t)
            if t == 0 else 0.0)
    renew = (expense_basis("comm_renewal_rate") * premiums(t)
             if 1 <= t < premium_term_y() else 0.0)
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy year t, **income positive**.

    Premiums less annuity instalments, death and surrender benefits, commutation lump
    sums, acquisition and maintenance expense, claim expense, commission and any loan
    advanced.  :func:`claim_expenses` is deducted as its own term rather than through
    :func:`expenses`.  The notes print the stream this way round, so this model publishes no
    ``liability_cf`` companion — that absence is a fact about which orientation the notes
    chose, not an omission.

    The shape to expect is a large positive at ``t = 0``, then thirty years of declining
    positive margin as surrender outgo grows against a shrinking premium base, then a
    decade of pure outgo once the annuity is in payment.
    """
    return (premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
            - commissions(t) - policy_loans(t))


# --- Roll-forward and ledger checks ----------------------------------------

def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``l(t) - l(t+1) - deaths - lapses - commutations - expiries``.  Expiries are non-zero
    only in the year the last 確定年金 instalment is paid, where the survivors neither die
    nor lapse — the contract simply ends — so without that term the final payout year
    appears to lose contracts with no cause.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            - pols_commute(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    The library-wide form of a roll-forward check: no argument, one bool over all t.
    :func:`check_pols_roll_fwd_resid` gives the signed residual of the year that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol                # noqa: F821
               for t in range(0, proj_len()))


def check_lives_roll_fwd_resid(t):
    """The survivorship roll-forward residual in policy year t; zero everywhere.

    ``L(t) - L(t+1) - L(t) q(t)``.  Carried separately from the in-force check because the
    two measures decrement differently, and a model that has quietly collapsed them would
    still close one of the two.
    """
    return lives_if(t) - lives_if(t + 1) - lives_if(t) * mort_rate(t)


def check_lives_roll_fwd():
    """True when the survivorship roll-forward closes in every projected policy year."""
    return all(abs(check_lives_roll_fwd_resid(t)) <= roll_fwd_tol               # noqa: F821
               for t in range(0, proj_len()))


def check_fund_resid(t):
    """The 保険料積立金 recursion residual in policy year t; zero over the deferral phase.

    ``(V(t) + NP(t))(1 + i_d) - q' DB(t+1) - (1 - q') V(t+1)``.  Scaled by the fund, so the
    tolerance means the same thing at every duration.  Zero by definition from ``t = n``,
    where there is no fund left to roll forward.
    """
    if t >= annuitisation_t():
        return 0.0
    q = mort_rate_pricing(t)
    return (av_pp_at(t, "AFT_INT") - q * db_pp(t + 1)
            - (1.0 - q) * av_pp(t + 1))


def check_fund():
    """True when the 保険料積立金 recursion closes in every deferral year.

    The identity that the survivorship release is exactly what is left after the death
    benefit is paid out of the accumulated fund.  A model that had put lapse into this
    recursion, or that had used the best-estimate rate instead of the 予定死亡率, would fail
    here rather than silently misstate the 年金原資.
    """
    scale = max(1.0, annuity_fund_pp())
    return all(abs(check_fund_resid(t)) <= roll_fwd_tol * scale           # noqa: F821
               for t in range(0, proj_len()))


def check_cv_cap_resid(t):
    """The 解約返戻金 ceiling residual at duration t; zero or negative is the breach.

    ``DB(t) - CV(t)``, which is non-negative at every deferral duration by the sourced
    ceiling [S2] [S4].  The residual is published unsigned rather than clipped so that the
    crossover — where it reaches exactly zero and stays there — is readable off it.
    """
    if t >= annuitisation_t():
        return 0.0
    return db_pp(t) - cv_pp(t)


def check_cv_cap():
    """True when the 解約返戻金 never exceeds the 死亡給付金 at any deferral duration.

    The product's sourced invariant [S2] [S4].  It is the fund, not the surrender value,
    that is allowed past the ceiling: clipping :func:`av_pp` instead of :func:`cv_pp` would
    pass this check and destroy the 年金原資.
    """
    return all(check_cv_cap_resid(t) >= -roll_fwd_tol * max(              # noqa: F821
        1.0, db_pp(annuitisation_t())) for t in range(0, proj_len()))


def check_annuity_total_resid(t):
    """The guaranteed-instalment residual in policy year t; zero everywhere.

    The instalment actually payable per contract less ``B``, over the certain period of the
    確定年金 or the guarantee period of the 保証期間付終身年金.  Zero outside that window.
    """
    n = annuitisation_t()
    guaranteed = (payout_term_y() if payout_form() == "certain" else guar_term_y())
    if t < n or t >= n + guaranteed:
        return 0.0
    return annuity_pp(t) - annuity_amount_pp()


def check_annuity_total():
    """True when the undiscounted guaranteed instalments sum to k B (or g B).

    The 確定年金 pays exactly ``k`` instalments of the same amount, regardless of survival
    [S2] [R16], and the 保証期間付終身年金 pays at least ``g`` of them [S4] [R16].  A model that
    had decremented the payout phase by mortality, or that had recomputed ``B`` after
    annuitisation, would fail here.
    """
    n = annuitisation_t()
    guaranteed = (payout_term_y() if payout_form() == "certain" else guar_term_y())
    total = sum(annuity_pp(t) for t in range(n, n + guaranteed))
    scale = max(1.0, annuity_amount_pp())
    return (all(abs(check_annuity_total_resid(t)) <= roll_fwd_tol * scale  # noqa: F821
                for t in range(0, proj_len()))
            and abs(total - guaranteed * annuity_amount_pp())
            <= roll_fwd_tol * scale)


def check_net_cf_resid(t):
    """The cash flow ledger residual in policy year t; zero everywhere.

    :func:`net_cf` less the sum of the columns ``result_cf()`` publishes.  It is the check
    that the published statement and the projected total are the same object, which is the
    one identity a reader of the output cannot verify for themselves.
    """
    return (net_cf(t) - premiums(t) + claims(t, "ANNUITY") + claims(t, "DEATH")
            + claims(t, "LAPSE") + claims(t, "COMMUTATION") + expenses(t)
            + claim_expenses(t) + commissions(t) + policy_loans(t))


def check_net_cf():
    """True when the published cash flow columns add up to :func:`net_cf` in every year."""
    scale = max(1.0, premium_pp())
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol * scale         # noqa: F821
               for t in range(0, proj_len()))


def mort_anchor_ages(table):
    """The ages at which ``table`` is anchored to a quoted rate, ascending.

    Read from ``data.mort_anchor_table()``.  On 死亡保険用 these are the sourced ages of the
    canonical library-wide table; on 年金開始後用 they are the three spot rates the Makeham
    construction is fitted to.
    """
    rows = data.mort_anchor_table().loc[(table, sex())]               # noqa: F821
    return [int(a) for a in sorted(rows["age"])]


def makeham_coeff(table):
    """(A, B, c) of the [std] Makeham law fitted to the three anchors of ``table``.

    Solved in closed form from equally spaced anchors: with ``mu = -ln(1 - q)`` and a
    spacing of ``h`` years, ``c**h`` is the ratio of the two successive differences.  The
    anchors are therefore reproduced exactly by construction.  Used for 年金開始後用 only —
    死亡保険用 is graduated log-linearly instead; see :func:`mort_rate_graduated`.
    """
    rows = data.mort_anchor_table().loc[(table, sex())]               # noqa: F821
    rows = rows.sort_values("age")
    ages = [int(a) for a in rows["age"]]
    mus = [-math.log(1.0 - float(q)) for q in rows["mort_rate"]]      # noqa: F821
    h = ages[1] - ages[0]
    ch = (mus[2] - mus[1]) / (mus[1] - mus[0])
    c = ch ** (1.0 / h)
    b = (mus[1] - mus[0]) / (c ** ages[0] * (ch - 1.0))
    return (mus[0] - b * c ** ages[0], b, c)


def mort_rate_graduated(table, x):
    """The rate the shipped table's own stated graduation produces at age ``x``.

    On ``death_cover_2018`` the graduation is **log-linear in age between the two
    neighbouring anchors** — linear in ``ln q``, evaluated in full double precision and
    rounded to five decimal places — which is the graduation the canonical library-wide
    死亡保険用 file states in its ``provenance`` column.  There is no extrapolation: every age
    the model can reach lies between two sourced anchors.

    On ``annuity_payout_2007`` it is the Makeham law of :func:`makeham_coeff`.  Two tables,
    two graduations, because the two anchor sets are different: the death-cover table is
    anchored at every published age the library uses, the payout table at three spot rates.
    """
    if table != "death_cover_2018":
        a, b, c = makeham_coeff(table)
        return 1.0 - math.exp(-(a + b * c ** x))                     # noqa: F821
    ages = mort_anchor_ages(table)
    if x in ages:
        return mort_rate_at_age(table, x)
    lo = max(a for a in ages if a < x)
    hi = min(a for a in ages if a > x)
    q_lo = math.log(mort_rate_at_age(table, lo))                     # noqa: F821
    q_hi = math.log(mort_rate_at_age(table, hi))                     # noqa: F821
    return round(math.exp(q_lo + (x - lo) / (hi - lo) * (q_hi - q_lo)), 5)  # noqa: F821


def check_mort_graduation_resid(t):
    """The shipped-rate residual at the attained age of policy year t; zero everywhere.

    ``mort_table.csv`` rate less the graduation :func:`mort_rate_graduated` rebuilds from
    the anchors in ``mort_anchor_table.csv``.  Non-zero is not a defect once a licensed or
    company table has been dropped in — it is the correct answer, and the reason this check
    reports a residual rather than raising.
    """
    tbl = mort_table_name(t)
    x = age(t)
    if x >= omega_age(tbl):
        return 0.0
    return mort_rate_at_age(tbl, x) - mort_rate_graduated(tbl, x)


def check_mort_graduation():
    """True when the shipped rates are still the [std] graduation of the quoted anchors.

    The library ships no copy of 標準生命表2018 or of the 2007 年金開始後用 table: what it ships
    is a construction anchored to quoted rates, and this is the assertion that
    ``mort_table.csv`` and ``mort_anchor_table.csv`` still agree with each other — the
    死亡保険用 rates log-linear between their anchors, the 年金開始後用 rates on the Makeham law.
    """
    return all(abs(check_mort_graduation_resid(t)) <= 1e-15
               for t in range(0, proj_len()))


# --- Results ---------------------------------------------------------------

def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the start-of-year count, which is the weight applied to every cash flow
    on the same row.  ``net_cf`` carries the notes' own income-positive sign, so the
    deferral rows are positive and the payout rows are large negatives.
    ``claims_commutation`` and ``policy_loans`` are columns of zeros in the base run and are
    published rather than dropped, because a zero states the module is off where a missing
    column would only hide it.

    ``claims_annuity`` is a **living** benefit on this product — the instalments are paid on
    the annuitant surviving to a payment date, never on death.  The library uses the same
    column name for the *form* of the benefit, a stream rather than a lump sum, so it names
    a **death** benefit in ``IncomeTerm_JP_S`` and a living benefit in ``LTC_JP_S``; the
    contingency is a product fact and is stated rather than inferred.  The death
    contingency has its own column here, ``claims_death``, carrying the 死亡給付金.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_commutation": [claims(t, "COMMUTATION") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "policy_loans": [policy_loans(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force, decrements and per-policy amounts, indexed by t.

    The companion to :func:`result_cf`: the two in-force measures side by side, the
    decrements that move them, and the fund, death benefit and surrender value that price
    them.  Reading ``av_pp``, ``db_pp`` and ``cv_pp`` in one table is the quickest way to
    see the crossover, where the fund passes the death benefit and the surrender value
    stops rising.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "lives_if": [lives_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_commute": [pols_commute(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "db_pp": [db_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def lapse_rate_mean(weighting="count"):
    """The mean 解約・失効 rate over the deferral phase, on a stated weighting.

    ``"count"``
        weighted by :func:`pols_if`, ``sum l(t) w(t) / sum l(t)`` over
        ``t = 0 .. n - 1``.

    ``"fund"``
        weighted by :func:`av_pp` over the same range.

    Published as a cells because the two are not interchangeable and a calibration must say
    which one it used.  Lapse is front-loaded and the fund is back-loaded, so the fund
    weighting comes out materially lower — and the one public figure this curve is anchored
    to, a market-wide 3.4% for FY2024, is itself measured on 契約高 rather than on policy
    count [R15] [REG-R31].  Calibrating a count model directly against the published number
    without saying which weighting is meant mis-states the deferral decrement.
    """
    ts = range(0, annuitisation_t())
    if weighting == "count":
        w = [pols_if(t) for t in ts]
    elif weighting == "fund":
        w = [av_pp(t) for t in ts]
    else:
        raise ValueError("invalid weighting")
    num = sum(wt * lapse_rate(t) for wt, t in zip(w, ts))
    den = sum(w)
    return num / den if den else 0.0


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

roll_fwd_tol = 1e-10

math = ("Module", "math")

pd = ("Module", "pandas")
