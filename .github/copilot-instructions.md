# Copilot Instructions for lifelib

## Repository Overview

**lifelib** is a collection of open-source life actuarial models written in Python. It provides versatile and transparent actuarial models for pricing, valuation, risk modeling, and asset-liability management. The models are built using `modelx`, an open-source Python package for building object-oriented models.

### Key Information
- **Language**: Python 3.7+
- **Project Type**: Python package distributed via PyPI
- **Primary Dependencies**: modelx (>=0.26.0), pandas, numpy, openpyxl, networkx
- **Size**: ~40 test files, multiple libraries and project templates
- **Testing Framework**: pytest with coverage (pytest-cov)
- **Code Quality Tools**: flake8, black, isort

## Build and Development Setup

### Initial Environment Setup

**ALWAYS** use the Makefile for environment setup. The project requires a virtual environment with specific dependencies.

1. **Initialize development environment** (first time only):
```bash
make init
```
This creates a virtual environment in `venv_lifelib/` and installs all dev dependencies. Takes ~30-60 seconds.

2. **Activate the virtual environment**:
```bash
source venv_lifelib/bin/activate
```

### Installation Options

- **Development mode** (recommended for code changes):
  ```bash
  make install-dev
  ```
  Installs: pytest, pytest-cov, pytest-xdist, pandas, numpy, openpyxl, flake8, black, isort, modelx

- **Test mode only**:
  ```bash
  make install-test
  ```

- **Production mode**:
  ```bash
  make install
  ```

**IMPORTANT**: Always activate the virtual environment (`source venv_lifelib/bin/activate`) before running any Python commands or tests.

## Running Tests

### Basic Test Execution

Tests take approximately 90-120 seconds to complete. The test suite includes 40 tests covering libraries, projects, and commands.

```bash
# Run all tests with coverage
make test

# Or directly with pytest (venv must be activated)
pytest -v --cov=lifelib --cov-report=term-missing
```

**Expected Results**: All 40 tests should pass. Some FutureWarnings from pandas are expected in the ifrs17a library tests but do not cause failures.

### Test Locations

Tests are organized in multiple locations:
- `lifelib/tests/` - Main test directory (commands, data, filecomp, projects)
- `lifelib/libraries/*/tests/` - Library-specific tests (e.g., ifrs17a)
- `lifelib/projects/*/tests/` - Project-specific tests

### Advanced Testing

```bash
# Run tests in parallel (faster)
make test-fast

# Generate HTML coverage report
make test-cov  # Opens htmlcov/index.html

# Run tests across multiple Python versions
make tox
```

## Code Quality and Linting

### Linting

**NOTE**: The codebase has pre-existing lint warnings in the solvency2 project scripts (undefined names like 'pol', 'asmp', 'scen'). These are intentional as they're defined dynamically by the modelx framework. **Do not attempt to fix these warnings**.

```bash
# Check code quality
make lint

# Or directly
flake8 lifelib --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 lifelib --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Code Formatting

**ALWAYS** format code before committing:

```bash
# Auto-format code with black and isort
make format

# Check formatting without modifying
make check

# Run all checks
make check-all
```

**Formatting Standards**:
- Line length: 88 characters (black default)
- Import sorting: Use isort with black profile
- Target Python versions: 3.7-3.13

## Building the Package

```bash
# Build source distribution and wheel
make build

# Clean and rebuild
make dist

# Clean build artifacts
make clean
```

Build artifacts are created in `dist/` directory.

## Project Structure

### Root Directory Files

Key configuration files in the repository root:
- `pyproject.toml` - Package metadata, dependencies, pytest/coverage/black/isort configuration
- `setup.py` - Legacy setup script (still used for package data collection)
- `Makefile` - Development automation (ALWAYS use this for common tasks)
- `tox.ini` - Multi-environment testing configuration
- `setup.cfg` - Minimal wheel configuration
- `.gitignore` - Git ignore patterns
- `MANIFEST.in` - Package manifest for non-Python files

### Source Code Organization

```
lifelib/
├── __init__.py           # Package version and exports
├── _dirs.py              # Directory utilities
├── commands/             # CLI commands (lifelib-create)
│   └── create.py         # Project creation command
├── libraries/            # Reusable model libraries
│   ├── appliedlife/
│   ├── assets/
│   ├── basiclife/
│   ├── cluster/
│   ├── economic/
│   ├── economic_curves/
│   ├── ifrs17a/          # IFRS17 accounting library (has tests/)
│   └── savings/
├── projects/             # Sample project templates
│   ├── fastlife/
│   ├── ifrs17sim/
│   ├── nestedlife/
│   ├── simplelife/
│   ├── smithwilson/
│   └── solvency2/
└── tests/                # Main test suite
    ├── commands/         # CLI command tests
    ├── data/             # Test data generators
    ├── filecomp/         # File comparison utilities
    └── projects/         # Project integration tests
