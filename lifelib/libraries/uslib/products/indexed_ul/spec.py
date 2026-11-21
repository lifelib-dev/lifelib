# IUL_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1454: need_max 1452 + 1 (av_at(t+1, BEF_PREM) av_change line 1542, check_av_roll_fwd line 2141) + 1
#     margin = 1454
#   m < 1454: segment birth month (seg_new_pp(m) = sweep_pp(m), line 1220), m <= t; same as t
{'cells_param_size': {'t': 1454, 'm': 1454}}
