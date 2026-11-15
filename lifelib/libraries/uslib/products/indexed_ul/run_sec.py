"""Run the IUL_US_SEC model and print a model point's cash flows, or the block's.

    python products/indexed_ul/run_sec.py          # point 1: S point 1, issued now
    python products/indexed_ul/run_sec.py 7        # S point 4 in force 65 months
    python products/indexed_ul/run_sec.py --block  # every model point, row by row
    python products/indexed_ul/run_sec.py 7 --cython  # point 7 on the compiled model

Point 7 is in force 65 months at the valuation date with all twelve index segments live,
carried in from the segment ladder, so its rows show the segments it brings in maturing
one a month and their credits reaching the account value.  ``t`` counts months from the
valuation date, which is the same instant for every model point, so row ``t`` of one
point's frame is the same month as row ``t`` of any other's, and a block is the frames
summed row by row.  Points are named by their ``point_id``, and ``Projection`` is indexed
by a point's position in the table, as basiclife's BasicTerm_SC is, so the runner maps the
one to the other.  It takes the key from the model: the position where ``Projection``
takes ``idx``, as every compiled model does, and the label where it takes ``point_id``,
as an SEC model does before its Phase 2.  A label that is not one of the table's is
refused, naming them, whether it is a number or not.

``--cython`` runs the compiled model instead of modelx, and prints the same lines.  It is
``IUL_US_SEC_nomx_cy`` beside the model, which the repository's ``tools/build_sec_cy.py``
builds there the first time, and again whenever it is not built for this interpreter or
the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it: about three
minutes, which it says on stderr.  The build is never committed, and ``.gitignore`` covers
everything it leaves.  A ``lifelib.create()`` copy of the library carries no ``tools/``,
wherever it is put, so there ``--cython`` stops, saying so, where it would build.
``--build DIR`` runs the package a build put in ``DIR`` instead, on the CSVs the build
copied there, and never builds.  Either way the runner stops, saying why, if the package
imports without its extension modules, which would compute the same numbers uncompiled.

A block run releases each point's ItemSpace once it is read, so that it holds one point's
cells at a time: about 5.0 MB a point compiled.  Deleting the ItemSpace is not enough,
because it sits in reference cycles that only Python's cyclic collector frees, so the
runner collects after each release, in both passes.  It freezes everything alive
(``gc.freeze``) once the model and its table are read, and again once it has every
point's length, so that each collection scans only what the block has made since.  The
block's sum is kept as it goes, a frame at a time, compensated as pandas' ``groupby`` sum
is, so that it is the sum of the frames concatenated and grouped by ``t``, bit for bit,
wherever every frame is finite.

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
NAME = "IUL_US_SEC"
SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
USAGE = ("usage: python run_sec.py [point_id | --block] [--cython] [--build DIR]")


def parse(argv):
    """``(point_id or None for the block, cython, build_dir)``, or exit with the usage.

    Any argument but an option is the point's label: ``int`` of it where it reads as a
    whole number, and the text otherwise, which no label of the table matches, so that
    the run refuses it naming the table's labels.
    """
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
        elif arg.startswith("--") or point is not None:
            sys.exit(USAGE)
        else:
            try:
                point = int(arg)
            except ValueError:  # not a number, so no point_id: refused below, by name
                point = arg
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
            print(f"building {NAME} with {tool.name}, which takes about three minutes "
                  f"...", file=sys.stderr)
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


def months(n):
    """``n`` with its unit: "1 month", "25 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


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


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    live = min(proj.seg_term_mth, d)
    held = 0.0
    for k in range(1, live + 1):
        held = held + proj.seg_bal_pp_init(k)
    return ("in force {}: policy year {}, attained age {}, {:.6f} in force, "
            "account value {:,.2f}: fixed account {:,.2f}, segments of the last {} "
            "{:,.2f}, collateral {:,.2f}; loan {:,.2f}, face in force {:,.2f}, "
            "premiums paid {:,.2f}, no-lapse accumulator {:,.2f}, {}".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), proj.fa_pp_init(), months(live), held,
                proj.lca_pp_init(),
                proj.loan_bal_init(), proj.sum_assured_init(), proj.cum_prem_init(),
                proj.cum_prem_net_init(),
                "a MEC" if proj.is_mec_init() else "not a MEC"))


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
    return " (S's {})".format(source)


if point_id is None:
    # Every point's frame first.  The table checks itself as it is read, but whether a
    # point is still inside the projection, issued by the contract, withdrawing less than
    # its fee, or holding one ladder row for each live segment is the product's rule,
    # which proj_len() applies, so a point past it would otherwise stop the run part-way,
    # after the points before it.  The model and its table are frozen first, so that the
    # collection after each release scans only what the release left.
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
    if point_id not in key:
        sys.exit(f"no model point {point_id} in the table: {list(key)}")
    proj = model.Projection[key[point_id]]
    print("model point {}: {}{} - {}{} {} face {:,.0f} option {} {}, premium "
          "{:,.2f}/yr {}, indexed allocation {:.0%}".format(
              point_id, table.at[point_id, "policy_id"], origin(point_id), proj.sex(),
              proj.age_at_entry(), proj.rate_class(), proj.sum_assured(),
              proj.db_option(), proj.premium_type(), proj.premium_pp_ann(),
              proj.premium_mode(), proj.index_alloc_rate()))
    print("at the valuation date: {}".format(describe(proj)))
    print("proj_len = {} months from the valuation date (t = 0..{}); the projection ends "
          "at policy month {}, attained age {}".format(
              proj.proj_len(), proj.proj_len() - 1, proj.maturity_mth(),
              proj.maturity_age))
    print()
    print("first 12 rows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("account value per policy, t = 0..11:")
    print(proj.result_av().head(12).round(2).to_string())
    print()
    print("segment ladder per policy, t = 0..11:")
    print(proj.result_seg().head(12).round(4).to_string())
    print()
    print("policy counts and decrement rates, t = 0..11:")
    print(proj.result_pols().head(12).round(6).to_string())

if not cython:
    model.close()
