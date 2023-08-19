.. module:: smithwilson

.. _project_smithwilson:

Project **smithwilson**
=======================

.. include:: /banners.rst
   :start-after: Begin modelx badge
   :end-before: End modelx badge

|modelx badge|

The **smithwilson** project includes the **smithwilson** model,
which extrapolates observed risk-free interest rates using the Smith-Wilson method.

The Smith-Wilson method is used for extrapolating risk-free interest rates under the Solvency II framework.
The method is described in
*"QIS 5 Risk-free interest rates – Extrapolation method"*,
a technical paper issued by CEIOPS(the predecessor of EIOPA).
The technical paper is available on `EIOPA's web site`_.
Cells in this model are named consistently
with the mathematical symbols in the technical paper.

This project is inspired by a pure Python implementation of Smith-Wilson
yield curve fitting algorithm created by Dejan Simic.
His original work can be found `here <https://github.com/simicd/smith-wilson-py>`_.
A copy of the original work is included in this project
under smith-wilson-py folder for your reference.

The model contains default input values as references (refs),
such as ``spot_rates``, ``N``, ``UFR`` and ``alpha``.
By default, these values are set equal to the values used in Dejan's
reference model.
The original source of the input data is Switzerland EIOPA spot rates
with LLP 25 years available from the following source.

Source: RFR_spot_no_VA tab in EIOPA_RFR_20190531_Term_Structures.xlsx,
archived in EIOPA_RFR_20190531.zip, avaialble on
`EIOPA's Risk-Free Interest Rate Term Structures web site`_.

.. _EIOPA's Risk-Free Interest Rate Term Structures web site: https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/regulation-supervision/insurance/solvency-ii-technical-information/risk-free-interest-rate-term-structures

.. _EIOPA's web site: https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/publications/qis/insurance/insurance-quantitative-impact-study-5/background-documents
.. _QIS 5 Risk-free interest rates – Extrapolation method: https://wayback.archive-it.org/org-1495/20191229100044/https:/eiopa.europa.eu/Publications/QIS/ceiops-paper-extrapolation-risk-free-rates_en-20100802.pdf


Project files and folders
-------------------------

A ``smithwilson`` project folder is created by the ``lifelib-create`` command.
The table below lists files and folders included in the project.

.. table::

    ===================================== ==============================================================================================
    File/Folder                           Notes
    ===================================== ==============================================================================================
    smithwilson-overview.ipnb             A `Jupyter notebook`_ showing how to read or create the model.
    model                                 The smithwilson model.
    smith-wilson-py                       Pure python implementation by Dejan Simic.
    plot_smithwilson.py                   An :doc:`example script </generated_examples/index>` to plot forward rates with various alpha.
    ===================================== ==============================================================================================

How to use the model
--------------------

Create a project folder
by executing the following command in the *WinPython Command Prompt*
as explained in :ref:`create-a-project` section.
You should pass your own project path as the last argument.

.. code-block:: none

    > lifelib-create --template smithwilson C:\Users\fumito\mysmithwilson


A `Jupyter notebook`_ is included in the created folder.
The notebook shows how to read in the model included in the project.
It also shows how to create the same model from scratch.

Each formula in the model is explained
in :mod:`~smithwilson.model.SmithWilson` space page.


Jupyter notebook
-----------------

A live version of the Jupyter notebook below is available online,
thanks to Binder.

*Launch this sample now!* |binder smithwilson_overview|

.. include:: /banners.rst
   :start-after: Begin binder banner
   :end-before: End binder banner

.. toctree::

   smithwilson-overview


Space Details
-------------

The **smithwilson** model contains only one space
named :mod:`~smithwilson.model.SmithWilson`.

.. autosummary::
   :toctree: generated/
   :template: llmodule.rst

   ~model.SmithWilson



















