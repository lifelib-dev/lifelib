.. module:: ifrs17sim

Project **ifrs17sim**
=====================

**ifrs17sim** is a project template for simulating IFRS17
financial statements on sample insurance contracts.

Files that are unique to this project are :mod:`~ifrs17sim` and
:mod:`~ifrs17sim.ifrs`.
Other files in this project are the same as those in :mod:`nestedlife`.

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