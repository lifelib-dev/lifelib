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

Nested projection example
^^^^^^^^^^^^^^^^^^^^^^^^^^

The library also packages :mod:`~annuallife.TradLife_A_EX1`, an example
model that demonstrates how to build a **nested projection** in modelx —
a projection that, at each step, runs further inner projections. The
technique is illustrated with a Solvency II life-risk SCR and risk-margin
calculation built on :mod:`~annuallife.TradLife_A`, but the focus is the
nested-projection pattern rather than the Solvency II implementation
itself.

:mod:`~annuallife.TradLife_A_EX1` reuses the structure, assumptions and
input data of :mod:`~annuallife.TradLife_A`; only the spaces that change
are documented on its page. See :mod:`~annuallife.TradLife_A_EX1` for the
list of updates from :mod:`~annuallife.TradLife_A`.

Successor of simplelife and solvency2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Likewise, :mod:`~annuallife.TradLife_A_EX1` supersedes the legacy
:ref:`project_solvency2` project. Both build a Solvency II life-risk SCR
and risk-margin calculation as a reference for complex nested
projections, but :mod:`~annuallife.TradLife_A_EX1` does so on top of the
modernized :mod:`~annuallife.TradLife_A` model. The *solvency2* project
is therefore deprecated and will be removed in a future release.

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

Older modelx versions
^^^^^^^^^^^^^^^^^^^^^

:mod:`~annuallife.TradLife_A` is saved in the modelx serializer
version 7 format and requires **modelx v0.31.0 or newer**.

For users whose ``modelx`` is older than v0.31.0, the library also
includes ``TradLife_A_mx30``, a copy of :mod:`~annuallife.TradLife_A`
saved in the older serializer version 6 format. It is the same model
and reads its data from the same *input.xlsx*. Read it instead with::

    >>> import modelx as mx

    >>> m = mx.read_model("TradLife_A_mx30")


Library Contents
------------------

.. toctree::
   :hidden:
   :maxdepth: 1

   TradLife_A
   TradLife_A_EX1
   tradlife_a-demo
   tradlife_a-space-overview

.. table::
   :widths: 25 75

   ============================================= ==========================================================================
   File or Folder                                Description
   ============================================= ==========================================================================
   ``TradLife_A``                                The :mod:`~annuallife.TradLife_A` model.
   ``TradLife_A_EX1``                            The :mod:`~annuallife.TradLife_A_EX1` model, a Solvency II life-risk extension of :mod:`~annuallife.TradLife_A`.
   ``TradLife_A_mx30``                           Copy of :mod:`~annuallife.TradLife_A` saved in the modelx serializer version 6 format, for ``modelx`` older than v0.31.0.
   ``input.xlsx``                                Excel workbook holding policy data, assumptions, mortality tables, scenarios and product specs. It also holds the ``LifeShocks``, ``LifeCorr`` and ``CoCRate`` inputs read by :mod:`~annuallife.TradLife_A_EX1`.
   ``plot_tradlife_a.py``                        Python script for :doc:`/generated_examples/annuallife/plot_tradlife_a`
   ``plot_pvcashflows_tradlife_a.py``            Python script for :doc:`/generated_examples/annuallife/plot_pvcashflows_tradlife_a`
   ``plot_scr_cashflows_tradlife_a_ex1.py``      Python script for :doc:`/generated_examples/annuallife/plot_scr_cashflows_tradlife_a_ex1`
   ``plot_scr_radar_tradlife_a_ex1.py``          Python script for :doc:`/generated_examples/annuallife/plot_scr_radar_tradlife_a_ex1`
   ``plot_pols_if_lapse_up_tradlife_a_ex1.py``   Python script for :doc:`/generated_examples/annuallife/plot_pols_if_lapse_up_tradlife_a_ex1`
   ``draw_charts_radar.py``                      Helper module providing ``draw_radar`` for the radar plot script.
   ``tradlife_a-demo.ipynb``                     Jupyter notebook demonstrating cashflow projection.
   ``tradlife_a-space-overview.ipynb``           Tutorial notebook on the space tree of :mod:`~annuallife.TradLife_A`.
   ============================================= ==========================================================================


Jupyter Notebooks
-----------------

======================================== ===================================================================
:doc:`tradlife_a-demo`                   |colab annuallife tradlife_a-demo|
:doc:`tradlife_a-space-overview`         |colab annuallife tradlife_a-space-overview|
======================================== ===================================================================
