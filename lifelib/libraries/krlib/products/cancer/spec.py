# Cancer_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1034: need_max 1021 + 1 for pols_if(t + 1)/pols_cancer(t + 1) roll-forward checks at t = proj_len-1
#     + 12 margin
{'cells_param_size': {'t': 1034}}
