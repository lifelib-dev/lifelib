.. module:: savings.CashValue_SE

The **CashValue_SE** Model
==========================

.. py:currentmodule:: savings.CashValue_SE.Projection

Overview
-----------

The :mod:`~savings.CashValue_SE` model projects cashflows
of a generic hypothetical savings product.
The model is a monthly-step model and
projects insurance cashflows of a sample model point at a time.
The model can project both new business and in-force policies.
The present values of cashflows are also calculated.

By default, the model is configured as follows:

* 4 types of product specs, A, B, C, D are available. The spec parameters
  are read into :attr:`product_spec_table`
  from the file *product_spec_table.xlsx* in the model folder.

* A and B are single premium products with limited policy terms,
  while C and D are level premium whole life products.
  A and B are simulate variable annuities, while C and D are simulate variable life.

* By default, 4 model points, 1 for each product type, are set up.
  The 4 model points are new business policies issued at time 0.
  The model can also project in-force policies at time 0 or
  future new business policies issued after time 0.

* Premiums, net of premium loadings if applicable, are transferred to
  the account value. Maintenance fees and cost-of-insurance charges
  are deducted from the account value at the beginning of
  every month. The investment return is then added to/subtracted from
  the account value. The investment returns are calculated from
  standard normal random numbers read into :attr:`std_norm_rand`
  from the file
  *std_norm_rand.csv*.

* Upon death, a death benefit is paid. The amount of the death benefit
  is the greater of the sum assured and the account value.
  The entire account value is transferred for paying the death benefit.

* Upon lapse, the account value is paid out as surrender benefit.
  Whether surrender charge applies or not varies by the product types.
  If it applies, the cash surrender value is the account value
  net of the surrender charge amount.

* For A and B, the maturity benefit is paid at maturity.
  The remaining account value is paid as the maturity benefit.

* Depending on the product types, premium loads are collected
  and the remaining portions of the premiums are transferred to the account value.
  How much premium loading is collected from each premium varies
  by the product types, and it
  is specified in *product_spec_table.xlsx*.
  Whether each type has surrender charge and if so its percentages
  are also specified in the file.


Policy decrement
^^^^^^^^^^^^^^^^

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

.. figure:: /images/libraries/pols_if_at_illustration.png


Although the default model points are all new business policies,
:mod:`~savings.CashValue_SE` reads the duration of each model
point at time 0 from the model point file.
The duration of a model point being *N* months (*N* > 0) means
*N* months have elapsed before time 0 since the issue of the model point.
If the duration is *-N* months, the model point is issued
*N* months after time 0.

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


Account value roll-forward
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The account value per policy at each ``t`` is calculated
from the previous balance by adding cash inflows and
subtracting cash outflows.
The order and timing of the cashflows are as follows:

    * At the beginning of each month, premium net of loadings, if any,
      is put into the account value.
    * At the beginning of the month after the premium inflow,
      fees are deducted from the account value.
    * The investment income is earned on the account value
      throughout the month. Since policy decrement due to
      lapse and death is assumed to occur at the middle of the month,
      half the monthly investment return is assumed to be earned
      on the account values of the exiting policies.

.. figure:: /images/libraries/av_pp_at.png


Basic Usage
-----------

Reading the model
^^^^^^^^^^^^^^^^^

Create your copy of the *savings* library by following
the steps on the :doc:`/quickstart` page.
The model is saved as the folder named *CashValue_SE* in the copied folder.

To read the model from Spyder, right-click on the empty space in *MxExplorer*,
and select *Read Model*.
Click the folder icon on the dialog box and select the
*CashValue_SE* folder.

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
:attr:`point_id` in :mod:`~savings.CashValue_SE.Projection`.
It is ``1`` by default.
:attr:`model_point_table` contains 4 model points
as a pandas DataFrame.
To change the model point to another one, set the other model point's ID
to :attr:`point_id`. Setting the new :attr:`point_id` clears
all the values of Cells that are specific to the previous model point.


Getting multiple results
^^^^^^^^^^^^^^^^^^^^^^^^

The :mod:`~savings.CashValue_SE.Projection` space
is parameterized with :attr:`point_id`,
i.e. the Projection space can have dynamic child spaces, such as
``Projection[1]``, ``Projection[2]``, ``Projection[3]`` ..., each of which
represents the Projection for each of the model points.


.. figure:: /images/libraries/savings/CashValue_SE/diagram1.png

.. note::

   Getting results for too many dynamic child spaces
   takes a considerable amount of time.
   The default *CashValue_SE* model would take more than a minute
   for 1000 model points on an ordinary spec PC.
   To calculate for many model points,
   consider using the :mod:`~savings.CashValue_ME` model.



