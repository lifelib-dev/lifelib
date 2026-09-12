"""Run the VUL_US_S reference model and print its account value roll-forward.

    python products/variable_ul/run.py            # anchor cell (point_id = 1)
    python products/variable_ul/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "VUL_US_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {} face {:,.0f} option {} {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.rate_class(), proj.sum_assured(), proj.db_option(), proj.qual_test()))
print("planned premium {:,.2f}/yr, load {:.0%}   M&E {:.2%}/yr   "
      "fixed option {:.2%} (floor {:.2%})".format(
          proj.premium_pp_ann(), proj.load_prem_rate(), proj.me_rate_ann,
          proj.crediting_rate_ann(0), proj.guar_rate_ann))
print("subaccounts: " + "  ".join(
    "{} e={:.2%} alloc {:.0%}".format(i, proj.fund_expense_ann(i), proj.alloc(i))
    for i in proj.subaccount_ids())
    + "   fixed alloc {:.0%}".format(proj.alloc_fixed()))
print("scenario {}   t = 0 gross returns {}   corridor(0) = {:.4f}   "
      "current COI(0) = {:.6f} per 1,000 NAAR".format(
          proj.scenario_id(),
          "/".join("{:+.2%}".format(proj.gross_return_mth(0, i))
                   for i in proj.subaccount_ids()),
          proj.corridor_factor(0), proj.coi_rate(0)))
print("surrender charge {:,.2f} in policy year {} (t = 0 is {} completed months "
      "after issue)   loan {:.2%} charged / {:.2%} credited on debt {:,.2f}".format(
          proj.surr_charge_pp(0), proj.policy_year(0), proj.duration_mth_init(),
          proj.loan_rate_ann(0), proj.loan_cr_rate_ann(0), proj.loan_bal_init()))
print("projection = {} projected months, t = 0 .. {}, to attained age {}   "
      "dynamic behavior module {}".format(
          proj.proj_len(), proj.proj_len() - 1, proj.age(proj.proj_len() - 1),
          "on" if proj.dyn_behavior_on else "off"))

shortfall = proj.first_shortfall_month()
print("first deduction shortfall: {}   account value roll-forward closes: {}".format(
    "projected month t = {}".format(shortfall) if shortfall >= 0 else "none",
    proj.check_av_roll_fwd()))
if proj.corridor_factor(0) != proj.corridor_factor_at(proj.age(0)) \
        or proj.coi_rate(0) != proj.coi_rate_at(proj.policy_year(0)):
    print("NOTE: this model point pins the worked example's first-month (t = 0) "
          "corridor factor and COI rate;")
    print("      the rule takes over from t = 1, so those two columns step there. "
          "Point 2 is the")
    print("      same cell without the pins. See README, 'The worked example's two "
          "age lookups'.")
print()
print("Account value roll-forward (per policy) - first 12 projected months, t = 0 .. 11")
print(proj.result_av().head(12).round(2).to_string())
print()
print("Liability cash flows, gross view - first 12 projected months, t = 0 .. 11")
print(proj.result_cf().head(12).round(2).to_string())

model.close()
