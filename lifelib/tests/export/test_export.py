"""Every registered model in uslib, uklib, jplib and frlib exports to a working nomx package.

``Model.export`` writes a model out as a pure-Python package that does not import modelx.
For these libraries that is a supported way to run the models, so the export is part of
what they promise, and this module holds the promise to two things: the generated package
must evaluate at all, and it must produce the same numbers as the model it came from.

The two are tested separately because they fail separately. A name the exporter fails to
qualify is not visible in the generated file's shape — the package imports fine and the
formula raises ``NameError`` the first time something calls it, which may be in a cells no
test happens to reach. :func:`test_no_generated_name_resolves_to_nothing` therefore checks
the whole generated module symbolically rather than waiting for evaluation to stumble on
it, and it covers every formula in the model, not the ones a projection happens to use.

The value comparison runs over the ``result_*`` cells, which is the library convention for
a published statement: ``result_cf`` everywhere, plus whatever else a product publishes,
such as ``DIA_US_S.result_annual``. Comparing the frames rather than a hand-picked set of
cells means a model that grows a new statement is covered by that fact alone.
"""
import builtins
import symtable

import pandas as pd
import pytest

modelx = pytest.importorskip("modelx")


GENERATED_MODULES = {"__init__.py", "_mx_sys.py", "_mx_classes.py", "_mx_model.py"}


def generated_files(package):
    """The package's own file names, ignoring the interpreter's caches.

    ``__pycache__`` appears as soon as the package is imported, which the fixture does, so
    it is here in every run and is not part of what was generated.
    """
    return {path.name for path in package.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts}


def unresolvable_names(package):
    """Names in the generated formulas that are global and defined nowhere.

    The exporter rewrites a formula's references to the model's own objects into
    ``self.<name>``. A name it fails to rewrite stays a bare global in the generated
    module, where nothing defines it: the formula then raises ``NameError`` when it is
    evaluated. ``symtable`` finds those without running anything.
    """
    source = (package / "_mx_classes.py").read_text(encoding="utf-8")
    table = symtable.symtable(source, str(package / "_mx_classes.py"), "exec")
    defined = {symbol.get_name() for symbol in table.get_symbols()} | set(dir(builtins))

    found = []

    def walk(scope, path):
        for child in scope.get_children():
            here = path + [child.get_name()]
            if child.get_type() == "function":
                for symbol in child.get_symbols():
                    if symbol.is_global() and symbol.get_name() not in defined:
                        found.append(f"{'.'.join(here)} -> {symbol.get_name()}")
            walk(child, here)

    walk(table, [])
    return found


def published_statements(model):
    """The names of the model's zero-argument ``result_*`` cells."""
    cells = model.Projection.cells
    return [name for name in sorted(cells)
            if name.startswith("result_") and not cells[name].parameters]


def assert_statements_match(model, nomx, point_id, statements):
    """Every published statement of one model point, compared value by value.

    A statement is usually a DataFrame, but one that publishes a single labelled column
    -- ``PER_FR_S.result_settlement``, the only one today -- returns a Series. The
    comparison therefore dispatches on what the statement actually is, and asserts first
    that the export returns the same type as the model, so a statement that changed shape
    fails here rather than being compared as something it is not.
    """
    for name in statements:
        expected = getattr(model.Projection[point_id], name)()
        actual = getattr(nomx.Projection[point_id], name)()
        obj = f"{model.name}.Projection[{point_id}].{name}()"
        assert type(expected) is type(actual), (
            f"{obj}: the model returned {type(expected).__name__} and the export "
            f"returned {type(actual).__name__}")
        assert_equal = (pd.testing.assert_series_equal
                        if isinstance(expected, pd.Series)
                        else pd.testing.assert_frame_equal)
        assert_equal(expected, actual, check_exact=True, obj=obj)


def test_the_export_holds_the_generated_modules(exported):
    """An export is four modules and no data: the inputs stay external CSVs."""
    _name, _model, _nomx, package = exported
    assert generated_files(package) == GENERATED_MODULES


def test_the_model_name_survives_the_export(exported):
    """The exported model answers to the name the registry knows it by.

    The package folder is named by the caller, so the model's own name is the only thing
    tying the export back to the model it came from.
    """
    name, _model, nomx, _package = exported
    assert nomx._name == name


def test_no_generated_name_resolves_to_nothing(exported):
    """No formula in the generated module reads a name the module does not define."""
    name, _model, _nomx, package = exported
    unresolvable = unresolvable_names(package)
    assert not unresolvable, (
        f"{name}: the export reads {len(unresolvable)} name(s) that nothing defines, "
        f"which raise NameError when the formula is evaluated: {unresolvable}")


def test_the_first_model_point_matches_the_modelx_model(exported):
    """The exported model reproduces the model it came from, on the first model point.

    The whole table is swept by the slow test below; this one is the always-on check, and
    one model point is enough to catch an export that does not evaluate at all.
    """
    _name, model, nomx, _package = exported
    statements = published_statements(model)
    assert "result_cf" in statements, "every model in these libraries publishes result_cf"
    point_id = model.Data.model_point_table().index[0]
    assert_statements_match(model, nomx, point_id, statements)


@pytest.mark.slow
def test_every_model_point_matches_the_modelx_model(exported):
    """The same, over the whole shipped model point table.

    Marked slow: it evaluates every model point twice, once on each side. Deselect with
    ``-m "not slow"``; the check above still covers whether the export runs.
    """
    _name, model, nomx, _package = exported
    statements = published_statements(model)
    for point_id in model.Data.model_point_table().index:
        assert_statements_match(model, nomx, point_id, statements)
