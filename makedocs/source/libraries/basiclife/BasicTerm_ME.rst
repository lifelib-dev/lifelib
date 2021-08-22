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

duration
<new> duration_mth
expenses
mort_rate
mort_rate_reindexed
net_premium_pp
pols_death
pols_if
pols_if_at
pols_if_init
pols_lapse
pols_maturity
pols_new_biz
pv_pols_if
premiums
proj_len
<new> result_pols


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

   >>> timeit.timeit("[Projection[i].pv_net_cf() for i in range(1, 101)]",globals=globals(), number=1)
   7.6481730999998945

.. code-block::
   :caption: 10000 model points with BasicTerm_ME

   >>> timeit.timeit("pv_net_cf()",globals=globals(), number=1)
   1.3366562999999587

Note that only the first 100 model points were run with :mod:`~basiclife.BasicTerm_SE`
while all the 10000 model points were run with :mod:`~basiclife.BasicTerm_ME`.
While :mod:`~basiclife.BasicTerm_SE` took about 7.6 seconds for the 100 model points,
:mod:`~basiclife.BasicTerm_ME` took only 1.3 seconds for the 10000 model points.
This means :mod:`~basiclife.BasicTerm_ME`
runs about **580** times faster than :mod:`~basiclife.BasicTerm_SE`.


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
        if t == policy_term() * 12:
            return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)
        else:
            return 0

.. code-block:: python
   :caption: pols_maturity in BasicTerm_ME

    def pols_maturity(t):
        return (t == policy_term() * 12) * (pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1))

In :mod:`~basiclife.BasicTerm_SE`,
:func:`~basiclife.BasicTerm_SE.Projection.pols_maturity` returns an integer,
such as 10 indicating a policy term of the selected model point in years,
so the ``if`` clause checks if the value of ``t``
is equal to the policy term in month:

.. code-block:: python
   :caption: In BasicTerm_SE for model point 1

   >>> policy_term()
   120

   >>> pols_maturity(120)
   0.6534679117893804

In contrast,  :func:`~policy_term` in :mod:`~basiclife.BasicTerm_ME` returns
a `Series`_ of policy terms of all the model points.
If the *if* clause were
defined in the same way as in the :mod:`~basiclife.BasicTerm_SE`,
it would result in an error,
because the condition ``t == policy_term() * 12``  for a certain ``t``
returns a `Series`_ of boolean values and it is ambiguous
for the `Series`_ to be the if condition.
Further more, whether the ``if`` branch or the ``else`` branch should
be evaluated needs to be determined element-wise,
but the ``if`` statement would not allow such element-wise branching.
Instead of using the ``if`` statement, the formula in :mod:`~basiclife.BasicTerm_ME`
achieves the element-wise conditional operation by multiplication
by a `Series`_ of boolean values.
In the formula in :mod:`~basiclife.BasicTerm_ME`,
``(pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1))``
returns the numbers of policies at time t for all the model points
as a `Series`_.
Multiplying it
by ``(t == policy_term() * 12)`` replaces
the numbers of policies with 0 for model points whose policy terms in month
are not equal to ``t``. This operation is effectively an element-wise if
operation:

.. code-block:: python
   :caption: In BasicTerm_ME

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


   >>> (120 == policy_term() * 12)
   point_id
   1         True
   2        False
   3         True
   4        False
   5        False

   9996     False
   9997     False
   9998     False
   9999     False
   10000    False
   Name: policy_term, Length: 10000, dtype: bool


   >>> pols_maturity(120)
   point_id
   1        0.653468
   2        0.000000
   3        0.650917
   4        0.000000
   5        0.000000

   9996     0.000000
   9997     0.000000
   9998     0.000000
   9999     0.000000
   10000    0.000000
   Length: 10000, dtype: float64



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

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=120;
     model_point[label="model_point()"];
     model_point -> model_point_table
   }

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


Assumptions
^^^^^^^^^^^^^^^^^^

The mortality table is stored in an Excel file named *mort_table.xlsx*
under the model folder, and is read into :attr:`mort_table` as a `DataFrame`_.
:func:`mort_rate` looks up :attr:`mort_table` and picks up
the annual mortality rate to be applied for the selected
model point at time ``t``.
:func:`mort_rate_mth` converts :func:`mort_rate` to the monthly mortality
rate to be applied during the month starting at time ``t``.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=120;
     mort_rate_mth[label="mort_rate_mth(t)"];
     mort_rate[label="mort_rate(t)"];
     mort_rate_mth -> mort_rate -> mort_table
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

   ~mort_rate
   ~mort_rate_mth
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
   ~pols_if_init
   ~pols_lapse
   ~pols_maturity


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


.. _basicterm_m-results:

Results
^^^^^^^^^^^^^^^^^^

:func:`result_cf` outputs the total cashflows of all the model points
as a `DataFrame`_::

      >>> result_cf()
                Premiums         Claims      Expenses    Commissions  Net Cashflow
      0    828052.400000  240181.385376  3.000000e+06  828052.400000 -3.240181e+06
      1    820758.893595  238066.700397  4.956055e+04  820758.893595 -2.876273e+05
      2    813529.629362  235970.634461  4.912497e+04  813529.629362 -2.850956e+05
      3    806364.041439  233893.023631  4.869321e+04  806364.041439 -2.825862e+05
      4    799261.568951  231833.705414  4.826525e+04  799261.568951 -2.800990e+05
      ..             ...            ...           ...            ...           ...
      236  175639.935592  255080.430556  1.065127e+04       0.000000 -9.009177e+04
      237  175262.324017  254523.319976  1.063033e+04       0.000000 -8.989132e+04
      238  174885.540149  253967.449257  1.060943e+04       0.000000 -8.969133e+04
      239  174509.582137  253412.815586  1.058857e+04       0.000000 -8.949180e+04
      240       0.000000       0.000000  0.000000e+00       0.000000  0.000000e+00

      [241 rows x 5 columns]


:func:`result_pv` outputs the present values of the cashflows by model points::

      >>> result_pv()
                 PV Premiums     PV Claims  ...  PV Commissions  PV Net Cashflow
      point_id                              ...
      1          8251.931435   5501.074678  ...     1084.601434       917.951731
      2          8934.647903   5956.375886  ...      699.317588      1190.137329
      3         13785.154420   9190.166764  ...     1814.196468      2033.119958
      4          5771.417165   3847.385432  ...      452.022146       383.742941
      5          4951.158886   3300.643396  ...      474.220266       245.572689
                     ...           ...  ...             ...              ...
      9996      27755.139250  18503.269117  ...     2189.101714      5980.458717
      9997       7338.893087   4892.682575  ...      703.088993       812.566152
      9998      22878.042022  15252.462621  ...     1801.701611      4740.283791
      9999       6029.228626   4019.657332  ...      473.273387       449.939683
      10000      3804.512116   2536.489758  ...      364.193562       -27.270550

      [10000 rows x 5 columns]


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv


