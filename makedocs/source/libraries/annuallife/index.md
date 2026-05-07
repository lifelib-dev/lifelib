```{module} annuallife
```
```{include} /banners.rst
```

# The **annuallife** Library

|modelx badge|

```{warning}
:mod:`annuallife` is in its active development phase, and its contents are
subject to change.
```

## Overview

The **annuallife** library is the updated successor of the legacy
{ref}`project_simplelife` project. It packages
{mod}`~annuallife.TradLife_A`, an annual projection model of basic
traditional life policies, alongside the original intermediate
{mod}`~annuallife.model_new` snapshot from which it was derived.

{mod}`~annuallife.TradLife_A` projects life insurance cashflows and their
present values for policies represented by model points. Projected items
include:

* Premium income,
* Commissions and expenses,
* Benefit outgo.

Cells for investment income, change in reserve and profits are included
but not tested.

Compared with the original *simplelife* model, {mod}`~annuallife.TradLife_A`
introduces:

* **Snake-case cell and reference names** following the
  {mod}`basiclife.BasicTerm_SC` naming convention
  (for example, ``net_cf`` rather than ``NetInsurCF``,
  ``claims`` rather than ``BenefitDeath``).
* **Array-based model points.** Policy attributes are read from
  *input.xlsx* as 1-D NumPy arrays and addressed by the integer
  parameter ``idx`` (0-based) instead of ``PolicyID`` (1-based).
* **A flatter space layout.** ``Assumptions`` and ``PolicyAttrs`` are
  top-level spaces instead of being nested inside ``Projection``.
* **A renamed input space.** The space holding *input.xlsx*-backed
  References is now ``InputData`` and is referenced as ``input_data``
  by the rest of the model.

See {mod}`~annuallife.TradLife_A` for more details.

## How to Use the Library

As explained in the {ref}`create-a-project` section,
create your own copy of the *annuallife* library.
For example, to copy as a folder named *annuallife*
under the path *C:\\path\\to\\your\\*, type below in an IPython console:

```python
>>> import lifelib

>>> lifelib.create("annuallife", r"C:\path\to\your\annuallife")
```

The {mod}`~annuallife.TradLife_A` model loads its data from *input.xlsx*,
which lives next to the model directory inside the library folder.

To read the model on the IPython console, change the working directory
to the library folder and use modelx's `read_model` function:

```python
>>> import modelx as mx

>>> m = mx.read_model("TradLife_A")
```

## Library Contents

```{toctree}
:hidden:
:maxdepth: 1

TradLife_A
tradlife_a-demo
tradlife_a-space-overview
```

```{table}
:widths: 25 75

| File or Folder            | Description                                                       |
| ------------------------- | ----------------------------------------------------------------- |
| ``TradLife_A``            | The {mod}`~annuallife.TradLife_A` model.                          |
| ``model_new``             | The intermediate backup model that ``TradLife_A`` was derived from. |
| ``input.xlsx``            | Excel workbook holding policy data, assumptions, mortality tables, scenarios and product specs. |
| ``plot_tradlife_a.py``    | sphinx-gallery plot script that renders the cashflow chart.       |
| ``plot_pvcashflows.py``   | sphinx-gallery plot script that renders present-value cashflows.  |
| ``tradlife_a-demo.ipynb`` | Jupyter notebook demonstrating cashflow projection.               |
| ``tradlife_a-space-overview.ipynb`` | Tutorial notebook on the space tree of {mod}`~annuallife.TradLife_A`. |
```

## Jupyter Notebooks

[badge-image]: https://colab.research.google.com/assets/colab-badge.svg "Open In Colab"
[tradlife_a-demo]: https://colab.research.google.com/github/lifelib-dev/lifelib/blob/current/lifelib/libraries/annuallife/tradlife_a-demo.ipynb
[tradlife_a-space-overview]: https://colab.research.google.com/github/lifelib-dev/lifelib/blob/current/lifelib/libraries/annuallife/tradlife_a-space-overview.ipynb

|                                       |                                                |
| ------------------------------------- | ---------------------------------------------- |
| {doc}`tradlife_a-demo`                | [![badge-image]][tradlife_a-demo]              |
| {doc}`tradlife_a-space-overview`      | [![badge-image]][tradlife_a-space-overview]    |
