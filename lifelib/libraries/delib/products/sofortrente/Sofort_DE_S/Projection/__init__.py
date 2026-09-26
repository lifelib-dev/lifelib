# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Sofort_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **months from Vertragsbeginn**, 0-based: ``t = t_start()`` is the first
projected month — 0 for a new-business point, ``duration_mth_init()`` for one already in
force — and ``t = proj_len() - 1`` the last. ``proj_len()`` is the **exclusive end** of
the frame, counted from inception, so ``result_cf()`` is indexed
``range(t_start(), proj_len())`` and carries ``proj_len() - t_start()`` rows.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/sofortrente/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values — so a diff of the model shows logic changes only, and an input can be edited or
swapped without rewriting the model. This follows ``annuallife.TradLife_A``; contrast
``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``Sofort_DE_S`` folder without its parent's CSVs produces a model that reads and then
fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Sofort_DE_S.Data`, reached here through the ``data`` Reference:

============================  ===================================  ================================
Reference                     Cells                                File
============================  ===================================  ================================
model_point_file              data.model_point_table()             model_point_table.csv
mort_table_file               data.mort_table()                    mort_table.csv
improvement_file              data.improvement_table()             improvement_table.csv
surplus_scale_file            data.surplus_scale_table()           surplus_scale_table.csv
hoechstrechnungszins_file     data.hoechstrechnungszins_table()    hoechstrechnungszins_table.csv
============================  ===================================  ================================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for exposure, plural nouns for cash
flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an
uppercase ``kind`` string, ``check_*()`` returning one bool over all ``t`` with the
per-period residual at ``check_*_resid(t)``. The technical notes use compact actuarial
symbols instead. The mapping is:

===============  ====================================  ========================================
Notes symbol     Cells                                 Meaning
===============  ====================================  ========================================
(none)           model_point()                         The selected model point row
t0               t_start()                             First projected month index
n                proj_len()                            Exclusive end of the frame, t < n
(none)           horizon_mths(life)                    12 (omega_age - entry age)
(none)           duration_mth(t)                       Months elapsed since inception
(none)           duration(t)                           Completed policy years, t // 12
(none)           policy_year(t)                        Contractual policy year, t // 12 + 1
x_a(t), x_s(t)   age(t, life)                          Attained age of each life
(none)           calendar_year(t)                      Calendar year of month t
SP               single_prem()                         The Einmalbeitrag
SP_net           net_single_prem()                     SP (1 - alpha)
alpha            expense_load_alpha                    Acquisition loading in the tariff
beta             expense_load_beta                     Loading on the annuity value
i                tariff_int_rate()                     Tariff Rechnungszins
(cap)            max_tariff_int_rate()                 Hoechstrechnungszins at entry_year
m                payment_freq()                        Instalments per year
p = 12/m         pay_period_mths()                     Months between instalments
D                defer_mths()                          Aufschubzeit in months
(none)           first_pay_mth()                       Month of the first instalment
G                guar_years()                          Rentengarantiezeit in years
(none)           guar_end_mth()                        First month after the guarantee
gamma(t)         certain_floor(t)                      1 inside the guarantee, else 0
(none)           is_payment_mth(t)                     Whether an instalment falls at t
delta            surv_pct()                            Hinterbliebenenrente percentage
(table)          mort_rate_at_age(x, s, b)             Table rate; s = M, F or U
lambda(x)        improve_rate_at_age(x, b)             Improvement rate at age x
q(x, s, g, b)    mort_rate_gen(x, s, g, b)             The generational surface
q2(t)            mort_rate(t, life)                    Annual second-order rate
(none)           mort_rate_mth(t, life)                Its monthly equivalent
q1(t)            mort_rate_tariff(t, life)             Annual first-order unisex rate
(none)           mort_rate_tariff_mth(t, life)         Its monthly equivalent
l_a(t), l_s(t)   lives_if(t, life)                     Second-order survival to start of t
d_a(t), d_s(t)   lives_death(t, life)                  Deaths during month t
l~(k)            tariff_lives(k, life)                 First-order survival, pricing only
a-double-dot     annuity_factor()                      Value at t=0 of one unit of instalment
(refund leg)     refund_pv()                           PV of the Kapitalrueckgewaehr
R                annuity_pp_derived()                  Instalment struck by equivalence
R                annuity_guar_pp(t)                    The garantierte Rente in force
u0, psi          surplus_init_pct(), surplus_growth()  Opening surplus share, growth
U(t)             annuity_surp_pp(t)                    The Ueberschussrente instalment
A(t)             annuity_pp(t)                         Total instalment, R + U(t)
C(t)             cum_annuity_guar_pp(t)                Guaranteed instalments paid to t
K(t)             refund_pp(t)                          max(SP - C(t), 0)
F(t)             payment_factor(t)                     Expected instalments payable at t
(none)           pols_if(t)                            Probability an obligation remains
(none)           premiums(t)                           The Einmalbeitrag, at t = 0 only
(none)           annuity_payments(t, kind)             ANNUITANT / SURVIVOR instalments
(none)           claims(t, kind)                       GUARANTEE / REFUND death outgo
(none)           infl_factor(t)                        Expense inflation factor
c_e, c_p, pi     expenses(t)                           Maintenance, per-instalment, acquisition
liability_cf(t)  liability_cf(t)                       The stream, outgo positive
net_cf(t)        net_cf(t)                             The same stream, income positive
===============  ====================================  ========================================

Five names needed care.

``pols_if(t)`` is **not a policy count** on this product. It is the probability that a
payment obligation of any kind still stands at the start of month ``t`` — the guarantee
period running, the annuitant alive, or the survivor's annuity in payment — and it is the
weight the maintenance expense is carried on. It keeps the library's name for that weight
because that is what the name means everywhere else, and its docstring says what it is so
that the shared conventions suite applies the payout-product exemption by reading the
docstring rather than by consulting a list.

``payment_factor(t)`` is the number of instalments expected to be payable at the payment
instant ``t``, per unit of ``pols_if_init()``, and it is a ``max`` and not a sum:
``max(gamma(t), l_a(t)) + delta (1 - l_a(t)) l_s(t) (1 - gamma(t))``. Inside the
*Rentengarantiezeit* the instalment goes out whether the annuitant is alive or not, so
``gamma + l_a`` would pay ``1 + l_a`` for the whole guarantee — nearly double the outgo
for ten years on the anchor cell. The survivor's leg is gated by ``(1 - gamma(t))`` for
the same reason: inside the guarantee the full instalment already goes out, and adding the
survivor's percentage on top would pay ``1 + delta``.

``annuity_guar_pp(t)``, ``annuity_surp_pp(t)`` and ``annuity_pp(t)`` are the *garantierte
Rente*, the *Überschussrente* and their sum. Only the first is a promise. The second is
declared annually out of surplus actually earned, steps at the **policy anniversary** and
never monthly, and ratchets under the *Bonusrente* crediting mechanic — an increment,
once bought as paid-up annuity, does not come back off. A projection of it is a central
estimate of a stream the insurer may reduce, never a guaranteed cash flow.

``mort_rate(t, life)`` and ``mort_rate_tariff(t, life)`` are **different objects, not two
readings of one table**. The first is second order and sex-specific and drives the
projection; the second is first order and unisex and is used only inside the pricing
sums. ``mort_rate_tariff`` is below ``mort_rate`` at every ``t``, and the ratio of the two
*falls* with ``t`` because the first-order margin reaches the improvement trend as well as
the level. Letting the model point's ``sex`` into the tariff would reproduce a tariff
unlawful in Germany since 21 December 2012.

``annuity_factor()`` is the notes' ``ä`` and is **not** the market's ``a12``:
``a12 = annuity_factor() / payment_freq()``, so a research figure of ``a12 = 20.426``
corresponds to ``annuity_factor() = 245.11``. It is a pricing quantity and stays acyclic:
it depends on the tariff basis, the elected options and the tariff interest rate, and on
nothing that depends on the projected path. In particular it does **not** depend on
``surplus_form``, because the *Überschussrente* is financed out of surplus actually
earned rather than priced into the guarantee.

.. rubric:: The Kapitalrückgewähr is solved, not evaluated

Where ``refund_form() == "full"`` the death benefit is the *Einmalbeitrag* less the
**guaranteed** instalments already paid, floored at zero. Because a larger refund means a
smaller annuity, and a smaller annuity means the refund runs off more slowly, the pricing
equation is **implicit in R**::

    g(R) = R x annuity_factor() x (1 + beta)
         + sum over t of v^(t/12) d~_a(t) max(SP - n(t) R, 0)   =   net_single_prem()

with ``n(t)`` the instalments paid by month ``t``. ``g`` is increasing in ``R`` on
``(0, R_max]``, where ``R_max`` is the no-refund annuity, and ``g(0) < net_single_prem()``
on any basis with a positive interest rate, so a root exists and bisection converges.
:func:`annuity_pp_derived` bisects to ``solve_tol`` in at most ``solve_max_iter`` steps,
evaluating the sum inline from the cached :func:`tariff_lives` path rather than through a
cells parameterized by the trial ``R``.

**Computing R_max and then subtracting a refund cost is a different — and wrong —
answer.** :func:`refund_pv` is published so the identity can be seen, and
:func:`check_equivalence` asserts it.

During an *Aufschubzeit* no instalment has been paid, so the refund is the whole
*Einmalbeitrag*: the same machinery gives the *Beitragsrückgewähr* on death before
*Rentenbeginn* without a second mechanic, and ``refund_form() == "none"`` on a deferred
point gives the pure deferred annuity in which the fund of those who die is forfeited to
the survivors.

.. rubric:: There is no behaviour to model, and that is the product

Once the *Rentenbezug* has begun the policyholder has no right of termination, no
*Rückkaufswert*, no *Beitragsfreistellung*, no capital option and no transfer. So this
Space carries **no lapse rate, no surrender cells, no paid-up state, no account value and
no option take-up rate** — there is no ``lapse_rate``, ``lapse_rate_mth``, ``av_pp_at`` or
``cv_pp`` anywhere in it. The only decrement is death, and where a *Hinterbliebenenrente*
is in force there are two lives and the liability runs to the second death. That absence
is a statutory fact about the product, asserted by the model's own tests rather than left
to inspection, and it is the reason this model's result depends more purely on the
mortality basis and the surplus assumption than any other in the library.

.. rubric:: What is deliberately absent

The *Bewertungsreserven* share, which continues in the payout phase but is path- and
balance-sheet-dependent on the HGB accounts; a commuted settlement of the
*Restgarantiezeit*, whose basis was not established; a reduction of a declared
*Überschussrente*, which the sensitivity section of the notes prices instead of the base
run reserving for; taxation, which falls on the annuitant rather than on the insurer's
liability; and any management action on the declared surplus. Each is named so that the
projection's silence about it reads as a decision rather than an oversight.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — the *Einmalbeitrag* in, instalments, death
benefits and expenses out — which is the library-wide sign. :func:`liability_cf`
publishes the same stream outgo-positive, the notes' own orientation, with
``net_cf(t) = -liability_cf(t)`` exactly, so a Solvency II best estimate is
``sum v(t) liability_cf(t)`` over whatever discount curve the valuation layer supplies.
Both are columns of :func:`result_cf`, so the identity is verifiable in the frame rather
than only in prose.

The shape to expect is a large positive first month — the whole *Einmalbeitrag* arrives
against one instalment and the acquisition expense — and a long negative tail that decays
with survival. The tail is what a *Deckungsrückstellung* is held against, and this model
does not compute one.
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


def policy_id():
    """The policy identifier of the selected model point."""
    return str(model_point()["policy_id"])


def single_prem():
    """SP: the *Einmalbeitrag*, in euros — the contract's whole consideration.

    Paid once, at the start of month 0.  There is no premium stream, no *Beitragsdynamik*
    and no premium-payment decrement anywhere in this model, so a projection of this
    product has exactly one inflow.  The shipped points run from 25 000 € to 500 000 €
    around a representative 100 000 €, which is the unit the German market quotes an
    immediate annuity in — *Rente je 100 000 € Einmalbeitrag*.
    """
    return float(model_point()["single_prem"])


def entry_age(life=1):
    """Age last birthday at *Vertragsbeginn*: the annuitant's, or the second life's.

    ``life = 1`` is the annuitant and ``life = 2`` the *mitversicherte Person* of a
    *Hinterbliebenenrente*.  Where ``surv_pct() == 0`` the second life's columns are
    carried as zeros and are never read, because every cells that would read them returns
    early.
    """
    if life == 1:
        return int(model_point()["entry_age"])
    if life == 2:
        return int(model_point()["surv_age"])
    raise ValueError("invalid life")


def birth_year(life=1):
    """The *Geburtsjahr* of each life — the key into the generational mortality surface.

    Carried as its own model point attribute and **never derived from the projection
    year**.  DAV 2004 R is a *Generationentafel*: mortality is given per birth cohort and
    the expected future improvement is inside the table rather than applied on top of it,
    so a 65-year-old born in 1960 and a 65-year-old born in 1970 are priced on different
    mortality.  Reading the surface by projection year instead walks diagonally across
    cohorts, which is this product's classic mortality error.
    """
    if life == 1:
        return int(model_point()["birth_year"])
    if life == 2:
        return int(model_point()["surv_birth_year"])
    raise ValueError("invalid life")


def sex(life=1):
    """The sex of each life, M or F.  **Decrement only — it must not enter the tariff.**

    German new business has had to be unisex since 21 December 2012, so the annuity factor
    is struck on a blend of the sex-distinct tables at ``mix_male`` and never on the model
    point's own sex; see :func:`mort_rate_tariff`.  The tension worth knowing is that the
    underlying tables remain sex-distinct, so a realised portfolio mix away from the
    assumed one shows up as a *Risikoergebnis* — which is precisely why a unisex annuity is
    a better deal for women than for men and why the female share of a voluntary annuitant
    portfolio sits above the population share.
    """
    if life == 1:
        v = str(model_point()["sex"])
    elif life == 2:
        v = str(model_point()["surv_sex"])
    else:
        raise ValueError("invalid life")
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def entry_year():
    """The calendar year of *Vertragsbeginn*.

    It is not a cash flow driver — every step in this product falls on a policy
    anniversary, not on 31 December — but it does two things.  It is the calendar anchor of
    the cohort exponent through :func:`calendar_year`, and it selects the contract's own
    *Höchstrechnungszins* vintage, which stays with the contract for life; see
    :func:`max_tariff_int_rate`.
    """
    return int(model_point()["entry_year"])


def defer_mths():
    """D: the *Aufschubzeit* in months, 0 for a pure *Sofortrente*.

    The market sells a hybrid in which the *Einmalbeitrag* is paid now and the annuity
    begins after a short deferment.  Three things happen inside it and must not be
    conflated: interest accrues, mortality accrues so the survivors share the fund of those
    who died, and the annuity starts at an older age.  All three fall out of the pricing
    sum without a second mechanic.  No carrier's terms for the variant were established,
    so the base run leaves it off and model point 6 switches it on.
    """
    return 12 * int(model_point()["defer_years"])


def guar_years():
    """G: the *Rentengarantiezeit* in years, 0 for none.

    A guaranteed payment period running from *Rentenbeginn*: if the annuitant dies inside
    it, the instalments continue to the beneficiaries until it expires.  Durations of 5,
    10, 15, 20, 25 and 30+ years are offered, typically 15 years to retirement age 70 and
    10 years above it, and most policyholders choose 10 to 20.  It is carried in the tariff
    name at one carrier and has a settable contractual minimum at another, so a
    *Sofortrente* with **no** guarantee period is a configuration rather than the default.
    """
    return int(model_point()["guar_years"])


def refund_form():
    """The *Kapital-* / *Beitragsrückgewähr* election: ``none`` or ``full``.

    ``full`` refunds the *Einmalbeitrag* less the **guaranteed** instalments already paid,
    floored at zero.  Measuring the refund against the guaranteed rather than the total
    annuity is a **[std]** reading, argued from the principle that a guaranteed benefit
    cannot be defined by reference to a discretionary quantity; which reading a German
    carrier uses was not established, and the two diverge materially over twenty years.
    """
    v = str(model_point()["refund_form"])
    if v not in ("none", "full"):
        raise ValueError("invalid refund_form")
    return v


def surv_pct():
    """delta: the *Hinterbliebenenrente* as a fraction of the annuitant's instalment.

    0 switches the rider off, and the second life's attributes are then never read.  60 %
    and 100 % are the market's two standard levels; no carrier's menu was established.
    The German market treats the survivor's annuity as a *Zusatzversicherung* — a rider
    with its own condition set — which is why it is a gated leg here rather than a term in
    the main annuity's benefit formula.
    """
    return float(model_point()["surv_pct"])


def payment_freq():
    """m: instalments per year, one of 12, 4, 2 or 1.

    Monthly is the market standard and the product's whole commercial proposition — an
    income replacing a salary.  The other frequencies exist as options; no carrier's menu,
    and no loading or discount for choosing one, was established, so this model prices
    them on the same basis and lets the timing of the instalments do the work.
    """
    v = int(model_point()["payment_freq"])
    if v not in (1, 2, 4, 12):
        raise ValueError("invalid payment_freq")
    return v


def payment_timing():
    """*vorschüssig* (``advance``) or *nachschüssig* (``arrears``) — a **[std]** convention.

    Every arithmetic in the research file uses an annuity-due, and advance payment is the
    German market convention for annuities in payment, but **no source in the corpus states
    it in terms**.  It is worth about 5 % of the annuity, which is larger than most
    assumption changes anyone would argue about, so model point 9 is the anchor cell in
    arrears and exists to make the difference measurable rather than assumed.
    """
    v = str(model_point()["payment_timing"])
    if v not in ("advance", "arrears"):
        raise ValueError("invalid payment_timing")
    return v


def tariff_int_rate():
    """i: the tariff *Rechnungszins* the guaranteed annuity is struck at.

    At or **below** the statutory *Höchstrechnungszins* of the contract's vintage, never
    automatically at it: one carrier's AVB in the corpus states its annuity factor is
    calculated at "an underlying interest rate (currently 0 percent p.a.)" while the
    statutory maximum was positive.  See :func:`check_tariff_int_rate`, which is therefore
    an inequality.

    This rate reaches the projection **only** through :func:`annuity_factor` and
    :func:`refund_pv`.  The published cash flows are undiscounted; a best estimate
    discounts them on the EIOPA curve, not on the tariff rate.
    """
    return float(model_point()["tariff_int_rate"])


def surplus_form():
    """The *Überschussverwendung*: ``none``, ``konstant``, ``teildynamisch`` or ``volldynamisch``.

    Elected once, at inception.  The constant form fixes the total annuity from a
    projection of surplus over the whole remaining lifetime and holds it level **in
    intention only** — if the insurer earns less than projected the annuity is reduced,
    which is the single most important thing to understand about this product.  The
    volldynamic form starts lowest and rises with each declaration; the teildynamic form is
    intermediate on both axes.  All four distribute the same expected surplus and differ
    only in *when*.
    """
    v = str(model_point()["surplus_form"])
    if v not in ("none", "konstant", "teildynamisch", "volldynamisch"):
        raise ValueError("invalid surplus_form")
    return v


def annuity_pp_init():
    """The guaranteed instalment carried on an in-force point; 0 means derive it.

    This is the model's one structural fork, and it is **not** two premium forms — a
    *Sofortrente* has exactly one.  A new-business point carries 0 and the model strikes
    the *garantierte Rente* from :func:`single_prem` by equivalence on the tariff basis; an
    in-force point carries an annuity struck years ago on a basis this model does not
    reproduce, and the model uses it as given.  On the second kind
    :func:`check_equivalence` returns True without asserting anything, because there is no
    equivalence here to assert.
    """
    return float(model_point()["annuity_pp_init"])


def duration_mth_init():
    """Months already elapsed at the valuation date; the frame's first ``t``.

    0 for a new-business point.  An in-force point opens at the duration it has already
    run, so its frame contains no ``t = 0`` and therefore neither the *Einmalbeitrag* nor
    the acquisition expense — both of which happened before the valuation date and belong
    to a period this projection does not cover.
    """
    return int(model_point()["duration_mth_init"])


def pols_if_init():
    """The number of policies the model point represents; 1.0 on every shipped point.

    Every cash flow is proportional to it, and it is the scale
    :func:`result_cf`'s first ``pols_if`` opens at.
    """
    return float(model_point()["pols_if_init"])


def t_start():
    """t0: the first projected month index, ``duration_mth_init()``.

    Where the frame *starts* is a product fact rather than a house convention: a
    new-business point opens at 0 and an in-force point at the duration it has already run.
    What the library asserts instead is contiguity and the frame's *end*.
    """
    return duration_mth_init()


def horizon_mths(life=1):
    """``12 (omega_age - entry_age(life))``: the month at which that life's survival ends.

    With ``q = 1`` at attained age 120 in every series and ``omega_age = 121``, the
    survival path reaches zero inside this horizon and stays there, so the tail months
    carry no cash flow.
    """
    return 12 * (omega_age - entry_age(life))                        # noqa: F821


def proj_len():
    """n: the **exclusive end** of the frame, counted in months from *Vertragsbeginn*.

    The frame is ``range(t_start(), proj_len())``, so the last projected month index is
    ``proj_len() - 1`` and ``result_cf()`` carries ``proj_len() - t_start()`` rows — the
    library's ``range(proj_len())`` idiom, read from inception rather than from the
    frame's own start because an in-force point opens partway through.

    The maximum of three terms, and all three are needed::

        max( horizon_mths(1),                      the annuitant's survival horizon
             guar_end_mth(),                       the Rentengarantiezeit's own end
             horizon_mths(2)  if surv_pct() > 0 )  the second life's horizon

    Stopping on the annuitant's horizon alone truncates a younger survivor's tail — on
    model point 4 the second life is three years younger and outlives the frame by three
    years — and stopping on the guarantee alone truncates the life annuity.  On the anchor
    cell ``horizon_mths(1) = 12 x (121 - 65) = 672``, the guarantee ends at month 120, and
    ``proj_len() = 672``: 672 monthly rows, ``t = 0 ... 671``.
    """
    n = max(horizon_mths(1), guar_end_mth())
    if surv_pct() > 0.0:
        n = max(n, horizon_mths(2))
    return n


def duration_mth(t):
    """Complete months elapsed since *Vertragsbeginn* at the start of month ``t``.

    The frame's index is itself the duration, because ``t`` is counted from
    *Vertragsbeginn* on a 0-based grid — so this cells is ``t``.  It is published because
    the notes name the quantity, because an in-force point's frame opens at
    ``duration_mth_init()`` rather than at 0 and the identity is then worth being able to
    read off, and because a reader coming from a model whose index is a policy year should
    find the unit stated rather than inferred.
    """
    return t


def duration(t):
    """Completed policy years at the start of month ``t``: ``t // 12``; 0 for t = 0..11.

    The step that matters in this product.  The *Überschussrente* increase, the expense
    inflation index and the attained-age step all fall on the **policy anniversary**;
    nothing happens on 31 December, so no cells needs the civil month.  This is the
    0-based elapsed count; the 1-based contractual label is :func:`policy_year`.
    """
    return t // 12


def policy_year(t):
    """y(t) = ``t // 12 + 1``: the contractual, 1-based policy year containing month ``t``.

    1 for ``t = 0 ... 11``, 2 for ``t = 12 ... 23``, and so on.  It is **derived from**
    ``t`` and never indexed **by**: no cells in this model takes a policy year as its
    argument.  Every formula that needs the elapsed count — the *Überschussrente*
    exponent, the inflation index, the attained age — uses :func:`duration` instead.
    """
    return duration(t) + 1


def age(t, life=1):
    """Attained age of a life at month ``t``: ``entry_age(life) + t // 12``.

    Age last birthday at inception, incrementing at each 12-month multiple of it.  A real
    implementation on dates carries a fractional offset of up to a year; the shipped model
    points satisfy ``entry_year == birth_year + entry_age``, which is a **[std]**
    internal-consistency convention rather than a contract fact.
    """
    return entry_age(life) + t // 12


def calendar_year(t):
    """The calendar year month ``t`` falls in: ``entry_year() + t // 12``.

    Reporting, and the cross-check on the cohort exponent — the year a life attains
    ``age(t, life)`` is ``birth_year(life) + age(t, life)``, which equals this only when
    the model point's own consistency convention holds.
    """
    return entry_year() + t // 12


def mort_rate_at_age(x, table_sex, basis):
    """The table's annual death rate at attained age ``x``.

    ``table_sex`` is ``M``, ``F`` or ``U``; ``basis`` is ``FIRST`` or ``SECOND``.  ``U`` is
    **computed** as ``mix_male q_M + (1 - mix_male) q_F`` and is never a row of the CSV,
    because no real sex-distinct table carries one — the unisex tariff is a blend an
    insurer strikes on an assumed portfolio mix, not a published table.

    Ages outside the table are clamped to its ends.  The upper clamp is the one that
    matters: on a joint-life point the frame runs to the *second* life's horizon, so the
    annuitant's attained age passes the closing row while their survival is already zero.
    """
    if table_sex == "U":
        return (mix_male * mort_rate_at_age(x, "M", basis)           # noqa: F821
                + (1.0 - mix_male) * mort_rate_at_age(x, "F", basis))   # noqa: F821
    tab = data.mort_table()                                          # noqa: F821
    ages = tab.index.get_level_values("age")
    xx = min(max(int(x), int(ages.min())), int(ages.max()))
    return float(tab.loc[(basis, table_sex, xx), "mort_rate"])


def improve_rate_at_age(x, basis):
    """lambda(x): the annual mortality improvement rate at attained age ``x``.

    The *Trendfunktion* of the generational surface, in a **[std]** proxy: 1,5 % a year to
    age 70 on the second-order basis, tapering linearly to zero at 105, with the
    first-order basis improving 25 % faster.  Prudence in an annuity table must reach the
    **rate** of improvement as well as its level, because the improvement compounds over a
    forty-year stream, and a proxy reproducing only the level is not a proxy for the table.
    """
    tab = data.improvement_table()                                   # noqa: F821
    ages = tab.index.get_level_values("age")
    xx = min(max(int(x), int(ages.min())), int(ages.max()))
    return float(tab.loc[(basis, xx), "improve_rate"])


def mort_rate_gen(x, table_sex, cohort, basis):
    """The generational surface: ``q_table(x) (1 - lambda(x))^(cohort + x - mort_base_year)``.

    The improvement lives **inside** the surface, keyed by birth cohort, rather than being
    applied on top of a period rate keyed to the projection year.  ``cohort + x`` is the
    calendar year in which the life attains age ``x``, so the exponent is simply that year
    less ``mort_base_year`` and the shipped tables are the period tables of 2025.

    The exponent may be **negative** — an in-force point issued in 2012 attains its ages
    before 2025 and reads correspondingly heavier mortality — and it is not floored.

    The result is capped at 1.  A negative exponent scales the rate **up**, and at the top
    of the proxy's age range the second-order series is already close to 1, so the cap is
    what keeps ``q`` a probability; it binds only in the last two or three years of the
    table, where survival is zero to eleven decimal places and no cash flow depends on it.
    """
    return min(1.0,
               mort_rate_at_age(x, table_sex, basis)
               * (1.0 - improve_rate_at_age(x, basis))
               ** (cohort + x - mort_base_year))                     # noqa: F821


def mort_rate(t, life=1):
    """The **annual** second-order death rate for a life in month ``t``.

    Read from the generational surface at that life's own attained age, birth cohort and
    sex.  This is the best-estimate basis and drives the projected decrement; it is
    **heavier** than :func:`mort_rate_tariff` at every ``t``, and the wedge between the two
    is the systematic *Risikoüberschuss* the *Überschussrente* is largely financed from.

    Returns 0 for the second life where no *Hinterbliebenenrente* is in force: the life
    does not exist, its model point columns are zeros, and nothing may read them.
    """
    if life == 2 and surv_pct() == 0.0:
        return 0.0
    return mort_rate_gen(age(t, life), sex(life), birth_year(life), "SECOND")


def mort_rate_mth(t, life=1):
    """The monthly equivalent of :func:`mort_rate`: ``1 - (1 - q)^(1/12)`` **[std]**.

    A uniform force of mortality across the policy year, which is the convention that makes
    twelve monthly survivals compound back to the annual one exactly.  At the closing age,
    where ``q = 1``, it is 1 and the survival path steps to zero in that month.
    """
    return 1.0 - (1.0 - mort_rate(t, life)) ** (1.0 / 12.0)


def mort_rate_tariff(t, life=1):
    """The **annual** first-order rate on the **unisex** blend, used only for pricing.

    Two things separate it from :func:`mort_rate` and both are deliberate.  It is
    **first order** — lighter, because prudence for an annuity means assuming annuitants
    live longer, which raises the annuity value and lowers the annuity a given
    *Einmalbeitrag* buys.  And it is **unisex**, read at ``table_sex = "U"`` rather than at
    the model point's own sex, because a German tariff written since 21 December 2012 may
    not differentiate.  Letting ``sex()`` in here reproduces an unlawful tariff and is a
    listed pitfall.
    """
    if life == 2 and surv_pct() == 0.0:
        return 0.0
    return mort_rate_gen(age(t, life), "U", birth_year(life), "FIRST")


def mort_rate_tariff_mth(t, life=1):
    """The monthly equivalent of :func:`mort_rate_tariff`: ``1 - (1 - q)^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - mort_rate_tariff(t, life)) ** (1.0 / 12.0)


def lives_if(t, life=1):
    """l(t): the second-order probability a life is alive at the **start** of month ``t``.

    1 at ``t_start()`` — for an in-force point the projection is conditional on the
    annuitant being alive at the valuation date — and rolled forward monthly by
    ``l(t) = l(t - 1) (1 - mort_rate_mth(t - 1))``.  0 throughout for the second life where
    no *Hinterbliebenenrente* is in force, which is also what makes the *Anwartschaft*
    lapsing on the second life's prior death need no separate rule: ``l_s(t)`` is already
    zero then.
    """
    if life == 2 and surv_pct() == 0.0:
        return 0.0
    if t <= t_start():
        return 1.0
    return lives_if(t - 1, life) * (1.0 - mort_rate_mth(t - 1, life))


def lives_death(t, life=1):
    """d(t): deaths **during** month ``t``, ``lives_if(t) - lives_if(t + 1)``.

    A life dying in month ``t`` has already received the instalment due at the start of
    that month, so the *Kapitalrückgewähr* settled against this decrement is net of it.
    """
    return lives_if(t, life) - lives_if(t + 1, life)


def tariff_lives(k, life=1):
    """l~(k): first-order survival to the start of month ``k``, used only in the pricing sums.

    Rolled forward from 1 at ``k = 0`` on :func:`mort_rate_tariff_mth`.  It runs from
    inception whatever ``t_start()`` is, because the annuity factor is a quantity struck at
    inception; an in-force point does not use it, its annuity having been struck on a basis
    this model does not reproduce.
    """
    if life == 2 and surv_pct() == 0.0:
        return 0.0
    if k <= 0:
        return 1.0
    return tariff_lives(k - 1, life) * (1.0 - mort_rate_tariff_mth(k - 1, life))


def net_single_prem():
    """SP_net: the *Nettoeinmalbeitrag*, ``single_prem() (1 - expense_load_alpha)``.

    The insurer deducts the acquisition and distribution loading from the *Einmalbeitrag*
    and annuitises the remainder.  An accumulation product's *Deckungskapital* recursion
    degenerates, for a single premium, to exactly this one netting step.  ``alpha`` is
    **[std]**: no charge parameter was established at any carrier.
    """
    return single_prem() * (1.0 - expense_load_alpha)                # noqa: F821


def pay_period_mths():
    """p: months between instalments, ``12 // payment_freq()``."""
    return 12 // payment_freq()


def first_pay_mth():
    """The month the first instalment falls due.

    ``defer_mths()`` under *vorschüssig*, ``defer_mths() + pay_period_mths()`` under
    *nachschüssig*.  The survival index of a payment is ``t`` under **both**: with month
    starts as the payment instants, an advance instalment for month ``t`` and an arrears
    instalment covering ``[t - p, t)`` are both paid at the start of month ``t`` and both
    require the payee to be alive then.  The two conventions therefore differ only in
    *which months carry an instalment*.
    """
    if payment_timing() == "advance":
        return defer_mths()
    return defer_mths() + pay_period_mths()


def is_payment_mth(t):
    """Whether an instalment falls due at the start of month ``t``.

    ``t >= first_pay_mth()`` and ``(t - first_pay_mth()) % pay_period_mths() == 0``.
    """
    if t < first_pay_mth():
        return False
    return (t - first_pay_mth()) % pay_period_mths() == 0


def guar_end_mth():
    """The first month **after** the *Rentengarantiezeit*: ``first_pay_mth() + 12 G``.

    Note that it is 12 G and not ``G x payment_freq() x pay_period_mths()`` spelled out —
    they are the same number, which is the point: a G-year guarantee covers ``G x m``
    instalments at every frequency and under both timings.
    """
    return first_pay_mth() + 12 * guar_years()


def certain_floor(t):
    """gamma(t): 1 while the *Rentengarantiezeit* runs, 0 otherwise.

    Inside it the instalment is payable **whether the annuitant is alive or not**, which is
    why it enters :func:`payment_factor` through a ``max`` and not a sum.
    """
    if first_pay_mth() <= t < guar_end_mth():
        return 1.0
    return 0.0


def annuity_factor():
    """ä: the value at inception of one unit of instalment, on the tariff basis.

    ``sum over payment months k of v^(k/12) F~(k)``, where ``F~`` is
    :func:`payment_factor` computed on the **first-order** survival path
    :func:`tariff_lives` rather than on the projected one, and ``v = 1 / (1 + i)``.

    It is dimensionless and it is **not** the market's ``a12``:
    ``a12 = annuity_factor() / payment_freq()``.  It is a pricing quantity and stays
    acyclic — it depends on the tariff basis, the elected options and the tariff interest
    rate, and on nothing that depends on the projected path.  In particular it does not
    depend on ``surplus_form``, so :func:`annuity_pp_derived` is invariant to it.
    """
    v = 1.0 / (1.0 + tariff_int_rate())
    d = surv_pct()
    total = 0.0
    for k in range(0, proj_len()):
        if not is_payment_mth(k):
            continue
        g = certain_floor(k)
        la = tariff_lives(k, 1)
        f = max(g, la) + d * (1.0 - la) * tariff_lives(k, 2) * (1.0 - g)
        total += v ** (k / 12.0) * f
    return total


def annuity_pp_derived():
    """R: the *garantierte Rente* per instalment, struck at inception by equivalence.

    Where no refund is elected the equivalence is explicit::

        R = net_single_prem() / ( annuity_factor() x (1 + expense_load_beta) )

    Where ``refund_form() == "full"`` it is **implicit**, because the death benefit is the
    *Einmalbeitrag* less the instalments already paid and a smaller annuity runs that
    refund off more slowly.  The equation

        g(R) = R ä (1 + beta) + sum_t v^(t/12) d~_a(t) max(SP - n(t) R, 0) = SP_net

    is increasing in ``R`` on ``(0, R_max]`` with ``g(0) < SP_net``, so bisection on that
    interval converges; the sum is evaluated inline from the cached
    :func:`tariff_lives` path rather than through a cells parameterized by the trial ``R``,
    which is what keeps the solve out of the dependency graph.

    **Computing R_max and then subtracting a refund cost computed at that annuity is a
    different — and wrong — answer**, and the difference is not a rounding.
    """
    a = annuity_factor()
    load = 1.0 + expense_load_beta                                   # noqa: F821
    r_max = net_single_prem() / (a * load)
    if refund_form() == "none":
        return r_max
    v = 1.0 / (1.0 + tariff_int_rate())
    p = pay_period_mths()
    fp = first_pay_mth()
    sp = single_prem()
    target = net_single_prem()
    disc = []
    dens = []
    paid = []
    for t in range(0, proj_len()):
        d = tariff_lives(t, 1) - tariff_lives(t + 1, 1)
        if d <= 0.0:
            continue
        disc.append(v ** (t / 12.0))
        dens.append(d)
        paid.append(0 if t < fp else (t - fp) // p + 1)
    lo = 0.0
    hi = r_max
    for it in range(solve_max_iter):                                 # noqa: F821
        mid = 0.5 * (lo + hi)
        g = mid * a * load
        for j in range(len(dens)):
            g += disc[j] * dens[j] * max(sp - paid[j] * mid, 0.0)
        if g > target:
            hi = mid
        else:
            lo = mid
        if hi - lo <= solve_tol:                                     # noqa: F821
            break
    return 0.5 * (lo + hi)


def refund_pv():
    """The value at inception of the *Kapitalrückgewähr* leg, on the tariff basis.

    ``sum_t v^(t/12) d~_a(t) max(SP - n(t) R, 0)`` at the struck ``R``.  Zero where no
    refund is elected.  Published so that the pricing identity can be *seen* rather than
    only asserted: :func:`check_equivalence` closes ``net_single_prem()`` against
    ``R ä (1 + beta) + refund_pv()``, and on model point 3 the refund leg is a fifth of the
    *Nettoeinmalbeitrag*.
    """
    if refund_form() == "none":
        return 0.0
    v = 1.0 / (1.0 + tariff_int_rate())
    p = pay_period_mths()
    fp = first_pay_mth()
    sp = single_prem()
    r = annuity_pp_derived()
    total = 0.0
    for t in range(0, proj_len()):
        d = tariff_lives(t, 1) - tariff_lives(t + 1, 1)
        if d <= 0.0:
            continue
        n = 0 if t < fp else (t - fp) // p + 1
        total += v ** (t / 12.0) * d * max(sp - n * r, 0.0)
    return total


def max_tariff_int_rate():
    """The statutory *Höchstrechnungszins* in force at ``entry_year()``.

    Read from *hoechstrechnungszins_table.csv* by the contract's own vintage, because a
    German in-force book is a stack of cohorts and the cap that applied at conclusion stays
    with the contract for life: a 2012 point sits at 1,75 %, a 2022 point at 0,25 % and a
    2025 point at 1,00 %, the last being the first increase in about thirty years.  The two
    mid-year steps of 1994 and 2000 are assigned **[std]** to the rate in force on
    1 January of the split year.
    """
    tab = data.hoechstrechnungszins_table()                          # noqa: F821
    y = entry_year()
    for year_from in tab.index:
        if int(year_from) <= y <= int(tab.loc[year_from, "year_to"]):
            return float(tab.loc[year_from, "max_rate"])
    raise ValueError("no Hoechstrechnungszins band covers entry_year")


def surplus_init_pct():
    """u0: the *Überschussrente* at outset, as a fraction of the *garantierte Rente*.

    Read from *surplus_scale_table.csv* at ``surplus_form()``.  **[std]** — no
    *Überschussanteilsatz* was established at any carrier for any year.
    """
    return float(
        data.surplus_scale_table().loc[surplus_form(), "surplus_init_pct"])   # noqa: F821


def surplus_growth():
    """psi: the annual increase in the *Überschussrente*, at the policy anniversary.

    Read from *surplus_scale_table.csv* at ``surplus_form()``.  **[std]** — the shape is
    established and no level is.
    """
    return float(
        data.surplus_scale_table().loc[surplus_form(), "surplus_growth"])   # noqa: F821


def annuity_guar_pp(t):
    """R: the *garantierte Rente* in force in month ``t`` — level for life.

    ``annuity_pp_init()`` where the model point carries one, else
    :func:`annuity_pp_derived`.  It is immutable: § 163 VVG is the only channel by which a
    German insurer could change it after conclusion, it is narrow, and the courts have
    narrowed it further by holding a low-interest phase to be entrepreneurial risk that
    cannot be passed to policyholders.  It takes ``t`` because the notes' ``R`` does and
    because a variant that steps would have somewhere to live; here it does not step.
    """
    r = annuity_pp_init()
    if r > 0.0:
        return r
    return annuity_pp_derived()


def annuity_surp_pp(t):
    """U(t): the *Überschussrente* instalment in month ``t``.

    ``R u0 (1 + psi)^(duration(t) - defer_mths() // 12)`` from the first payment month,
    and zero before it.  Two properties, both asserted by
    :func:`check_annuity_roll_fwd`.  It steps at the **policy anniversary**, so it is
    constant across each block of twelve months and compounding it monthly is a listed
    pitfall.  And it **ratchets**: an increment bought as paid-up annuity under the
    *Bonusrente* mechanic does not come back off.

    It is an **insurer-discretionary current** quantity and never a guaranteed cash flow.
    A projection of it is a central estimate of a stream the insurer may reduce — the
    *konstante Überschussrente* included, which is exactly what the consumer literature
    warns about — and the notes' sensitivity section prices that downside rather than the
    base run reserving for it.
    """
    if t < first_pay_mth():
        return 0.0
    return (annuity_guar_pp(t) * surplus_init_pct()
            * (1.0 + surplus_growth()) ** (duration(t) - defer_mths() // 12))


def annuity_pp(t):
    """A(t): the total instalment actually paid, ``annuity_guar_pp(t) + annuity_surp_pp(t)``.

    Only the first term is a promise.  A model publishing the guaranteed annuity alone
    models less than the payment: on typical market designs the *Überschussrente* is 15 %
    to 25 % of it.
    """
    return annuity_guar_pp(t) + annuity_surp_pp(t)


def cum_annuity_guar_pp(t):
    """C(t): the **guaranteed** instalments paid to and including month ``t``.

    ``C(t) = C(t - 1) + R`` at a payment month and ``C(t - 1)`` otherwise, opened at
    ``t_start()`` at the instalments an in-force point has already been paid.  It includes
    the instalment due at ``t`` itself, because that instalment was paid at the start of
    the month in which the death occurs.

    It accumulates the **guaranteed** annuity and not the total one **[std]**: a guaranteed
    benefit cannot be defined by reference to a discretionary quantity, so
    :func:`refund_pp` is invariant to ``surplus_form``.
    """
    if t < t_start():
        return 0.0
    if t == t_start():
        if t < first_pay_mth():
            return 0.0
        n = (t - first_pay_mth()) // pay_period_mths() + 1
        return annuity_guar_pp(t) * n
    prev = cum_annuity_guar_pp(t - 1)
    if is_payment_mth(t):
        return prev + annuity_guar_pp(t)
    return prev


def refund_pp(t):
    """K(t): the *Kapitalrückgewähr* payable on a death during month ``t``.

    ``max(single_prem() - cum_annuity_guar_pp(t), 0)`` where the refund is elected, and
    identically zero where it is not.  It starts at the whole *Einmalbeitrag* and runs to
    nothing over roughly the period in which the annuitant recovers the capital nominally.

    During an *Aufschubzeit* no instalment has been paid, so ``C(t) = 0`` and this is the
    whole *Einmalbeitrag*: the *Beitragsrückgewähr* on death before *Rentenbeginn* falls
    out of the same machinery without a second mechanic.
    """
    if refund_form() == "none":
        return 0.0
    return max(single_prem() - cum_annuity_guar_pp(t), 0.0)


def payment_factor(t):
    """F(t): instalments expected to be payable at ``t``, per unit of ``pols_if_init()``.

    ``max(gamma(t), l_a(t)) + delta (1 - l_a(t)) l_s(t) (1 - gamma(t))``.

    The ``max`` is what makes the *Rentengarantiezeit* a certain floor rather than a second
    stream: inside the guarantee the full instalment goes out whether the annuitant is
    alive or not, and ``gamma + l_a`` would pay ``1 + l_a`` for the whole guarantee.  The
    survivor's leg is gated by ``(1 - gamma(t))`` for the same reason, and its
    ``(1 - l_a(t)) l_s(t)`` is the probability that the annuitant is dead and the second
    life alive at the payment instant, **assuming independence [std]** — real joint lives
    are positively dependent, so this overstates the joint-life annuity value and
    understates the rider's cost.

    Defined at every ``t``, not only at payment months; the cash flows carry the
    payment-month indicator themselves.
    """
    g = certain_floor(t)
    la = lives_if(t, 1)
    return (max(g, la)
            + surv_pct() * (1.0 - la) * lives_if(t, 2) * (1.0 - g))


def pols_if(t):
    """The probability that a **payment obligation remains** at the start of month ``t``.

    Not a policy count.  It is 1 while the guarantee period runs or the annuitant is alive,
    and it stays positive after the annuitant's death for as long as a *Hinterbliebenenrente*
    can still come into payment::

        pols_if_init x min( 1, max(gamma(t), l_a(t)) + 1{delta > 0} (1 - l_a(t)) l_s(t) )

    That is the weight the per-policy maintenance expense is carried on, which is what the
    name means everywhere else in this library — the exposure at the **start** of period
    ``t``, and the weight on that same ``result_cf()`` row's cash flows.  At the frame's
    first row it is ``pols_if_init()`` exactly, on a new-business point and an in-force one
    alike.  The ``min`` closes the one case where the two terms would otherwise overlap: a
    joint-life contract inside its guarantee period, where the full instalment is already
    going out.

    There is no lapse, surrender or paid-up exit to net off it.  The only decrement is
    death.
    """
    g = certain_floor(t)
    la = lives_if(t, 1)
    x = max(g, la)
    if surv_pct() > 0.0:
        x = x + (1.0 - la) * lives_if(t, 2)
    return pols_if_init() * min(1.0, x)


def premiums(t):
    """The *Einmalbeitrag*, an inflow at the start of month 0 and nowhere else.

    ``single_prem() x pols_if_init()`` at ``t = 0``.  An in-force model point's frame does
    not contain ``t = 0``, so it collects nothing: the premium was paid before the
    valuation date and counting it again is a listed pitfall.

    There is no premium stream, no *Beitragsdynamik* and no *Ratenzahlungszuschlag* on this
    product — the whole consideration is paid once.
    """
    if t == 0:
        return single_prem() * pols_if_init()
    return 0.0


def annuity_payments(t, kind=None):
    """Instalments paid to a living payee in month ``t``, by kind; the total when omitted.

    ``"ANNUITANT"``
        the instalment paid to the annuitant, ``pols_if_init x A(t) x l_a(t)``, at a
        payment month.

    ``"SURVIVOR"``
        the *Hinterbliebenenrente*, ``pols_if_init x A(t) x delta (1 - l_a(t)) l_s(t)``,
        gated by ``(1 - gamma(t))`` so that it never runs on top of a guaranteed
        instalment.  Zero throughout wherever ``surv_pct() == 0``.

    Payments to a *beneficiary* inside the guarantee period are not here: they are
    ``claims(t, "GUARANTEE")``, because they are paid on the strength of a death rather
    than of survival.  Splitting the stream that way separates annuity outgo from death
    outgo, which is the shape of the product, and it puts the two commonest errors — the
    additive certain floor and the survivor paid on top of the guarantee — in a column
    rather than in a total.
    """
    if kind is None:
        return sum(annuity_payments(t, k) for k in ("ANNUITANT", "SURVIVOR"))
    if not is_payment_mth(t):
        return 0.0
    if kind == "ANNUITANT":
        return pols_if_init() * annuity_pp(t) * lives_if(t, 1)
    if kind == "SURVIVOR":
        return (pols_if_init() * annuity_pp(t) * surv_pct()
                * (1.0 - lives_if(t, 1)) * lives_if(t, 2)
                * (1.0 - certain_floor(t)))
    raise ValueError("invalid kind")


def claims(t, kind=None):
    """Death outgo in month ``t``, by kind; the total when ``kind`` is omitted.

    ``"GUARANTEE"``
        the instalment paid to the beneficiaries of an annuitant who has died inside the
        *Rentengarantiezeit*, ``pols_if_init x A(t) x gamma(t) (1 - l_a(t))`` at a payment
        month.  The instalments continue as they fall due; a commuted settlement of the
        *Restgarantiezeit* exists in the market, its basis was not established at any
        carrier, and it is deliberately not implemented.

    ``"REFUND"``
        the *Kapital-* / *Beitragsrückgewähr*, ``pols_if_init x K(t) x d_a(t)``, settled on
        deaths **during** month ``t`` and already net of the instalment paid at its start.

    There is no ``"LAPSE"`` or ``"SURRENDER"`` kind, at any duration, and no
    surrender-value cells anywhere in this model: once the *Rentenbezug* has begun the
    contract cannot be terminated, so § 169 VVG is displaced and there is nothing to pay.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("GUARANTEE", "REFUND"))
    if kind == "GUARANTEE":
        if not is_payment_mth(t):
            return 0.0
        return (pols_if_init() * annuity_pp(t) * certain_floor(t)
                * (1.0 - lives_if(t, 1)))
    if kind == "REFUND":
        return pols_if_init() * refund_pp(t) * lives_death(t, 1)
    raise ValueError("invalid kind")


def infl_factor(t):
    """The expense inflation factor in month ``t``: ``(1 + expense_infl)^(t // 12)`` **[std]**.

    It steps at the **policy anniversary**, like everything else in this product, and not
    on a calendar date.
    """
    return (1.0 + expense_infl) ** (t // 12)                         # noqa: F821


def expenses(t):
    """Insurer expense in month ``t``: acquisition, maintenance and the payment run.

    Three terms, all **[std]** — no expense parameter was established at any carrier::

        1{t = 0} pols_if_init (expense_acq_rate SP + expense_acq_fixed)
      + (expense_maint_pp / 12) infl_factor(t) pols_if(t)
      + 1{payment month} expense_pay_pp infl_factor(t) pols_if_init payment_factor(t)

    The acquisition term appears at ``t = 0`` only, and therefore not at all on an in-force
    point.  The per-instalment term is weighted by :func:`payment_factor` rather than by
    :func:`pols_if`, and that is not a slip: a survivor's annuity in payment is a **second**
    payment run, and inside the guarantee the beneficiary's instalment costs the same to
    pay as the annuitant's.

    These are the expenses *incurred*.  The two tariff *loadings* — ``expense_load_alpha``
    and ``expense_load_beta`` — are pricing parameters and appear only in the equivalence.
    Keeping them apart is the point of the split: the gap between them is the modelled
    *Kostenüberschuss*, and a user replacing one set must replace the other with it or the
    modelled profit moves silently.
    """
    e = 0.0
    if t == 0:
        e = e + pols_if_init() * (expense_acq_rate * single_prem()   # noqa: F821
                                  + expense_acq_fixed)               # noqa: F821
    e = e + (expense_maint_pp / 12.0) * infl_factor(t) * pols_if(t)  # noqa: F821
    if is_payment_mth(t):
        e = e + (expense_pay_pp * infl_factor(t)                     # noqa: F821
                 * pols_if_init() * payment_factor(t))
    return e


def liability_cf(t):
    """The liability cash flow of month ``t``, **outgo positive** — the notes' orientation.

    ``annuity_payments(t) + claims(t) + expenses(t) - premiums(t)``.  The orientation a
    valuation layer consumes: a Solvency II best estimate is ``sum v(t) liability_cf(t)``
    over the relevant risk-free term structure, plus a risk margin.  Published as a column
    beside :func:`net_cf` so the sign convention is verifiable in the frame rather than
    only in prose.
    """
    return annuity_payments(t) + claims(t) + expenses(t) - premiums(t)


def net_cf(t):
    """The same stream as :func:`liability_cf`, **income positive**: ``-liability_cf(t)``.

    The library-wide sign.  The *Einmalbeitrag* in; instalments, death benefits and
    expenses out.  The shape to expect on a new-business point is one large positive month
    at ``t = 0`` — the whole *Einmalbeitrag* against one instalment and the acquisition
    expense — and a long negative tail decaying with survival.  The tail is what a
    *Deckungsrückstellung* is held against; this model does not compute one.
    """
    return -liability_cf(t)


def check_net_cf_resid(t):
    """The cash flow statement's reconciliation residual in month ``t``; zero everywhere.

    ``net_cf(t)`` less ``premiums(t) - pols_if_init x A(t) x payment_factor(t)
    - claims(t, "REFUND") - expenses(t)``, the annuity term taken at payment months and
    zero elsewhere.

    **Not a restatement of the definition.**  :func:`net_cf` reaches the instalment outgo
    through the two published legs — :func:`annuity_payments` and
    ``claims(t, "GUARANTEE")`` — while this rebuilds it through the single ``max()``
    payment factor.  So what the identity asserts is that the split into those legs is
    **exhaustive and non-overlapping**: a survivor's annuity paid on top of a guaranteed
    instalment, or a guarantee counted additively, leaves a residual here.
    """
    if is_payment_mth(t):
        paid = pols_if_init() * annuity_pp(t) * payment_factor(t)
    else:
        paid = 0.0
    return net_cf(t) - (premiums(t) - paid - claims(t, "REFUND") - expenses(t))


def check_net_cf():
    """True when the cash flow statement reconciles in every projected month.

    The library's first ruling: every model reconciles its own headline number in code and
    not only in prose.  No argument, one bool over all ``t``;
    :func:`check_net_cf_resid` gives the signed residual of the month that failed.
    """
    tol = roll_fwd_tol * max(single_prem() * pols_if_init(), 1.0)    # noqa: F821
    return bool(all(abs(check_net_cf_resid(t)) <= tol
                    for t in range(t_start(), proj_len())))


def check_lives_roll_fwd_resid(t):
    """The survival roll-forward residual at month ``t``; zero everywhere.

    ``lives_if(t + 1, life) - lives_if(t, life) (1 - mort_rate_mth(t, life))``, taken for
    whichever life gives the larger absolute value so that two lives cannot cancel.  What
    it catches is a **misindexed recursion** — rolling forward with ``q(t + 1)`` or reading
    the monthly rate at the wrong end of the month.
    """
    lives = [1]
    if surv_pct() > 0.0:
        lives.append(2)
    vals = [lives_if(t + 1, life)
            - lives_if(t, life) * (1.0 - mort_rate_mth(t, life))
            for life in lives]
    return max(vals, key=abs)


def check_lives_roll_fwd():
    """True when the survival path rolls forward and the decrements close, for every life.

    Two identities, and the second is the one that is more than a telescope of the first:
    ``sum_t lives_death(t, life) + lives_if(n, life) == lives_if(t_start(), life)``, the
    sum taken over ``t = t_start() ... n - 1`` and the tail read at the frame's exclusive
    end ``n = proj_len()``,
    built by direct summation over the death cells with no reference to the recursion that
    produced them.  Death is the only decrement in this product — there is no lapse, no
    paid-up conversion and no option exercise — so this is the whole closure identity, and
    a life that leaves and reappears fails here rather than in a cash flow.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    if not all(abs(check_lives_roll_fwd_resid(t)) <= tol
               for t in range(t_start(), proj_len())):
        return False
    lives = [1]
    if surv_pct() > 0.0:
        lives.append(2)
    for life in lives:
        deaths = sum(lives_death(t, life)
                     for t in range(t_start(), proj_len()))
        closure = (deaths + lives_if(proj_len(), life)
                   - lives_if(t_start(), life))
        if abs(closure) > tol:
            return False
    return True


def check_annuity_roll_fwd_resid(t):
    """The *Überschussrente* step residual at month ``t``; zero everywhere.

    ``annuity_surp_pp(t) - annuity_surp_pp(t - 1) x (1 + psi)^{1 if t % 12 == 0 else 0}``,
    inside the payment phase.  It asserts that the increase falls at the **policy
    anniversary** and nowhere else: compounding the surplus monthly, which is the obvious
    wrong reading of an annual rate on a monthly grid, leaves a residual at every month
    that is not a multiple of twelve.
    """
    if t <= max(t_start(), first_pay_mth()):
        return 0.0
    step = (1.0 + surplus_growth()) if t % 12 == 0 else 1.0
    return annuity_surp_pp(t) - annuity_surp_pp(t - 1) * step


def check_annuity_roll_fwd():
    """True when the *Überschussrente* steps only at anniversaries and the annuity ratchets.

    The second half is the *Bonusrente* mechanic stated arithmetically:
    ``annuity_pp(t) >= annuity_pp(t - 1)`` at every ``t``.  An increment, once bought as
    paid-up annuity, is not taken back off — which is what makes a rising
    *Überschussverwendung* ratchet rather than fluctuate.
    """
    tol = roll_fwd_tol * max(single_prem() * pols_if_init(), 1.0)    # noqa: F821
    stepped = all(abs(check_annuity_roll_fwd_resid(t)) <= tol
                  for t in range(t_start(), proj_len()))
    ratchet = all(annuity_pp(t) >= annuity_pp(t - 1) - tol
                  for t in range(t_start() + 1, proj_len()))
    return bool(stepped and ratchet)


def check_refund_run_off_resid(t):
    """The *Kapitalrückgewähr* run-off residual at month ``t``; zero everywhere.

    ``refund_pp(t) - max(refund_pp(t - 1) - R 1{payment month}, 0)``.  The refund declines
    by exactly one **guaranteed** instalment at each payment month and by nothing in
    between, and it is floored rather than allowed to go negative.
    """
    if t <= t_start():
        return 0.0
    step = annuity_guar_pp(t) if is_payment_mth(t) else 0.0
    return refund_pp(t) - max(refund_pp(t - 1) - step, 0.0)


def check_refund_run_off():
    """True when the refund runs off one instalment at a time and reaches zero on schedule.

    Where no refund is elected it asserts the stronger thing: ``refund_pp(t)`` is
    identically zero, so a refund cannot leak into a contract that did not buy one.

    Where one is elected it asserts the recursion, that the benefit is non-increasing, that
    it has reached zero by the end of the projection, and — independently of the recursion —
    that the number of instalments needed to exhaust it is ``ceil(SP / R)`` counted
    directly.  The last is what catches a refund measured against the *total* annuity: the
    *Überschussrente* would retire the capital sooner and the count would not match.
    """
    tol = roll_fwd_tol * max(single_prem() * pols_if_init(), 1.0)    # noqa: F821
    if refund_form() == "none":
        return bool(all(refund_pp(t) == 0.0
                        for t in range(t_start(), proj_len())))
    if not all(abs(check_refund_run_off_resid(t)) <= tol
               for t in range(t_start(), proj_len())):
        return False
    if not all(refund_pp(t) <= refund_pp(t - 1) + tol
               for t in range(t_start() + 1, proj_len())):
        return False
    if refund_pp(proj_len() - 1) > tol:
        return False
    r = annuity_guar_pp(t_start())
    n_req = 0
    while n_req * r < single_prem() - tol:
        n_req = n_req + 1
    t_zero = first_pay_mth() + (n_req - 1) * pay_period_mths()
    if t_zero >= proj_len():
        return True
    if refund_pp(t_zero) > tol:
        return False
    if t_zero - pay_period_mths() >= max(t_start(), first_pay_mth()):
        if refund_pp(t_zero - pay_period_mths()) <= tol:
            return False
    return True


def check_payment_factor_resid(t):
    """The instalment-split residual at month ``t``; zero everywhere.

    ``annuity_payments(t) + claims(t, "GUARANTEE")`` less
    ``pols_if_init x A(t) x payment_factor(t)`` at a payment month, and less zero at every
    other month.  It is the arithmetic statement that the three legs — annuitant, survivor,
    guarantee beneficiary — partition the instalment exactly, with nothing double-counted
    and nothing dropped.
    """
    lhs = annuity_payments(t) + claims(t, "GUARANTEE")
    if is_payment_mth(t):
        rhs = pols_if_init() * annuity_pp(t) * payment_factor(t)
    else:
        rhs = 0.0
    return lhs - rhs


def check_payment_factor():
    """True when the instalment splits exactly into its three legs at every month."""
    tol = roll_fwd_tol * max(single_prem() * pols_if_init(), 1.0)    # noqa: F821
    return bool(all(abs(check_payment_factor_resid(t)) <= tol
                    for t in range(t_start(), proj_len())))


def check_guarantee_certain_resid(t):
    """``payment_factor(t) - 1`` at a payment month inside the *Rentengarantiezeit*; else 0.

    Inside the guarantee the instalment is **certain**, whatever ``delta`` is: the full
    instalment goes out to the annuitant or to the beneficiaries, and the survivor's leg is
    gated off.  A factor above 1 means the survivor is being paid on top; a factor below 1
    means the guaranteed instalments are being decremented for survival, which is the
    single largest overstatement-of-margin error available on this product.
    """
    if is_payment_mth(t) and first_pay_mth() <= t < guar_end_mth():
        return payment_factor(t) - 1.0
    return 0.0


def check_guarantee_certain():
    """True when every instalment inside the *Rentengarantiezeit* is certain.

    Vacuously true on a model point with no guarantee period, which is the honest reading:
    there is nothing to be certain about.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    return bool(all(abs(check_guarantee_certain_resid(t)) <= tol
                    for t in range(t_start(), proj_len())))


def check_equivalence_resid():
    """The pricing residual: ``net_single_prem() - (R ä (1 + beta) + refund_pv())``.

    Takes **no argument**, unlike the other residuals in this Space, because the identity
    it belongs to is struck once at inception rather than holding period by period.  Zero
    by construction on an in-force point, where there is no equivalence to assert.
    """
    if annuity_pp_init() > 0.0:
        return 0.0
    return net_single_prem() - (annuity_pp_derived() * annuity_factor()
                                * (1.0 + expense_load_beta) + refund_pv())   # noqa: F821


def check_equivalence():
    """True when the *Nettoeinmalbeitrag* buys exactly the annuity and the refund leg.

    On a **derived** point this is the whole pricing identity, and on a point with a refund
    it is the only thing that distinguishes a solved annuity from an evaluated one: the
    naive answer — the no-refund annuity, less a refund cost computed at that annuity —
    fails here by a wide margin.

    On an **in-force** point it returns True without asserting anything, the annuity having
    been struck years ago on a basis this model does not reproduce.  That is stated here
    rather than left for a reader to discover from a check that passes vacuously.

    The tolerance is ``roll_fwd_tol`` scaled by the *Nettoeinmalbeitrag*, because the
    identity is an equality between euro amounts of that size and the refund solve
    converges on ``R`` rather than on the residual.
    """
    if annuity_pp_init() > 0.0:
        return True
    tol = roll_fwd_tol * max(net_single_prem(), 1.0)                 # noqa: F821
    return bool(abs(check_equivalence_resid()) <= tol)


def check_death_option_xor():
    """True when at most one death-benefit family is in force on the model point.

    ``refund_form() == "none"`` **or** (``guar_years() == 0`` and ``surv_pct() == 0``).

    The *Kapitalrückgewähr* and the *Rentengarantiezeit* both protect against early death —
    one with a declining lump sum, the other with a fixed number of payments — and a buyer
    who takes both pays for both.  Which German carriers permit the combination was not
    established, so this implementation makes them exclusive **[std]** and asserts the
    exclusivity rather than assuming it: the refund's implicit pricing equation is written
    against a plain annuity leg, and a model point combining the two would price a
    guarantee the solve does not see.
    """
    return bool(refund_form() == "none"
                or (guar_years() == 0 and surv_pct() == 0.0))


def check_tariff_int_rate():
    """True when the tariff *Rechnungszins* is within the cap of the contract's own vintage.

    ``tariff_int_rate() <= max_tariff_int_rate() + roll_fwd_tol``.  An **inequality**, not
    an equality: the *Höchstrechnungszins* binds the reserving rate and, through the VAG,
    the rate a new tariff may be priced at, but a carrier may price below it and one in the
    corpus is observed pricing a guaranteed annuity factor at 0 % while the statutory
    maximum was positive.
    """
    return bool(tariff_int_rate()
                <= max_tariff_int_rate() + roll_fwd_tol)             # noqa: F821


def result_cf():
    """Result table of cash flows, indexed by month ``t``.

    ``pols_if`` is the start-of-month obligation weight, which is the weight applied to the
    maintenance expense on the same row.  ``annuity_payments`` is the total of the
    ANNUITANT and SURVIVOR legs; ``claims_guarantee`` is the instalment paid to the
    beneficiaries of an annuitant who died inside the *Rentengarantiezeit* and
    ``claims_refund`` the *Kapitalrückgewähr*.  ``liability_cf`` is the notes'
    outgo-positive orientation and ``net_cf`` its negative.

    The frame runs ``t_start() ... proj_len() - 1`` and stops.  There is no maturity payment
    and no tail state: the annuitant's survival has reached zero and the guarantee has
    expired, so nothing remains to be paid.
    """
    ts = list(range(t_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "claims_guarantee": [claims(t, "GUARANTEE") for t in ts],
            "claims_refund": [claims(t, "REFUND") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of survival, instalments and per-policy amounts, indexed by month ``t``.

    The state behind :func:`result_cf`: the two survival paths, the certain floor and the
    payment factor built from them, the three-way split of the instalment into guaranteed
    and surplus parts, and the refund's run-off against the cumulative guaranteed
    instalments.
    """
    ts = list(range(t_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "lives_if_1": [lives_if(t, 1) for t in ts],
            "lives_if_2": [lives_if(t, 2) for t in ts],
            "certain_floor": [certain_floor(t) for t in ts],
            "payment_factor": [payment_factor(t) for t in ts],
            "annuity_guar_pp": [annuity_guar_pp(t) for t in ts],
            "annuity_surp_pp": [annuity_surp_pp(t) for t in ts],
            "annuity_pp": [annuity_pp(t) for t in ts],
            "refund_pp": [refund_pp(t) for t in ts],
            "cum_annuity_guar_pp": [cum_annuity_guar_pp(t) for t in ts],
            "pols_if": [pols_if(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

expense_load_alpha = 0.025

expense_load_beta = 0.02

expense_acq_rate = 0.02

expense_acq_fixed = 200.0

expense_maint_pp = 60.0

expense_pay_pp = 1.5

expense_infl = 0.015

mix_male = 0.45

mort_base_year = 2025

omega_age = 121

roll_fwd_tol = 1e-08

solve_tol = 1e-10

solve_max_iter = 200

pd = ("Module", "pandas")
