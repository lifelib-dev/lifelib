"""Run the WholeLife_KR_S reference model and print its cash flow statement.

    python products/whole_life/run.py            # anchor cell (point_id = 1)
    python products/whole_life/run.py 8          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: amounts are
KRW, the product is written "jongsin boheom (whole life)" rather than in hangul, and the
suppressed-surrender-value forms are written "muhaeji hwangeuphyeong" (nil) and "jeohaeji
hwangeuphyeong" (low).  Ages are boheom nai, the Korean insurance age.

The time index t is 0-based and counts policy months: t = 0 is the first policy month,
the frame is t = 0 .. proj_len() - 1, and the contractual policy year is t // 12 + 1.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "WholeLife_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
k = proj.cv_floor_ratio()
if k >= 1.0:
    form = "pyojunhyeong (standard form), k = 1.00"
elif k <= 0.0:
    form = "muhaeji hwangeuphyeong (nil surrender value), k = 0.00"
else:
    form = "jeohaeji hwangeuphyeong (low surrender value), k = {:.2f}".format(k)
term = ("jeongi-nap (whole-of-life premium)" if proj.prem_term() == 0
        else "{}-year premium term".format(proj.prem_term()))

print("WholeLife_KR_S - jongsin boheom (whole life), monthly grid, boheom nai")
print("model point {}: {} - {}{}, cover KRW {:,.0f}, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.sum_assured(), term))
print("form: {}   premium ratio to standard form {:.3f}".format(
    form, proj.prem_susp_ratio()))
print("premium = KRW {:,.2f}/month ({:,.2f} p.a.; model rule gives {:,.2f} p.a.)   "
      "projection = {} months ({} years) to attained age {}".format(
          proj.premium_mth_pp(), proj.premium_pp(), proj.prem_gross_calc_pp(),
          proj.proj_len(), proj.proj_years(), proj.omega_age()))
print("basis: pricing rate {:.3%}   accrual rate {:.3%}   policy loan rate {:.3%}   "
      "lapse basis {}".format(
          0.025, proj.acc_int_rate(), proj.loan_int_rate(), proj.lapse_basis()))
print("net level premium: monthly P = KRW {:,.2f} (yeonnap equivalent {:,.2f} p.a.)   "
      "pyojun haeyak gongjeaek (statutory surrender charge cap) = KRW {:,.2f}".format(
          proj.prem_net_level_mth_pp(), proj.prem_net_level_pp(),
          proj.surr_chg_cap_pp()))
print("acquisition cost = KRW {:,.2f} of which first-year commission KRW {:,.2f}   "
      "surrender-charge period = {} years".format(
          proj.acq_cost_pp(), proj.comm_init_pp(), proj.surr_chg_period()))
print("modules: waiver rate = {:.3%}   loan utilisation = {:.2f} at year {}   "
      "bonus = {:.3%}   reduction = {:.0%} at year {}   reinstatement = {:.2%}   "
      "mort_be_factor = {:.2f}".format(
          proj.waiver_rate(0), proj.loan_util(), proj.loan_year(), proj.bonus_rate(),
          proj.reduce_frac(), proj.reduce_year(), proj.reinstate_rate(),
          proj.mort_be_factor()))
print()

df = proj.result_cf()
m = proj.prem_period_mths()
rows = [t for t in (0, 1, 2, 11, 12) if t < proj.proj_len()]
rows += [t for t in (m - 2, m - 1, m) if 0 <= t < proj.proj_len() and t not in rows]
print("cash flow statement - t is 0-based and counts months, policy year = t // 12 + 1: "
      "the first months, the turn of the first policy year, and the months around napip "
      "wallyo (completion of premium payment):")
print(df.loc[sorted(rows)].round(2).to_string())
print()

val = proj.result_val()
print("surrender values on the same rows, at the month-end d = t + 1 that closes each "
      "month (KRW per policy):")
print(val.loc[sorted(rows)].round(2).to_string())
print()

print("undiscounted totals per policy issued (KRW):")
print(df.sum().round(2).to_string())
print()

print("checks:")
print("  policy count roll forward   {}".format(proj.check_pols_roll_fwd()))
print("  decrements sum to one       {}".format(proj.check_decrement_sum()))
print("  account roll forward        {}".format(proj.check_pol_val_roll_fwd()))
print("  account prospective form    {}".format(proj.check_pol_val_prosp()))
print("  surrender charge under cap  {}".format(proj.check_surr_chg_cap()))
print("  suppression and the cliff   {}".format(proj.check_cv_cliff()))
print("  policy loan roll forward    {}".format(proj.check_loan_roll_fwd()))
print("  acquisition cost under cap  {}".format(proj.check_acq_cost_cap()))
print("  net cash flow ledger        {}".format(proj.check_net_cf()))

model.close()
