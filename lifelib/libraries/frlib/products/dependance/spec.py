# Dep_FR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 842: need_max 840; check_states sweeps range(proj_len()+1) (:1927) and
#   y < 73: policy year y = duration(t)+1 (:667); premium_factor(policy_year(t)), t<=840 -> y<=71 -> 72 exclusive,
#   z < 843: claim duration cohorts 1..max_dur(); max_dur (:682) = proj_len()+claim_duration_months()+1; z0 <=
#   n < 72: reduction_coeff(n) (:842), n = years_paid() or years_premiums_paid(t-1)=(t)//12 <= 70 = 110-40 -> 71
#   y_e < 73: shipped declaration
{'cells_param_size': {'t': 842, 'y': 73, 'z': 843, 'n': 72, 'y_e': 73}}
