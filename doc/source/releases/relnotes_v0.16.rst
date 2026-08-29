.. currentmodule:: lifelib.libraries

==================================
lifelib v0.16 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.16.0:

lifelib v0.16.0 (29 August 2026)
==================================

New Library
----------------

This release adds a new library, :mod:`~jplib`.
:mod:`~jplib` packages nine reference liability cash flow projection
models for the individual life insurance products sold in Japan, and,
for each model, the product specification and technical notes it was
built from. See the :mod:`~jplib` page for more details.

The two protection models are ``Term_JP_A`` (level term life) and
``IncomeTerm_JP_S`` (survivor income term). The three savings models
are ``WholeLife_JP_A`` (whole life), ``Endowment_JP_A`` (endowment)
and ``FXWholeLife_JP_S`` (foreign-currency whole life), and
``Annuity_JP_A`` is the individual annuity. The three third-sector
models are ``Medical_JP_S`` (medical), ``Cancer_JP_S`` (cancer) and
``LTC_JP_S`` (nursing care). The grid letters follow the same
convention as :mod:`~uslib` and :mod:`~uklib`: ``_A`` marks an annual
projection step and ``_S`` a monthly one, and all nine models project
one model point at a time.

What separates the coverage from :mod:`~uslib`'s and :mod:`~uklib`'s
is the third sector (dai-san bunya). Medical, cancer and nursing care
are what Japanese households buy most by policy count, and none of the
three is priced off a sum assured. Medical is frequency times severity
times limit: a daily hospitalization amount, a per-hospitalization day
cap and a lifetime day cap, with the limits carrying the product.
Cancer keeps the frequency and the severity, drops the day limit
entirely, and adds a waiting period, a repeating diagnosis lump sum
and a reduced tier for carcinoma in situ. Nursing care is neither,
being a three-state model, healthy, in care and dead, whose trigger is
the grading made by the public long-term care scheme rather than a
carrier's own benefit definition.

Two of the nine also have no analogue in either sibling library. The
endowment's premium waiver runs on the death of the policyholder, a
decrement on a life who is not the insured; and the foreign-currency
whole life is the only model in any of the three libraries projected
in a currency other than its home one, carrying a declared crediting
rate over a guaranteed floor and a market value adjustment on
surrender.

:mod:`~jplib` is shaped exactly like :mod:`~uslib` and :mod:`~uklib`.
Each model projects one product's gross liability cash flows, such as
premiums, claims, surrenders, expenses and commission, on the
product's own processing order and timing. None of the models
discounts, so discounting, the current estimate, the margin over
current estimate and required capital are left to a layer that
consumes the cash flows. Every model has the same two Spaces:
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
``tests/test_model_conventions_jp.py`` asserts the shared model
structure and Cells names across all nine models.

.. warning::

   :mod:`~jplib` is in its draft stage, and its contents are subject to
   change as development continues.

.. warning::

   The :mod:`~jplib` models are mechanics demonstrations, not pricing or
   reserving results. More is sourced here than in either sibling
   library, because Japanese carriers publish premium rate cards and
   the statutory mortality tables are public, and that makes it more
   important, not less, to say what is still standardized: every
   best-estimate decrement basis, every expense and commission level,
   and every behavioural assumption. A published premium is a real
   premium, but the basis this library projects it on is not the basis
   it was priced on. Replace both with company data before drawing any
   conclusion from the numbers.

Changes
------------

* The test suites shipped in :mod:`~uslib` and :mod:`~uklib` are
  updated. They no longer re-project the same model points on a second
  modelx instance to check the input files are read once, so a suite
  run costs one sweep per model instead of two. None of the models in
  either library behaves differently.

* A new test suite in the repository exports every model in
  :mod:`~uslib`, :mod:`~uklib` and :mod:`~jplib` with
  ``Model.export``, and checks that the exported package imports and
  reproduces the model it came from. Running the exported models
  requires a modelx newer than 0.32.0, which fixes a defect in the
  exporter that left names unqualified after a generator expression.
