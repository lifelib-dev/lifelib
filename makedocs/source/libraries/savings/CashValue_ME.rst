.. module:: savings.CashValue_ME

The **CashValue_ME** Model
==========================

.. _DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
.. _Series: https://pandas.pydata.org/docs/reference/api/pandas.Series.html

.. py:currentmodule:: savings.CashValue_ME.Projection

Overview
-----------

The :mod:`~savings.CashValue_ME` model is a faster reimplementation of
the :mod:`~savings.CashValue_SE` model.

The :mod:`~savings.CashValue_ME` model reproduces the same results as
:mod:`~savings.CashValue_SE`, but is more suitable for
processing a large number of model points.
Each formula to be applied to all the model points
operates on the entire set of model points at once
with the help of Numpy and Pandas.

The default product specs, assumptions and input data
are the same as :mod:`~savings.CashValue_SE`.

Changes from **CashValue_SE**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:currentmodule:: savings.CashValue_ME.Projection

Below is the list of
Cells and References that are newly added or
updated from :mod:`~savings.CashValue_SE`.

* :func:`check_av_roll_fwd`
* :func:`check_margin`
* :func:`check_pv_net_cf`
* :func:`disc_factors`
* :func:`disc_rate_mth`
* :func:`lapse_rate`
* :attr:`max_proj_len` <new>
* :func:`model_point`
* :func:`mort_rate`
* :func:`mort_table_reindexed` <new>
* :func:`net_amt_at_risk`
* :func:`policy_term`
* :func:`pols_if_init`
* :func:`pols_maturity`
* :func:`pols_new_biz`
* :func:`premium_pp`
* :func:`proj_len`
* :func:`pv_av_change`
* :func:`pv_claims`
* :func:`pv_commissions`
* :func:`pv_expenses`
* :func:`pv_inv_income`
* :func:`pv_expenses`
* :func:`pv_pols_if`
* :func:`pv_premiums`
* :func:`result_cf`
* :func:`result_pols`
* :func:`result_pv`
* :func:`surr_charge_rate`
* :func:`surr_charge_table_stacked`
* :func:`surr_charge_max_idx`


Running with 10000 model points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main advantage of the :mod:`~savings.CashValue_ME` model over the
:mod:`~savings.CashValue_SE` model is its speed.
By default, :mod:`~savings.CashValue_ME` is configured
to run the same 4 model points as the ones in :mod:`~savings.CashValue_SE`,
but a larger table of 10000 model points is also included in the model.
The larger model point table is saved in the model folder
as an Excel file named *model_point_10000.xlsx*,
and this table is read into the model as
a DataFrame named :attr:`model_point_10000`.
The 10000 model points are all new business at time 0, and
created by modifying the sample model points in :mod:`basiclife`.

To run the model with the larger model point table,
assign the table to :attr:`model_point_table`::

   >>> Projection.model_point_table = Projection.model_point_10000

In the code above, ``Projection`` must be defined beforehand to
refer to the :mod:`~savings.CashValue_ME.Projection` space.

Below is the speed result of running the entire 10000 model points
on a consumer PC equipped
with `Intel Core i5-6500T`_ CPU and 16GB RAM.

.. _Intel Core i5-6500T: https://ark.intel.com/content/www/us/en/ark/products/88183/intel-core-i5-6500t-processor-6m-cache-up-to-3-10-ghz.html

.. code-block::
   :caption: 10000 model points with CashValue_ME without split by product

   >>> timeit.timeit("Projection.result_pv()", globals=globals(), number=1)
   34.3045132

   >>> Projection.result_pv()
                  Premiums         Death  ...  Change in AV  Net Cashflow
   policy_id                              ...
   1          5.349200e+07  4.852612e+05  ...  4.465141e+06  1.881696e+06
   2          4.446054e+07  1.356468e+07  ...  1.604824e+07  1.177058e+07
   3          1.210841e+08  7.179706e+07  ...  2.796228e+07  2.192224e+07
   4          3.038400e+07  2.938897e+05  ...  4.840159e+06  4.346383e+06
   5          5.989500e+07  3.342985e+05  ...  7.238519e+06  7.671440e+06
                   ...           ...  ...           ...           ...
   9996       2.067500e+07  5.335816e+05  ...  3.627718e+06  1.951471e+06
   9997       6.690600e+07  4.291283e+05  ...  8.984202e+06  4.590207e+06
   9998       7.629662e+06  4.007463e+06  ...  1.982635e+06  1.441142e+06
   9999       2.835552e+06  1.258307e+06  ...  8.583928e+05  4.917449e+05
   10000      1.513202e+07  3.834462e+06  ...  6.555234e+06  3.667102e+06

   [10000 rows x 9 columns]

