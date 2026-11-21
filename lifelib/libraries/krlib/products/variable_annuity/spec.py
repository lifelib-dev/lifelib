# VA_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1273: need_max 1260 + 1 for pols_if(t + 1)/pols_if(t+1) at t = proj_len-1 + 12 margin
#   x < 121: mort_table.csv age keys 15..120 (mort_rate_at_age :1180, ann_mort_rate_at_age :1167);
#     risk_prem_table.csv age_from asof lookup (:660, keys from 15); x = age(t) <= 120 at t = proj_len;
#     ann_surv reads annuity_age()+k-1 <= 118; bound 120+1
#   k < 75: completed payout years: annuity_factor sums ann_surv(k) for k in range(0, omega_age -
#     annuity_age()) (:1340-1346), max with 연금개시나이 min 45 (product-spec.md:156): 120-45-1 = 74;
#     credit_rate/decl_rate/min_guar_rate called with k = 0 (:1164) via crediting_table.csv dur_from asof;
#     bound 74+1
#   y < 108: policy year in comm_rate(policy_year(t)) (:1484), y <= proj_len//12 + 1 = 106 at t = proj_len;
#     +1 exclusive, +1 year margin (matches t margin). Non-zero only for y <= 5 (:1456)
{'cells_param_size': {'t': 1273, 'x': 121, 'k': 75, 'y': 108}}
