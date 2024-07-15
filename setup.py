"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

DISTNAME = 'lifelib'
LICENSE = 'MIT License'
AUTHOR = "lifelib Developers"
EMAIL = "admin@lifelib.io"
URL = "https://lifelib.io"

DESCRIPTION = "Actuarial models in Python"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     LONG_DESCRIPTION = f.read()

LONG_DESCRIPTION = """
**lifelib** is a collection of open-source life actuarial models written in Python.
lifelib includes a variety of models, with sample scripts
and Jupyter notebooks that demonstrate how to use the models.

Visit https://lifelib.io for more information!

What for?
---------

lifelib models are highly versatile and transparent.
You can customize lifelib models and utilize them
in various practical areas, such as:

- Model validation / testing
- Pricing / profit testing
- Research / educational projects
- Valuation / cashflow projections
- Asset-liability modeling
- Risk and capital modeling
- Actuarial modernization to replace spreadsheet models


Why lifelib?
------------

By effectively utilizing the models in lifelib,
you can expect the following benefits from both model development and governance perspectives:

- A more efficient, transparent, and faster model development experience
- Model integration with the Python ecosystem (Pandas, Numpy, SciPy, etc.)
- Elimination of spreadsheet errors
- Improved version control and model governance
- Automated model testing

Some of the models in lifelib are built using `modelx`_, an open-source
Python package for building object-oriented models in Python.
By using lifelib, you can enjoy the following advantages:

* Models run fast!
* Formulas are easy to read
* Easy to trace formula dependency and errors
* Formulas are instantly evaluated
* Pandas and Numpy can be utilized
* Object-oriented
* Input from Excel and CSV files
* Documents can be integrated
* Formulas are saved in text files

.. _modelx: http://docs.modelx.io

"""

def get_version(version_tuple):
    # additional handling of a,b,rc tags, this can
    # be simpler depending on your versioning scheme
    if not isinstance(version_tuple[-1], int):
        return '.'.join(
            map(str, version_tuple[:-1])
        ) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))

# path to the packages __init__ module in project source tree
init = path.join(
    path.dirname(__file__), 'lifelib', '__init__.py'
)
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(init))
)[0]


# VERSION is a tuple so we need to eval its line of code.
# We could simply import it from the package but we
# cannot be sure that this package is importable before
# finishing its installation
VERSION = get_version(eval(version_line.split('=')[-1]))


def get_package_data(top_dirs: list):
    result = []
    extensions = ['py', 'ipynb', 'xlsx', 'csv', 'json', 'pickle']
    modelfiles = ['_dynamic_inputs']
    for topd in top_dirs:
        for root, dirs, files in os.walk(topd):
            for f in files:
                l = f.split(".")
                if len(l) > 1 and l[-1] in extensions:
                    # https://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
                    # exclude such *.ipynb in .ipynb_checkpoints/
                    dir_comps = path.normpath(root).split(os.sep)
                    if not any(dname[0] == "." for dname in dir_comps if dname):
                        result.append(path.join(root, f))
                elif len(l) == 1 and f in modelfiles:
                    result.append(path.join(root, f))
    return result


setup(
    name=DISTNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Scientific/Engineering :: Mathematics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],

    # What does your project relate to?
    keywords='actuary model development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'doc']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['modelx>=0.26.0'],

    # If your project only runs on certain Python versions,
    # setting the python_requires argument to the appropriate PEP 440 version
    #  specifier string will prevent pip from installing the project on
    # other Python versions.
    # For example, if your package is for Python 3+ only, write:
    python_requires='>=3.7',

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,tests]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'tests': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'lifelib': get_package_data([
            path.join(here, 'lifelib', 'libraries'),
            path.join(here, 'lifelib', 'projects')
        ]),
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'lifelib-create = lifelib.commands.create:main',
        ],
    },
)
