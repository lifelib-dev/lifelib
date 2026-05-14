The **ProductBase** Space
==========================


.. automodule:: appliedlife.IntegratedLife.ProductBase



Projection parameters
----------------------

.. autosummary::

   fixed_params
   proj_len
   scen_index
   asmp_id
   date_id


Model point data
------------------

.. autosummary::

   model_point
   model_point_index
   model_point_table_ext
   age
   sex
   age_at_entry
   av_pp_init
   commission_rate
   duration
   duration_mth
   duration_mth_init
   has_gmab
   has_gmdb
   has_surr_charge
   is_wl
   maint_fee_rate
   policy_term
   premium_type
   sum_assured
   surr_charge_id


Assumptions
-------------

.. autosummary::

   base_lapse_rate
   is_lapse_dynamic
   dyn_lapse_param
   dyn_lapse_factor
   lapse_rate_key
   lapse_rate
   disc_factors
   disc_rate
   disc_rate_mth
   expense_acq
   expense_maint
   inflation_rate
   inflation_factor
   mort_last_age
   base_mort_rate
   mort_rate
   mort_rate_key
   mort_rate_mth
   mort_table_id


Policy values
---------------

.. autosummary::

   claim_net_pp
   claim_pp
   coi_pp
   coi_rate
   premium_pp
   surr_charge_key
   surr_charge_rate


Policy decrement
------------------

.. autosummary::

   pols_if
   pols_if_at
   pols_if_init
   pols_lapse
   pols_death
   pols_maturity
   pols_new_biz



Account Value
--------------

.. autosummary::

   inv_income
   inv_income_pp
   inv_return_mth
   av_at
   av_change
   av_pp_at
   csv_pp
   coi
   maint_fee
   maint_fee_pp
   net_amt_at_risk
   prem_to_av
   prem_to_av_pp


Cashflows
-----------

.. autosummary::

   claims
   claims_from_av
   claims_over_av
   commissions
   expenses
   surr_charge
   net_cf



Margin Analysis
----------------

.. autosummary::

   margin_expense
   margin_guarantee


Present values
---------------

.. autosummary::

   pv_av_change
   pv_claims
   pv_claims_from_av
   pv_claims_over_av
   pv_commissions
   pv_expenses
   pv_inv_income
   pv_maint_fee
   pv_net_cf
   pv_pols_if
   pv_premiums


Results and output
--------------------

.. autosummary::

   result_pv
   result_cf
   result_pols
   result_sample
   excel_sample


Validation
-----------

.. autosummary::

   check_av_roll_fwd
   check_margin
   check_pv_net_cf


Cells Descriptions
------------------

.. autofunction:: fixed_params

.. autofunction:: proj_len

.. autofunction:: scen_index

.. autofunction:: asmp_id

.. autofunction:: date_id

.. autofunction:: model_point

.. autofunction:: model_point_index

.. autofunction:: model_point_table_ext

.. autofunction:: age

.. autofunction:: sex

.. autofunction:: age_at_entry

.. autofunction:: av_pp_init

.. autofunction:: commission_rate

.. autofunction:: duration

.. autofunction:: duration_mth

.. autofunction:: duration_mth_init

.. autofunction:: has_gmab

.. autofunction:: has_gmdb

.. autofunction:: has_surr_charge

.. autofunction:: is_wl

.. autofunction:: maint_fee_rate

.. autofunction:: policy_term

.. autofunction:: premium_type

.. autofunction:: sum_assured

.. autofunction:: surr_charge_id

.. autofunction:: base_lapse_rate

.. autofunction:: is_lapse_dynamic

.. autofunction:: dyn_lapse_param

.. autofunction:: dyn_lapse_factor

.. autofunction:: lapse_rate_key

.. autofunction:: lapse_rate

.. autofunction:: disc_factors

.. autofunction:: disc_rate

.. autofunction:: disc_rate_mth

.. autofunction:: expense_acq

.. autofunction:: expense_maint

.. autofunction:: inflation_rate

.. autofunction:: inflation_factor

.. autofunction:: mort_last_age

.. autofunction:: base_mort_rate

.. autofunction:: mort_rate

.. autofunction:: mort_rate_key

.. autofunction:: mort_rate_mth

.. autofunction:: mort_table_id

.. autofunction:: claim_net_pp

.. autofunction:: claim_pp

.. autofunction:: coi_pp

.. autofunction:: coi_rate

.. autofunction:: premium_pp

.. autofunction:: surr_charge_key

.. autofunction:: surr_charge_rate

.. autofunction:: pols_if

.. autofunction:: pols_if_at

.. autofunction:: pols_if_init

.. autofunction:: pols_lapse

.. autofunction:: pols_death

.. autofunction:: pols_maturity

.. autofunction:: pols_new_biz

.. autofunction:: inv_income

.. autofunction:: inv_income_pp

.. autofunction:: inv_return_mth

.. autofunction:: av_at

.. autofunction:: av_change

.. autofunction:: av_pp_at

.. autofunction:: csv_pp

.. autofunction:: coi

.. autofunction:: maint_fee

.. autofunction:: maint_fee_pp

.. autofunction:: net_amt_at_risk

.. autofunction:: prem_to_av

.. autofunction:: prem_to_av_pp

.. autofunction:: claims

.. autofunction:: claims_from_av

.. autofunction:: claims_over_av

.. autofunction:: commissions

.. autofunction:: expenses

.. autofunction:: surr_charge

.. autofunction:: net_cf

.. autofunction:: margin_expense

.. autofunction:: margin_guarantee

.. autofunction:: pv_av_change

.. autofunction:: pv_claims

.. autofunction:: pv_claims_from_av

.. autofunction:: pv_claims_over_av

.. autofunction:: pv_commissions

.. autofunction:: pv_expenses

.. autofunction:: pv_inv_income

.. autofunction:: pv_maint_fee

.. autofunction:: pv_net_cf

.. autofunction:: pv_pols_if

.. autofunction:: pv_premiums

.. autofunction:: result_pv

.. autofunction:: result_cf

.. autofunction:: result_pols

.. autofunction:: result_sample

.. autofunction:: excel_sample

.. autofunction:: check_av_roll_fwd

.. autofunction:: check_margin

.. autofunction:: check_pv_net_cf