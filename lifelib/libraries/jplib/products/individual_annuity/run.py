"""Run the Annuity_JP_S reference model and print its cash flow statement.

    python products/individual_annuity/run.py            # anchor cell (point_id = 1)
    python products/individual_annuity/run.py 4          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: the product
is written "kojin nenkin hoken" rather than in kana, and amounts are in JPY.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Annuity_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
form = ("{}-year kakutei nenkin (annuity-certain)".format(proj.payout_term_y())
        if proj.payout_form() == "certain"
        else "whole-life annuity with a {}-year guarantee".format(proj.guar_term_y()))

print("Annuity_JP_S - JPY, monthly grid")
print("model point {}: {} - kojin nenkin hoken (individual annuity), {}{}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.issue_age()))
print("premium = JPY {:,.0f} p.a. for {} years, then a {}-year deferral gap; "
      "annuity starts at age {}".format(
          proj.premium_pp(), proj.premium_term_y(), proj.defer_gap_y(),
          proj.annuity_start_age()))
print("payout form = {}   death benefit ratio = {:.2f}   tax rider = {}".format(
    form, proj.db_ratio(), proj.tax_rider()))
print("modules: APL = {}   policy loan = {}   commutation = {:.0%}   "
      "dividend = {:.3%}   new-business rate = {:.2%}".format(
          proj.apl_on(), proj.loan_on(), proj.commute_rate(),
          proj.div_rate(), proj.rate_new()))
print()
print("nenkin genshi (annuity fund) F   = JPY {:,.2f}".format(proj.annuity_fund_pp()))
print("annuity-due factor               = {:.8f}".format(
    proj.annuity_due_factor() if proj.payout_form() == "certain"
    else proj.annuity_due_life_factor()))
print("kihon nenkin gaku (annuity)  B   = JPY {:,.0f} p.a.".format(
    proj.annuity_amount_pp()))
print("mean lapse rate, count-weighted  = {:.4%}".format(proj.lapse_rate_mean("count")))
print("mean lapse rate, fund-weighted   = {:.4%}".format(proj.lapse_rate_mean("fund")))
print()

df = proj.result_cf()
n = proj.annuitisation_t()
print("cash flow statement, JPY per policy issued, income positive")
print("t is 0-based and counts policy MONTHS: the frame runs t = 0 .. {} ({} rows, "
      "12 to the policy year)".format(proj.proj_len() - 1, proj.proj_len()))
print("first 13 months, t = 0 .. 12 - note the premium falls in one month in twelve")
print(df.head(13).round(2).to_string())
print("...")
print("around the nenkin shiharai kaishi bi, t = n - 2 .. n + 2 (n = {})".format(n))
print(df.loc[n - 2:n + 2].round(2).to_string())
print("...")
print("last two months, t = {} .. {}".format(proj.proj_len() - 2, proj.proj_len() - 1))
print(df.tail(2).round(2).to_string())
print()
annual = df.groupby(df.index // 12).sum()
annual["pols_if"] = [proj.pols_if(12 * y) for y in annual.index]
annual.index.name = "policy year - 1"
print("the same statement grouped into policy years (pols_if at the anniversary):")
print(annual.round(2).to_string())
print()
print("undiscounted total net_cf        = JPY {:,.2f}".format(df["net_cf"].sum()))
for name in ("check_pols_roll_fwd", "check_lives_roll_fwd", "check_fund",
             "check_cv_cap", "check_annuity_total", "check_net_cf",
             "check_mort_graduation"):
    print("{:<24} {}".format(name + "()", getattr(proj, name)()))

model.close()
