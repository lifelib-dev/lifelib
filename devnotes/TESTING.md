# Testing Guide for lifelib

This document describes how to run tests for the lifelib project.

## Prerequisites

The project requires Python 3.7 or higher. Tests are run using pytest.

## Installation for Testing

To install the package with test dependencies:

```bash
pip install -e .[test]
```

For development (includes linting and formatting tools):

```bash
pip install -e .[dev]
```

## Running Tests

### Quick Test Run

Run all tests:

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=lifelib --cov-report=term-missing
```

### Run Specific Tests

Run tests in a specific file:

```bash
pytest lifelib/tests/projects/test_simplelife.py
```

Run tests matching a pattern:

```bash
pytest -k "test_present_value"
```

### Run Tests in Parallel

For faster execution on multi-core systems:

```bash
pytest -n auto
```

## Using Tox

Tox allows testing across multiple Python versions. Make sure you have the desired Python versions installed.

### Run tests on all configured Python versions:

```bash
tox
```

### Run tests on a specific Python version:

```bash
tox -e py311
```

### Run linting checks:

```bash
tox -e lint
```

### Generate coverage report:

```bash
tox -e coverage
```

### Auto-format code:

```bash
tox -e format
```

## Code Quality

### Linting

Check for code issues with flake8:

```bash
flake8 lifelib
```

### Formatting

Check code formatting with black:

```bash
black --check lifelib
```

Auto-format code:

```bash
black lifelib
```

### Import Sorting

Check import order with isort:

```bash
isort --check-only lifelib
```

Auto-sort imports:

```bash
isort lifelib
```

## Continuous Integration

The project uses GitHub Actions for CI/CD:

- **Tests**: Run on every push and pull request
- **Python versions**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Operating systems**: Ubuntu, Windows, macOS
- **Coverage**: Uploaded to Codecov for Python 3.11 on Ubuntu

### Viewing CI Results

1. Go to the repository on GitHub
2. Click on "Actions" tab
3. View the latest workflow runs

## Test Structure

```
lifelib/
├── tests/                      # Main test directory
│   ├── projects/              # Tests for projects
│   ├── commands/              # Tests for CLI commands
│   ├── data/                  # Test data generators
│   └── filecomp/              # File comparison utilities
├── libraries/
│   └── ifrs17a/
│       └── tests/             # Library-specific tests
└── projects/
    └── smithwilson/
        └── smith-wilson-py/
            └── smithwilson/
                └── tests/     # Project-specific tests
```

## Writing Tests

### Test Naming

- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
import pytest

def test_example():
    assert 1 + 1 == 2

class TestCalculation:
    def test_addition(self):
        assert 2 + 2 == 4
```

### Using Markers

Mark slow tests:

```python
@pytest.mark.slow
def test_slow_operation():
    # Test code here
    pass
```

Run tests excluding slow ones:

```bash
pytest -m "not slow"
```

## Coverage Reports

Coverage reports are generated in multiple formats:

- **Terminal**: Displayed after test run
- **HTML**: `htmlcov/index.html` (open in browser)
- **XML**: `coverage.xml` (for CI tools)

## Troubleshooting

### Tests Failing Locally

1. Ensure all dependencies are installed: `pip install -e .[test]`
2. Check Python version compatibility: `python --version`
3. Clear pytest cache: `pytest --cache-clear`

### Import Errors

Make sure the package is installed in editable mode:

```bash
pip install -e .
```

### Tox Errors

Rebuild tox environments if you encounter issues:

```bash
tox -r
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [tox documentation](https://tox.wiki/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
