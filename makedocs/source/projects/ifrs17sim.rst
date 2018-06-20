.. module:: ifrs17sim

Project **ifrs17sim**
=====================

**ifrs17sim** is a project template for simulating IFRS17
financial statements on sample insurance contracts.

Files that are unique to this project are :mod:`~ifrs17sim` and
:mod:`~ifrs17sim.ifrs`.
Other files in this project are the same as those in :mod:`nestedlife`.


Model Structure
---------------

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     ifrs17sim [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC"]
     ifrs17sim <- IFRS [hstyle=composition, style=dotted];
     IFRS [style=dotted]
     "OuterProj[PolicyID]" -> IFRS [folded, hstyle=generalization]
     ifrs17sim <- "OuterProj[PolicyID]" <- "InnerProj[t0]" [hstyle=composition];
     "OuterProj[PolicyID]" [stacked];
     "OuterProj[PolicyID]" -> BaseProj [folded, hstyle=generalization]
     "InnerProj[t0]" -> BaseProj [folded, hstyle=generalization]
     "InnerProj[t0]" [stacked];
     "InnerProj[t0]" <- "PresentValue[t_rate]" [hstyle=composition];
     BaseProj [style=dotted];
     ifrs17sim <- BaseProj [hstyle=composition, style=dotted];
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

Jupyter Notebooks
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!*

* CSM waterfalls |binder ifrs17sim_csm_waterfall|
* IFRS waterfalls |binder ifrs17sim_ifrs_waterfall|

.. include:: /binderlinks.rst
   :start-after: Begin binder ifrs17sim_csm_waterfall
   :end-before: End binder ifrs17sim_ifrs_waterfall

.. toctree::

   ifrs17sim_csm_waterfall.ipynb
   ifrs17sim_ifrs_waterfall.ipynb


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