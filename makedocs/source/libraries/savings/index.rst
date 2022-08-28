.. module:: savings

The **savings** Library
==========================

Overview
---------

The **savings** library is for
modeling savings products, such as universal life, unit-linked,
variable life and annuities.
These saving products have investment features. Most part of premiums
paid by the policyholder of such products is
kept as the account value of the policy.

The models in this library include the account value logic,
and differ from the :mod:`basiclife` models in the following points.

* In the :mod:`basiclife` models, premiums are calculated so that
  the present value of premiums cover the present value of
  claims. In the :mod:`savings` models, premiums are given as input,
  whether they are a single premium or recurring premiums.

* In the :mod:`savings` models, most part of the premium received from a
  policyholder is transferred to the account value. When the policy holder
  exits, whether by death, lapse or maturity, the account value
  of the policyholder is used to fund the claim paid to the policyholder.

* During each time step, the account value
  increases by the amount transferred from premiums,
  positive investment returns or interest credited,
  and decrease by the transferred amounts of claims, negative
  investment returns, and deducted fees. The beginning balance
  of the account value plus the changes in account value
  should reconcile to the ending balance of the account value.

* The death benefit amount is by default set equal to the
  premium amount, or the accumulated premium amount for recurring premium types
  of products. This spec should be customized by the user.
  When the account value increases above the premium amount,
  the account value is paid as the death benefit.
  By default, cost of insurance charges are deducted from the account value.

* The net cashflows of the saving models can be presented in two ways,
  gross of the account value and net of the account value.
  The gross presentation shows investment return on account value
  and change in account value, in addition to
  premiums, claims, expenses.
  The net presentation better depict the sources of profit and looses,
  and can be expressed as the sum of
  mortality margin adn expense margin.


The library currently includes 2 models.

.. toctree::
   :maxdepth: 1

   CashValue_SE
   CashValue_ME

:mod:`~savings.CashValue_SE` and :mod:`~savings.CashValue_ME`
produce the exact same results but in different ways.

The :mod:`~savings.CashValue_SE` model defines and executes formulas for each model point separately,
while the :mod:`~savings.CashValue_ME` model executes each formula at each time step
for all model points at once. They produce the same results for the same model point.
:mod:`~savings.CashValue_SE` is straight forward, and its formulas are easier to understand,
but it runs slower. It's suitable for validation purposes.
:mod:`~savings.CashValue_ME` runs fast, but its formulas are expressed as vector operations
and can be more complex in some places.

:mod:`~savings.CashValue_SE` and :mod:`~savings.CashValue_ME`
project the cashflows of in-force policies at time 0 as well as
new business policies at 0 or any future time.
:mod:`~savings.CashValue_ME` is to :mod:`~savings.CashValue_SE`
as :mod:`~basiclife.BasicTerm_M` is :mod:`~basiclife.BasicTerm_S`.
Formulas in :mod:`~savings.CashValue_ME` apply to all the model point
at a time while :mod:`~savings.CashValue_SE` carries out
projection for each model point separately.


How to Use the Library
------------------------------

As explained in the :ref:`create-a-project` section,
Create you own copy of the *savings* library.
For example, to copy as a folder named *savings*
under the path *C:\\path\\to\\your\\*, type below in an IPython console::

    >>> import lifelib

    >>> lifelib.create("savings", r"C:\path\to\your\savings")


Examples
-----------

.. toctree::
   :maxdepth: 1

   /libraries/notebooks/savings/savings_example1.ipynb
   /libraries/notebooks/savings/savings_example2.ipynb
   /libraries/notebooks/savings/savings_example3.ipynb



Library Contents
------------------

.. table::
   :widths: 20 80

   ========================================= ===============================================================
   File or Folder                            Description
   ========================================= ===============================================================
   CashValue_SE                              The :mod:`~savings.CashValue_SE` model.
   CashValue_ME                              The :mod:`~savings.CashValue_ME` model.
   cash_value_sample.xlsx                    An Excel file that reproduces the results of a selected model point. The file also shows the derivation of the sample mortality rates.
   CashValue_ME_EX1                          The example model for *savings_example1.ipynb*
   CashValue_ME_EX2                          The example model for *savings_example2.ipynb*
   savings_example1.ipynb                    Jupyter notebook :doc:`/libraries/notebooks/savings/savings_example1`
   savings_example2.ipynb                    Jupyter notebook :doc:`/libraries/notebooks/savings/savings_example2`
   savings_example3.ipynb                    Jupyter notebook :doc:`/libraries/notebooks/savings/savings_example3`
   generate_100K_model_points.ipynb          Jupyter notebook used for generating the large model point data for :doc:`/libraries/notebooks/savings/savings_example3`.
   plot_ex1_av_paths.py                      Python script for :doc:`/generated_examples/savings/plot_ex1_av_paths`
   plot_ex1_rand.py                          Python script for :doc:`/generated_examples/savings/plot_ex1_rand`
   plot_ex1_option_value.py                  Python script for :doc:`/generated_examples/savings/plot_ex1_option_value`
   plot_ex2_comp_option_values.py            Python script for :doc:`/generated_examples/savings/plot_ex2_comp_option_values`
   plot_ex2_lapse_decrement.py               Python script for :doc:`/generated_examples/savings/plot_ex2_lapse_decrement`
   plot_ex2_av_to_pols.py                    Python script for :doc:`/generated_examples/savings/plot_ex2_av_to_pols`
   ========================================= ===============================================================


Other Notebooks
----------------

.. toctree::
   :maxdepth: 1

   /libraries/notebooks/savings/generate_100K_model_points.ipynb



