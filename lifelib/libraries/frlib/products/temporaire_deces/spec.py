# TD_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 686: need_max 684; pols_if(t+1) in check_pols_roll_fwd_resid/check_decrement_closure_resid -> max t = 684 ->
#   y < 58: policy year y in range(proj_len_y()) (tariff_annuity :849), max 56 -> 57 exclusive, +1 margin;
#     prem_tariff_pp(12*y) <= 672
{'cells_param_size': {'t': 686, 'y': 58}}
