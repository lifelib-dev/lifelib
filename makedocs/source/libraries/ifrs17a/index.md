```{module} ifrs17a
```
# The **ifrs17a** library

## Overview

This library includes Python modules that calculate [IFRS 17] figures
for sample sets of input data. 
The modules read input data such as dimensions, data nodes, discount rates,
and both actual and nominal cashflows,
then calculate items used for IFRS 17 reporting, such as present value
of cashflows, contractual service margin, loss component and loss recovery component.
The calculation logic is based on [IFRS 17 Calculation Engine],
which is developed and made open-source under the MIT license by [Systemorph], a Swiss software firm. 

[IFRS 17]: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
[IFRS 17 Calculation Engine]: https://github.com/Systemorph/IFRS17CalculationEngine
[Systemorph]: https://systemorph.com/

```{seealso}
* [Systemorph's repository on github](https://github.com/Systemorph/IFRS17CalculationEngine)
* [Systemorph's site](https://systemorph.com/) 
* [Systemorph's YouTube channel](https://www.youtube.com/@systemorph)
* [Crude primary transltion of Systemorph's C# codebase into Python](https://github.com/lifelib-dev/IFRS17CalculationEnginePython)
```

## Limitations

This library is experimental, and has been tested only with a limited number of sample sets. 
The calculation logic is not validated, and may not comply with the standard or its variants. 
As this library is in an early stage of development, error-proofing in the code is not comprehensive.
Although this library implements some caching mechanisms, since the entire code is witten in Python, 
the code may not run fast enough for a large set of input data.

## How to Set Up the Library

You need Python 3.8 or a newer version for this library to work.
This library does not use modelx.
The included modules use the following packages.
Most of the packages are pre-installed in major Python distributions,
but if any of them are missing, install them by `pip` or `conda` manually.

```{admonition} Additional packages used
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [openpyxl](https://openpyxl.readthedocs.io)
```

As explained in the {ref}`create-a-project` section,
create you own copy of the *ifrs17a* library.
For example, to copy as a folder named *myifrs17*
under the path *C:\\path\\to\\your\\*, type below in an IPython console:

```python
>>> import lifelib

>>> lifelib.create("ifrs17a", r"C:\path\to\your\myifrs17")
```
In case you've placed your copy in the current directory,
you can simply provide "myifrs17" as the second argument.
To check the location of the current
directory, `import os` then run `os.getcwd()`. To change the current directly,
use the `os.chdir` function.

Alternatively, you can do the same outside Python from a command prompt (or a shell on Linux).
To create *myifrs17* in the current directory, type:

```
> lifelib-create --template ifrs17a C:\path\to\your\myrfrs17
```

## Jupyter Notebooks

This library includes the following Jupyter Notebooks:

* {doc}`template_example` 
* {doc}`present_value_example_ep2`
* {doc}`present_value_example_ep3`
* {doc}`logic_inspection_example`

Each of the first three notebooks runs a corresponding Python script,
such `template.py`, `present_value_ep2.py` and  `present_value_ep3.py`,
and reproduces tables presented in Systemorph's videos.
The last notebook demonstrates how to inspect the calculation logic. 

To run any of the Jupyter notebooks, the current directory
of the notebook needs to be your copy of this library, 
so that modules in this library can be importable.
Normally, the current directory of a Jupyter notebook is 
set to the directory that the notebook was launched from.

```{admonition} Module search path
[`sys.path`](https://docs.python.org/3/library/sys.html#sys.path) 
holds a list of paths that Python searches for modules.
'' (the empty string) in the list indicates the current directory.
If you're having *ModuleNotFoundError*, check the list
and try inserting '' in the list.
```

## Python Scripts

As mentioned above, this library includes the following Python scripts:

* template_example.py 
* present_value_ep2.py
* present_value_ep3.py

Each of the scripts read an example data set, and calculate items for IFRS17.

### Template Example

`template.py` creates a `IfrsWorkspace` workspace object,
reads input data from Excel files in the *Files/ifrs-template* folder,
generates `IfrsVaribale` objects,
stores all of them into a pandas DataFrame
and assigns it to a global variable named `ifrsvars` for later use.
Each row in `ifrsvars` represents an `IfrsVariable` object.
A subset of rows, filtered by the EstimateType column,
composes an analysis-of-change table of a certain IFRS17 item, 
such as contractual service margin, as demonstrated in the accompanying 
Jupyter notebook, {doc}`template_example` .

