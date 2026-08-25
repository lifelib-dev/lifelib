"""Run the IncomeTerm_JP_S reference model and print its cash flow statement.

    python products/income_guarantee/run.py            # anchor cell (point_id = 1)
    python products/income_guarantee/run.py 6          # another model point

The product is shuunyuu-hoshou-hoken (survivor income term): a **death** benefit paid
as a level monthly income to the end of the term, floored by a minimum payment
guarantee period. It is not income protection.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "IncomeTerm_JP_S")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
modules = [name for name, on in (
    ("commutation", proj.commutation()), ("living-needs", proj.living_needs()),
    ("waiver", proj.wop()), ("reinstatement", proj.reinstatement())) if on]

print("model point {}: {} - {}{} {}, to age {} ({} months), "
      "guarantee {} months".format(
          point_id, proj.model_point()["policy_id"], proj.sex(),
          proj.issue_age(), proj.rate_class(), proj.expiry_age(),
          proj.term_m(), proj.guar_m()))
print("income = JPY {:,.0f}/month   premium = JPY {:,.0f}/month ({})   "
      "class factor = {:.2f}".format(
          proj.annuity_mth(), proj.premium_mth_pp(), proj.premium_mode(),
          proj.class_factor()))
print("projection horizon = {} months, {} months past the end of cover   "
      "modules on: {}".format(
          proj.proj_len(), proj.proj_len() - proj.term_m(),
          ", ".join(modules) if modules else "none (base run)"))
print()

df = proj.result_cf()
print("first 12 policy months")
print(df.head(12).round(2).to_string())
print()
print("the last month of cover and the run-off tail after it")
print(df.loc[proj.term_m():].head(6).round(2).to_string())
print()
print("totals over the {} projected months, undiscounted, per policy issued"
      .format(proj.proj_len()))
for col in df.columns:
    if col in ("pols_if", "annuities_if"):
        continue
    print("  {:<22} {:>16,.2f}".format(col, df[col].sum()))
print("  {:<22} {:>16,.2f}".format(
    "claim outgo after cover", df.loc[proj.term_m() + 1:, "claims_annuity"].sum()))
print()
print("identity checks: " + "  ".join(
    "{}={}".format(name, getattr(proj, name)()) for name in sorted(
        c for c in model.Projection.cells
        if c.startswith("check_") and not c.endswith("_resid"))))

model.close()
