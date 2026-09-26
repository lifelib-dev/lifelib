# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.RV_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 6            # or switch the default

.. rubric:: Two clocks: a monthly frame over a mostly annual product

``t`` counts **policy months** from inception and is **0-based**: ``t = 0`` is the first
policy month. ``proj_len() = 12 x proj_len_y()`` is the **exclusive** end of the frame, so
``result_cf().index[-1] == proj_len() - 1``, and ``proj_len_y() = omega_age() - issue_age``
is the number of policy **years** behind it. A life annuity has no term, so the projection
ends where the annuitant cannot survive further rather than at a fixed horizon: on the
anchor cell, ``t = 0 ... 851``, seventy-one policy years running to attained age 121. A
new-business model point opens at ``t = 0``; an in-force point that has run ``duration_init``
complete policy years opens at ``t = t_start() = 12 x duration_init``, carrying its opening
balances on the model point. That is what lets one generational mortality surface and one
declared-rate path serve a book of mixed vintages.

**Almost nothing on this product is monthly, and the argument of a cells says which it is.**
Cells that state an **annual account** take a 0-based policy year ``k`` — the premium and its
whole decomposition, the *Deckungskapital*, the *Ansammlungsguthaben*, the § 169 Abs. 3
spread account, the declared rate and the interest surplus, the surrender value, the death
benefit, the *Beitragsfreistellung* election and the *Überschussrente* step. Cells that
state a **month** take ``t`` — the in force, the three decrements, the claims, the annuity
instalment, the expenses and every ``result_cf()`` column. ``duration(t) = t // 12`` is the
bridge, ``policy_year(t) = duration(t) + 1`` is the contractual 1-based label,
``age(t) = age_y(duration(t))`` and ``calendar_year(t) = calendar_year_y(duration(t))`` both
step on the **anniversary**, and ``is_anniv(t) = (t % 12 == 11)`` marks the month the annual
machinery acts in.

The decrement rates keep the library's two speeds: ``mort_rate(t)`` and ``lapse_rate(t)``
return the **annual** rate of the policy year — the vectors the notes tabulate and
``result_pols()`` prints — while ``mort_rate_mth(t)`` and ``lapse_rate_mth(t)``, each
``1 - (1 - r)^(1/12)``, are what the recursion applies, so twelve of each compound back to
the year. That is what leaves the whole annual layer **bit-identical** to the annual-step
model this replaced, on all fourteen model points: ``pols_if`` at every anniversary, both
account balances, the § 169 floor, the surrender value, the conversion capital and the
*Rentenfaktor* are unchanged, and ``result_pols()`` is row for row the table it was.

Two rates of 1 are **certainties rather than rates** and are placed in the anniversary month
instead of being twelfth-rooted: the terminal ``q = 1`` of the mortality proxy, which is the
table's closure convention, and the § 165 cash-out, which is a dated contractual act.
Spreading either geometrically would empty the cohort eleven months early.

.. rubric:: What the monthly grid changed, and what it did not

It did not change the premium. § 12 Abs. 1 VVG makes the *Versicherungsperiode* the **year**
for this tariff, the *Beitrag* is payable in advance for it, and the *Deckungskapital* the
whole model turns on is defined at anniversaries and nowhere between them — so
``prem_due(t)`` is true in the first month of each policy year and nowhere else, and premium
income is identical to the annual-step model's. The *Ratenzahlungszuschlag* remains the whole
of what the *Zahlweise* does here. (``KLV_DE_S`` is the contrast: there the ``echt`` reading
makes the period genuinely monthly, two model points differ in nothing else, and the
instalment stream is in the frame.)

It did not change what a claim is **paid**. § 169 Abs. 3 VVG strikes the value *zum Schluss
der laufenden Versicherungsperiode* and not at the cancellation date, so a policy leaving in
any month of policy year ``k`` is paid ``cv_pp(k)`` or ``db_pp(k)`` — the year-end value it
paid the year's premium in advance for. What moved is **when** the claim falls and **how many
policies are exposed** to it.

Three things did change, and they are the point of the conversion.

- **The annuity is monthly, and is now paid monthly.** ``annuity_pp(t)`` is one instalment,
  ``G + U(k)``, paid in advance at the beginning of the month on ``pols_annuity(t)``. The
  annual-step model paid ``12 (G + U)`` at the start of each payout year — a compression
  carried as a **[std]** that was generous to the payout phase by roughly half a year's
  interest on a year's annuity and by a full year of survivorship on instalments a decedent
  did not live to collect. On the anchor cell the annuity outgo falls from 23 485,03 € to
  23 115,89 €, and it falls on every one of the ten model points that reach a *Rentenbeginn*.
  The *Rentengarantiezeit* is now ``12m`` guaranteed **instalments** rather than ``m``
  annual lumps.
- **The decrements compete monthly.** Deaths and surrenders are taken in the same order as
  before — deaths first, surrenders on the survivors of them — but twelve times a year rather
  than once, so a life that the annual ordering would have counted as a death may surrender
  first. The **total** exits are unchanged at every anniversary; the split moves, by 16,87 €
  of claims from death to lapse on the anchor cell.
- **Expenses are borne for the months a policy was there.** ``expenses_pp(t)`` is a twelfth
  of the year's amount, inflated by ``(1 + expense_infl())^duration(t)``, so a policy leaving
  mid-year no longer bears a full year of administration. The anchor cell's expenses fall
  from 1 669,77 € to 1 646,77 €.

The *Rentenbeginn* falls at the **end of the deferment period** of ``n = aufschub_y`` years,
which is the end of month ``12n - 1`` and the same instant as the start of month ``12n``.
Accumulation months are ``t < 12n``; payout months are ``t >= 12n``. The *Kapitalabfindung*
is paid in month ``12n - 1``; the first annuity instalment falls in month ``12n``. On the
anchor cell ``n = 17``, the *Rentengarantiezeit* covers ``t = 204 ... 323`` and the
survivor-weighted annuity runs from ``t = 324`` to ``t = 851``.

.. rubric:: Two frames, and the third

