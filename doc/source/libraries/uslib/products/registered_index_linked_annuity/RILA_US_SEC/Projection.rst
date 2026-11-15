The **Projection** Space
========================

.. automodule:: uslib.products.registered_index_linked_annuity.RILA_US_SEC.Projection

Cells Descriptions
------------------

.. autofunction:: model_point

.. autofunction:: point_id

.. autofunction:: policy_id

.. autofunction:: age_at_entry

.. autofunction:: sex

.. autofunction:: mort_schedule

.. autofunction:: premium_pp

.. autofunction:: policy_count

.. autofunction:: pols_if_init

.. autofunction:: duration_mth_init

.. autofunction:: term_years

.. autofunction:: buffer

.. autofunction:: crediting_type

.. autofunction:: declared_cap

.. autofunction:: declared_step

.. autofunction:: declared_edge

.. autofunction:: participation

.. autofunction:: floor_rate

.. autofunction:: iv_family

.. autofunction:: amort_rule

.. autofunction:: nge_reset

.. autofunction:: wd_rate_ann

.. autofunction:: scenario_id

.. autofunction:: wd_schedule_id

.. autofunction:: wd_schedule_number

.. autofunction:: scenario_number

.. autofunction:: is_cap_crediting

.. autofunction:: is_step_crediting

.. autofunction:: is_edge_crediting

.. autofunction:: is_floor_crediting

.. autofunction:: is_iv_portfolio

.. autofunction:: is_iv_notional

.. autofunction:: is_iv_delta

.. autofunction:: is_iv_legacy

.. autofunction:: is_straight_line

.. autofunction:: is_updated_expiry

.. autofunction:: inv_amt_pp_init

.. autofunction:: fixed_acct_pp_init

.. autofunction:: holding_acct_pp_init

.. autofunction:: av_pp_init

.. autofunction:: av_pp_prev_anniv_init

.. autofunction:: free_wd_remain_init

.. autofunction:: rop_pp_init

.. autofunction:: index_at_term_start_init

.. autofunction:: mvr_at_term_start_init

.. autofunction:: risk_free_at_term_start_init

.. autofunction:: div_yield_at_term_start_init

.. autofunction:: impl_vol_at_term_start_init

.. autofunction:: cap_rate_init

.. autofunction:: is_uncapped

.. autofunction:: policy_term

.. autofunction:: maturity_mth

.. autofunction:: proj_len

.. autofunction:: duration_mth

.. autofunction:: t_entry

.. autofunction:: is_active

.. autofunction:: duration

.. autofunction:: duration_eom

.. autofunction:: policy_year

.. autofunction:: age

.. autofunction:: is_anniv

.. autofunction:: term_elapsed_mth

.. autofunction:: term_start_month

.. autofunction:: tau

.. autofunction:: is_term_end

.. autofunction:: market_state

.. autofunction:: index_level

.. autofunction:: index_at_term_start

.. autofunction:: mvr

.. autofunction:: mvr_at_term_start

.. autofunction:: risk_free_at_term_start

.. autofunction:: div_yield_at_term_start

.. autofunction:: impl_vol_at_term_start

.. autofunction:: risk_free

.. autofunction:: div_yield

.. autofunction:: impl_vol

.. autofunction:: index_perf

.. autofunction:: norm_cdf

.. autofunction:: bs_d1

.. autofunction:: bs_d2

.. autofunction:: bs_call

.. autofunction:: bs_put

.. autofunction:: bs_binary_call

.. autofunction:: guar_min_rate

.. autofunction:: opt_budget_target

.. autofunction:: opt_budget_at_cap

.. autofunction:: declared_cap_solved

.. autofunction:: cap_solved_at_start

.. autofunction:: cap_rate

.. autofunction:: step_rate

.. autofunction:: edge_rate

.. autofunction:: opt_leg_count

.. autofunction:: opt_leg

.. autofunction:: opt_component

.. autofunction:: opt_component_at

.. autofunction:: opt_portfolio

.. autofunction:: opt_portfolio_abs

.. autofunction:: opt_portfolio_at

.. autofunction:: opt_portfolio_abs_at

.. autofunction:: opt_budget

.. autofunction:: fixed_leg_yield

