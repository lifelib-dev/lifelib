"""Run the FIA_US_SEC model and print a model point's account value, rider and cash flows.

    python products/fixed_indexed_annuity/run_sec.py          # point 1, in force 84 months
    python products/fixed_indexed_annuity/run_sec.py 14       # the anchor, depleted
    python products/fixed_indexed_annuity/run_sec.py --block  # the block, row by row
    python products/fixed_indexed_annuity/run_sec.py 1 --cython  # on the compiled model

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row. Point 1 is the worked example's anchor in force at
anniversary 7: its row ``t = 11`` is the worked example's policy month 95, the anniversary
closing contract year 8, where its first lifetime withdrawal is taken.

The contract is annual on a monthly grid, so the account value and rider traces are
printed at the anniversary months, those where ``duration_mth(t) % 12 == 11``, and the cash
flows are printed month by month for the first year and summed into contract years by
``result_cf_annual()``.

Points are named by their ``point_id``, and ``Projection`` is indexed by a point's position
in the table, as basiclife's BasicTerm_SC is, so the runner maps the one to the other.  It
takes the key from the model: the position where ``Projection`` takes ``idx``, as every
compiled model does, and the label where it takes ``point_id``, as an SEC model does before
its Phase 2.

``--cython`` runs the compiled model instead of modelx, and prints the same lines.  It is
``FIA_US_SEC_nomx_cy`` beside the model, which the repository's ``tools/build_sec_cy.py``
builds there the first time, and again whenever it is not built for this interpreter or
the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it: about three
and a half minutes, which it says on stderr.  The build is never committed, and ``.gitignore``
covers everything it leaves.  A ``lifelib.create()`` copy of the library carries no
``tools/``, wherever it is put, so there ``--cython`` stops, saying so, where it would
build.  ``--build DIR`` runs the package a build put in ``DIR`` instead, on the CSVs the
build copied there, and never builds.  Either way the runner stops, saying why, if the
package imports without its extension modules, which would compute the same numbers
uncompiled.

A block run asks every point for its frame before it projects any, because whether a point
is still in cover, and whether the contract issues it, are the product's rules, which
``proj_len()`` applies, and such a point would otherwise stop the run part-way.  It
releases each point's ItemSpace once it is read, so that it holds one point's cells at a
time: about 3.4 MB a point compiled.  Deleting the ItemSpace is not enough, because it
sits in reference cycles that only Python's cyclic collector frees, so the runner
collects after each release, in both passes.  It freezes everything alive
(``gc.freeze``) once the model and its table are read, and again once it has every
point's length, so that each collection scans only what the block has made since, and it
unfreezes them at the end.  The block's sum is kept as it goes, a frame at a time,
compensated as pandas' ``groupby`` sum is, so that it is the sum of the frames concatenated
and grouped by ``t``, bit for bit.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import importlib
import importlib.machinery
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NAME = "FIA_US_SEC"
SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
USAGE = ("usage: python run_sec.py [point_id | --block] [--cython] [--build DIR]")


def parse(argv):
    """``(point_id or None for the block, cython, build_dir)``, or exit with the usage."""
    point, block, cython, build = None, False, False, None
    args = iter(argv)
    for arg in args:
        if arg == "--block":
            block = True
        elif arg == "--cython":
            cython = True
        elif arg == "--build":
            build = next(args, None)
            if build is None:
                sys.exit(USAGE)
            cython = True
        elif arg.startswith("-") or point is not None or not arg.isdigit():
            sys.exit(USAGE)
        else:
            point = int(arg)
    if block and point is not None:
        sys.exit(USAGE)
    return (None if block else (1 if point is None else point)), cython, build


def _built(package):
    """The compiled space module of ``package`` built for this interpreter, if any."""
    found = [package / f"_mx_classes{suffix}" for suffix in SUFFIXES]
    return [path for path in found if path.is_file()]


def _tool():
    """``tools/build_sec_cy.py`` of the repository holding this product, or ``None``.

    The product sits at ``lifelib/libraries/<lib>/products/<product>`` in the repository,
    and a ``lifelib.create()`` copy of the library has no repository above it, and no
    tool, wherever it is put, as ``sec_support._tool`` finds it.
    """
    up = HERE.parents
    if len(up) < 5 or up[2].name != "libraries":
        return None
    return up[4] / "tools" / "build_sec_cy.py"


def compiled_model(build_dir):
    """The compiled model: from ``build_dir``, or built in place first where it is stale."""
    if build_dir is None:
        out, tool = HERE, _tool()
        package = out / f"{NAME}_nomx_cy"
        sources = [*(HERE / NAME).rglob("*.py"), HERE / "sample_sec.py",
                   HERE / "spec_sec.py", *([tool] if tool else [])]
        built = _built(package)
        newest = max((path.stat().st_mtime for path in sources if path.is_file()),
                     default=0.0)
        if not built or min(path.stat().st_mtime for path in built) < newest:
            if tool is None or not tool.is_file():
                sys.exit("--cython builds the model with the source repository's "
                         "tools/build_sec_cy.py, and a lifelib.create() copy carries no "
                         "tools/, so it cannot build")
            print(f"building {NAME} with {tool.name}, which takes about three and a "
                  f"half minutes ...", file=sys.stderr)
            done = subprocess.run([sys.executable, str(tool), str(HERE)],
                                  stdout=subprocess.DEVNULL)
            if done.returncode:
                sys.exit(f"the build failed; {tool.name} printed why")
    else:
        out = Path(build_dir).resolve()
        package = out / f"{NAME}_nomx_cy"
        if not _built(package):
            sys.exit(f"{package} holds no build of {NAME} for this interpreter")
    sys.path.insert(0, str(out))
    model = importlib.import_module(f"{NAME}_nomx_cy").mx_model
    space = type(model.Projection)
    if not sys.modules[space.__module__].__file__.endswith(SUFFIXES):
        sys.exit(f"{package} imported without its extension modules, so it would run "
                 f"uncompiled; rebuild it with tools/build_sec_cy.py")
    return model


point_id, cython, build_dir = parse(sys.argv[1:])
if cython:
    model = compiled_model(build_dir)
else:
    import modelx as mx
    model = mx.read_model(HERE / NAME)
table = model.Data.model_point_table()
# Projection's key for each point_id: its position, or the label itself (the docstring).
if cython or tuple(model.Projection.parameters) == ("idx",):
    key = {label: i for i, label in enumerate(table.index)}
else:
    key = {label: label for label in table.index}


def release(label):
    """Drop a point's ItemSpace once read, and collect it (the module docstring)."""
    del model.Projection[key[label]]
    gc.collect()


