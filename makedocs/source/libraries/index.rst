.. include:: /banners.rst

Libraries
=========

.. table::

   =============================== =============== ===============================================================
   Library                                         Contents
   =============================== =============== ===============================================================
   :doc:`basiclife/index`          |modelx banner| Basic life insurance cashflow models and examples
   :doc:`savings/index`            |modelx banner| Cashflow models of saving products with cash values
   :doc:`assets/index`             |modelx banner| Basic models of bond portfolios
   :doc:`ifrs17a/index`                            IFRS17 calculation model and examples
   :doc:`economic/index`           |modelx banner| Basic Hull-White model
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
were developed using an older cashflow model.
Additionally, all the projects relies on modelx.

.. toctree::
   :maxdepth: 1

   ../projects/fastlife
   ../projects/simplelife
   ../projects/nestedlife
   ../projects/ifrs17sim
   ../projects/solvency2
   ../projects/smithwilson
   ../projects/devguide/index
