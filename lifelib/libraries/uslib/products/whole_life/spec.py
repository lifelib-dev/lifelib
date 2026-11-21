# WholeLife_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1202: need_max 1200 + 1 (pols_if(t+1) in check_pols_roll_fwd_resid line 1537) + 1 margin = 1202
{'cells_param_size': {'t': 1202}}
