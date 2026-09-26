# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.BU_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **policy months**, 0-based: ``t = 0`` is the first projected month — the
month of inception for a new-business point, the valuation month for an in-force one —
and ``proj_len()`` is the **number** of projected months, the exclusive end of the frame,
so :func:`result_cf` runs ``t = 0 ... proj_len() - 1`` and ends there. On the anchor cell
that is ``proj_len() == 444``, i.e. 444 monthly rows ending at ``t = 443``.
Nothing is payable at the end: cover ceases at attained age ``cover_end_age``, there is
no maturity value, no surrender value and no death benefit, and a claim still in payment
at the horizon simply stops.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/berufsunfaehigkeit/``, read at run time rather than stored inside the model.
The model folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no
embedded values — so a diff of the model shows logic changes only, and an input can be
edited or swapped without rewriting the model. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model through
modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``BU_DE_S`` folder without its parent's CSVs produces a model that reads and then fails
on first evaluation.

Each table has a filename Reference and a reader Cells, both on :mod:`~.BU_DE_S.Data`,
reached here through the ``data`` Reference:

========================  =================================  ==========================
Reference                 Cells                              File
========================  =================================  ==========================
model_point_file          data.model_point_table()           model_point_table.csv
inception_file            data.inception_table()             inception_table.csv
claim_duration_file       data.claim_duration_table()        claim_duration_table.csv
mortality_file            data.mortality_table()             mortality_table.csv
occupation_file           data.occupation_table()            occupation_table.csv
lapse_file                data.lapse_table()                 lapse_table.csv
freq_loading_file         data.freq_loading_table()          freq_loading_table.csv
========================  =================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for annual rates with ``*_rate_mth`` for their monthly
equivalents, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with an uppercase
``kind`` string, ``pols_if_at(t, timing)`` for the end-of-month read. The technical notes
use compact actuarial symbols instead. The mapping is:

