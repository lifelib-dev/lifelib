.. currentmodule:: lifelib.libraries

.. _relnotes_v0.9.1:

==================================
lifelib v0.9.1 (8 July 2023)
==================================

This release adds a new notebook, :doc:`/libraries/ifrs17a/template_example2` in
the :mod:`~ifrs17a` library, and fixes some bugs.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


Updates in :mod:`~ifrs17a`
===========================

* A new notebook, :doc:`/libraries/ifrs17a/template_example2` is added.
* A new column, *PnlType* is added to the *AocType* table in *Dimension.xlsx*
* ``IfrsDatabase.Query`` now optionally takes a boolean parameter `as_df` to indicate
  whether to return the query result as a DataFrame.
* Fixed multiplier in *ImportScopeCalculation.py*.

.. seealso::

    * `Systemorph's video on IFRS17 Profit and loss statement  <https://www.youtube.com/watch?v=Ud2jX3J1eNU>`_





