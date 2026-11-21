# Child_KR_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 1334: need_max 1321 + 1 for pols_if(t + 1)/frac_open(t+1) at t = proj_len-1 + 12 margin
#   x < 121: mort_table.csv age keys 0..120; mort_rate_at_age(x, s) :675 clamps the lookup to
#     min(max(x,0),120) (:684); insured 만나이 <= 110 (term_age 110), inc_rate_at(min(age_man(t),100), cause)
#     :869, payer_age()+t//12 :714 only for t <= prem_end (20년납, product-spec.md:310), ref_age = 40 (:2315);
#     bound = 120+1
{'cells_param_size': {'t': 1334, 'x': 121}}
