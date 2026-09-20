.. currentmodule:: lifelib.libraries

==================================
lifelib v0.17 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.17.1:

lifelib v0.17.1 (21 September 2026)
====================================

New Library
----------------

This release adds a new library, :mod:`~krlib`.
:mod:`~krlib` packages ten reference liability cash flow projection
models for the individual life, health and annuity products sold in
Korea, and, for each model, the product specification and technical
notes it was built from. See the :mod:`~krlib` page for more details.
The library is in its draft stage.

The three protection models are ``WholeLife_KR_S`` (jongsin boheom,
whole life), ``Term_KR_S`` (jeonggi boheom, term) and ``CI_KR_S``
(critical illness). The four third-sector models are ``Medical_KR_S``
(silson uiryo boheom, fourth-generation indemnity medical),
``Cancer_KR_S`` (am boheom), ``LTC_KR_S`` (ganbyeong boheom, long-term
care) and ``Child_KR_S`` (eorini boheom, child cover). The three
savings and annuity models are ``Pension_KR_S`` (yeongeum jeochuk
boheom, the tax-qualified deferred contract), ``VA_KR_S`` (byeonaek
yeongeum boheom, variable annuity) and ``Immediate_KR_S`` (jeuksi
yeongeum, the single-premium immediate annuity). All ten run on the
same 0-based monthly projection step as the other reference libraries
and project one model point at a time.

What separates the coverage from :mod:`~uslib`'s, :mod:`~uklib`'s,
:mod:`~jplib`'s and :mod:`~frlib`'s is that the regulator wrote more of
the product than the carrier did, while the quantitative basis is the
least public of any market covered so far. Je-sam boheom, third
insurance, is not a market label but a statutory licence category that
either a life insurer or a non-life insurer may hold, and four of the
ten products sit in it. Silson uiryo boheom is the sharpest case: it is
held on 35.96 million individual contracts against a population near 51
million, its benefit definition is the supervisor's own standard policy
wording, and it is the only indemnity contract anywhere in lifelib.
Every other product, in every library, pays a stated sum; this one
reimburses an incurred cost inside an annual limit. Eorini boheom, a
bundled child health policy commonly written before birth, has no
counterpart in any sibling library either.

Against that, the industry experience table the models would want,
the gyeongheom saengmyeongpyo, is not published at all, so every
mortality and morbidity input in the library is a documented
construction that reports its own basis and its gap against the public
life table. Korea also uses two age conventions, boheom nai, the
contractual insurance age, and man nai, age last birthday, and the
library uses both because its sources do. Which one a model is on is
recorded in the library's test registry and asserted against the
model's own docstring, because a man nai model point read against a
boheom nai rate table understates the rate by roughly half a year of
ageing. Group business, retirement pensions and the non-life carrier's
form of each third-sector product are out of scope.

Changes
------------

* The repository now carries a ``.gitattributes`` that checks every
  text file out with LF line endings on all platforms. The reference
  libraries keep their model inputs as external CSV files that the
  in-library test suites read as bytes, and on Windows the default
  ``core.autocrlf`` setting rewrote those files on checkout, so a test
  that asserts an input carries no byte order mark and no CRLF failed
  on Windows alone against files that are LF in the repository.

* The test suite that exports every model with ``Model.export`` and
  checks the exported package against the model it came from now
  covers :mod:`~krlib`'s ten models as well, bringing it to 47 models.
  ``Pension_KR_S`` joins ``EC_FR_S`` in the set whose whole-table sweep
  is skipped on Windows up to Python 3.10, where an exported package
  inherits modelx's raised recursion limit but not the thread stack it
  evaluates on.

.. _relnotes_v0.17.0:

lifelib v0.17.0 (13 September 2026)
====================================

New Library
----------------

This release adds a new library, :mod:`~frlib`.
:mod:`~frlib` packages nine reference liability cash flow projection
models for the individual life insurance products sold in France, and,
for each model, the product specification and technical notes it was
built from. See the :mod:`~frlib` page for more details.

The three savings models are ``Euro_FR_S`` (assurance vie on the
guaranteed fonds en euros), ``UC_FR_S`` (unit-linked assurance vie)
and ``EC_FR_S`` (eurocroissance). The two retirement models are
``PER_FR_S`` (the loi PACTE retirement plan) and ``Rente_FR_S`` (the
immediate life annuity it pays into). The four protection models are
``TD_FR_S`` (temporaire deces, individual term life), ``ADE_FR_S``
(assurance emprunteur, creditor insurance), ``Obseques_FR_S`` (funeral
cover) and ``Dep_FR_S`` (dependance, long-term care). The grid letters
follow the same convention as the other reference libraries, and all
nine models run on a monthly projection step and project one model
point at a time.

