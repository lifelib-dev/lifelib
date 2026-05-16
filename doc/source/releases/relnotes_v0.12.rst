.. currentmodule:: lifelib.libraries

==================================
lifelib v0.12 Releases
==================================

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


.. _relnotes_v0.12.0:

lifelib v0.12.0 (17 May 2026)
==================================

New Library
----------------

This release adds a new library, :mod:`~annuallife`.
:mod:`~annuallife` includes the :mod:`~annuallife.TradLife_A` model,
a traditional life insurance projection model that works on an annual basis.
See the :mod:`~annuallife` page for more details.

Changes
------------

* lifelib projects have been migrated into the ``lifelib/libraries``
  directory structure, unifying projects and libraries
  (`GH92 <https://github.com/lifelib-dev/lifelib/pull/92>`_).

* :mod:`~simplelife` and its dependent projects are now deprecated.
  Deprecation notices are added to the affected models.

* Python 3.14 is added to the supported Python versions, and
  Python 3.7 and 3.8 are no longer supported.

Fixes
------------

* Compatibility fixes for pandas 3.0, including ``select_dtypes``
  string-dtype handling and chained-assignment ``fillna`` calls in
  :mod:`~ifrs17a` Importers.

* ``draw_charts`` and ``draw_waterfall`` are fixed to reflect a
  modelx implementation change.

* The Pandas4Warning raised by ``select_dtypes`` for string columns
  is now silenced.
