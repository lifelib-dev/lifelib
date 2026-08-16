.. currentmodule:: lifelib.libraries

==================================
lifelib v0.14 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.14.0:

lifelib v0.14.0 (17 August 2026)
==================================

New Library
----------------

This release adds a new library, :mod:`~uslib`.
:mod:`~uslib` packages twelve reference liability cash flow projection
models for the individual life insurance and annuity products sold in
the United States, and, for each model, the product specification and
technical notes it was built from.
See the :mod:`~uslib` page for more details.

The six life models are ``Term_US_A`` (level premium term),
``WholeLife_US_A`` (participating whole life), ``UL_US_S`` (universal
life), ``IUL_US_S`` (indexed UL), ``VUL_US_S`` (variable UL) and
``ULSG_US_S`` (guaranteed UL). The six annuity models are ``MYGA_US_S``
(fixed deferred), ``FIA_US_S`` (fixed indexed), ``VA_US_S`` (variable),
``RILA_US_S`` (registered index-linked), ``SPIA_US_S`` (immediate) and
``DIA_US_S`` (deferred income). The grid letters follow lifelib's own
model names: ``_A`` marks an annual projection step, as in
:mod:`~annuallife.TradLife_A`, and ``_S`` a monthly one, as in
:mod:`~basiclife.BasicTerm_S`. ``S`` also carries its other lifelib
sense, scalar rather than vectorized, and all twelve models project
one model point at a time.

Each model projects one product's gross liability cash flows, such as
premiums, claims, surrenders, withdrawals, expenses and commissions,
on the product's own processing order and timing. None of the models
discounts, so discounting, reserving and capital are left to a layer
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
and run against your own copy: each model reproduces the worked example
in its technical notes, and ``tests/test_model_conventions.py`` asserts
the shared model structure and Cells names across all twelve models.

.. warning::

   :mod:`~uslib` is in its draft stage, and its contents are subject to
   change as development continues.

.. warning::

   The :mod:`~uslib` models are mechanics demonstrations, not pricing or
   reserving results. The contractual elements are sourced, but most
   behavioural and expense assumptions are standardizations introduced
   for the reference implementation, because no public source carries
   them, and current non-guaranteed scales, such as declared crediting
   rates, current cost of insurance and indexed UL caps, are not public
   at all. Replace them with company data before drawing any conclusion
   from the numbers.

Changes
------------

* lifelib now requires ``modelx`` v0.32.0 or newer, because the
  :mod:`~uslib` models are saved in the modelx serializer version 8
  format introduced in modelx v0.32.0. Earlier versions of ``modelx``
  cannot read them. The requirement is declared in both ``setup.py``
  and ``pyproject.toml``.

* Markdown files are now packaged with lifelib, so the documents that
  accompany the :mod:`~uslib` models are installed with lifelib and
  copied into your project by ``lifelib.create``.