=========================  ==============================  ===============================
Notes symbol               Cells                           Meaning
=========================  ==============================  ===============================
(none)                     model_point()                   The selected model point row
n                          proj_len()                      Number of projected months
(none)                     first_len()                     Months in the pricing run
u(t)                       duration_mth(t)                 Elapsed policy months at t
y(t)                       policy_year(t)                  Policy year containing t
x(t)                       age(t)                          Attained age, ALB
(none)                     age_first(s)                    Attained age in the pricing run
z                          (the cohort index)              Months since onset of the BU
(none)                     claim_year(z)                   Claim year containing z
k                          (the run-off slot)              Months into the § 174 run-off
R                          bu_rente_mth()                  Agreed monthly BU-Rente
R(t)                       bu_rente_pp(t)                  Insured BU-Rente at t
R_p(t, z)                  rente_pay_pp(t, z)              BU-Rente in payment, cohort z
K                          karenz_months()                 Karenzzeit, months
g_L                        leistungsdyn_rate()             Leistungsdynamik p.a.
g_B                        beitragsdyn_rate()              Beitragsdynamik p.a.
(1 + g_B)^(y-1)            dyn_factor(t)                   Beitragsdynamik factor at t
(1 + g_L)^((z-1)//12)      leistungsdyn_factor(z)          Leistungsdynamik factor at z
theta                      beitragsverrechnung()           Zahlbeitrag / Bruttobeitrag
rho                        risk_factor()                   Risikozuschlag on the premium
phi                        freq_load()                     Ratenzahlungszuschlag
M                          prem_mode_months()              Months between instalments
kappa                      occ_factor()                    Occupational loading
alpha                      accept_factor                   Anerkennungsquote factor
upsilon                    au_uplift()                     AU-Klausel inception uplift
P                          prem_gross_level_pp()           Level annual Bruttobeitrag
(none)                     prem_gross_ann_pp(t)            Annual Bruttobeitrag at t
(none)                     prem_due(t)                     1 in a payment month, else 0
P_b(t)                     prem_gross_pp(t)                Bruttobeitrag instalment at t
P_z(t)                     prem_zahl_pp(t)                 Zahlbeitrag instalment at t
(1 - theta) P_b(t)         surplus_credit_pp(t)            Beitragsverrechnung instalment
BS_unit                    beitragssumme_unit()            Beitragssumme per 1 EUR p.a.
i(x)                       inc_rate_base(t)                Table inception rate at x(t)
i(x) kappa alpha upsilon   inc_rate(t)                     Composed annual inception rate
i_m(t)                     inc_rate_mth(t)                 The same, monthly
r(z)                       recov_rate(z)                   Annual reactivation rate
r_m(z)                     recov_rate_mth(z)               The same, monthly
q^a(x)                     mort_rate(t)                    Annual active-lives mortality
q^a_m(t)                   mort_rate_mth(t)                The same, monthly
s(z)                       mort_dis_sel_factor(z)          Disabled-mortality select factor
q^i(x, z)                  mort_rate_dis(t, z)             Annual disabled-lives mortality
q^i_m(t, z)                mort_rate_dis_mth(t, z)         The same, monthly
w(y)                       lapse_rate(t)                   Annual Stornoquote
w_m(t)                     lapse_rate_mth(t)               The same, monthly
lambda_i .. lambda_a       inc_load_first ..               The four first-order loads
v^t                        disc_first(t)                   Rechnungszins discount factor
l_a(t)                     pols_actv(t)                    Aktiv, start of month t
l_d(t, z)                  pols_dis_dur(t, z)              Leistungspflichtig at duration z
(sum over z)               pols_dis(t)                     The whole disabled ledger
l_r(t, k)                  pols_runoff_slot(t, k)          § 174 run-off slot k
V_r(t, k)                  runoff_val(t, k)                The same, times its BU-Rente
(sum over k)               pols_runoff(t)                  The whole run-off ledger
L(t)                       pols_if(t)                      In force at the start of t
(none)                     pols_if_at(t, timing)           BEG / END of month t
L_p(t)                     pols_prem(t)                    Premium-paying count
(none)                     pols_inception(t)               Aktiv -> leistungspflichtig
(none)                     pols_recovery(t)                Claim terminations into run-off
(none)                     pols_reactivation(t)            Run-off completions to aktiv
(none)                     pols_death(t)                   Deaths out of all three ledgers
(none)                     pols_lapse(t)                   Lapses, from pols_actv only
(the shadow ledgers)       ``*_first``                      The first-order pricing run
premiums(t)                premiums(t)                     Gross Bruttobeitrag income
surplus_credit(t)          surplus_credit(t)               Beitragsverrechnung returned
claims_bu_rente etc.       claims(t, kind)                 Benefit outgo by kind
expenses(t)                expenses(t)                     Acquisition and administration
claim_expenses(t)          claim_expenses(t)               Leistungsbearbeitungskosten
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ===============================

Five names needed care.

``occ_factor`` and ``risk_factor`` are **not two spellings of the same thing**.
:func:`occ_factor` loads the *inception rate* and reaches the premium only through the
equivalence, so it moves every claim and every decrement;
:func:`risk_factor` loads the *Bruttobeitrag* alone and leaves the claims untouched. A
*Risikozuschlag* prices an individually assessed impairment that the base table does not
carry and this model does not carry either, so a loaded contract is priced above its own
modelled cost. The direction is stated rather than corrected.

``bu_rente_pp`` and ``rente_pay_pp`` run on **different clocks**. :func:`bu_rente_pp` is
the *insured* monthly *BU-Rente*, escalating at ``beitragsdyn_rate`` on each **policy**
anniversary before any claim; :func:`rente_pay_pp` is the amount **in payment**,
escalating at ``leistungsdyn_rate`` on each anniversary of the **onset**. Escalating the
*BU-Rente* in payment on the policy anniversary is a numbered pitfall.

``pols_prem`` is not ``pols_if``. It is ``pols_actv(t)`` **plus** the disabled cohorts
still inside the *Karenzzeit*: the *Beitragsbefreiung* runs with the benefit, so a life
inside the *Karenzzeit* is *berufsunfaehig* and still pays. Weighting the premium by
``pols_if`` charges premium to lives in claim and silently deletes the
*Beitragsbefreiung*, which is core cover.

``pols_recovery`` feeds the **run-off**, not the active ledger. A life whose claim ends
in month ``t`` is still paid in ``t+1``, ``t+2`` and ``t+3`` and only then rejoins
``pols_actv``, because § 174 VVG leaves the insurer liable to the end of the third month
after the notice reaches the policyholder. :func:`pols_reactivation` is the return arc
and is three months behind :func:`pols_recovery`.

The ``*_first`` cells are a **second projection**, not a variant of the first. They run
the same four-ledger chain on *Rechnungsgrundlagen erster Ordnung* — inception x 1.30,
reactivation x 0.70, disabled-lives mortality x 0.80, active-lives mortality x 0.80,
**no lapse** — over the contract's **original** term from ``entry_age``, indexed by
``s`` rather than ``t``. They exist only to fix :func:`prem_gross_level_pp` and never
touch a published cash flow. Running them from inception rather than from the valuation
date is what gives an in-force model point the *Bruttobeitrag* its contract was actually
struck at: model point 6 is model point 1 fifteen years on, and the two must price the
same.

.. rubric:: The premium is derived, not read

No German BU rate card exists in this library's source corpus, so the *Bruttobeitrag* is
an **output of a stated first-order basis**. With ``d(s) = disc_first(s)``, the
equivalence is

    P x PV_prem = PV_rente + PV_wgh + PV_cost + PV_admin
                + acq_rate x P x BS_unit + admin_prem_rate x P x PV_prem

which is **linear in P**, because both the acquisition and the proportional
administration loadings are proportional to it, so

    P = (PV_rente + PV_wgh + PV_cost + PV_admin)
        / ( PV_prem x (1 - admin_prem_rate) - acq_rate x BS_unit )

and :func:`prem_gross_level_pp` is ``risk_factor() x P``, or ``risk_factor() x
gross_prem_ann()`` where the model point overrides it. **The recursion is acyclic**: no
decrement in this model depends on the premium, so nothing in the ``pv_*`` cells depends
on ``P``. The equivalence is struck **before** the *Risikozuschlag* and **without lapse**,
which is deliberate on both counts — German pricing does not anticipate lapse, because a
lapse releases a liability and a prudent basis does not anticipate a favourable event.

``PV_prem`` is struck on ``P / 12`` in every month, so the *Ratenzahlungszuschlag*
``freq_load`` is a genuine loading on top of the tariff premium rather than a
re-expression of it. That is the market's own construction and it is why an annual payer
and a monthly payer do not pay the same present value.

.. rubric:: The four-ledger chain, and the two things it must not do

At the **end** of month ``t``, in order: from the active ledger, deaths, then lapses on
the survivors, then inceptions on the survivors of both; from each disabled cohort,
deaths, then terminations on the survivors, the terminations entering run-off slot 1
carrying the *BU-Rente* they were on; from the run-off, deaths at **active-lives**
mortality — these lives have recovered — then slot 1 to 2, slot 2 to 3, and the slot-3
survivors back to ``pols_actv`` with the *Wiedereingliederungshilfe*.

Death and lapse are the **only** exits, so

    pols_if(t+1) = pols_if(t) - pols_death(t) - pols_lapse(t)

and inception, recovery and reactivation are internal transfers that must not appear in
it. Putting them there is how a multi-state model silently loses mass, and it is why
:func:`pols_if` is built by that roll-forward and :func:`check_states` then compares it
against the three ledgers rather than restating a sum of them.

At the *Leistungsendalter* the benefit stops but **the mass is held, not deleted**: once
``age(t) >= benefit_end_age()`` every payment and every claim-maintenance cost is zero
while the ledgers keep rolling, so both state identities still close. Those lives do not
resume paying premium — they are still *berufsunfaehig*, and the *Beitragsbefreiung* is
read here as keyed to the state rather than to the payment **[std]**. The alternative
reading is defensible and is named so that a user who takes it knows what to change.

.. rubric:: The run-off carries amounts as well as counts

:func:`runoff_val` is a **value** ledger: the run-off population times the monthly
*BU-Rente* it is being paid. A cohort entering the run-off keeps the *BU-Rente* it was on
at the *Nachpruefung* date and receives no further *Leistungsdynamik* **[std]** — three
months is inside one anniversary of onset in every realistic case, so the simplification
costs nothing and removes a second duration dimension from the run-off. The disabled
ledger carries a value vector for the same reason, so that the month's *BU-Rente* outgo
is one sum over a list rather than a lookup per cohort.

.. rubric:: Modules that are off in the base run

- **The *AU-Klausel***, ``au_klausel`` true on model point 10 with ``au_uplift`` 1.00.
  The machinery is present and demonstrably inert until a user supplies an uplift: no
  source quantifies what six months of certified *Arbeitsunfaehigkeit* adds to the
  incidence, so shipping a number would be an invention.
- **Lapse selection**, not implemented. BU lapse is strongly selective — the healthy
  leave, the impaired cannot — so a non-selective rate understates the average inception
  rate of the surviving book, increasingly with duration. The direction is known and
  one-sided; the size is not, and stacking a selection loading on an already-``[std]``
  inception proxy would compound two unsourced choices.
- **Premium-shock lapse**, not implemented. On the ``dynamik`` form the take-up of the
  increases is folded into the **effective** ``beitragsdyn_rate`` rather than modelled as
  a decision. That also keeps the equivalence acyclic: a shock-lapse module would make
  the lapse rate depend on the premium, which depends on the projection.
- **The *Zahlbeitrag* re-rating.** ``beitragsverrechnung`` is held constant for the whole
  projection. It is the model's single largest discretionary assumption and the one the
  product's own consumer literature warns about; a user modelling the risk raises
  :func:`surplus_credit` toward zero over time, which raises collected premium toward the
  *Bruttobeitrag* and moves nothing else.
- **The *Nachversicherungsgarantie***, not modelled at all: it needs a take-up assumption
  *and* an anti-selection loading on the incremental cover, and neither is sourceable.

.. rubric:: Four absences are product facts

There is **no account value and no surrender value**, so no ``av_pp_at`` exists and
``claims(t, "LAPSE")`` is structurally zero at every ``t`` — a lapse removes the policy
and pays nothing. § 169 VVG through § 176 gives this contract a real *Rueckkaufswert* and
§ 165 a real *beitragsfreie BU-Rente*, but both are the release of a reserve this model
deliberately does not compute, and the zero column states the scope rather than hiding
it. There is **no death benefit**: an SBU pays nothing on death, before or during a
claim, so :func:`pols_death` is a decrement and never a cash flow and there is no
``claims_death`` column for a reader arriving from a term-life model to find. There is
**no maturity benefit**. And there is **no acknowledged state**: this model pays from
onset and does not model the *Leistungspruefung* delay, so the *Anerkenntnis* is a timing
event with no cash-flow consequence here — right in amount, early in timing.

.. rubric:: Unisex

``sex`` is a model-point attribute for reporting purposes only and **must not** enter the
premium: sex-differentiated pricing has been unlawful in Germany for contracts written
from 21 December 2012. The shipped decrement tables are unisex, so in the base
parameterization ``sex`` moves nothing at all — model points 1 and 2 differ in it and in
nothing else, and their frames are identical.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — the *Bruttobeitrag* in, the
*Beitragsverrechnung*, claims and expenses out — which is the library-wide sign.
:func:`liability_cf` publishes the same stream outgo-positive, ``-net_cf(t)`` exactly, so
a best-estimate liability is ``sum v(t) liability_cf(t)`` over whatever discount curve the
valuation layer supplies. Both are columns of :func:`result_cf`, so the identity is
verifiable in the frame rather than only in prose. The shape to expect is a large
first-month strain — the whole acquisition charge falls in month 0, at 2.5 % of a
37-year *Beitragssumme* — then thin positive margins that thin further as the inception
rate accelerates from the mid-forties.
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


def status():
    """The state at ``t = 0``: ``aktiv`` or ``leistung``.

    ``aktiv`` seeds the whole policy into :func:`pols_actv`; ``leistung`` seeds it into
    the disabled ledger at duration :func:`seed_claim_dur` instead, which is how an
    in-force claim is valued.  It does **not** affect the first-order shadow used to
    price the contract: that always runs from inception as an active life, because the
    *Bruttobeitrag* was struck there.
    """
    v = model_point()["status"]
    if v not in ("aktiv", "leistung"):
        raise ValueError("invalid status")
    return v


def entry_age():
    """The *Eintrittsalter*: age last birthday at inception.

    Age last birthday advancing at the **policy anniversary** rather than the birthday
    **[std]** — the model carries no dates, so :func:`age` steps every twelfth month from
    here.  An implementation on real dates carries a fractional offset of at most one
    year.
    """
    return int(model_point()["entry_age"])


def sex():
    """The insured's sex, M or F.  **Reporting only — it must not price.**

    Sex-differentiated premiums and benefits have been unlawful in Germany for contracts
    written from 21 December 2012, and the shipped decrement tables are unisex, so
    nothing in this model reads this cells.  The tension worth knowing is that the
    underlying *Invalidisierungswahrscheinlichkeiten* do differ by sex, so a unisex BU
    tariff embeds a mix assumption the insurer bears the risk of.  Model points 1 and 2
    differ in this attribute alone, and their frames are identical.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def berufsgruppe():
    """The occupational rating class, BG1 - BG5; the key into *occupation_table.csv*."""
    return model_point()["berufsgruppe"]


def occ_factor():
    """kappa: the occupational loading on the **inception rate**, from the table.

    BG1 1.00 (the reference class) to BG5 4.50.  It multiplies :func:`inc_rate_base` and
    therefore reaches the premium only through the equivalence — it is **not** the
    *Risikozuschlag*, which loads the premium alone and leaves the claims untouched.
    Because the flat administration and assessment costs do not scale with the risk, a
    model point three times the anchor's inception rate carries a premium slightly
    **below** three times the anchor's.
    """
    return float(data.occupation_table().loc[                        # noqa: F821
        berufsgruppe(), "occ_factor"])


def bu_rente_mth():
    """R: the agreed monthly *BU-Rente* at inception, in euros.

    The product's only substantive benefit.  Subject in the market to an
    *Angemessenheitsgrenze* capping it at 60-70 % of gross income, which is a
    underwriting rule rather than a projection parameter and is not modelled.
    """
    return float(model_point()["bu_rente_mth"])


def cover_end_age():
    """The *Endalter*: the attained age at which the *Versicherungsdauer* ends.

    Cover ceases here, so the last projected month is the last month of attained age
    ``cover_end_age() - 1``.  It is the market's dominant premium lever, because the
    inception rate accelerates from the mid-forties and cutting the *Endalter* removes
    the most expensive years of cover.
    """
    return int(model_point()["cover_end_age"])


def benefit_end_age():
    """The *Leistungsendalter*: the attained age at which the *Leistungsdauer* ends.

    A **separate contractual term** from :func:`cover_end_age` and not a synonym: model
    point 9 carries cover to 67 and benefit to 63, so a claim incepting at 62 is paid for
    one year while the premium runs for five more.  From this age the *BU-Rente* and the
    claim-maintenance cost are zero and **the disabled mass is held rather than deleted**,
    so both state identities still close.
    """
    return int(model_point()["benefit_end_age"])


def karenz_months():
    """K: the *Karenzzeit* — the agreed deferment of **payment**, in months.

    Not the six-month *Prognosezeitraum*, which is part of the *definition* of
    *Berufsunfaehigkeit*; the *Karenzzeit* defers payment on a BU already established.
    Cohorts at duration ``z <= K`` are *berufsunfaehig*, are **not** paid, and **still
    pay premium**, because the *Beitragsbefreiung* runs with the benefit **[std]**.
    """
    return int(model_point()["karenz_months"])


def leistungsdyn_rate():
    """g_L: the *Leistungsdynamik* — annual escalation of the *BU-Rente* **in payment**.

    Steps on each anniversary of the **onset**, not of the policy.  Compounding 2 % over
    a claim that can run thirty years raises the final payment to about 1.70x the first.
    """
    return float(model_point()["leistungsdyn_rate"])


def premium_form():
    """The premium form: ``level`` or ``dynamik``.

    ``level`` is a *Bruttobeitrag* guaranteed flat for the whole term.  ``dynamik`` is the
    *Beitragsdynamik*: premium and insured *BU-Rente* escalate together at
    :func:`beitragsdyn_rate` on each policy anniversary, and the whole escalating stream
    is priced by one equivalence at inception.  That is internally consistent but is
    **not** the German market's practice, which prices each increment at the attained age
    reached, so a given increase buys less than proportional cover; the direction is
    recorded rather than corrected.
    """
    v = model_point()["premium_form"]
    if v not in ("level", "dynamik"):
        raise ValueError("invalid premium_form")
    return v


def beitragsdyn_rate():
    """g_B: the **effective** *Beitragsdynamik* rate, net of declined increases.

    Zero on the ``level`` form.  Folding take-up into an effective rate — a policyholder
    accepting two increases in three is represented by a lower rate — is the honest
    treatment of an option whose decline behaviour no source quantifies, and it keeps the
    equivalence acyclic.
    """
    if premium_form() == "level":
        return 0.0
    return float(model_point()["beitragsdyn_rate"])


def prem_mode():
    """The payment frequency: ``annual``, ``half_yearly``, ``quarterly`` or ``monthly``.

    The key into *freq_loading_table.csv*, which supplies both the months between
    instalments and the *Ratenzahlungszuschlag*.
    """
    v = model_point()["prem_mode"]
    if v not in ("annual", "half_yearly", "quarterly", "monthly"):
        raise ValueError("invalid prem_mode")
    return v


def prem_mode_months():
    """M: the number of months between premium instalments — 12, 6, 3 or 1.

    A premium falls in month ``t`` when ``duration_mth(t)`` is a multiple of it, so on
    the anchor cell one falls every month and on model point 4 one falls in months
    0, 12, 24, ... and is twelve times as large.  Carrying the frequency as a parameter
    rather than smoothing it is the whole reason this model runs on a monthly grid.
    """
    return int(data.freq_loading_table().loc[                        # noqa: F821
        prem_mode(), "prem_mode_months"])


def freq_load():
    """phi: the *Ratenzahlungszuschlag* on the tariff premium **[std]**.

    1.00 annual, 1.02 half-yearly, 1.03 quarterly, 1.05 monthly.  It loads the
    *Bruttobeitrag* and the *Beitragsverrechnung* **together**, so
    :func:`beitragsverrechnung` stays exactly the ratio the tariff quotes and the loading
    is invisible in the *Brutto* / *Zahl* split.
    """
    return float(data.freq_loading_table().loc[                      # noqa: F821
        prem_mode(), "freq_load"])


def gross_prem_ann():
    """The annual *Bruttobeitrag* override, in euros; **0 means derive by equivalence**.

    Only model point 13 supplies one.  A real tariff would read the premium off a rate
    card; no German BU rate card of any kind was obtained for this library, so the
    derivation is the default and the override is the exception.
    """
    return float(model_point()["gross_prem_ann"])


def beitragsverrechnung():
    """theta: the *Zahlbeitrag* / *Bruttobeitrag* ratio, held constant **[std]**.

    0.70 on twelve of the thirteen model points, against a recalled market range of
    0.50 - 0.80.  This is the *Beitragsverrechnung*: the anticipated *Ueberschuss*
    credited against the premium in advance under § 153 VVG through § 176, with the MindZV
    risk-result minimum allocation behind it.  Holding it constant is the model's single
    largest discretionary assumption; the insurer may reduce the credit as far as the
    *Bruttobeitrag* and no further, and across the recalled range collected premium moves
    by more than 40 % either way.
    """
    return float(model_point()["beitragsverrechnung"])


def risk_factor():
    """rho: the *Risikozuschlag* — a multiplier on the *Bruttobeitrag* **and nothing else**.

    It prices an individually assessed impairment that the base inception table does not
    carry, and which this model does not carry either, so the loaded contract is
    projected above its own modelled cost.  Contrast :func:`occ_factor`, which loads the
    inception rate and so moves every claim and every decrement.
    """
    return float(model_point()["risk_factor"])


def au_klausel():
    """Whether the *AU-Klausel* is elected.

    The clause pays on a certificate of six months' *Arbeitsunfaehigkeit* without a BU
    determination.  Carried as machinery whose effect runs entirely through
    :func:`au_uplift`, which ships at 1.00 everywhere, so the switch is demonstrably inert
    until a user supplies a number.
    """
    return bool(model_point()["au_klausel"])


def au_uplift():
    """upsilon: the inception uplift when the *AU-Klausel* is on; 1.00 when it is off.

    **Shipped at 1.00 everywhere** — no source in this library's corpus quantifies what
    the clause adds to the incidence, and inventing a loading would be worse than leaving
    the machinery visibly inert.  It is one of the three multipliers composed into
    :func:`inc_rate` and the only one that can be switched off by a model point column.
    """
    if not au_klausel():
        return 1.0
    return float(model_point()["au_uplift"])


def wiedereingliederung_months():
    """The *Wiedereingliederungshilfe*, expressed in monthly *Renten*; 0 switches it off.

    Paid on the **completion** of the run-off, so a life that dies inside the run-off
    never returns to work and is paid nothing.  Paying it on every recovery instead
    overstates it, and the difference is exactly the run-off's own mortality.
    """
    return int(model_point()["wiedereingliederung_months"])


def duration_init_months():
    """Elapsed policy months at ``t = 0``; 0 for a new-business point.

    It shortens :func:`proj_len`, shifts :func:`age` and :func:`policy_year`, decides
    which months carry a premium instalment, and **suppresses the acquisition charge**:
    an in-force point has already incurred it, and charging it again at the valuation
    date is a numbered pitfall.  It does *not* touch the first-order shadow, which always
    runs from inception.
    """
    return int(model_point()["duration_init_months"])


def claim_duration_init():
    """Months since the onset of the BU at ``t = 0``, for a ``leistung`` model point.

    Zero on every ``aktiv`` point.  See :func:`seed_claim_dur` for the cohort it seeds.
    """
    return int(model_point()["claim_duration_init"])


def pols_if_init():
    """The policy count at ``t = 0``: **1.0 for every model point**.

    This is a per-policy probability projection, one model point at a time, so every
    ledger is a probability and every cash flow an expected amount per policy in force at
    the valuation date.  ``result_cf()``'s first ``pols_if`` value is this number exactly.
    """
    return 1.0


# --- the time frame ---

def proj_len():
    """n: the **number of projected months**, so the frame runs ``t = 0 ... proj_len() - 1``.

    ``12 x (cover_end_age() - entry_age()) - duration_init_months()``.  Cover ceases
    at attained age ``cover_end_age()``, so the last projected month is the last month of
    attained age ``cover_end_age() - 1``, index ``proj_len() - 1``.  On the anchor cell
    that is ``12 x (67 - 30) = 444`` monthly rows, the last of them ``t = 443``.

    This is the library's reading of ``proj_len()`` — the **exclusive end** of the frame,
    the row count rather than the last index — and ``result_cf().index[-1] ==
    proj_len() - 1`` is asserted for every model point.
    """
    return 12 * (cover_end_age() - entry_age()) - duration_init_months()


def first_len():
    """The **number of months** in the **first-order pricing run**, from inception.

    ``12 x (cover_end_age() - entry_age())``, which is ``proj_len() +
    duration_init_months()``, so the run is ``s = 0 ... first_len() - 1``.
    :func:`pols_actv_first` admits ``s == first_len()`` as well, the month past the end,
    exactly as the roll-forward checks read ``t == proj_len()`` on the main frame.  The
    shadow ledgers run over the contract's original term whatever duration the model point
    has already run, because the *Bruttobeitrag* was struck at inception and does not
    change afterwards.
    """
    return 12 * (cover_end_age() - entry_age())


def duration_mth(t):
    """u(t): elapsed policy months at the start of month t.

    ``duration_init_months() + t``.  Defined for negative ``t`` as well, because
    :func:`bu_rente_pp` reads it there to recover the insured *BU-Rente* at the onset of a
    claim that began before the valuation date.
    """
    return duration_init_months() + t


def policy_year(t):
    """y(t): the policy year containing month t, 1-based.

    ``duration_mth(t) // 12 + 1``, floored at 1 so that a negative ``t`` reaching back
    before inception reads as policy year 1 rather than as a year 0 the tariff never had.
    """
    return max(1, duration_mth(t) // 12 + 1)


def age(t):
    """x(t): the attained age at month t, age last birthday.

    ``entry_age() + duration_mth(t) // 12``, so it steps at the **policy anniversary**
    rather than at a birthday the model does not carry **[std]**.  Every rate lookup in
    the model is keyed by this age.
    """
    return entry_age() + max(0, duration_mth(t)) // 12


def age_first(s):
    """The attained age at month s of the **first-order pricing run**.

    ``entry_age() + s // 12``: the shadow ledgers run from inception, so their age clock
    ignores ``duration_init_months()``.
    """
    return entry_age() + max(0, s) // 12


def policy_year_first(s):
    """The policy year containing month s of the **first-order pricing run**, 1-based."""
    return max(0, s) // 12 + 1


def claim_year(z):
    """The claim year containing claim duration z, 1-based and capped at the table's last row.

    ``(z - 1) // 12 + 1``, capped at 11: rows 1-10 of *claim_duration_table.csv* are claim
    years 1-10 and row 11 is the ultimate.  Duration ``z = 1`` is the first month a claim
    can be paid, so ``z = 1 ... 12`` is claim year 1 and ``z = 13`` opens claim year 2.
    """
    return min(11, max(1, (z - 1) // 12 + 1))


def seed_claim_dur():
    """The claim-duration cohort the initial population occupies, or 0 if it is not seeded.

    ``claim_duration_init() + 1`` on a ``leistung`` model point, 0 on an ``aktiv`` one: a
    claim whose onset was ``claim_duration_init()`` months before the valuation month is
    in its next month of duration at the start of it, exactly as a claim recognised at the
    end of month ``t`` sits at ``z = 1`` at the start of month ``t + 1``.
    """
    return claim_duration_init() + 1 if status() == "leistung" else 0


def max_claim_dur():
    """The longest claim duration the cohort vectors have to carry.

    ``proj_len() + seed_claim_dur() + 1``.  A cohort seeded at ``seed_claim_dur()``
    reaches ``seed_claim_dur() + proj_len()`` at ``t = proj_len()``, the month past the
    end of the frame that the roll-forward checks read, and the extra element is what
    makes the duration shift lossless — the last slot is structurally zero, so nothing
    falls off the end.
    """
    return proj_len() + seed_claim_dur() + 1


def cohort_len(t):
    """The number of claim-duration cohorts that can be non-zero at the start of month t.

    ``min(max_claim_dur(), t + seed_claim_dur() + 1)``.  The vectors are truncated to this
    length rather than carried at full :func:`max_claim_dur` from month zero, which is
    purely a cost decision: :func:`pols_dis_dur` returns zero past the end of the list, so
    nothing about the two-dimensional view changes.
    """
    return min(max_claim_dur(), t + seed_claim_dur() + 1)


def cohort_len_first(s):
    """The cohort-vector length in the first-order pricing run at month s.

    ``min(first_len() + 1, s + 1)``: the shadow chain always starts as a new-business
    active life, so it carries no seeded claim and its first cohort appears at ``s = 1``.
    """
    return min(first_len() + 1, s + 1)


# --- the rate tables, keyed by age ---

def inc_rate_at_age(x):
    """i(x): the table *Invalidisierungswahrscheinlichkeit* at attained age x, per year.

    A lookup into *inception_table.csv*, clamped to the table's range 18-66.  **[std]**
    and **gross of declinature**: ``accept_factor`` sits on top of it, and a
    replacement table already net of declinature must be used with that factor at 1.00 or
    the *Anerkennungsquote* is counted twice.
    """
    tbl = data.inception_table()                                     # noqa: F821
    return float(tbl.loc[min(max(x, int(tbl.index.min())),
                             int(tbl.index.max())), "inc_rate"])


def mort_rate_at_age(x):
    """q^a(x): the table active-lives mortality rate at attained age x, per year.

    A lookup into the ``mort_rate_actv`` column of *mortality_table.csv*, clamped to the
    table's range 18-70.  It applies to the *aktiv* ledger **and to the § 174 run-off**,
    whose lives have recovered and are no longer impaired lives.
    """
    tbl = data.mortality_table()                                     # noqa: F821
    return float(tbl.loc[min(max(x, int(tbl.index.min())),
                             int(tbl.index.max())), "mort_rate_actv"])


def mort_rate_dis_at_age(x):
    """q^i(x): the table disabled-lives mortality rate at attained age x, per year.

    The ``mort_rate_dis`` column of *mortality_table.csv*, **before** the claim-duration
    select factor, clamped to the table's range.  Four times the active rate at every
    age; with the first claim year's select factor of 3.0 that is twelve times active
    mortality in the first year of a claim, falling to 4.8x ultimate.  **Using one rate
    for both states is a numbered pitfall**, which is why the two live in separate
    columns.
    """
    tbl = data.mortality_table()                                     # noqa: F821
    return float(tbl.loc[min(max(x, int(tbl.index.min())),
                             int(tbl.index.max())), "mort_rate_dis"])


def recov_rates():
    """The eleven annual reactivation rates by claim year, as a tuple.

    Read once from *claim_duration_table.csv* and indexed by ``claim_year(z) - 1``.  The
    table itself is the object the projection uses; this cells exists so that the file is
    turned into a tuple once rather than once per cohort, which on a 444-month projection
    with 445 cohorts is the difference between a lookup and a quarter of a million of
    them.
    """
    tbl = data.claim_duration_table()                                # noqa: F821
    return tuple(float(tbl.loc[y, "recov_rate"]) for y in range(1, 12))


def mort_dis_sel_factors():
    """The eleven disabled-mortality select factors by claim year, as a tuple.

    3.0 / 2.0 / 1.6 / 1.4 / 1.3 and 1.2 from claim year 6, read once from
    *claim_duration_table.csv*.  See :func:`recov_rates` for why it is a tuple.
    """
    tbl = data.claim_duration_table()                                # noqa: F821
    return tuple(float(tbl.loc[y, "mort_dis_sel_factor"]) for y in range(1, 12))


# --- the best-estimate rates as composed ---

def inc_rate_base(t):
    """i(x(t)): the **table** inception rate at month t, before every multiplier.

    Published separately from :func:`inc_rate` so that the composition
    ``inc_rate = inc_rate_base x occ_factor x accept_factor x au_uplift`` is visible and
    testable rather than buried in one formula.
    """
    return inc_rate_at_age(age(t))


def inc_rate(t):
    """The **composed** annual inception rate at month t.

    ``inc_rate_base(t) x occ_factor() x accept_factor x au_uplift()`` — and those are the
    **only three** multipliers on it.  ``risk_factor`` is deliberately not among them: it
    loads the *Bruttobeitrag* and leaves every claim untouched.  Publishing the
    composition explicitly is what makes a substituted table that is already net of
    declinature visible rather than silent.
    """
    return inc_rate_base(t) * occ_factor() * accept_factor * au_uplift()  # noqa: F821


def inc_rate_mth(t):
    """i_m(t): the monthly inception rate, ``1 - (1 - inc_rate(t))^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - inc_rate(t)) ** (1.0 / 12.0)


