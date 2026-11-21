# Cancer_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1190: need_max 1188; max index 1188 via pols_if(t+1) in pols_if_at(AFT_DECR):1041 and
#     check_pols_roll_fwd_resid:1502, pols_cancer(t+1):1525; exclusive 1189 + 1 spare
{'cells_param_size': {'t': 1190}}
