# Endowment_JP_S: declared parameter sizes (cells_param_size, model level), only where Probe A showed a
# policy valid for the product raising on the traced range. Sources (model folder, product-spec.md):
#   t < 722: need_max 720; max index 720 via pols_if(t+1) check_pols_roll_fwd_resid:1629 and pols_if_*_at(AFT_DECR);
#     exclusive 721 + 1 spare
#   u < 722: elapsed month u = t+1 (claims:1491-1493, death_ben_pp:1176-1179, dyn_lapse_factor:781-785) <= 12n =
#     720; exclusive 721 + 1 spare
#   z < 62: mort_table.csv age 0..60 (max 60); z = issue_age()+k up to x+n (endow_epv(x+n, 0) at k=n,
#     pol_val_at:995; annuity_due(x+k,...)) with x+n-1 <= 60 => z <= 61, +1
#   k < 62: anniversary k in 0..proj_years()=n (loops :1703-1751 range(proj_years()+1)); k+1 in
#     pol_val_pre_at_m:1116 / apl_advance_pp:1200 stays <= n; surv_prob(z,k) k <= n; n <= 60 (product-spec.md:96) =>
#     61 + 1 spare
{'cells_param_size': {'t': 722, 'u': 722, 'z': 62, 'k': 62}}
