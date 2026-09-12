# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French *rente viagère immédiate*.

:mod:`~.Rente_FR_S` is the executable counterpart of
``products/rente_viagere/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single French immediate life
annuity in payment: the *arrérages* to the annuitant, the *prorata d'arrérages* settled
on death, the *réversion* stream, the *frais d'arrérages* the insurer retains out of
each *quittance*, and maintenance expense.

**Mortality is the model.** After conversion the contract has no premiums, no surrender
value at any duration, no account value and no policyholder option of any kind. The only
decrements are deaths. There is **no lapse machinery anywhere in this model** and that is
a cited product feature, not an omission.

The UK counterpart in the same library is :mod:`.PA_UK_S` and the US one
:mod:`.SPIA_US_S`; the three share the payout chassis, so ``lives_if``, ``lives_death``,
``certain_floor``, ``payment_factor``, ``payment_surv_mth``, ``cum_annuity_pp``,
``annuity_pp``, ``annuity_payments``, ``pols_if`` and ``liability_cf`` mean the same
thing on all three and can be laid side by side. Where France parts company:

* the mortality basis is a **generational** table keyed on ``(sex, birth_year, age)``, so
  there is no improvement scale and no calendar-year argument — the trend is inside the
  table, and an ``improve_factor`` on top of it would double-count;
* the tariff is **unisex by law** and struck on the more prudent table for every life,
  while the best estimate is sex-dependent, so the two are separate objects and the gap
  between them is the surplus the eight-year profit-sharing rule sends back;
* **revalorisation** is a discretionary annual uplift credited at 31 December, pro-rated
  in the first partial calendar year and floored at zero — a calendar event, never a
  policy anniversary;
* the *frais d'arrérages* are retained out of **every** payment, including the
  *prorata* settled on death, which is why they are a cash flow rather than a pricing
  loading; and
* the month of death is **paid in full**: the accrued arrears go to the heirs.

**Spaces.** The model contains two:

:mod:`~.Rente_FR_S.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.Rente_FR_S.Projection`
    The by-contract projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.Rente_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every contract, and the generational mortality table is the
largest input in this library. In ``Data`` they are evaluated once, however many
contracts are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so the
model and its inputs must travel together.

**Projection basis.** Monthly steps from the effective date, which is always the 1st day
of a civil month. The month index ``t`` is **0-based**: ``t = 0`` is the first projected
month — the first whole civil month of service — and the frame is
``t = 0, 1, …, proj_len() - 1``, so ``proj_len()`` is the number of months projected and
``policy_year(t) = t // 12 + 1``. The model therefore carries the **calendar** — the
effective year and civil month — and not merely the duration, because revalorisation and
expense inflation step at 31 December while the *paliers* and the attained ages step on
12-month multiples of the effective date. Age is **age last birthday**; the *millésime* (year of birth) is a
separate model point attribute and is never derived from the projection year. The
limiting age is 120, the published top age of the tables, and the projection runs to the
last month of age 119 of the **youngest** covered life, ``t = proj_len() - 1`` — stopping
on the annuitant's age alone would truncate a younger reversionary's tail.

**What is sourced and what is not.** The contractual mechanics are sourced: the
instalment formula and its *terme échu* timing, the rule that the arrérage of the month
of death is due in full, the reversion at a stated percentage of the *rente atteinte*
starting the month after death, the definitive reversion coefficient and its published
age-difference table, the *annuités garanties* as an annuity-certain floor and their
exclusivity with the reversion, the four *paliers* schemes, the 31 December
revalorisation date with its first-year pro-rating and its zero floor, the *frais
d'arrérages* per *quittance*, the *frais sur encours de rentes* biting on the provision
rather than on the instalment, the absence of any surrender value, and the statutory
commutation threshold. Every **rate** is a standardization. TGH05/TGF05 are annexed to
the Code des assurances and are not redistributable here, so the mortality basis shipped
with the model is a **[std]** INSEE-shaped generational proxy, anchored so that the
tariff annuity factor reproduces the notes' placeholder *taux de rente* exactly; no
French insurer publishes an annuity rate card.
**This model is a mechanics demonstration, not a pricing or reserving result.**
Replace the basis with a licensed same-schema file before drawing any conclusion from the
output.

**Verification.** ``tests/test_rente_viagere_fr.py`` asserts the notes' worked example
row by row to the cent, including the 1.125% pro-rated first uplift reaching the month-9
instalment, the whole instalment settled as a *prorata* on the month-25 death, and the
reversion starting at 60% of the *rente atteinte* in month 26.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/rente_viagere/Rente_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "Rente_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
