# Makefile Guide for lifelib

This document describes how to use the Makefile to automate development environment setup and common tasks for the lifelib project.

## Overview

The Makefile provides a convenient way to manage your development environment, run tests, check code quality, and build the package. It automates the creation of a Python virtual environment and installation of dependencies.

## Quick Start

### Initialize Development Environment

To set up a complete development environment with all dependencies:

```bash
make init
```

This will:
- Create a Python virtual environment in `venv_lifelib/`
- Install the package in editable mode
- Install all development dependencies (pytest, flake8, black, isort, etc.)

### Activate the Virtual Environment

After running `make init`, activate the virtual environment:

```bash
source venv_lifelib/bin/activate
```

## Available Commands

To see all available commands with descriptions:

```bash
make help
```

## Environment Management

### Create Virtual Environment

Create the virtual environment without installing dependencies:

```bash
make venv
```

### Install Package

Install in production mode (runtime dependencies only):

```bash
make install
```

Install in development mode (all dev dependencies):

```bash
make install-dev
```

Install in test mode (test dependencies only):

```bash
make install-test
```

### Upgrade Dependencies

Update all installed packages to their latest versions:

```bash
make upgrade
```

### View Environment Info

Display information about the current environment:

```bash
make info
```

This shows:
- Python version
- Virtual environment status
- Installed packages

## Testing

### Run All Tests

Run the full test suite:

```bash
make test
```

### Run Tests with Coverage Report

Generate an HTML coverage report:

```bash
make test-cov
```

The report will be available at `htmlcov/index.html`.

### Run Tests in Parallel

Run tests faster using multiple CPU cores:

```bash
make test-fast
```

### Run Tests with Tox

Test across all configured Python versions:

```bash
make tox
```

Run only linting checks with tox:

```bash
make tox-lint
```

## Code Quality

### Linting

Check code for errors and style issues with flake8:

```bash
make lint
```

### Formatting

Auto-format code with black and isort:

```bash
make format
```

### Check Formatting

Verify code formatting without making changes:

```bash
make check
```

### Run All Checks

Run both linting and formatting checks:

```bash
make check-all
```

## Building and Distribution

### Build Package

Build source distribution and wheel:

```bash
make build
```

The built files will be in the `dist/` directory.

### Clean Build and Rebuild

Clean all generated files and rebuild:

```bash
make dist
```

## Cleaning

### Clean Generated Files

Remove build artifacts, caches, and test reports:

```bash
make clean
```

This removes:
- `build/`, `dist/`, `*.egg-info/` directories
- `.pytest_cache/`, `htmlcov/` directories
- `__pycache__/` directories
- `.pyc`, `.pyo`, `.pyd` files
- Coverage files

### Clean Everything

Remove all generated files including the virtual environment:

```bash
make clean-all
```

**Warning**: This will delete the `.venv/` directory. You'll need to run `make venv` or `make init` again.

## Advanced Usage

### Open Shell in Virtual Environment

Open an interactive shell with the virtual environment activated:

```bash
make shell
```

Type `exit` to leave the shell.

### Common Workflows

#### Starting Fresh on a New Machine

```bash
make init                      # Set up environment
source venv_lifelib/bin/activate  # Activate environment
make test                      # Verify everything works
```

#### Before Committing Code

```bash
make format              # Format code
make check-all           # Verify code quality
make test                # Run tests
```

#### Preparing a Release

```bash
make clean-all           # Start clean
make init                # Reinstall everything
make test                # Run tests
make tox                 # Test all Python versions
make dist                # Build distribution
```

#### Daily Development

```bash
source venv_lifelib/bin/activate  # Activate environment
# ... make your changes ...
make test                         # Test your changes
make format                       # Format new code
```

## Integration with Other Tools

The Makefile complements the existing development tools:

- **pyproject.toml**: Defines package metadata and dependencies
- **tox.ini**: Configures multi-environment testing
- **pytest**: Test runner (configured in pyproject.toml)
- **GitHub Actions**: CI/CD pipeline

You can use the Makefile commands locally, while GitHub Actions uses the same underlying tools (pytest, flake8, etc.) for continuous integration.

## Makefile Variables

The Makefile uses these variables (you don't need to modify them):

- `PYTHON`: Python 3 executable (default: `python3`)
- `VENV`: Virtual environment directory (default: `venv_lifelib`)
- `BIN`: Binary directory in venv (default: `venv_lifelib/bin`)

## Troubleshooting

### "make: command not found"

Install GNU Make:

```bash
# Ubuntu/Debian
sudo apt-get install make

# macOS (usually pre-installed)
# If not: install via Xcode Command Line Tools
xcode-select --install
```

### Virtual Environment Not Working

Clean and recreate:

```bash
make clean-all
make init
```

### Permission Errors

Ensure you have write permissions in the project directory.

### Python Version Issues

The Makefile uses `python3` by default. Ensure Python 3.7+ is installed:

```bash
python3 --version
```

If you need a specific Python version, you can modify the `PYTHON` variable in the Makefile or create a symbolic link.

## Windows Compatibility

The Makefile is designed for Unix-like systems (Linux, macOS). On Windows:

- Use **WSL (Windows Subsystem for Linux)** for the best experience
- Or use **Git Bash** which includes GNU Make
- Alternatively, run commands manually from PowerShell (see TESTING.md)

## Resources

- [GNU Make documentation](https://www.gnu.org/software/make/manual/)
- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [pip documentation](https://pip.pypa.io/)

## See Also

- `TESTING.md` - Detailed testing guide
- `pyproject.toml` - Package configuration and dependencies
- `tox.ini` - Multi-environment testing configuration