Model Specifications
---------------------

The *CashValue_SE* model has only one UserSpace,
named :mod:`~savings.CashValue_SE.Projection`,
and all the Cells and References are defined in the space.

The Projection Space
^^^^^^^^^^^^^^^^^^^^

.. automodule:: savings.CashValue_SE.Projection


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

The model point data stored in an Excel file named *model_point_table.xlsx*
under the model folder is read into :attr:`model_point_table`.
Policy attributes that only vary by product spec are
stored separately in another Excel file named *product_spec_table.xlsx*,
and read into :attr:`product_spec_table`.
The  :attr:`product_spec_table` attributes are joined with
:attr:`model_point_table` in :func:`model_point_table_ext`
and referenced from :func:`model_point`.

.. figure:: /images/libraries/savings/CashValue_SE/diagram2.png

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
under the model folder, and is read into :attr:`mort_table` as a DataFrame.
:func:`mort_rate` looks up :attr:`mort_table` and picks up
the annual mortality rate to be applied for the selected
model point at time ``t``.
:func:`mort_rate_mth` converts :func:`mort_rate` to the monthly mortality
rate to be applied during the month starting at time ``t``.

.. figure:: /images/libraries/savings/CashValue_SE/diagram3.png

The discount rate data is stored in an Excel file named *disc_rate_ann.xlsx*
under the model folder, and is read into :attr:`disc_rate_ann` as a Series.

.. figure:: /images/libraries/savings/CashValue_SE/diagram4.png

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

.. figure:: /images/libraries/pols_if_at_illustration.png


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

:func:`av_pp_at(t, timing)<av_pp_at>` calculates the account value per policy
at ``t``.
Since :func:`av_pp_at` can take multiple values for the same ``t``
depending on the timing of various cashflows into and out of the
account value, the second parameter ``timing`` is used
to specify the timing of measuring the account value.

:func:`av_pp_at(t, 'BEF_PREM')<av_pp_at>` indicates
the account value before premium payment for the month.
At time 0, it is read from :func:`av_pp_init`,
otherwise its calculated from the previous period
as :func:`av_pp_at(t-1, 'BEF_INV')<av_pp_at>` plus
:func:`inv_income_(t-1)<inv_income>`.

:func:`av_pp_at(t, 'BEF_FEE')<av_pp_at>` indicates
the account value after the premium payment before fee deduction, and
is calculated as :func:`av_pp_at(t, 'BEF_PREM')<av_pp_at>` plus
:func:`prem_to_av_pp`.

:func:`av_pp_at(t, 'BEF_INV')<av_pp_at>` indicates
the account value after then fee deduction before earning investment yield, and
is calculated as :func:`av_pp_at(t, 'BEF_FEE')<av_pp_at>` minus
:func:`maint_fee_pp` and :func:`coi_pp`.

:func:`av_pp_at(t, 'MID_MTH')<av_pp_at>` indicates
the account value at ``t+0.5``, and half of :func:`inv_income`
is earned. :func:`av_pp_at(t, 'MID_MTH')<av_pp_at>` is
for policies exiting by lapse and death during the month.

.. figure:: /images/libraries/av_pp_at.png

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


.. _cashvalue_se-results:

Results
^^^^^^^^^^^^^^^^^^

:func:`result_cf` outputs the cashflows of the selected model point
as a DataFrame::

    >>> result_cf()
           Premiums        Death  ...  Change in AV  Net Cashflow
    0    50000000.0   999.844857  ...  4.447174e+07  2.033342e+06
    1           0.0   991.084783  ... -1.065060e+06  3.292919e+04
    2           0.0   982.401460  ...  2.039757e+05  3.208843e+04
    3           0.0   973.794216  ... -2.527055e+05  3.228511e+04
    4           0.0   965.262383  ... -7.053975e+05  3.210189e+04
    ..          ...          ...  ...           ...           ...
    116         0.0  1346.032341  ...  2.851405e+04  2.368209e+04
    117         0.0  1343.713636  ... -2.927039e+05  2.370171e+04
    118         0.0  1341.398924  ...  4.096877e+05  2.347573e+04
    119         0.0  1339.088201  ...  4.207922e+05  2.381819e+04
    120         0.0     0.000000  ... -3.263268e+07  0.000000e+00

    [121 rows x 9 columns]


:func:`result_pv` outputs the present values of the cashflows::

    >>> result_pv()
          Premiums          Death  ...  Commissions  Net Cashflow
    PV  50000000.0  135032.740399  ...    2500000.0  4.957050e+06


.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   ~result_cf
   ~result_pv
   ~result_pols


