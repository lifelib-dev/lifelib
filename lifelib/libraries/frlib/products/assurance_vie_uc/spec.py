# UC_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1226: need_max 1224 = 12*(120-18); no forward offsets in code (only t-1, t-12) -> 1225 exclusive, +1
#     margin
{'cells_param_size': {'t': 1226}}
