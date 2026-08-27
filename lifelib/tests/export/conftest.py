"""Fixtures that export each registered model and hand back both sides of the comparison.

The export is written **beside the model folder**, in a copy of the product directory made
under ``tmp_path``. That placement is not a detail: these libraries keep their inputs as
external CSVs and resolve them in ``Data`` as ``_model.path.parent``, and in an exported
package ``path`` is the package's own directory. An export written anywhere else imports
cleanly and then raises ``FileNotFoundError`` on the first evaluation.
``libraries/test_tradlife_a.py`` copies a model and its workbook to a temporary directory
for the same reason.

Nothing is written into ``lifelib/libraries``. Besides the usual reason not to write into
the source tree, ``setup.py``'s ``get_package_data`` walks that directory and sweeps every
``*.py`` it finds into ``package_data``, so a stray export would ship in the wheel.
"""
import importlib
import shutil
import sys
import textwrap

import pytest

from .registries import IDS, MODELS


@pytest.fixture(scope="session")
def exporter_qualifies_names(tmp_path_factory):
    """Whether this modelx exporter qualifies model references after a generator expression.

    modelx 0.32.0 as released leaves them bare, which makes the exported formula raise
    ``NameError`` when it is first evaluated (it reaches ``DIA_US_S.result_annual`` in
    ``uslib``). The check is behavioural rather than a version comparison because the fix
    landed after 0.32.0 was tagged: ``modelx.__version__`` reads ``0.32.0`` either way.
    """
    import modelx as mx

    source = textwrap.dedent("""\
        def probe():
            xs = [1, 2]
            return [sum(other(x) for x in xs)], [other(x) for x in xs]
        """)

    model = mx.new_model(name="ExportProbe")
    try:
        space = model.new_space("Probe")
        space.new_cells(name="other", formula="lambda x: x")
        space.new_cells(name="probe", formula=source)
        path = tmp_path_factory.mktemp("export_probe") / "probe_nomx"
        model.export(path)
        generated = (path / "_mx_classes.py").read_text(encoding="utf-8")
    finally:
        model.close()

    # The reference inside the generator expression is qualified even by the unfixed
    # exporter; the one in the comprehension that follows it is the one that regressed.
    return generated.count("self.other(") == 2


@pytest.fixture(scope="module", params=MODELS, ids=IDS)
def exported(request, tmp_path_factory, exporter_qualifies_names):
    """One registered model, as ``(name, modelx model, exported model, package folder)``.

    Module-scoped, so each model is read and exported once and every test below shares it.
    The modelx model is read from the library itself while the exported one runs out of the
    copy, so the two sides of the comparison do not share a directory.
    """
    if not exporter_qualifies_names:
        pytest.skip(
            "this modelx exporter leaves model references after a generator expression "
            "unqualified; the exported models raise NameError when evaluated")

    import modelx as mx

    _library, name, model_path = request.param

    product = tmp_path_factory.mktemp("product")
    shutil.copytree(model_path.parent, product / model_path.parent.name,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    package = product / model_path.parent.name / (name + "_nomx")

    model = mx.read_model(model_path)
    try:
        model.export(package)

        sys.path.insert(0, str(package.parent))
        try:
            nomx = importlib.import_module(name + "_nomx").mx_model
        finally:
            sys.path.remove(str(package.parent))

        yield name, model, nomx, package
    finally:
        model.close()
