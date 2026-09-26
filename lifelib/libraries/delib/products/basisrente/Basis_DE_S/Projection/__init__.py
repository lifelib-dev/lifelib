# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.Basis_DE_S` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

.. rubric:: Two clocks, and the argument of a cells says which

The grid is **monthly** and the contract is almost entirely annual, so the model runs on
two clocks and a cells' argument names the one it is on.

``t`` counts **projection months from the valuation date**, 0-based: ``t = 0`` is the
first projected month and ``t = proj_len() - 1`` the last, with
``proj_len() = 12 x proj_len_y()`` and ``proj_len_y() = omega_age() - age(0) + 1``. It is
the argument of the in force, the decrements, the claims, the expenses, the commission and
the *Rente* instalments — everything that happens **on a date**.

``k = proj_year(t) = t // 12`` counts **projection years** and is the argument of
everything the contract states per *Versicherungsjahr*: the *Beitrag*, the *Zuzahlung*, the
four account charges, the declared rate, the *Deckungskapital*, the *Rentenfaktor*
conversion and the *Überschussrente*. ``k`` is the annual-step model's own ``t``, and
``result_cf_annual().loc[k]`` is that model's row ``k``.

Policy duration at the start of projection year ``k`` is
``duration_y(k) = duration_init + k`` **completed** policy years, so a new-business point
opens at ``duration_y(0) = 0``; an in-force point opens at whatever duration it has already
run and **the frame still starts at ``t = 0``**. ``duration(t)`` is the same quantity read
from a month, ``duration_mth(t) // 12`` with ``duration_mth(t) = 12 duration_init + t``,
and ``policy_year(t) = duration(t) + 1`` is the contractual 1-based label the AVB and the
behaviour table use. The frame opens on a policy anniversary, so a projection year is a
*Versicherungsjahr* and ``is_anniv(t)`` — ``t % 12 == 11`` — is its last month.

The decrements carry the library's two speeds: ``mort_rate(t)`` is the **annual** rate of
the year the month falls in and ``mort_rate_mth(t) = 1 - (1 - mort_rate(t))^(1/12)`` is
what the recursion applies, so twelve months compound back to the annual rate exactly and
``pols_if(12k)`` is the annual-step model's ``pols_if(k)`` to the last bit. The whole
*Aufschubphase* is therefore unchanged: the premium, the *Zuzahlung*, the commission, the
four charges, both account blocks, the fund at *Rentenbeginn* and the annuity struck on it
are bit-identical on all thirteen model points.

**What the finer grid buys on this product is the *Rente* itself.** A *Rentenfaktor* is
quoted in euro a **month** and a *Leibrente* is paid monthly; the annual-step model booked
twelve instalments together at the start of each payout year on the opening in-force
count, named that as a pitfall and as a stated approximation, and was generous to the year
of death by up to a full year's annuity — 4 290,52 € of the anchor cell's payout phase,
1,6 % of it. Here the instalment is paid to whoever is alive at the start of each month.
The *Rentengarantiezeit* becomes ``12m`` guaranteed **instalments** beginning in the month
after the death that triggered them rather than in the following year, which moves
116,29 € onto model point 4 and 562,91 € onto model point 12; and a policy that dies in
the third month of a year now bears three twelfths of that year's maintenance expense
rather than the whole of it.

The annuity is lifelong, so the projection runs to the end of the mortality table; in the
terminal year ``mort_rate`` is 1, the certainty falls in that year's **last month**, the
last survivor dies at ``t = proj_len() - 1`` and ``pols_if(proj_len())`` is zero.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/basisrente/``, read at run time rather than stored inside the model. The model
folder therefore holds nothing but formulas — no ``_data/``, no IOSpec, no embedded
values. This follows ``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which
keeps its inputs *inside* the model.

Each table has a filename Reference and a reader Cells, both on
:mod:`~.Basis_DE_S.Data`, reached here through the ``data`` Reference:

=========================  ===================================  ==========================
Reference                  Cells                                File
=========================  ===================================  ==========================
model_point_file           data.model_point_table()             model_point_table.csv
mort_table_file            data.mort_table()                    mort_table.csv
surplus_file               data.surplus_table()                 surplus_table.csv
rentenfaktor_file          data.rentenfaktor_table()            rentenfaktor_table.csv
charge_file                data.charge_table()                  charge_table.csv
behaviour_file             data.behaviour_table()               behaviour_table.csv
option_file                data.option_table()                  option_table.csv
=========================  ===================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string, ``av_pp_at(t, timing)`` and ``pols_if_at(t, timing)``
for the within-year reads. The technical notes use compact actuarial symbols instead.
The mapping is:

=========================  ==============================  ==============================
Notes symbol               Cells                           Meaning
=========================  ==============================  ==============================
(none)                     model_point()                   The selected model point row
n = omega - x(0) + 1       proj_len_y()                    Number of projected years
12 n                       proj_len()                      Number of projected months
k = t // 12                proj_year(t)                    Projection year of month t
(none)                     is_anniv(t)                     Last month of a projection year
x(k)                       age_y(k)                        Attained age in year k
x(t)                       age(t)                          The same, read from a month
d(k)                       duration_y(k)                   Completed policy years in year k
d(t)                       duration(t)                     The same, read from a month
(none)                     duration_mth(t)                 Completed policy months
(none)                     policy_year(t)                  Contractual 1-based label
y(k)                       cal_year_y(k)                   Calendar year in year k
y(t)                       cal_year(t)                     The same, read from a month
omega                      omega_age()                     Terminal age of the table
T                          ret_y()                         Projection year of Rentenbeginn
12 T                       ret_t()                         Month of the first instalment
(none)                     gtd_end_t()                     Last month of the Rentengarantiezeit
S                          beitragssumme_pp()              Beitragssumme at inception
P0 (1 + delta)^d(k)        prem_base_pp(k)                 Contractual Beitrag before phi
phi                        prem_freq_load()                Ratenzahlungszuschlag
P(k)                       prem_pp(k)                      Beitrag charged per paying policy
(none)                     prem_due(t)                     True in the month it falls due
Z(k)                       zuz_pp(k)                       Zuzahlung per paying policy
(take-up)                  zuz_take_up(k)                  Zuzahlung utilisation rate
(none)                     prem_total_pp(k)                Total contribution incl. BUZ
zill_rate x S              alpha_total_pp()                Zillmerised acquisition charge
alpha(k)                   alpha_amort_pp(k)               Its annual instalment
alpha_z(k)                 alpha_zuz_pp(k)                 Acquisition charge on a Zuzahlung
u(k)                       unit_cost_pp(k)                 Stueckkosten, inflating
N(k)                       prem_to_av_pp(k)                Premium credited after charges
premiums(t)                premiums(t)                     Laufende Beitraege, fund level
zuzahlungen(t)             zuzahlungen(t)                  Zuzahlungen, fund level
A^p(k, .)                  av_pp_at(k, timing)             Deckungskapital per paying policy
A^p(k)                     av_pp(k)                        Its start-of-year value
A^f(k, .)                  av_pu_at(k, timing)             Premium-free block, fund level
A(k, .)                    av_at(k, timing)                Whole Deckungskapital, fund level
A(k)                       av(k)                           Its start-of-year value
(declared)                 decl_rate(k)                    Declared laufende Verzinsung
i(k)                       cred_rate(k)                    max(gtd_rate, decl_rate(k))
q^t(x, y)                  mort_rate_at_age(x, y)          First-order table rate
(table)                    mort_rate_base(t)               Table rate of the year of month t
q(t)                       mort_rate(t)                    Best-estimate annual death rate
q_mth(t)                   mort_rate_mth(t)                Its geometric twelfth
f(t)                       bf_rate(t)                      Beitragsfreistellung rate, annual
l(t)                       pols_if(t)                      In force at the start of month t
l^p(t)                     pols_paying(t)                  Premium-paying subset
l^f(t)                     pols_paidup(t)                  Premium-free subset
l(t)(1-q_mth)              pols_if_at(t, timing)           BEF_DECR / AFT_DEATH / AFT_FREEZE
(none)                     pols_death(t)                   Expected deaths in month t
(none)                     pols_death_paying(t)            of which premium-paying
(none)                     pols_death_paidup(t)            of which premium-free
(none)                     pols_freeze(t)                  Beitragsfreistellung transfers
g(t)                       pols_gtd(t)                     Rentengarantiezeit continuations
(current)                  rentenfaktor_curr()             Aktueller Rentenfaktor at ret_age
(options)                  rf_option_factor()              Option reduction on the factor
R                          rentenfaktor_applied()          The factor actually applied
F                          fund_at_conv()                  Fund converted at Rentenbeginn
b(k)                       ann_bonus_rate(k)               Ueberschussrente uplift
a(k)                       ann_pp(k)                       Annual annuity per annuitant
a(k) / 12                  ann_mth_pp(t)                   The monthly Rente instalment
(none)                     db_pp(k)                        Reserve released per paying death
(none)                     db_pu_pp(k)                     Reserve released per paid-up death
claims_death, _annuity,    claims(t, kind)                 Benefit outgo by kind
claims_survivor
E(t)                       expenses(t)                     Insurer expense outgo
C(t)                       commissions(t)                  Commission outgo
net_cf(t)                  net_cf(t)                       Net cash flow, income positive
liability_cf(t)            liability_cf(t)                 The same stream, outgo positive
=========================  ==============================  ==============================

Four names needed care.

``av_pp_at`` is **per premium-paying policy** and ``av_pu_at`` is the premium-free block
**at fund level**. They are not two spellings of one quantity and they must not be
averaged into a single per-policy figure: a policy that froze at duration 5 and one that
froze at duration 15 hold different reserves, only the aggregate of the second kind is
meaningful, and collapsing the two is the third listed modeling pitfall.
:func:`av_at` is the fund-level total,
``av_pp_at(k, .) x pols_paying(12 k) + av_pu_at(k, .)``, and it is the only one of the
three that rolls forward on mortality alone. All three take a projection **year**: one
premium, one set of charges and one interest credit fall per *Versicherungsjahr*, so the
account has nothing to say about a month.

``bf_rate`` is the *Beitragsfreistellung* rate and is emphatically **not** ``lapse_rate``.
There is no lapse decrement on this product and no cells of that name anywhere in the
model. A freeze is a transfer between two ledgers, not an exit: it appears in
:func:`pols_paying` and :func:`pols_paidup` and **not** in :func:`pols_if`, which
decrements on mortality alone.

``prem_total_pp`` reconstructs the contribution the policyholder actually pays,
``(P(t) + Z(t)) / (1 - buz_prem_share)``, and is a **reporting cells that enters no cash
flow**. The BUZ premium buys a cover this model does not project — the disability
mechanics belong to ``BU_DE_S`` — so it appears in no :func:`result_cf` column and in
:func:`net_cf` at no ``t``. Modelling it as premium income with no benefit is the
seventeenth pitfall.

``claims(t, "DEATH")`` is not a lump sum to a beneficiary. § 10 EStG requires everything
paid to a survivor to be paid **as an annuity**, so what is booked at the moment of death
is the *Deckungskapital* leaving this contract as the **single premium of a survivor's
annuity** — itself a new liability, an immediate annuity, that this model does not
project. Reading it as a payable capital sum misreads the product, which is the tenth
pitfall.

.. rubric:: The product is defined by prohibitions

The entitlement under a *Basisrentenvertrag* is *nicht vererblich*, *nicht übertragbar*,
*nicht beleihbar*, *nicht veräußerbar* and *nicht kapitalisierbar*. Arithmetically that
means there is **no surrender value at any duration**, no *Kapitalwahlrecht*, no
*Teilkapitalauszahlung* and no lump sum of any kind at any date. The one commutation
Schicht 1 does allow — the *Kleinbetragsrenten-Abfindung* of § 10 Abs. 1 Nr. 2 Satz 3
EStG — is left out of this model by choice and not by prohibition; ``model.md`` gives the
reasons. § 169 VVG — the *Rückkaufswert*, the *Mindestrückkaufswert*, the *Stornoabzug* —
is inoperative on this contract.

So this model has **no ``lapse_rate``, no ``surr_rate``, no ``cv_pp``, no ``loan_pp``,
no ``withdrawals`` and no ``claims_lapse`` column**. Those are structural absences, not
switched-off options, and :func:`check_no_capital` asserts the consequence at every
``t``: the only payments the model can make are an annuity instalment, a
*Rentengarantiezeit* continuation and a survivor's single premium.

