"""Run the Cancer_KR_S reference model and print its cash flow statement.

    python products/cancer/run.py            # anchor cell (point_id = 1)
    python products/cancer/run.py 4          # another model point

This file and everything it prints are ASCII-only, so the output lands on a Windows
console under any code page. Korean terms are romanized (Revised Romanization) rather
than written in hangul: the product is "am boheom" (cancer insurance), the four
diagnosis tiers are "gohaek-am" (high-cost cancer, a top-up), "ilban-am" (general
cancer), "teukjeong soaek-am" (named small-amount cancer) and "yusa-am" (similar
cancer, the reduced tier), the waiting period is the "myeonchaek gigan" and the
reduced-benefit period the "gamaek gigan", the suppressed surrender-value form is
"haeyak hwangeupgeum mijigeuphyeong", the two chassis are "bi-gaengsin"
(non-renewable) and "gaengsin" (renewable), the account paid on death is the
"gyeyakja jeoklipaek", and amounts are labelled KRW rather than carrying a currency
sign. The age basis is "man nai" (age last birthday).
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Cancer_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
chassis = ("gaengsin (10-year renewable)" if proj.chassis() == "gaengsin"
           else "bi-gaengsin (non-renewable)")
pay = ("jeongi-nap (whole-term pay)" if proj.pay_term() == 0
       else "{}-year pay".format(proj.pay_term()))
form = ("pyojunhyeong (conventional surrender value)"
        if proj.cv_form() == "pyojun"
        else "mijigeuphyeong (no surrender value while paying)")
modules = "diag={} hosp={} surg={} treat={}".format(
    proj.diag_module(), proj.hosp_module(), proj.surg_module(), proj.treat_module())

print("Cancer_KR_S - am boheom (cancer insurance), KRW, monthly grid, man nai")
print("model point {}: {} - {}{}, {}".format(
    point_id, proj.policy_id(), proj.sex(), proj.issue_age(), chassis))
print("  cover to man nai {}, {}, {}, sum insured KRW {:,.0f}".format(
    proj.expiry_age(), pay, form, proj.sum_assured()))
print("  premium = KRW {:,.0f}/month   frame = {} rows (t = 0 .. {})   "
      "myeonchaek = {} m   gamaek = {} m".format(
          proj.premium_mth_pp(), proj.proj_len(), proj.proj_len() - 1,
          proj.tier_wait_months("general"), proj.reduction_months()))
print("  tiers: gohaek {:.0%} top-up / ilban {:.0%} / soaek {:.0%} / yusa {:.0%}"
      " of the sum insured".format(
          proj.benefit_ratio("high"), proj.benefit_ratio("general"),
          proj.benefit_ratio("minor"), proj.benefit_ratio("similar")))
print("  modules: {}   waiver = {}".format(modules, proj.waiver_trigger()))
print("  pyojun haeyak gongjeaek (standard surrender charge cap) = KRW {:,.0f}".format(
    proj.surr_chg_cap_pp()))
print()

df = proj.result_cf()
cols = ["pols_if", "pols_healthy", "pols_minor", "pols_waived", "premiums",
        "claims_diag_gen", "claims_diag_high", "claims_diag_minor",
        "claims_diag_similar", "claims_hosp", "claims_surgery", "claims_treat",
        "claims_death", "claims_lapse", "claims_maturity", "expenses",
        "claim_expenses", "commissions", "net_cf"]
print(df[cols].head(12).round(4).to_string())
if len(df) > 12:
    print("... {} further months to t = {}".format(
        len(df) - 12, proj.proj_len() - 1))
print()

claim_cols = [c for c in df.columns if c.startswith("claims_")]
print("undiscounted totals over the whole projection (per policy issued):")
print("  premiums          {:>16,.2f}".format(df["premiums"].sum()))
print("  claims, diagnosis {:>16,.2f}".format(
    df[["claims_diag_gen", "claims_diag_high", "claims_diag_minor",
        "claims_diag_similar"]].sum().sum()))
print("  claims, care      {:>16,.2f}".format(
    df[["claims_hosp", "claims_surgery", "claims_treat"]].sum().sum()))
print("  claims, account   {:>16,.2f}".format(
    df[["claims_death", "claims_lapse", "claims_maturity"]].sum().sum()))
print("  claims, all       {:>16,.2f}".format(df[claim_cols].sum().sum()))
print("  expenses          {:>16,.2f}".format(
    df["expenses"].sum() + df["claim_expenses"].sum()))
print("  commissions       {:>16,.2f}".format(df["commissions"].sum()))
print("  net_cf            {:>+16,.2f}".format(df["net_cf"].sum()))
print()
print("  note: these are gross UNDISCOUNTED cash flows. On a contract whose premium")
print("  stops at the end of the payment term and whose cover runs to man nai 100,")
print("  the undiscounted net_cf is negative by construction; discounting, the")
print("  chaekimjunbigeum and the IFRS 17 CSM belong to a layer that consumes this")
print("  output rather than to this model.")
print()
print("checks:")
for name in sorted(c for c in model.Projection.cells
                   if c.startswith("check_") and not c.endswith("_resid")):
    print("  {:<26} {}".format(name, getattr(proj, name)()))

model.close()
