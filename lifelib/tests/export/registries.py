"""The registered models of ``uslib``, ``uklib`` and ``jplib``, read from their registries.

Each of those libraries ships an in-library test suite whose registry — ``us_registry``,
``uk_registry``, ``jp_registry`` — is the single source of truth for which models the
library has and where they sit. ``test_model_conventions`` asserts that the registry
agrees with the folders on disk, so reusing it here means a model added to a library is
covered by the export tests without a second list to keep in step.

The registries are loaded **by path**. Those ``tests`` directories are not packages, and
their modules are importable only because pytest prepends each directory to ``sys.path``
when it collects it; a plain ``import us_registry`` here would therefore work or not
depending on what else the run collected first.
"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve()
LIBRARIES = HERE.parents[2] / "libraries"

# library -> the module name its registry lives under, which is unique per library for
# the reason given in the registry's own docstring.
REGISTRIES = {
    "uslib": "us_registry",
    "uklib": "uk_registry",
    "jplib": "jp_registry",
}


def _load_registry(library, module_name):
    """Import ``<library>/tests/<module_name>.py`` without touching ``sys.path``."""
    path = LIBRARIES / library / "tests" / (module_name + ".py")
    spec = importlib.util.spec_from_file_location(
        f"_lifelib_export_tests_{module_name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def registered_models():
    """``(library, model name, path to the model folder)`` for every registered model."""
    models = []
    for library, module_name in REGISTRIES.items():
        registry = _load_registry(library, module_name)
        for name, (relative_path, _metadata) in sorted(registry.MODELS.items()):
            models.append((library, name, LIBRARIES / library / relative_path))
    return models


MODELS = registered_models()

# "uslib/Term_US_A" and so on, so a failure names the library as well as the model.
IDS = [f"{library}/{name}" for library, name, _path in MODELS]
