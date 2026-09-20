.. include:: /banners.rst

Libraries
=========

The following is a list of the lifelib libraries.
|modelx badge| indicates that the models in the library are built with it.
These models can be transformed to self-contained Python packages
independent of modelx using modelx's export feature.


Generic Liability Models
------------------------

The libraries in this category provide projection models of generic
life insurance products, assuming no specific market or regulation.
They are meant to be customized and extended by the user, and range from
minimal cashflow models suitable for learning and validation
to a comprehensive model designed for practical use.

.. table::

   =============================== =============== ===============================================================
   Library                                         Contents
   =============================== =============== ===============================================================
   :doc:`annuallife/index`         |modelx badge|  Annual projection model of basic traditional life policies
   :doc:`basiclife/index`          |modelx badge|  Basic life insurance cashflow models and examples
   :doc:`savings/index`            |modelx badge|  Cashflow models of saving products with cash values
   :doc:`appliedlife/index`        |modelx badge|  Comprehensive and practical projection model
   =============================== =============== ===============================================================

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Generic Liability Models

   annuallife/index.rst
   basiclife/index.rst
   savings/index.rst
   appliedlife/index.rst


Reference Liability Models
--------------------------

The libraries in this category provide reference liability cashflow models
of the individual life and annuity products sold in a specific market.
Each product comes with the product specification and technical notes
that its model was built from, and the model reproduces the worked example
in the notes, asserted cell by cell.

.. table::

   =============================== =============== ===============================================================
   Library                                         Contents
   =============================== =============== ===============================================================
   :doc:`uslib/index`              |modelx badge|  U.S. life and annuity reference products and models
   :doc:`uklib/index`              |modelx badge|  UK life and pension annuity reference products and models
   :doc:`jplib/index`              |modelx badge|  Japanese life and third-sector reference products and models
   :doc:`frlib/index`              |modelx badge|  French life, savings and annuity reference products and models
   :doc:`krlib/index`              |modelx badge|  Korean life, health and annuity reference products and models
   =============================== =============== ===============================================================

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Reference Liability Models

   uslib/index.md
   uklib/index.md
   jplib/index.md
   frlib/index.md
   krlib/index.md


Miscellaneous Models
--------------------

The libraries in this category cover areas other than liability cashflow
projection, such as asset portfolios, economic scenario generation,
IFRS 17 reporting and model point selection by cluster analysis.

.. table::

   =============================== =============== ===============================================================
   Library                                         Contents
   =============================== =============== ===============================================================
   :doc:`assets/index`             |modelx badge|  Basic models of bond portfolios
   :doc:`ifrs17a/index`                            IFRS17 calculation model and examples
   :doc:`economic/index`           |modelx badge|  Basic Hull-White model
   :doc:`economic_curves/index`                    Algorithms for modeling economic scenarios
   :doc:`cluster/index`                            Notebooks for model point selection by cluster analysis
   =============================== =============== ===============================================================

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Miscellaneous Models

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

.. table::

   =============================== =============== ===============================================================
   Library                                         Contents
   =============================== =============== ===============================================================
   :doc:`../projects/fastlife`     |modelx badge|  Faster reimplementation of the simplelife model
   :doc:`../projects/simplelife`   |modelx badge|  Annual projection model of basic traditional life policies
   :doc:`../projects/nestedlife`   |modelx badge|  Nested projections based on the simplelife model
   :doc:`../projects/ifrs17sim`    |modelx badge|  Simulation of IFRS17 financial statements
   :doc:`../projects/solvency2`    |modelx badge|  Life risk calculation based on the Solvency II standard formula
   :doc:`../projects/smithwilson`  |modelx badge|  Extrapolation of risk-free rates by the Smith-Wilson method
   =============================== =============== ===============================================================

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Past Libraries

   ../projects/fastlife
   ../projects/simplelife
   ../projects/nestedlife
   ../projects/ifrs17sim
   ../projects/solvency2
   ../projects/smithwilson
