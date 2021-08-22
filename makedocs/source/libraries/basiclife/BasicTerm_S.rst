.. module:: basiclife.BasicTerm_S

The **BasicTerm_S** Model
=========================

Overview
-----------

The **BasicTerm_S** model is the most basic cashflow model in lifelib.

The model is a monthly step, new business model and
projects insurance cashflows of a sample model point.
The modeled product is a level-premium plain term product with no surrender value.
The projected cashflows are premiums, claims, expenses and commissions.
The assumptions used are mortality rates, lapse rates, discount rates, expense,
inflation and commission rates.
The present values of the cashflows are also calculated.
The premium amount for each individual model point is calculated as the net premium with loadings,
where the net premium is calculated from the present value of the claims.


Basic Usage
-----------

Reading the model
^^^^^^^^^^^^^^^^^

Create your copy of the *basiclife* library by following
the steps on the :doc:`/quickstart` page.
The model is saved as the folder named *BasicTerm_S* in the copied folder.

To read the model from Spyder, right-click on the empty space in *MxExplorer*,
and select *Read Model*.
Click the folder icon on the dialog box and select the
*BasicTerm_S* folder.

Getting the results
^^^^^^^^^^^^^^^^^^^
By default, the model has Cells
for outputting projection results as listed in the
:ref:`basicterm_s-results` section.
:func:`~Projection.result_cf` outputs cashflows of the selected model point,
and :func:`~Projection.result_pv` outputs the present values of the cashflows.
Both Cells outputs the results as pandas DataFrame.

See the :doc:`/quickstart` page for how
to get the results in an *MxConsole* and view the results in *MxDataViewer*.

Changing the model point
^^^^^^^^^^^^^^^^^^^^^^^^

The model point to be selected is determined by
:attr:`~Projection.point_id` in :mod:`~basiclife.BasicTerm_S.Projection`.
It is ``1`` by default.
:attr:`~Projection.model_point_table` contains all the 10,000 sample model points
as a pandas DataFrame.
To change the model point to another one, set the other model point's ID
to :attr:`~Projection.point_id`. Setting the new :attr:`~Projection.point_id` clears
all the values of Cells that are specific to the previous model point.


Getting multiple results
^^^^^^^^^^^^^^^^^^^^^^^^

The :mod:`~basiclife.BasicTerm_S.Projection` space
is parameterized with :attr:`~Projection.point_id`,
i.e. the Projection space can have dynamic child spaces, such as
``Projection[1]``, ``Projection[2]``, ``Projection[3]`` ..., each of which
represents the Projection for each of the model points.


.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     node_width=120;
     BasicTerm_S [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     BasicTerm_S <- Projection[hstyle=composition];
     Projection <- Proj1[hstyle=composition];
     Projection <- Proj2[hstyle=composition];
     Projection <- Proj3[hstyle=composition];
     Proj1[label="Projection[1]" ]
     Proj2[label="Projection[2]" ]
     Proj3[label="Projection[...]"]
   }

.. note::

   Getting results for too many dynamic child spaces
   takes a considerable amount of time.
   The default *BasicTerm_S* model would take more than a minute
   for 1000 model points on an ordinary spec PC.
   To calculate for many model points,
   consider using the :mod:`~basiclife.BasicTerm_M` model.



Model Specifications
---------------------

The *BasicTerm_S* model has only one UserSpace,
named :mod:`~basiclife.BasicTerm_S.Projection`,
and all the Cells and References are defined in the space.

The Projection Space
^^^^^^^^^^^^^^^^^^^^

.. automodule:: basiclife.BasicTerm_S.Projection


Projection parameters
^^^^^^^^^^^^^^^^^^^^^

This is a new business model and all model points are issued at time 0.
The time step of the model is monthly. Cashflows and other time-dependent
variables are indexed with ``t``.

Cashflows and other flows that accumulate throughout a period
indexed with ``t`` denote the sums of the flows from ``t`` til ``t+1``.
Balance items indexed with ``t`` denote the amount at ``t``.

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

    ~proj_len


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
under the model folder, and is read into :attr:`mort_table` as a DataFrame.
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
under the model folder, and is read into :attr:`disc_rate_ann` as a Series.

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
:func:`pols_if` is not a cashflow, but used as an annuity factor
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
  ~check_pv_net_cf


.. _basicterm_s-results:

Results
^^^^^^^^^^^^^^^^^^

:func:`result_cf` outputs the cashflows of the selected model point
as a DataFrame::

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


:func:`result_pv` outputs the present values of the cashflows
and also their percentages against the present value of premiums as a DataFrame::

    >>> result_pv()
                  Premiums       Claims    Expenses  Commissions  Net Cashflow
    PV         8251.931435  5501.074678  748.303591  1084.601434    917.951731
    % Premium     1.000000     0.666641    0.090682     0.131436      0.111241


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv


