# UL_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1238: need_max 1236 + 1 (av_at(t+1, Timing.BEF_PREM) in av_change line 964 and check_av_roll_fwd
#     line 1475) + 1 margin = 1238
{'cells_param_size': {'t': 1238}}
