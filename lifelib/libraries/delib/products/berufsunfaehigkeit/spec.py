# BU_DE_S: declared parameter ranges (cells_param_size, model level) from the product limits; a
# (lower, stop) pair where the parameter is an absolute value. Sources (model folder, product-spec.md):
#   t < 625: t runs 0..proj_len() inclusive: pols_actv/pols_if return 0 only for t > proj_len() (line 1396),
#     check_states loops range(0, proj_len()+1) (line 1928), pols_if_at(t, END) and the roll-forward checks
#     read pols_if(t+1) at t=proj_len()-1 (lines 1697, 1945). Max index = 624, exclusive bound 624+1 = 625.
#     NOTE: t is also NEGATIVE: rente_pay_pp(t, z0) calls bu_rente_pp(t - z0) with z0 = seed_claim_dur() =
#     claim_duration_init()+1 (lines 1050, 1468) and duration_mth/policy_year/dyn_factor are documented for
#     negative t (traced lo = -9); the lowest t is -(claim_duration_init+1) >= -first_len() = -624.
#   s < 625: first-order run s = 0..first_len() inclusive: pols_actv_first admits s == first_len() (line
#     1156 'if s < 0 or s > first_len()'), *_first ledgers read s-1. first_len max = 12*(67-15) = 624 -> bound
#     625.
#   z < 626: claim-duration cohort index 1..max_claim_dur(): max_claim_dur() = proj_len() + seed_claim_dur()
#     + 1 (line 681), seed_claim_dur() = claim_duration_init()+1 (line 667). Since the onset follows
#     inception, claim_duration_init <= duration_init_months - 1, so proj_len + seed_claim_dur + 1 <=
#     12*(cover_end_age-entry_age) + 1 = 625; first run cohort_len_first <= first_len()+1 = 625 (line 701).
#     Max z = 625 -> bound 626. claim_year(z) caps at 11 (line 658) so values beyond are harmless.
#   x < 71: x = age(t) = entry_age + max(0,duration_mth(t))//12 (line 640) reaches cover_end_age (67,
#     product-spec.md:134) at t = proj_len(); lookups clamp to the table (lines 711-740). Max table key:
#     mortality_table.csv age 70 (inception_table.csv max 66) -> bound max(67+1, 70+1) = 71.
{'cells_param_size': {'t': 625, 's': 625, 'z': 626, 'x': 71}}
