# KLV_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 481: t = t_start()..proj_len(): loops range(t_start(), proj_len()) (lines 2202-2486),
#     check_pols_roll_fwd_resid reads pols_if(t+1) at t = proj_len()-1 (line 2215). Max t = 480 -> bound 481.
#   k < 41: policy year k = k_start()..proj_len_y(): loops range(k_start(), proj_len_y()) (lines 2292-2549)
#     plus res_pp(k+1)/res_zill_pp(k+1)/av_sur_pp(k+1)/bonus_si_pp(k+1) at k = proj_len_y()-1 (lines
#     1327-1346, 1875-1898, 2281-2313, 2349). Max k = 40 -> bound 41. NOTE k = -1 is read: res_guar_pp(k-1)
#     with k = duration(t) = 0 (line 1923; traced lo -1).
#   x < 121: mort_rate_at_age(x) reads mort_table.csv .loc[(sex, int(x))] (lines 795-805), ages 0..120 per
#     sex; called with issue_age()+k and x+j (lines 877, 989, 1117, 1139). Bound 120+1 = 121 (reachable max =
#     60 + 40 = 100 per product-spec.md:158-159).
{'cells_param_size': {'t': 481, 'k': 41, 'x': 121}}
