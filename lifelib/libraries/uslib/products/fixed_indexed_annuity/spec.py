# FIA_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 974: need_max 972 + 1 (pols_if(t+1) in av_at EOY line 2584 and check_pols_roll_fwd_resid line 2668) + 1
#   a < 121: attained age: payout_rate(exercise_age(t), ...) (line 1287), activation_rate(a) (line 1294, reported
#   y < 82: anniversary number: index_return uses index_level(duration(t)+1) (line 895), mva_rate uses
#     mva_ref_yield(duration(t)+1) (line 1920); duration <= 971//12 = 80, so y <= 81, bound 82. scenario_value
#     clamps via index.asof (rate_scenario.csv t column)
{'cells_param_size': {'t': 974, 'a': 121, 'y': 82}}
