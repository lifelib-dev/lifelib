# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the klassische aufgeschobene private Rentenversicherung.

:mod:`~.RV_DE_S` is the executable counterpart of
``products/klassische_rentenversicherung/technical-notes.md`` in the lifelib-products
library. It projects gross best-estimate liability cash flows, undiscounted, for a
single-policy model point of the German Schicht-3 deferred annuity written on the general
account — premiums accumulate in the *Deckungskapital* at the contract's own
*Rechnungszins* with a declared *Überschussbeteiligung* beside it, and at the
*Rentenbeginn* the accumulated capital converts at a *Rentenfaktor* into a lifelong
monthly *Leibrente* or is taken as a lump sum under the *Kapitalwahlrecht*. The grid is
**monthly** and the contract is mostly not: the *Rechnungszins* is credited per
*Versicherungsjahr*, the surplus is declared per calendar year, and both *Kündigung* and
*Beitragsfreistellung* take effect "for the end of the current insurance period", so those
constructions take a policy year ``k`` while the in force, the decrements, the claims and
the *Rente* itself take a month ``t``. The **annuity is the reason the grid is monthly**:
the *Rentenfaktor* is quoted in euro a month and the *Rentengarantiezeit* guarantees monthly
instalments, and an annual grid could only pay a year of them at once.

Four things make this the German deferred-annuity model rather than a translated
endowment.

**The declared rate contains the guarantee; it does not sit on top of it.** The *laufende
Verzinsung* is the *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung*, so
``bonus_rate(k) = max(0, decl_rate(k) - int_rate_guar())`` and the two credits together
deliver the declared rate and never more. On the anchor cell that is 1,00 % guaranteed
plus 1,55 % surplus against a 2,55 % declaration. On model point 6, a 2,75 % legacy
vintage against the same declaration, ``bonus_rate`` is **zero in every policy year** while interest
is still credited at 2,75 % — a real German result and the first listed modeling pitfall,
not an artefact. ``check_av_roll_fwd()`` and ``check_av_sur_roll_fwd()`` keep the two
accounts honest about which credit went where.

**The *Rechnungszins* is a model-point attribute, not a global assumption.** A German life
book is a layered stack of guarantee vintages: the rate a contract was written on stays
with it for its whole life, so points 1, 6 and 14 credit 1,00 %, 2,75 % and 0,90 % in the
same run, from the same tables. Anything that reads a single interest rate off the model
has misunderstood the product.

**The conversion is an option the insurer wrote.** At the *Rentenbeginn* the applied
*Rentenfaktor* is ``max(garantierter, aktueller)`` — the factor fixed at inception against
the one the carrier is applying to immediate annuities at that date — and the higher of
the two is then guaranteed for the whole payment period. On the anchor cell the current
factor wins at 32,00 € against a guaranteed 28,00 €; on point 13 the guarantee binds over
a *low* scenario. A model applying the guaranteed factor alone understates the anchor's
annuity by 12,5 %. ``check_annuity_conv()`` asserts the rule and the guaranteed-contract-
value floor beside it.

**The *Rentengarantiezeit* is paid to the dead.** Inside the guarantee window the
instalment is due whether or not the annuitant is alive, so the annuity is weighted by the
**annuitised** count and not by survivors: ``pols_annuity(t) = max(pols_if(t),
1{12n <= t < 12n + 12m} pols_annuitization(12n - 1))``, asserted by
``check_annuity_guarantee()`` on every model point. On a monthly grid the window is what it
says it is — ``12m`` guaranteed **instalments**.

**Spaces.** The model contains two:

