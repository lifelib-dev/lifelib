# EC_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 481: need_max 480; t-cells only called for t in range(proj_start(), proj_len()) and t-1 -> max 479
#     -> 480 exclusive, +1 margin
#   m < 482: month boundary m in 0..proj_len() (rem_term :890, tec_rate :983, i_pm :1030, disc_factor
#     :1047); disc_factor(t+1)/i_pm(t+1)/rem_term(t+1) reach 480 -> 481 exclusive, +1 margin
{'cells_param_size': {'t': 481, 'm': 482}}