The above run projects all model points for the max length
of the entire model points::

   >>> Projection.max_proj_len()
   1141

Since product A and B are limited term up to 20 years
and C and D are whole life,
it may be more efficient to run the limited term and whole life model
points separately,
because the limited term model points don't need as long the length
of projection period as C and D model points.
You can do so by defining, for example, ``seg_id`` to
filter model points in the formula of :func:`model_point`.
The code below is an example of the modified formula of :func:`model_point`
to filter the model points by ``seg_id``::

   >>> Projection.model_point.formula
   def model_point():
       """"Target model points
       ...
       """
       cond = model_point_table_ext()['is_wl'] == (True if seg_id == 'WL' else False)
       return model_point_table_ext().loc[cond]

Assigning ``"WL"`` to ``seg_id`` results in running only whole life model points,
while assigning anything other than ``"WL"`` results in running
limited term model points::

   >>> Projection.seg_id = 'WL'

   >>> timeit.timeit("Projection.result_pv()", globals=globals(), number=1)
   24.311953799999998

   >>> Projection.result_pv()
                  Premiums         Death  ...  Change in AV  Net Cashflow
   policy_id                              ...
   2          4.446054e+07  1.356468e+07  ...  1.604824e+07  1.177058e+07
   3          1.210841e+08  7.179706e+07  ...  2.796228e+07  2.192224e+07
   6          5.051520e+06  3.011482e+06  ...  1.152065e+06  4.933033e+04
   9          5.537287e+07  3.686858e+07  ...  1.126645e+07  7.784990e+06
   10         2.957650e+07  1.156441e+07  ...  9.877157e+06  6.451814e+06
                   ...           ...  ...           ...           ...
   9988       5.051377e+05  1.692807e+05  ...  1.715821e+05  1.065215e+05
   9989       2.889266e+07  1.769398e+07  ...  5.681889e+06  4.869589e+06
   9998       7.629662e+06  4.007463e+06  ...  1.982635e+06  1.441142e+06
   9999       2.835552e+06  1.258307e+06  ...  8.583928e+05  4.917449e+05
   10000      1.513202e+07  3.834462e+06  ...  6.555234e+06  3.667102e+06

   [5015 rows x 9 columns]

   >>> Projection.max_proj_len()
   1141

   >>> Projection.seg_id = 'NWL'

   >>> timeit.timeit("Projection.result_pv()", globals=globals(), number=1)
   5.201247100000003

   >>> Projection.result_pv()
                Premiums          Death  ...  Change in AV  Net Cashflow
   policy_id                             ...
   1          53492000.0  485261.238999  ...  4.465141e+06  1.881696e+06
   4          30384000.0  293889.696238  ...  4.840159e+06  4.346383e+06
   5          59895000.0  334298.511514  ...  7.238519e+06  7.671440e+06
   7          42066000.0  337495.895163  ...  3.513768e+06  1.355059e+06
   8           5270000.0   85955.434866  ...  7.032080e+05 -2.137742e+05
                 ...            ...  ...           ...           ...
   9993        1116000.0    6862.126164  ...  1.498832e+05  6.988384e+04
   9994       22050000.0  765048.795780  ...  3.453998e+06  3.159848e+06
   9995        3420000.0   24997.118829  ...  6.067274e+05 -4.430946e+04
   9996       20675000.0  533581.639585  ...  3.627718e+06  1.951471e+06
   9997       66906000.0  429128.288942  ...  8.984202e+06  4.590207e+06

   [4985 rows x 9 columns]

   >>> Projection.max_proj_len()
   1141

