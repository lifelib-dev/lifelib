"""Run the Pension_KR_S reference model and print its cash flow statement.

    python products/pension_savings/run.py            # anchor cell (point_id = 1)
    python products/pension_savings/run.py 4          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: the product
is written "yeongeum jeochuk boheom" rather than in hangul, and amounts are in KRW.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Pension_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
form = ("jongsin yeongeumhyeong (life annuity) with a {}-year guarantee".format(
            proj.guar_term_y())
        if proj.payout_form() == "life_guar"
        else "hwakjeong gigan yeongeumhyeong (annuity-certain) over {} years".format(
            proj.payout_term_y()))

print("model point {}: {} - yeongeum jeochuk boheom "
      "(tax-qualified pension savings), {}{}".format(
          point_id, proj.model_point()["policy_id"], proj.sex(), proj.issue_age()))
print("age basis boheom nai (insurance age); t counts completed policy MONTHS from issue, "
      "0-based")
print("frame t = 0 .. {} ({} rows, {} policy years); policy year = t // 12 + 1".format(
    proj.proj_len() - 1, proj.proj_len(), proj.proj_years()))
print("gibon boheomryo (basic premium) = KRW {:,.0f}/month ({:,.0f} p.a.) for {} years, "
      "chuga nabip (additional) = KRW {:,.0f} p.a.".format(
          proj.prem_mth_pp(), proj.prem_pp(), proj.premium_term_y(),
          proj.addl_prem_pp()))
print("premium term ends at t = {}, annuity starts at t = {} (age {}), payout form = {}"
      .format(proj.prem_end_t(), proj.annuitisation_t(), proj.annuity_age_eff(), form))
print("modules: mortality vintage = {}   100.1% minimum fund = {}   "
      "surrender charge = {:.2%} of premium".format(
          proj.mort_vintage(), proj.min_fund_on(), proj.surr_chg_rate()))
print("         payment holiday = {} yrs   policy loan = {}   participating = {}   "
      "dividend = {:.3%}".format(
          proj.holiday_years(), proj.loan_on(), proj.par(), proj.div_rate()))
print("         lapse basis = {}   crediting-rate scenario = {}   "
      "gongsi iyul at t=0 = {:.2%}".format(
          proj.lapse_basis(), proj.rate_scenario(), proj.decl_rate(0)))
print()

n = proj.annuitisation_t()
print("cumulative premiums to t = n     = KRW {:,.2f}".format(proj.cum_prem_pp(n)))
print("gyeyakja jeongnibaek AV(n)       = KRW {:,.2f}".format(proj.av_pp(n)))
print("100.1% minimum fund              = KRW {:,.2f}".format(proj.min_fund_pp()))
print("annuity fund F, after the floor  = KRW {:,.2f}".format(proj.annuity_fund_pp()))
print("  net of loan, plus dividend     = KRW {:,.2f}".format(proj.annuity_fund_net_pp()))
print("annuity-due factor               = {:.8f}".format(proj.annuity_due_factor()))
print("yeongeum yeonaek B               = KRW {:,.0f} p.a. "
      "(KRW {:,.0f} a month)".format(proj.annuity_amount_pp(),
                                     proj.annuity_amount_pp() / 12))
print("implied factor F_net / B         = {:.4f}".format(
    proj.annuity_fund_net_pp() / proj.annuity_amount_pp()))
print("pyojun haeyak gongjeaek (cap)    = KRW {:,.2f}".format(proj.surr_chg_cap_pp()))
print("haeyak hwangeupgeum CV(12)/prem  = {:.2%}".format(
    proj.cv_pp(12) / proj.cum_prem_pp(12)))
print("seaek gongje (tax credit) p.a.   = KRW {:,.0f}  [not an insurer cash flow]".format(
    12 * proj.tax_credit_pp(0)))
print("gita sodeukse on surrender at 10y= KRW {:,.0f}  [not an insurer cash flow]".format(
    proj.surr_tax_pp(min(120, n))))
print()

df = proj.result_cf()
print("cash flow statement, KRW per policy issued per month, income positive")
print(df.head(4).round(2).to_string())
print("...")
print(df.loc[n - 2:n + 2].round(2).to_string())
print("...")
print(df.tail(2).round(2).to_string())
print()
print("undiscounted total premiums      = KRW {:,.2f}".format(df["premiums"].sum()))
print("undiscounted total annuity outgo = KRW {:,.2f}".format(df["claims_annuity"].sum()))
print("undiscounted total net_cf        = KRW {:,.2f}".format(df["net_cf"].sum()))
print()
for name in ("check_pols_roll_fwd", "check_av_roll_fwd", "check_cv_floor",
             "check_surr_chg_cap", "check_min_fund", "check_annuity_total",
             "check_annuity_limit", "check_mort_law", "check_net_cf"):
    print("{:<24} {}".format(name + "()", getattr(proj, name)()))

model.close()