def mort_rate(t):
    """q^a(x(t)): the **annual** active-lives mortality rate at month t.

    The library's convention is that ``mort_rate`` is annual and :func:`mort_rate_mth`
    monthly.  It applies to the *aktiv* ledger and to the § 174 run-off.
    """
    return mort_rate_at_age(age(t))


def mort_rate_mth(t):
    """q^a_m(t): the monthly active-lives mortality rate, ``1 - (1 - mort_rate(t))^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def mort_dis_sel_factor(z):
    """s(z): the disabled-mortality select factor at claim duration z.

    ``mort_dis_sel_factors()[claim_year(z) - 1]``: 3.0 in the first claim year falling to
    1.2 from the sixth.  Disabled-lives mortality is select on **claim duration**, not on
    attained age alone, and a model that drops the duration dimension understates deaths
    in exactly the months where the claim reserve is largest.
    """
    return mort_dis_sel_factors()[claim_year(z) - 1]


def mort_rate_dis(t, z):
    """q^i(x(t), z): the **annual** disabled-lives mortality rate at month t, duration z.

    ``mort_rate_dis_at_age(age(t)) x mort_dis_sel_factor(z)``.  Twelve times
    :func:`mort_rate` at duration 1 and 4.8 times it ultimately; it is never equal to it,
    at any age or duration.
    """
    return mort_rate_dis_at_age(age(t)) * mort_dis_sel_factor(z)


def mort_rate_dis_mth(t, z):
    """q^i_m(t, z): the monthly disabled-lives mortality rate at month t, duration z.

    ``1 - (1 - mort_rate_dis(t, z))^(1/12)``.  This is the published two-dimensional
    view; the ledger recursions read :func:`mort_rate_dis_mth_year` instead, which is the
    same eleven numbers held once per month rather than once per cohort.
    """
    return 1.0 - (1.0 - mort_rate_dis(t, z)) ** (1.0 / 12.0)


def mort_rate_dis_mth_year(t):
    """The eleven monthly disabled-lives mortality rates at month t, by claim year.

    ``mort_rate_dis_mth(t, z)`` depends on ``z`` only through ``claim_year(z)``, so the
    whole cohort vector needs eleven numbers per month rather than one per cohort.  This
    is what the disabled-ledger recursions read; :func:`mort_rate_dis_mth` is the
    addressable view of the same numbers and the two agree by construction.
    """
    q = mort_rate_dis_at_age(age(t))
    return tuple(1.0 - (1.0 - q * s) ** (1.0 / 12.0)
                 for s in mort_dis_sel_factors())


def recov_rate(z):
    """r(z): the **annual** *Reaktivierungswahrscheinlichkeit* at claim duration z.

    ``recov_rates()[claim_year(z) - 1]``: 0.250 in the first claim year, 0.130 in the
    second, and 0.006 from the eleventh.  **The front-loading is the point** — a claim
    that survives its first two years is very likely to run to the *Leistungsendalter* —
    and a flat rate is a modelling error rather than a simplification, worth roughly a
    factor of two on projected benefit in either direction.

    This one rate covers both recovery and *konkrete Verweisung*.  They end the benefit
    the same way, through the same *Nachpruefung*, with the same three-month run-off, and
    no public data separates them, so the model publishes exactly one
    claim-termination-other-than-death rate.
    """
    return recov_rates()[claim_year(z) - 1]


def recov_rate_mth(z):
    """r_m(z): the monthly reactivation rate, ``1 - (1 - recov_rate(z))^(1/12)`` **[std]**."""
    return 1.0 - (1.0 - recov_rate(z)) ** (1.0 / 12.0)


def recov_rate_mth_year():
    """The eleven monthly reactivation rates by claim year, as a tuple.

    Constant in ``t``, because the shipped reactivation basis carries no age-at-disablement
    dimension — DAV 1997 RI does, and that absence is named rather than hidden.  The
    disabled-ledger recursions read this; :func:`recov_rate_mth` is the addressable view.
    """
    return tuple(1.0 - (1.0 - r) ** (1.0 / 12.0) for r in recov_rates())


def lapse_rate(t):
    """w(y(t)): the **annual** *Stornoquote* in the policy year containing month t.

    4.0 % in the first two policy years falling to a 2.0 % ultimate from the sixth
    **[std]**, capped at the table's last row.  Low by the standards of every other delib
    product, and that is a product fact: once health has changed the cover cannot be
    replaced, so an insured with a claimable impairment cannot rationally lapse.  Lapse
    applies to :func:`pols_actv` only — a life in claim pays no premium and so cannot
    lapse for non-payment.
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(policy_year(t),
                             int(tbl.index.max())), "lapse_rate"])


