# IncomeTerm_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 900: need_max 899 => max index 898 (frame); t+1 only in check_pols_roll_fwd_resid:1083 over
#     range(term_m()) (<= 840); exclusive 899 + 1 spare
#   n < 842: annuity_certain_factor(n) n = pay_count(m) = max(term_m - m, guar_m) <= 840 (pay_count:725-738,
#     term_m max 840); exclusive 841 + 1 spare
#   m < 900: pay_count/pay_end(m) receive the claim month t (commute_pp:790, check_pay_count_resid:1155) =>
#     same range as t
{'cells_param_size': {'t': 900, 'n': 842, 'm': 900}}
