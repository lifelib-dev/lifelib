.. module:: simplelife
.. include:: /banners.rst

.. _project_simplelife:

Project **simplelife**
======================

|modelx badge|

This project includes the **simplelife** model,
which is an annual projection model of basic traditional life policies.
The simplelife model is designed in such a way that allows you to
trace calculations for each individual model point,
so it can be a good reference for building validation models.

A simplelife model projects life insurance cashflows and
their present values for policies
represented by model points. Projected items include:

* Premium income,
* Commissions and expenses,
* Benefit outgo.

Cells for investment income, change in reserve and profits are included
but not tested.

The cashflow projection is carried out in the :mod:`~simplelife.model.Projection` Space.
Most Cells in the :mod:`~simplelife.model.Projection` Spaces are defined in its base Spaces,
:mod:`~simplelife.model.BaseProj` and :mod:`~simplelife.model.PV`.
The :mod:`~simplelife.model.Projection` is parametrized with ``PolicyID``,
so ``Projection[1]`` represents the Projection Space for Policy 1.
The present values of the cashflow items are also calculated in
the :mod:`~simplelife.model.Projection` Spaces.
For example, the expression
``simplelife.Projection[1].PV_NetCashflow(0)``
returns the present value of net cashflows for Policy 1.

The :mod:`~simplelife.model.Projection` Space has child Spaces,
:mod:`~simplelife.model.Projection.Policy` and :mod:`~simplelife.model.Projection.Assumptions`.
The :mod:`~simplelife.model.Projection.Policy` Space contains Cells representing policy attributes, such as
product type, issue age, sum assured, etc.
It also contains Cells for calculating policy values such as premium rates and
cash surrender value rates.
The :mod:`~simplelife.model.Projection.Assumptions` Space contains Cells to pick up assumption data for
its model point.

The :mod:`~simplelife.model.Input` Space is for storing input data read from  the Excel input file,
*input.xlsx*.

Input data, such as:

* model point data,
* product specs,
* actuarial assumptions,
* economic scenarios,

are read from an Excel input file, which is in the model folder.
The Space contains References that hold `ExcelRange`_ objects.

.. _ExcelRange:
   https://docs.modelx.io/en/latest/reference/dataclient.html#excelrange

Premium rates are calculated using commutation functions and actuarial
formulas. Commutation functions are calculated for each
combination of mortality table IDs, sex and constant interest rates
in LifeTable Spaces.

Cash surrender values are calculated as net premium reserves net of
surrender charges. The net premium reserves are calculated using
the same commutation functions as the ones used by
the premium rate calculation.

.. warning::

    The **simplelife** model is designed with a focus more on traceability
    than speed and is best suited for model validation.
    To build a fast model, you should take `the parallel modeling approach`_
    as employed by :doc:`/projects/fastlife`.

.. _the parallel modeling approach:
   http://modelx.io/blog/2020/12/12/introduction-to-fastlife-and-parallel-modeling/

How to use the project
-----------------------

Create a project folder from IPython in Spyder.
as explained in :ref:`create-a-project` section.
Read the model in Spyder
by following the steps in :ref:`read-a-model` section.

The model become accessible
as ``simplelife`` global variable
in the IPython console in Spyder.

There is no explicit 'Run' command to run the model. The model calculates its values on the fly, when requested.

Model structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

The diagram below shows the spaces in the simplelife model.

.. figure:: /images/projects/simplelife/composition.png

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

The :mod:`~simplelife.model.Projection` Space inherits from
:mod:`~simplelife.model.BaseProj` and :mod:`~simplelife.model.PV`.

.. figure:: /images/projects/simplelife/inheritance.png

Jupyter Notebooks
-----------------

======================================== ======================================================
:doc:`simplelife-demo`                   |colab simplelife simplelife-demo|
:doc:`simplelife-space-overview`         |colab simplelife simplelife-space-overview|
======================================== ======================================================

.. toctree::
   :hidden:

   simplelife-demo
   simplelife-space-overview

Space Details
-------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~model.Input
   ~model.LifeTable
   ~model.Economic
   ~model.BaseProj
   ~model.PV
   ~model.Projection
   ~model.Projection.Policy
   ~model.Projection.Assumptions












   

   
   
   

   
   
   