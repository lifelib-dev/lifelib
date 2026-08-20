"""Run the WOL_UK_S reference model and print its cash flow statement.

    python products/whole_of_life/run.py            # the O50 anchor cell
    python products/whole_of_life/run.py 5          # the underwritten cell

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "WOL_UK_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {} cell, {}{} {}, cover {:,.0f}, premium {:,.2f}/month".format(
    point_id, proj.model_point()["policy_id"], proj.cell(), proj.sex(),
    proj.age_at_entry(), proj.smoker(), proj.sum_assured(), proj.premium_mth()))
cess = proj.cessation_mths()
print("basis = {} x {:.0%}   moratorium = {} months   premiums {}   escalation = {}".format(
    proj.mort_basis(), proj.mort_loading(), proj.moratorium_mths(),
    "cease at month {}".format(cess) if cess else "payable for life",
    proj.escalation()))
xover = proj.crossover_mth()
print("crossover = {}   paid-up variant = {}   accidental multiplier = {:.0f}x".format(
    "month {} ({} years {} months)".format(xover, xover // 12, xover % 12)
    if xover else "none", proj.pu_variant(), proj.adb_multiplier()))
print()
rows = [1, 6, 12, 13, 24, 60, 120]
print(proj.result_cf().loc[[t for t in rows if t <= proj.proj_len()]].round(2).to_string())

model.close()
