.. module:: ifrs17sim

.. _project_ifrs17sim:

Project **ifrs17sim**
=====================

**ifrs17sim** is a project for simulating IFRS17
financial statements on sample insurance contracts.

Files that are unique to this project are :mod:`~ifrs17sim` and
:mod:`~ifrs17sim.ifrs`.
Other files in this project are similar to those in :mod:`nestedlife`.

Model Structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

The composition structure is almost the same as the structure of
:mod:`~nestedlife`, except that :mod:`~ifrs17sim.model.OuterProj.InnerProj.PV`
in this model is a child Space of :mod:`~ifrs17sim.model.OuterProj.InnerProj`


.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     ifrs17sim [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     ifrs17sim <- "OuterProj\n[PolicyID, ScenID=1]" <- "InnerProj[t0]" [hstyle=composition];
     "OuterProj\n[PolicyID, ScenID=1]" [stacked];
     "InnerProj[t0]" [stacked];
     "InnerProj[t0]" <- PV [hstyle=composition]
     ifrs17sim <- Economic [hstyle=composition];
     "OuterProj\n[PolicyID, ScenID=1]" <- Policy [hstyle=composition];
     ifrs17sim <- LifeTable [hstyle=composition];
     ifrs17sim <- Input [hstyle=composition];
     ifrs17sim<- BaseProj
     BaseProj[style=dotted]
     BaseProj <- Assumptions [hstyle=composition];
     Assumptions[style=dotted]
     ifrs17sim<- IFRS
     IFRS [style=dotted]
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
   }

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     BaseProj[style=dotted]
     BaseProj <- InnerProj[hstyle=generalization]
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


Space Details
-------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst


   ~model.BaseProj
   ~model.BaseProj.Assumptions
   ~model.Economic
   ~model.LifeTable
   ~model.OuterProj
   ~model.OuterProj.Policy
   ~model.OuterProj.InnerProj
   ~model.OuterProj.InnerProj.PV