# Term_UK_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 612: need_max 600 + t+1 offset -> 601 required; +12 margin => 612.
#   m < 612: annuity_certain_factor(m) called with m = term_mths() - t (fib_commute_pp, Projection:930); t
#     in [proj_start, proj_len) -> m in 1..600 -> 601 exclusive; shares 612. m <= 0 only if t >= term_mths
#     (returns 0).
#   k < 612: benefit_sched(k) called with k = duration_mth(t) = t (benefit_pp, Projection:942) for t <
#     proj_len -> k <= 599; shares the t bound 612.
{'cells_param_size': {'t': 612, 'm': 612, 'k': 612}}
