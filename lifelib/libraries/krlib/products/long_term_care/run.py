"""Run the LTC_KR_S reference model and print its cash flow statement.

    python products/long_term_care/run.py            # anchor cell (point_id = 1)
    python products/long_term_care/run.py 5          # another model point

The product is ganbyeong boheom (long-term-care insurance), the je-3-boheom contract of
boheomeop-beop art.4(1)3 whose benefit trigger is the public scheme's own janggi-yoyang
grade under the noin janggi-yoyang boheom beop. Output is ASCII-only so it prints on a
Windows console under any code page: amounts are KRW, ages are man-nai (age last birthday),
and the grade thresholds are printed as the codes the input tables use - g1 is 1deunggeup
only, g2 is 1~2deunggeup, through to g6 for 1~injijiwon-deunggeup.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "LTC_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - ganbyeong boheom, {}{} man-nai, to age {}, {}-year pay, "
      "frame = {} rows (t = 0 .. {})".format(
          point_id, proj.policy_id(), proj.sex(), proj.issue_age(), proj.term_age(),
          proj.prem_period_years(), proj.proj_len(), proj.proj_len() - 1))
print("lump {:,.0f} KRW at {}   annuity {:,.0f} / {:,.0f} KRW per month x{} months "
      "({} guaranteed), on = {}".format(
          proj.lump_amount(), proj.benefit_grade(), proj.annuity_high(),
          proj.annuity_low(), proj.annuity_max_mths(), proj.annuity_guar_mths(),
          proj.annuity_on()))
print("premium = {:,.2f} KRW/month ({:,.2f} p.a.)   uw loading = {:.2f}   "
      "dementia rider = {}   wait = {} mths   reduction = {} mths".format(
          proj.premium_mth_pp(), 12 * proj.premium_mth_pp(), proj.uw_loading(),
          proj.dementia_rider(), proj.wait_mths(), proj.red_mths()))
print("cv form = {}   lapse form = {}   net premium ratio = {:.4f}   "
      "care mortality multiple = {:.2f}".format(
          proj.cv_form(), proj.lapse_form(), proj.net_prem_ratio(),
          proj.care_mort_mult))
print()

df = proj.result_cf()
cols = ["pols_if", "pols_care", "premiums", "claims_lump", "claims_annuity",
        "claims_death", "claims_lapse", "expenses", "claim_expenses",
        "commissions", "net_cf"]
print("first 13 policy months, t = 0 .. 12 (columns claims_dementia, claims_void and "
      "claims_maturity omitted here; result_cf() carries them):")
print(df.head(13)[cols].round(2).to_string())
print()
print("policy year 1 totals, t = 0 .. 11 (unrounded sums):")
year1 = df.head(12).sum()
for col in ("premiums", "claims_lump", "claims_annuity", "claims_death",
            "claims_lapse", "claims_void", "expenses", "claim_expenses",
            "commissions", "net_cf"):
    print("  {:<16} {:>18,.2f}".format(col, year1[col]))
print()
total = df.sum()
benefits = (total["claims_lump"] + total["claims_annuity"] + total["claims_dementia"])
print("whole projection, undiscounted:")
print("  premiums          {:>18,.2f}".format(total["premiums"]))
print("  ltc benefits      {:>18,.2f}".format(benefits))
print("  gyeyakja-jeongnipaek on death "
      "{:>7,.2f}".format(total["claims_death"]))
print("  haeyak-hwangeupgeum on lapse  "
      "{:>7,.2f}".format(total["claims_lapse"]))
print("  expenses + commission "
      "{:>15,.2f}".format(total["expenses"] + total["claim_expenses"]
                          + total["commissions"]))
print("  net_cf            {:>18,.2f}".format(total["net_cf"]))
print("  lives ever certified at the benefit grade: {:.5f}".format(
    sum(proj.pols_entry_care(t) for t in range(proj.proj_len() - 1))))
print()
print("model incidence over the disclosed yejeong-wiheomnyul, first-entry basis:")
for x in (40, 50, 60):
    print("  man-nai {}: ratio {:.3f}".format(x, proj.disclosed_inc_ratio_at(x)))
print()
print("checks: pols_roll_fwd={} nesting={} ann_ledger={} av_continuity={} "
      "cv_form={} net_cf={}".format(
          proj.check_pols_roll_fwd(), proj.check_nesting(), proj.check_ann_ledger(),
          proj.check_av_continuity(), proj.check_cv_form(), proj.check_net_cf()))

model.close()
