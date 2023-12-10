.. module:: basiclife.BasicTerm_ME

The **BasicTerm_ME** Model
==========================

.. _DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
.. _Series: https://pandas.pydata.org/docs/reference/api/pandas.Series.html

.. py:currentmodule:: basiclife.BasicTerm_ME.Projection

Overview
-----------

The **BasicTerm_ME** model is a faster reimplementation of
the :mod:`~basiclife.BasicTerm_SE` model.

The :mod:`~basiclife.BasicTerm_ME` model reproduces the same results as
:mod:`~basiclife.BasicTerm_SE` much faster.
Each formula to be applied to all the model points
operates on the entire set of model points at once
with the help of Numpy and Pandas.

The default product specs, assumptions and input data
are the same as :mod:`~basiclife.BasicTerm_SE`.

Changes from **BasicTerm_M**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:currentmodule:: basiclife.BasicTerm_ME.Projection

Below is the list of
Cells and References that are newly added or updated from :mod:`~basiclife.BasicTerm_M`.

* :attr:`model_point_table`
* :attr:`premium_table` <new>
* :attr:`duration`
* :attr:`duration_mth` <new>
* :func:`expenses`
* :func:`mort_rate`
* :func:`mort_table_reindexed`
* :func:`pols_death`
* :func:`pols_if`
* :func:`pols_if_at` <new>
* :func:`pols_if_init`
* :func:`pols_lapse`
* :func:`pols_maturity`
* :func:`pols_new_biz` <new>
* :func:`pv_pols_if`
* :func:`premium_pp`
* :func:`premiums`
* :func:`proj_len`
* :func:`result_pols` <new>

In summary, below are the main changes
common to :mod:`~basiclife.BasicTerm_ME` and :mod:`~basiclife.BasicTerm_SE`.
Refer to the descritpion for :mod:`~basiclife.BasicTerm_SE` for
more details.

* :attr:`model_point_table` has the ``duration_mth`` column,
  to indicate the duration of the model point at time 0,

* :func:`pols_if_at(t, timing)<pols_if_at>` is introduced to allow
  multiple values for the number of policy in-force at the same time
  at different policy flow timing.

* :attr:`premium_table` holds premium rate data calculated outside the model.

Speed comparison
^^^^^^^^^^^^^^^^

The main advantage of the :mod:`~basiclife.BasicTerm_ME` model over the
:mod:`~basiclife.BasicTerm_SE` model is its speed.
Below is the result of a simple speed comparison between the two models.
The machine used for this comparison is a consumer PC equipped
with `Intel Core i5-6500T`_ CPU and 16GB RAM.

.. _Intel Core i5-6500T: https://ark.intel.com/content/www/us/en/ark/products/88183/intel-core-i5-6500t-processor-6m-cache-up-to-3-10-ghz.html


.. code-block::
   :caption: 100 model points with BasicTerm_SE

   >>> timeit.timeit("[Projection[i].pv_net_cf() for i in range(1, 101)]", globals=globals(), number=1)
   5.971486999999996

.. code-block::
   :caption: 10000 model points with BasicTerm_ME

   >>> timeit.timeit("pv_net_cf()", globals=globals(), number=1)
   3.9130262000000045

Note that only the first 100 model points were run with :mod:`~basiclife.BasicTerm_SE`
while all the 10000 model points were run with :mod:`~basiclife.BasicTerm_ME`.
While :mod:`~basiclife.BasicTerm_SE` took about 6.0 seconds for the 100 model points,
:mod:`~basiclife.BasicTerm_ME` took only 3.9 seconds for the 10000 model points.
This means :mod:`~basiclife.BasicTerm_ME`
runs about **153** times faster than :mod:`~basiclife.BasicTerm_SE`.
The run time of :mod:`~basiclife.BasicTerm_SE`
is shorter that :mod:`~basiclife.BasicTerm_S` because
the projection length of each model point is shorter for
:mod:`~basiclife.BasicTerm_SE`.

Formula examples
^^^^^^^^^^^^^^^^

Most formulas in the :mod:`~basiclife.BasicTerm_ME` model
are the same as those in :mod:`~basiclife.BasicTerm_SE`.
However, some formulas are updated since they cannot
be applied to vector operations without change.
For example, below shows how
``pols_maturity``, the number of maturing policies
at time *t*, is defined differently in
:mod:`~basiclife.BasicTerm_SE` and in
:mod:`~basiclife.BasicTerm_ME`.

.. code-block:: python
   :caption: pols_maturity in BasicTerm_SE

   def pols_maturity(t):
       if duration_mth(t) == policy_term() * 12:
           return pols_if_at(t, "BEF_MAT")
       else:
           return 0

.. code-block:: python
   :caption: pols_maturity in BasicTerm_ME

    def pols_maturity(t):
        return (duration_mth(t) == policy_term() * 12) * pols_if_at(t, "BEF_MAT")

