# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.TD_FR_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **policy months**, 0-based, the clock ``basiclife.BasicTerm_S`` and the five
monthly frlib models run on: ``t = 0`` is the first policy month, month ``t`` runs from
time ``t`` to time ``t + 1``, ``pols_if(t)`` is the count at time ``t`` (so
``pols_if(0) == pols_if_init()``), and the frame is ``t = 0, 1, ..., proj_len() - 1``
with ``proj_len() = 12 * (cover_end_age() - issue_age())`` the **number** of projected
months — the exclusive end of the frame, so the loop is lifelib's
``for t in range(proj_len())``. Within a month the cotisation instalment, the maintenance
expense and the commission fall at the **beginning**; deaths and PTIA claims at the
**end**, settled there; lapses at the end, after both insured decrements.

Everything *contractual* about this product is nevertheless on an **annual** cycle — the
one-year risk renewed by *tacite reconduction*, the repricing at the new attained age,
the benefit schedule, the art. L. 132-7 suicide year, the first-year commission rate and
the ``constante`` equivalence — and the model keeps all of them there. So the policy year
is derived and used as a lookup key throughout: ``duration_mth(t) = t`` is the completed
policy months at the start of month ``t``, ``duration(t) = duration_mth(t) // 12`` the
completed policy years, ``policy_year(t) = duration(t) + 1`` the contractual 1-based
label, and the attained age is ``age(t) = issue_age() + duration(t)``, stepping on the
anniversary and not monthly. The frame is indexed by ``t``; the policy year is derived
and never indexed by. There is nothing after the frame — cover ceases at the *échéance*
following ``cover_end_age``, nothing is payable there, and there is no maturity value, no
renewal and no conversion.