The mirror error is subtler than importing a surrender column, and it is worth naming:
computing a *Rückkaufswert* internally "for reference" and then flooring the
*Deckungskapital* at it. :func:`prem_to_av_pp` is negative in the first years of a
heavily zillmerised contract and the account is **not** floored, because there is no
*Rückkaufswert* for a floor to protect. That is why a German *Deckungskapital* starts
near zero.

.. rubric:: Two ledgers, one model point

A *Beitragsfreistellung* under § 165 VVG survives intact on this contract and is its only
behavioural exit. It stops the premium and moves the policy to the premium-free cohort,
where its *Deckungskapital* is still credited, still pays the *Stückkosten* and the
reserve charge, stops paying the premium charge and the *Zillmerung* instalment, and
still converts at *Rentenbeginn*. It does not end the contract, release any value, change
the *Rentenbeginn* or release any of the § 10 constraints.

The model therefore carries :func:`pols_paying` and :func:`pols_paidup` and their two
account blocks, and

    ``pols_if(t + 1) = pols_if(t) x (1 - mort_rate_mth(t))``

with ``bf_rate`` absent from the identity. :func:`check_pols_roll_fwd` asserts both that
the two ledgers sum to :func:`pols_if` and that :func:`pols_if` decrements on mortality
alone. A model point opens either **entirely** premium-paying or **entirely**
premium-free (``paidup_at_init``); a part-paid-up book is two model points, because
averaging the two cohorts' reserves is the third pitfall.

No *Wiederinkraftsetzung* is modelled: the premium-free block is absorbing, which is
conservative on premium income and is a standardization rather than a contract fact.

.. rubric:: The declared rate is the total credited rate

``cred_rate(k) = max(gtd_rate, decl_rate(k))``, a maximum and not a sum. A German
*laufende Verzinsung* is quoted as the **total** rate credited to the *Deckungskapital*,
already including the contract's *Rechnungszins*; adding the declared rate on top of the
guarantee is the sixth pitfall. The guarantee is a cohort fact fixed at conclusion and
carried on the model point as ``gtd_rate``, so a book spanning the 2,75 % vintage of 2006
and the 1,00 % vintage of 2025 has both branches of the ``max`` live at once — model
point 8 credits its guarantee in every year while the anchor credits the declared path in
every year.

The reserve charge γ is netted inside the same step, ``(1 + cred_rate(k) - gamma_av)``,
and the *Stückkosten* are taken before it. γ, β, the *Stückkosten* and the *Zillmerung*
instalment are **deductions from the policyholder's account** — insurer income — and the
insurer's own outgo is the acquisition expense, the commission, the maintenance expense
and the annuity administration. Booking a charge as both is the fourth pitfall, and it is
why :func:`expenses` is invariant to ``beta_prem``, ``gamma_av`` and ``zill_rate``: those
three move :func:`net_cf` only through the smaller annuity the smaller fund buys at
*Rentenbeginn*.

.. rubric:: The conversion at Rentenbeginn

At the start of projection year ``T = ret_y()`` — equivalently at the end of month
``ret_t() - 1`` — the whole fund carried out of year ``T - 1``, grossed up by the
*Schlussüberschussanteil*, converts::

    fund_at_conv()  = av_at(T, "BEF_PREM") x (1 + terminal_bonus_rate)

    ann_pp(T)       = fund_at_conv() / pols_if(ret_t()) / rf_unit
                      x rentenfaktor_applied() x ann_freq

    ann_mth_pp(t)   = ann_pp(proj_year(t)) / ann_freq

There is no lump sum, no election and no notice period — this is the one date in the
contract's life at which anything happens, and nothing happens at it that the
policyholder chooses. ``av(k)`` is zero for every ``k > T``; at ``k = T`` itself the
published ``av`` is the pre-conversion fund, which is the number the annuity is struck on
and the one a reader of the worked example needs. :func:`check_conversion` inverts the
identity and is zero at every other ``k``; :func:`check_av_roll_fwd` asserts that the
account is emptied at ``T`` and stays empty.

``ann_pp`` is an **annual** amount and is nobody's payment: the *Rentenfaktor* is quoted in
euro a month, ``ann_freq = 12`` is the conversion from one to the other, and
:func:`ann_mth_pp` is the instalment that is actually paid — monthly in advance, from
``t = ret_t()``, to whoever is alive at the start of the month. The annual figure survives
as the cells the conversion and the *Überschussrente* are stated on, because both are
annual terms: the factor is applied once and the uplift compounds once a year, so the
twelve instalments of a payout year are equal and the thirteenth is ``(1 + b)`` times the
twelfth.

``rentenfaktor_applied() = max(rentenfaktor_gtd, rentenfaktor_curr()) x
rf_option_factor()``. The ``max`` is the contract's own rule, and it means the projection
is sensitive to whichever of the two factors is higher and completely insensitive to the
other: the anchor converts at the current 31,50 € and model point 13 at its guaranteed
34,00 €. Taking the guaranteed factor when the current one is higher, or the reverse, is
the thirteenth pitfall.

**The conversion basis is not the projection basis, and that is deliberate.**
``rentenfaktor_gtd`` was struck at inception on first-order DAV 2004 R with a prudential
margin and a conservative interest basis; the projection runs on the best estimate,
``mort_rate(t) = mort_be_factor x mort_rate_base(t)``. The wedge between the two is the
payout phase's *Risikoüberschuss*, and ``ann_bonus_rate`` — a *teildynamische Rente* —
is the mechanism that gives it back to the annuitant. :func:`ann_pp` at ``ret_t()`` is
therefore invariant to ``mort_be_factor`` while ``claims_annuity`` is not. A model that
converted on its own best-estimate mortality would abolish the wedge and with it the
whole German payout-phase surplus mechanic, which is the eleventh pitfall.

.. rubric:: Death before Rentenbeginn pays nothing in the base design

With the survivor rider off — ``surv_annuity_rate = 0``, which is the base design and the
anchor's setting — a death in the *Aufschubphase* pays **nothing**: the reserve is
released as a mortality profit, because the entitlement is *nicht vererblich*. With the
rider on, the released reserve is payable **only where an eligible survivor exists**, and
:func:`claims` weights it by ``elig_surv_prob``.

Either way the reserve leaves the fund, which is why

    ``av_at(k + 1, "BEF_PREM") = av_at(k, "AFT_INT") x (1 - mort_rate(12 k))``

holds whether or not the rider is on — at the year's **annual** rate, which is exactly what
its twelve monthly rates compound to. That single identity is the arithmetic content of
*nicht vererblich*, and :func:`check_av_roll_fwd` asserts it. The survivor's annuity
fraction is paid for through :func:`rf_option_factor` — a reduction in the
*Rentenfaktor* — rather than by scaling the death benefit, which is how a German tariff
prices the cover.

.. rubric:: The Rentengarantiezeit is a stream, never a lump sum

A *Rentengarantiezeit* runs ``guarantee_period_y`` years **from *Rentenbeginn***, not from
each death, so every continuation ends on the same date and :func:`pols_gtd` is a
one-line recursion ending at :func:`gtd_end_t`. On this grid the window is what the
contract says it is — ``12m`` guaranteed monthly **instalments** — and a continuation
begins in the month after the death that triggered it rather than in the following year. The instalments continue **only to a
permitted survivor**, so each death contributes ``elig_surv_prob`` of a continuation and
where no eligible survivor exists the payments simply cease. They are **never
commutable**: no cash flow anywhere in this model discounts a continuation into a capital
sum. Getting either limb wrong is the fourteenth pitfall.

.. rubric:: Modules that are off in the base run

Three constructions are implemented and are inert on the anchor, so the base run
reproduces the worked example while the machinery stays visible and testable:

- **The survivor's annuity**, ``surv_annuity_rate = 0`` on the anchor, which makes
  ``claims_death`` structurally zero at every ``t``. Model points 3 and 12 switch it on.
  With it off, ``elig_surv_prob`` has no effect on any cash flow.  Where it is on, the
  reserve released per death is the **annual** ``db_pp(k)``, struck at the end of the
  *Versicherungsjahr*, so the month decides when it is released and not how much.
- **The *Rentengarantiezeit***, ``guarantee_period_y = 0`` on the anchor, which makes
  ``claims_survivor`` structurally zero and ``pols_gtd`` zero at every ``t``. Model points
  4 and 12 switch it on at 10 and 20 years.
- **The BUZ**, ``buz_prem_share = 0`` on the anchor. It is carried as a premium share and
  nothing else; model point 11 sets it to 0.49, the statutory boundary, and
  ``prem_total_pp`` is the only cells that reads it.

Both zero columns are **published rather than dropped**, because a column of zeros states
the product fact where a missing column would only hide it.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — *laufende Beiträge* and *Zuzahlungen* in, death
benefits, annuity instalments, survivor continuations, expenses and commission out —
which is the library-wide sign. :func:`liability_cf` publishes the same stream
outgo-positive, ``liability_cf(t) = -net_cf(t)`` exactly, so a Solvency II best estimate
is ``sum v(t) x liability_cf(t)`` over whatever discount curve the valuation layer
supplies. Both are columns of :func:`result_cf`, so the identity is verifiable in the
frame rather than only in prose. Unlike ``TD_FR_S``, :func:`expenses` here does **not**
include the commission: the two are separate lines of the notes' own cash flow statement
and :func:`net_cf` subtracts each once.

The shape to expect on the monthly frame is a saw-tooth: the whole *Versicherungsjahr*'s
*Beitrag* and *Zuzahlung* fall in the first month of each projection year and nothing else
does, so that month is strongly positive and the other eleven carry a twelfth of the
maintenance expense and are slightly negative. Summed into years by
:func:`result_cf_annual` the familiar shape returns — a large new-business strain at
``k = 0``, since the *Zillmerung* instalment is an account deduction and costs the insurer
nothing but the initial commission at 2,5 % of the *Beitragssumme* and the acquisition
expense both fall at inception against a single year's contribution; then two decades of
positive accumulation-phase margin; a *Rentenbeginn* at which the fund converts and no
cash moves; and a long negative payout tail, now paid one instalment at a time.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series, from *model_point_table.csv*."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def pols_if_init():
    """The number of policies the model point represents at the valuation date.

    The opening value of :func:`pols_if`, and therefore the first ``pols_if`` value of
    :func:`result_cf`.  It opens entirely in :func:`pols_paying` or entirely in
    :func:`pols_paidup` according to ``paidup_at_init``.
    """
    return float(model_point()["pols_if_init"])


def omega_age():
    """The terminal age of the mortality table: the last ``age`` in *mort_table.csv*.

    121 on the shipped **[std]** table, the age German annuity tables are conventionally
    carried to.  The projection runs to it because the annuity is lifelong, and
    :func:`mort_rate` returns 1.0 there, so the last survivor dies in the last month of the
    terminal year, at ``t = proj_len() - 1``, and there is no tail state of any kind.
    """
    return int(data.mort_table().index.max())                        # noqa: F821


def proj_len_y():
    """n: the **number of projected years**, ``omega_age() - age(0) + 1``.

    The annual coordinate of the projection, and the one the contract is written in: the
    declared rate, the *Beitragsdynamik*, the *Zillmerung* window, the *Zuzahlung* end
    date, the *Beitragsfreistellung* and the *Überschussrente* are all annual terms.  77 on
    the anchor cell — twenty-two years of *Aufschubphase* at attained ages 45 to 66 and
    fifty-five years of *Rentenphase* at ages 67 to 121.

    This is the annual-step model's own ``proj_len()``, and ``k = 0 ... proj_len_y() - 1``
    indexes exactly the rows that model projected.
    """
    return omega_age() - age(0) + 1


def proj_len():
    """The **number of projected months**, ``12 x proj_len_y()``.

    The **exclusive end** of the frame: :func:`result_cf` is 0-based and runs
    ``t = 0 ... proj_len() - 1``, so ``len(result_cf()) == proj_len()``, which is this
    library's reading of ``proj_len()`` and is asserted by the conventions suite.  924 on
    the anchor cell.

    The last month is the last month of the terminal year, where :func:`mort_rate` is 1:
    the last survivor dies at ``t = proj_len() - 1``, ``pols_if(proj_len()) = 0`` exactly
    and there is no tail state of any kind.
    """
    return 12 * proj_len_y()


