"""Compile the DV01 model with modelx-cython, and load the compiled model.

:func:`build` exports the model built by :func:`model.build_model` on the shipped book into a
directory, with ``ESG`` and ``Market`` locked (no Cell of theirs is cleared while a report
runs), copies the input CSVs beside the export, writes the compilation spec
(:func:`spec`) and the sample run (``sample.py``), and runs the compiler there.  The compiled
package is ``model_cy`` in that directory.  :func:`load` imports it and points it at a book.

The build takes several minutes and is never written into the library tree.
"""
import hashlib
import importlib
import importlib.machinery
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

from .model import SHOCK_STEPS_FILE, TABLES, build_model

HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
PACKAGE = 'model'
STAMP = 'build.stamp'

# The compiler is run with a raised recursion limit and a large thread stack: tracing the
# sample calls a policy's cold cash flow at the end of its frame, hundreds of months deep.
_ENTRY = """
import sys, threading
sys.setrecursionlimit(20_000)
threading.stack_size(268_435_455)
from modelx_cython.cli import entry_point_main
sys.argv[0] = 'modelx_cython'
entry_point_main()
"""


def spec(model):
    """The compiler's cache sizes, by Space and parameter.

    ``Actual`` and ``Valuation`` take MYGA_US_SEC's own sizes (``spec_sec.py``), ``Valuation``
    also the curve offset ``k`` and the close ``month``.  ``Market`` sizes the two arguments
    of ``rate(tenor_month, forward_month)`` separately: the tenor runs to the longest
    guarantee period in months, and at least 60, the renewal and MVA fixing tenor.  ``ESG``
    and the curve prices run to 1,800 months.  ``Outer``'s ``key`` is left unbounded, so that
    a longer ``shock_steps.csv`` needs no rebuild.
    """
    import ast
    sec = ast.literal_eval((PRODUCT / 'spec_sec.py').read_text())
    sizes = sec['spaces']['Projection']['cells_param_size']
    years = int(model.Data.model_point_table()['guar_period'].max())
    tenor_count = max(60, 12 * years) + 1
    policy_months = max(1202, model.Data.book_projection_end() + 2)
    curve_months = 1801
    close_months = int(model.ESG.step_size()) + 1
    scenarios = (1, int(model.ESG.scen_size()) + 1)
    return {'spaces': {
        'ESG': {'cells_param_size': {**dict.fromkeys(('i', 'j', 'm', 'k'), curve_months),
                                     'scen_id': scenarios}},
        'Market': {
            'cells_param_size': {
                'maturity_month': curve_months, 'tenor_month': curve_months,
                ('tenor_month', 'forward_month'): (tenor_count, policy_months)},
            'cells': {'rate': {'max_dense_entries': tenor_count * policy_months}}},
        'Actual': {'cells_param_size': dict(sizes)},
        'Valuation': {'cells_param_size': {**sizes, 'k': (-1, sizes['t']),
                                           'month': (-1, close_months)}},
        'Outer': {'cells_param_size': {
            'month': (-1, close_months), 'valuation_month': (-1, close_months),
            'scen_id': scenarios, 'num_scenarios': scenarios,
            'annual_steps': (close_months - 2) // 12 + 1, 'key': 2147483647}},
    }}


def copy_inputs(folder, source=PRODUCT):
    """Copy the book's CSVs from ``source`` into ``folder``, the key tenors below it."""
    folder = Path(folder)
    (folder / SHOCK_STEPS_FILE).parent.mkdir(parents=True, exist_ok=True)
    for table in Path(source).glob('*.csv'):
        shutil.copyfile(table, folder / table.name)
    shutil.copyfile(Path(source) / SHOCK_STEPS_FILE, folder / SHOCK_STEPS_FILE)


def build(folder, log=None):
    """Export, trace and compile the model in ``folder``; return the seconds it took."""
    import time
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    model = build_model()
    try:
        copy_inputs(folder)
        model.export(folder / PACKAGE, locked_spaces=['ESG', 'Market'])
        (folder / 'spec.py').write_text(repr(spec(model)) + '\n', encoding='utf-8')
    finally:
        model.close()
    shutil.copyfile(HERE / 'sample.py', folder / 'sample.py')
    with open(log or folder / 'compile.log', 'w') as stream:
        done = subprocess.run([sys.executable, '-c', _ENTRY, PACKAGE, '--sample', 'sample.py',
                               '--spec', 'spec.py'], cwd=folder, stdout=stream,
                              stderr=subprocess.STDOUT)
    if done.returncode:
        raise RuntimeError(f'the compiler exited with {done.returncode}; see compile.log in '
                           f'{folder}')
    (folder / STAMP).write_text(build_stamp() + '\n', encoding='utf-8')
    if not is_built(folder):
        raise RuntimeError(f'the compiler left no extension module in {folder}')
    return time.perf_counter() - start


def build_stamp():
    """A digest of what a build depends on: this package, the MYGA_US_SEC model and book it is
    built from, the compiler and modelx sources, and the interpreter.

    A build made from other sources, by another compiler or for another interpreter has another
    stamp, so :func:`is_built` does not take it for a build of this one.
    """
    digest = hashlib.sha256(sys.version.encode())
    roots = [HERE, PRODUCT / 'MYGA_US_SEC']
    for name in ('modelx_cython', 'modelx'):
        found = importlib.util.find_spec(name)
        if found is not None and found.origin:
            roots.append(Path(found.origin).resolve().parent)
    files = sorted(PRODUCT.glob('*.csv'))
    for root in roots:
        files += sorted(path for path in root.rglob('*')
                        if path.suffix in ('.py', '.pyx', '.pxd', '.csv', '.json'))
    for path in files:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def is_built(folder):
    """Whether ``folder`` holds a compiled package built from the present sources, by the present
    compiler and modelx, for this interpreter."""
    folder = Path(folder)
    stamp = folder / STAMP
    if not stamp.is_file() or stamp.read_text(encoding='utf-8').strip() != build_stamp():
        return False
    suffixes = tuple(importlib.machinery.EXTENSION_SUFFIXES)
    package = folder / f'{PACKAGE}_cy'
    return any((package / f'_mx_classes{suffix}').is_file() for suffix in suffixes)


def load(folder, input_dir=None):
    """The compiled model in ``folder``, reading its book from ``input_dir``.

    ``input_dir`` holds the CSVs, as :func:`copy_inputs` lays them out; by default the
    build's own copy of the shipped book.  The input tables are read here, before any
    report, so that a report's time is the projection's.
    """
    folder = Path(folder).resolve()
    if not is_built(folder):
        raise RuntimeError(f'{folder} holds no compiled DV01 model for this interpreter')
    sys.path.insert(0, str(folder))
    module = importlib.import_module(f'{PACKAGE}_cy')
    classes = importlib.import_module(f'{PACKAGE}_cy._mx_classes')
    if Path(classes.__file__).suffix not in ('.so', '.pyd'):
        raise RuntimeError(f'{folder} imported without its extension modules')
    model = module.mx_model
    model.path = Path(input_dir or folder).resolve() / PACKAGE
    for table in (*TABLES, 'shock_key_months'):
        getattr(model.Data, table)()
    model.ESG.param_table()
    model.ESG.curve_knots()
    return model
