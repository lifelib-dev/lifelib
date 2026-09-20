"""Run the Medical_KR_S reference model and print its cash flow statement.

    python products/indemnity_medical/run.py            # anchor cell (point_id = 1)
    python products/indemnity_medical/run.py 8          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: the product
is written "silson uiryo boheom" (indemnity medical insurance), the two priced units are
"geubyeo" (covered by National Health Insurance) and "bigeubyeo" (not covered), and
amounts are KRW.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Medical_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
cf = proj.result_cf()

print("Medical_KR_S - silson uiryo boheom (4th-generation indemnity medical), "
      "monthly grid")
print("model point {}: {} - {}{} (man nai, age last birthday), {}".format(
    point_id, proj.model_point()["label"], proj.sex(), proj.issue_age(),
    "inside National Health Insurance" if proj.nhi_covered()
    else "outside National Health Insurance (40 pct reimbursement)"))
ceiling = ("KRW {:,.0f} (decile {})".format(proj.oop_ceiling(), proj.oop_decile())
           if proj.nhi_covered() else "not applicable outside the scheme")
print("annual limit = KRW {:,.0f} per bojang jongmok   per-visit cap = KRW {:,.0f}   "
      "boninbudam sanghanaek = {}".format(
          proj.annual_limit(), proj.visit_cap(), ceiling))
print("first-year premium = KRW {:,.2f}/month, split geubyeo {:,.2f} / "
      "bigeubyeo {:,.2f}".format(
          proj.premium_mth_pp(), proj.prem_ge_base(1), proj.prem_np_base(1)))
print("retention: geubyeo {:.0%} inpatient, bigeubyeo {:.0%} inpatient;   "
      "projection = {} months, {} policy years to age {}".format(
          proj.retain_rate_ge(), proj.retain_rate_np(), proj.proj_len(),
          proj.policy_year(proj.proj_len() - 1),
          proj.age(proj.proj_len() - 1)))
print("modules: bigeubyeo rider = {}   3-dae bigeubyeo = {}   yoyul sangdaedo = {}   "
      "musago halin = {}".format(
          proj.np_rider(), proj.three_np(), proj.reld_on(), proj.noclaim_on()))
print("         suspension rate = {:.2%}   cost-trend multiplier = {:.2f}   "
      "utilisation multiplier = {:.2f}".format(
          proj.suspend_rate(), proj.trend_mult(), proj.util_mult()))
print()

print("Cash flow statement, first 13 months (KRW; net_cf is income-positive)")
print(cf.head(13).round(2).to_string())
print()

annual = cf.groupby(cf.index // 12 + 1).sum()
annual.index.name = "policy_year"
print("Policy year totals (sums of unrounded monthly values)")
print(annual.round(2).to_string())
print()

print("Renewal and experience-rating ledger, one row per policy year")
print(proj.result_prem().round(6).to_string())
print()

claim_cols = [c for c in cf.columns if c.startswith("claims_")]
print("Undiscounted totals over the projection (KRW)")
print("  premiums        {:16,.2f}".format(cf["premiums"].sum()))
print("  claims          {:16,.2f}".format(cf[claim_cols].sum().sum()))
print("  expenses        {:16,.2f}".format(cf["expenses"].sum()))
print("  claim_expenses  {:16,.2f}".format(cf["claim_expenses"].sum()))
print("  commissions     {:16,.2f}".format(cf["commissions"].sum()))
print("  net_cf          {:16,.2f}".format(cf["net_cf"].sum()))
print("  loss ratio      {:16.4f}".format(
    cf[claim_cols].sum().sum() / cf["premiums"].sum()))
print()

checks = sorted(c for c in model.Projection.cells
                if c.startswith("check_") and not c.endswith("_resid"))
print("Roll-forward and contractual identities")
for name in checks:
    print("  {:26s} {}".format(name, getattr(proj, name)()))

model.close()
