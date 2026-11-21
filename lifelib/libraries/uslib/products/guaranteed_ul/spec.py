# ULSG_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1238: need_max 1236 + 1 (av_at(t+1, BEF_PREM) line 1166/2065; is_lapsed(t+1) in pols_lapse_grace
#     line 1715) + 1 margin = 1238
{'cells_param_size': {'t': 1238}}
