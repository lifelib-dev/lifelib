.. module:: economic.BasicHullWhite

The **BasicHullWhite** Model
=============================

Overview
---------

:mod:`~economic.BasicHullWhite` is a simple implementation of `the Hull-White model <https://en.wikipedia.org/wiki/Hull%E2%80%93White_model>`_.
The Hull-White model is a short rate model represented by the stochastic differential equation:

.. math::

    dr(t) = (\theta(t) - a r(t))dt + \sigma dW


:mod:`~economic.BasicHullWhite` preforms Monte-Carlo simulations
and generates paths of the instantaneous short rate based on the Hull-White model.
Many properties of the Hull-White model are analytically solvable,
and :mod:`~economic.BasicHullWhite` also includes formulas analytically solving for the properties.

Formulas for the Monte-Carlo simulation perform computation fast,
as they operate on numpy vectors to process all scenarios at once.

All the contents are defined in :mod:`~economic.BasicHullWhite.HullWhite` space.

.. seealso::
    * `Damiano Brigo, Fabio Mercurio (2001, 2nd Ed. 2006). Interest Rate Models - Theory and Practice with Smile, Inflation and Credit <https://link.springer.com/book/10.1007/978-3-540-34604-3>`_
    * `Paul Glasserman (2003). Monte Carlo Methods in Financial Engineering <https://link.springer.com/book/10.1007/978-0-387-21617-1>`_

Model Specifications
---------------------

The :mod:`~economic.BasicHullWhite.HullWhite` Space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



.. autosummary::
   :toctree: ../generated/
   :template: llmodule.rst

   ~HullWhite
