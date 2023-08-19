.. include:: /banners.rst

Libraries
=========

The following is a list of the lifelib libraries.
|modelx badge| indicates that the models in the library are built with it.
These models can be transformed to self-contained Python packages
independent of modelx using modelx's export feature.

.. table::

   =============================== =============== ===============================================================
   Library                                         Contents
   =============================== =============== ===============================================================
   :doc:`basiclife/index`          |modelx badge|  Basic life insurance cashflow models and examples
   :doc:`savings/index`            |modelx badge|  Cashflow models of saving products with cash values
   :doc:`assets/index`             |modelx badge|  Basic models of bond portfolios
   :doc:`ifrs17a/index`                            IFRS17 calculation model and examples
   :doc:`economic/index`           |modelx badge|  Basic Hull-White model
   :doc:`economic_curves/index`                    Algorithms for modeling economic scenarios
   :doc:`cluster/index`                            Notebooks for model point selection by cluster analysis
   =============================== =============== ===============================================================


.. toctree::
   :maxdepth: 2
   :hidden:

   basiclife/index.rst
   savings/index.rst
   assets/index.rst
   ifrs17a/index.md
   economic/index.rst
   economic_curves/index.md
   cluster/index.rst

.. _past-libraries:


Past Libraries
----------------

The libraries listed below were introduced before the release of lifelib v0.1.1
and were originally referred to as "projects."
All of these libraries, with the exception of *simithwilson*,
were developed using an older cashflow model. All the projects use modelx.

.. toctree::
   :maxdepth: 1

   ../projects/fastlife
   ../projects/simplelife
   ../projects/nestedlife
   ../projects/ifrs17sim
   ../projects/solvency2
   ../projects/smithwilson
   ../projects/devguide/index