def lapse_rate_mth(t):
    """w_m(t): the monthly lapse rate, ``1 - (1 - lapse_rate(t))^(1/12)`` **[std]**.

    Strictly below the annual rate wherever the annual rate is positive, which is the
    library's convention for the pair.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


# --- the first-order (pricing) rates ---

def inc_rate_first(s):
    """The **annual** first-order inception rate at month s of the pricing run.

    ``inc_rate_at_age(age_first(s)) x occ_factor() x accept_factor x au_uplift() x
    inc_load_first``.  Prudence for a disability product means a **higher** incidence, so
    the load is above one: a claim that starts more often.
    """
    return (inc_rate_at_age(age_first(s)) * occ_factor()
            * accept_factor * au_uplift() * inc_load_first)          # noqa: F821


def inc_rate_first_mth(s):
    """The monthly first-order inception rate at month s of the pricing run."""
    return 1.0 - (1.0 - inc_rate_first(s)) ** (1.0 / 12.0)


def recov_rate_first(z):
    """The **annual** first-order reactivation rate at claim duration z.

    ``recov_rate(z) x recov_load_first``, and the load is **below** one: prudence means a
    claim that ends less often and therefore lasts longer.
    """
    return recov_rate(z) * recov_load_first                          # noqa: F821


def recov_rate_first_mth(z):
    """The monthly first-order reactivation rate at claim duration z."""
    return 1.0 - (1.0 - recov_rate_first(z)) ** (1.0 / 12.0)


def recov_rate_first_mth_year():
    """The eleven monthly first-order reactivation rates by claim year, as a tuple."""
    return tuple(1.0 - (1.0 - r * recov_load_first) ** (1.0 / 12.0)  # noqa: F821
                 for r in recov_rates())


def mort_rate_first_mth(s):
    """The monthly first-order active-lives mortality rate at month s of the pricing run.

    ``mort_rate_at_age(age_first(s)) x mort_actv_load_first``, and that load is **below**
    one: on this contract an active death releases a liability, so it is favourable to
    the insurer and a prudent basis does not anticipate it.  The same reasoning is why
    the first-order basis carries **no lapse at all**.
    """
    return 1.0 - (1.0 - mort_rate_at_age(age_first(s))
                  * mort_actv_load_first) ** (1.0 / 12.0)            # noqa: F821


def mort_rate_dis_first_mth(s, z):
    """The monthly first-order disabled-lives mortality rate at month s, duration z.

    ``mort_rate_dis_at_age(age_first(s)) x mort_dis_sel_factor(z) x mort_dis_load_first``,
    the load again **below** one so that claims run longer on the pricing basis than on
    the best-estimate one.
    """
    return 1.0 - (1.0 - mort_rate_dis_at_age(age_first(s))
                  * mort_dis_sel_factor(z)
                  * mort_dis_load_first) ** (1.0 / 12.0)             # noqa: F821


def mort_rate_dis_first_mth_year(s):
    """The eleven monthly first-order disabled-mortality rates at month s, by claim year."""
    q = mort_rate_dis_at_age(age_first(s)) * mort_dis_load_first     # noqa: F821
    return tuple(1.0 - (1.0 - q * f) ** (1.0 / 12.0)
                 for f in mort_dis_sel_factors())


def disc_first(s):
    """v^s: the *Rechnungszins* discount factor at month s, ``(1 + rechnungszins)^(-s/12)``.

    Used **only** inside the equivalence that fixes :func:`prem_gross_level_pp`, and never
    to discount a published cash flow: this library projects gross liability cash flows
    **undiscounted**, and the valuation layers that discount them are cited rather than
    reproduced.  The rate is the *Hoechstrechnungszins* for contracts written from
    1 January 2025, and both the figure and its effective date are ``[unverified]``.
    """
    return (1.0 + rechnungszins) ** (-s / 12.0)                      # noqa: F821


# --- benefit and premium amounts ---

def dyn_factor(t):
    """(1 + g_B)^(y(t) - 1): the *Beitragsdynamik* factor in the policy year containing t.

    1.0 throughout on the ``level`` form.  It escalates the insured *BU-Rente* and the
    annual *Bruttobeitrag* **together**, on the **policy** anniversary — a different
    quantity and a different clock from :func:`leistungsdyn_factor`.
    """
    return (1.0 + beitragsdyn_rate()) ** (policy_year(t) - 1)


def dyn_factor_first(s):
    """The *Beitragsdynamik* factor at month s of the first-order pricing run."""
    return (1.0 + beitragsdyn_rate()) ** (policy_year_first(s) - 1)


def leistungsdyn_factor(z):
    """(1 + g_L)^((z - 1) // 12): the *Leistungsdynamik* factor at claim duration z.

    Steps on each anniversary of the **onset**: cohorts ``z = 1 ... 12`` are paid the
    amount they came in on, ``z = 13 ... 24`` are paid 1.02 times it, and so on.  A model
    that steps this on the policy anniversary has the wrong clock.
    """
    return (1.0 + leistungsdyn_rate()) ** ((z - 1) // 12)


def bu_rente_pp(t):
    """R(t): the **insured** monthly *BU-Rente* at month t, in euros.

    ``bu_rente_mth() x dyn_factor(t)``, so it is constant on the ``level`` form and
    escalates on the policy anniversary on the ``dynamik`` one.  It is the amount a claim
    incepting at ``t`` comes into payment on; once in payment the amount leaves this cells
    behind and moves at :func:`leistungsdyn_factor` instead.  Defined for negative ``t``,
    where it returns the policy-year-1 amount, so that a claim seeded at ``t = 0`` on an
    in-force point can recover the amount it came in on.
    """
    return bu_rente_mth() * dyn_factor(t)


def bu_rente_pp_first(s):
    """The insured monthly *BU-Rente* at month s of the first-order pricing run."""
    return bu_rente_mth() * dyn_factor_first(s)


def rente_pay_pp(t, z):
    """R_p(t, z): the monthly *BU-Rente* **in payment** at month t for the cohort at duration z.

    ``bu_rente_pp(t - z) x leistungsdyn_factor(z)``: the insured amount at the moment of
    onset, which for a cohort at duration ``z`` in month ``t`` is month ``t - z``,
    escalated on each anniversary of that onset.

    The projection itself carries the product of this and the cohort population in the
    value vector of :func:`dis_cohorts`, so this cells is the addressable view rather than
    the hot path.  The two agree by construction, and the identity
    ``pols_dis_dur(t, z) x rente_pay_pp(t, z)`` against that vector is a test.
    """
    return bu_rente_pp(t - z) * leistungsdyn_factor(z)


def beitragssumme_unit():
    """BS_unit: the *Beitragssumme* per 1 EUR p.a. of *Bruttobeitrag*.

    ``sum over y = 1 .. (cover_end_age() - entry_age()) of (1 + g_B)^(y - 1)`` — 37 on the
    anchor cell, where the *Beitragsdynamik* is off.  It is the base of the acquisition
    charge, which § 4 DeckRV caps at 25 per mille (2.5 %) of it, and it is the whole
    original term rather than the remaining one: the charge was incurred at inception.
    """
    g = 1.0 + beitragsdyn_rate()
    return sum(g ** (y - 1) for y in range(1, cover_end_age() - entry_age() + 1))


def prem_gross_level_pp():
    """P: the **level annual** *Bruttobeitrag* per policy, in euros.

    ``risk_factor()`` times either the model point's ``gross_prem_ann`` override or, where
    that is zero, the premium the equivalence produces::

        P = (pv_rente_first() + pv_wiedereingl_first() + pv_claim_cost_first()
             + pv_admin_first())
            / (pv_prem_unit_first() x (1 - admin_prem_rate)
               - acq_rate x beitragssumme_unit())

    struck on the first-order shadow ledgers, **without lapse** and **before** the
    *Risikozuschlag*.  It is linear in P because both loadings are proportional to it, and
    it is acyclic because no decrement in this model depends on the premium.

    This is the *Bruttobeitrag*: the contractually guaranteed **maximum**.  What is
    actually charged is :func:`prem_zahl_pp`, ``beitragsverrechnung()`` times it.
    """
    if gross_prem_ann() > 0.0:
        return risk_factor() * gross_prem_ann()
    numer = (pv_rente_first() + pv_wiedereingl_first()
             + pv_claim_cost_first() + pv_admin_first())
    denom = (pv_prem_unit_first() * (1.0 - admin_prem_rate)          # noqa: F821
             - acq_rate * beitragssumme_unit())                      # noqa: F821
    return risk_factor() * numer / denom


def prem_gross_ann_pp(t):
    """The annual *Bruttobeitrag* in force in the policy year containing month t.

    ``prem_gross_level_pp() x dyn_factor(t)`` — level on the ``level`` form, growing by
    ``1 + beitragsdyn_rate()`` each policy year on the ``dynamik`` one.  It is an annual
    rate, not an instalment; :func:`prem_gross_pp` turns it into what is billed.
    """
    return prem_gross_level_pp() * dyn_factor(t)


def prem_due(t):
    """1 in a month a premium instalment falls due, 0 otherwise.

    ``duration_mth(t) % prem_mode_months() == 0``.  On the anchor cell that is every
    month; on model point 4, months 0, 12, 24, ...; and on model point 6, whose valuation
    date is 180 policy months in and whose mode is half-yearly, months 0, 6, 12, ...
    """
    return 1.0 if duration_mth(t) % prem_mode_months() == 0 else 0.0


def prem_gross_pp(t):
    """P_b(t): the *Bruttobeitrag* **instalment** due at the start of month t, per policy.

    ``prem_due(t) x prem_gross_ann_pp(t) x freq_load() x prem_mode_months() / 12``, so it
    is zero in a month that is not a payment month and carries the whole period's premium
    in one that is.  The *Ratenzahlungszuschlag* scales it, which is why the annual
    *Bruttobeitrag* of a monthly payer buys a 5 % larger bill than the tariff amount.
    """
    return (prem_due(t) * prem_gross_ann_pp(t) * freq_load()
            * prem_mode_months() / 12.0)


def prem_zahl_pp(t):
    """P_z(t): the *Zahlbeitrag* instalment actually billed at month t, per policy.

    ``beitragsverrechnung() x prem_gross_pp(t)`` — the *Bruttobeitrag* less the
    *Beitragsverrechnung*.  This is the number a *Produktinformationsblatt* prints beside
    the *Bruttobeitrag*, and the one the policyholder pays; the gap between them is the
    anticipated *Ueberschuss* credited in advance, and it can be withdrawn as far as the
    *Bruttobeitrag* and no further.
    """
    return beitragsverrechnung() * prem_gross_pp(t)


def surplus_credit_pp(t):
    """(1 - theta) P_b(t): the *Beitragsverrechnung* credited at month t, per policy.

    Published as its own quantity rather than netted inside the premium, so that the
    *Ueberschussbeteiligung* is a visible line of the cash flow statement.  A model
    carrying only the *Zahlbeitrag* silently assumes this credit is permanent.
    """
    return (1.0 - beitragsverrechnung()) * prem_gross_pp(t)


# --- the first-order shadow ledgers ---

def pols_actv_first(s):
    """The *aktiv* population at the start of month s of the first-order pricing run.

    Unit size at ``s = 0`` whatever the model point's own ``status``, because the
    *Bruttobeitrag* was struck at inception on a new-business active life.  Thereafter
    ``- deaths - inceptions + reactivations``, with **no lapse**: a prudent German pricing
    basis does not anticipate a decrement that releases the liability.
    """
    if s < 0 or s > first_len():
        return 0.0
    if s == 0:
        return 1.0
    prev = pols_actv_first(s - 1)
    d = prev * mort_rate_first_mth(s - 1)
    return (prev - d - pols_inception_first(s - 1)
            + pols_reactivation_first(s - 1))


def pols_inception_first(s):
    """Transitions *aktiv* to *leistungspflichtig* at the end of month s, first-order basis.

    Taken from the survivors of the month's mortality; there is no lapse to survive.
    """
    surv = pols_actv_first(s) * (1.0 - mort_rate_first_mth(s))
    return surv * inc_rate_first_mth(s)


def dis_cohorts_first(s):
    """The first-order disabled ledger at the start of month s: ``(populations, values)``.

    Element ``z - 1`` of each list is the state at claim duration ``z``.  The second list
    is a **population times the monthly *BU-Rente* it is paid**, rolled with the same
    survival factors and stepped by ``1 + leistungsdyn_rate()`` at each anniversary of
    onset, so the month's benefit is one sum over a list.  The shadow chain starts empty:
    at ``s <= 0`` both lists are zeros, because the pricing run is always a new-business
    active life.  See :func:`dis_cohorts` for the same construction on the best-estimate
    basis, which this mirrors exactly but for the loaded rates and the absent lapse.
    """
    n = cohort_len_first(s)
    pols = [0.0] * n
    val = [0.0] * n
    if s <= 0:
        return pols, val
    ppols, pval = dis_cohorts_first(s - 1)
    qy = mort_rate_dis_first_mth_year(s - 1)
    ry = recov_rate_first_mth_year()
    g = 1.0 + leistungsdyn_rate()
    for i in range(min(len(ppols), n - 1)):
        cy = i // 12
        if cy > 10:
            cy = 10
        keep = (1.0 - qy[cy]) * (1.0 - ry[cy])
        step = g if (i + 1) % 12 == 0 else 1.0
        pols[i + 1] = ppols[i] * keep
        val[i + 1] = pval[i] * keep * step
    pols[0] = pols_inception_first(s - 1)
    val[0] = pols[0] * bu_rente_pp_first(s - 1)
    return pols, val


def dis_exits_first(s):
    """The first-order disabled ledger's month-end exits: ``(deaths, recoveries, value)``.

    One pass over the cohort vectors at month ``s``, taking deaths first and terminations
    on the survivors.  The third element is the recoveries **times the *BU-Rente* they
    were on**, which is what enters run-off slot 1 as a value.
    """
    pols, val = dis_cohorts_first(s)
    qy = mort_rate_dis_first_mth_year(s)
    ry = recov_rate_first_mth_year()
    deaths = 0.0
    rec = 0.0
    recval = 0.0
    for i in range(len(pols)):
        cy = i // 12
        if cy > 10:
            cy = 10
        q = qy[cy]
        r = ry[cy]
        deaths += pols[i] * q
        rec += pols[i] * (1.0 - q) * r
        recval += val[i] * (1.0 - q) * r
    return deaths, rec, recval


def runoff_cohorts_first(s):
    """The first-order § 174 run-off at the start of month s: ``(populations, values)``.

    Three slots, both lists rolled at **active-lives** mortality because these lives have
    recovered.  Slot 1 is last month's claim terminations and the value they carried.
    """
    n = runoff_months                                                # noqa: F821
    pols = [0.0] * n
    val = [0.0] * n
    if s <= 0:
        return pols, val
    ppols, pval = runoff_cohorts_first(s - 1)
    surv = 1.0 - mort_rate_first_mth(s - 1)
    exits = dis_exits_first(s - 1)
    pols[0] = exits[1]
    val[0] = exits[2]
    for k in range(1, n):
        pols[k] = ppols[k - 1] * surv
        val[k] = pval[k - 1] * surv
    return pols, val


def pols_dis_dur_first(s, z):
    """The first-order disabled population at claim duration z, start of month s."""
    v = dis_cohorts_first(s)[0]
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_dis_first(s):
    """The whole first-order disabled ledger at the start of month s."""
    return sum(dis_cohorts_first(s)[0])


def pols_runoff_first(s):
    """The whole first-order § 174 run-off ledger at the start of month s."""
    return sum(runoff_cohorts_first(s)[0])


def runoff_val_first(s, k):
    """The first-order run-off slot k times the monthly *BU-Rente* it is being paid."""
    v = runoff_cohorts_first(s)[1]
    return v[k - 1] if 1 <= k <= len(v) else 0.0


def pols_reactivation_first(s):
    """First-order run-off completions returning to *aktiv* at the end of month s.

    The last run-off slot's survivors of the month's active-lives mortality.  Three months
    behind :func:`dis_exits_first`'s recoveries, which is § 174 in arithmetic.
    """
    slots = runoff_cohorts_first(s)[0]
    return slots[-1] * (1.0 - mort_rate_first_mth(s))


def pols_prem_first(s):
    """The first-order **premium-paying** count at the start of month s.

    ``pols_actv_first(s)`` plus the disabled cohorts still inside the *Karenzzeit*, on the
    same reading as :func:`pols_prem`: the *Beitragsbefreiung* runs with the benefit, so a
    life inside the *Karenzzeit* still pays.
    """
    dis = dis_cohorts_first(s)[0]
    return pols_actv_first(s) + sum(dis[:karenz_months()])


def pols_if_first(s):
    """The whole first-order in-force population at the start of month s.

    The three shadow ledgers summed.  It is the base of the flat administration charge in
    the equivalence and is read nowhere else.
    """
    return pols_actv_first(s) + pols_dis_first(s) + pols_runoff_first(s)


# --- the equivalence ---

def pv_prem_unit_first():
    """PV_prem: the present value of 1 EUR p.a. of *Bruttobeitrag*, first-order basis.

    ``sum over s of disc_first(s) x dyn_factor_first(s) x pols_prem_first(s) / 12``:
    a twelfth of the annual premium in **every** month of the pricing run, weighted by the
    premium-paying population.  The *Ratenzahlungszuschlag* is deliberately **not** in it,
    which is what makes ``freq_load`` a genuine loading on the tariff premium rather than
    a re-expression of it.
    """
    return sum(disc_first(s) * dyn_factor_first(s) * pols_prem_first(s) / 12.0
               for s in range(0, first_len()))


def pv_rente_first():
    """PV_rente: the present value of the *BU-Rente*, first-order basis.

    The disabled cohorts past the *Karenzzeit* plus **all three run-off slots**, each
    already carried as a population times its own *BU-Rente*, discounted at
    :func:`disc_first` and zero from the *Leistungsendalter*.  Dropping the run-off from
    this sum understates the premium by the whole of the § 174 tail.
    """
    total = 0.0
    for s in range(0, first_len()):
        if age_first(s) >= benefit_end_age():
            continue
        val = dis_cohorts_first(s)[1]
        total += disc_first(s) * (sum(val[karenz_months():])
                                  + sum(runoff_cohorts_first(s)[1]))
    return total


def pv_wiedereingl_first():
    """PV_wgh: the present value of the *Wiedereingliederungshilfe*, first-order basis.

    ``wiedereingliederung_months()`` monthly *Renten* paid on each **completed** run-off,
    so a life that dies inside the run-off is paid nothing.  Zero on a model point with
    the benefit switched off.
    """
    if wiedereingliederung_months() == 0:
        return 0.0
    return sum(disc_first(s) * wiedereingliederung_months()
               * runoff_val_first(s, runoff_months)                  # noqa: F821
               * (1.0 - mort_rate_first_mth(s))
               for s in range(0, first_len()))


def pv_claim_cost_first():
    """PV_cost: the present value of the *Leistungsbearbeitungskosten*, first-order basis.

    ``claim_assess_cost`` on each inception plus ``claim_maint_cost_mth`` on each month a
    claim is in payment — the disabled cohorts past the *Karenzzeit* and all three run-off
    slots, and nothing at all from the *Leistungsendalter*.  These are flat euro amounts,
    which is why a heavier occupational class carries a premium slightly **below** the
    ratio of its inception rates.
    """
    total = 0.0
    for s in range(0, first_len()):
        total += disc_first(s) * claim_assess_cost * pols_inception_first(s)  # noqa: F821
        if age_first(s) < benefit_end_age():
            pols = dis_cohorts_first(s)[0]
            paying = sum(pols[karenz_months():]) + pols_runoff_first(s)
            total += disc_first(s) * claim_maint_cost_mth * paying   # noqa: F821
    return total


def pv_admin_first():
    """PV_admin: the present value of the flat *Verwaltungskosten*, first-order basis.

    ``admin_flat_ann / 12`` on every in-force life in every month, uninflated: a German
    *Verwaltungskostenzuschlag* is fixed in the tariff at conclusion.  The *proportional*
    administration loading is not here — it is proportional to the premium, so it stays on
    the left-hand side of the equivalence and reduces the denominator instead.
    """
    return sum(disc_first(s) * admin_flat_ann / 12.0 * pols_if_first(s)  # noqa: F821
               for s in range(0, first_len()))


# --- the best-estimate ledgers ---

def pols_actv(t):
    """l_a(t): the *aktiv* population at the **start** of month t.

    Premium-paying and exposed to inception, active-lives mortality and lapse.  Seeded
    with :func:`pols_if_init` on an ``aktiv`` model point and with zero on a ``leistung``
    one.  Thereafter ``- deaths - lapses - inceptions + reactivations``, the last of them
    being the § 174 return arc three months behind the recovery that produced it.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init() if status() == "aktiv" else 0.0
    return (pols_actv(t - 1) - pols_death_actv(t - 1) - pols_lapse(t - 1)
            - pols_inception(t - 1) + pols_reactivation(t - 1))


def pols_death_actv(t):
    """Deaths out of the *aktiv* ledger at the end of month t.

    Taken **first**, before lapses and inceptions, which is the model's stated processing
    order **[std]**.  A decrement and never a cash flow: an SBU pays nothing on death.
    """
    return pols_actv(t) * mort_rate_mth(t)


def pols_lapse(t):
    """Lapses at the end of month t, from the *aktiv* ledger only.

    Taken from the survivors of the month's mortality.  A lapse **pays nothing** here:
    § 169 VVG through § 176 gives this contract a real *Rueckkaufswert* and § 165 a real
    *beitragsfreie BU-Rente*, but both are the release of a reserve this model does not
    compute, so a lapse is a pure decrement and ``claims(t, "LAPSE")`` is zero.
    """
    return (pols_actv(t) - pols_death_actv(t)) * lapse_rate_mth(t)


def pols_inception(t):
    """Transitions *aktiv* to *leistungspflichtig* at the end of month t.

    Taken from the survivors of **both** the month's mortality and its lapses, and
    weighted by the composed :func:`inc_rate_mth`, which already carries the occupational
    factor, the *Anerkennungsquote* and the *AU-Klausel* uplift.  These lives enter claim
    duration ``z = 1`` at the start of month ``t + 1``, which is when their first
    *BU-Rente* falls due if there is no *Karenzzeit*.  Each one costs
    ``claim_assess_cost``.
    """
    base = pols_actv(t) - pols_death_actv(t) - pols_lapse(t)
    return base * inc_rate_mth(t)


def dis_cohorts(t):
    """The disabled ledger at the start of month t: ``(populations, values)``.

    Element ``z - 1`` of each list is the state at claim duration ``z``, for
    ``z = 1 ... cohort_len(t)``.  The second list is a **population times the monthly
    *BU-Rente* it is being paid** rather than a population, so that the month's benefit is
    one sum over a slice rather than a lookup per cohort; it rolls with the same survival
    factors and is stepped by ``1 + leistungsdyn_rate()`` exactly when a cohort crosses an
    anniversary of its own onset, which is when ``z`` is a multiple of 12.

    At ``t <= 0`` the vectors are the seeded state: all zeros on an ``aktiv`` model point,
    and :func:`pols_if_init` at cohort :func:`seed_claim_dur` on a ``leistung`` one, whose
    value is the *BU-Rente* that claim came into payment on.  Thereafter cohort 1 is the
    previous month's inceptions and every other cohort is the previous cohort survived one
    month of disabled-lives mortality and one month of reactivation.

    This is the model's list-valued cells and the reason is cost: a two-argument recursion
    would be ``proj_len() x max_claim_dur()`` separate cells — nearly two hundred
    thousand on the anchor cell — where this is ``proj_len()`` cells with a loop
    inside.  :func:`pols_dis_dur` reads elements out of it, so the notes' two-dimensional
    object is still addressable by name.  A new list is built on each step rather than the
    previous one mutated, so holding a returned list cannot corrupt the cache.
    """
    n = cohort_len(t)
    pols = [0.0] * n
    val = [0.0] * n
    if t <= 0:
        z0 = seed_claim_dur()
        if z0 and z0 <= n:
            pols[z0 - 1] = pols_if_init()
            val[z0 - 1] = pols_if_init() * rente_pay_pp(t, z0)
        return pols, val
    ppols, pval = dis_cohorts(t - 1)
    qy = mort_rate_dis_mth_year(t - 1)
    ry = recov_rate_mth_year()
    g = 1.0 + leistungsdyn_rate()
    for i in range(min(len(ppols), n - 1)):
        cy = i // 12
        if cy > 10:
            cy = 10
        keep = (1.0 - qy[cy]) * (1.0 - ry[cy])
        step = g if (i + 1) % 12 == 0 else 1.0
        pols[i + 1] = ppols[i] * keep
        val[i + 1] = pval[i] * keep * step
    pols[0] = pols_inception(t - 1)
    val[0] = pols[0] * bu_rente_pp(t - 1)
    return pols, val


def dis_exits(t):
    """The disabled ledger's month-end exits at t: ``(deaths, recoveries, recovery value)``.

    One pass over the cohort vectors, taking deaths at :func:`mort_rate_dis_mth_year` first
    and terminations at :func:`recov_rate_mth_year` on the survivors, which is the model's
    stated processing order.  The third element is the terminations **times the *BU-Rente*
    they were on**: that amount is frozen at the *Nachpruefung* date and is what the run-off
    goes on paying.

    Published as one cells because the three totals come from the same pass and because
    :func:`dis_cohorts` would otherwise have to be walked three times a month.
    """
    pols, val = dis_cohorts(t)
    qy = mort_rate_dis_mth_year(t)
    ry = recov_rate_mth_year()
    deaths = 0.0
    rec = 0.0
    recval = 0.0
    for i in range(len(pols)):
        cy = i // 12
        if cy > 10:
            cy = 10
        q = qy[cy]
        r = ry[cy]
        deaths += pols[i] * q
        rec += pols[i] * (1.0 - q) * r
        recval += val[i] * (1.0 - q) * r
    return deaths, rec, recval


def runoff_cohorts(t):
    """The § 174 run-off at the start of month t: ``(populations, values)``.

    ``runoff_months`` slots — three, the statutory run-off being to the end of the third
    month after the *Einstellungsmitteilung* reaches the policyholder.  Slot 1 is last
    month's claim terminations; slots 2 and 3 are the previous slots survived one month of
    **active-lives** mortality, because these lives have recovered and are no longer
    impaired lives.  The value list is the same population times the *BU-Rente* it is
    still being paid, frozen at the *Nachpruefung* date and receiving no further
    *Leistungsdynamik* **[std]**.

    Empty at ``t <= 0`` on every model point, including the in-force claim: a claim in
    payment is *leistungspflichtig*, not in run-off.
    """
    n = runoff_months                                                # noqa: F821
    pols = [0.0] * n
    val = [0.0] * n
    if t <= 0:
        return pols, val
    ppols, pval = runoff_cohorts(t - 1)
    surv = 1.0 - mort_rate_mth(t - 1)
    exits = dis_exits(t - 1)
    pols[0] = exits[1]
    val[0] = exits[2]
    for k in range(1, n):
        pols[k] = ppols[k - 1] * surv
        val[k] = pval[k - 1] * surv
    return pols, val


def pols_dis_dur(t, z):
    """l_d(t, z): the *leistungspflichtig* population at claim duration z, start of month t.

    Zero outside ``1 <= z <= cohort_len(t)``, so the two-dimensional view is total.
    """
    v = dis_cohorts(t)[0]
    return v[z - 1] if 1 <= z <= len(v) else 0.0


def pols_dis(t):
    """The whole *leistungspflichtig* ledger at the start of month t.

    ``sum over z of pols_dis_dur(t, z)``.  It includes cohorts still inside the
    *Karenzzeit*, which are *berufsunfaehig*, are not yet paid and are still paying
    premium.
    """
    return sum(dis_cohorts(t)[0])


def pols_death_dis(t):
    """Deaths out of the disabled ledger at the end of month t.

    At disabled-lives mortality, which is select on claim duration: twelve times the
    active rate in the first claim year, 4.8 times it ultimately.
    """
    return dis_exits(t)[0]


def pols_recovery(t):
    """Claim terminations other than death at the end of month t, entering the run-off.

    Recovery **and** *konkrete Verweisung* together — one rate, because they end the
    benefit the same way, through the same *Nachpruefung*, with the same run-off, and no
    public data separates them.  **These lives do not rejoin :func:`pols_actv` here**:
    they enter run-off slot 1 and return three months later as
    :func:`pols_reactivation`.
    """
    return dis_exits(t)[1]


def runoff_value_in(t):
    """The recoveries at the end of month t times the *BU-Rente* they were on.

    What enters run-off slot 1 as a value.  Carried as an amount rather than recomputed
    from a count because the cohorts terminating in one month are on different *BU-Renten*
    — they incepted in different months and have crossed different numbers of onset
    anniversaries.
    """
    return dis_exits(t)[2]


def pols_runoff_slot(t, k):
    """l_r(t, k): the § 174 run-off population k months into the run-off, start of month t."""
    v = runoff_cohorts(t)[0]
    return v[k - 1] if 1 <= k <= len(v) else 0.0


def runoff_val(t, k):
    """V_r(t, k): run-off slot k times the monthly *BU-Rente* it is being paid.

    A **value** ledger rather than a count, because a cohort entering the run-off keeps
    the *BU-Rente* it was on at the *Nachpruefung* date.  It is what makes the run-off's
    benefit and the *Wiedereingliederungshilfe* computable without a second duration
    dimension.
    """
    v = runoff_cohorts(t)[1]
    return v[k - 1] if 1 <= k <= len(v) else 0.0


def pols_runoff(t):
    """The whole § 174 run-off ledger at the start of month t.

    The ledger a naive model omits, and omitting it is a first-order error: a recovery
    does not release the liability in the month it happens, it releases it three months
    later, and every one of those months carries a full *BU-Rente*.
    """
    return sum(runoff_cohorts(t)[0])


def pols_death_runoff(t):
    """Deaths out of the § 174 run-off at the end of month t, at active-lives mortality.

    These lives have recovered, so they are no longer impaired lives.  A death here also
    extinguishes the *Wiedereingliederungshilfe* the life would have been paid on
    completing the run-off.
    """
    return pols_runoff(t) * mort_rate_mth(t)


def pols_reactivation(t):
    """Run-off completions returning to *aktiv* at the end of month t.

    The last run-off slot's survivors of the month's active-lives mortality.  The
    *Beitragsbefreiung* stops with them, the premium resumes at the same *Zahlbeitrag*,
    and a fresh BU may be claimed later — so these lives re-enter :func:`pols_actv` fully
    exposed to inception again.  They are also the population the
    *Wiedereingliederungshilfe* is paid on.
    """
    return pols_runoff_slot(t, runoff_months) * (1.0 - mort_rate_mth(t))  # noqa: F821


def pols_death(t):
    """Deaths out of all three ledgers at the end of month t.

    **A decrement and never a cash flow.**  An SBU pays nothing on death, before or during
    a claim, so there is no ``claims_death`` column for a reader arriving from a term-life
    model to find.  With :func:`pols_lapse` it is one of the only two exits from the
    model.
    """
    return pols_death_actv(t) + pols_death_dis(t) + pols_death_runoff(t)


def pols_if(t):
    """L(t): the policy count at the **start** of month t, and the weight on that row.

    Built by its own roll-forward — ``pols_if(t-1) - pols_death(t-1) - pols_lapse(t-1)``,
    from :func:`pols_if_init` at ``t = 0`` — rather than as the sum of the three ledgers,
    and that is deliberate.  Death and lapse are the **only** exits from this model:
    inception, recovery and reactivation are internal transfers between the ledgers.
    Building ``pols_if`` from the exits and then comparing it against the ledgers in
    :func:`check_states` makes that structural claim a real test at every ``t``, where
    defining it as the sum would make the check a restatement of its own definition.

    It is the count at the **start** of the month, before any decrement, so it is the
    weight on that same :func:`result_cf` row's cash flows and ``result_cf()``'s first
    value is ``pols_if_init()`` exactly.  End-of-month state goes through
    :func:`pols_if_at`.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init()
    return pols_if(t - 1) - pols_death(t - 1) - pols_lapse(t - 1)


def pols_if_at(t, timing):
    """The policy count at a point inside month t.

    ``"BEG"``
        ``pols_if(t)``, the start of the month before any decrement — the same
        number as :func:`pols_if` and the weight on that month's cash flows.

    ``"END"``
        ``pols_if(t + 1)``, the end-of-month state after deaths and lapses.
        At ``t = proj_len() - 1`` it is the population whose cover simply runs
        out, and nothing is payable to it.
    """
    if timing == "BEG":
        return pols_if(t)
    if timing == "END":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_prem(t):
    """L_p(t): the **premium-paying** count at the start of month t.

    ``pols_actv(t)`` plus the disabled cohorts still inside the *Karenzzeit*,
    ``sum over z <= karenz_months() of pols_dis_dur(t, z)``.  A life inside the
    *Karenzzeit* is *berufsunfaehig* but is not yet being paid, so the
    *Beitragsbefreiung* has not started **[std]**.

    **This, and not :func:`pols_if`, is the weight on the premium.**  Weighting the
    premium by the in-force count charges premium to lives in claim and so silently
    deletes the *Beitragsbefreiung*, which is core cover rather than an option — the
    classic German BU implementation error.  On the anchor cell, where the *Karenzzeit* is
    zero, this equals :func:`pols_actv` at every ``t``.
    """
    dis = dis_cohorts(t)[0]
    return pols_actv(t) + sum(dis[:karenz_months()])


# --- the cash flows ---

def premiums(t):
    """The **gross** *Bruttobeitrag* income at the start of month t, an inflow.

    ``prem_gross_pp(t) x pols_prem(t)``, zero in a month that is not a payment month.
    This is the gross stream; the *Beitragsverrechnung* returned out of it is
    :func:`surplus_credit`, and the cash actually collected is the difference.  Publishing
    both is what keeps the *Ueberschussbeteiligung* a visible line rather than a netting
    hidden inside the premium.
    """
    return prem_gross_pp(t) * pols_prem(t)


def surplus_credit(t):
    """The *Beitragsverrechnung* credited back at the start of month t, an outflow.

    ``surplus_credit_pp(t) x pols_prem(t)`` — 30 % of every *Bruttobeitrag* at the
    shipped ratio.  It is the *Ueberschussbeteiligung* of § 153 VVG through § 176, applied
    immediately as a reduction of the premium charged rather than accumulated, which is
    the standard *Ueberschussverwendung* in German BU and is why this model carries no
    surplus account, no RfB and no declaration mechanic.
    """
    return surplus_credit_pp(t) * pols_prem(t)


def claims(t, kind=None):
    """Benefit outgo at the start of month t, by kind; the total when kind is omitted.

    ``"BU_RENTE"``
        the monthly annuity, paid in advance to the disabled cohorts past the
        *Karenzzeit* **and to all three § 174 run-off slots**, each already
        carried as a population times its own *BU-Rente*.  Zero from the
        *Leistungsendalter*, where the mass is held rather than deleted.

    ``"REINTEGRATION"``
        the *Wiedereingliederungshilfe*, ``wiedereingliederung_months()``
        monthly *Renten* on each **completed** run-off, so a life that dies
        inside the run-off never returns to work and is paid nothing.  It is
        not gated at the *Leistungsendalter*: a life may return to work after
        it while the cover still runs.

    ``"LAPSE"``
        zero, always.  § 169 VVG through § 176 gives this contract a real
        *Rueckkaufswert* and § 165 a real *beitragsfreie BU-Rente*, and this
        model prices neither, because both are the release of a reserve it
        deliberately does not compute.  The kind exists so that the zero is a
        published scope statement rather than a missing column.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("BU_RENTE", "REINTEGRATION", "LAPSE"))
    if kind == "BU_RENTE":
        if age(t) >= benefit_end_age():
            return 0.0
        val = dis_cohorts(t)[1]
        return sum(val[karenz_months():]) + sum(runoff_cohorts(t)[1])
    if kind == "REINTEGRATION":
        if wiedereingliederung_months() == 0:
            return 0.0
        return (wiedereingliederung_months()
                * runoff_val(t, runoff_months)                       # noqa: F821
                * (1.0 - mort_rate_mth(t)))
    if kind == "LAPSE":
        return 0.0
    raise ValueError("invalid kind")