:func:`result_cf` is the **monthly** cash flow statement and carries the six flows that cross
the contract boundary. :func:`result_cf_annual` sums it into policy years, which is the view
the technical notes' worked example is stated on. :func:`result_pols` is the **annual state**
behind both — the rates, the premium decomposition, the three account balances per policy and
at fund level, the year's credits, the surrender value and the death benefit — indexed by the
1-based ``policy_year``. The account movements ``av``, ``av_sur``, ``prem_to_av``,
``int_credited`` and ``bonus_credited`` live there and not in the cash flow statement: they
move once a year, and a cash flow statement whose columns do not all sum to its bottom line is
one a reader has to know which columns to skip.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/klassische_rentenversicherung/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RV_DE_S`` folder without its parent's CSVs produces a model that reads and then fails on
first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.RV_DE_S.Data`,
reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
mort_file                 data.mort_table()                  mort_table.csv
decl_rate_file            data.decl_rate_table()             decl_rate_table.csv
rentenfaktor_file         data.rentenfaktor_table()          rentenfaktor_table.csv
charge_file               data.charge_table()                charge_table.csv
lapse_file                data.lapse_table()                 lapse_table.csv
freq_load_file            data.freq_load_table()             freq_load_table.csv
param_file                data.param_table()                 param_table.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, ``av_*`` for account
values, plural nouns for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claims(t, kind)`` with an uppercase ``kind`` string, ``av_pp_at(t, timing)`` and
``pols_if_at(t, timing)`` for the within-year reads. The technical notes use compact
actuarial symbols instead. The mapping is:

==========================  ==============================  ==========================
Notes symbol                Cells                           Meaning
==========================  ==============================  ==========================
(none)                      model_point()                   The selected model point row
N = omega - issue_age       proj_len_y()                    Number of policy years
12 N                        proj_len()                      Exclusive end, in months
t0 = 12 duration_init       t_start()                       First projected month
k0 = duration_init          k_start()                       First projected policy year
(none)                      duration_mth(t)                 Elapsed policy months, = t
k(t)                        duration(t)                     0-based policy year of month t
t + 1 (contractual)         policy_year(t)                  1-based policy year label
(none)                      is_anniv(t)                     Last month of a policy year
x(k)                        age_y(k)                        Attained age in policy year k
x(t)                        age(t)                          The same, read at a month
tau(k)                      calendar_year_y(k)              Calendar year of policy year k
tau(t)                      calendar_year(t)                The same, read at a month
omega                       omega_age()                     Terminal age of the proxy
n                           (model point aufschub_y)        Deferment years
m                           (model point rgz_years)         Rentengarantiezeit years
kappa                       (model point kapitalwahl_rate)  Commutation take-up
l(t)                        pols_if(t)                      In force at the start of month t
l(t) - D, l(t+1)            pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
a(t)                        pols_annuity(t)                 Count the instalment is paid on
P(k)                        prem_pp(k)                      Gross premium in policy year k
P_sched(k)                  prem_pp_sched(k)                The premium as written at issue
(none)                      prem_due(t)                     Whether P falls due in month t
phi                         freq_load()                     Ratenzahlungszuschlag
(sum of P_sched)            beitragssumme_pp()              Zillmer base
alpha_total                 alpha_total_pp()                Total acquisition charge
alpha(k)                    charge_acq_pp(k)                Zillmered acquisition charge
alpha~(k)                   charge_acq_spread_pp(k)         Evenly spread acquisition charge
beta(k)                     charge_prem_pp(k)               Premium charge
gamma(k)                    charge_admin_pp(k)              Reserve-based charge
rho(k)                      charge_risk_pp(k)               Risikobeitrag
(none)                      nar_pp(k)                       Net amount at risk
S(k)                        prem_to_av_pp(k)                Sparbeitrag
C(k)                        charge_from_av_pp(k)            Charge met from the account
V(k)                        av_pp(k)                        Deckungskapital per policy
V after prem / after int    av_pp_at(k, timing)             BEF_PREM / AFT_PREM / AFT_INT
A(k)                        av_sur_pp(k)                    Ansammlungsguthaben per policy
Vtilde(k)                   av_spread_pp(k)                 Sec. 169(3) parallel account
Delta(k)                    spread_diff_pp(k)               Vtilde(k) - V(k)
i                           int_rate_guar()                 Rechnungszins
d(k)                        decl_rate(k)                    Declared laufende Verzinsung
b(k)                        bonus_rate(k)                   max(0, d(k) - i)
q*(t)                       mort_rate_guar(t)               First-order mortality, annual
q(t)                        mort_rate(t)                    Best-estimate mortality, annual
q^m(t)                      mort_rate_mth(t)                The monthly rate applied
(table)                     mort_rate_at_age(x)             Base-year table rate at age x
(trend)                     improve_rate(x)                 Annual improvement at age x
w(t)                        lapse_rate(t)                   Surrender rate, annual
w^m(t)                      lapse_rate_mth(t)               The monthly rate applied
Dcheck(k)                   db_base_pp(k)                   Start-of-year death measure
D(k)                        db_pp(k)                        Death benefit of policy year k
Rbar(k)                     cv_tariff_pp(k)                 Tariff surrender value
Runder(k)                   cv_floor_pp(k)                  Sec. 169(3) floor
R(k)                        cv_pp(k)                        Surrender value paid
K                           capital_conv_pp()               Conversion capital
f_g                         annuity_rate_guar()             Garantierter Rentenfaktor
f_c                         annuity_rate_curr()             Aktueller Rentenfaktor
f                           annuity_rate_appl()             max(f_g, f_c)
G                           annuity_guar_mth_pp()           Garantierte Rente, monthly
U(k)                        annuity_sur_mth_pp(k)           Ueberschussrente, monthly
G + U(k)                    annuity_pp(t)                   The instalment paid in month t
net_cf(t)                   net_cf(t)                       Net cash flow, income positive
liability_cf(t)             liability_cf(t)                 The same stream, outgo positive
==========================  ==============================  ==========================

Five namings needed care.

``db_base_pp`` and ``db_pp`` are two different quantities with deliberately similar names.
``db_base_pp(k)`` is the death benefit measured on **start-of-year** balances and exists
only to strike the *Risikobeitrag*, because a risk charge computed on the post-charge
balance would make the recursion circular. ``db_pp(k)`` is what a death claim actually pays,
on **end-of-year** balances. Both are published so the difference is visible rather than
buried, and **both take a policy year**: a death in any month of year ``k`` is paid
``db_pp(k)``.

``charge_*`` and ``expense_*`` are not synonyms. A **charge** is a deduction the tariff
makes from the premium or the *Deckungskapital*: it moves money inside the contract and
produces no cash flow. An **expense** is the insurer's own best-estimate outgo and is a cash
flow. ``expenses(t)`` is invariant to ``beta_rate`` and ``gamma_rate``; ``av_pp(k+1)`` is
not. Booking the *Kostenbeitrag* as an expense inflates outgo by the whole charge load and
is the commonest way to make a German model look conservative.

``av_pp`` and ``av_sur_pp`` are two accounts, not one balance split in two. The
*Deckungskapital* carries the guarantee and is credited at ``int_rate_guar()``; the
*Ansammlungsguthaben* is the *verzinsliche Ansammlung* side account and is credited at
``decl_rate(k)`` on its own balance plus ``bonus_rate(k)`` on the *Deckungskapital*'s
post-premium base. Each has its own roll-forward check, and both checks are **annual**.

``pols_if`` and ``pols_annuity`` differ inside the *Rentengarantiezeit* and nowhere else.
``pols_if(t)`` is the start-of-month count and the weight on every cash flow of the same
``result_cf()`` row; ``pols_annuity(t)`` is the count the annuity instalment is *paid on*,
which inside the guarantee window is the annuitised count and not the survivors.

``mort_rate`` and ``mort_rate_mth`` — and ``lapse_rate`` and ``lapse_rate_mth`` beside them —
are the library's two speeds and not two spellings of one rate. The unsuffixed name is the
**annual** rate of the policy year, which is what the notes tabulate and what a reader
checking against a table wants; the ``_mth`` name is the geometric twelfth the recursion
applies. Nothing in this model applies an unsuffixed decrement rate, and nothing divides one
by twelve.

.. rubric:: The declared rate contains the guarantee

This is the first thing to get right about a German profit-participating contract and the
first listed modeling pitfall. The *laufende Verzinsung* is the *Garantieverzinsung* **plus**
the *laufende Zinsüberschussbeteiligung*, not a surplus on top of the guarantee, so::

    bonus_rate(k) = max(0, decl_rate(k) - int_rate_guar())

and the two credits together deliver ``decl_rate(k)`` on the post-premium *Deckungskapital*
and never more. On the anchor cell that is 1,00 % into ``int_credited_pp`` and 1,55 % into
``bonus_credited_pp`` against a 2,55 % declaration. On model point 6 — a 2,75 % legacy
vintage against the same declaration — ``bonus_rate(k)`` is **zero in every policy year**
while ``int_credited_pp(k)`` is the largest in the table. A model that credits 1,00 % *and* a further
2,55 % puts 56,82 € into the anchor cell's first year against 40,82 €, and reaches 63 768,69 €
of accumulated value at the *Rentenbeginn* against 58 788,98 € — 8,5 % too much, the whole of it
sitting in the *Ansammlungsguthaben*.

.. rubric:: The guarantee vintage is a model-point attribute

``int_rate_guar()`` reads the model point, not a Reference. A German life book is a layered
stack of guarantee vintages: the *Höchstrechnungszins* applies to contracts concluded while
it is in force and existing contracts keep the rate they were written on. Points 1, 6 and 14
credit 1,00 %, 2,75 % and 0,90 % in the same run, from the same tables. Re-running point 6 on a
single global 1,00 % rate moves its *Deckungskapital* at *Rentenbeginn* by −7,7 % and its
*Ansammlungsguthaben* by +156 %, while the conversion capital moves by −0,8 %: the vintage error
is a **misallocation between the two accounts**, not a hole in the total, and it therefore
survives a reasonableness check on the headline figure.

.. rubric:: The within-year order, which no source fixes

Premium in advance, then the charges, then the *Rechnungszins* on what is left — all of it
once a **policy year**, on the anniversary::

    av_pp_at(k, "AFT_PREM") = av_pp(k) + prem_to_av_pp(k) - charge_from_av_pp(k)
    int_credited_pp(k)      = int_rate_guar() * av_pp_at(k, "AFT_PREM")
    av_pp_at(k, "AFT_INT")  = av_pp_at(k, "AFT_PREM") + int_credited_pp(k)

**This ordering is a standardization.** No document in this product's corpus fixes the
sequence of premium credit, charge deduction and interest accrual, and it is the single most
consequential such choice in the model: crediting interest on the opening balance alone
changes year-one interest by the whole of ``i x (prem_to_av_pp(0) - charge_from_av_pp(0))``.

Two further conventions inside the decomposition are [std] and are worth naming.
``charge_risk_pp`` and ``charge_admin_pp`` are struck on **start-of-year** balances, or the
recursion is circular. And charges are met **from the premium where there is one and from
the *Deckungskapital* where there is not**: ``charge_from_av_pp(k)`` is what makes a
*Beitragsfreistellung* cost something instead of being free.

.. rubric:: The Sec. 169(3) floor, carried as a difference

The surrender value is floored at the *Deckungskapital* that results from spreading the
charged acquisition costs **evenly over the first five contract years**. The two accounts
differ only in that charge, so the model carries the difference rather than a second full
recursion::

    spread_diff_pp_at(k, "AFT_INT") = (Delta(k) + alpha(k) - alpha~(k)) * (1 + i)

with ``gamma`` and ``rho`` taken at the same euro amount in both accounts **[std]**, which
is what makes the difference exact. Two consequences are not obvious. The difference is
**large in the first five years** — on the anchor cell the whole 25 ‰ is taken in the first
year against one fifth of it — and it **never returns to zero**, because the spread account earns
the *Rechnungszins* on the amounts not yet deducted. So on a zillmered tariff with a positive
*Rechnungszins* the floor sits above the tariff *Deckungskapital* at every duration.

The floor is the § 169 Abs. 3 *Deckungskapital* **alone**: profit shares sit on top of the
statutory minimum rather than inside it. That reading lets the floor bind early and stop
binding once the *Ansammlungsguthaben* has outgrown the interest residual and the
*Stornoabzug*, so both branches of ``cv_pp(k) = max(cv_tariff_pp, cv_floor_pp)`` are
exercised on the anchor cell alone — it binds through policy year 4 (``k = 3``) and not
after. The
alternative reading, in which the floor also carries the *Ansammlungsguthaben*, is **not
implemented** and would make the floor bind at every duration.

.. rubric:: Beitragsfreistellung is an election, not a decrement

*Beitragsfreistellung* is a **deterministic election** in the contractual policy year
``pup_year`` — policy year ``k = pup_year - 1`` — rather than a rate: a scalar per-policy
account cannot carry two sub-populations with different *Deckungskapital*, and no source
establishes a rate. Both statutory branches are implemented and both are exercised:

- **Conversion** (model point 7). ``prem_pp(k) = 0`` from the paid-up year, the *Deckungskapital*
  is **reset to** ``pup_value_pp()`` — the § 165 rule that the paid-up benefit is computed on
  the § 169 Abs. 3–5 value — the *Ansammlungsguthaben* is untouched, ``spread_diff_pp`` is set
  to zero because the two accounts have merged, and ``charge_admin_pp`` switches to
  ``gamma_pup_rate``. No *Stornoabzug* is taken **[std]**: Abs. 5 is drafted for a payout on
  *Kündigung*, and here the contract continues. The reset is real money and is published as
  ``pup_uplift(k)``.
- **Cash-out** (model point 8). Where the paid-up annuity would fall below the
  *Mindestversicherungsleistung*, § 165 has the contract cashed out at the surrender value
  including profit shares instead of made paid-up. The whole surviving cohort then leaves in
  the **last month** of policy year ``k = pup_year - 2`` through the surrender decrement, at
  ``cv_pp(k)``. That is the one place ``lapse_rate`` returns 1, and ``lapse_rate_mth``
  places the certainty in the anniversary month rather than spreading it: § 165 makes the
  cash-out fall at the end of the *Versicherungsperiode*, not a twelfth of the way into it.

``pup_year`` is the **contractual policy year** of the election, so the contract is paid up
from ``k = pup_year - 1``. ``pup_uplift(k)`` is booked in the **transition year**
``k = pup_year - 2``, weighted by ``pols_if(12 (pup_year - 1))``, because that is the year
whose roll-forward needs it: the uplift is the step between
``av_pp_at(pup_year - 2, "AFT_INT")`` and the reset ``av_pp(pup_year - 1)``, and
``check_av_roll_fwd()`` closes in every policy year only if it is credited there. The
technical notes describe the same amount from the receiving year's point of view.

A *Beitragsfreistellung* is not a lapse. The paid-up contract keeps its guarantee vintage and
its guaranteed *Rentenfaktor* and pays a reduced benefit; the surrendered one is gone for
cash. On point 7 ``pols_if`` is unbroken through the paid-up year and the conversion itself
moves no policy: ``lapse_rate`` in policy year ``pup_year - 2`` is the ordinary duration-9
table rate of 3,5 % and not 1. What is **not** true is that surrender ceases: a *beitragsfrei*
contract keeps its § 168 VVG *Kündigung* right, so the surrender claims of policy year
``pup_year`` are positive on point 7 and stay positive from the paid-up year on.

.. rubric:: The Rentenbeginn

Everything happens at the end of the last accumulation month ``t = 12n - 1`` — which is the
end of policy year ``k = n - 1`` — on the survivors of that month's decrements::

    capital_gross_pp = av_pp_at(n - 1, "AFT_INT") + av_sur_pp_at(n - 1, "AFT_INT")
    capital_conv_pp  = max(guar_capital_pp, capital_gross_pp + val_reserve_pp)
    annuity_rate_appl = max(annuity_rate_guar, annuity_rate_curr)
    annuity_guar_mth_pp = capital_conv_pp / 10 000 * annuity_rate_appl

``val_reserve_pp`` is the *Bewertungsreserven* crystallisation, which § 153 Abs. 3 VVG makes
*hälftig* and which the transition to annuity payment is a key point for; the **rate** is a
placeholder. The commuting policyholders receive ``capital_conv_pp`` — the same capital the
annuitants convert, *Bewertungsreserven* included: the corpus gives no basis for paying them
less, and inventing one would be a charge no source supports. Both account balances go to
zero from ``k = n``.

The applied factor is ``max(garantierter, aktueller)``, guaranteed for the whole payment
period, and it is a **written option on the insurer's own future annuity tariff**. Both
branches ship: the current factor wins on the anchor cell at 32,00 € against 28,00 €, and
the guarantee binds on point 13, whose ``guar_capital_pp`` floor binds at the same time.

.. rubric:: The Rentengarantiezeit is paid to the dead

Inside the guarantee window the instalment is due whether or not the annuitant is alive, so
it is weighted by the **annuitised** count and not by survivors::

    pols_annuity(t) = pols_annuitization(12n - 1)  for 12n <= t < 12n + 12m
                    = pols_if(t)                   for t >= 12n + 12m

Because ``pols_if(t) <= pols_annuitization(12n - 1)`` throughout the payout phase this is
``max(pols_if(t), 1{12n <= t < 12n + 12m} pols_annuitization(12n - 1))``, which is how
:func:`check_annuity_guarantee` states it — and stating it that way is what makes the check
independent of the definition it is checking. On the anchor cell the two differ at
``t = 204 ... 323`` and coincide from ``t = 324``.

**The window is 12m guaranteed instalments, not m annual lumps.** That is what a
*Rentengarantiezeit* is — a *Rente* is a monthly payment and the guarantee is a guarantee of
monthly payments — and it is a thing the annual grid could only approximate.

.. rubric:: Modules that are recorded and not applied

- ``annuity_admin_rate`` ships in ``charge_table.csv`` at 1,5 % of each instalment and is
  **not applied**. The *Rentenfaktor* is exogenous here and already carries the tariff's
  payout loading, so deducting a further administration charge from the annuity would charge
  it twice. ``annuity_payments(t)`` is ``(G + U(k)) a(t)`` exactly.
- ``annuity_due_factor()`` is a **diagnostic and nothing else**. It is the annuity-due
  present value on the shipped mortality proxy at the guarantee interest basis, published so
  that the gap between the [std] *Rentenfaktor* and the [std] annuity table is visible rather
  than hidden. **They are not calibrated to each other, and the *Rentenfaktor* is
  authoritative**: it fixes the benefit amount, while the mortality proxy fixes only how long
  that amount is paid. No cash flow reads it.
- No *Bonusrente* ledger, no *Zuzahlung*, no survivor's-annuity or BU rider, no § 163 VVG
  adjustment of the guaranteed *Rentenfaktor*, no dynamic surrender, no premium-default path
  and no tax. Each is named in the technical notes where it belongs.
- **No death benefit after the *Rentenbeginn***. *Beitragsrückgewähr in der Rentenbezugsphase*
  was not established by any source in this product's corpus and is not asserted:
  ``claims(t, "DEATH")`` is zero for every ``t >= 12n`` on every model point. What the corpus
  does establish for post-*Rentenbeginn* death is the *Rentengarantiezeit*, which is modelled.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — premiums in, benefits, annuity instalments and
expenses out — which is the notes' own orientation and the library-wide sign.
:func:`liability_cf` publishes the same stream outgo-positive, ``liability_cf(t) =
-net_cf(t)`` exactly, so a best estimate is ``sum v(t) liability_cf(t)`` over whatever
discount curve the valuation layer supplies. Both are columns of :func:`result_cf`, so the
identity is verifiable in the frame rather than only in prose.

``av``, ``av_sur``, ``prem_to_av``, ``int_credited`` and ``bonus_credited`` are **state
movements reported, not cash flows summed**: the *Sparbeitrag* and the two credits move money
inside the contract and never cross the boundary, and they move once a policy year, so they
are reported in :func:`result_pols`. The six that do cross it are ``premiums``, the three
``claims_*``, ``annuity_payments`` and ``expenses``, they are the whole of
:func:`result_cf`'s flow columns, and those six are exactly what :func:`check_net_cf`
reconciles.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells
#
# The model point and the frame


def model_point():
    """The selected model point as a Series, from *model_point_table.csv*.

    Thirty columns; the projection reads them through this one cells so that a model point
    is fetched once per ItemSpace.  Point 1 is the technical notes' worked-example anchor.
    """
    return data.model_point_table().loc[point_id]                    # noqa: F821


def omega_age():
    """The terminal age of the shipped mortality proxy, from *param_table.csv*.

    121 **[std]**.  ``mort_rate`` is 1 at ``omega_age - 1``, so the projection ends with no
    survivors and :func:`check_decrement_closure` closes on ``pols_if_init()`` exactly.
    """
    return int(data.param_table().at["omega_age", "value"])          # noqa: F821


def proj_len_y():
    """N: the **number** of projected policy years, ``omega_age() - issue_age``.

    A life annuity has no term, so the horizon is the age at which the annuitant cannot
    survive further rather than a fixed number of years — truncating one at, say, 40 years
    silently drops the tail the *Rentenfaktor* was priced for.  **71** on the anchor cell,
    whose last policy year ends at attained age 121.
    """
    return omega_age() - int(model_point()["issue_age"])


def proj_len():
    """The **exclusive** end of the frame, counted in policy **months**: ``12 x proj_len_y()``.

    The library-wide reading of ``proj_len()``, asserted in
    ``tests/test_model_conventions_de.py``: ``result_cf()`` covers
    ``t = t_start() ... proj_len() - 1`` and ``result_cf().index[-1] == proj_len() - 1``.
    This is lifelib's own ``for t in range(proj_len())``.  852 on the anchor cell, whose last
    row is ``t = 851``.
    """
    return 12 * proj_len_y()


def t_start():
    """The frame's first **month**: ``12 x duration_init``.

    ``duration_init`` is an elapsed count of completed policy **years**, so the conversion is
    a multiplication and no model point column changed.  0 for new business; 168 on an
    in-force point that has run fourteen years.
    """
    return 12 * k_start()


def k_start():
    """The frame's first **policy year**: ``duration_init`` itself.

    The annual clock's counterpart to :func:`t_start`.  Every cells taking a policy year ``k``
    — the premium, the charges, both accounts, the § 169 floor, the surrender value and the
    death benefit — is defined from here.
    """
    return int(model_point()["duration_init"])


def duration_mth(t):
    """The number of **complete policy months** elapsed at the start of month t: ``t`` itself.

    Published rather than inlined because it is the name the rest of the library uses for the
    elapsed-month count, and because a model whose frame starts partway through a contract
    must say once, in one place, that ``t`` is counted from **inception** and not from the
    frame's own start.
    """
    return t


def duration(t):
    """k(t): the **0-based policy year** month t falls in, ``duration_mth(t) // 12``.

    The bridge between the two clocks.  Every annual construction in this model — the
    premium, the *Deckungskapital*, the *Ansammlungsguthaben*, the § 169 Abs. 3 account, the
    declared rate, the surrender value and the death benefit — takes this ``k``, and every
    monthly one takes ``t``.
    """
    return duration_mth(t) // 12


def is_anniv(t):
    """Whether month t is the **last** month of its policy year: ``t % 12 == 11``.

    The month the annual machinery acts in.  Two decrements are certainties rather than
    rates — the § 165 cash-out and the terminal ``q = 1`` of the mortality proxy — and a
    certainty cannot be spread geometrically over twelve months without emptying the cohort
    eleven months early, so both are placed here instead.
    """
    return t % 12 == 11


def policy_year(t):
    """The **contractual, 1-based** policy year of month t: ``duration(t) + 1``.

    The label the input files are keyed on, and derived rather than indexed by.
    """
    return duration(t) + 1


def age_y(k):
    """x(k): the attained age at the start of policy year k, ``issue_age + k``."""
    return int(model_point()["issue_age"]) + k


def age(t):
    """x(t): the attained age in month t, ``age_y(duration(t))``.

    Age last birthday at issue **stepping on the policy anniversary**, which is the age basis
    the tariff is written on: the monthly grid does not refine it, and a model that stepped
    the age monthly would read a mortality rate the table does not publish.
    """
    return age_y(duration(t))


def calendar_year_y(k):
    """tau(k): the calendar year of policy year k, ``issue_year + k``.

    The second index of the generational mortality surface and of the declared-rate path.
    Because it is derived from the model point's own ``issue_year``, one surface and one
    declared path serve a book of mixed vintages: policy year 0 of a 2005 contract and policy
    year 0 of a 2026 contract read different calendar years from the same table.

    Like the attained age, it steps on the **anniversary** and not in a calendar month.  A
    policy-year grid and a calendar-year grid coincide only for contracts written on
    1 January, and reconciling the two is a valuation-date question this model does not pose.
    """
    return int(model_point()["issue_year"]) + k


def calendar_year(t):
    """tau(t): the calendar year of month t, ``calendar_year_y(duration(t))``."""
    return calendar_year_y(duration(t))


def pols_if_init():
    """The number of policies the model point represents; ``pols_if`` at the frame's start."""
    return float(model_point()["pols_if_init"])


def int_rate_guar():
    """i: the contract's *Rechnungszins*, **read from the model point**.

    Not a global assumption.  The *Höchstrechnungszins* applies to contracts concluded while
    it is in force and an existing contract keeps the rate it was written on, so a German
    life book is a layered stack of guarantee vintages: 1,00 % on the 2026 points, 2,75 % on
    point 6 and 0,90 % on point 14, in one run from one set of tables.
    """
    return float(model_point()["int_rate_guar"])


def mort_be_factor():
    """The loading from the first-order table to the best estimate, from *param_table.csv*.

    1.15 **[std]**, and **above one on purpose**.  For an annuity, prudence means assuming
    mortality *lower* than expected, so the first-order (tariff) table sits below best
    estimate and the second-order rate is the tariff rate loaded upward.  The safety margin
    of the real construction runs in two dimensions, level and trend; only the level is
    reproduced here.
    """
    return float(data.param_table().at["mort_be_factor", "value"])   # noqa: F821


def roll_fwd_tol():
    """The relative tolerance the ``check_*`` identities close to, from *param_table.csv*.

    1e-9, scaled by the magnitude of the quantities being compared.  A float comparison
    tolerance, not an actuarial assumption.
    """
    return float(data.param_table().at["roll_fwd_tol", "value"])     # noqa: F821


# ----------------------------------------
# The premium and the Beitragssumme


def freq_load():
    """phi: the *Ratenzahlungszuschlag* for the model point's *Zahlweise* **[std]**.

    1,000 annual, 1,020 half-yearly, 1,030 quarterly, 1,050 monthly.

    **The loading is what a sub-annual *Zahlweise* costs, and it is the whole of what this
    model takes from the *Zahlweise*.**  The premium is charged once a policy year, at the
    start of it, on a monthly grid exactly as on the annual one, because § 12 Abs. 1 VVG
    makes the *Versicherungsperiode* the **year** for this tariff — and the *Deckungskapital*
    the whole model turns on is defined at anniversaries and nowhere between them.  The
    instalments themselves are therefore still not modelled and ``n_instalments`` in the
    table remains documentation; what a finer grid would buy here is an unearned-premium
    convention on mid-year exits that no source in this product's corpus establishes.
    Compare ``KLV_DE_S``, whose *Zahlweise* **is** in the frame: there the ``echt`` reading
    makes the *Versicherungsperiode* genuinely monthly and two model points differ in nothing
    else, which is what justifies the instalment stream.
    """
    return float(data.freq_load_table().at[                          # noqa: F821
        model_point()["prem_freq"], "freq_load"])


def prem_pp_sched(k):
    """P_sched(k): the premium schedule **as written at inception**, per policy.

    Zero after the *Rentenbeginn* and after the paying term; the *Einmalbeitrag* in the
    first year (``k = 0``) on the ``einmal`` form; otherwise the loaded gross premium grown
    by the *Dynamik*.

    It ignores any later *Beitragsfreistellung* on purpose.  The § 4 DeckRV zillmer base is
    the sum of all premiums payable under the contract **as written**, and a later election
    does not retrospectively shrink that base — which is why :func:`beitragssumme_pp` sums
    this cells and not :func:`prem_pp`.
    """
    mp = model_point()
    if k < 0 or k >= int(mp["aufschub_y"]) or k >= int(mp["prem_term_y"]):
        return 0.0
    if mp["premium_form"] == "einmal":
        return float(mp["premium_single_pp"]) if k == 0 else 0.0
    return (float(mp["prem_gross_pp"]) * freq_load()
            * (1.0 + float(mp["dynamik_rate"])) ** k)


def prem_pp(k):
    """P(k): the gross premium actually charged per policy in year k, at the **start** of it.

    The schedule, switched off from the paid-up row where the contract has been made
    premium free.  Not further multiplied by a survival factor: deaths and surrenders fall at the end
    of the year, so a claimant has already paid the year's premium.
    """
    return 0.0 if paid_up(k) else prem_pp_sched(k)


def beitragssumme_pp():
    """The *Beitragssumme*: the sum of the premiums payable under the contract as written.

    ``sum of P_sched(u) for u = 0 .. min(prem_term_y, aufschub_y) - 1``, so the frequency loading
    is inside it.  51 000,00 € on the anchor cell.  This is the § 4 DeckRV base on which the
    acquisition charge is struck, and it is fixed at inception: a later
    *Beitragsfreistellung* does not shrink it.
    """
    mp = model_point()
    last = min(int(mp["prem_term_y"]), int(mp["aufschub_y"]))
    return sum(prem_pp_sched(u) for u in range(last))


def alpha_total_pp():
    """The total acquisition charge: ``alpha_rate x beitragssumme_pp()``.

    The *Höchstzillmersatz* is 25 ‰ of the *Beitragssumme* for contracts concluded from
    1 January 2015 and 40 ‰ before, the rate at conclusion applying for the whole term; the
    model uses the cap itself **[std]**, which is what makes the year-one *Sparbeitrag* small
    and the § 169 Abs. 3 floor bite.  1 275,00 € on the anchor cell.
    """
    return (float(data.charge_table().at[                            # noqa: F821
        (model_point()["charge_id"], "alpha_rate"), "value"])
        * beitragssumme_pp())


def alpha_cum_pp(k):
    """The acquisition charge already amortised at the **start** of period k.

    ``alpha_amort_pp_init`` at the frame's start, then a running total of
    :func:`charge_acq_pp`.  It never exceeds :func:`alpha_total_pp`, which is what the
    ``max(0, .)`` in :func:`charge_acq_pp` guarantees.
    """
    if k <= k_start():
        return float(model_point()["alpha_amort_pp_init"])
    return alpha_cum_pp(k - 1) + charge_acq_pp(k - 1)


def prem_cum_pp(k):
    """The premiums paid per policy before the **start** of period k.

    ``prem_cum_pp_init`` at the frame's start, then a running total of :func:`prem_pp`.  The
    *Beitragsrückgewähr* base: on the ``prem_refund`` death-benefit form the benefit is
    ``prem_cum_pp(k) + prem_pp(k)``, the premiums paid including the year of death, because
    the year's premium fell due at the start of it.
    """
    if k <= k_start():
        return float(model_point()["prem_cum_pp_init"])
    return prem_cum_pp(k - 1) + prem_pp(k - 1)


def prem_due(t):
    """Whether the year's premium falls due at the **beginning** of month t.

    ``duration_mth(t) % 12 == 0`` — the first month of each policy year and no other.  The
    *Versicherungsperiode* of this tariff is the year (§ 12 Abs. 1 VVG) and the *Beitrag* is
    payable in advance for it, so a monthly grid moves **when the exposed count is measured**
    and not when the money arrives.  See :func:`freq_load` for why the *Ratenzahlungszuschlag*
    is the whole of what the *Zahlweise* does here.
    """
    return duration_mth(t) % 12 == 0


def premiums(t):
    """Premium income in month t, an inflow: ``prem_pp(duration(t)) x pols_if(t)``, or zero.

    Non-zero only where :func:`prem_due` makes the year's premium payable.  The count is the
    in-force at the **start of the policy year**, which is ``pols_if(12k)`` — so the premium
    income of this model is **bit-identical** to the annual-step model it replaced.
    """
    return prem_pp(duration(t)) * pols_if(t) if prem_due(t) else 0.0


# ----------------------------------------
# The premium decomposition


def charge_acq_pp(k):
    """alpha(k): the **zillmered** acquisition charge taken in period k.

    ``min(P(k), max(0, alpha_total_pp() - alpha_cum_pp(k)))`` — as much of the outstanding
    acquisition charge as the year's premium can meet, and no more.  On the anchor cell the
    whole 1 275,00 € comes out of the first year's premium (``k = 0``) and nothing
    thereafter, which is what *Zillmerung* means and why that year's *Sparbeitrag* is thin.
    """
    return min(prem_pp(k), max(0.0, alpha_total_pp() - alpha_cum_pp(k)))


def charge_acq_spread_pp(k):
    """alpha~(k): the same charge spread **evenly over the first five contract years**.

    ``alpha_total_pp() / alpha_spread_years`` for ``k = 0 .. 4``, zero after.  This is the
    § 169 Abs. 3 VVG treatment, and it enters no account of its own: it drives
    :func:`spread_diff_pp`, the difference between the tariff *Deckungskapital* and the
    statutory surrender floor.  255,00 € on the anchor cell.
    """
    years = int(data.charge_table().at[                              # noqa: F821
        (model_point()["charge_id"], "alpha_spread_years"), "value"])
    return alpha_total_pp() / years if 0 <= k < years else 0.0


def charge_prem_pp(k):
    """beta(k): the premium charge, ``beta_rate x P(k)`` **[std]**.

    4,0 % of each gross premium.  An internal deduction, not an expense: it reduces the
    *Sparbeitrag* and produces no cash flow.
    """
    return float(data.charge_table().at[                             # noqa: F821
        (model_point()["charge_id"], "beta_rate"), "value"]) * prem_pp(k)


def charge_admin_pp(k):
    """gamma(k): the reserve-based administration charge on the **start-of-year** balance.

    ``gamma_rate x av_pp(k)`` while premiums are being paid and ``gamma_pup_rate x av_pp(k)``
    while the contract is premium-free **[std]** — a paid-up contract still bears
    administration cost, and the higher premium-free rate is what makes
    *Beitragsfreistellung* cost something instead of being free.  Struck on the start-of-year
    balance so the recursion stays acyclic.
    """
    item = "gamma_pup_rate" if paid_up(k) else "gamma_rate"
    return float(data.charge_table().at[                             # noqa: F821
        (model_point()["charge_id"], item), "value"]) * av_pp(k)


def nar_pp(k):
    """The net amount at risk at the start of period k: ``max(0, db_base_pp - av_pp)``.

    What the insurer would have to find out of its own funds if the policyholder died: the
    death benefit less the reserve already held against it.  On the ``deckungskapital``
    death-benefit form it is **identically zero**, because the benefit *is* the reserve — a
    good invariance test, and the reason :func:`charge_risk_pp` vanishes on points 2 and 12.
    On the ``prem_refund`` form it falls towards zero as the *Deckungskapital* catches up
    with the premiums paid.
    """
    return max(0.0, db_base_pp(k) - av_pp(k))


def charge_risk_pp(k):
    """rho(k): the *Risikobeitrag*, ``mort_rate_guar(k) x nar_pp(k)``, accumulation phase only.

    On the **first-order** basis, not the best estimate: the tariff's own mortality fixes the
    risk charge and the guaranteed benefits, while the second-order basis drives the
    projection's decrements.  Using one basis for both is a listed pitfall.  Zero after the
    *Rentenbeginn*, where no death benefit is payable.

    The rate is read at ``mort_rate_guar(12 * k)`` — the first month of policy year ``k``,
    which is where the monthly clock and the annual one meet.  ``mort_rate_guar`` returns the
    **year's** rate at every month of that year, so the argument selects the year and not a
    month, and the charge is the annual one the tariff strikes.
    """
    if k >= int(model_point()["aufschub_y"]):
        return 0.0
    return mort_rate_guar(12 * k) * nar_pp(k)


def charge_due_pp(k):
    """The total charge falling due in period k: ``alpha + beta + gamma + rho``.

    What the tariff deducts, before asking where it comes from.  :func:`charge_from_prem_pp`
    and :func:`charge_from_av_pp` split it between the premium and the *Deckungskapital*.
    """
    return (charge_acq_pp(k) + charge_prem_pp(k)
            + charge_admin_pp(k) + charge_risk_pp(k))


def charge_from_prem_pp(k):
    """The part of the year's charge the premium meets: ``min(P(k), charge_due_pp(k))``."""
    return min(prem_pp(k), charge_due_pp(k))


def charge_from_av_pp(k):
    """C(k): the part of the year's charge the premium could not meet, taken from the account.

    Zero while a premium is being paid that covers the charges; the whole of
    :func:`charge_due_pp` once the contract is premium-free, which is how a paid-up contract
    pays for its own administration **[std]**.
    """
    return charge_due_pp(k) - charge_from_prem_pp(k)


def prem_to_av_pp(k):
    """S(k): the *Sparbeitrag*, the premium net of what the charges took from it.

    ``P(k) - charge_from_prem_pp(k)``.  This is the amount credited to the
    *Deckungskapital* — the premium "insofar as it is not required for risk and expense
    cover".  1 600,63 € of the anchor cell's 3 000,00 € first premium, the rest being the
    whole zillmered acquisition charge.
    """
    return prem_pp(k) - charge_from_prem_pp(k)


def prem_to_av(k):
    """The *Sparbeitrag* for the model point as a whole: ``prem_to_av_pp(k) x pols_if(12 k)``.

    Reported in :func:`result_pols` as a **state movement, not a cash flow**: it moves money
    from the premium into the account and never crosses the contract boundary.

    Weighted by the in-force at the **start of the policy year**, which is the population the
    year's premium was collected from — the same weight the annual-step model used, so this
    and the four movements beside it are unchanged by the conversion.
    """
    return prem_to_av_pp(k) * pols_if(12 * k)


# ----------------------------------------
# The Deckungskapital


def av_pp(k):
    """V(k): the *Deckungskapital* per policy at the **start** of period k.

    ``av_pp_init`` at the frame's start, then :func:`av_pp_at` at ``"AFT_INT"`` of the
    previous year — with two exceptions.  In the paid-up row ``k = pup_year - 1`` on a
    converting contract the balance is **reset** to :func:`pup_value_pp`, the § 165 paid-up
    value computed on the § 169 Abs. 3–5 basis.  And from ``k = n`` it is **zero**: at the
    *Rentenbeginn* the whole balance is converted into the annuity or paid out as the
    *Kapitalabfindung*.
    """
    mp = model_point()
    if k <= k_start():
        return float(mp["av_pp_init"])
    if k >= int(mp["aufschub_y"]):
        return 0.0
    if int(mp["pup_year"]) > 0 and k == int(mp["pup_year"]) - 1 and not pup_cashout():
        return pup_value_pp()
    return av_pp_at(k - 1, "AFT_INT")


def av_pp_at(k, timing):
    """The *Deckungskapital* per policy at a point inside period k.

    ``"BEF_PREM"``
        V(k), the opening balance; the same number as :func:`av_pp`.

    ``"AFT_PREM"``
        after the premium has been credited and the charges taken:
        ``av_pp(k) + prem_to_av_pp(k) - charge_from_av_pp(k)``.  This is the base the
        *Rechnungszins* and the interest surplus are both applied to.

    ``"AFT_INT"``
        the end-of-year balance, after the *Rechnungszins*.  It is the balance a death claim
        and a surrender are measured on, the balance that rolls into V(k+1), and — at
        ``k = n - 1`` — half of the conversion capital.

    The order premium, then charges, then interest on what is left is a **standardization**:
    no document in this product's corpus fixes it, and it is the most consequential such
    choice in the model.
    """
    if timing == "BEF_PREM":
        return av_pp(k)
    if timing == "AFT_PREM":
        return av_pp(k) + prem_to_av_pp(k) - charge_from_av_pp(k)
    if timing == "AFT_INT":
        return av_pp_at(k, "AFT_PREM") + int_credited_pp(k)
    raise ValueError("invalid timing")


def int_credited_pp(k):
    """The *Rechnungszins* credited per policy: ``int_rate_guar() x av_pp_at(k, "AFT_PREM")``.

    The **guaranteed** part of the year's crediting.  The declared *laufende Verzinsung* is
    this plus :func:`bonus_credited_pp`'s interest-surplus component, never this plus the
    whole declared rate.
    """
    return int_rate_guar() * av_pp_at(k, "AFT_PREM")


def int_credited(k):
    """The *Rechnungszins* for the model point as a whole, a **state movement** not a cash flow."""
    return int_credited_pp(k) * pols_if(12 * k)


def av(k):
    """The *Deckungskapital* for the model point as a whole at the start of policy year k.

    ``av_pp(k) x pols_if(12 k)``: the per-policy balance times the in-force at the year's own
    anniversary.  The account is an **annual** construction and the fund built on it is too;
    the months in between move the population, not the balance.
    """
    return av_pp(k) * pols_if(12 * k)


def av_at(k, timing):
    """The fund-level *Deckungskapital* inside year k: ``av_pp_at x pols_if(12 k)``."""
    return av_pp_at(k, timing) * pols_if(12 * k)


def av_release(k):
    """The *Deckungskapital* leaving the fund at the end of period k.

    The end-of-year balance carried out by the policies that leave — deaths and surrenders
    before the *Rentenbeginn*, and in the last accumulation row ``k = n - 1`` **the whole
    balance**, because the annuitants' account is converted into the annuity and the
    commuters' is paid out.  Zero in the payout phase, where there is no account left.  Read
    by :func:`check_av_roll_fwd` and by nothing else.

    The leavers are counted over the **whole policy year**, ``pols_if(12k) - pols_if(12(k+1))``,
    whatever months inside it they left in, and each carries the balance struck at the year's
    end.  That is § 169 Abs. 3 VVG read literally — the value is struck *zum Schluss der
    laufenden Versicherungsperiode* and not at the cancellation date — and it is consistent
    with a premium payable in advance for the whole period: the policy paid for the period and
    is credited with it.
    """
    n = int(model_point()["aufschub_y"])
    if k >= n:
        return 0.0
    if k == n - 1:
        return av_pp_at(k, "AFT_INT") * pols_if(12 * k)
    return av_pp_at(k, "AFT_INT") * (pols_if(12 * k) - pols_if(12 * (k + 1)))


# ----------------------------------------
# The Ansammlungsguthaben


def av_sur_pp(k):
    """A(k): the *Ansammlungsguthaben* per policy at the **start** of period k.

    The *verzinsliche Ansammlung* side account: a **second, parallel** balance holding the
    declared surplus, with its own credited rate, settling at year end and on exit.  Zero
    from ``k = n``, the balance having gone into the conversion capital.  It is untouched
    by a *Beitragsfreistellung*.
    """
    mp = model_point()
    if k <= k_start():
        return float(mp["av_sur_pp_init"])
    if k >= int(mp["aufschub_y"]):
        return 0.0
    return av_sur_pp_at(k - 1, "AFT_INT")


def av_sur_pp_at(k, timing):
    """The *Ansammlungsguthaben* per policy at a point inside period k.

    ``"BEF_PREM"`` and ``"AFT_PREM"`` are both the opening balance — no premium is credited
    to this account — and ``"AFT_INT"`` is the balance after the year's surplus credit, which
    is what a death claim including surplus, a surrender and the conversion all read.
    """
    if timing in ("BEF_PREM", "AFT_PREM"):
        return av_sur_pp(k)
    if timing == "AFT_INT":
        return av_sur_pp(k) + bonus_credited_pp(k)
    raise ValueError("invalid timing")


def bonus_credited_pp(k):
    """The surplus credited per policy at the end of period k.

    ``bonus_rate(k) x av_pp_at(k, "AFT_PREM") + decl_rate(k) x av_sur_pp(k)``: the interest
    surplus on the *Deckungskapital*'s post-premium base, plus the **full declared rate** on
    the side account's own balance **[std]**.

    The first term is where the German arithmetic lives.  ``bonus_rate`` is
    ``max(0, decl_rate - int_rate_guar)``, applied to the same base the guarantee is applied
    to, so the guarantee and the surplus together deliver the declared *laufende Verzinsung*
    and never more.  On a 2,75 % vintage against a 2,55 % declaration the term is zero at
    every k, and that is the correct answer rather than a missing credit.
    """
    if k >= int(model_point()["aufschub_y"]):
        return 0.0
    return bonus_rate(k) * av_pp_at(k, "AFT_PREM") + decl_rate(k) * av_sur_pp(k)


def bonus_credited(k):
    """The surplus credit for the model point as a whole, a **state movement** not a cash flow."""
    return bonus_credited_pp(k) * pols_if(12 * k)


def av_sur(k):
    """The *Ansammlungsguthaben* for the model point as a whole at the start of policy year k."""
    return av_sur_pp(k) * pols_if(12 * k)


def av_sur_at(k, timing):
    """The fund-level *Ansammlungsguthaben* inside year k: ``av_sur_pp_at x pols_if(12 k)``."""
    return av_sur_pp_at(k, timing) * pols_if(12 * k)


def av_sur_release(k):
    """The *Ansammlungsguthaben* leaving the fund at the end of period k.

    The same shape as :func:`av_release`: the balance carried out by the policies that leave,
    and the whole balance at ``k = n - 1``.  Read by :func:`check_av_sur_roll_fwd` alone.
    """
    n = int(model_point()["aufschub_y"])
    if k >= n:
        return 0.0
    if k == n - 1:
        return av_sur_pp_at(k, "AFT_INT") * pols_if(12 * k)
    return av_sur_pp_at(k, "AFT_INT") * (pols_if(12 * k) - pols_if(12 * (k + 1)))


# ----------------------------------------
# The Sec. 169(3) parallel account, carried as a difference


def spread_diff_pp(k):
    """Delta(k): ``av_spread_pp(k) - av_pp(k)`` at the start of period k.

    The two accounts differ **only** in the acquisition charge, so the model carries the
    difference rather than a second full recursion — with ``gamma`` and ``rho`` taken at the
    same euro amount in both **[std]**, which is what makes the difference exact.

    Zero at the frame's start.  That is exact for new business and is a **simplification for
    an in-force point**, where the interest the spread account earned on the amounts not yet
    deducted is discarded; every in-force model point therefore opens at
    ``duration_init >= alpha_spread_years``, once the charge is fully amortised under both
    treatments.  Zero again from the paid-up row ``k = pup_year - 1`` on a converting
    contract, the two accounts having merged at the paid-up value.
    """
    mp = model_point()
    if k <= k_start():
        return 0.0
    if k >= int(mp["aufschub_y"]):
        return 0.0
    if int(mp["pup_year"]) > 0 and k == int(mp["pup_year"]) - 1 and not pup_cashout():
        return 0.0
    return spread_diff_pp_at(k - 1, "AFT_INT")


def spread_diff_pp_at(k, timing):
    """The difference recursion inside period k.

    ``"AFT_INT"`` is ``(Delta(k) + alpha(k) - alpha~(k)) x (1 + i)``: the year's excess of the
    zillmered charge over the evenly spread one, added to the running difference and rolled
    forward at the *Rechnungszins*.  ``"BEF_PREM"`` and ``"AFT_PREM"`` are the opening
    difference.

    The difference is large in the first five years — on the anchor cell the whole 25 ‰ is
    taken in the first year against one fifth of it — and it **never returns to zero**,
    because the spread account earns interest on what has not yet been deducted.
    """
    if timing in ("BEF_PREM", "AFT_PREM"):
        return spread_diff_pp(k)
    if timing == "AFT_INT":
        return ((spread_diff_pp(k) + charge_acq_pp(k) - charge_acq_spread_pp(k))
                * (1.0 + int_rate_guar()))
    raise ValueError("invalid timing")


def av_spread_pp(k):
    """Vtilde(k): the § 169 Abs. 3 *Deckungskapital* per policy at the start of year k."""
    return av_pp(k) + spread_diff_pp(k)


def av_spread_pp_at(k, timing):
    """The § 169 Abs. 3 *Deckungskapital* inside year k: ``av_pp_at + spread_diff_pp_at``."""
    return av_pp_at(k, timing) + spread_diff_pp_at(k, timing)


# ----------------------------------------
# Rates


def mort_rate_at_age(x):
    """The first-order base-year death rate at attained age x, for the model point's sex.

    ``q_base`` from *mort_table.csv*, a **[std]** Gompertz proxy anchored at
    ``q_base(M, 50) = 0.002000``.  The real basis is DAV 2004 R, which is the property of the
    Deutsche Aktuarvereinigung, is not public and is not redistributed here.
    """
    return float(data.mort_table().at[                               # noqa: F821
        (model_point()["sex"], int(x)), "q_base"])


def improve_rate(x):
    """The annual mortality improvement rate at attained age x, from *mort_table.csv*.

    1,5 % below age 60, grading linearly to 0,5 % at 100 and to zero at 110 **[std]** — a
    deliberate simplification of the *Starttrend* / *Zieltrend* structure the German
    construction uses, documented as one rather than presented as a replication.
    """
    return float(data.mort_table().at[                               # noqa: F821
        (model_point()["sex"], int(x)), "improve"])


def mort_rate_guar(t):
    """q*(t): the **first-order** annual death rate, on the generational surface.

    ``q_base(sex, x(t)) x (1 - improve(x(t)))^(tau(t) - mort_base_year)``.

    DAV 2004 R is a *Generationentafel*: mortality is indexed by birth cohort and the
    expected future improvement is built into the table rather than applied on top of it.
    That is why this cells depends on :func:`calendar_year` as well as :func:`age`.  A
    period-table proxy, priced at an annuitisation decades ahead, understates the liability
    by a margin that dwarfs every other assumption — on the anchor cell the annuitant reaches
    67 in 2043, thirty-eight improvement years after the proxy's 2005 base.

    This is the basis the *Risikobeitrag* and the guaranteed benefits are struck on, and
    **not** the basis the projection's decrements run on.

    It takes a **month** and returns that month's **policy year's annual** rate, which is the
    library convention wherever a grid is monthly: the rate the notes tabulate keeps its own
    name, and the rate the recursion applies is spelled ``_mth``.  Flat across the twelve
    months of a policy year, because both the attained age and the calendar year step on the
    anniversary.
    """
    x = age(t)
    base_year = int(data.param_table().at["mort_base_year", "value"])  # noqa: F821
    return min(1.0, mort_rate_at_age(x)
               * (1.0 - improve_rate(x)) ** (calendar_year(t) - base_year))


def mort_rate(t):
    """q(t): the **best-estimate annual** death rate, ``mort_rate_guar(t) x mort_be_factor()``.

    The second-order basis, which drives :func:`pols_death` and hence every decrement.  The
    factor is above one because for an annuity prudence means assuming mortality *lower* than
    expected, so the first-order table sits below best estimate.  Capped at 1, and equal to 1
    at attained age ``omega_age() - 1``, which is what ends the projection with no survivors.

    The **annual** rate, flat across a policy year; :func:`mort_rate_mth` is what the monthly
    recursion applies.
    """
    return min(1.0, mort_rate_guar(t) * mort_be_factor())


def mort_rate_mth(t):
    """q^m(t): the **monthly** death rate, ``1 - (1 - q(t))^(1/12)``.

    The rate the in-force recursion applies.  It is a **geometric** twelfth and never
    ``q(t) / 12``: twelve of it compound back to the year's annual rate exactly, which is what
    leaves ``pols_if`` at every anniversary equal to the annual-step model's and with it every
    account balance, every reserve and every premium.  Dividing by twelve would undershoot the
    annual rate and leave a cohort that never quite runs off.

    **One exception, and it is a certainty rather than a rate.**  ``mort_rate`` is 1 at attained
    age ``omega_age() - 1``, which is the mortality proxy's closure convention — nobody survives
    the table's last year — and not an experience rate.  Twelfth-rooting it would kill the whole
    cohort in the **first** month of that policy year and stop the annuity eleven months early;
    the certainty is placed in the anniversary month instead, so the survivors are paid the
    table's last full year of annuity and then die, which is what the table says.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def decl_rate(k):
    """d(k): the declared *laufende Verzinsung* for the model point's scenario in year k.

    Read from *decl_rate_table.csv* at ``(decl_scenario_id, calendar_year_y(k))``, clamped to
    the table's calendar range so a projection running past its last declared year holds that
    year flat.  2,55 % level on the ``base`` path, 1,50 % on ``low`` **[std]**.

    **The declared rate contains the guarantee.**  It is the *Garantieverzinsung* plus the
    *laufende Zinsüberschussbeteiligung*, never a surplus on top of the guarantee.
    """
    tbl = data.decl_rate_table()                                     # noqa: F821
    scen = model_point()["decl_scenario_id"]
    years = tbl.loc[scen].index
    y = min(max(calendar_year_y(k), int(years.min())), int(years.max()))
    return float(tbl.at[(scen, y), "decl_rate"])


def bonus_rate(k):
    """b(k): the interest-surplus rate, ``max(0, decl_rate(k) - int_rate_guar())``.

    1,55 % on the anchor cell's 1,00 % vintage against a 2,55 % declaration; **zero in every
    policy year** on point 6's 2,75 % vintage against the same declaration, because a contract already
    guaranteed more than the declared rate receives no interest surplus.  That is a real and
    important German result, not a modelling artefact, and it is what the ``max(0, .)``
    exists to produce.
    """
    return max(0.0, decl_rate(k) - int_rate_guar())


def lapse_rate(t):
    """w(t): the annual surrender rate in period t.

    From *lapse_table.csv*, holding the last row for durations beyond the table.  **Zero from
    the *Rentenbeginn***: there is no surrender in the payout phase.

    The table's ``duration`` column is the **contractual policy year**, 1-based, so the
    lookup goes through :func:`policy_year`: the frame's first month ``t = 0`` reads
    duration 1, and so do the eleven months after it.  Every level is **[std]**; the one
    shaped feature is the **duration-12 step**, at the twelve-year threshold § 20 Abs. 1
    Nr. 6 EStG puts on the halving of the taxable gain, so German Schicht-3 surrenders are
    suppressed approaching duration 12 and spike at it — which the model reads across months
    132 to 143.

    It also carries the § 165 cash-out branch: where a *Beitragsfreistellung* would leave a
    paid-up annuity below the *Mindestversicherungsleistung*, the rate is 1 in the policy year
    before the paid-up one and the whole surviving cohort leaves at the surrender value.

    This is the **annual** rate, flat across a policy year; :func:`lapse_rate_mth` is what the
    recursion applies.
    """
    mp = model_point()
    if duration(t) >= int(mp["aufschub_y"]):
        return 0.0
    pup = int(mp["pup_year"])
    if pup > 0 and duration(t) == pup - 2 and pup_cashout():
        return 1.0
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.at[min(policy_year(t), int(tbl.index.max())), "lapse_rate"])


def lapse_rate_mth(t):
    """w^m(t): the **monthly** surrender rate, ``1 - (1 - w(t))^(1/12)``.

    A geometric twelfth, for the same reason as :func:`mort_rate_mth`: twelve of it compound
    back to the year's rate, so every anniversary count is the annual-step model's.

    **The § 165 cash-out is the exception**, and for the same reason the terminal ``q = 1`` is.
    An annual rate of 1 there is not an experience rate but a dated contractual act: § 165 VVG
    has the contract cashed out at the end of the *Versicherungsperiode* in which the election
    would have fallen.  Spreading that certainty geometrically would empty the cohort in the
    year's first month, eleven months before the election; it is placed in the anniversary
    month instead.
    """
    w = lapse_rate(t)
    if w >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - w) ** (1.0 / 12.0)


# ----------------------------------------
# Benefits, values and the Beitragsfreistellung election


def db_base_pp(k):
    """Dcheck(k): the death benefit measured on **start-of-year** balances.

    Used for one thing only — striking the *Risikobeitrag* through :func:`nar_pp`.  A risk
    charge computed on the post-premium, post-charge balance would make the recursion
    circular, since that balance depends on the charge.  Compare :func:`db_pp`, which is what
    a claim actually pays and reads end-of-year balances: the two are different quantities
    with deliberately similar names.
    """
    mp = model_point()
    form = mp["death_benefit_form"]
    paid = prem_cum_pp(k) + prem_pp(k)
    if form == "prem_refund":
        return paid
    if form == "deckungskapital":
        return av_pp(k)
    if form == "max":
        return max(paid, av_pp(k))
    raise ValueError("invalid death_benefit_form")


def db_pp(k):
    """D(k): the death benefit per policy actually paid on a death in period k.

    Three documented designs, on **end-of-year** balances: *Beitragsrückgewähr* (the premiums
    paid, including the year's), the accumulated *Deckungskapital*, or the larger of the two;
    plus the *Ansammlungsguthaben* where ``db_incl_surplus`` is set.

    **Zero after the *Rentenbeginn*.**  *Beitragsrückgewähr in der Rentenbezugsphase* was not
    established by any source in this product's corpus, so it is not asserted; what the corpus
    does establish for post-*Rentenbeginn* death is the *Rentengarantiezeit*, which is
    modelled in :func:`pols_annuity`.
    """
    mp = model_point()
    if k >= int(mp["aufschub_y"]):
        return 0.0
    form = mp["death_benefit_form"]
    paid = prem_cum_pp(k) + prem_pp(k)
    if form == "prem_refund":
        base = paid
    elif form == "deckungskapital":
        base = av_pp_at(k, "AFT_INT")
    elif form == "max":
        base = max(paid, av_pp_at(k, "AFT_INT"))
    else:
        raise ValueError("invalid death_benefit_form")
    if int(mp["db_incl_surplus"]):
        base = base + av_sur_pp_at(k, "AFT_INT")
    return base


def surr_charge_pp(k):
    """The *Stornoabzug*: ``stornoabzug_rate x (av_pp_at + av_sur_pp_at)`` at ``"AFT_INT"``.

    A **flat percentage of the pre-deduction value with no duration term**, which is the
    shape § 169 Abs. 5 VVG allows: a deduction is permitted only if agreed, quantified and
    appropriate, and an agreement of a deduction in respect of not-yet-amortised *Abschluss-
    und Vertriebskosten* is void.  A duration-graded deduction that unwound over the first
    years would be exactly the void kind.  2,0 % on ``zillmer_25`` and nil on ``zillmer_40``
    **[std]**; whatever it is set to, :func:`cv_pp` cannot fall below :func:`cv_floor_pp`.
    """
    return (float(data.charge_table().at[                            # noqa: F821
        (model_point()["charge_id"], "stornoabzug_rate"), "value"])
        * (av_pp_at(k, "AFT_INT") + av_sur_pp_at(k, "AFT_INT")))


def cv_tariff_pp(k):
    """Rbar(k): the tariff surrender value, both accounts net of the *Stornoabzug*."""
    return (av_pp_at(k, "AFT_INT") + av_sur_pp_at(k, "AFT_INT")
            - surr_charge_pp(k))


def cv_floor_pp(k):
    """Runder(k): the § 169 Abs. 3 VVG floor — the five-year-spread *Deckungskapital*.

    ``av_spread_pp_at(k, "AFT_INT")``, and the *Deckungskapital* **alone**: § 169 Abs. 3
    speaks of the reserve, and profit shares sit on top of the statutory minimum rather than
    inside it, which is the reading § 165 Abs. 2's "surrender value ... including profit
    shares" supports.  The alternative reading, in which the floor also carries the
    *Ansammlungsguthaben*, is not implemented and would make the floor bind at every duration.
    """
    return av_spread_pp_at(k, "AFT_INT")


def cv_pp(k):
    """R(k): the surrender value per policy, ``max(cv_tariff_pp(k), cv_floor_pp(k))``.

    On the anchor cell the **floor binds through k = 3** — the zillmered account has not yet
    caught up with the evenly spread one — and stops binding once the *Ansammlungsguthaben*
    has outgrown the interest residual and the *Stornoabzug*.  Both branches are therefore
    exercised on the anchor cell alone, which is why the floor is not merely present but
    tested.
    """
    return max(cv_tariff_pp(k), cv_floor_pp(k))


def paid_up(k):
    """True where the contract has been made premium-free by ``pup_year``.

    ``pup_year`` is the **contractual policy year** of the *Beitragsfreistellung*, 1-based,
    with 0 meaning "never", so the paid-up row is ``k = pup_year - 1`` and the contract is
    premium-free from there on.

    A **deterministic election** on the model point, not a decrement rate: a scalar
    per-policy account cannot carry two sub-populations with different *Deckungskapital*, and
    no source establishes a rate.  A portfolio model needs the sub-population split this one
    does not have.
    """
    pup = int(model_point()["pup_year"])
    return bool(pup > 0 and k >= pup - 1)


def pup_value_pp():
    """The § 165 paid-up value: the § 169 Abs. 3–5 value at the end of row ``pup_year - 2``.

    ``max(av_pp_at, av_spread_pp_at)`` at ``"AFT_INT"`` of that year — the § 165 rule that the
    premium-free benefit is calculated on the calculation basis of the premium calculation,
    **on the basis of the surrender value under § 169 paragraphs 3 to 5**.  No *Stornoabzug*
    is taken on this route **[std]**: Abs. 5 is drafted for a payout on *Kündigung*, and here
    the contract continues.
    """
    pup = int(model_point()["pup_year"])
    if pup <= 0:
        return 0.0
    return max(av_pp_at(pup - 2, "AFT_INT"), av_spread_pp_at(pup - 2, "AFT_INT"))


def pup_cashout():
    """True where the paid-up annuity would fall below the *Mindestversicherungsleistung*.

    § 165 VVG gives the conversion right only where the agreed minimum insurance benefit is
    reached; below it the insurer must pay the surrender value attributable to the insurance,
    **including profit shares**, under § 169.  The test here is
    ``pup_value_pp() / 10 000 x annuity_rate_guar() < min_annuity_mth``: the monthly annuity
    the paid-up value would buy at the **guaranteed** factor, against a 30,00 € threshold
    **[std]**.  True on model point 8, whose paid-up value at duration 2 buys 5,45 € a month.
    """
    pup = int(model_point()["pup_year"])
    if pup <= 0:
        return False
    threshold = float(data.charge_table().at[                        # noqa: F821
        (model_point()["charge_id"], "min_annuity_mth"), "value"])
    return bool(pup_value_pp() / 10000.0 * annuity_rate_guar() < threshold)


def pup_uplift(k):
    """The *Deckungskapital* credited by the paid-up reset, booked in the transition year.

    ``(pup_value_pp() - av_pp_at(k, "AFT_INT")) x pols_if(k + 1)`` in the transition row
    ``k = pup_year - 2``, and zero everywhere else and on every point that never converts.
    It is the step between the zillmered end-of-year balance and the § 169 Abs. 3–5 paid-up
    value the contract restarts from, and it is **real money** rather than a bookkeeping
    entry: without it the fund-level roll-forward of :func:`check_av_roll_fwd` would not
    close at that ``k``.

    Booked in the row **before** the paid-up row ``k = pup_year - 1`` because that is the row
    whose roll-forward needs it; the technical notes describe the same amount from the
    receiving row's point of view.
    """
    pup = int(model_point()["pup_year"])
    if pup <= 0 or k != pup - 2 or pup_cashout():
        return 0.0
    return (pup_value_pp() - av_pp_at(k, "AFT_INT")) * pols_if(12 * (k + 1))


# ----------------------------------------
# Decrements and the in-force recursion


def pols_if(t):
    """l(t): the number of policies in force at the **start** of period t.

    ``pols_if_init()`` at the frame's start — ``t = 0`` for new business and
    ``t = t_start()`` for an in-force point — then
    ``l(t+1) = l(t) - deaths - surrenders - commutations``, **month by month**.  This is the
    weight on every monthly cash flow of the same :func:`result_cf` row; the annuity is
    weighted by :func:`pols_annuity` instead, which differs inside the *Rentengarantiezeit*.

    ``pols_if(12k)`` — the count at an anniversary — is **bit-identical to the annual-step
    model's** ``pols_if(k)``, because both decrements compound geometrically and the order
    within a month is the annual model's order within a year: deaths first, surrenders on the
    survivors of them.  What the finer grid changes is the **split** between the two, not the
    total: competing monthly means a life that would have died in the annual model's year-end
    ordering may surrender first, so deaths fall and surrenders rise by the same count.

    ``pols_if(proj_len())`` — one past the frame's last row — is defined and is **zero**,
    because ``mort_rate`` is 1 in the policy year at attained age ``omega_age() - 1``.  It is
    read by :func:`check_decrement_closure` and by nothing else, and :func:`result_cf` stops
    at ``proj_len() - 1``.
    """
    if t < t_start() or t > proj_len():
        return 0.0
    if t == t_start():
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside period t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after deaths, before surrenders — the processing order takes deaths at the end of the
        month and surrenders after them **[std order]**, so this is the population surrenders
        are taken from.  It is the annual-step model's order, one twelfth of the way along.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state, after deaths, surrenders and — at the last
        accumulation month ``t = 12n - 1`` — the commutation split.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) - pols_death(t)
    if timing == "AFT_DECR":
        return (pols_if(t) - pols_death(t) - pols_lapse(t)
                - pols_commutation(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q^m(t): expected deaths in **month** t, at the end of it.

    On the **second-order** basis, at the monthly rate.  The claimant has already paid the
    year's premium, which fell due in advance at the start of the *Versicherungsperiode*, so
    :func:`premiums` is not further multiplied by a survival factor.  Deaths continue through
    the payout phase and move :func:`pols_if`, but pay nothing: ``db_pp`` is zero after the
    *Rentenbeginn*.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Surrenders at the end of period t, taken from the survivors of the year's deaths.

    Zero in the payout phase, where :func:`lapse_rate` is zero.  A *Beitragsfreistellung* is
    **not** counted here: it is an election that keeps the contract alive, not a decrement.
    The one place the two meet is the § 165 cash-out branch, where the whole surviving cohort
    leaves through this decrement at the surrender value, in the anniversary month.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def pols_surv_rb():
    """The policies surviving to the *Rentenbeginn*: ``l - deaths - surrenders`` at ``n - 1``.

    The population the *Kapitalwahlrecht* splits.  Struck at the end of the last accumulation
    **month** ``t = 12n - 1``, after that month's decrements and before the commutation — the
    same instant as the annual-step model's end of row ``n - 1``, and the same number.
    """
    t_rb = 12 * int(model_point()["aufschub_y"]) - 1
    return pols_if(t_rb) - pols_death(t_rb) - pols_lapse(t_rb)


def pols_commutation(t):
    """The policies taking the *Kapitalabfindung* at the *Rentenbeginn*.

    ``kapitalwahl_rate x pols_surv_rb()`` in the last accumulation month ``t = 12n - 1`` and
    zero at every other t.  The rate is a **model-point attribute, not a behavioural
    formula**: the annuitise-or-commute decision is a tax comparison — the *Ertragsanteil* on
    each instalment against half the *Unterschiedsbetrag* taxed once — and this model computes
    no tax, so the rate stands in for a calculation it does not perform.
    """
    if t != 12 * int(model_point()["aufschub_y"]) - 1:
        return 0.0
    return float(model_point()["kapitalwahl_rate"]) * pols_surv_rb()


def pols_annuitization(t):
    """The policies converting to the annuity at the *Rentenbeginn*.

    ``(1 - kapitalwahl_rate) x pols_surv_rb()`` in the last accumulation month ``t = 12n - 1``
    and zero elsewhere.  It is ``pols_if(12n)`` by construction, and it is the count the
    *Rentengarantiezeit* instalments are paid on however many annuitants are still alive.
    """
    if t != 12 * int(model_point()["aufschub_y"]) - 1:
        return 0.0
    return (1.0 - float(model_point()["kapitalwahl_rate"])) * pols_surv_rb()


def pols_annuity(t):
    """a(t): the count the annuity instalment is **paid on** in period t.

    Zero before the *Rentenbeginn*; the **annuitised** count inside the *Rentengarantiezeit*,
    ``12n <= t < 12n + 12m``, because there the instalment is due whether or not the annuitant
    is alive; the survivors after it.  Weighting the guaranteed months by survivors is a listed
    pitfall, and on the anchor cell the two differ over ``t = 204 ... 323`` and coincide from
    ``t = 324``.

    The window is counted in **months** now, which is what the *Rentengarantiezeit* is: ten
    guaranteed years are 120 guaranteed monthly instalments, and the annual grid could only
    state them as ten annual lumps.
    """
    mp = model_point()
    n_mth = 12 * int(mp["aufschub_y"])
    if t < n_mth:
        return 0.0
    if t < n_mth + 12 * int(mp["rgz_years"]):
        return pols_annuitization(n_mth - 1)
    return pols_if(t)


# ----------------------------------------
# The Rentenbeginn and the annuity in payment


def capital_gross_pp():
    """The accumulated value per policy at the *Rentenbeginn*, before the *Bewertungsreserven*.

    ``av_pp_at(n - 1, "AFT_INT") + av_sur_pp_at(n - 1, "AFT_INT")``: both accounts, at the
    end of the last accumulation **policy year** ``k = n - 1``, after that year's crediting.
    The contract value used for annuitisation includes the *Überschussbeteiligung*.  Unchanged
    by the conversion: the *Rentenbeginn* is an anniversary — month ``12n`` — and both accounts
    are annual constructions struck there.
    """
    k_rb = int(model_point()["aufschub_y"]) - 1
    return av_pp_at(k_rb, "AFT_INT") + av_sur_pp_at(k_rb, "AFT_INT")


def val_reserve_pp():
    """The *Bewertungsreserven* crystallised at the *Rentenbeginn*, per policy.

    ``val_reserve_rate x capital_gross_pp()``, 1,5 % **[std]**.  The mechanic is cited twice
    over — participation in the *Bewertungsreserven* is *hälftig* under § 153 Abs. 3 VVG and
    the transition to annuity payment is a key point for it — and **no amount, ratio or
    reserve level was established anywhere**, so the rate is a placeholder sized to be visible
    without dominating.  Policyholders also participate during the payout phase; that
    continuing participation is not modelled.
    """
    return (float(data.param_table().at["val_reserve_rate", "value"])  # noqa: F821
            * capital_gross_pp())


def capital_conv_pp():
    """K: the conversion capital per policy, ``max(guar_capital_pp, capital_gross + val_reserve)``.

    The contract value used for annuitisation, including *Überschussbeteiligung* and
    *Bewertungsreserven*, **subject to a minimum guaranteed contract value** stated in the
    general contract data.  The floor is inoperative on the anchor cell, whose
    ``guar_capital_pp`` is nil, and binds on point 13.

    The commuting policyholders receive this same amount: the corpus gives no basis for paying
    them less than the annuitants convert, and inventing one would be a charge no source
    supports.
    """
    return max(float(model_point()["guar_capital_pp"]),
               capital_gross_pp() + val_reserve_pp())


def annuity_rate_guar():
    """f_g: the *garantierter Rentenfaktor*, in euro a month per 10 000 € of capital.

    Fixed **at inception** on the tariff bases — a recognised mortality table (DAV 2004 R) and
    an interest basis the carrier chooses, in the one document that states it below the
    then-current *Höchstrechnungszins*.  A model-point attribute, because it is a property of
    the contract's vintage and not of the projection.  It is a floor, not the applied factor.
    """
    return float(model_point()["annuity_rate_guar"])


def annuity_rate_curr():
    """f_c: the *aktueller Rentenfaktor* at the annuitant's attained age at *Rentenbeginn*.

    Read from *rentenfaktor_table.csv* at ``(rf_scenario_id, issue_age + aufschub_y)``.
    German insurers derive the current factor of a deferred contract from the tariff they are
    then writing for **immediately beginning annuities**, which is why the immediate-annuity
    document is the direct evidence for the deferred contract's conversion basis.  Every level
    here is **[std]**: no market factor was established for any carrier in any year.
    """
    mp = model_point()
    return float(data.rentenfaktor_table().at[                       # noqa: F821
        (mp["rf_scenario_id"], int(mp["issue_age"]) + int(mp["aufschub_y"])),
        "annuity_rate_curr"])


def annuity_rate_appl():
    """f: the applied *Rentenfaktor*, ``max(annuity_rate_guar(), annuity_rate_curr())``.

    At the start of annuity payments a second *Rentenfaktor* is compared with the guaranteed
    one and **the higher of the two is guaranteed for the annuity payment period**.  That
    ``max`` is a written option on the insurer's own future annuity tariff, and the
    deterministic path does not price it.

    Both branches ship: 32,00 € on the anchor cell, where the current factor wins over a
    guaranteed 28,00 €, and the guarantee binding on point 13.  A model applying the
    guaranteed factor alone understates the anchor cell's annuity by 12,5 %.
    """
    return max(annuity_rate_guar(), annuity_rate_curr())


def annuity_guar_mth_pp():
    """G: the *garantierte Rente*, monthly, per policy.

    ``capital_conv_pp() / 10 000 x annuity_rate_appl()`` — the conversion rule in one line.
    Struck once, at the *Rentenbeginn*, and level for life thereafter; only this part is
    guaranteed, the *Überschussrente* beside it is not.
    """
    return capital_conv_pp() / 10000.0 * annuity_rate_appl()


def annuity_sur_mth_pp(k):
    """U(k): the *Überschussrente*, monthly, per policy, by *Überschussverwendung*.

    The argument is the **policy year**, because all three escalations are annual: an
    *Überschussrente* is redeclared once a year and steps on the anniversary, so the twelve
    instalments of a payout year are equal and the monthly grid refines when they are *paid*
    rather than what they are.

    ``konstant``
        ``sur_ann_rate x G``, level.  Set from a whole-period projection at outset and
        falling if the insurer earns less.

    ``volldynamisch``
        ``G x ((1 + sur_ann_growth)^j - 1)`` with ``j = k - n`` the completed payout years:
        nil in the first payout year and rising with actual surplus development thereafter.

    ``teildynamisch``
        ``theta sur_ann_rate G + G ((1 + theta sur_ann_growth)^j - 1)``: a stated combination
        of the two, half of each at ``theta = 0.5``.

    The three systems and their *directions* are established; **no level, rate or split was
    established for any of them**, so all three parameters are **[std]**.
    """
    mp = model_point()
    n = int(mp["aufschub_y"])
    if k < n:
        return 0.0
    par = data.param_table()                                         # noqa: F821
    rate = float(par.at["sur_ann_rate", "value"])
    growth = float(par.at["sur_ann_growth", "value"])
    theta = float(par.at["sur_ann_theta", "value"])
    j = k - n
    system = mp["payout_system"]
    guar = annuity_guar_mth_pp()
    if system == "konstant":
        return rate * guar
    if system == "volldynamisch":
        return guar * ((1.0 + growth) ** j - 1.0)
    if system == "teildynamisch":
        return (theta * rate * guar
                + guar * ((1.0 + theta * growth) ** j - 1.0))
    raise ValueError("invalid payout_system")


def annuity_pp(t):
    """The annuity instalment per policy in month t: ``G + U(k)``, zero before the *Rentenbeginn*.

    **The *Rente* is monthly, and is now paid monthly.**  The *Rentenfaktor* is quoted in euro
    a month per 10 000 € of capital and every carrier document in the corpus states the annuity
    that way, so this is where the product's central quantity finally appears undisguised.  The
    annual-step model this replaced paid ``12 x (G + U)`` at the **start** of each payout year,
    a compression carried as a **[std]** that was generous to the payout phase by roughly half
    a year's interest on a year's annuity, every year, and by a full year of survivorship on
    instalments a decedent did not live to collect.  **That standardization is gone**, and with
    it the only place in this model where a stated payment frequency was not the one modelled.

    The instalment is paid **in advance**, at the beginning of the month, on the count
    :func:`pols_annuity` gives.  ``U`` steps once a year, on the anniversary, because the
    *Überschussrente* is redeclared annually.

    No administration charge is deducted.  ``annuity_admin_rate`` ships in the charge table at
    1,5 % and is **not applied**: the *Rentenfaktor* is exogenous here and already carries the
    tariff's payout loading, so deducting again would charge it twice.
    """
    if duration(t) < int(model_point()["aufschub_y"]):
        return 0.0
    return annuity_guar_mth_pp() + annuity_sur_mth_pp(duration(t))


def annuity_payments(t):
    """The annuity outgo in month t: ``annuity_pp(t) x pols_annuity(t)``.

    Weighted by the count the instalment is *paid on*, which inside the *Rentengarantiezeit*
    is the annuitised count and not the survivors.
    """
    return annuity_pp(t) * pols_annuity(t)


def annuity_due_factor():
    """A **diagnostic**: the annuity-due factor on the shipped proxy at the guarantee basis.

    ``sum over the payout **months** of v^(s/12) x s/12 p_x`` with
    ``v = 1 / (1 + int_rate_guar())`` and survivorship from :func:`mort_rate_mth`, evaluated at
    the annuitant's attained age at *Rentenbeginn*.  **No cash flow reads it.**

    It is a **monthly** annuity-due factor because the annuity is monthly, which is what the
    monthly grid finally lets it be: the implied *Rentenfaktor* is now
    ``10 000 / annuity_due_factor()`` with no twelve in it, where the annual-step model needed
    ``10 000 / (12 x annuity_due_factor())`` and carried the in-advance approximation the
    twelve stood for.

    It exists because this model publishes a **[std]** *Rentenfaktor* and a **[std]** annuity
    table, and those two are **not calibrated to each other**.  The *Rentenfaktor* is
    authoritative: it fixes the benefit amount, while the mortality proxy fixes only how long
    that amount is paid.  Publishing the factor the proxy would imply makes the gap visible
    rather than hidden.  Anyone substituting a real DAV 2004 R must re-strike the
    *Rentenfaktoren* with it or accept an inconsistency the model will not flag.
    """
    n_mth = 12 * int(model_point()["aufschub_y"])
    disc = (1.0 / (1.0 + int_rate_guar())) ** (1.0 / 12.0)
    surv = 1.0
    total = 0.0
    for s in range(n_mth, proj_len()):
        total = total + surv * disc ** (s - n_mth)
        surv = surv * (1.0 - mort_rate_mth(s))
    return total


# ----------------------------------------
# Claims, expenses and the cash flow statement


def claims(t, kind=None):
    """Benefit outgo in **month** t, by kind; the total when kind is omitted.

    The **counts are monthly and the amounts are annual**, which is the whole shape of this
    conversion in one cells: a claim is recognised in the month it happens, and what it is paid
    is the value struck at the end of that *Versicherungsperiode* — § 169 Abs. 3 VVG's *zum
    Schluss der laufenden Versicherungsperiode*, the year for this tariff, and the year the
    *Beitrag* was paid in advance for.

    ``"DEATH"``
        ``db_pp(duration(t)) x pols_death(t)``.  **Zero after the *Rentenbeginn***, where
        ``db_pp`` is zero.

    ``"LAPSE"``
        ``cv_pp(duration(t)) x pols_lapse(t)``, the surrender value on the survivors of the
        month's deaths.  Zero in the payout phase, where there is no surrender.

    ``"COMMUTATION"``
        ``capital_conv_pp() x pols_commutation(t)``, the *Kapitalabfindung* under the
        *Kapitalwahlrecht*, paid in the last accumulation month ``12n - 1`` and in no other.
        The commuters receive the same capital the annuitants convert, *Bewertungsreserven*
        included.

    The annuity itself is **not** a claim kind: it is a recurring benefit with its own
    weighting rule and is published as :func:`annuity_payments`.
    """
    if kind is None:
        return sum(claims(t, j) for j in ("DEATH", "LAPSE", "COMMUTATION"))
    if kind == "DEATH":
        return db_pp(duration(t)) * pols_death(t)
    if kind == "LAPSE":
        return cv_pp(duration(t)) * pols_lapse(t)
    if kind == "COMMUTATION":
        return capital_conv_pp() * pols_commutation(t)
    raise ValueError("invalid kind")


def expense_acq_pp():
    """The acquisition expense per policy at issue, from *param_table.csv*: 400,00 € **[std]**."""
    return float(data.param_table().at["expense_acq_pp", "value"])   # noqa: F821


def expense_maint_pp():
    """The maintenance expense per policy per year in the accumulation phase: 45,00 € **[std]**."""
    return float(data.param_table().at["expense_maint_pp", "value"])  # noqa: F821


def expense_annuity_pp():
    """The administration expense per policy per year in the payout phase: 30,00 € **[std]**."""
    return float(data.param_table().at["expense_annuity_pp", "value"])  # noqa: F821


def expense_claim_pp():
    """The settlement expense per death, surrender or commutation event: 120,00 € **[std]**."""
    return float(data.param_table().at["expense_claim_pp", "value"])  # noqa: F821


def expense_infl():
    """The annual expense inflation rate: 2,0 % p.a. **[std]**."""
    return float(data.param_table().at["expense_infl", "value"])     # noqa: F821


def expenses_pp(t):
    """The per-policy administration expense in **month** t, inflated: a twelfth of the year's.

    ``expense_maint_pp()`` in the accumulation phase and ``expense_annuity_pp()`` in the payout
    phase, **divided by twelve** and times ``(1 + expense_infl())^duration(t)``.

    Two decisions are stated by that formula.  The level is a twelfth of the annual amount
    rather than a monthly amount of its own, so a year of it on a closed cohort is exactly the
    annual-step model's charge; and the **inflation factor steps on the anniversary**, not
    monthly, because it compounds from inception in policy years and a twelfth-rooted inflation
    would be a different assumption wearing the same number.  The expense of a policy that
    leaves mid-year is now borne only for the months it was there, which is the refinement the
    finer grid buys here.
    """
    level = (expense_maint_pp() if duration(t) < int(model_point()["aufschub_y"])
             else expense_annuity_pp())
    return level / 12.0 * (1.0 + expense_infl()) ** duration(t)


def expenses(t):
    """The insurer's own outgo in period t: acquisition, administration and settlement.

    Acquisition falls once, in the frame's first **month** and only for new business — an
    in-force model point's acquisition cost was incurred before the valuation date.
    Administration is per policy per month on the exposed count, which is ``pols_if(t)`` while
    premiums accumulate and ``pols_annuity(t)`` once the annuity is in payment.  Settlement
    falls on every death, surrender and commutation, in the month it happens.

    **These are expenses, not charges.**  The *Kostenbeiträge* the tariff deducts —
    ``charge_acq_pp``, ``charge_prem_pp``, ``charge_admin_pp``, ``charge_risk_pp`` — move
    money inside the contract and are not here: ``expenses(t)`` is invariant to ``beta_rate``
    and ``gamma_rate`` while ``av_pp(t+1)`` is not.  Booking the charges as expenses inflates
    outgo by the whole charge load and is the commonest way to make a German model look
    conservative.
    """
    mp = model_point()
    n_mth = 12 * int(mp["aufschub_y"])
    out = 0.0
    if t == t_start() and k_start() == 0:
        out = out + expense_acq_pp() * pols_if(t)
    out = out + expenses_pp(t) * (pols_if(t) if t < n_mth else pols_annuity(t))
    out = out + expense_claim_pp() * (pols_death(t) + pols_lapse(t)
                                      + pols_commutation(t))
    return out


def net_cf(t):
    """The net liability cash flow of period t, **income positive**.

    ``premiums - claims_death - claims_lapse - claims_commutation - annuity_payments -
    expenses``.  The six components are exactly the six that cross the contract boundary; the
    account movements beside them in :func:`result_cf` — ``prem_to_av``, ``int_credited``,
    ``bonus_credited`` — are internal and are reported, not summed.

    The shape to expect on the anchor cell is strongly positive in the first month of each
    accumulation year and mildly negative in the other eleven, a large negative spike at
    ``t = 203`` where the *Kapitalabfindung* falls, and a long negative annuity tail thereafter.
    """
    return (premiums(t) - claims(t, "DEATH") - claims(t, "LAPSE")
            - claims(t, "COMMUTATION") - annuity_payments(t) - expenses(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside :func:`net_cf` so the sign convention is verifiable
    in the frame rather than only in prose.
    """
    return -net_cf(t)


# ----------------------------------------
# The published identities


def check_net_cf_resid(t):
    """The cash-flow-statement residual in month t; zero everywhere.

    ``net_cf`` as published in :func:`result_cf`, less the same frame's own
    ``premiums - claims_death - claims_lapse - claims_commutation - annuity_payments -
    expenses``.  It is rebuilt **from the frame** rather than from the cells, so it fails if a
    published column and the headline number ever stop being the same arithmetic — which is
    the failure the identity exists to catch.
    """
    row = result_cf().loc[t]
    rebuilt = (row["premiums"] - row["claims_death"] - row["claims_lapse"]
               - row["claims_commutation"] - row["annuity_payments"]
               - row["expenses"])
    return float(row["net_cf"]) - float(rebuilt)


def check_net_cf():
    """True when the published cash flow statement reconciles in every projected year.

    delib's first ruling: every model in this library publishes the identity that
    reconstructs its headline number from the statement's own parts, so that ``net_cf`` is not
    the one quantity nothing checks.  It also asserts ``liability_cf(t) == -net_cf(t)``
    exactly, which is the library-wide sign convention.
    """
    for t in result_cf().index:
        scale = max(1.0, abs(premiums(t)) + abs(claims(t))
                    + abs(annuity_payments(t)) + abs(expenses(t)))
        if abs(check_net_cf_resid(t)) > roll_fwd_tol() * scale:
            return False
        if abs(liability_cf(t) + net_cf(t)) > roll_fwd_tol() * scale:
            return False
    return True


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - pols_death(t) - pols_lapse(t) - pols_commutation(t)``.  The
    recursion and the three exits are formed separately, so they agree by algebra when — and
    only when — every one of them is read at the same ``t``.  What it catches is a misindexed
    recursion: rolling forward with ``w(t-1)``, or dropping the commutation from the recursion
    while still paying the *Kapitalabfindung*, both leave a residual here.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t)
            - pols_lapse(t) - pols_commutation(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes and ``pols_if`` stays non-negative."""
    tol = roll_fwd_tol() * max(pols_if_init(), 1.0)
    for t in result_cf().index:
        if abs(check_pols_roll_fwd_resid(t)) > tol:
            return False
        if pols_if(t) < -tol:
            return False
    return True


def check_decrement_closure_resid(t):
    """The cumulative decrement-closure residual at the end of period t; zero.

    The deaths, surrenders and commutations up to and including ``t``, plus ``pols_if(t+1)``,
    less the original cohort.  Built by **direct summation over the exit cells**, with no
    reference to the recursion that produced ``pols_if``, which is what makes it more than the
    telescope of :func:`check_pols_roll_fwd`: it catches a wrong starting cohort, an exit
    counted in two places, and a policy that commutes at the *Rentenbeginn* and reappears in
    the annuity — the arithmetic form of paying the capital twice.

    At the last row ``t = proj_len() - 1`` it closes on ``pols_if_init()`` exactly with
    ``pols_if(proj_len()) = 0``, because ``mort_rate`` is 1 in the policy year at attained age
    ``omega_age() - 1``.  A projection truncated before then would fail here rather than
    silently drop the annuity tail.
    """
    exits = sum(pols_death(s) + pols_lapse(s) + pols_commutation(s)
                for s in range(t_start(), t + 1))
    return exits + pols_if(t + 1) - pols_if_init()


def check_decrement_closure():
    """True when exits and survivors account for the whole cohort at every projected t."""
    tol = roll_fwd_tol() * max(pols_if_init(), 1.0)
    return all(abs(check_decrement_closure_resid(t)) <= tol
               for t in result_cf().index)


def check_av_roll_fwd_resid(k):
    """The *Deckungskapital* roll-forward residual in policy **year** k; zero everywhere.

    ``av(k) + prem_to_av(k) - charge_from_av(k) + int_credited(k) + pup_uplift(k) -
    av_release(k) - av(k+1)``, at fund level.

    It ties the account to the cash flow statement: the *Sparbeitrag* that left the premium
    must arrive here, the charge the premium could not meet must leave here, and the balance
    the leavers took with them must equal what the death and surrender claims paid out.  It
    closes across the *Beitragsfreistellung* reset only because :func:`pup_uplift` is
    published, and across the *Rentenbeginn* only because the whole balance is released there.

    **It is an annual identity and it is stated annually**, one residual per policy year rather
    than one per month.  The *Deckungskapital* of this tariff is defined at anniversaries; a
    monthly residual for it would first have had to invent a monthly reserve, which is the
    error the two-clock split exists to make impossible.  Every term is weighted at the
    anniversary counts ``pols_if(12k)`` and ``pols_if(12(k+1))``, so the identity closes on the
    same numbers the annual-step model closed on.
    """
    return (av(k) + prem_to_av(k) - charge_from_av_pp(k) * pols_if(12 * k)
            + int_credited(k) + pup_uplift(k) - av_release(k) - av(k + 1))


def check_av_roll_fwd():
    """True when the *Deckungskapital* rolls forward exactly in every projected policy year."""
    for k in range(k_start(), proj_len_y()):
        scale = max(1.0, abs(av(k)), abs(av(k + 1)), abs(prem_pp(k)))
        if abs(check_av_roll_fwd_resid(k)) > roll_fwd_tol() * scale:
            return False
    return True


def check_av_sur_roll_fwd_resid(k):
    """The *Ansammlungsguthaben* roll-forward residual in policy **year** k; zero everywhere.

    ``av_sur(k) + bonus_credited(k) - av_sur_release(k) - av_sur(k+1)``.  Nothing else touches
    the side account: no premium is credited to it, no charge is taken from it, and it is
    untouched by a *Beitragsfreistellung*.  A model that credited the declared rate to the
    *Deckungskapital* as well as here would leave a residual at every k.
    """
    return (av_sur(k) + bonus_credited(k) - av_sur_release(k)
            - av_sur(k + 1))


def check_av_sur_roll_fwd():
    """True when the *Ansammlungsguthaben* rolls forward exactly in every projected year."""
    for k in range(k_start(), proj_len_y()):
        scale = max(1.0, abs(av_sur(k)), abs(av_sur(k + 1)), abs(av(k)))
        if abs(check_av_sur_roll_fwd_resid(k)) > roll_fwd_tol() * scale:
            return False
    return True


def check_prem_split_resid(k):
    """The premium-decomposition residual in policy **year** k; zero everywhere.

    Two identities in one number, the larger in absolute value being returned:
    ``prem_pp = prem_to_av_pp + charge_from_prem_pp`` — every euro of premium is either saved
    or spent on a charge — and ``charge_due_pp = charge_from_prem_pp + charge_from_av_pp`` —
    every euro of charge is met either from the premium or from the account.  Together they
    are what stops a charge from being taken twice or from vanishing.
    """
    a = prem_pp(k) - prem_to_av_pp(k) - charge_from_prem_pp(k)
    b = charge_due_pp(k) - charge_from_prem_pp(k) - charge_from_av_pp(k)
    return a if abs(a) >= abs(b) else b


def check_prem_split():
    """True when the premium and the charge both decompose exactly in every projected year."""
    for k in range(k_start(), proj_len_y()):
        scale = max(1.0, abs(prem_pp(k)), abs(charge_due_pp(k)))
        if abs(check_prem_split_resid(k)) > roll_fwd_tol() * scale:
            return False
    return True


def check_cv_floor_resid(k):
    """The surrender-value residual in policy year k: ``cv_pp - max(cv_tariff_pp, cv_floor_pp)``.

    Zero everywhere by construction; what the companion :func:`check_cv_floor` adds is the
    one-sided assertion that the value never falls below the § 169 Abs. 3 floor however large
    the *Stornoabzug* is set — which is the statutory content, since a deduction in respect of
    unamortised acquisition costs is void.  Annual, like the value it checks.
    """
    return cv_pp(k) - max(cv_tariff_pp(k), cv_floor_pp(k))


def check_cv_floor():
    """True when the surrender value is the floored tariff value in every projected year."""
    for k in range(k_start(), proj_len_y()):
        scale = max(1.0, abs(cv_pp(k)))
        if abs(check_cv_floor_resid(k)) > roll_fwd_tol() * scale:
            return False
        if cv_pp(k) < cv_floor_pp(k) - roll_fwd_tol() * scale:
            return False
    return True


def check_annuity_conv_resid(t):
    """The conversion residual: ``annuity_guar_mth_pp x 10 000 - capital_conv_pp x f``.

    A scalar identity — the conversion is struck once, at the *Rentenbeginn* — evaluated at
    every ``t`` so that it has the same shape as the other checks.  ``f`` is rebuilt here as
    ``max(annuity_rate_guar(), annuity_rate_curr())`` rather than read from
    :func:`annuity_rate_appl`, so the check is independent of the cells it is checking.
    """
    return (annuity_guar_mth_pp() * 10000.0
            - capital_conv_pp() * max(annuity_rate_guar(), annuity_rate_curr()))


def check_annuity_conv():
    """True when the *Rentenbeginn* conversion obeys all three of its rules.

    The conversion arithmetic itself; that the applied *Rentenfaktor* is never below the
    guaranteed one, which is the whole content of ``max(garantierter, aktueller)``; and that
    the conversion capital is never below the minimum guaranteed contract value stated in the
    general contract data.
    """
    scale = max(1.0, abs(capital_conv_pp()))
    tol = roll_fwd_tol() * scale * 10000.0
    if abs(check_annuity_conv_resid(result_cf().index[0])) > tol:
        return False
    if annuity_rate_appl() < annuity_rate_guar() - roll_fwd_tol():
        return False
    if capital_conv_pp() < float(model_point()["guar_capital_pp"]) - roll_fwd_tol() * scale:
        return False
    return True


def check_annuity_guarantee_resid(t):
    """The *Rentengarantiezeit* weighting residual in period t; zero everywhere.

    ``pols_annuity(t)`` less
    ``max(pols_if(t), 1{12n <= t < 12n + 12m} x pols_annuitization(12n - 1))``, which is zero
    before the *Rentenbeginn*.  Stating the identity with the ``max`` is what makes it
    independent of the definition it checks: it holds because
    ``pols_if(t) <= pols_annuitization(12n - 1)`` throughout the payout phase, so a model that
    weighted the guaranteed months by survivors would fail here at every ``t`` inside the
    window where a death has occurred.
    """
    mp = model_point()
    n_mth = 12 * int(mp["aufschub_y"])
    if t < n_mth:
        return pols_annuity(t)
    guaranteed = (pols_annuitization(n_mth - 1)
                  if t < n_mth + 12 * int(mp["rgz_years"]) else 0.0)
    return pols_annuity(t) - max(pols_if(t), guaranteed)


def check_annuity_guarantee():
    """True when the annuity is weighted by the annuitised count inside the guarantee period."""
    tol = roll_fwd_tol() * max(pols_if_init(), 1.0)
    return all(abs(check_annuity_guarantee_resid(t)) <= tol
               for t in result_cf().index)


# ----------------------------------------
# Output


def result_cf():
    """Result table of **monthly** cash flows, indexed by the 0-based policy month t.

    The frame runs from the model point's first projected month — ``t = 0`` for new business,
    ``t = t_start()`` for an in-force point — to ``proj_len() - 1``, contiguously;
    ``proj_len()`` is the exclusive end, as in lifelib's ``range(proj_len())``.  852 rows on
    the anchor cell.

    ``pols_if`` is the start-of-month count and the weight on every cash flow of the same row;
    ``pols_annuity`` is the count the annuity instalment is paid on, which differs inside the
    *Rentengarantiezeit*.  The six columns that cross the contract boundary are ``premiums``,
    the three ``claims_*``, ``annuity_payments`` and ``expenses``, and those six are exactly
    what :func:`check_net_cf` reconciles.  ``liability_cf`` is ``net_cf`` outgo-positive.

    **The account movements are not here.**  ``av``, ``av_sur``, ``prem_to_av``,
    ``int_credited`` and ``bonus_credited`` move once a policy year, so they live in
    :func:`result_pols` with the rest of the annual state: a state table that moves once a year
    should not be printed twelve times over, and a cash flow statement whose columns do not all
    sum to its bottom line is one a reader has to know which columns to skip.
    :func:`result_cf_annual` sums this frame into policy years.
    """
    ts = list(range(t_start(), proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_annuity": [pols_annuity(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_commutation": [claims(t, "COMMUTATION") for t in ts],
            "annuity_payments": [annuity_payments(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by the 1-based ``policy_year``.

    A **regrouping of the monthly frame and never a second projection**: every cash flow column
    is the sum of that policy year's twelve months, while ``pols_if`` and ``pols_annuity`` are
    the counts at the year's **start**, which is the only reading under which a count and a
    flow can share a row.  This is the view the technical notes' worked example is stated on.
    """
    df = result_cf()
    years = pd.Index([duration(t) + 1 for t in df.index],            # noqa: F821
                     name="policy_year")
    counts = ["pols_if", "pols_annuity"]
    out = df.drop(columns=counts).groupby(years).sum()
    for i, column in enumerate(counts):
        out.insert(i, column, df[column].groupby(years).first())
    return out


def result_pols():
    """The **annual** state behind the monthly cash flows, indexed by the 1-based policy year.

    Everything on this product that moves once a year and on the anniversary: the two mortality
    bases side by side, the surrender rate, the premium and its decomposition, the three
    account balances per policy and at fund level, the year's credits, the surrender value with
    its two branches, the death benefit and the annuity instalment.  Nothing here is a monthly
    quantity, and nothing here changed when the grid did — the account movements are weighted
    at the anniversary counts, so this table is row for row the one the annual-step model
    published.

    ``mort_rate`` and ``lapse_rate`` are the **annual** rates the notes tabulate; the rates the
    recursion applies are ``mort_rate_mth`` and ``lapse_rate_mth``, which belong to the monthly
    frame and are not printed here.
    """
    ks = list(range(k_start(), proj_len_y()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(12 * k) for k in ks],
            "mort_rate_guar": [mort_rate_guar(12 * k) for k in ks],
            "mort_rate": [mort_rate(12 * k) for k in ks],
            "lapse_rate": [lapse_rate(12 * k) for k in ks],
            "prem_pp": [prem_pp(k) for k in ks],
            "charge_due_pp": [charge_due_pp(k) for k in ks],
            "prem_to_av_pp": [prem_to_av_pp(k) for k in ks],
            "av_pp": [av_pp(k) for k in ks],
            "av_sur_pp": [av_sur_pp(k) for k in ks],
            "av_spread_pp": [av_spread_pp(k) for k in ks],
            "av": [av(k) for k in ks],
            "av_sur": [av_sur(k) for k in ks],
            "prem_to_av": [prem_to_av(k) for k in ks],
            "int_credited": [int_credited(k) for k in ks],
            "bonus_credited": [bonus_credited(k) for k in ks],
            "cv_tariff_pp": [cv_tariff_pp(k) for k in ks],
            "cv_floor_pp": [cv_floor_pp(k) for k in ks],
            "cv_pp": [cv_pp(k) for k in ks],
            "db_pp": [db_pp(k) for k in ks],
            "annuity_pp": [annuity_pp(12 * k) for k in ks],
        },
        index=pd.Index([k + 1 for k in ks], name="policy_year"),     # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

pd = ("Module", "pandas")
