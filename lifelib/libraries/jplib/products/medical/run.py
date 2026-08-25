"""Run the Medical_JP_S reference model and print its cash flow statement.

    python products/medical/run.py            # anchor cell (point_id = 1)
    python products/medical/run.py 3          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: the product
is written "iryo hoken" (medical insurance, third sector) and amounts are JPY.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Medical_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
chassis = {"shushin": "whole-of-life", "teiki": "10-year renewable"}[proj.chassis()]
prem_period = {"whole_life": "premiums for life",
               "to_65": "premiums to age 65"}[proj.prem_period_type()]

print("Medical_JP_S - iryo hoken (third-sector medical insurance), monthly grid")
print("model point {}: {} - {}{} {} chassis, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.issue_age(),
    chassis, prem_period))
print("daily amount = JPY {:,.0f}/day   per-hospitalization limit = {} days   "
      "aggregate limit = {:,.0f} days/limb".format(
          proj.daily_amount(), proj.limit_per_hosp(), proj.limit_agg()))
print("premium = JPY {:,.2f}/month   surgery {:.0f}x in hospital / {:.0f}x outpatient   "
      "projection = {} months to age {}".format(
          proj.premium_mth_pp(), proj.surg_mult_ih(), proj.surg_mult_op(),
          proj.proj_len(), proj.issue_age() + proj.proj_len() // 12 - 1))
print("modules: five-day minimum = {}   advanced-medicine rider = {}   "
      "lump-sum rider = {}".format(
          proj.min_days_5(), proj.adv_rider(), proj.lump_rider()))
print("         3-disease unlimited = {}   3-disease waiver = {}   "
      "surgery paid after the day limit = {}".format(
          proj.tokusoku_3dis(), proj.waiver_3dis(), proj.surg_after_limit()))
print()

print("Cash flow statement, first 13 months (JPY; net_cf is income-positive)")
print(proj.result_cf().head(13).round(2).to_string())
print()

print("Benefit-day and rider ledgers, per surviving policy, first 13 months")
print(proj.result_days().head(13).round(4).to_string())
print()

annual = proj.result_cf().groupby(proj.result_cf().index // 12).sum()
annual.index.name = "policy_year_less_1"
print("Policy year totals, first 5 years (sums of unrounded monthly values)")
print(annual.head(5).round(2).to_string())
print()

print("Roll-forward and ledger identities: {}".format(
    "  ".join("{} = {}".format(c, getattr(proj, c)())
              for c in ("check_pols_roll_fwd", "check_agg_days", "check_day_limits",
                        "check_adv_ledger", "check_lump_ledger",
                        "check_waiver_roll_fwd", "check_net_cf"))))

model.close()
