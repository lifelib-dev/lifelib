"""Run the Euro_FR_S reference model and print its crediting and cash flow statements.

    python products/assurance_vie_euro/run.py            # the worked example's anchor cell
    python products/assurance_vie_euro/run.py 7          # the same cell, low scenario
    python products/assurance_vie_euro/run.py 8          # the high scenario, PPB building

Output is ASCII-only so it prints on a Windows console under any code page; the French
terms are spelled without their accents here and nowhere else.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Euro_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}, adhesion age {}, attained {}, in force {} years, "
      "pols_if_init {:g}".format(
          point_id, proj.policy_id(), proj.sex(), proj.issue_age(), proj.age(0),
          proj.duration_init(), proj.pols_if_init()))
print("scenario {}: r_fin {:.2%} in year y = 0 to {:.2%} in y = 11; "
      "reference rate {:.2%}".format(
          proj.scenario_id(), proj.r_fin(0), proj.r_fin(11), proj.ref_rate(0)))
print("target taux servi {:.2%}   TMG {:.2%}   frais de gestion {:.3%}   "
      "frais sur versement {:.2%}   prelevements sociaux {:.1%}".format(
          proj.ts_target(), proj.tmg_rate(), proj.fee_rate(),
          proj.prem_charge_rate(), proj.soc_levy_rate()))
print("carried in: epargne acquise {:,.2f}   PPB {:,.2f} in {} vintages falling due "
      "in years y = {} to {}".format(
          proj.av_pp(0), proj.ppb_pp(0), proj.ppb_vintages_init(),
          proj.ppb_vintage_first() + 8, 7))
print("versements {:,.2f} p.a.   rachats partiels {:,.2f} p.a. from year y = {}   "
      "guarantee form {}".format(
          proj.prem_gross_pp(0), proj.wd_prog_pp(), proj.wd_start_year(),
          proj.guarantee_form()))
print("t counts POLICY MONTHS, 0-based: the projection runs t = 0 to {} ({} years, "
      "y = t // 12), and 31 December is t % 12 == 11 (no maturity: the euro support has "
      "no term)".format(proj.proj_len() - 1, proj.proj_len() // 12))
print()
print("Crediting machinery, by projection year y (per policy; the ppb_pp column is the "
      "PPB at the END of year y, i.e. ppb_pp(y + 1), while av_pp and guar_floor_pp are "
      "start of year):")
pb = proj.result_pb()
rates = ("r_fin", "ts_stat", "ts_net")
# Adding 0.0 turns IEEE negative zero back into zero: an exhausted PPB carries a few
# hundredths of a femto-euro of float residue and would otherwise print as -0.00.
print((pb.head(12).round(
    {c: (6 if c in rates else 2) for c in pb.columns}) + 0.0).to_string())
print()
# Policy months are 0-based: t = 0 is the first month, t = 11 the first 31 December.
# The whole of the year's revalorisation and levy lands in that last month.
print("Cash flows, the twelve months of projection year 0 (t = 0 .. 11):")
print((proj.result_cf().head(12).round(2) + 0.0).to_string())
print()
print("The same frame summed into projection years (years y = 0 .. 11):")
print((proj.result_cf_annual().head(12).round(2) + 0.0).to_string())
print()
print("Checks: account roll-forward {}  PPB roll-forward {}  PPB eight-year clock {}"
      .format(proj.check_av_roll_fwd(), proj.check_ppb_roll_fwd(),
              proj.check_ppb_clock()))
print("        policies {}  PB allocation {}  effet cliquet {}  guarantee floor {}"
      .format(proj.check_pols_roll_fwd(), proj.check_pb_allocation(),
              proj.check_cliquet(), proj.check_guar_floor()))
print("        twelve monthly decrements compound to the annual ones {}"
      .format(proj.check_decrements_compound()))

model.close()
