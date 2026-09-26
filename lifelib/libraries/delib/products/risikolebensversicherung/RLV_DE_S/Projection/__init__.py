# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.RLV_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 8            # or switch the default

``t`` counts **policy months from issue** and is **0-based**, the clock
``basiclife.BasicTerm_S`` and the other nine delib models run on: ``t = 0`` is the first
policy month, month ``t`` runs from time ``t`` to time ``t + 1``, ``pols_if(t)`` is the
count at time ``t``, and ``proj_len() = 12 x policy_term`` is the **number** of projected
months — 300 on the anchor cell — and so the frame's **exclusive end**, the loop being
lifelib's ``for t in range(proj_len())``. A new-business model point opens at ``t = 0``;
an **in-force** model point opens at ``t = proj_start() = 12 x duration_y``, so that
everything keyed to duration reads off one clock and needs no second one. There is nothing
after ``proj_len() - 1``: the survivors' cover simply expires, nothing is payable, and
``pols_if(proj_len())`` is exactly zero.

Everything *contractual* about this product is nevertheless on an **annual** cycle — the
level *Bruttobeitrag* struck once by first-order equivalence, the annual
*Überschussdeklaration* behind the *Beitragsverrechnung*, the *Versicherungssumme*
schedule, the *Nachversicherungsgarantie* increments, the § 161 three-year window, the
*Beitragszahlungsdauer*, the lapse table and the first-order *Deckungskapital* — and the
model keeps all of them there. So the policy year is derived and used as a lookup key
throughout: ``duration_mth(t) = t`` is the completed policy months at the start of month
``t``, ``duration(t) = duration_mth(t) // 12`` the completed policy years,
``policy_year(t) = duration(t) + 1`` the contractual 1-based label the three schedule CSVs
are keyed on, and the attained age is ``age(t) = issue_age + duration(t)``, stepping on
the anniversary and not monthly. The frame is indexed by ``t``; the policy year is derived
and never indexed by. Cover ends at attained age ``issue_age + policy_term``;
``cover_end_age()`` is derived from the term rather than carried beside it, so the two
cannot disagree.