def expenses(t):
    """Total administration expense at the start of month t **[std]**.

    Three components, all shipped as standardizations because no German insurer publishes
    a BU charge structure and a pure risk contract carries no *Effektivkosten*
    disclosure:

    * **acquisition**, ``acq_rate x prem_gross_level_pp() x beitragssumme_unit()``,
      levied **once, at t = 0, and only on a new-business point** — an in-force point has
      already incurred it, and charging it again at the valuation date is a numbered
      pitfall.  At 2.5 % of a 37-year *Beitragssumme* it is the largest single expense
      item in the model and it dominates the first month's :func:`net_cf`;
    * **proportional administration**, ``admin_prem_rate x premiums(t)``, in every month a
      premium is due;
    * **flat administration**, ``admin_flat_ann / 12`` per in-force policy per month,
      **uninflated**, because a German *Verwaltungskostenzuschlag* is fixed in the tariff
      at conclusion.

    Commission is not a separate line: it sits inside ``acq_rate``, which is the German
    taxonomy.  Claim handling is not here either — it is :func:`claim_expenses`, because
    it scales with claims rather than with policies.
    """
    acq = 0.0
    if t == 0 and duration_init_months() == 0:
        acq = acq_rate * prem_gross_level_pp() * beitragssumme_unit()  # noqa: F821
    admin_prop = admin_prem_rate * prem_gross_pp(t) * pols_prem(t)   # noqa: F821
    admin_flat = admin_flat_ann / 12.0 * pols_if(t)                  # noqa: F821
    return acq + admin_prop + admin_flat