The two-speed structure that follows is the library's convention, asserted by
``tests/test_model_conventions_fr.py``: :func:`mort_rate`, :func:`ptia_rate` and
:func:`lapse_rate` are the **annual** rates of the policy year containing month ``t`` —
the vectors the technical notes tabulate — and :func:`mort_rate_mth`,
:func:`ptia_rate_mth` and :func:`lapse_rate_mth` are the monthly rates actually applied,
derived at ``1 - (1 - r)^(1/12)`` so that twelve of them compound back to exactly the
year's rate. :func:`result_cf_annual` sums the monthly frame into policy years, which is
the view the notes' worked example is stated on.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/temporaire_deces/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``TD_FR_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.TD_FR_S.Data`, reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
premium_rate_file         data.premium_rate_table()          premium_rate_table.csv
mort_table_file           data.mort_table()                  mort_table.csv
lapse_file                data.lapse_table()                 lapse_table.csv
freq_loading_file         data.freq_loading_table()          freq_loading_table.csv
benefit_schedule_file     data.benefit_schedule()            benefit_schedule.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` wherever that model has an
analogue — ``pols_*`` for policy counts, plural nouns for cash flows, ``*_rate`` for
**annual** rates and ``*_rate_mth`` for the monthly ones derived from them, ``*_pp`` for
per-policy amounts, ``claims(t, kind)`` with an uppercase ``kind`` string,
``pols_if_at(t, timing)`` for the within-month in-force reads — and, for the monthly
grid, the ``duration_mth`` / ``duration`` / ``policy_year`` triple that ``Obseques_FR_S``,
``ADE_FR_S`` and ``savings.CashValue_SE`` use. The technical notes use compact actuarial
symbols instead. The mapping is:

=========================  ==============================  ==========================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==========================
(none)                     model_point()                   The selected model point row
n = cover - issue          proj_len_y()                    Number of projected years
t = 0..12n-1               proj_len()                      Number of projected months
(none)                     duration_mth(t)                 Months elapsed at BOM, = t
dur(t)                     duration(t)                     Completed policy years, t // 12
y = dur(t) + 1             policy_year(t)                  Policy year, the 1-based label
x(t)                       age(t)                          Attained age of month t's year
SA                         sum_assured()                   Guaranteed capital
r(x)                       prem_rate(t)                    Tariff rate at that age
(table)                    mort_rate_base(t)               Table death rate at that age
f                          rating_factor()                 Surprime multiplier
phi                        prem_freq_load()                Fractionation multiplier
F                          prem_freq_fee()                 Fixed annual frais d'echeance
P_tar(t) = SA r(x) f phi   prem_tariff_pp(t)               Tariff cotisation, before F
P_lev                      prem_level_pp()                 Level cotisation, constante
P(t) = P_tar(t) + F        prem_pp(t)                      Annual cotisation of the year
(instalments)              prem_instalments()              Instalments per policy year
(modal cycle)              prem_cycle()                    Months between instalments
(due month)                prem_due(t)                     Is an instalment due at BOM
P_inst(t)                  prem_inst_pp(t)                 Instalment collected in month t
v                          disc_factor(y)                  (1 + tech_rate)^-y, y a year
p_tau(y)                   pols_tariff(y)                  Tariff survivorship, no lapse
(denominator)              tariff_annuity()                Sum of v^y p_tau(y)
(numerator)                tariff_prem_pv()                PV of the revisable stream
(schedule)                 benefit_factor(t)               Benefit schedule factor
B(t)                       benefit_pp(t)                   Contractual capital in period t
(none)                     benefit_death_pp(t)             What a death claim pays
(none)                     benefit_ptia_pp(t)              What a PTIA claim pays
(none)                     prem_refund_pp(t)               Cotisations returned in the
                                                           delai d'attente
(none)                     accident_extra_pp(t)            Additional accidental capital
sigma(t)                   suicide_factor(t)               First-year death exclusion
q_d(t)                     mort_rate(t)                    Annual dependent death rate
q_p(t)                     ptia_rate(t)                    Annual dependent PTIA rate
q_d(t) + q_p(t)            decr_rate(t)                    Annual insured decrement
q_m(t)                     decr_rate_mth(t)                Monthly insured decrement
q_dm(t)                    mort_rate_mth(t)                Monthly death rate applied
q_pm(t)                    ptia_rate_mth(t)                Monthly PTIA rate applied
(tariff basis)             ptia_rate_base(t)               PTIA rate before the loading
(table)                    lapse_rate_base(t)              Annual table lapse rate
M_shock(t)                 shock_lapse_factor(t)           Premium-shock multiplier
w(t)                       lapse_rate(t)                   Annual lapse rate of the year
w_m(t)                     lapse_rate_mth(t)               Monthly lapse rate applied
w_cum(t)                   lapse_cum(t)                    Cumulative lapse proportion
lambda                     sel_lapse_lambda                Selective-lapsation loading
w_ref                      sel_lapse_ref                   Selective-lapsation threshold
(none)                     sel_lapse_factor(t)             Mortality loading on persisters
l(t)                       pols_if(t)                      In force at the start of month t
l(t)(1-q), l(t+1)          pols_if_at(t, timing)           BEF_DECR / BEF_LAPSE / AFT_DECR
pols_death(t)              pols_death(t)                   Expected deaths in month t
pols_ptia(t)               pols_ptia(t)                     Expected PTIA claims in month t
pols_lapse(t)              pols_lapse(t)                   Expected lapses in month t
premiums(t)                premiums(t)                     Cotisation income
claims_death, claims_ptia  claims(t, kind)                 Benefit outgo by kind
ec x (D + P)               claim_expenses(t)               Claim handling expense
(none)                     inflation_factor(t)             Expense inflation factor
c0, c_r                    commissions(t)                  Commission outgo
E0, e(t), ec, commission   expenses(t)                     Total expense, incl. commission
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
(none)                     result_cf_annual()              result_cf() summed into years
=========================  ==============================  ==========================

Six names needed care.

``P(t)`` in the notes is the cotisation actually charged, which on the ``revisable``
form is ``SA r(x(t)) f phi`` and on the ``constante`` form is a level ``P_lev``. Both
then carry the fixed *frais d'échéance*. :func:`prem_tariff_pp` is the tariff amount,
:func:`prem_level_pp` the level one and :func:`prem_pp` what is charged, so the three
have somewhere to live and the fee is added exactly once — the notes' pitfall 13, which
is about applying the fractionation *loading* and the fee both as percentages.

``q_d(t)`` and ``q_p(t)`` are **dependent** rates of a two-decrement table, not
independent single-decrement rates, so they are additive: ``l(t+1) = l(t)(1 - q_d -
q_p)(1 - w)``. An implementation using ``1 - (1 - q_d)(1 - q_p)`` gets 0.00479680
against 0.00480000 in the first year of the worked configuration — immaterial there,
material at older ages. :func:`mort_rate_base` is the table rate and :func:`mort_rate` the rate
applied after the selective-lapsation loading; :func:`ptia_rate_base` is the tariff-basis
PTIA rate that the ``constante`` equivalence is struck on, and :func:`ptia_rate` the one
the projection applies. Keeping the two pairs apart is also what keeps the level-premium
derivation acyclic: the equivalence is struck on the tariff basis, so it cannot depend on
a behavioural loading that depends on the lapse path that depends on the premium.

``q_d`` and ``q_p`` being additive is also why they are converted to the month
**together** and split afterwards rather than converted apart. :func:`decr_rate` is their
sum, :func:`decr_rate_mth` is ``1 - (1 - q_d - q_p)^(1/12)``, and :func:`mort_rate_mth` /
:func:`ptia_rate_mth` are that rate split in the two rates' own proportion. Converting
each rate separately and adding the results gives a twelve-month insured survival of
0.9952029339 against the annual model's 0.9952000000 at the anchor cell — an error of
2.6e-6 at the very first anniversary and 1.0e-5 in ``pols_if`` over the run, which is
what would break the anniversary equivalence. The proportional split also keeps
``ptia_rate_mth / mort_rate_mth = ptia_ratio`` exactly, so the acceleration ratio the
product is built on survives the conversion untouched.

``B(t)`` is the *contractual* capital. What a claim actually pays is not always ``B(t)``:
inside a *délai d'attente* an illness-caused death pays back the cotisations collected
and PTIA pays nothing, and in policy year 1 (``t = 0``) the death cover is void for
suicide. So
:func:`benefit_pp` is ``B(t)``, :func:`benefit_death_pp` and :func:`benefit_ptia_pp` are
what is payable, and :func:`suicide_factor` is applied on top of the first of them alone.

``w(t)`` is the lapse rate and ``w_cum(t)`` the cumulative lapse proportion that drives
the selective-lapsation loading on *mortality*. Spelling them :func:`lapse_rate` and
:func:`lapse_cum` keeps the second from reading as a running total of the first, which it
is not: it is a proportion of the original cohort, and the loading it feeds moves claims,
not lapses.

``expenses(t)`` in the notes **includes** the commission, and :func:`result_cf` publishes
:func:`commissions` beside it because the notes' worked-example table does. The
commission is therefore a *part* of the expense column, not a further line: subtracting
both from :func:`premiums` charges the commission twice. The notes' worked example fixes
the reading — ``expenses(0) = 882.14`` is ``250 + 2.08 + 0.06 + 630``, the maintenance
term being one twelfth of the annual charge, and the last of those four is the 40 %
initial commission.

.. rubric:: The cotisation rises with attained age

This is the French delta, and it is visible in the cash flows rather than buried in a
parameter. On the ``revisable`` form — the default of every retrieved French contract —
the cotisation is recomputed at *every* annual renewal from the tariff rate at the new
attained age, so ``prem_pp(t)`` moves every year — and only at the anniversary: it is
flat across the twelve months of a policy year, because the contracts say "à chaque
échéance annuelle" and not "chaque mois":

    prem_pp(24) / prem_pp(12) = 1.56 / 1.13 = 1.380531

— policy year 3 against policy year 2 — a 38 % step from age 59 to 60 against a trend of
about 8 % a year. That step is in the
published grid and a fitted curve would smooth it away, so :func:`prem_rate` is a table
lookup and nothing else. Over the worked configuration the cotisation runs from
1 575,00 € to 7 290,00 €, a factor of 4,6286 — which is exactly ``r(74)/r(58)`` and does
not depend on the capital at all.

The ``constante`` form is the level alternative, and it is a **[std]** construction: no
French standalone contract in the corpus writes one. With ``level_premium = 0`` it is
derived by actuarial equivalence with the revisable stream over the whole cover period,
on **tariff survivorship** — insured decrements only, no lapse — at ``tech_rate``:

    P_lev = sum v^t p_tau(t) SA r(x(t)) f phi / sum v^t p_tau(t)

which on the worked configuration is ``60,476.2476 / 15.449728 = 3,914.3891``. With
``level_premium > 0`` that figure is supplied instead and no equivalence is struck.

The two forms do **not** collect the same projected premium total: the equivalence
ignores lapse, and once lapses truncate the expensive late years the ``constante``
projection collects 36 367,46 € against the revisable 31 999,13 €. That is correct
rather than a bug — the identity that holds is the discounted one on tariff
survivorship — and a test asserting equality of projected totals is testing the wrong
thing.

.. rubric:: PTIA is an acceleration, not an addition

*Perte totale et irréversible d'autonomie* pays the **same** capital, early, to the
insured, and its payment ends the contract. Arithmetically that means one two-decrement
table: a life that leaves through ``ptia_rate`` is gone from ``pols_if`` and can never
generate a death claim, and the two rates add rather than compound.
:func:`check_decrement_closure` asserts the consequence at every ``t`` — claim events
plus lapses plus survivors equal the original policy — so a PTIA life left in force, or
counted twice, fails there.

PTIA cover also **stops earlier than death cover**, at ``ptia_end_age``, and the switch
is a hard gate on the attained age rather than a taper: ``ptia_rate(t)`` — and with it
``ptia_rate_mth(t)`` — is exactly zero from the first ``t`` with
``age(t) >= ptia_end_age()``. Because the age steps on the anniversary, the gate closes
on an anniversary too: on the worked configuration that is ``t = 84 ... 203``, the whole
of the policy year at attained age 65 onwards, and model point 11 enters at exactly
``ptia_end_age`` so its PTIA cover never attaches at all. :func:`check_ptia_gate` asserts
both.

The suicide exclusion never touches PTIA. Art. L. 132-7 voids the **death** cover for
suicide in the first year, and PTIA is not death, so :func:`suicide_factor` multiplies
:func:`benefit_death_pp` alone and only at ``t = 0``. Nor does the model carry the
art. R. 132-5 immediate-cover ceiling of 120 000 €: that alinéa belongs to
principal-residence loan cover and does not apply to a standalone temporaire décès.

.. rubric:: No cash value, anywhere

Art. L. 132-23 forbids both *rachat* and *réduction* on a temporaire décès. There is no
account value, no surrender value, no reduced-paid-up state and no maturity value at any
duration, so a lapse is a pure decrement: it moves ``pols_if`` and pays nothing.
``claims(t, "LAPSE")`` exists, returns zero, and appears in :func:`result_cf` as a zero
column, because a non-zero lapse row is the pitfall a reader arriving from a US model
with cash surrender values will import. A column of zeros states the product fact where a
missing column would only hide it, and :func:`check_no_cash_value` asserts it on every
model point.

The same statutory fact is why the whole of the exit machinery is lapse. The 30-day
*renonciation* window sits inside the year-1 lapse rate **[std]**; there is no surrender
charge, no dynamic surrender behaviour and no paid-up election to model.

.. rubric:: The last projected year has no lapse, and why

The notes' processing order puts lapses at the **end** of the month, after both insured
decrements. At the end of the final projected policy year the cover expires, and a lapse
and an expiry are then the same event paying the same nothing. So :func:`lapse_rate`
returns 0 through the **whole** of that policy year — ``duration(t) >= proj_len_y() - 1``,
months 192 to 203 on the worked configuration — and the whole surviving population leaves
as an expiry: ``pols_if(proj_len())`` is that cohort. The notes set out the same
convention, ``w(n - 1) = 0`` **[std]**, under *Lapse* and in step 7 of their processing
order, and they state it of a **policy year**; zeroing only the final month would leave
eleven months of 6 % lapse inside that year and move the expiring cohort from 27,887 % to
about 26,6 %, contradicting the notes' own figure. Read over the whole year it reproduces
their split of the closure identity — 6,737 % deaths, 0,517 % PTIA, 64,859 % lapses and
27,887 % survivors on the worked configuration, the **survivor term exactly the
annual-step model's** and the three exit terms reallocated by the finer grid. No cash flow
depends on the split.

``pols_if(proj_len())`` is read by :func:`check_decrement_closure` and by nothing
else. It is never a weight on a cash flow, and :func:`result_cf` stops at
``t = proj_len() - 1``.

.. rubric:: The délai d'attente

A *délai d'attente* delays the start of cover: 12 months for illness-caused death and
PTIA where the adhesion carried no medical formality, with the cotisations collected
returned to the heirs on a death inside the window, and 3 months at another carrier
waived for accidental causes. Five of the eight retrieved carriers have none, and the
composite runs with ``waiting_period_y = 0``.

Where it is switched on — model point 9 — the implementation is **[std]** in its
arithmetic and cited in its shape: inside the window a death claim pays
:func:`prem_refund_pp`, the cotisations collected up to and including the **month** of
claim, in place of the capital, and a PTIA claim pays nothing. The window itself is now
counted in months, ``duration_mth(t) < 12 * waiting_period_y()``, which is the unit the
sources state it in and exactly the old window for a whole number of years; a sub-annual
window is expressible for the first time, and no shipped model point uses one. The accidental capital is *not*
suppressed inside the window, which is the one carrier's express waiver for accidental
death. The decrements are untouched: the window changes what a claim pays, never who
leaves.

.. rubric:: Modules that are off in the base run

Four constructions are implemented and switched off, so the base run reproduces the
worked example while the machinery stays visible and testable:

- **Tariff drift**, ``tariff_drift = 0``. Two of the eight retrieved carriers reserve an
  explicit right to reprice the class for experience, and the representative carrier's
  current page implies a level above its own retrieved grid. Setting the drift to zero keeps the
  base run reproducible from cited data alone. A drift assumption is a premium-income
  assumption, not a mortality one.
- **Premium-shock lapse**, ``shock_lapse_beta = 0``, with ``shock_lapse_g0 = 0.10``.
  ``M_shock = 1 + beta max(0, P(t)/P(t-12) - 1 - g0)``, the ratio being between
  consecutive **renewals** and so read twelve months back — on a monthly grid
  ``P(t)/P(t-1)`` would be 1 in eleven months of twelve and the module would never fire.
  The revisable form hands the policyholder a rising bill, and the grid's own +38 % step
  at age 60 is exactly where an affordability response would show. Switched on it would
  bite through the whole of policy year 3, months 24 to 35 of the worked configuration,
  and nowhere else.
- **Selective lapsation**, ``sel_lapse_lambda = 0``, with ``sel_lapse_ref = 0.30``.
  ``q_d_eff = q_d (1 + lambda max(0, w_cum - w_ref))``, with ``w_cum`` read **at the
  anniversary** so that the loaded rate stays one annual rate for its policy year.
  Lapsers are healthier, so persisters are progressively impaired. The effect is larger
  here than on a UK level-premium term policy, because cumulative lapse reaches 64,9 % of
  the original cohort over seventeen years.
- **The accidental capital**, ``acc_share = 0``. The option pays an *additional* capital
  on the accidental share of claims, not a uniform uplift on every claim, and no
  retrieved source gives an accidental share of deaths. With the share at zero,
  ``accident_multiplier`` must have no effect on any cash flow — model point 6 is model
  point 1 with the multiplier at 2.00, and their frames are identical.

Indexation on the PASS or an insurer rate is described in the sources and is **not**
implemented: it reprices capital and cotisation together on an exogenous index, refusal
is definitive at three carriers, and modelling it would add an absorbing state driven
entirely by an assumption with no source.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — cotisations in, claims and expenses out — which
is the notes' own orientation and the library-wide sign. :func:`liability_cf` publishes
the same stream outgo-positive, ``liability_cf(t) = -net_cf(t)`` exactly, so a
best-estimate liability is ``sum v(t) liability_cf(t)`` over whatever discount curve the
valuation layer supplies. Both are columns of :func:`result_cf`, so the identity is
verifiable in the frame rather than only in prose.

The shape to expect on the ``revisable`` form, read on :func:`result_cf_annual`, is
almost no new-business strain — policy year 1 is +2,58 € on the worked configuration,
because the year's cotisation very nearly pays the year's acquisition cost — and thin
positive margins thereafter that grow as the tariff climbs. On the annual grid the same
year read -38,72 €; the sign flips because a decrementing block carries fewer claims and
less maintenance than an anniversary weighting charges it. Within policy year 1 the
monthly frame shows what the annual one could not: ``net_cf(0) = +633,73 €``, the whole
annual cotisation against the acquisition cost, then eleven negative months. The
``constante`` form inverts the annual picture: strongly positive in the first year,
+1 406,22 €, and it would carry a real *provision mathématique* against the later years.

.. rubric:: What the monthly grid changes, and what it does not

The grid is monthly; the **product is not**. Every contractual mechanic stays exactly
where the contract puts it, and each of the following is a decision taken deliberately
rather than inherited from the frame:

- the tariff is re-read, and the cotisation repriced, on the **anniversary only**
  (:func:`prem_rate`, :func:`prem_pp`), so both are flat across a policy year;
- the *fractionnement* is the one cycle the **model point** chooses rather than the
  contract, so the cotisation is collected in instalments on that cycle
  (:func:`prem_cycle`, :func:`prem_inst_pp`) and the annual *frais d'échéance* is divided
  among them rather than charged twelve times — which is what the loading and the fee
  were pricing all along;
- the art. L. 132-7 suicide void covers the whole of **policy year 1**
  (:func:`suicide_factor`), the 40 % commission rate the whole of policy year 1
  (:func:`commissions`), and the *délai d'attente* a whole number of months
  (:func:`in_waiting`);
- expenses inflate **by policy year**, stepping on the anniversary
  (:func:`inflation_factor`), which is the frlib house form rather than uslib's
  continuous one;
- the ``constante`` equivalence stays an **annual** construction on policy-year arguments
  (:func:`disc_factor`, :func:`pols_tariff`), so ``P_lev`` is unmoved by the conversion;
- the zero lapse rate of the final projected year covers that whole **year**
  (:func:`lapse_rate`), because the notes state it of a year;
- the selective-lapsation loading reads cumulative lapse **at the anniversary**
  (:func:`sel_lapse_factor`) and the premium-shock module compares **consecutive
  renewals** (:func:`shock_lapse_factor`), so both stay annual experience statements;
- the two dependent insured rates are converted to the month **together and split**, not
  converted apart (:func:`decr_rate_mth`).

What the finer grid does resolve is everything that is not a contract term: claims fall
at the end of the **month** of claim rather than of the policy year, maintenance expense
accrues a twelfth a month on the in-force of that month, and a fractionated cotisation is
collected on a block that has already lost lives.

That is what makes the two grids reconcile. Because the monthly insured decrement and the
monthly lapse rate each compound back to the year's annual rate, the recursion collapses
over any twelve months of one policy year to ``l(t+12) = l(t)(1 - q_d - q_p)(1 - w)`` —
the annual-step recursion, term for term — so the in-force **at every policy anniversary**
is identical to the annual-step model's, ``pols_if(12k)`` here equalling ``pols_if(k)``
there to floating point, and so is every annual contractual quantity: the tariff rate, the
cotisation, the capital, the level premium and the annuity-due factor behind it. The cash
flows are not identical and are not meant to be: death claims fall from 10 396,90 € to
10 094,20 € over the worked configuration, PTIA claims from 804,25 € to 775,29 €, expenses
from 2 676,38 € to 2 666,69 €, and ``net_cf`` rises from 18 121,59 € to 18 462,95 €.
Those timing differences are the reason for the monthly grid. :func:`result_cf_annual`
sums the frame into policy years so the two can be laid side by side.

.. rubric:: What a sibling may inherit

``ADE_FR_S`` and ``Obseques_FR_S`` sit on this chassis, and all three now run the same
monthly grid and the same ``duration_mth`` / ``duration`` / ``policy_year`` vocabulary.
The decrement machinery (:func:`mort_rate`, :func:`mort_rate_mth`, :func:`ptia_rate`,
:func:`ptia_rate_mth`, :func:`lapse_rate`, :func:`lapse_rate_mth`, :func:`pols_if_at`,
:func:`pols_death`, :func:`pols_ptia`, :func:`pols_lapse`), the exclusion machinery
(:func:`suicide_factor`, :func:`benefit_death_pp`, :func:`benefit_ptia_pp`), the expense
and commission ledger and the ``claims(t, kind)`` interface carry over unchanged. What
does **not** carry over is the benefit: an ADE capital follows the **outstanding loan
balance** on an amortisation schedule and adds ITT and IPT covers with their own
*franchise* and *quotité*, and an obsèques capital is a small fixed sum over a lifetime
horizon with a cash value, behind a twelve-month *carence*. Anything a sibling adds to
those layers belongs there, not here.
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


def premium_form():
    """The cotisation form: ``revisable`` or ``constante``.

    ``revisable`` is the French default and the product's signature — the cotisation is
    recomputed at every annual renewal on the new attained age.  ``constante`` is a
    **[std]** construction: no French standalone contract in the corpus writes a level
    cotisation, and it is carried because the contrast between the two is the largest
    structural lever in the model and the reason a *provision mathématique* exists on one
    form and not the other.
    """
    v = model_point()["premium_form"]
    if v not in ("revisable", "constante"):
        raise ValueError("invalid premium_form")
    return v


def benefit_shape():
    """The capital's shape over the cover period: ``constant`` or ``decreasing``.

    Only ``constant`` has a shipped schedule, because no retrieved French standalone
    contract amortizes the capital — a decreasing capital is the *assurance emprunteur*
    shape, and it lives in ``ADE_FR_S`` against a real loan balance rather than here
    against an invented one.  A model point carrying ``decreasing`` fails in
    :func:`benefit_factor`, which is the honest failure: the schedule is missing, not the
    formula.
    """
    v = model_point()["benefit_shape"]
    if v not in ("constant", "decreasing"):
        raise ValueError("invalid benefit_shape")
    return v


def benefit_schedule_id():
    """The key into *benefit_schedule.csv* naming this policy's benefit schedule."""
    return model_point()["benefit_schedule_id"]


def sex():
    """The insured's sex, M or F.  **Reporting only — it must not enter pricing.**

    Art. L. 111-7 forbids sex-based premium and benefit differences for contracts written
    from 21 December 2012, so :func:`prem_rate` and :func:`mort_rate_base` are both
    indexed by attained age alone and neither reads this cells.  The tension worth knowing
    is that the homologated valuation tables remain sex-specific, so a French reserving
    basis is sex-dependent while the tariff may not be; ``products/rente_viagere/`` meets
    the same tension from the other side.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def smoker():
    """The insured's smoker status, N or S.

    Carried because underwriting asks, and because it is what a *surprime* would be
    struck on.  It feeds :func:`rating_factor` through the model point rather than through
    a formula: no French insurer publishes a smoker loading, or any *surprime* scale at
    all, so there is nothing to look up.
    """
    v = model_point()["smoker"]
    if v not in ("N", "S"):
        raise ValueError("invalid smoker")
    return v


def issue_age():
    """The issue age on the *différence de millésime* basis: calendar year less birth year.

    Not age nearest birthday and not age last birthday — an integer age that steps on
    1 January irrespective of birth month, and the single most important convention to get
    right in a French annual-step model.  A one-year shift moves ``prem_pp(0)`` on the
    worked configuration from 1 575,00 € to 1 695,00 €, a 7,6 % error in year one that
    compounds through the whole projection.  On this annual grid the age steps at the
    policy anniversary instead, so an implementation on real dates carries a fractional
    offset of at most one year **[std]**.
    """
    return int(model_point()["issue_age"])


def sum_assured():
    """SA: the guaranteed capital, in euros.

    Freely chosen rather than tied to a loan balance, subject to a carrier minimum that
    runs from 6 097,96 € to 100 000 € across the corpus.  Model point 12 sits at the
    representative carrier's 20 000 € minimum, where the year-one cotisation at age 58 is
    210 € against 250 € of acquisition expense **[std]** — on small capitals the expense
    assumption, not mortality, decides whether the cell is viable.
    """
    return float(model_point()["sum_assured"])


def cover_end_age():
    """The attained age at which the death cover ceases.

    Nothing is payable at that boundary: no maturity value, no renewal, no conversion.
    """
    return int(model_point()["cover_end_age"])


def ptia_end_age():
    """The attained age at which the PTIA cover ceases, earlier than the death cover.

    Earlier in five of the eight retrieved carriers, and the model treats it as a hard
    gate on the attained age rather than a taper; see :func:`ptia_rate`.
    """
    return int(model_point()["ptia_end_age"])


def premium_rate_id():
    """The key into *premium_rate_table.csv* naming this policy's rate card."""
    return model_point()["premium_rate_id"]


def rating_factor():
    """f: the *surprime* multiplier on the tariff rate; 1.00 at standard rates.

    It scales the **cotisation only, never the capital** — a *surprime* buys the same
    capital at a higher price — so :func:`claims` is invariant to it.  No insurer
    publishes a *surprime* scale; the only public French price evidence on rated lives is
    on borrower cover, which bounds a standard rate from above rather than giving one.
    Model point 5 carries 1.50 **[std]**.
    """
    return float(model_point()["rating_factor"])


def prem_freq():
    """The cotisation payment frequency, a key into *freq_loading_table.csv*.

    Annual, half-yearly, quarterly or monthly.  The frequency buys two separate charges —
    a percentage loading and a fixed euro fee — and they must not be conflated; see
    :func:`prem_pp`.
    """
    v = model_point()["prem_freq"]
    if v not in data.freq_loading_table().index:                     # noqa: F821
        raise ValueError("no fractionation loading for prem_freq " + str(v))
    return v


def level_premium():
    """The level cotisation supplied on the ``constante`` form; 0 means derive it.

    Zero on every ``revisable`` point, where it is never read.  Model point 2 derives
    ``P_lev`` by equivalence and model point 3 supplies 3 900,00 € directly, so both
    branches of :func:`prem_level_pp` are exercised.
    """
    return float(model_point()["level_premium"])


def waiting_period_y():
    """The *délai d'attente* in policy years; 0 in the base run.

    Inside the window an illness-caused death pays back the cotisations collected and PTIA
    pays nothing.  See the Space docstring for the arithmetic, which is **[std]**, and
    model point 9, which switches it on for one year.
    """
    return int(model_point()["waiting_period_y"])


def accident_multiplier():
    """The accidental-capital option; 1.00 means the option is off.

    An *additional* capital payable where death or PTIA follows an accident — observed as
    100 % of the death capital, as 50 % at one carrier and as x2 or x3 by cause at
    another — not a uniform uplift on every claim.  With ``acc_share = 0`` in the base run
    it has **no effect on any cash flow**, which is the invariance model point 6 asserts.
    """
    return float(model_point()["accident_multiplier"])


def issue_date():
    """The issue date, carried for identification and not read by any formula.

    On the *différence de millésime* basis the age driving both the tariff and the cover
    limits is calendar year less birth year, so a projection on policy years needs
    :func:`issue_age` and nothing else.  A real-dates implementation would need this cells
    and would carry the fractional offset :func:`issue_age` describes.
    """
    return model_point()["issue_date"]


def pols_if_init():
    """The number of policies in force at issue: 1.0, a single-policy model point.

    The library's projections are per policy, so this is 1 everywhere; it is named rather
    than written as a literal because it is the scale of the roll-forward tolerances.
    """
    return 1.0


def proj_len_y():
    """n: the **number** of projected policy **years**, ``cover_end_age() - issue_age()``.

    17 on the worked configuration.  The contract states its own horizon in years, so
    this cells keeps it in years and everything annual is written against it: the
    ``constante`` equivalence sums over ``range(proj_len_y())``, and :func:`lapse_rate`
    compares ``duration(t)`` against ``proj_len_y() - 1`` to find the final policy year.
    :func:`proj_len` is twelve times this and is the frame.
    """
    return cover_end_age() - issue_age()


def proj_len():
    """The **number** of projected policy **months**, ``12 * proj_len_y()``.

    204 on the worked configuration.  The exclusive end of the frame, counted from
    ``t = 0``: the projection runs ``t = 0 ... proj_len() - 1``, :func:`result_cf` has
    ``proj_len()`` rows and the loop is lifelib's ``for t in range(proj_len())``.  Month
    ``t`` falls in the policy year at attained age ``issue_age() + duration(t)``, so the
    last covered month is the twelfth of the policy year at attained age
    ``cover_end_age() - 1``.  There is no benefit, no cotisation and no maturity value at
    ``t = proj_len()``, and ``pols_if`` there is the expiring cohort rather than a
    cash-flow weight; see the Space docstring.
    """
    return 12 * proj_len_y()


def duration_mth(t):
    """Completed policy months at the start of month t; equal to ``t``.

    ``t`` is 0-based and every model point in this product is projected from issue, so
    the identity is trivial — the cells exists so the monthly models in this library
    share one vocabulary with ``Obseques_FR_S`` and ``ADE_FR_S``, where an in-force point
    could open mid-policy.  It is what the modal premium cycle and the *délai d'attente*
    window are counted in.
    """
    return t


def duration(t):
    """Completed policy years at the start of month t: ``duration_mth(t) // 12``.

    0-based, as ``duration`` is throughout lifelib: 0 through the whole of the first
    policy year.  Every contractual schedule in this product is annual, so this is what
    the attained age, the tariff re-read, the suicide year and the commission year are
    keyed on.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """y: the contractual **1-based** policy year containing month t; 1 for ``t = 0..11``.

    The label ``duration(t) + 1``, derived from the 0-based ``t`` and never indexed by:
    it exists because two shipped inputs are keyed by a contractual policy year —
    *lapse_table.csv* (years 1-4) and *benefit_schedule.csv* (years 1-57) — and those
    lookups must map through this cells rather than pass ``t`` raw.  It also keys the
    expense inflation.  See :func:`lapse_rate_base`, :func:`benefit_factor` and
    :func:`inflation_factor`.
    """
    return duration(t) + 1


def age(t):
    """x(t): the attained age in the policy year containing month t, ``issue_age() + duration(t)``.

    The age steps on the **policy anniversary** — at ``t = 12, 24, ...`` — not on
    1 January and not monthly; the monthly grid does not make it finer.  On the
    *différence de millésime* basis — see :func:`issue_age` for why that matters more
    here than the choice would in a UK or US model.
    """
    return issue_age() + duration(t)


def prem_rate(t):
    """r(x): the tariff rate at the attained age of month t's policy year, as a fraction of SA.

    Re-read on the **anniversary only**: it is a function of ``age(t)``, which steps at
    the anniversary, so it is constant across the twelve months of a policy year.

    A **table lookup and nothing else**.  The published grid steps +38 % from age 59 to 60
    against a trend of about +8 % a year, and a fitted curve smooths that step away — so
    ``prem_rate(24)/prem_rate(12) = 1.56/1.13 = 1.380531`` on the worked configuration —
    the third policy year against the second — is a test of the premium engine, not a
    coincidence.

    ``tariff_drift`` multiplies the card by ``(1 + drift)^duration(t)`` and is 0 in the
    base run: two of the eight retrieved carriers reserve an express right to reprice the
    class for experience, but freezing the card at its vintage is what keeps the base run
    reproducible from cited data alone.  The exponent is **completed policy years** and
    not months, because a re-rating of the card is an annual act; the rate is therefore
    flat across the twelve months of a policy year, like everything else contractual
    here.  The grid itself is a 2019-2021 edition — use it for shape, not for level.
    """
    base = float(data.premium_rate_table().loc[                      # noqa: F821
        (premium_rate_id(), age(t)), "prem_rate"])
    return base * (1.0 + tariff_drift) ** duration(t)                # noqa: F821


def prem_freq_load():
    """phi: the fractionation multiplier for this policy's payment frequency.

    1.0000 annual, 1.0250 half-yearly, 1.0400 quarterly and monthly.  A multiplier
    embedded in the cotisation TTC, and one of only three disclosed charge figures in the
    whole source corpus.
    """
    return float(data.freq_loading_table().loc[                      # noqa: F821
        prem_freq(), "prem_freq_load"])


def prem_freq_fee():
    """The fixed annual *frais d'échéance* for this policy's payment frequency, in euros.

    3 € half-yearly, 6 € quarterly, 18 € monthly over twelve instalments, nil annual.  A
    **euro amount, not a second percentage** — applying it as a percentage load, or
    applying the fractionation loading and then billing the fee on top of it as a
    percentage, overstates premium income.  See :func:`prem_pp`.
    """
    return float(data.freq_loading_table().loc[                      # noqa: F821
        prem_freq(), "prem_freq_fee"])


def prem_instalments():
    """The number of cotisation instalments per policy year: 1 / 2 / 4 / 12.

    Read from the ``instalments`` column of *freq_loading_table.csv*, which ships beside
    the loading and the fee and names the cycle those two charges exist to price.  On the
    annual grid this model ran on, the column could not be used for anything — the whole
    loaded cotisation was charged once at the start of the year whatever the mode, which
    made the fractionation loading a charge for a service the model never rendered.  On
    the monthly grid it drives :func:`prem_cycle` and :func:`prem_inst_pp`.
    """
    return int(data.freq_loading_table().loc[                        # noqa: F821
        prem_freq(), "instalments"])


def prem_cycle():
    """Months between cotisation instalments: annual 12, half-yearly 6, quarterly 3, monthly 1.

    ``12 // prem_instalments()`` — arithmetic of the elected mode rather than an
    assumption, so it is written here rather than held in a Reference.
    """
    return 12 // prem_instalments()


def prem_due(t):
    """Whether a cotisation instalment falls due at the **beginning** of month t.

    ``duration_mth(t) % prem_cycle() == 0``.  An annual payer is due in the first month
    of every policy year and nowhere else; a monthly payer is due in every month.  The
    *fractionnement* is the one cycle in this product the **model point** chooses rather
    than the contract, so it is collected on its own cycle and not on the anniversary.
    """
    return duration_mth(t) % prem_cycle() == 0


def prem_tariff_pp(t):
    """SA r(x(t)) f phi: the tariff cotisation per policy in period t, before the fee.

    The rule the source states in its own worked examples: 20 000 € at attained age 34
    gives 20 000 x 0,15/100 = 30 € for one year, and 150 000 € at attained age 49 gives
    900 €.  The same rule at attained age 58 gives 1 575,00 €.
    """
    return sum_assured() * prem_rate(t) * rating_factor() * prem_freq_load()


def disc_factor(y):
    """v^y: the discount factor at ``tech_rate`` for **policy year** y, 0-based.

    The argument is a policy year and not a month: the ``constante`` equivalence is an
    annual construction and stays one on the monthly grid, so re-striking it month by
    month would move ``P_lev`` and break the identity the notes assert.  The published
    cash flows are undiscounted; this rate exists to strike the level cotisation and for
    nothing else.  0,5 % p.a. **[std]**, which is what the Institut des actuaires' own
    illustrations for a death cover use and is well inside the art. A. 132-1 cap of
    min(3,5 %, 60 % TME).
    """
    return (1.0 + tech_rate) ** (-y)                                 # noqa: F821


def pols_tariff(y):
    """p_tau(y): tariff survivorship entering **policy year** y — insured decrements, no lapse.

    ``p_tau(0) = 1``, ``p_tau(y+1) = p_tau(y) (1 - q_d - q_p)`` on the **table** rates
    :func:`mort_rate_base` and :func:`ptia_rate_base` of that policy year, read at its
    opening month ``12 * y``.  Like :func:`disc_factor` this is a policy-year recursion
    and not a monthly one: it is the tariff basis of an annual equivalence, and spreading
    it over months would change the level cotisation the notes publish while adding
    nothing.  Using the table rates rather than the behaviourally loaded ones is both the
    actuarially right basis and what keeps the derivation acyclic — the loaded death rate
    depends on the lapse path, which on the ``constante`` form would depend on the
    premium the equivalence is about to produce.
    """
    if y <= 0:
        return 1.0
    return pols_tariff(y - 1) * (
        1.0 - mort_rate_base(12 * (y - 1)) - ptia_rate_base(12 * (y - 1)))


def tariff_annuity():
    """The annuity-due factor of the equivalence: ``sum v^y p_tau(y)`` over the cover years.

    15,449728 on the worked configuration, and ``P_lev x 15,449728 = 60 476,25 €`` is the
    present value of the revisable stream on the same basis — the identity that *does*
    hold between the two premium forms, as against the projected premium totals, which do
    not.  Summed over ``range(proj_len_y())``: the equivalence is annual, so it is struck
    over policy years and is unchanged by the monthly grid.
    """
    return sum(disc_factor(y) * pols_tariff(y)
               for y in range(proj_len_y()))


def tariff_prem_pv():
    """The present value of the revisable cotisation stream on tariff survivorship.

    ``sum v^y p_tau(y) SA r(x(y)) f phi``; 60 476,2476 € on the worked configuration, the
    tariff cotisation being read at each policy year's opening month ``12 * y``.  The
    fixed *frais d'échéance* is deliberately outside it: the fee is the same amount under
    either premium form, so it neither belongs in the equivalence nor changes it.
    """
    return sum(disc_factor(y) * pols_tariff(y) * prem_tariff_pp(12 * y)
               for y in range(proj_len_y()))


def prem_level_pp():
    """P_lev: the level cotisation of the ``constante`` form, before the fee.

    ``level_premium()`` where the model point supplies one, otherwise
    ``tariff_prem_pv() / tariff_annuity()`` — a survivorship-and-discount-weighted average
    of the same grid rates, 3 914,3891 € on the worked configuration, unchanged by the
    monthly grid because the equivalence never left the annual one.  Read another way,
    ``P_lev / SA`` is the ``v^y p_tau(y)``-weighted mean of the seventeen grid rates,
    2,60959276 %, which reaches the same figure without ever forming the premium stream.

    Not read at all on the ``revisable`` form.
    """
    if level_premium() > 0.0:
        return level_premium()
    return tariff_prem_pv() / tariff_annuity()


def prem_pp(t):
    """P(t): the **annual** cotisation per in-force policy for month t's policy year, in euros.

    The tariff amount on the ``revisable`` form and ``P_lev`` on the ``constante`` form,
    **plus the fixed frais d'échéance once**.  The two fractionation charges are of
    different kinds and are applied in different places: ``prem_freq_load`` is a
    multiplier inside :func:`prem_tariff_pp`, and ``prem_freq_fee`` is a euro amount added
    here.  Charging the fee as a further percentage, or loading the already-loaded
    cotisation with it, overstates premium income.

    It is the **annual** charge of the policy year containing month ``t`` and is flat
    across that year's twelve months, because the contract reprices "à chaque échéance
    annuelle" and not monthly.  What is actually collected in month ``t`` is
    :func:`prem_inst_pp`, the instalment the elected *fractionnement* makes due.

    On the ``revisable`` form this cells is the whole French delta: it changes every year
    because :func:`prem_rate` is read at the new attained age, and over the worked
    configuration it runs from 1 575,00 € to 7 290,00 € — a factor of 4,6286 that depends
    only on the grid and not on the capital.
    """
    base = (prem_level_pp() if premium_form() == "constante"
            else prem_tariff_pp(t))
    return base + prem_freq_fee()


def prem_inst_pp(t):
    """P_inst(t): the cotisation instalment actually collected per policy in month t.

    ``prem_pp(t) / prem_instalments()`` in a month :func:`prem_due` makes due, zero
    otherwise, so the instalments of a policy year sum to exactly the year's annual
    cotisation — the fee included, which is what *freq_loading_table.csv* itself says of
    the monthly mode ("18 EUR frais d'echeance over 12 instalments").  An annual payer
    therefore collects the whole 1 575,00 € in the first month of the policy year and
    nothing in the other eleven, which is what an annual-mode policy looks like on a
    monthly grid; model point 4 is the contrast, twelve instalments of 77,77 €.

    This is what the fractionation loading and the *frais d'échéance* were charging for
    all along, and it is the one place the finer grid changes an answer rather than its
    resolution: on a fractionated point the instalments after the first are collected on
    a block that has already lost lives, so the premium-cessation rule of the contracts
    finally bites where an annual grid could not express it.
    """
    return prem_pp(t) / prem_instalments() if prem_due(t) else 0.0


def mort_rate_base(t):
    """The **annual** table death rate at the attained age of month t's policy year.

    A **[std]** Gompertz-form proxy, ``0.00400 x 1.09^(age - 58)``, not a homologated or
    fitted table: the regulatory TH 00-02 / TF 00-02 tables are annexed to an *arrêté* and
    are cited by name rather than redistributed, and no French insurer publishes a basis.
    Indexed by attained age alone — sex may not enter a French tariff written from
    21 December 2012, and the proxy carries no *décalage d'âge* — the annexed shifts are
    required only for *contrats en cas de vie* other than annuities, which a temporaire
    décès is not, and a shift applied to a table that was never homologated would be
    theatre in any case.
    """
    return float(data.mort_table().loc[age(t), "mort_rate"])    # noqa: F821


def sel_lapse_factor(t):
    """The selective-lapsation loading on mortality in period t **[std]**.

    ``1 + lambda max(0, w_cum(12 dur(t)) - w_ref)``.  Lapsers are healthier than
    persisters, so a
    block that has already shed a large proportion of its lives carries impaired mortality
    on the remainder.  The effect is larger on this product than on a UK level-premium
    term policy, because cumulative lapse reaches 64,9 % of the original cohort over the
    worked configuration's seventeen years.

    ``w_cum`` is read **at the anniversary**, ``lapse_cum(12 * duration(t))``, so the
    loading is one number for the whole policy year and :func:`mort_rate` stays the
    *annual* rate of that year, as the library's ``*_rate`` / ``*_rate_mth`` split
    requires.  Letting it drift month by month would be a second modelling change
    smuggled in beside the grid change: the module was only ever calibrated as an annual
    experience statement, and a within-year drift would break the anniversary
    equivalence without buying anything.

    Off in the base run (``sel_lapse_lambda = 0``), where it returns 1 in every month
    without reading :func:`lapse_cum` at all — the short circuit is what keeps the
    ``constante`` premium derivation from depending on the lapse path it feeds.
    """
    if sel_lapse_lambda == 0.0:                                      # noqa: F821
        return 1.0
    return 1.0 + sel_lapse_lambda * max(                             # noqa: F821
        0.0, lapse_cum(12 * duration(t)) - sel_lapse_ref)            # noqa: F821


def mort_rate(t):
    """q_d(t): the **annual** dependent death rate of the policy year containing month t.

    The table rate times the selective-lapsation loading, capped at 1 — the vector the
    technical notes tabulate, kept annual as the library-wide convention requires.
    :func:`mort_rate_mth` is the rate actually applied in the month.  Dependent means a
    rate of decrement in a two-decrement table rather than an independent
    single-decrement rate, so it **adds** to :func:`ptia_rate` rather than compounding
    with it: an implementation using ``1 - (1 - q_d)(1 - q_p)`` gets 0.00479680 against
    0.00480000 in the first year of the worked configuration.  That additivity is also
    why the two rates are converted to the month **together** rather than apart; see
    :func:`decr_rate_mth`.
    """
    return min(1.0, mort_rate_base(t) * sel_lapse_factor(t))


def ptia_rate_base(t):
    """The PTIA decrement rate on the tariff basis, before any behavioural loading.

    ``ptia_ratio x mort_rate_base(t)`` while the cover is on, and **exactly zero** from
    the first period with ``age(t) >= ptia_end_age()``.  Used by :func:`pols_tariff`,
    so that the ``constante`` equivalence is struck on the tariff decrements alone.
    """
    if age(t) >= ptia_end_age():
        return 0.0
    return ptia_ratio * mort_rate_base(t)                            # noqa: F821


def ptia_rate(t):
    """q_p(t): the **annual** dependent PTIA rate of the policy year containing month t.

    ``ptia_ratio x mort_rate(t)`` while the cover is on, and **exactly zero** from the
    first period with ``age(t) >= ptia_end_age()`` — a hard gate on the attained age,
    not a taper, because "the PTIA capital is an anticipated payment of the death capital
    and its payment ends the contract" means the life is gone from ``pols_if``, and the
    cover either attaches at that age or does not.

    ``ptia_ratio = 0.20`` is a pure placeholder **[std]**: no retrieved French source
    gives a PTIA incidence rate at any age, and the only public French figure touching
    PTIA at all is an underwriting-outcome statistic that says nothing about incidence.
    It is the assumption in this model most in need of a real source, and it moves 7,2 %
    of total claims on the worked configuration.
    """
    if age(t) >= ptia_end_age():
        return 0.0
    return ptia_ratio * mort_rate(t)                                 # noqa: F821


def decr_rate(t):
    """q_d(t) + q_p(t): the **annual** insured decrement of the policy year containing month t.

    The two-decrement table's total rate of exit through a claim.  It is named because
    the additive dependent-rate convention needs somewhere to live on a monthly grid: it
    is this sum, and not either rate alone, that the annual recursion applies and that the
    monthly conversion must reproduce.  See :func:`decr_rate_mth`.
    """
    return mort_rate(t) + ptia_rate(t)


def decr_rate_mth(t):
    """The monthly insured decrement applied in month t **[std]**.

    ``1 - (1 - q_d - q_p)^(1/12)``: the constant-force conversion of the **combined**
    annual rate, derived geometrically and not by dividing by twelve, so that twelve
    months of it compound back to exactly ``q_d + q_p`` — the factor the annual-step
    model applied at the anniversary.

    Converting the two rates **separately** and adding the results is the tempting
    reading and it is wrong here, because ``q_d`` and ``q_p`` are dependent rates of one
    table: ``(1-(1-q_d)^(1/12)) + (1-(1-q_p)^(1/12))`` gives a twelve-month insured
    survival of 0.9952029339 against the annual model's 0.9952000000 at the anchor cell,
    an error already 2.6e-6 at the first anniversary and 1.0e-5 in ``pols_if`` by the end
    of the run.  No French source states a conversion convention for any decrement, so
    the choice is a standardization; what is not optional is that it reproduce the annual
    factor.  :func:`mort_rate_mth` and :func:`ptia_rate_mth` split this back in the rates'
    own proportion.
    """
    return 1.0 - (1.0 - decr_rate(t)) ** (1.0 / 12.0)


def mort_rate_mth(t):
    """q_dm(t): the monthly death rate applied in month t **[std]**.

    The combined monthly insured decrement split in the annual rates' own proportion,
    ``decr_rate_mth(t) * q_d(t) / (q_d(t) + q_p(t))``, and zero where the whole insured
    decrement is.  Splitting proportionally is what keeps
    ``ptia_rate_mth(t) / mort_rate_mth(t) = ptia_ratio`` exactly — the acceleration ratio
    the product is built on — while twelve months of ``q_dm + q_pm`` still compound back
    to the year's ``q_d + q_p``.  Where the PTIA gate has closed, ``q_p = 0`` and this
    degenerates to the house form ``1 - (1 - q_d)^(1/12)``.
    """
    d = decr_rate(t)
    return 0.0 if d == 0.0 else decr_rate_mth(t) * mort_rate(t) / d


def ptia_rate_mth(t):
    """q_pm(t): the monthly PTIA rate applied in month t **[std]**.

    ``decr_rate_mth(t) * q_p(t) / (q_d(t) + q_p(t))``, and zero where the whole insured
    decrement is — in particular exactly zero from the first month at or beyond
    ``ptia_end_age()``, because :func:`ptia_rate` is.  Identically
    ``ptia_ratio * mort_rate_mth(t)`` while the cover is on, which is the acceleration
    ratio surviving the conversion untouched.
    """
    d = decr_rate(t)
    return 0.0 if d == 0.0 else decr_rate_mth(t) * ptia_rate(t) / d


def lapse_rate_base(t):
    """The **annual** table lapse rate of month t's policy year **[std]**, before any shock.

    12 / 10 / 8 / 6 per cent **a year**, elevated in the first three years to absorb the
    30-day *renonciation* window and early-duration attrition, then flat.
    *lapse_table.csv* is keyed by the **contractual policy year**, 1 to 4, so the lookup
    maps through :func:`policy_year` — months ``t = 0 ... 11`` read the file's policy
    year 1 — and policy years beyond the table take its last row.  The rates stay annual;
    :func:`lapse_rate_mth` does the spreading.  **No observed range exists**: not one of
    the eight retrieved contracts and neither secondary guide publishes a lapse rate, so
    the shape is a modeler's construction and the levels are unsourced.  What the
    contracts do tell us is that voluntary exit is easy and cheap, because there is
    nothing to forfeit.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[
        min(policy_year(t), int(tbl.index.max())), "lapse_rate"])


def shock_lapse_factor(t):
    """M_shock(t): the premium-shock lapse multiplier **[std]**; 1 in the base run.

    ``1 + beta max(0, P(t)/P(t-12) - 1 - g0)``.  The ratio is between **consecutive
    renewals** and so reads the cotisation twelve months back, not one: on a monthly grid
    ``P(t)/P(t-1)`` would be 1 in eleven months of twelve and the module would never fire
    at all.  The revisable form hands the policyholder a rising bill, and the published
    grid's own +38 % step at age 60 is exactly where an affordability response would show;
    switched on it takes the value 1.420796 through the whole of policy year 3, months 24
    to 35 of the worked configuration, and 1 everywhere else — the annual model's own
    behaviour at ``t = 2``, now spread over that year's twelve months by
    :func:`lapse_rate_mth`.  Off by default (``shock_lapse_beta = 0``), and 1 through the
    whole of policy year 1, which has no previous renewal to compare with.
    """
    if shock_lapse_beta == 0.0 or duration(t) <= 0:                  # noqa: F821
        return 1.0
    return 1.0 + shock_lapse_beta * max(                             # noqa: F821
        0.0, prem_pp(t) / prem_pp(t - 12) - 1.0 - shock_lapse_g0)    # noqa: F821


def lapse_rate(t):
    """w(t): the **annual** lapse rate of the policy year containing month t.

    The table rate times the shock multiplier, capped at 1 — the vector the technical
    notes tabulate; :func:`lapse_rate_mth` is the rate actually applied at the end of the
    month.  **Zero through the whole of the final projected policy year**,
    ``duration(t) >= proj_len_y() - 1`` (months 192 to 203 on the worked configuration):
    the end of that year is also the moment the cover expires, so a lapse and an expiry
    are the same event paying the same nothing, and the whole surviving population leaves
    as an expiry.  That is the notes' ``w(n - 1) = 0`` **[std]** — stated under *Lapse*
    and in step 7 of their processing order — and it is what reproduces their split of the
    closure identity, survivor term included.  The zero covers the **year** and not just
    its last month, because the notes name a policy year: zeroing only month 203 would
    leave eleven months of 6 % lapse in the final year and move the expiring cohort from
    0,27886852 to about 0,266, contradicting the notes' own figure.  It moves no cash
    flow, only the split.  A lapse pays nothing at any duration; see :func:`claims`.
    """
    if duration(t) >= proj_len_y() - 1:
        return 0.0
    return min(1.0, lapse_rate_base(t) * shock_lapse_factor(t))


def lapse_rate_mth(t):
    """w_m(t): the lapse rate applied at the **end** of month t **[std]**.

    ``1 - (1 - w)^(1/12)`` on the policy year's annual rate, derived geometrically and
    not by dividing by twelve, so that twelve months of it compound back to exactly that
    rate.  No exception is made for any month: unlike ``Term_US_S``, this product has no
    shock lapse tied to a named date inside a policy year, and the one rate the notes do
    put on a boundary — the zero of the final policy year — is a rate for the whole year
    rather than for a month of it.  No French source states a conversion convention for
    any decrement **[std]**.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def lapse_cum(t):
    """w_cum(t): the cumulative lapse proportion of the original cohort before month t.

    A proportion of :func:`pols_if_init`, **not** a running total of :func:`lapse_rate`,
    and it drives a loading on *mortality* rather than on lapse.  A monthly recursion now,
    but read only at anniversaries — see :func:`sel_lapse_factor`.  Zero in the first
    month, ``t = 0``.
    """
    if t <= 0:
        return 0.0
    return lapse_cum(t - 1) + pols_lapse(t - 1) / pols_if_init()


def pols_if(t):
    """l(t): the number of policies in force at the **start** of month t, at time t.

    ``pols_if(0) = pols_if_init()``, then the notes' recursion on the monthly rates,
    ``l(t+1) = l(t)(1 - q_dm(t) - q_pm(t))(1 - w_m(t))``.  This is the weight on every
    cash flow of the same :func:`result_cf` row.  Because the monthly rates compound back
    to the annual ones, ``pols_if(12k)`` is exactly what an annual-step model carried at
    its year ``k``.

    ``pols_if(proj_len())`` is defined and is the **expiring cohort** — the survivors
    whose cover simply runs out — because the notes' closure identity needs it.  It is
    read by :func:`check_decrement_closure` and by nothing else: it is never a weight on a
    cash flow, and :func:`result_cf` stops at ``t = proj_len() - 1``.  Zero outside
    ``0 .. proj_len()``.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return pols_if_at(t - 1, "AFT_DECR")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number
        as :func:`pols_if` and the weight on that month's cash flows.

    ``"BEF_LAPSE"``
        after both insured decrements, before lapses — the notes' processing
        order takes deaths and PTIA claims at the end of the month and lapses
        after them **[std order]**, so this is the population lapses are
        taken from.  The two insured **monthly** rates are subtracted rather
        than compounded, because they are the proportional split of one
        two-decrement table's combined monthly rate.

    ``"AFT_DECR"``
        l(t+1), the end-of-month state.  In the final projected policy year
        :func:`lapse_rate` is zero, so at ``t = proj_len() - 1`` this is the
        expiring cohort.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate_mth(t) - ptia_rate_mth(t))
    if timing == "AFT_DECR":
        if t < 0 or t > proj_len() - 1:
            return 0.0
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate_mth(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """l(t) q_dm(t): expected deaths in month t, claimed at the **end of that month**.

    The monthly rate, not the annual one: a death now falls in the month it happens and
    the claim is settled there, which is the resolution the finer grid buys and the reason
    the death-claim total is below the annual-step model's — an anniversary weighting
    exposes the whole opening cohort for the whole year.

    The claimant has already paid the instalment that fell due in advance at the start of
    the month; that is this model's reading of "premium payment ceases on death"
    **[std]**.  Multiplying :func:`premiums` by ``(1 - q_dm - q_pm)`` on top of it applies
    the rule twice.
    """
    return pols_if(t) * mort_rate_mth(t)


def pols_ptia(t):
    """l(t) q_pm(t): expected PTIA claims in month t, claimed at the end of that month.

    A **second exit from the same table**, not a second cover: the capital is the death
    capital paid early to the insured, and its payment ends the contract.  A life counted
    here is gone from :func:`pols_if` and can never generate a death claim.
    """
    return pols_if(t) * ptia_rate_mth(t)


def pols_lapse(t):
    """Lapses at the end of month t, taken from the survivors of both insured decrements.

    Pays nothing — art. L. 132-23 forbids both *rachat* and *réduction* on a temporaire
    décès — so this moves :func:`pols_if` and nothing else.  Zero through the whole of the
    final projected policy year, where the survivors leave as an expiry instead; see
    :func:`lapse_rate`.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t)


def benefit_factor(t):
    """The benefit schedule factor of month t's policy year, from *benefit_schedule.csv*.

    1.0 in every year on the ``constant`` schedule, the only one shipped.  The file is
    keyed by the **contractual policy year**, 1 to 57, so the lookup maps through
    :func:`policy_year` — months ``t = 0 ... 11`` read the file's policy year 1 — and
    policy years beyond the table take its last row.  The schedule is a contract term and
    steps on the anniversary, never within a year.  A model point naming a schedule the file
    does not carry fails here, which is the honest failure: the schedule is missing, not
    the formula.
    """
    rows = data.benefit_schedule().loc[benefit_schedule_id()]        # noqa: F821
    return float(rows.loc[
        min(policy_year(t), int(rows.index.max())), "benefit_factor"])


def benefit_pp(t):
    """B(t): the **contractual** capital payable on a month-t claim, in euros.

    ``sum_assured() x benefit_factor(t)``.  It is invariant to :func:`rating_factor`: a
    *surprime* scales the cotisation only, never the capital.  What a claim actually pays
    is :func:`benefit_death_pp` or :func:`benefit_ptia_pp`, which differ from this inside
    a *délai d'attente*.
    """
    return sum_assured() * benefit_factor(t)


def in_waiting(t):
    """Whether month t falls inside the *délai d'attente*.

    ``waiting_period_y`` is a length in **contractual policy years**, so the window is
    ``duration_mth(t) < 12 * waiting_period_y()`` — a one-year window covers months
    ``t = 0 ... 11``, exactly the annual model's ``t = 0``.  Counting the window in months
    is what the sources actually state (12 months at one carrier, 3 months at another),
    and the monthly grid makes a sub-annual window expressible for the first time; no
    shipped model point uses one, so no ``waiting_period_m`` column is introduced.  False
    everywhere when the window is not elected, which is the base run and eleven of the
    twelve model points.
    """
    return duration_mth(t) < 12 * waiting_period_y()


def prem_refund_pp(t):
    """The cotisations **actually collected** up to and including month t, per policy.

    Paid back to the heirs on a death inside the *délai d'attente*, in place of the
    capital.  It accumulates :func:`prem_inst_pp` and not :func:`prem_pp`, because the
    contract returns "les cotisations collectées": on a fractionated point a claimant part
    way through a policy year has paid only the instalments billed so far, which is both
    the literal reading and the only one that stays a cash quantity.  On an annual-mode
    point — model point 9, the only one that elects the window — the whole year's
    cotisation is collected in its first month, so this is 296,00 € through the whole
    window, exactly the annual model's figure.  Accumulated at nil interest **[std]**: no
    source gives a rate.
    """
    if t <= 0:
        return prem_inst_pp(0)
    return prem_refund_pp(t - 1) + prem_inst_pp(t)


def benefit_death_pp(t):
    """What a death claim in month t actually pays, per claim, in euros.

    ``B(t)`` outside the *délai d'attente*; inside it, the cotisations collected, because
    an illness-caused death inside the window is not covered and the contract returns what
    was paid.  The first-year suicide exclusion is applied on top of this by
    :func:`claims`, not here, so the two exclusions stay separable.
    """
    if in_waiting(t):
        return prem_refund_pp(t)
    return benefit_pp(t)


def benefit_ptia_pp(t):
    """What a PTIA claim in month t actually pays, per claim, in euros.

    ``B(t)`` — the same capital as a death claim, which is what "acceleration" means —
    and **zero** inside a *délai d'attente*, where the PTIA cover has not yet attached.
    The suicide factor never touches it: art. L. 132-7 voids the *death* cover in year
    one, and PTIA is not death.
    """
    if in_waiting(t):
        return 0.0
    return benefit_pp(t)


def accident_extra_pp(t):
    """The additional accidental capital per claim in month t **[std]**.

    ``(accident_multiplier() - 1) x acc_share x B(t)``.  The option pays an *additional*
    capital on the **accidental share** of claims, not a uniform uplift on every claim, so
    it carries ``acc_share`` and not just the multiplier.  No retrieved source gives an
    accidental share of deaths, so ``acc_share = 0`` in the base run and the whole term is
    zero however large the multiplier — model point 6 asserts that invariance.

    It is not suppressed inside a *délai d'attente*: the one carrier that publishes a
    waiting period waives it for accidental causes.
    """
    return (accident_multiplier() - 1.0) * acc_share * benefit_pp(t)  # noqa: F821


def suicide_factor(t):
    """sigma(t): the death-benefit exclusion factor; below 1 through policy year 1 only.

    Art. L. 132-7 makes the death cover "de nul effet" for suicide "au cours de la
    **première année** du contrat", so the exclusion covers the whole of policy year 1 —
    months ``t = 0 ... 11``, ``duration(t) == 0`` — and not merely the first month.  The
    statute names a year; a monthly grid does not make it a month.  0.98 **[std]** stands
    for "about 2 % of first-year deaths are excluded suicides" — no retrieved source gives
    a suicide share of deaths at any age, and setting it to 1.000 is a defensible variant.
    What is not defensible is applying it to PTIA, or beyond the first year, or importing
    the art. R. 132-5 immediate-cover ceiling of 120 000 €, which belongs to
    principal-residence loan cover.

    It is worth 11,33 € on the worked configuration — immaterial to the result, material
    to correctness, because it is the *only* thing standing between expected claim events
    and expected claim amounts there.
    """
    return suicide_year1_factor if duration(t) == 0 else 1.0         # noqa: F821


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the capital paid at the end of the **month** of death,
        ``sigma(t) x benefit_death_pp(t) x pols_death(t)``, plus any
        accidental capital.  The suicide factor applies here and nowhere
        else.

    ``"PTIA"``
        the **same** capital paid early on a PTIA claim, with no suicide
        factor.  Zero from the first month at or beyond
        ``ptia_end_age()``, and zero inside a *délai d'attente*.

    ``"LAPSE"``
        zero, always.  Art. L. 132-23 forbids both *rachat* and *réduction*
        on a temporaire décès, so there is no surrender value and no
        reduced-paid-up value at any duration; the kind exists so that the
        zero is stated rather than left to inference.  See
        :func:`check_no_cash_value`.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "PTIA", "LAPSE"))
    if kind == "DEATH":
        return pols_death(t) * (
            suicide_factor(t) * benefit_death_pp(t) + accident_extra_pp(t))
    if kind == "PTIA":
        return pols_ptia(t) * (benefit_ptia_pp(t) + accident_extra_pp(t))
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def premiums(t):
    """Cotisation income at the **beginning** of month t, an inflow.

    ``P_inst(t) l(t)``: the instalment the elected *fractionnement* makes due this month,
    weighted by the in-force entering it.  An annual payer therefore contributes the
    whole year's cotisation in the first month of the policy year and nothing in the
    other eleven, and a monthly payer contributes a twelfth each month on a block that has
    already lost lives — which is where the premium-cessation rule of the contracts
    finally bites.  Not further multiplied by ``(1 - q_dm - q_pm)``: claims fall at the
    end of the month, so a claimant has already paid the month's instalment, and applying
    the rule again here would charge it twice.
    """
    return prem_inst_pp(t) * pols_if(t)


def inflation_factor(t):
    """The expense inflation factor in month t: ``(1 + expense_infl)^(policy_year(t) - 1)`` **[std]**.

    Expenses inflate **by policy year and not by month**, stepping on the anniversary,
    which is how ``Obseques_FR_S``, ``ADE_FR_S`` and ``Dep_FR_S`` all write it and how the
    notes tabulate the maintenance charge.  (``Term_US_S`` in uslib uses the continuous
    ``(1 + i)^(t/12)`` instead; frlib does not follow it there.)  It is arithmetically the
    same sequence the annual-step model published, re-indexed — what changes is that a
    twelfth of the charge is borne by the in-force of each month.
    """
    return (1.0 + expense_infl) ** (policy_year(t) - 1)              # noqa: F821


def claim_expenses(t):
    """ec x (D(t) + P(t)): the claim handling expense on the month's claims **[std]**.

    150 € per death or PTIA claim, uninflated.  A round-number placeholder: the
    *chargements de gestion* of a French tariff are not separately disclosed anywhere,
    which is precisely why art. R. 343-3 has to require the *provision mathématique* to
    carry an estimate of them.  Inside :func:`expenses`, and named separately because it
    is the only expense line that scales with claims rather than with policies.
    """
    return claim_expense * (pols_death(t) + pols_ptia(t))            # noqa: F821


def commissions(t):
    """Commission outgo in month t **[std]**, on the cotisation **collected** that month.

    40 % through the whole of policy year 1, ``duration(t) == 0``, then 5 % from policy
    year 2 — levels chosen so that the year-one acquisition cost is of the same order as
    the year-one cotisation at the anchor age.  No French insurer publishes a commission
    scale for this product.

    The *rate* is a policy-year rate and steps on the anniversary; the *base* is
    :func:`premiums`, the instalment actually collected, so a fractionated payer earns the
    commission in instalments too.  On an annual-mode point that reproduces the annual
    model's commission exactly, because both the rate and the collection sit on the
    anniversary.

    This is a **part of** :func:`expenses`, not a further line beside it: the notes' own
    expense column includes it, and subtracting both from :func:`premiums` charges the
    commission twice.
    """
    rate = comm_rate_init if duration(t) == 0 else comm_rate_renew   # noqa: F821
    return rate * premiums(t)


def expenses(t):
    """Total expense outgo in month t, **including commission** **[std]**.

    Acquisition 250 € per policy at issue — a single amount in month 0, not a fraction of
    any premium — maintenance at **one twelfth** of the 25 € per in-force policy per year
    inflating at 2 %, the claim expense, and the commission.  All four are round-number
    placeholders: no French insurer publishes an expense loading, an acquisition cost or a
    commission scale for this product, and the only disclosed charge figures in the whole
    corpus are the fractionation loadings, the *frais d'échéance* and a 1,30 € association
    subscription — none of which is an expense assumption.

    A twelfth of the annual maintenance charge accrues each month, so a policy that runs a
    full year carries the same charge as it did on the annual grid — but it is now borne
    by the in-force of **each month** rather than of the anniversary, which is what makes
    a decrementing block cost less: 254,60 € of maintenance over the worked configuration
    against the annual grid's 263,96 €.

    On the worked configuration ``expenses(0) = 882.14`` is ``250 + 2.08 + 0.06 + 630``,
    and the twelve months of policy year 1 total 904,22 €.  That last term is the initial
    commission, which is why :func:`net_cf` subtracts this cells and not
    :func:`commissions` as well.
    """
    acq = acq_expense * pols_if(t) if t == 0 else 0.0                # noqa: F821
    maint = (maint_expense / 12.0                                    # noqa: F821
             * inflation_factor(t) * pols_if(t))
    return acq + maint + claim_expenses(t) + commissions(t)


def net_cf(t):
    """The net liability cash flow of month t, **income positive**.

    Cotisations less death claims, PTIA claims and total expense — and total expense
    already carries the commission, so it is subtracted once.  The notes' own sign, and
    the library-wide one.

    On the ``revisable`` form the shape to expect, read on :func:`result_cf_annual`, is
    almost no new-business strain — policy year 1 is +2,58 € on the worked configuration,
    the year's cotisation very nearly paying the year's acquisition cost — then thin
    positive margins that grow as the tariff climbs.  Within policy year 1 the monthly
    frame shows the shape the annual grid could not: +633,73 € in month 0, where the whole
    annual cotisation is collected against the acquisition cost, then eleven negative
    months of claims and maintenance.  The ``constante`` form inverts the annual picture:
    strongly positive in the first year and carrying a real *provision mathématique*
    against the later years.
    """
    return premiums(t) - claims(t) - expenses(t)


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvabilité II best estimate is
    ``sum v(t) liability_cf(t)`` over the relevant risk-free term structure, plus a risk
    margin.  Published as a column beside :func:`net_cf` so the sign convention is
    verifiable in the frame rather than only in prose.
    """
    return -net_cf(t)


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - pols_death(t) - pols_ptia(t) - pols_lapse(t)``.  The
    recursion multiplies ``(1 - q_dm - q_pm)(1 - w_m)`` while the three exits are formed
    separately, so the two agree by algebra when — and only when — every one of them is
    read at the same ``t``.  What it catches is therefore a **misindexed recursion**:
    rolling forward with ``w_m(t-1)`` or ``q_dm(t+1)``, or dropping the PTIA decrement
    from the recursion while still paying PTIA claims, all leave a residual here.  On the
    monthly grid it must close **month by month**, not only at anniversaries.  In the
    final projected policy year ``pols_lapse`` is zero and, at ``t = proj_len() - 1``,
    ``pols_if(t+1) = pols_if(proj_len())`` is the expiring cohort, so the identity closes
    there too.
    """
    return (pols_if(t) - pols_if(t + 1)
            - pols_death(t) - pols_ptia(t) - pols_lapse(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the
    signed residual of the month that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(proj_len()))


def check_decrement_closure_resid(t):
    """The cumulative decrement-closure residual at the end of month t; zero.

    ``sum of (deaths + PTIA claims + lapses) up to t, plus pols_if(t+1), less the original
    policy``.  It is the notes' own closure identity — ``0.06737020 + 0.00516859 +
    0.64859269 + 0.27886852 = 1`` on the worked configuration — asserted at every ``t``
    rather than only at the horizon, and it is built by **direct summation over the exit
    cells**, with no reference to the recursion that produced ``pols_if``.  The survivor
    term is exactly the annual-step model's 0,27886852; the three exit sums are not,
    because a decrementing block reaches the claim decrements later in the year and more
    of the cohort therefore leaves as a lapse.

    That independence is what makes it more than the telescope of
    :func:`check_pols_roll_fwd`.  It catches a wrong starting cohort, an exit counted in
    two places, and above all a **life that leaves through the PTIA decrement and
    reappears in force** — the arithmetic form of paying the capital twice, which is this
    product's first-order failure mode and which the cash flows alone would not reveal.
    """
    exits = sum(pols_death(s) + pols_ptia(s) + pols_lapse(s)
                for s in range(t + 1))
    return exits + pols_if(t + 1) - pols_if_init()


def check_decrement_closure():
    """True when claim events, lapses and survivors account for the whole cohort at every t.

    No argument, one bool over all t, the library-wide shape;
    :func:`check_decrement_closure_resid` gives the signed residual of the month that
    failed.
    """
    return all(abs(check_decrement_closure_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(proj_len()))


def check_ptia_gate_resid(t):
    """The PTIA cessation residual in month t; zero everywhere.

    ``ptia_rate(t) + pols_ptia(t) + claims(t, "PTIA")`` in every month whose attained age
    has reached ``ptia_end_age()``, and zero before that.

    **Trivially zero by construction** when the gate in :func:`ptia_rate` is right, since
    that cells returns exactly 0 past the cessation age.  It is published because the gate
    is written twice — there and here, each recomputed from ``age(t)`` and the model
    point — so the two disagree if either is wrong.  What it catches: a taper instead of a
    hard cut-off, ``>`` where ``>=`` belongs (which would keep PTIA cover for the whole of
    the year at the cessation age), a gate read off ``cover_end_age`` instead of
    ``ptia_end_age``, and a gate applied to the death decrement instead of the PTIA one.
    On the worked configuration it is exercised at ``t = 84 ... 203`` — the whole of the
    policy year at attained age 65 onwards — and on model point 11, which enters at
    exactly ``ptia_end_age``, at every ``t``.
    """
    if age(t) < ptia_end_age():
        return 0.0
    return ptia_rate(t) + pols_ptia(t) + claims(t, "PTIA")


def check_ptia_gate():
    """True when the PTIA cover is exactly off from the cessation age in every month.

    No argument, one bool over all t;  :func:`check_ptia_gate_resid` gives the signed
    residual of the month that failed.
    """
    return all(abs(check_ptia_gate_resid(t)) <= roll_fwd_tol         # noqa: F821
               for t in range(proj_len()))


def check_no_cash_value_resid(t):
    """The lapse-benefit residual in month t: ``claims(t, "LAPSE")``; zero everywhere.

    **Trivially zero by construction**, because ``claims(t, "LAPSE")`` returns a literal
    zero.  It is published because the zero is a statutory fact rather than a modelling
    choice — art. L. 132-23 forbids both *rachat* and *réduction* on a temporaire décès —
    and because the failure it guards against is not an arithmetic slip but an import: a
    reader arriving from a US model with cash surrender values wires an account value or a
    surrender scale into the lapse decrement, and every total in the frame still looks
    plausible.  A named check that must stay at zero makes that edit fail loudly.
    """
    return claims(t, "LAPSE")


def check_no_cash_value():
    """True when a lapse pays nothing in every projected month.

    No argument, one bool over all t;  :func:`check_no_cash_value_resid` gives the signed
    residual of the month that failed.
    """
    return all(abs(check_no_cash_value_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, one row per **month**, indexed by the 0-based index t.

    ``pols_if`` is the start-of-**month** count, which is the weight applied to every cash
    flow on the same row.  ``expenses`` is the notes' total and **includes**
    ``commissions``, which is published beside it because the notes' worked-example table
    prints both; ``net_cf`` subtracts the total once.  ``claims_lapse`` is a column of
    zeros by statute — there is no surrender value — and is published rather than dropped.
    ``liability_cf`` is ``net_cf`` outgo-positive.

    The frame runs ``t = 0 ... proj_len() - 1`` — ``proj_len()`` rows, 204 on the worked
    configuration — and stops: cover ceases at the *échéance* following ``cover_end_age``
    with nothing payable.  :func:`result_cf_annual` sums it into policy years, which is
    the view the notes' worked example is stated on and the one to lay beside the
    annual-step model this replaced.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_ptia": [claims(t, "PTIA") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by ``policy_year``.

    Every cash flow column is the total of its twelve months; ``pols_if`` is the count at
    the **start** of the policy year, ``pols_if(12 * (policy_year - 1))``, which is the
    number the annual-step model this replaced carried on the same row.  It is the monthly
    frame **regrouped and never a second projection**, which is what lets the notes'
    annual worked example stay in the notes and still be asserted.

    On the nine annual-mode model points the two grids agree exactly on three columns —
    ``pols_if``, ``premiums`` and ``commissions`` — because an annual cotisation is
    collected on the anniversary and weighted by the anniversary in-force under either
    grid, and the commission is a policy-year rate on it.  They do **not** agree on
    ``claims_death``, ``claims_ptia`` or ``expenses``, which now fall where they happen
    rather than at the anniversary, and so not on ``net_cf``: 10 094,20 € of death claims
    over the worked configuration against the annual grid's 10 396,90 €, and 2 666,69 € of
    expense against 2 676,38 €.  That gap is the point of the finer grid.
    """
    df = result_cf()
    years = pd.Index([duration(t) + 1 for t in df.index],            # noqa: F821
                     name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_pols():
    """Result table of policy counts, decrement rates and per-policy amounts, indexed by t.

    The same monthly frame as :func:`result_cf`: ``t = 0 ... proj_len() - 1``.  Each
    annual rate is published beside the monthly rate derived from it, so the two speeds of
    the conversion can be read off one table: ``mort_rate`` / ``ptia_rate`` /
    ``lapse_rate`` are the **annual** rates of the policy year containing the month, and
    ``mort_rate_mth`` / ``ptia_rate_mth`` / ``lapse_rate_mth`` the rates actually applied
    in it.  ``prem_pp`` is likewise the year's annual cotisation and ``prem_inst_pp`` the
    instalment collected in the month.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_ptia": [pols_ptia(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) for t in ts],
            "ptia_rate": [ptia_rate(t) for t in ts],
            "ptia_rate_mth": [ptia_rate_mth(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) for t in ts],
            "prem_rate": [prem_rate(t) for t in ts],
            "prem_pp": [prem_pp(t) for t in ts],
            "prem_inst_pp": [prem_inst_pp(t) for t in ts],
            "benefit_pp": [benefit_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

ptia_ratio = 0.2

suicide_year1_factor = 0.98

tech_rate = 0.005

tariff_drift = 0.0

acc_share = 0.0

shock_lapse_beta = 0.0

shock_lapse_g0 = 0.1

sel_lapse_lambda = 0.0

sel_lapse_ref = 0.3

acq_expense = 250.0

maint_expense = 25.0

expense_infl = 0.02

claim_expense = 150.0

comm_rate_init = 0.4

comm_rate_renew = 0.05

roll_fwd_tol = 1e-10

pd = ("Module", "pandas")
