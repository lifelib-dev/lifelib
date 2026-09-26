"""Run the RV_DE_S reference model and print its cash flow statement.

    python products/klassische_rentenversicherung/run.py       # anchor cell (point_id = 1)
    python products/klassische_rentenversicherung/run.py 6     # another model point

The frame counts policy **months**.  Three views are printed - the first twelve months of
``result_cf()``, the whole run summed into policy years by ``result_cf_annual()``, and the
annual state of ``result_pols()``, which is where the two accounts and their credits live.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "RV_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
mp = proj.model_point()
n = int(mp["aufschub_y"])

print("model point {}: {} - {}{} issued {}, duration {}, {} EUR {} to age {}".format(
    point_id, mp["policy_id"], mp["sex"], mp["issue_age"], mp["issue_year"],
    mp["duration_init"], mp["premium_form"], mp["prem_freq"],
    int(mp["issue_age"]) + n))
print("premium {:,.2f} EUR p.a. x {} y (freq load {:.3f})   Beitragssumme {:,.2f}   "
      "alpha {:,.2f}".format(
          proj.prem_pp(proj.k_start()), mp["prem_term_y"],
          proj.freq_load(), proj.beitragssumme_pp(), proj.alpha_total_pp()))
print("Rechnungszins {:.2%}   declared {:.2%}   bonus {:.2%}   charge set {}".format(
    proj.int_rate_guar(), proj.decl_rate(proj.k_start()),
    proj.bonus_rate(proj.k_start()), mp["charge_id"]))
print("Rentenbeginn: last accumulation month t = {} (age {}):  capital {:,.2f}  "
      "Rentenfaktor max({:.2f}, {:.2f}) = {:.2f}  ->  garantierte Rente {:,.2f} "
      "EUR/month".format(
          12 * n - 1, int(mp["issue_age"]) + n, proj.capital_conv_pp(),
          proj.annuity_rate_guar(), proj.annuity_rate_curr(),
          proj.annuity_rate_appl(), proj.annuity_guar_mth_pp()))
print("Rentengarantiezeit {} y = {} instalments   Kapitalwahl {:.0%}   payout system {}"
      .format(mp["rgz_years"], 12 * int(mp["rgz_years"]),
              float(mp["kapitalwahl_rate"]), mp["payout_system"]))
print("frame t = {} .. {} months ({} policy years; policy_year = t // 12 + 1)   "
      "implied Rentenfaktor on the shipped proxy {:.2f}".format(
          proj.t_start(), proj.proj_len() - 1, proj.proj_len_y(),
          10000.0 / proj.annuity_due_factor()))
print()

df = proj.result_cf()
print("first 12 months")
print(df.head(12).round(2).to_string())
print()
print("summed into policy years")
print(proj.result_cf_annual().head(12).round(2).to_string())
print()
print("annual state")
print(proj.result_pols().head(12).round(2).to_string())
print()
print("totals over t = {} .. {}: premiums {:,.2f}  claims {:,.2f}  annuity {:,.2f}  "
      "expenses {:,.2f}  net_cf {:,.2f}".format(
          df.index[0], df.index[-1],
          df["premiums"].sum(),
          df["claims_death"].sum() + df["claims_lapse"].sum()
          + df["claims_commutation"].sum(),
          df["annuity_payments"].sum(), df["expenses"].sum(),
          df["net_cf"].sum()))
print("checks: net_cf {}  pols {}  closure {}  av {}  av_sur {}  prem split {}  "
      "cv floor {}  conversion {}  annuity guarantee {}".format(
          proj.check_net_cf(), proj.check_pols_roll_fwd(),
          proj.check_decrement_closure(), proj.check_av_roll_fwd(),
          proj.check_av_sur_roll_fwd(), proj.check_prem_split(),
          proj.check_cv_floor(), proj.check_annuity_conv(),
          proj.check_annuity_guarantee()))

model.close()
