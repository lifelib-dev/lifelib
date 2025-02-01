.. module:: basiclife.BasicTerm_SC

The **BasicTerm_SC** Model
==========================

Overview
--------

The :mod:`~basiclife.BasicTerm_SC` model is a variant of :mod:`~basiclife.BasicTerm_S` that
is optimized for generating a compiled model using
`Cython <https://cython.org/>`_ with `modelx-cython <https://github.com/fumitoh/modelx-cython>`_.

Like the original model, :mod:`~basiclife.BasicTerm_SC` can be exported as a pure Python model
(also called a "nomx" model), which is written as standard Python objects and does not depend on modelx.
This exported model can then be compiled with Cython using the modelx-cython package
(see `the relevant blog post <https://modelx.io/blog/2023/10/21/introducing-modelx-cython/>`_
for more details on modelx-cython).

A compiled version of :mod:`~basiclife.BasicTerm_SC` runs about 7–8 times faster
than its nomx model but yields the same results as :mod:`~basiclife.BasicTerm_S`.
With future improvements to modelx-cython, it is expected that the compiled model
will run even faster. Although :mod:`~basiclife.BasicTerm_S` can also be compiled
by modelx-cython, it achieves only about twice the speed of its nomx model,
because it was not written to take full advantage of Cython optimizations.

The :mod:`~basiclife.BasicTerm_SC` model thus serves as an example of
how to optimize a modelx model for generating a fast compiled version.


Optimization Strategy
---------------------

:mod:`~basiclife.BasicTerm_SC` is derived from :mod:`~basiclife.BasicTerm_S` by applying the following changes
to make its cythonized model run faster:

* **Use of primitive types**
  To accelerate cash flow projection over a large number of model points,
  high-level Python objects (such as strings, lists, dictionaries, and pandas DataFrames)
  are removed from the :mod:`~basiclife.BasicTerm_SC.Projection` space.
  Formulas in that space are instead written to operate primarily on primitive numeric types,
  such as ``int`` and ``float``.

* **Separate data and projection**
  Cells for reading input data from files have been moved to the :mod:`~basiclife.BasicTerm_SC.Data` space.
  Input data (such as policy attributes) is held in NumPy arrays instead of pandas DataFrames.

* **Parameterize with array indices**
  The :mod:`~basiclife.BasicTerm_SC.Projection` space is parameterized by an array index,
  :attr:`~basiclife.BasicTerm_SC.Projection.idx`
  (rather than ``point_id``) to identify model points.
  :attr:`~basiclife.BasicTerm_SC.Projection.idx` is used as a key
  to look up the value of the selected model point in the arrays of policy attributes.


Basic Usage
-----------

This section explains the steps to create the cythonized version of the *BasicTerm_SC* model.

Install C compiler, Cython, and modelx-cython
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to lifelib and modelx, you need to install Cython and modelx-cython.
Because Cython requires a C compiler, install one if necessary by following the
instructions in Cython's official documentation.

Then install Cython and modelx-cython using pip::

    > pip install Cython

    > pip install modelx-cython

Or using conda, if you're using Anaconda::

    > conda install Cython

    > conda install modelx-cython


Copy the basiclife library
^^^^^^^^^^^^^^^^^^^^^^^^^^

Create your own copy of the *basiclife* library by following
the steps in the :doc:`/quickstart/index` page.
Within the copied folder, you will find a *BasicTerm_SC* subfolder that contains the model.

Because *BasicTerm_SC* is a modelx model, you can load and run it
from IPython or Spyder (with the spyder-modelx plugin).

For example, in IPython with your current directory set to the location of *BasicTerm_SC*::

    >>> import modelx as mx

    >>> model = mx.read_model("BasicTerm_SC")

If you're using Spyder, open the *MxExplorer* pane, right-click on an empty area,
choose *Read Model*, then select the *BasicTerm_SC* folder.


Export and compile the model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, export the modelx model to create a pure-Python (nomx) model.
Use the ``export`` method on the model object as follows (IPython example)::

    >>> model.export("BasicTerm_SC_nomx")

This command exports the model as a Python package named "BasicTerm_SC_nomx" in the current directory.

You can test the exported (nomx) model by importing it and accessing its cells. For instance::

    >>> from BasicTerm_SC_nomx import mx_model

    >>> mx_model.Projection[0].result_pv()

    >>> mx_model.Projection[9999].result_pv()

(Here, ``mx_model`` is the nomx model object.)


Cythonize the model
^^^^^^^^^^^^^^^^^^^

