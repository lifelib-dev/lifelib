# Term_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 722: need_max 720 (proj_len:532); max index reached 720 via pols_if(t+1) in
#     check_pols_roll_fwd_resid:1447 and pols_lapse_pool(t+1):1472 over range(proj_len()); exclusive 721 + 1
#     spare
#   x < 81: mort_table.csv age 20..80 per sex (max key 80) + 1; mort_rate_at_age:638 read at age(t)<=79 and
#     min(age+1, omega_age)=80 (mort_age_shift, :678); mort_table_mean:650 x = term_start_age <= 79
#   m < 61: mort_table_mean(x, m) m = term_len(k) <= policy_term; max sai term 80-20 = 60 years (product-
#     spec.md:94-95) + 1
#   k < 8: term index k = 1 + duration//policy_term (term_index:581); composite 年満了 term 10y (product-
#     spec.md:95,121-127), duration <= 59 => k <= 6; exclusive 7 + 1 spare
{'cells_param_size': {'t': 722, 'x': 81, 'm': 61, 'k': 8}}
