.. module:: ifrs17sim

.. _project_ifrs17sim:

Project **ifrs17sim**
=====================

.. include:: /banners.rst
   :start-after: Begin modelx badge
   :end-before: End modelx badge

|modelx badge|

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


.. figure:: /images/projects/ifrs17sim/composition.png

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

.. figure:: /images/projects/ifrs17sim/inheritance1.png

.. figure:: /images/projects/ifrs17sim/inheritance2.png

Jupyter Notebooks
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!*

* CSM waterfalls |binder ifrs17sim_csm_waterfall|
* IFRS17 Simulation (Baseline) |binder ifrs17sim_charts_baseline|
* IFRS17 Simulation (Lapse Scenario) |binder ifrs17sim_charts_lapsescen|

.. include:: /banners.rst
   :start-after: Begin binder banner
   :end-before: End binder banner

.. toctree::

   ifrs17sim_csm_waterfall
   ifrs17sim_charts_baseline
   ifrs17sim_charts_lapsescen


Space Details
-------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst


   ~model.BaseProj
   ~model.BaseProj.Assumptions
   ~model.Economic
   ~model.LifeTable
   ~model.IFRS
   ~model.OuterProj
   ~model.OuterProj.Policy
   ~model.OuterProj.InnerProj
   ~model.OuterProj.InnerProj.PV