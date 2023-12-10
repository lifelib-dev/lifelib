.. currentmodule:: lifelib.libraries

.. _relnotes_v0.1.1:

===============================
lifelib v0.1.1 (23 July 2021)
===============================

This release introduces the following changes.
To update lifelib, execute the command::

    >>> pip install lifelib --upgrade

.. rubric:: Projects renamed to Libraries

lifelib *projects* are now called *libraries*.

.. rubric:: Introduction of the basiclife library

This release introduces a new cashflow library, :mod:`basiclife`.

Prior to this release,
:mod:`simplelife` was the base cashflow library,
and :mod:`fastlife` was the faster reimplementation of :mod:`simplelife`.
More complex models in other advanced libraries such
as :mod:`nestedlife`, :mod:`ifrs17sim` and :mod:`solvency2`
are based on :mod:`simplelife` for their base cashflow models.
However, :mod:`simplelife` was not ideal for the base cashflow library
because:

- The model includes multiple spaces, which makes it hard for novice users to understand the model.
- The method of calculating premiums and cash values used in the model
  is based on the commutation functions and is not common in many regions.
- The model is an annual step model, but monthly step models are more common in actual practices.

The :mod:`basiclife` library contains a new cashflow model :mod:`~basiclife.BasicTerm_S`,
and also its reimplementation :mod:`~basiclife.BasicTerm_M`,
which produces the same results as :mod:`~basiclife.BasicTerm_S` significantly faster.
The :mod:`basiclife` will be the new base cashflow library
for future new libraries,
although all the libraries existing prior to this release continue
to be available.
The new cashflow models in :mod:`basiclife` are monthly-step models
and much simpler than the models in :mod:`simplelife` and :mod:`fastlife`.
See the :mod:`basiclife` page for more details.
The :doc:`/quickstart/index` page is also updated
to use :mod:`basiclife` as the sample library instead of :mod:`simplelife`.

Special thanks to Lewis Fogden (https://digitalactuary.co.uk/).
The :mod:`~basiclife.BasicTerm_S` is modified from a model and samples
contributed by him.


lifelib v0.1.0 is discarded due to packaging error.
