# mx2cy's spec for MYGA_US_SEC: the length of each C-array cache in Projection, by the
# cells' parameters (USLIB-SEC-PLAN.md F4, section 6.1 step 6).  A compiled cache raises
# IndexError for an argument outside [0, size), so each size covers the largest argument
# any cell is called with on a point the contract allows, in its frame and in the month
# after it, t = proj_len(), which the roll-forwards read and C4's full sweep evaluates
# every monthly cell at; plus one because the index starts at 0; and one of headroom where
# that leaves room.  mx2cy keys a size by a cell's parameter names, so every cell taking t
# alone shares one.  The contract is three References and one of Data's.
# Projection.proj_len refuses a point issued below issue_age_min, 0, the youngest issue
# age product-spec.md admits (and one issued above issue_age_max, 85, which sizes
# nothing: an older issue only shortens every frame); cover ends at maturity_age, 100;
# and Data refuses a point issued more than future_horizon_mth, 120 months, after the
# valuation date.  So no point a report projects outruns these sizes, and a change to
# issue_age_min, maturity_age or future_horizon_mth needs them recomputed here and the
# model rebuilt.
#
# t, months from the valuation date.  The longest frame is a contract issued at 0, covered
# to 100, 12 * (100 - 0) = 1,200 months, and issued 120 months on: t = 0 .. 1,319, and
# 1,320 in the month after.  There check_pols_roll_fwd_resid, and av_change through
# av_at(t, EOM), read pols_if_at(t + 1, BEF_NB), 1,321: so 1,322, and no headroom.  A
# longer future_horizon_mth, a higher maturity_age or a lower issue_age_min needs t raised
# to 12 * (maturity_age - issue_age_min) + the horizon + 2.  Data.read_last_mth, the last
# month the scenario and withdrawal arrays hold, is the last t, 1,321, and moves with it.
# timing, beside t in pols_if_at, av_pp_at and av_at: BEF_NB 0 to EOM 7, one numbering for
# the count's five timings and the account value's three, and no more, so a code past them
# raises IndexError: (1,322, 8).
# kind, beside t in pols_decr, claim_pp, claim_from_av_pp, claims, claims_from_av and
# claims_over_av: DEATH 0 to MATURITY 3 and ALL 4, sized 8 all the same: (1,322, 8).
# name, beside t in scenario_rate: MVA_REF_YIELD 0 and MARKET_RATE 1, sized 8 all the
# same: (1,322, 8).  Every 2-D cache of a model has one inner width, timing's here,
# because Cython's generated unpickle code converts the 2-D caches of a space with one
# function, written for one width: given two widths, it passes the narrower array where
# the wider is expected, which gcc 14 refuses (-Wincompatible-pointer-types, made an error
# on every gcc and clang by tools/build_sec_cy.py), and would write past its end.  So a
# kind 5 to 7, a name 2 to 7, or a timing a cell does not take, is inside the cache, where
# the cell refuses it as modelx does, ValueError("invalid kind"), ("invalid name") or
# ("invalid timing"), and a code from 8 raises IndexError, compiled alone.
# y, a contract year, read by free_wd_base and free_wd_allow in cover alone: 1 .. 100 at
# issue age 0: 101, and one of headroom, 102.  A higher maturity_age or a lower
# issue_age_min needs y raised to maturity_age - issue_age_min + 2.
# a, an attained age, read by surr_charge_age_cap_at and mort_rate_at in cover alone:
# issue_age_min .. maturity_age - 1, 0 .. 99: 100, and one of headroom, 101.  It rests on
# issue_age_min only through its being 0 or more, which proj_len holds.  A higher
# maturity_age needs a raised to maturity_age + 1.
# The duration factors are read at whole years remaining in mva_duration_factor, keyed by
# t, through no cache of their own: those years run to the factor table's last and the
# guarantee period, data no contract bound holds.
{"spaces": {"Projection": {"cells_param_size": {
    "t": 1322, ("t", "timing"): (1322, 8), ("t", "kind"): (1322, 8),
    ("t", "name"): (1322, 8), "y": 102, "a": 101}}}}
