# Pension_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1465: need_max 1452 + 1 for pols_if(t + 1)/av_pp(t + 1)/cv_pp_net(t + 1) at t = proj_len-1 + 12
#     margin; annuity window min(t + 12, proj_len()) (:1938) stays inside
#   x < 122: mort_table.csv age keys 0..120 per (table, sex); mort_rate_at_age(table, x) :836 returns 1.0
#     without a read for x >= omega_age = 120; x = age(t) (:849) reaches x0 + proj_years = 121 at t =
#     proj_len; annuity_due_factor_on loops x0+j <= omega (:1330); bound = 121+1 (mort_rate_law(table, x) :820
#     forms the float x - age_setback internally; its argument is the int age)
{'cells_param_size': {'t': 1465, 'x': 122}}
