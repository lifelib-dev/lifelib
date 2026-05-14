.. currentmodule:: lifelib.libraries

.. _relnotes_v0.9.3:

==================================
lifelib v0.9.3 (2 December 2023)
==================================

In this release, modelx models in the following projects have been updated
in response to the backward incompatible changes introduced in modelx v0.24.0.

- ifrs17sim
- nestedlife
- simplelife(*scripts/simplelife.py*)
- solvency2(*scripts/solvency2.py*)

Models that are based on previous versions off projects need to be updated
manually so that each child space in the base spaces in the models are inherited explicitly.

.. seealso::

    * `modelx v0.24.0 Release Notes <https://docs.modelx.io/en/latest/releases/relnotes_v0_24_0.html>`_


To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


Fixes
===================

*  Remove constant coercion in ifrs17sim.



