"""Run the key-rate DV01 and CS01 report of a MYGA_US_SEC book, live or compiled.

    python products/fixed_deferred_annuity/run_dv01_sec.py                  # live modelx
    python products/fixed_deferred_annuity/run_dv01_sec.py --compiled       # compiled, 1 and 4 workers
    python products/fixed_deferred_annuity/run_dv01_sec.py --compiled --workers 8 --build DIR
    python products/fixed_deferred_annuity/run_dv01_sec.py --input-dir DIR
    python products/fixed_deferred_annuity/run_dv01_sec.py --compiled --policies 1050

The report is ``dv01_sec/``'s ``Outer.annual_risk_report``: for each ESG path and each year,
the key-rate DV01 and CS01 of the book at the close before the year starts, one column per
tenor of ``dv01_sec/shock_steps.csv`` (``dv01-sec.md``).  By default it covers path 1 and
years 0, 1 and 2 (``--paths``, ``--years``).

By default the book is MYGA_US_SEC's shipped model point table, fourteen points.
``--input-dir DIR`` uses an existing directory containing ``model_point_table_sec.csv``,
the MYGA_US_SEC assumption CSVs, and ``dv01_sec/shock_steps.csv``. Alternatively,
``--policies N`` writes a temporary book of N policies by repeating the seven new-business
twins (points 1 to 7), as used for the timings in ``dv01-sec.md``.

Live modelx computes the report from the model's ``Outer`` Cells, releasing each close's
ItemSpaces as it goes.  ``--compiled`` builds the model with modelx-cython into ``--build
DIR`` (a temporary directory by default; an existing build there is reused) and runs the
report there twice, in a fresh process each time: with one worker thread, and with
``--workers`` threads (default 4), one task per policy.  Each run prints its totals and
seconds, and the runner checks that the two reports are equal.  On free-threaded CPython
(``python3.14t``) the workers run in parallel; on a build with the GIL they take turns.
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4]))   # the repository root, for a run from a checkout

from lifelib.libraries.uslib.products.fixed_deferred_annuity.dv01_sec import (  # noqa: E402
    build_model, compiled, report)

TWINS = 7


def parse(argv):
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--compiled', action='store_true', help='build and run the compiled model')
    parser.add_argument('--build', help='directory of the compiled build (made if absent)')
    parser.add_argument('--workers', type=int, default=4, help='threads of the parallel run')
    book = parser.add_mutually_exclusive_group()
    book.add_argument('--input-dir', '--input', dest='input', metavar='DIR',
                      help='directory containing the policy, assumption and shock CSVs')
    book.add_argument('--policies', type=int, help='a book of N copies of the seven twins')
    parser.add_argument('--paths', type=int, default=1, help='ESG paths 1..N')
    parser.add_argument('--years', type=int, default=2, help='years 0..N')
    parser.add_argument('--json', help='also write the reports and totals to this JSON file')
    parser.add_argument('--run', help=argparse.SUPPRESS)    # one compiled run, in a child
    return parser.parse_args(argv)


def write_book(folder, policies):
    """A book of ``policies`` copies of the seven twins, with the shipped assumptions."""
    compiled.copy_inputs(folder)
    table = pd.read_csv(HERE / 'model_point_table_sec.csv').iloc[:TWINS]
    assert (table['row_kind'] == 'twin').all() and (table['duration_mth'] == 0).all()
    book = pd.concat([table] * -(-policies // TWINS), ignore_index=True).iloc[:policies]
    book['point_id'] = range(1, len(book) + 1)
    book.to_csv(Path(folder) / 'model_point_table_sec.csv', index=False)
    return folder


def summary(dv01, cs01, seconds, **extra):
    return {**extra, 'policies': None, 'dv01_total': float(dv01.to_numpy().sum()),
            'cs01_total': float(cs01.to_numpy().sum()), 'seconds': round(seconds, 2)}


def show(title, result):
    print(f"{title}: DV01 total {result['dv01_total']:,.6f}  CS01 total "
          f"{result['cs01_total']:,.6f}  {result['seconds']:.2f} s", flush=True)


def child(args):
    """One compiled run, in this process: print its result as JSON on the last line."""
    sys.setrecursionlimit(20_000)
    model = compiled.load(args.run, args.input)
    start = time.perf_counter()
    dv01, cs01 = report.pooled_report(model, args.paths, args.years, args.workers)
    seconds = time.perf_counter() - start
    result = summary(dv01, cs01, seconds, workers=args.workers,
                     gil=getattr(sys, '_is_gil_enabled', lambda: True)())
    result['policies'] = len(model.Valuation.point_indices())
    result['dv01'] = dv01.to_numpy().tolist()
    result['cs01'] = cs01.to_numpy().tolist()
    print(json.dumps(result))


def compiled_runs(args, input_dir, folder):
    if not compiled.is_built(folder):
        print(f'building the compiled model in {folder}; this takes several minutes ...',
              flush=True)
        print(f'built in {compiled.build(folder):.0f} s', flush=True)
    results = []
    for workers in dict.fromkeys((1, args.workers)):
        command = [sys.executable, __file__, '--run', str(folder), '--workers', str(workers),
                   '--paths', str(args.paths), '--years', str(args.years)]
        if input_dir is not None:
            command += ['--input', str(input_dir)]
        done = subprocess.run(command, capture_output=True, text=True)
        if done.returncode:
            sys.exit(f'the compiled run with {workers} worker(s) failed:\n{done.stderr[-3000:]}')
        result = json.loads(done.stdout.strip().splitlines()[-1])
        show(f"compiled, {workers} worker{'s' if workers > 1 else ''}, "
             f"{result['policies']} policies", result)
        results.append(result)
    first = np.asarray(results[0]['dv01'] + results[0]['cs01'])
    for other in results[1:]:
        values = np.asarray(other['dv01'] + other['cs01'])
        if not np.allclose(values, first, rtol=1e-10, atol=1e-7):
            sys.exit('the reports differ between 1 worker and ' f"{other['workers']}")
    if len(results) > 1:
        print(f"speed-up at {results[-1]['workers']} workers: "
              f"{results[0]['seconds'] / results[-1]['seconds']:.2f}x; the reports are equal")
    return results


def main(argv):
    args = parse(argv)
    if args.run:
        return child(args)
    with tempfile.TemporaryDirectory() as scratch:
        input_dir = args.input
        if args.policies:
            input_dir = write_book(Path(scratch) / 'book', args.policies)
        if args.compiled:
            folder = Path(args.build).resolve() if args.build else Path(scratch) / 'build'
            results = compiled_runs(args, input_dir, folder)
            if args.json:
                Path(args.json).write_text(json.dumps(results) + '\n')
            return results
        sys.setrecursionlimit(20_000)
        model = build_model(input_dir=input_dir)
        try:
            start = time.perf_counter()
            dv01, cs01 = report.live_report(model, args.paths, args.years)
            seconds = time.perf_counter() - start
            result = summary(dv01, cs01, seconds)
            result['policies'] = len(model.Valuation.point_indices())
            pd.set_option('display.width', 200)
            print('DV01 by tenor (months), per 1 bp, liability decrease positive:')
            print(dv01.round(4).to_string())
            print('\nCS01 by tenor (months), base cash flows rediscounted:')
            print(cs01.round(4).to_string())
            show(f"\nlive modelx, {result['policies']} policies", result)
            if args.json:
                result['dv01'] = dv01.to_numpy().tolist()
                result['cs01'] = cs01.to_numpy().tolist()
                Path(args.json).write_text(json.dumps([result]) + '\n')
        finally:
            model.close()


if __name__ == '__main__':
    main(sys.argv[1:])