The sample input data in the Excel files are taken from the CSV files
in [IFRS17CalculationEngine v1.0.0](https://github.com/Systemorph/IFRS17CalculationEngine/tree/v1.0.0/ifrs17-template/Files)

### Present Value Examples

`present_value_ep2.py` and `present_value_ep3.py` follow
the same as `template.py`, except that they only generate
`IfrsVariable` for the best estimate components
from smaller sets of input data in the *Files/present-values* folder.

`present_value_ep2.py` reads a sample data set for one reporting node
and one reporting period, while `present_value_ep3.py` reads a sample
for multiple reporting nodes and periods.

The sample input data  are taken from the CSV files
in [IFRS17CalculationEngine v1.0.0](https://github.com/Systemorph/IFRS17CalculationEngine/tree/v1.0.0/PresentValueSeries)

## Modules

The `ifrs17` package contains the following modules,
which form the central part of this library.

Since the modules were originally translated from C# to Python, 
the naming convention used in the modules does not adhere to Python's best practices.

* **BaseClasses**: This module includes base classes, including BaseDatabase, which is the base class of IfrsDatabase
* **Consts**: This module includes classes that define string keys, as described below.
* **Database**: This module includes IfrsDatabase, which is for storing calculation results as IfrsVariables
* **DataStructure**: This module includes several dataclasses that represents object identities and attributes.
* **Enums**: This module includes the definitions of constants.
* **Extensions**: This module includes some utility functions used from the ImportScopeCalculation module.
* **ImportCalculationMethods**: This module includes some utility functions used by other modules. 
* **Importers**: Import hooks by import formats are defined. 
* **ImportScopeCalculation**: This module includes IfrsWorkspace, IModel, IScope and various subclasses of IScope, which 
  collectively form the central part of the calculation logic.
* **ImportStorage**: ImportStorage class is defined in this module.
* **Validations**: Custom exception classes are defined in this module.


## Object Structure and Usage

Below is a class diagram that depicts relationships
among main classes in the modules. 
The classes are mostly implemented from scratch for this library.

```{mermaid}
classDiagram
    IfrsWorkspace o-- IfrsDatabase
    IfrsWorkspace o-- "0..n" ImportStorage
    IfrsWorkspace o-- "0..n" IModel
    BaseDatabase <|-- IfrsDatabase
class IfrsWorkspace{
    database
    models
    storages
    import_with_type()
    import_with_format()
}
class IfrsDatabase{

    get_ifrsvars()
}
class IModel{
    -storage
    -scope_cache
    debug()
}
class ImportStorage{
    -args
    -database
}
class BaseDatabase{
    -data
}
```

An IfrsWorkspace object contains one IfrsDatabase object 
and can possess multiple pairs of ImportStorage and IModel objects as its components. 

The IfrsDatabase is instantiated 
upon the creation of the IfrsWorkspace object.
It stores imported and calculated data
in the forms of objects of data types defined in the DataStructure module.
As demonstrated in the scripts,
the `import_with_type` method of IfrsDatabase reads 
data from multiple tabs in an Excel file.
The first parameter specifies the file path,
while the second parameter accepts a list of data types
to be imported. The names of the tabs in the file should match the names
of the types.

While `import_with_type` directly reads data into the IfrsDatabase object 
within the IfrsWorkspace, `import_with_format` invokes an import hook 
to process the data before storing it in the IfrsDatabase.
The import hooks, defined and registered by `ImportFormats` in the Importers module,
are functions whose names start with `_Format`.

The `format_` parameter of `import_with_format` specifies
which `ImportFormats` should be used. When `format_` is set to
`Cashflow`, `Actual`, or `Opening`, the selected hook creates
a pair of ImportStorage and IModel objects and invokes
the `compute` method of `IModel` at the end.

The ImportStorage object is an intermediate data storage for the paired IModel object.
The IModel object calculates IfrsVariables by recursively creating a variety of IScope objects,
as defined in the ImportScopeCalculation module, and invoking their methods and properties.
All the created IScope objects are retained, 
and their properties, once called, are cached after their initial invocation.
The IScope objects and their property values can be inspected 
to understand the calculation logic by using the `debug` method,
as demonstrated by the {doc}`logic_inspection_example` notebook.


```{note}
The logic defined in the ImportStorage and IScope classes is mostly based on
[the original implementation by Systemorph](https://github.com/Systemorph/IFRS17CalculationEngine/blob/v1.0.0/ifrs17/Import/ImportScopeCalculation.ipynb).
For more detailed explanations, refer to the original documentation linked above.
```

## Library Contents


| File or Folder                                                    | Description                                                             |
|-------------------------------------------------------------------|-------------------------------------------------------------------------|
| template.py                                                       | Python script for template example                                      |
| present_value_ep2.py                                              | Python script for present value episode 2 example                       |
| present_value_ep3.py                                              | Python script for present value episode 3 exmaple                       |
| {doc}`template_example.ipynb<template_example>`                   | Jupyter notebook to reproduce tables of template example                |
| {doc}`present_value_example_ep2.ipynb<present_value_example_ep2>` | Jupyter notebook to reproduce tables of present value example episode 2 |
| {doc}`present_value_example_ep3.ipynb<present_value_example_ep3>` | Jupyter notebook to reproduce tables of present value example episode 3 |
| {doc}`logic_inspection_example.ipynb<logic_inspection_example>`   | Jupyter notebook showing how to inspect the calculation logic           |
| pnl_mapping.xlsx                                                  | Excel file showing how to map IfrsVariables to P&L items                |



## String Keys

The Const module contains several classes that define string keys used to 
identify IfrsVariable objects.
The string keys appear in the columns of `ifrsvars` DataFrames
generated by the scripts. Below are the classes and their string keys.

```{list-table} Novelty
:header-rows: 1
:name: novelty

* - Key
  - Term
* - I
  - In-Force
* - N
  - New Business
* - C
  - Both Combined
```

```{list-table} AocType
:header-rows: 1
:name: aoc-type

* - Key
  - Term
* - BOP
  - Beginning of Period (opening value of an AOC chain)
* - MC
  - Model Corrections (changes to the model)
* - PC
  - Portfolio Changes
* - RCU
  - Reinsurance Coverage Update
* - CF
  - Cash flow (Nominal)
* - IA
  - Interest Accretion
* - AU
  - Assumptions Update (changes to general assumptions)
* - FAU
  - Financial Assumptions Update (changes to financial assumptions)
* - YCU
  - Yield Curve Update
* - CRU
  - Credit Default Risk Parameters Update    
* - WO
  - Write-off
* - EV
  - Experience Variance
* - CL
  - Combined Liabilities (control run where all changes are calculated together for all novelties)
* - EA
  - Experience Adjustment
* - AM
  - Amortization
* - FX
  - Foreing Exchange
* - EOP
  - End of Period (closing value of an AOC chain)
```

```{list-table} AmountType
:header-rows: 1
:name: amount-type

* - Key
  - Term
* - ACA
  - Attributable Commissions Acquisition
* - AEA
  - Attributable Expenses Acquisition
* - CDR
  - Credit Default Risk
* - CL
  - Claims
* - PR
  - Premiums
* - NIC
  - Claims Non-Investment component
* - ICO
  - Claims Investment component
* - NE
  - Non Attributable Expenses
* - ACM
  - Attributable Commissions Maintenance
* - AEM
  - Attributable Expenses Maintenance
* - AC
  - Attributable Commissions
* - AE
  - Attributable Expenses
```


```{list-table} EstimateType
:header-rows: 1
:name: estimate-type

* - Key
  - Term
* - BE
  - Best Estimate
* - RA
  - Risk Adjustment
* - CU
  - Coverage Units
* - A
  - Actuals
* - AA
  - Advance Actuals
* - OA
  - Overdue Actuals
* - DA
  - Deferrable Actuals
* - C
  - Contractual Service Margin
* - L
  - Loss Component
* - LR
  - Loss Recovery
* - F
  - Factors
* - FCF
  - Fulfilment Cash flows
* - BEPA
  - Experience Adjusted BE Premium to Csm
* - APA
  - Experience Adjusted Written Actual Premium to Csm
```

```{list-table} EconomicBasis
:header-rows: 1
:name: economic-basis

* - Key
  - Term
* - L
  - Locked Interest Rates
* - C
  - Current Interest Rates
* - N
  - Nominal Interest Rates
```

```{list-table} LiabilityTypes
:header-rows: 1
:name: liability-types

* - Key
  - Term
* - LRC
  - Liability for Remaining Coverage
* - LIC
  - Liability Incurred Claims
```


```{toctree}
---
hidden:
--- 
template_example
present_value_example_ep2
present_value_example_ep3
logic_inspection_example
```

