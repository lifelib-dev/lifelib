"""Run the Obseques_FR_S reference model and print its cash flow statement.

    python products/obseques/run.py            # the RefOBS-VIA anchor cell
    python products/obseques/run.py 3          # the prime unique cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Obseques_FR_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {} cell, {}{}, capital {:,.0f} EUR, {} premium {:,.2f}/year".format(
    point_id, proj.model_point()["policy_id"], proj.cell(), proj.sex(),
    proj.age_at_entry(), proj.capital_0(), proj.premium_form(), proj.annual_premium()))
cease = proj.prem_cease_age()
print("carence = {} months   accidental multiplier = {:.0f}x   "
      "premiums {}   instalments {}/year".format(
          proj.carence_months(), proj.accident_mult(),
          "cease at attained age {}".format(cease) if cease else "payable to the end",
          proj.prem_freq()))
print("revalorisation = {:.2%} p.a. {}   premiums linked = {}   reduction share = {:.0%}".format(
    proj.reval_rate(), "simple" if proj.reval_simple() else "compound",
    proj.reval_prem_linked(), proj.reduction_share()))
xi, xc = proj.crossover_mth("ISSUE"), proj.crossover_mth("CURRENT")


def crossover_label(x):
    """Label a crossover month, or "none" for the -1 never-crosses sentinel.

    ``t`` is the 0-based policy month, so the policy year is ``t // 12 + 1``.
    """
    if x < 0:
        return "none"
    return "t = {} (policy year {})".format(x, x // 12 + 1)


print("surrender scale = {}   crossover: vs capital at issue {}, vs revalorised {}".format(
    proj.surr_scale(), crossover_label(xi), crossover_label(xc)))
print()
# Policy months are 0-based: t = 0 is the first month, t = 12 the first anniversary.
rows = [0, 5, 11, 12, 23, 59, 119, 239]
print(proj.result_cf().loc[[t for t in rows if t < proj.proj_len()]].round(2).to_string())

model.close()
