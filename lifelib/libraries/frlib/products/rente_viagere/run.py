"""Run the Rente_FR_S reference model and print its cash flow statement.

    python products/rente_viagere/run.py            # the worked-example scenario
    python products/rente_viagere/run.py 2          # the same contract, expected basis

Output is ASCII-only so it prints on a Windows console under any code page.  The
documents may use accented French freely; this may not.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Rente_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
lives = "{}{}".format(proj.sex(1), proj.age_at_entry(1))
if proj.reversion_pct() > 0:
    lives += " with reversion to {}{} at {:.0%}".format(
        proj.sex(2), proj.age_at_entry(2), proj.reversion_pct())
print("model point {}: {} - capital {:,.0f}, {}".format(
    point_id, proj.model_point()["policy_id"], proj.purchase_price(), lives))
print("effective 1/{}/{}   millesimes {}/{}   taux de rente {:.4%}   "
      "taux technique {:.2%}".format(
          proj.effective_month(), proj.effective_year(), proj.birth_year(1),
          proj.birth_year(2) if proj.reversion_pct() > 0 else "-",
          proj.annuity_rate(), proj.technical_rate()))
print("annuity {:,.2f} p.a. after coeff {:.4f}   {} payments in {}   "
      "paliers = {}".format(
          proj.annual_income_init(), proj.option_coeff(), proj.payment_freq(),
          proj.payment_timing(), proj.palier_scheme()))
print("annuites garanties = {} months   frais d'arrerages = {:.2%}   "
      "revalorisation = {:.2%}   basis = {}".format(
          proj.guarantee_mths(), proj.arrerage_charge_rate(),
          proj.revalo_rate, proj.mort_basis()))
print()
print("cash flow at the worked-example months, t 0-based (t = 0 .. {})".format(
    proj.proj_len() - 1))
rows = [t for t in (0, 8, 9, 11, 20, 21, 24, 25, 26, 29, 32, 33, 35)
        if t < proj.proj_len()]
print(proj.result_cf().loc[rows].round(2).to_string())

model.close()
