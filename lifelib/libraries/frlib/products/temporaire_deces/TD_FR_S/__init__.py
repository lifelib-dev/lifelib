# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for the French assurance temporaire décès.

:mod:`~.TD_FR_S` is the executable counterpart of
``products/temporaire_deces/technical-notes.md`` in the lifelib-products library. It
projects gross best-estimate liability cash flows for a single-policy model point of a
French standalone term death cover — *capital décès* on death from any cause, with
*perte totale et irréversible d'autonomie* (PTIA) accelerating the same capital — on a
**monthly** grid, with **no tail state of any kind**: cover ceases at the *échéance*
following ``cover_end_age``, nothing is payable there, and there is no maturity value,
no renewal option and no conversion.

Two things make this the French model rather than a translated UK one.

**The cotisation rises with attained age.** The default premium form is
``revisable``: the cotisation is recomputed at *every* annual renewal from the tariff
rate at the new *différence de millésime* age, so ``prem_pp(t)`` moves every year and
runs from 1 575,00 € to 7 290,00 € over the worked configuration's seventeen years — a
factor of 4,6286, which is exactly the ratio of the two grid rates and does not depend
on the capital. The level alternative, ``constante``, is carried as a model point column
and is derived by actuarial equivalence on tariff survivorship; it is a standardization,
not a French market form. Reading a French term policy as level-premium is the first
listed modeling pitfall, and the two forms are the largest structural lever in the model.

**There is no cash value anywhere.** Art. L. 132-23 of the Code des assurances forbids
both *rachat* and *réduction* on a temporaire décès, so the model has no account value,
no surrender cells and no paid-up state, and ``claims_lapse(t)`` is structurally zero at
every ``t``. That is a statutory fact about the product, not a modeling simplification,
and the zero column is published rather than dropped so that the fact is stated instead
of inferred.

**PTIA is an acceleration, not an addition.** A life that leaves through the PTIA
decrement is gone from ``pols_if`` and can never generate a death claim; the two rates
are *dependent* rates in one two-decrement table and are therefore additive. PTIA cover
also stops earlier than death cover, at ``ptia_end_age``, as a hard gate on the attained
age rather than a taper. ``check_decrement_closure()`` and ``check_ptia_gate()`` assert
both, on every model point.

**Spaces.** The model contains two:

