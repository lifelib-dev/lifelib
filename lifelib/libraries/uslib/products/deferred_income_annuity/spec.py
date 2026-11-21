# DIA_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1206: need_max 1200 + 5 (lives_if(a + j) with j < accel_months = 6, accel_cost line 1403 /
#   from_mth < 1206: month index (premium month tk, adjust_mth, income_start), < proj_len; same as t
#   start_mth < 362: month index (income_start_mth_at / adjust_start_mth), < proj_len; same as t
#   y < 101: policy year 1..proj_len()//12 (result_annual line 1944); 1200//12 = 100, +1 = 101
{'cells_param_size': {'t': 1206, 'from_mth': 1206, 'start_mth': 362, 'y': 101}}
