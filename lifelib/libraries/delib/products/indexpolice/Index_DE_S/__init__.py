# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the German *Indexpolice*.

:mod:`~.Index_DE_S` is the executable counterpart of
``products/indexpolice/technical-notes.md`` in the lifelib-products library. It projects
gross best-estimate liability cash flows, undiscounted, for a single-policy model point
of an *indexgebundene Rentenversicherung* — the deferred private annuity whose capital
sits in the insurer's *Sicherungsvermögen* under a guarantee and whose annually declared
*Überschuss* is not credited as interest but **spent as an option budget** buying one
year of index participation — on a **monthly** grid, from inception (or from the
valuation date of an in-force point) to *Rentenbeginn*.

Four things make this the *Indexpolice* model rather than a re-labelled unit-linked one.

**The capital is in the general account and cannot fall from the index.** There is no
*Anlagestock*, no unit price and no fund value anywhere in this model. The policyholder
holds a claim measured in euros, the *Deckungskapital* rolls forward by a recursion, and
a bad *Indexjahr* credits zero rather than taking anything away. Reading the contract as
unit-linked is the first listed modeling pitfall, and it is the single most common
misunderstanding of the product.

**The payoff is a sum of capped monthly returns, floored once at the year.** Each month's
return is capped above at ``C`` and **not floored below**; the twelve are **summed, not
compounded**; and the sum alone is floored at zero. The asymmetry is the whole product:
truncating every right tail while leaving every left tail intact means a year in which
the index *rose* can credit **nothing**. The shipped index path reproduces the research
file's two constructed *Indexjahre* at ``k = 8`` and ``k = 9`` (policy years 9 and 10) —
Example A credits 8.90 % of the base, and Example B credits zero on a year whose
compounded index return was +6.4402 %.

**One budget, two arms, and the policyholder elects between them each year.** The
declared surplus rate is either spent on options (``opt_budget_pp``) or credited as
interest (``surplus_credit_pp``), never both and never neither:
``check_surplus_alloc()`` asserts that identity at every ``t``. The annual *Wahlrecht* is
a **behavioural** assumption, carried as an election path ``w(t)`` in an external table.

**Whatever is credited is locked in.** A credit, once made, is permanently part of the
guaranteed capital, enters the base of every later *Indexjahr*, and can never be lost —
the *Höchststandsicherung*. What ratchets is the **ledger of credits**, not the account
balance: with the reserve charge at or above the guaranteed rate the balance itself falls
in a year that credits nothing, which is why ``check_lock_in()`` asserts monotone
``guar_cap_pp`` and non-negative credits and says nothing about ``av_pp``.

**Spaces.** The model contains two:

:mod:`~.Index_DE_S.Data`
    Reads the eight input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Index_DE_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its ``data``
    Reference, which resolves to the single :mod:`~.Index_DE_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Monthly steps over an annual contract, so the model runs on **two
clocks** and the argument of a cells says which. ``t`` counts **policy months** from issue
and is 0-based; ``duration(t) = t // 12`` is the 0-based policy year ``k``,
``policy_year(t) = duration(t) + 1`` the contractual label, and
``proj_len() = 12 x proj_len_y()`` the exclusive end of the frame, with
``proj_len_y() = ann_start_age - entry_age``. A new-business point starts at ``t = 0``, an
in-force point at ``t = 12 x dur_init``.

**Everything that makes this product what it is stays annual and takes ``k``**, because the
contract is annual: the *Indexjahr* is twelve months, the surplus is declared once a year,
the *Wahlrecht* is exercised once a year and the credit is struck once a year, at its end,
to the **survivors only**. The premium falls at the start of the policy year — the
*Versicherungsperiode* of this tariff — and the account, the ledger and the guaranteed
capital roll once a year. The in force, the two decrements, the claims and the expenses take
``t``, so a death or a surrender now falls in the month it happens and is paid the policy
year's own amount.

What the finer grid earns here is the *Indexjahr* itself: its twelve monthly returns were
always the mechanic but lived inside a single cells, and ``index_month(t)``,
``index_return_mth(t)`` and ``index_return_capped_mth(t)`` now put them on the frame, one
row each, so *capped above and not floored below* can be read month by month. It also dates
the forfeiture — a surrender in month 7 of an *Indexjahr* loses that year's credit, and the
incentive to surrender just after a year closes rather than just before is now in the
projection instead of only in the prose.

The decrements carry the library's two speeds — ``mort_rate(t)`` and ``lapse_rate(t)`` are
the **annual** rates of the policy year, ``mort_rate_mth`` and ``lapse_rate_mth`` the
geometric twelfths the recursion applies — so the annual layer is **bit-identical** to the
annual-step model this replaced on all thirteen model points: the account, every
*Indexgutschrift*, the *Höchststandsicherung* ledger, the guaranteed capital, the surrender
value and premium income are unchanged. What moved is the split of a year's exits between
death and surrender, and the expenses a mid-year leaver bears.

**What is sourced and what is not, stated without softening.** The *mechanics* are firm
and are cited to the statutes that govern them: the index participation is a form of
*Überschussverwendung* under § 153 VVG with no independent statutory footing, the capital
is in the *Sicherungsvermögen*, the guarantee falls due at *Rentenbeginn* in the *Neue
Klassik* architecture, the *Rückkaufswert* is a reserve floored by the five-year
acquisition-cost spread of § 169 Abs. 3 VVG, and the *Stornoabzug* must be agreed,
quantified and appropriate. **No level is sourced at all.** Direct HTTP egress was blocked
in the build environment and the session's search budget was exhausted before this product
was researched, so no Cap, no *Partizipationsquote*, no declared surplus rate, no charge,
no lapse rate and no commercial-envelope parameter was established for any German carrier.
Every such number here is **[std]** with a stated rationale, and the DAV tables (DAV 2008 T,
DAV 2004 R) are proprietary, are cited by name and are never shipped. **This model is a
mechanics demonstration, not a pricing or reserving result.** Replace the decrement,
charge and index tables with company data before drawing any conclusion from the output.

**Model points.** Thirteen, covering both premium forms, all four payment frequencies,
both payoff designs, all three index paths, all four election paths, both *Kapitalwahlrecht*
elections, both *Stornoabzug* settings, two in-force points, four *Rechnungszins* cohorts
and four *Garantieniveaus*. Model point 1 is the anchor cell of the worked example in the
technical notes; model point 8 is an in-force cell whose first projected *Indexjahr* is
``k = 8``, so it reproduces the research file's Examples A and B on a 50,000.00 EUR base.

**Verification.** ``tests/test_indexpolice_de.py`` asserts the notes' twenty-seven-year
worked example to the cent off ``result_cf_annual()`` and ``pols_if`` to six decimals, the
twelve months of an *Indexjahr* on the monthly frame beside it, and one test per listed
modeling pitfall. Six ``check_*()`` cells travel with the model and are called on every
model point by the library's conventions suite: ``check_net_cf`` and
``check_pols_roll_fwd`` monthly, and ``check_av_roll_fwd``, ``check_surplus_alloc``,
``check_lock_in`` and ``check_index_credit`` per policy **year**, because the constructions
they check are annual.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/indexpolice/Index_DE_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Index_DE_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
