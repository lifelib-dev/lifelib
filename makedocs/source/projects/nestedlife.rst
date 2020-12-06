.. module:: nestedlife

.. _project_nestedlife:

Project **nestedlife**
======================

The **nestedlife** project has the same annual projection
model of basic traditional life policies
as :mod:`simplelife`, but at each projection step,
a nested projection going forward from the step is carried out.
The outer and nested projections share the same base assumptions, but
the assumptions of the nested projections can be adjusted based on how
the outer projection develops up to each projection step at which point a
nested projection starts.

The main purpose of this model is to simulate actual/realistic
cashflows as the outer projection, and expected future cashflows at each
projection step as each of the inner projection.

.. contents:: Contents
   :depth: 1
   :local:

Model Structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

:mod:`~nestedlife.model.Input` Space and :mod:`~nestedlife.model.Economic` Space hold
input data read from *input.xlsx*. :mod:`~nestedlife.model.LifeTable` Space
is the same is the one in :mod:`simplelife`, and calculates
commutation functions and actuarial notations.
:mod:`~nestedlife.model.BaseProj`, and :mod:`~nestedlife.model.PV` serve as
base Spaces for :mod:`~nestedlife.model.OuterProj`
and :mod:`~nestedlife.model.OuterProj.InnerProj`.
:mod:`~nestedlife.model.OuterProj` is for carrying out outer projections,

As is the case of :mod:`simplelife`,
The :mod:`~nestedlife.model.OuterProj` is parametrized with ``PolicyID``,
so ``Projection[1]`` represents the Projection Space for Policy 1.
The present values of the cashflow items are also calculated in
the :mod:`~nestedlife.model.OuterProj` Spaces.
For example, the expression
``nestedlife.OuterProj[1].PV_NetCashflow(0)``
returns the present value of net cashflows for Policy 1.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     nestedlife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     nestedlife <- "OuterProj\n[PolicyID, ScenID=1]" <- "InnerProj[t0]" [hstyle=composition];
     "OuterProj\n[PolicyID, ScenID=1]" [stacked];
     "InnerProj[t0]" [stacked];
     nestedlife <- Economic [hstyle=composition];
     "OuterProj\n[PolicyID, ScenID=1]" <- Policy [hstyle=composition];
     nestedlife <- LifeTable [hstyle=composition];
     nestedlife <- Input [hstyle=composition];
     nestedlife<- BaseProj
     BaseProj[style=dotted]
     BaseProj <- Assumptions [hstyle=composition];
     Assumptions[style=dotted]
     nestedlife <- PV;
     PV[style=dotted];

   }

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";

     BaseProj[style=dotted]
     BaseProj <- OuterProj [hstyle=generalization]
     BaseProj <- InnerProj [hstyle=generalization]
   }

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";

     PV[style=dotted]
     PV <- OuterProj [hstyle=generalization]
     PV <- InnerProj [hstyle=generalization]
   }

Space Details
-------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~model.Input
   ~model.Economic
   ~model.BaseProj
   ~model.BaseProj.Assumptions
   ~model.LifeTable
   ~model.PV
   ~model.OuterProj
   ~model.OuterProj.Policy
   ~model.OuterProj.InnerProj