To keep the results for both ``"WL"`` and ``"NWL"``,
you can parameterize :mod:`~savings.CashValue_ME.Projection`
with ``seg_id`` and have ``Projection['WL']`` and ``Projection['NWL']``
as dynamic child spaces of :mod:`~savings.CashValue_ME.Projection`::

   >>> Projection.parameters = ("seg_id",)

   >>> Projection['WL'].model_point()
             spec_id  age_at_entry sex  ...  surr_charge_id  load_prem_rate  is_wl
   policy_id                            ...
   2               C            29   M  ...             NaN            0.10   True
   3               D            51   F  ...          type_3            0.05   True
   6               D            51   F  ...          type_3            0.05   True
   9               D            59   F  ...          type_3            0.05   True
   10              D            35   F  ...          type_3            0.05   True
             ...           ...  ..  ...             ...             ...    ...
   9988            C            32   M  ...             NaN            0.10   True
   9989            C            56   M  ...             NaN            0.10   True
   9998            D            45   F  ...          type_3            0.05   True
   9999            D            39   M  ...          type_3            0.05   True
   10000           D            22   F  ...          type_3            0.05   True

   [5015 rows x 14 columns]

   >>> Projection['WL'].result_pv()
                  Premiums         Death  ...  Change in AV  Net Cashflow
   policy_id                              ...
   2          4.446054e+07  1.356468e+07  ...  1.604824e+07  1.177058e+07
   3          1.210841e+08  7.179706e+07  ...  2.796228e+07  2.192224e+07
   6          5.051520e+06  3.011482e+06  ...  1.152065e+06  4.933033e+04
   9          5.537287e+07  3.686858e+07  ...  1.126645e+07  7.784990e+06
   10         2.957650e+07  1.156441e+07  ...  9.877157e+06  6.451814e+06
                   ...           ...  ...           ...           ...
   9988       5.051377e+05  1.692807e+05  ...  1.715821e+05  1.065215e+05
   9989       2.889266e+07  1.769398e+07  ...  5.681889e+06  4.869589e+06
   9998       7.629662e+06  4.007463e+06  ...  1.982635e+06  1.441142e+06
   9999       2.835552e+06  1.258307e+06  ...  8.583928e+05  4.917449e+05
   10000      1.513202e+07  3.834462e+06  ...  6.555234e+06  3.667102e+06

   [5015 rows x 9 columns]

   >>> Projection['NWL'].model_point()
             spec_id  age_at_entry sex  ...  surr_charge_id  load_prem_rate  is_wl
   policy_id                            ...
   1               B            47   M  ...          type_1             0.0  False
   4               A            32   F  ...             NaN             0.1  False
   5               A            28   M  ...             NaN             0.1  False
   7               B            45   F  ...          type_1             0.0  False
   8               B            47   F  ...          type_1             0.0  False
             ...           ...  ..  ...             ...             ...    ...
   9993            B            29   M  ...          type_1             0.0  False
   9994            A            52   F  ...             NaN             0.1  False
   9995            B            24   M  ...          type_1             0.0  False
   9996            B            47   M  ...          type_1             0.0  False
   9997            B            30   M  ...          type_1             0.0  False

   [4985 rows x 14 columns]

   >>> Projection['NWL'].result_pv()
                Premiums          Death  ...  Change in AV  Net Cashflow
   policy_id                             ...
   1          53492000.0  485261.238999  ...  4.465141e+06  1.881696e+06
   4          30384000.0  293889.696238  ...  4.840159e+06  4.346383e+06
   5          59895000.0  334298.511514  ...  7.238519e+06  7.671440e+06
   7          42066000.0  337495.895163  ...  3.513768e+06  1.355059e+06
   8           5270000.0   85955.434866  ...  7.032080e+05 -2.137742e+05
                 ...            ...  ...           ...           ...
   9993        1116000.0    6862.126164  ...  1.498832e+05  6.988384e+04
   9994       22050000.0  765048.795780  ...  3.453998e+06  3.159848e+06
   9995        3420000.0   24997.118829  ...  6.067274e+05 -4.430946e+04
   9996       20675000.0  533581.639585  ...  3.627718e+06  1.951471e+06
   9997       66906000.0  429128.288942  ...  8.984202e+06  4.590207e+06

   [4985 rows x 9 columns]

While running the entire model points at once took 34 seconds,
running the whole life and limited term model points separately
took about 30 seconds in total.
The whole life segment is about half the size of the entire model points,
and takes 24 seconds, while the entire segment takes 34 seconds,
which implies
the processing speed per model point improves as
the number of model points gets larger.

Formula examples
^^^^^^^^^^^^^^^^

Most formulas in the :mod:`~savings.CashValue_ME` model
are the same as those in :mod:`~savings.CashValue_SE`.
However, some formulas are updated since they cannot
be applied to vector operations without change.
For example, below shows how
``pols_maturity``, the number of maturing policies
at time *t*, is defined differently in
:mod:`~savings.CashValue_SE` and in
:mod:`~savings.CashValue_ME`.

