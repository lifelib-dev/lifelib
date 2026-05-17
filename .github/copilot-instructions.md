# GitHub Copilot Instructions for lifelib

## Project Overview

lifelib is a Python package that contains reusable project templates for building actuarial models, particularly in life insurance. 

lifelib is not meant to be used directly by importing it in user code; instead, users create new projects by copying the provided templates, using `lifelib-create` from shell or command line, or using the `lifelib.create` API function from Python.

Each project template is called a "library" and is designed to be easily extended and customized for specific modeling needs. Many of the libraries include actuarial models built using the modelx framework.

## Key Technologies

- **Python**: 3.7+
- **modelx**: Core dependency for model development (>=0.31.0)
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **openpyxl**: Excel file handling

## Project Structure
```
lifelib/
├── libraries/          # New project templates
│   ├── basiclife/     # Includes modelx models for simple life issurance products
│   ├── appliedlife/   # Includes integrated life insurance models
│   ├── assets/        # Includes a bond portfolio model
│   ├── economic/      # Economic scenarios
│   ├── ifrs17a/       # IFRS 17 reporting
│   ├── savings/       # Include modelx models for savings products
│   └── cluster/       # Cluster analysis
├── projects/          # Old project templates (To be updated)
│   ├── simplelife/
│   ├── nestedlife/
│   ├── ifrs17sim/
│   └── fastlife/
├── commands/          # CLI commands
└── tests/             # Test suite
```

## Documentation

- RST files in `doc/source/`
- Generated examples from Jupyter notebooks
- API documentation auto-generated from docstrings

## CLI Development
- Entry point defined in `setup.py`
- Commands in `lifelib/commands/`
- Use `create` command for generating projects
- Support for interactive model creation





