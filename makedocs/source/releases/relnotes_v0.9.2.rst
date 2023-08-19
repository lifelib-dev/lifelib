.. currentmodule:: lifelib.libraries

.. _relnotes_v0.9.2:

==================================
lifelib v0.9.2 (19 August 2023)
==================================

In this release, modelx models in the following libraries have been updated
so that they can now be exported as standalone Python packages
by the new export feature introduced in modelx version 0.22.0.

- basiclife
- savings
- assets
- economic
- smithwilson (project)

All the modelx models from the libraries listed above, including their example models,
can now be transformed to Python packages.
These transformed models are independent of modelx,
and they run significantly faster and consume less memory than their original counterparts.
For further insights into the export feature, refer to the following articles.

.. seealso::

    * `New Feature: Export Models as Self-contained Python Packages <https://modelx.io/blog/2023/07/29/export-feature-intro>`_
    * `Enhanced Speed for Exported lifelib Models <https://modelx.io/blog/2023/08/19/enhanced-speed-for-exported-lifelib-models>`_


To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


Fixes and Updates
===================

* Auto-coercion (implicit conversion) of parameterless Cells objects to their
  values is deprecated in modelx 0.23.0.
  All modelx models across all the lifelib libraries are updated to eliminate the
  implicit conversion (See `commit 5b7357f <https://github.com/lifelib-dev/lifelib/commit/5b7357f82aa0bcc075c9c59f8780180c6b1d2de4>`_).

* CashValue_ME_EX4 and its example notebook are updated to make
  some formulas more effective and concise,
  in response to a contributor's suggestion (`GH57 <https://github.com/lifelib-dev/lifelib/pull/57>`_).

* Models are updated to eliminate deprecated usage of Pandas.

* Fix an error in ifrs17a.

Changes
===================

* Starting with this release, lifelib no longer supports Python 3.6,
  given that this version reached its end of life over a year ago.
  While lifelib may still function with Python 3.6,
  lifelib won't be tested against this version anymore.