.. code-block:: python
   :caption: pols_maturity in CashValue_SE

   def pols_maturity(t):
       if duration_mth(t) == policy_term() * 12:
           return pols_if_at(t, "BEF_MAT")
       else:
           return 0

.. code-block:: python
   :caption: pols_maturity in CashValue_ME

    def pols_maturity(t):
        return (duration_mth(t) == policy_term() * 12) * pols_if_at(t, "BEF_MAT")

In :mod:`~savings.CashValue_SE`,
:func:`~savings.CashValue_SE.Projection.policy_term` returns an integer,
such as 10 indicating a policy term of the selected model point in years,
so the ``if`` clause checks if the value of :func:`~savings.CashValue_SE.Projection.duration_mth`
is equal to the policy term in month:

.. code-block:: python
   :caption: In CashValue_SE for model point 1

   >>> policy_term()
   10

   >>> pols_maturity(120)
   65.9357318577613

In contrast,  :func:`~policy_term` in :mod:`~savings.CashValue_ME` returns
a `Series`_ of policy terms of all the model points.
If the *if* clause were
defined in the same way as in the :mod:`~savings.CashValue_SE`,
it would result in an error,
because the condition ``duration_mth(t) == policy_term() * 12``  for a certain ``t``
returns a `Series`_ of boolean values and it is ambiguous
for the `Series`_ to be in the if condition.
Further more, whether the ``if`` branch or the ``else`` branch should
be evaluated needs to be determined element-wise,
but the ``if`` statement would not allow such element-wise branching.
Instead of using the ``if`` statement, the formula in :mod:`~savings.CashValue_ME`
achieves the element-wise conditional operation by multiplication
by a `Series`_ of boolean values.
In the formula in :mod:`~savings.CashValue_ME`,
``pols_if_at(t, "BEF_MAT")``
returns the numbers of policies at time t for all the model points
as a `Series`_.
Multiplying it
by ``(duration_mth(t) == policy_term() * 12)`` replaces
the numbers of policies with 0 for model points whose policy terms in month
are not equal to ``t``. This operation is effectively an element-wise if
operation:

.. code-block:: python
   :caption: In CashValue_ME at t=120

   >>> policy_term()
   poind_id
   1    10
   2    20
   3    95
   4    65
   dtype: int64


   >>> (duration_mth(120) == policy_term() * 12)
   poind_id
   1     True
   2    False
   3    False
   4    False
   dtype: bool


   >>> pols_maturity(120)
   1    65.935732
   2     0.000000
   3     0.000000
   4     0.000000
   dtype: float64


Basic Usage
-----------


Reading the model
^^^^^^^^^^^^^^^^^

Create your copy of the *savings* library by following
the steps on the :doc:`/quickstart` page.
The model is saved as the folder named :mod:`~savings.CashValue_ME` in the copied folder.

To read the model from Spyder, right-click on the empty space in *MxExplorer*,
and select *Read Model*.
Click the folder icon on the dialog box and select the
:mod:`~savings.CashValue_ME` folder.

Getting the results
^^^^^^^^^^^^^^^^^^^
By default, the model has Cells
for outputting projection results as listed in the
:ref:`basicterm_m-results` section.
:func:`~result_cf` outputs total cashflows of all the model points,
and :func:`~result_pv` outputs the present values of the cashflows
by model points.
Both Cells outputs the results as pandas `DataFrame`_.

By following the same steps explained in the :doc:`/quickstart` page
using this model,
You can get the results in an *MxConsole* and show
the results as tables in *MxDataViewer*.


Changing the model point
^^^^^^^^^^^^^^^^^^^^^^^^

By default, :func:`~model_point` returns the entire :func:`~model_point_table_ext`::

   >>> Projection.model_point.formula
   def model_point():
       return model_point_table_ext()

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=150;
     model_point[label="model_point()"];
     model_point_table_ext[label="model_point_table_ext()"];
     model_point -> model_point_table_ext;
     model_point_table_ext -> model_point_table;
     model_point_table_ext -> product_spec_table;
   }

The calculations in :mod:`~savings.CashValue_ME.Projection` apply to all the model points
in :attr:`~model_point_table`.
To limit the calculation target, change the :func:`~model_point` formula
so that :func:`~model_point` returns a `DataFrame`_ that contains
only the target rows.
For example, to select only the model point 1::

   >>> Projection.model_point.formula
   def model_point():
       return model_point_table_ext().loc[1:1]