```

### Additional Directories

- `devnotes/` - Developer documentation (MAKEFILE.md, TESTING.md, TEST_MIGRATION_SUMMARY.md)
- `makedocs/` - Sphinx documentation source (separate from main package)
- `LICENSES/` - License information

## GitHub Workflows and CI

The project uses GitHub Actions for CI/CD with three jobs:

### 1. Tests Job (`.github/workflows/tests.yml`)

**Matrix Testing**:
- Python versions: 3.9, 3.10, 3.11, 3.12, 3.13
- Operating systems: ubuntu-latest, windows-latest, macos-latest
- Strategy: fail-fast = false (all combinations run)

**Steps**:
1. Checkout code
2. Set up Python (with pip cache)
3. Install dependencies: `pip install -e .[test]`
4. Run tests: `pytest -v --cov --cov-report=xml --cov-report=term`
5. Upload coverage to Codecov (Ubuntu + Python 3.11 only)

### 2. Lint Job

**Environment**: Ubuntu with Python 3.11

**Steps**:
1. Install dev dependencies: `pip install -e .[dev]`
2. Run flake8 (continue-on-error: true)
3. Check isort (continue-on-error: true)
4. Check black formatting (continue-on-error: true)

**NOTE**: Lint checks have continue-on-error enabled, meaning they won't fail the build but will show warnings.

### 3. Test Install Job

Validates package build and installation:
1. Build package: `python -m build`
2. Install wheel: `pip install dist/*.whl`
3. Test import: `python -c "import lifelib; print(f'lifelib version: {lifelib.__version__}')"`

## Common Development Workflows

### Before Committing Code

```bash
# 1. Format code
make format

# 2. Run tests
make test

# 3. Check code quality (optional, has existing warnings)
make lint
```

### Starting Fresh / Clean Environment

```bash
# Remove everything and start over
make clean-all
make init
source venv_lifelib/bin/activate
make test
```

### Daily Development

```bash
# Activate environment
source venv_lifelib/bin/activate

# Make changes...

# Test changes
make test

# Format code
make format
```

## Important Notes and Gotchas

### 1. Virtual Environment Required

**ALWAYS** activate the virtual environment before running Python commands. Commands will fail if the venv is not activated.

### 2. Modelx Framework

The project uses `modelx` which creates dynamic references in model code. Variables like `pol`, `asmp`, `scen`, `_space`, `_model` in project scripts are defined at runtime by modelx. **Do not treat F821 "undefined name" warnings for these as errors**.

### 3. Test Execution Time

Full test suite takes 90-120 seconds. Use `pytest -k "test_name"` to run specific tests during development.

### 4. Existing Lint Issues

The solvency2 project has ~50+ F821 warnings that are intentional. Do not attempt to "fix" these as they will break the models.

### 5. Package Data

The package includes non-Python files (Excel files, Jupyter notebooks, CSV, JSON) from `lifelib/libraries/` and `lifelib/projects/`. The `setup.py` has a custom `get_package_data()` function to collect these.

### 6. Windows Compatibility

The Makefile works best on Linux/macOS. For Windows, use:
- WSL (Windows Subsystem for Linux)
- Git Bash (includes GNU Make)
- Or run commands manually (see devnotes/TESTING.md)

### 7. Build Tool Installation

The build tool is NOT included in dev dependencies. Install separately if needed:
```bash
pip install build
python -m build
```

## Debugging Tips

### Import Errors
Ensure package is installed in editable mode:
```bash
pip install -e .
```

### Test Discovery Issues
Clear pytest cache:
```bash
pytest --cache-clear
```

### Dependency Conflicts
Recreate virtual environment:
```bash
make clean-all
make init
```

## Trust These Instructions

These instructions have been validated by:
1. Running `make init` successfully
2. Running `pytest` with all 40 tests passing
3. Testing `make lint`, `make format`, and other commands
4. Reviewing all configuration files and workflows

**If you encounter issues not documented here**, investigate the specific error before assuming these instructions are incorrect. The commands and workflows documented above are known to work correctly.
