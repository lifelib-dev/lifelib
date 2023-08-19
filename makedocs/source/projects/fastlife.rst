.. module:: fastlife

.. _project_fastlife:

Project **fastlife**
======================

.. include:: /banners.rst
   :start-after: Begin modelx badge
   :end-before: End modelx badge

|modelx badge|

This project includes the **fastlife** model. The firstlife model
calculates the present values of the net insurance cashflows.
The calculation results are the same as the model in :doc:`simplelife`.
However, the fastlife model
carries out the calculations for all model points in parallel at the same time,
while the calculations in the simplelife model are done separately for
each model point. Because the parallel processing is

The values of most Cells for projecting cashflows are `pandas Series`_ objects
that contain calculation results for all model points::

    >>> fastlife.Projection.PV_NetCashflow(0)
    Policy
    1      8.954018e+03
    2      7.511092e+03
    3      9.173907e+03
    4      7.638071e+03
    5      9.418541e+03
               ...
    296    2.599794e+06
    297    2.298079e+06
    298    2.557191e+06
    299    2.242406e+06
    300    2.510715e+06
    Length: 300, dtype: float64

fastlife runs faster than simplelife thanks to powerful vector operations
on `pandas Series`_.
The blog posts on https://modelx.io/blog linked below discuss the background
and performance of fastlife.

**Related posts**

* `modelx blog: Introduction to fastlife and parallel modeling <http://modelx.io/blog/2020/12/12/introduction-to-fastlife-and-parallel-modeling/>`_
* `modelx blog: fastlife got faster <http://modelx.io/blog/2021/01/31/fastlife-got-faster/>`_

.. _pandas Series:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

How to use the project
-----------------------

Create a project folder from IPython in Spyder.
as explained in :ref:`create-a-project` section.
Read the model in Spyder
by following the steps in :ref:`read-a-model` section.

The model become accessible
as ``fastlife`` global variable
in the IPython console in Spyder.

There is no explicit 'Run' command to run the model. The model calculates its values on the fly, when requested.

Model structure
---------------

Composition Structure
^^^^^^^^^^^^^^^^^^^^^

The diagram below shows the spaces in the fastlife model.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     fastlife [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     fastlife <- Projection [hstyle=composition];
     Projection <- Assumptions [hstyle=composition];
     Projection <- Policy [hstyle=composition];
     fastlife <- PV
     Econ[label="Economic[ScenID]", stacked];
     fastlife <- Econ[hstyle=composition];
     LifeTable [label="LifeTable\n[Sex, IntRate, TableID]", stacked];
     fastlife <- LifeTable [hstyle=composition];
     fastlife <- Input [hstyle=composition];
     PV[style=dotted]
   }

Inheritance Structure
^^^^^^^^^^^^^^^^^^^^^

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     PV[style=dotted]
     PV<- Projection [hstyle=generalization];
   }

Jupyter Notebooks
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!*

* Introduction to fastlife |binder fastlife_introduction|

.. include:: /banners.rst
   :start-after: Begin binder banner
   :end-before: End binder banner

.. toctree::

   fastlife-introduction

Space Details
-------------

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~model.Input
   ~model.LifeTable
   ~model.Economic
   ~model.PV
   ~model.Projection
   ~model.Projection.Policy
   ~model.Projection.Assumptions




















