"""Run the Pflege_DE_S reference model and print its cash flow statement.

    python products/pflegerentenversicherung/run.py            # anchor cell (point_id = 1)
    python products/pflegerentenversicherung/run.py 5          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Pflege_DE_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {} entry {}, {} - Pflegerente {:,.2f} EUR/month at PG5, "
      "Staffel {}".format(
          point_id, proj.policy_id(), proj.sex(), proj.age_at_entry(),
          proj.status_init(), proj.rente_mth(), proj.staffel_id()))
print("Leistungsstaffel  PG1 {:.0%}  PG2 {:.0%}  PG3 {:.0%}  PG4 {:.0%}  PG5 {:.0%}".format(
    *[proj.benefit_pct(g) for g in range(1, 6)]))
print("premium: mode = {} (m = {}), to age {}, model point value {:,.2f}, "
      "Risikozuschlag {:.2f}".format(
          proj.prem_mode(), proj.prem_mode_months(), proj.prem_end_age(),
          proj.premium_mth(), proj.rating_factor()))
print("options: Wartezeit {} m, Karenzzeit {} m, Leistungsdynamik {:.2%}, "
      "Beitragsrueckgewaehr {}, Stornoabzug {:.2%}".format(
          proj.wartezeit_months(), proj.karenz_months(), proj.leistungsdynamik(),
          proj.beitragsrueckgewaehr(), proj.stornoabzug_rate()))
print("Beitrag {:,.6f} EUR/month   net level premium {:,.6f} EUR/month   "
      "Beitragssumme {:,.2f} EUR   acquisition charge {:,.2f} EUR".format(
          proj.premium_mth_pp(), proj.prem_net_level_pp(), proj.beitragssumme(),
          proj.acq_expense_pp()))
print("EPV benefits {:,.6f}   EPV premium units {:,.6f}   EPV admin {:,.6f}   "
      "EPV claim expense {:,.6f}".format(
          proj.epv_benefits(), proj.epv_prem_units(), proj.epv_admin(),
          proj.epv_claim_expense()))
print("frame: t = {} to {} (proj_len = {}, {} monthly rows), attained ages {} to {}".format(
    proj.duration_mth_init(), proj.proj_len() - 1, proj.proj_len(),
    proj.proj_len() - proj.duration_mth_init(),
    proj.age(proj.duration_mth_init()), proj.age(proj.proj_len() - 1)))
print()

df = proj.result_cf()
print(df.head(13).round(6).to_string())
print()
print("totals over {} months: premiums {:,.2f}  claims_annuity {:,.2f}  "
      "claims_lapse {:,.2f}  claims_death {:,.2f}".format(
          len(df), df["premiums"].sum(), df["claims_annuity"].sum(),
          df["claims_lapse"].sum(), df["claims_death"].sum()))
print("                       expenses {:,.2f}  claim_expenses {:,.2f}  "
      "net_cf {:,.2f}".format(
          df["expenses"].sum(), df["claim_expenses"].sum(), df["net_cf"].sum()))
print("decrements: deaths {:.6f}  surrenders {:.6f}  still in force at t = {}: "
      "{:.6f}".format(
          proj.pols_dead_cum(proj.proj_len()),
          proj.pols_lapse_cum(proj.proj_len()),
          proj.proj_len(), proj.pols_if(proj.proj_len())))
print("checks: net_cf {}  pols roll fwd {}  states {}  waiver {}  esc ledger {}  "
      "prem equiv {}".format(
          proj.check_net_cf(), proj.check_pols_roll_fwd(), proj.check_states(),
          proj.check_waiver(), proj.check_esc_ledger(), proj.check_prem_equiv()))

model.close()
