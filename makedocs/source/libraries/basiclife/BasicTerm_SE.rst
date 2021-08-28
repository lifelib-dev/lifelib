.. module:: basiclife.BasicTerm_SE

The **BasicTerm_SE** Model
==========================

.. py:currentmodule:: basiclife.BasicTerm_SE.Projection

Overview
-----------

The :mod:`~basiclife.BasicTerm_SE` model is a variation of :mod:`~basiclife.BasicTerm_S`,
and it projects the cashslows of
in-force policies at time 0 and future new business
policies issued at or after time 0.

While :mod:`~basiclife.BasicTerm_S` is a new business model and it assumes all model points
are issued at time 0, :mod:`~basiclife.BasicTerm_SE` reads the duration of each model
point at time 0 from the model point file.
The duration of a model point being *N* months (*N* > 0) means
*N* months have elapsed before time 0 since the issue of the model point.
If the duration is *-N* months, the model point is issued
*N* months after time 0. Premium rates are fed into the model from a table
which is assigned to :attr:`premium_table`.
The rates are calculated by :mod:`~basiclife.BasicTerm_M`.
How to create the table is demonstrated in the
:doc:`create_premium_table.ipynb </libraries/notebooks/basiclife/create_premium_table>`
notebook included in this library.

Other specifications of :mod:`~basiclife.BasicTerm_SE` are the same as :mod:`~basiclife.BasicTerm_S`.
The model is a monthly step model and
projects insurance cashflows of a sample model point at a time.
The modeled product is a level-premium plain term product with no surrender value.
The projected cashflows are premiums, claims, expenses and commissions.
The assumptions used are mortality rates, lapse rates, discount rates, expense,
inflation and commission rates.
The present values of the cashflows are also calculated.
The premium amount for each individual model point is calculated as the net
premium with loadings,
where the net premium is calculated from the present value of the claims.

Changes from **BasicTerm_S**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is the list of
Cells and References that are newly added or updated from :mod:`~basiclife.BasicTerm_S`.

* :attr:`model_point_table`
* :attr:`premium_table` <new>
* :func:`duration`
* :func:`duration_mth` <new>
* :func:`expenses`
* :func:`pols_death`
* :func:`pols_if`
* :func:`pols_if_at` <new>
* :func:`pols_if_init`
* :func:`pols_lapse`
* :func:`pols_maturity`
* :func:`pols_new_biz` <new>
* :func:`premiums`
* :func:`premium_pp`
* :func:`proj_len`
* :func:`result_pols` <new>


The number of policies at a certain time can take different values
depending on the timing of policy inflows and outflows at the same time.
To represent different values for the number of policies
depending on the timing of the policy flows,
:func:`pols_if_at(t, timing)<pols_if_at>` is introduced.
:func:`pols_if_at(t, timing)<pols_if_at>`
calculates the number of policies in-force
at time ``t`` and has a parameter named ``timing`` in addition to ``t``.
Strings are passed to ``timing`` to indicate at what timing the number
of polices in-force is measured.

* ``"BEF_DECR"``: Before lapse and death
* ``"BEF_MAT"``: Before maturity
* ``"BEF_NB"``: Before new business

The figure below illustrates how various policy inflows and outflows
are modeled in this model for one calculation step
from time ``t-1`` to time ``t``.

:func:`pols_lapse(t)<pols_lapse>` and :func:`pols_death(t)<pols_death>`
are the number of lapse and death from ``t-1`` to ``t``.
It is assumed that policies mature at the beginning of each month,
and new business policies enter at the beginning of the month
but after the maturity in that month.

.. figure:: /images/libraries/basiclife/pols_if_at_illustration.png


:attr:`model_point_table` has the ``duration_mth`` column,
and the column is read into the :func:`duration_mth(0)<duration_mth>`.
If :func:`duration_mth(0)<duration_mth>` is positive,
the model point is in-force policies and
the number of policies
at time 0 is read from the ``policy_count`` column in :attr:`model_point_table`
into :func:`pols_if_init`, and
:func:`pols_if_at(0, "BEF_MAT")<pols_if_at>` is set from :func:`pols_if_init`.
:func:`duration_mth` increments by 1 each step. If :func:`duration_mth`
is negative, ``policy_count`` is read into :func:`pols_new_biz`
when :func:`duration_mth` becomes 0.

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
The model is saved as the folder named *BasicTerm_SE* in the copied folder.

To read the model from Spyder, right-click on the empty space in *MxExplorer*,
and select *Read Model*.
Click the folder icon on the dialog box and select the
*BasicTerm_SE* folder.

Getting the results
^^^^^^^^^^^^^^^^^^^
By default, the model has Cells
for outputting projection results as listed in the
:ref:`basicterm_se-results` section.
:func:`result_cf` outputs cashflows of the selected model point,
:func:`result_pv` outputs the present values of the cashflows,
:func:`result_pols` outputs the decrement table of the model point.
All the Cells outputs the results as pandas DataFrame.

See the :doc:`/quickstart` page for how
to get the results in an *MxConsole* and view the results in *MxDataViewer*.

Changing the model point
^^^^^^^^^^^^^^^^^^^^^^^^

