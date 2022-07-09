.. currentmodule:: lifelib.libraries

.. _relnotes_v0.5.0:

================================
lifelib v0.5.0 (9 July 2022)
================================

This release adds a new model,
:mod:`~basiclife.BasicTermASL_ME` in the :mod:`~basiclife` library.

To update lifelib, run the following command::

    >>> pip install lifelib --upgrade

If you're using Anaconda, use the ``conda`` command instead::

    >>> conda update lifelib


New Model
===============

:mod:`~basiclife.BasicTermASL_ME`
is an adjustable step length(ASL) model, and projects the cashflows of
in-force policies at time 0 and future new business
policies issued after time 0.

Unlike :mod:`~basiclife.BasicTerm_ME`, with :mod:`~basiclife.BasicTermASL_ME`
the user can specify the length of each projection step,
from 1 month to 1 year. By default, the first 60 steps are monthly
projections, while steps after that are annual.
This model reads issue date information from model point input,
and handles policy anniversaries precisely.
See :mod:`~basiclife.BasicTermASL_ME` for more details.




