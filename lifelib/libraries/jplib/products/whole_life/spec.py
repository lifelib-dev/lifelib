# WholeLife_JP_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1179: need_max 1177; max index 1177 via pols_if(t+1) check_pols_roll_fwd_resid:1737,
#     check_decrement_sum_resid:1775; exclusive 1178 + 1 spare
#   n < 100: annuity_due(y,n) n <= prem_period years, 終身払 = proj_years 99 (prem_period:394); max 99 + 1
#   y < 115: epv_death(y):847 recursion y+1 until y > omega_age (returns 0 at 114); annuity_due(y,n):860 y+1
#     to x+n <= 114; mort_rate_at_age(y) reads <= 113 (mort_table.csv max 113); max y 114 + 1
#   d < 101: anniversary d in range(proj_years()+1) (:1845,1972); proj_years:595 = 113-15+1 = 99; d+1 stays
#     <= 99; exclusive 100 + 1 spare
#   s < 100: APL cohort year s <= min(duration(t), prem_end()-1) (:1433,1447) <= proj_years-1 = 98;
#     exclusive 99 + 1 spare
#   u < 1179: u = t+1 <= 1177; exclusive 1178 + 1 spare
{'cells_param_size': {'t': 1179, 'n': 100, 'y': 115, 'd': 101, 's': 100, 'u': 1179}}
