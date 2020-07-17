.. module:: simplelife

.. _project_simplelife:

Project **simplelife**
======================

**simplelife** includes an annual projection
model of basic traditional life policies.

A simplelife model projects life insurance cashflows and reserves for policies
represented by model points. Projection items include:

* premium income,
* investment income,
* commissions and expenses,
* benefit outgo, change in reserves.

Required capital and investment assets are not modeled.
Input data, such as:

* model point data,
* product specs,
* actuarial assumptions,
* economic scenarios,

are read from an Excel file.

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

The diagram below shows the spaces contained in a simplelife model.
Note that the subspaces under Input space are not drawn in the diagram,
as they are quite a few.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     simplelife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     Proj [label="Projection[PolicyID]", stacked];
     simplelife <- Proj [hstyle=composition];
     Econ[label="Economic[ScenID]", stacked];
     simplelife <- Econ[hstyle=composition];
     Assumption [label="Assumption[PolicyID]", stacked];
     simplelife <- Assumption [hstyle=composition];
     Policy [label="Policy[PolicyID]", stacked];
     simplelife <- Policy [hstyle=composition];
     LifeTable [label="LifeTable\n[Sex, IntRate, TableID]", stacked];
     simplelife <- LifeTable [hstyle=composition];
     simplelife <- Input [hstyle=composition];
     "various..." [stacked, width=96];
     Input <- "various..."[hstyle=composition];
   }

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- OuterProj [hstyle=generalization]
     PresentValue[style=dotted]
     PresentValue <- OuterProj [hstyle=generalization];
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

   ~model.LifeTable
   ~model.Policy
   ~model.Assumption
   ~model.Economic
   ~model.BaseProj
   ~model.PV












   

   
   
   

   
   
   