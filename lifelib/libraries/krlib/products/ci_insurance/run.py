"""Run the CI_KR_S reference model and print its cash flow statement.

    python products/ci_insurance/run.py            # anchor cell (point_id = 1)
    python products/ci_insurance/run.py 4          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: amounts are
KRW, the product is written "CI boheom (jungdae jilbyeong boheom, critical illness)"
rather than in hangul, the acceleration is "seonjigeup biyul", and the suppressed
surrender-value form is "jeohaeji hwangeup-hyeong".
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "CI_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
k = proj.cv_floor_ratio()
form = ("gibon hwangeup-hyeong (k = 1.00)" if k >= 1.0
        else "muhaeji hwangeup-hyeong (k = 0.00)" if k <= 0.0
        else "jeohaeji hwangeup-hyeong, k = {:.2f}".format(k))

print("CI_KR_S - CI boheom (jungdae jilbyeong boheom, critical illness), monthly grid")
print("age basis: boheom nai (insurance age, six-month rounding)")
print("model point {}: {} - {}{}, cover KRW {:,.0f}, {}-year premium term, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.sum_assured(), proj.prem_term(), form))
print("seonjigeup biyul a = {:.2f}   residual r = {:.2f}   account floor c = {:.2f}   "
      "first-year reduction: {}".format(
          proj.accel_rate(), proj.resid_rate(), proj.resid_floor_mult(),
          proj.first_year_scope()))
print("gross premium = KRW {:,.2f}/month ({:,.2f} p.a.)   net level premium = "
      "KRW {:,.2f}/month ({:,.2f} p.a.)".format(
          proj.premium_mth_pp(), proj.premium_pp(),
          proj.prem_net_level_mth_pp(), proj.prem_net_level_pp()))
print("projection = {} months ({} years, t = 0 .. {}) to attained age {}   CI cover runs "
      "{} months ({} years), to age 100".format(
          proj.proj_len(), proj.proj_years(), proj.proj_len() - 1, proj.omega_age(),
          proj.ci_cover_end(), proj.ci_cover_end() // 12))
print("pyojun haeyak gongje-aek (statutory surrender-charge cap) = KRW {:,.2f}".format(
    proj.surr_chg_cap_pp()))
print("modules: lapse basis = {}   loan utilisation = {:.2%} at policy year {} "
      "(month-end {})   mort_be_factor = {:.2f}   ci_be_factor = {:.2f}   "
      "post-CI mortality x {:.2f}".format(
          proj.lapse_basis(), proj.pol_loan_util(), proj.pol_loan_year(),
          12 * proj.pol_loan_year(), proj.mort_be_factor(), proj.ci_be_factor(),
          proj.mort_ci_factor()))
print()

df = proj.result_cf()
rows = [t for t in range(13) if t < proj.proj_len()]
mm = proj.prem_period_mths()
rows += [t for t in (mm - 2, mm - 1, mm) if t < proj.proj_len() and t not in rows]
print("t is 0-based and counts months; policy year = t // 12 + 1.  The first policy year "
      "and the turn of it, and the months around napip wallyo:")
print(df.loc[sorted(rows)].round(2).to_string())
print()
print("undiscounted totals per policy issued (KRW):")
print(df.sum().round(2).to_string())
print()

val = proj.result_val()
print("the acceleration, at three gyeyak haedangil (per policy, KRW):")
for d in (60, 120, mm):
    if d > proj.proj_len():
        continue
    print("  month-end {:>3} = policy year {:>2} (the close of month t = {:>3})  "
          "account V = {:>14,.0f}   surrender pre-CI = {:>14,.0f}   "
          "post-CI = {:>14,.0f}".format(
              d, d // 12, d - 1, val.loc[d - 1, "pol_val_pp"], val.loc[d - 1, "cv_pp"],
              val.loc[d - 1, "cv_pp_ci"]))
    print("          accelerated a*B = {:>10,.0f}   nominal residual r*B = {:>12,.0f}   "
          "loan limit pre/post = {:,.0f} / {:,.0f}".format(
              val.loc[d - 1, "accel_benefit_pp"], val.loc[d - 1, "resid_nominal_pp"],
              proj.loan_avail_pp(d), proj.loan_avail_ci_pp(d)))
print()

print("checks: pols {}  ci states {}  decrements {}  account {}  complement {}".format(
    proj.check_pols_roll_fwd(), proj.check_ci_state_roll_fwd(),
    proj.check_decrement_sum(), proj.check_pol_val_roll_fwd(),
    proj.check_accel_complement()))
print("        residual floor {}  carve-out {}  loans {}  net cf {}".format(
    proj.check_resid_floor(), proj.check_cv_carve_out(),
    proj.check_loan_roll_fwd(), proj.check_net_cf()))

model.close()
