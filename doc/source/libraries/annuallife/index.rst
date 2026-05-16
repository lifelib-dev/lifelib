.. module:: annuallife
.. include:: /banners.rst

The **annuallife** Library
=============================

|modelx badge|

Overview
-----------

The **annuallife** library packages :mod:`~annuallife.TradLife_A`, an
annual new business projection model of basic traditional life policies,
covering term, whole life and endowment products, built with modelx.

:mod:`~annuallife.TradLife_A` projects liability cashflows and their
present values for policies represented by model points. Projected items
include:

* Premiums,
* Commissions and expenses,
* Claims.

Premiums are calculated using commutation functions.

Cells for investment income reserves are defined but not implemented.

See :mod:`~annuallife.TradLife_A` for more details.

Successor of simplelife
^^^^^^^^^^^^^^^^^^^^^^^

The **annuallife** library is the updated successor of the legacy
:ref:`project_simplelife` project. Compared with the original
*simplelife* model, :mod:`~annuallife.TradLife_A` introduces:

* **Snake-case cell and reference names** following the
  :mod:`basiclife.BasicTerm_SC` naming convention
  (for example, ``net_cf`` rather than ``NetInsurCF``,
  ``claims`` rather than ``BenefitDeath``).
* **Array-based model points.** Policy attributes are read from
  *input.xlsx* as 1-D NumPy arrays and addressed by the integer
  parameter ``idx`` (0-based) instead of ``PolicyID`` (1-based).
* **A flatter space layout.** ``Assumptions`` and ``PolicyAttrs`` are
  top-level spaces instead of being nested inside ``Projection``.
* **A renamed input space.** The space holding *input.xlsx*-backed
  References is now ``InputData`` and is referenced as ``input_data``
  by the rest of the model.

How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
create your own copy of the *annuallife* library.
For example, to copy as a folder named *annuallife*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("annuallife", r"C:\path\to\your\annuallife")

The :mod:`~annuallife.TradLife_A` model loads its data from *input.xlsx*,
which lives next to the model directory inside the library folder.

To read the model on the IPython console, change the working directory
to the library folder and use modelx's ``read_model`` function::

    >>> import modelx as mx

    >>> m = mx.read_model("TradLife_A")

More detailed instructions on how to read, run and inspect the model
are described in the
:ref:`Basic Usage <tradlife_a-basic-usage>` section
of the :mod:`~annuallife.TradLife_A` documentation.


Library Contents
------------------

.. toctree::
   :hidden:
   :maxdepth: 1

   TradLife_A
   tradlife_a-demo
   tradlife_a-space-overview

.. table::
   :widths: 25 75

   ====================================== ==========================================================================
   File or Folder                         Description
   ====================================== ==========================================================================
   ``TradLife_A``                         The :mod:`~annuallife.TradLife_A` model.
   ``input.xlsx``                         Excel workbook holding policy data, assumptions, mortality tables, scenarios and product specs.
   ``plot_tradlife_a.py``                 sphinx-gallery plot script that renders the cashflow chart.
   ``plot_pvcashflows_tradlife_a.py``     sphinx-gallery plot script that renders present-value cashflows.
   ``tradlife_a-demo.ipynb``              Jupyter notebook demonstrating cashflow projection.
   ``tradlife_a-space-overview.ipynb``    Tutorial notebook on the space tree of :mod:`~annuallife.TradLife_A`.
   ====================================== ==========================================================================


Jupyter Notebooks
-----------------

======================================== ===================================================================
:doc:`tradlife_a-demo`                   |colab annuallife tradlife_a-demo|
:doc:`tradlife_a-space-overview`         |colab annuallife tradlife_a-space-overview|
======================================== ===================================================================