:mod:`~.RV_DE_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.RV_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.RV_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: plain CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data — no
``_data/``, no IOSpec, no embedded values — so the model and its inputs must travel
together. This follows ``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``,
which keeps its inputs inside the model.

**Projection basis.** Monthly steps over an annual product, so the model runs on **two
clocks** and the argument of a cells says which. ``t`` counts **policy months** from
inception and is **0-based**; ``duration(t) = t // 12`` is the 0-based policy year ``k``,
``policy_year(t) = duration(t) + 1`` the contractual 1-based label, and both the attained age
and the calendar year step on the **anniversary** — ``age(t) = issue_age + duration(t)``,
``calendar_year(t) = issue_year + duration(t)`` — which is what lets one generational
mortality surface and one declared-rate path serve a book of mixed vintages. A new-business
point opens at ``t = 0``; an in-force point that has run ``duration_init`` complete policy
years opens at ``t = t_start() = 12 duration_init`` carrying its balances on the model point.
``proj_len() = 12 x proj_len_y()`` with ``proj_len_y() = omega_age() - issue_age`` is the
**exclusive** end of the frame, so a life annuity is projected to exhaustion rather than
truncated at a fixed horizon — on the anchor cell, ``t = 0 ... 851``. The *Rentenbeginn* falls
at the end of the deferment period of ``n = aufschub_y`` years: accumulation months are
``t < 12n``, payout months ``t >= 12n``, the *Kapitalabfindung* is paid in month ``12n - 1``
and the first annuity instalment in month ``12n``.

The decrements carry the library's two speeds — ``mort_rate(t)`` and ``lapse_rate(t)`` are
the **annual** rates of the policy year, ``mort_rate_mth`` and ``lapse_rate_mth`` the
geometric twelfths the recursion applies — so the whole annual layer is **bit-identical** to
the annual-step model this replaced, on all fourteen model points: every account balance,
the § 169 floor, the surrender value, the conversion capital and the premium income are
unchanged. What the finer grid changed is the annuity, which is now paid monthly in advance;
the split of exits between death and surrender, which now compete month by month; and the
expenses, which a mid-year leaver now bears only for the months it was there.

**What is sourced and what is not.** The contractual mechanics are sourced: the
*Deckungskapital* as the premium net of risk and expense cover accumulated at the
*Rechnungszins*; the *Höchstzillmersatz* of 25 ‰ from 2015 and 40 ‰ before; the § 169
Abs. 3 surrender floor that spreads acquisition costs over five years; the § 169 Abs. 5
*Stornoabzug* conditions; the § 165 paid-up rule and its minimum-benefit branch; the three
death-benefit designs; the conversion rule and the ``max(guaranteed, current)``
*Rentenfaktor*; the *Bewertungsreserven* crystallisation at the transition to annuity
payment; and the *Rentengarantiezeit*. **Every level is a standardization.** No
*Rentenfaktor*, no declared surplus rate, no charge parameter, no expense and no
behavioural rate was established for this product at any German carrier for any year, and
the DAV tables (DAV 2004 R here) are the property of the Deutsche Aktuarvereinigung, are
not public and are cited by name rather than redistributed. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the decrement, charge and rate
tables with company data before drawing any conclusion from the output.

**Model points.** Fourteen, covering both premium forms, all four payment frequencies, two
in-force cells on two legacy guarantee vintages, both charge sets, all three death-benefit
forms with and without the surplus account, all three payout systems, five
*Rentengarantiezeit* durations including zero, *Kapitalwahlrecht* take-ups of 0 %, 20 %,
30 % and 100 %, the *Dynamik*, both statutory *Beitragsfreistellung* branches, and the
boundary cases: the paid-up conversion that fails the *Mindestversicherungsleistung* and
is cashed out (8), full commutation at *Rentenbeginn* (9), and the guaranteed
*Rentenfaktor* binding over a lower current one together with a binding
``guar_capital_pp`` (13). Model point 1 is the anchor cell of the worked example in the
technical notes.

**Verification.** ``tests/test_klassische_rentenversicherung_de.py`` asserts the notes'
worked example to the cent off ``result_cf_annual()`` and ``pols_if`` to six decimals, the
months of the first policy year on the monthly frame beside it, and one test per listed
modeling pitfall. Nine ``check_*`` identities travel with the model itself and are called
on every model point by ``tests/test_model_conventions_de.py``; six of them are monthly and
three — the two account roll-forwards and the premium split — are stated per policy **year**,
because the accounts they check are.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/klassische_rentenversicherung/RV_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "RV_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