In :mod:`~basiclife.BasicTerm_SE`,
:func:`~basiclife.BasicTerm_SE.Projection.policy_term` returns an integer,
such as 10 indicating a policy term of the selected model point in years,
so the ``if`` clause checks if the value of :func:`~basiclife.BasicTerm_SE.Projection.duration_mth`
is equal to the policy term in month:

.. code-block:: python
   :caption: In BasicTerm_SE for model point 1

   >>> policy_term()
   10

   >>> pols_maturity(120)
   0.6534679117893804

In contrast,  :func:`~policy_term` in :mod:`~basiclife.BasicTerm_ME` returns
a `Series`_ of policy terms of all the model points.
If the *if* clause were
defined in the same way as in the :mod:`~basiclife.BasicTerm_SE`,
it would result in an error,
because the condition ``duration_mth(t) == policy_term() * 12``  for a certain ``t``
returns a `Series`_ of boolean values and it is ambiguous
for the `Series`_ to be in the if condition.
Further more, whether the ``if`` branch or the ``else`` branch should
be evaluated needs to be determined element-wise,
but the ``if`` statement would not allow such element-wise branching.
Instead of using the ``if`` statement, the formula in :mod:`~basiclife.BasicTerm_ME`
achieves the element-wise conditional operation by multiplication
by a `Series`_ of boolean values.
In the formula in :mod:`~basiclife.BasicTerm_ME`,
``pols_if_at(t, "BEF_MAT")``
returns the numbers of policies at time t for all the model points
as a `Series`_.
Multiplying it
by ``(duration_mth(t) == policy_term() * 12)`` replaces
the numbers of policies with 0 for model points whose policy terms in month
are not equal to ``t``. This operation is effectively an element-wise if
operation:

.. code-block:: python
   :caption: In BasicTerm_ME at t=119

   >>> policy_term()
   point_id
   1        10
   2        20
   3        10
   4        20
   5        15
            ..
   9996     20
   9997     15
   9998     20
   9999     20
   10000    15
   Name: policy_term, Length: 10000, dtype: int64


   >>> (duration_mth(119) == policy_term() * 12)
   policy_id
   1         True
   2        False
   3        False
   4        False
   5        False

   9996     False
   9997     False
   9998     False
   9999     False
   10000    False
   Length: 10000, dtype: bool


   >>> pols_maturity(119)
   policy_id
   1        56.696979
   2         0.000000
   3         0.000000
   4         0.000000
   5         0.000000

   9996      0.000000
   9997      0.000000
   9998      0.000000
   9999      0.000000
   10000     0.000000
   Length: 10000, dtype: float64


Since projections for in-force policies do not start from their issuance,
the premium rates are calculated externaly by
:mod:`~basiclife.BasicTerm_M` and fed into the model as a table.
The premium rates are stored in *premium_table.xlsx* in the model folder
and read into :attr:`premium_table` as a Series.


Basic Usage
-----------


Reading the model
^^^^^^^^^^^^^^^^^

Create your copy of the *basiclife* library by following
the steps on the :doc:`/quickstart` page.
The model is saved as the folder named :mod:`~basiclife.BasicTerm_ME` in the copied folder.

To read the model from Spyder, right-click on the empty space in *MxExplorer*,
and select *Read Model*.
Click the folder icon on the dialog box and select the
:mod:`~basiclife.BasicTerm_ME` folder.

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

By default, :func:`~model_point` returns the entire :attr:`~model_point_table`::

   >>> Projection.model_point.formula
   def model_point():
       return model_point_table

.. figure:: /images/libraries/basiclife/BasicTerm_ME/diagram1.png

The calculations in :mod:`~basiclife.BasicTerm_ME.Projection` apply to all the model points
in :attr:`~model_point_table`.
To limit the calculation target, change the :func:`~model_point` formula
so that :func:`~model_point` returns a `DataFrame`_ that contains
only the target rows.
For example, to select only the model point 1::

   >>> Projection.model_point.formula
   def model_point():
       return model_point_table.loc[1:1]

There are many methods of `DataFrame`_ for selecting its rows.
See the `pandas documentation`_ for details.

.. _pandas documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

When selecting only one model point, make sure that :func:`~model_point`
returns the model point as a `DataFrame`_ not as a `Series`_.
In the code example above, ``model_point_table.loc[1:1]``
is specified instead of ``model_point_table.loc[1]``,
because ``model_point_table.loc[1]`` would return the model point as a `Series`_.

Also, you should be careful not to accidentally update the original `DataFrame`_
held as :attr:`~model_point_table`.


Model Specifications
---------------------


The :mod:`~basiclife.BasicTerm_ME` model has only one UserSpace,
named :mod:`~basiclife.BasicTerm_ME.Projection`,
and all the Cells and References are defined in the space.

The Projection Space
^^^^^^^^^^^^^^^^^^^^