The two-speed structure that follows is the library's convention: :func:`mort_rate` and
:func:`lapse_rate` are the **annual** rates of the policy year containing month ``t`` —
the vectors the technical notes tabulate — and :func:`mort_rate_mth` and
:func:`lapse_rate_mth` are the monthly rates actually applied, derived at
``1 - (1 - r)^(1/12)`` so that twelve of them compound back to exactly the year's rate.
:func:`result_cf_annual` sums the monthly frame into policy years, which is the view the
notes' worked example is stated on.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/risikolebensversicherung/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec,
no embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RLV_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.RLV_DE_S.Data`, reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
mort_table_file           data.mort_table()                  mort_table.csv
benefit_schedule_file     data.benefit_schedule()            benefit_schedule.csv
nvg_schedule_file         data.nvg_schedule()                nvg_schedule.csv
lapse_file                data.lapse_table()                 lapse_table.csv
freq_loading_file         data.freq_loading_table()          freq_loading_table.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind``
string, ``*_at(t, timing)`` for within-year reads. The technical notes use compact
actuarial symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
(none)                     model_point()                   The selected model point row
n = policy_term            proj_len_y()                    Number of policy years
12 n                       proj_len()                      Number of projected months
t0 = 12 duration_y         proj_start()                    First projected month index
(none)                     duration_mth(t)                 Completed policy months, = t
(none)                     duration(t)                     Completed policy years, t // 12
y = duration(t) + 1        policy_year(t)                  Contractual 1-based policy year
x(t)                       age(t)                          Attained age, first life
x2(t)                      age2(t)                         Attained age, second life
S0                         sum_assured()                   Initial Versicherungssumme
k                          prem_term()                     Beitragszahlungsdauer
f(t)                       benefit_factor(t)               Versicherungssumme schedule
u(t)                       sum_uplift(t)                   Cumulative NVG multiplier
B(t)                       benefit_pp(t)                   Versicherungssumme in year t
(none)                     benefit_paid_pp(t)              What a death claim pays
sigma(t)                   suicide_factor(t)               Para 161 benefit switch
q(x) tilde                 mort_rate_at_age(s, r, x)       Shipped table rate
Q(t) tilde                 mort_rate_base(t)               Own-sex rate, first death
(unisex blend)             mort_rate_blend(t)              50/50 blend, first death
q2(t)                      mort_rate(t)                    Second-order annual rate
q2m(t)                     mort_rate_mth(t)                The same, applied in month t
q1(t)                      mort_rate_tar(t)                First-order tariff rate
rf                         rating_factor()                 Risikozuschlag multiplier
w(t)                       lapse_rate(t)                   Annual lapse rate of the year
wm(t)                      lapse_rate_mth(t)               The same, applied in month t
(table)                    lapse_rate_base(t)              Table lapse rate
w_cum(t)                   lapse_cum(t)                    Cumulative lapse proportion
M_shock(t)                 shock_lapse_factor(t)           Premium-shock multiplier
(none)                     sel_lapse_factor(t)             Loading on persisters
v^y                        disc_factor(y)                  Rechnungszins discount
p1(y)                      pols_tariff(y)                  Tariff survivorship, no lapse
ae                         tariff_annuity()                Premium annuity-due
A                          tariff_claims_pv()              APV of death benefits
Gamma                      tariff_sum_pv()                 Sum-exposure annuity
G                          prem_gross_level_pp()           Bruttobeitrag, before phi
Gn                         prem_net_level_pp()             Actuarial Nettopraemie
v_d                        beitragsverrechnung_rate()      Beitragsverrechnungssatz
phi                        prem_freq_load()                Ratenzahlungszuschlag
G phi                      prem_gross_pp(t)                Bruttobeitrag, annual
v_d G phi                  prem_rebate_pp(t)               Beitragsverrechnung, annual
P(t)                       prem_paid_pp(t)                 Zahlbeitrag, annual
(none)                     instalments()                   Instalments a year, 1/2/4/12
(none)                     prem_cycle()                    Months between instalments
(none)                     prem_due(t)                     Is an instalment due in month t
(none)                     prem_gross_inst_pp(t)           Gross instalment collected
(none)                     prem_rebate_inst_pp(t)          Rebate netted off it
P_inst(t)                  prem_inst_pp(t)                 Zahlbeitrag instalment
(reserve)                  res_pp_at(y, timing)            First-order Deckungskapital
(gezillmert)               res_zill_pp_at(y, timing)       The same, less the Zillmer
l(t)                       pols_if(t)                      In force, start of period t
l(t)(1-q2m), l(t+1)        pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
pols_death(t)              pols_death(t)                   Expected deaths in month t
pols_lapse(t)              pols_lapse(t)                   Expected lapses in month t
pols_maturity(t)           pols_maturity(t)                Expiring survivors, last month
premiums(t)                premiums(t)                     Zahlbeitrag income, billed
prem_gross(t)              prem_gross(t)                   Bruttobeitrag, guaranteed
prem_rebate(t)             prem_rebate(t)                  Beitragsverrechnung, in force
claims_death               claims(t, kind)                 Benefit outgo by kind
z k G                      acq_cost_pp()                   Acquisition cost at issue
c0 k G                     comm_init_pp()                  Initial Abschlussprovision
(1 + pi)^duration(t)       inflation_factor(t)             Expense inflation factor
maint(t)                   maint_pp(t)                     Admin plus collection cost
expenses(t)                expenses(t)                     Total expense, ex commission
commissions(t)             commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
(the notes' table)         result_cf_annual()              result_cf() summed by policy year
=========================  ==============================  ==========================

Four names needed care.

**The three "netto"s.** Three unrelated things are called *netto* in this product and
confusing them is the classic implementation error. :func:`prem_net_level_pp` is the
**actuarial** *Nettoprämie* ``Gn = A / ae``: the risk premium on the first-order basis
before expense loadings, a pricing quantity that never becomes a cash flow and is used
only by the reserve. :func:`prem_paid_pp` is the **consumer** *Zahlbeitrag*, what is
actually billed. The *Nettotarif* — a commission-free tariff sold through fee-based
advice — is a third, unrelated sense and is not modelled. The bare word *Nettobeitrag* is
never a name here, and ``prem_net_pp`` is on the library's retired-names register.

The order between the first two is worth stating, because the intuition gets it backwards:
on the shipped calibration ``prem_paid_pp(0)/phi = 733.01 < prem_net_level_pp() =
1 084.80 < prem_gross_pp(0)/phi = 1 275.41``. The billed premium sits **below** the
actuarial net premium, because ``Gn`` is struck on the loaded first-order rate and 90 % of
that loading is handed straight back as *Beitragsverrechnung*. A test asserting
``Gn < P`` is asserting the absence of the product's central mechanic.

**``q1`` prices and ``q2`` projects.** :func:`mort_rate_tar` is the first-order tariff
rate — the unisex 50/50 blend, loaded by ``(1 + sicherheitszuschlag_m)`` and by the
*Risikozuschlag* — and it enters the premium and the reserve and **nothing else**.
:func:`mort_rate` is the second-order rate on the policy's own sex and smoker status and
it drives every decrement and every claim. The ratio between them is *not* ``1 + m``: it
is ``2.25 x (unisex blend / own-sex rate)``, which on the shipped proxy is **1.6875 for a
male and 3.375 for a female**. That asymmetry is the unisex cross-subsidy and it is a
product fact, not a modelling artefact. Applying the *Sicherheitszuschlag* to the
projection is the pitfall; ``claims_death`` must be invariant to ``sicherheitszuschlag_m``
while ``prem_gross`` is not.

**``B(t)`` is the contractual sum; what a claim pays is not always ``B(t)``.**
:func:`benefit_pp` is ``S0 f(t) u(t)``, and :func:`benefit_paid_pp` applies the § 161
switch **tranche by tranche**: the base cover and each *Nachversicherungsgarantie*
increment carry their own three-year window, so in a year when one tranche is inside its
window and another is not, :func:`suicide_factor` — defined as the ratio of the two — is a
weighted average strictly between ``1 - suicide_share`` and ``1``. The switch touches
death claims and nothing else; it never reaches a lapse or an expiry, both of which pay
nothing in any event.

**``expenses`` here excludes ``commissions``.** The notes' identity is ``net_cf =
premiums - claims - expenses - commissions`` and :func:`result_cf` publishes the four
parts, so subtracting both is right rather than double-counting. That is the opposite
convention from ``frlib.TD_FR_S``, where the notes fold commission into the expense total,
and it is stated here because the two libraries' columns look alike and do not mean the
same thing. :func:`check_net_cf` is the identity in code.

.. rubric:: Two premium streams, and why one is not enough

This is the German delta and it is visible in the frame rather than buried in a parameter.
The **Bruttobeitrag** ``G`` is struck once, at issue, by first-order equivalence on tariff
survivorship — mortality only, no lapse — so it is acyclic with respect to everything
behavioural::

    G = ( A + gamma Gamma ) / ( (1 - beta) ae - z k )

With ``premium_form = einmal`` the paying term ``k`` is 1 and ``ae`` is 1, so the same
expression returns the *Einmalbeitrag*: the second premium form is this engine at a
boundary, not a second engine.

The **Zahlbeitrag** follows from the surplus mechanic rather than from an assumption. The
tariff's own mortality margin has actuarial value ``(m/(1+m)) A`` at issue, and the
declared *Beitragsverrechnungssatz* returns ``surplus_share`` of it over the paying term::

    v_d = min( v_max, decl_scale surplus_share (m/(1+m)) A / (G ae) )
        = decl_scale surplus_share (m/(1+m)) [ 1 - beta - (gamma Gamma + z k G)/(G ae) ]

— the surplus share, times the margin fraction of the risk element, times the risk share
of the gross premium. On the anchor cell the bracket is 0.8506, so ``v_d = 0.42527476``
and ``Zahlbeitrag / Bruttobeitrag = 0.574725``, reproducing the research file's frozen
[std] ratio **from the mechanic rather than by assumption**. Raising the
*Sicherheitszuschlag* raises ``G`` and ``v_d`` together, which is why the *Bruttobeitrag*
moves far more than the *Zahlbeitrag* — the most useful single result in this product, and
the reason the billed premium is derived.

``surplus_form = keine`` is the § 153-excluded non-participating tariff: ``v_d`` is zero
and the billed premium *is* the guaranteed one, which is model point 12.

.. rubric:: Modules that are off in the base run

Two behavioural constructions are implemented and switched off, so the base run reproduces
the worked example while the machinery stays visible and testable:

- **Premium-shock lapse**, ``shock_lapse_lambda = 0``.
  ``M_shock(t) = 1 + lambda_s max(0, prem_paid_pp(t)/prem_paid_pp(t-1) - 1)``. The
  product's distinctive behavioural risk is that the insurer can raise the bill without
  changing a guaranteed term, simply by cutting the declaration — no § 163 procedure, no
  *Treuhänder*, no policyholder remedy. The module is inert in the base run because the
  billed premium is level there; it bites exactly when ``decl_scale`` is stressed, which
  is when it should. A stress that raises the *Zahlbeitrag* toward the *Bruttobeitrag* and
  leaves lapse unchanged is understating itself.
- **Selective lapse**, ``sel_lapse_lambda = 0``, with ``sel_lapse_ref = 0.25``.
  ``q2_eff = q2 (1 + lambda max(0, w_cum - w_ref))``. Healthy lives can re-underwrite into
  a cheaper contract and impaired lives cannot, so persisters' mortality drifts up. delib
  does not model it in the base run — one basis for stayers and leavers — which is a
  stated simplification rather than an oversight.

Both are driven off the premium and the lapse table alone, never off ``pols_if``, so the
projection stays acyclic: a pricing quantity struck by equivalence cannot depend on a
behavioural assumption that depends on the path that depends on the premium.

.. rubric:: No cash value, anywhere — and yet a reserve

§ 169 Abs. 1 VVG confines the surrender-value duty to a life insurance whose insured event
is certain to occur; a term assurance's is not, so there is no *Rückkaufswert*. § 165's
*Beitragsfreistellung* right and § 166's paid-up conversion on non-payment both collapse
into the same nil through the minimum-benefit test, the paid-up sum a term contract's
reserve buys failing it in most durations. So a lapse is a pure decrement: it moves
``pols_if`` and pays nothing, ``claims(t, "LAPSE")`` and ``claims(t, "MATURITY")`` are
zero columns published rather than dropped, and :func:`check_no_cash_value` asserts it on
every model point. The 30-day § 152 *Widerrufsfrist* sits inside the year-one lapse rate
**[std]**.

What is **not** true is that nothing accumulates. A level premium charged against a rising
death rate necessarily overcharges early and undercharges late, and the difference is a
*Deckungskapital* that builds, peaks near the middle of the term and runs off to exactly
zero at expiry — on the anchor cell it peaks at 7 553,29 €, 2,5 % of the sum insured, at
``t = 15``. :func:`res_pp_at` publishes it and :func:`check_res_roll_fwd` asserts the
Thiele recursion, ``res_pp_at(0) = 0`` by the equivalence and ``res_pp_at(n) = 0`` by
exhaustion. **It is a pricing diagnostic and not a balance-sheet provision**: it is net,
it is not *gezillmert*, it is not floored, it enters no cash flow, and nothing in this
library discounts a published cash flow. :func:`res_zill_pp_at` subtracts the unamortised
Zillmer balance and is ``-z k G`` at ``t = 0`` — negative from the first day and back to
zero at expiry, which is what *Zillmerung* on a contract with almost no reserve looks like.

.. rubric:: The last policy year has no lapse, and why

Lapses fall at the **end** of the month, after the death decrement, and the end of the
last month ``t = proj_len() - 1`` is the moment cover expires. A lapse and an expiry are
then the same event paying the same nothing, so :func:`lapse_rate` returns 0 through the
**whole of the final policy year** — ``duration(t) >= proj_len_y() - 1``, months 288 to
299 on the anchor cell — and the surviving cohort leaves through :func:`pols_maturity`
instead. The zero covers the year rather than merely its last month because that is what
the annual-step model this replaced said of it, and it is what keeps the expiring cohort
at the figure the notes publish. The table's own row for policy year ``n`` still reads
3 %: the zero is a property of the last policy year, not of the assumption, and putting
it in the formula is what keeps the two readable apart.

No cash flow moves either way — the split only decides how the closure identity divides
between the three exits — but the identity itself is load-bearing, and
:func:`check_pols_roll_fwd` asserts that they account for the whole cohort:
``0.03261764`` deaths, ``0.53597922`` lapses and ``0.43140314`` expiries on the anchor
cell, summing to ``pols_if_init() = 1`` exactly. The expiring cohort is the annual-step
model's own figure to the last digit, because it is a survivorship the two grids share;
the **split between deaths and lapses** moved by 0.00044, which is the one thing
interleaving the two decrements monthly genuinely changes — on an annual grid a year's
lapses are taken from a block that has already borne the whole year's mortality, and on a
monthly one each decrement erodes the exposure the other works on.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — billed premiums in, claims, expenses and
commission out — which is the notes' own orientation and the library-wide sign.
:func:`liability_cf` publishes the same stream outgo-positive,
``liability_cf(t) = -net_cf(t)`` exactly, so a best-estimate liability is
``sum v(t) liability_cf(t)`` over whatever discount curve the valuation layer supplies.
Both are columns of :func:`result_cf`, so the identity is verifiable in the frame rather
than only in prose.

The shape to expect on the anchor, read on :func:`result_cf_annual`, is a year-one strain
of -351,88 €, the acquisition cost and the initial commission together exceeding the first
year's billed premium; thin positive years while the level premium runs ahead of the
natural risk premium; and a crossover in **policy year 14** after which the rising death
rate takes the year negative. Within policy year 1 the monthly frame shows the shape the
annual grid could not: +733,01 € of premium against 826,64 € of acquisition cost and
commission in month 0, a net -108,90 €, then eleven months of about -22 € each as claims
and maintenance accrue against no further premium. The **total** is -644,78 € on model
point 1 and strongly positive on model point 2, and the difference is the unisex
cross-subsidy: the tariff prices a 50/50 blend, the declaration returns 90 % of the margin
measured against that blend, and a male life then claims a third more than the tariff's
own best estimate while paying the same premium as a female one. That is the product
working as the law requires it to, not a defect.

.. rubric:: What the monthly grid changes, and what it does not

The grid is monthly; the **product is not**. Every contractual mechanic stays exactly
where the contract puts it, and each of the following is a decision taken deliberately
rather than inherited from the frame:

- the whole first-order equivalence — the *Bruttobeitrag* ``G``, the *Nettoprämie* ``Gn``,
  the *Beitragsverrechnungssatz* ``v_d`` and the *Deckungskapital* — stays an **annual**
  construction on policy-year arguments (:func:`disc_factor`, :func:`pols_tariff`,
  :func:`res_pp_at`), so every one of them is **bit-identical** to the annual-step model's;
- the *Versicherungssumme* schedule and the *Nachversicherungsgarantie* steps on the
  **anniversary** (:func:`benefit_factor`, :func:`sum_uplift`), so a declining sum insured
  does not decline monthly;
- the § 161 three-year window runs in whole years from issue, tranche by tranche
  (:func:`benefit_paid_pp`), and every boundary it has therefore falls on an anniversary;
- the *Beitragszahlungsdauer* ends on an anniversary (:func:`prem_gross_pp`) and the
  *Bestandspflegeprovision* starts on one (:func:`commissions`);
- expenses inflate **by policy year**, stepping on the anniversary
  (:func:`inflation_factor`), which is ``Sofort_DE_S``'s form rather than ``FRV_DE_S``'s
  continuous one;
- the zero lapse rate of the final projected year covers that whole **year**
  (:func:`lapse_rate`), because the annual model stated it of a year;
- the premium-shock module compares **consecutive renewals** twelve months apart
  (:func:`shock_lapse_factor`) and the selective-lapse loading reads a cumulative lapse
  built from the monthly rates (:func:`lapse_cum`), so both stay experience statements
  about a year rather than about a month.

What the finer grid does resolve is everything that is **not** a contract term. The
*Zahlweise* is now real: a modal *Zahlbeitrag* is collected in instalments on its own
cycle (:func:`prem_inst_pp`) instead of whole at the anniversary, so the four
fractionated model points collect 0,95 %-1,67 % less over the run — model point 4's
*monatlich* premium income falls from 4 471,82 € to 4 400,26 € — which is the
premium-cessation rule biting where an annual grid could not express it, and the
*Ratenzahlungszuschlag* at last charging for a service the model renders. Claims fall in
the month of claim rather than at the year end, so the anchor's death claims fall from
9 899,20 € to 9 768,05 €. Maintenance accrues a twelfth a month on the in-force of that
month rather than of the anniversary, so expense falls from 2 396,51 € to 2 367,66 €. And
§ 168 VVG's *Versicherungsperiode*, which follows the *Zahlweise* and which the annual
grid could only book at anniversaries and call an approximation, is simply expressed.

That is also what makes the two grids reconcile. Because the monthly death rate and the
monthly lapse rate each compound back to their policy year's annual rate, the recursion
collapses over any twelve months of one policy year to
``l(t+12) = l(t)(1 - q2(t))(1 - w(t))`` — the annual-step recursion, term for term — so
``pols_if(12k)`` here equals the annual model's ``pols_if(k)`` to 4e-15 across all
fourteen model points, and every annual contractual quantity is unmoved.
:func:`result_cf_annual` sums the frame into policy years so the two can be laid side by
side.
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
    return model_point()["policy_id"]


def issue_age():
    """The *Eintrittsalter* of the first *versicherte Person*.

    The age basis is *Alter am Jahrestag* — the attained age at the policy anniversary,
    which is also this model's projection step, so ``age(t) = issue_age + t``
    exactly.  Germany has no counterpart to the French *différence de millésime*, where
    the rating age steps on 1 January irrespective of birth month; on a real-date
    implementation the offset here is at most a few months **[std]**.
    """
    return int(model_point()["issue_age"])


def sex():
    """The first life's sex, M or F.  **Decrement only — it must never enter pricing.**

    Art. 5(2) of the Gender Directive was struck down by *Test-Achats* with effect for
    contracts concluded from 21 December 2012, so no German premium written since may
    differ by sex.  :func:`mort_rate_tar` therefore reads the **blend** of the two tables
    and never this cells, while :func:`mort_rate` reads it and nothing else does.

    The tension worth knowing is that DAV 2008 T is itself sex-distinct, so every German
    unisex term tariff is a blend at a mixing ratio the carrier chooses from its own
    expected new-business mix — proprietary, unpublished and periodically re-estimated.
    ``sex_mix_male`` is the model's **[std]** 50/50 stand-in for it, and it is one of the
    largest single sources of unexplained rate spread between German carriers.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def smoker():
    """The first life's *Raucher* / *Nichtraucher* status, R or N.

    The largest rating split after age, and unlike ``sex`` it is a lawful one: the DAV
    *Richtlinie* states that DAV 2008 T R and DAV 2008 T NR are in principle suitable for
    premium calculation differentiated by smoking status — **but not for policies written
    without a *Gesundheitsprüfung***, which is why simplified-issue German death covers
    are aggregate-rated.  It enters both mortality bases, so a smoker pays more *and* is
    expected to claim more.
    """
    v = model_point()["smoker"]
    if v not in ("N", "R"):
        raise ValueError("invalid smoker")
    return v


def sum_assured():
    """S0: the initial *Versicherungssumme*, in euros.

    The sum actually at risk in period ``t`` is :func:`benefit_pp`, which applies the
    schedule and any *Nachversicherungsgarantie* uplift on top of this.
    """
    return float(model_point()["sum_assured"])


def policy_term():
    """The *Versicherungsdauer* in whole years; equals :func:`proj_len`."""
    return int(model_point()["policy_term"])


def prem_term():
    """k: the *Beitragszahlungsdauer* in whole years, at most :func:`policy_term`.

    An ***abgekürzte Beitragszahlungsdauer*** — premiums stopping before cover does — is
    model point 6, where ``k = 12`` against a twenty-year term.  It is the configuration
    that builds the largest *Deckungskapital* in the shipped set, and the one HGB § 341f
    has in mind when it requires a provision for future administration costs where the
    paying period is shorter than the cover period.
    """
    k = int(model_point()["prem_term"])
    if k < 1 or k > policy_term():
        raise ValueError("prem_term outside 1 .. policy_term")
    return k


def premium_form():
    """The premium form: ``laufend`` or ``einmal``.

    ``laufend`` is a level *Bruttobeitrag* over ``prem_term`` years and is the German
    market form.  ``einmal`` is a **[std]** construction — no German standalone
    *Risikolebensversicherung* in the research corpus is written on a single premium — and
    is carried because it is the degenerate case ``k = 1`` of the same equivalence, so it
    exercises the premium engine at a boundary rather than adding a second engine.  The
    cells is a stated consistency gate: ``einmal`` requires ``prem_term = 1``.
    """
    v = model_point()["premium_form"]
    if v not in ("laufend", "einmal"):
        raise ValueError("invalid premium_form")
    if v == "einmal" and prem_term() != 1:
        raise ValueError("einmal requires prem_term = 1")
    return v


def prem_freq():
    """The *Zahlweise*: ``jaehrlich``, ``halbjaehrlich``, ``vierteljaehrlich`` or ``monatlich``.

    On an annual grid the frequency reaches the cash flows through the
    *Ratenzahlungszuschlag* alone; the within-year timing of the instalments is not
    modelled.  What is worth recording is the consequence the annual grid **cannot**
    represent: § 168 VVG makes the *Versicherungsperiode* follow the *Zahlweise*, so a
    monthly-paying contract is terminable monthly and its exits are not concentrated at
    policy anniversaries.  This model books them at anniversaries and says so.
    """
    return model_point()["prem_freq"]


def benefit_schedule_id():
    """The key into *benefit_schedule.csv* naming this policy's *Versicherungssumme* shape."""
    return model_point()["benefit_schedule_id"]


def nvg_schedule_id():
    """The key into *nvg_schedule.csv* naming this policy's *Nachversicherungsgarantie*."""
    return model_point()["nvg_schedule_id"]


def surplus_form():
    """``beitragsverrechnung`` or ``keine``.

    ``beitragsverrechnung`` is the market form and the base design: the declared surplus
    is netted against the *Bruttobeitrag* before billing.  ``keine`` is the § 153-excluded
    non-participating tariff — lawful, since participation may be excluded by express
    agreement, and not the market form; none was located.  It sets
    :func:`beitragsverrechnung_rate` to zero, so the billed premium *is* the guaranteed
    one, which is model point 12 and the cleanest available control on the whole surplus
    mechanic.
    """
    v = model_point()["surplus_form"]
    if v not in ("beitragsverrechnung", "keine"):
        raise ValueError("invalid surplus_form")
    return v


def lives():
    """1 for a single life, 2 for *verbundene Leben* paying on the **first** death.

    One chassis parameterised by the number of lives, not two products.  Both lives are
    underwritten and both give the § 150 VVG *schriftliche Einwilligung*; one payment is
    ever made and the contract then ends.
    """
    n = int(model_point()["lives"])
    if n not in (1, 2):
        raise ValueError("lives must be 1 or 2")
    return n


def issue_age2():
    """The *Eintrittsalter* of the second life; 0 where ``lives = 1``."""
    return int(model_point()["issue_age2"])


def smoker2():
    """The second life's smoker status, R or N; ``-`` where ``lives = 1``."""
    v = model_point()["smoker2"]
    if v not in ("N", "R", "-"):
        raise ValueError("invalid smoker2")
    if lives() == 2 and v == "-":
        raise ValueError("lives = 2 requires a smoker2 of N or R")
    return v


def rating_factor():
    """rf: the *Risikozuschlag*, a multiplier on the **mortality basis**; 1.00 standard.

    A German impairment loading is normally expressed as a percentage of the risk premium
    rather than as a benefit exclusion, life *Leistungsausschlüsse* being used sparingly.
    So it multiplies **both** orders — :func:`mort_rate` and :func:`mort_rate_tar` alike —
    and an impaired life pays more *and* is expected to claim more.  The consequence worth
    testing is the invariance: ``prem_paid_pp(0)/prem_gross_pp(0)`` barely moves when the
    factor goes from 1.00 to 1.75, because the rebate scales with the loading it is struck
    on.  The alternative reading, in which the loading is pure price and falls through to
    surplus, is a listed pitfall rather than an alternative default.  **No German carrier
    publishes a *Risikozuschlag* scale**, so the levels in the model point table are
    **[std]**.
    """
    return float(model_point()["rating_factor"])


def mort_table_id():
    """The key into *mort_table.csv*; one table ships, ``dav2008t_proxy``."""
    return model_point()["mort_table_id"]


def duration_y():
    """Completed policy years at the valuation date; 0 for new business.

    **The only thing that moves where the frame starts.**  It is an **elapsed count and so
    already 0-based**: the projection opens at ``t = duration_y``, so an in-force point
    reads the same lapse table, the same § 161 window and the same *Zillmerung* run-off off
    the same clock as a new-business one, with no re-based issue age and no second duration
    variable to keep in step.  It is also the acquisition-cost switch: on an in-force point
    the acquisition cost and the initial commission are **sunk** and are not incurred at
    all, which is why the switch tests ``duration_y = 0`` and not merely ``t = 0``.
    """
    return int(model_point()["duration_y"])


def issue_date():
    """The issue date, for reporting only; the model runs on integer durations."""
    return model_point()["issue_date"]


def cover_end_age():
    """The attained age at which cover ends, ``issue_age + policy_term``.

    **Derived, never carried**, so the term and the end age cannot disagree.  The last
    covered policy year is the one at attained age ``cover_end_age() - 1``.
    """
    return issue_age() + policy_term()


def pols_if_init():
    """The policy count the projection opens with: one policy.

    Every delib model is a scalar single-model-point projection, so this is 1.0 and every
    cash flow in :func:`result_cf` is a per-policy expectation.
    """
    return 1.0


def proj_start():
    """t0: the first projected **month**, ``12 x duration_y``.

    0 for a new-business point and 144 for the in-force model point 8, whose twelve
    completed policy years are now twelve completed *years* of months.  ``result_cf()``
    runs from here to ``proj_len() - 1`` inclusive and contiguously.  ``duration_y`` is an
    elapsed count and already 0-based, so the conversion is a multiplication and not an
    offset.
    """
    return 12 * duration_y()


def proj_len_y():
    """n: the **number of policy years**, equal to ``policy_term``.

    The contract states its own horizon in whole years — the *Versicherungsdauer* — so
    this cells keeps it in years, and everything annual is written against it: the
    first-order equivalence sums over ``range(proj_len_y())``, and :func:`lapse_rate`
    compares ``duration(t)`` with ``proj_len_y() - 1`` to find the final policy year.
    :func:`proj_len` is twelve times this and is the frame.
    """
    return policy_term()


def proj_len():
    """The **number of projected policy months**, ``12 x proj_len_y()``.

    300 on the anchor cell.  It is the frame's **exclusive end**: ``result_cf()`` runs
    over ``range(proj_start(), proj_len())``, so the last index is ``proj_len() - 1`` and
    the frame has ``12 (policy_term - duration_y)`` rows.  Cover ends at the end of the
    last month ``t = proj_len() - 1`` with nothing payable, and ``pols_if(proj_len())`` is
    exactly zero.
    """
    return 12 * proj_len_y()


def duration_mth(t):
    """Completed policy months at the start of month t; equal to ``t``.

    ``t`` is 0-based and counted from **issue** on every model point, the in-force one
    included — its frame opens at ``t = proj_start()`` rather than re-basing the clock —
    so the identity is trivial and the cells exists to name the unit.  It is what the
    premium instalment cycle is counted in, and the vocabulary ``Sofort_DE_S``,
    ``BU_DE_S`` and ``Pflege_DE_S`` already use.
    """
    return t


def duration(t):
    """Completed policy **years** at the start of month t: ``duration_mth(t) // 12``.

    0-based, as ``duration`` is throughout lifelib: 0 through the whole of the first
    policy year.  Every contractual schedule on this product is annual, so this is what
    the attained age, the *Versicherungssumme* schedule, the lapse table, the § 161
    window, the *Beitragszahlungsdauer* and the commission year are keyed on.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y: the contractual **1-based** policy year containing month t; 1 for ``t = 0..11``.

    The label ``duration(t) + 1``, derived from the 0-based ``t`` and never indexed by.
    It exists because three shipped inputs are keyed on a contractual policy year —
    *benefit_schedule.csv*, *nvg_schedule.csv* and *lapse_table.csv* — and those lookups
    map through this cells rather than pass ``t`` raw.
    """
    return duration(t) + 1


def age(t):
    """x(t): the attained age of the first life, ``issue_age + duration(t)``.

    The age steps on the **policy anniversary** — at ``t = 12, 24, ...`` — and not
    monthly: the age basis is *Alter am Jahrestag* and the finer grid does not make it
    finer.  Every rate read at this age is therefore flat across a policy year's twelve
    months.
    """
    return issue_age() + duration(t)


def age2(t):
    """x2(t): the attained age of the second life, ``issue_age2 + duration(t)``.

    Meaningless and unused where ``lives = 1``; :func:`mort_rate_base` never reads it
    there.  Steps on the anniversary, like :func:`age`.
    """
    return issue_age2() + duration(t)


# ==========================================================================
# Mortality: the shipped table, and the two orders built from it


def mort_rate_at_age(sex_code, smoker_code, x):
    """q(x) tilde: the shipped second-order table rate for one life at one attained age.

    A lookup into *mort_table.csv* keyed by ``table_id``, sex, smoker status and attained
    age, and nothing else — no loading, no rating, no combination across lives.  Both
    orders and both lives are built from this one cells, which is what keeps the model's
    unsourced mortality level to a single number.  A **[std]** proxy for DAV 2008 T; see
    the ``Data`` docstring for the anchors a replacement must preserve.
    """
    return float(data.mort_table().at[                               # noqa: F821
        (mort_table_id(), sex_code, smoker_code, int(x)), "mort_rate"])


def mort_rate_base(t):
    """Q(t) tilde: the table rate on the policy's **own** sex, before loading or rating.

    For ``lives = 2`` the two lives are combined **at table level, before any loading**,
    on an independence assumption **[std]**::

        Q = q_A + q_B - q_A q_B

    which is the first-death rate of two independent lives.  Combining *after* loading
    inflates the cross term and is a listed pitfall.  The independence assumption
    understates the true first-death rate for a couple sharing a household, a vehicle and
    a lifestyle, and no German figure bounds the understatement.
    """
    q_a = mort_rate_at_age(sex(), smoker(), age(t))
    if lives() == 1:
        return q_a
    q_b = mort_rate_at_age(sex(), smoker2(), age2(t))
    return q_a + q_b - q_a * q_b


def mort_rate_blend(t):
    """The unisex 50/50 blend of the sex-distinct table rates — the **tariff's** life.

    ``sex_mix_male`` weights the male table and its complement the female one, and for
    ``lives = 2`` the two blends are combined by the same first-death rule as
    :func:`mort_rate_base`, again **before** any loading.  This is what a German tariff is
    priced on, because sex may not enter the premium while the underlying tables remain
    sex-distinct.  The mixing ratio is proprietary at every carrier and the 50/50 here is
    **[std]**.
    """
    w_m = sex_mix_male                                               # noqa: F821
    q_a = (w_m * mort_rate_at_age("M", smoker(), age(t))
           + (1.0 - w_m) * mort_rate_at_age("F", smoker(), age(t)))
    if lives() == 1:
        return q_a
    q_b = (w_m * mort_rate_at_age("M", smoker2(), age2(t))
           + (1.0 - w_m) * mort_rate_at_age("F", smoker2(), age2(t)))
    return q_a + q_b - q_a * q_b


def sel_lapse_factor(t):
    """The selective-lapse loading on persisters' mortality; 1.0 in the base run.

    ``1 + sel_lapse_lambda max(0, lapse_cum(t) - sel_lapse_ref)``.  Healthy lives can
    re-underwrite into a cheaper contract and impaired lives cannot, so the lapsing
    population is healthier than the remaining one and a term book's mortality drifts up
    relative to a table calibrated on the whole cohort.  **delib does not model selective
    lapse in the base run** — ``sel_lapse_lambda = 0``, one basis for stayers and leavers —
    which is a stated simplification rather than a pitfall.  It is driven off
    :func:`lapse_cum`, which is built from the lapse rates alone and never from
    :func:`pols_if`, so switching it on does not make the projection circular.
    """
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, lapse_cum(t) - sel_lapse_ref)                           # noqa: F821


def mort_rate(t):
    """q2(t): the **second-order** annual death rate actually projected.

    ``mort_be_factor x rating_factor x mort_rate_base(t) x sel_lapse_factor(t)`` — the
    policy's own sex and smoker status, rated, first-death where there are two lives, and
    loaded for selective lapse where that module is on.  This drives every decrement and
    every claim, and the *Sicherheitszuschlag* must not appear in it: ``claims_death`` is
    invariant to ``sicherheitszuschlag_m`` while ``prem_gross`` is not, and an
    implementation that projects on ``q1`` overstates claims by a factor of about two.

    ``mort_be_factor`` is 1.00, so the shipped proxy **is** the best estimate and there is
    exactly one unsourced mortality level in the model rather than two stacked on each
    other.  A user with experience data should move this rather than editing the table.

    It is the **annual** rate of the policy year containing month ``t`` — the vector the
    technical notes tabulate — and is flat across that year's twelve months, the attained
    age stepping on the anniversary.  What the projection applies is
    :func:`mort_rate_mth`.
    """
    return (mort_be_factor * rating_factor()                         # noqa: F821
            * mort_rate_base(t) * sel_lapse_factor(t))


def mort_rate_mth(t):
    """q2m(t): the **monthly** death rate applied at the end of month t **[std]**.

    ``1 - (1 - q2(t))^(1/12)``, the constant-force conversion of the policy year's annual
    rate — derived geometrically and **not** by dividing by twelve, so that twelve months
    of it compound back to exactly ``q2(t)``, which is the factor the annual-step model
    applied at the anniversary.  Dividing by twelve instead leaves a second-order gap that
    accumulates over a twenty-five-year term; the geometric form leaves none, and that is
    what makes ``pols_if(12k)`` here reproduce the annual model's ``pols_if(k)``.

    No German instrument states a conversion convention for any decrement, so the choice
    is a standardization; what is not optional is that it reproduce the annual factor.
    Unlike ``frlib.TD_FR_S``, this product has a **single** insured decrement, so there is
    no dependent-rate split to make: the conversion is applied to the one rate.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_rate_tar(t):
    """q1(t): the **first-order** tariff rate, ``(1 + m) x rf x`` the unisex blend.

    It prices the *Bruttobeitrag* and the first-order *Deckungskapital* and enters nothing
    else.  The *Sicherheitszuschlag* ``m = 1.25`` is **[std]**: the DAV *Richtlinie*
    regulates the **procedure** for setting the *Sicherheitszuschläge*, not the level,
    which is not public, and the argued range is 1.0 to 1.5.  It is the single parameter
    that sets the *Brutto* / *Zahlbeitrag* spread — and, because 90 % of the extra margin
    is returned as *Beitragsverrechnung*, the parameter with the widest uncertainty has
    the narrowest effect on the billed premium.

    ``mort_rate_tar(t) / mort_rate(t)`` is **not** ``1 + m``.  It is
    ``(1 + m) x (blend / own-sex rate)``, which on the shipped proxy is 1.6875 for a male
    and 3.375 for a female.  That is the unisex cross-subsidy, and expecting 2.25 for both is a
    listed pitfall.
    """
    return (1.0 + sicherheitszuschlag_m) * rating_factor() * mort_rate_blend(t)  # noqa: F821


# ==========================================================================
# The Versicherungssumme, and the para 161 benefit switch


def benefit_factor(t):
    """f(t): the *Versicherungssumme* schedule factor, from *benefit_schedule.csv*.

    1.0 at every year on ``konstant``; ``(20 - y)/20`` on ``linear_fallend``; and the
    outstanding balance of a thirty-year annuity loan at 3 % on
    ``annuitaet_fallend_3pct``.  The file is keyed on the contractual **1-based**
    ``policy_year``, so the lookup maps through :func:`policy_year` and the factor is
    **flat across a policy year's twelve months**: the *Versicherungssumme* steps on the
    anniversary, which is where the contract steps it, and the monthly grid does not make
    a declining sum insured decline monthly.  The last shape is the *Darlehensabsicherung*
    one and it falls **slowly then fast** — the property a linear schedule gets backwards,
    and the reason a linear sum is a poor match to an annuity loan.  The rate is a
    contractual schedule parameter fixed at issue; it does not follow the borrower's loan
    if that is refinanced, repaid early or rolled onto a new fixed rate.
    """
    return float(data.benefit_schedule().at[                         # noqa: F821
        (benefit_schedule_id(), policy_year(t)), "benefit_factor"])


def sum_uplift_y(y):
    """u(y): the cumulative *Nachversicherungsgarantie* multiplier at **policy year** y.

    From *nvg_schedule.csv*, keyed on the contractual **1-based** ``policy_year``, so the
    lookup is at ``y + 1`` for the 0-based ``y``.  Defined for ``y >= 0`` only: the tranche
    decomposition in :func:`benefit_paid_pp` takes the base cover as its first tranche with
    ``delta u(0) = u(0)`` and never reaches below ``y = 0``.  1.0 throughout on ``keine``,
    the base run.

    The argument is a **policy year and not a month**.  A *Nachversicherungsgarantie*
    increment is granted at a policy anniversary, and its own § 161 window is a whole
    number of years from that anniversary, so the tranche decomposition is an annual
    construction on both counts and stays one on the monthly grid.

    Take-up is exogenous: no event list, cap, exercise window or age limit was established
    from any document, so an increase is supplied as a schedule rather than modelled as a
    decision.  What the model does *with* an increase is not exogenous — see
    :func:`benefit_paid_pp`.
    """
    return float(data.nvg_schedule().at[                             # noqa: F821
        (nvg_schedule_id(), int(y) + 1), "sum_uplift"])


def sum_uplift(t):
    """u(t): the cumulative *Nachversicherungsgarantie* multiplier in month t.

    ``sum_uplift_y(duration(t))`` — the policy year's multiplier, flat across its twelve
    months.  The month-indexed face of :func:`sum_uplift_y`, so that :func:`benefit_pp`
    and :func:`result_pols` read one clock.
    """
    return sum_uplift_y(duration(t))


def benefit_pp(t):
    """B(t): the *Versicherungssumme* in force in period t, ``S0 f(t) u(t)``.

    The **contractual** sum.  What a death claim actually pays is
    :func:`benefit_paid_pp`, which is smaller inside a § 161 window.  Note what does *not*
    enter here: ``rating_factor`` is a mortality loading, not a benefit uplift, and a
    model that lets it scale the sum insured has confused a price with a promise.
    """
    return sum_assured() * benefit_factor(t) * sum_uplift(t)


def benefit_paid_pp(t):
    """What a death claim in period t actually pays, after the § 161 switch.

    § 161 VVG makes the insurer *leistungsfrei* where the *versicherte Person*
    intentionally takes her own life **within three years of conclusion**, unless the act
    was committed in a state excluding free determination of the will caused by a
    *krankhafte Störung der Geistestätigkeit*; the period may be extended by agreement;
    and where *leistungsfrei* the insurer must nevertheless pay the *Rückkaufswert* — which
    on this product is **nil**.  So on a term contract the rule is an exclusion in all but
    name, and the model carries it as a **benefit switch**, never as a decrement
    adjustment.

    The switch runs **tranche by tranche**, and it runs on **policy years**.  The base
    cover's window runs from issue; a *Nachversicherungsgarantie* increment granted at the
    anniversary opening policy year ``s`` carries **its own** window
    ``s <= duration(t) < s + suicide_years`` [unverified — German AVB practice is
    understood to restart the clock for the increment, and no statutory treatment was
    established].  With ``delta u(s) = u(s) - u(s - 1)`` for ``s > 0`` and
    ``delta u(0) = u(0)``::

        benefit_paid_pp(t) = S0 f(t) sum_s delta u(s) sigma_s(t)
        sigma_s(t) = 1 - suicide_share  if duration(t) < s + suicide_years, else 1

    Both clocks are annual and both boundaries therefore fall on an anniversary, so the
    monthly grid resolves the switch exactly rather than approximately: § 161's three
    years from conclusion are months 0 to 35, and ``duration(t) < 3`` is the same
    statement as ``t < 36``.  The comparison is left in years because that is the unit
    the statute and the *Bedingungen* use.

    On an in-force point with ``duration_y >= 3`` and no increments the switch is inert at
    every projected ``t``, which is model point 8.  ``suicide_share = 0.03`` is **[std]**
    with an argued range of 0.01 to 0.05: no German cause-of-death share was retrieved.
    It carries three times the weight of the French one-year factor simply because the
    German window is three times as long.
    """
    total = 0.0
    for s in range(duration(t) + 1):
        delta = sum_uplift_y(s) - (sum_uplift_y(s - 1) if s > 0 else 0.0)
        if delta == 0.0:
            continue
        sigma = ((1.0 - suicide_share)                               # noqa: F821
                 if duration(t) < s + suicide_years else 1.0)        # noqa: F821
        total += delta * sigma
    return sum_assured() * benefit_factor(t) * total


def suicide_factor(t):
    """sigma(t): the § 161 switch as a ratio, ``benefit_paid_pp(t) / benefit_pp(t)``.

    Exactly ``1 - suicide_share`` while the only tranche in force is inside its window,
    exactly 1 once every tranche is out of one, and **strictly between the two** in a year
    when one tranche is inside its window and another is not — which is what the tranche
    decomposition buys and what a single policy-level flag would get wrong.  Defined as
    the ratio rather than the other way round, so the weighting across tranches is done
    once, in euros, where it belongs.
    """
    b = benefit_pp(t)
    if b == 0.0:
        return 1.0
    return benefit_paid_pp(t) / b


# ==========================================================================
# Lapse


def lapse_rate_base(t):
    """The table lapse rate for period t, from *lapse_table.csv*.

    6 % in policy year 1, 4 % in policy years 2 and 3, 3 % thereafter, all **[std]**.  The
    file is keyed on the contractual **1-based** ``policy_year``, so the lookup maps
    through :func:`policy_year` — months ``t = 0 ... 11`` read the file's policy year 1.
    An **annual** rate, and one the table publishes for the final policy year too;
    :func:`lapse_rate` is where the zero goes and :func:`lapse_rate_mth` is where the
    spreading happens.
    """
    return float(data.lapse_table().at[                              # noqa: F821
        policy_year(t), "lapse_rate"])


def shock_lapse_factor(t):
    """M_shock(t): the premium-shock lapse multiplier; 1.0 in the base run.

    ``1 + shock_lapse_lambda max(0, prem_paid_pp(t)/prem_paid_pp(t-12) - 1)``, and 1.0
    through the whole of policy year 1, which has no preceding bill to compare with.  The
    product's distinctive behavioural risk is that the insurer can raise the customer's
    bill without changing a guaranteed term, simply by cutting the *Beitragsverrechnung*:
    no § 163 procedure, no *Treuhänder* and no policyholder remedy, because no guaranteed
    term has moved.  The module is inert in the base run because the billed premium is
    level there — it bites exactly when ``decl_scale`` is stressed, which is when it
    should.  Depends on the premium and never on ``pols_if``, so it does not make the
    projection circular.

    The ratio is between **consecutive renewals** and so reads the annual *Zahlbeitrag*
    twelve months back, not one.  :func:`prem_paid_pp` is the year's whole billed premium
    rather than the instalment, so the comparison is between two annual bills under every
    *Zahlweise*; comparing consecutive **instalments** would make the module fire on the
    *Zahlweise* rather than on the declaration, and on an annual payer it would divide by
    a zero bill in eleven months of twelve.
    """
    if shock_lapse_lambda == 0.0 or duration(t) <= 0:                # noqa: F821
        return 1.0
    prev = prem_paid_pp(t - 12)
    if prev <= 0.0:
        return 1.0
    return 1.0 + shock_lapse_lambda * max(                           # noqa: F821
        0.0, prem_paid_pp(t) / prev - 1.0)


def lapse_rate(t):
    """w(t): the lapse rate applied at the end of period t.

    The table rate times the premium-shock multiplier, and **exactly 0 through the whole
    of the final policy year**, ``duration(t) >= proj_len_y() - 1`` — months 288 to 299 on
    the anchor cell.  The end of that year is the moment cover expires, so a lapse and an
    expiry are then the same event paying the same nothing, and the whole surviving cohort
    is booked through :func:`pols_maturity` instead.  The zero covers the **year** and not
    merely its last month, because that is what the annual-step model this replaced said
    of it: zeroing only month 299 would leave eleven months of 3 % lapse inside the final
    year and move the expiring cohort away from the notes' own figure.

    No cash flow moves either way — the convention only decides how the closure identity
    divides between lapses and expiries — but it is load-bearing for that identity, and
    putting it here rather than in the table keeps the assumption and the convention
    readable apart.  This is the **annual** rate; :func:`lapse_rate_mth` is what is
    applied.
    """
    if duration(t) >= proj_len_y() - 1:
        return 0.0
    return lapse_rate_base(t) * shock_lapse_factor(t)


def lapse_rate_mth(t):
    """wm(t): the lapse rate applied at the **end** of month t, after the death decrement.

    ``1 - (1 - w(t))^(1/12)`` on the policy year's annual rate **[std]**, derived
    geometrically and not by dividing by twelve, so that twelve months of it compound back
    to exactly that rate.  No month is excepted: the one rate this product puts on a
    boundary — the zero of the final policy year — is a rate for a whole year rather than
    for a month of it, so it converts to a monthly zero for each of that year's twelve
    months and needs no special case here.

    § 168 VVG makes the *Versicherungsperiode* follow the *Zahlweise*, so a
    monthly-paying contract is terminable monthly and its exits are genuinely **not**
    concentrated at anniversaries.  The annual grid this model ran on booked them there
    and said so as an approximation; the monthly grid removes it.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_cum(t):
    """w_cum(t): the cumulative lapse proportion entering period t.

    ``1 - prod (1 - wm(s))`` over the projected **months** before ``t``.  A proportion of
    the original cohort on a **lapse-only** basis, not a running total of
    :func:`pols_lapse` and not read off :func:`pols_if`: it feeds
    :func:`sel_lapse_factor`, which loads *mortality*, so building it from the in-force
    count would close a loop between the two decrements.  Zero at ``t = proj_start()``.

    Built on the **monthly** rate, so that at every anniversary it equals the annual-step
    model's own figure exactly — twelve months of ``wm`` compounding back to the year's
    ``w`` — while inside a policy year it now advances month by month instead of jumping
    at the anniversary.
    """
    if t <= proj_start():
        return 0.0
    surv = 1.0
    for s in range(proj_start(), t):
        surv *= (1.0 - lapse_rate_mth(s))
    return 1.0 - surv


# ==========================================================================
# Pricing: the Bruttobeitrag by first-order equivalence, struck once at issue


def disc_factor(y):
    """v^y: the *Rechnungszins* discount factor to the start of **policy year** y, 0-based.

    ``rechnungszins`` is the *Höchstrechnungszins* for new business from 1 January 2025,
    **1,00 %**, raised from 0,25 % and the first increase since 1994.  It appears **only**
    in the premium equivalence and in the first-order *Deckungskapital*.  **Nothing in
    this library discounts a published cash flow**, and on this product the rate barely
    matters in any event — the reserve is small and short-lived, which is a genuine
    difference from every other delib model.

    The argument is a **policy year and not a month**.  The first-order equivalence is an
    annual construction — a *Höchstrechnungszins* is an annual rate and the *Bruttobeitrag*
    it strikes is an annual amount — so it stays one on the monthly grid.  Re-striking it
    month by month would move ``G`` and with it every figure the notes publish, while
    changing nothing about the contract.
    """
    return (1.0 + rechnungszins) ** -y                               # noqa: F821


def pols_tariff(y):
    """p1(y): tariff survivorship entering **policy year** y — **mortality only**.

    ``p1(0) = 1`` and ``p1(y+1) = p1(y)(1 - q1(y))`` on the first-order **annual** rate,
    read at that policy year's opening month ``12 y``.  Lapse is **not** a German
    first-order basis element: the bases are mortality, interest and expenses, and a
    *Stornowahrscheinlichkeit* is a second-order quantity used for projection and
    profit-testing, not for the tariff.  Striking the premium on this survivorship is also
    what keeps the model acyclic — a pricing quantity cannot depend on a behavioural
    assumption that depends on the path that depends on the premium.

    A policy-year recursion and not a monthly one, for the same reason
    :func:`disc_factor` is: it is the tariff basis of an annual equivalence.  It always
    starts at issue, at ``y = 0``, even on an in-force model point whose projection opens
    later: the tariff was struck when the contract was written.
    """
    if y <= 0:
        return 1.0
    return pols_tariff(y - 1) * (1.0 - mort_rate_tar(12 * (y - 1)))


def tariff_annuity():
    """ae: the premium annuity-due over the paying term, ``sum v^y p1(y)``.

    ``y = 0 .. prem_term() - 1``, the *Beitragszahlungsdauer* being stated in whole years.
    Equal to 1 where ``prem_term = 1``, which is why the ``einmal`` form falls out of the
    same equivalence rather than needing its own.
    """
    return sum(disc_factor(y) * pols_tariff(y)
               for y in range(prem_term()))


def tariff_claims_pv():
    """A: the actuarial present value of the death benefits, on first-order bases.

    ``sum v^(y+1) p1(y) q1(y) B(y)`` over the whole cover period, ``y = 0 .. n - 1``,
    benefits paid at the end of the **policy year** of death and the annual rate and sum
    insured read at that year's opening month ``12 y``.  It is the quantity the whole
    product turns on: the *Bruttobeitrag* is built from it and the
    *Beitragsverrechnungssatz* returns ``surplus_share`` of ``m/(1+m)`` of it.

    The end-of-year benefit timing here is the **tariff's** convention and is not the
    projection's: the cash flow statement pays a death claim at the end of the month of
    death.  A first-order equivalence is a pricing calculation on a prudent annual basis,
    and moving it to the month would change the guaranteed premium a German contract
    states in its own *Versicherungsschein*.
    """
    return sum(disc_factor(y + 1) * pols_tariff(y)
               * mort_rate_tar(12 * y) * benefit_pp(12 * y)
               for y in range(proj_len_y()))


def tariff_sum_pv():
    """Gamma: the sum-exposure annuity ``sum v^y p1(y) B(y)``, for the gamma loading.

    Runs over the whole **cover** period rather than the paying term, because the
    sum-related administration charge is incurred for as long as there is a sum at risk —
    which is exactly the situation HGB § 341f has in mind when it requires a provision for
    future administration costs on a contract whose premiums stop before its cover does.
    Annual, like the rest of the equivalence.
    """
    return sum(disc_factor(y) * pols_tariff(y) * benefit_pp(12 * y)
               for y in range(proj_len_y()))


def prem_gross_level_pp():
    """G: the level *Bruttobeitrag* per policy, **before** the *Ratenzahlungszuschlag*.

    Struck once, at issue, by first-order equivalence with the alpha loading a per-mille
    of the *Beitragssumme* ``k G`` incurred at issue::

        G ae = A + z k G + beta G ae + gamma Gamma

    which is linear in ``G`` and solves in closed form::

        G = ( A + gamma Gamma ) / ( (1 - beta) ae - z k )

    ``z = 0.025`` is the *Höchstzillmersatz* — 25 permille of the *Beitragssumme*, cut
    from 40 permille by the LVRG with effect from 1 January 2015 — and the composite
    **assumes a term tariff runs at the cap**, which may well be wrong: a slim
    direct-channel acquisition cost would sit far below it.  That is the single **[std]**
    charge most likely to be overstated in this model.  ``beta = 0.05`` and
    ``gamma = 0.00030`` are **[std]** placeholders: German term-life charge levels are
    structurally undisclosed — no *Effektivkostenquote*, because a reduction in yield
    presupposes a yield; no *Basisinformationsblatt*, because the product is not a PRIIP;
    and the *Produktinformationsblatt* quotes premiums, not loadings.

    **This is the guaranteed premium** — the maximum the policyholder can ever be required
    to pay, unchanged for the term.  It is not what is billed.
    """
    denom = (1.0 - beta_tariff) * tariff_annuity() - zillmer_rate * prem_term()  # noqa: F821
    if denom <= 0.0:
        raise ValueError("degenerate premium equivalence: loadings exceed the annuity")
    return (tariff_claims_pv() + gamma_rate * tariff_sum_pv()) / denom  # noqa: F821


def prem_net_level_pp():
    """Gn: the actuarial *Nettoprämie* ``A / ae`` — a pricing quantity, never a cash flow.

    The risk premium on the first-order basis before expense loadings, and the premium the
    reserve recursion in :func:`res_pp_at` is struck on.  **It is not the consumer's
    *Nettobeitrag***, which is the *Zahlbeitrag* and is :func:`prem_paid_pp`, and on this
    calibration it sits **above** it: ``Gn = 1 084.80`` against a billed 733.01, because
    ``Gn`` carries the whole *Sicherheitszuschlag* and 90 % of that is handed back as
    *Beitragsverrechnung*.  Confusing the two is the classic implementation error on this
    product, and it never appears in :func:`result_cf`.
    """
    return tariff_claims_pv() / tariff_annuity()


def beitragsverrechnung_rate():
    """v_d: the declared *Beitragsverrechnungssatz*, struck once at issue.

    **Derived from the surplus mechanic, not assumed.**  The tariff's own mortality margin
    in year ``t`` is ``(q1 - q1/(1+m)) B = (m/(1+m)) q1 B`` per in-force policy, so its
    actuarial value at issue is exactly ``(m/(1+m)) A``.  The declaration returns
    ``surplus_share`` of it over the paying term::

        v_d = min( v_max, decl_scale surplus_share (m/(1+m)) A / (G ae) )

    ``surplus_share = 0.90`` is the **MindZV minimum allocation from the
    *Risikoergebnis***, and modelling the statutory minimum is the conservative choice for
    the billed premium and the only level any instrument fixes — no German carrier
    publishes a declaration for this product.  ``decl_scale = 1.00`` is the stress lever:
    setting it to 0 raises the billed premium to the guaranteed one at every ``t``, with
    no change to any claim, no § 163 procedure, no *Treuhänder* and no policyholder
    remedy.  On the anchor that is a 74 % increase in the bill for no change in cover, and
    it is the product's largest policyholder risk.  ``v_max = 0.95`` binds nowhere in the
    shipped model points; it exists so that an extreme ``m`` cannot drive the billed
    premium negative and so that :func:`check_prem_split` has a stated domain.

    Zero where ``surplus_form = keine``, the § 153-excluded non-participating tariff.
    """
    if surplus_form() == "keine":
        return 0.0
    m = sicherheitszuschlag_m                                        # noqa: F821
    raw = (decl_scale * surplus_share * (m / (1.0 + m))              # noqa: F821
           * tariff_claims_pv()
           / (prem_gross_level_pp() * tariff_annuity()))
    return min(v_max, raw)                                           # noqa: F821


# ==========================================================================
# What is billed


def prem_freq_load():
    """phi: the *Ratenzahlungszuschlag* multiplier for this policy's *Zahlweise*.

    1.000 annual, 1.02 half-yearly, 1.03 quarterly, 1.05 monthly — a German market
    convention with no carrier attribution, carried as **[std]**.  Whether German carriers
    strike it on the *Bruttobeitrag* or the *Zahlbeitrag* was not established; this model
    loads the **billed** amount, which means it multiplies all three of the gross, the
    rebate and the paid premium, so the split identity holds at every frequency.  Applying
    it to each stream separately, or twice, is a listed pitfall.
    """
    return float(data.freq_loading_table().at[                       # noqa: F821
        prem_freq(), "prem_freq_load"])


def instalments():
    """The number of premium instalments a year for this policy's *Zahlweise*.

    1 / 2 / 4 / 12, read from the ``instalments`` column of *freq_loading_table.csv*,
    which ships beside the *Ratenzahlungszuschlag* and names the cycle that surcharge
    exists to price.  On the annual grid this model ran on, the column could not be used
    for anything — the whole loaded annual premium was collected at the anniversary
    whatever the *Zahlweise*, which made the surcharge a charge for a service the model
    never rendered.  On the monthly grid it drives :func:`prem_cycle` and
    :func:`prem_inst_pp`.
    """
    return int(data.freq_loading_table().at[                         # noqa: F821
        prem_freq(), "instalments"])


def prem_cycle():
    """Months between premium instalments: 12 annual, 6 half-yearly, 3 quarterly, 1 monthly.

    ``12 // instalments()`` — arithmetic of the elected *Zahlweise* rather than an
    assumption, so it is written here rather than held in a Reference or a column.
    """
    return 12 // instalments()


def prem_due(t):
    """Whether a premium instalment falls due at the **beginning** of month t.

    ``duration_mth(t) % prem_cycle() == 0``.  An annual payer is due in the first month of
    every policy year and nowhere else; a monthly payer is due in every month.  § 168 VVG
    makes the *Versicherungsperiode* follow the *Zahlweise*, so this cycle is a
    contractual fact and not a modelling convenience — it is the period the contract is
    written in.
    """
    return duration_mth(t) % prem_cycle() == 0


def prem_gross_pp(t):
    """The **annual** *Bruttobeitrag* per in-force policy for month t's policy year, ``G phi``.

    **The guaranteed stream**: the maximum the policyholder can ever be required to pay in
    a policy year.  Zero for ``duration(t) >= prem_term()``, so the *abgekürzte
    Beitragszahlungsdauer* of model point 6 pays its last premium in month 143 while cover
    and claims run on to month 239.  It does **not** enter :func:`net_cf`; it is published
    beside the billed stream because a model carrying one premium cannot represent this
    product.

    An **annual** amount, flat across the policy year: the *Bruttobeitrag* is struck once
    at issue and is level for the term.  What is collected in month ``t`` is
    :func:`prem_gross_inst_pp`, the instalment the elected *Zahlweise* makes due.
    """
    if t < 0 or duration(t) >= prem_term():
        return 0.0
    return prem_gross_level_pp() * prem_freq_load()


def prem_rebate_pp(t):
    """The **annual** *Beitragsverrechnung* per in-force policy, ``v_d G phi``.

    The declared surplus, netted against the *Bruttobeitrag* **before billing** rather
    than credited to an account — which is what § 153 VVG's *verursachungsorientiert*
    allocation looks like on a product with no account to credit.  Zero where
    ``surplus_form = keine`` and zero once the paying term is over.  An annual amount,
    like :func:`prem_gross_pp`; :func:`prem_rebate_inst_pp` is what is netted off each
    instalment.
    """
    if t < 0 or duration(t) >= prem_term():
        return 0.0
    return beitragsverrechnung_rate() * prem_gross_level_pp() * prem_freq_load()


def prem_paid_pp(t):
    """P(t): the **annual** *Zahlbeitrag* per in-force policy — what the customer is billed.

    ``prem_gross_pp(t) - prem_rebate_pp(t)``, formed as the difference so that the split
    identity is true by construction rather than by coincidence.  **Not guaranteed**:
    § 153 VVG confers an entitlement to participate in surplus, not to a level, and a
    reduction of the declaration raises this toward the *Bruttobeitrag* with no procedure
    and no remedy.

    The annual bill, and so the quantity :func:`shock_lapse_factor` compares between
    consecutive renewals.  The stream inside :func:`net_cf` is :func:`prem_inst_pp`,
    collected on the *Zahlweise*'s own cycle.
    """
    return prem_gross_pp(t) - prem_rebate_pp(t)


def prem_gross_inst_pp(t):
    """The *Bruttobeitrag* instalment falling due in month t, or zero.

    ``prem_gross_pp(t) / instalments()`` where :func:`prem_due` makes one due.  The
    instalments of a policy year therefore sum to exactly that year's annual
    *Bruttobeitrag*, the *Ratenzahlungszuschlag* included: ``phi`` is a multiplier on the
    annual amount and dividing the loaded amount into instalments is what the surcharge
    prices.  Loading each instalment again, or dividing and then loading, charges it
    twice.
    """
    return prem_gross_pp(t) / instalments() if prem_due(t) else 0.0


def prem_rebate_inst_pp(t):
    """The *Beitragsverrechnung* netted off the instalment falling due in month t, or zero.

    ``prem_rebate_pp(t) / instalments()`` where one is due.  The declaration is an annual
    one and the rebate an annual amount; what reaches a bill is its share of that bill,
    which is why this divides by the same :func:`instalments` as the gross.
    """
    return prem_rebate_pp(t) / instalments() if prem_due(t) else 0.0


def prem_inst_pp(t):
    """P_inst(t): the *Zahlbeitrag* instalment actually collected per policy in month t.

    ``prem_gross_inst_pp(t) - prem_rebate_inst_pp(t)``, formed as the difference so that
    the split identity holds instalment by instalment as well as year by year.  An annual
    payer therefore collects the whole 733,01 € of the anchor cell in the first month of
    each policy year and nothing in the other eleven; model point 4 is the contrast,
    twelve instalments on a *monatlich* *Zahlweise*.

    **This is the one place the finer grid changes an answer rather than its resolution.**
    On a fractionated point the instalments after the first are collected on a block that
    has already lost lives, so the premium-cessation rule finally bites where an annual
    grid could not express it — and the *Ratenzahlungszuschlag* is at last charging for
    something the model does.
    """
    return prem_gross_inst_pp(t) - prem_rebate_inst_pp(t)


# ==========================================================================
# The first-order Deckungskapital — a pricing diagnostic, not a provision


def res_pp_at(y, timing):
    """The first-order **net** *Deckungskapital* per policy at **policy year** y, prospectively.

    ``"BEF_PREM"``
        before the year's premium: ``sum_{u>=y} v^(u-y+1) (p1(u)/p1(y)) q1(u) B(u)``
        over ``u = y .. n - 1``, less ``Gn sum_{u=y..k-1} v^(u-y) (p1(u)/p1(y))``.

    ``"AFT_PREM"``
        the same plus ``Gn`` where a premium is due in policy year ``y``.

    The argument is a **policy year and not a month**, like the equivalence it belongs to:
    a first-order *Deckungskapital* is struck on the tariff's annual bases, and the annual
    Thiele recursion :func:`check_res_roll_fwd_resid` asserts is the statement the German
    literature makes of it.  A monthly reserve would be a different quantity built on a
    monthly *Rechnungszins* this contract does not have.  :func:`result_pols` publishes it
    against the policy year of each month, so it is flat across that year's twelve rows.

    Zero at ``y = 0`` by the equivalence, zero at ``y = n`` by exhaustion, and strictly
    positive in between — on the anchor cell it peaks at 7 553,29 €, 2,5 % of the sum
    insured, at ``y = 15``.  **That it exists at all is the point.**  An RLV has no
    *Sparanteil* in the endowment's sense, but a level premium charged against a rising
    death rate necessarily overcharges early and undercharges late, and the difference has
    to be held.  Concluding "no *Sparanteil*, therefore no reserve" is wrong, and a model
    built on it fails :func:`check_res_roll_fwd`.

    **It is a pricing diagnostic and not a balance-sheet provision.**  It is net, it is not
    *gezillmert*, it is not floored at zero, it enters no cash flow, and nothing in this
    library discounts a published cash flow.  The statutory *Deckungsrückstellung* of
    HGB § 341f, the *Zinszusatzreserve* and the Solvency II best estimate are cited in the
    technical notes and computed nowhere.
    """
    if timing == "AFT_PREM":
        return res_pp_at(y, "BEF_PREM") + (prem_net_level_pp() if y < prem_term() else 0.0)
    if timing != "BEF_PREM":
        raise ValueError("invalid timing")
    if y >= proj_len_y():
        return 0.0
    p_y = pols_tariff(y)
    claims_pv = sum(
        disc_factor(u - y + 1) * (pols_tariff(u) / p_y)
        * mort_rate_tar(12 * u) * benefit_pp(12 * u)
        for u in range(y, proj_len_y()))
    prem_pv = prem_net_level_pp() * sum(
        disc_factor(u - y) * (pols_tariff(u) / p_y)
        for u in range(y, prem_term()))
    return claims_pv - prem_pv


def res_zill_pp_at(y, timing):
    """The *gezillmerte* companion of :func:`res_pp_at`: less the unamortised Zillmer balance.

    ``res_pp_at(y, timing) - z k G x [ sum_{u=y..k-1} v^(u-y) (p1(u)/p1(y)) ] / ae``, so it
    is exactly ``-z k G`` at ``y = 0`` — **negative from the first day** — and back to zero
    at expiry.  That is what *Zillmerung* looks like on a contract with almost no reserve:
    the cap is 25 permille of the *Beitragssumme*, which for a twenty-five-year contract is
    twenty-five times the annual premium and therefore large relative to a reserve that
    peaks at a low single-digit percentage of the sum insured.  A **policy-year** quantity,
    like the reserve it adjusts.

    Whether a negative individual reserve must be floored at zero for balance-sheet
    purposes — the *Nullstellung* question — was **not established**, and because this
    model publishes no balance-sheet reserve the question does not reach its cash flows.
    """
    p_y = pols_tariff(y) if y < proj_len_y() else 1.0
    remaining = sum(disc_factor(u - y) * (pols_tariff(u) / p_y)
                    for u in range(max(y, 0), prem_term()))
    zill = (zillmer_rate * prem_term() * prem_gross_level_pp()       # noqa: F821
            * remaining / tariff_annuity())
    return res_pp_at(y, timing) - zill


# ==========================================================================
# Decrements


def pols_if(t):
    """l(t): policies in force at the **start** of month t.

    ``pols_if_init()`` at ``t = proj_start()``, then
    ``l(t+1) = l(t) - pols_death(t) - pols_lapse(t) - pols_maturity(t)`` on the **monthly**
    rates, which is ``l(t)(1 - q2m(t))(1 - wm(t))`` everywhere but the last month.  This is
    the weight on every cash flow of the same :func:`result_cf` row — a start-of-period
    exposure under a start-of-period name, which is the library-wide ruling and is
    asserted by the conventions suite because breaking it is silent.

    Because both monthly rates compound back to their policy year's annual rate, twelve
    months of this recursion collapse to ``l(t+12) = l(t)(1 - q2(t))(1 - w(t))`` — the
    annual-step recursion this replaced, term for term — so the in-force **at every policy
    anniversary** is the annual model's own figure, ``pols_if(12k)`` here equalling
    ``pols_if(k)`` there to floating point.  What the finer grid adds is the eleven months
    between them.

    ``pols_if(proj_len())`` is defined and is **exactly zero**: it is the state one step
    past the last projected month, the expiring cohort having left through
    :func:`pols_maturity` in that month, so every exit lands inside the frame and there is
    no tail state.  Zero outside the projected range.
    """
    if t < proj_start() or t > proj_len():
        return 0.0
    if t == proj_start():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside period t.

    ``"BEF_DECR"``
        l(t), the start of the period, before any decrement — the same number as
        :func:`pols_if` and the weight on that period's cash flows.

    ``"BEF_LAPSE"``
        after the death decrement, before lapses.  The processing order takes deaths at
        the end of the **month** and lapses **after** them, so this is the population
        lapses are taken from.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state, after deaths, lapses and — in the final month —
        the expiry, which is why it is exactly zero at ``t = proj_len() - 1``.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_DECR":
        if t < proj_start() or t >= proj_len():
            return 0.0
        return (pols_if(t) - pols_death(t) - pols_lapse(t) - pols_maturity(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q2m(t): expected deaths in month t, claimed at the end of the month.

    On the **monthly** death rate, so a claim now falls in the month it happens rather
    than at the anniversary.  The claimant has already paid whatever instalment fell due
    in advance at the start of that month; that is this model's reading of "premium
    payment ceases at death" **[std]**, and multiplying :func:`premiums` by ``(1 - q2m)``
    on top of it applies the rule twice.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Lapses at the end of period t, taken from the survivors of the death decrement.

    ``l(t)(1 - q2m(t)) wm(t)``.  Pays **nothing**: there is no *Rückkaufswert*, so this
    moves :func:`pols_if` and nothing else, and at most an unearned fraction of a prepaid
    instalment — not modelled, and smaller on a fractionated *Zahlweise* than on an annual
    one — would be returned in practice.  Zero through the whole final policy year, where
    the survivors leave as an expiry instead.

    The economic reason lapse matters on a product with no surrender value to forfeit is
    on the **other** side of the ledger: acquisition cost is incurred at issue and
    recovered over the term, so an early lapse is a loss to the insurer.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_maturity(t):
    """The expiring survivors, at the **last projected month** ``t = proj_len() - 1``.

    ``l(proj_len()-1)(1 - q2m(proj_len()-1))``, and zero in every month before it: the
    *Versicherungsdauer* runs to the end of the last month of the last policy year, and
    that is the single instant cover ceases.  Lapse is already zero through the whole of
    that policy year, so the survivors of the twelve months' mortality all leave here.

    Cover simply ends.  **Nothing is paid** — there is no *Erlebensfallleistung*, no
    maturity value and no return of premium — so ``claims(t, "MATURITY")`` is zero and the
    count is published only because the closure identity needs it.  The name is the
    library's: ``pols_maturity`` is the count whose cover ends at the scheduled end of the
    contract, whether or not anything is paid for it, and ``pols_expiry`` is retired.
    """
    if t != proj_len() - 1:
        return 0.0
    return pols_if(t) * (1.0 - mort_rate_mth(t))


# ==========================================================================
# Cash flows


def premiums(t):
    """*Zahlbeitrag* income at the **beginning** of month t, an inflow.

    ``prem_inst_pp(t) l(t)``: the instalment the elected *Zahlweise* makes due this month,
    weighted by the in-force entering it.  **The billed stream, and the one inside**
    :func:`net_cf`.  An annual payer contributes the whole year's *Zahlbeitrag* in the
    first month of the policy year and nothing in the other eleven; a monthly payer
    contributes a twelfth each month on a block that has already lost lives, which is
    where § 168's *Versicherungsperiode* finally bites.

    Not further multiplied by ``(1 - q2m)``: claims fall at the end of the month, so a
    claimant has already paid that month's instalment, and applying the premium-cessation
    rule again here charges it twice.
    """
    return prem_inst_pp(t) * pols_if(t)


def prem_gross(t):
    """*Bruttobeitrag* instalments on the in-force cohort — the **guaranteed** stream.

    ``prem_gross_inst_pp(t) l(t)``.  Published beside :func:`premiums` and **not** part of
    :func:`net_cf`.  It is what the contract guarantees the insurer may charge, so it is
    also the ``decl_scale = 0`` stress: the whole distance between the two columns is
    surplus the insurer may withdraw by declaration alone.
    """
    return prem_gross_inst_pp(t) * pols_if(t)


def prem_rebate(t):
    """The *Beitragsverrechnung* on the in-force cohort, ``prem_rebate_inst_pp(t) l(t)``.

    The contract-level consequence of the MindZV allocation, not the allocation itself:
    the statutory minimum binds on the HGB accounts and is a transfer to the *Rückstellung
    für Beitragsrückerstattung*, and what reaches one policy is this.  It is the middle
    term of ``prem_gross = premiums + prem_rebate``, which :func:`check_prem_split`
    asserts at every ``t`` and every *Zahlweise* — instalment by instalment now, and so in
    every month rather than only at the anniversary.
    """
    return prem_rebate_inst_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in period t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the *Todesfallleistung* at the end of the period of death,
        ``benefit_paid_pp(t) x pols_death(t)`` — the sum insured after the § 161 switch.
        The only kind that is ever non-zero.

    ``"LAPSE"``
        **zero, always.**  § 169 Abs. 1 VVG confines the surrender-value duty to a life
        insurance whose insured event is certain to occur and a term assurance's is not,
        and § 165's *Beitragsfreistellung* and § 166's paid-up conversion both collapse
        into the same nil through the minimum-benefit test.  The kind exists so that the
        zero is stated rather than inferred.

    ``"MATURITY"``
        **zero, always.**  A term contract pays nothing at expiry: no
        *Erlebensfallleistung*, no maturity value, no return of premium.  The
        *Risikolebensversicherung mit Beitragsrückgewähr*, which does return premiums on
        survival, has a savings element by construction and is a different product.

    Both zeros are published as columns rather than dropped, and
    :func:`check_no_cash_value` asserts them on every model point: a reader arriving from
    a model with cash surrender values will wire one in, and every total in the frame will
    still look plausible.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "MATURITY"))
    if kind == "DEATH":
        return benefit_paid_pp(t) * pols_death(t)
    if kind == "LAPSE":
        return 0.0
    if kind == "MATURITY":
        return 0.0
    raise ValueError("invalid kind")


def acq_cost_pp():
    """The total acquisition cost per policy, ``z k G`` — incurred **once, at issue**.

    25 permille of the *Beitragssumme*, the *Höchstzillmersatz* ceiling, of which
    ``comm_init_pp()`` is the initial *Abschlussprovision* and the remainder is other
    acquisition cost.  **A year-one outgo, not an annualised loading**: the tariff
    amortises it through the equivalence, the cash flow incurs it at issue, and that gap
    is the economic reason an early lapse hurts on a product with no surrender value to
    forfeit.  On an **in-force** model point it is sunk and is not incurred at all.
    """
    return zillmer_rate * prem_term() * prem_gross_level_pp()        # noqa: F821


def comm_init_pp():
    """The initial *Abschlussprovision* per policy, ``c0 k G``: 20 permille of the *Beitragssumme*.

    Published apart from the rest of the acquisition cost because :func:`result_cf` prints
    commission as its own column, and because the commission is the part that differs most
    between the German distribution channels — the direct writers' spread is wide precisely
    because no *Abschlussprovision* is paid to an intermediary, leaving more of the
    *Bruttobeitrag* available for *Beitragsverrechnung*.  **[std]**: no German scale is
    public.
    """
    return comm_rate_init * prem_term() * prem_gross_level_pp()      # noqa: F821


def inflation_factor(t):
    """(1 + pi)^duration(t): expense inflation on the sum-related admin charge only.

    2,0 % a year **[std]**, stepping on the **policy anniversary** and flat across a
    policy year's twelve months — the form ``Sofort_DE_S`` already uses in this library,
    and arithmetically the same sequence the annual-step model published, re-indexed.
    (``FRV_DE_S`` and ``Pflege_DE_S`` inflate continuously at ``(1 + pi)^(t/12)`` instead;
    the difference is second-order and the anniversary form is what keeps a policy year's
    charge equal to the annual model's.)  Applied from issue rather than from the start of
    the projection, so an in-force point carries the inflation its duration has already
    accrued.  **The tariff's own gamma is level**, so the cost result narrows over a long
    term and eventually reverses — a real feature of a twenty-five-year contract, and the
    reason model point 14's forty-year run is worth its place.
    """
    return (1.0 + expense_infl) ** duration(t)                       # noqa: F821


def maint_pp(t):
    """Maintenance expense per in-force policy at the beginning of month t.

    ``gamma B(t) (1 + pi)^duration(t) / 12`` — sum-related administration, 0,30 permille
    of the sum insured a year and therefore **one twelfth of it a month**, expressed
    sum-related so it scales across the model point table — plus
    ``a x prem_inst_pp(t)``, collection cost at 3,0 % of the instalment **actually
    collected** in the month.  Both **[std]**; no German level is public.

    The two halves move differently on a monthly grid and both moves are the point.  The
    administration charge accrues a twelfth a month, so a policy that runs a full year
    carries the same annual charge as it did — but it is now borne by the in-force of
    **each month** rather than of the anniversary, which is what makes a decrementing
    block cost less.  The collection cost follows the *Zahlweise*: it is charged when a
    bill is collected, which on an annual payer is once a year and on a *monatlich* one is
    twelve times, and that is what a collection cost is.

    The tariff loads 5,0 % of each *Bruttobeitrag* against a modelled collection cost of
    3,0 % of the *Zahlbeitrag*, and the gap is the ***Kostenüberschuss***.  The model does
    **not** return it: splitting the MindZV's *übriges Ergebnis* limb, whose minimum share
    is different, has no basis in the research corpus, so the cost result emerges in
    :func:`net_cf` and stays there.  That is a stated simplification — ``prem_rebate`` is
    invariant to ``maint_prem_pct`` and ``comm_rate_renew`` while ``net_cf`` is not — and
    not an oversight.
    """
    return (gamma_rate * benefit_pp(t) * inflation_factor(t) / 12.0  # noqa: F821
            + maint_prem_pct * prem_inst_pp(t))                      # noqa: F821


def expenses(t):
    """Total expense outgo in month t, **excluding** commission.

    Acquisition cost net of the initial commission in month ``t = 0`` and only where
    ``duration_y = 0`` — a single amount at issue, not an annualised loading and not a
    twelfth of one; maintenance and collection on the opening in-force; and the claim
    expense on the month's deaths, 250 € each **[std]**.

    Commission is **not** in here.  It is :func:`commissions`, its own column, and
    :func:`net_cf` subtracts the two separately — the opposite convention from
    ``frlib.TD_FR_S``, whose notes fold commission into the expense total.  The two
    libraries' columns look alike and do not mean the same thing, so the identity is
    written down in :func:`check_net_cf` rather than left to a reader's assumption.
    """
    acq = (acq_cost_pp() - comm_init_pp()) if (t == 0 and duration_y() == 0) else 0.0
    return (acq + maint_pp(t) * pols_if(t)
            + claim_expense * pols_death(t))                        # noqa: F821


def commissions(t):
    """Commission outgo in month t.

    The initial *Abschlussprovision* at issue — in month ``t = 0`` and only where
    ``duration_y = 0``, because on an in-force point it is sunk — plus the
    *Bestandspflegeprovision* at 1,0 % of each *Zahlbeitrag* instalment from
    ``duration(t) >= 1``, which is policy year 2.  Both **[std]**.

    The **rate** is a policy-year rate and steps on the anniversary; the **base** is the
    instalment actually collected, so a fractionated payer earns the renewal commission in
    instalments too.  On an annual-mode point that reproduces the annual model's
    commission exactly, both the rate and the collection sitting on the anniversary.
    """
    init = comm_init_pp() if (t == 0 and duration_y() == 0) else 0.0
    renew = (comm_rate_renew * prem_inst_pp(t) * pols_if(t)          # noqa: F821
             if duration(t) >= 1 else 0.0)
    return init + renew


def net_cf(t):
    """Net liability cash flow in period t, **income positive**.

    ``premiums(t) - claims(t) - expenses(t) - commissions(t)`` — the *billed* premium, not
    the guaranteed one.  This is the library-wide sign, so ``result_cf()["net_cf"]`` can be
    compared and summed across delib without checking which product it came from; the
    outgo-positive orientation is :func:`liability_cf`.

    Undiscounted, and deliberately so: this library publishes gross best-estimate-style
    liability cash flows and leaves discounting, the *Deckungsrückstellung*, Solvency II
    technical provisions and the SCR to a layer that consumes them.
    """
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def liability_cf(t):
    """The same stream, outgo positive: ``-net_cf(t)`` exactly.

    Published so that a best-estimate liability is ``sum v(t) liability_cf(t)`` over
    whatever discount curve the valuation layer supplies, without a sign flip a reader has
    to remember.  Both orientations are columns of :func:`result_cf`, so the identity is
    verifiable in the frame.
    """
    return -net_cf(t)


# ==========================================================================
# The published check_* identities


def check_net_cf_resid(t):
    """The cash-flow-statement residual in month t; zero everywhere.

    ``net_cf`` **as published in** :func:`result_cf`, less that same frame's own

        ``premiums - claims_death - claims_lapse - claims_maturity - expenses
        - commissions``

    — read from the frame rather than from the cells behind it, and reached by a different
    route from :func:`net_cf`'s own, which subtracts the kind-less ``claims(t)`` subtotal.
    So the identity crosses two boundaries rather than restating a formula: the
    cells-to-frame boundary, where a column can be dropped, renamed or mis-signed on the
    way in, and the ``claims(t, kind)`` dispatch, where a benefit kind can exist in the
    model and not in the subtotal.

    This is **delib's first ruling**: every model in the library reconstructs its headline
    number from its own published parts, in code and not only in prose, so that the one
    quantity a cash flow model exists to produce is not the one quantity nothing checks.
    What it catches on *this* product is the ambiguity the second premium stream creates —
    ``prem_gross`` is published beside ``premiums`` and must **not** enter the identity,
    and ``prem_rebate`` is the difference between them and must not be subtracted a second
    time — and the commission convention, which is a column of its own here and part of
    the expense total in ``frlib.TD_FR_S``.
    """
    row = result_cf().loc[t]
    rebuilt = (row["premiums"] - row["claims_death"] - row["claims_lapse"]
               - row["claims_maturity"] - row["expenses"] - row["commissions"])
    return float(row["net_cf"] - rebuilt)


def check_net_cf():
    """True when the cash flow statement reconciles in every projected period.

    No argument, one bool over all ``t``, the library-wide shape;
    :func:`check_net_cf_resid` gives the signed residual of the period that failed.  The
    tolerance scales with the sum insured, which is the largest number in the statement.
    """
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(proj_start(), proj_len()))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - pols_death(t) - pols_lapse(t) - pols_maturity(t)``.
    What it catches is a **misindexed recursion**: rolling forward with ``wm(t-1)`` or
    ``q2m(t+1)``, or leaving the expiry out of the roll-forward while still booking it as
    an exit.  In the last month ``pols_lapse`` is zero, ``pols_maturity`` carries the
    whole surviving cohort and ``pols_if(proj_len())`` is exactly zero, so the identity
    closes there too — and that it closes at ``proj_len() - 1`` with nothing left over is
    what lets :func:`result_cf` stop there.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected period.

    It also asserts the **closure identity** at the horizon: the three exits summed over
    the whole projection equal ``pols_if_init()``, so every policy the projection opens
    with leaves it through exactly one named door.  On the anchor cell that is
    0,03305608 deaths, 0,53554078 lapses and 0,43140314 expiries.
    """
    tol = roll_fwd_tol * max(pols_if_init(), 1.0)                    # noqa: F821
    if not all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_start(), proj_len())):
        return False
    exits = sum(pols_death(t) + pols_lapse(t) + pols_maturity(t)
                for t in range(proj_start(), proj_len()))
    return abs(exits - pols_if_init()) <= tol


def check_prem_split_resid(t):
    """The premium-split residual in month t: ``Brutto - Zahl - Verrechnung``; zero.

    **The product's signature identity.**  The German term premium is two numbers and a
    difference — a guaranteed *Bruttobeitrag*, a billed *Zahlbeitrag* and the declared
    *Beitragsverrechnung* between them — and every consumer document, every comparison
    test and every rating criterion turns on the gap.  The residual is zero by
    construction, :func:`prem_inst_pp` being formed as the difference; what
    :func:`check_prem_split` adds on top is the **domain**, which is not.

    Struck on the **instalments**, which is what the cash flow statement publishes: an
    identity asserted on the annual amounts alone would not see a *Zahlweise* that
    fractionates the gross and the rebate on different cycles.
    """
    return (prem_gross_inst_pp(t) - prem_inst_pp(t)
            - prem_rebate_inst_pp(t))


def check_prem_split():
    """True when the premium splits, and stays inside its domain, at every ``t``.

    Beyond the residual: in a month where an instalment is due inside the paying term the
    rebate must be non-negative and strictly below the gross instalment — a
    *Beitragsverrechnung* that reached the whole premium would make the contract free,
    which ``v_max`` exists to prevent — and in every other month all three instalments
    must be exactly zero, which is what stops a model running the premium past the
    *Beitragszahlungsdauer* on model point 6 or collecting outside the *Zahlweise*'s own
    cycle.  The annual amounts must close the same way, so both are asserted.

    The identity holds at every *Zahlweise*, because the *Ratenzahlungszuschlag*
    multiplies the annual billed amount once and the division into instalments is applied
    to all three terms alike.
    """
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    for t in range(proj_start(), proj_len()):
        if abs(check_prem_split_resid(t)) > tol:
            return False
        if abs(prem_gross_pp(t) - prem_paid_pp(t) - prem_rebate_pp(t)) > tol:
            return False
        if duration(t) < prem_term() and prem_due(t):
            if not (0.0 <= prem_rebate_inst_pp(t) < prem_gross_inst_pp(t)):
                return False
        elif not (prem_gross_inst_pp(t) == prem_rebate_inst_pp(t)
                  == prem_inst_pp(t) == 0.0):
            return False
    return True


def check_res_roll_fwd_resid(y):
    """The Thiele residual of the first-order *Deckungskapital* in **policy year** y; zero.

    ``( res_pp_at(y,"BEF_PREM") + Gn 1{y<k} ) (1 + i)
    - q1(y) B(y) - (1 - q1(y)) res_pp_at(y+1,"BEF_PREM")``, the annual rate and the sum
    insured read at that policy year's opening month ``12 y``.

    An **annual** recursion on an annual reserve, and it stays one on the monthly grid:
    the *Rechnungszins* is an annual rate and the reserve is struck against it.  The
    reserve is built **prospectively** and the recursion rolls it **forward**, so the two
    agree only if the survivorship, the discounting and the premium term are all indexed
    consistently.  It is checked from ``y = 0`` on every model point, including an
    in-force one whose cash flows start later: the reserve is a tariff quantity and the
    tariff was struck at issue.
    """
    lhs = (res_pp_at(y, "AFT_PREM")) * (1.0 + rechnungszins)         # noqa: F821
    q1 = mort_rate_tar(12 * y)
    rhs = (q1 * benefit_pp(12 * y)
           + (1.0 - q1) * res_pp_at(y + 1, "BEF_PREM"))
    return lhs - rhs


def check_res_roll_fwd():
    """True when the reserve rolls forward, opens at zero and closes at zero.

    ``res_pp_at(0, "BEF_PREM") = 0`` is the premium equivalence restated, and
    ``res_pp_at(n, "BEF_PREM") = 0`` is exhaustion: the *Deckungskapital* of a term
    contract is fully consumed by expiry.  Between them the Thiele recursion must hold in
    every policy year.  This is the check that catches the product's characteristic
    modelling error — concluding from the absence of a *Sparanteil* that there is no
    reserve, and building a projection that cannot close.
    """
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    if abs(res_pp_at(0, "BEF_PREM")) > tol:
        return False
    if abs(res_pp_at(proj_len_y(), "BEF_PREM")) > tol:
        return False
    return all(abs(check_res_roll_fwd_resid(y)) <= tol
               for y in range(proj_len_y()))


def check_no_cash_value_resid(t):
    """The non-death benefit residual: ``claims(t,"LAPSE") + claims(t,"MATURITY")``; zero.

    **Trivially zero by construction**, because both kinds return a literal zero.  It is
    published because the zero is a statutory and contractual fact rather than a modelling
    choice — there is no *Rückkaufswert*, no *beitragsfreie Versicherungssumme* worth
    having and no *Erlebensfallleistung* — and because the failure it guards against is not
    an arithmetic slip but an import: a reader arriving from an endowment or a US model
    with cash surrender values wires a surrender scale into the lapse decrement, and every
    total in the frame still looks plausible.  A named check that must stay at zero makes
    that edit fail loudly.
    """
    return claims(t, "LAPSE") + claims(t, "MATURITY")


def check_no_cash_value():
    """True when a lapse and an expiry both pay nothing in every projected month."""
    return all(abs(check_no_cash_value_resid(t)) <= val_tol          # noqa: F821
               for t in range(proj_start(), proj_len()))


# ==========================================================================
# Result frames


def result_cf():
    """Result table of cash flows, indexed by the 0-based **policy month** t.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash flow
    on the same row.  **Two premium columns**: ``prem_gross`` is the guaranteed
    *Bruttobeitrag* instalment and does **not** enter ``net_cf``; ``premiums`` is the
    billed *Zahlbeitrag* instalment and does; ``prem_rebate`` is the
    *Beitragsverrechnung* between them.  All three are the amounts **collected in the
    month**, so on an annual *Zahlweise* eleven rows in twelve carry zeros in them — which
    is what an annual-mode policy looks like on a monthly grid, and what
    :func:`result_cf_annual` sums back up.
    ``expenses`` **excludes** ``commissions``, which is its own column, and ``net_cf``
    subtracts both once.  ``claims_lapse`` and ``claims_maturity`` are columns of zeros by
    statute and by contract and are published rather than dropped.  ``liability_cf`` is
    ``net_cf`` outgo-positive.

    The frame runs ``t = 12 duration_y ... proj_len() - 1`` contiguously and stops there:
    cover expires at the end of the last month with nothing payable and no survivors left
    in force.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "prem_gross": [prem_gross(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "prem_rebate": [prem_rebate(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by ``policy_year``.

    Every cash flow column is the total of that policy year's twelve months; ``pols_if``
    is the count at the **start** of the policy year, ``pols_if(12 (policy_year - 1))``,
    which is the number the annual-step model this replaced carried on the same row.  It
    is the monthly frame **regrouped and never a second projection**, which is what lets
    the notes' annual worked example stay annual and still be asserted cell by cell.

    On the ten annual-*Zahlweise* model points the two grids agree exactly on four
    columns — ``pols_if``, ``prem_gross``, ``premiums`` and ``prem_rebate`` — because an
    annual instalment is collected on the anniversary and weighted by the anniversary
    in-force under either grid.  They do **not** agree on ``claims_death`` or
    ``expenses``, which now fall where they happen rather than at the anniversary, and so
    not on ``net_cf``.  On a fractionated point not even the premium columns agree, and
    that is the *Ratenzahlungszuschlag* finally being charged for something.
    """
    df = result_cf()
    years = pd.Index([duration(t) + 1 for t in df.index],            # noqa: F821
                     name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_pols():
    """Result table of policy counts, rates, per-policy amounts and the reserve, indexed by t.

    The same 0-based monthly frame as :func:`result_cf`:
    ``t = proj_start() ... proj_len() - 1``.  Each **annual** rate is published beside the
    **monthly** rate derived from it, so the two speeds of the conversion can be read off
    one table: ``mort_rate`` and ``lapse_rate`` are the annual rates of the policy year
    containing the month — the vectors the technical notes tabulate — and
    ``mort_rate_mth`` and ``lapse_rate_mth`` the rates actually applied in it.
    ``prem_*_pp`` are likewise the year's annual amounts and ``prem_inst_pp`` the
    instalment collected in the month.  ``res_pp`` and ``res_zill_pp`` are the policy
    year's reserves, flat across its twelve rows, the first-order *Deckungskapital* being
    an annual construction.
    """
    ts = list(range(proj_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "age": [age(t) for t in ts],
            "policy_year": [policy_year(t) for t in ts],
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "mort_rate_tar": [mort_rate_tar(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "benefit_pp": [benefit_pp(t) for t in ts],
            "benefit_paid_pp": [benefit_paid_pp(t) for t in ts],
            "suicide_factor": [suicide_factor(t) for t in ts],
            "prem_gross_pp": [prem_gross_pp(t) for t in ts],
            "prem_rebate_pp": [prem_rebate_pp(t) for t in ts],
            "prem_paid_pp": [prem_paid_pp(t) for t in ts],
            "prem_inst_pp": [prem_inst_pp(t) for t in ts],
            "res_pp": [res_pp_at(duration(t), "BEF_PREM") for t in ts],
            "res_zill_pp": [res_zill_pp_at(duration(t), "BEF_PREM") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

rechnungszins = 0.01

sicherheitszuschlag_m = 1.25

sex_mix_male = 0.5

mort_be_factor = 1.0

surplus_share = 0.9

decl_scale = 1.0

v_max = 0.95

zillmer_rate = 0.025

comm_rate_init = 0.02

beta_tariff = 0.05

gamma_rate = 0.0003

maint_prem_pct = 0.03

comm_rate_renew = 0.01

expense_infl = 0.02

claim_expense = 250.0

suicide_share = 0.03

suicide_years = 3

shock_lapse_lambda = 0.0

sel_lapse_lambda = 0.0

sel_lapse_ref = 0.25

roll_fwd_tol = 1e-10

val_tol = 1e-09

pd = ("Module", "pandas")