def proj_year(t):
    """k(t): the 0-based **projection year** month t falls in, ``t // 12``.

    The bridge between the model's two clocks.  ``t`` counts projection **months** from the
    valuation date and is the argument of the in force, the decrements, the claims, the
    expenses and the annuity instalments; ``k`` counts projection **years** and is the
    argument of everything the contract states per *Versicherungsjahr* — the premium, the
    *Zuzahlung*, the four account charges, the declared rate, the *Deckungskapital* and the
    *Überschussrente*.  A cells' argument therefore says which clock it is on, and this is
    the only place the two meet.

    ``k`` is the annual-step model's own ``t``, which is what makes the two comparable row
    by row: ``result_cf_annual().loc[k]`` is that model's row ``k``.
    """
    return t // 12


def is_anniv(t):
    """True in the **last** month of a projection year, ``t % 12 == 11``.

    The frame opens at a policy anniversary — an in-force model point has completed
    ``duration_init`` whole policy years at the valuation date — so a projection year is a
    *Versicherungsjahr* and its last month is the month before the next anniversary.  It is
    where everything contractually annual falls: the year's *Beitragsfreistellung*, the
    interest credit, and the certainty that the terminal year kills the last survivor.
    """
    return t % 12 == 11


def age_y(k):
    """x(k): attained age in projection year k.

    ``entry_age + duration_init + k``.  Age last birthday at conclusion
    (*Eintrittsalter*), stepping on the policy anniversary **[std]**: no German convention
    was established, and here mortality drives the annuity's duration rather than any
    benefit amount, so a half-year offset is second order.
    """
    return int(model_point()["entry_age"]) + int(model_point()["duration_init"]) + k


def age(t):
    """x(t): attained age in projection month t, ``age_y(proj_year(t))``.

    The age **steps on the anniversary** and not monthly, which is what lets one
    generational mortality surface serve every month of a *Versicherungsjahr* and is why
    the twelve months of a year share one annual death rate.
    """
    return age_y(proj_year(t))


def duration_y(k):
    """d(k): **completed** policy years at the start of projection year k.

    ``duration_init + k``, so a new-business point opens at ``duration_y(0) = 0``.  The
    *Beitragsdynamik*, the *Zillmerung* amortisation window and the *Zuzahlung* end date
    are all keyed to this rather than to ``k``, which is what makes an in-force model
    point work: model point 6 opens at ``duration_y(0) = 17`` and its premium at
    ``prem_base_pp x 1.02^17``.  Keying any of the three to ``k`` is the seventh pitfall.

    The ``dur`` index of *behaviour_table.csv* is the **policy year**, ``duration_y(k) + 1``.
    """
    return int(model_point()["duration_init"]) + k


def duration(t):
    """d(t): **completed** policy years at the start of projection month t.

    ``duration_y(proj_year(t))``.  It steps on the anniversary, so the twelve months of a
    projection year share one policy duration and therefore one row of
    *behaviour_table.csv*.
    """
    return duration_y(proj_year(t))


def duration_mth(t):
    """**Completed policy months** at the start of projection month t.

    ``12 x duration_init + t``.  Carried because it is the only quantity that distinguishes
    two model points at the same projection month — a new-business point at ``t = 12`` has
    completed twelve policy months, an in-force point opening at ``duration_init = 17`` has
    completed 216 — and because ``duration(t) = duration_mth(t) // 12`` states in code that
    the policy duration is the policy month divided down.
    """
    return 12 * int(model_point()["duration_init"]) + t


def policy_year(t):
    """The contractual **1-based** policy year label of month t, ``duration(t) + 1``.

    The label the AVB and *behaviour_table.csv* use: the first year of the contract is
    policy year 1 and ``duration`` is 0 through the whole of it.  Published so that a
    reader never has to decide which of the two a table's ``dur`` column means.
    """
    return duration(t) + 1


def cal_year_y(k):
    """y(k): calendar year at the start of projection year k.

    ``conclusion_year + duration_init + k``.  Carried because the mortality basis is
    **generational**: DAV 2004 R is a *Generationentafel* with the improvement inside the
    table, so :func:`mort_rate_at_age` needs a calendar year as well as an age.  Two model
    points that reach the same attained age in different calendar years see different
    rates, and treating the basis as a period table is the fifteenth pitfall.
    """
    return int(model_point()["conclusion_year"]) + int(model_point()["duration_init"]) + k


def cal_year(t):
    """y(t): calendar year in projection month t, ``cal_year_y(proj_year(t))``.

    Steps on the policy anniversary rather than on 1 January, which is the same convention
    the attained age follows and the one the annual-step model necessarily used.
    """
    return cal_year_y(proj_year(t))


def ret_y():
    """T: the projection **year** in which *Rentenbeginn* falls, ``ret_age - age(0)``.

    22 on the anchor cell.  **``T < 0`` for a model point that opens in the
    *Rentenphase***, in which case the conversion never occurs inside the projection,
    ``ann_pp(0) = ann_pp_init`` and :func:`check_conversion` is vacuously true.  Model
    point 8 has ``ret_y() = -3``.

    The earliest permitted *Rentenbeginn* is the completion of the 62nd year of life for
    contracts concluded after 31 December 2011 and the 60th for earlier ones; the model
    reads ``ret_age`` from the model point and does not enforce the floor, which is a
    contract-writing rule rather than a projection rule.
    """
    return int(model_point()["ret_age"]) - age(0)


def ret_t():
    """The projection **month** of the first annuity instalment, ``12 x ret_y()``.

    The *Rentenbeginn* falls at the end of the deferment: the last accumulation month is
    ``ret_t() - 1``, the fund is converted on the balance struck there, and the first of the
    monthly instalments is paid at ``t = ret_t()``.  264 on the anchor cell.

    Negative for a model point that opens in the *Rentenphase*, and every comparison against
    it is written ``max(0, ret_t())`` for that reason.
    """
    return 12 * ret_y()


def gtd_end_t():
    """The last projection **month** in which a *Rentengarantiezeit* continuation is payable.

    ``max(0, ret_t()) + 12 x guarantee_period_y - 1``.  The guarantee runs from
    *Rentenbeginn*, **not** from each death, so every continuation ends on the same date and
    :func:`pols_gtd` is zero from ``gtd_end_t() + 1`` onwards however late the death that
    started it.  Zero-length where ``guarantee_period_y = 0``, in which case
    :func:`pols_gtd` is zero everywhere.

    On the monthly grid the window is what the contract says it is — ``12m`` guaranteed
    monthly **instalments** — where the annual grid could only offer ``m`` payments of a
    whole year's annuity each.
    """
    return max(0, ret_t()) + 12 * int(model_point()["guarantee_period_y"]) - 1


def beitragssumme_pp():
    """S: the contract's *Beitragssumme* at inception, per policy.

    The sum of the contractual *laufende Beiträge* over the whole premium term
    **including** the *Beitragsdynamik* and **excluding** *Zuzahlungen* and the
    *Ratenzahlungszuschlag*::

        S = sum_{u=0}^{m-1} prem_base_pp x (1 + prem_dyn_rate)^u,   m = ret_age - entry_age

    and simply ``prem_base_pp`` for a single premium.  Excluding *Zuzahlungen* is the
    conservative reading of a question no retrieved source settles, and it matters twice:
    S is the base of the 25 ‰ *Höchstzillmersatz* cap on the acquisition charge written
    into the account, and it is the base of the initial commission.  On a long-dated
    contract with a *Dynamik* the cap binds in euro terms far above what the same
    percentage would allow on a short one.

    Struck once, at inception, from the *contract's* own terms — not from the projection —
    so an in-force model point carries the same S it was written with.
    """
    dyn = float(model_point()["prem_dyn_rate"])
    base = float(model_point()["prem_base_pp"])
    if model_point()["prem_form"] == "single":
        return base
    m = int(model_point()["ret_age"]) - int(model_point()["entry_age"])
    return sum(base * (1.0 + dyn) ** u for u in range(max(m, 0)))


def prem_freq_load():
    """phi: the *Ratenzahlungszuschlag* for the model point's payment frequency.

    Read from *option_table.csv* under ``option_id = "prem_mode"``: 1.000 annual, 1.020
    half-yearly, 1.030 quarterly, 1.050 monthly **[std]**.  It multiplies the *laufender
    Beitrag* and **nothing else** — not the *Zuzahlung*, which carries no frequency
    loading because it is a single payment, and not a single premium, which is why
    :func:`prem_freq_load` returns 1.0 for ``prem_form = "single"``.  Applying it twice, or
    to the *Zuzahlung*, is the eighth pitfall.
    """
    if model_point()["prem_form"] == "single":
        return 1.0
    return float(data.option_table().loc[                            # noqa: F821
        ("prem_mode", model_point()["prem_mode"]), "factor"])


def prem_base_pp(k):
    """The contractual *laufender Beitrag* in year k, before the *Ratenzahlungszuschlag*.

    ``prem_base_pp x (1 + prem_dyn_rate)^duration_y(k)`` on the ``regular`` form: the
    *Beitragsdynamik* compounds on the base premium from **inception**, so it is keyed to
    the policy duration and not to the projection year.  For ``prem_form = "single"`` the
    *Einmalbeitrag* is paid once, at ``k = 0`` and only where ``duration_init = 0``, and is
    zero at every other ``k``.

    This is the contractual amount.  What is actually charged is :func:`prem_pp`, which
    applies phi and stops at *Rentenbeginn*.
    """
    if model_point()["prem_form"] == "single":
        if k == 0 and int(model_point()["duration_init"]) == 0:
            return float(model_point()["prem_base_pp"])
        return 0.0
    return (float(model_point()["prem_base_pp"])
            * (1.0 + float(model_point()["prem_dyn_rate"])) ** duration_y(k))


def prem_pp(k):
    """P(k): the *laufender Beitrag* charged per premium-paying policy in year k.

    ``prem_base_pp(k) x prem_freq_load()``, taken at the **start** of the year (annual in
    advance; a fractionated mode changes the amount through the *Ratenzahlungszuschlag*,
    not the grid).  Zero from ``k = ret_y()`` — premiums stop at *Rentenbeginn* — and zero
    on a model point that opens *beitragsfrei*, whose whole cohort is in
    :func:`pols_paidup` anyway.  Letting premiums run past *Rentenbeginn* is the seventh
    pitfall.

    A dying policy has already paid the year's premium, because deaths fall at the end of
    the year: :func:`premiums` is weighted by the **opening** :func:`pols_paying` and is
    not further multiplied by ``(1 - mort_rate)``.
    """
    if k < 0 or k >= ret_y() or k >= proj_len_y():
        return 0.0
    if int(model_point()["paidup_at_init"]) == 1:
        return 0.0
    return prem_base_pp(k) * prem_freq_load()


def zuz_take_up(k):
    """The *Zuzahlung* utilisation rate in year k, from *behaviour_table.csv*.

    Looked up at ``dur = duration_y(k) + 1``, the policy year: 0.70 at policy years 1–5,
    0.85 at 6–15, 0.90 at 16+ **[std]**, clamped to the last row beyond the table.

    A *utilisation rate*, not a contract term.  The contribution the *Höchstbetrag* makes
    possible is paid out of a profit not known until the year end, so whether it is paid
    at all is behavioural; a model that treats the *Zuzahlung* as contractual has quietly
    set this to 1.0.  Nothing in the delib corpus supports any level.
    """
    tab = data.behaviour_table()                                     # noqa: F821
    key = model_point()["beh_table_id"]
    d = min(duration_y(k) + 1, int(tab.loc[key].index.max()))
    return float(tab.loc[(key, max(d, 1)), "zuz_take_up"])


def zuz_pp(k):
    """Z(k): the *Zuzahlung* paid per premium-paying policy in year k.

    ``zuzahlung_pp x zuz_take_up(k)``, taken at the start of the year alongside the
    *laufender Beitrag* and carrying **no** *Ratenzahlungszuschlag*.  Zero from
    ``k = ret_y()``, zero once ``duration_y(k) >= zuzahlung_end_dur``, and zero on a
    model point that opens *beitragsfrei*.

    The *Zuzahlung* is the product's signature premium form — a self-employed buyer tops
    the contract up out of a good year — and it is the reason ``zuzahlungen`` is published
    as a column of its own rather than folded into ``premiums``: it is a distinct premium
    form on a distinct charge basis, carrying ``alpha_zuz_rate`` instead of a share of the
    *Zillmerung*.
    """
    if k < 0 or k >= ret_y() or k >= proj_len_y():
        return 0.0
    if int(model_point()["paidup_at_init"]) == 1:
        return 0.0
    if duration_y(k) >= int(model_point()["zuzahlung_end_dur"]):
        return 0.0
    return float(model_point()["zuzahlung_pp"]) * zuz_take_up(k)


