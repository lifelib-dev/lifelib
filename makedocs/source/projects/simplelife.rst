.. module:: simplelife

.. _project_simplelife:

Project **simplelife**
======================

This project includes the **simplelife** model,
which is an annual projection model of basic traditional life policies.
The simplelife model is designed in such a way that allows you to
trace calculations for each individual model point,
so it can be a good reference for building validation models.

A simplelife model projects life insurance cashflows for policies
represented by model points. Projected items include:

* Premium income,
* Investment income,
* Commissions and expenses,
* Benefit outgo, change in reserves.

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

.. contents:: Contents
   :depth: 1
   :local:

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

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     simplelife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     Proj [label="Projection\n[PolicyID, ScenID=1]", stacked];
     simplelife <- Proj [hstyle=composition];
     Econ[label="Economic[ScenID]", stacked];
     simplelife <- Econ[hstyle=composition];
     Proj <- Assumptions [hstyle=composition];
     Proj <- Policy [hstyle=composition];
     LifeTable [label="LifeTable\n[Sex, IntRate, TableID]", stacked];
     simplelife <- LifeTable [hstyle=composition];
     simplelife <- Input [hstyle=composition];
     simplelife <- BaseProj
     BaseProj[style=dotted]
     simplelife <- PV
     PV[style=dotted]
   }

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

The :mod:`~simplelife.model.Projection` Space inherits from
:mod:`~simplelife.model.BaseProj` and :mod:`~simplelife.model.PV`.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- Projection [hstyle=generalization]
     PV[style=dotted]
     PV<- Projection [hstyle=generalization];
   }

Jupyter Notebooks
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!*

* simplelife Space Overview |binder simplelife_space_overview|

.. include:: /binderlinks.rst
   :start-after: Begin binder banner
   :end-before: End binder banner

.. toctree::

   notebooks/simplelife/simplelife-space-overview.ipynb

Project Modules
---------------

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












   

   
   
   

   
   
   