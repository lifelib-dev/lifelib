# Sofort_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 853: t = t_start()..proj_len(): loops range(t_start(), proj_len()) (lines 1247-1531), lives_death(t)
#     and check_lives_roll_fwd_resid read lives_if(t+1) at t = proj_len()-1 (lines 706, 1261). Max t = 852 ->
#     bound 853 (single-life only: 733).
#   x < 157: x = age(t, life) = entry_age(life) + t//12 (line 539-547) passed to mort_rate_gen /
#     mort_rate_at_age / improve_rate_at_age (lines 570-635, 648, 675); lookups clamp to the table (lines 582,
#     608) so x is NOT limited by the table (max key 120). The annuitant keeps being evaluated over the whole
#     frame: max x = 85 (max entry age, product-spec.md:168) + 852//12 = 156 (survivor aged 50); single life
#     max = 85 + (12*15+12*30+12)//12 = 131. Bound 156+1 = 157.
#   k < 853: tariff_lives(k, life) with k = t+1 for t in range(0, proj_len()) (annuity_pp_derived /
#     refund_pv, lines 847-848, 888-889): max k = proj_len() = 852 -> bound 853.
{'cells_param_size': {'t': 853, 'x': 157, 'k': 853}}