.. autofunction:: nge_spread_implied

.. autofunction:: credit_rate_at

.. autofunction:: credit_rate_by

.. autofunction:: credit_rate_term

.. autofunction:: credit_rate_accrued

.. autofunction:: budget_amort_factor

.. autofunction:: mva_factor

.. autofunction:: fixed_proxy_factor

.. autofunction:: deriv_proxy_factor

.. autofunction:: trading_cost_factor

.. autofunction:: cap_calc_factor

.. autofunction:: iv_factor

.. autofunction:: iv_ratio

.. autofunction:: inv_amt_basis_pp

.. autofunction:: iv_notional_pp

.. autofunction:: opt_component_pp

.. autofunction:: fixed_proxy_pp

.. autofunction:: budget_amort_pp

.. autofunction:: deriv_proxy_pp

.. autofunction:: trading_cost_pp

.. autofunction:: inv_amt_pp_at

.. autofunction:: inv_amt_pp

.. autofunction:: interim_value_pp_at

.. autofunction:: roll_share

.. autofunction:: roll_to_acct_pp

.. autofunction:: acct_rate

.. autofunction:: fixed_acct_pp_at

.. autofunction:: fixed_acct_pp

.. autofunction:: holding_acct_pp_at

.. autofunction:: holding_acct_pp

.. autofunction:: av_pp_at

.. autofunction:: av_pp

.. autofunction:: inv_income_pp

.. autofunction:: free_wd_base

.. autofunction:: free_wd_allow

.. autofunction:: free_wd_avail

.. autofunction:: wd_scheduled_pp

.. autofunction:: wd_amount_pm

.. autofunction:: wd_behavioral_pp

.. autofunction:: wd_pp

.. autofunction:: wd_free_pp

.. autofunction:: free_wd_remain

.. autofunction:: wd_excess_pp

.. autofunction:: surr_charge_rate

.. autofunction:: surr_charge_rate_at

.. autofunction:: wd_charge_pp

.. autofunction:: wd_payment_pp

.. autofunction:: wd_bucket_value_pp

.. autofunction:: wd_alloc_pp

.. autofunction:: surr_excess_pp

.. autofunction:: surr_charge_pp

.. autofunction:: surr_value_pp

.. autofunction:: rop_pp

.. autofunction:: death_ben_pp

.. autofunction:: mort_rate

.. autofunction:: mort_rate_base_at

.. autofunction:: mort_rate_mth

.. autofunction:: lapse_rate_base

.. autofunction:: lapse_rate_base_py

.. autofunction:: lapse_shock_year

.. autofunction:: lapse_rate_sc_mult

.. autofunction:: lapse_iv_mult

.. autofunction:: lapse_rate

.. autofunction:: lapse_rate_mth

.. autofunction:: term_end_lapse_rate

.. autofunction:: pols_if_at

.. autofunction:: pols_if

.. autofunction:: pols_new_biz

.. autofunction:: pols_death

.. autofunction:: pols_lapse_term

.. autofunction:: pols_lapse

.. autofunction:: pols_maturity

.. autofunction:: pols_decr

.. autofunction:: claim_pp

.. autofunction:: claim_from_av_pp

.. autofunction:: premiums

.. autofunction:: prem_to_av_pp

.. autofunction:: prem_to_av

.. autofunction:: withdrawals

.. autofunction:: claims

.. autofunction:: claims_from_av

.. autofunction:: claims_over_av

.. autofunction:: inflation_factor

.. autofunction:: expenses

.. autofunction:: premium_taxes

.. autofunction:: net_cf

.. autofunction:: av_at

.. autofunction:: inv_income

.. autofunction:: wd_from_av

.. autofunction:: av_change

.. autofunction:: roll_fwd_tol

.. autofunction:: check_av_roll_fwd_resid

.. autofunction:: check_av_roll_fwd

.. autofunction:: check_pols_roll_fwd_resid

.. autofunction:: check_pols_roll_fwd

.. autofunction:: check_term_end_identity_resid

.. autofunction:: check_term_end_identity

.. autofunction:: result_cf

.. autofunction:: result_pols

.. autofunction:: result_av

.. autofunction:: result_iv