The modelx-cython package provides a shell command named ``mx2cy``.
To generate a compiled version of :mod:`~basiclife.BasicTerm_SC`, change to the
directory containing the exported nomx model (e.g., the folder with *BasicTerm_SC_nomx*)
and run::

    > mx2cy BasicTerm_SC

To see help options, run::

    > mx2cy --help

    usage: mx2cy [-h] [--sample SAMPLE] [--spec SPEC] [--setup SETUP] [--translate-only | --compile-only] model_path

    Translate an exported modelx model into Cython and compile it.

    positional arguments:
      model_path        Path to an exported modelx model to translate into Cython

    options:
      -h, --help        show this help message and exit
      --sample SAMPLE   Path to a sample file to run for collecting type information (default: sample.py)
      --spec SPEC       Path to a spec file for setting parameters (default: spec.py)
      --setup SETUP     Path to a setup file for Cython (default: setup.py)
      --translate-only  Perform translation only (default: False)
      --compile-only    Perform compilation only (default: False)

The ``mx2cy`` command requires two files, ``sample.py`` and ``spec.py``, both included in
the *basiclife* library. When run, ``mx2cy`` does the following:

1. Executes ``sample.py`` to collect run-time type information for ``BasicTerm_SC_nomx``.
2. Outputs a folder *BasicTerm_SC_nomx_cy*, containing Cython-translated files.
3. Compiles the translated files into a binary module using Cython, producing the compiled model
   in *BasicTerm_SC_nomx_cy*.


Test the compiled model
^^^^^^^^^^^^^^^^^^^^^^^

Use the ``run_sc.py`` script to test speed and memory usage. For the compiled (Cython) model::

    > python run_sc.py --cython
    {'value': 1448.9630534601538, 'mem_use': 477.5078125, 'time': 1.5274626000027638}

For comparison, run the nomx version::

    > python run_sc.py --nomx
    {'value': 1448.9630534601563, 'mem_use': 2050.42578125, 'time': 11.355696699989494}

The script calculates the present value of net cash flows for 10,000 model points
and outputs the total present value, the maximum memory usage, and the time taken.


Model Specifications
--------------------

:mod:`~basiclife.BasicTerm_SC` consists of two spaces: :mod:`~basiclife.BasicTerm_SC.Data`
and :mod:`~basiclife.BasicTerm_SC.Projection`.

- The :mod:`~basiclife.BasicTerm_SC.Data` space contains references to input files and cells
  for loading input data. In :mod:`~basiclife.BasicTerm_S`, these tasks were done in the Projection space.
  In *BasicTerm_SC*, the model point table is kept as a pandas DataFrame in
  :attr:`~basiclife.BasicTerm_SC.Data.model_point_table`, and each attribute (e.g., `policy_term`)
  is stored in a NumPy array. The NumPy array index is used for identifying model points.

- The :mod:`~basiclife.BasicTerm_SC.Projection` space contains the projection logic for a
  single model point, parameterized by an array index
  :attr:`~basiclife.BasicTerm_SC.Projection.idx` (instead of ``point_id``).
  Formulas here reference the NumPy arrays in :mod:`~basiclife.BasicTerm_SC.Data`.


The Data Space
^^^^^^^^^^^^^^

.. automodule:: basiclife.BasicTerm_SC.Data

Model point data
~~~~~~~~~~~~~~~~

The model point data is stored in an Excel file named *model_point_table.xlsx*
under the library directory.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~age_at_entry
   ~sex
   ~policy_term
   ~policy_count
   ~point_id
   ~sum_assured

Assumption data
~~~~~~~~~~~~~~~

The mortality table is stored in *mort_table.xlsx* under the model folder and read
into :attr:`mort_table` as a DataFrame. :func:`mort_table_array` converts this DataFrame
into a NumPy array, adding rows filled with ``nan`` to align row indices with ages.
:func:`mort_table_array` is then used by
:func:`~basiclife.BasicTerm_SC.Projection.mort_rate` in the Projection space.

The discount rate data is stored in *disc_rate_ann.xlsx* under the model folder
and read into :attr:`disc_rate_ann` as a Series, which is then converted into a NumPy array.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~mort_table_array
   ~disc_rate_ann_array


The Projection Space
^^^^^^^^^^^^^^^^^^^^

.. automodule:: basiclife.BasicTerm_SC.Projection

Projection parameters
~~~~~~~~~~~~~~~~~~~~~

