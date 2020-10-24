.. module:: nestedlife

.. _project_nestedlife:

Project **nestedlife**
======================

**nestedlife** is a project template to build the same annual projection
model of basic traditional life policies
as :mod:`simplelife`, but at each projection step,
a nested projection going forward from the step is carried out.
The outer and nested projections share the same base assumptions, but
the assumptions of the nested projections can be adjusted based on how
the outer projection develops up to each projection step at which point a
nested projection starts.

The main purpose of this template is to simulate actual/realistic
cashflows as the outer projection, and expected future cashflows at each
projection step as each of the inner projection.

By default, some formulas are redefined in :mod:`~nestedlife` module,
to define new cells or redefine existing cells
in :mod:`~projection` module for nested projection, and to allow the user
to adjust surrender rates.

.. contents:: Contents
   :depth: 1
   :local:

Model Structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

Spaces in the dotted yellow line have the same structure as :mod:`simplelife`
model, so refer to :mod:`simplelife` for more details about those sapces.

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
     BaseProj <- Assumption [hstyle=composition];
     Assumption[style=dotted]
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

Project Modules
---------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~model.BaseProj
   ~model.BaseProj.Assumptions
   ~model.Economic
   ~model.LifeTable
   ~model.PV
   ~model.OuterProj
   ~model.OuterProj.Policy
   ~model.OuterProj.InnerProj
