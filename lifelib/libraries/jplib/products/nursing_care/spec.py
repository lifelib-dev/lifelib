# LTC_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 950: need_max 948; max index 948: check_nesting:1326 scans range(proj_len()+1) and pols_if(t+1) in
#     pols_if_at:979 / check_pols_roll_fwd_resid:1283; exclusive 949 + 1 spare
#   j < 80: shipped declaration
{'cells_param_size': {'t': 950, 'j': 80}}
