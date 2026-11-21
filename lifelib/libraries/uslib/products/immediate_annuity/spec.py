# SPIA_US_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1226: need_max 1224 + 1 (lives_if(t+1) / lives_if_last(t+1), lines 742, 768, 849, 1227;
#     cum_annuity_pp(t+1) via claim_pp line 1050) + 1 margin = 1226
#   y < 104: policy_year(t) = t//12 + 1 <= 1225//12 + 1 = 103 (calls at lines 575, 962, 1009, 1074); +1 =
#     104. surr_charge_rate clamps y to surr_charge_table.csv policy_year range (line 994)
#   k < 1226: month index; k reaches proj_len() (check_lives_roll_fwd range(proj_len()+1), line 1174;
#     lives_if(t+1)); 1224+1+1
{'cells_param_size': {'t': 1226, 'y': 104, 'k': 1226}}
