.. module:: nestedlife

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

Model Structure
---------------

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     nestedlife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC"]
     nestedlife <- "OuterProj[PolicyID]" <- "InnerProj[t0]" [hstyle=composition];
     "OuterProj[PolicyID]" [stacked];
     "OuterProj[PolicyID]" -> BaseProjection [folded, hstyle=generalization]
     "InnerProj[t0]" -> BaseProjection [folded, hstyle=generalization]
     "InnerProj[t0]" [stacked];
     BaseProjection [style=dotted];
     nestedlife <- BaseProjection [hstyle=composition, style=dotted];
     PV_Mixin [style=dotted];
     nestedlife <- PV_Mixin [hstyle=composition, style=dotted];
     BaseProjection -> PV_Mixin [folded, hstyle=generalization];
     nestedlife <- Economic [hstyle=composition];
     nestedlife <- Assumption [hstyle=composition];
     nestedlife <- Policy [hstyle=composition];
     nestedlife <- LifeTable [hstyle=composition];
     nestedlife <- Input [hstyle=composition];
     group {
       Economic;
       Assumption;
       Policy;
       LifeTable;
       Input;
       shape=line
       style=dashed
       color=orange
     }
   }


Project Modules
---------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~nestedlife
   ~build_input
   ~lifetable
   ~policy
   ~assumption
   ~economic
   ~projection