def prem_total_pp(k):
    """The **total** contribution the policyholder pays in year k, including the BUZ.

    ``(prem_pp(k) + zuz_pp(k)) / (1 - buz_prem_share)``.  A **reporting cells that enters
    no cash flow**: it appears in no :func:`result_cf` column and in :func:`net_cf` at no
    ``k``.  ``prem_base_pp`` is the *old-age* contribution; the BUZ premium buys a cover
    this model does not project, and its disability mechanics belong to ``BU_DE_S``.

    ``buz_prem_share < 0.50`` is the statutory invariant — the supplementary covers
    together must stay strictly below half the total contribution or the whole
    contribution loses its *Sonderausgabenabzug* — and model point 11 sits at 0.49, the
    boundary.  Modelling the BUZ as premium income with no benefit is the seventeenth
    pitfall.
    """
    return (prem_pp(k) + zuz_pp(k)) / (1.0 - float(model_point()["buz_prem_share"]))


def alpha_total_pp():
    """The zillmerised acquisition charge written into the account, per policy.

    ``zill_rate x beitragssumme_pp()``.  The *Höchstzillmersatz* caps it at **25 ‰ of the
    *Beitragssumme*** for business written from 1 January 2015, reduced from 40 ‰ by the
    LVRG; the shipped tariffs carry the two rates and the in-force pre-2015 model points
    take the older one.

    This is a **deduction from the policyholder's *Deckungskapital***, hence insurer
    income — not an expense.  The insurer's own acquisition outgo is ``acq_expense_pp``
    plus the initial commission, and the German design is precisely that what the insurer
    pays out is sized to what it may write into the reserve.
    """
    return (float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "zill_rate"]) * beitragssumme_pp())


def alpha_amort_pp(k):
    """alpha(k): the *Zillmerung* instalment struck against the account in year k.

    ``alpha_total_pp() / zill_spread_y`` in equal instalments over the contract's first
    ``zill_spread_y = 5`` years of *Aufschubphase* — **of the contract**, not of the
    projection — and zero thereafter.  An in-force model point past duration 5 therefore
    sees none of it at any ``k``: model point 6, at ``duration_init = 17``, sees zero
    throughout.  A single-premium contract runs the same five instalments, so the total
    written into its account is the same 25 ‰ of the *Beitragssumme* and the debit simply
    outlives the one premium that paid for it.

    Charging the whole *Zillmerung* in year one is the fifth pitfall.  On the anchor cell
    the instalment is equal at ``k = 0 ... 4``, zero from ``k = 5``, and the five sum to
    ``zill_rate x beitragssumme_pp()`` exactly.

    Whether the AltZertG's five-year spreading of acquisition and distribution costs
    reaches *Basisrentenverträge* at all was not established; the five years here are the
    LVRG-era German market shape and are **[std]**.
    """
    if k < 0 or k >= ret_y() or k >= proj_len_y():
        return 0.0
    if int(model_point()["paidup_at_init"]) == 1:
        return 0.0
    if duration_y(k) >= zill_spread_y:                                 # noqa: F821
        return 0.0
    return alpha_total_pp() / zill_spread_y                          # noqa: F821


def alpha_zuz_pp(k):
    """alpha_z(k): the acquisition charge on the year's *Zuzahlung*, per paying policy.

    ``alpha_zuz_rate x zuz_pp(k)``, charged in the year the *Zuzahlung* is paid **[std]**.
    A *Zuzahlung* is not part of the *Beitragssumme* and so carries no share of the
    *Zillmerung*; it carries its own single charge instead, which is the normal German
    treatment of a top-up.  Zero where no *Zuzahlung* is paid.
    """
    return (float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "alpha_zuz_rate"]) * zuz_pp(k))


def unit_cost_pp(k):
    """u(k): the *Stückkosten* charged to the account in year k, per policy.

    ``unit_cost_pp x (1 + expense_infl)^k`` **[std]** — 36,00 € inflating at 1,5 %
    a year.  Charged to **both** blocks: a premium-free policy keeps paying the
    *Stückkosten* and the reserve charge and stops paying beta and the *Zillmerung*
    instalment, which is the whole economic content of a *Beitragsfreistellung*.

    An account deduction, not an expense.  The insurer's own maintenance outgo is
    ``maint_expense_pp`` and is a separate line of :func:`expenses`.
    """
    return (float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "unit_cost_pp"])
        * (1.0 + float(data.charge_table().loc[                      # noqa: F821
            model_point()["tariff_id"], "expense_infl"])) ** k)


def prem_to_av_pp(k):
    """N(k): the premium credited to the account in year k, after all four charges.

    ``(P(k) + Z(k)) x (1 - beta_prem) - alpha_amort_pp(k) - alpha_zuz_pp(k) -
    unit_cost_pp(k)``.

    **N(k) may be negative** in the first years of a heavily zillmerised contract, and it
    is **not floored**: there is no *Rückkaufswert* on this product for a floor to protect,
    and flooring the account at an internally computed surrender value would change the
    early years even though nothing is ever paid.  That a German *Deckungskapital* starts
    near zero is a consequence of this line and not a modelling artefact.

    Zero from ``k = ret_y()``: there is no account in the *Rentenphase*.
    """
    if k < 0 or k >= ret_y() or k >= proj_len_y():
        return 0.0
    beta = float(data.charge_table().loc[                            # noqa: F821
        model_point()["tariff_id"], "beta_prem"])
    return ((prem_pp(k) + zuz_pp(k)) * (1.0 - beta)
            - alpha_amort_pp(k) - alpha_zuz_pp(k) - unit_cost_pp(k))


def prem_due(t):
    """True in the month the year's *Beitrag* falls due, ``t % 12 == 0``.

    The whole *Versicherungsjahr*'s contribution is taken in the **first month** of the
    projection year, with the *Zuzahlung* beside it.  The *Ratenzahlungszuschlag* is the
    reason a fractionated mode needs no finer grid than this: a German tariff prices
    half-yearly, quarterly and monthly payment by **loading the amount**, not by moving the
    *Versicherungsperiode*, so :func:`prem_freq_load` changes what is paid and this cells
    changes nothing.  The account is a *Deckungskapital* struck per *Versicherungsjahr* and
    is credited the same annual contribution whatever the mode.
    """
    return t % 12 == 0


def premiums(t):
    """*Laufende Beiträge* collected in month t at fund level, an inflow.

    ``prem_pp(proj_year(t)) x pols_paying(t)`` in the month the year's premium falls due
    and zero in the other eleven, weighted by the **premium-paying** ledger and by the
    **opening** count: the premium falls at the start of the year and the year's deaths
    after it, so a policy that dies during the year has already paid for it.  Multiplying
    by ``(1 - mort_rate(t))`` here applies the death rule twice.

    Because the count at the start of a projection year is the annual-step model's own
    ``pols_paying(k)``, this column sums over a year to that model's premium income
    exactly.
    """
    if not prem_due(t):
        return 0.0
    return prem_pp(proj_year(t)) * pols_paying(t)


def zuzahlungen(t):
    """*Zuzahlungen* collected in month t at fund level, an inflow.

    ``zuz_pp(proj_year(t)) x pols_paying(t)`` in the month the year's premium falls due and
    zero in the other eleven: the *Zuzahlung* is a single payment made alongside the
    *laufender Beitrag* and carries no *Ratenzahlungszuschlag* precisely because it is not
    fractionated.

    Published as a column of its own rather than folded into :func:`premiums` because it is
    a distinct premium form on a distinct charge basis, and because setting ``zuz_take_up``
    to zero — which removes about two fifths of the anchor's contribution stream — is a
    legitimate variant a reader should be able to see the size of.
    """
    if not prem_due(t):
        return 0.0
    return zuz_pp(proj_year(t)) * pols_paying(t)


def mort_rate_at_age(x, y):
    """q^t(x, y): the **first-order** table death rate at age x in calendar year y.

    ``qx(x) x (1 - trend(x))^(y - mort_base_year)``, clipped to ``[0, 1]``.  The
    generational form: the improvement lives **inside** the basis, which is what makes
    DAV 2004 R a *Generationentafel* and what a replacement table must preserve.  Two
    model points at the same attained age in different calendar years see different rates,
    and the shipped table is anchored at ``mort_rate_at_age(67, 2005) = 0.014000``.

    First order, so it carries the DAV's prudential margins.  The guaranteed
    *Rentenfaktor* is struck on this basis; the projection runs on :func:`mort_rate`.
    """
    row = data.mort_table().loc[x]                                   # noqa: F821
    rate = (float(row["qx"])
            * (1.0 - float(row["trend"])) ** (y - mort_base_year))   # noqa: F821
    return min(max(rate, 0.0), 1.0)


def mort_rate_base(t):
    """The first-order table rate applying in projection month t, an **annual** rate.

    ``mort_rate_at_age(age(t), cal_year(t))``.  Split from :func:`mort_rate` so that the
    table rate and the best-estimate rate have separate names and the step between them is
    a single visible factor.  Both are annual rates of the projection year the month falls
    in: the age and the calendar year step on the anniversary, so the twelve months of a
    year share one table rate.
    """
    return mort_rate_at_age(age(t), cal_year(t))


def mort_rate(t):
    """q(t): the best-estimate **annual** death rate of the year month t falls in.

    ``mort_be_factor x mort_rate_base(t)``, the step from the shipped first-order table to
    a best estimate.  ``mort_be_factor = 0.85`` is **[std]** and is the single largest
    unanchored number in the payout phase.

    This is the library's two-speed convention: ``mort_rate`` is the **annual** rate and
    :func:`mort_rate_mth` the monthly rate the recursion actually applies.  Reading this
    one into a monthly roll-forward projects twelve years of mortality in one year.

    **The terminal age is absorbing**: ``mort_rate(t) = 1.0`` where
    ``age(t) >= omega_age()``, whatever ``mort_be_factor`` says, so the last survivor dies
    in the **last month** of the terminal year, ``pols_if(proj_len()) = 0`` exactly and the
    decrement closure identity holds to the last euro.  Without it the generational trend
    would carry the table's own terminal rate below 1 and leave a residue in force after
    the end of the table.

    Deaths fall at the end of the **month**, after that month's annuity instalment; the
    interest credit and the premium are annual and fall at the two ends of the year, so a
    dying policy has been credited its year's interest and has paid its year's premium.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_be_factor * mort_rate_base(t))              # noqa: F821


def mort_rate_mth(t):
    """The **monthly** death rate applied in projection month t.

    ``1 - (1 - mort_rate(t))^(1/12)``: the geometric twelfth of the year's annual rate, so
    the twelve months of a projection year compound back to it **exactly** and
    ``pols_if(12k)`` is the annual-step model's ``pols_if(k)`` to the last bit.  Dividing
    the annual rate by twelve instead would leave a residue that grows with the rate and is
    largest exactly where this product's cash flows are — in the tail of a lifelong annuity.

    A rate of **1 is a certainty and is not twelfth-rooted**: at the terminal age the whole
    cohort dies, and it dies in the last month of the year rather than a little in each, so
    the annuity is paid for the whole terminal year and ``pols_if(proj_len()) = 0``.
    """
    q = mort_rate(t)
    if q >= 1.0:
        return 1.0 if is_anniv(t) else 0.0
    return 1.0 - (1.0 - q) ** (1.0 / 12.0)


def bf_rate(t):
    """f(t): the *Beitragsfreistellung* rate of the year month t falls in, **annual**.

    Read from *behaviour_table.csv* at ``dur = policy_year(t)``: 4,0 % at policy years
    1–5, 3,0 % at 6–10, 2,0 % at 11+ **[std]**, clamped to the last row beyond the table.

    **An annual rate applied once a year, not a monthly one.**  § 165 VVG lets the
    policyholder demand a *Beitragsfreistellung* "für den Schluss der laufenden
    Versicherungsperiode", and § 12 Abs. 1 VVG makes that period the *Versicherungsjahr*
    here, so the election takes effect at the anniversary and :func:`pols_freeze` is
    non-zero only in the last month of a projection year.  That is also what keeps the
    premium-paying ledger bit-identical to the annual-step model's at every anniversary.

    **This is not a lapse rate and there is no lapse decrement on this product.** § 165 VVG
    survives and is the contract's only behavioural exit, but it removes the premium, not
    the policy: the rate moves policies from :func:`pols_paying` to :func:`pols_paidup` and
    appears nowhere in :func:`pols_if`.  Treating it as a lapse is the second pitfall.

    Zero from ``t = ret_t()`` — there is no premium left to stop — and zero on a
    single-premium contract for the same reason.  Applied to the **survivors** of the
    year's death decrement.
    """
    if t < 0 or t >= ret_t() or t >= proj_len():
        return 0.0
    if model_point()["prem_form"] == "single":
        return 0.0
    tab = data.behaviour_table()                                     # noqa: F821
    key = model_point()["beh_table_id"]
    d = min(policy_year(t), int(tab.loc[key].index.max()))
    return float(tab.loc[(key, max(d, 1)), "bf_rate"])


def pols_paying(t):
    """l^p(t): premium-paying policies at the **start** of projection month t.

    ``pols_if_init()`` at ``t = 0`` unless the model point opens *beitragsfrei*, then

        ``l^p(t + 1) = l^p(t) x (1 - q_mth(t)) - pols_freeze(t)``

    — the month's death decrement, and, in the last month of a projection year only, the
    *Beitragsfreistellung* on its survivors.  The weight on :func:`premiums` and
    :func:`zuzahlungen`, which are due in the first month of a year, so the count they see
    is the count the annual-step model saw.

    A model point opens **entirely** paying or **entirely** premium-free.  A part-paid-up
    book is two model points; averaging the two cohorts is the third pitfall.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return 0.0 if int(model_point()["paidup_at_init"]) == 1 else pols_if_init()
    return pols_paying(t - 1) * (1.0 - mort_rate_mth(t - 1)) - pols_freeze(t - 1)