def add(total, compensation, frame):
    """Add ``frame``'s rows to the running sum's first rows, compensated (Kahan), as
    pandas' ``groupby`` sum adds each group's values in turn."""
    rows = len(frame)
    y = frame - compensation[:rows]
    t = total[:rows] + y
    compensation[:rows] = (t - total[:rows]) - y
    total[:rows] = t


def months(n):
    """``n`` with its unit: "1 month", "15 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


def phase_label(proj, t):
    """The label ``result_glwb()`` gives the phase of month ``t``."""
    return proj.result_glwb()["phase"].iloc[t]


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {}: contract year {}, attained age {}, {:.6f} in force, "
            "AV {:,.2f} per contract, phase {} in month 0".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), phase_label(proj, 0)))


def origin(label):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[label, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} on)".format(source, months(-m))
    if m:
        return " (S's {}, in force at its month {})".format(source, m)
    return " (S's {})".format(source)


def events(proj, anniversaries):
    """The first lifetime withdrawal and the account value running out.

    Each in the frame, or before the valuation date on a point in force that opens
    month 0 in income, or with no account value left, as the depleted anchor does.
    """
    exercise = [t for t in anniversaries if proj.is_exercise(t)]
    glwb = proj.result_glwb()["phase"]
    out = [t for t in anniversaries if glwb.iloc[t] in ("DEPLETED", "TERMINATED")]
    in_force = proj.duration_mth_init() > 0
    if exercise:
        first = "in contract year {}, at t = {}".format(proj.policy_year(exercise[0]),
                                                       exercise[0])
    elif in_force and glwb.iloc[0] in ("INCOME", "DEPLETED"):
        first = "before the valuation date"
    else:
        first = "not in the frame"
    if in_force and proj.av_pp_init() == 0.0:
        empty = "before the valuation date"
    elif out:
        empty = "in contract year {}, at t = {} ({})".format(
            proj.policy_year(out[0]), out[0], glwb.iloc[out[0]])
    else:
        empty = "not in the frame"
    return "first lifetime withdrawal {}; account value runs out {}".format(first, empty)


if point_id is None:
    # Every point's frame first.  The table checks itself as it is read, but whether a
    # point is still in cover, and whether the contract issues it, are the product's
    # rules, which proj_len() applies, so such a point would otherwise stop the run
    # part-way, after the points before it.  The model and its table are frozen first,
    # so that the collection after each release scans only what the release left.
    rows = {}
    gc.freeze()
    for label in table.index:
        rows[label] = model.Projection[key[label]].proj_len()
        release(label)
    gc.freeze()
    total, columns = np.zeros((max(rows.values(), default=0), 0)), None
    print("model points, t = 0 the valuation date for each:")
    for label in table.index:
        proj = model.Projection[key[label]]
        df = proj.result_cf()
        if columns is None:
            columns = list(df.columns)
            total = np.zeros((len(total), len(columns)))
            compensation = np.zeros_like(total)
        add(total, compensation, df[columns].to_numpy())
        print("  {:>2}  {:<16} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), rows[label]))
        del proj, df
        release(label)                          # each point is read once, then released
    block = pd.DataFrame(total, columns=columns,
                         index=pd.RangeIndex(len(total), name="t"))
    print()
    print("the block, first 12 rows, t = 0..11 (months from the valuation date):")
    print(block.head(12).round(2).to_string())
    print()
    print("the block summed into projection years 1-12, year = t // 12 + 1:")
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    print(annual.head(12).round(2).to_string())
else:
    label = point_id
    if label not in key:
        sys.exit("no model point {} in the table: {}".format(label, list(key)))
    proj = model.Projection[key[label]]
    print("model point {}: {}{} - {}{} {} premium {:,.0f}, bonus {:.0%}, {} indexed".format(
        label, table.at[label, "policy_id"], origin(label), proj.sex(),
        proj.age_at_entry(), proj.tax_status(), proj.premium_pp(), proj.bonus_rate(),
        "{:.0%}".format(proj.alloc_indexed())))
    print("GLWB {}  basis {}  income from age {}  utilization {:.0%}  "
          "cap {:.2%}  rollup {}  stack {:.2f}x".format(
              "elected" if proj.glwb_elected() else "not elected", proj.glwb_basis(),
              proj.income_start_age(), proj.utilization_intensity(),
              proj.cap_rate_in_force(), proj.rollup_id(), proj.stack_factor()))
    print("at the valuation date: {}".format(describe(proj)))
    n = proj.proj_len()
    print("proj_len = {} from the valuation date (t = 0..{}); cover ends at policy month "
          "{}, the anniversary at attained age {}".format(
              months(n), n - 1, proj.maturity_mth(),
              proj.age_at_entry() + proj.policy_term()))
    anniversaries = [t for t in range(proj.t_entry(), n) if proj.is_anniv(t)]
    print(events(proj, anniversaries))
    print("every contractual event falls in an anniversary month, where "
          "duration_mth(t) % 12 == 11; the rows below are those months")
    print()
    print("account value, benefit base and lifetime withdrawal (per contract), at the")
    print("anniversaries closing the first fourteen contract years on the books:")
    cols = ["av_pp_bef_inv", "index_credit_pp", "rider_charge_pp", "wd_pp", "av_pp",
            "mgsv_pp"]
    av = proj.result_av().loc[anniversaries[:14], cols]
    bb = proj.result_glwb().loc[anniversaries[:14], ["benefit_base_pp", "lw_pp", "phase"]]
    print(av.join(bb).round(2).to_string())
    print()
    print("cash flows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("cash flows, summed into contract years (months in cover only):")
    print(proj.result_cf_annual().head(14).round(2).to_string())


if not cython:
    model.close()
gc.unfreeze()
