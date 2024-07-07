The **ProductBase** Space
==========================


.. automodule:: appliedlife.IntegratedLife.ProductBase



Projection parameters
----------------------

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   fixed_params
   proj_len
   scen_index
   asmp_id
   date_id


Model point data
------------------

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

   margin_expense
   margin_guarantee


Present values
---------------

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

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
   :toctree: ../generated/
   :template: mxbase.rst

   result_pv
   result_cf
   result_pols
   result_sample
   excel_sample


Validation
-----------

.. autosummary::
   :toctree: ../generated/
   :template: mxbase.rst

   check_av_roll_fwd
   check_margin
   check_pv_net_cf