def pols_paidup(t):
    """l^f(t): premium-free (*beitragsfreie*) policies at the start of projection month t.

    ``l^f(t + 1) = l^f(t) x (1 - q_mth(t)) + pols_freeze(t)``.  The block is **absorbing**:
    no *Wiederinkraftsetzung* is modelled, because none was established, which is
    conservative on premium income and is a standardization rather than a contract fact.

    A premium-free policy is still in force, still certified, still protected and still
    converts at *Rentenbeginn*.  It keeps paying the *Stückkosten* and the reserve charge
    out of its own *Deckungskapital* and stops paying beta and the *Zillmerung* instalment.
    Both charges are annual, so the block is carried at fund level by projection **year**
    in :func:`av_pu_at` while its head count is carried here by month.
    """
    if t < 0 or t > proj_len():
        return 0.0
    if t == 0:
        return pols_if_init() if int(model_point()["paidup_at_init"]) == 1 else 0.0
    return pols_paidup(t - 1) * (1.0 - mort_rate_mth(t - 1)) + pols_freeze(t - 1)


def pols_if(t):
    """l(t): policies in force at the **start** of projection month t, both cohorts.

    ``pols_paying(t) + pols_paidup(t)``, and the weight on every cash flow of the same
    :func:`result_cf` row.  It obeys

        ``pols_if(t + 1) = pols_if(t) x (1 - mort_rate_mth(t))``

    with ``bf_rate`` **absent from the identity**, because a *Beitragsfreistellung* is a
    transfer between the two ledgers and not an exit.  That is the whole of what
    distinguishes this product's decrement structure from a Schicht-3 annuity's, and
    :func:`check_pols_roll_fwd` asserts it.

    ``pols_if(proj_len())`` is defined and is **zero**, because :func:`mort_rate` is 1 in
    the terminal year and :func:`mort_rate_mth` places that certainty in its last month.
    It is read by :func:`check_pols_roll_fwd` and by nothing else; :func:`result_cf` stops
    at ``t = proj_len() - 1``.
    """
    return pols_paying(t) + pols_paidup(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside projection month t.

    ``"BEF_DECR"``
        l(t), the start of the month, before any decrement; the same number as
        :func:`pols_if` and the weight on that month's cash flows.

    ``"AFT_DEATH"``
        ``l(t) x (1 - q_mth(t))``, after the month's death decrement, which falls at the
        end of the month.  In the last month of a projection year this is the population
        the *Beitragsfreistellung* is taken from.

    ``"AFT_FREEZE"``
        l(t + 1).  **Numerically identical to** ``"AFT_DEATH"``, and deliberately so: the
        freeze moves policies between :func:`pols_paying` and :func:`pols_paidup` without
        removing any, so the total is unchanged.  The two timings exist so that the
        processing order is readable in the code and so that the equality is a statement
        the model makes rather than one a reader has to reconstruct.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "AFT_DEATH":
        return pols_if(t) * (1.0 - mort_rate_mth(t))
    if timing == "AFT_FREEZE":
        return pols_if_at(t, "AFT_DEATH")
    raise ValueError("invalid timing")


def pols_death_paying(t):
    """Expected deaths among premium-paying policies in month t: ``l^p(t) x q_mth(t)``.

    Split from :func:`pols_death_paidup` because the two cohorts release **different**
    reserves — :func:`db_pp` per policy against :func:`db_pu_pp` — and only the split
    figure can be multiplied by the right one.  Both reserves are annual amounts, struck at
    the end of the projection year, so the twelve months of a year release the same
    per-policy sum and the year's total is the annual-step model's.
    """
    return pols_paying(t) * mort_rate_mth(t)


def pols_death_paidup(t):
    """Expected deaths among premium-free policies in month t: ``l^f(t) x q_mth(t)``."""
    return pols_paidup(t) * mort_rate_mth(t)


def pols_death(t):
    """Expected deaths in projection month t, both cohorts.

    ``pols_death_paying(t) + pols_death_paidup(t)``, equivalently ``l(t) x q_mth(t)``.  In
    the *Aufschubphase* a death pays **nothing** in the base design — the reserve is
    released as a mortality profit, because the entitlement is *nicht vererblich* — and
    with the survivor rider on it pays only where an eligible survivor exists.  In the
    *Rentenphase* the annuity simply stops with that month's instalment, and each death
    contributes ``elig_surv_prob`` of a *Rentengarantiezeit* continuation where one is
    running.
    """
    return pols_death_paying(t) + pols_death_paidup(t)


def pols_freeze(t):
    """Policies going *beitragsfrei* at the end of projection month t.

    ``l^p(t) x (1 - q_mth(t)) x f(t)`` in the **last month of a projection year** and zero
    in the other eleven: the *Beitragsfreistellung* takes effect for the end of the current
    *Versicherungsperiode* (§ 165 with § 12 Abs. 1 VVG), and it is taken on the
    **survivors** of that month's death decrement, which is the processing order the notes
    set out **[std]**.  Zero in the *Rentenphase* and zero on a single-premium contract.

    Each frozen policy carries ``av_pp_at(k, "AFT_INT")`` of *Deckungskapital* with it from
    the paying block into the premium-free block, which is the term
    ``pols_freeze(12 k - 1) x av_pp_at(k - 1, "AFT_INT")`` in :func:`av_pu_at`: the freeze
    and the year's interest credit fall at the same instant, the end of the
    *Versicherungsjahr*.  Nothing leaves the fund, which is why :func:`check_av_roll_fwd`
    closes across a freeze.
    """
    if t < 0 or t >= ret_t() or t >= proj_len():
        return 0.0
    if not is_anniv(t):
        return 0.0
    return pols_paying(t) * (1.0 - mort_rate_mth(t)) * bf_rate(t)


def pols_gtd(t):
    """g(t): *Rentengarantiezeit* continuations running at the start of month t.

    The guarantee runs ``guarantee_period_y`` years **from *Rentenbeginn***, so every
    continuation ends on the same date::

        g(t) = 0                                   for t < max(0, ret_t()) or t > gtd_end_t()
        g(t) = g(t - 1) + pols_death(t - 1) x elig_surv_prob    inside the window

    On the monthly grid the window is ``12m`` **instalments** and a continuation starts in
    the month after the death that triggered it, rather than in the following year.

    ``elig_surv_prob`` is what makes this a Schicht-1 guarantee rather than a Schicht-3
    one: the instalments continue **only to a permitted survivor** — a spouse, a registered
    partner, or a child while *Kindergeld* runs — and where none exists the payments simply
    cease.  They are also **never commutable**: :func:`claims` pays ``ann_mth_pp(t) x g(t)``
    as a stream and nothing anywhere discounts a continuation into a capital sum.

    Monotone non-decreasing inside the window, and exactly zero outside it.  Zero at every
    ``t`` where ``guarantee_period_y = 0``, which is the base design and the anchor's
    setting.
    """
    if int(model_point()["guarantee_period_y"]) == 0:
        return 0.0
    start = max(0, ret_t())
    if t < start or t > gtd_end_t() or t > proj_len():
        return 0.0
    if t == start:
        return 0.0
    return pols_gtd(t - 1) + pols_death(t - 1) * elig_surv_prob      # noqa: F821


def decl_rate(k):
    """The declared *laufende Verzinsung* in projection year k, from *surplus_table.csv*.

    2,60 % for ``k = 0 ... 9``, 2,40 % for ``k = 10 ... 19``, 2,20 % thereafter in the
    ``base`` scenario **[std]**, clamped to the last row beyond the table.

    **It is the total credited rate, not a spread over the *Rechnungszins*.**  German
    declared rates are quoted that way, which is why :func:`cred_rate` is a maximum and not
    a sum.  A scenario rather than a forecast: no declared rate specific to a Basisrente
    was established anywhere in the delib corpus, and the path is set above the 1,00 %
    *Höchstrechnungszins* by a plausible surplus margin and graded down.
    """
    tab = data.surplus_table()                                       # noqa: F821
    key = model_point()["surplus_scenario_id"]
    tt = min(max(k, 0), int(tab.loc[key].index.max()))
    return float(tab.loc[(key, tt), "decl_rate"])


def cred_rate(k):
    """i(k): the rate credited to the *Deckungskapital* in projection year k.

    ``max(gtd_rate, decl_rate(k))`` — a **maximum**, not a sum.  ``gtd_rate`` is the
    contract's *Rechnungszins*, capped at the *Höchstrechnungszins* in force at conclusion
    and fixed for the whole term, so a book carries a stack of guarantee vintages and the
    ``max`` picks a different branch on each.  On the anchor (1,00 %) the declared path
    binds at every ``k``; on model point 8 (2,75 %, above the whole declared path) the
    guarantee binds at every ``k``.

    Stacking the declared rate on top of the guarantee is the sixth pitfall and is worth a
    great deal over a twenty-two-year deferment.  The reserve charge gamma is netted
    inside the same crediting step, in :func:`av_pp_at` and :func:`av_pu_at`.
    """
    return max(float(model_point()["gtd_rate"]), decl_rate(k))


def av_pp(k):
    """A^p(k): the *Deckungskapital* **per premium-paying policy** at the start of year k.

    ``av_pp_init`` at ``k = 0`` for a point that opens premium-paying, zero for one that
    opens *beitragsfrei* (whose whole reserve is in :func:`av_pu_at`), then
    ``av_pp_at(k - 1, "AFT_INT")``.

    Per **policy**, against :func:`av_pu_at`, which is the premium-free block at **fund**
    level.  The two diverge from the first freeze and must not be averaged into one
    per-policy figure: that is the third pitfall.  Zero from ``k = ret_y() + 1``, the fund
    having become an annuity obligation.
    """
    if k < 0 or k > ret_y() or k > proj_len_y():
        return 0.0
    if k == 0:
        if int(model_point()["paidup_at_init"]) == 1:
            return 0.0
        return float(model_point()["av_pp_init"])
    return av_pp_at(k - 1, "AFT_INT")


def av_pp_at(k, timing):
    """A^p(k, .): the *Deckungskapital* per premium-paying policy inside year k.

    ``"BEF_PREM"``
        :func:`av_pp`, the start of the year before the premium is taken.

    ``"AFT_PREM"``
        after the year's premium, *Zuzahlung* and all four charges:
        ``av_pp_at(k, "BEF_PREM") + prem_to_av_pp(k)``.

    ``"AFT_INT"``
        after interest, credited at the **end** of the year net of the reserve charge:
        ``av_pp_at(k, "AFT_PREM") x (1 + cred_rate(k) - gamma_av)``.  A policy that dies
        during the year has been credited a full year's interest, because deaths fall
        after crediting.

    All three are zero from ``k = ret_y()`` except ``"BEF_PREM"`` at ``k = ret_y()``
    itself, which is the fund the annuity is struck on.
    """
    if k < 0 or k >= proj_len_y():
        return 0.0
    if timing == "BEF_PREM":
        return av_pp(k)
    if k >= ret_y():
        if timing in ("AFT_PREM", "AFT_INT"):
            return 0.0
        raise ValueError("invalid timing")
    if timing == "AFT_PREM":
        return av_pp_at(k, "BEF_PREM") + prem_to_av_pp(k)
    if timing == "AFT_INT":
        gamma = float(data.charge_table().loc[                       # noqa: F821
            model_point()["tariff_id"], "gamma_av"])
        return av_pp_at(k, "AFT_PREM") * (1.0 + cred_rate(k) - gamma)
    raise ValueError("invalid timing")


def av_pu_at(k, timing):
    """A^f(k, .): the premium-free block's *Deckungskapital*, at **fund** level.

    Carried at fund level rather than per policy because a policy that froze at duration 5
    and one that froze at duration 15 hold different reserves and only the aggregate is
    meaningful.

    ``"BEF_PREM"``
        ``av_pp_init x pols_if_init()`` at ``k = 0`` for a model point that opens
        *beitragsfrei*, zero otherwise; then
        ``av_pu_at(k - 1, "AFT_INT") x (1 - q(k - 1)) + pols_freeze(12 k - 1) x
        av_pp_at(k - 1, "AFT_INT")`` — the survivors of the block, plus the reserves the
        year's freezes carried across from the paying block.

    ``"AFT_PREM"``
        ``av_pu_at(k, "BEF_PREM") - unit_cost_pp(k) x pols_paidup(12 k)``.  The block pays the
        *Stückkosten* and nothing else: no premium, so no beta and no *Zillmerung*
        instalment.  That asymmetry is the whole economic content of a
        *Beitragsfreistellung*.

    ``"AFT_INT"``
        as for the paying block, ``x (1 + cred_rate(k) - gamma_av)``.
    """
    if k < 0 or k >= proj_len_y():
        return 0.0
    if timing == "BEF_PREM":
        if k > ret_y():
            return 0.0
        if k == 0:
            if int(model_point()["paidup_at_init"]) == 1:
                return float(model_point()["av_pp_init"]) * pols_if_init()
            return 0.0
        return (av_pu_at(k - 1, "AFT_INT") * (1.0 - mort_rate(12 * (k - 1)))
                + pols_freeze(12 * k - 1) * av_pp_at(k - 1, "AFT_INT"))
    if k >= ret_y():
        if timing in ("AFT_PREM", "AFT_INT"):
            return 0.0
        raise ValueError("invalid timing")
    if timing == "AFT_PREM":
        return av_pu_at(k, "BEF_PREM") - unit_cost_pp(k) * pols_paidup(12 * k)
    if timing == "AFT_INT":
        gamma = float(data.charge_table().loc[                       # noqa: F821
            model_point()["tariff_id"], "gamma_av"])
        return av_pu_at(k, "AFT_PREM") * (1.0 + cred_rate(k) - gamma)
    raise ValueError("invalid timing")


def av_at(k, timing):
    """A(k, .): the whole *Deckungskapital* at fund level inside year k.

    ``av_pp_at(k, timing) x pols_paying(12 k) + av_pu_at(k, timing)``, with the **opening**
    paying count as the weight at every timing, because deaths fall after interest.

    This is the only one of the three account cells that rolls forward on mortality alone::

        av_at(k + 1, "BEF_PREM") = av_at(k, "AFT_INT") x (1 - mort_rate(12 k))

    and that identity — :func:`check_av_roll_fwd` — holds **whether or not** the survivor
    rider is on, because the reserve of a policy terminated by death leaves the fund either
    way: as a claim where an eligible survivor exists, as a mortality profit where none
    does.  It is the arithmetic content of *nicht vererblich*.  It also holds across a
    *Beitragsfreistellung*, because a freeze moves reserve between the two blocks without
    removing any.
    """
    return av_pp_at(k, timing) * pols_paying(12 * k) + av_pu_at(k, timing)


def av(k):
    """A(k): the *Deckungskapital* at the start of year k, fund level.

    ``av_at(k, "BEF_PREM")``.  A **state variable, reported and not summed** — the third
    column of :func:`result_cf` is a balance, not a cash flow, and adding it to anything
    is a category error.

    Zero for every ``k > ret_y()``.  At ``k = ret_y()`` itself it is the **pre-conversion
    fund**, which is the number the annuity is struck on and the one a reader following the
    worked example needs; :func:`fund_at_conv` grosses it up by the *Schlussüberschussanteil*
    and the account is empty from the next year onwards.
    """
    return av_at(k, "BEF_PREM")


def rentenfaktor_curr():
    """The insurer's *aktueller Rentenfaktor* at the conversion age.

    Read from *rentenfaktor_table.csv* at ``(rf_scenario_id, ret_age)``: euro of monthly
    annuity per 10 000 € of capital.  31,50 € at age 67 in the ``base`` scenario **[std]**;
    the ``low`` scenario runs about 12 % below it.

    Entirely **[std]**: no *Rentenfaktor* level, range or time series exists anywhere in
    the delib corpus, for this or any product.  It is the single largest lever in the
    model, because it converts the entire accumulated fund into the entire payout-phase
    liability.  Zero where the model point opens in the *Rentenphase* and no conversion
    occurs.
    """
    if ret_t() < 0:
        return 0.0
    return float(data.rentenfaktor_table().loc[                      # noqa: F821
        (model_point()["rf_scenario_id"], int(model_point()["ret_age"])), "rf_curr"])


def rf_option_factor():
    """The multiplicative reduction in the *Rentenfaktor* bought by the two options.

    ``factor("guarantee_period", guarantee_period_y) x factor("survivor",
    surv_annuity_rate)`` from *option_table.csv*: 1,000 for no *Rentengarantiezeit*, 0,995
    for ten years and 0,974 for twenty; 1,000 for no survivor's annuity and 0,930 for one
    at 60 % of the main annuity.  All **[std]**.

    A German tariff pays for both covers **out of the annuity** rather than by scaling the
    death benefit, which is why they appear here and not in :func:`claims`.  1,000 on the
    anchor cell, where both options are off.
    """
    tab = data.option_table()                                        # noqa: F821
    g = "%d" % int(model_point()["guarantee_period_y"])
    s = "%.2f" % float(model_point()["surv_annuity_rate"])
    return (float(tab.loc[("guarantee_period", g), "factor"])
            * float(tab.loc[("survivor", s), "factor"]))


def rentenfaktor_applied():
    """R: the *Rentenfaktor* actually applied at *Rentenbeginn*.

    ``max(rentenfaktor_gtd, rentenfaktor_curr()) x rf_option_factor()``.

    The ``max`` is the contract's own rule and it is a genuine discontinuity: the
    projection is sensitive to whichever factor is higher and completely insensitive to the
    other.  The anchor cell converts at the current 31,50 € against a guaranteed 28,00 €;
    model point 13 converts at its guaranteed 34,00 € against a ``low``-scenario current
    27,72 €, which is why that point exists.  Taking one when the other is higher is the
    thirteenth pitfall.  Monotone non-decreasing in both inputs.

    ``rentenfaktor_gtd`` was struck at inception on **first-order** DAV 2004 R with a
    prudential margin and a conservative interest basis; it is not, and must not be, the
    projection's own best-estimate basis.
    """
    return max(float(model_point()["rentenfaktor_gtd"]),
               rentenfaktor_curr()) * rf_option_factor()


def fund_at_conv():
    """F: the fund converted at *Rentenbeginn*, including the *Schlussüberschussanteil*.

    ``av_at(ret_y(), "BEF_PREM") x (1 + terminal_bonus_rate)``, at fund level: the balance
    carried out of the last accumulation year, struck at the start of projection year
    ``ret_y()`` — equivalently at the end of month ``ret_t() - 1`` — before any annuity is
    paid.

    The *Schlussüberschussanteil* is allocated at this **single date** and at no other,
    which is a contract fact rather than a standardization: the contract has no earlier
    exit — no surrender, no capital option — so there is no earlier trigger for a terminal
    bonus to attach to.  The 4,0 % level is **[std]** with nothing behind it.

    Zero for a model point that opens in the *Rentenphase*, where no conversion occurs
    inside the projection.
    """
    if ret_y() < 0:
        return 0.0
    sigma = float(data.charge_table().loc[                           # noqa: F821
        model_point()["tariff_id"], "terminal_bonus_rate"])
    return av_at(ret_y(), "BEF_PREM") * (1.0 + sigma)


def ann_bonus_rate(k):
    """b(k): the *Überschussrente* uplift applied at the end of payout year k.

    1,0 % p.a. compounding in the ``base`` scenario **[std]**, read from
    *surplus_table.csv*.  A *teildynamische Rente*: a *volldynamische* one would consume
    the whole first-order margin released in the payout phase and a *konstante* one none,
    and 1,0 % is deliberately in between.

    It is the mechanism that gives the conversion-basis wedge back to the annuitant — the
    fund is converted on first-order mortality and run off on the best estimate — so this
    lever and ``mort_be_factor`` between them decide the payout phase's whole economics.
    Both are **[std]** independently.
    """
    tab = data.surplus_table()                                       # noqa: F821
    key = model_point()["surplus_scenario_id"]
    tt = min(max(k, 0), int(tab.loc[key].index.max()))
    return float(tab.loc[(key, tt), "ann_bonus_rate"])


def ann_pp(k):
    """a(k): the **annual** annuity per surviving annuitant in projection year k.

    Zero before *Rentenbeginn*; at ``k = ret_y()`` the conversion::

        ann_pp(T) = fund_at_conv() / pols_if(ret_t()) / rf_unit
                    x rentenfaktor_applied() x ann_freq

    which is the **cohort-average** annual annuity per annuitant — exact at fund level even
    though the paying and premium-free cohorts arrive with different per-policy reserves —
    and thereafter ``ann_pp(k) = ann_pp(k - 1) x (1 + ann_bonus_rate(k - 1))``.

    ``pols_if(ret_t())`` is the count at the **first payout month**, which is the count at
    the start of payout year ``T``: the conversion is struck on the cohort that reaches
    *Rentenbeginn*.

    For a model point that opens in the *Rentenphase* (``ret_y() < 0``) the conversion
    never occurs inside the projection and ``ann_pp(0) = ann_pp_init``.

    This is an **annual** amount and is not what anybody is paid: ``ann_freq = 12`` because
    the *Rentenfaktor* is quoted in euro a **month**, and :func:`ann_mth_pp` is the
    instalment.  The annual figure is kept as the cells the conversion identity and the
    *Überschussrente* are stated on, because both are annual terms — the *Rentenfaktor* is
    applied once and the surplus uplift compounds once a year.
    """
    if k < 0 or k >= proj_len_y():
        return 0.0
    start = max(0, ret_y())
    if k < start:
        return 0.0
    if k == start:
        if ret_y() < 0:
            return float(model_point()["ann_pp_init"])
        if pols_if(max(0, ret_t())) <= 0.0:
            return 0.0
        return (fund_at_conv() / pols_if(max(0, ret_t())) / rf_unit  # noqa: F821
                * rentenfaktor_applied() * ann_freq)                 # noqa: F821
    return ann_pp(k - 1) * (1.0 + ann_bonus_rate(k - 1))


def ann_mth_pp(t):
    """The monthly *Rente* instalment per surviving annuitant in projection month t.

    ``ann_pp(proj_year(t)) / ann_freq``, paid **monthly in advance** from ``t = ret_t()``
    and zero before it.  This is the amount the contract actually promises: a *Rentenfaktor*
    is quoted as euro of monthly annuity per 10 000 € of capital, and a *Leibrente* is paid
    monthly.

    **This is what the monthly grid buys on this product.**  The annual-step model booked
    twelve instalments together at the start of the payout year on the opening in-force
    count, so a life that died in the first month of a payout year was paid the whole year;
    it named that as the twelfth pitfall and as a stated approximation of a monthly grid on
    an annual one, generous to the year of death by up to a full year's annuity and
    concentrated in the high-mortality tail.  Here the instalment is paid to whoever is
    alive at the start of **each month** and the approximation is gone.

    The uplift still steps once a year, on the payout anniversary, because the
    *Überschussrente* is declared annually: the twelve instalments of a payout year are
    equal and the thirteenth is ``(1 + ann_bonus_rate)`` times the twelfth.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    if t < max(0, ret_t()):
        return 0.0
    return ann_pp(proj_year(t)) / ann_freq                           # noqa: F821


def db_pp(k):
    """The *Deckungskapital* released per dying **premium-paying** policy in year k.

    ``av_pp_at(k, "AFT_INT")``: deaths fall after interest is credited, so the reserve
    released is the end-of-year one.  What is *paid* is this amount only where the survivor
    rider is on **and** an eligible survivor exists; otherwise the whole of it is a
    mortality profit and nothing is paid.  See :func:`claims`.
    """
    return av_pp_at(k, "AFT_INT")


def db_pu_pp(k):
    """The *Deckungskapital* released per dying **premium-free** policy in year k.

    ``av_pu_at(k, "AFT_INT") / pols_paidup(12 k)``: the premium-free block is carried at fund
    level, so the per-policy figure is an average over policies that froze at different
    durations.  That average is exact for this purpose — the deaths are a uniform share of
    the block — and it is the only per-policy figure the block admits.  Zero where the
    block is empty.
    """
    if pols_paidup(12 * k) <= 0.0:
        return 0.0
    return av_pu_at(k, "AFT_INT") / pols_paidup(12 * k)


def claims(t, kind=None):
    """Benefit outgo in projection month t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the *Deckungskapital* released by the month's deaths in the *Aufschubphase*,
        weighted by ``elig_surv_prob``.  The amount released per policy is the **annual**
        ``db_pp(k)`` — the reserve at the end of the *Versicherungsjahr*, which is where the
        account is struck — so the twelve months of a year release the same per-policy sum
        and the year's total is the annual-step model's to the last bit.  What the month
        decides is **when** it is released, not how much.

        **Structurally zero where ``surv_annuity_rate = 0``**, which is the base design and
        the anchor's setting: the entitlement is *nicht vererblich*, so a death before
        *Rentenbeginn* pays nothing and the reserve is released as a mortality profit.  Zero
        from ``t = ret_t()`` in every case.

        Where the rider is on this is **not a lump sum to a beneficiary**.  Everything paid
        to a survivor must be paid as an annuity, so what is booked is the reserve leaving
        this contract as the **single premium of a survivor's annuity** — a new liability,
        an immediate annuity, that this model does not project.

    ``"ANNUITY"``
        ``ann_mth_pp(t) x pols_if(t)``: one monthly instalment, in advance, to the lives in
        force at the start of the month.

    ``"SURVIVOR"``
        ``ann_mth_pp(t) x pols_gtd(t)``: the *Rentengarantiezeit* stream, payable only to a
        permitted survivor and **never commutable**.  Structurally zero where
        ``guarantee_period_y = 0``.

    There is no fourth kind, and there can be none: no surrender value, no capital option,
    no partial capital payment and no commutation exist on this product.
    :func:`check_no_capital` asserts that the total is exactly the sum of these three.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "ANNUITY", "SURVIVOR"))
    if kind == "DEATH":
        if float(model_point()["surv_annuity_rate"]) <= 0.0:
            return 0.0
        if t < 0 or t >= ret_t() or t >= proj_len():
            return 0.0
        k = proj_year(t)
        return elig_surv_prob * (                                    # noqa: F821
            db_pp(k) * pols_death_paying(t) + db_pu_pp(k) * pols_death_paidup(t))
    if kind == "ANNUITY":
        if t < max(0, ret_t()) or t >= proj_len():
            return 0.0
        return ann_mth_pp(t) * pols_if(t)
    if kind == "SURVIVOR":
        if t < 0 or t >= proj_len():
            return 0.0
        return ann_mth_pp(t) * pols_gtd(t)
    raise ValueError("invalid kind")


