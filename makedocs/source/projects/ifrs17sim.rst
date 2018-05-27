.. module:: ifrs17sim

Project **ifrs17sim**
=====================

**ifrs17sim** is a project template for simulating IFRS17
financial statements on sample insurance contracts.

Files that are unique to this project are :mod:`~ifrs17sim`,
:mod:`~ifrs17sim.ifrs` and :mod:`~ifrs17sim.present_values`.
Other files in this project are the same as those in :mod:`nestedlife`.

Jupyter Notebooks
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!*  |launch binder ifrs17sim|

.. |launch binder ifrs17sim| image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/fumitoh/ifrs17sim-demo/master?filepath=ifrs17sim-demo.ipynb

.. toctree::

   ifrs17sim_csm_waterfall.ipynb

Model structure
---------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~ifrs17sim
   ~ifrs
   ~present_values
   ~build_input
   ~lifetable
   ~policy
   ~assumptions
   ~economic
   ~projection