What separates the coverage from :mod:`~uslib`'s, :mod:`~uklib`'s and
:mod:`~jplib`'s is that the savings side dominates. Assurance vie is
France's savings vehicle rather than one product among several, so
three of the nine slots go to it and its eurocroissance hybrid, a
fourth to the PER that the loi PACTE built on the same chassis, and a
fifth to the rente viagere they pay out into. The split between the
two supports is the first fact about any French life balance sheet:
the insurer carries the investment risk on the fonds en euros, where
the effet cliquet makes each year's credited return permanent, and
guarantees only the number of units on the unites de compte. On the
protection side, assurance emprunteur, the cover a French borrower
buys with a mortgage, is the largest individual protection market in
the country and has no counterpart in either sibling library. Group
business, epargne salariale and Luxembourg contracts are out of scope.

Three mechanisms in the library have no analogue anywhere else in
lifelib. The euro fund carries its provision pour participation aux
benefices as a per-vintage ledger, so the eight-year statutory release
clock is a real deadline on each year's allocation rather than an
average over all of them. Eurocroissance splits the account between a
provision mathematique accumulating at the taux technique toward a
guarantee that bites only at the echeance and a provision de
diversification carrying the upside in parts, so a surrender before
term pays the current part value with no guarantee at all. And the
creditor insurance model projects the amortising loan it covers,
paying the outstanding balance times the insured share on death and
total disability while the incapacity benefit pays the instalment
after a waiting period, under age limits that differ by guarantee, so
cover can end before the loan does.

:mod:`~frlib` is shaped exactly like its three siblings. Each model
projects one product's gross liability cash flows, such as premiums,
claims, surrenders, expenses and charges, on the product's own
processing order and timing. None of the models discounts, so
discounting, the technical provisions and capital are left to a layer
that consumes the cash flows. Every model has the same two Spaces:
``Data``, which reads the input files, and ``Projection``, which is
parameterized by ``point_id``. The inputs are CSV files kept outside
the model folder so that they can be edited or swapped in place.

Beside each model sit the documents it was built from:
``product-spec.md``, a representative product specification composed
from publicly available documentation of real products;
``technical-notes.md``, the liability cash flow model on paper, with
state variables, recursions, processing order and a numeric worked
example; ``model.md``, how the model implements those notes; and
``sources.md``, every source cited. The tests ship inside the library
and run against your own copy: each model reproduces the worked
example in its technical notes, and
``tests/test_model_conventions_fr.py`` asserts the shared model
structure and Cells names across all nine models.

.. warning::

   :mod:`~frlib` is in its draft stage, and its contents are subject to
   change as development continues.

.. warning::

   The :mod:`~frlib` models are mechanics demonstrations, not pricing or
   reserving results. The contractual side is sourced unusually well,
   because French contract law and the Code des assurances are
   published in full, so the participation aux benefices machinery,
   the eurocroissance provisions and the loi Lemoine substitution
   rights are taken from the instruments themselves rather than from
   commentary. Every decrement basis shipped here, on the other hand,
   is a standardization. The mortality tables a French insurer must
   use are annexed to an arrete and are cited by name throughout, but
   this library does not redistribute them; experience tables
   certified by an actuary are by construction not public; and there
   is no published rate card at all, because French pricing is
   quote-driven and the encadre a contract must carry discloses charge
   maxima rather than levels. Replace both with company data before
   drawing any conclusion from the numbers.

Changes
------------

* The models in :mod:`~uslib`, :mod:`~uklib` and :mod:`~jplib` now run
  on a 0-based time index, so ``t = 0`` is the first projection step
  rather than the point before it, and the last eight models that
  stepped annually are converted to a monthly grid. With :mod:`~frlib`
  arriving on the same convention, all 37 models in the four reference
  libraries now share one grid.

  Because the grid letter is part of the model name, the eight
  converted models are renamed with it: ``Term_US_A``,
  ``WholeLife_US_A``, ``Term_UK_A``, ``WP_UK_A``, ``Term_JP_A``,
  ``WholeLife_JP_A``, ``Endowment_JP_A`` and ``Annuity_JP_A`` become
  ``Term_US_S``, ``WholeLife_US_S``, ``Term_UK_S``, ``WP_UK_S``,
  ``Term_JP_S``, ``WholeLife_JP_S``, ``Endowment_JP_S`` and
  ``Annuity_JP_S``. The release notes for v0.14, v0.15 and v0.16 keep
  the old names, because they record what those releases shipped.

  A monthly grid is not the same thing as a monthly product. Where a
  product's contractual drivers are annual, the models keep those
  events on the policy anniversary and derive the policy year from
  ``t``. What the finer grid resolves is everything that is not a
  contractual event: decrements falling in the month they happen,
  account values accruing month by month so a mid-term exit is valued
  on the balance it actually has, and expenses and premium instalments
  falling where they are incurred.

* The :doc:`/libraries/index` page is grouped into three titled
  categories, Generic Liability Models, Reference Liability Models and
  Miscellaneous Models, each with its own introduction and table, and
  the sidebar menu shows the same separators. The past libraries are
  now listed in a table in the same format as the rest of the page.

* The test suite in the repository that exports every model with
  ``Model.export`` and checks the exported package against the model it
  came from now dispatches on what each published statement actually
  is, instead of assuming every one returns a DataFrame, and asserts
  that the model and the export return the same type before comparing
  values. ``PER_FR_S.result_settlement`` returns a Series and is the
  only one of the 102 statements across all 37 models that does.