def expenses(t):
    """E(t): the insurer's own expense outgo in projection month t, fund level.

    Acquisition expense at inception (``t = 0`` and ``duration_init = 0`` only), then a
    **twelfth** of the annual maintenance expense per in-force policy in the
    *Aufschubphase* and a twelfth of the annual annuity administration per annuitant **and
    per *Rentengarantiezeit* continuation** in the *Rentenphase*, both inflating at
    ``expense_infl`` from the valuation date.  The payout phase is administratively cheaper
    than the accumulation phase, which is why the two rates differ.

    The inflation factor steps on the **anniversary**, ``(1 + expense_infl)^proj_year(t)``,
    because an expense assumption is quoted per policy per year; the twelve months of a
    projection year therefore carry the same monthly amount.  A policy that dies in the
    third month of a year now bears three twelfths of that year's maintenance rather than
    the whole of it, which is the second thing the finer grid changes on this product.

    **The commission is not in here.**  It is a separate line of the notes' cash flow
    statement and a separate column of :func:`result_cf`, and :func:`net_cf` subtracts each
    once.

    Nor are the *charges*: beta, gamma, the *Stückkosten* and the *Zillmerung* amortisation
    are deductions from the policyholder's account and hence insurer **income**.  This
    cells is therefore invariant to ``beta_prem``, ``gamma_av`` and ``zill_rate``, and
    those three move :func:`net_cf` only through the smaller annuity that a smaller fund
    buys at *Rentenbeginn*.  Booking a charge as an expense as well is the fourth pitfall.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    row = data.charge_table().loc[model_point()["tariff_id"]]        # noqa: F821
    infl = (1.0 + float(row["expense_infl"])) ** proj_year(t)
    out = 0.0
    if t == 0 and int(model_point()["duration_init"]) == 0:
        out += float(row["acq_expense_pp"]) * pols_if_init()
    if t < ret_t():
        out += float(row["maint_expense_pp"]) / 12.0 * infl * pols_if(t)
    else:
        out += (float(row["annuity_admin_pp"]) / 12.0 * infl
                * (pols_if(t) + pols_gtd(t)))
    return out


def commissions(t):
    """C(t): commission outgo in projection month t, fund level.

    ``comm_init_rate x beitragssumme_pp() x pols_if_init()`` at inception — the
    *Abschlussprovision*, sized to the *Zillmerung* cap, which is the German design in
    which what the insurer pays out is what it may write into the reserve — plus
    ``comm_renew_rate x (premiums(t) + zuzahlungen(t))`` from ``t = 1``, the
    *Bestandsprovision*.  Both **[std]**: the corpus's only datum is a 1 575 €
    *Abschlussprovision* on one specimen quotation, and it is [unverified].

    The renewal commission is a percentage of a contribution, so it falls in the month the
    contribution does and in no other — the ``t >= 1`` condition excludes the first year's
    premium at ``t = 0`` and admits every later one at ``t = 12, 24, ...``, which is
    exactly the annual-step model's rule.

    Paid **only** where the model point is new business (``duration_init = 0``): an
    in-force point's acquisition commission was paid before the valuation date and is not a
    projected cash flow.
    """
    if t < 0 or t >= proj_len():
        return 0.0
    row = data.charge_table().loc[model_point()["tariff_id"]]        # noqa: F821
    out = 0.0
    if t == 0 and int(model_point()["duration_init"]) == 0:
        out += float(row["comm_init_rate"]) * beitragssumme_pp() * pols_if_init()
    if t >= 1:
        out += float(row["comm_renew_rate"]) * (premiums(t) + zuzahlungen(t))
    return out


def net_cf(t):
    """The net liability cash flow of projection month t, **income positive**.

    ``premiums + zuzahlungen - claims_death - claims_annuity - claims_survivor - expenses
    - commissions``.  The library-wide sign; :func:`liability_cf` publishes the same stream
    outgo-positive.

    ``expenses`` here does **not** include the commission — the two are separate lines and
    each is subtracted once — and the *Deckungskapital* is a balance rather than a cash
    flow and enters nothing.  ``prem_total_pp`` enters nothing either: the BUZ premium buys
    a cover this model does not project.

    :func:`check_net_cf` reconstructs this from :func:`result_cf`'s own published columns,
    which is delib's first ruling — the headline number of a cash flow model must not be
    the one quantity nothing checks.
    """
    return (premiums(t) + zuzahlungen(t)
            - claims(t, "DEATH") - claims(t, "ANNUITY") - claims(t, "SURVIVOR")
            - expenses(t) - commissions(t))


def liability_cf(t):
    """The same stream as :func:`net_cf`, outgo positive: ``-net_cf(t)`` exactly.

    The orientation the technical notes print and the one a valuation layer consumes: a
    Solvency II best estimate is ``sum v(t) x liability_cf(t)`` over the relevant risk-free
    term structure, plus a risk margin.  Published as a column beside :func:`net_cf` so
    the sign convention is verifiable in the frame rather than only in prose.  This library
    discounts nothing and computes no reserve.
    """
    return -net_cf(t)


def check_net_cf_resid(t):
    """The cash flow statement's residual in projection month t; zero everywhere.

    Reconstructs ``net_cf(t)`` from :func:`result_cf`'s **own published columns** —

        ``premiums + zuzahlungen - claims_death - claims_annuity - claims_survivor
        - expenses - commissions - net_cf``

    — rather than from the cells that produced them, so a column added to the frame but not
    to :func:`net_cf`, a mis-signed column, or a column whose cells and frame entry have
    drifted apart all leave a residual here.  ``pols_if`` and ``pols_paying`` are counts and
    are excluded from the identity by construction; the *Deckungskapital* is a balance on an
    annual clock and is not a column of this frame at all.
    """
    row = result_cf().loc[t]
    return float(row["premiums"] + row["zuzahlungen"]
                 - row["claims_death"] - row["claims_annuity"] - row["claims_survivor"]
                 - row["expenses"] - row["commissions"] - row["net_cf"])


def check_net_cf():
    """True when the published cash flow statement reconciles in every projected month.

    **delib's first ruling**, required of every model in this library: the identity that
    reconstructs ``net_cf(t)`` from the statement's own parts, in code rather than in prose.
    :func:`check_net_cf_resid` gives the signed residual of the month that failed.

    The tolerance is ``roll_fwd_tol`` relative to the largest ``|net_cf|`` in the run, so
    it means the same thing on a 300 € contribution and on a 30 826 € one.
    """
    scale = max([1.0] + [abs(net_cf(t)) for t in range(proj_len())])
    return all(abs(check_net_cf_resid(t)) <= roll_fwd_tol * scale     # noqa: F821
               for t in range(proj_len()))


def check_pols_roll_fwd_resid(t):
    """The policy-ledger residual in projection month t; zero everywhere.

    A **non-negative** residual, because it closes two identities at once and a signed sum
    could let them cancel.  The first term says the two ledgers exhaust the in-force
    count; the second and third say the in-force count decrements on **mortality alone**,
    the last of them saying in code that the *Beitragsfreistellung* leaves the total
    untouched::

        |pols_paying(t) + pols_paidup(t) - pols_if(t)|
        |pols_if(t + 1) - pols_if_at(t, "AFT_FREEZE")|
        |pols_if_at(t, "AFT_FREEZE") - pols_if(t) x (1 - mort_rate_mth(t))|

    The second is the one to stare at: ``bf_rate`` does not appear in it.  A
    *Beitragsfreistellung* is a transfer between the ledgers and not an exit, so a model
    that subtracts it from :func:`pols_if` — the second pitfall — fails here, and so does a
    misindexed recursion that rolls forward with ``mort_rate_mth(t + 1)``.  It is the
    **monthly** rate throughout: a roll-forward that used the annual ``mort_rate(t)`` here
    would fail in the first month of the projection.
    """
    return (abs(pols_paying(t) + pols_paidup(t) - pols_if(t))
            + abs(pols_if(t + 1) - pols_if_at(t, "AFT_FREEZE"))
            + abs(pols_if_at(t, "AFT_FREEZE") - pols_if(t) * (1.0 - mort_rate_mth(t))))


def check_pols_roll_fwd():
    """True when both policy-ledger identities close in every projected month."""
    scale = max(pols_if_init(), 1.0)
    return all(check_pols_roll_fwd_resid(t) <= roll_fwd_tol * scale  # noqa: F821
               for t in range(proj_len()))


def check_av_roll_fwd_resid(k):
    """The *Deckungskapital* residual in projection **year** k; zero everywhere.

    The account is an annual construction — one premium, one set of charges and one
    interest credit per *Versicherungsjahr* — so its roll-forward is stated per year and
    this residual takes ``k``, not ``t``.  Before *Rentenbeginn*::

        av_at(k + 1, "BEF_PREM") - av_at(k, "AFT_INT") x (1 - mort_rate(12 k))

    the fund-level roll-forward on **mortality alone**, at the year's annual rate — which is
    exactly what the twelve monthly rates compound to, so the identity closes on the
    monthly grid with the annual arithmetic unchanged.  It holds across a
    *Beitragsfreistellung*, because a freeze moves reserve between the two blocks without
    removing any, and it holds whether or not the survivor rider is on, because the reserve
    of a policy terminated by death leaves the fund either way — as a claim where an
    eligible survivor exists, as a mortality profit where none does.  That is the
    arithmetic content of *nicht vererblich*.

    At ``k = ret_y()`` the residual is ``av_at(k, "AFT_INT")``: the conversion empties the
    account, so nothing is credited into it in the conversion year.  After it the residual
    adds ``av(k)`` as well, so a *Deckungskapital* surviving into the *Rentenphase* fails
    here.  A model that collapsed the paying and premium-free blocks into one average
    per-policy reserve fails at the first freeze.
    """
    if k < ret_y():
        return av_at(k + 1, "BEF_PREM") - av_at(k, "AFT_INT") * (1.0 - mort_rate(12 * k))
    if k == ret_y():
        return av_at(k, "AFT_INT")
    return av_at(k, "AFT_INT") + av(k)


def check_av_roll_fwd():
    """True when the *Deckungskapital* rolls forward and is emptied at *Rentenbeginn*."""
    return all(abs(check_av_roll_fwd_resid(k))
               <= roll_fwd_tol * max(1.0, abs(av_at(k, "AFT_INT")),   # noqa: F821
                                     abs(av(k)))
               for k in range(proj_len_y()))


def check_conversion_resid(k):
    """The conversion residual; zero at every k, and non-trivial only at ``ret_y()``.

    Inverts the conversion identity at ``T = ret_y()``::

        ann_pp(T) x pols_if(ret_t()) x rf_unit / (rentenfaktor_applied() x ann_freq)
        - fund_at_conv()

    so it catches a factor applied per policy instead of per fund, an ``ann_freq`` of 1
    where the annuity is monthly, and a ``rf_unit`` of 1 000 instead of 10 000.  Zero at
    every other ``k``, which is the second thing it asserts: the fund converts **exactly
    once**, at *Rentenbeginn*, and there is no second conversion, no partial commutation and
    no re-quotation.

    An **annual** residual, because the conversion is struck once on a balance the contract
    defines per *Versicherungsjahr*; the instalments it buys are monthly and are checked by
    :func:`check_annuity_roll_fwd`.

    Vacuously zero for a model point that opens in the *Rentenphase*, where the conversion
    happened before the valuation date.
    """
    if ret_y() < 0 or k != ret_y():
        return 0.0
    if rentenfaktor_applied() <= 0.0:
        return 0.0
    return (ann_pp(k) * pols_if(max(0, ret_t())) * rf_unit           # noqa: F821
            / (rentenfaktor_applied() * ann_freq)                    # noqa: F821
            - fund_at_conv())


def check_conversion():
    """True when the whole fund converts exactly once, at *Rentenbeginn*."""
    scale = max(1.0, abs(fund_at_conv()))
    return all(abs(check_conversion_resid(k)) <= roll_fwd_tol * scale  # noqa: F821
               for k in range(proj_len_y()))


def check_no_capital_resid(t):
    """The *nicht kapitalisierbar* residual in projection month t; zero everywhere.

    A **non-negative** residual with two limbs:

    * ``|claims(t, "DEATH")|`` wherever the survivor rider is off (``surv_annuity_rate =
      0``) or ``t >= ret_t()``.  A death before *Rentenbeginn* pays **nothing** in the base
      design, and after *Rentenbeginn* the annuity simply stops; paying anything there is
      the ninth pitfall.
    * ``|claims(t) - claims(t, "DEATH") - claims(t, "ANNUITY") - claims(t, "SURVIVOR")|``,
      which asserts that there is **no fourth kind of payment**.  No surrender value, no
      *Rückkaufswert*, no *Kapitalwahlrecht*, no *Teilkapitalauszahlung* and no commutation
      of a *Rentengarantiezeit* exist on this product, so the only things this model can
      pay are a monthly annuity instalment, a guarantee continuation and a survivor's single
      premium.  The *Kleinbetragsrenten-Abfindung* is absent too, but by standardization
      rather than by prohibition — Schicht 1 does permit it — so this residual records a
      property of **this implementation** and not of the statute.

    Stated per month, because it is a statement about payments and payments are monthly.

    The absence of a ``claims_lapse`` column, a ``cv_pp`` cells and a ``lapse_rate`` cells
    is asserted in the product's own test module, because it is an absence and cannot be
    computed here.
    """
    resid = abs(claims(t) - claims(t, "DEATH") - claims(t, "ANNUITY")
                - claims(t, "SURVIVOR"))
    if float(model_point()["surv_annuity_rate"]) <= 0.0 or t >= ret_t():
        resid += abs(claims(t, "DEATH"))
    return resid


def check_no_capital():
    """True when no payment other than a permitted annuity or survivor benefit is made."""
    scale = max([1.0] + [abs(claims(t)) for t in range(proj_len())])
    return all(check_no_capital_resid(t) <= roll_fwd_tol * scale      # noqa: F821
               for t in range(proj_len()))


def check_annuity_roll_fwd_resid(k):
    """The annuity and *Rentengarantiezeit* residual in projection year k; zero everywhere.

    A **non-negative** residual with four limbs, stated per year because the annuity is
    struck once and uplifted once a year while its instalments are monthly:

    * inside the payout phase, ``|ann_pp(k) - ann_pp(k - 1) x (1 + ann_bonus_rate(k - 1))|``
      — the *Überschussrente* compounds and nothing else touches the annuity once it is
      struck;
    * before it, ``|ann_pp(k)|`` and the year's ``|pols_gtd(t)|`` — nothing is in payment
      before *Rentenbeginn*;
    * ``|12 x ann_mth_pp(t) - ann_pp(k)|`` over the year's months — the twelve instalments
      of a payout year are equal and are exactly the annual amount, so the uplift steps on
      the anniversary and nowhere else;
    * after ``gtd_end_t()``, ``|pols_gtd(t)|`` — the *Rentengarantiezeit* runs from
      *Rentenbeginn*, not from each death, so every continuation ends on the same date, and
      on this grid that date is the end of the ``12m``-th instalment.
    """
    start = max(0, ret_y())
    resid = 0.0
    if k < start:
        resid += abs(ann_pp(k))
    elif k > start:
        resid += abs(ann_pp(k) - ann_pp(k - 1) * (1.0 + ann_bonus_rate(k - 1)))
    for t in range(12 * k, 12 * k + 12):
        if k < start or t > gtd_end_t():
            resid += abs(pols_gtd(t))
        if k >= start:
            resid += abs(ann_freq * ann_mth_pp(t) - ann_pp(k))       # noqa: F821
    return resid


def check_annuity_roll_fwd():
    """True when the annuity compounds and the guarantee window closes on time."""
    scale = max(1.0, abs(ann_pp(max(0, ret_y()))))
    return all(check_annuity_roll_fwd_resid(k) <= roll_fwd_tol * scale  # noqa: F821
               for k in range(proj_len_y()))


def result_cf():
    """Result table of cash flows, indexed by projection **month** t.

    ``pols_if`` is the start-of-month count and the weight applied to every cash flow on the
    same row; ``pols_paying`` is the premium-paying subset and the weight on the two premium
    columns, which are non-zero only in the first month of a projection year.  Columns 3 and
    4 enter ``net_cf`` positively and columns 5 to 9 negatively.  ``liability_cf`` is
    ``net_cf`` outgo-positive.

    The *Deckungskapital* is **not** a column here.  It is a balance on the annual clock —
    one premium, one set of charges and one interest credit per *Versicherungsjahr* — and it
    lives in :func:`result_pols` beside the rates and per-policy amounts that move with it.
    A balance in a monthly cash flow statement would invite exactly the summation that is a
    category error.

    ``claims_death`` is structurally zero wherever ``surv_annuity_rate = 0`` and
    ``claims_survivor`` wherever ``guarantee_period_y = 0``; both are published rather than
    dropped, because a column of zeros states the product fact where a missing column
    would only hide it.  There is **no ``claims_lapse`` column and no surrender column of
    any name**: the entitlement is *nicht kapitalisierbar*.

    The frame runs ``t = 0 ... proj_len() - 1`` and stops, so ``len(result_cf())`` is
    ``proj_len()``.  At ``t = proj_len() - 1`` the last survivor dies, and there is no tail
    state, no maturity payment and nothing left to pay.  :func:`result_cf_annual` is the
    same stream summed into projection years, which is the view the technical notes print.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_paying": [pols_paying(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "zuzahlungen": [zuzahlungen(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_annuity": [claims(t, "ANNUITY") for t in ts],
            "claims_survivor": [claims(t, "SURVIVOR") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into projection years, indexed by k.

    The seven cash flow columns are **summed** over the twelve months of each projection
    year and the two counts are taken at the year's **start**, which is what they are
    everywhere else in the model.  It is a regrouping of the monthly frame and not a second
    projection: no cells is evaluated on a different basis to produce it.

    Indexed by the projection year ``k`` rather than by the policy year, because everything
    annual in this model is keyed to the projection — the declared rate, the expense
    inflation and the *Überschussrente* all count from the valuation date — and because ``k``
    is the annual-step model's own ``t``, so ``result_cf_annual().loc[k]`` is that model's
    row ``k`` and the two can be read side by side.  ``policy_year`` is published as a
    column of :func:`result_pols` for a reader who needs the contractual label.

    The *Aufschubphase* rows reproduce the annual-step model's to the last bit on the
    premium, the *Zuzahlung* and the commission, which fall on the anniversary and are
    weighted by a count the finer grid does not change.  The annuity rows do not and are not
    meant to: the instalments are monthly now, and a life that dies during a payout year is
    no longer paid the whole of it.
    """
    ks = list(range(proj_len_y()))
    flows = ["premiums", "zuzahlungen", "claims_death", "claims_annuity",
             "claims_survivor", "expenses", "commissions", "net_cf", "liability_cf"]
    df = result_cf()
    out = {"pols_if": [pols_if(12 * k) for k in ks],
           "pols_paying": [pols_paying(12 * k) for k in ks]}
    for col in flows:
        out[col] = [float(df[col].iloc[12 * k:12 * k + 12].sum()) for k in ks]
    return pd.DataFrame(out, index=pd.Index(ks, name="k"))           # noqa: F821


def result_pols():
    """Result table of the annual state, indexed by projection year k.

    The companion to :func:`result_cf`, and the model's **annual** view: the two policy
    ledgers at the start of the year and the transfers between them, the decrement and
    crediting rates the year is run on, the per-policy premium and *Zuzahlung*, the
    *Deckungskapital* of the premium-paying cohort and of the fund, and the annual annuity
    with the monthly instalment it is paid in.

    Every rate here is the **annual** one: ``mort_rate`` is the year's death rate and
    ``mort_rate_mth`` the twelfth the recursion applies, and the two are printed together
    because confusing them is the easiest way to break a monthly model of an annual product.
    ``pols_death`` and ``pols_freeze`` are the year's **totals** — the deaths summed over its
    twelve months, the freezes falling in its last — so the columns reconcile with the
    ledgers beside them.

    ``policy_year`` is the contractual 1-based label, which is ``k + 1`` only for a model
    point projected from issue.
    """
    ks = list(range(proj_len_y()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "policy_year": [duration_y(k) + 1 for k in ks],
            "age": [age_y(k) for k in ks],
            "pols_if": [pols_if(12 * k) for k in ks],
            "pols_paidup": [pols_paidup(12 * k) for k in ks],
            "pols_death": [sum(pols_death(t) for t in range(12 * k, 12 * k + 12))
                           for k in ks],
            "pols_freeze": [sum(pols_freeze(t) for t in range(12 * k, 12 * k + 12))
                            for k in ks],
            "pols_gtd": [pols_gtd(12 * k) for k in ks],
            "mort_rate": [mort_rate(12 * k) for k in ks],
            "mort_rate_mth": [mort_rate_mth(12 * k) for k in ks],
            "bf_rate": [bf_rate(12 * k) for k in ks],
            "cred_rate": [cred_rate(k) for k in ks],
            "prem_pp": [prem_pp(k) for k in ks],
            "zuz_pp": [zuz_pp(k) for k in ks],
            "prem_to_av_pp": [prem_to_av_pp(k) for k in ks],
            "av_pp": [av_pp(k) for k in ks],
            "av": [av(k) for k in ks],
            "ann_pp": [ann_pp(k) for k in ks],
            "ann_mth_pp": [ann_mth_pp(12 * k) for k in ks],
        },
        index=pd.Index(ks, name="k"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

mort_be_factor = 0.85

elig_surv_prob = 0.55

mort_base_year = 2005

zill_spread_y = 5

rf_unit = 10000.0

ann_freq = 12

roll_fwd_tol = 1e-9

pd = ("Module", "pandas")
