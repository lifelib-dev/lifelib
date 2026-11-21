# RILA_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1082: need_max 1080 + 1 (market_state(t+1, ...) in index_level/mvr/risk_free/div_yield/impl_vol
#     lines 674-719; opt_component CURRENT k = t+1; pols_if(t+1) in av_at line 2064, check_pols_roll_fwd_resid
#     line 2136) + 1 margin = 1082
#   k < 1082: month index into market_scenario.csv month_end via index.asof (market_state line ~650); k =
#     t+1 or term_start_month(t) <= proj_len(); same as t
{'cells_param_size': {'t': 1082, 'k': 1082}}
