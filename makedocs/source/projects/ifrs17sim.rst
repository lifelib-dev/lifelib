.. module:: ifrs17sim

.. _project_ifrs17sim:

Project **ifrs17sim**
=====================

**ifrs17sim** is a project template for simulating IFRS17
financial statements on sample insurance contracts.

Files that are unique to this project are :mod:`~ifrs17sim` and
:mod:`~ifrs17sim.ifrs`.
Other files in this project are the same as those in :mod:`nestedlife`.

.. contents:: Contents
   :depth: 1
   :local:

Model Structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

Spaces in the dotted yellow line have the same structure as :mod:`simplelife`
model, so refer to :mod:`simplelife` for more details about those spaces.


.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     ifrs17sim [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96];
     ifrs17sim <- "OuterProj[PolicyID]" <- "InnerProj[t0]" [hstyle=composition];
     "OuterProj[PolicyID]" [stacked];
     "InnerProj[t0]" [stacked, width=96];
     "InnerProj[t0]" <- "PresentValue[t_rate]" [hstyle=composition];
     "PresentValue[t_rate]"[stacked];
     ifrs17sim <- Economic [hstyle=composition];
     ifrs17sim  <- Assumption [hstyle=composition];
     ifrs17sim <- Policy [hstyle=composition];
     ifrs17sim <- LifeTable [hstyle=composition];
     ifrs17sim <- Input [hstyle=composition];

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

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     IFRS[style=dotted]
     IFRS <- OuterProj [hstyle=generalization]
     BaseProj[style=dotted]
     BaseProj <- OuterProj [hstyle=generalization]
     BaseProj <- InnerProj [folded, hstyle=generalization]
   }


Jupyter Notebooks
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!*

* CSM waterfalls |binder ifrs17sim_csm_waterfall|
* IFRS17 Simulation (Baseline) |binder ifrs17sim_charts_baseline|
* IFRS17 Simulation (Lapse Scenario) |binder ifrs17sim_charts_lapsescen|

.. include:: /binderlinks.rst
   :start-after: Begin binder banner
   :end-before: End binder banner

.. toctree::

   notebooks/ifrs17sim/ifrs17sim_csm_waterfall.ipynb
   notebooks/ifrs17sim/ifrs17sim_charts_baseline.ipynb
   notebooks/ifrs17sim/ifrs17sim_charts_lapsescen.ipynb


Project Modules
---------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~ifrs17sim
   ~ifrs
   ~present_value
   ~build_input
   ~lifetable
   ~policy
   ~assumption
   ~economic
   ~projection