There are many methods of `DataFrame`_ for selecting its rows.
See the `pandas documentation`_ for details.

.. _pandas documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

When selecting only one model point, make sure that :func:`~model_point`
returns the model point as a `DataFrame`_ not as a `Series`_.
In the code example above, ``model_point_table_ext().loc[1:1]``
is specified instead of ``model_point_table_ext().loc[1]``,
because ``model_point_table_ext().loc[1]`` would return the model point as a `Series`_.

Also, you should be careful not to accidentally update the original `DataFrame`_
held as :attr:`~model_point_table`.


Model Specifications
---------------------


The :mod:`~savings.CashValue_ME` model has only one UserSpace,
named :mod:`~savings.CashValue_ME.Projection`,
and all the Cells and References are defined in the space.

The Projection Space
^^^^^^^^^^^^^^^^^^^^

.. automodule:: savings.CashValue_ME.Projection


Projection parameters
^^^^^^^^^^^^^^^^^^^^^

This is a new business model and all model points are issued at time 0.
The time step of the model is monthly. Cashflows and other time-dependent
variables are indexed with ``t``.

Cashflows and other flows that accumulate throughout a period
indexed with ``t`` denotes the sums of the flows from ``t`` til ``t+1``.
Balance items indexed with ``t`` denotes the amount at ``t``.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~proj_len
    ~max_proj_len


Model point data
^^^^^^^^^^^^^^^^^^

The model point data is stored in an Excel file named *model_point_table.xlsx*
under the model folder.


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~model_point
   ~model_point_table_ext
   ~sex
   ~sum_assured
   ~policy_term
   ~age
   ~age_at_entry
   ~duration
   ~duration_mth
   ~has_surr_charge
   ~is_wl
   ~load_prem_rate
   ~surr_charge_id
   ~premium_type
   ~av_pp_init


Assumptions
^^^^^^^^^^^^^^^^^^

The mortality table is stored in an Excel file named *mort_table.xlsx*
under the model folder, and is read into :attr:`mort_table` as a `DataFrame`_.
:func:`mort_table_reindexed` returns a mortality table
reshaped from :attr:`mort_table`, which is a `Series`_
indexed with ``Age`` and ``Duration``.
:func:`mort_rate` looks up :func:`mort_table_reindexed` and picks up
the annual mortality rates to be applied for all the
model points at time ``t`` and returns them in a `Series`_.
:func:`mort_rate_mth` converts :func:`mort_rate` to the monthly mortality
rate to be applied during the month starting at time ``t``.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=100;
     mort_rate_mth[label="mort_rate_mth(t)"];
     mort_rate[label="mort_rate(t)"];
     mort_table_reindexed[width=150];
     mort_rate_mth -> mort_rate -> mort_table_reindexed -> mort_table
   }

The discount rate data is stored in an Excel file named *disc_rate_ann.xlsx*
under the model folder, and is read into :attr:`disc_rate_ann` as a `Series`_.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=120;
     disc_factors[label="disc_factors(t)"];
     disc_rate_mth[label="disc_rate_mth(t)"];
     disc_factors -> disc_rate_mth -> disc_rate_ann
   }

The lapse by duration is defined by a formula in :func:`lapse_rate`.
:func:`expense_acq` holds the acquisition expense per policy at `t=0`.
:func:`expense_maint` holds the maintenance expense per policy per annum.
The maintenance expense inflates at a constant rate
of inflation given as :func:`inflation_rate`.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~mort_table_last_age
   ~mort_rate
   ~mort_rate_mth
   ~mort_table_reindexed
   ~disc_factors
   ~disc_rate_mth
   ~lapse_rate
   ~expense_acq
   ~expense_maint
   ~inflation_factor
   ~inflation_rate


Policy values
^^^^^^^^^^^^^^^^^^

By default, the amount of death benefit for each policy (:func:`claim_pp`)
is set equal to :attr:`sum_assured`.

:func:`premium_pp` is the single premium amount if the model point
represents single premium policies (i.e. :func:`premium_type` is ``"SINGLE"``),
or the monthly premium amount if the model point represents
level premium policies (i.e. :func:`premium_type` is ``"LEVEL"``).

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~claim_pp
   ~premium_pp
   ~maint_fee_rate
   ~coi_rate
   ~surr_charge_rate
   ~surr_charge_table_stacked
   ~surr_charge_max_idx


Policy decrement
^^^^^^^^^^^^^^^^^^

