# VUL_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1466: need_max 1464 + 1 (av_at(t+1, BEF_PREM) in av_change line 1479, check_av_roll_fwd line 2110) +
#     1 margin = 1466
#   y < 123: policy year policy_year(t) = duration(t)+1 (callers lines 1126, 1178) and
#     policy_year_pricing(m) = m//12+1 <= 1463//12+1 = 122, +1 = 123 (coi_rate_guar_at clamps to the coi scale
#     max)
{'cells_param_size': {'t': 1466, 'y': 123}}
