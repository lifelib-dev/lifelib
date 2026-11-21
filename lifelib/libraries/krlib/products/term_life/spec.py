# Term_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   x < 121: mort_table.csv column age, keys 19..120 (read by mort_rate_at_age :759 and acc_mort_rate_at_age :772
#   m < 72: mort_table_mean(x, m) :785 is called with m = term_len(k) (:1030/:1038) <= policy_term() <= 71 years
#   t < 865: need_max 852 (see need_source) + 1 for t+1 reads at t=proj_len-1 (check_pols_roll_fwd_resid
#     :1675 pols_if(t + 1), lapse pool :1700 pols_lapse_pool(t + 1)) + 12-month margin = 852+1+12
#   k < 8: k = term_index(t) = 1 + (t//12)//policy_term() (:679). 갱신형 is the modelled 10-year cycle to
#     ceiling 보험나이 80 (product-spec.md:164,181): from entry 19, proj_years = 61, t//12 <= 61 at t=proj_len ->
#     k <= 1+61//10 = 7; 비갱신형 k = 1; bound = 7+1
{'cells_param_size': {'x': 121, 'm': 72, 't': 865, 'k': 8}}
