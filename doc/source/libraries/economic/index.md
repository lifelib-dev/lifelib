```{module} economic
```

# The **economic** Library

[![modelx](https://img.shields.io/badge/modelx-0080FF)](https://docs.modelx.io)

## Overview

The **economic** library is for modeling economic scenarios.
Currently, the library includes three models:

```{toctree}
:maxdepth: 1

BasicHullWhite
BasicG2PP
CashValue_ME_G2PP
```

{mod}`~economic.BasicHullWhite` simulates the short rate of the Hull-White model.
{mod}`~economic.BasicG2PP` generates risk-neutral interest rate scenarios
from the G2++ model, fitted to an initial yield curve,
for calculating the time value of options and guarantees (TVOG).
{mod}`~economic.CashValue_ME_G2PP` calculates the TVOG of savings policies
with a maturity guarantee under those scenarios.

```{todo}
This library is in its early alpha release stage, and more
contents will be added in near future.
```

## How to Use the Library

As explained in the {ref}`create-a-project` section,
Create you own copy of the *economic* library.
For example, to copy as a folder named *economic*
under the path *C:\\path\\to\\your\\*, type below in an IPython console:

```python
>>> import lifelib

>>> lifelib.create("economic", r"C:\path\to\your\economic")
```

## Jupyter Notebooks

[badge-image]: https://colab.research.google.com/assets/colab-badge.svg "Open In Colab"
[hull-white-simulation]: https://colab.research.google.com/github/lifelib-dev/lifelib/blob/current/lifelib/libraries/economic/hull-white-simulation.ipynb
[g2pp-simulation]: https://colab.research.google.com/github/lifelib-dev/lifelib/blob/current/lifelib/libraries/economic/g2pp-simulation.ipynb
[g2pp-tvog]: https://colab.research.google.com/github/lifelib-dev/lifelib/blob/current/lifelib/libraries/economic/g2pp-tvog.ipynb

|                              |                                         |
|------------------------------|-----------------------------------------|
| {doc}`hull-white-simulation` | [![badge-image]][hull-white-simulation] |
| {doc}`g2pp-simulation`       | [![badge-image]][g2pp-simulation]       |
| {doc}`g2pp-tvog`             | [![badge-image]][g2pp-tvog]             |

```{toctree}
:hidden:
:maxdepth: 1

hull-white-simulation
g2pp-simulation
g2pp-tvog
```

## Library Contents

| File or Folder                       | Description                                                                             |
|--------------------------------------|-----------------------------------------------------------------------------------------|
| BasicHullWhite                       | The {mod}`~economic.BasicHullWhite` model.                                              |
| BasicG2PP                            | The {mod}`~economic.BasicG2PP` model.                                                   |
| CashValue_ME_G2PP                    | The {mod}`~economic.CashValue_ME_G2PP` model.                                           |
| g2pp_input.xlsx                      | Excel input read by {mod}`~economic.BasicG2PP` and {mod}`~economic.CashValue_ME_G2PP`   |
| hull-white-simulation.ipynb          | Jupyter notebook {doc}`hull-white-simulation`                                           |
| g2pp-simulation.ipynb                | Jupyter notebook {doc}`g2pp-simulation`                                                 |
| g2pp-tvog.ipynb                      | Jupyter notebook {doc}`g2pp-tvog`                                                       |
| plot_ex1_short_rate_paths.py         | Python script for {doc}`/generated_examples/economic/plot_ex1_short_rate_paths`         |
| plot_ex2_short_rate_mean_variance.py | Python script for {doc}`/generated_examples/economic/plot_ex2_short_rate_mean_variance` |
| plot_ex3_disc_factor_convergence.py  | Python script for {doc}`/generated_examples/economic/plot_ex3_disc_factor_convergence`  |
| plot_ex4_g2pp_rate_fan.py            | Python script for {doc}`/generated_examples/economic/plot_ex4_g2pp_rate_fan`            |
| plot_ex5_g2pp_martingale.py          | Python script for {doc}`/generated_examples/economic/plot_ex5_g2pp_martingale`          |
