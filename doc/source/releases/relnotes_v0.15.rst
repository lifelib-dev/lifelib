.. currentmodule:: lifelib.libraries

==================================
lifelib v0.15 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.15.0:

lifelib v0.15.0 (22 August 2026)
==================================

New Library
----------------

This release adds a new library, :mod:`~uklib`.
:mod:`~uklib` packages seven reference liability cash flow projection
models for the individual life insurance products sold in the United
Kingdom, plus the pension annuity, and, for each model, the product
specification and technical notes it was built from.
See the :mod:`~uklib` page for more details.

The four protection models are ``Term_UK_A`` (guaranteed-premium term
assurance), ``CI_UK_S`` (critical illness cover), ``IP_UK_S`` (income
protection) and ``WOL_UK_S`` (whole of life). The two savings models
are ``WP_UK_A`` (with-profits) and ``ULB_UK_S`` (unit-linked investment
bond), and ``PA_UK_S`` is the pension annuity. The grid letters follow
the same convention as :mod:`~uslib`: ``_A`` marks an annual projection
step and ``_S`` a monthly one, and all seven models project one model
point at a time.

The pension annuity is in the library because annuities are the
dominant liability of UK life insurers and the centrepiece of the
Solvency UK matching adjustment. The coverage otherwise differs in kind
from :mod:`~uslib`'s, because the UK retail deferred annuity market is
negligible, while the pension annuity bought with a pension pot is the
product that matters.

:mod:`~uklib` is shaped exactly like :mod:`~uslib`. Each model projects
one product's gross liability cash flows, such as premiums, claims,
surrenders, expenses and commission, on the product's own processing
order and timing. None of the models discounts, so discounting,
reserving and capital are left to a layer that consumes the cash flows.
Every model has the same two Spaces: ``Data``, which reads the input
files, and ``Projection``, which is parameterized by ``point_id``. The
inputs are CSV files kept outside the model folder so that they can be
edited or swapped in place.

Beside each model sit the documents it was built from:
``product-spec.md``, a representative product specification composed
from publicly available documentation of real products;
``technical-notes.md``, the liability cash flow model on paper, with
state variables, recursions, processing order and a numeric worked
example; ``model.md``, how the model implements those notes; and
``sources.md``, every source cited. The tests ship inside the library
and run against your own copy: each model reproduces the worked example
in its technical notes, and ``tests/test_model_conventions_uk.py``
asserts the shared model structure and Cells names across all seven
models.

.. warning::

   :mod:`~uklib` is in its draft stage, and its contents are subject to
   change as development continues.

.. warning::

   The :mod:`~uklib` models are mechanics demonstrations, not pricing or
   reserving results. The contractual elements are sourced, but every
   decrement basis shipped with the library is a standardization
   introduced for the reference implementation, because the CMI tables
   that a UK insurer would actually use are restricted to Authorised
   Users and cannot be redistributed. Nor is there any public premium
   rate card, because UK protection and annuity pricing is quote-driven.
   Replace both with company data before drawing any conclusion from the
   numbers.

Changes
------------

* The documents and docstrings in :mod:`~uslib` are updated. Product
  sources are now cited by source tag in the published documents, with
  the source details kept in ``sources.md``. Specification citations of
  the form ``[S1]`` are now plain bracketed text rather than links,
  which is the citation convention :mod:`~uklib` also follows. None of
  the :mod:`~uslib` models behaves differently.