:mod:`~.TD_FR_S.Data`
    Reads the six input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.TD_FR_S.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1. It reaches the input tables through its
    ``data`` Reference, which resolves to the single :mod:`~.TD_FR_S.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized,
every ``Projection[N]`` is a separate ItemSpace with its own cells cache; readers
placed there would re-read every file for every policy. In ``Data`` they are evaluated
once, however many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run
time rather than stored inside the model. The model folder itself holds no data, so
the model and its inputs must travel together.

**Projection basis.** Monthly steps, on lifelib's 0-based time index — the clock
``basiclife/BasicTerm_S`` and the rest of this library's monthly models run on. ``t = 0``
is the first policy month and the frame runs ``t = 0, 1, ..., proj_len() - 1``, where
``proj_len() = 12 * (cover_end_age() - issue_age())`` is the number of policy months
projected (204 on the worked configuration). A monthly grid is not a monthly product:
everything *contractual* here is annual — the one-year risk renewed by *tacite
reconduction* and repriced at each renewal, the benefit schedule, the art. L. 132-7
suicide year, the first-year commission rate, the ``constante`` equivalence — and the
model keeps all of it on the anniversary. So the policy year is derived and used as a
lookup key: ``duration(t) = t // 12`` is the completed policy years,
``policy_year(t) = duration(t) + 1`` the contractual 1-based label, and the attained age
is ``issue_age() + duration(t)``, stepping at the anniversary. The cotisation instalment,
maintenance expense and commission fall at the beginning of the month; death and PTIA
claims and their claim expense at the end of the month of claim; lapses at the end, on the
survivors of both insured decrements. Acquisition expense and the initial commission rate
fall at issue.

Decrements follow suit in two speeds. ``mort_rate(t)``, ``ptia_rate(t)`` and
``lapse_rate(t)`` are the **annual** rates of the policy year containing month ``t`` — the
vectors the technical notes tabulate — and ``mort_rate_mth(t)``, ``ptia_rate_mth(t)`` and
``lapse_rate_mth(t)`` are the monthly rates actually applied, at ``1 - (1 - r)^(1/12)``.
The death and PTIA rates are dependent rates of one two-decrement table and are therefore
**additive**, so it is their *sum* that is converted to the month and split back in their
own proportion; converting each apart would miss the annual decrement factor by 2.6e-6 in
the first year alone.

Because those monthly rates compound back to the annual ones, the in-force **at every
policy anniversary** is exactly what an annual-step model would carry, and so is every
annual contractual quantity — the tariff rate, the cotisation, the capital and the level
premium. The cash flows are not, and are not meant to be: claims fall at the end of the
month of claim, maintenance expense accrues a twelfth a month on the in-force of that
month, and a fractionated cotisation is collected on the mode's own cycle, on a block that
has already lost lives. That is what the finer grid is for. ``result_cf_annual()`` sums
the frame into policy years so the two can be read side by side.

**What a sibling may inherit.** This is the protection chassis behind ``ADE_FR_S``
(``products/assurance_emprunteur/``) and ``Obseques_FR_S`` (``products/obseques/``). The
names those models should take from here are ``prem_rate`` / ``prem_pp`` for the attained-age tariff and
the cotisation it produces, ``mort_rate`` / ``ptia_rate`` / ``lapse_rate`` for the three
annual decrements, ``pols_death`` / ``pols_ptia`` / ``pols_lapse`` for the exits they
produce, ``benefit_pp`` for the contractual capital and ``benefit_death_pp`` /
``benefit_ptia_pp`` for what is actually payable once the exclusions bite,
``suicide_factor`` for the art. L. 132-7 first-year void, and ``claims(t, kind)`` with
``"DEATH"`` / ``"PTIA"`` / ``"LAPSE"``. All three run the same monthly grid and the same
``duration_mth`` / ``duration`` / ``policy_year`` vocabulary, so ``mort_rate_mth`` /
``ptia_rate_mth`` / ``lapse_rate_mth`` and ``prem_inst_pp`` carry over too. What they must
*not* inherit is the benefit shape: ``TD_FR_S``'s capital is level and freely chosen,
while an ADE capital follows the outstanding loan balance and an obsèques capital is a
small fixed sum with a lifetime horizon behind a twelve-month *carence*.

**What is sourced and what is not.** The contractual mechanics are sourced: the
attained-age revision rule and the published rate grid, PTIA as an acceleration whose
payment ends the contract, PTIA cessation before death cessation, premium cessation on
death and on PTIA, the first-year suicide void, the absence of any surrender or
reduced-paid-up value, and the fractionation loadings with their *frais d'échéance*.
Every behavioural and experience assumption is a standardization: no French insurer
publishes a mortality table, a PTIA incidence rate, an expense loading, a commission
scale or a lapse rate for this product, and the homologated TH 00-02 / TF 00-02 tables
are annexed to an *arrêté* and are cited by name rather than redistributed here.
**This model is a mechanics demonstration, not a pricing or reserving result.** Replace
the decrement and expense tables with company data before drawing any conclusion from
the output.

**Model points.** Twelve, covering both premium forms with the level cotisation derived
and given, all four fractionation frequencies, a *surprime*, the accidental-capital
option, a PTIA cover running to the death-cover limit, a cell whose PTIA cover never
attaches at all, a *délai d'attente* with return of cotisations, a thirty-five-year run
from age 30, and a capital small enough that the acquisition expense decides whether the
cell is viable. Model point 1 is the anchor cell of the worked example in the technical
notes.

**Verification.** ``tests/test_temporaire_deces_fr.py`` asserts the twelve months of the
notes' first policy year and every row of their seventeen-year worked example, restated on
``result_cf_annual()``, to the cent and ``pols_if`` to six decimals; the level premium
3 914,3891 € and the annuity-due factor behind it, both unmoved by the conversion; that
twelve monthly rates compound back to exactly the annual ones; that the in-force at every
anniversary is what the annual recursion gives; and one test per listed modeling pitfall.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/temporaire_deces/TD_FR_S")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "TD_FR_S"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