def claim_expenses(t):
    """The *Leistungsbearbeitungskosten* at month t **[std]**.

    ``claim_assess_cost`` on each inception at the **end** of the month — the
    *Leistungspruefung* of a German BU claim is expensive and is incurred once, when the
    claim is decided — plus ``claim_maint_cost_mth`` on each month a claim is in payment,
    on the same population the *BU-Rente* is paid to: the disabled cohorts past the
    *Karenzzeit* and all three run-off slots, and nothing from the *Leistungsendalter*.

    Named separately from :func:`expenses` because it is the only expense line that scales
    with claims rather than with policies, and because both are flat euro amounts, which
    is what makes a heavier occupational class carry a premium slightly below the ratio of
    its inception rates.
    """
    assess = claim_assess_cost * pols_inception(t)                   # noqa: F821
    maint = 0.0
    if age(t) < benefit_end_age():
        pols = dis_cohorts(t)[0]
        paying = sum(pols[karenz_months():]) + pols_runoff(t)
        maint = claim_maint_cost_mth * paying                        # noqa: F821
    return assess + maint


def net_cf(t):
    """The net liability cash flow of month t, **income positive**.

    The gross *Bruttobeitrag* less the *Beitragsverrechnung* returned out of it, less the
    *BU-Rente*, the *Wiedereingliederungshilfe* and the (structurally zero) lapse benefit,
    less administration expense and *Leistungsbearbeitungskosten*.  The library-wide sign;
    :func:`liability_cf` publishes the same stream outgo-positive.

    The shape to expect is a large first-month strain — the whole acquisition charge falls
    in month 0 — then thin positive margins that thin further as the inception rate
    accelerates from the mid-forties, and turn negative in the last years before the
    *Endalter*, which is exactly the *Deckungsrueckstellung* this model does not compute
    being run down.
    """
    return (premiums(t) - surplus_credit(t) - claims(t)
            - expenses(t) - claim_expenses(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation a valuation layer consumes: a Solvency II best estimate is
    ``sum v(t) liability_cf(t)`` over whatever risk-free term structure is supplied, plus
    a risk margin.  Published as a column beside :func:`net_cf` so the sign convention is
    verifiable in the frame rather than only in prose.
    """
    return -net_cf(t)


# --- the published identities ---

def check_net_cf_resid(t):
    """The cash-flow-statement residual in month t; zero everywhere.

    delib's first ruling: every model reconstructs :func:`net_cf` from its own published
    parts, so the headline number of a cash flow model is not the one quantity nothing
    checks.  The identity is

        net_cf(t) = prem_zahl_pp(t) x pols_prem(t)
                    - claims(t, "BU_RENTE") - claims(t, "REINTEGRATION")
                    - claims(t, "LAPSE") - expenses(t) - claim_expenses(t)

    and the premium leg is deliberately rebuilt from the *Zahlbeitrag* **actually billed**
    times the premium-paying count rather than from ``premiums(t) - surplus_credit(t)``.
    That makes this a real reconciliation instead of a restatement of :func:`net_cf`'s own
    formula: it crosses the *Brutto* / *Zahl* split, and it fails if the premium is
    weighted by :func:`pols_if` instead of :func:`pols_prem` — which is this product's
    classic implementation error, and one that leaves every total in the frame looking
    plausible.
    """
    return net_cf(t) - (prem_zahl_pp(t) * pols_prem(t)
                        - claims(t, "BU_RENTE")
                        - claims(t, "REINTEGRATION")
                        - claims(t, "LAPSE")
                        - expenses(t) - claim_expenses(t))


def check_net_cf():
    """True when the cash flow statement reconciles in every projected month.

    No argument, one bool over all ``t``, the library-wide shape;
    :func:`check_net_cf_resid` gives the signed residual of the month that failed.
    """
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol            # noqa: F821
               * max(1.0, abs(bu_rente_pp(t)))
               for t in range(0, proj_len()))


def check_states_resid(t):
    """The state-decomposition residual at the start of month t; zero everywhere.

    ``pols_if(t) - pols_actv(t) - pols_dis(t) - pols_runoff(t)``.

    **This is the model's structural check, and it is not trivially zero**, because
    :func:`pols_if` is built by its own roll-forward off the two exits rather than as the
    sum of the three ledgers.  What it catches is a life that leaves one ledger without
    arriving in another, or arrives in two: a recovery that both rejoins ``pols_actv`` and
    stays in the run-off, an inception counted in the disabled ledger and left in the
    active one, a run-off slot that falls off the end of its list.  Every one of those is
    a first-order error in a multi-state model, and none of them shows in the cash flows
    as anything but a number that is slightly wrong.
    """
    return pols_if(t) - pols_actv(t) - pols_dis(t) - pols_runoff(t)


def check_states():
    """True when the three ledgers account for the whole in-force population at every t."""
    return all(abs(check_states_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(0, proj_len() + 1))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if(t+1) - pols_death(t) - pols_lapse(t)``.  Death and lapse are the
    only exits, so inception, recovery and reactivation — which are internal transfers
    between the three ledgers — must **not** appear here.  Putting them in is how a
    multi-state model silently loses mass.

    **Trivially zero by construction** on this model, because :func:`pols_if` is defined
    by exactly this recursion.  It is published because it is the notes' own identity and
    because the substantive content of it — that the exits really are the only two — is
    asserted by :func:`check_states`, which compares that recursion against the ledgers.
    Read the two together: this one fixes the definition, that one tests it.
    """
    return pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month."""
    return all(abs(check_pols_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(0, proj_len()))


def check_dis_roll_fwd_resid(t):
    """The disabled-ledger roll-forward residual in month t; zero everywhere.

    ``pols_dis(t+1) - pols_dis(t) + pols_death_dis(t) + pols_recovery(t)
    - pols_inception(t)``.  The disabled ledger gains the month's inceptions and loses its
    own deaths and its claim terminations, and nothing else — in particular it does **not**
    lose anything at the *Leistungsendalter*, where the benefit stops but the mass is
    held.  It is built by direct comparison of the ledger total against the flows, so a
    cohort dropping off the end of the vector, a duration shift that loses a slot, or a
    *Karenzzeit* mistakenly applied to the population rather than to the payment all fail
    here.
    """
    return (pols_dis(t + 1) - pols_dis(t) + pols_death_dis(t)
            + pols_recovery(t) - pols_inception(t))


def check_dis_roll_fwd():
    """True when the disabled ledger rolls forward exactly in every projected month."""
    return all(abs(check_dis_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(0, proj_len()))


def check_runoff_roll_fwd_resid(t):
    """The § 174 run-off roll-forward residual in month t; zero everywhere.

    ``pols_runoff(t+1) - pols_runoff(t) + pols_death_runoff(t) + pols_reactivation(t)
    - pols_recovery(t)``.  The run-off gains the month's claim terminations and loses its
    own deaths and its completions, so a model that returns a recovery straight to
    ``pols_actv`` — the commonest way to forget § 174 — fails here immediately, and with
    it loses three monthly *BU-Renten* per recovery.
    """
    return (pols_runoff(t + 1) - pols_runoff(t) + pols_death_runoff(t)
            + pols_reactivation(t) - pols_recovery(t))


def check_runoff_roll_fwd():
    """True when the § 174 run-off ledger rolls forward exactly in every projected month."""
    return all(abs(check_runoff_roll_fwd_resid(t))
               <= roll_fwd_tol * max(pols_if_init(), 1.0)            # noqa: F821
               for t in range(0, proj_len()))


def check_prem_split_resid(t):
    """The *Brutto* / *Zahl* split residual in month t; zero everywhere.

    ``premiums(t) - surplus_credit(t) - prem_zahl_pp(t) x pols_prem(t)``.  The two premium
    columns must reconcile to the *Zahlbeitrag* actually billed, so that a reader can
    recover the cash collected from the frame without knowing the ratio.  It also fixes
    the *Ratenzahlungszuschlag*'s place: ``freq_load`` scales the *Bruttobeitrag* and the
    *Beitragsverrechnung* together, so it cancels out of this identity and
    ``beitragsverrechnung`` stays exactly the ratio the tariff quotes.
    """
    return premiums(t) - surplus_credit(t) - prem_zahl_pp(t) * pols_prem(t)


def check_prem_split():
    """True when the two premium columns reconcile to the *Zahlbeitrag* in every month."""
    return all(abs(check_prem_split_resid(t)) <= roll_fwd_tol        # noqa: F821
               * max(1.0, abs(prem_gross_ann_pp(t)))
               for t in range(0, proj_len()))


def check_cover_end_resid(t):
    """The cover-cessation residual in month t; zero everywhere.

    ``claims(t, "BU_RENTE")`` in every month whose attained age has reached
    ``benefit_end_age()``, plus ``premiums(t)`` in every month whose attained age has
    reached ``cover_end_age()``, and zero before both.

    The second term is vacuous by construction of :func:`proj_len`, which stops the frame
    in the last month of attained age ``cover_end_age() - 1``, and it is written anyway so
    that a change to the horizon cannot quietly extend the premium.  The first is the live
    one: on model point 9 the *Leistungsdauer* ends four years before the
    *Versicherungsdauer*, so from attained age 63 the *BU-Rente* is zero while the premium
    runs on to 67 — and the disabled mass is **held**, not deleted, so the state identities
    still close across the boundary.
    """
    resid = 0.0
    if age(t) >= benefit_end_age():
        resid += claims(t, "BU_RENTE")
    if age(t) >= cover_end_age():
        resid += premiums(t)
    return resid


def check_cover_end():
    """True when benefit and premium both stop exactly at their own contractual ages."""
    return all(abs(check_cover_end_resid(t)) <= roll_fwd_tol         # noqa: F821
               for t in range(0, proj_len()))


# --- the result frames ---

def result_cf():
    """Result table of cash flows, indexed by policy month t.

    ``pols_if`` is the start-of-month count, which is the weight applied to every cash
    flow on the same row, and its first value is ``pols_if_init()`` exactly.  The three
    state columns beside it decompose it — *aktiv*, *leistungspflichtig* and the § 174
    run-off — and ``pols_prem`` is the premium-paying count, which is **below**
    ``pols_if`` wherever anyone is in claim past the *Karenzzeit*.

    ``premiums`` is the **gross** *Bruttobeitrag* and ``surplus_credit`` the
    *Beitragsverrechnung* returned out of it, so the cash actually collected is the
    difference of the two.  ``claims_lapse`` is a column of zeros — there is no surrender
    or paid-up cash flow in this model — and is published rather than dropped so that the
    scope statement is made rather than inferred.  ``liability_cf`` is ``net_cf``
    outgo-positive.

    The frame runs ``t = 0 ... proj_len() - 1`` and stops: cover ceases at attained age
    ``cover_end_age()`` with nothing payable, and a claim still in payment at the horizon
    simply stops.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_actv": [pols_actv(t) for t in ts],
            "pols_dis": [pols_dis(t) for t in ts],
            "pols_runoff": [pols_runoff(t) for t in ts],
            "pols_prem": [pols_prem(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "surplus_credit": [surplus_credit(t) for t in ts],
            "claims_bu_rente": [claims(t, "BU_RENTE") for t in ts],
            "claims_reintegration": [claims(t, "REINTEGRATION") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_states():
    """Result table of transitions, rates and per-policy amounts, indexed by policy month t.

    The transition columns are the flows at the **end** of month ``t``, so they are the
    difference between one :func:`result_cf` row's state columns and the next.

    ``recov_rate`` is the only column that is not a function of ``t`` alone: reactivation
    depends on claim duration, not on the projection month.  What is published here is
    ``recov_rate(t + 1)`` — the rate faced at month ``t`` by the cohort that entered claim
    duration 1 in month 0, which is exactly the duration profile laid out along ``t``.
    Read it as the shape of the assumption, not as the rate applied in that month; the
    rate applied to a cohort is ``recov_rate(z)`` and belongs to the cohort.
    """
    ts = list(range(0, proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_inception": [pols_inception(t) for t in ts],
            "pols_recovery": [pols_recovery(t) for t in ts],
            "pols_reactivation": [pols_reactivation(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "inc_rate": [inc_rate(t) for t in ts],
            "recov_rate": [recov_rate(t + 1) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
            "bu_rente_pp": [bu_rente_pp(t) for t in ts],
            "prem_gross_pp": [prem_gross_pp(t) for t in ts],
            "prem_zahl_pp": [prem_zahl_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

accept_factor = 0.8

inc_load_first = 1.3

recov_load_first = 0.7

mort_dis_load_first = 0.8

mort_actv_load_first = 0.8

rechnungszins = 0.01

acq_rate = 0.025

admin_prem_rate = 0.09

admin_flat_ann = 18.0

claim_assess_cost = 800.0

claim_maint_cost_mth = 12.0

runoff_months = 3

roll_fwd_tol = 1e-10

pd = ("Module", "pandas")