.. automodule:: basiclife.BasicTerm_ME.Projection


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
   ~sex
   ~sum_assured
   ~policy_term
   ~age
   ~age_at_entry
   ~duration
   ~duration_mth


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

.. figure:: /images/libraries/basiclife/BasicTerm_ME/diagram2.png

The discount rate data is stored in an Excel file named *disc_rate_ann.xlsx*
under the model folder, and is read into :attr:`disc_rate_ann` as a `Series`_.

.. figure:: /images/libraries/basiclife/BasicTerm_ME/diagram3.png

The lapse by duration is defined by a formula in :func:`lapse_rate`.
:func:`expense_acq` holds the acquisition expense per policy at `t=0`.
:func:`expense_maint` holds the maintenance expense per policy per annum.
The maintenance expense inflates at a constant rate
of inflation given as :func:`inflation_rate`.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

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

The payment method is monthly whole term payment for all model points.
The monthly premium per policy  (:func:`premium_pp`)
is calculated for each policy
as (1 + :func:`loading_prem`) times :func:`net_premium_pp`.
The net premium is calculated so that the present value of the
net premiums equates to the present values of claims.

This product is assumed to have no surrender value.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~claim_pp
   ~net_premium_pp
   ~loading_prem
   ~premium_pp


Policy decrement
^^^^^^^^^^^^^^^^^^

The initial number of policies is set to 1 per model point by default,
and decreases through out the policy term by lapse and death.
At the end of the policy term the remaining number of policies
mature.

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


Cashflows
^^^^^^^^^^^^^^^^^^

An acquisition expense at t=0 and maintenance expenses thereafter
comprise expense cashflows.

Commissions are assumed to be paid out during the first year
and the commission amount is assumed to be 100% premium during the first
year and 0 afterwards.


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~claims
   ~commissions
   ~premiums
   ~expenses
   ~net_cf


Present values
^^^^^^^^^^^^^^^^^^

The Cells whose names start with ``pv_`` are for calculating
the present values of the cashflows indicated by the rest of their names.
:func:`pols_if` is not a cashflow, but used as annuity factors
in calculating :func:`net_premium_pp`.

.. autosummary::
  :toctree: ../generated/
  :template: mxbase.rst

  ~pv_claims
  ~pv_commissions
  ~pv_expenses
  ~pv_net_cf
  ~pv_pols_if
  ~pv_premiums


.. _basicterm_me-results:

Results
^^^^^^^^^^^^^^^^^^

:func:`result_cf` outputs the total cashflows of all the model points
as a `DataFrame`_::

      >>> result_cf()
               Premiums        Claims      Expenses   Commissions  Net Cashflow
      0    3.481375e+07  2.551366e+07  2.722470e+06  2.304871e+06  4.272750e+06
      1    3.458612e+07  2.533530e+07  2.777227e+06  2.271010e+06  4.202583e+06
      2    3.460642e+07  2.532024e+07  2.992697e+06  2.316894e+06  3.976592e+06
      3    3.446821e+07  2.526094e+07  2.816155e+06  2.308385e+06  4.082731e+06
      4    3.440382e+07  2.527465e+07  2.896164e+06  2.319160e+06  3.913840e+06
      ..            ...           ...           ...           ...           ...
      272  1.509838e+05  2.281406e+05  8.909740e+03  0.000000e+00 -8.606662e+04
      273  1.292070e+05  1.969228e+05  6.464827e+03  0.000000e+00 -7.418061e+04
      274  9.360930e+04  1.447365e+05  4.187218e+03  0.000000e+00 -5.531445e+04
      275  5.851123e+04  9.225161e+04  1.942107e+03  0.000000e+00 -3.568248e+04
      276  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00

      [277 rows x 5 columns]


:func:`result_pv` outputs the present values of the cashflows by model points::

      >>> result_pv()
                  PV Premiums      PV Claims  ...  PV Commissions  PV Net Cashflow
      policy_id                               ...
      1          7.083791e+05  474803.297001  ...    85874.887301    108798.061916
      2          9.950994e+04  109613.723658  ...        0.000000    -18305.709146
      3          1.104613e+06  802437.653322  ...        0.000000    266073.249126
      4          2.839117e+05  264723.616424  ...        0.000000    -18224.092562
      5          4.399130e+05  352234.521794  ...        0.000000     32214.118896
                      ...            ...  ...             ...              ...
      9996       3.574210e+05  405869.354038  ...        0.000000    -58052.929127
      9997       5.917467e+04   59908.482977  ...        0.000000     -5547.111546
      9998       1.314719e+05  141951.671002  ...        0.000000    -14790.802910
      9999       5.615703e+04   39215.159798  ...      372.420000      9219.186564
      10000      7.927437e+03    7433.441293  ...        0.000000      -752.642292

      [10000 rows x 5 columns]


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv
   ~result_pols