This model represents new business, with all model points issued at time 0. The
time step is monthly. Cash flows and other time-dependent variables are indexed by ``t``.

Flows that accumulate throughout period ``t`` (until ``t+1``) have indices ``t``,
while balance items indexed by ``t`` represent the value at that exact time.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~proj_len
   ~duration

Model point data
~~~~~~~~~~~~~~~~

The same *model_point_table.xlsx* file under the model folder is referenced to obtain
model point data such as ages, sum assured, and terms.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~age
   ~age_at_entry
   ~sex
   ~sum_assured
   ~policy_term

Assumptions
~~~~~~~~~~~

:func:`mort_rate` reads annual mortality rates from
:func:`~basiclife.BasicTerm_SC.Data.mort_table_array`
in :mod:`~basiclife.BasicTerm_SC.Data` and converts them to monthly rates via
:func:`mort_rate_mth`.

:func:`disc_rate_mth` reads annual discount rates from
:func:`~basiclife.BasicTerm_SC.Data.disc_rate_ann_array` in :mod:`~basiclife.BasicTerm_SC.Data`
and converts them to monthly discount factors via :func:`disc_factor`.

:func:`lapse_rate` is defined as a simple function of policy duration.
:func:`expense_acq` is the acquisition expense per policy at ``t=0``,
and :func:`expense_maint` is the annual maintenance expense per policy,
inflated at a constant rate (:func:`inflation_rate`).

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~mort_rate
   ~mort_rate_mth
   ~disc_factor
   ~disc_rate_mth
   ~lapse_rate
   ~expense_acq
   ~expense_maint
   ~inflation_factor
   ~inflation_rate

Policy values
~~~~~~~~~~~~~

By default, the death benefit for each policy (:func:`claim_pp`) equals :attr:`sum_assured`.
All model points pay monthly premiums for the entire policy term.

The monthly premium per policy (:func:`premium_pp`) is calculated as
``(1 + loading_prem) * net_premium_pp``,
where the net premium is set so that the present value of net premiums equals
the present value of claims. This product has no surrender value.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~claim_pp
   ~net_premium_pp
   ~loading_prem
   ~premium_pp

Policy decrement
~~~~~~~~~~~~~~~~

Initially, each model point is assumed to have one policy in force. The in-force
policies decrease by lapses and deaths each month, and any remaining policies at
the end of the policy term reach maturity and exit.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~pols_death
   ~pols_if
   ~pols_if_init
   ~pols_lapse
   ~pols_maturity

Cashflows
~~~~~~~~~

Cashflows consist of acquisition expenses at ``t=0``, maintenance expenses thereafter,
commissions, premiums, and claims. Commissions are assumed to be 100% of premium during
the first policy year and zero afterward.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~claims
   ~commissions
   ~premiums
   ~expenses
   ~net_cf

Present values
~~~~~~~~~~~~~~

Cells whose names begin with ``pv_`` compute present values of various flows.
Although :func:`pols_if` is not itself a cashflow, it is used as an annuity factor
in :func:`net_premium_pp`.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~pv_claims
   ~pv_commissions
   ~pv_expenses
   ~pv_net_cf
   ~pv_pols_if
   ~pv_premiums
   ~check_pv_net_cf

Results
~~~~~~~

:func:`result_cf` returns a DataFrame of monthly cashflows and decrements for a
selected model point::

    >>> result_cf()
          Premiums     Claims  ...  Policies Death  Policies Exits
    0    94.840000  34.180793  ...        0.000055        0.008742
    1    94.005734  33.880120  ...        0.000054        0.008665
    2    93.178806  33.582091  ...        0.000054        0.008588
    3    92.359153  33.286684  ...        0.000054        0.008513
    4    91.546710  32.993876  ...        0.000053        0.008438
    ..         ...        ...  ...             ...             ...
    116  62.432465  63.534771  ...        0.000102        0.001107
    117  62.317757  63.418038  ...        0.000102        0.001105
    118  62.203260  63.301519  ...        0.000102        0.001103
    119  62.088973  63.185215  ...        0.000102        0.001101
    120   0.000000   0.000000  ...        0.000000        0.000000

    [121 rows x 8 columns]


:func:`result_pv` returns the present values of these cashflows,
along with each flow’s percentage relative to the present value of premiums::

    >>> result_pv()
                  Premiums       Claims    Expenses  Commissions  Net Cashflow
    PV         8251.931435  5501.074678  748.303591  1084.601434    917.951731
    % Premium     1.000000     0.666641    0.090682     0.131436      0.111241

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv