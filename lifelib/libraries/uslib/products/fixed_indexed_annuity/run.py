"""Run the FIA_US_S reference model and print its cash flow statement.

The projection steps monthly; the contract is annual, so the account value and rider
traces are printed at the anniversary months and the cash flows are summed into contract
years by ``result_cf_annual()``.

    python products/fixed_indexed_annuity/run.py            # anchor cell (point_id = 1)
    python products/fixed_indexed_annuity/run.py 2          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "FIA_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
entry, first = proj.entry_year(), proj.entry_mth()
print("model point {}: {} - {}{} {} premium {:,.0f}, bonus {:.0%}, {} indexed".format(
    point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(), proj.tax_status(),
    proj.premium_pp(), proj.bonus_rate(), "{:.0%}".format(proj.alloc_indexed())))
print("entered {} at anniversary {}: AV {:,.2f}  BB {:,.2f}  MGV {:,.2f}".format(
    "in force" if entry else "at issue", entry,
    proj.av_pp_at(first, "BEF_INV"), proj.benefit_base_pp_at(first, "BEF_ROLLUP"),
    proj.mgsv_pp_init()))
print("GLWB {}  basis {}  income from age {}  utilization {:.0%}  "
      "cap {:.2%}  rollup {}  stack {:.2f}x".format(
          "elected" if proj.glwb_elected() else "not elected", proj.glwb_basis(),
          proj.income_start_age(), proj.utilization_intensity(),
          proj.cap_rate_in_force(), proj.rollup_id(), proj.stack_factor()))

anniversaries = [t for t in range(first, proj.proj_len()) if proj.is_anniv(t)]
exercise = [t for t in anniversaries if proj.is_exercise(t)]
depleted = [t for t in anniversaries
            if proj.phase(t) in ("DEPLETED", "TERMINATED")]
last = proj.proj_len() - 1
print("months t = {}..{} (contract years {}..{}, to attained age {}); "
      "first lifetime withdrawal {}; account value runs out {}".format(
          first, last,
          proj.policy_year(first), proj.policy_year(last),
          proj.age(last) + 1,
          "in contract year {}".format(proj.policy_year(exercise[0]))
          if exercise else "never",
          "in contract year {} ({})".format(proj.policy_year(depleted[0]),
                                            proj.phase(depleted[0]))
          if depleted else "never"))
print("every contractual event falls in an anniversary month, t = 12k + 11; "
      "the rows below are those months")
print()

print("account value, benefit base and lifetime withdrawal (per contract),")
print("at the anniversary closing each of the first fourteen contract years:")
cols = ["av_pp_bef_inv", "index_credit_pp", "rider_charge_pp", "wd_pp", "av_pp", "mgsv_pp"]
av = proj.result_av().loc[anniversaries[:14], cols]
bb = proj.result_glwb().loc[anniversaries[:14], ["benefit_base_pp", "lw_pp", "phase"]]
print(av.join(bb).round(2).to_string())
print()

print("cash flows, summed into contract years:")
print(proj.result_cf_annual().head(14).round(2).to_string())

model.close()