The policy decrement logic of :mod:`~savings.CashValue_ME`
is based on that of :mod:`~savings.CashValue_SE`.
except that each relevant formula operates on the entire model points.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~pols_death
   ~pols_if
   ~pols_if_at
   ~pols_if_init
   ~pols_lapse
   ~pols_maturity
   ~pols_new_biz

Account Value
^^^^^^^^^^^^^^^^

The account value logic of :mod:`~savings.CashValue_ME`
is based on :mod:`~savings.CashValue_SE`.
except that each relevant formula operates on the entire model points.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~inv_income
   ~inv_income_pp
   ~inv_return_mth
   ~inv_return_table
   ~av_pp_at
   ~net_amt_at_risk
   ~coi_pp
   ~prem_to_av_pp
   ~maint_fee_pp
   ~av_at
   ~prem_to_av
   ~claims_from_av
   ~claims_over_av
   ~coi
   ~maint_fee
   ~av_change
   ~check_av_roll_fwd


Cashflows
^^^^^^^^^^^^^^^^^^

Cashflows are calculated as its per-policy amount times the number
of policies.

The expense cashflow consists of acquisition expenses at issue
and monthly maintenance expenses spent each month.

By default, commissions are defined as 5% premiums.


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~surr_charge
   ~claims
   ~commissions
   ~premiums
   ~expenses
   ~net_cf


Margin Analysis
^^^^^^^^^^^^^^^^

:func:`~net_cf` can be expressed as the sum of expense and mortality
margins. The expense margin is defined as the sum of
premium loading, surrender charge and maintenance fees
net of commissions and expenses.
The mortality margin is defined :func:`coi` net of :func:`claims_over_av`.


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~margin_expense
   ~margin_mortality
   ~check_margin


Present values
^^^^^^^^^^^^^^^^^^

The Cells whose names start with ``pv_`` are for calculating
the present values of the cashflows indicated by the rest of their names.
:func:`pv_pols_if` is not used
in :mod:`~savings.CashValue_SE` and :mod:`~basiclife.BasicTerm_ME`.

.. autosummary::
  :toctree: ../generated/
  :template: mxbase.rst

  ~pv_claims
  ~pv_commissions
  ~pv_expenses
  ~pv_net_cf
  ~pv_pols_if
  ~pv_premiums
  ~pv_av_change
  ~pv_inv_income
  ~check_pv_net_cf


.. _cashvalue_me-results:

Results
^^^^^^^^^^^^^^^^^^

:func:`result_cf` outputs the total cashflows of all the model points
as a `DataFrame`_::

      >>> result_cf()
                Premiums         Claims      Expenses   Commissions  Net Cashflow
      0     1.002000e+08  795274.520511  2.016667e+06  5.010000e+06 -1.888257e+06
      1     1.982432e+05  782659.768793  1.653397e+04  9.912161e+03  1.102781e+05
      2     1.965019e+05  776554.840116  1.640233e+04  9.825093e+03  1.083123e+05
      3     1.947758e+05  777512.879071  1.627174e+04  9.738790e+03  1.088861e+05
      4     1.930649e+05  770406.958695  1.614219e+04  9.653245e+03  1.082080e+05
                 ...            ...           ...           ...           ...
      1136  0.000000e+00       0.000000  0.000000e+00  0.000000e+00  0.000000e+00
      1137  0.000000e+00       0.000000  0.000000e+00  0.000000e+00  0.000000e+00
      1138  0.000000e+00       0.000000  0.000000e+00  0.000000e+00  0.000000e+00
      1139  0.000000e+00       0.000000  0.000000e+00  0.000000e+00  0.000000e+00
      1140  0.000000e+00       0.000000  0.000000e+00  0.000000e+00  0.000000e+00

      [1141 rows x 5 columns]


:func:`result_pv` outputs the present values of the cashflows by model points::

      >>> result_pv()
                    Premiums         Death  ...  Change in AV  Net Cashflow
      poind_id                              ...
      1         5.000000e+07  1.350327e+05  ...  3.771029e+06  4.957050e+06
      2         5.000000e+07  1.608984e+06  ...  8.740610e+06  4.241619e+06
      3         2.642236e+07  6.107771e+06  ...  1.104837e+07  6.058365e+06
      4         2.201418e+07  1.329419e+07  ...  4.763115e+06  2.514042e+06

      [4 rows x 9 columns]


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv
   ~result_pols


