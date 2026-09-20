"""Run the Immediate_KR_S reference model and print its cash flow statement.

    python products/immediate_annuity/run.py            # the worked-example anchor
    python products/immediate_annuity/run.py 6          # sangsok, retention as designed
    python products/immediate_annuity/run.py 7          # the same contract, as ordered
    python products/immediate_annuity/run.py 9          # hwakjeong-gigan, 10 years

Output is ASCII-only so it prints on a Windows console under any code page.  The
documents may use Hangul freely; this may not, so Korean terms are romanized here
(Revised Romanization) and amounts are written KRW.
"""
import sys
from pathlib import Path

import modelx as mx

SHAPE_NAME = {
    "life": "jongsin yeongeum-hyeong (life annuity)",
    "inheritance": "sangsok yeongeum-hyeong mangi-hyeong (inheritance, term)",
    "certain": "hwakjeong-gigan yeongeum-hyeong (annuity certain)",
}
TERM_NAME = {
    "life": "bojeung jigeup gigan (guaranteed period)",
    "inheritance": "boheom gigan (benefit term)",
    "certain": "yeongeum jigeup gigan (payment term)",
}

model = mx.read_model(Path(__file__).parent / "Immediate_KR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
proj = model.Projection[point_id]

print("Immediate_KR_S - jeuksi yeongeum (Korean single-premium immediate annuity)")
print("model point {}: {} - {}".format(
    point_id, proj.model_point()["policy_id"], SHAPE_NAME[proj.shape()]))
print("annuitant {} boheom nai {} (insurance age)   single premium KRW {:,.0f}"
      " ({:,.0f} manwon)".format(
          proj.sex(), proj.age_at_entry(), proj.prem_pp(), proj.prem_pp() / 10000))
print("{} = {} years ({} months)   lapse {:.2%} p.a.".format(
    TERM_NAME[proj.shape()], proj.annuity_term(), proj.annuity_term_mths(),
    proj.lapse_rate(0)))
print("crediting basis {}: gongsi iyul {:.2%}, choejeo bojeung iyul {:.2%} to {:.2%}"
      " -> credited {:.2%} p.a. at t = 0 and {:.2%} p.a. at t = {}".format(
          proj.crediting_basis(), proj.decl_rate(), proj.min_guar_rate(0),
          proj.min_guar_rate(proj.proj_len() - 1), proj.crediting_rate(0),
          proj.crediting_rate(proj.proj_len() - 1), proj.proj_len() - 1))
print("   monthly equivalent {:.6%} at t = 0 (twelve compound back to the annual rate)"
      .format(proj.crediting_rate_mth(0)))
print("expense load {:.2%} + wiheom boheomnyo {:.2%} -> opening gyeyakja jeongnimaek"
      " KRW {:,.0f} ({:.2%} of premium)".format(
          proj.expense_load_rate(), proj.risk_prem_rate(), proj.av_pp_init(),
          proj.av_pp_init() / proj.prem_pp()))
if proj.shape() == "life":
    print("monthly annuity factor {:.4f} -> yeongeum wolaek KRW {:,.0f} a month"
          " (KRW {:,.0f} a year)".format(
              proj.annuity_factor(), proj.annuity_pp(0), proj.annuity_pp_annual(0)))
else:
    print("retention basis {} -> first yeongeum wolaek KRW {:,.0f} a month"
          " (KRW {:,.0f} a year), mangi boheomgeum KRW {:,.0f}".format(
              proj.retention_basis(), proj.annuity_pp(0), proj.annuity_pp_annual(0),
              proj.maturity_benefit()))
    if proj.retention_shortfall_pp() > 0.0:
        print("cost of the 2017 jojeong gyeoljeong liability at inception:"
              " KRW {:,.0f}".format(proj.retention_shortfall_pp()))
print("projection runs t = 0 .. {} ({} months = {} policy years; monthly, in arrears;"
      " row t pays at t + 1)".format(
          proj.proj_len() - 1, proj.proj_len(), proj.proj_years()))
print()

cf = proj.result_cf()
rows = [t for t in (0, 1, 2, 11, 12, 59, 60, 119, 120, 239, 240, 359, 360, 479, 480,
                    611, 612) if t < proj.proj_len()]
print("Cash flow statement (KRW, income positive in net_cf)")
print(cf.loc[rows].round(2).to_string())
print()
print("undiscounted totals over t = 0 .. {}:".format(proj.proj_len() - 1))
for col in ("premiums", "annuity_payments", "claims_death", "claims_lapse",
            "claims_maturity", "commissions", "expenses", "net_cf"):
    print("    {:<20s} {:>20,.2f}".format(col, cf[col].sum()))
print()

print("checks")
names = sorted(c for c in model.Projection.cells
               if c.startswith("check_") and not c.endswith("_resid"))
for name in names:
    print("    {:<26s} {}".format(name, getattr(proj, name)()))

model.close()
