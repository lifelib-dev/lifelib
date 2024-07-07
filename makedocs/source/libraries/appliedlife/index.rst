.. module:: appliedlife
.. include:: /banners.rst

The **appliedlife** Library
=============================

|modelx badge|

.. warning::

   :mod:`appliedlife` is in its active development phase, and its contents are subject to change.


Overview
-----------

The **appliedlife** library features :mod:`~appliedlife.IntegratedLife`, a comprehensive and practical projection model
designed for real-world actuarial tasks.

The :mod:`~appliedlife.IntegratedLife` model offers several key features:

* **Multiple Products:** supports multiple products by inheriting the base logic common to all products.
  Currently, the model supports VA GMAB and GMDB products, with plans to add more in future releases.

* **Flexible Input:** Perform projections with various combinations of input data by simply setting parameters.
  For instance, specify the model point file and scenario file for a specific run using a parameter file.

* **Multiple Runs:** Define multiple runs within the model,
  such as a base case for a certain date or a stressed case for another date,
  thanks to the flexible input feature.

* **External File Input:** All input files are stored externally, outside of the model,
  allowing for decoupling data and logic.

* **Excel Output:** Output projection results of a sample model point directly
  to Excel using `xlwings`_.

The cashflow logic in :mod:`~appliedlife.IntegratedLife` is based on the :mod:`~savings.CashValue_ME` model
from the :mod:`savings` library, with several enhancements.

See :mod:`~appliedlife.IntegratedLife` for more details.

.. _xlwings:
   https://www.xlwings.org/

How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *appliedlife* library.
For example, to copy as a folder named *appliedlife*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("appliedlife", r"C:\path\to\your\applifedlife")


:mod:`~appliedlife.IntegratedLife` uses `xlwings`_ in
:func:`ProductBase.excel_sample <appliedlife.IntegratedLife.ProductBase.excel_sample>`.
If not yet installed, install it using ``pip`` or ``conda``.

.. seealso::

   * :ref:`FAQ on xlwings <faq_xlwings>`

Library Contents
------------------

.. toctree::
   :hidden:
   :maxdepth: 1

   IntegratedLife

.. table::
   :widths: 20 80

   ========================================= ===========================================================================
   File or Folder                            Description
   ========================================= ===========================================================================
   IntegratedLife                               The :mod:`~appliedlife.IntegratedLife` model.
   model_parameters.xlsx                     The parameter file of :mod:`~appliedlife.IntegratedLife`
   input_tables                              Folder containing sample assumptions, mortality tables and product specs
   economic_data                             Folder containing economic data files
   model_point_data                          Folder containing model point files
   ========================================= ===========================================================================

