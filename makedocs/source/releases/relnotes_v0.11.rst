.. currentmodule:: lifelib.libraries

==================================
lifelib v0.11 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.11.0:

lifelib v0.11.0 (1 Feb 2024)
==================================

New Model
----------------

This release adds a new model, :mod:`~basiclife.BasicTerm_SC` in :mod:`~basiclife`.
The :mod:`~basiclife.BasicTerm_SC` model is a variant of :mod:`~basiclife.BasicTerm_S` that
is optimized for generating a compiled model using Cython with modelx-cython.
See :mod:`~basiclife.BasicTerm_SC` for more details.

