# LTC_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   x < 121: mort_table.csv age keys 30..120; mort_rate_at_age clamps to min(x, 120) (:453); int x = age(t)
#     <= term_age = 90 (:469,:928-938,:1030); bound 120+1
#   j < 71: shipped declaration
{'cells_param_size': {'x': 121, 'j': 71}}
