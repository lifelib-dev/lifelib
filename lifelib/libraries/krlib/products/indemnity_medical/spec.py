# Medical_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   y < 13: policy year y = t//12 + 1 (:599); checks loop y in range(1, policy_year(proj_len() - 1) + 1) =
#     1..10 (:1902 etc.); policy_year(proj_len) = 11; bound 11+1, + 1 year margin (matches t margin)
#   t < 133: need_max 120 + 1 for pols_if(t + 1)/pols_if(t+1) roll-forward at t = proj_len-1 + 12 margin
{'cells_param_size': {'y': 13, 't': 133}}