The model point to be selected is determined by
:attr:`point_id` in :mod:`~basiclife.BasicTerm_SE.Projection`.
It is ``1`` by default.
:attr:`model_point_table` contains all the 10,000 sample model points
as a pandas DataFrame.
To change the model point to another one, set the other model point's ID
to :attr:`point_id`. Setting the new :attr:`point_id` clears
all the values of Cells that are specific to the previous model point.


Getting multiple results
^^^^^^^^^^^^^^^^^^^^^^^^

The :mod:`~basiclife.BasicTerm_SE.Projection` space
is parameterized with :attr:`point_id`,
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
   The default *BasicTerm_SE* model would take more than a minute
   for 1000 model points on an ordinary spec PC.
   To calculate for many model points,
   consider using the :mod:`~basiclife.BasicTerm_ME` model.



Model Specifications
---------------------

The *BasicTerm_SE* model has only one UserSpace,
named :mod:`~basiclife.BasicTerm_SE.Projection`,
and all the Cells and References are defined in the space.

The Projection Space
^^^^^^^^^^^^^^^^^^^^

.. automodule:: basiclife.BasicTerm_SE.Projection


Projection parameters
^^^^^^^^^^^^^^^^^^^^^

The time step of the model is monthly. Cashflows and other time-dependent
variables are indexed with ``t``.

Projection is carried out separately for individual model points.
:func:`proj_len` calculates the number of months to be
projected for the selected model point.

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
   ~duration_mth


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
as :func:`sum_assured` times the premium rate in :attr:`premium_table`.
for :func:`age_at_entry` and :func:`policy_term` of the policy.
:func:`net_premium_pp` and :func:`loading_prem` are not used
in :mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`.

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

.. rubric:: At ``t=0``

If the selected model point represents in-force policies, i.e.
the ``duration_mth`` of the model point in :attr:`model_point_table`
is positive, :func:`pols_if_at(0, "BEF_MAT")<pols_if_at>` is set to
the value through :func:`pols_if_init`.

.. rubric:: At each projection step

:func:`pols_if_at(t, timing)<pols_if_at>` represents
the number of policies at ``t``.
The ``timing`` parameter can take the following string values.

* ``"BEF_MAT"``: Before maturity
* ``"BEF_NB"``: Before new business
* ``"BEF_DECR"``: Before lapse and death

Policy flows and in-force at each timing from ``t-1`` to ``t``
are calculated recursively as follows:

* :func:`pols_if_at(t-1, "BEF_DECR")<pols_if_at>` is calculated
  by adding :func:`pols_new_biz(t-1)<pols_new_biz>` to
  :func:`pols_if_at(t-1, "BEF_NB")<pols_if_at>`.
* :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>` is calculated by
  deducting :func:`pols_lapse(t)<pols_lapse>` and :func:`pols_death(t)<pols_death>`
  from :func:`pols_if_at(t-1, "BEF_DECR")<pols_if_at>`.
* :func:`pols_if_at(t, "BEF_NB")<pols_if_at>` is calculated by
  deducting :func:`pols_maturity(t)<pols_maturity>` from
  :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.
* :func:`pols_if_at(t, "BEF_DECR")<pols_if_at>` is calculated by
  :func:`pols_new_biz(t)<pols_new_biz>` from :func:`pols_if_at(t, "BEF_NB")<pols_if_at>`.

It is assumed that policies mature at the beginning of each month,
and new business policies enter at the beginning of the month
but after the maturity in that month.
:func:`pols_if(t)<pols_if>` is an alias
for :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

The figure below illustrates how various policy inflows and outflows
are modeled in this model for one calculation step
from time ``t-1`` to time ``t``.

.. figure:: /images/libraries/basiclife/pols_if_at_illustration.png


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

Commissions are assumed to be paid out during the first policy year
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
:func:`pv_pols_if` is not used
in :mod:`~basiclife.BasicTerm_SE` and :mod:`~basiclife.BasicTerm_ME`.

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


.. _basicterm_se-results:

Results
^^^^^^^^^^^^^^^^^^

:func:`result_cf` outputs the cashflows of the selected model point
as a DataFrame::

    >>> result_cf()
            Premiums       Claims    Expenses  Commissions  Net Cashflow
    0    8156.240000  2939.548223  430.000000  8156.240000  -3369.548223
    1    8084.493113  2913.690299  426.217477  8084.493113  -3339.907776
    2    8013.377352  2888.059836  422.468228  8013.377352  -3310.528064
    3    7942.887165  2862.654832  418.751959  7942.887165  -3281.406792
    4    7873.017050  2837.473306  415.068381  7873.017050  -3252.541687
    ..           ...          ...         ...          ...           ...
    115  5416.841591  5512.481202  312.332343     0.000000   -407.971953
    116  5406.889171  5502.353062  311.758491     0.000000   -407.222382
    117  5396.955036  5492.243531  311.185694     0.000000   -406.474188
    118  5387.039154  5482.152574  310.613949     0.000000   -405.727369
    119     0.000000     0.000000    0.000000     0.000000      0.000000


:func:`result_pv` outputs the present values of the cashflows
and also their percentages against the present value of premiums as a DataFrame::

    >>> result_pv()
             Premiums         Claims      Expenses   Commissions   Net Cashflow
    PV  708379.130574  474803.297001  38902.884356  85874.887301  108798.061916


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv
   ~result_pols


