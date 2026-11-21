# PER_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 746: need_max 744; check_horizon (:1967) probes premium_pp(proj_len()) and
#     years_to_horizon(proj_len()) -> max t = 744 -> 745 exclusive, +1 margin
{'cells_param_size': {'t': 746}}
